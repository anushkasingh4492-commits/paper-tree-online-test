import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

X, Y = symbols('x y', real=True)
k = Symbol('k', real=True)
m = Symbol('m', real=True)

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_FORM = "Forms of the equation of a line"
TOP_DIST = "Distance of a point from a line"
TOP_PAR = "Distance between parallel lines"
TOP_ANG = "Angle between two lines"
TOP_INT = "Intersection and concurrency of lines"
TOP_FOOT = "Foot of perpendicular and image of a point"
TOP_FAM = "Lines through the intersection of two lines"


def _norm(a, b, c):
    """Canonical coefficient tuple of ax + by + c = 0 (first nonzero of a, b scaled to 1)."""
    a, b, c = sympify(a), sympify(b), sympify(c)
    s = a if simplify(a) != 0 else b
    return tuple(simplify(t / s) for t in (a, b, c))


def _lines(*Ls):
    out = [_norm(*L) for L in Ls]
    return tuple(sorted(out, key=lambda t: tuple(float(N(v)) for v in t)))


def _pts(*Ps):
    out = [tuple(simplify(sympify(v)) for v in p) for p in Ps]
    return tuple(sorted(out, key=lambda t: tuple(float(N(v)) for v in t)))


def _val(P, L):
    return L[0]*P[0] + L[1]*P[1] + L[2]


def _dist(P, L):
    P, L = tuple(map(S, P)), tuple(map(S, L))
    return simplify(Abs(_val(P, L)) / sqrt(L[0]**2 + L[1]**2))


def _foot(P, L):
    P, L = tuple(map(S, P)), tuple(map(S, L))
    lam = -_val(P, L) / (L[0]**2 + L[1]**2)
    return (simplify(P[0] + L[0]*lam), simplify(P[1] + L[1]*lam))


def _img(P, L):
    P, L = tuple(map(S, P)), tuple(map(S, L))
    lam = -2*_val(P, L) / (L[0]**2 + L[1]**2)
    return (simplify(P[0] + L[0]*lam), simplify(P[1] + L[1]*lam))


def _meet(L1, L2):
    s = solve([L1[0]*X + L1[1]*Y + L1[2], L2[0]*X + L2[1]*Y + L2[2]], [X, Y], dict=True)[0]
    return (s[X], s[Y])


def _through(P, Q):
    """Coefficients of the line through P and Q."""
    a = Q[1] - P[1]
    b = P[0] - Q[0]
    c = -(a*P[0] + b*P[1])
    return (a, b, c)


def _slope(L):
    return simplify(-sympify(L[0]) / L[1])


def _shoelace(*V):
    n = len(V)
    s = sum(V[i][0]*V[(i+1) % n][1] - V[(i+1) % n][0]*V[i][1] for i in range(n))
    return simplify(Abs(s) / 2)


# ======================================================================= EASY
# ----------------------------------------------------------------------- 001
def _c001():
    p, al = 4, 2*pi/3
    return _norm(cos(al), sin(al), -p)
q("U10-B-001", TOP_FORM, "Normal form from given data", "Easy", "Single-step computation MCQ",
  r"The equation of the line whose perpendicular distance from the origin is $4$ units and whose perpendicular from the origin makes an angle of $120^\circ$ with the positive direction of the $x$-axis is",
  r"$x - \sqrt{3}y + 8 = 0$",
  [(r"$x + \sqrt{3}y - 8 = 0$", r"Takes $\cos 120^\circ = +\frac{1}{2}$, so $\frac{x}{2} + \frac{\sqrt{3}}{2}y = 4$, i.e. $x + \sqrt{3}y - 8 = 0$."),
   (r"$\sqrt{3}x - y - 8 = 0$", r"Interchanges $\cos\alpha$ and $\sin\alpha$, writing $x\sin\alpha + y\cos\alpha = p$: $\frac{\sqrt{3}}{2}x - \frac{1}{2}y = 4$, i.e. $\sqrt{3}x - y - 8 = 0$."),
   (r"$x - \sqrt{3}y + 4 = 0$", r"Clears the halves on the left, $-x + \sqrt{3}y$, but leaves the right side as $4$ instead of $8$.")],
  r"In normal form $x\cos\alpha + y\sin\alpha = p$ with $p = 4$, $\alpha = 120^\circ$: $-\frac{1}{2}x + \frac{\sqrt{3}}{2}y = 4$. Multiplying by $-2$ gives $x - \sqrt{3}y + 8 = 0$.",
  r"Using the wrong sign of $\cos 120^\circ$ or swapping $\cos\alpha$ and $\sin\alpha$ in the normal form.",
  "U10-B-normal-form", "Direct substitution in the normal form with one trigonometric value in the second quadrant.",
  check=_c001,
  values=[_norm(1, -sqrt(3), 8), _norm(1, sqrt(3), -8), _norm(sqrt(3), -1, -8), _norm(1, -sqrt(3), 4)],
  cognitive="Application")

# ----------------------------------------------------------------------- 002
def _c002():
    P = (2, 3)
    a, b = 2*P[0], 2*P[1]          # intercepts, P is the midpoint
    return _norm(b, a, -a*b)       # x/a + y/b = 1  ->  b x + a y - ab = 0
q("U10-B-002", TOP_FORM, "Intercept form with a bisected segment", "Easy", "Single-step computation MCQ",
  r"A line passes through $P(2, 3)$ and the portion of it intercepted between the coordinate axes is bisected at $P$. The equation of the line is",
  r"$3x + 2y = 12$",
  [(r"$2x + 3y = 12$", r"Interchanges the intercepts, taking $6$ on the $x$-axis and $4$ on the $y$-axis: $\frac{x}{6} + \frac{y}{4} = 1$, i.e. $2x + 3y = 12$."),
   (r"$3x + 2y = 6$", r"Takes the coordinates of $P$ themselves as the intercepts: $\frac{x}{2} + \frac{y}{3} = 1$, i.e. $3x + 2y = 6$."),
   (r"$2x + 3y = 13$", r"Treats $P$ as the foot of the perpendicular from the origin: slope $-\frac{2}{3}$ through $(2, 3)$ gives $2x + 3y = 13$.")],
  r"If the intercepts are $(a, 0)$ and $(0, b)$, then $P$ is their midpoint, so $a = 4$ and $b = 6$. The line is $\frac{x}{4} + \frac{y}{6} = 1$, i.e. $3x + 2y = 12$.",
  "Using the coordinates of the midpoint directly as intercepts, or interchanging the intercepts.",
  "U10-B-intercept-form", "One idea (midpoint of the intercepts) followed by the intercept form.",
  check=_c002,
  values=[_norm(3, 2, -12), _norm(2, 3, -12), _norm(3, 2, -6), _norm(2, 3, -13)],
  cognitive="Application")

# ----------------------------------------------------------------------- 003
def _c003():
    return _dist((3, -2), (4, 3, -21))
q("U10-B-003", TOP_DIST, "Perpendicular distance of a point from a line", "Easy", "Single-step computation MCQ",
  r"The perpendicular distance of the point $(3, -2)$ from the line $4x + 3y = 21$ is",
  r"$3$",
  [(r"$\frac{27}{5}$", r"Uses $+21$ for the constant: $\frac{|12 - 6 + 21|}{5} = \frac{27}{5}$."),
   (r"$\frac{15}{7}$", r"Divides by $4 + 3 = 7$ instead of $\sqrt{4^2 + 3^2} = 5$: $\frac{15}{7}$."),
   (r"$\frac{3}{5}$", r"Divides by $4^2 + 3^2 = 25$ instead of its square root: $\frac{15}{25} = \frac{3}{5}$.")],
  r"Write the line as $4x + 3y - 21 = 0$. Then $d = \frac{|4(3) + 3(-2) - 21|}{\sqrt{16 + 9}} = \frac{|-15|}{5} = 3$.",
  "Not moving the constant to the left side before substituting, or dropping the square root in the denominator.",
  "U10-B-dist-point-line", "Single formula application.",
  check=_c003, values=[3, Rational(27, 5), Rational(15, 7), Rational(3, 5)], cognitive="Application",
  numerical=dict(question=r"The perpendicular distance of the point $(3, -2)$ from the line $4x + 3y = 21$ is", answer=3))

# ----------------------------------------------------------------------- 004
def _c004():
    L1 = (6, 8, -14)   # 3x + 4y = 7 scaled by 2
    L2 = (6, 8, 11)
    return simplify(Abs(L1[2] - L2[2]) / sqrt(L1[0]**2 + L1[1]**2))
q("U10-B-004", TOP_PAR, "Distance between parallel lines with unequal coefficients", "Easy", "Single-step computation MCQ",
  r"The distance between the parallel lines $3x + 4y = 7$ and $6x + 8y + 11 = 0$ is",
  r"$\frac{5}{2}$",
  [(r"$\frac{18}{5}$", r"Uses the constants $-7$ and $11$ directly without making the $x$, $y$ coefficients equal: $\frac{|-7 - 11|}{5} = \frac{18}{5}$."),
   (r"$\frac{3}{10}$", r"Scales the first line with the wrong sign of the constant, $6x + 8y + 14 = 0$: $\frac{|14 - 11|}{10} = \frac{3}{10}$."),
   (r"$\frac{9}{5}$", r"Divides by $\sqrt{36 + 64} = 10$ but keeps the unscaled constant $-7$: $\frac{|-7 - 11|}{10} = \frac{9}{5}$.")],
  r"Write the first line as $6x + 8y - 14 = 0$. The distance is $\frac{|-14 - 11|}{\sqrt{36 + 64}} = \frac{25}{10} = \frac{5}{2}$.",
  "Applying $\\frac{|c_1 - c_2|}{\\sqrt{a^2+b^2}}$ before making the coefficients of $x$ and $y$ identical.",
  "U10-B-dist-parallel", "One formula, with the single trap of rescaling one equation.",
  check=_c004, values=[Rational(5, 2), Rational(18, 5), Rational(3, 10), Rational(9, 5)], cognitive="Application")

# ----------------------------------------------------------------------- 005
def _c005():
    m1, m2 = _slope((1, -2, 3)), _slope((3, 1, -1))
    return atan(Abs((m1 - m2) / (1 + m1*m2)))
q("U10-B-005", TOP_ANG, "Acute angle between two lines", "Easy", "Single-step computation MCQ",
  r"The acute angle between the lines $x - 2y + 3 = 0$ and $3x + y - 1 = 0$ is",
  r"$\tan^{-1}(7)$",
  [(r"$\tan^{-1}\left(\frac{7}{5}\right)$", r"Uses $1 - m_1 m_2$ in the denominator: $\frac{\frac{1}{2} + 3}{1 + \frac{3}{2}} = \frac{7}{5}$."),
   (r"$\tan^{-1}(5)$", r"Uses $m_1 + m_2$ in the numerator: $\left|\frac{\frac{1}{2} - 3}{1 - \frac{3}{2}}\right| = 5$."),
   (r"$\tan^{-1}\left(\frac{1}{7}\right)$", r"Inverts the formula, computing $\left|\frac{1 + m_1 m_2}{m_1 - m_2}\right| = \frac{1}{7}$.")],
  r"The slopes are $m_1 = \frac{1}{2}$ and $m_2 = -3$. Then $\tan\theta = \left|\frac{m_1 - m_2}{1 + m_1 m_2}\right| = \left|\frac{\frac{7}{2}}{1 - \frac{3}{2}}\right| = 7$, so $\theta = \tan^{-1}(7)$.",
  "Sign slips in $\\frac{m_1 - m_2}{1 + m_1 m_2}$, especially in the denominator.",
  "U10-B-angle-lines", "Two slopes and one formula.",
  check=_c005, values=[atan(7), atan(Rational(7, 5)), atan(5), atan(Rational(1, 7))], cognitive="Application")

# ----------------------------------------------------------------------- 006
def _c006():
    P = _meet((4, 3, -12), (3, 4, -12))
    return sqrt(P[0]**2 + P[1]**2)
q("U10-B-006", TOP_INT, "Distance of the point of intersection from the origin", "Easy", "Multi-step computation MCQ",
  r"The lines $\frac{x}{3} + \frac{y}{4} = 1$ and $\frac{x}{4} + \frac{y}{3} = 1$ meet at $P$. If $O$ is the origin, then $OP$ equals",
  r"$\frac{12\sqrt{2}}{7}$",
  [(r"$\frac{12}{7}$", r"Finds $P = \left(\frac{12}{7}, \frac{12}{7}\right)$ correctly but reports one coordinate as the distance."),
   (r"$\frac{24}{7}$", r"Adds the coordinates of $P$, $\frac{12}{7} + \frac{12}{7}$, in place of $\sqrt{x^2 + y^2}$."),
   (r"$\frac{7\sqrt{2}}{12}$", r"With $x = y$, solves $x\left(\frac{1}{3} + \frac{1}{4}\right) = 1$ as $x = \frac{7}{12}$, so $OP = \frac{7\sqrt{2}}{12}$.")],
  r"Subtracting the equations gives $x\left(\frac{1}{3} - \frac{1}{4}\right) = y\left(\frac{1}{3} - \frac{1}{4}\right)$, so $x = y$. Then $\frac{7x}{12} = 1$, $x = y = \frac{12}{7}$ and $OP = \frac{12}{7}\sqrt{2}$.",
  "Inverting a sum of fractions incorrectly, or confusing a coordinate with a distance.",
  "U10-B-intersection-dist", "Symmetric pair of equations solved quickly, then a distance.",
  check=_c006, values=[12*sqrt(2)/7, Rational(12, 7), Rational(24, 7), 7*sqrt(2)/12], cognitive="Application")

