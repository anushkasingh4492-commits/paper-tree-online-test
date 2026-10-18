# CAT Quantitative Ability question bank v1.0.0

Prepared 17 October 2026 by Paper Tree Educational Studio. The complete CAT QA bank: 3000 original CAT-style
questions in 28 chapters across Arithmetic, Algebra, Geometry, Number System and Modern Maths.

Extract the whole folder and open **START_HERE.html**. Keep the `katex` and `figures` folders where
they are; the books use them offline.

## At a glance

- 1950 MCQ (four options, one correct, +3 / -1) and 1050 TITA (type a whole number, +3 / 0): the 35 percent TITA share of the CAT QA section.
- 900 Easy / 1350 Medium / 750 Difficult (30 / 45 / 25 percent), labelled on the CAT scale.
- 155 geometry questions carry an SVG figure drawn to scale from the stem's data (never showing the unknown).
- MCQ keys balanced within each chapter, no letter run longer than 3.
- 1772 concept families plus 216 alias groups, so a generated paper never repeats a method.
- Exam reuse tags on every item (CAT always; XAT, NMAT, SNAP, CMAT, MAH-CET where suitable).

| Ch | Chapter | Area | Questions | TITA | Figures |
|---|---|---|---:|---:|---:|
| 01 | Percentages | Arithmetic | 175 | 62 | 0 |
| 02 | Profit, Loss and Discount | Arithmetic | 175 | 62 | 0 |
| 03 | Simple and Compound Interest | Arithmetic | 100 | 35 | 0 |
| 04 | Ratio, Proportion, Variation and Partnership | Arithmetic | 150 | 52 | 0 |
| 05 | Averages | Arithmetic | 100 | 35 | 0 |
| 06 | Mixtures and Alligations | Arithmetic | 100 | 35 | 0 |
| 07 | Time and Work | Arithmetic | 150 | 52 | 0 |
| 08 | Time, Speed and Distance | Arithmetic | 250 | 88 | 0 |
| 09 | Linear Equations | Algebra | 140 | 49 | 0 |
| 10 | Quadratic Equations and Polynomials | Algebra | 130 | 46 | 0 |
| 11 | Inequalities and Modulus | Algebra | 120 | 42 | 0 |
| 12 | Logarithms, Surds and Indices | Algebra | 110 | 38 | 0 |
| 13 | Progressions and Series | Algebra | 130 | 46 | 0 |
| 14 | Functions, Graphs and Maxima/Minima | Algebra | 120 | 42 | 0 |
| 15 | Lines, Angles and Triangles | Geometry | 120 | 42 | 32 |
| 16 | Circles | Geometry | 90 | 32 | 33 |
| 17 | Quadrilaterals and Polygons | Geometry | 70 | 24 | 27 |
| 18 | Mensuration | Geometry | 90 | 32 | 34 |
| 19 | Coordinate Geometry | Geometry | 50 | 17 | 19 |
| 20 | Trigonometry and Heights and Distances | Geometry | 30 | 11 | 10 |
| 21 | Factors, Divisibility, HCF and LCM | Number System | 90 | 32 | 0 |
| 22 | Remainders and Modular Arithmetic | Number System | 70 | 24 | 0 |
| 23 | Unit Digits, Bases and Trailing Zeros | Number System | 60 | 21 | 0 |
| 24 | Digits, Integer Solutions and Number Properties | Number System | 80 | 28 | 0 |
| 25 | Permutations and Combinations | Modern Maths | 110 | 38 | 0 |
| 26 | Probability | Modern Maths | 80 | 28 | 0 |
| 27 | Set Theory and Venn Diagrams | Modern Maths | 60 | 20 | 0 |
| 28 | Basic Statistics | Modern Maths | 50 | 17 | 0 |

## Files

- `cat_qa_v1.0.0.json`, `.jsonl` and `.csv`: the canonical bank (schema v2). In the CSV, nested fields are JSON-encoded. Mathematics is LaTeX inline between `$...$`.
- `questions_only.json` and `answers_and_explanations.json`: the student and teacher exports.
- `books/Chapter_NN_Student.html` and `books/Chapter_NN_Teacher.html`: a searchable, filterable, printable pair for every chapter. The teacher book shows keys, worked solutions, the misconception each item targets and, for TITA, the common wrong entries.
- `figures/`: the SVG figure files referenced by the `figures` field of each record.
- `Sample_Paper.html` and `Sample_Solutions.html`: a 22-question, 40-minute CAT-style section (seed 42).
- `generate_paper.py` and `Generator_Contract.md`: the paper generator. Example:
  `python generate_paper.py --bank cat_qa_v1.0.0.json --seed 7 --output practice7`.
  Options: `--questions`, `--tita`, `--chapter 8`, `--area Algebra`, `--exam XAT`, `--minutes`.
- `question_bank_schema.json`: schema v2 (MCQ and TITA, exam tags, figures, and a `set_id` reserved for VARC passages and DILR sets).
- `coverage_map.json`, `family_register.json`, `question_index.csv`, `distractor_review.json` (the error behind every wrong option and every common TITA wrong entry).
- `evidence/`: machine checks with source code, all blind re-solve rounds with adjudication, the editorial audits, closures, chapter sweeps and lead-editor decisions, key balancing and the automated test results.
- `authoring/`: the full pipeline (drafting spec, briefs, draft sources, harness, figure library, build scripts, prompts, tests), so the bank can be extended or corrected the same way.
- `Build_Report.html`: chapter table and verification summary.
- `verify_release.py`: reproduces the structural checks with the Python standard library only.

## How it was verified

1. Every answer is recomputed by code from the givens in the stem, and every MCQ distractor is confirmed distinct from the key.
2. Blind re-solve of all 3000 questions by solvers who never saw the keys (2993 agreed in round 1; every disagreement adjudicated in `evidence/blind_resolve_results.json`). Every changed item was solved again by two separate solver sets and the final edits once more (1297/1300 agreed).
3. Hostile editorial audit of every item, correction under lead-editor decisions, then a post-fix sweep of every chapter for changed items and duplicates.
4. 10/10 automated tests pass (`authoring/tests/test_release.py`): schema, full rebuild reproducibility, harness on every draft, machine checks, KaTeX rendering of every string, export parity, no answer leakage, 200 generator seeds, and a mutation test.

## Conventions

- Units are those stated in each stem; TITA stems always name the unit. Areas and volumes are written cm$^2$, m$^3$ and so on.
- Clock times are written like 9:00 am. Money is written Rs. 1,200.
- Unless a question says otherwise, rates and speeds are constant and people start at the same time.
- Difficulty labels are editorial estimates; recalibrate them with student attempt data.
