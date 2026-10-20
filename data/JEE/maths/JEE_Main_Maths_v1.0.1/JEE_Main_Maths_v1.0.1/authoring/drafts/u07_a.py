import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from sympy.calculus.util import function_range, continuous_domain
import random as _random

# ---------------------------------------------------------------- helpers
X = Symbol('x', real=True)
Y = Symbol('y', real=True)


def dom(f):
    return continuous_domain(f, X, S.Reals)


def simp_set(S_):
    if isinstance(S_, Interval):
        return Interval(nsimplify(simplify(S_.left)), nsimplify(simplify(S_.right)), S_.left_open, S_.right_open)
    if isinstance(S_, Union):
        return Union(*[simp_set(a) for a in S_.args])
    return S_


def rng(f, D=S.Reals):
    return simp_set(function_range(f, X, D))


def ints_in(S_, lo=-60, hi=60):
    return sum(1 for n in range(lo, hi + 1) if S_.contains(n) == True)


def _isper(f, T):
    r = _random.Random(3)
    for _ in range(8):
        a = Rational(r.randint(-997, 997), r.randint(101, 211)) + sqrt(2) / 7
        if abs(N(f.subs(X, a + T) - f.subs(X, a), 30)) > 1e-18:
            return False
    return True


def min_period(f, T0, kmax=24):
    """Smallest period of the form T0/k, after confirming T0 is a period."""
    T0 = sympify(T0)
    assert _isper(f, T0)
    best = T0
    for k in range(2, kmax + 1):
        if _isper(f, T0 / k) and (T0 / k) < best:
            best = T0 / k
    return best


def parity(f, pts=None):
    """2 = even and odd, 1 = even only, -1 = odd only, 0 = neither."""
    pts = pts or [Rational(k, 7) + sqrt(3) / 11 for k in (1, 3, 5, 9, 13)]
    ev = all(abs(N(f.subs(X, -p) - f.subs(X, p), 30)) < 1e-18 for p in pts)
    od = all(abs(N(f.subs(X, -p) + f.subs(X, p), 30)) < 1e-18 for p in pts)
    return 2 if (ev and od) else 1 if ev else -1 if od else 0


def abs_range(f, D=S.Reals):
    """Range of an expression built from |linear| pieces, piece by piece."""
    bps = sorted({r for a in f.atoms(Abs) for r in solve(a.args[0], X)}, key=lambda r: float(r))
    edges = [-oo] + bps + [oo]
    out = S.EmptySet
    for lo, hi in zip(edges[:-1], edges[1:]):
        I_ = Interval(lo, hi).intersect(D)
        if I_ is S.EmptySet:
            continue
        if lo == -oo and hi == oo:
            mid = 0
        elif lo == -oo:
            mid = hi - 1
        elif hi == oo:
            mid = lo + 1
        else:
            mid = (lo + hi) / 2
        g = f.replace(lambda e: isinstance(e, Abs), lambda e: e.args[0] * sign(e.args[0].subs(X, mid)))
        out = Union(out, function_range(g, X, I_))
    return out


def pre_inc(I_, ginv):
    """Preimage of an interval under an increasing map, given its inverse."""
    return Interval(ginv(I_.left), ginv(I_.right), I_.left_open, I_.right_open)


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."
T_DOM = "Domain of real functions"
T_RNG = "Range of real functions"
T_INV = "Inverse and composite functions"
T_PAR = "Even, odd and periodic functions"
T_GRF = "Graphs of modulus, greatest integer and signum functions"

# ================================================================ CLASS XI: EASY (9)

q("U07-A-001", T_DOM, "Square root of a rational expression", "Easy", "Single-step computation MCQ",
  r"The domain of the real function $f(x) = \sqrt{\frac{x-2}{x+3}}$ is",
  r"$(-\infty, -3) \cup [2, \infty)$",
  [(r"$(-\infty, -3] \cup [2, \infty)$", r"Allows $x = -3$, where the denominator $x + 3$ vanishes."),
   (r"$(-3, 2]$", r"Reverses the sign chart and takes the region where $\frac{x-2}{x+3} \le 0$."),
   (r"$[2, \infty)$", r"Imposes only $x - 2 \ge 0$ and $x + 3 > 0$, missing the case where both factors are negative.")],
  r"We need $\frac{x-2}{x+3} \ge 0$ with $x \ne -3$. The critical points are $-3$ and $2$; the quotient is non-negative for $x < -3$ and for $x \ge 2$. Hence the domain is $(-\infty, -3) \cup [2, \infty)$.",
  r"Including the zero of the denominator, or ignoring the case where numerator and denominator are both negative.",
  "U07-A-dom-root-rational", "One sign-chart with an excluded endpoint.",
  check=lambda: dom(sqrt((X - 2) / (X + 3))),
  values=[Union(Interval.open(-oo, -3), Interval(2, oo)), Union(Interval(-oo, -3), Interval(2, oo)),
          Interval.Lopen(-3, 2), Interval(2, oo)], cognitive="Application")

q("U07-A-002", T_DOM, "Logarithm in a denominator", "Easy", "Multi-step computation MCQ",
  r"The domain of $f(x) = \frac{1}{\log_{10}(3 - x)} + \sqrt{x + 2}$ is",
  r"$[-2, 2) \cup (2, 3)$",
  [(r"$[-2, 3)$", r"Uses $3 - x > 0$ and $x + 2 \ge 0$ but ignores $\log_{10}(3-x) \ne 0$, so keeps $x = 2$."),
   (r"$[-2, 2)$", r"Requires $\log_{10}(3 - x) > 0$, as if a logarithm in the denominator had to be positive."),
   (r"$(-2, 2) \cup (2, 3)$", r"Demands $x + 2 > 0$, excluding $x = -2$ where $\sqrt{x+2} = 0$ is defined.")],
  r"We need $3 - x > 0$, $\log_{10}(3 - x) \ne 0$ (that is $3 - x \ne 1$, so $x \ne 2$) and $x + 2 \ge 0$. Together: $-2 \le x < 3$, $x \ne 2$, giving $[-2, 2) \cup (2, 3)$.",
  r"Forgetting that a logarithm in the denominator must be non-zero.",
  "U07-A-dom-log-denominator", "Three simple conditions combined.",
  check=lambda: dom(1 / log(3 - X, 10) + sqrt(X + 2)),
  values=[Union(Interval.Ropen(-2, 2), Interval.open(2, 3)), Interval.Ropen(-2, 3), Interval.Ropen(-2, 2),
          Union(Interval.open(-2, 2), Interval.open(2, 3))], cognitive="Application")

q("U07-A-003", T_RNG, "Range of a rational function", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = \frac{x^2}{1 + x^2}$, $x \in \mathbb{R}$, is",
  r"$[0, 1)$",
  [(r"$[0, 1]$", r"Assumes the value $1$ is attained, although $\frac{1}{1+x^2}$ never becomes $0$."),
   (r"$(0, 1)$", r"Excludes $0$, overlooking $f(0) = 0$."),
   (r"$[0, \infty)$", r"Treats the function like $x^2$, ignoring that the denominator grows as fast as the numerator.")],
  r"Write $f(x) = 1 - \frac{1}{1 + x^2}$. Since $1 + x^2 \ge 1$, we have $0 < \frac{1}{1+x^2} \le 1$, so $0 \le f(x) < 1$. The value $0$ occurs at $x = 0$ and values near $1$ occur for large $|x|$, so the range is $[0, 1)$.",
  r"Treating a horizontal asymptote value as attained.",
  "U07-A-rng-rational-asymptote", "One rewriting, then a bound.",
  check=lambda: rng(X**2 / (1 + X**2)),
  values=[Interval.Ropen(0, 1), Interval(0, 1), Interval.open(0, 1), Interval(0, oo)], cognitive="Understanding")

q("U07-A-004", T_RNG, "Range of a sinusoidal expression", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = 3\sin x - 4\cos x + 2$, $x \in \mathbb{R}$, is",
  r"$[-3, 7]$",
  [(r"$[-5, 5]$", r"Finds the range of $3\sin x - 4\cos x$ but drops the constant $+2$."),
   (r"$[-5, 9]$", r"Takes $|3| + |4| = 7$ as the amplitude in place of $\sqrt{3^2 + 4^2} = 5$."),
   (r"$[-7, 3]$", r"Shifts the interval $[-5, 5]$ by $-2$ in place of $+2$.")],
  r"$3\sin x - 4\cos x$ has amplitude $\sqrt{9 + 16} = 5$, so it takes every value in $[-5, 5]$. Adding $2$ gives the range $[-3, 7]$.",
  r"Using $|a| + |b|$ as the amplitude of $a\sin x + b\cos x$.",
  "U07-A-rng-asin-bcos", "Direct use of the amplitude $\\sqrt{a^2+b^2}$.",
  check=lambda: rng(3 * sin(X) - 4 * cos(X) + 2),
  values=[Interval(-3, 7), Interval(-5, 5), Interval(-5, 9), Interval(-7, 3)], cognitive="Application")

q("U07-A-005", T_DOM, "Two square roots", "Easy", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{4 - x^2} + \frac{1}{\sqrt{x^2 - 1}}$ is",
  r"$[-2, -1) \cup (1, 2]$",
  [(r"$[-2, -1] \cup [1, 2]$", r"Allows $x^2 - 1 = 0$, although that root sits in the denominator."),
   (r"$(-2, -1) \cup (1, 2)$", r"Also excludes $x = \pm 2$, treating $\sqrt{4 - x^2}$ as if it needed a positive radicand."),
   (r"$[-2, 2] \setminus \{-1, 1\}$", r"Removes only the zeros of the denominator and ignores that $x^2 - 1$ must be positive.")],
  r"We need $4 - x^2 \ge 0$, so $-2 \le x \le 2$, and $x^2 - 1 > 0$, so $|x| > 1$. The intersection is $[-2, -1) \cup (1, 2]$.",
  r"Treating a square root in the denominator like one in the numerator.",
  "U07-A-dom-two-roots", "Two quadratic inequalities intersected.",
  check=lambda: dom(sqrt(4 - X**2) + 1 / sqrt(X**2 - 1)),
  values=[Union(Interval.Ropen(-2, -1), Interval.Lopen(1, 2)), Union(Interval(-2, -1), Interval(1, 2)),
          Union(Interval.open(-2, -1), Interval.open(1, 2)), Interval(-2, 2) - FiniteSet(-1, 1)],
  cognitive="Application")

q("U07-A-006", T_RNG, "Logarithm of a quadratic", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = \log_2(x^2 - 2x + 5)$, $x \in \mathbb{R}$, is",
  r"$[2, \infty)$",
  [(r"$[\log_2 5, \infty)$", r"Uses the value of the quadratic at $x = 0$ as its minimum, in place of the vertex value $4$."),
   (r"$(-\infty, \infty)$", r"Assumes a logarithm always takes every real value, ignoring that its argument is at least $4$."),
   (r"$(2, \infty)$", r"Excludes $2$, though $f(1) = \log_2 4 = 2$.")],
  r"$x^2 - 2x + 5 = (x - 1)^2 + 4$ takes every value in $[4, \infty)$. Since $\log_2$ is increasing, $f$ takes every value in $[\log_2 4, \infty) = [2, \infty)$.",
  r"Not using the minimum of the inner quadratic.",
  "U07-A-rng-log-quadratic", "Completing the square, then monotonicity of log.",
  check=lambda: rng(log(X**2 - 2 * X + 5, 2)),
  values=[Interval(2, oo), Interval(log(5, 2), oo), S.Reals, Interval.open(2, oo)], cognitive="Application")

q("U07-A-007", T_DOM, "Variable base of a logarithm", "Easy", "Multi-step computation MCQ",
  r"The domain of $f(x) = \log_{x}(9 - x^2)$ is",
  r"$(0, 1) \cup (1, 3)$",
  [(r"$(0, 3)$", r"Ignores that the base of a logarithm cannot equal $1$."),
   (r"$(-3, 1) \cup (1, 3)$", r"Ignores that the base must be positive, using only $9 - x^2 > 0$ and $x \ne 1$."),
   (r"$(1, 3)$", r"Assumes the base must exceed $1$.")],
  r"We need base $x > 0$, $x \ne 1$, and argument $9 - x^2 > 0$, so $-3 < x < 3$. Together: $(0, 1) \cup (1, 3)$.",
  r"Forgetting one of the base conditions $x > 0$, $x \ne 1$.",
  "U07-A-dom-log-variable-base", "Three standard conditions on a logarithm.",
  check=lambda: dom(log(9 - X**2) / log(X)),
  values=[Union(Interval.open(0, 1), Interval.open(1, 3)), Interval.open(0, 3),
          Union(Interval.open(-3, 1), Interval.open(1, 3)), Interval.open(1, 3)], cognitive="Recall")