# ----------------------------------------------------------------------- 007
def _c007():
    return _foot((1, 2), (2, -1, 5))
q("U10-B-007", TOP_FOOT, "Foot of the perpendicular", "Easy", "Single-step computation MCQ",
  r"The foot of the perpendicular from the point $(1, 2)$ to the line $2x - y + 5 = 0$ is",
  r"$(-1, 3)$",
  [(r"$(-3, 4)$", r"Uses the factor $-2$ of the image formula, $\frac{x-1}{2} = \frac{y-2}{-1} = -2$, which gives the image, not the foot."),
   (r"$(3, 1)$", r"Drops the minus sign: $\frac{x-1}{2} = \frac{y-2}{-1} = +1$, giving $(3, 1)$."),
   (r"$(-1, 1)$", r"Takes the $y$ direction ratio as $+1$ instead of $-1$: $x = 1 + 2(-1)$, $y = 2 + (-1)$, giving $(-1, 1)$.")],
  r"For the foot, $\frac{x - 1}{2} = \frac{y - 2}{-1} = -\frac{2(1) - 2 + 5}{2^2 + 1^2} = -1$. Hence $x = -1$, $y = 3$; check: $2(-1) - 3 + 5 = 0$.",
  "Confusing the foot formula with the image formula (factor $-2$), or slipping a sign in the direction ratios.",
  "U10-B-foot", "Direct use of the foot formula.",
  check=_c007, values=[(-1, 3), (-3, 4), (3, 1), (-1, 1)], cognitive="Application")

# ----------------------------------------------------------------------- 008
def _c008():
    return _img((4, 1), (2, -1, 3))
q("U10-B-008", TOP_FOOT, "Image of a point in a line", "Easy", "Single-step computation MCQ",
  r"The image of the point $(4, 1)$ in the line $2x - y + 3 = 0$ is",
  r"$(-4, 5)$",
  [(r"$(0, 3)$", r"Uses the factor $-1$ instead of $-2$, which gives the foot of the perpendicular $(0, 3)$."),
   (r"$(12, -3)$", r"Drops the minus sign: $\frac{x-4}{2} = \frac{y-1}{-1} = +4$, giving $(12, -3)$."),
   (r"$(8, -7)$", r"Interchanges the direction ratios, using $\frac{x-4}{-1} = \frac{y-1}{2} = -4$, giving $(8, -7)$.")],
  r"$\frac{x - 4}{2} = \frac{y - 1}{-1} = -\frac{2(8 - 1 + 3)}{4 + 1} = -4$, so $x = 4 - 8 = -4$ and $y = 1 + 4 = 5$. The midpoint $(0, 3)$ lies on the line, as it should.",
  "Using the foot formula for the image, or mixing up the direction ratios $(a, b)$ of the normal.",
  "U10-B-image", "Direct use of the image formula.",
  check=_c008, values=[(-4, 5), (0, 3), (12, -3), (8, -7)], cognitive="Application")

# ----------------------------------------------------------------------- 009
def _c009():
    P = _meet((1, 1, -3), (2, -1, 0))
    return solve(k*P[0] + 3*P[1] - 11, k)[0]
q("U10-B-009", TOP_INT, "Concurrency with one unknown coefficient", "Easy", "Inverse/parameter MCQ",
  r"The lines $x + y = 3$, $2x - y = 0$ and $kx + 3y = 11$ are concurrent. Then $k$ equals",
  r"$5$",
  [(r"$4$", r"Interchanges the coordinates of the common point, using $(2, 1)$: $2k + 3 = 11$ gives $k = 4$."),
   (r"$-17$", r"Writes the third line as $kx + 3y + 11 = 0$: $k + 6 + 11 = 0$ gives $k = -17$."),
   (r"$\frac{7}{3}$", r"Solves $2x - y = 0$ as $y = -2x$, so $x - 2x = 3$ gives $(-3, 6)$ and $-3k + 18 = 11$, $k = \frac{7}{3}$.")],
  r"Adding $x + y = 3$ and $2x - y = 0$ gives $3x = 3$, so the common point is $(1, 2)$. Substituting in the third line: $k + 6 = 11$, so $k = 5$.",
  "Mis-solving the first two equations or mis-signing the constant of the third line.",
  "U10-B-concurrency-value", "Solve two lines, substitute once.",
  check=_c009, values=[5, 4, -17, Rational(7, 3)], cognitive="Application",
  numerical=dict(question=r"The lines $x + y = 3$, $2x - y = 0$ and $kx + 3y = 11$ are concurrent. The value of $k$ is", answer=5))

# ----------------------------------------------------------------------- 010
def _c010():
    P, th, r = (2, 3), pi/3, 4
    return _pts(*[(P[0] + s*r*cos(th), P[1] + s*r*sin(th)) for s in (1, -1)])
q("U10-B-010", TOP_FORM, "Distance (symmetric) form of a line", "Easy", "Single-step computation MCQ",
  r"The points on the line through $P(2, 3)$ with inclination $60^\circ$ that are at a distance of $4$ units from $P$ are",
  r"$(4,\ 3 + 2\sqrt{3})$ and $(0,\ 3 - 2\sqrt{3})$",
  [(r"$(2 + 2\sqrt{3},\ 5)$ and $(2 - 2\sqrt{3},\ 1)$", r"Interchanges $\cos 60^\circ$ and $\sin 60^\circ$ in $(2 + r\cos\theta,\ 3 + r\sin\theta)$."),
   (r"$(6,\ 3 + 4\sqrt{3})$ and $(-2,\ 3 - 4\sqrt{3})$", r"Uses the direction ratios $(1, \sqrt{3})$ without dividing by their length $2$, so moves a distance of $8$."),
   (r"$(4,\ 3 - 2\sqrt{3})$ and $(0,\ 3 + 2\sqrt{3})$", r"Takes $\sin\theta$ with the wrong sign, which is the line of inclination $-60^\circ$ through $P$.")],
  r"Points on the line are $(2 + r\cos 60^\circ,\ 3 + r\sin 60^\circ) = \left(2 + \frac{r}{2},\ 3 + \frac{\sqrt{3}r}{2}\right)$. With $r = \pm 4$: $(4,\ 3 + 2\sqrt{3})$ and $(0,\ 3 - 2\sqrt{3})$.",
  "Not using unit direction cosines $(\\cos\\theta, \\sin\\theta)$ in the distance form.",
  "U10-B-distance-form", "Direct use of the distance form with $r = \\pm 4$.",
  check=_c010,
  values=[_pts((4, 3 + 2*sqrt(3)), (0, 3 - 2*sqrt(3))), _pts((2 + 2*sqrt(3), 5), (2 - 2*sqrt(3), 1)),
          _pts((6, 3 + 4*sqrt(3)), (-2, 3 - 4*sqrt(3))), _pts((4, 3 - 2*sqrt(3)), (0, 3 + 2*sqrt(3)))],
  cognitive="Application")

# ----------------------------------------------------------------------- 011
def _c011():
    P = (2, -3)
    return _norm(P[0], P[1], -(P[0]**2 + P[1]**2))
q("U10-B-011", TOP_FOOT, "Line from the foot of the perpendicular from the origin", "Easy", "Single-step computation MCQ",
  r"The foot of the perpendicular drawn from the origin to a line $L$ is $(2, -3)$. The equation of $L$ is",
  r"$2x - 3y = 13$",
  [(r"$2x - 3y + 13 = 0$", r"Gets the normal direction $(2, -3)$ right but puts the constant on the wrong side: $2x - 3y = -13$."),
   (r"$2x + 3y + 5 = 0$", r"Takes the perpendicular slope as $-\frac{2}{3}$ instead of $+\frac{2}{3}$: $y + 3 = -\frac{2}{3}(x - 2)$ gives $2x + 3y + 5 = 0$."),
   (r"$3x + 2y = 0$", r"Writes the line joining the origin to $(2, -3)$, which is the perpendicular itself, not $L$.")],
  r"$L$ is perpendicular to the segment from $O$ to $(2, -3)$, so $(2, -3)$ is a normal vector: $2(x - 2) - 3(y + 3) = 0$, i.e. $2x - 3y = 13$.",
  "Writing the line along the perpendicular instead of across it, or the negative reciprocal with the wrong sign.",
  "U10-B-foot-from-origin", "One idea: the foot gives a normal vector.",
  check=_c011, values=[_norm(2, -3, -13), _norm(2, -3, 13), _norm(2, 3, 5), _norm(3, 2, 0)],
  cognitive="Understanding")

# ----------------------------------------------------------------------- 012
def _c012():
    P = _meet((2, -1, -1), (1, 1, -5))
    return _norm(3, 4, -(3*P[0] + 4*P[1]))
q("U10-B-012", TOP_FAM, "Line through an intersection parallel to a given line", "Easy", "Multi-step computation MCQ",
  r"The equation of the line through the point of intersection of $2x - y = 1$ and $x + y = 5$, parallel to $3x + 4y = 0$, is",
  r"$3x + 4y = 18$",
  [(r"$3x + 4y = 17$", r"Interchanges the coordinates of the intersection, using $(3, 2)$: $9 + 8 = 17$."),
   (r"$4x - 3y + 1 = 0$", r"Draws the perpendicular to $3x + 4y = 0$ through $(2, 3)$: $4(x - 2) - 3(y - 3) = 0$."),
   (r"$3x + 4y + 18 = 0$", r"Uses the correct point $(2, 3)$ but writes the constant with the wrong sign.")],
  r"Adding the equations gives $3x = 6$, so the lines meet at $(2, 3)$. A line parallel to $3x + 4y = 0$ is $3x + 4y = c$; with $(2, 3)$, $c = 18$.",
  "Mixing up the parallel and perpendicular families, or misreading the intersection point.",
  "U10-B-family-parallel", "Intersection plus parallel family: two short steps.",
  check=_c012, values=[_norm(3, 4, -18), _norm(3, 4, -17), _norm(4, -3, 1), _norm(3, 4, 18)],
  cognitive="Application")

# ----------------------------------------------------------------------- 013
def _c013():
    L = _through((1, 2), (3, -2))
    return _dist((0, 0), L)
q("U10-B-013", TOP_DIST, "Distance of the origin from a two-point line", "Easy", "Multi-step computation MCQ",
  r"The distance of the origin from the line passing through $(1, 2)$ and $(3, -2)$ is",
  r"$\frac{4}{\sqrt{5}}$",
  [(r"$\frac{4}{5}$", r"Has the correct line $2x + y - 4 = 0$ but divides by $2^2 + 1^2 = 5$ instead of $\sqrt{5}$."),
   (r"$\frac{4}{3}$", r"Divides by $2 + 1 = 3$ instead of $\sqrt{2^2 + 1^2}$."),
   (r"$\sqrt{5}$", r"Takes the slope as $\frac{\Delta x}{\Delta y} = -\frac{1}{2}$, giving $x + 2y - 5 = 0$ and distance $\frac{5}{\sqrt{5}}$.")],
  r"The slope is $\frac{-2 - 2}{3 - 1} = -2$, so the line is $y - 2 = -2(x - 1)$, i.e. $2x + y - 4 = 0$. Its distance from the origin is $\frac{4}{\sqrt{4 + 1}} = \frac{4}{\sqrt{5}}$.",
  "Inverting the slope, or dropping the square root in the distance formula.",
  "U10-B-dist-point-line", "Two-point form then one distance.",
  check=_c013, values=[4/sqrt(5), Rational(4, 5), Rational(4, 3), sqrt(5)], cognitive="Application")

# ----------------------------------------------------------------------- 014
def _c014():
    a, b, c = sqrt(3), 1, -8
    r = sqrt(a**2 + b**2)
    return (atan2(b/r, a/r), -c/r)
