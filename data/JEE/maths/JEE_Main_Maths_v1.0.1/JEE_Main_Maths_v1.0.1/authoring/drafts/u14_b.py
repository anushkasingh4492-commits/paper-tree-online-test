import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import mpmath as _mp
from sympy.calculus.util import function_range

# ---------------------------------------------------------------- helpers
x = Symbol('x', real=True)
t = Symbol('t', real=True)
u = Symbol('u', real=True)
a_ = Symbol('a', real=True)
th = Symbol('theta', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TT, FF, TF, FT = (True, True), (False, False), (True, False), (False, True)

TOP_F = "Trigonometric functions"
TOP_M = "Maximum and minimum of trigonometric expressions"
TOP_G = "Number of solutions by graphs"
TOP_S = "Signs and comparison of trigonometric values"

FULL = Interval(0, 2*pi)


def fund_period(f, var=x):
    """Smallest positive T dividing sympy's period P with f(x+T) = f(x) at sample points."""
    P = periodicity(f, var)
    pts = [Rational(3, 10) + Rational(37, 100)*k for k in range(7)]
    for n in range(24, 0, -1):
        T = P/n
        if all(abs(N(f.subs(var, p + T) - f.subs(var, p), 40)) < 1e-25 for p in pts):
            return simplify(T)
    raise ValueError("no period")


def clean(v):
    """Recognise the exact closed form of a computed constant (verified to 40 digits)."""
    v = sympify(v)
    w = nsimplify(N(v, 60), [sqrt(2), sqrt(3), sqrt(5), sqrt(7)], tolerance=1e-45)
    assert abs(N(w - v, 50)) < 1e-40
    return w


def ext(f, I, var=x):
    """(min, max) of a continuous f on the closed interval I, via critical points and endpoints."""
    crit = solveset(diff(f, var), var, I)
    assert isinstance(crit, FiniteSet), crit
    vals = [f.subs(var, p) for p in list(crit) + [I.inf, I.sup]]
    lo = min(vals, key=lambda v: float(re(N(v, 30))))
    hi = max(vals, key=lambda v: float(re(N(v, 30))))
    return clean(re(N(lo, 60))), clean(re(N(hi, 60)))


def to_t(expr):
    """Rewrite an expression in sin x and cos x as a polynomial in t = sin x."""
    e = expand(expand_trig(expr))
    e = e.subs(cos(x)**2, 1 - sin(x)**2).subs(sin(x), t)
    assert x not in e.free_symbols
    return expand(e)


def count_roots(fx, lo, hi, n=40000, var=x):
    """Number of zeros of fx on [lo, hi] by sign changes on a fine grid."""
    _mp.mp.dps = 25
    g = lambdify(var, fx, 'mpmath')
    lo, hi = _mp.mpf(N(lo, 30)), _mp.mpf(N(hi, 30))
    c = 0
    prev = g(lo)
    if prev == 0:
        c += 1
    for i in range(1, n + 1):
        xv = lo + (hi - lo)*i/n
        v = g(xv)
        if v == 0:
            c += 1
        elif prev != 0 and (v > 0) != (prev > 0):
            c += 1
        prev = v
    return c


# =================================================================== Q1-Q16 (Easy)

q("U14-B-001", TOP_F, "Period of the modulus of a cosine", "Easy", "Single-step computation MCQ",
  r"The fundamental period of $f(x) = |\cos 3x|$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{2\pi}{3}$", r"Uses the period $\frac{2\pi}{3}$ of $\cos 3x$ and ignores that the modulus halves it."),
   (r"$\frac{\pi}{6}$", r"Takes the period of $|\cos x|$ as $\frac{\pi}{2}$ and then divides by $3$."),
   (r"$3\pi$", r"Multiplies the period $\pi$ of $|\cos x|$ by $3$ instead of dividing by $3$.")],
  r"Since $\cos(x + \pi) = -\cos x$, the function $|\cos x|$ has fundamental period $\pi$. Replacing $x$ by $3x$ divides the period by $3$, so $|\cos 3x|$ has fundamental period $\frac{\pi}{3}$.",
  r"Forgetting that taking the modulus of $\cos x$ halves its period.",
  "U14-B-period-abs", r"One property (modulus halves the period) plus scaling of the argument.",
  check=lambda: fund_period(Abs(cos(3*x))),
  values=[pi/3, 2*pi/3, pi/6, 3*pi], cognitive="Understanding")

q("U14-B-002", TOP_F, "Period of tangent with scaled argument", "Easy", "Single-step computation MCQ",
  r"The fundamental period of $f(x) = \tan\left(\frac{2x}{3}\right)$ is",
  r"$\frac{3\pi}{2}$",
  [(r"$3\pi$", r"Uses $\frac{2\pi}{k}$, the rule for sine and cosine, instead of $\frac{\pi}{k}$ for tangent."),
   (r"$\frac{2\pi}{3}$", r"Multiplies the period $\pi$ by $k = \frac{2}{3}$ instead of dividing by it."),
   (r"$\pi$", r"Ignores the coefficient of $x$ and quotes the period of $\tan x$.")],
  r"$\tan x$ has period $\pi$, so $\tan(kx)$ has period $\frac{\pi}{|k|}$. With $k = \frac{2}{3}$ the period is $\frac{\pi}{2/3} = \frac{3\pi}{2}$.",
  r"Using $2\pi$ as the base period of tangent, or multiplying by $k$.",
  "U14-B-period-linear-arg", r"Direct use of $T = \frac{\pi}{|k|}$ once.",
  check=lambda: fund_period(tan(2*x/3)),
  values=[3*pi/2, 3*pi, 2*pi/3, pi], cognitive="Recall")

q("U14-B-003", TOP_F, "Period of a sum (LCM of periods)", "Easy", "Single-step computation MCQ",
  r"The fundamental period of $f(x) = \sin\frac{x}{2} + \cos\frac{x}{3}$ is",
  r"$12\pi$",
  [(r"$24\pi$", r"Multiplies the two periods' coefficients, $4 \times 6 = 24$, instead of taking their LCM."),
   (r"$6\pi$", r"Takes the larger of the two periods $4\pi$ and $6\pi$ as the period of the sum."),
   (r"$10\pi$", r"Adds the two periods, $4\pi + 6\pi$.")],
  r"$\sin\frac{x}{2}$ has period $\frac{2\pi}{1/2} = 4\pi$ and $\cos\frac{x}{3}$ has period $6\pi$. Since the two terms have different frequencies, any period of the sum must be a common period of both terms, i.e. a common multiple of $4\pi$ and $6\pi$. The least such value is $\operatorname{LCM}(4\pi, 6\pi) = 12\pi$, and $12\pi$ clearly works.",
  r"Combining periods of a sum by multiplying, adding or taking the larger one instead of the LCM.",
  "U14-B-period-lcm", r"Two periods found and combined by an LCM.",
  check=lambda: fund_period(sin(x/2) + cos(x/3)),
  values=[12*pi, 24*pi, 6*pi, 10*pi], cognitive="Application",
  numerical=dict(question=r"If the fundamental period of $f(x) = \sin\frac{x}{2} + \cos\frac{x}{3}$ is $k\pi$, then $k$ is", answer=12))

q("U14-B-004", TOP_M, "Range of a sin x + b cos x", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = 3\sin x + 4\cos x$, $x \in \mathbb{R}$, is",
  r"$[-5, 5]$",
  [(r"$[-7, 7]$", r"Adds the coefficients, taking the maximum as $3 + 4$."),
   (r"$[-\sqrt{7}, \sqrt{7}]$", r"Uses $\sqrt{4^2 - 3^2}$ instead of $\sqrt{3^2 + 4^2}$."),
   (r"$[-4, 4]$", r"Takes the larger coefficient as the amplitude.")],
  r"$3\sin x + 4\cos x = 5\sin(x + \alpha)$ with $\cos\alpha = \frac{3}{5}$, $\sin\alpha = \frac{4}{5}$. Since $\sin(x+\alpha)$ takes every value in $[-1,1]$, the range is $[-\sqrt{3^2+4^2}, \sqrt{3^2+4^2}] = [-5, 5]$.",
  r"Adding the coefficients instead of using $\sqrt{a^2 + b^2}$.",
  "U14-B-asinbcos-range", r"Single standard result $\pm\sqrt{a^2+b^2}$.",
  check=lambda: Interval(*ext(3*sin(x) + 4*cos(x), FULL)),
  values=[Interval(-5, 5), Interval(-7, 7), Interval(-sqrt(7), sqrt(7)), Interval(-4, 4)], cognitive="Recall")

q("U14-B-005", TOP_M, "Maximum of a sin x + b cos x + c", "Easy", "Single-step computation MCQ",
  r"The maximum value of $5 + 12\sin x - 5\cos x$, $x \in \mathbb{R}$, is",
  r"$18$",
  [(r"$22$", r"Adds the separate maxima $5 + 12 + 5$, assuming $\sin x = 1$ and $\cos x = -1$ together."),
   (r"$13$", r"Finds the amplitude $\sqrt{12^2 + 5^2} = 13$ but drops the constant $5$."),
   (r"$17$", r"Takes $5 + 12$, treating the cosine term as contributing nothing at the maximum.")],
  r"$12\sin x - 5\cos x$ has maximum $\sqrt{12^2 + (-5)^2} = 13$, attained when $\sin x = \frac{12}{13}$, $\cos x = -\frac{5}{13}$. Hence the maximum of the expression is $5 + 13 = 18$.",
  r"Adding separate maxima of $\sin x$ and $\cos x$ that cannot occur together.",
  "U14-B-asinbcos-const-max", r"One standard result plus a constant shift.",
  check=lambda: ext(5 + 12*sin(x) - 5*cos(x), FULL)[1],
  values=[18, 22, 13, 17], cognitive="Application",
  numerical=dict(question=r"The maximum value of $5 + 12\sin x - 5\cos x$, $x \in \mathbb{R}$, is", answer=18))


def _c6():
    c = Rational(-3, 5)
    cands = [acos(c), 2*pi - acos(c)]
    th0 = [v for v in cands if N(tan(v)) > 0][0]
    return simplify(sin(th0) + 1/cos(th0))
q("U14-B-006", TOP_S, "Signs of ratios from the quadrant", "Easy", "Single-step computation MCQ",
  r"If $\cos\theta = -\frac{3}{5}$ and $\tan\theta > 0$, then $\sin\theta + \sec\theta$ equals",
  r"$-\frac{37}{15}$",
  [(r"$-\frac{13}{15}$", r"Takes $\sin\theta = +\frac{4}{5}$, giving $\frac{4}{5} - \frac{5}{3} = -\frac{13}{15}$."),
   (r"$\frac{13}{15}$", r"Takes $\sec\theta = +\frac{5}{3}$, giving $-\frac{4}{5} + \frac{5}{3} = \frac{13}{15}$."),
   (r"$\frac{37}{15}$", r"Places $\theta$ in the first quadrant with all ratios positive, $\frac{4}{5} + \frac{5}{3}$.")],
  r"$\cos\theta < 0$ and $\tan\theta > 0$ put $\theta$ in the third quadrant, where $\sin\theta < 0$. So $\sin\theta = -\frac{4}{5}$ and $\sec\theta = -\frac{5}{3}$, giving $-\frac{4}{5} - \frac{5}{3} = -\frac{37}{15}$.",
  r"Attaching the wrong sign to $\sin\theta$ or $\sec\theta$ in the third quadrant.",
  "U14-B-quadrant-eval", r"Quadrant from two signs, then one Pythagorean step.",
  check=_c6, values=[Rational(-37, 15), Rational(-13, 15), Rational(13, 15), Rational(37, 15)], cognitive="Application")


