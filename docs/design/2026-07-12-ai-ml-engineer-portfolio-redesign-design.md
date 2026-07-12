# AI/ML Engineer Portfolio Redesign

**Date:** 2026-07-12  
**Status:** Approved visual direction; specification awaiting final user review  
**Approved direction:** Engineer Dossier  
**Visual reference:** `/home/avisaha/.gstack/projects/sahaavi-sahaavi.github.io/designs/engineer-dossier-20260712/homepage-preview.html`

## 1. Purpose

Redesign Avishek Saha's portfolio so the first impression is an experienced AI and machine learning engineer, not the author of one maintenance-agent project.

The homepage must lead with professional experience, engineering range, and evidence. Public projects support that story by making selected technical decisions inspectable.

The redesign targets recruiters and hiring managers evaluating candidates for:

- Applied AI Engineer and AI Engineer roles
- Machine Learning Engineer roles
- Generative AI, RAG, agent, and AI-platform roles
- Relevant applied data science roles

## 2. Approved Product Decisions

1. Keep Hugo as the static-site generator.
2. Keep PaperMod for general content behavior, posts, taxonomies, and existing content compatibility.
3. Override the homepage, shared navigation, selected project presentation, and visual system where PaperMod is too generic.
4. Do not create a downloadable resume or a Resume navigation item.
5. Do not organize the personal brand around BCRTC-specific operational problems.
6. Do not let Maintenance-Eye or any other project dominate the homepage.
7. Lead with professional experience and engineering identity.
8. Position AI engineering first, ML engineering second, with data science as a supporting foundation.
9. Keep public claims mapped to approved evidence or inspectable public repositories.
10. Treat the approved HTML mockup as a visual reference, not production code to copy wholesale.

## 3. Positioning

### Primary identity

**Applied AI & ML Engineer**

### Hero-copy requirements

The final hero statement remains user-editable and requires explicit user approval before implementation. It must:

- Lead with AI and machine learning engineering
- Reflect experience building systems and producing outcomes
- Remain concise enough to scan in two or three lines
- Avoid leading with years of experience, Python, SQL, BCRTC, an operational domain, or a single project
- Avoid generic claims that are not supported by the experience and evidence sections

### Supporting statement

Working direction:

> My experience spans source-grounded LLM workflows, predictive models, evaluation systems, data and feature pipelines, APIs, and cloud delivery, with measured improvements in quality, efficiency, review effort, and decision support.

### Hero evidence line

- LLM systems, RAG, and evaluation
- Predictive ML and human review
- Measured quality and efficiency gains

Do not use a years-of-Python-or-SQL statement in the hero. Python and SQL remain supporting technical evidence in the engineering-range and experience sections. Exact quantified hero metrics may render only after explicit website-public approval; otherwise the hero uses the evidence-safe non-numeric signals above.

## 4. Audience and Questions Answered

### Recruiter scan

Within ten seconds, the homepage must answer:

- Who is Avishek?
- Which roles does he fit?
- Does he have professional experience?
- What is his education?
- Where is he based?
- Where can I inspect his work or contact him?

### Hiring-manager scan

Within two minutes, the homepage must answer:

- Has he worked across AI, ML, software, data, and cloud delivery?
- Does he understand evaluation, testing, guardrails, and human review?
- What did he own, contribute to, or support professionally?
- Which public systems can I inspect?
- Is the ML evidence more substantial than notebooks or coursework?

## 5. Information Architecture

### Primary navigation

1. Experience
2. Expertise
3. Selected Work
4. Writing
5. Contact

GitHub and LinkedIn remain visible in the footer and contact surfaces. Search is a utility, not a primary navigation item. Books must not appear in primary navigation until it contains substantive content.

### Homepage order

1. Identity and career signal
2. Professional experience
3. Engineering range and lifecycle
4. Selected public work
5. Writing, research, and education
6. Contact

### Supporting routes

- `/experience/`: canonical web-native professional profile
- `/projects/`: categorized work index
- `/projects/<slug>/`: technical case studies
- `/posts/`: technical writing
- `/#contact`: homepage contact section