q("U10-B-014", TOP_FORM, "Reducing to normal form", "Easy", "Single-step computation MCQ",
  r"The line $\sqrt{3}x + y = 8$ is written in the normal form $x\cos\alpha + y\sin\alpha = p$ with $p > 0$ and $0 \le \alpha < 2\pi$. Then",
  r"$\alpha = \frac{\pi}{6},\ p = 4$",
  [(r"$\alpha = \frac{\pi}{3},\ p = 4$", r"Takes $\tan\alpha = \frac{\sqrt{3}}{1}$, reading the ratio of coefficients upside down ($\tan\alpha$ is $\frac{b}{a} = \frac{1}{\sqrt{3}}$)."),
   (r"$\alpha = \frac{\pi}{6},\ p = 8$", r"Divides the $x$ and $y$ coefficients by $2$ but not the constant $8$."),
   (r"$\alpha = \frac{\pi}{3},\ p = 8$", r"Makes both slips: $\tan\alpha = \sqrt{3}$ and the constant left undivided.")],
  r"Divide by $\sqrt{3 + 1} = 2$: $\frac{\sqrt{3}}{2}x + \frac{1}{2}y = 4$. So $\cos\alpha = \frac{\sqrt{3}}{2}$, $\sin\alpha = \frac{1}{2}$, giving $\alpha = \frac{\pi}{6}$ and $p = 4$.",
  "Not dividing the whole equation by $\\sqrt{a^2 + b^2}$, or reading $\\tan\\alpha$ as $\\frac{a}{b}$.",
  "U10-B-normal-form", "One division and one standard angle.",
  check=_c014, values=[(pi/6, 4), (pi/3, 4), (pi/6, 8), (pi/3, 8)], cognitive="Understanding")

# ----------------------------------------------------------------------- 015
def _c015():
    L1, L2 = (6, -8, 4), (6, -8, 9)          # first line scaled by 2
    s1 = simplify(Abs(L1[2] - L2[2]) / sqrt(L1[0]**2 + L1[1]**2)) == Rational(1, 2)
    P = (1, 1)
    s2 = bool(_val(P, L1) * _val(P, L2) < 0)
    return (s1, s2)
q("U10-B-015", TOP_PAR, "Distance between parallel lines and position of a point", "Easy", "Statement-based MCQ",
  r"Consider the lines $3x - 4y + 2 = 0$ and $6x - 8y + 9 = 0$." "\n"
  r"Statement I: The distance between the two lines is $\frac{1}{2}$." "\n"
  r"Statement II: The point $(1, 1)$ lies between the two lines." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II without checking signs; $6 - 8 + 4 = 2$ and $6 - 8 + 9 = 7$ have the same sign, so $(1, 1)$ is on the same side of both lines."),
   (ST_FF, r"Rejects Statement I by using $\frac{|2 - 9|}{10} = \frac{7}{10}$ without first scaling $3x - 4y + 2 = 0$ to $6x - 8y + 4 = 0$."),
   (ST_FT, r"Makes the unscaled distance slip in Statement I and also misjudges the side of $(1, 1)$.")],
  r"Scaling, the lines are $6x - 8y + 4 = 0$ and $6x - 8y + 9 = 0$, at distance $\frac{|9 - 4|}{10} = \frac{1}{2}$, so Statement I is true. At $(1, 1)$ the left sides are $2$ and $7$, both positive, so $(1, 1)$ lies on the same side of both lines and not between them; Statement II is false.",
  "Forgetting to equalise coefficients, and not using the sign test to decide whether a point lies between two parallel lines.",
  "U10-B-stmt-parallel", "Two quick checks, each a single computation.",
  check=_c015, values=[(T, F_), (T, T), (F_, F_), (F_, T)], cognitive="Analysis")

# ======================================================================= MEDIUM
# ----------------------------------------------------------------------- 016
def _c016():
    m0 = _slope((2, -1, -3))
    return FiniteSet(*solve((m - m0)**2 - (1 + m*m0)**2, m))
q("U10-B-016", TOP_ANG, "Lines through a point at a given angle to a line", "Medium", "Multi-step computation MCQ",
  r"Two lines pass through $(1, 1)$ and each makes an angle of $45^\circ$ with the line $2x - y = 3$. Their equations are",
  r"$3x + y = 4$ and $x - 3y + 2 = 0$",
  [(r"$x - y = 0$ and $x + y = 2$", r"Uses $1 - 2m$ in the denominator: $m - 2 = \pm(1 - 2m)$ gives $m = 1$ and $m = -1$."),
   (r"$3x - y = 2$ and $x + 3y = 4$", r"Reads the slope of $2x - y = 3$ as $-2$: $\frac{m + 2}{1 - 2m} = \pm 1$ gives $m = 3$ and $m = -\frac{1}{3}$."),
   (r"$x - y = 0$ and $3x - y = 2$", r"Drops the denominator, solving $|m - 2| = 1$ to get $m = 1$ and $m = 3$.")],
  r"The given line has slope $2$. A line of slope $m$ makes $45^\circ$ with it when $\left|\frac{m - 2}{1 + 2m}\right| = 1$, so $m - 2 = \pm(1 + 2m)$, giving $m = -3$ or $m = \frac{1}{3}$. Through $(1, 1)$: $y - 1 = -3(x - 1)$, i.e. $3x + y = 4$, and $y - 1 = \frac{1}{3}(x - 1)$, i.e. $x - 3y + 2 = 0$.",
  "Sign slips in $\\tan\\theta = \\left|\\frac{m_1 - m_2}{1 + m_1 m_2}\\right|$ or reading the slope of $ax + by + c = 0$ as $\\frac{a}{b}$.",
  "U10-B-line-at-angle", "Modulus equation with two cases, then two point-slope equations.",
  check=_c016,
  values=[FiniteSet(-3, Rational(1, 3)), FiniteSet(1, -1), FiniteSet(3, Rational(-1, 3)), FiniteSet(1, 3)],
  cognitive="Application", flags="")

# ----------------------------------------------------------------------- 017
def _c017():
    P = _meet((1, -1, -2), (1, 2, -5))
    Q = (1, 5)
    n = (Q[0] - P[0], Q[1] - P[1])
    return _norm(n[0], n[1], -(n[0]*P[0] + n[1]*P[1]))
q("U10-B-017", TOP_FAM, "Line through an intersection at maximum distance from a point", "Medium", "Multi-step computation MCQ",
  r"Among all lines passing through the point of intersection of $x - y = 2$ and $x + 2y = 5$, the one whose distance from the point $Q(1, 5)$ is the greatest is",
  r"$x - 2y = 1$",
  [(r"$2x + y = 7$", r"Takes the line joining the intersection point to $Q$, which is at distance $0$ from $Q$."),
   (r"$3x + y = 10$", r"Maximises the distance from the origin instead of from $Q$: perpendicular to $OP$ with $P(3, 1)$."),
   (r"$x + 2y = 5$", r"Slips the sign of one component of $\overrightarrow{PQ}$, using $(-2, -4)$: $-2(x - 3) - 4(y - 1) = 0$, i.e. $x + 2y = 5$.")],
  r"The lines meet at $P(3, 1)$. Any line through $P$ is at distance at most $PQ$ from $Q$, with equality when it is perpendicular to $PQ$. Since $\overrightarrow{PQ} = (-2, 4)$, the line is $-2(x - 3) + 4(y - 1) = 0$, i.e. $x - 2y = 1$.",
  "Measuring from the origin by habit, or taking the line through the wrong point.",
  "U10-B-family-max-dist", "Intersection, then the geometric fact that the maximum distance is $PQ$.",
  check=_c017, values=[_norm(1, -2, -1), _norm(2, 1, -7), _norm(3, 1, -10), _norm(1, 2, -5)],
  cognitive="Analysis")

# ----------------------------------------------------------------------- 018
def _c018():
    P = _meet((2, -1, -5), (1, 3, 1))
    a = Symbol('a')
    av = solve(P[0]/a - P[1]/a - 1, a)[0]       # x/a + y/(-a) = 1
    return _norm(1, -1, -av)
q("U10-B-018", TOP_FAM, "Line through an intersection with intercepts of opposite signs", "Medium", "Multi-step computation MCQ",
  r"A line passes through the point of intersection of $2x - y = 5$ and $x + 3y + 1 = 0$, and its intercepts on the coordinate axes are non-zero, equal in magnitude and opposite in sign. Its equation is",
  r"$x - y = 3$",
  [(r"$x + y = 1$", r"Takes the intercepts equal in sign as well: $x + y = a$ through $(2, -1)$."),
   (r"$9x - y = 19$", r"Uses the family $(2x - y - 5) + \lambda(x + 3y + 1) = 0$ and the right condition $2 + \lambda = -(3\lambda - 1)$, but solves it with a sign slip as $\lambda = \frac{1}{4}$, giving $\frac{9}{4}x - \frac{1}{4}y - \frac{19}{4} = 0$."),
   (r"$x + 2y = 0$", r"Takes the line through the origin and $(2, -1)$, whose intercepts are both zero.")],
  r"Solving, $y = 2x - 5$ and $x + 6x - 15 + 1 = 0$, so $x = 2$, $y = -1$. Intercepts $a$ and $-a$ give $\frac{x}{a} - \frac{y}{a} = 1$, i.e. $x - y = a$; through $(2, -1)$, $a = 3$. So the line is $x - y = 3$.",
  "Mixing up the equal-intercept and opposite-intercept families, or allowing the zero-intercept line.",
  "U10-B-family-intercepts", "Intersection plus a constrained intercept form.",
  check=_c018, values=[_norm(1, -1, -3), _norm(1, 1, -1), _norm(9, -1, -19), _norm(1, 2, 0)],
  cognitive="Application")

# ----------------------------------------------------------------------- 019
def _c019():
    L, M = (2, -1, -4), (1, -1, 1)
    P = _meet(L, M)
    Q = _img((2, 0), M)              # (2, 0) lies on L
    return _norm(*_through(P, Q))
q("U10-B-019", TOP_FOOT, "Image of a line in a line", "Medium", "Multi-step computation MCQ",
  r"The image of the line $2x - y = 4$ in the line $x - y + 1 = 0$ is",
  r"$x - 2y + 7 = 0$",
  [(r"$x - 2y + 4 = 0$", r"Reflects in $y = x$, simply interchanging $x$ and $y$, and ignores the $+1$ in the mirror."),
   (r"$x - 2y + 1 = 0$", r"Uses the map $(x, y) \to (y + 1, x - 1)$, which is reflection in $y = x - 1$, not in $y = x + 1$."),
   (r"$2x - y + 5 = 0$", r"Reflects $(2, 0)$ correctly to $(-1, 3)$ but assumes the image line is parallel to the original.")],
  r"The lines meet at $P(5, 6)$, which is fixed by the reflection. The point $(2, 0)$ of the given line has image $(2 - 2(3)/2,\ 0 + 2(3)/2) = (-1, 3)$ in $x - y + 1 = 0$. The line through $(5, 6)$ and $(-1, 3)$ has slope $\frac{1}{2}$: $y - 6 = \frac{1}{2}(x - 5)$, i.e. $x - 2y + 7 = 0$.",
  "Treating every reflection as an interchange of $x$ and $y$, or assuming the image of a line is parallel to it.",
  "U10-B-image-of-line", "Needs the invariant intersection point plus the image of one more point.",
  check=_c019, values=[_norm(1, -2, 7), _norm(1, -2, 4), _norm(1, -2, 1), _norm(2, -1, 5)],
  cognitive="Application")

# ----------------------------------------------------------------------- 020
def _c020():
    P, Q = (5, -1), (1, 1)
    n = (Q[0] - P[0], Q[1] - P[1])                    # PQ is normal to L
    L = (n[0], n[1], -(n[0]*Q[0] + n[1]*Q[1]))
    assert _val(Q, L) == 0
    return _img((0, 0), L)
q("U10-B-020", TOP_FOOT, "Image of a point in a line fixed by a given foot", "Medium", "Multi-step computation MCQ",
  r"The foot of the perpendicular from $P(5, -1)$ to a line $L$ is $Q(1, 1)$. The image of the origin in $L$ is",
  r"$\left(\frac{4}{5}, -\frac{2}{5}\right)$",
  [(r"$\left(\frac{2}{5}, -\frac{1}{5}\right)$", r"Finds $L: 2x - y - 1 = 0$ correctly but uses the factor $-1$ of the foot formula, $\frac{x}{2} = \frac{y}{-1} = \frac{1}{5}$, which gives the foot of the perpendicular from the origin."),
   (r"$\left(\frac{6}{5}, \frac{12}{5}\right)$", r"Takes $L$ through $Q$ along $PQ$, i.e. $x + 2y - 3 = 0$, and reflects the origin in it: $\frac{x}{1} = \frac{y}{2} = \frac{6}{5}$."),
   (r"$\left(-\frac{4}{5}, \frac{2}{5}\right)$", r"Finds $L$ correctly but drops the minus sign in $-\frac{2(ax_1 + by_1 + c)}{a^2 + b^2}$, using $-\frac{2}{5}$ in place of $\frac{2}{5}$.")],
  r"$L$ passes through $Q(1, 1)$ and is perpendicular to $PQ$, whose direction is $(-4, 2)$, so $(2, -1)$ is normal to $L$: $2(x - 1) - (y - 1) = 0$, i.e. $2x - y - 1 = 0$. For the image of $(0, 0)$: $\frac{x}{2} = \frac{y}{-1} = -\frac{2(0 - 0 - 1)}{5} = \frac{2}{5}$, so the image is $\left(\frac{4}{5}, -\frac{2}{5}\right)$. Check: the midpoint $\left(\frac{2}{5}, -\frac{1}{5}\right)$ satisfies $2x - y - 1 = 0$.",
  "Using the foot formula for the image, or building $L$ along $PQ$ instead of across it.",
  "U10-B-foot-then-image", "Two linked steps: recover $L$ from a point and its foot, then apply the image formula with a sign trap.",
  check=_c020, values=[(Rational(4, 5), Rational(-2, 5)), (Rational(2, 5), Rational(-1, 5)), (Rational(6, 5), Rational(12, 5)), (Rational(-4, 5), Rational(2, 5))],
  cognitive="Application")

