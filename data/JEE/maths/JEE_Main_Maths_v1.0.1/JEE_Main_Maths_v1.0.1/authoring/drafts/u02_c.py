import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from sympy.calculus.util import function_range

x = Symbol('x', real=True)
k = Symbol('k', real=True)
R = S.Reals


def _rs(expr):
    return solveset(expr, x, R)


def _nature(a, b, c):
    # 1 real distinct, 2 real equal, 3 non-real conjugates
    d = b**2 - 4*a*c
    if d > 0:
        return 1
    if d == 0:
        return 2
    return 3


def _nature2(a, b, c):
    # 1 real rational distinct, 2 real irrational distinct, 3 real equal, 4 non-real (rational a, b, c)
    d = Integer(b**2 - 4*a*c)
    if d < 0:
        return 4
    if d == 0:
        return 3
    return 1 if sqrt(d).is_rational else 2


def _kset(cond):
    return solveset(cond, k, R)


T, F_ = True, False
ST_OPTS = ["Both Statement I and Statement II are true",
           "Both Statement I and Statement II are false",
           "Statement I is true but Statement II is false",
           "Statement I is false but Statement II is true"]
ST_VALS = {ST_OPTS[0]: (T, T), ST_OPTS[1]: (F_, F_), ST_OPTS[2]: (T, F_), ST_OPTS[3]: (F_, T)}

# ---------------------------------------------------------------- 001
q("U02-C-001", "Quadratic equations", "Nature of roots from the discriminant", "Easy", "Direct concept MCQ",
  r"The roots of the equation $5x^2 - 6x + 9 = 0$ are",
  r"non-real complex conjugates",
  [(r"real, rational and distinct", "Uses $b^2 - 4a = 36 - 20 = 16$, omitting $c$, a positive perfect square."),
   (r"real and equal", "Uses $b^2 - 4c = 36 - 36 = 0$, omitting $a$ from $4ac$."),
   (r"real, irrational and distinct", "Sign slip: uses $b^2 + 4ac = 36 + 180 = 216$, a positive non-square.")],
  r"Here $D = b^2 - 4ac = 36 - 4 \cdot 5 \cdot 9 = 36 - 180 = -144 < 0$. Since the coefficients are real and $D < 0$, the roots are non-real and occur as a complex conjugate pair, namely $\frac{6 \pm 12i}{10} = \frac{3 \pm 6i}{5}$.",
  "Computing $b^2 + 4ac$ or dropping a coefficient from $4ac$.",
  "U02-nature-of-roots", "Single discriminant computation and its interpretation.",
  check=lambda: _nature2(5, -6, 9), values=[4, 1, 3, 2], cognitive="Understanding")

# ---------------------------------------------------------------- 002
def _c002():
    return FiniteSet(*solve(3*x**2 + 2*sqrt(3)*x + 1, x))
q("U02-C-002", "Quadratic equations", "Equal roots", "Easy", "Single-step computation MCQ",
  r"The roots of the equation $3x^2 + 2\sqrt{3}\,x + 1 = 0$ are",
  r"$-\frac{1}{\sqrt{3}}, -\frac{1}{\sqrt{3}}$",
  [(r"$\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}$", "Drops the minus sign in $-\\frac{b}{2a}$."),
   (r"$-\sqrt{3}, -\sqrt{3}$", "Uses $-\\frac{b}{2}$, forgetting to divide by $a = 3$."),
   (r"$-\frac{1}{\sqrt{3}} \pm \frac{i}{\sqrt{3}}$", "Miscomputes the discriminant as $12 - 24 = -12$ (uses $4ac = 24$).")],
  r"$D = (2\sqrt{3})^2 - 4 \cdot 3 \cdot 1 = 12 - 12 = 0$, so the roots are equal, each equal to $-\frac{b}{2a} = -\frac{2\sqrt{3}}{6} = -\frac{1}{\sqrt{3}}$. Indeed $3x^2 + 2\sqrt{3}x + 1 = (\sqrt{3}x + 1)^2$.",
  "Mishandling $-\\frac{b}{2a}$ for a repeated root.",
  "U02-equal-roots-value", "Recognising a zero discriminant and one formula.",
  check=_c002, values=[FiniteSet(-1/sqrt(3)), FiniteSet(1/sqrt(3)), FiniteSet(-sqrt(3)),
                       FiniteSet(-1/sqrt(3) + I/sqrt(3), -1/sqrt(3) - I/sqrt(3))], cognitive="Application")

# ---------------------------------------------------------------- 003
def _c003():
    sols = solve(discriminant(x**2 - k*x + 9, x), k)
    return [s for s in sols if s > 0][0]
q("U02-C-003", "Quadratic equations", "Parameter for equal roots", "Easy", "Inverse/parameter MCQ",
  r"If the equation $x^2 - kx + 9 = 0$ has equal roots and $k > 0$, then $k$ equals",
  r"$6$",
  [(r"$3$", "Sets $k^2 = 9$ instead of $k^2 = 36$, dropping the factor $4$ in $4ac$."),
   (r"$36$", "Stops at $k^2 = 36$ and reports $k^2$."),
   (r"$12$", "Sets $k^2 = 4 \\cdot 36$ by squaring the constant term wrongly.")],
  r"Equal roots need $D = k^2 - 4 \cdot 1 \cdot 9 = 0$, so $k^2 = 36$ and $k = \pm 6$. With $k > 0$, $k = 6$.",
  "Dropping the factor $4$ in $b^2 - 4ac$.",
  "U02-param-equal-roots", "One condition, one equation.",
  check=_c003, values=[6, 3, 36, 12], cognitive="Application",
  numerical=dict(question=r"If the equation $x^2 - kx + 9 = 0$ has equal roots and $k > 0$, then the value of $k$ is", answer=6))

