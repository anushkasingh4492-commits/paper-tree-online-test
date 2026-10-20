import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
X, Y = symbols('x y', positive=True)   # used for slope comparison of solution families
x, y, t, u = symbols('x y t u')
P1, P2, P3 = symbols('p1 p2 p3')        # y', y'', y'''
UNDEF = 0                               # sentinel: degree not defined


def od(expr):
    """(order, degree) of the DE expr = 0, expr written in P1, P2, P3. Degree UNDEF if not polynomial."""
    ps = [P1, P2, P3]
    present = [p for p in ps if expr.has(p)]
    top = present[-1]
    order = ps.index(top) + 1
    e = expand(expr)
    if not e.is_polynomial(*ps):
        return (order, UNDEF)
    return (order, Poly(e, top).degree())


def slope(F):
    """Slope dy/dx implied by the family F(x, y) = C."""
    return simplify(-diff(F, X) / diff(F, Y))


def sep_family(gy, fx):
    """Family for g(y) dy = f(x) dx, computed by integration: G(y) - F(x) = C."""
    return integrate(gy, Y) - integrate(fx, X)


def curve(F, pt):
    """Value for a particular-curve option F(x, y) = 0 through pt: (slope, F at pt)."""
    return (slope(F), simplify(F.subs({X: pt[0], Y: pt[1]})))


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."
T_OD = "Order and degree"
T_VS = "Variables separable"
T_SUB = "Reducible to variables separable"
T_PS = "Particular solutions"
D1 = r"\frac{dy}{dx}"
D2 = r"\frac{d^2y}{dx^2}"
D3 = r"\frac{d^3y}{dx^3}"

# ================================================================ EASY (14)

q("U09-A-001", T_OD, "Order and degree of a polynomial DE", "Easy", "Direct concept MCQ",
  r"The order and degree of the differential equation $\left(" + D2 + r"\right)^{3} + \left(" + D1 + r"\right)^{4} + y = x$ are respectively",
  r"$2$ and $3$",
  [(r"$2$ and $4$", r"Takes the degree as the highest exponent appearing anywhere, $4$ on $\frac{dy}{dx}$, not the exponent of the highest order derivative."),
   (r"$3$ and $2$", r"Interchanges order and degree."),
   (r"$1$ and $4$", r"Picks the derivative carrying the largest exponent, $\frac{dy}{dx}$, and reads order $1$, degree $4$ from it.")],
  r"The highest order derivative present is $\frac{d^2y}{dx^2}$, so the order is $2$. The equation is a polynomial in the derivatives and the exponent of $\frac{d^2y}{dx^2}$ is $3$, so the degree is $3$.",
  r"Reading the degree from the largest exponent instead of the exponent of the highest order derivative.",
  "U09-A-od-polynomial", "Single definition applied once.",
  check=lambda: od(P2**3 + P1**4 + y - x), values=[(2, 3), (2, 4), (3, 2), (1, 4)], source_class="XII", cognitive="Recall")

def _c2():
    # y'' = (1 + y'^2)^(3/2); square both sides to clear the radical
    return od(P2**2 - (1 + P1**2)**3)[1]
q("U09-A-002", T_OD, "Degree after clearing a radical", "Easy", "Direct concept MCQ",
  r"The degree of the differential equation $" + D2 + r" = \left[1 + \left(" + D1 + r"\right)^{2}\right]^{3/2}$ is",
  r"$2$",
  [(r"$1$", r"Reads the exponent of $\frac{d^2y}{dx^2}$ before clearing the fractional power on the right side."),
   (r"$3$", r"After squaring, takes the exponent $3$ of the bracket $\left[1 + \left(\frac{dy}{dx}\right)^2\right]^3$ as the degree."),
   (r"$6$", r"Expands $\left[1 + \left(\frac{dy}{dx}\right)^2\right]^3$ and takes the highest power of $\frac{dy}{dx}$ as the degree.")],
  r"Squaring gives $\left(\frac{d^2y}{dx^2}\right)^2 = \left[1 + \left(\frac{dy}{dx}\right)^2\right]^3$, which is a polynomial in the derivatives. The highest order derivative $\frac{d^2y}{dx^2}$ appears with exponent $2$, so the degree is $2$.",
  r"Not clearing the fractional power before reading the degree.",
  "U09-A-degree-radical", "One squaring step, then the definition.",
  check=_c2, values=[2, 1, 3, 6], source_class="XII", cognitive="Understanding")

q("U09-A-003", T_OD, "Degree not defined", "Easy", "Direct concept MCQ",
  r"For the differential equation $" + D3 + r" + x\sin\left(" + D1 + r"\right) = 0$, which of the following is correct?",
  r"Order $3$, degree not defined",
  [(r"Order $3$, degree $1$", r"Reads the exponent of $\frac{d^3y}{dx^3}$ without checking that the equation is a polynomial in all the derivatives."),
   (r"Order $1$, degree not defined", r"Takes the order from the derivative inside the sine."),
   (r"Order $3$, degree $3$", r"Copies the order into the degree.")],
  r"The highest derivative is $\frac{d^3y}{dx^3}$, so the order is $3$. Because $\frac{dy}{dx}$ occurs inside $\sin$, the equation is not a polynomial in the derivatives, so its degree is not defined.",
  r"Assigning a degree to an equation that is not a polynomial in its derivatives.",
  "U09-A-degree-undefined", "Recognising a non-polynomial term in one look.",
  check=lambda: od(P3 + x*sin(P1)), values=[(3, UNDEF), (3, 1), (1, UNDEF), (3, 3)], source_class="XII", cognitive="Understanding")

q("U09-A-004", T_OD, "Degree after clearing a fraction", "Easy", "Direct concept MCQ",
  r"The order and degree of the differential equation $y = x" + D1 + r" + \dfrac{2}{\,dy/dx\,}$ are respectively",
  r"$1$ and $2$",
  [(r"$1$ and $1$", r"Reads the exponent of $\frac{dy}{dx}$ in the term $x\frac{dy}{dx}$ without clearing the derivative from the denominator."),
   (r"$2$ and $1$", r"Interchanges order and degree."),
   (r"$1$ and $3$", r"Multiplies through by $\left(\frac{dy}{dx}\right)^2$ instead of $\frac{dy}{dx}$, getting a cubic in $\frac{dy}{dx}$.")],
  r"Multiplying by $\frac{dy}{dx}$ gives $y\frac{dy}{dx} = x\left(\frac{dy}{dx}\right)^2 + 2$, a polynomial in $\frac{dy}{dx}$. The order is $1$ and the highest power of $\frac{dy}{dx}$ is $2$, so the degree is $2$.",
  r"Reading the degree before clearing derivatives from denominators.",
  "U09-A-degree-clear-fraction", "One clearing step, then the definition.",
  check=lambda: od(expand(P1*(y - x*P1) - 2)), values=[(1, 2), (1, 1), (2, 1), (1, 3)], source_class="XII", cognitive="Understanding")

def _c5():
    return slope(sep_family(exp(Y), exp(X)))   # e^y dy = e^x dx
q("U09-A-005", T_VS, "General solution, exponential", "Easy", "Single-step computation MCQ",
  r"The general solution of the differential equation $" + D1 + r" = e^{x-y}$ is (where $C$ is an arbitrary constant)",
  r"$e^{y} = e^{x} + C$",
  [(r"$e^{y} + e^{-x} = C$", r"Writes $e^{x-y}$ as $e^{-x}e^{-y}$, a sign slip in the exponent, and separates $e^{y}\,dy = e^{-x}\,dx$."),
   (r"$e^{-y} + e^{x} = C$", r"Treats $e^{x-y}$ as $e^{x}e^{y}$ and separates $e^{-y}\,dy = e^{x}\,dx$."),
   (r"$y = e^{x} + C$", r"Integrates $e^{x}$ but leaves out the factor $e^{-y}$, solving $\frac{dy}{dx} = e^{x}$.")],
  r"Write $\frac{dy}{dx} = e^{x}e^{-y}$, so $e^{y}\,dy = e^{x}\,dx$. Integrating, $e^{y} = e^{x} + C$.",
  r"Splitting $e^{x-y}$ with the wrong sign on one exponent.",
  "U09-A-vs-exponential", "One separation and two standard integrals.",
  check=_c5,
  values=[slope(exp(Y) - exp(X)), slope(exp(Y) + exp(-X)), slope(exp(-Y) + exp(X)), slope(Y - exp(X))],
  source_class="XII", cognitive="Application")

def _c6():
    return slope(sep_family((1 - Y)/Y, -(1 + X)/X))   # (1-y)/y dy = -(1+x)/x dx
q("U09-A-006", T_VS, "General solution with logarithms", "Easy", "Single-step computation MCQ",
  r"The general solution of $(1+x)\,y\,dx + (1-y)\,x\,dy = 0$, for $x > 0$, $y > 0$, is",
  r"$\log_e (xy) + x - y = C$",
  [(r"$\log_e (xy) - x + y = C$", r"Integrates $\frac{1+x}{x}$ as $\log_e x - x$ and $\frac{1-y}{y}$ as $\log_e y + y$, slipping the sign on both linear terms."),
   (r"$\log_e (xy) + x + y = C$", r"Integrates $\frac{1-y}{y}$ as $\log_e y + y$, losing the minus sign of the $y$ term."),
   (r"$\log_e \frac{x}{y} + x - y = C$", r"Integrates $\frac{1}{y}$ as $-\log_e y$.")],
  r"Divide by $xy$: $\frac{1+x}{x}\,dx + \frac{1-y}{y}\,dy = 0$. Integrating, $\log_e x + x + \log_e y - y = C$, that is $\log_e(xy) + x - y = C$.",
  r"Sign slips when integrating $\frac{1-y}{y} = \frac{1}{y} - 1$.",
  "U09-A-vs-log-family", "Divide by $xy$, split two fractions, integrate.",
  check=_c6,
  values=[slope(log(X*Y) + X - Y), slope(log(X*Y) - X + Y), slope(log(X*Y) + X + Y), slope(log(X/Y) + X - Y)],
  source_class="XII", cognitive="Application")

def _c7():
    return slope(sep_family(1/sqrt(1 - Y**2), -1/sqrt(1 - X**2)))
q("U09-A-007", T_VS, "Inverse trigonometric family", "Easy", "Single-step computation MCQ",
  r"For $|x| < 1$, $|y| < 1$, the general solution of $" + D1 + r" + \sqrt{\dfrac{1-y^2}{1-x^2}} = 0$ is",
  r"$\sin^{-1} x + \sin^{-1} y = C$",
  [(r"$\sin^{-1} y - \sin^{-1} x = C$", r"Drops the minus sign when moving the second term across, solving $\frac{dy}{dx} = \sqrt{\frac{1-y^2}{1-x^2}}$."),
   (r"$\tan^{-1} x + \tan^{-1} y = C$", r"Uses $\int \frac{dt}{1+t^2}$ in place of $\int \frac{dt}{\sqrt{1-t^2}}$."),
   (r"$\sqrt{1-x^2} + \sqrt{1-y^2} = C$", r"Treats $\int \frac{dt}{\sqrt{1-t^2}}$ as $\sqrt{1-t^2}$.")],
  r"Separating, $\frac{dy}{\sqrt{1-y^2}} = -\frac{dx}{\sqrt{1-x^2}}$. Integrating, $\sin^{-1} y = -\sin^{-1} x + C$, so $\sin^{-1} x + \sin^{-1} y = C$.",
  r"Using the wrong standard integral for $\frac{1}{\sqrt{1-t^2}}$.",
  "U09-A-vs-inverse-sine", "One separation and a standard integral.",
  check=_c7,
  values=[slope(asin(X) + asin(Y)), slope(asin(Y) - asin(X)), slope(atan(X) + atan(Y)), slope(sqrt(1 - X**2) + sqrt(1 - Y**2))],
  source_class="XII", cognitive="Application")

