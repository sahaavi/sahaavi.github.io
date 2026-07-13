from pathlib import Path

from tests.site_harness import HugoSiteTestCase, ROOT


class DesignAssetTests(HugoSiteTestCase):
    def test_required_fonts_are_local(self) -> None:
        expected = (
            "static/fonts/instrument-sans-latin-wght-normal.woff2",
            "static/fonts/ibm-plex-mono-latin-400-normal.woff2",
            "static/fonts/ibm-plex-mono-latin-500-normal.woff2",
        )
        for relative_path in expected:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_homepage_does_not_load_google_fonts(self) -> None:
        html = self.page_html("/")
        self.assertNotIn("fonts.googleapis.com", html)
        self.assertNotIn("fonts.gstatic.com", html)
        self.assertIn("/fonts/instrument-sans-latin-wght-normal.woff2", html)
        self.assertIn("/fonts/ibm-plex-mono-latin-400-normal.woff2", html)

    def test_design_tokens_cover_light_and_dark_modes(self) -> None:
        tokens_css = (ROOT / "assets/css/extended/portfolio-tokens.css").read_text(
            encoding="utf-8"
        )
        base_css = (ROOT / "assets/css/extended/portfolio-base.css").read_text(
            encoding="utf-8"
        )
        root_css = tokens_css.split(":root {", 1)[1].split("}", 1)[0]
        dark_css = tokens_css.split(':root[data-theme="dark"]', 1)[1].split("}", 1)[0]

        self.assertIn("--portfolio-paper: #f5f7f4", tokens_css.lower())
        self.assertIn(':root[data-theme="dark"]', tokens_css)
        self.assertIn("--portfolio-paper: #08111c", tokens_css.lower())

        compatibility_aliases = (
            "--accent: var(--portfolio-cyan)",
            "--proof: var(--portfolio-green)",
        )
        for alias in compatibility_aliases:
            with self.subTest(alias=alias):
                self.assertIn(alias, root_css)

        paper_mod_mappings = (
            "--theme: var(--portfolio-paper)",
            "--entry: var(--portfolio-surface)",
            "--primary: var(--portfolio-ink)",
            "--secondary: var(--portfolio-ink-soft)",
            "--tertiary: var(--portfolio-surface-soft)",
            "--content: var(--portfolio-ink)",
            "--border: var(--portfolio-line)",
            "--main-width: var(--portfolio-max)",
        )
        for mapping in paper_mod_mappings:
            with self.subTest(mapping=mapping):
                self.assertIn(mapping, dark_css)

        system_theme_support = (
            "@media (prefers-color-scheme: dark)",
            ':root[data-theme="auto"]',
        )
        for selector in system_theme_support:
            with self.subTest(selector=selector):
                self.assertIn(selector, tokens_css)

        focus_and_background_selectors = (
            "body.list",
            "#theme-toggle:focus-visible",
            ".top-link:focus-visible",
            ".toc summary:focus-visible",
            "#searchResults a:focus-visible",
        )
        for selector in focus_and_background_selectors:
            with self.subTest(selector=selector):
                self.assertIn(selector, base_css)
