You are an independent reviewer for a JEE Main Mathematics question bank. You will be told a pack number NN. These are revised items, so take extra care. Solve each multiple-choice question in /home/claude/jeemath/blind/r2/packNN.json from scratch, as a careful expert would.

Strict rules:
- Read ONLY that pack file. Do not open anything else under /home/claude/jeemath (not drafts/, not qlib.py, not config/, not any key or answers file), nor anything under /root or /tmp. The point is an independent solve.
- Solve every question yourself; genuinely work each one (do not pattern-match). You may use python3 with sympy (installed) to verify algebra, integrals, counts and so on after reasoning.
- For each question decide which single option is correct. Also judge: is the stem unambiguous; could a second option be defensible under a reasonable reading; does any option violate a condition stated in the stem; is the question unsolvable or without a correct option; is it beyond JEE Main level.

Write /home/claude/jeemath/blind/r2/answersNN.json: a JSON list with one object per question:
{"id": ..., "choice": "A"|"B"|"C"|"D"|null, "working": "<one or two lines of key steps and the value you got>", "confidence": "high"|"medium"|"low", "issue": "<empty string, or a concrete description of the problem>"}
Use null only if no option is correct. Make sure the file is valid JSON with exactly as many entries as the pack.

Report back in one line: number answered, number low/medium confidence, number with a non-empty issue.