def _c7():
    good = []
    for k in range(1, 5):
        m = (2*k - 1)*pi/4
        if N(sin(m)*cos(m)) < 0 and N(cos(m)*tan(m)) > 0:
            good.append(k)
    assert len(good) == 1
    return good[0]
q("U14-B-007", TOP_S, "Quadrant from sign conditions", "Easy", "Conceptual/application MCQ",
  r"If $\sin\theta\cos\theta < 0$ and $\cos\theta\tan\theta > 0$, then the terminal side of $\theta$ lies in the",
  r"second quadrant",
  [(r"fourth quadrant", r"Uses the first condition (second or fourth quadrant) and then picks the one where $\cos\theta > 0$, not simplifying $\cos\theta\tan\theta$ to $\sin\theta$."),
   (r"third quadrant", r"Keeps only the case $\cos\theta < 0$ from $\sin\theta\cos\theta < 0$, then makes a sign slip in $\cos\theta\tan\theta > 0$, concluding $\tan\theta > 0$ instead of $\tan\theta < 0$; $\cos\theta < 0$ with $\tan\theta > 0$ gives the third quadrant."),
   (r"first quadrant", r"Reads $\cos\theta\tan\theta > 0$ as both factors positive and ignores the first condition.")],
  r"$\sin\theta\cos\theta < 0$ means $\theta$ is in the second or fourth quadrant. Also $\cos\theta\tan\theta = \sin\theta > 0$, which means the first or second quadrant. Together, $\theta$ lies in the second quadrant.",
  r"Not simplifying $\cos\theta\tan\theta$ to $\sin\theta$ and misreading a negative product.",
  "U14-B-quadrant-identify", r"Two sign conditions intersected; one simplification.",
  check=_c7, values=[2, 4, 3, 1], cognitive="Understanding")

q("U14-B-008", TOP_F, "Domain of a square root of cosine", "Easy", "Single-step computation MCQ",
  r"The set of all $x \in [0, 2\pi)$ for which $f(x) = \sqrt{\cos x}$ is real is",
  r"$\left[0, \frac{\pi}{2}\right] \cup \left[\frac{3\pi}{2}, 2\pi\right)$",
  [(r"$[0, \pi]$", r"Uses the set where $\sin x \ge 0$ instead of $\cos x \ge 0$."),
   (r"$\left[\frac{\pi}{2}, \frac{3\pi}{2}\right]$", r"Reverses the inequality and takes $\cos x \le 0$."),
   (r"$\left[0, \frac{\pi}{2}\right]$", r"Keeps only the first quadrant and misses the fourth quadrant.")],
  r"We need $\cos x \ge 0$. On $[0, 2\pi)$ cosine is non-negative in the first and fourth quadrants including the zeros $\frac{\pi}{2}$ and $\frac{3\pi}{2}$, giving $\left[0, \frac{\pi}{2}\right] \cup \left[\frac{3\pi}{2}, 2\pi\right)$.",
  r"Forgetting that cosine is also positive in the fourth quadrant.",
  "U14-B-domain-sqrt-interval", r"One sign condition read from the graph of cosine.",
  check=lambda: solveset(cos(x) >= 0, x, Interval.Ropen(0, 2*pi)),
  values=[Union(Interval(0, pi/2), Interval.Ropen(3*pi/2, 2*pi)), Interval(0, pi), Interval(pi/2, 3*pi/2), Interval(0, pi/2)],
  cognitive="Application")

q("U14-B-009", TOP_F, "Domain of log of sine", "Easy", "Single-step computation MCQ",
  r"The set of all $x \in [0, 2\pi)$ for which $f(x) = \log_e(\sin x)$ is defined is",
  r"$(0, \pi)$",
  [(r"$[0, \pi]$", r"Includes the zeros of $\sin x$, where the logarithm is undefined."),
   (r"$(\pi, 2\pi)$", r"Takes the interval where $\sin x < 0$."),
   (r"$\left[0, \frac{\pi}{2}\right) \cup \left(\frac{3\pi}{2}, 2\pi\right)$", r"Uses the set where $\cos x > 0$ instead of $\sin x > 0$.")],
  r"The logarithm needs $\sin x > 0$ strictly. On $[0, 2\pi)$ this holds exactly for $0 < x < \pi$, so the domain is $(0, \pi)$.",
  r"Allowing $\sin x = 0$ inside a logarithm.",
  "U14-B-domain-log-interval", r"One strict sign condition.",
  check=lambda: solveset(sin(x) > 0, x, Interval.Ropen(0, 2*pi)),
  values=[Interval.open(0, pi), Interval(0, pi), Interval.open(pi, 2*pi), Union(Interval.Ropen(0, pi/2), Interval.open(3*pi/2, 2*pi))],
  cognitive="Application")

q("U14-B-010", TOP_M, "Range of a reciprocal expression", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = \frac{3}{2 - \cos x}$, $x \in \mathbb{R}$, is",
  r"$[1, 3]$",
  [(r"$\left[\frac{1}{3}, 1\right]$", r"Finds the range of $\frac{1}{2 - \cos x}$ and drops the numerator $3$."),
   (r"$\left[\frac{3}{2}, 3\right]$", r"Takes $\cos x \in [0, 1]$ only, so $2 - \cos x \in [1, 2]$."),
   (r"$[3, 9]$", r"Multiplies $3$ by the range $[1, 3]$ of $2 - \cos x$ instead of dividing.")],
  r"Since $-1 \le \cos x \le 1$, we get $1 \le 2 - \cos x \le 3$. Taking reciprocals and multiplying by $3$, $1 \le \frac{3}{2 - \cos x} \le 3$, with both ends attained at $\cos x = -1$ and $\cos x = 1$.",
  r"Restricting $\cos x$ to $[0,1]$ or mishandling the reciprocal.",
  "U14-B-reciprocal-range", r"Bounds of cosine pushed through a reciprocal.",
  check=lambda: Interval(*ext(3/(2 - cos(x)), FULL)),
  values=[Interval(1, 3), Interval(Rational(1, 3), 1), Interval(Rational(3, 2), 3), Interval(3, 9)], cognitive="Application")

q("U14-B-011", TOP_M, "Minimum of a combination of squares", "Easy", "Single-step computation MCQ",
  r"The minimum value of $3\sin^2 x + 5\cos^2 x$, $x \in \mathbb{R}$, is",
  r"$3$",
  [(r"$0$", r"Takes the minimum of each term separately as $0$, which cannot happen together."),
   (r"$2$", r"Takes the coefficient $5 - 3 = 2$ of the varying part $2\cos^2 x$ as the minimum."),
   (r"$5$", r"Picks the larger coefficient, confusing the minimum with the maximum.")],
  r"$3\sin^2 x + 5\cos^2 x = 3(\sin^2 x + \cos^2 x) + 2\cos^2 x = 3 + 2\cos^2 x$. Since $0 \le \cos^2 x \le 1$, the minimum is $3$ (at $\cos x = 0$).",
  r"Minimising $\sin^2 x$ and $\cos^2 x$ independently.",
  "U14-B-sin2cos2-linear", r"One identity reduces it to a single square.",
  check=lambda: ext(3*sin(x)**2 + 5*cos(x)**2, FULL)[0],
  values=[3, 0, 2, 5], cognitive="Application")


def _c12():
    opts = [tan(2), sin(3), cos(5), sec(6)]
    neg = [v for v in opts if N(v) < 0]
    assert len(neg) == 1
    return neg[0]
q("U14-B-012", TOP_S, "Sign of a ratio at a radian angle", "Easy", "Conceptual/application MCQ",
  r"Which of the following is negative? (All angles are in radians.)",
  r"$\tan 2$",
  [(r"$\sin 3$", r"Treats $3$ rad as more than $\pi$, i.e. in the third quadrant, though $3 < \pi$."),
   (r"$\cos 5$", r"Places $5$ rad in the third quadrant, though $\frac{3\pi}{2} \approx 4.71 < 5$."),
   (r"$\sec 6$", r"Places $6$ rad before $\frac{3\pi}{2}$, in the third quadrant, though it lies in the fourth.")],
  r"Using $\frac{\pi}{2} \approx 1.57$, $\pi \approx 3.14$, $\frac{3\pi}{2} \approx 4.71$, $2\pi \approx 6.28$: $2$ rad is in the second quadrant, where $\tan$ is negative. $3$ rad is also in the second quadrant ($\sin 3 > 0$), while $5$ and $6$ rad are in the fourth quadrant ($\cos$ and $\sec$ positive).",
  r"Misplacing a radian angle in the wrong quadrant.",
  "U14-B-sign-radian", r"Locate four radian angles; one sign rule each.",
  check=_c12, values=[tan(2), sin(3), cos(5), sec(6)], cognitive="Understanding")


def _c13():
    vals = [sin(1), cos(1), tan(1)]
    return tuple(sorted(vals, key=lambda v: N(v)))
q("U14-B-013", TOP_S, "Comparing ratios of the same angle", "Easy", "Conceptual/application MCQ",
  r"For the angle $1$ radian, which of the following is true?",
  r"$\cos 1 < \sin 1 < \tan 1$",
  [(r"$\sin 1 < \cos 1 < \tan 1$", r"Assumes $1$ rad is less than $\frac{\pi}{4}$, where cosine exceeds sine."),
   (r"$\sin 1 < \tan 1 < \cos 1$", r"Treats the angle as $1^\circ$, where sine and tangent are tiny and cosine is near $1$."),
   (r"$\cos 1 < \tan 1 < \sin 1$", r"Believes $\tan x < \sin x$, forgetting that $\tan 1 > 1$ because $1 > \frac{\pi}{4}$.")],
  r"Since $\frac{\pi}{4} \approx 0.785 < 1 < \frac{\pi}{2}$, we have $\sin 1 > \cos 1$. Also $\tan 1 = \frac{\sin 1}{\cos 1} > \sin 1$ because $0 < \cos 1 < 1$. Hence $\cos 1 < \sin 1 < \tan 1$.",
  r"Comparing ratios without locating $1$ rad relative to $\frac{\pi}{4}$.",
  "U14-B-compare-same-angle", r"Locate 1 rad against $\frac{\pi}{4}$; one inequality each.",
  check=_c13,
  values=[(cos(1), sin(1), tan(1)), (sin(1), cos(1), tan(1)), (sin(1), tan(1), cos(1)), (cos(1), tan(1), sin(1))],
  cognitive="Understanding")

def _c14():
    lo, hi = ext(cos(2*x), Interval(0, pi))
    a_lo = 0 if (lo <= 0 <= hi) else Min(Abs(lo), Abs(hi))
    a_hi = Max(Abs(lo), Abs(hi))
    r = function_range(7 - 3*u, u, Interval(a_lo, a_hi))
    return r.inf + r.sup
q("U14-B-014", TOP_M, "Range of a shifted modulus of cosine", "Easy", "Single-step computation MCQ",
  r"If the range of $f(x) = 7 - 3|\cos 2x|$, $x \in \mathbb{R}$, is $[m, M]$, then $m + M$ is",
  r"$11$",
  [(r"$14$", r"Drops the modulus and uses $-1 \le \cos 2x \le 1$, getting the range $[4, 10]$ and $4 + 10 = 14$."),
   (r"$8$", r"Multiplies the amplitude by the $2$ in $2x$, taking $0 \le 3|\cos 2x| \le 6$, so the range is $[1, 7]$ and $1 + 7 = 8$."),
   (r"$17$", r"Makes a sign slip and works with $7 + 3|\cos 2x|$, getting the range $[7, 10]$ and $7 + 10 = 17$.")],
  r"Since $0 \le |\cos 2x| \le 1$, with $|\cos 2x| = 0$ at $x = \frac{\pi}{4}$ and $|\cos 2x| = 1$ at $x = 0$, we get $7 - 3 \le f(x) \le 7$. So $m = 4$, $M = 7$ and $m + M = 11$.",
  r"Ignoring the modulus, or letting the factor $2$ inside the cosine change the amplitude.",
  "U14-B-abs-shift-range", r"One bound on $|\cos 2x|$ pushed through a linear map.",
  check=_c14, values=[11, 14, 8, 17], cognitive="Application",
  numerical=dict(question=r"If the range of $f(x) = 7 - 3|\cos 2x|$, $x \in \mathbb{R}$, is $[m, M]$, then $m + M$ is", answer=11))


