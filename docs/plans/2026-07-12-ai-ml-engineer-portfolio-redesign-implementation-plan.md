# AI/ML Engineer Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the Hugo homepage and supporting portfolio surfaces into an experience-first Applied AI & ML Engineer portfolio while preserving PaperMod, Markdown content, existing routes, and GitHub Pages deployment.

**Architecture:** Keep Hugo 0.147 and PaperMod as the publishing foundation. Replace the monolithic homepage with small Hugo partials backed by structured YAML data and project front matter, add a scoped technical-editorial CSS system, and verify generated HTML through Python standard-library contract tests plus browser QA.

**Tech Stack:** Hugo 0.147.x, PaperMod, Go templates, YAML front matter/data, CSS, minimal vanilla JavaScript already provided by PaperMod, Python 3 `unittest`, GitHub Actions.

---

## Before Execution

1. Read `docs/design/2026-07-12-ai-ml-engineer-portfolio-redesign-design.md` completely.
2. Open the approved reference at `/home/avisaha/.gstack/projects/sahaavi-sahaavi.github.io/designs/engineer-dossier-20260712/homepage-preview.html`.
3. Execute in an isolated git worktree created from `master`.
4. Preserve the user's untracked `.omx/` directory. Never stage it.
5. Use the working hero statement stored in `data/profile.yaml`. The user can revise that single value without changing templates.
6. Do not create a downloadable resume, replace Hugo, add a frontend framework, or introduce unapproved portfolio claims.
7. Treat the exact experience and metric copy in Tasks 3 and 4 as the website-public disclosure bundle. Starting implementation after the user approves this plan authorizes only that listed copy; any additional ledger claim requires separate approval.

## Production File Map

### Create

- `data/profile.yaml` — identity, hero copy, evidence signals, social links, education, and contact content.
- `data/experience.yaml` — canonical website-visible roles, dates, summaries, evidence, and role metrics.
- `data/expertise.yaml` — four engineering-range groups and the five-stage AI/ML lifecycle.
- `layouts/_default/baseof.html` — minimal PaperMod-compatible shell override that gives the main landmark a skip-link target.
- `layouts/partials/header.html` — PaperMod-compatible header override with monogram, role descriptor, navigation, and existing theme control.
- `layouts/partials/home/hero.html` — hero and career-signal panel.
- `layouts/partials/home/experience.html` — current and prior professional experience.
- `layouts/partials/home/expertise.html` — AI/ML engineering range and lifecycle.
- `layouts/partials/home/selected-work.html` — exactly two equally weighted public systems.
- `layouts/partials/home/writing-education.html` — writing, research, and education proof.
- `layouts/partials/home/contact.html` — final contact band.
- `layouts/_default/experience.html` — web-native professional profile at `/experience/`.
- `content/experience.md` — route metadata and `/about/` alias.
- `assets/css/extended/portfolio-tokens.css` — fonts, colors, spacing, and PaperMod variable mapping.
- `assets/css/extended/portfolio-base.css` — shared typography, header, footer, focus, and layout rules.
- `assets/css/extended/portfolio-home.css` — homepage-only layout and responsive behavior.
- `assets/css/extended/portfolio-projects.css` — project list and project metadata presentation.
- `assets/css/extended/portfolio-blog.css` — existing blog-specific rules moved from `custom.css` without redesign.
- `static/fonts/instrument-sans-latin-wght-normal.woff2` — self-hosted display/body variable font.
- `static/fonts/ibm-plex-mono-latin-400-normal.woff2` — self-hosted technical-label font.
- `static/fonts/ibm-plex-mono-latin-500-normal.woff2` — self-hosted medium technical-label font.
- `static/fonts/LICENSE-Instrument-Sans.txt` — font license.
- `static/fonts/LICENSE-IBM-Plex-Mono.txt` — font license.
- `scripts/generate_og_image.py` — deterministic 1200×630 social-image generator.
- `static/images/og-image.png` — generated branded social image.
- `layouts/partials/templates/schema_json.html` — ProfilePage, SoftwareSourceCode, ScholarlyArticle, BlogPosting, and CollectionPage schema.
- `tests/site_harness.py` — reusable temporary Hugo-build harness.
- `tests/test_baseline.py` — build and route preservation.
- `tests/test_design_assets.py` — local fonts and design-token contract.
- `tests/test_homepage_contract.py` — hero, order, navigation, experience, expertise, selected work, and no-resume contract.
- `tests/test_experience_contract.py` — canonical experience route, titles, dates, and alias.
- `tests/test_project_contract.py` — grouped project index and safe project metadata.
- `tests/test_metadata_contract.py` — title, Open Graph, and JSON-LD contract.
- `tests/test_internal_links.py` — generated internal-link validation.

### Modify

- `layouts/index.html` — orchestrate the six homepage partials only.
- `layouts/partials/extend_head.html` — remove Google-hosted Inter and preload local fonts.
- `layouts/partials/footer.html` — retain PaperMod behavior while aligning contact/social presentation.
- `layouts/projects/list.html` — grouped work index.
- `layouts/projects/single.html` — metadata summary and independent previous/next navigation.
- `archetypes/projects.md` — structured project fields.
- `content/projects/vision-maintenance-agent/index.md` — safe featured metadata and local architecture image.
- `content/projects/govtintel/index.md` — safe featured metadata and local UI image.
- `content/projects/llm-engineering-from-scratch/index.md` — lab-series metadata.
- `content/projects/asd-prediction/index.md` — research/foundation metadata.
- `content/projects/_index.md` — work-index description.
- `hugo.yaml` — navigation, homepage metadata, social schema inputs, and social image.
- `.github/workflows/hugo.yml` — contract tests before production build.

### Delete After Migration

- `content/about.md` — replaced by `content/experience.md` with `/about/` alias.
- `assets/css/extended/custom.css` — replaced by scoped CSS files after its blog rules are preserved.

---

