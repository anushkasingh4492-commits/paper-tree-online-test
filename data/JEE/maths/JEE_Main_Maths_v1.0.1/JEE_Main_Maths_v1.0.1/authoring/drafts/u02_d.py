import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x')


def rts(p):
    P = Poly(expand(p), x)
    out = []
    for r_, m_ in roots(P).items():
        out += [r_] * m_
    assert len(out) == 2
    return out


def mon(e):
    return Poly(expand(e), x).monic().as_expr()


def formed(p, f):
    a_, b_ = rts(p)
    u, v = f(a_, b_), f(b_, a_)
    return x**2 - simplify(expand(u + v)) * x + simplify(expand(u * v))


def sym(p, f):
    a_, b_ = rts(p)
    return simplify(expand(f(a_, b_)))


def S(p, n):
    a_, b_ = rts(p)
    return simplify(expand(a_**n + b_**n))


def equal_poly(f, g):
    return simplify(mon(f) - mon(g)) == 0


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

# ============================ EASY ============================

q("U02-D-001", "Roots and coefficients", "Sum of reciprocals of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 7x + 4 = 0$, then $\frac{1}{\alpha} + \frac{1}{\beta}$ equals",
  r"$\frac{7}{4}$",
  [(r"$\frac{4}{7}$", r"Inverts the ratio: computes $\frac{\alpha\beta}{\alpha+\beta} = \frac{4}{7}$."),
   (r"$-\frac{7}{4}$", r"Takes $\alpha + \beta = -7$ (sign slip in $-\frac{b}{a}$), giving $\frac{-7}{4}$."),
   (r"$\frac{1}{7}$", r"Treats $\frac{1}{\alpha} + \frac{1}{\beta}$ as $\frac{1}{\alpha + \beta} = \frac{1}{7}$.")],
  r"$\alpha + \beta = 7$ and $\alpha\beta = 4$. Hence $\frac{1}{\alpha} + \frac{1}{\beta} = \frac{\alpha + \beta}{\alpha\beta} = \frac{7}{4}$.",
  r"Treating $\frac{1}{\alpha} + \frac{1}{\beta}$ as $\frac{1}{\alpha + \beta}$.",
  "U02-recip-sum", r"One identity, $\frac{\alpha+\beta}{\alpha\beta}$, and one substitution.",
  check=lambda: sym(x**2 - 7*x + 4, lambda a, b: 1/a + 1/b),
  values=[Rational(7, 4), Rational(4, 7), Rational(-7, 4), Rational(1, 7)], cognitive="Application")

q("U02-D-002", "Roots and coefficients", "Sum of squares of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $2x^2 + 5x - 1 = 0$, then $\alpha^2 + \beta^2$ equals",
  r"$\frac{29}{4}$",
  [(r"$\frac{21}{4}$", r"Takes $\alpha\beta = +\frac{1}{2}$: $\frac{25}{4} - 1 = \frac{21}{4}$."),
   (r"$\frac{25}{4}$", r"Uses $(\alpha+\beta)^2 = \frac{25}{4}$ and drops $-2\alpha\beta$."),
   (r"$\frac{27}{4}$", r"Subtracts $\alpha\beta$ once instead of $2\alpha\beta$: $\frac{25}{4} + \frac{1}{2} = \frac{27}{4}$.")],
  r"$\alpha + \beta = -\frac{5}{2}$, $\alpha\beta = -\frac{1}{2}$. So $\alpha^2 + \beta^2 = (\alpha+\beta)^2 - 2\alpha\beta = \frac{25}{4} + 1 = \frac{29}{4}$.",
  r"Wrong sign of $\alpha\beta$ when $c < 0$, or dropping $-2\alpha\beta$.",
  "U02-sum-squares", r"One identity $(\alpha+\beta)^2 - 2\alpha\beta$ with fractional values.",
  check=lambda: sym(2*x**2 + 5*x - 1, lambda a, b: a**2 + b**2),
  values=[Rational(29, 4), Rational(21, 4), Rational(25, 4), Rational(27, 4)])

q("U02-D-003", "Formation of quadratic equations", "Equation from a squared surd root", "Easy", "Single-step computation MCQ",
  r"If one root of a quadratic equation with rational coefficients and leading coefficient $1$ is $(\sqrt{3} - 1)^2$, then the equation is",
  r"$x^2 - 8x + 4 = 0$",
  [(r"$x^2 + 8x + 4 = 0$", r"Writes $x^2 + (\text{sum})x + \text{product}$, a sign slip in the linear term."),
   (r"$x^2 - 8x + 13 = 0$", r"Expands $(\sqrt{3} - 1)^2$ as $4 - \sqrt{3}$, dropping the factor $2$ in the middle term; the roots $4 \pm \sqrt{3}$ give sum $8$ and product $16 - 3 = 13$."),
   (r"$x^2 - 8x + 28 = 0$", r"Computes the product $(4 - 2\sqrt{3})(4 + 2\sqrt{3})$ as $16 + 12 = 28$.")],
  r"$(\sqrt{3} - 1)^2 = 3 - 2\sqrt{3} + 1 = 4 - 2\sqrt{3}$. With rational coefficients the other root is $4 + 2\sqrt{3}$. Sum of roots $= 8$, product $= 16 - 12 = 4$, so the equation is $x^2 - 8x + 4 = 0$.",
  r"Expanding $(\sqrt{a} - b)^2$ without the middle term $2b\sqrt{a}$, or the product $(p + q\sqrt{r})(p - q\sqrt{r}) = p^2 - q^2 r$.",
  "U02-form-squared-surd-root", r"Expand one square, then conjugate surd root with sum and product.",
  check=lambda: mon(expand((x - expand((sqrt(3) - 1)**2)) * (x - (4 + 2*sqrt(3))))),
  values=[mon(x**2 - 8*x + 4), mon(x**2 + 8*x + 4), mon(x**2 - 8*x + 13), mon(x**2 - 8*x + 28)])

q("U02-D-004", "Formation of quadratic equations", "Roots reciprocal", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $2x^2 - 7x + 3 = 0$, then the equation whose roots are $\frac{1}{\alpha}$ and $\frac{1}{\beta}$ is",
  r"$3x^2 - 7x + 2 = 0$",
  [(r"$3x^2 + 7x + 2 = 0$", r"Takes the new sum as $-\frac{7}{3}$ (sign slip)."),
   (r"$2x^2 + 7x + 3 = 0$", r"Replaces $x$ by $-x$, which gives the roots $-\alpha, -\beta$."),
   (r"$21x^2 - 6x + 14 = 0$", r"Takes the new sum as $\frac{1}{\alpha+\beta} = \frac{2}{7}$ with product $\frac{2}{3}$.")],
  r"Replacing $x$ by $\frac{1}{x}$: $\frac{2}{x^2} - \frac{7}{x} + 3 = 0$, i.e. $3x^2 - 7x + 2 = 0$. Check: new sum $= \frac{\alpha+\beta}{\alpha\beta} = \frac{7/2}{3/2} = \frac{7}{3}$, new product $= \frac{2}{3}$.",
  r"Confusing the roots $\frac{1}{\alpha}, \frac{1}{\beta}$ with $-\alpha, -\beta$.",
  "U02-transform-reciprocal", r"One substitution $x \to \frac{1}{x}$.",
  check=lambda: formed(2*x**2 - 7*x + 3, lambda a, b: 1/a),
  values=[mon(3*x**2 - 7*x + 2), mon(3*x**2 + 7*x + 2), mon(2*x**2 + 7*x + 3), mon(21*x**2 - 6*x + 14)])


def _c5():
    k = Symbol('k')
    kv = solve((2*x**2 - 9*x + k).subs(x, 3), k)[0]
    rr = rts(2*x**2 - 9*x + kv)
    return [r_ for r_ in rr if r_ != 3][0]


q("U02-D-005", "Roots and coefficients", "Other root from one known root", "Easy", "Single-step computation MCQ",
  r"If $3$ is a root of $2x^2 - 9x + k = 0$, then the other root is",
  r"$\frac{3}{2}$",
  [(r"$6$", r"Takes the sum of roots as $9$, not dividing by $a = 2$: $9 - 3 = 6$."),
   (r"$-\frac{3}{2}$", r"Subtracts in the wrong order: $3 - \frac{9}{2} = -\frac{3}{2}$."),
   (r"$3$", r"Finds $k = 9$, then takes the product of roots as $k$ instead of $\frac{k}{2}$: $\frac{9}{3} = 3$.")],
  r"Sum of roots $= \frac{9}{2}$, so the other root is $\frac{9}{2} - 3 = \frac{3}{2}$. (Also $k = 9$ and $3 \cdot \frac{3}{2} = \frac{9}{2} = \frac{k}{2}$.)",
  r"Ignoring the leading coefficient in $-\frac{b}{a}$ or $\frac{c}{a}$.",
  "U02-other-root-given-one", "One relation used once.",
  check=_c5, values=[Rational(3, 2), 6, Rational(-3, 2), 3])

