# Paper Tree student dark-mode consistency fix

This patch contains only changed/new files and preserves the repository's folder structure.

## Changes
- Persists and synchronizes the saved student theme across dashboard, tests, results, history, statistics and test-summary routes.
- Applies dark styles to light backgrounds, text, borders, inputs and report summary panels.
- Explicitly fixes both earned and unearned badge cards, including the pale gradient used for locked badges.
- Does not alter test scoring, submission, academy permissions, or badge-award logic.

## Apply
Extract this ZIP into the repository root, then run `npx tsc --noEmit`, `git diff --check`, and your normal production build. Verify dark mode on `/dashboard`, `/test/<id>`, `/test/result/<id>`, `/tests/test-summary`, `/test-summary`, `/history`, and `/stats`.
