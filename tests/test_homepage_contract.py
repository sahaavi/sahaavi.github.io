import shutil
import subprocess
import tempfile
from html import unescape
from pathlib import Path
from typing import Callable

from tests.site_harness import HugoSiteTestCase, ROOT


class HomepageContractTests(HugoSiteTestCase):
    def build_with_project_fixture(
        self,
        project_path: str,
        transform: Callable[[str], str],
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
            self.assertNotEqual(
                transformed,
                original,
                f"Fixture did not modify {project_path}",
            )
            project.write_text(transformed, encoding="utf-8")
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

    def build_with_expertise_fixture(
        self, expertise_yaml: str | None
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="portfolio-expertise-invalid-") as temp:
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
            expertise_path = source / "data/expertise.yaml"
            if expertise_yaml is None:
                expertise_path.unlink()
            else:
                expertise_path.write_text(expertise_yaml, encoding="utf-8")
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

    def test_professional_experience_precedes_selected_work(self) -> None:
        html = self.page_html("/")
        self.assertIn('id="experience"', html)
        hero_index = html.index('id="portfolio-hero"')
        experience_index = html.index('id="experience"')
        self.assertLess(hero_index, experience_index)
        self.assertLess(experience_index, html.index("</main>"))
        if 'id="work"' in html:
            self.assertLess(experience_index, html.index('id="work"'))

        home_css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        self.assertIn("@media (max-width: 480px)", home_css)
        evidence_mobile_css = home_css.split("@media (max-width: 480px)", 1)[1]
        self.assertIn(
            ".portfolio-evidence-list li { grid-template-columns: 1fr; gap: 6px; }",
            evidence_mobile_css,
        )

        base_css = (ROOT / "assets/css/extended/portfolio-base.css").read_text(
            encoding="utf-8"
        )
        self.assertIn("@media (max-width: 480px)", base_css)
        top_link_mobile_css = base_css.split("@media (max-width: 480px)", 1)[1]
        self.assertIn(".top-link { display: none; }", top_link_mobile_css)

    def test_experience_uses_canonical_titles_and_scoped_metrics(self) -> None:
        html = unescape(self.page_html("/"))
        experience = html.split('id="experience"', 1)[1].split("</section>", 1)[0]
        for text in (
            "Data & Applied AI Analyst",
            "Data Scientist, Applied AI",
            "Capstone Data Scientist",
            "Co-Founder / Data Scientist",
            "21%",
            "17%",
            "26%",
        ):
            self.assertIn(text, experience)
        self.assertNotIn(
            "Data Scientist, Financial Analytics & AI Workflows", experience
        )
        self.assertEqual(experience.count('class="portfolio-metric-row"'), 1)

        current = experience.split(
            'class="portfolio-experience-primary"', 1
        )[1].split("</article>", 1)[0]
        previous_cards = [
            card.split("</article>", 1)[0]
            for card in experience.split('class="portfolio-experience-card"')[1:]
        ]
        self.assertEqual(len(previous_cards), 3)
        brainstation_cards = [
            card for card in previous_cards if "Brain Station 23" in card
        ]
        self.assertEqual(len(brainstation_cards), 1)
        brainstation_card = brainstation_cards[0]
        self.assertIn('class="portfolio-metric-row"', brainstation_card)
        for metric in ("21%", "17%", "26%"):
            self.assertIn(metric, brainstation_card)
        self.assertNotIn('class="portfolio-metric-row"', current)
        for card in previous_cards:
            if card != brainstation_card:
                self.assertNotIn('class="portfolio-metric-row"', card)

        home_css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        metric_label_css = home_css.split(".portfolio-metric-row dd {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn('font: 400 10px "IBM Plex Mono", monospace', metric_label_css)

    def test_current_role_foregrounds_ai_evaluation_and_predictive_ml(self) -> None:
        html = unescape(self.page_html("/"))
        current = html.split('class="portfolio-experience-primary"', 1)[1].split(
            "</article>", 1
        )[0]
        for text in (
            "150-case evaluation harness",
            "RAGAS",
            "predictive ML",
            "planning accuracy by 21%",
            "unsupported AI-generated summary claims by 60%",
        ):
            self.assertIn(text, current)

        experience_source = (
            ROOT / "layouts/partials/home/experience.html"
        ).read_text(encoding="utf-8")
        for validation in (
            "data/experience.yaml must define exactly four roles",
            "experience role current must be boolean",
            "experience roles must define id, employer, title, period, short_period, location, and homepage_summary",
            "data/experience.yaml must define exactly one current role",
            "data/experience.yaml must define exactly three previous roles",
            "current role evidence must contain exactly three items",
            "current role evidence items must define label and text",
            "experience metrics must define value and label",
        ):
            self.assertIn(validation, experience_source)
        self.assertIn("$rolesValid := true", experience_source)
        validation_index = experience_source.index(
            'ne (printf "%T" .current) "bool"'
        )
        guard_index = experience_source.index("if $rolesValid")
        selection_index = experience_source.index('$currentRoles := where $roles')
        self.assertLess(validation_index, guard_index)
        self.assertLess(guard_index, selection_index)

    def test_expertise_covers_ai_ml_software_and_delivery(self) -> None:
        html = self.page_html("/")
        expertise = html.split('id="expertise"', 1)[1].split("</section>", 1)[0]
        semantic_expertise = unescape(expertise)
        for text in (
            "Applied AI systems",
            "Machine learning",
            "Software & data",
            "Delivery & trust",
            "Data foundation",
            "Model or retrieval",
            "Evaluation",
            "Software integration",
            "Delivery loop",
        ):
            self.assertIn(text, semantic_expertise)

        for text in (
            "02 · Engineering range",
            "More than models. The surrounding system matters.",
            "The profile spans AI behavior, machine learning, software interfaces, "
            "data foundations, and delivery quality.",
        ):
            self.assertIn(text, semantic_expertise)
        self.assertIn("<h2", expertise)
        self.assertEqual(expertise.count("<article>"), 4)
        self.assertIn('<ol class="portfolio-lifecycle">', expertise)
        lifecycle = expertise.split('<ol class="portfolio-lifecycle">', 1)[1].split(
            "</ol>", 1
        )[0]
        self.assertEqual(lifecycle.count("<li>"), 5)

        hero_index = html.index('id="portfolio-hero"')
        experience_index = html.index('id="experience"')
        expertise_index = html.index('id="expertise"')
        self.assertLess(hero_index, experience_index)
        self.assertLess(experience_index, expertise_index)
        self.assertLess(expertise_index, html.index("</main>"))
        if 'id="work"' in html:
            self.assertLess(expertise_index, html.index('id="work"'))

        expertise_source = (
            ROOT / "layouts/partials/home/expertise.html"
        ).read_text(encoding="utf-8")
        for validation in (
            "data/expertise.yaml is required",
            "data/expertise.yaml must be a map",
            "data/expertise.yaml must define groups",
            "data/expertise.yaml must define lifecycle",
            "expertise.groups must be a list",
            "expertise.lifecycle must be a list",
            "expertise group items must be maps",
            "expertise lifecycle items must be maps",
            "expertise.groups must contain four groups",
            "expertise.lifecycle must contain five stages",
            "expertise groups must define code, title, and summary",
            "expertise groups must define at least one source_refs entry",
            "expertise source_refs entries must be nonblank strings",
            "expertise lifecycle stages must define title and detail",
        ):
            self.assertIn(validation, expertise_source)

        expertise_data = (ROOT / "data/expertise.yaml").read_text(encoding="utf-8")
        source_refs = (
            "claim:stan-bcrtc-ragas-semantic-eval-20260709",
            "project:content/projects/govtintel/index.md",
            "project:content/projects/vision-maintenance-agent/index.md",
            "claim:aviva-bcrtc-p15-recovery-duration-001",
            "claim:seed-p11-event-feature-foundation",
            "experience:data/experience.yaml#statscan",
            "claim:stage-bs23-ai-002",
        )
        self.assertEqual(expertise_data.count("source_refs:"), 4)
        for source_ref in source_refs:
            self.assertIn(source_ref, expertise_data)
            self.assertNotIn(source_ref, semantic_expertise)

        home_css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            ".portfolio-capability-rail { display: grid; grid-template-columns: repeat(4, 1fr);",
            home_css,
        )
        tablet_css = home_css.split("@media (max-width: 920px)", 1)[1]
        self.assertIn(
            ".portfolio-capability-rail { grid-template-columns: 1fr 1fr; }",
            tablet_css,
        )
        self.assertIn(
            ".portfolio-lifecycle { grid-template-columns: 1fr;", tablet_css
        )
        mobile_css = home_css.split("@media (max-width: 640px)", 1)[1]
        self.assertIn(
            ".portfolio-capability-rail { grid-template-columns: 1fr; }",
            mobile_css,
        )
        section_css = home_css.split(".portfolio-section {", 1)[1].split("}", 1)[0]
        self.assertIn("scroll-margin-top: 84px", section_css)

    def test_selected_work_contains_exactly_two_equal_public_systems(self) -> None:
        html = self.page_html("/")
        work = html.split('id="work"', 1)[1].split("</section>", 1)[0]
        self.assertIn('<body class="list portfolio-homepage" id="top">', html)
        posts_body = self.page_html("/posts/").split("<body", 1)[1].split(">", 1)[0]
        self.assertNotIn("portfolio-homepage", posts_body)
        self.assertLess(html.index('id="experience"'), html.index('id="work"'))
        self.assertLess(html.index('id="expertise"'), html.index('id="work"'))
        self.assertLess(html.index('id="work"'), html.index("</main>"))
        self.assertEqual(work.count('class="portfolio-work-row"'), 2)
        self.assertEqual(work.count(">Maintenance-Eye<"), 1)
        self.assertEqual(work.count(">GovIntel<"), 1)
        self.assertLess(work.index(">Maintenance-Eye<"), work.index(">GovIntel<"))
        self.assertEqual(work.count('class="portfolio-system-map"'), 2)
        self.assertEqual(work.count('role="img"'), 2)
        self.assertEqual(work.count("system components:"), 2)
        self.assertNotIn("system flow:", work)
        self.assertEqual(work.count(">Repository</a>"), 2)
        self.assertEqual(work.count(">Case study</a>"), 2)
        self.assertEqual(work.count('target="_blank"'), 2)
        self.assertEqual(work.count('rel="noopener noreferrer"'), 2)
        for text in (
            "03 · Selected work",
            "Public systems for inspecting the engineering.",
            "Two focused case studies provide technical proof without taking over "
            "the professional narrative.",
            "Public demo",
            "Public repository",
            "Applied AI",
            "RAG system",
            "Builder",
        ):
            self.assertIn(text, unescape(work))

        maintenance_row, govintel_row = [
            row.split("</article>", 1)[0]
            for row in work.split('class="portfolio-work-row"')[1:]
        ]
        self.assertIn(
            'href="https://github.com/sahaavi/Maintenance-Eye"', maintenance_row
        )
        self.assertIn('aria-labelledby="work-project-1-title"', maintenance_row)
        self.assertIn('<h3 id="work-project-1-title">Maintenance-Eye</h3>', maintenance_row)
        self.assertIn('href="/projects/maintenance-eye/"', maintenance_row)
        self.assertIn(
            'aria-label="Maintenance-Eye repository, opens in a new tab"',
            maintenance_row,
        )
        self.assertIn('aria-label="Maintenance-Eye case study"', maintenance_row)
        self.assertIn(
            'aria-label="Maintenance-Eye system components: Camera + voice, Gemini Live, User response, FastAPI, 9 guarded tools, Approval gate"',
            maintenance_row,
        )
        self.assertIn('href="https://github.com/sahaavi/GovtIntel"', govintel_row)
        self.assertIn('aria-labelledby="work-project-2-title"', govintel_row)
        self.assertIn('<h3 id="work-project-2-title">GovIntel</h3>', govintel_row)
        self.assertIn('href="/projects/govtintel/"', govintel_row)
        self.assertIn(
            'aria-label="GovIntel repository, opens in a new tab"', govintel_row
        )
        self.assertIn('aria-label="GovIntel case study"', govintel_row)
        self.assertIn(
            'aria-label="GovIntel system components: Award data, PostgreSQL, Vector index, Hybrid retrieval, Reranking, Citation checks"',
            govintel_row,
        )
        self.assertIn("fail-closed citation validation", govintel_row)
        self.assertNotIn("90%", govintel_row)
        self.assertNotIn("<h3></h3>", work)
        self.assertNotIn('aria-label=""', work)

        selected_work_source = (
            ROOT / "layouts/partials/home/selected-work.html"
        ).read_text(encoding="utf-8")
        for validation in (
            "Homepage requires exactly two home_featured projects",
            "Featured project title must be a nonblank string",
            "Featured projects must define home_order, portfolio_group, portfolio_status, portfolio_category, portfolio_role, portfolio_year, repository_url, case_study_url, and home_summary",
            "featured project home_order must be an integer",
            "featured project portfolio_year must be an integer",
            "featured project portfolio_year must be a four-digit year",
            "featured project repository_url must be an absolute HTTPS URL",
            "Featured project case_study_url must be an internal path matching its permalink",
            "Featured project portfolio_group must equal featured-ai",
            "Featured project home_order values must be unique",
            "Featured project home_order values must be exactly 1 and 2",
            "Featured project system_map must be a six-item list",
            "Featured project system_map items must be maps",
            "Featured project system_map items must define a nonblank string label",
            "Featured project system_map accent must be boolean",
        ):
            self.assertIn(validation, selected_work_source)

        home_css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        system_node_css = home_css.split(".portfolio-system-map span {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn('font: 400 10px "IBM Plex Mono", monospace', system_node_css)
        self.assertIn("padding: 4px", system_node_css)
        self.assertIn("overflow-wrap: break-word", system_node_css)
        self.assertIn("word-break: normal", system_node_css)
        self.assertNotIn("overflow-wrap: anywhere", system_node_css)
        work_link_css = home_css.split(".portfolio-work-links a {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("min-height: 44px", work_link_css)
        tablet_css = home_css.split("@media (max-width: 920px)", 1)[1]
        self.assertIn(
            ".portfolio-work-row { grid-template-columns: 130px minmax(0, 1fr); }",
            tablet_css,
        )
        self.assertIn(".portfolio-system-map { grid-column: 2; }", tablet_css)
        mobile_css = home_css.split("@media (max-width: 640px)", 1)[1]
        self.assertIn(
            ".portfolio-work-row { grid-template-columns: minmax(0, 1fr); gap: 18px; }",
            mobile_css,
        )
        self.assertIn(".portfolio-system-map { grid-column: auto; }", mobile_css)

        baseof_source = (ROOT / "layouts/_default/baseof.html").read_text(
            encoding="utf-8"
        )
        self.assertIn(".IsHome", baseof_source)
        self.assertIn('append "portfolio-homepage"', baseof_source)

        base_css = (ROOT / "assets/css/extended/portfolio-base.css").read_text(
            encoding="utf-8"
        )
        top_link_css = base_css.split(".top-link {", 1)[1].split("}", 1)[0]
        self.assertIn("width: 44px", top_link_css)
        self.assertIn("height: 44px", top_link_css)
        homepage_top_link_css = base_css.split(
            "@media (max-width: 1360px)", 1
        )[1]
        self.assertIn(
            "body.portfolio-homepage .top-link { display: none; }",
            homepage_top_link_css,
        )

    def test_maintenance_eye_copy_matches_public_code(self) -> None:
        html = self.page_html("/")
        work = html.split('id="work"', 1)[1].split("</section>", 1)[0]
        self.assertIn("nine guarded tool workflows", work)
        self.assertIn("human approval", work)
        self.assertNotIn("multi-agent", work.lower())
        self.assertNotIn("66 assets", work)
        self.assertNotIn("150 work orders", work)

    def test_malformed_selected_work_data_fails_with_deliberate_errors(self) -> None:
        maintenance = "content/projects/vision-maintenance-agent/index.md"
        govintel = "content/projects/govtintel/index.md"

        def replace_once(old: str, new: str) -> Callable[[str], str]:
            return lambda content: content.replace(old, new, 1)

        cases = (
            (
                "featured count",
                maintenance,
                replace_once("home_featured: true\n", "home_featured: false\n"),
                "Homepage requires exactly two home_featured projects",
            ),
            (
                "missing title",
                govintel,
                replace_once('title: "GovIntel"\n', ""),
                "Featured project title must be a nonblank string",
            ),
            (
                "blank title",
                govintel,
                replace_once('title: "GovIntel"\n', 'title: "   "\n'),
                "Featured project title must be a nonblank string",
            ),
            (
                "missing required metadata",
                maintenance,
                replace_once('portfolio_status: "Public demo"\n', ""),
                "Featured projects must define home_order, portfolio_group, portfolio_status, portfolio_category, portfolio_role, portfolio_year, repository_url, case_study_url, and home_summary",
            ),
            (
                "duplicate order",
                govintel,
                replace_once("home_order: 2\n", "home_order: 1\n"),
                "Featured project home_order values must be unique",
            ),
            (
                "wrong order",
                govintel,
                replace_once("home_order: 2\n", "home_order: 3\n"),
                "Featured project home_order values must be exactly 1 and 2",
            ),
            (
                "string home order",
                govintel,
                replace_once("home_order: 2\n", 'home_order: "2"\n'),
                "featured project home_order must be an integer",
            ),
            (
                "boolean home order",
                govintel,
                replace_once("home_order: 2\n", "home_order: true\n"),
                "featured project home_order must be an integer",
            ),
            (
                "float home order",
                govintel,
                replace_once("home_order: 2\n", "home_order: 2.0\n"),
                "featured project home_order must be an integer",
            ),
            (
                "string portfolio year",
                govintel,
                replace_once("portfolio_year: 2026\n", 'portfolio_year: "2026"\n'),
                "featured project portfolio_year must be an integer",
            ),
            (
                "boolean portfolio year",
                govintel,
                replace_once("portfolio_year: 2026\n", "portfolio_year: true\n"),
                "featured project portfolio_year must be an integer",
            ),
            (
                "out-of-range portfolio year",
                govintel,
                replace_once("portfolio_year: 2026\n", "portfolio_year: 1999\n"),
                "featured project portfolio_year must be a four-digit year",
            ),
            (
                "null system map",
                maintenance,
                replace_once("system_map:\n", "system_map: null\nunused_system_map:\n"),
                "Featured project system_map must be a six-item list",
            ),
            (
                "scalar system map",
                maintenance,
                replace_once("system_map:\n", "system_map: invalid\nunused_system_map:\n"),
                "Featured project system_map must be a six-item list",
            ),
            (
                "non-map system node",
                govintel,
                replace_once('  - label: "Award data"\n', "  - invalid\n"),
                "Featured project system_map items must be maps",
            ),
            (
                "blank system node label",
                govintel,
                replace_once('  - label: "Award data"\n', '  - label: "   "\n'),
                "Featured project system_map items must define a nonblank string label",
            ),
            (
                "non-boolean accent",
                govintel,
                replace_once("    accent: true\n", '    accent: "true"\n'),
                "Featured project system_map accent must be boolean",
            ),
            (
                "non-https repository",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "http://github.com/sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "hostless https repository",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "https://"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "relative repository",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "/sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "whitespace repository host",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "https://   /sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "wrong-type repository",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    "repository_url: true\n",
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "double-dot repository host",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "https://github..com/sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "leading-hyphen repository host",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "https://-github.com/sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "trailing-hyphen repository host",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "https://github-.com/sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "repository URL with port",
                govintel,
                replace_once(
                    'repository_url: "https://github.com/sahaavi/GovtIntel"\n',
                    'repository_url: "https://github.com:443/sahaavi/GovtIntel"\n',
                ),
                "featured project repository_url must be an absolute HTTPS URL",
            ),
            (
                "case-study permalink mismatch",
                govintel,
                replace_once(
                    'case_study_url: "/projects/govtintel/"\n',
                    'case_study_url: "/projects/not-govtintel/"\n',
                ),
                "Featured project case_study_url must be an internal path matching its permalink",
            ),
            (
                "wrong portfolio group",
                govintel,
                replace_once(
                    'portfolio_group: "featured-ai"\n',
                    'portfolio_group: "other"\n',
                ),
                "Featured project portfolio_group must equal featured-ai",
            ),
        )
        generic_errors = (
            "reflect:",
            "range can't iterate",
            "can't evaluate field",
            "error calling isset",
            "error calling len",
            "error calling parse",
        )
        global_errors = (
            "Homepage requires exactly two home_featured projects",
            "Featured project home_order values must be unique",
            "Featured project home_order values must be exactly 1 and 2",
        )

        for name, project_path, transform, expected_error in cases:
            with self.subTest(name=name):
                result = self.build_with_project_fixture(project_path, transform)
                output = (result.stdout + result.stderr).lower()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error.lower(), output)
                if expected_error not in global_errors:
                    self.assertIn(
                        project_path.removeprefix("content/").lower(), output
                    )
                for generic_error in generic_errors:
                    self.assertNotIn(generic_error, output)

    def test_missing_expertise_data_fails_with_deliberate_error(self) -> None:
        result = self.build_with_expertise_fixture(None)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("data/expertise.yaml is required", output)
        self.assertNotIn("reflect:", output)

    def test_missing_expertise_groups_fails_with_deliberate_error(self) -> None:
        valid_data = (ROOT / "data/expertise.yaml").read_text(encoding="utf-8")
        lifecycle = "lifecycle:" + valid_data.split("lifecycle:", 1)[1]
        result = self.build_with_expertise_fixture(lifecycle)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("data/expertise.yaml must define groups", output)
        self.assertNotIn("reflect:", output)

    def test_missing_expertise_lifecycle_fails_with_deliberate_error(self) -> None:
        valid_data = (ROOT / "data/expertise.yaml").read_text(encoding="utf-8")
        groups = valid_data.split("lifecycle:", 1)[0]
        result = self.build_with_expertise_fixture(groups)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("data/expertise.yaml must define lifecycle", output)
        self.assertNotIn("reflect:", output)

    def test_malformed_expertise_shapes_fail_with_deliberate_errors(self) -> None:
        valid_group = (
            '  - code: "placeholder"\n'
            '    title: "Placeholder"\n'
            '    summary: "Placeholder"\n'
            '    source_refs:\n'
            '      - "placeholder:source"\n'
        )
        valid_stage = (
            '  - title: "Placeholder"\n'
            '    detail: "Placeholder"\n'
        )
        valid_groups = "groups:\n" + (valid_group * 4)
        valid_lifecycle = "lifecycle:\n" + (valid_stage * 5)
        cases = (
            (
                "list-valued root",
                "- groups\n- lifecycle\n",
                "data/expertise.yaml must be a map",
            ),
            (
                "groups null",
                "groups:\n" + valid_lifecycle,
                "expertise.groups must be a list",
            ),
            (
                "groups scalar",
                "groups: invalid\n" + valid_lifecycle,
                "expertise.groups must be a list",
            ),
            (
                "lifecycle null",
                valid_groups + "lifecycle:\n",
                "expertise.lifecycle must be a list",
            ),
            (
                "lifecycle scalar",
                valid_groups + "lifecycle: invalid\n",
                "expertise.lifecycle must be a list",
            ),
            (
                "non-map group item",
                "groups:\n  - invalid\n"
                + (valid_group * 3)
                + valid_lifecycle,
                "expertise group items must be maps",
            ),
            (
                "non-map lifecycle item",
                valid_groups
                + "lifecycle:\n  - invalid\n"
                + (valid_stage * 4),
                "expertise lifecycle items must be maps",
            ),
        )
        generic_errors = (
            "reflect:",
            "range can't iterate",
            "can't evaluate field",
            "error calling isset",
            "error calling len",
        )

        for name, fixture, expected_error in cases:
            with self.subTest(name=name):
                result = self.build_with_expertise_fixture(fixture)
                output = (result.stdout + result.stderr).lower()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error.lower(), output)
                for generic_error in generic_errors:
                    self.assertNotIn(generic_error, output)