def _c15():
    s1 = bool(diff(tan(x), x) > 0)
    s2 = fund_period(sin(x)*cos(x)) == 2*pi
    return (s1, bool(s2))
q("U14-B-015", TOP_F, "Monotonicity of tangent and period of a product", "Easy", "Statement-based MCQ",
  r"Statement I: $\tan x$ is strictly increasing on $\left(\frac{\pi}{2}, \frac{3\pi}{2}\right)$. Statement II: The fundamental period of $\sin x\cos x$ is $2\pi$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Takes the period of a product of $\sin x$ and $\cos x$ to be their common period $2\pi$."),
   (ST_FF, r"Rejects Statement I because of the asymptotes at the ends of the interval, and correctly rejects Statement II."),
   (ST_FT, r"Rejects Statement I because of the asymptotes and accepts the period $2\pi$.")],
  r"On $\left(\frac{\pi}{2}, \frac{3\pi}{2}\right)$ there is no asymptote of $\tan x$ inside and $\frac{d}{dx}\tan x = \sec^2 x > 0$, so Statement I is true. But $\sin x\cos x = \frac{1}{2}\sin 2x$ has fundamental period $\pi$, so Statement II is false.",
  r"Assuming a product of functions with period $2\pi$ has fundamental period $2\pi$.",
  "U14-B-stmt-monotone-period", r"Two quick facts checked independently.",
  check=_c15, values=[TF, TT, FF, FT], cognitive="Understanding")


def _c16():
    r1 = Interval(*ext(sin(x) + cos(x), FULL))
    m2 = ext(sin(x)*cos(x), FULL)[1]
    return (r1 == Interval(-2, 2), m2 == 1)
q("U14-B-016", TOP_M, "Range of sin x + cos x and maximum of sin x cos x", "Easy", "Statement-based MCQ",
  r"Statement I: The range of $\sin x + \cos x$, $x \in \mathbb{R}$, is $[-2, 2]$. Statement II: The maximum value of $\sin x\cos x$, $x \in \mathbb{R}$, is $1$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Takes $\sin x$ and $\cos x$ to equal $1$ (and $-1$) at the same $x$ in both statements, giving the sum range $[-2, 2]$ and the product maximum $1 \times 1 = 1$."),
   (ST_TF, r"Accepts $[-2, 2]$ by adding maxima but correctly rejects the maximum $1$ of $\sin x\cos x$."),
   (ST_FT, r"Correctly finds $[-\sqrt{2}, \sqrt{2}]$ but takes the maximum of the product as $1 \times 1$.")],
  r"$\sin x + \cos x = \sqrt{2}\sin\left(x + \frac{\pi}{4}\right)$ has range $[-\sqrt{2}, \sqrt{2}]$, so Statement I is false. $\sin x\cos x = \frac{1}{2}\sin 2x$ has maximum $\frac{1}{2}$, so Statement II is false.",
  r"Assuming $\sin x$ and $\cos x$ reach $1$ at the same $x$.",
  "U14-B-stmt-range-max", r"Two standard reductions checked independently.",
  check=_c16, values=[FF, TT, TF, FT], cognitive="Understanding")


# =================================================================== Q17-Q30

q("U14-B-017", TOP_M, "Range of a quadratic in sin x (vertex outside)", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \cos^2 x - 3\sin x + 2$, $x \in \mathbb{R}$, is",
  r"$[-1, 5]$",
  [(r"$\left[-1, \frac{21}{4}\right]$", r"Uses the vertex value at $\sin x = -\frac{3}{2}$, which is outside $[-1, 1]$, as the maximum."),
   (r"$[-1, 6]$", r"Bounds $\cos^2 x \in [0, 1]$ and $-3\sin x \in [-3, 3]$ separately and adds."),
   (r"$[1, 7]$", r"Writes $\cos^2 x = 1 + \sin^2 x$, giving $t^2 - 3t + 3$ on $[-1, 1]$.")],
  r"With $t = \sin x \in [-1, 1]$, $f = 1 - t^2 - 3t + 2 = 3 - 3t - t^2$. Its vertex is at $t = -\frac{3}{2}$, outside $[-1,1]$, so $f$ is decreasing on $[-1,1]$: $f(-1) = 5$ and $f(1) = -1$. The range is $[-1, 5]$.",
  r"Using the vertex of the quadratic when it lies outside $[-1, 1]$.",
  "U14-B-quad-sin-range", r"Convert to a quadratic in $\sin x$ and notice the vertex is outside the allowed interval.",
  check=lambda: function_range(to_t(cos(x)**2 - 3*sin(x) + 2), t, Interval(-1, 1)),
  values=[Interval(-1, 5), Interval(-1, Rational(21, 4)), Interval(-1, 6), Interval(1, 7)], cognitive="Application")

q("U14-B-018", TOP_M, "Range of a quadratic in sin x (vertex at an end)", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \sin^2 x - 2\sin x + 3$, $x \in \mathbb{R}$, is",
  r"$[2, 6]$",
  [(r"$[1, 6]$", r"Bounds $\sin^2 x \in [0,1]$ and $-2\sin x \in [-2, 2]$ separately and adds $3$."),
   (r"$[2, 3]$", r"Takes $\sin x \in [0, 1]$ only, missing the negative values of $\sin x$."),
   (r"$[3, 6]$", r"Assumes the minimum occurs at $\sin x = 0$.")],
  r"Put $t = \sin x \in [-1,1]$: $f = t^2 - 2t + 3 = (t - 1)^2 + 2$. On $[-1, 1]$ this decreases, so the minimum is $f(1) = 2$ and the maximum is $f(-1) = 6$. The range is $[2, 6]$.",
  r"Bounding the terms of a quadratic in $\sin x$ separately.",
  "U14-B-quad-sin-range", r"Completing the square in $\sin x$ and checking both ends of $[-1,1]$.",
  check=lambda: function_range(to_t(sin(x)**2 - 2*sin(x) + 3), t, Interval(-1, 1)),
  values=[Interval(2, 6), Interval(1, 6), Interval(2, 3), Interval(3, 6)], cognitive="Application")

q("U14-B-019", TOP_M, "Range of a sin x + b cos x + c on a restricted interval", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \sin x + \sqrt{3}\cos x + 1$ for $x \in \left[0, \frac{\pi}{2}\right]$ is",
  r"$[2, 3]$",
  [(r"$[-1, 3]$", r"Uses the full range $[-2, 2]$ of $2\sin\left(x + \frac{\pi}{3}\right)$, ignoring the restriction on $x$."),
   (r"$[2, 1 + \sqrt{3}]$", r"Evaluates only at the endpoints $x = 0$ and $x = \frac{\pi}{2}$, missing the interior maximum."),
   (r"$[1 + \sqrt{3}, 3]$", r"Takes the value at $x = 0$ as the minimum without comparing with $x = \frac{\pi}{2}$.")],
  r"$f(x) = 2\sin\left(x + \frac{\pi}{3}\right) + 1$. For $x \in \left[0, \frac{\pi}{2}\right]$, $x + \frac{\pi}{3} \in \left[\frac{\pi}{3}, \frac{5\pi}{6}\right]$, on which $\sin$ ranges over $\left[\frac{1}{2}, 1\right]$ (minimum at $\frac{5\pi}{6}$, maximum at $\frac{\pi}{2}$). So $f$ ranges over $[2, 3]$.",
  r"Using the unrestricted amplitude, or checking only endpoints.",
  "U14-B-asinbcos-restricted", r"Combine into one sine, then restrict the argument and read the range.",
  check=lambda: Interval(*ext(sin(x) + sqrt(3)*cos(x) + 1, Interval(0, pi/2))),
  values=[Interval(2, 3), Interval(-1, 3), Interval(2, 1 + sqrt(3)), Interval(1 + sqrt(3), 3)], cognitive="Application")


def _c20():
    mx = sqrt(a_**2 + 9) + 2
    sols = [s for s in solve(Eq(mx, 7), a_) if s > 0]
    assert len(sols) == 1
    s = sols[0]
    assert ext(s*sin(x) + 3*cos(x) + 2, FULL)[1] == 7
    return s
q("U14-B-020", TOP_M, "Coefficient from a given maximum", "Medium", "Inverse/parameter MCQ",
  r"If the maximum value of $a\sin x + 3\cos x + 2$, $x \in \mathbb{R}$, is $7$, where $a > 0$, then $a$ equals",
  r"$4$",
  [(r"$2$", r"Takes the maximum as $a + 3 + 2 = 7$."),
   (r"$2\sqrt{10}$", r"Forgets the constant and solves $\sqrt{a^2 + 9} = 7$."),
   (r"$\sqrt{34}$", r"Adds instead of subtracting: $a^2 = 5^2 + 3^2$.")],
  r"The maximum is $\sqrt{a^2 + 9} + 2 = 7$, so $\sqrt{a^2 + 9} = 5$, $a^2 = 16$, and with $a > 0$, $a = 4$.",
  r"Using $a + b$ instead of $\sqrt{a^2 + b^2}$ for the amplitude.",
  "U14-B-asinbcos-inverse", r"Reverse use of the amplitude formula with a constant shift.",
  check=_c20, values=[4, 2, 2*sqrt(10), sqrt(34)], cognitive="Application",
  numerical=dict(question=r"If the maximum value of $a\sin x + 3\cos x + 2$, $x \in \mathbb{R}$, is $7$, where $a > 0$, then $a$ is", answer=4))


def _c21():
    lo, hi = ext(sin(x) + sqrt(3)*cos(x), FULL)
    return len([k for k in range(-10, 11) if lo <= k <= hi])
q("U14-B-021", TOP_M, "Integer values attained by a sin x + b cos x", "Medium", "Inverse/parameter MCQ",
  r"The number of integer values of $k$ for which the equation $\sin x + \sqrt{3}\cos x = k$ has at least one real solution is",
  r"$5$",
  [(r"$3$", r"Takes the range of the left side as $[-1, 1]$, like a single sine."),
   (r"$9$", r"Uses amplitude $1 + 3 = 4$, adding the squares without the square root."),
   (r"$4$", r"Excludes one endpoint, thinking $\pm 2$ cannot both be attained.")],
  r"$\sin x + \sqrt{3}\cos x = 2\sin\left(x + \frac{\pi}{3}\right)$ takes exactly the values in $[-2, 2]$. The equation is solvable iff $k \in [-2, 2]$, i.e. $k = -2, -1, 0, 1, 2$: $5$ values.",
  r"Using the wrong amplitude for $a\sin x + b\cos x$.",
  "U14-B-asinbcos-solvable", r"Solvability converted to the range of $a\sin x + b\cos x$, then counting.",
  check=_c21, values=[5, 3, 9, 4], cognitive="Application",
  numerical=dict(question=r"The number of integer values of $k$ for which the equation $\sin x + \sqrt{3}\cos x = k$ has at least one real solution is", answer=5))