q("U07-A-008", T_RNG, "Rational function with a removable factor", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = \frac{x^2 - 4}{x - 2}$, $x \ne 2$, is",
  r"$\mathbb{R} \setminus \{4\}$",
  [(r"$\mathbb{R} \setminus \{2\}$", r"Excludes the point missing from the domain, $x = 2$, in place of the missing output $f$-value."),
   (r"$\mathbb{R}$", r"Cancels to $x + 2$ and forgets that $x = 2$ is not allowed."),
   (r"$\mathbb{R} \setminus \{0\}$", r"Factors $x^2 - 4$ as $(x - 2)^2$, cancels to $x - 2$, and removes the value $0$.")],
  r"For $x \ne 2$, $f(x) = x + 2$, which takes every real value except $2 + 2 = 4$. So the range is $\mathbb{R} \setminus \{4\}$.",
  r"Confusing the excluded input with the excluded output.",
  "U07-A-rng-hole", "One cancellation and one excluded value.",
  check=lambda: rng((X**2 - 4) / (X - 2), dom((X**2 - 4) / (X - 2))),
  values=[S.Reals - FiniteSet(4), S.Reals - FiniteSet(2), S.Reals, S.Reals - FiniteSet(0)], cognitive="Understanding")

q("U07-A-009", T_RNG, "Quadratic on a closed interval", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = x^2 - 4x + 7$ on the domain $[0, 5]$ is",
  r"$[3, 12]$",
  [(r"$[7, 12]$", r"Uses only the end-point values $f(0) = 7$ and $f(5) = 12$, missing the vertex at $x = 2$."),
   (r"$[3, \infty)$", r"Ignores the restriction to $[0, 5]$."),
   (r"$[3, 7]$", r"Compares the vertex value only with $f(0)$, forgetting the other end $x = 5$.")],
  r"$f(x) = (x - 2)^2 + 3$. On $[0, 5]$ the minimum is $f(2) = 3$; the maximum is at the farther end, $f(5) = 12$ (while $f(0) = 7$). By continuity the range is $[3, 12]$.",
  r"Evaluating only at the end points of the interval.",
  "U07-A-rng-quadratic-interval", "Vertex plus end-point comparison.",
  check=lambda: rng(X**2 - 4 * X + 7, Interval(0, 5)),
  values=[Interval(3, 12), Interval(7, 12), Interval(3, oo), Interval(3, 7)], cognitive="Application")

# ================================================================ CLASS XI: MEDIUM (12)

q("U07-A-010", T_DOM, "Root of a logarithm with base below 1", "Medium", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{\log_{1/2}(x - 1)}$ is",
  r"$(1, 2]$",
  [(r"$[2, \infty)$", r"Treats the base $\frac{1}{2}$ like a base greater than $1$ and solves $x - 1 \ge 1$."),
   (r"$(1, \infty)$", r"Uses only $x - 1 > 0$, forgetting that the logarithm itself must be non-negative."),
   (r"$(1, 2)$", r"Requires $\log_{1/2}(x-1) > 0$, excluding $x = 2$ where the root is $0$.")],
  r"We need $x - 1 > 0$ and $\log_{1/2}(x - 1) \ge 0$. Because the base is less than $1$, the second condition means $x - 1 \le 1$. So $1 < x \le 2$.",
  r"Not reversing the inequality for a logarithm with base between $0$ and $1$.",
  "U07-A-dom-log-small-base", "Two conditions; the trap is the decreasing logarithm.",
  check=lambda: dom(sqrt(log(X - 1) / log(Rational(1, 2)))),
  values=[Interval.Lopen(1, 2), Interval(2, oo), Interval.open(1, oo), Interval.open(1, 2)], cognitive="Application")

q("U07-A-011", T_DOM, "Exponential quotient under a root", "Medium", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{\frac{1 - 5^{x}}{7^{-x} - 7}}$ is",
  r"$(-\infty, -1) \cup [0, \infty)$",
  [(r"$(-\infty, -1] \cup [0, \infty)$", r"Keeps $x = -1$, where the denominator $7^{-x} - 7$ is zero."),
   (r"$(-1, 0]$", r"Reverses the sign analysis and takes the region where the quotient is non-positive."),
   (r"$(-\infty, 0]$", r"Imposes only $1 - 5^{x} \ge 0$, treating the denominator as positive throughout.")],
  r"$1 - 5^{x} \ge 0 \iff x \le 0$ and $7^{-x} - 7 > 0 \iff -x > 1 \iff x < -1$. The quotient is $\ge 0$ when both parts are non-negative with positive denominator ($x < -1$) or both non-positive with negative denominator ($x \ge 0$; at $x = 0$ the numerator is $0$). So the domain is $(-\infty, -1) \cup [0, \infty)$.",
  r"Ignoring the sign of the denominator.",
  "U07-A-dom-exponential-quotient", "Sign of two exponential expressions, then a sign chart.",
  check=lambda: dom(sqrt((1 - 5**X) / (7**(-X) - 7))),
  values=[Union(Interval.open(-oo, -1), Interval(0, oo)), Union(Interval(-oo, -1), Interval(0, oo)),
          Interval.Lopen(-1, 0), Interval(-oo, 0)], cognitive="Application")

q("U07-A-012", T_RNG, "Sum of two square roots", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \sqrt{x - 1} + \sqrt{5 - x}$ is",
  r"$[2, 2\sqrt{2}]$",
  [(r"$[0, 2\sqrt{2}]$", r"Assumes the minimum is $0$ because each root can vanish, though they never vanish together."),
   (r"$[2, 4]$", r"Adds the separate maxima $2 + 2$ of the two roots, which occur at different points."),
   (r"$[0, 4]$", r"Combines both slips: minimum $0$ and maximum $2 + 2$.")],
  r"The domain is $[1, 5]$ and $f \ge 0$. Squaring, $f^2 = 4 + 2\sqrt{(x-1)(5-x)}$. On $[1, 5]$, $(x-1)(5-x) = 4 - (x-3)^2$ takes every value in $[0, 4]$, so $f^2 \in [4, 8]$ and $f \in [2, 2\sqrt{2}]$.",
  r"Adding the individual extremes of two terms that peak at different points.",
  "U07-A-rng-sum-of-roots", "Domain, squaring and bounding a product.",
  check=lambda: rng(sqrt(X - 1) + sqrt(5 - X), dom(sqrt(X - 1) + sqrt(5 - X))),
  values=[Interval(2, 2 * sqrt(2)), Interval(0, 2 * sqrt(2)), Interval(2, 4), Interval(0, 4)], cognitive="Analysis")

q("U07-A-013", T_RNG, "Quotient of quadratics by discriminant", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{x^2 + x + 1}{x^2 - x + 1}$, $x \in \mathbb{R}$, is",
  r"$\left[\frac{1}{3}, 3\right]$",
  [(r"$\left[\frac{1}{3}, 3\right] \setminus \{1\}$", r"Excludes $y = 1$ because the leading coefficient $y - 1$ vanishes, although then $-2x = 0$ gives $x = 0$."),
   (r"$\left(\frac{1}{3}, 3\right)$", r"Uses a strict discriminant inequality, missing $x = \pm 1$ where the extremes occur."),
   (r"$[1, 3]$", r"Considers only $x \ge 0$, so takes $f(0) = 1$ as the minimum.")],
  r"Set $y = f(x)$: $(y - 1)x^2 - (y + 1)x + (y - 1) = 0$. For $y \ne 1$, real $x$ needs $(y+1)^2 - 4(y-1)^2 \ge 0$, i.e. $(3 - y)(3y - 1) \ge 0$, so $\frac{1}{3} \le y \le 3$. For $y = 1$, $x = 0$ works. Hence the range is $\left[\frac{1}{3}, 3\right]$.",
  r"Discarding the value of $y$ that makes the leading coefficient zero.",
  "U07-A-rng-discriminant", "Discriminant method with a degenerate case.",
  check=lambda: rng((X**2 + X + 1) / (X**2 - X + 1)),
  values=[Interval(Rational(1, 3), 3), Interval(Rational(1, 3), 3) - FiniteSet(1),
          Interval.open(Rational(1, 3), 3), Interval(1, 3)], cognitive="Application")

q("U07-A-014", T_DOM, "Modulus in a rational expression under a root", "Medium", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{\frac{4 - |x|}{x - 1}}$ is",
  r"$(-\infty, -4] \cup (1, 4]$",
  [(r"$(1, 4]$", r"Considers only the case numerator $\ge 0$ and denominator $> 0$, missing $x \le -4$ where both are negative (equivalently, treats $|x|$ as $x$)."),
   (r"$(-\infty, -4] \cup [1, 4]$", r"Keeps $x = 1$, where the denominator $x - 1$ vanishes."),
   (r"$[-4, 1) \cup [4, \infty)$", r"Reverses the sign chart and takes the region where $\frac{4 - |x|}{x - 1} \le 0$.")],
  r"We need $\frac{4 - |x|}{x - 1} \ge 0$ with $x \ne 1$. For $x \ge 0$: $\frac{4 - x}{x - 1} \ge 0$ gives $1 < x \le 4$. For $x < 0$: $\frac{4 + x}{x - 1} \ge 0$; here $x - 1 < 0$, so we need $4 + x \le 0$, i.e. $x \le -4$. Hence the domain is $(-\infty, -4] \cup (1, 4]$.",
  r"Ignoring the case in which numerator and denominator are both negative once the modulus is opened.",
  "U07-A-dom-modulus-rational", "Casework on the sign of $x$ to open the modulus, then a sign chart in each case.",
  check=lambda: dom(sqrt((4 - Abs(X)) / (X - 1))),
  values=[Union(Interval(-oo, -4), Interval.Lopen(1, 4)), Interval.Lopen(1, 4), Union(Interval(-oo, -4), Interval(1, 4)),
          Union(Interval.Ropen(-4, 1), Interval(4, oo))], cognitive="Application")

def _c15():
    return ints_in(dom(1 / sqrt(X**2 - X - 2) + log(12 - X - X**2)))
q("U07-A-015", T_DOM, "Integers in a domain", "Medium", "Multi-step computation MCQ",
  r"The number of integers in the domain of $f(x) = \frac{1}{\sqrt{x^2 - x - 2}} + \log_e(12 - x - x^2)$ is",
  r"$2$",
  [(r"$4$", r"Uses $x^2 - x - 2 \ge 0$, keeping $x = -1$ and $x = 2$ though the root is in a denominator."),
   (r"$6$", r"Uses only $12 - x - x^2 > 0$ and ignores the square-root condition."),
   (r"$0$", r"Solves $(x - 2)(x + 1) > 0$ as $x > 2$ only, losing the branch $x < -1$; the set $(2, 3)$ then contains no integer.")],
  r"$x^2 - x - 2 = (x - 2)(x + 1) > 0$ gives $x < -1$ or $x > 2$. $12 - x - x^2 = -(x + 4)(x - 3) > 0$ gives $-4 < x < 3$. The domain is $(-4, -1) \cup (2, 3)$, whose only integers are $-3$ and $-2$. So the count is $2$.",
  r"Using non-strict inequalities where strict ones are required.",
  "U07-A-dom-integer-count", "Two quadratic inequalities, intersection, then counting.",
  check=_c15, values=[2, 4, 6, 0], cognitive="Application",
  numerical=dict(question=r"The number of integers in the domain of $f(x) = \frac{1}{\sqrt{x^2 - x - 2}} + \log_e(12 - x - x^2)$ is", answer=2))

