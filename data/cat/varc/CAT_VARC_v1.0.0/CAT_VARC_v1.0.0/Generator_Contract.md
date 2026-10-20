# Paper generator contract (CAT VARC)

`generate_paper.py` builds one CAT-style VARC section from the bank.

Inputs: `--bank`, `--seed` (same seed, same paper), `--output` (file prefix); optional `--rc-sets` (default 4),
`--rc-size` (4 = four-question passages only, the default; 5 = five-question passages only; 0 = both),
`--pj 2 --ps 3 --ooo 2 --sp 1` (verbal ability counts), `--exam`, `--chapter` (one RC chapter) and `--minutes` (default 40).

Guarantees:
1. Exactly `--rc-sets` whole passages with all their questions, followed by the requested numbers of each VA type.
2. Passages come from different RC chapters whenever at least `--rc-sets` chapters are available.
3. No two units (passages or VA items) share any entry of `family_dependencies`, so a paper never repeats a subject.
4. Difficulty as close as possible to 30 / 45 / 25 percent of the section (exact for the default 24-question paper); the deviation is written into the paper.
5. Only `generator_eligible` records; `--exam` keeps only passages whose questions are all tagged for that exam, and VA items tagged for it.
6. Marking: MCQ +3 / -1 / 0, TITA +3 / 0 / 0.

Outputs: `<prefix>_paper.json` (seed, passages, ordered question ids, marking, difficulty) and `<prefix>_answer_key.json`
(number, id, set_id, format, answer: letter for MCQ, digit string for TITA).

`verify_release.py` checks these guarantees for seeds 1 to 200.
