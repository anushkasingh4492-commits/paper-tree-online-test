import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x', real=True)
xp = Symbol('x', positive=True)
yv = Symbol('y', real=True)
yp = Symbol('y', positive=True)
t = Symbol('t', real=True)
Cs = Symbol('C', real=True)
Y = Function('Y')

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TOP_IF = "Integrating factor"
TOP_SOL = "Solving linear equations with initial conditions"
TOP_X = "Equations linear in x"
TOP_APP = "Applications of linear equations"


def _ivp(P, Q, v, v0, w0):
    """Solve w' + P w = Q with w(v0) = w0 via the integrating factor; return w as expression in v."""
    IF = simplify(exp(integrate(P, v)))
    w = (integrate(simplify(Q*IF), v) + Cs) / IF
    c = solve(Eq(w.subs(v, v0), w0), Cs)[0]
    return simplify(w.subs(Cs, c))


def _ds(eq, v, ics):
    sol = dsolve(eq, Y(v), ics=ics)
    return sol.rhs


# ================================================================ EASY
q("U09-C-001", TOP_IF, "Integrating factor after reducing to standard form", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, an integrating factor of the differential equation $x\frac{dy}{dx} + 2y = x^4$ is",
  r"$x^2$",
  [(r"$\frac{1}{x^2}$", r"Takes $e^{-\int \frac{2}{x}dx}$, a sign slip in the exponent."),
   (r"$2\log_e x$", r"Stops at $\int \frac{2}{x}\,dx = 2\log_e x$ and does not exponentiate."),
   (r"$e^{-\frac{2}{x^2}}$", r"Differentiates $P = \frac{2}{x}$ (getting $-\frac{2}{x^2}$) instead of integrating it.")],
  r"Dividing by $x$ gives $\frac{dy}{dx} + \frac{2}{x}y = x^3$, so $P = \frac{2}{x}$ and the integrating factor is $e^{\int \frac{2}{x}dx} = e^{2\log_e x} = x^2$.",
  "Forgetting to exponentiate $\\int P\\,dx$, or differentiating $P$ instead of integrating.",
  "U09-C-if-power", "One reduction to standard form and one integral.",
  check=lambda: simplify(exp(integrate(2/xp, xp))), values=[xp**2, xp**-2, 2*log(xp), exp(-2/xp**2)],
  cognitive="Recall", source_class="XII")

q("U09-C-002", TOP_IF, "Integrating factor with a trigonometric coefficient", "Easy", "Single-step computation MCQ",
  r"For $0 < x < \pi$, an integrating factor of $\frac{dy}{dx} + y\cot x = \cos x$ is",
  r"$\sin x$",
  [(r"$\cos x$", r"Integrates $\cot x$ as $\log_e|\cos x|$, mixing it up with the integral of $\tan x$."),
   (r"$\csc x$", r"Uses $e^{-\int \cot x\,dx}$, a sign slip, giving $\frac{1}{\sin x}$."),
   (r"$e^{-\csc^2 x}$", r"Differentiates $\cot x$ (getting $-\csc^2 x$) instead of integrating it.")],
  r"$\int \cot x\,dx = \log_e \sin x$ on $(0,\pi)$, so the integrating factor is $e^{\log_e \sin x} = \sin x$.",
  "Recalling the wrong antiderivative of $\\cot x$.",
  "U09-C-if-trig", "Single standard integral followed by exponentiation.",
  check=lambda: simplify(exp(integrate(cot(x), x))), values=[sin(x), cos(x), 1/sin(x), exp(-1/sin(x)**2)],
  cognitive="Recall", source_class="XII")


def _c003():
    return _ds(Eq(Y(x).diff(x) + Y(x), exp(-x)), x, {Y(0): 2}).subs(x, 1)
q("U09-C-003", TOP_SOL, "Value from an initial condition, exponential forcing", "Easy", "Single-step computation MCQ",
  r"If $y = y(x)$ satisfies $\frac{dy}{dx} + y = e^{-x}$ and $y(0) = 2$, then $y(1)$ equals",
  r"$\frac{3}{e}$",
  [(r"$\frac{2}{e}$", r"After multiplying by $e^x$ gets $\frac{d}{dx}(ye^x) = 1$ but integrates the right side to $0$, so $y = 2e^{-x}$."),
   (r"$3e$", r"Finds $ye^x = x + 2$ correctly but then multiplies by $e^x$ instead of dividing, writing $y = (x+2)e^x$."),
   (r"$\frac{1}{e}$", r"Takes the constant of integration as $0$, so $y = xe^{-x}$, ignoring $y(0) = 2$.")],
  r"The integrating factor is $e^x$, so $\frac{d}{dx}(ye^x) = 1$ and $ye^x = x + C$. From $y(0) = 2$, $C = 2$, so $y = (x+2)e^{-x}$ and $y(1) = \frac{3}{e}$.",
  "Multiplying by the integrating factor at the end instead of dividing.",
  "U09-C-ivp-exp-resonant", "One integrating factor, one constant from the initial condition.",
  check=_c003, values=[3/E, 2/E, 3*E, 1/E], source_class="XII")

q("U09-C-004", TOP_X, "Integrating factor of an equation linear in x", "Easy", "Single-step computation MCQ",
  r"For $y > 0$, the differential equation $y\,dx - (x + 2y^3)\,dy = 0$ is linear in $x$ (treated as a function of $y$). When it is written in the standard form $\frac{dx}{dy} + P(y)\,x = Q(y)$, its integrating factor $e^{\int P(y)\,dy}$ is",
  r"$\frac{1}{y}$",
  [(r"$y$", r"Writes the equation as $\frac{dx}{dy} + \frac{x}{y} = 2y^2$, a sign slip in the coefficient of $x$, so the factor is $e^{\log_e y} = y$."),
   (r"$e^{-y}$", r"Does not divide through by $y$: from $y\frac{dx}{dy} - x = 2y^3$ takes $P = -1$, giving $e^{\int -1\,dy} = e^{-y}$."),
   (r"$e^{\frac{1}{y^2}}$", r"Differentiates $P = -\frac{1}{y}$ (getting $\frac{1}{y^2}$) instead of integrating it, giving $e^{\frac{1}{y^2}}$.")],
  r"Dividing by $y\,dy$: $\frac{dx}{dy} = \frac{x}{y} + 2y^2$, i.e. $\frac{dx}{dy} - \frac{1}{y}x = 2y^2$, so $P(y) = -\frac{1}{y}$. The integrating factor is $e^{-\int \frac{dy}{y}} = e^{-\log_e y} = \frac{1}{y}$.",
  "Not reducing to the standard form $\\frac{dx}{dy} + P(y)x = Q(y)$ before reading off $P(y)$.",
  "U09-C-linx-if", "One rearrangement to $\\frac{dx}{dy} + P(y)x = Q(y)$ and one integral.",
  check=lambda: simplify(exp(integrate(-1/yp, yp))), values=[1/yp, yp, exp(-yp), exp(1/yp**2)], cognitive="Understanding", source_class="XII")


def _c005():
    return simplify(_ds(Eq(Y(x).diff(x) + 2*Y(x), 6), x, {Y(0): 1}).subs(x, log(2)))
q("U09-C-005", TOP_SOL, "Constant forcing with initial value", "Easy", "Single-step computation MCQ",
  r"If $y = y(x)$ is the solution of $\frac{dy}{dx} + 2y = 6$ with $y(0) = 1$, then $y(\log_e 2)$ equals",
  r"$\frac{5}{2}$",
  [(r"$2$", r"Gets $y = 3 - 2e^{-2x}$ but evaluates $e^{-2\log_e 2}$ as $\frac{1}{2}$ instead of $\frac{1}{4}$."),
   (r"$\frac{7}{2}$", r"Finds the constant with the wrong sign, $y = 3 + 2e^{-2x}$."),
   (r"$\frac{1}{4}$", r"Solves only $\frac{dy}{dx} + 2y = 0$, giving $y = e^{-2x}$.")],
  r"With integrating factor $e^{2x}$, $ye^{2x} = 3e^{2x} + C$, so $y = 3 + Ce^{-2x}$. Then $y(0) = 1$ gives $C = -2$, and $y(\log_e 2) = 3 - 2 \cdot \frac{1}{4} = \frac{5}{2}$.",
  "Dropping the particular (steady) part of the solution.",
  "U09-C-ivp-const", "Standard integrating factor and one substitution.",
  check=_c005, values=[Rational(5, 2), 2, Rational(7, 2), Rational(1, 4)], source_class="XII")

q("U09-C-006", TOP_IF, "Integrating factor that is a logarithm", "Easy", "Single-step computation MCQ",
  r"For $x > 1$, an integrating factor of $\frac{dy}{dx} + \frac{y}{x\log_e x} = x$ is",
  r"$\log_e x$",
  [(r"$x\log_e x$", r"Takes the denominator of the coefficient of $y$ as the factor instead of integrating."),
   (r"$\frac{1}{\log_e x}$", r"Uses $e^{-\int P\,dx}$, a sign slip."),
   (r"$x$", r"Integrates $\frac{1}{x\log_e x}$ as $\log_e x$, so the factor becomes $e^{\log_e x} = x$.")],
  r"With $u = \log_e x$, $\int \frac{dx}{x\log_e x} = \log_e(\log_e x)$, so the integrating factor is $e^{\log_e(\log_e x)} = \log_e x$ (positive for $x > 1$).",
  "Integrating $\\frac{1}{x\\log_e x}$ incorrectly.",
  "U09-C-if-log", "One substitution inside the exponent.",
  check=lambda: simplify(exp(integrate(1/(xp*log(xp)), xp))), values=[log(xp), xp*log(xp), 1/log(xp), xp],
  cognitive="Application", source_class="XII")


def _c007():
    return _ivp(1/xp, xp**2, xp, 1, 1).subs(xp, 2)
