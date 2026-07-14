# Homepage Copy Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the three approved homepage copy refinements without changing layout, navigation, project content, or any non-homepage location.

**Architecture:** Keep homepage identity and actions in `data/profile.yaml`, and remove the obsolete authorization rendering and validation from the existing hero partial. Extend the existing homepage contract test so the approved copy and absence of the authorization badge remain durable.

**Tech Stack:** Hugo 0.147, PaperMod, Go templates, YAML, Python `unittest`

**Design reference:** `docs/design/2026-07-13-homepage-copy-refinement-design.md`

---

### Task 1: Refine the Homepage Hero Copy

**Files:**
- Modify: `tests/test_homepage_contract.py:219-265`
- Modify: `data/profile.yaml:4-18`
- Modify: `layouts/partials/home/hero.html:7-8,51-55`

- [ ] **Step 1: Write the failing homepage contract**

In `test_hero_leads_with_ai_ml_and_not_a_project`, add these assertions after the existing hero-statement checks:

```python
self.assertIn("Applied AI & ML Engineer · Canada", hero)
self.assertIn('href="/#work">Projects</a>', hero)
self.assertNotIn('>Selected work</a>', hero)
self.assertNotIn("Canada work authorized", hero)
```

After reading `hero_source`, require the obsolete data field to be absent from the template:

```python
self.assertNotIn("work_authorized_label", hero_source)
```

Remove this obsolete expected validation from the existing validation tuple:

```python
"data/profile.yaml must define work_authorized_label",
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run:

```bash
python3 -m unittest \
  tests.test_homepage_contract.HomepageContractTests.test_hero_leads_with_ai_ml_and_not_a_project \
  -v
```

Expected: `FAIL` because the rendered hero still contains `Vancouver, BC`, `Selected work`, and `Canada work authorized`, and the hero template still references `work_authorized_label`.

- [ ] **Step 3: Apply the minimal profile-data changes**

Change the top of `data/profile.yaml` to:

```yaml
name: "Avishek Saha"
monogram: "AS"
role: "Applied AI & ML Engineer"
location: "Canada"
hero:
```

Change only the middle action label, retaining its existing destination:

```yaml
  - label: "Projects"
    url: "/#work"
    primary: false
```

- [ ] **Step 4: Remove authorization rendering and validation**

Delete this validation from `layouts/partials/home/hero.html`:

```go-html-template
{{- if or (not $profile.work_authorized_label) (not (strings.TrimSpace $profile.work_authorized_label)) }}{{ errorf "data/profile.yaml must define work_authorized_label" }}{{ end -}}
```

Leave the panel heading with no replacement badge:

```go-html-template
<div class="portfolio-panel-heading">
  <strong>Experience at a glance</strong>
</div>
```

- [ ] **Step 5: Run the focused test to verify it passes**

Run:

```bash
python3 -m unittest \
  tests.test_homepage_contract.HomepageContractTests.test_hero_leads_with_ai_ml_and_not_a_project \
  -v
```

Expected: `PASS`.

- [ ] **Step 6: Run the homepage contract and production build gates**

Run:

```bash
python3 -m unittest tests.test_homepage_contract -v
hugo --gc --minify --cleanDestinationDir --panicOnWarning \
  --destination /tmp/portfolio-copy-refinement
```

Expected: all homepage contract tests pass; Hugo produces at least 65 pages and exits `0` with no warning.

- [ ] **Step 7: Verify the exact rendered copy**

Run:

```bash
rg -n "Applied AI &amp; ML Engineer · Canada|>Projects</a>" \
  /tmp/portfolio-copy-refinement/index.html

if rg -n "Vancouver, BC|Canada work authorized|>Selected work</a>" \
  /tmp/portfolio-copy-refinement/index.html; then
  echo "Obsolete homepage copy found" >&2
  exit 1
fi
```

Expected: the first command finds both approved strings; the obsolete-copy check returns no matches.

- [ ] **Step 8: Commit the implementation**

```bash
git add data/profile.yaml layouts/partials/home/hero.html tests/test_homepage_contract.py
git commit -m "fix: refine homepage hero copy"
```
