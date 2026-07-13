from __future__ import annotations

import re
import tempfile
import unittest
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from tests.site_harness import HugoSiteTestCase, ROOT


SAME_SITE_HOSTS = frozenset({"avisheksaha.com", "www.avisheksaha.com"})
MALFORMED_PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")


@dataclass(frozen=True)
class InvalidInternalLink:
    reason: str


def decode_url_path(encoded_path: str) -> str | InvalidInternalLink:
    if MALFORMED_PERCENT_ESCAPE.search(encoded_path):
        return InvalidInternalLink("URL path contains a malformed percent escape")
    try:
        path = unquote(encoded_path, encoding="utf-8", errors="strict")
    except (UnicodeError, ValueError) as error:
        return InvalidInternalLink(f"URL path is not valid UTF-8: {error}")
    if any(ord(character) < 32 or ord(character) == 127 for character in path):
        return InvalidInternalLink("URL path contains an ASCII control character")
    return path


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def internal_link_target(
    output_dir: Path, source_html: Path, href: str
) -> Path | InvalidInternalLink | None:
    """Return the generated target for a checkable internal href, if any."""

    href = href.strip()
    try:
        parsed = urlsplit(href)
    except (UnicodeError, ValueError) as error:
        return InvalidInternalLink(f"malformed URL: {error}")

    scheme = parsed.scheme.lower()
    if scheme not in ("", "http", "https"):
        return None
    if scheme in ("http", "https") and not parsed.netloc:
        return InvalidInternalLink("absolute HTTP(S) URL has no host")

    if parsed.netloc:
        try:
            hostname = (parsed.hostname or "").lower().rstrip(".")
            username = parsed.username
            password = parsed.password
            port = parsed.port
        except (UnicodeError, ValueError) as error:
            return InvalidInternalLink(f"malformed URL authority: {error}")
        if not hostname:
            return InvalidInternalLink("URL authority has no hostname")
        if "%" in hostname:
            return InvalidInternalLink("URL hostname contains percent escapes")
        if hostname not in SAME_SITE_HOSTS:
            external_path = decode_url_path(parsed.path or "/")
            return (
                external_path
                if isinstance(external_path, InvalidInternalLink)
                else None
            )
        if username is not None or password is not None:
            return InvalidInternalLink("same-site URL must not contain userinfo")
        effective_scheme = scheme or "https"
        expected_port = 80 if effective_scheme == "http" else 443
        if port is not None and port != expected_port:
            return InvalidInternalLink(
                f"unexpected {effective_scheme} port for same-site URL"
            )
    if not parsed.path and not parsed.netloc:
        return None

    try:
        site_root = output_dir.resolve(strict=False)
        source_path = source_html.resolve(strict=False)
        relative_source = source_path.relative_to(site_root).as_posix()
    except (OSError, RuntimeError, ValueError) as error:
        return InvalidInternalLink(f"source page is outside generated site: {error}")

    if relative_source == "index.html":
        source_url = "/"
    elif relative_source.endswith("/index.html"):
        source_url = "/" + relative_source.removesuffix("index.html")
    else:
        source_url = "/" + relative_source

    try:
        resolved = urlsplit(urljoin(f"https://avisheksaha.com{source_url}", href))
    except (UnicodeError, ValueError) as error:
        return InvalidInternalLink(f"URL resolution failed: {error}")

    decoded_path = decode_url_path(resolved.path or "/")
    if isinstance(decoded_path, InvalidInternalLink):
        return decoded_path
    path = decoded_path
    if ".." in path.split("/"):
        return InvalidInternalLink("URL path contains decoded traversal")

    try:
        candidate = (site_root / path.lstrip("/")).resolve(strict=False)
        candidate.relative_to(site_root)
        if path.endswith("/"):
            target = candidate / "index.html"
        elif candidate.is_file():
            target = candidate
        elif candidate.is_dir() or candidate.suffix == "":
            target = candidate / "index.html"
        else:
            target = candidate
        target = target.resolve(strict=False)
        target.relative_to(site_root)
    except (OSError, RuntimeError, ValueError) as error:
        return InvalidInternalLink(f"URL target is outside generated site: {error}")
    return target