q("U09-C-007", TOP_SOL, "Value of a solution with integrating factor x", "Easy", "Single-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, satisfy $\frac{dy}{dx} + \frac{y}{x} = x^2$ and $y(1) = 1$. Then $y(2)$ equals",
  r"$\frac{19}{8}$",
  [(r"$\frac{19}{4}$", r"Gets $xy = \frac{x^4}{4} + \frac{3}{4}$ but forgets to divide by $x$ at $x = 2$."),
   (r"$\frac{5}{3}$", r"Does not multiply the right side by the factor: $xy = \frac{x^3}{3} + C$, $C = \frac{2}{3}$, so $y(2) = \frac{5}{3}$."),
   (r"$2$", r"Drops the constant, using $y = \frac{x^3}{4}$.")],
  r"The integrating factor is $x$: $\frac{d}{dx}(xy) = x^3$, so $xy = \frac{x^4}{4} + C$. From $y(1) = 1$, $C = \frac{3}{4}$, so $y(2) = \frac{4 + \frac{3}{4}}{2} = \frac{19}{8}$.",
  "Not multiplying $Q$ by the integrating factor.",
  "U09-C-ivp-power", "Standard factor $x$ and one constant.",
  check=_c007, values=[Rational(19, 8), Rational(19, 4), Rational(5, 3), 2],
  numerical=dict(question=r"Let $y = y(x)$, $x > 0$, satisfy $\frac{dy}{dx} + \frac{y}{x} = x^2$ and $y(1) = 1$. Then the value of $8\,y(2)$ is", answer=19), source_class="XII")


def _c008():
    T = _ds(Eq(Y(t).diff(t), -Rational(1, 10)*(Y(t) - 25)), t, {Y(0): 85})
    return simplify(T.subs(t, 10*log(3)))
q("U09-C-008", TOP_APP, "Cooling law as a linear equation", "Easy", "Single-step computation MCQ",
  r"The temperature $T$ (in $^\circ\mathrm{C}$) of a body at time $t$ minutes satisfies $\frac{dT}{dt} = -\frac{1}{10}(T - 25)$, with $T = 85$ at $t = 0$. The temperature at $t = 10\log_e 3$ is",
  r"$45$",
  [(r"$\frac{160}{3}$", r"Writes $T = 25 + 85e^{-t/10}$, using the initial temperature instead of the initial excess $85 - 25$."),
   (r"$65$", r"Finds the excess $60e^{-t/10} = 20$ correctly but treats it as the fall in temperature, giving $85 - 20$."),
   (r"$\frac{85}{3}$", r"Solves $\frac{dT}{dt} = -\frac{T}{10}$, dropping the surrounding temperature.")],
  r"Write $\frac{dT}{dt} + \frac{T}{10} = \frac{5}{2}$; with factor $e^{t/10}$, $T = 25 + Ce^{-t/10}$ and $C = 60$. At $t = 10\log_e 3$, $e^{-t/10} = \frac{1}{3}$, so $T = 25 + 20 = 45$.",
  "Applying the decay to the temperature itself instead of the excess over the surroundings.",
  "U09-C-app-cooling-value", "One linear solve and one substitution.",
  check=_c008, values=[45, Rational(160, 3), 65, Rational(85, 3)], source_class="XII")


def _c009():
    return simplify(_ds(Eq(Y(x).diff(x), Y(x) + 2*x), x, {Y(0): 1}).subs(x, 1))
q("U09-C-009", TOP_SOL, "Polynomial forcing, value at a point", "Easy", "Single-step computation MCQ",
  r"If $\frac{dy}{dx} = y + 2x$ and $y(0) = 1$, then $y(1)$ equals",
  r"$3e - 4$",
  [(r"$4 - e$", r"Integrates $\int 2xe^{-x}dx$ as $+2(x+1)e^{-x}$, a sign slip, giving $y = 2x + 2 - e^x$."),
   (r"$e - 4$", r"Uses $y = -2x - 2 + Ce^x$ but sets $C = y(0) = 1$, forgetting the $-2$ at $x = 0$."),
   (r"$\frac{3}{e}$", r"Solves $\frac{dy}{dx} + y = 2x$ instead, getting $y = 2x - 2 + 3e^{-x}$.")],
  r"Write $\frac{dy}{dx} - y = 2x$; with factor $e^{-x}$, $ye^{-x} = \int 2xe^{-x}dx = -2(x+1)e^{-x} + C$, so $y = -2x - 2 + Ce^x$. From $y(0) = 1$, $C = 3$, and $y(1) = 3e - 4$.",
  "Sign errors in integration by parts or in moving $y$ across.",
  "U09-C-ivp-poly-growth", "One integrating factor with one integration by parts.",
  check=_c009, values=[3*E - 4, 4 - E, E - 4, 3/E], source_class="XII")

q("U09-C-010", TOP_IF, "Recognising a linear equation", "Easy", "Direct concept MCQ",
  r"Which of the following differential equations is linear in $y$ (with $y$ a function of $x$)?",
  r"$\frac{dy}{dx} + x^2 y = \sin x$",
  [(r"$\frac{dy}{dx} + x y^2 = \sin x$", r"Thinks only $\frac{dy}{dx}$ must appear to the first power, ignoring the $y^2$ term."),
   (r"$y\frac{dy}{dx} + x^2 = \sin x$", r"Overlooks that the product $y\frac{dy}{dx}$ makes the equation non-linear."),
   (r"$\frac{dy}{dx} + x^2 \sin y = 0$", r"Treats $\sin y$ as harmless because the coefficient $x^2$ is a function of $x$ only.")],
  r"A first-order equation is linear in $y$ when it has the form $\frac{dy}{dx} + P(x)y = Q(x)$: $y$ and $\frac{dy}{dx}$ appear only to the first power and are not multiplied together or placed inside other functions. Only $\frac{dy}{dx} + x^2 y = \sin x$ has this form.",
  "Believing that non-linear terms in $x$ spoil linearity, or that terms like $y^2$, $y\\frac{dy}{dx}$, $\\sin y$ do not.",
  "U09-C-recognise-linear", "Direct recall of the definition.",
  cognitive="Understanding", source_class="XII")


def _c011():
    sol = dsolve(Eq(Y(x).diff(x) - Y(x), exp(x)), Y(x)).rhs
    return sol.subs(Symbol('C1'), Cs)
q("U09-C-011", TOP_SOL, "General solution with resonant forcing", "Easy", "Single-step computation MCQ",
  r"The general solution of $\frac{dy}{dx} - y = e^x$ is (where $C$ is an arbitrary constant)",
  r"$y = (x + C)e^x$",
  [(r"$y = \frac{e^x}{2} + Ce^{-x}$", r"Uses the factor $e^{x}$ (sign slip), solving $\frac{dy}{dx} + y = e^x$."),
   (r"$y = e^{2x} + Ce^x$", r"Does not multiply $e^x$ by the factor $e^{-x}$ before integrating, so $ye^{-x} = e^x + C$."),
   (r"$y = (x + C)e^{-x}$", r"Correctly gets $ye^{-x} = x + C$ but multiplies by $e^{-x}$ instead of dividing.")],
  r"The integrating factor is $e^{-x}$, giving $\frac{d}{dx}(ye^{-x}) = 1$. Hence $ye^{-x} = x + C$, i.e. $y = (x + C)e^x$.",
  "Mishandling the integrating factor when the forcing term matches the homogeneous solution.",
  "U09-C-general-resonant", "One integrating factor; the forcing cancels to a constant.",
  check=_c011, values=[(x + Cs)*exp(x), exp(x)/2 + Cs*exp(-x), exp(2*x) + Cs*exp(x), (x + Cs)*exp(-x)], source_class="XII")


def _c012():
    s1 = simplify(exp(integrate(2, x)) - exp(2*x)) == 0
    s2 = simplify(exp(integrate(-1/xp, xp)) - xp) == 0
    return (bool(s1), bool(s2))
q("U09-C-012", TOP_IF, "Statements on integrating factors", "Easy", "Statement-based MCQ",
  r"Statement I: An integrating factor of $\frac{dy}{dx} + 2y = x$ is $e^{2x}$. Statement II: For $x > 0$, an integrating factor of $x\frac{dy}{dx} - y = x^2$ is $x$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Reads $P = \frac{1}{x}$ for $x\frac{dy}{dx} - y = x^2$, losing the minus sign, and so accepts the factor $x$."),
   (ST_FF, r"Correctly rejects Statement II but forgets to integrate $P$ in Statement I, writing the factor as $e^{P} = e^{2}$, a constant, and so rejects $e^{2x}$."),
   (ST_FT, r"Uses $e^{-\int P\,dx}$ instead of $e^{\int P\,dx}$: gets $e^{-2x}$ for the first equation (rejecting Statement I) and $e^{\log_e x} = x$ for the second (accepting Statement II).")],
  r"For $\frac{dy}{dx} + 2y = x$, $P = 2$ and the factor is $e^{2x}$, so Statement I is true. For $x\frac{dy}{dx} - y = x^2$, the standard form is $\frac{dy}{dx} - \frac{1}{x}y = x$, so the factor is $e^{-\log_e x} = \frac{1}{x}$, not $x$; Statement II is false.",
  "Reading $P$ before putting the equation in standard form, or losing its sign.",
  "U09-C-stmt-if", "Two direct factor computations.",
  check=_c012, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding", source_class="XII")


def _c013():
    return simplify(_ds(Eq(Y(x).diff(x), 2*Y(x) + exp(x)), x, {Y(0): 0}).subs(x, log(2)))
q("U09-C-013", TOP_APP, "Curve from a slope condition", "Easy", "Single-step computation MCQ",
  r"A curve passes through the origin and its slope at every point $(x, y)$ on it is $2y + e^x$. The ordinate of the point on the curve with abscissa $\log_e 2$ is",
  r"$2$",
  [(r"$-2$", r"Integrates $e^{-x}$ as $e^{-x}$ (dropping the minus sign), giving $y = e^x - e^{2x}$."),
   (r"$4$", r"Does not multiply $e^x$ by the factor $e^{-2x}$: $ye^{-2x} = e^x - 1$, so $y = e^{3x} - e^{2x}$."),
   (r"$\frac{7}{12}$", r"Writes the equation as $\frac{dy}{dx} + 2y = e^x$, giving $y = \frac{e^x - e^{-2x}}{3}$.")],
  r"$\frac{dy}{dx} - 2y = e^x$ has factor $e^{-2x}$, so $ye^{-2x} = \int e^{-x}dx = -e^{-x} + C$. Through the origin, $C = 1$, so $y = e^{2x} - e^x$ and $y(\log_e 2) = 4 - 2 = 2$.",
  "Sign slips when integrating $e^{-x}$ or when moving $2y$ to the left side.",
  "U09-C-slope-exp", "Translate slope to an equation, then one standard solve.",
  check=_c013, values=[2, -2, 4, Rational(7, 12)],
  numerical=dict(question=r"A curve passes through the origin and its slope at every point $(x, y)$ on it is $2y + e^x$. The ordinate of the point on the curve with abscissa $\log_e 2$ is", answer=2), source_class="XII")


