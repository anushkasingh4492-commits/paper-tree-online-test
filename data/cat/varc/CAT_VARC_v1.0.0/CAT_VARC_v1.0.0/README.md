# CAT VARC question bank v1.0.0

Prepared 18 October 2026 by Paper Tree Educational Studio. The complete CAT Verbal Ability and Reading Comprehension bank:
2800 original questions in 12 chapters, built on the same pipeline as the CAT QA bank v1.0.0.

Extract the whole folder and open **START_HERE.html**.

## At a glance

- 400 original reading passages (300 four-question passages of 400 to 512 words; 100 five-question passages of 572 to 650 words) carrying 1700 RC questions, in 8 subject domains.
- 1100 verbal ability items: 350 para jumbles, 350 para summaries, 250 odd sentence out, 150 sentence placement.
- 2200 MCQ (+3 / -1) and 600 TITA (+3 / 0). TITA answers are digit strings: a para jumble is keyed like 3142, an odd sentence out like 4.
- 840 Easy / 1260 Medium / 700 Difficult (30 / 45 / 25 percent), on the CAT scale.
- Every wrong option carries a written reason why it is wrong; every para jumble and odd-one-out lists the most common wrong entries.
- MCQ letters balanced within each chapter (no run longer than 3, no letter more than twice in one passage).
- Exam reuse tags on every item (CAT always; XAT, NMAT, SNAP, CMAT, MAH-CET where suitable).

| Ch | Chapter | Area | Questions | Passages | TITA | Easy / Medium / Difficult |
|---|---|---|---:|---:|---:|---|
| 01 | Philosophy and Ethics | Reading Comprehension | 238 | 56 | 0 | 77 / 112 / 49 |
| 02 | Psychology and Cognitive Science | Reading Comprehension | 204 | 48 | 0 | 63 / 96 / 45 |
| 03 | Society, Anthropology and Culture | Reading Comprehension | 238 | 56 | 0 | 70 / 107 / 61 |
| 04 | History and Politics | Reading Comprehension | 204 | 48 | 0 | 60 / 90 / 54 |
| 05 | Economics, Business and Development | Reading Comprehension | 238 | 56 | 0 | 70 / 105 / 63 |
| 06 | Science, Environment and Technology | Reading Comprehension | 238 | 56 | 0 | 70 / 105 / 63 |
| 07 | Arts, Literature and Aesthetics | Reading Comprehension | 204 | 48 | 0 | 60 / 90 / 54 |
| 08 | Language, Media and Communication | Reading Comprehension | 136 | 32 | 0 | 40 / 60 / 36 |
| 09 | Para Jumbles | Verbal Ability | 350 |  | 350 | 105 / 158 / 87 |
| 10 | Para Summary | Verbal Ability | 350 |  | 0 | 105 / 157 / 88 |
| 11 | Odd Sentence Out | Verbal Ability | 250 |  | 250 | 75 / 113 / 62 |
| 12 | Sentence Placement | Verbal Ability | 150 |  | 0 | 45 / 67 / 38 |

## Files

- `cat_varc_v1.0.0.json`: the canonical bank (schema v2): `meta`, `sets` (passages) and `questions`. RC questions link to their passage by `set_id`.
- `cat_varc_v1.0.0_questions.jsonl/.csv` and `cat_varc_v1.0.0_passages.jsonl/.csv`: the same data, one record per line or row (nested fields JSON-encoded in CSV).
- `questions_only.json` and `answers_and_explanations.json`: student and teacher exports.
- `books/Chapter_NN_Student.html` and `Chapter_NN_Teacher.html`: searchable, filterable, printable books. RC books show each passage with its questions; teacher books add answers, explanations, the reason each wrong option fails and the common misconception.
- `Sample_Paper.html` and `Sample_Solutions.html`: a 24-question, 40-minute CAT-style VARC section (4 passages x 4 questions, 2 para jumbles, 3 para summaries, 2 odd sentence out, 1 sentence placement; seed 42).
- `generate_paper.py` and `Generator_Contract.md`: the paper generator (whole passages only). Example:
  `python generate_paper.py --bank cat_varc_v1.0.0.json --seed 7 --output practice7`.
- `question_bank_schema.json`, `verify_release.py` (checks the release, including generator seeds 1 to 200).
- `coverage_map.json`, `family_register.json`, `question_index.csv`, `distractor_review.json`.
- `evidence/`: blind solving rounds, the editorial audit, originality checks, key balance and test results.
- `authoring/`: the full pipeline (drafting library, harness, spec, briefs, prompts, every drafting file, every verification file).

## For the CBT platform

- Passages are set records. A passage must be shown in a split-screen view beside its questions, and a paper must take whole passages.
- Para jumble answers are compared as exact digit strings; odd sentence out as a single digit. Sentence placement is an MCQ whose options are Blank (1) to Blank (4).
- `family_dependencies`: never put two units that share any entry into one paper (the generator enforces this).

## Verification

- Round 1: every item solved blind by two independent solvers who saw only the student view; both matched the key on 2797 of 2800. The 3 disagreements were adjudicated (two typing slips, one para jumble with a second defensible order, rewritten).
- Editorial audit of every file: 5 critical, 94 major, 734 minor findings; every critical and major finding fixed.
- Round 2: the 257 items whose student-facing content changed were solved blind again by two new solvers; both matched the key on 257 of 257.
- Originality: all passages and items are newly written; every file checked against every other for shared 8-word runs, with no blocking overlap left; a 60-sentence web spot check found no published match.
- 9/9 automated tests pass.
- Not yet done: a human subject-expert review (`human_subject_expert_reviewed` is false on every record) and difficulty calibration with student data.
