import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x', real=True)
t = Symbol('t', real=True)
k = Symbol('k', real=True)
m = Symbol('m', positive=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TOP = "Inverse trigonometric functions"


def Q(*a, **kw):
    kw.setdefault("source_class", "XII")
    return q(*a, **kw)


def acotp(y):
    """Principal cot^{-1} with range (0, pi)."""
    return pi/2 - atan(y)


def close(a, b, tol=1e-20):
    return bool(abs(N(a - b, 40)) < tol)


def holds_at(lhs, rhs, var, pts):
    return bool(all(close(lhs.subs(var, p), rhs.subs(var, p)) for p in pts))


def real_roots_filtered(poly_expr, original, var):
    """Exact real roots of an algebraic consequence, kept only if they satisfy the original equation."""
    out = []
    for s in solve(poly_expr, var):
        if not s.is_real:
            continue
        try:
            val = N(original.subs(var, s), 40)
        except Exception:
            continue
        if val.is_real and abs(val) < 1e-25:
            out.append(nsimplify(s))
    return FiniteSet(*out)


# ================================================================ EASY
# ---------------------------------------------------------------- 001
Q("U14-C-001", TOP, "Principal values", "Easy", "Single-step computation MCQ",
  r"Using principal values, $\tan^{-1}(-\sqrt{3}) + \cos^{-1}\left(-\frac{1}{2}\right)$ equals",
  r"$\frac{\pi}{3}$",
  [(r"$-\frac{2\pi}{3}$", r"Treats $\cos^{-1}$ as odd, taking $\cos^{-1}\left(-\frac{1}{2}\right) = -\frac{\pi}{3}$, so the sum is $-\frac{\pi}{3} - \frac{\pi}{3}$."),
   (r"$\frac{4\pi}{3}$", r"Uses the range $(0, \pi)$ for $\tan^{-1}$, taking $\tan^{-1}(-\sqrt{3}) = \frac{2\pi}{3}$, so the sum is $\frac{2\pi}{3} + \frac{2\pi}{3}$."),
   (r"$0$", r"Drops the sign inside $\cos^{-1}$, taking $\cos^{-1}\left(-\frac{1}{2}\right) = \frac{\pi}{3}$, so the sum is $-\frac{\pi}{3} + \frac{\pi}{3}$.")],
  r"The principal value of $\tan^{-1}(-\sqrt{3})$ lies in $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$, so it is $-\frac{\pi}{3}$. The principal value of $\cos^{-1}\left(-\frac{1}{2}\right)$ lies in $[0, \pi]$, so it is $\pi - \frac{\pi}{3} = \frac{2\pi}{3}$. The sum is $-\frac{\pi}{3} + \frac{2\pi}{3} = \frac{\pi}{3}$.",
  r"Using $\cos^{-1}(-x) = -\cos^{-1}x$ instead of $\cos^{-1}(-x) = \pi - \cos^{-1}x$.",
  "U14-C-principal-values", "Two principal values with sign handling; one step each.",
  check=lambda: atan(-sqrt(3)) + acos(-Rational(1, 2)),
  values=[pi/3, -2*pi/3, 4*pi/3, 0], cognitive="Understanding")

# ---------------------------------------------------------------- 002
Q("U14-C-002", TOP, "Inverse of a trigonometric function at a given angle", "Easy", "Single-step computation MCQ",
  r"The value of $\sin^{-1}\left(\sin\frac{2\pi}{3}\right) + \cos^{-1}\left(\cos\frac{7\pi}{6}\right)$ is",
  r"$\frac{7\pi}{6}$",
  [(r"$\frac{5\pi}{6}$", r"Cancels the first composition to $\frac{2\pi}{3}$ without checking the principal range, and reduces the second as $\frac{7\pi}{6} - \pi = \frac{\pi}{6}$, adding $\frac{2\pi}{3} + \frac{\pi}{6}$."),
   (r"$\frac{3\pi}{2}$", r"Correctly gets $\frac{\pi}{3}$ for the first term but cancels the second, adding $\frac{\pi}{3} + \frac{7\pi}{6}$."),
   (r"$\frac{\pi}{2}$", r"Gets $\frac{\pi}{3}$ for the first term but reduces the second as $\frac{7\pi}{6} - \pi = \frac{\pi}{6}$, which has the wrong cosine sign, giving $\frac{\pi}{3} + \frac{\pi}{6}$.")],
  r"Since $\frac{2\pi}{3} \notin \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$, use $\sin\frac{2\pi}{3} = \sin\frac{\pi}{3}$, so the first term is $\frac{\pi}{3}$. Since $\frac{7\pi}{6} \notin [0, \pi]$, use $\cos\frac{7\pi}{6} = \cos\left(2\pi - \frac{7\pi}{6}\right) = \cos\frac{5\pi}{6}$, so the second term is $\frac{5\pi}{6}$. The sum is $\frac{\pi}{3} + \frac{5\pi}{6} = \frac{7\pi}{6}$.",
  r"Assuming $\sin^{-1}(\sin\theta) = \theta$ and $\cos^{-1}(\cos\theta) = \theta$ for every $\theta$.",
  "U14-C-inverse-of-function-exact", "Two compositions, each reduced to the principal range in one step.",
  check=lambda: asin(sin(2*pi/3)) + acos(cos(7*pi/6)),
  values=[7*pi/6, 5*pi/6, 3*pi/2, pi/2], cognitive="Understanding")

# ---------------------------------------------------------------- 003
def _c003():
    d1 = solveset(Abs(3*x - 2) <= 1, x, S.Reals)
    d2 = solveset(Abs(2*x - 1) <= 1, x, S.Reals)
    return Intersection(d1, d2)
Q("U14-C-003", TOP, "Domain", "Easy", "Single-step computation MCQ",
  r"The domain of $f(x) = \cos^{-1}(3x - 2) + \sin^{-1}(2x - 1)$ is",
  r"$\left[\frac{1}{3}, 1\right]$",
  [(r"$[0, 1]$", r"Takes the union of the two domains $\left[\frac{1}{3}, 1\right]$ and $[0, 1]$ rather than their intersection."),
   (r"$[1, 3]$", r"From $-1 \le 3x - 2 \le 1$ adds $2$ to get $1 \le 3x \le 3$ but does not divide by $3$."),
   (r"$\left[\frac{2}{3}, 1\right]$", r"Uses $0 \le 3x - 2 \le 1$, taking the domain of $\cos^{-1}$ as $[0, 1]$.")],
  r"$\cos^{-1}(3x-2)$ needs $-1 \le 3x - 2 \le 1$, that is $\frac{1}{3} \le x \le 1$. $\sin^{-1}(2x-1)$ needs $-1 \le 2x - 1 \le 1$, that is $0 \le x \le 1$. Both must hold, so the domain is $\left[\frac{1}{3}, 1\right]$.",
  r"Combining domains of a sum by union instead of intersection.",
  "U14-C-domain-intersection", "Two linear double inequalities and an intersection.",
  check=_c003,
  values=[Interval(Rational(1, 3), 1), Interval(0, 1), Interval(1, 3), Interval(Rational(2, 3), 1)], cognitive="Application")

# ---------------------------------------------------------------- 004
def _c004():
    f = asin(x) + 2*acos(x)
    assert simplify(diff(f, x) + 1/sqrt(1 - x**2)) == 0  # strictly decreasing on [-1, 1]
    return Interval(f.subs(x, 1), f.subs(x, -1))
Q("U14-C-004", TOP, "Range", "Easy", "Single-step computation MCQ",
  r"The range of $f(x) = \sin^{-1}x + 2\cos^{-1}x$ is",
  r"$\left[\frac{\pi}{2}, \frac{3\pi}{2}\right]$",
  [(r"$\left[-\frac{\pi}{2}, \frac{5\pi}{2}\right]$", r"Adds the ranges $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ and $[0, 2\pi]$ separately, ignoring that both terms depend on the same $x$."),
   (r"$[0, \pi]$", r"Rewrites $f$ as $\frac{\pi}{2} + \sin^{-1}x$ (replacing the leftover $\cos^{-1}x$ by $\sin^{-1}x$), whose range is $[0, \pi]$."),
   (r"$\left[\frac{\pi}{2}, \pi\right]$", r"Correctly writes $f = \frac{\pi}{2} + \cos^{-1}x$ but takes the range of $\cos^{-1}x$ as $\left[0, \frac{\pi}{2}\right]$.")],
  r"Write $f(x) = (\sin^{-1}x + \cos^{-1}x) + \cos^{-1}x = \frac{\pi}{2} + \cos^{-1}x$. As $x$ runs over $[-1, 1]$, $\cos^{-1}x$ takes every value in $[0, \pi]$. Hence the range is $\left[\frac{\pi}{2}, \frac{3\pi}{2}\right]$.",
  r"Adding the ranges of dependent terms independently.",
  "U14-C-range-linear-combo", r"One identity reduces the function to a shifted $\cos^{-1}x$.",
  check=_c004,
  values=[Interval(pi/2, 3*pi/2), Interval(-pi/2, 5*pi/2), Interval(0, pi), Interval(pi/2, pi)], cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    s = nsolve(acos(x) - asin(x) - pi/6, x, 0.3)
    return nsimplify(s, [sqrt(3)])
Q("U14-C-005", TOP, "Equation using sin^-1 x + cos^-1 x = pi/2", "Easy", "Single-step computation MCQ",
  r"If $\cos^{-1}x - \sin^{-1}x = \frac{\pi}{6}$, then $x$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{\sqrt{3}}{2}$", r"Reaches $2\sin^{-1}x = \frac{\pi}{3}$ but forgets to halve, taking $\sin^{-1}x = \frac{\pi}{3}$."),
   (r"$-\frac{1}{2}$", r"Sign slip: writes $\cos^{-1}x - \sin^{-1}x = \frac{\pi}{2} + 2\sin^{-1}x$, getting $\sin^{-1}x = -\frac{\pi}{6}$."),
   (r"$\frac{\sqrt{6}+\sqrt{2}}{4}$", r"Uses $\sin^{-1}x + \cos^{-1}x = \pi$, so $\pi - 2\sin^{-1}x = \frac{\pi}{6}$ and $\sin^{-1}x = \frac{5\pi}{12}$, $x = \sin 75^\circ$.")],
  r"Put $\cos^{-1}x = \frac{\pi}{2} - \sin^{-1}x$: then $\frac{\pi}{2} - 2\sin^{-1}x = \frac{\pi}{6}$, so $\sin^{-1}x = \frac{\pi}{6}$ and $x = \frac{1}{2}$. Check: $\cos^{-1}\frac{1}{2} - \sin^{-1}\frac{1}{2} = \frac{\pi}{3} - \frac{\pi}{6} = \frac{\pi}{6}$.",
  r"Using the wrong constant in $\sin^{-1}x + \cos^{-1}x = \frac{\pi}{2}$.",
  "U14-C-complement-equation", "One identity and one linear step.",
  check=_c005,
  values=[Rational(1, 2), sqrt(3)/2, -Rational(1, 2), (sqrt(6) + sqrt(2))/4], cognitive="Application")

# ---------------------------------------------------------------- 006
Q("U14-C-006", TOP, "Trigonometric ratio of an inverse function", "Easy", "Single-step computation MCQ",
  r"The value of $\tan\left(\cos^{-1}\left(-\frac{3}{5}\right)\right)$ is",
  r"$-\frac{4}{3}$",
  [(r"$\frac{4}{3}$", r"Takes the angle as acute, ignoring that $\cos^{-1}$ of a negative number lies in $\left(\frac{\pi}{2}, \pi\right)$."),
   (r"$-\frac{3}{4}$", r"Gets the quadrant right but computes $\frac{\cos\theta}{\sin\theta}$, the cotangent."),
   (r"$\frac{3}{4}$", r"Computes the cotangent and also treats the angle as acute.")],
  r"Let $\theta = \cos^{-1}\left(-\frac{3}{5}\right)$; then $\theta \in \left(\frac{\pi}{2}, \pi\right)$ and $\cos\theta = -\frac{3}{5}$. So $\sin\theta = \frac{4}{5}$ (positive in the second quadrant) and $\tan\theta = \frac{4/5}{-3/5} = -\frac{4}{3}$.",
  r"Forgetting that $\cos^{-1}$ of a negative number is an obtuse angle.",
  "U14-C-trig-of-inverse", "One triangle and one quadrant decision.",
  check=lambda: tan(acos(-Rational(3, 5))),
  values=[-Rational(4, 3), Rational(4, 3), -Rational(3, 4), Rational(3, 4)], cognitive="Application")

