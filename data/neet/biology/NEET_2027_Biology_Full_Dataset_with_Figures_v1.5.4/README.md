# NEET 2027 Biology Full Dataset with Figures v1.5.4

Status: PASS / upload-ready

This bank is designed for the NEET 2027 student cohort whose two-year senior-secondary cycle spans 2025-27. It does not claim that a separately published NEET-UG 2027 syllabus exists. Scope is locked to the latest official NMC/NTA NEET-UG Biology syllabus available at build time (NEET-UG 2026, issued for the 2026-27 academic session).

## Source basis

- Official NMC/NTA NEET-UG 2026 Biology syllabus, Units 1-10.
- NCERT Biology Class XI, Revised Edition November 2022; cohort study year 2025-26, verified against the official 2026-27 reprint of the same revised edition.
- NCERT Biology Class XII, Revised Edition November 2022, Reprint 2026-27.
- No separate official NCERT Biology corrigendum for these reprints was located on the NCERT site during the source audit. Corrections incorporated in the official reprints govern.

When NMC/NTA publishes the NEET-UG 2027 syllabus, run a syllabus-delta audit before continuing production use.

## Release summary

- Questions: 2160
- NCERT chapters represented: 32
- Difficulty: 720 Easy, 720 Medium, 720 Difficult
- Correct options: 540 each of A, B, C and D
- Figure-linked questions: 45
- Figure assets: 26
- Pre-release corrections completed: 1519
- Unresolved errors: 0

Every question is a four-option, single-correct-answer MCQ with +4/-1/0 marking. `questions_only.json` omits answer fields; `answers_and_explanations.json` provides keyed answers and explanations. `schema_and_generator_contract.json` defines the record contract. `independent_validation.json` records the second-pass delivery-gate checks.

## Manifest convention

`manifest.json` hashes every other packaged file. A file cannot contain its own final SHA-256 without changing that hash, so the manifest records this standard self-reference exception explicitly. The final ZIP hash is reported at delivery.
