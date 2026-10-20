import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
x = symbols('x', positive=True)


def cx(expr, k):
    """Coefficient of x**k in the expanded form of expr (allows negative and fractional powers)."""
    s = 0
    for t in Add.make_args(expand(expr)):
        c, p = t.as_coeff_exponent(x)
        if simplify(p - k) == 0:
            s += c
    return nsimplify(simplify(s))


def rat_count(p, a, q, b, n):
    """Number of r in 0..n with (n - r)/a and r/b both integers (term p^((n-r)/a) q^(r/b) rational)."""
    return sum(1 for r in range(n + 1) if Rational(n - r, a).is_integer and Rational(r, b).is_integer)


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

T_GEN = "General term and specific coefficients"
T_PROD = "Coefficients in products of binomials"
T_RAT = "Rational and integral terms"
T_RATIO = "Ratio of consecutive coefficients and terms"

# ================================================================ EASY (14)

q("U05-A-001", T_GEN, "Term independent of x", "Easy", "Single-step computation MCQ",
  r"The term independent of $x$ in the expansion of $\left(2x^2 - \frac{1}{x}\right)^9$ is",
  r"$672$",
  [(r"$-672$", r"Sign slip: treats $(-1)^6$ as $-1$."),
   (r"$84$", r"Finds $r = 6$ and $\binom{9}{6} = 84$ but drops the factor $2^{3}$ from $(2x^2)^{3}$."),
   (r"$5376$", r"Raises $2$ to the power $r = 6$ in place of $9 - r = 3$, giving $84 \cdot 64$.")],
  r"$T_{r+1} = \binom{9}{r}(2x^2)^{9-r}\left(-\frac{1}{x}\right)^r = \binom{9}{r}2^{9-r}(-1)^r x^{18-3r}$. Setting $18 - 3r = 0$ gives $r = 6$, so the term is $\binom{9}{6} 2^3 (-1)^6 = 84 \cdot 8 = 672$.",
  "Attaching the numerical coefficient to the wrong power in the general term.",
  "U05-A-indep-term-basic", "General term plus one exponent equation.",
  check=lambda: cx((2*x**2 - 1/x)**9, 0), values=[672, -672, 84, 5376], cognitive="Application",
  numerical=dict(question=r"The term independent of $x$ in the expansion of $\left(2x^2 - \frac{1}{x}\right)^9$ is", answer=672))

q("U05-A-002", T_GEN, "Coefficient of a positive power", "Easy", "Single-step computation MCQ",
  r"The coefficient of $x^5$ in the expansion of $\left(x^2 - \frac{3}{x}\right)^7$ is",
  r"$-945$",
  [(r"$945$", r"Sign slip: takes $(-3)^3$ as $+27$."),
   (r"$-315$", r"Uses $3^2$ in place of $3^3$: $-\binom{7}{3} \cdot 9 = -315$."),
   (r"$-105$", r"Uses the factor $-3$ only once: $\binom{7}{3}(-3) = -105$.")],
  r"$T_{r+1} = \binom{7}{r}(x^2)^{7-r}\left(-\frac{3}{x}\right)^r = \binom{7}{r}(-3)^r x^{14-3r}$. For $14 - 3r = 5$, $r = 3$, so the coefficient is $\binom{7}{3}(-3)^3 = 35 \cdot (-27) = -945$.",
  "Not raising the constant inside the second term to the full power $r$.",
  "U05-A-coeff-xk-basic", "One exponent equation and one evaluation.",
  check=lambda: cx((x**2 - 3/x)**7, 5), values=[-945, 945, -315, -105], cognitive="Application")

q("U05-A-003", T_GEN, "A specified term", "Easy", "Single-step computation MCQ",
  r"The $5$th term in the expansion of $\left(2x - \frac{1}{x}\right)^7$ (in descending powers of $x$) is",
  r"$\frac{280}{x}$",
  [(r"$-\frac{84}{x^3}$", r"Takes $r = 5$ for the $5$th term: $\binom{7}{5}(2x)^2\left(-\frac{1}{x}\right)^5 = -\frac{84}{x^3}$."),
   (r"$-560x$", r"Swaps the powers: $\binom{7}{4}(2x)^4\left(-\frac{1}{x}\right)^3 = -560x$."),
   (r"$\frac{35}{x}$", r"Uses $r = 4$ but drops the factor $2^3$ from $(2x)^3$.")],
  r"$T_5 = T_{4+1} = \binom{7}{4}(2x)^{3}\left(-\frac{1}{x}\right)^4 = 35 \cdot 8x^3 \cdot \frac{1}{x^4} = \frac{280}{x}$.",
  "Using $r$ equal to the term number instead of one less.",
  "U05-A-kth-term", "Direct use of $T_{r+1}$.",
  check=lambda: binomial(7, 4)*(2*x)**3*(-1/x)**4,
  values=[280/x, -84/x**3, -560*x, 35/x], cognitive="Application")

def _c4():
    n = 15
    rs = [r for r in range(n + 1) if 2*(n - r) - 3*r == 0]
    return rs[0] + 1
q("U05-A-004", T_GEN, "Position of the term independent of x", "Easy", "Single-step computation MCQ",
  r"In the expansion of $\left(x^2 - \frac{1}{x^3}\right)^{15}$ in descending powers of $x$, the term independent of $x$ is the $k$th term. Then $k$ equals",
  r"$7$",
  [(r"$6$", r"Solves for $r = 6$ correctly but reports $r$ instead of the term number $r + 1$."),
   (r"$10$", r"Takes $-\frac{1}{x^3}$ as the first term of the binomial, so the exponent is $2r - 3(15 - r)$, giving $r = 9$ and position $10$, which counts in ascending rather than descending powers."),
   (r"$11$", r"Ignores the cube on $x^3$, using exponent $2(15 - r) - r = 30 - 3r$, so $r = 10$.")],
  r"$T_{r+1} = \binom{15}{r}(x^2)^{15-r}\left(-\frac{1}{x^3}\right)^r$ has power $30 - 2r - 3r = 30 - 5r$. This is $0$ for $r = 6$, which is the $7$th term.",
  "Confusing $r$ with the position $r + 1$.",
  "U05-A-indep-term-position", "One exponent equation and the index shift.",
  check=_c4, values=[7, 6, 10, 11], cognitive="Understanding")

q("U05-A-005", T_RATIO, "Ratio of consecutive coefficients", "Easy", "Single-step computation MCQ",
  r"In the expansion of $(1 + x)^{12}$, the ratio of the coefficient of $x^5$ to the coefficient of $x^4$ is",
  r"$\frac{8}{5}$",
  [(r"$\frac{5}{8}$", "Inverts the ratio."),
   (r"$\frac{7}{5}$", r"Uses $\frac{n - r}{r}$ with $r = 5$ in place of $\frac{n - r + 1}{r}$."),
   (r"$\frac{9}{4}$", r"Uses $\frac{n - r + 1}{r}$ with $r = 4$, the lower power.")],
  r"$\frac{\binom{12}{5}}{\binom{12}{4}} = \frac{12 - 5 + 1}{5} = \frac{8}{5}$; indeed $\frac{792}{495} = \frac{8}{5}$.",
  r"Misremembering $\frac{\binom{n}{r}}{\binom{n}{r-1}} = \frac{n-r+1}{r}$.",
  "U05-A-ratio-consecutive-basic", "One standard ratio.",
  check=lambda: cx((1 + x)**12, 5)/cx((1 + x)**12, 4),
  values=[Rational(8, 5), Rational(5, 8), Rational(7, 5), Rational(9, 4)], cognitive="Recall")

q("U05-A-006", T_GEN, "Coefficient with numerical constants", "Easy", "Single-step computation MCQ",
  r"The coefficient of $x^4$ in the expansion of $(2 - 3x)^6$ is",
  r"$4860$",
  [(r"$2160$", r"Swaps the powers of $2$ and $3$: $\binom{6}{4} 2^4 3^2$."),
   (r"$-4860$", r"Takes $(-3)^4$ as negative."),
   (r"$1215$", r"Forgets the factor $2^2$: $\binom{6}{4} 3^4$.")],
  r"$T_{r+1} = \binom{6}{r}2^{6-r}(-3x)^r$. With $r = 4$: $\binom{6}{4} \cdot 2^2 \cdot 81 = 15 \cdot 4 \cdot 81 = 4860$.",
  "Mismatching the powers of the two terms of the binomial.",
  "U05-A-coeff-xk-basic", "Direct general term.",
  check=lambda: cx((2 - 3*x)**6, 4), values=[4860, 2160, -4860, 1215], cognitive="Application",
  numerical=dict(question=r"The coefficient of $x^4$ in the expansion of $(2 - 3x)^6$ is", answer=4860))