q("U07-A-016", T_DOM, "Exponential quadratic under a root", "Medium", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{4^{x} - 3 \cdot 2^{x+1} + 8}$ is",
  r"$(-\infty, 1] \cup [2, \infty)$",
  [(r"$[1, 2]$", r"Solves $t^2 - 6t + 8 \le 0$, reversing the inequality."),
   (r"$(-\infty, 2] \cup [4, \infty)$", r"Solves for $t = 2^{x}$ but forgets to convert $t \le 2$, $t \ge 4$ back to $x$."),
   (r"$(0, 1] \cup [2, \infty)$", r"Imposes $x > 0$ from the condition $2^{x} > 0$.")],
  r"Put $t = 2^{x} > 0$: $4^{x} - 3 \cdot 2^{x+1} + 8 = t^2 - 6t + 8 = (t - 2)(t - 4) \ge 0$, so $t \le 2$ or $t \ge 4$. Thus $x \le 1$ or $x \ge 2$.",
  r"Stopping at the substitution variable instead of returning to $x$.",
  "U07-A-dom-exponential-quadratic", "Substitution, quadratic inequality, back-substitution.",
  check=lambda: dom(sqrt(4**X - 3 * 2**(X + 1) + 8)),
  values=[Union(Interval(-oo, 1), Interval(2, oo)), Interval(1, 2), Union(Interval(-oo, 2), Interval(4, oo)),
          Union(Interval.Lopen(0, 1), Interval(2, oo))], cognitive="Application")

q("U07-A-017", T_RNG, "Trigonometric range by identity", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \sin^2 x + \cos^4 x$, $x \in \mathbb{R}$, is",
  r"$\left[\frac{3}{4}, 1\right]$",
  [(r"$\left[\frac{1}{2}, 1\right]$", r"Writes $\sin^2 x\cos^2 x = \frac{1}{2}\sin^2 2x$, missing the square on $\frac{1}{2}$."),
   (r"$[0, 2]$", r"Adds the separate ranges $[0, 1]$ of $\sin^2 x$ and $\cos^4 x$."),
   (r"$\left[1, \frac{5}{4}\right]$", r"Obtains $1 + \sin^2 x\cos^2 x$ through a sign slip.")],
  r"$\cos^4 x = \cos^2 x(1 - \sin^2 x)$, so $f = \sin^2 x + \cos^2 x - \sin^2 x\cos^2 x = 1 - \frac{1}{4}\sin^2 2x$. As $\sin^2 2x \in [0, 1]$, the range is $\left[\frac{3}{4}, 1\right]$.",
  r"Adding ranges of terms that are not independent.",
  "U07-A-rng-trig-identity", "Identity reduction, then a bound.",
  check=lambda: rng(sin(X)**2 + cos(X)**4, Interval(0, 2 * pi)),
  values=[Interval(Rational(3, 4), 1), Interval(Rational(1, 2), 1), Interval(0, 2), Interval(1, Rational(5, 4))],
  cognitive="Application")


def _c18():
    return ints_in(rng(8 / (X**2 - 2 * X + 3)))
q("U07-A-018", T_RNG, "Integers in a range", "Medium", "Multi-step computation MCQ",
  r"The number of integers in the range of $f(x) = \frac{8}{x^2 - 2x + 3}$, $x \in \mathbb{R}$, is",
  r"$4$",
  [(r"$5$", r"Includes $0$, although $f(x) > 0$ for every $x$."),
   (r"$8$", r"Takes the minimum of $x^2 - 2x + 3$ as $1$ in place of $2$, getting $(0, 8]$."),
   (r"$3$", r"Excludes $4$, thinking the maximum is not attained.")],
  r"$x^2 - 2x + 3 = (x - 1)^2 + 2$ takes every value in $[2, \infty)$, so $f$ takes every value in $(0, 4]$. The integers in $(0, 4]$ are $1, 2, 3, 4$, so the count is $4$.",
  r"Including a value approached only in the limit.",
  "U07-A-rng-integer-count", "Minimum of a quadratic, reciprocal bound, counting.",
  check=_c18, values=[4, 5, 8, 3], cognitive="Application",
  numerical=dict(question=r"The number of integers in the range of $f(x) = \frac{8}{x^2 - 2x + 3}$, $x \in \mathbb{R}$, is", answer=4))

q("U07-A-019", T_DOM, "Trigonometric inequality in one period", "Medium", "Single-step computation MCQ",
  r"If $f(x) = \sqrt{2\cos x - 1}$ with $x$ restricted to $[0, 2\pi)$, then the domain of $f$ is",
  r"$\left[0, \frac{\pi}{3}\right] \cup \left[\frac{5\pi}{3}, 2\pi\right)$",
  [(r"$\left[\frac{\pi}{3}, \frac{5\pi}{3}\right]$", r"Reverses the inequality and solves $\cos x \le \frac{1}{2}$."),
   (r"$\left[0, \frac{\pi}{6}\right] \cup \left[\frac{11\pi}{6}, 2\pi\right)$", r"Uses $\frac{\pi}{6}$ as the angle with cosine $\frac{1}{2}$, mixing it up with sine."),
   (r"$\left[0, \frac{\pi}{3}\right]$", r"Finds only the first-quadrant part and misses the fourth-quadrant arc.")],
  r"We need $\cos x \ge \frac{1}{2}$. In $[0, 2\pi)$, $\cos x = \frac{1}{2}$ at $x = \frac{\pi}{3}$ and $\frac{5\pi}{3}$, and $\cos x \ge \frac{1}{2}$ on $\left[0, \frac{\pi}{3}\right]$ and $\left[\frac{5\pi}{3}, 2\pi\right)$.",
  r"Missing the fourth-quadrant solutions of a cosine inequality.",
  "U07-A-dom-trig-inequality", "One trigonometric inequality over one period.",
  check=lambda: solve_univariate_inequality(2 * cos(X) - 1 >= 0, X, relational=False, domain=Interval.Ropen(0, 2 * pi)),
  values=[Union(Interval(0, pi / 3), Interval.Ropen(5 * pi / 3, 2 * pi)), Interval(pi / 3, 5 * pi / 3),
          Union(Interval(0, pi / 6), Interval.Ropen(11 * pi / 6, 2 * pi)), Interval(0, pi / 3)], cognitive="Application")


def _c20():
    u = Symbol('u', real=True)
    # cos(sin x) <= 1 always, so log(cos(sin x)) >= 0 exactly when cos(sin x) = 1
    pts = solveset(cos(u) - 1, u, Interval(-1, 1))
    win = Union(*[solveset(sin(X) - p, X, Interval(-10, 10)) for p in pts])
    s1 = (win == FiniteSet(*[n * pi for n in range(-3, 4)]))
    s2 = (rng((exp(X) - exp(-X)) / (exp(X) + exp(-X))) == Interval(-1, 1))
    return (bool(s1), bool(s2))
q("U07-A-020", T_DOM, "Domain and range statements", "Medium", "Statement-based MCQ",
  r"Statement I: The domain of $f(x) = \sqrt{\log_e(\cos(\sin x))}$ is $\{n\pi : n \in \mathbb{Z}\}$. Statement II: The range of $g(x) = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}}$, $x \in \mathbb{R}$, is $[-1, 1]$." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Accepts $[-1, 1]$ for $g$, not noticing that $|e^{x} - e^{-x}| < e^{x} + e^{-x}$, so $\pm 1$ are never attained."),
   (ST_FF, r"Rejects Statement I, thinking $\log_e(\cos(\sin x)) \le 0$ makes the domain empty, and also rejects Statement II correctly."),
   (ST_FT, r"Makes both slips: treats the domain in Statement I as empty and accepts the closed interval in Statement II.")],
  r"Since $\cos(\sin x) \le 1$, $\log_e(\cos(\sin x)) \le 0$, and the root needs it $\ge 0$, so we need $\cos(\sin x) = 1$. As $\sin x \in [-1, 1]$, this forces $\sin x = 0$, i.e. $x = n\pi$; Statement I is true. For $g$, $g(x) = \frac{e^{2x} - 1}{e^{2x} + 1} = 1 - \frac{2}{e^{2x} + 1}$ and $e^{2x} + 1 \in (1, \infty)$, so $g(x) \in (-1, 1)$; Statement II is false.",
  r"Treating a domain consisting of isolated points as empty, or treating asymptotic values as attained.",
  "U07-A-stmt-domain-range", "Two independent checks, one with an unusual discrete domain.",
  check=_c20, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis")


def _c21():
    k = Symbol('k', real=True)
    # k = 0 gives sqrt(-4x), not defined for all x; for k != 0 need k > 0 and discriminant <= 0
    assert dom(sqrt(-4 * X)) != S.Reals
    s = solve_univariate_inequality(16 - 4 * k**2 <= 0, k, relational=False)
    return s.intersect(Interval.open(0, oo))
q("U07-A-021", T_DOM, "Parameter for an all-real domain", "Medium", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which $f(x) = \sqrt{kx^2 - 4x + k}$ is defined for every real $x$ is",
  r"$[2, \infty)$",
  [(r"$(2, \infty)$", r"Requires a negative discriminant, excluding $k = 2$ where $2(x-1)^2 \ge 0$ still works."),
   (r"$(-\infty, -2] \cup [2, \infty)$", r"Solves only the discriminant condition and forgets that the leading coefficient must be positive."),
   (r"$[-2, 2]$", r"Reverses the discriminant inequality, solving $16 - 4k^2 \ge 0$.")],
  r"For $kx^2 - 4x + k \ge 0$ for all $x$ we need $k > 0$ (the case $k = 0$ gives $-4x$, negative for $x > 0$) and discriminant $16 - 4k^2 \le 0$, i.e. $k^2 \ge 4$. With $k > 0$ this gives $k \ge 2$.",
  r"Dropping the sign condition on the leading coefficient.",
  "U07-A-dom-parameter-all-reals", "Two conditions on a quadratic, one boundary case.",
  check=_c21, values=[Interval(2, oo), Interval.open(2, oo), Union(Interval(-oo, -2), Interval(2, oo)), Interval(-2, 2)],
  cognitive="Analysis")

# ================================================================ CLASS XI: DIFFICULT (7)

def _c22():
    f = (X**2 - 3 * X + 2) / (X**2 + X - 6)
    return rng(cancel(f), dom(f))
q("U07-A-022", T_RNG, "Range with a hole and an asymptote", "Difficult", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{x^2 - 3x + 2}{x^2 + x - 6}$ (on its natural domain) is",
  r"$\mathbb{R} \setminus \left\{1, \frac{1}{5}\right\}$",
  [(r"$\mathbb{R} \setminus \{1\}$", r"Cancels $(x - 2)$ and forgets that $x = 2$ is still excluded, so the value $\frac{1}{5}$ is missing."),
   (r"$\mathbb{R} \setminus \left\{\frac{1}{5}\right\}$", r"Removes the value at the hole but forgets that $\frac{x-1}{x+3} = 1$ has no solution."),
   (r"$\mathbb{R} \setminus \{1, 5\}$", r"Evaluates the reciprocal $\frac{x+3}{x-1}$ at $x = 2$, getting $5$ for the missing value.")],
  r"The domain is $x \ne 2, -3$, and there $f(x) = \frac{(x-1)(x-2)}{(x+3)(x-2)} = \frac{x - 1}{x + 3} = 1 - \frac{4}{x + 3}$. This never equals $1$, and it takes every other value once; but the value at $x = 2$, namely $\frac{1}{5}$, is lost. Hence the range is $\mathbb{R} \setminus \left\{1, \frac{1}{5}\right\}$.",
  r"Forgetting that a cancelled factor still removes a point from the domain and hence a value from the range.",
  "U07-A-rng-hole-and-asymptote", "Factorisation, an asymptotic value and a removed point; two separate exclusions.",
  check=_c22, values=[S.Reals - FiniteSet(1, Rational(1, 5)), S.Reals - FiniteSet(1), S.Reals - FiniteSet(Rational(1, 5)),
                      S.Reals - FiniteSet(1, 5)], cognitive="Analysis")


def _c23():
    a = Symbol('a', real=True)
    g = X**2 + 2 * a * X + 2 * a + 3
    xv = solve(diff(g, X), X)[0]
    mn = expand(g.subs(X, xv))
    sols = solve(Eq(mn, 1), a)            # minimum of the argument must be e^0 = 1
    assert all(mn.subs(a, s) > 0 for s in sols)
    return simplify(prod(sols))
