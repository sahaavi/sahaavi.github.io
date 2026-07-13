from __future__ import annotations

import re
import shutil
import struct
import subprocess
import tempfile
from html import unescape
from pathlib import Path
from typing import Callable

from tests.site_harness import HugoSiteTestCase, ROOT


class ProjectContractTests(HugoSiteTestCase):
    def build_with_project_fixture(
        self,
        project_path: str,
        transform: Callable[[str], str],
        *,
        consumer: str = "full",
        bundle_files: dict[str, str] | None = None,
        site_files: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="portfolio-project-invalid-") as temp:
            source = Path(temp) / "site"
            shutil.copytree(
                ROOT,
                source,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".gstack",
                    ".hugo_build.lock",
                    "__pycache__",
                    "public",
                    "resources",
                ),
            )
            project = source / project_path
            original = project.read_text(encoding="utf-8")
            transformed = transform(original)
            self.assertNotEqual(transformed, original, f"Fixture did not modify {project_path}")
            project.write_text(transformed, encoding="utf-8")
            for filename, contents in (bundle_files or {}).items():
                resource = project.parent / filename
                self.assertFalse(
                    resource.exists(), f"Fixture resource already exists: {filename}"
                )
                resource.write_text(contents, encoding="utf-8")
            for relative_path, contents in (site_files or {}).items():
                fixture_file = source / relative_path
                self.assertFalse(
                    fixture_file.exists(),
                    f"Fixture site file already exists: {relative_path}",
                )
                fixture_file.parent.mkdir(parents=True, exist_ok=True)
                fixture_file.write_text(contents, encoding="utf-8")

            if consumer in {"list", "single"}:
                (source / "layouts/_default/baseof.html").write_text(
                    '<!doctype html><html><body>{{ block "main" . }}{{ end }}</body></html>\n',
                    encoding="utf-8",
                )
                (source / "layouts/index.html").write_text(
                    '{{ define "main" }}<p>Project validation fixture</p>{{ end }}\n',
                    encoding="utf-8",
                )
                with (source / "hugo.yaml").open("a", encoding="utf-8") as config:
                    config.write(
                        '\ndisableKinds: ["taxonomy", "term", "RSS", "sitemap", "robotsTXT", "404"]\n'
                    )
            if consumer == "list":
                (source / "layouts/projects/single.html").write_text(
                    '{{ define "main" }}<article>Single fixture</article>{{ end }}\n',
                    encoding="utf-8",
                )
            elif consumer == "single":
                (source / "layouts/projects/list.html").write_text(
                    '{{ define "main" }}<section>List fixture</section>{{ end }}\n',
                    encoding="utf-8",
                )
            elif consumer != "full":
                self.fail(f"Unsupported fixture consumer: {consumer}")

            return subprocess.run(
                [
                    "hugo",
                    "--gc",
                    "--minify",
                    "--enableGitInfo=false",
                    "--cleanDestinationDir",
                    "--destination",
                    str(source / "public"),
                ],
                cwd=source,
                check=False,
                capture_output=True,
                text=True,
            )

    def assert_project_fixture_error(
        self,
        project_path: str,
        transform: Callable[[str], str],
        expected_error: str,
        *,
        consumer: str = "full",
    ) -> None:
        result = self.build_with_project_fixture(
            project_path, transform, consumer=consumer
        )
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(project_path.removeprefix("content/"), output)
        self.assertIn(expected_error, output)
        for generic_error in (
            "can't evaluate field",
            "error calling Width",
            "nil pointer evaluating",
            "range can't iterate over",
            "this method is only available for image resources",
            "this method is only available for raster images",
            "wrong type for value",
        ):
            self.assertNotIn(generic_error, output)

    def test_work_index_has_three_evidence_groups(self) -> None:
        html = unescape(self.page_html("/projects/"))
        self.assertIn(
            "Selected AI systems, machine-learning work, technical labs, and research foundations.",
            html,
        )
        self.assertEqual(html.count('class="portfolio-project-group"'), 3)
        self.assertEqual(html.count('class="portfolio-project-card"'), 4)
        element_ids = re.findall(r'\sid="([^"]+)"', html)
        self.assertEqual(len(element_ids), len(set(element_ids)))

        group_contract = (
            (
                "Featured AI Systems",
                ("Maintenance-Eye", "GovIntel"),
                "ML Systems & Labs",
            ),
            (
                "ML Systems & Labs",
                ("LLM Engineering From Scratch",),
                "Research & Foundations",
            ),
            (
                "Research & Foundations",
                ("Autism Screening Data Dashboard Research",),
                "</main>",
            ),
        )
        cursor = -1
        for heading, titles, next_marker in group_contract:
            with self.subTest(group=heading):
                heading_index = html.find(f">{heading}</h2>", cursor + 1)
                self.assertGreater(heading_index, cursor, heading)
                next_index = html.find(next_marker, heading_index + 1)
                self.assertGreater(next_index, heading_index, next_marker)
                group = html[heading_index:next_index]
                self.assertEqual(group.count('class="portfolio-project-card"'), len(titles))
                title_cursor = -1
                for title in titles:
                    title_index = group.find(title, title_cursor + 1)
                    self.assertGreater(title_index, title_cursor, title)
                    title_cursor = title_index
                cursor = heading_index

        for draft_title in ("Pennymize", "Price Prediction Platform on AWS"):
            self.assertNotIn(draft_title, html)
        for draft_route in ("/projects/pennymize/", "/projects/price-prediction-aws/"):
            self.assertFalse(self.page_path(draft_route).exists(), draft_route)

        list_layout = (ROOT / "layouts/projects/list.html").read_text(encoding="utf-8")
        self.assertNotIn("project group cardinality", list_layout)
        self.assertNotIn("$featuredCount", list_layout)
        self.assertNotIn("$labsCount", list_layout)
        self.assertNotIn("$researchCount", list_layout)

    def test_project_cards_show_status_role_and_year(self) -> None:
        html = unescape(self.page_html("/projects/"))
        card_contract = (
            ("Maintenance-Eye", "Public demo", "Builder", "2026"),
            ("GovIntel", "Public repository", "Builder", "2026"),
            (
                "LLM Engineering From Scratch",
                "In-progress lab series",
                "Builder and writer",
                "2026",
            ),
            (
                "Autism Screening Data Dashboard Research",
                "Published research",
                "Research contributor",
                "2021",
            ),
        )
        articles = html.split('<article class="portfolio-project-card"')[1:]
        self.assertEqual(len(articles), len(card_contract))
        for article, (title, status, role, year) in zip(articles, card_contract):
            card = article.split("</article>", 1)[0]
            with self.subTest(project=title):
                for text in (title, status, role, year):
                    self.assertIn(text, card)
                self.assertIn(f'aria-label="Open {title} case study"', card)
        self.assertNotIn("portfolio-project-metric", html)
        self.assertIn(
            "An expanding LLM engineering lab, currently featuring a runnable "
            "byte-level BPE tokenizer, failure analysis, and an interactive demo, "
            "with later model components on the roadmap.",
            html,
        )
        self.assertNotIn(
            "rebuilds LLM mechanics from tokenization to evaluation", html
        )

    def test_middle_project_has_independent_previous_and_next_links(self) -> None:
        html = unescape(self.page_html("/projects/govtintel/"))
        self.assertEqual(html.count('<nav class="paginav"'), 1)
        navigation = html.split('<nav class="paginav"', 1)[1].split("</nav>", 1)[0]
        self.assertIn('aria-label="Project navigation"', navigation)
        self.assertIn("Previous Project", navigation)
        self.assertIn("Next Project", navigation)
        self.assertIn('/projects/llm-engineering-from-scratch/', navigation)
        self.assertIn('/projects/maintenance-eye/', navigation)
        self.assertIn(
            'aria-label="Previous project: LLM Engineering From Scratch"', navigation
        )
        self.assertIn('aria-label="Next project: Maintenance-Eye"', navigation)

        first = unescape(self.page_html("/projects/maintenance-eye/"))
        first_nav = first.split('<nav class="paginav"', 1)[1].split("</nav>", 1)[0]
        self.assertEqual(first_nav.count("Previous Project"), 1)
        self.assertNotIn("Next Project", first_nav)
        self.assertEqual(first_nav.count("<a "), 1)

        last = unescape(
            self.page_html("/projects/autism-spectrum-disorder-prediction/")
        )
        last_nav = last.split('<nav class="paginav"', 1)[1].split("</nav>", 1)[0]
        self.assertNotIn("Previous Project", last_nav)
        self.assertEqual(last_nav.count("Next Project"), 1)
        self.assertEqual(last_nav.count("<a "), 1)

    def test_project_images_are_local_and_single_pages_keep_evidence(self) -> None:
        index_html = unescape(self.page_html("/projects/"))
        index_cards = [
            article.split("</article>", 1)[0]
            for article in index_html.split(
                '<article class="portfolio-project-card"'
            )[1:]
        ]
        self.assertEqual(len(index_cards), 4)
        maintenance_card, govintel_card, _, research_card = index_cards

        maintenance_system_label = (
            "Maintenance-Eye system components: Camera + voice, Gemini Live, "
            "User response, FastAPI, 9 guarded tools, Approval gate"
        )
        self.assertIn(
            'class="portfolio-project-cover portfolio-project-system-map"',
            maintenance_card,
        )
        self.assertIn('role="img"', maintenance_card)
        self.assertIn(
            f'aria-label="{maintenance_system_label}"', maintenance_card
        )
        for label in (
            "Camera + voice",
            "Gemini Live",
            "User response",
            "FastAPI",
            "9 guarded tools",
            "Approval gate",
        ):
            with self.subTest(system_label=label):
                self.assertEqual(maintenance_card.count(f">{label}</span>"), 1)
        self.assertEqual(maintenance_card.count('aria-hidden="true"'), 6)
        self.assertIn(
            '<span aria-hidden="true" class="is-accent">Gemini Live</span>',
            maintenance_card,
        )
        self.assertIn(
            '<span aria-hidden="true" class="is-accent">9 guarded tools</span>',
            maintenance_card,
        )

        self.assertIn(
            'class="portfolio-project-cover"', govintel_card
        )
        self.assertIn(
            '/projects/govtintel/govintel-ui.png', govintel_card
        )
        self.assertNotIn("portfolio-project-system-map", govintel_card)
        self.assertNotIn("portfolio-project-cover--text", govintel_card)

        self.assertIn(
            'class="portfolio-project-cover portfolio-project-cover--text" '
            'aria-hidden="true"',
            research_card,
        )
        self.assertIn(">Machine learning</span>", research_card)
        self.assertNotIn('role="img"', research_card)

        cover_contract = (
            (
                "content/projects/govtintel/govintel-ui.png",
                "/projects/govtintel/govintel-ui.png",
            ),
            (
                "content/projects/llm-engineering-from-scratch/cover.png",
                "/projects/llm-engineering-from-scratch/cover.png",
            ),
        )
        for relative_path, public_path in cover_contract:
            with self.subTest(image=relative_path):
                image_path = ROOT / relative_path
                self.assertTrue(image_path.is_file(), relative_path)
                data = image_path.read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                width, height = struct.unpack(">II", data[16:24])
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)
                self.assertIn(public_path, index_html)

        architecture_path = (
            ROOT / "content/projects/vision-maintenance-agent/architecture.png"
        )
        self.assertTrue(architecture_path.is_file())
        architecture_public_path = "/projects/maintenance-eye/architecture.png"
        self.assertNotIn(architecture_public_path, index_html)
        self.assertNotIn("/projects/maintenance-eye/architecture", index_html)

        raw_github = "https://" + "raw.githubusercontent.com"
        remote_urls = (
            f"{raw_github}/sahaavi/Maintenance-Eye/main/docs/architecture.png",
            f"{raw_github}/sahaavi/GovtIntel/main/docs/assets/govintel-ui.png",
        )
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "content/projects").glob("*/index.md")
        )
        rendered = "\n".join(
            self.page_html(route)
            for route in (
                "/projects/",
                "/projects/maintenance-eye/",
                "/projects/govtintel/",
            )
        )
        for remote_url in remote_urls:
            self.assertNotIn(remote_url, source)
            self.assertNotIn(remote_url, rendered)

        maintenance_source = (
            ROOT / "content/projects/vision-maintenance-agent/index.md"
        ).read_text(encoding="utf-8")
        self.assertIn('  image: ""', maintenance_source)
        self.assertNotIn("  fit: contain", maintenance_source)

        maintenance_html = unescape(self.page_html("/projects/maintenance-eye/"))
        maintenance_alt = (
            "Maintenance-Eye architecture diagram showing the multimodal client, "
            "AI agent, backend services, and deployment components"
        )
        self.assertNotIn('class="entry-cover', maintenance_html)
        self.assertEqual(maintenance_html.count(f'alt="{maintenance_alt}"'), 1)
        preview_match = re.search(
            rf'<img src="(?P<src>[^"]+\.webp)" width="(?P<width>\d+)" '
            rf'height="(?P<height>\d+)" alt="{re.escape(maintenance_alt)}" '
            r'loading="lazy" decoding="async">',
            maintenance_html,
        )
        self.assertIsNotNone(preview_match, maintenance_html)
        assert preview_match is not None
        self.assertEqual(int(preview_match.group("width")), 2360)
        self.assertGreater(int(preview_match.group("height")), 0)
        preview_path = self.output_dir / preview_match.group("src").lstrip("/")
        self.assertTrue(preview_path.is_file(), preview_path)
        self.assertLess(preview_path.stat().st_size, architecture_path.stat().st_size)
        self.assertEqual(maintenance_html.count(architecture_public_path), 1)
        self.assertIn(
            f'href="{architecture_public_path}"', maintenance_html
        )
        self.assertIn("View full-resolution architecture diagram", maintenance_html)

        single_contract = (
            (
                "/projects/maintenance-eye/",
                "Public demo",
                "Builder",
                "2026",
                None,
            ),
            (
                "/projects/govtintel/",
                "Public repository",
                "Builder",
                "2026",
                "GovIntel Streamlit UI showing a generated procurement intelligence brief",
            ),
            (
                "/projects/llm-engineering-from-scratch/",
                "In-progress lab series",
                "Builder and writer",
                "2026",
                "Abstract BPE token tiles used as the cover for LLM Engineering From Scratch",
            ),
            (
                "/projects/autism-spectrum-disorder-prediction/",
                "Published research",
                "Research contributor",
                "2021",
                None,
            ),
        )
        for route, status, role, year, image_alt in single_contract:
            html = unescape(self.page_html(route))
            with self.subTest(route=route):
                self.assertIn('class="post-single portfolio-project-single"', html)
                header = html.split('<header class="post-header">', 1)[1].split(
                    "</header>", 1
                )[0]
                for text in (status, role, year):
                    self.assertIn(text, header)
                self.assertIn('id="toc-container"', html)
                self.assertIn('class="post-content"', html)
                if image_alt is not None:
                    self.assertIn(f'alt="{image_alt}"', html)

        for route in (
            "/projects/govtintel/",
            "/projects/llm-engineering-from-scratch/",
        ):
            html = unescape(self.page_html(route))
            cover = html.split('<figure class="entry-cover', 1)[1].split(
                "</figure>", 1
            )[0]
            with self.subTest(eager_cover=route):
                self.assertIn('loading="eager"', cover)
                self.assertIn('fetchpriority="high"', cover)
                self.assertIn('decoding="async"', cover)
                self.assertNotIn('loading="lazy"', cover)

        shortcode = ROOT / "layouts/shortcodes/project-image.html"
        self.assertTrue(shortcode.is_file())
        single_layout = (ROOT / "layouts/projects/single.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('loading="eager"', single_layout)
        self.assertIn('fetchpriority="high"', single_layout)

        system_map_partial = ROOT / "layouts/partials/system-map.html"
        self.assertTrue(system_map_partial.is_file())
        list_layout = (ROOT / "layouts/projects/list.html").read_text(
            encoding="utf-8"
        )
        home_layout = (
            ROOT / "layouts/partials/home/selected-work.html"
        ).read_text(encoding="utf-8")
        self.assertIn('partial "system-map.html"', list_layout)
        self.assertIn('partial "system-map.html"', home_layout)

    def test_project_styles_support_balanced_cards_and_the_exact_breakpoint(self) -> None:
        stylesheet_path = ROOT / "assets/css/extended/portfolio-projects.css"
        self.assertTrue(stylesheet_path.is_file())
        css = stylesheet_path.read_text(encoding="utf-8")
        grid = css.split(".portfolio-project-grid {", 1)[1].split("}", 1)[0]
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", grid)
        self.assertIn("align-items: stretch", grid)

        card = css.split(".portfolio-project-card {", 1)[1].split("}", 1)[0]
        self.assertIn("display: flex", card)
        self.assertIn("flex-direction: column", card)
        self.assertIn("min-height: 100%", card)
        content = css.split(".portfolio-project-content {", 1)[1].split("}", 1)[0]
        self.assertIn("flex: 1", content)
        self.assertIn("display: flex", content)
        cta = css.rsplit(".portfolio-project-cta {", 1)[1].split("}", 1)[0]
        self.assertIn("min-height: 44px", cta)
        self.assertIn("margin-top: auto", cta)

        contain = css.split(
            ".portfolio-project-cover.is-contain img {", 1
        )[1].split("}", 1)[0]
        self.assertIn("object-fit: contain", contain)
        cover_slot = css.split(".portfolio-project-cover {", 1)[1].split("}", 1)[0]
        self.assertIn("aspect-ratio: 16 / 9", cover_slot)
        self.assertIn("background: var(--portfolio-surface-soft)", cover_slot)
        self.assertIn(".portfolio-project-system-map {", css)
        system_map = css.split(
            ".portfolio-project-system-map {", 1
        )[1].split("}", 1)[0]
        self.assertIn("display: grid", system_map)
        self.assertIn("grid-template-columns: repeat(3, minmax(0, 1fr))", system_map)
        system_node = css.split(
            ".portfolio-project-system-map span {", 1
        )[1].split("}", 1)[0]
        self.assertIn("background: var(--portfolio-surface)", system_node)
        self.assertIn("border: 1px solid var(--portfolio-line-strong)", system_node)
        system_accent = css.split(
            ".portfolio-project-system-map .is-accent {", 1
        )[1].split("}", 1)[0]
        self.assertIn("color: var(--portfolio-blue)", system_accent)
        self.assertIn("background: var(--portfolio-blue-soft)", system_accent)
        text_fallback = css.split(
            ".portfolio-project-cover--text {", 1
        )[1].split("}", 1)[0]
        self.assertIn("display: grid", text_fallback)
        self.assertIn("color: var(--portfolio-ink-soft)", text_fallback)
        navigation = css.split(
            ".portfolio-project-single .paginav a {", 1
        )[1].split("}", 1)[0]
        self.assertIn("min-height: 44px", navigation)
        single_navigation = css.split(
            ".portfolio-project-single .paginav a:only-child {", 1
        )[1].split("}", 1)[0]
        self.assertIn("width: 100%", single_navigation)

        self.assertIn("@media (max-width: 720px)", css)
        mobile = css.split("@media (max-width: 720px)", 1)[1]
        mobile_grid = mobile.split(".portfolio-project-grid {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("grid-template-columns: 1fr", mobile_grid)
        self.assertNotIn("@media (max-width: 721px)", css)

    def test_project_archetype_captures_portfolio_metadata(self) -> None:
        archetype = (ROOT / "archetypes/projects.md").read_text(encoding="utf-8")
        for field in (
            'portfolio_group: "ml-labs"',
            'portfolio_status: "Prototype"',
            'portfolio_category: ""',
            'portfolio_role: "Builder"',
            "portfolio_year: {{ now.Year }}",
            'repository_url: ""',
            "home_featured: false",
            "home_order: 99",
            'home_summary: ""',
            "system_map: []",
        ):
            with self.subTest(field=field):
                self.assertIn(field, archetype)

    def test_list_and_single_routes_share_project_validation(self) -> None:
        project_path = "content/projects/asd-prediction/index.md"
        transform = lambda text: text.replace(
            'portfolio_group: "research"', 'portfolio_group: "unknown"'
        )
        expected = (
            "portfolio_group must be one of featured-ai, ml-labs, or research"
        )
        for consumer in ("list", "single"):
            with self.subTest(consumer=consumer):
                self.assert_project_fixture_error(
                    project_path, transform, expected, consumer=consumer
                )

    def test_project_validation_rejects_malformed_required_metadata(self) -> None:
        asd = "content/projects/asd-prediction/index.md"
        cases = (
            (
                "blank title",
                asd,
                lambda text: re.sub(r'(?m)^title: .+$', 'title: "   "', text, count=1),
                "project title must be a nonblank string",
            ),
            (
                "blank description",
                asd,
                lambda text: re.sub(
                    r'(?m)^description: .+$', 'description: ""', text, count=1
                ),
                "project description must be a nonblank string",
            ),
            (
                "missing group",
                asd,
                lambda text: re.sub(r'(?m)^portfolio_group:.*\n', "", text, count=1),
                "portfolio_group must be one of featured-ai, ml-labs, or research",
            ),
            (
                "unknown group",
                asd,
                lambda text: text.replace(
                    'portfolio_group: "research"', 'portfolio_group: "unknown"'
                ),
                "portfolio_group must be one of featured-ai, ml-labs, or research",
            ),
            (
                "status type",
                asd,
                lambda text: re.sub(
                    r'(?m)^portfolio_status: .+$', "portfolio_status: 42", text, count=1
                ),
                "portfolio_status, portfolio_category, and portfolio_role must be nonblank strings",
            ),
            (
                "blank category",
                asd,
                lambda text: re.sub(
                    r'(?m)^portfolio_category: .+$', 'portfolio_category: ""', text, count=1
                ),
                "portfolio_status, portfolio_category, and portfolio_role must be nonblank strings",
            ),
            (
                "blank role",
                asd,
                lambda text: re.sub(
                    r'(?m)^portfolio_role: .+$', 'portfolio_role: "   "', text, count=1
                ),
                "portfolio_status, portfolio_category, and portfolio_role must be nonblank strings",
            ),
            (
                "year type",
                asd,
                lambda text: text.replace("portfolio_year: 2021", 'portfolio_year: "2021"'),
                "portfolio_year must be an integer from 2000 through 2100",
            ),
            (
                "year range",
                asd,
                lambda text: text.replace("portfolio_year: 2021", "portfolio_year: 2101"),
                "portfolio_year must be an integer from 2000 through 2100",
            ),
            (
                "home featured type",
                asd,
                lambda text: text.replace("home_featured: false", 'home_featured: "false"'),
                "home_featured must be boolean",
            ),
            (
                "repository type",
                asd,
                lambda text: re.sub(
                    r'(?m)^repository_url: .+$', "repository_url: 42", text, count=1
                ),
                "repository_url must be a string",
            ),
            (
                "repository scheme",
                asd,
                lambda text: re.sub(
                    r'(?m)^repository_url: .+$',
                    'repository_url: "http://example.com/repo"',
                    text,
                    count=1,
                ),
                "repository_url must be blank or an absolute HTTPS URL with a valid host and no port",
            ),
            (
                "repository port",
                asd,
                lambda text: re.sub(
                    r'(?m)^repository_url: .+$',
                    'repository_url: "https://example.com:443/repo"',
                    text,
                    count=1,
                ),
                "repository_url must be blank or an absolute HTTPS URL with a valid host and no port",
            ),
        )
        for label, project_path, transform, expected in cases:
            with self.subTest(case=label):
                self.assert_project_fixture_error(project_path, transform, expected)

    def test_project_validation_rejects_malformed_or_missing_local_covers(self) -> None:
        project_path = "content/projects/govtintel/index.md"
        cases = (
            (
                "missing cover",
                lambda text: re.sub(
                    r"(?m)^cover:\n(?: {2}[^\n]*\n)+", "", text, count=1
                ),
                "project cover must be a map",
            ),
            (
                "cover type",
                lambda text: text.replace("cover:\n", 'cover: "govintel-ui.png"\nignored_cover:\n', 1),
                "project cover must be a map",
            ),
            (
                "image type",
                lambda text: re.sub(r'(?m)^  image: .+$', "  image: 42", text, count=1),
                "cover image and alt must be strings and relative must be boolean",
            ),
            (
                "alt type",
                lambda text: re.sub(r'(?m)^  alt: .+$', "  alt: 42", text, count=1),
                "cover image and alt must be strings and relative must be boolean",
            ),
            (
                "relative type",
                lambda text: re.sub(
                    r'(?m)^  relative: .+$', '  relative: "true"', text, count=1
                ),
                "cover image and alt must be strings and relative must be boolean",
            ),
            (
                "blank image alt",
                lambda text: re.sub(r'(?m)^  alt: .+$', '  alt: ""', text, count=1),
                "local cover images must define nonblank alt text",
            ),
            (
                "remote image",
                lambda text: re.sub(
                    r'(?m)^  image: .+$',
                    '  image: "https://example.com/cover.png"',
                    text,
                    count=1,
                ),
                "cover image must be a local relative page resource",
            ),
            (
                "image path whitespace",
                lambda text: text.replace(
                    '  image: "govintel-ui.png"',
                    '  image: " govintel-ui.png "',
                    1,
                ),
                "cover image path must not have surrounding whitespace",
            ),
            (
                "nonrelative image",
                lambda text: text.replace("  relative: true", "  relative: false", 1),
                "cover image must be a local relative page resource",
            ),
            (
                "missing resource",
                lambda text: re.sub(
                    r'(?m)^  image: .+$', '  image: "missing.png"', text, count=1
                ),
                "cover image missing.png does not match a page resource",
            ),
            (
                "hidden type",
                lambda text: text.replace(
                    "  hiddenInList: false", '  hiddenInList: "false"', 1
                ),
                "cover hiddenInList must be boolean when provided",
            ),
        )
        for label, transform, expected in cases:
            with self.subTest(case=label):
                self.assert_project_fixture_error(
                    project_path, transform, expected, consumer="list"
                )

        result = self.build_with_project_fixture(
            project_path,
            lambda text: text.replace(
                '  image: "govintel-ui.png"', '  image: "cover.txt"'
            ),
            bundle_files={
                "cover.txt": "This page resource is deliberately not an image.\n"
            },
        )
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(project_path.removeprefix("content/"), output)
        self.assertIn("cover image cover.txt must be an image resource", output)
        for generic_error in (
            "can't evaluate field",
            "error calling Width",
            "nil pointer evaluating",
            "range can't iterate over",
            "this method is only available for image resources",
            "this method is only available for raster images",
            "wrong type for value",
        ):
            self.assertNotIn(generic_error, output)

        result = self.build_with_project_fixture(
            project_path,
            lambda text: text.replace(
                '  image: "govintel-ui.png"', '  image: "cover.svg"'
            ),
            bundle_files={
                "cover.svg": (
                    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="9" '
                    'viewBox="0 0 16 9"><rect width="16" height="9"/></svg>\n'
                )
            },
        )
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(project_path.removeprefix("content/"), output)
        self.assertIn(
            "cover image cover.svg must use a supported raster image format", output
        )
        for generic_error in (
            "can't evaluate field",
            "error calling Width",
            "nil pointer evaluating",
            "range can't iterate over",
            "this method is only available for image resources",
            "this method is only available for raster images",
            "wrong type for value",
        ):
            self.assertNotIn(generic_error, output)

        validator = (ROOT / "layouts/partials/projects/validate.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("ResourceType", validator)
        self.assertIn("cover image %s must be an image resource", validator)
        self.assertIn(".png", validator)
        self.assertIn(".jpg", validator)
        self.assertIn(".jpeg", validator)
        self.assertIn(".webp", validator)
        self.assertIn("cover image %s must use a supported raster image format", validator)

        list_layout = (ROOT / "layouts/projects/list.html").read_text(encoding="utf-8")
        single_layout = (ROOT / "layouts/projects/single.html").read_text(
            encoding="utf-8"
        )
        self.assertLess(
            list_layout.index("if $projectsValid"), list_layout.index(".Width")
        )
        self.assertLess(
            single_layout.index("if $projectValid"), single_layout.index(".Width")
        )

    def test_project_list_allows_future_projects_and_optional_repositories(self) -> None:
        future_project = """---
title: "Future Applied AI Project"
date: 2026-07-01
draft: false
description: "A future evidence-backed applied AI case study."
tags: ["applied-ai"]
portfolio_group: "featured-ai"
portfolio_status: "Prototype"
portfolio_category: "Applied AI"
portfolio_role: "Builder"
portfolio_year: 2026
repository_url: "https://example.com/future-applied-ai-project"
home_featured: false
cover:
  image: ""
  alt: ""
  relative: true
weight: 5
showToc: true
---

## Overview

Future project fixture.
"""
        result = self.build_with_project_fixture(
            "content/projects/asd-prediction/index.md",
            lambda text: text + "\n",
            consumer="list",
            site_files={
                "content/projects/future-applied-ai/index.md": future_project
            },
        )
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("project group cardinality", output)

        optional_repository_cases = (
            (
                "missing",
                "content/projects/asd-prediction/index.md",
                lambda text: re.sub(
                    r'(?m)^repository_url:.*\n', "", text, count=1
                ),
            ),
            (
                "blank",
                "content/projects/llm-engineering-from-scratch/index.md",
                lambda text: re.sub(
                    r'(?m)^repository_url: .+$', 'repository_url: ""', text, count=1
                ),
            ),
        )
        for label, project_path, transform in optional_repository_cases:
            with self.subTest(repository=label):
                result = self.build_with_project_fixture(
                    project_path, transform, consumer="list"
                )
                output = result.stdout + result.stderr
                self.assertEqual(result.returncode, 0, output)

        validator = (ROOT / "layouts/partials/projects/validate.html").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("$page.RelPermalink", validator)
        self.assertNotIn("ASD research project", validator)
        homepage_validator = (
            ROOT / "layouts/partials/home/selected-work.html"
        ).read_text(encoding="utf-8")
        self.assertIn('"repository_url"', homepage_validator)
        self.assertIn(
            "featured project repository_url must be an absolute HTTPS URL",
            homepage_validator,
        )

    def test_optional_cover_fit_is_validated(self) -> None:
        self.assert_project_fixture_error(
            "content/projects/govtintel/index.md",
            lambda text: text.replace(
                "  hiddenInList: false",
                "  hiddenInList: false\n  fit: stretch",
            ),
            "cover fit must be contain or cover when provided",
            consumer="single",
        )