# ---------------------------------------------------------------- 007
Q("U14-C-007", TOP, "Trigonometric ratio of an inverse function", "Easy", "Single-step computation MCQ",
  r"The value of $\sin\left(2\tan^{-1}\frac{1}{2}\right)$ is",
  r"$\frac{4}{5}$",
  [(r"$\frac{2}{\sqrt{5}}$", r"Computes $2\sin\theta$ with $\sin\theta = \frac{1}{\sqrt{5}}$ instead of $\sin 2\theta$."),
   (r"$\frac{3}{5}$", r"Uses $\frac{1 - \tan^2\theta}{1 + \tan^2\theta}$, which is $\cos 2\theta$."),
   (r"$\frac{4}{3}$", r"Uses $\frac{2\tan\theta}{1 - \tan^2\theta}$, which is $\tan 2\theta$.")],
  r"With $\theta = \tan^{-1}\frac{1}{2}$, $\sin 2\theta = \frac{2\tan\theta}{1 + \tan^2\theta} = \frac{1}{1 + \frac{1}{4}} = \frac{4}{5}$.",
  r"Mixing up the $\sin 2\theta$, $\cos 2\theta$ and $\tan 2\theta$ formulas in terms of $\tan\theta$.",
  "U14-C-trig-of-inverse", "One double-angle formula.",
  check=lambda: sin(2*atan(Rational(1, 2))),
  values=[Rational(4, 5), 2/sqrt(5), Rational(3, 5), Rational(4, 3)], cognitive="Application")

# ---------------------------------------------------------------- 008
Q("U14-C-008", TOP, "Principal values", "Easy", "Direct concept MCQ",
  r"The principal value of $\cot^{-1}(-\sqrt{3})$, where the principal range of $\cot^{-1}$ is $(0, \pi)$, is",
  r"$\frac{5\pi}{6}$",
  [(r"$\frac{\pi}{3}$", r"Ignores the negative sign and also confuses $\cot^{-1}\sqrt{3}$ with $\tan^{-1}\sqrt{3} = \frac{\pi}{3}$."),
   (r"$\frac{\pi}{6}$", r"Ignores the negative sign and returns $\cot^{-1}\sqrt{3}$."),
   (r"$\frac{2\pi}{3}$", r"Uses the $\tan$ value: $\tan\frac{\pi}{3} = \sqrt{3}$, then takes $\pi - \frac{\pi}{3}$, mixing up $\tan$ and $\cot$.")],
  r"In $(0, \pi)$, $\cot\theta = -\sqrt{3}$ needs $\theta$ in the second quadrant with reference angle $\frac{\pi}{6}$. So $\cot^{-1}(-\sqrt{3}) = \pi - \cot^{-1}\sqrt{3} = \pi - \frac{\pi}{6} = \frac{5\pi}{6}$.",
  r"Dropping the negative sign or mixing up $\cot^{-1}$ and $\tan^{-1}$ values instead of using $\cot^{-1}(-x) = \pi - \cot^{-1}x$.",
  "U14-C-principal-values", "Single principal-value recall with the negative-argument rule.",
  check=lambda: acotp(-sqrt(3)),
  values=[5*pi/6, pi/3, pi/6, 2*pi/3], cognitive="Recall")

# ---------------------------------------------------------------- 009
def _c009():
    s1 = close(asin(sin(Integer(3))), 3)
    s2 = close(acos(cos(Integer(3))), 3)
    return (s1, s2)
Q("U14-C-009", TOP, "Inverse of a trigonometric function at a radian value", "Easy", "Statement-based MCQ",
  r"All angles are in radians. Statement I: $\sin^{-1}(\sin 3) = 3$. Statement II: $\cos^{-1}(\cos 3) = 3$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Assumes $\sin^{-1}(\sin\theta) = \theta$ for every $\theta$; but $3 > \frac{\pi}{2}$, so $\sin^{-1}(\sin 3) = \pi - 3$."),
   (ST_FF, r"Rejects both, not noticing that $3 < \pi \approx 3.14$ lies in $[0, \pi]$, the principal range of $\cos^{-1}$."),
   (ST_TF, r"Swaps the two principal ranges, thinking $3$ lies in the range of $\sin^{-1}$ but not of $\cos^{-1}$.")],
  r"Since $\pi \approx 3.14$, the number $3$ lies in $[0, \pi]$, so $\cos^{-1}(\cos 3) = 3$ and Statement II is true. But $3 \notin \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$; as $\sin 3 = \sin(\pi - 3)$ with $\pi - 3 \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$, we get $\sin^{-1}(\sin 3) = \pi - 3 \ne 3$. So Statement I is false.",
  r"Cancelling $\sin^{-1}$ with $\sin$ outside the principal range.",
  "U14-C-statement-radian-composition", r"Two range checks with $\pi \approx 3.14$.",
  check=_c009,
  values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Understanding")

# ---------------------------------------------------------------- 010
Q("U14-C-010", TOP, "Using sin^-1 x + cos^-1 x = pi/2", "Easy", "Single-step computation MCQ",
  r"The value of $\cos\left(\sin^{-1}\frac{3}{5} + \cos^{-1}\frac{3}{5}\right)$ is",
  r"$0$",
  [(r"$-1$", r"Uses $\sin^{-1}x + \cos^{-1}x = \pi$, so evaluates $\cos\pi$."),
   (r"$\frac{7}{25}$", r"Treats both angles as the same $\theta = \sin^{-1}\frac{3}{5}$ and computes $\cos 2\theta = 1 - 2\cdot\frac{9}{25}$."),
   (r"$\frac{24}{25}$", r"Expands with the wrong sign: $\cos A\cos B + \sin A\sin B = \frac{4}{5}\cdot\frac{3}{5} + \frac{3}{5}\cdot\frac{4}{5}$.")],
  r"For $x \in [-1, 1]$, $\sin^{-1}x + \cos^{-1}x = \frac{\pi}{2}$. With $x = \frac{3}{5}$ the bracket is $\frac{\pi}{2}$, and $\cos\frac{\pi}{2} = 0$.",
  r"Forgetting that $\sin^{-1}x + \cos^{-1}x = \frac{\pi}{2}$ makes the expansion unnecessary.",
  "U14-C-complement-identity", "Recognising one standard identity.",
  check=lambda: cos(asin(Rational(3, 5)) + acos(Rational(3, 5))),
  values=[0, -1, Rational(7, 25), Rational(24, 25)],
  numerical=dict(question=r"The value of $\cos\left(\sin^{-1}\frac{3}{5} + \cos^{-1}\frac{3}{5}\right)$ is", answer=0),
  cognitive="Application")

# ---------------------------------------------------------------- 011
Q("U14-C-011", TOP, "tan^-1 x + tan^-1 y", "Easy", "Single-step computation MCQ",
  r"The value of $\tan^{-1}\frac{1}{2} + \tan^{-1}\frac{1}{3}$ is",
  r"$\frac{\pi}{4}$",
  [(r"$\frac{3\pi}{4}$", r"Adds $\pi$ to $\tan^{-1}1$ as if $xy > 1$, although here $xy = \frac{1}{6} < 1$."),
   (r"$\tan^{-1}\frac{5}{7}$", r"Uses $1 + xy$ in the denominator: $\frac{5/6}{7/6} = \frac{5}{7}$."),
   (r"$\tan^{-1}\frac{5}{6}$", r"Adds the arguments: $\frac{1}{2} + \frac{1}{3} = \frac{5}{6}$.")],
  r"Here $x, y > 0$ and $xy = \frac{1}{6} < 1$, so $\tan^{-1}x + \tan^{-1}y = \tan^{-1}\frac{x + y}{1 - xy} = \tan^{-1}\frac{5/6}{5/6} = \tan^{-1}1 = \frac{\pi}{4}$.",
  r"Using $1 + xy$ instead of $1 - xy$ in the addition formula.",
  "U14-C-tan-sum-basic", "One application of the addition formula.",
  check=lambda: atan(Rational(1, 2)) + atan(Rational(1, 3)),
  values=[pi/4, 3*pi/4, atan(Rational(5, 7)), atan(Rational(5, 6))], cognitive="Application")

# ---------------------------------------------------------------- 012
def _c012():
    d1 = solveset(Abs(x/2) >= 1, x, S.Reals)
    d2 = solveset(9 - x**2 >= 0, x, S.Reals)
    return Intersection(d1, d2)
Q("U14-C-012", TOP, "Domain", "Easy", "Single-step computation MCQ",
  r"The domain of $f(x) = \sec^{-1}\frac{x}{2} + \sqrt{9 - x^2}$ is",
  r"$[-3, -2] \cup [2, 3]$",
  [(r"$[-2, 2]$", r"Uses the condition $\left|\frac{x}{2}\right| \le 1$, which is the domain condition of $\sin^{-1}$ or $\cos^{-1}$, not $\sec^{-1}$."),
   (r"$[-3, -2) \cup (2, 3]$", r"Excludes $x = \pm 2$, thinking $\sec^{-1}(\pm 1)$ is undefined; in fact $\sec^{-1}1 = 0$ and $\sec^{-1}(-1) = \pi$."),
   (r"$\left[-3, -\frac{1}{2}\right] \cup \left[\frac{1}{2}, 3\right]$", r"Inverts the scaling, solving $|2x| \ge 1$ instead of $\left|\frac{x}{2}\right| \ge 1$.")],
  r"$\sec^{-1}u$ is defined for $|u| \ge 1$, so $|x| \ge 2$. The root needs $9 - x^2 \ge 0$, so $-3 \le x \le 3$. Intersecting gives $[-3, -2] \cup [2, 3]$.",
  r"Using $|u| \le 1$ as the domain of $\sec^{-1}u$.",
  "U14-C-domain-sec", "Two conditions and an intersection.",
  check=_c012,
  values=[Union(Interval(-3, -2), Interval(2, 3)), Interval(-2, 2),
          Union(Interval.Ropen(-3, -2), Interval.Lopen(2, 3)),
          Union(Interval(-3, -Rational(1, 2)), Interval(Rational(1, 2), 3))], cognitive="Application")

# ---------------------------------------------------------------- 013
def _c013():
    s1 = (limit(atan(x), x, oo) == pi/2) and (limit(atan(x), x, -oo) == -pi/2)
    s2 = simplify(acotp(-1) + acotp(1)) == 0
    return (bool(s1), bool(s2))
Q("U14-C-013", TOP, "Principal ranges", "Easy", "Statement-based MCQ",
  r"Take the principal range of $\cot^{-1}$ as $(0, \pi)$. Statement I: The range of $\tan^{-1}x$, $x \in \mathbb{R}$, is $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$. Statement II: $\cot^{-1}(-x) = -\cot^{-1}x$ for every real $x$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II by analogy with $\tan^{-1}(-x) = -\tan^{-1}x$; but $-\cot^{-1}x$ is negative, outside $(0, \pi)$."),
   (ST_FF, r"Rejects Statement I by thinking the range is the closed interval $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$; the endpoints are never attained."),
   (ST_FT, r"Both wrong judgements together: closed-interval range for $\tan^{-1}$ and odd symmetry for $\cot^{-1}$.")],
  r"$\tan^{-1}x$ takes every value strictly between $-\frac{\pi}{2}$ and $\frac{\pi}{2}$ and never the endpoints, so Statement I is true. For $\cot^{-1}$ with range $(0, \pi)$, $\cot^{-1}(-x) = \pi - \cot^{-1}x$; for example $\cot^{-1}(-1) = \frac{3\pi}{4} \ne -\frac{\pi}{4}$. So Statement II is false.",
  r"Treating $\cot^{-1}$ as an odd function.",
  "U14-C-statement-ranges", "Recall of a range and of the negative-argument rule.",
  check=_c013,
  values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Recall")

# ---------------------------------------------------------------- 014
def _c014():
    xs = solve(asin(x) - pi/2, x)
    ys = solve(acos(x) - pi, x)
    assert len(xs) == 1 and len(ys) == 1
    return xs[0] - 2*ys[0]
Q("U14-C-014", TOP, "Extreme values of inverse functions", "Easy", "Inverse/parameter MCQ",
  r"If $x, y \in [-1, 1]$ and $\sin^{-1}x + \cos^{-1}y = \frac{3\pi}{2}$, then $x - 2y$ equals",
  r"$3$",
  [(r"$-1$", r"Takes $\cos^{-1}y = \pi$ at $y = 1$, so uses $x = 1, y = 1$."),
   (r"$1$", r"Takes both inverse functions at their largest values at the argument $-1$, so uses $x = -1, y = -1$."),
   (r"$-3$", r"Swaps the two extreme points, using $x = -1$ and $y = 1$.")],
  r"The largest value of $\sin^{-1}x$ is $\frac{\pi}{2}$ and of $\cos^{-1}y$ is $\pi$, so the sum can equal $\frac{3\pi}{2}$ only when both are maximal. Thus $x = 1$ and $y = -1$, giving $x - 2y = 1 + 2 = 3$.",
  r"Placing the maximum of $\cos^{-1}y$ at $y = 1$ instead of $y = -1$.",
  "U14-C-extreme-values", "Recognising that the sum equals the sum of the maxima.",
  check=_c014, values=[3, -1, 1, -3],
  numerical=dict(question=r"If $x, y \in [-1, 1]$ and $\sin^{-1}x + \cos^{-1}y = \frac{3\pi}{2}$, then the value of $x - 2y$ is", answer=3),
  cognitive="Application")