q("U07-A-023", T_RNG, "Parameter fixing the range of a logarithm", "Difficult", "Inverse/parameter MCQ",
  r"The product of all real values of $a$ for which $f(x) = \log_e(x^2 + 2ax + 2a + 3)$ is defined for every real $x$ and has range exactly $[0, \infty)$ is",
  r"$-2$",
  [(r"$-3$", r"Sets the minimum of the quadratic equal to $0$ in place of $e^{0} = 1$, getting $a^2 - 2a - 3 = 0$."),
   (r"$-1$", r"Uses $c - \frac{b^2}{2}$ for the minimum, getting $2a^2 - 2a - 2 = 0$."),
   (r"$2$", r"Reports the sum $a_1 + a_2$ of the two values in place of their product.")],
  r"The quadratic has minimum value $2a + 3 - a^2$ at $x = -a$ and is unbounded above. The range of $f$ is $[0, \infty)$ exactly when this minimum is $e^{0} = 1$: $a^2 - 2a - 2 = 0$, so $a = 1 \pm \sqrt{3}$ (both make the quadratic positive everywhere). Their product is $-2$.",
  r"Equating the minimum of the argument to $0$ rather than to $1$.",
  "U07-A-rng-log-parameter", "Vertex value, translation of a log range into a minimum, then Vieta.",
  check=_c23, values=[-2, -3, -1, 2], cognitive="Analysis")

def _c24():
    t = Symbol('t', positive=True)          # t = 2**x takes every value in (0, oo)
    c = Symbol('c', positive=True)
    assert solveset(2**X - c, X, S.Reals) == FiniteSet(log(c) / log(2))   # every c > 0 is attained exactly once
    R = function_range((t**2 + 1) / (t + 1), t, Interval.open(0, oo))
    return Interval(nsimplify(simplify(R.left)), R.right, R.left_open, R.right_open)
q("U07-A-024", T_RNG, "Exponential rational expression with restricted variable", "Difficult", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{4^{x} + 1}{2^{x} + 1}$, $x \in \mathbb{R}$, is",
  r"$[2\sqrt{2} - 2, \infty)$",
  [(r"$(1, \infty)$", r"Assumes $f$ increases with $t = 2^{x}$ and takes the limit $1$ as $t \to 0^{+}$ as the lower end, missing the interior minimum."),
   (r"$[2\sqrt{2}, \infty)$", r"Applies AM-GM to $s + \frac{2}{s} \ge 2\sqrt{2}$ but forgets to subtract the $2$ in $f = s + \frac{2}{s} - 2$."),
   (r"$[1, \infty)$", r"Takes $t = 2^{x} \ge 1$ as if $x \ge 0$; then $s = t + 1 \ge 2$, $f$ is increasing there and starts at $f(0) = 1$.")],
  r"Let $t = 2^{x}$, which takes every value in $(0, \infty)$, and $s = t + 1 \in (1, \infty)$. Then $f = \frac{t^2 + 1}{t + 1} = t - 1 + \frac{2}{t + 1} = s + \frac{2}{s} - 2$. By AM-GM, $s + \frac{2}{s} \ge 2\sqrt{2}$, with equality at $s = \sqrt{2}$, which lies in $(1, \infty)$ (that is $x = \log_2(\sqrt{2} - 1)$). So the minimum is $2\sqrt{2} - 2$, and $f \to \infty$ as $s \to \infty$; by continuity the range is $[2\sqrt{2} - 2, \infty)$.",
  r"Assuming monotonicity in the substituted variable instead of locating the interior minimum and checking it is admissible.",
  "U07-A-rng-exponential-substitution", r"Substitution with $t > 0$, division to a form $s + \frac{2}{s}$, AM-GM, and a check that the equality point is admissible.",
  check=_c24,
  values=[Interval(2 * sqrt(2) - 2, oo), Interval.open(1, oo), Interval(2 * sqrt(2), oo), Interval(1, oo)], cognitive="Analysis")

q("U07-A-025", T_DOM, "Logarithm with a variable base under a root", "Difficult", "Multi-step computation MCQ",
  r"The domain of $f(x) = \frac{1}{\sqrt{\log_{(x-2)}(5 - x)}}$ is",
  r"$(3, 4)$",
  [(r"$(2, 3) \cup (3, 4)$", r"Uses $5 - x > 1$ for every admissible base, forgetting that for a base in $(0, 1)$ the inequality reverses."),
   (r"$(3, 5)$", r"Uses only base $> 1$ and argument $> 0$, forgetting that the logarithm itself must be positive."),
   (r"$(4, 5)$", r"Reverses the inequality for every base, solving $5 - x < 1$.")],
  r"We need $x - 2 > 0$, $x - 2 \ne 1$, $5 - x > 0$ and $\log_{(x-2)}(5 - x) > 0$. If $x - 2 > 1$ ($3 < x < 5$), we need $5 - x > 1$, so $3 < x < 4$. If $0 < x - 2 < 1$ ($2 < x < 3$), we need $5 - x < 1$, i.e. $x > 4$, impossible. So the domain is $(3, 4)$.",
  r"Not splitting into cases according to whether the base exceeds $1$.",
  "U07-A-dom-variable-base-casework", "Casework on the base with four simultaneous conditions.",
  check=lambda: dom(1 / sqrt(log(5 - X) / log(X - 2))),
  values=[Interval.open(3, 4), Union(Interval.open(2, 3), Interval.open(3, 4)), Interval.open(3, 5), Interval.open(4, 5)],
  cognitive="Analysis")


def _c26():
    return ints_in(dom(sqrt(16 - X**2) / log(X**2 - 2 * X)))
q("U07-A-026", T_DOM, "Integers in a domain with a log denominator", "Difficult", "Multi-step computation MCQ",
  r"The number of integers in the domain of $f(x) = \frac{\sqrt{16 - x^2}}{\log_e(x^2 - 2x)}$ is",
  r"$6$",
  [(r"$8$", r"Uses $x^2 - 2x \ge 0$, admitting $x = 0$ and $x = 2$ where the logarithm is undefined."),
   (r"$9$", r"Counts every integer in $[-4, 4]$, ignoring the logarithm altogether."),
   (r"$4$", r"Uses $16 - x^2 > 0$ for the numerator root, wrongly excluding $x = \pm 4$.")],
  r"We need $16 - x^2 \ge 0$ ($-4 \le x \le 4$), $x^2 - 2x > 0$ ($x < 0$ or $x > 2$) and $x^2 - 2x \ne 1$ ($x \ne 1 \pm \sqrt{2}$, not integers). The integers are $-4, -3, -2, -1$ and $3, 4$, so there are $6$.",
  r"Using $\ge 0$ for a logarithm's argument, or treating a numerator root like a denominator root.",
  "U07-A-dom-log-denominator-count", "Three conditions including a non-zero logarithm; careful counting.",
  check=_c26, values=[6, 8, 9, 4], cognitive="Analysis",
  numerical=dict(question=r"The number of integers in the domain of $f(x) = \frac{\sqrt{16 - x^2}}{\log_e(x^2 - 2x)}$ is", answer=6))

q("U07-A-027", T_RNG, "Double-angle sinusoid on a restricted interval", "Difficult", "Multi-step computation MCQ",
  r"The range of $f(x) = \sin^2 x + \sqrt{3}\sin x \cos x$ for $x \in \left[0, \frac{\pi}{2}\right]$ is",
  r"$\left[0, \frac{3}{2}\right]$",
  [(r"$\left[-\frac{1}{2}, \frac{3}{2}\right]$", r"Correctly writes $f = \frac{1}{2} + \sin\left(2x - \frac{\pi}{6}\right)$ but gives the range over all real $x$, ignoring the restricted interval."),
   (r"$[0, 1]$", r"Uses only the end-point values $f(0) = 0$ and $f\left(\frac{\pi}{2}\right) = 1$, missing the interior maximum at $x = \frac{\pi}{3}$."),
   (r"$\left[-\frac{1}{2}, 1\right]$", r"Drops the constant $\frac{1}{2}$ from $\sin^2 x = \frac{1 - \cos 2x}{2}$ and gives the range of $\sin\left(2x - \frac{\pi}{6}\right)$ alone.")],
  r"$\sin^2 x = \frac{1 - \cos 2x}{2}$ and $\sqrt{3}\sin x\cos x = \frac{\sqrt{3}}{2}\sin 2x$, so $f(x) = \frac{1}{2} + \frac{\sqrt{3}}{2}\sin 2x - \frac{1}{2}\cos 2x = \frac{1}{2} + \sin\left(2x - \frac{\pi}{6}\right)$. For $x \in \left[0, \frac{\pi}{2}\right]$, $2x - \frac{\pi}{6} \in \left[-\frac{\pi}{6}, \frac{5\pi}{6}\right]$, where the sine takes every value in $\left[-\frac{1}{2}, 1\right]$ (minimum at the left end, maximum at $\frac{\pi}{2}$). So $f$ takes every value in $\left[0, \frac{3}{2}\right]$.",
  r"Evaluating only at the ends of the interval, or using the unrestricted range of the sinusoid.",
  "U07-A-rng-sinusoid-interval", "Double-angle reduction, combination into one sinusoid, then tracking an interior maximum and an end-point minimum on a restricted interval.",
  check=lambda: rng(sin(X)**2 + sqrt(3) * sin(X) * cos(X), Interval(0, pi / 2)),
  values=[Interval(0, Rational(3, 2)), Interval(Rational(-1, 2), Rational(3, 2)), Interval(0, 1), Interval(Rational(-1, 2), 1)], cognitive="Analysis")

def _c28():
    v = Symbol('v', positive=True)
    V = solve_univariate_inequality(log(v) / log(Rational(1, 2)) >= 0, v, relational=False)  # v = log_2(log_3 x) > 0
    U = pre_inc(V, lambda t: 2**t)       # u = log_3 x, v = log_2 u
    return pre_inc(U, lambda t: 3**t)    # x = 3^u
q("U07-A-028", T_DOM, "Nested logarithms", "Difficult", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{\log_{1/2}\left(\log_2\left(\log_3 x\right)\right)}$ is",
  r"$(3, 9]$",
  [(r"$(1, 9]$", r"Uses only $\log_3 x > 0$ and $\log_2(\log_3 x) \le 1$, forgetting that $\log_2(\log_3 x)$ must itself be positive."),
   (r"$[9, \infty)$", r"Treats base $\frac{1}{2}$ like a base above $1$, solving $\log_2(\log_3 x) \ge 1$."),
   (r"$(3, 9)$", r"Requires the outer logarithm to be strictly positive, losing $x = 9$.")],
  r"Work outwards in. $\log_3 x$ needs $x > 0$; $\log_2(\log_3 x)$ needs $\log_3 x > 0$, so $x > 1$; $\log_{1/2}(\cdot)$ needs $\log_2(\log_3 x) > 0$, so $\log_3 x > 1$, $x > 3$; and the root needs $\log_{1/2}(\log_2(\log_3 x)) \ge 0$, so $\log_2(\log_3 x) \le 1$, $\log_3 x \le 2$, $x \le 9$. Domain $(3, 9]$.",
  r"Losing one layer's positivity condition in nested logarithms.",
  "U07-A-dom-nested-logs", "Four layered conditions, one with a decreasing logarithm.",
  check=_c28, values=[Interval.Lopen(3, 9), Interval.Lopen(1, 9), Interval(9, oo), Interval.open(3, 9)], cognitive="Analysis")

# ================================================================ CLASS XII: EASY (8)

def _c29():
    s = solve(Eq(Y, (2 * X + 3) / (X - 1)), X)
    assert len(s) == 1
    return s[0].subs(Y, X)