# ----------------------------------------------------------------------- 021
def _c021():
    t = Symbol('t', real=True)
    L = (4, 3, -10)
    ts = solve(Eq(Abs(_val((t, 5 - t), L)) / 5, 1), t)
    P1, P2 = [(s, 5 - s) for s in ts]
    return sqrt((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2)
q("U10-B-021", TOP_DIST, "Points on a line at a given distance from another line", "Medium", "Multi-step computation MCQ",
  r"Two points on the line $x + y = 5$ are each at a distance of $1$ unit from the line $4x + 3y = 10$. The distance between these two points is",
  r"$10\sqrt{2}$",
  [(r"$2\sqrt{2}$", r"Forgets to divide by $5$: $|t + 5| = 1$ gives $t = -4, -6$ and points $2\sqrt{2}$ apart."),
   (r"$10$", r"Finds $t = 0$ and $t = -10$ correctly but reports $|t_1 - t_2|$, the difference of abscissae."),
   (r"$5\sqrt{2}$", r"Gives the distance of one point from the point where the two lines meet, which is half the required length.")],
  r"Take $(t, 5 - t)$. Its distance from $4x + 3y - 10 = 0$ is $\frac{|4t + 15 - 3t - 10|}{5} = \frac{|t + 5|}{5} = 1$, so $t = 0$ or $t = -10$. The points are $(0, 5)$ and $(-10, 15)$, at distance $\sqrt{100 + 100} = 10\sqrt{2}$.",
  "Dropping the denominator of the distance formula, or confusing the difference of abscissae with the distance along the line.",
  "U10-B-points-at-distance", "Parametrise, solve a modulus equation, then a distance.",
  check=_c021, values=[10*sqrt(2), 2*sqrt(2), 10, 5*sqrt(2)], cognitive="Application")

# ----------------------------------------------------------------------- 022
def _c022():
    c = Symbol('c', real=True)
    L1 = (6, -8, -4)        # 3x - 4y = 2 scaled
    sols = solve(Eq(Abs(c - L1[2]) / 10, 1), c)
    return [s for s in sols if s > 0][0]
q("U10-B-022", TOP_PAR, "Unknown constant from the distance between parallel lines", "Medium", "Inverse/parameter MCQ",
  r"The lines $3x - 4y = 2$ and $6x - 8y + c = 0$ are at a distance of $1$ unit from each other. The positive value of $c$ is",
  r"$6$",
  [(r"$8$", r"Uses the unscaled constant $-2$: $\frac{|c + 2|}{10} = 1$ gives $c = 8$ or $-12$."),
   (r"$1$", r"Scales correctly but divides by $5$: $\frac{|c + 4|}{5} = 1$ gives $c = 1$ or $-9$."),
   (r"$14$", r"Scales the first line with the wrong sign of the constant, $6x - 8y + 4 = 0$: $\frac{|c - 4|}{10} = 1$ gives $c = 14$ or $-6$.")],
  r"Write the first line as $6x - 8y - 4 = 0$. Then $\frac{|c - (-4)|}{\sqrt{36 + 64}} = 1$, so $|c + 4| = 10$ and $c = 6$ or $c = -14$. The positive value is $6$.",
  "Not equalising the coefficients before comparing constants.",
  "U10-B-dist-parallel-inverse", "Rescale, then a modulus equation with two roots.",
  check=_c022, values=[6, 8, 1, 14], cognitive="Application",
  numerical=dict(question=r"The lines $3x - 4y = 2$ and $6x - 8y + c = 0$ are at a distance of $1$ unit from each other. The positive value of $c$ is", answer=6))

# ----------------------------------------------------------------------- 023
def _c023():
    m1 = _slope((2, 1, -3))
    return sum(solve((k - m1)**2 - (1 + k*m1)**2, k))
q("U10-B-023", TOP_ANG, "Parameter from the angle between lines", "Medium", "Inverse/parameter MCQ",
  r"The angle between the lines $2x + y = 3$ and $kx - y = 1$ is $45^\circ$. The sum of all possible values of $k$ is",
  r"$\frac{8}{3}$",
  [(r"$0$", r"Uses $1 - m_1 m_2$ in the denominator: $k + 2 = \pm(1 + 2k)$ gives $k = 1$ and $k = -1$."),
   (r"$3$", r"Solves only one case of the modulus, $k + 2 = -(1 - 2k)$, getting $k = 3$ alone."),
   (r"$-\frac{8}{3}$", r"Reads the slope of $2x + y = 3$ as $2$: $k - 2 = \pm(1 + 2k)$ gives $k = -3$ and $k = \frac{1}{3}$.")],
  r"The slopes are $-2$ and $k$. So $\left|\frac{k + 2}{1 - 2k}\right| = 1$: either $k + 2 = 1 - 2k$, giving $k = -\frac{1}{3}$, or $k + 2 = 2k - 1$, giving $k = 3$. The sum is $\frac{8}{3}$.",
  "Keeping only one sign of the modulus, or slipping a sign in $1 + m_1 m_2$.",
  "U10-B-angle-inverse", "Modulus equation with two cases.",
  check=_c023, values=[Rational(8, 3), 0, 3, Rational(-8, 3)], cognitive="Application")

# ----------------------------------------------------------------------- 024
def _c024():
    p, qq = symbols('p q')
    r = -(3*p + 2*qq) / 4
    expr = expand(p*X + qq*Y + r)
    s = solve([expr.coeff(p), expr.coeff(qq)], [X, Y], dict=True)[0]
    return (s[X], s[Y])
q("U10-B-024", TOP_FAM, "Fixed point of a family of lines", "Medium", "Conceptual/application MCQ",
  r"The real numbers $p, q, r$, with $p$ and $q$ not both zero, satisfy $3p + 2q + 4r = 0$. Then every line $px + qy + r = 0$ passes through the fixed point",
  r"$\left(\frac{3}{4}, \frac{1}{2}\right)$",
  [(r"$(3, 2)$", r"Reads the coefficients of $p$ and $q$ off $3p + 2q + 4r = 0$ without dividing by $4$."),
   (r"$\left(-\frac{3}{4}, -\frac{1}{2}\right)$", r"Substitutes $r = \frac{3p + 2q}{4}$ with the wrong sign."),
   (r"$\left(\frac{4}{3}, 2\right)$", r"Divides $4$ by each coefficient instead of each coefficient by $4$.")],
  r"Dividing the condition by $4$: $p\left(\frac{3}{4}\right) + q\left(\frac{1}{2}\right) + r = 0$. This says exactly that $\left(\frac{3}{4}, \frac{1}{2}\right)$ satisfies $px + qy + r = 0$, for every admissible $p, q, r$.",
  "Not normalising the linear condition so that the coefficient of $r$ is $1$.",
  "U10-B-fixed-point", "Recognising a linear condition as a point lying on every line.",
  check=_c024, values=[(Rational(3, 4), Rational(1, 2)), (3, 2), (Rational(-3, 4), Rational(-1, 2)), (Rational(4, 3), 2)],
  cognitive="Understanding")

# ----------------------------------------------------------------------- 025
def _c025():
    P, Q = (1, 2), (5, 4)
    M = (Rational(P[0] + Q[0], 2), Rational(P[1] + Q[1], 2))
    n = (Q[0] - P[0], Q[1] - P[1])
    L = (n[0], n[1], -(n[0]*M[0] + n[1]*M[1]))
    return _dist((0, 0), L)
q("U10-B-025", TOP_FOOT, "Mirror line from a point and its image", "Medium", "Multi-step computation MCQ",
  r"The image of the point $P(1, 2)$ in a line $L$ is $Q(5, 4)$. The distance of the origin from $L$ is",
  r"$\frac{9}{\sqrt{5}}$",
  [(r"$\frac{3}{\sqrt{5}}$", r"Takes $L$ as the line $PQ$ itself, $x - 2y + 3 = 0$."),
   (r"$\frac{4}{\sqrt{5}}$", r"Draws the perpendicular to $PQ$ through $P$ (as if $P$ were the foot): $2x + y = 4$."),
   (r"$\frac{9}{5}$", r"Finds $L: 2x + y = 9$ correctly but divides by $2^2 + 1^2$ instead of $\sqrt{5}$.")],
  r"$L$ is the perpendicular bisector of $PQ$. The midpoint is $(3, 3)$ and $\overrightarrow{PQ} = (4, 2)$, so $L: 4(x - 3) + 2(y - 3) = 0$, i.e. $2x + y = 9$. Its distance from the origin is $\frac{9}{\sqrt{5}}$.",
  "Not recognising that the mirror is the perpendicular bisector of a point and its image.",
  "U10-B-image-inverse", "Mirror from image, then a distance.",
  check=_c025, values=[9/sqrt(5), 3/sqrt(5), 4/sqrt(5), Rational(9, 5)], cognitive="Application")

# ----------------------------------------------------------------------- 026
def _c026():
    P = (2, -1)
    Q = _img(P, (1, 1, -3))
    R = _img(Q, (1, -1, -1))
    return sqrt((R[0] - P[0])**2 + (R[1] - P[1])**2)
q("U10-B-026", TOP_FOOT, "Successive reflections in two perpendicular lines", "Medium", "Multi-step computation MCQ",
  r"$Q$ is the image of $P(2, -1)$ in the line $x + y = 3$, and $R$ is the image of $Q$ in the line $x - y = 1$. The length $PR$ is",
  r"$4$",
  [(r"$2\sqrt{2}$", r"Stops after the first reflection and gives $PQ$, with $Q = (4, 1)$."),
   (r"$\sqrt{10}$", r"Uses the foot $(3, 2)$ of $Q$ on $x - y = 1$ in place of its image."),
   (r"$2$", r"Gives the distance of $P$ from the common point $(2, 1)$ of the two mirrors, which is only half of $PR$.")],
  r"Image of $(2, -1)$ in $x + y - 3 = 0$: $\lambda = -\frac{2(2 - 1 - 3)}{2} = 2$, so $Q = (4, 1)$. Image of $(4, 1)$ in $x - y - 1 = 0$: $\lambda = -\frac{2(4 - 1 - 1)}{2} = -2$, so $R = (2, 3)$. Hence $PR = 4$. (The mirrors are perpendicular and meet at $(2, 1)$, so $R$ is the reflection of $P$ through $(2, 1)$.)",
  "Using a foot where an image is needed, or stopping after one reflection.",
  "U10-B-double-reflection", "Two image computations, or one insight about perpendicular mirrors.",
  check=_c026, values=[4, 2*sqrt(2), sqrt(10), 2], cognitive="Application",
  numerical=dict(question=r"$Q$ is the image of $P(2, -1)$ in the line $x + y = 3$, and $R$ is the image of $Q$ in the line $x - y = 1$. The length $PR$ is", answer=4))

# ----------------------------------------------------------------------- 027
def _c027():
    r = Symbol('r', positive=True)
    P, th = (1, 2), pi/4
    pt = (P[0] + r*cos(th), P[1] + r*sin(th))
    return solve(pt[0] + 2*pt[1] - 7, r)[0]
q("U10-B-027", TOP_FORM, "Distance along a line using the distance form", "Medium", "Multi-step computation MCQ",
  r"A line through $P(1, 2)$ with inclination $45^\circ$ meets the line $x + 2y = 7$ at $Q$. The length $PQ$ is",
  r"$\frac{2\sqrt{2}}{3}$",
  [(r"$\frac{2}{\sqrt{5}}$", r"Gives the perpendicular distance of $P$ from $x + 2y = 7$, not the distance along the $45^\circ$ line."),
   (r"$\frac{2}{3}$", r"Uses $(1 + r,\ 2 + r)$ without the factor $\frac{1}{\sqrt{2}}$, so finds $r = \frac{2}{3}$, which is the change in each coordinate."),
   (r"$\frac{4}{3}$", r"Finds $Q = \left(\frac{5}{3}, \frac{8}{3}\right)$ but adds the coordinate differences $\frac{2}{3} + \frac{2}{3}$.")],
  r"Points on the line are $\left(1 + \frac{r}{\sqrt{2}},\ 2 + \frac{r}{\sqrt{2}}\right)$. Substituting in $x + 2y = 7$: $5 + \frac{3r}{\sqrt{2}} = 7$, so $r = \frac{2\sqrt{2}}{3}$, which is $PQ$.",
  "Confusing the distance measured along a line with the perpendicular distance.",
  "U10-B-distance-form", "Distance form substituted in a second line.",
  check=_c027, values=[2*sqrt(2)/3, 2/sqrt(5), Rational(2, 3), Rational(4, 3)], cognitive="Application")

# ----------------------------------------------------------------------- 028
def _c028():
    p, ta = 5, Rational(3, 4)
    c, s = 1/sqrt(1 + ta**2), ta/sqrt(1 + ta**2)
    return p / c                      # x-intercept of x cos a + y sin a = p
q("U10-B-028", TOP_FORM, "Intercept from the normal form", "Medium", "Single-step computation MCQ",
  r"The perpendicular from the origin to a line $L$ has length $5$ and makes an acute angle $\alpha$ with the positive $x$-axis, where $\tan\alpha = \frac{3}{4}$. The $x$-intercept of $L$ is",
  r"$\frac{25}{4}$",
  [(r"$\frac{25}{3}$", r"Interchanges $\cos\alpha$ and $\sin\alpha$, giving $3x + 4y = 25$."),
   (r"$\frac{5}{4}$", r"Writes $4x + 3y = 5$, forgetting to multiply $p = 5$ by the same factor $5$."),
   (r"$4$", r"Takes the intercept as $p\cos\alpha$ (a projection) instead of $\frac{p}{\cos\alpha}$.")],
  r"Here $\cos\alpha = \frac{4}{5}$ and $\sin\alpha = \frac{3}{5}$, so $L$ is $\frac{4}{5}x + \frac{3}{5}y = 5$, i.e. $4x + 3y = 25$. Putting $y = 0$ gives $x = \frac{25}{4}$.",
  "Using $p\\cos\\alpha$ for the intercept or swapping $\\cos\\alpha$ and $\\sin\\alpha$.",
  "U10-B-normal-form", "Normal form from a ratio, then an intercept.",
  check=_c028, values=[Rational(25, 4), Rational(25, 3), Rational(5, 4), 4], cognitive="Application")

# ----------------------------------------------------------------------- 029
def _c029():
    L = (3, 4, -12)
    s1 = _foot((1, 1), L) == (Rational(2, 5), Rational(1, 5))
    s2 = _img((0, 0), L) == (Rational(72, 25), Rational(96, 25))
    return (s1, s2)
q("U10-B-029", TOP_FOOT, "Foot and image checked together", "Medium", "Statement-based MCQ",
  r"Consider the line $3x + 4y = 12$." "\n"
  r"Statement I: The foot of the perpendicular from $(1, 1)$ to the line is $\left(\frac{2}{5}, \frac{1}{5}\right)$." "\n"
  r"Statement II: The image of the origin in the line is $\left(\frac{72}{25}, \frac{96}{25}\right)$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I, which is what the foot formula gives with the sign of $\lambda$ reversed ($\lambda = -\frac{1}{5}$ instead of $+\frac{1}{5}$)."),
   (ST_FF, r"Rejects Statement II by computing the foot $\left(\frac{36}{25}, \frac{48}{25}\right)$ of the origin and expecting that as the image."),
   (ST_TF, r"Makes both slips: reverses the sign in Statement I and uses the foot for the image in Statement II.")],
  r"For $(1, 1)$: $\frac{x - 1}{3} = \frac{y - 1}{4} = -\frac{3 + 4 - 12}{25} = \frac{1}{5}$, so the foot is $\left(\frac{8}{5}, \frac{9}{5}\right)$ and Statement I is false. For the origin: $\frac{x}{3} = \frac{y}{4} = -\frac{2(-12)}{25} = \frac{24}{25}$, so the image is $\left(\frac{72}{25}, \frac{96}{25}\right)$ and Statement II is true.",
  "Sign errors in $\\lambda = -\\frac{ax_1 + by_1 + c}{a^2 + b^2}$ and confusing the foot with the image.",
  "U10-B-stmt-foot-image", "Two separate formula checks, each with a sign trap.",
  check=_c029, values=[(F_, T), (T, T), (F_, F_), (T, F_)], cognitive="Analysis")