q("U05-A-007", T_GEN, "Term independent of x", "Easy", "Single-step computation MCQ",
  r"The term independent of $x$ in the expansion of $\left(x + \frac{2}{x^2}\right)^6$ is",
  r"$60$",
  [(r"$15$", r"Finds $\binom{6}{2}$ and forgets the factor $2^2$."),
   (r"$30$", r"Uses $2^1$ in place of $2^2$."),
   (r"$240$", r"Uses $2^{6-r} = 2^4$ in place of $2^r$.")],
  r"$T_{r+1} = \binom{6}{r}x^{6-r}\left(\frac{2}{x^2}\right)^r = \binom{6}{r}2^r x^{6-3r}$. Setting $6 - 3r = 0$ gives $r = 2$, and the term is $15 \cdot 4 = 60$.",
  "Dropping or misplacing the constant factor in the second term.",
  "U05-A-indep-term-basic", "General term plus one exponent equation.",
  check=lambda: cx((x + 2/x**2)**6, 0), values=[60, 15, 30, 240], cognitive="Application",
  numerical=dict(question=r"The term independent of $x$ in the expansion of $\left(x + \frac{2}{x^2}\right)^6$ is", answer=60))

def _c8():
    a = symbols('a', positive=True)
    return solve(Eq(cx((1 + a*x)**6, 2), 60), a)[0]
q("U05-A-008", T_GEN, "Parameter from a coefficient", "Easy", "Inverse/parameter MCQ",
  r"If $a > 0$ and the coefficient of $x^2$ in the expansion of $(1 + ax)^6$ is $60$, then $a$ equals",
  r"$2$",
  [(r"$4$", r"Solves $a^2 = 4$ but reports $a^2$."),
   (r"$\sqrt{10}$", r"Uses $\binom{6}{1} = 6$ as the coefficient multiplier: $6a^2 = 60$."),
   (r"$\sqrt{2}$", r"Uses $6 \cdot 5 = 30$ without dividing by $2!$: $30a^2 = 60$.")],
  r"The coefficient of $x^2$ is $\binom{6}{2}a^2 = 15a^2 = 60$, so $a^2 = 4$ and, as $a > 0$, $a = 2$.",
  r"Using the wrong binomial coefficient for $x^2$.",
  "U05-A-inverse-coeff-param", "One equation in $a$.",
  check=_c8, values=[2, 4, sqrt(10), sqrt(2)], cognitive="Application")

q("U05-A-009", T_RAT, "Number of rational terms", "Easy", "Single-step computation MCQ",
  r"The number of rational terms in the expansion of $\left(\sqrt{2} + \sqrt[3]{3}\right)^{12}$ is",
  r"$3$",
  [(r"$5$", r"Only requires $\frac{r}{3}$ to be an integer, forgetting $\frac{12 - r}{2}$."),
   (r"$7$", r"Only requires $\frac{12 - r}{2}$ to be an integer, forgetting $\frac{r}{3}$."),
   (r"$2$", r"Lists $r = 6, 12$ as the common multiples of $2$ and $3$ and misses $r = 0$.")],
  r"$T_{r+1} = \binom{12}{r} 2^{\frac{12-r}{2}} 3^{\frac{r}{3}}$ is rational exactly when $r$ is even and a multiple of $3$, i.e. $r \in \{0, 6, 12\}$. So there are $3$ rational terms.",
  "Imposing only one of the two integrality conditions.",
  "U05-A-rational-terms-count", "Two divisibility conditions on $r$.",
  check=lambda: rat_count(2, 2, 3, 3, 12), values=[3, 5, 7, 2], cognitive="Application",
  numerical=dict(question=r"The number of rational terms in the expansion of $\left(\sqrt{2} + \sqrt[3]{3}\right)^{12}$ is", answer=3))

def _c10():
    s1 = cx((x + 1/x)**11, 0) == 0
    s2 = cx((x**2 + 1/x)**12, 3) == binomial(12, 6)
    return (s1, s2)
q("U05-A-010", T_GEN, "Existence of terms", "Easy", "Statement-based MCQ",
  r"Statement I: The expansion of $\left(x + \frac{1}{x}\right)^{11}$ has no term independent of $x$. Statement II: The coefficient of $x^3$ in the expansion of $\left(x^2 + \frac{1}{x}\right)^{12}$ is $\binom{12}{6}$." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II by solving $24 - 2r - r = 3$ carelessly as $r = 6$."),
   (ST_FF, r"Thinks a term independent of $x$ always exists in $\left(x + \frac{1}{x}\right)^n$, and also rejects Statement II."),
   (ST_FT, r"Believes the middle terms of $\left(x + \frac{1}{x}\right)^{11}$ give a constant term, and accepts Statement II via $r = 6$.")],
  r"In $\left(x + \frac{1}{x}\right)^{11}$ the powers are $11 - 2r$, always odd, so no constant term: Statement I is true. In $\left(x^2 + \frac{1}{x}\right)^{12}$ the power is $24 - 3r = 3$ for $r = 7$, so the coefficient is $\binom{12}{7} = 792$, not $\binom{12}{6} = 924$: Statement II is false.",
  "Solving the exponent equation carelessly.",
  "U05-A-statement-existence", "Two short independent checks.",
  check=_c10, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding")

q("U05-A-011", T_GEN, "Term from the end", "Easy", "Single-step computation MCQ",
  r"The $4$th term from the end in the expansion of $\left(x - \frac{2}{x}\right)^9$ (in descending powers of $x$) is",
  r"$\frac{5376}{x^3}$",
  [(r"$-672x^3$", r"Computes the $4$th term from the beginning."),
   (r"$-\frac{4032}{x}$", r"Takes the $4$th term from the end as $T_{n-k+1} = T_6$."),
   (r"$\frac{84}{x^3}$", r"Finds $T_7$ but forgets the factor $(-2)^6 = 64$.")],
  r"The $4$th term from the end of $10$ terms is $T_7 = \binom{9}{6}x^3\left(-\frac{2}{x}\right)^6 = 84 \cdot 64 \cdot x^{-3} = \frac{5376}{x^3}$.",
  r"Using $T_{n-k+1}$ in place of $T_{n-k+2}$ for the $k$th term from the end.",
  "U05-A-kth-term", "Position from the end, then the general term.",
  check=lambda: binomial(9, 6)*x**3*(-2/x)**6,
  values=[5376/x**3, -672*x**3, -4032/x, 84/x**3], cognitive="Application")

q("U05-A-012", T_GEN, "Coefficient of a negative power", "Easy", "Single-step computation MCQ",
  r"The coefficient of $x^{-7}$ in the expansion of $\left(2x - \frac{1}{x^2}\right)^8$ is",
  r"$-448$",
  [(r"$448$", r"Sign slip: takes $(-1)^5$ as $+1$."),
   (r"$-56$", r"Forgets the factor $2^3$ from $(2x)^3$."),
   (r"$-1792$", r"Uses $2^r = 2^5$ in place of $2^{8-r} = 2^3$.")],
  r"$T_{r+1} = \binom{8}{r}(2x)^{8-r}\left(-\frac{1}{x^2}\right)^r = \binom{8}{r}2^{8-r}(-1)^r x^{8-3r}$. For $8 - 3r = -7$, $r = 5$: $56 \cdot 8 \cdot (-1) = -448$.",
  "Placing the constant factor on the wrong power.",
  "U05-A-coeff-negative-power", "One exponent equation.",
  check=lambda: cx((2*x - 1/x**2)**8, -7), values=[-448, 448, -56, -1792], cognitive="Application")

def _c13():
    opts = [10, 9, 8, 6]
    good = [n for n in opts if any(3*(n - r) - 2*r == 0 for r in range(n + 1))]
    return good[0] if len(good) == 1 else None
q("U05-A-013", T_GEN, "Condition for a term independent of x", "Easy", "Conceptual/application MCQ",
  r"The expansion of $\left(x^3 + \frac{1}{x^2}\right)^n$, $n \in \mathbb{N}$, has a term independent of $x$ for which one of the following values of $n$?",
  r"$10$",
  [(r"$9$", r"Thinks $n$ must be a multiple of $3$ because of $x^3$."),
   (r"$8$", r"Thinks $n$ must be a multiple of $2$ because of $x^{-2}$."),
   (r"$6$", r"Takes $n$ to be a multiple of $3 \cdot 2 = 6$, the product of the exponents, in place of their sum.")],
  r"$T_{r+1}$ has power $3(n - r) - 2r = 3n - 5r$. This is $0$ only if $r = \frac{3n}{5}$ is an integer, i.e. $5 \mid n$. Among the values, only $n = 10$ works ($r = 6$).",
  "Guessing the divisibility condition from one exponent only.",
  "U05-A-indep-term-existence", "One exponent equation and a divisibility observation.",
  check=_c13, values=[10, 9, 8, 6], cognitive="Understanding")