def _c22():
    # k = -(t^2 - 4t) over t = sin x in [-1, 1]
    kt = solve(Eq(to_t(sin(x)**2 - 4*sin(x)) + Symbol('k'), 0), Symbol('k'))[0]
    return function_range(kt, t, Interval(-1, 1))
q("U14-B-022", TOP_M, "Solvability of a quadratic in sin x", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $k$ for which the equation $\sin^2 x - 4\sin x + k = 0$ has at least one real solution $x$ is",
  r"$[-5, 3]$",
  [(r"$(-\infty, 4]$", r"Uses only the discriminant condition $16 - 4k \ge 0$ for real $\sin x$, ignoring $|\sin x| \le 1$."),
   (r"$[-5, 4]$", r"Takes the vertex value $4$ (at $\sin x = 2$) as the largest $k$."),
   (r"$[0, 3]$", r"Allows only $\sin x \in [0, 1]$.")],
  r"Write $k = 4t - t^2$ with $t = \sin x \in [-1, 1]$. The vertex is at $t = 2$, outside $[-1,1]$, so $4t - t^2$ is increasing there, from $-5$ at $t = -1$ to $3$ at $t = 1$. Hence the equation is solvable exactly for $k \in [-5, 3]$.",
  r"Treating real roots of the quadratic as enough, without $|\sin x| \le 1$.",
  "U14-B-quad-sin-solvability", r"Trap: the discriminant condition is not sufficient; needs the range over $[-1,1]$ with an outside vertex.",
  check=_c22, values=[Interval(-5, 3), Interval(-oo, 4), Interval(-5, 4), Interval(0, 3)], cognitive="Analysis")

q("U14-B-023", TOP_M, "Maximum of a quadratic in sin x (vertex inside)", "Medium", "Multi-step computation MCQ",
  r"The maximum value of $\cos 2x + 3\sin x$, $x \in \mathbb{R}$, is",
  r"$\frac{17}{8}$",
  [(r"$2$", r"Evaluates only at $\sin x = 1$, missing the interior vertex at $\sin x = \frac{3}{4}$."),
   (r"$4$", r"Adds the separate maxima $1 + 3$ of $\cos 2x$ and $3\sin x$."),
   (r"$3$", r"Uses $\cos 2x = 1 - \sin^2 x$, so maximises $1 + 3t - t^2$ on $[-1,1]$ and gets $3$ at $t = 1$.")],
  r"With $t = \sin x$, $\cos 2x + 3\sin x = 1 - 2t^2 + 3t$. The vertex $t = \frac{3}{4}$ lies in $[-1, 1]$, giving $1 - \frac{9}{8} + \frac{9}{4} = \frac{17}{8}$.",
  r"Checking only endpoints of $[-1,1]$ or using a wrong double-angle formula.",
  "U14-B-quad-sin-vertex-max", r"Double-angle conversion, then a vertex inside $[-1,1]$.",
  check=lambda: function_range(to_t(cos(2*x) + 3*sin(x)), t, Interval(-1, 1)).sup,
  values=[Rational(17, 8), 2, 4, 3], cognitive="Application",
  numerical=dict(question=r"If $M$ is the maximum value of $\cos 2x + 3\sin x$, $x \in \mathbb{R}$, then the value of $8M$ is", answer=17))

q("U14-B-024", TOP_M, "Maximum after expanding a compound angle", "Medium", "Multi-step computation MCQ",
  r"The maximum value of $5\cos\theta + 3\cos\left(\theta + \frac{\pi}{3}\right) + 3$, $\theta \in \mathbb{R}$, is",
  r"$10$",
  [(r"$11$", r"Adds the separate maxima $5 + 3 + 3$."),
   (r"$3 + \sqrt{34}$", r"Treats the two cosines as $a\sin + b\cos$ with $a = 5$, $b = 3$ without expanding."),
   (r"$7$", r"Finds the amplitude $7$ correctly but drops the constant $3$.")],
  r"Expand: $3\cos\left(\theta + \frac{\pi}{3}\right) = \frac{3}{2}\cos\theta - \frac{3\sqrt{3}}{2}\sin\theta$. So the expression is $\frac{13}{2}\cos\theta - \frac{3\sqrt{3}}{2}\sin\theta + 3$, with amplitude $\sqrt{\frac{169}{4} + \frac{27}{4}} = 7$. The maximum is $7 + 3 = 10$.",
  r"Not expanding the compound angle before using $\sqrt{a^2 + b^2}$.",
  "U14-B-asinbcos-expand", r"Compound-angle expansion followed by the amplitude formula.",
  check=lambda: clean(maximum(5*cos(x) + 3*cos(x + pi/3) + 3, x, FULL)),
  values=[10, 11, 3 + sqrt(34), 7], cognitive="Application",
  numerical=dict(question=r"The maximum value of $5\cos\theta + 3\cos\left(\theta + \frac{\pi}{3}\right) + 3$, $\theta \in \mathbb{R}$, is", answer=10))

q("U14-B-025", TOP_M, "Maximum of a sum of two shifted sines", "Medium", "Multi-step computation MCQ",
  r"The maximum value of $\sin x + \sin\left(x + \frac{\pi}{3}\right)$, $x \in \mathbb{R}$, is",
  r"$\sqrt{3}$",
  [(r"$2$", r"Adds the separate maxima $1 + 1$, which cannot occur at the same $x$."),
   (r"$\frac{3}{2}$", r"Assumes the maximum is at $x = \frac{\pi}{2}$, giving $1 + \sin\frac{5\pi}{6}$."),
   (r"$2 + \frac{\sqrt{3}}{2}$", r"Writes $\sin\left(x + \frac{\pi}{3}\right)$ as $\sin x + \sin\frac{\pi}{3}$, so maximises $2\sin x + \frac{\sqrt{3}}{2}$.")],
  r"Expanding, $\sin x + \frac{1}{2}\sin x + \frac{\sqrt{3}}{2}\cos x = \frac{3}{2}\sin x + \frac{\sqrt{3}}{2}\cos x$, whose maximum is $\sqrt{\frac{9}{4} + \frac{3}{4}} = \sqrt{3}$.",
  r"Adding maxima of terms that peak at different $x$.",
  "U14-B-asinbcos-expand", r"Expansion then amplitude; tempting shortcut of adding maxima.",
  check=lambda: clean(maximum(sin(x) + sin(x + pi/3), x, FULL)),
  values=[sqrt(3), 2, Rational(3, 2), 2 + sqrt(3)/2], cognitive="Application")

q("U14-B-026", TOP_M, "Maximum via double-angle reduction", "Medium", "Multi-step computation MCQ",
  r"The maximum value of $\sin x(\sin x + \cos x)$, $x \in \mathbb{R}$, is",
  r"$\frac{1 + \sqrt{2}}{2}$",
  [(r"$\frac{\sqrt{2}}{2}$", r"Reduces to $\frac{1}{2} + \frac{1}{2}(\sin 2x - \cos 2x)$ but drops the constant $\frac{1}{2}$."),
   (r"$1 + \sqrt{2}$", r"Forgets the factor $\frac{1}{2}$ in both $\sin^2 x$ and $\sin x\cos x$."),
   (r"$\frac{3}{2}$", r"Adds the separate maxima $1$ of $\sin^2 x$ and $\frac{1}{2}$ of $\sin x\cos x$.")],
  r"$\sin^2 x + \sin x\cos x = \frac{1 - \cos 2x}{2} + \frac{\sin 2x}{2} = \frac{1}{2} + \frac{1}{2}(\sin 2x - \cos 2x)$. Since $\sin 2x - \cos 2x$ has maximum $\sqrt{2}$, the maximum is $\frac{1 + \sqrt{2}}{2}$.",
  r"Maximising $\sin^2 x$ and $\sin x\cos x$ separately.",
  "U14-B-double-angle-max", r"Double-angle reduction to $a\sin 2x + b\cos 2x + c$.",
  check=lambda: clean(maximum(sin(x)*(sin(x) + cos(x)), x, FULL)),
  values=[(1 + sqrt(2))/2, sqrt(2)/2, 1 + sqrt(2), Rational(3, 2)], cognitive="Application")

q("U14-B-027", TOP_F, "Period after factorising a difference of fourth powers", "Medium", "Multi-step computation MCQ",
  r"The fundamental period of $f(x) = \sin^4 x - \cos^4 x + \sin 2x$ is",
  r"$\pi$",
  [(r"$\frac{\pi}{2}$", r"Assumes the fourth powers reduce to $\cos 4x$, as for $\sin^4 x + \cos^4 x$, giving period $\frac{\pi}{2}$."),
   (r"$2\pi$", r"Takes the common period $2\pi$ of $\sin x$ and $\cos x$."),
   (r"$\frac{\pi}{4}$", r"Halves the period $\frac{\pi}{2}$ again for the fourth powers.")],
  r"$\sin^4 x - \cos^4 x = (\sin^2 x - \cos^2 x)(\sin^2 x + \cos^2 x) = -\cos 2x$. So $f(x) = \sin 2x - \cos 2x = \sqrt{2}\sin\left(2x - \frac{\pi}{4}\right)$, whose fundamental period is $\frac{2\pi}{2} = \pi$.",
  r"Reading the period off the powers instead of simplifying the expression.",
  "U14-B-period-diff-fourth-powers", r"Factorise the difference of squares, then combine into one sinusoid.",
  check=lambda: fund_period(sin(x)**4 - cos(x)**4 + sin(2*x)),
  values=[pi, pi/2, 2*pi, pi/4], cognitive="Application")

q("U14-B-028", TOP_F, "Period of a difference of tangent and cotangent", "Medium", "Multi-step computation MCQ",
  r"The fundamental period of $f(x) = \tan x - \cot x$ is",
  r"$\frac{\pi}{2}$",
  [(r"$\pi$", r"Takes the common period $\pi$ of $\tan x$ and $\cot x$ without simplifying."),
   (r"$2\pi$", r"Uses $2\pi$ as the period of tangent and cotangent."),
   (r"$\frac{\pi}{4}$", r"Reaches $-2\cot 2x$ but takes the period of $\cot 2x$ as $\frac{\pi}{4}$, halving twice.")],
  r"$\tan x - \cot x = \frac{\sin^2 x - \cos^2 x}{\sin x\cos x} = \frac{-\cos 2x}{\frac{1}{2}\sin 2x} = -2\cot 2x$, whose fundamental period is $\frac{\pi}{2}$.",
  r"Assuming the sum of two functions with period $\pi$ has fundamental period $\pi$.",
  "U14-B-period-combination", r"Simplify to $-2\cot 2x$; the trap is the obvious answer $\pi$.",
  check=lambda: fund_period(tan(x) - cot(x)),
  values=[pi/2, pi, 2*pi, pi/4], cognitive="Analysis")

q("U14-B-029", TOP_F, "Period of a sum with pi x arguments", "Medium", "Single-step computation MCQ",
  r"The fundamental period of $f(x) = \sin(\pi x) + \cos\left(\frac{2\pi x}{3}\right)$ is",
  r"$6$",
  [(r"$6\pi$", r"Applies $\frac{2\pi}{k}$ as if the coefficients were $1$ and $\frac{2}{3}$, losing the $\pi$ inside the argument."),
   (r"$3$", r"Takes the larger of the periods $2$ and $3$."),
   (r"$5$", r"Adds the periods $2$ and $3$.")],
  r"$\sin(\pi x)$ has period $\frac{2\pi}{\pi} = 2$ and $\cos\left(\frac{2\pi x}{3}\right)$ has period $\frac{2\pi}{2\pi/3} = 3$. The sum has period $\operatorname{LCM}(2, 3) = 6$; at $x \to x + 3$ the sine term changes sign, so $3$ fails.",
  r"Losing the factor $\pi$ in the argument, or not taking an LCM.",
  "U14-B-period-lcm", r"Two periods with $\pi$ in the argument, then an LCM.",
  check=lambda: fund_period(sin(pi*x) + cos(2*pi*x/3)),
  values=[6, 6*pi, 3, 5], cognitive="Application",
  numerical=dict(question=r"The fundamental period of $f(x) = \sin(\pi x) + \cos\left(\frac{2\pi x}{3}\right)$ is", answer=6))


