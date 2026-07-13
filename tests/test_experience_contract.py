from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from html import unescape
from pathlib import Path
from typing import Callable

from tests.site_harness import HugoSiteTestCase, ROOT


VALID_EDUCATION = """hero:
  supporting: "Profile supporting copy"
education:
  - degree: "First degree"
    institution: "First institution"
    period: "First period"
  - degree: "Second degree"
    institution: "Second institution"
    period: "Second period"
"""

VALID_ROLES = """roles:
  - period: "Role one period"
    title: "Role one"
    employer: "Employer one"
    location: "Location one"
    details: ["Role one detail"]
  - period: "Role two period"
    title: "Role two"
    employer: "Employer two"
    location: "Location two"
    details: ["Role two detail"]
  - period: "Role three period"
    title: "Role three"
    employer: "Employer three"
    location: "Location three"
    details: ["Role three detail"]
  - period: "Role four period"
    title: "Role four"
    employer: "Employer four"
    location: "Location four"
    details: ["Role four detail"]
"""

VALID_GROUPS = """groups:
  - title: "Group one"
    summary: "Group one summary"
  - title: "Group two"
    summary: "Group two summary"
  - title: "Group three"
    summary: "Group three summary"
  - title: "Group four"
    summary: "Group four summary"
"""


class ExperienceRouteTests(HugoSiteTestCase):
    def build_full_site_with_experience_transform(
        self,
        transform: Callable[[str], str],
    ) -> subprocess.CompletedProcess[str]:
        """Build the real homepage and experience route against one mutation."""
        with tempfile.TemporaryDirectory(prefix="portfolio-shared-experience-") as temp:
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
            experience_path = source / "data/experience.yaml"
            original = experience_path.read_text(encoding="utf-8")
            transformed = transform(original)
            self.assertNotEqual(
                transformed,
                original,
                "Fixture did not modify data/experience.yaml",
            )
            experience_path.write_text(transformed, encoding="utf-8")
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

    def build_with_data_fixture(
        self,
        relative_path: str,
        fixture: str | None,
    ) -> subprocess.CompletedProcess[str]:
        """Build only the experience data consumer against an isolated fixture."""
        with tempfile.TemporaryDirectory(prefix="portfolio-experience-invalid-") as temp:
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
            fixture_path = source / relative_path
            if fixture is None:
                fixture_path.unlink()
            else:
                fixture_path.write_text(fixture, encoding="utf-8")

            # Keep the malformed-data check isolated from homepage and shared-shell
            # consumers so each failure comes from the experience layout itself.
            (source / "layouts/index.html").write_text(
                '{{ define "main" }}<p>Fixture home</p>{{ end }}\n',
                encoding="utf-8",
            )
            (source / "layouts/partials/header.html").write_text(
                '<header><a href="/">Fixture home</a></header>\n',
                encoding="utf-8",
            )
            (source / "layouts/partials/footer.html").write_text(
                "<footer>Fixture footer</footer>\n",
                encoding="utf-8",
            )
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

    def test_experience_is_the_canonical_profile(self) -> None:
        raw_html = self.page_html("/experience/")
        html = unescape(raw_html)
        self.assertIn("Professional experience", html)
        self.assertIn("Data & Applied AI Analyst", html)
        self.assertIn("Data Scientist, Applied AI", html)
        self.assertIn("Capstone Data Scientist", html)
        self.assertIn("Co-Founder / Data Scientist", html)

        ordered_copy = (
            "Professional experience",
            "Experience",
            "Data & Applied AI Analyst",
            "Data Scientist, Applied AI",
            "Capstone Data Scientist",
            "Co-Founder / Data Scientist",
            "Education",
            "Master of Data Science",
            "BSc Computer Science & Engineering",
            "Engineering range",
            "Applied AI systems",
            "Machine learning",
            "Software & data",
            "Delivery & trust",
        )
        cursor = -1
        for copy in ordered_copy:
            with self.subTest(copy=copy):
                next_index = html.find(copy, cursor + 1)
                self.assertGreater(next_index, cursor, copy)
                cursor = next_index

        for detail in (
            "Built a 150-case AI evaluation harness with RAGAS",
            "Owned label definition, contextual feature engineering",
            "Designed a reusable event and feature foundation",
            "Contributed to production Python services",
            "Built predictive ML prototypes",
            "Contributed to document-intelligence and data workflows",
            "Implemented K-means and hierarchical clustering",
            "Produced cluster profiles and policy-facing findings",
            "Co-founded a software firm",
            "Managed project scope, implementation, client communication",
        ):
            with self.subTest(detail=detail):
                self.assertIn(detail, html)

        for education_copy in (
            "University of British Columbia",
            "Sep 2022 to Jun 2023",
            "American International University-Bangladesh",
            "Jan 2018 to Sep 2021",
            "CGPA 3.91/4.00",
        ):
            with self.subTest(education=education_copy):
                self.assertIn(education_copy, html)

        for summary in (
            "LLM integration, RAG, agent and tool workflows",
            "Feature engineering, anomaly detection, ranking",
            "Python, FastAPI, REST and WebSocket APIs",
            "MLOps practices, Docker, cloud deployment",
        ):
            with self.subTest(summary=summary):
                self.assertIn(summary, html)

        lowered = html.lower()
        for forbidden in ("4+ years", "resume", "download", ".pdf"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, lowered)
        self.assertNotIn(" download=", lowered)
        self.assertIsNone(
            re.search(r"(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}", html)
        )
        self.assertNotIn("source_refs", html)
        self.assertNotIn("claim:stan-bcrtc", html)
        self.assertNotIn("project:content/", html)

    def test_about_redirects_to_experience(self) -> None:
        html = unescape(self.page_html("/about/"))
        self.assertIn("/experience/", html)
        self.assertRegex(
            html,
            r'(?is)<meta[^>]+http-equiv=["\']refresh["\'][^>]+/experience/',
        )
        self.assertRegex(
            html,
            r'(?is)<link[^>]+rel=["\']canonical["\'][^>]+/experience/',
        )
        self.assertRegex(
            html,
            r'(?is)<meta[^>]+name=["\']robots["\'][^>]+content=["\']noindex["\']',
        )
        for stale_copy in (
            "Applied AI engineer with a data science and analytics background",
            "What I Build",
            "Selected Projects",
            "Certifications",
        ):
            with self.subTest(stale_copy=stale_copy):
                self.assertNotIn(stale_copy, html)
        lowered = html.lower()
        for forbidden in ("4+ years", "resume", "download", ".pdf"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, lowered)

    def test_experience_has_semantic_hierarchy_and_active_navigation(self) -> None:
        html = unescape(self.page_html("/experience/"))
        page = html.split('<article class="portfolio-experience-page">', 1)[1]
        self.assertEqual(len(re.findall(r"<h1(?:\s|>)", page)), 1)
        self.assertEqual(len(re.findall(r"<h2(?:\s|>)", page)), 3)
        self.assertEqual(len(re.findall(r"<h3(?:\s|>)", page)), 8)
        self.assertEqual(page.count('class="portfolio-role-detail"'), 4)
        self.assertEqual(page.count('class="portfolio-education-item"'), 2)
        self.assertEqual(page.count('class="portfolio-expertise-item"'), 4)

        expected_detail_counts = (3, 3, 2, 2)
        role_cards = page.split('class="portfolio-role-detail"')[1:]
        self.assertEqual(len(role_cards), 4)
        for card, expected_count in zip(role_cards, expected_detail_counts):
            with self.subTest(expected_count=expected_count):
                card = card.split("</article>", 1)[0]
                self.assertIn("<ul", card)
                self.assertEqual(card.count("<li>"), expected_count)

        self.assertEqual(html.count('aria-current="page"'), 1)
        experience_anchor = html.split(">Experience</a>", 1)[0].rsplit("<a", 1)[1]
        self.assertIn('aria-current="page"', experience_anchor)

    def test_role_metrics_stay_scoped_to_brainstation_experience(self) -> None:
        html = unescape(self.page_html("/experience/"))
        page = html.split('<article class="portfolio-experience-page">', 1)[1]
        role_cards = [
            card.split("</article>", 1)[0]
            for card in page.split('class="portfolio-role-detail"')[1:]
        ]
        self.assertEqual(len(role_cards), 4)
        self.assertEqual(page.count('class="portfolio-role-metrics"'), 1)

        brainstation_cards = [
            card for card in role_cards if "Brain Station 23" in card
        ]
        self.assertEqual(len(brainstation_cards), 1)
        brainstation = brainstation_cards[0]
        self.assertIn('class="portfolio-role-metrics"', brainstation)
        for value, label in (
            ("21%", "analysis efficiency"),
            ("17%", "data consistency"),
            ("26%", "query performance"),
        ):
            with self.subTest(value=value, label=label):
                self.assertIn(f"<dt>{value}</dt>", brainstation)
                self.assertIn(f"<dd>{label}</dd>", brainstation)

        for card in role_cards:
            if card == brainstation:
                continue
            self.assertNotIn('class="portfolio-role-metrics"', card)
            for metric_copy in (
                "analysis efficiency",
                "data consistency",
                "query performance",
            ):
                self.assertNotIn(metric_copy, card)
            for value in ("21%", "17%", "26%"):
                self.assertNotIn(f"<dt>{value}</dt>", card)

    def test_experience_layout_validates_each_structured_data_source(self) -> None:
        source = (ROOT / "layouts/_default/experience.html").read_text(
            encoding="utf-8"
        )
        for error in (
            "data/profile.yaml is required for the experience page",
            "data/profile.yaml must be a map for the experience page",
            "data/profile.yaml hero must be a map for the experience page",
            "data/profile.yaml hero.supporting must be a nonblank string for the experience page",
            "data/profile.yaml education must be a list of exactly two items for the experience page",
            "data/profile.yaml education item must be a map for the experience page",
            "data/profile.yaml education items must define nonblank string degree, institution, and period",
            "data/profile.yaml education item detail must be a string when provided",
            "data/experience.yaml is required for the experience page",
            "data/experience.yaml must be a map for the experience page",
            "data/experience.yaml roles must be a list of exactly four items for the experience page",
            "data/experience.yaml role item must be a map for the experience page",
            "data/experience.yaml roles must define nonblank string period, title, employer, and location",
            "data/experience.yaml role details must be a nonempty list for the experience page",
            "data/experience.yaml role details must contain only nonblank strings",
            "data/experience.yaml role metrics must be a nonempty list for the experience page",
            "data/experience.yaml role metrics items must be maps for the experience page",
            "data/experience.yaml role metrics must define nonblank string value and label",
            "data/expertise.yaml is required for the experience page",
            "data/expertise.yaml must be a map for the experience page",
            "data/expertise.yaml groups must be a list of exactly four items for the experience page",
            "data/expertise.yaml group item must be a map for the experience page",
            "data/expertise.yaml groups must define nonblank string title and summary",
        ):
            with self.subTest(error=error):
                self.assertIn(error, source)
        self.assertIn("if $pageDataValid", source)

    def test_experience_styles_keep_the_two_to_one_grid_contract(self) -> None:
        css = (ROOT / "assets/css/extended/portfolio-base.css").read_text(
            encoding="utf-8"
        )
        home_css = (ROOT / "assets/css/extended/portfolio-home.css").read_text(
            encoding="utf-8"
        )
        for selector in (
            ".portfolio-experience-page",
            ".portfolio-role-detail",
            ".portfolio-role-metrics",
            ".portfolio-education-list",
            ".portfolio-experience-expertise",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)
        self.assertIn("@media (max-width: 640px)", css)
        mobile = css.rsplit("@media (max-width: 640px)", 1)[1]
        self.assertIn(
            ".portfolio-role-detail, .portfolio-experience-expertise { grid-template-columns: 1fr; }",
            mobile,
        )
        self.assertIn(".portfolio-home .portfolio-meta {", home_css)
        self.assertIsNone(re.search(r"(?m)^\.portfolio-meta\s*\{", home_css))
        experience_meta = css.split(".portfolio-meta {", 1)[1].split("}", 1)[0]
        self.assertIn("font-size: 0.9rem", experience_meta)
        metric_labels = css.split(".portfolio-role-metrics dd {", 1)[1].split(
            "}", 1
        )[0]
        self.assertRegex(metric_labels, r"font:\s*\d+\s+10px")

    def test_malformed_experience_data_fails_deliberately(self) -> None:
        education_items = VALID_EDUCATION.split("education:\n", 1)[1]
        profile_cases = (
            (
                "missing profile root",
                None,
                "data/profile.yaml is required for the experience page",
            ),
            (
                "wrong profile root",
                "- not-a-map\n",
                "data/profile.yaml must be a map for the experience page",
            ),
            (
                "wrong hero collection",
                f"hero: []\neducation:\n{education_items}",
                "data/profile.yaml hero must be a map for the experience page",
            ),
            (
                "blank supporting copy",
                VALID_EDUCATION.replace(
                    'supporting: "Profile supporting copy"', 'supporting: "   "'
                ),
                "data/profile.yaml hero.supporting must be a nonblank string for the experience page",
            ),
            (
                "wrong education collection",
                'hero:\n  supporting: "Profile supporting copy"\neducation: {}\n',
                "data/profile.yaml education must be a list of exactly two items for the experience page",
            ),
            (
                "wrong education count",
                'hero:\n  supporting: "Profile supporting copy"\neducation:\n'
                '  - {degree: "Only", institution: "One", period: "Now"}\n',
                "data/profile.yaml education must be a list of exactly two items for the experience page",
            ),
            (
                "wrong education item",
                'hero:\n  supporting: "Profile supporting copy"\neducation:\n'
                '  - not-a-map\n  - {degree: "Two", institution: "Two", period: "Two"}\n',
                "data/profile.yaml education item must be a map for the experience page",
            ),
            (
                "blank education field",
                VALID_EDUCATION.replace('degree: "First degree"', 'degree: " "'),
                "data/profile.yaml education items must define nonblank string degree, institution, and period",
            ),
            (
                "wrong education detail type",
                VALID_EDUCATION.replace(
                    'period: "First period"', 'period: "First period"\n    detail: 42'
                ),
                "data/profile.yaml education item detail must be a string when provided",
            ),
        )

        role_items = VALID_ROLES.split("roles:\n", 1)[1]
        experience_cases = (
            (
                "missing experience root",
                None,
                "data/experience.yaml is required for the experience page",
            ),
            (
                "wrong experience root",
                "- not-a-map\n",
                "data/experience.yaml must be a map for the experience page",
            ),
            (
                "wrong roles collection",
                "roles: {}\n",
                "data/experience.yaml roles must be a list of exactly four items for the experience page",
            ),
            (
                "wrong role count",
                "roles:\n" + role_items.rsplit("  - period:", 1)[0],
                "data/experience.yaml roles must be a list of exactly four items for the experience page",
            ),
            (
                "wrong role item",
                VALID_ROLES.replace(
                    '  - period: "Role one period"\n'
                    '    title: "Role one"\n'
                    '    employer: "Employer one"\n'
                    '    location: "Location one"\n'
                    '    details: ["Role one detail"]',
                    "  - not-a-map",
                ),
                "data/experience.yaml role item must be a map for the experience page",
            ),
            (
                "blank role field",
                VALID_ROLES.replace('title: "Role one"', 'title: " "'),
                "data/experience.yaml roles must define nonblank string period, title, employer, and location",
            ),
            (
                "wrong role details collection",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]', "details: {}", 1
                ),
                "data/experience.yaml role details must be a nonempty list for the experience page",
            ),
            (
                "blank role detail",
                VALID_ROLES.replace('details: ["Role one detail"]', 'details: [" "]'),
                "data/experience.yaml role details must contain only nonblank strings",
            ),
            (
                "wrong role metrics collection",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n    metrics: {}',
                    1,
                ),
                "data/experience.yaml role metrics must be a nonempty list for the experience page",
            ),
            (
                "empty role metrics",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n    metrics: []',
                    1,
                ),
                "data/experience.yaml role metrics must be a nonempty list for the experience page",
            ),
            (
                "wrong role metric item",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n    metrics: [not-a-map]',
                    1,
                ),
                "data/experience.yaml role metrics items must be maps for the experience page",
            ),
            (
                "blank role metric value",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n'
                    '    metrics:\n      - {value: " ", label: "Label"}',
                    1,
                ),
                "data/experience.yaml role metrics must define nonblank string value and label",
            ),
            (
                "wrong role metric value type",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n'
                    '    metrics:\n      - {value: 21, label: "Label"}',
                    1,
                ),
                "data/experience.yaml role metrics must define nonblank string value and label",
            ),
            (
                "blank role metric label",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n'
                    '    metrics:\n      - {value: "21%", label: " "}',
                    1,
                ),
                "data/experience.yaml role metrics must define nonblank string value and label",
            ),
            (
                "wrong role metric label type",
                VALID_ROLES.replace(
                    'details: ["Role one detail"]',
                    'details: ["Role one detail"]\n'
                    '    metrics:\n      - {value: "21%", label: 42}',
                    1,
                ),
                "data/experience.yaml role metrics must define nonblank string value and label",
            ),
        )

        group_items = VALID_GROUPS.split("groups:\n", 1)[1]
        expertise_cases = (
            (
                "missing expertise root",
                None,
                "data/expertise.yaml is required for the experience page",
            ),
            (
                "wrong expertise root",
                "- not-a-map\n",
                "data/expertise.yaml must be a map for the experience page",
            ),
            (
                "wrong groups collection",
                "groups: false\n",
                "data/expertise.yaml groups must be a list of exactly four items for the experience page",
            ),
            (
                "wrong group count",
                "groups:\n" + group_items.rsplit("  - title:", 1)[0],
                "data/expertise.yaml groups must be a list of exactly four items for the experience page",
            ),
            (
                "wrong group item",
                VALID_GROUPS.replace(
                    '  - title: "Group one"\n'
                    '    summary: "Group one summary"',
                    "  - not-a-map",
                ),
                "data/expertise.yaml group item must be a map for the experience page",
            ),
            (
                "blank group field",
                VALID_GROUPS.replace('summary: "Group one summary"', 'summary: " "'),
                "data/expertise.yaml groups must define nonblank string title and summary",
            ),
        )

        for relative_path, cases in (
            ("data/profile.yaml", profile_cases),
            ("data/experience.yaml", experience_cases),
            ("data/expertise.yaml", expertise_cases),
        ):
            for label, fixture, expected_error in cases:
                with self.subTest(case=label):
                    result = self.build_with_data_fixture(relative_path, fixture)
                    output = result.stdout + result.stderr
                    self.assertNotEqual(result.returncode, 0, output)
                    self.assertIn(expected_error, output)
                    for generic_error in (
                        "can't evaluate field",
                        "wrong type for value",
                        "index of untyped nil",
                        "slice bounds out of range",
                        "can't iterate over",
                    ):
                        self.assertNotIn(generic_error, output.lower())

    def test_shared_consumers_reject_malformed_role_metrics_deliberately(self) -> None:
        metrics_block = """    metrics:
      - value: "21%"
        label: "analysis efficiency"
      - value: "17%"
        label: "data consistency"
      - value: "26%"
        label: "query performance"
"""
        cases = (
            (
                "null metrics",
                "    metrics: null\n",
                "experience metrics must be a nonempty list",
                "data/experience.yaml role metrics must be a nonempty list for the experience page",
            ),
            (
                "scalar metrics",
                '    metrics: "not-a-list"\n',
                "experience metrics must be a nonempty list",
                "data/experience.yaml role metrics must be a nonempty list for the experience page",
            ),
            (
                "empty metrics",
                "    metrics: []\n",
                "experience metrics must be a nonempty list",
                "data/experience.yaml role metrics must be a nonempty list for the experience page",
            ),
            (
                "non-map metric item",
                "    metrics:\n      - not-a-map\n",
                "experience metrics items must be maps",
                "data/experience.yaml role metrics items must be maps for the experience page",
            ),
            (
                "blank metric field",
                metrics_block.replace('value: "21%"', 'value: " "', 1),
                "experience metrics must define value and label",
                "data/experience.yaml role metrics must define nonblank string value and label",
            ),
            (
                "wrong metric field type",
                metrics_block.replace(
                    'label: "analysis efficiency"', "label: 42", 1
                ),
                "experience metrics must define value and label",
                "data/experience.yaml role metrics must define nonblank string value and label",
            ),
        )

        for label, replacement, home_error, experience_error in cases:
            with self.subTest(case=label):
                result = self.build_full_site_with_experience_transform(
                    lambda source, replacement=replacement: source.replace(
                        metrics_block, replacement, 1
                    )
                )
                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0, output)
                self.assertIn(home_error, output)
                self.assertIn(experience_error, output)
                for generic_error in (
                    "can't evaluate field",
                    "can't iterate over",
                    "can't range over",
                    "wrong type for value",
                    "index of untyped nil",
                    "error calling len",
                    "reflect:",
                ):
                    self.assertNotIn(generic_error, output.lower())