q("U02-D-006", "Roots and coefficients", "Sum of cubes of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x - 2 = 0$, then $\alpha^3 + \beta^3$ equals",
  r"$45$",
  [(r"$9$", r"Uses $\alpha\beta = +2$: $27 - 3(2)(3) = 9$."),
   (r"$27$", r"Takes $\alpha^3 + \beta^3 = (\alpha+\beta)^3 = 27$."),
   (r"$33$", r"Subtracts $3\alpha\beta$ without the factor $(\alpha+\beta)$: $27 - 3(-2) = 33$.")],
  r"$\alpha+\beta = 3$, $\alpha\beta = -2$. $\alpha^3+\beta^3 = (\alpha+\beta)^3 - 3\alpha\beta(\alpha+\beta) = 27 + 18 = 45$.",
  r"Treating $\alpha^3 + \beta^3$ as $(\alpha+\beta)^3$.",
  "U02-sum-cubes", r"One identity $s^3 - 3ps$; signs need care.",
  check=lambda: sym(x**2 - 3*x - 2, lambda a, b: a**3 + b**3), values=[45, 9, 27, 33],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x - 2 = 0$, then the value of $\alpha^3 + \beta^3$ is", answer=45))

q("U02-D-007", "Roots and coefficients", "Difference of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 6x + 4 = 0$, then $|\alpha - \beta|$ equals",
  r"$2\sqrt{5}$",
  [(r"$4\sqrt{2}$", r"Uses $(\alpha-\beta)^2 = (\alpha+\beta)^2 - \alpha\beta = 32$."),
   (r"$2\sqrt{13}$", r"Uses $(\alpha-\beta)^2 = (\alpha+\beta)^2 + 4\alpha\beta = 52$."),
   (r"$\sqrt{5}$", r"Halves $\sqrt{20}$, mixing up with the $\frac{\sqrt{D}}{2a}$ in the root formula.")],
  r"$(\alpha-\beta)^2 = (\alpha+\beta)^2 - 4\alpha\beta = 36 - 16 = 20$, so $|\alpha-\beta| = \sqrt{20} = 2\sqrt{5}$.",
  r"Wrong identity for $(\alpha - \beta)^2$.",
  "U02-root-difference", r"One identity and a square root.",
  check=lambda: sym(x**2 - 6*x + 4, lambda a, b: Abs(a - b)),
  values=[2*sqrt(5), 4*sqrt(2), 2*sqrt(13), sqrt(5)])

q("U02-D-008", "Quadratics with complex coefficients", "Sum and product of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - (2+i)x + (3-i) = 0$, then $\alpha + \beta + \alpha\beta$ equals",
  r"$5$",
  [(r"$1 - 2i$", r"Takes $\alpha + \beta = -(2+i)$: $-(2+i) + (3-i) = 1 - 2i$."),
   (r"$-1 + 2i$", r"Takes $\alpha\beta = -(3-i)$: $(2+i) - (3-i) = -1 + 2i$."),
   (r"$-5$", r"Reverses the sign of both: $-(2+i) - (3-i) = -5$.")],
  r"Vieta's relations hold for complex coefficients: $\alpha+\beta = 2+i$, $\alpha\beta = 3-i$. So the required value is $(2+i)+(3-i) = 5$.",
  r"Sign conventions in $\alpha+\beta = -\frac{b}{a}$, $\alpha\beta = \frac{c}{a}$; thinking they fail for complex coefficients.",
  "U02-complex-coeff-vieta", "Direct Vieta with complex numbers.",
  check=lambda: sym(x**2 - (2 + I)*x + (3 - I), lambda a, b: a + b + a*b),
  values=[5, 1 - 2*I, -1 + 2*I, -5], cognitive="Understanding")

q("U02-D-009", "Formation of quadratic equations", "Roots increased by a constant", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x + 1 = 0$, then the equation whose roots are $\alpha + 1$ and $\beta + 1$ is",
  r"$x^2 - 5x + 5 = 0$",
  [(r"$x^2 - x - 1 = 0$", r"Replaces $x$ by $x + 1$, which decreases the roots by $1$."),
   (r"$x^2 - 5x + 2 = 0$", r"Takes the new product as $\alpha\beta + 1 = 2$."),
   (r"$x^2 - 5x + 4 = 0$", r"Expands $(\alpha+1)(\beta+1)$ as $\alpha\beta + \alpha + \beta = 4$, dropping $1$.")],
  r"New sum $= 3 + 2 = 5$; new product $= \alpha\beta + (\alpha+\beta) + 1 = 1 + 3 + 1 = 5$. Equivalently replace $x$ by $x - 1$: $(x-1)^2 - 3(x-1) + 1 = x^2 - 5x + 5$.",
  r"Replacing $x$ by $x + 1$ instead of $x - 1$ to increase the roots.",
  "U02-transform-shift", r"One substitution $x \to x - 1$.",
  check=lambda: formed(x**2 - 3*x + 1, lambda a, b: a + 1),
  values=[mon(x**2 - 5*x + 5), mon(x**2 - x - 1), mon(x**2 - 5*x + 2), mon(x**2 - 5*x + 4)])


def _c10():
    k = Symbol('k', nonzero=True)
    a_, b_ = rts(k*x**2 + 2*x + 3*k)
    return solve(Eq(simplify(a_ + b_), simplify(expand(a_*b_))), k)[0]


q("U02-D-010", "Roots and coefficients", "Parameter from sum equal to product", "Easy", "Inverse/parameter MCQ",
  r"If the sum of the roots of $kx^2 + 2x + 3k = 0$ ($k \neq 0$) is equal to their product, then $k$ equals",
  r"$-\frac{2}{3}$",
  [(r"$\frac{2}{3}$", r"Takes the sum as $+\frac{2}{k}$: $\frac{2}{k} = 3$ gives $k = \frac{2}{3}$."),
   (r"$-\frac{3}{2}$", r"Solves $-\frac{2}{k} = 3$ as $k = \frac{3}{-2}$ (inverts the division)."),
   (r"$\frac{3}{2}$", r"Takes the sum as $+\frac{2}{k}$ and also inverts: $k = \frac{3}{2}$.")],
  r"Sum $= -\frac{2}{k}$, product $= \frac{3k}{k} = 3$. Setting $-\frac{2}{k} = 3$ gives $k = -\frac{2}{3}$.",
  r"Sign of $-\frac{b}{a}$ for the sum of roots.",
  "U02-param-sum-product", r"One equation in $k$.",
  check=_c10, values=[Rational(-2, 3), Rational(2, 3), Rational(-3, 2), Rational(3, 2)])

q("U02-D-011", "Roots and coefficients", "Sum of ratios of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 4x + 2 = 0$, then $\frac{\alpha}{\beta} + \frac{\beta}{\alpha}$ equals",
  r"$6$",
  [(r"$7$", r"Subtracts $\alpha\beta$ once in the numerator: $\frac{16 - 2}{2} = 7$."),
   (r"$8$", r"Uses $(\alpha+\beta)^2$ as the numerator: $\frac{16}{2} = 8$."),
   (r"$10$", r"Adds $2\alpha\beta$ in the numerator: $\frac{16 + 4}{2} = 10$.")],
  r"$\frac{\alpha}{\beta}+\frac{\beta}{\alpha} = \frac{\alpha^2+\beta^2}{\alpha\beta} = \frac{16 - 4}{2} = 6$.",
  r"Dropping or mis-signing $2\alpha\beta$ in $\alpha^2 + \beta^2$.",
  "U02-ratio-sum", "Two identities in one line.",
  check=lambda: sym(x**2 - 4*x + 2, lambda a, b: a/b + b/a), values=[6, 7, 8, 10],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 4x + 2 = 0$, then the value of $\frac{\alpha}{\beta} + \frac{\beta}{\alpha}$ is", answer=6))


def _c12():
    k = Symbol('k')
    a_, b_ = rts(x**2 - 7*x + k)
    return solve(expand((a_ - b_)**2) - 1, k)[0]


q("U02-D-012", "Roots and coefficients", "Roots differing by a constant", "Easy", "Inverse/parameter MCQ",
  r"If the roots of $x^2 - 7x + k = 0$ differ by $1$, then $k$ equals",
  r"$12$",
  [(r"$24$", r"Uses $(\alpha-\beta)^2 = (\alpha+\beta)^2 - 2\alpha\beta$: $49 - 2k = 1$."),
   (r"$48$", r"Uses $(\alpha-\beta)^2 = (\alpha+\beta)^2 - \alpha\beta$: $49 - k = 1$."),
   (r"$\frac{25}{2}$", r"Sets $49 - 4k = -1$ (sign slip on the right side).")],
  r"$(\alpha-\beta)^2 = (\alpha+\beta)^2 - 4\alpha\beta = 49 - 4k = 1$, so $k = 12$ (roots $3$ and $4$).",
  r"Wrong identity for $(\alpha - \beta)^2$.",
  "U02-roots-differ-param", "One identity, one linear equation.",
  check=_c12, values=[12, 24, 48, Rational(25, 2)],
  numerical=dict(question=r"If the roots of $x^2 - 7x + k = 0$ differ by $1$, then the value of $k$ is", answer=12))

q("U02-D-013", "Formation of quadratic equations", "Equation from a complex root", "Easy", "Single-step computation MCQ",
  r"The quadratic equation with real coefficients and leading coefficient $1$, one of whose roots is $3 - 2i$, is",
  r"$x^2 - 6x + 13 = 0$",
  [(r"$x^2 + 6x + 13 = 0$", r"Uses $+(\text{sum})$ for the $x$ coefficient."),
   (r"$x^2 - 6x + 5 = 0$", r"Computes $(3-2i)(3+2i)$ as $9 - 4 = 5$."),
   (r"$x^2 - 3x + 13 = 0$", r"Takes the sum of the roots as the real part $3$ only.")],
  r"With real coefficients the other root is $3 + 2i$. Sum $= 6$, product $= 9 + 4 = 13$, so $x^2 - 6x + 13 = 0$.",
  r"Forgetting that $i^2 = -1$ in the product of conjugates.",
  "U02-form-given-roots", "Conjugate root plus sum and product.",
  check=lambda: mon(expand((x - (3 - 2*I)) * (x - (3 + 2*I)))),
  values=[mon(x**2 - 6*x + 13), mon(x**2 + 6*x + 13), mon(x**2 - 6*x + 5), mon(x**2 - 3*x + 13)])


def _c14():
    p, qq = symbols('p q')
    return sym(x**2 - p*x + qq, lambda a, b: (a + 1)*(b + 1))


_p, _q = symbols('p q')
q("U02-D-014", "Roots and coefficients", "Shifted product of roots", "Easy", "Single-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - px + q = 0$, then $(\alpha + 1)(\beta + 1)$ equals",
  r"$1 + p + q$",
  [(r"$1 - p + q$", r"Takes $\alpha + \beta = -p$."),
   (r"$p + q$", r"Drops the constant $1$ in $\alpha\beta + \alpha + \beta + 1$."),
   (r"$1 + p - q$", r"Takes $\alpha\beta = -q$.")],
  r"$(\alpha+1)(\beta+1) = \alpha\beta + (\alpha+\beta) + 1 = q + p + 1$.",
  r"Sign of $\alpha + \beta$ when the equation is written with $-px$.",
  "U02-product-shifted", "One expansion and Vieta.",
  check=_c14, values=[1 + _p + _q, 1 - _p + _q, _p + _q, 1 + _p - _q], cognitive="Understanding")


def _c15():
    p = x**2 - 4*x + 1
    return (sym(p, lambda a, b: a**2 + b**2) == 14, sym(p, lambda a, b: 1/a + 1/b) == 4)


q("U02-D-015", "Roots and coefficients", "Symmetric functions", "Easy", "Statement-based MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 - 4x + 1 = 0$. Statement I: $\alpha^2 + \beta^2 = 14$. Statement II: $\frac{1}{\alpha} + \frac{1}{\beta} = 4$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Uses $(\alpha+\beta)^2 + 2\alpha\beta = 18$ and $\frac{\alpha\beta}{\alpha+\beta} = \frac{1}{4}$, rejecting both."),
   (ST_TF, r"Computes $\frac{1}{\alpha} + \frac{1}{\beta}$ as $\frac{\alpha\beta}{\alpha+\beta} = \frac{1}{4}$."),
   (ST_FT, r"Computes $\alpha^2 + \beta^2$ as $(\alpha+\beta)^2 = 16$.")],
  r"$\alpha+\beta = 4$, $\alpha\beta = 1$. $\alpha^2+\beta^2 = 16 - 2 = 14$ and $\frac{1}{\alpha}+\frac{1}{\beta} = \frac{4}{1} = 4$. Both statements are true.",
  r"Inverting $\frac{\alpha+\beta}{\alpha\beta}$.",
  "U02-symmetric-statement", "Two one-line identities.",
  check=_c15, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Understanding")


def _c16():
    k = Symbol('k')
    kv = solve((x**2 - (5 + I)*x + k).subs(x, 3), k)[0]
    rr = rts(x**2 - (5 + I)*x + kv)
    return [r_ for r_ in rr if simplify(r_ - 3) != 0][0]


q("U02-D-016", "Quadratics with complex coefficients", "Other root from one known root", "Easy", "Single-step computation MCQ",
  r"If $3$ is a root of $x^2 - (5 + i)x + k = 0$, where $k$ is a complex constant, then the other root is",
  r"$2 + i$",
  [(r"$2 - i$", r"Takes the sum of roots as $5 - i$ (conjugating the coefficient as if roots came in conjugate pairs): $5 - i - 3$."),
   (r"$8 + i$", r"Adds instead of subtracting: $(5 + i) + 3$."),
   (r"$-2 - i$", r"Subtracts in the wrong order: $3 - (5 + i)$.")],
  r"Sum of roots $= 5 + i$, so the other root is $(5 + i) - 3 = 2 + i$. (Then $k = 3(2+i) = 6 + 3i$, consistent with substituting $x = 3$.)",
  r"Applying the conjugate-root property when the coefficients are not real.",
  "U02-complex-coeff-other-root", "One relation; conceptual trap about conjugates.",
  check=_c16, values=[2 + I, 2 - I, 8 + I, -2 - I], cognitive="Understanding")

# ============================ MEDIUM ============================

q("U02-D-017", "Roots and coefficients", "Fourth powers of roots", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x + 1 = 0$, then $\alpha^4 + \beta^4$ equals",
  r"$47$",
  [(r"$49$", r"Squares $\alpha^2 + \beta^2 = 7$ and drops $-2\alpha^2\beta^2$."),
   (r"$51$", r"Adds $2\alpha^2\beta^2$ instead of subtracting: $49 + 2$."),
   (r"$81$", r"Takes $\alpha^4 + \beta^4 = (\alpha+\beta)^4 = 3^4$.")],
  r"$\alpha^2+\beta^2 = 9 - 2 = 7$. Then $\alpha^4+\beta^4 = (\alpha^2+\beta^2)^2 - 2\alpha^2\beta^2 = 49 - 2 = 47$.",
  r"Forgetting $-2\alpha^2\beta^2$ at the second squaring.",
  "U02-fourth-powers", "Two successive squarings with a correction each time.",
  check=lambda: sym(x**2 - 3*x + 1, lambda a, b: a**4 + b**4), values=[47, 49, 51, 81],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x + 1 = 0$, then the value of $\alpha^4 + \beta^4$ is", answer=47))

q("U02-D-018", "Roots and coefficients", "Sum of cubes of roots", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $2x^2 - 3x - 4 = 0$, then $\alpha^3 + \beta^3$ equals",
  r"$\frac{99}{8}$",
  [(r"$-\frac{45}{8}$", r"Takes $\alpha\beta = +2$: $\frac{27}{8} - 9$."),
   (r"$\frac{27}{8}$", r"Takes $\alpha^3 + \beta^3 = (\alpha+\beta)^3$."),
   (r"$\frac{75}{8}$", r"Uses $-3\alpha\beta$ without the factor $(\alpha+\beta)$: $\frac{27}{8} + 6$.")],
  r"$\alpha+\beta = \frac{3}{2}$, $\alpha\beta = -2$. $\alpha^3+\beta^3 = \frac{27}{8} - 3(-2)\left(\frac{3}{2}\right) = \frac{27}{8} + 9 = \frac{99}{8}$.",
  r"Sign of $\alpha\beta$ when the constant term is negative.",
  "U02-sum-cubes", r"Identity $s^3 - 3ps$ with fractional values and a sign trap.",
  check=lambda: sym(2*x**2 - 3*x - 4, lambda a, b: a**3 + b**3),
  values=[Rational(99, 8), Rational(-45, 8), Rational(27, 8), Rational(75, 8)])


def _c19():
    p = Symbol('p', positive=True)
    a_, b_ = rts(x**2 - p*x + 8)
    return solve(expand((a_ - b_)**2) - 4, p)[0]**2


q("U02-D-019", "Roots and coefficients", "Roots differing by a constant", "Medium", "Inverse/parameter MCQ",
  r"If the roots of $x^2 - px + 8 = 0$ differ by $2$, then $p^2$ equals",
  r"$36$",
  [(r"$34$", r"Sets $(\alpha-\beta)^2 = 2$ instead of $4$: $p^2 - 32 = 2$."),
   (r"$20$", r"Uses $(\alpha-\beta)^2 = (\alpha+\beta)^2 - 2\alpha\beta$: $p^2 - 16 = 4$."),
   (r"$12$", r"Uses $(\alpha-\beta)^2 = (\alpha+\beta)^2 - \alpha\beta$: $p^2 - 8 = 4$.")],
  r"$(\alpha-\beta)^2 = (\alpha+\beta)^2 - 4\alpha\beta = p^2 - 32 = 4$, so $p^2 = 36$ (for instance roots $2$ and $4$ with $p = 6$).",
  r"Not squaring the given difference; wrong identity for $(\alpha-\beta)^2$.",
  "U02-roots-differ-param", r"Identity for $(\alpha-\beta)^2$ and squaring the data.",
  check=_c19, values=[36, 34, 20, 12])


def _c20():
    t, p = symbols('t p')
    sols = solve([3*(t*4*t) - 12, 3*(t + 4*t) + p], [t, p], dict=True)
    return [s_[p] for s_ in sols if s_[p] < 0][0]


q("U02-D-020", "Roots and coefficients", "Roots in a given ratio", "Medium", "Inverse/parameter MCQ",
  r"If the roots of $3x^2 + px + 12 = 0$ are in the ratio $1 : 4$ and $p < 0$, then $p$ equals",
  r"$-15$",
  [(r"$-\frac{5}{3}$", r"Writes the sum of roots as $-3p$ (multiplying by $a$ instead of dividing): $5 = -3p$."),
   (r"$-5$", r"Forgets $a = 3$ in the sum: $5t = -p$ with $t = 1$."),
   (r"$-\frac{15}{2}$", r"Uses $(mn)^2b^2 = (m+n)^2ac$: $16p^2 = 25 \cdot 36$.")],
  r"Let the roots be $t$ and $4t$. Product: $4t^2 = 4$, so $t = \pm 1$. Sum: $5t = -\frac{p}{3}$, so $p = -15t$. With $p < 0$, $t = 1$ and $p = -15$.",
  r"Ignoring the leading coefficient in $-\frac{b}{a}$.",
  "U02-roots-ratio", "Parametrise roots, two relations, sign condition.",
  check=_c20, values=[-15, Rational(-5, 3), -5, Rational(-15, 2)])


def _c21():
    a_, k = symbols('a k')
    out = []
    for s_ in solve([a_ + a_**2 - 20, k - a_**3], [a_, k], dict=True):
        if s_[k] > 0:
            out.append(s_[k])
    return out[0]


q("U02-D-021", "Roots and coefficients", "One root the square of the other", "Medium", "Inverse/parameter MCQ",
  r"If one root of $x^2 - 20x + k = 0$ is the square of the other and $k > 0$, then $k$ equals",
  r"$64$",
  [(r"$16$", r"Takes the product of roots as $\alpha^2$ instead of $\alpha \cdot \alpha^2$, with $\alpha = 4$."),
   (r"$125$", r"Uses $\alpha = -5$ and writes $(-5)^3 = 125$."),
   (r"$256$", r"Takes $k = (\alpha^2)^2 = \alpha^4$ with $\alpha = 4$.")],
  r"Let the roots be $\alpha, \alpha^2$. Then $\alpha + \alpha^2 = 20$, so $\alpha = 4$ or $\alpha = -5$, and $k = \alpha^3 = 64$ or $-125$. Since $k > 0$, $k = 64$.",
  r"Using $\alpha^2$ instead of $\alpha^3$ for the product of the roots.",
  "U02-root-square", r"Set up roots, solve a quadratic in $\alpha$, apply a sign condition.",
  check=_c21, values=[64, 16, 125, 256],
  numerical=dict(question=r"If one root of $x^2 - 20x + k = 0$ is the square of the other and $k > 0$, then the value of $k$ is", answer=64))


def _c22():
    k = Symbol('k')
    vals = []
    for r_ in rts(x**2 - 5*x + 6):
        kv = solve((x**2 + k*x - 12).subs(x, r_), k)[0]
        common = set(rts(x**2 - 5*x + 6)) & set(rts(x**2 + kv*x - 12))
        if len(common) == 1:
            vals.append(kv)
    return sum(vals)


q("U02-D-022", "Common roots", "Common root with a known equation", "Medium", "Inverse/parameter MCQ",
  r"The equations $x^2 - 5x + 6 = 0$ and $x^2 + kx - 12 = 0$ have exactly one common root. The sum of all possible values of $k$ is",
  r"$5$",
  [(r"$4$", r"Considers only the common root $2$."),
   (r"$1$", r"Considers only the common root $3$."),
   (r"$-5$", r"Transposes with the wrong sign in both cases, getting $k = -4$ and $k = -1$.")],
  r"The roots of the first equation are $2$ and $3$. If $2$ is common, $4 + 2k - 12 = 0$, $k = 4$ (other root $-6$). If $3$ is common, $9 + 3k - 12 = 0$, $k = 1$ (other root $-4$). Sum $= 5$.",
  "Considering only one of the possible common roots.",
  "U02-common-root-known", "Casework over two candidate common roots.",
  check=_c22, values=[5, 4, 1, -5],
  numerical=dict(question=r"The equations $x^2 - 5x + 6 = 0$ and $x^2 + kx - 12 = 0$ have exactly one common root. The sum of all possible values of $k$ is", answer=5))


def _c23():
    a, b = symbols('a b')
    al = solve(cancel(((x**2 + a*x + b) - (x**2 + b*x + a)) / (a - b)), x)[0]
    return solve((x**2 + a*x + b).subs(x, al), a)[0] + b


q("U02-D-023", "Common roots", "Common root of symmetric pair", "Medium", "Inverse/parameter MCQ",
  r"If the equations $x^2 + ax + b = 0$ and $x^2 + bx + a = 0$, where $a \neq b$, have a common root, then $a + b$ equals",
  r"$-1$",
  [(r"$1$", r"Reaches $1 + a + b = 0$ but transposes it as $a + b = 1$."),
   (r"$-\frac{1}{2}$", r"Adds the equations to get $2x^2 + (a+b)x + (a+b) = 0$, then at $x = 1$ writes $1 + 2(a+b) = 0$, forgetting to double $x^2$."),
   (r"$-2$", r"Adds the equations and at $x = 1$ writes $2 + (a+b) = 0$, counting the $(a+b)$ terms once.")],
  r"Subtracting, $(a - b)x + (b - a) = 0$, and since $a \ne b$, $x = 1$. Substituting in the first equation, $1 + a + b = 0$, so $a + b = -1$.",
  "Not using subtraction to locate the common root.",
  "U02-common-root-symmetric", r"Elimination then substitution; uses $a \neq b$.",
  check=_c23, values=[-1, 1, Rational(-1, 2), -2])


def _c24():
    a, b, c = symbols('a b c', real=True)
    r_ = rts(x**2 + 3*x + 5)[0]
    e = expand(a*r_**2 + b*r_ + c)
    sol = solve([re(e), im(e), a + b + c - 18], [a, b, c], dict=True)[0]
    return sol[b]


q("U02-D-024", "Common roots", "Both roots common", "Medium", "Inverse/parameter MCQ",
  r"If the equations $x^2 + 3x + 5 = 0$ and $ax^2 + bx + c = 0$, where $a, b, c \in \mathbb{R}$, have a common root and $a + b + c = 18$, then $b$ equals",
  r"$6$",
  [(r"$2$", r"Gives the scaling factor $\lambda = a = 2$ instead of $b = 3\lambda$."),
   (r"$10$", r"Gives $c = 5\lambda$ instead of $b$."),
   (r"$3$", r"Takes $b$ equal to the coefficient $3$ without scaling by $\lambda$.")],
  r"The roots of $x^2 + 3x + 5 = 0$ are non-real (discriminant $9 - 20 < 0$). Since $ax^2 + bx + c = 0$ has real coefficients, the conjugate of the common root is also its root, so both roots are common and $\frac{a}{1} = \frac{b}{3} = \frac{c}{5} = \lambda$. Then $9\lambda = 18$, $\lambda = 2$, and $b = 6$.",
  "Not realising that one non-real common root forces both roots to be common.",
  "U02-common-both", "Conjugate-root idea plus proportional coefficients.",
  check=_c24, values=[6, 2, 10, 3],
  numerical=dict(question=r"If the equations $x^2 + 3x + 5 = 0$ and $ax^2 + bx + c = 0$, where $a, b, c \in \mathbb{R}$, have a common root and $a + b + c = 18$, then the value of $b$ is", answer=6))

_p25 = x**2 - 5*x + 3
q("U02-D-025", "Recurrence for power sums", "Ratio of power sums", "Medium", "Multi-step computation MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 - 5x + 3 = 0$ and $S_n = \alpha^n + \beta^n$. Then $\frac{S_{12} + 3S_{10}}{S_{11}}$ equals",
  r"$5$",
  [(r"$-5$", r"Writes $\alpha^2 = -5\alpha - 3$, so $S_{12} = -5S_{11} - 3S_{10}$."),
   (r"$3$", r"Uses $\alpha\beta = 3$ in place of $\alpha + \beta$ as the multiplier of $S_{11}$."),
   (r"$-3$", r"Uses $\alpha\beta$ in place of $\alpha + \beta$ and also writes the multiplier as $-\alpha\beta$.")],
  r"Since $\alpha^2 = 5\alpha - 3$, multiplying by $\alpha^{10}$ gives $\alpha^{12} = 5\alpha^{11} - 3\alpha^{10}$; similarly for $\beta$. Adding, $S_{12} = 5S_{11} - 3S_{10}$, so $\frac{S_{12} + 3S_{10}}{S_{11}} = 5$.",
  r"Sign errors or swapping $\alpha+\beta$ and $\alpha\beta$ in $S_n = (\alpha+\beta)S_{n-1} - \alpha\beta S_{n-2}$.",
  "U02-recurrence-ratio", "Derive the recurrence and recognise the combination.",
  check=lambda: simplify((S(_p25, 12) + 3*S(_p25, 10)) / S(_p25, 11)), values=[5, -5, 3, -3],
  numerical=dict(question=r"Let $\alpha$ and $\beta$ be the roots of $x^2 - 5x + 3 = 0$ and $S_n = \alpha^n + \beta^n$. Then the value of $\frac{S_{12} + 3S_{10}}{S_{11}}$ is", answer=5))

q("U02-D-026", "Quadratics with complex coefficients", "Sum of squares of roots", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - (2 + i)x + (1 + 3i) = 0$, then $\alpha^2 + \beta^2$ equals",
  r"$1 - 2i$",
  [(r"$5 + 10i$", r"Adds $2\alpha\beta$: $(3 + 4i) + (2 + 6i)$."),
   (r"$3 + 4i$", r"Uses $(\alpha+\beta)^2 = 3 + 4i$ and drops $-2\alpha\beta$."),
   (r"$3 - 2i$", r"Expands $(2+i)^2$ as $5 + 4i$ (taking $i^2 = 1$), then subtracts $2 + 6i$.")],
  r"$\alpha+\beta = 2 + i$, $\alpha\beta = 1 + 3i$. $(2+i)^2 = 3 + 4i$, so $\alpha^2+\beta^2 = 3 + 4i - 2 - 6i = 1 - 2i$.",
  r"Mishandling $i^2$ while squaring a complex sum.",
  "U02-complex-coeff-vieta", "Vieta with complex numbers plus complex squaring.",
  check=lambda: sym(x**2 - (2 + I)*x + (1 + 3*I), lambda a, b: a**2 + b**2),
  values=[1 - 2*I, 5 + 10*I, 3 + 4*I, 3 - 2*I])

q("U02-D-027", "Formation of quadratic equations", "Roots squared", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $2x^2 - 5x + 1 = 0$, then the equation whose roots are $\alpha^2$ and $\beta^2$ is",
  r"$4x^2 - 21x + 1 = 0$",
  [(r"$4x^2 - 25x + 1 = 0$", r"Takes $\alpha^2 + \beta^2 = (\alpha+\beta)^2 = \frac{25}{4}$."),
   (r"$4x^2 - 21x + 2 = 0$", r"Takes the new product as $\alpha\beta = \frac{1}{2}$ instead of $(\alpha\beta)^2$."),
   (r"$4x^2 + 21x + 1 = 0$", r"Uses $+(\text{sum})$ for the $x$ coefficient.")],
  r"$\alpha+\beta = \frac{5}{2}$, $\alpha\beta = \frac{1}{2}$. New sum $= \frac{25}{4} - 1 = \frac{21}{4}$; new product $= \frac{1}{4}$. Equation: $x^2 - \frac{21}{4}x + \frac{1}{4} = 0$, i.e. $4x^2 - 21x + 1 = 0$.",
  r"Forgetting to square $\alpha\beta$.",
  "U02-transform-square", "Two symmetric functions then clearing fractions.",
  check=lambda: formed(2*x**2 - 5*x + 1, lambda a, b: a**2),
  values=[mon(4*x**2 - 21*x + 1), mon(4*x**2 - 25*x + 1), mon(4*x**2 - 21*x + 2), mon(4*x**2 + 21*x + 1)])

q("U02-D-028", "Formation of quadratic equations", "Roots alpha/beta and beta/alpha", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 + 5x + 3 = 0$, then the equation whose roots are $\frac{\alpha}{\beta}$ and $\frac{\beta}{\alpha}$ is",
  r"$3x^2 - 19x + 3 = 0$",
  [(r"$3x^2 + 19x + 3 = 0$", r"Takes the new sum as $-\frac{19}{3}$."),
   (r"$3x^2 - 25x + 3 = 0$", r"Uses $(\alpha+\beta)^2 = 25$ in place of $\alpha^2 + \beta^2$."),
   (r"$3x^2 - 19x + 9 = 0$", r"Takes the new product as $\alpha\beta = 3$ instead of $1$.")],
  r"New sum $= \frac{\alpha^2+\beta^2}{\alpha\beta} = \frac{25 - 6}{3} = \frac{19}{3}$, new product $= 1$. Equation: $x^2 - \frac{19}{3}x + 1 = 0$, i.e. $3x^2 - 19x + 3 = 0$.",
  r"Missing that $\frac{\alpha}{\beta} \cdot \frac{\beta}{\alpha} = 1$.",
  "U02-transform-ratio-roots", "Symmetric function plus a structural observation.",
  check=lambda: formed(x**2 + 5*x + 3, lambda a, b: a/b),
  values=[mon(3*x**2 - 19*x + 3), mon(3*x**2 + 19*x + 3), mon(3*x**2 - 25*x + 3), mon(3*x**2 - 19*x + 9)])

q("U02-D-029", "Formation of quadratic equations", "Linear transformation of roots", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $3x^2 - 4x - 2 = 0$, then the equation whose roots are $2\alpha + 1$ and $2\beta + 1$ is",
  r"$3x^2 - 14x + 3 = 0$",
  [(r"$12x^2 + 4x - 3 = 0$", r"Substitutes $2x + 1$ for $x$ instead of $\frac{x-1}{2}$."),
   (r"$3x^2 - 14x - 5 = 0$", r"Takes the new product as $4\alpha\beta + 1 = -\frac{5}{3}$, dropping $2(\alpha+\beta)$."),
   (r"$3x^2 - 11x + 3 = 0$", r"Takes the new sum as $2(\alpha+\beta) + 1 = \frac{11}{3}$.")],
  r"If $y = 2x + 1$ then $x = \frac{y-1}{2}$. Substituting: $\frac{3(y-1)^2}{4} - 2(y-1) - 2 = 0$, i.e. $3(y-1)^2 - 8(y-1) - 8 = 0$, giving $3y^2 - 14y + 3 = 0$. Check: new sum $= 2 \cdot \frac{4}{3} + 2 = \frac{14}{3}$, new product $= 4\left(-\frac{2}{3}\right) + 2 \cdot \frac{4}{3} + 1 = 1$.",
  "Substituting the forward map instead of its inverse.",
  "U02-transform-linear", "Inverse substitution and algebraic expansion.",
  check=lambda: formed(3*x**2 - 4*x - 2, lambda a, b: 2*a + 1),
  values=[mon(3*x**2 - 14*x + 3), mon(12*x**2 + 4*x - 3), mon(3*x**2 - 14*x - 5), mon(3*x**2 - 11*x + 3)])

q("U02-D-030", "Roots and coefficients", "Sum of reciprocals of squares", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $3x^2 - 2x - 4 = 0$, then $\frac{1}{\alpha^2} + \frac{1}{\beta^2}$ equals",
  r"$\frac{7}{4}$",
  [(r"$-\frac{7}{3}$", r"Divides $\alpha^2 + \beta^2 = \frac{28}{9}$ by $\alpha\beta = -\frac{4}{3}$ instead of $(\alpha\beta)^2$."),
   (r"$\frac{1}{4}$", r"Takes the expression as $\left(\frac{1}{\alpha} + \frac{1}{\beta}\right)^2 = \left(-\frac{1}{2}\right)^2$."),
   (r"$-\frac{5}{4}$", r"Uses $\alpha^2 + \beta^2 = (\alpha+\beta)^2 + 2\alpha\beta = -\frac{20}{9}$, then divides by $\frac{16}{9}$.")],
  r"$\alpha+\beta = \frac{2}{3}$, $\alpha\beta = -\frac{4}{3}$. $\alpha^2+\beta^2 = \frac{4}{9} + \frac{8}{3} = \frac{28}{9}$. Hence $\frac{\alpha^2+\beta^2}{(\alpha\beta)^2} = \frac{28/9}{16/9} = \frac{7}{4}$.",
  r"Using $\alpha\beta$ instead of $(\alpha\beta)^2$ in the denominator.",
  "U02-recip-squares", "Two identities and fraction handling with a negative product.",
  check=lambda: sym(3*x**2 - 2*x - 4, lambda a, b: 1/a**2 + 1/b**2),
  values=[Rational(7, 4), Rational(-7, 3), Rational(1, 4), Rational(-5, 4)])


def _c31():
    k = Symbol('k', real=True)
    e = sym(x**2 - (k - 2)*x - (k + 1), lambda a, b: a**2 + b**2)
    return solve(diff(e, k), k)[0]


q("U02-D-031", "Roots and coefficients", "Parameter minimising a symmetric function", "Medium", "Inverse/parameter MCQ",
  r"For real $k$, let $\alpha$ and $\beta$ be the roots of $x^2 - (k - 2)x - (k + 1) = 0$. The value of $k$ for which $\alpha^2 + \beta^2$ is least is",
  r"$1$",
  [(r"$2$", r"Minimises $(k - 2)^2$ alone, ignoring the $2(k + 1)$ term."),
   (r"$-1$", r"Takes the vertex of $k^2 - 2k + 6$ at $k = \frac{-2}{2}$ (sign slip in $-\frac{b}{2a}$)."),
   (r"$5$", r"Reports the least value of $\alpha^2 + \beta^2$ instead of $k$.")],
  r"$\alpha^2+\beta^2 = (k-2)^2 + 2(k+1) = k^2 - 2k + 6 = (k-1)^2 + 5$, which is least at $k = 1$. The roots are real for every $k$ since $(k-2)^2 + 4(k+1) = k^2 + 8 > 0$.",
  "Reporting the minimum value instead of the minimising parameter.",
  "U02-param-minimize", "Symmetric function then completing the square.",
  check=_c31, values=[1, 2, -1, 5])


def _c32():
    k = Symbol('k', positive=True)
    a_, b_ = rts(x**2 - k*x + 16)
    return solve(expand(a_**2 + b_**2) - 68, k)[0]


q("U02-D-032", "Roots and coefficients", "Parameter from sum of squares", "Medium", "Inverse/parameter MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - kx + 16 = 0$ with $\alpha^2 + \beta^2 = 68$ and $k > 0$, then $k$ equals",
  r"$10$",
  [(r"$6$", r"Writes $k^2 + 32 = 68$ (sign slip in $(\alpha+\beta)^2 - 2\alpha\beta$)."),
   (r"$2\sqrt{17}$", r"Takes $\alpha^2 + \beta^2 = k^2$, dropping $-2\alpha\beta$."),
   (r"$2\sqrt{21}$", r"Subtracts $\alpha\beta$ once: $k^2 - 16 = 68$.")],
  r"$\alpha^2+\beta^2 = k^2 - 32 = 68$, so $k^2 = 100$ and $k = 10$ since $k > 0$ (roots $2$ and $8$).",
  r"Wrong sign or missing factor $2$ in $(\alpha+\beta)^2 - 2\alpha\beta$.",
  "U02-param-sum-squares", "Identity, solve, sign condition.",
  check=_c32, values=[10, 6, 2*sqrt(17), 2*sqrt(21)],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - kx + 16 = 0$ with $\alpha^2 + \beta^2 = 68$ and $k > 0$, then the value of $k$ is", answer=10))


def _c33():
    a, t = symbols('a t', nonzero=True)
    b = -a*(3*t + 4*t)
    c = a*(3*t)*(4*t)
    return simplify(b**2 / (a*c))


q("U02-D-033", "Roots and coefficients", "Condition for roots in a ratio", "Medium", "Conceptual/application MCQ",
  r"If the roots of $ax^2 + bx + c = 0$ ($a \neq 0$, $c \neq 0$) are in the ratio $3 : 4$, then",
  r"$12b^2 = 49ac$",
  [(r"$49b^2 = 12ac$", r"Interchanges the two sides of $mnb^2 = (m+n)^2ac$."),
   (r"$12b^2 = 7ac$", r"Uses $(m + n)$ instead of $(m + n)^2$."),
   (r"$144b^2 = 49ac$", r"Uses $(mn)^2$ instead of $mn$.")],
  r"Let the roots be $3t$ and $4t$. Then $7t = -\frac{b}{a}$ and $12t^2 = \frac{c}{a}$. Eliminating $t$: $\frac{b^2}{49a^2} = \frac{c}{12a}$, so $12b^2 = 49ac$.",
  r"Misremembering the ratio condition $mnb^2 = (m+n)^2ac$.",
  "U02-roots-ratio", r"Parametrise the roots and eliminate $t$.",
  check=_c33, values=[Rational(49, 12), Rational(12, 49), Rational(7, 12), Rational(49, 144)], cognitive="Understanding")


def _c34():
    k = Symbol('k')
    a_, b_ = rts(x**2 - 7*x + k)
    return solve(expand((a_ - 1)*(b_ - 1)) - 2, k)[0]


q("U02-D-034", "Roots and coefficients", "Parameter from shifted product", "Medium", "Inverse/parameter MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 7x + k = 0$ and $(\alpha - 1)(\beta - 1) = 2$, then $k$ equals",
  r"$8$",
  [(r"$-6$", r"Expands as $\alpha\beta + (\alpha+\beta) + 1$: $k + 8 = 2$."),
   (r"$9$", r"Drops the constant $1$: $k - 7 = 2$."),
   (r"$10$", r"Uses $-1$ as the constant: $k - 7 - 1 = 2$.")],
  r"$(\alpha-1)(\beta-1) = \alpha\beta - (\alpha+\beta) + 1 = k - 7 + 1 = 2$, so $k = 8$.",
  r"Sign errors when expanding $(\alpha - 1)(\beta - 1)$.",
  "U02-product-shifted", "Expansion plus Vieta, solving for the parameter.",
  check=_c34, values=[8, -6, 9, 10],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 7x + k = 0$ and $(\alpha - 1)(\beta - 1) = 2$, then the value of $k$ is", answer=8))


def _c35():
    p = 2*x**2 - 3*x + 5
    s1 = equal_poly(formed(p, lambda a, b: 1/a), 5*x**2 - 3*x + 2)
    s2 = equal_poly(formed(p, lambda a, b: -a), 2*x**2 - 3*x - 5)
    return (s1, s2)


q("U02-D-035", "Formation of quadratic equations", "Reciprocal and negated roots", "Medium", "Statement-based MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $2x^2 - 3x + 5 = 0$. Statement I: The equation whose roots are $\frac{1}{\alpha}$ and $\frac{1}{\beta}$ is $5x^2 - 3x + 2 = 0$. Statement II: The equation whose roots are $-\alpha$ and $-\beta$ is $2x^2 - 3x - 5 = 0$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Believes negating the roots changes the sign of the constant term."),
   (ST_FF, r"Also rejects Statement I, thinking $x \to \frac{1}{x}$ does not simply reverse the coefficients."),
   (ST_FT, r"Swaps the two transformations: thinks $x \to \frac{1}{x}$ flips a sign and $x \to -x$ flips the constant.")],
  r"Replacing $x$ by $\frac{1}{x}$ reverses the coefficients: $5x^2 - 3x + 2 = 0$, so Statement I is true. Replacing $x$ by $-x$ changes the sign of the $x$ term only: $2x^2 + 3x + 5 = 0$; the new sum is $-\frac{3}{2}$ and product $\frac{5}{2}$, so Statement II is false.",
  r"Thinking that the roots $-\alpha, -\beta$ change the sign of the constant term.",
  "U02-transform-statement", "Two transformations compared.",
  check=_c35, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding")

_p36 = x**2 - x - 1
q("U02-D-036", "Recurrence for power sums", "Evaluating a power sum", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - x - 1 = 0$, then $\alpha^5 + \beta^5$ equals",
  r"$11$",
  [(r"$7$", r"Stops one step early and gives $S_4 = \alpha^4 + \beta^4$."),
   (r"$18$", r"Goes one step too far and gives $S_6$."),
   (r"$5$", r"Starts with $S_2 = 1$ (forgetting $-2\alpha\beta$), so $S_3 = 2$, $S_4 = 3$, $S_5 = 5$.")],
  r"From $\alpha^2 = \alpha + 1$, $S_n = S_{n-1} + S_{n-2}$ with $S_1 = 1$, $S_2 = 1 + 2 = 3$. Then $S_3 = 4$, $S_4 = 7$, $S_5 = 11$.",
  r"Wrong starting value $S_2$ for the recurrence.",
  "U02-recurrence-value", "Derive recurrence and iterate four times.",
  check=lambda: S(_p36, 5), values=[11, 7, 18, 5],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - x - 1 = 0$, then the value of $\alpha^5 + \beta^5$ is", answer=11))


def _c37():
    p = x**2 - 2*x - 1
    return (simplify(S(p, 6) - (2*S(p, 5) - S(p, 4))) == 0, S(p, 4) == 34)


q("U02-D-037", "Recurrence for power sums", "Recurrence and values", "Medium", "Statement-based MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 - 2x - 1 = 0$ and $S_n = \alpha^n + \beta^n$. Statement I: $S_6 = 2S_5 - S_4$. Statement II: $S_4 = 34$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts the slipped recurrence in Statement I, but finds $S_4 = S_2^2 - 2(\alpha\beta)^2 = 36 - 2 = 34$ directly."),
   (ST_FF, r"Rejects Statement I correctly but takes $S_4 = S_2^2 = 36$."),
   (ST_TF, r"Uses the slipped recurrence $S_n = 2S_{n-1} - S_{n-2}$ throughout: $S_3 = 10$, $S_4 = 14$.")],
  r"$\alpha^2 = 2\alpha + 1$ gives $S_n = 2S_{n-1} + S_{n-2}$, so $S_6 = 2S_5 + S_4$ and Statement I is false. With $S_1 = 2$, $S_2 = 4 + 2 = 6$, $S_3 = 14$, $S_4 = 2(14) + 6 = 34$, so Statement II is true.",
  r"Sign error in moving the constant term: writing $\alpha^2 = 2\alpha - 1$.",
  "U02-recurrence-statement", "Recurrence derivation plus iteration.",
  check=_c37, values=[(False, True), (True, True), (False, False), (True, False)])


def _c38():
    k, m = symbols('k m')
    d = expand((2*x**2 + k*x + 6)/2 - (3*x**2 + 9*x + m)/3)
    sol = solve(Poly(d, x).all_coeffs(), [k, m], dict=True)[0]
    return sol[k] + sol[m]


q("U02-D-038", "Common roots", "Both roots common", "Medium", "Inverse/parameter MCQ",
  r"If the equations $2x^2 + kx + 6 = 0$ and $3x^2 + 9x + m = 0$ have both roots in common, then $k + m$ equals",
  r"$15$",
  [(r"$10$", r"Inverts the ratio for $m$: $m = \frac{2}{3} \cdot 6 = 4$, so $6 + 4$."),
   (r"$\frac{45}{2}$", r"Inverts the ratio for $k$: $k = \frac{3}{2} \cdot 9 = \frac{27}{2}$, so $\frac{27}{2} + 9$."),
   (r"$\frac{35}{2}$", r"Inverts the ratio for both: $\frac{27}{2} + 4$.")],
  r"Both roots common means the coefficients are proportional: $\frac{2}{3} = \frac{k}{9} = \frac{6}{m}$. Hence $k = 6$, $m = 9$ and $k + m = 15$.",
  "Inverting the proportionality ratio.",
  "U02-common-both", "Condition for identical root sets.",
  check=_c38, values=[15, 10, Rational(45, 2), Rational(35, 2)])

q("U02-D-039", "Roots and coefficients", "Sum of square roots of roots", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 4x + 1 = 0$, then $\sqrt{\alpha} + \sqrt{\beta}$ equals",
  r"$\sqrt{6}$",
  [(r"$2$", r"Squares and forgets the cross term: $\sqrt{\alpha + \beta} = \sqrt{4}$."),
   (r"$\sqrt{5}$", r"Uses $\sqrt{\alpha\beta}$ instead of $2\sqrt{\alpha\beta}$ as the cross term: $\sqrt{4 + 1}$."),
   (r"$\sqrt{2}$", r"Computes $|\sqrt{\alpha} - \sqrt{\beta}| = \sqrt{4 - 2}$ instead.")],
  r"Both roots are positive ($2 \pm \sqrt{3}$). $(\sqrt{\alpha}+\sqrt{\beta})^2 = \alpha + \beta + 2\sqrt{\alpha\beta} = 4 + 2 = 6$, so $\sqrt{\alpha}+\sqrt{\beta} = \sqrt{6}$.",
  r"Missing the cross term $2\sqrt{\alpha\beta}$ when squaring.",
  "U02-sqrt-roots", "Squaring trick with a positivity check.",
  check=lambda: sym(x**2 - 4*x + 1, lambda a, b: sqrt(a) + sqrt(b)),
  values=[sqrt(6), 2, sqrt(5), sqrt(2)])

q("U02-D-040", "Roots and coefficients", "Cubes over squared product", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x - 1 = 0$, then $\frac{\alpha}{\beta^2} + \frac{\beta}{\alpha^2}$ equals",
  r"$36$",
  [(r"$18$", r"Takes $\alpha\beta = +1$: $\alpha^3 + \beta^3 = 27 - 9$."),
   (r"$-36$", r"Divides $\alpha^3 + \beta^3 = 36$ by $\alpha\beta = -1$ instead of $(\alpha\beta)^2$."),
   (r"$27$", r"Takes $\alpha^3 + \beta^3 = (\alpha+\beta)^3$.")],
  r"$\frac{\alpha}{\beta^2}+\frac{\beta}{\alpha^2} = \frac{\alpha^3+\beta^3}{(\alpha\beta)^2}$. With $\alpha+\beta = 3$, $\alpha\beta = -1$: $\alpha^3+\beta^3 = 27 + 9 = 36$ and $(\alpha\beta)^2 = 1$, giving $36$.",
  "Wrong denominator after combining fractions.",
  "U02-cubes-over-square-product", "Combine fractions, then a cubic identity.",
  check=lambda: sym(x**2 - 3*x - 1, lambda a, b: a/b**2 + b/a**2), values=[36, 18, -36, 27],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x - 1 = 0$, then the value of $\frac{\alpha}{\beta^2} + \frac{\beta}{\alpha^2}$ is", answer=36))

# ============================ DIFFICULT ============================

_p41 = 2*x**2 - 6*x - 1
q("U02-D-041", "Recurrence for power sums", "Recurrence with leading coefficient", "Difficult", "Multi-step computation MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $2x^2 - 6x - 1 = 0$ and $S_n = \alpha^n + \beta^n$. Then $\frac{2S_{10} - S_8}{S_9}$ equals",
  r"$6$",
  [(r"$3$", r"Answers $\alpha + \beta = 3$ as for a monic equation, not noticing the numerator already carries the factor $2$."),
   (r"$-6$", r"Writes $2\alpha^2 = -6\alpha + 1$ (sign slip), giving $2S_{10} - S_8 = -6S_9$."),
   (r"$12$", r"Multiplies the correct ratio by the leading coefficient $2$ once more.")],
  r"From $2\alpha^2 = 6\alpha + 1$, multiplying by $\alpha^8$: $2\alpha^{10} = 6\alpha^9 + \alpha^8$; similarly for $\beta$. Adding, $2S_{10} - S_8 = 6S_9$, so the ratio is $6$.",
  "Ignoring the leading coefficient when forming the recurrence.",
  "U02-recurrence-ratio", "Recurrence with a non-monic leading coefficient; trap.",
  check=lambda: simplify((2*S(_p41, 10) - S(_p41, 8)) / S(_p41, 9)), values=[6, 3, -6, 12],
  numerical=dict(question=r"Let $\alpha$ and $\beta$ be the roots of $2x^2 - 6x - 1 = 0$ and $S_n = \alpha^n + \beta^n$. Then the value of $\frac{2S_{10} - S_8}{S_9}$ is", answer=6))


def _c42():
    p = Symbol('p')
    return sum(solve(S(x**2 - 3*x + p, 4) - 47, p))


q("U02-D-042", "Roots and coefficients", "Parameter from fourth powers", "Difficult", "Inverse/parameter MCQ",
  r"Let $\alpha$ and $\beta$ be the roots (real or non-real) of $x^2 - 3x + p = 0$, where $p$ is a real number. If $\alpha^4 + \beta^4 = 47$, then the sum of all possible values of $p$ is",
  r"$18$",
  [(r"$1$", r"Rejects $p = 17$ because the roots are then non-real, though the stem allows non-real roots."),
   (r"$\frac{19}{2}$", r"Drops the square on $\alpha\beta$: $(9 - 2p)^2 - 2p = 47$ gives $2p^2 - 19p + 17 = 0$, sum $\frac{19}{2}$."),
   (r"$36$", r"From $2p^2 - 36p + 34 = 0$ takes the sum of roots as $36$, not dividing by $2$.")],
  r"$\alpha^2+\beta^2 = 9 - 2p$, so $\alpha^4+\beta^4 = (9-2p)^2 - 2p^2 = 2p^2 - 36p + 81 = 47$, i.e. $p^2 - 18p + 17 = 0$, giving $p = 1$ or $p = 17$. Both are valid (for $p = 17$ the roots are non-real but the identity still holds), so the sum is $18$.",
  r"Dropping a valid value by assuming the roots must be real, or forgetting $-2(\alpha\beta)^2$.",
  "U02-param-fourth-power", r"Two-level identity, a quadratic in $p$, and judging which values are admissible.",
  check=_c42, values=[18, 1, Rational(19, 2), 36], cognitive="Analysis",
  numerical=dict(question=r"Let $\alpha$ and $\beta$ be the roots (real or non-real) of $x^2 - 3x + p = 0$, where $p$ is a real number. If $\alpha^4 + \beta^4 = 47$, then the sum of all possible values of $p$ is", answer=18))


def _c43():
    r_, a, b = symbols('r a b')
    sols = solve([r_**2 + a*r_ + 6, r_**2 + b*r_ + 8, r_**2 + (a + b)*r_ + 18], [r_, a, b], dict=True)
    return [s_[b] for s_ in sols if s_[r_] > 0][0]


q("U02-D-043", "Common roots", "Common root of three equations", "Difficult", "Inverse/parameter MCQ",
  r"The equations $x^2 + ax + 6 = 0$, $x^2 + bx + 8 = 0$ and $x^2 + (a + b)x + 18 = 0$ have a common positive root. Then $b$ equals",
  r"$-6$",
  [(r"$6$", r"Uses the negative root $r = -2$: $4 - 2b + 8 = 0$."),
   (r"$-5$", r"Reports $a$ (from $4 + 2a + 6 = 0$) instead of $b$."),
   (r"$-4$", r"Uses $b = -\frac{8}{r}$ with $r = 2$, dropping the $r^2$ term.")],
  r"Let $r$ be the common root. Adding the first two equations and subtracting the third: $r^2 + 6 + 8 - 18 = 0$, so $r^2 = 4$ and $r = 2$. Then $4 + 2b + 8 = 0$ gives $b = -6$ (and $a = -5$).",
  r"Not combining the equations to eliminate $a$ and $b$.",
  "U02-common-root-three", "Non-obvious elimination across three equations, then a sign condition.",
  check=_c43, values=[-6, 6, -5, -4], cognitive="Analysis")


def _c44():
    al, k = symbols('al k')
    sols = solve([al**2 - k*al - 21, al**2 - 3*k*al + 35], [al, k], dict=True)
    return [s_[k] for s_ in sols if s_[k] > 0][0]


q("U02-D-044", "Common roots", "Parameter for a common root", "Difficult", "Inverse/parameter MCQ",
  r"If the equations $x^2 - kx - 21 = 0$ and $x^2 - 3kx + 35 = 0$ have a common root and $k > 0$, then $k$ equals",
  r"$4$",
  [(r"$7$", r"Reports the common root $\alpha = 7$ instead of $k$."),
   (r"$16$", r"Reports $k^2 = 16$ instead of $k$."),
   (r"$28$", r"Reports $k\alpha = 28$, found after subtracting, instead of $k$.")],
  r"Let $\alpha$ be common. Subtracting, $2k\alpha - 56 = 0$, so $\alpha = \frac{28}{k}$. Substituting in the first: $\frac{784}{k^2} - 28 - 21 = 0$, so $k^2 = 16$ and $k = 4$ (common root $7$).",
  "Stopping at an intermediate quantity.",
  "U02-common-root-param", "Elimination, substitution and a sign condition.",
  check=_c44, values=[4, 7, 16, 28],
  numerical=dict(question=r"If the equations $x^2 - kx - 21 = 0$ and $x^2 - 3kx + 35 = 0$ have a common root and $k > 0$, then the value of $k$ is", answer=4))

q("U02-D-045", "Formation of quadratic equations", "Mixed transformation of roots", "Difficult", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 3x + 1 = 0$, then the equation whose roots are $\alpha^2 + \beta$ and $\beta^2 + \alpha$ is",
  r"$x^2 - 10x + 20 = 0$",
  [(r"$x^2 - 10x + 19 = 0$", r"Drops the $\alpha\beta$ term in the expanded product: $1 + 18$."),
   (r"$x^2 - 7x + 20 = 0$", r"Takes the new sum as $\alpha^2 + \beta^2 = 7$ only."),
   (r"$x^2 - 10x + 2 = 0$", r"Omits $\alpha^3 + \beta^3$ in the product: $1 + 1$.")],
  r"$\alpha+\beta = 3$, $\alpha\beta = 1$. New sum $= \alpha^2+\beta^2 + \alpha+\beta = 7 + 3 = 10$. New product $= \alpha^2\beta^2 + \alpha^3 + \beta^3 + \alpha\beta = 1 + 18 + 1 = 20$, using $\alpha^3+\beta^3 = 27 - 9 = 18$.",
  "Incomplete expansion of the product of the new roots.",
  "U02-transform-mixed", "Expansion into four terms needing three identities.",
  check=lambda: formed(x**2 - 3*x + 1, lambda a, b: a**2 + b),
  values=[mon(x**2 - 10*x + 20), mon(x**2 - 10*x + 19), mon(x**2 - 7*x + 20), mon(x**2 - 10*x + 2)])

q("U02-D-046", "Formation of quadratic equations", "Fractional transformation of roots", "Difficult", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 5x + 2 = 0$, then the equation whose roots are $\frac{\alpha - 1}{\alpha + 1}$ and $\frac{\beta - 1}{\beta + 1}$ is",
  r"$4x^2 - x - 1 = 0$",
  [(r"$4x^2 + x - 1 = 0$", r"Takes the new sum as $-\frac{1}{4}$."),
   (r"$x^2 + x - 4 = 0$", r"Substitutes $x = \frac{y + 1}{y - 1}$ instead of $\frac{1 + y}{1 - y}$."),
   (r"$4x^2 - x + 1 = 0$", r"Takes the new product as $+\frac{1}{4}$.")],
  r"Let $y = \frac{x-1}{x+1}$, so $x = \frac{1+y}{1-y}$. Substituting and multiplying by $(1-y)^2$: $(1+y)^2 - 5(1+y)(1-y) + 2(1-y)^2 = 0$, i.e. $8y^2 - 2y - 2 = 0$, so $4y^2 - y - 1 = 0$. Check: product $= \frac{2 - 5 + 1}{2 + 5 + 1} = -\frac{1}{4}$.",
  "Inverting the fractional map incorrectly.",
  "U02-transform-mobius", "Inverse of a fractional map, substitution and simplification.",
  check=lambda: formed(x**2 - 5*x + 2, lambda a, b: (a - 1)/(a + 1)),
  values=[mon(4*x**2 - x - 1), mon(4*x**2 + x - 1), mon(x**2 + x - 4), mon(4*x**2 - x + 1)])


def _c47():
    b, c = symbols('b c')
    a_, b_ = rts(x**2 + b*x + c)
    sol = solve([expand((a_ - 1)*(b_ - 1)) - 6, expand((a_ + 1)*(b_ + 1)) - 2], [b, c], dict=True)[0]
    return sym(x**2 + sol[b]*x + sol[c], lambda u, v: u**3 + v**3)


q("U02-D-047", "Roots and coefficients", "Two shifted-product conditions", "Difficult", "Multi-step computation MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 + bx + c = 0$. If $(\alpha - 1)(\beta - 1) = 6$ and $(\alpha + 1)(\beta + 1) = 2$, then $\alpha^3 + \beta^3$ equals",
  r"$10$",
  [(r"$-10$", r"Takes $\alpha + \beta = b = 2$ instead of $-b$: $8 - 18$."),
   (r"$16$", r"Drops the constant $1$ in both expansions, getting $c = 4$: $-8 + 24$."),
   (r"$-26$", r"Uses $\alpha^3 + \beta^3 = s^3 + 3ps$: $-8 - 18$.")],
  r"$(\alpha-1)(\beta-1) = c + b + 1 = 6$ and $(\alpha+1)(\beta+1) = c - b + 1 = 2$. So $b = 2$, $c = 3$, giving $\alpha+\beta = -2$, $\alpha\beta = 3$. Then $\alpha^3+\beta^3 = -8 - 3(3)(-2) = 10$.",
  r"Sign of $\alpha + \beta$ when the $x$ coefficient is $+b$.",
  "U02-shifted-system", "Two expansions, a linear system, then a cubic identity.",
  check=_c47, values=[10, -10, 16, -26],
  numerical=dict(question=r"Let $\alpha$ and $\beta$ be the roots of $x^2 + bx + c = 0$. If $(\alpha - 1)(\beta - 1) = 6$ and $(\alpha + 1)(\beta + 1) = 2$, then the value of $\alpha^3 + \beta^3$ is", answer=10))

_P, _Q, _R, _S = symbols('p q r s')


def _c48():
    a_, b_ = rts(x**2 + _P*x + _Q)
    g_, d_ = rts(x**2 + _R*x + _S)
    return expand(simplify(expand((a_ - g_)*(a_ - d_)*(b_ - g_)*(b_ - d_))))


q("U02-D-048", "Common roots", "Product of root differences", "Difficult", "Multi-step computation MCQ",
  r"Let $\alpha, \beta$ be the roots of $x^2 + px + q = 0$ and $\gamma, \delta$ be the roots of $x^2 + rx + s = 0$. Then $(\alpha - \gamma)(\alpha - \delta)(\beta - \gamma)(\beta - \delta)$ equals",
  r"$(q - s)^2 + (p - r)(ps - qr)$",
  [(r"$(q - s)^2 + q(p - r)^2$", r"Omits the cross term $(r-p)(s-q)(\alpha+\beta)$, keeping only $(r-p)^2\alpha\beta + (s-q)^2$."),
   (r"$(q - s)^2 + (p - r)(2pq - ps - qr)$", r"Takes $\alpha + \beta = p$ in the cross term: $(r-p)^2q + p(r-p)(s-q) + (s-q)^2$."),
   (r"$(q + s)^2 + (p - r)(2pq + ps - qr)$", r"Reduces with $\alpha^2 = -p\alpha + q$, so each factor is $(r-p)\alpha + (s+q)$: $(r-p)^2q - p(r-p)(s+q) + (s+q)^2$.")],
  r"$(\alpha-\gamma)(\alpha-\delta) = \alpha^2 + r\alpha + s = (r - p)\alpha + (s - q)$, using $\alpha^2 = -p\alpha - q$. Similarly for $\beta$. The product is $(r-p)^2\alpha\beta + (r-p)(s-q)(\alpha+\beta) + (s-q)^2 = (r-p)^2 q - p(r-p)(s-q) + (s-q)^2$, which simplifies to $(q-s)^2 + (p-r)(ps - qr)$. It vanishes exactly when the two equations have a common root.",
  r"Sign errors in reducing $\alpha^2$ via $\alpha^2 = -p\alpha - q$.",
  "U02-resultant", "Reduction by the equation, symmetric expansion and factoring.",
  check=_c48, values=[(_Q - _S)**2 + (_P - _R)*(_P*_S - _Q*_R), (_Q - _S)**2 + _Q*(_P - _R)**2,
                      (_Q - _S)**2 + (_P - _R)*(2*_P*_Q - _P*_S - _Q*_R), (_Q + _S)**2 + (_P - _R)*(2*_P*_Q + _P*_S - _Q*_R)],
  cognitive="Analysis")

q("U02-D-049", "Recurrence for power sums", "High power sum via a cube identity", "Difficult", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 2x + 4 = 0$, then $\alpha^6 + \beta^6$ equals",
  r"$128$",
  [(r"$256$", r"Squares $\alpha^3 + \beta^3 = -16$ and drops $-2\alpha^3\beta^3$."),
   (r"$384$", r"Adds $2\alpha^3\beta^3 = 128$ instead of subtracting: $256 + 128$."),
   (r"$-64$", r"Takes $\alpha^6 + \beta^6 = (\alpha^2 + \beta^2)^3 = (-4)^3$.")],
  r"Since $(x + 2)(x^2 - 2x + 4) = x^3 + 8$, each root satisfies $\alpha^3 = -8$. Hence $\alpha^6 = \beta^6 = 64$ and $\alpha^6 + \beta^6 = 128$. (Equivalently, $\alpha^3+\beta^3 = 8 - 24 = -16$ and $(-16)^2 - 2(64) = 128$.)",
  "Treating power sums as powers of lower sums.",
  "U02-cube-trick", "Non-obvious factorisation route or careful identity chain.",
  check=lambda: S(x**2 - 2*x + 4, 6), values=[128, 256, 384, -64],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 2x + 4 = 0$, then the value of $\alpha^6 + \beta^6$ is", answer=128))

_a50, _t50 = symbols('a t', nonzero=True)
_b50 = -_a50*(_t50 + _t50**2)
_cc50 = _a50*_t50**3
q("U02-D-050", "Roots and coefficients", "Condition for one root the square of the other", "Difficult", "Conceptual/application MCQ",
  r"If one root of $ax^2 + bx + c = 0$ ($a \neq 0$) is the square of the other, then",
  r"$b^3 + a^2c + ac^2 = 3abc$",
  [(r"$b^3 + a^2c + ac^2 = abc$", r"Expands $(t + t^2)^3$ as $t^3 + t^6 + t^3(t + t^2)$, dropping the factor $3$ in the cross term."),
   (r"$a^3 + b^2c + bc^2 = 3abc$", r"Interchanges the roles of $a$ and $b$ in the final relation."),
   (r"$b^3 - a^2c - ac^2 = 3abc$", r"Takes $t + t^2 = \frac{b}{a}$ (sign slip in the sum of roots) and carries it through the cubing.")],
  r"Let the roots be $t$ and $t^2$. Then $t + t^2 = -\frac{b}{a}$ and $t^3 = \frac{c}{a}$. Cubing the first: $t^3 + t^6 + 3t^3(t + t^2) = -\frac{b^3}{a^3}$, i.e. $\frac{c}{a} + \frac{c^2}{a^2} - \frac{3bc}{a^2} = -\frac{b^3}{a^3}$. Multiplying by $a^3$: $b^3 + a^2c + ac^2 = 3abc$.",
  "Errors while cubing the sum relation.",
  "U02-root-square", "Elimination by cubing a relation; several terms.",
  check=lambda: simplify(_b50**3 + _a50**2*_cc50 + _a50*_cc50**2 - 3*_a50*_b50*_cc50),
  values=[0, _b50**3 + _a50**2*_cc50 + _a50*_cc50**2 - _a50*_b50*_cc50,
          _a50**3 + _b50**2*_cc50 + _b50*_cc50**2 - 3*_a50*_b50*_cc50,
          _b50**3 - _a50**2*_cc50 - _a50*_cc50**2 - 3*_a50*_b50*_cc50],
  cognitive="Analysis")

_p51 = x**2 - 5*x + 1
q("U02-D-051", "Recurrence for power sums", "Ratio of power-sum differences", "Difficult", "Multi-step computation MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 - 5x + 1 = 0$ and $S_n = \alpha^n + \beta^n$. Then $\frac{S_{12} - S_8}{S_{11} - S_9}$ equals",
  r"$5$",
  [(r"$-5$", r"Writes the recurrence from $\alpha^2 = -5\alpha - 1$ (sign slip in the coefficients), so $S_{n+1} + S_{n-1} = -5S_n$ and the ratio comes out as $-5$."),
   (r"$23$", r"Carries over the identity $S_{n+2} + S_{n-2} = S_2 S_n$ for sums, taking the ratio as $S_2 = 25 - 2 = 23$."),
   (r"$25$", r"Treats the gap of four indices in the numerator against the gap of two in the denominator as two applications of the factor $5$, giving $5^2 = 25$.")],
  r"From $\alpha^2 = 5\alpha - 1$ (and likewise for $\beta$), $S_{n+1} = 5S_n - S_{n-1}$. Taking $n = 11$ gives $S_{12} = 5S_{11} - S_{10}$, and taking $n = 9$ gives $S_{10} = 5S_9 - S_8$, i.e. $S_8 = 5S_9 - S_{10}$. Subtracting, $S_{12} - S_8 = 5(S_{11} - S_9)$. Since $\alpha\beta = 1$ and $\alpha \ne \beta$, $S_{11} - S_9 = (\alpha - \beta)(\alpha^{10} - \beta^{10}) \ne 0$, so the ratio is $5$.",
  r"Sign slip in the recurrence $S_{n+1} = 5S_n - S_{n-1}$, or carrying over the sum identity $S_{n+2} + S_{n-2} = S_2 S_n$ to differences.",
  "U02-recurrence-difference-ratio", r"Needs the non-obvious pairing of the recurrence at $n = 11$ and $n = 9$ so that $S_{10}$ cancels, plus a check that the denominator is nonzero.",
  check=lambda: simplify((S(_p51, 12) - S(_p51, 8)) / (S(_p51, 11) - S(_p51, 9))), values=[5, -5, 23, 25], cognitive="Analysis",
  numerical=dict(question=r"Let $\alpha$ and $\beta$ be the roots of $x^2 - 5x + 1 = 0$ and $S_n = \alpha^n + \beta^n$. Then the value of $\frac{S_{12} - S_8}{S_{11} - S_9}$ is", answer=5))


def _c52():
    p, qq = symbols('p q', real=True)
    e = expand(sym(x**2 + (p + I*qq)*x + 3*I, lambda a, b: a**2 + b**2) - 8)
    sols = solve([re(e), im(e)], [p, qq], dict=True)
    vals = set(simplify(s_[p]**2 + s_[qq]**2) for s_ in sols)
    assert len(vals) == 1
    return vals.pop()


q("U02-D-052", "Quadratics with complex coefficients", "Parameter from a complex symmetric function", "Difficult", "Inverse/parameter MCQ",
  r"The roots $\alpha, \beta$ of $x^2 + (p + iq)x + 3i = 0$, where $p, q \in \mathbb{R}$, satisfy $\alpha^2 + \beta^2 = 8$. Then $p^2 + q^2$ equals",
  r"$10$",
  [(r"$14$", r"Adds $p^2 - q^2 = 8$ and $2pq = 6$ directly."),
   (r"$2\sqrt{7}$", r"Uses $\sqrt{(p^2 - q^2)^2 - (2pq)^2} = \sqrt{64 - 36}$."),
   (r"$\sqrt{73}$", r"Uses $\alpha\beta$ instead of $2\alpha\beta$, so $2pq = 3$ and $\sqrt{64 + 9}$.")],
  r"$\alpha^2+\beta^2 = (p+iq)^2 - 2(3i) = (p^2 - q^2) + i(2pq - 6) = 8$. So $p^2 - q^2 = 8$ and $pq = 3$. Then $(p^2+q^2)^2 = (p^2-q^2)^2 + 4p^2q^2 = 64 + 36 = 100$, so $p^2 + q^2 = 10$.",
  r"Not separating real and imaginary parts, or mishandling $2\alpha\beta$.",
  "U02-complex-coeff-param", "Complex Vieta, equating parts, then an algebraic identity.",
  check=_c52, values=[10, 14, 2*sqrt(7), sqrt(73)], cognitive="Analysis",
  numerical=dict(question=r"The roots $\alpha, \beta$ of $x^2 + (p + iq)x + 3i = 0$, where $p, q \in \mathbb{R}$, satisfy $\alpha^2 + \beta^2 = 8$. Then the value of $p^2 + q^2$ is", answer=10))


def _c53():
    a_, b_ = rts(x**2 - x + 2)
    u = simplify(expand(a_**3 - 2*a_**2 + 3*a_ - 1))
    v = simplify(expand(b_**3 - b_**2 + 2*b_ + 4))
    return mon(expand((x - u)*(x - v)))


q("U02-D-053", "Formation of quadratic equations", "Roots given by polynomial expressions", "Difficult", "Multi-step computation MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 - x + 2 = 0$. The quadratic equation whose roots are $\alpha^3 - 2\alpha^2 + 3\alpha - 1$ and $\beta^3 - \beta^2 + 2\beta + 4$ is",
  r"$x^2 - 5x + 4 = 0$",
  [(r"$x^2 + 5x + 4 = 0$", r"Gets the values $1$ and $4$ but writes $x^2 + (\text{sum})x + \text{product}$."),
   (r"$x^2 - 9x + 8 = 0$", r"Reduces $\beta^3$ as $-\beta + 2$ (sign slip), so the second value is $(-\beta + 2) - (\beta - 2) + 2\beta + 4 = 8$; the first stays $1$."),
   (r"$x^2 - 13x + 40 = 0$", r"Uses the slip $\alpha^3 = -\alpha + 2$ for both roots, getting $5$ and $8$.")],
  r"From $\alpha^2 = \alpha - 2$: $\alpha^3 = \alpha^2 - 2\alpha = -\alpha - 2$. Then $\alpha^3 - 2\alpha^2 + 3\alpha - 1 = (-\alpha - 2) - 2(\alpha - 2) + 3\alpha - 1 = 1$. Similarly $\beta^3 - \beta^2 + 2\beta + 4 = (-\beta - 2) - (\beta - 2) + 2\beta + 4 = 4$. The equation with roots $1$ and $4$ is $x^2 - 5x + 4 = 0$.",
  "Not reducing higher powers using the equation itself.",
  "U02-poly-reduction", "Polynomial reduction twice; non-obvious that both values are constants.",
  check=_c53, values=[mon(x**2 - 5*x + 4), mon(x**2 + 5*x + 4), mon(x**2 - 9*x + 8), mon(x**2 - 13*x + 40)],
  cognitive="Analysis")


def _c54():
    a, b, c = symbols('a b c', nonzero=True)
    res = resultant(a*x**2 + b*x + c, b*x**2 + c*x + a, x)
    F = expand(cancel(res / a))
    F = F / Poly(F, a, b, c).coeff_monomial(a**3)
    return simplify((a**3 + b**3 + c**3 - F) / (a*b*c))


q("U02-D-054", "Common roots", "Common root of cyclic equations", "Difficult", "Multi-step computation MCQ",
  r"If $a, b, c$ are non-zero real numbers and the equations $ax^2 + bx + c = 0$ and $bx^2 + cx + a = 0$ have a common root, then $\frac{a^3 + b^3 + c^3}{abc}$ equals",
  r"$3$",
  [(r"$1$", r"Reaches $a + b + c = 0$ but misremembers the identity as $a^3 + b^3 + c^3 = abc$."),
   (r"$0$", r"Uses the false implication $a + b + c = 0 \Rightarrow a^3 + b^3 + c^3 = 0$."),
   (r"$-3$", r"A sign slip in expanding $(bc - a^2)^2$ leads to $a^3 + b^3 + c^3 + 3abc = 0$.")],
  r"By cross-multiplication, a common root requires $(bc - a^2)^2 = (ab - c^2)(ac - b^2)$. Expanding, $a^4 - 3a^2bc + ab^3 + ac^3 = 0$, i.e. $a(a^3 + b^3 + c^3 - 3abc) = 0$. As $a \neq 0$, $a^3 + b^3 + c^3 = 3abc$ and the ratio is $3$.",
  r"Thinking $a + b + c = 0$ makes $a^3 + b^3 + c^3$ zero.",
  "U02-common-root-symmetric", "Common-root condition via elimination and factoring.",
  check=_c54, values=[3, 1, 0, -3], cognitive="Analysis",
  numerical=dict(question=r"If $a, b, c$ are non-zero real numbers and the equations $ax^2 + bx + c = 0$ and $bx^2 + cx + a = 0$ have a common root, then the value of $\frac{a^3 + b^3 + c^3}{abc}$ is", answer=3))


def _c55():
    p = x**2 + 2*x + 4
    s3 = sym(p, lambda a, b: a**3 + b**3)
    r_ = rem(Poly(x**2025, x), Poly(p, x)).as_expr()
    s2025 = sym(p, lambda a, b: r_.subs(x, a) + r_.subs(x, b))
    return (s3 == -16, simplify(s2025 + 2**2026) == 0)


q("U02-D-055", "Recurrence for power sums", "Large powers of roots", "Difficult", "Statement-based MCQ",
  r"Let $\alpha$ and $\beta$ be the roots of $x^2 + 2x + 4 = 0$. Statement I: $\alpha^3 + \beta^3 = -16$. Statement II: $\alpha^{2025} + \beta^{2025} = -2^{2026}$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Uses $x^3 + 8$ instead of $x^3 - 8$ as the multiple, so takes $\alpha^3 = -8$ for both statements."),
   (ST_TF, r"Uses $\alpha + \beta = 2$, getting $8 - 24 = -16$, but evaluates the large power correctly."),
   (ST_FT, r"Gets Statement I right but takes $\alpha^3 = -8$ for the large power.")],
  r"$(x - 2)(x^2 + 2x + 4) = x^3 - 8$, so $\alpha^3 = \beta^3 = 8$ and $\alpha^3 + \beta^3 = 16$; Statement I is false. Since $2025 = 3 \cdot 675$, $\alpha^{2025} = 8^{675} = 2^{2025}$, so $\alpha^{2025} + \beta^{2025} = 2^{2026}$; Statement II is false.",
  r"Wrong sign in the cube identity linked to $x^2 + 2x + 4$.",
  "U02-cube-trick", "Factorisation insight then large exponent reduction.",
  check=_c55, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")
