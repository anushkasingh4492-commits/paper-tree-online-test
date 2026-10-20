# JEE Main Mathematics bank: drafting spec (read fully before writing)

You are authoring part of a commercial JEE Main Mathematics question bank for Paper Tree
Educational Studio. It sits beside finished JEE Main Physics and Chemistry banks that went through
several rounds of external errata audit. Your questions will be machine-checked, then re-solved
blind by a separate reviewer who does not see your key. Every disagreement costs a correction
round, so be exact.

Syllabus basis: NTA JEE Main 2026, Paper 1 Mathematics. Stay strictly inside the topics listed in
your brief. Anything outside it (even if NCERT covers it) is out of scope.

## Output

Write ONE Python file at the path in your brief. Start it with exactly:

```python
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
```

Then call `q(...)` once per question. Read `/home/claude/jeemath/qlib.py` for the signature and
field meanings, and `/home/claude/jeemath/drafts/_sample.py` for two worked examples.
Local IDs are `<PREFIX>-001`, `<PREFIX>-002`, ... in order, with the prefix from your brief.

## The four rules that matter most

1. **Option text is only the answer.** The reason a distractor is wrong goes in the rationale
   field, never in the option. A student reading the four options must not be able to tell which is
   correct. Options are parallel in form and similar in length (all exact surds, or all intervals,
   or all short statements).
2. **Every computational question has a machine check.** `check` is a function that recomputes the
   answer FROM THE GIVENS IN THE STEM using sympy (solve, roots, simplify, Abs, arg, re, im,
   Poly, nroots, solveset, summation, etc.). Do not just `return` the answer you already know;
   actually compute it. `values` gives the sympy value of each option, correct first. The harness
   fails the item if check() differs from values[0] or if any distractor value equals the key.
   For "number of solutions / number of integral values" questions, compute the count. For interval
   answers use sympy `Interval`/`Union`; for sets use `FiniteSet`; for true/false, Python bools.
   Only purely conceptual or statement items may have `check=None`; if a statement item involves
   any computation, check the computation and return a tuple of truth values, e.g.
   `values=[(True, False), (True, True), (False, False), (False, True)]`.
3. **Exactly one option is defensible.** Before keeping an item, ask: under any reasonable reading
   of the stem, could a second option also be right? Could the keyed one be wrong? State every
   convention that matters (principal argument in $(-\pi,\pi]$, real coefficients, $a \ne 0$, $z \ne 0$,
   distinct roots, etc.) inside the stem.
4. **Never name option letters** in the explanation ("option C", "(B)"). Refer to values.
   Never label things in the stem A, B, C or D; use P, Q, R, S or $z_1, z_2$.

## Notation (LaTeX, rendered with KaTeX)

- All mathematics inline with `$...$`. Never `$$`. Use Python raw strings `r"..."`.
- Pure ASCII source only. No Unicode maths symbols, no curly quotes, and **no em dash or en
  dash anywhere** (house rule). Use commas, semicolons or separate sentences.
- Imaginary unit `i`. Conjugate `\overline{z}`. `\operatorname{Re}(z)`, `\operatorname{Im}(z)`,
  `\arg(z)`, `|z|`. Fractions `\frac{}{}`, roots `\sqrt{}`, `\sqrt[3]{}`. Intervals like
  `$(-\infty, 2) \cup (3, \infty)$`. Sets `$\{1, 2\}$` (escape braces). `\in`, `\mathbb{R}`, `\mathbb{C}`.
- Write numbers in options in simplest exact form ($\frac{3}{2}$, $2\sqrt{3}$), never long decimals.
- Stems end naturally: "...then $|z|$ equals", "...is", or a full question with "?".

## Difficulty (editorial, JEE Main scale)

- **Easy**: one idea, one or two steps, under a minute. Still JEE-flavoured, not school drill.
- **Medium**: typical JEE Main question; two to four steps or two ideas combined; 1.5 to 2.5 min.
- **Difficult**: upper end of JEE Main shifts; several ideas, a non-obvious route, a trap, or
  casework; about 3 minutes. Not JEE Advanced. Must be solvable without a calculator.

`difficulty_reason` says concretely why (steps, ideas combined, trap). `cognitive`:
Recall, Understanding, Application or Analysis.

## Question types (use these exact strings)