def broken_internal_links(output_dir: Path) -> list[str]:
    failures: list[str] = []
    for html_path in sorted(output_dir.rglob("*.html")):
        parser = LinkCollector()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for href in parser.links:
            candidate = internal_link_target(output_dir, html_path, href)
            if isinstance(candidate, InvalidInternalLink) or (
                isinstance(candidate, Path) and not candidate.is_file()
            ):
                failures.append(f"{html_path.relative_to(output_dir)} -> {href}")
    return failures


class InternalLinkResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory(
            prefix="portfolio-link-contract-"
        )
        self.addCleanup(self._temporary_directory.cleanup)
        fixture_root = Path(self._temporary_directory.name)
        self.output_dir = fixture_root / "site"
        outside_dir = fixture_root / "outside"
        self.output_dir.mkdir()
        outside_dir.mkdir()
        for relative_path in (
            "index.html",
            "experience/index.html",
            "posts/index.html",
            "posts/example/index.html",
            "assets/report.pdf",
            "images/system diagram.png",
        ):
            path = self.output_dir / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        (outside_dir / "secret.txt").write_text("outside site root", encoding="utf-8")
        (self.output_dir / "escape").symlink_to(outside_dir, target_is_directory=True)
        self.source_html = self.output_dir / "posts/example/index.html"

    def assert_resolves(self, href: str, expected: str) -> None:
        target = internal_link_target(self.output_dir, self.source_html, href)
        self.assertIsNotNone(target, href)
        self.assertIsInstance(target, Path, href)
        self.assertEqual(target, self.output_dir / expected)
        self.assertTrue(target.is_file(), f"Expected fixture target for {href}: {target}")
        target.resolve(strict=False).relative_to(self.output_dir.resolve(strict=False))

    def assert_invalid(self, href: str) -> None:
        try:
            target = internal_link_target(self.output_dir, self.source_html, href)
        except Exception as error:  # pragma: no cover - assertion reports the defect
            self.fail(f"Malformed internal href raised {type(error).__name__}: {href}")
        self.assertIsNotNone(target, href)
        self.assertNotIsInstance(
            target,
            Path,
            f"Invalid href must not expose a filesystem candidate: {href} -> {target}",
        )

    def test_root_relative_extensionless_and_file_links_resolve(self) -> None:
        for href, expected in (
            ("/", "index.html"),
            ("/experience/", "experience/index.html"),
            ("/experience", "experience/index.html"),
            ("/assets/report.pdf", "assets/report.pdf"),
        ):
            with self.subTest(href=href):
                self.assert_resolves(href, expected)

    def test_relative_links_resolve_from_the_source_route(self) -> None:
        for href, expected in (
            ("../", "posts/index.html"),
            ("../../experience/", "experience/index.html"),
            ("./", "posts/example/index.html"),
        ):
            with self.subTest(href=href):
                self.assert_resolves(href, expected)

    def test_same_site_absolute_links_queries_fragments_and_encoding_resolve(self) -> None:
        for href, expected in (
            ("https://avisheksaha.com", "index.html"),
            ("//www.avisheksaha.com?source=nav#top", "index.html"),
            ("https://avisheksaha.com:443/experience/", "experience/index.html"),
            ("http://avisheksaha.com:80/experience/", "experience/index.html"),
            ("//avisheksaha.com:443/experience/", "experience/index.html"),
            (
                "https://avisheksaha.com/experience/?source=portfolio#roles",
                "experience/index.html",
            ),
            (
                "https://www.avisheksaha.com/posts/#writing",
                "posts/index.html",
            ),
            ("/images/system%20diagram.png?download=1", "images/system diagram.png"),
        ):
            with self.subTest(href=href):
                self.assert_resolves(href, expected)

    def test_external_and_non_navigating_links_are_ignored(self) -> None:
        for href in (
            "mailto:hello@example.com",
            "tel:+16045550123",
            "#section",
            "?filter=ai#results",
            "javascript:void(0)",
            "data:text/plain,example",
            "https://github.com/sahaavi",
            "https://user@github.com:444/sahaavi?tab=repositories#readme",
            "//cdn.example.com/library.css",
        ):
            with self.subTest(href=href):
                self.assertIsNone(
                    internal_link_target(self.output_dir, self.source_html, href)
                )

    def test_missing_internal_route_returns_an_actionable_candidate(self) -> None:
        target = internal_link_target(
            self.output_dir, self.source_html, "/missing-route/?source=test#detail"
        )
        self.assertEqual(target, self.output_dir / "missing-route/index.html")
        self.assertFalse(target.exists())

    def test_percent_decoded_traversal_is_invalid_before_filesystem_access(self) -> None:
        for href in (
            "/%2e%2e/etc/passwd",
            "/%2e%2e/%2e%2e/etc/passwd",
            "/%2E%2E/%2E%2E/etc/passwd",
            "/posts/%2e%2e/experience/",
            "/%2e%2e%2fetc/passwd",
        ):
            with self.subTest(href=href):
                self.assert_invalid(href)

    def test_decoded_ascii_controls_and_invalid_utf8_are_invalid(self) -> None:
        for href in (
            "/%00",
            "/%01",
            "/%09",
            "/%0A",
            "/%0D",
            "/%1F",
            "/%7F",
            "/%FF",
            "/%E2%82",
            "/%",
            "/%2",
            "/%GG",
        ):
            with self.subTest(href=href):
                self.assert_invalid(href)

    def test_malformed_or_noncanonical_same_site_authorities_are_invalid(self) -> None:
        for href in (
            "http://[::1",
            "https:relative-without-a-host",
            "https://avisheksaha.com:notaport/experience/",
            "https://avisheksaha.com:99999/experience/",
            "https://avisheksaha.com:444/experience/",
            "//avisheksaha.com:80/experience/",
            "https://user@avisheksaha.com/experience/",
            "https://user:secret@avisheksaha.com/experience/",
            "https://@avisheksaha.com/experience/",
        ):
            with self.subTest(href=href):
                self.assert_invalid(href)

    def test_malformed_external_http_paths_are_invalid(self) -> None:
        for href in (
            "https://github.com/%00",
            "https://github.com/%FF",
            "https://github.com/%GG",
        ):
            with self.subTest(href=href):
                self.assert_invalid(href)

    def test_symlink_targets_outside_the_generated_site_are_invalid(self) -> None:
        self.assert_invalid("/escape/secret.txt")


