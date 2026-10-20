You are the correcting editor for one batch of a JEE Main Mathematics question bank. You are told the batch prefix PP (e.g. U07-A). The draft file is /home/claude/jeemath/drafts/<pp lower-case, e.g. u07_a>.py, built with /home/claude/jeemath/qlib.py under the rules in /home/claude/jeemath/DRAFTING_SPEC.md (read it, including Special check patterns and Self-audit) and the scope in /home/claude/jeemath/briefs/UNN_scope.md. The batch quotas and classes are in /home/claude/jeemath/config/prompts/PP.md (the original drafting brief).

Findings to resolve: /home/claude/jeemath/verify/fix/PP.json (from an independent editorial audit and from blind solvers). For each finding:
- Re-verify it yourself first (print the full record, use sympy). If it is real, fix the record. If it is unfounded, retain the record and give the reason.
- Wrong key / two defensible options / ambiguity: change the stem or options so exactly one option is defensible, update check/values/explanation.
- Rationale that does not produce its distractor: rewrite the rationale so the named mistake truly gives that value, or replace the distractor (and its value) with one that a realistic mistake gives.
- Near-duplicate: rewrite the item named in the finding (the later one, or the one in this batch) into a genuinely different question on the same subtopic and difficulty, with a new concept family if appropriate.
- Out of scope: replace with an in-scope question of the same difficulty.
- Difficulty mislabel: keep the batch quotas exactly. Prefer making the item genuinely harder so the label is right; otherwise relabel it and make another item genuinely harder to compensate.
- Distractor ruled out on sight (violates a stated condition or range): replace it with a plausible in-range value from a real mistake.
- Control characters (TAB, form feed, backspace) come from non-raw strings: make every string with a backslash a raw string r"...".
- A numerical alternate with a negative integer answer: remove that numerical alternate (set numerical=None), keeping at least the minimum count from the brief.
- Policy decisions: derivative of one function with respect to another is allowed (chain rule). "Two circles touching" and scalar triple product / volume of tetrahedron are out of scope. Write "does not exist" and similar words as plain text, not math mode. Unit 9 items are all source_class "XII".

Then run: cd /home/claude/jeemath && python3 harness.py drafts/<file>.py --easy E --medium M --difficult D (quotas from the brief). The harness now also blocks control characters and KaTeX errors in rationales, misconceptions and difficulty reasons; fix every BLOCKING line, including ones not in the findings. Keep local IDs unchanged (edit in place; do not renumber).

Write /home/claude/jeemath/verify/fix/PP_closure.json: {"closures": [{"finding_id", "action": "fixed"|"retained", "note"}], "changed_stem_or_options": [local ids whose stem or any option text changed]}.
Report back in one line: harness summary line, number fixed, number retained, number of items with changed stem/options.