q("U05-A-014", T_PROD, "Coefficient in a product of two binomials", "Easy", "Single-step computation MCQ",
  r"The coefficient of $x^2$ in the expansion of $(1 + x)^5(1 - 2x)^4$ is",
  r"$-6$",
  [(r"$74$", r"Sign slip in the cross term: adds $5 \cdot 8$ in place of $5 \cdot (-8)$."),
   (r"$34$", r"Omits the cross term $(5x)(-8x)$, adding only $24 + 10$."),
   (r"$-24$", r"Takes the $x^2$ coefficient of $(1 - 2x)^4$ as $\binom{4}{2} = 6$, forgetting $(-2)^2$.")],
  r"$(1 + x)^5 = 1 + 5x + 10x^2 + \dots$ and $(1 - 2x)^4 = 1 - 8x + 24x^2 - \dots$. The $x^2$ coefficient is $1 \cdot 24 + 5 \cdot (-8) + 10 \cdot 1 = -6$.",
  "Forgetting the cross terms when multiplying expansions.",
  "U05-A-product-two-binomials", "Three products of low-order coefficients.",
  check=lambda: cx((1 + x)**5*(1 - 2*x)**4, 2), values=[-6, 74, 34, -24], cognitive="Application")

# ================================================================ MEDIUM (21)

q("U05-A-015", T_PROD, "Product of conjugate-type binomials", "Medium", "Multi-step computation MCQ",
  r"The coefficient of $x^3$ in the expansion of $(1 + x)^6(1 - x)^4$ is",
  r"$-8$",
  [(r"$8$", r"Writes $(1 - x^2)^4 = 1 + 4x^2 + \dots$, dropping the sign."),
   (r"$-4$", r"Takes the $x$ coefficient of $(1 + x)^2$ as $1$: $(-4)(1)$."),
   (r"$16$", r"Adds the $x^3$ coefficients of the two factors, $20 + (-4)$, in place of multiplying the series.")],
  r"$(1 + x)^6(1 - x)^4 = (1 - x^2)^4(1 + x)^2 = (1 - 4x^2 + 6x^4 - \dots)(1 + 2x + x^2)$. The $x^3$ term comes only from $(-4x^2)(2x)$, so the coefficient is $-8$.",
  "Adding coefficients of two factors instead of convolving them.",
  "U05-A-product-conjugate-pair", "Regrouping into $(1 - x^2)^4(1 + x)^2$ and one product.",
  check=lambda: cx((1 + x)**6*(1 - x)**4, 3), values=[-8, 8, -4, 16], cognitive="Application")

def _c16():
    n, r = symbols('n r', positive=True, integer=True)
    sol = solve([Eq((n - r + 1)/r, Rational(330, 165)), Eq((n - r)/(r + 1), Rational(462, 330))], [n, r], dict=True)
    nn = sol[0][n]
    assert [binomial(nn, k) for k in (sol[0][r] - 1, sol[0][r], sol[0][r] + 1)] == [165, 330, 462]
    return nn
q("U05-A-016", T_RATIO, "Three consecutive coefficients", "Medium", "Inverse/parameter MCQ",
  r"The coefficients of three consecutive terms in the expansion of $(1 + x)^n$ are $165$, $330$ and $462$ in that order. Then $n$ equals",
  r"$11$",
  [(r"$12$", r"Uses $\frac{\binom{n}{r}}{\binom{n}{r-1}} = \frac{n - r}{r}$, giving $n = 3r$ and $5(n - r - 1) = 7(r + 1)$, so $r = 4$, $n = 12$."),
   (r"$4$", r"Stops at $r = 4$ (the power of $x$ attached to $330$) and reports it as $n$."),
   (r"$5$", r"Reports the position $T_5$ of the term with coefficient $330$.")],
  r"Let the coefficients be $\binom{n}{r-1}, \binom{n}{r}, \binom{n}{r+1}$. Then $\frac{n - r + 1}{r} = 2$ gives $n = 3r - 1$, and $\frac{n - r}{r + 1} = \frac{7}{5}$ gives $5n = 12r + 7$. So $15r - 5 = 12r + 7$, $r = 4$, $n = 11$; check $\binom{11}{3}, \binom{11}{4}, \binom{11}{5} = 165, 330, 462$.",
  "Using the wrong ratio formula for consecutive binomial coefficients.",
  "U05-A-consecutive-coeff-n", "Two ratio equations solved simultaneously.",
  check=_c16, values=[11, 12, 4, 5], cognitive="Application",
  numerical=dict(question=r"The coefficients of three consecutive terms in the expansion of $(1 + x)^n$ are $165$, $330$ and $462$ in that order. The value of $n$ is", answer=11))

def _c17():
    t = symbols('t', positive=True)
    T5 = binomial(10, 4)*t**4
    T6 = binomial(10, 5)*t**5
    return solve(Eq(T5, T6), t)[0]
q("U05-A-017", T_RATIO, "Equal consecutive terms", "Medium", "Inverse/parameter MCQ",
  r"If $x > 0$ and the $5$th and $6$th terms in the expansion of $(1 + x)^{10}$ (in ascending powers of $x$) are equal, then $x$ equals",
  r"$\frac{5}{6}$",
  [(r"$\frac{6}{5}$", r"Inverts the ratio $\frac{T_6}{T_5} = \frac{6}{5}x$."),
   (r"$1$", r"Uses $\frac{n - r}{r} = \frac{5}{5}$ for the ratio of coefficients."),
   (r"$\frac{4}{7}$", r"Uses $\frac{n - r + 1}{r}$ with $r = 4$, i.e. $\frac{7}{4}x = 1$.")],
  r"$T_5 = \binom{10}{4}x^4$ and $T_6 = \binom{10}{5}x^5$. Then $\frac{T_6}{T_5} = \frac{10 - 5 + 1}{5}x = \frac{6}{5}x = 1$, so $x = \frac{5}{6}$.",
  "Mis-indexing the ratio of consecutive terms.",
  "U05-A-ratio-consecutive-terms", "Index bookkeeping plus a ratio.",
  check=_c17, values=[Rational(5, 6), Rational(6, 5), 1, Rational(4, 7)], cognitive="Application")

q("U05-A-018", T_GEN, "Term independent of x with surd coefficients", "Medium", "Multi-step computation MCQ",
  r"The term independent of $x$ in the expansion of $\left(\frac{\sqrt{x}}{\sqrt{3}} + \frac{\sqrt{3}}{2x^2}\right)^{10}$, $x > 0$, is",
  r"$\frac{5}{12}$",
  [(r"$\frac{45}{4}$", r"Finds $r = 2$ but ignores all the powers of $\sqrt{3}$."),
   (r"$\frac{5}{3}$", r"Handles the powers of $\sqrt{3}$ but forgets $\left(\frac{1}{2}\right)^2$."),
   (r"$\frac{5}{6}$", r"Uses $\frac{1}{2}$ in place of $\left(\frac{1}{2}\right)^2$.")],
  r"$T_{r+1} = \binom{10}{r}\left(\frac{x^{1/2}}{\sqrt{3}}\right)^{10-r}\left(\frac{\sqrt{3}}{2x^2}\right)^r$ has power $\frac{10 - r}{2} - 2r$, which is $0$ for $r = 2$. The term is $45 \cdot \frac{1}{81} \cdot \frac{3}{4} = \frac{5}{12}$.",
  "Losing track of constant factors carried by each binomial term.",
  "U05-A-indep-term-surd-coeffs", "Fractional exponent equation, then careful constant bookkeeping.",
  check=lambda: cx((sqrt(x)/sqrt(3) + sqrt(3)/(2*x**2))**10, 0),
  values=[Rational(5, 12), Rational(45, 4), Rational(5, 3), Rational(5, 6)], cognitive="Application")