def _c8():
    C = symbols('C')
    F = integrate(1/y, y) - integrate(2*x, x)          # log y - x^2 = C
    c0 = F.subs({x: 0, y: 3})
    sol = solve(Eq(F, c0), y)
    return simplify(sol[0].subs(x, 1))
q("U09-A-008", T_PS, "Particular solution, exponential growth in x squared", "Easy", "Single-step computation MCQ",
  r"If $y = y(x)$ satisfies $" + D1 + r" = 2xy$ and $y(0) = 3$, then $y(1)$ equals",
  r"$3e$",
  [(r"$e + 2$", r"Writes the general solution as $y = e^{x^2} + C$, adding the constant after exponentiating."),
   (r"$e^{4}$", r"Writes $y = e^{x^2 + 3}$, using the initial value $3$ as the constant in the exponent."),
   (r"$3\sqrt{e}$", r"Integrates $2x$ as $\frac{x^2}{2}$, getting $y = 3e^{x^2/2}$.")],
  r"$\frac{dy}{y} = 2x\,dx$ gives $\log_e |y| = x^2 + c$, so $y = Ae^{x^2}$. From $y(0) = 3$, $A = 3$, so $y = 3e^{x^2}$ and $y(1) = 3e$.",
  r"Converting $\log_e y = x^2 + c$ into $y = e^{x^2} + c$.",
  "U09-A-ps-exp-square", "Separate, integrate, fix the constant.",
  check=_c8, values=[3*E, E + 2, exp(4), 3*sqrt(E)], source_class="XII", cognitive="Application")

def _c9():
    F = integrate(y, y) - integrate(x, x)
    c0 = F.subs({x: 1, y: 2})
    sols = [s for s in solve(Eq(F.subs(x, 3), c0), y) if s > 0]
    return sols[0]
q("U09-A-009", T_PS, "Particular solution, hyperbola", "Easy", "Single-step computation MCQ",
  r"Let $y = y(x)$, with $y > 0$, satisfy $y" + D1 + r" = x$ and $y(1) = 2$. Then $y(3)$ equals",
  r"$2\sqrt{3}$",
  [(r"$2\sqrt{5}$", r"Integrates $y\,dy$ as $\frac{y^2}{2}$ but $x\,dx$ as $x^2$, getting $y^2 = 2x^2 + 2$."),
   (r"$6$", r"Drops the factor $y$ and solves $\frac{dy}{dx} = x$, getting $y = \frac{x^2}{2} + \frac{3}{2}$."),
   (r"$\sqrt{14}$", r"From $y^2 = x^2 + C$, computes $C = 4 + 1 = 5$ with a sign slip.")],
  r"$y\,dy = x\,dx$ gives $y^2 = x^2 + C$. With $y(1) = 2$, $C = 4 - 1 = 3$, so $y^2 = x^2 + 3$ and $y(3) = \sqrt{12} = 2\sqrt{3}$.",
  r"Losing the factor $\frac{1}{2}$ on one side only.",
  "U09-A-ps-hyperbola", "Separate, integrate, substitute.",
  check=_c9, values=[2*sqrt(3), 2*sqrt(5), 6, sqrt(14)], source_class="XII", cognitive="Application")

def _c10():
    F = integrate(y/(1 + y**2), y) - integrate(x/(1 + x**2), x)
    c0 = F.subs({x: 0, y: 1})
    sols = [s for s in solve(Eq(F.subs(x, 2), c0), y) if s.is_positive]
    return simplify(sols[0])
q("U09-A-010", T_PS, "Particular solution with logarithmic integrals", "Easy", "Single-step computation MCQ",
  r"Let $y = y(x)$, with $y > 0$, be the solution of $" + D1 + r" = \dfrac{x(1+y^2)}{y(1+x^2)}$ with $y(0) = 1$. Then $y(2)$ equals",
  r"$3$",
  [(r"$\sqrt{5}$", r"Writes $\log_e(1+y^2) = \log_e(1+x^2) + c$ as $1 + y^2 = 1 + x^2 + c$, adding the constant instead of multiplying."),
   (r"$\sqrt{10}$", r"From $1 + y^2 = 2(1+x^2)$, drops the $1$ on the left and takes $y^2 = 2(1 + x^2)$."),
   (r"$9$", r"Finds $y^2 = 9$ and reports $y^2$ instead of $y$.")],
  r"$\frac{y\,dy}{1+y^2} = \frac{x\,dx}{1+x^2}$ gives $\frac{1}{2}\log_e(1+y^2) = \frac{1}{2}\log_e(1+x^2) + c$, so $1 + y^2 = k(1+x^2)$. From $y(0) = 1$, $k = 2$. At $x = 2$, $1 + y^2 = 10$, so $y = 3$.",
  r"Turning a logarithmic constant into an additive one.",
  "U09-A-ps-log-ratio", "Two log integrals and a multiplicative constant.",
  check=_c10, values=[3, sqrt(5), sqrt(10), 9], source_class="XII", cognitive="Application",
  numerical=dict(question=r"Let $y = y(x)$, with $y > 0$, be the solution of $\frac{dy}{dx} = \dfrac{x(1+y^2)}{y(1+x^2)}$ with $y(0) = 1$. Then $y(2)$ is", answer=3))

def _c11():
    k, T = symbols('k T', positive=True)
    kk = solve(Eq(exp(k*10), 2), k)[0]       # P = P0 e^{kt}, doubles in 10 years
    return solve(Eq(exp(kk*T), 8), T)[0]
q("U09-A-011", T_PS, "Exponential growth", "Easy", "Single-step computation MCQ",
  r"A population grows at a rate proportional to its current size, that is $\frac{dP}{dt} = kP$ for a constant $k > 0$. If the population doubles in $10$ years, then the number of years in which it becomes $8$ times its initial size is",
  r"$30$",
  [(r"$80$", r"Assumes the time is proportional to the growth factor: $8$ times needs $8 \times 10$ years."),
   (r"$70$", r"Treats the growth as linear, adding the initial size every $10$ years, so $7$ additions are needed."),
   (r"$40$", r"Counts the stages $1, 2, 4, 8$ as four doubling periods instead of three.")],
  r"$\frac{dP}{P} = k\,dt$ gives $P = P_0 e^{kt}$. From $e^{10k} = 2$, $P = P_0\,2^{t/10}$. Setting $2^{t/10} = 8 = 2^3$ gives $t = 30$ years.",
  r"Treating exponential growth as linear in the factor.",
  "U09-A-app-growth", "Separate, then use the doubling condition once.",
  check=_c11, values=[30, 80, 70, 40], source_class="XII", cognitive="Application",
  numerical=dict(question=r"A population grows according to $\frac{dP}{dt} = kP$, $k > 0$. If the population doubles in $10$ years, the number of years in which it becomes $8$ times its initial size is", answer=30))

def _c12():
    F = integrate(y, y) - integrate(exp(x)/(1 + exp(x)), x)
    c0 = F.subs({x: 0, y: 1})
    Y2 = symbols('Y2')
    expr = solve(Eq(F.subs(y**2, Y2), c0), Y2)[0]
    return simplify(expand_log(expr.subs(x, log(3)), force=True))
q("U09-A-012", T_PS, "Particular solution with a logarithmic integral", "Easy", "Single-step computation MCQ",
  r"Let $y = y(x)$ satisfy $(1 + e^{x})\,y\," + D1 + r" = e^{x}$ with $y(0) = 1$. Then the value of $y^2$ at $x = \log_e 3$ is",
  r"$1 + 2\log_e 2$",
  [(r"$1 + \log_e 2$", r"Integrates $y\,dy$ as $y^2$ instead of $\frac{y^2}{2}$."),
   (r"$4\log_e 2$", r"Takes the constant of integration as $0$, ignoring $y(0) = 1$, so $y^2 = 2\log_e(1 + e^{x})$."),
   (r"$1 + 4\log_e 2$", r"Finds the constant as $\frac{1}{2}$, omitting the term $\log_e 2$ that comes from $\log_e(1 + e^{0})$.")],
  r"$y\,dy = \frac{e^{x}}{1+e^{x}}\,dx$ gives $\frac{y^2}{2} = \log_e(1+e^{x}) + c$. From $y(0) = 1$, $c = \frac{1}{2} - \log_e 2$. So $y^2 = 1 + 2\log_e\frac{1+e^{x}}{2}$, and at $x = \log_e 3$, $y^2 = 1 + 2\log_e 2$.",
  r"Mishandling the constant when the initial point gives $\log_e 2$.",
  "U09-A-ps-log-integral", r"Recognise $\frac{e^x}{1+e^x}$ as $\frac{f'}{f}$, then fix the constant.",
  check=_c12, values=[1 + 2*log(2), 1 + log(2), 4*log(2), 1 + 4*log(2)], source_class="XII", cognitive="Application")

def _c13():
    # subtangent y / y' = 3  ->  dy/y = dx/3
    F = integrate(1/y, y) - integrate(Rational(1, 3), x)
    c0 = F.subs({x: 0, y: 2})
    sol = solve(Eq(F, c0), y)[0]
    return simplify(sol.subs(x, 3))
q("U09-A-013", T_PS, "Curve with constant subtangent", "Easy", "Single-step computation MCQ",
  r"A curve $y = f(x)$, with $f(x) > 0$, passes through $(0, 2)$, and at every point $(x, y)$ on it the subtangent $\dfrac{y}{dy/dx}$ equals $3$. Then $f(3)$ equals",
  r"$2e$",
  [(r"$2e^{9}$", r"Writes the condition as $\frac{dy}{dx} = 3y$, inverting the ratio."),
   (r"$11$", r"Writes the condition as $\frac{dy}{dx} = 3$, taking the subtangent as the slope."),
   (r"$e + 1$", r"Writes the solution as $y = e^{x/3} + C$, adding the constant after exponentiating.")],
  r"$\frac{y}{dy/dx} = 3$ gives $\frac{dy}{y} = \frac{dx}{3}$, so $y = Ae^{x/3}$. Through $(0, 2)$, $A = 2$. Hence $f(3) = 2e$.",
  r"Inverting the subtangent ratio.",
  "U09-A-app-subtangent", "Translate the condition, separate, fix the constant.",
  check=_c13, values=[2*E, 2*exp(9), 11, E + 1], source_class="XII", cognitive="Application")

def _c14():
    F = integrate(exp(y), y) - integrate(2*x + 1, x)
    c0 = F.subs({x: 0, y: 0})
    xs = solve(Eq(F.subs(y, 0), c0), x)
    return [r for r in xs if r != 0][0]