class InternalLinkTests(HugoSiteTestCase):
    def test_generated_internal_links_resolve(self) -> None:
        failures = broken_internal_links(self.output_dir)
        self.assertEqual([], failures, "Broken internal links:\n" + "\n".join(failures))

    def test_generated_link_scan_reports_malformed_hrefs_actionably(self) -> None:
        fixture = self.output_dir / "invalid-link-fixture.html"
        invalid_hrefs = (
            "/%2e%2e/%2e%2e/etc/passwd",
            "/%00",
            "http://[::1",
        )
        fixture.write_text(
            "".join(f'<a href="{href}">invalid</a>' for href in invalid_hrefs),
            encoding="utf-8",
        )
        try:
            failures = broken_internal_links(self.output_dir)
            for href in invalid_hrefs:
                self.assertIn(f"invalid-link-fixture.html -> {href}", failures)
        finally:
            fixture.unlink(missing_ok=True)

    def test_legacy_custom_stylesheet_is_removed(self) -> None:
        self.assertFalse(
            (ROOT / "assets/css/extended/custom.css").exists(),
            "Legacy custom.css must be removed after its live blog rules are scoped.",
        )

    def test_blog_styles_are_scoped_and_present_in_the_generated_bundle(self) -> None:
        path = ROOT / "assets/css/extended/portfolio-blog.css"
        self.assertTrue(path.is_file(), f"Expected scoped blog stylesheet: {path}")
        css = path.read_text(encoding="utf-8")

        required_selectors = (
            ".blog-list",
            ".blog-empty",
            ".blog-list-item",
            ".blog-list-title",
            ".blog-list-meta",
            ".blog-list-tags",
            ".blog-tag",
            ".blog-shell",
            ".blog-article",
            ".blog-meta",
            ".blog-sidebar",
            ".blog-toc",
            ".blog-series-nav",
            ".blog-mobile-toc",
            ".blog-tags",
            ".blog-post-nav",
            ".blog-post-nav-link",
        )
        for selector in required_selectors:
            with self.subTest(selector=selector):
                self.assertIn(selector, css)

        self.assertIn("@media (max-width: 960px)", css)
        self.assertIn("@media (max-width: 768px)", css)
        self.assertEqual(css.count("@media"), 2)
        self.assertIn("grid-template-columns: minmax(150px, 0.28fr)", css)
        self.assertIn("position: sticky", css)

        for obsolete_selector in (
            ".hero-greeting",
            ".flagship-layout",
            ".case-study-grid",
            ".projects-grid",
            ".project-card",
            ".social-icons",
            ".dark",
            ".portfolio-",
            "@font-face",
            "html {",
            "body {",
            ":root",
        ):
            with self.subTest(obsolete_selector=obsolete_selector):
                self.assertNotIn(obsolete_selector, css)

        posts_html = self.page_html("/posts/")
        post_html = self.page_html("/posts/llm-engineering-from-scratch-tokenizer/")
        for rendered_class, rendered_html in (
            ('class="blog-list"', posts_html),
            ('class="blog-list-item"', posts_html),
            ('class="blog-shell"', post_html),
            ('class="blog-article"', post_html),
            ('class="blog-mobile-toc"', post_html),
            ('class="blog-sidebar blog-series-nav"', post_html),
            ('class="blog-sidebar blog-toc"', post_html),
        ):
            with self.subTest(rendered_class=rendered_class):
                self.assertIn(rendered_class, rendered_html)

        css_paths = sorted(self.output_dir.rglob("*.css"))
        self.assertTrue(css_paths, "Expected Hugo to emit a CSS bundle")
        generated_css = "\n".join(
            css_path.read_text(encoding="utf-8") for css_path in css_paths
        )
        for selector in (".blog-list-item", ".blog-shell", ".blog-mobile-toc"):
            with self.subTest(generated_selector=selector):
                self.assertIn(selector, generated_css)

    def test_deployment_runs_contracts_before_a_warning_clean_hugo_build(self) -> None:
        workflow = (ROOT / ".github/workflows/hugo.yml").read_text(encoding="utf-8")
        expected_markers = (
            "- name: Checkout",
            "- name: Setup Pages",
            "- name: Run site contract tests",
            "- name: Build with Hugo",
            "- name: Upload artifact",
        )
        for marker in expected_markers:
            self.assertIn(marker, workflow)
        marker_positions = [workflow.index(marker) for marker in expected_markers]
        self.assertEqual(marker_positions, sorted(marker_positions))
        self.assertIn("python3 -m unittest discover -s tests -v", workflow)

        build_block = workflow.split("- name: Build with Hugo", 1)[1].split(
            "- name: Upload artifact", 1
        )[0]
        for flag in ("--gc", "--minify", "--cleanDestinationDir", "--panicOnWarning"):
            with self.subTest(flag=flag):
                self.assertIn(flag, build_block)

        for preserved_contract in (
            "submodules: recursive",
            "actions/configure-pages@v5",
            "actions/upload-pages-artifact@v3",
            "actions/deploy-pages@v4",
        ):
            with self.subTest(preserved_contract=preserved_contract):
                self.assertIn(preserved_contract, workflow)