# ---------------------------------------------------------------- 015
def _c015():
    s = nsolve(atan(x) + 2*acotp(x) - 2*pi/3, x, 1.5)
    return nsimplify(s, [sqrt(3)])
Q("U14-C-015", TOP, "Equation using tan^-1 x + cot^-1 x = pi/2", "Easy", "Single-step computation MCQ",
  r"If $\tan^{-1}x + 2\cot^{-1}x = \frac{2\pi}{3}$, where $\cot^{-1}$ has principal range $(0, \pi)$, then $x$ equals",
  r"$\sqrt{3}$",
  [(r"$\frac{1}{\sqrt{3}}$", r"Correctly gets $\cot^{-1}x = \frac{\pi}{6}$ but then writes $x = \tan\frac{\pi}{6}$ instead of $\cot\frac{\pi}{6}$."),
   (r"$2 + \sqrt{3}$", r"Pairs $\tan^{-1}x$ with $\cot^{-1}x$ to get $\frac{\pi}{2}$ but still keeps $2\cot^{-1}x$, so $\cot^{-1}x = \frac{\pi}{12}$ and $x = \cot\frac{\pi}{12}$."),
   (r"$2 - \sqrt{3}$", r"Keeps $2\cot^{-1}x$ after using $\tan^{-1}x + \cot^{-1}x = \frac{\pi}{2}$, so $\frac{\pi}{2} + 2\cot^{-1}x = \frac{2\pi}{3}$ and $\cot^{-1}x = \frac{\pi}{12}$; then writes $x = \tan\frac{\pi}{12} = 2 - \sqrt{3}$ instead of $\cot\frac{\pi}{12}$.")],
  r"Write $\tan^{-1}x + 2\cot^{-1}x = (\tan^{-1}x + \cot^{-1}x) + \cot^{-1}x = \frac{\pi}{2} + \cot^{-1}x$. So $\cot^{-1}x = \frac{2\pi}{3} - \frac{\pi}{2} = \frac{\pi}{6}$ and $x = \cot\frac{\pi}{6} = \sqrt{3}$.",
  r"Double counting $\cot^{-1}x$ after using $\tan^{-1}x + \cot^{-1}x = \frac{\pi}{2}$.",
  "U14-C-complement-equation", "One identity and one inverse step.",
  check=_c015, values=[sqrt(3), 1/sqrt(3), 2 + sqrt(3), 2 - sqrt(3)], cognitive="Application")

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 016
Q("U14-C-016", TOP, "tan^-1 x + tan^-1 y when xy > 1", "Medium", "Single-step computation MCQ",
  r"The value of $\tan^{-1}2 + \tan^{-1}3$ is",
  r"$\frac{3\pi}{4}$",
  [(r"$\frac{\pi}{2}$", r"Overgeneralises $\tan^{-1}x + \tan^{-1}\frac{1}{x} = \frac{\pi}{2}$ to every pair with $xy > 1$."),
   (r"$\frac{\pi}{4}$", r"Writes the denominator as $xy - 1$ instead of $1 - xy$, getting $\tan^{-1}1$."),
   (r"$\frac{2\pi}{3}$", r"Rounds both arguments to $\sqrt{3}$, taking $\tan^{-1}2 = \tan^{-1}3 = \frac{\pi}{3}$, and adds $\frac{\pi}{3} + \frac{\pi}{3}$.")],
  r"Here $x = 2, y = 3 > 0$ and $xy = 6 > 1$, so $\tan^{-1}x + \tan^{-1}y = \pi + \tan^{-1}\frac{x+y}{1-xy}$. This gives $\pi + \tan^{-1}\frac{5}{-5} = \pi - \frac{\pi}{4} = \frac{3\pi}{4}$. (Each term exceeds $\frac{\pi}{4}$, so the sum must exceed $\frac{\pi}{2}$.)",
  r"Ignoring the $xy < 1$ condition of the addition formula.",
  "U14-C-tan-sum-condition", "Formula plus a range correction that is easy to miss.",
  check=lambda: atan(2) + atan(3),
  values=[3*pi/4, pi/2, pi/4, 2*pi/3], cognitive="Analysis")

# ---------------------------------------------------------------- 017
Q("U14-C-017", TOP, "tan^-1 x + tan^-1(1/x) and negative arguments", "Medium", "Multi-step computation MCQ",
  r"With $\cot^{-1}$ taking values in $(0, \pi)$, the value of $\tan^{-1}(-2) + \tan^{-1}\left(-\frac{1}{2}\right) + \cot^{-1}(-1)$ is",
  r"$\frac{\pi}{4}$",
  [(r"$\frac{5\pi}{4}$", r"Uses $\tan^{-1}x + \tan^{-1}\frac{1}{x} = \frac{\pi}{2}$ even for $x < 0$, so adds $\frac{\pi}{2} + \frac{3\pi}{4}$."),
   (r"$-\frac{3\pi}{4}$", r"Takes $\cot^{-1}(-1) = -\frac{\pi}{4}$ (odd symmetry), so adds $-\frac{\pi}{2} - \frac{\pi}{4}$."),
   (r"$-\frac{\pi}{4}$", r"Drops the sign in $\cot^{-1}(-1)$, taking it as $\frac{\pi}{4}$, so adds $-\frac{\pi}{2} + \frac{\pi}{4}$.")],
  r"For $x < 0$, $\tan^{-1}x + \tan^{-1}\frac{1}{x} = -\frac{\pi}{2}$, so the first two terms give $-\frac{\pi}{2}$. Also $\cot^{-1}(-1) = \pi - \cot^{-1}1 = \frac{3\pi}{4}$. The total is $-\frac{\pi}{2} + \frac{3\pi}{4} = \frac{\pi}{4}$.",
  r"Using $\tan^{-1}x + \tan^{-1}\frac{1}{x} = \frac{\pi}{2}$ for negative $x$.",
  "U14-C-tan-reciprocal-pair", "Two sign-sensitive rules combined.",
  check=lambda: atan(-2) + atan(-Rational(1, 2)) + acotp(-1),
  values=[pi/4, 5*pi/4, -3*pi/4, -pi/4], cognitive="Analysis")

# ---------------------------------------------------------------- 018
_P018 = [-1, Rational(1, 3), 1]
def _c018():
    return tuple(atan(cos(p)/(1 + sin(p))) for p in _P018)
Q("U14-C-018", TOP, "Simplification", "Medium", "Multi-step computation MCQ",
  r"For $-\frac{\pi}{2} < x < \frac{\pi}{2}$, the expression $\tan^{-1}\left(\frac{\cos x}{1 + \sin x}\right)$ equals",
  r"$\frac{\pi}{4} - \frac{x}{2}$",
  [(r"$\frac{\pi}{4} + \frac{x}{2}$", r"Writes $\frac{\cos x}{1+\sin x}$ as $\frac{1 + \tan(x/2)}{1 - \tan(x/2)}$ (the reciprocal), which is $\tan\left(\frac{\pi}{4} + \frac{x}{2}\right)$."),
   (r"$\frac{\pi}{2} - x$", r"Uses $\cos x = \sin\left(\frac{\pi}{2} - x\right)$ and then cancels as if the ratio were $\tan\left(\frac{\pi}{2} - x\right)$, never halving."),
   (r"$\frac{\pi}{4} - x$", r"Halves $\frac{\pi}{2}$ but not $x$ when converting $\frac{\pi}{2} - x$ to a half angle.")],
  r"Write $\cos x = \sin\left(\frac{\pi}{2} - x\right)$ and $1 + \sin x = 1 + \cos\left(\frac{\pi}{2} - x\right)$. Then $\frac{\cos x}{1 + \sin x} = \frac{2\sin\theta\cos\theta}{2\cos^2\theta} = \tan\theta$ with $\theta = \frac{\pi}{4} - \frac{x}{2}$. Since $\theta \in \left(0, \frac{\pi}{2}\right)$ for the given $x$, $\tan^{-1}(\tan\theta) = \theta = \frac{\pi}{4} - \frac{x}{2}$.",
  r"Inverting the half-angle ratio, which flips the sign of $\frac{x}{2}$.",
  "U14-C-simplification-half-angle", "Complementary-angle rewrite, half-angle identities and a range check.",
  check=_c018,
  values=[tuple(pi/4 - p/2 for p in _P018), tuple(pi/4 + p/2 for p in _P018),
          tuple(pi/2 - p for p in _P018), tuple(pi/4 - p for p in _P018)], cognitive="Application")

# ---------------------------------------------------------------- 019
_P019 = [-Rational(1, 2), -2, -5]
def _c019():
    return tuple(acos((1 - p**2)/(1 + p**2)) for p in _P019)
Q("U14-C-019", TOP, "Simplification by tangent substitution", "Medium", "Conceptual/application MCQ",
  r"For every real $x < 0$, $\cos^{-1}\left(\frac{1 - x^2}{1 + x^2}\right)$ equals",
  r"$-2\tan^{-1}x$",
  [(r"$2\tan^{-1}x$", r"Applies the formula valid for $x \ge 0$, giving a negative value for an inverse cosine."),
   (r"$\pi + 2\tan^{-1}x$", r"Uses the branch $\pi - 2\theta$ of the inverse sine formula, writing $\pi - 2|\theta|$."),
   (r"$-\tan^{-1}x$", r"Handles the sign correctly but drops the factor $2$ of the double-angle identity, reading $\frac{1 - x^2}{1 + x^2}$ as $\cos\theta$ instead of $\cos 2\theta$ for $x = \tan\theta$, so gets $-\theta$.")],
  r"Put $x = \tan\theta$ with $\theta \in \left(-\frac{\pi}{2}, 0\right)$. Then $\frac{1 - x^2}{1 + x^2} = \cos 2\theta = \cos(-2\theta)$ and $-2\theta \in (0, \pi)$. Hence $\cos^{-1}(\cos(-2\theta)) = -2\theta = -2\tan^{-1}x$, which is positive as it must be.",
  r"Using $\cos^{-1}\frac{1-x^2}{1+x^2} = 2\tan^{-1}x$ without the condition $x \ge 0$.",
  "U14-C-double-angle-branch", "Substitution plus a branch decision on the sign of $x$.",
  check=_c019,
  values=[tuple(-2*atan(p) for p in _P019), tuple(2*atan(p) for p in _P019),
          tuple(pi + 2*atan(p) for p in _P019), tuple(-atan(p) for p in _P019)], cognitive="Analysis")

# ---------------------------------------------------------------- 020
def _c020():
    tv = Integer(0)
    for j in range(1, 21):
        a = Rational(1, j**2 + j + 1)
        tv = (tv + a)/(1 - tv*a)
    return tv
Q("U14-C-020", TOP, "Telescoping sum of tan^-1 terms", "Medium", "Multi-step computation MCQ",
  r"If $S = \sum_{k=1}^{20} \tan^{-1}\left(\frac{1}{k^2 + k + 1}\right)$, then $\tan S$ equals",
  r"$\frac{10}{11}$",
  [(r"$\frac{19}{21}$", r"Telescopes to $\tan^{-1}20 - \tan^{-1}1$, stopping one step early at the upper end."),
   (r"$\frac{21}{23}$", r"Telescopes to $\tan^{-1}22 - \tan^{-1}1$, going one step too far at the upper end."),
   (r"$\frac{19}{43}$", r"Telescopes to $\tan^{-1}21 - \tan^{-1}2$, shifting the lower end by one.")],
  r"Since $\frac{1}{k^2 + k + 1} = \frac{(k+1) - k}{1 + k(k+1)}$, each term is $\tan^{-1}(k+1) - \tan^{-1}k$. The sum telescopes to $S = \tan^{-1}21 - \tan^{-1}1$. Hence $\tan S = \frac{21 - 1}{1 + 21} = \frac{20}{22} = \frac{10}{11}$.",
  r"Off-by-one errors at the ends of a telescoping sum.",
  "U14-C-telescoping-finite", "Recognise the difference form, telescope, then apply the subtraction formula.",
  check=_c020, values=[Rational(10, 11), Rational(19, 21), Rational(21, 23), Rational(19, 43)],
  numerical=dict(question=r"If $S = \sum_{k=1}^{20} \tan^{-1}\left(\frac{1}{k^2 + k + 1}\right)$, then the value of $11\tan S$ is", answer=10),
  cognitive="Application")

# ---------------------------------------------------------------- 021
def _c021():
    r_ = Symbol('r', positive=True)
    nn = Symbol('nn', positive=True)
    lhs = ((2*r_ + 1) - (2*r_ - 1))/(1 + (2*r_ + 1)*(2*r_ - 1))
    assert simplify(lhs - 1/(2*r_**2)) == 0
    return limit(atan(2*nn + 1), nn, oo) - atan(1)
