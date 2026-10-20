You are the correcting editor for one batch of a released JEE Main Mathematics bank, in an errata round (v1.0.0 -> v1.0.1). Batch prefix PP is given in your task (e.g. U07-A). Draft file: /home/claude/jeemath/drafts/<pp lower-case, e.g. u07_a.py>, built with /home/claude/jeemath/qlib.py under /home/claude/jeemath/DRAFTING_SPEC.md (read it, including Special check patterns and Self-audit). Scope: /home/claude/jeemath/briefs/UNN_scope.md. Quotas: /home/claude/jeemath/config/prompts/PP.md.

Findings: /home/claude/jeemath/errata/fix/PP.json (from an external errata audit). Findings cite released IDs (JEE-MATH-Uxx-nnn); each finding has owner_local_id (the record in YOUR file to act on) and related_local_ids. /home/claude/jeemath/errata/id_map.json maps released IDs to local IDs. To read a local record: cd /home/claude/jeemath && python3 -c "import sys; sys.path.insert(0,'.'); from harness import load; [print(x) for x in load('drafts/FILE.py') if x['local_id']=='LOCAL']".

Rules:
- Re-verify every finding yourself (sympy). Fix real ones; retain unfounded ones with a reason.
- critical (two defensible options / wrong key): change stem or options so exactly one option is defensible for EVERY admissible case; update check, values, explanation.
- E6 duplicates/near-duplicates: if the owner item repeats another item's task with the same data, the same answer, or gives/gets the other's answer directly, REWRITE the owner item into a genuinely different question on the same subtopic and difficulty (new numbers AND a different unknown or twist), with a new concept family. If it is only a related task, do NOT rewrite; instead request an alias link (see closure file). When unsure, prefer rewriting for "major" and aliasing for "minor".
- E3 explanation errors: fix the explanation. Explanations must never refer to options by position ("the last option", "the first") or letter; refer to values.
- E5: rewrite the rationale so the named slip yields exactly that option, or replace the distractor (and its value) with one a real slip yields; options must not be ruled out on sight.
- E7: correct metadata. source_class follows NCERT placement: modulus/greatest-integer/signum graphs, real functions, limits, derivatives by first principles and product/quotient rules, 3D coordinates/distance/section formula are Class XI; continuity/differentiability, chain/implicit/inverse-trig differentiation, applications of derivatives, direction cosines and lines in space are XII. Difficulty: keep the batch quotas exactly; prefer making the item genuinely harder, otherwise relabel and compensate with another item made genuinely harder. question_type should fit the item.
- E8 scope rulings: translated (shifted) standard conics are in scope; trigonometric equations solved in an interval are OUT of scope (replace the item); explanations must not rely on out-of-unit tools (rewrite the explanation).
- E9: fix wording and LaTeX (wrap maths and numbers in $...$ in explanations, rationales, misconceptions, difficulty reasons). IGNORE log-notation findings (the editor unifies \log notation bank-wide afterwards).
- Keep local IDs unchanged; edit in place; raw strings r"..." for anything with a backslash.

Then run the harness with your quotas (python3 harness.py drafts/<file>.py --easy E --medium M --difficult D) and clear every BLOCKING line.

Write /home/claude/jeemath/errata/fix/PP_closure.json:
{"closures": [{"finding_id": <released id from the finding>, "category", "severity", "action": "fixed"|"rewritten"|"aliased"|"retained", "note"}],
 "changed_stem_or_options": [local ids whose stem or option text changed],
 "alias_requests": [[local_id_1, local_id_2, ...], ...]   (groups that must never appear in the same paper; may include ids from other batches of the same unit)}
Report back in one line: harness summary, and counts of fixed / rewritten / aliased / retained.