q("U05-A-019", T_RAT, "Number of rational terms (large index)", "Medium", "Multi-step computation MCQ",
  r"The number of rational terms in the expansion of $\left(\sqrt{3} + \sqrt[4]{5}\right)^{100}$ is",
  r"$26$",
  [(r"$51$", r"Only requires $\frac{100 - r}{2}$ to be an integer."),
   (r"$25$", r"Counts $\frac{100}{4} = 25$ multiples of $4$, missing $r = 0$."),
   (r"$75$", r"Gives the number of irrational terms, $101 - 26$.")],
  r"$T_{r+1} = \binom{100}{r}3^{\frac{100-r}{2}}5^{\frac{r}{4}}$ is rational iff $4 \mid r$ and $100 - r$ is even. Since $4 \mid r$ forces $r$ even, $r = 0, 4, \dots, 100$, giving $26$ terms.",
  "Off-by-one counting of the admissible $r$.",
  "U05-A-rational-terms-count", "Combining two conditions and counting an arithmetic progression.",
  check=lambda: rat_count(3, 2, 5, 4, 100), values=[26, 51, 25, 75], cognitive="Application",
  numerical=dict(question=r"The number of rational terms in the expansion of $\left(\sqrt{3} + \sqrt[4]{5}\right)^{100}$ is", answer=26))

q("U05-A-020", T_RAT, "Number of irrational terms", "Medium", "Multi-step computation MCQ",
  r"The number of irrational terms in the expansion of $\left(\sqrt[3]{2} + \sqrt[4]{3}\right)^{48}$ is",
  r"$44$",
  [(r"$5$", r"Gives the number of rational terms."),
   (r"$43$", r"Takes the expansion to have $48$ terms."),
   (r"$36$", r"Only requires $4 \mid r$, getting $13$ rational terms and $49 - 13 = 36$.")],
  r"$T_{r+1} = \binom{48}{r}2^{\frac{48-r}{3}}3^{\frac{r}{4}}$ is rational iff $4 \mid r$ and $3 \mid (48 - r)$, i.e. $12 \mid r$: $r = 0, 12, 24, 36, 48$. So $5$ of the $49$ terms are rational and $44$ are irrational.",
  "Counting $n$ terms instead of $n + 1$, or imposing one condition only.",
  "U05-A-irrational-terms-count", "Two divisibility conditions, then complement count.",
  check=lambda: 49 - rat_count(2, 3, 3, 4, 48), values=[44, 5, 43, 36], cognitive="Application",
  numerical=dict(question=r"The number of irrational terms in the expansion of $\left(\sqrt[3]{2} + \sqrt[4]{3}\right)^{48}$ is", answer=44))

def _c21():
    a = 2
    b = symbols('b', positive=True)
    c1 = cx((a*x**2 + 1/(b*x))**10, 8)
    c2 = cx((a*x - 1/(b*x**2))**10, -8)
    return solve(Eq(c1, c2), b)[0]
q("U05-A-021", T_GEN, "Equal coefficients in two expansions", "Medium", "Inverse/parameter MCQ",
  r"Let $b > 0$. If the coefficient of $x^8$ in $\left(2x^2 + \frac{1}{bx}\right)^{10}$ equals the coefficient of $x^{-8}$ in $\left(2x - \frac{1}{bx^2}\right)^{10}$, then $b$ equals",
  r"$\frac{1}{2}$",
  [(r"$2$", r"Simplifies $\frac{2^6}{b^4} = \frac{2^4}{b^6}$ wrongly to $2^2 = b^2$, so $b = 2$."),
   (r"$\frac{1}{4}$", r"Reaches $b^2 = \frac{1}{4}$ and forgets the square root."),
   (r"$\frac{1}{\sqrt{2}}$", r"Simplifies $\frac{2^6}{b^4} = \frac{2^4}{b^6}$ wrongly to $2b^2 = 1$.")],
  r"In the first, the power is $20 - 3r = 8$, so $r = 4$ and the coefficient is $\binom{10}{4}\frac{2^6}{b^4}$. In the second, $10 - 3r = -8$, so $r = 6$ and the coefficient is $\binom{10}{6}\frac{2^4}{b^6}$. Equating gives $2^2 b^2 = 1$, so $b = \frac{1}{2}$.",
  "Algebra slips when cancelling powers of the parameters.",
  "U05-A-equal-coeff-two-expansions", "Two general terms and an equation in $b$.",
  check=_c21, values=[Rational(1, 2), 2, Rational(1, 4), 1/sqrt(2)], cognitive="Application")

def _c22():
    e = (1 + x)**6*(1 - x)**6
    return (cx(e, 6) == 20, cx(e, 5) == 0)
q("U05-A-022", T_PROD, "Coefficients in (1+x)^n (1-x)^n", "Medium", "Statement-based MCQ",
  r"Consider the expansion of $(1 + x)^6(1 - x)^6$. Statement I: The coefficient of $x^6$ is $20$. Statement II: The coefficient of $x^5$ is $0$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Takes $\binom{6}{3}$ without the sign $(-1)^3$."),
   (ST_TF, r"Gets the coefficient of $x^6$ without the sign and also expects odd powers to survive."),
   (ST_FF, r"Correctly rejects Statement I but expects a nonzero odd-power coefficient.")],
  r"$(1 + x)^6(1 - x)^6 = (1 - x^2)^6 = \sum \binom{6}{k}(-1)^k x^{2k}$. Only even powers occur, so the coefficient of $x^5$ is $0$ (Statement II true). The coefficient of $x^6$ is $\binom{6}{3}(-1)^3 = -20$, so Statement I is false.",
  r"Forgetting the sign $(-1)^k$ in $(1 - x^2)^n$.",
  "U05-A-statement-product", "Recognising $(1 - x^2)^6$ and checking two claims.",
  check=_c22, values=[(False, True), (True, True), (True, False), (False, False)], cognitive="Understanding")

q("U05-A-023", T_GEN, "Coefficient with fractional constants", "Medium", "Single-step computation MCQ",
  r"The coefficient of $x^3$ in the expansion of $\left(\frac{x}{3} - \frac{2}{x^2}\right)^9$ is",
  r"$\frac{16}{243}$",
  [(r"$-\frac{16}{243}$", r"Sign slip: takes $(-2)^2$ as negative."),
   (r"$\frac{4}{243}$", r"Forgets the factor $2^2$: $\frac{36}{3^7}$."),
   (r"$\frac{8}{243}$", r"Uses $2^1$ in place of $2^2$: $\frac{72}{3^7}$.")],
  r"$T_{r+1} = \binom{9}{r}\left(\frac{x}{3}\right)^{9-r}\left(-\frac{2}{x^2}\right)^r$ has power $9 - 3r = 3$, so $r = 2$. The coefficient is $36 \cdot \frac{1}{3^7} \cdot 4 = \frac{144}{2187} = \frac{16}{243}$.",
  "Mishandling the constant raised to the power $r$.",
  "U05-A-coeff-xk-fraction", "Exponent equation then fractional arithmetic.",
  check=lambda: cx((x/3 - 2/x**2)**9, 3),
  values=[Rational(16, 243), Rational(-16, 243), Rational(4, 243), Rational(8, 243)], cognitive="Application")

q("U05-A-024", T_PROD, "Product of binomials in x and x^2", "Medium", "Multi-step computation MCQ",
  r"The coefficient of $x^4$ in the expansion of $(1 + x^2)^5(1 + x)^4$ is",
  r"$41$",
  [(r"$31$", r"Misses the pairing $10x^4 \cdot 1$."),
   (r"$40$", r"Misses the pairing $1 \cdot x^4$."),
   (r"$16$", r"Adds $1 + 5 + 10$, forgetting to multiply by the coefficients of $(1 + x)^4$.")],
  r"$(1 + x^2)^5 = 1 + 5x^2 + 10x^4 + \dots$ and $(1 + x)^4 = 1 + 4x + 6x^2 + 4x^3 + x^4$. The $x^4$ coefficient is $1 \cdot 1 + 5 \cdot 6 + 10 \cdot 1 = 41$.",
  "Missing one of the pairings that make up the power.",
  "U05-A-product-two-binomials", "Three pairings to collect.",
  check=lambda: cx((1 + x**2)**5*(1 + x)**4, 4), values=[41, 31, 40, 16], cognitive="Application")

def _c25():
    k = symbols('k', positive=True)
    return solve(Eq(cx((sqrt(x) - k/x**2)**10, 0), 405), k)[0]
