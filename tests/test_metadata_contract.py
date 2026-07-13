from __future__ import annotations

import json
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from tests.site_harness import HugoSiteTestCase, ROOT


EXPECTED_TITLE = "Avishek Saha | Applied AI & ML Engineer"
EXPECTED_DESCRIPTION = (
    "Applied AI and machine learning engineer with experience across LLM "
    "applications, RAG and evaluation, predictive ML, APIs, data systems, and "
    "cloud delivery."
)
EXPECTED_SAME_AS = {
    "https://github.com/sahaavi",
    "https://linkedin.com/in/sahaavi",
}


class MetadataContractTests(HugoSiteTestCase):
    def schema_payloads(self, route: str) -> list[dict[str, object]]:
        html = self.page_html(route)
        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        )
        self.assertTrue(blocks, f"Expected structured data on {route}")
        payloads: list[dict[str, object]] = []
        for block in blocks:
            payload = json.loads(block)
            self.assertIsInstance(payload, dict)
            payloads.append(payload)
        return payloads

    def build_with_html_sensitive_project_title(
        self,
    ) -> tuple[subprocess.CompletedProcess[str], str]:
        with tempfile.TemporaryDirectory(prefix="portfolio-schema-safe-") as temp:
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
            project_path = source / "content/projects/govtintel/index.md"
            project = project_path.read_text(encoding="utf-8")
            mutated = re.sub(
                r"(?m)^title:.*$",
                "title: 'GovIntel <RAG> & \"evaluation\" </script>'",
                project,
                count=1,
            )
            self.assertNotEqual(project, mutated)
            project_path.write_text(mutated, encoding="utf-8")
            output = source / "public"
            result = subprocess.run(
                [
                    "hugo",
                    "--gc",
                    "--minify",
                    "--enableGitInfo=false",
                    "--cleanDestinationDir",
                    "--destination",
                    str(output),
                ],
                cwd=source,
                check=False,
                capture_output=True,
                text=True,
            )
            html = (
                (output / "projects/govtintel/index.html").read_text(encoding="utf-8")
                if result.returncode == 0
                else ""
            )
            return result, html

    def build_with_research_publication_transform(
        self,
        transform,
    ) -> tuple[subprocess.CompletedProcess[str], str]:
        with tempfile.TemporaryDirectory(
            prefix="portfolio-publication-invalid-"
        ) as temp:
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
            project_path = source / "content/projects/asd-prediction/index.md"
            project = project_path.read_text(encoding="utf-8")
            mutated = transform(project)
            self.assertNotEqual(project, mutated, "Publication fixture made no change")
            project_path.write_text(mutated, encoding="utf-8")
            output = source / "public"
            result = subprocess.run(
                [
                    "hugo",
                    "--gc",
                    "--minify",
                    "--enableGitInfo=false",
                    "--cleanDestinationDir",
                    "--destination",
                    str(output),
                ],
                cwd=source,
                check=False,
                capture_output=True,
                text=True,
            )
            html = (
                (
                    output / "projects/autism-spectrum-disorder-prediction/index.html"
                ).read_text(encoding="utf-8")
                if result.returncode == 0
                else ""
            )
            return result, html

    def test_homepage_title_description_canonical_and_social_image(self) -> None:
        html = self.page_html("/")
        self.assertIn(f"<title>{EXPECTED_TITLE}</title>", html)
        self.assertIn(
            f'<meta name="description" content="{EXPECTED_DESCRIPTION}">', html
        )
        self.assertIn('<link rel="canonical" href="https://avisheksaha.com/">', html)
        self.assertIn(
            '<meta property="og:image" '
            'content="https://avisheksaha.com/images/og-image.png">',
            html,
        )
        self.assertIn(
            '<meta name="twitter:image" '
            'content="https://avisheksaha.com/images/og-image.png">',
            html,
        )
        image_url = re.search(r'<meta property="og:image" content="([^"]+)">', html)
        self.assertIsNotNone(image_url)
        parsed = urlsplit(image_url.group(1))
        self.assertEqual(parsed.netloc, "avisheksaha.com")
        self.assertTrue((self.output_dir / parsed.path.lstrip("/")).is_file())

    def test_metadata_leads_with_ai_ml_without_legacy_keyword_stuffing(self) -> None:
        html = self.page_html("/")
        keywords = re.search(r'<meta name="keywords" content="([^"]*)">', html)
        self.assertIsNotNone(keywords)
        keyword_text = keywords.group(1)
        self.assertIn("Applied AI Engineer", keyword_text)
        self.assertIn("Machine Learning Engineer", keyword_text)
        for obsolete in (
            "SQL",
            "Azure AI Foundry",
            "Copilot Studio",
            "Power Platform",
            "Anthropic API",
        ):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, keyword_text)

    def test_social_image_is_local_png_with_canonical_dimensions(self) -> None:
        image_path = ROOT / "static/images/og-image.png"
        data = image_path.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1200, 630))
        self.assertLess(len(data), 500_000, "OG image should remain web-efficient")

    def test_homepage_schema_is_profile_page_with_person_identity(self) -> None:
        profile = next(
            payload
            for payload in self.schema_payloads("/")
            if payload.get("@type") == "ProfilePage"
        )
        self.assertEqual(profile["name"], EXPECTED_TITLE)
        self.assertEqual(profile["description"], EXPECTED_DESCRIPTION)
        person = profile["mainEntity"]
        self.assertIsInstance(person, dict)
        self.assertEqual(person["@type"], "Person")
        self.assertEqual(person["name"], "Avishek Saha")
        self.assertEqual(person["jobTitle"], "Applied AI & ML Engineer")
        self.assertEqual(person["image"], "https://avisheksaha.com/images/og-image.png")
        self.assertEqual(set(person["sameAs"]), EXPECTED_SAME_AS)

    def test_code_and_research_projects_emit_appropriate_schema(self) -> None:
        code = next(
            payload
            for payload in self.schema_payloads("/projects/govtintel/")
            if payload.get("@type") == "SoftwareSourceCode"
        )
        self.assertEqual(
            code["description"],
            (
                "A local-first federal procurement intelligence RAG system that turns "
                "USAspending contract awards into citation-grounded market briefs."
            ),
        )
        self.assertEqual(code["codeRepository"], "https://github.com/sahaavi/GovtIntel")

        research_payloads = self.schema_payloads(
            "/projects/autism-spectrum-disorder-prediction/"
        )
        self.assertFalse(
            any(
                payload.get("@type") == "ScholarlyArticle"
                for payload in research_payloads
            ),
            "The portfolio case study must not impersonate the journal article.",
        )
        research_page = next(
            payload
            for payload in research_payloads
            if payload.get("@type") == "WebPage"
        )
        self.assertEqual(
            research_page["name"], "Autism Screening Data Dashboard Research"
        )
        self.assertTrue(str(research_page["description"]).strip())
        self.assertEqual(research_page["author"]["name"], "Avishek Saha")
        self.assertNotIn("codeRepository", research_page)

        article = research_page["about"]
        self.assertEqual(article["@type"], "ScholarlyArticle")
        self.assertEqual(
            article["name"],
            "Development of an Interactive Dashboard for Analyzing Autism "
            "Spectrum Disorder (ASD) Data using Machine Learning",
        )
        self.assertEqual(
            [author["name"] for author in article["author"]],
            [
                "Avishek Saha",
                "Dibakar Barua",
                "Mahbub C. Mishu",
                "Ziad Mohib",
                "Sumaya Binte Zilani Choya",
            ],
        )
        self.assertEqual(article["datePublished"], "2022-08-08")
        self.assertEqual(article["pagination"], "14-24")
        self.assertEqual(article["pageStart"], 14)
        self.assertEqual(article["pageEnd"], 24)
        self.assertEqual(
            article["identifier"], "https://doi.org/10.5815/ijitcs.2022.04.02"
        )
        self.assertEqual(article["url"], "https://doi.org/10.5815/ijitcs.2022.04.02")
        self.assertEqual(
            article["sameAs"],
            "https://www.mecs-press.org/ijitcs/ijitcs-v14-n4/v14n4-2.html",
        )
        issue = article["isPartOf"]
        self.assertEqual(issue["@type"], "PublicationIssue")
        self.assertEqual(issue["issueNumber"], "4")
        volume = issue["isPartOf"]
        self.assertEqual(volume["@type"], "PublicationVolume")
        self.assertEqual(volume["volumeNumber"], "14")
        journal = volume["isPartOf"]
        self.assertEqual(journal["@type"], "Periodical")
        self.assertEqual(
            journal["name"],
            "International Journal of Information Technology and Computer "
            "Science (IJITCS)",
        )
        for key in (
            "name",
            "datePublished",
            "pagination",
            "identifier",
            "url",
            "sameAs",
        ):
            with self.subTest(article_field=key):
                self.assertIsInstance(article[key], str)
                self.assertTrue(article[key].strip())
        self.assertTrue(article["author"])
        self.assertTrue(all(author["name"].strip() for author in article["author"]))
        self.assertNotIn("null", json.dumps(research_page))

    def test_research_bibliography_lives_in_structured_front_matter(self) -> None:
        source = (ROOT / "content/projects/asd-prediction/index.md").read_text(
            encoding="utf-8"
        )
        template = (ROOT / "layouts/partials/templates/schema_json.html").read_text(
            encoding="utf-8"
        )
        for field in (
            "publication:",
            'title: "Development of an Interactive Dashboard',
            "authors:",
            'date_published: "2022-08-08"',
            'doi_url: "https://doi.org/10.5815/ijitcs.2022.04.02"',
        ):
            with self.subTest(field=field):
                self.assertIn(field, source)
        for hardcoded in (
            "autism-spectrum-disorder-prediction",
            "Development of an Interactive Dashboard for Analyzing Autism",
            "10.5815/ijitcs.2022.04.02",
        ):
            with self.subTest(hardcoded=hardcoded):
                self.assertNotIn(hardcoded, template)

    def test_invalid_research_publication_metadata_fails_deliberately(self) -> None:
        publication_block = r"(?ms)^publication:\n.*?(?=^---\n)"
        cases = (
            (
                "publication scalar",
                lambda text: re.sub(
                    publication_block, "publication: false\n", text, count=1
                ),
                "publication must be a map",
            ),
            (
                "blank title",
                lambda text: re.sub(
                    r"(?m)^  title:.*$", '  title: "   "', text, count=1
                ),
                "publication.title must be a nonblank string",
            ),
            (
                "missing journal",
                lambda text: re.sub(r"(?m)^  journal:.*\n", "", text, count=1),
                "publication.journal must be a nonblank string",
            ),
            (
                "empty authors",
                lambda text: re.sub(
                    r"(?m)^  authors:\n(?:    - .*\n)+",
                    "  authors: []\n",
                    text,
                    count=1,
                ),
                "publication.authors must be a nonempty list",
            ),
            (
                "blank author",
                lambda text: text.replace('    - "Avishek Saha"', '    - "   "', 1),
                "publication.authors items must be nonblank strings",
            ),
            (
                "nonstring author",
                lambda text: text.replace('    - "Avishek Saha"', "    - 42", 1),
                "publication.authors items must be nonblank strings",
            ),
            (
                "missing DOI",
                lambda text: re.sub(r"(?m)^  doi_url:.*\n", "", text, count=1),
                "publication.doi_url must be a nonblank string",
            ),
            (
                "javascript DOI",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "javascript:alert(1)"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "wrong DOI host",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://example.com/10.5815/ijitcs.2022.04.02"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "DOI userinfo",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://user@doi.org/10.5815/ijitcs.2022.04.02"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "bare DOI resolver",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "query-only DOI resolver",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/?doi=10.5815/ijitcs.2022.04.02"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "fragment-only DOI resolver",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/#10.5815/ijitcs.2022.04.02"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "arbitrary DOI path",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/foo"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "short DOI registrant",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.123/article"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "missing DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1234/"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "whitespace in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.5815/bad suffix"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "slash-only DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1234//"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded slash-only DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%2F"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded whitespace-only DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%20"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "embedded encoded space in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%20def"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "embedded encoded Unicode separator in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%E3%80%80def"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "embedded encoded Unicode line separator in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%E2%80%A8def"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "embedded encoded zero-width space in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%E2%80%8Bdef"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "embedded encoded bidi override in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%E2%80%AEdef"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded slash and Unicode whitespace-only DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%2F%E3%80%80%2F"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded NUL in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%00"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded tab in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%09"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded DEL in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%7F"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "encoded Unicode C1 control in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%C2%80"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "dangling DOI percent escape",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "short DOI percent escape",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%2"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "nonhex DOI percent escape",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc%ZZ"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "invalid UTF-8 leading byte in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%FF"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "overlong UTF-8 sequence in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%C0%80"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "UTF-8 surrogate sequence in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%ED%A0%80"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "out-of-range UTF-8 sequence in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%F4%90%80%80"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "incomplete UTF-8 sequence in DOI suffix",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/%E2%82"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "DOI suffix query",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc?version=1"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "DOI suffix fragment",
                lambda text: re.sub(
                    r"(?m)^  doi_url:.*$",
                    '  doi_url: "https://doi.org/10.1000/abc#section"',
                    text,
                    count=1,
                ),
                "publication.doi_url must be an absolute https://doi.org/ URL",
            ),
            (
                "HTTP record URL",
                lambda text: text.replace(
                    "https://www.mecs-press.org/ijitcs/",
                    "http://www.mecs-press.org/ijitcs/",
                    1,
                ),
                "publication.record_url must be an absolute HTTPS URL",
            ),
            (
                "relative record URL",
                lambda text: re.sub(
                    r"(?m)^  record_url:.*$",
                    '  record_url: "/ijitcs/v14n4-2.html"',
                    text,
                    count=1,
                ),
                "publication.record_url must be an absolute HTTPS URL",
            ),
            (
                "record URL port",
                lambda text: text.replace(
                    "https://www.mecs-press.org/ijitcs/",
                    "https://www.mecs-press.org:443/ijitcs/",
                    1,
                ),
                "publication.record_url must be an absolute HTTPS URL",
            ),
            (
                "literal angle brackets in record URL",
                lambda text: re.sub(
                    r"(?m)^  record_url:.*$",
                    '  record_url: "https://example.com/<record>"',
                    text,
                    count=1,
                ),
                "publication.record_url must be an absolute HTTPS URL",
            ),
            (
                "malformed date",
                lambda text: re.sub(
                    r"(?m)^  date_published:.*$",
                    '  date_published: "August 8, 2022"',
                    text,
                    count=1,
                ),
                "publication.date_published must be a valid ISO YYYY-MM-DD date",
            ),
            (
                "invalid calendar date",
                lambda text: re.sub(
                    r"(?m)^  date_published:.*$",
                    '  date_published: "2022-02-30"',
                    text,
                    count=1,
                ),
                "publication.date_published must be a valid ISO YYYY-MM-DD date",
            ),
            (
                "noninteger page start",
                lambda text: text.replace("  page_start: 14", '  page_start: "14"', 1),
                "publication.page_start must be a positive integer",
            ),
            (
                "negative page end",
                lambda text: text.replace("  page_end: 24", "  page_end: -24", 1),
                "publication.page_end must be a positive integer",
            ),
            (
                "reversed page bounds",
                lambda text: text.replace("  page_start: 14", "  page_start: 25", 1),
                "publication.page_start must be less than or equal to publication.page_end",
            ),
            (
                "page range mismatch",
                lambda text: text.replace('  pages: "14-24"', '  pages: "15-24"', 1),
                "publication.pages must match publication.page_start-publication.page_end",
            ),
        )
        generic_errors = (
            "can't evaluate field",
            "range can't iterate over",
            "wrong type for value",
            "nil pointer evaluating",
            "error calling",
        )
        for label, transform, expected_error in cases:
            with self.subTest(case=label):
                result, _ = self.build_with_research_publication_transform(transform)
                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0, output)
                self.assertIn("projects/asd-prediction/index.md", output)
                self.assertIn(expected_error, output)
                for generic_error in generic_errors:
                    self.assertNotIn(generic_error, output.lower())

    def test_valid_encoded_and_legacy_doi_suffixes_are_preserved(self) -> None:
        crossref_sici_url = (
            "https://doi.org/10.1002/(SICI)1521-3951(199911)216:1"
            "<135::AID-PSSB135>3.0.CO;2-%23"
        )
        doi_urls = (
            "https://doi.org/10.1000/res%23test",
            "https://doi.org/10.1000/(SICI)123",
            "https://doi.org/10.1000/abc/def",
            "https://doi.org/10.1000/abc%2Fdef",
            "https://doi.org/10.5555/abc%3Cdef%3E%23ghi",
            "https://doi.org/10.1000/caf%C3%A9",
            "https://doi.org/10.1000/%E6%B5%8B%E8%AF%95",
            "https://doi.org/10.1000/%F0%9F%A4%96",
            crossref_sici_url,
        )
        for doi_url in doi_urls:
            with self.subTest(doi_url=doi_url):
                result, html = self.build_with_research_publication_transform(
                    lambda text, value=doi_url: re.sub(
                        r"(?m)^  doi_url:.*$",
                        f'  doi_url: "{value}"',
                        text,
                        count=1,
                    )
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                schema_blocks = re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>',
                    html,
                    re.S,
                )
                page_block = next(
                    block
                    for block in schema_blocks
                    if json.loads(block).get("@type") == "WebPage"
                )
                page = json.loads(page_block)
                article = page["about"]
                self.assertEqual(article["identifier"], doi_url)
                self.assertEqual(article["url"], doi_url)
                if doi_url == crossref_sici_url:
                    escaped_page_block = page_block.lower()
                    self.assertIn(r"\u003c", escaped_page_block)
                    self.assertIn(r"\u003e", escaped_page_block)
                    self.assertNotIn("<", page_block)
                    self.assertNotIn(">", page_block)

    def test_experience_is_a_described_profile_page_not_a_blog_post(self) -> None:
        payloads = self.schema_payloads("/experience/")
        self.assertFalse(
            any(payload.get("@type") == "BlogPosting" for payload in payloads)
        )
        profile = next(
            payload for payload in payloads if payload.get("@type") == "ProfilePage"
        )
        self.assertTrue(str(profile["description"]).strip())
        serialized = json.dumps(profile)
        for artifact in ("articleBody", "wordCount", "0001-01-01"):
            with self.subTest(artifact=artifact):
                self.assertNotIn(artifact, serialized)

    def test_experience_search_record_uses_canonical_data(self) -> None:
        records = json.loads(
            (self.output_dir / "index.json").read_text(encoding="utf-8")
        )
        experience = next(
            record
            for record in records
            if record["permalink"] == "https://avisheksaha.com/experience/"
        )
        self.assertTrue(str(experience["summary"]).strip())
        content = str(experience["content"])
        self.assertTrue(content.strip())
        self.assertIn("Data & Applied AI Analyst", content)
        self.assertIn("BC Rapid Transit Company", content)
        self.assertRegex(content, r"(?i)(AI|machine learning|LLM|RAG)")

    def test_published_post_remains_a_described_blog_post(self) -> None:
        payloads = self.schema_payloads(
            "/posts/llm-engineering-from-scratch-tokenizer/"
        )
        article = next(
            payload for payload in payloads if payload.get("@type") == "BlogPosting"
        )
        self.assertTrue(str(article["description"]).strip())

    def test_standalone_resource_pages_use_nonarticle_schema(self) -> None:
        cases = (
            (
                "/search/",
                "WebPage",
                "Search Avishek Saha's AI and ML projects, technical writing, "
                "and professional experience.",
            ),
            ("/archives/", "CollectionPage", None),
            ("/books/", "WebPage", "Books I’m reading and AI/ML resources I recommend"),
        )
        for route, expected_type, expected_description in cases:
            with self.subTest(route=route):
                payloads = self.schema_payloads(route)
                self.assertFalse(
                    any(payload.get("@type") == "BlogPosting" for payload in payloads)
                )
                page = next(
                    payload
                    for payload in payloads
                    if payload.get("@type") == expected_type
                )
                description = str(page["description"])
                self.assertTrue(description.strip())
                if expected_description is not None:
                    self.assertEqual(description, expected_description)
                self.assertNotIn("&rsquo;", description)

    def test_open_graph_distinguishes_posts_from_site_pages(self) -> None:
        post_html = self.page_html("/posts/llm-engineering-from-scratch-tokenizer/")
        self.assertEqual(
            re.findall(r'<meta property="og:type" content="([^"]+)">', post_html),
            ["article"],
        )
        self.assertIn('property="article:section" content="posts"', post_html)
        self.assertIn('property="article:published_time"', post_html)

        website_routes = (
            "/",
            "/experience/",
            "/search/",
            "/archives/",
            "/books/",
            "/projects/",
            "/projects/maintenance-eye/",
            "/projects/govtintel/",
            "/projects/llm-engineering-from-scratch/",
            "/projects/autism-spectrum-disorder-prediction/",
        )
        for route in website_routes:
            with self.subTest(route=route):
                html = self.page_html(route)
                self.assertEqual(
                    re.findall(r'<meta property="og:type" content="([^"]+)">', html),
                    ["website"],
                )
                self.assertIsNone(re.search(r'<meta property="article:[^"]+"', html))
                for property_name in (
                    "og:url",
                    "og:title",
                    "og:description",
                    "og:image",
                ):
                    matches = re.findall(
                        rf'<meta property="{property_name}" content="([^"]+)">',
                        html,
                    )
                    self.assertTrue(matches, f"Missing {property_name} on {route}")
                    self.assertTrue(matches[0].strip())
                self.assertEqual(
                    len(re.findall(r'<link rel="canonical" href="[^"]+">', html)),
                    1,
                )

        books_html = self.page_html("/books/")
        books_description = re.search(
            r'<meta property="og:description" content="([^"]+)">', books_html
        )
        self.assertIsNotNone(books_description)
        self.assertEqual(
            books_description.group(1),
            "Books I’m reading and AI/ML resources I recommend",
        )
        self.assertNotIn("&rsquo;", books_description.group(1))

    def test_all_schema_blocks_on_key_routes_are_valid_json(self) -> None:
        for route in (
            "/",
            "/experience/",
            "/search/",
            "/archives/",
            "/books/",
            "/projects/",
            "/projects/maintenance-eye/",
            "/projects/govtintel/",
            "/projects/llm-engineering-from-scratch/",
            "/projects/autism-spectrum-disorder-prediction/",
            "/posts/llm-engineering-from-scratch-tokenizer/",
        ):
            with self.subTest(route=route):
                self.schema_payloads(route)

    def test_schema_json_safely_encodes_html_sensitive_text(self) -> None:
        result, html = self.build_with_html_sensitive_project_title()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        )
        self.assertTrue(blocks)
        payloads = [json.loads(block) for block in blocks]
        project = next(
            item for item in payloads if item.get("@type") == "SoftwareSourceCode"
        )
        self.assertEqual(
            project["name"],
            'GovIntel <RAG> & "evaluation" </script>',
        )
        project_block = next(
            block for block in blocks if '"SoftwareSourceCode"' in block
        )
        self.assertNotIn("<RAG>", project_block)
        self.assertNotIn("</script>", project_block)