q("U07-A-029", T_INV, "Inverse of a linear fractional function", "Easy", "Single-step computation MCQ",
  r"The function $f : \mathbb{R} \setminus \{1\} \to \mathbb{R} \setminus \{2\}$, $f(x) = \frac{2x + 3}{x - 1}$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\frac{x + 3}{x - 2}$",
  [(r"$\frac{x - 1}{2x + 3}$", r"Takes the reciprocal $\frac{1}{f(x)}$ in place of the inverse function."),
   (r"$\frac{3 - x}{x - 2}$", r"From $xy - y = 2x + 3$, moves $-y$ across without changing its sign, getting $x(y - 2) = 3 - y$."),
   (r"$\frac{x + 3}{x + 2}$", r"Collects $xy - 2x$ as $x(y + 2)$.")],
  r"Let $y = \frac{2x + 3}{x - 1}$. Then $xy - y = 2x + 3$, so $x(y - 2) = y + 3$ and $x = \frac{y + 3}{y - 2}$. Hence $f^{-1}(x) = \frac{x + 3}{x - 2}$.",
  r"Confusing $f^{-1}$ with $\frac{1}{f}$.",
  "U07-A-inv-linear-fractional", "One rearrangement.",
  check=_c29, values=[(X + 3) / (X - 2), (X - 1) / (2 * X + 3), (3 - X) / (X - 2), (X + 3) / (X + 2)],
  cognitive="Application", source_class="XII")


def _c30():
    cands = [log(X + sqrt(X**2 + 1)), X * sin(X), X**3 + X**2, (exp(X) + exp(-X)) / 2]
    odd = [c for c in cands if parity(c) == -1]
    assert len(odd) == 1
    return odd[0]
q("U07-A-030", T_PAR, "Identifying an odd function", "Easy", "Direct concept MCQ",
  r"Which of the following functions, defined on $\mathbb{R}$, is odd?",
  r"$\log_e\left(x + \sqrt{x^2 + 1}\right)$",
  [(r"$x\sin x$", r"Thinks a product involving $x$ and $\sin x$ is odd, but the product of two odd functions is even."),
   (r"$x^3 + x^2$", r"Sees the cubic term and calls the whole polynomial odd, ignoring the even term $x^2$."),
   (r"$\frac{e^{x} + e^{-x}}{2}$", r"Mixes it up with $\frac{e^{x} - e^{-x}}{2}$; this one satisfies $f(-x) = f(x)$.")],
  r"For $f(x) = \log_e\left(x + \sqrt{x^2 + 1}\right)$, $f(-x) + f(x) = \log_e\left[\left(\sqrt{x^2+1} - x\right)\left(\sqrt{x^2+1} + x\right)\right] = \log_e 1 = 0$, so $f$ is odd. $x\sin x$ and $\frac{e^{x}+e^{-x}}{2}$ are even, and $x^3 + x^2$ is neither.",
  r"Believing a product of odd functions is odd.",
  "U07-A-par-identify-odd", "One parity test per option.",
  check=_c30, values=[log(X + sqrt(X**2 + 1)), X * sin(X), X**3 + X**2, (exp(X) + exp(-X)) / 2],
  cognitive="Understanding", source_class="XII")

q("U07-A-031", T_PAR, "Period of a sum of sinusoids", "Easy", "Single-step computation MCQ",
  r"The fundamental period of $f(x) = \sin 3x + \cos 2x$ is",
  r"$2\pi$",
  [(r"$\pi$", r"Takes the period of $\cos 2x$ alone."),
   (r"$\frac{2\pi}{3}$", r"Takes the period of $\sin 3x$ alone."),
   (r"$6\pi$", r"Multiplies the LCM of the numerators by the LCM of the denominators: $2\pi \times 3$.")],
  r"The periods are $\frac{2\pi}{3}$ and $\pi$. Their LCM is $\frac{\operatorname{LCM}(2\pi, \pi)}{\operatorname{HCF}(3, 1)} = 2\pi$. Checking smaller divisors such as $\pi$ shows $\sin 3(x + \pi) = -\sin 3x$, so $2\pi$ is the least period.",
  r"Using the period of only one term.",
  "U07-A-per-sum-sinusoids", "LCM of two periods.",
  check=lambda: min_period(sin(3 * X) + cos(2 * X), 2 * pi),
  values=[2 * pi, pi, 2 * pi / 3, 6 * pi], cognitive="Application", source_class="XII")


def _c32():
    out = S.EmptySet
    for n in range(-4, 4):
        out = Union(out, rng(n - X, Interval.Ropen(n, n + 1)))   # [x] = n on [n, n+1)
    return out
q("U07-A-032", T_GRF, "Greatest integer minus identity", "Easy", "Graph/diagram MCQ",
  r"If $[x]$ denotes the greatest integer less than or equal to $x$, the range of $f(x) = [x] - x$, $x \in \mathbb{R}$, is",
  r"$(-1, 0]$",
  [(r"$[0, 1)$", r"Gives the range of $x - [x]$, the fractional part, missing the sign."),
   (r"$[-1, 0)$", r"Places the open and closed ends the wrong way round, as if $-1$ were attained and $0$ not."),
   (r"$[-1, 0]$", r"Closes both ends, assuming the value $-1$ is reached at integers.")],
  r"$f(x) = -(x - [x]) = -\{x\}$. Since $\{x\} \in [0, 1)$, with $0$ at integers, $f(x) \in (-1, 0]$.",
  r"Losing track of which end of $[0, 1)$ is open after negation.",
  "U07-A-gif-fractional-range", "One identity and one negation.",
  check=_c32, values=[Interval.Lopen(-1, 0), Interval.Ropen(0, 1), Interval.Ropen(-1, 0), Interval(-1, 0)],
  cognitive="Understanding", source_class="XI")


def _c33():
    f = lambda t: t**2 + 1
    g = lambda t: 2 * t - 3
    r = solve(f(g(X)) - g(f(X)), X)
    return sum(r)