q("U05-A-025", T_GEN, "Parameter from the term independent of x", "Medium", "Inverse/parameter MCQ",
  r"If $k > 0$ and the term independent of $x$ in the expansion of $\left(\sqrt{x} - \frac{k}{x^2}\right)^{10}$ is $405$, then $k$ equals",
  r"$3$",
  [(r"$9$", r"Reaches $k^2 = 9$ and forgets the square root."),
   (r"$\sqrt[4]{3}$", r"Raises $k$ to the power $10 - r = 8$: $45k^8 = 405$."),
   (r"$\sqrt{3}$", r"Squares the coefficient twice, writing $(kx^{-2})^2 = k^4x^{-4}$: $45k^4 = 405$.")],
  r"The power in $T_{r+1}$ is $\frac{10 - r}{2} - 2r = 0$, so $r = 2$ and the term is $\binom{10}{2}k^2 = 45k^2$. Then $45k^2 = 405$, $k^2 = 9$, $k = 3$.",
  "Mismatching the power of the parameter with $r$.",
  "U05-A-inverse-indep-param", "Exponent equation then a parameter equation.",
  check=_c25, values=[3, 9, 3**Rational(1, 4), sqrt(3)], cognitive="Application")

q("U05-A-026", T_PROD, "Product with unequal indices", "Medium", "Multi-step computation MCQ",
  r"The coefficient of $x^4$ in the expansion of $(1 + x)^{12}(1 - x)^{10}$ is",
  r"$35$",
  [(r"$45$", r"Keeps only $45x^4$ from $(1 - x^2)^{10}$, missing $(-10x^2)(x^2)$."),
   (r"$55$", r"Sign slip: uses $+10x^2$ in $(1 - x^2)^{10}$."),
   (r"$25$", r"Uses $2$ as the $x^2$ coefficient of $(1 + x)^2$.")],
  r"$(1 + x)^{12}(1 - x)^{10} = (1 - x^2)^{10}(1 + x)^2 = (1 - 10x^2 + 45x^4 - \dots)(1 + 2x + x^2)$. The $x^4$ coefficient is $45 + (-10)(1) = 35$.",
  r"Not regrouping into $(1 - x^2)^{10}$, or losing a pairing.",
  "U05-A-product-conjugate-pair", "Regrouping plus two pairings.",
  check=lambda: cx((1 + x)**12*(1 - x)**10, 4), values=[35, 45, 55, 25], cognitive="Application",
  numerical=dict(question=r"The coefficient of $x^4$ in the expansion of $(1 + x)^{12}(1 - x)^{10}$ is", answer=35))

def _c28():
    k = symbols('k', nonzero=True)
    e = (2 + k*x)**8
    s = [v for v in solve(Eq(cx(e, 3), cx(e, 4)), k) if v != 0]
    return s[0]
q("U05-A-027", T_GEN, "Equal coefficients of consecutive powers", "Medium", "Inverse/parameter MCQ",
  r"If $k \ne 0$ and the coefficients of $x^3$ and $x^4$ in the expansion of $(2 + kx)^8$ are equal, then $k$ equals",
  r"$\frac{8}{5}$",
  [(r"$\frac{5}{8}$", r"Inverts the final ratio."),
   (r"$\frac{4}{5}$", r"Ignores the powers of $2$: $\binom{8}{3} = \binom{8}{4}k$."),
   (r"$\frac{16}{5}$", r"Takes the powers of $2$ as $2^5$ and $2^3$: $56 \cdot 32 = 70 \cdot 8k$.")],
  r"$\binom{8}{3}2^5k^3 = \binom{8}{4}2^4k^4$, so $56 \cdot 2 = 70k$ and $k = \frac{112}{70} = \frac{8}{5}$.",
  "Dropping the powers of the constant term.",
  "U05-A-equal-coeff-param", "Two general terms and a linear equation.",
  check=_c28, values=[Rational(8, 5), Rational(5, 8), Rational(4, 5), Rational(16, 5)], cognitive="Application")

def _c28b():
    a = symbols('a')
    av = solve(Eq(cx((1 + a*x)**8*(1 - 2*x)**6, 1), 4), a)[0]
    return cx((1 + av*x)**8*(1 - 2*x)**6, 2)
q("U05-A-028", T_PROD, "Parameter then coefficient in a product", "Medium", "Multi-step computation MCQ",
  r"If the coefficient of $x$ in the expansion of $(1 + ax)^8(1 - 2x)^6$ is $4$, then the coefficient of $x^2$ in the same expansion is",
  r"$-20$",
  [(r"$184$", r"Sign slip in $8a - 12 = 4$ giving $a = -1$, then $28 + 96 + 60$."),
   (r"$172$", r"Finds $a = 2$ but omits the cross term $(16x)(-12x)$."),
   (r"$364$", r"Finds $a = 2$ but adds the cross term as $+192$.")],
  r"The coefficient of $x$ is $8a - 12 = 4$, so $a = 2$. Then $(1 + 2x)^8 = 1 + 16x + 112x^2 + \dots$ and $(1 - 2x)^6 = 1 - 12x + 60x^2 - \dots$, so the $x^2$ coefficient is $112 + 16(-12) + 60 = -20$.",
  "Omitting or mis-signing the cross term.",
  "U05-A-product-param-then-coeff", "Find the parameter, then a three-term convolution.",
  check=_c28b,
  values=[-20, 184, 172, 364], cognitive="Application")

q("U05-A-029", T_GEN, "Count of terms with positive powers", "Medium", "Multi-step computation MCQ",
  r"The number of terms in the expansion of $\left(x^3 - \frac{1}{x^2}\right)^{15}$ that contain a positive power of $x$ is",
  r"$9$",
  [(r"$10$", r"Also counts the term independent of $x$ ($r = 9$)."),
   (r"$8$", r"Counts $r = 1, \dots, 8$, missing $r = 0$."),
   (r"$6$", r"Counts the terms with negative powers ($r = 10, \dots, 15$).")],
  r"The power in $T_{r+1}$ is $3(15 - r) - 2r = 45 - 5r$, which is positive for $r \le 8$. So $r = 0, 1, \dots, 8$ give $9$ terms.",
  "Off-by-one counting, or including the constant term.",
  "U05-A-count-positive-power-terms", "Inequality on the exponent and a careful count.",
  check=lambda: sum(1 for r in range(16) if 45 - 5*r > 0), values=[9, 10, 8, 6], cognitive="Application",
  numerical=dict(question=r"The number of terms in the expansion of $\left(x^3 - \frac{1}{x^2}\right)^{15}$ that contain a positive power of $x$ is", answer=9))

def _c30():
    n = symbols('n', positive=True, integer=True)
    eq = expand_func(2*binomial(n, 5) - binomial(n, 4) - binomial(n, 6))
    return sum(v for v in solve(eq, n) if v >= 6)
q("U05-A-030", T_RATIO, "Coefficients in arithmetic progression", "Medium", "Inverse/parameter MCQ",
  r"The coefficients of the $5$th, $6$th and $7$th terms in the expansion of $(1 + x)^n$ are in arithmetic progression. The sum of all possible values of $n$ is",
  r"$21$",
  [(r"$7$", r"Keeps only the smaller root of $n^2 - 21n + 98 = 0$."),
   (r"$14$", r"Keeps only the larger root."),
   (r"$98$", r"Gives the product of the roots in place of their sum.")],
  r"$2\binom{n}{5} = \binom{n}{4} + \binom{n}{6}$. Dividing by $\binom{n}{5}$: $2 = \frac{5}{n - 4} + \frac{n - 5}{6}$, which simplifies to $n^2 - 21n + 98 = 0$, so $n = 7$ or $14$. Both allow a $7$th term, so the sum is $21$.",
  "Discarding a valid root of the quadratic.",
  "U05-A-ap-coefficients", "Ratio form of the AP condition, a quadratic, and checking both roots.",
  check=_c30, values=[21, 7, 14, 98], cognitive="Application",
  numerical=dict(question=r"The coefficients of the $5$th, $6$th and $7$th terms in the expansion of $(1 + x)^n$ are in arithmetic progression. The sum of all possible values of $n$ is", answer=21))

q("U05-A-031", T_GEN, "Requested power absent", "Medium", "Conceptual/application MCQ",
  r"The coefficient of $x^4$ in the expansion of $\left(x^2 - \frac{2}{x}\right)^{10}$ is",
  r"$0$",
  [(r"$-8064$", r"Rounds $r = \frac{16}{3}$ to $5$ and gives the coefficient of $x^5$."),
   (r"$13440$", r"Rounds $r = \frac{16}{3}$ to $6$ and gives the coefficient of $x^2$."),
   (r"$3360$", r"Writes the power as $20 - 4r$ (treating $\frac{2}{x}$ as $\frac{2}{x^2}$), so $r = 4$, which is really the $x^8$ term.")],
  r"$T_{r+1} = \binom{10}{r}(-2)^r x^{20 - 3r}$. For $20 - 3r = 4$ we need $r = \frac{16}{3}$, not an integer, so no term contains $x^4$ and its coefficient is $0$.",
  "Forcing an integer $r$ when the exponent equation has no integer solution.",
  "U05-A-absent-power", "Recognising a non-integral $r$; trap for students who round.",
  check=lambda: cx((x**2 - 2/x)**10, 4), values=[0, -8064, 13440, 3360], cognitive="Analysis")