def _c014():
    A = _ds(Eq(Y(t).diff(t), 3 - Y(t)/50), t, {Y(0): 0})
    return limit(A, t, oo)
q("U09-C-014", TOP_APP, "Long-run value in a mixing model", "Easy", "Single-step computation MCQ",
  r"The amount $A$ (in kg) of salt in a tank at time $t$ (in minutes) satisfies $\frac{dA}{dt} = 3 - \frac{A}{50}$, with $A(0) = 0$. As $t \to \infty$, $A$ approaches",
  r"$150$",
  [(r"$50$", r"Reads the constant $50$ in the decay term as the limiting amount."),
   (r"$\frac{3}{50}$", r"Sets $3 - \frac{A}{50} = 0$ but solves it as $A = \frac{3}{50}$."),
   (r"$3$", r"Takes the inflow rate $3$ as the limiting amount.")],
  r"$\frac{dA}{dt} + \frac{A}{50} = 3$ with factor $e^{t/50}$ gives $A = 150 + Ce^{-t/50}$; $A(0) = 0$ gives $C = -150$. So $A = 150(1 - e^{-t/50}) \to 150$.",
  "Confusing the rate constants with the equilibrium value.",
  "U09-C-app-mixing-limit", "One linear solve and a limit.",
  check=_c014, values=[150, 50, Rational(3, 50), 3],
  numerical=dict(question=r"The amount $A$ (in kg) of salt in a tank at time $t$ (in minutes) satisfies $\frac{dA}{dt} = 3 - \frac{A}{50}$, with $A(0) = 0$. The limiting value of $A$ as $t \to \infty$ is", answer=150), source_class="XII")


# ================================================================ MEDIUM
def _c015():
    yy = _ds(Eq(cos(x)*Y(x).diff(x) + Y(x)*sin(x), 1), x, {Y(0): 2})
    return simplify(yy.subs(x, pi/3))
q("U09-C-015", TOP_SOL, "Trigonometric integrating factor", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $-\frac{\pi}{2} < x < \frac{\pi}{2}$, satisfy $\cos x\frac{dy}{dx} + y\sin x = 1$ and $y(0) = 2$. Then $y\left(\frac{\pi}{3}\right)$ equals",
  r"$1 + \frac{\sqrt{3}}{2}$",
  [(r"$2 + \frac{\sqrt{3}}{2}$", r"Writes the solution as $y = \sin x + C$, not multiplying the constant by $\cos x$."),
   (r"$4 + 2\sqrt{3}$", r"From $y\sec x = \tan x + 2$ multiplies by $\sec x$ instead of $\cos x$."),
   (r"$1 - \frac{\sqrt{3}}{2}$", r"Integrates $\sec^2 x$ as $-\tan x$, giving $y = 2\cos x - \sin x$.")],
  r"Standard form: $\frac{dy}{dx} + y\tan x = \sec x$, factor $\sec x$. Then $\frac{d}{dx}(y\sec x) = \sec^2 x$, so $y\sec x = \tan x + C$, i.e. $y = \sin x + C\cos x$. $y(0) = 2$ gives $C = 2$, so $y\left(\frac{\pi}{3}\right) = \frac{\sqrt{3}}{2} + 1$.",
  "Mishandling the factor $\\sec x$ when returning to $y$.",
  "U09-C-ivp-trig-sec", "Standard form, trigonometric factor, initial condition.",
  check=_c015, values=[1 + sqrt(3)/2, 2 + sqrt(3)/2, 4 + 2*sqrt(3), 1 - sqrt(3)/2], source_class="XII")


def _c016():
    k = Symbol('k')
    yy = _ivp(1, 2*x, x, 0, k)
    return solve(Eq(yy.subs(x, 1), 3/E), k)[0]
q("U09-C-016", TOP_SOL, "Initial value recovered from a later value", "Medium", "Inverse/parameter MCQ",
  r"Let $y = y(x)$ satisfy $\frac{dy}{dx} + y = 2x$. If $y(1) = \frac{3}{e}$, then $y(0)$ equals",
  r"$1$",
  [(r"$3$", r"Finds the constant $C = 3$ in $y = 2x - 2 + Ce^{-x}$ and reports it as $y(0)$."),
   (r"$-2$", r"Evaluates only the particular part $2x - 2$ at $x = 0$."),
   (r"$\frac{3}{e^2} - 2$", r"Uses $y = 2x - 2 + Ce^{x}$, a sign slip in the exponent, so $C = \frac{3}{e^2}$.")],
  r"With factor $e^x$, $ye^x = \int 2xe^x dx = (2x - 2)e^x + C$, so $y = 2x - 2 + Ce^{-x}$. Then $y(1) = \frac{C}{e} = \frac{3}{e}$ gives $C = 3$ and $y(0) = -2 + 3 = 1$.",
  "Confusing the constant of integration with the initial value.",
  "U09-C-reverse-initial", "Reversed unknown: solve, fix $C$ from a later value, then evaluate at $0$.",
  check=_c016, values=[1, 3, -2, 3/E**2 - 2], cognitive="Analysis", source_class="XII")


def _c017():
    tt = Symbol('tau', real=True)
    X = _ivp(1/(1 + yv**2), atan(yv)/(1 + yv**2), yv, 0, 0)
    return simplify(X.subs(yv, 1))
q("U09-C-017", TOP_X, "Linear in x with inverse tangent", "Medium", "Multi-step computation MCQ",
  r"Let $x = x(y)$ satisfy $(1 + y^2)\,dx = (\tan^{-1} y - x)\,dy$ with $x = 0$ when $y = 0$. Then the value of $x$ when $y = 1$ is",
  r"$\frac{\pi}{4} - 1 + e^{-\pi/4}$",
  [(r"$\frac{\pi}{4} + 1 - e^{-\pi/4}$", r"Integrates $\int te^t\,dt$ as $(t + 1)e^t$, giving $x = t + 1 - e^{-t}$ with $t = \tan^{-1} y$."),
   (r"$\frac{\pi}{4} - 1 - e^{-\pi/4}$", r"Gets $x = t - 1 + Ce^{-t}$ but solves $0 = -1 + C$ as $C = -1$."),
   (r"$\frac{\pi}{4} - 1$", r"Drops the constant of integration, keeping only $x = \tan^{-1} y - 1$.")],
  r"$\frac{dx}{dy} + \frac{x}{1+y^2} = \frac{\tan^{-1} y}{1+y^2}$ has factor $e^{\tan^{-1} y}$. With $t = \tan^{-1} y$: $xe^t = \int te^t\,dt = (t - 1)e^t + C$, so $x = t - 1 + Ce^{-t}$. $x = 0$ at $t = 0$ gives $C = 1$; at $y = 1$, $t = \frac{\pi}{4}$ and $x = \frac{\pi}{4} - 1 + e^{-\pi/4}$.",
  "Integration by parts sign errors and dropping the constant.",
  "U09-C-linx-atan", "Recognise linearity in $x$, substitute $t = \\tan^{-1} y$, integrate by parts.",
  check=_c017, values=[pi/4 - 1 + exp(-pi/4), pi/4 + 1 - exp(-pi/4), pi/4 - 1 - exp(-pi/4), pi/4 - 1], source_class="XII")


def _c018():
    yy = _ivp(-1/xp, xp, xp, 1, 0)
    return yy.subs(xp, 3)
q("U09-C-018", TOP_APP, "Curve with slope y/x + x", "Medium", "Multi-step computation MCQ",
  r"A curve in the region $x > 0$ passes through $(1, 0)$, and the slope of its tangent at every point $(x, y)$ is $\frac{y}{x} + x$. The ordinate of the point on the curve with abscissa $3$ is",
  r"$6$",
  [(r"$12$", r"Does not multiply $x$ by the factor $\frac{1}{x}$: $\frac{y}{x} = \frac{x^2}{2} - \frac{1}{2}$."),
   (r"$\frac{26}{9}$", r"Uses the factor $x$ (sign slip): $xy = \frac{x^3}{3} - \frac{1}{3}$."),
   (r"$9$", r"Ignores the constant, taking $y = x^2$, which does not pass through $(1, 0)$.")],
  r"$\frac{dy}{dx} - \frac{y}{x} = x$ has factor $\frac{1}{x}$, so $\frac{d}{dx}\left(\frac{y}{x}\right) = 1$ and $y = x^2 + Cx$. Through $(1, 0)$: $C = -1$, so $y = x^2 - x$ and $y(3) = 6$.",
  "Not multiplying the right side by the integrating factor.",
  "U09-C-slope-y-over-x", "Translate geometry to a linear equation and solve with a condition.",
  check=_c018, values=[6, 12, Rational(26, 9), 9],
  numerical=dict(question=r"A curve in the region $x > 0$ passes through $(1, 0)$, and the slope of its tangent at every point $(x, y)$ is $\frac{y}{x} + x$. The ordinate of the point on the curve with abscissa $3$ is", answer=6), source_class="XII")


def _c019():
    # y-intercept of tangent: y - x y' = x^2
    yy = _ds(Eq(Y(xp) - xp*Y(xp).diff(xp), xp**2), xp, {Y(1): 1})
    return simplify(yy.subs(xp, 3))
