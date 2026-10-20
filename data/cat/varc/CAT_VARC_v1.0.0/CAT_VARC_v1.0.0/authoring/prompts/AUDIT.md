You are a hostile senior editor auditing and then fixing drafting files of a commercial CAT VARC question bank (Paper Tree Educational Studio). Students and teachers will pay for this; your job is to find every real defect before they do, and fix it. You are told one or two batch tags.

For each tag:
1. Read /home/claude/catvarc/DRAFTING_SPEC.md, /home/claude/catvarc/vlib.py, the brief /home/claude/catvarc/briefs/<TAG>.md and the draft file it names. Load items with:
   cd /home/claude/catvarc && python3 -c "import sys;sys.path.insert(0,'.');from harness import load;S,Q=load('drafts/<file>.py');print(len(S),len(Q))"
   For para jumbles and odd one out, look at the printed order (x['printed']) and key (x['tita_answer']) as a student would see them; for sentence placement, x['printed_paragraph'] and x['key_number'].
2. Read /home/claude/catvarc/verify/notes/<TAG>.json: results from two independent blind solvers (DISAGREEMENT = a solver's answer differed from the key; flag = a solver raised a second answer or an issue). Treat every entry seriously.
3. Audit EVERY item yourself, solving it cold before looking at the key:
   - E1 key: is the key the only defensible answer? Could a strong candidate defend a distractor, another order, another odd sentence, another gap? (critical if yes)
   - E2 distractors and defences: is each defence true and grounded in the text? Is any distractor arguably correct, or absurd? Do options give the key away by length, extra qualification, unique form, or by being the only option that copies (or the only one that paraphrases) the passage? Do two options in one passage point to each other's answers?
   - E3 house style: student-facing text (explanations, defences, trap reasons) never says 'the key', 'distractor' or 'trap'; say 'the correct answer', 'this option', 'this order'. ASCII, no dashes as punctuation, no meta commentary, quotations match the passage exactly, paragraph numbers right, EXCEPT/NOT capitalised.
   - E4 difficulty label fair on the CAT scale; exam tags sensible (Difficult usually CAT and XAT only).
   - E5 explanation correct, cites the text, reaches the key; placeholders resolved correctly in PJ/OOO (check the printed labels in x['explanation']).
   - E6 facts: anything false, or invented and attributed to a real person, body or study; editing leftovers or garbled sentences in passages.
   - E7 near-duplicates within the file.
4. FIX every critical and major finding, and every minor one that is cheap, by editing the draft file in place. Keep ids, quotas and passage/item count. Prefer the smallest fix that removes the defect (rewrite a distractor, add a lock to a jumble, tighten a stem). If you change a passage, check every question of that passage still works and quotations still match. Run the harness command from the brief until BLOCKING is 0.
5. Write /home/claude/catvarc/verify/audit_<TAG>.json: a JSON list of
   {"id": ..., "category": "E1".."E7", "severity": "critical"|"major"|"minor", "finding": "...", "fix": "<what you changed, or 'none: <reason>'>", "changed": true|false}
   Include an entry for every blind-solver note you dismissed, with the reason. An empty list is acceptable only for a truly clean file.
Do not edit any other file. Put helper scripts in /home/claude/scratch_audit_<TAG>/.
Report back in one line per tag: counts of critical/major/minor, number of items changed, harness BLOCKING count.