q("U05-A-032", T_GEN, "Fractional exponents", "Medium", "Multi-step computation MCQ",
  r"The term independent of $x$ in the expansion of $\left(\sqrt{x} + \frac{2}{\sqrt[3]{x}}\right)^{10}$, $x > 0$, is",
  r"$13440$",
  [(r"$210$", r"Finds $r = 6$ but forgets the factor $2^6$."),
   (r"$3360$", r"Uses $2^{10 - r} = 2^4$ in place of $2^r$."),
   (r"$8064$", r"Drops the denominators in $\frac{10 - r}{2} = \frac{r}{3}$, solving $10 - r = r$, so $r = 5$: $\binom{10}{5}2^5$.")],
  r"$T_{r+1} = \binom{10}{r}x^{\frac{10 - r}{2}}2^r x^{-\frac{r}{3}}$. Setting $\frac{10 - r}{2} - \frac{r}{3} = 0$ gives $30 - 5r = 0$, $r = 6$, and the term is $210 \cdot 64 = 13440$.",
  "Clearing fractional exponents carelessly.",
  "U05-A-indep-term-fractional-exp", "Fractional exponent equation plus evaluation.",
  check=lambda: cx((sqrt(x) + 2/x**Rational(1, 3))**10, 0), values=[13440, 210, 3360, 8064], cognitive="Application",
  numerical=dict(question=r"The term independent of $x$ in the expansion of $\left(\sqrt{x} + \frac{2}{\sqrt[3]{x}}\right)^{10}$, $x > 0$, is", answer=13440))

def _c33():
    for n in range(3, 40):
        e4 = binomial(n, n - 3)*(Integer(2)**Rational(1, 3))**3*(Integer(3)**Rational(-1, 3))**(n - 3)
        t4 = binomial(n, 3)*(Integer(2)**Rational(1, 3))**(n - 3)*(Integer(3)**Rational(-1, 3))**3
        if simplify(t4/e4 - 36) == 0:
            return n
q("U05-A-033", T_GEN, "Terms from the beginning and the end", "Medium", "Inverse/parameter MCQ",
  r"In the expansion of $\left(\sqrt[3]{2} + \frac{1}{\sqrt[3]{3}}\right)^n$, $n \ge 3$, the ratio of the $4$th term from the beginning to the $4$th term from the end is $36$. Then $n$ equals",
  r"$12$",
  [(r"$9$", r"Drops the factors $2^1$ and $3^{-1}$ in the two terms, getting $6^{\frac{n-3}{3}} = 36$."),
   (r"$8$", r"Writes the ratio as $6^{n-6}$, forgetting the cube roots."),
   (r"$5$", r"Drops the factors $2^1$, $3^{-1}$ and also the cube roots: $6^{n-3} = 36$.")],
  r"$T_4 = \binom{n}{3}2^{\frac{n-3}{3}}3^{-1}$, and the $4$th term from the end is $\binom{n}{3}2^{1}3^{-\frac{n-3}{3}}$. Their ratio is $2^{\frac{n-6}{3}}3^{\frac{n-6}{3}} = 6^{\frac{n-6}{3}} = 36$, so $\frac{n-6}{3} = 2$ and $n = 12$.",
  "Forgetting that each of the two terms carries a small power of the other surd.",
  "U05-A-terms-from-ends-ratio", "Two symmetric terms, exponent algebra and an equation.",
  check=_c33, values=[12, 9, 8, 5], cognitive="Application")

q("U05-A-034", T_RATIO, "Same power in two expansions", "Medium", "Single-step computation MCQ",
  r"The ratio of the coefficient of $x^5$ in $(1 + x)^{12}$ to the coefficient of $x^5$ in $(1 + x)^{11}$ is",
  r"$\frac{12}{7}$",
  [(r"$\frac{7}{12}$", "Inverts the ratio."),
   (r"$2$", r"Uses the middle-term fact $\binom{2m}{m} = 2\binom{2m-1}{m}$, which does not apply here."),
   (r"$\frac{12}{5}$", r"Uses the coefficient of $x^4$ in $(1 + x)^{11}$, i.e. $\frac{792}{330}$.")],
  r"$\frac{\binom{12}{5}}{\binom{11}{5}} = \frac{12}{12 - 5} = \frac{12}{7}$, since $\binom{n}{r} = \frac{n}{n - r}\binom{n-1}{r}$; numerically $\frac{792}{462} = \frac{12}{7}$.",
  r"Applying a remembered special case outside its conditions.",
  "U05-A-ratio-coeff-two-expansions", "One identity or direct evaluation.",
  check=lambda: cx((1 + x)**12, 5)/cx((1 + x)**11, 5),
  values=[Rational(12, 7), Rational(7, 12), 2, Rational(12, 5)], cognitive="Understanding")

def _c35():
    n = symbols('n', positive=True, integer=True)
    return [v for v in solve(Eq(binomial(n, 2).expand(func=True)*9, 1890), n) if v > 0][0]
q("U05-A-035", T_GEN, "Index from a coefficient", "Medium", "Inverse/parameter MCQ",
  r"If the coefficient of $x^2$ in the expansion of $(1 + 3x)^n$ is $1890$, then $n$ equals",
  r"$21$",
  [(r"$36$", r"Uses $3$ in place of $3^2$: $\frac{3n(n-1)}{2} = 1890$."),
   (r"$15$", r"Forgets to divide by $2!$: $9n(n-1) = 1890$."),
   (r"$20$", r"Solves $n(n-1) = 420$ but reports the smaller factor.")],
  r"$\binom{n}{2}3^2 = \frac{9n(n-1)}{2} = 1890$ gives $n(n-1) = 420 = 21 \cdot 20$, so $n = 21$.",
  r"Using $3$ in place of $3^2$ or $n(n-1)$ in place of $\binom{n}{2}$.",
  "U05-A-index-from-coeff", "Forming and solving a quadratic in $n$.",
  check=_c35, values=[21, 36, 15, 20], cognitive="Application")

# ================================================================ DIFFICULT (12)

q("U05-A-036", T_PROD, "Binomial times binomial in 1/x", "Difficult", "Multi-step computation MCQ",
  r"The coefficient of $\frac{1}{x}$ in the expansion of $(1 - x)(1 + x)^8\left(1 + \frac{1}{x}\right)^8$ is",
  r"$3432$",
  [(r"$11440$", r"Rewrites as $\frac{(1 - x)(1 + x)^{16}}{x^8}$ but ignores the $-x$ term, taking only $\binom{16}{7}$."),
   (r"$19448$", r"Sign slip: treats $(1 - x)$ as $(1 + x)$, giving $\binom{16}{7} + \binom{16}{6}$."),
   (r"$-1430$", r"Pairs $-x$ with $x^8$ in place of $x^6$ in $(1 + x)^{16}$, giving $\binom{16}{7} - \binom{16}{8}$.")],
  r"$\left(1 + \frac{1}{x}\right)^8 = \frac{(1 + x)^8}{x^8}$, so the expression is $\frac{(1 - x)(1 + x)^{16}}{x^8}$. The coefficient of $x^{-1}$ is the coefficient of $x^7$ in $(1 - x)(1 + x)^{16}$, namely $\binom{16}{7} - \binom{16}{6} = 11440 - 8008 = 3432$.",
  r"Not accounting for the shift by $x^{-8}$ when pairing the extra factor.",
  "U05-A-product-reciprocal-binomials", "Non-obvious rewriting, an index shift by $x^{-8}$, and a second pairing with the extra factor $(1 - x)$ where the shift is easily misapplied.",
  check=lambda: cx((1 - x)*(1 + x)**8*(1 + 1/x)**8, -1), values=[3432, 11440, 19448, -1430], cognitive="Analysis",
  numerical=dict(question=r"The coefficient of $\frac{1}{x}$ in the expansion of $(1 - x)(1 + x)^8\left(1 + \frac{1}{x}\right)^8$ is", answer=3432))