def _c30():
    return (fund_period(Abs(sin(x)) + Abs(cos(x))) == pi, fund_period(sin(x)**3) == 2*pi)
q("U14-B-030", TOP_F, "Periods involving modulus and odd powers", "Medium", "Statement-based MCQ",
  r"Statement I: The fundamental period of $|\sin x| + |\cos x|$ is $\pi$. Statement II: The fundamental period of $\sin^3 x$ is $2\pi$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Takes the period $\pi$ of each of $|\sin x|$, $|\cos x|$ as the period of the sum."),
   (ST_TF, r"Accepts $\pi$ for the sum and wrongly halves the period for the odd power $\sin^3 x$."),
   (ST_FF, r"Correctly rejects Statement I but wrongly halves the period of $\sin^3 x$ to $\pi$.")],
  r"Shifting by $\frac{\pi}{2}$ swaps $|\sin x|$ and $|\cos x|$, so the sum has period $\frac{\pi}{2}$ (and no smaller, as the value is $1$ at $x = 0$ but $\sqrt{2}$ at $x = \frac{\pi}{4}$); Statement I is false. $\sin^3(x + \pi) = -\sin^3 x$, so $\pi$ is not a period, while $2\pi$ is; Statement II is true.",
  r"Halving the period for odd powers, or not noticing the $\frac{\pi}{2}$ symmetry of $|\sin x| + |\cos x|$.",
  "U14-B-stmt-period-abs-power", r"Two period facts, one with a trap.",
  check=_c30, values=[FT, TT, TF, FF], cognitive="Analysis")


# =================================================================== Q31-Q44

def _c31():
    _mp.mp.dps = 20
    g = lambdify(x, cos(sin(x)) - sin(cos(x)), 'mpmath')
    s1 = min(g(_mp.mpf(i)*2*_mp.pi/4000) for i in range(4001)) > 0
    s2 = N(sin(2) + cos(2), 30) > 0
    return (bool(s1), bool(s2))
q("U14-B-031", TOP_S, "Comparing composite trigonometric values", "Medium", "Statement-based MCQ",
  r"Statement I: $\cos(\sin x) > \sin(\cos x)$ for every real $x$. Statement II: $\sin 2 + \cos 2 > 0$ (angles in radians). In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FT, r"Expects the two sides to meet near $x = 0$, since $\sin(\cos 0) = \sin 1$ is close to $1 = \cos(\sin 0)$, and rejects Statement I."),
   (ST_TF, r"Believes $2$ rad lies beyond $\frac{3\pi}{4}$, where $|\cos x| > \sin x$, so takes $\sin 2 + \cos 2 < 0$."),
   (ST_FF, r"Rejects Statement I as if the sides meet near $x = 0$, and also places $2$ rad beyond $\frac{3\pi}{4}$.")],
  r"$\sin(\cos x) = \cos\left(\frac{\pi}{2} - \cos x\right)$. Since $|\sin x| + |\cos x| \le \sqrt{2} < \frac{\pi}{2}$, we get $|\sin x| < \frac{\pi}{2} - \cos x$, with both $|\sin x|$ and $\frac{\pi}{2} - \cos x$ in $[0, \pi]$, where cosine decreases. Hence $\cos(\sin x) > \sin(\cos x)$, so Statement I is true. $\sin 2 + \cos 2 = \sqrt{2}\sin\left(2 + \frac{\pi}{4}\right)$, and $\frac{\pi}{2} < 2 < \frac{3\pi}{4} \approx 2.36$ gives $\frac{3\pi}{4} < 2 + \frac{\pi}{4} < \pi$, where sine is positive; Statement II is true.",
  r"Not converting $\sin(\cos x)$ into a cosine to compare arguments.",
  "U14-B-stmt-compare-composite", r"Comparison of composite functions needs a bound $|\sin x| + |\cos x| \le \sqrt{2}$; Statement II needs locating $2$ rad against $\frac{3\pi}{4}$.",
  check=_c31, values=[TT, FT, TF, FF], cognitive="Analysis")

q("U14-B-032", TOP_F, "Domain of reciprocal square root", "Medium", "Multi-step computation MCQ",
  r"The set of all $x \in [0, 2\pi)$ for which $f(x) = \frac{1}{\sqrt{\sin x - \cos x}}$ is defined is",
  r"$\left(\frac{\pi}{4}, \frac{5\pi}{4}\right)$",
  [(r"$\left[\frac{\pi}{4}, \frac{5\pi}{4}\right]$", r"Includes the points where $\sin x = \cos x$, where the denominator is $0$."),
   (r"$(0, \pi)$", r"Uses only $\sin x > 0$."),
   (r"$\left[0, \frac{\pi}{4}\right) \cup \left(\frac{5\pi}{4}, 2\pi\right)$", r"Reverses the inequality to $\sin x < \cos x$.")],
  r"We need $\sin x - \cos x > 0$, i.e. $\sqrt{2}\sin\left(x - \frac{\pi}{4}\right) > 0$, so $0 < x - \frac{\pi}{4} < \pi$. Within $[0, 2\pi)$ this is $\frac{\pi}{4} < x < \frac{5\pi}{4}$.",
  r"Allowing a zero under a square root that sits in a denominator.",
  "U14-B-domain-sqrt-interval", r"Combine into one sine, then a strict inequality.",
  check=lambda: solveset(sin(x) - cos(x) > 0, x, Interval.Ropen(0, 2*pi)),
  values=[Interval.open(pi/4, 5*pi/4), Interval(pi/4, 5*pi/4), Interval.open(0, pi), Union(Interval.Ropen(0, pi/4), Interval.open(5*pi/4, 2*pi))],
  cognitive="Application")


def _c33():
    # cos(cos x) > 0 always: min of cos(v) for v = cos x in [-1, 1]
    assert minimum(cos(u), u, Interval(-1, 1)) > 0
    # sin(sin x) >= 0 iff sin x lies where sin(v) >= 0 for v in [-1, 1]
    vset = solveset(sin(u) >= 0, u, Interval(-1, 1))
    assert vset == Interval(0, 1)
    return solveset(sin(x) >= vset.inf, x, Interval.Ropen(0, 2*pi))
q("U14-B-033", TOP_F, "Domain of composite trigonometric functions", "Medium", "Multi-step computation MCQ",
  r"The set of all $x \in [0, 2\pi)$ for which $f(x) = \sqrt{\cos(\cos x)} + \sqrt{\sin(\sin x)}$ is real is",
  r"$[0, \pi]$",
  [(r"$[0, 2\pi)$", r"Assumes both radicands are always non-negative because $\sin x$ and $\cos x$ lie in $[-1, 1]$."),
   (r"$\left[0, \frac{\pi}{2}\right] \cup \left[\frac{3\pi}{2}, 2\pi\right)$", r"Requires $\cos x \ge 0$, attaching the sign condition to the wrong inner function."),
   (r"$(0, \pi)$", r"Demands $\sin(\sin x) > 0$ strictly, wrongly excluding $x = 0$ and $x = \pi$ where the radicand is $0$.")],
  r"Since $|\cos x| \le 1 < \frac{\pi}{2}$, $\cos(\cos x) > 0$ always. For the second term, $\sin x \in [-1, 1] \subset (-\pi, \pi)$, and on this interval $\sin v \ge 0$ iff $v \ge 0$; so we need $\sin x \ge 0$. In $[0, 2\pi)$ this gives $[0, \pi]$, the endpoints included since $\sqrt{0}$ is real.",
  r"Assuming a composite like $\sin(\sin x)$ is always non-negative.",
  "U14-B-domain-composite", r"Two composite radicands analysed through the range of the inner function.",
  check=_c33,
  values=[Interval(0, pi), Interval.Ropen(0, 2*pi), Union(Interval(0, pi/2), Interval.Ropen(3*pi/2, 2*pi)), Interval.open(0, pi)],
  cognitive="Analysis")


def _c34():
    part1 = solveset(16 - x**2 >= 0, x, S.Reals)
    # sin x > 0 for x in [-4, 0): put x = -y, y in (0, 4], need sin y < 0
    y = Symbol('y', real=True)
    neg = solveset(sin(y) < 0, y, Interval.Lopen(0, 4))
    neg_x = Interval(-neg.sup, -neg.inf, neg.right_open, neg.left_open)
    pos = solveset(sin(x) > 0, x, Interval(0, 4))
    return Intersection(part1, Union(neg_x, pos))
q("U14-B-034", TOP_F, "Domain combining an algebraic and a log condition", "Medium", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sqrt{16 - x^2} + \log_e(\sin x)$ is",
  r"$[-4, -\pi) \cup (0, \pi)$",
  [(r"$(0, \pi)$", r"Uses only the principal arch $(0, \pi)$ of $\sin x > 0$ and misses the part of $(-2\pi, -\pi)$ inside $[-4, 4]$."),
   (r"$(-4, -\pi) \cup (0, \pi)$", r"Excludes $x = -4$, requiring $16 - x^2 > 0$ although the square root allows $0$."),
   (r"$[-4, -\pi] \cup [0, \pi]$", r"Uses $\sin x \ge 0$, including the zeros of $\sin x$ where the logarithm is undefined.")],
  r"We need $-4 \le x \le 4$ and $\sin x > 0$. Sine is positive on $(0, \pi)$ and on $(-2\pi, -\pi)$; since $-2\pi < -4 < -\pi$ and $\pi < 4$, the intersection is $[-4, -\pi) \cup (0, \pi)$.",
  r"Looking for $\sin x > 0$ only on $(0, \pi)$.",
  "U14-B-domain-combined", r"Intersect an algebraic interval with sign regions of sine on both sides of $0$.",
  check=_c34,
  values=[Union(Interval.Ropen(-4, -pi), Interval.open(0, pi)), Interval.open(0, pi),
          Union(Interval.open(-4, -pi), Interval.open(0, pi)), Union(Interval(-4, -pi), Interval(0, pi))],
  cognitive="Analysis")

q("U14-B-035", TOP_F, "Integers in the domain of sqrt(sin x)", "Medium", "Multi-step computation MCQ",
  r"The number of integers $n$ with $0 \le n \le 10$ for which $\sqrt{\sin n}$ is a real number ($n$ in radians) is",
  r"$7$",
  [(r"$6$", r"Excludes $n = 0$, thinking $\sin 0 = 0$ is not allowed under the square root."),
   (r"$4$", r"Counts only $n \in [0, \pi]$, i.e. $0, 1, 2, 3$, missing the next arch."),
   (r"$8$", r"Takes $2\pi \approx 6$, so includes $n = 6$ although $\sin 6 < 0$.")],
  r"We need $\sin n \ge 0$, i.e. $n \in [0, \pi] \cup [2\pi, 3\pi]$ within $[0, 10]$, with $\pi \approx 3.14$, $2\pi \approx 6.28$, $3\pi \approx 9.42$. The integers are $0, 1, 2, 3$ and $7, 8, 9$: $7$ values.",
  r"Using rough values of $2\pi$ that move an integer across a boundary.",
  "U14-B-domain-integer-count", r"Sign of sine over two arches with careful decimal boundaries.",
  check=lambda: len([n for n in range(0, 11) if N(sin(n), 30) >= 0]),
  values=[7, 6, 4, 8], cognitive="Application",
  numerical=dict(question=r"The number of integers $n$ with $0 \le n \le 10$ for which $\sqrt{\sin n}$ is a real number ($n$ in radians) is", answer=7))


