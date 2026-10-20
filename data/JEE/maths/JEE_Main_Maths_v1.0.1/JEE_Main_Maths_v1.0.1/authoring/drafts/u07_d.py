import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from sympy import idiff

x = Symbol('x', real=True)
y = Symbol('y', real=True)
a = Symbol('a', real=True)
k = Symbol('k', real=True)
p_, q_ = symbols('p q', real=True)
A_, B_ = symbols('A B', real=True)

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_PQ = "Product and quotient rules"
TOP_CH = "Chain rule and composite functions"
TOP_IMP = "Implicit differentiation"
TOP_INV = "Derivatives of inverse trigonometric functions"
TOP_LOG = "Logarithmic differentiation"
TOP_SEC = "Second order derivatives"
TOP_WRT = "Derivative of one function with respect to another"
XII = "XII"


def at(expr, val):
    return nsimplify(simplify(expr.subs(x, val)))


# ================================================================ EASY
# ---------------------------------------------------------------- 001
def _c001():
    f = (x**2 + 1)*(x**3 - 2*x)
    return diff(f, x).subs(x, 2)
q("U07-D-001", TOP_PQ, "Product rule at a point", "Easy", "Single-step computation MCQ",
  r"If $f(x) = (x^2 + 1)(x^3 - 2x)$, then $f'(2)$ equals",
  r"$66$",
  [(r"$40$", r"Multiplies the derivatives of the two factors: $(2x)(3x^2 - 2) = 4 \cdot 10 = 40$ at $x = 2$."),
   (r"$50$", r"Keeps only $(x^2+1)(3x^2-2) = 5 \cdot 10$, not differentiating the first factor."),
   (r"$16$", r"Keeps only $2x(x^3 - 2x) = 4 \cdot 4$, not differentiating the second factor.")],
  r"By the product rule $f'(x) = 2x(x^3 - 2x) + (x^2 + 1)(3x^2 - 2)$. At $x = 2$: $4 \cdot 4 + 5 \cdot 10 = 16 + 50 = 66$.",
  r"Treating the derivative of a product as the product of the derivatives.",
  "U07-D-product-value", "One rule (product rule) and one substitution.",
  check=_c001, values=[66, 40, 50, 16], source_class="XI", cognitive="Application",
  numerical=dict(question=r"If $f(x) = (x^2 + 1)(x^3 - 2x)$, then the value of $f'(2)$ is", answer=66))

# ---------------------------------------------------------------- 002
def _c002():
    f = (2*x + 3)/(x - 1)
    return simplify(diff(f, x).subs(x, 3))
q("U07-D-002", TOP_PQ, "Quotient rule at a point", "Easy", "Single-step computation MCQ",
  r"If $y = \frac{2x+3}{x-1}$, then the value of $\frac{dy}{dx}$ at $x = 3$ is",
  r"$-\frac{5}{4}$",
  [(r"$\frac{5}{4}$", r"Reverses the order in the numerator of the quotient rule: $\frac{(2x+3)\cdot 1 - 2(x-1)}{(x-1)^2} = \frac{5}{4}$."),
   (r"$-\frac{5}{2}$", r"Does not square the denominator: $\frac{-5}{x-1} = -\frac{5}{2}$ at $x = 3$."),
   (r"$2$", r"Divides the derivative of the numerator by that of the denominator: $\frac{2}{1} = 2$.")],
  r"$\frac{dy}{dx} = \frac{2(x-1) - (2x+3)(1)}{(x-1)^2} = \frac{-5}{(x-1)^2}$. At $x = 3$ this is $-\frac{5}{4}$.",
  r"Writing the quotient rule numerator in the wrong order.",
  "U07-D-quotient-value", "Direct quotient rule and one substitution.",
  check=_c002, values=[Rational(-5, 4), Rational(5, 4), Rational(-5, 2), 2], source_class="XI", cognitive="Application")

# ---------------------------------------------------------------- 003
def _c003():
    return diff(sin(2*x)**3, x)
