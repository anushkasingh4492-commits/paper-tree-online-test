import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

TOP_PT = "Coordinates of a point in space"
TOP_DC = "Direction ratios and direction cosines"
TOP_ANG = "Angle between two lines"
XII = "XII"


def V(*c):
    return Matrix([nsimplify(x) for x in c])


def tup(v):
    return tuple(simplify(x) for x in v)


def dist(P, Q):
    return sqrt(sum((P[i] - Q[i])**2 for i in range(3)))


def dirn(v):
    """Canonical direction-ratio tuple: divide by the first nonzero entry."""
    v = [nsimplify(x) for x in v]
    lead = [x for x in v if x != 0][0]
    return tuple(simplify(x / lead) for x in v)


def cosang(a, b):
    a = Matrix(a); b = Matrix(b)
    return simplify(a.dot(b) / (a.norm() * b.norm()))


def collinear(P, Q, R):
    return (Matrix(Q) - Matrix(P)).cross(Matrix(R) - Matrix(P)) == zeros(3, 1)


# ================================================================ EASY

def _c1():
    return dist(V(1, 2, -3), V(3, -1, 3))
q("U11-A-001", TOP_PT, "Distance between two points", "Easy", "Single-step computation MCQ",
  r"The distance between the points $P(1, 2, -3)$ and $Q(3, -1, 3)$ is",
  r"$7$",
  [(r"$\sqrt{17}$", r"Adds corresponding coordinates: $(4, 1, 0)$ gives $\sqrt{16+1+0}=\sqrt{17}$."),
   (r"$11$", r"Adds the absolute differences $2+3+6$ without squaring."),
   (r"$49$", r"Stops at the sum of squares $4+9+36$ and does not take the square root.")],
  r"The differences of coordinates are $2, -3, 6$, so $PQ = \sqrt{4+9+36} = \sqrt{49} = 7$.",
  "Adding coordinates or absolute differences instead of using the distance formula.",
  "U11-A-distance-basic", "Direct use of the distance formula in one step.",
  check=_c1, values=[7, sqrt(17), 11, 49], cognitive="Application", source_class="XI",
  numerical=dict(question=r"The distance between the points $P(1, 2, -3)$ and $Q(3, -1, 3)$ is", answer=7))


def _c2():
    P = V(3, -4, 12)
    foot = V(0, P[1], 0)          # foot of perpendicular on the y-axis
    return dist(P, foot)
q("U11-A-002", TOP_PT, "Distance of a point from a coordinate axis", "Easy", "Single-step computation MCQ",
  r"The distance of the point $P(3, -4, 12)$ from the $y$-axis is",
  r"$3\sqrt{17}$",
  [(r"$4$", r"Takes $|y|$, the distance from the $xz$-plane, as the distance from the $y$-axis."),
   (r"$13$", r"Computes the distance from the origin, $\sqrt{9+16+144}$."),
   (r"$5$", r"Uses $\sqrt{x^2+y^2}$, which is the distance from the $z$-axis.")],
  r"The foot of the perpendicular from $P$ to the $y$-axis is $(0, -4, 0)$, so the distance is $\sqrt{x^2+z^2} = \sqrt{9+144} = \sqrt{153} = 3\sqrt{17}$.",
  "Using the coordinate itself, or the wrong pair of coordinates, for the distance from an axis.",
  "U11-A-distance-axis", "One idea: the distance from the $y$-axis uses the other two coordinates.",
  check=_c2, values=[3*sqrt(17), 4, 13, 5], cognitive="Understanding", source_class="XI")


def _c3():
    P, Q = V(2, -3, 4), V(8, 0, 10)
    m, n = 1, 2
    return tup((m*Q + n*P) / (m + n))
q("U11-A-003", TOP_PT, "Section formula (internal)", "Easy", "Single-step computation MCQ",
  r"The point which divides the line segment joining $P(2, -3, 4)$ and $Q(8, 0, 10)$ internally in the ratio $1 : 2$ (that is, $PX : XQ = 1 : 2$) is",
  r"$(4, -2, 6)$",
  [(r"$(6, -1, 8)$", r"Attaches the weights to the wrong ends, computing $\frac{1\cdot P + 2\cdot Q}{3}$, which divides in the ratio $2 : 1$."),
   (r"$(5, -\frac{3}{2}, 7)$", r"Takes the midpoint of $PQ$, ignoring the ratio."),
   (r"$(-4, -6, -2)$", r"Uses the external division formula $\frac{1\cdot Q - 2\cdot P}{1-2}$.")],
  r"$X = \frac{1\cdot Q + 2\cdot P}{3} = \left(\frac{8+4}{3}, \frac{0-6}{3}, \frac{10+8}{3}\right) = (4, -2, 6)$.",
  "Placing the ratio weights on the wrong endpoints.",
  "U11-A-section-internal", "Single application of the section formula.",
  check=_c3, values=[(4, -2, 6), (6, -1, 8), (5, Rational(-3, 2), 7), (-4, -6, -2)],
  cognitive="Application", source_class="XI")


def _c4():
    P, Q, G = V(2, -1, 4), V(3, 5, -2), V(1, 2, 1)
    x, y, z = symbols('x y z')
    R = Matrix([x, y, z])
    s = solve(list((P + Q + R) / 3 - G), [x, y, z], dict=True)[0]
    return (s[x], s[y], s[z])
q("U11-A-004", TOP_PT, "Centroid of a triangle", "Easy", "Single-step computation MCQ",
  r"Two vertices of a triangle are $P(2, -1, 4)$ and $Q(3, 5, -2)$, and its centroid is $G(1, 2, 1)$. The third vertex $R$ is",
  r"$(-2, 2, 1)$",
  [(r"$(2, -2, -1)$", r"Computes $P + Q - 3G$, which reverses every sign."),
   (r"$(-4, -2, -1)$", r"Uses $G = P + Q + R$, dropping the factor $3$, so $R = G - P - Q$."),
   (r"$(-3, 0, 0)$", r"Uses $2G$ in place of $3G$, giving $R = 2G - P - Q$.")],
  r"Since $G = \frac{P+Q+R}{3}$, $R = 3G - P - Q = (3-2-3,\ 6+1-5,\ 3-4+2) = (-2, 2, 1)$.",
  "Forgetting the factor 3 in the centroid formula when solving for a vertex.",
  "U11-A-centroid-vertex", "One rearrangement of the centroid formula.",
  check=_c4, values=[(-2, 2, 1), (2, -2, -1), (-4, -2, -1), (-3, 0, 0)],
  cognitive="Application", source_class="XI")


def _c5():
    d = V(2, -1, 2)
    u = d / d.norm()
    if u[0] > 0:
        u = -u
    return tup(u)
q("U11-A-005", TOP_DC, "Direction cosines from direction ratios", "Easy", "Single-step computation MCQ",
  r"A line has direction ratios $2, -1, 2$ and makes an obtuse angle with the positive direction of the $x$-axis. Its direction cosines are",
  r"$-\frac{2}{3}, \frac{1}{3}, -\frac{2}{3}$",
  [(r"$\frac{2}{3}, -\frac{1}{3}, \frac{2}{3}$", r"Normalises correctly but ignores the obtuse-angle condition, so $l > 0$."),
   (r"$-\frac{2}{5}, \frac{1}{5}, -\frac{2}{5}$", r"Divides by $|2|+|-1|+|2| = 5$ instead of $\sqrt{4+1+4} = 3$."),
   (r"$-\frac{2}{9}, \frac{1}{9}, -\frac{2}{9}$", r"Divides by $4+1+4 = 9$, forgetting the square root.")],
  r"$\sqrt{2^2+1^2+2^2} = 3$, so the direction cosines are $\pm\left(\frac{2}{3}, -\frac{1}{3}, \frac{2}{3}\right)$. An obtuse angle with the $x$-axis needs $l < 0$, so take the negative sign: $-\frac{2}{3}, \frac{1}{3}, -\frac{2}{3}$.",
  "Ignoring the sign choice fixed by the angle condition.",
  "U11-A-dc-from-dr", "Normalise once and choose the sign.",
  check=_c5, values=[(Rational(-2, 3), Rational(1, 3), Rational(-2, 3)), (Rational(2, 3), Rational(-1, 3), Rational(2, 3)),
                     (Rational(-2, 5), Rational(1, 5), Rational(-2, 5)), (Rational(-2, 9), Rational(1, 9), Rational(-2, 9))],
  cognitive="Application", source_class=XII)


def _c6():
    g = Symbol('g')
    sols = solve(cos(pi/4)**2 + cos(pi/3)**2 + cos(g)**2 - 1, g)
    acute = [s for s in sols if 0 < s < pi/2]
    return acute[0] * 180 / pi
q("U11-A-006", TOP_DC, "Angles made with the axes", "Easy", "Single-step computation MCQ",
  r"A line makes angles of $45^\circ$ and $60^\circ$ with the positive $x$-axis and positive $y$-axis respectively, and an acute angle $\gamma$ with the positive $z$-axis. Then $\gamma$ equals",
  r"$60^\circ$",
  [(r"$30^\circ$", r"Finds $\cos^2\gamma = \frac{1}{4}$ correctly but then takes $\sin\gamma = \frac{1}{2}$."),
   (r"$75^\circ$", r"Assumes the three angles add up to $180^\circ$."),
   (r"$45^\circ$", r"Ignores the angle with the $y$-axis and uses $\cos^2\gamma = 1 - \cos^2 45^\circ = \frac{1}{2}$.")],
  r"$\cos^2 45^\circ + \cos^2 60^\circ + \cos^2\gamma = 1$ gives $\cos^2\gamma = 1 - \frac{1}{2} - \frac{1}{4} = \frac{1}{4}$. As $\gamma$ is acute, $\cos\gamma = \frac{1}{2}$ and $\gamma = 60^\circ$.",
  r"Treating the angles with the axes as summing to $180^\circ$ instead of using $l^2+m^2+n^2=1$.",
  "U11-A-axes-angles", r"One identity $l^2+m^2+n^2=1$ applied once.",
  check=_c6, values=[60, 30, 75, 45], cognitive="Application", source_class=XII,
  numerical=dict(question=r"A line makes angles of $45^\circ$ and $60^\circ$ with the positive $x$-axis and positive $y$-axis respectively, and an acute angle $\gamma$ with the positive $z$-axis. The value of $\gamma$ in degrees is", answer=60))