The existing `/about/` URL redirects to `/experience/` through a Hugo alias. The source file may remain `content/about.md` during the first implementation, but its canonical public URL and navigation label are `Experience`.

Header destinations are explicit: `/experience/`, `/#expertise`, `/#work`, `/posts/`, and `/#contact`.

## 6. Homepage Design

### 6.1 Header

The header contains:

- `AS` monogram
- Avishek Saha
- Applied AI & ML Engineer descriptor on desktop
- Primary navigation
- Light/dark theme control

The header is sticky with a translucent background and one-pixel divider. It must not include a Resume button.

### 6.2 Hero

The hero uses an asymmetric two-column layout.

The left column contains:

- Role and location eyebrow
- User-approved AI/ML hero statement
- Experience-and-impact supporting statement
- `Explore experience`, `Selected work`, and `Contact` actions
- Three compact AI/ML evidence and impact signals

The right column contains an experience signal panel rather than a project image. It shows:

- BC Rapid Transit Company, Data & Applied AI Analyst
- Brain Station 23, Data Scientist, Applied AI
- University of British Columbia, Master of Data Science
- Softology IT, Co-Founder / Data Scientist

The panel may show Canada work authorization because it is a confirmed profile fact. It must not expose phone numbers or resume-download controls.

### 6.3 Experience

Professional experience appears before projects.

The current BCRTC role receives the largest treatment because it is current, not because BCRTC defines the site. The copy must balance applied AI, ML/data foundations, analysis, software integration, and business delivery.

Brain Station 23, Statistics Canada, and Softology appear as secondary experience cards. The approved visible titles are:

- `Data & Applied AI Analyst`
- `Data Scientist, Applied AI`
- `Capstone Data Scientist`
- `Co-Founder / Data Scientist`

Metrics must be scoped to the exact role and source. The initial homepage may use already-public claims while additional ledger claims await explicit website-disclosure approval.

Experience cards must state contribution level accurately. `Contributed to production Python services` must not become sole ownership of production systems.

### 6.4 Engineering Range

Four horizontally aligned evidence groups replace an unstructured skill dump:

1. **Applied AI systems:** LLM integration, RAG, tool workflows, structured outputs, source grounding, prompting, human review, and evaluation.
2. **Machine learning:** feature engineering, anomaly detection, ranking, calibration, temporal modeling, clustering, NLP, and reviewer feedback.
3. **Software and data:** Python, FastAPI, REST and WebSocket APIs, SQL, PostgreSQL, BigQuery, pipelines, contracts, and user-facing integration.
4. **Delivery and trust:** Docker, cloud deployment, CI, automated tests, observability, validation, approval boundaries, and documentation.

A five-step lifecycle visually connects the categories:

1. Data foundation
2. Model or retrieval
3. Evaluation
4. Software integration
5. Delivery loop

This lifecycle communicates engineering breadth without claiming every example was a production deployment.

### 6.5 Selected Work

The homepage contains two compact public-work rows:

- Maintenance-Eye
- GovIntel

They receive equal visual weight. Neither appears in the hero.

Each row contains:

- Public status
- Engineering category
- Concise problem and system description
- Repository and case-study links
- A small CSS or SVG system map

Maintenance-Eye must use the corrected evidence-safe description. It must not claim a multi-agent architecture or historical dataset counts that conflict with the current repository. It may describe nine guarded tool workflows, multimodal camera and voice input, FastAPI/WebSockets, human approval, cloud packaging, and automated tests.

GovIntel may describe asynchronous ingestion, PostgreSQL, hybrid retrieval, reranking, SQL analytics, structured outputs, and fail-closed citation validation. It must not present a coverage threshold as a measured coverage result.

### 6.6 Writing, Research, and Education

The final evidence section links:

- LLM Engineering From Scratch
- The interactive tokenizer work
- Relevant engineering articles
- Published ASD research
- UBC and AIUB education

The LLM series must be labeled as a lab or learning series while most planned projects remain incomplete. Research supports engineering credibility but does not replace current professional evidence.

