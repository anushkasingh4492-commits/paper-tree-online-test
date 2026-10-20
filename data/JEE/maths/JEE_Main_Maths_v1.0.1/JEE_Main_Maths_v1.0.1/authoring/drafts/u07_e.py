import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from sympy.calculus.util import maximum, minimum

x = Symbol('x', real=True)
t = Symbol('t', real=True)
k = Symbol('k', real=True)
a = Symbol('a', real=True)
b = Symbol('b', real=True)
xp = Symbol('xp', positive=True)
xn = Symbol('xn', negative=True)

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_RATE = "Rate of change of quantities"
TOP_MONO = "Increasing and decreasing functions"
TOP_EXT = "Local maxima and minima"
TOP_ABS = "Absolute extrema on a closed interval"
TOP_OPT = "Optimisation problems"
XII = "XII"


def _ext_count(f, pts, h=Rational(1, 1000)):
    """Number of points in pts at which f has a strict local extremum (two-sided comparison)."""
    cnt = 0
    for c in pts:
        fc = N(f.subs(x, c), 30)
        l = N(f.subs(x, c - h), 30)
        r = N(f.subs(x, c + h), 30)
        if (l < fc and r < fc) or (l > fc and r > fc):
            cnt += 1
    return cnt


def _abs_vals(f, lo, hi, extra=()):
    """Values of f at endpoints, interior stationary points and extra points in [lo, hi]."""
    pts = {lo, hi}
    for c in solveset(diff(f, x), x, Interval.open(lo, hi)):
        pts.add(c)
    for c in extra:
        if lo <= c <= hi:
            pts.add(c)
    return [simplify(f.subs(x, c)) for c in pts]


def _opt_crit(f, v, dom):
    crit = list(solveset(diff(f, v), v, dom))
    return crit


# ================================================================ EASY
# ---------------------------------------------------------------- 001
def _c001():
    r = Symbol('r', positive=True)
    A = pi*r**2
    return diff(A, r).subs(r, 6)*2