def _c36():
    return tuple(sorted([sin(1), sin(2), sin(3)], key=lambda v: N(v)))
q("U14-B-036", TOP_S, "Ordering sines of radian angles", "Medium", "Conceptual/application MCQ",
  r"Which of the following orderings is true? (Angles are in radians.)",
  r"$\sin 3 < \sin 1 < \sin 2$",
  [(r"$\sin 1 < \sin 2 < \sin 3$", r"Treats sine as increasing on $[1, 3]$, as it would be for small degree measures."),
   (r"$\sin 3 < \sin 2 < \sin 1$", r"Reduces $\sin 3$ correctly but thinks $1$ rad is nearer to $\frac{\pi}{2}$ than $2$ rad is."),
   (r"$\sin 1 < \sin 3 < \sin 2$", r"Sees that $\sin 2$ is largest but treats $3$ rad as still close to $\frac{\pi}{2}$, ranking $\sin 3$ above $\sin 1$.")],
  r"$\sin 2 = \sin(\pi - 2) \approx \sin 1.14$ and $\sin 3 = \sin(\pi - 3) \approx \sin 0.14$. All of $0.14, 1, 1.14$ lie in $\left(0, \frac{\pi}{2}\right)$ where sine increases, so $\sin 3 < \sin 1 < \sin 2$.",
  r"Not reducing obtuse radian angles via $\sin(\pi - x)$ before comparing.",
  "U14-B-compare-sin-radians", r"Reduce two angles to the first quadrant, then use monotonicity.",
  check=_c36,
  values=[(sin(3), sin(1), sin(2)), (sin(1), sin(2), sin(3)), (sin(3), sin(2), sin(1)), (sin(1), sin(3), sin(2))],
  cognitive="Analysis")


def _c37():
    return tuple(sorted([tan(1), tan(2), tan(3), tan(4)], key=lambda v: N(v)))
q("U14-B-037", TOP_S, "Ordering tangents of radian angles", "Difficult", "Conceptual/application MCQ",
  r"Which of the following orderings is correct? (Angles are in radians.)",
  r"$\tan 2 < \tan 3 < \tan 4 < \tan 1$",
  [(r"$\tan 1 < \tan 2 < \tan 3 < \tan 4$", r"Treats $\tan x$ as increasing on $[1, 4]$, ignoring the asymptote at $\frac{\pi}{2}$."),
   (r"$\tan 3 < \tan 2 < \tan 4 < \tan 1$", r"Thinks $\tan$ becomes more negative further into the second quadrant, so ranks $\tan 3$ below $\tan 2$."),
   (r"$\tan 2 < \tan 3 < \tan 1 < \tan 4$", r"Reduces $\tan 4 = \tan(4 - \pi)$ but overestimates $4 - \pi$ as more than $1$.")],
  r"$\tan 2$ and $\tan 3$ are negative (second quadrant) and $\tan$ increases on $\left(\frac{\pi}{2}, \pi\right)$, so $\tan 2 < \tan 3 < 0$. Also $\tan 4 = \tan(4 - \pi)$ with $4 - \pi \approx 0.86 < 1$, so $0 < \tan 4 < \tan 1$. Hence $\tan 2 < \tan 3 < \tan 4 < \tan 1$.",
  r"Ignoring that $\tan$ restarts after each asymptote.",
  "U14-B-compare-tan-radians", r"Four angles across three branches; signs, monotonicity per branch, and a reduction by $\pi$.",
  check=_c37,
  values=[(tan(2), tan(3), tan(4), tan(1)), (tan(1), tan(2), tan(3), tan(4)), (tan(3), tan(2), tan(4), tan(1)), (tan(2), tan(3), tan(1), tan(4))],
  cognitive="Analysis")

q("U14-B-038", TOP_S, "Counting negative cosines at integer radians", "Medium", "Multi-step computation MCQ",
  r"Among the ten numbers $\cos 1, \cos 2, \cos 3, \ldots, \cos 10$ (angles in radians), the number of negative numbers is",
  r"$6$",
  [(r"$3$", r"Considers only the first turn, where $2, 3, 4$ lie in $\left(\frac{\pi}{2}, \frac{3\pi}{2}\right)$."),
   (r"$7$", r"Places $5$ rad in the third quadrant, though $5 > \frac{3\pi}{2} \approx 4.71$."),
   (r"$5$", r"Takes $\frac{7\pi}{2}$ as about $9.4$ (confusing it with $3\pi$), so excludes $n = 10$ from $\left(\frac{5\pi}{2}, \frac{7\pi}{2}\right)$.")],
  r"$\cos n < 0$ iff $n$ lies in $\left(\frac{\pi}{2}, \frac{3\pi}{2}\right) \approx (1.57, 4.71)$ or in $\left(\frac{5\pi}{2}, \frac{7\pi}{2}\right) \approx (7.85, 11.0)$. This gives $n = 2, 3, 4$ and $n = 8, 9, 10$: $6$ numbers.",
  r"Forgetting the second turn, or rough decimal values of multiples of $\frac{\pi}{2}$.",
  "U14-B-sign-count", r"Sign of cosine over two turns with decimal boundaries.",
  check=lambda: len([n for n in range(1, 11) if N(cos(n), 30) < 0]),
  values=[6, 3, 7, 5], cognitive="Application",
  numerical=dict(question=r"Among the ten numbers $\cos 1, \cos 2, \cos 3, \ldots, \cos 10$ (angles in radians), the number of negative numbers is", answer=6))


def _c39():
    e = sqrt((1 + sin(th))/(1 - sin(th)))
    return tuple(N(e.subs(th, v), 30) for v in (2, Rational(5, 2), Rational(29, 10)))
_opts39 = [-(sec(th) + tan(th)), sec(th) + tan(th), sec(th) - tan(th), tan(th) - sec(th)]
q("U14-B-039", TOP_S, "Simplifying a square root using the quadrant", "Medium", "Multi-step computation MCQ",
  r"If $\frac{\pi}{2} < \theta < \pi$, then $\sqrt{\frac{1 + \sin\theta}{1 - \sin\theta}}$ equals",
  r"$-(\sec\theta + \tan\theta)$",
  [(r"$\sec\theta + \tan\theta$", r"Takes $\sqrt{\cos^2\theta} = \cos\theta$, ignoring that $\cos\theta < 0$ here."),
   (r"$\sec\theta - \tan\theta$", r"Inverts the fraction under the root and also takes $\sqrt{\cos^2\theta} = \cos\theta$."),
   (r"$\tan\theta - \sec\theta$", r"Inverts the fraction under the root but handles the sign of $\cos\theta$ correctly.")],
  r"Multiply inside by $\frac{1 + \sin\theta}{1 + \sin\theta}$: the expression is $\frac{1 + \sin\theta}{\sqrt{\cos^2\theta}} = \frac{1 + \sin\theta}{|\cos\theta|}$. In the second quadrant $|\cos\theta| = -\cos\theta$, so it equals $-\frac{1 + \sin\theta}{\cos\theta} = -(\sec\theta + \tan\theta)$.",
  r"Writing $\sqrt{\cos^2\theta} = \cos\theta$ in a quadrant where cosine is negative.",
  "U14-B-sign-sqrt-simplify", r"Rationalise, then use the sign of cosine in the quadrant.",
  check=_c39,
  values=[tuple(N(o.subs(th, v), 30) for v in (2, Rational(5, 2), Rational(29, 10))) for o in _opts39],
  cognitive="Application")

q("U14-B-040", TOP_G, "Sine curve against a parabola", "Medium", "Graph/diagram MCQ",
  r"The number of real solutions of $\sin x = x^2$ is",
  r"$2$",
  [(r"$1$", r"Notices only the obvious root $x = 0$."),
   (r"$3$", r"Assumes a symmetric second intersection for $x < 0$ as well."),
   (r"$4$", r"Assumes two crossings on each side of the origin.")],
  r"For $|x| > 1$, $x^2 > 1 \ge \sin x$, so roots lie in $[-1, 1]$. For $-1 \le x < 0$, $\sin x < 0 < x^2$, so no root. At $x = 0$ both are $0$; near $0^+$, $\sin x \approx x > x^2$, while at $x = 1$, $\sin 1 < 1$, so there is exactly one root in $(0, 1)$ (the parabola is convex, the sine concave there). Total: $2$.",
  r"Assuming symmetry between $\sin x$ (odd) and $x^2$ (even).",
  "U14-B-graph-poly-count", r"Bound the region, then compare concave and convex curves.",
  check=lambda: count_roots(sin(x) - x**2, -3, 3),
  values=[2, 1, 3, 4], cognitive="Analysis")


def _c41():
    eps = Rational(1, 10**6)
    tot = 0
    for k in range(3):
        lo, hi = -pi/2 + k*pi + eps, pi/2 + k*pi - eps
        tot += count_roots(tan(x) - x, lo, hi)
    return tot
q("U14-B-041", TOP_G, "Tangent curve against the line y = x", "Medium", "Graph/diagram MCQ",
  r"The number of solutions of $\tan x = x$ in the interval $\left(-\frac{\pi}{2}, \frac{5\pi}{2}\right)$ (where $\tan x$ is defined) is",
  r"$3$",
  [(r"$2$", r"Ignores the root $x = 0$ as trivial."),
   (r"$4$", r"Counts $x = 0$ separately and again as the intersection on the first branch."),
   (r"$6$", r"Expects two intersections of the line with each branch.")],
  r"On each branch $\left(k\pi - \frac{\pi}{2}, k\pi + \frac{\pi}{2}\right)$, $\tan x - x$ is increasing (derivative $\tan^2 x \ge 0$) and goes from $-\infty$ to $+\infty$, so it has exactly one zero. The interval contains three branches ($k = 0, 1, 2$), giving $3$ solutions, one of which is $x = 0$.",
  r"Miscounting intersections per branch of $\tan x$.",
  "U14-B-graph-tan-line", r"Monotonicity of $\tan x - x$ on each branch.",
  check=_c41, values=[3, 2, 4, 6], cognitive="Analysis")

def _c42():
    lo, hi = ext(8*(sin(x)**6 + cos(x)**6), Interval(0, pi))
    return len(range(int(ceiling(lo)), int(floor(hi)) + 1))
q("U14-B-042", TOP_M, "Integers in the range of a sum of sixth powers", "Medium", "Multi-step computation MCQ",
  r"The number of integers in the range of $f(x) = 8(\sin^6 x + \cos^6 x)$, $x \in \mathbb{R}$, is",
  r"$7$",
  [(r"$3$", r"Uses $a^3 + b^3 = (a + b)^3 - ab(a + b)$, dropping the factor $3$, so the minimum is $8\left(1 - \frac{1}{4}\right) = 6$ and the range is $[6, 8]$."),
   (r"$9$", r"Minimises $\sin^6 x$ and $\cos^6 x$ separately, taking the minimum as $0$ and the range as $[0, 8]$."),
   (r"$13$", r"Writes $\sin^2 x\cos^2 x = \frac{1}{2}\sin^2 2x$, so the minimum becomes $8\left(1 - \frac{3}{2}\right) = -4$ and the range $[-4, 8]$.")],
  r"With $a = \sin^2 x$, $b = \cos^2 x$, $a + b = 1$: $a^3 + b^3 = (a + b)^3 - 3ab(a + b) = 1 - 3\sin^2 x\cos^2 x = 1 - \frac{3}{4}\sin^2 2x$. As $0 \le \sin^2 2x \le 1$ with both ends attained, $f$ ranges over $\left[8 \cdot \frac{1}{4}, 8\right] = [2, 8]$, which contains the $7$ integers $2, 3, \ldots, 8$.",
  r"Minimising the two sixth powers independently or mishandling the cube identity.",
  "U14-B-sixth-power-range", r"Cube identity, double-angle reduction, then a bound and an integer count.",
  check=_c42, values=[7, 3, 9, 13], cognitive="Application",
  numerical=dict(question=r"The number of integers in the range of $f(x) = 8(\sin^6 x + \cos^6 x)$, $x \in \mathbb{R}$, is", answer=7))