### 6.7 Contact

The final call to action is direct and role-relevant:

> Building AI or ML systems that need engineering depth?

It links to email and exposes GitHub and LinkedIn. It must not include a portfolio chatbot, lead-generation form, phone number, or downloadable resume in the first release.

## 7. Visual System

### Aesthetic

**Technical editorial.** The site should feel authored, calm, and engineering-led. Typography, spacing, evidence labels, and diagrams create the AI/ML character. Decorative AI imagery does not.

### Decoration

**Intentional and restrained.** Use subtle grid lines, one-pixel dividers, small monospaced labels, and simple system diagrams. Avoid glowing neural networks, terminal loading screens, floating model logos, gradient buttons, glass-card walls, and decorative chat interfaces.

### Typography

- **Display and body:** Instrument Sans
- **Technical labels and metadata:** IBM Plex Mono
- **Fallback:** system sans-serif and system monospace stacks

Production fonts should be self-hosted as optimized WOFF2 assets with their license files. Use `font-display: swap`. Avoid runtime dependence on Google Fonts.

### Color tokens

#### Light

- Paper: `#F5F7F4`
- Surface: `#FFFFFF`
- Soft surface: `#EDF2F8`
- Primary ink: `#0D1726`
- Secondary ink: `#526071`
- Divider: `#D7DEE7`
- Strong divider: `#B8C3D1`
- Primary blue: `#245BDC`
- Dark blue: `#1643AD`
- Soft blue: `#E7EEFF`
- Cyan accent: `#0D8D9D`
- Success green: `#177A55`

#### Dark

- Paper: `#08111C`
- Surface: `#101B29`
- Soft surface: `#152235`
- Primary ink: `#ECF2F9`
- Secondary ink: `#A8B5C5`
- Divider: `#26364A`
- Strong divider: `#3E526C`
- Primary blue: `#78A2FF`
- Cyan accent: `#4CC0CC`
- Success green: `#62CF9F`

All foreground/background combinations must pass WCAG AA contrast. Dark mode must target PaperMod's `data-theme="dark"` behavior rather than a `.dark` class.

### Layout

- Maximum content width: `1180px`
- Desktop grid: 12 columns
- Tablet grid: 8 columns
- Mobile grid: 4 columns
- Minimum page gutter: `20px` desktop/tablet and `14px` mobile
- Primary section spacing: `104px` desktop, `74px` mobile
- Base spacing unit: `8px`
- Corner radii: `8px`, `14px`, and `22px`

Use cards only where grouping improves comprehension. Section structure should rely mainly on alignment, whitespace, and dividers.

### Motion

- Functional transitions only
- Hover and focus transitions: `160ms`
- Section entrance transitions, if retained: `220ms` to `300ms`
- No scroll-jacking, loading animation, parallax, autoplay video, or continuous decorative motion
- Respect `prefers-reduced-motion`

## 8. Hugo Architecture

### Preserve

- Hugo `0.147.x` compatibility
- PaperMod content conventions
- Markdown posts and project pages
- Existing GitHub Pages deployment
- RSS, taxonomies, and search output

### Homepage templates

`layouts/index.html` remains the homepage entry point but should delegate to focused partials:

- `layouts/partials/home/hero.html`
- `layouts/partials/home/experience.html`
- `layouts/partials/home/expertise.html`
- `layouts/partials/home/selected-work.html`
- `layouts/partials/home/writing-education.html`
- `layouts/partials/home/contact.html`

Each partial has one clear content responsibility. The homepage template only defines order and passes data.

### Structured content

Use Hugo data or page front matter instead of duplicating copy in templates.

Recommended data boundaries:

- `data/profile.yaml`: homepage identity, location, AI/ML evidence signals, and external links
- `data/experience.yaml`: homepage-visible roles and evidence-safe summaries
- Project front matter: status, role, category, year, repository, case-study metadata, system-map labels, and featured order
- Existing Markdown: long-form project and writing content