q("U07-E-001", TOP_RATE, "Rate of change of area of a circle", "Easy", "Single-step computation MCQ",
  r"The radius of a circular oil patch increases at the rate of $2$ cm/s. The rate (in cm$^2$/s) at which its area is increasing when the radius is $6$ cm is",
  r"$24\pi$",
  [(r"$12\pi$", r"Uses $\frac{dA}{dr} = \pi r$, dropping the factor $2$ from $\frac{d}{dr}(r^2)$: $\pi(6)(2) = 12\pi$."),
   (r"$4\pi$", r"Finds the rate of change of the circumference, $2\pi\frac{dr}{dt} = 2\pi(2) = 4\pi$."),
   (r"$72\pi$", r"Multiplies the area $\pi(6)^2 = 36\pi$ by the rate $2$ without differentiating.")],
  r"$A = \pi r^2$, so $\frac{dA}{dt} = 2\pi r\frac{dr}{dt} = 2\pi(6)(2) = 24\pi$ cm$^2$/s.",
  r"Not applying the power rule correctly to $r^2$ while using the chain rule.",
  "U07-E-rate-circle-area", "One chain-rule step with one substitution.",
  check=_c001, values=[24*pi, 12*pi, 4*pi, 72*pi], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 002
def _c002():
    r = Symbol('r', positive=True)
    V = Rational(4, 3)*pi*r**3
    return diff(V, r).subs(r, 4)*Rational(1, 2)
q("U07-E-002", TOP_RATE, "Rate of change of volume of a sphere", "Easy", "Single-step computation MCQ",
  r"The radius of a spherical soap bubble is increasing at the rate of $\frac{1}{2}$ cm/s. The rate (in cm$^3$/s) at which its volume is increasing when the radius is $4$ cm is",
  r"$32\pi$",
  [(r"$64\pi$", r"Computes $\frac{dV}{dr} = 4\pi r^2 = 64\pi$ and does not multiply by $\frac{dr}{dt} = \frac{1}{2}$."),
   (r"$16\pi$", r"Finds the rate of change of surface area, $8\pi r\frac{dr}{dt} = 8\pi(4)\left(\frac{1}{2}\right) = 16\pi$."),
   (r"$\frac{128\pi}{3}$", r"Multiplies the volume $\frac{4}{3}\pi(4)^3 = \frac{256\pi}{3}$ by $\frac{1}{2}$ without differentiating.")],
  r"$V = \frac{4}{3}\pi r^3$ gives $\frac{dV}{dt} = 4\pi r^2\frac{dr}{dt} = 4\pi(16)\left(\frac{1}{2}\right) = 32\pi$ cm$^3$/s.",
  "Stopping at $dV/dr$ and not multiplying by the given rate $dr/dt$.",
  "U07-E-rate-sphere-volume", "One chain-rule step with given rate.",
  check=_c002, values=[32*pi, 64*pi, 16*pi, Rational(128, 3)*pi], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 003
def _c003():
    s = Symbol('s', positive=True)
    S = 6*s**2
    return diff(S, s).subs(s, 10)*3
q("U07-E-003", TOP_RATE, "Rate of change of surface area of a cube", "Easy", "Single-step computation MCQ",
  r"Each edge of a metal cube expands at the rate of $3$ cm/s when heated. The rate (in cm$^2$/s) at which its total surface area increases when the edge is $10$ cm is",
  r"$360$",
  [(r"$900$", r"Finds the rate of change of volume instead: $3s^2\frac{ds}{dt} = 3(100)(3) = 900$."),
   (r"$180$", r"Differentiates $6s^2$ as $6s$, missing the power-rule factor $2$: $6(10)(3) = 180$."),
   (r"$120$", r"Computes $\frac{dS}{ds} = 12s = 120$ and does not multiply by $\frac{ds}{dt} = 3$.")],
  r"$S = 6s^2$, so $\frac{dS}{dt} = 12s\frac{ds}{dt} = 12(10)(3) = 360$ cm$^2$/s.",
  "Mixing up the volume and surface-area formulas of a cube, or omitting the chain-rule factor.",
  "U07-E-rate-cube-surface", "Single chain-rule substitution.",
  check=_c003, values=[360, 900, 180, 120], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Each edge of a metal cube expands at the rate of $3$ cm/s when heated. The rate (in cm$^2$/s) at which its total surface area increases when the edge is $10$ cm is", answer=360))

# ---------------------------------------------------------------- 004
def _c004():
    f = x**3 - 12*x
    return solve_univariate_inequality(diff(f, x) < 0, x, relational=False)
q("U07-E-004", TOP_MONO, "Interval of decrease of a cubic", "Easy", "Single-step computation MCQ",
  r"The largest open interval on which $f(x) = x^3 - 12x$ is strictly decreasing is",
  r"$(-2, 2)$",
  [(r"$(-2\sqrt{3}, 2\sqrt{3})$", r"Writes $3x^2 - 12 < 0$ as $x^2 < 12$, not dividing the constant by $3$."),
   (r"$(0, 2)$", r"Takes only the positive root of $x^2 = 4$ and starts the interval at $0$."),
   (r"$(-\infty, 2)$", r"Solves $x^2 < 4$ as $x < 2$, taking the square root on one side only.")],
  r"$f'(x) = 3x^2 - 12 = 3(x-2)(x+2)$, which is negative exactly when $-2 < x < 2$. So $f$ is strictly decreasing on $(-2, 2)$ and increasing outside it.",
  r"Solving the quadratic inequality $x^2 < 4$ incorrectly.",
  "U07-E-decr-cubic-basic", "One derivative and one quadratic inequality.",
  check=_c004, values=[Interval.open(-2, 2), Interval.open(-2*sqrt(3), 2*sqrt(3)), Interval.open(0, 2), Interval.open(-oo, 2)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 005
def _c005():
    f = x**2*exp(-x)
    return solve_univariate_inequality(diff(f, x) > 0, x, relational=False)
q("U07-E-005", TOP_MONO, "Interval of increase of a product with an exponential", "Easy", "Single-step computation MCQ",
  r"The largest open interval on which $f(x) = x^2 e^{-x}$ is strictly increasing is",
  r"$(0, 2)$",
  [(r"$(-\infty, 2)$", r"Writes $f'(x) = xe^{-x}(2 - x)$ but ignores the factor $x$, solving only $2 - x > 0$."),
   (r"$(0, \infty)$", r"Uses only the first product-rule term, $f'(x) = 2xe^{-x}$, which is positive for all $x > 0$."),
   (r"$(2, \infty)$", r"Reads the sign chart of $x(2-x)$ the wrong way round and takes the right-hand region where $f' < 0$.")],
  r"$f'(x) = 2xe^{-x} - x^2e^{-x} = x(2 - x)e^{-x}$. Since $e^{-x} > 0$, $f'(x) > 0$ exactly when $x(2-x) > 0$, that is $0 < x < 2$.",
  "Dropping a factor of the derivative or a product-rule term when finding its sign.",
  "U07-E-incr-poly-exp", "Product rule followed by a two-factor sign check.",
  check=_c005, values=[Interval.open(0, 2), Interval.open(-oo, 2), Interval.open(0, oo), Interval.open(2, oo)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 006
def _c006():
    f = x + 4/x
    crit = solve(diff(f, x), x)
    mx = [c for c in crit if diff(f, x, 2).subs(x, c) < 0]
    return f.subs(x, mx[0])
q("U07-E-006", TOP_EXT, "Local maximum value smaller than local minimum value", "Easy", "Single-step computation MCQ",
  r"The local maximum value of $f(x) = x + \frac{4}{x}$, $x \ne 0$, is",
  r"$-4$",
  [(r"$4$", r"Reports the local minimum value $f(2) = 4$, assuming the larger value must be the maximum."),
   (r"$-2$", r"Reports the point $x = -2$ where the local maximum occurs, not the value."),
   (r"$2$", r"Reports the point $x = 2$, which is where the local minimum occurs.")],
  r"$f'(x) = 1 - \frac{4}{x^2} = 0$ gives $x = \pm 2$, and $f''(x) = \frac{8}{x^3}$ is negative at $x = -2$. So the local maximum value is $f(-2) = -2 - 2 = -4$, which is less than the local minimum value $f(2) = 4$.",
  "Believing a local maximum value must exceed every local minimum value.",
  "U07-E-localmax-below-localmin", "Two stationary points and a second-derivative sign.",
  check=_c006, values=[-4, 4, -2, 2], cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 007
def _c007():
    f = 2*x**3 - 3*x**2 - 12*x + 1
    v = _abs_vals(f, -2, 4)
    return Max(*v) - Min(*v)
q("U07-E-007", TOP_ABS, "Absolute extrema of a cubic on a closed interval", "Easy", "Multi-step computation MCQ",
  r"For $f(x) = 2x^3 - 3x^2 - 12x + 1$ on $[-2, 4]$, the difference between the absolute maximum value and the absolute minimum value of $f$ is",
  r"$52$",
  [(r"$27$", r"Uses only the stationary points: $f(-1) - f(2) = 8 - (-19) = 27$, ignoring the endpoints."),
   (r"$36$", r"Uses only the endpoints: $f(4) - f(-2) = 33 - (-3) = 36$, ignoring the stationary points."),
   (r"$14$", r"Adds the two values, $33 + (-19) = 14$, in place of subtracting.")],
  r"$f'(x) = 6x^2 - 6x - 12 = 6(x-2)(x+1)$, so the candidates are $x = -2, -1, 2, 4$ with $f = -3, 8, -19, 33$. The absolute maximum is $33$ and the absolute minimum is $-19$, so the difference is $52$.",
  "Comparing only stationary points or only endpoints on a closed interval.",
  "U07-E-absext-cubic-closed", "Four evaluations after one factorisation.",
  check=_c007, values=[52, 27, 36, 14], cognitive="Application", source_class=XII,
  numerical=dict(question=r"For $f(x) = 2x^3 - 3x^2 - 12x + 1$ on $[-2, 4]$, the absolute maximum value of $f$ minus the absolute minimum value of $f$ is", answer=52))

# ---------------------------------------------------------------- 008
def _c008():
    f = x**3 - 6*x**2 + 9*x + 4
    crit = solve(diff(f, x), x)
    return [c for c in crit if diff(f, x, 2).subs(x, c) > 0][0]
q("U07-E-008", TOP_EXT, "Point of local minimum of a cubic", "Easy", "Single-step computation MCQ",
  r"The function $f(x) = x^3 - 6x^2 + 9x + 4$ has a local minimum at $x$ equal to",
  r"$3$",
  [(r"$1$", r"Picks the other stationary point, $x = 1$, which is a local maximum since $f''(1) = -6 < 0$."),
   (r"$4$", r"Reports the local minimum value $f(3) = 4$ instead of the point."),
   (r"$2$", r"Solves $f''(x) = 6x - 12 = 0$, which gives the point of inflection.")],
  r"$f'(x) = 3x^2 - 12x + 9 = 3(x-1)(x-3)$ and $f''(x) = 6x - 12$. Since $f''(3) = 6 > 0$, the local minimum is at $x = 3$ (and $f''(1) < 0$ gives a local maximum at $x = 1$).",
  "Confusing the point of extremum with the extreme value, or with the inflection point.",
  "U07-E-localmin-point-cubic", "Factorise $f'$ and apply the second-derivative test.",
  check=_c008, values=[3, 1, 4, 2], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 009
def _c009():
    s = Symbol('s', positive=True)
    A = sqrt(3)/4*s**2
    return simplify(diff(A, s).subs(s, 10)*2)
q("U07-E-009", TOP_RATE, "Rate of change of area of an equilateral triangle", "Easy", "Single-step computation MCQ",
  r"Each side of an equilateral triangle increases at the rate of $2$ cm/s. The rate (in cm$^2$/s) at which its area increases when the side is $10$ cm is",
  r"$10\sqrt{3}$",
  [(r"$5\sqrt{3}$", r"Computes $\frac{dA}{ds} = \frac{\sqrt{3}}{2}s = 5\sqrt{3}$ and does not multiply by $\frac{ds}{dt} = 2$."),
   (r"$25\sqrt{3}$", r"Gives the area $\frac{\sqrt{3}}{4}(10)^2 = 25\sqrt{3}$ itself."),
   (r"$20\sqrt{3}$", r"Uses area $\frac{\sqrt{3}}{2}s^2$ (mixing in the altitude formula), so $\frac{dA}{dt} = \sqrt{3}s\frac{ds}{dt} = 20\sqrt{3}$.")],
  r"$A = \frac{\sqrt{3}}{4}s^2$, so $\frac{dA}{dt} = \frac{\sqrt{3}}{2}s\frac{ds}{dt} = \frac{\sqrt{3}}{2}(10)(2) = 10\sqrt{3}$ cm$^2$/s.",
  "Using a wrong area formula or omitting the given rate.",
  "U07-E-rate-equilateral-area", "Single chain-rule step.",
  check=_c009, values=[10*sqrt(3), 5*sqrt(3), 25*sqrt(3), 20*sqrt(3)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 010
def _c010():
    f = x**3
    neg = solveset(diff(f, x) < 0, x, S.Reals)
    zero = solveset(diff(f, x), x, S.Reals)
    s1 = bool(neg == S.EmptySet and isinstance(zero, FiniteSet))
    s2 = bool(diff(f, x).subs(x, 0) > 0)
    return (s1, s2)
q("U07-E-010", TOP_MONO, "Strict increase versus positive derivative", "Easy", "Statement-based MCQ",
  r"Statement I: The function $f(x) = x^3$ is strictly increasing on $\mathbb{R}$. Statement II: If a differentiable function is strictly increasing on an interval $I$, then its derivative is positive at every point of $I$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts the converse of the sufficient condition $f' > 0$; the example $x^3$ has $f'(0) = 0$ yet is strictly increasing."),
   (ST_FF, r"Thinks $f'(0) = 0$ stops $x^3$ from being strictly increasing, and also rejects Statement II."),
   (ST_FT, r"Treats $f' > 0$ everywhere as necessary for strict increase, so rejects Statement I because $f'(0) = 0$.")],
  r"$f'(x) = 3x^2 \ge 0$ with equality only at the single point $x = 0$, so $x^3$ is strictly increasing on $\mathbb{R}$; Statement I is true. The same function shows Statement II is false, since it is strictly increasing but $f'(0) = 0$.",
  r"Treating $f'(x) > 0$ as necessary, rather than sufficient, for strict increase.",
  "U07-E-stmt-strict-increase", "One standard counterexample.",
  check=_c010, values=[(T, F_), (T, T), (F_, F_), (F_, T)], cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 011
def _c011():
    m = minimum(diff(x**3 + k*x, x), x, S.Reals)
    return solve_univariate_inequality(m >= 0, k, relational=False)
q("U07-E-011", TOP_MONO, "Parameter for a cubic to be increasing", "Easy", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $f(x) = x^3 + kx$ is strictly increasing on $\mathbb{R}$ is",
  r"$[0, \infty)$",
  [(r"$(0, \infty)$", r"Demands $f'(x) > 0$ for every $x$ and so wrongly rejects $k = 0$, though $x^3$ is strictly increasing."),
   (r"$(-\infty, 0]$", r"Reverses the inequality, requiring $k \le 0$."),
   (r"$\mathbb{R}$", r"Assumes the $x^3$ term always dominates, so that every $k$ works; for $k < 0$, $f' < 0$ near $0$.")],
  r"$f'(x) = 3x^2 + k$ has minimum value $k$ (at $x = 0$). If $k > 0$ then $f' > 0$ everywhere; if $k = 0$ then $f' = 3x^2$ vanishes only at $x = 0$, so $f$ is still strictly increasing; if $k < 0$ then $f' < 0$ near $0$. Hence $k \in [0, \infty)$.",
  "Excluding the boundary value where the derivative vanishes at isolated points.",
  "U07-E-param-mono-cubic-linear", "Minimum of a simple quadratic and a boundary check.",
  check=_c011, values=[Interval(0, oo), Interval.open(0, oo), Interval(-oo, 0), S.Reals], cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 012
def _c012():
    return maximum(x*exp(-x), x, S.Reals)
q("U07-E-012", TOP_EXT, "Maximum value of x e^{-x}", "Easy", "Single-step computation MCQ",
  r"The maximum value of $f(x) = xe^{-x}$, $x \in \mathbb{R}$, is",
  r"$\frac{1}{e}$",
  [(r"$1$", r"Reports the point $x = 1$ where the maximum occurs instead of the value."),
   (r"$\frac{2}{e^2}$", r"Solves $f''(x) = (x-2)e^{-x} = 0$ and evaluates $f(2) = 2e^{-2}$."),
   (r"$e$", r"Finds $x = 1$ correctly but evaluates $1 \cdot e^{1}$, dropping the minus sign in the exponent.")],
  r"$f'(x) = e^{-x}(1 - x)$, positive for $x < 1$ and negative for $x > 1$. So $f$ has its maximum at $x = 1$, with value $\frac{1}{e}$.",
  "Confusing the point of maximum with the maximum value, or using $f'' = 0$.",
  "U07-E-max-xexp", "One derivative and a sign check.",
  check=_c012, values=[exp(-1), 1, 2*exp(-2), E], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 013
def _c013():
    r = Symbol('r', positive=True)
    V = Rational(4, 3)*pi*r**3
    dVdt = 18*pi
    return simplify(dVdt/diff(V, r).subs(r, Rational(6, 2)))
q("U07-E-013", TOP_RATE, "Rate of change of radius of a balloon", "Easy", "Single-step computation MCQ",
  r"Air is pumped into a spherical balloon so that its volume increases at the rate of $18\pi$ cm$^3$/s. The rate (in cm/s) at which the radius of the balloon increases when its diameter is $6$ cm is",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{8}$", r"Uses the diameter $6$ as the radius: $\frac{18\pi}{4\pi(36)} = \frac{1}{8}$."),
   (r"$1$", r"Gives the rate of increase of the diameter, $2 \cdot \frac{1}{2} = 1$."),
   (r"$\frac{3}{2}$", r"Takes $\frac{dV}{dr} = \frac{4}{3}\pi r^2 = 12\pi$, missing the factor $3$ from $r^3$: $\frac{18\pi}{12\pi} = \frac{3}{2}$.")],
  r"Here $r = 3$. From $V = \frac{4}{3}\pi r^3$, $\frac{dV}{dt} = 4\pi r^2\frac{dr}{dt}$, so $18\pi = 4\pi(9)\frac{dr}{dt}$ and $\frac{dr}{dt} = \frac{1}{2}$ cm/s.",
  "Substituting the diameter for the radius.",
  "U07-E-rate-balloon-radius", "Reverse use of one chain-rule relation.",
  check=_c013, values=[Rational(1, 2), Rational(1, 8), 1, Rational(3, 2)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 014
def _c014():
    f = sin(x) + sqrt(3)*cos(x)
    return Min(*_abs_vals(f, 0, pi/2))
q("U07-E-014", TOP_ABS, "Absolute minimum of a trigonometric sum", "Easy", "Single-step computation MCQ",
  r"The absolute minimum value of $f(x) = \sin x + \sqrt{3}\cos x$ on $\left[0, \frac{\pi}{2}\right]$ is",
  r"$1$",
  [(r"$\sqrt{3}$", r"Checks only the left endpoint $f(0) = \sqrt{3}$ and the stationary point."),
   (r"$-2$", r"Uses the minimum $-2$ of $2\sin\left(x + \frac{\pi}{3}\right)$ over all of $\mathbb{R}$, ignoring the interval."),
   (r"$2$", r"Gives the absolute maximum $f\left(\frac{\pi}{6}\right) = 2$.")],
  r"$f'(x) = \cos x - \sqrt{3}\sin x = 0$ gives $x = \frac{\pi}{6}$, where $f = 2$. At the endpoints $f(0) = \sqrt{3}$ and $f\left(\frac{\pi}{2}\right) = 1$. The absolute minimum is $1$.",
  "Ignoring the restriction to the closed interval or not checking both endpoints.",
  "U07-E-absext-trig-sum", "Three evaluations after one stationary point.",
  check=_c014, values=[1, sqrt(3), -2, 2], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 015
def _c015():
    f = x**4 - 4*x**3
    return _ext_count(f, solve(diff(f, x), x))
q("U07-E-015", TOP_EXT, "Number of local extrema of a quartic", "Easy", "Conceptual/application MCQ",
  r"The number of points at which $f(x) = x^4 - 4x^3$ has a local maximum or a local minimum is",
  r"$1$",
  [(r"$2$", r"Counts both stationary points $x = 0$ and $x = 3$, not noticing that $f'$ does not change sign at $x = 0$."),
   (r"$3$", r"Counts the roots of $f'(x) = 4x^2(x - 3)$ with multiplicity."),
   (r"$0$", r"Concludes that the squared factor in $f'(x) = 4x^2(x-3)$ keeps $f'$ of one sign, so that no extremum exists.")],
  r"$f'(x) = 4x^3 - 12x^2 = 4x^2(x - 3)$. The factor $x^2$ does not change sign at $0$, so $f' < 0$ on both sides of $0$ and there is no extremum there. At $x = 3$, $f'$ changes from negative to positive, a local minimum. So there is exactly $1$ such point.",
  "Treating every stationary point as an extremum.",
  "U07-E-count-extrema-stationary", "One factorisation and a sign-change check.",
  check=_c015, values=[1, 2, 3, 0], cognitive="Understanding", source_class=XII,
  numerical=dict(question=r"The number of points at which $f(x) = x^4 - 4x^3$ has a local maximum or a local minimum is", answer=1))

# ---------------------------------------------------------------- 016
def _c016():
    m = maximum(sin(x), x, S.Reals)
    return Interval(m, oo)
q("U07-E-016", TOP_MONO, "Parameter for a trigonometric function to be increasing", "Easy", "Inverse/parameter MCQ",
  r"The set of all real $a$ for which $f(x) = ax + \cos x$ is strictly increasing on $\mathbb{R}$ is",
  r"$[1, \infty)$",
  [(r"$(1, \infty)$", r"Rejects $a = 1$, though then $f'(x) = 1 - \sin x$ vanishes only at isolated points and $f$ is still strictly increasing."),
   (r"$[-1, \infty)$", r"Compares $a$ with the minimum of $\sin x$ instead of its maximum."),
   (r"$(-\infty, -1]$", r"Writes the condition as $a \le \sin x$ for all $x$, the condition for decrease.")],
  r"$f'(x) = a - \sin x \ge 0$ for all $x$ requires $a \ge \max \sin x = 1$. For $a = 1$, $f'(x) = 1 - \sin x$ is zero only at isolated points, so $f$ remains strictly increasing. Hence $a \in [1, \infty)$.",
  "Mishandling the boundary value of the parameter.",
  "U07-E-param-mono-trig", r"Bound of $\sin x$ plus a boundary check.",
  check=_c016, values=[Interval(1, oo), Interval.open(1, oo), Interval(-1, oo), Interval(-oo, -1)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 017
def _c017():
    L, W = Function('L')(t), Function('W')(t)
    A = L*W
    dA = diff(A, t).subs({Derivative(L, t): 3, Derivative(W, t): -2}).subs({L: 8, W: 6})
    return dA
q("U07-E-017", TOP_RATE, "Rate of change of area of a rectangle", "Easy", "Single-step computation MCQ",
  r"The length of a rectangle increases at $3$ cm/s while its width decreases at $2$ cm/s. When the length is $8$ cm and the width is $6$ cm, the area is changing at the rate (in cm$^2$/s, positive if increasing) of",
  r"$2$",
  [(r"$34$", r"Ignores the sign of the decreasing width: $3(6) + 8(2) = 34$."),
   (r"$12$", r"Pairs each rate with its own side: $3(8) + (-2)(6) = 12$."),
   (r"$-6$", r"Multiplies the two rates, $3 \times (-2) = -6$.")],
  r"$A = \ell w$, so $\frac{dA}{dt} = \frac{d\ell}{dt}w + \ell\frac{dw}{dt} = 3(6) + 8(-2) = 2$ cm$^2$/s; the area is increasing.",
  "Mishandling the product rule or the sign of a decreasing quantity.",
  "U07-E-rate-rectangle-product", "Product rule with one sign.",
  check=_c017, values=[2, 34, 12, -6], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The length of a rectangle increases at $3$ cm/s while its width decreases at $2$ cm/s. When the length is $8$ cm and the width is $6$ cm, the rate (in cm$^2$/s) at which the area is increasing is", answer=2))

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 018
def _c018():
    X, Y, Xd, Yd = symbols('X Y Xd Yd', real=True)
    # differentiate X^2 + Y^2 = 169 with respect to t: 2 X Xd + 2 Y Yd = 0
    yv = solve(Eq(25 + Y**2, 169), Y)
    yv = [v for v in yv if v > 0][0]
    sol = solve(Eq(2*X*Xd + 2*Y*Yd, 0).subs({X: 5, Y: yv, Xd: 2}), Yd)
    return -sol[0]
q("U07-E-018", TOP_RATE, "Sliding ladder", "Medium", "Multi-step computation MCQ",
  r"A ladder $13$ m long leans against a vertical wall. Its foot is pulled away from the wall along the level ground at $2$ m/s. The rate (in m/s) at which the top of the ladder slides down the wall when the foot is $5$ m from the wall is",
  r"$\frac{5}{6}$",
  [(r"$\frac{24}{5}$", r"Inverts the ratio, using $\frac{dy}{dt} = -\frac{y}{x}\frac{dx}{dt} = -\frac{12}{5}(2)$."),
   (r"$\frac{5}{12}$", r"Gets $\frac{dy}{dt} = -\frac{x}{y}\frac{dx}{dt}$ but omits the factor $\frac{dx}{dt} = 2$."),
   (r"$2$", r"Assumes the top moves down at the same rate as the foot moves out.")],
  r"With foot distance $x$ and height $y$, $x^2 + y^2 = 169$. When $x = 5$, $y = 12$. Differentiating, $x\frac{dx}{dt} + y\frac{dy}{dt} = 0$, so $\frac{dy}{dt} = -\frac{5(2)}{12} = -\frac{5}{6}$. The top slides down at $\frac{5}{6}$ m/s.",
  "Inverting the ratio of the legs in the related-rates equation.",
  "U07-E-rate-ladder", "Pythagoras, implicit differentiation, and substitution.",
  check=_c018, values=[Rational(5, 6), Rational(24, 5), Rational(5, 12), 2], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 019
def _c019():
    h = Symbol('h', positive=True)
    V = Rational(1, 3)*pi*(h/2)**2*h
    return simplify(9/diff(V, h).subs(h, 6))
q("U07-E-019", TOP_RATE, "Rate of rise of water in a conical tank", "Medium", "Multi-step computation MCQ",
  r"A tank is in the shape of a right circular cone with vertex downwards, height $10$ m and radius of the top $5$ m. Water is poured in at the rate of $9$ m$^3$/min. The rate (in m/min) at which the water level is rising when the depth of water is $6$ m is",
  r"$\frac{1}{\pi}$",
  [(r"$\frac{1}{3\pi}$", r"Uses $V = \pi r^2 h$ without the factor $\frac{1}{3}$, so $\frac{dV}{dh} = \frac{3\pi h^2}{4} = 27\pi$."),
   (r"$\frac{3}{\pi}$", r"Differentiates $\frac{\pi h^3}{12}$ as $\frac{\pi h^2}{12}$, missing the factor $3$, so $\frac{dV}{dh} = 3\pi$."),
   (r"$\frac{1}{16\pi}$", r"Inverts the similar-triangle ratio to $r = 2h$, so $V = \frac{4\pi h^3}{3}$ and $\frac{dV}{dh} = 144\pi$.")],
  r"By similar triangles $r = \frac{h}{2}$, so $V = \frac{1}{3}\pi\frac{h^2}{4}h = \frac{\pi h^3}{12}$. Then $\frac{dV}{dt} = \frac{\pi h^2}{4}\frac{dh}{dt}$, so $9 = \frac{36\pi}{4}\frac{dh}{dt} = 9\pi\frac{dh}{dt}$ and $\frac{dh}{dt} = \frac{1}{\pi}$ m/min.",
  "Not eliminating $r$ correctly using similar triangles.",
  "U07-E-rate-cone-depth", "Similar triangles, a volume formula and a chain rule.",
  check=_c019, values=[1/pi, 1/(3*pi), 3/pi, 1/(16*pi)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 020
def _c020():
    X = Symbol('X', positive=True)
    s = Symbol('s', positive=True)
    sv = solve(Eq(Rational(6, 1)/(X + s), Rational(2, 1)/s), s)[0]
    tip = X + sv
    return diff(tip, X)*5
q("U07-E-020", TOP_RATE, "Speed of the tip of a shadow", "Medium", "Multi-step computation MCQ",
  r"A man $2$ m tall walks at $5$ km/h directly away from a lamp post whose lamp is $6$ m above the level ground. The speed (in km/h) at which the tip of his shadow moves along the ground is",
  r"$\frac{15}{2}$",
  [(r"$\frac{5}{2}$", r"Finds the rate of growth of the shadow's length, $\frac{ds}{dt} = \frac{1}{2}(5)$, not the speed of the tip."),
   (r"$\frac{20}{3}$", r"Writes $s = \frac{2}{6}x$ directly from the heights, so the tip is at $\frac{4x}{3}$ and moves at $\frac{20}{3}$."),
   (r"$\frac{5}{3}$", r"Uses $s = \frac{x}{3}$ and also reports only the shadow's growth rate.")],
  r"Let the man be $x$ from the post and his shadow have length $s$. Similar triangles give $\frac{6}{x+s} = \frac{2}{s}$, so $s = \frac{x}{2}$. The tip is at distance $x + s = \frac{3x}{2}$, which changes at $\frac{3}{2}(5) = \frac{15}{2}$ km/h.",
  "Confusing the rate of growth of the shadow with the speed of its tip.",
  "U07-E-rate-shadow-tip", "Similar triangles then a linear rate, with a target-quantity trap.",
  check=_c020, values=[Rational(15, 2), Rational(5, 2), Rational(20, 3), Rational(5, 3)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 021
def _c021():
    f = 3*x**4 - 8*x**3 - 6*x**2 + 24*x
    return solve_univariate_inequality(diff(f, x) < 0, x, relational=False)
q("U07-E-021", TOP_MONO, "Sign of the derivative of a quartic", "Medium", "Multi-step computation MCQ",
  r"If $f(x) = 3x^4 - 8x^3 - 6x^2 + 24x$, then the set of all real $x$ for which $f'(x) < 0$ is",
  r"$(-\infty, -1) \cup (1, 2)$",
  [(r"$(-1, 1) \cup (2, \infty)$", r"Reverses the sign chart and gives the set where $f'(x) > 0$."),
   (r"$(1, 2)$", r"Tests only between the positive roots and misses that all three factors are negative for $x < -1$."),
   (r"$(-\infty, -1)$", r"Tests only to the left of the smallest root and misses the bounded interval $(1, 2)$.")],
  r"$f'(x) = 12x^3 - 24x^2 - 12x + 24 = 12(x - 2)(x^2 - 1) = 12(x-2)(x-1)(x+1)$. The sign is negative for $x < -1$, positive on $(-1, 1)$, negative on $(1, 2)$ and positive for $x > 2$. So $f'(x) < 0$ exactly on $(-\infty, -1) \cup (1, 2)$.",
  "Incomplete sign chart for a cubic derivative with three roots.",
  "U07-E-decr-quartic-signchart", "Factorisation by grouping and a three-root sign chart.",
  check=_c021, values=[Union(Interval.open(-oo, -1), Interval.open(1, 2)), Union(Interval.open(-1, 1), Interval.open(2, oo)), Interval.open(1, 2), Interval.open(-oo, -1)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 022
def _c022():
    fp = diff(x**3 + a*x**2 + 3*x + 5, x)
    return solve_univariate_inequality(discriminant(fp, x) <= 0, a, relational=False)
q("U07-E-022", TOP_MONO, "Parameter range for a monotonic cubic", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $a$ for which $f(x) = x^3 + ax^2 + 3x + 5$ is strictly increasing on $\mathbb{R}$ is",
  r"$[-3, 3]$",
  [(r"$(-3, 3)$", r"Requires a strictly negative discriminant, rejecting $a = \pm 3$ where $f' = 3(x \pm 1)^2$ vanishes at one point only."),
   (r"$[-6, 6]$", r"Uses $f'(x) = 3x^2 + ax + 3$, forgetting the $2$ in $2ax$, so $a^2 - 36 \le 0$."),
   (r"$(-\infty, -3] \cup [3, \infty)$", r"Reverses the discriminant condition to $4a^2 - 36 \ge 0$.")],
  r"$f'(x) = 3x^2 + 2ax + 3$ must be $\ge 0$ for all $x$, which needs $4a^2 - 36 \le 0$, i.e. $-3 \le a \le 3$. At $a = \pm 3$, $f'(x) = 3(x \pm 1)^2$ vanishes at a single point, so $f$ is still strictly increasing. Hence $a \in [-3, 3]$.",
  "Excluding the boundary of the discriminant condition.",
  "U07-E-param-mono-cubic-disc", "Discriminant condition plus a boundary check.",
  check=_c022, values=[Interval(-3, 3), Interval.open(-3, 3), Interval(-6, 6), Union(Interval(-oo, -3), Interval(3, oo))],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 023
def _c023():
    m = maximum(diff(log(1 + x**2), x), x, S.Reals)
    return Interval(m, oo)
q("U07-E-023", TOP_MONO, "Parameter with a bounded derivative term", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $f(x) = kx - \log_e(1 + x^2)$ is strictly increasing on $\mathbb{R}$ is",
  r"$[1, \infty)$",
  [(r"$(1, \infty)$", r"Rejects $k = 1$, though then $f'(x) = \frac{(x-1)^2}{1+x^2}$ vanishes only at $x = 1$."),
   (r"$[-1, \infty)$", r"Compares $k$ with the minimum $-1$ of $\frac{2x}{1+x^2}$ instead of its maximum."),
   (r"$\left[\frac{1}{2}, \infty\right)$", r"Differentiates $\log_e(1+x^2)$ as $\frac{x}{1+x^2}$, dropping the $2$, whose maximum is $\frac{1}{2}$.")],
  r"$f'(x) = k - \frac{2x}{1 + x^2}$. Since $\frac{2x}{1+x^2}$ has maximum value $1$ (at $x = 1$), $f' \ge 0$ for all $x$ iff $k \ge 1$. For $k = 1$, $f'(x) = \frac{(x - 1)^2}{1 + x^2}$ is zero only at $x = 1$, so $f$ is strictly increasing. Hence $k \in [1, \infty)$.",
  r"Using the wrong bound of $\frac{2x}{1+x^2}$ or excluding the boundary.",
  "U07-E-param-mono-log", "Range of a rational expression and a boundary check.",
  check=_c023, values=[Interval(1, oo), Interval.open(1, oo), Interval(-1, oo), Interval(Rational(1, 2), oo)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 024
def _c024():
    A, B = symbols('A B', real=True)
    f = x**3 + A*x**2 + B*x
    sol = solve([diff(f, x).subs(x, -1), diff(f, x).subs(x, 3)], [A, B], dict=True)[0]
    g = f.subs(sol)
    pt = [c for c in [-1, 3] if diff(g, x, 2).subs(x, c) < 0][0]
    return g.subs(x, pt)
q("U07-E-024", TOP_EXT, "Coefficients from the points of extrema", "Medium", "Multi-step computation MCQ",
  r"The function $f(x) = x^3 + ax^2 + bx$ has its points of local extrema at $x = -1$ and $x = 3$. The local maximum value of $f$ is",
  r"$5$",
  [(r"$-27$", r"Gives $f(3) = -27$, which is the local minimum value."),
   (r"$11$", r"Takes the sum of roots of $3x^2 + 2ax + b$ as $\frac{2a}{3}$, getting $a = 3$, and then $f(-1) = -1 + 3 + 9 = 11$."),
   (r"$-1$", r"Takes the product of roots as $b$ instead of $\frac{b}{3}$, getting $b = -3$, and then $f(-1) = -1 - 3 + 3 = -1$.")],
  r"$f'(x) = 3x^2 + 2ax + b$ has roots $-1$ and $3$, so $-\frac{2a}{3} = 2$ and $\frac{b}{3} = -3$, giving $a = -3$, $b = -9$. Then $f''(x) = 6x - 6$ is negative at $x = -1$, so the local maximum value is $f(-1) = -1 - 3 + 9 = 5$.",
  "Sign or factor slips in Vieta's relations for the derivative.",
  "U07-E-localext-coeffs-from-points", "Vieta on $f'$, second-derivative test, evaluation.",
  check=_c024, values=[5, -27, 11, -1], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The function $f(x) = x^3 + ax^2 + bx$ has its points of local extrema at $x = -1$ and $x = 3$. The local maximum value of $f$ is", answer=5))

# ---------------------------------------------------------------- 025
def _c025():
    g = x**2 - 2*x - 3
    f = Abs(g)
    pts = {-2, 2}
    for c in list(solve(diff(g, x), x)) + list(solve(g, x)):
        if -2 <= c <= 2:
            pts.add(c)
    vals = [f.subs(x, c) for c in pts]
    return Max(*vals) + Min(*vals)
q("U07-E-025", TOP_ABS, "Absolute extrema with a modulus corner", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = |x^2 - 2x - 3|$ on $[-2, 2]$. The sum of the absolute maximum value and the absolute minimum value of $f$ on this interval is",
  r"$5$",
  [(r"$8$", r"Checks only the endpoints and the stationary point $x = 1$, getting minimum $3$ and missing $f(-1) = 0$ at the corner."),
   (r"$4$", r"Takes the vertex value $f(1) = 4$ as the maximum, missing $f(-2) = 5$, with minimum $0$."),
   (r"$1$", r"Drops the modulus and uses $x^2 - 2x - 3$, whose maximum $5$ and minimum $-4$ on the interval add to $1$.")],
  r"$x^2 - 2x - 3 = (x - 3)(x + 1)$ vanishes at $x = -1$ in the interval, where $f$ has a corner and $f = 0$. Other candidates: $f(-2) = 5$, $f(1) = 4$, $f(2) = 3$. So the maximum is $5$, the minimum is $0$, and the sum is $5$.",
  "Forgetting points where the function is not differentiable when finding absolute extrema.",
  "U07-E-absext-modulus-corner", "Candidates include a non-differentiable point; casework.",
  check=_c025, values=[5, 8, 4, 1], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"Let $f(x) = |x^2 - 2x - 3|$ on $[-2, 2]$. The sum of the absolute maximum value and the absolute minimum value of $f$ on this interval is", answer=5))

# ---------------------------------------------------------------- 026
def _c026():
    u = Symbol('u', positive=True)
    A = 2*u*sqrt(36 - u**2)
    crit = _opt_crit(A, u, Interval.open(0, 6))
    return Max(*[simplify(A.subs(u, c)) for c in crit])
q("U07-E-026", TOP_OPT, "Largest rectangle in a semicircle", "Medium", "Multi-step computation MCQ",
  r"A rectangle is inscribed in a semicircle of radius $6$ cm with one side along the diameter. The maximum possible area (in cm$^2$) of the rectangle is",
  r"$36$",
  [(r"$72$", r"Uses the result $2r^2$ for a rectangle inscribed in a full circle."),
   (r"$18$", r"Takes the base as $x$ instead of $2x$, maximising $x\sqrt{36 - x^2}$."),
   (r"$\frac{144}{5}$", r"Assumes the best rectangle is a square, with $s^2 + \frac{s^2}{4} = 36$.")],
  r"Let the rectangle have base $2x$ and height $\sqrt{36 - x^2}$, so $A = 2x\sqrt{36 - x^2}$. Maximising $A^2 = 4x^2(36 - x^2)$ gives $x^2 = 18$, so $A = 2\sqrt{18}\cdot\sqrt{18} = 36$ cm$^2$.",
  "Setting up the base as half its true length, or assuming a square.",
  "U07-E-opt-rect-semicircle", "Model set-up plus one optimisation.",
  check=_c026, values=[36, 72, 18, Rational(144, 5)], cognitive="Application", source_class=XII,
  numerical=dict(question=r"A rectangle is inscribed in a semicircle of radius $6$ cm with one side along the diameter. The maximum possible area (in cm$^2$) of the rectangle is", answer=36))

# ---------------------------------------------------------------- 027
def _c027():
    u = Symbol('u', positive=True)
    V = u*(18 - 2*u)**2
    crit = _opt_crit(V, u, Interval.open(0, 9))
    return Max(*[V.subs(u, c) for c in crit])
q("U07-E-027", TOP_OPT, "Open box from a square sheet", "Medium", "Multi-step computation MCQ",
  r"An open box is made from a square sheet of side $18$ cm by cutting equal squares from the four corners and folding up the sides. The maximum possible volume (in cm$^3$) of the box is",
  r"$432$",
  [(r"$864$", r"Takes the base side as $18 - x$ instead of $18 - 2x$; maximising $x(18 - x)^2$ gives $x = 6$ and $864$."),
   (r"$\frac{729}{2}$", r"Differentiates $(18 - 2x)^2$ as $-2(18 - 2x)$, missing a factor $2$, which gives $x = \frac{9}{2}$ and $\frac{9}{2}\cdot 81$."),
   (r"$216$", r"Writes the volume as $x^2(18 - 2x)$, swapping the roles of height and base side; the maximum is at $x = 6$.")],
  r"With squares of side $x$ cut out, $V = x(18 - 2x)^2$ for $0 < x < 9$. $V'(x) = (18 - 2x)(18 - 6x) = 0$ gives $x = 3$ (since $x = 9$ gives zero volume). $V(3) = 3 \cdot 12^2 = 432$ cm$^3$.",
  "Wrong expression for the base side of the box.",
  "U07-E-opt-open-box", "Model, derivative and rejection of the endpoint root.",
  check=_c027, values=[432, 864, Rational(729, 2), 216], cognitive="Application", source_class=XII,
  numerical=dict(question=r"An open box is made from a square sheet of side $18$ cm by cutting equal squares from the four corners and folding up the sides. The maximum possible volume (in cm$^3$) of the box is", answer=432))

# ---------------------------------------------------------------- 028
def _c028():
    D2 = x**2 + (x**2 - 3)**2
    crit = solve(diff(D2, x), x)
    return sqrt(Min(*[D2.subs(x, c) for c in crit]))
q("U07-E-028", TOP_OPT, "Shortest distance from a point to a parabola", "Medium", "Multi-step computation MCQ",
  r"The shortest distance between the point $(0, 3)$ and the curve $y = x^2$ is",
  r"$\frac{\sqrt{11}}{2}$",
  [(r"$3$", r"Uses only the stationary point $x = 0$, the vertex, which is actually a local maximum of the distance."),
   (r"$\sqrt{3}$", r"Differentiates $(x^2 - 3)^2$ as $2x(x^2 - 3)$, missing a factor $2$, which gives $x^2 = 2$ and $D^2 = 3$."),
   (r"$\frac{11}{4}$", r"Finds the minimum of the squared distance and forgets to take the square root.")],
  r"For a point $(x, x^2)$, $D^2 = x^2 + (x^2 - 3)^2$. Then $\frac{d}{dx}D^2 = 2x + 4x(x^2 - 3) = 2x(2x^2 - 5) = 0$ gives $x = 0$ or $x^2 = \frac{5}{2}$. At $x^2 = \frac{5}{2}$, $D^2 = \frac{5}{2} + \frac{1}{4} = \frac{11}{4}$, smaller than $9$ at $x = 0$. So the shortest distance is $\frac{\sqrt{11}}{2}$.",
  "Accepting the first stationary point found without comparing values.",
  "U07-E-opt-distance-parabola", "Squared-distance function with a quartic and comparison.",
  check=_c028, values=[sqrt(11)/2, 3, sqrt(3), Rational(11, 4)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 029
def _c029():
    s = Symbol('s', positive=True)
    P = (60 - s)*s**3
    crit = _opt_crit(P, s, Interval.open(0, 60))
    return [c for c in crit if diff(P, s, 2).subs(s, c) < 0][0]
q("U07-E-029", TOP_OPT, "Maximising a product with a fixed sum", "Medium", "Single-step computation MCQ",
  r"Two positive numbers $x$ and $y$ satisfy $x + y = 60$. If $xy^3$ is to be maximum, then $y$ equals",
  r"$45$",
  [(r"$40$", r"Maximises $xy^2$ instead, which gives $y = \frac{2}{3}(60) = 40$."),
   (r"$30$", r"Assumes the numbers must be equal, as when maximising $xy$."),
   (r"$15$", r"Reports the value of $x$ instead of $y$.")],
  r"Substitute $x = 60 - y$: $P(y) = (60 - y)y^3$. Then $P'(y) = 180y^2 - 4y^3 = 4y^2(45 - y)$, which changes from positive to negative at $y = 45$. So $y = 45$ (and $x = 15$).",
  "Assuming equal parts maximise any product with a fixed sum.",
  "U07-E-opt-product-power", "One substitution and one derivative.",
  check=_c029, values=[45, 40, 30, 15], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Two positive numbers $x$ and $y$ satisfy $x + y = 60$. If $xy^3$ is maximum, then the value of $y$ is", answer=45))

# ---------------------------------------------------------------- 030
def _c030():
    f = x**3 - 3*x**2 + 3*x + 1
    s1 = _ext_count(f, solve(diff(f, x), x)) == 0
    h = x**3 - 12*x
    pts = [0, 4] + list(solveset(diff(h, x), x, Interval.open(0, 4)))
    best = max(pts, key=lambda c: N(h.subs(x, c)))
    s2 = (best == 4)
    return (bool(s1), bool(s2))
q("U07-E-030", TOP_EXT, "Extremum tests in two statements", "Medium", "Statement-based MCQ",
  r"Statement I: The function $f(x) = x^3 - 3x^2 + 3x + 1$ has no point of local maximum or local minimum on $\mathbb{R}$. Statement II: The absolute maximum value of $h(x) = x^3 - 12x$ on $[0, 4]$ is attained at $x = 4$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Treats the stationary point $x = 1$ of $f$ as an extremum and takes the stationary point $x = 2$ of $h$ as its maximum."),
   (ST_FT, r"Treats $x = 1$, where $f'(x) = 3(x-1)^2 = 0$, as a point of extremum."),
   (ST_TF, r"Assumes the absolute maximum of $h$ on $[0, 4]$ is at the stationary point $x = 2$, where $h$ is actually least.")],
  r"$f'(x) = 3(x - 1)^2 \ge 0$ does not change sign, so $f$ is strictly increasing and has no local extremum; Statement I is true. For $h$, $h'(x) = 3x^2 - 12$ gives $x = 2$ in $[0, 4]$ with $h(2) = -16$, while $h(0) = 0$ and $h(4) = 16$; the maximum $16$ is at $x = 4$, so Statement II is true.",
  "Equating stationary points with extrema, and ignoring endpoints.",
  "U07-E-stmt-extrema-endpoint", "Two separate checks, each needing a sign or endpoint test.",
  check=_c030, values=[(T, T), (F_, F_), (F_, T), (T, F_)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 031
def _c031():
    th = Function('th')(t)
    A = Rational(1, 2)*4*6*sin(th)
    dA = diff(A, t).subs(Derivative(th, t), Rational(1, 10)).subs(th, pi/3)
    return simplify(dA)
q("U07-E-031", TOP_RATE, "Rate of change of area with a changing angle", "Medium", "Single-step computation MCQ",
  r"Two sides of a triangle have fixed lengths $4$ cm and $6$ cm, and the angle between them increases at $\frac{1}{10}$ radian per second. The rate (in cm$^2$/s) at which the area of the triangle increases when this angle is $\frac{\pi}{3}$ is",
  r"$\frac{3}{5}$",
  [(r"$\frac{3\sqrt{3}}{5}$", r"Uses $\sin\frac{\pi}{3}$ in place of $\cos\frac{\pi}{3}$ after differentiating."),
   (r"$\frac{6}{5}$", r"Drops the $\frac{1}{2}$ in the area formula, using $A = 24\sin\theta$."),
   (r"$\frac{6\sqrt{3}}{5}$", r"Drops the $\frac{1}{2}$ and also uses $\sin\frac{\pi}{3}$ in place of $\cos\frac{\pi}{3}$.")],
  r"$A = \frac{1}{2}(4)(6)\sin\theta = 12\sin\theta$, so $\frac{dA}{dt} = 12\cos\theta\frac{d\theta}{dt} = 12\cdot\frac{1}{2}\cdot\frac{1}{10} = \frac{3}{5}$ cm$^2$/s.",
  r"Not differentiating $\sin\theta$ before substituting.",
  "U07-E-rate-triangle-angle", "Area formula with trigonometry and chain rule.",
  check=_c031, values=[Rational(3, 5), 3*sqrt(3)/5, Rational(6, 5), 6*sqrt(3)/5], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 032
def _c032():
    Y = Symbol('Y', real=True)
    xd = Symbol('xd', positive=True)
    # y^2 = 8x  =>  2 y y' = 8 x', with y' = 2 x'
    yv = solve(Eq(2*Y*(2*xd), 8*xd), Y)[0]
    return (yv**2/8, yv)
q("U07-E-032", TOP_RATE, "Point where coordinates change at related rates", "Medium", "Inverse/parameter MCQ",
  r"A particle moves along the curve $y^2 = 8x$ so that its $x$-coordinate is increasing. At the point where its $y$-coordinate is increasing twice as fast as its $x$-coordinate, the particle is at",
  r"$\left(\frac{1}{2}, 2\right)$",
  [(r"$(8, 8)$", r"Reverses the condition, taking $\frac{dx}{dt} = 2\frac{dy}{dt}$, which gives $y = 8$."),
   (r"$(2, 4)$", r"Differentiates $y^2$ as $y\frac{dy}{dt}$, missing the $2$, which gives $y = 4$."),
   (r"$\left(\frac{1}{2}, -2\right)$", r"Finds $x = \frac{1}{2}$ but takes the other point on the curve; at $y = -2$ the $y$-coordinate is decreasing.")],
  r"Differentiate: $2y\frac{dy}{dt} = 8\frac{dx}{dt}$. With $\frac{dy}{dt} = 2\frac{dx}{dt}$ and $\frac{dx}{dt} \ne 0$, we get $4y = 8$, so $y = 2$ and $x = \frac{y^2}{8} = \frac{1}{2}$.",
  "Setting up the rate condition the wrong way round.",
  "U07-E-rate-curve-coordinates", "Implicit differentiation with a reversed unknown.",
  check=_c032, values=[(Rational(1, 2), 2), (8, 8), (2, 4), (Rational(1, 2), -2)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 033
def _c033():
    f = Abs(x)**Rational(2, 3)*(5 - x)
    fpos = xp**Rational(2, 3)*(5 - xp)
    fneg = (-xn)**Rational(2, 3)*(5 - xn)
    pts = [0] + list(solve(diff(fpos, xp), xp)) + list(solve(diff(fneg, xn), xn))
    return _ext_count(f, pts)
q("U07-E-033", TOP_EXT, "Extrema including a cusp", "Medium", "Multi-step computation MCQ",
  r"The number of points at which $f(x) = x^{2/3}(5 - x)$, $x \in \mathbb{R}$, has a local maximum or a local minimum is",
  r"$2$",
  [(r"$1$", r"Solves only $f'(x) = 0$, finding $x = 2$, and misses the point $x = 0$ where $f'$ does not exist but changes sign."),
   (r"$3$", r"Also counts the zero $x = 5$ of $f$ as an extremum."),
   (r"$4$", r"Counts every notable point of the graph as an extremum: the zeros $x = 0$ and $x = 5$ of $f$, the stationary point $x = 2$, and the inflection point $x = -1$ where $f''(x) = -\frac{10}{9}x^{-4/3}(1 + x)$ vanishes and changes sign.")],
  r"For $x \ne 0$, $f'(x) = \frac{2}{3}x^{-1/3}(5 - x) - x^{2/3} = \frac{10 - 5x}{3x^{1/3}}$. Its sign is negative for $x < 0$, positive on $(0, 2)$ and negative for $x > 2$. So $x = 0$ (a cusp) is a local minimum and $x = 2$ is a local maximum: $2$ points.",
  "Ignoring critical points where the derivative does not exist.",
  "U07-E-count-extrema-cusp", "Derivative of a fractional power plus sign chart through a cusp.",
  check=_c033, values=[2, 1, 3, 4], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The number of points at which $f(x) = x^{2/3}(5 - x)$, $x \in \mathbb{R}$, has a local maximum or a local minimum is", answer=2))

# ---------------------------------------------------------------- 034
def _c034():
    f = x + 2*cos(x)
    vals = _abs_vals(f, 0, pi)
    return min(vals, key=lambda v: N(v))
q("U07-E-034", TOP_ABS, "Absolute minimum of a linear plus cosine function", "Medium", "Multi-step computation MCQ",
  r"The absolute minimum value of $f(x) = x + 2\cos x$ on $[0, \pi]$ is",
  r"$\frac{5\pi}{6} - \sqrt{3}$",
  [(r"$\pi - 2$", r"Compares only the endpoints $f(0) = 2$ and $f(\pi) = \pi - 2$."),
   (r"$2$", r"Takes the value at the left endpoint, assuming the cosine term dominates."),
   (r"$\frac{\pi}{6} + \sqrt{3}$", r"Gives the value at $x = \frac{\pi}{6}$, which is the absolute maximum.")],
  r"$f'(x) = 1 - 2\sin x = 0$ gives $x = \frac{\pi}{6}, \frac{5\pi}{6}$. Values: $f(0) = 2$, $f\left(\frac{\pi}{6}\right) = \frac{\pi}{6} + \sqrt{3}$, $f\left(\frac{5\pi}{6}\right) = \frac{5\pi}{6} - \sqrt{3} \approx 0.89$, $f(\pi) = \pi - 2 \approx 1.14$. The least is $\frac{5\pi}{6} - \sqrt{3}$.",
  "Not comparing every candidate value numerically.",
  "U07-E-absext-linear-trig", "Two stationary points and two endpoints compared.",
  check=_c034, values=[5*pi/6 - sqrt(3), pi - 2, 2, pi/6 + sqrt(3)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 035
def _c035():
    r, h = symbols('r h', positive=True)
    hv = (10 - 2*r - pi*r)/2
    A = 2*r*hv + pi*r**2/2
    return simplify(solve(diff(A, r), r)[0])
q("U07-E-035", TOP_OPT, "Window of maximum area", "Medium", "Multi-step computation MCQ",
  r"A window is in the form of a rectangle surmounted by a semicircle whose diameter is the top side of the rectangle. The perimeter of the window (the base, the two vertical sides and the semicircular arc) is $10$ m. For the window to admit the maximum light (maximum area), the radius (in m) of the semicircle must be",
  r"$\frac{10}{4 + \pi}$",
  [(r"$\frac{20}{4 + \pi}$", r"Reports the width $2r$ of the window instead of the radius."),
   (r"$\frac{5}{2 + \pi}$", r"Leaves the semicircle out of the area, maximising only $2rh$."),
   (r"$\frac{10}{8 + \pi}$", r"Also counts the common diameter in the perimeter, using $4r + 2h + \pi r = 10$.")],
  r"With radius $r$ and rectangle height $h$, $2r + 2h + \pi r = 10$, so $h = \frac{10 - 2r - \pi r}{2}$. Area $A = 2rh + \frac{\pi r^2}{2} = 10r - 2r^2 - \frac{\pi r^2}{2}$. $A'(r) = 10 - 4r - \pi r = 0$ gives $r = \frac{10}{4 + \pi}$, and $A'' < 0$.",
  "Wrong perimeter or area model for a composite figure.",
  "U07-E-opt-norman-window", "Composite figure model and one-variable optimisation.",
  check=_c035, values=[10/(4 + pi), 20/(4 + pi), 5/(2 + pi), 10/(8 + pi)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 036
def _c036():
    w = Symbol('w', positive=True)
    A = (600 - 2*w)*w
    crit = _opt_crit(A, w, Interval.open(0, 300))
    return Max(*[A.subs(w, c) for c in crit])
q("U07-E-036", TOP_OPT, "Fencing along a river", "Medium", "Multi-step computation MCQ",
  r"A rectangular plot lies along a straight river. Fencing is needed on the other three sides only, and $600$ m of fencing is available. The maximum area (in m$^2$) that can be enclosed is",
  r"$45000$",
  [(r"$22500$", r"Fences all four sides, giving a square of side $150$ m."),
   (r"$40000$", r"Assumes the three fenced sides are equal, each $200$ m."),
   (r"$90000$", r"Treats the $600$ m as covering one length and one width only, so $x + y = 600$ with $x = y = 300$.")],
  r"Let the two sides perpendicular to the river be $w$ and the side parallel be $600 - 2w$. Then $A = w(600 - 2w)$, $A'(w) = 600 - 4w = 0$ at $w = 150$. The maximum area is $150 \times 300 = 45000$ m$^2$.",
  "Using a symmetric guess instead of setting up the constraint correctly.",
  "U07-E-opt-fencing-river", "Constraint set-up and a quadratic maximum.",
  check=_c036, values=[45000, 22500, 40000, 90000], cognitive="Application", source_class=XII,
  numerical=dict(question=r"A rectangular plot lies along a straight river. Fencing is needed on the other three sides only, and $600$ m of fencing is available. The maximum area (in m$^2$) that can be enclosed is", answer=45000))

# ---------------------------------------------------------------- 037
def _c037():
    fp = diff(x**3 + 3*k*x**2 + 12*x + 1, x)
    return solve_univariate_inequality(discriminant(fp, x) > 0, k, relational=False)
q("U07-E-037", TOP_EXT, "Parameter for existence of local extrema", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which $f(x) = x^3 + 3kx^2 + 12x + 1$ has both a local maximum and a local minimum is",
  r"$(-\infty, -2) \cup (2, \infty)$",
  [(r"$(-\infty, -2] \cup [2, \infty)$", r"Includes $k = \pm 2$, where $f'(x) = 3(x \pm 2)^2$ does not change sign, so there is no extremum."),
   (r"$(-2, 2)$", r"Reverses the discriminant condition, which is the case of $f$ being strictly increasing."),
   (r"$[-2, 2]$", r"Uses the condition $36k^2 - 144 \le 0$ for monotonicity instead of the condition for extrema.")],
  r"$f'(x) = 3x^2 + 6kx + 12$ must have two distinct real roots so that it changes sign twice: $36k^2 - 144 > 0$, i.e. $|k| > 2$. At $|k| = 2$ the derivative is a perfect square and $f$ has no extremum.",
  "Allowing a repeated root of $f'$ to count as giving extrema.",
  "U07-E-param-extrema-existence", "Discriminant condition with strictness reasoning.",
  check=_c037, values=[Union(Interval.open(-oo, -2), Interval.open(2, oo)), Union(Interval(-oo, -2), Interval(2, oo)), Interval.open(-2, 2), Interval(-2, 2)],
  cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 038
def _c038():
    f = x - 2*sin(x)
    return solveset(diff(f, x) > 0, x, Interval.open(0, 2*pi))
q("U07-E-038", TOP_MONO, "Interval of increase of a trigonometric function", "Medium", "Single-step computation MCQ",
  r"The largest open interval contained in $(0, 2\pi)$ on which $f(x) = x - 2\sin x$ is strictly increasing is",
  r"$\left(\frac{\pi}{3}, \frac{5\pi}{3}\right)$",
  [(r"$\left(\frac{5\pi}{6}, 2\pi\right)$", r"Differentiates $\sin x$ as itself, so $f'(x) = 1 - 2\sin x > 0$ gives $\sin x < \frac{1}{2}$, i.e. $\left(0, \frac{\pi}{6}\right) \cup \left(\frac{5\pi}{6}, 2\pi\right)$, whose larger piece is $\left(\frac{5\pi}{6}, 2\pi\right)$."),
   (r"$\left(0, \frac{\pi}{3}\right)$", r"Reverses the inequality and solves $\cos x > \frac{1}{2}$, the condition for decrease."),
   (r"$\left(\frac{\pi}{3}, \pi\right)$", r"Solves $\cos x < \frac{1}{2}$ only within $[0, \pi]$, the principal range of $\cos^{-1}$.")],
  r"$f'(x) = 1 - 2\cos x > 0$ iff $\cos x < \frac{1}{2}$. In $(0, 2\pi)$ this holds exactly for $\frac{\pi}{3} < x < \frac{5\pi}{3}$.",
  "Solving a trigonometric inequality only over the principal range.",
  "U07-E-incr-trig", "One derivative plus a trigonometric inequality over a full period.",
  check=_c038, values=[Interval.open(pi/3, 5*pi/3), Interval.open(5*pi/6, 2*pi), Interval.open(0, pi/3), Interval.open(pi/3, pi)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 039
def _c039():
    g = log(x)/x
    # x^(1/x) = e^{g(x)}; g increases on (0, e) and decreases on (e, oo)
    assert solveset(diff(g, x), x, Interval.open(0, oo)) == FiniteSet(E)
    cands = [2, 3, 5, 7]
    best = max(cands, key=lambda n: N(g.subs(x, n), 30))
    return Integer(best)**Rational(1, best)
q("U07-E-039", TOP_MONO, "Comparing numbers using monotonicity", "Medium", "Conceptual/application MCQ",
  r"The greatest of the numbers $2^{1/2}$, $3^{1/3}$, $5^{1/5}$ and $7^{1/7}$ is",
  r"$3^{1/3}$",
  [(r"$2^{1/2}$", r"Assumes $x^{1/x}$ is decreasing for all $x > 0$, so the smallest base wins."),
   (r"$7^{1/7}$", r"Assumes $x^{1/x}$ is increasing, so the largest base wins."),
   (r"$5^{1/5}$", r"Compares the values of $\frac{\log_e x}{x}$ but uses $\log_e 5 \approx 2.3$ (confusing it with $\log_e 10$), so $\frac{\log_e 5}{5} \approx 0.46$ appears to exceed $\frac{\log_e 3}{3} \approx 0.37$, $\frac{\log_e 2}{2} \approx 0.35$ and $\frac{\log_e 7}{7} \approx 0.28$.")],
  r"Let $g(x) = \frac{\log_e x}{x}$, so $x^{1/x} = e^{g(x)}$. $g'(x) = \frac{1 - \log_e x}{x^2}$, so $g$ increases on $(0, e)$ and decreases on $(e, \infty)$. Hence $g(3) > g(5) > g(7)$, and $2^{1/2} = 4^{1/4}$ with $g(4) < g(3)$. The greatest is $3^{1/3}$.",
  r"Not using the turning point $x = e$ of $\frac{\log_e x}{x}$.",
  "U07-E-monotone-compare-roots", "Choosing an auxiliary function and using its monotonicity.",
  check=_c039, values=[3**Rational(1, 3), sqrt(2), 7**Rational(1, 7), 5**Rational(1, 5)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 040
def _c040():
    f = x**3 - 12*x + k
    vals = _abs_vals(f, 1, 5)
    # minimum over [1,5] occurs where f is least for every k (shift invariant)
    base = [v.subs(k, 0) for v in vals]
    mn = min(base, key=lambda v: N(v)); mx = max(base, key=lambda v: N(v))
    kv = solve(Eq(mn + k, -10), k)[0]
    return mx + kv
q("U07-E-040", TOP_ABS, "Parameter from the absolute minimum", "Medium", "Multi-step computation MCQ",
  r"The absolute minimum value of $f(x) = x^3 - 12x + k$ on $[1, 5]$ is $-10$. Then the absolute maximum value of $f$ on $[1, 5]$ is",
  r"$71$",
  [(r"$22$", r"Uses the local maximum value $f(-2) = 22$, although $x = -2$ lies outside $[1, 5]$."),
   (r"$66$", r"Takes the minimum at the endpoint $x = 1$: $k - 11 = -10$ gives $k = 1$, and then $f(5) = 66$."),
   (r"$6$", r"Finds $k = 6$ correctly and reports $f(0) = k$, though $0$ is not in the interval.")],
  r"$f'(x) = 3x^2 - 12 = 0$ gives $x = 2$ in $[1, 5]$. $f(1) = k - 11$, $f(2) = k - 16$, $f(5) = k + 65$, so the minimum is $k - 16 = -10$, giving $k = 6$. The maximum is $f(5) = 71$.",
  "Using a stationary point outside the given interval.",
  "U07-E-absext-param-from-min", "Find a parameter from one extreme, then the other extreme.",
  check=_c040, values=[71, 22, 66, 6], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The absolute minimum value of $f(x) = x^3 - 12x + k$ on $[1, 5]$ is $-10$. Then the absolute maximum value of $f$ on $[1, 5]$ is", answer=71))

# ---------------------------------------------------------------- 041
def _c041():
    r, rd = symbols('r rd', positive=True)
    hgt = 3
    rv = 3*hgt                      # height is one-third of the base radius
    V_rate = diff(pi*r**2*(r/3)/3, r)*rd   # dV/dt in terms of r and dr/dt
    rdv = solve(Eq(V_rate.subs(r, rv), 12), rd)[0]
    return simplify(diff(pi*r**2, r).subs(r, rv)*rdv)
q("U07-E-041", TOP_RATE, "Rate of growth of the base area of a sand pile", "Medium", "Multi-step computation MCQ",
  r"Sand is poured at the rate of $12$ cm$^3$/s and forms a conical pile whose height is always one-third of the radius of its base. The rate (in cm$^2$/s) at which the area of the base of the pile increases when the height of the pile is $3$ cm is",
  r"$8$",
  [(r"$\frac{8}{3}$", r"Uses $V = \pi r^2 h$ without the $\frac{1}{3}$, so $V = \frac{\pi r^3}{3}$, $12 = 81\pi\frac{dr}{dt}$ and $\frac{dA}{dt} = 18\pi\cdot\frac{4}{27\pi} = \frac{8}{3}$."),
   (r"$24$", r"Differentiates $\frac{\pi r^3}{9}$ as $\frac{\pi r^2}{9}$, missing the factor $3$, so $12 = 9\pi\frac{dr}{dt}$ and $\frac{dA}{dt} = 18\pi\cdot\frac{4}{3\pi} = 24$."),
   (r"$4$", r"Finds $\frac{dr}{dt} = \frac{4}{9\pi}$ correctly but differentiates $A = \pi r^2$ as $\pi r\frac{dr}{dt}$, missing the factor $2$: $9\pi\cdot\frac{4}{9\pi} = 4$.")],
  r"With $h = \frac{r}{3}$, $V = \frac{1}{3}\pi r^2\cdot\frac{r}{3} = \frac{\pi r^3}{9}$, so $\frac{dV}{dt} = \frac{\pi r^2}{3}\frac{dr}{dt}$. When $h = 3$, $r = 9$, so $12 = 27\pi\frac{dr}{dt}$ and $\frac{dr}{dt} = \frac{4}{9\pi}$. The base area $A = \pi r^2$ changes at $\frac{dA}{dt} = 2\pi r\frac{dr}{dt} = 18\pi\cdot\frac{4}{9\pi} = 8$ cm$^2$/s.",
  r"Stopping at $\frac{dr}{dt}$ or mishandling the second chain-rule step from $r$ to the base area.",
  "U07-E-rate-cone-base-area", "Two linked rates: volume to radius, then radius to base area.",
  check=_c041, values=[Integer(8), Rational(8, 3), Integer(24), Integer(4)], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Sand is poured at the rate of $12$ cm$^3$/s and forms a conical pile whose height is always one-third of the radius of its base. The rate (in cm$^2$/s) at which the area of the base of the pile increases when the height of the pile is $3$ cm is", answer=8))

# ---------------------------------------------------------------- 042
def _c042():
    s1 = _ext_count(x**3, [0]) == 1
    f = 4*x - x**2
    s2 = Max(*_abs_vals(f, 3, 5)) == 4
    return (bool(s1), bool(s2))
q("U07-E-042", TOP_EXT, "Necessary condition versus sufficient condition", "Medium", "Statement-based MCQ",
  r"Statement I: If $f$ is differentiable on $\mathbb{R}$ and $f'(c) = 0$, then $f$ has a local maximum or a local minimum at $x = c$. Statement II: The absolute maximum value of $g(x) = 4x - x^2$ on $[3, 5]$ is $4$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Treats $f'(c) = 0$ as sufficient for an extremum and uses the vertex value $g(2) = 4$ though $2 \notin [3, 5]$."),
   (ST_TF, r"Treats $f'(c) = 0$ as sufficient for an extremum, but correctly finds the maximum of $g$ is $g(3) = 3$."),
   (ST_FT, r"Rejects Statement I correctly but uses the vertex value $g(2) = 4$ outside the interval.")],
  r"Statement I is false: $f(x) = x^3$ has $f'(0) = 0$ but no extremum at $0$. Statement II is false: $g'(x) = 4 - 2x < 0$ on $[3, 5]$, so $g$ is decreasing there and its maximum is $g(3) = 3$, not $4$ (the vertex $x = 2$ is outside the interval).",
  "Treating $f'(c) = 0$ as sufficient, and using a vertex outside the interval.",
  "U07-E-stmt-necessary-vertex", "Two conceptual checks, each with a common trap.",
  check=_c042, values=[(F_, F_), (T, T), (T, F_), (F_, T)], cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 043
def _c043():
    f = a*log(Abs(x)) + b*x**2 + x
    fp = diff(f, x)
    sol = solve([fp.subs(x, -1), fp.subs(x, 2)], [a, b], dict=True)[0]
    return (sol[a], sol[b])
q("U07-E-043", TOP_EXT, "Coefficients of a log function from its extrema", "Medium", "Inverse/parameter MCQ",
  r"If $f(x) = a\log_e|x| + bx^2 + x$, $x \ne 0$, has extreme values at $x = -1$ and $x = 2$, then the ordered pair $(a, b)$ is",
  r"$\left(2, -\frac{1}{2}\right)$",
  [(r"$\left(2, -1\right)$", r"Differentiates $bx^2$ as $bx$, so the equations become $-a - b + 1 = 0$ and $\frac{a}{2} + 2b + 1 = 0$."),
   (r"$\left(-\frac{6}{5}, -\frac{1}{10}\right)$", r"Uses $\frac{d}{dx}\log_e|x| = \frac{1}{|x|}$, so at $x = -1$ writes $a - 2b + 1 = 0$."),
   (r"$\left(2, \frac{1}{2}\right)$", r"Sets up the equations correctly but drops the minus sign when solving $3b = -\frac{3}{2}$, while keeping $a = 2$.")],
  r"$f'(x) = \frac{a}{x} + 2bx + 1$ for $x \ne 0$. $f'(-1) = 0$ gives $-a - 2b + 1 = 0$ and $f'(2) = 0$ gives $\frac{a}{2} + 4b + 1 = 0$. Substituting $a = 1 - 2b$: $\frac{1}{2} - b + 4b + 1 = 0$, so $b = -\frac{1}{2}$ and $a = 2$.",
  r"Mis-differentiating $\log_e|x|$ for negative $x$.",
  "U07-E-param-log-extrema", r"Derivative of $\log_e|x|$ and a $2 \times 2$ linear system.",
  check=_c043, values=[(2, Rational(-1, 2)), (2, -1), (Rational(-6, 5), Rational(-1, 10)), (2, Rational(1, 2))],
  cognitive="Application", source_class=XII)

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 044
def _c044():
    f = (a + 2)*x**3 - 3*a*x**2 + 9*a*x - 1
    fp = expand(diff(f, x))
    lead = Poly(fp, x).coeff_monomial(x**2)
    s1 = solve_univariate_inequality(lead < 0, a, relational=False)
    s2 = solve_univariate_inequality(discriminant(fp, x) <= 0, a, relational=False)
    res = Intersection(s1, s2)
    # a = -2 makes f' linear, never non-positive everywhere; already excluded by lead < 0
    assert not (fp.subs(a, -2) <= 0) == True
    return res
q("U07-E-044", TOP_MONO, "Parameter for a cubic to be decreasing everywhere", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $a$ for which $f(x) = (a + 2)x^3 - 3ax^2 + 9ax - 1$ is strictly decreasing on $\mathbb{R}$ is",
  r"$(-\infty, -3]$",
  [(r"$(-\infty, -3] \cup [0, \infty)$", r"Uses only the discriminant condition $a^2 + 3a \ge 0$ and forgets that the leading coefficient $3(a+2)$ must be negative."),
   (r"$(-\infty, -2)$", r"Uses only the leading-coefficient condition $a + 2 < 0$ and ignores the discriminant."),
   (r"$[-3, 0]$", r"Reverses the discriminant condition to $a^2 + 3a \le 0$ and ignores the leading coefficient.")],
  r"$f'(x) = 3(a + 2)x^2 - 6ax + 9a$. For $a = -2$ it is $12x - 18$, which is positive for large $x$. Otherwise we need $a + 2 < 0$ and discriminant $36a^2 - 108a(a + 2) \le 0$, i.e. $-72a(a + 3) \le 0$, i.e. $a \le -3$ or $a \ge 0$. Together with $a < -2$ this gives $a \le -3$; at $a = -3$, $f'(x) = -3(x - 3)^2$ vanishes only at one point. Hence $a \in (-\infty, -3]$.",
  "Forgetting the sign of the leading coefficient of the quadratic derivative.",
  "U07-E-param-decr-leading-coeff", "Two simultaneous conditions, a degenerate case and boundary check.",
  check=_c044, values=[Interval(-oo, -3), Union(Interval(-oo, -3), Interval(0, oo)), Interval.open(-oo, -2), Interval(-3, 0)],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 045
def _c045():
    R = Symbol('R', positive=True)
    h = Symbol('h', positive=True)
    V = Rational(1, 3)*pi*h*(2*R - h)*h
    crit = _opt_crit(V, h, Interval.open(0, 2*R))
    Vmax = Max(*[V.subs(h, c) for c in crit])
    return simplify(Vmax/(Rational(4, 3)*pi*R**3))
q("U07-E-045", TOP_OPT, "Largest cone in a sphere", "Difficult", "Multi-step computation MCQ",
  r"A right circular cone is inscribed in a sphere of radius $R$ (its vertex and the circle of its base lie on the sphere). The ratio of the maximum possible volume of the cone to the volume of the sphere is",
  r"$\frac{8}{27}$",
  [(r"$\frac{8}{9}$", r"Uses cone volume $\pi r^2 h$ without the $\frac{1}{3}$."),
   (r"$\frac{\sqrt{3}}{18}$", r"Places the vertex at the centre, using $r^2 = R^2 - h^2$; the maximum is then at $h = \frac{R}{\sqrt{3}}$."),
   (r"$\frac{\sqrt{3}}{3}$", r"Uses the known ratio for the largest inscribed cylinder, $\frac{1}{\sqrt{3}}$.")],
  r"If the cone has height $h$ and base radius $r$, the chord geometry gives $r^2 = h(2R - h)$, so $V = \frac{\pi}{3}h^2(2R - h)$. $V'(h) = \frac{\pi}{3}(4Rh - 3h^2) = 0$ gives $h = \frac{4R}{3}$, so $V = \frac{\pi}{3}\cdot\frac{16R^2}{9}\cdot\frac{2R}{3} = \frac{32\pi R^3}{81}$. Dividing by $\frac{4}{3}\pi R^3$ gives $\frac{8}{27}$.",
  "Setting up the radius-height relation of the inscribed cone wrongly.",
  "U07-E-opt-cone-in-sphere", "Geometry set-up, optimisation and a ratio.",
  check=_c045, values=[Rational(8, 27), Rational(8, 9), sqrt(3)/18, sqrt(3)/3], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 046
def _c046():
    s = Symbol('s', positive=True)
    A = (s/4)**2 + (20 - s)**2/(4*pi)
    crit = _opt_crit(A, s, Interval.open(0, 20))
    c = crit[0]
    assert diff(A, s, 2).subs(s, c) > 0
    return simplify(c)
q("U07-E-046", TOP_OPT, "Wire cut into a square and a circle", "Difficult", "Multi-step computation MCQ",
  r"A wire of length $20$ cm is cut into two pieces. One piece is bent into a square and the other into a circle. If the sum of the areas of the square and the circle is to be minimum, the length (in cm) of the piece bent into the square is",
  r"$\frac{80}{\pi + 4}$",
  [(r"$\frac{20\pi}{\pi + 4}$", r"Reports the length of the piece used for the circle."),
   (r"$\frac{40}{\pi + 2}$", r"Differentiates the square's area $\frac{s^2}{16}$ as $\frac{s}{4}$ instead of $\frac{s}{8}$."),
   (r"$10$", r"Assumes the minimum occurs when the wire is cut into equal halves.")],
  r"If the square uses length $s$, total area $A = \frac{s^2}{16} + \frac{(20 - s)^2}{4\pi}$. $A'(s) = \frac{s}{8} - \frac{20 - s}{2\pi} = 0$ gives $\pi s = 4(20 - s)$, so $s = \frac{80}{\pi + 4}$. Since $A'' = \frac{1}{8} + \frac{1}{2\pi} > 0$, this is the minimum.",
  "Symmetry guess or wrong area derivative in a two-shape problem.",
  "U07-E-opt-wire-square-circle", "Two area formulas in terms of one variable, then a minimum.",
  check=_c046, values=[80/(pi + 4), 20*pi/(pi + 4), 40/(pi + 2), 10], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 047
def _c047():
    D = sqrt((30 - 15*t)**2 + (20*t)**2)
    return simplify(diff(D, t).subs(t, 1))
q("U07-E-047", TOP_RATE, "Rate of change of distance between two ships", "Difficult", "Multi-step computation MCQ",
  r"At noon, ship P is $30$ km due west of ship Q. Ship P sails due east at $15$ km/h and ship Q sails due north at $20$ km/h. The rate (in km/h) at which the distance between the ships is changing at $1$ pm (positive if increasing) is",
  r"$7$",
  [(r"$25$", r"Combines the speeds as perpendicular velocities, $\sqrt{15^2 + 20^2} = 25$, ignoring the geometry."),
   (r"$35$", r"Adds the two speeds."),
   (r"$-15$", r"Evaluates the derivative at noon ($t = 0$) instead of at $1$ pm.")],
  r"Take Q's start as origin. After $t$ hours P is at $(-30 + 15t, 0)$ and Q at $(0, 20t)$, so $D^2 = (30 - 15t)^2 + (20t)^2$. Then $D\frac{dD}{dt} = -15(30 - 15t) + 400t$. At $t = 1$: $D = \sqrt{225 + 400} = 25$ and $D\frac{dD}{dt} = -225 + 400 = 175$, so $\frac{dD}{dt} = 7$ km/h.",
  "Combining speeds directly instead of differentiating the distance.",
  "U07-E-rate-two-ships", "Coordinate set-up, implicit differentiation, sign of a closing component.",
  check=_c047, values=[7, 25, 35, -15], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"At noon, ship P is $30$ km due west of ship Q. Ship P sails due east at $15$ km/h and ship Q sails due north at $20$ km/h. The rate (in km/h) at which the distance between the ships is increasing at $1$ pm is", answer=7))

# ---------------------------------------------------------------- 048
def _c048():
    g = 2*x**2  # condition a >= 2x^2 on (1, 2)
    bound = maximum(g, x, Interval(1, 2))
    fp = diff(x**2 - bound*log(x), x)
    assert solveset(fp >= 0, x, Interval.open(1, 2)) == S.EmptySet
    return Interval(bound, oo)
q("U07-E-048", TOP_MONO, "Parameter for decrease on a bounded interval", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $a$ for which $f(x) = x^2 - a\log_e x$ is strictly decreasing on the interval $(1, 2)$ is",
  r"$[8, \infty)$",
  [(r"$(8, \infty)$", r"Rejects $a = 8$, though then $f'(x) = \frac{2(x^2 - 4)}{x}$ is negative throughout $(1, 2)$."),
   (r"$[2, \infty)$", r"Uses the value of $2x^2$ at the left end $x = 1$ instead of its supremum on $(1, 2)$."),
   (r"$[4, \infty)$", r"Writes $f'(x) = x - \frac{a}{x}$, dropping the $2$, which leads to $a \ge x^2$ on $(1, 2)$.")],
  r"$f'(x) = 2x - \frac{a}{x} = \frac{2x^2 - a}{x}$. For $f' \le 0$ on $(1, 2)$ we need $a \ge 2x^2$ for every $x \in (1, 2)$, i.e. $a \ge \sup 2x^2 = 8$. For $a = 8$, $f'(x) = \frac{2(x^2 - 4)}{x} < 0$ on the open interval, so $a = 8$ is allowed. Hence $a \in [8, \infty)$.",
  "Using the wrong end of the interval or wrongly excluding a supremum that is not attained.",
  "U07-E-param-decr-on-interval", "Converting to a uniform bound, taking a supremum, and a boundary decision.",
  check=_c048, values=[Interval(8, oo), Interval.open(8, oo), Interval(2, oo), Interval(4, oo)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 049
def _c049():
    f = x**3 - 3*x
    return solveset(f <= f.subs(x, 0), x, Interval.open(0, oo))
q("U07-E-049", TOP_ABS, "Interval length for which the maximum stays at an endpoint", "Difficult", "Inverse/parameter MCQ",
  r"Let $f(x) = x^3 - 3x$. The set of all $k > 0$ for which the absolute maximum value of $f$ on $[0, k]$ equals $f(0)$ is",
  r"$(0, \sqrt{3}]$",
  [(r"$(0, 1]$", r"Assumes that once $x$ passes the local minimum at $x = 1$, $f$ immediately exceeds $f(0)$."),
   (r"$(0, \sqrt{3})$", r"Excludes $k = \sqrt{3}$, though there $f(\sqrt{3}) = 0 = f(0)$ and the maximum value still equals $f(0)$."),
   (r"$(0, 2]$", r"Compares $f(k)$ with the local maximum value $f(-1) = 2$ instead of with $f(0)$: $k^3 - 3k \le 2$, i.e. $(k - 2)(k + 1)^2 \le 0$, gives $k \le 2$.")],
  r"$f'(x) = 3x^2 - 3$, so on $[0, \infty)$ $f$ decreases on $[0, 1]$ to $f(1) = -2$ and then increases. The maximum on $[0, k]$ is $\max(f(0), f(k)) = \max(0, k^3 - 3k)$. This equals $0$ iff $k^3 - 3k \le 0$, i.e. $k \le \sqrt{3}$ for $k > 0$. So $k \in (0, \sqrt{3}]$.",
  "Not comparing the far endpoint value with the near endpoint value.",
  "U07-E-absext-param-interval", "Absolute maximum as a function of the interval with casework.",
  check=_c049, values=[Interval.Lopen(0, sqrt(3)), Interval.Lopen(0, 1), Interval.open(0, sqrt(3)), Interval.Lopen(0, 2)],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 050
def _c050():
    cnt = 0
    for kv in range(-100, 101):
        p = Poly(2*x**3 - 3*x**2 - 12*x + kv, x)
        if discriminant(p) > 0:
            cnt += 1
    return cnt
q("U07-E-050", TOP_EXT, "Three real roots through extreme values", "Difficult", "Multi-step computation MCQ",
  r"The number of integers $k$ for which the equation $2x^3 - 3x^2 - 12x + k = 0$ has three distinct real roots is",
  r"$26$",
  [(r"$28$", r"Allows $k = -7$ and $k = 20$, where one root is repeated."),
   (r"$27$", r"Includes one of the endpoint values $k = -7$ or $k = 20$."),
   (r"$25$", r"Counts the integers in $(-7, 20)$ as $19 - (-6) = 25$, off by one.")],
  r"Let $f(x) = 2x^3 - 3x^2 - 12x + k$. Then $f'(x) = 6(x - 2)(x + 1)$, so the local maximum is $f(-1) = k + 7$ and the local minimum is $f(2) = k - 20$. Three distinct real roots need $f(-1) > 0 > f(2)$, i.e. $-7 < k < 20$. The integers $-6, -5, \dots, 19$ number $26$.",
  "Including the tangency cases or miscounting integers in an open interval.",
  "U07-E-extrema-root-count", "Extreme values, sign condition and integer counting.",
  check=_c050, values=[26, 28, 27, 25], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The number of integers $k$ for which the equation $2x^3 - 3x^2 - 12x + k = 0$ has three distinct real roots is", answer=26))

# ---------------------------------------------------------------- 051
def _c051():
    L = sqrt(x**2 + 9) + sqrt((8 - x)**2 + 25)
    crit = list(solveset(diff(L, x), x, Interval(0, 8)))
    vals = [simplify(L.subs(x, c)) for c in crit + [0, 8]]
    return min(vals, key=lambda v: N(v))
q("U07-E-051", TOP_OPT, "Shortest path touching a line", "Difficult", "Multi-step computation MCQ",
  r"Points $P(0, 3)$ and $Q(8, 5)$ lie on the same side of the $x$-axis. A point $R$ moves on the $x$-axis. The minimum value of $PR + RQ$ is",
  r"$8\sqrt{2}$",
  [(r"$8$", r"Minimises the two square roots separately, adding their least values $3$ and $5$, which cannot occur together."),
   (r"$3 + \sqrt{89}$", r"Takes $R$ at the origin, directly below $P$."),
   (r"$2\sqrt{17}$", r"Gives the straight-line distance $PQ$, ignoring that the path must touch the $x$-axis.")],
  r"With $R = (x, 0)$, $L(x) = \sqrt{x^2 + 9} + \sqrt{(8 - x)^2 + 25}$. $L'(x) = 0$ gives $\frac{x}{\sqrt{x^2 + 9}} = \frac{8 - x}{\sqrt{(8 - x)^2 + 25}}$, so $\frac{x}{3} = \frac{8 - x}{5}$ and $x = 3$. Then $L(3) = 3\sqrt{2} + 5\sqrt{2} = 8\sqrt{2}$, which equals the distance from $P$ to the reflection $(8, -5)$ of $Q$.",
  "Minimising terms of a sum independently.",
  "U07-E-opt-reflection-path", "Distance function with two radicals and a ratio condition.",
  check=_c051, values=[8*sqrt(2), 8, 3 + sqrt(89), 2*sqrt(17)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 052
def _c052():
    f = x - sin(x)
    h = Rational(1, 100)
    s1 = bool(f.subs(x, -h) >= 0 and f.subs(x, h) >= 0)  # local min at 0 would need f(+-h) >= f(0) = 0
    g = log(x)/x
    crit = list(solveset(diff(g, x), x, Interval.open(0, oo)))
    val = exp(g.subs(x, crit[0]))
    s2 = bool(simplify(val - E**(1/E)) == 0)
    return (s1, s2)
q("U07-E-052", TOP_EXT, "Monotonic function and maximum of x^{1/x}", "Difficult", "Statement-based MCQ",
  r"Statement I: The function $f(x) = x - \sin x$ has a local minimum at $x = 0$. Statement II: The maximum value of $g(x) = x^{1/x}$ for $x > 0$ is $e^{1/e}$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Sees $f'(0) = 1 - \cos 0 = 0$ and assumes a stationary point at the bottom of the graph is a minimum."),
   (ST_TF, r"Treats $x = 0$ as a minimum and takes the maximum of $x^{1/x}$ as $e$, the point where it occurs."),
   (ST_FF, r"Correctly rejects Statement I but confuses the maximising point $x = e$ with the maximum value.")],
  r"$f'(x) = 1 - \cos x \ge 0$ with zeros only at isolated points, so $f$ is strictly increasing; $f(x) < f(0)$ for $x < 0$, and $0$ is not a local minimum. Statement I is false. For $g$, $\log_e g = \frac{\log_e x}{x}$ has derivative $\frac{1 - \log_e x}{x^2}$, which changes sign from positive to negative at $x = e$, so the maximum of $g$ is $e^{1/e}$. Statement II is true.",
  "Equating a stationary point with an extremum.",
  "U07-E-stmt-strict-incr-xpow", "Two independent analyses including logarithmic differentiation.",
  check=_c052, values=[(F_, T), (T, T), (T, F_), (F_, F_)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 053
def _c053():
    h = Symbol('h', positive=True)
    R = 4
    A = h*sqrt(h*(2*R - h))
    crit = _opt_crit(A, h, Interval.open(0, 2*R))
    return Max(*[simplify(A.subs(h, c)) for c in crit])
q("U07-E-053", TOP_OPT, "Isosceles triangle of maximum area in a circle", "Difficult", "Multi-step computation MCQ",
  r"An isosceles triangle is inscribed in a circle of radius $4$ cm. The maximum possible area (in cm$^2$) of such a triangle is",
  r"$12\sqrt{3}$",
  [(r"$16$", r"Takes the base along a diameter with the apex at the top, a right isosceles triangle of area $\frac{1}{2}(8)(4)$."),
   (r"$24\sqrt{3}$", r"Finds the correct height $6$ and base $4\sqrt{3}$ but forgets the $\frac{1}{2}$ in the area."),
   (r"$8\sqrt{3}$", r"Uses the base $4\sqrt{3}$ but takes the height equal to the radius $4$.")],
  r"Let the height from the apex be $h$; the base is a chord at distance $h - 4$ from the centre, of half-length $\sqrt{16 - (h - 4)^2} = \sqrt{h(8 - h)}$. So $A = h\sqrt{h(8 - h)}$ and $A^2 = 8h^3 - h^4$. Then $\frac{d}{dh}A^2 = 24h^2 - 4h^3 = 0$ gives $h = 6$, so $A = 6\sqrt{12} = 12\sqrt{3}$ (the equilateral triangle).",
  "Assuming the base must be a diameter.",
  "U07-E-opt-triangle-in-circle", "Chord geometry, optimisation of a radical expression.",
  check=_c053, values=[12*sqrt(3), 16, 24*sqrt(3), 8*sqrt(3)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 054
def _c054():
    f = Abs(x)*(x - 3)**2
    pts = [0] + list(solve(diff(xp*(xp - 3)**2, xp), xp)) + list(solve(diff(-xn*(xn - 3)**2, xn), xn))
    return _ext_count(f, pts)
q("U07-E-054", TOP_EXT, "Counting extrema of a modulus product", "Difficult", "Multi-step computation MCQ",
  r"The number of points at which $f(x) = |x|(x - 3)^2$ has a local maximum or a local minimum is",
  r"$3$",
  [(r"$2$", r"Solves $f'(x) = 0$ only, getting $x = 1$ and $x = 3$, and misses the corner at $x = 0$."),
   (r"$5$", r"Treats $f$ as an even function and reflects $x = 1$ and $x = 3$ to the negative side as well."),
   (r"$1$", r"Counts only $x = 1$, treating the zeros $x = 0$ and $x = 3$ of $f$ as non-extrema.")],
  r"For $x > 0$, $f = x(x - 3)^2$ with $f' = 3(x - 1)(x - 3)$: local maximum at $x = 1$ and local minimum at $x = 3$. For $x < 0$, $f = -x(x - 3)^2$ with $f' = -3(x - 1)(x - 3) < 0$, so $f$ decreases to $f(0) = 0$ and then increases on $(0, 1)$: $x = 0$ is a local minimum. Total: $3$ points.",
  "Missing points of non-differentiability, or treating zeros of $f$ as non-extremal.",
  "U07-E-count-extrema-modulus", "Piecewise casework with a corner point.",
  check=_c054, values=[3, 2, 5, 1], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The number of points at which $f(x) = |x|(x - 3)^2$ has a local maximum or a local minimum is", answer=3))

# ---------------------------------------------------------------- 055
def _c055():
    c = Symbol('c', positive=True)  # base length; hypotenuse = 1 - c (sum fixed at 1)
    A2 = c**2*((1 - c)**2 - c**2)/4
    crit = _opt_crit(A2, c, Interval.open(0, Rational(1, 2)))
    cv = crit[0]
    return acos(cv/(1 - cv))
q("U07-E-055", TOP_OPT, "Right triangle with fixed sum of side and hypotenuse", "Difficult", "Multi-step computation MCQ",
  r"In a right-angled triangle, the sum of the hypotenuse and one of the sides containing the right angle is a fixed number. When the area of the triangle is maximum, the angle between that side and the hypotenuse is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{\pi}{4}$", r"Assumes the area is greatest for an isosceles right triangle."),
   (r"$\frac{\pi}{6}$", r"Finds the optimal triangle but reports the other acute angle."),
   (r"$\cos^{-1}\frac{1}{3}$", r"Finds the side as $\frac{k}{3}$ but divides by the fixed sum $k$ instead of the hypotenuse $\frac{2k}{3}$.")],
  r"Let the side be $x$ and the hypotenuse $k - x$. The other side is $\sqrt{(k - x)^2 - x^2} = \sqrt{k^2 - 2kx}$, so $A^2 = \frac{x^2(k^2 - 2kx)}{4}$. Differentiating, $2xk^2 - 6kx^2 = 0$, so $x = \frac{k}{3}$ and the hypotenuse is $\frac{2k}{3}$. Then $\cos\theta = \frac{1}{2}$, so $\theta = \frac{\pi}{3}$.",
  "Assuming symmetry gives the optimum.",
  "U07-E-opt-right-triangle-angle", "Model with a constraint, optimisation, then trigonometry.",
  check=_c055, values=[pi/3, pi/4, pi/6, acos(Rational(1, 3))], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 056
def _c056():
    c = Symbol('c', real=True)
    f = x**4 - 4*x**3 + 4*x**2 + c
    crit = solve(diff(f, x), x)
    mx = [p for p in crit if diff(f, x, 2).subs(x, p) < 0][0]
    cv = solve(Eq(f.subs(x, mx), 10), c)[0]
    g = f.subs(c, cv)
    return Max(*_abs_vals(g, -1, 3))
q("U07-E-056", TOP_ABS, "Absolute maximum after fixing a constant", "Difficult", "Multi-step computation MCQ",
  r"The local maximum value of $f(x) = x^4 - 4x^3 + 4x^2 + c$ is $10$. The absolute maximum value of $f$ on $[-1, 3]$ is",
  r"$18$",
  [(r"$10$", r"Takes the local maximum value as the absolute maximum on the interval, ignoring the endpoints."),
   (r"$19$", r"Sets $f(1) = c = 10$, forgetting that $f(1) = 1 + c$, and then evaluates $f(-1) = 9 + c$."),
   (r"$9$", r"Gives the absolute minimum value $f(0) = f(2) = 9$.")],
  r"$f'(x) = 4x^3 - 12x^2 + 8x = 4x(x - 1)(x - 2)$, so the local maximum is at $x = 1$: $f(1) = 1 + c = 10$, so $c = 9$. On $[-1, 3]$: $f(-1) = 18$, $f(0) = 9$, $f(1) = 10$, $f(2) = 9$, $f(3) = 18$. The absolute maximum is $18$.",
  "Confusing the local maximum with the absolute maximum on a closed interval.",
  "U07-E-absext-quartic-constant", "Find a constant from a local value, then compare five candidates.",
  check=_c056, values=[18, 10, 19, 9], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The local maximum value of $f(x) = x^4 - 4x^3 + 4x^2 + c$ is $10$. The absolute maximum value of $f$ on $[-1, 3]$ is", answer=18))

# ---------------------------------------------------------------- 057
def _c057():
    f = 8/sin(x) + 27/cos(x)
    u = Symbol('u', positive=True)  # u = tan x
    tv = solve(Eq(u**3, Rational(8, 27)), u)[0]
    # confirm tan x = tv is the stationary point: f' = -8cos/sin^2 + 27 sin/cos^2
    xv = atan(tv)
    assert abs(N(diff(f, x).subs(x, xv))) < 1e-20
    return nsimplify(simplify(f.subs(x, xv)))
q("U07-E-057", TOP_OPT, "Minimum of a sum of cosecant and secant terms", "Difficult", "Multi-step computation MCQ",
  r"The minimum value of $f(x) = \frac{8}{\sin x} + \frac{27}{\cos x}$ for $0 < x < \frac{\pi}{2}$ is",
  r"$13\sqrt{13}$",
  [(r"$\frac{97\sqrt{13}}{6}$", r"Inverts the stationary condition to $\tan x = \frac{3}{2}$, so $\sin x = \frac{3}{\sqrt{13}}$ and $\cos x = \frac{2}{\sqrt{13}}$."),
   (r"$35\sqrt{2}$", r"Assumes the minimum is at the symmetric point $x = \frac{\pi}{4}$."),
   (r"$13$", r"Computes $8^{2/3} + 27^{2/3} = 13$ and forgets to raise it to the power $\frac{3}{2}$.")],
  r"$f'(x) = -\frac{8\cos x}{\sin^2 x} + \frac{27\sin x}{\cos^2 x} = 0$ gives $\tan^3 x = \frac{8}{27}$, so $\tan x = \frac{2}{3}$, $\sin x = \frac{2}{\sqrt{13}}$, $\cos x = \frac{3}{\sqrt{13}}$. Then $f = 4\sqrt{13} + 9\sqrt{13} = 13\sqrt{13}$; as $f \to \infty$ at both ends of the interval, this is the minimum.",
  "Assuming symmetric optimum or inverting the stationary condition.",
  "U07-E-opt-csc-sec", "Trigonometric derivative, cube-root condition, exact evaluation.",
  check=_c057, values=[13*sqrt(13), Rational(97, 6)*sqrt(13), 35*sqrt(2), 13], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 058
def _c058():
    h = Symbol('h', positive=True)
    R = 3*sqrt(3)
    V = pi*(R**2 - h**2/4)*h
    crit = _opt_crit(V, h, Interval.open(0, 2*R))
    return Max(*[simplify(V.subs(h, c)) for c in crit])
q("U07-E-058", TOP_OPT, "Largest cylinder in a sphere", "Difficult", "Multi-step computation MCQ",
  r"A right circular cylinder is inscribed in a sphere of radius $3\sqrt{3}$ cm. The maximum possible volume (in cm$^3$) of the cylinder is",
  r"$108\pi$",
  [(r"$54\pi$", r"Uses $r^2 + h^2 = R^2$, taking the full height instead of half the height in the right triangle."),
   (r"$32\sqrt{3}\pi$", r"Uses the result $\frac{32}{81}\pi R^3$ for the largest inscribed cone."),
   (r"$162\pi$", r"Finds the optimal height $6$ but takes the cylinder's radius equal to the sphere's radius.")],
  r"With height $h$ and radius $r$, $r^2 + \frac{h^2}{4} = 27$, so $V = \pi\left(27 - \frac{h^2}{4}\right)h$. $V'(h) = \pi\left(27 - \frac{3h^2}{4}\right) = 0$ gives $h = 6$ and $r^2 = 18$. So $V = \pi(18)(6) = 108\pi$ cm$^3$.",
  "Using the full height in the radius-height relation.",
  "U07-E-opt-cylinder-in-sphere", "Geometry relation, optimisation and exact evaluation with surds.",
  check=_c058, values=[108*pi, 54*pi, 32*sqrt(3)*pi, 162*pi], cognitive="Application", source_class=XII)
