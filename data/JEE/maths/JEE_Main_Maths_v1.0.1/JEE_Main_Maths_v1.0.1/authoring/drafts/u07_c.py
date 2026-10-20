import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x', real=True)
n = Symbol('n', positive=True, integer=True)
a_, b_, c_, k_, p_, q_ = symbols('a b c k p q', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_CP = "Continuity at a point"
TOP_PW = "Piecewise functions with parameters"
TOP_GM = "Greatest integer, signum and modulus functions"
TOP_CNT = "Counting points of discontinuity and non-differentiability"
TOP_DF = "Differentiability"

GIF = r"where $[t]$ denotes the greatest integer less than or equal to $t$"

# ---------------------------------------------------------------- numeric helpers
_H = Rational(1, 10**30)
_P = 80


def _v(f, a):
    return N(f.subs(x, a), _P)


def _s(f, a, sg):
    return N(f.subs(x, a + sg * _H), _P)


def _cont(f, a):
    fa = _v(f, a)
    return bool(abs(_s(f, a, -1) - fa) < 1e-12 and abs(_s(f, a, 1) - fa) < 1e-12)


def _rd(f, a):
    return (_s(f, a, 1) - _v(f, a)) / _H


def _ld(f, a):
    return (_v(f, a) - _s(f, a, -1)) / _H


def _diff(f, a):
    return _cont(f, a) and bool(abs(_rd(f, a) - _ld(f, a)) < 1e-9)


def _disc_pts(f, cands):
    return [c for c in cands if not _cont(f, c)]


def _nondiff_pts(f, cands):
    return [c for c in cands if not _diff(f, c)]


def _roots_in(e, lo, hi):
    return list(solveset(e, x, Interval.open(lo, hi)))


def _ints_in(lo, hi):
    return [Integer(m) for m in range(int(floor(lo)) - 1, int(ceiling(hi)) + 2) if lo < m < hi]


def _sym(s):
    return Symbol(s)


# ================================================================ EASY
# ---------------------------------------------------------------- 001
def _c001():
    f = (x**3 - x**2 - 8*x + 12) / (x - 2)**2
    return solve(Eq(k_, limit(f, x, 2)), k_)[0]
q("U07-C-001", TOP_CP, "Removable discontinuity with a squared factor in the denominator", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \frac{x^3 - x^2 - 8x + 12}{(x - 2)^2}$ for $x \ne 2$ and $f(2) = k$. If $f$ is continuous at $x = 2$, then $k$ equals",
  r"$5$",
  [(r"$0$", r"Cancels only one factor $x - 2$, writing $f(x) = \frac{x^2 + x - 6}{x - 2}$, then puts $x = 2$ in the numerator $x^2 + x - 6$ alone, getting $0$."),
   (r"$2$", r"Keeps only the leading terms, $\frac{x^3}{x^2} = x$, and puts $x = 2$."),
   (r"$-1$", r"Matches the constant term with the wrong sign, taking the cofactor of $(x - 2)^2$ as $x - 3$, so $k = 2 - 3 = -1$.")],
  r"The numerator vanishes at $x = 2$, and dividing by $x - 2$ gives $x^3 - x^2 - 8x + 12 = (x - 2)(x^2 + x - 6) = (x - 2)^2(x + 3)$. So for $x \ne 2$, $f(x) = x + 3 \to 5$, and continuity at $2$ needs $k = 5$.",
  r"Cancelling a repeated factor only once, or assuming a squared factor in the denominator always gives an infinite discontinuity.",
  "U07-C-removable-double-factor", "One factorisation that must spot the double factor $(x - 2)^2$, then one substitution.",
  check=_c001, values=[5, 0, 2, -1], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = \frac{x^3 - x^2 - 8x + 12}{(x - 2)^2}$ for $x \ne 2$ and $f(2) = k$. If $f$ is continuous at $x = 2$, then the value of $k$ is", answer=5))


# ---------------------------------------------------------------- 002
def _c002():
    f = sin(2*x) / x + x*sin(1/x)
    return solve(Eq(k_, limit(f, x, 0)), k_)[0]
q("U07-C-002", TOP_CP, "Value for continuity with a bounded oscillating factor", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \frac{\sin 2x}{x} + x \sin\frac{1}{x}$ for $x \ne 0$ and $f(0) = k$. If $f$ is continuous at $x = 0$, then $k$ equals",
  r"$2$",
  [(r"$3$", r"Rewrites $x \sin\frac{1}{x}$ as $\frac{\sin(1/x)}{1/x}$ and applies $\frac{\sin \theta}{\theta} \to 1$, although here $\theta = \frac{1}{x} \to \infty$; this gives $2 + 1 = 3$."),
   (r"$1$", r"Uses $\frac{\sin 2x}{x} \to 1$, ignoring the coefficient $2$, and correctly takes $x \sin\frac{1}{x} \to 0$, giving $1 + 0 = 1$."),
   (r"$\frac{1}{2}$", r"Inverts the coefficient, taking $\frac{\sin 2x}{x} \to \frac{1}{2}$, and correctly takes $x \sin\frac{1}{x} \to 0$, giving $\frac{1}{2}$.")],
  r"$\frac{\sin 2x}{x} = 2 \cdot \frac{\sin 2x}{2x} \to 2$. Since $\left|x \sin\frac{1}{x}\right| \le |x|$ and $|x| \to 0$, the sandwich theorem gives $x \sin\frac{1}{x} \to 0$. So $\lim_{x \to 0} f(x) = 2 + 0 = 2$, and continuity at $0$ needs $k = 2$.",
  r"Treating $x \sin\frac{1}{x}$ as a standard $\frac{\sin \theta}{\theta}$ limit, or dropping the coefficient in $\frac{\sin 2x}{x}$.",
  "U07-C-squeeze-removable", "Two short limits: one standard limit and one sandwich bound.",
  check=_c002, values=[2, 3, 1, Rational(1, 2)], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 003
def _c003():
    L = (k_*x + 1).subs(x, 3)
    R = limit(x**2 - k_, x, 3, '+')
    return solve(Eq(L, R), k_)[0]
q("U07-C-003", TOP_PW, "One parameter for continuity at a join", "Easy", "Inverse/parameter MCQ",
  r"Let $f(x) = kx + 1$ for $x \le 3$ and $f(x) = x^2 - k$ for $x > 3$. If $f$ is continuous at $x = 3$, then $k$ equals",
  r"$2$",
  [(r"$\frac{8}{3}$", r"Drops $-k$ from the right piece and solves $3k + 1 = 9$."),
   (r"$4$", r"Takes the right-hand value as $9 + k$ (sign slip), so $3k + 1 = 9 + k$ gives $k = 4$."),
   (r"$\frac{5}{2}$", r"Moves the $1$ across with the wrong sign: $4k = 9 + 1 = 10$, so $k = \frac{5}{2}$.")],
  r"The left value at $3$ is $f(3) = 3k + 1$ and the right-hand limit is $9 - k$. Continuity needs $3k + 1 = 9 - k$, so $4k = 8$ and $k = 2$.",
  "Sign slips while equating the one-sided values.",
  "U07-C-piecewise-one-param", "One equation in one unknown.",
  check=_c003, values=[2, Rational(8, 3), 4, Rational(5, 2)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = kx + 1$ for $x \le 3$ and $f(x) = x^2 - k$ for $x > 3$. If $f$ is continuous at $x = 3$, then the value of $k$ is", answer=2))


# ---------------------------------------------------------------- 004
def _c004():
    f = floor(2*x)
    cands = sorted(set(_roots_in(sin(pi*2*x), 0, 2)))  # 2x integer
    return len(_disc_pts(f, cands))
q("U07-C-004", TOP_CNT, "Discontinuities of [2x] on an open interval", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = [2x]$, " + GIF + r". The number of points in the interval $(0, 2)$ at which $f$ is discontinuous is",
  r"$3$",
  [(r"$1$", r"Treats $[2x]$ like $[x]$ and counts only the integer $x = 1$."),
   (r"$4$", r"Also counts the endpoint $x = 2$, which is not in the open interval."),
   (r"$2$", r"Counts only $x = \frac{1}{2}$ and $x = \frac{3}{2}$, thinking the jump at $x = 1$ is absent because $1$ is an integer.")],
  r"$[2x]$ jumps exactly where $2x$ is an integer. In $(0, 2)$ we have $2x \in (0, 4)$, so $2x = 1, 2, 3$, that is $x = \frac{1}{2}, 1, \frac{3}{2}$. Hence $3$ points.",
  r"Assuming $[kx]$ jumps only at integers.",
  "U07-C-gif-count", "One idea: locate where the inner expression is an integer.",
  check=_c004, values=[3, 1, 4, 2], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [2x]$, " + GIF + r". The number of points in the interval $(0, 2)$ at which $f$ is discontinuous is", answer=3))


# ---------------------------------------------------------------- 005
def _c005():
    f = Abs(x - 2) + Abs(x + 1)
    cands = solve(x - 2, x) + solve(x + 1, x)
    return FiniteSet(*_nondiff_pts(f, cands))
q("U07-C-005", TOP_GM, "Corners of a sum of moduli", "Easy", "Single-step computation MCQ",
  r"The set of all points at which $f(x) = |x - 2| + |x + 1|$ is not differentiable is",
  r"$\{-1, 2\}$",
  [(r"$\{-2, 1\}$", r"Takes the zeros of $x - 2$ and $x + 1$ with the wrong signs."),
   (r"$\{-1, \frac{1}{2}, 2\}$", r"Adds $x = \frac{1}{2}$, where $|x - 2| = |x + 1|$, as an extra corner."),
   (r"$\{2\}$", r"Notices only the corner of the first modulus.")],
  r"Each $|x - c|$ has a corner only at $x = c$, and a sum of a corner with a smooth function is still a corner. So $f$ fails to be differentiable exactly at $x = 2$ and $x = -1$ (slopes jump from $-2$ to $0$ at $-1$, and from $0$ to $2$ at $2$).",
  "Solving the zeros of the moduli with the wrong sign.",
  "U07-C-mod-sum-nondiff", "Read off two corners.",
  check=_c005, values=[FiniteSet(-1, 2), FiniteSet(-2, 1), FiniteSet(-1, Rational(1, 2), 2), FiniteSet(2)],
  cognitive="Understanding", source_class="XII")


# ---------------------------------------------------------------- 006
def _c006():
    return diff(x*Abs(x), x).subs(x, -3)
q("U07-C-006", TOP_DF, "Derivative of x|x|", "Easy", "Single-step computation MCQ",
  r"If $f(x) = x|x|$, then $f'(-3)$ equals",
  r"$6$",
  [(r"$-6$", r"Treats $x|x|$ as $x^2$ for all $x$ and uses $f'(x) = 2x$."),
   (r"$0$", r"Uses the product rule with the derivative of $|x|$ taken as $+1$: $|x| + x = 3 - 3 = 0$."),
   (r"$3$", r"Differentiates only the factor $x$ and reports $|x| = 3$.")],
  r"For $x < 0$, $f(x) = x(-x) = -x^2$, so $f'(x) = -2x$ and $f'(-3) = 6$. Equivalently $f'(x) = 2|x|$ for all real $x$.",
  r"Ignoring that $|x| = -x$ for $x < 0$.",
  "U07-C-x-mod-x", "One case split and one derivative.",
  check=_c006, values=[6, -6, 0, 3], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 007
def _c007():
    f = (x**2 - 4) / (x**2 - 3*x + 2)
    res = []
    for c in (1, 2):
        L1, L2 = limit(f, x, c, '-'), limit(f, x, c, '+')
        res.append(bool(L1 == L2 and L1.is_finite))
    return tuple(res)
q("U07-C-007", TOP_CP, "Identifying removable discontinuities", "Easy", "Conceptual/application MCQ",
  r"Let $f(x) = \frac{x^2 - 4}{x^2 - 3x + 2}$ for $x \ne 1, 2$. By assigning a suitable value at the point, $f$ can be made continuous at",
  r"$x = 2$ only",
  [(r"$x = 1$ only", r"Mixes up the cancelled factor: $x - 2$ cancels, not $x - 1$."),
   (r"each of $x = 1$ and $x = 2$", r"Assumes every zero of the denominator gives a removable discontinuity."),
   (r"neither $x = 1$ nor $x = 2$", r"Assumes any zero of the denominator gives a non-removable discontinuity.")],
  r"$f(x) = \frac{(x-2)(x+2)}{(x-1)(x-2)} = \frac{x+2}{x-1}$ for $x \ne 1, 2$. As $x \to 2$ the limit is $4$, so defining $f(2) = 4$ removes the discontinuity. As $x \to 1$, $|f(x)| \to \infty$, so no value works at $x = 1$.",
  "Treating every zero of the denominator alike.",
  "U07-C-removable-identify", "One factorisation and one limit check at each point.",
  check=_c007, values=[(False, True), (True, False), (True, True), (False, False)], cognitive="Understanding", source_class="XII")


# ---------------------------------------------------------------- 008
def _c008():
    g = x + floor(-x)
    vals = (_s(g, 3, -1), _s(g, 3, 1), _v(g, 3))
    return tuple(int(round(float(v))) for v in vals)
q("U07-C-008", TOP_GM, "One-sided limits of x + [-x]", "Easy", "Single-step computation MCQ",
  r"Let $g(x) = x + [-x]$, " + GIF + r". Then $\lim_{x \to 3^-} g(x)$, $\lim_{x \to 3^+} g(x)$ and $g(3)$ are respectively",
  r"$0, -1, 0$",
  [(r"$1, 0, 0$", r"Uses $[-x] = -[x]$, so $g(x) = x - [x]$, which tends to $1$ from the left and $0$ from the right, with value $0$ at $x = 3$."),
   (r"$0, 0, 0$", r"Evaluates both one-sided limits by substituting $x = 3$, getting $3 + [-3] = 0$ each time."),
   (r"$0, -1, -1$", r"Finds both limits correctly but applies $[-x] = -[x] - 1$ also at the integer $x = 3$, so $g(3) = 3 - 3 - 1 = -1$.")],
  r"For $2 < x < 3$, $-3 < -x < -2$, so $[-x] = -3$ and $g(x) = x - 3 \to 0$. For $3 < x < 4$, $[-x] = -4$ and $g(x) = x - 4 \to -1$. At $x = 3$, $g(3) = 3 + [-3] = 0$. So the values are $0, -1, 0$; $g$ is continuous from the left but not from the right at $3$.",
  r"Using $[-x] = -[x]$ for non-integers, or $[-x] = -[x] - 1$ at integers.",
  "U07-C-gif-x-plus-neg-gif", "Two one-sided evaluations of $[-x]$ and one value.",
  check=_c008, values=[(0, -1, 0), (1, 0, 0), (0, 0, 0), (0, -1, -1)], cognitive="Understanding", source_class="XII")


# ---------------------------------------------------------------- 009
def _c009():
    f = Abs(x**2 - 4)
    R = limit((f - f.subs(x, 2)) / (x - 2), x, 2, '+')
    L = limit((f - f.subs(x, 2)) / (x - 2), x, 2, '-')
    return R - L
q("U07-C-009", TOP_DF, "One-sided derivatives at a zero of a modulus", "Easy", "Single-step computation MCQ",
  r"For $f(x) = |x^2 - 4|$, the value of $Rf'(2) - Lf'(2)$, the right-hand derivative minus the left-hand derivative at $x = 2$, is",
  r"$8$",
  [(r"$0$", r"Assumes $f$ is differentiable at $x = 2$ because $x^2 - 4$ is a polynomial."),
   (r"$4$", r"Reports only the right-hand derivative $2x = 4$."),
   (r"$-8$", r"Subtracts in the reverse order, left minus right.")],
  r"For $x > 2$ (near $2$), $f = x^2 - 4$, so $Rf'(2) = 4$. For $x < 2$ (near $2$), $f = 4 - x^2$, so $Lf'(2) = -4$. The difference is $8$.",
  "Assuming the modulus of a polynomial is differentiable at its zeros.",
  "U07-C-onesided-derivative", "Two one-sided derivatives.",
  check=_c009, values=[8, 0, 4, -8], cognitive="Application", source_class="XII",
  numerical=dict(question=r"For $f(x) = |x^2 - 4|$, the right-hand derivative of $f$ at $x = 2$ minus the left-hand derivative of $f$ at $x = 2$ is", answer=8))


# ---------------------------------------------------------------- 010
def _c010():
    f = Abs(sin(x))
    cands = _roots_in(sin(x), 0, 3*pi) + _roots_in(cos(x), 0, 3*pi)
    return len(_nondiff_pts(f, cands))
q("U07-C-010", TOP_CNT, "Corners of |sin x| on an interval", "Easy", "Single-step computation MCQ",
  r"The number of points in the interval $(0, 3\pi)$ at which $f(x) = |\sin x|$ is not differentiable is",
  r"$2$",
  [(r"$3$", r"Counts the zeros $0$ or $3\pi$ along with $\pi$ and $2\pi$, but those endpoints are excluded."),
   (r"$4$", r"Counts all four zeros $0, \pi, 2\pi, 3\pi$ including both endpoints."),
   (r"$5$", r"Adds the three peaks at $x = \frac{\pi}{2}, \frac{3\pi}{2}, \frac{5\pi}{2}$ to the zeros $\pi, 2\pi$.")],
  r"$|\sin x|$ has a corner exactly where $\sin x$ changes sign, that is at its simple zeros. In $(0, 3\pi)$ these are $x = \pi$ and $x = 2\pi$; at the peaks the graph is smooth. Hence $2$ points.",
  "Counting the endpoints of an open interval, or treating peaks as corners.",
  "U07-C-mod-trig-count", "Locate zeros of $\\sin x$ inside an open interval.",
  check=_c010, values=[2, 3, 4, 5], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The number of points in the open interval $(0, 3\pi)$ at which $f(x) = |\sin x|$ is not differentiable is", answer=2))


# ---------------------------------------------------------------- 011
def _c011():
    f = x*floor(x)
    return _s(f, 3, 1) - _s(f, 3, -1)
q("U07-C-011", TOP_GM, "Jump of x[x] at an integer", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = x[x]$, " + GIF + r". Then $\lim_{x \to 3^+} f(x) - \lim_{x \to 3^-} f(x)$ equals",
  r"$3$",
  [(r"$1$", r"Reports the jump of $[x]$ alone and forgets the factor $x$."),
   (r"$0$", r"Assumes $f$ is continuous at $x = 3$ because $x$ is continuous."),
   (r"$-3$", r"Subtracts in the reverse order, left limit minus right limit.")],
  r"As $x \to 3^+$, $[x] = 3$ and $f \to 9$. As $x \to 3^-$, $[x] = 2$ and $f \to 6$. The difference is $9 - 6 = 3$.",
  "Forgetting that the jump of $[x]$ is scaled by the factor $x$.",
  "U07-C-gif-jump", "Two one-sided limits.",
  check=_c011, values=[3, 1, 0, -3], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = x[x]$, " + GIF + r". The value of $\lim_{x \to 3^+} f(x) - \lim_{x \to 3^-} f(x)$ is", answer=3))


# ---------------------------------------------------------------- 012
def _c012():
    f = (exp(4*x) - 1) / (2*x)
    return limit(f, x, 0)
q("U07-C-012", TOP_CP, "Value at a point for continuity (exponential quotient)", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \frac{e^{4x} - 1}{2x}$ for $x \ne 0$. If $f$ is continuous at $x = 0$, then $f(0)$ equals",
  r"$2$",
  [(r"$4$", r"Uses $\frac{e^{4x}-1}{x} \to 4$ but forgets the $2$ in the denominator."),
   (r"$\frac{1}{2}$", r"Inverts the ratio and takes $\frac{2}{4}$."),
   (r"$1$", r"Uses $\frac{e^{\theta}-1}{\theta} \to 1$ without matching the argument $4x$ with the denominator.")],
  r"$\frac{e^{4x}-1}{2x} = 2 \cdot \frac{e^{4x}-1}{4x} \to 2 \cdot 1 = 2$. Hence $f(0) = 2$.",
  r"Not matching the argument of $e^{\theta} - 1$ with the denominator.",
  "U07-C-exp-removable", "One standard limit.",
  check=_c012, values=[2, 4, Rational(1, 2), 1], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 013
def _c013():
    L = limit(cos(x) / (pi - 2*x), x, pi/2)
    return solve(Eq(k_*L, 3), k_)[0]
q("U07-C-013", TOP_PW, "Parameter in a trigonometric quotient", "Easy", "Inverse/parameter MCQ",
  r"Let $f(x) = \frac{k \cos x}{\pi - 2x}$ for $x \ne \frac{\pi}{2}$ and $f\left(\frac{\pi}{2}\right) = 3$. If $f$ is continuous at $x = \frac{\pi}{2}$, then $k$ equals",
  r"$6$",
  [(r"$\frac{3}{2}$", r"Takes the limit of $\frac{\cos x}{\pi - 2x}$ as $2$ instead of $\frac{1}{2}$, so $2k = 3$."),
   (r"$3$", r"Takes $\frac{\cos x}{\pi - 2x} \to 1$, ignoring the factor $2$ in $\pi - 2x$."),
   (r"$-6$", r"Takes the limit as $-\frac{1}{2}$ through a sign slip in $\cos x = \sin\left(\frac{\pi}{2} - x\right)$.")],
  r"Put $x = \frac{\pi}{2} - h$: $\frac{\cos x}{\pi - 2x} = \frac{\sin h}{2h} \to \frac{1}{2}$. Continuity needs $\frac{k}{2} = 3$, so $k = 6$.",
  r"Losing the factor $2$ when substituting $x = \frac{\pi}{2} - h$.",
  "U07-C-trig-removable", "One substitution and one standard limit.",
  check=_c013, values=[6, Rational(3, 2), 3, -6], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = \frac{k \cos x}{\pi - 2x}$ for $x \ne \frac{\pi}{2}$ and $f\left(\frac{\pi}{2}\right) = 3$. If $f$ is continuous at $x = \frac{\pi}{2}$, then the value of $k$ is", answer=6))


# ---------------------------------------------------------------- 014
def _c014():
    f1 = (x - 1)*Abs(x - 1)
    f2 = Abs(x - 1) + (x - 1)
    return (_diff(f1, 1), _diff(f2, 1))
q("U07-C-014", TOP_DF, "Differentiability of products and sums with |x - 1|", "Easy", "Statement-based MCQ",
  r"Statement I: $f(x) = (x - 1)|x - 1|$ is differentiable at $x = 1$. Statement II: $g(x) = |x - 1| + (x - 1)$ is differentiable at $x = 1$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Thinks adding the smooth term $x - 1$ removes the corner of $|x - 1|$."),
   (ST_FF, r"Thinks any function containing $|x - 1|$ has a corner at $x = 1$."),
   (ST_FT, r"Reverses the two cases, believing the sum smooths the corner while the product does not.")],
  r"For $f$: $\frac{f(1+h) - f(1)}{h} = |h| \to 0$ from both sides, so $f'(1) = 0$ and Statement I is true. For $g$: $g = 2(x-1)$ for $x > 1$ and $g = 0$ for $x < 1$, so the one-sided derivatives are $2$ and $0$; Statement II is false.",
  r"Believing that every expression involving $|x - a|$ has a corner at $a$.",
  "U07-C-stmt-product-sum", "Two short one-sided derivative checks.",
  check=_c014, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding", source_class="XII")


# ---------------------------------------------------------------- 015
def _c015():
    f = sign(x**2 - 3*x + 2)
    cands = _roots_in(x**2 - 3*x + 2, -oo, oo) + [Rational(3, 2)]
    return len(_disc_pts(f, cands))
q("U07-C-015", TOP_GM, "Discontinuities of a signum composite", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \operatorname{sgn}(x^2 - 3x + 2)$, where $\operatorname{sgn}$ is the signum function. The number of points of discontinuity of $f$ on $\mathbb{R}$ is",
  r"$2$",
  [(r"$0$", r"Assumes the signum of a continuous function is continuous."),
   (r"$1$", r"Counts only the point $x = 1$ where the quadratic turns from positive to negative."),
   (r"$3$", r"Adds the vertex $x = \frac{3}{2}$ to the two zeros.")],
  r"$x^2 - 3x + 2 = (x-1)(x-2)$ changes sign at $x = 1$ and $x = 2$. At each of these $f$ jumps between $1$ and $-1$ (with value $0$ at the point), and elsewhere $f$ is locally constant. Hence $2$ points.",
  "Assuming signum preserves continuity.",
  "U07-C-signum-disc", "Find the sign changes of a quadratic.",
  check=_c015, values=[2, 0, 1, 3], cognitive="Understanding", source_class="XII")


# ---------------------------------------------------------------- 016
def _c016():
    f = (x**2 - 9) / Abs(x - 3)
    return limit(f, x, 3, '+') - limit(f, x, 3, '-')
q("U07-C-016", TOP_GM, "Size of a jump with a modulus denominator", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \frac{x^2 - 9}{|x - 3|}$ for $x \ne 3$. Then $\lim_{x \to 3^+} f(x) - \lim_{x \to 3^-} f(x)$ equals",
  r"$12$",
  [(r"$0$", r"Cancels $|x - 3|$ as if it were $x - 3$ on both sides, giving $6 - 6$."),
   (r"$-12$", r"Subtracts in the reverse order."),
   (r"$6$", r"Reports only the right-hand limit $x + 3 \to 6$.")],
  r"For $x > 3$, $f = x + 3 \to 6$. For $x < 3$, $|x - 3| = 3 - x$, so $f = -(x + 3) \to -6$. The difference is $12$.",
  r"Replacing $|x - 3|$ by $x - 3$ on both sides.",
  "U07-C-jump-size", "Two one-sided limits after cancelling.",
  check=_c016, values=[12, 0, -12, 6], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 017
def _c017():
    f = Min(x, x**2)
    cands = solve(Eq(x, x**2), x)
    return FiniteSet(*_nondiff_pts(f, cands))
q("U07-C-017", TOP_DF, "Corners of a minimum function", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \min\{x, x^2\}$ for $x \in \mathbb{R}$. The set of points at which $f$ is not differentiable is",
  r"$\{0, 1\}$",
  [(r"$\{1\}$", r"Thinks the two graphs meet tangentially at the origin, so misses the corner at $x = 0$."),
   (r"$\{0\}$", r"Misses the switch from $x^2$ to $x$ at $x = 1$."),
   (r"$\{-1, 0, 1\}$", r"Solves $x^2 = |x|$ instead of $x^2 = x$, adding $x = -1$.")],
  r"$x^2 \le x$ exactly on $[0, 1]$, so $f = x$ for $x < 0$, $f = x^2$ on $[0, 1]$, $f = x$ for $x > 1$. At $0$ the slopes are $1$ and $0$; at $1$ they are $2$ and $1$. So $f$ is not differentiable at $0$ and $1$ only.",
  "Missing a corner where the two curves cross at the origin.",
  "U07-C-minmax-nondiff", "Find crossings and compare slopes.",
  check=_c017, values=[FiniteSet(0, 1), FiniteSet(1), FiniteSet(0), FiniteSet(-1, 0, 1)],
  cognitive="Application", source_class="XII")


# ================================================================ MEDIUM
# ---------------------------------------------------------------- 018
def _c018():
    inner = solve(denom(1/x), x)
    outer = solve(Eq(1 + 1/x, 0), x)
    return FiniteSet(*(inner + outer))
q("U07-C-018", TOP_CP, "Problem points of a composite rational function", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \frac{1}{1 + \frac{1}{x}}$. The set of all real $x$ at which $f$ is either undefined or discontinuous is",
  r"$\{-1, 0\}$",
  [(r"$\{-1\}$", r"Simplifies to $\frac{x}{x+1}$ first and forgets that the original expression needs $x \ne 0$."),
   (r"$\{0\}$", r"Looks only at the inner fraction $\frac{1}{x}$."),
   (r"$\{0, 1\}$", r"Solves $1 + \frac{1}{x} = 0$ with a sign slip, getting $x = 1$.")],
  r"The inner $\frac{1}{x}$ needs $x \ne 0$, and the outer reciprocal needs $1 + \frac{1}{x} \ne 0$, i.e. $x \ne -1$. Elsewhere $f(x) = \frac{x}{x+1}$ is continuous. So the problem points are $x = 0$ and $x = -1$.",
  "Simplifying a composite expression before reading off its domain.",
  "U07-C-composite-disc", "Two layers of the composite must be checked; simplification trap.",
  check=_c018, values=[FiniteSet(-1, 0), FiniteSet(-1), FiniteSet(0), FiniteSet(0, 1)],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 019
def _c019():
    f = floor(x**2)
    cands = []
    for m in range(1, 4):
        cands += _roots_in(x**2 - m, 0, 2)
    return len(_disc_pts(f, cands))
q("U07-C-019", TOP_CNT, "Discontinuities of [x^2]", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = [x^2]$, " + GIF + r". The number of points in the interval $(0, 2)$ at which $f$ is discontinuous is",
  r"$3$",
  [(r"$1$", r"Checks only the integer $x = 1$, as if $[x^2]$ jumped only at integers."),
   (r"$4$", r"Also counts $x = 2$, which is outside the open interval."),
   (r"$2$", r"Counts only the irrational points $\sqrt{2}$ and $\sqrt{3}$.")],
  r"$[x^2]$ jumps where $x^2$ crosses an integer. For $x \in (0, 2)$, $x^2 \in (0, 4)$, so $x^2 = 1, 2, 3$, i.e. $x = 1, \sqrt{2}, \sqrt{3}$. Each is a jump, so $3$ points.",
  r"Looking for jumps of $[g(x)]$ only at integer $x$.",
  "U07-C-gif-count", "Convert to where $x^2$ is an integer, then restrict to the interval.",
  check=_c019, values=[3, 1, 4, 2], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x^2]$, " + GIF + r". The number of points in the open interval $(0, 2)$ at which $f$ is discontinuous is", answer=3))


# ---------------------------------------------------------------- 020
def _c020():
    left = (a_*x + 2*b_).subs(x, 1)
    right = (2*a_*x**2 - b_).subs(x, 1)
    s = solve([Eq(left, 5), Eq(right, 5)], [a_, b_], dict=True)[0]
    return s[a_] - s[b_]
q("U07-C-020", TOP_PW, "Two parameters for continuity at a point", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = ax + 2b$ for $x < 1$, $f(1) = 5$, and $f(x) = 2ax^2 - b$ for $x > 1$. If $f$ is continuous at $x = 1$, then $a - b$ equals",
  r"$2$",
  [(r"$0$", r"Reads the right piece at $x = 1$ as $2a + b$ (sign slip), so $a + 2b = 5$ and $2a + b = 5$ give $a = b$."),
   (r"$\frac{5}{3}$", r"Drops the $2$ in the left piece: $a + b = 5$ and $2a - b = 5$ give $a = \frac{10}{3}$, $b = \frac{5}{3}$."),
   (r"$5$", r"Drops the $2$ in the right piece: $a + 2b = 5$ and $a - b = 5$ give $a = 5$, $b = 0$.")],
  r"Continuity needs both one-sided limits to equal $f(1) = 5$: $a + 2b = 5$ and $2a - b = 5$. Doubling the second and adding gives $5a = 15$, so $a = 3$, $b = 1$ and $a - b = 2$.",
  "Sign or coefficient slips when evaluating the pieces at the join.",
  "U07-C-piecewise-two-param", "Set up and solve a two-variable linear system.",
  check=_c020, values=[2, 0, Rational(5, 3), 5], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = ax + 2b$ for $x < 1$, $f(1) = 5$, and $f(x) = 2ax^2 - b$ for $x > 1$. If $f$ is continuous at $x = 1$, then the value of $a - b$ is", answer=2))


# ---------------------------------------------------------------- 021
def _c021():
    L = a_*x**2 + b_
    R = 1/Abs(x)
    eqs = [Eq(L.subs(x, 1), R.subs(x, 1)), Eq(diff(L, x).subs(x, 1), diff(R, x).subs(x, 1))]
    s = solve(eqs, [a_, b_], dict=True)[0]
    return s[b_] - s[a_]
q("U07-C-021", TOP_PW, "Parameters for differentiability at a join", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = ax^2 + b$ for $x < 1$ and $f(x) = \frac{1}{|x|}$ for $x \ge 1$. If $f$ is differentiable at $x = 1$, then $b - a$ equals",
  r"$2$",
  [(r"$0$", r"Takes the derivative of $\frac{1}{x}$ as $+\frac{1}{x^2}$, so $2a = 1$ and $a = b = \frac{1}{2}$."),
   (r"$3$", r"Differentiates $ax^2$ as $a$, so $a = -1$ and $b = 2$."),
   (r"$5$", r"Keeps the constant in the derivative, writing $2a + b = -1$, which with $a + b = 1$ gives $a = -2$, $b = 3$.")],
  r"Near $x = 1$ the right piece is $\frac{1}{x}$, with value $1$ and derivative $-1$. Continuity: $a + b = 1$. Equal derivatives: $2a = -1$, so $a = -\frac{1}{2}$ and $b = \frac{3}{2}$. Hence $b - a = 2$.",
  r"Sign error in the derivative of $\frac{1}{x}$.",
  "U07-C-diff-params", "Two conditions (continuity and equal slopes) combined.",
  check=_c021, values=[2, 0, 3, 5], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = ax^2 + b$ for $x < 1$ and $f(x) = \frac{1}{|x|}$ for $x \ge 1$. If $f$ is differentiable at $x = 1$, then the value of $b - a$ is", answer=2))


# ---------------------------------------------------------------- 022
def _c022():
    L = x**3 - 2*x
    R = a_*x + b_
    s = solve([Eq(L.subs(x, 2), R.subs(x, 2)), Eq(diff(L, x).subs(x, 2), diff(R, x))], [a_, b_], dict=True)[0]
    return s[a_] + s[b_]
q("U07-C-022", TOP_PW, "Line joining a cubic smoothly", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = x^3 - 2x$ for $x \le 2$ and $f(x) = ax + b$ for $x > 2$. If $f$ is differentiable at $x = 2$, then $a + b$ equals",
  r"$-6$",
  [(r"$-8$", r"Drops the $-2$ in the derivative, taking $a = 12$ and then $b = 4 - 24 = -20$."),
   (r"$-2$", r"Uses $f(2) = 8$ (forgetting $-2x$) with the correct $a = 10$, so $b = -12$."),
   (r"$4$", r"Finds $a = 10$ but writes $b = f(2) - a = -6$, forgetting to multiply $a$ by $2$.")],
  r"Differentiability needs continuity, $2a + b = f(2) = 8 - 4 = 4$, and equal slopes, $a = f'(2) = 3(4) - 2 = 10$. So $b = 4 - 20 = -16$ and $a + b = -6$.",
  "Slips in evaluating the value or the slope of the cubic at the join.",
  "U07-C-diff-params", "Two conditions solved in sequence.",
  check=_c022, values=[-6, -8, -2, 4], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 023
def _c023():
    g = x**2 + k_*x + 3
    f = Abs(x - 2)*g
    # one-sided derivatives at 2
    R = limit((((x - 2)*g) - 0) / (x - 2), x, 2)
    L = limit((((2 - x)*g) - 0) / (x - 2), x, 2)
    return solve(Eq(R, L), k_)[0]
q("U07-C-023", TOP_DF, "Making |x - 2| g(x) differentiable", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = |x - 2|\,(x^2 + kx + 3)$. If $f$ is differentiable at $x = 2$, then $k$ equals",
  r"$-\frac{7}{2}$",
  [(r"$\frac{7}{2}$", r"Solves $4 + 2k + 3 = 0$ with a sign slip."),
   (r"$-4$", r"Sets the derivative of the quadratic factor to zero at $x = 2$: $4 + k = 0$."),
   (r"$-7$", r"Evaluates $kx$ at $x = 2$ as $k$, solving $4 + k + 3 = 0$.")],
  r"Write $g(x) = x^2 + kx + 3$. Then $Rf'(2) = g(2)$ and $Lf'(2) = -g(2)$, so $f$ is differentiable at $2$ exactly when $g(2) = 0$: $4 + 2k + 3 = 0$, giving $k = -\frac{7}{2}$.",
  r"Requiring $g'(a) = 0$ instead of $g(a) = 0$ for $|x - a| g(x)$.",
  "U07-C-abs-times-g", r"Uses the $|x-a|g(x)$ criterion plus one equation.",
  check=_c023, values=[Rational(-7, 2), Rational(7, 2), -4, -7], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 024
def _c024():
    f = Abs(x**2 - 3*Abs(x) + 2)
    cands = [Integer(0)] + _roots_in(x**2 - 3*Abs(x) + 2, -oo, oo)
    return len(_nondiff_pts(f, cands))
q("U07-C-024", TOP_CNT, "Nested modulus with |x| inside", "Medium", "Multi-step computation MCQ",
  r"The number of points at which $f(x) = \left|x^2 - 3|x| + 2\right|$ is not differentiable is",
  r"$5$",
  [(r"$4$", r"Finds the zeros $x = \pm 1, \pm 2$ but misses the corner at $x = 0$ from the inner $|x|$."),
   (r"$3$", r"Works only with $x \ge 0$ and counts $x = 0, 1, 2$."),
   (r"$2$", r"Solves $x^2 - 3x + 2 = 0$ and counts only $x = 1, 2$.")],
  r"The inner expression $x^2 - 3|x| + 2 = (|x|-1)(|x|-2)$ vanishes at $x = \pm1, \pm2$, all simple sign changes, giving $4$ corners. Near $x = 0$ the expression is close to $2 > 0$, so $f = x^2 - 3|x| + 2$ has slopes $3$ and $-3$ there, another corner. Total $5$.",
  r"Forgetting the corner contributed by the inner $|x|$ at $x = 0$.",
  "U07-C-nested-mod-count", "Even function, sign analysis, plus the inner corner.",
  check=_c024, values=[5, 4, 3, 2], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of points in $\mathbb{R}$ at which $f(x) = \left|x^2 - 3|x| + 2\right|$ is not differentiable is", answer=5))


# ---------------------------------------------------------------- 025
def _c025():
    f = floor(x)*sin(pi*x)
    return len(_nondiff_pts(f, _ints_in(-1, 3)))
q("U07-C-025", TOP_CNT, "Non-differentiability of [x] sin(pi x)", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = [x]\sin(\pi x)$, " + GIF + r". The number of points in the interval $(-1, 3)$ at which $f$ is not differentiable is",
  r"$3$",
  [(r"$0$", r"Thinks the factor $\sin(\pi x)$, which vanishes at every integer, removes the effect of $[x]$ completely."),
   (r"$4$", r"Includes the endpoint $x = -1$."),
   (r"$2$", r"Skips $x = 0$, thinking $[x] = 0$ there makes $f$ smooth.")],
  r"$f$ is continuous everywhere since $\sin(n\pi) = 0$. At an integer $m$, $Lf'(m) = (m-1)\pi\cos(m\pi)$ and $Rf'(m) = m\pi\cos(m\pi)$, which always differ. The integers in $(-1, 3)$ are $0, 1, 2$, so $3$ points.",
  "Confusing continuity at the integers with differentiability there.",
  "U07-C-gif-times-trig", "One-sided derivatives at integers with a vanishing factor.",
  check=_c025, values=[3, 0, 4, 2], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x]\sin(\pi x)$, " + GIF + r". The number of points in the open interval $(-1, 3)$ at which $f$ is not differentiable is", answer=3))


# ---------------------------------------------------------------- 026
def _c026():
    f = Max(x, x**3)
    cands = solve(Eq(x, x**3), x)
    return len(_nondiff_pts(f, cands))
q("U07-C-026", TOP_CNT, "Corners of a maximum of two curves", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \max\{x, x^3\}$ for $x \in \mathbb{R}$. The number of points at which $f$ is not differentiable is",
  r"$3$",
  [(r"$2$", r"Misses $x = 0$, thinking the curves only touch at the origin."),
   (r"$1$", r"Considers only $x \ge 0$ and finds the corner at $x = 1$."),
   (r"$0$", r"Assumes the maximum of two differentiable functions is differentiable.")],
  r"$x = x^3$ at $x = -1, 0, 1$, and the curves cross at each. So $f = x$ on $(-\infty, -1]$, $x^3$ on $[-1, 0]$, $x$ on $[0, 1]$, $x^3$ on $[1, \infty)$. The slopes at $-1, 0, 1$ are $(1, 3)$, $(0, 1)$, $(1, 3)$, all unequal. Hence $3$ points.",
  "Missing a crossing at the origin.",
  "U07-C-minmax-nondiff", "Piecewise rewrite and slope comparison at three points.",
  check=_c026, values=[3, 2, 1, 0], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 027
def _c027():
    f = floor(x) + sqrt(x - floor(x))
    return len(_disc_pts(f, _ints_in(-2, 3)))
q("U07-C-027", TOP_GM, "Continuity of [x] plus root of the fractional part", "Medium", "Conceptual/application MCQ",
  r"Let $f(x) = [x] + \sqrt{x - [x]}$, " + GIF + r". The number of points in the interval $(-2, 3)$ at which $f$ is discontinuous is",
  r"$0$",
  [(r"$4$", r"Counts every integer $-1, 0, 1, 2$ because $[x]$ jumps there."),
   (r"$5$", r"Counts the integers in $[-2, 2]$, including the endpoint $-2$."),
   (r"$6$", r"Counts all integers from $-2$ to $3$, including both endpoints.")],
  r"Only integers need checking. At an integer $m$: $\lim_{x\to m^-} f = (m - 1) + \sqrt{1} = m$, $\lim_{x\to m^+} f = m + 0 = m$, and $f(m) = m$. The jump of $[x]$ is exactly compensated, so $f$ is continuous everywhere; the count is $0$.",
  r"Assuming any expression containing $[x]$ is discontinuous at integers.",
  "U07-C-gif-compensated", "Check both one-sided limits at a general integer.",
  check=_c027, values=[0, 4, 5, 6], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x] + \sqrt{x - [x]}$, " + GIF + r". The number of points in the open interval $(-2, 3)$ at which $f$ is discontinuous is", answer=0))


# ---------------------------------------------------------------- 028
def _c028():
    f = floor(cos(x))
    cands = []
    for m in (-1, 0, 1):
        cands += _roots_in(cos(x) - m, 0, 2*pi)
    return len(_disc_pts(f, cands))
q("U07-C-028", TOP_CNT, "Discontinuities of [cos x]", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = [\cos x]$, " + GIF + r". The number of points in the interval $(0, 2\pi)$ at which $f$ is discontinuous is",
  r"$2$",
  [(r"$3$", r"Also counts $x = \pi$, where $\cos x = -1$ is an integer, though $[\cos x] = -1$ on both sides of it."),
   (r"$1$", r"Counts only $x = \pi$, the single point where $\cos x$ reaches an integer extreme value."),
   (r"$5$", r"Counts $\frac{\pi}{2}, \pi, \frac{3\pi}{2}$ and also the excluded endpoints $0$ and $2\pi$.")],
  r"$f = 0$ on $(0, \frac{\pi}{2}]$, $f = -1$ on $(\frac{\pi}{2}, \frac{3\pi}{2})$ (including $x = \pi$, where $\cos x = -1$), and $f = 0$ on $[\frac{3\pi}{2}, 2\pi)$. So $f$ jumps only at $\frac{\pi}{2}$ and $\frac{3\pi}{2}$: $2$ points.",
  r"Treating every point where the inner function is an integer as a discontinuity.",
  "U07-C-gif-trig", "Track the integer part of $\\cos x$ across the interval; trap at a minimum.",
  check=_c028, values=[2, 3, 1, 5], cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 029
def _c029():
    f = floor(2*sin(x))
    cands = []
    for m in (0, 1, 2):
        cands += _roots_in(2*sin(x) - m, 0, pi)
    return len(_disc_pts(f, sorted(set(cands), key=lambda t: float(t))))
q("U07-C-029", TOP_CNT, "Discontinuities of [2 sin x]", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = [2\sin x]$, " + GIF + r". The number of points in the interval $(0, \pi)$ at which $f$ is discontinuous is",
  r"$3$",
  [(r"$2$", r"Finds $x = \frac{\pi}{6}, \frac{5\pi}{6}$ from $2\sin x = 1$ but misses $x = \frac{\pi}{2}$, where $f$ takes the isolated value $2$."),
   (r"$1$", r"Counts only $x = \frac{\pi}{2}$, where $2\sin x$ reaches the integer $2$."),
   (r"$5$", r"Adds the endpoints $0$ and $\pi$, where $2\sin x = 0$, to the three interior points.")],
  r"On $(0, \pi)$, $2\sin x \in (0, 2]$. $f = 0$ on $(0, \frac{\pi}{6})$, $f = 1$ on $[\frac{\pi}{6}, \frac{\pi}{2})$, $f(\frac{\pi}{2}) = 2$, $f = 1$ on $(\frac{\pi}{2}, \frac{5\pi}{6}]$ and $f = 0$ on $(\frac{5\pi}{6}, \pi)$. Discontinuities: $\frac{\pi}{6}, \frac{\pi}{2}, \frac{5\pi}{6}$, so $3$.",
  "Missing an isolated value at a maximum of the inner function.",
  "U07-C-gif-trig", "Piecewise description of $[2\\sin x]$; trap at the maximum.",
  check=_c029, values=[3, 2, 1, 5], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [2\sin x]$, " + GIF + r". The number of points in the open interval $(0, \pi)$ at which $f$ is discontinuous is", answer=3))


# ---------------------------------------------------------------- 030
def _c030():
    L = limit((1 - cos(8*x)) / (4*x**2), x, 0, '-')
    R = limit(sqrt(x) / (sqrt(16 + sqrt(x)) - 4), x, 0, '+')
    assert L == R
    return L
q("U07-C-030", TOP_PW, "Matching two different one-sided limits", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \frac{1 - \cos 8x}{4x^2}$ for $x < 0$, $f(0) = a$, and $f(x) = \frac{\sqrt{x}}{\sqrt{16 + \sqrt{x}} - 4}$ for $x > 0$. If $f$ is continuous at $x = 0$, then $a$ equals",
  r"$8$",
  [(r"$4$", r"Rationalises the right piece to $\sqrt{16 + \sqrt{x}} + 4$ but drops the $+4$, getting $4$, and takes this one-sided value as $a$ without checking the left side."),
   (r"$16$", r"Uses $1 - \cos 8x \approx (8x)^2$ without the factor $\frac{1}{2}$, getting $\frac{64}{4} = 16$ on the left, and takes this one-sided value as $a$ without checking the right side."),
   (r"$1$", r"Uses $1 - \cos kx \approx \frac{k x^2}{2}$, forgetting to square $k$, getting $\frac{4x^2}{4x^2} = 1$ on the left, and takes this one-sided value as $a$ without checking the right side.")],
  r"Left: $\frac{1 - \cos 8x}{4x^2} = \frac{2\sin^2 4x}{4x^2} = \frac{1}{2}\left(\frac{\sin 4x}{x}\right)^2 \to \frac{16}{2} = 8$. Right: multiplying by the conjugate, $\frac{\sqrt{x}(\sqrt{16+\sqrt{x}}+4)}{\sqrt{x}} = \sqrt{16 + \sqrt{x}} + 4 \to 8$. Both equal $8$, so $a = 8$.",
  r"Mishandling $1 - \cos kx \approx \frac{k^2x^2}{2}$.",
  "U07-C-two-sided-match", "Two different limit techniques on the two sides.",
  check=_c030, values=[8, 4, 16, 1], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = \frac{1 - \cos 8x}{4x^2}$ for $x < 0$, $f(0) = a$, and $f(x) = \frac{\sqrt{x}}{\sqrt{16 + \sqrt{x}} - 4}$ for $x > 0$. If $f$ is continuous at $x = 0$, then the value of $a$ is", answer=8))


# ---------------------------------------------------------------- 031
def _c031():
    f = Abs(x**2 - 1)*(x**2 + x - 2)
    cands = _roots_in(x**2 - 1, -oo, oo)
    return FiniteSet(*_nondiff_pts(f, cands))
q("U07-C-031", TOP_DF, "Which corners survive in |x^2 - 1| g(x)", "Medium", "Multi-step computation MCQ",
  r"The set of all points at which $f(x) = |x^2 - 1|\,(x^2 + x - 2)$ is not differentiable is",
  r"$\{-1\}$",
  [(r"$\{1\}$", r"Reverses the criterion and keeps the corner where $x^2 + x - 2$ vanishes."),
   (r"$\{-1, 1\}$", r"Lists both zeros of $x^2 - 1$ without checking the second factor."),
   (r"$\{-2, -1, 1\}$", r"Also adds $x = -2$, a zero of $x^2 + x - 2$, as a corner.")],
  r"Corners can occur only at $x = \pm1$. Write $g(x) = x^2 + x - 2 = (x-1)(x+2)$. At $x = 1$, $g(1) = 0$, so $f$ behaves like $|x-1|(x-1)\cdot(\text{smooth})$ and is differentiable. At $x = -1$, $g(-1) = -2 \ne 0$ and the one-sided derivatives are $\pm 2 \cdot g(-1)$, which differ. So the set is $\{-1\}$.",
  r"Not using the criterion $g(a) = 0$ for $|x - a| g(x)$.",
  "U07-C-abs-times-g", "Apply the criterion at two candidate points.",
  check=_c031, values=[FiniteSet(-1), FiniteSet(1), FiniteSet(-1, 1), FiniteSet(-2, -1, 1)],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 032
def _c032():
    import mpmath as _mp
    expr = (x**(2*n + 1) + x**2) / (x**(2*n) + 1)
    def F(c):
        # numerical limit: evaluate at a very large n with high precision
        with _mp.workdps(60):
            cc = _mp.mpf(c)
            N_ = 10**7
            return (cc**(2*N_ + 1) + cc**2) / (cc**(2*N_) + 1)
    # sanity: the evaluator reproduces the given expression at a small n
    assert abs(float(expr.subs({x: Rational(3, 2), n: 3})) - float((Rational(3, 2)**7 + Rational(9, 4)) / (Rational(3, 2)**6 + 1))) < 1e-12
    cands = solve(x**2 - 1, x) + [Integer(0)]
    eps = Rational(1, 10**4)
    bad = [c for c in cands if not (abs(F(c - eps) - F(c)) < 0.01 and abs(F(c + eps) - F(c)) < 0.01)]
    return len(bad)
q("U07-C-032", TOP_CP, "Continuity of a function defined by a limit", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \lim_{n \to \infty} \frac{x^{2n+1} + x^2}{x^{2n} + 1}$ for $x \in \mathbb{R}$, $n \in \mathbb{N}$. The number of points of discontinuity of $f$ is",
  r"$1$",
  [(r"$2$", r"Sees that the formula changes at $|x| = 1$ and counts both $x = 1$ and $x = -1$ without comparing the one-sided values."),
   (r"$0$", r"Checks $x = 1$, where $x^2$ and $x$ both tend to $1 = f(1)$, and assumes by symmetry that $x = -1$ behaves the same way."),
   (r"$3$", r"Counts $x = \pm 1$ and also $x = 0$, where the branches $x^2$ and $x$ take the same value, treating it as a break point.")],
  r"For $|x| < 1$, $x^{2n} \to 0$ and $x^{2n+1} \to 0$, so $f(x) = x^2$. For $|x| > 1$, dividing by $x^{2n}$ gives $f(x) = \lim \frac{x + x^{2 - 2n}}{1 + x^{-2n}} = x$. Also $f(1) = \frac{1 + 1}{2} = 1$ and $f(-1) = \frac{-1 + 1}{2} = 0$. At $x = 1$ both sides tend to $1 = f(1)$, so $f$ is continuous; at $x = -1$ the left limit is $-1$ and the right limit is $1$, so $f$ is discontinuous. Elsewhere $f$ is locally a polynomial, so there is exactly $1$ point.",
  r"Assuming the two boundary points $x = \pm 1$ of a limit-defined function behave alike.",
  "U07-C-limit-defined-fn-odd", "Evaluate the limit in three regions, then compare one-sided values at two boundaries that behave differently.",
  check=_c032, values=[1, 2, 0, 3], cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 033
q("U07-C-033", TOP_CP, "Algebra of continuous and discontinuous functions", "Medium", "Statement-based MCQ",
  r"Statement I: If $f$ and $g$ are both discontinuous at $x = a$, then $fg$ is discontinuous at $x = a$. Statement II: If $f$ is continuous at $x = a$ and $g$ is discontinuous at $x = a$, then $f + g$ is discontinuous at $x = a$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Generalises Statement II to products without testing a counterexample."),
   (ST_FF, r"Rejects Statement II by thinking of $f \cdot g$ examples rather than $f + g$."),
   (ST_TF, r"Reverses the truth values of the two statements.")],
  r"Statement I is false: take $f(x) = 1$ for $x \ge 0$, $f(x) = -1$ for $x < 0$, and $g = f$. Both jump at $0$, but $fg = 1$ everywhere. Statement II is true: if $f + g$ were continuous at $a$, then $g = (f + g) - f$ would be continuous at $a$, a contradiction.",
  "Assuming discontinuities can never cancel in products.",
  "U07-C-stmt-algebra", "Needs a counterexample and a short contradiction argument.",
  cognitive="Understanding", source_class="XII")


# ---------------------------------------------------------------- 034
def _c034():
    L = limit((sin((p_ + 1)*x) + sin(2*x)) / x, x, 0, '-')
    R = limit((sqrt(1 + 4*x) - 1) / x, x, 0, '+')
    s = solve([Eq(L, q_), Eq(R, q_)], [p_, q_], dict=True)[0]
    return s[p_]*s[q_]
q("U07-C-034", TOP_PW, "Two parameters from two different one-sided limits", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = \frac{\sin((p+1)x) + \sin 2x}{x}$ for $x < 0$, $f(0) = q$, and $f(x) = \frac{\sqrt{1 + 4x} - 1}{x}$ for $x > 0$. If $f$ is continuous at $x = 0$, then $pq$ equals",
  r"$-2$",
  [(r"$0$", r"Takes $\frac{\sin 2x}{x} \to 1$, so $p + 2 = 2$ and $p = 0$."),
   (r"$4$", r"Rationalises the right piece but keeps $4$ as the limit, forgetting the denominator $\sqrt{1+4x}+1 \to 2$; then $q = 4$, $p = 1$."),
   (r"$-\frac{5}{4}$", r"Drops the factor $4$ when rationalising, getting $q = \frac{1}{2}$ and $p = -\frac{5}{2}$.")],
  r"Right: $\frac{\sqrt{1+4x}-1}{x} = \frac{4}{\sqrt{1+4x}+1} \to 2$, so $q = 2$. Left: $\frac{\sin(p+1)x}{x} + \frac{\sin 2x}{x} \to (p + 1) + 2$. Setting $p + 3 = 2$ gives $p = -1$. Hence $pq = -2$.",
  r"Losing a coefficient in $\frac{\sin kx}{x} \to k$ or in rationalising.",
  "U07-C-two-sided-match", "Two limits of different kinds, then two equations.",
  check=_c034, values=[-2, 0, 4, Rational(-5, 4)], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 035
def _c035():
    p = x**3 - 3*x + 2
    f = Abs(p)
    return FiniteSet(*_nondiff_pts(f, _roots_in(p, -oo, oo)))
q("U07-C-035", TOP_DF, "Modulus of a cubic with a repeated root", "Medium", "Multi-step computation MCQ",
  r"The set of all points at which $f(x) = |x^3 - 3x + 2|$ is not differentiable is",
  r"$\{-2\}$",
  [(r"$\{-2, 1\}$", r"Lists every real zero of the cubic, including the double zero $x = 1$."),
   (r"$\{1\}$", r"Keeps the repeated zero and drops the simple one."),
   (r"$\{-1, 2\}$", r"Takes the zeros with the wrong signs.")],
  r"$x^3 - 3x + 2 = (x-1)^2(x+2)$. At the double zero $x = 1$ the cubic does not change sign, so $|f|$ equals $(x-1)^2|x+2|$ near $1$, which is differentiable (derivative $0$). At the simple zero $x = -2$ the sign changes, giving a corner. So the set is $\{-2\}$.",
  "Assuming every zero of the inner polynomial is a corner.",
  "U07-C-mod-poly-roots", "Factorise, then distinguish simple and repeated zeros.",
  check=_c035, values=[FiniteSet(-2), FiniteSet(-2, 1), FiniteSet(1), FiniteSet(-1, 2)],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 036
def _c036():
    g = 1/(x - 2)
    from_g = solve(denom(together(g)), x)
    from_f = solve(Eq(g, 1), x)
    return FiniteSet(*(from_g + from_f))
q("U07-C-036", TOP_CP, "Problem points of a composition f(g(x))", "Medium", "Multi-step computation MCQ",
  r"Let $f(t) = \frac{1}{t - 1}$ and $g(x) = \frac{1}{x - 2}$. The set of all real $x$ at which $f(g(x))$ is either undefined or discontinuous is",
  r"$\{2, 3\}$",
  [(r"$\{3\}$", r"Simplifies $f(g(x))$ to $\frac{x-2}{3-x}$ and forgets that $g$ itself needs $x \ne 2$."),
   (r"$\{2\}$", r"Checks only where $g$ is undefined."),
   (r"$\{1, 2\}$", r"Uses the problem point $t = 1$ of $f$ directly as a value of $x$.")],
  r"$g$ needs $x \ne 2$. Then $f(g(x))$ needs $g(x) \ne 1$, i.e. $\frac{1}{x-2} \ne 1$, so $x \ne 3$. Elsewhere $f(g(x)) = \frac{x-2}{3-x}$ is continuous. The problem points are $2$ and $3$.",
  "Reading the problem points of a composite from its simplified form.",
  "U07-C-composite-disc", "Two layers of the composition; simplification trap.",
  check=_c036, values=[FiniteSet(2, 3), FiniteSet(3), FiniteSet(2), FiniteSet(1, 2)],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 037
def _c037():
    f = floor(2*x) - 2*floor(x)
    cands = [Rational(m, 2) for m in range(1, 6)]
    return len(_disc_pts(f, cands))
q("U07-C-037", TOP_CNT, "Discontinuities of [2x] - 2[x]", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = [2x] - 2[x]$, " + GIF + r". The number of points in the interval $(0, 3)$ at which $f$ is discontinuous is",
  r"$5$",
  [(r"$3$", r"Thinks the jumps of $[2x]$ and $2[x]$ cancel at integers and counts only $x = \frac{1}{2}, \frac{3}{2}, \frac{5}{2}$."),
   (r"$2$", r"Counts only the integers $1$ and $2$."),
   (r"$6$", r"Also counts the endpoint $x = 3$.")],
  r"Possible jumps are at multiples of $\frac{1}{2}$. At a half-integer only $[2x]$ jumps (by $1$). At an integer, $[2x]$ jumps by $1$ and $2[x]$ by $2$, a net jump of $-1$; indeed $f$ is the indicator of $\{x\} \ge \frac{1}{2}$. So all of $\frac{1}{2}, 1, \frac{3}{2}, 2, \frac{5}{2}$ are discontinuities: $5$.",
  "Assuming jumps of the two terms cancel at integers.",
  "U07-C-gif-combination", "Compare jump sizes of two greatest-integer terms.",
  check=_c037, values=[5, 3, 2, 6], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [2x] - 2[x]$, " + GIF + r". The number of points in the open interval $(0, 3)$ at which $f$ is discontinuous is", answer=5))


# ---------------------------------------------------------------- 038
def _c038():
    f = Min(1, x**2, x**3)
    cands = set(solve(x**2 - 1, x) + solve(x**3 - 1, x) + solve(x**2 - x**3, x))
    cands = [c for c in cands if c.is_real]
    return len(_nondiff_pts(f, cands))
q("U07-C-038", TOP_CNT, "Corners of a minimum of three functions", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \min\{1, x^2, x^3\}$ for $x \in \mathbb{R}$. The number of points at which $f$ is not differentiable is",
  r"$1$",
  [(r"$2$", r"Counts $x = 0$ as a corner because $x^2$ and $x^3$ meet there, though $f = x^3$ on both sides."),
   (r"$3$", r"Counts $x = -1, 0, 1$, the points where some pair of the three curves meet."),
   (r"$0$", r"Assumes the minimum of smooth functions is smooth.")],
  r"For $x < 0$, $x^3$ is negative and smallest; for $0 \le x \le 1$, $x^3 \le x^2 \le 1$; for $x > 1$, $1$ is smallest. So $f = x^3$ for $x \le 1$ and $f = 1$ for $x > 1$. The only corner is at $x = 1$ (slopes $3$ and $0$).",
  "Counting every meeting point of a pair of curves as a corner.",
  "U07-C-minmax-nondiff", "Identify which function is minimal on each region.",
  check=_c038, values=[1, 2, 3, 0], cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 039
def _c039():
    f = (x - 1)*sign(x**2 - 1)
    return len(_disc_pts(f, _roots_in(x**2 - 1, -oo, oo)))
q("U07-C-039", TOP_GM, "Signum times a vanishing factor", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = (x - 1)\operatorname{sgn}(x^2 - 1)$, where $\operatorname{sgn}$ is the signum function. The number of points of discontinuity of $f$ on $\mathbb{R}$ is",
  r"$1$",
  [(r"$2$", r"Counts both sign changes $x = \pm 1$ of $x^2 - 1$ without using the factor $x - 1$."),
   (r"$0$", r"Thinks the factor $x - 1$ makes $f$ continuous at both $\pm 1$."),
   (r"$3$", r"Adds $x = 0$, where $x^2 - 1$ is least, to the points $\pm 1$.")],
  r"Only $x = \pm1$ need checking. At $x = 1$, $|f(x)| \le |x - 1| \to 0 = f(1)$, so $f$ is continuous. At $x = -1$, $f \to (-2)(1) = -2$ from the left and $(-2)(-1) = 2$ from the right, a jump. So $1$ point.",
  "Ignoring that a vanishing factor can neutralise a jump.",
  "U07-C-signum-disc", "Check two points; one is neutralised by a vanishing factor.",
  check=_c039, values=[1, 2, 0, 3], cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 040
def _c040():
    f1 = floor(Abs(x))
    s1 = _cont(f1, 0)
    g = Abs(floor(x))
    s2 = _cont(g, 0)
    return (s1, s2)
q("U07-C-040", TOP_GM, "Order of composition of greatest integer and modulus at a point", "Medium", "Statement-based MCQ",
  r"Let $[t]$ denote the greatest integer less than or equal to $t$. Statement I: $f(x) = [\,|x|\,]$ is continuous at $x = 0$. Statement II: $g(x) = |\,[x]\,|$ is continuous at $x = 0$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Assumes that taking a modulus always removes a jump, so treats $|\,[x]\,|$ as continuous at $0$ just like $[\,|x|\,]$."),
   (ST_FF, r"Assumes every function built from the greatest integer function is discontinuous at each integer, including $[\,|x|\,]$ at $0$."),
   (ST_FT, r"Interchanges the order of composition, analysing $|\,[x]\,|$ for Statement I and $[\,|x|\,]$ for Statement II.")],
  r"Statement I: for $-1 < x < 1$, $0 \le |x| < 1$, so $[\,|x|\,] = 0$ on the whole interval, including $x = 0$; $f$ is constant near $0$ and hence continuous there. True. Statement II: for $-1 \le x < 0$, $[x] = -1$ and $g(x) = 1$, while for $0 \le x < 1$, $g(x) = 0$. The left limit $1$ differs from $g(0) = 0$, so $g$ is discontinuous at $0$. False.",
  r"Treating $[\,|x|\,]$ and $|\,[x]\,|$ as the same function.",
  "U07-C-stmt-gif-mod-order", "Two compositions analysed separately on both sides of $0$; trap in the order of composition.",
  check=_c040, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 041
def _c041():
    num = x**2 + a_*x + b_
    s1 = solve(Eq(num.subs(x, 1), 0), b_)[0]
    L = limit((num.subs(b_, s1)) / (x - 1), x, 1)
    av = solve(Eq(L, 5), a_)[0]
    return s1.subs(a_, av)
q("U07-C-041", TOP_PW, "Coefficients from a removable discontinuity", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = \frac{x^2 + ax + b}{x - 1}$ for $x \ne 1$, where $a, b$ are real. If $\lim_{x \to 1} f(x) = 5$, so that defining $f(1) = 5$ makes $f$ continuous at $x = 1$, then $b$ equals",
  r"$-4$",
  [(r"$-5$", r"Writes the cofactor as $x + a$ instead of $x + 1 + a$, so $1 + a = 5$, $a = 4$, $b = -5$."),
   (r"$-6$", r"Sets $a$ equal to the limit $5$ and then uses $1 + a + b = 0$."),
   (r"$4$", r"Writes $b = 1 + a$ instead of $b = -1 - a$ (sign slip).")],
  r"A finite limit needs the numerator to vanish at $1$: $1 + a + b = 0$. Then $x^2 + ax + b = (x - 1)(x + 1 + a)$, so the limit is $2 + a = 5$, giving $a = 3$ and $b = -4$.",
  "Mis-forming the cofactor after removing the factor $x - 1$.",
  "U07-C-removable-param", "Two conditions: numerator vanishes, then the limit value.",
  check=_c041, values=[-4, -5, -6, 4], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 042
def _c042():
    f = Abs(log(Abs(x)))
    cands = _roots_in(log(Abs(x)), -oo, oo)
    return len(_nondiff_pts(f, cands))
q("U07-C-042", TOP_CNT, "Corners of |log|x||", "Medium", "Multi-step computation MCQ",
  r"The number of points in the domain of $f(x) = \left|\log_e |x|\right|$ at which $f$ is not differentiable is",
  r"$2$",
  [(r"$3$", r"Also counts $x = 0$, which is not in the domain."),
   (r"$1$", r"Finds the corner at $x = 1$ but forgets that $f$ is even."),
   (r"$0$", r"Assumes a composition of functions that are differentiable on the domain stays differentiable.")],
  r"The domain is $x \ne 0$. $\log_e|x|$ changes sign at $|x| = 1$, i.e. $x = \pm1$, with nonzero slope $\pm1$ there, so $|\log_e|x||$ has a corner at each. Elsewhere in the domain it is differentiable. Hence $2$ points.",
  "Counting a point outside the domain, or missing the symmetric corner.",
  "U07-C-mod-log", "Domain plus sign changes of the inner log.",
  check=_c042, values=[2, 3, 1, 0], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 043
def _c043():
    f = floor(x) + floor(x + Rational(1, 3)) + floor(x + Rational(2, 3))
    cands = [Rational(m, 3) for m in range(1, 9)]
    return len(_disc_pts(f, cands))
q("U07-C-043", TOP_CNT, "Sum of shifted greatest-integer functions", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = [x] + \left[x + \frac{1}{3}\right] + \left[x + \frac{2}{3}\right]$, " + GIF + r". The number of points in the interval $(0, 3)$ at which $f$ is discontinuous is",
  r"$8$",
  [(r"$2$", r"Counts only the integers $1$ and $2$, as for $[x]$ alone."),
   (r"$6$", r"Counts only the jumps of the two shifted terms, missing the integers $1, 2$."),
   (r"$9$", r"Also counts the endpoint $x = 3$.")],
  r"Each term jumps by $+1$ at its own points: $[x]$ at integers, $[x + \frac{1}{3}]$ at $x \equiv \frac{2}{3}$, $[x + \frac{2}{3}]$ at $x \equiv \frac{1}{3} \pmod 1$; these never coincide and never cancel (in fact $f = [3x]$). So $f$ jumps at every multiple of $\frac{1}{3}$ in $(0, 3)$: $\frac{1}{3}, \frac{2}{3}, \ldots, \frac{8}{3}$, that is $8$ points.",
  "Overlooking that the three terms jump at different points.",
  "U07-C-gif-combination", "Locate jumps of three shifted terms.",
  check=_c043, values=[8, 2, 6, 9], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x] + \left[x + \frac{1}{3}\right] + \left[x + \frac{2}{3}\right]$, " + GIF + r". The number of points in the open interval $(0, 3)$ at which $f$ is discontinuous is", answer=8))


# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 044
def _c044():
    f = floor(x**2) - floor(x)**2
    cands = set()
    for m in range(1, 9):
        cands |= set(_roots_in(x**2 - m, 0, 3))
    cands |= set(_ints_in(0, 3))
    return len(_disc_pts(f, sorted(cands, key=lambda t: float(t))))
q("U07-C-044", TOP_CNT, "Discontinuities of [x^2] - [x]^2", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = [x^2] - [x]^2$, " + GIF + r". The number of points in the interval $(0, 3)$ at which $f$ is discontinuous is",
  r"$7$",
  [(r"$8$", r"Counts every point where $x^2$ is an integer, $1, \sqrt{2}, \sqrt{3}, 2, \sqrt{5}, \sqrt{6}, \sqrt{7}, \sqrt{8}$, without checking for cancellation at $x = 1$."),
   (r"$6$", r"Assumes the jumps of the two terms cancel at both integers $1$ and $2$."),
   (r"$10$", r"Adds the jumps of $[x]^2$ at $1$ and $2$ to the $8$ points from $[x^2]$, double counting.")],
  r"Candidates are $x = \sqrt{m}$ for $m = 1, \ldots, 8$. At a non-integer $\sqrt{m}$ only $[x^2]$ jumps. At $x = 1$: left value $0 - 0 = 0$, and $f(1) = 1 - 1 = 0 = $ right value, so $f$ is continuous. At $x = 2$: left value $3 - 1 = 2$ but $f(2) = 4 - 4 = 0$, a jump. So the discontinuities are $\sqrt{2}, \sqrt{3}, 2, \sqrt{5}, \sqrt{6}, \sqrt{7}, 2\sqrt{2}$: $7$ points.",
  "Not checking whether jumps of two greatest-integer terms cancel.",
  "U07-C-gif-difference", "Casework over eight candidates with a cancellation at one integer but not the other.",
  check=_c044, values=[7, 8, 6, 10], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x^2] - [x]^2$, " + GIF + r". The number of points in the open interval $(0, 3)$ at which $f$ is discontinuous is", answer=7))


# ---------------------------------------------------------------- 045
def _c045():
    f = floor(x)*Abs(x - 1)
    cands = sorted(set(_ints_in(-1, 3) + solve(x - 1, x)))
    m = len(_disc_pts(f, cands))
    nn = len(_nondiff_pts(f, cands))
    return m + nn
q("U07-C-045", TOP_CNT, "Counting discontinuities and corners of [x]|x - 1|", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = [x]\,|x - 1|$, " + GIF + r". If $m$ is the number of points in $(-1, 3)$ at which $f$ is discontinuous and $n$ is the number of points in $(-1, 3)$ at which $f$ is not differentiable, then $m + n$ equals",
  r"$5$",
  [(r"$6$", r"Counts $x = 1$ as a discontinuity as well, taking $m = 3$ and $n = 3$."),
   (r"$4$", r"Misses the corner at $x = 1$, taking $m = 2$ and $n = 2$."),
   (r"$3$", r"Reports the number of distinct problem points $0, 1, 2$ instead of $m + n$.")],
  r"Candidates are $0, 1, 2$. At $0$ and $2$, $[x]$ jumps by $1$ while $|x - 1| = 1$, so $f$ jumps: discontinuous and hence not differentiable. At $1$, $f \to 0 = f(1)$ from both sides (continuous), but $f = 0$ on $(0, 1)$ and $f = x - 1$ on $(1, 2)$, so the slopes are $0$ and $1$: not differentiable. So $m = 2$, $n = 3$, $m + n = 5$.",
  "Forgetting that every discontinuity is also a point of non-differentiability, or that a vanishing factor restores continuity only.",
  "U07-C-gif-times-mod", "Classify three candidates for both continuity and differentiability.",
  check=_c045, values=[5, 6, 4, 3], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x]\,|x - 1|$, " + GIF + r". If $m$ is the number of points in $(-1, 3)$ at which $f$ is discontinuous and $n$ is the number of points in $(-1, 3)$ at which $f$ is not differentiable, then $m + n$ is", answer=5))


# ---------------------------------------------------------------- 046
def _c046():
    f = Abs(x) + Abs(Abs(x) - 1)
    cands = [Integer(0)] + _roots_in(Abs(x) - 1, -oo, oo)
    return len(_nondiff_pts(f, cands))
q("U07-C-046", TOP_CNT, "Cancelling corners in a nested modulus", "Difficult", "Multi-step computation MCQ",
  r"The number of points at which $f(x) = |x| + \big||x| - 1\big|$ is not differentiable is",
  r"$2$",
  [(r"$3$", r"Counts the corner of $|x|$ at $x = 0$ together with $x = \pm 1$, without noticing that the two corners at $0$ cancel."),
   (r"$1$", r"Works only with $x \ge 0$ and finds the corner at $x = 1$."),
   (r"$4$", r"Counts the corner at $0$ twice, once for each modulus, along with $x = \pm 1$.")],
  r"For $|x| \le 1$: $f = |x| + 1 - |x| = 1$, a constant, so there is no corner at $x = 0$. For $|x| > 1$: $f = 2|x| - 1$. At $x = \pm 1$ the slope changes between $0$ and $\pm 2$, giving corners. Hence $2$ points.",
  "Adding up corners without checking for cancellation.",
  "U07-C-nested-mod-count", "Region-wise simplification reveals a hidden cancellation.",
  check=_c046, values=[2, 3, 1, 4], cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 047
def _c047():
    p = x**2 - 3*x + 2
    g = x**3 + a_*x**2 + b_*x + 6
    eqs = []
    for r in (1, 2):
        sgL = sign(p.subs(x, r - Rational(1, 100)))
        sgR = sign(p.subs(x, r + Rational(1, 100)))
        eqs.append(Eq(diff(sgL*p*g, x).subs(x, r), diff(sgR*p*g, x).subs(x, r)))
    s = solve(eqs, [a_, b_], dict=True)[0]
    return s[a_] - s[b_]
q("U07-C-047", TOP_DF, "Making |quadratic| times cubic differentiable everywhere", "Difficult", "Inverse/parameter MCQ",
  r"Let $f(x) = |x^2 - 3x + 2|\,(x^3 + ax^2 + bx + 6)$, where $a, b$ are real. If $f$ is differentiable at every real $x$, then $a - b$ equals",
  r"$7$",
  [(r"$13$", r"Drops the constant $6$ from the condition at $x = 2$, solving $a + b = -7$ and $4a + 2b = -8$."),
   (r"$-5$", r"Uses the zeros $-1, -2$ (sign slip) in place of $1, 2$, which gives $a = 6$, $b = 11$."),
   (r"$15$", r"Imposes $g(1) = 0$ and $g'(1) = 0$, treating only the point $x = 1$, which gives $a = 4$, $b = -11$.")],
  r"$|x^2 - 3x + 2| = |x-1||x-2|$ has corners at $1$ and $2$. With $g(x) = x^3 + ax^2 + bx + 6$, $f$ is differentiable at $1$ and $2$ exactly when $g(1) = g(2) = 0$: $a + b = -7$ and $4a + 2b = -14$. Then $2a = 0$, so $a = 0$, $b = -7$, and $a - b = 7$ (indeed $g = (x-1)(x-2)(x+3)$).",
  r"Requiring $g' = 0$ instead of $g = 0$ at the corners.",
  "U07-C-abs-times-g", "Criterion at two corners gives a linear system; several traps.",
  check=_c047, values=[7, 13, -5, 15], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = |x^2 - 3x + 2|\,(x^3 + ax^2 + bx + 6)$, where $a, b$ are real. If $f$ is differentiable at every real $x$, then the value of $a - b$ is", answer=7))


# ---------------------------------------------------------------- 048
def _c048():
    left = -2*sin(x)
    mid = a_*sin(x) + b_
    right = cos(x)
    s = solve([Eq(left.subs(x, -pi/2), mid.subs(x, -pi/2)), Eq(mid.subs(x, pi/2), right.subs(x, pi/2))], [a_, b_], dict=True)[0]
    m = mid.subs(s)
    f = Piecewise((left, x <= -pi/2), (m, x < pi/2), (right, True))
    return FiniteSet(*_nondiff_pts(f, [-pi/2, pi/2]))
q("U07-C-048", TOP_PW, "Continuity fixes parameters, then test differentiability", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = -2\sin x$ for $x \le -\frac{\pi}{2}$, $f(x) = a\sin x + b$ for $-\frac{\pi}{2} < x < \frac{\pi}{2}$, and $f(x) = \cos x$ for $x \ge \frac{\pi}{2}$. If $f$ is continuous on $\mathbb{R}$, then the set of points at which $f$ is not differentiable is",
  r"$\left\{\frac{\pi}{2}\right\}$",
  [(r"$\left\{-\frac{\pi}{2}\right\}$", r"Finds $a, b$ correctly but swaps which join has unequal slopes."),
   (r"$\left\{-\frac{\pi}{2}, \frac{\pi}{2}\right\}$", r"Assumes every join of different formulas is a corner, without comparing slopes."),
   (r"$\emptyset$", r"Assumes that once $a, b$ make $f$ continuous, the joins are automatically smooth.")],
  r"Continuity at $-\frac{\pi}{2}$: $2 = -a + b$; at $\frac{\pi}{2}$: $a + b = 0$. So $a = -1$, $b = 1$ and the middle piece is $1 - \sin x$. At $-\frac{\pi}{2}$: left slope $-2\cos(-\frac{\pi}{2}) = 0$, right slope $-\cos(-\frac{\pi}{2}) = 0$, differentiable. At $\frac{\pi}{2}$: left slope $-\cos\frac{\pi}{2} = 0$, right slope $-\sin\frac{\pi}{2} = -1$, not differentiable. The set is $\{\frac{\pi}{2}\}$.",
  "Equating continuity at a join with differentiability there.",
  "U07-C-param-then-diff", "Solve for two parameters, then compare four one-sided slopes.",
  check=_c048, values=[FiniteSet(pi/2), FiniteSet(-pi/2), FiniteSet(-pi/2, pi/2), S.EmptySet],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 049
def _c049():
    expr = (a_*x + 2 + x**(2*n)*(x**3 + b_)) / (1 + x**(2*n))
    inside = limit(expr.subs(x, Rational(1, 2)), n, oo)   # check the region formula numerically
    assert simplify(inside - (a_/2 + 2)) == 0
    inner = a_*x + 2
    outer = x**3 + b_
    s = solve([Eq(inner.subs(x, 1), outer.subs(x, 1)), Eq(inner.subs(x, -1), outer.subs(x, -1))], [a_, b_], dict=True)[0]
    # value at x = +-1 must also match
    for c in (1, -1):
        val = limit(expr.subs({a_: s[a_], b_: s[b_]}).subs(x, c), n, oo)
        assert simplify(val - inner.subs(s).subs(x, c)) == 0
    return s[a_] + 2*s[b_]
q("U07-C-049", TOP_PW, "Parameters in a function defined by a limit", "Difficult", "Inverse/parameter MCQ",
  r"Let $f(x) = \lim_{n \to \infty} \frac{ax + 2 + x^{2n}(x^3 + b)}{1 + x^{2n}}$, $n \in \mathbb{N}$, where $a, b$ are real. If $f$ is continuous on $\mathbb{R}$, then $a + 2b$ equals",
  r"$5$",
  [(r"$2$", r"Uses $(-1)^3 = 1$ in the outer formula at $x = -1$, which gives $a = 0$, $b = 1$."),
   (r"$1$", r"Drops the constant $2$ from the inner formula, which gives $a = 1$, $b = 0$."),
   (r"$4$", r"Solves correctly but interchanges the values, taking $a = 2$, $b = 1$.")],
  r"For $|x| < 1$, $f = ax + 2$; for $|x| > 1$, $f = x^3 + b$; at $x = \pm1$, $f$ is the average of the two expressions. Continuity at $1$: $a + 2 = 1 + b$; at $-1$: $-a + 2 = -1 + b$. Adding, $4 = 2b$, so $b = 2$ and $a = 1$; then $f(\pm1)$ also matches. Hence $a + 2b = 5$.",
  r"Mishandling the behaviour of $x^{2n}$ in the three regions, or the sign of $x^3$ at $x = -1$.",
  "U07-C-limit-defined-fn", "Evaluate a limit-defined function by regions, then two continuity equations.",
  check=_c049, values=[5, 2, 1, 4], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = \lim_{n \to \infty} \frac{ax + 2 + x^{2n}(x^3 + b)}{1 + x^{2n}}$, $n \in \mathbb{N}$, where $a, b$ are real. If $f$ is continuous on $\mathbb{R}$, then the value of $a + 2b$ is", answer=5))


# ---------------------------------------------------------------- 050
def _c050():
    f = (x**2 - 1)*floor(x)
    cands = _ints_in(-3, 3)
    cont_not_diff = [c for c in cands if _cont(f, c) and not _diff(f, c)]
    return len(cont_not_diff)
q("U07-C-050", TOP_CNT, "Continuous but not differentiable points of (x^2 - 1)[x]", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = (x^2 - 1)[x]$, " + GIF + r". The number of points in the interval $(-3, 3)$ at which $f$ is continuous but not differentiable is",
  r"$2$",
  [(r"$0$", r"Assumes that wherever the factor $x^2 - 1$ makes $f$ continuous, it also makes $f$ differentiable."),
   (r"$3$", r"Counts the discontinuities $x = -2, 0, 2$ instead."),
   (r"$5$", r"Counts all points of non-differentiability, $-2, -1, 0, 1, 2$.")],
  r"Only integers matter. At an integer $m$ the jump is $(m^2 - 1) \cdot 1$, so $f$ is continuous only at $m = \pm1$. At $x = 1$: $f = 0$ on $(0, 1)$ and $f = x^2 - 1$ on $(1, 2)$, slopes $0$ and $2$. At $x = -1$: $f = -2(x^2 - 1)$ on $(-2, -1)$ and $-(x^2 - 1)$ on $(-1, 0)$, slopes $4$ and $2$. Both are corners, so the count is $2$.",
  "Believing a vanishing factor that restores continuity also restores differentiability.",
  "U07-C-gif-times-poly", "Classify five integers for continuity, then two for differentiability.",
  check=_c050, values=[2, 0, 3, 5], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = (x^2 - 1)[x]$, " + GIF + r". The number of points in the open interval $(-3, 3)$ at which $f$ is continuous but not differentiable is", answer=2))


# ---------------------------------------------------------------- 051
def _c051():
    def piece(lo, hi):
        return lambda t: Piecewise((1 + t, (t >= lo) & (t <= hi)), (3 - t, True))
    f = Piecewise((1 + x, x <= 2), (3 - x, True))
    def F(e):
        return Piecewise((1 + e, e <= 2), (3 - e, True))
    fof = F(f)
    cands = [Integer(1), Integer(2), Rational(5, 2)]
    return FiniteSet(*_disc_pts(fof, cands))
q("U07-C-051", TOP_PW, "Discontinuities of f(f(x)) for a piecewise f", "Difficult", "Multi-step computation MCQ",
  r"Let $f : [0, 3] \to [0, 3]$ be given by $f(x) = 1 + x$ for $0 \le x \le 2$ and $f(x) = 3 - x$ for $2 < x \le 3$. The set of points in $(0, 3)$ at which $f(f(x))$ is discontinuous is",
  r"$\{1, 2\}$",
  [(r"$\{2\}$", r"Uses $f(f(x)) = 2 + x$ on all of $[0, 2]$, ignoring that $f(x) > 2$ for $x > 1$, so finds only the jump at $2$."),
   (r"$\{1\}$", r"Finds the new break at $x = 1$ but assumes the outer $f$ smooths out the jump of $f$ at $x = 2$."),
   (r"$\emptyset$", r"Assumes a composition of linear pieces is continuous.")],
  r"For $0 \le x \le 1$: $f(x) = 1 + x \in [1, 2]$, so $f(f(x)) = 2 + x$. For $1 < x \le 2$: $f(x) \in (2, 3]$, so $f(f(x)) = 3 - (1 + x) = 2 - x$. For $2 < x \le 3$: $f(x) = 3 - x \in [0, 1)$, so $f(f(x)) = 4 - x$. At $x = 1$ the values jump from $3$ to $1$; at $x = 2$ from $0$ to $2$. So the set is $\{1, 2\}$.",
  "Composing piecewise functions without splitting by the range of the inner function.",
  "U07-C-composite-piecewise", "Careful case split by the range of the inner function, then two jump checks.",
  check=_c051, values=[FiniteSet(1, 2), FiniteSet(2), FiniteSet(1), S.EmptySet],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 052
def _c052():
    p = (x - 1)*(x**2 - a_)
    # critical parameter values where two roots of p coincide
    crit = sorted(set(solve(resultant(x - 1, x**2 - a_, x), a_) + solve(discriminant(x**2 - a_, x), a_)))
    def cnt(av):
        pp = p.subs(a_, av)
        rts = [r for r in roots(Poly(pp, x)).keys() if r.is_real]
        return len(_nondiff_pts(Abs(pp), rts))
    pieces = []
    bounds = [-oo] + crit + [oo]
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        sample = (lo + hi)/2 if lo.is_finite and hi.is_finite else (hi - 1 if lo == -oo else lo + 1)
        if cnt(sample) == 1:
            pieces.append(Interval.open(lo, hi))
    for c in crit:
        if cnt(c) == 1:
            pieces.append(FiniteSet(c))
    return Union(*pieces)
q("U07-C-052", TOP_DF, "Parameter for exactly one corner of |cubic|", "Difficult", "Inverse/parameter MCQ",
  r"Let $f(x) = |(x - 1)(x^2 - a)|$, where $a$ is a real parameter. The set of all values of $a$ for which $f$ is not differentiable at exactly one point of $\mathbb{R}$ is",
  r"$(-\infty, 0] \cup \{1\}$",
  [(r"$(-\infty, 0) \cup \{1\}$", r"Misses $a = 0$, not seeing that the double zero $x = 0$ of $x^2$ leaves only the corner at $x = 1$."),
   (r"$\{1\}$", r"Considers only the double zero obtained when $x^2 - a$ shares the zero $x = 1$, ignoring $a \le 0$."),
   (r"$(-\infty, 0]$", r"Handles $a \le 0$ but misses $a = 1$, where $(x-1)^2(x+1)$ has a single corner at $x = -1$.")],
  r"$|p|$ has a corner exactly at the simple real zeros of $p = (x-1)(x^2 - a)$. If $a < 0$, the only zero is $x = 1$: one corner. If $a = 0$, $p = (x-1)x^2$: corner at $1$ only. If $0 < a$, $a \ne 1$: three simple zeros $1, \pm\sqrt{a}$, three corners. If $a = 1$, $p = (x-1)^2(x+1)$: corner only at $-1$. So $a \in (-\infty, 0] \cup \{1\}$.",
  "Missing boundary cases where zeros merge.",
  "U07-C-mod-poly-param", "Casework on a parameter, including two boundary cases.",
  check=_c052, values=[Union(Interval(-oo, 0), FiniteSet(1)), Union(Interval.open(-oo, 0), FiniteSet(1)), FiniteSet(1), Interval(-oo, 0)],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 053
def _c053():
    f = floor(x)**2 - floor(x)
    return len(_disc_pts(f, _ints_in(-2, 3)))
q("U07-C-053", TOP_CNT, "Discontinuities of [x]^2 - [x]", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = [x]^2 - [x]$, " + GIF + r". The number of points in the interval $(-2, 3)$ at which $f$ is discontinuous is",
  r"$3$",
  [(r"$4$", r"Counts every integer $-1, 0, 1, 2$ in the interval because $[x]$ jumps at each."),
   (r"$2$", r"Thinks $f$ is continuous at every integer $m$ where $m^2 - m = 0$, i.e. $m = 0$ and $m = 1$, leaving only $-1$ and $2$."),
   (r"$0$", r"Assumes the quadratic expression in $[x]$ cancels all jumps.")],
  r"Write $h(t) = t^2 - t$. At an integer $m$, the left limit is $h(m - 1) = (m-1)(m-2)$ and $f(m) = h(m) = m(m-1)$. They agree only when $(m - 1)(m - 2 - m) = 0$, i.e. $m = 1$. In $(-2, 3)$ the integers are $-1, 0, 1, 2$, so $f$ is discontinuous at $-1, 0, 2$: $3$ points.",
  r"Assuming $h([x])$ jumps at every integer, or that a zero of $h$ prevents a jump.",
  "U07-C-gif-poly-of-gif", "General jump condition $h(m-1) = h(m)$, then casework.",
  check=_c053, values=[3, 4, 2, 0], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = [x]^2 - [x]$, " + GIF + r". The number of points in the open interval $(-2, 3)$ at which $f$ is discontinuous is", answer=3))


# ---------------------------------------------------------------- 054
def _c054():
    f = Abs(sin(x))*(x**2 - pi*x)
    cands = _roots_in(sin(x), -2*pi, 2*pi)
    return FiniteSet(*_nondiff_pts(f, cands))
q("U07-C-054", TOP_DF, "Corners of |sin x| times a quadratic", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = |\sin x|\,(x^2 - \pi x)$. The set of points in $(-2\pi, 2\pi)$ at which $f$ is not differentiable is",
  r"$\{-\pi\}$",
  [(r"$\{-\pi, 0, \pi\}$", r"Lists every zero of $\sin x$ in the interval without checking the second factor."),
   (r"$\{0, \pi\}$", r"Reverses the criterion and keeps the points where $x^2 - \pi x$ vanishes."),
   (r"$\{-\pi, \pi\}$", r"Notices that $x^2 - \pi x$ vanishes at $0$ but misses its zero at $\pi$.")],
  r"Corners of $|\sin x|$ in $(-2\pi, 2\pi)$ are at $-\pi, 0, \pi$. Near such a point $c$, $|\sin x| = |x - c|\cdot(\text{positive smooth})$, so $f$ is differentiable at $c$ exactly when $g(c) = c^2 - \pi c = 0$. This holds at $c = 0$ and $c = \pi$ but $g(-\pi) = 2\pi^2 \ne 0$. So the set is $\{-\pi\}$.",
  r"Not applying the $|x-c|g(x)$ criterion at each corner.",
  "U07-C-abs-trig-times-g", "Locate three corners, then test the criterion at each.",
  check=_c054, values=[FiniteSet(-pi), FiniteSet(-pi, 0, pi), FiniteSet(0, pi), FiniteSet(-pi, pi)],
  cognitive="Analysis", source_class="XII")


# ---------------------------------------------------------------- 055
def _c055():
    L = a_*x**2 + b_*x + c_
    R = log(x)
    eqs = [Eq(diff(L, x, k).subs(x, 1), diff(R, x, k).subs(x, 1)) for k in range(3)]
    s = solve(eqs, [a_, b_, c_], dict=True)[0]
    return s[a_] + s[b_]
q("U07-C-055", TOP_PW, "Three parameters for a twice differentiable join", "Difficult", "Inverse/parameter MCQ",
  r"Let $f(x) = ax^2 + bx + c$ for $x < 1$ and $f(x) = \log_e x$ for $x \ge 1$. If $f$ is twice differentiable at $x = 1$, then $a + b$ equals",
  r"$\frac{3}{2}$",
  [(r"$\frac{1}{2}$", r"Takes $(\log_e x)'' = +\frac{1}{x^2}$, so $2a = 1$, $a = \frac{1}{2}$, $b = 0$."),
   (r"$2$", r"Writes the second derivative of $ax^2$ as $a$, so $a = -1$ and $b = 1 - 2a = 3$."),
   (r"$1$", r"Matches first derivatives as $a + b = 1$, differentiating $ax^2$ as $ax$.")],
  r"Matching value, first and second derivatives at $1$: $a + b + c = 0$, $2a + b = 1$, $2a = -1$. So $a = -\frac{1}{2}$, $b = 2$, $c = -\frac{3}{2}$, and $a + b = \frac{3}{2}$.",
  r"Sign error in $(\log_e x)'' = -\frac{1}{x^2}$.",
  "U07-C-twice-diff-param", "Three matching conditions including the second derivative.",
  check=_c055, values=[Rational(3, 2), Rational(1, 2), 2, 1], cognitive="Application", source_class="XII")


# ---------------------------------------------------------------- 056
def _c056():
    f = Min(Abs(sin(x)), Abs(cos(x)))
    cands = set(_roots_in(sin(x), 0, 2*pi)) | set(_roots_in(cos(x), 0, 2*pi)) | set(_roots_in(tan(x)**2 - 1, 0, 2*pi))
    return len(_nondiff_pts(f, sorted(cands, key=lambda t: float(t))))
q("U07-C-056", TOP_CNT, "Corners of min{|sin x|, |cos x|}", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = \min\{|\sin x|, |\cos x|\}$. The number of points in the interval $(0, 2\pi)$ at which $f$ is not differentiable is",
  r"$7$",
  [(r"$4$", r"Counts only the crossing points $\frac{\pi}{4}, \frac{3\pi}{4}, \frac{5\pi}{4}, \frac{7\pi}{4}$, assuming (as for a maximum) that the zeros cause no corners."),
   (r"$3$", r"Counts only the zeros $\frac{\pi}{2}, \pi, \frac{3\pi}{2}$ of $\cos x$ and $\sin x$."),
   (r"$6$", r"Counts the four crossings and the zeros of $\cos x$ but overlooks the zero of $\sin x$ at $x = \pi$.")],
  r"Where $|\sin x| = |\cos x|$, i.e. $x = \frac{\pi}{4}, \frac{3\pi}{4}, \frac{5\pi}{4}, \frac{7\pi}{4}$, the minimum switches between curves with slopes of opposite sign: $4$ corners. Near a zero of $\cos x$ ($\frac{\pi}{2}, \frac{3\pi}{2}$) the minimum is $|\cos x|$, which has a corner there; near $x = \pi$ the minimum is $|\sin x|$, again a corner. Total $4 + 3 = 7$.",
  "Thinking zeros of the inner functions never create corners of the minimum.",
  "U07-C-min-trig", "Two kinds of corners must both be found on a periodic graph.",
  check=_c056, values=[7, 4, 3, 6], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = \min\{|\sin x|, |\cos x|\}$. The number of points in the open interval $(0, 2\pi)$ at which $f$ is not differentiable is", answer=7))


# ---------------------------------------------------------------- 057
def _c057():
    g = Abs(x)**3
    gp = diff(g, x)
    s1 = bool(limit(gp/x, x, 0, '+') == limit(gp/x, x, 0, '-'))   # gp(0) = 0
    assert gp.subs(x, 0) == 0
    h = (x - floor(x))*(1 - (x - floor(x)))
    s2 = all(_cont(h, m) for m in range(-3, 4))
    return (s1, s2)
q("U07-C-057", TOP_DF, "Second derivative of |x|^3 and continuity of a fractional-part product", "Difficult", "Statement-based MCQ",
  r"Statement I: $g(x) = |x|^3$ is twice differentiable at $x = 0$. Statement II: $h(x) = \{x\}\,(1 - \{x\})$ is continuous at every integer, where $\{x\} = x - [x]$ and $[t]$ denotes the greatest integer less than or equal to $t$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Thinks any modulus gives a corner at $0$ and that $\{x\}$ makes $h$ jump at integers."),
   (ST_TF, r"Gets Statement I right but assumes $h$ jumps at integers because $\{x\}$ does."),
   (ST_FT, r"Confuses $|x|^3$ with $x|x|$, whose second derivative fails at $0$.")],
  r"Statement I: $g'(x) = 3x|x|$, so $g'(0) = 0$ and $\frac{g'(h) - g'(0)}{h} = 3|h| \to 0$; thus $g''(0) = 0$ exists. True. Statement II: at an integer $m$, as $x \to m^-$, $\{x\} \to 1$ and $h \to 1 \cdot 0 = 0$; as $x \to m^+$, $\{x\} \to 0$ and $h \to 0$; and $h(m) = 0$. True.",
  r"Assuming any function built from $|x|$ or $\{x\}$ misbehaves at the special points.",
  "U07-C-stmt-second-deriv", "Second derivative via a difference quotient plus a one-sided limit argument.",
  check=_c057, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis", source_class="XII")