q("U09-C-019", TOP_APP, "Curve from a tangent intercept condition", "Medium", "Multi-step computation MCQ",
  r"A curve lies in the region $x > 0$ and passes through $(1, 1)$. For every point $P(x, y)$ on it, the tangent at $P$ cuts the $y$-axis at a point whose ordinate is $x^2$. The value of $y$ on the curve at $x = 3$ is",
  r"$-3$",
  [(r"$\frac{29}{9}$", r"Takes the $y$-intercept of the tangent as $y + x\frac{dy}{dx}$, so $\frac{d}{dx}(xy) = x^2$."),
   (r"$9$", r"Takes the intercept as $x\frac{dy}{dx} - y$, giving $y = x^2 + Cx$ with $C = 0$."),
   (r"$-9$", r"Uses the correct equation but does not multiply $-x$ by the factor $\frac{1}{x}$: $\frac{y}{x} = -\frac{x^2}{2} + \frac{3}{2}$.")],
  r"The tangent at $P$ is $Y - y = y'(X - x)$, whose $y$-intercept is $y - xy'$. So $y - xy' = x^2$, i.e. $\frac{dy}{dx} - \frac{y}{x} = -x$. With factor $\frac{1}{x}$, $\frac{y}{x} = -x + C$; through $(1, 1)$, $C = 2$. So $y = 2x - x^2$ and $y(3) = -3$.",
  "Wrong formula for the intercept of a tangent.",
  "U09-C-tangent-intercept", "Geometry to equation, then a linear solve with a condition.",
  check=_c019, values=[-3, Rational(29, 9), 9, -9], cognitive="Analysis", source_class="XII")


def _c020():
    P = _ds(Eq(Y(t).diff(t), Y(t)/10 - 50), t, {Y(0): 600})
    s = solve(Eq(P, 700), t)
    return simplify(s[0])
q("U09-C-020", TOP_APP, "Population with constant harvesting", "Medium", "Multi-step computation MCQ",
  r"A fish population $P(t)$ ($t$ in years) grows according to $\frac{dP}{dt} = \frac{P}{10} - 50$, where $50$ fish per year are removed. If $P(0) = 600$, the population reaches $700$ when $t$ equals",
  r"$10\log_e 2$",
  [(r"$10\log_e\frac{7}{6}$", r"Ignores the harvesting term, solving $600e^{t/10} = 700$."),
   (r"$10\log_e\frac{12}{11}$", r"Takes the equilibrium as $-500$ (sign slip), so $P = -500 + 1100e^{t/10}$."),
   (r"$\log_e 2$", r"Correctly reaches $e^{t/10} = 2$ but drops the factor $10$.")],
  r"$\frac{dP}{dt} - \frac{P}{10} = -50$ with factor $e^{-t/10}$ gives $P = 500 + Ce^{t/10}$, and $P(0) = 600$ gives $C = 100$. Then $500 + 100e^{t/10} = 700$ gives $e^{t/10} = 2$, $t = 10\log_e 2$.",
  "Ignoring the constant term that sets the equilibrium.",
  "U09-C-app-harvest", "Linear solve with an equilibrium shift, then solving for time.",
  check=_c020, values=[10*log(2), 10*log(Rational(7, 6)), 10*log(Rational(12, 11)), log(2)], source_class="XII")


def _c021():
    yy = _ivp(1/(xp*log(xp)), 2/xp, xp, E, 2)
    return simplify(yy.subs(xp, E**2))
q("U09-C-021", TOP_SOL, "Logarithmic integrating factor with a condition", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 1$, satisfy $x\log_e x\,\frac{dy}{dx} + y = 2\log_e x$ and $y(e) = 2$. Then $y(e^2)$ equals",
  r"$\frac{5}{2}$",
  [(r"$2$", r"Integrates $\frac{2}{x}$ without multiplying by the factor $\log_e x$: $y\log_e x = 2\log_e x + C$ with $C = 0$."),
   (r"$\frac{7}{4}$", r"Integrates $\frac{2\log_e x}{x}$ as $\frac{(\log_e x)^2}{2}$, so $C = \frac{3}{2}$."),
   (r"$5$", r"Finds $y\log_e x = (\log_e x)^2 + 1$ but forgets to divide by $\log_e x = 2$.")],
  r"Standard form: $\frac{dy}{dx} + \frac{y}{x\log_e x} = \frac{2}{x}$, factor $\log_e x$. Then $\frac{d}{dx}(y\log_e x) = \frac{2\log_e x}{x}$, so $y\log_e x = (\log_e x)^2 + C$. $y(e) = 2$ gives $C = 1$, so $y = \log_e x + \frac{1}{\log_e x}$ and $y(e^2) = 2 + \frac{1}{2} = \frac{5}{2}$.",
  "Not multiplying $Q$ by the integrating factor.",
  "U09-C-ivp-log-factor", "Reduce to standard form, logarithmic factor, substitution integral.",
  check=_c021, values=[Rational(5, 2), 2, Rational(7, 4), 5], source_class="XII")


def _c022():
    yy = _ds(Eq(Y(x).diff(x) + 2*x*Y(x), 2*x), x, None)
    gen = yy.subs(Symbol('C1'), Cs)
    s1 = limit(gen, x, oo) == 0
    part = _ds(Eq(Y(x).diff(x) + 2*x*Y(x), 2*x), x, {Y(0): 0})
    s2 = simplify(part.subs(x, 1) - (1 - 1/E)) == 0
    return (bool(s1), bool(s2))
q("U09-C-022", TOP_SOL, "Behaviour of all solutions and one particular solution", "Medium", "Statement-based MCQ",
  r"Consider $\frac{dy}{dx} + 2xy = 2x$. Statement I: Every solution $y(x)$ of this equation tends to $0$ as $x \to \infty$. Statement II: The solution with $y(0) = 0$ satisfies $y(1) = 1 - \frac{1}{e}$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Sees the factor $e^{-x^2}$ in the general solution and concludes that the whole solution decays to $0$, overlooking the constant particular solution $y = 1$."),
   (ST_FF, r"Rejects Statement I correctly but solves $0 = 1 + C$ as $C = 1$, so $y(1) = 1 + \frac{1}{e}$ and Statement II is rejected."),
   (ST_TF, r"Takes $y = Ce^{-x^2}$, dropping the particular solution $1$; then every solution decays to $0$, and $y(0) = 0$ forces $y \equiv 0$, so $y(1) = 0$ and Statement II is rejected.")],
  r"The factor is $e^{x^2}$: $ye^{x^2} = \int 2xe^{x^2}dx = e^{x^2} + C$, so $y = 1 + Ce^{-x^2}$. Every solution tends to $1$, not $0$, so Statement I is false. With $y(0) = 0$, $C = -1$ and $y(1) = 1 - \frac{1}{e}$, so Statement II is true.",
  "Forgetting the particular (steady) part when judging long-run behaviour.",
  "U09-C-stmt-longrun", "Solve once, then judge a limit and a value.",
  check=_c022, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis", source_class="XII")


def _c023():
    yy = _ds(Eq(xp*Y(xp).diff(xp) + Y(xp), xp*cos(xp)), xp, {Y(pi): 0})
    return simplify(yy.subs(xp, pi/2))
q("U09-C-023", TOP_SOL, "Exact left side with integration by parts", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, satisfy $x\frac{dy}{dx} + y = x\cos x$ and $y(\pi) = 0$. Then $y\left(\frac{\pi}{2}\right)$ equals",
  r"$1 + \frac{2}{\pi}$",
  [(r"$1 - \frac{2}{\pi}$", r"Integrates $x\cos x$ as $x\sin x - \cos x$ (sign slip), so $C = -1$."),
   (r"$1 + \frac{\pi}{2}$", r"Gets $xy = x\sin x + \cos x + 1$ but forgets to divide by $x$ at $x = \frac{\pi}{2}$."),
   (r"$1$", r"Ignores the constant, taking $xy = x\sin x + \cos x$.")],
  r"The left side is $\frac{d}{dx}(xy)$, so $xy = \int x\cos x\,dx = x\sin x + \cos x + C$. At $x = \pi$: $0 = -1 + C$, so $C = 1$. At $x = \frac{\pi}{2}$: $\frac{\pi}{2}y = \frac{\pi}{2} + 0 + 1$, so $y = 1 + \frac{2}{\pi}$.",
  "Sign error in $\\int x\\cos x\\,dx$.",
  "U09-C-exact-lhs-trig", "Spot the exact derivative, integrate by parts, apply a condition.",
  check=_c023, values=[1 + 2/pi, 1 - 2/pi, 1 + pi/2, 1], source_class="XII")


def _c024():
    X = _ivp(-1, yv, yv, 0, 0)
    return simplify(X.subs(yv, 1))
q("U09-C-024", TOP_X, "Treating x as the dependent variable", "Medium", "Multi-step computation MCQ",
  r"A curve passes through the origin and satisfies $(x + y)\,dy = dx$. The value of $x$ on this curve where $y = 1$ is",
  r"$e - 2$",
  [(r"$\frac{1}{e}$", r"Writes $\frac{dx}{dy} + x = y$ (sign slip), giving $x = y - 1 + e^{-y}$."),
   (r"$e$", r"Integrates $\int ye^{-y}dy$ as $(y - 1)e^{-y}$, giving $x = y - 1 + e^{y}$."),
   (r"$\frac{e}{2}$", r"Does not multiply $y$ by the factor $e^{-y}$: $xe^{-y} = \frac{y^2}{2}$.")],
  r"As an equation in $x(y)$: $\frac{dx}{dy} - x = y$, factor $e^{-y}$. Then $xe^{-y} = \int ye^{-y}dy = -(y + 1)e^{-y} + C$, so $x = -y - 1 + Ce^{y}$. Through the origin, $C = 1$; at $y = 1$, $x = e - 2$.",
  "Trying to treat the equation as linear in $y$, or sign errors in integration by parts.",
  "U09-C-linx-sum", "Recognise linearity in $x$, then integrate by parts.",
  check=_c024, values=[E - 2, 1/E, E, E/2], source_class="XII")


def _c025():
    yy = _ds(Eq(Y(x).diff(x) + 2*x*Y(x), x*exp(-x**2)), x, {Y(0): 1})
    return simplify(yy.subs(x, 1))
q("U09-C-025", TOP_SOL, "Gaussian integrating factor", "Medium", "Multi-step computation MCQ",
  r"If $\frac{dy}{dx} + 2xy = xe^{-x^2}$ and $y(0) = 1$, then $y(1)$ equals",
  r"$\frac{3}{2e}$",
  [(r"$\frac{3}{2e} - \frac{1}{2e^2}$", r"Does not multiply $xe^{-x^2}$ by the factor: $ye^{x^2} = -\frac{1}{2}e^{-x^2} + \frac{3}{2}$."),
   (r"$\frac{1}{2e}$", r"Drops the constant, taking $ye^{x^2} = \frac{x^2}{2}$."),
   (r"$\frac{3e}{2}$", r"Finds $ye^{x^2} = \frac{x^2}{2} + 1$ but multiplies by $e^{x^2}$ instead of dividing.")],
  r"The factor is $e^{x^2}$, so $\frac{d}{dx}(ye^{x^2}) = x$ and $ye^{x^2} = \frac{x^2}{2} + C$. $y(0) = 1$ gives $C = 1$, so $y(1) = \frac{3/2}{e} = \frac{3}{2e}$.",
  "Not multiplying $Q$ by the integrating factor.",
  "U09-C-ivp-gauss", "Non-trivial factor $e^{x^2}$ that simplifies the right side.",
  check=_c025, values=[3/(2*E), 3/(2*E) - 1/(2*E**2), 1/(2*E), 3*E/2], source_class="XII")


