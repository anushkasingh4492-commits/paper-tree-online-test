import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x, y = symbols('x y', positive=True)
v = Symbol('v', real=True)
vp = Symbol('v', positive=True)
m, k = symbols('m k', real=True)
tt = Symbol('tt', positive=True)
t = Symbol('t', positive=True)

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TOP_ID = "Identifying homogeneous equations"
TOP_GS = "General solution by y = vx"
TOP_PS = "Particular solutions"
TOP_CURVE = "Solution curves through given points"
TOP_XVY = "Substitution x = vy"
TOP_APP = "Geometric applications"
SEL = [(T, F_, F_, F_), (F_, T, F_, F_), (F_, F_, T, F_), (F_, F_, F_, T)]


def is_homog(f):
    """True if f(tx, ty) = f(x, y) for t > 0 (homogeneous of degree zero)."""
    return simplify(f.subs({x: tt*x, y: tt*y}, simultaneous=True) - f) == 0


def hdeg(f):
    """Degree n with f(2x, 2y) = 2^n f(x, y); returns None if the ratio is not constant."""
    r = simplify(f.subs({x: 2*x, y: 2*y}, simultaneous=True) / f)
    if r.free_symbols:
        return None
    return simplify(log(r, 2))


def Fv(f, var=vp):
    """f(x, vx) for a homogeneous dy/dx = f(x, y); free of x."""
    r = simplify(expand_log(f.subs(y, var*x), force=True))
    assert x not in r.free_symbols, r
    return r


def Gx(g, var=vp):
    """g(vy, y) for a homogeneous dx/dy = g(x, y); free of y."""
    r = simplify(g.subs(x, var*y))
    assert y not in r.free_symbols, r
    return r


def vint(Fexpr, var=vp):
    """G(v) = integral dv/(F(v) - v), so that G(y/x) = ln x + const."""
    return integrate(1/simplify(Fexpr - var), var)


def slope(G):
    """Slope dy/dx of the family G(x, y) = C."""
    return simplify(-diff(G, x)/diff(G, y))


# ---------------------------------------------------------------- 001
def _c001():
    fs = [y/x + x**2/(x**2 + y**2), (x + y + 1)/(x - y), (x**2 + y)/(x*y), sin(y/x) + y**2/x]
    return tuple(bool(is_homog(f)) for f in fs)
q("U09-B-001", TOP_ID, "Recognising a homogeneous equation", "Easy", "Conceptual/application MCQ",
  r"Which of the following differential equations is homogeneous? (Take $x > 0$, $y > 0$.)",
  r"$\frac{dy}{dx} = \frac{y}{x} + \frac{x^{2}}{x^{2} + y^{2}}$",
  [(r"$\frac{dy}{dx} = \frac{x + y + 1}{x - y}$", r"Sees numerator and denominator as both linear in $x$ and $y$ and overlooks the constant term $1$, which has degree $0$."),
   (r"$\frac{dy}{dx} = \frac{x^{2} + y}{xy}$", r"Judges degree by the highest power present ($x^2$ and $xy$ both of degree $2$) and ignores the degree $1$ term $y$ in the numerator."),
   (r"$\frac{dy}{dx} = \sin\left(\frac{y}{x}\right) + \frac{y^{2}}{x}$", r"Assumes that any right side containing $\sin\left(\frac{y}{x}\right)$ is homogeneous, ignoring the term $\frac{y^2}{x}$ of degree $1$.")],
  r"An equation $\frac{dy}{dx} = f(x,y)$ is homogeneous when $f(tx, ty) = f(x,y)$ for $t > 0$. For $\frac{y}{x} + \frac{x^2}{x^2+y^2}$ we get $\frac{ty}{tx} + \frac{t^2x^2}{t^2(x^2+y^2)}$, which is unchanged, so this one is homogeneous. In the others the constant $1$, the mixed term $x^2 + y$ and the term $\frac{y^2}{x}$ each break the invariance.",
  "Checking only the highest-degree terms instead of testing $f(tx,ty) = f(x,y)$.",
  "U09-B-identify-homog", "One test applied to four short expressions.",
  check=_c001, source_class="XII", values=SEL, cognitive="Understanding")

# ---------------------------------------------------------------- 002
def _c002():
    f = (x**5 - 2*y**5)/(x**2 + y**2) + x*y**2*cos(y/x)
    return hdeg(f)
q("U09-B-002", TOP_ID, "Degree of a homogeneous function", "Easy", "Single-step computation MCQ",
  r"The function $f(x,y) = \frac{x^{5} - 2y^{5}}{x^{2} + y^{2}} + xy^{2}\cos\left(\frac{y}{x}\right)$ is homogeneous of degree",
  r"$3$",
  [(r"$5$", r"Reads the degree from the numerator $x^5 - 2y^5$ alone and ignores division by the degree $2$ denominator."),
   (r"$7$", r"Adds the degrees of numerator and denominator, $5 + 2 = 7$, as if the fraction were a product."),
   (r"$2$", r"Reads the degree from the denominator $x^2 + y^2$, or from $y^2$ in the second term, ignoring the factor $x$.")],
  r"Replacing $(x,y)$ by $(tx,ty)$, the fraction becomes $\frac{t^5}{t^2}\cdot\frac{x^5-2y^5}{x^2+y^2} = t^3(\ldots)$ and the second term becomes $t^3 xy^2\cos\left(\frac{y}{x}\right)$ since $\frac{y}{x}$ is unchanged. Hence $f(tx,ty) = t^3 f(x,y)$ and the degree is $3$.",
  "Taking the degree of a quotient as that of the numerator, or adding degrees.",
  "U09-B-degree-homog", "Single scaling substitution on two terms.",
  check=_c002, source_class="XII", values=[3, 5, 7, 2], cognitive="Application",
  numerical=dict(question=r"The function $f(x,y) = \frac{x^{5} - 2y^{5}}{x^{2} + y^{2}} + xy^{2}\cos\left(\frac{y}{x}\right)$ is homogeneous. Its degree of homogeneity is", answer=3))

# ---------------------------------------------------------------- 003
def _c003():
    p, qq = symbols('p q', positive=True, integer=True)
    den = Poly(x**2*y + 4*y**3, x, y)
    d = den.total_degree()
    assert all(sum(mon) == d for mon in den.monoms())
    sol = solve([Eq(p, d), Eq(1 + qq, d)], [p, qq])
    return sol[p] + sol[qq]
q("U09-B-003", TOP_ID, "Exponents making an equation homogeneous", "Easy", "Inverse/parameter MCQ",
  r"For positive integers $p$ and $q$, the differential equation $\frac{dy}{dx} = \frac{x^{p} + 2y^{3} + xy^{q}}{x^{2}y + 4y^{3}}$ is homogeneous. Then $p + q$ equals",
  r"$5$",
  [(r"$6$", r"Sets each exponent equal to $3$ ($p = 3$, $q = 3$), ignoring the factor $x$ in $xy^q$, which already contributes degree $1$."),
   (r"$7$", r"Believes the numerator must have degree one more than the denominator, taking $p = 4$ and $q + 1 = 4$, so $p + q = 7$."),
   (r"$3$", r"Reads the required degree as $2$ from $x^2$ in $x^2y$, taking $p = 2$ and $q + 1 = 2$, so $p + q = 3$.")],
  r"Every term of the denominator $x^2y + 4y^3$ has degree $3$, and the numerator already has $2y^3$ of degree $3$. So each numerator term must have degree $3$: $p = 3$ and $1 + q = 3$, giving $q = 2$. Hence $p + q = 5$.",
  "Matching exponents term by term without counting the degree of every factor.",
  "U09-B-homog-parameter", "One condition (equal degrees) applied to two terms.",
  check=_c003, source_class="XII", values=[5, 6, 7, 3], cognitive="Application",
  numerical=dict(question=r"For positive integers $p$ and $q$, the differential equation $\frac{dy}{dx} = \frac{x^{p} + 2y^{3} + xy^{q}}{x^{2}y + 4y^{3}}$ is homogeneous. The value of $p + q$ is", answer=5))

# ---------------------------------------------------------------- 004
def _c004():
    f = (x**2 + y**2)/(x*y)
    return simplify((Fv(f, v) - v)/x)