# ----------------------------------------------------------------------- 030
def _c030():
    L1, L2 = (6, 8, -10), (6, 8, 15)     # 3x + 4y = 5 scaled
    side = Abs(L1[2] - L2[2]) / 10
    return side**2
q("U10-B-030", TOP_PAR, "Square with two sides on parallel lines", "Medium", "Multi-step computation MCQ",
  r"Two sides of a square lie on the lines $3x + 4y = 5$ and $6x + 8y + 15 = 0$. The area of the square is",
  r"$\frac{25}{4}$",
  [(r"$16$", r"Uses $\frac{|-5 - 15|}{5} = 4$ as the side, without scaling $3x + 4y - 5 = 0$ to $6x + 8y - 10 = 0$."),
   (r"$\frac{1}{4}$", r"Scales with the wrong sign, $6x + 8y + 10 = 0$, so the side is $\frac{|10 - 15|}{10} = \frac{1}{2}$."),
   (r"$\frac{25}{8}$", r"Treats the distance $\frac{5}{2}$ between the lines as a diagonal, so area $= \frac{1}{2}\left(\frac{5}{2}\right)^2$.")],
  r"The two lines are parallel (opposite sides). With $6x + 8y - 10 = 0$ and $6x + 8y + 15 = 0$, the side is $\frac{|-10 - 15|}{10} = \frac{5}{2}$, so the area is $\frac{25}{4}$.",
  "Comparing constants of parallel lines before equalising coefficients.",
  "U10-B-dist-parallel", "Rescale, distance, then square it.",
  check=_c030, values=[Rational(25, 4), 16, Rational(1, 4), Rational(25, 8)], cognitive="Application")

# ----------------------------------------------------------------------- 031
def _c031():
    Ls = [(1, -1, 0), (1, -1, 2), (2, -1, 0), (2, -1, 3)]   # y=x, y=x+2, y=2x, y=2x+3
    V = [_meet(Ls[0], Ls[2]), _meet(Ls[0], Ls[3]), _meet(Ls[1], Ls[3]), _meet(Ls[1], Ls[2])]
    return _shoelace(*V)
q("U10-B-031", TOP_PAR, "Area of a parallelogram formed by two pairs of parallel lines", "Medium", "Multi-step computation MCQ",
  r"The area of the parallelogram formed by the lines $y = x$, $y = x + 2$, $y = 2x$ and $y = 2x + 3$ is",
  r"$6$",
  [(r"$3$", r"Uses $\frac{1}{2}\left|\frac{(c_1 - c_2)(d_1 - d_2)}{m_1 - m_2}\right|$, halving as if for a triangle."),
   (r"$\frac{3\sqrt{10}}{5}$", r"Multiplies the two distances between parallel sides, $\frac{2}{\sqrt{2}} \cdot \frac{3}{\sqrt{5}}$, which is not the area."),
   (r"$2$", r"Uses $m_1 + m_2 = 3$ in the denominator of $\left|\frac{(c_1 - c_2)(d_1 - d_2)}{m_1 - m_2}\right|$.")],
  r"The vertices are $(0, 0)$, $(-3, -3)$, $(-1, 1)$ and $(2, 4)$ (intersections of one line from each pair). By the shoelace formula, or by $\left|\frac{(c_1 - c_2)(d_1 - d_2)}{m_1 - m_2}\right| = \frac{2 \cdot 3}{1} = 6$, the area is $6$.",
  "Multiplying the two widths instead of width times side length.",
  "U10-B-parallelogram-area", "Four intersections, or a formula that needs care with the denominator.",
  check=_c031, values=[6, 3, 3*sqrt(10)/5, 2], cognitive="Application",
  numerical=dict(question=r"The area of the parallelogram formed by the lines $y = x$, $y = x + 2$, $y = 2x$ and $y = 2x + 3$ is", answer=6))

# ----------------------------------------------------------------------- 032
def _c032():
    P = _meet((2, -3, -1), (3, 2, -8))
    L = _through((0, 0), (4, 3))
    return _dist(P, L)
q("U10-B-032", TOP_INT, "Distance of a point of intersection from a line", "Medium", "Multi-step computation MCQ",
  r"The lines $2x - 3y = 1$ and $3x + 2y = 8$ meet at $P$. The perpendicular distance of $P$ from the line joining the origin to $(4, 3)$ is",
  r"$\frac{2}{5}$",
  [(r"$1$", r"Uses $(1, 2)$ for $P$, interchanging its coordinates: $\frac{|3 - 8|}{5} = 1$."),
   (r"$\frac{2}{7}$", r"Divides $|3(2) - 4(1)|$ by $3 + 4$ instead of $5$."),
   (r"$\frac{2}{25}$", r"Divides by $3^2 + 4^2$ instead of $\sqrt{3^2 + 4^2}$.")],
  r"Solving, $4x - 6y = 2$ and $9x + 6y = 24$ give $13x = 26$, so $P = (2, 1)$. The line through $(0, 0)$ and $(4, 3)$ is $3x - 4y = 0$, and the distance is $\frac{|6 - 4|}{5} = \frac{2}{5}$.",
  "Slips in solving the pair or in the denominator of the distance formula.",
  "U10-B-intersection-dist", "Solve a pair, form a two-point line, apply the distance formula.",
  check=_c032, values=[Rational(2, 5), 1, Rational(2, 7), Rational(2, 25)], cognitive="Application")

# ----------------------------------------------------------------------- 033
def _c033():
    c, s = symbols('c s', real=True)
    P, L, PQ = (1, 1), (2, 1, -13), 5
    eq = L[0]*(P[0] + PQ*c) + L[1]*(P[1] + PQ*s) + L[2]
    sols = solve([eq, c**2 + s**2 - 1], [c, s], dict=True)
    slopes = [sl[s] / sl[c] for sl in sols if sl[s] != 0]   # line not parallel to the x-axis
    assert len(slopes) == 1
    return slopes[0]
q("U10-B-033", TOP_DIST, "Direction of a line from a distance measured along it", "Medium", "Inverse/parameter MCQ",
  r"A line through $P(1, 1)$, not parallel to the $x$-axis, meets the line $2x + y = 13$ at a point $Q$ such that $PQ = 5$. The slope of the line $PQ$ is",
  r"$\frac{4}{3}$",
  [(r"$\frac{3}{4}$", r"Writes the point as $(1 + 5\sin\theta,\ 1 + 5\cos\theta)$, swapping the roles of $\cos\theta$ and $\sin\theta$; then $2\sin\theta + \cos\theta = 2$ gives $\cos\theta = \frac{4}{5}$, $\sin\theta = \frac{3}{5}$ and slope $\frac{3}{4}$."),
   (r"$\frac{1}{2}$", r"Assumes $PQ$ is perpendicular to $2x + y = 13$ and takes the slope $\frac{1}{2}$ of its normal, without using $PQ = 5$."),
   (r"$\frac{4}{5}$", r"Solves correctly for $\cos\theta = \frac{3}{5}$, $\sin\theta = \frac{4}{5}$ but reports $\sin\theta$ instead of $\tan\theta$.")],
  r"Write $Q = (1 + 5\cos\theta,\ 1 + 5\sin\theta)$. Substituting in $2x + y = 13$: $3 + 5(2\cos\theta + \sin\theta) = 13$, so $\sin\theta = 2 - 2\cos\theta$. Then $\cos^2\theta + (2 - 2\cos\theta)^2 = 1$ gives $5\cos^2\theta - 8\cos\theta + 3 = 0$, so $\cos\theta = 1$ or $\cos\theta = \frac{3}{5}$. The value $\cos\theta = 1$ gives the horizontal line $y = 1$, which is excluded, so $\cos\theta = \frac{3}{5}$, $\sin\theta = \frac{4}{5}$ and the slope is $\frac{4}{3}$.",
  r"Mixing up $\cos\theta$ and $\sin\theta$ in the distance form, or assuming the shortest route is the required one.",
  "U10-B-direction-from-distance", "Reverse use of the distance form: a trigonometric pair reduced to a quadratic, with one root excluded by the stem.",
  check=_c033, values=[Rational(4, 3), Rational(3, 4), Rational(1, 2), Rational(4, 5)], cognitive="Application",
  numerical=dict(question=r"A line through $P(1, 1)$, not parallel to the $x$-axis, meets the line $2x + y = 13$ at a point $Q$ such that $PQ = 5$. If $m$ is the slope of the line $PQ$, then $3m$ is", answer=4))