Q("U14-C-021", TOP, "Infinite telescoping sum", "Medium", "Multi-step computation MCQ",
  r"The value of $\sum_{r=1}^{\infty} \tan^{-1}\left(\frac{1}{2r^2}\right)$ is",
  r"$\frac{\pi}{4}$",
  [(r"$\frac{\pi}{2}$", r"Keeps only the limit $\tan^{-1}(2n+1) \to \frac{\pi}{2}$ and forgets to subtract $\tan^{-1}1$."),
   (r"$\frac{\pi}{8}$", r"Pulls the $\frac{1}{2}$ out as a factor, writing each term as $\frac{1}{2}\left[\tan^{-1}(2r+1) - \tan^{-1}(2r-1)\right]$."),
   (r"$\frac{3\pi}{4}$", r"Adds $\tan^{-1}1$ instead of subtracting it.")],
  r"Write $\frac{1}{2r^2} = \frac{2}{4r^2} = \frac{(2r+1) - (2r-1)}{1 + (2r+1)(2r-1)}$, so each term equals $\tan^{-1}(2r+1) - \tan^{-1}(2r-1)$. The partial sum is $\tan^{-1}(2n+1) - \tan^{-1}1$. As $n \to \infty$ this tends to $\frac{\pi}{2} - \frac{\pi}{4} = \frac{\pi}{4}$.",
  r"Mishandling the constant factor when forcing a term into difference form.",
  "U14-C-telescoping-infinite", r"Non-obvious rewriting of $\frac{1}{2r^2}$, telescoping, then a limit.",
  check=_c021, values=[pi/4, pi/2, pi/8, 3*pi/4], cognitive="Application")

# ---------------------------------------------------------------- 022
def _c022():
    a, b = 2*x, 3*x
    poly = numer(together((a + b)/(1 - a*b) - 1))
    return real_roots_filtered(poly, atan(2*x) + atan(3*x) - pi/4, x)