q("U09-B-004", TOP_GS, "Effect of the substitution y = vx", "Easy", "Single-step computation MCQ",
  r"Under the substitution $y = vx$, the differential equation $\frac{dy}{dx} = \frac{x^{2} + y^{2}}{xy}$ becomes",
  r"$x\frac{dv}{dx} = \frac{1}{v}$",
  [(r"$x\frac{dv}{dx} = \frac{1 + v^{2}}{v}$", r"Writes $\frac{dy}{dx} = x\frac{dv}{dx}$, dropping the term $v$ from the product rule, so nothing is subtracted from $\frac{1+v^2}{v}$."),
   (r"$\frac{dv}{dx} = \frac{1}{v}$", r"Differentiates $vx$ as $v + \frac{dv}{dx}$, losing the factor $x$ on the derivative term."),
   (r"$x\frac{dv}{dx} = \frac{1 + 2v^{2}}{v}$", r"Adds $v$ instead of subtracting it when moving it across: $\frac{1+v^2}{v} + v = \frac{1+2v^2}{v}$.")],
  r"With $y = vx$, $\frac{dy}{dx} = v + x\frac{dv}{dx}$ and the right side is $\frac{x^2(1+v^2)}{x^2 v} = \frac{1+v^2}{v}$. So $x\frac{dv}{dx} = \frac{1+v^2}{v} - v = \frac{1}{v}$.",
  "Forgetting the product rule term when differentiating $y = vx$.",
  "U09-B-vx-transform", "One substitution and one simplification.",
  check=_c004, source_class="XII", values=[1/(v*x), (1 + v**2)/(v*x), 1/v, (1 + 2*v**2)/(v*x)], cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    f = (y + sqrt(x**2 + y**2))/x
    return simplify((Fv(f, v) - v)/x)
q("U09-B-005", TOP_GS, "Separated form after y = vx", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, the substitution $y = vx$ reduces $x\frac{dy}{dx} = y + \sqrt{x^{2} + y^{2}}$ to the separated form",
  r"$\frac{dv}{\sqrt{1 + v^{2}}} = \frac{dx}{x}$",
  [(r"$\frac{dv}{v + \sqrt{1 + v^{2}}} = \frac{dx}{x}$", r"Uses $\frac{dy}{dx} = x\frac{dv}{dx}$, so the $v$ on the right is not cancelled."),
   (r"$\frac{dv}{\sqrt{1 + v^{2}}} = dx$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $x\left(v + \frac{dv}{dx}\right) = vx + x\sqrt{1+v^2}$ gives $\frac{dv}{dx} = \sqrt{1+v^2}$."),
   (r"$\frac{dv}{1 + v} = \frac{dx}{x}$", r"Simplifies $\sqrt{x^2 + v^2x^2}$ as $x + vx$, so $x\frac{dv}{dx} = 1 + v$.")],
  r"With $y = vx$ and $x > 0$, $\sqrt{x^2 + y^2} = x\sqrt{1+v^2}$. Then $x\left(v + x\frac{dv}{dx}\right) = vx + x\sqrt{1+v^2}$, so $x\frac{dv}{dx} = \sqrt{1+v^2}$, that is $\frac{dv}{\sqrt{1+v^2}} = \frac{dx}{x}$.",
  r"Treating $\sqrt{a^2 + b^2}$ as $a + b$, or mishandling $\frac{dy}{dx}$ under $y = vx$.",
  "U09-B-vx-transform", "One substitution with a surd to simplify.",
  check=_c005, source_class="XII", values=[sqrt(1 + v**2)/x, (v + sqrt(1 + v**2))/x, sqrt(1 + v**2), (1 + v)/x], cognitive="Application")

# ---------------------------------------------------------------- 006
def _c006():
    g = x/y + exp(x/y)
    return simplify((Gx(g, v) - v)/y)
q("U09-B-006", TOP_XVY, "Separated form after x = vy", "Easy", "Single-step computation MCQ",
  r"For $y > 0$, the substitution $x = vy$ reduces $y\frac{dx}{dy} = x + y\,e^{x/y}$ to the separated form",
  r"$e^{-v}\,dv = \frac{dy}{y}$",
  [(r"$e^{v}\,dv = \frac{dy}{y}$", r"Reaches $y\frac{dv}{dy} = e^{v}$ but puts $e^{v}$ in the numerator when separating instead of dividing by it."),
   (r"$\frac{dv}{v + e^{v}} = \frac{dy}{y}$", r"Takes $\frac{dx}{dy} = y\frac{dv}{dy}$, dropping the term $v$, so $v$ is not cancelled from the right side."),
   (r"$e^{-v}\,dv = dy$", r"Takes $\frac{dx}{dy} = v + \frac{dv}{dy}$, losing the factor $y$, so $\frac{dv}{dy} = e^{v}$.")],
  r"With $x = vy$, $\frac{dx}{dy} = v + y\frac{dv}{dy}$, and dividing the equation by $y$ gives $v + y\frac{dv}{dy} = v + e^{v}$. Hence $y\frac{dv}{dy} = e^{v}$, i.e. $e^{-v}\,dv = \frac{dy}{y}$.",
  "Mishandling the derivative of $x = vy$ or separating with the factor on the wrong side.",
  "U09-B-xvy-transform", "One substitution and one separation.",
  check=_c006, source_class="XII", values=[exp(v)/y, exp(-v)/y, (v + exp(v))/y, exp(v)], cognitive="Application")

# ---------------------------------------------------------------- 007
def _c007():
    return (x**2 + y**2)/(2*x*y)
q("U09-B-007", TOP_GS, "Rational homogeneous equation", "Easy", "Single-step computation MCQ",
  r"The general solution of $2xy\frac{dy}{dx} = x^{2} + y^{2}$ (where $C$ is an arbitrary constant) is",
  r"$x^{2} - y^{2} = Cx$",
  [(r"$x^{2} - y^{2} = Cx^{3}$", r"Integrates $\frac{2v}{1-v^2}$ as $+\log_e|1-v^2|$, losing the minus sign, so $1 - v^2 = Cx$ and $x^2 - y^2 = Cx^3$."),
   (r"$x^{2} + y^{2} = Cx^{3}$", r"Uses $\frac{dy}{dx} = x\frac{dv}{dx}$, so $x\frac{dv}{dx} = \frac{1+v^2}{2v}$, giving $1 + v^2 = Cx$ and $x^2 + y^2 = Cx^3$."),
   (r"$x(y^{2} - x^{2}) = Cy^{2}$", r"Reaches $1 - v^2 = \frac{C}{x}$ correctly but back-substitutes $v = \frac{x}{y}$, giving $1 - \frac{x^2}{y^2} = \frac{C}{x}$.")],
  r"Put $y = vx$: $v + x\frac{dv}{dx} = \frac{1+v^2}{2v}$, so $x\frac{dv}{dx} = \frac{1-v^2}{2v}$ and $\frac{2v\,dv}{1-v^2} = \frac{dx}{x}$. Integrating, $-\log_e|1-v^2| = \log_e|x| + c$, so $x(1 - v^2) = C$, i.e. $x^2 - y^2 = Cx$.",
  r"Sign slip in $\int \frac{2v}{1-v^2}\,dv = -\log_e|1-v^2|$.",
  "U09-B-gs-quadratic", "Standard substitution, one logarithmic integral.",
  check=_c007, source_class="XII", values=[slope((x**2 - y**2)/x), slope((x**2 - y**2)/x**3), slope((x**2 + y**2)/x**3), slope(x*(y**2 - x**2)/y**2)],
  cognitive="Application")

# ---------------------------------------------------------------- 008
def _c008():
    return (x - y)/(x + y)
q("U09-B-008", TOP_GS, "Rational homogeneous equation", "Easy", "Single-step computation MCQ",
  r"The general solution of $\frac{dy}{dx} = \frac{x - y}{x + y}$ (where $C$ is an arbitrary constant) is",
  r"$x^{2} - 2xy - y^{2} = C$",
  [(r"$x^{2} - 2xy - y^{2} = Cx^{4}$", r"Separates with a sign slip as $\frac{(1+v)\,dv}{1-2v-v^2} = -\frac{dx}{x}$, so $1 - 2v - v^2 = Cx^2$."),
   (r"$x^{2} - 2xy - y^{2} = Cx$", r"Integrates $\frac{1+v}{1-2v-v^2}$ as $-\log_e|1-2v-v^2|$, missing the factor $\frac{1}{2}$, so $x(1-2v-v^2) = C$."),
   (r"$\frac{y}{x} + \log_e\frac{(x-y)^{2}}{|x|} = C$", r"Uses $\frac{dy}{dx} = x\frac{dv}{dx}$, so $\frac{(1+v)\,dv}{1-v} = \frac{dx}{x}$, giving $-v - 2\log_e|1-v| = \log_e|x| + c$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{1-v}{1+v} - v = \frac{1-2v-v^2}{1+v}$. Since $\frac{d}{dv}(1-2v-v^2) = -2(1+v)$, integrating gives $-\frac{1}{2}\log_e|1-2v-v^2| = \log_e|x| + c$, so $x^2(1-2v-v^2) = C$, i.e. $x^2 - 2xy - y^2 = C$.",
  "Dropping the factor $\\frac{1}{2}$ when the numerator is a multiple of the derivative of the denominator.",
  "U09-B-gs-quadratic", "Substitution plus a recognisable logarithmic integral.",
  check=_c008, source_class="XII", values=[slope(x**2 - 2*x*y - y**2), slope((x**2 - 2*x*y - y**2)/x**4), slope((x**2 - 2*x*y - y**2)/x), slope(y/x + log((x - y)**2/x))],
  cognitive="Application")

# ---------------------------------------------------------------- 009
def _c009():
    return y/x + tan(y/x)
q("U09-B-009", TOP_GS, "Trigonometric homogeneous equation", "Easy", "Single-step computation MCQ",
  r"The general solution of $\frac{dy}{dx} = \frac{y}{x} + \tan\left(\frac{y}{x}\right)$ (where $C$ is an arbitrary constant) is",
  r"$\sin\left(\frac{y}{x}\right) = Cx$",
  [(r"$x\cos\left(\frac{y}{x}\right) = C$", r"Uses $\int \cot v\,dv = -\log_e|\cos v|$ (the integral of $\tan v$), giving $\cos v = \frac{C}{x}$."),
   (r"$\sin\left(\frac{y}{x}\right) = x + C$", r"Integrates correctly to $\log_e|\sin v| = \log_e|x| + c$ but exponentiates it as $\sin v = x + C$."),
   (r"$\sin\left(\frac{y}{x}\right) = Ce^{x}$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $\cot v\,dv = dx$ and $\log_e|\sin v| = x + c$.")],
  r"With $y = vx$: $v + x\frac{dv}{dx} = v + \tan v$, so $\cot v\,dv = \frac{dx}{x}$. Integrating, $\log_e|\sin v| = \log_e|x| + c$, hence $\sin\left(\frac{y}{x}\right) = Cx$.",
  r"Confusing $\int\cot v\,dv$ with $\int\tan v\,dv$.",
  "U09-B-gs-trig", "Substitution and one standard integral.",
  check=_c009, source_class="XII", values=[slope(sin(y/x)/x), slope(x*cos(y/x)), slope(sin(y/x) - x), slope(sin(y/x)*exp(-x))],
  cognitive="Application")

# ---------------------------------------------------------------- 010
def _c010():
    return y/x + exp(y/x)
q("U09-B-010", TOP_GS, "Exponential homogeneous equation", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, the general solution of $\frac{dy}{dx} = \frac{y}{x} + e^{y/x}$ (where $C$ is an arbitrary constant) is",
  r"$e^{-y/x} + \log_e x = C$",
  [(r"$e^{-y/x} - \log_e x = C$", r"Integrates $e^{-v}$ as $e^{-v}$ instead of $-e^{-v}$."),
   (r"$e^{y/x} - \log_e x = C$", r"Separates $x\frac{dv}{dx} = e^{v}$ as $e^{v}\,dv = \frac{dx}{x}$, putting $e^v$ in the numerator."),
   (r"$e^{-y/x} + x = C$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $e^{-v}\,dv = dx$ and $-e^{-v} = x + c$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = e^{v}$, so $e^{-v}\,dv = \frac{dx}{x}$. Integrating, $-e^{-v} = \log_e x + c$, i.e. $e^{-y/x} + \log_e x = C$.",
  r"Sign error in $\int e^{-v}\,dv$.",
  "U09-B-gs-exp", "Substitution and one exponential integral.",
  check=_c010, source_class="XII", values=[slope(exp(-y/x) + log(x)), slope(exp(-y/x) - log(x)), slope(exp(y/x) - log(x)), slope(exp(-y/x) + x)],
  cognitive="Application")

# ---------------------------------------------------------------- 011
def _c011():
    return (x**3 + y**3)/(x*y**2)
q("U09-B-011", TOP_GS, "Cubic homogeneous equation", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, the general solution of $(x^{3} + y^{3})\,dx = xy^{2}\,dy$ (where $C$ is an arbitrary constant) is",
  r"$y^{3} = 3x^{3}\log_e x + Cx^{3}$",
  [(r"$y^{3} = x^{3}\log_e x + Cx^{3}$", r"Integrates $v^2$ as $v^3$, dropping the factor $\frac{1}{3}$."),
   (r"$y^{3} = 3x^{4} + Cx^{3}$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $v^2\,dv = dx$ and $\frac{v^3}{3} = x + c$."),
   (r"$x^{3} = 3y^{3}\log_e x + Cy^{3}$", r"Solves $\frac{v^3}{3} = \log_e x + c$ correctly but back-substitutes $v = \frac{x}{y}$.")],
  r"Here $\frac{dy}{dx} = \frac{x^3+y^3}{xy^2}$. With $y = vx$: $v + x\frac{dv}{dx} = \frac{1}{v^2} + v$, so $v^2\,dv = \frac{dx}{x}$ and $\frac{v^3}{3} = \log_e x + c$. Multiplying by $3x^3$: $y^3 = 3x^3\log_e x + Cx^3$.",
  "Losing the factor from $\\int v^2\\,dv$ or back-substituting $v$ the wrong way round.",
  "U09-B-gs-cubic", "Substitution and a power integral.",
  check=_c011, source_class="XII", values=[slope(y**3/x**3 - 3*log(x)), slope(y**3/x**3 - log(x)), slope((y**3 - 3*x**4)/x**3), slope(x**3/y**3 - 3*log(x))],
  cognitive="Application")

# ---------------------------------------------------------------- 012
def _c012():
    f1 = x**2*sin(y/x) + x*y
    f2 = y/x + log(x**2/y)
    return (hdeg(f1) == 2, bool(is_homog(f2)))
q("U09-B-012", TOP_ID, "Homogeneity of functions and equations", "Easy", "Statement-based MCQ",
  r"Let $x > 0$ and $y > 0$. Statement I: $f(x,y) = x^{2}\sin\left(\frac{y}{x}\right) + xy$ is a homogeneous function of degree $2$. Statement II: The differential equation $\frac{dy}{dx} = \frac{y}{x} + \log_e\left(\frac{x^{2}}{y}\right)$ is homogeneous. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Treats $\log_e\left(\frac{x^2}{y}\right)$ as a function of $\frac{y}{x}$ because it is the logarithm of a quotient; in fact it changes by $\log_e t$ when $(x,y)$ becomes $(tx,ty)$."),
   (ST_FF, r"Thinks a term containing $\sin\left(\frac{y}{x}\right)$ cannot be part of a homogeneous function since $\sin$ is not a polynomial, and also rejects Statement II."),
   (ST_FT, r"Rejects Statement I because of the $\sin$ term and accepts Statement II for the quotient inside the logarithm.")],
  r"Statement I: $f(tx,ty) = t^2x^2\sin\left(\frac{y}{x}\right) + t^2xy = t^2 f(x,y)$, so it is homogeneous of degree $2$; true. Statement II: $\log_e\left(\frac{t^2x^2}{ty}\right) = \log_e t + \log_e\left(\frac{x^2}{y}\right)$, so the right side is not unchanged under scaling and the equation is not homogeneous; false.",
  r"Assuming any logarithm of a quotient is a function of $\frac{y}{x}$.",
  "U09-B-identify-homog", "Two direct scaling checks.",
  check=_c012, source_class="XII", values=[(T, F_), (T, T), (F_, F_), (F_, T)], cognitive="Understanding")

# ---------------------------------------------------------------- 013
def _c013():
    f = y/x + sec(y/x)
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    x1 = sqrt(E)
    sols = [s for s in solve(Eq(G, log(x1) + K), v) if -pi/2 < s < pi/2]
    assert len(sols) == 1
    return x1*sols[0]
q("U09-B-013", TOP_PS, "Value of a particular solution", "Easy", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, be the solution of $\frac{dy}{dx} = \frac{y}{x} + \sec\left(\frac{y}{x}\right)$ with $y(1) = 0$ and $-\frac{\pi}{2} < \frac{y}{x} < \frac{\pi}{2}$. Then $y(\sqrt{e})$ equals",
  r"$\frac{\pi\sqrt{e}}{6}$",
  [(r"$-\frac{\pi\sqrt{e}}{6}$", r"Integrates $\cos v$ as $-\sin v$, so $\sin v = -\log_e x$ and $v = -\frac{\pi}{6}$ at $x = \sqrt{e}$."),
   (r"$\frac{\pi}{6}$", r"Finds $v = \frac{y}{x} = \frac{\pi}{6}$ and reports it as $y$, forgetting to multiply by $x = \sqrt{e}$."),
   (r"$\frac{\pi\sqrt{e}}{2}$", r"Takes $\log_e\sqrt{e} = 1$, so $\sin v = 1$ and $v = \frac{\pi}{2}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \sec v$, so $\cos v\,dv = \frac{dx}{x}$ and $\sin v = \log_e x + c$. The condition $y(1) = 0$ gives $c = 0$. At $x = \sqrt{e}$, $\sin v = \frac{1}{2}$, so $v = \frac{\pi}{6}$ and $y = \frac{\pi\sqrt{e}}{6}$.",
  r"Reporting $v = \frac{y}{x}$ as the value of $y$.",
  "U09-B-ps-trig-value", "Short substitution, one integral, one evaluation.",
  check=_c013, source_class="XII", values=[pi*sqrt(E)/6, -pi*sqrt(E)/6, pi/6, pi*sqrt(E)/2], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    s = solveset(Eq(m*x**2, (m*x)**2 + 2*x*(m*x)), m, S.Reals) - FiniteSet(0)
    return list(s)[0]
q("U09-B-014", TOP_ID, "Straight-line solutions through the origin", "Easy", "Inverse/parameter MCQ",
  r"The line $y = mx$, $m \ne 0$, is a solution curve of the differential equation $x^{2}\frac{dy}{dx} = y^{2} + 2xy$ (for $x \ne 0$). Then $m$ equals",
  r"$-1$",
  [(r"$-2$", r"Substitutes $y = mx$ into the right side only, solving $m^2 + 2m = 0$ and forgetting that $\frac{dy}{dx} = m$ appears on the left."),
   (r"$-3$", r"Moves $m$ across with the wrong sign, solving $m^2 + 3m = 0$."),
   (r"$1$", r"Collects terms as $m^2 - m = 0$ through a sign slip.")],
  r"For $y = mx$, $\frac{dy}{dx} = m$, so $x^2 m = m^2x^2 + 2mx^2$. Dividing by $x^2$: $m = m^2 + 2m$, i.e. $m(m+1) = 0$. With $m \ne 0$, $m = -1$.",
  "Not using the left side $x^2\\frac{dy}{dx}$ after substituting $y = mx$.",
  "U09-B-line-solution", "One substitution and a quadratic.",
  check=_c014, source_class="XII", values=[-1, -2, -3, 1], cognitive="Application")

# ---------------------------------------------------------------- 015
def _c015():
    return y/x + sin(y/x)
q("U09-B-015", TOP_GS, "Trigonometric homogeneous equation", "Medium", "Multi-step computation MCQ",
  r"The general solution of $x\frac{dy}{dx} = y + x\sin\left(\frac{y}{x}\right)$ (where $C$ is an arbitrary constant) is",
  r"$\tan\left(\frac{y}{2x}\right) = Cx$",
  [(r"$x\tan\left(\frac{y}{2x}\right) = C$", r"Uses $\int\csc v\,dv = \log_e|\csc v + \cot v|$, which equals $-\log_e\left|\tan\frac{v}{2}\right|$, so the sign of the logarithm is reversed."),
   (r"$\tan\left(\frac{y}{x}\right) = Cx$", r"Takes $\int\csc v\,dv = \log_e|\tan v|$, dropping the half angle."),
   (r"$\tan\left(\frac{y}{2x}\right) = Ce^{x}$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $\csc v\,dv = dx$ and $\log_e\left|\tan\frac{v}{2}\right| = x + c$.")],
  r"Dividing by $x$ and putting $y = vx$: $x\frac{dv}{dx} = \sin v$, so $\csc v\,dv = \frac{dx}{x}$. Since $\int\csc v\,dv = \log_e\left|\tan\frac{v}{2}\right|$, we get $\log_e\left|\tan\frac{v}{2}\right| = \log_e|x| + c$, i.e. $\tan\left(\frac{y}{2x}\right) = Cx$.",
  r"Misremembering $\int\csc v\,dv = \log_e\left|\tan\frac{v}{2}\right|$.",
  "U09-B-gs-trig", "Substitution plus a less familiar standard integral.",
  check=_c015, source_class="XII", values=[slope(tan(y/(2*x))/x), slope(x*tan(y/(2*x))), slope(tan(y/x)/x), slope(tan(y/(2*x))*exp(-x))],
  cognitive="Application")

# ---------------------------------------------------------------- 016
def _c016():
    f = y/x + exp(-y/x)
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    x1 = E
    s = solve(Eq(G, log(x1) + K), v)
    assert len(s) == 1
    return x1*s[0]
q("U09-B-016", TOP_PS, "Value of a particular solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, satisfy $x\frac{dy}{dx} = y + x\,e^{-y/x}$ and $y(1) = 0$. Then $y(e)$ equals",
  r"$e\log_e 2$",
  [(r"$\log_e 2$", r"Finds $\frac{y}{x} = \log_e 2$ at $x = e$ and reports it as $y(e)$ without multiplying by $e$."),
   (r"$\frac{\log_e 2}{e}$", r"Finds $v = \log_e 2$ and then divides by $x$ instead of multiplying, taking $y = \frac{v}{x}$."),
   (r"$e$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, giving $e^{v}\,dv = dx$, $e^{v} = x$ after using $y(1) = 0$, so $v = 1$ and $y(e) = e$.")],
  r"Dividing by $x$ and putting $y = vx$: $x\frac{dv}{dx} = e^{-v}$, so $e^{v}\,dv = \frac{dx}{x}$ and $e^{v} = \log_e x + c$. From $y(1) = 0$, $c = 1$. At $x = e$, $e^{v} = 2$, so $v = \log_e 2$ and $y(e) = e\log_e 2$.",
  r"Stopping at $v = \frac{y}{x}$ instead of returning to $y$.",
  "U09-B-ps-exp-value", "Substitution, constant from initial condition, back-substitution.",
  check=_c016, source_class="XII", values=[E*log(2), log(2), log(2)/E, E], cognitive="Application")

# ---------------------------------------------------------------- 017
def _c017():
    f = x/y + y/x
    G = vint(Fv(f))
    K = G.subs(vp, 2) - log(1)
    s = [r for r in solve(Eq(G, log(E) + K), vp) if r > 0]
    return E*s[0]
q("U09-B-017", TOP_PS, "Value of a particular solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, $y > 0$, be the solution of $\frac{dy}{dx} = \frac{x}{y} + \frac{y}{x}$ with $y(1) = 2$. Then $y(e)$ equals",
  r"$\sqrt{6}\,e$",
  [(r"$\sqrt{5}\,e$", r"Integrates $v\,dv$ as $v^2$ instead of $\frac{v^2}{2}$: $v^2 = \log_e x + 4$, so $v^2 = 5$ at $x = e$."),
   (r"$2e$", r"Fixes the constant as $v(1) = 2$ instead of $v(1)^2 = 4$, getting $v^2 = 2\log_e x + 2$, so $v = 2$ at $x = e$."),
   (r"$\sqrt{6}$", r"Finds $v = \sqrt{6}$ correctly but forgets that $y = vx$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{1}{v}$, so $v\,dv = \frac{dx}{x}$ and $v^2 = 2\log_e x + c$. From $v(1) = 2$, $c = 4$. At $x = e$, $v^2 = 6$, so $v = \sqrt{6}$ and $y(e) = \sqrt{6}\,e$.",
  "Mishandling the constant when the solution involves $v^2$.",
  "U09-B-ps-power-value", "Three steps: substitution, constant, back-substitution.",
  check=_c017, source_class="XII", values=[sqrt(6)*E, sqrt(5)*E, 2*E, sqrt(6)], cognitive="Application",
  numerical=dict(question=r"Let $y = y(x)$, $x > 0$, $y > 0$, be the solution of $\frac{dy}{dx} = \frac{x}{y} + \frac{y}{x}$ with $y(1) = 2$. Then the value of $\frac{(y(e))^{2}}{e^{2}}$ is", answer=6))

# ---------------------------------------------------------------- 018
def _c018():
    f = (y/x)*(log(y) - log(x) + 1)
    G = vint(Fv(f))
    K = G.subs(vp, E**2) - log(1)
    x1 = Rational(1, 2)
    s = solve(Eq(G, log(x1) + K), vp)
    return x1*s[0]
q("U09-B-018", TOP_PS, "Logarithmic homogeneous equation", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, $y > 0$, satisfy $x\frac{dy}{dx} = y\left(\log_e y - \log_e x + 1\right)$ and $y(1) = e^{2}$. Then $y\left(\frac{1}{2}\right)$ equals",
  r"$\frac{e}{2}$",
  [(r"$e$", r"Reaches $\frac{y}{x} = e$ at $x = \frac{1}{2}$ and reports it as $y$."),
   (r"$\frac{e^{3/2}}{2}$", r"Gets $\log_e(\log_e v) = \log_e x + c$ but exponentiates it as $\log_e v = x + C$, so $\log_e v = x + 1$."),
   (r"$\frac{e^{4}}{2}$", r"Reads $\log_e y - \log_e x$ as $\log_e\frac{x}{y}$, so $x\frac{dv}{dx} = -v\log_e v$ and $\log_e v = \frac{2}{x}$.")],
  r"With $y = vx$ the equation becomes $v + x\frac{dv}{dx} = v(\log_e v + 1)$, so $\frac{dv}{v\log_e v} = \frac{dx}{x}$ and $\log_e(\log_e v) = \log_e x + c$, i.e. $\log_e v = Cx$. At $x = 1$, $v = e^2$, so $C = 2$ and $y = xe^{2x}$. Hence $y\left(\frac{1}{2}\right) = \frac{1}{2}e$.",
  r"Exponentiating $\log_e(\log_e v) = \log_e x + c$ incorrectly.",
  "U09-B-ps-log", "Substitution, a log-of-log integral, constant and evaluation.",
  check=_c018, source_class="XII", values=[E/2, E, exp(Rational(3, 2))/2, exp(4)/2], cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    f = (y + sqrt(x**2 + y**2))/x
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    s = solve(Eq(G, log(3) + K), v)
    return 3*s[0]
q("U09-B-019", TOP_PS, "Equation with a surd", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, be the solution of $x\,dy - y\,dx = \sqrt{x^{2} + y^{2}}\,dx$ with $y(1) = 0$. Then $y(3)$ equals",
  r"$4$",
  [(r"$\frac{4}{3}$", r"Finds $v = \frac{y}{x} = \frac{4}{3}$ at $x = 3$ and forgets to multiply by $x$."),
   (r"$6$", r"Simplifies $\sqrt{x^2 + y^2}$ as $x + y$, so $x\frac{dv}{dx} = 1 + v$, $v = x - 1$ and $y = x(x-1)$."),
   (r"$-4$", r"Writes $\int\frac{dv}{\sqrt{1+v^2}} = \log_e\left(\sqrt{1+v^2} - v\right)$, giving $y = \frac{1 - x^2}{2}$.")],
  r"Dividing by $x\,dx$: $\frac{dy}{dx} = \frac{y + \sqrt{x^2+y^2}}{x}$. With $y = vx$, $\frac{dv}{\sqrt{1+v^2}} = \frac{dx}{x}$, so $\log_e\left(v + \sqrt{1+v^2}\right) = \log_e x + c$ and $c = 0$ from $y(1) = 0$. Thus $y + \sqrt{x^2+y^2} = x^2$, which gives $y = \frac{x^2 - 1}{2}$ and $y(3) = 4$.",
  r"Treating $\sqrt{x^2 + y^2}$ as $x + y$.",
  "U09-B-ps-sqrt", "Substitution, inverse-hyperbolic type integral, algebra to make $y$ explicit.",
  check=_c019, source_class="XII", values=[4, Rational(4, 3), 6, -4], cognitive="Application",
  numerical=dict(question=r"Let $y = y(x)$, $x > 0$, be the solution of $x\,dy - y\,dx = \sqrt{x^{2} + y^{2}}\,dx$ with $y(1) = 0$. Then the value of $y(3)$ is", answer=4))

# ---------------------------------------------------------------- 020
def _c020():
    f = y/x - cos(y/x)**2
    G = vint(Fv(f, v), v)
    K = G.subs(v, pi/4) - log(1)
    X = Symbol('X', positive=True)
    s = solve(Eq(G.subs(v, 0), log(X) + K), X)
    return s[0]
q("U09-B-020", TOP_CURVE, "Where a solution curve meets an axis", "Medium", "Multi-step computation MCQ",
  r"A curve in the region $x > 0$ passes through $\left(1, \frac{\pi}{4}\right)$, and its slope at every point $(x,y)$ is $\frac{y}{x} - \cos^{2}\left(\frac{y}{x}\right)$. The curve meets the $x$-axis at $x =$",
  r"$e$",
  [(r"$\frac{1}{e}$", r"Separates as $\sec^2 v\,dv = \frac{dx}{x}$, losing the minus sign, so $\tan v = \log_e x + 1$."),
   (r"$e^{\pi/4}$", r"Fixes the constant using $v = \frac{\pi}{4}$ itself instead of $\tan\frac{\pi}{4} = 1$, so $\tan v = \frac{\pi}{4} - \log_e x$."),
   (r"$e^{-\pi/4}$", r"Makes both slips: drops the minus sign and uses $\frac{\pi}{4}$ for $\tan\frac{\pi}{4}$, so $\tan v = \log_e x + \frac{\pi}{4}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = -\cos^2 v$, so $\sec^2 v\,dv = -\frac{dx}{x}$ and $\tan v = -\log_e x + c$. At $(1, \frac{\pi}{4})$, $\tan\frac{\pi}{4} = 1$ gives $c = 1$, so $\tan\left(\frac{y}{x}\right) = 1 - \log_e x$. On the $x$-axis $y = 0$, so $\log_e x = 1$ and $x = e$.",
  "Losing the sign of the $\\cos^2$ term, or using the angle instead of its tangent for the constant.",
  "U09-B-ps-trig-curve", "Substitution, constant from a point, then a condition on the curve.",
  check=_c020, source_class="XII", values=[E, 1/E, exp(pi/4), exp(-pi/4)], cognitive="Application")

# ---------------------------------------------------------------- 021
def _c021():
    return -(1 + exp(x/y))/(exp(x/y)*(1 - x/y))
q("U09-B-021", TOP_XVY, "General solution with x = vy", "Medium", "Multi-step computation MCQ",
  r"The general solution of $\left(1 + e^{x/y}\right)dx + e^{x/y}\left(1 - \frac{x}{y}\right)dy = 0$, $y > 0$ (where $C$ is an arbitrary constant) is",
  r"$x + y\,e^{x/y} = C$",
  [(r"$x + y\,e^{x/y} = Cy^{2}$", r"Reaches $\frac{dy}{y} + \frac{(1+e^v)\,dv}{v + e^v} = 0$ but moves $\log_e y$ across without changing sign, getting $v + e^{v} = Cy$."),
   (r"$x + e^{x/y} = C$", r"Obtains $y(v + e^{v}) = C$ correctly but back-substitutes it as $yv + e^{v}$, dropping the factor $y$ on $e^{v}$."),
   (r"$\frac{y^{2}}{x} + y\,e^{y/x} = C$", r"Solves $y(v + e^v) = C$ correctly but back-substitutes $v = \frac{y}{x}$ instead of $v = \frac{x}{y}$.")],
  r"Put $x = vy$, so $dx = v\,dy + y\,dv$. The equation becomes $(1 + e^v)(v\,dy + y\,dv) + e^v(1 - v)\,dy = 0$, i.e. $(v + e^v)\,dy + y(1 + e^v)\,dv = 0$. Separating, $\frac{dy}{y} + \frac{(1+e^v)\,dv}{v + e^v} = 0$, so $\log_e y + \log_e(v + e^v) = c$ and $y(v + e^v) = C$, which is $x + y\,e^{x/y} = C$.",
  r"Using $y = vx$ out of habit when the equation is built from $\frac{x}{y}$.",
  "U09-B-xvy-gs", "Choosing $x = vy$, expanding, recognising an exact logarithmic integral.",
  check=_c021, source_class="XII", values=[slope(x + y*exp(x/y)), slope((x + y*exp(x/y))/y**2), slope(x + exp(x/y)), slope(y**2/x + y*exp(y/x))],
  cognitive="Analysis")

# ---------------------------------------------------------------- 022
def _c022():
    g = -(y - 2*x*exp(x/y))/(2*y*exp(x/y))
    H = vint(Gx(g, v), v)
    K = H.subs(v, 0) - log(1)
    s = solve(Eq(H, log(E) + K), v)
    return E*s[0]
q("U09-B-022", TOP_XVY, "Particular solution with x = vy", "Medium", "Multi-step computation MCQ",
  r"Let $x = x(y)$ satisfy $2y\,e^{x/y}\,dx + \left(y - 2x\,e^{x/y}\right)dy = 0$, $y > 0$, with $x = 0$ when $y = 1$. Then the value of $x$ when $y = e$ is",
  r"$-e\log_e 2$",
  [(r"$e\log_e\frac{3}{2}$", r"Makes a sign slip when separating, getting $2e^{v} = \log_e y + 2$, so $e^{v} = \frac{3}{2}$ at $y = e$."),
   (r"$-\log_e 2$", r"Finds $v = \frac{x}{y} = -\log_e 2$ and reports it as $x$ without multiplying by $y = e$."),
   (r"$e\log_e 2$", r"Solves $e^{x/e} = \frac{1}{2}$ but writes $\log_e\frac{1}{2}$ as $\log_e 2$.")],
  r"Put $x = vy$, $dx = v\,dy + y\,dv$: $2ye^{v}(v\,dy + y\,dv) + (y - 2vye^{v})\,dy = 0$ simplifies to $2y^2e^{v}\,dv + y\,dy = 0$, so $2e^{v}\,dv = -\frac{dy}{y}$ and $2e^{x/y} = -\log_e y + c$. From $x = 0$ at $y = 1$, $c = 2$. At $y = e$: $2e^{x/e} = 1$, so $x = e\log_e\frac{1}{2} = -e\log_e 2$.",
  r"Sign slips when separating and when simplifying $\log_e\frac{1}{2}$.",
  "U09-B-xvy-ps", "Substitution $x = vy$, simplification, constant, solving an exponential equation.",
  check=_c022, source_class="XII", values=[-E*log(2), E*log(Rational(3, 2)), -log(2), E*log(2)], cognitive="Application")

# ---------------------------------------------------------------- 023
def _c023():
    f = y/x + y**2/x**2
    G = vint(Fv(f))
    K = G.subs(vp, 1) - log(1)
    x1 = sqrt(E)
    s = solve(Eq(G, log(x1) + K), vp)
    return x1*s[0]
q("U09-B-023", TOP_PS, "Value of a particular solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$ be the solution of $x^{2}\frac{dy}{dx} = xy + y^{2}$ with $y(1) = 1$, on an interval containing $1$ on which $y > 0$. Then $y(\sqrt{e})$ equals",
  r"$2\sqrt{e}$",
  [(r"$\frac{2\sqrt{e}}{3}$", r"Integrates $\frac{dv}{v^2}$ as $+\frac{1}{v}$, so $\frac{1}{v} = \log_e x + 1$ and $v = \frac{2}{3}$ at $x = \sqrt{e}$."),
   (r"$2$", r"Finds $v = 2$ at $x = \sqrt{e}$ and reports it as $y$."),
   (r"$\frac{\sqrt{e}}{2 - \sqrt{e}}$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $\frac{dv}{v^2} = dx$, $\frac{1}{v} = 2 - x$ and $v = \frac{1}{2 - \sqrt{e}}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = v^2$, so $\frac{dv}{v^2} = \frac{dx}{x}$ and $-\frac{1}{v} = \log_e x + c$. From $v(1) = 1$, $c = -1$, so $\frac{x}{y} = 1 - \log_e x$ and $y = \frac{x}{1 - \log_e x}$. Hence $y(\sqrt{e}) = \frac{\sqrt{e}}{1/2} = 2\sqrt{e}$.",
  r"Sign error in $\int v^{-2}\,dv$.",
  "U09-B-ps-reciprocal", "Substitution, power integral with sign care, evaluation.",
  check=_c023, source_class="XII", values=[2*sqrt(E), 2*sqrt(E)/3, 2, sqrt(E)/(2 - sqrt(E))], cognitive="Application")

# ---------------------------------------------------------------- 024
def _c024():
    f = (x**2 + x*y + y**2)/x**2
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    x1 = exp(pi/4)
    s = solve(Eq(G, log(x1) + K), v)
    return x1*s[0]
q("U09-B-024", TOP_PS, "Inverse tangent type solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, be the solution of $x^{2}\frac{dy}{dx} = x^{2} + xy + y^{2}$ with $y(1) = 0$, for $1 \le x < e^{\pi/2}$. Then $y\left(e^{\pi/4}\right)$ equals",
  r"$e^{\pi/4}$",
  [(r"$1$", r"Finds $\frac{y}{x} = \tan\frac{\pi}{4} = 1$ and reports it as $y$."),
   (r"$-e^{\pi/4}$", r"Separates as $\frac{dv}{1+v^2} = -\frac{dx}{x}$, so $\tan^{-1}v = -\log_e x$ and $v = -1$."),
   (r"$\frac{e^{\pi/4}}{\sqrt{2}}$", r"Integrates $\frac{dv}{1+v^2}$ as $\sin^{-1}v$, so $v = \sin\frac{\pi}{4} = \frac{1}{\sqrt{2}}$.")],
  r"With $y = vx$: $v + x\frac{dv}{dx} = 1 + v + v^2$, so $\frac{dv}{1+v^2} = \frac{dx}{x}$ and $\tan^{-1}v = \log_e x + c$, with $c = 0$ from $y(1) = 0$. So $y = x\tan(\log_e x)$ and $y\left(e^{\pi/4}\right) = e^{\pi/4}\tan\frac{\pi}{4} = e^{\pi/4}$.",
  r"Confusing $\int\frac{dv}{1+v^2}$ with $\int\frac{dv}{\sqrt{1-v^2}}$.",
  "U09-B-ps-arctan", "Substitution, standard inverse tangent integral, evaluation.",
  check=_c024, source_class="XII", values=[exp(pi/4), 1, -exp(pi/4), exp(pi/4)/sqrt(2)], cognitive="Application")

# ---------------------------------------------------------------- 025
def _c025():
    f = (x**2 + 3*y**2)/(2*x*y)
    G = vint(Fv(f))
    K = G.subs(vp, 1) - log(1)
    s = [r for r in solve(Eq(G, log(2) + K), vp) if r > 0]
    return 2*s[0]
q("U09-B-025", TOP_CURVE, "Point on a particular solution curve", "Medium", "Multi-step computation MCQ",
  r"The solution curve of $2xy\frac{dy}{dx} = x^{2} + 3y^{2}$, $x > 0$, passing through $(1,1)$ also passes through $(2, \beta)$ with $\beta > 0$. Then $\beta$ equals",
  r"$2\sqrt{3}$",
  [(r"$2\sqrt{7}$", r"Integrates $\frac{2v}{1+v^2}$ as $\frac{1}{2}\log_e(1+v^2)$, so $1 + v^2 = 2x^2$ and $\frac{\beta^2}{4} = 7$."),
   (r"$\sqrt{3}$", r"Gets $1 + v^2 = 2x$ correctly but puts $v = \beta$ at $x = 2$ instead of $v = \frac{\beta}{2}$."),
   (r"$2\sqrt{2e - 1}$", r"Uses $\frac{dy}{dx} = v + \frac{dv}{dx}$, so $\log_e(1+v^2) = x + c$ and $1 + v^2 = 2e^{x-1}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{1+3v^2}{2v} - v = \frac{1+v^2}{2v}$, so $\frac{2v\,dv}{1+v^2} = \frac{dx}{x}$ and $1 + v^2 = Cx$, i.e. $x^2 + y^2 = Cx^3$. Through $(1,1)$, $C = 2$. At $x = 2$: $4 + \beta^2 = 16$, so $\beta = 2\sqrt{3}$.",
  r"Substituting $v = y$ instead of $v = \frac{y}{x}$ at the new point.",
  "U09-B-curve-through", "Substitution, constant from a point, evaluation at a second point.",
  check=_c025, source_class="XII", values=[2*sqrt(3), 2*sqrt(7), sqrt(3), 2*sqrt(2*E - 1)], cognitive="Application",
  numerical=dict(question=r"The solution curve of $2xy\frac{dy}{dx} = x^{2} + 3y^{2}$, $x > 0$, passing through $(1,1)$ also passes through $(2, \beta)$ with $\beta > 0$. Then the value of $\beta^{2}$ is", answer=12))

# ---------------------------------------------------------------- 026
def _c026():
    f = (2*x**2 + y**2)/(2*x*y)
    G = vint(Fv(f))
    K = G.subs(vp, 2) - log(3)
    s = [r for r in solve(Eq(G, log(1) + K), vp) if r > 0]
    return s[0]
q("U09-B-026", TOP_CURVE, "Curve through two given points", "Medium", "Inverse/parameter MCQ",
  r"The solution curve of $2xy\,dy = (2x^{2} + y^{2})\,dx$, $x > 0$, $y > 0$, that passes through $(3, 6)$ also passes through $(1, k)$. Then $k$ equals",
  r"$2\sqrt{2}$",
  [(r"$\frac{2\sqrt{6}}{3}$", r"Loses the minus sign in $\int\frac{2v}{2-v^2}\,dv$, getting $2 - v^2 = Cx$, i.e. $2x^2 - y^2 = Cx^3$: $C = -\frac{2}{3}$ and $2 - k^2 = -\frac{2}{3}$."),
   (r"$2\sqrt{5}$", r"Writes the family as $2x^2 - y^2 = C$, dropping the factor $x$: $C = -18$ and $2 - k^2 = -18$."),
   (r"$\sqrt{10}$", r"Drops the coefficient $2$ of $x^2$ and solves $2xy\frac{dy}{dx} = x^2 + y^2$, whose family is $x^2 - y^2 = Cx$: $C = -9$ and $1 - k^2 = -9$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{2+v^2}{2v} - v = \frac{2-v^2}{2v}$, so $\frac{2v\,dv}{2-v^2} = \frac{dx}{x}$ and $-\log_e|2 - v^2| = \log_e x + c$, i.e. $x(2 - v^2) = C$, or $2x^2 - y^2 = Cx$. Through $(3,6)$: $18 - 36 = 3C$, so $C = -6$. At $x = 1$: $2 - k^2 = -6$, so $k = 2\sqrt{2}$.",
  r"Losing the sign in $\int\frac{2v}{2-v^2}\,dv = -\log_e|2-v^2|$ or dropping the factor $x$ in the family.",
  "U09-B-curve-through", "General solution, constant from one point, unknown at another.",
  check=_c026, source_class="XII", values=[2*sqrt(2), 2*sqrt(6)/3, 2*sqrt(5), sqrt(10)], cognitive="Application",
  numerical=dict(question=r"The solution curve of $2xy\,dy = (2x^{2} + y^{2})\,dx$, $x > 0$, $y > 0$, that passes through $(3, 6)$ also passes through $(1, k)$. Then the value of $k^{2}$ is", answer=8))

# ---------------------------------------------------------------- 027
def _c027():
    f = (y + 2*sqrt(x*y))/x
    G = vint(Fv(f))
    K = G.subs(vp, 1) - log(1)
    s = solve(Eq(G, log(E) + K), vp)
    return E*s[0]
q("U09-B-027", TOP_PS, "Equation with a surd", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x \ge 1$, $y > 0$, satisfy $x\frac{dy}{dx} = y + 2\sqrt{xy}$ and $y(1) = 1$. Then $y(e)$ equals",
  r"$4e$",
  [(r"$\frac{9e}{4}$", r"Integrates $\frac{dv}{2\sqrt{v}}$ as $2\sqrt{v}$, so $2\sqrt{v} = \log_e x + 2$ and $v = \frac{9}{4}$ at $x = e$."),
   (r"$4$", r"Finds $v = 4$ at $x = e$ and reports it as $y$."),
   (r"$e^{3}$", r"Simplifies $\sqrt{x \cdot vx}$ as $xv$, so $x\frac{dv}{dx} = 2v$, $v = x^2$ and $y = x^3$.")],
  r"With $y = vx$, $\sqrt{xy} = x\sqrt{v}$, so $v + x\frac{dv}{dx} = v + 2\sqrt{v}$ and $\frac{dv}{2\sqrt{v}} = \frac{dx}{x}$. Then $\sqrt{v} = \log_e x + c$ with $c = 1$, so $y = x(1 + \log_e x)^2$ and $y(e) = 4e$.",
  r"Simplifying $\sqrt{x^2 v}$ as $xv$.",
  "U09-B-ps-sqrt", "Substitution with a surd, constant, evaluation.",
  check=_c027, source_class="XII", values=[4*E, 9*E/4, 4, E**3], cognitive="Application",
  numerical=dict(question=r"Let $y = y(x)$, $x \ge 1$, $y > 0$, satisfy $x\frac{dy}{dx} = y + 2\sqrt{xy}$ and $y(1) = 1$. Then the value of $\frac{y(e)}{e}$ is", answer=4))

# ---------------------------------------------------------------- 028
def _c028():
    return (x + 2*y)/(2*x + y)
q("U09-B-028", TOP_GS, "Partial fractions after substitution", "Difficult", "Multi-step computation MCQ",
  r"The general solution of $\frac{dy}{dx} = \frac{x + 2y}{2x + y}$ (where $C$ is an arbitrary constant) is",
  r"$x + y = C(x - y)^{3}$",
  [(r"$x(x + y) = C(x - y)^{3}$", r"Uses partial fractions $\frac{3}{1-v} + \frac{1}{1+v}$, missing the factor $\frac{1}{2}$, so $\frac{1+v}{(1-v)^3} = Cx$."),
   (r"$x^{2}(x + y) = C(x - y)^{3}$", r"Reaches $\frac{1+v}{(1-v)^3} = Cx^2$ but drops the $x^2$ when exponentiating, writing $\frac{1+v}{(1-v)^3} = C$."),
   (r"$(x + y)(x - y)^{3} = Cx^{6}$", r"Integrates $\frac{1}{1-v}$ as $+\log_e|1-v|$, so $(1-v)^3(1+v) = Cx^2$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{1+2v}{2+v} - v = \frac{1-v^2}{2+v}$, so $\frac{(2+v)\,dv}{(1-v)(1+v)} = \frac{dx}{x}$. Partial fractions give $\frac{3/2}{1-v} + \frac{1/2}{1+v}$, so $-\frac{3}{2}\log_e|1-v| + \frac{1}{2}\log_e|1+v| = \log_e|x| + c$, i.e. $\frac{1+v}{(1-v)^3} = Cx^2$. Since $\frac{1+v}{(1-v)^3} = \frac{x^2(x+y)}{(x-y)^3}$, this is $x + y = C(x-y)^3$.",
  "Errors in partial-fraction coefficients or the sign of $\\int\\frac{dv}{1-v}$.",
  "U09-B-gs-partial-fractions", "Substitution, partial fractions, careful recombination of logarithms and powers.",
  check=_c028, source_class="XII", values=[slope((x + y)/(x - y)**3), slope(x*(x + y)/(x - y)**3), slope(x**2*(x + y)/(x - y)**3), slope((x + y)*(x - y)**3/x**6)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 029
def _c029():
    return (x + y)/(x - y)
q("U09-B-029", TOP_GS, "Solution in inverse tangent and logarithm", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, the general solution of $\frac{dy}{dx} = \frac{x + y}{x - y}$ (where $C$ is an arbitrary constant) is",
  r"$\tan^{-1}\left(\frac{y}{x}\right) = \log_e\sqrt{x^{2} + y^{2}} + C$",
  [(r"$\tan^{-1}\left(\frac{y}{x}\right) = \log_e\frac{x^{2}}{\sqrt{x^{2} + y^{2}}} + C$", r"Integrates $-\frac{v}{1+v^2}$ as $+\frac{1}{2}\log_e(1+v^2)$, a sign slip, so $\tan^{-1}v = \log_e x - \frac{1}{2}\log_e(1+v^2) + c = \log_e\frac{x^2}{\sqrt{x^2+y^2}} + c$."),
   (r"$\tan^{-1}\left(\frac{y}{x}\right) = \log_e\frac{x^{2} + y^{2}}{x} + C$", r"Integrates $\frac{v}{1+v^2}$ as $\log_e(1+v^2)$, missing the factor $\frac{1}{2}$."),
   (r"$\tan^{-1}\left(\frac{y}{x}\right) = \log_e\frac{\sqrt{x^{2} + y^{2}}}{x} + C$", r"Writes $\tan^{-1}v = \frac{1}{2}\log_e(1+v^2) + C$, forgetting the $\log_e x$ from integrating $\frac{dx}{x}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{1+v}{1-v} - v = \frac{1+v^2}{1-v}$, so $\frac{(1-v)\,dv}{1+v^2} = \frac{dx}{x}$. Integrating, $\tan^{-1}v - \frac{1}{2}\log_e(1+v^2) = \log_e x + c$. Since $\log_e x + \frac{1}{2}\log_e(1+v^2) = \log_e\sqrt{x^2+y^2}$, this is $\tan^{-1}\left(\frac{y}{x}\right) = \log_e\sqrt{x^2+y^2} + C$.",
  "Splitting $\\frac{1-v}{1+v^2}$ and losing a sign or factor in one part.",
  "U09-B-gs-polar", "Substitution, splitting the integrand, recombining logarithms.",
  check=_c029, source_class="XII", values=[slope(atan(y/x) - log(sqrt(x**2 + y**2))), slope(atan(y/x) - log(x**2/sqrt(x**2 + y**2))),
                       slope(atan(y/x) - log((x**2 + y**2)/x)), slope(atan(y/x) - log(sqrt(x**2 + y**2)/x))],
  cognitive="Application")

# ---------------------------------------------------------------- 030
def _c030():
    f1 = (y**2 - 3*x**2)/(2*x*y)
    s1 = equal_expr(slope((3*x**2 + y**2)/x**3), f1)
    f2 = (x**2*y + y**3)/x**3
    G = vint(Fv(f2))
    K = G.subs(vp, 1) - log(1)
    x1 = exp(Rational(1, 4))
    vs = [r for r in solve(Eq(G, log(x1) + K), vp) if r > 0]
    s2 = len(vs) == 1 and simplify(x1*vs[0] - sqrt(2)*exp(Rational(1, 4))) == 0
    return (bool(s1), bool(s2))


def equal_expr(a, b):
    return simplify(a - b) == 0


q("U09-B-030", TOP_PS, "Checking claimed solutions", "Medium", "Statement-based MCQ",
  r"Statement I: The general solution of $\frac{dy}{dx} = \frac{y^{2} - 3x^{2}}{2xy}$ (where $C$ is an arbitrary constant) is $3x^{2} + y^{2} = Cx^{3}$. Statement II: If $y = y(x)$, $x > 0$, $y > 0$, satisfies $x^{3}\frac{dy}{dx} = x^{2}y + y^{3}$ and $y(1) = 1$, then $y\left(e^{1/4}\right) = \sqrt{2}\,e^{1/4}$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I by slipping a sign in $\frac{v^2-3}{2v} - v$, writing $+\frac{3+v^2}{2v}$, so $3 + v^2 = Cx$ and $3x^2 + y^2 = Cx^3$; verifies Statement II correctly."),
   (ST_TF, r"Accepts Statement I through the same sign slip and, in Statement II, integrates $v^{-3}$ as $\frac{1}{2v^2}$, getting $v^2 = \frac{2}{3}$ instead of $2$."),
   (ST_FF, r"Rejects Statement I correctly but in Statement II forgets to multiply $v = \sqrt{2}$ by $x$ and so rejects the value $\sqrt{2}\,e^{1/4}$.")],
  r"Statement I: with $y = vx$, $x\frac{dv}{dx} = \frac{v^2-3}{2v} - v = -\frac{3+v^2}{2v}$, so $\frac{2v\,dv}{3+v^2} = -\frac{dx}{x}$ and $x(3 + v^2) = C$, i.e. $3x^2 + y^2 = Cx$, not $Cx^3$; false. Statement II: with $y = vx$, $x\frac{dv}{dx} = v^3$, so $-\frac{1}{2v^2} = \log_e x + c$ and $c = -\frac{1}{2}$. At $x = e^{1/4}$, $\frac{1}{2v^2} = \frac{1}{4}$, so $v = \sqrt{2}$ and $y = \sqrt{2}\,e^{1/4}$; true.",
  r"Losing the sign of $-v$ when forming $x\frac{dv}{dx}$, which changes the power of $x$ in the family.",
  "U09-B-statement-ps", "Two independent solve-and-verify tasks.",
  check=_c030, source_class="XII", values=[(F_, T), (T, T), (T, F_), (F_, F_)], cognitive="Analysis")

# ---------------------------------------------------------------- 031
def _c031():
    f = y/x + 2*tan(y/x)
    G = vint(Fv(f, v), v)
    K = G.subs(v, pi/6) - log(1)
    x1 = root(2, 4)
    # continuity from v = pi/6 at x = 1 on 0 < x < sqrt(2) keeps v in (0, pi/2)
    s = [r for r in solve(Eq(G, log(x1) + K), v) if 0 < r < pi/2]
    assert len(s) == 1
    return x1*s[0]
q("U09-B-031", TOP_PS, "Value of a particular solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $0 < x < \sqrt{2}$, be the solution of $\frac{dy}{dx} = \frac{y}{x} + 2\tan\left(\frac{y}{x}\right)$ with $y(1) = \frac{\pi}{6}$. Then $y\left(\sqrt[4]{2}\right)$ equals",
  r"$\frac{\pi\sqrt[4]{2}}{4}$",
  [(r"$\frac{\pi}{4}$", r"Finds $\frac{y}{x} = \frac{\pi}{4}$ at $x = \sqrt[4]{2}$ and reports it as $y$."),
   (r"$\frac{3\pi\sqrt[4]{2}}{4}$", r"Solves $\sin v = \frac{\sqrt{2}}{2}$ with $v = \frac{3\pi}{4}$; reaching it from $v = \frac{\pi}{6}$ would need $v = \frac{\pi}{2}$, where $\sin v = \frac{x^2}{2}$ forces $x = \sqrt{2}$."),
   (r"$\frac{\pi\sqrt[4]{2}}{6}$", r"Assumes $\frac{y}{x}$ keeps its initial value $\frac{\pi}{6}$ along the curve, so $y = \frac{\pi}{6}\cdot\sqrt[4]{2}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = 2\tan v$, so $\cot v\,dv = \frac{2\,dx}{x}$ and $\sin v = Cx^2$. At $x = 1$, $v = \frac{\pi}{6}$, so $C = \frac{1}{2}$ and $\sin v = \frac{x^2}{2}$, with $v$ staying in $\left(0, \frac{\pi}{2}\right)$ for $0 < x < \sqrt{2}$. At $x = \sqrt[4]{2}$, $\sin v = \frac{\sqrt{2}}{2}$, so $v = \frac{\pi}{4}$ and $y = \frac{\pi\sqrt[4]{2}}{4}$.",
  r"Choosing the wrong inverse-sine branch, or forgetting $y = vx$.",
  "U09-B-ps-trig-value", "Substitution, constant at a non-trivial point, branch choice by continuity.",
  check=_c031, source_class="XII", values=[pi*root(2, 4)/4, pi/4, 3*pi*root(2, 4)/4, pi*root(2, 4)/6], cognitive="Application")

# ---------------------------------------------------------------- 032
def _c032():
    sols = solveset(Eq(m, m**3 - 3*m**2 + 3*m), m, S.Reals)
    good = [s for s in sols if simplify(x**3*s - ((s*x)**3 - 3*x*(s*x)**2 + 3*x**2*(s*x))) == 0]
    return len(good)
q("U09-B-032", TOP_ID, "Straight-line solutions through the origin", "Medium", "Multi-step computation MCQ",
  r"The number of real values of $m$ for which $y = mx$ ($x > 0$) is a solution of $x^{3}\frac{dy}{dx} = y^{3} - 3xy^{2} + 3x^{2}y$ is",
  r"$3$",
  [(r"$2$", r"Divides $m^3 - 3m^2 + 2m = 0$ by $m$ and loses the root $m = 0$ (the line $y = 0$)."),
   (r"$1$", r"Forgets that $\frac{dy}{dx} = m$ and sets the right side equal to zero: $m(m^2 - 3m + 3) = 0$ has only the real root $m = 0$."),
   (r"$4$", r"Finds $m = 0, 1, 2$ and also counts the $y$-axis, which is not of the form $y = mx$.")],
  r"For $y = mx$, $\frac{dy}{dx} = m$ and the equation becomes $mx^3 = (m^3 - 3m^2 + 3m)x^3$. So $m^3 - 3m^2 + 2m = 0$, i.e. $m(m-1)(m-2) = 0$, giving $m = 0, 1, 2$. Hence there are $3$ values.",
  "Dividing by $m$ and losing the trivial line $y = 0$.",
  "U09-B-line-solution", "Substitution, cubic factorisation, counting with a trap.",
  check=_c032, source_class="XII", values=[3, 2, 1, 4], cognitive="Analysis",
  numerical=dict(question=r"The number of real values of $m$ for which $y = mx$ ($x > 0$) is a solution of $x^{3}\frac{dy}{dx} = y^{3} - 3xy^{2} + 3x^{2}y$ is", answer=3))

# ---------------------------------------------------------------- 033
def _c033():
    # (x - y ln y + y ln x) dx + x (ln y - ln x) dy = 0
    return -(x - y*log(y) + y*log(x))/(x*(log(y) - log(x)))
q("U09-B-033", TOP_GS, "Logarithmic homogeneous equation", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $y > 0$, the general solution of $\left(x - y\log_e y + y\log_e x\right)dx + x\left(\log_e y - \log_e x\right)dy = 0$ (where $C$ is an arbitrary constant) is",
  r"$x\log_e x + y\log_e\frac{y}{x} - y = Cx$",
  [(r"$x\log_e x + y\log_e\frac{y}{x} = Cx$", r"Integrates $\log_e v$ as $v\log_e v$, forgetting the $-v$ term."),
   (r"$x\log_e x - y\log_e\frac{y}{x} + y = Cx$", r"Separates with a sign slip as $\frac{dx}{x} = \log_e v\,dv$."),
   (r"$x\log_e x + y\log_e\frac{y}{x} - y = C$", r"Reaches $\log_e x + v\log_e v - v = C$ but multiplies through by $x$ on the left side only.")],
  r"Write the equation as $(1 - v\log_e v)\,dx + \log_e v\,dy = 0$ with $y = vx$, after dividing by $x$. Since $dy = v\,dx + x\,dv$, it becomes $dx + x\log_e v\,dv = 0$, so $\frac{dx}{x} + \log_e v\,dv = 0$. Integrating, $\log_e x + v\log_e v - v = C$; multiplying by $x$ gives $x\log_e x + y\log_e\frac{y}{x} - y = Cx$.",
  r"Errors in $\int\log_e v\,dv = v\log_e v - v$.",
  "U09-B-gs-log", "Recognising homogeneity in log form, substitution, integration by parts result.",
  check=_c033, source_class="XII", values=[slope((x*log(x) + y*log(y/x) - y)/x), slope((x*log(x) + y*log(y/x))/x),
                       slope((x*log(x) - y*log(y/x) + y)/x), slope(x*log(x) + y*log(y/x) - y)],
  cognitive="Application")

# ---------------------------------------------------------------- 034
def _c034():
    kk = Symbol('kk', positive=True)
    f = y/x + kk*x**2/y**2
    G = vint(Fv(f))
    K = G.subs(vp, 1) - log(1)
    return solve(Eq(G.subs(vp, 2), log(E) + K), kk)[0]
q("U09-B-034", TOP_CURVE, "Parameter from a point on the curve", "Medium", "Inverse/parameter MCQ",
  r"For a constant $k > 0$, the solution curve of $\frac{dy}{dx} = \frac{y}{x} + \frac{kx^{2}}{y^{2}}$ ($x > 0$, $y > 0$) through $(1,1)$ passes through $(e, 2e)$. Then $k$ equals",
  r"$\frac{7}{3}$",
  [(r"$7$", r"Integrates $v^2$ as $v^3$, so $v^3 = k\log_e x + 1$ and $8 = k + 1$."),
   (r"$\frac{8}{3}$", r"Omits the constant of integration, using $\frac{v^3}{3} = k\log_e x$ at $(e, 2e)$ only."),
   (r"$\frac{8e^{3} - 1}{3}$", r"Solves correctly up to $\frac{v^3}{3} = k\log_e x + \frac{1}{3}$ but substitutes $v = 2e$ (the ordinate) at $(e, 2e)$ instead of $v = \frac{2e}{e} = 2$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{k}{v^2}$, so $v^2\,dv = k\frac{dx}{x}$ and $\frac{v^3}{3} = k\log_e x + c$. At $(1,1)$, $c = \frac{1}{3}$. At $(e, 2e)$, $v = 2$: $\frac{8}{3} = k + \frac{1}{3}$, so $k = \frac{7}{3}$.",
  "Dropping the factor $\\frac{1}{3}$ or the constant of integration.",
  "U09-B-parameter-from-point", "Solve with an unknown parameter, then two point conditions.",
  check=_c034, source_class="XII", values=[Rational(7, 3), 7, Rational(8, 3), (8*E**3 - 1)/3], cognitive="Application",
  numerical=dict(question=r"For a constant $k > 0$, the solution curve of $\frac{dy}{dx} = \frac{y}{x} + \frac{kx^{2}}{y^{2}}$ ($x > 0$, $y > 0$) through $(1,1)$ passes through $(e, 2e)$. Then the value of $3k$ is", answer=7))

# ---------------------------------------------------------------- 035
def _c035():
    f = (y**2 - x**2)/(2*x*y)
    G = vint(Fv(f))
    I = simplify(x/exp(G.subs(vp, y/x)))
    C0 = I.subs({x: 1, y: 3})
    eq = expand(simplify(I*x) - C0*x)
    P = Poly(eq, x, y)
    assert P.coeff_monomial(x**2) == 1 and P.coeff_monomial(y**2) == 1
    g = P.coeff_monomial(x)/2
    f0 = P.coeff_monomial(y)/2
    c0 = P.coeff_monomial(1)
    return sqrt(g**2 + f0**2 - c0)
q("U09-B-035", TOP_CURVE, "Solution curve that is a circle", "Medium", "Multi-step computation MCQ",
  r"The solution curve of $2xy\frac{dy}{dx} = y^{2} - x^{2}$, $x > 0$, passing through $(1, 3)$ is an arc of a circle. The radius of this circle is",
  r"$5$",
  [(r"$10$", r"Finds $x^2 + y^2 = 10x$ correctly and takes the constant $10$ as the radius instead of the diameter."),
   (r"$\sqrt{10}$", r"Clears $1 + v^2 = \frac{C}{x}$ as $x^2 + y^2 = C$, a circle centred at the origin, and gets $C = 10$."),
   (r"$3\sqrt{10}$", r"Finds $x^2 + y^2 = 10x$ but places the centre at $(10, 0)$ and measures its distance to $(1,3)$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{v^2-1}{2v} - v = -\frac{1+v^2}{2v}$, so $\frac{2v\,dv}{1+v^2} = -\frac{dx}{x}$ and $x(1+v^2) = C$, i.e. $x^2 + y^2 = Cx$. Through $(1,3)$, $C = 10$. The circle $x^2 + y^2 - 10x = 0$ has centre $(5,0)$ and radius $5$.",
  r"Reading the constant in $x^2 + y^2 = Cx$ as the radius.",
  "U09-B-curve-circle", "Solve, fix constant, then interpret the conic.",
  check=_c035, source_class="XII", values=[5, 10, sqrt(10), 3*sqrt(10)], cognitive="Application",
  numerical=dict(question=r"The solution curve of $2xy\frac{dy}{dx} = y^{2} - x^{2}$, $x > 0$, passing through $(1, 3)$ is an arc of a circle. The radius of this circle is", answer=5))

# ---------------------------------------------------------------- 036
def _c036():
    p = Symbol('p')
    # tangent at P(x, y) meets y-axis at T(0, y - x p); OT = PT
    sol = solve(Eq((y - x*p)**2, x**2 + (x*p)**2), p)
    assert len(sol) == 1
    f = sol[0]
    G = vint(Fv(f))
    I = simplify(x/exp(G.subs(vp, y/x)))
    C0 = I.subs({x: 2, y: 1})
    b = Symbol('b', positive=True)
    s = solve(Eq(I.subs({x: Rational(1, 2), y: b}), C0), b)
    assert len(s) == 1
    return s[0]
q("U09-B-036", TOP_APP, "Curve from a tangent property", "Difficult", "Multi-step computation MCQ",
  r"A curve in the region $x > 0$, $y > 0$ passes through $(2, 1)$. At every point $P$ of the curve, the tangent at $P$ meets the $y$-axis at a point $T$ such that $T$ is equidistant from $P$ and the origin $O$. If the curve also passes through $\left(\frac{1}{2}, \beta\right)$, then $\beta$ equals",
  r"$1$",
  [(r"$2$", r"Reaches $x(1 + v^2) = \frac{5}{2}$ correctly but substitutes $v = \beta$ at $x = \frac{1}{2}$ instead of $v = \frac{\beta}{1/2} = 2\beta$, so $\frac{1}{2}(1 + \beta^2) = \frac{5}{2}$."),
   (r"$\frac{\sqrt{19}}{2}$", r"Integrates $\frac{2v}{1+v^2}$ as $\frac{1}{2}\log_e(1+v^2)$, so $x^2(1+v^2) = C$, i.e. $x^2 + y^2 = 5$, and $\beta^2 = 5 - \frac{1}{4}$."),
   (r"$\frac{\sqrt{13}}{8}$", r"Uses $\frac{dy}{dx} = x\frac{dv}{dx}$, dropping the term $v$, so $\frac{2v\,dv}{v^2-1} = \frac{dx}{x}$, $y^2 - x^2 = Cx^3$ with $C = -\frac{3}{8}$, and $\beta^2 - \frac{1}{4} = -\frac{3}{64}$.")],
  r"The tangent at $P(x,y)$ meets the $y$-axis at $T(0, y - xy')$. From $OT^2 = PT^2$: $(y - xy')^2 = x^2 + x^2y'^2$, which gives $y' = \frac{y^2 - x^2}{2xy}$. With $y = vx$, $x\frac{dv}{dx} = -\frac{1+v^2}{2v}$, so $\frac{2v\,dv}{1+v^2} = -\frac{dx}{x}$ and $x(1 + v^2) = C$, i.e. $x^2 + y^2 = Cx$. Through $(2,1)$, $C = \frac{5}{2}$. At $x = \frac{1}{2}$: $\frac{1}{4} + \beta^2 = \frac{5}{4}$, so $\beta = 1$ (as $y > 0$).",
  "Substituting $v = y$ instead of $v = \\frac{y}{x}$ at a point with $x \\ne 1$, or mishandling $\\int\\frac{2v}{1+v^2}\\,dv$.",
  "U09-B-geom-tangent", "Translate geometry into an equation, solve the homogeneous equation, fix the constant, evaluate at a second point.",
  check=_c036, source_class="XII", values=[1, 2, sqrt(19)/2, sqrt(13)/8], cognitive="Analysis")

# ---------------------------------------------------------------- 037
def _c037():
    return (x**3 - 3*x*y**2)/(y**3 - 3*x**2*y)
q("U09-B-037", TOP_GS, "Cubic homogeneous equation with partial fractions", "Difficult", "Multi-step computation MCQ",
  r"The general solution of $(x^{3} - 3xy^{2})\,dx = (y^{3} - 3x^{2}y)\,dy$ (where $C$ is an arbitrary constant) is",
  r"$x^{2} - y^{2} = C(x^{2} + y^{2})^{2}$",
  [(r"$x(x^{2} - y^{2}) = C(x^{2} + y^{2})^{2}$", r"Puts $u = v^2$ but forgets that $v\,dv = \frac{1}{2}du$, so the left side is doubled and $\frac{1-u}{(1+u)^2} = Cx$."),
   (r"$(x^{2} - y^{2})(x^{2} + y^{2})^{2} = Cx^{4}$", r"Integrates $\frac{-1}{1-u}$ as $-\log_e|1-u|$ (missing the chain-rule sign), so $(1-u)(1+u)^2 = \frac{C}{x^2}$."),
   (r"$x - y = Cx(x + y)^{2}$", r"Reaches $\frac{1-u}{(1+u)^2} = Cx^2$ correctly but back-substitutes $u = \frac{y}{x}$ instead of $\frac{y^2}{x^2}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = \frac{1-3v^2}{v^3-3v} - v = \frac{1-v^4}{v^3-3v}$, so $\frac{v(v^2-3)\,dv}{(1-v^2)(1+v^2)} = \frac{dx}{x}$. Put $u = v^2$: $\frac{1}{2}\int\left(\frac{-1}{1-u} - \frac{2}{1+u}\right)du = \frac{1}{2}\log_e|1-u| - \log_e(1+u)$. So $\frac{1-v^2}{(1+v^2)^2} = Cx^2$, i.e. $\frac{x^2(x^2-y^2)}{(x^2+y^2)^2} = Cx^2$, giving $x^2 - y^2 = C(x^2+y^2)^2$.",
  "Losing the factor $\\frac{1}{2}$ from $u = v^2$ or a sign in $\\int\\frac{du}{1-u}$.",
  "U09-B-gs-partial-fractions", "Long simplification, second substitution, partial fractions, recombination.",
  check=_c037, source_class="XII", values=[slope((x**2 - y**2)/(x**2 + y**2)**2), slope(x*(x**2 - y**2)/(x**2 + y**2)**2),
                       slope((x**2 - y**2)*(x**2 + y**2)**2/x**4), slope((x - y)/(x*(x + y)**2))],
  cognitive="Analysis")

# ---------------------------------------------------------------- 038
def _c038():
    f = (y - x)/(x + y)
    G = vint(Fv(f, v), v)
    K = G.subs(v, 1) - log(1)
    X = Symbol('X', positive=True)
    return solve(Eq(G.subs(v, 0), log(X) + K), X)[0]
q("U09-B-038", TOP_CURVE, "Where a solution curve meets an axis", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, be the solution of $(x + y)\,dy + (x - y)\,dx = 0$ with $y(1) = 1$. The arc of this solution curve lying in the region $x > 0$ meets the $x$-axis at the point whose abscissa is",
  r"$\sqrt{2}\,e^{\pi/4}$",
  [(r"$\frac{e^{-\pi/4}}{\sqrt{2}}$", r"Separates as $\frac{(1+v)\,dv}{1+v^2} = +\frac{dx}{x}$, losing the minus sign, so $\log_e x = -\left(\frac{\pi}{4} + \frac{1}{2}\log_e 2\right)$ at $y = 0$."),
   (r"$2e^{\pi/4}$", r"Integrates $\frac{v}{1+v^2}$ as $\log_e(1+v^2)$, missing the factor $\frac{1}{2}$, so the constant becomes $\frac{\pi}{4} + \log_e 2$."),
   (r"$e^{\pi/4}$", r"Fixes the constant as $\frac{\pi}{4}$, dropping the term $\frac{1}{2}\log_e 2$ that comes from $\log_e\sqrt{x^2+y^2}$ at $(1,1)$.")],
  r"Here $\frac{dy}{dx} = \frac{y - x}{x + y}$. With $y = vx$: $x\frac{dv}{dx} = \frac{v-1}{1+v} - v = -\frac{1+v^2}{1+v}$, so $\frac{(1+v)\,dv}{1+v^2} = -\frac{dx}{x}$ and $\tan^{-1}v + \frac{1}{2}\log_e(1+v^2) = -\log_e x + c$, i.e. $\tan^{-1}\frac{y}{x} + \log_e\sqrt{x^2+y^2} = c$. At $(1,1)$, $c = \frac{\pi}{4} + \frac{1}{2}\log_e 2$. On the $x$-axis, $\log_e x = \frac{\pi}{4} + \frac{1}{2}\log_e 2$, so $x = \sqrt{2}\,e^{\pi/4}$.",
  r"Losing the constant contribution $\log_e\sqrt{2}$ at the initial point.",
  "U09-B-ps-polar", "Substitution, split integrand, constant with two parts, evaluation.",
  check=_c038, source_class="XII", values=[sqrt(2)*exp(pi/4), exp(-pi/4)/sqrt(2), 2*exp(pi/4), exp(pi/4)], cognitive="Analysis")

# ---------------------------------------------------------------- 039
def _c039():
    p = Symbol('p')
    # tangent at P(x, y) meets x-axis at x - y/p; this equals y
    pp = solve(Eq(x - y/p, y), p)[0]
    g = simplify(1/pp)  # dx/dy
    H = vint(Gx(g, v), v)
    K = H.subs(v, 2) - log(1)
    Y = Symbol('Y', positive=True)
    return solve(Eq(H.subs(v, 0), log(Y) + K), Y)[0]
q("U09-B-039", TOP_APP, "Curve from a tangent-intercept property", "Difficult", "Multi-step computation MCQ",
  r"A curve passes through $(2, 1)$ and lies in the region $x \ge 0$, $y > 0$. At every point $P(x, y)$ of the curve, the tangent meets the $x$-axis at a point whose abscissa equals $y$. If the curve meets the $y$-axis at $(0, \beta)$, then $\beta$ equals",
  r"$e^{2}$",
  [(r"$e^{-2}$", r"Solves to $\frac{x}{y} = 2 - \log_e y$ but writes it as $\frac{x}{y} = 2 + \log_e y$ through a sign slip, so $\log_e\beta = -2$."),
   (r"$1$", r"Drops the constant of integration, using $\frac{x}{y} = -\log_e y$, so $\log_e\beta = 0$."),
   (r"$\sqrt{e}$", r"Evaluates the constant with $\frac{y}{x} = \frac{1}{2}$ at $(2,1)$ instead of $\frac{x}{y} = 2$, so $\frac{x}{y} = \frac{1}{2} - \log_e y$.")],
  r"The tangent at $P$ meets the $x$-axis at $x - \frac{y}{y'}$, so $x - \frac{y}{y'} = y$, i.e. $\frac{dx}{dy} = \frac{x - y}{y}$. Put $x = vy$: $v + y\frac{dv}{dy} = v - 1$, so $dv = -\frac{dy}{y}$ and $\frac{x}{y} = c - \log_e y$. At $(2,1)$, $c = 2$. At $x = 0$: $\log_e\beta = 2$, so $\beta = e^2$.",
  r"Choosing $y = vx$ when $\frac{dx}{dy}$ is the simpler form, then losing track of the constant.",
  "U09-B-geom-intercept", "Geometry to equation, choosing $x = vy$, constant and evaluation.",
  check=_c039, source_class="XII", values=[E**2, exp(-2), 1, sqrt(E)], cognitive="Analysis")

# ---------------------------------------------------------------- 040
def _c040():
    f = y/x + exp(2*y/x)
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    x1 = exp(Rational(1, 4))
    s = solve(Eq(G, log(x1) + K), v)
    return x1*s[0]
q("U09-B-040", TOP_PS, "Value of a particular solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$ satisfy $x\frac{dy}{dx} = y + x\,e^{2y/x}$ for $0 < x < \sqrt{e}$, with $y(1) = 0$. Then $y\left(e^{1/4}\right)$ equals",
  r"$\frac{e^{1/4}\log_e 2}{2}$",
  [(r"$-\frac{e^{1/4}\log_e 2}{2}$", r"Solves $e^{-2v} = \frac{1}{2}$ as $v = -\frac{1}{2}\log_e 2$, a sign slip with the negative exponent."),
   (r"$\frac{e^{1/4}}{2}\log_e\frac{4}{3}$", r"Integrates $e^{-2v}$ as $-e^{-2v}$, missing the factor $\frac{1}{2}$, so $e^{-2v} = 1 - \log_e x = \frac{3}{4}$ at $x = e^{1/4}$."),
   (r"$\frac{\log_e 2}{2}$", r"Finds $v = \frac{1}{2}\log_e 2$ and reports it as $y$ without multiplying by $e^{1/4}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = e^{2v}$, so $e^{-2v}\,dv = \frac{dx}{x}$ and $-\frac{1}{2}e^{-2v} = \log_e x + c$. From $y(1) = 0$, $c = -\frac{1}{2}$, so $e^{-2y/x} = 1 - 2\log_e x$. At $x = e^{1/4}$: $e^{-2v} = \frac{1}{2}$, so $v = \frac{1}{2}\log_e 2$ and $y = \frac{e^{1/4}\log_e 2}{2}$.",
  r"Losing the factor $\frac{1}{2}$ in $\int e^{-2v}\,dv$, or a sign error in solving for $v$.",
  "U09-B-ps-exp-value", "Substitution, constant, solving an exponential equation with signs.",
  check=_c040, source_class="XII", values=[exp(Rational(1, 4))*log(2)/2, -exp(Rational(1, 4))*log(2)/2, exp(Rational(1, 4))*log(Rational(4, 3))/2, log(2)/2], cognitive="Application")

# ---------------------------------------------------------------- 041
def _c041():
    g = (x**2 + y**2)/(x*y)  # dx/dy
    H = vint(Gx(g))
    K = H.subs(vp, 1) - log(1)
    s = [r for r in solve(Eq(H, log(E) + K), vp) if r > 0]
    return E*s[0]
q("U09-B-041", TOP_XVY, "Particular solution with x = vy", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, $y > 0$, be the solution of $(x^{2} + y^{2})\,dy = xy\,dx$ with $y(1) = 1$. If $y(x_{0}) = e$, then $x_{0}$ equals",
  r"$\sqrt{3}\,e$",
  [(r"$\sqrt{2}\,e$", r"Integrates $v\,dv$ as $v^2$, so $v^2 = \log_e y + 1$ and $v^2 = 2$ at $y = e$."),
   (r"$\sqrt{3}$", r"Finds $\frac{x}{y} = \sqrt{3}$ and reports it as $x_0$ without multiplying by $y = e$."),
   (r"$3e$", r"Finds $\left(\frac{x}{y}\right)^2 = 3$ but forgets the square root, taking $\frac{x}{y} = 3$.")],
  r"Write $\frac{dx}{dy} = \frac{x^2 + y^2}{xy} = \frac{x}{y} + \frac{y}{x}$ and put $x = vy$: $v + y\frac{dv}{dy} = v + \frac{1}{v}$, so $v\,dv = \frac{dy}{y}$ and $\frac{v^2}{2} = \log_e y + c$. At $(1,1)$, $c = \frac{1}{2}$, so $x^2 = y^2(2\log_e y + 1)$. At $y = e$: $x_0^2 = 3e^2$, so $x_0 = \sqrt{3}\,e$.",
  r"Using $y = vx$, which leads to a harder integral, then making slips; $x = vy$ separates at once.",
  "U09-B-xvy-ps", "Recognising $x = vy$ as the efficient route, constant, solving for $x$.",
  check=_c041, source_class="XII", values=[sqrt(3)*E, sqrt(2)*E, sqrt(3), 3*E], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c042():
    f = (y + sqrt(x**2 - y**2))/x
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    s = solve(Eq(G, log(x) + K), v)
    assert len(s) == 1
    yy = x*s[0]
    # verify it solves the equation on the interval (cos(ln x) >= 0 there)
    xs = Rational(3, 2)
    assert abs(N((x*diff(yy, x) - yy - sqrt(x**2 - yy**2)).subs(x, xs))) < 1e-12
    return simplify(integrate(yy, (x, 1, exp(pi/2))))
q("U09-B-042", TOP_PS, "Integral of a particular solution", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $1 \le x \le e^{\pi/2}$, be the solution of $x\,dy - y\,dx = \sqrt{x^{2} - y^{2}}\,dx$ with $y(1) = 0$. Then $\int_{1}^{e^{\pi/2}} y(x)\,dx$ equals",
  r"$\frac{2e^{\pi} + 1}{5}$",
  [(r"$\frac{2e^{\pi} - 1}{5}$", r"Uses $\int e^{2t}\sin t\,dt = \frac{e^{2t}(2\sin t + \cos t)}{5}$, a sign slip in the standard result."),
   (r"$\frac{e^{\pi/2} + 1}{2}$", r"Substitutes $x = e^{t}$ but forgets $dx = e^{t}dt$, integrating $e^{t}\sin t$ from $0$ to $\frac{\pi}{2}$."),
   (r"$-\frac{2e^{\pi} + 1}{5}$", r"Integrates $\frac{dv}{\sqrt{1-v^2}}$ as $+\cos^{-1}v$, so $y = -x\sin(\log_e x)$.")],
  r"With $y = vx$ ($x > 0$): $x\frac{dv}{dx} = \sqrt{1-v^2}$, so $\sin^{-1}v = \log_e x + c$ and $c = 0$, giving $y = x\sin(\log_e x)$ on the given interval. Put $x = e^{t}$: $\int_0^{\pi/2} e^{2t}\sin t\,dt = \left[\frac{e^{2t}(2\sin t - \cos t)}{5}\right]_0^{\pi/2} = \frac{2e^{\pi} + 1}{5}$.",
  r"Forgetting the Jacobian $dx = e^{t}dt$ when substituting $x = e^{t}$.",
  "U09-B-ps-integral", "Solve the equation, then a non-trivial definite integral by substitution and a standard formula.",
  check=_c042, source_class="XII", values=[(2*exp(pi) + 1)/5, (2*exp(pi) - 1)/5, (exp(pi/2) + 1)/2, -(2*exp(pi) + 1)/5], cognitive="Analysis")

# ---------------------------------------------------------------- 043
def _c043():
    f = (x**2 + 3*x*y + y**2)/x**2
    G = vint(Fv(f, v), v)
    K = G.subs(v, 0) - log(1)
    x1 = sqrt(E)
    s = solve(Eq(G, log(x1) + K), v)
    assert len(s) == 1
    return x1*s[0]
q("U09-B-043", TOP_PS, "Perfect square after substitution", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $1 \le x < e$, be the solution of $x^{2}\frac{dy}{dx} = x^{2} + 3xy + y^{2}$ with $y(1) = 0$. Then $y(\sqrt{e})$ equals",
  r"$\sqrt{e}$",
  [(r"$1$", r"Finds $\frac{y}{x} = 1$ at $x = \sqrt{e}$ and reports it as $y$."),
   (r"$-\frac{\sqrt{e}}{3}$", r"Integrates $\frac{dv}{(v+1)^2}$ as $+\frac{1}{v+1}$, so $\frac{1}{v+1} = \log_e x + 1$ and $v + 1 = \frac{2}{3}$ at $x = \sqrt{e}$."),
   (r"$2\sqrt{e}$", r"Finds $v + 1 = \frac{1}{1 - \log_e x} = 2$ and takes this as $\frac{y}{x}$, forgetting to subtract $1$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = 1 + 2v + v^2 = (v+1)^2$, so $\frac{dv}{(v+1)^2} = \frac{dx}{x}$ and $-\frac{1}{v+1} = \log_e x + c$. From $v(1) = 0$, $c = -1$, so $v + 1 = \frac{1}{1 - \log_e x}$. At $x = \sqrt{e}$: $v + 1 = 2$, so $v = 1$ and $y = \sqrt{e}$.",
  r"Losing track of the shift $v + 1$ when returning to $y$.",
  "U09-B-ps-perfect-square", "Spotting the perfect square, sign care in the integral, back-substitution through a shift.",
  check=_c043, source_class="XII", values=[sqrt(E), 1, -sqrt(E)/3, 2*sqrt(E)], cognitive="Analysis")

# ---------------------------------------------------------------- 044
def _c044():
    p = Symbol('p')
    pp = solve(Eq(x - y/p, sqrt(x**2 + y**2)), p)
    assert len(pp) == 1
    G = vint(Fv(pp[0]))
    I = simplify(exp(log(x) - G.subs(vp, y/x)))
    I0 = simplify(I.subs({x: 3, y: 4}))
    s = solve(Eq(limit(I, x, 0), I0), y)
    return s[0]
q("U09-B-044", TOP_APP, "Curve from a tangent-intercept property", "Difficult", "Multi-step computation MCQ",
  r"A curve passes through $(3, 4)$. At every point $P(x, y)$ of the curve with $y > 0$, the tangent at $P$ meets the $x$-axis at a point whose abscissa equals $OP$, where $O$ is the origin. If the curve meets the $y$-axis at $(0, \beta)$ with $\beta > 0$, then $\beta$ equals",
  r"$8$",
  [(r"$5$", r"Reads the condition as $OP$ being constant, so the curve is the circle $x^2 + y^2 = 25$ and $\beta = 5$."),
   (r"$2$", r"Takes the intercept as $-OP$ (point on the negative $x$-axis), which gives $\sqrt{x^2+y^2} = x + c$ with $c = 2$."),
   (r"$18$", r"Reaches $x\left(1 + \sqrt{1+v^2}\right) = c$ but evaluates $\sqrt{1+v^2}$ at $(3,4)$ as $OP = 5$, getting $c = 18$.")],
  r"The tangent meets the $x$-axis at $x - \frac{y}{y'}$, so $x - \frac{y}{y'} = \sqrt{x^2+y^2}$ and $\frac{dy}{dx} = \frac{y}{x - \sqrt{x^2+y^2}}$, which is homogeneous. With $y = vx$ ($x > 0$) and $s = \sqrt{1+v^2}$: $x\frac{dv}{dx} = \frac{vs}{1-s}$, which integrates to $x(1 + s) = c$, i.e. $x + \sqrt{x^2+y^2} = c$. At $(3,4)$, $c = 8$. At $x = 0$: $\beta = 8$.",
  r"Misreading which intercept equals $OP$, or substituting $OP$ for $\frac{OP}{x}$.",
  "U09-B-geom-intercept", "Geometry to equation, an awkward separated integral, constant, evaluation.",
  check=_c044, source_class="XII", values=[8, 5, 2, 18], cognitive="Analysis",
  numerical=dict(question=r"A curve passes through $(3, 4)$. At every point $P(x, y)$ of the curve with $y > 0$, the tangent at $P$ meets the $x$-axis at a point whose abscissa equals $OP$, where $O$ is the origin. If the curve meets the $y$-axis at $(0, \beta)$ with $\beta > 0$, then $\beta$ is", answer=8))

# ---------------------------------------------------------------- 045
def _c045():
    f1 = y/x - exp(-y/x)
    G1 = vint(Fv(f1, v), v)
    K1 = G1.subs(v, 0) - log(1)
    s1 = solve(Eq(G1, log(x) + K1), v)
    st1 = len(s1) == 1 and limit(x*s1[0], x, E, '-') == -oo
    f2 = (x*y - y**2)/x**2
    G2 = vint(Fv(f2))
    K2 = G2.subs(vp, 1) - log(1)
    s2 = solve(Eq(G2, log(x) + K2), vp)
    st2 = len(s2) == 1 and limit(x*s2[0], x, 1/E, '+') == oo
    return (bool(st1), bool(st2))
q("U09-B-045", TOP_PS, "Behaviour of particular solutions", "Difficult", "Statement-based MCQ",
  r"Statement I: If $y = y(x)$ satisfies $x\frac{dy}{dx} = y - x\,e^{-y/x}$ with $y(1) = 0$, for $1 \le x < e$, then $y(x) \to -\infty$ as $x \to e^{-}$. Statement II: If $y = y(x)$ satisfies $x^{2}\frac{dy}{dx} = xy - y^{2}$ with $y(1) = 1$, for $\frac{1}{e} < x \le 1$, then $y(x) \to \infty$ as $x \to \left(\frac{1}{e}\right)^{+}$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"In Statement II integrates $-\frac{dv}{v^2}$ as $-\frac{1}{v}$, getting $y = \frac{x}{1 - \log_e x}$, which stays bounded near $x = \frac{1}{e}$."),
   (ST_FT, r"In Statement I integrates $-e^{v}$ with a sign slip, getting $e^{v} = 1 + \log_e x$, which is bounded as $x \to e^{-}$."),
   (ST_FF, r"Makes both integration sign slips above and concludes neither solution is unbounded.")],
  r"Statement I: with $y = vx$, $x\frac{dv}{dx} = -e^{-v}$, so $e^{v}\,dv = -\frac{dx}{x}$ and $e^{v} = 1 - \log_e x$; thus $y = x\log_e(1 - \log_e x) \to -\infty$ as $x \to e^{-}$; true. Statement II: $x\frac{dv}{dx} = -v^2$, so $\frac{1}{v} = \log_e x + 1$ and $y = \frac{x}{1 + \log_e x}$, which tends to $+\infty$ as $x \to \left(\frac{1}{e}\right)^{+}$; true.",
  "Sign slips with negative right sides, which change where the solution blows up.",
  "U09-B-statement-ps", "Two full solutions plus a limiting argument for each.",
  check=_c045, source_class="XII", values=[(T, T), (T, F_), (F_, T), (F_, F_)], cognitive="Analysis")

# ---------------------------------------------------------------- 046
def _c046():
    g = -(x**2 - x*y + y**2)/y**2  # dx/dy
    H = vint(Gx(g, v), v)
    K = H.subs(v, 0) - log(1)
    y1 = exp(-pi/3)
    s = solve(Eq(H, log(y1) + K), v)
    return y1*s[0]
q("U09-B-046", TOP_XVY, "Particular solution with x = vy", "Difficult", "Multi-step computation MCQ",
  r"Let $x = x(y)$, $y > 0$, satisfy $y^{2}\,dx + \left(x^{2} - xy + y^{2}\right)dy = 0$ for $e^{-\pi/2} < y \le 1$, with $x = 0$ when $y = 1$. Then the value of $x$ when $y = e^{-\pi/3}$ is",
  r"$\sqrt{3}\,e^{-\pi/3}$",
  [(r"$-\sqrt{3}\,e^{-\pi/3}$", r"Separates as $\frac{dv}{1+v^2} = +\frac{dy}{y}$, so $\tan^{-1}v = \log_e y = -\frac{\pi}{3}$."),
   (r"$\sqrt{3}$", r"Finds $\frac{x}{y} = \sqrt{3}$ and reports it as $x$."),
   (r"$\frac{e^{-\pi/3}}{\sqrt{3}}$", r"Finds $\tan^{-1}v = \frac{\pi}{3}$ but back-substitutes as $\frac{y}{x} = \sqrt{3}$.")],
  r"Here $\frac{dx}{dy} = -\frac{x^2 - xy + y^2}{y^2}$. Put $x = vy$: $v + y\frac{dv}{dy} = -(v^2 - v + 1)$, so $y\frac{dv}{dy} = -(1 + v^2)$ and $\tan^{-1}v = -\log_e y + c$, with $c = 0$ from $(0, 1)$. At $y = e^{-\pi/3}$: $\tan^{-1}v = \frac{\pi}{3}$, so $v = \sqrt{3}$ and $x = \sqrt{3}\,e^{-\pi/3}$.",
  r"Using $y = vx$ where $x = 0$ at the initial point makes $\frac{y}{x}$ undefined; $x = vy$ is the right choice.",
  "U09-B-xvy-ps", "Choosing $x = vy$ because the initial point has $x = 0$, then sign care.",
  check=_c046, source_class="XII", values=[sqrt(3)*exp(-pi/3), -sqrt(3)*exp(-pi/3), sqrt(3), exp(-pi/3)/sqrt(3)], cognitive="Analysis")

# ---------------------------------------------------------------- 047
def _c047():
    f = (y**2 + 3*x*y)/x**2
    G = vint(Fv(f))
    K = G.subs(vp, 1) - log(1)
    x1 = sqrt(2)
    s = [r for r in solve(Eq(G, log(x1) + K), vp) if r > 0]
    return x1*s[0]
q("U09-B-047", TOP_PS, "Partial fractions in a particular solution", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $0 < x < \sqrt{3}$, $y > 0$, be the solution of $x^{2}\frac{dy}{dx} = y^{2} + 3xy$ with $y(1) = 1$. Then $y(\sqrt{2})$ equals",
  r"$4\sqrt{2}$",
  [(r"$4$", r"Finds $\frac{y}{x} = 4$ at $x = \sqrt{2}$ and reports it as $y$."),
   (r"$\frac{2\sqrt{2}}{5}$", r"Writes the partial fractions with the wrong sign, getting $\frac{v+2}{v} = 3x^2$, so $v = \frac{2}{5}$ at $x = \sqrt{2}$."),
   (r"$\frac{4(3 + \sqrt{2})}{7}$", r"Omits the factor $\frac{1}{2}$ in $\frac{1}{v(v+2)} = \frac{1}{2}\left(\frac{1}{v} - \frac{1}{v+2}\right)$, so $\frac{v}{v+2} = \frac{x}{3}$ and $y = \frac{2x^2}{3 - x}$.")],
  r"With $y = vx$: $x\frac{dv}{dx} = v^2 + 2v$, so $\frac{dv}{v(v+2)} = \frac{dx}{x}$ and $\frac{1}{2}\log_e\frac{v}{v+2} = \log_e x + c$, i.e. $\frac{v}{v+2} = Cx^2$. From $v(1) = 1$, $C = \frac{1}{3}$. At $x = \sqrt{2}$: $\frac{v}{v+2} = \frac{2}{3}$, so $v = 4$ and $y = 4\sqrt{2}$.",
  r"Dropping the factor $\frac{1}{2}$ in the partial fractions of $\frac{1}{v(v+2)}$.",
  "U09-B-ps-partial-fractions", "Substitution, partial fractions with a factor, constant, solving a rational equation.",
  check=_c047, source_class="XII", values=[4*sqrt(2), 4, 2*sqrt(2)/5, 4*(3 + sqrt(2))/7], cognitive="Analysis")
