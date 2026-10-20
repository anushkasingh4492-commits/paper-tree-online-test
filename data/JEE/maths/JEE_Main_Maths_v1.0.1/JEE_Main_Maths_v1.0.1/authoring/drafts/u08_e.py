import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x', real=True)
y = Symbol('y', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_UNDER = "Area under a curve"
TOP_LP = "Area between a line and a curve"
TOP_PP = "Area between two curves"
TOP_CE = "Areas involving circles and ellipses"
TOP_MOD = "Areas with modulus curves and inequalities"
TOP_PAR = "Parameter from a given area"


def _pieces(expr, a, b, v):
    """Split [a, b] at the zeros of every Abs argument and of the expression itself."""
    pts = {sympify(a), sympify(b)}
    for ab in expr.atoms(Abs):
        pts |= set(solveset(ab.args[0], v, Interval(a, b)))
    pts = sorted(pts, key=lambda t: float(t))
    out = []
    for p, r in zip(pts, pts[1:]):
        m = (p + r) / 2
        g = expr.replace(Abs, lambda u: u * sign(u.subs(v, m)))
        sub = {p, r} | set(solveset(g, v, Interval(p, r)))
        sub = sorted(sub, key=lambda t: float(t))
        for s, t in zip(sub, sub[1:]):
            out.append((g, s, t))
    return out


def area(expr, a, b, v=x):
    """Geometric area between the graph of expr and the axis over [a, b]."""
    expr = sympify(expr)
    tot = 0
    for g, s, t in _pieces(expr, a, b, v):
        tot += Abs(integrate(g, (v, s, t)))
    return nsimplify(simplify(tot)) if tot.is_number and not tot.has(pi, E, log) else simplify(tot)


def real_roots(expr, v=x):
    return sorted(solveset(expr, v, S.Reals), key=lambda t: float(t))


# ================================================================ EASY
# ---------------------------------------------------------------- 001
q("U08-E-001", TOP_UNDER, "Area under a parabola between two ordinates", "Easy", "Single-step computation MCQ",
  r"The area of the region bounded by the curve $y = x^2$, the $x$-axis and the lines $x = 1$ and $x = 3$ is",
  r"$\frac{26}{3}$",
  [(r"$26$", r"Uses $x^3$ as the antiderivative of $x^2$, getting $27 - 1 = 26$."),
   (r"$9$", r"Evaluates $\frac{x^3}{3}$ at the upper limit only: $\frac{27}{3} = 9$."),
   (r"$8$", r"Subtracts the integrand values $3^2 - 1^2 = 8$ in place of the antiderivative values.")],
  r"The curve lies above the $x$-axis, so the area is $\int_1^3 x^2\,dx = \left[\frac{x^3}{3}\right]_1^3 = 9 - \frac{1}{3} = \frac{26}{3}$.",
  "Evaluating the antiderivative at only one limit, or using the integrand instead of the antiderivative.",
  "U08-E-under-poly", "One definite integral of a power.",
  check=lambda: area(x**2, 1, 3), values=[Rational(26, 3), 26, 9, 8], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 002
q("U08-E-002", TOP_LP, "Parabola and its latus rectum", "Easy", "Single-step computation MCQ",
  r"The area of the region bounded by the parabola $y^2 = 12x$ and its latus rectum is",
  r"$24$",
  [(r"$12$", r"Integrates only the upper branch, $\int_0^3 \sqrt{12x}\,dx = 12$, and does not double for the part below the axis."),
   (r"$36$", r"Takes the enclosing rectangle, latus rectum length $12$ times the distance $3$ from the vertex, instead of the parabolic region."),
   (r"$8$", r"Uses $\frac{8a}{3}$ with $a = 3$ in place of $\frac{8a^2}{3}$.")],
  r"Here $4a = 12$, so $a = 3$ and the latus rectum is $x = 3$. By symmetry the area is $2\int_0^3 \sqrt{12x}\,dx = 2\cdot 2\sqrt{3}\cdot\frac{2}{3}\cdot 3^{3/2} = 2\cdot 12 = 24$, which matches $\frac{8a^2}{3} = 24$.",
  "Forgetting the part of the region below the axis of the parabola.",
  "U08-E-latus-rectum", "One symmetric integral of $\\sqrt{x}$.",
  check=lambda: 2 * area(sqrt(12 * x), 0, solve(Eq(4 * Symbol('a'), 12))[0]),
  values=[24, 12, 36, 8], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region bounded by the parabola $y^2 = 12x$ and its latus rectum is", answer=24))

# ---------------------------------------------------------------- 003
def _c003():
    a, b = real_roots(x + 2 - x**2)
    return area(x + 2 - x**2, a, b)
q("U08-E-003", TOP_LP, "Parabola and a chord line", "Easy", "Single-step computation MCQ",
  r"The area of the region enclosed by the parabola $y = x^2$ and the line $y = x + 2$ is",
  r"$\frac{9}{2}$",
  [(r"$9$", r"Uses $\frac{(\beta - \alpha)^3}{3} = \frac{27}{3}$ in place of $\frac{(\beta - \alpha)^3}{6}$."),
   (r"$\frac{15}{2}$", r"Finds only the area under the line, $\int_{-1}^{2}(x+2)\,dx = \frac{15}{2}$, without subtracting the parabola."),
   (r"$3$", r"Finds only the area under the parabola, $\int_{-1}^{2}x^2\,dx = 3$.")],
  r"The curves meet where $x^2 = x + 2$, i.e. $x = -1, 2$. The area is $\int_{-1}^{2}(x + 2 - x^2)\,dx = \left[\frac{x^2}{2} + 2x - \frac{x^3}{3}\right]_{-1}^{2} = \frac{10}{3} + \frac{7}{6} = \frac{9}{2}$.",
  "Not subtracting the lower curve from the upper curve.",
  "U08-E-line-parabola", "Find intersections, then one integral.",
  check=_c003, values=[Rational(9, 2), 9, Rational(15, 2), 3], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 004
q("U08-E-004", TOP_CE, "Quarter of an ellipse", "Easy", "Single-step computation MCQ",
  r"The area of the region in the first quadrant enclosed by the ellipse $\frac{x^2}{16} + \frac{y^2}{9} = 1$ and the coordinate axes is",
  r"$3\pi$",
  [(r"$12\pi$", r"Gives the area $\pi ab$ of the whole ellipse."),
   (r"$6\pi$", r"Gives the area of half the ellipse."),
   (r"$12$", r"Takes the rectangle $ab = 4 \cdot 3$ enclosing the quarter instead of integrating.")],
  r"In the first quadrant $y = \frac{3}{4}\sqrt{16 - x^2}$, so the area is $\frac{3}{4}\int_0^4\sqrt{16 - x^2}\,dx = \frac{3}{4}\cdot\frac{\pi\cdot 16}{4} = 3\pi$, i.e. $\frac{\pi ab}{4}$.",
  "Confusing the quarter region with the whole ellipse.",
  "U08-E-ellipse-full", "Direct use of the ellipse area integral.",
  check=lambda: area(Rational(3, 4) * sqrt(16 - x**2), 0, 4), values=[3 * pi, 12 * pi, 6 * pi, 12], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 005
def _c005():
    a, b = real_roots(3 - Abs(x - 1))
    return area(3 - Abs(x - 1), a, b)
q("U08-E-005", TOP_MOD, "Modulus curve and a horizontal line", "Easy", "Single-step computation MCQ",
  r"The area of the region enclosed by the curve $y = |x - 1|$ and the line $y = 3$ is",
  r"$9$",
  [(r"$\frac{9}{2}$", r"Computes only the part on one side of $x = 1$."),
   (r"$18$", r"Takes the full rectangle $6 \times 3$ between $x = -2$ and $x = 4$ without subtracting the area under the graph."),
   (r"$\frac{27}{2}$", r"Subtracts the area under only one branch: $18 - \frac{9}{2}$.")],
  r"$|x - 1| = 3$ gives $x = -2$ and $x = 4$. The region is a triangle with vertices $(-2, 3)$, $(4, 3)$, $(1, 0)$, so its area is $\int_{-2}^{4}(3 - |x - 1|)\,dx = 18 - 9 = 9$, i.e. $\frac{1}{2}\cdot 6\cdot 3$.",
  "Handling only one branch of the modulus graph.",
  "U08-E-mod-line", "Sketch a V-shaped graph and one subtraction.",
  check=_c005, values=[9, Rational(9, 2), 18, Rational(27, 2)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the curve $y = |x - 1|$ and the line $y = 3$ is", answer=9))

# ---------------------------------------------------------------- 006
q("U08-E-006", TOP_CE, "Minor segment of a circle cut by a line", "Easy", "Single-step computation MCQ",
  r"The area of the smaller of the two regions into which the line $x + y = 2$ divides the circle $x^2 + y^2 = 4$ is",
  r"$\pi - 2$",
  [(r"$\pi + 2$", r"Adds the triangle with vertices $(0,0)$, $(2,0)$, $(0,2)$ to the quarter circle instead of subtracting it."),
   (r"$3\pi + 2$", r"Gives the area of the larger region, $4\pi - (\pi - 2)$."),
   (r"$\pi$", r"Gives the area of the quarter circle, ignoring the triangle below the chord.")],
  r"The line meets the circle at $(2, 0)$ and $(0, 2)$. The smaller region is $\int_0^2\left(\sqrt{4 - x^2} - (2 - x)\right)dx = \pi - 2$, the quarter circle minus the right triangle of area $2$.",
  "Adding instead of subtracting the triangle cut off by the chord.",
  "U08-E-circle-chord", "Quarter circle minus a triangle.",
  check=lambda: area(sqrt(4 - x**2) - (2 - x), 0, 2), values=[pi - 2, pi + 2, 3 * pi + 2, pi], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 007
def _c007():
    b = solve(Eq(exp(x), 3), x)[0]
    return area(3 - exp(x), 0, b)
q("U08-E-007", TOP_UNDER, "Region between an exponential curve and a horizontal line", "Easy", "Single-step computation MCQ",
  r"The area of the region bounded by the curve $y = e^x$, the line $y = 3$ and the $y$-axis is",
  r"$3\log_e 3 - 2$",
  [(r"$2$", r"Finds the area under $y = e^x$ from $x = 0$ to $x = \log_e 3$, the region below the curve."),
   (r"$3\log_e 3$", r"Takes the rectangle of height $3$ and width $\log_e 3$ without subtracting the area under the curve."),
   (r"$3\log_e 3 - 3$", r"Drops the lower limit value $e^0 = 1$, writing $\int_0^{\log_e 3} e^x\,dx = 3$.")],
  r"The curve meets $y = 3$ at $x = \log_e 3$. The region lies between $x = 0$ and $x = \log_e 3$, below $y = 3$ and above the curve, so its area is $\int_0^{\log_e 3}(3 - e^x)\,dx = 3\log_e 3 - (3 - 1) = 3\log_e 3 - 2$.",
  "Computing the area under the curve instead of the area between the curve and the line.",
  "U08-E-exp-under", "One subtraction and a log limit.",
  check=_c007, values=[3 * log(3) - 2, 2, 3 * log(3), 3 * log(3) - 3], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 008
def _c008():
    p = [r for r in real_roots(x**2 - (2 - x)) if r > 0][0]
    q0 = solve(2 - x, x)[0]
    return area(x**2, 0, p) + area(2 - x, p, q0)
q("U08-E-008", TOP_LP, "Curvilinear triangle with a parabola, a line and the axis", "Easy", "Multi-step computation MCQ",
  r"The area of the region in the first quadrant bounded by the parabola $y = x^2$, the line $x + y = 2$ and the $x$-axis is",
  r"$\frac{5}{6}$",
  [(r"$\frac{7}{6}$", r"Finds the region between the line and the parabola next to the $y$-axis, $\int_0^1 (2 - x - x^2)\,dx$."),
   (r"$\frac{1}{3}$", r"Finds only the area under the parabola from $x = 0$ to $x = 1$, omitting the triangle under the line."),
   (r"$2$", r"Takes the triangle formed by the line and the axes, ignoring the parabola.")],
  r"The parabola meets the line at $(1, 1)$ and the line meets the $x$-axis at $(2, 0)$. The region is $\int_0^1 x^2\,dx + \int_1^2 (2 - x)\,dx = \frac{1}{3} + \frac{1}{2} = \frac{5}{6}$.",
  "Picking the wrong one of the regions formed by the three boundaries.",
  "U08-E-split-region", "Split at one intersection point.",
  check=_c008, values=[Rational(5, 6), Rational(7, 6), Rational(1, 3), 2], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 009
q("U08-E-009", TOP_UNDER, "Area versus signed integral for a cosine curve", "Easy", "Conceptual/application MCQ",
  r"The area of the region bounded by the curve $y = \cos x$, the $x$-axis and the lines $x = 0$ and $x = \frac{3\pi}{2}$ is",
  r"$3$",
  [(r"$1$", r"Takes the absolute value of the signed integral $\int_0^{3\pi/2}\cos x\,dx = -1$."),
   (r"$2$", r"Counts only the part below the axis, from $x = \frac{\pi}{2}$ to $x = \frac{3\pi}{2}$."),
   (r"$4$", r"Treats the piece from $0$ to $\frac{\pi}{2}$ as a full arch of area $2$ as well.")],
  r"$\cos x \ge 0$ on $[0, \frac{\pi}{2}]$ and $\le 0$ on $[\frac{\pi}{2}, \frac{3\pi}{2}]$. Area $= \int_0^{\pi/2}\cos x\,dx - \int_{\pi/2}^{3\pi/2}\cos x\,dx = 1 + 2 = 3$.",
  "Using the signed integral as the area when the curve crosses the axis.",
  "U08-E-signed-vs-area", "One split at a zero of the integrand.",
  check=lambda: area(cos(x), 0, 3 * pi / 2), values=[3, 1, 2, 4], cognitive="Understanding", source_class="XII",
  numerical=dict(question=r"The area of the region bounded by the curve $y = \cos x$, the $x$-axis and the lines $x = 0$ and $x = \frac{3\pi}{2}$ is", answer=3))

# ---------------------------------------------------------------- 010
q("U08-E-010", TOP_MOD, "Region enclosed by $|x| + |y| = k$", "Easy", "Single-step computation MCQ",
  r"The area of the region enclosed by the curve $|x| + |y| = 2$ is",
  r"$8$",
  [(r"$4$", r"Takes the side of the square as $2$; the side is actually $2\sqrt{2}$."),
   (r"$16$", r"Squares the diagonal length $4$ instead of halving its square."),
   (r"$2$", r"Gives only the part in one quadrant.")],
  r"In the first quadrant the curve is $y = 2 - x$, enclosing $\int_0^2(2 - x)\,dx = 2$. By symmetry in all four quadrants the area is $4 \cdot 2 = 8$.",
  "Misreading the side length of the tilted square.",
  "U08-E-mod-square", "One quadrant integral and symmetry.",
  check=lambda: 4 * area(2 - x, 0, 2), values=[8, 4, 16, 2], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the curve $|x| + |y| = 2$ is", answer=8))

# ---------------------------------------------------------------- 011
def _c011():
    k = Symbol('k', positive=True)
    sol = [s for s in solve(Eq(integrate(1 / x, (x, 1, k)), 3), k) if s > 1]
    return sol[0]
q("U08-E-011", TOP_PAR, "Upper limit from a given area under a hyperbola", "Easy", "Inverse/parameter MCQ",
  r"For $k > 1$, the area of the region bounded by the curve $y = \frac{1}{x}$, the $x$-axis and the lines $x = 1$ and $x = k$ is $3$. Then $k$ equals",
  r"$e^3$",
  [(r"$e^4$", r"Takes $\log_e 1 = 1$, so $\log_e k - 1 = 3$."),
   (r"$4$", r"Integrates $\frac{1}{x}$ as $x$, getting $k - 1 = 3$."),
   (r"$\log_e 3$", r"Inverts the relation, writing $k = \log_e 3$ from $\log_e k = 3$.")],
  r"For $x > 0$ the curve is above the axis, so the area is $\int_1^k\frac{dx}{x} = \log_e k = 3$, giving $k = e^3$.",
  "Mishandling the logarithm when solving for the limit.",
  "U08-E-param-limit", "One integral, then solve a log equation.",
  check=_c011, values=[exp(3), exp(4), 4, log(3)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 012
def _c012():
    f = x**2 - 4*x + 3
    a, b = real_roots(f)
    return area(f, a, b)
q("U08-E-012", TOP_UNDER, "Parabola below the axis", "Easy", "Single-step computation MCQ",
  r"The area of the region enclosed by the curve $y = x^2 - 4x + 3$ and the $x$-axis is",
  r"$\frac{4}{3}$",
  [(r"$\frac{8}{3}$", r"Uses $\frac{(\beta - \alpha)^3}{3}$ in place of $\frac{(\beta - \alpha)^3}{6}$ with $\beta - \alpha = 2$."),
   (r"$\frac{2}{3}$", r"Integrates only from $x = 1$ to the vertex $x = 2$ and does not double."),
   (r"$1$", r"Approximates the region by the triangle with vertices $(1, 0)$, $(3, 0)$, $(2, -1)$.")],
  r"The roots are $x = 1, 3$ and the curve lies below the axis between them. Area $= -\int_1^3(x^2 - 4x + 3)\,dx = -\left[\frac{x^3}{3} - 2x^2 + 3x\right]_1^3 = -\left(0 - \frac{4}{3}\right) = \frac{4}{3}$.",
  "Using the wrong constant in the parabolic segment formula.",
  "U08-E-parabola-axis", "Roots, then one integral with a sign.",
  check=_c012, values=[Rational(4, 3), Rational(8, 3), Rational(2, 3), 1], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 013
def _c013():
    a, b = real_roots(sqrt(x) - x)
    return area(sqrt(x) - x, a, b)
q("U08-E-013", TOP_PP, "Square-root curve and a line", "Easy", "Single-step computation MCQ",
  r"The area of the region enclosed by the curve $y = \sqrt{x}$ and the line $y = x$ is",
  r"$\frac{1}{6}$",
  [(r"$\frac{2}{3}$", r"Finds only the area under $y = \sqrt{x}$ from $0$ to $1$."),
   (r"$\frac{1}{2}$", r"Finds only the area under $y = x$ from $0$ to $1$."),
   (r"$\frac{7}{6}$", r"Adds the two areas instead of subtracting.")],
  r"They meet at $x = 0$ and $x = 1$, where $\sqrt{x} \ge x$. Area $= \int_0^1(\sqrt{x} - x)\,dx = \frac{2}{3} - \frac{1}{2} = \frac{1}{6}$.",
  "Not subtracting the lower curve.",
  "U08-E-root-line", "Two power integrals subtracted.",
  check=_c013, values=[Rational(1, 6), Rational(2, 3), Rational(1, 2), Rational(7, 6)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 014
def _c014():
    rts = real_roots(x**3 - x)
    return area(x**3 - x, rts[0], rts[-1])
q("U08-E-014", TOP_PP, "Two loops between a cubic and a line", "Easy", "Single-step computation MCQ",
  r"The total area of the region enclosed between the curve $y = x^3$ and the line $y = x$ is",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{4}$", r"Counts only the loop in the first quadrant."),
   (r"$\frac{3}{2}$", r"Adds $\int_0^1 x\,dx$ and $\int_0^1 x^3\,dx$ instead of subtracting, for both loops: $2\left(\frac{1}{2} + \frac{1}{4}\right)$."),
   (r"$\frac{3}{4}$", r"Adds the two functions instead of subtracting, for one loop only.")],
  r"$x^3 = x$ at $x = -1, 0, 1$. On $[0, 1]$, $x \ge x^3$ and $\int_0^1 (x - x^3)\,dx = \frac{1}{4}$; the loop on $[-1, 0]$ has the same area by odd symmetry. Total $= \frac{1}{2}$.",
  "Missing the second loop, or treating the signed integral over $[-1, 1]$ as the area.",
  "U08-E-cubic-line", "Two symmetric loops.",
  check=_c014, values=[Rational(1, 2), Rational(1, 4), Rational(3, 2), Rational(3, 4)], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 015
def _c015():
    a, b = real_roots(9 - x**2)
    return area(9 - x**2, a, b)
q("U08-E-015", TOP_UNDER, "Downward parabola and the axis", "Easy", "Single-step computation MCQ",
  r"The area of the region enclosed by the curve $y = 9 - x^2$ and the $x$-axis is",
  r"$36$",
  [(r"$18$", r"Integrates from $0$ to $3$ only and does not double."),
   (r"$54$", r"Takes the rectangle of width $6$ and height $9$."),
   (r"$72$", r"Integrates $9 + x^2$ by a sign slip: $\int_{-3}^{3}(9 + x^2)\,dx = 54 + 18$.")],
  r"The curve meets the axis at $x = \pm 3$. Area $= \int_{-3}^{3}(9 - x^2)\,dx = 54 - 18 = 36$, which is two thirds of the $6 \times 9$ rectangle.",
  "Forgetting to use symmetry correctly.",
  "U08-E-parabola-axis", "One integral of a quadratic.",
  check=_c015, values=[36, 18, 54, 72], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the curve $y = 9 - x^2$ and the $x$-axis is", answer=36))

# ---------------------------------------------------------------- 016
q("U08-E-016", TOP_PP, "Between $e^x$ and $e^{-x}$", "Easy", "Single-step computation MCQ",
  r"The area of the region bounded by the curves $y = e^x$, $y = e^{-x}$ and the line $x = 1$ is",
  r"$e + \frac{1}{e} - 2$",
  [(r"$e - \frac{1}{e}$", r"Integrates $e^{-x}$ as $e^{-x}$ (sign slip), getting $\left[e^x - e^{-x}\right]_0^1$."),
   (r"$e + \frac{1}{e}$", r"Drops the lower limit value $e^0 + e^0 = 2$."),
   (r"$e + \frac{1}{e} - 1$", r"Subtracts the lower limit value of only one exponential.")],
  r"The curves meet at $x = 0$, and on $[0, 1]$ we have $e^x \ge e^{-x}$. Area $= \int_0^1(e^x - e^{-x})\,dx = \left[e^x + e^{-x}\right]_0^1 = e + \frac{1}{e} - 2$.",
  "Sign error in the antiderivative of $e^{-x}$.",
  "U08-E-exp-pair", "One integral after locating the meeting point.",
  check=lambda: area(exp(x) - exp(-x), solve(exp(x) - exp(-x), x)[0], 1),
  values=[E + 1 / E - 2, E - 1 / E, E + 1 / E, E + 1 / E - 1], cognitive="Application", source_class="XII")

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 017
def _c017():
    rts = [r for r in real_roots(x**4 / 36 - 6 * x)]
    return area(sqrt(6 * x) - x**2 / 6, rts[0], rts[-1])
q("U08-E-017", TOP_PP, "Two perpendicular-axis parabolas", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the parabolas $y^2 = 6x$ and $x^2 = 6y$ is",
  r"$12$",
  [(r"$24$", r"Finds only the area under $y = \sqrt{6x}$ from $0$ to $6$."),
   (r"$36$", r"Adds the area under $x^2 = 6y$ to the area under $y^2 = 6x$ instead of subtracting."),
   (r"$6$", r"Finds only the region between the line $y = x$ and one parabola, half of the required region.")],
  r"Substituting $y = \frac{x^2}{6}$ into $y^2 = 6x$ gives $x^4 = 216x$, so $x = 0, 6$. Area $= \int_0^6\left(\sqrt{6x} - \frac{x^2}{6}\right)dx = \sqrt{6}\cdot\frac{2}{3}\cdot 6^{3/2} - \frac{216}{18} = 24 - 12 = 12$, matching $\frac{16a^2}{3}$ with $a = \frac{3}{2}$.",
  "Not subtracting the lower parabola.",
  "U08-E-two-parabolas", "Intersection by elimination, then two integrals.",
  check=_c017, values=[12, 24, 36, 6], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the parabolas $y^2 = 6x$ and $x^2 = 6y$ is", answer=12))

# ---------------------------------------------------------------- 018
def _c018():
    ys = real_roots((y + 4) / 2 - y**2 / 4, y)
    return area((y + 4) / 2 - y**2 / 4, ys[0], ys[-1], y)
q("U08-E-018", TOP_LP, "Parabola and a slant line, horizontal strips", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the parabola $y^2 = 4x$ and the line $y = 2x - 4$ is",
  r"$9$",
  [(r"$\frac{32}{3}$", r"Integrates $\int_0^4\left(2\sqrt{x} - (2x - 4)\right)dx$ in vertical strips, ignoring that for $0 \le x \le 1$ the lower boundary is $y = -2\sqrt{x}$, not the line."),
   (r"$36$", r"Writes the strip width as $8 + 2y - y^2$, dropping the factor $\frac{1}{4}$, and gets $\frac{6^3}{6}$."),
   (r"$\frac{20}{3}$", r"Takes only the part above the $x$-axis, $y$ from $0$ to $4$.")],
  r"With $x = \frac{y^2}{4}$ and $x = \frac{y + 4}{2}$, equating gives $y^2 - 2y - 8 = 0$, so $y = -2, 4$. Area $= \int_{-2}^{4}\left(\frac{y + 4}{2} - \frac{y^2}{4}\right)dy = \left[\frac{y^2}{4} + 2y - \frac{y^3}{12}\right]_{-2}^{4} = \frac{20}{3} + \frac{7}{3} = 9$.",
  "Using vertical strips when the lower boundary changes along the way.",
  "U08-E-horizontal-strips", "Choosing horizontal strips; two intersection points.",
  check=_c018, values=[9, Rational(32, 3), 36, Rational(20, 3)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the parabola $y^2 = 4x$ and the line $y = 2x - 4$ is", answer=9))

# ---------------------------------------------------------------- 019
def _c019():
    a = Symbol('a', positive=True)
    b = [r for r in solve(a * x**2 - 2 * x, x) if r != 0][0]
    A = integrate(2 * x - a * x**2, (x, 0, b))
    return [s for s in solve(Eq(A, Rational(4, 27)), a) if s > 0][0]
q("U08-E-019", TOP_PAR, "Coefficient of a parabola from an enclosed area", "Medium", "Inverse/parameter MCQ",
  r"For $a > 0$, the area of the region enclosed by the parabola $y = ax^2$ and the line $y = 2x$ is $\frac{4}{27}$. Then $a$ equals",
  r"$3$",
  [(r"$3\sqrt{3}$", r"Uses only the area under the line, $\int_0^{2/a}2x\,dx = \frac{4}{a^2}$."),
   (r"$3\sqrt{2}$", r"Uses only the area under the parabola, $\frac{8}{3a^2}$."),
   (r"$\frac{13}{9}$", r"Takes the upper limit as $x = 2$ instead of $x = \frac{2}{a}$, so $4 - \frac{8a}{3} = \frac{4}{27}$.")],
  r"They meet at $x = 0$ and $x = \frac{2}{a}$. Area $= \int_0^{2/a}(2x - ax^2)\,dx = \frac{4}{a^2} - \frac{8}{3a^2} = \frac{4}{3a^2}$. Setting $\frac{4}{3a^2} = \frac{4}{27}$ gives $a^2 = 9$, so $a = 3$.",
  "Using a fixed limit instead of the parameter-dependent intersection.",
  "U08-E-param-parabola-line", "Area in terms of a parameter, then solve.",
  check=_c019, values=[3, 3 * sqrt(3), 3 * sqrt(2), Rational(13, 9)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"For $a > 0$, the area of the region enclosed by the parabola $y = ax^2$ and the line $y = 2x$ is $\frac{4}{27}$. Then $a$ is", answer=3))

# ---------------------------------------------------------------- 020
def _c020():
    f = 2 - x**2 - x**2
    a, b = real_roots(f)
    return area(f, a, b)
q("U08-E-020", TOP_PP, "Two opposite parabolas", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the parabolas $y = x^2$ and $y = 2 - x^2$ is",
  r"$\frac{8}{3}$",
  [(r"$\frac{4}{3}$", r"Integrates from $0$ to $1$ only and does not double."),
   (r"$\frac{4\sqrt{2}}{3}$", r"Takes the limits $\pm\sqrt{2}$ where $2 - x^2$ meets the $x$-axis, computing $\int_{-\sqrt{2}}^{\sqrt{2}}(2 - 2x^2)\,dx$."),
   (r"$4$", r"Adds the two functions, integrating $\int_{-1}^{1}(2 - x^2 + x^2)\,dx$.")],
  r"$x^2 = 2 - x^2$ gives $x = \pm 1$. Area $= \int_{-1}^{1}\left((2 - x^2) - x^2\right)dx = \left[2x - \frac{2x^3}{3}\right]_{-1}^{1} = 2\left(2 - \frac{2}{3}\right) = \frac{8}{3}$.",
  "Using the wrong limits of integration.",
  "U08-E-two-parabolas", "Intersections, then one even integral.",
  check=_c020, values=[Rational(8, 3), Rational(4, 3), 4 * sqrt(2) / 3, 4], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 021
def _c021():
    f = (6 * x - 2 * x**2) - x**2
    a, b = real_roots(f)
    return area(f, a, b)
q("U08-E-021", TOP_PP, "Two parabolas with the same axis direction", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the parabolas $y = x^2$ and $y = 6x - 2x^2$ is",
  r"$4$",
  [(r"$\frac{20}{3}$", r"Finds only the area under $y = 6x - 2x^2$ from $0$ to $2$."),
   (r"$8$", r"Uses $\frac{|a|(\beta - \alpha)^3}{3}$ with $a = 3$, $\beta - \alpha = 2$, in place of division by $6$."),
   (r"$\frac{4}{3}$", r"Uses $\frac{(\beta - \alpha)^3}{6}$ with leading coefficient $1$ instead of $3$ for the difference $6x - 3x^2$.")],
  r"$x^2 = 6x - 2x^2$ gives $3x^2 = 6x$, so $x = 0, 2$. Area $= \int_0^2(6x - 3x^2)\,dx = 12 - 8 = 4$.",
  "Ignoring the leading coefficient of the difference of the two quadratics.",
  "U08-E-two-parabolas", "Difference of quadratics, then one integral.",
  check=_c021, values=[4, Rational(20, 3), 8, Rational(4, 3)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the parabolas $y = x^2$ and $y = 6x - 2x^2$ is", answer=4))

# ---------------------------------------------------------------- 022
q("U08-E-022", TOP_CE, "Ellipse and the chord joining the ends of its axes", "Medium", "Multi-step computation MCQ",
  r"The area of the smaller region bounded by the ellipse $\frac{x^2}{25} + \frac{y^2}{4} = 1$ and the line $\frac{x}{5} + \frac{y}{2} = 1$ is",
  r"$\frac{5\pi}{2} - 5$",
  [(r"$\frac{5\pi}{2}$", r"Gives the area of the quarter ellipse without removing the triangle under the chord."),
   (r"$\frac{15\pi}{2} + 5$", r"Gives the larger region, $10\pi - \left(\frac{5\pi}{2} - 5\right)$."),
   (r"$5\pi - 5$", r"Subtracts the triangle from half of the ellipse instead of a quarter.")],
  r"The line meets the ellipse at $(5, 0)$ and $(0, 2)$. In the first quadrant the ellipse is $y = \frac{2}{5}\sqrt{25 - x^2}$, so the smaller region is $\int_0^5\left(\frac{2}{5}\sqrt{25 - x^2} - 2\left(1 - \frac{x}{5}\right)\right)dx = \frac{2}{5}\cdot\frac{25\pi}{4} - 5 = \frac{5\pi}{2} - 5$, i.e. the quarter ellipse $\frac{\pi ab}{4}$ minus the triangle $\frac{ab}{2}$.",
  "Using the wrong portion of the ellipse.",
  "U08-E-ellipse-chord", "Quarter ellipse integral and a triangle.",
  check=lambda: area(Rational(2, 5) * sqrt(25 - x**2) - 2 * (1 - x / 5), 0, 5),
  values=[5 * pi / 2 - 5, 5 * pi / 2, 15 * pi / 2 + 5, 5 * pi - 5], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 023
def _c023():
    f = 2 - x**2 - Abs(x)
    rts = real_roots(f)
    return area(f, rts[0], rts[-1])
q("U08-E-023", TOP_MOD, "Modulus curve under a downward parabola", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the curves $y = |x|$ and $y = 2 - x^2$ is",
  r"$\frac{7}{3}$",
  [(r"$\frac{7}{6}$", r"Computes only the part for $x \ge 0$ and does not double."),
   (r"$\frac{10}{3}$", r"Replaces $|x|$ by $x$ in the integrand but keeps the limits $\pm 1$: $\int_{-1}^{1}(2 - x^2 - x)\,dx$."),
   (r"$\frac{9}{2}$", r"Replaces $|x|$ by $x$ throughout, so the limits become $-2$ and $1$: $\int_{-2}^{1}(2 - x - x^2)\,dx$.")],
  r"For $x \ge 0$, $x = 2 - x^2$ gives $x = 1$; by symmetry the other end is $x = -1$. Area $= 2\int_0^1(2 - x^2 - x)\,dx = 2\left(2 - \frac{1}{3} - \frac{1}{2}\right) = \frac{7}{3}$.",
  "Treating $|x|$ as $x$ on the negative side.",
  "U08-E-mod-parabola", "Modulus split and symmetry.",
  check=_c023, values=[Rational(7, 3), Rational(7, 6), Rational(10, 3), Rational(9, 2)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 024
def _c024():
    f = (3 - Abs(x)) - Abs(x - 1)
    rts = real_roots(f)
    return area(f, rts[0], rts[-1])
q("U08-E-024", TOP_MOD, "Two V-shaped graphs", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the curves $y = |x - 1|$ and $y = 3 - |x|$ is",
  r"$4$",
  [(r"$5$", r"Replaces $3 - |x|$ by $3 - x$ for $-1 \le x \le 0$ while keeping the limits $-1$ and $2$."),
   (r"$3$", r"Omits the piece between $x = -1$ and $x = 0$."),
   (r"$\frac{13}{2}$", r"Finds the area under $y = 3 - |x|$ from $x = -1$ to $x = 2$ without subtracting the area under $y = |x - 1|$.")],
  r"For $x \ge 1$: $x - 1 = 3 - x$ gives $x = 2$; for $x \le 0$: $1 - x = 3 + x$ gives $x = -1$. The region is the quadrilateral with vertices $(-1, 2)$, $(0, 3)$, $(2, 1)$, $(1, 0)$. Splitting at $x = 0$ and $x = 1$: $\int_{-1}^{0}(2 + 2x)\,dx + \int_0^1 2\,dx + \int_1^2(4 - 2x)\,dx = 1 + 2 + 1 = 4$.",
  "Not splitting the integral at every corner of the two modulus graphs.",
  "U08-E-mod-two-v", "Three pieces from two modulus functions.",
  check=_c024, values=[4, 5, 3, Rational(13, 2)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the curves $y = |x - 1|$ and $y = 3 - |x|$ is", answer=4))

# ---------------------------------------------------------------- 025
def _c025():
    c = solve(x**2 + 1 - (x + 1), x)
    c = [r for r in c if 0 < r < 2][0]
    m1 = Min(x**2 + 1, x + 1).subs(x, c / 2)
    g1 = x**2 + 1 if m1 == (x**2 + 1).subs(x, c / 2) else x + 1
    g2 = x + 1 if g1 == x**2 + 1 else x**2 + 1
    return integrate(g1, (x, 0, c)) + integrate(g2, (x, c, 2))
q("U08-E-025", TOP_MOD, "Region defined by two upper bounds", "Medium", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : 0 \le y \le x^2 + 1,\ 0 \le y \le x + 1,\ 0 \le x \le 2\}$ is",
  r"$\frac{23}{6}$",
  [(r"$\frac{14}{3}$", r"Uses only the bound $y \le x^2 + 1$ on the whole of $[0, 2]$."),
   (r"$4$", r"Uses only the bound $y \le x + 1$ on the whole of $[0, 2]$."),
   (r"$\frac{29}{6}$", r"Takes the larger of the two bounds on each piece: $x + 1$ on $[0, 1]$ and $x^2 + 1$ on $[1, 2]$.")],
  r"The upper boundary is $\min(x^2 + 1, x + 1)$; since $x^2 \le x$ exactly on $[0, 1]$, it is $x^2 + 1$ on $[0, 1]$ and $x + 1$ on $[1, 2]$. Area $= \int_0^1(x^2 + 1)\,dx + \int_1^2(x + 1)\,dx = \frac{4}{3} + \frac{5}{2} = \frac{23}{6}$.",
  "Taking the larger instead of the smaller of two upper bounds.",
  "U08-E-ineq-min", "Interpreting simultaneous inequalities and splitting at the crossing.",
  check=_c025, values=[Rational(23, 6), Rational(14, 3), 4, Rational(29, 6)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 026
def _c026():
    f = sqrt(4 - x**2) - sqrt(3) * Abs(x)
    rts = real_roots(4 - x**2 - 3 * x**2)
    return area(f, rts[0], rts[-1])
q("U08-E-026", TOP_CE, "Circular sector cut by two lines", "Medium", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : x^2 + y^2 \le 4,\ y \ge \sqrt{3}\,|x|\}$ is",
  r"$\frac{2\pi}{3}$",
  [(r"$\frac{\pi}{3}$", r"Uses $\frac{1}{2}r\theta$ with $r = 2$ in place of $\frac{1}{2}r^2\theta$."),
   (r"$\frac{4\pi}{3}$", r"Reads slope $\sqrt{3}$ as an inclination of $30^\circ$, giving a wedge of angle $\frac{2\pi}{3}$."),
   (r"$\frac{2\pi}{3} - \sqrt{3}$", r"Treats the region as a circular segment and subtracts the triangle $\frac{1}{2}r^2\sin\theta = \sqrt{3}$.")],
  r"The lines $y = \pm\sqrt{3}x$ make angles $\frac{\pi}{3}$ and $\frac{2\pi}{3}$ with the $x$-axis, so the region is a sector of angle $\frac{\pi}{3}$ in a circle of radius $2$. Area $= \frac{1}{2}\cdot 4\cdot\frac{\pi}{3} = \frac{2\pi}{3}$. Directly, $\int_{-1}^{1}\left(\sqrt{4 - x^2} - \sqrt{3}|x|\right)dx = \left(\sqrt{3} + \frac{2\pi}{3}\right) - \sqrt{3}$.",
  "Confusing a sector with a segment.",
  "U08-E-circle-sector", "Recognise a sector, or integrate with a modulus.",
  check=_c026, values=[2 * pi / 3, pi / 3, 4 * pi / 3, 2 * pi / 3 - sqrt(3)], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 027
q("U08-E-027", TOP_PP, "Sine and cosine over a half period", "Medium", "Multi-step computation MCQ",
  r"The area of the region bounded by the curves $y = \sin x$, $y = \cos x$ and the lines $x = 0$ and $x = \pi$ is",
  r"$2\sqrt{2}$",
  [(r"$2$", r"Takes the absolute value of the single integral $\int_0^{\pi}(\cos x - \sin x)\,dx = -2$ without splitting at $x = \frac{\pi}{4}$."),
   (r"$\sqrt{2} + 1$", r"Counts only the part from $x = \frac{\pi}{4}$ to $x = \pi$."),
   (r"$\sqrt{2} - 1$", r"Counts only the part from $x = 0$ to $x = \frac{\pi}{4}$.")],
  r"The curves cross at $x = \frac{\pi}{4}$. Area $= \int_0^{\pi/4}(\cos x - \sin x)\,dx + \int_{\pi/4}^{\pi}(\sin x - \cos x)\,dx = (\sqrt{2} - 1) + (1 + \sqrt{2}) = 2\sqrt{2}$.",
  "Not splitting at the crossing point of the two curves.",
  "U08-E-trig-pair", "Split at a crossing and evaluate two pieces.",
  check=lambda: area(sin(x) - cos(x), 0, pi), values=[2 * sqrt(2), 2, sqrt(2) + 1, sqrt(2) - 1], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 028
q("U08-E-028", TOP_UNDER, "Logarithmic curve on both sides of $x = 1$", "Medium", "Multi-step computation MCQ",
  r"The area of the region bounded by the curve $y = \log_e x$, the $x$-axis and the lines $x = \frac{1}{e}$ and $x = e$ is",
  r"$2 - \frac{2}{e}$",
  [(r"$\frac{2}{e}$", r"Uses the signed integral $\int_{1/e}^{e}\log_e x\,dx = \frac{2}{e}$, letting the part below the axis cancel."),
   (r"$1$", r"Counts only the part from $x = 1$ to $x = e$."),
   (r"$2$", r"Assumes the part from $\frac{1}{e}$ to $1$ also has area $1$, by a false symmetry about $x = 1$.")],
  r"Using $\int\log_e x\,dx = x\log_e x - x$: on $[1, e]$ the area is $(e - e) - (0 - 1) = 1$; on $[\frac{1}{e}, 1]$ the curve is below the axis and the area is $-\left[(0 - 1) - \left(-\frac{1}{e} - \frac{1}{e}\right)\right] = 1 - \frac{2}{e}$. Total $= 2 - \frac{2}{e}$.",
  "Letting the region below the axis cancel the region above.",
  "U08-E-signed-vs-area", "By-parts antiderivative with a split at the root.",
  check=lambda: area(log(x), 1 / E, E), values=[2 - 2 / E, 2 / E, 1, 2], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 029
def _c029():
    c = Symbol('c', positive=True)
    total = area(4 - x**2, -2, 2)
    below = integrate(c - x**2, (x, -sqrt(c), sqrt(c)))
    return [s for s in solve(Eq(below, total / 2), c) if 0 < s < 4][0]
q("U08-E-029", TOP_PAR, "Horizontal line bisecting a parabolic region", "Medium", "Inverse/parameter MCQ",
  r"The line $y = c$ divides the region enclosed by $y = x^2$ and $y = 4$ into two parts of equal area. Then $c$ equals",
  r"$2\sqrt[3]{2}$",
  [(r"$2$", r"Halves the height of the region, assuming area is proportional to height."),
   (r"$2\sqrt{2}$", r"Assumes the area below $y = c$ is proportional to $c^2$, so $c^2 = 8$."),
   (r"$2\sqrt[3]{4}$", r"Assumes the area below $y = c$ is proportional to $c^3$, so $c^3 = 32$.")],
  r"The area between $y = x^2$ and $y = c$ is $\int_{-\sqrt{c}}^{\sqrt{c}}(c - x^2)\,dx = \frac{4}{3}c^{3/2}$. The whole region has area $\frac{4}{3}\cdot 8 = \frac{32}{3}$, so $\frac{4}{3}c^{3/2} = \frac{16}{3}$, giving $c^{3/2} = 4$ and $c = 4^{2/3} = 2\sqrt[3]{2}$.",
  "Assuming the area scales linearly with the height of a parabolic segment.",
  "U08-E-bisect-parabola", "Area as a function of the cutting height, then solve.",
  check=_c029, values=[2 * 2**Rational(1, 3), 2, 2 * sqrt(2), 2 * 4**Rational(1, 3)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The line $y = c$ divides the region enclosed by $y = x^2$ and $y = 4$ into two parts of equal area. Then the value of $c^3$ is", answer=16))

# ---------------------------------------------------------------- 030
def _c030():
    A = area(x**3, -1, 1)
    return (simplify(A - Rational(1, 2)) == 0, simplify(A - integrate(x**3, (x, -1, 1))) == 0)
q("U08-E-030", TOP_UNDER, "Area of an odd function's graph", "Medium", "Statement-based MCQ",
  r"Statement I: The area of the region bounded by the curve $y = x^3$, the $x$-axis and the lines $x = -1$ and $x = 1$ is $\frac{1}{2}$. Statement II: The area of the region described in Statement I equals $\int_{-1}^{1}x^3\,dx$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts the signed integral as the area, not noticing that $\int_{-1}^{1}x^3\,dx = 0$."),
   (ST_FF, r"Counts only the part with $x \ge 0$, getting area $\frac{1}{4}$ and rejecting Statement I, and correctly rejects Statement II."),
   (ST_FT, r"Takes the area to be the signed integral $0$, so rejects Statement I and accepts Statement II.")],
  r"The area is $\int_{-1}^{0}(-x^3)\,dx + \int_0^1 x^3\,dx = \frac{1}{4} + \frac{1}{4} = \frac{1}{2}$, so Statement I is true. But $\int_{-1}^{1}x^3\,dx = 0$ because $x^3$ is odd, so Statement II is false.",
  "Equating the area with the signed definite integral.",
  "U08-E-stmt-signed", "Separating area from signed integral for an odd function.",
  check=_c030, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 031
def _c031():
    s1 = 2 * area(Rational(2, 3) * sqrt(9 - x**2), -3, 3)
    s2 = area(sin(x), 0, pi)
    return (simplify(s1 - 6 * pi) == 0, simplify(s2 - 2) == 0)
q("U08-E-031", TOP_CE, "Ellipse area and one arch of the sine curve", "Medium", "Statement-based MCQ",
  r"Statement I: The area enclosed by the ellipse $4x^2 + 9y^2 = 36$ is $6\pi$. Statement II: The area of the region bounded by the curve $y = \sin x$, $0 \le x \le \pi$, and the $x$-axis is $2$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Takes $\int\sin x\,dx = \cos x$ for Statement II, getting $\cos\pi - \cos 0 = -2$ and rejecting it."),
   (ST_FT, r"Reads the ellipse as having semi-axes $9$ and $4$ (the denominators, not their square roots), getting $36\pi$ and rejecting Statement I."),
   (ST_FF, r"Reads the semi-axes as $9$ and $4$ (getting $36\pi$) and integrates $\sin x$ as $\cos x$ (getting $-2$), so rejects both statements.")],
  r"The ellipse is $\frac{x^2}{9} + \frac{y^2}{4} = 1$ with $a = 3$, $b = 2$, so its area is $\pi ab = 6\pi$: true. On $[0, \pi]$, $\sin x \ge 0$, so the area is $\int_0^{\pi}\sin x\,dx = \left[-\cos x\right]_0^{\pi} = 1 + 1 = 2$: true.",
  "Using the denominators of the standard form as semi-axes.",
  "U08-E-stmt-standard", "Two standard areas checked independently.",
  check=_c031, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 032
def _c032():
    s1 = 4 * area(3 - x, 0, 3)
    s2 = area(x**2 - x**3, 0, 1)
    return (simplify(s1 - 9) == 0, simplify(s2 - Rational(1, 12)) == 0)
q("U08-E-032", TOP_MOD, "Tilted square and the region between two power curves", "Medium", "Statement-based MCQ",
  r"Statement I: The area of the region enclosed by $|x| + |y| = 3$ is $9$. Statement II: The area of the region enclosed by the curves $y = x^2$ and $y = x^3$ is $\frac{1}{12}$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Takes the side of the square as $3$, accepting the value $9$ in Statement I."),
   (ST_TF, r"Takes the side as $3$ for Statement I and uses only $\int_0^1 x^2\,dx = \frac{1}{3}$ for Statement II, rejecting it."),
   (ST_FF, r"Correctly rejects Statement I but applies the parabola-and-line shortcut $\frac{(\beta - \alpha)^3}{6} = \frac{1}{6}$ to Statement II, rejecting it.")],
  r"$|x| + |y| = 3$ is a square with vertices $(\pm 3, 0)$, $(0, \pm 3)$; each quadrant contributes $\int_0^3(3 - x)\,dx = \frac{9}{2}$, so the area is $18$ and Statement I is false. For Statement II, the curves meet at $x = 0$ and $x = 1$, and $x^2 \ge x^3$ on $[0, 1]$, so the area is $\int_0^1(x^2 - x^3)\,dx = \frac{1}{3} - \frac{1}{4} = \frac{1}{12}$; it is true.",
  "Misjudging the side length of the square $|x| + |y| = k$.",
  "U08-E-stmt-standard", "Two short area checks.",
  check=_c032, values=[(False, True), (True, True), (True, False), (False, False)], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 033
def _c033():
    f = x**2
    t = diff(f, x).subs(x, 1) * (x - 1) + 1
    x0 = solve(t, x)[0]
    return area(f, 0, 1) - area(t, x0, 1)
q("U08-E-033", TOP_LP, "Parabola, its tangent and the axis", "Medium", "Multi-step computation MCQ",
  r"The area of the region bounded by the parabola $y = x^2$, the tangent to it at the point $(1, 1)$ and the $x$-axis is",
  r"$\frac{1}{12}$",
  [(r"$\frac{1}{3}$", r"Gives the area under the parabola from $0$ to $1$ without removing the triangle under the tangent."),
   (r"$\frac{1}{4}$", r"Gives the area of the triangle under the tangent instead of the region between curve and tangent."),
   (r"$\frac{7}{12}$", r"Adds the triangle to the area under the parabola instead of subtracting it.")],
  r"The tangent at $(1, 1)$ is $y = 2x - 1$, meeting the $x$-axis at $x = \frac{1}{2}$. The region is the area under the parabola on $[0, 1]$ minus the triangle with vertices $(\frac{1}{2}, 0)$, $(1, 0)$, $(1, 1)$: $\frac{1}{3} - \frac{1}{4} = \frac{1}{12}$.",
  "Not removing the triangle under the tangent.",
  "U08-E-tangent-region", "Tangent equation, then a difference of two areas.",
  check=_c033, values=[Rational(1, 12), Rational(1, 3), Rational(1, 4), Rational(7, 12)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 034
def _c034():
    f = 1 / (1 + x**2) - x**2 / 2
    rts = real_roots(2 - x**2 * (1 + x**2))
    return area(f, rts[0], rts[-1])
q("U08-E-034", TOP_PP, "Witch-type curve and a parabola", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the curves $y = \frac{1}{1 + x^2}$ and $y = \frac{x^2}{2}$ is",
  r"$\frac{\pi}{2} - \frac{1}{3}$",
  [(r"$\frac{\pi}{4} - \frac{1}{6}$", r"Integrates from $0$ to $1$ only and does not double."),
   (r"$\frac{\pi}{2} - \frac{2}{3}$", r"Drops the factor $\frac{1}{2}$ in $\frac{x^2}{2}$ when integrating, using $\int_{-1}^{1}x^2\,dx = \frac{2}{3}$."),
   (r"$\frac{\pi}{2} + \frac{1}{3}$", r"Adds the area under the parabola instead of subtracting it.")],
  r"$\frac{1}{1 + x^2} = \frac{x^2}{2}$ gives $x^4 + x^2 - 2 = 0$, so $x^2 = 1$, $x = \pm 1$. Area $= \int_{-1}^{1}\left(\frac{1}{1 + x^2} - \frac{x^2}{2}\right)dx = 2\left(\frac{\pi}{4} - \frac{1}{6}\right) = \frac{\pi}{2} - \frac{1}{3}$.",
  "Mishandling the constant factor of one curve.",
  "U08-E-witch-parabola", "Biquadratic intersection and an inverse-tangent integral.",
  check=_c034, values=[pi / 2 - Rational(1, 3), pi / 4 - Rational(1, 6), pi / 2 - Rational(2, 3), pi / 2 + Rational(1, 3)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 035
def _c035():
    ys = [r for r in real_roots(y**2 - (2 * y + 3), y)]
    top = [r for r in ys if r > 0][0]
    return area(2 * y + 3 - y**2, 0, top, y)
q("U08-E-035", TOP_LP, "Square-root curve, a line and the axis", "Medium", "Multi-step computation MCQ",
  r"The area of the region in the first quadrant bounded by the curve $y = \sqrt{x}$, the line $x = 2y + 3$ and the $x$-axis is",
  r"$9$",
  [(r"$18$", r"Finds the area under $y = \sqrt{x}$ from $x = 0$ to $x = 9$ and forgets to remove the triangle under the line."),
   (r"$\frac{32}{3}$", r"Integrates $\int_{-1}^{3}(2y + 3 - y^2)\,dy$, using both roots of $y^2 = 2y + 3$ and ignoring the $x$-axis boundary."),
   (r"$\frac{9}{2}$", r"Subtracts a triangle with base from $x = 0$ to $x = 9$ (area $\frac{27}{2}$) instead of from $x = 3$ to $x = 9$.")],
  r"In horizontal strips the region runs from $x = y^2$ to $x = 2y + 3$; they meet where $y^2 = 2y + 3$, i.e. $y = 3$ (the root $y = -1$ is not in the first quadrant). Area $= \int_0^3(2y + 3 - y^2)\,dy = 9 + 9 - 9 = 9$.",
  "Ignoring the $x$-axis as a boundary and using both intersection roots.",
  "U08-E-horizontal-strips", "Choosing the strip direction and rejecting one root.",
  check=_c035, values=[9, 18, Rational(32, 3), Rational(9, 2)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The area of the region in the first quadrant bounded by the curve $y = \sqrt{x}$, the line $x = 2y + 3$ and the $x$-axis is", answer=9))

# ---------------------------------------------------------------- 036
def _c036():
    f = Abs(x) - (x**2 - 2)
    rts = real_roots(f)
    return area(f, rts[0], rts[-1])
q("U08-E-036", TOP_MOD, "Region between an upward parabola and a modulus curve", "Medium", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : x^2 - 2 \le y \le |x|\}$ is",
  r"$\frac{20}{3}$",
  [(r"$\frac{10}{3}$", r"Computes only the part with $x \ge 0$."),
   (r"$\frac{8}{3}$", r"Replaces $|x|$ by $x$ in the integrand but keeps the limits $\pm 2$."),
   (r"$\frac{9}{2}$", r"Replaces $|x|$ by $x$ throughout, so the limits become $-1$ and $2$.")],
  r"For $x \ge 0$, $x^2 - 2 = x$ gives $x = 2$; by symmetry the region spans $-2 \le x \le 2$. Area $= 2\int_0^2(x - x^2 + 2)\,dx = 2\left(2 - \frac{8}{3} + 4\right) = \frac{20}{3}$.",
  "Dropping the modulus and losing the symmetry of the region.",
  "U08-E-mod-parabola", "Inequality region with a modulus bound.",
  check=_c036, values=[Rational(20, 3), Rational(10, 3), Rational(8, 3), Rational(9, 2)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 037
def _c037():
    f = x**3
    g = real_root(x, 3)
    one = integrate(x**Rational(1, 3) - x**3, (x, 0, 1))
    # odd symmetry: the loop in the third quadrant equals the first
    assert simplify(g.subs(x, -Rational(1, 2)) + g.subs(x, Rational(1, 2))) == 0
    return 2 * one
q("U08-E-037", TOP_PP, "Curve and its inverse", "Medium", "Conceptual/application MCQ",
  r"Let $f(x) = x^3$, $x \in \mathbb{R}$. The total area of the region enclosed between the graphs of $y = f(x)$ and $y = f^{-1}(x)$ is",
  r"$1$",
  [(r"$\frac{1}{2}$", r"Counts only the loop in the first quadrant."),
   (r"$2$", r"Adds the areas under $y = \sqrt[3]{x}$ and $y = x^3$ instead of subtracting, for both loops: $2\left(\frac{3}{4} + \frac{1}{4}\right)$."),
   (r"$\frac{1}{4}$", r"Finds only the area between $y = x^3$ and $y = x$ in the first quadrant and does not use the reflection in $y = x$.")],
  r"$f^{-1}(x) = \sqrt[3]{x}$, and the graphs meet at $x = -1, 0, 1$. In the first quadrant the area is $\int_0^1(x^{1/3} - x^3)\,dx = \frac{3}{4} - \frac{1}{4} = \frac{1}{2}$; the loop in the third quadrant is congruent by odd symmetry. Total $= 1$.",
  "Missing the second loop in the third quadrant.",
  "U08-E-inverse-pair", "Inverse function, symmetry and two loops.",
  check=_c037, values=[1, Rational(1, 2), 2, Rational(1, 4)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $f(x) = x^3$, $x \in \mathbb{R}$. The total area of the region enclosed between the graphs of $y = f(x)$ and $y = f^{-1}(x)$ is", answer=1))

# ---------------------------------------------------------------- 038
def _c038():
    f = (3 - 2 * y**2) - y**2
    ys = real_roots(f, y)
    return area(f, ys[0], ys[-1], y)
q("U08-E-038", TOP_PP, "Two parabolas opening along the $x$-axis", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed by the curves $x = y^2$ and $x = 3 - 2y^2$ is",
  r"$4$",
  [(r"$2$", r"Computes only the part above the $x$-axis."),
   (r"$\frac{14}{3}$", r"Finds only the region between $x = 3 - 2y^2$ and the $y$-axis for $-1 \le y \le 1$."),
   (r"$\frac{2}{3}$", r"Finds only the region between $x = y^2$ and the $y$-axis for $-1 \le y \le 1$.")],
  r"$y^2 = 3 - 2y^2$ gives $y = \pm 1$. Using horizontal strips, area $= \int_{-1}^{1}\left(3 - 2y^2 - y^2\right)dy = \left[3y - y^3\right]_{-1}^{1} = 4$.",
  "Not subtracting the inner curve when using horizontal strips.",
  "U08-E-sideways-parabolas", "Integration with respect to $y$.",
  check=_c038, values=[4, 2, Rational(14, 3), Rational(2, 3)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed by the curves $x = y^2$ and $x = 3 - 2y^2$ is", answer=4))

# ---------------------------------------------------------------- 039
def _c039():
    rts = [r for r in solveset(sin(2 * x) - sin(x), x, Interval(0, pi / 2))]
    rts = sorted(rts, key=lambda t: float(t))
    return area(sin(2 * x) - sin(x), rts[0], rts[1])
q("U08-E-039", TOP_PP, "Between $\\sin 2x$ and $\\sin x$", "Medium", "Multi-step computation MCQ",
  r"The area of the region enclosed between the curves $y = \sin 2x$ and $y = \sin x$ for $0 \le x \le \frac{\pi}{3}$ is",
  r"$\frac{1}{4}$",
  [(r"$\frac{3}{4}$", r"Finds only the area under $y = \sin 2x$ on $[0, \frac{\pi}{3}]$."),
   (r"$\frac{1}{2}$", r"Finds only the area under $y = \sin x$ on $[0, \frac{\pi}{3}]$."),
   (r"$\frac{5}{4}$", r"Adds the two areas instead of subtracting.")],
  r"$\sin 2x = \sin x$ gives $\sin x(2\cos x - 1) = 0$, so the curves meet at $x = 0$ and $x = \frac{\pi}{3}$, with $\sin 2x \ge \sin x$ between. Area $= \left[-\frac{\cos 2x}{2} + \cos x\right]_0^{\pi/3} = \left(\frac{1}{4} + \frac{1}{2}\right) - \left(-\frac{1}{2} + 1\right) = \frac{1}{4}$.",
  "Not subtracting the lower curve.",
  "U08-E-trig-pair", "Trig equation for the limits, then one integral.",
  check=_c039, values=[Rational(1, 4), Rational(3, 4), Rational(1, 2), Rational(5, 4)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 040
def _c040():
    a = Symbol('a', positive=True)
    yy = Symbol('yy', positive=True)
    # horizontal strip at height yy: between x = sqrt(yy/a) and x = sqrt(yy) on each side
    A = 2 * integrate(sqrt(yy) - sqrt(yy / a), (yy, 0, 1))
    return [s for s in solve(Eq(A, Rational(1, 3)), a) if s > 1][0]
q("U08-E-040", TOP_PAR, "Parameter of a parabola from the area between two coaxial parabolas", "Medium", "Inverse/parameter MCQ",
  r"For $a > 1$, the area of the region $\{(x, y) : x^2 \le y \le ax^2,\ y \le 1\}$ is $\frac{1}{3}$. Then $a$ equals",
  r"$\frac{16}{9}$",
  [(r"$4$", r"Uses only the part with $x \ge 0$, $\frac{2}{3}\left(1 - \frac{1}{\sqrt{a}}\right) = \frac{1}{3}$, forgetting the congruent part with $x \le 0$."),
   (r"$\frac{4}{3}$", r"Takes the half-width of $y = ax^2$ at height $y$ as $\frac{\sqrt{y}}{a}$ instead of $\frac{\sqrt{y}}{\sqrt{a}}$, getting $\frac{4}{3}\left(1 - \frac{1}{a}\right) = \frac{1}{3}$."),
   (r"$16$", r"Finds the area enclosed by $y = ax^2$ and $y = 1$ alone, $\frac{4}{3\sqrt{a}} = \frac{1}{3}$, instead of the area between the two parabolas.")],
  r"Use horizontal strips: at height $y \in [0, 1]$ the region consists of two strips, each from $|x| = \sqrt{\frac{y}{a}}$ to $|x| = \sqrt{y}$. Area $= 2\int_0^1\left(\sqrt{y} - \frac{\sqrt{y}}{\sqrt{a}}\right)dy = \frac{4}{3}\left(1 - \frac{1}{\sqrt{a}}\right)$. Setting this equal to $\frac{1}{3}$ gives $\frac{1}{\sqrt{a}} = \frac{3}{4}$, so $a = \frac{16}{9}$.",
  "Mishandling how the width of a parabola scales with its coefficient, or dropping one symmetric half.",
  "U08-E-param-nested-parabolas", "Horizontal strips between two coaxial parabolas, then solve for the coefficient.",
  check=_c040, values=[Rational(16, 9), 4, Rational(4, 3), 16], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 041
def _c041():
    up = Piecewise((x + 1, x <= 1), (2, True))
    lo = Piecewise((0, x <= 1), (x - 1, True))
    c = solve(Eq(x + 1, 2), x)[0]
    return integrate((x + 1) - 0, (x, 0, c)) + integrate(2 - (x - 1), (x, c, 2))
q("U08-E-041", TOP_MOD, "Band inside a square", "Medium", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : |x - y| \le 1,\ 0 \le x \le 2,\ 0 \le y \le 2\}$ is",
  r"$3$",
  [(r"$\frac{7}{2}$", r"Removes only one of the two corner triangles from the square."),
   (r"$2$", r"Removes both corner triangles but takes each to have area $1$ instead of $\frac{1}{2}$."),
   (r"$1$", r"Gives the total area of the two corner triangles, the part excluded by $|x - y| \le 1$.")],
  r"$|x - y| \le 1$ is the band between $y = x - 1$ and $y = x + 1$. Inside the $2 \times 2$ square it removes the triangles near $(2, 0)$ and $(0, 2)$, each with legs $1$ and area $\frac{1}{2}$. Area $= 4 - 1 = 3$; equivalently $\int_0^1(x + 1)\,dx + \int_1^2\left(2 - (x - 1)\right)dx = \frac{3}{2} + \frac{3}{2}$.",
  "Missing one of the two cut-off corners.",
  "U08-E-ineq-band", "Modulus inequality turned into a band, then two pieces.",
  check=_c041, values=[3, Rational(7, 2), 2, 1], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The area of the region $\{(x, y) : |x - y| \le 1,\ 0 \le x \le 2,\ 0 \le y \le 2\}$ is", answer=3))

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 042
def _c042():
    xs = [r for r in real_roots(x**2 + 6 * x - 16) if r > 0]
    p = xs[0]
    return 2 * (area(sqrt(6 * x), 0, p) + area(sqrt(16 - x**2), p, 4))
q("U08-E-042", TOP_CE, "Region common to a circle and a parabola", "Difficult", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : x^2 + y^2 \le 16,\ y^2 \le 6x\}$ is",
  r"$\frac{4}{3}(4\pi + \sqrt{3})$",
  [(r"$\frac{4}{3}(8\pi - \sqrt{3})$", r"Gives the rest of the disc, $16\pi - \frac{4}{3}(4\pi + \sqrt{3})$, the part outside the parabola."),
   (r"$\frac{2}{3}(4\pi + \sqrt{3})$", r"Computes only the part above the $x$-axis and does not double."),
   (r"$\frac{4}{3}(2\pi + \sqrt{3})$", r"Uses $\sin^{-1}\frac{1}{2} = \frac{\pi}{3}$ when evaluating $\int_2^4\sqrt{16 - x^2}\,dx$.")],
  r"$x^2 + 6x = 16$ gives $x = 2$ (with $y = \pm 2\sqrt{3}$). Above the axis the region is $\int_0^2\sqrt{6x}\,dx + \int_2^4\sqrt{16 - x^2}\,dx = \frac{8\sqrt{3}}{3} + \left(4\pi - 2\sqrt{3} - \frac{4\pi}{3}\right) = \frac{8\pi}{3} + \frac{2\sqrt{3}}{3}$. Doubling, the area is $\frac{16\pi}{3} + \frac{4\sqrt{3}}{3} = \frac{4}{3}(4\pi + \sqrt{3})$.",
  "Switching the boundary at the wrong point or misevaluating the inverse sine.",
  "U08-E-circle-parabola", "Intersection, split integral, inverse sine evaluation, symmetry.",
  check=_c042, values=[Rational(4, 3) * (4 * pi + sqrt(3)), Rational(4, 3) * (8 * pi - sqrt(3)), Rational(2, 3) * (4 * pi + sqrt(3)), Rational(4, 3) * (2 * pi + sqrt(3))],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 043
def _c043():
    p = [r for r in real_roots(x**2 - 8 / x) if r > 0][0]      # parabola meets hyperbola
    s = [r for r in real_roots(x**2 - 1) if r > 0][0]           # parabola meets y = 1
    t = solve(Eq(8 / x, 1), x)[0]                               # hyperbola meets y = 1
    return simplify(integrate(x**2 - 1, (x, s, p)) + integrate(8 / x - 1, (x, p, t)))
q("U08-E-043", TOP_MOD, "Region bounded by a parabola, a hyperbola and a line", "Difficult", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : x \ge 0,\ xy \le 8,\ 1 \le y \le x^2\}$ is",
  r"$16\log_e 2 - \frac{14}{3}$",
  [(r"$16\log_e 2 - \frac{11}{3}$", r"On $[1, 2]$ integrates $x^2$ alone, forgetting the lower boundary $y = 1$ there."),
   (r"$16\log_e 2 + \frac{4}{3}$", r"On $[2, 8]$ integrates $\frac{8}{x}$ alone, forgetting the lower boundary $y = 1$ there."),
   (r"$16\log_e 2 - 6$", r"Uses only the piece under the hyperbola from $x = 2$ to $x = 8$, omitting the piece under the parabola.")],
  r"The upper boundary is $\min\left(x^2, \frac{8}{x}\right)$, which switches at $x^3 = 8$, i.e. $x = 2$; the region starts where $x^2 = 1$ ($x = 1$) and ends where $\frac{8}{x} = 1$ ($x = 8$). Area $= \int_1^2(x^2 - 1)\,dx + \int_2^8\left(\frac{8}{x} - 1\right)dx = \frac{4}{3} + (8\log_e 4 - 6) = 16\log_e 2 - \frac{14}{3}$.",
  "Dropping the lower boundary $y = 1$ on one of the pieces.",
  "U08-E-ineq-hyperbola", "Three boundaries, three intersection points, two pieces.",
  check=_c043, values=[16 * log(2) - Rational(14, 3), 16 * log(2) - Rational(11, 3), 16 * log(2) + Rational(4, 3), 16 * log(2) - 6],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 044
def _c044():
    f = 1 - Abs(x**2 - 1)
    rts = real_roots(Abs(x**2 - 1) - 1)
    return area(f, rts[0], rts[-1])
q("U08-E-044", TOP_MOD, "Modulus of a quadratic and a horizontal line", "Difficult", "Multi-step computation MCQ",
  r"The total area of the region enclosed between the curve $y = |x^2 - 1|$ and the line $y = 1$ is",
  r"$\frac{8\sqrt{2} - 8}{3}$",
  [(r"$\frac{2}{3}$", r"Counts only the part with $|x| \le 1$, where the curve is $1 - x^2$."),
   (r"$\frac{8\sqrt{2}}{3}$", r"Ignores the modulus and finds the region between $y = x^2 - 1$ and $y = 1$."),
   (r"$\frac{4\sqrt{2} - 4}{3}$", r"Counts only the part with $x \ge 0$.")],
  r"$|x^2 - 1| = 1$ gives $x = 0, \pm\sqrt{2}$, and the curve stays below $y = 1$ on $[-\sqrt{2}, \sqrt{2}]$. For $0 \le x \le 1$ the gap is $1 - (1 - x^2) = x^2$, giving $\frac{1}{3}$; for $1 \le x \le \sqrt{2}$ it is $2 - x^2$, giving $\frac{4\sqrt{2}}{3} - \frac{5}{3}$. Doubling, the area is $2\left(\frac{4\sqrt{2} - 4}{3}\right) = \frac{8\sqrt{2} - 8}{3}$.",
  "Ignoring the reflection of the negative part of the quadratic.",
  "U08-E-mod-quadratic", "Modulus graph, two pieces on each side and symmetry.",
  check=_c044, values=[(8 * sqrt(2) - 8) / 3, Rational(2, 3), 8 * sqrt(2) / 3, (4 * sqrt(2) - 4) / 3], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 045
def _c045():
    m = Symbol('m', real=True)
    ms = solve(discriminant(x**2 + 1 - m * x, x), m)
    pts = sorted([solve(x**2 + 1 - mm * x, x)[0] for mm in ms], key=lambda t: float(t))
    low = Piecewise((ms[0] * x, x < 0), (ms[1] * x, True)) if ms[0] < 0 else Piecewise((ms[1] * x, x < 0), (ms[0] * x, True))
    return integrate(x**2 + 1 - low, (x, pts[0], pts[1]))
q("U08-E-045", TOP_LP, "Parabola and its tangents from the origin", "Difficult", "Multi-step computation MCQ",
  r"Two tangents are drawn from the origin to the parabola $y = x^2 + 1$. The area of the region enclosed by the parabola and these two tangents is",
  r"$\frac{2}{3}$",
  [(r"$\frac{1}{3}$", r"Computes the region on one side of the $y$-axis only."),
   (r"$\frac{8}{3}$", r"Finds the area under the parabola from $x = -1$ to $x = 1$ without removing the two triangles under the tangents."),
   (r"$\frac{5}{3}$", r"Removes only one of the two triangles, each of area $1$.")],
  r"$y = mx$ touches $y = x^2 + 1$ when $x^2 - mx + 1 = 0$ has a double root, i.e. $m = \pm 2$, with contact points $x = \pm 1$. The region lies between the parabola and $y = 2|x|$ on $[-1, 1]$: area $= 2\int_0^1(x^2 + 1 - 2x)\,dx = 2\int_0^1(x - 1)^2\,dx = \frac{2}{3}$.",
  "Forgetting to subtract the area under the tangents.",
  "U08-E-tangent-region", "Tangency condition, then area with symmetry.",
  check=_c045, values=[Rational(2, 3), Rational(1, 3), Rational(8, 3), Rational(5, 3)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 046
def _c046():
    s1 = 4 * area(sqrt(1 - x**2) - (1 - x), 0, 1)
    s2 = 4 * area(x * sqrt(1 - x**2), 0, 1)
    return (simplify(s1 - (pi - 1)) == 0, simplify(s2 - Rational(2, 3)) == 0)
q("U08-E-046", TOP_MOD, "Disc minus a square; a figure-of-eight curve", "Difficult", "Statement-based MCQ",
  r"Statement I: The area of the region $\{(x, y) : x^2 + y^2 \le 1 \le |x| + |y|\}$ is $\pi - 1$. Statement II: The area of the region enclosed by the curve $y^2 = x^2(1 - x^2)$ is $\frac{2}{3}$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Takes the inscribed square to have area $1$ (side $1$) and counts only the part of the second curve above the $x$-axis."),
   (ST_TF, r"Takes the inscribed square to have area $1$, but evaluates Statement II correctly."),
   (ST_FT, r"Evaluates Statement I correctly, but counts only the half of the second curve above the $x$-axis.")],
  r"The square $|x| + |y| = 1$ has side $\sqrt{2}$ and area $2$, so the first region has area $\pi - 2$: Statement I is false. The curve $y = \pm x\sqrt{1 - x^2}$ is symmetric in both axes, so its area is $4\int_0^1 x\sqrt{1 - x^2}\,dx = 4\cdot\frac{1}{3} = \frac{4}{3}$: Statement II is false.",
  "Using the wrong side length for the square, or counting only half of a symmetric curve.",
  "U08-E-stmt-symmetry", "Two regions needing careful symmetry arguments.",
  check=_c046, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 047
def _c047():
    m = Symbol('m', real=True)
    k = 2 + m                                   # x^2 - 2x = mx  ->  x = 0, 2 + m
    sols = solve(Eq(Abs(k)**3 / 6, 36), m)
    # confirm the formula against a direct integral for each root
    for s in sols:
        top = 2 + s
        lo, hi = sorted([0, top], key=lambda t: float(t))
        assert simplify(area(s * x - (x**2 - 2 * x), lo, hi) - 36) == 0
    return sum(sols)
q("U08-E-047", TOP_PAR, "All slopes giving a prescribed area", "Difficult", "Inverse/parameter MCQ",
  r"The area of the region enclosed by the parabola $y = x^2 - 2x$ and the line $y = mx$, where $m \in \mathbb{R}$, is $36$. The sum of all possible values of $m$ is",
  r"$-4$",
  [(r"$0$", r"Drops the $-2x$ term, so the area is $\frac{|m|^3}{6} = 36$, giving $m = \pm 6$."),
   (r"$4$", r"Keeps only the case $2 + m > 0$, giving the single value $m = 4$."),
   (r"$-8$", r"Keeps only the case $2 + m < 0$, giving the single value $m = -8$.")],
  r"$x^2 - 2x = mx$ gives $x = 0$ and $x = 2 + m$, and the enclosed area is $\frac{|2 + m|^3}{6}$. Setting this equal to $36$ gives $|2 + m| = 6$, so $m = 4$ or $m = -8$. Their sum is $-4$.",
  "Forgetting that the second intersection can lie on either side of the origin.",
  "U08-E-param-slope", "Area as a function of the slope, with two sign cases.",
  check=_c047, values=[-4, 0, 4, -8], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 048
def _c048():
    f = x**2 - 4 * x + 3
    rts = real_roots(f - 3)
    return area(3 - Abs(f), rts[0], rts[-1])
q("U08-E-048", TOP_MOD, "Reflected parabola under a horizontal line", "Difficult", "Multi-step computation MCQ",
  r"The area of the region enclosed between the curve $y = |x^2 - 4x + 3|$ and the line $y = 3$ is",
  r"$8$",
  [(r"$\frac{32}{3}$", r"Ignores the modulus and finds the region between $y = x^2 - 4x + 3$ and $y = 3$."),
   (r"$\frac{28}{3}$", r"Allows for the reflected dip on $[1, 3]$ but subtracts its area $\frac{4}{3}$ only once."),
   (r"$4$", r"Finds the area under $y = |x^2 - 4x + 3|$ on $[0, 4]$ instead of the area between the curve and the line.")],
  r"$|x^2 - 4x + 3| = 3$ only when $x^2 - 4x = 0$, i.e. $x = 0, 4$. On $[0, 4]$, $\int_0^4|x^2 - 4x + 3|\,dx = \frac{4}{3} + \frac{4}{3} + \frac{4}{3} = 4$ (pieces on $[0,1]$, $[1,3]$, $[3,4]$). Area $= \int_0^4 3\,dx - 4 = 12 - 4 = 8$.",
  "Forgetting that reflecting the dip removes its area twice from the region below the line.",
  "U08-E-mod-quadratic", "Modulus reflection, three pieces, subtraction from a rectangle.",
  check=_c048, values=[8, Rational(32, 3), Rational(28, 3), 4], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The area of the region enclosed between the curve $y = |x^2 - 4x + 3|$ and the line $y = 3$ is", answer=8))

# ---------------------------------------------------------------- 049
def _c049():
    rts = real_roots(4 * x - x**2 - 2 * x)
    return area(sqrt(4 * x - x**2) - sqrt(2 * x), rts[0], rts[-1])
q("U08-E-049", TOP_CE, "Inside a circle and outside a parabola", "Difficult", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : x^2 + y^2 \le 4x,\ y^2 \ge 2x,\ y \ge 0\}$ is",
  r"$\pi - \frac{8}{3}$",
  [(r"$2\pi - \frac{8}{3}$", r"Integrates the circle over $[0, 4]$ (the whole upper semicircle) but the parabola only over $[0, 2]$."),
   (r"$\pi - \frac{4\sqrt{2}}{3}$", r"Uses $y = \sqrt{x}$ for the parabola, dropping the factor $\sqrt{2}$."),
   (r"$\pi + \frac{8}{3}$", r"Adds the area under the parabola to the quarter disc instead of subtracting it.")],
  r"The circle is $(x - 2)^2 + y^2 = 4$; it meets $y^2 = 2x$ where $4x - x^2 = 2x$, i.e. $x = 0, 2$. For $0 \le x \le 2$ the region lies between $y = \sqrt{2x}$ and $y = \sqrt{4x - x^2}$. The circle part is a quarter of the disc, $\pi$, and $\int_0^2\sqrt{2x}\,dx = \frac{8}{3}$, so the area is $\pi - \frac{8}{3}$.",
  "Integrating the circle beyond the intersection with the parabola.",
  "U08-E-circle-parabola", "Reading three inequalities, then quarter disc minus a parabolic area.",
  check=_c049, values=[pi - Rational(8, 3), 2 * pi - Rational(8, 3), pi - 4 * sqrt(2) / 3, pi + Rational(8, 3)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 050
def _c050():
    rts = real_roots(log(x) - log(x)**2)
    return area(log(x) - log(x)**2, rts[0], rts[-1])
q("U08-E-050", TOP_PP, "Between $\\log_e x$ and $(\\log_e x)^2$", "Difficult", "Multi-step computation MCQ",
  r"The area of the region enclosed between the curves $y = \log_e x$ and $y = (\log_e x)^2$ is",
  r"$3 - e$",
  [(r"$e - 2$", r"Finds only $\int_1^e(\log_e x)^2\,dx$, the area under the lower curve."),
   (r"$1$", r"Finds only $\int_1^e\log_e x\,dx$, the area under the upper curve."),
   (r"$2$", r"Takes $\int\log_e x\,dx = x\log_e x$ (dropping $-x$), so the first integral becomes $e$ and the answer $e - (e - 2)$.")],
  r"$\log_e x = (\log_e x)^2$ gives $\log_e x = 0$ or $1$, i.e. $x = 1, e$, and $\log_e x \ge (\log_e x)^2$ between. $\int_1^e\log_e x\,dx = 1$ and $\int_1^e(\log_e x)^2\,dx = \left[x(\log_e x)^2 - 2x\log_e x + 2x\right]_1^e = e - 2$. Area $= 1 - (e - 2) = 3 - e$.",
  "Errors in the by-parts antiderivatives of $\\log_e x$ and $(\\log_e x)^2$.",
  "U08-E-log-curves", "Limits from a log equation and two by-parts integrals.",
  check=_c050, values=[3 - E, E - 2, 1, 2], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 051
def _c051():
    # normal to y^2 = 4x at (1, 2): slope of tangent dy/dx = 2/y
    slope_t = (2 / y).subs(y, 2)
    xn = 1 - slope_t * (y - 2)      # normal: x - 1 = -(dy/dx)(y - 2)
    ys = real_roots(xn - y**2 / 4, y)
    return area(xn - y**2 / 4, ys[0], ys[-1], y)
q("U08-E-051", TOP_LP, "Parabola cut off by a normal", "Difficult", "Multi-step computation MCQ",
  r"The area of the region enclosed by the parabola $y^2 = 4x$ and its normal at the point $(1, 2)$ is",
  r"$\frac{64}{3}$",
  [(r"$\frac{256}{3}$", r"Writes the strip width $3 - y - \frac{y^2}{4}$ as $-(y - 2)(y + 6)$, dropping the factor $\frac{1}{4}$."),
   (r"$18$", r"Treats the $x$-axis as a boundary and integrates only from $y = -6$ to $y = 0$."),
   (r"$\frac{128}{3}$", r"Uses $\frac{1}{4}\cdot\frac{(\beta - \alpha)^3}{3}$ in place of $\frac{1}{4}\cdot\frac{(\beta - \alpha)^3}{6}$.")],
  r"The slope of the tangent at $(1, 2)$ is $\frac{2}{y} = 1$, so the normal is $x + y = 3$. With $x = 3 - y$ and $x = \frac{y^2}{4}$: $y^2 + 4y - 12 = 0$, so $y = -6, 2$. Area $= \int_{-6}^{2}\left(3 - y - \frac{y^2}{4}\right)dy = \frac{1}{4}\int_{-6}^{2}(2 - y)(y + 6)\,dy = \frac{1}{4}\cdot\frac{8^3}{6} = \frac{64}{3}$.",
  "Mishandling the leading coefficient when using the parabolic segment formula.",
  "U08-E-normal-region", "Normal line, horizontal strips, and a wide segment.",
  check=_c051, values=[Rational(64, 3), Rational(256, 3), 18, Rational(128, 3)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 052
def _c052():
    m = Symbol('m', real=True)
    p = Poly(x**2 - (m * (x - 1) + 4), x)
    s = -p.all_coeffs()[1]; pr = p.all_coeffs()[2]
    d2 = expand(s**2 - 4 * pr)                         # (beta - alpha)^2
    m0 = solve(diff(d2, m), m)[0]
    dmin = d2.subs(m, m0)
    return simplify(dmin**Rational(3, 2) / 6)
q("U08-E-052", TOP_LP, "Least area cut off by a chord through a fixed point", "Difficult", "Multi-step computation MCQ",
  r"A line through the point $(1, 4)$ cuts the parabola $y = x^2$ at two points. The least possible area of the region enclosed by the line and the parabola is",
  r"$4\sqrt{3}$",
  [(r"$8\sqrt{3}$", r"Uses $\frac{(\beta - \alpha)^3}{3}$ for the segment area instead of $\frac{(\beta - \alpha)^3}{6}$."),
   (r"$2\sqrt{3}$", r"Uses $\frac{(\beta - \alpha)^3}{12}$ for the segment area."),
   (r"$\frac{32}{3}$", r"Assumes the horizontal line $y = 4$ gives the least area, with $\beta - \alpha = 4$.")],
  r"The line $y - 4 = m(x - 1)$ meets the parabola where $x^2 - mx + m - 4 = 0$, so $(\beta - \alpha)^2 = m^2 - 4m + 16 = (m - 2)^2 + 12 \ge 12$. The enclosed area is $\frac{(\beta - \alpha)^3}{6}$, least when $m = 2$: $\frac{12\sqrt{12}}{6} = \frac{24\sqrt{3}}{6} = 4\sqrt{3}$.",
  "Assuming the symmetric (horizontal) chord gives the extreme area.",
  "U08-E-min-chord-area", "Segment area formula plus minimisation of a quadratic in the slope.",
  check=_c052, values=[4 * sqrt(3), 8 * sqrt(3), 2 * sqrt(3), Rational(32, 3)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 053
def _c053():
    xs = [r for r in real_roots(4 - x**2 - (x**2 / 3)**2)]
    f = sqrt(4 - x**2) - x**2 / 3
    xs = [r for r in xs]
    return area(f, xs[0], xs[-1])
q("U08-E-053", TOP_CE, "Disc above a parabola", "Difficult", "Multi-step computation MCQ",
  r"The area of the region $\{(x, y) : x^2 + y^2 \le 4,\ x^2 \le 3y\}$ is",
  r"$\frac{4\pi}{3} + \frac{\sqrt{3}}{3}$",
  [(r"$\frac{8\pi}{3} - \frac{\sqrt{3}}{3}$", r"Gives the rest of the disc, $4\pi - \left(\frac{4\pi}{3} + \frac{\sqrt{3}}{3}\right)$."),
   (r"$\frac{4\pi}{3} + \frac{4\sqrt{3}}{3}$", r"Uses the circular sector above the chord $y = 1$ instead of the segment, not removing the triangle of area $\sqrt{3}$."),
   (r"$\frac{2\pi}{3} + \frac{\sqrt{3}}{3}$", r"Uses $\sin^{-1}\frac{\sqrt{3}}{2} = \frac{\pi}{6}$ when evaluating $\int_{-\sqrt{3}}^{\sqrt{3}}\sqrt{4 - x^2}\,dx$.")],
  r"Substituting $x^2 = 3y$ into the circle: $y^2 + 3y - 4 = 0$, so $y = 1$ and $x = \pm\sqrt{3}$. Area $= \int_{-\sqrt{3}}^{\sqrt{3}}\left(\sqrt{4 - x^2} - \frac{x^2}{3}\right)dx = \left(\sqrt{3} + \frac{4\pi}{3}\right) - \frac{2\sqrt{3}}{3} = \frac{4\pi}{3} + \frac{\sqrt{3}}{3}$.",
  "Confusing a sector with a segment, or misevaluating the inverse sine.",
  "U08-E-circle-parabola", "Intersection, circle integral with inverse sine, subtraction.",
  check=_c053, values=[4 * pi / 3 + sqrt(3) / 3, 8 * pi / 3 - sqrt(3) / 3, 4 * pi / 3 + 4 * sqrt(3) / 3, 2 * pi / 3 + sqrt(3) / 3],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 054
def _c054():
    f = x**3 - 3 * x
    t = f.subs(x, -1) + diff(f, x).subs(x, -1) * (x + 1)
    rts = real_roots(f - t)
    return area(t - f, rts[0], rts[-1])
q("U08-E-054", TOP_LP, "Cubic and its tangent at a turning point", "Difficult", "Multi-step computation MCQ",
  r"The area of the region enclosed by the curve $y = x^3 - 3x$ and its tangent at the point where $x = -1$ is",
  r"$\frac{27}{4}$",
  [(r"$\frac{9}{2}$", r"Applies the parabola-and-line shortcut $\frac{(\beta - \alpha)^3}{6}$ with $\alpha = -1$, $\beta = 2$ to the cubic, getting $\frac{27}{6} = \frac{9}{2}$."),
   (r"$4$", r"Assumes the tangent meets the curve again at $x = 1$ and integrates over $[-1, 1]$."),
   (r"$\frac{45}{4}$", r"Integrates $3x$ as $3x^2$ (dropping the $\frac{1}{2}$) in $\int_{-1}^{2}(2 - x^3 + 3x)\,dx$.")],
  r"At $x = -1$, $y = 2$ and $y' = 3x^2 - 3 = 0$, so the tangent is $y = 2$. Then $x^3 - 3x - 2 = (x + 1)^2(x - 2) = 0$ gives the second point $x = 2$. Area $= \int_{-1}^{2}(2 - x^3 + 3x)\,dx = \left[2x - \frac{x^4}{4} + \frac{3x^2}{2}\right]_{-1}^{2} = 6 + \frac{3}{4} = \frac{27}{4}$.",
  "Assuming symmetry fixes the second intersection of a tangent with a cubic.",
  "U08-E-cubic-tangent", "Tangent, factorisation with a double root, one integral.",
  check=_c054, values=[Rational(27, 4), Rational(9, 2), 4, Rational(45, 4)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 055
def _c055():
    f = Rational(1, 2) * sqrt(16 - x**2) - (2 - Abs(x) / 2)
    return area(f, -4, 4)
q("U08-E-055", TOP_CE, "Ellipse above a V-shaped boundary", "Difficult", "Multi-step computation MCQ",
  r"The area of the region $\left\{(x, y) : \frac{x^2}{16} + \frac{y^2}{4} \le 1,\ y \ge 2 - \frac{|x|}{2}\right\}$ is",
  r"$4\pi - 8$",
  [(r"$2\pi - 4$", r"Computes only the part with $x \ge 0$."),
   (r"$8\pi - 8$", r"Subtracts the triangle from the whole ellipse instead of the upper half."),
   (r"$4\pi - 4$", r"Takes the triangle with vertices $(-4, 0)$, $(4, 0)$, $(0, 2)$ to have area $4$ (base taken as $4$).")],
  r"The lines $y = 2 - \frac{|x|}{2}$ join $(0, 2)$ to $(\pm 4, 0)$, the ends of the axes, so for $|x| \le 4$ the condition forces $y \ge 0$. The region is the upper half of the ellipse minus the triangle with vertices $(-4, 0)$, $(4, 0)$, $(0, 2)$: $\frac{\pi\cdot 4\cdot 2}{2} - \frac{1}{2}\cdot 8\cdot 2 = 4\pi - 8$.",
  "Not recognising which part of the ellipse the modulus inequality keeps.",
  "U08-E-ellipse-chord", "Modulus inequality with an ellipse; reduce to standard pieces.",
  check=_c055, values=[4 * pi - 8, 2 * pi - 4, 8 * pi - 8, 4 * pi - 4], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 056
def _c056():
    a = Symbol('a', positive=True)
    A = integrate(exp(x) - exp(-x), (x, 0, a))
    return [s for s in solve(Eq(A, Rational(1, 2)), a) if s > 0][0]
q("U08-E-056", TOP_PAR, "Upper limit from the area between $e^x$ and $e^{-x}$", "Difficult", "Inverse/parameter MCQ",
  r"For $a > 0$, the area of the region bounded by the curves $y = e^x$, $y = e^{-x}$ and the line $x = a$ is $\frac{1}{2}$. Then $a$ equals",
  r"$\log_e 2$",
  [(r"$\log_e\frac{5}{2}$", r"Reaches $e^a + e^{-a} = \frac{5}{2}$ but then drops $e^{-a}$, setting $e^a = \frac{5}{2}$."),
   (r"$\log_e\frac{3}{2}$", r"Ignores the curve $y = e^{-x}$ and uses the area under $y = e^x$ alone: $e^a - 1 = \frac{1}{2}$."),
   (r"$\log_e\frac{1 + \sqrt{17}}{4}$", r"Integrates $e^{-x}$ as $e^{-x}$ (sign slip), getting $e^a - e^{-a} = \frac{1}{2}$.")],
  r"On $[0, a]$, $e^x \ge e^{-x}$, so the area is $\int_0^a(e^x - e^{-x})\,dx = e^a + e^{-a} - 2 = \frac{1}{2}$. With $t = e^a > 1$: $t + \frac{1}{t} = \frac{5}{2}$, i.e. $2t^2 - 5t + 2 = 0$, so $t = 2$ (the root $\frac{1}{2}$ gives $a < 0$). Hence $a = \log_e 2$.",
  "Mishandling the reciprocal term when solving the exponential equation.",
  "U08-E-exp-pair", "Area in terms of $a$, then a quadratic in $e^a$ with a root rejected.",
  check=_c056, values=[log(2), log(Rational(5, 2)), log(Rational(3, 2)), log((1 + sqrt(17)) / 4)], cognitive="Analysis", source_class="XII")
