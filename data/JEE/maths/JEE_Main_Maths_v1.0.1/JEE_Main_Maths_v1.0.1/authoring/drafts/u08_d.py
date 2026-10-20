import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x', real=True)
t = Symbol('t', real=True)
xp = Symbol('x', positive=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_FTC = "Fundamental theorem of calculus"
TOP_PROP = "Properties of definite integrals"
TOP_MOD = "Modulus and greatest integer integrands"
TOP_VAR = "Integrals with variable limits"
TOP_EQ = "Integral equations"
SC = "XII"


def _breaks(expr, a, b):
    """Points of [a, b] where a floor, modulus, max or min inside expr changes its formula."""
    pts = {sympify(a), sympify(b)}
    for fl in expr.atoms(floor):
        g = fl.args[0]
        vals = [g.subs(x, a + (b - a)*Rational(k, 400)).evalf() for k in range(401)]
        lo, hi = int(floor(min(vals))) - 1, int(ceiling(max(vals))) + 1
        for n in range(lo, hi + 1):
            pts |= set(solveset(Eq(g, n), x, Interval(a, b)))
    for ab in expr.atoms(Abs):
        pts |= set(solveset(Eq(ab.args[0], 0), x, Interval(a, b)))
    for mm in list(expr.atoms(Max)) + list(expr.atoms(Min)):
        ar = mm.args
        for i in range(len(ar)):
            for j in range(i + 1, len(ar)):
                pts |= set(solveset(Eq(ar[i], ar[j]), x, Interval(a, b)))
    return sorted(pts, key=lambda p: float(p))


def pint(expr, a, b):
    """Exact integral of an integrand containing floor, Abs, Max or Min, split at its break points."""
    pts = _breaks(expr, a, b)
    tot = 0
    for l, r in zip(pts, pts[1:]):
        m = (l + r)/2
        e = expr.replace(lambda z: isinstance(z, floor), lambda z: floor(z.args[0].subs(x, m).evalf(50)))
        e = e.replace(lambda z: isinstance(z, Abs), lambda z: z.args[0]*sign(z.args[0].subs(x, m).evalf(50)))
        e = e.replace(lambda z: isinstance(z, (Max, Min)),
                      lambda z: (max if isinstance(z, Max) else min)(z.args, key=lambda w: float(w.subs(x, m))))
        tot += integrate(e, (x, l, r))
    return simplify(tot)


def NI(f, a, b):
    return Integral(f, (x, a, b)).evalf(30)


# ================================================================ EASY
# ---------------------------------------------------------------- 001
q("U08-D-001", TOP_FTC, "Definite integral by substitution", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{1}^{e} \frac{1 + \log_e x}{x}\,dx$ is",
  r"$\frac{3}{2}$",
  [(r"$\frac{1}{2}$", r"Integrates only the $\frac{\log_e x}{x}$ part, getting $\left[\frac{(\log_e x)^2}{2}\right]_1^e = \frac{1}{2}$, and drops $\int_1^e \frac{dx}{x} = 1$."),
   (r"$2$", r"Uses $u = \log_e x$ but takes $\int_0^1 u\,du = 1$ (writes the antiderivative of $u$ as $u^2$), so $1 + 1 = 2$."),
   (r"$1$", r"Keeps only $\int_1^e \frac{dx}{x} = 1$ and drops the $\frac{\log_e x}{x}$ term.")],
  r"Put $u = \log_e x$, $du = \frac{dx}{x}$; the limits $x = 1, e$ become $u = 0, 1$. The integral is $\int_0^1 (1 + u)\,du = \left[u + \frac{u^2}{2}\right]_0^1 = \frac{3}{2}$.",
  r"Dropping one of the two terms after splitting, or mishandling the power rule for $\int u\,du$.",
  "U08-D-ftc-substitution", "One substitution with a change of limits.",
  check=lambda: integrate((1 + log(x))/x, (x, 1, E)), values=[Rational(3, 2), Rational(1, 2), 2, 1],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 002
q("U08-D-002", TOP_PROP, "King's property on a general interval", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{\pi/6}^{\pi/3} \frac{dx}{1 + \sqrt{\tan x}}$ is",
  r"$\frac{\pi}{12}$",
  [(r"$\frac{\pi}{6}$", r"Adds $I$ and its King's-property form correctly to get $2I = \frac{\pi}{3} - \frac{\pi}{6} = \frac{\pi}{6}$, but forgets to divide by $2$."),
   (r"$\frac{\pi}{4}$", r"Quotes the familiar value $\frac{\pi}{4}$ of the same integrand over $\left[0, \frac{\pi}{2}\right]$ without using the given limits."),
   (r"$\frac{\pi}{24}$", r"Divides by $2$ twice, taking $2I = \frac{\pi}{12}$.")],
  r"Replacing $x$ by $\frac{\pi}{6} + \frac{\pi}{3} - x = \frac{\pi}{2} - x$ turns $\sqrt{\tan x}$ into $\sqrt{\cot x}$, so $I = \int \frac{\sqrt{\tan x}}{\sqrt{\tan x} + 1}\,dx$ over the same limits. Adding the two forms, $2I = \int_{\pi/6}^{\pi/3} 1\,dx = \frac{\pi}{6}$, hence $I = \frac{\pi}{12}$.",
  r"Forgetting to halve after adding the two forms, or using the $\left[0, \frac{\pi}{2}\right]$ answer for other limits.",
  "U08-D-king-ratio", "One standard property, applied with non-standard limits.",
  check=lambda: NI(1/(1 + sqrt(tan(x))), pi/6, pi/3), values=[pi/12, pi/6, pi/4, pi/24],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 003
q("U08-D-003", TOP_PROP, "Odd and even parts on a symmetric interval", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{-2}^{2} \left(x^3\cos x + x^2 + 1\right)dx$ is",
  r"$\frac{28}{3}$",
  [(r"$0$", r"Treats the whole integrand as odd because of the $x^3 \cos x$ term."),
   (r"$\frac{14}{3}$", r"Drops the odd part correctly but evaluates the even part only over $[0, 2]$, giving $\frac{8}{3} + 2$, and does not double."),
   (r"$\frac{56}{3}$", r"Uses $2\int$ for the even part but over the full interval $[-2, 2]$, doubling the correct value $\frac{28}{3}$.")],
  r"$x^3 \cos x$ is odd, so its integral over $[-2, 2]$ is $0$. The rest is even: $2\int_0^2 (x^2 + 1)\,dx = 2\left(\frac{8}{3} + 2\right) = \frac{28}{3}$.",
  "Treating an integrand as odd when only one of its terms is odd.",
  "U08-D-odd-even-split", "One property (odd/even split) and a short computation.",
  check=lambda: integrate(x**3*cos(x) + x**2 + 1, (x, -2, 2)), values=[Rational(28, 3), 0, Rational(14, 3), Rational(56, 3)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 004
def _c004():
    F = Integral(sqrt(1 + t**3), (t, 0, x**2))
    return diff(F, x).doit().subs(x, 2)
q("U08-D-004", TOP_VAR, "Derivative of an integral with a variable upper limit", "Easy", "Single-step computation MCQ",
  r"If $F(x) = \displaystyle\int_{0}^{x^2} \sqrt{1 + t^3}\,dt$, then $F'(2)$ equals",
  r"$4\sqrt{65}$",
  [(r"$\sqrt{65}$", r"Writes $F'(x) = \sqrt{1 + x^6}$, omitting the chain-rule factor $2x$."),
   (r"$12$", r"Keeps the factor $2x = 4$ but evaluates the integrand at $t = x = 2$, giving $4\sqrt{1 + 8} = 12$."),
   (r"$3$", r"Evaluates the integrand at $t = x$ and omits the factor $2x$: $\sqrt{1 + 8} = 3$.")],
  r"By the fundamental theorem with the chain rule, $F'(x) = \sqrt{1 + (x^2)^3}\cdot 2x = 2x\sqrt{1 + x^6}$. At $x = 2$: $F'(2) = 4\sqrt{65}$.",
  "Omitting the derivative of the upper limit, or substituting $x$ for $t$ in place of $x^2$.",
  "U08-D-leibniz-chain", "Direct use of the Leibniz rule with one chain factor.",
  check=_c004, values=[4*sqrt(65), sqrt(65), 12, 3], cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 005
q("U08-D-005", TOP_MOD, "Modulus of a quadratic", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{2} \left|x^2 - 1\right| dx$ is",
  r"$2$",
  [(r"$\frac{2}{3}$", r"Ignores the modulus: $\int_0^2 (x^2 - 1)\,dx = \frac{8}{3} - 2 = \frac{2}{3}$."),
   (r"$\frac{4}{3}$", r"Integrates only over $[1, 2]$, where $x^2 - 1 \ge 0$, getting $\frac{4}{3}$ and leaving out $[0, 1]$."),
   (r"$\frac{8}{3}$", r"Writes $|x^2 - 1| = x^2 + 1$ on $[0, 1]$, giving $\frac{4}{3} + \frac{4}{3} = \frac{8}{3}$.")],
  r"$x^2 - 1 < 0$ on $[0, 1)$ and $\ge 0$ on $[1, 2]$. So the integral is $\int_0^1 (1 - x^2)\,dx + \int_1^2 (x^2 - 1)\,dx = \frac{2}{3} + \frac{4}{3} = 2$.",
  "Ignoring the sign change of the expression inside the modulus.",
  "U08-D-modulus-poly", "Split at one point and two short integrals.",
  check=lambda: pint(Abs(x**2 - 1), 0, 2), values=[2, Rational(2, 3), Rational(4, 3), Rational(8, 3)],
  numerical=dict(question=r"The value of $\displaystyle\int_{0}^{2} \left|x^2 - 1\right| dx$ is", answer=2),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 006
q("U08-D-006", TOP_MOD, "Greatest integer function times a polynomial", "Easy", "Single-step computation MCQ",
  r"If $[x]$ denotes the greatest integer less than or equal to $x$, then $\displaystyle\int_{0}^{2} x[x]\,dx$ equals",
  r"$\frac{3}{2}$",
  [(r"$2$", r"Drops the greatest integer function and evaluates $\int_0^2 x\,dx = 2$."),
   (r"$\frac{7}{2}$", r"Takes $[x] = 1$ on $(0, 1)$ and $[x] = 2$ on $(1, 2)$ (rounding up), giving $\frac{1}{2} + 3 = \frac{7}{2}$."),
   (r"$\frac{8}{3}$", r"Replaces $[x]$ by $x$, evaluating $\int_0^2 x^2\,dx = \frac{8}{3}$.")],
  r"$[x] = 0$ on $[0, 1)$ and $[x] = 1$ on $[1, 2)$. So the integral is $\int_0^1 0\,dx + \int_1^2 x\,dx = \frac{4 - 1}{2} = \frac{3}{2}$.",
  "Using the ceiling value of $[x]$ or ignoring the step function.",
  "U08-D-floor-linear", "One split at an integer point.",
  check=lambda: pint(x*floor(x), 0, 2), values=[Rational(3, 2), 2, Rational(7, 2), Rational(8, 3)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 007
def _c007():
    assert simplify(1 - cos(2*x) - 2*sin(x)**2) == 0
    return pint(sqrt(2*sin(x)**2), 0, 10*pi)
q("U08-D-007", TOP_PROP, "Periodic integrand with a hidden modulus", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{10\pi} \sqrt{1 - \cos 2x}\,dx$ is",
  r"$20\sqrt{2}$",
  [(r"$0$", r"Writes $\sqrt{2\sin^2 x} = \sqrt{2}\sin x$ without the modulus; then the integral over whole periods is $0$."),
   (r"$10\sqrt{2}$", r"Uses period $2\pi$ for $|\sin x|$ with area $2$ per period: $5 \times 2\sqrt{2}$."),
   (r"$20$", r"Uses $1 - \cos 2x = \sin^2 x$ (missing the factor $2$), so the integrand becomes $|\sin x|$.")],
  r"$1 - \cos 2x = 2\sin^2 x$, so the integrand is $\sqrt{2}\,|\sin x|$, which has period $\pi$ and $\int_0^{\pi} |\sin x|\,dx = 2$. Over $10$ periods the integral is $10 \times 2\sqrt{2} = 20\sqrt{2}$.",
  r"Writing $\sqrt{\sin^2 x} = \sin x$ in place of $|\sin x|$.",
  "U08-D-periodic-modsin", "One identity and the periodicity property.",
  check=_c007, values=[20*sqrt(2), 0, 10*sqrt(2), 20], cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 008
q("U08-D-008", TOP_PROP, "King's property giving zero", "Easy", "Direct concept MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi/2} \log_e(\tan x)\,dx$ is",
  r"$0$",
  [(r"$\frac{\pi}{2}\log_e 2$", r"Uses the known value of $\int_0^{\pi/2} \log_e(\sin x)\,dx$ with the sign reversed, as though the tangent integral were that result."),
   (r"$-\frac{\pi}{2}\log_e 2$", r"Quotes $\int_0^{\pi/2} \log_e(\sin x)\,dx = -\frac{\pi}{2}\log_e 2$ for the tangent integral."),
   (r"$\frac{\pi}{4}$", r"Applies the familiar answer $\frac{\pi}{4}$ for $\int_0^{\pi/2} \frac{f(\sin x)}{f(\sin x) + f(\cos x)}\,dx$, which is a different form.")],
  r"With $x \to \frac{\pi}{2} - x$, $\log_e(\tan x)$ becomes $\log_e(\cot x) = -\log_e(\tan x)$. So $I = -I$, giving $I = 0$.",
  r"Confusing the $\log_e(\tan x)$ integral with the $\log_e(\sin x)$ result.",
  "U08-D-king-logtan", "One property; recognising the integrand changes sign.",
  check=lambda: NI(log(tan(x)), 0, pi/2), values=[0, pi/2*log(2), -pi/2*log(2), pi/4],
  cognitive="Understanding", source_class=SC)

# ---------------------------------------------------------------- 009
q("U08-D-009", TOP_PROP, "King's property with algebraic integrand", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{2}^{4} \frac{\sqrt{x}}{\sqrt{x} + \sqrt{6 - x}}\,dx$ is",
  r"$1$",
  [(r"$2$", r"Adds the two forms to get $2I = 4 - 2 = 2$ and forgets to divide by $2$."),
   (r"$\frac{1}{2}$", r"Divides the interval length by $4$, halving once more after $2I = 2$."),
   (r"$3$", r"Answers with the midpoint $\frac{2 + 4}{2}$ of the interval.")],
  r"Replacing $x$ by $2 + 4 - x = 6 - x$ gives $I = \int_2^4 \frac{\sqrt{6 - x}}{\sqrt{6 - x} + \sqrt{x}}\,dx$. Adding, $2I = \int_2^4 1\,dx = 2$, so $I = 1$.",
  "Forgetting to halve after adding the two forms.",
  "U08-D-king-ratio", "One property applied once.",
  check=lambda: integrate(sqrt(x)/(sqrt(x) + sqrt(6 - x)), (x, 2, 4)).evalf(30), values=[1, 2, Rational(1, 2), 3],
  numerical=dict(question=r"The value of $\displaystyle\int_{2}^{4} \frac{\sqrt{x}}{\sqrt{x} + \sqrt{6 - x}}\,dx$ is", answer=1),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 010
def _c010():
    F = integrate(1/t, (t, xp, xp**2))
    return simplify(diff(F, xp)).subs(xp, x)
q("U08-D-010", TOP_VAR, "Leibniz rule with both limits variable", "Easy", "Single-step computation MCQ",
  r"For $x > 1$, let $F(x) = \displaystyle\int_{x}^{x^2} \frac{dt}{t}$. Then $F'(x)$ equals",
  r"$\frac{1}{x}$",
  [(r"$\frac{1 - x}{x^2}$", r"Omits the chain factor $2x$ for the upper limit: $\frac{1}{x^2} - \frac{1}{x}$."),
   (r"$\frac{3}{x}$", r"Adds the lower-limit term: $\frac{2x}{x^2} + \frac{1}{x}$."),
   (r"$\frac{2}{x}$", r"Differentiates only the upper-limit term $\frac{2x}{x^2}$ and ignores the variable lower limit.")],
  r"By the Leibniz rule, $F'(x) = \frac{1}{x^2}\cdot 2x - \frac{1}{x}\cdot 1 = \frac{2}{x} - \frac{1}{x} = \frac{1}{x}$. (Directly, $F(x) = \log_e x^2 - \log_e x = \log_e x$.)",
  "Dropping the chain factor or the sign of the lower-limit term.",
  "U08-D-leibniz-two-limits", "Single application of the two-limit rule.",
  check=_c010, values=[1/x, (1 - x)/x**2, 3/x, 2/x], cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 011
def _c011():
    G = x**2 + x*sin(x)
    return diff(G, x).subs(x, pi/3)
q("U08-D-011", TOP_EQ, "Recovering f from its integral function", "Easy", "Single-step computation MCQ",
  r"A continuous function $f$ satisfies $\displaystyle\int_{0}^{x} f(t)\,dt = x^2 + x\sin x$ for all real $x$. Then $f\!\left(\frac{\pi}{3}\right)$ equals",
  r"$\frac{5\pi}{6} + \frac{\sqrt{3}}{2}$",
  [(r"$\frac{2\pi}{3} + \frac{\sqrt{3}}{2}$", r"Differentiates $x\sin x$ as $\sin x$ only, losing the $x\cos x$ term: $\frac{2\pi}{3} + \frac{\sqrt{3}}{2}$."),
   (r"$\frac{5\pi}{6}$", r"Differentiates $x\sin x$ as $x\cos x$ only, losing the $\sin x$ term: $\frac{2\pi}{3} + \frac{\pi}{6}$."),
   (r"$\frac{\pi^2}{9} + \frac{\sqrt{3}\pi}{6}$", r"Takes $f$ to be the right-hand side itself and evaluates $x^2 + x\sin x$ at $\frac{\pi}{3}$.")],
  r"Differentiating both sides, $f(x) = 2x + \sin x + x\cos x$. At $x = \frac{\pi}{3}$: $f = \frac{2\pi}{3} + \frac{\sqrt{3}}{2} + \frac{\pi}{6} = \frac{5\pi}{6} + \frac{\sqrt{3}}{2}$.",
  "Incomplete product rule, or not differentiating the integral equation at all.",
  "U08-D-inteq-differentiate", "One differentiation with the product rule.",
  check=_c011, values=[5*pi/6 + sqrt(3)/2, 2*pi/3 + sqrt(3)/2, 5*pi/6, pi**2/9 + sqrt(3)*pi/6],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 012
def _c012():
    f = Rational(7, 4) + sin(pi*x/2)          # a sample continuous function with period 4 and integral 7 over a period
    assert simplify(f.subs(x, x + 4) - f) == 0 and integrate(f, (x, 0, 4)) == 7
    return integrate(f, (x, -2, 18))
q("U08-D-012", TOP_PROP, "Integral over several periods with shifted limits", "Easy", "Single-step computation MCQ",
  r"Let $f$ be a continuous function on $\mathbb{R}$ with $f(x + 4) = f(x)$ for all $x$ and $\displaystyle\int_{0}^{4} f(x)\,dx = 7$. Then $\displaystyle\int_{-2}^{18} f(x)\,dx$ equals",
  r"$35$",
  [(r"$\frac{63}{2}$", r"Ignores $[-2, 0]$ and scales proportionally over $[0, 18]$: $\frac{18}{4}\times 7 = \frac{63}{2}$."),
   (r"$28$", r"Counts only the four complete periods $[0, 16]$ inside $[0, 18]$: $4 \times 7$."),
   (r"$42$", r"Counts the points $-2, 2, 6, 10, 14, 18$ as six periods (a fencepost slip): $6 \times 7$.")],
  r"The integral of a periodic function over any interval of length one period is the same, $7$. The interval $[-2, 18]$ has length $20 = 5 \times 4$, so the integral is $5 \times 7 = 35$.",
  "Thinking the periods must start at $0$, or miscounting periods.",
  "U08-D-periodic-shift", "One property (shift invariance over a period).",
  check=_c012, values=[35, Rational(63, 2), 28, 42],
  numerical=dict(question=r"Let $f$ be a continuous function on $\mathbb{R}$ with $f(x + 4) = f(x)$ for all $x$ and $\displaystyle\int_{0}^{4} f(x)\,dx = 7$. Then the value of $\displaystyle\int_{-2}^{18} f(x)\,dx$ is", answer=35),
  cognitive="Understanding", source_class=SC)

# ---------------------------------------------------------------- 013
def _c013():
    a = Symbol('a', positive=True)
    return solve(Eq(integrate(3*x**2 + 2*x, (x, 0, a)), 12), a)[0]
q("U08-D-013", TOP_FTC, "Unknown upper limit", "Easy", "Inverse/parameter MCQ",
  r"If $a > 0$ and $\displaystyle\int_{0}^{a} \left(3x^2 + 2x\right)dx = 12$, then $a$ equals",
  r"$2$",
  [(r"$\frac{5}{3}$", r"Differentiates the integrand and sets $6a + 2 = 12$."),
   (r"$\sqrt[3]{12}$", r"Drops the $2x$ term, solving $a^3 = 12$."),
   (r"$2\sqrt{3}$", r"Drops the $3x^2$ term, solving $a^2 = 12$.")],
  r"$\int_0^a (3x^2 + 2x)\,dx = a^3 + a^2$. Solving $a^3 + a^2 - 12 = 0$: $(a - 2)(a^2 + 3a + 6) = 0$, and the quadratic has no real root, so $a = 2$.",
  "Differentiating in place of integrating, or losing a term.",
  "U08-D-ftc-inverse-limit", "One antiderivative and a cubic with an obvious root.",
  check=_c013, values=[2, Rational(5, 3), 12**Rational(1, 3), 2*sqrt(3)],
  numerical=dict(question=r"If $a > 0$ and $\displaystyle\int_{0}^{a} \left(3x^2 + 2x\right)dx = 12$, then the value of $a$ is", answer=2),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 014
q("U08-D-014", TOP_MOD, "Exponential of a modulus", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{-1}^{1} e^{|x|}\,dx$ is",
  r"$2(e - 1)$",
  [(r"$e - \frac{1}{e}$", r"Ignores the modulus and evaluates $\int_{-1}^1 e^x\,dx$."),
   (r"$e - 1$", r"Uses the even-function property but forgets the factor $2$."),
   (r"$2e$", r"Doubles $\int_0^1 e^x\,dx$ but evaluates it as $e$, forgetting the lower limit $e^0 = 1$.")],
  r"$e^{|x|}$ is even, so the integral is $2\int_0^1 e^x\,dx = 2(e - 1)$.",
  "Dropping the modulus or the factor $2$ for an even integrand.",
  "U08-D-even-modulus-exp", "One property, one antiderivative.",
  check=lambda: pint(exp(Abs(x)), -1, 1), values=[2*(E - 1), E - 1/E, E - 1, 2*E],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 015
def _c015():
    s1 = integrate(sin(x)**3*cos(x)**2, (x, -pi, pi)) == 0
    s2 = pint(x**2*Abs(x), -1, 1) == 0
    return (bool(s1), bool(s2))
q("U08-D-015", TOP_PROP, "Odd and even integrands", "Easy", "Statement-based MCQ",
  r"Statement I: $\displaystyle\int_{-\pi}^{\pi} \sin^3 x\cos^2 x\,dx = 0$. Statement II: $\displaystyle\int_{-1}^{1} x^2|x|\,dx = 0$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Treats $x^2|x|$ as odd; it is even (both factors are even), so its integral is $\frac{1}{2}$."),
   (ST_FF, r"Thinks $\sin^3 x\cos^2 x$ is even because of $\cos^2 x$; the product of an odd and an even function is odd."),
   (ST_FT, r"Reverses the parity of both integrands.")],
  r"$\sin^3 x\cos^2 x$ is odd, so Statement I holds. $x^2|x|$ is even and positive away from $0$, so $\int_{-1}^1 x^2|x|\,dx = 2\int_0^1 x^3\,dx = \frac{1}{2} \ne 0$; Statement II is false.",
  "Misjudging the parity of a product involving $|x|$.",
  "U08-D-statement-odd-even", "Parity of two products; one quick evaluation.",
  check=_c015, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Understanding", source_class=SC)

# ---------------------------------------------------------------- 016
def _c016():
    f = Piecewise((x**2, x <= 1), (2*x - 1, True))
    return integrate(f, (x, 0, 3))
q("U08-D-016", TOP_FTC, "Piecewise integrand", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = x^2$ for $x \le 1$ and $f(x) = 2x - 1$ for $x > 1$. Then $\displaystyle\int_{0}^{3} f(x)\,dx$ equals",
  r"$\frac{19}{3}$",
  [(r"$9$", r"Uses $f(x) = x^2$ on all of $[0, 3]$."),
   (r"$6$", r"Uses $f(x) = 2x - 1$ on all of $[0, 3]$: $[x^2 - x]_0^3 = 6$."),
   (r"$\frac{16}{3}$", r"Evaluates $[x^2 - x]_1^3$ as $6 - 1 = 5$, subtracting only $1^2$ at the lower limit, then adds $\frac{1}{3}$.")],
  r"Split at $x = 1$: $\int_0^1 x^2\,dx = \frac{1}{3}$ and $\int_1^3 (2x - 1)\,dx = [x^2 - x]_1^3 = 6 - 0 = 6$. Total $\frac{19}{3}$.",
  "Not splitting at the point where the formula changes.",
  "U08-D-ftc-piecewise", "One split, two elementary integrals.",
  check=_c016, values=[Rational(19, 3), 9, 6, Rational(16, 3)], cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 017
q("U08-D-017", TOP_PROP, "King's property on a polynomial", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{1} x(1 - x)^{9}\,dx$ is",
  r"$\frac{1}{110}$",
  [(r"$\frac{1}{90}$", r"After $x \to 1 - x$, integrates $x^9 - x^{10}$ as $\frac{1}{9} - \frac{1}{10}$, dividing by the old exponents."),
   (r"$\frac{21}{110}$", r"Adds the two terms: $\frac{1}{10} + \frac{1}{11}$."),
   (r"$\frac{1}{10}$", r"Integrates only the $x^9$ term and drops $-x^{10}$.")],
  r"Using $\int_0^1 f(x)\,dx = \int_0^1 f(1 - x)\,dx$, the integral is $\int_0^1 (1 - x)x^9\,dx = \frac{1}{10} - \frac{1}{11} = \frac{1}{110}$.",
  "Mishandling the power rule after the substitution.",
  "U08-D-king-poly", "One property avoids a ninth-power expansion.",
  check=lambda: integrate(x*(1 - x)**9, (x, 0, 1)), values=[Rational(1, 110), Rational(1, 90), Rational(21, 110), Rational(1, 10)],
  cognitive="Application", source_class=SC)


# ================================================================ MEDIUM
# ---------------------------------------------------------------- 018
q("U08-D-018", TOP_PROP, "Symmetric interval with an exponential denominator", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{-\pi/2}^{\pi/2} \frac{\cos x}{1 + e^{x}}\,dx$ is",
  r"$1$",
  [(r"$2$", r"Adds $I$ and its $x \to -x$ form to get $2I = \int_{-\pi/2}^{\pi/2} \cos x\,dx = 2$ but forgets to halve."),
   (r"$0$", r"Assumes the integrand is odd because of the $e^x$ in the denominator."),
   (r"$\frac{1}{2}$", r"After $2I = \int_{-\pi/2}^{\pi/2}\cos x\,dx$, evaluates only $\int_0^{\pi/2} \cos x\,dx = 1$ and then halves.")],
  r"Replacing $x$ by $-x$: $I = \int_{-\pi/2}^{\pi/2} \frac{e^x\cos x}{1 + e^x}\,dx$. Adding to the original, $2I = \int_{-\pi/2}^{\pi/2} \cos x\,dx = 2$, so $I = 1$.",
  r"Using the odd-function rule on an integrand that is neither odd nor even.",
  "U08-D-even-pair-exp", r"Needs the $x \to -x$ pairing and recognition that $\frac{1}{1+e^x} + \frac{e^x}{1+e^x} = 1$.",
  check=lambda: NI(cos(x)/(1 + exp(x)), -pi/2, pi/2), values=[1, 2, 0, Rational(1, 2)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 019
q("U08-D-019", TOP_PROP, "King's property with a factor x", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi} \frac{x\sin x}{1 + \cos^2 x}\,dx$ is",
  r"$\frac{\pi^2}{4}$",
  [(r"$\frac{\pi^2}{2}$", r"Gets $2I = \pi\int_0^{\pi}\frac{\sin x}{1 + \cos^2 x}\,dx = \frac{\pi^2}{2}$ and forgets to halve."),
   (r"$\frac{\pi}{4}$", r"Loses the factor $\pi$ when adding the two forms, writing $2I = \int_0^{\pi}\frac{\sin x}{1 + \cos^2 x}\,dx = \frac{\pi}{2}$."),
   (r"$\frac{\pi^2}{8}$", r"Evaluates $\int_0^{\pi}\frac{\sin x}{1 + \cos^2 x}\,dx$ as $\tan^{-1}(1) - \tan^{-1}(0) = \frac{\pi}{4}$ (wrong limits for $u = \cos x$).")],
  r"With $x \to \pi - x$, $I = \int_0^{\pi}\frac{(\pi - x)\sin x}{1 + \cos^2 x}\,dx$, so $2I = \pi\int_0^{\pi}\frac{\sin x}{1 + \cos^2 x}\,dx$. Put $u = \cos x$: $\int_{-1}^{1}\frac{du}{1 + u^2} = \frac{\pi}{2}$. Hence $I = \frac{\pi}{2}\cdot\frac{\pi}{2} = \frac{\pi^2}{4}$.",
  r"Mishandling the limits $u = 1$ to $u = -1$ after $u = \cos x$.",
  "U08-D-king-x-times", "King's property plus a substitution with changed limits.",
  check=lambda: NI(x*sin(x)/(1 + cos(x)**2), 0, pi), values=[pi**2/4, pi**2/2, pi/4, pi**2/8],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 020
q("U08-D-020", TOP_MOD, "Greatest integer of a quadratic", "Medium", "Multi-step computation MCQ",
  r"If $[\,\cdot\,]$ denotes the greatest integer function, then $\displaystyle\int_{0}^{2} [x^2]\,dx$ equals",
  r"$5 - \sqrt{2} - \sqrt{3}$",
  [(r"$3 - \sqrt{2}$", r"Misses the break at $x = \sqrt{3}$ and uses $[x^2] = 2$ on all of $[\sqrt{2}, 2)$: $(\sqrt{2} - 1) + 2(2 - \sqrt{2})$."),
   (r"$2\sqrt{3} - \sqrt{2} - 1$", r"Stops at $x = \sqrt{3}$ and leaves out the piece $[\sqrt{3}, 2)$ where $[x^2] = 3$."),
   (r"$6 - \sqrt{2} - \sqrt{3}$", r"Takes $[x^2] = 1$ on $[0, 1)$ as well, adding an extra $1$.")],
  r"$[x^2] = 0, 1, 2, 3$ on $[0, 1), [1, \sqrt{2}), [\sqrt{2}, \sqrt{3}), [\sqrt{3}, 2)$. So the integral is $(\sqrt{2} - 1) + 2(\sqrt{3} - \sqrt{2}) + 3(2 - \sqrt{3}) = 5 - \sqrt{2} - \sqrt{3}$.",
  r"Using integer break points in $x$ in place of the points where $x^2$ is an integer.",
  "U08-D-floor-nonlinear", "Four pieces with irrational break points.",
  check=lambda: pint(floor(x**2), 0, 2), values=[5 - sqrt(2) - sqrt(3), 3 - sqrt(2), 2*sqrt(3) - sqrt(2) - 1, 6 - sqrt(2) - sqrt(3)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 021
q("U08-D-021", TOP_MOD, "Modulus of a trigonometric difference", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi/2} \left|\sin x - \cos x\right| dx$ is",
  r"$2\sqrt{2} - 2$",
  [(r"$0$", r"Ignores the modulus; $\int_0^{\pi/2} (\sin x - \cos x)\,dx = 0$."),
   (r"$\sqrt{2} - 1$", r"Evaluates only the piece on $\left[0, \frac{\pi}{4}\right]$ and does not double it."),
   (r"$2$", r"Replaces $|\sin x - \cos x|$ by $\sin x + \cos x$, whose integral is $2$.")],
  r"$\cos x \ge \sin x$ on $\left[0, \frac{\pi}{4}\right]$ and the reverse on $\left[\frac{\pi}{4}, \frac{\pi}{2}\right]$. Each piece equals $[\sin x + \cos x]_0^{\pi/4} = \sqrt{2} - 1$, so the total is $2\sqrt{2} - 2$.",
  "Not splitting at the point where the expression inside the modulus vanishes.",
  "U08-D-modulus-trig", "Locating the sign change and two evaluations.",
  check=lambda: pint(Abs(sin(x) - cos(x)), 0, pi/2), values=[2*sqrt(2) - 2, 0, sqrt(2) - 1, 2],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 022
q("U08-D-022", TOP_PROP, "Using the standard log-sine integral", "Medium", "Multi-step computation MCQ",
  r"Given that $\displaystyle\int_{0}^{\pi/2} \log_e(\sin x)\,dx = -\frac{\pi}{2}\log_e 2$, the value of $\displaystyle\int_{0}^{\pi/2} \log_e(\sin 2x)\,dx$ is",
  r"$-\frac{\pi}{2}\log_e 2$",
  [(r"$-\pi\log_e 2$", r"Writes $\log_e(\sin 2x) = \log_e(\sin x) + \log_e(\cos x)$, dropping the $\log_e 2$ term."),
   (r"$0$", r"Keeps the $\log_e 2$ term but uses only one of $\log_e(\sin x)$ and $\log_e(\cos x)$: $\frac{\pi}{2}\log_e 2 - \frac{\pi}{2}\log_e 2 = 0$."),
   (r"$-\frac{\pi}{4}\log_e 2$", r"Puts $u = 2x$ and takes $\frac{1}{2}\int_0^{\pi}\log_e(\sin u)\,du$ as $\frac{1}{2}\int_0^{\pi/2}\log_e(\sin u)\,du$, missing the doubling.")],
  r"$\log_e(\sin 2x) = \log_e 2 + \log_e(\sin x) + \log_e(\cos x)$. By King's property $\int_0^{\pi/2}\log_e(\cos x)\,dx = \int_0^{\pi/2}\log_e(\sin x)\,dx$. So the integral is $\frac{\pi}{2}\log_e 2 - \frac{\pi}{2}\log_e 2 - \frac{\pi}{2}\log_e 2 = -\frac{\pi}{2}\log_e 2$.",
  r"Forgetting the constant $\log_e 2$ in $\log_e(2\sin x\cos x)$.",
  "U08-D-king-logsin", "Log identity, King's property and a given standard value combined.",
  check=lambda: NI(log(sin(2*x)), 0, pi/2), values=[-pi/2*log(2), -pi*log(2), 0, -pi/4*log(2)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 023
def _c023():
    F = Integral(log(t), (t, x**2, x**3))
    return diff(F, x).doit().subs(x, E)
q("U08-D-023", TOP_VAR, "Leibniz rule with logarithmic integrand", "Medium", "Multi-step computation MCQ",
  r"For $x > 1$, let $F(x) = \displaystyle\int_{x^2}^{x^3} \log_e t\,dt$. Then $F'(e)$ equals",
  r"$9e^2 - 4e$",
  [(r"$3e^2 - 2e$", r"Keeps the chain factors $3x^2$ and $2x$ but writes $\log_e x$ in place of $\log_e x^3$ and $\log_e x^2$."),
   (r"$9e^2 + 4e$", r"Adds the lower-limit term in place of subtracting it."),
   (r"$9e^2$", r"Uses only the upper-limit term $3x^2\log_e x^3$ and ignores the variable lower limit.")],
  r"$F'(x) = \log_e(x^3)\cdot 3x^2 - \log_e(x^2)\cdot 2x = 9x^2\log_e x - 4x\log_e x$. At $x = e$, $\log_e e = 1$, so $F'(e) = 9e^2 - 4e$.",
  "Mishandling the lower-limit term or the logarithm of a power.",
  "U08-D-leibniz-two-limits", "Two-limit Leibniz rule with chain factors and log of powers.",
  check=_c023, values=[9*E**2 - 4*E, 3*E**2 - 2*E, 9*E**2 + 4*E, 9*E**2],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 024
def _c024():
    k = Symbol('k')
    ks = solve(Eq(k, integrate(t*(t + k), (t, 0, 1))), k)[0]
    return (x + ks).subs(x, 2)
q("U08-D-024", TOP_EQ, "Integral equation with a constant definite integral", "Medium", "Multi-step computation MCQ",
  r"A continuous function $f$ satisfies $f(x) = x + \displaystyle\int_{0}^{1} t\,f(t)\,dt$ for all real $x$. Then $f(2)$ equals",
  r"$\frac{8}{3}$",
  [(r"$\frac{7}{3}$", r"Writes $\int_0^1 t f(t)\,dt = \int_0^1 t^2\,dt = \frac{1}{3}$, ignoring the constant inside $f$."),
   (r"$3$", r"Sets up $k = \int_0^1 t(t + k)\,dt$ but evaluates $\int_0^1 t^2\,dt$ as $\frac{1}{2}$, so $k = \frac{1}{2} + \frac{k}{2}$ and $k = 1$."),
   (r"$\frac{20}{9}$", r"Sign slip in solving $k = \frac{1}{3} + \frac{k}{2}$: writes $\frac{3k}{2} = \frac{1}{3}$, so $k = \frac{2}{9}$.")],
  r"The integral is a constant $k$, so $f(x) = x + k$. Then $k = \int_0^1 t(t + k)\,dt = \frac{1}{3} + \frac{k}{2}$, giving $k = \frac{2}{3}$. Hence $f(2) = 2 + \frac{2}{3} = \frac{8}{3}$.",
  "Forgetting that the unknown constant also appears inside the integral.",
  "U08-D-inteq-constant", "Recognise the constant, set up and solve a linear equation.",
  check=_c024, values=[Rational(8, 3), Rational(7, 3), 3, Rational(20, 9)], cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 025
q("U08-D-025", TOP_PROP, "Periodic modulus integrand over a non-integral number of periods", "Medium", "Multi-step computation MCQ",
  r"The value of $I = \displaystyle\int_{0}^{10\pi + \frac{\pi}{3}} |\sin x|\,dx$ is",
  r"$\frac{41}{2}$",
  [(r"$\frac{43}{2}$", r"Evaluates the leftover piece as $1 + \cos\frac{\pi}{3} = \frac{3}{2}$, a sign slip in $[-\cos x]_0^{\pi/3}$."),
   (r"$20$", r"Counts the $10$ full periods and drops the leftover $\left[10\pi, 10\pi + \frac{\pi}{3}\right]$."),
   (r"$20 + \frac{\sqrt{3}}{2}$", r"Evaluates the leftover piece as $\sin\frac{\pi}{3}$ in place of $1 - \cos\frac{\pi}{3}$.")],
  r"$|\sin x|$ has period $\pi$ and $\int_0^{\pi}|\sin x|\,dx = 2$, so the first $10\pi$ contribute $20$. The rest equals $\int_0^{\pi/3}\sin x\,dx = 1 - \frac{1}{2} = \frac{1}{2}$. Hence $I = \frac{41}{2}$.",
  "Dropping or mis-evaluating the partial period.",
  "U08-D-periodic-modsin", "Periodicity plus a partial period evaluation.",
  check=lambda: pint(Abs(sin(x)), 0, 10*pi + pi/3), values=[Rational(41, 2), Rational(43, 2), 20, 20 + sqrt(3)/2],
  numerical=dict(question=r"If $I = \displaystyle\int_{0}^{10\pi + \frac{\pi}{3}} |\sin x|\,dx$, then the value of $2I$ is", answer=41),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 026
q("U08-D-026", TOP_PROP, "King's property with a logarithm", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi/4} \log_e(1 + \tan x)\,dx$ is",
  r"$\frac{\pi}{8}\log_e 2$",
  [(r"$\frac{\pi}{4}\log_e 2$", r"Reaches $2I = \frac{\pi}{4}\log_e 2$ and forgets to halve."),
   (r"$\frac{\pi}{16}\log_e 2$", r"Halves twice after reaching $2I = \frac{\pi}{4}\log_e 2$."),
   (r"$\frac{\pi}{2}\log_e 2$", r"Integrates the constant $\log_e 2$ over $\left[0, \frac{\pi}{2}\right]$ (the usual King's interval) and does not halve.")],
  r"With $x \to \frac{\pi}{4} - x$, $1 + \tan\left(\frac{\pi}{4} - x\right) = \frac{2}{1 + \tan x}$. So $I = \int_0^{\pi/4}\left(\log_e 2 - \log_e(1 + \tan x)\right)dx = \frac{\pi}{4}\log_e 2 - I$, giving $I = \frac{\pi}{8}\log_e 2$.",
  "Forgetting to halve, or using the wrong interval length.",
  "U08-D-king-ln1tan", "King's property plus a tangent identity.",
  check=lambda: NI(log(1 + tan(x)), 0, pi/4), values=[pi/8*log(2), pi/4*log(2), pi/16*log(2), pi/2*log(2)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 027
q("U08-D-027", TOP_PROP, "Symmetric interval with base-2 exponential", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{-\pi/2}^{\pi/2} \frac{\sin^2 x}{1 + 2^{x}}\,dx$ is",
  r"$\frac{\pi}{4}$",
  [(r"$\frac{\pi}{2}$", r"Reaches $2I = \int_{-\pi/2}^{\pi/2}\sin^2 x\,dx = \frac{\pi}{2}$ and forgets to halve."),
   (r"$0$", r"Treats the integrand as odd."),
   (r"$\frac{\pi}{8}$", r"After $2I = \int_{-\pi/2}^{\pi/2}\sin^2 x\,dx$, evaluates only $\int_0^{\pi/2}\sin^2 x\,dx = \frac{\pi}{4}$ and halves.")],
  r"Under $x \to -x$, $\frac{1}{1 + 2^{-x}} = \frac{2^x}{1 + 2^x}$, so adding the two forms gives $2I = \int_{-\pi/2}^{\pi/2}\sin^2 x\,dx = 2\cdot\frac{\pi}{4} = \frac{\pi}{2}$. Hence $I = \frac{\pi}{4}$.",
  "Halving errors after pairing $x$ with $-x$.",
  "U08-D-even-pair-exp", "Pairing $x$ with $-x$ and a standard trigonometric integral.",
  check=lambda: NI(sin(x)**2/(1 + 2**x), -pi/2, pi/2), values=[pi/4, pi/2, 0, pi/8],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 028
def _c028():
    F = Function('f')
    # differentiate both sides of  int_0^x f = x - int_0^x t f(t) dt
    eqn = Eq(F(x), 1 - x*F(x))
    fx = solve(eqn, F(x))[0]
    assert simplify(integrate(fx.subs(x, t), (t, 0, x)) - x + integrate(t*fx.subs(x, t), (t, 0, x))) == 0
    return fx.subs(x, 3)
q("U08-D-028", TOP_EQ, "Integral equation solved by differentiation", "Medium", "Multi-step computation MCQ",
  r"A continuous function $f : [0, \infty) \to \mathbb{R}$ satisfies $\displaystyle\int_{0}^{x} f(t)\,dt = x - \int_{0}^{x} t\,f(t)\,dt$ for all $x \ge 0$. Then $f(3)$ equals",
  r"$\frac{1}{4}$",
  [(r"$-\frac{1}{2}$", r"Sign slip in differentiating: writes $f(x) = 1 + x f(x)$, so $f(x) = \frac{1}{1 - x}$."),
   (r"$\frac{1}{2}$", r"Differentiates $\int_0^x t f(t)\,dt$ as $f(x)$, dropping the factor $t = x$: $f = 1 - f$."),
   (r"$0$", r"Forgets the derivative of the term $x$ on the right: $f(x) = -x f(x)$, so $f \equiv 0$.")],
  r"Differentiating, $f(x) = 1 - x f(x)$, so $f(x) = \frac{1}{1 + x}$. (Check: $\int_0^x \frac{dt}{1+t} + \int_0^x \frac{t\,dt}{1+t} = \int_0^x 1\,dt = x$.) Hence $f(3) = \frac{1}{4}$.",
  "Mis-differentiating an integral whose integrand contains $t$ as a factor.",
  "U08-D-inteq-differentiate", "Differentiate, solve a linear equation in $f(x)$, evaluate.",
  check=_c028, values=[Rational(1, 4), Rational(-1, 2), Rational(1, 2), 0],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 029
q("U08-D-029", TOP_VAR, "Limit of a ratio involving an integral", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\lim_{x \to 0^{+}} \frac{\int_{0}^{x^2} \sin\sqrt{t}\,dt}{x^3}$ is",
  r"$\frac{2}{3}$",
  [(r"$\frac{1}{2}$", r"Replaces $\sin\sqrt{t}$ by $\sqrt{t}$ near $0$ but integrates $\sqrt{t}$ as $\frac{t^{3/2}}{2}$, so the numerator is about $\frac{x^3}{2}$."),
   (r"$0$", r"Differentiates the numerator as $2x\sin(x^2)$, substituting $x^2$ for $\sqrt{t}$, which gives $\frac{2x^3}{3x^2} \to 0$."),
   (r"$2$", r"Differentiates the denominator $x^3$ as $x^2$, getting $\frac{2x\sin x}{x^2} \to 2$.")],
  r"Both numerator and denominator tend to $0$. By L'Hospital's rule and the Leibniz rule, the numerator's derivative is $\sin\sqrt{x^2}\cdot 2x = 2x\sin x$ for $x > 0$. So the limit is $\lim \frac{2x\sin x}{3x^2} = \frac{2}{3}$.",
  r"Evaluating the integrand at the wrong point or dropping the chain factor.",
  "U08-D-limit-lhopital", "L'Hospital's rule combined with differentiating an integral.",
  check=lambda: limit(integrate(sin(sqrt(t)), (t, 0, x**2))/x**3, x, 0, '+'), values=[Rational(2, 3), Rational(1, 2), 0, 2],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 030
q("U08-D-030", TOP_MOD, "Greatest integer of a trigonometric function", "Medium", "Multi-step computation MCQ",
  r"If $[\,\cdot\,]$ denotes the greatest integer function, then $\displaystyle\int_{0}^{\pi} [2\sin x]\,dx$ equals",
  r"$\frac{2\pi}{3}$",
  [(r"$\pi$", r"Takes $[2\sin x] = 1$ on the whole of $(0, \pi)$, ignoring where $2\sin x < 1$."),
   (r"$\frac{4\pi}{3}$", r"Uses the right interval $\left[\frac{\pi}{6}, \frac{5\pi}{6}\right]$ but assigns the value $2$ there."),
   (r"$\frac{\pi}{3}$", r"Takes $2\sin x \ge 1$ only on $\left[\frac{\pi}{6}, \frac{\pi}{2}\right]$, forgetting the symmetric part up to $\frac{5\pi}{6}$.")],
  r"On $(0, \pi)$, $0 < 2\sin x \le 2$, and $2\sin x \ge 1$ exactly on $\left[\frac{\pi}{6}, \frac{5\pi}{6}\right]$; the value $2$ occurs only at $x = \frac{\pi}{2}$, which does not affect the integral. So the integral is $1 \cdot \left(\frac{5\pi}{6} - \frac{\pi}{6}\right) = \frac{2\pi}{3}$.",
  "Not locating where the inner function crosses an integer.",
  "U08-D-floor-trig", "Find the solution set of $\\sin x \\ge \\frac{1}{2}$ and interpret a step function.",
  check=lambda: pint(floor(2*sin(x)), 0, pi), values=[2*pi/3, pi, 4*pi/3, pi/3],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 031
def _c031():
    a = Symbol('a', real=True)
    g_in = integrate(a - x, (x, 0, a)) + integrate(x - a, (x, a, 1))      # valid for 0 <= a <= 1
    crit = [c for c in solve(diff(g_in, a), a) if 0 <= c <= 1]
    inner = min(g_in.subs(a, c) for c in crit + [0, 1])
    # for a < 0 the value is 1/2 - a > 1/2, for a > 1 it is a - 1/2 > 1/2
    return Min(inner, Rational(1, 2))
q("U08-D-031", TOP_MOD, "Minimising an integral of a modulus over a parameter", "Medium", "Multi-step computation MCQ",
  r"For real $a$, let $g(a) = \displaystyle\int_{0}^{1} |x - a|\,dx$. The minimum value of $g(a)$ is",
  r"$\frac{1}{4}$",
  [(r"$\frac{1}{2}$", r"Assumes the minimum occurs at an end point, $a = 0$ or $a = 1$, where $g = \frac{1}{2}$."),
   (r"$\frac{1}{8}$", r"Takes $a = \frac{1}{2}$ but integrates only over $\left[0, \frac{1}{2}\right]$, forgetting the matching part on $\left[\frac{1}{2}, 1\right]$."),
   (r"$\frac{1}{3}$", r"Takes the parameter at the end point $a = 0$ and also replaces $|x|$ by $x^2$, getting $\int_0^1 x^2\,dx = \frac{1}{3}$.")],
  r"For $0 \le a \le 1$, $g(a) = \int_0^a (a - x)\,dx + \int_a^1 (x - a)\,dx = \frac{a^2}{2} + \frac{(1 - a)^2}{2} = a^2 - a + \frac{1}{2}$, minimised at $a = \frac{1}{2}$ with value $\frac{1}{4}$. For $a$ outside $[0, 1]$, $g(a) = \left|a - \frac{1}{2}\right| > \frac{1}{2}$. So the minimum is $\frac{1}{4}$.",
  "Not treating the parameter's position relative to the limits by cases.",
  "U08-D-modulus-param-min", "Casework on the parameter, then minimising a quadratic.",
  check=_c031, values=[Rational(1, 4), Rational(1, 2), Rational(1, 8), Rational(1, 3)],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 032
q("U08-D-032", TOP_PROP, "King's property with a factor x and a trigonometric denominator", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi} \frac{x}{1 + \sin x}\,dx$ is",
  r"$\pi$",
  [(r"$2\pi$", r"Reaches $2I = \pi\int_0^{\pi}\frac{dx}{1 + \sin x} = 2\pi$ and forgets to halve."),
   (r"$\frac{\pi}{2}$", r"Evaluates $\int_0^{\pi}\frac{dx}{1 + \sin x}$ only over $\left[0, \frac{\pi}{2}\right]$, getting $1$, so $I = \frac{\pi}{2}\cdot 1$."),
   (r"$2$", r"Reports $\int_0^{\pi}\frac{dx}{1 + \sin x} = 2$ and omits the factor $\frac{\pi}{2}$ from King's property.")],
  r"With $x \to \pi - x$, $2I = \pi\int_0^{\pi}\frac{dx}{1 + \sin x}$. Using $\frac{1}{1 + \sin x} = \frac{1 - \sin x}{\cos^2 x}$, an antiderivative is $\tan x - \sec x = -\frac{\cos x}{1 + \sin x}$, which is continuous on $[0, \pi]$, so $\int_0^{\pi}\frac{dx}{1 + \sin x} = 1 - (-1) = 2$. Hence $I = \frac{\pi}{2}\cdot 2 = \pi$.",
  "Dropping the factor $\\frac{\\pi}{2}$ or the halving step.",
  "U08-D-king-x-times", "King's property, then a trigonometric integral across $x = \\frac{\\pi}{2}$.",
  check=lambda: NI(x/(1 + sin(x)), 0, pi), values=[pi, 2*pi, pi/2, 2],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 033
def _c033():
    Fp = diff(Integral((t - 1)*(t - 2)*exp(-t**2), (t, 0, x)), x).doit()
    crit = solve(Fp, x)
    mins = [c for c in crit if diff(Fp, x).subs(x, c) > 0]
    return mins[0]
q("U08-D-033", TOP_VAR, "Extremum of an integral function", "Medium", "Multi-step computation MCQ",
  r"Let $F(x) = \displaystyle\int_{0}^{x} (t - 1)(t - 2)e^{-t^2}\,dt$ for real $x$. The point of local minimum of $F$ is $x =$",
  r"$2$",
  [(r"$1$", r"Takes the first critical point; at $x = 1$, $F'$ changes from positive to negative, so it is a local maximum."),
   (r"$\frac{3}{2}$", r"Minimises the quadratic factor $(x - 1)(x - 2)$ in place of finding where $F'$ changes sign."),
   (r"$0$", r"Uses the lower limit, where $F(0) = 0$, as the minimum.")],
  r"$F'(x) = (x - 1)(x - 2)e^{-x^2}$, which is zero at $x = 1, 2$. Since $e^{-x^2} > 0$, $F'$ goes from $+$ to $-$ at $x = 1$ and from $-$ to $+$ at $x = 2$. So $F$ has a local minimum at $x = 2$.",
  "Confusing the local maximum with the local minimum, or minimising the integrand.",
  "U08-D-varlimit-extremum", "Leibniz rule plus a sign chart.",
  check=_c033, values=[2, 1, Rational(3, 2), 0],
  numerical=dict(question=r"Let $F(x) = \displaystyle\int_{0}^{x} (t - 1)(t - 2)e^{-t^2}\,dt$ for real $x$. If $F$ has a local minimum at $x = p$, then $p$ is", answer=2),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 034
def _c034():
    F = Function('f')
    lhs = diff(Integral(F(t), (t, 0, xp**2)), xp).doit()
    sol = solve(Eq(lhs, diff(xp**3, xp)), F(xp**2))[0]
    return sol.subs(xp, 2)            # x = 2 gives x^2 = 4
q("U08-D-034", TOP_EQ, "Integral equation with a squared upper limit", "Medium", "Multi-step computation MCQ",
  r"A continuous function $f : [0, \infty) \to \mathbb{R}$ satisfies $\displaystyle\int_{0}^{x^2} f(t)\,dt = x^3$ for all $x \ge 0$. Then $f(4)$ equals",
  r"$3$",
  [(r"$12$", r"Omits the chain factor $2x$, writing $f(x^2) = 3x^2$, and puts $x = 2$."),
   (r"$6$", r"Differentiates to $f(x) = \frac{3x^2}{2x} = \frac{3x}{2}$, treating $f(x^2)$ as $f(x)$, and puts $x = 4$."),
   (r"$48$", r"Multiplies by the chain factor in place of dividing: $f(x^2) = 3x^2 \cdot 2x$ at $x = 2$.")],
  r"Differentiating, $f(x^2)\cdot 2x = 3x^2$, so $f(x^2) = \frac{3x}{2}$ for $x > 0$. For $f(4)$ take $x = 2$: $f(4) = 3$. (Equivalently $f(u) = \frac{3\sqrt{u}}{2}$.)",
  "Mixing up $f(x^2)$ with $f(x)$, or mishandling the chain factor.",
  "U08-D-inteq-chain", "Differentiate with a chain factor, then invert the argument.",
  check=_c034, values=[3, 12, 6, 48],
  numerical=dict(question=r"A continuous function $f : [0, \infty) \to \mathbb{R}$ satisfies $\displaystyle\int_{0}^{x^2} f(t)\,dt = x^3$ for all $x \ge 0$. Then the value of $f(4)$ is", answer=3),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 035
def _c035():
    a, b = 1, 4
    f = (x - a)*(b - x)                           # satisfies f(a + b - x) = f(x)
    assert simplify(f.subs(x, a + b - x) - f) == 0
    s1 = simplify(integrate(x*f, (x, a, b)) - Rational(a + b, 2)*integrate(f, (x, a, b))) == 0
    s2 = simplify(integrate(x*cos(x)**2, (x, 0, pi)) - pi**2/4) == 0
    return (bool(s1), bool(s2))
q("U08-D-035", TOP_PROP, "King's property with a factor x", "Medium", "Statement-based MCQ",
  r"Statement I: If $f$ is continuous on $[a, b]$ and $f(a + b - x) = f(x)$ for all $x \in [a, b]$, then $\displaystyle\int_{a}^{b} x f(x)\,dx = \frac{a + b}{2}\int_{a}^{b} f(x)\,dx$. Statement II: $\displaystyle\int_{0}^{\pi} x\cos^2 x\,dx = \frac{\pi^2}{4}$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Uses $\int_0^{\pi}\cos^2 x\,dx = \pi$ (forgetting the factor $\frac{1}{2}$ in $\cos^2 x = \frac{1 + \cos 2x}{2}$), so gets $\frac{\pi^2}{2}$ for Statement II."),
   (ST_FT, r"Thinks the factor should be $(a + b)$, not $\frac{a + b}{2}$, forgetting to halve after adding the two forms."),
   (ST_FF, r"Makes both slips: the missing halving in Statement I and a wrong value of $\int_0^{\pi}\cos^2 x\,dx$ in Statement II.")],
  r"Statement I: with $x \to a + b - x$, $I = \int_a^b (a + b - x)f(x)\,dx$, so $2I = (a + b)\int_a^b f$, which is the claim. Statement II: $\cos^2(\pi - x) = \cos^2 x$, so by Statement I the integral is $\frac{\pi}{2}\int_0^{\pi}\cos^2 x\,dx = \frac{\pi}{2}\cdot\frac{\pi}{2} = \frac{\pi^2}{4}$. Both are true.",
  "Forgetting to halve after adding the two King's-property forms.",
  "U08-D-statement-king", "A general property and its application to a specific integral.",
  check=_c035, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Understanding", source_class=SC)

# ---------------------------------------------------------------- 036
q("U08-D-036", TOP_MOD, "Greatest integer plus an odd function", "Medium", "Multi-step computation MCQ",
  r"If $[\,\cdot\,]$ denotes the greatest integer function, then $\displaystyle\int_{-1/2}^{1/2} \left([x] + \log_e\frac{1 + x}{1 - x}\right)dx$ equals",
  r"$-\frac{1}{2}$",
  [(r"$0$", r"Treats $[x]$ as an odd function along with the logarithm, so the whole integral vanishes."),
   (r"$-1$", r"Takes $[x] = -1$ on the whole interval $\left[-\frac{1}{2}, \frac{1}{2}\right]$."),
   (r"$\frac{1}{2}$", r"Takes $[x] = 1$ on $\left(0, \frac{1}{2}\right)$ by rounding up, and $[x] = 0$ on $\left(-\frac{1}{2}, 0\right)$.")],
  r"$\log_e\frac{1 + x}{1 - x}$ is odd, so it contributes $0$. $[x] = -1$ on $\left[-\frac{1}{2}, 0\right)$ and $0$ on $\left[0, \frac{1}{2}\right]$, contributing $-\frac{1}{2}$. Total $-\frac{1}{2}$.",
  r"Assuming $[x]$ is odd.",
  "U08-D-floor-odd-combo", "Combines the odd-function property with a step function.",
  check=lambda: pint(floor(x) + log((1 + x)/(1 - x)), Rational(-1, 2), Rational(1, 2)), values=[Rational(-1, 2), 0, -1, Rational(1, 2)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 037
q("U08-D-037", TOP_PROP, "Periodicity of the fractional part", "Medium", "Multi-step computation MCQ",
  r"If $[x]$ denotes the greatest integer less than or equal to $x$, then $\displaystyle\int_{0}^{50} e^{x - [x]}\,dx$ equals",
  r"$50(e - 1)$",
  [(r"$e^{50} - 1$", r"Ignores $[x]$ and integrates $e^x$ over $[0, 50]$."),
   (r"$25(e - 1)$", r"Takes the period of $x - [x]$ to be $2$, so counts only $25$ periods."),
   (r"$50e$", r"Counts $50$ periods but evaluates $\int_0^1 e^x\,dx$ as $e$, forgetting the lower limit.")],
  r"$x - [x]$ has period $1$, so $e^{x - [x]}$ has period $1$ and equals $e^x$ on $[0, 1)$. Hence the integral is $50\int_0^1 e^x\,dx = 50(e - 1)$.",
  "Ignoring the fractional-part structure or the period length.",
  "U08-D-periodic-fractional", "Periodicity of the fractional part plus one evaluation.",
  check=lambda: pint(exp(x - floor(x)), 0, 50), values=[50*(E - 1), exp(50) - 1, 25*(E - 1), 50*E],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 038
def _c038():
    F = Function('f')
    sol = dsolve(Eq(F(x).diff(x), 1 + F(x)), F(x), ics={F(0): 0}).rhs
    assert simplify(sol - x - integrate(sol.subs(x, t), (t, 0, x))) == 0
    return simplify(sol.subs(x, log(3)))
q("U08-D-038", TOP_EQ, "Integral equation leading to an exponential", "Medium", "Multi-step computation MCQ",
  r"A continuous function $f$ satisfies $f(x) = x + \displaystyle\int_{0}^{x} f(t)\,dt$ for all real $x$. Then $f(\log_e 3)$ equals",
  r"$2$",
  [(r"$3$", r"Solves $f' = 1 + f$ as $f = e^x$, dropping the constant term."),
   (r"$\log_e 3$", r"Ignores the integral term and takes $f(x) = x$."),
   (r"$5$", r"Uses the initial value $f(0) = 1$, getting $f(x) = 2e^x - 1$.")],
  r"Putting $x = 0$ gives $f(0) = 0$. Differentiating, $f'(x) = 1 + f(x)$, so $(f + 1)' = f + 1$ and $f(x) + 1 = Ce^x$ with $C = 1$. Thus $f(x) = e^x - 1$ and $f(\log_e 3) = 2$.",
  "Using a wrong initial condition after differentiating an integral equation.",
  "U08-D-inteq-ode", "Differentiate, find the initial value from the equation itself, solve.",
  check=_c038, values=[2, 3, log(3), 5],
  numerical=dict(question=r"A continuous function $f$ satisfies $f(x) = x + \displaystyle\int_{0}^{x} f(t)\,dt$ for all real $x$. Then the value of $f(\log_e 3)$ is", answer=2),
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 039
q("U08-D-039", TOP_MOD, "Integral of a maximum function", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{2} \max\{x, x^2\}\,dx$ is",
  r"$\frac{17}{6}$",
  [(r"$\frac{8}{3}$", r"Uses $x^2$ on the whole interval, not noticing $x > x^2$ on $(0, 1)$."),
   (r"$2$", r"Uses $x$ on the whole interval."),
   (r"$\frac{11}{6}$", r"Integrates $\min\{x, x^2\}$: $x^2$ on $[0, 1]$ and $x$ on $[1, 2]$.")],
  r"$x \ge x^2$ on $[0, 1]$ and $x^2 \ge x$ on $[1, 2]$. So the integral is $\int_0^1 x\,dx + \int_1^2 x^2\,dx = \frac{1}{2} + \frac{7}{3} = \frac{17}{6}$.",
  r"Not splitting at the point where the two functions cross.",
  "U08-D-minmax", "Find the crossing point and split.",
  check=lambda: pint(Max(x, x**2), 0, 2), values=[Rational(17, 6), Rational(8, 3), 2, Rational(11, 6)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 040
def _c040():
    F = integrate((x - t)*cos(t), (t, 0, x))
    return simplify(diff(F, x).subs(x, pi/3))
q("U08-D-040", TOP_VAR, "Differentiating when x appears inside the integrand", "Medium", "Multi-step computation MCQ",
  r"If $F(x) = \displaystyle\int_{0}^{x} (x - t)\cos t\,dt$, then $F'\!\left(\frac{\pi}{3}\right)$ equals",
  r"$\frac{\sqrt{3}}{2}$",
  [(r"$0$", r"Applies the Leibniz rule as if $x$ appeared only in the limit: the integrand at $t = x$ is $(x - x)\cos x = 0$."),
   (r"$\frac{\pi}{6}$", r"Keeps only the $x\cos t$ part of the integrand and applies the Leibniz rule to it, getting $F'(x) = x\cos x = \frac{\pi}{6}$ at $x = \frac{\pi}{3}$."),
   (r"$\frac{1}{2}$", r"Gets $F'(x) = \int_0^x \cos t\,dt$ correctly but evaluates it as $\cos x$.")],
  r"Write $F(x) = x\int_0^x \cos t\,dt - \int_0^x t\cos t\,dt$. Then $F'(x) = \int_0^x \cos t\,dt + x\cos x - x\cos x = \sin x$. So $F'\left(\frac{\pi}{3}\right) = \frac{\sqrt{3}}{2}$.",
  r"Forgetting that $x$ inside the integrand must be taken outside before differentiating.",
  "U08-D-leibniz-x-inside", "Separate $x$ from the integrand, then product rule and Leibniz rule.",
  check=_c040, values=[sqrt(3)/2, 0, pi/6, Rational(1, 2)],
  cognitive="Application", source_class=SC)

# ---------------------------------------------------------------- 041
def _c041():
    f = 3 + (x - 2)**3 + sin(x - 2)             # a sample continuous f with f(x) + f(4 - x) = 6
    assert simplify(f + f.subs(x, 4 - x) - 6) == 0
    return integrate(f, (x, 0, 4))
q("U08-D-041", TOP_PROP, "King's property with a constant sum", "Medium", "Conceptual/application MCQ",
  r"Let $f$ be continuous on $\mathbb{R}$ with $f(x) + f(4 - x) = 6$ for all real $x$. Then $\displaystyle\int_{0}^{4} f(x)\,dx$ equals",
  r"$12$",
  [(r"$24$", r"Writes $2I = \int_0^4 6\,dx = 24$ and forgets to halve."),
   (r"$6$", r"Writes $I = \int_0^4 f(x)\,dx = f(x) + f(4 - x) = 6$, reporting the constant sum as the integral without multiplying by the interval length $4$ and halving."),
   (r"$3$", r"Puts $x = 2$ to get $f(2) = 3$ and reports this value of $f$ as the integral.")],
  r"By King's property $I = \int_0^4 f(4 - x)\,dx$. Adding, $2I = \int_0^4 \left(f(x) + f(4 - x)\right)dx = 6 \times 4 = 24$, so $I = 12$.",
  "Forgetting to halve after adding the two forms.",
  "U08-D-king-sum-constant", "King's property used abstractly on an unknown function.",
  check=_c041, values=[12, 24, 6, 3],
  numerical=dict(question=r"Let $f$ be continuous on $\mathbb{R}$ with $f(x) + f(4 - x) = 6$ for all real $x$. Then the value of $\displaystyle\int_{0}^{4} f(x)\,dx$ is", answer=12),
  cognitive="Understanding", source_class=SC)

# ---------------------------------------------------------------- 042
def _c042():
    k = Symbol('k', positive=True)
    n = 0
    while pint(floor(x), 0, n + 1) <= 7:        # find the integer n with int_0^n [x] <= 7 < int_0^(n+1) [x]
        n += 1
    return solve(Eq(pint(floor(x), 0, n) + n*(k - n), 7), k)[0]
q("U08-D-042", TOP_MOD, "Unknown limit of a greatest integer integral", "Medium", "Inverse/parameter MCQ",
  r"If $[x]$ denotes the greatest integer less than or equal to $x$ and $k > 0$ satisfies $\displaystyle\int_{0}^{k} [x]\,dx = 7$, then $k$ equals",
  r"$\frac{17}{4}$",
  [(r"$\frac{13}{3}$", r"Finds $\int_0^4 [x]\,dx = 6$ but then uses $[x] = 3$ beyond $x = 4$, so $3(k - 4) = 1$."),
   (r"$\sqrt{14}$", r"Drops the greatest integer function: $\frac{k^2}{2} = 7$."),
   (r"$\frac{10}{3}$", r"Takes $\int_0^3 [x]\,dx = 1 + 2 + 3 = 6$ and then needs $3(k - 3) = 1$.")],
  r"$\int_0^n [x]\,dx = 0 + 1 + \dots + (n - 1)$, so $\int_0^4 [x]\,dx = 6$ and $\int_0^5 [x]\,dx = 10$. Hence $4 < k < 5$ and $6 + 4(k - 4) = 7$, giving $k = \frac{17}{4}$.",
  "Off-by-one errors in the value of $[x]$ on each unit interval.",
  "U08-D-floor-inverse", "Reverse problem: locate the unit interval, then solve a linear equation.",
  check=_c042, values=[Rational(17, 4), Rational(13, 3), sqrt(14), Rational(10, 3)],
  numerical=dict(question=r"If $[x]$ denotes the greatest integer less than or equal to $x$ and $k > 0$ satisfies $\displaystyle\int_{0}^{k} [x]\,dx = 7$, then the value of $4k$ is", answer=17),
  cognitive="Application", source_class=SC)


# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 043
q("U08-D-043", TOP_PROP, "Odd-even split, half-period doubling and King's ratio", "Difficult", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{-\pi}^{\pi} \frac{x\cos x + \sin^4 x}{\sin^4 x + \cos^4 x}\,dx$ is",
  r"$\pi$",
  [(r"$\frac{\pi}{2}$", r"Doubles only once: writes the even part as $2\int_0^{\pi/2}\frac{\sin^4 x}{\sin^4 x + \cos^4 x}\,dx = 2\cdot\frac{\pi}{4}$, treating $[0, \pi]$ as if it were $[0, \frac{\pi}{2}]$."),
   (r"$2\pi$", r"Uses the average value $\frac{1}{2}$ of the ratio over the whole interval $[-\pi, \pi]$ to get $\frac{1}{2}\cdot 2\pi = \pi$, then doubles again for evenness."),
   (r"$\frac{\pi}{4}$", r"Quotes $\int_0^{\pi/2}\frac{\sin^4 x}{\sin^4 x + \cos^4 x}\,dx = \frac{\pi}{4}$ and forgets both doublings (for evenness and for $[0, \pi]$).")],
  r"The denominator is even and $x\cos x$ is odd, so $\frac{x\cos x}{\sin^4 x + \cos^4 x}$ integrates to $0$. The remaining part is even, so the integral is $2\int_0^{\pi}\frac{\sin^4 x}{\sin^4 x + \cos^4 x}\,dx$; this integrand is unchanged under $x \to \pi - x$, so it equals $4\int_0^{\pi/2}\frac{\sin^4 x}{\sin^4 x + \cos^4 x}\,dx$. By King's property on $[0, \frac{\pi}{2}]$, $J = \int_0^{\pi/2}\frac{\sin^4 x}{\sin^4 x + \cos^4 x}\,dx = \int_0^{\pi/2}\frac{\cos^4 x}{\sin^4 x + \cos^4 x}\,dx$, so $2J = \frac{\pi}{2}$ and $J = \frac{\pi}{4}$. Hence the value is $4\cdot\frac{\pi}{4} = \pi$.",
  r"Losing one of the two doubling steps ($[-\pi, \pi] \to [0, \pi]$ and $[0, \pi] \to [0, \frac{\pi}{2}]$).",
  "U08-D-odd-even-king-ratio", r"Three ideas chained: parity split with an odd numerator over an even denominator, the $f(2a - x) = f(x)$ doubling rule, and King's property in ratio form.",
  check=lambda: NI((x*cos(x) + sin(x)**4)/(sin(x)**4 + cos(x)**4), -pi, pi), values=[pi, pi/2, 2*pi, pi/4],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 044
q("U08-D-044", TOP_PROP, "Reducing a log integral to the log-sine integral", "Difficult", "Multi-step computation MCQ",
  r"Given that $\displaystyle\int_{0}^{\pi/2} \log_e(\sin x)\,dx = -\frac{\pi}{2}\log_e 2$, the value of $\displaystyle\int_{0}^{\pi} \log_e(1 + \cos x)\,dx$ is",
  r"$-\pi\log_e 2$",
  [(r"$0$", r"After $1 + \cos x = 2\cos^2\frac{x}{2}$, puts $u = \frac{x}{2}$ but forgets $dx = 2\,du$: $\pi\log_e 2 + 2\int_0^{\pi/2}\log_e(\cos u)\,du = 0$."),
   (r"$-2\pi\log_e 2$", r"Drops the constant: writes $\log_e(1 + \cos x) = 2\log_e\left(\cos\frac{x}{2}\right)$, losing $\log_e 2$."),
   (r"$\frac{\pi}{2}\log_e 2$", r"Forgets both the factor $2$ from the square and the factor $2$ from $dx = 2\,du$: $\pi\log_e 2 + \int_0^{\pi/2}\log_e(\cos u)\,du$.")],
  r"$\log_e(1 + \cos x) = \log_e 2 + 2\log_e\left(\cos\frac{x}{2}\right)$ on $[0, \pi)$. With $x = 2u$, $\int_0^{\pi}\log_e\left(\cos\frac{x}{2}\right)dx = 2\int_0^{\pi/2}\log_e(\cos u)\,du = -\pi\log_e 2$, using King's property to switch $\cos$ to $\sin$. So the integral is $\pi\log_e 2 + 2(-\pi\log_e 2) = -\pi\log_e 2$.",
  "Losing a factor of $2$ in the half-angle identity or in the substitution.",
  "U08-D-king-logsin", "Half-angle identity, substitution with changed limits and King's property.",
  check=lambda: NI(log(1 + cos(x)), 0, pi), values=[-pi*log(2), 0, -2*pi*log(2), pi/2*log(2)],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 045
def _c045():
    A, B = symbols('A B')
    f = x + x*A + B                          # f(x) = x + x*int f + int t f
    sol = solve([Eq(A, integrate(f, (x, 0, 1))), Eq(B, integrate(x*f, (x, 0, 1)))], [A, B])
    return f.subs(sol).subs(x, 1)
q("U08-D-045", TOP_EQ, "Integral equation with two unknown constants", "Difficult", "Multi-step computation MCQ",
  r"A continuous function $f$ satisfies $f(x) = x + \displaystyle\int_{0}^{1} (x + t)\,f(t)\,dt$ for all real $x$. Then $f(1)$ equals",
  r"$-10$",
  [(r"$\frac{5}{3}$", r"Keeps only $\int_0^1 t f(t)\,dt$ and drops the $x\int_0^1 f(t)\,dt$ part, so $f(x) = x + B$ with $B = \frac{2}{3}$."),
   (r"$8$", r"Sets up $f(x) = (1 + A)x + B$ but in $B = \int_0^1 t f(t)\,dt$ omits the $\frac{B}{2}$ term, giving $A = 5$, $B = 2$."),
   (r"$-4$", r"Evaluates $\int_0^1 t^2\,dt$ as $\frac{1}{2}$ in the equation for $B$, giving $A = -3$, $B = -2$.")],
  r"Let $A = \int_0^1 f(t)\,dt$ and $B = \int_0^1 t f(t)\,dt$; then $f(x) = (1 + A)x + B$. So $A = \frac{1 + A}{2} + B$ and $B = \frac{1 + A}{3} + \frac{B}{2}$. The second gives $B = \frac{2(1 + A)}{3}$; substituting, $A = \frac{7(1 + A)}{6}$, so $A = -7$ and $B = -4$. Thus $f(x) = -6x - 4$ and $f(1) = -10$.",
  "Not separating the $x$-dependent and constant parts of the kernel $x + t$.",
  "U08-D-inteq-constant", "Two unknown constants and a simultaneous linear system.",
  check=_c045, values=[-10, Rational(5, 3), 8, -4], cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 046
def _c046():
    G = integrate((x - t)*sin(t**2), (t, 0, x))
    return limit(G/x**4, x, 0)
q("U08-D-046", TOP_VAR, "Limit with x inside the integrand", "Difficult", "Multi-step computation MCQ",
  r"The value of $\displaystyle\lim_{x \to 0} \frac{1}{x^4}\int_{0}^{x} (x - t)\sin(t^2)\,dt$ is",
  r"$\frac{1}{12}$",
  [(r"$\frac{1}{4}$", r"Differentiates the numerator as $x\sin(x^2)$, applying the Leibniz rule to the $x\sin(t^2)$ part only, then $\frac{x\sin x^2}{4x^3} \to \frac{1}{4}$."),
   (r"$\frac{1}{3}$", r"Replaces $\sin(t^2)$ by $t^2$ but drops the $-t$ part, so the numerator is about $x\cdot\frac{x^3}{3}$."),
   (r"$0$", r"Takes the derivative of the numerator to be the integrand at $t = x$, which is $0$, and concludes the limit is $0$.")],
  r"Let $G(x) = x\int_0^x \sin(t^2)\,dt - \int_0^x t\sin(t^2)\,dt$. Then $G'(x) = \int_0^x \sin(t^2)\,dt$ and $G''(x) = \sin(x^2)$. Applying L'Hospital's rule twice, the limit is $\lim\frac{\sin x^2}{12x^2} = \frac{1}{12}$.",
  r"Differentiating $\int_0^x (x - t)g(t)\,dt$ as if $x$ appeared only in the limit.",
  "U08-D-limit-lhopital", "Two L'Hospital steps with an integrand that depends on $x$.",
  check=_c046, values=[Rational(1, 12), Rational(1, 4), Rational(1, 3), 0], cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 047
q("U08-D-047", TOP_MOD, "Greatest integer of a quadratic with irrational break point", "Difficult", "Multi-step computation MCQ",
  r"If $[\,\cdot\,]$ denotes the greatest integer function, then $\displaystyle\int_{0}^{2} \left[x^2 - x + 1\right]dx$ equals",
  r"$\frac{5 - \sqrt{5}}{2}$",
  [(r"$\frac{7 - \sqrt{5}}{2}$", r"Takes $[x^2 - x + 1] = 1$ on $[0, 1]$, missing that $\frac{3}{4} \le x^2 - x + 1 < 1$ on $(0, 1)$."),
   (r"$\frac{1 + \sqrt{5}}{2}$", r"Swaps the values on the two pieces: $2$ on $\left[1, \frac{1 + \sqrt{5}}{2}\right)$ and $1$ on $\left[\frac{1 + \sqrt{5}}{2}, 2\right]$."),
   (r"$\frac{3 - \sqrt{5}}{2}$", r"Uses values one less than correct on $[1, 2]$: $0$ up to $\frac{1 + \sqrt{5}}{2}$ and $1$ after it.")],
  r"$x^2 - x + 1 = \left(x - \frac{1}{2}\right)^2 + \frac{3}{4}$ lies in $\left[\frac{3}{4}, 1\right)$ on $(0, 1)$, so the floor is $0$ there. On $[1, 2]$ it rises from $1$ to $3$ and equals $2$ at $x = \frac{1 + \sqrt{5}}{2}$. So the integral is $\left(\frac{1 + \sqrt{5}}{2} - 1\right) + 2\left(2 - \frac{1 + \sqrt{5}}{2}\right) = \frac{5 - \sqrt{5}}{2}$.",
  "Not checking the minimum of the quadratic before assigning floor values.",
  "U08-D-floor-nonlinear", "Range of a quadratic, solving for an irrational break point, three pieces.",
  check=lambda: pint(floor(x**2 - x + 1), 0, 2), values=[(5 - sqrt(5))/2, (7 - sqrt(5))/2, (1 + sqrt(5))/2, (3 - sqrt(5))/2],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 048
q("U08-D-048", TOP_MOD, "Greatest integer of a sum of sine and cosine", "Difficult", "Multi-step computation MCQ",
  r"If $[\,\cdot\,]$ denotes the greatest integer function, then $\displaystyle\int_{0}^{2\pi} [\sin x + \cos x]\,dx$ equals",
  r"$-\pi$",
  [(r"$0$", r"Truncates toward zero, using $[y] = 0$ for $-1 \le y < 0$ and $[y] = -1$ for $-\sqrt{2} \le y < -1$."),
   (r"$-\frac{\pi}{2}$", r"Omits the two pieces where the value is $-1$, keeping only the $+1$ and $-2$ pieces."),
   (r"$\frac{\pi}{2}$", r"Keeps only the piece $\left[0, \frac{\pi}{2}\right]$ where the value is $1$ and ignores negative values.")],
  r"$\sin x + \cos x = \sqrt{2}\sin\left(x + \frac{\pi}{4}\right)$. Its floor is $1$ on $\left[0, \frac{\pi}{2}\right]$, $0$ on $\left(\frac{\pi}{2}, \frac{3\pi}{4}\right]$, $-1$ on $\left(\frac{3\pi}{4}, \pi\right]$, $-2$ on $\left(\pi, \frac{3\pi}{2}\right)$, $-1$ on $\left[\frac{3\pi}{2}, \frac{7\pi}{4}\right)$ and $0$ on $\left[\frac{7\pi}{4}, 2\pi\right]$. So the integral is $\frac{\pi}{2} - \frac{\pi}{4} - \pi - \frac{\pi}{4} = -\pi$.",
  r"Treating the greatest integer of a negative number as its integer part toward zero.",
  "U08-D-floor-trig", "Six pieces, negative floor values, careful sign handling.",
  check=lambda: pint(floor(sin(x) + cos(x)), 0, 2*pi), values=[-pi, 0, -pi/2, pi/2],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 049
q("U08-D-049", TOP_PROP, "King's property to simplify a numerator", "Difficult", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi/2} \frac{\sin^2 x}{\sin x + \cos x}\,dx$ is",
  r"$\frac{1}{\sqrt{2}}\log_e\left(1 + \sqrt{2}\right)$",
  [(r"$\sqrt{2}\log_e\left(1 + \sqrt{2}\right)$", r"Finds $\int_0^{\pi/2}\frac{dx}{\sin x + \cos x} = \sqrt{2}\log_e(1 + \sqrt{2})$ and forgets that this is $2I$."),
   (r"$\frac{1}{2\sqrt{2}}\log_e\left(1 + \sqrt{2}\right)$", r"Halves twice, taking $2I$ to be $\frac{1}{\sqrt{2}}\log_e(1 + \sqrt{2})$."),
   (r"$\frac{\pi}{4}$", r"Adds the two forms and cancels the denominator as if $\frac{\sin^2 x + \cos^2 x}{\sin x + \cos x}$ were $1$, so $2I = \frac{\pi}{2}$.")],
  r"By King's property $I = \int_0^{\pi/2}\frac{\cos^2 x}{\cos x + \sin x}\,dx$, so $2I = \int_0^{\pi/2}\frac{dx}{\sin x + \cos x} = \frac{1}{\sqrt{2}}\int_0^{\pi/2}\csc\left(x + \frac{\pi}{4}\right)dx$. This equals $\frac{1}{\sqrt{2}}\left[\log_e\tan\frac{x + \pi/4}{2}\right]_0^{\pi/2} = \frac{1}{\sqrt{2}}\log_e\frac{\tan(3\pi/8)}{\tan(\pi/8)} = \frac{1}{\sqrt{2}}\log_e(1 + \sqrt{2})^2 = \sqrt{2}\log_e(1 + \sqrt{2})$. Hence $I = \frac{1}{\sqrt{2}}\log_e(1 + \sqrt{2})$.",
  "Forgetting to halve, or mis-evaluating the cosecant integral.",
  "U08-D-king-reduce-denominator", "King's property, then a cosecant integral with exact tangent values.",
  check=lambda: NI(sin(x)**2/(sin(x) + cos(x)), 0, pi/2), values=[log(1 + sqrt(2))/sqrt(2), sqrt(2)*log(1 + sqrt(2)), log(1 + sqrt(2))/(2*sqrt(2)), pi/4],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 050
def _c050():
    g = integrate(t**2, (t, x, x + 1))
    crit = solve(diff(g, x), x)
    return min(g.subs(x, c) for c in crit)
q("U08-D-050", TOP_VAR, "Minimum of a sliding-window integral", "Difficult", "Multi-step computation MCQ",
  r"For real $x$, let $g(x) = \displaystyle\int_{x}^{x + 1} t^2\,dt$. The minimum value of $g(x)$ is",
  r"$\frac{1}{12}$",
  [(r"$\frac{1}{3}$", r"Assumes the minimum occurs at $x = 0$, where the integrand $t^2$ is smallest at the lower limit: $g(0) = \frac{1}{3}$."),
   (r"$\frac{1}{24}$", r"Finds $x = -\frac{1}{2}$ and uses symmetry $g = 2\int_0^{1/2} t^2\,dt$ but forgets the factor $2$."),
   (r"$\frac{3}{4}$", r"Expands $\frac{(x + 1)^3 - x^3}{3}$ as $x^2 + x + 1$, not dividing the constant term by $3$, and minimises.")],
  r"$g'(x) = (x + 1)^2 - x^2 = 2x + 1$, which vanishes at $x = -\frac{1}{2}$ and changes sign from $-$ to $+$. So the minimum is $g\left(-\frac{1}{2}\right) = \int_{-1/2}^{1/2} t^2\,dt = \frac{1}{12}$.",
  "Minimising the integrand in place of the integral function.",
  "U08-D-varlimit-sliding-window", "Leibniz rule with both limits moving, then optimisation.",
  check=_c050, values=[Rational(1, 12), Rational(1, 3), Rational(1, 24), Rational(3, 4)],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 051
def _c051():
    f = x**3 + x
    b = [r for r in solve(Eq(f, 2), x) if r.is_real][0]          # f(b) = 2
    a = [r for r in solve(Eq(f, 0), x) if r.is_real][0]          # f(a) = 0
    return integrate(x*diff(f, x), (x, a, b))                    # y = f(x) turns int f^{-1}(y) dy into int x f'(x) dx
q("U08-D-051", TOP_PROP, "Integral of an inverse function", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = x^3 + x$, which is strictly increasing on $\mathbb{R}$, and let $f^{-1}$ be its inverse. If $I = \displaystyle\int_{0}^{2} f^{-1}(y)\,dy$, then $I$ equals",
  r"$\frac{5}{4}$",
  [(r"$\frac{3}{4}$", r"Computes $\int_0^1 f(x)\,dx = \frac{1}{4} + \frac{1}{2}$ in place of the inverse integral."),
   (r"$\frac{11}{4}$", r"Uses $b f(b) - a f(a) + \int_a^b f$ with a plus sign: $2 + \frac{3}{4}$."),
   (r"$14$", r"Substitutes $y = f(x)$ but keeps the old limits $0$ to $2$ for $x$: $\int_0^2 x(3x^2 + 1)\,dx = 14$.")],
  r"Put $y = f(x)$, so $f^{-1}(y) = x$ and $dy = (3x^2 + 1)\,dx$; $y = 0, 2$ correspond to $x = 0, 1$. Then $I = \int_0^1 x(3x^2 + 1)\,dx = \frac{3}{4} + \frac{1}{2} = \frac{5}{4}$. (Equivalently $I = 1\cdot f(1) - \int_0^1 f(x)\,dx = 2 - \frac{3}{4}$.)",
  "Not changing the limits when substituting $y = f(x)$.",
  "U08-D-inverse-function-integral", "Requires the substitution $y = f(x)$ with new limits; no explicit inverse is available.",
  check=_c051, values=[Rational(5, 4), Rational(3, 4), Rational(11, 4), 14],
  numerical=dict(question=r"Let $f(x) = x^3 + x$, which is strictly increasing on $\mathbb{R}$, and let $f^{-1}$ be its inverse. If $I = \displaystyle\int_{0}^{2} f^{-1}(y)\,dy$, then the value of $4I$ is", answer=5),
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 052
def _c052():
    s1 = pint(x - floor(x), -2, 3) == 2
    s2 = abs(NI(sin(2*x)*log(tan(x)), 0, pi/2)) < Float('1e-20')
    return (bool(s1), bool(s2))
q("U08-D-052", TOP_PROP, "Fractional part and King's property", "Difficult", "Statement-based MCQ",
  r"Let $[x]$ denote the greatest integer less than or equal to $x$. Statement I: $\displaystyle\int_{-2}^{3} (x - [x])\,dx = 2$. Statement II: $\displaystyle\int_{0}^{\pi/2} \sin 2x\,\log_e(\tan x)\,dx = 0$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts $2$ for Statement I by counting only the four unit intervals from $-2$ to $2$ (or treating $x - [x]$ as vanishing for negative $x$)."),
   (ST_TF, r"Accepts $2$ for Statement I as above and also wrongly treats $\sin 2x\log_e(\tan x)$ as unchanged under $x \to \frac{\pi}{2} - x$, so expects a nonzero value."),
   (ST_FF, r"Correctly rejects Statement I but misses that $\sin 2x$ is unchanged and $\log_e(\tan x)$ changes sign under $x \to \frac{\pi}{2} - x$.")],
  r"Statement I: $x - [x]$ has period $1$ and $\int_0^1 x\,dx = \frac{1}{2}$; the interval $[-2, 3]$ contains $5$ periods, so the integral is $\frac{5}{2} \ne 2$, and Statement I is false. Statement II: under $x \to \frac{\pi}{2} - x$, $\sin 2x$ is unchanged and $\log_e(\tan x) \to -\log_e(\tan x)$, so $I = -I$ and $I = 0$; Statement II is true.",
  "Miscounting periods of the fractional part over an interval with negative end point.",
  "U08-D-statement-fractional", "Two independent properties, one with a negative-limit trap.",
  check=_c052, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 053
def _c053():
    s1 = simplify(integrate(x*sin(x)**2, (x, 0, pi)) - pi**2/2) == 0
    F = Integral(exp(t**2), (t, x, x**2))
    s2 = simplify(diff(F, x).doit().subs(x, 1) - 2*E) == 0
    return (bool(s1), bool(s2))
q("U08-D-053", TOP_VAR, "King's property and two-limit Leibniz rule", "Difficult", "Statement-based MCQ",
  r"Statement I: $\displaystyle\int_{0}^{\pi} x\sin^2 x\,dx = \frac{\pi^2}{2}$. Statement II: If $F(x) = \displaystyle\int_{x}^{x^2} e^{t^2}\,dt$, then $F'(1) = 2e$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Forgets to halve in Statement I ($2I = \pi\cdot\frac{\pi}{2}$ read as $I$) and drops the lower-limit term in Statement II."),
   (ST_TF, r"Accepts the unhalved value $\frac{\pi^2}{2}$ in Statement I but handles Statement II correctly."),
   (ST_FT, r"Handles Statement I correctly but uses only the upper-limit term $2x e^{x^4}$ in Statement II.")],
  r"Statement I: by King's property $\int_0^{\pi} x\sin^2 x\,dx = \frac{\pi}{2}\int_0^{\pi}\sin^2 x\,dx = \frac{\pi}{2}\cdot\frac{\pi}{2} = \frac{\pi^2}{4}$, so it is false. Statement II: $F'(x) = 2x e^{x^4} - e^{x^2}$, so $F'(1) = 2e - e = e$; it is false.",
  "Forgetting the halving in King's property and the lower-limit term in the Leibniz rule.",
  "U08-D-statement-king", "Two separate evaluations, each with a standard trap.",
  check=_c053, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 054
def _c054():
    u = Symbol('u', positive=True)
    F = Function('f')
    # differentiate int_u^1 t^2 f(t) dt = 1 - u with respect to u = sin x (dividing out cos x > 0)
    lhs = diff(Integral(t**2*F(t), (t, u, 1)), u).doit()
    fu = solve(Eq(lhs, diff(1 - u, u)), F(u))[0]
    assert simplify(integrate(t**2*fu.subs(u, t), (t, u, 1)) - (1 - u)) == 0
    return fu.subs(u, 1/sqrt(3))
q("U08-D-054", TOP_EQ, "Integral equation with a trigonometric lower limit", "Difficult", "Multi-step computation MCQ",
  r"A continuous function $f : (0, 1] \to \mathbb{R}$ satisfies $\displaystyle\int_{\sin x}^{1} t^2 f(t)\,dt = 1 - \sin x$ for all $x \in \left(0, \frac{\pi}{2}\right]$. Then $f\!\left(\frac{1}{\sqrt{3}}\right)$ equals",
  r"$3$",
  [(r"$\frac{1}{3}$", r"Solves $\sin^2 x\,f(\sin x) = 1$ upside down, writing $f(\sin x) = \sin^2 x$."),
   (r"$1$", r"Drops the factor $t^2$ when differentiating, getting $f(\sin x)\cos x = \cos x$."),
   (r"$\sqrt{3}$", r"Takes the factor as $t$ in place of $t^2$, so $f(\sin x) = \frac{1}{\sin x}$.")],
  r"Differentiating with respect to $x$: $-\sin^2 x\,f(\sin x)\cos x = -\cos x$. For $x \in \left(0, \frac{\pi}{2}\right)$, $\cos x \ne 0$, so $f(\sin x) = \frac{1}{\sin^2 x}$, i.e. $f(u) = \frac{1}{u^2}$ (which indeed satisfies the equation). Hence $f\left(\frac{1}{\sqrt{3}}\right) = 3$.",
  "Mishandling the factor $t^2$ or the chain factor $\\cos x$.",
  "U08-D-inteq-trig-limit", "Leibniz rule with a trigonometric limit, cancelling a chain factor, then re-expressing in $u$.",
  check=_c054, values=[3, Rational(1, 3), 1, sqrt(3)],
  numerical=dict(question=r"A continuous function $f : (0, 1] \to \mathbb{R}$ satisfies $\displaystyle\int_{\sin x}^{1} t^2 f(t)\,dt = 1 - \sin x$ for all $x \in \left(0, \frac{\pi}{2}\right]$. Then the value of $f\!\left(\frac{1}{\sqrt{3}}\right)$ is", answer=3),
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 055
q("U08-D-055", TOP_MOD, "Integral of a minimum of three functions", "Difficult", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{-1}^{1} \min\left\{|x|,\ 1 - |x|,\ \frac{1}{4}\right\}dx$ is",
  r"$\frac{3}{8}$",
  [(r"$\frac{1}{2}$", r"Ignores the cap $\frac{1}{4}$ and integrates $\min\{|x|, 1 - |x|\}$, two triangles of area $\frac{1}{4}$."),
   (r"$\frac{3}{16}$", r"Computes the integral over $[0, 1]$ correctly but forgets to double for the even integrand."),
   (r"$\frac{1}{4}$", r"Keeps only the flat parts at height $\frac{1}{4}$ on $\left[\frac{1}{4}, \frac{3}{4}\right]$ and its mirror image, dropping the four triangular end pieces.")],
  r"The integrand is even. On $[0, 1]$ it equals $x$ on $\left[0, \frac{1}{4}\right]$, $\frac{1}{4}$ on $\left[\frac{1}{4}, \frac{3}{4}\right]$ and $1 - x$ on $\left[\frac{3}{4}, 1\right]$, giving $\frac{1}{32} + \frac{1}{8} + \frac{1}{32} = \frac{3}{16}$. Doubling, the integral is $\frac{3}{8}$.",
  "Not locating all the crossing points among three functions.",
  "U08-D-minmax", "Even-function reduction plus three crossing points.",
  check=lambda: pint(Min(Abs(x), 1 - Abs(x), Rational(1, 4)), -1, 1), values=[Rational(3, 8), Rational(1, 2), Rational(3, 16), Rational(1, 4)],
  numerical=dict(question=r"If $I = \displaystyle\int_{-1}^{1} \min\left\{|x|,\ 1 - |x|,\ \frac{1}{4}\right\}dx$, then the value of $8I$ is", answer=3),
  cognitive="Analysis", source_class=SC)

# ---------------------------------------------------------------- 056
q("U08-D-056", TOP_PROP, "King's property with a cosine-squared denominator", "Difficult", "Multi-step computation MCQ",
  r"The value of $\displaystyle\int_{0}^{\pi} \frac{x}{1 + \cos^2 x}\,dx$ is",
  r"$\frac{\pi^2}{2\sqrt{2}}$",
  [(r"$\frac{\pi^2}{\sqrt{2}}$", r"Reaches $2I = \pi\int_0^{\pi}\frac{dx}{1 + \cos^2 x} = \frac{\pi^2}{\sqrt{2}}$ and forgets to halve."),
   (r"$\frac{\pi^2}{2}$", r"After dividing by $\cos^2 x$, writes the denominator $\sec^2 x + 1$ as $u^2 + 1$ (not $u^2 + 2$), so $\int_0^{\pi/2}\frac{dx}{1 + \cos^2 x}$ becomes $\frac{\pi}{2}$ and $I = \frac{\pi^2}{2}$."),
   (r"$\frac{\pi^2}{4\sqrt{2}}$", r"Uses $I = \frac{\pi}{2}\int_0^{\pi/2}\frac{dx}{1 + \cos^2 x}$, forgetting that $\int_0^{\pi} = 2\int_0^{\pi/2}$ here: $\frac{\pi}{2}\cdot\frac{\pi}{2\sqrt{2}}$.")],
  r"By King's property, $I = \frac{\pi}{2}\int_0^{\pi}\frac{dx}{1 + \cos^2 x} = \pi\int_0^{\pi/2}\frac{dx}{1 + \cos^2 x}$. Dividing by $\cos^2 x$ and putting $u = \tan x$: $\int_0^{\infty}\frac{du}{u^2 + 2} = \frac{\pi}{2\sqrt{2}}$. Hence $I = \pi\cdot\frac{\pi}{2\sqrt{2}} = \frac{\pi^2}{2\sqrt{2}}$.",
  r"Using $u = \tan x$ directly across $x = \frac{\pi}{2}$, or forgetting to double the half-interval.",
  "U08-D-king-x-times", "King's property, the $2a$ property and a tangent substitution.",
  check=lambda: NI(x/(1 + cos(x)**2), 0, pi), values=[pi**2/(2*sqrt(2)), pi**2/sqrt(2), pi**2/2, pi**2/(4*sqrt(2))],
  cognitive="Analysis", source_class=SC)