# ----------------------------------------------------------------------- 034
def _c034():
    s = solve([X + 2*Y - 3, k*X - Y - 4], [X, Y], dict=True)[0]
    c1 = solve_univariate_inequality(s[X] > 0, k, relational=False)
    c2 = solve_univariate_inequality(s[Y] > 0, k, relational=False)
    return Intersection(c1, c2)
q("U10-B-034", TOP_INT, "Intersection point in the first quadrant", "Medium", "Inverse/parameter MCQ",
  r"The lines $x + 2y = 3$ and $kx - y = 4$ intersect at a point lying in the first quadrant (both coordinates positive). The set of all real values of $k$ is",
  r"$\left(\frac{4}{3}, \infty\right)$",
  [(r"$\left(-\frac{1}{2}, \infty\right)$", r"Imposes only $x = \frac{11}{1 + 2k} > 0$ and ignores the condition on $y$."),
   (r"$\left(-\infty, -\frac{1}{2}\right) \cup \left(\frac{4}{3}, \infty\right)$", r"Imposes only $y = \frac{3k - 4}{1 + 2k} > 0$ and ignores the condition on $x$."),
   (r"$\left(-\frac{1}{2}, \frac{4}{3}\right)$", r"Writes $y = \frac{4 - 3k}{1 + 2k}$ with the numerator sign reversed, then combines with $x > 0$.")],
  r"From $y = kx - 4$: $x + 2kx - 8 = 3$, so $x = \frac{11}{1 + 2k}$ and $y = \frac{3k - 4}{1 + 2k}$. $x > 0$ needs $k > -\frac{1}{2}$; then $y > 0$ needs $3k - 4 > 0$. Hence $k > \frac{4}{3}$.",
  "Using only one of the two coordinate conditions, or a sign slip when solving the pair.",
  "U10-B-intersection-quadrant", "Solve with a parameter, then two rational inequalities.",
  check=_c034,
  values=[Interval.open(Rational(4, 3), oo), Interval.open(Rational(-1, 2), oo),
          Union(Interval.open(-oo, Rational(-1, 2)), Interval.open(Rational(4, 3), oo)),
          Interval.open(Rational(-1, 2), Rational(4, 3))],
  cognitive="Analysis")

# ----------------------------------------------------------------------- 035
def _c035():
    kk = Symbol('kk', real=True)
    P = (1, 2)
    L = (3, -1, kk)
    Q = _img(P, L)
    return solve(Q[0] + Q[1] - 5, kk)[0]
q("U10-B-035", TOP_FOOT, "Parameter of a mirror from a condition on the image", "Medium", "Inverse/parameter MCQ",
  r"The image of the point $(1, 2)$ in the line $3x - y + k = 0$ is $(\alpha, \beta)$. If $\alpha + \beta = 5$, then $k$ equals",
  r"$-6$",
  [(r"$4$", r"Drops the minus sign in $\lambda = -\frac{2(3 - 2 + k)}{10}$, so $\frac{1 + k}{5} = 1$ gives $k = 4$."),
   (r"$-11$", r"Uses the foot formula (factor $1$ instead of $2$): $\lambda = -\frac{1 + k}{10} = 1$ gives $k = -11$."),
   (r"$-\frac{7}{2}$", r"Takes the direction ratios as $(3, 1)$ instead of $(3, -1)$: $\alpha + \beta = 3 + 4\lambda = 5$, so $\lambda = \frac{1}{2}$ and $k = -\frac{7}{2}$.")],
  r"$\frac{\alpha - 1}{3} = \frac{\beta - 2}{-1} = \lambda = -\frac{2(3 - 2 + k)}{10} = -\frac{1 + k}{5}$. Then $\alpha + \beta = (1 + 3\lambda) + (2 - \lambda) = 3 + 2\lambda = 5$, so $\lambda = 1$ and $k = -6$. Check: the image is $(4, 1)$ and the midpoint $\left(\frac{5}{2}, \frac{3}{2}\right)$ lies on $3x - y - 6 = 0$.",
  "Sign and factor slips in the image formula when the mirror contains a parameter.",
  "U10-B-image-param", "Image formula with a parameter plus one linear condition.",
  check=_c035, values=[-6, 4, -11, Rational(-7, 2)], cognitive="Application")

# ----------------------------------------------------------------------- 036
def _c036():
    c = Symbol('c', real=True)
    P, O = (4, -2), (0, 0)
    cands = solve(Eq(Abs(3*P[0] - 4*P[1] + c) / 5, 2), c)
    good = [cv for cv in cands if (3*P[0] - 4*P[1] + cv) * (cv) < 0]
    return _norm(3, -4, good[0])
q("U10-B-036", TOP_DIST, "Parallel line at a given distance separating two points", "Medium", "Multi-step computation MCQ",
  r"A line $L$ is parallel to $3x - 4y = 5$, is at a distance of $2$ units from $P(4, -2)$, and the origin and $P$ lie on opposite sides of $L$. The equation of $L$ is",
  r"$3x - 4y = 10$",
  [(r"$3x - 4y = 30$", r"Takes the other root of $|20 + c| = 10$; for $c = -30$ the origin and $P$ give $-30$ and $-10$, the same side."),
   (r"$3x - 4y = -10$", r"Finds $c = -10$ in $3x - 4y + c = 0$ but then writes $3x - 4y = c$, mixing the two forms."),
   (r"$3x - 4y = 15$", r"Measures the distance $2$ from the given line $3x - 4y = 5$ instead of from $P$, and keeps the one of $3x - 4y = 15$, $3x - 4y = -5$ that separates $O$ and $P$.")],
  r"Let $L: 3x - 4y + c = 0$. Then $\frac{|12 + 8 + c|}{5} = 2$, so $c = -10$ or $c = -30$. The origin gives the value $c$ and $P$ gives $20 + c$; these have opposite signs only for $c = -10$ (values $-10$ and $10$). So $L$ is $3x - 4y = 10$.",
  "Not applying the sign test to choose between the two parallel lines.",
  "U10-B-parallel-side-condition", "Two candidate lines, then a sign test to select one.",
  check=_c036, values=[_norm(3, -4, -10), _norm(3, -4, -30), _norm(3, -4, 10), _norm(3, -4, -15)],
  cognitive="Analysis")

# ----------------------------------------------------------------------- 037
def _c037():
    kk = Symbol('kk', real=True)
    a, b, c = kk + 1, kk - 1, -2*kk
    s1 = simplify(a*1 + b*(-1) + c) == 0          # must vanish for every k
    # x + y - 2 = 0 is a member iff (a, b, c) is proportional to (1, 1, -2)
    s2 = len(solve([a - b, -2*a - c], kk, dict=True)) > 0
    return (bool(s1), bool(s2))
q("U10-B-037", TOP_FAM, "Members and fixed point of a one-parameter family", "Medium", "Statement-based MCQ",
  r"Consider the family of lines $(k + 1)x + (k - 1)y = 2k$, where $k$ is real." "\n"
  r"Statement I: Every line of the family passes through the point $(1, -1)$." "\n"
  r"Statement II: The line $x + y = 2$ is a member of the family for some real $k$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Believes both: tests $(1, -1)$ only at $k = 1$, where it fits, and assumes the line $x + y - 2 = 0$ appearing in the rearrangement is a member."),
   (ST_TF, r"Accepts Statement I after checking $(1, -1)$ for $k = 1$ only."),
   (ST_FT, r"Rewrites the family as $(x - y) + k(x + y - 2) = 0$ and wrongly counts $x + y - 2 = 0$ as a member.")],
  r"Rewrite as $(x - y) + k(x + y - 2) = 0$: every member passes through the intersection of $x - y = 0$ and $x + y = 2$, which is $(1, 1)$. At $(1, -1)$ the left side minus right side is $(k + 1) - (k - 1) - 2k = 2 - 2k$, zero only for $k = 1$, so Statement I is false. For $x + y = 2$ we would need $k + 1 = k - 1$, impossible, so Statement II is false.",
  "Checking a fixed point for one value of the parameter, and forgetting that $L_1 + kL_2 = 0$ never gives $L_2 = 0$ itself.",
  "U10-B-stmt-family", "Recasting the family and testing two claims.",
  check=_c037, values=[(F_, F_), (T, T), (T, F_), (F_, T)], cognitive="Analysis")

# ----------------------------------------------------------------------- 038
def _c038():
    L1, L2, L3 = (0, 1, 0), (2, -5, 0), (2, -1, -8)
    O, P, Q = _meet(L1, L2), _meet(L1, L3), _meet(L2, L3)
    u = (O[0] - P[0], O[1] - P[1]); v = (Q[0] - P[0], Q[1] - P[1])
    cosang = (u[0]*v[0] + u[1]*v[1]) / (sqrt(u[0]**2 + u[1]**2) * sqrt(v[0]**2 + v[1]**2))
    return acos(cosang)
q("U10-B-038", TOP_ANG, "Interior angle of a triangle formed by three lines", "Difficult", "Multi-step computation MCQ",
  r"A triangle is formed by the lines $y = 0$, $2x - 5y = 0$ and $2x - y = 8$. Its interior angle at the vertex where $y = 0$ meets $2x - y = 8$ is",
  r"$\pi - \tan^{-1}(2)$",
  [(r"$\tan^{-1}(2)$", r"Takes the acute angle between $y = 0$ and $2x - y = 8$ from the formula without checking which angle is interior."),
   (r"$\tan^{-1}\left(\frac{2}{5}\right)$", r"Gives the interior angle at the origin, between $y = 0$ and $2x - 5y = 0$."),
   (r"$\tan^{-1}\left(\frac{8}{9}\right)$", r"Gives the interior angle at the third vertex $(5, 2)$.")],
  r"The vertices are $O(0, 0)$, $P(4, 0)$ and $Q(5, 2)$. At $P$, $\overrightarrow{PO} = (-4, 0)$ and $\overrightarrow{PQ} = (1, 2)$ have dot product $-4 < 0$, so the angle is obtuse. The acute angle between the lines is $\tan^{-1}(2)$, so the interior angle is $\pi - \tan^{-1}(2)$.",
  "Assuming the angle formula always gives the interior angle of a triangle.",
  "U10-B-interior-angle", "Three vertices from three lines, then the trap: the formula gives the acute angle but the interior angle is obtuse.",
  check=_c038, values=[pi - atan(2), atan(2), atan(Rational(2, 5)), atan(Rational(8, 9))], cognitive="Analysis")

# ----------------------------------------------------------------------- 039
def _c039():
    V, S = (2, -1), (1, 1, -2)
    m0 = _slope(S)
    ms = solve((m - m0)**2 - 3*(1 + m*m0)**2, m)          # 60 degrees with the base
    W = [_meet((mm, -1, V[1] - mm*V[0]), S) for mm in ms]
    return _shoelace(V, W[0], W[1])
q("U10-B-039", TOP_DIST, "Equilateral triangle from a vertex and the opposite side", "Medium", "Multi-step computation MCQ",
  r"An equilateral triangle has one vertex at $(2, -1)$, and the opposite side lies along $x + y = 2$. The area of the triangle is",
  r"$\frac{\sqrt{3}}{6}$",
  [(r"$\frac{\sqrt{3}}{3}$", r"Takes the altitude as $|2 - 1 - 2| = 1$, forgetting the divisor $\sqrt{2}$, so area $= \frac{1}{\sqrt{3}}$."),
   (r"$\frac{1}{4}$", r"Uses $\frac{1}{2} h^2$ with $h = \frac{1}{\sqrt{2}}$, treating the altitude as the base as well."),
   (r"$\frac{\sqrt{3}}{8}$", r"Puts the altitude $\frac{1}{\sqrt{2}}$ into $\frac{\sqrt{3}}{4}a^2$ as if it were the side.")],
  r"The altitude is $h = \frac{|2 - 1 - 2|}{\sqrt{2}} = \frac{1}{\sqrt{2}}$. For an equilateral triangle $h = \frac{\sqrt{3}}{2}a$, so area $= \frac{\sqrt{3}}{4}a^2 = \frac{h^2}{\sqrt{3}} = \frac{1}{2\sqrt{3}} = \frac{\sqrt{3}}{6}$.",
  "Confusing the altitude with the side in the area formula.",
  "U10-B-equilateral", "Distance of a point from a line combined with equilateral-triangle relations.",
  check=_c039, values=[sqrt(3)/6, sqrt(3)/3, Rational(1, 4), sqrt(3)/8], cognitive="Application")

# ======================================================================= DIFFICULT
# ----------------------------------------------------------------------- 040
def _c040():
    rows = lambda kv: [(kv, 1, 1), (1, kv, 1), (1, 1, kv)]
    D = Matrix(rows(k)).det()
    good = []
    for r in set(solve(D, k)):
        Ls = rows(r)
        distinct = all(Matrix([Ls[i], Ls[j]]).rank() == 2 for i in range(3) for j in range(i + 1, 3))
        if distinct:
            good.append(r)
    return FiniteSet(*good)