q("U14-B-043", TOP_G, "Sine curve against a decaying exponential", "Difficult", "Graph/diagram MCQ",
  r"The number of solutions of $\sin x = e^{-x}$ in the interval $[0, 4\pi]$ is",
  r"$4$",
  [(r"$2$", r"Finds the two crossings on $(0, \pi)$ and assumes $e^{-x}$ never meets the later arches."),
   (r"$3$", r"Treats $e^{-x}$ as $0$ for large $x$ and counts the interior zeros $\pi, 2\pi, 3\pi$ of $\sin x$."),
   (r"$8$", r"Assumes two crossings in every interval of length $\pi$.")],
  r"Since $e^{-x} > 0$, solutions need $\sin x > 0$: $x \in (0, \pi) \cup (2\pi, 3\pi)$. On each such arch $\sin x$ rises from $0$ to $1$ and back to $0$, while $0 < e^{-x} < 1$ there and is decreasing, so the curves cross exactly twice per arch (once near each end). Total $2 \times 2 = 4$.",
  r"Assuming a tiny positive curve cannot cross the later arches.",
  "U14-B-graph-exp-count", r"Sign restriction, then crossings near both ends of each arch; easy to undercount.",
  check=lambda: count_roots(sin(x) - exp(-x), 0, 4*pi),
  values=[4, 2, 3, 8], cognitive="Analysis")

q("U14-B-044", TOP_M, "Attaining the maximum of a sin x + b cos x", "Medium", "Conceptual/application MCQ",
  r"The number of values of $x \in [0, 2\pi]$ for which $2\sin x + \sqrt{5}\cos x = 3$ is",
  r"$1$",
  [(r"$2$", r"Assumes a horizontal line always meets a sinusoid twice per period."),
   (r"$0$", r"Takes the amplitude as $\sqrt{2^2 + \sqrt{5}}$, which is less than $3$."),
   (r"$4$", r"Counts two solutions in each half of $[0, 2\pi]$.")],
  r"$2\sin x + \sqrt{5}\cos x = 3\sin(x + \alpha)$ with amplitude $\sqrt{4 + 5} = 3$. So the equation means $\sin(x + \alpha) = 1$, the maximum, attained once per period. In $[0, 2\pi]$ there is exactly one such $x$ (the value at $x = 0$ is $\sqrt{5} \ne 3$, so the endpoints do not double count).",
  r"Treating a line at the maximum value like a generic horizontal line.",
  "U14-B-asinbcos-attain", r"Recognise the right side equals the amplitude: tangency, not crossing.",
  check=lambda: len(solveset(2*sin(x) + sqrt(5)*cos(x) - 3, x, Interval(0, 2*pi))),
  values=[1, 2, 0, 4], cognitive="Analysis")


# =================================================================== Q45-Q55 (Difficult)

q("U14-B-045", TOP_G, "Sine curve against a line through the origin", "Difficult", "Graph/diagram MCQ",
  r"The number of real solutions of $\sin x = \frac{x}{10}$ is",
  r"$7$",
  [(r"$6$", r"Counts the intersections on the arches but forgets $x = 0$."),
   (r"$4$", r"Counts only $x \ge 0$ and does not use the odd symmetry."),
   (r"$9$", r"Assumes two intersections on each positive arch $(0, \pi)$ and $(2\pi, 3\pi)$, then reflects.")],
  r"Roots satisfy $|x| \le 10$. For $x > 0$: on $(0, \pi)$ the line meets the arch once (besides $x = 0$, since the slope $\frac{1}{10} < 1$); on $(\pi, 2\pi)$ sine is negative, no root; on $(2\pi, 3\pi) \approx (6.28, 9.42)$ the line is below $1$, so it meets the arch twice; beyond $3\pi$ up to $10$, sine is negative. That is $3$ positive roots, $3$ negative by symmetry, plus $x = 0$: total $7$.",
  r"Forgetting the root at the origin or the symmetric negative roots.",
  "U14-B-graph-line-count", r"Arch-by-arch analysis on both sides with an odd symmetry.",
  check=lambda: count_roots(sin(x) - x/10, -11, 11),
  values=[7, 6, 4, 9], cognitive="Analysis",
  numerical=dict(question=r"The number of real solutions of $\sin x = \frac{x}{10}$ is", answer=7))

q("U14-B-046", TOP_G, "Sine curve against a logarithm", "Difficult", "Graph/diagram MCQ",
  r"The number of real solutions of $\sin x = \log_{10} x$ is",
  r"$3$",
  [(r"$2$", r"Counts only one intersection on the arch $(2\pi, 3\pi)$."),
   (r"$1$", r"Considers only the first arch $(0, \pi)$."),
   (r"$4$", r"Counts two intersections on each of the arches $(0, \pi)$ and $(2\pi, 3\pi)$.")],
  r"We need $0 < x \le 10$ (as $\log_{10} x \le 1$). On $(0, 1)$ the log is negative while $\sin x > 0$: no root. On $[1, \pi)$ the log rises from $0$ to about $0.5$ while $\sin x$ falls to $0$ after its peak, giving one root. On $(\pi, 2\pi)$, $\sin x < 0 < \log_{10} x$. On $(2\pi, 3\pi) \approx (6.28, 9.42)$, $\log_{10} x$ stays between about $0.80$ and $0.97$, below the peak $1$, so two roots. Beyond $3\pi$, $\sin x < 0$. Total $3$.",
  r"Misjudging whether $\log_{10} x$ stays below the second arch's peak.",
  "U14-B-graph-log-count", r"Bounding the log curve on each arch.",
  check=lambda: count_roots(sin(x) - log(x, 10), Rational(1, 100), 11),
  values=[3, 2, 1, 4], cognitive="Analysis",
  numerical=dict(question=r"The number of real solutions of $\sin x = \log_{10} x$ is", answer=3))


def _c47():
    s = Symbol('s', positive=True)  # s = sin^2 x in (0, 1]
    g = 9*s + 16/s
    crit = [c for c in solve(diff(g, s), s) if 0 < c <= 1]
    cands = [g.subs(s, c) for c in crit] + [g.subs(s, 1)]
    # g -> oo as s -> 0+, so the minimum is the least candidate
    return Min(*cands)
q("U14-B-047", TOP_M, "AM-GM equality case outside the range", "Difficult", "Multi-step computation MCQ",
  r"The minimum value of $9\sin^2 x + \frac{16}{\sin^2 x}$, over all real $x$ with $\sin x \ne 0$, is",
  r"$25$",
  [(r"$24$", r"Applies AM-GM, $\ge 2\sqrt{9 \cdot 16} = 24$, without checking that equality needs $\sin^2 x = \frac{4}{3}$, impossible."),
   (r"$12$", r"Uses AM-GM without the factor $2$: $\sqrt{9 \cdot 16}$."),
   (r"$16$", r"Minimises the two terms separately: $0 + 16$.")],
  r"Let $s = \sin^2 x \in (0, 1]$ and $g(s) = 9s + \frac{16}{s}$. Then $g'(s) = 9 - \frac{16}{s^2} < 0$ for $s \le 1$, since the critical point $s = \frac{4}{3}$ lies outside. So $g$ decreases on $(0, 1]$ and the minimum is $g(1) = 25$.",
  r"Using the AM-GM bound when its equality case is unattainable.",
  "U14-B-amgm-trap", r"Trap: AM-GM equality case is outside $(0,1]$; needs monotonicity.",
  check=_c47, values=[25, 24, 12, 16], cognitive="Analysis")


def _c48():
    _mp.mp.dps = 40
    f = lambda v: _mp.power(2, _mp.sin(v)) + _mp.power(2, _mp.cos(v))
    df = lambda v: _mp.log(2)*(_mp.cos(v)*_mp.power(2, _mp.sin(v)) - _mp.sin(v)*_mp.power(2, _mp.cos(v)))
    grid = [_mp.mpf(i)*2*_mp.pi/2000 for i in range(2000)]
    v0 = min(grid, key=f)
    root = _mp.findroot(df, v0)
    return Float(f(root), 35)
q("U14-B-048", TOP_M, "Minimum of a sum of exponentials of sine and cosine", "Difficult", "Multi-step computation MCQ",
  r"The minimum value of $2^{\sin x} + 2^{\cos x}$, $x \in \mathbb{R}$, is",
  r"$2^{1 - \frac{1}{\sqrt{2}}}$",
  [(r"$\frac{3}{2}$", r"Tries $\sin x = -1$, $\cos x = 0$, giving $\frac{1}{2} + 1$, and assumes this is least."),
   (r"$2^{1 + \frac{1}{\sqrt{2}}}$", r"Uses the maximum $\sqrt{2}$ of $\sin x + \cos x$ instead of the minimum $-\sqrt{2}$."),
   (r"$2^{1 - \sqrt{2}}$", r"Uses $2 \cdot 2^{\sin x + \cos x}$, forgetting to halve the exponent in AM-GM.")],
  r"By AM-GM, $2^{\sin x} + 2^{\cos x} \ge 2\sqrt{2^{\sin x + \cos x}} = 2^{1 + \frac{\sin x + \cos x}{2}}$. Since $\sin x + \cos x \ge -\sqrt{2}$, this is at least $2^{1 - \frac{\sqrt{2}}{2}} = 2^{1 - \frac{1}{\sqrt{2}}}$. Both equalities hold at $x = \frac{5\pi}{4}$, where $\sin x = \cos x = -\frac{1}{\sqrt{2}}$.",
  r"Testing only the points where $\sin x$ or $\cos x$ is $\pm 1$.",
  "U14-B-exp-sum-min", r"AM-GM combined with the range of $\sin x + \cos x$, plus checking equality.",
  check=_c48,
  values=[2**(1 - 1/sqrt(2)), Rational(3, 2), 2**(1 + 1/sqrt(2)), 2**(1 - sqrt(2))], cognitive="Analysis")


def _c49():
    lo, hi = ext(3*sin(x) + 4*cos(x), FULL)
    return function_range(u**2 - 6*u, u, Interval(lo, hi))
q("U14-B-049", TOP_M, "Range of a quadratic in a sin x + b cos x", "Difficult", "Multi-step computation MCQ",
  r"If $u = 3\sin x + 4\cos x$, then the range of $u^2 - 6u$ over all real $x$ is",
  r"$[-9, 55]$",
  [(r"$[-5, 55]$", r"Evaluates $u^2 - 6u$ only at the endpoints $u = \pm 5$, missing the vertex $u = 3$."),
   (r"$[-9, 91]$", r"Uses $u \in [-7, 7]$, adding the coefficients."),
   (r"$[-5, 7]$", r"Treats $u$ as ranging over $[-1, 1]$ like a single sine.")],
  r"First $u \in [-5, 5]$. Then $u^2 - 6u = (u - 3)^2 - 9$. The vertex $u = 3$ lies in $[-5, 5]$, giving the minimum $-9$; the maximum is at $u = -5$: $25 + 30 = 55$. So the range is $[-9, 55]$.",
  r"Checking only the endpoints of the range of $u$.",
  "U14-B-composite-quadratic-range", r"Two layers: amplitude of $u$, then a quadratic with an interior vertex.",
  check=_c49, values=[Interval(-9, 55), Interval(-5, 55), Interval(-9, 91), Interval(-5, 7)], cognitive="Analysis")


