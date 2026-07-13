import re
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

    def build_with_profile_fixture(
        self,
        transform: Callable[[str], str],
        *,
        footer_only: bool = False,
        writing_only: bool = False,
        capture_home: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], str | None]:
        with tempfile.TemporaryDirectory(prefix="portfolio-profile-invalid-") as temp:
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
            profile_path = source / "data/profile.yaml"
            original = profile_path.read_text(encoding="utf-8")
            transformed = transform(original)
            self.assertNotEqual(transformed, original, "Fixture did not modify profile")
            profile_path.write_text(transformed, encoding="utf-8")
            if footer_only:
                (source / "layouts/index.html").write_text(
                    '{{ define "main" }}<p>Footer validation fixture</p>{{ end }}\n',
                    encoding="utf-8",
                )
                (source / "content/_index.md").write_text(
                    "---\nhideFooter: true\n---\n",
                    encoding="utf-8",
                )
            elif writing_only:
                (source / "layouts/index.html").write_text(
                    '{{ define "main" }}{{ partial "home/writing-education.html" . }}{{ end }}\n',
                    encoding="utf-8",
                )
            result = subprocess.run(
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
            rendered_home = None
            if capture_home and result.returncode == 0:
                rendered_home = (source / "public/index.html").read_text(
                    encoding="utf-8"
                )
            return result, rendered_home

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
        self.assertIn("@media (min-width: 641px) and (max-width: 899px)", css)
        self.assertIn("@media (max-width: 640px)", css)
        self.assertNotIn("@media (max-width: 820px)", css)
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

    def test_header_compacts_before_intrinsic_width_overflows(self) -> None:
        css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        compact_header = re.search(
            r"@media \(max-width: (?P<width>\d+)px\) \{\s*"
            r"\.portfolio-nav \{ gap: 8px; \}\s*"
            r"\.portfolio-monogram \{ display: none; \}\s*\}",
            css,
        )
        self.assertIsNotNone(compact_header)

        # Chromium renders the self-hosted font/header footprint without overflow
        # from 254px onward; the compact layout must cover the 253px boundary.
        last_overflowing_css_width = 253
        self.assertGreaterEqual(
            int(compact_header.group("width")), last_overflowing_css_width
        )

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
            "experience metrics must be a nonempty list",
            "experience metrics items must be maps",
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
        metrics_key_index = experience_source.index('isset $role "metrics"')
        metrics_slice_guard = experience_source.index(
            "reflect.IsSlice $metricsCandidate"
        )
        metrics_item_guard = experience_source.index("reflect.IsMap .")
        metrics_range = experience_source.index("range $metricsCandidate")
        self.assertLess(metrics_key_index, metrics_slice_guard)
        self.assertLess(metrics_slice_guard, metrics_range)
        self.assertLess(metrics_range, metrics_item_guard)
        self.assertLess(metrics_item_guard, guard_index)
        self.assertLess(metrics_item_guard, experience_source.index("{{ .value }}"))
        self.assertLess(metrics_item_guard, experience_source.index("{{ .label }}"))

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

    def test_homepage_closes_with_writing_education_and_contact(self) -> None:
        raw_html = self.page_html("/")
        html = unescape(raw_html)
        for text in (
            "Writing & research",
            "Data science and computer science foundations",
            "Master of Data Science",
            "BSc Computer Science & Engineering",
            "LLM Engineering From Scratch",
            "Tokenizer From Scratch",
            "Published ASD research",
            "Start a conversation",
        ):
            self.assertIn(text, html)

        section_ids = (
            'id="portfolio-hero"',
            'id="experience"',
            'id="expertise"',
            'id="work"',
            'id="writing"',
            'id="contact"',
        )
        section_positions = [raw_html.index(section_id) for section_id in section_ids]
        self.assertEqual(section_positions, sorted(section_positions))
        self.assertLess(section_positions[-1], raw_html.index("</main>"))
        self.assertLess(raw_html.index("</main>"), raw_html.index("<footer"))

        writing = raw_html.split('id="writing"', 1)[1].split("</section>", 1)[0]
        semantic_writing = unescape(writing)
        self.assertIn('aria-label="Writing, research, and education"', writing)
        self.assertEqual(writing.count("<article"), 2)
        evidence = writing.split('class="portfolio-evidence-links"', 1)[1].split(
            "</ul>", 1
        )[0]
        self.assertEqual(evidence.count("<li>"), 3)
        expected_links = {
            "/projects/llm-engineering-from-scratch/": "LLM Engineering From Scratch",
            "/posts/llm-engineering-from-scratch-tokenizer/": "Tokenizer From Scratch",
            "/projects/autism-spectrum-disorder-prediction/": "Published ASD research",
        }
        for route, label in expected_links.items():
            self.assertIn(f'href="{route}"', evidence)
            self.assertIn(label, semantic_writing)
            self.assertTrue(self.page_path(route).is_file(), route)
        self.assertIn("Learning lab and implementation series", semantic_writing)
        self.assertNotIn("%", semantic_writing)
        self.assertIn('href="/posts/"', writing)
        self.assertIn('href="/experience/"', writing)
        self.assertEqual(writing.count('class="portfolio-education-entry"'), 2)
        for canonical_entry in (
            "Master of Data Science</strong>, University of British Columbia",
            "BSc Computer Science & Engineering</strong>, "
            "American International University-Bangladesh · CGPA 3.91/4.00",
        ):
            self.assertIn(canonical_entry, semantic_writing)

        contact = raw_html.split('id="contact"', 1)[1].split("</section>", 1)[0]
        semantic_contact = unescape(contact)
        self.assertIn('aria-labelledby="contact-title"', contact)
        self.assertIn(
            "Building AI or ML systems that need engineering depth?",
            semantic_contact,
        )
        self.assertIn(
            'href="mailto:avisheksaha123@gmail.com"', contact
        )
        self.assertNotIn("<form", contact.lower())
        self.assertNotIn("chatbot", semantic_contact.lower())

    def test_homepage_has_no_resume_or_download_control(self) -> None:
        html = self.page_html("/")
        main = html.split("<main", 1)[1].split("</main>", 1)[0]
        footer = html.split("<footer", 1)[1].split("</footer>", 1)[0]
        public_closure = main + footer
        for forbidden in (
            ">Resume<",
            "downloadable resume",
            "download pdf",
            "resume",
            ".pdf",
            "application/pdf",
            "download=",
            "<form",
            "chatbot",
            "tel:",
            ">X<",
        ):
            self.assertNotIn(forbidden.lower(), public_closure.lower())

        for label in ("GitHub", "LinkedIn", "Email"):
            self.assertEqual(footer.count(f">{label}</a>"), 1)
        self.assertIn(
            'href="https://github.com/sahaavi" target="_blank" '
            'rel="noopener noreferrer me" '
            'aria-label="GitHub profile, opens in a new tab"',
            footer,
        )
        self.assertIn(
            'href="https://linkedin.com/in/sahaavi" target="_blank" '
            'rel="noopener noreferrer me" '
            'aria-label="LinkedIn profile, opens in a new tab"',
            footer,
        )
        self.assertIn(
            'href="mailto:avisheksaha123@gmail.com" '
            'aria-label="Email Avishek Saha"',
            footer,
        )
        self.assertEqual(footer.count("opens in a new tab"), 2)

        article = self.page_html("/posts/llm-engineering-from-scratch-tokenizer/")
        self.assertIn('class="top-link"', article)
        self.assertIn("copy-code", article)
        self.assertIn(">GitHub</a>", article)
        self.assertNotIn(">X</a>", article)

    def test_closing_sections_and_footer_preserve_accessible_behavior(self) -> None:
        writing_source = (
            ROOT / "layouts/partials/home/writing-education.html"
        ).read_text(encoding="utf-8")
        contact_source = (ROOT / "layouts/partials/home/contact.html").read_text(
            encoding="utf-8"
        )
        footer_source = (ROOT / "layouts/partials/footer.html").read_text(
            encoding="utf-8"
        )
        index_source = (ROOT / "layouts/index.html").read_text(encoding="utf-8")

        expected_partial_order = (
            'partial "home/hero.html"',
            'partial "home/experience.html"',
            'partial "home/expertise.html"',
            'partial "home/selected-work.html"',
            'partial "home/writing-education.html"',
            'partial "home/contact.html"',
        )
        positions = [index_source.index(partial) for partial in expected_partial_order]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(index_source.count('partial "home/'), 6)

        for validation in (
            "data/profile.yaml is required",
            "data/profile.yaml must be a map",
            "profile.education must be a list of exactly two items",
            "profile.education items must be maps",
            "profile.education items must define nonblank string degree and institution",
            "profile.education detail must be a string",
        ):
            self.assertIn(validation, writing_source)

        shared_profile_validations = (
            "data/profile.yaml is required",
            "data/profile.yaml must be a map",
            "profile.name must be a nonblank string",
            "profile.social must be a map",
            "profile.social must define nonblank string github, linkedin, and email",
            "profile.social.github and profile.social.linkedin must be absolute HTTPS public URLs",
            "profile.social.email must be a valid mailto address",
        )
        for source in (contact_source, footer_source):
            for validation in shared_profile_validations:
                self.assertIn(validation, source)

        for preserved_behavior in (
            "menu-scroll-position",
            "partial \"extend_footer.html\"",
            "document.querySelectorAll('a[href^=\"#\"]')",
            "decodeURIComponent(this.getAttribute(\"href\").slice(1))",
            "if (!target) return",
            "prefers-reduced-motion: reduce",
            'target.focus({ preventScroll: true })',
            'history.replaceState(null, "", window.location.pathname + window.location.search)',
            'history.pushState(null, "", `#${id}`)',
            "const html = document.documentElement",
            "localStorage.setItem(\"pref-theme\", nextTheme)",
            'themeToggle.setAttribute("aria-pressed"',
            "copy-code",
        ):
            self.assertIn(preserved_behavior, footer_source)

        home_css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        base_css = (ROOT / "assets/css/extended/portfolio-base.css").read_text(
            encoding="utf-8"
        )
        footer_css = base_css.split(".portfolio-footer {", 1)[1].split("}", 1)[0]
        self.assertIn(
            "max-width: calc(var(--portfolio-max) + 40px)", footer_css
        )
        closing_css = home_css.split(".portfolio-closing-grid {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("grid-template-columns: 1fr 1fr", closing_css)
        contact_css = home_css.split(".portfolio-contact-band {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("grid-template-columns: 1fr auto", contact_css)
        self.assertIn("clip-path: inset(0 -100vmax)", contact_css)
        mobile_css = home_css.split("@media (max-width: 640px)", 1)[1]
        self.assertIn(
            ".portfolio-closing-grid, .portfolio-contact-band { grid-template-columns: 1fr; }",
            mobile_css,
        )
        text_link_css = home_css.split(".portfolio-text-link {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("min-height: 44px", text_link_css)
        self.assertIn("display: inline-flex", text_link_css)
        self.assertIn(
            ".portfolio-contact-band .portfolio-label { color: var(--portfolio-paper); }",
            home_css,
        )
        self.assertIn(
            ".portfolio-contact-band :focus-visible { outline-color: var(--portfolio-paper); }",
            home_css,
        )
        footer_link_css = base_css.split(".portfolio-footer-links a {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("min-width: 44px", footer_link_css)
        self.assertIn("min-height: 44px", footer_link_css)
        self.assertIn("display: inline-flex", footer_link_css)
        copyright_css = base_css.split(".portfolio-footer > span {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("min-height: 44px", copyright_css)
        self.assertIn("align-items: center", copyright_css)
        self.assertIn("margin-inline: 0", copyright_css)
        home_link_css = base_css.split(".portfolio-footer > span a {", 1)[1].split(
            "}", 1
        )[0]
        self.assertIn("min-height: 44px", home_link_css)
        self.assertIn("display: inline-flex", home_link_css)
        self.assertIn("align-items: center", home_link_css)

    def test_malformed_education_fails_with_deliberate_errors(self) -> None:
        first_item = (
            '  - institution: "University of British Columbia"\n'
            '    degree: "Master of Data Science"\n'
            '    period: "Sep 2022 to Jun 2023"\n'
            '    short_period: "2022 · 2023"\n'
            '    hero_signal: true\n'
            '    hero_order: 3\n'
        )
        cases = (
            (
                "null education",
                lambda content: content.replace(
                    "education:\n", "education: null\nunused_education:\n", 1
                ),
                "profile.education must be a list of exactly two items",
            ),
            (
                "scalar education",
                lambda content: content.replace(
                    "education:\n", "education: invalid\nunused_education:\n", 1
                ),
                "profile.education must be a list of exactly two items",
            ),
            (
                "null education item",
                lambda content: content.replace(first_item, "  - null\n", 1),
                "profile.education items must be maps",
            ),
            (
                "scalar education item",
                lambda content: content.replace(first_item, "  - invalid\n", 1),
                "profile.education items must be maps",
            ),
            (
                "blank degree",
                lambda content: content.replace(
                    '    degree: "Master of Data Science"\n',
                    '    degree: "   "\n',
                    1,
                ),
                "profile.education items must define nonblank string degree and institution",
            ),
            (
                "blank institution",
                lambda content: content.replace(
                    '  - institution: "University of British Columbia"\n',
                    '  - institution: "   "\n',
                    1,
                ),
                "profile.education items must define nonblank string degree and institution",
            ),
            (
                "non-string optional detail",
                lambda content: content.replace(
                    '    detail: "CGPA 3.91/4.00"\n', "    detail: 3.91\n", 1
                ),
                "profile.education detail must be a string",
            ),
        )
        generic_errors = (
            "reflect:",
            "range can't iterate",
            "can't evaluate field",
            "error calling isset",
            "error calling len",
        )
        for name, transform, expected_error in cases:
            with self.subTest(name=name):
                result, _ = self.build_with_profile_fixture(
                    transform, writing_only=True
                )
                output = (result.stdout + result.stderr).lower()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error.lower(), output)
                for generic_error in generic_errors:
                    self.assertNotIn(generic_error, output)

    def test_blank_optional_education_detail_has_no_separator(self) -> None:
        for name, detail in (("blank", ""), ("whitespace", "   ")):
            with self.subTest(name=name):
                result, html = self.build_with_profile_fixture(
                    lambda content, value=detail: content.replace(
                        '    detail: "CGPA 3.91/4.00"\n',
                        f'    detail: "{value}"\n',
                        1,
                    ),
                    writing_only=True,
                    capture_home=True,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    result.stdout + "\n" + result.stderr,
                )
                self.assertIsNotNone(html)
                writing = unescape(
                    html.split('id="writing"', 1)[1].split("</section>", 1)[0]
                )
                education_entry = writing.split(
                    "BSc Computer Science & Engineering", 1
                )[1].split("</p>", 1)[0]
                self.assertNotIn("·", education_entry)

    def test_malformed_profile_identity_and_social_fail_on_home_and_footer(self) -> None:
        social_block = (
            'social:\n'
            '  github: "https://github.com/sahaavi"\n'
            '  linkedin: "https://linkedin.com/in/sahaavi"\n'
            '  email: "mailto:avisheksaha123@gmail.com"\n'
        )
        cases = (
            (
                "missing name",
                lambda content: content.replace('name: "Avishek Saha"\n', "", 1),
                "profile.name must be a nonblank string",
            ),
            (
                "non-string name",
                lambda content: content.replace(
                    'name: "Avishek Saha"\n', "name: true\n", 1
                ),
                "profile.name must be a nonblank string",
            ),
            (
                "missing social",
                lambda content: content.replace(social_block, "", 1),
                "profile.social must be a map",
            ),
            (
                "scalar social",
                lambda content: content.replace(
                    "social:\n", "social: invalid\nunused_social:\n", 1
                ),
                "profile.social must be a map",
            ),
            (
                "missing github",
                lambda content: content.replace(
                    '  github: "https://github.com/sahaavi"\n', "", 1
                ),
                "profile.social must define nonblank string github, linkedin, and email",
            ),
            (
                "non-https linkedin",
                lambda content: content.replace(
                    '  linkedin: "https://linkedin.com/in/sahaavi"\n',
                    '  linkedin: "http://linkedin.com/in/sahaavi"\n',
                    1,
                ),
                "profile.social.github and profile.social.linkedin must be absolute HTTPS public URLs",
            ),
            (
                "malformed mailto",
                lambda content: content.replace(
                    '  email: "mailto:avisheksaha123@gmail.com"\n',
                    '  email: "avisheksaha123@gmail.com"\n',
                    1,
                ),
                "profile.social.email must be a valid mailto address",
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
        for footer_only in (False, True):
            for name, transform, expected_error in cases:
                with self.subTest(
                    renderer="footer" if footer_only else "homepage", name=name
                ):
                    result, _ = self.build_with_profile_fixture(
                        transform, footer_only=footer_only
                    )
                    output = (result.stdout + result.stderr).lower()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected_error.lower(), output)
                    for generic_error in generic_errors:
                        self.assertNotIn(generic_error, output)