The portfolio data files are rendering inputs, not new evidence sources. Their claims must be copied from approved evidence and retain source references in comments or documentation.

### CSS

Split the current large custom stylesheet by responsibility while keeping Hugo's extended-CSS loading behavior:

- `assets/css/extended/portfolio-tokens.css`
- `assets/css/extended/portfolio-base.css`
- `assets/css/extended/portfolio-home.css`
- `assets/css/extended/portfolio-projects.css`

Home-specific styles must be scoped under homepage classes to prevent regressions in posts and project pages.

### JavaScript

PaperMod continues to control theme persistence. Add no frontend framework. Add small JavaScript only where semantic HTML and CSS cannot provide the interaction.

The first release requires no portfolio chatbot, client-side data fetching, animation library, or component runtime.

## 9. Content and Evidence Controls

1. Every visible claim must map to approved evidence or a public repository.
2. Resume renderability does not imply website-public approval.
3. Ownership verbs must match `owned`, `contributed`, `supported`, or `co-owned` evidence.
4. Every project must display stage: public demo, public repository, internal use, prototype, production contribution, academic, lab, or archived.
5. Do not claim four years of AI or ML experience.
6. Do not describe Maintenance-Eye as multi-agent until the public code supports that architecture.
7. Do not use the conflicting Maintenance-Eye asset/work-order counts.
8. Do not publish Pennymize, Centstep, unsupported ASD accuracy, Stock Analysis metrics, or future BCRTC targets.
9. Use the canonical visible role titles from the resume profile.
10. BCRTC-specific material must remain one experience source, not the site's brand umbrella.

## 10. Responsive Behavior

### Desktop, 1200px and above

- Hero uses a wide copy column and narrower experience panel.
- Navigation displays all primary links.
- Experience cards use a three-column secondary row.
- Engineering range uses four columns.
- Selected work uses metadata, copy, and diagram columns.

### Tablet, 641px to 1199px

- Hero stacks when space becomes constrained.
- Experience cards use two columns, then one full-width card.
- Engineering range becomes a two-by-two grid.
- Selected-work diagrams move beneath the copy when required.

### Mobile, 640px and below

- The role descriptor and navigation links collapse, retaining name and theme control.
- The hero becomes one column with readable line breaks.
- Actions use a two-column arrangement with Contact below when needed.
- All experience, expertise, and work content becomes one column.
- No horizontal scrolling is permitted at `320px`, `375px`, or `390px` widths.

## 11. Accessibility

- Semantic landmarks and ordered heading hierarchy
- Skip link and visible keyboard focus
- WCAG AA color contrast in both themes
- Accessible theme-toggle label and state
- System diagrams accompanied by accessible text
- No meaning communicated through color alone
- Minimum interactive target of approximately `44px`
- `prefers-reduced-motion` support
- Images use useful alternative text; decorative imagery uses empty alt text
- Link labels describe destinations rather than generic `Read More`

## 12. SEO and Social Presentation

- Homepage title: `Avishek Saha | Applied AI & ML Engineer`
- Homepage description focuses on AI engineering, ML systems, data/software foundations, and delivery
- Add a real local Open Graph image
- Use `ProfilePage` structured data with Avishek represented as the `Person` main entity
- Use `SoftwareSourceCode` or `CreativeWork` structured data for appropriate project pages
- Populate GitHub and LinkedIn in `sameAs`
- Remove obsolete keyword stuffing
- Preserve canonical URLs, RSS, sitemap, and robots behavior

## 13. Failure and Fallback Behavior

- Required homepage data must fail the Hugo build with a clear `errorf` message when missing.
- Optional metrics, diagrams, or external links must disappear cleanly when absent.
- Project cards must not render empty labels or dead controls.
- Local images are preferred. When an optional project image is missing, the layout uses a styled system map or text treatment instead of a broken remote image.
- External links open safely with `rel="noopener noreferrer"` where a new tab is used.
- Theme behavior must fall back to the system preference when no saved preference exists.

## 14. Verification Strategy

### Content and claims