q("U09-A-014", T_PS, "Particular curve meeting the x-axis", "Easy", "Single-step computation MCQ",
  r"The solution curve of $" + D1 + r" = (2x + 1)e^{-y}$ passing through the origin meets the $x$-axis again at $x =$",
  r"$-1$",
  [(r"$1$", r"Integrates $2x + 1$ as $x^2 - x$, a sign slip, getting $e^{y} = x^2 - x + 1$."),
   (r"$\frac{-1 + \sqrt{5}}{2}$", r"Drops the constant of integration, taking $e^{y} = x^2 + x$, and solves $x^2 + x = 1$."),
   (r"$\frac{-1 - \sqrt{5}}{2}$", r"Drops the constant of integration, taking $e^{y} = x^2 + x$, and picks the other root of $x^2 + x = 1$.")],
  r"$e^{y}\,dy = (2x+1)\,dx$ gives $e^{y} = x^2 + x + C$. Through $(0, 0)$, $C = 1$. On the $x$-axis $y = 0$, so $x^2 + x + 1 = 1$, giving $x = 0$ or $x = -1$. The other point is $x = -1$.",
  r"Forgetting the constant fixed by the given point.",
  "U09-A-ps-x-intercept", "Separate, fix the constant, solve a quadratic.",
  check=_c14, values=[-1, 1, (-1 + sqrt(5))/2, (-1 - sqrt(5))/2], source_class="XII", cognitive="Application")

# ================================================================ MEDIUM (21)

def _c15():
    # (y'')^(2/3) = (1 + y')^(1/2): raise to the power 6
    o, d = od(P2**4 - (1 + P1)**3)
    return o + d
q("U09-A-015", T_OD, "Order plus degree with fractional powers", "Medium", "Multi-step computation MCQ",
  r"If $m$ and $n$ are the order and degree of the differential equation $\left(" + D2 + r"\right)^{2/3} = \left(1 + " + D1 + r"\right)^{1/2}$, then $m + n$ equals",
  r"$6$",
  [(r"$4$", r"Cubes both sides only, reaching $\left(\frac{d^2y}{dx^2}\right)^2 = \left(1 + \frac{dy}{dx}\right)^{3/2}$, and reads degree $2$ while a fractional power remains."),
   (r"$5$", r"After clearing powers, takes the exponent $3$ of $\left(1 + \frac{dy}{dx}\right)$ as the degree."),
   (r"$8$", r"Takes the LCM $6$ of the denominators $3$ and $2$ as the degree.")],
  r"Raise both sides to the power $6$: $\left(\frac{d^2y}{dx^2}\right)^4 = \left(1 + \frac{dy}{dx}\right)^3$, a polynomial in the derivatives. The order is $m = 2$ and the degree is $n = 4$, so $m + n = 6$.",
  r"Reading the degree before every fractional power has been cleared.",
  "U09-A-order-plus-degree", "Two-stage clearing of fractional powers, then the definition.",
  check=_c15, values=[6, 4, 5, 8], source_class="XII", cognitive="Understanding",
  numerical=dict(question=r"If $m$ and $n$ are the order and degree of the differential equation $\left(\frac{d^2y}{dx^2}\right)^{2/3} = \left(1 + \frac{dy}{dx}\right)^{1/2}$, then $m + n$ is", answer=6))

def _c16():
    s1 = od(P2 + sin(y))[1] == 1
    s2 = od(P1 + log(P1) - x)[1] == 1
    return (s1, s2)
q("U09-A-016", T_OD, "Degree when a function of y appears", "Medium", "Statement-based MCQ",
  r"Statement I: The degree of the differential equation $" + D2 + r" + \sin y = 0$ is $1$. Statement II: The degree of the differential equation $" + D1 + r" + \log_e\left(" + D1 + r"\right) = x$ is $1$." + STEM_TAIL,
  ST_TF,
  [(ST_FF, r"Believes that $\sin y$ also makes the degree undefined, not seeing that only functions of the derivatives matter."),
   (ST_TT, r"Reads the exponent $1$ on $\frac{dy}{dx}$ in Statement II, ignoring the logarithm of the derivative."),
   (ST_FT, r"Swaps the two judgements: rejects the equation with $\sin y$ and accepts the one with $\log_e\left(\frac{dy}{dx}\right)$.")],
  r"In Statement I the equation is a polynomial in the derivatives ($\sin y$ is a function of $y$, not of a derivative), and $\frac{d^2y}{dx^2}$ has exponent $1$, so the degree is $1$; it is true. In Statement II the derivative appears inside $\log_e$, so the equation is not a polynomial in $\frac{dy}{dx}$ and its degree is not defined; it is false.",
  r"Thinking any transcendental function anywhere makes the degree undefined.",
  "U09-A-degree-statements", "Two separate checks of polynomial form.",
  check=_c16, values=[(True, False), (False, False), (True, True), (False, True)], source_class="XII", cognitive="Understanding")

def _c17():
    # key: y'' = sqrt(y + y'^2) -> square
    return od(P2**2 - (y + P1**2))[1]
q("U09-A-017", T_OD, "Identify the equation of degree 2", "Medium", "Conceptual/application MCQ",
  r"Which of the following differential equations has degree $2$?",
  r"$" + D2 + r" = \sqrt{y + \left(" + D1 + r"\right)^{2}}$",
  [(r"$\left(" + D2 + r"\right)^{2} + \cos\left(" + D1 + r"\right) = 0$", r"Sees the square on $\frac{d^2y}{dx^2}$ but misses that $\cos\left(\frac{dy}{dx}\right)$ makes the degree undefined."),
   (r"$\sqrt[3]{" + D3 + r"} = \left(" + D1 + r"\right)^{2}$", r"Reads the exponent $2$ on $\frac{dy}{dx}$; cubing gives $\frac{d^3y}{dx^3} = \left(\frac{dy}{dx}\right)^6$, of degree $1$."),
   (r"$\left(" + D2 + r"\right)^{3} = \left(" + D1 + r"\right)^{2} + y$", r"Takes the exponent of $\frac{dy}{dx}$ as the degree; the highest derivative has exponent $3$.")],
  r"Squaring $\frac{d^2y}{dx^2} = \sqrt{y + \left(\frac{dy}{dx}\right)^2}$ gives $\left(\frac{d^2y}{dx^2}\right)^2 = y + \left(\frac{dy}{dx}\right)^2$, so its degree is $2$. The equation with $\cos\left(\frac{dy}{dx}\right)$ has no degree, the cube root one becomes $\frac{d^3y}{dx^3} = \left(\frac{dy}{dx}\right)^6$ of degree $1$, and $\left(\frac{d^2y}{dx^2}\right)^{3} = \left(\frac{dy}{dx}\right)^{2} + y$ has degree $3$.",
  r"Taking the degree from a lower order derivative.",
  "U09-A-degree-identify", "Four equations, each needing a separate check.",
  check=_c17, values=[2, UNDEF, od(P3 - P1**6)[1], od(P2**3 - P1**2 - y)[1]], source_class="XII", cognitive="Analysis")

def _c18():
    # sqrt(1 + y2) = y1^3 + y  ->  square both sides; the radical sat on the highest derivative
    return od(1 + P2 - (P1**3 + y)**2)
q("U09-A-018", T_OD, "Radical over the highest derivative", "Medium", "Conceptual/application MCQ",
  r"The order and degree of the differential equation $\sqrt{1 + " + D2 + r"} = \left(" + D1 + r"\right)^{3} + y$ are respectively",
  r"$2$ and $1$",
  [(r"$2$ and $2$", r"Squares both sides and takes the degree as $2$, as though the square fell on $\frac{d^2y}{dx^2}$ rather than on the right side."),
   (r"$2$ and $6$", r"After squaring, takes the highest power appearing anywhere, $\left(\frac{dy}{dx}\right)^{6}$, as the degree."),
   (r"$1$ and $6$", r"After squaring, reads both order and degree from the term $\left(\frac{dy}{dx}\right)^{6}$.")],
  r"Squaring both sides gives $1 + \frac{d^2y}{dx^2} = \left(\left(\frac{dy}{dx}\right)^{3} + y\right)^{2}$, which is a polynomial in the derivatives. The highest derivative is $\frac{d^2y}{dx^2}$, so the order is $2$, and it now appears to the first power, so the degree is $1$. The powers of $\frac{dy}{dx}$ do not affect the degree.",
  r"Assuming that clearing a radical always raises the degree, or reading the degree from a lower order derivative.",
  "U09-A-degree-radical-on-highest", r"One squaring step with a trap: the square lands on the lower order side, so the degree stays $1$.",
  check=_c18, values=[(2, 1), (2, 2), (2, 6), (1, 6)], source_class="XII", cognitive="Understanding")

def _c19():
    return slope(sep_family(1/(1 + Y**2), 1/(1 + X**2)))
q("U09-A-019", T_VS, "Inverse tangent family in algebraic form", "Medium", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = \dfrac{1 + y^2}{1 + x^2}$ can be written as ($C$ an arbitrary constant)",
  r"$y - x = C(1 + xy)$",
  [(r"$y + x = C(1 - xy)$", r"Writes $\tan^{-1} y + \tan^{-1} x = c$, a sign slip when separating."),
   (r"$y - x = C(1 - xy)$", r"Uses $1 - xy$ in the denominator of $\tan(\alpha - \beta)$, the formula for $\tan(\alpha + \beta)$."),
   (r"$y + x = C(1 + xy)$", r"Combines $\tan^{-1} y - \tan^{-1} x$ with the numerator of $\tan(\alpha + \beta)$ and the denominator of $\tan(\alpha - \beta)$.")],
  r"Separating, $\frac{dy}{1+y^2} = \frac{dx}{1+x^2}$, so $\tan^{-1} y - \tan^{-1} x = c$. Taking tangent, $\frac{y - x}{1 + xy} = \tan c = C$, that is $y - x = C(1 + xy)$.",
  r"Mixing up the $\tan(\alpha \pm \beta)$ formulas.",
  "U09-A-vs-tan-inverse-algebraic", "Separation, then a trigonometric identity to rewrite.",
  check=_c19,
  values=[slope((Y - X)/(1 + X*Y)), slope((Y + X)/(1 - X*Y)), slope((Y - X)/(1 - X*Y)), slope((Y + X)/(1 + X*Y))],
  source_class="XII", cognitive="Application")

def _c20():
    return slope(sep_family(1 + cos(2*Y), 1 - cos(2*X)))
q("U09-A-020", T_VS, "Trigonometric separable equation", "Medium", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = \dfrac{1 - \cos 2x}{1 + \cos 2y}$ is",
  r"$2(y - x) + \sin 2y + \sin 2x = C$",
  [(r"$2(y - x) + \sin 2y - \sin 2x = C$", r"Integrates $-\cos 2x$ as $-\frac{\sin 2x}{2}$ but then moves it across without changing sign."),
   (r"$2(y + x) + \sin 2y + \sin 2x = C$", r"Integrates $1 - \cos 2x$ as $-x - \frac{\sin 2x}{2}$, a sign slip on the constant term."),
   (r"$y - x + \sin 2y + \sin 2x = C$", r"Integrates $\cos 2t$ as $\sin 2t$, dropping the factor $\frac{1}{2}$.")],
  r"$(1 + \cos 2y)\,dy = (1 - \cos 2x)\,dx$ gives $y + \frac{\sin 2y}{2} = x - \frac{\sin 2x}{2} + c$. Multiplying by $2$: $2(y - x) + \sin 2y + \sin 2x = C$.",
  r"Dropping the factor $\frac{1}{2}$ in $\int \cos 2t\,dt$.",
  "U09-A-vs-trig-double-angle", "Separation and two trigonometric integrals with careful signs.",
  check=_c20,
  values=[slope(2*(Y - X) + sin(2*Y) + sin(2*X)), slope(2*(Y - X) + sin(2*Y) - sin(2*X)),
          slope(2*(Y + X) + sin(2*Y) + sin(2*X)), slope(Y - X + sin(2*Y) + sin(2*X))],
  source_class="XII", cognitive="Application")