q("U05-A-037", T_PROD, "Term independent of x in a product", "Difficult", "Multi-step computation MCQ",
  r"The term independent of $x$ in the expansion of $(1 + x^2)^4\left(x - \frac{1}{x}\right)^6$ is",
  r"$8$",
  [(r"$-20$", r"Uses only the constant term $-\binom{6}{3}$ of the second factor."),
   (r"$120$", r"Takes every contribution as positive: $20 + 60 + 36 + 4$."),
   (r"$4$", r"Misses the pairing $4x^6 \cdot x^{-6}$, adding only $-20 + 60 - 36$.")],
  r"Write $\left(x - \frac{1}{x}\right)^6 = \frac{(x^2 - 1)^6}{x^6}$; the required term is the coefficient of $x^6$ in $(1 + x^2)^4(x^2 - 1)^6 = (x^4 - 1)^4(x^2 - 1)^2$. With $y = x^2$, this is the coefficient of $y^3$ in $(y^2 - 1)^4(y - 1)^2$, namely $(-4y^2)(-2y)$, i.e. $8$. Directly: $-20 + 4 \cdot 15 + 6 \cdot (-6) + 4 \cdot 1 = 8$.",
  "Missing pairings or signs when several terms contribute.",
  "U05-A-product-indep-term", "Four contributions with alternating signs, or a clever regrouping.",
  check=lambda: cx((1 + x**2)**4*(x - 1/x)**6, 0), values=[8, -20, 120, 4], cognitive="Analysis")

q("U05-A-038", T_PROD, "Polynomial times binomial with a trap", "Difficult", "Multi-step computation MCQ",
  r"The term independent of $x$ in the expansion of $(1 + x + 2x^3)\left(x^2 - \frac{1}{x}\right)^9$ is",
  r"$12$",
  [(r"$84$", r"Uses only the constant term of the binomial, ignoring the $2x^3$ term."),
   (r"$156$", r"Takes the $x^{-3}$ coefficient as $+36$, a sign slip with $(-1)^7$."),
   (r"$48$", r"Uses $x^3$ in place of $2x^3$: $84 - 36$.")],
  r"In $\left(x^2 - \frac{1}{x}\right)^9$, $T_{r+1} = \binom{9}{r}(-1)^r x^{18 - 3r}$, so only powers that are multiples of $3$ occur. The constant needs $x^0$ ($r = 6$, coefficient $84$), $x^{-1}$ (impossible) and $x^{-3}$ ($r = 7$, coefficient $-36$). Hence the term is $84 + 2(-36) = 12$.",
  "Assuming every term of the polynomial factor contributes.",
  "U05-A-product-polynomial-indep", "Three candidate pairings, one impossible, with a sign.",
  check=lambda: cx((1 + x + 2*x**3)*(x**2 - 1/x)**9, 0), values=[12, 84, 156, 48], cognitive="Analysis")

def _c39():
    e = expand((sqrt(2) + 3**Rational(1, 4))**8)
    return sum(t for t in Add.make_args(e) if t.is_rational)
q("U05-A-039", T_RAT, "Sum of the rational terms", "Difficult", "Multi-step computation MCQ",
  r"The sum of all the rational terms in the expansion of $\left(\sqrt{2} + \sqrt[4]{3}\right)^8$ is",
  r"$865$",
  [(r"$25$", r"Keeps only the end terms $16$ and $9$, missing $r = 4$."),
   (r"$235$", r"For $r = 4$ forgets the factor $(\sqrt{2})^4 = 4$: $16 + 70 \cdot 3 + 9$."),
   (r"$445$", r"For $r = 4$ takes $(\sqrt{2})^4$ as $2$: $16 + 70 \cdot 2 \cdot 3 + 9$.")],
  r"$T_{r+1} = \binom{8}{r}2^{\frac{8-r}{2}}3^{\frac{r}{4}}$ is rational iff $4 \mid r$: $r = 0, 4, 8$. These give $2^4 = 16$, $\binom{8}{4} \cdot 2^2 \cdot 3 = 840$ and $3^2 = 9$. The sum is $865$.",
  "Missing interior rational terms or mis-evaluating powers of surds.",
  "U05-A-rational-terms-sum", "Find the admissible $r$, then evaluate three terms exactly.",
  check=_c39, values=[865, 25, 235, 445], cognitive="Application",
  numerical=dict(question=r"The sum of all the rational terms in the expansion of $\left(\sqrt{2} + \sqrt[4]{3}\right)^8$ is", answer=865))

def _c40():
    s1 = rat_count(2, 2, 3, 5, 20) == 3
    rs = [r for r in range(20) if binomial(20, r + 1) == 2*binomial(20, r)]
    s2 = rs == [6] and binomial(20, 7) == 2*binomial(20, 6)
    return (s1, s2)
q("U05-A-040", T_RAT, "Rational terms and ratio of coefficients", "Difficult", "Statement-based MCQ",
  r"Statement I: The expansion of $\left(\sqrt{2} + \sqrt[5]{3}\right)^{20}$ has exactly $3$ rational terms. Statement II: If the coefficients of $x^r$ and $x^{r+1}$ in the expansion of $(1 + x)^{20}$ are in the ratio $1 : 2$, then $r = 6$." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Uses $\frac{n - r + 1}{r}$ for $\frac{\binom{20}{r+1}}{\binom{20}{r}}$, so $21 - r = 2r$, $r = 7$, and rejects Statement II."),
   (ST_FT, r"Counts $5$ rational terms by requiring only $5 \mid r$."),
   (ST_FF, r"Requires only $5 \mid r$, counting $5$ rational terms ($r = 0, 5, 10, 15, 20$), and also uses $\frac{n - r + 1}{r}$ for $\frac{\binom{20}{r+1}}{\binom{20}{r}}$, getting $21 - r = 2r$, $r = 7$; so rejects both statements.")],
  r"Statement I: $T_{r+1} = \binom{20}{r}2^{\frac{20-r}{2}}3^{\frac{r}{5}}$ is rational iff $5 \mid r$ and $r$ is even, i.e. $r = 0, 10, 20$: exactly $3$ terms, true. Statement II: $\frac{\binom{20}{r+1}}{\binom{20}{r}} = \frac{20 - r}{r + 1} = 2$ gives $20 - r = 2r + 2$, $r = 6$; indeed $\binom{20}{7} = 77520 = 2 \cdot 38760 = 2\binom{20}{6}$. True.",
  "Imposing one condition only, or misapplying the ratio of consecutive coefficients.",
  "U05-A-statement-rational-ratio", "Two separate multi-step verifications, each with a standard trap.",
  check=_c40, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Analysis")

q("U05-A-041", T_PROD, "Factorising into binomials", "Difficult", "Multi-step computation MCQ",
  r"The coefficient of $x^5$ in the expansion of $(1 + x + x^2 + x^3)^4$ is",
  r"$40$",
  [(r"$16$", r"Uses only $x^3 \cdot x^2$, i.e. $\binom{4}{3}\binom{4}{1}$, missing $\binom{4}{1}\binom{4}{2}$."),
   (r"$24$", r"Uses only $x \cdot x^4$, i.e. $\binom{4}{1}\binom{4}{2}$, missing $\binom{4}{3}\binom{4}{1}$."),
   (r"$56$", r"Treats the base as $(1 + x)^2$ and takes $\binom{8}{5}$.")],
  r"$1 + x + x^2 + x^3 = (1 + x)(1 + x^2)$, so the expression is $(1 + x)^4(1 + x^2)^4$. The $x^5$ coefficient is $\sum \binom{4}{i}\binom{4}{j}$ over $i + 2j = 5$: $(i, j) = (3, 1), (1, 2)$, giving $4 \cdot 4 + 4 \cdot 6 = 40$.",
  "Missing one solution of $i + 2j = 5$.",
  "U05-A-factorised-product", "Factorisation into two binomials plus casework.",
  check=lambda: cx((1 + x + x**2 + x**3)**4, 5), values=[40, 16, 24, 56], cognitive="Analysis",
  numerical=dict(question=r"The coefficient of $x^5$ in the expansion of $(1 + x + x^2 + x^3)^4$ is", answer=40))

def _c42():
    for n in range(1, 200):
        if rat_count(2, 2, 3, 4, n) == 11:
            return n