q("U10-B-040", TOP_INT, "Concurrency of three distinct lines with a parameter", "Difficult", "Inverse/parameter MCQ",
  r"The lines $kx + y + 1 = 0$, $x + ky + 1 = 0$ and $x + y + k = 0$ are three distinct concurrent lines. The set of all real values of $k$ is",
  r"$\{-2\}$",
  [(r"$\{1\}$", r"Keeps the repeated root $k = 1$ of $(k - 1)^2(k + 2) = 0$, but then all three equations are $x + y + 1 = 0$, so the lines are not distinct."),
   (r"$\{1, -2\}$", r"Solves the determinant condition and keeps both roots without checking distinctness."),
   (r"$\{-1, 2\}$", r"Factorises $k^3 - 3k + 2$ with the signs of the roots reversed.")],
  r"Concurrency requires $\begin{vmatrix} k & 1 & 1 \\ 1 & k & 1 \\ 1 & 1 & k \end{vmatrix} = k^3 - 3k + 2 = (k - 1)^2(k + 2) = 0$. For $k = 1$ all three equations become $x + y + 1 = 0$, which are not distinct lines. For $k = -2$ the lines are distinct and all pass through $(1, 1)$. So $k = -2$ only.",
  "Accepting every root of the determinant without checking that the lines are distinct.",
  "U10-B-concurrency-param", "Determinant factorisation plus a casework trap on coincident lines.",
  check=_c040, values=[FiniteSet(-2), FiniteSet(1), FiniteSet(1, -2), FiniteSet(-1, 2)], cognitive="Analysis")

# ----------------------------------------------------------------------- 041
def _c041():
    mp = Symbol('mp', positive=True)
    P = (2, 3)
    L = (mp, -1, 0)
    Q = _img(P, L)
    return [s for s in solve(Q[1], mp) if s > 0][0]
q("U10-B-041", TOP_FOOT, "Mirror through the origin sending a point to the x-axis", "Difficult", "Inverse/parameter MCQ",
  r"The image of the point $(2, 3)$ in the line $y = mx$, where $m > 0$, lies on the $x$-axis. Then $m$ equals",
  r"$\frac{\sqrt{13} - 2}{3}$",
  [(r"$\frac{\sqrt{13} + 2}{3}$", r"Uses $\tan\frac{\theta}{2} = \frac{1 + \cos\theta}{\sin\theta}$, which is actually $\cot\frac{\theta}{2}$, with $\tan\theta = \frac{3}{2}$."),
   (r"$\frac{3}{4}$", r"Halves the slope of $OP$, taking $\tan\frac{\theta}{2} = \frac{1}{2}\tan\theta$."),
   (r"$\frac{\sqrt{13} + 3}{2}$", r"Bisects the angle between $OP$ and the $y$-axis, so the image would lie on the $y$-axis instead.")],
  r"Reflection in a line through $O$ preserves distance from $O$, so the mirror must bisect the angle between $OP$ and the $x$-axis. With $\tan\theta = \frac{3}{2}$, $\cos\theta = \frac{2}{\sqrt{13}}$ and $\sin\theta = \frac{3}{\sqrt{13}}$, so $m = \tan\frac{\theta}{2} = \frac{\sin\theta}{1 + \cos\theta} = \frac{3}{\sqrt{13} + 2} = \frac{\sqrt{13} - 2}{3}$. (The other bisector has negative slope.) Equivalently, the image has $y$-coordinate $\frac{4m + 3(m^2 - 1)}{1 + m^2} = 0$, giving $3m^2 + 4m - 3 = 0$.",
  "Halving the slope instead of the angle, or using the cotangent half-angle identity.",
  "U10-B-image-on-axis", "Image formula with a parameter leading to a quadratic, or a half-angle insight; the sign of $m$ selects the root.",
  check=_c041, values=[(sqrt(13) - 2)/3, (sqrt(13) + 2)/3, Rational(3, 4), (sqrt(13) + 3)/2], cognitive="Analysis")

# ----------------------------------------------------------------------- 042
def _c042():
    M = (2, 1, -4)
    P, Q = (5, 2), (4, 6)
    Pp = _img(P, M)
    return _meet(M, _through(Pp, Q))
q("U10-B-042", TOP_FOOT, "Point of incidence of a reflected ray", "Difficult", "Multi-step computation MCQ",
  r"A ray of light from $P(5, 2)$ strikes the plane mirror along the line $2x + y = 4$ and, after reflection, passes through $Q(4, 6)$. The point at which the ray strikes the mirror is",
  r"$(1, 2)$",
  [(r"$\left(\frac{9}{5}, \frac{2}{5}\right)$", r"Uses the foot of the perpendicular from $P$ in place of its image; the line from that foot to $Q$ meets the mirror at the foot itself."),
   (r"$\left(-\frac{9}{7}, \frac{46}{7}\right)$", r"Computes the image of $P$ with the wrong sign of $\lambda$, getting $\left(\frac{57}{5}, \frac{26}{5}\right)$, and joins it to $Q$."),
   (r"$\left(\frac{9}{10}, \frac{11}{5}\right)$", r"Assumes the ray strikes at the foot of the perpendicular from the midpoint of $PQ$.")],
  r"The image of $P(5, 2)$ in $2x + y - 4 = 0$: $\lambda = -\frac{2(10 + 2 - 4)}{5} = -\frac{16}{5}$, so $P' = \left(-\frac{7}{5}, -\frac{6}{5}\right)$. The reflected ray lies on $P'Q$, whose slope is $\frac{6 + \frac{6}{5}}{4 + \frac{7}{5}} = \frac{4}{3}$: $4x - 3y + 2 = 0$. Solving with $2x + y = 4$ gives $10x - 10 = 0$, so the point is $(1, 2)$.",
  "Joining $Q$ to the foot instead of the image of $P$.",
  "U10-B-reflection-ray", "Image of a point, a line through two points, and an intersection.",
  check=_c042, values=[(1, 2), (Rational(9, 5), Rational(2, 5)), (Rational(-9, 7), Rational(46, 7)), (Rational(9, 10), Rational(11, 5))],
  cognitive="Application")

# ----------------------------------------------------------------------- 043
def _c043():
    R = _meet((1, 1, -5), (2, -1, -1))
    P, Q = (-1, 2), (3, 4)
    sols = []
    # line through R with normal (cos t, sin t): solve |n.(P-R)| = |n.(Q-R)| via the two cases
    for sgn in (1, -1):
        # n.(P - R) = sgn * n.(Q - R)  ->  n.((P - R) - sgn (Q - R)) = 0
        dvec = ((P[0] - R[0]) - sgn*(Q[0] - R[0]), (P[1] - R[1]) - sgn*(Q[1] - R[1]))
        n = (-dvec[1], dvec[0])          # normal perpendicular to dvec
        sols.append((n[0], n[1], -(n[0]*R[0] + n[1]*R[1])))
    return _lines(*sols)
q("U10-B-043", TOP_FAM, "Lines through an intersection equidistant from two points", "Difficult", "Multi-step computation MCQ",
  r"Lines are drawn through the point of intersection of $x + y = 5$ and $2x - y = 1$ so that each is equidistant from the points $P(-1, 2)$ and $Q(3, 4)$. The equations of these lines are",
  r"$x - 2y + 4 = 0$ and $y = 3$",
  [(r"$x - 2y + 4 = 0$ and $2x + y = 7$", r"Gets the line parallel to $PQ$, but for the second takes the line through $R$ perpendicular to $PQ$ instead of through the midpoint of $PQ$."),
   (r"$y = 3$ and $2x + y = 7$", r"Misses the case parallel to $PQ$, and adds the perpendicular to $PQ$ through $R$."),
   (r"$x - 2y + 5 = 0$ and $y = 3$", r"Draws the parallel to $PQ$ through the midpoint $(1, 3)$ instead of through $R(2, 3)$.")],
  r"The lines meet at $R(2, 3)$. A line through $R$ is equidistant from $P$ and $Q$ when either it is parallel to $PQ$ or it passes through the midpoint $(1, 3)$ of $PQ$. Slope of $PQ$ is $\frac{1}{2}$, giving $y - 3 = \frac{1}{2}(x - 2)$, i.e. $x - 2y + 4 = 0$. The line through $R(2, 3)$ and $(1, 3)$ is $y = 3$.",
  "Missing one of the two cases (parallel to $PQ$, or through its midpoint).",
  "U10-B-family-equidistant", "Two-case geometric reasoning on a family through an intersection.",
  check=_c043,
  values=[_lines((1, -2, 4), (0, 1, -3)), _lines((1, -2, 4), (2, 1, -7)), _lines((0, 1, -3), (2, 1, -7)), _lines((1, -2, 5), (0, 1, -3))],
  cognitive="Analysis")

# ----------------------------------------------------------------------- 044
def _c044():
    V, H = (2, 2), (3, 4, -4)
    m0 = _slope(H)
    ms = solve((m - m0)**2 - (1 + m*m0)**2, m)
    legs = [(mm, -1, V[1] - mm*V[0]) for mm in ms]
    P1, P2 = _meet(legs[0], H), _meet(legs[1], H)
    return _shoelace(V, P1, P2)
q("U10-B-044", TOP_DIST, "Isosceles right triangle from its hypotenuse line", "Difficult", "Multi-step computation MCQ",
  r"The hypotenuse of an isosceles right-angled triangle lies along $3x + 4y = 4$, and the vertex containing the right angle is $(2, 2)$. The area of the triangle is",
  r"$4$",
  [(r"$2$", r"Takes each leg equal to the altitude $2$, so area $= \frac{1}{2}(2)(2)$."),
   (r"$8$", r"Uses hypotenuse $= 2h = 4$ and altitude $h = 2$ but forgets the $\frac{1}{2}$: $4 \times 2$."),
   (r"$2\sqrt{2}$", r"Takes the hypotenuse as $h\sqrt{2} = 2\sqrt{2}$ (the leg length) and computes $\frac{1}{2}(2\sqrt{2})(2)$.")],
  r"The altitude from the right angle to the hypotenuse is $h = \frac{|6 + 8 - 4|}{5} = 2$. In an isosceles right triangle the foot of this altitude is the midpoint of the hypotenuse and $h$ equals half the hypotenuse, so the hypotenuse is $4$ and the area is $\frac{1}{2}(4)(2) = 4$. (The legs have slopes $\frac{1}{7}$ and $-7$, making $45^\circ$ with the hypotenuse.)",
  "Mixing up altitude, leg and hypotenuse in an isosceles right triangle.",
  "U10-B-isosceles-right", "Distance from a line plus the special-triangle geometry; the legs need the $45^\\circ$ angle condition if done directly.",
  check=_c044, values=[4, 2, 8, 2*sqrt(2)], cognitive="Analysis",
  numerical=dict(question=r"The hypotenuse of an isosceles right-angled triangle lies along $3x + 4y = 4$, and the vertex containing the right angle is $(2, 2)$. The area of the triangle is", answer=4))

# ----------------------------------------------------------------------- 045
def _c045():
    Mm, Nn = (1, 4), (4, -4)
    L = (1, 1, -2)
    assert _val(Mm, L) * _val(Nn, L) < 0                     # opposite sides
    Np = _img(Nn, L)
    assert (Np[1] - Mm[1]) * L[1] != -(Np[0] - Mm[0]) * L[0]  # line MN' not parallel to L
    return sqrt((Mm[0] - Np[0])**2 + (Mm[1] - Np[1])**2)
q("U10-B-045", TOP_FOOT, "Maximum of a difference of distances via reflection", "Difficult", "Multi-step computation MCQ",
  r"$P$ is a point on the line $x + y = 2$, and $M(1, 4)$, $N(4, -4)$ are fixed points. The maximum value of $|PM - PN|$ is",
  r"$\sqrt{61}$",
  [(r"$\sqrt{73}$", r"Uses the triangle inequality bound $|PM - PN| \le MN = \sqrt{9 + 64}$, but equality needs $P$ on line $MN$ outside the segment, and line $MN$ meets $x + y = 2$ between $M$ and $N$."),
   (r"$\sqrt{101}$", r"Reflects $N$ with the wrong sign of $\lambda$, getting $(2, -6)$, and computes its distance from $M$: $\sqrt{1 + 100}$."),
   (r"$\sqrt{65}$", r"Uses the foot $(5, -3)$ of $N$ in place of its image and computes its distance from $M$: $\sqrt{16 + 49}$.")],
  r"$x + y - 2$ is $3$ at $M$ and $-2$ at $N$, so they are on opposite sides. Reflect $N$: $\lambda = -\frac{2(-2)}{2} = 2$, so $N' = (6, -2)$, on the same side as $M$, and $PN = PN'$ for every $P$ on the line. Then $|PM - PN| = |PM - PN'| \le MN' = \sqrt{25 + 36} = \sqrt{61}$, with equality where line $MN'$ meets $x + y = 2$, at $(16, -14)$ (there $PM = 3\sqrt{61}$, $PN = 2\sqrt{61}$).",
  r"Applying $|PM - PN| \le MN$ directly when the points are on opposite sides, or using the foot instead of the image.",
  "U10-B-max-diff-reflection", "Recognise that the points must first be brought to the same side by a reflection, then an image, a distance and an attainment check.",
  check=_c045, values=[sqrt(61), sqrt(73), sqrt(101), sqrt(65)], cognitive="Analysis",
  numerical=dict(question=r"$P$ is a point on the line $x + y = 2$, and $M(1, 4)$, $N(4, -4)$ are fixed points. If $\mu$ is the maximum value of $|PM - PN|$, then $\mu^2$ is", answer=61))