def _c21():
    return slope(sep_family(exp(-Y), exp(X) + X**2))
q("U09-A-021", T_VS, "Factorising before separating", "Medium", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = e^{x+y} + x^{2}e^{y}$ is",
  r"$e^{x} + e^{-y} + \frac{x^{3}}{3} = C$",
  [(r"$e^{x} - e^{-y} + \frac{x^{3}}{3} = C$", r"Integrates $e^{-y}$ as $e^{-y}$, losing the minus sign."),
   (r"$e^{x} + e^{-y} - \frac{x^{3}}{3} = C$", r"Moves $\frac{x^3}{3}$ to the other side without changing its sign."),
   (r"$e^{x} - e^{y} + \frac{x^{3}}{3} = C$", r"Separates as $e^{y}\,dy = (e^{x} + x^2)\,dx$, multiplying by $e^{y}$ instead of dividing.")],
  r"Factor: $\frac{dy}{dx} = e^{y}(e^{x} + x^2)$, so $e^{-y}\,dy = (e^{x} + x^2)\,dx$. Integrating, $-e^{-y} = e^{x} + \frac{x^3}{3} + c$, that is $e^{x} + e^{-y} + \frac{x^3}{3} = C$.",
  r"Losing the sign in $\int e^{-y}\,dy = -e^{-y}$.",
  "U09-A-vs-factorise-first", "Factorise to separate, then integrate with sign care.",
  check=_c21,
  values=[slope(exp(X) + exp(-Y) + X**3/3), slope(exp(X) - exp(-Y) + X**3/3),
          slope(exp(X) + exp(-Y) - X**3/3), slope(exp(X) - exp(Y) + X**3/3)],
  source_class="XII", cognitive="Application")

def _c22():
    F = integrate(1/(Y*log(Y)), Y) - integrate(1/X, X)   # log(log y) - log x
    c0 = simplify(F.subs({X: 2, Y: E}))
    sol = solve(Eq(F.subs(X, 6), c0), Y)
    return simplify(sol[0])
q("U09-A-022", T_PS, "Double logarithm", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, $y > 1$, satisfy $x" + D1 + r" = y\log_e y$ and $y(2) = e$. Then $y(6)$ equals",
  r"$e^{3}$",
  [(r"$e^{5}$", r"After $\log_e(\log_e y) = \log_e x + c$, exponentiates as $\log_e y = x + c$, getting $\log_e y = x - 1$."),
   (r"$3e$", r"Drops the factor $\log_e y$ and solves $x\frac{dy}{dx} = y$, getting $y = \frac{ex}{2}$."),
   (r"$e^{12}$", r"Gets $c = \log_e 2$ instead of $-\log_e 2$, so $\log_e y = 2x$.")],
  r"$\frac{dy}{y\log_e y} = \frac{dx}{x}$ gives $\log_e(\log_e y) = \log_e x + c$, so $\log_e y = kx$. From $y(2) = e$, $k = \frac{1}{2}$. Then $\log_e y(6) = 3$, so $y(6) = e^{3}$.",
  r"Integrating $\frac{1}{y\log_e y}$ incorrectly or mishandling the constant.",
  "U09-A-ps-double-log", "Substitution inside the integral, then a multiplicative constant.",
  check=_c22, values=[exp(3), exp(5), 3*E, exp(12)], source_class="XII", cognitive="Application")

def _c23():
    F = integrate(1/(y**2 - y), y) - integrate(1/x, x)
    F = simplify(expand_log(F, force=True))
    c0 = F.subs({x: 1, y: 2})
    sols = solve(Eq(F.subs(x, Rational(3, 2)), c0), y)
    return [s for s in sols if s > 1][0]
q("U09-A-023", T_PS, "Partial fractions in y", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$ be the solution of $" + D1 + r" = \dfrac{y^2 - y}{x}$, $0 < x < 2$, with $y(1) = 2$. Then $y\left(\frac{3}{2}\right)$ equals",
  r"$4$",
  [(r"$\frac{3}{2}$", r"Writes $\frac{1}{y(y-1)} = \frac{1}{y} - \frac{1}{y-1}$, a sign slip, getting $\frac{y}{y-1} = 2x$."),
   (r"$\frac{7}{4}$", r"Reaches $\frac{y-1}{y} = \frac{x}{2}$ but solves it as $y = 1 + \frac{x}{2}$, ignoring the $y$ in the denominator."),
   (r"$\frac{1 + \sqrt{13}}{2}$", r"Integrates $\frac{1}{y(y-1)}$ as $\log_e|y(y-1)|$, getting $y^2 - y = 2x$.")],
  r"$\frac{dy}{y(y-1)} = \frac{dx}{x}$ and $\frac{1}{y(y-1)} = \frac{1}{y-1} - \frac{1}{y}$, so $\log_e\left|\frac{y-1}{y}\right| = \log_e x + c$, giving $\frac{y-1}{y} = kx$. From $y(1) = 2$, $k = \frac{1}{2}$. So $y = \frac{2}{2 - x}$ and $y\left(\frac{3}{2}\right) = 4$.",
  r"Sign error in partial fractions.",
  "U09-A-ps-partial-fraction-y", "Partial fractions, constant, then solving for $y$.",
  check=_c23, values=[4, Rational(3, 2), Rational(7, 4), (1 + sqrt(13))/2], source_class="XII", cognitive="Application",
  numerical=dict(question=r"Let $y = y(x)$ be the solution of $\frac{dy}{dx} = \dfrac{y^2 - y}{x}$, $0 < x < 2$, with $y(1) = 2$. Then $y\left(\frac{3}{2}\right)$ is", answer=4))

def _c24():
    F = integrate(2**(-y), y) - integrate(2**x, x)
    c0 = F.subs({x: 0, y: 0})
    sol = solve(Eq(F.subs(x, -1), c0), y)
    return simplify(sol[0])
q("U09-A-024", T_PS, "Exponential with base 2", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$ satisfy $" + D1 + r" = 2^{x+y}$ with $y(0) = 0$. Then $y(-1)$ equals",
  r"$\log_2 \frac{2}{3}$",
  [(r"$\log_2 \frac{3}{2}$", r"Reaches $2^{-y} = \frac{3}{2}$ but solves it as $y = \log_2 \frac{3}{2}$, forgetting the minus sign."),
   (r"$1$", r"Integrates $2^{-y}$ as $+\frac{2^{-y}}{\log_e 2}$, losing the minus sign, so $2^{x} - 2^{-y} = C$ with $C = 0$, giving $y = -x$."),
   (r"$-1$", r"Separates as $2^{y}\,dy = 2^{x}\,dx$, multiplying instead of dividing, so $y = x$.")],
  r"$2^{-y}\,dy = 2^{x}\,dx$ gives $-\frac{2^{-y}}{\log_e 2} = \frac{2^{x}}{\log_e 2} + c$, so $2^{x} + 2^{-y} = K$. From $y(0) = 0$, $K = 2$. At $x = -1$, $2^{-y} = 2 - \frac{1}{2} = \frac{3}{2}$, so $y = -\log_2\frac{3}{2} = \log_2\frac{2}{3}$.",
  r"Losing the sign of $\int 2^{-y}\,dy$.",
  "U09-A-ps-base-two", "Separate exponentials, constant, then a logarithm.",
  check=_c24, values=[log(Rational(2, 3), 2), log(Rational(3, 2), 2), 1, -1], source_class="XII", cognitive="Application")

def _c25():
    k, T = symbols('k T', positive=True)
    # d(theta)/dt = -k(theta - 20): theta - 20 = 60 e^{-kt}
    kk = solve(Eq(20 + 60*exp(-10*k), 50), k)[0]
    return simplify(solve(Eq(20 + 60*exp(-kk*T), 35), T)[0])
q("U09-A-025", T_PS, "Newton's law of cooling", "Medium", "Multi-step computation MCQ",
  r"A body at $80^\circ\mathrm{C}$ is placed in a room kept at $20^\circ\mathrm{C}$. Its temperature $\theta$ obeys $\frac{d\theta}{dt} = -k(\theta - 20)$, $k > 0$, with $t$ in minutes. If the temperature falls to $50^\circ\mathrm{C}$ in $10$ minutes, then the time (in minutes, from the start) for it to reach $35^\circ\mathrm{C}$ is",
  r"$20$",
  [(r"$15$", r"Assumes a constant cooling rate of $3^\circ\mathrm{C}$ per minute, as in linear cooling."),
   (r"$30$", r"Counts the excess temperatures $60$, $30$, $15$ as three $10$-minute stages instead of two halvings, giving $30$ minutes."),
   (r"$40$", r"Notes that the excess temperature must fall by a factor of $4$ and multiplies $10$ minutes by $4$.")],
  r"$\frac{d\theta}{\theta - 20} = -k\,dt$ gives $\theta - 20 = 60e^{-kt}$. From $30 = 60e^{-10k}$, $e^{-10k} = \frac{1}{2}$, so $\theta - 20 = 60\left(\frac{1}{2}\right)^{t/10}$. Setting $\theta = 35$: $\left(\frac{1}{2}\right)^{t/10} = \frac{1}{4}$, so $t = 20$.",
  r"Treating exponential cooling as linear.",
  "U09-A-app-cooling", "Separate, use one data point, then solve an exponential equation.",
  check=_c25, values=[20, 15, 30, 40], source_class="XII", cognitive="Application",
  numerical=dict(question=r"A body at $80^\circ\mathrm{C}$ is placed in a room kept at $20^\circ\mathrm{C}$, and its temperature obeys $\frac{d\theta}{dt} = -k(\theta - 20)$, $k > 0$, with $t$ in minutes. If it cools to $50^\circ\mathrm{C}$ in $10$ minutes, the time in minutes from the start for it to reach $35^\circ\mathrm{C}$ is", answer=20))

def _c26():
    F = integrate(1/(y*(2 - y)), y) - integrate(1, x)
    c0 = F.subs({x: 0, y: 1})
    sols = solve(Eq(F.subs(x, log(2)), c0), y)
    return [simplify(s) for s in sols if 0 < s < 2][0]
q("U09-A-026", T_PS, "Logistic type equation", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, with $0 < y < 2$, satisfy $" + D1 + r" = y(2 - y)$ and $y(0) = 1$. Then $y(\log_e 2)$ equals",
  r"$\frac{8}{5}$",
  [(r"$\frac{4}{3}$", r"Uses $\frac{1}{y(2-y)} = \frac{1}{y} + \frac{1}{2-y}$ without the factor $\frac{1}{2}$, so $\frac{y}{2-y} = e^{x}$."),
   (r"$\frac{2}{5}$", r"Writes the partial-fraction integral with the overall sign reversed, $\frac{1}{2}\log_e\frac{2-y}{y} = x + c$; then $c = 0$, $\frac{2-y}{y} = e^{2x} = 4$ at $x = \log_e 2$, so $y = \frac{2}{5}$."),
   (r"$\frac{2}{3}$", r"Makes both slips: drops the factor $\frac{1}{2}$ and reverses the overall sign, getting $\frac{2-y}{y} = e^{x} = 2$, so $y = \frac{2}{3}$.")],
  r"$\frac{1}{y(2-y)} = \frac{1}{2}\left(\frac{1}{y} + \frac{1}{2-y}\right)$, so $\frac{1}{2}\log_e\frac{y}{2-y} = x + c$. From $y(0) = 1$, $c = 0$, so $\frac{y}{2-y} = e^{2x}$. At $x = \log_e 2$, $\frac{y}{2-y} = 4$, so $y = \frac{8}{5}$.",
  r"Dropping the factor $\frac{1}{2}$ in the partial fractions.",
  "U09-A-ps-logistic", "Partial fractions with a factor, constant, then solving for $y$.",
  check=_c26, values=[Rational(8, 5), Rational(4, 3), Rational(2, 5), Rational(2, 3)], source_class="XII", cognitive="Application")