q("U05-A-042", T_RAT, "Index from the number of integral terms", "Difficult", "Inverse/parameter MCQ",
  r"The least positive integer $n$ for which the expansion of $\left(\sqrt{2} + \sqrt[4]{3}\right)^n$ has exactly $11$ integral terms is",
  r"$40$",
  [(r"$44$", r"Sets $\frac{n}{4} = 11$, forgetting $r = 0$."),
   (r"$20$", r"Only requires $\frac{n - r}{2}$ integral: $\frac{n}{2} + 1 = 11$."),
   (r"$42$", r"Gives the largest such $n$ ($n = 42$ also has $11$ integral terms).")],
  r"$T_{r+1} = \binom{n}{r}2^{\frac{n-r}{2}}3^{\frac{r}{4}}$ is an integer iff $4 \mid r$ and $n - r$ is even; this needs $n$ even, and then the count is $\left\lfloor \frac{n}{4} \right\rfloor + 1$. Setting this to $11$ gives $n \in \{40, 42\}$, and the least is $40$.",
  "Off-by-one in counting, or ignoring the parity of $n$.",
  "U05-A-integral-terms-inverse", "Counting argument with parity casework, then minimisation.",
  check=_c42, values=[40, 44, 20, 42], cognitive="Analysis",
  numerical=dict(question=r"The least positive integer $n$ for which the expansion of $\left(\sqrt{2} + \sqrt[4]{3}\right)^n$ has exactly $11$ integral terms is", answer=40))

def _c43():
    n = symbols('n', positive=True, integer=True)
    c = [1, Rational(1, 2)*n, Rational(1, 4)*n*(n - 1)/2]
    ns = [v for v in solve(Eq(2*c[1], c[0] + c[2]), n) if v >= 2]
    N = ns[0]
    return sum(1 for r in range(N + 1) if Rational(N - r, 2) - Rational(r, 3) == int(Rational(N - r, 2) - Rational(r, 3)))
q("U05-A-043", T_RAT, "AP condition then integral powers", "Difficult", "Multi-step computation MCQ",
  r"In the expansion of $\left(\sqrt{x} + \frac{1}{2\sqrt[3]{x}}\right)^n$, $x > 0$, $n \ge 2$, the coefficients of the first three terms are in arithmetic progression. The number of terms in which $x$ has an integral exponent is",
  r"$2$",
  [(r"$3$", r"Only requires $\frac{r}{3}$ to be an integer ($r = 0, 3, 6$)."),
   (r"$5$", r"Only requires $\frac{8 - r}{2}$ to be an integer ($r$ even)."),
   (r"$1$", r"Counts only the term with a positive integral exponent, missing $x^{-1}$.")],
  r"The coefficients are $1$, $\frac{n}{2}$, $\frac{n(n-1)}{8}$. The AP condition $n = 1 + \frac{n(n-1)}{8}$ gives $n^2 - 9n + 8 = 0$, so $n = 8$ ($n = 1$ is rejected). Then the exponent in $T_{r+1}$ is $\frac{8 - r}{2} - \frac{r}{3} = \frac{24 - 5r}{6}$, an integer iff $6 \mid r$: $r = 0, 6$ (powers $4$ and $-1$). So $2$ terms.",
  "Imposing integrality on each part separately in place of the combined exponent.",
  "U05-A-ap-then-integral-powers", "AP condition to find $n$, then a congruence on $r$.",
  check=_c43, values=[2, 3, 5, 1], cognitive="Analysis")

q("U05-A-044", T_PROD, "Trinomial that factors into binomials", "Difficult", "Multi-step computation MCQ",
  r"The coefficient of $x^3$ in the expansion of $(1 + x - 2x^2)^6$ is",
  r"$-40$",
  [(r"$40$", r"Factorises $1 + x - 2x^2$ as $(1 + x)(1 - 2x)$."),
   (r"$140$", r"Uses only $x^3 \cdot 1$ and $1 \cdot x^3$ from $(1 - x)^6(1 + 2x)^6$: $-20 + 160$."),
   (r"$680$", r"Sign slip on the pairing $(-6x)(60x^2)$, adding $360$.")],
  r"$1 + x - 2x^2 = (1 - x)(1 + 2x)$. With $(1 - x)^6 = 1 - 6x + 15x^2 - 20x^3 + \dots$ and $(1 + 2x)^6 = 1 + 12x + 60x^2 + 160x^3 + \dots$, the $x^3$ coefficient is $-20 + 15 \cdot 12 + (-6)(60) + 160 = -40$.",
  "Wrong factorisation or missing the middle pairings.",
  "U05-A-factor-quadratic-product", "Factorisation, two expansions and four pairings with signs.",
  check=lambda: cx((1 + x - 2*x**2)**6, 3), values=[-40, 40, 140, 680], cognitive="Analysis")

def _c45():
    m, n = symbols('m n', positive=True, integer=True)
    e = expand_func(binomial(m, 2) - m*n + binomial(n, 2))
    s = solve([Eq(m - n, 4), Eq(e, -2)], [m, n], dict=True)
    return s[0][m]
q("U05-A-045", T_PROD, "Unknown indices from two coefficients", "Difficult", "Inverse/parameter MCQ",
  r"If the coefficients of $x$ and $x^2$ in the expansion of $(1 + x)^m(1 - x)^n$ are $4$ and $-2$ respectively, where $m, n \in \mathbb{N}$, then $m$ equals",
  r"$12$",
  [(r"$11$", r"Forgets the factor $\frac{1}{2}$: $(m - n)^2 - (m + n) = -2$ gives $m + n = 18$."),
   (r"$8$", r"Solves correctly but reports $n$."),
   (r"$20$", r"Reports $m + n$.")],
  r"Coefficient of $x$: $m - n = 4$. Coefficient of $x^2$: $\binom{m}{2} - mn + \binom{n}{2} = \frac{(m - n)^2 - (m + n)}{2} = -2$, so $16 - (m + n) = -4$, $m + n = 20$. Hence $m = 12$, $n = 8$.",
  "Mishandling the symmetric expression for the $x^2$ coefficient.",
  "U05-A-product-unknown-exponents", "Two coefficient equations, a symmetric-function rewrite and a linear system.",
  check=_c45, values=[12, 11, 8, 20], cognitive="Analysis",
  numerical=dict(question=r"If the coefficients of $x$ and $x^2$ in the expansion of $(1 + x)^m(1 - x)^n$ are $4$ and $-2$ respectively, where $m, n \in \mathbb{N}$, then the value of $m$ is", answer=12))

def _c46():
    good = [n for n in range(1, 16) if any(4*(n - r) - 3*r == 0 for r in range(n + 1))]
    return sum(good)
q("U05-A-046", T_GEN, "All indices admitting a constant term", "Difficult", "Conceptual/application MCQ",
  r"The sum of all $n \in \{1, 2, \dots, 15\}$ for which the expansion of $\left(x^4 - \frac{1}{x^3}\right)^n$ has a term independent of $x$ is",
  r"$21$",
  [(r"$7$", r"Finds only the least such $n$."),
   (r"$12$", r"Takes $n$ to be a multiple of $4 \cdot 3 = 12$."),
   (r"$45$", r"Takes $n$ to be a multiple of $3$: $3 + 6 + 9 + 12 + 15$.")],
  r"The power in $T_{r+1}$ is $4(n - r) - 3r = 4n - 7r$, which is $0$ iff $r = \frac{4n}{7}$ is an integer, i.e. $7 \mid n$. In the range, $n = 7, 14$, with sum $21$.",
  "Using the product or one exponent in place of the sum of exponents.",
  "U05-A-indep-term-existence", "Divisibility condition from the exponent equation, then enumeration.",
  check=_c46, values=[21, 7, 12, 45], cognitive="Analysis",
  numerical=dict(question=r"The sum of all $n \in \{1, 2, \dots, 15\}$ for which the expansion of $\left(x^4 - \frac{1}{x^3}\right)^n$ has a term independent of $x$ is", answer=21))

q("U05-A-047", T_PROD, "Quadratic times binomial", "Difficult", "Multi-step computation MCQ",
  r"The coefficient of $x^5$ in the expansion of $(1 + 2x + 3x^2)(1 - x)^{10}$ is",
  r"$-192$",
  [(r"$168$", r"Ignores the $3x^2$ term: $-252 + 420$."),
   (r"$528$", r"Takes the $x^3$ coefficient of $(1 - x)^{10}$ as $+120$."),
   (r"$1032$", r"Treats every coefficient of $(1 - x)^{10}$ as positive.")],
  r"The $x^5$ coefficient is $\binom{10}{5}(-1)^5 + 2\binom{10}{4}(-1)^4 + 3\binom{10}{3}(-1)^3 = -252 + 420 - 360 = -192$.",
  "Losing the alternating signs of $(1 - x)^n$.",
  "U05-A-product-polynomial-coeff", "Three contributions with alternating signs.",
  check=lambda: cx((1 + 2*x + 3*x**2)*(1 - x)**10, 5), values=[-192, 168, 528, 1032], cognitive="Application")
