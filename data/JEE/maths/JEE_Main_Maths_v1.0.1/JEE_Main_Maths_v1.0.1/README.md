# JEE Main Mathematics: full bank v1.0.1

Prepared 8 October 2026 by Paper Tree Educational Studio. This is the errata release. It supersedes v1.0.0.

- Question IDs and key letters are the same as in v1.0.0. Every item that was not changed keeps its exact option order.
- 122 items had their stem or options corrected or rewritten (three of them were reworded a second time during re-verification). A further 10 items had only their integer-answer alternate changed. All 132 were re-solved independently and agreed with their keys.
- All corrections are listed one by one in `Errata_Closure_Register.csv` and summarised in `Errata_Report.html` (also as PDF).

Extract the whole folder and open **START_HERE.html**. Keep the `katex` folder where it is. The books use it to render the mathematics offline.

## Contents

- 2,700 four-option single-correct MCQs across all 14 NTA 2026 units.
- 810 Easy / 1,215 Medium / 675 Difficult (30 / 45 / 25 percent, the same proportions as Physics and Chemistry).
- 1,386 Class XI / 1,314 Class XII. (v1.0.0 had 1,350 / 1,350. The errata round moved 36 items to Class XI to match NCERT placement.)
- 675 keys per letter. Each unit is balanced to within one key per letter, no letter runs longer than 3, and no two units share a key sequence.
- 342 integer-answer alternates for Section B. These are alternate forms of existing questions, not extra items. Every one has a non-negative exact integer answer.
- 2,285 concept families, plus 116 alias dependencies, to control paper selection.

| Unit | Name | Questions | XI | XII | Numerical |
|---:|---|---:|---:|---:|---:|
| 1 | Sets, Relations and Functions | 140 | 60 | 80 | 18 |
| 2 | Complex Numbers and Quadratic Equations | 220 | 220 | 0 | 28 |
| 3 | Matrices and Determinants | 220 | 0 | 220 | 28 |
| 4 | Permutations and Combinations | 160 | 160 | 0 | 20 |
| 5 | Binomial Theorem and its Simple Applications | 140 | 140 | 0 | 18 |
| 6 | Sequence and Series | 180 | 180 | 0 | 23 |
| 7 | Limit, Continuity and Differentiability | 280 | 94 | 186 | 35 |
| 8 | Integral Calculus | 280 | 0 | 280 | 35 |
| 9 | Differential Equations | 140 | 0 | 140 | 18 |
| 10 | Co-ordinate Geometry | 300 | 300 | 0 | 38 |
| 11 | Three Dimensional Geometry | 140 | 22 | 118 | 18 |
| 12 | Vector Algebra | 160 | 0 | 160 | 20 |
| 13 | Statistics and Probability | 180 | 100 | 80 | 23 |
| 14 | Trigonometry | 160 | 110 | 50 | 20 |

## Files

- `jee_main_maths_v1.0.1.json`, `.jsonl` and `.csv`: the canonical bank. In the CSV, nested fields are JSON-encoded. Mathematics is LaTeX inline between `$...$`.
- `questions_only.json` and `answers_and_explanations.json`: the student and teacher exports.
- `books/Unit_NN_Student.html` and `books/Unit_NN_Teacher.html`: searchable, filterable, printable books for each unit, with KaTeX already rendered.
- `Sample_Paper.html` and `Sample_Solutions.html`: a 25-question Mathematics section from the full bank (seed 42).
- `generate_paper.py` and `Generator_Contract.md`: the paper generator. Example: `python generate_paper.py --bank jee_main_maths_v1.0.1.json --seed 7 --output practice7`. Add `--unit N` for a single-unit practice section.
- `question_bank_schema.json`, `coverage_map.json`, `family_register.json`, `question_index.csv`, `source_references.json`, `distractor_review.json`: structure, scope and the reasoning behind each wrong option.
- `evidence/`: machine-check source and results, blind re-solve results with adjudication, the editorial audit with every closure, key balancing, numerical checks and generator validation. `evidence/errata_v1.0.1/` holds the errata round: independent recomputation of every item, audit findings, batch closures, re-verification of changed items, the post-fix duplicate review and the automated test results.
- `Errata_Closure_Register.csv`, `Errata_Report.html` and `Errata_Report.pdf`: what the errata round found and how each finding was closed.
- `authoring/`: the full pipeline (drafting spec, harness, unit briefs, draft sources, build scripts), so the bank can be extended or corrected the same way.
- `verify_release.py`: reproduces the structural checks using only the Python standard library.
- `checksums.sha256`: file integrity list (the KaTeX assets are excluded).