def _c27():
    F = integrate(1/(1 + y**2), y) - integrate(2/(1 + x**2), x)   # (1 + x^2) dy = 2(1 + y^2) dx
    c0 = F.subs({x: 0, y: 1})
    sol = solve(Eq(F.subs(x, Rational(1, 3)), c0), y)
    return simplify(expand_trig(sol[0]))
q("U09-A-027", T_PS, "Particular solution, inverse tangent with a double angle", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $0 \le x < \sqrt{2} - 1$, be the solution of $(1 + x^2)\,dy = 2(1 + y^2)\,dx$ with $y(0) = 1$. Then $y\left(\frac{1}{3}\right)$ equals",
  r"$7$",
  [(r"$2$", r"Drops the factor $2$ when integrating, so $\tan^{-1} y = \tan^{-1} x + \frac{\pi}{4}$ and $y\left(\frac{1}{3}\right) = \frac{1 + 1/3}{1 - 1/3} = 2$."),
   (r"$5$", r"Writes $2\tan^{-1} x$ as $\tan^{-1} 2x$, so $y = \frac{1 + 2x}{1 - 2x}$, which is $5$ at $x = \frac{1}{3}$."),
   (r"$\frac{1}{7}$", r"Uses $\tan\left(\frac{\pi}{4} - \theta\right)$ in place of $\tan\left(\frac{\pi}{4} + \theta\right)$ with $\tan\theta = \frac{3}{4}$: $\frac{1 - 3/4}{1 + 3/4} = \frac{1}{7}$.")],
  r"Separating, $\frac{dy}{1 + y^2} = \frac{2\,dx}{1 + x^2}$, so $\tan^{-1} y = 2\tan^{-1} x + c$, and $y(0) = 1$ gives $c = \frac{\pi}{4}$. At $x = \frac{1}{3}$, $\tan\left(2\tan^{-1}\frac{1}{3}\right) = \frac{2/3}{1 - 1/9} = \frac{3}{4}$. Hence $y\left(\frac{1}{3}\right) = \tan\left(\theta + \frac{\pi}{4}\right)$ with $\tan\theta = \frac{3}{4}$, which is $\frac{1 + 3/4}{1 - 3/4} = 7$.",
  r"Mishandling the coefficient $2$ in front of $\tan^{-1} x$.",
  "U09-A-ps-tan-double-angle", r"Separate, fix the constant, then a double-angle and a compound-angle formula in sequence.",
  check=_c27, values=[7, 2, 5, Rational(1, 7)], source_class="XII", cognitive="Application",
  numerical=dict(question=r"Let $y = y(x)$, $0 \le x < \sqrt{2} - 1$, be the solution of $(1 + x^2)\,dy = 2(1 + y^2)\,dx$ with $y(0) = 1$. Then $y\left(\frac{1}{3}\right)$ is", answer=7))

def _c28():
    F = integrate(y, y) - integrate(4, x)       # y y' = 4
    c0 = F.subs({x: 1, y: 2})
    xv = solve(Eq(F.subs(y, 0), c0), x)[0]       # vertex of the parabola y^2 = 8x + k lies on y = 0
    return (xv, 0)
q("U09-A-028", T_PS, "Curve with constant subnormal", "Medium", "Multi-step computation MCQ",
  r"A curve passes through $(1, 2)$, and at every point $(x, y)$ on it the subnormal $y" + D1 + r"$ equals $4$. The curve is a parabola whose vertex is",
  r"$\left(\frac{1}{2}, 0\right)$",
  [(r"$\left(-\frac{1}{2}, 0\right)$", r"Finds the constant with a sign slip, getting $y^2 = 8x + 4$."),
   (r"$(0, 0)$", r"Integrates $y\,dy$ as $y^2$, getting $y^2 = 4x$, which passes through $(1, 2)$."),
   (r"$\left(\frac{1}{4}, 0\right)$", r"Gets $y^2 = 8x + 2c$ but uses $c = -1$ instead of $-2$, so $y^2 = 8x - 2$.")],
  r"$y\,dy = 4\,dx$ gives $\frac{y^2}{2} = 4x + c$. At $(1, 2)$, $2 = 4 + c$, so $c = -2$ and $y^2 = 8x - 4 = 8\left(x - \frac{1}{2}\right)$. The vertex is $\left(\frac{1}{2}, 0\right)$.",
  r"Dropping the factor $\frac{1}{2}$ in $\int y\,dy$.",
  "U09-A-app-subnormal", "Translate, separate, constant, then read the vertex.",
  check=_c28, values=[(Rational(1, 2), 0), (Rational(-1, 2), 0), (0, 0), (Rational(1, 4), 0)], source_class="XII", cognitive="Application")

def _c29():
    # normal at (x, y) passes through (1, 0):  (x - 1) + y y' = 0
    F = integrate(y, y) + integrate(x - 1, x)
    c0 = F.subs({x: 2, y: sqrt(3)})
    circ = expand(2*(F - c0))                   # x^2 - 2x + y^2 - const
    p = Poly(circ, x, y)
    a = -p.coeff_monomial(x)/2; b = -p.coeff_monomial(y)/2
    return sqrt(a**2 + b**2 - p.coeff_monomial(1))
q("U09-A-029", T_PS, "Normals through a fixed point", "Medium", "Multi-step computation MCQ",
  r"A curve passes through $(2, \sqrt{3})$, and the normal at every point of it passes through the fixed point $(1, 0)$. The curve is a circle of radius",
  r"$2$",
  [(r"$4$", r"Reaches $(x-1)^2 + y^2 = 4$ and reports the right side as the radius."),
   (r"$\sqrt{7}$", r"Takes the normals to pass through the origin, getting $x^2 + y^2 = 7$."),
   (r"$\sqrt{3}$", r"Reaches $x^2 - 2x + y^2 = 3$ and reads the radius as $\sqrt{3}$ without completing the square.")],
  r"The normal at $(x, y)$ has slope $-\frac{dx}{dy}$ and passes through $(1, 0)$, so $-\frac{1}{dy/dx} = \frac{y}{x - 1}$, that is $(x - 1) + y\frac{dy}{dx} = 0$. Integrating, $(x-1)^2 + y^2 = c$, and $(2, \sqrt{3})$ gives $c = 4$. The radius is $2$.",
  r"Reading the radius before completing the square.",
  "U09-A-app-normal-circle", "Translate the geometric condition, separate, identify the circle.",
  check=_c29, values=[2, 4, sqrt(7), sqrt(3)], source_class="XII", cognitive="Application",
  numerical=dict(question=r"A curve passes through $(2, \sqrt{3})$, and the normal at every point of it passes through $(1, 0)$. The curve is a circle; its radius is", answer=2))

def _c30():
    G = integrate(1/(1 + t**2), t)           # x + y = t, t' = 1 + t^2
    return slope(G.subs(t, X + Y) - X)
q("U09-A-030", T_SUB, "Substitution x + y = t", "Medium", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = (x + y)^{2}$ is",
  r"$\tan^{-1}(x + y) = x + C$",
  [(r"$-\dfrac{1}{x + y} = x + C$", r"With $t = x + y$, writes $\frac{dt}{dx} = t^2$, forgetting the $1$ from $\frac{d}{dx}(x) = 1$."),
   (r"$\tan^{-1}(x + y) = -x + C$", r"Separates $\frac{dt}{1 + t^2} = -dx$, a sign slip."),
   (r"$\tan^{-1}(x + y) = y + C$", r"After substituting, integrates the right side with respect to $y$ instead of $x$.")],
  r"Put $x + y = t$, so $\frac{dt}{dx} = 1 + \frac{dy}{dx} = 1 + t^2$. Then $\frac{dt}{1 + t^2} = dx$, giving $\tan^{-1} t = x + C$, that is $\tan^{-1}(x + y) = x + C$.",
  r"Forgetting the extra $1$ in $\frac{dt}{dx}$ after substitution.",
  "U09-A-sub-square", "Substitution, then a standard integral.",
  check=_c30,
  values=[slope(atan(X + Y) - X), slope(-1/(X + Y) - X), slope(atan(X + Y) + X), slope(atan(X + Y) - Y)],
  source_class="XII", cognitive="Application")

def _c31():
    G = integrate((1 - sin(t))/cos(t)**2, t)   # = 1/(1 + sin t)
    assert simplify(diff(G, t) - 1/(1 + sin(t))) == 0
    return slope(G.subs(t, X + Y) - X)
q("U09-A-031", T_SUB, "Substitution with a trigonometric right side", "Medium", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = \sin(x + y)$ is",
  r"$\tan(x + y) - \sec(x + y) = x + C$",
  [(r"$\tan(x + y) + \sec(x + y) = x + C$", r"Integrates $\frac{1 - \sin t}{\cos^2 t}$ as $\tan t + \sec t$, a sign slip on $\int \sec t \tan t\,dt$."),
   (r"$\sec(x + y) - \tan(x + y) = x + C$", r"Gets the antiderivative of $\frac{1}{1 + \sin t}$ with the opposite overall sign."),
   (r"$\log_e\left|\tan\frac{x + y}{2}\right| = x + C$", r"Writes $\frac{dt}{dx} = \sin t$, forgetting the $1$, and integrates $\csc t$.")],
  r"Put $t = x + y$: $\frac{dt}{dx} = 1 + \sin t$. Then $\int \frac{dt}{1 + \sin t} = \int \frac{1 - \sin t}{\cos^2 t}\,dt = \tan t - \sec t$. So $\tan(x + y) - \sec(x + y) = x + C$.",
  r"Sign slips when rationalising $\frac{1}{1 + \sin t}$.",
  "U09-A-sub-sine", "Substitution, rationalising, two standard integrals.",
  check=_c31,
  values=[slope(tan(X + Y) - sec(X + Y) - X), slope(tan(X + Y) + sec(X + Y) - X),
          slope(sec(X + Y) - tan(X + Y) - X), slope(log(tan((X + Y)/2)) - X)],
  source_class="XII", cognitive="Application")

def _c32():
    G = integrate((t - 1)/(2*t), t)           # t' = 2t/(t - 1)
    return slope(G.subs(t, X + Y) - X)
