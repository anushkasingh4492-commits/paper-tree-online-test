import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools

# ---------------------------------------------------------------- helpers
X, Y = symbols('x y', real=True)
T_ = Symbol('t', real=True)
K_ = Symbol('k', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

MONOS = [X**2, X*Y, Y**2, X, Y, Integer(1)]


def canon(expr):
    """Normalised coefficient tuple of a curve/line expr = 0 (degree <= 2 in x, y)."""
    p = Poly(expand(expr), X, Y)
    cs = [p.coeff_monomial(m) for m in MONOS]
    lead = [c for c in cs if c != 0][0]
    return tuple(simplify(c / lead) for c in cs)


def pt(*c):
    return tuple(nsimplify(v) for v in c)


def dist(P, Q):
    return sqrt((P[0] - Q[0])**2 + (P[1] - Q[1])**2)


def area3(P, Q, R):
    return Abs(P[0]*(Q[1] - R[1]) + Q[0]*(R[1] - P[1]) + R[0]*(P[1] - Q[1])) / 2


def shoelace(V):
    n = len(V)
    return Abs(sum(V[i][0]*V[(i+1) % n][1] - V[(i+1) % n][0]*V[i][1] for i in range(n))) / 2


def section(P, Q, m, n):
    """Point dividing PQ internally in m:n."""
    return tuple(simplify((m*Q[i] + n*P[i]) / (m + n)) for i in range(2))


def centroid(P, Q, R):
    return tuple(simplify((P[i] + Q[i] + R[i]) / 3) for i in range(2))


def circumcentre(P, Q, R):
    h, k = symbols('h k')
    s = solve([(h - P[0])**2 + (k - P[1])**2 - (h - Q[0])**2 - (k - Q[1])**2,
               (h - P[0])**2 + (k - P[1])**2 - (h - R[0])**2 - (k - R[1])**2], [h, k], dict=True)[0]
    return (s[h], s[k])


def orthocentre(P, Q, R):
    h, k = symbols('h k')
    s = solve([(h - P[0])*(Q[0] - R[0]) + (k - P[1])*(Q[1] - R[1]),
               (h - Q[0])*(P[0] - R[0]) + (k - Q[1])*(P[1] - R[1])], [h, k], dict=True)[0]
    return (simplify(s[h]), simplify(s[k]))


def incentre(P, Q, R):
    a, b, c = dist(Q, R), dist(P, R), dist(P, Q)
    return tuple(simplify((a*P[i] + b*Q[i] + c*R[i]) / (a + b + c)) for i in range(2))


def meet(l1, l2):
    s = solve([l1, l2], [X, Y], dict=True)[0]
    return (s[X], s[Y])


TOPIC = "Cartesian coordinates and triangle geometry"

# ================================================================ EASY (15)

def _c1():
    s = solve(Eq(dist((X, 0), (2, -5))**2, dist((X, 0), (-2, 9))**2), X)
    return (s[0], 0)
q("U10-A-001", "Distance formula", "Equidistant point on an axis", "Easy", "Single-step computation MCQ",
  r"The point on the $x$-axis which is equidistant from the points $(2, -5)$ and $(-2, 9)$ is",
  r"$(-7, 0)$",
  [(r"$(7, 0)$", r"Writes $(x-2)^2 - (x+2)^2 = 8x$ (sign slip), so $8x = 56$ and $x = 7$."),
   (r"$\left(-\frac{1}{2}, 0\right)$", r"Leaves the $y$-differences unsquared, solving $(x-2)^2 + 5 = (x+2)^2 + 9$ to get $-8x = 4$."),
   (r"$(0, 0)$", r"Drops the $y$-terms, solving $(x-2)^2 = (x+2)^2$ to get $x = 0$.")],
  r"Let the point be $(x, 0)$. Then $(x-2)^2 + 25 = (x+2)^2 + 81$, so $-4x + 29 = 4x + 85$, giving $-8x = 56$ and $x = -7$. The point is $(-7, 0)$.",
  r"Sign slips when expanding the squared differences, or forgetting the $y$-contributions.",
  "U10-A-axis-equidistant", "One equation from the distance formula, solved linearly.",
  check=_c1, values=[(-7, 0), (7, 0), (Rational(-1, 2), 0), (0, 0)], cognitive="Application")

q("U10-A-002", "Section formula", "Internal division", "Easy", "Single-step computation MCQ",
  r"The point which divides the line segment joining $P(2, 3)$ and $Q(8, -6)$ internally in the ratio $1 : 2$ is",
  r"$(4, 0)$",
  [(r"$(6, -3)$", r"Attaches the weights to the wrong ends: $\left(\frac{2 \cdot 8 + 1 \cdot 2}{3}, \frac{2(-6) + 1 \cdot 3}{3}\right)$, which is the $2 : 1$ point."),
   (r"$\left(5, -\frac{3}{2}\right)$", r"Takes the midpoint of $PQ$, ignoring the ratio."),
   (r"$(-4, 12)$", r"Uses the external division formula $\left(\frac{1 \cdot 8 - 2 \cdot 2}{1-2}, \frac{1(-6) - 2 \cdot 3}{1-2}\right)$.")],
  r"With $m : n = 1 : 2$, the point is $\left(\frac{1 \cdot 8 + 2 \cdot 2}{3}, \frac{1(-6) + 2 \cdot 3}{3}\right) = (4, 0)$.",
  r"Pairing the ratio weights with the wrong end points.",
  "U10-A-section-internal", "Direct use of the section formula.",
  check=lambda: section((2, 3), (8, -6), 1, 2),
  values=[(4, 0), (6, -3), (5, Rational(-3, 2)), (-4, 12)], cognitive="Application")

def _c3():
    lam = Symbol('lam')
    s = solve(Eq((lam*6 + 1*(-4)) / (lam + 1), 0), lam)
    return s[0]  # signed ratio: positive means internal
q("U10-A-003", "Section formula", "Ratio in which an axis divides a segment", "Easy", "Single-step computation MCQ",
  r"The $x$-axis divides the line segment joining $(3, -4)$ and $(-2, 6)$ in the ratio",
  r"$2 : 3$ internally",
  [(r"$3 : 2$ internally", r"Uses the $x$-coordinates, $-\frac{x_1}{x_2} = \frac{3}{2}$, which gives the ratio for the $y$-axis."),
   (r"$2 : 3$ externally", r"Uses $\frac{y_1}{y_2} = -\frac{4}{6}$ without the minus sign in $-\frac{y_1}{y_2}$, reading the negative value as external."),
   (r"$3 : 2$ externally", r"Inverts the ratio to $\frac{y_2}{y_1} = -\frac{3}{2}$ and reads the negative value as external.")],
  r"If the ratio is $\lambda : 1$, the dividing point has ordinate $\frac{6\lambda - 4}{\lambda + 1} = 0$, so $\lambda = \frac{2}{3}$. Since $\lambda > 0$ the division is internal, in the ratio $2 : 3$.",
  r"Using the $x$-coordinates for the $x$-axis, or dropping the sign in $-\frac{y_1}{y_2}$.",
  "U10-A-axis-divides-segment", "One linear equation from the section formula.",
  check=_c3, values=[Rational(2, 3), Rational(3, 2), Rational(-2, 3), Rational(-3, 2)], cognitive="Application")

def _c4():
    a, b = symbols('a b')
    s = solve([Eq((4 - 1 + a) / 3, 2), Eq((3 - 2 + b) / 3, -1)], [a, b], dict=True)[0]
    return (s[a], s[b])
q("U10-A-004", "Centroid", "Third vertex from the centroid", "Easy", "Single-step computation MCQ",
  r"The centroid of triangle $PQR$ is $(2, -1)$. If $P = (4, 3)$ and $Q = (-1, -2)$, then $R$ is",
  r"$(3, -4)$",
  [(r"$(1, -3)$", r"Uses $R = 2G - P - Q$, as if the centroid were the average of only two points."),
   (r"$(9, -2)$", r"Adds instead of subtracting: $R = 3G + P + Q$."),
   (r"$(1, -8)$", r"Takes $R = 3G - P + Q$, slipping the sign of $Q$.")],
  r"$R = 3G - P - Q = (6 - 4 + 1, -3 - 3 + 2) = (3, -4)$.",
  r"Using the factor $2$ in place of $3$ when recovering a vertex from the centroid.",
  "U10-A-centroid-third-vertex", "Direct reversal of the centroid formula.",
  check=_c4, values=[(3, -4), (1, -3), (9, -2), (1, -8)], cognitive="Application")

def _c5():
    return solve(Eq((1 - (-1)) / (2 - K_), (5 - 1) / (4 - 2)), K_)[0]
q("U10-A-005", "Slope of a line", "Collinearity by slopes", "Easy", "Inverse/parameter MCQ",
  r"If the points $(k, -1)$, $(2, 1)$ and $(4, 5)$ are collinear, then $k$ equals",
  r"$1$",
  [(r"$3$", r"Writes the first slope as $\frac{1 - (-1)}{k - 2} = 2$, mixing the order of the points."),
   (r"$-2$", r"Inverts only the first slope, writing it as $\frac{\Delta x}{\Delta y} = \frac{2-k}{2}$, while keeping the second slope as $2$; then $\frac{2-k}{2} = 2$ gives $k = -2$."),
   (r"$\frac{4}{3}$", r"Computes the second slope as $\frac{5-(-1)}{4-2} = 3$, mixing points, and solves $\frac{2}{2-k} = 3$.")],
  r"The slope through $(2, 1)$ and $(4, 5)$ is $\frac{4}{2} = 2$. Collinearity needs $\frac{1-(-1)}{2-k} = 2$, so $2 - k = 1$ and $k = 1$.",
  r"Mixing the order of points in the slope formula.",
  "U10-A-collinear-slope", "One slope equality, solved linearly.",
  check=_c5, values=[1, 3, -2, Rational(4, 3)], cognitive="Application")

def _c6():
    m2 = Rational(-2 - 4, 3 - (-1))
    return solve(Eq((3 - K_) / (8 - 2) * m2, -1), K_)[0]
q("U10-A-006", "Parallel and perpendicular lines", "Perpendicularity by slopes", "Easy", "Inverse/parameter MCQ",
  r"The line through $(2, k)$ and $(8, 3)$ is perpendicular to the line through $(-1, 4)$ and $(3, -2)$. Then $k$ equals",
  r"$-1$",
  [(r"$12$", r"Uses the parallel condition $\frac{3-k}{6} = -\frac{3}{2}$."),
   (r"$-6$", r"Takes the reciprocal slope $\frac{3}{2}$ without changing sign, i.e. $\frac{3-k}{6} = \frac{3}{2}$."),
   (r"$7$", r"Takes the perpendicular slope as $-\frac{2}{3}$, slipping a sign: $\frac{3-k}{6} = -\frac{2}{3}$.")],
  r"The second line has slope $\frac{-2-4}{3+1} = -\frac{3}{2}$, so the first must have slope $\frac{2}{3}$. Then $\frac{3-k}{8-2} = \frac{2}{3}$ gives $3 - k = 4$, so $k = -1$.",
  r"Confusing the parallel and perpendicular conditions on slopes.",
  "U10-A-perpendicular-slope-param", "One slope condition, solved linearly.",
  check=_c6, values=[-1, 12, -6, 7], cognitive="Application")

def _c7():
    L = 3*X - 4*Y + 12
    return solve(L.subs(Y, 0), X)[0] + solve(L.subs(X, 0), Y)[0]
q("U10-A-007", "Intercepts of a line", "Sum of intercepts", "Easy", "Single-step computation MCQ",
  r"The sum of the intercepts made by the line $3x - 4y + 12 = 0$ on the coordinate axes is",
  r"$-1$",
  [(r"$1$", r"Computes the intercepts as $\frac{12}{3} = 4$ and $\frac{12}{-4} = -3$, dropping the minus sign in $-\frac{c}{a}$, $-\frac{c}{b}$."),
   (r"$7$", r"Adds the lengths $4 + 3$ of the intercepts, ignoring their signs."),
   (r"$-7$", r"Takes both intercepts as $-\frac{12}{3} = -4$ and $-\frac{12}{4} = -3$, ignoring the sign of the $y$ coefficient.")],
  r"Putting $y = 0$ gives $x = -4$; putting $x = 0$ gives $y = 3$. The sum of the intercepts is $-4 + 3 = -1$.",
  r"Treating intercepts as lengths, or slipping the sign of $-\frac{c}{a}$.",
  "U10-A-intercepts-sum", "Two substitutions.",
  check=_c7, values=[-1, 1, 7, -7], cognitive="Application")

q("U10-A-008", "Area of a triangle", "Area from vertices", "Easy", "Single-step computation MCQ",
  r"The area of the triangle with vertices $(1, -1)$, $(-4, 6)$ and $(-3, -5)$ is",
  r"$24$",
  [(r"$48$", r"Omits the factor $\frac{1}{2}$ in the determinant formula."),
   (r"$8$", r"Slips the sign of the middle term: $\frac{1}{2}|11 - 16 + 21|$."),
   (r"$3$", r"Slips the sign of the last term: $\frac{1}{2}|11 + 16 - 21|$.")],
  r"Area $= \frac{1}{2}|1(6+5) + (-4)(-5+1) + (-3)(-1-6)| = \frac{1}{2}|11 + 16 + 21| = 24$.",
  r"Dropping the factor $\frac{1}{2}$ or slipping a sign in the determinant expansion.",
  "U10-A-area-triangle-basic", "Direct use of the area formula.",
  check=lambda: area3((1, -1), (-4, 6), (-3, -5)), values=[24, 48, 8, 3], cognitive="Application",
  numerical=dict(question=r"The area of the triangle with vertices $(1, -1)$, $(-4, 6)$ and $(-3, -5)$ is", answer=24))

def _c9():
    P, Q, R = Matrix([1, 2]), Matrix([4, 3]), Matrix([6, 6])
    S = P + R - Q
    return (S[0], S[1])
q("U10-A-009", "Section formula", "Fourth vertex of a parallelogram", "Easy", "Single-step computation MCQ",
  r"$P(1, 2)$, $Q(4, 3)$ and $R(6, 6)$ are three consecutive vertices of a parallelogram $PQRS$. The vertex $S$ is",
  r"$(3, 5)$",
  [(r"$(9, 7)$", r"Uses $S = Q + R - P$, pairing $P$ with $S$ as opposite vertices, so that $QR$ becomes a diagonal instead of a side."),
   (r"$(-1, -1)$", r"Uses $S = P + Q - R$, matching the wrong pair of opposite vertices."),
   (r"$\left(\frac{7}{2}, 4\right)$", r"Stops at the midpoint of the diagonal $PR$.")],
  r"In a parallelogram the diagonals $PR$ and $QS$ bisect each other, so $P + R = Q + S$. Hence $S = (1 + 6 - 4, 2 + 6 - 3) = (3, 5)$.",
  r"Pairing the wrong vertices as ends of a diagonal.",
  "U10-A-parallelogram-fourth-vertex", "One midpoint condition.",
  check=_c9, values=[(3, 5), (9, 7), (-1, -1), (Rational(7, 2), 4)], cognitive="Application")

q("U10-A-010", "Locus", "Locus of a point equidistant from two points", "Easy", "Single-step computation MCQ",
  r"The locus of a point which is equidistant from $(1, 2)$ and $(3, -4)$ is",
  r"$x - 3y - 5 = 0$",
  [(r"$3x + y - 5 = 0$", r"Draws the line through the midpoint $(2, -1)$ with the slope $-3$ of the segment itself, not the perpendicular slope."),
   (r"$x + 3y + 1 = 0$", r"Uses slope $-\frac{1}{3}$ through $(2, -1)$, a sign slip in the negative reciprocal."),
   (r"$x - 3y + 5 = 0$", r"Uses the correct slope $\frac{1}{3}$ but through the point $(1, 2)$ in place of the midpoint.")],
  r"$(x-1)^2 + (y-2)^2 = (x-3)^2 + (y+4)^2$ gives $-2x - 4y + 5 = -6x + 8y + 25$, i.e. $4x - 12y - 20 = 0$, or $x - 3y - 5 = 0$. This is the perpendicular bisector of the segment.",
  r"Forgetting that the locus is perpendicular to the segment and passes through its midpoint.",
  "U10-A-locus-equidistant", "One equation from the distance formula, simplified.",
  check=lambda: canon(expand((X-1)**2 + (Y-2)**2 - (X-3)**2 - (Y+4)**2)),
  values=[canon(X - 3*Y - 5), canon(3*X + Y - 5), canon(X + 3*Y + 1), canon(X - 3*Y + 5)], cognitive="Application")

q("U10-A-011", "Circumcentre", "Circumcentre of a right triangle", "Easy", "Direct concept MCQ",
  r"The circumcentre of the triangle with vertices $(1, 1)$, $(7, 1)$ and $(1, 9)$ is",
  r"$(4, 5)$",
  [(r"$\left(3, \frac{11}{3}\right)$", r"Gives the centroid, averaging the three vertices."),
   (r"$(1, 1)$", r"Gives the right-angled vertex, which is the orthocentre."),
   (r"$(4, 1)$", r"Takes the midpoint of the leg joining $(1, 1)$ and $(7, 1)$ in place of the hypotenuse.")],
  r"The sides from $(1, 1)$ are horizontal and vertical, so the right angle is at $(1, 1)$. The circumcentre of a right triangle is the midpoint of the hypotenuse: $\left(\frac{7+1}{2}, \frac{1+9}{2}\right) = (4, 5)$.",
  r"Mixing up the centroid, orthocentre and circumcentre of a right triangle.",
  "U10-A-circumcentre-right", "Recognise the right angle, then one midpoint.",
  check=lambda: circumcentre((1, 1), (7, 1), (1, 9)),
  values=[(4, 5), (Rational(3), Rational(11, 3)), (1, 1), (4, 1)], cognitive="Understanding")

def _c12():
    l1, l2, l3 = X - 2, Y + 3, 3*X + 4*Y - 12
    return orthocentre(meet(l1, l2), meet(l1, l3), meet(l2, l3))
q("U10-A-012", "Orthocentre", "Orthocentre of a triangle formed by lines", "Easy", "Single-step computation MCQ",
  r"The orthocentre of the triangle formed by the lines $x = 2$, $y = -3$ and $3x + 4y = 12$ is",
  r"$(2, -3)$",
  [(r"$\left(5, -\frac{3}{4}\right)$", r"Gives the circumcentre, the midpoint of the hypotenuse joining $\left(2, \frac{3}{2}\right)$ and $(8, -3)$."),
   (r"$\left(4, -\frac{3}{2}\right)$", r"Gives the centroid of the vertices $(2, -3)$, $\left(2, \frac{3}{2}\right)$, $(8, -3)$."),
   (r"$(8, -3)$", r"Takes the vertex opposite the shortest side, not the right-angled vertex.")],
  r"The lines $x = 2$ and $y = -3$ are perpendicular, so the triangle is right-angled at their intersection $(2, -3)$. The altitudes from the other two vertices are the two legs, which meet at $(2, -3)$, so that is the orthocentre.",
  r"Confusing the orthocentre of a right triangle with its circumcentre or centroid.",
  "U10-A-orthocentre-right", "Recognise the right angle; no computation beyond one intersection.",
  check=_c12, values=[(2, -3), (5, Rational(-3, 4)), (4, Rational(-3, 2)), (8, -3)], cognitive="Understanding")

def _c13():
    P, Q, R = (1, 1), (4, 5), (8, 2)
    s = sorted([dist(P, Q)**2, dist(Q, R)**2, dist(P, R)**2])
    iso = s[0] == s[1] or s[1] == s[2]
    right = s[0] + s[1] == s[2]
    equi = s[0] == s[2]
    return (bool(iso), bool(right), bool(equi))
q("U10-A-013", "Distance formula", "Nature of a triangle", "Easy", "Conceptual/application MCQ",
  r"The triangle with vertices $(1, 1)$, $(4, 5)$ and $(8, 2)$ is",
  r"isosceles and right-angled",
  [(r"equilateral", r"Computes the two equal sides $5$ and $5$ and assumes the third is also $5$ without checking."),
   (r"scalene and right-angled", r"Detects the right angle from the slopes $\frac{4}{3}$ and $-\frac{3}{4}$ of the two shorter sides but never compares their lengths."),
   (r"isosceles but not right-angled", r"Finds two equal sides but does not test Pythagoras on the squares $25, 25, 50$.")],
  r"The squared side lengths are $3^2 + 4^2 = 25$, $4^2 + 3^2 = 25$ and $7^2 + 1^2 = 50$. Two sides are equal, and $25 + 25 = 50$, so the triangle is isosceles and right-angled.",
  r"Stopping after finding two equal sides.",
  "U10-A-triangle-nature", "Three distances and one Pythagoras check.",
  check=_c13, values=[(True, True, False), (True, False, True), (False, True, False), (True, False, False)],
  cognitive="Understanding")

def _c14():
    m = (-2*sqrt(3) - (-sqrt(3))) / (3 - 2)
    th = atan(m)
    return th + pi if th < 0 else th
q("U10-A-014", "Slope of a line", "Inclination from two points", "Easy", "Single-step computation MCQ",
  r"The inclination $\theta \in [0, \pi)$ of the line through $(2, -\sqrt{3})$ and $(3, -2\sqrt{3})$ with the positive $x$-axis is",
  r"$\frac{2\pi}{3}$",
  [(r"$\frac{\pi}{3}$", r"Drops the sign of the slope $-\sqrt{3}$ and uses $\tan\theta = \sqrt{3}$."),
   (r"$\frac{5\pi}{6}$", r"Uses $\frac{\Delta x}{\Delta y} = -\frac{1}{\sqrt{3}}$ as the slope."),
   (r"$\frac{\pi}{6}$", r"Uses $\frac{\Delta x}{\Delta y}$ and also drops the sign, taking $\tan\theta = \frac{1}{\sqrt{3}}$.")],
  r"The slope is $\frac{-2\sqrt{3} + \sqrt{3}}{3 - 2} = -\sqrt{3}$. With $\theta \in [0, \pi)$ and $\tan\theta = -\sqrt{3}$, $\theta = \frac{2\pi}{3}$.",
  r"Ignoring the sign of the slope when choosing the inclination.",
  "U10-A-inclination", "One slope and one standard angle.",
  check=_c14, values=[2*pi/3, pi/3, 5*pi/6, pi/6], cognitive="Application")

def _c15():
    lam = Symbol('lam', positive=True)
    l = solve(Eq((lam*(-3) + 5) / (lam + 1), 2), lam)[0]
    return (lam*4 + 12).subs(lam, l) / (l + 1)
q("U10-A-015", "Section formula", "Unknown coordinate of a dividing point", "Easy", "Multi-step computation MCQ",
  r"The point $(h, 2)$ lies on the line segment joining $(12, 5)$ and $(4, -3)$. Then $h$ equals",
  r"$9$",
  [(r"$7$", r"Finds the ratio $3 : 5$ but attaches the weights to the wrong ends: $\frac{3 \cdot 12 + 5 \cdot 4}{8}$."),
   (r"$8$", r"Assumes the point is the midpoint of the segment."),
   (r"$24$", r"Uses the external division formula $\frac{3 \cdot 4 - 5 \cdot 12}{3 - 5}$ with the ratio $3 : 5$.")],
  r"Let the ratio be $\lambda : 1$. Then $\frac{-3\lambda + 5}{\lambda + 1} = 2$ gives $\lambda = \frac{3}{5}$, so the ratio is $3 : 5$. Hence $h = \frac{3 \cdot 4 + 5 \cdot 12}{8} = \frac{72}{8} = 9$.",
  r"Pairing the ratio weights with the wrong end points.",
  "U10-A-section-unknown-coordinate", "Find a ratio from one coordinate, then use it for the other.",
  check=_c15, values=[9, 7, 8, 24], cognitive="Application",
  numerical=dict(question=r"The point $(h, 2)$ lies on the line segment joining $(12, 5)$ and $(4, -3)$. The value of $h$ is", answer=9))

# ================================================================ MEDIUM (23)

def _c16():
    s = solve(Eq(area3((K_, 0), (4, 0), (0, 2)), 6), K_)
    return sum(v**2 for v in s)
q("U10-A-016", "Area of a triangle", "Parameter from a given area", "Medium", "Inverse/parameter MCQ",
  r"The area of the triangle with vertices $(k, 0)$, $(4, 0)$ and $(0, 2)$ is $6$ square units. The sum of the squares of all possible values of $k$ is",
  r"$104$",
  [(r"$50$", r"Omits the factor $\frac{1}{2}$, solving $2|4 - k| = 6$ to get $k = 1, 7$."),
   (r"$100$", r"Drops the modulus and solves only $k - 4 = 6$, getting $k = 10$."),
   (r"$4$", r"Drops the modulus and solves only $4 - k = 6$, getting $k = -2$.")],
  r"The base on the $x$-axis has length $|4 - k|$ and the height is $2$, so the area is $|4 - k| = 6$. Thus $k = -2$ or $k = 10$, and $k^2$ sums to $4 + 100 = 104$.",
  r"Dropping the modulus in the area formula and losing a solution.",
  "U10-A-area-parameter", "Area with modulus gives two cases; combine them.",
  check=_c16, values=[104, 50, 100, 4], cognitive="Application",
  numerical=dict(question=r"The area of the triangle with vertices $(k, 0)$, $(4, 0)$ and $(0, 2)$ is $6$ square units. The sum of the squares of all possible values of $k$ is", answer=104))

def _c17():
    H, O = Matrix([1, 4]), Matrix([4, 1])
    G = (H + 2*O) / 3
    return (G[0], G[1])
q("U10-A-017", "Centroid", "Centroid from orthocentre and circumcentre", "Medium", "Single-step computation MCQ",
  r"The orthocentre and the circumcentre of a triangle are $(1, 4)$ and $(4, 1)$ respectively. The centroid of the triangle is",
  r"$(3, 2)$",
  [(r"$(2, 3)$", r"Divides the segment from the orthocentre to the circumcentre in the ratio $1 : 2$ in place of $2 : 1$."),
   (r"$\left(\frac{5}{2}, \frac{5}{2}\right)$", r"Takes the midpoint of the orthocentre and circumcentre."),
   (r"$\left(\frac{11}{2}, -\frac{1}{2}\right)$", r"Takes the circumcentre as dividing the orthocentre-centroid segment in $2 : 1$, i.e. $G = \frac{3O - H}{2}$.")],
  r"On the Euler line the centroid $G$ divides $HO$ internally in the ratio $2 : 1$, so $G = \frac{H + 2O}{3} = \left(\frac{1 + 8}{3}, \frac{4 + 2}{3}\right) = (3, 2)$.",
  r"Using the Euler line ratio from the wrong end.",
  "U10-A-euler-line", "Recall the Euler line ratio and apply the section formula.",
  check=_c17, values=[(3, 2), (2, 3), (Rational(5, 2), Rational(5, 2)), (Rational(11, 2), Rational(-1, 2))],
  cognitive="Application")

q("U10-A-018", "Orthocentre", "Orthocentre from vertices", "Medium", "Multi-step computation MCQ",
  r"The orthocentre of the triangle with vertices $(0, 0)$, $(4, 0)$ and $(1, 3)$ is",
  r"$(1, 1)$",
  [(r"$(2, 1)$", r"Finds the circumcentre, intersecting perpendicular bisectors in place of altitudes."),
   (r"$\left(\frac{5}{3}, 1\right)$", r"Finds the centroid."),
   (r"$(1, -1)$", r"Takes the line from $(0, 0)$ parallel to the side joining $(4, 0)$ and $(1, 3)$, slope $-1$, in place of the altitude.")],
  r"The altitude from $(1, 3)$ to the side on the $x$-axis is $x = 1$. The side through $(4, 0)$ and $(1, 3)$ has slope $-1$, so the altitude from $(0, 0)$ is $y = x$. These meet at $(1, 1)$.",
  r"Using the side's slope rather than its negative reciprocal for an altitude.",
  "U10-A-orthocentre-vertices", "Two altitudes, then their intersection.",
  check=lambda: orthocentre((0, 0), (4, 0), (1, 3)),
  values=[(1, 1), (2, 1), (Rational(5, 3), 1), (1, -1)], cognitive="Application")

def _c19():
    P, Q, R = (0, 0), (6, 0), (2, 4)
    return dist(circumcentre(P, Q, R), P)
q("U10-A-019", "Circumcentre", "Circumradius from vertices", "Medium", "Multi-step computation MCQ",
  r"The radius of the circle passing through the vertices of the triangle $(0, 0)$, $(6, 0)$ and $(2, 4)$ is",
  r"$\sqrt{10}$",
  [(r"$2\sqrt{10}$", r"Uses $R = \frac{abc}{2\Delta}$ in place of $\frac{abc}{4\Delta}$: $\frac{6 \cdot 2\sqrt{5} \cdot 4\sqrt{2}}{24}$."),
   (r"$4\sqrt{10}$", r"Uses $R = \frac{abc}{\Delta}$, dropping the factor $4$."),
   (r"$\frac{4\sqrt{5}}{3}$", r"Measures the distance from the centroid $\left(\frac{8}{3}, \frac{4}{3}\right)$ to the origin.")],
  r"The perpendicular bisector of the side on the $x$-axis is $x = 3$. The perpendicular bisector of the join of $(0, 0)$ and $(2, 4)$ is $y - 2 = -\frac{1}{2}(x - 1)$, which meets $x = 3$ at $y = 1$. The circumcentre is $(3, 1)$ and the radius is $\sqrt{9 + 1} = \sqrt{10}$.",
  r"Using the centroid as the centre of the circumcircle, or misremembering $R = \frac{abc}{4\Delta}$.",
  "U10-A-circumradius", "Two perpendicular bisectors and a distance.",
  check=_c19, values=[sqrt(10), 2*sqrt(10), 4*sqrt(10), 4*sqrt(5)/3], cognitive="Application")

q("U10-A-020", "Incentre", "Incentre of a scalene triangle", "Medium", "Multi-step computation MCQ",
  r"The incentre of the triangle with vertices $P(0, 0)$, $Q(14, 0)$ and $R(5, 12)$ is",
  r"$(6, 4)$",
  [(r"$\left(\frac{19}{3}, 4\right)$", r"Gives the centroid, using equal weights for the vertices."),
   (r"$\left(7, \frac{33}{8}\right)$", r"Gives the circumcentre, intersecting perpendicular bisectors."),
   (r"$\left(5, \frac{15}{4}\right)$", r"Gives the orthocentre, intersecting altitudes.")],
  r"The opposite side lengths are $QR = 15$, $PR = 13$, $PQ = 14$. The incentre is $\frac{15P + 13Q + 14R}{42} = \left(\frac{0 + 182 + 70}{42}, \frac{0 + 0 + 168}{42}\right) = (6, 4)$. As a check, $r = \frac{\Delta}{s} = \frac{84}{21} = 4$ matches the ordinate.",
  r"Weighting vertices equally, or confusing the incentre with another centre.",
  "U10-A-incentre-weights", "Three distances, then weighted average.",
  check=lambda: incentre((0, 0), (14, 0), (5, 12)),
  values=[(6, 4), (Rational(19, 3), 4), (7, Rational(33, 8)), (5, Rational(15, 4))], cognitive="Application")

def _c21():
    G = ((2 - 4 + T_) / 3, (3 + 1 + 3*T_ - 2) / 3)
    t_of_x = solve(Eq(X, G[0]), T_)[0]
    return canon(Y - G[1].subs(T_, t_of_x))
q("U10-A-021", "Locus", "Locus of a centroid", "Medium", "Multi-step computation MCQ",
  r"Two vertices of a triangle are $(2, 3)$ and $(-4, 1)$, and the third vertex moves on the line $3x - y = 2$. The locus of the centroid of the triangle is",
  r"$9x - 3y + 8 = 0$",
  [(r"$3x - y + 8 = 0$", r"Omits the division by $3$, taking the centroid as the sum of the vertices."),
   (r"$9x - 3y - 16 = 0$", r"Slips the sign of $-4$, using $x = \frac{2 + 4 + t}{3}$."),
   (r"$3x - y - 2 = 0$", r"Assumes the centroid moves on the same line as the third vertex.")],
  r"Let the third vertex be $(t, 3t - 2)$. The centroid is $\left(\frac{t - 2}{3}, \frac{3t + 2}{3}\right)$. From $x = \frac{t-2}{3}$, $t = 3x + 2$, so $3y = 3(3x + 2) + 2 = 9x + 8$, giving $9x - 3y + 8 = 0$.",
  r"Assuming the centroid locus coincides with the vertex's path.",
  "U10-A-locus-centroid-line", "Parametrise, apply centroid formula, eliminate.",
  check=_c21, values=[canon(9*X - 3*Y + 8), canon(3*X - Y + 8), canon(9*X - 3*Y - 16), canon(3*X - Y - 2)],
  cognitive="Application")

def _c22():
    a, b, h, k = symbols('a b h k', nonzero=True)
    # P(a,0), Q(0,b) with 2/a + 3/b = 1; midpoint (h, k) = (a/2, b/2)
    expr = (2/a + 3/b - 1).subs({a: 2*h, b: 2*k})
    num = numer(together(expr))
    return canon(num.subs({h: X, k: Y}))
q("U10-A-022", "Locus", "Locus of the midpoint of an intercepted segment", "Medium", "Multi-step computation MCQ",
  r"A variable line through the fixed point $(2, 3)$ meets the $x$-axis at $P$ and the $y$-axis at $Q$. The locus of the midpoint of $PQ$ is",
  r"$3x + 2y = 2xy$",
  [(r"$2x + 3y = 2xy$", r"Swaps the roles of the coordinates $2$ and $3$ when substituting into the intercept condition."),
   (r"$3x + 2y = xy$", r"Treats the midpoint coordinates as the intercepts themselves, using $\frac{2}{h} + \frac{3}{k} = 1$."),
   (r"$6x + 4y = xy$", r"Inverts the midpoint relation, using $a = \frac{h}{2}$, $b = \frac{k}{2}$.")],
  r"Let $P = (a, 0)$, $Q = (0, b)$; the line passes through $(2, 3)$, so $\frac{2}{a} + \frac{3}{b} = 1$. The midpoint is $(h, k) = \left(\frac{a}{2}, \frac{b}{2}\right)$, so $\frac{2}{2h} + \frac{3}{2k} = 1$, i.e. $2k + 3h = 2hk$. The locus is $3x + 2y = 2xy$.",
  r"Substituting the midpoint coordinates for the intercepts without the factor $2$.",
  "U10-A-locus-midpoint-intercepts", "Intercept condition plus midpoint substitution and elimination.",
  check=_c22, values=[canon(3*X + 2*Y - 2*X*Y), canon(2*X + 3*Y - 2*X*Y), canon(3*X + 2*Y - X*Y), canon(6*X + 4*Y - X*Y)],
  cognitive="Application")

def _c23():
    L = lambda p: 2*p[0] + p[1] - 4
    lam = Symbol('lam')
    P1, P2 = (2, -2), (3, 7)
    s = solve(L(((lam*P2[0] + P1[0]) / (lam + 1), (lam*P2[1] + P1[1]) / (lam + 1))), lam)
    return s[0]
q("U10-A-023", "Section formula", "Ratio in which a line divides a segment", "Medium", "Single-step computation MCQ",
  r"The line $2x + y - 4 = 0$ divides the line segment joining $(2, -2)$ and $(3, 7)$ in the ratio",
  r"$2 : 9$ internally",
  [(r"$9 : 2$ internally", r"Inverts the ratio, using $-\frac{L_2}{L_1}$ with $L_1 = -2$, $L_2 = 9$."),
   (r"$2 : 9$ externally", r"Drops the minus sign in $-\frac{L_1}{L_2}$, reading $\frac{-2}{9}$ as external."),
   (r"$2 : 13$ externally", r"Evaluates $2x + y$ without the constant $-4$ at both points, getting $-\frac{2}{13}$.")],
  r"If the ratio is $\lambda : 1$, the point $\left(\frac{3\lambda + 2}{\lambda + 1}, \frac{7\lambda - 2}{\lambda + 1}\right)$ lies on the line: $2(3\lambda + 2) + (7\lambda - 2) - 4(\lambda + 1) = 0$, i.e. $9\lambda - 2 = 0$. So $\lambda = \frac{2}{9} > 0$, an internal division in the ratio $2 : 9$.",
  r"Mishandling the sign in $\lambda = -\frac{L_1}{L_2}$.",
  "U10-A-line-divides-segment", "Section point substituted into a line; sign interpretation.",
  check=_c23, values=[Rational(2, 9), Rational(9, 2), Rational(-2, 9), Rational(-2, 13)], cognitive="Application")

def _c24():
    P, Q, R, S = [Matrix(v) for v in ([-2, -1], [1, 0], [4, 3], [1, 2])]
    para = (P + R) == (Q + S)
    rhombus = para and (Q - P).norm() == (R - Q).norm()
    return (bool(para), bool(rhombus))
q("U10-A-024", "Distance formula", "Classifying a quadrilateral", "Medium", "Statement-based MCQ",
  r"Consider the points $P(-2, -1)$, $Q(1, 0)$, $R(4, 3)$ and $S(1, 2)$, taken in this order. Statement I: $PQRS$ is a parallelogram. Statement II: $PQRS$ is a rhombus." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Sees that opposite sides are equal and assumes all four sides are equal, without comparing $PQ = \sqrt{10}$ with $QR = \sqrt{18}$."),
   (ST_FF, r"Checks whether the diagonals $PR$ and $QS$ are equal in length, finds they are not, and concludes it is not a parallelogram."),
   (ST_FT, r"Rejects the parallelogram because the diagonals are unequal, then takes the equal opposite sides $PQ = RS$ as enough for a rhombus.")],
  r"The midpoint of $PR$ is $(1, 1)$ and the midpoint of $QS$ is $(1, 1)$, so the diagonals bisect each other and $PQRS$ is a parallelogram. But $PQ = \sqrt{9 + 1} = \sqrt{10}$ while $QR = \sqrt{9 + 9} = \sqrt{18}$, so adjacent sides are unequal and it is not a rhombus. Statement I is true and Statement II is false.",
  r"Mixing up the diagonal and side tests for parallelogram, rectangle and rhombus.",
  "U10-A-quadrilateral-type", "Two separate coordinate tests, one per statement.",
  check=_c24, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis")

def _c25():
    s = solve(Eq((2 - 0)*(-3 - 0) + (3 - Y)*(-2 - Y), 0), Y)
    return FiniteSet(*s)
q("U10-A-025", "Parallel and perpendicular lines", "Right angle at a point on an axis", "Medium", "Multi-step computation MCQ",
  r"$P(2, 3)$ and $Q(-3, -2)$ are given points. $R$ is a point on the $y$-axis such that $\angle PRQ = 90^\circ$. The possible ordinates of $R$ are",
  r"$4$ and $-3$",
  [(r"$-4$ and $3$", r"Expands $(y - 3)(y + 2)$ as $y^2 + y - 6$, getting $y^2 + y - 12 = 0$."),
   (r"$0$ and $1$", r"Sets the product of the slopes of $RP$ and $RQ$ equal to $1$ in place of $-1$."),
   (r"$5$ and $-5$", r"Places the right angle at $P$ (giving $y = 5$) or at $Q$ (giving $y = -5$) in place of at $R$.")],
  r"Let $R = (0, y)$. Perpendicularity of $RP$ and $RQ$ gives $\frac{y - 3}{0 - 2} \cdot \frac{y + 2}{0 + 3} = -1$, i.e. $(y - 3)(y + 2) = 6$, so $y^2 - y - 12 = 0$ and $y = 4$ or $y = -3$.",
  r"Using the product of slopes $+1$, or putting the right angle at the wrong vertex.",
  "U10-A-right-angle-on-axis", "Perpendicular slopes giving a quadratic.",
  check=_c25, values=[FiniteSet(4, -3), FiniteSet(-4, 3), FiniteSet(0, 1), FiniteSet(5, -5)], cognitive="Application")

def _c26():
    a, b, c = symbols('a b c', real=True)
    d1 = Matrix([[a, b + c, 1], [b, c + a, 1], [c, a + b, 1]]).det()
    s1 = simplify(d1) == 0
    P, Q, R = (1, 1), (-1, -1), (-sqrt(3), sqrt(3))
    s2 = simplify(dist(P, Q) - dist(Q, R)) == 0 and simplify(dist(Q, R) - dist(P, R)) == 0
    return (bool(s1), bool(s2))
q("U10-A-026", "Area of a triangle", "Collinearity and equilateral test", "Medium", "Statement-based MCQ",
  r"Statement I: For all real $a$, $b$, $c$, the points $(a, b + c)$, $(b, c + a)$ and $(c, a + b)$ are collinear. Statement II: The points $(1, 1)$, $(-1, -1)$ and $(-\sqrt{3}, \sqrt{3})$ are the vertices of an equilateral triangle." + STEM_TAIL,
  ST_TT,
  [(ST_FF, r"Expands the determinant with a sign slip so it does not vanish, and also miscomputes $(1 - \sqrt{3})^2$ as $4 + 2\sqrt{3}$."),
   (ST_TF, r"Miscomputes $(1 - \sqrt{3})^2$ as $4 + 2\sqrt{3}$, so the side from $(1, 1)$ to $(-\sqrt{3}, \sqrt{3})$ looks longer than $2\sqrt{2}$."),
   (ST_FT, r"Expands the determinant with a sign slip so it does not vanish, missing that every point lies on $x + y = a + b + c$.")],
  r"Each point satisfies $x + y = a + b + c$, so all three lie on one line and Statement I is true. For Statement II, the squared distances are $2^2 + 2^2 = 8$, $(1 + \sqrt{3})^2 + (1 - \sqrt{3})^2 = 8$ and $(-1 + \sqrt{3})^2 + (-1 - \sqrt{3})^2 = 8$, so the triangle is equilateral. Both statements are true.",
  r"Not seeing the common line $x + y = a + b + c$, or mis-expanding surd squares.",
  "U10-A-collinear-equilateral", "Two independent checks, one symbolic.",
  check=_c26, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis")

V12 = [(1, 1), (7, -3), (12, 2), (7, 21)]
q("U10-A-027", "Area of a triangle", "Area of a quadrilateral", "Medium", "Multi-step computation MCQ",
  r"The area of the quadrilateral with vertices $P(1, 1)$, $Q(7, -3)$, $R(12, 2)$ and $S(7, 21)$, taken in this order, is",
  r"$132$",
  [(r"$264$", r"Omits the factor $\frac{1}{2}$ in the shoelace formula."),
   (r"$35$", r"Takes the vertices in the order $P, Q, S, R$, which traces a self-crossing figure."),
   (r"$107$", r"Splits along the diagonal $PR$ but adds only the triangle $PRS$, leaving out $PQR$.")],
  r"Splitting along the diagonal $PR$: area of $PQR = \frac{1}{2}|1(-3-2) + 7(2-1) + 12(1+3)| = \frac{1}{2}(50) = 25$, and area of $PRS = \frac{1}{2}|1(2-21) + 12(21-1) + 7(1-2)| = \frac{1}{2}(214) = 107$. The total is $25 + 107 = 132$.",
  r"Taking vertices out of cyclic order, or omitting one of the two triangles.",
  "U10-A-area-quadrilateral", "Two triangle areas or one shoelace sum.",
  check=lambda: shoelace(V12), values=[132, 264, 35, 107], cognitive="Application",
  numerical=dict(question=r"The area of the quadrilateral with vertices $P(1, 1)$, $Q(7, -3)$, $R(12, 2)$ and $S(7, 21)$, taken in this order, is", answer=132))

def _c28():
    D, E, F = Matrix([2, 1]), Matrix([5, 3]), Matrix([3, 6])
    V = [E + F - D, D + F - E, D + E - F]
    return area3(*[(v[0], v[1]) for v in V])
q("U10-A-028", "Area of a triangle", "Triangle from midpoints of its sides", "Medium", "Multi-step computation MCQ",
  r"The midpoints of the sides of a triangle are $(2, 1)$, $(5, 3)$ and $(3, 6)$. The area of the triangle is",
  r"$26$",
  [(r"$\frac{13}{2}$", r"Gives the area of the triangle formed by the midpoints themselves."),
   (r"$13$", r"Takes the original triangle to be twice the area of the midpoint triangle, using the side ratio $2$ in place of its square."),
   (r"$52$", r"Omits the factor $\frac{1}{2}$ in the area of the midpoint triangle and then multiplies by $4$.")],
  r"The triangle formed by the midpoints has area $\frac{1}{2}|2(3 - 6) + 5(6 - 1) + 3(1 - 3)| = \frac{1}{2}|{-6} + 25 - 6| = \frac{13}{2}$. Its sides are half the original sides, so the original area is $4 \cdot \frac{13}{2} = 26$.",
  r"Scaling area by the side ratio rather than its square.",
  "U10-A-medial-triangle-area", "Area plus a similarity factor.",
  check=_c28, values=[26, Rational(13, 2), 13, 52], cognitive="Application",
  numerical=dict(question=r"The midpoints of the sides of a triangle are $(2, 1)$, $(5, 3)$ and $(3, 6)$. The area of the triangle is", answer=26))

def _c29():
    a, b = symbols('a b')
    R = section((a, 0), (0, b), 1, 2)
    s = solve([R[0] - 3, R[1] + 4], [a, b], dict=True)[0]
    return (s[a], s[b])
q("U10-A-029", "Intercepts of a line", "Intercepts from a dividing point", "Medium", "Inverse/parameter MCQ",
  r"A line meets the $x$-axis at $P$ and the $y$-axis at $Q$. The point $(3, -4)$ divides $PQ$ internally in the ratio $1 : 2$, that is, its distance from $P$ is half its distance from $Q$. The $x$-intercept and $y$-intercept of the line are respectively",
  r"$\frac{9}{2}$ and $-12$",
  [(r"$9$ and $-6$", r"Attaches the weights to the wrong ends, writing the point as $\left(\frac{a}{3}, \frac{2b}{3}\right)$."),
   (r"$6$ and $-8$", r"Treats $(3, -4)$ as the midpoint of $PQ$."),
   (r"$\frac{9}{2}$ and $12$", r"Slips the sign of the ordinate, solving $\frac{b}{3} = 4$.")],
  r"Let $P = (a, 0)$ and $Q = (0, b)$. The point dividing $PQ$ in $1 : 2$ is $\left(\frac{1 \cdot 0 + 2a}{3}, \frac{1 \cdot b + 2 \cdot 0}{3}\right) = \left(\frac{2a}{3}, \frac{b}{3}\right) = (3, -4)$. So $a = \frac{9}{2}$ and $b = -12$.",
  r"Placing the ratio weights on the wrong end points.",
  "U10-A-intercepts-from-section", "Section formula with unknown end points, solved twice.",
  check=_c29, values=[(Rational(9, 2), -12), (9, -6), (6, -8), (Rational(9, 2), 12)], cognitive="Application")

def _c30():
    P, Q, R = (2, 1), (5, 2), (3, 4)
    return 2*area3(P, Q, R) / dist(P, Q)
q("U10-A-030", "Area of a triangle", "Altitude from area", "Medium", "Multi-step computation MCQ",
  r"In the triangle with vertices $P(2, 1)$, $Q(5, 2)$ and $R(3, 4)$, the length of the altitude from $R$ to the side $PQ$ is",
  r"$\frac{4\sqrt{10}}{5}$",
  [(r"$\frac{2\sqrt{10}}{5}$", r"Uses $h = \frac{\Delta}{PQ}$, forgetting the factor $2$ in $\Delta = \frac{1}{2} \cdot PQ \cdot h$."),
   (r"$\frac{\sqrt{26}}{2}$", r"Finds the length of the median from $R$ to the midpoint $\left(\frac{7}{2}, \frac{3}{2}\right)$ of $PQ$."),
   (r"$\frac{8\sqrt{10}}{5}$", r"Omits the $\frac{1}{2}$ in the area (taking $8$) and then still uses $h = \frac{2\Delta}{PQ}$.")],
  r"Area $= \frac{1}{2}|2(2 - 4) + 5(4 - 1) + 3(1 - 2)| = \frac{1}{2}|{-4} + 15 - 3| = 4$ and $PQ = \sqrt{9 + 1} = \sqrt{10}$. Hence $h = \frac{2 \cdot 4}{\sqrt{10}} = \frac{8}{\sqrt{10}} = \frac{4\sqrt{10}}{5}$.",
  r"Mixing up the altitude with the median, or misusing $\Delta = \frac{1}{2}bh$.",
  "U10-A-area-altitude", "Area, a distance, then a ratio.",
  check=_c30, values=[4*sqrt(10)/5, 2*sqrt(10)/5, sqrt(26)/2, 8*sqrt(10)/5], cognitive="Application")

q("U10-A-031", "Locus", "Locus from difference of squared distances", "Medium", "Multi-step computation MCQ",
  r"A point $P$ moves so that $PS^2 - PT^2 = 6$, where $S = (1, 2)$ and $T = (3, -2)$. The locus of $P$ is",
  r"$2x - 4y - 7 = 0$",
  [(r"$2x - 4y - 1 = 0$", r"Computes $PT^2 - PS^2 = 6$, reversing the difference."),
   (r"$2x - 4y - 3 = 0$", r"Drops the constant terms $1 + 4 - 9 - 4 = -8$ when expanding."),
   (r"$x - 2y - 2 = 0$", r"Sets $PS^2 = PT^2$, ignoring the $6$, which gives the perpendicular bisector.")],
  r"$(x-1)^2 + (y-2)^2 - (x-3)^2 - (y+2)^2 = (-2x - 4y + 5) - (-6x + 4y + 13) = 4x - 8y - 8$. Setting this equal to $6$ gives $4x - 8y - 14 = 0$, i.e. $2x - 4y - 7 = 0$.",
  r"Reversing the order of the difference or losing the constant terms.",
  "U10-A-locus-difference-squares", "Expand two squared distances, cancel, simplify.",
  check=lambda: canon(expand((X-1)**2 + (Y-2)**2 - (X-3)**2 - (Y+2)**2 - 6)),
  values=[canon(2*X - 4*Y - 7), canon(2*X - 4*Y - 1), canon(2*X - 4*Y - 3), canon(X - 2*Y - 2)], cognitive="Application")

def _c32():
    expr = numer(together(Y/(X + 2) * Y/(X - 2) + 4))
    return canon(expr)
q("U10-A-032", "Locus", "Locus from a product of slopes", "Medium", "Multi-step computation MCQ",
  r"$S(-2, 0)$ and $T(2, 0)$ are fixed points, and $P$ is a point not on the $x$-axis such that the product of the slopes of $PS$ and $PT$ is $-4$. Then $P$ lies on the curve",
  r"$4x^2 + y^2 = 16$",
  [(r"$x^2 + 4y^2 = 4$", r"Writes the slopes as $\frac{x+2}{y}$ and $\frac{x-2}{y}$ (reciprocals), giving $x^2 - 4 = -4y^2$."),
   (r"$4x^2 - y^2 = 16$", r"Drops the minus sign, solving $\frac{y^2}{x^2 - 4} = 4$."),
   (r"$4x^2 + y^2 = 4$", r"Distributes $-4$ over $x^2$ only, writing $y^2 = -4x^2 + 4$.")],
  r"With $P = (x, y)$, $\frac{y}{x + 2} \cdot \frac{y}{x - 2} = -4$ gives $y^2 = -4(x^2 - 4) = -4x^2 + 16$, i.e. $4x^2 + y^2 = 16$.",
  r"Inverting the slope or mishandling the sign of the product.",
  "U10-A-locus-slope-product", "Two slopes, a product condition, and simplification.",
  check=_c32, values=[canon(4*X**2 + Y**2 - 16), canon(X**2 + 4*Y**2 - 4), canon(4*X**2 - Y**2 - 16), canon(4*X**2 + Y**2 - 4)],
  cognitive="Application")

def _c33():
    P, Q, R = (0, 0), (8, 0), (0, 6)
    return dist(incentre(P, Q, R), circumcentre(P, Q, R))
q("U10-A-033", "Incentre", "Distance between incentre and circumcentre", "Medium", "Multi-step computation MCQ",
  r"The line $3x + 4y = 24$ forms a triangle with the coordinate axes. The distance between the incentre and the circumcentre of this triangle is",
  r"$\sqrt{5}$",
  [(r"$\frac{5}{3}$", r"Uses the centroid $\left(\frac{8}{3}, 2\right)$ in place of the incentre."),
   (r"$2\sqrt{2}$", r"Measures the distance from the incentre $(2, 2)$ to the origin in place of the circumcentre."),
   (r"$3\sqrt{5}$", r"Uses $\sqrt{R^2 + 2Rr} = \sqrt{25 + 20}$, slipping the sign in Euler's relation.")],
  r"The vertices are $(0, 0)$, $(8, 0)$, $(0, 6)$ with hypotenuse $10$. The inradius is $r = \frac{8 + 6 - 10}{2} = 2$, so the incentre is $(2, 2)$. The circumcentre is the midpoint of the hypotenuse, $(4, 3)$. The distance is $\sqrt{4 + 1} = \sqrt{5}$.",
  r"Confusing the incentre with the centroid.",
  "U10-A-incentre-circumcentre", "Two centres of a right triangle, then a distance.",
  check=_c33, values=[sqrt(5), Rational(5, 3), 2*sqrt(2), 3*sqrt(5)], cognitive="Application")

def _c34():
    V = (meet(X - Y + 1, 2*X + Y - 10), meet(X - Y + 1, X + 2*Y - 2), meet(2*X + Y - 10, X + 2*Y - 2))
    return orthocentre(*V)
q("U10-A-034", "Orthocentre", "Orthocentre of a triangle formed by three lines", "Medium", "Multi-step computation MCQ",
  r"The orthocentre of the triangle formed by the lines $x - y + 1 = 0$, $2x + y - 10 = 0$ and $x + 2y - 2 = 0$ is",
  r"$(2, 2)$",
  [(r"$(3, 1)$", r"Gives the centroid of the vertices $(3, 4)$, $(0, 1)$, $(6, -2)$."),
   (r"$\left(\frac{7}{2}, \frac{1}{2}\right)$", r"Gives the circumcentre, intersecting perpendicular bisectors in place of altitudes."),
   (r"$(3, -5)$", r"Draws each altitude with the slope of the opposite side itself: $y + 2 = 1(x - 6)$ from $(6, -2)$ and $y - 1 = -2x$ from $(0, 1)$, which meet at $(3, -5)$.")],
  r"Solving in pairs, the vertices are $(3, 4)$ (first and second lines), $(0, 1)$ (first and third) and $(6, -2)$ (second and third). The altitude from $(6, -2)$ is perpendicular to $x - y + 1 = 0$ (slope $1$), so it is $x + y = 4$. The altitude from $(0, 1)$ is perpendicular to $2x + y - 10 = 0$ (slope $-2$), so it is $x - 2y + 2 = 0$. These meet at $(2, 2)$, and the third altitude $y = 2x - 2$ from $(3, 4)$ also passes through it.",
  r"Using the side's own slope for the altitude, or confusing the orthocentre with the centroid or circumcentre.",
  "U10-A-orthocentre-lines", "Three line intersections for the vertices, two altitudes with non-axis sides, then their intersection.",
  check=_c34, values=[(2, 2), (3, 1), (Rational(7, 2), Rational(1, 2)), (3, -5)], cognitive="Application")

def _c35():
    # Statement I: centroid of a lattice triangle is always a lattice point -> search a counterexample
    s1 = True
    pts = list(itertools.product(range(3), repeat=2))
    for P, Q, R in itertools.combinations(pts, 3):
        if area3(P, Q, R) != 0:
            G = centroid(P, Q, R)
            if not (G[0].is_integer and G[1].is_integer):
                s1 = False
                break
    # Statement II: no equilateral lattice triangle (exhaustive in a 7 x 7 grid)
    s2 = True
    pts = list(itertools.product(range(7), repeat=2))
    for P, Q, R in itertools.combinations(pts, 3):
        d = sorted([(P[0]-Q[0])**2 + (P[1]-Q[1])**2, (Q[0]-R[0])**2 + (Q[1]-R[1])**2, (P[0]-R[0])**2 + (P[1]-R[1])**2])
        if d[0] > 0 and d[0] == d[2]:
            s2 = False
            break
    return (s1, s2)
q("U10-A-035", "Area of a triangle", "Lattice-point triangles", "Medium", "Statement-based MCQ",
  r"Call a point a lattice point if both its coordinates are integers. Statement I: The centroid of every triangle whose vertices are lattice points is a lattice point. Statement II: There is no equilateral triangle whose three vertices are all lattice points." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Assumes integer sums divided by $3$ stay integers; the triangle $(0, 0)$, $(1, 0)$, $(0, 1)$ has centroid $\left(\frac{1}{3}, \frac{1}{3}\right)$."),
   (ST_FF, r"Rejects Statement II by guessing that a large enough grid contains an equilateral triangle, without the area argument."),
   (ST_TF, r"Gets both statements reversed: trusts the centroid claim and doubts the equilateral claim.")],
  r"Statement I is false: the vertices $(0, 0)$, $(1, 0)$, $(0, 1)$ give centroid $\left(\frac{1}{3}, \frac{1}{3}\right)$. For Statement II, a lattice triangle has area $\frac{1}{2}|\text{integer}|$, which is rational, while an equilateral triangle of side $a$ has area $\frac{\sqrt{3}}{4}a^2$ with $a^2$ a positive integer (a sum of two integer squares), which is irrational. So Statement II is true.",
  r"Not using the rational-area argument for lattice triangles.",
  "U10-A-lattice-triangle-facts", "Counterexample for one statement and an area-rationality argument for the other.",
  check=_c35, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis")

def _c36():
    P, Q, R = (Integer(-3), Integer(0)), (Integer(3), Integer(0)), (Integer(0), Integer(4))
    G, I, O = centroid(P, Q, R), incentre(P, Q, R), circumcentre(P, Q, R)
    assert G[0] == 0 and I[0] == 0 and O[0] == 0
    lo, hi = sorted([G[1], O[1]])
    s1 = bool(lo < I[1] < hi)
    s2 = bool(simplify(dist(O, P) - Rational(25, 4)) == 0)
    return (s1, s2)
q("U10-A-036", "Centres of a triangle", "Relative position of centres in an isosceles triangle", "Medium", "Statement-based MCQ",
  r"For the triangle with vertices $(-3, 0)$, $(3, 0)$ and $(0, 4)$: Statement I: On the axis of symmetry $x = 0$, the incentre lies between the centroid and the circumcentre. Statement II: The circumradius of the triangle is $\frac{25}{4}$." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Assumes the incentre is always the middle one of the centres on the axis, and uses $R = \frac{abc}{2\Delta} = \frac{5 \cdot 5 \cdot 6}{24} = \frac{25}{4}$ in place of $\frac{abc}{4\Delta}$."),
   (ST_TF, r"Assumes the incentre is always the middle one of the centres on the axis, but computes $R = \frac{abc}{4\Delta} = \frac{25}{8}$ correctly."),
   (ST_FT, r"Places the three centres correctly, but uses $R = \frac{abc}{2\Delta} = \frac{25}{4}$, dropping a factor $2$ from the formula $R = \frac{abc}{4\Delta}$.")],
  r"The sides are $5$, $5$, $6$ and the area is $\Delta = \frac{1}{2} \cdot 6 \cdot 4 = 12$, so $s = 8$ and $r = \frac{\Delta}{s} = \frac{3}{2}$; the incentre is $\left(0, \frac{3}{2}\right)$. The centroid is $\left(0, \frac{4}{3}\right)$. The circumcentre $(0, k)$ satisfies $9 + k^2 = (4 - k)^2$, so $k = \frac{7}{8}$. Since $\frac{7}{8} < \frac{4}{3} < \frac{3}{2}$, the incentre lies above both and not between them, so Statement I is false. The circumradius is $4 - \frac{7}{8} = \frac{25}{8}$ (also $\frac{abc}{4\Delta} = \frac{150}{48}$), not $\frac{25}{4}$, so Statement II is false.",
  r"Assuming a fixed order of the centres on the axis of an isosceles triangle, or using $R = \frac{abc}{2\Delta}$.",
  "U10-A-isosceles-centres-order", "Three centres located on a symmetry axis and compared, plus a circumradius computation.",
  check=_c36, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")

def _c37():
    V = [(3, 0), (0, 3), (-3, 0), (0, -3)]
    for v in V:
        assert Abs(v[0]) + Abs(v[1]) == 3
    return shoelace(V)
q("U10-A-037", "Locus", "Locus from sum of distances to the axes", "Medium", "Multi-step computation MCQ",
  r"A point moves so that the sum of its distances from the two coordinate axes is always $3$. The area of the region enclosed by its locus is",
  r"$18$",
  [(r"$9$", r"Takes the locus as a square of side $3$, reading $3$ as the side length."),
   (r"$36$", r"Takes the locus as a square of side $6$, using the distance between $(3, 0)$ and $(-3, 0)$ as the side."),
   (r"$\frac{9}{2}$", r"Uses only the first-quadrant piece $x + y = 3$, $x, y \ge 0$, forgetting the moduli.")],
  r"The locus is $|x| + |y| = 3$, a square with vertices $(\pm 3, 0)$ and $(0, \pm 3)$. Its diagonals have length $6$, so its area is $\frac{1}{2} \cdot 6 \cdot 6 = 18$.",
  r"Forgetting that the distances to the axes are $|y|$ and $|x|$.",
  "U10-A-locus-modulus-square", "Translate to a modulus equation and find the enclosed area.",
  check=_c37, values=[18, 9, 36, Rational(9, 2)], cognitive="Application",
  numerical=dict(question=r"A point moves so that the sum of its distances from the two coordinate axes is always $3$. The area of the region enclosed by its locus is", answer=18))

def _c38():
    V = (meet(Y - X, Y - 2*X), meet(Y - X, X + Y - 6), meet(Y - 2*X, X + Y - 6))
    return area3(*V)
q("U10-A-038", "Area of a triangle", "Area of a triangle formed by three lines", "Medium", "Multi-step computation MCQ",
  r"The area of the triangle formed by the lines $y = x$, $y = 2x$ and $x + y = 6$ is",
  r"$3$",
  [(r"$6$", r"Omits the factor $\frac{1}{2}$ in the area formula."),
   (r"$18$", r"Uses the triangle formed by $x + y = 6$ with the coordinate axes."),
   (r"$9$", r"Uses the $y$-axis in place of $y = 2x$, taking the vertices $(0, 0)$, $(3, 3)$, $(0, 6)$.")],
  r"The vertices are $(0, 0)$, $(3, 3)$ (from $y = x$ and $x + y = 6$) and $(2, 4)$ (from $y = 2x$ and $x + y = 6$). Area $= \frac{1}{2}|3 \cdot 4 - 3 \cdot 2| = 3$.",
  r"Using the wrong boundary lines or dropping the factor $\frac{1}{2}$.",
  "U10-A-area-from-lines", "Three intersections, then the area formula.",
  check=_c38, values=[3, 6, 18, 9], cognitive="Application")

# ================================================================ DIFFICULT (12)

def _c39():
    return sum(1 for a in range(0, 16) for b in range(0, 16) if a > 0 and b > 0 and a + b < 15)
q("U10-A-039", "Cartesian coordinates", "Lattice points inside a triangle", "Difficult", "Multi-step computation MCQ",
  r"The number of points with both coordinates integers that lie strictly inside the triangle with vertices $(0, 0)$, $(15, 0)$ and $(0, 15)$ is",
  r"$91$",
  [(r"$105$", r"Includes the points on the hypotenuse $x + y = 15$ with $x, y \ge 1$."),
   (r"$78$", r"Uses $x + y \le 13$, excluding the points with $x + y = 14$ as well."),
   (r"$136$", r"Counts every lattice point with $x, y \ge 0$ and $x + y \le 15$, including the boundary.")],
  r"Interior lattice points satisfy $x \ge 1$, $y \ge 1$ and $x + y \le 14$. For $x = 1, 2, \ldots, 13$ there are $14 - x$ values of $y$, so the count is $13 + 12 + \cdots + 1 = 91$.",
  r"Including boundary points when counting points strictly inside.",
  "U10-A-lattice-interior-count", "Careful boundary handling and a summation.",
  check=_c39, values=[91, 105, 78, 136], cognitive="Analysis",
  numerical=dict(question=r"The number of points with both coordinates integers that lie strictly inside the triangle with vertices $(0, 0)$, $(15, 0)$ and $(0, 15)$ is", answer=91))

def _c40():
    a, b = symbols('a b', positive=True)
    t = Symbol('t', real=True)
    gx = (a*cos(t) + b*sin(t) + 1) / 3
    gy = (a*sin(t) - b*cos(t)) / 3
    # eliminate t: (3x-1)^2 + 9y^2 must equal a constant
    const = simplify(expand((3*gx - 1)**2 + 9*gy**2))
    assert const.free_symbols <= {a, b}
    return canon((3*X - 1)**2 + 9*Y**2 - const)
_a, _b = symbols('a b', positive=True)
q("U10-A-040", "Locus", "Locus of a centroid with a parametric vertex pair", "Difficult", "Multi-step computation MCQ",
  r"The vertices of a triangle are $(a\cos t, a\sin t)$, $(b\sin t, -b\cos t)$ and $(1, 0)$, where $a$ and $b$ are positive constants and $t$ is a real parameter. The locus of the centroid of the triangle is",
  r"$(3x - 1)^2 + 9y^2 = a^2 + b^2$",
  [(r"$(3x + 1)^2 + 9y^2 = a^2 + b^2$", r"Moves the fixed vertex to the wrong side, writing $3x + 1 = a\cos t + b\sin t$."),
   (r"$9x^2 + 9y^2 = a^2 + b^2$", r"Ignores the fixed vertex $(1, 0)$ when forming the centroid."),
   (r"$(3x - 1)^2 + 9y^2 = (a + b)^2$", r"Assumes $(a\cos t + b\sin t)^2 + (a\sin t - b\cos t)^2 = (a + b)^2$, adding the amplitudes instead of their squares.")],
  r"The centroid $(x, y)$ satisfies $3x - 1 = a\cos t + b\sin t$ and $3y = a\sin t - b\cos t$. Squaring and adding, the cross terms $2ab\sin t\cos t$ cancel, giving $(3x - 1)^2 + 9y^2 = a^2 + b^2$.",
  r"Not isolating the parametric parts before squaring and adding.",
  "U10-A-locus-centroid-parametric", "Centroid formula, isolation, and elimination of a parameter by squaring.",
  check=_c40, values=[canon((3*X - 1)**2 + 9*Y**2 - _a**2 - _b**2), canon((3*X + 1)**2 + 9*Y**2 - _a**2 - _b**2),
                      canon(9*X**2 + 9*Y**2 - _a**2 - _b**2), canon((3*X - 1)**2 + 9*Y**2 - (_a + _b)**2)],
  cognitive="Analysis")

def _c41():
    P, Q, H = (1, 1), (5, 1), (3, 2)
    # PR perpendicular to QH, QR perpendicular to PH
    s = solve([(X - P[0])*(H[0] - Q[0]) + (Y - P[1])*(H[1] - Q[1]),
               (X - Q[0])*(H[0] - P[0]) + (Y - Q[1])*(H[1] - P[1])], [X, Y], dict=True)[0]
    R = (s[X], s[Y])
    assert orthocentre(P, Q, R) == H
    return R
q("U10-A-041", "Orthocentre", "Third vertex from the orthocentre", "Difficult", "Inverse/parameter MCQ",
  r"Two vertices of a triangle are $P(1, 1)$ and $Q(5, 1)$, and its orthocentre is $(3, 2)$. The third vertex is",
  r"$(3, 5)$",
  [(r"$(3, 4)$", r"Treats $(3, 2)$ as the centroid, taking $R = 3(3, 2) - P - Q$."),
   (r"$(3, 0)$", r"Makes $QR$ parallel to $PH$ and $PR$ parallel to $QH$, in place of perpendicular."),
   (r"$(3, 3)$", r"Assumes the orthocentre is the midpoint of the altitude from the third vertex, whose foot is $(3, 1)$.")],
  r"Let $H = (3, 2)$. Since $PH \perp QR$ and $QH \perp PR$: $PH$ has slope $\frac{1}{2}$, so $QR$ has slope $-2$: $y - 1 = -2(x - 5)$. $QH$ has slope $-\frac{1}{2}$, so $PR$ has slope $2$: $y - 1 = 2(x - 1)$. Solving, $2x - 1 = -2x + 11$, so $x = 3$, $y = 5$. Check: the altitude from $(3, 5)$ is $x = 3$, which passes through $H$.",
  r"Using parallel in place of perpendicular, or mixing up orthocentre and centroid.",
  "U10-A-orthocentre-inverse", "Reverse use of altitudes: two perpendicularity conditions, then a check.",
  check=_c41, values=[(3, 5), (3, 4), (3, 0), (3, 3)], cognitive="Analysis")

def _c42():
    P, Q, R = (K_, 3 - K_), (2 - K_, K_ + 1), (K_ - 5, 2*K_ + 2)
    D = Matrix([[P[0], P[1], 1], [Q[0], Q[1], 1], [R[0], R[1], 1]]).det()
    good = []
    for r in solve(D, K_):
        pts = {tuple(c.subs(K_, r) for c in p) for p in (P, Q, R)}
        if len(pts) == 3:
            good.append(r)
    return FiniteSet(*good)
q("U10-A-042", "Area of a triangle", "Collinearity with a parameter and distinct points", "Difficult", "Inverse/parameter MCQ",
  r"The points $(k, 3 - k)$, $(2 - k, k + 1)$ and $(k - 5, 2k + 2)$ are three distinct collinear points. The value(s) of $k$ are",
  r"$2$ only",
  [(r"$1$ only", r"Solves the determinant equation but keeps only the root $k = 1$, at which the first two points coincide."),
   (r"$1$ and $2$", r"Keeps both roots of the determinant equation without checking that the points are distinct."),
   (r"$-1$ and $-2$", r"Factorises $k^2 - 3k + 2$ as $(k + 1)(k + 2)$.")],
  r"The first two points always satisfy $x + y = 3$, and they are distinct unless $k = 2 - k$, i.e. $k = 1$. So collinearity needs the third point on $x + y = 3$: $3k - 3 = 3$, $k = 2$. (The determinant gives $k^2 - 3k + 2 = 0$ up to a constant factor, i.e. $k = 1$ or $k = 2$, but at $k = 1$ the first two points coincide.) At $k = 2$ the points $(2, 1)$, $(0, 3)$, $(-3, 6)$ are distinct and collinear.",
  r"Accepting a parameter value at which two of the points coincide.",
  "U10-A-collinear-parameter-distinct", "Determinant or common-line insight plus a distinctness trap.",
  check=_c42, values=[FiniteSet(2), FiniteSet(1), FiniteSet(1, 2), FiniteSet(-1, -2)], cognitive="Analysis")

def _c43():
    H = orthocentre((-1, 0), (1, 0), (T_, 2))
    return canon(numer(together(Y - H[1].subs(T_, X))))
q("U10-A-043", "Locus", "Locus of an orthocentre", "Difficult", "Multi-step computation MCQ",
  r"$P(-1, 0)$ and $Q(1, 0)$ are fixed, and $R$ moves on the line $y = 2$. The locus of the orthocentre of triangle $PQR$ is",
  r"$x^2 + 2y = 1$",
  [(r"$x^2 - 2y = 1$", r"Slips the sign of the negative reciprocal, taking the altitude from $P$ with slope $\frac{t - 1}{2}$."),
   (r"$x^2 + y = 1$", r"Finds the altitude correctly but drops the factor $\frac{1}{2}$, writing $y = 1 - t^2$."),
   (r"$x^2 - x + 2y = 0$", r"Draws the altitude from $P$ through the origin, $y = -\frac{t-1}{2}x$, forgetting it must pass through $P$.")],
  r"Let $R = (t, 2)$. The altitude from $R$ is $x = t$. The side $QR$ has slope $\frac{2}{t - 1}$, so the altitude from $P$ is $y = -\frac{t - 1}{2}(x + 1)$. At $x = t$, $y = -\frac{(t - 1)(t + 1)}{2} = \frac{1 - t^2}{2}$. Eliminating $t = x$ gives $2y = 1 - x^2$, i.e. $x^2 + 2y = 1$.",
  r"Sign slips in perpendicular slopes, or an altitude not anchored at its vertex.",
  "U10-A-locus-orthocentre", "Parametrise, two altitudes, intersect, eliminate.",
  check=_c43, values=[canon(X**2 + 2*Y - 1), canon(X**2 - 2*Y - 1), canon(X**2 + Y - 1), canon(X**2 - X + 2*Y)],
  cognitive="Analysis")

def _c44():
    f = sqrt((X - 1)**2 + 4) + sqrt((X - 5)**2 + 16)
    crit = [c for c in solve(diff(f, X), X) if c.is_real]
    return simplify(min(f.subs(X, c) for c in crit))
q("U10-A-044", "Distance formula", "Minimum of a sum of distances via reflection", "Difficult", "Multi-step computation MCQ",
  r"$P$ is a point on the $x$-axis, and $S = (1, 2)$, $T = (5, 4)$. The minimum value of $PS + PT$ is",
  r"$2\sqrt{13}$",
  [(r"$2\sqrt{5}$", r"Takes the straight distance $ST$, ignoring that $P$ must lie on the $x$-axis."),
   (r"$2\sqrt{10}$", r"Reflects $S$ in the $y$-axis to $(-1, 2)$ in place of the $x$-axis."),
   (r"$2\sqrt{2} + 2\sqrt{5}$", r"Places $P$ at $(3, 0)$, directly below the midpoint of $ST$.")],
  r"$S$ and $T$ lie on the same side of the $x$-axis. Reflect $S$ to $S' = (1, -2)$; then $PS + PT = PS' + PT \ge S'T = \sqrt{16 + 36} = 2\sqrt{13}$, with equality where $S'T$ crosses the $x$-axis, at $P = \left(\frac{7}{3}, 0\right)$.",
  r"Reflecting in the wrong axis or using the midpoint as the optimal point.",
  "U10-A-reflection-min-distance", "Non-obvious reflection idea plus a distance.",
  check=_c44, values=[2*sqrt(13), 2*sqrt(5), 2*sqrt(10), 2*sqrt(2) + 2*sqrt(5)], cognitive="Analysis")

def _c45():
    P, Q, R = Matrix([1, 1]), Matrix([4, 2]), Matrix([2, 5])
    S = [P + Q - R, P + R - Q, Q + R - P]
    return area3(*[(s[0], s[1]) for s in S])
q("U10-A-045", "Area of a triangle", "Triangle of possible fourth vertices of a parallelogram", "Difficult", "Multi-step computation MCQ",
  r"$P(1, 1)$, $Q(4, 2)$ and $R(2, 5)$ are three vertices of a parallelogram (in some order). The three possible positions of the fourth vertex form a triangle whose area is",
  r"$22$",
  [(r"$\frac{11}{2}$", r"Gives the area of triangle $PQR$ itself."),
   (r"$11$", r"Doubles the area of $PQR$, using the side ratio $2$ in place of its square."),
   (r"$\frac{99}{2}$", r"Assumes the new triangle has sides three times those of $PQR$ and multiplies by $9$.")],
  r"The possible fourth vertices are $P + Q - R = (3, -2)$, $P + R - Q = (-1, 4)$ and $Q + R - P = (5, 6)$. Triangle $PQR$ is the medial triangle of the triangle they form, so the new area is $4 \cdot \frac{1}{2}|1(2 - 5) + 4(5 - 1) + 2(1 - 2)| = 4 \cdot \frac{11}{2} = 22$.",
  r"Missing the medial-triangle relation, or scaling area linearly.",
  "U10-A-parallelogram-three-fourth-vertices", "Three cases for the fourth vertex, then an area relation.",
  check=_c45, values=[22, Rational(11, 2), 11, Rational(99, 2)], cognitive="Analysis",
  numerical=dict(question=r"$P(1, 1)$, $Q(4, 2)$ and $R(2, 5)$ are three vertices of a parallelogram (in some order). The three possible positions of the fourth vertex form a triangle whose area is", answer=22))

def _c46():
    O, Q = (0, 0), (3, 4)
    ks = set()
    for eq in (Eq(dist(O, (K_, 0))**2, dist(O, Q)**2), Eq(dist((K_, 0), Q)**2, dist(O, Q)**2),
               Eq(dist(O, (K_, 0))**2, dist((K_, 0), Q)**2)):
        for r in solve(eq, K_):
            if r != 0:
                ks.add(r)
    return len(ks)
q("U10-A-046", "Distance formula", "Counting isosceles configurations", "Difficult", "Multi-step computation MCQ",
  r"$O$ is the origin, $Q = (3, 4)$ and $P = (k, 0)$ with $k \ne 0$. The number of real values of $k$ for which triangle $OPQ$ is isosceles is",
  r"$4$",
  [(r"$3$", r"Misses the case $OP = PQ$, which gives $k = \frac{25}{6}$."),
   (r"$5$", r"Counts $k = 0$ from the case $PQ = OQ$, though then $P$ coincides with $O$."),
   (r"$2$", r"Considers only $OP = OQ$, giving $k = \pm 5$.")],
  r"$OQ = 5$. Case $OP = OQ$: $|k| = 5$, so $k = \pm 5$. Case $PQ = OQ$: $(k - 3)^2 + 16 = 25$, so $k = 6$ or $k = 0$, and $k = 0$ is excluded. Case $OP = PQ$: $k^2 = (k - 3)^2 + 16$, so $k = \frac{25}{6}$. The values $5, -5, 6, \frac{25}{6}$ are distinct and none is degenerate, giving $4$ values.",
  r"Missing one of the three equal-side cases, or keeping a degenerate case.",
  "U10-A-isosceles-casework", "Three cases with an excluded degenerate root.",
  check=_c46, values=[4, 3, 5, 2], cognitive="Analysis",
  numerical=dict(question=r"$O$ is the origin, $Q = (3, 4)$ and $P = (k, 0)$ with $k \ne 0$. The number of real values of $k$ for which triangle $OPQ$ is isosceles is", answer=4))

def _c47():
    H = orthocentre((0, 0), (6, 0), (K_, 4))
    s = solve(Eq(H[1], 2), K_)
    return sum(v**2 for v in s)
q("U10-A-047", "Orthocentre", "Orthocentre on a given line", "Difficult", "Inverse/parameter MCQ",
  r"The orthocentre of the triangle with vertices $(0, 0)$, $(6, 0)$ and $(k, 4)$ lies on the line $y = 2$. The sum of the squares of all possible values of $k$ is",
  r"$20$",
  [(r"$52$", r"Slips the sign of the altitude slope, getting the ordinate $-\frac{k(6 - k)}{4}$ and $k^2 - 6k - 8 = 0$."),
   (r"$28$", r"Writes the ordinate as $\frac{k(6 - k)}{2}$, losing a factor $2$, and gets $k^2 - 6k + 4 = 0$."),
   (r"$16$", r"Finds only the root $k = 4$ and misses $k = 2$.")],
  r"The altitude from $(k, 4)$ is $x = k$. The side joining $(6, 0)$ and $(k, 4)$ has direction $(k - 6, 4)$, so the altitude from the origin is $(k - 6)x + 4y = 0$. At $x = k$, $y = \frac{k(6 - k)}{4}$. Setting this to $2$: $k^2 - 6k + 8 = 0$, so $k = 2$ or $4$, and $4 + 16 = 20$.",
  r"Sign slip in the perpendicular direction of an altitude.",
  "U10-A-orthocentre-parameter", "Orthocentre in terms of a parameter, then a quadratic.",
  check=_c47, values=[20, 52, 28, 16], cognitive="Analysis",
  numerical=dict(question=r"The orthocentre of the triangle with vertices $(0, 0)$, $(6, 0)$ and $(k, 4)$ lies on the line $y = 2$. The sum of the squares of all possible values of $k$ is", answer=20))

def _c48():
    b = Symbol('b', positive=True)
    I = incentre((0, 0), (12, 0), (0, b))
    return solve(Eq(I[0], 2), b)[0]
q("U10-A-048", "Incentre", "Parameter from the incentre", "Difficult", "Inverse/parameter MCQ",
  r"The line $\frac{x}{12} + \frac{y}{b} = 1$, where $b > 0$, forms a triangle with the coordinate axes whose incentre is $(2, 2)$. Then $b$ equals",
  r"$5$",
  [(r"$16$", r"Uses $r = \frac{\Delta}{\text{perimeter}}$ in place of $\frac{\Delta}{s}$: $\frac{6b}{12 + b + \sqrt{144 + b^2}} = 2$."),
   (r"$12$", r"Assumes the incentre lying on $y = x$ forces the triangle to be isosceles with equal legs."),
   (r"$6$", r"Uses the centroid formula $\frac{b}{3} = 2$.")],
  r"The triangle has a right angle at the origin, so its incentre is $(r, r)$ with $r = \frac{12 + b - \sqrt{144 + b^2}}{2} = 2$. Then $\sqrt{144 + b^2} = b + 8$, so $144 = 16b + 64$ and $b = 5$. Check: sides $12, 5, 13$ give $r = 2$.",
  r"Using the perimeter for the semi-perimeter, or confusing incentre and centroid.",
  "U10-A-incentre-inverse", "Incentre of a right triangle reversed into a surd equation.",
  check=_c48, values=[5, 16, 12, 6], cognitive="Analysis",
  numerical=dict(question=r"The line $\frac{x}{12} + \frac{y}{b} = 1$, where $b > 0$, forms a triangle with the coordinate axes whose incentre is $(2, 2)$. The value of $b$ is", answer=5))

def _c49():
    th = Symbol('theta', real=True)
    a, b = 10*cos(th), 10*sin(th)
    px, py = Rational(3, 5)*a, Rational(2, 5)*b
    lhs = simplify(4*px**2 + 9*py**2)
    assert lhs.free_symbols == set()
    return canon(4*X**2 + 9*Y**2 - lhs)
q("U10-A-049", "Locus", "Locus of a point on a sliding rod", "Difficult", "Multi-step computation MCQ",
  r"A rod $PQ$ of length $10$ slides with $P$ on the $x$-axis and $Q$ on the $y$-axis. The point $M$ on the rod with $PM : MQ = 2 : 3$ traces the curve",
  r"$4x^2 + 9y^2 = 144$",
  [(r"$9x^2 + 4y^2 = 144$", r"Attaches the ratio to the wrong ends, taking $M = \left(\frac{2a}{5}, \frac{3b}{5}\right)$."),
   (r"$4x^2 + 9y^2 = 36$", r"Uses half the rod length, $a^2 + b^2 = 25$."),
   (r"$9x^2 + 4y^2 = 2500$", r"Inverts $x = \frac{3a}{5}$ as $a = \frac{3x}{5}$, and similarly $b = \frac{2y}{5}$.")],
  r"Let $P = (a, 0)$, $Q = (0, b)$ with $a^2 + b^2 = 100$. Then $M = \frac{3P + 2Q}{5} = \left(\frac{3a}{5}, \frac{2b}{5}\right)$, so $a = \frac{5x}{3}$, $b = \frac{5y}{2}$. Hence $\frac{25x^2}{9} + \frac{25y^2}{4} = 100$, i.e. $4x^2 + 9y^2 = 144$.",
  r"Placing the section weights on the wrong ends of the rod.",
  "U10-A-locus-sliding-rod", "Section formula with a constraint, then elimination.",
  check=_c49, values=[canon(4*X**2 + 9*Y**2 - 144), canon(9*X**2 + 4*Y**2 - 144), canon(4*X**2 + 9*Y**2 - 36), canon(9*X**2 + 4*Y**2 - 2500)],
  cognitive="Analysis")

def _c50():
    P, Q, R = (0, 0), (10, 0), (0, 10)
    D = section(Q, R, 2, 3); E = section(R, P, 2, 3); F = section(P, Q, 2, 3)
    return area3(D, E, F)
q("U10-A-050", "Section formula", "Triangle formed by points dividing the sides", "Difficult", "Multi-step computation MCQ",
  r"In triangle $PQR$ with $P(0, 0)$, $Q(10, 0)$ and $R(0, 10)$, the points $U$, $V$, $W$ divide $QR$, $RP$, $PQ$ respectively in the ratio $2 : 3$ internally (so $QU : UR = 2 : 3$, $RV : VP = 2 : 3$, $PW : WQ = 2 : 3$). The area of triangle $UVW$ is",
  r"$14$",
  [(r"$8$", r"Assumes triangle $UVW$ is similar to $PQR$ with ratio $\frac{2}{5}$, giving $\frac{4}{25} \cdot 50$."),
   (r"$18$", r"Assumes similarity with ratio $\frac{3}{5}$, giving $\frac{9}{25} \cdot 50$."),
   (r"$38$", r"Subtracts only one corner triangle's share, using $\left(1 - \frac{6}{25}\right) \cdot 50$ in place of $\left(1 - \frac{18}{25}\right) \cdot 50$.")],
  r"$U = \frac{3Q + 2R}{5} = (6, 4)$, $V = \frac{3R + 2P}{5} = (0, 6)$, $W = \frac{3P + 2Q}{5} = (4, 0)$. Area $= \frac{1}{2}|6(6 - 0) + 0(0 - 4) + 4(4 - 6)| = \frac{1}{2}|36 - 8| = 14$. (Each corner triangle has area $\frac{6}{25} \cdot 50 = 12$, and $50 - 36 = 14$.)",
  r"Assuming the inner triangle is similar to the original.",
  "U10-A-section-inner-triangle", "Three section points then an area, or a corner-subtraction argument.",
  check=_c50, values=[14, 8, 18, 38], cognitive="Analysis",
  numerical=dict(question=r"In triangle $PQR$ with $P(0, 0)$, $Q(10, 0)$ and $R(0, 10)$, the points $U$, $V$, $W$ divide $QR$, $RP$, $PQ$ respectively in the ratio $2 : 3$ internally (so $QU : UR = 2 : 3$, $RV : VP = 2 : 3$, $PW : WQ = 2 : 3$). The area of triangle $UVW$ is", answer=14))