# ----------------------------------------------------------------------- 046
def _c046():
    a, b, c = symbols('a b c')
    D = Matrix([[a, 1, 1], [1, b, 1], [1, 1, c]]).det()
    cs = solve(D, c)[0]
    return simplify(1/(1 - a) + 1/(1 - b) + 1/(1 - cs))
q("U10-B-046", TOP_INT, "Identity from a concurrency condition", "Difficult", "Multi-step computation MCQ",
  r"The lines $ax + y + 1 = 0$, $x + by + 1 = 0$ and $x + y + c = 0$, where $a$, $b$, $c$ are distinct and none of them equals $1$, are concurrent. Then $\frac{1}{1 - a} + \frac{1}{1 - b} + \frac{1}{1 - c}$ equals",
  r"$1$",
  [(r"$-1$", r"Works with $\frac{1}{a - 1}$ in each term, which reverses the sign of the sum."),
   (r"$2$", r"Stops at the concurrency condition $a + b + c - abc = 2$ and reports that constant."),
   (r"$\frac{7}{3}$", r"Expands the determinant as $abc - a - b - c - 2 = 0$ (wrong sign on the constant), then tests $a = b = 0$, $c = -2$: $1 + 1 + \frac{1}{3}$.")],
  r"Concurrency gives $\begin{vmatrix} a & 1 & 1 \\ 1 & b & 1 \\ 1 & 1 & c \end{vmatrix} = 0$. Subtract the first column from the second and third: $\begin{vmatrix} a & 1 - a & 1 - a \\ 1 & b - 1 & 0 \\ 1 & 0 & c - 1 \end{vmatrix} = 0$. Dividing by $(1 - a)(1 - b)(1 - c)$ gives $\frac{a}{1 - a} + \frac{1}{1 - b} + \frac{1}{1 - c} = 0$, and since $\frac{a}{1 - a} = \frac{1}{1 - a} - 1$, the required sum is $1$.",
  "Sign errors when reducing the determinant or mixing $\\frac{1}{1-a}$ with $\\frac{1}{a-1}$.",
  "U10-B-concurrency-identity", "Determinant manipulation with a non-obvious division step.",
  check=_c046, values=[1, -1, 2, Rational(7, 3)], cognitive="Analysis",
  numerical=dict(question=r"The lines $ax + y + 1 = 0$, $x + by + 1 = 0$ and $x + y + c = 0$, where $a$, $b$, $c$ are distinct and none of them equals $1$, are concurrent. The value of $\frac{1}{1 - a} + \frac{1}{1 - b} + \frac{1}{1 - c}$ is", answer=1))

# ----------------------------------------------------------------------- 047
def _c047():
    C = (2, 3)
    S = (1, 2, -3)
    half = _dist(C, S)
    c = Symbol('c', real=True)
    sols = solve(Eq(Abs(2*C[0] - C[1] - c) / sqrt(5), half), c)
    return FiniteSet(*sols)
q("U10-B-047", TOP_PAR, "Sides of a square from its centre and one side", "Difficult", "Multi-step computation MCQ",
  r"One side of a square lies along $x + 2y = 3$ and its centre is $(2, 3)$. The two sides perpendicular to this side are",
  r"$2x - y = 6$ and $2x - y = -4$",
  [(r"$2x - y = 11$ and $2x - y = -9$", r"Places the perpendicular sides at a full side length $2\sqrt{5}$ from the centre instead of half of it."),
   (r"$2x - y = 5$ and $2x - y = -5$", r"Places them at distance $\sqrt{5}$ from the origin instead of from the centre, ignoring $2(2) - 3 = 1$."),
   (r"$2x - y = 4$ and $2x - y = -6$", r"Writes $|1 + c| = 5$ instead of $|1 - c| = 5$ when the side is $2x - y = c$.")],
  r"The centre is at distance $\frac{|2 + 6 - 3|}{\sqrt{5}} = \sqrt{5}$ from the given side, so half the side length is $\sqrt{5}$. A perpendicular side is $2x - y = c$, at distance $\frac{|4 - 3 - c|}{\sqrt{5}} = \sqrt{5}$ from the centre, so $|1 - c| = 5$ and $c = 6$ or $c = -4$.",
  "Using the full side instead of the half side, or measuring from the origin instead of the centre.",
  "U10-B-square-sides", "Square geometry turned into two distance conditions.",
  check=_c047, values=[FiniteSet(6, -4), FiniteSet(11, -9), FiniteSet(5, -5), FiniteSet(4, -6)], cognitive="Analysis")

# ----------------------------------------------------------------------- 048
def _c048():
    L, M = (1, -1, -1), (2, 1, -4)
    P = _meet(L, M)
    Q = _img((1, 0), M)          # (1, 0) lies on L
    return _norm(*_through(P, Q))
q("U10-B-048", TOP_FOOT, "Image of a line in an oblique mirror", "Difficult", "Multi-step computation MCQ",
  r"The image of the line $x - y = 1$ in the line $2x + y = 4$ is",
  r"$x - 7y + 3 = 0$",
  [(r"$3x + 3y = 7$", r"Takes the image line perpendicular to the given line, through the common point $\left(\frac{5}{3}, \frac{2}{3}\right)$."),
   (r"$11x - 17y = 7$", r"Reflects $(1, 0)$ with the wrong sign of $\lambda$, getting $\left(-\frac{3}{5}, -\frac{4}{5}\right)$, and joins it to the common point."),
   (r"$x - y + 1 = 0$", r"Interchanges $x$ and $y$ as if the mirror were $y = x$.")],
  r"The lines meet at $\left(\frac{5}{3}, \frac{2}{3}\right)$, which is its own image. The point $(1, 0)$ of $x - y = 1$ has image given by $\lambda = -\frac{2(2 - 4)}{5} = \frac{4}{5}$: $\left(\frac{13}{5}, \frac{4}{5}\right)$. The line through these two points has slope $\frac{\frac{4}{5} - \frac{2}{3}}{\frac{13}{5} - \frac{5}{3}} = \frac{1}{7}$, giving $x - 7y + 3 = 0$.",
  "Treating every mirror like $y = x$, or a sign slip in the image formula.",
  "U10-B-image-of-line", "Invariant point, image of a second point, and a line through both, with fractions throughout.",
  check=_c048, values=[_norm(1, -7, 3), _norm(3, 3, -7), _norm(11, -17, -7), _norm(1, -1, 1)], cognitive="Application")

# ----------------------------------------------------------------------- 049
def _c049():
    L1, L2 = (1, 2, -3), (1, 2, -8)
    d = Abs(L1[2] - L2[2]) / sqrt(L1[0]**2 + L1[1]**2)
    PQ = sqrt(10)
    s = d / PQ                       # sine of the angle between L and the parallel lines
    t = s / sqrt(1 - s**2)           # tangent of that angle
    m0 = _slope(L1)
    return FiniteSet(*solve((m - m0)**2 - t**2*(1 + m*m0)**2, m))
q("U10-B-049", TOP_PAR, "Line cutting a fixed length between parallel lines", "Difficult", "Multi-step computation MCQ",
  r"A line $L$ through the point $(1, 1)$ meets the lines $x + 2y = 3$ and $x + 2y = 8$ at points $P$ and $Q$ with $PQ = \sqrt{10}$. The possible slopes of $L$ are",
  r"$\frac{1}{3}$ and $-3$",
  [(r"$-\frac{1}{3}$ and $3$", r"Takes the slope of the parallel lines as $+\frac{1}{2}$: $\left|\frac{m - \frac{1}{2}}{1 + \frac{m}{2}}\right| = 1$ gives $m = 3$ and $m = -\frac{1}{3}$."),
   (r"$1$ and $-1$", r"Uses $1 + \frac{m}{2}$ in the denominator: $\left|\frac{m + \frac{1}{2}}{1 + \frac{m}{2}}\right| = 1$ gives $m = \pm 1$."),
   (r"$-\frac{1}{7}$ and $-1$", r"Takes the distance between the lines as $\frac{5}{5} = 1$ (dividing by $1^2 + 2^2$), so $\sin\theta = \frac{1}{\sqrt{10}}$, $\tan\theta = \frac{1}{3}$, leading to $m = -\frac{1}{7}$ or $m = -1$.")],
  r"The distance between the parallel lines is $\frac{|8 - 3|}{\sqrt{5}} = \sqrt{5}$. If $L$ makes angle $\theta$ with them, then $PQ\sin\theta = \sqrt{5}$, so $\sin\theta = \frac{1}{\sqrt{2}}$ and $\theta = 45^\circ$. With slope $-\frac{1}{2}$ for the given lines, $\left|\frac{m + \frac{1}{2}}{1 - \frac{m}{2}}\right| = 1$ gives $m = \frac{1}{3}$ or $m = -3$.",
  "Not linking the intercepted length to the distance between the lines through $\\sin\\theta$.",
  "U10-B-intercepted-segment", "Combines distance between parallel lines, a trigonometric link, and the angle formula with two cases.",
  check=_c049, values=[FiniteSet(Rational(1, 3), -3), FiniteSet(Rational(-1, 3), 3), FiniteSet(1, -1), FiniteSet(Rational(-1, 7), -1)],
  cognitive="Analysis")

# ----------------------------------------------------------------------- 050
def _c050():
    kk = Symbol('kk', real=True)
    a, b, c = 2 + kk, 1 - kk, -(5 + kk)
    sols = solve(Eq(c**2, Rational(1, 2)*(a**2 + b**2)), kk)
    return FiniteSet(*sols)
q("U10-B-050", TOP_FAM, "Members of a family at a given distance from the origin", "Difficult", "Inverse/parameter MCQ",
  r"For real $k$, consider the lines $(2 + k)x + (1 - k)y = 5 + k$. The set of all real values of $k$ for which the line is at a distance of $\frac{1}{\sqrt{2}}$ unit from the origin is",
  r"$\{-\frac{5}{2}\}$",
  [(r"$\{1 - \sqrt{6}, 1 + \sqrt{6}\}$", r"Inverts the distance while clearing the root, writing $(5 + k)^2 = 2[(2 + k)^2 + (1 - k)^2]$, which gives $k^2 - 2k - 5 = 0$."),
   (r"$\{-\frac{45}{16}\}$", r"Expands $(1 - k)^2$ as $1 + k^2$: $2(25 + 10k + k^2) = 2k^2 + 4k + 5$, so $16k = -45$."),
   (r"$\{\frac{45}{22}\}$", r"Writes the constant as $5 - k$: $2(25 - 10k + k^2) = 2k^2 + 2k + 5$, so $22k = 45$.")],
  r"The condition is $\frac{(5 + k)^2}{(2 + k)^2 + (1 - k)^2} = \frac{1}{2}$, i.e. $2(25 + 10k + k^2) = 2k^2 + 2k + 5$. The $k^2$ terms cancel, leaving $18k = -45$, so $k = -\frac{5}{2}$ only (the line $-x + 7y = 5$, at distance $\frac{5}{\sqrt{50}} = \frac{1}{\sqrt{2}}$). Geometrically, every member passes through $(2, 1)$, from which two lines are at distance $\frac{1}{\sqrt{2}}$ from the origin; the other one is $x - y = 1$, which is the excluded line of the pencil $(2x + y - 5) + k(x - y - 1) = 0$ and is given by no real $k$. The set is $\{-\frac{5}{2}\}$.",
  "Expecting two parameter values because two lines through the fixed point qualify, not noticing that one of them is the member no value of $k$ produces.",
  "U10-B-family-param-distance", "Squaring the distance condition, noticing the quadratic degenerates to a linear equation, and explaining via the excluded member of the pencil; the expected two-root answer is a trap.",
  check=_c050, values=[FiniteSet(Rational(-5, 2)), FiniteSet(1 - sqrt(6), 1 + sqrt(6)), FiniteSet(Rational(-45, 16)), FiniteSet(Rational(45, 22))], cognitive="Analysis",
  numerical=dict(question=r"For real $k$, consider the lines $(2 + k)x + (1 - k)y = 5 + k$. The number of real values of $k$ for which the line is at a distance of $\frac{1}{\sqrt{2}}$ unit from the origin is", answer=1))