_OPT7 = [(Rational(2, 7), Rational(3, 7), Rational(6, 7)), (Rational(1, 2), Rational(1, 2), Rational(1, 2)),
         (Rational(1, 3), Rational(1, 3), Rational(1, 3)), (1/sqrt(2), 1/sqrt(2), Rational(1, 2))]


def _c7():
    ok = [t for t in _OPT7 if simplify(sum(x**2 for x in t) - 1) == 0]
    return ok[0] if len(ok) == 1 else None
q("U11-A-007", TOP_DC, "Condition for direction cosines", "Easy", "Direct concept MCQ",
  r"Which of the following triples can be the direction cosines of a line?",
  r"$\frac{2}{7}, \frac{3}{7}, \frac{6}{7}$",
  [(r"$\frac{1}{2}, \frac{1}{2}, \frac{1}{2}$", r"Equal values look like a line equally inclined to the axes, but $\frac{1}{4}\cdot 3 = \frac{3}{4} \ne 1$."),
   (r"$\frac{1}{3}, \frac{1}{3}, \frac{1}{3}$", r"Checks $l+m+n = 1$ instead of $l^2+m^2+n^2 = 1$."),
   (r"$\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, \frac{1}{2}$", r"Recalls the values for angles $45^\circ$ and $60^\circ$ without testing; squares add to $\frac{5}{4}$.")],
  r"Direction cosines must satisfy $l^2+m^2+n^2=1$. For $\frac{2}{7}, \frac{3}{7}, \frac{6}{7}$ the sum of squares is $\frac{4+9+36}{49} = 1$; the other triples give $\frac{3}{4}$, $\frac{1}{3}$ and $\frac{5}{4}$.",
  r"Using $l+m+n=1$ as the defining condition.",
  "U11-A-dc-validity", "Recall of one condition, checked on four triples.",
  check=_c7, values=_OPT7, cognitive="Recall", source_class=XII)


def _c8():
    return cosang(V(1, 2, 2), V(2, 2, -1))
q("U11-A-008", TOP_ANG, "Angle between lines from direction ratios", "Easy", "Single-step computation MCQ",
  r"The angle between two lines with direction ratios $1, 2, 2$ and $2, 2, -1$ is",
  r"$\cos^{-1}\left(\frac{4}{9}\right)$",
  [(r"$\cos^{-1}\left(\frac{8}{9}\right)$", r"Sign slip in the last product: uses $2+4+2 = 8$ for the dot product."),
   (r"$\cos^{-1}\left(\frac{2}{3}\right)$", r"Divides by $3 + 3 = 6$, the sum of the magnitudes, instead of their product $9$."),
   (r"$\cos^{-1}\left(\frac{4}{81}\right)$", r"Divides by the product of the squared magnitudes $9 \cdot 9$.")],
  r"$\cos\theta = \frac{|1\cdot 2 + 2\cdot 2 + 2\cdot(-1)|}{\sqrt{9}\,\sqrt{9}} = \frac{4}{9}$, so $\theta = \cos^{-1}\left(\frac{4}{9}\right)$.",
  "Using squared magnitudes or the sum of magnitudes in the denominator.",
  "U11-A-angle-dr-basic", "Single formula, one computation.",
  check=_c8, values=[Rational(4, 9), Rational(8, 9), Rational(2, 3), Rational(4, 81)],
  cognitive="Application", source_class=XII)


def _c9():
    k = Symbol('k')
    return solve(list((V(3, k, 7) - V(1, 2, 3)).cross(V(5, 8, 11) - V(1, 2, 3))), k)[k]