# ---------------------------------------------------------------- 004
q("U02-C-004", "Quadratic equations", "Solving in the complex number system", "Easy", "Single-step computation MCQ",
  r"The roots of $x^2 + 2x + 5 = 0$ in $\mathbb{C}$ are",
  r"$-1 \pm 2i$",
  [(r"$1 \pm 2i$", "Uses $+b$ in the quadratic formula."),
   (r"$-1 \pm 4i$", "Writes $\\sqrt{-16} = 4i$ but forgets to divide it by $2a = 2$."),
   (r"$-2 \pm 4i$", "Does not divide by $2a$ at all.")],
  r"$D = 4 - 20 = -16$, so $\sqrt{D} = 4i$ and $x = \frac{-2 \pm 4i}{2} = -1 \pm 2i$.",
  "Not dividing every term by $2a$.",
  "U02-solve-real-coeff-C", "Direct use of the quadratic formula with negative discriminant.",
  check=lambda: FiniteSet(*solve(Symbol('w')**2 + 2*Symbol('w') + 5, Symbol('w'))),
  values=[FiniteSet(-1 + 2*I, -1 - 2*I), FiniteSet(1 + 2*I, 1 - 2*I), FiniteSet(-1 + 4*I, -1 - 4*I), FiniteSet(-2 + 4*I, -2 - 4*I)],
  cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    p, qq = symbols('p q', real=True)
    e = expand((2 - 3*I)**2 + p*(2 - 3*I) + qq)
    s = solve([re(e), im(e)], [p, qq], dict=True)[0]
    return s[qq]
q("U02-C-005", "Quadratic equations", "Conjugate-pair property", "Easy", "Inverse/parameter MCQ",
  r"If $2 - 3i$ is a root of $x^2 + px + q = 0$, where $p, q \in \mathbb{R}$, then $q$ equals",
  r"$13$",
  [(r"$-5$", "Uses $(2-3i)(2+3i) = 4 - 9$, forgetting that $-9i^2 = +9$."),
   (r"$4$", "Uses the sum of the roots, which gives $-p$, not $q$."),
   (r"$-13$", "Takes the product of the roots as $-q$.")],
  r"Since $p, q$ are real, the other root is $2 + 3i$. The product of the roots is $q = (2-3i)(2+3i) = 4 + 9 = 13$.",
  "Forgetting that non-real roots come in conjugate pairs or mishandling $i^2$.",
  "U02-conjugate-pair", "One property plus one multiplication.",
  check=_c005, values=[13, -5, 4, -13], cognitive="Application")

# ---------------------------------------------------------------- 006
q("U02-C-006", "Quadratic expressions", "Minimum value of a quadratic", "Easy", "Single-step computation MCQ",
  r"The minimum value of $x^2 - 6x + 13$ over all real $x$ is",
  r"$4$",
  [(r"$3$", "Reports the point $x = 3$ where the minimum occurs."),
   (r"$13$", "Takes the value at $x = 0$."),
   (r"$22$", "Sign slip: computes $13 + 9$ while completing the square.")],
  r"$x^2 - 6x + 13 = (x - 3)^2 + 4 \geq 4$, with equality at $x = 3$. So the minimum value is $4$.",
  "Confusing the minimising $x$ with the minimum value.",
  "U02-min-quadratic", "Completing the square once.",
  check=lambda: minimum(x**2 - 6*x + 13, x, R), values=[4, 3, 13, 22], cognitive="Application",
  numerical=dict(question=r"The minimum value of $x^2 - 6x + 13$ over all real $x$ is", answer=4))

# ---------------------------------------------------------------- 007
q("U02-C-007", "Quadratic expressions", "Maximum value of a quadratic", "Easy", "Single-step computation MCQ",
  r"The maximum value of $-2x^2 + 8x - 3$ over all real $x$ is",
  r"$5$",
  [(r"$2$", "Reports the maximising point $x = 2$."),
   (r"$11$", "Sign slip in $D$: uses $64 + 24 = 88$ in $-\\frac{D}{4a}$."),
   (r"$-3$", "Takes the value at $x = 0$.")],
  r"$-2x^2 + 8x - 3 = -2(x - 2)^2 + 5$, so the maximum is $5$ at $x = 2$. Equivalently $-\frac{D}{4a} = -\frac{64 - 24}{-8} = 5$.",
  "Sign error in the discriminant formula for the extreme value.",
  "U02-max-quadratic", "One formula or completing the square.",
  check=lambda: maximum(-2*x**2 + 8*x - 3, x, R), values=[5, 2, 11, -3], cognitive="Application")

# ---------------------------------------------------------------- 008
q("U02-C-008", "Quadratic expressions", "Sign of a quadratic for all real x", "Easy", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $x^2 + kx + 4 > 0$ for every real $x$ is",
  r"$(-4, 4)$",
  [(r"$[-4, 4]$", "Uses $D \\leq 0$; at $k = \\pm 4$ the expression vanishes at one point."),
   (r"$(-\infty, -4) \cup (4, \infty)$", "Uses $D > 0$, the condition for two real roots."),
   (r"$(-2, 2)$", "Uses $k^2 < 4$, dropping the factor $4a$ from $4ac$.")],
  r"Since the leading coefficient is $1 > 0$, the expression is positive for all real $x$ exactly when $D = k^2 - 16 < 0$, i.e. $-4 < k < 4$.",
  "Including the boundary where the expression touches zero.",
  "U02-positive-definite", "One condition on the discriminant with strict inequality.",
  check=lambda: _kset(discriminant(x**2 + k*x + 4, x) < 0),
  values=[Interval.open(-4, 4), Interval(-4, 4), Union(Interval.open(-oo, -4), Interval.open(4, oo)), Interval.open(-2, 2)],
  cognitive="Understanding")

# ---------------------------------------------------------------- 009
q("U02-C-009", "Quadratic equations", "Parameter for real roots", "Easy", "Inverse/parameter MCQ",
  r"The equation $x^2 + 4x + k = 0$ has real roots if and only if $k$ belongs to",
  r"$(-\infty, 4]$",
  [(r"$(-\infty, 4)$", "Excludes the equal-roots case; real roots include equal roots."),
   (r"$[4, \infty)$", "Reverses the inequality $16 - 4k \\geq 0$."),
   (r"$(-\infty, 16]$", "Uses $16 - k \\geq 0$, forgetting the factor $4$.")],
  r"Real roots need $D = 16 - 4k \geq 0$, i.e. $k \leq 4$. At $k = 4$ the roots are real and equal ($x = -2$), so $4$ is included.",
  "Excluding equal roots from 'real roots'.",
  "U02-param-real-roots", "Single discriminant inequality.",
  check=lambda: _kset(discriminant(x**2 + 4*x + k, x) >= 0),
  values=[Interval(-oo, 4), Interval.open(-oo, 4), Interval(4, oo), Interval(-oo, 16)], cognitive="Application")

# ---------------------------------------------------------------- 010
_eqs010 = [(2, -5, -6), (2, -7, 6), (1, -4, -12), (3, -1, -4)]
def _c010():
    idx = [i for i, (a, b, c) in enumerate(_eqs010)
           if (b*b - 4*a*c) > 0 and not sqrt(Integer(b*b - 4*a*c)).is_rational]
    assert len(idx) == 1
    return idx[0]
q("U02-C-010", "Quadratic equations", "Rational and irrational roots", "Easy", "Conceptual/application MCQ",
  r"Which of the following equations has irrational roots?",
  r"$2x^2 - 5x - 6 = 0$",
  [(r"$2x^2 - 7x + 6 = 0$", "Sign slip $b^2 + 4ac$: gets $49 + 48 = 97$, not a perfect square; the true discriminant is $49 - 48 = 1$."),
   (r"$x^2 - 4x - 12 = 0$", "Uses $b^2 - 2ac$: gets $16 + 24 = 40$, not a perfect square; the true discriminant is $16 + 48 = 64$."),
   (r"$3x^2 - x - 4 = 0$", "Drops the leading coefficient and uses $b^2 - 4c = 1 + 16 = 17$, not a perfect square; the true discriminant is $1 + 48 = 49$.")],
  r"With rational coefficients, the roots are rational exactly when $D = b^2 - 4ac$ is a perfect square. The discriminants are $25 + 48 = 73$, $49 - 48 = 1$, $16 + 48 = 64$ and $1 + 48 = 49$. Only $73$ is not a perfect square, so $2x^2 - 5x - 6 = 0$ has irrational roots $\frac{5 \pm \sqrt{73}}{4}$.",
  "Errors in computing $b^2 - 4ac$: a sign slip, the wrong multiple of $ac$, or dropping $a$.",
  "U02-rational-roots", "One discriminant per option, test for a perfect square.",
  check=_c010, values=[0, 1, 2, 3], cognitive="Understanding")

# ---------------------------------------------------------------- 011
q("U02-C-011", "Equations reducible to quadratics", "Biquadratic equations", "Easy", "Single-step computation MCQ",
  r"The number of real roots of $x^4 - 3x^2 - 4 = 0$ is",
  r"$2$",
  [(r"$4$", "Accepts $x^2 = -1$ as giving real roots."),
   (r"$1$", "Keeps only $x = 2$ from $x^2 = 4$."),
   (r"$0$", "Rejects both values of $x^2$.")],
  r"Put $t = x^2 \geq 0$: $t^2 - 3t - 4 = 0$ gives $t = 4$ or $t = -1$. Only $t = 4$ is admissible, giving $x = \pm 2$. So there are $2$ real roots.",
  "Not rejecting a negative value of $x^2$.",
  "U02-biquadratic-count", "One substitution and a sign check.",
  check=lambda: len(_rs(x**4 - 3*x**2 - 4)), values=[2, 4, 1, 0], cognitive="Application",
  numerical=dict(question=r"The number of real roots of $x^4 - 3x^2 - 4 = 0$ is", answer=2))

# ---------------------------------------------------------------- 012
q("U02-C-012", "Equations reducible to quadratics", "Equations in |x|", "Easy", "Single-step computation MCQ",
  r"The set of all real solutions of $x^2 - 5|x| + 6 = 0$ is",
  r"$\{-3, -2, 2, 3\}$",
  [(r"$\{2, 3\}$", "Solves $t^2 - 5t + 6 = 0$ with $t = |x|$ but reports $t$ instead of $x$."),
   (r"$\{-3, -2\}$", "Replaces $|x|$ by $-x$ for all $x$."),
   (r"$\{-6, 6\}$", "Factors as $(|x| - 6)(|x| + 1)$, mistaking $+6$ for $-6$.")],
  r"Since $x^2 = |x|^2$, put $t = |x| \geq 0$: $t^2 - 5t + 6 = 0$ gives $t = 2$ or $3$. Then $|x| = 2$ or $|x| = 3$, so $x \in \{-3, -2, 2, 3\}$.",
  "Forgetting that $|x| = a$ gives two values of $x$.",
  "U02-modulus-quadratic", "One substitution, then unpacking the modulus.",
  check=lambda: _rs(x**2 - 5*Abs(x) + 6),
  values=[FiniteSet(-3, -2, 2, 3), FiniteSet(2, 3), FiniteSet(-3, -2), FiniteSet(-6, 6)], cognitive="Application")

# ---------------------------------------------------------------- 013
q("U02-C-013", "Equations reducible to quadratics", "Exponential substitution", "Easy", "Single-step computation MCQ",
  r"The set of all real solutions of $4^x - 3 \cdot 2^x + 2 = 0$ is",
  r"$\{0, 1\}$",
  [(r"$\{1, 2\}$", "Reports the values of $t = 2^x$ instead of $x$."),
   (r"$\{1\}$", "Discards $2^x = 1$, overlooking $x = 0$."),
   (r"$\{0, \frac{1}{2}\}$", "Solves $4^x = 2$ instead of $2^x = 2$ for the second value.")],
  r"Put $t = 2^x > 0$, so $4^x = t^2$: $t^2 - 3t + 2 = 0$ gives $t = 1$ or $t = 2$. Then $2^x = 1$ gives $x = 0$ and $2^x = 2$ gives $x = 1$.",
  "Stopping at the substituted variable.",
  "U02-exponential-reducible", "One substitution and back-substitution.",
  check=lambda: _rs(4**x - 3*2**x + 2),
  values=[FiniteSet(0, 1), FiniteSet(1, 2), FiniteSet(1), FiniteSet(0, Rational(1, 2))], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    s1 = _rs(x**2 + x + 1) == S.EmptySet and (x**2 + x + 1).subs(x, 0) > 0
    # Statement II is the conjugate-pair theorem; verify on the quadratic with root 2+i and real coefficients
    pq = expand((x - (2 + I))*(x - (2 - I)))
    s2 = all(c.is_real for c in Poly(pq, x).all_coeffs()) and simplify(pq.subs(x, 2 - I)) == 0
    return (bool(s1), bool(s2))
q("U02-C-014", "Quadratic equations", "Sign of a quadratic and conjugate roots", "Easy", "Statement-based MCQ",
  r"Statement I: $x^2 + x + 1 > 0$ for every real $x$. Statement II: If $2 + i$ is a root of a quadratic equation with real coefficients, then $2 - i$ is also a root of that equation. In the light of the above statements, choose the correct answer.",
  ST_OPTS[0],
  [(ST_OPTS[1], "Thinks a quadratic with no real roots can take negative values, and doubts the conjugate-pair property."),
   (ST_OPTS[2], "Believes the conjugate-pair property needs extra hypotheses beyond real coefficients."),
   (ST_OPTS[3], "Concludes from $D < 0$ that the expression is negative somewhere.")],
  r"For $x^2 + x + 1$, $a = 1 > 0$ and $D = 1 - 4 = -3 < 0$, so the expression is positive for all real $x$; Statement I is true. If a real-coefficient polynomial vanishes at $z$, taking conjugates shows it vanishes at $\overline{z}$, so $2 - i$ is also a root; Statement II is true.",
  "Misreading $D < 0$ as 'negative expression'.",
  "U02-statement-sign-conj", "Two standard facts, each checked in one step.",
  check=_c014, values=[ST_VALS[ST_OPTS[0]], ST_VALS[ST_OPTS[1]], ST_VALS[ST_OPTS[2]], ST_VALS[ST_OPTS[3]]],
  cognitive="Understanding")

# ---------------------------------------------------------------- 015
q("U02-C-015", "Quadratic expressions", "Range of a quadratic", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = x^2 - 4x + 7$, $x \in \mathbb{R}$, is",
  r"$[3, \infty)$",
  [(r"$(3, \infty)$", "Excludes the minimum value, which is attained at $x = 2$."),
   (r"$[7, \infty)$", "Takes $f(0) = 7$ as the least value."),
   (r"$[2, \infty)$", "Uses the vertex abscissa $x = 2$ as the least value.")],
  r"$f(x) = (x - 2)^2 + 3 \geq 3$, with equality at $x = 2$, and $f(x) \to \infty$ as $|x| \to \infty$. So the range is $[3, \infty)$.",
  "Confusing the vertex abscissa with the minimum value.",
  "U02-range-quadratic", "Completing the square once.",
  check=lambda: function_range(x**2 - 4*x + 7, x, R),
  values=[Interval(3, oo), Interval.open(3, oo), Interval(7, oo), Interval(2, oo)], cognitive="Application")

# ---------------------------------------------------------------- 016
def _c016():
    a, b, c = -1, 2, -5
    d = b*b - 4*a*c
    if d < 0:
        return 1 if a < 0 else 2
    return 3 if d == 0 else 4
q("U02-C-016", "Quadratic expressions", "Sign of a quadratic expression", "Easy", "Direct concept MCQ",
  r"For real $x$, the expression $-x^2 + 2x - 5$ is",
  r"negative for every real $x$",
  [(r"positive for every real $x$", "Uses $D < 0$ alone and ignores the sign of the leading coefficient."),
   (r"zero for exactly one real $x$", "Takes $D = 4 - 4 = 0$, forgetting $4ac = 20$."),
   (r"positive for some $x$ and negative for others", "Sign slip $D = 4 + 20 > 0$.")],
  r"Here $a = -1 < 0$ and $D = 4 - 4(-1)(-5) = 4 - 20 = -16 < 0$. A quadratic with $D < 0$ has the sign of $a$ for all real $x$; indeed $-x^2 + 2x - 5 = -(x - 1)^2 - 4 \leq -4$.",
  "Ignoring the sign of the leading coefficient.",
  "U02-sign-definite-concept", "One discriminant plus the sign rule.",
  check=_c016, values=[1, 2, 3, 4], cognitive="Understanding")

# ---------------------------------------------------------------- 017
z = Symbol('z')
q("U02-C-017", "Quadratics with complex coefficients", "Solving with a complex discriminant", "Medium", "Multi-step computation MCQ",
  r"The roots of $z^2 - (4 + i)z + (3 + 3i) = 0$ are",
  r"$3$ and $1 + i$",
  [(r"$-3$ and $-1 - i$", "Uses $+b$ instead of $-b$ in the quadratic formula."),
   (r"$3$ and $1 - i$", "Assumes non-real roots occur in conjugate pairs even with complex coefficients."),
   (r"$3 + i$ and $1$", "Takes $\\sqrt{3 - 4i} = 2 + i$, with the wrong sign of the imaginary part.")],
  r"$D = (4 + i)^2 - 4(3 + 3i) = 15 + 8i - 12 - 12i = 3 - 4i$. Since $(2 - i)^2 = 3 - 4i$, $z = \frac{(4 + i) \pm (2 - i)}{2}$, giving $z = 3$ and $z = 1 + i$.",
  "Wrong square root of a complex discriminant.",
  "U02-complex-coeff-solve", "Complex discriminant, its square root, then the formula.",
  check=lambda: FiniteSet(*solve(z**2 - (4 + I)*z + (3 + 3*I), z)),
  values=[FiniteSet(3, 1 + I), FiniteSet(-3, -1 - I), FiniteSet(3, 1 - I), FiniteSet(3 + I, 1)], cognitive="Application")

# ---------------------------------------------------------------- 018
q("U02-C-018", "Quadratics with complex coefficients", "Solving with a complex discriminant", "Medium", "Multi-step computation MCQ",
  r"The roots of $z^2 - (1 - i)z + (6 + 2i) = 0$ are",
  r"$2i$ and $1 - 3i$",
  [(r"$-2i$ and $-1 + 3i$", "Uses $+b$ instead of $-b$ in the quadratic formula."),
   (r"$-2i$ and $1 + 3i$", "Conjugates the roots, assuming the conjugate-pair rule applies."),
   (r"$1 + 2i$ and $-3i$", "Takes $\\sqrt{-24 - 10i} = 1 + 5i$, whose square is actually $-24 + 10i$.")],
  r"$D = (1 - i)^2 - 4(6 + 2i) = -2i - 24 - 8i = -24 - 10i$. Since $(1 - 5i)^2 = 1 - 10i - 25 = -24 - 10i$, $z = \frac{(1 - i) \pm (1 - 5i)}{2}$, which gives $1 - 3i$ and $2i$.",
  "Choosing a wrong square root of the complex discriminant.",
  "U02-complex-coeff-solve", "Complex discriminant, square root by matching parts, then the formula.",
  check=lambda: FiniteSet(*solve(z**2 - (1 - I)*z + (6 + 2*I), z)),
  values=[FiniteSet(2*I, 1 - 3*I), FiniteSet(-2*I, -1 + 3*I), FiniteSet(-2*I, 1 + 3*I), FiniteSet(1 + 2*I, -3*I)],
  cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    t = Symbol('t', real=True)
    e = expand(t**2 + (2 - I)*t + (k + 3*I))
    s = solve([re(e), im(e)], [t, k], dict=True)
    assert len(s) == 1
    return s[0][k]
q("U02-C-019", "Quadratics with complex coefficients", "Real root of a complex-coefficient quadratic", "Medium", "Inverse/parameter MCQ",
  r"If $k$ is real and the equation $x^2 + (2 - i)x + (k + 3i) = 0$ has a real root, then $k$ equals",
  r"$-15$",
  [(r"$-3$", "Solves the imaginary part as $t + 3 = 0$, getting the real root $t = -3$."),
   (r"$15$", "Sign slip when solving $9 + 6 + k = 0$."),
   (r"$-9$", "Drops the term $2t$ in the real part.")],
  r"Let $x = t$ be the real root. Then $t^2 + 2t + k + i(3 - t) = 0$. Equating the imaginary part to zero gives $t = 3$, and the real part gives $9 + 6 + k = 0$, so $k = -15$.",
  "Not separating real and imaginary parts correctly.",
  "U02-complex-coeff-real-root", "Two equations from real and imaginary parts.",
  check=_c019, values=[-15, -3, 15, -9], cognitive="Application")

# ---------------------------------------------------------------- 020
def _c020():
    p, qq = symbols('p q', real=True)
    r0 = 1 / (1 - I)
    e = expand(r0**2 + p*r0 + qq)
    s = solve([re(e), im(e)], [p, qq], dict=True)[0]
    return s[p] + s[qq]
q("U02-C-020", "Quadratic equations", "Conjugate-pair property", "Medium", "Multi-step computation MCQ",
  r"If $\frac{1}{1 - i}$ is a root of $x^2 + px + q = 0$, where $p, q \in \mathbb{R}$, then $p + q$ equals",
  r"$-\frac{1}{2}$",
  [(r"$\frac{3}{2}$", "Takes $p$ as the sum of the roots, $p = 1$, instead of $p = -1$."),
   (r"$0$", "Uses $1 - i$ itself as the root, getting $p = -2$, $q = 2$."),
   (r"$-1$", "Computes the product as $\\frac{1 + i^2}{4} = 0$.")],
  r"$\frac{1}{1 - i} = \frac{1 + i}{2}$. With real coefficients the other root is $\frac{1 - i}{2}$. The sum of roots is $1 = -p$, so $p = -1$, and the product is $\frac{1 - i^2}{4} = \frac{1}{2} = q$. Hence $p + q = -\frac{1}{2}$.",
  "Not rationalising the root or misusing the sign of $p$.",
  "U02-conjugate-pair", "Rationalise, apply conjugate pair, use two coefficient relations.",
  check=_c020, values=[Rational(-1, 2), Rational(3, 2), 0, -1], cognitive="Application")

# ---------------------------------------------------------------- 021
def _c021():
    rts = solve(z**2 - (3 + I)*z + (2 + 2*I), z)
    s1 = all(any(simplify(conjugate(r) - u) == 0 for u in rts) for r in rts)
    s2 = any(im(r) == 0 for r in rts)
    return (bool(s1), bool(s2))
q("U02-C-021", "Quadratics with complex coefficients", "Conjugate roots and complex coefficients", "Medium", "Statement-based MCQ",
  r"Statement I: If a quadratic equation in $z$ has complex coefficients and has a non-real root $\alpha$, then $\overline{\alpha}$ is also a root. Statement II: The equation $z^2 - (3 + i)z + (2 + 2i) = 0$ has a real root. In the light of the above statements, choose the correct answer.",
  ST_OPTS[3],
  [(ST_OPTS[0], "Extends the conjugate-pair property to complex coefficients."),
   (ST_OPTS[1], "Assumes complex coefficients force both roots to be non-real."),
   (ST_OPTS[2], "Accepts the conjugate-pair rule and also assumes there is no real root.")],
  r"Substituting $z = 2$: $4 - 6 - 2i + 2 + 2i = 0$, so $2$ is a root and Statement II is true. The other root is $\frac{2 + 2i}{2} = 1 + i$, whose conjugate $1 - i$ is not a root, so Statement I is false. The conjugate-pair property needs real coefficients.",
  "Applying the conjugate-pair rule to complex coefficients.",
  "U02-statement-conj-complex", "Testing a general claim against a specific equation.",
  check=_c021, values=[ST_VALS[ST_OPTS[3]], ST_VALS[ST_OPTS[0]], ST_VALS[ST_OPTS[1]], ST_VALS[ST_OPTS[2]]],
  cognitive="Analysis")

# ---------------------------------------------------------------- 022
def _c022():
    e = (k + 1)*x**2 - 2*(k - 1)*x + 1
    sols = [s for s in solve(discriminant(e, x), k) if s != -1]
    return FiniteSet(*sols)
q("U02-C-022", "Quadratic equations", "Parameter for equal roots", "Medium", "Inverse/parameter MCQ",
  r"The equation $(k + 1)x^2 - 2(k - 1)x + 1 = 0$, where $k \neq -1$, has equal roots for $k$ in the set",
  r"$\{0, 3\}$",
  [(r"$\{0, -3\}$", "Sign slip: gets $k^2 + 3k = 0$ from $(k - 1)^2 - (k + 1)$."),
   (r"$\{3\}$", "Discards $k = 0$, confusing it with the excluded value that makes the equation linear."),
   (r"$\{-3\}$", "Sign slip and also discards $k = 0$.")],
  r"Equal roots need $\frac{D}{4} = (k - 1)^2 - (k + 1) = k^2 - 3k = 0$, so $k = 0$ or $k = 3$. Both keep the leading coefficient $k + 1$ non-zero. Check: $k = 0$ gives $(x + 1)^2 = 0$ and $k = 3$ gives $(2x - 1)^2 = 0$.",
  "Dropping a valid parameter value or mishandling $D/4$.",
  "U02-param-equal-roots", "Discriminant with a parameter in two coefficients, plus a validity check.",
  check=_c022, values=[FiniteSet(0, 3), FiniteSet(0, -3), FiniteSet(3), FiniteSet(-3)], cognitive="Application")

# ---------------------------------------------------------------- 023
def _c023():
    s = _kset(discriminant(k*x**2 + 4*x + 1, x) >= 0)
    return Complement(s, FiniteSet(0))
q("U02-C-023", "Quadratic equations", "Parameter for real roots with a != 0", "Medium", "Inverse/parameter MCQ",
  r"If $kx^2 + 4x + 1 = 0$ is a quadratic equation with real roots, then the set of all possible values of $k$ is",
  r"$(-\infty, 0) \cup (0, 4]$",
  [(r"$(-\infty, 4]$", "Does not exclude $k = 0$, where the equation is not quadratic."),
   (r"$(0, 4]$", "Assumes the leading coefficient must be positive."),
   (r"$(-\infty, 0) \cup (0, 4)$", "Excludes the equal-roots case $k = 4$.")],
  r"Real roots need $D = 16 - 4k \geq 0$, i.e. $k \leq 4$. Since the equation must be quadratic, $k \neq 0$. Hence $k \in (-\infty, 0) \cup (0, 4]$; at $k = 4$ the roots are equal ($x = -\frac{1}{2}$).",
  "Forgetting the $a \\neq 0$ condition.",
  "U02-param-real-roots", "Discriminant condition combined with the leading-coefficient condition.",
  check=_c023, values=[Union(Interval.open(-oo, 0), Interval.Lopen(0, 4)), Interval(-oo, 4), Interval.Lopen(0, 4),
                       Union(Interval.open(-oo, 0), Interval.open(0, 4))], cognitive="Application")

# ---------------------------------------------------------------- 024
q("U02-C-024", "Quadratic equations", "Parameter for no real roots", "Medium", "Inverse/parameter MCQ",
  r"The equation $x^2 + (k - 3)x + k = 0$ has no real roots if and only if $k$ belongs to",
  r"$(1, 9)$",
  [(r"$[1, 9]$", "Uses $D \\leq 0$; at $k = 1$ or $9$ the roots are real and equal."),
   (r"$(-\infty, 1) \cup (9, \infty)$", "Solves $D > 0$, the condition for distinct real roots."),
   (r"$(-9, -1)$", "Correctly reaches $k^2 - 10k + 9 < 0$ but factorises it as $(k + 1)(k + 9)$ with the wrong signs, giving $-9 < k < -1$.")],
  r"No real roots means $D = (k - 3)^2 - 4k < 0$, i.e. $k^2 - 10k + 9 < 0$, i.e. $(k - 1)(k - 9) < 0$. So $1 < k < 9$.",
  "Including boundary values where roots are equal.",
  "U02-param-nonreal-roots", "Discriminant becomes a quadratic inequality in $k$.",
  check=lambda: _kset(discriminant(x**2 + (k - 3)*x + k, x) < 0),
  values=[Interval.open(1, 9), Interval(1, 9), Union(Interval.open(-oo, 1), Interval.open(9, oo)), Interval.open(-9, -1)],
  cognitive="Application")

# ---------------------------------------------------------------- 025
def _c025():
    e = (k - 1)*x**2 + 2*(k - 1)*x + 3
    a = Poly(e, x).coeff_monomial(x**2)
    quad = Intersection(_kset(a > 0), _kset(discriminant(e, x) < 0))
    # degenerate case a = 0: expression must still be positive for all x
    deg = FiniteSet(*[kv for kv in solve(a, k) if _rs(e.subs(k, kv) <= 0) == S.EmptySet])
    return Union(quad, deg)
q("U02-C-025", "Quadratic expressions", "Positive for all real x with a parameter in the leading coefficient", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $(k - 1)x^2 + 2(k - 1)x + 3 > 0$ for every real $x$ is",
  r"$[1, 4)$",
  [(r"$(1, 4)$", "Ignores $k = 1$, where the expression reduces to the constant $3 > 0$."),
   (r"$(1, 4]$", "Uses $D \\leq 0$ and also drops $k = 1$."),
   (r"$(-\infty, 1) \cup (4, \infty)$", "Uses $D > 0$ instead of $D < 0$.")],
  r"If $k = 1$ the expression is $3 > 0$ for all $x$, so $k = 1$ works. If $k \neq 1$ we need $k - 1 > 0$ and $\frac{D}{4} = (k - 1)^2 - 3(k - 1) = (k - 1)(k - 4) < 0$, i.e. $1 < k < 4$. Together, $k \in [1, 4)$.",
  "Forgetting the degenerate case where the leading coefficient vanishes.",
  "U02-positive-definite-param", "Casework on the leading coefficient plus a discriminant inequality.",
  check=_c025, values=[Interval.Ropen(1, 4), Interval.open(1, 4), Interval.Lopen(1, 4),
                       Union(Interval.open(-oo, 1), Interval.open(4, oo))], cognitive="Analysis")

# ---------------------------------------------------------------- 026
q("U02-C-026", "Quadratic expressions", "Non-negative for all real x", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $x^2 + 2(k + 1)x + 9k - 5 \geq 0$ for every real $x$ is",
  r"$[1, 6]$",
  [(r"$(1, 6)$", "Uses $D < 0$; the boundary values make the expression a perfect square, still $\\geq 0$."),
   (r"$(-\infty, 1] \cup [6, \infty)$", "Reverses the inequality on $\\frac{D}{4}$."),
   (r"$[-6, -1]$", "Sign slip: gets $k^2 + 7k + 6$ for $\\frac{D}{4}$.")],
  r"With leading coefficient $1 > 0$, the condition is $\frac{D}{4} = (k + 1)^2 - (9k - 5) \leq 0$, i.e. $k^2 - 7k + 6 \leq 0$, i.e. $(k - 1)(k - 6) \leq 0$. So $1 \leq k \leq 6$.",
  "Using a strict inequality for a non-strict condition.",
  "U02-nonneg-all-x", "Discriminant condition with correct boundary handling.",
  check=lambda: _kset(discriminant(x**2 + 2*(k + 1)*x + 9*k - 5, x) <= 0),
  values=[Interval(1, 6), Interval.open(1, 6), Union(Interval(-oo, 1), Interval(6, oo)), Interval(-6, -1)],
  cognitive="Application")

# ---------------------------------------------------------------- 027
def _c027():
    m = minimum(x**2 - 2*k*x - k + 6, x, R)
    return [s for s in solve(m, k) if s > 0][0]
q("U02-C-027", "Quadratic expressions", "Minimum value with a parameter", "Medium", "Inverse/parameter MCQ",
  r"If $k > 0$ and the minimum value of $x^2 - 2kx - k + 6$ over all real $x$ is $0$, then $k$ equals",
  r"$2$",
  [(r"$3$", "Misreads the constant term as $k + 6$, so the minimum is $-k^2 + k + 6$ and $k^2 - k - 6 = 0$ gives $k = 3$."),
   (r"$\frac{3}{2}$", "Uses $c - \\frac{b^2}{2a}$ for the minimum: $-k + 6 - 2k^2 = 0$, i.e. $(2k - 3)(k + 2) = 0$, giving $k = \\frac{3}{2}$."),
   (r"$6$", "Places the vertex at $x = 2k$ (using $-\\frac{b}{a}$): $f(2k) = 6 - k = 0$ gives $k = 6$.")],
  r"The minimum occurs at $x = k$ and equals $k^2 - 2k^2 - k + 6 = -k^2 - k + 6$. Setting this to $0$ gives $k^2 + k - 6 = 0$, i.e. $(k + 3)(k - 2) = 0$, so $k = 2$ or $k = -3$. With $k > 0$, $k = 2$.",
  "Wrong vertex formula $-\\frac{b}{a}$ or $c - \\frac{b^2}{2a}$ for the extreme value.",
  "U02-min-param", "Vertex value as a function of the parameter, then a quadratic in $k$.",
  check=_c027, values=[2, 3, Rational(3, 2), 6], cognitive="Application",
  numerical=dict(question=r"If $k > 0$ and the minimum value of $x^2 - 2kx - k + 6$ over all real $x$ is $0$, then $k$ is", answer=2))

# ---------------------------------------------------------------- 028
def _c028():
    f = 2 / (x**2 - 2*x + 3)
    s1 = function_range(f, x, R) == Interval.Lopen(0, 2)
    s2 = minimum(x**2 - 2*x + 3, x, R) == 3
    return (bool(s1), bool(s2))
q("U02-C-028", "Quadratic expressions", "Range via the minimum of a quadratic", "Medium", "Statement-based MCQ",
  r"Statement I: The range of $f(x) = \frac{2}{x^2 - 2x + 3}$, $x \in \mathbb{R}$, is $(0, 2]$. Statement II: The minimum value of $x^2 - 2x + 3$ over all real $x$ is $3$. In the light of the above statements, choose the correct answer.",
  ST_OPTS[1],
  [(ST_OPTS[0], "Two separate errors: reads the constant $3$ as the minimum of the denominator (so Statement II looks true) and assumes the numerator $2$ is the largest value of $f$ (so Statement I looks true)."),
   (ST_OPTS[2], "Finds the minimum $2$ of the denominator correctly but takes the numerator $2$ as the largest value of $f$, as if the denominator could be $1$."),
   (ST_OPTS[3], "Reads the constant term $3$ as the minimum value, so Statement II looks true, while the resulting range $\\left(0, \\frac{2}{3}\\right]$ still makes Statement I false.")],
  r"$x^2 - 2x + 3 = (x - 1)^2 + 2 \geq 2$, so its minimum is $2$, not $3$; Statement II is false. Hence $0 < f(x) \leq \frac{2}{2} = 1$, with $f \to 0$ as $|x| \to \infty$, so the range is $(0, 1]$; Statement I is false.",
  "Reading the constant term as the minimum of a quadratic.",
  "U02-statement-range-reciprocal", "Two linked range facts to verify.",
  check=_c028, values=[ST_VALS[ST_OPTS[1]], ST_VALS[ST_OPTS[0]], ST_VALS[ST_OPTS[2]], ST_VALS[ST_OPTS[3]]],
  cognitive="Analysis")

# ---------------------------------------------------------------- 029
q("U02-C-029", "Range of rational functions", "Range of quadratic over quadratic", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{x^2 - 2x + 4}{x^2 + 2x + 4}$, $x \in \mathbb{R}$, is",
  r"$\left[\frac{1}{3}, 3\right]$",
  [(r"$\left(\frac{1}{3}, 3\right)$", "Uses $D > 0$ in the discriminant condition and loses the attained extremes."),
   (r"$\left[\frac{3}{5}, \frac{5}{3}\right]$", "Halves $b$ but keeps $4ac$: $(y + 1)^2 - 16(y - 1)^2 \\geq 0$, i.e. $(5 - 3y)(5y - 3) \\geq 0$."),
   (r"$\left[\frac{1}{3}, 1\right) \cup \left(1, 3\right]$", "Excludes $y = 1$ because the $x^2$ coefficient $y - 1$ vanishes, though $y = 1$ is attained at $x = 0$.")],
  r"The denominator is $(x + 1)^2 + 3 > 0$. Put $y = f(x)$: $(y - 1)x^2 + 2(y + 1)x + 4(y - 1) = 0$. For $y \neq 1$, real $x$ needs $(y + 1)^2 - 4(y - 1)^2 \geq 0$, i.e. $(3 - y)(3y - 1) \geq 0$, i.e. $\frac{1}{3} \leq y \leq 3$. Also $y = 1$ occurs at $x = 0$. So the range is $\left[\frac{1}{3}, 3\right]$.",
  "Dropping $y = 1$ when the equation in $x$ becomes linear.",
  "U02-range-rational", "Convert to a quadratic in $x$, impose $D \\geq 0$, handle the degenerate value.",
  check=lambda: function_range((x**2 - 2*x + 4)/(x**2 + 2*x + 4), x, R),
  values=[Interval(Rational(1, 3), 3), Interval.open(Rational(1, 3), 3), Interval(Rational(3, 5), Rational(5, 3)),
          Union(Interval.Ropen(Rational(1, 3), 1), Interval.Lopen(1, 3))], cognitive="Application")

# ---------------------------------------------------------------- 030
q("U02-C-030", "Range of rational functions", "Range with an unattained bound", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{x^2 + 2x + 1}{x^2 + 2x + 7}$, $x \in \mathbb{R}$, is",
  r"$[0, 1)$",
  [(r"$[0, 1]$", "Includes $y = 1$; that would need $\\frac{6}{(x + 1)^2 + 6} = 0$, which never happens."),
   (r"$(0, 1)$", "Excludes $y = 0$, which is attained at $x = -1$."),
   (r"$\left[\frac{1}{7}, 1\right)$", "Takes $f(0) = \\frac{1}{7}$ as the least value.")],
  r"Write $f(x) = 1 - \frac{6}{(x + 1)^2 + 6}$. Since $(x + 1)^2 + 6 \geq 6$, $0 < \frac{6}{(x + 1)^2 + 6} \leq 1$, so $0 \leq f(x) < 1$. The value $0$ is attained at $x = -1$, and $f(x) \to 1$ without reaching it.",
  "Treating a limiting value as attained.",
  "U02-range-rational", "Rewrite, bound the reciprocal of a quadratic, decide attainment.",
  check=lambda: function_range((x**2 + 2*x + 1)/(x**2 + 2*x + 7), x, R),
  values=[Interval.Ropen(0, 1), Interval(0, 1), Interval.open(0, 1), Interval.Ropen(Rational(1, 7), 1)],
  cognitive="Application")

# ---------------------------------------------------------------- 031
def _c031():
    e = x**2 - 2*(k - 1)*x + (k + 5)
    c = Poly(e, x).all_coeffs()
    return Intersection(_kset(discriminant(e, x) >= 0), _kset(-c[1]/c[0] > 0), _kset(c[2]/c[0] > 0))
q("U02-C-031", "Location of roots", "Both roots positive", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which both roots of $x^2 - 2(k - 1)x + (k + 5) = 0$ (not necessarily distinct) are real and positive is",
  r"$[4, \infty)$",
  [(r"$(4, \infty)$", "Uses $D > 0$, excluding the equal positive roots at $k = 4$."),
   (r"$(1, \infty)$", "Ignores the reality condition $D \\geq 0$."),
   (r"$(-5, -1] \cup [4, \infty)$", "Uses $D \\geq 0$ and product $> 0$ but ignores the sum condition.")],
  r"Need $\frac{D}{4} = (k - 1)^2 - (k + 5) = (k - 4)(k + 1) \geq 0$, sum $2(k - 1) > 0$ and product $k + 5 > 0$. These give $k \leq -1$ or $k \geq 4$; $k > 1$; $k > -5$. Together $k \geq 4$. At $k = 4$ the equation is $(x - 3)^2 = 0$, with positive roots.",
  "Omitting one of the three conditions (reality, sum, product).",
  "U02-location-both-positive", "Three simultaneous conditions intersected.",
  check=_c031, values=[Interval(4, oo), Interval.open(4, oo), Interval.open(1, oo), Union(Interval.Lopen(-5, -1), Interval(4, oo))],
  cognitive="Application")

# ---------------------------------------------------------------- 032
def _c032():
    e = (k - 1)*x**2 + 3*x + (k - 4)
    c = Poly(e, x).all_coeffs()
    s = Complement(_kset(c[2]/c[0] < 0), FiniteSet(1))
    # product < 0 forces real distinct roots; confirm D > 0 on this set
    assert Intersection(s, _kset(discriminant(e, x) <= 0)) == S.EmptySet
    return s
q("U02-C-032", "Location of roots", "Roots of opposite signs", "Medium", "Inverse/parameter MCQ",
  r"Let $k \neq 1$. The roots of $(k - 1)x^2 + 3x + (k - 4) = 0$ are real and of opposite signs if and only if $k$ belongs to",
  r"$(1, 4)$",
  [(r"$(1, 4]$", "Uses product of roots $\\leq 0$, accepting $k = 4$, where the roots are $0$ and $-1$ and $0$ has no sign."),
   (r"$(-\infty, 1) \cup (4, \infty)$", "Uses product of roots $> 0$."),
   (r"$(-\infty, 4)$", "Uses $k - 4 < 0$ only, ignoring the sign of the leading coefficient.")],
  r"Roots of opposite signs exactly when the product $\frac{k - 4}{k - 1} < 0$, i.e. $1 < k < 4$. Then $ac < 0$, so $D = 9 - 4ac > 0$ automatically and the roots are real.",
  "Testing $c < 0$ instead of $\\frac{c}{a} < 0$.",
  "U02-location-opposite-signs", "Product condition with a parametric leading coefficient.",
  check=_c032, values=[Interval.open(1, 4), Interval.Lopen(1, 4), Union(Interval.open(-oo, 1), Interval.open(4, oo)), Interval.open(-oo, 4)],
  cognitive="Application")

# ---------------------------------------------------------------- 033
def _c033():
    e = x**2 + 2*(k - 1)*x + k + 5
    return _kset(e.subs(x, 1) < 0)
q("U02-C-033", "Location of roots", "A number between the roots", "Medium", "Inverse/parameter MCQ",
  r"The number $1$ lies strictly between the roots of $x^2 + 2(k - 1)x + k + 5 = 0$ if and only if $k$ belongs to",
  r"$\left(-\infty, -\frac{4}{3}\right)$",
  [(r"$\left(-\infty, -\frac{4}{3}\right]$", "Uses $f(1) \\leq 0$; at $k = -\\frac{4}{3}$, $1$ is itself a root."),
   (r"$\left(-\frac{4}{3}, \infty\right)$", "Uses $f(1) > 0$."),
   (r"$(-\infty, -1) \cup (4, \infty)$", "Uses only the distinct-real-roots condition $D > 0$.")],
  r"Let $f(x) = x^2 + 2(k - 1)x + k + 5$. Since the leading coefficient is positive, $1$ lies strictly between the roots exactly when $f(1) < 0$: $1 + 2k - 2 + k + 5 = 3k + 4 < 0$, so $k < -\frac{4}{3}$. This already forces real distinct roots.",
  "Not knowing that $af(1) < 0$ alone characterises the situation.",
  "U02-location-k-between", "One evaluation and a sign rule.",
  check=_c033, values=[Interval.open(-oo, Rational(-4, 3)), Interval(-oo, Rational(-4, 3)), Interval.open(Rational(-4, 3), oo),
                       Union(Interval.open(-oo, -1), Interval.open(4, oo))], cognitive="Application")

# ---------------------------------------------------------------- 034
q("U02-C-034", "Equations reducible to quadratics", "Substitution t = x + 1/x", "Medium", "Multi-step computation MCQ",
  r"The number of distinct real solutions of $\left(x + \frac{1}{x}\right)^2 - 5\left(x + \frac{1}{x}\right) + 6 = 0$ is",
  r"$3$",
  [(r"$4$", "Counts the repeated root $x = 1$ from $x + \\frac{1}{x} = 2$ twice."),
   (r"$2$", "Rejects $t = 2$, thinking $x + \\frac{1}{x} = 2$ has no real solution."),
   (r"$1$", "Rejects $t = 3$ and keeps only $x = 1$.")],
  r"Put $t = x + \frac{1}{x}$: $t^2 - 5t + 6 = 0$ gives $t = 2$ or $t = 3$. $x + \frac{1}{x} = 2$ gives $(x - 1)^2 = 0$, so $x = 1$. $x + \frac{1}{x} = 3$ gives $x^2 - 3x + 1 = 0$ with $D = 5 > 0$, two more distinct real roots. Total $3$.",
  "Double counting a repeated root.",
  "U02-reciprocal-substitution", "Substitution, then two separate quadratics with a repeated root.",
  check=lambda: len(_rs((x + 1/x)**2 - 5*(x + 1/x) + 6)), values=[3, 4, 2, 1], cognitive="Application",
  numerical=dict(question=r"The number of distinct real solutions of $\left(x + \frac{1}{x}\right)^2 - 5\left(x + \frac{1}{x}\right) + 6 = 0$ is", answer=3))

# ---------------------------------------------------------------- 035
q("U02-C-035", "Equations reducible to quadratics", "Exponential substitution with a rejected root", "Medium", "Multi-step computation MCQ",
  r"The set of all real solutions of $4^x - 2^{x+1} - 8 = 0$ is",
  r"$\{2\}$",
  [(r"$\{-1, 2\}$", "Writes $2^x = -2$ as $x = -1$."),
   (r"$\{1, 2\}$", "Writes $2^x = -2$ as $2^x = 2$ by dropping the sign."),
   (r"$\{4\}$", "Reports $t = 2^x = 4$ instead of $x$.")],
  r"Put $t = 2^x > 0$; then $2^{x+1} = 2t$ and $t^2 - 2t - 8 = 0$, so $t = 4$ or $t = -2$. Since $2^x > 0$, only $2^x = 4$ is admissible, giving $x = 2$.",
  "Not rejecting a negative value of $2^x$.",
  "U02-exponential-reducible", "Substitution, root rejection and back-substitution.",
  check=lambda: _rs(4**x - 2**(x + 1) - 8),
  values=[FiniteSet(2), FiniteSet(-1, 2), FiniteSet(1, 2), FiniteSet(4)], cognitive="Application")

# ---------------------------------------------------------------- 036
q("U02-C-036", "Equations reducible to quadratics", "Modulus equation with casework", "Medium", "Multi-step computation MCQ",
  r"The sum of all real solutions of $x^2 - 4|x - 1| - 1 = 0$ is",
  r"$-1$",
  [(r"$0$", "Counts $x = 1$ twice, once from each case."),
   (r"$4$", "Solves only the case $x \\geq 1$."),
   (r"$-4$", "Solves only the case $x < 1$ and keeps $x = 1$, which lies outside that case.")],
  r"For $x \geq 1$: $x^2 - 4x + 3 = 0$, so $x = 1$ or $3$, both valid. For $x < 1$: $x^2 + 4x - 5 = 0$, so $x = 1$ (rejected, not $< 1$) or $x = -5$. The solutions are $-5, 1, 3$ with sum $-1$.",
  "Not checking each case's roots against the case condition.",
  "U02-modulus-casework", "Two cases, each a quadratic, with root validation.",
  check=lambda: Add(*_rs(x**2 - 4*Abs(x - 1) - 1)), values=[-1, 0, 4, -4], cognitive="Application")

# ---------------------------------------------------------------- 037
def _c037():
    cnt = 0
    for kv in range(-60, 61):
        rts = solve(x**2 + kv*x + 16, x)
        if rts and all(r.is_integer for r in rts):
            cnt += 1
    return cnt
q("U02-C-037", "Quadratic equations", "Integral roots and integer parameter", "Medium", "Inverse/parameter MCQ",
  r"The number of integers $k$ for which both roots of $x^2 + kx + 16 = 0$ are integers (the roots may be equal) is",
  r"$6$",
  [(r"$3$", "Uses only the positive factor pairs $(1, 16), (2, 8), (4, 4)$ and forgets their negatives."),
   (r"$10$", "Counts ordered factor pairs, so $(1, 16)$ and $(16, 1)$ separately: $5$ ordered pairs for each sign."),
   (r"$4$", "Discards the equal-root pairs $\\pm(4, 4)$, i.e. $k = \\pm 8$, assuming the roots must be distinct.")],
  r"Integer roots $r, s$ need $rs = 16$ and $k = -(r + s)$. The unordered pairs are $(1, 16), (2, 8), (4, 4)$ and their negatives, giving $k = \mp 17, \mp 10, \mp 8$; for $k = \pm 8$ the root is repeated, which is allowed. Equivalently $k^2 - 64$ must be a perfect square. So there are $6$ values.",
  "Ignoring negative factor pairs or the equal-root case.",
  "U02-integral-roots-count", "Discriminant as a perfect square plus systematic counting.",
  check=_c037, values=[6, 3, 10, 4], cognitive="Analysis",
  numerical=dict(question=r"The number of integers $k$ for which both roots of $x^2 + kx + 16 = 0$ are integers (the roots may be equal) is", answer=6))

# ---------------------------------------------------------------- 038
def _c038():
    p, qq = symbols('p q', rational=True)
    r0 = 2 + sqrt(3)
    e = expand(r0**2 + p*r0 + qq)
    s = solve([e.coeff(sqrt(3), 0), e.coeff(sqrt(3), 1)], [p, qq], dict=True)[0]
    s1 = s[qq] == 1
    # Statement II: counterexample with real coefficients
    poly = expand((x - r0)*(x - 1))
    s2 = simplify(poly.subs(x, 2 - sqrt(3))) == 0
    return (bool(s1), bool(s2))
q("U02-C-038", "Quadratic equations", "Irrational roots with rational coefficients", "Medium", "Statement-based MCQ",
  r"Statement I: If $p$ and $q$ are rational and $2 + \sqrt{3}$ is a root of $x^2 + px + q = 0$, then $q = 1$. Statement II: If $p$ and $q$ are real and $2 + \sqrt{3}$ is a root of $x^2 + px + q = 0$, then $2 - \sqrt{3}$ must also be a root. In the light of the above statements, choose the correct answer.",
  ST_OPTS[2],
  [(ST_OPTS[0], "Extends the surd-conjugate rule from rational to real coefficients."),
   (ST_OPTS[1], "Computes the product of the roots as $(2 + \\sqrt{3})(2 - \\sqrt{3}) = 4 + 3 = 7$, so rejects Statement I, and correctly rejects Statement II."),
   (ST_OPTS[3], "Confuses which hypothesis (rational or real) the surd-conjugate rule needs.")],
  r"With rational $p, q$: $(7 + 4\sqrt{3}) + p(2 + \sqrt{3}) + q = 0$ forces $4 + p = 0$ and $7 + 2p + q = 0$, so $p = -4$, $q = 1$; Statement I is true. With only real coefficients, $(x - 2 - \sqrt{3})(x - 1) = 0$ has root $2 + \sqrt{3}$ but not $2 - \sqrt{3}$; Statement II is false.",
  "Applying the irrational-conjugate rule without rational coefficients.",
  "U02-statement-surd-conj", "Comparing rational and irrational parts, plus constructing a counterexample.",
  check=_c038, values=[ST_VALS[ST_OPTS[2]], ST_VALS[ST_OPTS[0]], ST_VALS[ST_OPTS[1]], ST_VALS[ST_OPTS[3]]],
  cognitive="Analysis")

# ---------------------------------------------------------------- 039
q("U02-C-039", "Quadratic expressions", "Range on a closed interval", "Medium", "Multi-step computation MCQ",
  r"The set of values of $x^2 - 4x + 1$ as $x$ varies over $[0, 5]$ is",
  r"$[-3, 6]$",
  [(r"$[1, 6]$", "Uses only the endpoint values $f(0) = 1$ and $f(5) = 6$."),
   (r"$[-3, 1]$", "Compares the vertex value only with $f(0)$."),
   (r"$(-3, 6)$", "Excludes attained extreme values.")],
  r"$f(x) = (x - 2)^2 - 3$. The vertex $x = 2$ lies in $[0, 5]$, so the least value is $f(2) = -3$. The greatest value is at the endpoint farther from $2$, namely $f(5) = 6$ (while $f(0) = 1$). By continuity the set of values is $[-3, 6]$.",
  "Ignoring an interior vertex or the farther endpoint.",
  "U02-range-on-interval", "Vertex location plus endpoint comparison.",
  check=lambda: function_range(x**2 - 4*x + 1, x, Interval(0, 5)),
  values=[Interval(-3, 6), Interval(1, 6), Interval(-3, 1), Interval.open(-3, 6)], cognitive="Application")

# ---------------------------------------------------------------- 040
def _c040():
    e = x**2 + k*x - 4
    base = _kset(e.subs(x, 1) * e.subs(x, 2) < 0)

    def one_in(kv):
        rr = [r for r in solve(e.subs(k, kv), x) if r.is_real]
        return sum(1 for r in set(rr) if 1 < r < 2) == 1
    ends = [b for b in (base.inf, base.sup) if b.is_finite]
    extra = FiniteSet(*[b for b in ends if one_in(b)])
    # sample check outside base
    for kv in [Rational(-3), Rational(-1, 2), Rational(7, 2), 10]:
        assert not one_in(kv)
    return Union(base, extra)
q("U02-C-040", "Location of roots", "Exactly one root in an interval", "Medium", "Inverse/parameter MCQ",
  r"The equation $x^2 + kx - 4 = 0$ has exactly one root in the open interval $(1, 2)$ if and only if $k$ belongs to",
  r"$(0, 3)$",
  [(r"$[0, 3]$", "Uses $f(1)f(2) \\leq 0$; at $k = 0$ and $k = 3$ the root falls at an endpoint, outside the open interval."),
   (r"$(-\infty, 0) \cup (3, \infty)$", "Uses $f(1)f(2) > 0$."),
   (r"$(-3, 0)$", "Sign slip: takes $f(1) = -k - 3$ and $f(2) = -2k$.")],
  r"Let $f(x) = x^2 + kx - 4$. The product of roots is $-4 < 0$, so the roots have opposite signs and both cannot lie in $(1, 2)$. Exactly one root lies in $(1, 2)$ when $f(1)f(2) < 0$: $(k - 3)(2k) < 0$, i.e. $0 < k < 3$. At $k = 0$ the roots are $\pm 2$ and at $k = 3$ they are $1, -4$, so neither endpoint works.",
  "Including endpoints where a root sits on the boundary.",
  "U02-location-one-root-interval", "Sign change test plus endpoint analysis.",
  check=_c040, values=[Interval.open(0, 3), Interval(0, 3), Union(Interval.open(-oo, 0), Interval.open(3, oo)), Interval.open(-3, 0)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 041
def _c041():
    a, b = symbols('a b', real=True)
    kk = Symbol('kk', real=True, nonzero=True)
    d = discriminant((x - a)*(x - b) - kk**2, x)
    assert expand(d - ((a - b)**2 + 4*kk**2)) == 0
    pos = ((a - b)**2 + 4*kk**2).is_positive
    return 1 if pos else 0
q("U02-C-041", "Quadratic equations", "Nature of roots with literal coefficients", "Medium", "Conceptual/application MCQ",
  r"Let $a, b, k$ be real numbers with $k \neq 0$. The roots of $(x - a)(x - b) = k^2$ are",
  r"real and distinct",
  [(r"real and equal", "Treats $a = b$ as forcing equal roots, ignoring the $4k^2$ term."),
   (r"non-real complex conjugates", "Sign slip: takes $D = (a - b)^2 - 4k^2$ and assumes it negative."),
   (r"real and distinct only when $a \neq b$", "Sees the $(a - b)^2$ term but overlooks the strictly positive $4k^2$ term when $a = b$.")],
  r"The equation is $x^2 - (a + b)x + ab - k^2 = 0$, so $D = (a + b)^2 - 4ab + 4k^2 = (a - b)^2 + 4k^2$. Since $k \neq 0$, $D \geq 4k^2 > 0$, so the roots are always real and distinct.",
  "Sign error when expanding $-4(ab - k^2)$.",
  "U02-nature-symbolic", "Symbolic discriminant simplified to a sum of squares.",
  check=_c041, values=[1, 2, 3, 4], cognitive="Understanding")

# ================================================================= DIFFICULT
# ---------------------------------------------------------------- 042
def _c042():
    e = x**2 - 2*k*x + k**2 + k - 5
    c = Poly(e, x).all_coeffs()
    s = Intersection(_kset(discriminant(e, x) >= 0), _kset(-c[1]/(2*c[0]) < 5), _kset(e.subs(x, 5) > 0))
    # direct cross-check: larger root k + sqrt(5 - k) < 5
    s2 = Intersection(_kset(k + sqrt(5 - k) < 5), Interval(-oo, 5))
    assert s == s2
    return s
q("U02-C-042", "Location of roots", "Both roots less than a given number", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which both roots of $x^2 - 2kx + k^2 + k - 5 = 0$ (not necessarily distinct) are real and strictly less than $5$ is",
  r"$(-\infty, 4)$",
  [(r"$(-\infty, 5]$", "Imposes only $D \\geq 0$."),
   (r"$(-\infty, 4]$", "Uses $f(5) \\geq 0$; at $k = 4$ the larger root equals $5$."),
   (r"$(4, 5)$", "Uses $f(5) < 0$, the condition for $5$ to lie between the roots.")],
  r"Let $f(x) = x^2 - 2kx + k^2 + k - 5$. Need $\frac{D}{4} = 5 - k \geq 0$, vertex $k < 5$, and $f(5) = k^2 - 9k + 20 = (k - 4)(k - 5) > 0$. These give $k \leq 5$, $k < 5$, and $k < 4$ or $k > 5$; together $k < 4$. Check: the larger root is $k + \sqrt{5 - k}$, and $k + \sqrt{5 - k} < 5$ iff $\sqrt{5 - k} < 5 - k$ iff $5 - k > 1$.",
  "Using a non-strict boundary condition or the wrong sign of $f(5)$.",
  "U02-location-both-less-than-k", "Three conditions (reality, vertex, endpoint value) with strict/non-strict care.",
  check=_c042, values=[Interval.open(-oo, 4), Interval(-oo, 5), Interval(-oo, 4), Interval.open(4, 5)], cognitive="Analysis")

# ---------------------------------------------------------------- 043
q("U02-C-043", "Quadratic expressions", "Minimum of a quadratic in a quadratic", "Difficult", "Multi-step computation MCQ",
  r"The minimum value of $(x^2 - 2x)^2 + 4(x^2 - 2x) + 7$ over all real $x$ is",
  r"$4$",
  [(r"$3$", "Minimises $t^2 + 4t + 7$ at $t = -2$, but $t = x^2 - 2x \\geq -1$ cannot be $-2$."),
   (r"$7$", "Takes the value at $x = 0$, i.e. $t = 0$."),
   (r"$-1$", "Reports the least value of $t = x^2 - 2x$.")],
  r"Let $t = x^2 - 2x = (x - 1)^2 - 1$, so $t \geq -1$. Then $g(t) = t^2 + 4t + 7 = (t + 2)^2 + 3$, whose vertex $t = -2$ lies outside $[-1, \infty)$. On $[-1, \infty)$, $g$ is increasing, so the minimum is $g(-1) = 1 - 4 + 7 = 4$, attained at $x = 1$.",
  "Ignoring the restricted range of the substituted variable.",
  "U02-min-composite", "Substitution, range of the new variable, vertex outside the domain.",
  check=lambda: minimum((x**2 - 2*x)**2 + 4*(x**2 - 2*x) + 7, x, R), values=[4, 3, 7, -1], cognitive="Analysis")

# ---------------------------------------------------------------- 044
def _c044():
    rg = function_range((2*x**2 - 3*x + 2)/(2*x**2 + 3*x + 2), x, R)
    return sum(1 for n in range(-100, 101) if rg.contains(n) == True)
q("U02-C-044", "Range of rational functions", "Integers in the range", "Difficult", "Multi-step computation MCQ",
  r"The number of integers in the range of $f(x) = \frac{2x^2 - 3x + 2}{2x^2 + 3x + 2}$, $x \in \mathbb{R}$, is",
  r"$7$",
  [(r"$6$", "Takes the range as the open interval $\\left(\\frac{1}{7}, 7\\right)$, losing $7$."),
   (r"$5$", "Uses the open interval and also excludes $y = 1$, where the equation in $x$ becomes linear."),
   (r"$8$", "Counts $0$ as well, taking the range as $[0, 7]$.")],
  r"The denominator has $D = 9 - 16 < 0$, so it is always positive. With $y = f(x)$: $2(y - 1)x^2 + 3(y + 1)x + 2(y - 1) = 0$. For $y \neq 1$, real $x$ needs $9(y + 1)^2 - 16(y - 1)^2 \geq 0$, i.e. $(7 - y)(7y - 1) \geq 0$, so $\frac{1}{7} \leq y \leq 7$; $y = 1$ occurs at $x = 0$. The range is $\left[\frac{1}{7}, 7\right]$, containing the integers $1, 2, \ldots, 7$, i.e. $7$ integers.",
  "Mishandling endpoint attainment or the degenerate value $y = 1$.",
  "U02-range-rational-count", "Discriminant method, factorising a quadratic inequality, endpoint and degenerate case, then counting.",
  check=_c044, values=[7, 6, 5, 8], cognitive="Analysis",
  numerical=dict(question=r"The number of integers in the range of $f(x) = \frac{2x^2 - 3x + 2}{2x^2 + 3x + 2}$, $x \in \mathbb{R}$, is", answer=7))

# ---------------------------------------------------------------- 045
q("U02-C-045", "Range of rational functions", "Range with a removable factor", "Difficult", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{x^2 - 3x + 2}{x^2 + x - 6}$, over its natural domain, is",
  r"$\mathbb{R} \setminus \left\{\frac{1}{5}, 1\right\}$",
  [(r"$\mathbb{R} \setminus \{1\}$", "Cancels $x - 2$ but forgets that $x = 2$ is still excluded, so $\\frac{1}{5}$ is missed."),
   (r"$\mathbb{R} \setminus \left\{\frac{1}{5}\right\}$", "Forgets that the simplified function $\\frac{x - 1}{x + 3}$ never equals $1$."),
   (r"$\mathbb{R}$", "Applies the discriminant method without checking excluded points.")],
  r"$f(x) = \frac{(x - 1)(x - 2)}{(x + 3)(x - 2)} = \frac{x - 1}{x + 3}$ for $x \neq 2, -3$. The function $\frac{x - 1}{x + 3} = 1 - \frac{4}{x + 3}$ takes every real value except $1$ on $x \neq -3$. Removing $x = 2$ also removes the value $\frac{2 - 1}{2 + 3} = \frac{1}{5}$. So the range is $\mathbb{R} \setminus \left\{\frac{1}{5}, 1\right\}$.",
  "Forgetting the value lost at a cancelled factor.",
  "U02-range-rational-hole", "Factorisation, domain restriction, and the value lost at the hole.",
  check=lambda: function_range((x**2 - 3*x + 2)/(x**2 + x - 6), x,
                               Union(Interval.open(-oo, -3), Interval.open(-3, 2), Interval.open(2, oo))),
  values=[Complement(R, FiniteSet(Rational(1, 5), 1)), Complement(R, FiniteSet(1)), Complement(R, FiniteSet(Rational(1, 5))), R],
  cognitive="Analysis")

# ---------------------------------------------------------------- 046
q("U02-C-046", "Equations reducible to quadratics", "Counting solutions of a modulus equation", "Difficult", "Multi-step computation MCQ",
  r"The number of distinct real solutions of $|x^2 - 4| = x + 2$ is",
  r"$3$",
  [(r"$4$", "Counts $x = -2$ twice, once from each case."),
   (r"$2$", "Solves only $x^2 - 4 = x + 2$."),
   (r"$5$", "Takes all roots from both cases and also adds $x = 2$ where $x^2 - 4 = 0$.")],
  r"We need $x + 2 \geq 0$. Case $x^2 - 4 = x + 2$: $x^2 - x - 6 = 0$, so $x = 3$ or $x = -2$. Case $x^2 - 4 = -(x + 2)$: $x^2 + x - 2 = 0$, so $x = 1$ or $x = -2$. Each satisfies $x \geq -2$ and the original equation, e.g. $|1 - 4| = 3 = 1 + 2$. The distinct solutions are $-2, 1, 3$, giving $3$.",
  "Double counting a root shared by two cases.",
  "U02-modulus-count-casework", "Two-case analysis, validation, and de-duplication.",
  check=lambda: len(_rs(Abs(x**2 - 4) - x - 2)), values=[3, 4, 2, 5], cognitive="Analysis",
  numerical=dict(question=r"The number of distinct real solutions of $|x^2 - 4| = x + 2$ is", answer=3))

# ---------------------------------------------------------------- 047
q("U02-C-047", "Equations reducible to quadratics", "Substitution t = |x - a|", "Difficult", "Multi-step computation MCQ",
  r"The product of all real roots of $x^2 - 4x - |x - 2| - 2 = 0$ is",
  r"$-5$",
  [(r"$0$", "Accepts $|x - 2| = -2$ as $|x - 2| = 2$, adding the roots $0$ and $4$."),
   (r"$-6$", "Reports the product of the values of $t = |x - 2|$."),
   (r"$5$", "Sign slip: takes the roots as $5$ and $1$.")],
  r"Write $x^2 - 4x = (x - 2)^2 - 4$ and put $t = |x - 2| \geq 0$: $t^2 - 4 - t - 2 = 0$, i.e. $t^2 - t - 6 = 0$, so $t = 3$ or $t = -2$. Only $t = 3$ is admissible, so $x - 2 = \pm 3$, giving $x = 5$ or $x = -1$. The product is $-5$.",
  "Not rejecting a negative value of a modulus.",
  "U02-modulus-substitution", "Completing the square to expose $|x - 2|$, substitution, rejection.",
  check=lambda: Mul(*_rs(x**2 - 4*x - Abs(x - 2) - 2)), values=[-5, 0, -6, 5], cognitive="Analysis")

# ---------------------------------------------------------------- 048
def _c048():
    t = Symbol('t', real=True)
    cnt = 0
    for kv in range(-100, 101):
        pos = set(r for r in solve(t**2 - 5*t + kv, t) if r.is_real and r > 0)
        # each positive t gives exactly one real x = log_2 t
        if len(pos) == 2:
            cnt += 1
    return cnt
q("U02-C-048", "Equations reducible to quadratics", "Exponential equation with a parameter", "Difficult", "Inverse/parameter MCQ",
  r"The number of integers $k$ for which $4^x - 5 \cdot 2^x + k = 0$ has two distinct real solutions is",
  r"$6$",
  [(r"$7$", "Uses product $k \\geq 0$, counting $k = 0$, where the root $t = 0$ is inadmissible."),
   (r"$5$", "Discards $k = 4$, wrongly rejecting the root $t = 1$ (that is $x = 0$)."),
   (r"$2$", "Requires both solutions $x$ to be positive, i.e. both roots $t > 1$, giving only $k = 5, 6$.")],
  r"Put $t = 2^x > 0$: $t^2 - 5t + k = 0$. Each positive $t$ gives exactly one real $x$, so we need two distinct positive roots: $D = 25 - 4k > 0$, sum $5 > 0$, product $k > 0$. Hence $0 < k < \frac{25}{4}$, so $k \in \{1, 2, 3, 4, 5, 6\}$, i.e. $6$ integers.",
  "Forgetting that both values of $2^x$ must be positive.",
  "U02-exponential-param-count", "Substitution turns the question into a location-of-roots condition, then counting.",
  check=_c048, values=[6, 7, 5, 2], cognitive="Analysis",
  numerical=dict(question=r"The number of integers $k$ for which $4^x - 5 \cdot 2^x + k = 0$ has two distinct real solutions is", answer=6))

# ---------------------------------------------------------------- 049
q("U02-C-049", "Equations reducible to quadratics", "Reciprocal quartic", "Difficult", "Multi-step computation MCQ",
  r"The number of distinct real roots of $x^4 - 3x^3 + 4x^2 - 3x + 1 = 0$ is",
  r"$1$",
  [(r"$2$", "Counts the repeated root $x = 1$ twice."),
   (r"$4$", "Assumes each value of $x + \\frac{1}{x}$ gives two real roots."),
   (r"$3$", "Takes $x + \\frac{1}{x} = 1$ as giving one real root and $x + \\frac{1}{x} = 2$ as giving two.")],
  r"$x = 0$ is not a root, so divide by $x^2$: $\left(x^2 + \frac{1}{x^2}\right) - 3\left(x + \frac{1}{x}\right) + 4 = 0$. With $t = x + \frac{1}{x}$, $x^2 + \frac{1}{x^2} = t^2 - 2$, so $t^2 - 3t + 2 = 0$, $t = 1$ or $2$. $x + \frac{1}{x} = 1$ gives $x^2 - x + 1 = 0$ with $D < 0$; $x + \frac{1}{x} = 2$ gives $(x - 1)^2 = 0$. Only $x = 1$ is real.",
  "Ignoring that $|x + \\frac{1}{x}| \\geq 2$ for real $x$, or double counting.",
  "U02-reciprocal-quartic", "Recognise reciprocal symmetry, substitute, then test each case.",
  check=lambda: len(_rs(x**4 - 3*x**3 + 4*x**2 - 3*x + 1)), values=[1, 2, 4, 3], cognitive="Analysis")

# ---------------------------------------------------------------- 050
def _c050():
    e = x**2 - 2*k*x + 4
    s = Intersection(_kset(discriminant(e, x) >= 0), _kset(k > 1), _kset(k < 5),
                     _kset(e.subs(x, 1) > 0), _kset(e.subs(x, 5) > 0))
    return s
q("U02-C-050", "Location of roots", "Both roots in an interval", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which both roots of $x^2 - 2kx + 4 = 0$ (not necessarily distinct) are real and lie in the open interval $(1, 5)$ is",
  r"$\left[2, \frac{5}{2}\right)$",
  [(r"$\left(2, \frac{5}{2}\right)$", "Uses $D > 0$, losing the double root $x = 2$ at $k = 2$."),
   (r"$\left[2, \frac{29}{10}\right)$", "Omits the condition $f(1) > 0$."),
   (r"$\left(1, \frac{5}{2}\right)$", "Omits the reality condition $D \\geq 0$.")],
  r"Let $f(x) = x^2 - 2kx + 4$. Need $\frac{D}{4} = k^2 - 4 \geq 0$, vertex $1 < k < 5$, $f(1) = 5 - 2k > 0$ and $f(5) = 29 - 10k > 0$. These give $|k| \geq 2$, $1 < k < 5$, $k < \frac{5}{2}$, $k < \frac{29}{10}$. Together $2 \leq k < \frac{5}{2}$. At $k = \frac{5}{2}$ the roots are $1$ and $4$, and $1$ is not in the open interval.",
  "Dropping one of the four conditions or mishandling the boundary.",
  "U02-location-both-in-interval", "Four simultaneous conditions with mixed strictness.",
  check=_c050, values=[Interval.Ropen(2, Rational(5, 2)), Interval.open(2, Rational(5, 2)), Interval.Ropen(2, Rational(29, 10)),
                       Interval.open(1, Rational(5, 2))], cognitive="Analysis")

# ---------------------------------------------------------------- 051
def _c051():
    for kv in range(-40, 41):
        e = (kv - 2)*x**2 + 8*x + kv + 4
        if _rs(e <= 0) == S.EmptySet:
            return kv
q("U02-C-051", "Quadratic expressions", "Least integer parameter for positivity", "Difficult", "Inverse/parameter MCQ",
  r"The least integer $k$ for which $(k - 2)x^2 + 8x + k + 4 > 0$ for every real $x$ is",
  r"$5$",
  [(r"$4$", "Uses $D \\leq 0$; at $k = 4$ the expression $2(x + 2)^2$ vanishes at $x = -2$."),
   (r"$3$", "Uses only the leading-coefficient condition $k > 2$."),
   (r"$2$", "Accepts $k = 2$, where the expression becomes the linear $8x + 6$, which is not always positive.")],
  r"If $k = 2$ the expression is $8x + 6$, which is negative for $x < -\frac{3}{4}$. Otherwise we need $k - 2 > 0$ and $\frac{D}{4} = 16 - (k - 2)(k + 4) < 0$, i.e. $k^2 + 2k - 24 > 0$, i.e. $(k + 6)(k - 4) > 0$. With $k > 2$ this gives $k > 4$, so the least integer is $5$.",
  "Using a non-strict discriminant condition or overlooking the degenerate case.",
  "U02-positive-definite-param", "Degenerate case, leading-coefficient sign, strict discriminant, then integer selection.",
  check=_c051, values=[5, 4, 3, 2], cognitive="Analysis",
  numerical=dict(question=r"The least integer $k$ for which $(k - 2)x^2 + 8x + k + 4 > 0$ for every real $x$ is", answer=5))

# ---------------------------------------------------------------- 052
def _c052():
    t = Symbol('t')
    g = t**2 - 2*(k + 1)*t + k + 7
    c = Poly(g, t).all_coeffs()
    s = Intersection(_kset(discriminant(g, t) > 0), _kset(-c[1]/c[0] > 0), _kset(c[2]/c[0] > 0))
    # spot check with the quartic itself
    for kv, ok in [(3, True), (2, False), (Rational(5, 2), True), (-4, False), (0, False)]:
        n = len(_rs(x**4 - 2*(kv + 1)*x**2 + kv + 7))
        assert (n == 4) == ok, (kv, n)
    return s
q("U02-C-052", "Equations reducible to quadratics", "Biquadratic with a parameter", "Difficult", "Inverse/parameter MCQ",
  r"The equation $x^4 - 2(k + 1)x^2 + k + 7 = 0$ has four distinct real roots if and only if $k$ belongs to",
  r"$(2, \infty)$",
  [(r"$[2, \infty)$", "Uses $D \\geq 0$; at $k = 2$, $x^2 = 3$ is a double value giving only two roots."),
   (r"$(-7, -3) \cup (2, \infty)$", "Ignores the condition that the sum of the values of $x^2$ is positive."),
   (r"$(-1, \infty)$", "Ignores the discriminant condition.")],
  r"Put $t = x^2$: $t^2 - 2(k + 1)t + k + 7 = 0$. Four distinct real $x$ need two distinct positive $t$: $\frac{D}{4} = (k + 1)^2 - (k + 7) = (k + 3)(k - 2) > 0$, sum $2(k + 1) > 0$, product $k + 7 > 0$. So $k < -3$ or $k > 2$; $k > -1$; $k > -7$. Together $k > 2$.",
  "Not requiring both values of $x^2$ to be distinct and positive.",
  "U02-biquadratic-param", "Reduction to a location-of-roots problem with three conditions.",
  check=_c052, values=[Interval.open(2, oo), Interval(2, oo), Union(Interval.open(-7, -3), Interval.open(2, oo)), Interval.open(-1, oo)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 053
def _c053():
    e = (k - 1)*x**2 - (k + 1)*x + (k + 1)
    a = Poly(e, x).coeff_monomial(x**2)
    s = _kset(a * e.subs(x, 2) < 0)
    # spot check by explicit roots
    for kv, ok in [(Rational(4, 3), True), (Rational(3, 2), True), (Rational(1, 2), False), (2, False), (-1, False)]:
        rr = sorted([r for r in solve(e.subs(k, kv), x) if r.is_real])
        inside = len(rr) == 2 and rr[0] < 2 < rr[1]
        assert inside == ok, (kv, rr)
    return s
q("U02-C-053", "Location of roots", "A number between the roots with a parametric leading coefficient", "Difficult", "Inverse/parameter MCQ",
  r"Let $k \neq 1$ be real. The number $2$ lies strictly between the roots of $(k - 1)x^2 - (k + 1)x + (k + 1) = 0$ if and only if $k$ belongs to",
  r"$\left(1, \frac{5}{3}\right)$",
  [(r"$\left(-\infty, \frac{5}{3}\right)$", "Uses $f(2) < 0$, ignoring the sign of the leading coefficient $k - 1$."),
   (r"$(-\infty, 1) \cup \left(\frac{5}{3}, \infty\right)$", "Uses $(k - 1)f(2) > 0$."),
   (r"$\left(\frac{5}{3}, \infty\right)$", "Uses $f(2) > 0$.")],
  r"For $a x^2 + bx + c$ with $a \neq 0$, a number lies strictly between the roots iff $a \cdot f(\text{number}) < 0$. Here $f(2) = 4(k - 1) - 2(k + 1) + (k + 1) = 3k - 5$, so we need $(k - 1)(3k - 5) < 0$, i.e. $1 < k < \frac{5}{3}$. For example $k = \frac{3}{2}$ gives $x^2 - 5x + 5 = 0$ with roots $\frac{5 \pm \sqrt{5}}{2}$, on either side of $2$.",
  "Using $f(2) < 0$ without multiplying by the leading coefficient.",
  "U02-location-k-between", "The $af(k) < 0$ criterion with a parameter-dependent leading coefficient.",
  check=_c053, values=[Interval.open(1, Rational(5, 3)), Interval.open(-oo, Rational(5, 3)),
                       Union(Interval.open(-oo, 1), Interval.open(Rational(5, 3), oo)), Interval.open(Rational(5, 3), oo)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 054
def _c054():
    num = x**2 + k*x + 1
    den = x**2 + x + 1
    assert _rs(den <= 0) == S.EmptySet
    up = 3*den - num        # must be > 0 for all x
    lo = num + den          # must be > 0 for all x (leading coeff 2 > 0)
    return Intersection(_kset(discriminant(up, x) < 0), _kset(discriminant(lo, x) < 0))
q("U02-C-054", "Range of rational functions", "Parameter for a bounded rational expression", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $-1 < \frac{x^2 + kx + 1}{x^2 + x + 1} < 3$ for every real $x$ is",
  r"$(-1, 3)$",
  [(r"$(-1, 7)$", "Imposes only the upper bound $< 3$."),
   (r"$(-5, 3)$", "Imposes only the lower bound $> -1$."),
   (r"$[-1, 3]$", "Uses $D \\leq 0$; at $k = -1$ the value $3$ is attained at $x = -1$, and at $k = 3$ the value $-1$ is attained at $x = -1$.")],
  r"Since $x^2 + x + 1 > 0$ for all $x$, multiply through. Upper: $3x^2 + 3x + 3 - x^2 - kx - 1 = 2x^2 + (3 - k)x + 2 > 0$ for all $x$ needs $(3 - k)^2 < 16$, i.e. $-1 < k < 7$. Lower: $x^2 + kx + 1 + x^2 + x + 1 = 2x^2 + (k + 1)x + 2 > 0$ needs $(k + 1)^2 < 16$, i.e. $-5 < k < 3$. Both together give $-1 < k < 3$.",
  "Imposing only one of the two bounds, or using a non-strict condition.",
  "U02-rational-bounded-param", "Two positivity conditions, each reduced to a discriminant inequality, then intersected.",
  check=_c054, values=[Interval.open(-1, 3), Interval.open(-1, 7), Interval.open(-5, 3), Interval(-1, 3)], cognitive="Analysis")

# ---------------------------------------------------------------- 055
q("U02-C-055", "Equations reducible to quadratics", "Quadratic in a quadratic", "Difficult", "Multi-step computation MCQ",
  r"The number of distinct real solutions of $(x^2 - 2x)^2 - 2(x^2 - 2x) - 3 = 0$ is",
  r"$3$",
  [(r"$4$", "Counts the repeated root $x = 1$ from $x^2 - 2x = -1$ twice."),
   (r"$2$", "Rejects $t = -1$, believing $x^2 - 2x$ cannot be negative."),
   (r"$1$", "Rejects $t = 3$ and keeps only the root from $t = -1$.")],
  r"Put $t = x^2 - 2x = (x - 1)^2 - 1 \geq -1$: $t^2 - 2t - 3 = 0$ gives $t = 3$ or $t = -1$, both admissible. $x^2 - 2x = 3$ gives $x = 3, -1$; $x^2 - 2x = -1$ gives $(x - 1)^2 = 0$, so $x = 1$. The distinct solutions are $-1, 1, 3$, giving $3$.",
  "Double counting a repeated root or wrongly rejecting a negative $t$.",
  "U02-substitution-quadratic-in-quadratic", "Substitution with a restricted range, then counting distinct roots.",
  check=lambda: len(_rs((x**2 - 2*x)**2 - 2*(x**2 - 2*x) - 3)), values=[3, 4, 2, 1], cognitive="Analysis",
  numerical=dict(question=r"The number of distinct real solutions of $(x^2 - 2x)^2 - 2(x^2 - 2x) - 3 = 0$ is", answer=3))