- Check every homepage statement against the approved evidence matrix.
- Validate canonical titles and dates.
- Confirm no Resume or download control exists.
- Confirm project stage and ownership labels.

### Build and structure

- Run a clean Hugo build.
- Verify no template warnings introduced by custom overrides.
- Validate generated HTML.
- Verify internal links and required external links.
- Confirm draft and archived content is absent from output.

### Visual and accessibility

- Inspect at `1440x900`, `1024x768`, `768x1024`, `390x844`, `375x812`, and `320x568`.
- Test light and dark themes.
- Test keyboard navigation and focus order.
- Run automated accessibility checks.
- Verify contrast, text reflow, reduced motion, and browser zoom to 200%.

### Performance and metadata

- Check font loading and total page weight.
- Verify local responsive images.
- Confirm the Open Graph image returns `200`.
- Validate structured data and canonical metadata.
- Record a Lighthouse baseline before and after implementation.

## 15. Acceptance Criteria

The redesign is complete when:

1. The homepage identifies Avishek as an Applied AI & ML Engineer before mentioning any project.
2. Professional experience appears before selected work.
3. No project appears more than once on the homepage.
4. Maintenance-Eye receives no more visual weight than GovIntel.
5. AI engineering, ML engineering, software/data systems, and delivery quality are each visible.
6. The homepage contains no downloadable resume or Resume navigation item.
7. BCRTC is presented as current experience, not the brand theme.
8. The site remains Hugo-based and deploys through the existing workflow.
9. Posts, project routes, taxonomies, RSS, and existing public URLs continue to work.
10. Light and dark themes pass accessibility and responsive checks.
11. Visible claims pass evidence review.
12. The page has no horizontal overflow or browser-console errors at supported widths.
13. The hero contains no years-of-Python-or-SQL statement.
14. The hero evidence line foregrounds AI/ML work and impact rather than generic tenure or tool familiarity.

## 16. Explicit Non-Goals

- Migrating to React, Next.js, or another site framework
- Removing Hugo
- Rebuilding the blog engine
- Adding authentication or a backend
- Adding a portfolio chatbot
- Publishing proprietary or unapproved internal case studies
- Creating a downloadable resume
- Turning the homepage into a full resume transcript
- Rewriting every historical post in the first release
- Building a new CMS

## 17. Known Risks and Mitigations

| Risk | Mitigation |
|---|---|
| PaperMod styles leak into the new homepage | Scope homepage CSS and override only deliberate shared surfaces |
| Experience copy becomes a wall of text | Enforce line and bullet budgets; use hierarchy, metrics, and progressive disclosure |
| Skill lists become generic keyword dumps | Render four evidence groups and one lifecycle, not every tool |
| Public claims drift from the ledger | Maintain evidence references and review all copy before release |
| Project visuals dominate again | Cap selected work at two equal rows on the homepage |
| External assets break or slow the page | Self-host fonts and images; avoid runtime GitHub image dependencies |
| Dark mode regresses | Bind tokens to PaperMod's `data-theme` behavior and test both themes |
| Hugo templates become monolithic | Use focused partials and structured data boundaries |

## 18. Design Decisions Log

| Decision | Rationale |
|---|---|
| Engineer Dossier direction | Professional experience is stronger evidence than a project-gallery identity |
| Experience before projects | Recruiters and managers need career context before technical artifacts |
| Hugo and PaperMod retained | Existing publishing and deployment are sufficient; a framework rewrite adds no user value |
| Technical editorial aesthetic | Creates AI/ML character through information design rather than decorative AI tropes |
| Instrument Sans and IBM Plex Mono | Clear hierarchy with restrained technical metadata |
| Restrained blue/cyan palette | Communicates technology without the common purple-gradient aesthetic |
| No downloadable resume | User preference; the website provides the professional profile directly |
| Two equal selected-work rows | Keeps projects inspectable without allowing Maintenance-Eye to dominate |
| No BCRTC operating-problem umbrella | The portfolio represents a broader AI/ML engineering trajectory |
| No portfolio chatbot | It distracts from evidence and adds unnecessary runtime complexity |