q("U11-A-009", TOP_PT, "Collinearity of three points", "Easy", "Inverse/parameter MCQ",
  r"If the points $P(1, 2, 3)$, $Q(3, k, 7)$ and $R(5, 8, 11)$ are collinear, then $k$ equals",
  r"$5$",
  [(r"$3$", r"Finds $k - 2 = 3$ but reports $3$ as the value of $k$."),
   (r"$8$", r"Equates $k - 2$ to $6$, the $y$-component of $\overrightarrow{PR}$, ignoring the factor $\frac{1}{2}$."),
   (r"$14$", r"Inverts the ratio and writes $k - 2 = 2\cdot 6 = 12$.")],
  r"$\overrightarrow{PQ} = (2, k-2, 4)$ and $\overrightarrow{PR} = (4, 6, 8)$ must be proportional. The ratio is $\frac{2}{4} = \frac{4}{8} = \frac{1}{2}$, so $k - 2 = 3$ and $k = 5$.",
  "Mishandling the proportionality constant between direction ratios.",
  "U11-A-collinear-param", "One proportionality condition.",
  check=_c9, values=[5, 3, 8, 14], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If the points $P(1, 2, 3)$, $Q(3, k, 7)$ and $R(5, 8, 11)$ are collinear, then the value of $k$ is", answer=5))


def _c10():
    P, Q = V(-2, 4, 7), V(3, -5, 8)
    lam = Symbol('lam')
    X = (lam*Q + P) / (lam + 1)
    return solve(X[0], lam)[0]
q("U11-A-010", TOP_PT, "Ratio of division by a coordinate plane", "Easy", "Single-step computation MCQ",
  r"The $yz$-plane divides the line segment joining $P(-2, 4, 7)$ and $Q(3, -5, 8)$ in the ratio",
  r"$2 : 3$ internally",
  [(r"$3 : 2$ internally", r"Sets up $\frac{3k-2}{k+1} = 0$ correctly but writes the ratio as $1 : k$, reversing it."),
   (r"$4 : 5$ internally", r"Puts the $y$-coordinate equal to zero, which is the $xz$-plane."),
   (r"$7 : 8$ externally", r"Puts the $z$-coordinate equal to zero, which is the $xy$-plane.")],
  r"Let the point be $\frac{kQ + P}{k+1}$. On the $yz$-plane, $x = 0$: $\frac{3k - 2}{k+1} = 0$, so $k = \frac{2}{3}$. The ratio is $2 : 3$, and it is internal since $k > 0$.",
  "Setting the wrong coordinate to zero for a given coordinate plane.",
  "U11-A-section-plane-ratio", "One coordinate condition with the section formula.",
  check=_c10, values=[Rational(2, 3), Rational(3, 2), Rational(4, 5), Rational(-7, 8)],
  cognitive="Application", source_class="XI")


def _c11():
    d = V(3, 1, 9) - V(1, -2, 3)
    return tup(d / d.norm())
q("U11-A-011", TOP_DC, "Direction cosines of a directed segment", "Easy", "Single-step computation MCQ",
  r"The direction cosines of the line segment directed from $P(1, -2, 3)$ to $Q(3, 1, 9)$ are",
  r"$\frac{2}{7}, \frac{3}{7}, \frac{6}{7}$",
  [(r"$-\frac{2}{7}, -\frac{3}{7}, -\frac{6}{7}$", r"Uses $P - Q$, the direction from $Q$ to $P$."),
   (r"$\frac{2}{11}, \frac{3}{11}, \frac{6}{11}$", r"Divides by the sum $2+3+6 = 11$ instead of $\sqrt{4+9+36}$."),
   (r"$\frac{2}{49}, \frac{3}{49}, \frac{6}{49}$", r"Divides by $49$, forgetting the square root.")],
  r"$\overrightarrow{PQ} = (2, 3, 6)$ with length $\sqrt{4+9+36} = 7$, so the direction cosines are $\frac{2}{7}, \frac{3}{7}, \frac{6}{7}$.",
  "Reversing the direction or normalising incorrectly.",
  "U11-A-dc-two-points", "Subtract and normalise once.",
  check=_c11, values=[(Rational(2, 7), Rational(3, 7), Rational(6, 7)), (Rational(-2, 7), Rational(-3, 7), Rational(-6, 7)),
                      (Rational(2, 11), Rational(3, 11), Rational(6, 11)), (Rational(2, 49), Rational(3, 49), Rational(6, 49))],
  cognitive="Application", source_class=XII)


def _c12():
    a = Symbol('a', positive=True)
    return solve(dist(Matrix([a, 2, -1]), V(1, -1, 1)) - 7, a)[0]
q("U11-A-012", TOP_PT, "Unknown coordinate from a distance", "Easy", "Inverse/parameter MCQ",
  r"If the distance between $P(a, 2, -1)$ and $Q(1, -1, 1)$ is $7$ and $a > 0$, then $a$ equals",
  r"$7$",
  [(r"$8$", r"Forgets to subtract $3^2 + 2^2$ and solves $(a-1)^2 = 49$."),
   (r"$6$", r"Solves $a - 1 = 6$ but reports $6$ as $a$."),
   (r"$5$", r"Takes the root $a - 1 = -6$, gets $a = -5$, then drops the sign to satisfy $a > 0$.")],
  r"$(a-1)^2 + 3^2 + (-2)^2 = 49$, so $(a-1)^2 = 36$ and $a = 7$ or $a = -5$. With $a > 0$, $a = 7$.",
  "Not subtracting the known squared differences before taking the root.",
  "U11-A-distance-param", "One equation from the distance formula, one sign choice.",
  check=_c12, values=[7, 8, 6, 5], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If the distance between $P(a, 2, -1)$ and $Q(1, -1, 1)$ is $7$ and $a > 0$, then the value of $a$ is", answer=7))


def _c13():
    P, M = V(5, 2, -1), V(2, -1, 3)
    x, y, z = symbols('x y z')
    s = solve(list((P + Matrix([x, y, z])) / 2 - M), [x, y, z], dict=True)[0]
    return (s[x], s[y], s[z])
q("U11-A-013", TOP_PT, "Midpoint (reverse)", "Easy", "Single-step computation MCQ",
  r"If $M(2, -1, 3)$ is the midpoint of the segment $PQ$ where $P$ is $(5, 2, -1)$, then $Q$ is",
  r"$(-1, -4, 7)$",
  [(r"$(\frac{7}{2}, \frac{1}{2}, 1)$", r"Takes the midpoint of $P$ and $M$."),
   (r"$(3, 3, -4)$", r"Computes $P - M$."),
   (r"$(8, 5, -5)$", r"Computes $2P - M$, the point for which $P$ is the midpoint.")],
  r"From $M = \frac{P+Q}{2}$, $Q = 2M - P = (4-5, -2-2, 6+1) = (-1, -4, 7)$.",
  "Interchanging the roles of the midpoint and the endpoint.",
  "U11-A-midpoint-reverse", "Single rearrangement of the midpoint formula.",
  check=_c13, values=[(-1, -4, 7), (Rational(7, 2), Rational(1, 2), 1), (3, 3, -4), (8, 5, -5)],
  cognitive="Application", source_class="XI")


def _c14():
    s1 = collinear(V(1, 2, 3), V(2, 3, 4), V(4, 5, 6))
    s2 = collinear(V(1, -1, 2), V(2, 1, 3), V(4, 5, 6))
    return (bool(s1), bool(s2))
q("U11-A-014", TOP_PT, "Collinearity of three points", "Easy", "Statement-based MCQ",
  r"Statement I: The points $(1, 2, 3)$, $(2, 3, 4)$ and $(4, 5, 6)$ are collinear. Statement II: The points $(1, -1, 2)$, $(2, 1, 3)$ and $(4, 5, 6)$ are collinear." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Checks only the $x$- and $y$-differences in Statement II, $(1, 2)$ and $(3, 6)$, which are proportional, and ignores $z$."),
   (ST_FF, r"Compares the position vectors $(1,2,3)$ and $(4,5,6)$ instead of the difference vectors in Statement I."),
   (ST_FT, r"Combines both errors: compares position vectors in Statement I and ignores $z$ in Statement II.")],
  r"Statement I: the differences from the first point are $(1, 1, 1)$ and $(3, 3, 3)$, which are proportional, so the points are collinear. Statement II: the differences are $(1, 2, 1)$ and $(3, 6, 4)$; since $\frac{4}{1} \ne 3$, they are not proportional, so the points are not collinear.",
  "Checking proportionality on only some of the components.",
  "U11-A-st-collinear", "Two direct proportionality checks.",
  check=_c14, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Understanding", source_class="XI")


# ================================================================ MEDIUM

def _c15():
    l, m = symbols('l m', real=True)
    n2 = 1 - l**2 - m**2                       # n^2 from l^2+m^2+n^2=1
    s1 = simplify((1 - l**2) + (1 - m**2) + (1 - n2) - 2) == 0
    s2 = simplify((2*l**2 - 1) + (2*m**2 - 1) + (2*n2 - 1) + 1) == 0
    return (bool(s1), bool(s2))
q("U11-A-015", TOP_DC, "Identities for direction angles", "Medium", "Statement-based MCQ",
  r"A line makes angles $\alpha, \beta, \gamma$ with the positive coordinate axes. Statement I: $\sin^2\alpha + \sin^2\beta + \sin^2\gamma = 2$. Statement II: $\cos 2\alpha + \cos 2\beta + \cos 2\gamma = -1$." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Writes $\cos 2\alpha = 1 - 2\cos^2\alpha$, giving a sum of $3 - 2 = 1$, and so rejects Statement II."),
   (ST_FT, r"Carries over $\cos^2$ sum $= 1$ to the sines and expects $\sin^2\alpha + \sin^2\beta + \sin^2\gamma = 1$."),
   (ST_FF, r"Makes both slips: expects the sines to sum to $1$ and uses $\cos 2\alpha = 1 - 2\cos^2\alpha$.")],
  r"With $\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1$: $\sum \sin^2\alpha = 3 - 1 = 2$, and $\sum \cos 2\alpha = \sum (2\cos^2\alpha - 1) = 2 - 3 = -1$. Both statements are true.",
  r"Assuming the sine squares also add to $1$, or misremembering the double-angle formula.",
  "U11-A-st-axes-identity", "Two identities, each derived from $l^2+m^2+n^2=1$.",
  check=_c15, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Understanding", source_class=XII)


def _c16():
    c, cz = symbols('c cz', positive=True)   # c = cos^2(theta), cz = cos^2(phi)
    s = solve([2*c + cz - 1, (1 - c) - 3*(1 - cz)], [c, cz], dict=True)[0]
    return s[c]
q("U11-A-016", TOP_DC, "Angles with the axes under a condition", "Medium", "Multi-step computation MCQ",
  r"A line makes an angle $\theta$ with each of the positive $x$- and $y$-axes and an angle $\phi$ with the positive $z$-axis. If $\sin^2\theta = 3\sin^2\phi$, then $\cos^2\theta$ equals",
  r"$\frac{1}{7}$",
  [(r"$\frac{1}{4}$", r"Writes $\cos^2\theta + \cos^2\phi = 1$, counting $\theta$ only once; then $1 - c = 3c$."),
   (r"$\frac{4}{7}$", r"Uses $2\sin^2\theta + \sin^2\phi = 1$; then $\sin^2\phi = \frac{1}{7}$, $\sin^2\theta = \frac{3}{7}$ and $\cos^2\theta = \frac{4}{7}$."),
   (r"$\frac{6}{7}$", r"Solves correctly but reports $\sin^2\theta = 1 - \frac{1}{7}$.")],
  r"$2\cos^2\theta + \cos^2\phi = 1$ gives $\sin^2\phi = 1 - \cos^2\phi = 2\cos^2\theta$. Then $1 - \cos^2\theta = 3 \cdot 2\cos^2\theta$, so $7\cos^2\theta = 1$ and $\cos^2\theta = \frac{1}{7}$.",
  r"Counting the repeated angle once in $l^2+m^2+n^2 = 1$.",
  "U11-A-axes-angle-relation", "Two relations combined; the repeated angle must be counted twice.",
  check=_c16, values=[Rational(1, 7), Rational(1, 4), Rational(4, 7), Rational(6, 7)],
  cognitive="Application", source_class=XII)


def _c17():
    return dirn(V(1, 2, 3).cross(V(2, -1, 1)))
q("U11-A-017", TOP_DC, "Direction ratios of a line perpendicular to two lines", "Medium", "Single-step computation MCQ",
  r"Direction ratios of a line perpendicular to both the lines with direction ratios $1, 2, 3$ and $2, -1, 1$ are proportional to",
  r"$1, 1, -1$",
  [(r"$1, -1, -1$", r"Sign slip in the middle component of the cross product: uses $1\cdot 1 - 3\cdot 2$ for $n_1 l_2 - l_1 n_2$."),
   (r"$3, 1, 4$", r"Adds the direction ratios componentwise."),
   (r"$2, -2, 3$", r"Multiplies the direction ratios componentwise.")],
  r"Solve $a + 2b + 3c = 0$ and $2a - b + c = 0$: the solution is proportional to $(2\cdot 1 - 3\cdot(-1),\ 3\cdot 2 - 1\cdot 1,\ 1\cdot(-1) - 2\cdot 2) = (5, 5, -5)$, that is, to $1, 1, -1$. Check: $1 + 2 - 3 = 0$ and $2 - 1 - 1 = 0$.",
  "Sign errors in the middle component of the cross product.",
  "U11-A-perp-dr-cross", "Two perpendicularity conditions solved together.",
  check=_c17, values=[dirn((1, 1, -1)), dirn((1, -1, -1)), dirn((3, 1, 4)), dirn((2, -2, 3))],
  cognitive="Application", source_class=XII)


def _c18():
    k = Symbol('k')
    return sum(solve(Matrix([k, 2, -3]).dot(Matrix([2*k, k, 4])), k))
q("U11-A-018", TOP_ANG, "Perpendicular lines (parameter)", "Medium", "Inverse/parameter MCQ",
  r"The lines with direction ratios $k, 2, -3$ and $2k, k, 4$ are perpendicular. The sum of all possible values of $k$ is",
  r"$-1$",
  [(r"$1$", r"Takes the sum of roots of $k^2 + k - 6 = 0$ as $+\frac{b}{a}$."),
   (r"$-6$", r"Reports the product of the roots."),
   (r"$6$", r"Reports the product of the roots with the sign changed.")],
  r"$k\cdot 2k + 2\cdot k + (-3)\cdot 4 = 0$ gives $2k^2 + 2k - 12 = 0$, that is, $k^2 + k - 6 = 0$, so $k = 2$ or $k = -3$. The sum is $-1$.",
  r"Sign error in the sum of roots $-\frac{b}{a}$.",
  "U11-A-perp-param", "Perpendicularity condition leads to a quadratic; then Vieta.",
  check=_c18, values=[-1, 1, -6, 6], cognitive="Application", source_class=XII,
  numerical=None)


def _c19():
    a, b = symbols('a b')
    s = solve(list(Matrix([2, a, 3]).cross(Matrix([b, -2, 6]))), [a, b], dict=True)[0]
    return s[a] + s[b]
q("U11-A-019", TOP_ANG, "Parallel lines (parameters)", "Medium", "Inverse/parameter MCQ",
  r"If the lines with direction ratios $2, a, 3$ and $b, -2, 6$ are parallel, then $a + b$ equals",
  r"$3$",
  [(r"$-3$", r"Inverts the common ratio, using $2$ instead of $\frac{1}{2}$: $b = 1$, $a = -4$."),
   (r"$0$", r"Gets $b = 4$ correctly but inverts the ratio for $a$: $\frac{a}{-2} = 2$, so $a = -4$."),
   (r"$5$", r"Solves $\frac{a}{-2} = \frac{1}{2}$ as $a = 1$, dropping the sign.")],
  r"Parallel lines have proportional direction ratios: $\frac{2}{b} = \frac{a}{-2} = \frac{3}{6} = \frac{1}{2}$. So $b = 4$ and $a = -1$, and $a + b = 3$.",
  "Inverting the ratio between the two sets of direction ratios.",
  "U11-A-parallel-param", "Two unknowns from one proportionality chain.",
  check=_c19, values=[3, -3, 0, 5], cognitive="Application", source_class=XII,
  numerical=dict(question=r"If the lines with direction ratios $2, a, 3$ and $b, -2, 6$ are parallel, then the value of $a + b$ is", answer=3))


def _c20():
    P, Q, R = V(1, 0, 2), V(3, 2, 3), V(3, -1, 0)
    s = sorted([dist(P, Q)**2, dist(Q, R)**2, dist(R, P)**2])
    right = s[0] + s[1] == s[2]
    iso = len(set(s)) < 3
    equi = len(set(s)) == 1
    return (bool(right), bool(iso), bool(equi))
q("U11-A-020", TOP_PT, "Nature of a triangle from distances", "Medium", "Multi-step computation MCQ",
  r"The triangle with vertices $P(1, 0, 2)$, $Q(3, 2, 3)$ and $R(3, -1, 0)$ is",
  r"right-angled and isosceles",
  [(r"equilateral", r"Drops the $z$-difference in $QR^2$, getting $0 + 9 + 0 = 9$, so all three sides appear equal to $3$."),
   (r"isosceles but not right-angled", r"Finds $PQ = PR$ but tests Pythagoras with $QR$ as a leg instead of the hypotenuse, so no right angle appears."),
   (r"right-angled but not isosceles", r"Detects the right angle at $P$ but miscounts $PR^2$ as $4 + 1 + 2$, so $PQ \ne PR$.")],
  r"$PQ^2 = 4 + 4 + 1 = 9$, $PR^2 = 4 + 1 + 4 = 9$, $QR^2 = 0 + 9 + 9 = 18$. So $PQ = PR$ and $PQ^2 + PR^2 = QR^2$: the triangle is right-angled at $P$ and isosceles.",
  "Stopping after two sides, or not testing Pythagoras.",
  "U11-A-triangle-type", "Three distances and two tests combined.",
  check=_c20, values=[(True, True, False), (False, True, True), (False, True, False), (True, False, False)],
  cognitive="Analysis", source_class="XI")


def _c21():
    P, Q, R = V(1, 2, 3), V(2, 3, 1), V(3, 1, 2)
    return simplify((Q - P).cross(R - P).norm() / 2)
q("U11-A-021", TOP_PT, "Area of an equilateral triangle in space", "Medium", "Multi-step computation MCQ",
  r"The area of the triangle with vertices $P(1, 2, 3)$, $Q(2, 3, 1)$ and $R(3, 1, 2)$ is",
  r"$\frac{3\sqrt{3}}{2}$",
  [(r"$3\sqrt{3}$", r"Uses $\frac{\sqrt{3}}{2}a^2$ instead of $\frac{\sqrt{3}}{4}a^2$."),
   (r"$\frac{3\sqrt{2}}{4}$", r"Uses $\frac{\sqrt{3}}{4}a$ with the side not squared: $\frac{\sqrt{3}}{4}\sqrt{6}$."),
   (r"$3$", r"Treats the angle at $Q$ as a right angle and computes $\frac{1}{2}PQ\cdot QR = \frac{1}{2}\cdot 6$.")],
  r"$PQ^2 = 1+1+4 = 6$, $QR^2 = 1+4+1 = 6$, $RP^2 = 4+1+1 = 6$, so the triangle is equilateral with side $\sqrt{6}$. Area $= \frac{\sqrt{3}}{4}\cdot 6 = \frac{3\sqrt{3}}{2}$.",
  r"Using the wrong constant in the equilateral area formula.",
  "U11-A-equilateral-area", "Recognise equilateral from three distances, then apply the area formula.",
  check=_c21, values=[3*sqrt(3)/2, 3*sqrt(3), 3*sqrt(2)/4, 3], cognitive="Application", source_class="XI")


def _c22():
    a = Symbol('a', positive=True)
    d1 = Matrix([a, a, a]) - Matrix([0, 0, 0])
    d2 = Matrix([0, a, a]) - Matrix([a, 0, 0])
    return Abs(cosang(d1, d2))
q("U11-A-022", TOP_ANG, "Angle between diagonals of a cube", "Medium", "Conceptual/application MCQ",
  r"The acute angle between any two body diagonals of a cube is",
  r"$\cos^{-1}\left(\frac{1}{3}\right)$",
  [(r"$\cos^{-1}\left(\frac{1}{\sqrt{3}}\right)$", r"Computes the angle between a body diagonal and an edge."),
   (r"$\cos^{-1}\left(\sqrt{\frac{2}{3}}\right)$", r"Computes the angle between a body diagonal and a face diagonal through the same vertex."),
   (r"$\frac{\pi}{3}$", r"Computes the angle between two face diagonals meeting at a vertex.")],
  r"Take the cube with edges along the axes and edge $a$. Two body diagonals have direction ratios $1, 1, 1$ and $-1, 1, 1$. Then $\cos\theta = \frac{|-1 + 1 + 1|}{\sqrt{3}\sqrt{3}} = \frac{1}{3}$.",
  "Mixing up body diagonals, face diagonals and edges.",
  "U11-A-cube-diagonals", "Set up coordinates for a cube, then one angle computation.",
  check=_c22, values=[Rational(1, 3), 1/sqrt(3), sqrt(Rational(2, 3)), Rational(1, 2)],
  cognitive="Application", source_class=XII)


def _c23():
    proj = V(4, -3, 12)
    d = V(3, -2, 3) - V(1, 0, 2)
    return proj.dot(d) / d.norm()
q("U11-A-023", TOP_DC, "Projection of a segment on a line", "Medium", "Multi-step computation MCQ",
  r"The projections of a line segment on the $x$-, $y$- and $z$-axes are $4$, $-3$ and $12$ respectively. The projection of this segment on the line joining $R(1, 0, 2)$ to $S(3, -2, 3)$ is",
  r"$\frac{26}{3}$",
  [(r"$26$", r"Uses the direction ratios $2, -2, 1$ without dividing by their magnitude $3$."),
   (r"$\frac{14}{3}$", r"Sign slip: takes $(-3)(-2)$ as $-6$, giving $\frac{8 - 6 + 12}{3}$."),
   (r"$\frac{26}{9}$", r"Divides by $9$, the square of the magnitude.")],
  r"The segment is the vector $(4, -3, 12)$. The line $RS$ has direction ratios $2, -2, 1$ and direction cosines $\frac{2}{3}, -\frac{2}{3}, \frac{1}{3}$. Projection $= 4\cdot\frac{2}{3} + (-3)\left(-\frac{2}{3}\right) + 12\cdot\frac{1}{3} = \frac{8 + 6 + 12}{3} = \frac{26}{3}$.",
  "Using direction ratios instead of direction cosines in the projection formula.",
  "U11-A-projection", "Find direction cosines from two points, then project.",
  check=_c23, values=[Rational(26, 3), 26, Rational(14, 3), Rational(26, 9)], cognitive="Application", source_class=XII)


def _c24():
    x = Symbol('x')
    return solve(dist(Matrix([x, 0, 0]), V(1, 2, 3))**2 - dist(Matrix([x, 0, 0]), V(3, 5, -2))**2, x)[0]
q("U11-A-024", TOP_PT, "Point on an axis equidistant from two points", "Medium", "Inverse/parameter MCQ",
  r"The point on the $x$-axis that is equidistant from $P(1, 2, 3)$ and $Q(3, 5, -2)$ has $x$-coordinate",
  r"$6$",
  [(r"$2$", r"Ignores the $y$- and $z$-coordinates, so the condition reduces to the midpoint of the $x$-coordinates."),
   (r"$-6$", r"Sign slip when transposing: writes $-4x = 24$."),
   (r"$1$", r"Forgets to square the $y$-coordinate of $Q$, using $5$ in place of $25$.")],
  r"For $X(x, 0, 0)$: $(x-1)^2 + 4 + 9 = (x-3)^2 + 25 + 4$, so $-2x + 14 = -6x + 38$, giving $4x = 24$ and $x = 6$.",
  "Treating the equidistance condition as if the point lay on the segment.",
  "U11-A-equidistant-axis", "Set up the distance equality and solve the linear equation.",
  check=_c24, values=[6, 2, -6, 1], cognitive="Application", source_class="XI",
  numerical=dict(question=r"The point on the $x$-axis that is equidistant from $P(1, 2, 3)$ and $Q(3, 5, -2)$ has $x$-coordinate", answer=6))


def _c25():
    U, W = V(-1, 4, 2), V(4, -1, 7)
    m, n = 2, 3
    I_ = (m*W + n*U) / (m + n)
    E_ = (m*W - n*U) / (m - n)
    return simplify((I_ - E_).norm())
q("U11-A-025", TOP_PT, "Internal and external division", "Medium", "Multi-step computation MCQ",
  r"The points $X$ and $Y$ divide the segment joining $U(-1, 4, 2)$ and $W(4, -1, 7)$ internally and externally, respectively, in the ratio $2 : 3$ (that is, $UX : XW = UY : YW = 2 : 3$). Then $XY$ equals",
  r"$12\sqrt{3}$",
  [(r"$13\sqrt{3}$", r"Reverses the weights in only the external formula, using $\frac{2U - 3W}{2-3}$, which gives $Y = (14, -11, 17)$."),
   (r"$2\sqrt{93}$", r"Forgets to divide by $m - n = -1$ in the external formula, so $Y = (11, -14, 8)$."),
   (r"$\frac{6\sqrt{21}}{5}$", r"Uses $m + n$ in the denominator of the external formula, so $Y = (\frac{11}{5}, -\frac{14}{5}, \frac{8}{5})$.")],
  r"$X = \frac{2W + 3U}{5} = (1, 2, 4)$ and $Y = \frac{2W - 3U}{2 - 3} = (-11, 14, -8)$. Then $X - Y = (12, -12, 12)$ and $XY = 12\sqrt{3}$.",
  "Misplacing the denominator or the signs in the external section formula.",
  "U11-A-section-int-ext", "Two section formulas then a distance.",
  check=_c25, values=[12*sqrt(3), 13*sqrt(3), 2*sqrt(93), 6*sqrt(21)/5], cognitive="Application", source_class="XI")


def _c26():
    K, L, Mm = V(1, 2, -3), V(3, 0, 1), V(-1, 1, -4)
    p = symbols('p1:4'); qq = symbols('q1:4'); r = symbols('r1:4')
    P, Q, R = Matrix(p), Matrix(qq), Matrix(r)
    eqs = list((Q + R) / 2 - K) + list((R + P) / 2 - L) + list((P + Q) / 2 - Mm)
    s = solve(eqs, list(p) + list(qq) + list(r), dict=True)[0]
    return tuple(s[x] for x in p)
q("U11-A-026", TOP_PT, "Vertex from midpoints of sides", "Medium", "Multi-step computation MCQ",
  r"In triangle $PQR$, the midpoints of $QR$, $RP$ and $PQ$ are $K(1, 2, -3)$, $L(3, 0, 1)$ and $M(-1, 1, -4)$ respectively. The vertex $P$ is",
  r"$(1, -1, 0)$",
  [(r"$(5, 1, 2)$", r"Computes $K + L - M$, which is the vertex $R$."),
   (r"$(-3, 3, -8)$", r"Computes $K + M - L$, which is the vertex $Q$."),
   (r"$(1, \frac{1}{2}, -\frac{3}{2})$", r"Takes the midpoint of $L$ and $M$ as the vertex between them.")],
  r"$L + M = \frac{R + P}{2} + \frac{P + Q}{2} = P + \frac{Q + R}{2} = P + K$. So $P = L + M - K = (3 - 1 - 1,\ 0 + 1 - 2,\ 1 - 4 + 3) = (1, -1, 0)$.",
  "Pairing the wrong midpoints with the vertex.",
  "U11-A-midpoints-vertex", "Combine three midpoint relations correctly.",
  check=_c26, values=[(1, -1, 0), (5, 1, 2), (-3, 3, -8), (1, Rational(1, 2), Rational(-3, 2))],
  cognitive="Application", source_class="XI")


def _c27():
    P, Q, R = V(1, -2, 3), V(2, 1, -1), V(4, 0, 2)
    x, y, z = symbols('x y z')
    S = Matrix([x, y, z])
    s = solve(list((P + R) / 2 - (Q + S) / 2), [x, y, z], dict=True)[0]
    return (s[x], s[y], s[z])
q("U11-A-027", TOP_PT, "Fourth vertex of a parallelogram", "Medium", "Single-step computation MCQ",
  r"$P(1, -2, 3)$, $Q(2, 1, -1)$ and $R(4, 0, 2)$ are three consecutive vertices of a parallelogram $PQRS$. The vertex $S$ is",
  r"$(3, -3, 6)$",
  [(r"$(5, 3, -2)$", r"Takes $QR$ as a diagonal, computing $Q + R - P$."),
   (r"$(-1, -1, 0)$", r"Takes $PQ$ as a diagonal, computing $P + Q - R$."),
   (r"$(\frac{5}{2}, -1, \frac{5}{2})$", r"Takes the midpoint of the diagonal $PR$ as $S$.")],
  r"The diagonals $PR$ and $QS$ bisect each other, so $S = P + R - Q = (1 + 4 - 2,\ -2 + 0 - 1,\ 3 + 2 + 1) = (3, -3, 6)$.",
  "Using the wrong pair of opposite vertices.",
  "U11-A-parallelogram-vertex", "Midpoints of diagonals coincide; one rearrangement, with an order trap.",
  check=_c27, values=[(3, -3, 6), (5, 3, -2), (-1, -1, 0), (Rational(5, 2), -1, Rational(5, 2))],
  cognitive="Application", source_class="XI")


def _c28():
    s1 = simplify(cos(pi/6)**2 + cos(pi/4)**2 + cos(pi/3)**2 - 1) == 0
    s2 = simplify(cos(pi/4)**2 + cos(pi/4)**2 + cos(pi/2)**2 - 1) == 0
    return (bool(s1), bool(s2))
q("U11-A-028", TOP_DC, "Existence of direction angles", "Medium", "Statement-based MCQ",
  r"Statement I: There is a line that makes angles $30^\circ$, $45^\circ$ and $60^\circ$ with the positive $x$-, $y$- and $z$-axes respectively. Statement II: There is a line that makes angles $45^\circ$, $45^\circ$ and $90^\circ$ with the positive $x$-, $y$- and $z$-axes respectively." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Accepts any three angles between $0^\circ$ and $180^\circ$ without testing $l^2 + m^2 + n^2 = 1$."),
   (ST_TF, r"Does not test $l^2 + m^2 + n^2 = 1$ and instead requires every direction angle to lie strictly between $0^\circ$ and $90^\circ$: accepts Statement I, whose angles $30^\circ$, $45^\circ$, $60^\circ$ all qualify, and rejects Statement II because of its $90^\circ$ angle."),
   (ST_FF, r"Tests $l + m + n = 1$ instead of the sum of squares: Statement I gives $\frac{\sqrt{3}}{2} + \frac{1}{\sqrt{2}} + \frac{1}{2} \ne 1$ and Statement II gives $\frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} + 0 = \sqrt{2} \ne 1$, so both are rejected.")],
  r"Statement I: $\cos^2 30^\circ + \cos^2 45^\circ + \cos^2 60^\circ = \frac{3}{4} + \frac{1}{2} + \frac{1}{4} = \frac{3}{2} \ne 1$, so no such line. Statement II: $\frac{1}{2} + \frac{1}{2} + 0 = 1$, so such a line exists (it lies in the $xy$-plane).",
  r"Not testing $\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1$.",
  "U11-A-st-angle-existence", "Test the identity on two triples.",
  check=_c28, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Understanding", source_class=XII)


def _c29():
    P, Q, R = V(1, 2, -1), V(3, 0, 3), V(0, 3, -3)
    assert collinear(P, Q, R)
    lam = Symbol('lam')
    s = solve(list((lam*R + Q) / (lam + 1) - P), lam)
    return s[lam] if isinstance(s, dict) else s[0]
q("U11-A-029", TOP_PT, "Ratio of division for collinear points", "Medium", "Multi-step computation MCQ",
  r"The points $P(1, 2, -1)$, $Q(3, 0, 3)$ and $R(0, 3, -3)$ are collinear. The point $P$ divides $QR$ in the ratio",
  r"$2 : 1$ internally",
  [(r"$1 : 2$ internally", r"Measures from $R$ instead of $Q$, giving $RP : PQ$."),
   (r"$2 : 1$ externally", r"Gets the magnitude $2 : 1$ but fails to see that $P$ lies between $Q$ and $R$."),
   (r"$3 : 1$ internally", r"Compares $QR$ with $PR$ instead of $QP$ with $PR$.")],
  r"Let $P = \frac{\lambda R + Q}{\lambda + 1}$. The $x$-coordinate gives $\frac{0\cdot\lambda + 3}{\lambda + 1} = 1$, so $\lambda = 2$; the $y$- and $z$-coordinates agree ($\frac{3\lambda}{\lambda+1} = 2$, $\frac{-3\lambda + 3}{\lambda + 1} = -1$). Since $\lambda > 0$, $QP : PR = 2 : 1$ internally.",
  "Measuring the ratio from the wrong endpoint.",
  "U11-A-collinear-ratio", "Section formula solved for the ratio, then consistency check and interpretation.",
  check=_c29, values=[2, Rational(1, 2), -2, 3], cognitive="Application", source_class="XI",
  numerical=dict(question=r"The points $P(1, 2, -1)$, $Q(3, 0, 3)$ and $R(0, 3, -3)$ are collinear. If $P$ divides $QR$ internally in the ratio $\lambda : 1$ (that is, $QP : PR = \lambda : 1$), then $\lambda$ is", answer=2))


def _c30():
    return cosang(V(4, 1, 4) - V(3, -1, 2), V(4, 2, 4) - V(0, 2, 1))
q("U11-A-030", TOP_ANG, "Angle between lines through given points", "Medium", "Multi-step computation MCQ",
  r"The angle between the line through $P(3, -1, 2)$ and $Q(4, 1, 4)$ and the line through $R(0, 2, 1)$ and $S(4, 2, 4)$ is",
  r"$\cos^{-1}\left(\frac{2}{3}\right)$",
  [(r"$\cos^{-1}\left(\frac{2}{15}\right)$", r"Sign slip in the $z$-product: uses $4 + 0 - 6 = -2$."),
   (r"$\cos^{-1}\left(\frac{2}{45}\right)$", r"Divides $10$ by $9 \cdot 25$, the product of squared lengths."),
   (r"$\cos^{-1}\left(\frac{2}{9}\right)$", r"Divides $10$ by $9 \cdot 5$, squaring only the length of $\overrightarrow{PQ}$.")],
  r"$\overrightarrow{PQ} = (1, 2, 2)$ with length $3$, and $\overrightarrow{RS} = (4, 0, 3)$ with length $5$. Then $\cos\theta = \frac{4 + 0 + 6}{3\cdot 5} = \frac{2}{3}$.",
  "Errors in the denominator of the cosine formula.",
  "U11-A-angle-two-segments", "Find two sets of direction ratios, then the angle.",
  check=_c30, values=[Rational(2, 3), Rational(2, 15), Rational(2, 45), Rational(2, 9)], cognitive="Application", source_class=XII)


def _c31():
    g = Symbol('g')
    c3 = [s for s in solve(cos(pi/3)**2 + cos(pi/4)**2 + g**2 - 1, g) if s > 0][0]
    u = Matrix([cos(pi/3), cos(pi/4), c3])
    return tup(12 * u)
q("U11-A-031", TOP_DC, "Coordinates from distance and direction cosines", "Medium", "Multi-step computation MCQ",
  r"A point $P$ in the first octant is at distance $12$ from the origin $O$. The segment $OP$ makes angles of $60^\circ$ and $45^\circ$ with the positive $x$-axis and positive $y$-axis respectively. Then $P$ is",
  r"$(6, 6\sqrt{2}, 6)$",
  [(r"$(6\sqrt{2}, 6, 6)$", r"Swaps $\cos 60^\circ$ and $\cos 45^\circ$ between the $x$- and $y$-coordinates."),
   (r"$(12, 12\sqrt{2}, 12)$", r"Multiplies the direction ratios $1, \sqrt{2}, 1$ by $12$ without normalising them (their magnitude is $2$)."),
   (r"$(6, 6\sqrt{2}, 6\sqrt{3})$", r"Finds $\cos^2\gamma = \frac{1}{4}$ but then writes $\cos\gamma = \sqrt{1 - \frac{1}{4}} = \frac{\sqrt{3}}{2}$.")],
  r"$\cos^2\gamma = 1 - \frac{1}{4} - \frac{1}{2} = \frac{1}{4}$, and $\cos\gamma = \frac{1}{2}$ because $P$ is in the first octant. So $P = 12\left(\frac{1}{2}, \frac{1}{\sqrt{2}}, \frac{1}{2}\right) = (6, 6\sqrt{2}, 6)$.",
  "Using direction ratios where direction cosines are needed.",
  "U11-A-point-from-dc", "Third direction cosine from the identity, then scale by the distance.",
  check=_c31, values=[(6, 6*sqrt(2), 6), (6*sqrt(2), 6, 6), (12, 12*sqrt(2), 12), (6, 6*sqrt(2), 6*sqrt(3))],
  cognitive="Application", source_class=XII)


def _c32():
    th, ph = symbols('th ph', real=True)
    f = cos(th)*sin(ph) + sin(th)*sin(ph) + cos(ph)   # l + m + n on the unit sphere
    crit = solve([diff(f, th), diff(f, ph)], [th, ph], dict=True)
    return Max(*[simplify(f.subs(c)) for c in crit])
q("U11-A-032", TOP_DC, "Extreme value involving direction cosines", "Medium", "Conceptual/application MCQ",
  r"If $l, m, n$ are the direction cosines of a line, then the greatest possible value of $l + m + n$ is",
  r"$\sqrt{3}$",
  [(r"$1$", r"Confuses the condition and assumes $l + m + n = 1$ always."),
   (r"$3$", r"Bounds each direction cosine by $1$ separately, ignoring $l^2 + m^2 + n^2 = 1$."),
   (r"$\sqrt{2}$", r"Tests only a line equally inclined to two axes and perpendicular to the third, $\left(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0\right)$.")],
  r"By the Cauchy-Schwarz inequality, $(l + m + n)^2 \le 3(l^2 + m^2 + n^2) = 3$, so $l + m + n \le \sqrt{3}$, with equality for $l = m = n = \frac{1}{\sqrt{3}}$.",
  "Treating each direction cosine as independently able to equal 1.",
  "U11-A-dc-extremum", "Combine the identity with an inequality.",
  check=_c32, values=[sqrt(3), 1, 3, sqrt(2)], cognitive="Analysis", source_class=XII)


def _c33():
    P, Q, R = V(3, -1, 2), V(1, 2, -4), V(-1, 4, 2)
    return dist(P, (Q + R) / 2)
q("U11-A-033", TOP_PT, "Length of a median", "Medium", "Multi-step computation MCQ",
  r"The length of the median through $P$ of the triangle with vertices $P(3, -1, 2)$, $Q(1, 2, -4)$ and $R(-1, 4, 2)$ is",
  r"$\sqrt{34}$",
  [(r"$\sqrt{29}$", r"Uses $\frac{Q - R}{2} = (1, -1, -3)$ as the midpoint of $QR$."),
   (r"$\frac{2\sqrt{34}}{3}$", r"Finds the distance from $P$ to the centroid, which is two-thirds of the median."),
   (r"$\sqrt{74}$", r"Forgets to halve $Q + R$, using $(0, 6, -2)$ as the midpoint.")],
  r"The midpoint of $QR$ is $(0, 3, -1)$. The median length is $\sqrt{(3-0)^2 + (-1-3)^2 + (2+1)^2} = \sqrt{9 + 16 + 9} = \sqrt{34}$.",
  "Confusing the median with the vertex-to-centroid distance.",
  "U11-A-median-length", "Midpoint then distance.",
  check=_c33, values=[sqrt(34), sqrt(29), 2*sqrt(34)/3, sqrt(74)], cognitive="Application", source_class="XI")


def _c34():
    k = Symbol('k')
    P, Q, R = Matrix([k, 2, 1]), V(1, 0, 3), V(3, 1, 2)
    kv = solve((P - Q).dot(R - Q), k)[0]
    P = P.subs(k, kv)
    return simplify((P - Q).cross(R - Q).norm() / 2)
q("U11-A-034", TOP_ANG, "Right angle condition and area", "Medium", "Multi-step computation MCQ",
  r"The triangle with vertices $P(k, 2, 1)$, $Q(1, 0, 3)$ and $R(3, 1, 2)$ has a right angle at $Q$. Its area is",
  r"$3\sqrt{2}$",
  [(r"$6\sqrt{2}$", r"Finds $k = -1$ correctly but uses $QP \cdot QR$ without the factor $\frac{1}{2}$."),
   (r"$2\sqrt{3}$", r"Sign slip gives $k = 1$, so $QP = 2\sqrt{2}$, and then uses $\frac{1}{2}QP\cdot QR$."),
   (r"$3\sqrt{6}$", r"Uses the hypotenuse $PR = 3\sqrt{2}$ with $QP$ as the two legs: $\frac{1}{2}\cdot 2\sqrt{3}\cdot 3\sqrt{2}$.")],
  r"$\overrightarrow{QP} = (k - 1, 2, -2)$ and $\overrightarrow{QR} = (2, 1, -1)$. Perpendicularity: $2(k-1) + 2 + 2 = 0$, so $k = -1$. Then $QP = \sqrt{4 + 4 + 4} = 2\sqrt{3}$, $QR = \sqrt{6}$, and the area is $\frac{1}{2}\cdot 2\sqrt{3}\cdot\sqrt{6} = 3\sqrt{2}$.",
  "Using the hypotenuse as a leg in the right-triangle area.",
  "U11-A-right-angle-param", "Perpendicularity condition to find the parameter, then lengths and area.",
  check=_c34, values=[3*sqrt(2), 6*sqrt(2), 2*sqrt(3), 3*sqrt(6)], cognitive="Application", source_class=XII)


def _c35():
    P, Q, R = V(4, 0, 1), V(2, -1, 3), V(1, -3, 5)
    return acos(cosang(P - Q, R - Q))
q("U11-A-035", TOP_ANG, "Angle of a triangle in space", "Medium", "Multi-step computation MCQ",
  r"For the triangle with vertices $P(4, 0, 1)$, $Q(2, -1, 3)$ and $R(1, -3, 5)$, the angle $\angle PQR$ equals",
  r"$\pi - \cos^{-1}\left(\frac{8}{9}\right)$",
  [(r"$\cos^{-1}\left(\frac{8}{9}\right)$", r"Takes the acute angle between the lines $QP$ and $QR$, ignoring that the dot product of $\overrightarrow{QP}$ and $\overrightarrow{QR}$ is negative."),
   (r"$\frac{\pi}{2}$", r"Sign slip in the $z$-product: takes $(-2)(2)$ as $+4$, so the dot product becomes $-2 - 2 + 4 = 0$."),
   (r"$\pi - \cos^{-1}\left(\frac{8}{81}\right)$", r"Divides by $9 \cdot 9$, the product of the squared lengths.")],
  r"$\overrightarrow{QP} = (2, 1, -2)$ and $\overrightarrow{QR} = (-1, -2, 2)$, each of length $3$. Then $\cos\angle PQR = \frac{-2 - 2 - 4}{9} = -\frac{8}{9}$, so the angle is obtuse and equals $\pi - \cos^{-1}\left(\frac{8}{9}\right)$.",
  "Reporting the acute angle between lines when the angle of a triangle is obtuse.",
  "U11-A-triangle-angle", "Vectors from the vertex, a signed cosine, and an obtuse-angle trap.",
  check=_c35, values=[pi - acos(Rational(8, 9)), acos(Rational(8, 9)), pi/2, pi - acos(Rational(8, 81))],
  cognitive="Analysis", source_class=XII)


# ================================================================ DIFFICULT

def _c36():
    l, m, n = symbols('l m n', real=True)
    sols = solve([l - m + n, l*m - 2*m*n + 2*n*l, l**2 + m**2 + n**2 - 1], [l, m, n], dict=True)
    dirs = []
    for s in sols:
        v = Matrix([s[l], s[m], s[n]])
        if not any(v == w or v == -w for w in dirs):
            dirs.append(v)
    assert len(dirs) == 2
    return acos(Abs(simplify(dirs[0].dot(dirs[1]))))
q("U11-A-036", TOP_ANG, "Angle between lines whose direction cosines satisfy two relations", "Difficult", "Multi-step computation MCQ",
  r"The direction cosines $l, m, n$ of two lines satisfy $l - m + n = 0$ and $lm - 2mn + 2nl = 0$. The angle between the two lines is",
  r"$\frac{\pi}{3}$",
  [(r"$\cos^{-1}\left(\frac{5}{6}\right)$", r"Substitutes $n = l - m$ (sign slip) for the second direction, getting $2, 1, 1$ instead of $2, 1, -1$."),
   (r"$\frac{\pi}{6}$", r"Gets $\cos\theta = \frac{1}{2}$ but reads it as $\sin\theta = \frac{1}{2}$."),
   (r"$\cos^{-1}\left(\frac{1}{12}\right)$", r"Divides the dot product $3$ by $6 \cdot 6$, the product of squared magnitudes.")],
  r"From the first relation $n = m - l$. Substituting, $lm - 2m(m - l) + 2l(m - l) = 5lm - 2m^2 - 2l^2 = 0$, that is, $(2l - m)(l - 2m) = 0$. If $m = 2l$ then $n = l$, giving direction ratios $1, 2, 1$; if $l = 2m$ then $n = -m$, giving $2, 1, -1$. So $\cos\theta = \frac{2 + 2 - 1}{\sqrt{6}\sqrt{6}} = \frac{1}{2}$ and $\theta = \frac{\pi}{3}$.",
  "Sign errors when eliminating one direction cosine.",
  "U11-A-dc-two-relations", "Eliminate, factor a homogeneous quadratic, find two directions, then the angle.",
  check=_c36, values=[pi/3, acos(Rational(5, 6)), pi/6, acos(Rational(1, 12))], cognitive="Analysis", source_class=XII)


def _c37():
    a, b = V(2, 1, 2), V(4, -4, 2)
    ua, ub = a / a.norm(), b / b.norm()
    bis = ua + ub if ua.dot(ub) > 0 else ua - ub
    return dirn(bis)
q("U11-A-037", TOP_ANG, "Direction of an angle bisector", "Difficult", "Multi-step computation MCQ",
  r"Two intersecting lines have direction ratios $2, 1, 2$ and $4, -4, 2$. Direction ratios of the bisector of the acute angle between them are proportional to",
  r"$4, -1, 3$",
  [(r"$6, -3, 4$", r"Adds the direction ratios without first converting them to unit vectors (their magnitudes are $3$ and $6$)."),
   (r"$0, 3, 1$", r"Subtracts the unit vectors, which gives the bisector of the obtuse angle."),
   (r"$5, 2, -6$", r"Takes the cross product, which is perpendicular to both lines rather than bisecting them.")],
  r"Unit vectors: $\frac{1}{3}(2, 1, 2)$ and $\frac{1}{6}(4, -4, 2) = \frac{1}{3}(2, -2, 1)$. Their dot product is $\frac{4 - 2 + 2}{9} = \frac{4}{9} > 0$, so the angle between these directions is acute and its bisector is along their sum $\frac{1}{3}(4, -1, 3)$, that is, $4, -1, 3$.",
  "Adding raw direction ratios of different magnitudes to get a bisector.",
  "U11-A-bisector-dr", "Normalise, decide acute or obtuse by the sign of the dot product, then add.",
  check=_c37, values=[dirn((4, -1, 3)), dirn((6, -3, 4)), dirn((0, 3, 1)), dirn((5, 2, -6))],
  cognitive="Analysis", source_class=XII)


def _c38():
    P, Q, R = V(1, -1, 2), V(4, 5, 8), V(9, 3, -6)
    a, b, c = dist(Q, R), dist(R, P), dist(P, Q)
    return tup((a*P + b*Q + c*R) / (a + b + c))
q("U11-A-038", TOP_PT, "Incentre of a triangle in space", "Difficult", "Multi-step computation MCQ",
  r"The incentre of the triangle with vertices $P(1, -1, 2)$, $Q(4, 5, 8)$ and $R(9, 3, -6)$ is",
  r"$(4, 2, 2)$",
  [(r"$(\frac{16}{3}, \frac{8}{3}, \frac{2}{3})$", r"Pairs the side lengths with the wrong vertices, weighting $P, Q, R$ by $9, 12, 15$ instead of $15, 12, 9$."),
   (r"$(\frac{14}{3}, \frac{7}{3}, \frac{4}{3})$", r"Gives the centroid, using equal weights."),
   (r"$(\frac{13}{2}, 4, 1)$", r"Notices the right angle at $P$ and gives the midpoint of the hypotenuse $QR$, which is the circumcentre.")],
  r"$QR = \sqrt{25 + 4 + 196} = 15$, $RP = \sqrt{64 + 16 + 64} = 12$, $PQ = \sqrt{9 + 36 + 36} = 9$. The incentre is $\frac{15P + 12Q + 9R}{36} = \frac{(15 + 48 + 81,\ -15 + 60 + 27,\ 30 + 96 - 54)}{36} = (4, 2, 2)$.",
  "Weighting each vertex by an adjacent side instead of the opposite side.",
  "U11-A-incentre", "Three distances, then the weighted section-type formula with a pairing trap.",
  check=_c38, values=[(4, 2, 2), (Rational(16, 3), Rational(8, 3), Rational(2, 3)), (Rational(14, 3), Rational(7, 3), Rational(4, 3)), (Rational(13, 2), 4, 1)],
  cognitive="Analysis", source_class="XI")


def _c39():
    l, m = symbols('l m', real=True)
    n2 = 1 - l**2 - m**2
    diags = [V(1, 1, 1), V(-1, 1, 1), V(1, -1, 1), V(1, 1, -1)]
    n = Symbol('n', real=True)
    u = Matrix([l, m, n])
    s = sum(1 - (u.dot(d))**2 / d.dot(d) for d in diags)
    return simplify(expand(s).subs(n**2, n2))
q("U11-A-039", TOP_ANG, "Angles with the four diagonals of a cube", "Difficult", "Conceptual/application MCQ",
  r"A line makes angles $\theta_1, \theta_2, \theta_3, \theta_4$ with the four body diagonals of a cube. Then $\sin^2\theta_1 + \sin^2\theta_2 + \sin^2\theta_3 + \sin^2\theta_4$ equals",
  r"$\frac{8}{3}$",
  [(r"$\frac{4}{3}$", r"Computes $\sum\cos^2\theta_i = \frac{4}{3}$ and stops there."),
   (r"$2$", r"Carries over $\sin^2\alpha + \sin^2\beta + \sin^2\gamma = 2$ from the three axes."),
   (r"$3$", r"Assumes $\sum\cos^2\theta_i = 1$ by analogy with the axes, giving $4 - 1$.")],
  r"With the cube along the axes, the diagonals have direction cosines $\frac{1}{\sqrt{3}}(\pm 1, \pm 1, 1)$. For a line with direction cosines $l, m, n$, $\sum\cos^2\theta_i = \frac{1}{3}\left[(l+m+n)^2 + (-l+m+n)^2 + (l-m+n)^2 + (l+m-n)^2\right] = \frac{4}{3}(l^2+m^2+n^2) = \frac{4}{3}$. Hence $\sum\sin^2\theta_i = 4 - \frac{4}{3} = \frac{8}{3}$.",
  "Applying the three-axes identity to the four diagonals.",
  "U11-A-cube-diagonals-sum", "Coordinate set-up, expansion of four squares, and conversion to sines.",
  check=_c39, values=[Rational(8, 3), Rational(4, 3), 2, 3], cognitive="Analysis", source_class=XII)


def _c40():
    A = Matrix([[0, Rational(1, 2), Rational(1, 2)], [Rational(1, 2), 0, Rational(1, 2)], [Rational(1, 2), Rational(1, 2), 0]])
    ev = list(A.eigenvals().keys())     # lm+mn+nl = u^T A u on the unit sphere
    return Interval(Min(*ev), Max(*ev))
q("U11-A-040", TOP_DC, "Range of an expression in direction cosines", "Difficult", "Multi-step computation MCQ",
  r"If $l, m, n$ are the direction cosines of a line, then the set of all possible values of $lm + mn + nl$ is",
  r"$\left[-\frac{1}{2}, 1\right]$",
  [(r"$[-1, 2]$", r"Writes $lm + mn + nl = (l+m+n)^2 - 1$, dropping the factor $\frac{1}{2}$."),
   (r"$[0, 1]$", r"Assumes direction cosines are non-negative, so $l + m + n \ge 1$ and the expression cannot be negative."),
   (r"$\left[-\frac{1}{2}, \frac{1}{3}\right]$", r"Finds the minimum correctly but takes the maximum at $l = m = n = \frac{1}{3}$, using direction ratios as if they were direction cosines.")],
  r"$(l + m + n)^2 = 1 + 2(lm + mn + nl)$, so $lm + mn + nl = \frac{(l+m+n)^2 - 1}{2}$. Since $0 \le (l+m+n)^2 \le 3(l^2+m^2+n^2) = 3$, the expression lies in $\left[-\frac{1}{2}, 1\right]$; the value $-\frac{1}{2}$ occurs for $\frac{1}{\sqrt{2}}(1, -1, 0)$ and $1$ for $l = m = n = \frac{1}{\sqrt{3}}$.",
  "Forgetting that direction cosines can be negative, so $l + m + n$ can be zero.",
  "U11-A-dc-range", "Identity plus an inequality and attainment of both ends.",
  check=_c40, values=[Interval(Rational(-1, 2), 1), Interval(-1, 2), Interval(0, 1), Interval(Rational(-1, 2), Rational(1, 3))],
  cognitive="Analysis", source_class=XII)


def _c41():
    P, Q, R = V(1, -1, 2), V(3, 3, 6), V(9, 3, -6)
    c, b = dist(P, Q), dist(P, R)
    return tup((b*Q + c*R) / (b + c))     # QT:TR = PQ:PR
q("U11-A-041", TOP_PT, "Foot of an internal angle bisector", "Difficult", "Multi-step computation MCQ",
  r"In the triangle with vertices $P(1, -1, 2)$, $Q(3, 3, 6)$ and $R(9, 3, -6)$, the internal bisector of $\angle QPR$ meets $QR$ at $T$. Then $T$ is",
  r"$(5, 3, 2)$",
  [(r"$(7, 3, -2)$", r"Uses $QT : TR = PR : PQ = 2 : 1$, reversing the ratio."),
   (r"$(6, 3, 0)$", r"Assumes the bisector meets $QR$ at its midpoint."),
   (r"$(\frac{13}{3}, \frac{5}{3}, \frac{2}{3})$", r"Gives the centroid, confusing the bisector with a median.")],
  r"$PQ = \sqrt{4 + 16 + 16} = 6$ and $PR = \sqrt{64 + 16 + 64} = 12$. The bisector divides $QR$ in the ratio $QT : TR = PQ : PR = 1 : 2$, so $T = \frac{2Q + R}{3} = \left(\frac{6 + 9}{3}, \frac{6 + 3}{3}, \frac{12 - 6}{3}\right) = (5, 3, 2)$.",
  "Reversing the angle bisector ratio.",
  "U11-A-angle-bisector-foot", "Two distances, angle bisector theorem, then the section formula with an order trap.",
  check=_c41, values=[(5, 3, 2), (7, 3, -2), (6, 3, 0), (Rational(13, 3), Rational(5, 3), Rational(2, 3))],
  cognitive="Analysis", source_class="XI")


def _c42():
    a = Symbol('a', positive=True)
    O = Matrix([0, 0, 0])
    body = Matrix([a, a, a]) - O
    # face diagonals of the cube; keep those that do not meet the body diagonal from O to (a,a,a)
    verts = [Matrix([x, y, z]) for x in (0, a) for y in (0, a) for z in (0, a)]
    angs = set()
    for i, U in enumerate(verts):
        for W in verts[i+1:]:
            d = W - U
            if sum(1 for t in d if t != 0) != 2:
                continue
            if U == O or W == O or U == body or W == body:
                continue
            angs.add(acos(Abs(cosang(body, d))))
    assert len(angs) == 1
    return angs.pop()
q("U11-A-042", TOP_ANG, "Angle between a body diagonal and a face diagonal", "Difficult", "Conceptual/application MCQ",
  r"In a cube, let $d$ be a body diagonal and let $e$ be a diagonal of one of the faces such that $e$ does not meet $d$. The angle between the lines $d$ and $e$ is",
  r"$\frac{\pi}{2}$",
  [(r"$\cos^{-1}\left(\sqrt{\frac{2}{3}}\right)$", r"Uses a face diagonal through an end of $d$, which does meet $d$."),
   (r"$\cos^{-1}\left(\frac{1}{3}\right)$", r"Uses a second body diagonal in place of the face diagonal."),
   (r"$\frac{\pi}{3}$", r"Uses two face diagonals meeting at a vertex.")],
  r"Place the cube with $O(0,0,0)$ and $d$ from $O$ to $(a, a, a)$, so $d$ has direction ratios $1, 1, 1$. The face diagonals that avoid $d$ are those not through $O$ or $(a, a, a)$, such as the one joining $(a, 0, 0)$ and $(0, a, 0)$, with direction ratios $-1, 1, 0$. Every such diagonal has direction ratios like $\pm(1, -1, 0)$ up to order, and $1 - 1 + 0 = 0$, so the angle is $\frac{\pi}{2}$.",
  "Assuming a non-intersecting face diagonal is inclined like one through the same vertex.",
  "U11-A-cube-diagonals", "Spatial set-up, choosing the right face diagonal, then a perpendicularity check.",
  check=_c42, values=[pi/2, acos(sqrt(Rational(2, 3))), acos(Rational(1, 3)), pi/3],
  cognitive="Analysis", source_class=XII)


def _c43():
    k = Symbol('k')
    G = (Matrix([1, k, 2]) + Matrix([k, -1, 3]) + Matrix([4, 2, k])) / 3
    roots = solve(G.dot(G) - 3, k)
    assert all(r.is_real for r in roots) and len(roots) == 2
    return simplify(roots[0] * roots[1])
q("U11-A-043", TOP_PT, "Centroid with a parameter", "Difficult", "Inverse/parameter MCQ",
  r"The triangle with vertices $P(1, k, 2)$, $Q(k, -1, 3)$ and $R(4, 2, k)$ has its centroid at distance $\sqrt{3}$ from the origin. The product of all real values of $k$ is",
  r"$8$",
  [(r"$-\frac{22}{3}$", r"Solves $3k^2 + 22k + 24 = 0$ correctly but reports the sum of the roots."),
   (r"$24$", r"Takes the constant term of $3k^2 + 22k + 24 = 0$ without dividing by the leading coefficient."),
   (r"$-10$", r"Equates $|OG|^2$ to $9$ (squaring $3$ instead of $\sqrt{3}$), so $2(5+k)^2 + (1+k)^2 = 81$, that is, $3k^2 + 22k - 30 = 0$, whose real roots have product $-10$.")],
  r"The centroid is $\left(\frac{5+k}{3}, \frac{1+k}{3}, \frac{5+k}{3}\right)$. The condition gives $\frac{2(5+k)^2 + (1+k)^2}{9} = 3$, that is, $3k^2 + 22k + 24 = 0$, so $(k + 6)(3k + 4) = 0$ and $k = -6$ or $k = -\frac{4}{3}$, both real. The product is $8$.",
  r"Dropping the factor $\frac{1}{3}$ in the centroid before squaring.",
  "U11-A-centroid-param", "Centroid, distance, quadratic and Vieta combined.",
  check=_c43, values=[8, Rational(-22, 3), 24, -10], cognitive="Application", source_class="XI",
  numerical=dict(question=r"The triangle with vertices $P(1, k, 2)$, $Q(k, -1, 3)$ and $R(4, 2, k)$ has its centroid at distance $\sqrt{3}$ from the origin. The product of all real values of $k$ is", answer=8))


def _c44():
    k = Symbol('k', real=True)
    d1, d2 = V(1, 0, 1), Matrix([1, 1, k])
    eq = 4 * d1.dot(d2)**2 - d1.dot(d1) * d2.dot(d2)   # |cos| = 1/2, angle between lines
    sols = [r for r in solve(eq, k) if simplify(Abs(cosang(d1, d2.subs(k, r))) - Rational(1, 2)) == 0]
    return FiniteSet(*sols)
q("U11-A-044", TOP_ANG, "Parameter from the angle between lines", "Difficult", "Inverse/parameter MCQ",
  r"The acute angle between the lines with direction ratios $1, 0, 1$ and $1, 1, k$ is $\frac{\pi}{3}$. The set of all real values of $k$ is",
  r"$\{-4, 0\}$",
  [(r"$\{0\}$", r"Rejects $k = -4$ because the dot product $1 + k$ is then negative, forgetting that the angle between lines uses $|\cos\theta|$."),
   (r"$\{-4\}$", r"Divides $2k^2 + 8k = 0$ by $k$, losing the root $k = 0$."),
   (r"$\{0, 4\}$", r"Sign slip in expanding $(1+k)^2$, getting $2k^2 - 8k = 0$.")],
  r"$\cos\frac{\pi}{3} = \frac{|1 + k|}{\sqrt{2}\sqrt{2 + k^2}}$ gives $4(1+k)^2 = 2(2 + k^2)$, that is, $2k^2 + 8k = 0$, so $k = 0$ or $k = -4$. For $k = -4$ the direction ratios give $\cos = -\frac{1}{2}$, which still means the lines are inclined at $\frac{\pi}{3}$. Both values are valid.",
  "Discarding a root because the direction ratios make an obtuse angle, although lines have no preferred direction.",
  "U11-A-angle-param", "Squared condition, factorisation, and a validity check where the tempting rejection is wrong.",
  check=_c44, values=[FiniteSet(-4, 0), FiniteSet(0), FiniteSet(-4), FiniteSet(0, 4)],
  cognitive="Analysis", source_class=XII)


def _c45():
    P, Q, R, S = V(3, 2, 3), V(2, 1, 0), V(-1, 0, -1), V(0, 1, 2)
    para = (P + R) == (Q + S)
    rh = dist(P, Q) == dist(Q, R)
    eqd = dist(P, R) == dist(Q, S)
    return (bool(para), bool(rh), bool(eqd))
q("U11-A-045", TOP_PT, "Type of quadrilateral from coordinates", "Difficult", "Multi-step computation MCQ",
  r"The quadrilateral $PQRS$ with vertices $P(3, 2, 3)$, $Q(2, 1, 0)$, $R(-1, 0, -1)$ and $S(0, 1, 2)$, taken in this order, is",
  r"a rhombus but not a square",
  [(r"a square", r"Finds the diagonals bisecting each other and all sides equal, and assumes the diagonals are also equal without computing $PR = 6$ and $QS = 2\sqrt{2}$."),
   (r"a rectangle but not a square", r"Miscomputes $QR^2$ as $9 + 1 + 9$ by mis-squaring, so adjacent sides look unequal, and then assumes equal diagonals."),
   (r"a parallelogram that is neither a rectangle nor a rhombus", r"Checks only that the diagonals bisect each other and compares $PQ$ with $PR$ instead of with $QR$.")],
  r"The midpoints of $PR$ and $QS$ are both $(1, 1, 1)$, so $PQRS$ is a parallelogram. $PQ^2 = 1 + 1 + 9 = 11$ and $QR^2 = 9 + 1 + 1 = 11$, so adjacent sides are equal: a rhombus. The diagonals are $PR = \sqrt{16 + 4 + 16} = 6$ and $QS = \sqrt{4 + 0 + 4} = 2\sqrt{2}$, which are unequal, so it is not a square.",
  "Concluding square from equal sides without testing the diagonals.",
  "U11-A-quadrilateral-type", "Three separate tests (midpoints, sides, diagonals) combined.",
  check=_c45, values=[(True, True, False), (True, True, True), (True, False, True), (True, False, False)],
  cognitive="Analysis", source_class="XI")


def _c46():
    a, b, c = symbols('a b c')
    P, Q = V(2, -1, -3), Matrix([a, b, c])
    ex = []
    ex.append(((2*Q + 1*P) / 3)[0])        # yz-plane, PX:XQ = 2:1 internally
    ex.append(((1*Q + 3*P) / 4)[1])        # xz-plane, 1:3 internally
    ex.append(((3*Q - 2*P) / (3 - 2))[2])  # xy-plane, 3:2 externally
    s = solve(ex, [a, b, c], dict=True)[0]
    return (s[a], s[b], s[c])
q("U11-A-046", TOP_PT, "Point from ratios of division by coordinate planes", "Difficult", "Inverse/parameter MCQ",
  r"For $P(2, -1, -3)$ and an unknown point $Q$, the $yz$-plane divides $PQ$ internally in the ratio $2 : 1$, the $xz$-plane divides $PQ$ internally in the ratio $1 : 3$, and the $xy$-plane divides $PQ$ externally in the ratio $3 : 2$. (Each ratio is $PX : XQ$, where $X$ is the point of division.) Then $Q$ is",
  r"$(-1, 3, -2)$",
  [(r"$(-1, 3, 2)$", r"Treats the external division by the $xy$-plane as internal: $\frac{3c + 2(-3)}{5} = 0$."),
   (r"$(-4, \frac{1}{3}, -\frac{9}{2})$", r"Attaches every ratio the wrong way round, using $\frac{mP + nQ}{m + n}$ and $\frac{mP - nQ}{m - n}$."),
   (r"$(-1, 3, -\frac{9}{2})$", r"Handles the internal ratios correctly but reverses the external one: $\frac{3P - 2Q}{3 - 2}$ for $z$.")],
  r"With $Q(a, b, c)$: $x$-coordinate of $\frac{2Q + P}{3}$ is $0$, so $2a + 2 = 0$ and $a = -1$. $y$-coordinate of $\frac{Q + 3P}{4}$ is $0$, so $b - 3 = 0$ and $b = 3$. $z$-coordinate of $\frac{3Q - 2P}{3 - 2}$ is $0$, so $3c + 6 = 0$ and $c = -2$. Hence $Q = (-1, 3, -2)$; consistently, $z$ goes from $-3$ to $-2$ without crossing $0$, as external division requires.",
  "Swapping the weights in the section formula, especially for external division.",
  "U11-A-section-reverse-planes", "Three section conditions, internal and external, solved for an unknown endpoint.",
  check=_c46, values=[(-1, 3, -2), (-1, 3, 2), (-4, Rational(1, 3), Rational(-9, 2)), (-1, 3, Rational(-9, 2))],
  cognitive="Analysis", source_class="XI")


def _c47():
    s1, s2 = symbols('s1 s2', positive=True)
    f = s1 * s2 * (2 - s1 - s2)            # product of sin^2, with sum of sin^2 equal to 2
    crit = solve([diff(f, s1), diff(f, s2)], [s1, s2], dict=True)
    best = Max(*[f.subs(c) for c in crit])
    return sqrt(best)
q("U11-A-047", TOP_DC, "Maximum of a product of sines of direction angles", "Difficult", "Multi-step computation MCQ",
  r"A line makes angles $\alpha, \beta, \gamma$ with the positive coordinate axes. The greatest possible value of $\sin\alpha\sin\beta\sin\gamma$ is",
  r"$\frac{2\sqrt{6}}{9}$",
  [(r"$\frac{\sqrt{3}}{9}$", r"Maximises $\cos\alpha\cos\beta\cos\gamma$ instead, getting $\left(\frac{1}{\sqrt{3}}\right)^3$."),
   (r"$\frac{8}{27}$", r"Finds the maximum $\left(\frac{2}{3}\right)^3$ of $\sin^2\alpha\sin^2\beta\sin^2\gamma$ and forgets the square root."),
   (r"$\frac{1}{2}$", r"Tests only $\alpha = \beta = 45^\circ$, $\gamma = 90^\circ$.")],
  r"$\sin^2\alpha + \sin^2\beta + \sin^2\gamma = 3 - 1 = 2$. By AM-GM, $\sin^2\alpha\sin^2\beta\sin^2\gamma \le \left(\frac{2}{3}\right)^3 = \frac{8}{27}$, with equality when all three equal $\frac{2}{3}$ (the line equally inclined to the axes). So the greatest value is $\sqrt{\frac{8}{27}} = \frac{2\sqrt{2}}{3\sqrt{3}} = \frac{2\sqrt{6}}{9}$.",
  "Optimising the wrong quantity or forgetting the square root after AM-GM.",
  "U11-A-dc-extremum", r"Convert to $\sin^2$, use their fixed sum, apply AM-GM and take a root.",
  check=_c47, values=[2*sqrt(6)/9, sqrt(3)/9, Rational(8, 27), Rational(1, 2)], cognitive="Analysis", source_class=XII)