Direct concept MCQ; Single-step computation MCQ; Multi-step computation MCQ;
Inverse/parameter MCQ (find the parameter that makes a condition true);
Conceptual/application MCQ; Statement-based MCQ; Graph/diagram MCQ.

Statement-based items use the current JEE Main format: "Statement I: ... Statement II: ...
In the light of the above statements, choose the correct answer." with the four options
"Both Statement I and Statement II are true", "Both Statement I and Statement II are false",
"Statement I is true but Statement II is false", "Statement I is false but Statement II is true".
Use about 6 to 8 percent statement items. Vary which combination is correct.

## Distractors

Each distractor must be the result of a specific, realistic student error (sign slip, wrong
quadrant for the argument, forgetting the $a \ne 0$ case, double counting, using $\alpha\beta$ for
$\alpha+\beta$, dropping a root that fails a domain condition, etc.). Name that error in the
rationale. No silly or obviously impossible values. No two options with equal value.
- Every distractor must satisfy every condition stated in the stem (if the stem says $k > 0$,
  all four options are positive; a range of a positive function contains no negatives).
- Options must be mutually exclusive descriptions ("real and distinct" vs "real and irrational"
  overlap; do not pair them).
- Rationales are checked: the mistake you name must actually produce that exact value. Write the
  maths in rationales and misconceptions with $...$ LaTeX too, never plain "alpha beta" or "sqrt(x)".

Banned: "None of these", "All of the above", "Both ... and ...", "Cannot be determined".

## Variety and families

- `family` (concept_family) is a slug like `U02-arg-quadrant`. Items testing the same method
  with different numbers share a family; **at most 3 items per family**, and aim for many more
  families than that (the paper generator picks at most one item per family).
- Do not write near-copies. Vary the context, reverse the unknown, combine with another idea,
  use a limiting case, or target a different misconception.
- Write original questions. Do not reproduce a past JEE paper question word for word; you may
  use well-known JEE patterns with your own numbers and framing.

## Numerical (integer-answer) alternates

For at least the number given in your brief, supply
`numerical=dict(question=<stem rewritten without options, ending "...is" or "?">, answer=<int>)`.
Only use items whose answer is a whole number (or becomes one with a clearly stated scaling such
as "then $10k$ is"), in the style of JEE Main Section B. The integer must be what the rewritten
stem asks for, and should normally equal values[0].

## Solutions

`explanation`: a real worked solution a strong student would write, 2 to 6 sentences with the key
algebra shown. It must reach the keyed value. `misconception`: the specific error targeted.

## Special check patterns

- Indefinite integrals: `check` returns the integrand; `values` are the DERIVATIVES of the four
  option expressions (e.g. `diff(opt, x)`). The harness then confirms the keyed antiderivative
  differentiates to the integrand and no distractor does. Omit "+ C" from options; the stem says
  "(where $C$ is the constant of integration)" once, and options are written "... + C".
- Matrices: return sympy `Matrix` objects; equality is elementwise.
- Equations of lines/curves/loci as options: compare a canonical form, e.g. normalised
  coefficient tuples, or a direction-ratio tuple plus a point check; or return a tuple of the
  key parameters. The value must determine the option uniquely.
- Probability: use `Rational`, never floats.
- Counting: compute by brute-force enumeration (itertools) where feasible, not only by formula.

## Self-audit (do this after the harness passes, before reporting)

Go through every record once more as a hostile editor and fix anything that fails:
1. Explanation: every step true, no missing case, reaches the keyed value.
2. Each distractor rationale: perform the named mistake yourself and confirm it yields exactly
   that option. If not, rewrite the rationale or replace the distractor (and its value).
3. One defensible answer; all conventions stated; options mutually exclusive.
4. No distractor violates a condition stated in the stem; no option is absurd on sight; the key
   is not the odd one out in form (only integer among surds, only exact value, etc.).
5. Numerical alternate stem asks exactly for the integer given and is unambiguous without options.
6. Difficulty label fair; scope inside the brief.

## Before reporting back

Run: `cd /home/claude/jeemath && python3 harness.py <your file> --easy E --medium M --difficult D`
with your quotas. Fix everything under BLOCKING. Read every ADVISORY line and fix what is real.
Then re-read every item once more as a student would, checking rule 3.

Report back ONLY: the harness summary line, the list of any `flags` you set, and any item you are
still unsure about. Do not paste the questions.