def _c026():
    i = _ds(Eq(2*Y(t).diff(t) + 4*Y(t), 8), t, {Y(0): 0})
    steady = limit(i, t, oo)
    return simplify(solve(Eq(i, steady/2), t)[0])
q("U09-C-026", TOP_APP, "Growth of current in an RL circuit", "Medium", "Multi-step computation MCQ",
  r"The current $i$ in a circuit satisfies $2\frac{di}{dt} + 4i = 8$ for $t \ge 0$, with $i(0) = 0$. The time at which $i$ equals half of its limiting value as $t \to \infty$ is",
  r"$\frac{\log_e 2}{2}$",
  [(r"$\frac{\log_e 2}{4}$", r"Does not divide by the coefficient $2$ of $\frac{di}{dt}$, using $i = 2(1 - e^{-4t})$."),
   (r"$2\log_e 2$", r"Uses the exponent $-\frac{t}{2}$, inverting the ratio of the coefficients."),
   (r"$\log_e 2$", r"Reaches $e^{-2t} = \frac{1}{2}$ but solves it as $t = \log_e 2$.")],
  r"Standard form $\frac{di}{dt} + 2i = 4$, factor $e^{2t}$: $i = 2 + Ce^{-2t}$, and $i(0) = 0$ gives $i = 2(1 - e^{-2t})$. The limiting value is $2$; $i = 1$ when $e^{-2t} = \frac{1}{2}$, i.e. $t = \frac{\log_e 2}{2}$.",
  "Forgetting to reduce to standard form before reading the coefficient of $i$.",
  "U09-C-app-circuit", "Standard form, solve, limit, then solve for $t$.",
  check=_c026, values=[log(2)/2, log(2)/4, 2*log(2), log(2)], source_class="XII")


def _c027():
    f = _ds(Eq(Y(x).diff(x), 1 + Y(x)), x, {Y(0): 0})
    return simplify(f.subs(x, log(3)))
q("U09-C-027", TOP_SOL, "Integral equation converted to a linear equation", "Medium", "Multi-step computation MCQ",
  r"Let $f$ be a differentiable function satisfying $f(x) = x + \int_0^x f(t)\,dt$ for all real $x$. Then $f(\log_e 3)$ equals",
  r"$2$",
  [(r"$5$", r"Differentiates correctly but assumes $f(0) = 1$, giving $f = 2e^x - 1$."),
   (r"$\frac{2}{3}$", r"Differentiates to $f' = 1 - f$ (sign slip), giving $f = 1 - e^{-x}$."),
   (r"$3$", r"Solves only $f' = f$ with $f(0) = 1$, giving $f = e^x$.")],
  r"Differentiating, $f'(x) = 1 + f(x)$, and putting $x = 0$ in the given relation gives $f(0) = 0$. With factor $e^{-x}$: $f = -1 + Ce^x$ and $C = 1$, so $f(x) = e^x - 1$ and $f(\log_e 3) = 2$.",
  "Missing the initial condition hidden in the integral equation.",
  "U09-C-integral-eq", "Convert to a differential equation and extract the hidden initial value.",
  check=_c027, values=[2, 5, Rational(2, 3), 3], cognitive="Analysis",
  numerical=dict(question=r"Let $f$ be a differentiable function satisfying $f(x) = x + \int_0^x f(t)\,dt$ for all real $x$. Then the value of $f(\log_e 3)$ is", answer=2), source_class="XII")


def _c028():
    IF = xp**2*exp(xp)
    return simplify(diff(log(IF), xp))
q("U09-C-028", TOP_IF, "Coefficient recovered from the integrating factor", "Medium", "Inverse/parameter MCQ",
  r"For $x > 0$, the differential equation $\frac{dy}{dx} + P(x)\,y = Q(x)$ has integrating factor $x^2e^x$. Then $P(x)$ equals",
  r"$\frac{2}{x} + 1$",
  [(r"$(x^2 + 2x)e^x$", r"Differentiates the integrating factor itself instead of its logarithm."),
   (r"$2\log_e x + x$", r"Takes $\log_e(\text{IF})$ as $P$, forgetting to differentiate."),
   (r"$\frac{2}{x}$", r"Differentiates $\log_e(x^2)$ but loses the contribution of $e^x$.")],
  r"The integrating factor is $e^{\int P\,dx}$, so $\int P\,dx = \log_e(x^2e^x) = 2\log_e x + x$ and $P = \frac{2}{x} + 1$.",
  "Confusing the integrating factor with $P$ or with $\\int P\\,dx$.",
  "U09-C-if-reverse", "Reverse of the usual direction: log, then differentiate.",
  check=_c028, values=[2/xp + 1, (xp**2 + 2*xp)*exp(xp), 2*log(xp) + xp, 2/xp], cognitive="Understanding", source_class="XII")


def _c029():
    yy = _ds(Eq(xp**2*Y(xp).diff(xp) + xp*Y(xp), 1), xp, {Y(1): 0})
    crit = solve(diff(yy, xp), xp)
    return simplify(yy.subs(xp, crit[0]))
q("U09-C-029", TOP_SOL, "Maximum value of a particular solution", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $x > 0$, satisfy $x^2\frac{dy}{dx} + xy = 1$ and $y(1) = 0$. The maximum value of $y(x)$ on $(0, \infty)$ is",
  r"$\frac{1}{e}$",
  [(r"$e$", r"Finds the maximum at $x = e$ and reports the point instead of the value."),
   (r"$\frac{1}{4}$", r"Does not multiply $\frac{1}{x^2}$ by the factor $x$: $xy = 1 - \frac{1}{x}$, whose maximum of $y$ is at $x = 2$."),
   (r"$\frac{2}{e^2}$", r"Solves $y' = \frac{1 - \log_e x}{x^2} = 0$ as $\log_e x = 2$ and evaluates $y(e^2)$.")],
  r"Dividing by $x^2$: $\frac{dy}{dx} + \frac{y}{x} = \frac{1}{x^2}$, factor $x$. So $\frac{d}{dx}(xy) = \frac{1}{x}$, $xy = \log_e x + C$, and $y(1) = 0$ gives $C = 0$. Then $y = \frac{\log_e x}{x}$, $y' = \frac{1 - \log_e x}{x^2}$ vanishes at $x = e$, and the maximum is $\frac{1}{e}$.",
  "Reporting the location of a maximum instead of its value.",
  "U09-C-ivp-then-max", "Linear solve combined with a maximisation.",
  check=_c029, values=[1/E, E, Rational(1, 4), 2/E**2], source_class="XII")


def _c030():
    yy = _ivp(cot(x), 4*x/sin(x), x, pi/2, 0)
    return simplify(yy.subs(x, pi/6))
q("U09-C-030", TOP_SOL, "Cotangent coefficient with a condition at a quarter turn", "Medium", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $0 < x < \pi$, satisfy $\frac{dy}{dx} + y\cot x = 4x\csc x$ and $y\left(\frac{\pi}{2}\right) = 0$. Then $y\left(\frac{\pi}{6}\right)$ equals",
  r"$-\frac{8\pi^2}{9}$",
  [(r"$\frac{10\pi^2}{9}$", r"Finds $C = +\frac{\pi^2}{2}$ from $0 = \frac{\pi^2}{2} + C$, a sign slip."),
   (r"$-\frac{2\pi^2}{9}$", r"Reaches $y\sin x = 2x^2 - \frac{\pi^2}{2}$ but multiplies by $\sin\frac{\pi}{6}$ instead of dividing."),
   (r"$-\frac{16\pi^2}{9}$", r"Integrates $4x$ as $4x^2$, so $C = -\pi^2$.")],
  r"The factor is $\sin x$, and $\frac{d}{dx}(y\sin x) = 4x$, so $y\sin x = 2x^2 + C$. From $y\left(\frac{\pi}{2}\right) = 0$, $C = -\frac{\pi^2}{2}$. At $x = \frac{\pi}{6}$: $\frac{y}{2} = \frac{\pi^2}{18} - \frac{\pi^2}{2} = -\frac{4\pi^2}{9}$, so $y = -\frac{8\pi^2}{9}$.",
  "Dividing by the integrating factor incorrectly at the end.",
  "U09-C-ivp-cot", "Trigonometric factor and careful arithmetic with $\\pi^2$.",
  check=_c030, values=[-8*pi**2/9, 10*pi**2/9, -2*pi**2/9, -16*pi**2/9], source_class="XII")


def _c031():
    k = Symbol('k')
    yy = _ivp(1/xp, k, xp, 1, 0)
    return solve(Eq(yy.subs(xp, 2), 3), k)[0]
q("U09-C-031", TOP_SOL, "Parameter fixed by two values of the solution", "Medium", "Inverse/parameter MCQ",
  r"Let $k$ be a real constant and let $y = y(x)$, $x > 0$, satisfy $\frac{dy}{dx} + \frac{y}{x} = k$ with $y(1) = 0$. If $y(2) = 3$, then $k$ equals",
  r"$4$",
  [(r"$6$", r"Does not multiply $k$ by the factor $x$: $xy = kx - k$, so $2 \cdot 3 = k$."),
   (r"$2$", r"Finds $xy = \frac{kx^2}{2} - \frac{k}{2}$ but forgets to divide by $x$, so $\frac{3k}{2} = 3$."),
   (r"$3$", r"Drops the constant, taking $xy = \frac{kx^2}{2}$, so $6 = 2k$.")],
  r"With factor $x$: $xy = \frac{kx^2}{2} + C$; $y(1) = 0$ gives $C = -\frac{k}{2}$. At $x = 2$: $6 = 2k - \frac{k}{2} = \frac{3k}{2}$, so $k = 4$.",
  "Not multiplying the constant right side by the integrating factor.",
  "U09-C-param-two-values", "Reverse problem: parameter from two conditions.",
  check=_c031, values=[4, 6, 2, 3], cognitive="Analysis",
  numerical=dict(question=r"Let $k$ be a real constant and let $y = y(x)$, $x > 0$, satisfy $\frac{dy}{dx} + \frac{y}{x} = k$ with $y(1) = 0$. If $y(2) = 3$, then the value of $k$ is", answer=4), source_class="XII")