q("U09-A-032", T_SUB, "Substitution in a rational right side", "Medium", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = \dfrac{x + y + 1}{x + y - 1}$ (for $x + y > 0$) is",
  r"$y - x - \log_e(x + y) = C$",
  [(r"$y - x + \log_e(x + y) = C$", r"Splits $\frac{t - 1}{2t} = \frac{1}{2} + \frac{1}{2t}$, a sign slip."),
   (r"$y - 2\log_e(x + y + 1) = C$", r"Forgets the $1$ in $\frac{dt}{dx} = 1 + \frac{dy}{dx}$ and integrates $\frac{t - 1}{t + 1}$."),
   (r"$y - x - 2\log_e(x + y) = C$", r"Integrates $\frac{t - 1}{2t}$ as $\frac{t}{2} - \log_e t$, dropping the factor $\frac{1}{2}$ on the logarithm.")],
  r"Put $t = x + y$: $\frac{dt}{dx} = 1 + \frac{t + 1}{t - 1} = \frac{2t}{t - 1}$. So $\frac{t - 1}{2t}\,dt = dx$, giving $\frac{t}{2} - \frac{1}{2}\log_e t = x + c$. Then $x + y - \log_e(x + y) = 2x + 2c$, that is $y - x - \log_e(x + y) = C$.",
  r"Forgetting the $1$ from differentiating $x$ in the substitution.",
  "U09-A-sub-rational", "Substitution, simplification, splitting a fraction.",
  check=_c32,
  values=[slope(Y - X - log(X + Y)), slope(Y - X + log(X + Y)), slope(Y - 2*log(X + Y + 1)), slope(Y - X - 2*log(X + Y))],
  source_class="XII", cognitive="Application")

def _c33():
    G = integrate(t**2/(t**2 + 4), t)          # (x+y)^2 y' = 4, t = x + y
    F = G.subs(t, X + Y) - X
    F = F - F.subs({X: 2, Y: 0})
    return curve(F, (2, 0))
q("U09-A-033", T_SUB, "Particular solution after substitution", "Medium", "Multi-step computation MCQ",
  r"The solution curve of $(x + y)^{2}" + D1 + r" = 4$ passing through the point $(2, 0)$ is",
  r"$y + \frac{\pi}{2} = 2\tan^{-1}\left(\frac{x + y}{2}\right)$",
  [(r"$y + \pi = 4\tan^{-1}\left(\frac{x + y}{2}\right)$", r"Uses $\int \frac{dt}{t^2 + 4} = \tan^{-1}\frac{t}{2}$, missing the factor $\frac{1}{2}$."),
   (r"$y + 2\tan^{-1} 2 = 2\tan^{-1}(x + y)$", r"Uses $\int \frac{dt}{t^2 + 4} = \frac{1}{2}\tan^{-1} t$, missing the scaling inside the inverse tangent."),
   (r"$(x + y)^{3} = 12x - 16$", r"Writes $\frac{dt}{dx} = \frac{4}{t^2}$, forgetting the $1$ from $\frac{d}{dx}(x)$.")],
  r"Put $t = x + y$: $t^2\left(\frac{dt}{dx} - 1\right) = 4$, so $\frac{dt}{dx} = \frac{t^2 + 4}{t^2}$. Then $\int\left(1 - \frac{4}{t^2 + 4}\right)dt = x + c$ gives $t - 2\tan^{-1}\frac{t}{2} = x + c$, that is $y - 2\tan^{-1}\frac{x + y}{2} = c$. At $(2, 0)$, $c = -2\tan^{-1} 1 = -\frac{\pi}{2}$, so $y + \frac{\pi}{2} = 2\tan^{-1}\frac{x + y}{2}$.",
  r"Mishandling the factor in $\int \frac{dt}{t^2 + a^2} = \frac{1}{a}\tan^{-1}\frac{t}{a}$.",
  "U09-A-sub-particular-arctan", "Substitution, polynomial division, a standard integral, a constant.",
  check=_c33,
  values=[curve(Y + pi/2 - 2*atan((X + Y)/2), (2, 0)), curve(Y + pi - 4*atan((X + Y)/2), (2, 0)),
          curve(Y + 2*atan(2) - 2*atan(X + Y), (2, 0)), curve((X + Y)**3 - 12*X + 16, (2, 0))],
  source_class="XII", cognitive="Application")

def _c34():
    def sol(ic):
        F = integrate(1/(1 + y**2), y) - integrate(1, x)
        return solve(Eq(F, F.subs({x: ic[0], y: ic[1]})), y)[0]
    s1 = simplify(sol((0, 1)).subs(x, pi/12)) == Rational(1, 1)/sqrt(3)
    F2 = integrate(1/y**2, y) - integrate(1, x)
    s2v = solve(Eq(F2.subs(x, Rational(1, 2)), F2.subs({x: 0, y: 1})), y)[0]
    s2 = simplify(s2v - 2) == 0
    return (bool(s1), bool(s2))
q("U09-A-034", T_PS, "Two particular values", "Medium", "Statement-based MCQ",
  r"Statement I: If $" + D1 + r" = 1 + y^2$ and $y(0) = 1$, then $y\left(\frac{\pi}{12}\right) = \frac{1}{\sqrt{3}}$. Statement II: If $" + D1 + r" = y^2$ and $y(0) = 1$, then $y\left(\frac{1}{2}\right) = 2$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Takes $\tan^{-1} y = \frac{\pi}{4} - x$, a sign slip, so $y\left(\frac{\pi}{12}\right) = \tan\frac{\pi}{6}$, and solves Statement II correctly."),
   (ST_TF, r"Makes the same slip in Statement I, and in Statement II writes $\frac{1}{y} = x + 1$, a sign slip, which gives $y\left(\frac{1}{2}\right) = \frac{2}{3}$."),
   (ST_FF, r"Solves Statement I correctly but rejects Statement II after the sign slip $\frac{1}{y} = x + 1$.")],
  r"Statement I: $\tan^{-1} y = x + \frac{\pi}{4}$, so $y\left(\frac{\pi}{12}\right) = \tan\frac{\pi}{3} = \sqrt{3}$, not $\frac{1}{\sqrt{3}}$; false. Statement II: $-\frac{1}{y} = x + c$ with $c = -1$, so $y = \frac{1}{1 - x}$ and $y\left(\frac{1}{2}\right) = 2$; true.",
  r"Subtracting instead of adding the constant angle.",
  "U09-A-ps-statements", "Two separate particular solutions to verify.",
  check=_c34, values=[(False, True), (True, True), (True, False), (False, False)], source_class="XII", cognitive="Analysis")

def _c35():
    s1 = slope(exp(X) + exp(Y)) == simplify(exp(X + Y))
    F = integrate(1/y, y) - integrate(2/x, x)
    v = solve(Eq(F.subs(x, 2), F.subs({x: 1, y: 3})), y)[0]
    s2 = simplify(v - 6) == 0
    return (bool(s1), bool(s2))
q("U09-A-035", T_VS, "Checking claimed solutions", "Medium", "Statement-based MCQ",
  r"Statement I: The general solution of $" + D1 + r" = e^{x+y}$ is $e^{x} + e^{y} = C$. Statement II: If $x" + D1 + r" = 2y$, $x > 0$, and $y(1) = 3$, then $y(2) = 6$." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Accepts $e^{x} + e^{y} = C$ without checking it against the equation (the correct family is $e^{x} + e^{-y} = C$), and solves $x\frac{dy}{dx} = 2y$ as $y = kx$, so $y = 3x$."),
   (ST_TF, r"Accepts the family in Statement I without checking it, but solves Statement II correctly."),
   (ST_FT, r"Rejects Statement I correctly but solves $x\frac{dy}{dx} = 2y$ as $y = 3x$, forgetting that $\log_e y = 2\log_e x + c$ gives $x^2$.")],
  r"Statement I: $e^{-y}\,dy = e^{x}\,dx$ gives $-e^{-y} = e^{x} + c$, that is $e^{x} + e^{-y} = C$. Differentiating $e^{x} + e^{y} = C$ gives $\frac{dy}{dx} = -e^{x-y}$, not $e^{x+y}$; false. Statement II: $\frac{dy}{y} = \frac{2\,dx}{x}$ gives $y = kx^2$, $k = 3$, so $y(2) = 12$; false.",
  r"Dropping a factor or sign when integrating exponentials and powers.",
  "U09-A-vs-statements", "Two independent separable computations.",
  check=_c35, values=[(False, False), (True, True), (True, False), (False, True)], source_class="XII", cognitive="Analysis")

# ================================================================ DIFFICULT (12)

def _c36():
    # t = x + y, t' = 1 + tan t = (sin t + cos t)/cos t
    G = integrate(cos(t)/(sin(t) + cos(t)), t)
    return slope(G.subs(t, X + Y) - X)
q("U09-A-036", T_SUB, "Substitution with tangent", "Difficult", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = \tan(x + y)$ is",
  r"$y - x + \log_e\left|\sin(x + y) + \cos(x + y)\right| = C$",
  [(r"$y - x - \log_e\left|\sin(x + y) + \cos(x + y)\right| = C$", r"Writes $\frac{\cos t}{\sin t + \cos t} = \frac{1}{2} - \frac{1}{2}\cdot\frac{\cos t - \sin t}{\sin t + \cos t}$, a sign slip."),
   (r"$\log_e\left|\sin(x + y)\right| = x + C$", r"Forgets the $1$ in $\frac{dt}{dx} = 1 + \tan t$ and integrates $\cot t$."),
   (r"$\log_e\left|\sin(x + y) + \cos(x + y)\right| = x + C$", r"Treats $\frac{\cos t}{\sin t + \cos t}$ as $\frac{f'(t)}{f(t)}$ with $f = \sin t + \cos t$.")],
  r"Put $t = x + y$: $\frac{dt}{dx} = 1 + \tan t = \frac{\sin t + \cos t}{\cos t}$. Write $\frac{\cos t}{\sin t + \cos t} = \frac{1}{2} + \frac{1}{2}\cdot\frac{\cos t - \sin t}{\sin t + \cos t}$, which integrates to $\frac{t}{2} + \frac{1}{2}\log_e|\sin t + \cos t|$. So $t + \log_e|\sin t + \cos t| = 2x + C$, that is $y - x + \log_e|\sin(x + y) + \cos(x + y)| = C$.",
  r"Misreading $\frac{\cos t}{\sin t + \cos t}$ as a pure logarithmic derivative.",
  "U09-A-sub-tangent", "Substitution, then the numerator split into denominator plus its derivative; a non-obvious integral.",
  check=_c36,
  values=[slope(Y - X + log(sin(X + Y) + cos(X + Y))), slope(Y - X - log(sin(X + Y) + cos(X + Y))),
          slope(log(sin(X + Y)) - X), slope(log(sin(X + Y) + cos(X + Y)) - X)],
  source_class="XII", cognitive="Analysis")

def _c37():
    G = integrate((t + 1)/(3*t + 4), t)        # t' = (3t + 4)/(t + 1)
    F = G.subs(t, X + Y) - X
    F = F - F.subs({X: 0, Y: 0})
    return curve(F, (0, 0))