Q("U14-C-022", TOP, "Equation in tan^-1", "Medium", "Multi-step computation MCQ",
  r"The set of all real $x$ satisfying $\tan^{-1}(2x) + \tan^{-1}(3x) = \frac{\pi}{4}$ is",
  r"$\left\{\frac{1}{6}\right\}$",
  [(r"$\left\{-1, \frac{1}{6}\right\}$", r"Solves $6x^2 + 5x - 1 = 0$ but keeps $x = -1$, for which the left side is $-\tan^{-1}2 - \tan^{-1}3 = -\frac{3\pi}{4}$."),
   (r"$\left\{1, -\frac{1}{6}\right\}$", r"Sign slip in forming the quadratic, getting $6x^2 - 5x - 1 = 0$, and keeps both roots."),
   (r"$\{1\}$", r"Sign slip in forming the quadratic gives $6x^2 - 5x - 1 = 0$ (roots $1$ and $-\frac{1}{6}$); rejects the negative root and keeps $x = 1$.")],
  r"Taking tangents: $\frac{5x}{1 - 6x^2} = 1$, so $6x^2 + 5x - 1 = 0$, i.e. $(6x - 1)(x + 1) = 0$ and $x = \frac{1}{6}$ or $x = -1$. For $x = -1$ the left side is $-(\tan^{-1}2 + \tan^{-1}3) = -\frac{3\pi}{4} \ne \frac{\pi}{4}$, so it is rejected. For $x = \frac{1}{6}$, $\tan^{-1}\frac{1}{3} + \tan^{-1}\frac{1}{2} = \frac{\pi}{4}$. The solution set is $\left\{\frac{1}{6}\right\}$.",
  r"Not checking roots after taking tangent of both sides.",
  "U14-C-tan-equation-root-check", "Quadratic from the addition formula plus rejection of an extraneous root.",
  check=_c022,
  values=[FiniteSet(Rational(1, 6)), FiniteSet(-1, Rational(1, 6)), FiniteSet(1, -Rational(1, 6)), FiniteSet(1)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 023
def _c023():
    s1 = close(atan(Rational(1, 2)) + atan(Rational(1, 5)) + atan(Rational(1, 8)), pi/4)
    s2 = close(2*atan(2), pi - atan(Rational(4, 3)))
    return (s1, s2)
Q("U14-C-023", TOP, "Identities with tan^-1", "Medium", "Statement-based MCQ",
  r"Statement I: $\tan^{-1}\frac{1}{2} + \tan^{-1}\frac{1}{5} + \tan^{-1}\frac{1}{8} = \frac{\pi}{4}$. Statement II: $2\tan^{-1}2 = \pi - \tan^{-1}\frac{4}{3}$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Uses $2\tan^{-1}x = \tan^{-1}\frac{2x}{1-x^2}$ for $x = 2$, getting $\tan^{-1}\left(-\frac{4}{3}\right)$, and so rejects Statement II."),
   (ST_FT, r"Adds $\tan^{-1}\frac{1}{2} + \tan^{-1}\frac{1}{5}$ as $\tan^{-1}\frac{7}{10}$, dropping the denominator $1 - xy$; then $\tan^{-1}\frac{7}{10} + \tan^{-1}\frac{1}{8} = \tan^{-1}\frac{66}{73} \ne \frac{\pi}{4}$, so Statement I appears false."),
   (ST_FF, r"Drops the denominator $1 - xy$ when adding $\tan^{-1}\frac{1}{2} + \tan^{-1}\frac{1}{5}$, so Statement I appears false, and also uses $2\tan^{-1}x = \tan^{-1}\frac{2x}{1-x^2}$ for $x = 2$, getting $\tan^{-1}\left(-\frac{4}{3}\right)$, so Statement II appears false.")],
  r"For Statement I, $\tan^{-1}\frac{1}{2} + \tan^{-1}\frac{1}{5} = \tan^{-1}\frac{1/2 + 1/5}{1 - 1/10} = \tan^{-1}\frac{7}{9}$, and $\tan^{-1}\frac{7}{9} + \tan^{-1}\frac{1}{8} = \tan^{-1}\frac{7/9 + 1/8}{1 - 7/72} = \tan^{-1}\frac{65/72}{65/72} = \tan^{-1}1 = \frac{\pi}{4}$ (every product of arguments is less than $1$), so it is true. For Statement II, $x = 2 > 1$, so $2\tan^{-1}2 = \pi + \tan^{-1}\frac{4}{1 - 4} = \pi - \tan^{-1}\frac{4}{3}$, which is also true.",
  r"Using $2\tan^{-1}x = \tan^{-1}\frac{2x}{1-x^2}$ when $|x| > 1$.",
  "U14-C-statement-tan-identities", "Two separate verifications, one of which needs the $|x| > 1$ branch.",
  check=_c023,
  values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Analysis")

# ---------------------------------------------------------------- 024
Q("U14-C-024", TOP, "Using sin^-1 x + cos^-1 x = pi/2", "Medium", "Multi-step computation MCQ",
  r"For $x = \frac{1}{5}$, the value of $\cos\left(2\cos^{-1}x + \sin^{-1}x\right)$ is",
  r"$-\frac{2\sqrt{6}}{5}$",
  [(r"$\frac{2\sqrt{6}}{5}$", r"Uses $\cos\left(\frac{\pi}{2} + \theta\right) = \sin\theta$, losing the minus sign."),
   (r"$-\frac{1}{5}$", r"Uses $\cos\left(\frac{\pi}{2} + \theta\right) = -\cos\theta$, giving $-x$."),
   (r"$\frac{1}{5}$", r"Drops the $\frac{\pi}{2}$ shift entirely and evaluates $\cos(\cos^{-1}x)$.")],
  r"Write $2\cos^{-1}x + \sin^{-1}x = \frac{\pi}{2} + \cos^{-1}x$. Then $\cos\left(\frac{\pi}{2} + \theta\right) = -\sin\theta$ with $\theta = \cos^{-1}\frac{1}{5}$, and $\sin\theta = \sqrt{1 - \frac{1}{25}} = \frac{2\sqrt{6}}{5}$. So the value is $-\frac{2\sqrt{6}}{5}$.",
  r"Sign errors in the allied-angle formula after using the complementary identity.",
  "U14-C-complement-identity", "Identity reduction, an allied angle and a Pythagorean step.",
  check=lambda: cos(2*acos(Rational(1, 5)) + asin(Rational(1, 5))),
  values=[-2*sqrt(6)/5, 2*sqrt(6)/5, -Rational(1, 5), Rational(1, 5)], cognitive="Application")

# ---------------------------------------------------------------- 025
Q("U14-C-025", TOP, "Evaluating a combination of inverse functions", "Medium", "Multi-step computation MCQ",
  r"The value of $\tan\left(\cos^{-1}\frac{4}{5} + 2\tan^{-1}\frac{1}{3}\right)$ is",
  r"$\frac{24}{7}$",
  [(r"$\frac{17}{6}$", r"Takes $2\tan^{-1}\frac{1}{3} = \tan^{-1}\frac{2}{3}$, then $\frac{3/4 + 2/3}{1 - 1/2} = \frac{17}{6}$."),
   (r"$\frac{24}{25}$", r"Uses $1 + ab$ in the denominator: $\frac{3/4 + 3/4}{1 + 9/16} = \frac{24}{25}$."),
   (r"$\frac{7}{24}$", r"Computes everything correctly but reports the cotangent.")],
  r"$\cos^{-1}\frac{4}{5} = \tan^{-1}\frac{3}{4}$ and $2\tan^{-1}\frac{1}{3} = \tan^{-1}\frac{2/3}{1 - 1/9} = \tan^{-1}\frac{3}{4}$. So the angle is $2\tan^{-1}\frac{3}{4}$ and its tangent is $\frac{2 \cdot 3/4}{1 - 9/16} = \frac{3/2}{7/16} = \frac{24}{7}$.",
  r"Treating $2\tan^{-1}x$ as $\tan^{-1}2x$.",
  "U14-C-tan-sum-evaluate", "Two conversions and two applications of the double-angle formula.",
  check=lambda: tan(acos(Rational(4, 5)) + 2*atan(Rational(1, 3))),
  values=[Rational(24, 7), Rational(17, 6), Rational(24, 25), Rational(7, 24)],
  numerical=dict(question=r"If $T = \tan\left(\cos^{-1}\frac{4}{5} + 2\tan^{-1}\frac{1}{3}\right)$, then the value of $7T$ is", answer=24),
  cognitive="Application")

# ---------------------------------------------------------------- 026
Q("U14-C-026", TOP, "sin^-1(sin x) for a radian value", "Medium", "Single-step computation MCQ",
  r"The angle being in radians, $\sin^{-1}(\sin 10)$ equals",
  r"$3\pi - 10$",
  [(r"$10 - 3\pi$", r"Subtracts the nearest multiple of $\pi$ the other way round; $\sin(10 - 3\pi) = -\sin 10$."),
   (r"$10 - \frac{7\pi}{2}$", r"Subtracts the nearest multiple of $\frac{\pi}{2}$, namely $\frac{7\pi}{2}$, as if sine were unchanged by it; in fact $\sin\left(10 - \frac{7\pi}{2}\right) = \cos 10$."),
   (r"$\frac{7\pi}{2} - 10$", r"Reflects $10$ about $\frac{7\pi}{2}$ as if it were an odd multiple of $\pi$; in fact $\sin\left(\frac{7\pi}{2} - 10\right) = -\cos 10$.")],
  r"We need $\theta \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ with $\sin\theta = \sin 10$. Since $3\pi \approx 9.42$, the number $3\pi - 10 \approx -0.58$ lies in that interval, and $\sin(3\pi - 10) = \sin(\pi - 10) = \sin 10$. Hence $\sin^{-1}(\sin 10) = 3\pi - 10$.",
  r"Choosing a coterminal or reflected angle without checking both the sine value and the principal range.",
  "U14-C-inverse-of-function-radian", r"Locating $10$ between multiples of $\pi$ and using the right reflection.",
  check=lambda: asin(sin(Integer(10))),
  values=[3*pi - 10, 10 - 3*pi, 10 - 7*pi/2, 7*pi/2 - 10], cognitive="Analysis")

# ---------------------------------------------------------------- 027
Q("U14-C-027", TOP, "Compositions at radian values", "Medium", "Multi-step computation MCQ",
  r"The angles being in radians, $\tan^{-1}(\tan 5) + \cos^{-1}(\cos 5)$ equals",
  r"$0$",
  [(r"$\pi$", r"Reduces $\tan 5$ by one period only, taking $\tan^{-1}(\tan 5) = 5 - \pi \approx 1.86$, outside $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$."),
   (r"$10 - 3\pi$", r"Gets $5 - 2\pi$ for the first term but reflects about $\pi$ for the second, taking $\cos^{-1}(\cos 5) = 5 - \pi$; in fact $\cos(5 - \pi) = -\cos 5$."),
   (r"$4\pi - 10$", r"Reflects for the first term as well, taking $\tan^{-1}(\tan 5) = 2\pi - 5$ (but $\tan(2\pi - 5) = -\tan 5$), and correctly gets $2\pi - 5$ for the second.")],
  r"$5 - 2\pi \approx -1.28$ lies in $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$ and $\tan(5 - 2\pi) = \tan 5$, so $\tan^{-1}(\tan 5) = 5 - 2\pi$. Also $2\pi - 5 \approx 1.28$ lies in $[0, \pi]$ and $\cos(2\pi - 5) = \cos 5$, so $\cos^{-1}(\cos 5) = 2\pi - 5$. The sum is $0$.",
  r"Using $\theta$ itself, or the wrong shift, instead of the representative in the principal range.",
  "U14-C-inverse-of-function-radian", "Two different principal ranges for the same angle.",
  check=lambda: atan(tan(Integer(5))) + acos(cos(Integer(5))),
  values=[0, pi, 10 - 3*pi, 4*pi - 10], cognitive="Analysis")

# ---------------------------------------------------------------- 028
def _c028():
    T = Interval.Ropen(1, 2).intersect(Interval(-pi/2, pi/2))
    return Interval(sin(T.start), sin(T.end), T.left_open, T.right_open)
Q("U14-C-028", TOP, "Equation with the greatest integer function", "Medium", "Multi-step computation MCQ",
  r"Let $[t]$ denote the greatest integer less than or equal to $t$. The set of all $x$ satisfying $[\sin^{-1}x] = 1$ is",
  r"$[\sin 1, 1]$",
  [(r"$[\sin 1, \sin 2)$", r"Maps $1 \le \sin^{-1}x < 2$ directly to $\sin 1 \le x < \sin 2$, ignoring that $\sin^{-1}x \le \frac{\pi}{2} < 2$ and that $\sin$ is not increasing beyond $\frac{\pi}{2}$."),
   (r"$[\sin 1, 1)$", r"Excludes $x = 1$, not noticing that $\sin^{-1}1 = \frac{\pi}{2} \approx 1.57$ has integer part $1$."),
   (r"$(\sin 1, 1]$", r"Treats $[\sin^{-1}x] = 1$ as $\sin^{-1}x > 1$, excluding the left end.")],
  r"$[\sin^{-1}x] = 1$ means $1 \le \sin^{-1}x < 2$. Since $\sin^{-1}x \le \frac{\pi}{2} \approx 1.57$, this is $1 \le \sin^{-1}x \le \frac{\pi}{2}$. As $\sin$ is increasing on $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$, we get $\sin 1 \le x \le 1$.",
  r"Ignoring the principal range when undoing an inverse function.",
  "U14-C-greatest-integer", r"Greatest-integer condition combined with the range of $\sin^{-1}$.",
  check=_c028,
  values=[Interval(sin(1), 1), Interval.Ropen(sin(1), sin(2)), Interval.Ropen(sin(1), 1), Interval.Lopen(sin(1), 1)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 029
def _c029():
    u = (2*x - 1)/(x + 1)
    return Intersection(solveset(u <= 1, x, S.Reals), solveset(u >= -1, x, S.Reals))
Q("U14-C-029", TOP, "Domain", "Medium", "Multi-step computation MCQ",
  r"The domain of $f(x) = \sin^{-1}\left(\frac{2x - 1}{x + 1}\right)$ is",
  r"$[0, 2]$",
  [(r"$(-1, 2]$", r"Solves only $\frac{2x-1}{x+1} \le 1$, ignoring the lower bound $-1$."),
   (r"$(-\infty, -1) \cup [0, 2]$", r"Solves both inequalities but keeps the part $x < -1$ from the second, without intersecting with the first."),
   (r"$[0, \infty)$", r"Solves only $\frac{2x-1}{x+1} \ge -1$ and also drops its branch $x < -1$.")],
  r"Need $-1 \le \frac{2x-1}{x+1} \le 1$. The right inequality gives $\frac{x - 2}{x + 1} \le 0$, so $-1 < x \le 2$. The left gives $\frac{3x}{x + 1} \ge 0$, so $x < -1$ or $x \ge 0$. The intersection is $[0, 2]$.",
  r"Solving rational inequalities by cross-multiplying or handling only one side.",
  "U14-C-domain-rational", "Two rational inequalities and an intersection.",
  check=_c029,
  values=[Interval(0, 2), Interval.Lopen(-1, 2), Union(Interval.open(-oo, -1), Interval(0, 2)), Interval(0, oo)],
  cognitive="Application")

# ---------------------------------------------------------------- 030
def _c030():
    dom = Intersection(solveset(Abs((x - 3)/2) <= 1, x, S.Reals), solveset(4 - x > 0, x, S.Reals))
    return sum(1 for j in range(-20, 21) if dom.contains(j) == True)
Q("U14-C-030", TOP, "Domain", "Medium", "Single-step computation MCQ",
  r"The number of integers in the domain of $f(x) = \cos^{-1}\left(\frac{x - 3}{2}\right) - \log_{10}(4 - x)$ is",
  r"$3$",
  [(r"$4$", r"Allows $4 - x \ge 0$, so includes $x = 4$, where $\log_{10}0$ is undefined."),
   (r"$5$", r"Ignores the logarithm and counts the integers in $[1, 5]$."),
   (r"$2$", r"Takes the domain of $\cos^{-1}$ as the open interval $(-1, 1)$, so excludes $x = 1$.")],
  r"$\cos^{-1}\frac{x-3}{2}$ needs $-1 \le \frac{x-3}{2} \le 1$, i.e. $1 \le x \le 5$. The logarithm needs $4 - x > 0$, i.e. $x < 4$. The domain is $[1, 4)$, containing the integers $1, 2, 3$: three integers.",
  r"Allowing a zero argument inside a logarithm.",
  "U14-C-domain-log", "Two conditions and a count.",
  check=_c030, values=[3, 4, 5, 2],
  numerical=dict(question=r"The number of integers in the domain of $f(x) = \cos^{-1}\left(\frac{x - 3}{2}\right) - \log_{10}(4 - x)$ is", answer=3),
  cognitive="Application")

# ---------------------------------------------------------------- 031
def _c031():
    lhs = asin(3*x) + asin(4*x)
    # cos(lhs) = 0 gives sqrt(1-9x^2) sqrt(1-16x^2) = 12x^2; square it
    c = expand_trig(cos(lhs))
    assert simplify(c - (sqrt(1 - 9*x**2)*sqrt(1 - 16*x**2) - 12*x**2)) == 0
    poly = expand((1 - 9*x**2)*(1 - 16*x**2) - 144*x**4)
    return real_roots_filtered(poly, lhs - pi/2, x)
Q("U14-C-031", TOP, "Equation in sin^-1", "Medium", "Multi-step computation MCQ",
  r"The set of all real $x$ satisfying $\sin^{-1}(3x) + \sin^{-1}(4x) = \frac{\pi}{2}$ is",
  r"$\left\{\frac{1}{5}\right\}$",
  [(r"$\left\{-\frac{1}{5}, \frac{1}{5}\right\}$", r"Solves $25x^2 = 1$ but keeps $x = -\frac{1}{5}$, for which the left side is $-\frac{\pi}{2}$."),
   (r"$\left\{\frac{1}{7}\right\}$", r"Writes $\sqrt{1 - 9x^2}$ as $1 - 3x$, so $4x = 1 - 3x$."),
   (r"$\left\{\frac{1}{\sqrt{7}}\right\}$", r"Sign slip when squaring: $16x^2 = 1 + 9x^2$, so $7x^2 = 1$.")],
  r"The equation gives $\sin^{-1}(4x) = \frac{\pi}{2} - \sin^{-1}(3x) = \cos^{-1}(3x)$, so $4x = \sqrt{1 - 9x^2}$ with $x \ge 0$. Squaring, $16x^2 = 1 - 9x^2$, so $x^2 = \frac{1}{25}$ and $x = \frac{1}{5}$. Check: $\sin^{-1}\frac{3}{5} + \sin^{-1}\frac{4}{5} = \frac{\pi}{2}$.",
  r"Keeping a root introduced by squaring.",
  "U14-C-sin-equation-root-check", "Complementary identity, squaring and a sign check.",
  check=_c031,
  values=[FiniteSet(Rational(1, 5)), FiniteSet(-Rational(1, 5), Rational(1, 5)), FiniteSet(Rational(1, 7)), FiniteSet(1/sqrt(7))],
  cognitive="Application")

# ---------------------------------------------------------------- 032
Q("U14-C-032", TOP, "Half angle of an inverse function", "Medium", "Multi-step computation MCQ",
  r"The value of $\tan\left(\frac{1}{2}\cos^{-1}\frac{\sqrt{5}}{3}\right)$ is",
  r"$\frac{3 - \sqrt{5}}{2}$",
  [(r"$\frac{3 + \sqrt{5}}{2}$", r"Uses $\frac{1 + \cos\theta}{\sin\theta}$, which is $\cot\frac{\theta}{2}$."),
   (r"$\frac{1}{\sqrt{5}}$", r"Halves the tangent: $\frac{1}{2}\tan\theta = \frac{1}{2}\cdot\frac{2}{\sqrt{5}}$."),
   (r"$\frac{7 - 3\sqrt{5}}{2}$", r"Uses $\frac{1 - \cos\theta}{1 + \cos\theta}$ without the square root, which is $\tan^2\frac{\theta}{2}$.")],
  r"Let $\theta = \cos^{-1}\frac{\sqrt{5}}{3} \in \left(0, \frac{\pi}{2}\right)$, so $\sin\theta = \frac{2}{3}$. Then $\tan\frac{\theta}{2} = \frac{\sin\theta}{1 + \cos\theta} = \frac{2/3}{(3 + \sqrt{5})/3} = \frac{2}{3 + \sqrt{5}} = \frac{3 - \sqrt{5}}{2}$.",
  r"Confusing $\tan\frac{\theta}{2}$ with $\cot\frac{\theta}{2}$ or with $\tan^2\frac{\theta}{2}$.",
  "U14-C-half-angle-of-inverse", "Pythagorean step, half-angle formula and rationalisation.",
  check=lambda: tan(acos(sqrt(5)/3)/2),
  values=[(3 - sqrt(5))/2, (3 + sqrt(5))/2, 1/sqrt(5), (7 - 3*sqrt(5))/2], cognitive="Application")

# ---------------------------------------------------------------- 033
Q("U14-C-033", TOP, "Nested inverse functions", "Medium", "Multi-step computation MCQ",
  r"For real $x$, with $\cot^{-1}$ taking values in $(0, \pi)$, $\sin\left(\cot^{-1}\left(\cos\left(\tan^{-1}x\right)\right)\right)$ equals",
  r"$\sqrt{\frac{x^2 + 1}{x^2 + 2}}$",
  [(r"$\sqrt{\frac{x^2 + 2}{x^2 + 1}}$", r"Computes $\sqrt{1 + \cot^2\theta}$, which is $\operatorname{cosec}\theta$, not $\sin\theta$."),
   (r"$\frac{1}{\sqrt{x^2 + 2}}$", r"Computes $\cos\theta = \frac{\cot\theta}{\sqrt{1 + \cot^2\theta}}$ for the outer angle."),
   (r"$\sqrt{\frac{x^2 + 1}{2x^2 + 1}}$", r"Uses $\sin(\tan^{-1}x) = \frac{x}{\sqrt{1+x^2}}$ in place of $\cos(\tan^{-1}x)$ for the inner step.")],
  r"$\cos(\tan^{-1}x) = \frac{1}{\sqrt{1 + x^2}}$, which is positive. Let $\theta = \cot^{-1}\frac{1}{\sqrt{1+x^2}} \in \left(0, \frac{\pi}{2}\right)$. Then $\sin\theta = \frac{1}{\sqrt{1 + \cot^2\theta}} = \frac{1}{\sqrt{1 + \frac{1}{1 + x^2}}} = \sqrt{\frac{x^2 + 1}{x^2 + 2}}$.",
  r"Mixing up $\sin$, $\cos$ and $\operatorname{cosec}$ when converting through right triangles.",
  "U14-C-trig-of-inverse", "Two nested triangle conversions.",
  check=lambda: sin(acotp(cos(atan(x)))),
  values=[sqrt((x**2 + 1)/(x**2 + 2)), sqrt((x**2 + 2)/(x**2 + 1)), 1/sqrt(x**2 + 2), sqrt((x**2 + 1)/(2*x**2 + 1))],
  cognitive="Application")

# ---------------------------------------------------------------- 034
def _c034():
    kk = Symbol('kk', real=True)
    a, b, c = kk, 2*kk, 3*kk
    # sum = pi/2 forces the denominator of tan(sum) to vanish: 1 - (ab + bc + ca) = 0
    cands = solve(1 - (a*b + b*c + c*a), kk)
    good = [r for r in cands if close(atan(r) + atan(2*r) + atan(3*r), pi/2)]
    assert len(good) == 1
    # for kk <= 0 the left side is <= 0, so no other solution
    return nsimplify(good[0])
Q("U14-C-034", TOP, "Three tan^-1 terms with a given sum", "Medium", "Inverse/parameter MCQ",
  r"If $\tan^{-1}k + \tan^{-1}(2k) + \tan^{-1}(3k) = \frac{\pi}{2}$ for a real number $k$, then $k$ equals",
  r"$\frac{1}{\sqrt{11}}$",
  [(r"$1$", r"Uses the condition for a sum of $\pi$, namely $x + y + z = xyz$: $6k = 6k^3$, so $k = 1$ (rejecting $k = 0$)."),
   (r"$\frac{1}{\sqrt{7}}$", r"Writes $\tan^{-1}k + \tan^{-1}(2k) = \frac{\pi}{2} - \tan^{-1}(3k)$ but uses $1 + xy$ in the denominator: $\frac{3k}{1 + 2k^2} = \frac{1}{3k}$ gives $7k^2 = 1$."),
   (r"$\frac{1}{\sqrt{5}}$", r"Uses $xy + yz + zx = 1$ but lists only the products $k \cdot 2k$ and $k \cdot 3k$, omitting $2k \cdot 3k$, so $5k^2 = 1$.")],
  r"If $k \le 0$ every term is $\le 0$, so $k > 0$. Then $\tan^{-1}k + \tan^{-1}(2k) = \frac{\pi}{2} - \tan^{-1}(3k) = \tan^{-1}\frac{1}{3k}$. Taking tangents, $\frac{3k}{1 - 2k^2} = \frac{1}{3k}$, so $9k^2 = 1 - 2k^2$, i.e. $11k^2 = 1$ and $k = \frac{1}{\sqrt{11}}$. Here $k \cdot 2k = \frac{2}{11} < 1$, so the addition formula applies without correction.",
  r"Confusing the conditions for $\tan^{-1}x + \tan^{-1}y + \tan^{-1}z = \frac{\pi}{2}$ and $= \pi$.",
  "U14-C-tan-three-sum-param", r"Sign argument to fix $k > 0$, complementary conversion, then the addition formula and a quadratic in $k^2$.",
  check=_c034, values=[1/sqrt(11), 1, 1/sqrt(7), 1/sqrt(5)],
  numerical=dict(question=r"If $\tan^{-1}k + \tan^{-1}(2k) + \tan^{-1}(3k) = \frac{\pi}{2}$ for a real number $k$, then the value of $\frac{1}{k^2}$ is", answer=11),
  cognitive="Application")

# ---------------------------------------------------------------- 035
Q("U14-C-035", TOP, "Evaluating a combination of inverse functions", "Medium", "Multi-step computation MCQ",
  r"The value of $\cot\left(\operatorname{cosec}^{-1}\frac{5}{4} + \tan^{-1}\frac{1}{2}\right)$ is",
  r"$\frac{2}{11}$",
  [(r"$\frac{11}{2}$", r"Computes the tangent of the sum correctly but does not take the reciprocal."),
   (r"$\frac{10}{11}$", r"Uses $1 + ab$ in the denominator: $\tan = \frac{11/6}{5/3} = \frac{11}{10}$, then inverts."),
   (r"$\frac{1}{2}$", r"Takes $\operatorname{cosec}^{-1}\frac{5}{4} = \tan^{-1}\frac{3}{4}$ (sides swapped), then $\tan = \frac{3/4 + 1/2}{1 - 3/8} = 2$.")],
  r"If $\operatorname{cosec}\theta = \frac{5}{4}$ with $\theta$ acute, then $\sin\theta = \frac{4}{5}$, $\cos\theta = \frac{3}{5}$ and $\tan\theta = \frac{4}{3}$. So $\tan\left(\theta + \tan^{-1}\frac{1}{2}\right) = \frac{4/3 + 1/2}{1 - 2/3} = \frac{11/6}{1/3} = \frac{11}{2}$. Hence the cotangent is $\frac{2}{11}$.",
  r"Mislabelling opposite and adjacent sides when converting $\operatorname{cosec}^{-1}$ to $\tan^{-1}$.",
  "U14-C-tan-sum-evaluate", "Conversion, addition formula and a reciprocal.",
  check=lambda: 1/tan(acsc(Rational(5, 4)) + atan(Rational(1, 2))),
  values=[Rational(2, 11), Rational(11, 2), Rational(10, 11), Rational(1, 2)], cognitive="Application")

# ---------------------------------------------------------------- 036
def _c036():
    f = asin(x) - acos(x)
    assert simplify(diff(f, x) - 2/sqrt(1 - x**2)) == 0  # increasing
    c = nsimplify(nsolve(f, x, 0.7), [sqrt(2)])
    return Interval.Lopen(c, 1)
Q("U14-C-036", TOP, "Inequality in inverse functions", "Medium", "Single-step computation MCQ",
  r"The set of all $x$ for which $\sin^{-1}x > \cos^{-1}x$ is",
  r"$\left(\frac{1}{\sqrt{2}}, 1\right]$",
  [(r"$\left[\frac{1}{\sqrt{2}}, 1\right]$", r"Includes $x = \frac{1}{\sqrt{2}}$, where the two sides are equal."),
   (r"$(0, 1]$", r"Assumes $\sin^{-1}x$ exceeds $\cos^{-1}x$ whenever $x > 0$."),
   (r"$\left[-1, \frac{1}{\sqrt{2}}\right)$", r"Reverses the inequality while solving $2\sin^{-1}x > \frac{\pi}{2}$.")],
  r"Using $\cos^{-1}x = \frac{\pi}{2} - \sin^{-1}x$, the inequality becomes $2\sin^{-1}x > \frac{\pi}{2}$, i.e. $\sin^{-1}x > \frac{\pi}{4}$. Since $\sin^{-1}$ is increasing on $[-1, 1]$, this means $\frac{1}{\sqrt{2}} < x \le 1$.",
  r"Mishandling strictness or direction when undoing an increasing inverse function.",
  "U14-C-inequality", "Identity reduction and monotonicity.",
  check=_c036,
  values=[Interval.Lopen(1/sqrt(2), 1), Interval(1/sqrt(2), 1), Interval.Lopen(0, 1), Interval.Ropen(-1, 1/sqrt(2))],
  cognitive="Application")

# ---------------------------------------------------------------- 037
Q("U14-C-037", TOP, "cot^-1 of negative arguments", "Medium", "Multi-step computation MCQ",
  r"With $\cot^{-1}$ taking values in $(0, \pi)$, the value of $\cot^{-1}\left(-\frac{1}{2}\right) + \cot^{-1}\left(-\frac{1}{3}\right)$ is",
  r"$\frac{5\pi}{4}$",
  [(r"$\frac{7\pi}{4}$", r"Correctly writes the sum as $2\pi - (\tan^{-1}2 + \tan^{-1}3)$ but uses $xy - 1$ as the denominator, getting $\tan^{-1}2 + \tan^{-1}3 = \tan^{-1}1 = \frac{\pi}{4}$."),
   (r"$\frac{3\pi}{2}$", r"Correctly writes the sum as $2\pi - (\tan^{-1}2 + \tan^{-1}3)$ but takes $\tan^{-1}2 + \tan^{-1}3 = \frac{\pi}{2}$, overgeneralising the rule $\tan^{-1}x + \tan^{-1}\frac{1}{x} = \frac{\pi}{2}$."),
   (r"$\frac{3\pi}{4}$", r"Ignores the negative signs and evaluates $\cot^{-1}\frac{1}{2} + \cot^{-1}\frac{1}{3}$.")],
  r"$\cot^{-1}(-x) = \pi - \cot^{-1}x$, so the sum is $2\pi - \left(\cot^{-1}\frac{1}{2} + \cot^{-1}\frac{1}{3}\right) = 2\pi - (\tan^{-1}2 + \tan^{-1}3)$. As $2 \cdot 3 > 1$, $\tan^{-1}2 + \tan^{-1}3 = \pi + \tan^{-1}(-1) = \frac{3\pi}{4}$. Hence the value is $2\pi - \frac{3\pi}{4} = \frac{5\pi}{4}$.",
  r"Mishandling $\tan^{-1}x + \tan^{-1}y$ when $xy > 1$, or ignoring the negative signs.",
  "U14-C-cot-negative-sum", r"Negative-argument rule, conversion to $\tan^{-1}$ and the $xy > 1$ case.",
  check=lambda: acotp(-Rational(1, 2)) + acotp(-Rational(1, 3)),
  values=[5*pi/4, 7*pi/4, 3*pi/2, 3*pi/4], cognitive="Analysis")

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 038
def _c038():
    # take sine of both sides of sin^-1(1-x) = pi/2 + 2 sin^-1 x
    poly = simplify(expand_trig((1 - x) - sin(pi/2 + 2*asin(x))))
    return real_roots_filtered(poly, asin(1 - x) - 2*asin(x) - pi/2, x)
Q("U14-C-038", TOP, "Equation in sin^-1 with an extraneous root", "Difficult", "Multi-step computation MCQ",
  r"The set of all real $x$ satisfying $\sin^{-1}(1 - x) - 2\sin^{-1}x = \frac{\pi}{2}$ is",
  r"$\{0\}$",
  [(r"$\left\{\frac{1}{2}\right\}$", r"Divides $2x^2 = x$ by $x$, losing $x = 0$, and does not test $x = \frac{1}{2}$."),
   (r"$\left\{0, \frac{1}{2}\right\}$", r"Solves $2x^2 - x = 0$ correctly but keeps $x = \frac{1}{2}$, for which the left side is $\frac{\pi}{6} - \frac{\pi}{3} = -\frac{\pi}{6}$."),
   (r"$\left\{-\frac{1}{2}, 0\right\}$", r"Sign slip giving $2x^2 + x = 0$ and no verification; $x = -\frac{1}{2}$ makes $\sin^{-1}\frac{3}{2}$ undefined.")],
  r"Let $\sin^{-1}x = \theta$. Then $\sin^{-1}(1 - x) = \frac{\pi}{2} + 2\theta$, so $1 - x = \cos 2\theta = 1 - 2x^2$, giving $x(2x - 1) = 0$. For $x = \frac{1}{2}$: $\sin^{-1}\frac{1}{2} - 2\sin^{-1}\frac{1}{2} = -\frac{\pi}{6} \ne \frac{\pi}{2}$, so it is rejected. For $x = 0$: $\sin^{-1}1 - 0 = \frac{\pi}{2}$. The solution set is $\{0\}$.",
  r"Accepting roots of the squared or transformed equation without substituting back.",
  "U14-C-sin-equation-root-check", "Substitution, double angle, and rejection of an extraneous root.",
  check=_c038,
  values=[FiniteSet(0), FiniteSet(Rational(1, 2)), FiniteSet(0, Rational(1, 2)), FiniteSet(-Rational(1, 2), 0)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 039
def _range_quad(power):
    f = asin(x)**power + acos(x)**power
    c = nsimplify(nsolve(asin(x) - acos(x), x, 0.7), [sqrt(2)])
    # interior critical points: f'(x) = power*(asin^(p-1) - acos^(p-1))/sqrt(1-x^2) vanishes only where asin = acos
    assert abs(N(diff(f, x).subs(x, c))) < 1e-20
    vals = [simplify(f.subs(x, p)) for p in (-1, 1, c)]
    return min(vals, key=lambda v: N(v)), max(vals, key=lambda v: N(v))
def _c039():
    lo, hi = _range_quad(2)
    return Interval(lo, hi)
Q("U14-C-039", TOP, "Range of a quadratic in sin^-1 x", "Difficult", "Multi-step computation MCQ",
  r"The range of $f(x) = (\sin^{-1}x)^2 + (\cos^{-1}x)^2$ is",
  r"$\left[\frac{\pi^2}{8}, \frac{5\pi^2}{4}\right]$",
  [(r"$\left[\frac{\pi^2}{8}, \frac{\pi^2}{4}\right]$", r"Finds the minimum correctly but evaluates the maximum at $x = 1$ instead of $x = -1$."),
   (r"$\left[0, \frac{5\pi^2}{4}\right]$", r"Assumes a sum of squares has least value $0$ without checking that both terms cannot vanish together."),
   (r"$\left[\frac{\pi^2}{4}, \frac{5\pi^2}{4}\right]$", r"Uses only the endpoint values $x = \pm 1$, missing the interior minimum at $x = \frac{1}{\sqrt{2}}$.")],
  r"Put $t = \sin^{-1}x \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$, so $\cos^{-1}x = \frac{\pi}{2} - t$ and $f = 2t^2 - \pi t + \frac{\pi^2}{4} = 2\left(t - \frac{\pi}{4}\right)^2 + \frac{\pi^2}{8}$. The minimum $\frac{\pi^2}{8}$ is at $t = \frac{\pi}{4}$. The maximum is at the endpoint farther from $\frac{\pi}{4}$, $t = -\frac{\pi}{2}$: $2\cdot\frac{9\pi^2}{16} + \frac{\pi^2}{8} = \frac{5\pi^2}{4}$.",
  r"Taking the extreme values of a quadratic on an interval only at the endpoints, or at the wrong endpoint.",
  "U14-C-range-quadratic", "Substitution, completing the square, and choosing the farther endpoint.",
  check=_c039,
  values=[Interval(pi**2/8, 5*pi**2/4), Interval(pi**2/8, pi**2/4), Interval(0, 5*pi**2/4), Interval(pi**2/4, 5*pi**2/4)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 040
def _c040():
    lo, hi = _range_quad(3)
    return simplify(hi/lo)
Q("U14-C-040", TOP, "Range of a cubic in sin^-1 x", "Difficult", "Multi-step computation MCQ",
  r"If the range of $f(x) = (\sin^{-1}x)^3 + (\cos^{-1}x)^3$ is $[\alpha, \beta]$, then $\frac{\beta}{\alpha}$ equals",
  r"$28$",
  [(r"$4$", r"Finds $\alpha = \frac{\pi^3}{32}$ correctly but takes $\beta$ at $x = 1$, i.e. $\beta = \frac{\pi^3}{8}$."),
   (r"$7$", r"Finds $\beta = \frac{7\pi^3}{8}$ but takes $\alpha$ at the endpoint $x = 1$, i.e. $\alpha = \frac{\pi^3}{8}$, missing the interior minimum."),
   (r"$56$", r"Evaluates the minimum as $\left(\frac{\pi}{4}\right)^3 = \frac{\pi^3}{64}$, forgetting that both cubes contribute.")],
  r"With $t = \sin^{-1}x$ and $a = \frac{\pi}{2}$, $f = t^3 + (a - t)^3 = a\left(3t^2 - 3at + a^2\right)$. On $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ the minimum is at $t = \frac{a}{2}$: $\alpha = \frac{a^3}{4} = \frac{\pi^3}{32}$. The maximum is at $t = -a$: $\beta = 7a^3 = \frac{7\pi^3}{8}$. So $\frac{\beta}{\alpha} = 28$.",
  r"Missing the interior extremum or using the wrong endpoint.",
  "U14-C-range-quadratic", "Algebraic reduction of a cubic sum to a quadratic, then extremes on an interval.",
  check=_c040, values=[28, 4, 7, 56],
  numerical=dict(question=r"If the range of $f(x) = (\sin^{-1}x)^3 + (\cos^{-1}x)^3$ is $[\alpha, \beta]$, then the value of $\frac{\beta}{\alpha}$ is", answer=28),
  cognitive="Analysis")

# ---------------------------------------------------------------- 041
Q("U14-C-041", TOP, "sin^-1 x + sin^-1 y when x^2 + y^2 > 1", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sin^{-1}\frac{3}{5} + \sin^{-1}\frac{12}{13}$ is",
  r"$\pi - \sin^{-1}\frac{63}{65}$",
  [(r"$\sin^{-1}\frac{63}{65}$", r"Applies $\sin^{-1}\left(x\sqrt{1-y^2} + y\sqrt{1-x^2}\right)$ without noticing $x^2 + y^2 > 1$, so the sum exceeds $\frac{\pi}{2}$."),
   (r"$\cos^{-1}\frac{56}{65}$", r"Computes $\cos(A+B)$ with a plus sign: $\frac{4}{5}\cdot\frac{5}{13} + \frac{3}{5}\cdot\frac{12}{13} = \frac{56}{65}$."),
   (r"$\pi - \sin^{-1}\frac{33}{65}$", r"Knows the sum is obtuse but subtracts the products: $\frac{48}{65} - \frac{15}{65} = \frac{33}{65}$.")],
  r"Let $A = \sin^{-1}\frac{3}{5}$, $B = \sin^{-1}\frac{12}{13}$, both acute, with $\cos A = \frac{4}{5}$, $\cos B = \frac{5}{13}$. Then $\sin(A+B) = \frac{15}{65} + \frac{48}{65} = \frac{63}{65}$ and $\cos(A+B) = \frac{20}{65} - \frac{36}{65} = -\frac{16}{65} < 0$, so $A + B$ is obtuse. Hence $A + B = \pi - \sin^{-1}\frac{63}{65}$ (the condition $\frac{9}{25} + \frac{144}{169} > 1$ signals this).",
  r"Ignoring the $x^2 + y^2 \le 1$ condition of the $\sin^{-1}$ addition formula.",
  "U14-C-sin-sum-condition", "Addition formula plus a quadrant decision that most students skip.",
  check=lambda: asin(Rational(3, 5)) + asin(Rational(12, 13)),
  values=[pi - asin(Rational(63, 65)), asin(Rational(63, 65)), acos(Rational(56, 65)), pi - asin(Rational(33, 65))],
  cognitive="Analysis")

# ---------------------------------------------------------------- 042
_P042 = [Rational(3, 4), Rational(4, 5), Rational(9, 10)]
def _c042():
    return tuple(asin(2*p*sqrt(1 - p**2)) for p in _P042)
Q("U14-C-042", TOP, "Simplification by sine substitution", "Difficult", "Conceptual/application MCQ",
  r"For $\frac{1}{\sqrt{2}} < x < 1$, the expression $\sin^{-1}\left(2x\sqrt{1 - x^2}\right)$ equals",
  r"$\pi - 2\sin^{-1}x$",
  [(r"$2\sin^{-1}x$", r"Uses the formula valid only for $|x| \le \frac{1}{\sqrt{2}}$; here $2\sin^{-1}x > \frac{\pi}{2}$, outside the range of $\sin^{-1}$."),
   (r"$2\sin^{-1}x - \frac{\pi}{2}$", r"Shifts instead of reflecting, assuming $\sin 2\theta = \sin\left(2\theta - \frac{\pi}{2}\right)$ so as to land in $\left(0, \frac{\pi}{2}\right)$; in fact $\sin\left(2\theta - \frac{\pi}{2}\right) = -\cos 2\theta$."),
   (r"$\frac{\pi}{2} - \sin^{-1}x$", r"Substitutes $x = \cos\phi$, so the argument is $\sin 2\phi$ with $2\phi \in \left(0, \frac{\pi}{2}\right)$, but then writes $\sin^{-1}(\sin 2\phi) = \phi$, losing the factor $2$; this gives $\cos^{-1}x = \frac{\pi}{2} - \sin^{-1}x$.")],
  r"Put $x = \sin\theta$ with $\theta \in \left(\frac{\pi}{4}, \frac{\pi}{2}\right)$; then $2x\sqrt{1-x^2} = \sin 2\theta$ with $2\theta \in \left(\frac{\pi}{2}, \pi\right)$. Since $\sin 2\theta = \sin(\pi - 2\theta)$ and $\pi - 2\theta \in \left(0, \frac{\pi}{2}\right)$, the expression is $\pi - 2\theta = \pi - 2\sin^{-1}x$.",
  r"Applying $\sin^{-1}(2x\sqrt{1-x^2}) = 2\sin^{-1}x$ outside $|x| \le \frac{1}{\sqrt{2}}$.",
  "U14-C-double-angle-branch", r"Substitution, locating $2\theta$, and the correct reflection.",
  check=_c042,
  values=[tuple(pi - 2*asin(p) for p in _P042), tuple(2*asin(p) for p in _P042),
          tuple(2*asin(p) - pi/2 for p in _P042), tuple(pi/2 - asin(p) for p in _P042)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 043
def _c043():
    pts1 = [-Rational(9, 10), -Rational(1, 2), 0, Rational(1, 2), Rational(9, 10)]
    s1 = holds_at(asin(2*x*sqrt(1 - x**2)), 2*asin(x), x, pts1)
    pts2 = [-3, -Rational(1, 2), 0, Rational(1, 2), 3]
    s2 = holds_at(2*atan(x), asin(2*x/(1 + x**2)), x, pts2)
    return (s1, s2)
Q("U14-C-043", TOP, "Validity of double-angle formulas", "Difficult", "Statement-based MCQ",
  r"Statement I: $\sin^{-1}\left(2x\sqrt{1 - x^2}\right) = 2\sin^{-1}x$ for every $x \in [-1, 1]$. Statement II: $2\tan^{-1}x = \sin^{-1}\left(\frac{2x}{1 + x^2}\right)$ for every real $x$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts both standard formulas without their validity intervals $|x| \le \frac{1}{\sqrt{2}}$ and $|x| \le 1$."),
   (ST_TF, r"Accepts Statement I, missing that for $x = 1$ the left side is $0$ while the right side is $\pi$."),
   (ST_FT, r"Accepts Statement II, missing that for $x = 3$ the left side exceeds $\frac{\pi}{2}$, outside the range of $\sin^{-1}$.")],
  r"Statement I fails at $x = 1$: the left side is $\sin^{-1}0 = 0$ but $2\sin^{-1}1 = \pi$; it holds only for $|x| \le \frac{1}{\sqrt{2}}$. Statement II fails at $x = 3$: since $\tan^{-1}3 > \frac{\pi}{4}$, we get $2\tan^{-1}3 > \frac{\pi}{2}$, while $\sin^{-1}$ never exceeds $\frac{\pi}{2}$; it holds only for $|x| \le 1$. Both statements are false.",
  r"Using double-angle inverse formulas without their validity intervals.",
  "U14-C-statement-branch-formulas", "Two formulas whose failure needs a deliberately chosen counterexample.",
  check=_c043,
  values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 044
def _c044():
    found = []
    for nn in range(1, 200):
        tv = Integer(0)
        for j in range(1, nn + 1):
            a = Rational(1, j**2 + 3*j + 3)  # tan(cot^{-1} u) = 1/u for u > 0
            tv = (tv + a)/(1 - tv*a)
        if tv == Rational(2, 5):
            found.append(nn)
    assert len(found) == 1
    return found[0]
Q("U14-C-044", TOP, "Telescoping sum of cot^-1 terms", "Difficult", "Inverse/parameter MCQ",
  r"Let $S_n = \sum_{k=1}^{n} \cot^{-1}\left(k^2 + 3k + 3\right)$. If $\tan S_n = \frac{2}{5}$, then $n$ equals",
  r"$10$",
  [(r"$9$", r"Telescopes to $\tan^{-1}(n+3) - \tan^{-1}2$ (upper end one too far), so $\frac{n+1}{2n+7} = \frac{2}{5}$."),
   (r"$11$", r"Telescopes to $\tan^{-1}(n+1) - \tan^{-1}2$ (upper end one short), so $\frac{n-1}{2n+3} = \frac{2}{5}$."),
   (r"$8$", r"Correct telescoping but drops the $1$ in $1 + 2(n+2)$, so $\frac{n}{2n+4} = \frac{2}{5}$.")],
  r"$\cot^{-1}(k^2 + 3k + 3) = \tan^{-1}\frac{1}{1 + (k+1)(k+2)} = \tan^{-1}(k+2) - \tan^{-1}(k+1)$. So $S_n = \tan^{-1}(n+2) - \tan^{-1}2$ and $\tan S_n = \frac{n}{1 + 2(n+2)} = \frac{n}{2n + 5}$. Setting $\frac{n}{2n+5} = \frac{2}{5}$ gives $5n = 4n + 10$, so $n = 10$.",
  r"Mis-indexing the ends of a telescoping sum.",
  "U14-C-telescoping-parameter", r"Convert $\cot^{-1}$ to $\tan^{-1}$, find the difference form, telescope, then solve for $n$.",
  check=_c044, values=[10, 9, 11, 8],
  numerical=dict(question=r"Let $S_n = \sum_{k=1}^{n} \cot^{-1}\left(k^2 + 3k + 3\right)$. If $\tan S_n = \frac{2}{5}$, then the value of $n$ is", answer=10),
  cognitive="Analysis")

# ---------------------------------------------------------------- 045
def _c045():
    r_ = Symbol('r', positive=True)
    nn = Symbol('nn', positive=True)
    diff_form = (2**(r_ + 1) - 2**r_)/(1 + 2**(r_ + 1)*2**r_)
    assert simplify(diff_form - 2**r_/(1 + 2**(2*r_ + 1))) == 0
    return limit(atan(2**(nn + 1)), nn, oo) - atan(2)
Q("U14-C-045", TOP, "Infinite telescoping sum", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sum_{r=1}^{\infty} \tan^{-1}\left(\frac{2^r}{1 + 2^{2r+1}}\right)$ is",
  r"$\tan^{-1}\frac{1}{2}$",
  [(r"$\tan^{-1}\frac{1}{4}$", r"Starts the telescoping at $\tan^{-1}4$ instead of $\tan^{-1}2$, giving $\frac{\pi}{2} - \tan^{-1}4$."),
   (r"$\frac{\pi}{4}$", r"Starts the telescoping at $\tan^{-1}1$ (as if $r$ began at $0$), giving $\frac{\pi}{2} - \frac{\pi}{4}$."),
   (r"$\tan^{-1}2$", r"Reports the subtracted first term $\tan^{-1}2$ instead of $\frac{\pi}{2} - \tan^{-1}2$.")],
  r"Since $2^{2r+1} = 2^{r+1}\cdot 2^r$ and $2^{r+1} - 2^r = 2^r$, each term is $\tan^{-1}2^{r+1} - \tan^{-1}2^r$. The partial sum is $\tan^{-1}2^{n+1} - \tan^{-1}2$, which tends to $\frac{\pi}{2} - \tan^{-1}2 = \cot^{-1}2 = \tan^{-1}\frac{1}{2}$.",
  r"Mis-identifying the first term of a telescoping series.",
  "U14-C-telescoping-infinite", "Spotting the exponential difference form, telescoping and a limit.",
  check=_c045, values=[atan(Rational(1, 2)), atan(Rational(1, 4)), pi/4, atan(2)], cognitive="Analysis")

# ---------------------------------------------------------------- 046
def _c046():
    return sum(asin((sqrt(j) - sqrt(j - 1))/sqrt(j*(j + 1))) for j in range(1, 4))
Q("U14-C-046", TOP, "Telescoping sum of sin^-1 terms", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sum_{r=1}^{3} \sin^{-1}\left(\frac{\sqrt{r} - \sqrt{r - 1}}{\sqrt{r(r+1)}}\right)$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\tan^{-1}\sqrt{2}$", r"Telescopes correctly but stops at $r = 2$, giving $\tan^{-1}\sqrt{2}$."),
   (r"$\frac{\pi}{12}$", r"Subtracts $\tan^{-1}\sqrt{1} = \frac{\pi}{4}$ as the first term instead of $\tan^{-1}0$, giving $\frac{\pi}{3} - \frac{\pi}{4}$."),
   (r"$\tan^{-1}2$", r"Telescopes to $\tan^{-1}\sqrt{n+1} = \tan^{-1}\sqrt{4}$, shifting the upper end by one.")],
  r"Let $A = \tan^{-1}\sqrt{r}$, $B = \tan^{-1}\sqrt{r-1}$. Then $\tan(A - B) = \frac{\sqrt{r} - \sqrt{r-1}}{1 + \sqrt{r(r-1)}}$, and since $(\sqrt{r} - \sqrt{r-1})^2 + (1 + \sqrt{r(r-1)})^2 = r(r+1)$, $\sin(A - B) = \frac{\sqrt{r} - \sqrt{r-1}}{\sqrt{r(r+1)}}$ with $A - B \in \left[0, \frac{\pi}{2}\right)$. So each term is $\tan^{-1}\sqrt{r} - \tan^{-1}\sqrt{r-1}$ and the sum is $\tan^{-1}\sqrt{3} - \tan^{-1}0 = \frac{\pi}{3}$.",
  r"Mis-identifying the first or last term in telescoping.",
  "U14-C-telescoping-sin", r"Recognising a $\sin^{-1}$ term as a difference of $\tan^{-1}$ terms needs a non-obvious identity.",
  check=_c046, values=[pi/3, atan(sqrt(2)), pi/12, atan(2)], cognitive="Analysis")

# ---------------------------------------------------------------- 047
def _c047():
    tsol = solveset((t - 2)*(t - 3) > 0, t, Interval.open(0, pi))
    parts = tsol.args if isinstance(tsol, Union) else (tsol,)
    out = []
    for I_ in parts:
        a, b = I_.start, I_.end
        lo = -oo if b == pi else cot(b)
        hi = oo if a == 0 else cot(a)
        out.append(Interval.open(lo, hi))
    return Union(*out)
Q("U14-C-047", TOP, "Quadratic inequality in cot^-1 x", "Difficult", "Multi-step computation MCQ",
  r"With $\cot^{-1}x \in (0, \pi)$, the set of all real $x$ satisfying $(\cot^{-1}x)^2 - 5\cot^{-1}x + 6 > 0$ is",
  r"$(-\infty, \cot 3) \cup (\cot 2, \infty)$",
  [(r"$(\cot 3, \cot 2)$", r"Solves $(t - 2)(t - 3) < 0$, the region between the roots."),
   (r"$(\cot 2, \infty)$", r"Discards $\cot^{-1}x > 3$, thinking $3$ is outside the range $(0, \pi)$; but $3 < \pi$."),
   (r"$(-\infty, \cot 3] \cup [\cot 2, \infty)$", r"Treats the strict inequality as non-strict, including the endpoints.")],
  r"With $t = \cot^{-1}x \in (0, \pi)$, $(t - 2)(t - 3) > 0$ gives $t < 2$ or $t > 3$, i.e. $t \in (0, 2) \cup (3, \pi)$. Since $\cot^{-1}$ is decreasing, $t < 2 \iff x > \cot 2$ and $t > 3 \iff x < \cot 3$. Hence $x \in (-\infty, \cot 3) \cup (\cot 2, \infty)$.",
  r"Forgetting that $\cot^{-1}$ is decreasing, or that $3 < \pi$ lies in its range.",
  "U14-C-inequality", "Quadratic inequality, range restriction, and inversion of a decreasing function.",
  check=_c047,
  values=[Union(Interval.open(-oo, cot(3)), Interval.open(cot(2), oo)), Interval.open(cot(3), cot(2)),
          Interval.open(cot(2), oo), Union(Interval(-oo, cot(3)), Interval(cot(2), oo))],
  cognitive="Analysis")

# ---------------------------------------------------------------- 048
_P048 = [(Integer(1), Integer(1)), (-Integer(2), Integer(3)), (Rational(5, 2), -Integer(1))]
def _c048():
    out = []
    for (a, b) in _P048:
        th = acos(a/3) + acos(b/4)
        out.append(16*a**2 - 24*a*b*cos(th) + 9*b**2)
    return tuple(out)
def _v048(fn):
    return tuple(fn(acos(a/3) + acos(b/4)) for (a, b) in _P048)
Q("U14-C-048", TOP, "Eliminating inverse functions", "Difficult", "Multi-step computation MCQ",
  r"If $\cos^{-1}\frac{x}{3} + \cos^{-1}\frac{y}{4} = \theta$, then $16x^2 - 24xy\cos\theta + 9y^2$ equals",
  r"$144\sin^2\theta$",
  [(r"$144\cos^2\theta$", r"Reaches $\frac{x^2}{9} + \frac{y^2}{16} - \frac{xy}{6}\cos\theta = 1 - \cos^2\theta$ but writes $1 - \cos^2\theta$ as $\cos^2\theta$, then multiplies by $144$."),
   (r"$144$", r"Drops the $\cos^2\theta$ term after squaring, leaving $\frac{x^2}{9} + \frac{y^2}{16} - \frac{xy}{6}\cos\theta = 1$, then multiplies by $144$."),
   (r"$12\sin^2\theta$", r"Obtains $\frac{x^2}{9} + \frac{y^2}{16} - \frac{xy}{6}\cos\theta = \sin^2\theta$ but clears denominators by multiplying by $3 \cdot 4 = 12$ instead of $9 \cdot 16 = 144$.")],
  r"Let $a = \frac{x}{3}$, $b = \frac{y}{4}$. Taking cosines, $ab - \sqrt{1 - a^2}\sqrt{1 - b^2} = \cos\theta$, so $(ab - \cos\theta)^2 = (1 - a^2)(1 - b^2)$. Expanding, $a^2 + b^2 - 2ab\cos\theta = 1 - \cos^2\theta = \sin^2\theta$. Multiplying $\frac{x^2}{9} + \frac{y^2}{16} - \frac{xy}{6}\cos\theta = \sin^2\theta$ by $144$ gives $16x^2 - 24xy\cos\theta + 9y^2 = 144\sin^2\theta$.",
  r"Algebra slips while squaring to remove radicals.",
  "U14-C-cos-sum-elimination", "Addition formula, isolating and squaring a radical, then scaling.",
  check=_c048,
  values=[_v048(lambda th: 144*sin(th)**2), _v048(lambda th: 144*cos(th)**2), _v048(lambda th: Integer(144)),
          _v048(lambda th: 12*sin(th)**2)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 049
def _c049():
    lhs = asin(x) + asin(2*x) - pi/3
    # sin(sin^{-1} 2x) = sin(pi/3 - sin^{-1} x)
    eq = expand_trig(2*x - sin(pi/3 - asin(x)))
    eq = simplify(eq)
    # isolate the radical and square: 2x + x/2 = (sqrt3/2) sqrt(1-x^2)
    poly = expand((2*x + x/2)**2 - Rational(3, 4)*(1 - x**2))
    assert simplify(eq - (2*x + x/2 - sqrt(3)/2*sqrt(1 - x**2))) == 0
    sols = real_roots_filtered(poly, lhs, x)
    assert len(sols) == 1
    return list(sols)[0]**2
Q("U14-C-049", TOP, "Equation in sin^-1", "Difficult", "Multi-step computation MCQ",
  r"If $x$ is the real number satisfying $\sin^{-1}x + \sin^{-1}(2x) = \frac{\pi}{3}$, then $x^2$ equals",
  r"$\frac{3}{28}$",
  [(r"$\frac{1}{4}$", r"Sign slip in $\sin\left(\frac{\pi}{3} - \theta\right)$, writing $2x = \frac{\sqrt{3}}{2}\sqrt{1-x^2} + \frac{x}{2}$, so $12x^2 = 3$."),
   (r"$\frac{3}{19}$", r"Drops the $-\frac{x}{2}$ term, writing $2x = \frac{\sqrt{3}}{2}\sqrt{1-x^2}$, so $19x^2 = 3$."),
   (r"$\frac{3}{25}$", r"Squares $\frac{5x}{2} = \frac{\sqrt{3}}{2}\sqrt{1-x^2}$ but forgets the $-3x^2$ on the right, writing $25x^2 = 3$.")],
  r"Let $\theta = \sin^{-1}x$. Then $2x = \sin\left(\frac{\pi}{3} - \theta\right) = \frac{\sqrt{3}}{2}\sqrt{1 - x^2} - \frac{x}{2}$, so $\frac{5x}{2} = \frac{\sqrt{3}}{2}\sqrt{1 - x^2}$, which forces $x > 0$. Squaring, $25x^2 = 3 - 3x^2$, so $x^2 = \frac{3}{28}$. The left side is increasing in $x$, so this positive root is the unique solution.",
  r"Sign errors in the compound-angle expansion before squaring.",
  "U14-C-sin-equation-sum", "Compound angle, isolating a radical, squaring and a sign argument.",
  check=_c049, values=[Rational(3, 28), Rational(1, 4), Rational(3, 19), Rational(3, 25)],
  numerical=dict(question=r"If $x$ is the real number satisfying $\sin^{-1}x + \sin^{-1}(2x) = \frac{\pi}{3}$, then the value of $28x^2$ is", answer=3),
  cognitive="Analysis")

# ---------------------------------------------------------------- 050
def _c050():
    a = (x - 2)/(x - 3)
    b = (x + 2)/(x + 3)
    poly = numer(together((a + b) - (1 - a*b)))
    sols = real_roots_filtered(poly, atan(a) + atan(b) - pi/4, x)
    return sum(s**2 for s in sols)
Q("U14-C-050", TOP, "Equation in tan^-1 with rational arguments", "Difficult", "Multi-step computation MCQ",
  r"The sum of the squares of all real $x$ satisfying $\tan^{-1}\left(\frac{x - 2}{x - 3}\right) + \tan^{-1}\left(\frac{x + 2}{x + 3}\right) = \frac{\pi}{4}$ is",
  r"$7$",
  [(r"$\frac{7}{2}$", r"Finds $x^2 = \frac{7}{2}$ but counts only one of the two roots $\pm\sqrt{\frac{7}{2}}$."),
   (r"$17$", r"Sign slip in $1 - ab = \frac{-5}{x^2 - 9}$, writing $+5$, so $2x^2 - 12 = 5$ and $x^2 = \frac{17}{2}$ for each root."),
   (r"$1$", r"Expands the numerator as $2x^2 - 6$ instead of $2x^2 - 12$, so $2x^2 - 6 = -5$ and $x^2 = \frac{1}{2}$ for each root.")],
  r"With $a = \frac{x-2}{x-3}$, $b = \frac{x+2}{x+3}$: $a + b = \frac{2x^2 - 12}{x^2 - 9}$ and $1 - ab = \frac{(x^2 - 9) - (x^2 - 4)}{x^2 - 9} = \frac{-5}{x^2 - 9}$. Setting $\frac{a+b}{1-ab} = 1$ gives $2x^2 - 12 = -5$, so $x^2 = \frac{7}{2}$. For $x = \pm\sqrt{3.5}$ one finds $a, b > 0$ and $ab < 1$, so both roots satisfy the original equation. The sum of squares is $\frac{7}{2} + \frac{7}{2} = 7$.",
  r"Losing a root, or a sign, while simplifying the rational expressions.",
  "U14-C-tan-equation-root-check", "Rational algebra, a quadratic, and checking both roots against the $xy < 1$ condition.",
  check=_c050, values=[7, Rational(7, 2), 17, 1],
  numerical=dict(question=r"The sum of the squares of all real $x$ satisfying $\tan^{-1}\left(\frac{x - 2}{x - 3}\right) + \tan^{-1}\left(\frac{x + 2}{x + 3}\right) = \frac{\pi}{4}$ is", answer=7),
  cognitive="Analysis")