q("U07-A-033", T_INV, "Equal compositions", "Easy", "Multi-step computation MCQ",
  r"Let $f(x) = x^2 + 1$ and $g(x) = 2x - 3$. The sum of all real $x$ for which $(f \circ g)(x) = (g \circ f)(x)$ is",
  r"$6$",
  [(r"$\frac{11}{2}$", r"Reports the product of the roots of $2x^2 - 12x + 11 = 0$ in place of their sum."),
   (r"$-6$", r"Takes the sum of roots as $+\frac{b}{a}$ in place of $-\frac{b}{a}$."),
   (r"$12$", r"Reads the sum from $2x^2 - 12x + 11$ without dividing by the leading coefficient $2$.")],
  r"$(f \circ g)(x) = (2x - 3)^2 + 1 = 4x^2 - 12x + 10$ and $(g \circ f)(x) = 2(x^2 + 1) - 3 = 2x^2 - 1$. Equating: $2x^2 - 12x + 11 = 0$, whose discriminant $144 - 88 > 0$, so the sum of the real roots is $\frac{12}{2} = 6$.",
  r"Mishandling Vieta's formulas after forming the composition.",
  "U07-A-comp-equal-compositions", "Two compositions, then Vieta.",
  check=_c33, values=[6, Rational(11, 2), -6, 12], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = x^2 + 1$ and $g(x) = 2x - 3$. The sum of all real $x$ for which $(f \circ g)(x) = (g \circ f)(x)$ is", answer=6))


def _c34():
    r = [s for s in solve(X**3 + 2 * X - 1 - 2, X) if s.is_real]
    assert len(r) == 1
    return r[0]
q("U07-A-034", T_INV, "Value of an inverse function", "Easy", "Single-step computation MCQ",
  r"The function $f : \mathbb{R} \to \mathbb{R}$, $f(x) = x^3 + 2x - 1$, is a bijection. The value of $f^{-1}(2)$ is",
  r"$1$",
  [(r"$11$", r"Computes $f(2) = 8 + 4 - 1$ in place of $f^{-1}(2)$."),
   (r"$\frac{1}{11}$", r"Takes $f^{-1}(2)$ to mean $\frac{1}{f(2)}$."),
   (r"$\sqrt[3]{2}$", r"Keeps only the cubic term, solving $x^3 = 2$.")],
  r"$f^{-1}(2)$ is the real $x$ with $x^3 + 2x - 1 = 2$, i.e. $x^3 + 2x - 3 = (x - 1)(x^2 + x + 3) = 0$. The quadratic factor has discriminant $1 - 12 < 0$, so it has no real roots and $f^{-1}(2) = 1$.",
  r"Confusing $f^{-1}(a)$ with $f(a)$ or with $\frac{1}{f(a)}$.",
  "U07-A-inv-value", "Solve one cubic equation by inspection.",
  check=_c34, values=[1, 11, Rational(1, 11), cbrt(2)], cognitive="Understanding", source_class="XII",
  numerical=dict(question=r"The function $f : \mathbb{R} \to \mathbb{R}$, $f(x) = x^3 + 2x - 1$, is a bijection. The value of $f^{-1}(2)$ is", answer=1))

q("U07-A-035", T_PAR, "Period with a fractional part", "Easy", "Single-step computation MCQ",
  r"Let $\{x\} = x - [x]$ denote the fractional part of $x$. The fundamental period of $f(x) = \{x\} + \sin(\pi x)$ is",
  r"$2$",
  [(r"$1$", r"Uses the period of $\{x\}$ alone; but $\sin(\pi(x + 1)) = -\sin(\pi x)$."),
   (r"$2\pi$", r"Takes the period of $\sin(\pi x)$ to be $2\pi$, as for $\sin x$."),
   (r"$\pi$", r"Takes the period of $\sin(\pi x)$ to be $\pi$, then the LCM with $1$ as $\pi$.")],
  r"$\{x\}$ has period $1$ and $\sin(\pi x)$ has period $\frac{2\pi}{\pi} = 2$. The LCM is $2$, and $1$ fails because $\sin(\pi x)$ changes sign under $x \to x + 1$. So the period is $2$.",
  r"Using $2\pi$ as the period of $\sin(kx)$ for any $k$.",
  "U07-A-per-fractional-part", "LCM of two simple periods.",
  check=lambda: min_period(frac(X) + sin(pi * X), 2),
  values=[2, 1, 2 * pi, pi], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $\{x\} = x - [x]$ denote the fractional part of $x$. The fundamental period of $f(x) = \{x\} + \sin(\pi x)$ is", answer=2))

q("U07-A-036", T_GRF, "Sum of two moduli", "Easy", "Graph/diagram MCQ",
  r"The range of $f(x) = |x - 1| + |x - 3|$, $x \in \mathbb{R}$, is",
  r"$[2, \infty)$",
  [(r"$[0, \infty)$", r"Assumes a sum of moduli can be $0$, though both terms cannot vanish at once."),
   (r"$[4, \infty)$", r"Adds the constants $1 + 3$ for the minimum."),
   (r"$(2, \infty)$", r"Excludes $2$, though $f(x) = 2$ for every $x \in [1, 3]$.")],
  r"For $1 \le x \le 3$, $f(x) = (x - 1) + (3 - x) = 2$. For $x > 3$, $f(x) = 2x - 4 > 2$, and for $x < 1$, $f(x) = 4 - 2x > 2$, both unbounded. So the graph has a flat bottom at height $2$ and the range is $[2, \infty)$.",
  r"Not recognising the flat segment of the graph.",
  "U07-A-mod-sum-range", "Piecewise rewrite of two moduli.",
  check=lambda: abs_range(Abs(X - 1) + Abs(X - 3)),
  values=[Interval(2, oo), Interval(0, oo), Interval(4, oo), Interval.open(2, oo)], cognitive="Application", source_class="XI")

# ================================================================ CLASS XII: MEDIUM (13)

def _c37():
    k = Symbol('k', real=True)
    nsol = lambda kv: len(solveset(Abs(X**2 - 4) - kv, X, S.Reals))
    crit = sorted({0, (Abs(X**2 - 4)).subs(X, 0)})            # k = 0 and the local maximum at x = 0
    pts = [crit[0] - 1] + crit + [(crit[0] + crit[1]) / 2, crit[1] + 1]
    good = S.EmptySet
    edges = [-oo] + crit + [oo]
    for lo, hi in zip(edges[:-1], edges[1:]):
        mid = hi - 1 if lo == -oo else lo + 1 if hi == oo else (lo + hi) / 2
        if mid >= 0 and nsol(mid) == 4:
            good = Union(good, Interval.open(lo, hi))
    for c in crit:
        if nsol(c) == 4:
            good = Union(good, FiniteSet(c))
    return good
q("U07-A-037", T_GRF, "Modulus of a quadratic and a horizontal line", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which the equation $|x^2 - 4| = k$ has exactly four distinct real solutions is",
  r"$(0, 4)$",
  [(r"$(0, 4]$", r"Includes $k = 4$, where the line touches the peak at $x = 0$ and there are only three solutions."),
   (r"$[0, 4)$", r"Includes $k = 0$, where there are only the two solutions $x = \pm 2$."),
   (r"$(4, \infty)$", r"Takes the region above the central peak, where the line meets the graph only twice.")],
  r"The graph of $y = |x^2 - 4|$ is a W shape touching $0$ at $x = \pm 2$ with a central peak of height $4$ at $x = 0$. A horizontal line $y = k$ meets it in $4$ points exactly when $0 < k < 4$; $k = 0$ gives $2$, $k = 4$ gives $3$, and $k > 4$ gives $2$.",
  r"Mishandling the boundary cases where the line passes through a turning point.",
  "U07-A-mod-quadratic-line", "Graph of a reflected parabola with boundary cases.",
  check=_c37, values=[Interval.open(0, 4), Interval.Lopen(0, 4), Interval.Ropen(0, 4), Interval.open(4, oo)],
  cognitive="Analysis", source_class="XI")

_W = Interval.Ropen(-30, 30)


def _c38():
    out = S.EmptySet
    for n in range(-30, 30):
        if n**2 - n - 6 > 0:
            out = Union(out, Interval.Ropen(n, n + 1))
    return out
q("U07-A-038", T_GRF, "Domain involving the greatest integer function", "Medium", "Multi-step computation MCQ",
  r"If $[x]$ denotes the greatest integer less than or equal to $x$, the domain of $f(x) = \frac{1}{\sqrt{[x]^2 - [x] - 6}}$ is",
  r"$(-\infty, -2) \cup [4, \infty)$",
  [(r"$(-\infty, -2) \cup (3, \infty)$", r"Solves $[x] < -2$ or $[x] > 3$ and then replaces $[x]$ by $x$ directly."),
   (r"$(-\infty, -3) \cup [4, \infty)$", r"Converts $[x] \le -3$ into $x < -3$ in place of $x < -2$."),
   (r"$(-\infty, -2] \cup [4, \infty)$", r"Includes $x = -2$, where $[x]^2 - [x] - 6 = 0$.")],
  r"Put $n = [x]$: we need $n^2 - n - 6 = (n - 3)(n + 2) > 0$, so $n < -2$ or $n > 3$; as $n$ is an integer, $n \le -3$ or $n \ge 4$. Now $[x] \le -3 \iff x < -2$ and $[x] \ge 4 \iff x \ge 4$. Domain: $(-\infty, -2) \cup [4, \infty)$.",
  r"Translating a condition on $[x]$ into one on $x$ incorrectly.",
  "U07-A-gif-domain", "Quadratic in $[x]$, integer restriction, conversion back to $x$.",
  check=_c38, values=[Union(Interval.open(-oo, -2), Interval(4, oo)).intersect(_W),
                      Union(Interval.open(-oo, -2), Interval.open(3, oo)).intersect(_W),
                      Union(Interval.open(-oo, -3), Interval(4, oo)).intersect(_W),
                      Union(Interval(-oo, -2), Interval(4, oo)).intersect(_W)],
  cognitive="Application", source_class="XI")

q("U07-A-039", T_PAR, "Period of a power sum", "Medium", "Multi-step computation MCQ",
  r"The fundamental period of $f(x) = \sin^4 x + \cos^4 x$ is",
  r"$\frac{\pi}{2}$",
  [(r"$\pi$", r"Uses the fact that even powers of $\sin x$ and $\cos x$ have period $\pi$, without checking smaller periods."),
   (r"$2\pi$", r"Takes the period of $\sin x$ and $\cos x$ unchanged."),
   (r"$\frac{\pi}{4}$", r"Reduces to $\cos 4x$ correctly but then halves its period $\frac{\pi}{2}$ once more.")],
  r"$\sin^4 x + \cos^4 x = 1 - 2\sin^2 x\cos^2 x = 1 - \frac{1}{2}\sin^2 2x = \frac{3}{4} + \frac{1}{4}\cos 4x$. The period of $\cos 4x$ is $\frac{2\pi}{4} = \frac{\pi}{2}$.",
  r"Stopping at an obvious period without simplifying to find the least one.",
  "U07-A-per-power-sum", "Identity reduction before reading the period.",
  check=lambda: min_period(sin(X)**4 + cos(X)**4, 2 * pi),
  values=[pi / 2, pi, 2 * pi, pi / 4], cognitive="Application", source_class="XII")

q("U07-A-040", T_PAR, "Period of a sum with rational frequencies", "Medium", "Single-step computation MCQ",
  r"The fundamental period of $f(x) = \sin\left(\frac{\pi x}{2}\right) + \cos\left(\frac{\pi x}{3}\right)$ is",
  r"$12$",
  [(r"$24$", r"Multiplies the two periods $4 \times 6$ in place of taking their LCM."),
   (r"$2$", r"Takes the HCF of the periods $4$ and $6$."),
   (r"$6$", r"Takes the larger of the two periods.")],
  r"$\sin\left(\frac{\pi x}{2}\right)$ has period $\frac{2\pi}{\pi/2} = 4$ and $\cos\left(\frac{\pi x}{3}\right)$ has period $\frac{2\pi}{\pi/3} = 6$. The fundamental period is $\operatorname{LCM}(4, 6) = 12$.",
  r"Using the product or HCF of periods in place of the LCM.",
  "U07-A-per-rational-frequencies", "Two periods and an LCM.",
  check=lambda: min_period(sin(pi * X / 2) + cos(pi * X / 3), 24),
  values=[12, 24, 2, 6], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The fundamental period of $f(x) = \sin\left(\frac{\pi x}{2}\right) + \cos\left(\frac{\pi x}{3}\right)$ is", answer=12))


def _c41():
    s = solve(Eq(Y, X + 1 / X), X)
    keep = [r for r in s if r.subs(Y, Rational(5, 2)) >= 1]     # branch landing in [1, oo)
    assert len(keep) == 1
    return keep[0].subs(Y, X)
q("U07-A-041", T_INV, "Inverse on a restricted domain", "Medium", "Multi-step computation MCQ",
  r"The function $f : [1, \infty) \to [2, \infty)$, $f(x) = x + \frac{1}{x}$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\frac{x + \sqrt{x^2 - 4}}{2}$",
  [(r"$\frac{x - \sqrt{x^2 - 4}}{2}$", r"Picks the root lying in $(0, 1]$, not the one in $[1, \infty)$."),
   (r"$\frac{x}{x^2 + 1}$", r"Takes the reciprocal $\frac{1}{f(x)}$ in place of the inverse."),
   (r"$\frac{x + \sqrt{x^2 + 4}}{2}$", r"Writes the discriminant of $t^2 - yt + 1 = 0$ as $y^2 + 4$.")],
  r"Let $y = x + \frac{1}{x}$, so $x^2 - yx + 1 = 0$ and $x = \frac{y \pm \sqrt{y^2 - 4}}{2}$. The two roots have product $1$, so one is $\ge 1$ and the other $\le 1$; since $x \ge 1$ we take the $+$ sign. So $f^{-1}(x) = \frac{x + \sqrt{x^2 - 4}}{2}$.",
  r"Choosing the wrong branch when inverting a function on a restricted domain.",
  "U07-A-inv-restricted-branch", "Quadratic in $x$, then choosing the branch from the domain.",
  check=_c41, values=[(X + sqrt(X**2 - 4)) / 2, (X - sqrt(X**2 - 4)) / 2, X / (X**2 + 1), (X + sqrt(X**2 + 4)) / 2],
  cognitive="Application", source_class="XII")

q("U07-A-042", T_PAR, "Hidden even function", "Medium", "Conceptual/application MCQ",
  r"The function $f(x) = \frac{x}{e^{x} - 1} + \frac{x}{2} + 1$, $x \ne 0$, is",
  r"even but not odd",
  [(r"odd but not even", r"Sees the odd term $\frac{x}{2}$ and assumes the whole function is odd."),
   (r"neither even nor odd", r"Checks only that no single term is even, without combining $\frac{x}{e^{x}-1}$ with $\frac{x}{2}$."),
   (r"even as well as odd", r"Believes the even and odd parts cancel, making $f$ identically zero.")],
  r"$f(-x) = \frac{-x}{e^{-x} - 1} - \frac{x}{2} + 1 = \frac{x e^{x}}{e^{x} - 1} - \frac{x}{2} + 1$. Then $f(-x) - f(x) = \frac{x e^{x} - x}{e^{x} - 1} - x = x - x = 0$. So $f$ is even, and since $f(1) \ne 0$ it is not odd.",
  r"Judging parity term by term instead of for the whole expression.",
  "U07-A-par-hidden-even", "Algebraic simplification of $f(-x)$.",
  check=lambda: parity(X / (exp(X) - 1) + X / 2 + 1), values=[1, -1, 0, 2],
  cognitive="Analysis", source_class="XII")


def _c43():
    return solveset(Abs(X - 1) + Abs(X - 2) + Abs(X - 4) - 3, X, S.Reals)   # the full solution set
q("U07-A-043", T_GRF, "Sum of three moduli", "Medium", "Graph/diagram MCQ",
  r"The number of real solutions of $|x - 1| + |x - 2| + |x - 4| = 3$ is",
  r"$1$",
  [(r"infinitely many", r"Treats the graph like that of two moduli, assuming it is flat at height $4 - 1 = 3$ on all of $[1, 4]$ and ignoring the middle term $|x - 2|$."),
   (r"$3$", r"Solves the linear equation on every piece without checking the piece: $7 - 3x = 3$ gives $x = \frac{4}{3}$ and $3x - 7 = 3$ gives $x = \frac{10}{3}$, together with $x = 2$."),
   (r"$0$", r"Takes the minimum at the mean $x = \frac{7}{3}$ of $1, 2, 4$, where the sum is $\frac{10}{3} > 3$, and concludes the equation has no solution.")],
  r"Let $g(x) = |x - 1| + |x - 2| + |x - 4|$. Piecewise, $g = 7 - 3x$ on $x \le 1$, $5 - x$ on $[1, 2]$, $x + 1$ on $[2, 4]$ and $3x - 7$ on $x \ge 4$. So $g$ decreases up to $x = 2$ and increases after it, with minimum $g(2) = 3$ attained only at $x = 2$ (the median of $1, 2, 4$). Hence $g(x) = 3$ has exactly $1$ real solution.",
  r"Carrying the flat-bottom picture of two moduli over to three moduli, whose minimum is at the median point only.",
  "U07-A-mod-three-moduli-median", "Piecewise graph of three moduli; the minimum is at the median and is attained once.",
  check=_c43, values=[FiniteSet(2), Interval(1, 4), FiniteSet(Rational(4, 3), 2, Rational(10, 3)), S.EmptySet], cognitive="Analysis", source_class="XI")

def _c44():
    f = sign(X**2 - 2 * X - 3) + sign(X - 1)
    crit = sorted(set(solve(X**2 - 2 * X - 3, X) + solve(X - 1, X)))
    tests = list(crit) + [crit[0] - 1, crit[-1] + 1] + [(a + b) / 2 for a, b in zip(crit[:-1], crit[1:])]
    return FiniteSet(*[f.subs(X, t) for t in tests])
q("U07-A-044", T_GRF, "Range of a sum of signum functions", "Medium", "Multi-step computation MCQ",
  r"Let $\operatorname{sgn}$ denote the signum function. The range of $f(x) = \operatorname{sgn}(x^2 - 2x - 3) + \operatorname{sgn}(x - 1)$, $x \in \mathbb{R}$, is",
  r"$\{-2, -1, 0, 1, 2\}$",
  [(r"$\{-2, 0, 2\}$", r"Uses only the values $\pm 1$ of each signum, ignoring the points where an argument is $0$."),
   (r"$\{-1, 0, 1\}$", r"Assumes a sum of signum values is itself a signum value."),
   (r"$\{-2, -1, 0, 2\}$", r"Checks the zeros $x = -1$ and $x = 1$ but misses $x = 3$, where the value is $1$.")],
  r"$x^2 - 2x - 3 = (x - 3)(x + 1)$. For $x < -1$: $1 - 1 = 0$; $x = -1$: $0 - 1 = -1$; $-1 < x < 1$: $-1 - 1 = -2$; $x = 1$: $-1 + 0 = -1$; $1 < x < 3$: $-1 + 1 = 0$; $x = 3$: $0 + 1 = 1$; $x > 3$: $1 + 1 = 2$. The range is $\{-2, -1, 0, 1, 2\}$.",
  r"Forgetting that $\operatorname{sgn}(0) = 0$ produces extra values at isolated points.",
  "U07-A-sgn-sum-range", "Sign chart of two expressions including isolated points.",
  check=_c44, values=[FiniteSet(-2, -1, 0, 1, 2), FiniteSet(-2, 0, 2), FiniteSet(-1, 0, 1), FiniteSet(-2, -1, 0, 2)],
  cognitive="Application", source_class="XI")


def _c45():
    f = lambda t: (3 * t - 2) / (2 * t - 3)
    return simplify(f(f(f(X))))
q("U07-A-045", T_INV, "Self-inverse function composed thrice", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \frac{3x - 2}{2x - 3}$, $x \ne \frac{3}{2}$. Then $(f \circ f \circ f)(x)$, wherever defined, equals",
  r"$\frac{3x - 2}{2x - 3}$",
  [(r"$x$", r"Assumes three applications return $x$, when in fact two applications do."),
   (r"$\frac{2x - 3}{3x - 2}$", r"Takes $f \circ f \circ f$ to be $f^{-1}$ and then confuses $f^{-1}$ with $\frac{1}{f}$."),
   (r"$\frac{3x + 2}{2x + 3}$", r"Takes $f \circ f \circ f$ to be $f^{-1}$ and, solving $y(2x - 3) = 3x - 2$, gets $x(2y + 3) = 3y + 2$.")],
  r"$(f \circ f)(x) = \frac{3\frac{3x-2}{2x-3} - 2}{2\frac{3x-2}{2x-3} - 3} = \frac{9x - 6 - 4x + 6}{6x - 4 - 6x + 9} = \frac{5x}{5} = x$. So $f$ is its own inverse and $f \circ f \circ f = f$, i.e. $\frac{3x - 2}{2x - 3}$.",
  r"Not computing $f \circ f$ first to spot an involution.",
  "U07-A-comp-involution", "Composition revealing a self-inverse function.",
  check=_c45, values=[(3 * X - 2) / (2 * X - 3), X, (2 * X - 3) / (3 * X - 2), (3 * X + 2) / (2 * X + 3)],
  cognitive="Analysis", source_class="XII")


def _c46():
    t = Symbol('t', positive=True)       # t = 2^x
    s = [r for r in solve(Eq(Y, (t - 1 / t) / (t + 1 / t)), t) if r.subs(Y, 0) > 0]
    assert len(s) == 1
    return simplify(log(s[0], 2).subs(Y, X))
q("U07-A-046", T_INV, "Inverse of an exponential quotient", "Medium", "Multi-step computation MCQ",
  r"The function $f : \mathbb{R} \to (-1, 1)$, $f(x) = \frac{2^{x} - 2^{-x}}{2^{x} + 2^{-x}}$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\frac{1}{2}\log_2\left(\frac{1 + x}{1 - x}\right)$",
  [(r"$\log_2\left(\frac{1 + x}{1 - x}\right)$", r"Solves for $4^{x} = \frac{1+y}{1-y}$ correctly but then writes $x = \log_2\frac{1+y}{1-y}$, dropping the factor $\frac{1}{2}$."),
   (r"$\frac{1}{2}\log_2\left(\frac{1 - x}{1 + x}\right)$", r"Inverts the fraction while solving $y(4^{x} + 1) = 4^{x} - 1$."),
   (r"$\frac{1}{2}\log_e\left(\frac{1 + x}{1 - x}\right)$", r"Uses the natural logarithm, as for $\tanh$, although the base here is $2$.")],
  r"$f(x) = \frac{4^{x} - 1}{4^{x} + 1}$. Setting $y = f(x)$: $y \cdot 4^{x} + y = 4^{x} - 1$, so $4^{x} = \frac{1 + y}{1 - y}$ and $x = \frac{1}{2}\log_2\frac{1 + y}{1 - y}$. Hence $f^{-1}(x) = \frac{1}{2}\log_2\left(\frac{1 + x}{1 - x}\right)$.",
  r"Losing the factor $\frac{1}{2}$ from $4^{x} = 2^{2x}$.",
  "U07-A-inv-exponential-quotient", "Rewriting with $4^{x}$, solving and taking logarithms.",
  check=_c46, values=[log((1 + X) / (1 - X), 2) / 2, log((1 + X) / (1 - X), 2), log((1 - X) / (1 + X), 2) / 2,
                      log((1 + X) / (1 - X)) / 2], cognitive="Application", source_class="XII")


def _c47():
    f = lambda t: t**2 - 2 * t
    return len(solveset(f(f(X)) - 3, X, S.Reals))
q("U07-A-047", T_INV, "Solving a composite equation", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = x^2 - 2x$, $x \in \mathbb{R}$. The number of distinct real solutions of $f(f(x)) = 3$ is",
  r"$3$",
  [(r"$4$", r"Counts the repeated root $x = 1$ of $(x - 1)^2 = 0$ twice."),
   (r"$2$", r"Keeps only $f(x) = 3$ and discards $f(x) = -1$, thinking a quadratic cannot equal a negative number."),
   (r"$1$", r"Keeps only the branch $f(x) = -1$.")],
  r"Let $u = f(x)$: $u^2 - 2u - 3 = 0$, so $u = 3$ or $u = -1$. $f(x) = 3$ gives $x^2 - 2x - 3 = 0$, $x = 3, -1$. $f(x) = -1$ gives $(x - 1)^2 = 0$, $x = 1$. So there are $3$ distinct solutions.",
  r"Discarding a valid branch because the inner function's value is negative.",
  "U07-A-comp-equation-count", "Two-layer substitution with a repeated root.",
  check=_c47, values=[3, 4, 2, 1], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = x^2 - 2x$, $x \in \mathbb{R}$. The number of distinct real solutions of $f(f(x)) = 3$ is", answer=3))


def _c48():
    s1 = periodicity(sin(Abs(X)), X) is not None
    s2 = min_period(Abs(sin(X)), periodicity(Abs(sin(X)), X)) == pi
    return (bool(s1), bool(s2))
q("U07-A-048", T_PAR, "Periodicity with modulus", "Medium", "Statement-based MCQ",
  r"Statement I: The function $f(x) = \sin|x|$, $x \in \mathbb{R}$, is periodic. Statement II: The function $g(x) = |\sin x|$, $x \in \mathbb{R}$, is periodic with fundamental period $\pi$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Assumes $\sin|x|$ inherits the period $2\pi$, though its graph is a mirror image about the $y$-axis and does not repeat."),
   (ST_FF, r"Rejects Statement II, thinking $|\sin x|$ keeps the period $2\pi$ of $\sin x$."),
   (ST_TF, r"Makes both slips: accepts $\sin|x|$ as periodic and keeps $2\pi$ for $|\sin x|$.")],
  r"Suppose $T > 0$ were a period of $f(x) = \sin|x|$. For $x \ge 0$ this reads $\sin(x + T) = \sin x$, so $T$ is a multiple of $2\pi$. But then $f\left(-\frac{\pi}{2} + T\right) = \sin\left(T - \frac{\pi}{2}\right) = -1$, while $f\left(-\frac{\pi}{2}\right) = \sin\frac{\pi}{2} = 1$, a contradiction. Statement I is false. $|\sin(x + \pi)| = |-\sin x| = |\sin x|$, and no smaller positive number works, since $|\sin x| = 0$ only at multiples of $\pi$. Statement II is true.",
  r"Assuming any expression built from $\sin$ is periodic.",
  "U07-A-stmt-modulus-periodicity", "Two periodicity checks, one negative.",
  check=_c48, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis", source_class="XII")


def _c49():
    vals = set()
    for n in range(-5, 5):
        for t in (n, n + Rational(1, 3), n + Rational(5, 7)):
            vals.add(floor(t) + floor(-t))
    s1 = (FiniteSet(*vals) == FiniteSet(-1, 0, 1))
    s2 = parity(X * sign(X)) in (-1, 2)
    return (bool(s1), bool(s2))
q("U07-A-049", T_GRF, "Greatest integer and signum statements", "Medium", "Statement-based MCQ",
  r"Let $[x]$ denote the greatest integer less than or equal to $x$ and $\operatorname{sgn}$ the signum function. Statement I: The range of $f(x) = [x] + [-x]$, $x \in \mathbb{R}$, is $\{-1, 0, 1\}$. Statement II: The function $g(x) = x \operatorname{sgn}(x)$, $x \in \mathbb{R}$, is an odd function." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Accepts $1$ in the range of $[x] + [-x]$ and treats $x \operatorname{sgn}(x)$ as a product of two odd functions that stays odd."),
   (ST_TF, r"Accepts the range $\{-1, 0, 1\}$, assuming $[x] + [-x]$ can be $1$, but correctly sees that $g$ is not odd."),
   (ST_FT, r"Correctly finds the range $\{-1, 0\}$ but believes a product of two odd functions is odd.")],
  r"If $x$ is an integer, $[x] + [-x] = x - x = 0$; otherwise $[-x] = -[x] - 1$, so the sum is $-1$. The range is $\{-1, 0\}$; Statement I is false. $g(x) = x \operatorname{sgn}(x) = |x|$, which is even (and not odd, as $g(1) = 1 \ne 0$); Statement II is false.",
  r"Believing the product of two odd functions is odd.",
  "U07-A-stmt-gif-sgn", "Two short checks on special functions.",
  check=_c49, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Understanding", source_class="XI")

# ================================================================ CLASS XII: DIFFICULT (7)

def _c50():
    known = {Rational(1, 2): 3, Rational(1, 3): 5}

    def f(a):
        a = a - 2 * floor((a + 1) / 2)             # period 2: reduce into [-1, 1)
        if a == -1 or a == 0:
            return 0                               # f(0) = 0 (odd); f(-1) = f(1) = -f(-1) gives 0
        return known[a] if a > 0 else -known[-a]  # odd
    return f(Rational(7, 2)) + f(Rational(-11, 3)) + f(5)
q("U07-A-050", T_PAR, "Odd periodic function values", "Difficult", "Multi-step computation MCQ",
  r"Let $f : \mathbb{R} \to \mathbb{R}$ be an odd function with $f(x + 2) = f(x)$ for all real $x$. If $f\left(\frac{1}{2}\right) = 3$ and $f\left(\frac{1}{3}\right) = 5$, then $f\left(\frac{7}{2}\right) + f\left(-\frac{11}{3}\right) + f(5)$ equals",
  r"$2$",
  [(r"$8$", r"Ignores oddness and takes $f\left(-\frac{1}{2}\right) = 3$."),
   (r"$-8$", r"Writes $f\left(-\frac{11}{3}\right) = -f\left(\frac{11}{3}\right) = -f\left(-\frac{1}{3}\right)$ and then forgets the second sign, getting $-5$."),
   (r"$-2$", r"Applies oddness to the wrong terms: takes $f\left(\frac{7}{2}\right) = 3$ and $f\left(-\frac{11}{3}\right) = -5$.")],
  r"$f\left(\frac{7}{2}\right) = f\left(\frac{7}{2} - 4\right) = f\left(-\frac{1}{2}\right) = -3$. $f\left(-\frac{11}{3}\right) = f\left(-\frac{11}{3} + 4\right) = f\left(\frac{1}{3}\right) = 5$. For $f(5) = f(1)$: periodicity gives $f(1) = f(-1)$ and oddness gives $f(-1) = -f(1)$, so $f(1) = 0$. The sum is $-3 + 5 + 0 = 2$.",
  r"Not noticing that an odd function with period $2$ must vanish at odd integers.",
  "U07-A-par-odd-periodic", "Periodic reduction, oddness, and a hidden zero at $x = 1$.",
  check=_c50, values=[2, 8, -8, -2], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f : \mathbb{R} \to \mathbb{R}$ be an odd function with $f(x + 2) = f(x)$ for all real $x$. If $f\left(\frac{1}{2}\right) = 3$ and $f\left(\frac{1}{3}\right) = 5$, then the value of $f\left(\frac{7}{2}\right) + f\left(-\frac{11}{3}\right) + f(5)$ is", answer=2))


def _c51():
    sols = set()
    for n in range(-15, 15):
        for r in solve(X**2 - (3 - n), X):
            if r.is_real and floor(r) == n:
                sols.add(r)
    return len(sols)
q("U07-A-051", T_GRF, "Equation with the greatest integer function", "Difficult", "Multi-step computation MCQ",
  r"If $[x]$ denotes the greatest integer less than or equal to $x$, the number of real solutions of $x^2 + [x] = 3$ is",
  r"$2$",
  [(r"$1$", r"Checks only $[x] \ge 0$ and finds just $x = \sqrt{2}$."),
   (r"$3$", r"Also accepts $x = -\sqrt{5}$ from $[x] = -2$, misjudging $-\sqrt{5} \approx -2.24$ as lying in $[-2, -1)$."),
   (r"$4$", r"Accepts $x = -\sqrt{5}$ and also $x = \sqrt{3}$ from $[x] = 0$, without checking $[x]$ for either.")],
  r"Let $[x] = n$, so $x^2 = 3 - n$ with $n \le x < n + 1$. $n = 1$: $x = \sqrt{2} \in [1, 2)$, valid. $n = 0$: $x = \pm\sqrt{3}$, neither in $[0, 1)$. $n = -1$: $x = -2 \notin [-1, 0)$. $n = -2$: $x = -\sqrt{5} \approx -2.24 \notin [-2, -1)$. $n = -3$: $x = -\sqrt{6} \approx -2.45 \in [-3, -2)$, valid. For $n \le -4$, $(n + 1)^2 - (3 - n) = n^2 + 3n - 2 > 0$, so $\sqrt{3 - n} < -(n + 1)$ and $x = -\sqrt{3 - n} > n + 1$, outside $[n, n + 1)$; and $n \ge 2$ gives $x^2 \le 1 < n^2$. So there are $2$ solutions.",
  r"Not checking that each candidate actually has the assumed integer part.",
  "U07-A-gif-equation-count", "Casework over integer parts with consistency checks.",
  check=_c51, values=[2, 1, 3, 4], cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"If $[x]$ denotes the greatest integer less than or equal to $x$, the number of real solutions of $x^2 + [x] = 3$ is", answer=2))


def _c52():
    a, b = symbols('a b')                 # a = f(x - 1), b = f(x)
    seq = [a, b]
    while True:
        seq.append(expand(seq[-1] - seq[-2]))   # f(x + 1) = f(x) - f(x - 1)
        k = len(seq) - 2                         # seq[-1] is f(x + k)
        if expand(seq[-1] - b) == 0 and expand(seq[-2] - seq[0]) == 0:
            break
    # the solution sin(pi x / 3) shows no smaller common period exists
    g = sin(pi * X / 3)
    assert simplify(g.subs(X, X + 1) + g.subs(X, X - 1) - g) == 0
    assert min_period(g, k) == k
    return k
q("U07-A-052", T_PAR, "Period from a functional equation", "Difficult", "Multi-step computation MCQ",
  r"Let $f : \mathbb{R} \to \mathbb{R}$ satisfy $f(x + 1) + f(x - 1) = f(x)$ for all real $x$. The smallest positive $T$ such that $f(x + T) = f(x)$ holds for all real $x$ and for every such function $f$ is",
  r"$6$",
  [(r"$3$", r"Stops at $f(x + 3) = -f(x)$ and reads it as a period of $3$."),
   (r"$4$", r"Shifts the index wrongly to get $f(x + 2) = -f(x)$, giving period $4$."),
   (r"$2$", r"Treats the relation as $f(x + 1) = f(x - 1)$.")],
  r"Replace $x$ by $x + 1$: $f(x + 2) + f(x) = f(x + 1)$. Adding this to the given relation gives $f(x + 2) = -f(x - 1)$, i.e. $f(x + 3) = -f(x)$. Hence $f(x + 6) = -f(x + 3) = f(x)$. The function $\sin\frac{\pi x}{3}$ satisfies the relation and has least period $6$, so no smaller $T$ works for every $f$.",
  r"Confusing $f(x + T) = -f(x)$ with periodicity.",
  "U07-A-per-functional-equation", "Manipulating a functional equation twice and checking minimality.",
  check=_c52, values=[6, 3, 4, 2], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f : \mathbb{R} \to \mathbb{R}$ satisfy $f(x + 1) + f(x - 1) = f(x)$ for all real $x$. The smallest positive $T$ such that $f(x + T) = f(x)$ holds for all real $x$ and for every such function $f$ is", answer=6))


def _c53():
    q2 = X**2 - 4
    where = {1: solve_univariate_inequality(q2 > 0, X, relational=False),
             0: solveset(q2, X, S.Reals),
             -1: solve_univariate_inequality(q2 < 0, X, relational=False)}
    out = S.EmptySet
    for n, Sn in where.items():
        out = Union(out, Interval.Ropen(n, n + 1).intersect(Sn))
    return out
q("U07-A-053", T_GRF, "Signum equal to greatest integer", "Difficult", "Multi-step computation MCQ",
  r"Let $[x]$ denote the greatest integer less than or equal to $x$ and $\operatorname{sgn}$ the signum function. The set of all real $x$ satisfying $\operatorname{sgn}(x^2 - 4) = [x]$ is",
  r"$[-1, 0)$",
  [(r"$\{-1\}$", r"Tests only integer values of $x$."),
   (r"$(-2, 0)$", r"Uses $x^2 < 4$ and $x < 0$ but forgets that $[x] = -1$ also needs $x \ge -1$."),
   (r"$[-1, 0]$", r"Treats the interval where $[x] = -1$ as closed at $0$, though $[0] = 0$ while $\operatorname{sgn}(-4) = -1$.")],
  r"The left side lies in $\{-1, 0, 1\}$, so $[x] \in \{-1, 0, 1\}$. $[x] = 1$: $x \in [1, 2)$ needs $x^2 > 4$, impossible. $[x] = 0$: $x \in [0, 1)$ needs $x^2 = 4$, impossible. $[x] = -1$: $x \in [-1, 0)$ needs $x^2 < 4$, true throughout. So the solution set is $[-1, 0)$.",
  r"Not restricting to the interval on which the greatest integer has the assumed value.",
  "U07-A-sgn-gif-equation", "Casework combining two special functions.",
  check=_c53, values=[Interval.Ropen(-1, 0), FiniteSet(-1), Interval.open(-2, 0), Interval(-1, 0)],
  cognitive="Analysis", source_class="XI")


def _c54():
    out = S.EmptySet
    for n in range(0, 2):
        cond = solve_univariate_inequality(X**2 >= n**2, X, relational=False).intersect(
            solve_univariate_inequality(X**2 < n**2 + 1, X, relational=False))   # [x^2] = n^2
        out = Union(out, Interval.Ropen(n, n + 1).intersect(cond))                # [x] = n
    return out.intersect(Interval.Ropen(0, 2))
q("U07-A-054", T_GRF, "Commuting floor and square", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = x^2$ and $g(x) = [x]$, where $[x]$ is the greatest integer less than or equal to $x$. The set of all $x \in [0, 2)$ for which $(f \circ g)(x) = (g \circ f)(x)$ is",
  r"$[0, \sqrt{2})$",
  [(r"$[0, 1)$", r"Checks only the piece $[x] = 0$ and misses part of $[1, 2)$."),
   (r"$[0, 2)$", r"Assumes $[x^2] = [x]^2$ always holds."),
   (r"$[0, \sqrt{2}]$", r"Includes $x = \sqrt{2}$, where $[x^2] = 2$ but $[x]^2 = 1$.")],
  r"We need $[x]^2 = [x^2]$. On $[0, 1)$: $[x]^2 = 0$ and $x^2 < 1$ so $[x^2] = 0$; all of $[0, 1)$ works. On $[1, 2)$: $[x]^2 = 1$, so we need $1 \le x^2 < 2$, i.e. $1 \le x < \sqrt{2}$. The set is $[0, \sqrt{2})$.",
  r"Assuming the greatest integer function commutes with squaring.",
  "U07-A-gif-composition-commute", "Two compositions compared piece by piece.",
  check=_c54, values=[Interval.Ropen(0, sqrt(2)), Interval.Ropen(0, 1), Interval.Ropen(0, 2), Interval(0, sqrt(2))],
  cognitive="Analysis", source_class="XI")


def _c55():
    f = lambda t: t**2 - 4 * t + 3
    return rng(f(f(X)), Interval(0, 1))
q("U07-A-055", T_INV, "Range of a composite on an interval", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = x^2 - 4x + 3$ for all real $x$. The set of values taken by $f(f(x))$ as $x$ varies over $[0, 1]$ is",
  r"$[-1, 3]$",
  [(r"$[0, 3]$", r"Evaluates $f \circ f$ only at the end points: $f(f(0)) = f(3) = 0$ and $f(f(1)) = f(0) = 3$."),
   (r"$[-1, 8]$", r"Takes the range of $f$ as $[-1, 3]$ using the vertex at $x = 2$, which is outside $[0, 1]$, then applies $f$ to $[-1, 3]$."),
   (r"$[-1, \infty)$", r"Ignores the restriction $x \in [0, 1]$ and gives the range of $f(f(x))$ over all real $x$.")],
  r"On $[0, 1]$, $f$ is decreasing (vertex at $x = 2$), so $f([0, 1]) = [f(1), f(0)] = [0, 3]$. Now $f$ on $[0, 3]$ has its vertex $x = 2$ inside, giving minimum $f(2) = -1$ and maximum $f(0) = 3$ (since $f(3) = 0$). Since $f$ is defined for all real numbers, $f(f(x))$ is defined for every $x \in [0, 1]$, and the set of values it takes is $[-1, 3]$.",
  r"Mapping only end points through a composite when an inner image contains a turning point.",
  "U07-A-comp-range-interval", "Two-stage image of an interval with a turning point inside the second stage.",
  check=_c55, values=[Interval(-1, 3), Interval(0, 3), Interval(-1, 8), Interval(-1, oo)],
  cognitive="Analysis", source_class="XII")


def _c56():
    f0, fy = symbols('f0 fy')
    # x = y = 0: 2 f(0) = 2 f(0)^2, with f(0) != 0
    roots = [r for r in solve(2 * f0 - 2 * f0**2, f0) if r != 0]
    assert len(roots) == 1
    # x = 0: f(y) + f(-y) = 2 f(0) f(y)  =>  f(-y) = (2 f(0) - 1) f(y)
    f_minus_y = (2 * roots[0] - 1) * fy
    s1 = simplify(f_minus_y - fy) == 0
    s2 = parity(log((1 - X) / (1 + X)), [Rational(k, 10) for k in (1, 3, 5, 7, 9)]) == -1
    return (bool(s1), bool(s2))
q("U07-A-056", T_PAR, "Parity from a functional equation", "Difficult", "Statement-based MCQ",
  r"Statement I: If $f : \mathbb{R} \to \mathbb{R}$ satisfies $f(x + y) + f(x - y) = 2f(x)f(y)$ for all real $x, y$ and $f(0) \ne 0$, then $f$ is an even function. Statement II: The function $g(x) = \log_e\left(\frac{1 - x}{1 + x}\right)$, $-1 < x < 1$, is an odd function." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Rejects Statement II, thinking $\log_e\left(\frac{1-x}{1+x}\right)$ is even because swapping $x$ to $-x$ only inverts the fraction."),
   (ST_FT, r"Rejects Statement I, likening the relation to a sine addition formula and concluding $f$ is odd."),
   (ST_FF, r"Makes both slips: calls $f$ odd and $g$ even.")],
  r"Put $x = y = 0$: $2f(0) = 2f(0)^2$, and $f(0) \ne 0$ gives $f(0) = 1$. Put $x = 0$: $f(y) + f(-y) = 2f(0)f(y) = 2f(y)$, so $f(-y) = f(y)$; Statement I is true. For $g$: $g(-x) = \log_e\frac{1 + x}{1 - x} = -\log_e\frac{1 - x}{1 + x} = -g(x)$ on the symmetric interval $(-1, 1)$; Statement II is true.",
  r"Thinking that inverting the argument of a logarithm leaves its value unchanged.",
  "U07-A-stmt-functional-parity", "Substitution in a functional equation plus a log parity check.",
  check=_c56, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Analysis", source_class="XII")
