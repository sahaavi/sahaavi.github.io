# Homepage Copy Refinement

## Goal

Make three targeted homepage copy adjustments without changing the approved layout, visual system, information architecture, or content elsewhere.

## Approved Changes

1. Change the hero identity line from `Applied AI & ML Engineer · Vancouver, BC` to `Applied AI & ML Engineer · Canada`.
2. Change the middle hero action label from `Selected work` to `Projects`. Keep its existing `/#work` destination so it continues to move visitors directly to the homepage project section.
3. Remove `Canada work authorized` from the `Experience at a glance` panel without replacement. Remove the now-unused profile field and its template validation rather than hiding the text with CSS.

## Scope Boundaries

- Do not change the hero statement, supporting paragraph, evidence signals, experience timeline, navigation labels, project content, or page layout.
- Do not add a replacement badge or new visual element to the career panel.
- Do not change professional-role locations on the Experience page.
- Preserve Hugo and PaperMod.

## Verification

- Update homepage contract tests to require the new hero location and action label.
- Verify the rendered homepage no longer contains `Canada work authorized`.
- Run the focused homepage tests and a warning-strict Hugo production build.
