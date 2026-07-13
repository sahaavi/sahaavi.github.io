from html import unescape

from tests.site_harness import HugoSiteTestCase, ROOT


class HomepageContractTests(HugoSiteTestCase):
    def test_header_prioritizes_experience_and_work(self) -> None:
        html = self.page_html("/")
        for label in ("Experience", "Expertise", "Selected Work", "Writing", "Contact"):
            self.assertIn(f">{label}<", html)
        for forbidden in (">Resume<", ">Books<", ">Search<"):
            self.assertNotIn(forbidden, html)
        self.assertIn('href="#main-content"', html)
        self.assertIn('<main id="main-content"', html)
        self.assertNotIn('aria-current="page"', html)

        posts_html = self.page_html("/posts/")
        self.assertEqual(posts_html.count('aria-current="page"'), 1)
        writing_anchor = posts_html.split(">Writing</a>", 1)[0].rsplit("<a", 1)[1]
        self.assertIn('aria-current="page"', writing_anchor)

        css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        self.assertIn("@media (max-width: 1040px)", css)
        self.assertIn("@media (max-width: 820px)", css)
        brand_css = css.split(".portfolio-brand {", 1)[1].split("}", 1)[0]
        self.assertIn("white-space: nowrap", brand_css)
        for selector in (
            "#menu.portfolio-menu",
            "#menu.portfolio-menu li + li",
            "#menu.portfolio-menu a",
            "button#theme-toggle.portfolio-theme-toggle",
        ):
            self.assertIn(selector, css)
        primary_button_css = css.split(".portfolio-button-primary {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("color: var(--portfolio-on-primary)", primary_button_css)

        footer = (ROOT / "layouts/partials/footer.html").read_text(encoding="utf-8")
        for behavior in (
            "target.focus({ preventScroll: true })",
            "syncThemeState",
            'themeToggle.setAttribute("aria-pressed"',
        ):
            self.assertIn(behavior, footer)

    def test_hero_leads_with_ai_ml_and_not_a_project(self) -> None:
        html = self.page_html("/")
        hero = unescape(
            html.split('id="portfolio-hero"', 1)[1].split("</section>", 1)[0]
        )
        self.assertIn("Applied AI & ML Engineer", hero)
        self.assertIn("<h1", hero)
        self.assertIn(
            "Building AI products and ML systems with measurable impact.", hero
        )
        self.assertIn(
            "My experience spans source-grounded LLM workflows, predictive models, "
            "evaluation systems, data and feature pipelines, APIs, and cloud delivery, "
            "with measured improvements in quality, efficiency, review effort, and "
            "decision support.",
            hero,
        )
        self.assertIn("LLM systems, RAG & evaluation", hero)
        self.assertIn("Predictive ML & human review", hero)
        self.assertNotIn("4+ years", hero)
        self.assertNotIn("Python & SQL", hero)
        self.assertNotIn("Maintenance-Eye", hero)

        hero_source = (ROOT / "layouts/partials/home/hero.html").read_text(
            encoding="utf-8"
        )
        for validation in (
            "data/profile.yaml must define role",
            "data/profile.yaml must define location",
            "data/profile.yaml must define work_authorized_label",
            "profile.hero must define statement",
            "profile.hero must define supporting",
            "profile.hero.signals items must be nonblank",
            "profile.actions must contain exactly three items",
            "profile.actions items must define label and url",
            "profile.actions must contain exactly one primary action",
            "hero role must define hero_order, short_period, title, and employer",
            "hero education signal must define hero_order, short_period, degree, and institution",
            "homepage career signal must define order, period, title, and organization",
        ):
            self.assertIn(validation, hero_source)

    def test_hero_contains_canonical_career_signal(self) -> None:
        html = self.page_html("/")
        hero = unescape(
            html.split('id="portfolio-hero"', 1)[1].split("</section>", 1)[0]
        )
        for text in (
            "Data & Applied AI Analyst",
            "Data Scientist, Applied AI",
            "Master of Data Science",
            "Co-Founder / Data Scientist",
        ):
            self.assertIn(text, hero)