## Conventions

Unless a question says otherwise:

- log_e is the natural logarithm. From v1.0.1 every natural logarithm is written log_e; a bare log appears nowhere in the bank.
- Arguments of complex numbers are principal values in (-pi, pi].
- Inverse trigonometric functions take principal values.
- [x] is the greatest integer function.
- The angle between two lines is the acute one.

## How each question was checked

1. **Machine recomputation.** 2,681 of the 2,700 items include a sympy routine that recomputes the answer from the givens in the stem. The routine also confirms that no distractor has the same value as the key. The other 19 are conceptual items. The harness also renders every string with KaTeX and checks the house style: no em or en dashes, no option letters in solutions, no control characters.
2. **Blind re-solve.** Separate solver agents, with no access to drafts or keys, solved every item from shuffled packs.
   - Unit 2 (pilot): 220 of 220 agreed. Every changed item was re-solved: 18 of 18 agreed.
   - Units 1 and 3 to 14: 2,476 of 2,480 agreed. Of the 4 disagreements, 3 were solver errors. The fourth (U07-A-055) found a genuine defect, and the item was corrected.
   - Every item changed after the audit was re-solved: 161 of 161 agreed.
3. **Editorial audit.** Separate auditor agents read every full record. They checked explanations, distractor rationales, ambiguity, scope, option-form cues, difficulty labels and near-duplicates.
   - The audit raised 193 findings: 1 blocking, 60 fix, 132 minor. Blind solvers raised 8 more issues.
   - Correcting agents resolved them: 199 fixed and 7 retained with reasons. 161 items had their stem or options changed.
   - A bank-wide duplicate scan then found one cross-unit duplicate, which was rewritten. Two related pairs were joined by alias dependencies so they are never selected together.
   - Everything is in `evidence/editorial_audit_closure.json`.
4. **Errata round (v1.0.1).**
   - *Independent recomputation.* Fresh verifier agents saw only the stem and options of all 2,700 items and wrote their own code for each (2,679 by code). They agreed with 2,699 keys. The one disagreement was a verifier error. All 342 integer answers agreed.
   - *Hostile unit audit.* Auditors read every full record unit by unit, looking for ambiguity, explanation errors, distractor defects, duplicates, metadata, scope and presentation. They raised 299 findings: 2 critical (two stems that let a second option be correct for an admissible value), 65 major and 232 minor.
   - *Closure.* 125 fixed, 73 rewritten, 93 resolved by alias links (related items that must not share a paper), 8 retained with reasons. Logarithm notation was unified across the bank.
   - *Re-verification.* All 132 items whose stem, options or integer alternate changed were rebuilt and recomputed by fresh verifiers. This pass caught an ambiguous phrase in two Unit 2 stems; the editor reworded those and a third stem with the same phrase, and all three then agreed. A post-fix duplicate review of the rewrites added one more alias link. Final result: 132 of 132 agree.
   - *Automated test suite.* `authoring/tests/test_release.py` runs 25 tests on the finished release folder: schema, IDs, options, export parity (JSON, JSONL, CSV, student and teacher exports), KaTeX rendering of every string, house style, books (no answers in student books, every ID present), rendered HTML, integer alternates, machine-check evidence, a full rebuild from the shipped sources, selection dependencies, key balance, stability against v1.0.0, the generator in both modes (seeds 0 to 1004, and 0 to 199 per unit, against an independent validator), the sample paper, checksums, the shipped verifier, links, the zip, duplicates, the option-length cue, a scope sweep and summary consistency. All 25 pass. A mutation check (defects deliberately injected into a copy) confirmed the tests catch what they target. Results are in `evidence/errata_v1.0.1/test_results.json` and `mutation_check.json`.
5. **Generator validation.** In full-bank mode, seeds 0 to 1004 all produce valid papers. In unit-practice mode, seeds 0 to 199 were tested for every unit.

All review was done by AI model agents. **No external human subject-expert review is claimed.** Difficulty labels are editorial estimates, not calibrated on students. Question IDs are project IDs, not NTA question numbers.

## Syllabus

The syllabus basis is NTA JEE Main 2026, read strictly. The main exclusions:

- Planes (the 3D syllabus lists lines only).
- Special series beyond AP, GP and AM-GM.
- Trigonometric equations, and heights and distances.
- Binomial distribution by name.
- Tangents and normals to conics.
- Scalar and vector triple products.
- Formation of differential equations.
- Parametric differentiation.

The full interpretation for each unit is in `coverage_map.json`. Questions are original, and none is attributed to a past paper. No figures were needed: every question is self-contained in text.