q("U07-D-003", TOP_CH, "Power of a trigonometric function", "Easy", "Single-step computation MCQ",
  r"The derivative of $\sin^3 (2x)$ with respect to $x$ is",
  r"$6\sin^2 (2x)\cos (2x)$",
  [(r"$3\sin^2 (2x)\cos (2x)$", r"Leaves out the factor $2$ from the derivative of the innermost function $2x$."),
   (r"$6\cos^2 (2x)$", r"Differentiates inside the power, writing $3(\cos 2x)^2 \cdot 2$, so the outer layer $u^3$ and the middle layer $\sin u$ are merged."),
   (r"$\frac{3}{2}\sin^2 (2x)\cos (2x)$", r"Divides by the inner derivative $2$ (an integration habit) instead of multiplying by it.")],
  r"With three layers, $\frac{d}{dx}\sin^3(2x) = 3\sin^2(2x)\cdot\cos(2x)\cdot 2 = 6\sin^2(2x)\cos(2x)$.",
  r"Stopping the chain rule one layer early.",
  "U07-D-chain-trig-power", "Chain rule through three layers, single step each.",
  check=_c003, values=[6*sin(2*x)**2*cos(2*x), 3*sin(2*x)**2*cos(2*x), 6*cos(2*x)**2, Rational(3, 2)*sin(2*x)**2*cos(2*x)],
  source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 004
def _c004():
    F = x**2 + x*y + y**2 - 7
    assert F.subs({x: 1, y: 2}) == 0
    return idiff(F, y, x).subs({x: 1, y: 2})
q("U07-D-004", TOP_IMP, "Slope on an implicit curve", "Easy", "Single-step computation MCQ",
  r"For the curve $x^2 + xy + y^2 = 7$, the value of $\frac{dy}{dx}$ at the point $(1, 2)$ is",
  r"$-\frac{4}{5}$",
  [(r"$-\frac{1}{2}$", r"Ignores the $xy$ term: $2x + 2y\,y' = 0$ gives $y' = -\frac{x}{y} = -\frac{1}{2}$."),
   (r"$-\frac{2}{5}$", r"Differentiates $xy$ as $x\,y'$ only: $2x + x\,y' + 2y\,y' = 0$ gives $-\frac{2x}{x + 2y} = -\frac{2}{5}$."),
   (r"$-1$", r"Differentiates $xy$ as $y$ only: $2x + y + 2y\,y' = 0$ gives $-\frac{2x+y}{2y} = -1$.")],
  r"Differentiating, $2x + (y + x\,y') + 2y\,y' = 0$, so $y' = -\frac{2x + y}{x + 2y}$. At $(1, 2)$: $y' = -\frac{4}{5}$.",
  r"Not using the product rule on the mixed term $xy$.",
  "U07-D-implicit-point", "One implicit differentiation with a product term, then substitution.",
  check=_c004, values=[Rational(-4, 5), Rational(-1, 2), Rational(-2, 5), -1], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    return at(diff(asin(2*x), x), Rational(1, 4))
q("U07-D-005", TOP_INV, "Derivative of inverse sine with a linear argument", "Easy", "Single-step computation MCQ",
  r"If $f(x) = \sin^{-1}(2x)$, then $f'\left(\frac{1}{4}\right)$ equals",
  r"$\frac{4\sqrt{3}}{3}$",
  [(r"$\frac{2\sqrt{3}}{3}$", r"Leaves out the chain factor $2$: $\frac{1}{\sqrt{1-4x^2}} = \frac{2}{\sqrt{3}}$."),
   (r"$\frac{8\sqrt{15}}{15}$", r"Uses $\sqrt{1-x^2}$ in place of $\sqrt{1-(2x)^2}$: $\frac{2}{\sqrt{15/16}} = \frac{8}{\sqrt{15}}$."),
   (r"$-\frac{4\sqrt{3}}{3}$", r"Uses the sign of the derivative of $\cos^{-1}$.")],
  r"$f'(x) = \frac{2}{\sqrt{1-4x^2}}$. At $x = \frac{1}{4}$: $\frac{2}{\sqrt{3/4}} = \frac{4}{\sqrt{3}} = \frac{4\sqrt{3}}{3}$.",
  r"Forgetting the derivative of the inner function.",
  "U07-D-invtrig-direct", "Standard formula with one chain factor.",
  check=_c005, values=[4*sqrt(3)/3, 2*sqrt(3)/3, 8*sqrt(15)/15, -4*sqrt(3)/3], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 006
def _c006():
    return simplify(diff(x**x, x).subs(x, 2))
q("U07-D-006", TOP_LOG, "Variable base and variable exponent", "Easy", "Single-step computation MCQ",
  r"If $y = x^x$ for $x > 0$, then the value of $\frac{dy}{dx}$ at $x = 2$ is",
  r"$4(1 + \log_e 2)$",
  [(r"$4$", r"Uses the power rule $x \cdot x^{x-1} = x^x$, treating the exponent as constant."),
   (r"$4\log_e 2$", r"Uses the exponential rule $x^x \log_e x$, treating the base as constant."),
   (r"$1 + \log_e 2$", r"Finds $\frac{d}{dx}\log_e y = \log_e x + 1$ but does not multiply by $y = 4$.")],
  r"$\log_e y = x\log_e x$, so $\frac{1}{y}\frac{dy}{dx} = \log_e x + 1$ and $\frac{dy}{dx} = x^x(1 + \log_e x)$. At $x = 2$: $4(1 + \log_e 2)$.",
  r"Applying the power rule or the exponential rule when both base and exponent vary.",
  "U07-D-logdiff-xx", "One logarithmic differentiation and substitution.",
  check=_c006, values=[4*(1 + log(2)), 4, 4*log(2), 1 + log(2)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 007
def _c007():
    return diff(x**3*log(x), x, 2).subs(x, 1)
q("U07-D-007", TOP_SEC, "Second derivative at a point", "Easy", "Single-step computation MCQ",
  r"If $y = x^3 \log_e x$, then $\frac{d^2y}{dx^2}$ at $x = 1$ equals",
  r"$5$",
  [(r"$3$", r"Gets $y' = 3x^2\log_e x + x^2$ correctly but then writes $y'' = 6x\log_e x + 3x$, not differentiating the $x^2$ term."),
   (r"$-6$", r"Multiplies the second derivatives of the factors: $(6x)\left(-\frac{1}{x^2}\right) = -6$ at $x = 1$."),
   (r"$4$", r"Simplifies $x^3 \cdot \frac{1}{x}$ as $x$, so $y' = 3x^2\log_e x + x$ and $y'' = 6x\log_e x + 3x + 1$.")],
  r"$y' = 3x^2\log_e x + x^2$ and $y'' = 6x\log_e x + 3x + 2x = 6x\log_e x + 5x$. At $x = 1$: $y'' = 5$.",
  r"Dropping a term when differentiating the first derivative.",
  "U07-D-second-value", "Product rule twice; short.",
  check=_c007, values=[5, 3, -6, 4], source_class=XII, cognitive="Application",
  numerical=dict(question=r"If $y = x^3 \log_e x$, then the value of $\frac{d^2y}{dx^2}$ at $x = 1$ is", answer=5))

# ---------------------------------------------------------------- 008
def _c008():
    return simplify(diff(sin(x), x)/diff(cos(x), x))
q("U07-D-008", TOP_WRT, "Sine with respect to cosine", "Easy", "Single-step computation MCQ",
  r"The derivative of $\sin x$ with respect to $\cos x$ (at points where $\sin x \ne 0$) is",
  r"$-\cot x$",
  [(r"$\cot x$", r"Takes $\frac{d}{dx}\cos x = \sin x$, losing the minus sign."),
   (r"$-\tan x$", r"Inverts the ratio, computing $\frac{d(\cos x)}{d(\sin x)}$."),
   (r"$\tan x$", r"Inverts the ratio and also loses the minus sign.")],
  r"Let $u = \sin x$, $v = \cos x$. By the chain rule $\frac{du}{dv} = \frac{du/dx}{dv/dx} = \frac{\cos x}{-\sin x} = -\cot x$.",
  r"Dividing the derivatives in the wrong order.",
  "U07-D-wrt-basic", "Single ratio of two standard derivatives.",
  check=_c008, values=[-cot(x), cot(x), -tan(x), tan(x)], source_class=XII, cognitive="Understanding")

# ---------------------------------------------------------------- 009
def _c009():
    return at(diff(log(x + sqrt(x**2 + 1)), x), Rational(3, 4))
q("U07-D-009", TOP_CH, "Logarithm of a surd expression", "Easy", "Single-step computation MCQ",
  r"If $y = \log_e\left(x + \sqrt{x^2 + 1}\right)$, then the value of $\frac{dy}{dx}$ at $x = \frac{3}{4}$ is",
  r"$\frac{4}{5}$",
  [(r"$\frac{1}{2}$", r"Writes only $\frac{1}{x + \sqrt{x^2+1}} = \frac{1}{3/4 + 5/4}$, leaving out the inner derivative."),
   (r"$\frac{8}{5}$", r"Keeps only the inner derivative $1 + \frac{x}{\sqrt{x^2+1}} = 1 + \frac{3}{5}$."),
   (r"$\frac{3}{10}$", r"Takes the inner derivative as $\frac{x}{\sqrt{x^2+1}}$ (dropping the $1$ from $\frac{d}{dx}x$): $\frac{3/5}{2}$.")],
  r"$\frac{dy}{dx} = \frac{1 + \frac{x}{\sqrt{x^2+1}}}{x + \sqrt{x^2+1}} = \frac{1}{\sqrt{x^2+1}}$. At $x = \frac{3}{4}$, $\sqrt{x^2+1} = \frac{5}{4}$, so $\frac{dy}{dx} = \frac{4}{5}$.",
  r"Not multiplying by the derivative of the inner expression.",
  "U07-D-chain-log-root", "Chain rule with a simplification.",
  check=_c009, values=[Rational(4, 5), Rational(1, 2), Rational(8, 5), Rational(3, 10)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 010
def _c010():
    Y = A_*cos(2*x) + B_*sin(2*x)
    return simplify(diff(Y, x, 2)/Y)
q("U07-D-010", TOP_SEC, "Second derivative of a trigonometric combination", "Easy", "Direct concept MCQ",
  r"If $y = A\cos 2x + B\sin 2x$, where $A$ and $B$ are constants, then $\frac{d^2y}{dx^2}$ equals",
  r"$-4y$",
  [(r"$4y$", r"Loses the sign: the second derivative of $\cos 2x$ is $-4\cos 2x$, not $4\cos 2x$."),
   (r"$-2y$", r"Applies the inner factor $2$ only once over the two differentiations."),
   (r"$-y$", r"Leaves out the inner factor $2$ in both differentiations, as for $A\cos x + B\sin x$.")],
  r"$y' = -2A\sin 2x + 2B\cos 2x$ and $y'' = -4A\cos 2x - 4B\sin 2x = -4y$.",
  r"Forgetting that each differentiation brings down the factor $2$.",
  "U07-D-second-ode-trig", "Two quick differentiations and recognising $y$.",
  check=_c010, values=[-4, 4, -2, -1], source_class=XII, cognitive="Understanding")

# ---------------------------------------------------------------- 011
def _c011():
    return simplify(diff(sin(x)/(1 + cos(x)), x))
q("U07-D-011", TOP_PQ, "Quotient rule with trigonometric functions", "Easy", "Single-step computation MCQ",
  r"For $\cos x \ne -1$, the derivative of $\frac{\sin x}{1 + \cos x}$ with respect to $x$ is",
  r"$\frac{1}{1 + \cos x}$",
  [(r"$-\frac{1}{1 + \cos x}$", r"Writes the quotient rule numerator in reverse order, $u v' - v u'$."),
   (r"$\frac{\cos x + \cos 2x}{(1 + \cos x)^2}$", r"Takes $\frac{d}{dx}\cos x = \sin x$, so the numerator becomes $\cos x(1+\cos x) - \sin^2 x$."),
   (r"$-\cot x$", r"Divides the derivative of the numerator by that of the denominator: $\frac{\cos x}{-\sin x}$.")],
  r"$\frac{\cos x(1 + \cos x) - \sin x(-\sin x)}{(1+\cos x)^2} = \frac{\cos x + \cos^2 x + \sin^2 x}{(1+\cos x)^2} = \frac{1 + \cos x}{(1+\cos x)^2} = \frac{1}{1+\cos x}$.",
  r"Sign errors inside the quotient rule.",
  "U07-D-quotient-trig", "Quotient rule plus the identity $\\sin^2 x + \\cos^2 x = 1$.",
  check=_c011, values=[1/(1 + cos(x)), -1/(1 + cos(x)), (cos(x) + cos(2*x))/(1 + cos(x))**2, -cot(x)],
  source_class="XI", cognitive="Application")

# ---------------------------------------------------------------- 012
def _c012():
    return at(diff(atan(exp(x)), x), log(2))
q("U07-D-012", TOP_INV, "Inverse tangent of an exponential", "Easy", "Single-step computation MCQ",
  r"If $f(x) = \tan^{-1}\left(e^{x}\right)$, then $f'(\log_e 2)$ equals",
  r"$\frac{2}{5}$",
  [(r"$\frac{1}{5}$", r"Leaves out the chain factor $e^x = 2$: $\frac{1}{1 + e^{2x}} = \frac{1}{5}$."),
   (r"$\frac{2}{3}$", r"Uses $\frac{u'}{1+u}$, forgetting to square $u = e^x$: $\frac{2}{1+2}$."),
   (r"$\frac{2\sqrt{5}}{5}$", r"Uses the pattern $\frac{u'}{\sqrt{1+u^2}}$ (the derivative of $\log_e(u + \sqrt{1+u^2})$): $\frac{2}{\sqrt{5}} = \frac{2\sqrt{5}}{5}$.")],
  r"$f'(x) = \frac{e^x}{1 + e^{2x}}$. At $x = \log_e 2$, $e^x = 2$, so $f'(\log_e 2) = \frac{2}{1+4} = \frac{2}{5}$.",
  r"Forgetting the chain factor or the square in the inverse tangent formula.",
  "U07-D-invtrig-direct", "One formula with one chain factor.",
  check=_c012, values=[Rational(2, 5), Rational(1, 5), Rational(2, 3), 2/sqrt(5)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 013
def _c013():
    return simplify(diff(log(x**2 + 1, 2), x).subs(x, 1))
q("U07-D-013", TOP_CH, "Logarithm to base 2", "Easy", "Single-step computation MCQ",
  r"If $y = \log_2 (x^2 + 1)$, then the value of $\frac{dy}{dx}$ at $x = 1$ is",
  r"$\frac{1}{\log_e 2}$",
  [(r"$1$", r"Treats $\log_2$ as $\log_e$, so gets $\frac{2x}{x^2+1} = 1$."),
   (r"$\log_e 2$", r"Multiplies by $\log_e 2$ instead of dividing: $\frac{2x\log_e 2}{x^2+1}$."),
   (r"$\frac{1}{2\log_e 2}$", r"Leaves out the chain factor $2x$: $\frac{1}{(x^2+1)\log_e 2} = \frac{1}{2\log_e 2}$.")],
  r"$y = \frac{\log_e(x^2+1)}{\log_e 2}$, so $\frac{dy}{dx} = \frac{2x}{(x^2+1)\log_e 2}$. At $x = 1$ this is $\frac{2}{2\log_e 2} = \frac{1}{\log_e 2}$.",
  r"Forgetting the change of base factor $\frac{1}{\log_e 2}$.",
  "U07-D-chain-log-base", "Change of base and one chain factor.",
  check=_c013, values=[1/log(2), 1, log(2), 1/(2*log(2))], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    fval = {2: 3}
    fp = {1: 5, 2: 4}
    g = {1: 2}
    gp = {1: -1}
    return fp[g[1]]*gp[1]
q("U07-D-014", TOP_CH, "Chain rule from tabulated values", "Easy", "Single-step computation MCQ",
  r"Let $f$ and $g$ be differentiable functions with $g(1) = 2$, $g'(1) = -1$, $f(2) = 3$, $f'(1) = 5$ and $f'(2) = 4$. If $h(x) = f(g(x))$, then $h'(1)$ equals",
  r"$-4$",
  [(r"$-5$", r"Evaluates $f'$ at $1$ instead of at $g(1) = 2$: $f'(1)g'(1) = -5$."),
   (r"$4$", r"Writes $h'(1) = f'(g(1))$ and leaves out the factor $g'(1)$."),
   (r"$-3$", r"Multiplies $f(g(1)) = 3$ by $g'(1)$, using $f$ in place of $f'$.")],
  r"$h'(x) = f'(g(x))\,g'(x)$, so $h'(1) = f'(g(1))\,g'(1) = f'(2)\cdot(-1) = 4(-1) = -4$.",
  r"Evaluating the outer derivative at $x$ instead of at $g(x)$.",
  "U07-D-chain-table", "One application of the chain rule with a table.",
  check=_c014, values=[-4, -5, 4, -3], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 015
def _c015():
    return diff((x + 1)*(x + 2)*(x + 3), x).subs(x, 0)
q("U07-D-015", TOP_PQ, "Product of three factors", "Easy", "Single-step computation MCQ",
  r"If $y = (x+1)(x+2)(x+3)$, then the value of $\frac{dy}{dx}$ at $x = 0$ is",
  r"$11$",
  [(r"$1$", r"Multiplies the derivatives of the three factors, $1 \cdot 1 \cdot 1$."),
   (r"$\frac{11}{6}$", r"Finds $\frac{y'}{y} = 1 + \frac{1}{2} + \frac{1}{3}$ by logarithms but does not multiply by $y(0) = 6$."),
   (r"$9$", r"Uses only two of the three product-rule terms: $(x+2)(x+3) + (x+1)(x+3) = 6 + 3$.")],
  r"$y' = (x+2)(x+3) + (x+1)(x+3) + (x+1)(x+2)$. At $x = 0$: $6 + 3 + 2 = 11$.",
  r"Missing a term in the product rule for three factors.",
  "U07-D-product-three", "Product rule for three factors, one substitution.",
  check=_c015, values=[11, 1, Rational(11, 6), 9], source_class="XI", cognitive="Application",
  numerical=dict(question=r"If $y = (x+1)(x+2)(x+3)$, then the value of $\frac{dy}{dx}$ at $x = 0$ is", answer=11))

# ---------------------------------------------------------------- 016
def _c016():
    s1 = simplify(diff(log(E, x), x) - 1/(x*log(x))) == 0
    s2 = simplify(diff(x**E, x) - x**E*log(x)) == 0
    return (bool(s1), bool(s2))
q("U07-D-016", TOP_CH, "Logarithm with variable base and power with constant exponent", "Easy", "Statement-based MCQ",
  r"Consider the following statements for $x > 0$, $x \ne 1$. Statement I: $\frac{d}{dx}\left(\log_x e\right) = \frac{1}{x\log_e x}$. Statement II: $\frac{d}{dx}\left(x^{e}\right) = x^{e}\log_e x$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts both: confuses $\log_x e = \frac{1}{\log_e x}$ with $\log_e(\log_e x)$, and treats $x^e$ like an exponential $a^x$."),
   (ST_TF, r"Accepts Statement I, treating $\log_x e$ as $\log_e(\log_e x)$, whose derivative is $\frac{1}{x\log_e x}$."),
   (ST_FT, r"Rejects Statement I correctly but treats $x^e$ as an exponential function, using $\frac{d}{dx}a^x = a^x\log_e a$.")],
  r"$\log_x e = \frac{1}{\log_e x}$, so its derivative is $-\frac{1}{x(\log_e x)^2}$, not $\frac{1}{x\log_e x}$; Statement I is false. Here $e$ is a constant exponent, so $\frac{d}{dx}x^e = e\,x^{e-1}$, not $x^e\log_e x$; Statement II is false.",
  r"Mixing up the power rule and the exponential rule, and misreading $\log_x e$.",
  "U07-D-stmt-rules", "Two standard rules to recall and test.",
  check=_c016, values=[(F_, F_), (T, T), (T, F_), (F_, T)], source_class=XII, cognitive="Understanding")

# ---------------------------------------------------------------- 017
def _c017():
    Y = log(exp(x)*((x - 2)/(x + 2))**Rational(3, 4))
    return at(diff(Y, x), 3)
q("U07-D-017", TOP_LOG, "Simplifying with log laws before differentiating", "Easy", "Single-step computation MCQ",
  r"If $y = \log_e\left[e^{x}\left(\frac{x-2}{x+2}\right)^{3/4}\right]$ for $x > 2$, then the value of $\frac{dy}{dx}$ at $x = 3$ is",
  r"$\frac{8}{5}$",
  [(r"$\frac{3}{5}$", r"Drops the term from $\log_e e^x = x$, keeping only $\frac{3}{4}\left(\frac{1}{x-2} - \frac{1}{x+2}\right) = \frac{3}{5}$."),
   (r"$\frac{9}{5}$", r"Forgets the factor $\frac{3}{4}$: $1 + \left(1 - \frac{1}{5}\right)$."),
   (r"$\frac{19}{10}$", r"Adds the two logarithms instead of subtracting: $1 + \frac{3}{4}\left(1 + \frac{1}{5}\right)$.")],
  r"$y = x + \frac{3}{4}\left[\log_e(x-2) - \log_e(x+2)\right]$, so $\frac{dy}{dx} = 1 + \frac{3}{4}\left(\frac{1}{x-2} - \frac{1}{x+2}\right)$. At $x = 3$: $1 + \frac{3}{4}\cdot\frac{4}{5} = \frac{8}{5}$.",
  r"Losing a term or a sign when expanding the logarithm.",
  "U07-D-log-simplify", "Log laws then term by term differentiation.",
  check=_c017, values=[Rational(8, 5), Rational(3, 5), Rational(9, 5), Rational(19, 10)], source_class=XII, cognitive="Application")


# ================================================================ MEDIUM
# ---------------------------------------------------------------- 018
def _c018():
    F = x**2 + y**2 - 25
    return idiff(F, y, x, 2).subs({x: 3, y: 4})
q("U07-D-018", TOP_IMP, "Second derivative on a circle", "Medium", "Multi-step computation MCQ",
  r"For the curve $x^2 + y^2 = 25$, the value of $\frac{d^2y}{dx^2}$ at the point $(3, 4)$ is",
  r"$-\frac{25}{64}$",
  [(r"$-\frac{1}{4}$", r"Differentiates $y' = -\frac{x}{y}$ treating $y$ as a constant, getting $-\frac{1}{y} = -\frac{1}{4}$."),
   (r"$\frac{25}{64}$", r"Drops the overall minus sign of $y' = -\frac{x}{y}$ when differentiating again."),
   (r"$-\frac{7}{64}$", r"Uses $\frac{d}{dx}\frac{x}{y} = \frac{y + x\,y'}{y^2}$ (plus sign in the quotient rule): $-\frac{4 - 9/4}{16}$.")],
  r"$y' = -\frac{x}{y}$, so $y'' = -\frac{y - x\,y'}{y^2} = -\frac{y + x^2/y}{y^2} = -\frac{x^2 + y^2}{y^3}$. At $(3,4)$: $y'' = -\frac{25}{64}$.",
  r"Treating $y$ as a constant when differentiating the first derivative.",
  "U07-D-implicit-second", "Two differentiations with substitution of $y'$ back in.",
  check=_c018, values=[Rational(-25, 64), Rational(-1, 4), Rational(25, 64), Rational(-7, 64)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    return at(diff(acos((1 - x**2)/(1 + x**2)), x), sqrt(3))
q("U07-D-019", TOP_INV, "Substitution $x = \\tan\\theta$ in inverse cosine", "Medium", "Multi-step computation MCQ",
  r"If $y = \cos^{-1}\left(\frac{1 - x^2}{1 + x^2}\right)$ for $x > 0$, then the value of $\frac{dy}{dx}$ at $x = \sqrt{3}$ is",
  r"$\frac{1}{2}$",
  [(r"$-\frac{1}{2}$", r"Uses the form $y = -2\tan^{-1} x$, which holds only for $x < 0$."),
   (r"$\frac{1}{4}$", r"Simplifies $y$ to $\tan^{-1} x$, losing the factor $2$ from $\cos 2\theta$."),
   (r"$2$", r"Gets $y = 2\theta$ with $x = \tan\theta$ but forgets to multiply by $\frac{d\theta}{dx} = \frac{1}{1+x^2}$.")],
  r"Put $x = \tan\theta$ with $0 < \theta < \frac{\pi}{2}$. Then $\frac{1 - x^2}{1+x^2} = \cos 2\theta$ with $2\theta \in (0, \pi)$, so $y = 2\theta = 2\tan^{-1}x$. Hence $\frac{dy}{dx} = \frac{2}{1+x^2} = \frac{2}{4} = \frac{1}{2}$ at $x = \sqrt{3}$.",
  r"Ignoring the range of $2\theta$ when simplifying, or forgetting $\frac{d\theta}{dx}$.",
  "U07-D-invtrig-sub-2tan", "Substitution, range check, then differentiation.",
  check=_c019, values=[Rational(1, 2), Rational(-1, 2), Rational(1, 4), 2], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 020
def _c020():
    return at(diff(atan(cos(x)/(1 + sin(x))), x), pi/6)
q("U07-D-020", TOP_INV, "Half-angle simplification inside inverse tangent", "Medium", "Multi-step computation MCQ",
  r"If $y = \tan^{-1}\left(\frac{\cos x}{1 + \sin x}\right)$ for $-\frac{\pi}{2} < x < \frac{\pi}{2}$, then $\frac{dy}{dx}$ equals",
  r"$-\frac{1}{2}$",
  [(r"$\frac{1}{2}$", r"Writes the ratio as $\tan\left(\frac{\pi}{4} + \frac{x}{2}\right)$, a sign slip in the half-angle form."),
   (r"$-1$", r"Writes the ratio as $\tan\left(\frac{\pi}{4} - x\right)$, losing the half angle."),
   (r"$1$", r"Writes the ratio as $\tan\left(\frac{\pi}{4} + x\right)$, making both slips.")],
  r"$\frac{\cos x}{1+\sin x} = \frac{\cos^2\frac{x}{2} - \sin^2\frac{x}{2}}{\left(\cos\frac{x}{2} + \sin\frac{x}{2}\right)^2} = \frac{1 - \tan\frac{x}{2}}{1 + \tan\frac{x}{2}} = \tan\left(\frac{\pi}{4} - \frac{x}{2}\right)$. Since $\frac{\pi}{4} - \frac{x}{2} \in \left(0, \frac{\pi}{2}\right)$, $y = \frac{\pi}{4} - \frac{x}{2}$ and $\frac{dy}{dx} = -\frac{1}{2}$.",
  r"Mishandling half-angle identities before differentiating.",
  "U07-D-invtrig-sub-trig", "Trigonometric simplification and a principal-range check before a one-line derivative.",
  check=_c020, values=[Rational(-1, 2), Rational(1, 2), -1, 1], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 021
def _c021():
    return simplify(diff(x**log(x), x).subs(x, exp(2)))
q("U07-D-021", TOP_LOG, "Power with logarithmic exponent", "Medium", "Multi-step computation MCQ",
  r"If $y = x^{\log_e x}$ for $x > 0$, then the value of $\frac{dy}{dx}$ at $x = e^2$ is",
  r"$4e^2$",
  [(r"$2e^2$", r"Uses the power rule $\log_e x \cdot x^{\log_e x - 1} = 2(e^2)^1$, treating the exponent as constant."),
   (r"$4e^4$", r"Writes $\frac{d}{dx}(\log_e x)^2 = 2\log_e x$, leaving out the factor $\frac{1}{x}$: $e^4 \cdot 4$."),
   (r"$\frac{4}{e^2}$", r"Finds $\frac{d}{dx}\log_e y = \frac{2\log_e x}{x}$ but does not multiply by $y = e^4$.")],
  r"$\log_e y = (\log_e x)^2$, so $\frac{y'}{y} = \frac{2\log_e x}{x}$ and $y' = x^{\log_e x}\cdot\frac{2\log_e x}{x}$. At $x = e^2$: $y = e^4$, so $y' = e^4 \cdot \frac{4}{e^2} = 4e^2$.",
  r"Using the power rule when the exponent is a function of $x$.",
  "U07-D-logdiff-xlnx", "Logarithmic differentiation with chain rule and evaluation of a power.",
  check=_c021, values=[4*exp(2), 2*exp(2), 4*exp(4), 4*exp(-2)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 022
def _c022():
    Y = (1 + x)*(1 + x**2)*(1 + x**4)*(1 + x**8)
    return diff(Y, x).subs(x, 1)
q("U07-D-022", TOP_LOG, "Long product evaluated by logarithms", "Medium", "Multi-step computation MCQ",
  r"If $y = (1+x)(1+x^2)(1+x^4)(1+x^8)$, then the value of $\frac{dy}{dx}$ at $x = 1$ is",
  r"$120$",
  [(r"$\frac{15}{2}$", r"Finds $\frac{y'}{y} = \frac{1}{2} + \frac{2}{2} + \frac{4}{2} + \frac{8}{2}$ but does not multiply by $y(1) = 16$."),
   (r"$64$", r"Multiplies the derivatives of the four factors at $x = 1$: $1 \cdot 2 \cdot 4 \cdot 8$."),
   (r"$15$", r"Adds the derivatives of the factors, $1 + 2 + 4 + 8$, ignoring that each term carries the other three factors.")],
  r"$\log_e y = \sum \log_e(1 + x^{2^r})$, so $\frac{y'}{y} = \frac{1}{1+x} + \frac{2x}{1+x^2} + \frac{4x^3}{1+x^4} + \frac{8x^7}{1+x^8}$. At $x = 1$: $\frac{y'}{y} = \frac{1+2+4+8}{2} = \frac{15}{2}$ and $y = 16$, so $y' = 120$.",
  r"Forgetting to multiply back by $y$ in logarithmic differentiation.",
  "U07-D-product-telescoping", "Logarithmic differentiation of four factors and evaluation.",
  check=_c022, values=[120, Rational(15, 2), 64, 15], source_class=XII, cognitive="Application",
  numerical=dict(question=r"If $y = (1+x)(1+x^2)(1+x^4)(1+x^8)$, then the value of $\frac{dy}{dx}$ at $x = 1$ is", answer=120))

# ---------------------------------------------------------------- 023
def _c023():
    Y1 = asin(x)
    s1 = simplify((1 - x**2)*diff(Y1, x, 2) - x*diff(Y1, x)) == 0
    Y2 = atan(x)
    s2 = simplify((1 + x**2)*diff(Y2, x, 2) - 2*x*diff(Y2, x)) == 0
    return (bool(s1), bool(s2))
q("U07-D-023", TOP_SEC, "Differential relations of inverse trigonometric functions", "Medium", "Statement-based MCQ",
  r"Statement I: If $y = \sin^{-1}x$ for $|x| < 1$, then $(1 - x^2)\frac{d^2y}{dx^2} - x\frac{dy}{dx} = 0$. Statement II: If $y = \tan^{-1}x$, then $(1 + x^2)\frac{d^2y}{dx^2} = 2x\frac{dy}{dx}$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II by losing the minus sign in $y'' = -\frac{2x}{(1+x^2)^2}$."),
   (ST_FF, r"Rejects Statement I, typically from a sign error in $y'' = \frac{x}{(1-x^2)^{3/2}}$, and also rejects Statement II."),
   (ST_FT, r"Rejects Statement I by a sign error in $y''$ and accepts Statement II by another sign error.")],
  r"For $y = \sin^{-1}x$: $y' = (1-x^2)^{-1/2}$, $y'' = x(1-x^2)^{-3/2}$, so $(1-x^2)y'' = \frac{x}{\sqrt{1-x^2}} = x y'$; Statement I is true. For $y = \tan^{-1}x$: $y' = \frac{1}{1+x^2}$, $y'' = -\frac{2x}{(1+x^2)^2}$, so $(1+x^2)y'' = -2x y'$, not $2xy'$; Statement II is false.",
  r"Sign errors when differentiating negative powers.",
  "U07-D-second-relation-stmt", "Two second derivatives to compute and compare.",
  check=_c023, values=[(T, F_), (T, T), (F_, F_), (F_, T)], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 024
def _c024():
    Y = exp(x)*sin(x)
    expr = diff(Y, x, 2) + k*diff(Y, x) + 2*Y
    sol = solve([expr.subs(x, 0), expr.subs(x, pi/2)], k, dict=True)
    kv = sol[0][k]
    assert simplify(expr.subs(k, kv)) == 0
    return kv
q("U07-D-024", TOP_SEC, "Constant in a second order relation", "Medium", "Inverse/parameter MCQ",
  r"If $y = e^{x}\sin x$ satisfies $\frac{d^2y}{dx^2} + k\frac{dy}{dx} + 2y = 0$ for all real $x$, then $k$ equals",
  r"$-2$",
  [(r"$2$", r"Finds $y(0) = 0$, $y'(0) = 1$, $y''(0) = 2$ correctly but solves $2 + k = 0$ as $k = 2$, a sign slip when transposing."),
   (r"$-1$", r"Takes $y'' = e^{x}\cos x$ (keeping only one of the two $\cos x$ terms), so at $x = 0$: $1 + k = 0$."),
   (r"$1$", r"Takes $y'' = e^{x}\cos x$ (keeping only one of the two $\cos x$ terms), so $1 + k = 0$ at $x = 0$, and then solves this as $k = 1$ by a sign slip.")],
  r"$y' = e^{x}(\sin x + \cos x)$ and $y'' = e^{x}(\sin x + \cos x) + e^{x}(\cos x - \sin x) = 2e^{x}\cos x$. Then $y'' - 2y' + 2y = 2e^x\cos x - 2e^x(\sin x + \cos x) + 2e^x\sin x = 0$, so $k = -2$.",
  r"Dropping a term in the product rule for $y''$.",
  "U07-D-second-ode-exp", "Two product-rule differentiations and matching coefficients.",
  check=_c024, values=[-2, 2, -1, 1], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 025
def _c025():
    Y = asin(x)**2
    return simplify((1 - x**2)*diff(Y, x, 2) - x*diff(Y, x))
q("U07-D-025", TOP_SEC, "Relation for the square of inverse sine", "Medium", "Multi-step computation MCQ",
  r"If $y = \left(\sin^{-1}x\right)^2$ for $|x| < 1$, then $(1 - x^2)\frac{d^2y}{dx^2} - x\frac{dy}{dx}$ equals",
  r"$2$",
  [(r"$0$", r"Uses the relation $(1-x^2)y'' - xy' = 0$ that holds for $y = \sin^{-1}x$, not for its square."),
   (r"$4$", r"Differentiates $(1-x^2)(y')^2 = 4y$ to $2(1-x^2)y'y'' - 2x(y')^2 = 4y'$ and divides by $y'$ only, not by $2y'$."),
   (r"$1$", r"Writes $y' = \frac{\sin^{-1}x}{\sqrt{1-x^2}}$, missing the factor $2$ from the power.")],
  r"$y' = \frac{2\sin^{-1}x}{\sqrt{1-x^2}}$, so $(1-x^2)(y')^2 = 4y$. Differentiating: $2(1-x^2)y'y'' - 2x(y')^2 = 4y'$. Dividing by $2y'$ gives $(1-x^2)y'' - xy' = 2$.",
  r"Not cancelling the common factor $2y'$ completely.",
  "U07-D-second-invtrig", "Square-and-differentiate method with a cancellation.",
  check=_c025, values=[2, 0, 4, 1], source_class=XII, cognitive="Application",
  numerical=dict(question=r"If $y = \left(\sin^{-1}x\right)^2$ for $|x| < 1$, then the value of $(1 - x^2)\frac{d^2y}{dx^2} - x\frac{dy}{dx}$ is", answer=2))

# ---------------------------------------------------------------- 026
def _c026():
    u = atan(x); v = asin(2*x/(1 + x**2))
    return at(diff(u, x)/diff(v, x), Rational(1, 3))
q("U07-D-026", TOP_WRT, "Inverse tangent with respect to an inverse sine", "Medium", "Multi-step computation MCQ",
  r"For $-1 < x < 1$, the derivative of $\tan^{-1}x$ with respect to $\sin^{-1}\left(\frac{2x}{1+x^2}\right)$ is",
  r"$\frac{1}{2}$",
  [(r"$2$", r"Inverts the ratio, finding the derivative of $\sin^{-1}\left(\frac{2x}{1+x^2}\right)$ with respect to $\tan^{-1}x$."),
   (r"$-\frac{1}{2}$", r"Uses the form $\pi - 2\tan^{-1}x$, which holds only for $x > 1$."),
   (r"$1$", r"Simplifies $\sin^{-1}\left(\frac{2x}{1+x^2}\right)$ to $\tan^{-1}x$, losing the factor $2$.")],
  r"With $x = \tan\theta$, $|\theta| < \frac{\pi}{4}$, we get $\frac{2x}{1+x^2} = \sin 2\theta$ with $2\theta \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$, so $v = 2\tan^{-1}x$. With $u = \tan^{-1}x$, $\frac{du}{dv} = \frac{du/dx}{dv/dx} = \frac{1/(1+x^2)}{2/(1+x^2)} = \frac{1}{2}$.",
  r"Ignoring the interval when simplifying the inverse sine.",
  "U07-D-wrt-invtrig", "Substitution with range check, then a ratio of derivatives.",
  check=_c026, values=[Rational(1, 2), 2, Rational(-1, 2), 1], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 027
def _c027():
    u = asec(1/(2*x**2 - 1)); v = sqrt(1 - x**2)
    return at(diff(u, x)/diff(v, x), Rational(1, 2))
q("U07-D-027", TOP_WRT, "Inverse secant with respect to a surd", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < \frac{1}{\sqrt{2}}$, the derivative of $\sec^{-1}\left(\frac{1}{2x^2 - 1}\right)$ with respect to $\sqrt{1 - x^2}$, evaluated at $x = \frac{1}{2}$, is",
  r"$4$",
  [(r"$\frac{1}{4}$", r"Inverts the ratio, differentiating $\sqrt{1-x^2}$ with respect to the inverse secant."),
   (r"$-4$", r"Takes $\frac{d}{dx}\sqrt{1-x^2} = \frac{x}{\sqrt{1-x^2}}$, losing the minus sign."),
   (r"$2$", r"Simplifies $\cos^{-1}(2x^2 - 1)$ to $\cos^{-1}x$, losing the factor $2$, so the ratio becomes $\frac{1}{x}$.")],
  r"$\sec^{-1}\left(\frac{1}{2x^2-1}\right) = \cos^{-1}(2x^2 - 1)$. With $x = \cos\theta$, $\theta \in \left(\frac{\pi}{4}, \frac{\pi}{2}\right)$, this is $\cos^{-1}(\cos 2\theta) = 2\theta = 2\cos^{-1}x$, with derivative $-\frac{2}{\sqrt{1-x^2}}$. Also $\frac{d}{dx}\sqrt{1-x^2} = -\frac{x}{\sqrt{1-x^2}}$. The ratio is $\frac{2}{x} = 4$ at $x = \frac{1}{2}$.",
  r"Losing a factor or a sign when simplifying before taking the ratio.",
  "U07-D-wrt-mixed", "Conversion of $\\sec^{-1}$ to $\\cos^{-1}$, substitution and a ratio.",
  check=_c027, values=[4, Rational(1, 4), -4, 2], source_class=XII, cognitive="Application",
  numerical=dict(question=r"For $0 < x < \frac{1}{\sqrt{2}}$, the derivative of $\sec^{-1}\left(\frac{1}{2x^2 - 1}\right)$ with respect to $\sqrt{1 - x^2}$, evaluated at $x = \frac{1}{2}$, is", answer=4))

# ---------------------------------------------------------------- 028
def _c028():
    sol = solve(Eq(y*log(x), x - y), y)[0]
    return simplify(diff(sol, x).subs(x, E))
q("U07-D-028", TOP_IMP, "Exponential equation solved for $y$", "Medium", "Multi-step computation MCQ",
  r"If $x^{y} = e^{x - y}$ for $x > 0$, then the value of $\frac{dy}{dx}$ at $x = e$ is",
  r"$\frac{1}{4}$",
  [(r"$\frac{1}{2}$", r"Writes $\frac{dy}{dx} = \frac{\log_e x}{1 + \log_e x}$, forgetting to square the denominator in the quotient rule."),
   (r"$-\frac{1}{4}$", r"Reverses the order in the quotient rule numerator for $y = \frac{x}{1+\log_e x}$."),
   (r"$\frac{3}{4}$", r"Differentiates $y\log_e x = x - y$ with a sign slip, getting $y'(1 + \log_e x) = 1 + \frac{y}{x}$, then uses $y(e) = \frac{e}{2}$.")],
  r"Taking logarithms, $y\log_e x = x - y$, so $y = \frac{x}{1+\log_e x}$. Then $\frac{dy}{dx} = \frac{(1+\log_e x) - x\cdot\frac{1}{x}}{(1+\log_e x)^2} = \frac{\log_e x}{(1+\log_e x)^2}$, which equals $\frac{1}{4}$ at $x = e$.",
  r"Quotient rule errors after solving for $y$.",
  "U07-D-implicit-exp-log", "Taking logarithms, solving for $y$, quotient rule.",
  check=_c028, values=[Rational(1, 4), Rational(1, 2), Rational(-1, 4), Rational(3, 4)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 029
def _c029():
    return simplify(idiff(y**2 - y - sin(x), y, x))
q("U07-D-029", TOP_IMP, "Infinite nested radical", "Medium", "Multi-step computation MCQ",
  r"If $y = \sqrt{\sin x + \sqrt{\sin x + \sqrt{\sin x + \cdots}}}$ (to infinity, with $y > 0$ and $2y \ne 1$), then $\frac{dy}{dx}$ equals",
  r"$\frac{\cos x}{2y - 1}$",
  [(r"$\frac{\cos x}{2y}$", r"Squares to $y^2 = \sin x$, ignoring that the nested part equals $y$ again."),
   (r"$\frac{\cos x}{2y + 1}$", r"Transposes $y'$ with the wrong sign: $2y\,y' + y' = \cos x$."),
   (r"$\frac{2y - 1}{\cos x}$", r"Computes $\frac{dx}{dy}$ and stops there.")],
  r"The nested part equals $y$, so $y^2 = \sin x + y$. Differentiating, $2y\,y' = \cos x + y'$, so $y'(2y - 1) = \cos x$ and $\frac{dy}{dx} = \frac{\cos x}{2y-1}$.",
  r"Not recognising the self-similar part of the radical.",
  "U07-D-implicit-infinite", "Recognising the repeated structure then implicit differentiation.",
  check=_c029, values=[cos(x)/(2*y - 1), cos(x)/(2*y), cos(x)/(2*y + 1), (2*y - 1)/cos(x)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 030
def _c030():
    f = x**3 + x + 1
    r0 = [s for s in solve(Eq(f, 3), x) if s.is_real][0]
    return 1/diff(f, x).subs(x, r0)
q("U07-D-030", TOP_CH, "Derivative of an inverse function", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = x^3 + x + 1$ and let $g$ be the inverse of $f$. Then $g'(3)$ equals",
  r"$\frac{1}{4}$",
  [(r"$\frac{1}{28}$", r"Uses $\frac{1}{f'(3)}$, evaluating $f'$ at $3$ instead of at $g(3) = 1$."),
   (r"$4$", r"Takes $g'(3) = f'(1)$, forgetting the reciprocal."),
   (r"$28$", r"Takes $g'(3) = f'(3)$, forgetting both the reciprocal and the point $g(3)$.")],
  r"$f(1) = 3$, so $g(3) = 1$. Differentiating $f(g(x)) = x$ gives $f'(g(x))\,g'(x) = 1$, so $g'(3) = \frac{1}{f'(1)} = \frac{1}{3 + 1} = \frac{1}{4}$.",
  r"Evaluating $f'$ at the wrong point.",
  "U07-D-inverse-fn-derivative", "Find the preimage, then the chain rule on $f(g(x)) = x$.",
  check=_c030, values=[Rational(1, 4), Rational(1, 28), 4, 28], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 031
def _c031():
    f1, fp1, g1, gp1 = 2, 3, -1, 4
    t = Symbol('t')
    F = f1 + fp1*(t - 1)          # any differentiable f with the given f(1), f'(1)
    G = lambda s: g1 + gp1*(s - 1)  # any g with the given g(1), g'(1)
    return diff(F/G(t**2), t).subs(t, 1)
q("U07-D-031", TOP_PQ, "Quotient with a composite denominator from data", "Medium", "Multi-step computation MCQ",
  r"Let $f$ and $g$ be differentiable functions with $f(1) = 2$, $f'(1) = 3$, $g(1) = -1$ and $g'(1) = 4$. If $H(x) = \frac{f(x)}{g(x^2)}$, then $H'(1)$ equals",
  r"$-19$",
  [(r"$-11$", r"Differentiates $g(x^2)$ as $g'(x^2)$, leaving out the chain factor $2x$: $\frac{3(-1) - 2(4)}{1}$."),
   (r"$19$", r"Writes the quotient rule numerator in reverse order."),
   (r"$\frac{3}{8}$", r"Divides $f'(1)$ by the derivative of the denominator, $2g'(1) = 8$.")],
  r"$\frac{d}{dx}g(x^2) = 2x\,g'(x^2)$. So $H'(1) = \frac{f'(1)g(1) - f(1)\cdot 2g'(1)}{g(1)^2} = \frac{3(-1) - 2\cdot 8}{1} = -19$.",
  r"Forgetting the chain factor inside the quotient rule.",
  "U07-D-quotient-table", "Quotient rule combined with the chain rule using tabulated data.",
  check=_c031, values=[-19, -11, 19, Rational(3, 8)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 032
def _c032():
    Y = exp(2*asin(x))
    return simplify(((1 - x**2)*diff(Y, x, 2) - x*diff(Y, x))/Y)
q("U07-D-032", TOP_SEC, "Relation for an exponential of inverse sine", "Medium", "Inverse/parameter MCQ",
  r"If $y = e^{2\sin^{-1}x}$ for $|x| < 1$ and $(1 - x^2)\frac{d^2y}{dx^2} - x\frac{dy}{dx} = ky$, then $k$ equals",
  r"$4$",
  [(r"$2$", r"Takes $k = m$ instead of $m^2$ for $y = e^{m\sin^{-1}x}$, missing that the factor $2$ appears twice."),
   (r"$8$", r"Differentiates $(1-x^2)(y')^2 = 4y^2$ to $2(1-x^2)y'y'' - 2x(y')^2 = 8yy'$ and divides by $y'$ only."),
   (r"$-4$", r"Uses the relation for $y = \sin(2\sin^{-1}x)$, which is $(1-x^2)y'' - xy' = -4y$.")],
  r"$y' = \frac{2y}{\sqrt{1-x^2}}$, so $(1-x^2)(y')^2 = 4y^2$. Differentiating, $2(1-x^2)y'y'' - 2x(y')^2 = 8y\,y'$. Dividing by $2y'$: $(1-x^2)y'' - xy' = 4y$, so $k = 4$.",
  r"Incomplete cancellation after squaring and differentiating.",
  "U07-D-second-invtrig", "First derivative, squaring, second differentiation and cancellation.",
  check=_c032, values=[4, 2, 8, -4], source_class=XII, cognitive="Application",
  numerical=dict(question=r"If $y = e^{2\sin^{-1}x}$ for $|x| < 1$ and $(1 - x^2)\frac{d^2y}{dx^2} - x\frac{dy}{dx} = ky$ for all such $x$, then the value of $k$ is", answer=4))

# ---------------------------------------------------------------- 033
_Y33 = (x + 1)**2*sqrt(x - 1)/((x + 4)**3*exp(x))
def _c033():
    return diff(_Y33, x)
q("U07-D-033", TOP_LOG, "Logarithmic differentiation of a quotient", "Medium", "Multi-step computation MCQ",
  r"If $y = \frac{(x+1)^2\sqrt{x-1}}{(x+4)^3 e^{x}}$ for $x > 1$, then $\frac{dy}{dx}$ equals",
  r"$y\left(\frac{2}{x+1} + \frac{1}{2(x-1)} - \frac{3}{x+4} - 1\right)$",
  [(r"$y\left(\frac{2}{x+1} + \frac{1}{2(x-1)} - \frac{3}{x+4} + 1\right)$", r"Adds the term from $\log_e e^{x} = x$ although $e^x$ is in the denominator."),
   (r"$y\left(\frac{2}{x+1} + \frac{1}{x-1} - \frac{3}{x+4} - 1\right)$", r"Takes $\log_e\sqrt{x-1}$ as $\log_e(x-1)$, losing the factor $\frac{1}{2}$."),
   (r"$y\left(\frac{2}{x+1} + \frac{1}{2(x-1)} + \frac{3}{x+4} - 1\right)$", r"Adds $3\log_e(x+4)$ although $(x+4)^3$ is in the denominator.")],
  r"$\log_e y = 2\log_e(x+1) + \frac{1}{2}\log_e(x-1) - 3\log_e(x+4) - x$. Differentiating, $\frac{1}{y}\frac{dy}{dx} = \frac{2}{x+1} + \frac{1}{2(x-1)} - \frac{3}{x+4} - 1$; multiply by $y$.",
  r"Sign or coefficient slips when expanding the logarithm of a quotient.",
  "U07-D-logdiff-quotient", "Log expansion of four factors and term by term differentiation.",
  check=_c033, values=[_Y33*(2/(x + 1) + 1/(2*(x - 1)) - 3/(x + 4) - 1),
                       _Y33*(2/(x + 1) + 1/(2*(x - 1)) - 3/(x + 4) + 1),
                       _Y33*(2/(x + 1) + 1/(x - 1) - 3/(x + 4) - 1),
                       _Y33*(2/(x + 1) + 1/(2*(x - 1)) + 3/(x + 4) - 1)],
  source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 034
def _c034():
    return at(diff(sin(cos(x**2)), x), sqrt(pi/2))
q("U07-D-034", TOP_CH, "Three-layer composite at a point", "Medium", "Multi-step computation MCQ",
  r"If $f(x) = \sin\left(\cos\left(x^2\right)\right)$, then $f'\left(\sqrt{\frac{\pi}{2}}\right)$ equals",
  r"$-\sqrt{2\pi}$",
  [(r"$\sqrt{2\pi}$", r"Takes $\frac{d}{du}\cos u = \sin u$, losing the minus sign."),
   (r"$-1$", r"Leaves out the innermost chain factor $2x$."),
   (r"$-\sqrt{\frac{\pi}{2}}$", r"Uses $x$ instead of $2x$ as the derivative of $x^2$.")],
  r"$f'(x) = \cos\left(\cos x^2\right)\cdot\left(-\sin x^2\right)\cdot 2x$. At $x^2 = \frac{\pi}{2}$: $\cos(0)\cdot(-1)\cdot 2\sqrt{\frac{\pi}{2}} = -\sqrt{2\pi}$.",
  r"Dropping a layer of the chain rule.",
  "U07-D-chain-nested", "Three chain factors to track and evaluate.",
  check=_c034, values=[-sqrt(2*pi), sqrt(2*pi), -1, -sqrt(pi/2)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 035
def _c035():
    return simplify(diff(log(2, x), x).subs(x, 2))
q("U07-D-035", TOP_CH, "Logarithm with a variable base", "Medium", "Single-step computation MCQ",
  r"If $y = \log_{x} 2$ for $x > 0$, $x \ne 1$, then the value of $\frac{dy}{dx}$ at $x = 2$ is",
  r"$-\frac{1}{2\log_e 2}$",
  [(r"$\frac{1}{2\log_e 2}$", r"Differentiates $\log_2 x$ instead, getting $\frac{1}{x\log_e 2}$; equivalently loses the minus sign of $\frac{d}{dx}\frac{1}{u}$."),
   (r"$-\frac{1}{2}$", r"Uses $-\frac{\log_e 2}{x\log_e x}$, forgetting to square $\log_e x$ in $\frac{d}{dx}\frac{1}{\log_e x} = -\frac{1}{x(\log_e x)^2}$."),
   (r"$-\frac{\log_e 2}{2}$", r"Treats $\frac{d}{dx}\frac{1}{\log_e x}$ as $-\frac{1}{x}$, so $y' = -\frac{\log_e 2}{x}$.")],
  r"$y = \frac{\log_e 2}{\log_e x}$, so $\frac{dy}{dx} = -\frac{\log_e 2}{x(\log_e x)^2}$. At $x = 2$: $-\frac{\log_e 2}{2(\log_e 2)^2} = -\frac{1}{2\log_e 2}$.",
  r"Confusing $\log_x 2$ with $\log_2 x$.",
  "U07-D-chain-log-base", "Change of base then derivative of a reciprocal.",
  check=_c035, values=[-1/(2*log(2)), 1/(2*log(2)), Rational(-1, 2), -log(2)/2], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 036
def _c036():
    return at(diff(atan((sqrt(1 + x**2) - 1)/x), x), sqrt(3))
q("U07-D-036", TOP_INV, "Half-angle substitution in inverse tangent", "Medium", "Multi-step computation MCQ",
  r"If $f(x) = \tan^{-1}\left(\frac{\sqrt{1+x^2} - 1}{x}\right)$ for $x \ne 0$, then $f'\left(\sqrt{3}\right)$ equals",
  r"$\frac{1}{8}$",
  [(r"$\frac{1}{4}$", r"Simplifies $f(x)$ to $\tan^{-1}x$, losing the factor $\frac{1}{2}$."),
   (r"$\frac{1}{2}$", r"Gets $f = \frac{\theta}{2}$ with $x = \tan\theta$ but forgets $\frac{d\theta}{dx} = \frac{1}{1+x^2}$."),
   (r"$-\frac{1}{8}$", r"Simplifies $\frac{\sec\theta - 1}{\tan\theta}$ to $\cot\frac{\theta}{2}$, so $f = \frac{\pi}{2} - \frac{\theta}{2}$.")],
  r"Put $x = \tan\theta$, $\theta \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$, $\theta \ne 0$. Then $\frac{\sec\theta - 1}{\tan\theta} = \frac{1 - \cos\theta}{\sin\theta} = \tan\frac{\theta}{2}$, and $\frac{\theta}{2}$ is in the principal range, so $f(x) = \frac{1}{2}\tan^{-1}x$. Hence $f'(x) = \frac{1}{2(1+x^2)}$ and $f'(\sqrt{3}) = \frac{1}{8}$.",
  r"Mis-simplifying the half-angle ratio.",
  "U07-D-invtrig-sub-half", "Substitution and half-angle identity before differentiating.",
  check=_c036, values=[Rational(1, 8), Rational(1, 4), Rational(1, 2), Rational(-1, 8)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 037
def _c037():
    return simplify(idiff(log(x**2 + y**2) - 2*atan(y/x), y, x))
q("U07-D-037", TOP_IMP, "Implicit relation with logarithm and inverse tangent", "Medium", "Multi-step computation MCQ",
  r"If $\log_e\left(x^2 + y^2\right) = 2\tan^{-1}\left(\frac{y}{x}\right)$ (with $x \ne 0$ and $x \ne y$), then $\frac{dy}{dx}$ equals",
  r"$\frac{x + y}{x - y}$",
  [(r"$\frac{x - y}{x + y}$", r"Solves for $\frac{dx}{dy}$ instead of $\frac{dy}{dx}$."),
   (r"$\frac{y - x}{x + y}$", r"Writes $\frac{d}{dx}\frac{y}{x} = \frac{y - x\,y'}{x^2}$ (reversed quotient rule), leading to $x + yy' = y - xy'$."),
   (r"$\frac{x + y}{y - x}$", r"Transposes the $y'$ terms with a sign slip, getting $y'(y - x) = x + y$.")],
  r"Differentiating: $\frac{2x + 2yy'}{x^2+y^2} = \frac{2}{1 + y^2/x^2}\cdot\frac{xy' - y}{x^2} = \frac{2(xy' - y)}{x^2 + y^2}$. So $x + yy' = xy' - y$, giving $y'(x - y) = x + y$ and $\frac{dy}{dx} = \frac{x+y}{x-y}$.",
  r"Quotient rule slip on $\frac{y}{x}$.",
  "U07-D-implicit-log-atan", "Chain and quotient rules inside implicit differentiation, then rearranging.",
  check=_c037, values=[(x + y)/(x - y), (x - y)/(x + y), (y - x)/(x + y), (x + y)/(y - x)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 038
def _c038():
    return at(diff(sec(x), x, 2), pi/4)
q("U07-D-038", TOP_SEC, "Second derivative of secant", "Medium", "Multi-step computation MCQ",
  r"If $y = \sec x$, then the value of $\frac{d^2y}{dx^2}$ at $x = \frac{\pi}{4}$ is",
  r"$3\sqrt{2}$",
  [(r"$2\sqrt{2}$", r"Differentiates $\sec x\tan x$ as $\sec x\cdot\sec^2 x$ only, missing the term $\sec x\tan^2 x$."),
   (r"$\sqrt{2}$", r"Keeps only $\sec x\tan^2 x$, missing the term $\sec^3 x$."),
   (r"$2 + \sqrt{2}$", r"Adds the derivatives of the factors: $\sec x\tan x + \sec^2 x$, instead of using the product rule.")],
  r"$y' = \sec x\tan x$, so $y'' = \sec x\tan^2 x + \sec^3 x$. At $\frac{\pi}{4}$: $\sqrt{2}\cdot 1 + 2\sqrt{2} = 3\sqrt{2}$.",
  r"Incomplete product rule on $\sec x\tan x$.",
  "U07-D-second-value", "Product rule on the first derivative, then evaluation.",
  check=_c038, values=[3*sqrt(2), 2*sqrt(2), sqrt(2), 2 + sqrt(2)], source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 039
q("U07-D-039", TOP_CH, "Periodicity and parity under differentiation", "Medium", "Statement-based MCQ",
  r"Let $f : \mathbb{R} \to \mathbb{R}$ be differentiable. Statement I: If $f'$ is periodic, then $f$ is periodic. Statement II: If $f$ is an even function, then $f'(0) = 0$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I by reversing the true fact that the derivative of a periodic function is periodic."),
   (ST_TF, r"Accepts Statement I and rejects Statement II, thinking an even function such as $\cos x + x^2$ could have a nonzero slope at $0$."),
   (ST_FF, r"Rejects Statement II as well, not using $f'(-x) = -f'(x)$.")],
  r"For $f(x) = x + \sin x$, $f'(x) = 1 + \cos x$ is periodic with period $2\pi$, but $f(x + 2\pi) - f(x) = 2\pi \ne 0$, so $f$ is not periodic; Statement I is false. If $f(-x) = f(x)$, differentiating gives $-f'(-x) = f'(x)$, so $f'$ is odd and $f'(0) = -f'(0)$, giving $f'(0) = 0$; Statement II is true.",
  r"Reversing the implication about periodic functions and their derivatives.",
  "U07-D-concept-even-periodic", "Needs a counterexample and a chain-rule argument.",
  check=None, values=None, source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 040
def _c040():
    d = idiff(cos(y) - x*cos(a + y), y, x)
    return simplify(d.subs(x, cos(y)/cos(a + y)))
q("U07-D-040", TOP_IMP, "Implicit trigonometric relation with a constant angle", "Medium", "Multi-step computation MCQ",
  r"If $\cos y = x\cos(a + y)$, where $a$ is a constant with $\sin a \ne 0$, then $\frac{dy}{dx}$ equals",
  r"$\frac{\cos^2(a+y)}{\sin a}$",
  [(r"$\frac{\sin a}{\cos^2(a+y)}$", r"Finds $\frac{dx}{dy}$ and stops there."),
   (r"$-\frac{\cos^2(a+y)}{\sin a}$", r"Takes $\frac{d}{dy}\cos y = \sin y$ and $\frac{d}{dy}\cos(a+y) = \sin(a+y)$, losing both minus signs, so the numerator becomes $\sin y\cos(a+y) - \cos y\sin(a+y) = -\sin a$."),
   (r"$\frac{\cos^2(a+y)}{\cos a}$", r"Simplifies $\sin(a+y)\cos y - \cos(a+y)\sin y$ as $\cos a$ by a compound-angle slip.")],
  r"Write $x = \frac{\cos y}{\cos(a+y)}$. Then $\frac{dx}{dy} = \frac{-\sin y\cos(a+y) + \cos y\sin(a+y)}{\cos^2(a+y)} = \frac{\sin(a+y-y)}{\cos^2(a+y)} = \frac{\sin a}{\cos^2(a+y)}$. Hence $\frac{dy}{dx} = \frac{\cos^2(a+y)}{\sin a}$.",
  r"Forgetting to invert $\frac{dx}{dy}$.",
  "U07-D-implicit-trig-param", "Isolating $x$, quotient rule, compound-angle identity, inversion.",
  check=_c040, values=[cos(a + y)**2/sin(a), sin(a)/cos(a + y)**2, -cos(a + y)**2/sin(a), cos(a + y)**2/cos(a)],
  source_class=XII, cognitive="Application")

# ---------------------------------------------------------------- 041
def _c041():
    Y = (x + sqrt(1 + x**2))**3
    expr = ((1 + x**2)*diff(Y, x, 2) + x*diff(Y, x))/Y
    return nsimplify(simplify(expr.subs(x, Rational(3, 4))))
q("U07-D-041", TOP_SEC, "Relation for a power of $x + \\sqrt{1+x^2}$", "Medium", "Inverse/parameter MCQ",
  r"If $y = \left(x + \sqrt{1 + x^2}\right)^3$ and $(1 + x^2)\frac{d^2y}{dx^2} + x\frac{dy}{dx} = ky$ for all real $x$, then $k$ equals",
  r"$9$",
  [(r"$3$", r"Takes $k = n$ instead of $n^2$ for $y = \left(x + \sqrt{1+x^2}\right)^n$."),
   (r"$-9$", r"Uses the sign pattern of $y = \sin(3\sin^{-1}x)$, which gives $-9y$."),
   (r"$18$", r"Differentiates $(1+x^2)(y')^2 = 9y^2$ and divides by $y'$ only, not by $2y'$.")],
  r"$y' = 3\left(x + \sqrt{1+x^2}\right)^2\left(1 + \frac{x}{\sqrt{1+x^2}}\right) = \frac{3y}{\sqrt{1+x^2}}$, so $(1+x^2)(y')^2 = 9y^2$. Differentiating, $2x(y')^2 + 2(1+x^2)y'y'' = 18y\,y'$; dividing by $2y'$ gives $(1+x^2)y'' + xy' = 9y$.",
  r"Not cancelling the factor $2y'$ fully.",
  "U07-D-second-relation-root", "Chain rule simplification, squaring and differentiating again.",
  check=_c041, values=[9, 3, -9, 18], source_class=XII, cognitive="Application",
  numerical=dict(question=r"If $y = \left(x + \sqrt{1 + x^2}\right)^3$ and $(1 + x^2)\frac{d^2y}{dx^2} + x\frac{dy}{dx} = ky$ for all real $x$, then the value of $k$ is", answer=9))

# ---------------------------------------------------------------- 042
def _c042():
    u = asin(3*x - 4*x**3); v = asin(x)
    return at(diff(u, x)/diff(v, x), Rational(1, 4))
q("U07-D-042", TOP_WRT, "Triple-angle form with respect to inverse sine", "Medium", "Multi-step computation MCQ",
  r"For $|x| < \frac{1}{2}$, the derivative of $\sin^{-1}\left(3x - 4x^3\right)$ with respect to $\sin^{-1}x$ is",
  r"$3$",
  [(r"$-3$", r"Uses the form $\pi - 3\sin^{-1}x$, which holds only for $\frac{1}{2} < x \le 1$."),
   (r"$\frac{1}{3}$", r"Inverts the ratio."),
   (r"$-\frac{1}{3}$", r"Uses the form $\pi - 3\sin^{-1}x$ and also inverts the ratio.")],
  r"Put $x = \sin\theta$ with $|\theta| < \frac{\pi}{6}$. Then $3x - 4x^3 = \sin 3\theta$ and $3\theta \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$, so $\sin^{-1}(3x - 4x^3) = 3\sin^{-1}x$. Its derivative with respect to $\sin^{-1}x$ is $3$.",
  r"Ignoring which branch of the triple-angle simplification applies.",
  "U07-D-wrt-invtrig", "Substitution with range check, then chain rule ratio.",
  check=_c042, values=[3, -3, Rational(1, 3), Rational(-1, 3)], source_class=XII, cognitive="Application",
  numerical=dict(question=r"For $|x| < \frac{1}{2}$, the derivative of $\sin^{-1}\left(3x - 4x^3\right)$ with respect to $\sin^{-1}x$ is", answer=3))

# ---------------------------------------------------------------- 043
def _c043():
    f = asin(sin(x)) + 2*acos(cos(x))
    return at(diff(f, x), 5*pi/4)
q("U07-D-043", TOP_INV, "Inverse of a function of itself outside the principal range", "Medium", "Multi-step computation MCQ",
  r"If $f(x) = \sin^{-1}(\sin x) + 2\cos^{-1}(\cos x)$, then $f'\left(\frac{5\pi}{4}\right)$ equals",
  r"$-3$",
  [(r"$3$", r"Treats $\sin^{-1}(\sin x) = x$ and $\cos^{-1}(\cos x) = x$ outside the principal ranges."),
   (r"$1$", r"Uses $\sin^{-1}(\sin x) = \pi - x$ correctly but takes $\cos^{-1}(\cos x) = x$."),
   (r"$-1$", r"Takes $\sin^{-1}(\sin x) = x$ but uses $\cos^{-1}(\cos x) = 2\pi - x$ correctly.")],
  r"For $x$ near $\frac{5\pi}{4}$: $x \in \left[\frac{\pi}{2}, \frac{3\pi}{2}\right]$ gives $\sin^{-1}(\sin x) = \pi - x$, and $x \in [\pi, 2\pi]$ gives $\cos^{-1}(\cos x) = 2\pi - x$. So $f(x) = \pi - x + 2(2\pi - x)$ and $f'(x) = -1 - 2 = -3$.",
  r"Assuming $\sin^{-1}(\sin x) = x$ for every $x$.",
  "U07-D-invtrig-principal", "Two branch identifications before a simple derivative.",
  check=_c043, values=[-3, 3, 1, -1], source_class=XII, cognitive="Analysis")


# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 044
_X44, _Y44 = Rational(1, 2), Rational(1, 3)
def _opts44(X, Yv):
    r1 = sqrt(1 - Yv**6)/sqrt(1 - X**6)
    return [X**2/Yv**2*r1, X**2/Yv**2/r1, Yv**2/X**2*r1, -X**2/Yv**2*r1]
def _c044():
    c = Symbol('c')
    F = sqrt(1 - x**6) + sqrt(1 - y**6) - c*(x**3 - y**3)
    cval = solve(F.subs({x: _X44, y: _Y44}), c)[0]
    d = -diff(F, x)/diff(F, y)
    return nsimplify(simplify(d.subs(c, cval).subs({x: _X44, y: _Y44})))
q("U07-D-044", TOP_IMP, "Implicit relation simplified by a sine substitution", "Difficult", "Multi-step computation MCQ",
  r"If $\sqrt{1 - x^6} + \sqrt{1 - y^6} = a^3\left(x^3 - y^3\right)$, where $a$ is a constant, $0 < |x| < 1$ and $0 < |y| < 1$, then $\frac{dy}{dx}$ equals",
  r"$\frac{x^2}{y^2}\sqrt{\frac{1 - y^6}{1 - x^6}}$",
  [(r"$\frac{x^2}{y^2}\sqrt{\frac{1 - x^6}{1 - y^6}}$", r"Writes $\frac{d}{dx}\sin^{-1}(x^3) = 3x^2\sqrt{1-x^6}$, multiplying by the root instead of dividing."),
   (r"$\frac{y^2}{x^2}\sqrt{\frac{1 - y^6}{1 - x^6}}$", r"Writes $\frac{d}{dx}\sin^{-1}(x^3) = \frac{1}{3x^2\sqrt{1-x^6}}$, dividing by the chain factor $3x^2$ instead of multiplying."),
   (r"$-\frac{x^2}{y^2}\sqrt{\frac{1 - y^6}{1 - x^6}}$", r"Concludes $P + Q$ is constant (sign slip in the sum-to-product step), so $dP = -dQ$.")],
  r"Put $x^3 = \sin P$, $y^3 = \sin Q$. Then $\cos P + \cos Q = a^3(\sin P - \sin Q)$ gives $2\cos\frac{P+Q}{2}\cos\frac{P-Q}{2} = 2a^3\cos\frac{P+Q}{2}\sin\frac{P-Q}{2}$, so $\cot\frac{P-Q}{2} = a^3$ and $P - Q$ is constant. Thus $\sin^{-1}(x^3) - \sin^{-1}(y^3) = $ constant; differentiating, $\frac{3x^2}{\sqrt{1-x^6}} = \frac{3y^2}{\sqrt{1-y^6}}\frac{dy}{dx}$, so $\frac{dy}{dx} = \frac{x^2}{y^2}\sqrt{\frac{1-y^6}{1-x^6}}$.",
  r"Differentiating directly without spotting the substitution, then losing track of factors.",
  "U07-D-implicit-sub", "Recognising a trigonometric substitution, sum-to-product, then implicit differentiation.",
  check=_c044, values=_opts44(_X44, _Y44), source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 045
def _o45(X):
    return [1/sqrt(1 - X**2) - 1/(2*sqrt(X - X**2)),
            1/sqrt(1 - X**2) + 1/(2*sqrt(X - X**2)),
            1/sqrt(1 - X**2) - 1/sqrt(X - X**2),
            1/sqrt(1 - X**2) - 1/sqrt(1 - X)]
def _c045():
    f = asin(x*sqrt(1 - x) - sqrt(x)*sqrt(1 - x**2))
    d = diff(f, x)
    return tuple(simplify(d.subs(x, v)) for v in (Rational(1, 4), Rational(1, 2)))
q("U07-D-045", TOP_INV, "Difference formula for inverse sine", "Difficult", "Multi-step computation MCQ",
  r"For $0 < x < 1$, the derivative of $\sin^{-1}\left(x\sqrt{1-x} - \sqrt{x}\sqrt{1-x^2}\right)$ with respect to $x$ is",
  r"$\frac{1}{\sqrt{1-x^2}} - \frac{1}{2\sqrt{x - x^2}}$",
  [(r"$\frac{1}{\sqrt{1-x^2}} + \frac{1}{2\sqrt{x - x^2}}$", r"Uses the sum formula, reading the expression as $\sin^{-1}x + \sin^{-1}\sqrt{x}$."),
   (r"$\frac{1}{\sqrt{1-x^2}} - \frac{1}{\sqrt{x - x^2}}$", r"Differentiates $\sqrt{x}$ as $\frac{1}{\sqrt{x}}$, losing the factor $\frac{1}{2}$."),
   (r"$\frac{1}{\sqrt{1-x^2}} - \frac{1}{\sqrt{1 - x}}$", r"Differentiates $\sin^{-1}\sqrt{x}$ as $\frac{1}{\sqrt{1-x}}$, leaving out the chain factor $\frac{1}{2\sqrt{x}}$.")],
  r"With $p = x$ and $q = \sqrt{x}$, both in $(0, 1)$, the expression is $p\sqrt{1-q^2} - q\sqrt{1-p^2} = \sin\left(\sin^{-1}p - \sin^{-1}q\right)$, and $\sin^{-1}p - \sin^{-1}q \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$. So the function equals $\sin^{-1}x - \sin^{-1}\sqrt{x}$, whose derivative is $\frac{1}{\sqrt{1-x^2}} - \frac{1}{\sqrt{1-x}}\cdot\frac{1}{2\sqrt{x}} = \frac{1}{\sqrt{1-x^2}} - \frac{1}{2\sqrt{x - x^2}}$.",
  r"Not recognising the difference formula, or dropping the chain factor for $\sqrt{x}$.",
  "U07-D-invtrig-sub-difference", "Recognise the identity, check its range, then chain rule.",
  check=_c045, values=[tuple(simplify(o) for o in z) for z in zip(*[_o45(Rational(1, 4)), _o45(Rational(1, 2))])],
  source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 046
def _c046():
    f = asin(2*x/(1 + x**2)) + acos((1 - x**2)/(1 + x**2))
    d = diff(f, x)
    return nsimplify(simplify(d.subs(x, 2) + d.subs(x, Rational(1, 2))))
q("U07-D-046", TOP_INV, "Branch change of $\\sin^{-1}\\frac{2x}{1+x^2}$", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = \sin^{-1}\left(\frac{2x}{1+x^2}\right) + \cos^{-1}\left(\frac{1-x^2}{1+x^2}\right)$ for $x > 0$, $x \ne 1$. Then $f'(2) + f'\left(\frac{1}{2}\right)$ equals",
  r"$\frac{16}{5}$",
  [(r"$4$", r"Uses $f(x) = 4\tan^{-1}x$ for every $x > 0$, ignoring the branch change of the inverse sine at $x = 1$."),
   (r"$\frac{12}{5}$", r"Changes the branch of both terms for $x > 1$, taking $f'(x) = -\frac{4}{1+x^2}$ there."),
   (r"$2$", r"Uses $f(x) = 2\tan^{-1}x$, counting only one of the two terms.")],
  r"With $x = \tan\theta$, $0 < \theta < \frac{\pi}{2}$: $\cos^{-1}\frac{1-x^2}{1+x^2} = 2\theta$ always, while $\sin^{-1}\frac{2x}{1+x^2} = 2\theta$ for $x < 1$ and $\pi - 2\theta$ for $x > 1$. So $f(x) = 4\tan^{-1}x$ for $0 < x < 1$ and $f(x) = \pi$ for $x > 1$. Thus $f'(2) = 0$ and $f'\left(\frac{1}{2}\right) = \frac{4}{1 + 1/4} = \frac{16}{5}$.",
  r"Assuming $\sin^{-1}\frac{2x}{1+x^2} = 2\tan^{-1}x$ for all $x$.",
  "U07-D-invtrig-sub-2tan", "Two substitutions, a branch split at $x = 1$, and evaluation on each side.",
  check=_c046, values=[Rational(16, 5), 4, Rational(12, 5), 2], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 047
def _c047():
    f = x**3 + x + 1
    r0 = [s for s in solve(Eq(f, 3), x) if s.is_real][0]
    gp = 1/diff(f, x)                 # g'(f(x)) = 1/f'(x)
    gpp = diff(gp, x)/diff(f, x)      # chain rule: d/dy = (d/dx)/(dy/dx)
    return gpp.subs(x, r0)
q("U07-D-047", TOP_CH, "Second derivative of an inverse function", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = x^3 + x + 1$ and let $g$ be the inverse of $f$. Then $g''(3)$ equals",
  r"$-\frac{3}{32}$",
  [(r"$\frac{3}{32}$", r"Differentiates $\frac{1}{f'(x)}$ as $+\frac{f''(x)}{(f'(x))^2}$, losing the minus sign."),
   (r"$-\frac{3}{8}$", r"Uses $g'' = -\frac{f''}{(f')^2}$, forgetting the extra chain factor $g' = \frac{1}{f'}$."),
   (r"$\frac{1}{6}$", r"Takes $g''(3) = \frac{1}{f''(1)}$ by analogy with $g' = \frac{1}{f'}$.")],
  r"$g(3) = 1$ since $f(1) = 3$. From $g'(y) = \frac{1}{f'(g(y))}$, $g''(y) = -\frac{f''(g(y))\,g'(y)}{(f'(g(y)))^2} = -\frac{f''(g(y))}{(f'(g(y)))^3}$. With $f'(1) = 4$ and $f''(1) = 6$: $g''(3) = -\frac{6}{64} = -\frac{3}{32}$.",
  r"Missing a chain factor when differentiating $g'(y) = \frac{1}{f'(g(y))}$ again.",
  "U07-D-inverse-fn-derivative", "Inverse function, chain rule twice, careful powers.",
  check=_c047, values=[Rational(-3, 32), Rational(3, 32), Rational(-3, 8), Rational(1, 6)], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 048
def _c048():
    F = y*log(x) - x*log(y)
    assert simplify(F.subs({x: 2, y: 4})) == 0
    return simplify(idiff(F, y, x).subs({x: 2, y: 4}))
L2 = log(2)
q("U07-D-048", TOP_IMP, "Curve $x^y = y^x$ at a non-trivial point", "Difficult", "Multi-step computation MCQ",
  r"The curve $x^{y} = y^{x}$ ($x, y > 0$) passes through the point $(2, 4)$. The value of $\frac{dy}{dx}$ at this point is",
  r"$\frac{4(\log_e 2 - 1)}{2\log_e 2 - 1}$",
  [(r"$\frac{2\log_e 2 - 1}{4(\log_e 2 - 1)}$", r"Solves for $\frac{dx}{dy}$ instead of $\frac{dy}{dx}$."),
   (r"$\frac{4\log_e 2}{2\log_e 2 - 1}$", r"Differentiates $y\log_e x$ as $y'\log_e x$ only, dropping $\frac{y}{x}$: $y'\left(\log_e 2 - \frac{1}{2}\right) = \log_e 4$."),
   (r"$\frac{2(\log_e 2 - 1)}{\log_e 2}$", r"Differentiates $x\log_e y$ as $\log_e y$ only, dropping $\frac{x}{y}y'$: $y'\log_e 2 = \log_e 4 - 2$.")],
  r"Taking logarithms, $y\log_e x = x\log_e y$. Differentiating, $y'\log_e x + \frac{y}{x} = \log_e y + \frac{x}{y}y'$, so $y' = \frac{\log_e y - \frac{y}{x}}{\log_e x - \frac{x}{y}}$. At $(2, 4)$: $y' = \frac{2\log_e 2 - 2}{\log_e 2 - \frac{1}{2}} = \frac{4(\log_e 2 - 1)}{2\log_e 2 - 1}$.",
  r"Using only one term of the product rule on each side.",
  "U07-D-implicit-xy-power", "Logarithms, product rule on both sides, then exact simplification.",
  check=_c048, values=[4*(L2 - 1)/(2*L2 - 1), (2*L2 - 1)/(4*(L2 - 1)), 4*L2/(2*L2 - 1), 2*(L2 - 1)/L2],
  source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 049
def _c049():
    return simplify(idiff(y*log(x) - log(y), y, x))
q("U07-D-049", TOP_LOG, "Infinite power tower", "Difficult", "Multi-step computation MCQ",
  r"If $y = x^{x^{x^{\cdot^{\cdot^{\cdot}}}}}$ (an infinite tower, for those $x > 0$ where it converges and $y\log_e x \ne 1$), then $\frac{dy}{dx}$ equals",
  r"$\frac{y^2}{x(1 - y\log_e x)}$",
  [(r"$\frac{y^2}{x(1 + y\log_e x)}$", r"Transposes the $y'\log_e x$ term without changing its sign."),
   (r"$\frac{y}{x(1 - \log_e x)}$", r"Differentiates $\log_e y$ as $y'$ (forgetting $\frac{1}{y}$): $y' = y'\log_e x + \frac{y}{x}$."),
   (r"$\frac{y^2}{1 - y\log_e x}$", r"Differentiates $\log_e x$ as $1$, losing the factor $\frac{1}{x}$.")],
  r"The tower satisfies $y = x^{y}$, so $\log_e y = y\log_e x$. Differentiating, $\frac{y'}{y} = y'\log_e x + \frac{y}{x}$, so $y'\left(\frac{1}{y} - \log_e x\right) = \frac{y}{x}$ and $y' = \frac{y^2}{x(1 - y\log_e x)}$.",
  r"Not recognising $y = x^y$, or forgetting $\frac{1}{y}$ from $\log_e y$.",
  "U07-D-logdiff-infinite", "Self-similar structure, logarithms, implicit product rule, rearranging.",
  check=_c049, values=[y**2/(x*(1 - y*log(x))), y**2/(x*(1 + y*log(x))), y/(x*(1 - log(x))), y**2/(1 - y*log(x))],
  source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 050
def _c050():
    Y = x**x
    return simplify(diff(Y, x, 2) - diff(Y, x)**2/Y)
q("U07-D-050", TOP_LOG, "Second derivative of $x^x$ in terms of $y$", "Difficult", "Multi-step computation MCQ",
  r"If $y = x^{x}$ for $x > 0$, then $\frac{d^2y}{dx^2} - \frac{1}{y}\left(\frac{dy}{dx}\right)^2$ equals",
  r"$\frac{y}{x}$",
  [(r"$y$", r"Writes $\frac{d}{dx}(1 + \log_e x) = 1$, so $y'' = y(1+\log_e x)^2 + y$."),
   (r"$\frac{1}{x}$", r"Differentiates $y(1 + \log_e x)$ as $y'(1+\log_e x) + \frac{1}{x}$, dropping the factor $y$ in the second term."),
   (r"$0$", r"Treats $1 + \log_e x$ as a constant, so $y'' = y(1+\log_e x)^2$.")],
  r"$y' = y(1 + \log_e x)$. Then $y'' = y'(1 + \log_e x) + \frac{y}{x} = y(1+\log_e x)^2 + \frac{y}{x}$. Since $\frac{(y')^2}{y} = y(1+\log_e x)^2$, the required expression is $\frac{y}{x}$.",
  r"Incomplete product rule on $y(1+\log_e x)$.",
  "U07-D-logdiff-xx", "Logarithmic differentiation, product rule on $y'$, and expressing the result in $y$.",
  check=_c050, values=[x**x/x, x**x, 1/x, 0], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 051
def _c051():
    Y = exp(3*atan(x))
    expr = (1 + x**2)*diff(Y, x, 2) + (p_*x + q_)*diff(Y, x)
    sol = solve([expr.subs(x, 0), expr.subs(x, 1)], [p_, q_], dict=True)[0]
    assert simplify(expr.subs(sol)) == 0
    return sol[p_] - sol[q_]
q("U07-D-051", TOP_SEC, "Coefficients in a relation for $e^{3\\tan^{-1}x}$", "Difficult", "Inverse/parameter MCQ",
  r"If $y = e^{3\tan^{-1}x}$ satisfies $(1 + x^2)\frac{d^2y}{dx^2} + (px + q)\frac{dy}{dx} = 0$ for all real $x$, where $p$ and $q$ are constants, then $p - q$ equals",
  r"$5$",
  [(r"$3$", r"Differentiates $(1+x^2)y' = 3y$ without the product rule, missing $2xy'$, so $p = 0$, $q = -3$."),
   (r"$-1$", r"Transposes $3y'$ without changing its sign, getting $p = 2$, $q = 3$."),
   (r"$4$", r"Takes $\frac{d}{dx}(1+x^2) = x$, so $p = 1$, $q = -3$.")],
  r"$y' = \frac{3y}{1+x^2}$, so $(1+x^2)y' = 3y$. Differentiating, $2xy' + (1+x^2)y'' = 3y'$, i.e. $(1+x^2)y'' + (2x - 3)y' = 0$. Since $y' \ne 0$ the coefficients are forced: $p = 2$, $q = -3$, and $p - q = 5$.",
  r"Forgetting the product rule on $(1+x^2)y'$.",
  "U07-D-second-relation-exp-atan", "Clearing the denominator, product rule, and matching coefficients.",
  check=_c051, values=[5, 3, -1, 4], source_class=XII, cognitive="Analysis",
  numerical=dict(question=r"If $y = e^{3\tan^{-1}x}$ satisfies $(1 + x^2)\frac{d^2y}{dx^2} + (px + q)\frac{dy}{dx} = 0$ for all real $x$, where $p$ and $q$ are constants, then the value of $p - q$ is", answer=5))

# ---------------------------------------------------------------- 052
def _c052():
    u = asin(2*x*sqrt(1 - x**2)); v = asin(x)
    return at(diff(u, x)/diff(v, x), Rational(4, 5))
q("U07-D-052", TOP_WRT, "Double-angle form beyond $\\frac{1}{\\sqrt{2}}$", "Difficult", "Multi-step computation MCQ",
  r"For $\frac{1}{\sqrt{2}} < x < 1$, the derivative of $\sin^{-1}\left(2x\sqrt{1 - x^2}\right)$ with respect to $\sin^{-1}x$ is",
  r"$-2$",
  [(r"$2$", r"Uses $\sin^{-1}(\sin 2\theta) = 2\theta$, which needs $|x| \le \frac{1}{\sqrt{2}}$."),
   (r"$-\frac{1}{2}$", r"Uses the correct branch but inverts the ratio."),
   (r"$\frac{1}{2}$", r"Uses the branch $2\theta$ and also inverts the ratio.")],
  r"Put $x = \sin\theta$; for $\frac{1}{\sqrt{2}} < x < 1$, $\theta \in \left(\frac{\pi}{4}, \frac{\pi}{2}\right)$ and $2\theta \in \left(\frac{\pi}{2}, \pi\right)$. Then $2x\sqrt{1-x^2} = \sin 2\theta$ and $\sin^{-1}(\sin 2\theta) = \pi - 2\theta = \pi - 2\sin^{-1}x$. Its derivative with respect to $\sin^{-1}x$ is $-2$.",
  r"Applying the principal-range form outside its interval.",
  "U07-D-wrt-branch", "Substitution, branch identification, chain rule ratio.",
  check=_c052, values=[-2, 2, Rational(-1, 2), Rational(1, 2)], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 053
def _c053():
    F = x**2 - x*y + y**2 - 3
    assert F.subs({x: 1, y: 2}) == 0
    return simplify(idiff(F, y, x, 2).subs({x: 1, y: 2}))
q("U07-D-053", TOP_IMP, "Second derivative on an ellipse at a turning point", "Difficult", "Multi-step computation MCQ",
  r"For the curve $x^2 - xy + y^2 = 3$, the value of $\frac{d^2y}{dx^2}$ at the point $(1, 2)$ is",
  r"$-\frac{2}{3}$",
  [(r"$-\frac{1}{2}$", r"Differentiates the term $-x\,y'$ as $-y'$, losing $-x\,y''$, so $2 + 2y\,y'' = 0$ at the point."),
   (r"$\frac{2}{3}$", r"Gets $(2y - x)y'' = 2$ by a sign slip when transposing."),
   (r"$0$", r"Assumes $y'' = 0$ because $y' = 0$ at the point.")],
  r"Differentiating, $2x - y - xy' + 2yy' = 0$, so $y' = \frac{2x - y}{x - 2y}$, which is $0$ at $(1, 2)$. Differentiating again: $2 - 2y' - xy'' + 2(y')^2 + 2yy'' = 0$. At the point, $y' = 0$, so $2 + (2y - x)y'' = 0$, giving $y'' = -\frac{2}{3}$.",
  r"Confusing a zero first derivative with a zero second derivative.",
  "U07-D-implicit-second", "Two rounds of implicit differentiation with the product rule.",
  check=_c053, values=[Rational(-2, 3), Rational(-1, 2), Rational(2, 3), 0], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 054
def _c054():
    Y = prod([1 + kk*x for kk in range(1, 11)])
    return diff(expand(Y), x, 2).subs(x, 0)
q("U07-D-054", TOP_PQ, "Second derivative of a long product at zero", "Difficult", "Multi-step computation MCQ",
  r"If $f(x) = (1 + x)(1 + 2x)(1 + 3x)\cdots(1 + 10x)$, then $f''(0)$ equals",
  r"$2640$",
  [(r"$3025$", r"Uses $f''(0) = \left(\sum k\right)^2 = 55^2$, forgetting to subtract $\sum k^2 = 385$."),
   (r"$1320$", r"Computes $\sum_{i<j} ij = 1320$ but forgets the factor $2$ in $f''(0) = 2\sum_{i<j} ij$."),
   (r"$2255$", r"Subtracts $\sum k^2$ twice: $3025 - 770$.")],
  r"Let $g = \log_e f$, so $g'(x) = \sum \frac{k}{1+kx}$ and $g''(x) = -\sum \frac{k^2}{(1+kx)^2}$. At $0$: $f(0) = 1$, $f'(0) = g'(0) = 55$, and $f'' = f\left(g'' + (g')^2\right)$ gives $f''(0) = 55^2 - 385 = 2640$.",
  r"Treating $f''$ as $(f')^2/f$ and missing the $g''$ term.",
  "U07-D-product-many-second", "Logarithmic differentiation twice and two standard sums.",
  check=_c054, values=[2640, 3025, 1320, 2255], source_class=XII, cognitive="Analysis",
  numerical=dict(question=r"If $f(x) = (1 + x)(1 + 2x)(1 + 3x)\cdots(1 + 10x)$, then the value of $f''(0)$ is", answer=2640))

# ---------------------------------------------------------------- 055
_Y55 = asin(x)/sqrt(1 - x**2)
def _c055():
    return (1 - x**2)*diff(_Y55, x, 2)
_D55 = diff(_Y55, x)
q("U07-D-055", TOP_SEC, "Two-step relation for $\\frac{\\sin^{-1}x}{\\sqrt{1-x^2}}$", "Difficult", "Multi-step computation MCQ",
  r"If $y = \frac{\sin^{-1}x}{\sqrt{1 - x^2}}$ for $|x| < 1$, then $(1 - x^2)\frac{d^2y}{dx^2}$ equals",
  r"$3x\frac{dy}{dx} + y$",
  [(r"$2x\frac{dy}{dx} + y$", r"Differentiates $xy$ as $y$ only, losing $x\,y'$, in the step from $(1-x^2)y' - xy = 1$."),
   (r"$3x\frac{dy}{dx} - y$", r"Sign slip on the $y$ term when transposing."),
   (r"$x\frac{dy}{dx} + y$", r"Differentiates $(1-x^2)y'$ as $(1-x^2)y''$ only, missing $-2xy'$.")],
  r"$y\sqrt{1-x^2} = \sin^{-1}x$. Differentiating and multiplying by $\sqrt{1-x^2}$: $(1-x^2)y' - xy = 1$. Differentiating again: $(1-x^2)y'' - 2xy' - y - xy' = 0$, so $(1-x^2)y'' = 3xy' + y$.",
  r"Losing a term from a product when differentiating twice.",
  "U07-D-second-invtrig", "Clearing the root, two differentiations with product rules.",
  check=_c055, values=[3*x*_D55 + _Y55, 2*x*_D55 + _Y55, 3*x*_D55 - _Y55, x*_D55 + _Y55], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 056
def _c056():
    f = lambda t: t**3 - t + 1
    h = f(f(f(x)))
    return diff(h, x).subs(x, 0)
q("U07-D-056", TOP_CH, "Chain rule for a triple composition", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = x^3 - x + 1$ and $h(x) = f(f(f(x)))$. Then $h'(0)$ equals",
  r"$-4$",
  [(r"$-1$", r"Writes $h'(0) = \left(f'(0)\right)^3$, evaluating every factor at $0$."),
   (r"$8$", r"Writes $h'(0) = \left(f'(1)\right)^3$, evaluating every factor at the inner value $1$."),
   (r"$-2$", r"Uses only two chain factors, $f'(f(0))\,f'(0)$.")],
  r"$h'(x) = f'(f(f(x)))\cdot f'(f(x))\cdot f'(x)$. Here $f(0) = 1$, $f(1) = 1$, $f'(x) = 3x^2 - 1$, so $f'(0) = -1$ and $f'(1) = 2$. Hence $h'(0) = f'(1)\cdot f'(1)\cdot f'(0) = 2 \cdot 2 \cdot (-1) = -4$.",
  r"Evaluating the outer derivatives at the wrong points.",
  "U07-D-chain-iterate", "Three chain factors evaluated at different points.",
  check=_c056, values=[-4, -1, 8, -2], source_class=XII, cognitive="Analysis")

# ---------------------------------------------------------------- 057
def _c057():
    d1 = diff(acos(2*x**2 - 1), x)
    s1 = all(simplify(d1.subs(x, v) - 2/sqrt(1 - v**2)) == 0 for v in (Rational(-1, 2), Rational(-3, 5)))
    d2 = diff(atan(2*x/(1 - x**2)), x)
    s2 = all(simplify(d2.subs(x, v) - 2/(1 + v**2)) == 0 for v in (2, 3))
    return (bool(s1), bool(s2))
q("U07-D-057", TOP_INV, "Do branch changes alter the derivative?", "Difficult", "Statement-based MCQ",
  r"Statement I: For $-1 < x < 0$, $\frac{d}{dx}\left[\cos^{-1}\left(2x^2 - 1\right)\right] = \frac{2}{\sqrt{1 - x^2}}$. Statement II: For $x > 1$, $\frac{d}{dx}\left[\tan^{-1}\left(\frac{2x}{1 - x^2}\right)\right] = \frac{2}{1 + x^2}$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Uses $\cos^{-1}(2x^2 - 1) = 2\cos^{-1}x$ for negative $x$ too, and believes the branch change for $x > 1$ flips the sign of the derivative."),
   (ST_TF, r"Handles Statement I correctly but thinks $\tan^{-1}\frac{2x}{1-x^2} = \pi - 2\tan^{-1}x$ for $x > 1$, flipping the sign."),
   (ST_FT, r"Uses $\cos^{-1}(2x^2-1) = 2\cos^{-1}x$ for $-1 < x < 0$, getting $-\frac{2}{\sqrt{1-x^2}}$.")],
  r"For $x = \cos\theta$ with $\theta \in \left(\frac{\pi}{2}, \pi\right)$, $2x^2 - 1 = \cos 2\theta$ with $2\theta \in (\pi, 2\pi)$, so $\cos^{-1}(2x^2-1) = 2\pi - 2\theta = 2\pi - 2\cos^{-1}x$, whose derivative is $\frac{2}{\sqrt{1-x^2}}$; Statement I is true. For $x = \tan\theta$ with $\theta \in \left(\frac{\pi}{4}, \frac{\pi}{2}\right)$, $\tan^{-1}(\tan 2\theta) = 2\theta - \pi$, so the function is $2\tan^{-1}x - \pi$ with derivative $\frac{2}{1+x^2}$; Statement II is true.",
  r"Believing every branch change reverses the sign of the derivative.",
  "U07-D-invtrig-branch-stmt", "Two branch analyses where only one of them changes the sign.",
  check=_c057, values=[(T, T), (F_, F_), (T, F_), (F_, T)], source_class=XII, cognitive="Analysis")
