You are an independent verifier for a released JEE Main Mathematics question bank (errata pass). You get one pack: /home/claude/jeemath/errata/packs/PP.json (PP is given in your task). Each entry has id, question (LaTeX), options A-D, and sometimes numerical_question (an integer-answer version with no options).

STRICT INDEPENDENCE: read ONLY that pack file. Do not open anything else under /home/claude/jeemath (no drafts/, release/, build/, blind/, verify/, config/ other than this prompt, no keys), nor /root or /tmp. Your value comes from not having seen the authors' answers or code.

For EVERY question:
1. Solve it yourself.
2. For every question with any computation, write and RUN your own Python/sympy code that computes the answer directly from the stem's data (solve, integrate, diff, limit, Matrix, brute-force enumeration with itertools for counting/probability, numeric spot checks for identities, etc.). Then evaluate EACH of the four options numerically/symbolically and decide which option(s) equal your result. Do not trust your mental arithmetic alone.
3. For purely conceptual/statement items, reason carefully; where possible test statements with counterexample searches in code.
4. If numerical_question is present, compute its integer answer independently (it may ask for a scaled quantity such as 4k; read it carefully).

Put all your code in /home/claude/jeemath/errata/recompute/PP_work.py (it may be long; organise per id). Run it.

Write /home/claude/jeemath/errata/recompute/PP.json: a JSON list, one object per question:
{"id", "choice": "A"|"B"|"C"|"D"|null, "matching_options": [letters whose value equals your computed answer], "numerical_answer": int or null, "method": "code"|"reasoning", "computed": "<your value, short>", "confidence": "high"|"medium"|"low", "issue": "<empty, or a concrete defect: no option correct, two options correct, ambiguous stem, missing condition, numerical stem ambiguous, out of JEE Main level, LaTeX that would render wrongly, etc.>"}
matching_options must list EVERY option that is mathematically equal to the correct answer (normally exactly one). Use null choice only if no option is correct.

Report back in one line: count, how many with method=code, number with matching_options != 1 element, number with non-empty issue.