def _c50():
    rng = function_range(to_t(4*sin(x)**2 + 3*sin(x) - 1), t, Interval(-1, 1))
    return len([k for k in range(-20, 21) if rng.contains(k)])
q("U14-B-050", TOP_M, "Integer values of a quadratic in sin x", "Difficult", "Inverse/parameter MCQ",
  r"The number of integer values of $\lambda$ for which the equation $4\sin^2 x + 3\sin x - 1 = \lambda$ has at least one real solution $x$ is",
  r"$8$",
  [(r"$7$", r"Uses only the endpoint values $0$ and $6$ at $\sin x = \mp 1$, missing the vertex minimum $-\frac{25}{16}$."),
   (r"$9$", r"Finds the minimum $-\frac{25}{16}$ but rounds it down to include $\lambda = -2$."),
   (r"$6$", r"Counts only the positive integers $1, \ldots, 6$.")],
  r"With $t = \sin x \in [-1, 1]$, $4t^2 + 3t - 1$ has vertex $t = -\frac{3}{8}$ inside $[-1,1]$, minimum $4 \cdot \frac{9}{64} - \frac{9}{8} - 1 = -\frac{25}{16}$, and maximum $f(1) = 6$ (since $f(-1) = 0$). So $\lambda \in \left[-\frac{25}{16}, 6\right]$, containing the integers $-1, 0, 1, \ldots, 6$: $8$ values.",
  r"Ignoring an interior vertex of a quadratic in $\sin x$.",
  "U14-B-quad-sin-integer-count", r"Vertex inside $[-1,1]$, fractional minimum, careful integer count.",
  check=_c50, values=[8, 7, 9, 6], cognitive="Analysis",
  numerical=dict(question=r"The number of integer values of $\lambda$ for which the equation $4\sin^2 x + 3\sin x - 1 = \lambda$ has at least one real solution $x$ is", answer=8))

q("U14-B-051", TOP_F, "Period of a sum of composite functions", "Difficult", "Multi-step computation MCQ",
  r"The fundamental period of $f(x) = \cos(\cos x) + \cos(\sin x)$ is",
  r"$\frac{\pi}{2}$",
  [(r"$\pi$", r"Notes that each of $\cos(\cos x)$ and $\cos(\sin x)$ has period $\pi$ and stops there."),
   (r"$2\pi$", r"Takes the period $2\pi$ of the inner functions $\cos x$ and $\sin x$."),
   (r"$\frac{\pi}{4}$", r"Sees the quarter-shift swap and assumes the period halves again, as it does for $\sin^4 x + \cos^4 x$, without testing whether $f\left(\frac{\pi}{4}\right) = f(0)$.")],
  r"Each term has period $\pi$ (cosine is even). Moreover $f\left(x + \frac{\pi}{2}\right) = \cos(-\sin x) + \cos(\cos x) = f(x)$, so $\frac{\pi}{2}$ is a period. No smaller period works: the maximum value $f(0) = 1 + \cos 1$ is attained in $\left[0, \frac{\pi}{2}\right)$ only at $x = 0$ (for example $f\left(\frac{\pi}{4}\right) = 2\cos\frac{1}{\sqrt{2}} < 1 + \cos 1$), so a period $T < \frac{\pi}{2}$ would force $f(T) = f(0)$, which is impossible.",
  r"Stopping at the period of each term without testing the swap $x \to x + \frac{\pi}{2}$.",
  "U14-B-period-composite", r"Needs the observation that a quarter shift swaps the two terms.",
  check=lambda: fund_period(cos(cos(x)) + cos(sin(x))),
  values=[pi/2, pi, 2*pi, pi/4], cognitive="Analysis")


def _c52():
    g = t**2 + a_*t + 2
    cands = set()
    for e in (g.subs(t, -a_/2), g.subs(t, 1), g.subs(t, -1)):
        for s in solve(Eq(e, 0), a_):
            if s.is_real:
                cands.add(s)
    good = [c for c in cands if function_range(g.subs(a_, c), t, Interval(-1, 1)).inf == 0]
    return FiniteSet(*good)
q("U14-B-052", TOP_M, "Parameter from the minimum of a quadratic in sin x", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real values of $a$ for which the minimum value of $\sin^2 x + a\sin x + 2$ over $x \in \mathbb{R}$ is $0$ is",
  r"$\{-3, 3\}$",
  [(r"$\{-2\sqrt{2}, 2\sqrt{2}\}$", r"Sets the vertex value $2 - \frac{a^2}{4} = 0$ without checking that the vertex $\sin x = -\frac{a}{2}$ lies in $[-1, 1]$."),
   (r"$\{3\}$", r"Handles only the case where the minimum is at $\sin x = -1$ and misses the symmetric case."),
   (r"$\{-3, -2\sqrt{2}, 2\sqrt{2}, 3\}$", r"Accepts all candidate values from the vertex and endpoint equations without checking which case applies.")],
  r"Let $t = \sin x \in [-1, 1]$, $g(t) = t^2 + at + 2$. If $|a| \le 2$ the vertex is inside and the minimum $2 - \frac{a^2}{4} \ge 1 > 0$. If $a > 2$, $g$ increases on $[-1,1]$ and the minimum $g(-1) = 3 - a = 0$ gives $a = 3$. If $a < -2$, the minimum $g(1) = 3 + a = 0$ gives $a = -3$. So $a \in \{-3, 3\}$.",
  r"Using the vertex formula when the vertex lies outside $[-1, 1]$.",
  "U14-B-quad-sin-param-min", r"Casework on the vertex position; the tempting vertex answer is invalid.",
  check=_c52,
  values=[FiniteSet(-3, 3), FiniteSet(-2*sqrt(2), 2*sqrt(2)), FiniteSet(3), FiniteSet(-3, -2*sqrt(2), 2*sqrt(2), 3)],
  cognitive="Analysis")

q("U14-B-053", TOP_M, "Maximum of a product via sin x + cos x substitution", "Difficult", "Multi-step computation MCQ",
  r"The maximum value of $(\sin x + 2)(\cos x + 2)$, $x \in \mathbb{R}$, is",
  r"$\frac{9}{2} + 2\sqrt{2}$",
  [(r"$9$", r"Takes $\sin x = \cos x = 1$ together, giving $3 \times 3$."),
   (r"$\frac{11}{2} + 2\sqrt{2}$", r"Uses $\sin x\cos x = \frac{v^2 + 1}{2}$ instead of $\frac{v^2 - 1}{2}$ with $v = \sin x + \cos x$."),
   (r"$\frac{19}{2}$", r"Uses the correct reduction but takes $v = \sin x + \cos x$ up to $2$.")],
  r"Let $v = \sin x + \cos x \in [-\sqrt{2}, \sqrt{2}]$, so $\sin x\cos x = \frac{v^2 - 1}{2}$. The product is $\sin x\cos x + 2v + 4 = \frac{v^2}{2} + 2v + \frac{7}{2}$, increasing on $[-\sqrt{2}, \sqrt{2}]$ (vertex at $v = -2$). The maximum at $v = \sqrt{2}$ is $1 + 2\sqrt{2} + \frac{7}{2} = \frac{9}{2} + 2\sqrt{2}$.",
  r"Letting $\sin x$ and $\cos x$ both equal $1$, or the wrong range of $\sin x + \cos x$.",
  "U14-B-product-substitution", r"Substitution $v = \sin x + \cos x$, then a quadratic on a restricted interval.",
  check=lambda: ext((sin(x) + 2)*(cos(x) + 2), FULL)[1],
  values=[Rational(9, 2) + 2*sqrt(2), 9, Rational(11, 2) + 2*sqrt(2), Rational(19, 2)], cognitive="Analysis")


def _c54():
    lhs = 2*cos(x/2)**2*sin(x)**2
    rhs = x**2 + 1/x**2
    # count on (0, pi/2]; also confirm lhs - rhs < 0 throughout by the bounds argument
    return count_roots(lhs - rhs, Rational(1, 10**4), pi/2)
q("U14-B-054", TOP_M, "Counting solutions by comparing ranges", "Difficult", "Multi-step computation MCQ",
  r"The number of solutions of $2\cos^2\left(\frac{x}{2}\right)\sin^2 x = x^2 + \frac{1}{x^2}$ in the interval $\left(0, \frac{\pi}{2}\right]$ is",
  r"$0$",
  [(r"$1$", r"Sees that both sides can equal $2$ at $x = 1$ without checking that the left side is less than $2$ there."),
   (r"$2$", r"Assumes the curves cross twice as the right side dips to its minimum $2$."),
   (r"$3$", r"Sketches the left side as oscillating and counts several crossings.")],
  r"The left side is at most $2 \cdot 1 \cdot 1 = 2$, and the right side is at least $2$ (AM-GM), with equality only at $x = 1$. A solution would need both sides equal to $2$, hence $x = 1$; but at $x = 1$ the left side is $2\cos^2\frac{1}{2}\sin^2 1 < 2$. So there are no solutions.",
  r"Matching upper and lower bounds without checking they occur at the same $x$.",
  "U14-B-bound-comparison-count", r"Requires the bound argument and a check of the equality point.",
  check=_c54, values=[0, 1, 2, 3], cognitive="Analysis")


def _c55():
    res = set()
    for v in (Rational(3, 10), Rational(6, 10), Rational(3, 4)):
        p = sin(v)**sin(v); qq = sin(v)**cos(v); r = cos(v)**sin(v)
        vals = [N(p, 30), N(qq, 30), N(r, 30)]
        order = sorted(range(3), key=lambda i: vals[i])
        ranks = [0, 0, 0]
        for pos, i in enumerate(order):
            ranks[i] = pos + 1
        res.add(tuple(ranks))
    assert len(res) == 1
    return tuple(Integer(k) for k in res.pop())
q("U14-B-055", TOP_S, "Comparing powers with trigonometric bases", "Difficult", "Conceptual/application MCQ",
  r"For $0 < x < \frac{\pi}{4}$, let $p = (\sin x)^{\sin x}$, $q = (\sin x)^{\cos x}$ and $r = (\cos x)^{\sin x}$. Then",
  r"$q < p < r$",
  [(r"$p < q < r$", r"Assumes a larger exponent gives a larger power, which holds only for bases greater than $1$."),
   (r"$r < p < q$", r"Reverses both comparisons: larger exponent bigger and larger base smaller."),
   (r"$q < r < p$", r"Gets $q < p$ but thinks a smaller base gives a larger power for the same exponent, so $r < p$; then, since $q$ has both the smaller base and the larger exponent, places $q$ lowest.")],
  r"For $0 < x < \frac{\pi}{4}$, $0 < \sin x < \cos x < 1$. With base $\sin x < 1$, a larger exponent gives a smaller power, so $(\sin x)^{\cos x} < (\sin x)^{\sin x}$, i.e. $q < p$. With the same positive exponent $\sin x$, the larger base gives the larger power, so $(\sin x)^{\sin x} < (\cos x)^{\sin x}$, i.e. $p < r$. Hence $q < p < r$.",
  r"Treating powers of a base less than $1$ as increasing in the exponent.",
  "U14-B-compare-power", r"Two monotonicity facts about powers combined with $\sin x < \cos x$ in the interval.",
  check=_c55,
  values=[(Integer(2), Integer(1), Integer(3)), (Integer(1), Integer(2), Integer(3)), (Integer(2), Integer(3), Integer(1)), (Integer(3), Integer(1), Integer(2))],
  cognitive="Analysis")