def _c032():
    s1 = Poly(-x*sin(yv) + cos(yv), x).degree() <= 1
    s2 = simplify(exp(integrate(tan(x), x)) - 1/cos(x)) == 0
    return (bool(s1), bool(s2))
q("U09-C-032", TOP_X, "Statements on linearity in x and integrating factors", "Medium", "Statement-based MCQ",
  r"Statement I: The equation $\frac{dx}{dy} + x\sin y = \cos y$ is a linear differential equation in $x$ (with $x$ as a function of $y$). Statement II: On $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$, an integrating factor of $\frac{dy}{dx} + y\tan x = \sec x$ is $\sec x$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Integrates $\tan x$ as $\log_e|\cos x|$, getting the factor $\cos x$ and rejecting Statement II."),
   (ST_FT, r"Thinks the presence of $\sin y$ and $\cos y$ makes the equation non-linear, although they are functions of the independent variable only."),
   (ST_FF, r"Makes both of the above slips.")],
  r"In $\frac{dx}{dy} + (\sin y)x = \cos y$, the unknown $x$ and its derivative appear to the first power with coefficients depending only on $y$, so it is linear in $x$; Statement I is true. Since $\int \tan x\,dx = -\log_e\cos x$, the factor is $e^{-\log_e\cos x} = \sec x$; Statement II is true.",
  "Judging linearity by the independent variable instead of the unknown function.",
  "U09-C-stmt-linear-x", "Two short checks of definition and factor.",
  check=_c032, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Understanding", source_class="XII")


def _c033():
    k = Symbol('k', positive=True)
    S = Symbol('S', real=True)
    T = _ds(Eq(Y(t).diff(t), -k*(Y(t) - S)), t, {Y(0): 100})
    assert simplify(T.diff(t) + k*(T - S)) == 0
    sols = solve([Eq(T.subs(t, 10), 70), Eq(T.subs(t, 20), 52)], [S, k], dict=True)
    good = [s[S] for s in sols if s[k].is_positive]
    assert len(good) == 1
    return simplify(good[0])
q("U09-C-033", TOP_APP, "Cooling with an unknown surrounding temperature", "Medium", "Inverse/parameter MCQ",
  r"A body is placed in a room whose temperature $S$ (in $^\circ\mathrm{C}$) stays constant. The temperature $T$ (in $^\circ\mathrm{C}$) of the body at time $t$ minutes satisfies $\frac{dT}{dt} = -k(T - S)$ for some constant $k > 0$. If $T = 100$ at $t = 0$, $T = 70$ at $t = 10$ and $T = 52$ at $t = 20$, then $S$ equals",
  r"$25$",
  [(r"$7$", r"Sees that the falls $30, 18, \ldots$ form a GP with ratio $\frac{3}{5}$ but subtracts the whole sum $\frac{18}{1 - \frac{3}{5}} = 45$ from $52$, counting again the fall of $18$ already made, so $S = 52 - 45$."),
   (r"$10$", r"Takes the decay factor per $10$ minutes as $\frac{70}{100} = \frac{7}{10}$ from the temperatures themselves, then solves $52 - S = \frac{7}{10}(70 - S)$."),
   (r"$46$", r"Assumes each $10$-minute fall is $12$ less than the previous one ($30, 18, 6$), so the temperature levels off at $52 - 6$.")],
  r"With integrating factor $e^{kt}$, $T = S + (100 - S)e^{-kt}$, so the excess $T - S$ is multiplied by the same factor $r = e^{-10k}$ every $10$ minutes: $70 - S = (100 - S)r$ and $52 - S = (70 - S)r$. Eliminating $r$, $(70 - S)^2 = (100 - S)(52 - S)$, i.e. $4900 - 140S = 5200 - 152S$, so $12S = 300$ and $S = 25$. Then $r = \frac{45}{75} = \frac{3}{5} < 1$, consistent with $k > 0$.",
  "Measuring the decay ratio on the temperatures instead of on their excess over the surroundings.",
  "U09-C-app-cooling-ambient", "Solve the linear equation, see the excess decays by a common ratio, and eliminate $k$ to find the unknown surroundings; two unknowns from three readings.",
  check=_c033, values=[25, 7, 10, 46], cognitive="Analysis",
  numerical=dict(question=r"A body is placed in a room whose temperature $S$ (in $^\circ\mathrm{C}$) stays constant. The temperature $T$ (in $^\circ\mathrm{C}$) of the body at time $t$ minutes satisfies $\frac{dT}{dt} = -k(T - S)$ for some constant $k > 0$. If $T = 100$ at $t = 0$, $T = 70$ at $t = 10$ and $T = 52$ at $t = 20$, then the value of $S$ is", answer=25), source_class="XII")


def _c034():
    yy = _ds(Eq(Y(x).diff(x) + Y(x), x**2), x, {Y(0): 2})
    return simplify(yy.subs(x, 3))
q("U09-C-034", TOP_SOL, "Initial condition that kills the exponential term", "Medium", "Multi-step computation MCQ",
  r"If $y = y(x)$ satisfies $\frac{dy}{dx} + y = x^2$ and $y(0) = 2$, then $y(3)$ equals",
  r"$5$",
  [(r"$17$", r"Integrates $x^2e^x$ by parts with a sign slip, getting the particular part $x^2 + 2x + 2$."),
   (r"$3 + 2e^{-3}$", r"Uses the particular part $x^2 - 2x$, losing the constant $2$, so $C = 2$."),
   (r"$9 + 2e^{-3}$", r"Uses only $x^2$ as the particular part, so $C = 2$.")],
  r"With factor $e^x$: $ye^x = \int x^2e^x dx = (x^2 - 2x + 2)e^x + C$, so $y = x^2 - 2x + 2 + Ce^{-x}$. $y(0) = 2$ gives $C = 0$, so $y = x^2 - 2x + 2$ and $y(3) = 5$.",
  "Errors in repeated integration by parts.",
  "U09-C-ivp-quadratic", "Two integrations by parts and noticing $C = 0$.",
  check=_c034, values=[5, 17, 3 + 2*exp(-3), 9 + 2*exp(-3)],
  numerical=dict(question=r"If $y = y(x)$ satisfies $\frac{dy}{dx} + y = x^2$ and $y(0) = 2$, then the value of $y(3)$ is", answer=5), source_class="XII")


def _c035():
    yy = _ivp(2*x/(1 + x**2), 1/(1 + x**2)**2, x, 0, 0)
    return simplify(yy.subs(x, 1))
q("U09-C-035", TOP_SOL, "Integrating factor 1 + x squared", "Medium", "Multi-step computation MCQ",
  r"If $(1 + x^2)\frac{dy}{dx} + 2xy = \frac{1}{1 + x^2}$ and $y(0) = 0$, then $y(1)$ equals",
  r"$\frac{\pi}{8}$",
  [(r"$\frac{\pi}{4}$", r"Finds $(1 + x^2)y = \tan^{-1} x$ but forgets to divide by $1 + x^2 = 2$."),
   (r"$\frac{1}{8} + \frac{\pi}{16}$", r"Does not multiply $\frac{1}{(1+x^2)^2}$ by the factor and integrates it directly: $\int \frac{dx}{(1+x^2)^2} = \frac{x}{2(1+x^2)} + \frac{1}{2}\tan^{-1} x$."),
   (r"$\frac{\pi}{16}$", r"Divides $\tan^{-1} x$ by $(1 + x^2)^2 = 4$ instead of $1 + x^2$.")],
  r"The left side is $\frac{d}{dx}\left((1 + x^2)y\right)$, so $(1 + x^2)y = \tan^{-1} x + C$ and $y(0) = 0$ gives $C = 0$. Then $y(1) = \frac{\pi/4}{2} = \frac{\pi}{8}$.",
  "Not noticing that the left side is already an exact derivative.",
  "U09-C-exact-lhs-atan", "Recognise the factor $1 + x^2$, then one standard integral.",
  check=_c035, values=[pi/8, pi/4, Rational(1, 8) + pi/16, pi/16], source_class="XII")


# ================================================================ DIFFICULT
def _c036():
    X = _ivp(1/yp**2, 1/yp**3, yp, 1, 1)
    return simplify(X.subs(yp, 2))
q("U09-C-036", TOP_X, "Linear in x with factor exp(-1/y)", "Difficult", "Multi-step computation MCQ",
  r"Let $x = x(y)$, $y > 0$, satisfy $y^2\,dx + \left(x - \frac{1}{y}\right)dy = 0$ with $x = 1$ when $y = 1$. Then the value of $x$ when $y = 2$ is",
  r"$\frac{3}{2} - \frac{1}{\sqrt{e}}$",
  [(r"$\frac{3}{2} + \frac{1}{\sqrt{e}}$", r"Gets $x = 1 + \frac{1}{y} + Ce^{1/y}$ but solves $1 = 2 + Ce$ as $C = \frac{1}{e}$."),
   (r"$\frac{1}{2} + \sqrt{e}$", r"Takes the factor $e^{1/y}$ (sign slip in $\int \frac{dy}{y^2}$), leading to $x = 1 - \frac{1}{y} + Ce^{-1/y}$ with $C = e$."),
   (r"$\frac{1}{2}$", r"With $t = \frac{1}{y}$, evaluates $-\int te^{-t}dt$ as $te^{-t}$, so $x = \frac{1}{y} + Ce^{1/y}$ with $C = 0$.")],
  r"$\frac{dx}{dy} + \frac{x}{y^2} = \frac{1}{y^3}$ has factor $e^{-1/y}$. With $t = \frac{1}{y}$, $\int \frac{e^{-1/y}}{y^3}dy = -\int te^{-t}dt = (t + 1)e^{-t}$, so $x = 1 + \frac{1}{y} + Ce^{1/y}$. $x(1) = 1$ gives $C = -\frac{1}{e}$, and $x(2) = \frac{3}{2} - e^{\frac{1}{2} - 1} = \frac{3}{2} - \frac{1}{\sqrt{e}}$.",
  "Sign errors in the exponent of the integrating factor.",
  "U09-C-linx-recip", "Linear in $x$, a non-obvious factor, substitution plus integration by parts.",
  check=_c036, values=[Rational(3, 2) - exp(-Rational(1, 2)), Rational(3, 2) + exp(-Rational(1, 2)), Rational(1, 2) + exp(Rational(1, 2)), Rational(1, 2)],
  cognitive="Analysis", source_class="XII")