q("U09-A-037", T_SUB, "Particular solution, linear expression in x + y", "Difficult", "Multi-step computation MCQ",
  r"The solution curve of $" + D1 + r" = \dfrac{2x + 2y + 3}{x + y + 1}$ passing through the origin (in the region $x + y > -1$) is",
  r"$3y - 6x = \log_e\left(\frac{3x + 3y + 4}{4}\right)$",
  [(r"$3y - 6x = \log_e(3x + 3y + 4)$", r"Drops the constant fixed by the origin."),
   (r"$y - 2x = \log_e\left(\frac{3x + 3y + 4}{4}\right)$", r"Integrates $\frac{1}{3t + 4}$ as $\log_e(3t + 4)$, missing the factor $\frac{1}{3}$."),
   (r"$2y - 2x = \log_e\left(\frac{2x + 2y + 3}{3}\right)$", r"Forgets the $1$ in $\frac{dt}{dx} = 1 + \frac{dy}{dx}$, solving $\frac{dt}{dx} = \frac{2t + 3}{t + 1}$.")],
  r"Put $t = x + y$: $\frac{dt}{dx} = 1 + \frac{2t + 3}{t + 1} = \frac{3t + 4}{t + 1}$. Since $\frac{t + 1}{3t + 4} = \frac{1}{3} - \frac{1}{3(3t + 4)}$, integrating gives $\frac{t}{3} - \frac{1}{9}\log_e(3t + 4) = x + c$. At the origin $c = -\frac{1}{9}\log_e 4$. Multiplying by $9$: $3(x + y) - 9x = \log_e\frac{3t + 4}{4}$, that is $3y - 6x = \log_e\frac{3x + 3y + 4}{4}$.",
  r"Forgetting the $1$ from differentiating $x$, or a missing inner-derivative factor.",
  "U09-A-sub-linear-ratio", "Substitution, polynomial division, inner-derivative factor and a constant.",
  check=_c37,
  values=[curve(3*Y - 6*X - log((3*X + 3*Y + 4)/4), (0, 0)), curve(3*Y - 6*X - log(3*X + 3*Y + 4), (0, 0)),
          curve(Y - 2*X - log((3*X + 3*Y + 4)/4), (0, 0)), curve(2*Y - 2*X - log((2*X + 2*Y + 3)/3), (0, 0))],
  source_class="XII", cognitive="Analysis")

def _c38():
    G = integrate(1/(4 + t**2), t)             # t = 4x + y + 1, t' = 4 + t^2
    c0 = G.subs(t, 2) - 0
    tv = solve(Eq(G - pi/24, c0), t)
    tv = [s for s in tv if s.is_positive][0]
    return simplify(tv - 4*pi/24 - 1)
q("U09-A-038", T_SUB, "Substitution 4x + y + 1 = t", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$ satisfy $" + D1 + r" = (4x + y + 1)^{2}$ with $y(0) = 1$. Then $y\left(\frac{\pi}{24}\right)$ equals",
  r"$2\sqrt{3} - \frac{\pi}{6} - 1$",
  [(r"$2\sqrt{3} - 1$", r"Finds $4x + y + 1 = 2\sqrt{3}$ but forgets to subtract $4x = \frac{\pi}{6}$."),
   (r"$2\sqrt{3} + \frac{\pi}{6} - 1$", r"Finds $4x + y + 1 = 2\sqrt{3}$ but adds $4x$ instead of subtracting it."),
   (r"$\sqrt{3} - \frac{\pi}{6} - 1$", r"Drops the factor $2$ in $t = 2\tan\left(2x + \frac{\pi}{4}\right)$.")],
  r"Put $t = 4x + y + 1$: $\frac{dt}{dx} = 4 + t^2$, so $\frac{1}{2}\tan^{-1}\frac{t}{2} = x + c$. At $x = 0$, $t = 2$, so $c = \frac{\pi}{8}$ and $t = 2\tan\left(2x + \frac{\pi}{4}\right)$. At $x = \frac{\pi}{24}$, $t = 2\tan\frac{\pi}{3} = 2\sqrt{3}$, so $y = 2\sqrt{3} - \frac{\pi}{6} - 1$.",
  r"Forgetting to undo the substitution completely.",
  "U09-A-sub-shifted-square", "Substitution with coefficient $4$, scaled inverse tangent, constant, back-substitution.",
  check=_c38, values=[2*sqrt(3) - pi/6 - 1, 2*sqrt(3) - 1, 2*sqrt(3) + pi/6 - 1, sqrt(3) - pi/6 - 1], source_class="XII", cognitive="Analysis")

def _c39():
    G = log((1 + t)/(1 - t))/2                 # t = x - y, t' = 1 - t^2
    assert simplify(diff(G, t) - 1/(1 - t**2)) == 0
    c0 = G.subs(t, 0)
    tv = solve(Eq(G, log(2) + c0), t)
    tv = [s for s in tv if s.is_real and abs(s) < 1][0]
    return simplify(log(2) - tv)
q("U09-A-039", T_SUB, "Substitution x - y = t", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$ satisfy $" + D1 + r" = (x - y)^{2}$ with $y(0) = 0$. Then $y(\log_e 2)$ equals",
  r"$\log_e 2 - \frac{3}{5}$",
  [(r"$\log_e 2 - \frac{1}{3}$", r"Integrates $\frac{1}{1 - t^2}$ as $\log_e\frac{1 + t}{1 - t}$, missing the factor $\frac{1}{2}$, so $\frac{1 + t}{1 - t} = e^{x}$."),
   (r"$\log_e 2 + \frac{3}{5}$", r"Finds $t = \frac{3}{5}$ but takes $y = x + t$ instead of $y = x - t$."),
   (r"$\log_e 2 - \frac{5}{3}$", r"Solves $\frac{1 + t}{1 - t} = 4$ as $t = \frac{4 + 1}{4 - 1}$, inverting the fraction.")],
  r"Put $t = x - y$: $\frac{dt}{dx} = 1 - t^2$, so $\frac{1}{2}\log_e\frac{1 + t}{1 - t} = x + c$ with $c = 0$ since $t(0) = 0$. At $x = \log_e 2$, $\frac{1 + t}{1 - t} = 4$, so $t = \frac{3}{5}$ and $y = x - t = \log_e 2 - \frac{3}{5}$.",
  r"Losing the factor $\frac{1}{2}$ in $\int\frac{dt}{1 - t^2}$.",
  "U09-A-sub-difference-square", "Substitution with a minus sign, partial fractions, solving for $t$, back-substitution.",
  check=_c39, values=[log(2) - Rational(3, 5), log(2) - Rational(1, 3), log(2) + Rational(3, 5), log(2) - Rational(5, 3)],
  source_class="XII", cognitive="Analysis")

def _c40():
    G = integrate(y*(2*log(y) + 1), y)        # y^2 log y
    H = integrate(sin(x) + x*cos(x), x)       # x sin x
    c0 = G.subs(y, 1) - H.subs(x, 0)
    return simplify(H.subs(x, pi/2) + c0)
q("U09-A-040", T_PS, "Recognising exact derivatives on both sides", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $y > 0$, satisfy $y\,(2\log_e y + 1)" + D1 + r" = \sin x + x\cos x$ with $y(0) = 1$. Then the value of $y^{2}\log_e y$ at $x = \frac{\pi}{2}$ is",
  r"$\frac{\pi}{2}$",
  [(r"$\frac{\pi}{2} + 1$", r"Uses $\int x\cos x\,dx = x\sin x$, dropping $\cos x$, so the right side becomes $x\sin x - \cos x + 1$."),
   (r"$\frac{\pi}{2} + 2$", r"Uses $\int x\cos x\,dx = x\sin x - \cos x$, a sign slip, so the right side becomes $x\sin x - 2\cos x + 2$."),
   (r"$\pi$", r"Takes $\int y(2\log_e y + 1)\,dy = \frac{1}{2}y^2\log_e y$, so $y^2\log_e y = 2x\sin x$.")],
  r"$\frac{d}{dy}(y^2\log_e y) = 2y\log_e y + y$ and $\frac{d}{dx}(x\sin x) = \sin x + x\cos x$. So $y^2\log_e y = x\sin x + c$, and $y(0) = 1$ gives $c = 0$. At $x = \frac{\pi}{2}$, $y^2\log_e y = \frac{\pi}{2}$.",
  r"Errors in integration by parts on either side.",
  "U09-A-ps-exact-derivative", "Both sides need integration by parts or recognition of a product derivative.",
  check=_c40, values=[pi/2, pi/2 + 1, pi/2 + 2, pi], source_class="XII", cognitive="Analysis")

def _c41():
    s_ = Symbol('s', real=True)
    # log y(2) - log y(-2) = integral of |s| from -2 to 2, with y(-2) = 1
    return simplify(integrate(Abs(s_), (s_, -2, 2)) + log(1))
q("U09-A-041", T_PS, "Separable equation with modulus", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$ be the differentiable function on $\mathbb{R}$ satisfying $" + D1 + r" = |x|\,y$ for all real $x$, with $y(-2) = 1$. Then $\log_e y(2)$ equals",
  r"$4$",
  [(r"$0$", r"Uses $\int |x|\,dx = \frac{x^2}{2}$ for all $x$, so $\log_e y = \frac{x^2}{2} + c$; since $\frac{x^2}{2}$ is even, $\log_e y(2) = \log_e y(-2) = 0$."),
   (r"$2$", r"Fixes the constant as if the given value were $y(0) = 1$, so $\log_e y(2) = \int_0^2 x\,dx = 2$, ignoring the part from $-2$ to $0$."),
   (r"$8$", r"Takes the antiderivative of $|x|$ as $x|x|$, dropping the factor $\frac{1}{2}$, so $\log_e y(2) = 4 - (-4) = 8$.")],
  r"Separating, $\log_e y = \frac{x|x|}{2} + c$, since $\frac{d}{dx}\left(\frac{x|x|}{2}\right) = |x|$ on all of $\mathbb{R}$ (one constant, as $y$ is differentiable through $x = 0$). From $y(-2) = 1$: $0 = -2 + c$, so $c = 2$. Then $\log_e y(2) = 2 + 2 = 4$.",
  r"Using $\frac{x^2}{2}$ as the antiderivative of $|x|$ across $x = 0$.",
  "U09-A-ps-modulus", r"Antiderivative of $|x|$ is $\frac{x|x|}{2}$, not $\frac{x^2}{2}$; a single constant must carry the solution across $x = 0$, and the even-function trap gives $0$.",
  check=_c41, values=[4, 0, 2, 8], source_class="XII", cognitive="Analysis",
  numerical=dict(question=r"Let $y = y(x)$ be the differentiable function on $\mathbb{R}$ satisfying $\frac{dy}{dx} = |x|\,y$ for all real $x$, with $y(-2) = 1$. Then $\log_e y(2)$ is", answer=4))

def _c42():
    # midpoint of P(x, y) and T(x - y/y', 0) lies on the y-axis: 2x - y/y' = 0 -> y' = y/(2x)
    pp = Symbol('pp')
    yp = solve(Eq(2*x - y/pp, 0), pp)[0]
    F = integrate(1/y, y) - integrate(simplify(yp/y), x)
    c0 = F.subs({x: 1, y: 2})
    sols = [s for s in solve(Eq(F.subs(x, 4), c0), y) if s.is_positive]
    return simplify(sols[0])
q("U09-A-042", T_PS, "Tangent bisected by the y-axis", "Difficult", "Multi-step computation MCQ",
  r"A curve $y = f(x)$, $x > 0$, $y > 0$, passes through $(1, 2)$. At every point $P$ of it, the segment of the tangent from $P$ to the point where the tangent meets the $x$-axis is bisected by the $y$-axis. Then $f(4)$ equals",
  r"$4$",
  [(r"$32$", r"Writes the condition as $\frac{dy}{dx} = \frac{2y}{x}$, inverting the ratio, so $y = 2x^2$."),
   (r"$8$", r"Assumes the tangent passes through the origin, $\frac{dy}{dx} = \frac{y}{x}$, so $y = 2x$."),
   (r"$\sqrt{34}$", r"Takes the $x$-intercept of the tangent as $x - y\frac{dy}{dx}$, getting $y\frac{dy}{dx} = 2x$ and $y^2 = 2x^2 + 2$.")],
  r"The tangent at $P(x, y)$ meets the $x$-axis at $\left(x - \frac{y}{y'}, 0\right)$. The midpoint has abscissa $0$, so $2x = \frac{y}{y'}$, that is $\frac{dy}{y} = \frac{dx}{2x}$. Integrating, $y^2 = kx$, and $(1, 2)$ gives $k = 4$. So $f(4) = \sqrt{16} = 4$.",
  r"Using the wrong intercept of the tangent.",
  "U09-A-app-tangent-bisected", "Geometry to a DE, then separation and a constant; several places to slip.",
  check=_c42, values=[4, 32, 8, sqrt(34)], source_class="XII", cognitive="Analysis",
  numerical=dict(question=r"A curve $y = f(x)$, $x > 0$, $y > 0$, passes through $(1, 2)$. At every point $P$ of it, the segment of the tangent from $P$ to the point where the tangent meets the $x$-axis is bisected by the $y$-axis. Then $f(4)$ is", answer=4))