### Task 1: Add a Hugo Render-Test Harness

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/site_harness.py`
- Create: `tests/test_baseline.py`

- [ ] **Step 1: Create the empty test package**

```python
# tests/__init__.py
```

- [ ] **Step 2: Create the Hugo build harness**

```python
# tests/site_harness.py
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HugoSiteTestCase(unittest.TestCase):
    """Render the production Hugo site once per test class into a temp directory."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._temporary_directory = tempfile.TemporaryDirectory(prefix="portfolio-site-")
        cls.output_dir = Path(cls._temporary_directory.name)
        command = [
            "hugo",
            "--gc",
            "--minify",
            "--cleanDestinationDir",
            "--destination",
            str(cls.output_dir),
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise AssertionError(
                "Hugo build failed.\nSTDOUT:\n"
                + result.stdout
                + "\nSTDERR:\n"
                + result.stderr
            )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary_directory.cleanup()
        super().tearDownClass()

    def page_path(self, route: str) -> Path:
        normalized = route.strip("/")
        if not normalized:
            return self.output_dir / "index.html"
        return self.output_dir / normalized / "index.html"

    def page_html(self, route: str) -> str:
        path = self.page_path(route)
        self.assertTrue(path.is_file(), f"Expected generated page: {path}")
        return path.read_text(encoding="utf-8")
```

- [ ] **Step 3: Add baseline route tests**

```python
# tests/test_baseline.py
from tests.site_harness import HugoSiteTestCase


class BaselineSiteTests(HugoSiteTestCase):
    def test_existing_public_routes_render(self) -> None:
        for route in (
            "/",
            "/projects/",
            "/projects/maintenance-eye/",
            "/projects/govtintel/",
            "/posts/",
            "/search/",
            "/tags/",
            "/categories/",
        ):
            with self.subTest(route=route):
                self.page_html(route)

    def test_feeds_and_search_index_remain_generated(self) -> None:
        for relative_path in (
            "index.xml",
            "index.json",
            "posts/index.xml",
            "projects/index.xml",
            "tags/index.xml",
        ):
            with self.subTest(path=relative_path):
                self.assertTrue((self.output_dir / relative_path).is_file())

    def test_draft_projects_are_not_published(self) -> None:
        for route in (
            "/projects/pennymize-ai-powered-personal-finance/",
            "/projects/price-prediction-platform-on-aws/",
        ):
            with self.subTest(route=route):
                self.assertFalse(self.page_path(route).exists(), route)
```

- [ ] **Step 4: Run the baseline tests**

Run: `python3 -m unittest tests.test_baseline -v`
Expected: `Ran 3 tests` and `OK`.

- [ ] **Step 5: Commit the harness**

```bash
git add tests/__init__.py tests/site_harness.py tests/test_baseline.py
git commit -m "test: add Hugo site contract harness"
```

---

### Task 2: Self-Host Fonts and Establish Design Tokens

**Files:**
- Create: `tests/test_design_assets.py`
- Create: `static/fonts/instrument-sans-latin-wght-normal.woff2`
- Create: `static/fonts/ibm-plex-mono-latin-400-normal.woff2`
- Create: `static/fonts/ibm-plex-mono-latin-500-normal.woff2`
- Create: `static/fonts/LICENSE-Instrument-Sans.txt`
- Create: `static/fonts/LICENSE-IBM-Plex-Mono.txt`
- Create: `assets/css/extended/portfolio-tokens.css`
- Create: `assets/css/extended/portfolio-base.css`
- Modify: `layouts/partials/extend_head.html:1-3`
- Modify: `assets/css/extended/custom.css:1-31`

- [ ] **Step 1: Write the failing local-asset contract**

```python
# tests/test_design_assets.py
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

    def test_design_tokens_cover_light_and_dark_modes(self) -> None:
        css = (ROOT / "assets/css/extended/portfolio-tokens.css").read_text(
            encoding="utf-8"
        )
        self.assertIn("--portfolio-paper: #f5f7f4", css.lower())
        self.assertIn(':root[data-theme="dark"]', css)
        self.assertIn("--portfolio-paper: #08111c", css.lower())
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests.test_design_assets -v`
Expected: FAIL because the local font files and token stylesheet do not exist and Google Fonts is still referenced.

- [ ] **Step 3: Extract version-pinned Fontsource assets**

Run exactly:

```bash
font_tmp=$(mktemp -d)
npm pack --pack-destination "$font_tmp" @fontsource-variable/instrument-sans@5.2.8
npm pack --pack-destination "$font_tmp" @fontsource/ibm-plex-mono@5.2.7
mkdir -p static/fonts
mkdir -p "$font_tmp/instrument" "$font_tmp/plex"
tar -xzf "$font_tmp/fontsource-variable-instrument-sans-5.2.8.tgz" -C "$font_tmp/instrument"
tar -xzf "$font_tmp/fontsource-ibm-plex-mono-5.2.7.tgz" -C "$font_tmp/plex"
cp "$font_tmp/instrument/package/files/instrument-sans-latin-wght-normal.woff2" static/fonts/
cp "$font_tmp/instrument/package/LICENSE" static/fonts/LICENSE-Instrument-Sans.txt
cp "$font_tmp/plex/package/files/ibm-plex-mono-latin-400-normal.woff2" static/fonts/
cp "$font_tmp/plex/package/files/ibm-plex-mono-latin-500-normal.woff2" static/fonts/
cp "$font_tmp/plex/package/LICENSE" static/fonts/LICENSE-IBM-Plex-Mono.txt
```

Expected: three WOFF2 files and two license files under `static/fonts/`. The operating system can clean the temporary directory; do not add it to the repository.

- [ ] **Step 4: Create the token stylesheet**

```css
/* assets/css/extended/portfolio-tokens.css */
@font-face {
  font-family: "Instrument Sans";
  src: url("/fonts/instrument-sans-latin-wght-normal.woff2") format("woff2");
  font-style: normal;
  font-weight: 400 700;
  font-display: swap;
}

@font-face {
  font-family: "IBM Plex Mono";
  src: url("/fonts/ibm-plex-mono-latin-400-normal.woff2") format("woff2");
  font-style: normal;
  font-weight: 400;
  font-display: swap;
}

@font-face {
  font-family: "IBM Plex Mono";
  src: url("/fonts/ibm-plex-mono-latin-500-normal.woff2") format("woff2");
  font-style: normal;
  font-weight: 500;
  font-display: swap;
}

:root {
  --portfolio-paper: #f5f7f4;
  --portfolio-surface: #ffffff;
  --portfolio-surface-soft: #edf2f8;
  --portfolio-ink: #0d1726;
  --portfolio-ink-soft: #526071;
  --portfolio-line: #d7dee7;
  --portfolio-line-strong: #b8c3d1;
  --portfolio-blue: #245bdc;
  --portfolio-blue-dark: #1643ad;
  --portfolio-blue-soft: #e7eeff;
  --portfolio-cyan: #0d8d9d;
  --portfolio-green: #177a55;
  --portfolio-shadow: 0 18px 60px rgba(21, 45, 80, 0.09);
  --portfolio-max: 1180px;
  --portfolio-radius-sm: 8px;
  --portfolio-radius-md: 14px;
  --portfolio-radius-lg: 22px;
  --theme: var(--portfolio-paper);
  --entry: var(--portfolio-surface);
  --primary: var(--portfolio-ink);
  --secondary: var(--portfolio-ink-soft);
  --tertiary: var(--portfolio-surface-soft);
  --content: var(--portfolio-ink);
  --border: var(--portfolio-line);
  --main-width: var(--portfolio-max);
}

:root[data-theme="dark"] {
  --portfolio-paper: #08111c;
  --portfolio-surface: #101b29;
  --portfolio-surface-soft: #152235;
  --portfolio-ink: #ecf2f9;
  --portfolio-ink-soft: #a8b5c5;
  --portfolio-line: #26364a;
  --portfolio-line-strong: #3e526c;
  --portfolio-blue: #78a2ff;
  --portfolio-blue-dark: #9dbbff;
  --portfolio-blue-soft: #152b55;
  --portfolio-cyan: #4cc0cc;
  --portfolio-green: #62cf9f;
  --portfolio-shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
  color-scheme: dark;
}
```

- [ ] **Step 5: Create shared base rules**

```css
/* assets/css/extended/portfolio-base.css */
html { scroll-behavior: smooth; }

body {
  color: var(--portfolio-ink);
  background: var(--portfolio-paper);
  font-family: "Instrument Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 17px;
  line-height: 1.58;
}

h1, h2, h3, h4, h5, h6 {
  color: var(--portfolio-ink);
  font-family: "Instrument Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  letter-spacing: -0.025em;
}

:focus-visible {
  outline: 3px solid var(--portfolio-cyan);
  outline-offset: 4px;
}

.main {
  max-width: calc(var(--portfolio-max) + 40px);
  padding-inline: 20px;
}

.portfolio-label {
  margin: 0;
  color: var(--portfolio-blue);
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    scroll-behavior: auto !important;
    transition: none !important;
  }
}

@media (max-width: 640px) {
  .main { padding-inline: 14px; }
}
```

- [ ] **Step 6: Remove remote Inter and preload local fonts**

Replace `layouts/partials/extend_head.html:1-3` with:

```html
<link rel="preload" href="/fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ibm-plex-mono-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
```

Leave the existing conditional KaTeX and analytics blocks unchanged.

- [ ] **Step 7: Remove the obsolete global Inter and `.dark` rules**

Delete `assets/css/extended/custom.css:1-31`. Do not edit its homepage, blog, or project rules yet.

- [ ] **Step 8: Run the tests**

Run: `python3 -m unittest tests.test_design_assets tests.test_baseline -v`
Expected: `Ran 6 tests` and `OK`.

- [ ] **Step 9: Commit the design foundation**

```bash
git add static/fonts assets/css/extended/portfolio-tokens.css assets/css/extended/portfolio-base.css layouts/partials/extend_head.html assets/css/extended/custom.css tests/test_design_assets.py
git commit -m "feat: add portfolio design tokens and local fonts"
```

---

### Task 3: Build the Header and Experience-First Hero

**Files:**
- Create: `data/profile.yaml`
- Create: `data/experience.yaml`
- Create: `tests/test_homepage_contract.py`
- Create: `layouts/_default/baseof.html`
- Create: `layouts/partials/header.html`
- Create: `layouts/partials/home/hero.html`
- Create: `assets/css/extended/portfolio-home.css`
- Replace: `layouts/index.html`
- Modify: `hugo.yaml:67-88`

- [ ] **Step 1: Write the failing hero and navigation contract**

```python
# tests/test_homepage_contract.py
from tests.site_harness import HugoSiteTestCase


class HomepageContractTests(HugoSiteTestCase):
    def test_header_prioritizes_experience_and_work(self) -> None:
        html = self.page_html("/")
        for label in ("Experience", "Expertise", "Selected Work", "Writing", "Contact"):
            self.assertIn(f">{label}<", html)
        for forbidden in (">Resume<", ">Books<", ">Search<"):
            self.assertNotIn(forbidden, html)
        self.assertIn('href="#main-content"', html)
        self.assertIn('<main id="main-content"', html)

    def test_hero_leads_with_ai_ml_and_not_a_project(self) -> None:
        html = self.page_html("/")
        hero = html.split('id="portfolio-hero"', 1)[1].split("</section>", 1)[0]
        self.assertIn("Applied AI &amp; ML Engineer", hero)
        self.assertIn("<h1", hero)
        self.assertIn("LLM systems, RAG &amp; evaluation", hero)
        self.assertIn("Predictive ML &amp; human review", hero)
        self.assertNotIn("4+ years", hero)
        self.assertNotIn("Python &amp; SQL", hero)
        self.assertNotIn("Maintenance-Eye", hero)

    def test_hero_contains_canonical_career_signal(self) -> None:
        html = self.page_html("/")
        hero = html.split('id="portfolio-hero"', 1)[1].split("</section>", 1)[0]
        for text in (
            "Data &amp; Applied AI Analyst",
            "Data Scientist, Applied AI",
            "Master of Data Science",
            "Co-Founder / Data Scientist",
        ):
            self.assertIn(text, hero)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests.test_homepage_contract -v`
Expected: FAIL because the old navigation and project-first hero are still rendered.

- [ ] **Step 3: Create profile data**

```yaml
# data/profile.yaml
name: "Avishek Saha"
monogram: "AS"
role: "Applied AI & ML Engineer"
location: "Vancouver, BC"
work_authorized_label: "Canada work authorized"
hero:
  statement: "Building AI products and ML systems with measurable impact."
  supporting: "My experience spans source-grounded LLM workflows, predictive models, evaluation systems, data and feature pipelines, APIs, and cloud delivery, with measured improvements in quality, efficiency, review effort, and decision support."
  signals:
    - "LLM systems, RAG & evaluation"
    - "Predictive ML & human review"
    - "Measured quality & efficiency gains"
actions:
  - label: "Explore experience"
    url: "/experience/"
    primary: true
  - label: "Selected work"
    url: "/#work"
    primary: false
  - label: "Contact"
    url: "/#contact"
    primary: false
social:
  github: "https://github.com/sahaavi"
  linkedin: "https://linkedin.com/in/sahaavi"
  email: "mailto:avisheksaha123@gmail.com"
education:
  - institution: "University of British Columbia"
    degree: "Master of Data Science"
    period: "Sep 2022 to Jun 2023"
    short_period: "2022 · 2023"
    hero_signal: true
    hero_order: 3
  - institution: "American International University-Bangladesh"
    degree: "BSc Computer Science & Engineering"
    period: "Jan 2018 to Sep 2021"
    detail: "CGPA 3.91/4.00"
```

- [ ] **Step 4: Create canonical experience data**

```yaml
# data/experience.yaml
roles:
  - id: "bcrtc"
    employer: "BC Rapid Transit Company"
    title: "Data & Applied AI Analyst"
    period: "Dec 2024 to present"
    short_period: "2024 · Present"
    location: "Burnaby, BC"
    current: true
    hero_signal: true
    hero_order: 1
    homepage_summary: "Build applied AI evaluation and human-review controls, predictive ML, and reusable data and feature foundations for enterprise decision support."
    source_claim_ids:
      - "stan-bcrtc-ragas-semantic-eval-20260709"
      - "aviva-bcrtc-p15-recovery-duration-001"
      - "seed-p11-event-feature-foundation"
    evidence:
      - label: "AI quality"
        text: "Built a 150-case evaluation harness using RAGAS, semantic similarity, LLM-as-judge rubrics, trace capture, and latency and cost checks."
      - label: "ML impact"
        text: "Built an uncertainty-aware recovery-duration model that improved planning accuracy by 21% through calibration and interval-coverage checks."
      - label: "Trust"
        text: "Reduced unsupported AI-generated summary claims by 60% while keeping human review and release boundaries explicit."
    details:
      - "Built a 150-case AI evaluation harness with RAGAS, semantic-similarity and LLM-as-judge scoring, inspectable traces, and latency and cost gates, reducing unsupported summary claims by 60%."
      - "Owned label definition, contextual feature engineering, model comparison, calibration checks, and uncertainty-aware output design for an internally used predictive model that improved planning accuracy by 21%."
      - "Designed a reusable event and feature foundation with canonical entities, feature contracts, data-quality tests, lineage tracking, and read-only downstream consumption patterns."
  - id: "brainstation23"
    employer: "Brain Station 23"
    title: "Data Scientist, Applied AI"
    period: "Aug 2023 to Nov 2024"
    short_period: "2023 · 2024"
    location: "Dhaka, Bangladesh / Remote"
    current: false
    hero_signal: true
    hero_order: 2
    homepage_summary: "Financial analytics, predictive ML prototypes, document intelligence, production-service contributions, data pipelines, and cloud integrations."
    source_claim_ids:
      - "stage-bs23-ai-002"
      - "stage-bs23-analytics-001"
    metrics:
      - value: "21%"
        label: "analysis efficiency"
      - value: "17%"
        label: "data consistency"
      - value: "26%"
        label: "query performance"
    details:
      - "Contributed to production Python services and Dockerized integrations supporting financial analytics and data delivery."
      - "Built predictive ML prototypes with feature engineering, validation, scikit-learn, TensorFlow, and XGBoost."
      - "Contributed to document-intelligence and data workflows using Vertex AI, Cloud Functions, BigQuery, Python, SQL, and Power BI."
  - id: "statscan"
    employer: "UBC MDS × Statistics Canada"
    title: "Capstone Data Scientist"
    period: "Apr 2023 to Jul 2023"
    short_period: "2023"
    location: "Ottawa, ON"
    current: false
    hero_signal: false
    homepage_summary: "Interpretable clustering, data profiling, outlier analysis, comparative evaluation, and policy-facing communication through the UBC MDS capstone."
    details:
      - "Implemented K-means and hierarchical clustering after data profiling and outlier analysis in R."
      - "Produced cluster profiles and policy-facing findings for the Proximity Measure Database."
  - id: "softology"
    employer: "Softology IT"
    title: "Co-Founder / Data Scientist"
    period: "Sep 2021 to Aug 2022"
    short_period: "2021 · 2022"
    location: "Dhaka, Bangladesh"
    current: false
    hero_signal: true
    hero_order: 4
    homepage_summary: "Client-facing software delivery across applications, APIs, analytics, data workflows, project ownership, and technical handoff."
    details:
      - "Co-founded a software firm and delivered client applications, APIs, analytics, and data workflows."
      - "Managed project scope, implementation, client communication, and technical handoff across concurrent engagements."
```

- [ ] **Step 5: Replace the menu configuration**

Replace `hugo.yaml:67-88` with:

```yaml
menu:
  main:
    - identifier: experience
      name: Experience
      url: /experience/
      weight: 10
    - identifier: expertise
      name: Expertise
      url: /#expertise
      weight: 20
    - identifier: work
      name: Selected Work
      url: /#work
      weight: 30
    - identifier: writing
      name: Writing
      url: /posts/
      weight: 40
    - identifier: contact
      name: Contact
      url: /#contact
      weight: 50
```

- [ ] **Step 6: Create the PaperMod-compatible header override**

First create the local base shell. This is the theme's existing shell with only `id="main-content"` and `tabindex="-1"` added to `<main>`:

```html
{{- if lt hugo.Version "0.146.0" }}
{{- errorf "Hugo 0.146.0 or greater is required" }}
{{- end -}}
<!DOCTYPE html>
{{- $theme := site.Params.defaultTheme | default "auto" -}}
{{- if eq $theme "dark" }}
<html lang="{{ site.Language }}" dir="{{ .Language.LanguageDirection | default "auto" }}" data-theme="dark">
{{- else if eq $theme "light" }}
<html lang="{{ site.Language }}" dir="{{ .Language.LanguageDirection | default "auto" }}" data-theme="light">
{{- else }}
<html lang="{{ site.Language }}" dir="{{ .Language.LanguageDirection | default "auto" }}" data-theme="auto">
{{- end }}
<head>{{- partial "head.html" . -}}</head>
{{- if or (ne .Kind "page") (eq .Layout "archives") (eq .Layout "search") }}
<body class="list" id="top">
{{- else }}
<body id="top">
{{- end }}
  {{- partialCached "header.html" . .Page }}
  <main id="main-content" class="main" tabindex="-1">
    {{- block "main" . }}{{ end }}
  </main>
  {{- partialCached "footer.html" . .Layout .Kind (.Param "hideFooter") (.Param "ShowCodeCopyButtons") }}
</body>
</html>
```

Then create the header override:

```html
{{/* layouts/partials/header.html */}}
<a class="portfolio-skip-link" href="#main-content">Skip to content</a>
<header class="portfolio-header">
  <nav class="portfolio-nav" aria-label="Primary navigation">
    <a class="portfolio-brand" href="{{ site.Home.RelPermalink }}" aria-label="{{ site.Data.profile.name }} home">
      <span class="portfolio-monogram" aria-hidden="true">{{ site.Data.profile.monogram }}</span>
      <span>{{ site.Data.profile.name }}</span>
      <span class="portfolio-brand-role">{{ site.Data.profile.role }}</span>
    </a>
    <div class="portfolio-nav-actions">
      <ul id="menu" class="portfolio-menu">
        {{- range site.Menus.main }}
        <li><a href="{{ .URL | absLangURL }}">{{ .Name }}</a></li>
        {{- end }}
      </ul>
      {{- if not site.Params.disableThemeToggle }}
      <button id="theme-toggle" class="portfolio-theme-toggle" type="button" aria-label="Toggle color theme" aria-pressed="false" title="Toggle color theme">
        <svg id="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="none" stroke="currentColor" stroke-width="2"/></svg>
        <svg id="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72 1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" fill="none" stroke="currentColor" stroke-width="2"/></svg>
      </button>
      {{- end }}
    </div>
  </nav>
</header>
```

- [ ] **Step 7: Create the hero partial with fail-fast data checks**

```html
{{/* layouts/partials/home/hero.html */}}
{{- $profile := site.Data.profile -}}
{{- $roles := site.Data.experience.roles -}}
{{- $careerSignals := slice -}}
{{- range where $roles "hero_signal" true -}}
  {{- $careerSignals = $careerSignals | append (dict "order" .hero_order "period" .short_period "title" .title "organization" .employer "location" .location) -}}
{{- end -}}
{{- range where $profile.education "hero_signal" true -}}
  {{- $careerSignals = $careerSignals | append (dict "order" .hero_order "period" .short_period "title" .degree "organization" .institution) -}}
{{- end -}}
{{- if not $profile.name }}{{ errorf "data/profile.yaml must define name" }}{{ end -}}
{{- if ne (len $profile.hero.signals) 3 }}{{ errorf "profile.hero.signals must contain exactly three items" }}{{ end -}}
{{- if lt (len $roles) 4 }}{{ errorf "data/experience.yaml must define at least four roles" }}{{ end -}}
{{- if ne (len $careerSignals) 4 }}{{ errorf "homepage career panel requires exactly four hero signals" }}{{ end -}}

<section id="portfolio-hero" class="portfolio-hero" aria-labelledby="portfolio-hero-title">
  <div class="portfolio-hero-grid">
    <div class="portfolio-hero-copy">
      <p class="portfolio-label">{{ $profile.role }} · {{ $profile.location }}</p>
      <h1 id="portfolio-hero-title">{{ $profile.hero.statement }}</h1>
      <p class="portfolio-hero-lead">{{ $profile.hero.supporting }}</p>
      <div class="portfolio-hero-actions" aria-label="Primary actions">
        {{- range $profile.actions }}
        <a class="portfolio-button{{ if .primary }} portfolio-button-primary{{ end }}" href="{{ .url }}">{{ .label }}</a>
        {{- end }}
      </div>
      <ul class="portfolio-signal-list" aria-label="AI and machine learning evidence">
        {{- range $profile.hero.signals }}<li>{{ . }}</li>{{ end }}
      </ul>
    </div>
    <aside class="portfolio-career-panel" aria-label="Career timeline">
      <div class="portfolio-panel-heading">
        <strong>Experience at a glance</strong>
        <span class="portfolio-availability">{{ $profile.work_authorized_label }}</span>
      </div>
      <ol class="portfolio-career-list">
        {{- range sort $careerSignals "order" "asc" }}
        <li>
          <span class="portfolio-career-period">{{ .period }}</span>
          <strong>{{ .title }}</strong>
          <span>{{ .organization }}{{ with .location }} · {{ . }}{{ end }}</span>
        </li>
        {{- end }}
      </ol>
    </aside>
  </div>
</section>
```

- [ ] **Step 8: Replace the homepage with the first vertical slice**

```html
{{/* layouts/index.html */}}
{{- define "main" }}
<div class="portfolio-home">
  {{- partial "home/hero.html" . }}
</div>
{{- end }}
```

- [ ] **Step 9: Add the hero and header CSS**

Create `assets/css/extended/portfolio-home.css` with the approved preview's header/hero rules, using only `.portfolio-*` selectors. The required structural declarations are:

```css
.portfolio-header {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--portfolio-line);
  background: color-mix(in srgb, var(--portfolio-paper) 88%, transparent);
  backdrop-filter: blur(18px);
}

.portfolio-skip-link {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 100;
  padding: 10px 14px;
  color: var(--portfolio-surface);
  background: var(--portfolio-ink);
  transform: translateY(-160%);
}

.portfolio-skip-link:focus { transform: translateY(0); }

.portfolio-nav {
  width: min(calc(100% - 40px), var(--portfolio-max));
  min-height: 74px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
}

.portfolio-brand,
.portfolio-nav-actions,
.portfolio-menu,
.portfolio-hero-actions,
.portfolio-panel-heading {
  display: flex;
  align-items: center;
}

.portfolio-brand { gap: 12px; color: var(--portfolio-ink); text-decoration: none; font-weight: 700; }
.portfolio-monogram { width: 34px; height: 34px; display: grid; place-items: center; border: 1px solid var(--portfolio-line-strong); border-radius: 50%; color: var(--portfolio-blue); font: 500 12px "IBM Plex Mono", monospace; background: var(--portfolio-surface); }
.portfolio-brand-role { color: var(--portfolio-ink-soft); font: 400 10px "IBM Plex Mono", monospace; letter-spacing: .06em; text-transform: uppercase; }
.portfolio-nav-actions { gap: 20px; }
.portfolio-menu { gap: 24px; margin: 0; padding: 0; list-style: none; }
.portfolio-menu a { min-height: 44px; display: inline-flex; align-items: center; color: var(--portfolio-ink-soft); text-decoration: none; font-size: 14px; font-weight: 600; }
.portfolio-menu a:hover { color: var(--portfolio-blue); }
.portfolio-theme-toggle { width: 44px; height: 44px; display: grid; place-items: center; border: 1px solid var(--portfolio-line); border-radius: 50%; color: var(--portfolio-ink); background: var(--portfolio-surface); }
.portfolio-theme-toggle svg { width: 18px; height: 18px; }

.portfolio-home { width: 100%; }
.portfolio-hero { padding: 100px 0 80px; border-bottom: 1px solid var(--portfolio-line); }
.portfolio-hero-grid { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(330px, .65fr); gap: clamp(48px, 8vw, 108px); align-items: center; }
.portfolio-hero h1 { max-width: 760px; margin: 20px 0 24px; font-size: clamp(49px, 7vw, 84px); font-weight: 650; letter-spacing: -.058em; line-height: .98; }
.portfolio-hero-lead { max-width: 710px; margin: 0; color: var(--portfolio-ink-soft); font-size: clamp(18px, 2.1vw, 22px); line-height: 1.5; }
.portfolio-hero-actions { flex-wrap: wrap; gap: 12px; margin-top: 34px; }
.portfolio-button { min-height: 48px; display: inline-flex; align-items: center; justify-content: center; padding: 0 20px; border: 1px solid var(--portfolio-line-strong); border-radius: var(--portfolio-radius-sm); color: var(--portfolio-ink); background: var(--portfolio-surface); text-decoration: none; font-size: 14px; font-weight: 650; }
.portfolio-button-primary { color: #fff; background: var(--portfolio-blue-dark); border-color: var(--portfolio-blue-dark); }
.portfolio-signal-list { display: flex; flex-wrap: wrap; gap: 10px 22px; margin: 38px 0 0; padding: 22px 0 0; border-top: 1px solid var(--portfolio-line); color: var(--portfolio-ink-soft); font: 400 12px "IBM Plex Mono", monospace; list-style: none; }
.portfolio-signal-list li::before { content: ""; width: 6px; height: 6px; display: inline-block; margin-right: 8px; border-radius: 50%; background: var(--portfolio-cyan); vertical-align: 1px; }
.portfolio-career-panel { padding: 28px; border: 1px solid var(--portfolio-line-strong); border-radius: var(--portfolio-radius-lg); background: var(--portfolio-surface); box-shadow: var(--portfolio-shadow); }
.portfolio-panel-heading { justify-content: space-between; gap: 16px; margin-bottom: 24px; }
.portfolio-availability { color: var(--portfolio-green); font: 500 10px "IBM Plex Mono", monospace; text-transform: uppercase; }
.portfolio-career-list { margin: 0; padding: 0; list-style: none; }
.portfolio-career-list li { position: relative; padding: 0 0 24px 26px; border-left: 1px solid var(--portfolio-line-strong); }
.portfolio-career-list li::before { content: ""; position: absolute; left: -5px; top: 7px; width: 9px; height: 9px; border: 2px solid var(--portfolio-blue); border-radius: 50%; background: var(--portfolio-surface); }
.portfolio-career-list strong, .portfolio-career-list span { display: block; }
.portfolio-career-period { color: var(--portfolio-ink-soft); font: 400 10px "IBM Plex Mono", monospace; text-transform: uppercase; }

@media (max-width: 920px) {
  .portfolio-hero-grid { grid-template-columns: 1fr; }
  .portfolio-career-panel { max-width: 620px; }
}

@media (max-width: 640px) {
  .portfolio-nav { width: calc(100% - 28px); min-height: 66px; }
  .portfolio-brand-role, .portfolio-menu { display: none; }
  .portfolio-hero { padding: 62px 0 58px; }
  .portfolio-hero h1 { font-size: clamp(43px, 14.5vw, 64px); }
  .portfolio-hero-actions { display: grid; grid-template-columns: 1fr 1fr; }
  .portfolio-hero-actions a:last-child { grid-column: 1; }
  .portfolio-signal-list { display: grid; grid-template-columns: 1fr; gap: 8px; }
}
```

- [ ] **Step 10: Run the hero contract**

Run: `python3 -m unittest tests.test_homepage_contract tests.test_design_assets tests.test_baseline -v`
Expected: `Ran 9 tests` and `OK`.

- [ ] **Step 11: Commit the hero slice**

```bash
git add data/profile.yaml data/experience.yaml hugo.yaml layouts/_default/baseof.html layouts/index.html layouts/partials/header.html layouts/partials/home/hero.html assets/css/extended/portfolio-home.css tests/test_homepage_contract.py
git commit -m "feat: add experience-first portfolio hero"
```

---

### Task 4: Add the Professional Experience Section

**Files:**
- Create: `layouts/partials/home/experience.html`
- Modify: `layouts/index.html`
- Modify: `assets/css/extended/portfolio-home.css`
- Modify: `tests/test_homepage_contract.py`

- [ ] **Step 1: Add failing experience assertions**

Add these methods to `HomepageContractTests`:

```python
    def test_professional_experience_precedes_selected_work(self) -> None:
        html = self.page_html("/")
        self.assertIn('id="experience"', html)
        self.assertLess(html.index('id="experience"'), html.index("</main>"))

    def test_experience_uses_canonical_titles_and_scoped_metrics(self) -> None:
        html = self.page_html("/")
        for text in (
            "Data &amp; Applied AI Analyst",
            "Data Scientist, Applied AI",
            "Capstone Data Scientist",
            "Co-Founder / Data Scientist",
            "21%",
            "17%",
            "26%",
        ):
            self.assertIn(text, html)
        self.assertNotIn("Data Scientist, Financial Analytics &amp; AI Workflows", html)

    def test_current_role_foregrounds_ai_evaluation_and_predictive_ml(self) -> None:
        html = self.page_html("/")
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
```

- [ ] **Step 2: Run the assertions to verify failure**

Run: `python3 -m unittest tests.test_homepage_contract.HomepageContractTests.test_professional_experience_precedes_selected_work tests.test_homepage_contract.HomepageContractTests.test_experience_uses_canonical_titles_and_scoped_metrics -v`
Expected: FAIL because no experience section is rendered.

- [ ] **Step 3: Create the experience partial**

```html
{{/* layouts/partials/home/experience.html */}}
{{- $roles := site.Data.experience.roles -}}
{{- $current := index (where $roles "current" true) 0 -}}
{{- $previous := where $roles "current" false -}}
<section id="experience" class="portfolio-section" aria-labelledby="experience-title">
  <div class="portfolio-section-head">
    <p class="portfolio-label">01 · Experience</p>
    <div>
      <h2 id="experience-title">AI and ML engineering grounded in professional delivery.</h2>
      <p>Applied AI evaluation, predictive ML, software and data delivery, financial technology, and public-sector research provide the professional foundation for the engineering work.</p>
    </div>
  </div>
  <article class="portfolio-experience-primary">
    <div>
      <p class="portfolio-label">Current role</p>
      <h3>{{ $current.title }}</h3>
      <p class="portfolio-meta">{{ $current.employer }} · {{ $current.period }} · {{ $current.location }}</p>
      <p>{{ $current.homepage_summary }}</p>
    </div>
    <ul class="portfolio-evidence-list">
      {{- range $current.evidence }}
      <li><strong>{{ .label }}</strong><span>{{ .text }}</span></li>
      {{- end }}
    </ul>
  </article>
  <div class="portfolio-experience-grid">
    {{- range $previous }}
    <article class="portfolio-experience-card">
      <p class="portfolio-label">{{ .short_period }}</p>
      <h3>{{ .employer }}</h3>
      <p class="portfolio-meta">{{ .title }}</p>
      <p>{{ .homepage_summary }}</p>
      {{- with .metrics }}
      <dl class="portfolio-metric-row">
        {{- range . }}<div><dt>{{ .value }}</dt><dd>{{ .label }}</dd></div>{{ end }}
      </dl>
      {{- end }}
    </article>
    {{- end }}
  </div>
</section>
```

- [ ] **Step 4: Insert the partial after the hero**

```html
{{- partial "home/hero.html" . }}
{{- partial "home/experience.html" . }}
```

- [ ] **Step 5: Add scoped experience styles**

Append the approved `.portfolio-section`, `.portfolio-section-head`, `.portfolio-experience-primary`, `.portfolio-evidence-list`, `.portfolio-experience-grid`, `.portfolio-experience-card`, and `.portfolio-metric-row` rules from the preview. Required grid behavior:

```css
.portfolio-section { padding: 104px 0; border-bottom: 1px solid var(--portfolio-line); }
.portfolio-section-head { display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 34px; margin-bottom: 52px; }
.portfolio-section-head h2 { max-width: 790px; margin: -8px 0 0; font-size: clamp(34px, 5vw, 56px); line-height: 1.05; letter-spacing: -.045em; }
.portfolio-section-head p:not(.portfolio-label) { max-width: 720px; color: var(--portfolio-ink-soft); font-size: 18px; }
.portfolio-experience-primary { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(280px, .9fr); gap: 48px; padding: clamp(28px, 5vw, 48px); border: 1px solid var(--portfolio-line-strong); border-radius: var(--portfolio-radius-lg); background: var(--portfolio-surface); box-shadow: var(--portfolio-shadow); }
.portfolio-experience-primary h3 { margin: 12px 0 6px; font-size: clamp(27px, 4vw, 40px); }
.portfolio-meta { color: var(--portfolio-ink-soft); font: 400 12px "IBM Plex Mono", monospace; }
.portfolio-evidence-list { margin: 0; padding: 0; border-top: 1px solid var(--portfolio-line); list-style: none; }
.portfolio-evidence-list li { display: grid; grid-template-columns: 92px 1fr; gap: 18px; padding: 18px 0; border-bottom: 1px solid var(--portfolio-line); }
.portfolio-evidence-list strong { color: var(--portfolio-blue); font: 500 12px "IBM Plex Mono", monospace; }
.portfolio-experience-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 18px; }
.portfolio-experience-card { padding: 26px; border: 1px solid var(--portfolio-line); border-radius: var(--portfolio-radius-md); background: var(--portfolio-surface); }
.portfolio-metric-row { display: grid; grid-template-columns: repeat(3, 1fr); margin: 20px 0 0; padding-top: 16px; border-top: 1px solid var(--portfolio-line); }
.portfolio-metric-row dt { font-size: 23px; font-weight: 650; }
.portfolio-metric-row dd { margin: 0; color: var(--portfolio-ink-soft); font: 400 9px "IBM Plex Mono", monospace; text-transform: uppercase; }

@media (max-width: 920px) {
  .portfolio-experience-primary { grid-template-columns: 1fr; }
  .portfolio-experience-grid { grid-template-columns: 1fr 1fr; }
  .portfolio-experience-card:last-child { grid-column: 1 / -1; }
}

@media (max-width: 640px) {
  .portfolio-section { padding: 74px 0; }
  .portfolio-section-head { grid-template-columns: 1fr; gap: 20px; margin-bottom: 36px; }
  .portfolio-experience-grid { grid-template-columns: 1fr; }
  .portfolio-experience-card:last-child { grid-column: auto; }
}
```

- [ ] **Step 6: Run the homepage contract**

Run: `python3 -m unittest tests.test_homepage_contract -v`
Expected: all six homepage tests pass.

- [ ] **Step 7: Commit**

```bash
git add layouts/index.html layouts/partials/home/experience.html assets/css/extended/portfolio-home.css tests/test_homepage_contract.py
git commit -m "feat: foreground professional experience"
```

---

### Task 5: Add AI/ML Engineering Range and Lifecycle

**Files:**
- Create: `data/expertise.yaml`
- Create: `layouts/partials/home/expertise.html`
- Modify: `layouts/index.html`
- Modify: `assets/css/extended/portfolio-home.css`
- Modify: `tests/test_homepage_contract.py`

- [ ] **Step 1: Add the failing expertise contract**

```python
    def test_expertise_covers_ai_ml_software_and_delivery(self) -> None:
        html = self.page_html("/")
        for text in (
            "Applied AI systems",
            "Machine learning",
            "Software &amp; data",
            "Delivery &amp; trust",
            "Data foundation",
            "Model or retrieval",
            "Evaluation",
            "Software integration",
            "Delivery loop",
        ):
            self.assertIn(text, html)
```

- [ ] **Step 2: Verify failure**

Run: `python3 -m unittest tests.test_homepage_contract.HomepageContractTests.test_expertise_covers_ai_ml_software_and_delivery -v`
Expected: FAIL because `#expertise` is not rendered.

- [ ] **Step 3: Create expertise data**

```yaml
# data/expertise.yaml
groups:
  - code: "01 / AI"
    title: "Applied AI systems"
    summary: "LLM integration, RAG, agent and tool workflows, structured outputs, prompting, source grounding, human review, and evaluation."
  - code: "02 / ML"
    title: "Machine learning"
    summary: "Feature engineering, anomaly detection, ranking, calibration, temporal modeling, clustering, NLP, and reviewer feedback."
  - code: "03 / SWE"
    title: "Software & data"
    summary: "Python, FastAPI, REST and WebSocket APIs, SQL, PostgreSQL, BigQuery, pipelines, data contracts, and user-facing integration."
  - code: "04 / QUALITY"
    title: "Delivery & trust"
    summary: "MLOps practices, Docker, cloud deployment, CI, automated tests, observability, validation, approval boundaries, and technical documentation."
lifecycle:
  - title: "Data foundation"
    detail: "sources, contracts, features"
  - title: "Model or retrieval"
    detail: "ranking, RAG, prediction"
  - title: "Evaluation"
    detail: "quality, failure analysis"
  - title: "Software integration"
    detail: "APIs, tools, interfaces"
  - title: "Delivery loop"
    detail: "tests, monitoring, review"
```

- [ ] **Step 4: Create the expertise partial**

```html
{{/* layouts/partials/home/expertise.html */}}
{{- $expertise := site.Data.expertise -}}
{{- if ne (len $expertise.groups) 4 }}{{ errorf "expertise.groups must contain four groups" }}{{ end -}}
{{- if ne (len $expertise.lifecycle) 5 }}{{ errorf "expertise.lifecycle must contain five stages" }}{{ end -}}
<section id="expertise" class="portfolio-section" aria-labelledby="expertise-title">
  <div class="portfolio-section-head">
    <p class="portfolio-label">02 · Engineering range</p>
    <div>
      <h2 id="expertise-title">More than models. The surrounding system matters.</h2>
      <p>The profile spans AI behavior, machine learning, software interfaces, data foundations, and delivery quality.</p>
    </div>
  </div>
  <div class="portfolio-capability-rail">
    {{- range $expertise.groups }}
    <article>
      <span class="portfolio-capability-code">{{ .code }}</span>
      <h3>{{ .title }}</h3>
      <p>{{ .summary }}</p>
    </article>
    {{- end }}
  </div>
  <ol class="portfolio-lifecycle">
    {{- range $expertise.lifecycle }}
    <li><strong>{{ .title }}</strong><span>{{ .detail }}</span></li>
    {{- end }}
  </ol>
</section>
```

- [ ] **Step 5: Insert the partial and add styles**

Insert after experience:

```html
{{- partial "home/expertise.html" . }}
```

Append:

```css
.portfolio-capability-rail { display: grid; grid-template-columns: repeat(4, 1fr); border-block: 1px solid var(--portfolio-line-strong); }
.portfolio-capability-rail article { min-height: 250px; padding: 30px 26px; }
.portfolio-capability-rail article:not(:last-child) { border-right: 1px solid var(--portfolio-line); }
.portfolio-capability-code { color: var(--portfolio-blue); font: 400 11px "IBM Plex Mono", monospace; }
.portfolio-capability-rail h3 { margin: 38px 0 16px; font-size: 21px; }
.portfolio-capability-rail p { margin: 0; color: var(--portfolio-ink-soft); font-size: 14px; }
.portfolio-lifecycle { display: grid; grid-template-columns: repeat(5, 1fr); margin: 62px 0 0; padding: 0; list-style: none; counter-reset: lifecycle; }
.portfolio-lifecycle li { position: relative; padding: 38px 18px 0 0; border-top: 2px solid var(--portfolio-line-strong); counter-increment: lifecycle; }
.portfolio-lifecycle li::before { content: counter(lifecycle, decimal-leading-zero); position: absolute; top: -14px; left: 0; padding-right: 10px; color: var(--portfolio-blue); background: var(--portfolio-paper); font: 400 11px "IBM Plex Mono", monospace; }
.portfolio-lifecycle strong, .portfolio-lifecycle span { display: block; }
.portfolio-lifecycle span { color: var(--portfolio-ink-soft); font-size: 12px; }

@media (max-width: 920px) {
  .portfolio-capability-rail { grid-template-columns: 1fr 1fr; }
  .portfolio-lifecycle { grid-template-columns: 1fr; gap: 22px; }
}

@media (max-width: 640px) {
  .portfolio-capability-rail { grid-template-columns: 1fr; }
  .portfolio-capability-rail article { min-height: 0; padding: 26px 0; border-right: 0 !important; border-bottom: 1px solid var(--portfolio-line); }
}
```

- [ ] **Step 6: Run tests and commit**

Run: `python3 -m unittest tests.test_homepage_contract -v`
Expected: all homepage tests pass.

```bash
git add data/expertise.yaml layouts/index.html layouts/partials/home/expertise.html assets/css/extended/portfolio-home.css tests/test_homepage_contract.py
git commit -m "feat: show AI ML engineering range"
```

---

### Task 6: Add Two Equally Weighted Public Systems

**Files:**
- Create: `layouts/partials/home/selected-work.html`
- Modify: `content/projects/vision-maintenance-agent/index.md`
- Modify: `content/projects/govtintel/index.md`
- Modify: `layouts/index.html`
- Modify: `assets/css/extended/portfolio-home.css`
- Modify: `tests/test_homepage_contract.py`

- [ ] **Step 1: Add failing selected-work assertions**

```python
    def test_selected_work_contains_exactly_two_equal_public_systems(self) -> None:
        html = self.page_html("/")
        work = html.split('id="work"', 1)[1].split("</section>", 1)[0]
        self.assertLess(html.index('id="experience"'), html.index('id="work"'))
        self.assertEqual(work.count('class="portfolio-work-row"'), 2)
        self.assertEqual(work.count(">Maintenance-Eye<"), 1)
        self.assertEqual(work.count(">GovIntel<"), 1)

    def test_maintenance_eye_copy_matches_public_code(self) -> None:
        html = self.page_html("/")
        work = html.split('id="work"', 1)[1].split("</section>", 1)[0]
        self.assertIn("nine guarded tool workflows", work)
        self.assertIn("human approval", work)
        self.assertNotIn("multi-agent", work.lower())
        self.assertNotIn("66 assets", work)
        self.assertNotIn("150 work orders", work)
```

- [ ] **Step 2: Verify failure**

Run: `python3 -m unittest tests.test_homepage_contract.HomepageContractTests.test_selected_work_contains_exactly_two_equal_public_systems tests.test_homepage_contract.HomepageContractTests.test_maintenance_eye_copy_matches_public_code -v`
Expected: FAIL because `#work` is not rendered.

- [ ] **Step 3: Add exact featured metadata to Maintenance-Eye**

Add to its front matter:

```yaml
home_featured: true
home_order: 1
portfolio_group: "featured-ai"
portfolio_status: "Public demo"
portfolio_category: "Applied AI"
portfolio_role: "Builder"
portfolio_year: 2026
repository_url: "https://github.com/sahaavi/Maintenance-Eye"
case_study_url: "/projects/maintenance-eye/"
home_summary: "Multimodal maintenance copilot with live camera and voice input, nine guarded tool workflows, a FastAPI and WebSocket backend, human approval, cloud packaging, and automated tests."
system_map:
  - label: "Camera + voice"
  - label: "Gemini Live"
    accent: true
  - label: "User response"
  - label: "FastAPI"
  - label: "9 guarded tools"
    accent: true
  - label: "Approval gate"
```

- [ ] **Step 4: Add exact featured metadata to GovIntel**

```yaml
home_featured: true
home_order: 2
portfolio_group: "featured-ai"
portfolio_status: "Public repository"
portfolio_category: "RAG system"
portfolio_role: "Builder"
portfolio_year: 2026
repository_url: "https://github.com/sahaavi/GovtIntel"
case_study_url: "/projects/govtintel/"
home_summary: "Procurement intelligence system combining asynchronous ingestion, PostgreSQL, hybrid retrieval, reranking, SQL analytics, structured outputs, and fail-closed citation validation."
system_map:
  - label: "Award data"
  - label: "PostgreSQL"
  - label: "Vector index"
  - label: "Hybrid retrieval"
    accent: true
  - label: "Reranking"
  - label: "Citation checks"
    accent: true
```

- [ ] **Step 5: Create the selected-work partial**

```html
{{/* layouts/partials/home/selected-work.html */}}
{{- $featured := where site.RegularPages "Params.home_featured" true -}}
{{- if ne (len $featured) 2 }}{{ errorf "Homepage requires exactly two home_featured projects" }}{{ end -}}
{{- range $featured -}}
  {{- if or (not .Params.repository_url) (not .Params.portfolio_status) (not .Params.home_summary) -}}
    {{- errorf "%s requires repository_url, portfolio_status, and home_summary" .File.Path -}}
  {{- end -}}
{{- end -}}
<section id="work" class="portfolio-section" aria-labelledby="work-title">
  <div class="portfolio-section-head">
    <p class="portfolio-label">03 · Selected work</p>
    <div>
      <h2 id="work-title">Public systems for inspecting the engineering.</h2>
      <p>Two focused case studies provide technical proof without taking over the professional narrative.</p>
    </div>
  </div>
  <div class="portfolio-work-list">
    {{- range sort $featured "Params.home_order" "asc" }}
    <article class="portfolio-work-row">
      <div class="portfolio-work-meta"><strong>{{ .Params.portfolio_status }}</strong><span>{{ .Params.portfolio_category }}</span><span>{{ .Params.portfolio_year }}</span></div>
      <div class="portfolio-work-copy">
        <h3>{{ .Title }}</h3>
        <p>{{ .Params.home_summary }}</p>
        <div class="portfolio-work-links">
          <a href="{{ .Params.repository_url }}" target="_blank" rel="noopener noreferrer">Repository</a>
          <a href="{{ .RelPermalink }}">Case study</a>
        </div>
      </div>
      <div class="portfolio-system-map" aria-label="{{ .Title }} system map">
        {{- range .Params.system_map }}<span{{ if .accent }} class="is-accent"{{ end }}>{{ .label }}</span>{{ end }}
      </div>
    </article>
    {{- end }}
  </div>
</section>
```

- [ ] **Step 6: Insert the partial and add styles**

Insert after expertise:

```html
{{- partial "home/selected-work.html" . }}
```

Append the following complete structural rules:

```css
.portfolio-work-list { border-top: 1px solid var(--portfolio-line-strong); }
.portfolio-work-row { display: grid; grid-template-columns: 170px minmax(0, 1fr) minmax(290px, .8fr); gap: 34px; align-items: center; padding: 42px 0; border-bottom: 1px solid var(--portfolio-line); }
.portfolio-work-meta span, .portfolio-work-meta strong { display: block; }
.portfolio-work-meta { color: var(--portfolio-ink-soft); font: 400 10px/1.8 "IBM Plex Mono", monospace; text-transform: uppercase; }
.portfolio-work-meta strong { color: var(--portfolio-green); font-weight: 500; }
.portfolio-work-copy h3 { margin: 0 0 12px; font-size: clamp(25px, 3.2vw, 36px); }
.portfolio-work-copy p { margin: 0; color: var(--portfolio-ink-soft); }
.portfolio-work-links { margin-top: 18px; }
.portfolio-work-links a { margin-right: 18px; color: var(--portfolio-blue); font-size: 13px; font-weight: 650; text-underline-offset: 4px; }
.portfolio-system-map { min-height: 180px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; align-content: center; padding: 22px; border: 1px solid var(--portfolio-line); border-radius: var(--portfolio-radius-md); background: var(--portfolio-surface-soft); }
.portfolio-system-map span { min-height: 54px; display: grid; place-items: center; padding: 8px; border: 1px solid var(--portfolio-line-strong); border-radius: 6px; color: var(--portfolio-ink-soft); background: var(--portfolio-surface); font: 400 9px "IBM Plex Mono", monospace; text-align: center; }
.portfolio-system-map .is-accent { color: var(--portfolio-blue); border-color: var(--portfolio-blue); background: var(--portfolio-blue-soft); }

@media (max-width: 920px) {
  .portfolio-work-row { grid-template-columns: 130px 1fr; }
  .portfolio-system-map { grid-column: 2; }
}

@media (max-width: 640px) {
  .portfolio-work-row { grid-template-columns: 1fr; gap: 18px; }
  .portfolio-system-map { grid-column: auto; }
}
```

- [ ] **Step 7: Run tests and commit**

Run: `python3 -m unittest tests.test_homepage_contract -v`
Expected: all selected-work and earlier homepage tests pass.

```bash
git add content/projects/vision-maintenance-agent/index.md content/projects/govtintel/index.md layouts/index.html layouts/partials/home/selected-work.html assets/css/extended/portfolio-home.css tests/test_homepage_contract.py
git commit -m "feat: add balanced selected AI systems"
```

---

### Task 7: Complete the Homepage With Writing, Education, and Contact

**Files:**
- Create: `layouts/partials/home/writing-education.html`
- Create: `layouts/partials/home/contact.html`
- Modify: `layouts/index.html`
- Modify: `layouts/partials/footer.html`
- Modify: `assets/css/extended/portfolio-base.css`
- Modify: `assets/css/extended/portfolio-home.css`
- Modify: `tests/test_homepage_contract.py`

- [ ] **Step 1: Add failing closing-section assertions**

```python
    def test_homepage_closes_with_writing_education_and_contact(self) -> None:
        html = self.page_html("/")
        for text in (
            "Writing &amp; research",
            "Data science and computer science foundations",
            "Master of Data Science",
            "BSc Computer Science &amp; Engineering",
            "LLM Engineering From Scratch",
            "Tokenizer From Scratch",
            "Published ASD research",
            "Start a conversation",
        ):
            self.assertIn(text, html)

    def test_homepage_has_no_resume_or_download_control(self) -> None:
        html = self.page_html("/")
        self.assertNotIn(">Resume<", html)
        self.assertNotIn("downloadable resume", html.lower())
        self.assertNotIn("download pdf", html.lower())
        self.assertIn(">GitHub<", html)
        self.assertIn(">LinkedIn<", html)
        self.assertIn(">Email<", html)
        self.assertNotIn(">X<", html)
```

- [ ] **Step 2: Verify failure**

Run: `python3 -m unittest tests.test_homepage_contract.HomepageContractTests.test_homepage_closes_with_writing_education_and_contact -v`
Expected: FAIL because the closing sections do not exist.

- [ ] **Step 3: Create writing and education partial**

```html
{{/* layouts/partials/home/writing-education.html */}}
{{- $profile := site.Data.profile -}}
<section id="writing" class="portfolio-section portfolio-closing-grid" aria-label="Writing, research, and education">
  <article>
    <p class="portfolio-label">04 · Writing & research</p>
    <h2>Technical depth should remain inspectable.</h2>
    <p>Engineering notes, the LLM-from-scratch series, the interactive tokenizer, and published ML research show how the work is understood and communicated.</p>
    <ul class="portfolio-evidence-links">
      <li><a href="/projects/llm-engineering-from-scratch/"><strong>LLM Engineering From Scratch</strong><span>Learning lab and implementation series</span></a></li>
      <li><a href="/posts/llm-engineering-from-scratch-tokenizer/"><strong>Tokenizer From Scratch</strong><span>Interactive byte-level BPE walkthrough</span></a></li>
      <li><a href="/projects/autism-spectrum-disorder-prediction/"><strong>Published ASD research</strong><span>Early machine-learning research foundation</span></a></li>
    </ul>
    <a class="portfolio-text-link" href="/posts/">Explore all writing →</a>
  </article>
  <article>
    <p class="portfolio-label">05 · Education</p>
    <h2>Data science and computer science foundations.</h2>
    {{- range $profile.education }}
    <p><strong>{{ .degree }}</strong>, {{ .institution }}{{ with .detail }} · {{ . }}{{ end }}</p>
    {{- end }}
    <a class="portfolio-text-link" href="/experience/">View the full experience profile →</a>
  </article>
</section>
```

- [ ] **Step 4: Create the contact partial**

```html
{{/* layouts/partials/home/contact.html */}}
<section id="contact" class="portfolio-contact-band" aria-labelledby="contact-title">
  <div>
    <p class="portfolio-label">Contact</p>
    <h2 id="contact-title">Building AI or ML systems that need engineering depth?</h2>
  </div>
  <a class="portfolio-button" href="{{ site.Data.profile.social.email }}">Start a conversation →</a>
</section>
```

- [ ] **Step 5: Complete homepage order**

`layouts/index.html` must now be exactly:

```html
{{- define "main" }}
<div class="portfolio-home">
  {{- partial "home/hero.html" . }}
  {{- partial "home/experience.html" . }}
  {{- partial "home/expertise.html" . }}
  {{- partial "home/selected-work.html" . }}
  {{- partial "home/writing-education.html" . }}
  {{- partial "home/contact.html" . }}
</div>
{{- end }}
```

- [ ] **Step 6: Add closing and contact styles**

```css
.portfolio-closing-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 72px; }
.portfolio-closing-grid h2 { margin: 14px 0 18px; font-size: 30px; }
.portfolio-closing-grid p { color: var(--portfolio-ink-soft); }
.portfolio-evidence-links { margin: 26px 0; padding: 0; border-top: 1px solid var(--portfolio-line); list-style: none; }
.portfolio-evidence-links li { border-bottom: 1px solid var(--portfolio-line); }
.portfolio-evidence-links a { display: grid; gap: 3px; padding: 14px 0; color: var(--portfolio-ink); text-decoration: none; }
.portfolio-evidence-links span { color: var(--portfolio-ink-soft); font: 400 11px "IBM Plex Mono", monospace; }
.portfolio-text-link { color: var(--portfolio-blue); font-size: 14px; font-weight: 650; text-underline-offset: 4px; }
.portfolio-contact-band { padding: 78px 0; display: grid; grid-template-columns: 1fr auto; gap: 48px; align-items: center; color: var(--portfolio-paper); background: var(--portfolio-ink); box-shadow: 0 0 0 100vmax var(--portfolio-ink); clip-path: inset(0 -100vmax); }
.portfolio-contact-band h2 { max-width: 780px; margin: 12px 0 0; color: var(--portfolio-paper); font-size: clamp(38px, 5.5vw, 66px); line-height: 1.03; }
.portfolio-contact-band .portfolio-button { color: var(--portfolio-ink); background: var(--portfolio-paper); border-color: var(--portfolio-paper); }

@media (max-width: 640px) {
  .portfolio-closing-grid, .portfolio-contact-band { grid-template-columns: 1fr; }
  .portfolio-closing-grid { gap: 50px; }
  .portfolio-contact-band { padding-block: 62px; }
}
```

- [ ] **Step 7: Align the footer and preserve PaperMod behavior**

Replace only the opening footer markup in `layouts/partials/footer.html`—from its initial `hideFooter` condition through the matching `end`—with the block below. Leave the scroll-to-top control, `extend_footer` call, theme logic, menu persistence, and code-copy behavior in place:

```html
{{- if not (.Param "hideFooter") }}
<footer class="footer portfolio-footer">
  <span>&copy; {{ now.Year }} <a href="{{ site.Home.RelPermalink }}">{{ site.Data.profile.name }}</a></span>
  <nav class="portfolio-footer-links" aria-label="Professional links">
    <a href="{{ site.Data.profile.social.github }}" target="_blank" rel="noopener noreferrer me">GitHub</a>
    <a href="{{ site.Data.profile.social.linkedin }}" target="_blank" rel="noopener noreferrer me">LinkedIn</a>
    <a href="{{ site.Data.profile.social.email }}">Email</a>
  </nav>
</footer>
{{- end }}
```

Inside the existing first script block, replace only the `document.querySelectorAll('a[href^="#"]')` listener with this null-safe, skip-link-aware version:

```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (event) {
        const id = decodeURIComponent(this.getAttribute("href").slice(1));
        const target = document.getElementById(id);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({
            behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? "auto" : "smooth"
        });
        if (this.classList.contains("portfolio-skip-link")) {
            target.focus({ preventScroll: true });
        }
        if (id === "top") {
            history.replaceState(null, "", window.location.pathname + window.location.search);
        } else {
            history.pushState(null, "", `#${id}`);
        }
    });
});
```

Replace the current theme-toggle script body so the persisted theme behavior remains the same while `aria-pressed` reflects dark-mode state:

```javascript
const themeToggle = document.getElementById("theme-toggle");
const html = document.documentElement;
const syncThemeState = () => {
    themeToggle.setAttribute("aria-pressed", String(html.dataset.theme === "dark"));
};
syncThemeState();
themeToggle.addEventListener("click", () => {
    const nextTheme = html.dataset.theme === "dark" ? "light" : "dark";
    html.dataset.theme = nextTheme;
    localStorage.setItem("pref-theme", nextTheme);
    syncThemeState();
});
```

Append these shared rules to `portfolio-base.css`:

```css
.portfolio-footer {
  max-width: var(--portfolio-max);
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding-inline: 20px;
  color: var(--portfolio-ink-soft);
  font-size: 0.82rem;
}

.portfolio-footer-links { display: flex; flex-wrap: wrap; gap: 20px; }
.portfolio-footer a { color: var(--portfolio-ink); text-decoration: none; }

@media (max-width: 640px) {
  .portfolio-footer { align-items: flex-start; flex-direction: column; padding-inline: 14px; }
}
```

- [ ] **Step 8: Run tests and commit**

Run: `python3 -m unittest tests.test_homepage_contract tests.test_baseline -v`
Expected: all tests pass.

```bash
git add layouts/index.html layouts/partials/home/writing-education.html layouts/partials/home/contact.html layouts/partials/footer.html assets/css/extended/portfolio-base.css assets/css/extended/portfolio-home.css tests/test_homepage_contract.py
git commit -m "feat: complete portfolio homepage narrative"
```

---

### Task 8: Replace About With a Web-Native Experience Route

**Files:**
- Create: `content/experience.md`
- Create: `layouts/_default/experience.html`
- Create: `tests/test_experience_contract.py`
- Modify: `assets/css/extended/portfolio-base.css`
- Delete: `content/about.md`

- [ ] **Step 1: Write the failing experience-route contract**

```python
# tests/test_experience_contract.py
from tests.site_harness import HugoSiteTestCase


class ExperienceRouteTests(HugoSiteTestCase):
    def test_experience_is_the_canonical_profile(self) -> None:
        html = self.page_html("/experience/")
        self.assertIn("Professional experience", html)
        self.assertIn("Data &amp; Applied AI Analyst", html)
        self.assertIn("Data Scientist, Applied AI", html)
        self.assertIn("Capstone Data Scientist", html)
        self.assertIn("Co-Founder / Data Scientist", html)
        self.assertNotIn("4+ years", html)
        self.assertNotIn("Download", html)

    def test_about_redirects_to_experience(self) -> None:
        html = self.page_html("/about/")
        self.assertIn("/experience/", html)
```

- [ ] **Step 2: Verify failure**

Run: `python3 -m unittest tests.test_experience_contract -v`
Expected: FAIL because `/experience/` does not exist.

- [ ] **Step 3: Create route metadata**

```markdown
---
title: "Experience"
layout: "experience"
url: "/experience/"
aliases:
  - "/about/"
summary: "Professional experience, education, and engineering range for Avishek Saha, Applied AI and ML Engineer."
ShowReadingTime: false
ShowBreadCrumbs: false
ShowShareButtons: false
hideMeta: true
---
```

- [ ] **Step 4: Create the experience layout**

```html
{{/* layouts/_default/experience.html */}}
{{- define "main" }}
<article class="portfolio-experience-page">
  <header>
    <p class="portfolio-label">Applied AI & ML Engineer</p>
    <h1>Professional experience</h1>
    <p>{{ site.Data.profile.hero.supporting }}</p>
  </header>
  <section aria-labelledby="experience-page-roles">
    <h2 id="experience-page-roles">Experience</h2>
    {{- range site.Data.experience.roles }}
    <article class="portfolio-role-detail">
      <div>
        <p class="portfolio-label">{{ .period }}</p>
        <h3>{{ .title }}</h3>
        <p class="portfolio-meta">{{ .employer }} · {{ .location }}</p>
      </div>
      <ul>{{- range .details }}<li>{{ . }}</li>{{ end }}</ul>
    </article>
    {{- end }}
  </section>
  <section aria-labelledby="experience-page-education">
    <h2 id="experience-page-education">Education</h2>
    {{- range site.Data.profile.education }}
    <p><strong>{{ .degree }}</strong><br>{{ .institution }} · {{ .period }}{{ with .detail }} · {{ . }}{{ end }}</p>
    {{- end }}
  </section>
  <section aria-labelledby="experience-page-range">
    <h2 id="experience-page-range">Engineering range</h2>
    <div class="portfolio-experience-expertise">
      {{- range site.Data.expertise.groups }}
      <article><h3>{{ .title }}</h3><p>{{ .summary }}</p></article>
      {{- end }}
    </div>
  </section>
</article>
{{- end }}
```

- [ ] **Step 5: Delete the old About source and add scoped styles**

Delete `content/about.md`. Append to `portfolio-base.css`:

```css
.portfolio-experience-page { max-width: 980px; margin: 0 auto; }
.portfolio-experience-page > header { max-width: 760px; margin-bottom: 64px; }
.portfolio-experience-page > header h1 { font-size: clamp(44px, 7vw, 76px); line-height: 1; }
.portfolio-role-detail { display: grid; grid-template-columns: minmax(240px, .7fr) minmax(0, 1.3fr); gap: 48px; padding: 34px 0; border-top: 1px solid var(--portfolio-line); }
.portfolio-role-detail ul { margin: 0; color: var(--portfolio-ink-soft); }
.portfolio-experience-expertise { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }
.portfolio-experience-expertise article { padding: 24px; border: 1px solid var(--portfolio-line); border-radius: var(--portfolio-radius-md); background: var(--portfolio-surface); }

@media (max-width: 640px) {
  .portfolio-role-detail, .portfolio-experience-expertise { grid-template-columns: 1fr; }
  .portfolio-role-detail { gap: 12px; }
}
```

- [ ] **Step 6: Run tests and commit**

Run: `python3 -m unittest tests.test_experience_contract tests.test_homepage_contract -v`
Expected: all tests pass.

```bash
git add content/experience.md content/about.md layouts/_default/experience.html assets/css/extended/portfolio-base.css tests/test_experience_contract.py
git commit -m "feat: add web-native experience profile"
```

---

### Task 9: Reorganize the Work Index and Repair Project Navigation

**Files:**
- Create: `tests/test_project_contract.py`
- Modify: `archetypes/projects.md`
- Modify: `content/projects/_index.md`
- Modify: `content/projects/vision-maintenance-agent/index.md`
- Modify: `content/projects/govtintel/index.md`
- Modify: `content/projects/llm-engineering-from-scratch/index.md`
- Modify: `content/projects/asd-prediction/index.md`
- Modify: `layouts/projects/list.html`
- Modify: `layouts/projects/single.html:49-64`
- Create: `assets/css/extended/portfolio-projects.css`
- Create: `content/projects/vision-maintenance-agent/architecture.png`
- Create: `content/projects/govtintel/govintel-ui.png`

- [ ] **Step 1: Write failing grouped-index and pagination tests**

```python
# tests/test_project_contract.py
from tests.site_harness import HugoSiteTestCase


class ProjectContractTests(HugoSiteTestCase):
    def test_work_index_has_three_evidence_groups(self) -> None:
        html = self.page_html("/projects/")
        for heading in ("Featured AI Systems", "ML Systems &amp; Labs", "Research &amp; Foundations"):
            self.assertIn(heading, html)
        for title in ("Maintenance-Eye", "GovIntel", "LLM Engineering From Scratch", "Autism Screening Data Dashboard Research"):
            self.assertIn(title, html)

    def test_project_cards_show_status_role_and_year(self) -> None:
        html = self.page_html("/projects/")
        self.assertIn("Public demo", html)
        self.assertIn("Public repository", html)
        self.assertIn("Lab series", html)
        self.assertIn("Published research", html)

    def test_middle_project_has_independent_previous_and_next_links(self) -> None:
        html = self.page_html("/projects/govtintel/")
        self.assertIn("Previous Project", html)
        self.assertIn("Next Project", html)
```

- [ ] **Step 2: Verify failure**

Run: `python3 -m unittest tests.test_project_contract -v`
Expected: FAIL because the current list is ungrouped and Next is nested inside the Previous condition.

- [ ] **Step 3: Expand the project archetype**

```yaml
---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
tags: []
portfolio_group: "ml-labs"
portfolio_status: "Prototype"
portfolio_category: ""
portfolio_role: "Builder"
portfolio_year: {{ now.Year }}
repository_url: ""
home_featured: false
home_order: 99
home_summary: ""
system_map: []
cover:
  image: ""
  alt: ""
  relative: true
weight: 10
showToc: true
---
```

- [ ] **Step 4: Add metadata to the supporting public projects**

Add to LLM Engineering From Scratch:

```yaml
portfolio_group: "ml-labs"
portfolio_status: "Lab series"
portfolio_category: "LLM engineering"
portfolio_role: "Builder and writer"
portfolio_year: 2026
repository_url: "https://github.com/sahaavi/llm-engineering-from-scratch"
home_featured: false
```

Add to ASD research:

```yaml
portfolio_group: "research"
portfolio_status: "Published research"
portfolio_category: "Machine learning"
portfolio_role: "Research contributor"
portfolio_year: 2021
repository_url: ""
home_featured: false
```

- [ ] **Step 5: Localize the two remote project images**

```bash
curl -fsSL https://raw.githubusercontent.com/sahaavi/Maintenance-Eye/main/docs/architecture.png -o content/projects/vision-maintenance-agent/architecture.png
curl -fsSL https://raw.githubusercontent.com/sahaavi/GovtIntel/main/docs/assets/govintel-ui.png -o content/projects/govtintel/govintel-ui.png
```

Update Maintenance-Eye's architecture Markdown image to `![Maintenance-Eye architecture](architecture.png)`. Update GovIntel's cover front matter to:

```yaml
cover:
  image: "govintel-ui.png"
  alt: "GovIntel Streamlit UI showing a generated procurement intelligence brief"
  relative: true
  hiddenInList: false
```

- [ ] **Step 6: Replace the project-list layout**

```html
{{- define "main" }}
<header class="page-header portfolio-work-header">
  <p class="portfolio-label">Selected work</p>
  <h1>{{ .Title }}</h1>
  <p>{{ .Description }}</p>
</header>
{{- $groups := slice
  (dict "key" "featured-ai" "title" "Featured AI Systems")
  (dict "key" "ml-labs" "title" "ML Systems & Labs")
  (dict "key" "research" "title" "Research & Foundations")
-}}
{{- $section := . -}}
{{- range $section.Pages -}}
  {{- if or (not .Params.portfolio_group) (not .Params.portfolio_status) (not .Params.portfolio_role) (not .Params.portfolio_year) -}}
    {{- errorf "%s requires portfolio_group, portfolio_status, portfolio_role, and portfolio_year" .File.Path -}}
  {{- end -}}
{{- end -}}
{{- range $groups }}
  {{- $group := . -}}
  {{- $pages := where $section.Pages "Params.portfolio_group" $group.key -}}
  {{- if gt (len $pages) 0 }}
  <section class="portfolio-project-group" aria-labelledby="group-{{ $group.key }}">
    <h2 id="group-{{ $group.key }}">{{ $group.title }}</h2>
    <div class="portfolio-project-grid">
      {{- range sort $pages "Weight" "asc" }}
      {{- $page := . -}}
      <article class="portfolio-project-card">
        {{- with $page.Params.cover.image }}
        {{- $cover := . -}}
        <a href="{{ $page.RelPermalink }}" class="portfolio-project-cover">
          <img src="{{ if $page.Params.cover.relative }}{{ path.Join $page.RelPermalink $cover }}{{ else }}{{ $cover }}{{ end }}" alt="{{ $page.Params.cover.alt | default $page.Title }}" loading="lazy">
        </a>
        {{- end }}
        <div>
          <p class="portfolio-project-meta">{{ $page.Params.portfolio_status }} · {{ $page.Params.portfolio_role }} · {{ $page.Params.portfolio_year }}</p>
          <h3><a href="{{ $page.RelPermalink }}">{{ $page.Title }}</a></h3>
          <p>{{ $page.Description }}</p>
          <a href="{{ $page.RelPermalink }}">Open case study →</a>
        </div>
      </article>
      {{- end }}
    </div>
  </section>
  {{- end }}
{{- end }}
{{- end }}
```

- [ ] **Step 7: Repair project previous/next navigation**

Add `portfolio-project-single` to the existing article class:

```html
<article class="post-single portfolio-project-single">
```

Then replace `layouts/projects/single.html:49-64` with:

```html
{{- if or .PrevInSection .NextInSection }}
<nav class="paginav" aria-label="Project navigation">
  {{- with .PrevInSection }}
  <a class="prev" href="{{ .RelPermalink }}"><span class="title">← Previous Project</span><br><span>{{ .Title }}</span></a>
  {{- end }}
  {{- with .NextInSection }}
  <a class="next" href="{{ .RelPermalink }}"><span class="title">Next Project →</span><br><span>{{ .Title }}</span></a>
  {{- end }}
</nav>
{{- end }}
```

- [ ] **Step 8: Add project styles and update index copy**

Set `content/projects/_index.md` description to:

```yaml
description: "Selected AI systems, machine-learning work, technical labs, and research foundations."
```

Create the scoped project stylesheet:

```css
/* assets/css/extended/portfolio-projects.css */
.portfolio-work-header {
  max-width: 760px;
  margin: 20px 0 58px;
}

.portfolio-work-header h1 {
  margin: 10px 0 14px;
  font-size: clamp(42px, 7vw, 76px);
  line-height: 0.98;
}

.portfolio-work-header > p:last-child {
  color: var(--portfolio-ink-soft);
  font-size: 1.08rem;
}

.portfolio-project-group {
  margin: 0 0 72px;
}

.portfolio-project-group > h2 {
  margin: 0 0 24px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--portfolio-line-strong);
  font: 500 0.76rem/1.4 "IBM Plex Mono", monospace;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.portfolio-project-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.portfolio-project-card {
  overflow: hidden;
  border: 1px solid var(--portfolio-line);
  border-radius: var(--portfolio-radius-md);
  background: var(--portfolio-surface);
  box-shadow: var(--portfolio-shadow);
}

.portfolio-project-card > div {
  padding: 24px;
}

.portfolio-project-card h3 {
  margin: 8px 0 10px;
  font-size: clamp(22px, 2.5vw, 30px);
}

.portfolio-project-card h3 a,
.portfolio-project-card > div > a {
  color: var(--portfolio-ink);
  text-decoration: none;
}

.portfolio-project-card > div > a {
  color: var(--portfolio-blue);
  font-size: 0.86rem;
  font-weight: 650;
}

.portfolio-project-card p:not(.portfolio-project-meta) {
  color: var(--portfolio-ink-soft);
}

.portfolio-project-cover {
  display: block;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-bottom: 1px solid var(--portfolio-line);
  background: var(--portfolio-surface-soft);
}

.portfolio-project-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.portfolio-project-meta {
  margin: 0;
  color: var(--portfolio-green);
  font: 500 0.66rem/1.6 "IBM Plex Mono", monospace;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.portfolio-project-single,
.portfolio-project-single .post-content,
.portfolio-project-single .entry-cover,
.portfolio-project-single #toc-container {
  max-width: 100%;
  min-width: 0;
}

.portfolio-project-single .entry-cover {
  overflow: hidden;
}

.portfolio-project-single .entry-cover img {
  display: block;
  width: 100%;
  height: auto;
}

.portfolio-project-single .post-content {
  overflow-wrap: anywhere;
}

@media (max-width: 720px) {
  .portfolio-work-header { margin-bottom: 42px; }
  .portfolio-project-group { margin-bottom: 52px; }
  .portfolio-project-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 9: Run tests and commit**

Run: `python3 -m unittest tests.test_project_contract tests.test_baseline -v`
Expected: all tests pass and draft routes remain absent.

```bash
git add archetypes/projects.md content/projects layouts/projects/list.html layouts/projects/single.html assets/css/extended/portfolio-projects.css tests/test_project_contract.py
git commit -m "feat: organize portfolio work by evidence type"
```

---

### Task 10: Add Homepage Metadata, Social Image, and Structured Data

**Files:**
- Create: `tests/test_metadata_contract.py`
- Create: `scripts/generate_og_image.py`
- Create: `static/images/og-image.png`
- Create: `layouts/partials/templates/schema_json.html`
- Modify: `hugo.yaml:2,18-26`

- [ ] **Step 1: Write failing metadata tests**

```python
# tests/test_metadata_contract.py
import json
import re
import struct

from tests.site_harness import HugoSiteTestCase, ROOT


class MetadataContractTests(HugoSiteTestCase):
    def test_homepage_title_description_and_social_image(self) -> None:
        html = self.page_html("/")
        self.assertIn("<title>Avishek Saha | Applied AI &amp; ML Engineer</title>", html)
        self.assertIn('property="og:image"', html)
        self.assertIn("/images/og-image.png", html)

    def test_social_image_is_1200_by_630(self) -> None:
        data = (ROOT / "static/images/og-image.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1200, 630))

    def test_homepage_schema_is_profile_page_with_person(self) -> None:
        html = self.page_html("/")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        payloads = [json.loads(block) for block in blocks]
        profile = next(item for item in payloads if item.get("@type") == "ProfilePage")
        self.assertEqual(profile["mainEntity"]["@type"], "Person")
        self.assertIn("https://github.com/sahaavi", profile["mainEntity"]["sameAs"])

    def test_project_schema_is_software_source_code(self) -> None:
        html = self.page_html("/projects/govtintel/")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        payloads = [json.loads(block) for block in blocks]
        self.assertTrue(
            any(item.get("@type") == "SoftwareSourceCode" for item in payloads)
        )

    def test_research_project_schema_is_scholarly_article(self) -> None:
        html = self.page_html("/projects/autism-spectrum-disorder-prediction/")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        payloads = [json.loads(block) for block in blocks]
        self.assertTrue(
            any(item.get("@type") == "ScholarlyArticle" for item in payloads)
        )
```

- [ ] **Step 2: Verify failure**

Run: `python3 -m unittest tests.test_metadata_contract -v`
Expected: FAIL because the title, PNG, ProfilePage schema, and project schema are not complete.

- [ ] **Step 3: Update site metadata**

Set the top-level title used by PaperMod's `<title>` partial, then replace the relevant `params` values in `hugo.yaml`:

```yaml
title: "Avishek Saha | Applied AI & ML Engineer"

params:
  title: "Avishek Saha | Applied AI & ML Engineer"
  description: "Applied AI and machine learning engineer with experience across LLM applications, RAG and evaluation, predictive ML, APIs, data systems, and cloud delivery."
  keywords: ["Applied AI Engineer", "Machine Learning Engineer", "LLM Evaluation", "RAG", "Predictive Machine Learning", "FastAPI", "Python", "MLOps"]
  author: "Avishek Saha"
  images: ["/images/og-image.png"]
  schema:
    publisherType: "Person"
    sameAs:
      - "https://github.com/sahaavi"
      - "https://linkedin.com/in/sahaavi"
```

Do not override PaperMod's full `head.html`; its homepage title already reads the top-level `site.Title`. The custom header and footer continue to display `site.Data.profile.name`, so the SEO title does not become the visible wordmark.

- [ ] **Step 4: Add the deterministic OG generator**

```python
# scripts/generate_og_image.py
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static/images/og-image.png"
WIDTH, HEIGHT = 1200, 630


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    )
    for name in names:
        path = Path(name)
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#F5F7F4")
    draw = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 64):
        draw.line((x, 0, x, HEIGHT), fill="#E5E9EE", width=1)
    for y in range(0, HEIGHT, 64):
        draw.line((0, y, WIDTH, y), fill="#E5E9EE", width=1)
    draw.rounded_rectangle((70, 62, 133, 125), radius=31, outline="#245BDC", width=2, fill="#FFFFFF")
    draw.text((88, 80), "AS", fill="#245BDC", font=font(20, bold=True))
    draw.text((70, 170), "AVISHEK SAHA", fill="#245BDC", font=font(22, bold=True))
    draw.text((70, 220), "Applied AI &", fill="#0D1726", font=font(72, bold=True))
    draw.text((70, 305), "ML Engineer", fill="#0D1726", font=font(72, bold=True))
    draw.text((70, 420), "LLM systems · evaluation · predictive ML · APIs · cloud", fill="#526071", font=font(27))
    draw.rectangle((70, 512, 1130, 516), fill="#245BDC")
    draw.text((70, 545), "avisheksaha.com", fill="#526071", font=font(24))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
```

Run: `python3 scripts/generate_og_image.py`
Expected: `static/images/og-image.png` exists and is 1200×630.

Pillow is a workstation-only regeneration dependency. Commit the generated PNG; CI validates its PNG header and dimensions with the Python standard library and does not run this generator.

- [ ] **Step 5: Override schema for home and project pages**

Create the complete local schema override below. It preserves article and section types, describes the homepage as a professional profile, distinguishes code projects from research, and uses Hugo's JSON encoder instead of hand-built JSON:

```html
{{- $author := dict
  "@type" "Person"
  "name" site.Data.profile.name
  "url" site.Home.Permalink
-}}

{{- if .IsHome -}}
  {{- $person := merge $author (dict
    "jobTitle" site.Data.profile.role
    "image" ("/images/og-image.png" | absURL)
    "sameAs" site.Params.schema.sameAs
  ) -}}
  {{- $schema := dict
    "@context" "https://schema.org"
    "@type" "ProfilePage"
    "name" site.Params.title
    "url" site.Home.Permalink
    "description" site.Params.description
    "mainEntity" $person
  -}}
<script type="application/ld+json">
{{ $schema | jsonify | safeJS }}
</script>

{{- else if and .IsPage (eq .Section "projects") -}}
  {{- $schemaType := "SoftwareSourceCode" -}}
  {{- if eq .Params.portfolio_group "research" -}}
    {{- $schemaType = "ScholarlyArticle" -}}
  {{- end -}}
  {{- $schema := dict
    "@context" "https://schema.org"
    "@type" $schemaType
    "name" .Title
    "description" .Description
    "url" .Permalink
    "author" $author
    "keywords" (.Params.tags | default (slice))
  -}}
  {{- with .Params.repository_url -}}
    {{- $schema = merge $schema (dict "codeRepository" .) -}}
  {{- end -}}
<script type="application/ld+json">
{{ $schema | jsonify | safeJS }}
</script>

{{- else if and .IsPage (eq .Layout "experience") -}}
  {{- $schema := dict
    "@context" "https://schema.org"
    "@type" "ProfilePage"
    "name" .Title
    "description" .Description
    "url" .Permalink
    "mainEntity" $author
  -}}
<script type="application/ld+json">
{{ $schema | jsonify | safeJS }}
</script>

{{- else if .IsPage -}}
  {{- $schema := dict
    "@context" "https://schema.org"
    "@type" "BlogPosting"
    "headline" .Title
    "name" .Title
    "description" (.Description | default .Summary | plainify)
    "url" .Permalink
    "datePublished" .PublishDate
    "dateModified" .Lastmod
    "author" $author
    "keywords" (.Params.tags | default (slice))
  -}}
<script type="application/ld+json">
{{ $schema | jsonify | safeJS }}
</script>

{{- else if .IsSection -}}
  {{- $schema := dict
    "@context" "https://schema.org"
    "@type" "CollectionPage"
    "name" .Title
    "description" (.Description | default .Summary | plainify)
    "url" .Permalink
  -}}
<script type="application/ld+json">
{{ $schema | jsonify | safeJS }}
</script>
{{- end -}}
```

- [ ] **Step 6: Run tests and commit**

Run: `python3 -m unittest tests.test_metadata_contract -v`
Expected: all five metadata tests pass.

```bash
git add hugo.yaml scripts/generate_og_image.py static/images/og-image.png layouts/partials/templates/schema_json.html tests/test_metadata_contract.py
git commit -m "feat: add portfolio metadata and social identity"
```

---

### Task 11: Split Legacy CSS and Add CI Quality Gates

**Files:**
- Create: `assets/css/extended/portfolio-blog.css`
- Create: `tests/test_internal_links.py`
- Modify: `.github/workflows/hugo.yml`
- Delete: `assets/css/extended/custom.css`

- [ ] **Step 1: Write the failing CSS-cleanup and internal-link tests**

```python
# tests/test_internal_links.py
from html.parser import HTMLParser
from urllib.parse import urlsplit

from tests.site_harness import HugoSiteTestCase, ROOT


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = dict(attrs)
        if values.get("href"):
            self.links.append(values["href"] or "")


class InternalLinkTests(HugoSiteTestCase):
    def test_generated_internal_links_resolve(self) -> None:
        failures: list[str] = []
        for html_path in self.output_dir.rglob("*.html"):
            parser = LinkCollector()
            parser.feed(html_path.read_text(encoding="utf-8"))
            for href in parser.links:
                if href.startswith(("mailto:", "tel:", "#")):
                    continue
                parsed = urlsplit(href)
                if parsed.scheme not in ("", "http", "https"):
                    continue
                if parsed.netloc and parsed.netloc not in (
                    "avisheksaha.com",
                    "www.avisheksaha.com",
                ):
                    continue
                path = parsed.path
                if not path:
                    continue
                if path.startswith("/"):
                    candidate = self.output_dir / path.strip("/")
                else:
                    candidate = html_path.parent / path
                if path.endswith("/"):
                    candidate = candidate / "index.html"
                elif candidate.suffix == "":
                    candidate = candidate / "index.html"
                if not candidate.exists():
                    failures.append(f"{html_path.relative_to(self.output_dir)} -> {href}")
        self.assertEqual([], failures, "Broken internal links:\n" + "\n".join(failures))

    def test_legacy_custom_stylesheet_is_removed(self) -> None:
        self.assertFalse((ROOT / "assets/css/extended/custom.css").exists())

    def test_blog_styles_are_preserved_without_legacy_home_or_project_rules(self) -> None:
        path = ROOT / "assets/css/extended/portfolio-blog.css"
        self.assertTrue(path.is_file())
        css = path.read_text(encoding="utf-8")
        for selector in (
            ".blog-shell",
            ".blog-list-item",
            ".blog-mobile-toc",
            ".blog-post-nav",
        ):
            self.assertIn(selector, css)
        for legacy_selector in (
            ".hero-greeting",
            ".flagship-layout",
            ".case-study-grid",
            ".projects-grid",
            ".project-card",
        ):
            self.assertNotIn(legacy_selector, css)
```

- [ ] **Step 2: Verify the cleanup test fails**

Run: `python3 -m unittest tests.test_internal_links.InternalLinkTests.test_legacy_custom_stylesheet_is_removed tests.test_internal_links.InternalLinkTests.test_blog_styles_are_preserved_without_legacy_home_or_project_rules -v`
Expected: FAIL because `custom.css` still exists and the scoped blog stylesheet does not.

- [ ] **Step 3: Preserve only the existing blog rules**

Create `portfolio-blog.css` by moving the current blog rules without changing their declarations:

- Copy the contiguous source block beginning with `/* Blog list */` and ending immediately before `/* Projects grid */`.
- Copy the full `@media (max-width: 960px)` block containing `.main:has(.blog-shell)`, `.blog-shell`, `.blog-sidebar`, and `.blog-mobile-toc`.
- From the final `@media (max-width: 768px)` block, copy only `.blog-list-item`, `.blog-list-tags`, `.blog-post-nav`, and `.blog-post-nav-next` declarations into a new 768px media block.
- Do not copy global font rules, legacy homepage selectors, flagship/case-study selectors, old project-grid selectors, `.social-icons`, or `.dark` selectors. Their replacements already live in `portfolio-base.css`, `portfolio-home.css`, and `portfolio-projects.css`.

Run the two focused tests from Step 2. After they pass, delete `assets/css/extended/custom.css`, run the focused tests again, and confirm both remain green. This verifies the blog list, article shell, sidebar, mobile TOC, tags, and post navigation survived the split while legacy homepage/project rules did not.

- [ ] **Step 4: Update the deployment workflow**

Insert before `Build with Hugo`:

```yaml
      - name: Run site contract tests
        run: python3 -m unittest discover -s tests -v
```

Change the production build command to:

```yaml
      - name: Build with Hugo
        env:
          HUGO_CACHEDIR: ${{ runner.temp }}/hugo_cache
          HUGO_ENVIRONMENT: production
          TZ: America/Vancouver
        run: |
          hugo \
            --gc \
            --minify \
            --cleanDestinationDir
```

- [ ] **Step 5: Run the entire automated suite**

Run: `python3 -m unittest discover -s tests -v`
Expected: every test passes.

Run: `hugo --gc --minify --cleanDestinationDir --destination /tmp/portfolio-production-build`
Expected: exit code `0`, 65 or more generated pages, no new warning.

- [ ] **Step 6: Commit**

```bash
git add assets/css/extended/portfolio-blog.css assets/css/extended/custom.css tests/test_internal_links.py .github/workflows/hugo.yml
git commit -m "test: enforce portfolio build contracts"
```

---

### Task 12: Responsive, Accessibility, and Release Verification

**Files:**
- Modify only files implicated by verified failures.

- [ ] **Step 1: Run the full test and build gate**

```bash
python3 -m unittest discover -s tests -v
hugo --gc --minify --cleanDestinationDir --destination /tmp/portfolio-release
```

Expected: all tests pass and Hugo exits `0`.

- [ ] **Step 2: Start a local production-equivalent server**

Run in a persistent terminal:

```bash
hugo server --environment production --disableFastRender --bind 127.0.0.1 --port 1313
```

Expected: `Web Server is available at http://localhost:1313/`.

- [ ] **Step 3: Verify responsive layouts**

Inspect these exact viewport sizes in light and dark mode:

- `1440x900`
- `1024x768`
- `768x1024`
- `390x844`
- `375x812`
- `320x568`

At each size verify:

- No horizontal overflow.
- Hero text is not clipped.
- Experience precedes selected work.
- Header controls remain keyboard reachable.
- Maintenance-Eye and GovIntel use equal row structure.
- Project diagrams reflow beneath copy on small screens.
- Focus indicators are visible.
- Dark-mode links remain distinguishable from body text.
- Browser console contains no template, asset, or JavaScript errors.

At `390x844`, repeat the homepage check at 200% browser zoom. Then emulate `prefers-reduced-motion: reduce` and confirm the skip link, theme control, and all content remain usable without animated transitions.

- [ ] **Step 4: Run automated accessibility checks**

Run:

```bash
npx --yes browser-driver-manager@2.0.1 install chrome
eval "$(npx --yes browser-driver-manager@2.0.1 which)"
npx --yes @axe-core/cli@4.12.1 \
  http://127.0.0.1:1313/ \
  http://127.0.0.1:1313/experience/ \
  http://127.0.0.1:1313/projects/ \
  --exit \
  --chrome-path "$CHROME_TEST_PATH" \
  --chromedriver-path "$CHROMEDRIVER_TEST_PATH"
```

Expected: `0 violations found` for all three pages and exit code `0`. The browser-manager step pins a synchronized Chrome/ChromeDriver pair so axe does not depend on whatever browser version happens to be installed locally.

- [ ] **Step 5: Run Lighthouse**

```bash
CHROME_PATH="$CHROME_TEST_PATH" npx --yes lighthouse@13.4.0 http://127.0.0.1:1313/ \
  --only-categories=performance,accessibility,best-practices,seo \
  --output=json \
  --output-path=/tmp/portfolio-lighthouse.json \
  --chrome-flags="--headless --no-sandbox"
```

Expected minimum scores:

- Performance: `0.90`
- Accessibility: `0.95`
- Best Practices: `0.95`
- SEO: `0.95`

Read scores:

```bash
python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path('/tmp/portfolio-lighthouse.json').read_text())
for name in ('performance', 'accessibility', 'best-practices', 'seo'):
    print(name, data['categories'][name]['score'])
PY
```

- [ ] **Step 6: Validate the rendered metadata and forbidden copy**

```bash
if rg -n "Resume|Download PDF|4\+ years using Python|multi-agent|66 assets|150 work orders" \
  /tmp/portfolio-release/index.html \
  /tmp/portfolio-release/experience/index.html; then
  echo "Forbidden portfolio copy found" >&2
  exit 1
fi
```

Expected: no matches and exit code `0`.

```bash
test -f /tmp/portfolio-release/images/og-image.png
test ! -e /tmp/portfolio-release/projects/pennymize-ai-powered-personal-finance/index.html
test ! -e /tmp/portfolio-release/projects/price-prediction-platform-on-aws/index.html
```

Expected: all commands exit `0`.

- [ ] **Step 7: Review the final diff**

Run:

```bash
git diff --check
git status --short
git diff --stat master...HEAD
```

Expected: no whitespace errors and no unrelated files in the diff. If any verification command in this task fails, stop execution and return to the task that owns the failing acceptance criterion. Add a focused regression assertion there before changing source. When every command passes, do not create an empty final commit.

---

## Final Acceptance Checklist

- [ ] Hugo and PaperMod remain in place.
- [ ] Homepage identifies Avishek as an Applied AI & ML Engineer before any project.
- [ ] Hero statement is data-driven and contains no Python/SQL tenure claim.
- [ ] Professional experience appears before expertise and selected work.
- [ ] BCRTC is one current role, not the site's brand theme.
- [ ] Canonical visible titles and scoped metrics are used.
- [ ] Applied AI, ML, software/data, and delivery quality are all visible.
- [ ] Maintenance-Eye and GovIntel appear exactly once with equal visual structure.
- [ ] Maintenance-Eye copy contains no multi-agent or conflicting dataset claim.
- [ ] `/experience/` is canonical and `/about/` redirects to it.
- [ ] No downloadable resume or Resume navigation item exists.
- [ ] Projects are grouped into Featured AI Systems, ML Systems & Labs, and Research & Foundations.
- [ ] Draft/archived projects remain absent.
- [ ] Local fonts and local portfolio images replace runtime external dependencies.
- [ ] Homepage uses ProfilePage/Person schema, engineering projects use SoftwareSourceCode, and research uses ScholarlyArticle.
- [ ] Open Graph image exists at 1200×630.
- [ ] All Python contract tests pass.
- [ ] Hugo production build passes.
- [ ] Axe reports no critical/serious violations.
- [ ] Lighthouse thresholds pass.
- [ ] Desktop, tablet, mobile, light, dark, keyboard, zoom, and reduced-motion checks pass.