def _c037():
    yy = _ds(Eq(Y(x).diff(x) + 2*Y(x), 5*sin(x)), x, {Y(0): -1})
    return simplify(yy.subs(x, pi/2))
q("U09-C-037", TOP_SOL, "Sinusoidal forcing where the transient vanishes", "Difficult", "Multi-step computation MCQ",
  r"If $y = y(x)$ satisfies $\frac{dy}{dx} + 2y = 5\sin x$ and $y(0) = -1$, then $y\left(\frac{\pi}{2}\right)$ equals",
  r"$2$",
  [(r"$2 - 2e^{-\pi}$", r"Gets the particular part as $2\sin x + \cos x$ (sign slip), so $C = -2$."),
   (r"$1 + e^{-\pi}$", r"Swaps the coefficients, using $\sin x - 2\cos x$ as the particular part, so $C = 1$."),
   (r"$-2$", r"Solves $\frac{dy}{dx} - 2y = 5\sin x$ instead, whose particular part is $-2\sin x - \cos x$.")],
  r"With factor $e^{2x}$, $\int 5e^{2x}\sin x\,dx = e^{2x}(2\sin x - \cos x)$, so $y = 2\sin x - \cos x + Ce^{-2x}$. $y(0) = -1 + C = -1$ gives $C = 0$; hence $y\left(\frac{\pi}{2}\right) = 2$.",
  "Errors in $\\int e^{ax}\\sin x\\,dx$.",
  "U09-C-ivp-sin-forcing", "Cyclic integration by parts plus the observation that $C = 0$.",
  check=_c037, values=[2, 2 - 2*exp(-pi), 1 + exp(-pi), -2], source_class="XII")


def _c038():
    IF = 1/cos(x) + tan(x)
    assert simplify(diff(log(IF), x) - 1/cos(x)) == 0   # IF = exp(int sec x)
    F = integrate(expand(tan(x)*IF), x)
    yy = (F + Cs)/IF
    c = solve(Eq(yy.subs(x, 0), 1), Cs)[0]
    return simplify(yy.subs(Cs, c).subs(x, pi/4))
q("U09-C-038", TOP_SOL, "Integrating factor sec x + tan x", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, $-\frac{\pi}{2} < x < \frac{\pi}{2}$, satisfy $\frac{dy}{dx} + y\sec x = \tan x$ and $y(0) = 1$. Then $y\left(\frac{\pi}{4}\right)$ equals",
  r"$1 - \frac{\pi(\sqrt{2} - 1)}{4}$",
  [(r"$1$", r"Takes $\tan x(\sec x + \tan x) = \sec x\tan x + \sec^2 x$, losing the $-1$ from $\tan^2 x = \sec^2 x - 1$."),
   (r"$1 + \frac{\pi(\sqrt{2} - 1)}{4}$", r"Integrates $-1$ as $+x$, so $y(\sec x + \tan x) = \sec x + \tan x + x$."),
   (r"$1 - \frac{\pi(\sqrt{2} + 1)}{4}$", r"Divides $\frac{\pi}{4}$ by $\sqrt{2} - 1$ instead of $\sqrt{2} + 1$ when rationalising.")],
  r"The factor is $e^{\int \sec x\,dx} = \sec x + \tan x$. Then $\frac{d}{dx}\left(y(\sec x + \tan x)\right) = \sec x\tan x + \tan^2 x = \sec x\tan x + \sec^2 x - 1$, so $y(\sec x + \tan x) = \sec x + \tan x - x + C$ and $y(0) = 1$ gives $C = 0$. At $\frac{\pi}{4}$: $y = 1 - \frac{\pi/4}{\sqrt{2} + 1} = 1 - \frac{\pi(\sqrt{2} - 1)}{4}$.",
  "Forgetting $\\tan^2 x = \\sec^2 x - 1$ when integrating.",
  "U09-C-ivp-sec-tan", "Unusual factor, trigonometric identity, rationalisation.",
  check=_c038, values=[1 - pi*(sqrt(2) - 1)/4, 1, 1 + pi*(sqrt(2) - 1)/4, 1 - pi*(sqrt(2) + 1)/4],
  cognitive="Analysis", source_class="XII")


def _c039():
    u = _ivp(1, x, x, 0, 0)        # u = sin y
    return asin(simplify(u.subs(x, 1)))
q("U09-C-039", TOP_SOL, "Substitution sin y reducing to a linear equation", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$, with $-\frac{\pi}{2} \le y \le \frac{\pi}{2}$, satisfy $\cos y\,\frac{dy}{dx} + \sin y = x$ and $y(0) = 0$. Then $y(1)$ equals",
  r"$\sin^{-1}\frac{1}{e}$",
  [(r"$-\sin^{-1}\frac{1}{e}$", r"Gets $\sin y = x - 1 + Ce^{-x}$ but solves $0 = -1 + C$ as $C = -1$."),
   (r"$0$", r"Drops the constant of integration, taking $\sin y = x - 1$, so $\sin y = 0$ at $x = 1$."),
   (r"$\sin^{-1}\frac{1}{2e}$", r"Does not multiply $x$ by the factor $e^x$: $e^x\sin y = \frac{x^2}{2}$.")],
  r"Put $u = \sin y$, so $\frac{du}{dx} = \cos y\frac{dy}{dx}$ and $\frac{du}{dx} + u = x$. With factor $e^x$, $ue^x = (x - 1)e^x + C$, so $u = x - 1 + Ce^{-x}$; $u(0) = 0$ gives $C = 1$. At $x = 1$, $\sin y = \frac{1}{e}$, and with $y \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$, $y(1) = \sin^{-1}\frac{1}{e}$.",
  "Not spotting that $\\cos y\\,\\frac{dy}{dx}$ is the derivative of $\\sin y$.",
  "U09-C-subst-sin", "Substitution to reach a linear form, then a standard solve.",
  check=_c039, values=[asin(1/E), -asin(1/E), 0, asin(1/(2*E))], cognitive="Analysis", source_class="XII")


def _c040():
    gen = _ds(Eq(Y(x).diff(x) - Y(x), sin(x)), x, None).subs(Symbol('C1'), Cs)
    # bounded on [0, oo) requires coefficient of e^x to vanish
    c = solve(Eq(expand(gen).coeff(exp(x)), 0), Cs)[0]
    return simplify(gen.subs(Cs, c).subs(x, 0))
q("U09-C-040", TOP_SOL, "Initial value for a bounded solution", "Difficult", "Inverse/parameter MCQ",
  r"Consider $\frac{dy}{dx} - y = \sin x$. The value of $y(0)$ for which the solution $y(x)$ remains bounded on $[0, \infty)$ is",
  r"$-\frac{1}{2}$",
  [(r"$\frac{1}{2}$", r"Gets the particular part as $\frac{\sin x + \cos x}{2}$, a sign slip in the cyclic integration."),
   (r"$-1$", r"Takes the particular part as $-(\sin x + \cos x)$, losing the factor $\frac{1}{2}$."),
   (r"$0$", r"Assumes the bounded solution needs $C = 0$ and hence $y(0) = 0$, forgetting the particular part at $x = 0$.")],
  r"With factor $e^{-x}$, $ye^{-x} = \int e^{-x}\sin x\,dx = -\frac{e^{-x}(\sin x + \cos x)}{2} + C$, so $y = Ce^x - \frac{\sin x + \cos x}{2}$. The term $Ce^x$ is unbounded unless $C = 0$, so the bounded solution is $y = -\frac{\sin x + \cos x}{2}$ and $y(0) = -\frac{1}{2}$.",
  "Equating a zero constant with a zero initial value.",
  "U09-C-bounded-solution", "Combines solving with an asymptotic condition; reversed unknown.",
  check=_c040, values=[-Rational(1, 2), Rational(1, 2), -1, 0], cognitive="Analysis", source_class="XII")


def _c041():
    y1 = _ds(Eq(Y(x).diff(x) + Y(x), 1), x, {Y(0): 0})
    a = y1.subs(x, 1)
    y2 = _ds(Eq(Y(x).diff(x) + Y(x), 0), x, {Y(1): a})
    return simplify(y2.subs(x, 2))
q("U09-C-041", TOP_SOL, "Piecewise forcing with a continuous solution", "Difficult", "Multi-step computation MCQ",
  r"Let $g(x) = 1$ for $0 \le x \le 1$ and $g(x) = 0$ for $x > 1$. Let $y = y(x)$ be continuous on $[0, \infty)$ with $y(0) = 0$ and $\frac{dy}{dx} + y = g(x)$ for all $x \ne 1$. Then $y(2)$ equals",
  r"$\frac{e - 1}{e^2}$",
  [(r"$1 - \frac{1}{e^2}$", r"Uses $y = 1 - e^{-x}$ for all $x$, ignoring the change in $g$ at $x = 1$."),
   (r"$\frac{e - 1}{e}$", r"Thinks $y$ stays constant once $g = 0$, so $y(2) = y(1)$."),
   (r"$e - 1$", r"Writes the solution for $x > 1$ as $y(1)e^{x - 1}$, a sign slip in the exponent.")],
  r"On $[0, 1]$: $y = 1 - e^{-x}$, so $y(1) = 1 - \frac{1}{e}$. For $x > 1$: $\frac{dy}{dx} + y = 0$ gives $y = y(1)e^{-(x - 1)}$ by continuity. Hence $y(2) = \left(1 - \frac{1}{e}\right)\frac{1}{e} = \frac{e - 1}{e^2}$.",
  "Not restarting the solution when the forcing changes.",
  "U09-C-piecewise-forcing", "Two linear solves joined by continuity.",
  check=_c041, values=[(E - 1)/E**2, 1 - exp(-2), (E - 1)/E, E - 1], cognitive="Analysis", source_class="XII")