def _c43():
    G = integrate(1/(1 + y**2), y) - integrate(1, x)   # f' = 1 + f^2, so atan f - x = const
    c0 = G.subs({x: 0, y: -3})                         # f(0) = -3 from the integral equation
    ang = c0 + pi/4                                     # atan f(pi/4)
    assert -pi/2 < N(ang) < pi/2                        # solution exists on the whole interval
    return simplify(expand_trig(tan(ang)))
q("U09-A-043", T_PS, "Integral equation reducing to a separable DE", "Difficult", "Multi-step computation MCQ",
  r"Let $f$ be a differentiable function on $\left[0, \frac{\pi}{4}\right]$ such that $f(x) = -3 + \int_0^{x}\left(1 + f(t)^{2}\right)dt$ for all $x$ in this interval. Then $f\left(\frac{\pi}{4}\right)$ equals",
  r"$-\frac{1}{2}$",
  [(r"$1$", r"Uses $f(0) = 0$ instead of $-3$, getting $f(x) = \tan x$."),
   (r"$-2$", r"Writes $f(x) = \tan x - 3$, adding the initial value outside the tangent."),
   (r"$2$", r"Evaluates $\tan\left(\tan^{-1}(-3) + \frac{\pi}{4}\right)$ with the $\tan(\alpha - \beta)$ formula: $\frac{-3 - 1}{1 + (-3)(1)}$.")],
  r"Putting $x = 0$ gives $f(0) = -3$; differentiating gives $f'(x) = 1 + f(x)^2$. So $\tan^{-1} f = x + c$ with $c = \tan^{-1}(-3)$, and $x + c$ stays inside $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$ on the interval. Hence $f\left(\frac{\pi}{4}\right) = \tan\left(\tan^{-1}(-3) + \frac{\pi}{4}\right) = \frac{-3 + 1}{1 - (-3)(1)} = -\frac{1}{2}$.",
  r"Missing the initial value hidden in the integral equation.",
  "U09-A-ps-integral-equation", "Extract a DE and its initial value from an integral equation, then a compound angle.",
  check=_c43, values=[Rational(-1, 2), 1, -2, 2], source_class="XII", cognitive="Analysis")

def _c44():
    F = integrate(1/(y**2 - 1), y) - integrate(1/(x**2 - 1), x)
    c0 = F.subs({x: 2, y: 3})
    sols = [s for s in solve(Eq(F.subs(x, 3), c0), y) if s > 1]
    return simplify(sols[0])
q("U09-A-044", T_PS, "Partial fractions on both sides", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 1$, $y > 1$, be the solution of $" + D1 + r" = \dfrac{y^2 - 1}{x^2 - 1}$ with $y(2) = 3$. Then $y(3)$ equals",
  r"$7$",
  [(r"$5$", r"Writes $\frac{y-1}{y+1} = \frac{x-1}{x+1} + C$, adding the constant instead of multiplying."),
   (r"$2$", r"Uses $\frac{y-1}{y+1} = C\cdot\frac{x+1}{x-1}$, inverting one side."),
   (r"$4$", r"Reaches $\frac{y-1}{y+1} = \frac{3}{4}$ but expands $4(y - 1)$ as $4y - 1$.")],
  r"$\int\frac{dy}{y^2 - 1} = \frac{1}{2}\log_e\frac{y-1}{y+1}$, and similarly in $x$, so $\frac{y-1}{y+1} = C\cdot\frac{x-1}{x+1}$. At $(2, 3)$: $\frac{1}{2} = \frac{C}{3}$, so $C = \frac{3}{2}$. At $x = 3$: $\frac{y-1}{y+1} = \frac{3}{2}\cdot\frac{1}{2} = \frac{3}{4}$, so $4y - 4 = 3y + 3$ and $y = 7$.",
  r"Converting a logarithmic constant into an additive one.",
  "U09-A-ps-partial-fraction-both", "Partial fractions on both sides, a multiplicative constant, then solving for $y$.",
  check=_c44, values=[7, 5, 2, 4], source_class="XII", cognitive="Analysis",
  numerical=dict(question=r"Let $y = y(x)$, $x > 1$, $y > 1$, be the solution of $\frac{dy}{dx} = \dfrac{y^2 - 1}{x^2 - 1}$ with $y(2) = 3$. Then $y(3)$ is", answer=7))

def _c45():
    s = Symbol('s', positive=True)
    f = Function('f')
    # differentiate: f(t) = f(t)^2 f'(t)  ->  f f' = 1
    F = integrate(y, y) - integrate(1, x)
    c0 = F.subs({x: 1, y: 1})
    sols = [v for v in solve(Eq(F.subs(x, 5), c0), y) if v.is_positive]
    return sols[0]
q("U09-A-045", T_PS, "Area condition leading to a DE", "Difficult", "Multi-step computation MCQ",
  r"A curve $y = f(x)$, with $f(x) > 0$ for $x \ge 1$, passes through $(1, 1)$. For every $t > 1$, the area bounded by the curve, the $x$-axis and the lines $x = 1$ and $x = t$ equals $\frac{f(t)^{3} - 1}{3}$. Then $f(5)$ equals",
  r"$3$",
  [(r"$\sqrt{5}$", r"Reaches $f\,f' = 1$ but integrates $f\,df$ as $f^2$, getting $f^2 = x$."),
   (r"$e^{4}$", r"Differentiates to $f = f^2 f'$ but cancels to $f' = f$, so $f = e^{x - 1}$."),
   (r"$9$", r"Finds $f(5)^2 = 9$ and reports $f(5)^2$.")],
  r"Differentiating $\int_1^{t} f(x)\,dx = \frac{f(t)^3 - 1}{3}$ with respect to $t$ gives $f = f^2 f'$, so $f\,f' = 1$ (as $f > 0$). Then $\frac{f^2}{2} = x + c$ and $f(1) = 1$ gives $c = -\frac{1}{2}$, so $f^2 = 2x - 1$ and $f(5) = 3$.",
  r"Algebra slips after differentiating an area condition.",
  "U09-A-app-area-condition", "Fundamental theorem to obtain the DE, then separation and a constant.",
  check=_c45, values=[3, sqrt(5), exp(4), 9], source_class="XII", cognitive="Analysis",
  numerical=dict(question=r"A curve $y = f(x)$, with $f(x) > 0$ for $x \ge 1$, passes through $(1, 1)$. For every $t > 1$, the area bounded by the curve, the $x$-axis and the lines $x = 1$ and $x = t$ equals $\frac{f(t)^{3} - 1}{3}$. Then $f(5)$ is", answer=3))

def _c46():
    F = integrate(1/y**2, y) - integrate(x, x)
    c0 = F.subs({x: 0, y: 1})
    sol = solve(Eq(F, c0), y)[0]                     # 2/(2 - x^2)
    poles = sorted(solve(denom(together(sol)), x))
    return Interval.open(poles[0], poles[-1])
q("U09-A-046", T_PS, "Interval of existence", "Difficult", "Conceptual/application MCQ",
  r"Let $y = y(x)$ be the solution of $" + D1 + r" = xy^{2}$ with $y(0) = 1$, defined on the largest open interval containing $0$ on which it exists. This interval is",
  r"$(-\sqrt{2}, \sqrt{2})$",
  [(r"$(-1, 1)$", r"Integrates $x$ as $x^2$, getting $y = \frac{1}{1 - x^2}$."),
   (r"$(-\infty, \infty)$", r"Writes $\frac{1}{y} = \frac{x^2}{2} + c$, a sign slip, getting $y = \frac{2}{x^2 + 2}$, which never blows up."),
   (r"$(-2, 2)$", r"Finds $y = \frac{2}{2 - x^2}$ but solves $x^2 = 2$ as $x = \pm 2$.")],
  r"$\frac{dy}{y^2} = x\,dx$ gives $-\frac{1}{y} = \frac{x^2}{2} + c$, and $y(0) = 1$ gives $c = -1$. So $y = \frac{2}{2 - x^2}$, which blows up at $x = \pm\sqrt{2}$. The largest open interval containing $0$ is $(-\sqrt{2}, \sqrt{2})$.",
  r"Assuming a smooth right side means the solution exists for all $x$.",
  "U09-A-ps-interval-existence", "Solve, then reason about where the particular solution blows up.",
  check=_c46,
  values=[Interval.open(-sqrt(2), sqrt(2)), Interval.open(-1, 1), S.Reals, Interval.open(-2, 2)],
  source_class="XII", cognitive="Analysis")

def _c47():
    G = integrate((2*t + 5)/(t + 2), t)        # t = x - y, t' = (t + 2)/(2t + 5)
    return slope(G.subs(t, X - Y) - X)
q("U09-A-047", T_SUB, "Substitution x - y = t in a rational right side", "Difficult", "Multi-step computation MCQ",
  r"The general solution of $" + D1 + r" = \dfrac{x - y + 3}{2x - 2y + 5}$ (in the region $x - y + 2 > 0$) is",
  r"$x - 2y + \log_e(x - y + 2) = C$",
  [(r"$x - 2y - \log_e(x - y + 2) = C$", r"Splits $\frac{2t + 5}{t + 2}$ as $2 - \frac{1}{t + 2}$, a sign slip."),
   (r"$3x - 2y - \log_e(x - y + 3) = C$", r"Writes $\frac{dt}{dx} = -\frac{dy}{dx}$, forgetting the $1$, and integrates $\frac{2t + 5}{t + 3}$."),
   (r"$x - 2y + \log_e(2x - 2y + 5) = C$", r"Integrates $\frac{2t + 5}{t + 2}$ as $2t + \log_e(2t + 5)$, keeping the wrong denominator in the logarithm.")],
  r"Put $t = x - y$: $\frac{dt}{dx} = 1 - \frac{t + 3}{2t + 5} = \frac{t + 2}{2t + 5}$. Then $\int\frac{2t + 5}{t + 2}\,dt = \int\left(2 + \frac{1}{t + 2}\right)dt = 2t + \log_e(t + 2) = x + C$. So $2x - 2y + \log_e(x - y + 2) = x + C$, that is $x - 2y + \log_e(x - y + 2) = C$.",
  r"Forgetting the $1$ in $\frac{dt}{dx} = 1 - \frac{dy}{dx}$.",
  "U09-A-sub-difference-ratio", "Substitution with a minus sign, simplification, polynomial division, back-substitution.",
  check=_c47,
  values=[slope(X - 2*Y + log(X - Y + 2)), slope(X - 2*Y - log(X - Y + 2)),
          slope(3*X - 2*Y - log(X - Y + 3)), slope(X - 2*Y + log(2*X - 2*Y + 5))],
  source_class="XII", cognitive="Analysis")