def _c042():
    k = Symbol('k')
    f = _ivp(-1, k, x, 0, 1)
    return solve(Eq(integrate(f, (x, 0, 1)), k), k)[0]
q("U09-C-042", TOP_SOL, "Linear equation containing a definite integral", "Difficult", "Multi-step computation MCQ",
  r"Let $f$ be differentiable with $f(0) = 1$ and $f'(x) = f(x) + \int_0^1 f(t)\,dt$ for all real $x$. Then $\int_0^1 f(t)\,dt$ equals",
  r"$\frac{e - 1}{3 - e}$",
  [(r"$1$", r"Takes the particular part as $+k$ (sign slip), $f = (1 - k)e^x + k$, which forces $(1 - k)(e - 1) = 0$."),
   (r"$\frac{e - 1}{2}$", r"Uses $f = Ce^x - k$ with $C = 1$, forgetting that $f(0) = 1$ gives $C = 1 + k$."),
   (r"$\frac{e}{2 - e}$", r"Evaluates $\int_0^1 e^x\,dx$ as $e$ instead of $e - 1$.")],
  r"Let $k = \int_0^1 f(t)\,dt$, a constant. Then $f' - f = k$, so $f = Ce^x - k$, and $f(0) = 1$ gives $C = 1 + k$. Integrating, $k = (1 + k)(e - 1) - k$, so $k(3 - e) = e - 1$ and $k = \frac{e - 1}{3 - e}$.",
  "Not treating the definite integral as an unknown constant.",
  "U09-C-integral-const", "Unknown constant inside the equation, solved self-consistently.",
  check=_c042, values=[(E - 1)/(3 - E), 1, (E - 1)/2, E/(2 - E)], cognitive="Analysis", source_class="XII")


def _c043():
    X = _ivp(1/(1 + yv**2), exp(atan(yv))/(1 + yv**2), yv, 0, 1)
    return simplify(X.subs(yv, 1))
q("U09-C-043", TOP_X, "Linear in x with exponential of inverse tangent", "Difficult", "Multi-step computation MCQ",
  r"Let $x = x(y)$ satisfy $(1 + y^2) + \left(x - e^{\tan^{-1} y}\right)\frac{dy}{dx} = 0$ with $x = 1$ when $y = 0$. Then the value of $x$ when $y = 1$ is",
  r"$\frac{e^{\pi/4} + e^{-\pi/4}}{2}$",
  [(r"$e^{\pi/4}$", r"Integrates $e^{2t}$ as $e^{2t}$ (losing the $\frac{1}{2}$), so $xe^t = e^{2t}$ and $x = e^t$."),
   (r"$\frac{e^{\pi/4} - e^{-\pi/4}}{2}$", r"Gets $xe^t = \frac{e^{2t}}{2} + C$ but solves $1 = \frac{1}{2} + C$ as $C = -\frac{1}{2}$."),
   (r"$\left(1 + \frac{\pi}{4}\right)e^{\pi/4}$", r"Uses the factor $e^{-t}$ (sign slip), getting $xe^{-t} = t + 1$.")],
  r"Rewrite as $\frac{dx}{dy} + \frac{x}{1 + y^2} = \frac{e^{\tan^{-1} y}}{1 + y^2}$, with factor $e^{\tan^{-1} y}$. Putting $t = \tan^{-1} y$: $xe^t = \int e^{2t}dt = \frac{e^{2t}}{2} + C$; $x = 1$ at $t = 0$ gives $C = \frac{1}{2}$. So $x = \frac{e^t + e^{-t}}{2}$, and at $y = 1$, $t = \frac{\pi}{4}$.",
  "Not inverting $\\frac{dy}{dx}$ to see linearity in $x$.",
  "U09-C-linx-exp-atan", "Invert the derivative, identify linearity in $x$, substitute.",
  check=_c043, values=[(exp(pi/4) + exp(-pi/4))/2, exp(pi/4), (exp(pi/4) - exp(-pi/4))/2, (1 + pi/4)*exp(pi/4)],
  cognitive="Analysis", source_class="XII")


def _c044():
    # x-intercept of tangent: x - y dx/dy = y^2, curve through (2, 1)
    X = _ivp(-1/yp, -yp, yp, 1, 2)
    crit = solve(diff(X, yp), yp)
    return simplify(X.subs(yp, crit[0]))
q("U09-C-044", TOP_APP, "Curve from an x-intercept condition, then an extremum", "Difficult", "Multi-step computation MCQ",
  r"A curve lies in the region $y > 0$ and passes through $(2, 1)$. For every point $P(x, y)$ on it, the tangent at $P$ meets the $x$-axis at the point $(y^2, 0)$. The greatest value of $x$ for points on this curve is",
  r"$\frac{9}{4}$",
  [(r"$\frac{5\sqrt{15}}{9}$", r"Does not multiply $-y$ by the factor $\frac{1}{y}$: $\frac{x}{y} = -\frac{y^2}{2} + \frac{5}{2}$, whose maximum $x$ is at $y = \sqrt{\frac{5}{3}}$."),
   (r"$\frac{3}{2}$", r"Finds the vertex of $x = 3y - y^2$ at $y = \frac{3}{2}$ and reports that ordinate."),
   (r"$\frac{25}{16}$", r"Substitutes the point as $x = 1$, $y = 2$, so $C = \frac{5}{2}$ and the maximum is $\frac{C^2}{4}$.")],
  r"The tangent at $P$ meets the $x$-axis at $x - y\frac{dx}{dy}$, so $x - y\frac{dx}{dy} = y^2$, i.e. $\frac{dx}{dy} - \frac{x}{y} = -y$. With factor $\frac{1}{y}$, $\frac{x}{y} = -y + C$; through $(2, 1)$, $C = 3$. So $x = 3y - y^2 = \frac{9}{4} - \left(y - \frac{3}{2}\right)^2$, greatest at $y = \frac{3}{2}$, giving $\frac{9}{4}$.",
  "Not recognising that the intercept condition is linear in $x$ as a function of $y$.",
  "U09-C-tangent-x-intercept", "Geometry, linear in $x$, then an extremum.",
  check=_c044, values=[Rational(9, 4), 5*sqrt(15)/9, Rational(3, 2), Rational(25, 16)], cognitive="Analysis",
  numerical=dict(question=r"A curve lies in the region $y > 0$ and passes through $(2, 1)$. For every point $P(x, y)$ on it, the tangent at $P$ meets the $x$-axis at the point $(y^2, 0)$. If $M$ is the greatest value of $x$ for points on this curve, then $4M$ is", answer=9), source_class="XII")


def _c045():
    yy = _ds(Eq(Y(x).diff(x) + Y(x)*cos(x), sin(x)*cos(x)), x, {Y(0): 0})
    return simplify(yy.subs(x, pi/2))
q("U09-C-045", TOP_SOL, "Factor exp(sin x) with substitution", "Difficult", "Multi-step computation MCQ",
  r"If $\frac{dy}{dx} + y\cos x = \sin x\cos x$ and $y(0) = 0$, then $y\left(\frac{\pi}{2}\right)$ equals",
  r"$\frac{1}{e}$",
  [(r"$2 - \frac{1}{e}$", r"Integrates $\int se^s ds$ as $(s + 1)e^s$, giving $y = \sin x + 1 + Ce^{-\sin x}$ with $C = -1$."),
   (r"$0$", r"Drops the constant, taking $y = \sin x - 1$ and evaluating at $\frac{\pi}{2}$."),
   (r"$e$", r"Divides by the factor wrongly, writing $y = \sin x - 1 + e^{\sin x}$.")],
  r"The factor is $e^{\sin x}$. With $s = \sin x$, $ye^{s} = \int se^s ds = (s - 1)e^s + C$, so $y = \sin x - 1 + Ce^{-\sin x}$. $y(0) = 0$ gives $C = 1$, and $y\left(\frac{\pi}{2}\right) = 1 - 1 + e^{-1} = \frac{1}{e}$.",
  "Sign slip in $\\int se^s\\,ds$.",
  "U09-C-ivp-exp-sin", "Factor $e^{\\sin x}$, substitution, integration by parts.",
  check=_c045, values=[1/E, 2 - 1/E, 0, E], source_class="XII")


def _c046():
    yy = _ds(Eq(Y(x).diff(x) + Y(x), 3*x), x, {Y(0): 1})
    crit = solve(diff(yy, x), x)
    return simplify(yy.subs(x, crit[0]))
q("U09-C-046", TOP_SOL, "Minimum value of a particular solution", "Difficult", "Multi-step computation MCQ",
  r"Let $y = y(x)$ satisfy $\frac{dy}{dx} + y = 3x$ for all real $x$, with $y(0) = 1$. The minimum value of $y(x)$ over $\mathbb{R}$ is",
  r"$3\log_e\frac{4}{3}$",
  [(r"$\log_e\frac{4}{3}$", r"Finds the minimiser $x = \log_e\frac{4}{3}$ and reports it as the minimum value."),
   (r"$3\log_e\frac{4}{3} - 3$", r"Drops the term $4e^{-x}$ when evaluating $y$ at $x = \log_e\frac{4}{3}$."),
   (r"$-3\log_e 3$", r"Takes $C = 1$ (equal to $y(0)$), so $y = 3x - 3 + e^{-x}$, minimised at $x = -\log_e 3$ where $y = -3\log_e 3 - 3 + 3$.")],
  r"With factor $e^x$, $ye^x = \int 3xe^x\,dx = (3x - 3)e^x + C$, so $y = 3x - 3 + Ce^{-x}$, and $y(0) = 1$ gives $C = 4$. Then $y' = 3 - 4e^{-x} = 0$ at $x = \log_e\frac{4}{3}$, where $4e^{-x} = 3$, so the minimum is $3\log_e\frac{4}{3} - 3 + 3 = 3\log_e\frac{4}{3}$ (and $y \to \infty$ as $x \to \pm\infty$).",
  "Confusing the minimiser with the minimum value.",
  "U09-C-ivp-then-min", "Solve, then a calculus extremum with a non-obvious simplification.",
  check=_c046, values=[3*log(Rational(4, 3)), log(Rational(4, 3)), 3*log(Rational(4, 3)) - 3, -3*log(3)],
  cognitive="Analysis", source_class="XII")
