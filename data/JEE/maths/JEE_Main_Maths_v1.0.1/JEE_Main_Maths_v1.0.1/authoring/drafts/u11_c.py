import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
T_, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_SD = "Shortest distance between skew lines"
TOP_PAR = "Distance between parallel lines"
TOP_NAT = "Skew, intersecting and parallel lines"
TOP_INT = "Condition for intersection of two lines"
TOP_LSD = "Line of shortest distance"

# nature codes
INTERSECT, PARALLEL, SKEW, COINCIDENT = 0, 1, 2, 3


def _V(*a):
    return Matrix([nsimplify(x) for x in a])


def _sd(a1, b1, a2, b2):
    """Shortest distance between r = a1 + s b1 and r = a2 + t b2 (handles parallel lines)."""
    a1, b1, a2, b2 = [Matrix(v) for v in (a1, b1, a2, b2)]
    n = b1.cross(b2)
    if simplify(n.norm()) == 0:
        return simplify((a2 - a1).cross(b1).norm() / b1.norm())
    return simplify(Abs((a2 - a1).dot(n)) / n.norm())


def _nature(a1, b1, a2, b2):
    a1, b1, a2, b2 = [Matrix(v) for v in (a1, b1, a2, b2)]
    n = b1.cross(b2)
    d = a2 - a1
    if simplify(n.norm()) == 0:
        return COINCIDENT if simplify(d.cross(b1).norm()) == 0 else PARALLEL
    return INTERSECT if simplify(d.dot(n)) == 0 else SKEW


def _feet(a1, b1, a2, b2):
    a1, b1, a2, b2 = [Matrix(v) for v in (a1, b1, a2, b2)]
    s_, t_ = symbols('s_ t_')
    P = a1 + s_ * b1
    Q = a2 + t_ * b2
    sol = solve([(Q - P).dot(b1), (Q - P).dot(b2)], [s_, t_], dict=True)[0]
    return P.subs(sol), Q.subs(sol)


def _cdir(v):
    """Primitive integer direction with first nonzero entry positive."""
    v = [nsimplify(x) for x in v]
    den = 1
    for x in v:
        den = ilcm(den, fraction(x)[1])
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = igcd(g, abs(x))
    w = [x // g for x in w]
    for x in w:
        if x != 0:
            if x < 0:
                w = [-y for y in w]
            break
    return tuple(Integer(x) for x in w)


def _cline(p, v):
    """Canonical form of a line: (primitive direction, foot of perpendicular from the origin)."""
    p, v = Matrix(p), Matrix(v)
    f = p - (p.dot(v) / v.dot(v)) * v
    return (_cdir(v), tuple(simplify(x) for x in f))


def _det3(d, b1, b2):
    return Matrix([list(d), list(b1), list(b2)]).det()


# =========================================================== EASY (14)

def _c1():
    return _sd((1, 0, 2), (1, -2, 2), (2, 3, -1), (3, 2, 2))
q("U11-C-001", TOP_SD, "Shortest distance, vector form", "Easy", "Single-step computation MCQ",
  r"The shortest distance between the lines $\vec{r} = (\hat{i} + 2\hat{k}) + \lambda(\hat{i} - 2\hat{j} + 2\hat{k})$ and $\vec{r} = (2\hat{i} + 3\hat{j} - \hat{k}) + \mu(3\hat{i} + 2\hat{j} + 2\hat{k})$ is",
  r"$\frac{5}{3}$",
  [(r"$\frac{1}{3}$", r"Uses $\vec{a}_1 + \vec{a}_2 = 3\hat{i} + 3\hat{j} + \hat{k}$ in place of $\vec{a}_2 - \vec{a}_1$: $|(3,3,1)\cdot(-8,4,8)|/12 = 4/12 = \frac{1}{3}$."),
   (r"$\frac{5}{36}$", r"Divides $|(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2)| = 20$ by $|\vec{b}_1 \times \vec{b}_2|^2 = 144$ instead of by $12$."),
   (r"$\frac{20}{3}$", r"Divides $20$ by $\vec{b}_1 \cdot \vec{b}_2 = 3 - 4 + 4 = 3$ instead of by $|\vec{b}_1 \times \vec{b}_2|$.")],
  r"Here $\vec{a}_2 - \vec{a}_1 = \hat{i} + 3\hat{j} - 3\hat{k}$ and $\vec{b}_1 \times \vec{b}_2 = -8\hat{i} + 4\hat{j} + 8\hat{k}$, with $|\vec{b}_1 \times \vec{b}_2| = 12$. Then $(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2) = -8 + 12 - 24 = -20$. So the shortest distance is $\frac{20}{12} = \frac{5}{3}$.",
  r"Using the sum of position vectors or the wrong normalising factor in $d = \frac{|(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2)|}{|\vec{b}_1 \times \vec{b}_2|}$.",
  "U11-C-sd-vector", "Direct application of the skew-line distance formula; one cross product and one dot product.",
  check=_c1, values=[Rational(5, 3), Rational(1, 3), Rational(5, 36), Rational(20, 3)],
  cognitive="Application", source_class="XII")


def _c2():
    return _sd((1, 2, -1), (2, 1, -2), (4, 2, -1), (4, 2, -4))
q("U11-C-002", TOP_PAR, "Distance between parallel lines, vector form", "Easy", "Single-step computation MCQ",
  r"The distance between the parallel lines $\vec{r} = (\hat{i} + 2\hat{j} - \hat{k}) + \lambda(2\hat{i} + \hat{j} - 2\hat{k})$ and $\vec{r} = (4\hat{i} + 2\hat{j} - \hat{k}) + \mu(4\hat{i} + 2\hat{j} - 4\hat{k})$ is",
  r"$\sqrt{5}$",
  [(r"$2$", r"Computes the projection $\frac{|(\vec{a}_2 - \vec{a}_1)\cdot\vec{b}|}{|\vec{b}|} = \frac{6}{3} = 2$ along the lines instead of the perpendicular component."),
   (r"$3$", r"Takes $|\vec{a}_2 - \vec{a}_1| = |3\hat{i}| = 3$, the distance between the two given points, as the distance between the lines."),
   (r"$2\sqrt{5}$", r"Crosses $3\hat{i}$ with $4\hat{i} + 2\hat{j} - 4\hat{k}$ (magnitude $6\sqrt{5}$) but divides by $|2\hat{i} + \hat{j} - 2\hat{k}| = 3$.")],
  r"The lines are parallel with $\vec{b} = 2\hat{i} + \hat{j} - 2\hat{k}$, $|\vec{b}| = 3$. With $\vec{a}_2 - \vec{a}_1 = 3\hat{i}$, $(\vec{a}_2 - \vec{a}_1) \times \vec{b} = 6\hat{j} + 3\hat{k}$, of magnitude $3\sqrt{5}$. The distance is $\frac{3\sqrt{5}}{3} = \sqrt{5}$.",
  r"Using the projection of $\vec{a}_2 - \vec{a}_1$ on the line, or mixing the two scaled direction vectors.",
  "U11-C-sd-parallel", "One cross product for parallel lines; must notice the second direction is a multiple of the first.",
  check=_c2, values=[sqrt(5), 2, 3, 2 * sqrt(5)], cognitive="Application", source_class="XII")


def _c3():
    return _sd((0, 0, 0), (1, 0, 0), (4, 1, 4), (2, -1, 2))
q("U11-C-003", TOP_SD, "Shortest distance from a coordinate axis", "Easy", "Single-step computation MCQ",
  r"The shortest distance between the $x$-axis and the line $\vec{r} = (4\hat{i} + \hat{j} + 4\hat{k}) + \lambda(2\hat{i} - \hat{j} + 2\hat{k})$ is",
  r"$\frac{6\sqrt{5}}{5}$",
  [(r"$\sqrt{17}$", r"Gives the distance of the point $(4,1,4)$ from the $x$-axis, $\sqrt{1 + 16}$, ignoring the direction of the line."),
   (r"$6$", r"Stops at $|(4,1,4)\cdot(0,-2,-1)| = 6$ and does not divide by $|\hat{i} \times \vec{b}| = \sqrt{5}$."),
   (r"$2$", r"Divides $6$ by $|\vec{b}| = 3$ instead of by $|\hat{i} \times \vec{b}| = \sqrt{5}$.")],
  r"Take the $x$-axis as $\vec{r} = \mu\hat{i}$. Then $\hat{i} \times (2\hat{i} - \hat{j} + 2\hat{k}) = -2\hat{j} - \hat{k}$, of magnitude $\sqrt{5}$. With $\vec{a}_2 - \vec{a}_1 = 4\hat{i} + \hat{j} + 4\hat{k}$, the dot product is $-2 - 4 = -6$. So the distance is $\frac{6}{\sqrt{5}} = \frac{6\sqrt{5}}{5}$.",
  "Confusing the distance of a point of the line from the axis with the distance between the lines.",
  "U11-C-sd-axes", "Single use of the skew-line formula with the axis written as a line.",
  check=_c3, values=[6 * sqrt(5) / 5, sqrt(17), 6, 2], cognitive="Application", source_class="XII")


def _c4():
    k, t = symbols('k t')
    P = _V(1, k, -2) + t * _V(2, 3, 1)
    sol = solve([P[1], P[2]], [k, t], dict=True)
    assert len(sol) == 1
    kk = sol[0][k]
    # cross-check with the coplanarity test against the x-axis (a non-parallel line)
    assert _nature((1, kk, -2), (2, 3, 1), (0, 0, 0), (1, 0, 0)) == INTERSECT
    return kk
q("U11-C-004", TOP_INT, "Parameter for a line to meet a coordinate axis", "Easy", "Inverse/parameter MCQ",
  r"If the line $\frac{x-1}{2} = \frac{y-k}{3} = \frac{z+2}{1}$ meets the $x$-axis, then $k$ equals",
  r"$-6$",
  [(r"$6$", r"Reads $z + 2$ as $z - 2$, so $z = 0$ gives the parameter $t = -2$ and $y = k - 6 = 0$, i.e. $k = 6$."),
   (r"$\frac{3}{2}$", r"Imposes $x = 0$ and $y = 0$ (the conditions for meeting the $z$-axis) instead of $y = 0$ and $z = 0$: $x = 0$ gives $t = -\frac{1}{2}$, so $k - \frac{3}{2} = 0$."),
   (r"$-\frac{2}{3}$", r"Sets up $\frac{0 - k}{3} = \frac{0 + 2}{1}$ correctly but clears the fraction wrongly, writing $-k = \frac{2}{3}$.")],
  r"Every point of the $x$-axis has $y = 0$ and $z = 0$. A general point of the line is $(1 + 2t,\ k + 3t,\ -2 + t)$. Putting $z = 0$ gives $t = 2$, and then $y = k + 6 = 0$ gives $k = -6$. The common point is $(5, 0, 0)$, so for $k = -6$ the line does meet the $x$-axis.",
  r"Using the wrong pair of coordinate conditions for a point on an axis, or a sign slip in reading the point of the line.",
  "U11-C-meets-axis-param", r"One substitution $y = z = 0$ into the general point and a linear equation in $k$.",
  check=_c4, values=[-6, 6, Rational(3, 2), Rational(-2, 3)],
  cognitive="Application", source_class="XII")


def _c5():
    return _nature((1, -1, 0), (2, -3, 4), (3, 2, -1), (-4, 6, -8))
q("U11-C-005", TOP_NAT, "Recognising parallel lines", "Easy", "Conceptual/application MCQ",
  r"The lines $\frac{x-1}{2} = \frac{y+1}{-3} = \frac{z}{4}$ and $\frac{x-3}{-4} = \frac{y-2}{6} = \frac{z+1}{-8}$ are",
  r"parallel and distinct",
  [(r"coincident", r"Sees that the direction ratios are proportional and stops, without checking whether $(3,2,-1)$ lies on the first line (it does not)."),
   (r"intersecting at exactly one point", r"Assumes two lines with different-looking equations must meet, ignoring that proportional direction ratios rule out a single common point."),
   (r"skew", r"Takes the opposite signs of the denominators to mean non-parallel directions, missing that $(-4,6,-8) = -2(2,-3,4)$.")],
  r"The direction ratios satisfy $(-4, 6, -8) = -2(2, -3, 4)$, so the lines are parallel. The point $(3, 2, -1)$ of the second line gives $\frac{3-1}{2} = 1$ but $\frac{2+1}{-3} = -1$, so it is not on the first line. Hence the lines are parallel and distinct.",
  "Not separating the parallel case into coincident and distinct.",
  "U11-C-classify", "Two quick checks: proportional direction ratios, then a point test.",
  check=_c5, values=[PARALLEL, COINCIDENT, INTERSECT, SKEW], cognitive="Understanding", source_class="XII")


q("U11-C-006", TOP_NAT, "Coplanarity condition", "Easy", "Direct concept MCQ",
  r"Two lines $\vec{r} = \vec{a}_1 + \lambda\vec{b}_1$ and $\vec{r} = \vec{a}_2 + \mu\vec{b}_2$ satisfy $\vec{b}_1 \times \vec{b}_2 \ne \vec{0}$ and $(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2) = 0$. Then the lines",
  r"intersect at exactly one point",
  [(r"are parallel and distinct", r"Reads the zero triple product as the condition for parallel lines, ignoring $\vec{b}_1 \times \vec{b}_2 \ne \vec{0}$."),
   (r"are skew", r"Reverses the test: a zero scalar triple product means zero shortest distance, which is not the skew case."),
   (r"are coincident", r"Treats zero shortest distance as meaning the lines are the same, though non-parallel directions forbid that.")],
  r"The condition $\vec{b}_1 \times \vec{b}_2 \ne \vec{0}$ means the lines are not parallel. The shortest distance $\frac{|(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2)|}{|\vec{b}_1 \times \vec{b}_2|}$ is then $0$, so the two non-parallel lines are coplanar. Hence they meet in exactly one point.",
  "Mixing up the conditions for parallel, skew and intersecting lines.",
  "U11-C-concept-coplanar", "Recall of one criterion and its meaning.",
  cognitive="Understanding", source_class="XII")


def _c7():
    return _sd((2, 1, -3), (1, -2, -2), (4, 2, -1), (2, 2, -1))
q("U11-C-007", TOP_SD, "Shortest distance, Cartesian form", "Easy", "Single-step computation MCQ",
  r"The shortest distance between the lines $\frac{x-2}{1} = \frac{y-1}{-2} = \frac{z+3}{-2}$ and $\frac{x-4}{2} = \frac{y-2}{2} = \frac{z+1}{-1}$ is",
  r"$\frac{7}{3}$",
  [(r"$\frac{7}{27}$", r"Divides $21$ by $|\vec{b}_1 \times \vec{b}_2|^2 = 81$ instead of by $9$."),
   (r"$\frac{1}{3}$", r"Uses $\vec{a}_1 + \vec{a}_2 = (6,3,-4)$: $|(6,3,-4)\cdot(6,-3,6)|/9 = 3/9$."),
   (r"$3$", r"Gives the distance between the two given points $(2,1,-3)$ and $(4,2,-1)$, which is $3$.")],
  r"Here $\vec{b}_1 \times \vec{b}_2 = (1,-2,-2) \times (2,2,-1) = (6,-3,6)$, of magnitude $9$. With $\vec{a}_2 - \vec{a}_1 = (2,1,2)$, the dot product is $12 - 3 + 12 = 21$. So the shortest distance is $\frac{21}{9} = \frac{7}{3}$.",
  "Wrong normalisation or wrong connecting vector in the skew-line formula.",
  "U11-C-sd-cartesian", "Direct formula use with Cartesian data.",
  check=_c7, values=[Rational(7, 3), Rational(7, 27), Rational(1, 3), 3], cognitive="Application", source_class="XII")


def _c8():
    return _sd((2, -1, 3), (1, 2, 2), (2, 2, 6), (-2, -4, -4))
q("U11-C-008", TOP_PAR, "Distance between parallel lines, Cartesian form", "Easy", "Single-step computation MCQ",
  r"The distance between the lines $\frac{x-2}{1} = \frac{y+1}{2} = \frac{z-3}{2}$ and $\frac{x-2}{-2} = \frac{y-2}{-4} = \frac{z-6}{-4}$ is",
  r"$\sqrt{2}$",
  [(r"$3\sqrt{2}$", r"Takes the distance between the points $(2,-1,3)$ and $(2,2,6)$, i.e. $|(0,3,3)| = 3\sqrt{2}$."),
   (r"$\frac{\sqrt{2}}{3}$", r"Divides $|(0,3,3) \times (1,2,2)| = 3\sqrt{2}$ by $|\vec{b}|^2 = 9$ instead of by $3$."),
   (r"$\frac{\sqrt{2}}{2}$", r"Uses $|(0,3,3) \times (1,2,2)| = 3\sqrt{2}$ but divides by $|(-2,-4,-4)| = 6$.")],
  r"The direction ratios $(-2,-4,-4)$ and $(1,2,2)$ are proportional, so the lines are parallel with $\vec{b} = (1,2,2)$, $|\vec{b}| = 3$. With $\vec{a}_2 - \vec{a}_1 = (0,3,3)$, $(\vec{a}_2 - \vec{a}_1) \times \vec{b} = (0, 3, -3)$, of magnitude $3\sqrt{2}$. The distance is $\frac{3\sqrt{2}}{3} = \sqrt{2}$.",
  "Using the distance between two chosen points, or mismatching the scaled direction vectors.",
  "U11-C-sd-parallel", "One cross product after recognising parallel lines.",
  check=_c8, values=[sqrt(2), 3 * sqrt(2), sqrt(2) / 3, sqrt(2) / 2], cognitive="Application", source_class="XII")


def _c9():
    return _sd((0, 0, 0), (0, 0, 1), (3, -4, 1), (0, 0, 1))
q("U11-C-009", TOP_PAR, "Line parallel to an axis", "Easy", "Single-step computation MCQ",
  r"The distance between the $z$-axis and the line $\frac{x-3}{0} = \frac{y+4}{0} = \frac{z-1}{1}$ is",
  r"$5$",
  [(r"$\sqrt{26}$", r"Gives the distance of the point $(3,-4,1)$ from the origin, $\sqrt{9 + 16 + 1}$."),
   (r"$7$", r"Adds $|3| + |-4|$ instead of using $\sqrt{3^2 + 4^2}$."),
   (r"$25$", r"Computes $x^2 + y^2 = 25$ and forgets the square root.")],
  r"The line is $x = 3$, $y = -4$, parallel to the $z$-axis. Every point $(3, -4, z)$ is at distance $\sqrt{3^2 + (-4)^2} = 5$ from the $z$-axis, so the distance between the parallel lines is $5$.",
  "Including the $z$-coordinate or not taking a square root.",
  "U11-C-sd-axes", "One observation: the line is parallel to the axis.",
  check=_c9, values=[5, sqrt(26), 7, 25],
  numerical=dict(question=r"The distance between the $z$-axis and the line $\frac{x-3}{0} = \frac{y+4}{0} = \frac{z-1}{1}$ is", answer=5),
  cognitive="Application", source_class="XII")


def _c10():
    return _sd((1, 2, 3), (2, 3, 4), (4, 4, 9), (1, -1, 2))
q("U11-C-010", TOP_SD, "Zero shortest distance", "Easy", "Single-step computation MCQ",
  r"The shortest distance between the lines $\frac{x-1}{2} = \frac{y-2}{3} = \frac{z-3}{4}$ and $\frac{x-4}{1} = \frac{y-4}{-1} = \frac{z-9}{2}$ is",
  r"$0$",
  [(r"$7$", r"Takes the distance between the points $(1,2,3)$ and $(4,4,9)$, which is $\sqrt{9 + 4 + 36} = 7$."),
   (r"$\frac{\sqrt{5}}{5}$", r"Uses $\vec{a}_2 = (4,4,9)$ alone instead of $\vec{a}_2 - \vec{a}_1$: $|40 - 45|/(5\sqrt{5}) = \frac{1}{\sqrt{5}}$."),
   (r"$\frac{2\sqrt{5}}{5}$", r"Uses $\vec{a}_1 + \vec{a}_2 = (5,6,12)$: $|50 - 60|/(5\sqrt{5}) = \frac{2}{\sqrt{5}}$.")],
  r"Here $\vec{b}_1 \times \vec{b}_2 = (2,3,4) \times (1,-1,2) = (10, 0, -5)$ and $\vec{a}_2 - \vec{a}_1 = (3, 2, 6)$. The dot product is $30 + 0 - 30 = 0$. So the shortest distance is $0$; the lines intersect.",
  "Assuming any two lines with different equations must be a positive distance apart.",
  "U11-C-sd-zero", "One triple product that turns out to vanish.",
  check=_c10, values=[0, 7, sqrt(5) / 5, 2 * sqrt(5) / 5], cognitive="Application", source_class="XII")


def _c11():
    b1, b2 = _V(2, 1, -1), _V(1, -1, 1)
    return (_nature((1, 3, -1), b1, (2, -1, 0), b2), bool(simplify(b1.dot(b2)) == 0))
q("U11-C-011", TOP_NAT, "Deciding skew lines", "Easy", "Conceptual/application MCQ",
  r"The lines $\frac{x-1}{2} = \frac{y-3}{1} = \frac{z+1}{-1}$ and $\frac{x-2}{1} = \frac{y+1}{-1} = \frac{z}{1}$ are",
  r"skew and perpendicular",
  [(r"skew but not perpendicular", r"Correctly finds $(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2) = 9 \ne 0$, so the lines are skew, but believes perpendicular lines must meet and so rejects perpendicularity, although $\vec{b}_1 \cdot \vec{b}_2 = 2 - 1 - 1 = 0$."),
   (r"intersecting and perpendicular", r"Solves only the $x$ and $y$ equations $1 + 2s = 2 + t$, $3 + s = -1 - t$ (getting $s = -1$, $t = -3$) and does not check $z$ (which gives $0$ on the first line but $-3$ on the second), so takes the lines as meeting; with $\vec{b}_1 \cdot \vec{b}_2 = 0$ they would then be perpendicular."),
   (r"parallel and distinct", r"Carries over the plane-geometry fact that two lines which never meet are parallel: finds the triple product $9 \ne 0$, so no common point, and concludes parallel and distinct, forgetting that skew lines also never meet.")],
  r"The directions $\vec{b}_1 = (2,1,-1)$ and $\vec{b}_2 = (1,-1,1)$ are not proportional, and $\vec{b}_1 \cdot \vec{b}_2 = 2 - 1 - 1 = 0$, so the lines are perpendicular. Also $\vec{b}_1 \times \vec{b}_2 = (0,-3,-3)$ and $\vec{a}_2 - \vec{a}_1 = (1,-4,1)$ give $0 + 12 - 3 = 9 \ne 0$. So the lines are non-coplanar, that is, skew, and they are perpendicular because the angle between two lines is decided by their directions alone.",
  r"Believing that perpendicular lines in space must intersect, or that non-parallel lines must meet.",
  "U11-C-classify", "Two standard checks: the dot product of the directions, then the triple product.",
  check=_c11, values=[(SKEW, True), (SKEW, False), (INTERSECT, True), (PARALLEL, False)],
  cognitive="Understanding", source_class="XII")


def _c12():
    return _sd((0, 0, 0), (0, 0, 1), (2, -1, 0), (3, 4, -1))
q("U11-C-012", TOP_SD, "Shortest distance from the z-axis", "Easy", "Single-step computation MCQ",
  r"The shortest distance between the $z$-axis and the line $\frac{x-2}{3} = \frac{y+1}{4} = \frac{z}{-1}$ is",
  r"$\frac{11}{5}$",
  [(r"$\sqrt{5}$", r"Gives the distance of the point $(2,-1,0)$ from the $z$-axis, ignoring the direction of the line."),
   (r"$\frac{11\sqrt{26}}{26}$", r"Divides $11$ by $|\vec{b}_2| = \sqrt{26}$ instead of by $|\hat{k} \times \vec{b}_2| = 5$."),
   (r"$1$", r"Takes $\hat{k} \times (3,4,-1)$ as $(4,3,0)$, a sign slip in the first component, so $|8 - 3|/5 = 1$.")],
  r"Write the $z$-axis as $\vec{r} = \lambda\hat{k}$. Then $\hat{k} \times (3,4,-1) = (-4, 3, 0)$, of magnitude $5$. With $\vec{a}_2 - \vec{a}_1 = (2,-1,0)$, the dot product is $-8 - 3 = -11$. So the shortest distance is $\frac{11}{5}$.",
  "Using the distance of one point from the axis, or a sign slip in the cross product.",
  "U11-C-sd-axes", "One cross product with $\\hat{k}$ and one dot product.",
  check=_c12, values=[Rational(11, 5), sqrt(5), 11 * sqrt(26) / 26, 1], cognitive="Application", source_class="XII")


def _c13():
    return _sd((1, -1, 2), (2, -1, 0), (3, 0, 3), (2, 0, -1))
q("U11-C-013", TOP_SD, "Shortest distance, vector form with missing components", "Easy", "Single-step computation MCQ",
  r"The shortest distance between the lines $\vec{r} = (\hat{i} - \hat{j} + 2\hat{k}) + \lambda(2\hat{i} - \hat{j})$ and $\vec{r} = (3\hat{i} + 3\hat{k}) + \mu(2\hat{i} - \hat{k})$ is",
  r"$2$",
  [(r"$6$", r"Stops at $|(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2)| = 6$ without dividing by $|\vec{b}_1 \times \vec{b}_2| = 3$."),
   (r"$\frac{2}{3}$", r"Divides $6$ by $|\vec{b}_1 \times \vec{b}_2|^2 = 9$."),
   (r"$\sqrt{6}$", r"Gives $|\vec{a}_2 - \vec{a}_1| = |2\hat{i} + \hat{j} + \hat{k}| = \sqrt{6}$, the distance between the given points.")],
  r"$\vec{b}_1 \times \vec{b}_2 = (2,-1,0) \times (2,0,-1) = (1, 2, 2)$, of magnitude $3$. With $\vec{a}_2 - \vec{a}_1 = (2, 1, 1)$, the dot product is $2 + 2 + 2 = 6$. So the shortest distance is $\frac{6}{3} = 2$.",
  "Forgetting or squaring the normalising factor.",
  "U11-C-sd-vector", "Direct formula; care with missing components in the cross product.",
  check=_c13, values=[2, 6, Rational(2, 3), sqrt(6)],
  numerical=dict(question=r"The shortest distance between the lines $\vec{r} = (\hat{i} - \hat{j} + 2\hat{k}) + \lambda(2\hat{i} - \hat{j})$ and $\vec{r} = (3\hat{i} + 3\hat{k}) + \mu(2\hat{i} - \hat{k})$ is", answer=2),
  cognitive="Application", source_class="XII")


def _c14():
    s1 = _nature((0, 0, 0), (1, 2, 3), (1, 2, 3), (2, 4, 6)) == COINCIDENT
    s2 = _nature((1, 0, 0), (1, -1, 2), (0, 1, -1), (2, 1, 1)) == INTERSECT
    return (bool(s1), bool(s2))
q("U11-C-014", TOP_NAT, "Coincident and skew lines", "Easy", "Statement-based MCQ",
  r"Statement I: The lines $\frac{x}{1} = \frac{y}{2} = \frac{z}{3}$ and $\frac{x-1}{2} = \frac{y-2}{4} = \frac{z-3}{6}$ are coincident. Statement II: The lines $\frac{x-1}{1} = \frac{y}{-1} = \frac{z}{2}$ and $\frac{x}{2} = \frac{y-1}{1} = \frac{z+1}{1}$ intersect. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II without computing $(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2) = (-1,1,-1)\cdot(-3,3,3) = 3 \ne 0$."),
   (ST_FF, r"Rejects Statement I because the two equations look different, not noticing that $(1,2,3)$ lies on the first line and $(2,4,6) = 2(1,2,3)$."),
   (ST_FT, r"Rejects Statement I by reading proportional direction ratios as merely parallel, and accepts Statement II without the triple-product test.")],
  r"Statement I: $(2,4,6) = 2(1,2,3)$ and $(1,2,3)$ satisfies $\frac{x}{1} = \frac{y}{2} = \frac{z}{3}$, so the lines coincide; true. Statement II: $\vec{b}_1 \times \vec{b}_2 = (1,-1,2) \times (2,1,1) = (-3, 3, 3)$ and $\vec{a}_2 - \vec{a}_1 = (-1, 1, -1)$, so the triple product is $3 + 3 - 3 = 3 \ne 0$. The lines are skew, so Statement II is false.",
  "Judging coincidence or intersection by appearance rather than by the standard tests.",
  "U11-C-statement-nature", "Two short checks, one for each statement.",
  check=_c14, values=[(T_, F_), (T_, T_), (F_, F_), (F_, T_)], cognitive="Understanding", source_class="XII")


# =========================================================== MEDIUM (21)

def _c15():
    return _sd((1, 2, 3), (1, 1, 1), (4, 3, 2), (1, -1, 1))**2
q("U11-C-015", TOP_SD, "Square of shortest distance", "Medium", "Multi-step computation MCQ",
  r"If $d$ is the shortest distance between the lines $\frac{x-1}{1} = \frac{y-2}{1} = \frac{z-3}{1}$ and $\frac{x-4}{1} = \frac{y-3}{-1} = \frac{z-2}{1}$, then $d^2$ equals",
  r"$8$",
  [(r"$2$", r"Reduces $\vec{b}_1 \times \vec{b}_2 = (2,0,-2)$ to $(1,0,-1)$ for the dot product (getting $4$) but divides by $|(2,0,-2)| = 2\sqrt{2}$, so $d = \sqrt{2}$."),
   (r"$1$", r"Divides $8$ by $|\vec{b}_1 \times \vec{b}_2|^2 = 8$, so $d = 1$."),
   (r"$11$", r"Squares $|\vec{a}_2 - \vec{a}_1| = |(3,1,-1)| = \sqrt{11}$, the distance between the given points.")],
  r"$\vec{b}_1 \times \vec{b}_2 = (1,1,1) \times (1,-1,1) = (2, 0, -2)$, with magnitude $2\sqrt{2}$. With $\vec{a}_2 - \vec{a}_1 = (3, 1, -1)$, the dot product is $6 + 0 + 2 = 8$. So $d = \frac{8}{2\sqrt{2}} = 2\sqrt{2}$ and $d^2 = 8$.",
  "Inconsistent scaling of the normal vector between numerator and denominator.",
  "U11-C-sd-cartesian", "Cross product, dot product, simplification of a surd and squaring.",
  check=_c15, values=[8, 2, 1, 11],
  numerical=dict(question=r"If $d$ is the shortest distance between the lines $\frac{x-1}{1} = \frac{y-2}{1} = \frac{z-3}{1}$ and $\frac{x-4}{1} = \frac{y-3}{-1} = \frac{z-2}{1}$, then the value of $d^2$ is", answer=8),
  cognitive="Application", source_class="XII")


def _c16():
    lam = Symbol('lam')
    sol = solve(_V(1, 2, lam).dot(_V(2, -2, 1)), lam)
    assert len(sol) == 1
    L = sol[0]
    assert _nature((1, -1, 2), (1, 2, L), (2, 1, 1), (2, -2, 1)) == SKEW
    return _sd((1, -1, 2), (1, 2, L), (2, 1, 1), (2, -2, 1))
q("U11-C-016", TOP_SD, "Shortest distance after a perpendicularity condition", "Medium", "Multi-step computation MCQ",
  r"If the lines $\frac{x-1}{1} = \frac{y+1}{2} = \frac{z-2}{\lambda}$ and $\frac{x-2}{2} = \frac{y-1}{-2} = \frac{z-1}{1}$ are perpendicular, then the shortest distance between them is",
  r"$2$",
  [(r"$\frac{6\sqrt{65}}{65}$", r"Solves $2 - 4 + \lambda = 0$ as $\lambda = -2$; then $\vec{b}_1 \times \vec{b}_2 = (-2,-5,-6)$ of magnitude $\sqrt{65}$ and $(1,2,-1)\cdot(-2,-5,-6) = -6$, giving $\frac{6}{\sqrt{65}}$."),
   (r"$\sqrt{6}$", r"Finds $\lambda = 2$ but then gives $|\vec{a}_2 - \vec{a}_1| = |(1,2,-1)| = \sqrt{6}$, the distance between the two given points, not the shortest distance."),
   (r"$\frac{2}{9}$", r"Finds $\lambda = 2$ and the triple product $18$ but divides by $|\vec{b}_1 \times \vec{b}_2|^2 = 81$ instead of by $9$.")],
  r"Perpendicular lines need $\vec{b}_1 \cdot \vec{b}_2 = 0$: $(1)(2) + (2)(-2) + \lambda(1) = 0$, so $\lambda = 2$. Then $\vec{b}_1 \times \vec{b}_2 = (1,2,2) \times (2,-2,1) = (6, 3, -6)$, of magnitude $9$. With $\vec{a}_2 - \vec{a}_1 = (1, 2, -1)$, the triple product is $6 + 6 + 6 = 18 \ne 0$, so the lines are skew and the shortest distance is $\frac{18}{9} = 2$.",
  r"Assuming perpendicular lines must intersect, or mishandling the normalising factor $|\vec{b}_1 \times \vec{b}_2|$.",
  "U11-C-perp-param-sd", r"Two ideas: a dot-product condition fixes $\lambda$, then the skew-line distance formula.",
  check=_c16, values=[2, 6 * sqrt(65) / 65, sqrt(6), Rational(2, 9)],
  numerical=dict(question=r"If the lines $\frac{x-1}{1} = \frac{y+1}{2} = \frac{z-2}{\lambda}$ and $\frac{x-2}{2} = \frac{y-1}{-2} = \frac{z-1}{1}$ are perpendicular, then the shortest distance between them is", answer=2),
  cognitive="Application", source_class="XII")


def _c17():
    k = Symbol('k', real=True)
    tp = _det3(_V(-1, 0, 2) - _V(1, -2, k), (2, 3, -1), (1, -1, 2))
    bad = solveset(tp, k, S.Reals)
    assert _V(2, 3, -1).cross(_V(1, -1, 2)).norm() != 0
    return Complement(S.Reals, bad)
q("U11-C-017", TOP_NAT, "Set of parameter values for skew lines", "Medium", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which the lines $\frac{x-1}{2} = \frac{y+2}{3} = \frac{z-k}{-1}$ and $\frac{x+1}{1} = \frac{y}{-1} = \frac{z-2}{2}$ are skew is",
  r"$\mathbb{R} - \{6\}$",
  [(r"$\{6\}$", r"Gives the value where the triple product vanishes, which is where the lines intersect, not where they are skew."),
   (r"$\mathbb{R} - \{-6\}$", r"Reads the point of the first line as $(1,-2,-k)$, so the triple product becomes $-30 - 5k$ and vanishes at $k = -6$."),
   (r"$\mathbb{R}$", r"Assumes that lines with non-parallel directions are always skew, forgetting that they may intersect.")],
  r"The directions $(2,3,-1)$ and $(1,-1,2)$ are not parallel, and $\vec{b}_1 \times \vec{b}_2 = (5, -5, -5)$. With $\vec{a}_2 - \vec{a}_1 = (-2, 2, 2-k)$, the triple product is $-10 - 10 - 5(2 - k) = 5k - 30$. The lines are skew exactly when this is non-zero, i.e. for $k \ne 6$.",
  "Mixing up the skew condition with the intersection condition.",
  "U11-C-skew-set", "Triple product with a parameter, then interpreting the condition as a set.",
  check=_c17, values=[Complement(S.Reals, FiniteSet(6)), FiniteSet(6), Complement(S.Reals, FiniteSet(-6)), S.Reals],
  cognitive="Analysis", source_class="XII")


def _c18():
    lam = Symbol('lam', real=True)
    a1, b1, a2, b2 = _V(lam, 1, -1), _V(2, -2, 1), _V(1, -2, 3), _V(2, 1, -2)
    n = b1.cross(b2)
    sols = solveset(Eq(((a2 - a1).dot(n))**2 / n.dot(n), 4), lam, S.Reals)
    assert len(sols) == 2
    return Mul(*list(sols))
q("U11-C-018", TOP_SD, "Parameter from a given shortest distance", "Medium", "Inverse/parameter MCQ",
  r"If the shortest distance between the lines $\frac{x-\lambda}{2} = \frac{y-1}{-2} = \frac{z+1}{1}$ and $\frac{x-1}{2} = \frac{y+2}{1} = \frac{z-3}{-2}$ is $2$, then the product of all possible values of $\lambda$ is",
  r"$-27$",
  [(r"$5$", r"Sets $|3 - \lambda| = 2$, forgetting to divide by $|\vec{b}_1 \times \vec{b}_2|$ (with the normal reduced to $(1,2,2)$), giving $\lambda = 1, 5$."),
   (r"$-9$", r"Squares the left side of $\frac{|3 - \lambda|}{3} = 2$ but not the right, writing $\frac{(3 - \lambda)^2}{9} = 2$, so $\lambda^2 - 6\lambda - 9 = 0$."),
   (r"$-315$", r"Divides $|3 - \lambda|$ by $|(1,2,2)|^2 = 9$ instead of by $3$, so $|3 - \lambda| = 18$ and $\lambda = -15, 21$.")],
  r"$\vec{b}_1 \times \vec{b}_2 = (2,-2,1) \times (2,1,-2) = (3, 6, 6) = 3(1,2,2)$, so use the unit normal $\frac{1}{3}(1,2,2)$. With $\vec{a}_2 - \vec{a}_1 = (1-\lambda, -3, 4)$, the distance is $\frac{|1 - \lambda - 6 + 8|}{3} = \frac{|3 - \lambda|}{3}$. Setting this equal to $2$ gives $\lambda = -3$ or $\lambda = 9$, whose product is $-27$.",
  "Dropping the denominator or mishandling the absolute value when the distance is given.",
  "U11-C-sd-inverse-skew", "Reverse use of the distance formula with an absolute value giving two roots.",
  check=_c18, values=[-27, 5, -9, -315], cognitive="Application", source_class="XII")


def _c19():
    # x = 2y = 3z ; x - 2 = 2(y+1) = 3(z+1); direction (1, 1/2, 1/3)
    b = _V(1, Rational(1, 2), Rational(1, 3))
    return _sd((0, 0, 0), b, (2, -1, -1), b)
q("U11-C-019", TOP_PAR, "Parallel lines in equal-ratio form", "Medium", "Multi-step computation MCQ",
  r"The distance between the parallel lines $x = 2y = 3z$ and $x - 2 = 2(y + 1) = 3(z + 1)$ is",
  r"$\sqrt{5}$",
  [(r"$\sqrt{6}$", r"Takes the distance between the visible points $(0,0,0)$ and $(2,-1,-1)$ as the distance between the lines."),
   (r"$\frac{5\sqrt{42}}{14}$", r"Reads the direction ratios as $(1,2,3)$ from the coefficients: $|(2,-1,-1) \times (1,2,3)| = 5\sqrt{3}$, divided by $\sqrt{14}$."),
   (r"$\frac{\sqrt{5}}{7}$", r"Divides $|(2,-1,-1) \times (6,3,2)| = 7\sqrt{5}$ by $|\vec{b}|^2 = 49$ instead of by $7$.")],
  r"Writing $x = 2y = 3z = t$ gives the direction $(1, \frac{1}{2}, \frac{1}{3})$, i.e. $(6, 3, 2)$ with magnitude $7$. The second line passes through $(2, -1, -1)$ with the same direction. Then $(2,-1,-1) \times (6,3,2) = (1, -10, 12)$, of magnitude $\sqrt{245} = 7\sqrt{5}$. So the distance is $\frac{7\sqrt{5}}{7} = \sqrt{5}$.",
  "Taking the coefficients in $x = 2y = 3z$ as direction ratios instead of their reciprocals.",
  "U11-C-chain-form", "Conversion from equal-ratio form, then the parallel-line distance formula.",
  check=_c19, values=[sqrt(5), sqrt(6), 5 * sqrt(42) / 14, sqrt(5) / 7], cognitive="Application", source_class="XII")


def _c20():
    return _sd((1, 2, -1), (-2, 3, 1), (6, 4, -1), (1, -1, 1))
q("U11-C-020", TOP_SD, "Shortest distance with a non-standard form", "Medium", "Multi-step computation MCQ",
  r"The shortest distance between the lines $\frac{1-x}{2} = \frac{y-2}{3} = \frac{z+1}{1}$ and $\frac{x-6}{1} = \frac{y-4}{-1} = \frac{z+1}{1}$ is",
  r"$\sqrt{26}$",
  [(r"$\frac{3\sqrt{42}}{7}$", r"Takes the direction of the first line as $(2,3,1)$, ignoring the sign in $1 - x$: $\vec{b}_1 \times \vec{b}_2 = (4,-1,-5)$ and $\frac{|20 - 2|}{\sqrt{42}}$."),
   (r"$26$", r"Stops at $|(\vec{a}_2 - \vec{a}_1)\cdot(\vec{b}_1 \times \vec{b}_2)| = 26$ without dividing by $\sqrt{26}$."),
   (r"$\frac{17\sqrt{26}}{13}$", r"Reads the point of the first line as $(-1, 2, -1)$, so $\vec{a}_2 - \vec{a}_1 = (7,2,0)$ and $\frac{|28 + 6|}{\sqrt{26}} = \frac{34}{\sqrt{26}}$.")],
  r"Rewrite the first line as $\frac{x-1}{-2} = \frac{y-2}{3} = \frac{z+1}{1}$: point $(1,2,-1)$, direction $(-2,3,1)$. Then $\vec{b}_1 \times \vec{b}_2 = (-2,3,1) \times (1,-1,1) = (4, 3, -1)$, magnitude $\sqrt{26}$. With $\vec{a}_2 - \vec{a}_1 = (5, 2, 0)$, the dot product is $20 + 6 = 26$. So the distance is $\frac{26}{\sqrt{26}} = \sqrt{26}$.",
  "Not converting $\\frac{1-x}{2}$ to $\\frac{x-1}{-2}$ before reading the direction ratios and the point.",
  "U11-C-sd-nonstandard", "Rewriting to standard form is a trap, followed by the full skew-line computation.",
  check=_c20, values=[sqrt(26), 3 * sqrt(42) / 7, 26, 17 * sqrt(26) / 13], cognitive="Application", source_class="XII")


def _c21():
    P, Q = _feet((0, 0, 0), (1, 0, 0), (1, 2, 3), (1, -1, 1))
    return tuple(P)
q("U11-C-021", TOP_LSD, "Foot of the common perpendicular on an axis", "Medium", "Multi-step computation MCQ",
  r"The line of shortest distance between the $x$-axis and the line $\frac{x-1}{1} = \frac{y-2}{-1} = \frac{z-3}{1}$ meets the $x$-axis at the point",
  r"$\left(\frac{1}{2}, 0, 0\right)$",
  [(r"$(1, 0, 0)$", r"Drops the perpendicular from the given point $(1,2,3)$ to the $x$-axis, which is not perpendicular to the second line."),
   (r"$\left(\frac{3}{2}, 0, 0\right)$", r"Solves $1 + 2t = 0$ as $t = \frac{1}{2}$ (sign slip), then $s = 1 + t = \frac{3}{2}$."),
   (r"$\left(-\frac{1}{2}, 0, 0\right)$", r"Writes the general point of the second line with $x = t$ instead of $1 + t$, getting $s = t = -\frac{1}{2}$.")],
  r"Let $P = (s, 0, 0)$ and $Q = (1 + t, 2 - t, 3 + t)$. Then $\overrightarrow{PQ} = (1 + t - s, 2 - t, 3 + t)$. Perpendicularity to $\hat{i}$ gives $1 + t - s = 0$; perpendicularity to $(1,-1,1)$ gives $(1 + t - s) - (2 - t) + (3 + t) = 0$, i.e. $1 + 2t = 0$. So $t = -\frac{1}{2}$, $s = \frac{1}{2}$, and the line of shortest distance meets the $x$-axis at $\left(\frac{1}{2}, 0, 0\right)$.",
  "Assuming the common perpendicular passes through the given point of the line.",
  "U11-C-sd-feet", "Two perpendicularity conditions solved simultaneously.",
  check=_c21, values=[(Rational(1, 2), 0, 0), (1, 0, 0), (Rational(3, 2), 0, 0), (Rational(-1, 2), 0, 0)],
  cognitive="Application", source_class="XII")


def _c22():
    P, Q, R, S_ = _V(1, 2, 1), _V(3, 1, 3), _V(0, 5, 3), _V(2, 7, 2)
    return _sd(P, Q - P, R, S_ - R)
q("U11-C-022", TOP_SD, "Lines through two given points", "Medium", "Multi-step computation MCQ",
  r"The shortest distance between the line through $P(1, 2, 1)$ and $Q(3, 1, 3)$ and the line through $R(0, 5, 3)$ and $S(2, 7, 2)$ is",
  r"$\frac{11}{3}$",
  [(r"$\sqrt{14}$", r"Gives $PR = |(-1, 3, 2)| = \sqrt{14}$, the distance between two chosen points."),
   (r"$\frac{11}{27}$", r"Divides $|\overrightarrow{PR}\cdot(\overrightarrow{PQ} \times \overrightarrow{RS})| = 33$ by $|\overrightarrow{PQ} \times \overrightarrow{RS}|^2 = 81$."),
   (r"$\frac{3\sqrt{2}}{2}$", r"Uses $\overrightarrow{PS} = (1,5,1)$ as the second direction: $(2,-1,2) \times (1,5,1) = (-11,0,11)$ and $\frac{33}{11\sqrt{2}}$.")],
  r"Directions: $\overrightarrow{PQ} = (2,-1,2)$ and $\overrightarrow{RS} = (2,2,-1)$. Their cross product is $(-3, 6, 6)$, of magnitude $9$. With $\overrightarrow{PR} = (-1, 3, 2)$, the dot product is $3 + 18 + 12 = 33$. So the shortest distance is $\frac{33}{9} = \frac{11}{3}$.",
  "Choosing the wrong pair of points for the direction vectors, or wrong normalisation.",
  "U11-C-sd-two-points", "Form both directions from points, then apply the skew-line formula.",
  check=_c22, values=[Rational(11, 3), sqrt(14), Rational(11, 27), 3 * sqrt(2) / 2], cognitive="Application", source_class="XII")


def _c23():
    s1 = _nature((0, 0, 0), (1, 1, 1), (1, 2, 2), (0, 1, 1)) == SKEW
    s2 = _sd((1, -1, 0), (2, -1, 2), (4, -2, 3), (4, -2, 4)) == sqrt(2) / 3
    return (bool(s1), bool(s2))
q("U11-C-023", TOP_NAT, "Statements on nature and distance", "Medium", "Statement-based MCQ",
  r"Statement I: The lines $x = y = z$ and $\frac{x-1}{0} = \frac{y-2}{1} = \frac{z-2}{1}$ are skew. Statement II: The distance between the lines $\frac{x-1}{2} = \frac{y+1}{-1} = \frac{z}{2}$ and $\frac{x-4}{4} = \frac{y+2}{-2} = \frac{z-3}{4}$ is $\frac{\sqrt{2}}{3}$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I because the direction ratios differ, without computing the triple product $(1,2,2)\cdot(0,-1,1) = 0$."),
   (ST_FF, r"Rejects Statement II by using $|\vec{a}_2 - \vec{a}_1| = |(3,-1,3)| = \sqrt{19}$ as the distance between the parallel lines."),
   (ST_TF, r"Combines both slips: assumes non-parallel means skew, and uses the distance between the given points for the parallel lines.")],
  r"Statement I: $\vec{b}_1 \times \vec{b}_2 = (1,1,1) \times (0,1,1) = (0, -1, 1)$ and $\vec{a}_2 - \vec{a}_1 = (1, 2, 2)$; the triple product is $-2 + 2 = 0$, so the lines intersect (at $(1,1,1)$). Statement I is false. Statement II: the lines are parallel with $\vec{b} = (2,-1,2)$, $|\vec{b}| = 3$; with $\vec{a}_2 - \vec{a}_1 = (3,-1,3)$, $|\vec{a}_2 - \vec{a}_1|^2 = 19$ and $(\vec{a}_2 - \vec{a}_1)\cdot\vec{b} = 13$, so $d^2 = 19 - \frac{169}{9} = \frac{2}{9}$ and $d = \frac{\sqrt{2}}{3}$. Statement II is true.",
  "Assuming non-parallel lines are skew; using point-to-point distance for parallel lines.",
  "U11-C-statement-nature", "Two independent computations, one per statement.",
  check=_c23, values=[(F_, T_), (T_, T_), (F_, F_), (T_, F_)], cognitive="Analysis", source_class="XII")


def _c24():
    # x = y + 1, z = y - 1 : point (1,0,-1), dir (1,1,1); x = -y + 3, z = y + 2 : point (3,0,2), dir (-1,1,1)
    return _sd((1, 0, -1), (1, 1, 1), (3, 0, 2), (-1, 1, 1))
q("U11-C-024", TOP_SD, "Lines given as x = ay + b, z = cy + d", "Medium", "Multi-step computation MCQ",
  r"The shortest distance between the lines $x = y + 1,\ z = y - 1$ and $x = -y + 3,\ z = y + 2$ is",
  r"$\frac{3\sqrt{2}}{2}$",
  [(r"$3$", r"Computes the triple product $6$ correctly but takes $|(0,-2,2)|$ as $2$."),
   (r"$\sqrt{13}$", r"Gives the distance between the points $(1,0,-1)$ and $(3,0,2)$, which is $\sqrt{4 + 0 + 9}$."),
   (r"$3\sqrt{2}$", r"Reduces the normal to $(0,-1,1)$ for the denominator ($\sqrt{2}$) but keeps the triple product $6$ from $(0,-2,2)$.")],
  r"Put $y = t$: the first line is $(1 + t, t, -1 + t)$, through $(1,0,-1)$ with direction $(1,1,1)$; the second is $(3 - t, t, 2 + t)$, through $(3,0,2)$ with direction $(-1,1,1)$. Then $\vec{b}_1 \times \vec{b}_2 = (0, -2, 2)$, magnitude $2\sqrt{2}$, and $\vec{a}_2 - \vec{a}_1 = (2, 0, 3)$ gives the dot product $0 + 0 + 6 = 6$. So the distance is $\frac{6}{2\sqrt{2}} = \frac{3\sqrt{2}}{2}$.",
  "Mismatching the scale of the normal vector between numerator and denominator.",
  "U11-C-sd-xay-form", "Conversion to parametric form, then the skew-line formula.",
  check=_c24, values=[3 * sqrt(2) / 2, 3, sqrt(13), 3 * sqrt(2)], cognitive="Application", source_class="XII")


def _c25():
    k = Symbol('k')
    a1, a2 = _V(1, 2, 3), _V(1, 3, 4)
    b1, b2 = _V(k, 2, 1), _V(1, k, 2)
    roots = solve(_det3(a2 - a1, b1, b2), k)
    good = [r for r in roots if simplify(b1.subs(k, r).cross(b2.subs(k, r)).norm()) != 0]
    return simplify(sum(r**2 for r in good))
q("U11-C-025", TOP_INT, "Quadratic condition for intersection", "Medium", "Inverse/parameter MCQ",
  r"If the lines $\frac{x-1}{k} = \frac{y-2}{2} = \frac{z-3}{1}$ and $\frac{x-1}{1} = \frac{y-3}{k} = \frac{z-4}{2}$ intersect, then the sum of the squares of all possible real values of $k$ is",
  r"$6$",
  [(r"$10$", r"Expands the determinant with a $+$ sign on the middle cofactor, getting $k^2 + 2k - 3 = 0$ with roots $1, -3$."),
   (r"$2$", r"Uses $(k_1 + k_2)^2 + 2k_1k_2 = 4 - 2$ instead of $(k_1 + k_2)^2 - 2k_1k_2$."),
   (r"$4$", r"Reports $(k_1 + k_2)^2 = 4$, omitting the $-2k_1k_2$ term.")],
  r"With $\vec{a}_2 - \vec{a}_1 = (0, 1, 1)$, the coplanarity condition is $\begin{vmatrix} 0 & 1 & 1 \\ k & 2 & 1 \\ 1 & k & 2 \end{vmatrix} = -(2k - 1) + (k^2 - 2) = k^2 - 2k - 1 = 0$. The directions $(k,2,1)$ and $(1,k,2)$ are never parallel (that would need $k = \frac{1}{2}$ and $k = 4$ together), so both roots give intersecting lines. Then $k_1^2 + k_2^2 = (k_1 + k_2)^2 - 2k_1k_2 = 4 + 2 = 6$.",
  "Cofactor sign errors and wrong symmetric-function identity.",
  "U11-C-coplanar-quadratic", "Determinant giving a quadratic, a parallel-case check, then Vieta.",
  check=_c25, values=[6, 10, 2, 4],
  numerical=dict(question=r"If the lines $\frac{x-1}{k} = \frac{y-2}{2} = \frac{z-3}{1}$ and $\frac{x-1}{1} = \frac{y-3}{k} = \frac{z-4}{2}$ intersect, then the sum of the squares of all possible real values of $k$ is", answer=6),
  cognitive="Application", source_class="XII")


def _c26():
    k = Symbol('k', real=True)
    roots = solveset(Eq(_sd((3, -1, 1), (1, 2, 2), (k, 1, 1), (1, 2, 2))**2, 4), k, S.Reals)
    return sum(roots)
q("U11-C-026", TOP_PAR, "Parameter from distance between parallel lines", "Medium", "Inverse/parameter MCQ",
  r"If the distance between the parallel lines $\frac{x-3}{1} = \frac{y+1}{2} = \frac{z-1}{2}$ and $\frac{x-k}{1} = \frac{y-1}{2} = \frac{z-1}{2}$ is $2$, then the sum of all possible values of $k$ is",
  r"$7$",
  [(r"$3$", r"Sets the distance between the points $(3,-1,1)$ and $(k,1,1)$ equal to $2$, giving only $k = 3$."),
   (r"$-2$", r"Uses the projection $\frac{|(\vec{a}_2 - \vec{a}_1)\cdot\vec{b}|}{|\vec{b}|} = \frac{|k + 1|}{3} = 2$, giving $k = 5, -7$."),
   (r"$10$", r"Uses $d^2 = |\vec{a}_2 - \vec{a}_1|^2 - \frac{((\vec{a}_2 - \vec{a}_1)\cdot\vec{b})^2}{|\vec{b}|}$, dividing by $3$ instead of $9$, which gives $k^2 - 10k + 13 = 0$.")],
  r"Here $\vec{a}_2 - \vec{a}_1 = (k - 3, 2, 0)$ and $\vec{b} = (1,2,2)$ with $|\vec{b}| = 3$. Then $d^2 = |\vec{a}_2 - \vec{a}_1|^2 - \frac{((\vec{a}_2 - \vec{a}_1)\cdot\vec{b})^2}{9} = (k-3)^2 + 4 - \frac{(k+1)^2}{9}$. Setting $d^2 = 4$: $9(k-3)^2 = (k+1)^2$, so $3(k - 3) = \pm(k + 1)$, giving $k = 5$ or $k = 2$. The sum is $7$.",
  "Using the point-to-point distance or the projection along the line instead of the perpendicular distance.",
  "U11-C-sd-parallel-inverse", "Distance formula for parallel lines used in reverse, with two roots.",
  check=_c26, values=[7, 3, -2, 10],
  numerical=dict(question=r"If the distance between the parallel lines $\frac{x-3}{1} = \frac{y+1}{2} = \frac{z-1}{2}$ and $\frac{x-k}{1} = \frac{y-1}{2} = \frac{z-1}{2}$ is $2$, then the sum of all possible values of $k$ is", answer=7),
  cognitive="Application", source_class="XII")


def _c27():
    return _sd((0, 0, 0), (6, 6, 6), (6, 0, 0), (0, 6, 0))
q("U11-C-027", TOP_SD, "Cube: diagonal and a skew edge", "Medium", "Multi-step computation MCQ",
  r"A cube has edge $6$ with one vertex at the origin and three edges along the positive coordinate axes. The shortest distance between the diagonal joining $(0,0,0)$ to $(6,6,6)$ and the edge joining $(6,0,0)$ to $(6,6,0)$ is",
  r"$3\sqrt{2}$",
  [(r"$6$", r"Stops at $|(6,0,0)\cdot(-1,0,1)| = 6$ without dividing by $|(1,1,1) \times (0,1,0)| = \sqrt{2}$."),
   (r"$3$", r"Divides $6$ by $|(-1,0,1)|^2 = 2$ instead of by $\sqrt{2}$."),
   (r"$2\sqrt{3}$", r"Divides $6$ by $|(1,1,1)| = \sqrt{3}$, the length of the diagonal direction, instead of by $|\vec{b}_1 \times \vec{b}_2|$.")],
  r"Take the diagonal as $\vec{r} = \lambda(1,1,1)$ and the edge as $\vec{r} = (6,0,0) + \mu(0,1,0)$. Then $(1,1,1) \times (0,1,0) = (-1, 0, 1)$, magnitude $\sqrt{2}$. With $\vec{a}_2 - \vec{a}_1 = (6,0,0)$, the dot product is $-6$. So the shortest distance is $\frac{6}{\sqrt{2}} = 3\sqrt{2}$.",
  "Wrong normalising factor in the skew-line formula.",
  "U11-C-cube", "Setting up the lines from the solid, then the skew-line formula.",
  check=_c27, values=[3 * sqrt(2), 6, 3, 2 * sqrt(3)], cognitive="Application", source_class="XII")


def _c28():
    return _sd((0, 0, 0), (3, 3, 0), (3, 0, 0), (0, 3, 3))
q("U11-C-028", TOP_SD, "Cube: skew face diagonals", "Medium", "Multi-step computation MCQ",
  r"A cube has edge $3$ with one vertex at the origin and three edges along the positive coordinate axes. The shortest distance between the face diagonal joining $(0,0,0)$ to $(3,3,0)$ and the face diagonal joining $(3,0,0)$ to $(3,3,3)$ is",
  r"$\sqrt{3}$",
  [(r"$3$", r"Stops at $|(3,0,0)\cdot(1,-1,1)| = 3$ without dividing by $\sqrt{3}$."),
   (r"$1$", r"Divides $3$ by $|(1,-1,1)|^2 = 3$ instead of by $\sqrt{3}$."),
   (r"$\frac{3\sqrt{2}}{2}$", r"Divides $3$ by $|(1,1,0)| = \sqrt{2}$, the magnitude of one direction, instead of by $|\vec{b}_1 \times \vec{b}_2|$.")],
  r"Directions: $(1,1,0)$ and $(0,1,1)$, with cross product $(1, -1, 1)$ of magnitude $\sqrt{3}$. With $\vec{a}_2 - \vec{a}_1 = (3, 0, 0)$, the dot product is $3$. So the shortest distance is $\frac{3}{\sqrt{3}} = \sqrt{3}$.",
  "Wrong normalising factor in the skew-line formula.",
  "U11-C-cube", "Reading the lines off a solid and applying the formula.",
  check=_c28, values=[sqrt(3), 3, 1, 3 * sqrt(2) / 2], cognitive="Application", source_class="XII")


def _c29():
    O = _V(0, 0, 0)
    return _sd(O, _V(1, 2, 0) - O, _V(0, 0, 3), _V(1, 0, 0) - _V(0, 0, 3))
q("U11-C-029", TOP_SD, "Cuboid: skew face diagonals", "Medium", "Multi-step computation MCQ",
  r"A rectangular box has one vertex at the origin $O$ and edges of lengths $1, 2, 3$ along the positive $x$-, $y$- and $z$-axes. The shortest distance between the diagonal of the bottom face joining $O$ to $(1,2,0)$ and the diagonal of the face $y = 0$ joining $(0,0,3)$ to $(1,0,0)$ is",
  r"$\frac{6}{7}$",
  [(r"$\frac{3\sqrt{2}}{5}$", r"Divides the triple product $6$ by $|\vec{b}_1|\,|\vec{b}_2| = \sqrt{5}\cdot\sqrt{10} = 5\sqrt{2}$ instead of by $|\vec{b}_1 \times \vec{b}_2| = 7$."),
   (r"$3$", r"Takes the separation $|(0,0,3) - (0,0,0)| = 3$ of the two chosen points, the height of the box, as the shortest distance."),
   (r"$6$", r"Stops at $|(0,0,3)\cdot(-6,3,-2)| = 6$ without dividing by $|\vec{b}_1 \times \vec{b}_2| = 7$.")],
  r"The first diagonal is $\vec{r} = \lambda(1,2,0)$ and the second is $\vec{r} = (0,0,3) + \mu(1,0,-3)$. They share no vertex and are not parallel. Then $(1,2,0) \times (1,0,-3) = (-6, 3, -2)$, of magnitude $\sqrt{36 + 9 + 4} = 7$. With $\vec{a}_2 - \vec{a}_1 = (0,0,3)$, the dot product is $-6$. So the shortest distance is $\frac{6}{7}$.",
  "Normalising by the product of the lengths of the directions instead of the length of their cross product.",
  "U11-C-cube", "Reading two face diagonals off a box, a cross product, then the skew-line formula.",
  check=_c29, values=[Rational(6, 7), 3 * sqrt(2) / 5, 3, 6], cognitive="Application", source_class="XII")


def _c30():
    P, Q = _V(2, -1, 1), _V(3, 1, 1)
    return _sd(P, Q - P, (6, 0, 2), (0, 2, 1))
q("U11-C-030", TOP_SD, "Mixed forms: two points and vector form", "Medium", "Multi-step computation MCQ",
  r"$L_1$ is the line through $P(2, -1, 1)$ and $Q(3, 1, 1)$, and $L_2$ is $\vec{r} = (6\hat{i} + 2\hat{k}) + \mu(2\hat{j} + \hat{k})$. The shortest distance between $L_1$ and $L_2$ is",
  r"$3$",
  [(r"$9$", r"Stops at the triple product $|(4,1,1)\cdot(2,-1,2)| = 9$ without dividing by $3$."),
   (r"$1$", r"Divides $9$ by $|(2,-1,2)|^2 = 9$."),
   (r"$3\sqrt{2}$", r"Gives the distance from $P$ to the point $(6,0,2)$ of $L_2$, which is $|(4,1,1)| = 3\sqrt{2}$.")],
  r"$L_1$ has direction $\overrightarrow{PQ} = (1, 2, 0)$ and $L_2$ has direction $(0, 2, 1)$. Their cross product is $(2, -1, 2)$, magnitude $3$. With $(6,0,2) - (2,-1,1) = (4, 1, 1)$, the dot product is $8 - 1 + 2 = 9$. So the shortest distance is $\frac{9}{3} = 3$.",
  "Forgetting or squaring the normalising factor.",
  "U11-C-sd-two-points", "Combine two different line descriptions, then apply the formula.",
  check=_c30, values=[3, 9, 1, 3 * sqrt(2)],
  numerical=dict(question=r"$L_1$ is the line through $P(2, -1, 1)$ and $Q(3, 1, 1)$, and $L_2$ is $\vec{r} = (6\hat{i} + 2\hat{k}) + \mu(2\hat{j} + \hat{k})$. The shortest distance between $L_1$ and $L_2$ is", answer=3),
  cognitive="Application", source_class="XII")


def _c31():
    k = Symbol('k')
    b1, b2 = _V(2, k, 4), _V(1, 2, 2)
    kk = solve(b1.cross(b2), k, dict=True)[0][k]
    return _sd((1, 2, 3), b1.subs(k, kk), (4, 2, 3), b2)
q("U11-C-031", TOP_PAR, "Parameter for parallel lines, then distance", "Medium", "Multi-step computation MCQ",
  r"The lines $\frac{x-1}{2} = \frac{y-2}{k} = \frac{z-3}{4}$ and $\frac{x-4}{1} = \frac{y-2}{2} = \frac{z-3}{2}$ are parallel. The distance between them is",
  r"$2\sqrt{2}$",
  [(r"$3$", r"Gives the distance between the points $(1,2,3)$ and $(4,2,3)$, which is $3$."),
   (r"$\sqrt{2}$", r"Computes $|(3,0,0) \times (1,2,2)| = 6\sqrt{2}$ but divides by $|(2,4,4)| = 6$."),
   (r"$1$", r"Computes the projection $\frac{|(3,0,0)\cdot(1,2,2)|}{3} = 1$ along the lines instead of the perpendicular distance.")],
  r"Parallelism forces $(2, k, 4) = 2(1, 2, 2)$, so $k = 4$. Take $\vec{b} = (1,2,2)$ with $|\vec{b}| = 3$ and $\vec{a}_2 - \vec{a}_1 = (3, 0, 0)$. Then $(3,0,0) \times (1,2,2) = (0, -6, 6)$, magnitude $6\sqrt{2}$. The distance is $\frac{6\sqrt{2}}{3} = 2\sqrt{2}$.",
  "Using the projection or the point-to-point distance instead of the perpendicular distance.",
  "U11-C-parallel-param", "Find the parameter from parallelism, then the parallel-line distance.",
  check=_c31, values=[2 * sqrt(2), 3, sqrt(2), 1], cognitive="Application", source_class="XII")


def _c32():
    b1 = _V(3, -1, 2) - _V(1, 0, 2)
    n = b1.cross(_V(0, 1, -1))
    if n[2] < 0:
        n = -n
    return simplify(sum(n) / n.norm())
q("U11-C-032", TOP_LSD, "Direction cosines of the common perpendicular", "Medium", "Multi-step computation MCQ",
  r"$L_1$ is the line through $(1, 0, 2)$ and $(3, -1, 2)$, and $L_2$ is $\vec{r} = (\hat{i} - 2\hat{j} + \hat{k}) + \mu(\hat{j} - \hat{k})$. A line perpendicular to both $L_1$ and $L_2$ makes angles $\alpha, \beta, \gamma$ with the positive $x$-, $y$- and $z$-axes, where $\gamma$ is acute. Then $\cos\alpha + \cos\beta + \cos\gamma$ equals",
  r"$\frac{5}{3}$",
  [(r"$\frac{1}{3}$", r"Drops the minus sign in the middle component of $\vec{b}_1 \times \vec{b}_2$, getting $(1,-2,2)$ and direction cosines $\frac{1}{3}, -\frac{2}{3}, \frac{2}{3}$."),
   (r"$1$", r"Writes the first component of the cross product as $(-1)(-1) - 0 \cdot 1$ with the wrong sign, $-1$, getting $(-1,2,2)$ and direction cosines $-\frac{1}{3}, \frac{2}{3}, \frac{2}{3}$."),
   (r"$\frac{5}{9}$", r"Divides $(1,2,2)$ by $|\vec{n}|^2 = 9$ instead of by $|\vec{n}| = 3$ when converting direction ratios to direction cosines.")],
  r"$L_1$ has direction $(3,-1,2) - (1,0,2) = (2, -1, 0)$ and $L_2$ has direction $(0, 1, -1)$. A common perpendicular is along $(2,-1,0) \times (0,1,-1) = \left((-1)(-1) - 0 \cdot 1,\ 0 \cdot 0 - 2(-1),\ 2 \cdot 1 - (-1) \cdot 0\right) = (1, 2, 2)$, of magnitude $3$. Since $\gamma$ is acute, the direction cosines are $\frac{1}{3}, \frac{2}{3}, \frac{2}{3}$ (not their negatives), so the sum is $\frac{5}{3}$.",
  "Sign slips in the cross product, or confusing direction ratios with direction cosines.",
  "U11-C-sd-direction", "Direction from two points, a cross product, then direction cosines with an orientation condition.",
  check=_c32, values=[Rational(5, 3), Rational(1, 3), Integer(1), Rational(5, 9)],
  cognitive="Application", source_class="XII")


def _c33():
    P, Q = _feet((0, 0, 1), (1, 1, 0), (2, 0, -1), (1, -1, 0))
    return _cline(P, Q - P)
q("U11-C-033", TOP_LSD, "Equation of the line of shortest distance", "Medium", "Multi-step computation MCQ",
  r"The line of shortest distance between $\vec{r} = \hat{k} + \lambda(\hat{i} + \hat{j})$ and $\vec{r} = (2\hat{i} - \hat{k}) + \mu(\hat{i} - \hat{j})$ is the line",
  r"$x = 1,\ y = 1$",
  [(r"$x = 0,\ y = 0$", r"Takes the vertical line through the given point $(0,0,1)$ of the first line; it is perpendicular to both lines but does not meet the second."),
   (r"$x = 2,\ y = 0$", r"Takes the vertical line through the given point $(2,0,-1)$ of the second line; it does not meet the first line."),
   (r"$x = -1,\ y = -1$", r"Solves $2 - 2\lambda = 0$ as $\lambda = -1$ (sign slip) and takes the vertical line through $(-1,-1,1)$.")],
  r"Let $P = (\lambda, \lambda, 1)$ and $Q = (2 + \mu, -\mu, -1)$, so $\overrightarrow{PQ} = (2 + \mu - \lambda, -\mu - \lambda, -2)$. Perpendicular to $(1,1,0)$: $2 - 2\lambda = 0$; perpendicular to $(1,-1,0)$: $2 + 2\mu = 0$. So $\lambda = 1$, $\mu = -1$, $P = (1,1,1)$, $Q = (1,1,-1)$. The line $PQ$ is $x = 1,\ y = 1$ (parallel to the $z$-axis), and the shortest distance is $2$.",
  "Assuming the common perpendicular passes through a given point of one of the lines.",
  "U11-C-sd-line-eqn", "Two perpendicularity conditions, then the line through the feet.",
  check=_c33, values=[_cline((1, 1, 0), (0, 0, 1)), _cline((0, 0, 0), (0, 0, 1)), _cline((2, 0, 0), (0, 0, 1)), _cline((-1, -1, 0), (0, 0, 1))],
  cognitive="Application", source_class="XII")


def _c34():
    # x = 2y + 1, z = 3 -> (1,0,3) + s(2,1,0);  x = 1, y = 2z -> (1,0,0) + t(0,2,1)
    return _sd((1, 0, 3), (2, 1, 0), (1, 0, 0), (0, 2, 1))
q("U11-C-034", TOP_SD, "Lines given by two equations", "Medium", "Multi-step computation MCQ",
  r"The shortest distance between the lines $x = 2y + 1,\ z = 3$ and $x = 1,\ y = 2z$ is",
  r"$\frac{4\sqrt{21}}{7}$",
  [(r"$\frac{4\sqrt{5}}{5}$", r"Takes the direction of the first line as $(2,1,3)$, using the constant $z = 3$ as a direction ratio: $(2,1,3) \times (0,2,1) = (-5,-2,4)$ and $\frac{12}{3\sqrt{5}}$."),
   (r"$\frac{\sqrt{6}}{2}$", r"Reads $y = 2z$ as direction $(0,1,2)$ instead of $(0,2,1)$: $(2,1,0) \times (0,1,2) = (2,-4,2)$ and $\frac{6}{2\sqrt{6}}$."),
   (r"$\frac{\sqrt{21}}{21}$", r"Uses the position vector $(1,0,0)$ of the second point instead of $\vec{a}_2 - \vec{a}_1$: $|(1,0,0)\cdot(1,-2,4)| = 1$, giving $\frac{1}{\sqrt{21}}$.")],
  r"First line: $(2s + 1, s, 3)$, through $(1,0,3)$ with direction $(2,1,0)$. Second line: $(1, 2t, t)$, through $(1,0,0)$ with direction $(0,2,1)$. Then $\vec{b}_1 \times \vec{b}_2 = (1, -2, 4)$, magnitude $\sqrt{21}$, and $\vec{a}_2 - \vec{a}_1 = (0,0,-3)$ gives the dot product $-12$. So the distance is $\frac{12}{\sqrt{21}} = \frac{4\sqrt{21}}{7}$.",
  "Misreading direction ratios from lines written as a pair of equations.",
  "U11-C-sd-implicit-form", "Parametrising two non-symmetric forms, then the formula.",
  check=_c34, values=[4 * sqrt(21) / 7, 4 * sqrt(5) / 5, sqrt(6) / 2, sqrt(21) / 21],
  cognitive="Application", source_class="XII")


def _c35():
    # x - 1 = 2y = 2 - z  -> (1,0,2) + t(1, 1/2, -1);  x + 1 = -6y = -3z -> (-1,0,0) + t(1, -1/6, -1/3)
    return _sd((1, 0, 2), (1, Rational(1, 2), -1), (-1, 0, 0), (1, Rational(-1, 6), Rational(-1, 3)))
q("U11-C-035", TOP_SD, "Lines in equal-ratio form", "Medium", "Multi-step computation MCQ",
  r"The shortest distance between the lines $x - 1 = 2y = 2 - z$ and $x + 1 = -6y = -3z$ is",
  r"$2$",
  [(r"$\frac{20\sqrt{53}}{53}$", r"Takes the coefficients as direction ratios, $(1,2,-1)$ and $(1,-6,-3)$: cross product $(-12,2,-8)$ and $\frac{|(-2,0,-2)\cdot(-12,2,-8)|}{2\sqrt{53}}$."),
   (r"$6$", r"Stops at $|(-2,0,-2)\cdot(1,2,2)| = 6$ without dividing by $3$."),
   (r"$2\sqrt{2}$", r"Gives the distance between the points $(1,0,2)$ and $(-1,0,0)$.")],
  r"Setting each chain equal to $t$: the first line is $(1 + t, \frac{t}{2}, 2 - t)$, through $(1,0,2)$ with direction $(2, 1, -2)$; the second is $(-1 + t, -\frac{t}{6}, -\frac{t}{3})$, through $(-1,0,0)$ with direction $(6, -1, -2)$. Then $(2,1,-2) \times (6,-1,-2) = (-4, -8, -8) = -4(1,2,2)$, so the unit normal is $\frac{1}{3}(1,2,2)$. With $\vec{a}_2 - \vec{a}_1 = (-2, 0, -2)$, the distance is $\frac{|-2 - 4|}{3} = 2$.",
  "Using coefficients instead of their reciprocals as direction ratios.",
  "U11-C-chain-form", "Two conversions from equal-ratio form, then the skew-line formula.",
  check=_c35, values=[2, 20 * sqrt(53) / 53, 6, 2 * sqrt(2)],
  numerical=dict(question=r"The shortest distance between the lines $x - 1 = 2y = 2 - z$ and $x + 1 = -6y = -3z$ is", answer=2),
  cognitive="Application", source_class="XII")


# =========================================================== DIFFICULT (11)

def _c36():
    k = Symbol('k')
    kk = solve(_det3(_V(3, 1, 2) - _V(1, k, -1), (2, 1, -1), (1, 2, 1)), k)[0]
    return _sd((1, kk, -1), (2, 1, -1), (2, 0, 1), (0, 1, 1))
q("U11-C-036", TOP_INT, "Intersection parameter, then a shortest distance", "Difficult", "Multi-step computation MCQ",
  r"The lines $L_1: \frac{x-1}{2} = \frac{y-k}{1} = \frac{z+1}{-1}$ and $L_2: \frac{x-3}{1} = \frac{y-1}{2} = \frac{z-2}{1}$ intersect. Then the shortest distance between $L_1$ and $L_3: \frac{x-2}{0} = \frac{y}{1} = \frac{z-1}{1}$ is",
  r"$\frac{\sqrt{3}}{3}$",
  [(r"$\frac{7\sqrt{3}}{3}$", r"Solves $12 + 3k = 0$ as $k = 4$ (sign slip), so $L_1$ passes through $(1,4,-1)$ and the triple product with $L_3$ becomes $14$."),
   (r"$3\sqrt{3}$", r"Drops the minus sign of the middle cofactor, $6 + 3(1-k) + 9 = 0$, so $k = 6$; then the triple product with $L_3$ is $18$."),
   (r"$2$", r"Finds $k = -4$ correctly but stops at the triple product $|(1,4,2)\cdot(2,-2,2)| = 2$ without dividing by $2\sqrt{3}$.")],
  r"For $L_1, L_2$: $\vec{b}_1 \times \vec{b}_2 = (2,1,-1) \times (1,2,1) = (3,-3,3)$ and $\vec{a}_2 - \vec{a}_1 = (2, 1-k, 3)$, so $6 - 3(1-k) + 9 = 0$ gives $k = -4$. Now $L_1$ passes through $(1,-4,-1)$. For $L_1, L_3$: $(2,1,-1) \times (0,1,1) = (2,-2,2)$, magnitude $2\sqrt{3}$, and $(2,0,1) - (1,-4,-1) = (1,4,2)$ gives the dot product $2 - 8 + 4 = -2$. So the distance is $\frac{2}{2\sqrt{3}} = \frac{\sqrt{3}}{3}$.",
  "Sign errors in the coplanarity condition propagate into the second distance.",
  "U11-C-intersect-then-sd", "Two linked stages: intersection parameter, then a skew-line distance with a zero direction ratio.",
  check=_c36, values=[sqrt(3) / 3, 7 * sqrt(3) / 3, 3 * sqrt(3), 2], cognitive="Analysis", source_class="XII")


def _c37():
    k = Symbol('k', real=True)
    f = _sd((0, 0, 0), (1, 0, 0), (0, 3, 4), (1, 1, k))**2
    f = simplify(f)
    crit = solve(diff(f, k), k)
    cand = [f.subs(k, c) for c in crit] + [limit(f, k, oo), limit(f, k, -oo)]
    m = Max(*cand)
    # the maximum must be attained at a critical point
    assert any(simplify(f.subs(k, c) - m) == 0 for c in crit)
    return sqrt(m)
q("U11-C-037", TOP_SD, "Maximum shortest distance over a family", "Difficult", "Multi-step computation MCQ",
  r"For real $k$, let $d(k)$ be the shortest distance between the $x$-axis and the line $\frac{x}{1} = \frac{y-3}{1} = \frac{z-4}{k}$. The maximum value of $d(k)$ is",
  r"$5$",
  [(r"$4$", r"Takes $k = 0$ as the extreme case, where $d = \frac{4}{1} = 4$."),
   (r"$3$", r"Takes the limiting value as $k \to \infty$, where $d \to 3$, as the maximum."),
   (r"$\frac{25}{4}$", r"Finds the optimal $k = -\frac{3}{4}$ but evaluates only the numerator $|4 - 3k| = \frac{25}{4}$, forgetting the denominator $\sqrt{1 + k^2} = \frac{5}{4}$.")],
  r"$\hat{i} \times (1, 1, k) = (0, -k, 1)$, magnitude $\sqrt{1 + k^2}$. With $\vec{a}_2 - \vec{a}_1 = (0, 3, 4)$, $d(k) = \frac{|4 - 3k|}{\sqrt{1 + k^2}}$. By the Cauchy-Schwarz inequality, $|4 \cdot 1 + (-3) \cdot k| \le \sqrt{16 + 9}\,\sqrt{1 + k^2}$, so $d(k) \le 5$, with equality when $(1, k)$ is parallel to $(4, -3)$, i.e. $k = -\frac{3}{4}$. So the maximum is $5$.",
  "Checking only special values of the parameter instead of optimising.",
  "U11-C-sd-max", "Distance as a function of a parameter, then an optimisation by Cauchy-Schwarz or calculus.",
  check=_c37, values=[5, 4, 3, Rational(25, 4)],
  numerical=dict(question=r"For real $k$, let $d(k)$ be the shortest distance between the $x$-axis and the line $\frac{x}{1} = \frac{y-3}{1} = \frac{z-4}{k}$. The maximum value of $d(k)$ is", answer=5),
  cognitive="Analysis", source_class="XII")


def _c38():
    P, Q = _feet((1, 2, 0), (1, 0, 1), (0, 1, 4), (0, 1, 1))
    return _cline(P, Q - P)
q("U11-C-038", TOP_LSD, "Equation of the line of shortest distance", "Difficult", "Multi-step computation MCQ",
  r"The line of shortest distance between $\frac{x-1}{1} = \frac{y-2}{0} = \frac{z}{1}$ and $\frac{x}{0} = \frac{y-1}{1} = \frac{z-4}{1}$ is",
  r"$\frac{x-2}{1} = \frac{y-2}{1} = \frac{z-1}{-1}$",
  [(r"$\frac{x-1}{1} = \frac{y-2}{1} = \frac{z}{-1}$", r"Uses the correct direction $(1,1,-1)$ but passes it through the given point $(1,2,0)$ of the first line instead of the foot $(2,2,1)$."),
   (r"$\frac{x}{1} = \frac{y-1}{1} = \frac{z-4}{-1}$", r"Uses the correct direction but passes it through the given point $(0,1,4)$ of the second line instead of the foot $(0,0,3)$."),
   (r"$\frac{x-2}{1} = \frac{y-2}{-1} = \frac{z-1}{-1}$", r"Finds the foot $(2,2,1)$ but takes $\vec{b}_1 \times \vec{b}_2$ as $(-1, 1, 1)$, a sign slip in the middle component.")],
  r"Let $P = (1 + s, 2, s)$ and $Q = (0, 1 + t, 4 + t)$. Then $\overrightarrow{PQ} = (-1 - s, t - 1, 4 + t - s)$. Perpendicular to $(1,0,1)$: $3 + t - 2s = 0$; perpendicular to $(0,1,1)$: $3 + 2t - s = 0$. So $s = 1$, $t = -1$, giving $P = (2,2,1)$ and $Q = (0,0,3)$. The direction $\overrightarrow{PQ} = (-2,-2,2)$ is parallel to $(1,1,-1)$, so the line is $\frac{x-2}{1} = \frac{y-2}{1} = \frac{z-1}{-1}$.",
  "Taking the given points of the lines as the feet of the common perpendicular.",
  "U11-C-sd-line-eqn", "Feet of the common perpendicular from a 2 by 2 system, zero direction ratios, then the line equation.",
  check=_c38, values=[_cline((2, 2, 1), (1, 1, -1)), _cline((1, 2, 0), (1, 1, -1)), _cline((0, 1, 4), (1, 1, -1)), _cline((2, 2, 1), (1, -1, -1))],
  cognitive="Analysis", source_class="XII")


def _c39():
    a1, b1, a2, b2 = _V(1, 2, -1), _V(1, 2, 2), _V(-1, 3, 2), _V(2, -2, 1)
    P, Q = _feet(a1, b1, a2, b2)
    vals = set()
    for e1 in (1, -1):
        for e2 in (1, -1):
            S_ = P + e1 * 3 * b1 / b1.norm()
            T_ = Q + e2 * 4 * b2 / b2.norm()
            vals.add(simplify((S_ - T_).dot(S_ - T_)))
    assert len(vals) == 1
    return vals.pop()
q("U11-C-039", TOP_LSD, "Distance between points on perpendicular skew lines", "Difficult", "Multi-step computation MCQ",
  r"Let $P$ on $L_1: \frac{x-1}{1} = \frac{y-2}{2} = \frac{z+1}{2}$ and $Q$ on $L_2: \frac{x+1}{2} = \frac{y-3}{-2} = \frac{z-2}{1}$ be the points for which $PQ$ is the shortest distance between the two lines. If $S$ is a point on $L_1$ with $PS = 3$ and $T$ is a point on $L_2$ with $QT = 4$, then $ST^2$ equals",
  r"$34$",
  [(r"$25$", r"Treats the lines as if they met at $P = Q$, so $ST^2 = 3^2 + 4^2$, ignoring the common perpendicular $PQ$."),
   (r"$106$", r"Divides $|(-2,1,3)\cdot(6,3,-6)| = 27$ by $|(1,2,2)| = 3$, the length of one direction, instead of by $|\vec{b}_1 \times \vec{b}_2| = 9$, getting $PQ = 9$; then $ST^2 = 9 + 81 + 16 = 106$."),
   (r"$39$", r"Uses the distance between the given points $(1,2,-1)$ and $(-1,3,2)$, $\sqrt{14}$, as $PQ$; then $ST^2 = 9 + 16 + 14$.")],
  r"The directions $(1,2,2)$ and $(2,-2,1)$ have dot product $2 - 4 + 2 = 0$, so the lines are perpendicular. Their cross product is $(6, 3, -6)$, of magnitude $9$, and with $\vec{a}_2 - \vec{a}_1 = (-2, 1, 3)$ the dot product is $-12 + 3 - 18 = -27$, so $PQ = 3$. Now $\overrightarrow{ST} = \overrightarrow{SP} + \overrightarrow{PQ} + \overrightarrow{QT}$, where $\overrightarrow{SP}$ lies along $L_1$, $\overrightarrow{QT}$ along $L_2$, and $\overrightarrow{PQ}$ is perpendicular to both; since $L_1 \perp L_2$ as well, the three vectors are mutually perpendicular. Hence $ST^2 = 3^2 + 3^2 + 4^2 = 34$, whichever side of $P$ and $Q$ the points $S$ and $T$ lie.",
  "Ignoring the common perpendicular, or not noticing that perpendicular directions make the three segments mutually perpendicular.",
  "U11-C-sd-perp-segments", "Must spot that the lines are perpendicular, find the shortest distance, then combine three mutually perpendicular segments; the answer is independent of the positions of $S$ and $T$.",
  check=_c39, values=[34, 25, 106, 39],
  numerical=dict(question=r"Let $P$ on $L_1: \frac{x-1}{1} = \frac{y-2}{2} = \frac{z+1}{2}$ and $Q$ on $L_2: \frac{x+1}{2} = \frac{y-3}{-2} = \frac{z-2}{1}$ be the points for which $PQ$ is the shortest distance between the two lines. If $S$ is a point on $L_1$ with $PS = 3$ and $T$ is a point on $L_2$ with $QT = 4$, then $ST^2$ equals", answer=34),
  cognitive="Analysis", source_class="XII")


def _c40():
    k = Symbol('k', real=True)
    a1, a2 = _V(1, -1, 2), _V(1, 0, 3)
    b1, b2 = _V(k, 1, 2), _V(2, 1, k)
    roots = solveset(_det3(a2 - a1, b1, b2), k, S.Reals)
    good = [r for r in roots if _nature(a1, b1.subs(k, r), a2, b2.subs(k, r)) == INTERSECT]
    return FiniteSet(*good)
q("U11-C-040", TOP_INT, "Intersection with a parallel case to exclude", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which the lines $\frac{x-1}{k} = \frac{y+1}{1} = \frac{z-2}{2}$ and $\frac{x-1}{2} = \frac{y}{1} = \frac{z-3}{k}$ intersect is",
  r"$\{-1\}$",
  [(r"$\{-1, 2\}$", r"Takes both roots of the coplanarity condition, missing that for $k = 2$ the lines are parallel and distinct."),
   (r"$\{2\}$", r"Keeps only the root $k = 2$, where the direction ratios are equal, and calls those lines intersecting."),
   (r"$\{1, -2\}$", r"Sign slip in the determinant, getting $k^2 + k - 2 = 0$ instead of $k^2 - k - 2 = 0$.")],
  r"With $\vec{a}_2 - \vec{a}_1 = (0, 1, 1)$, the coplanarity condition is $\begin{vmatrix} 0 & 1 & 1 \\ k & 1 & 2 \\ 2 & 1 & k \end{vmatrix} = -(k^2 - 4) + (k - 2) = -(k - 2)(k + 1) = 0$, so $k = 2$ or $k = -1$. For $k = 2$ both directions are $(2,1,2)$, and $(0,1,1)$ is not along it, so the lines are parallel and distinct, not intersecting. For $k = -1$ the directions $(-1,1,2)$ and $(2,1,-1)$ are not parallel, so the lines intersect. The set is $\{-1\}$.",
  "Forgetting that the coplanarity condition also holds for parallel lines.",
  "U11-C-coplanar-casework", "Quadratic coplanarity condition plus casework to discard the parallel root.",
  check=_c40, values=[FiniteSet(-1), FiniteSet(-1, 2), FiniteSet(2), FiniteSet(1, -2)],
  cognitive="Analysis", source_class="XII")


def _c41():
    lam, k = Symbol('lam', real=True), Symbol('k', real=True)
    b1, b2 = _V(2, 1, -2), Matrix([-4, k, 4])
    # coplanar and non-intersecting forces parallel: solve b1 x b2 = 0 for k
    ks = solve(list(b1.cross(b2)), k, dict=True)
    assert len(ks) == 1
    kk = ks[0][k]
    b2 = b2.subs(k, kk)
    roots = solveset(Eq(_sd((1, lam, -1), b1, (3, -1, 1), b2)**2, 16), lam, S.Reals)
    assert len(roots) == 2
    for r in roots:
        assert _nature((1, r, -1), b1, (3, -1, 1), b2) == PARALLEL
    return Mul(*list(roots))
q("U11-C-041", TOP_PAR, "Coplanar non-intersecting lines, then a parameter from the distance", "Difficult", "Inverse/parameter MCQ",
  r"Let $\lambda, k \in \mathbb{R}$. The lines $\frac{x-1}{2} = \frac{y-\lambda}{1} = \frac{z+1}{-2}$ and $\frac{x-3}{-4} = \frac{y+1}{k} = \frac{z-1}{4}$ are coplanar but do not intersect, and the distance between them is $4$. Then the product of all possible values of $\lambda$ is",
  r"$-8$",
  [(r"$-7$", r"After finding $k = -2$, sets the distance between the points $(1,\lambda,-1)$ and $(3,-1,1)$ equal to $4$: $8 + (\lambda + 1)^2 = 16$, so $\lambda^2 + 2\lambda - 7 = 0$."),
   (r"$-11$", r"Subtracts $\frac{((\vec{a}_2 - \vec{a}_1)\cdot\vec{b})^2}{|\vec{b}|}$ instead of dividing by $|\vec{b}|^2$, with $\vec{b} = (2,1,-2)$: $8 + \frac{2}{3}(\lambda + 1)^2 = 16$, so $\lambda^2 + 2\lambda - 11 = 0$."),
   (r"$8$", r"Sets up $\lambda^2 + 2\lambda - 8 = 0$ correctly but takes the product of roots as $-\frac{c}{a}$.")],
  r"Two coplanar lines that do not meet must be parallel, so $(-4, k, 4)$ is proportional to $(2, 1, -2)$, giving $k = -2$. Take $\vec{b} = (2,1,-2)$, $|\vec{b}| = 3$, and $\vec{a}_2 - \vec{a}_1 = (2, -1-\lambda, 2)$; put $u = \lambda + 1$. Then $|\vec{a}_2 - \vec{a}_1|^2 = 8 + u^2$ and $(\vec{a}_2 - \vec{a}_1)\cdot\vec{b} = 4 - u - 4 = -u$, so $d^2 = 8 + u^2 - \frac{u^2}{9} = 8 + \frac{8u^2}{9}$. Setting $d^2 = 16$ gives $u^2 = 9$, so $\lambda = 2$ or $\lambda = -4$; for both the lines are distinct parallel lines, as required. The product is $-8$.",
  "Not seeing that coplanar non-intersecting lines must be parallel, or using a point-to-point distance or a wrong projection formula for parallel lines.",
  "U11-C-sd-parallel-inverse", r"Two ideas: deduce parallelism (and $k$) from 'coplanar but not intersecting', then invert the parallel-line distance formula, which gives a quadratic in $\lambda$.",
  check=_c41, values=[-8, -7, -11, 8], cognitive="Analysis", source_class="XII")


def _c42():
    s1 = _nature((1, 2, 3), (2, 3, 4), (2, 3, 4), (3, 4, 5)) == SKEW
    s2 = _sd((1, 2, 0), (1, -1, 1), (2, 0, 1), (2, -2, 2)) == sqrt(6)
    return (bool(s1), bool(s2))
q("U11-C-042", TOP_NAT, "Statements on skewness and parallel distance", "Difficult", "Statement-based MCQ",
  r"Statement I: The lines $\frac{x-1}{2} = \frac{y-2}{3} = \frac{z-3}{4}$ and $\frac{x-2}{3} = \frac{y-3}{4} = \frac{z-4}{5}$ are skew. Statement II: The distance between the lines $\vec{r} = (\hat{i} + 2\hat{j}) + \lambda(\hat{i} - \hat{j} + \hat{k})$ and $\vec{r} = (2\hat{i} + \hat{k}) + \mu(2\hat{i} - 2\hat{j} + 2\hat{k})$ is $\sqrt{6}$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts Statement I because the directions differ, and accepts Statement II by taking $|\vec{a}_2 - \vec{a}_1| = |(1,-2,1)| = \sqrt{6}$ as the distance."),
   (ST_TF, r"Accepts Statement I without evaluating the determinant (which is $0$), but correctly rejects Statement II."),
   (ST_FT, r"Correctly finds that the lines in Statement I meet, but accepts Statement II using the distance between the given points.")],
  r"Statement I: with $\vec{a}_2 - \vec{a}_1 = (1,1,1)$, $\begin{vmatrix} 1 & 1 & 1 \\ 2 & 3 & 4 \\ 3 & 4 & 5 \end{vmatrix} = 1(15 - 16) - 1(10 - 12) + 1(8 - 9) = 0$, and the directions are not parallel, so the lines intersect; false. Statement II: the lines are parallel with $\vec{b} = (1,-1,1)$; with $\vec{a}_2 - \vec{a}_1 = (1,-2,1)$, $(1,-2,1) \times (1,-1,1) = (-1, 0, 1)$, so $d = \frac{\sqrt{2}}{\sqrt{3}} = \frac{\sqrt{6}}{3}$, not $\sqrt{6}$; false.",
  "Assuming non-parallel lines are skew; using point-to-point distance for parallel lines.",
  "U11-C-statement-nature", "Two separate checks with a determinant and a parallel-line distance, both with traps.",
  check=_c42, values=[(F_, F_), (T_, T_), (T_, F_), (F_, T_)], cognitive="Analysis", source_class="XII")


def _c43():
    O, G = _V(0, 0, 0), _V(2, 2, 2)
    M = (_V(2, 0, 0) + _V(2, 2, 0)) / 2
    N = (_V(0, 2, 0) + _V(0, 2, 2)) / 2
    return _sd(O, G - O, M, N - M)
q("U11-C-043", TOP_SD, "Cube: diagonal and a line joining edge midpoints", "Difficult", "Multi-step computation MCQ",
  r"A cube has edge $2$ with one vertex at $O(0,0,0)$ and three edges along the positive coordinate axes; $G = (2,2,2)$. Let $M$ be the midpoint of the edge joining $(2,0,0)$ and $(2,2,0)$, and $N$ the midpoint of the edge joining $(0,2,0)$ and $(0,2,2)$. The shortest distance between the lines $OG$ and $MN$ is",
  r"$\frac{\sqrt{2}}{2}$",
  [(r"$3$", r"Stops at $|\overrightarrow{OM}\cdot(\overrightarrow{OG} \times \overrightarrow{MN})| = 3$ (with directions $(1,1,1)$ and $(-2,1,1)$) without dividing by $3\sqrt{2}$."),
   (r"$\frac{1}{6}$", r"Divides $3$ by $|(0,-3,3)|^2 = 18$ instead of by $3\sqrt{2}$."),
   (r"$\sqrt{5}$", r"Gives $OM = |(2,1,0)| = \sqrt{5}$, the distance between two chosen points.")],
  r"$M = (2, 1, 0)$ and $N = (0, 2, 1)$, so $\overrightarrow{MN} = (-2, 1, 1)$; $OG$ has direction $(1,1,1)$. Then $(1,1,1) \times (-2,1,1) = (0, -3, 3)$, magnitude $3\sqrt{2}$. With $\overrightarrow{OM} = (2,1,0)$, the dot product is $-3$. So the shortest distance is $\frac{3}{3\sqrt{2}} = \frac{\sqrt{2}}{2}$.",
  "Wrong normalising factor, or using a point-to-point distance.",
  "U11-C-cube-midpoints", "Locating midpoints in a solid, forming two lines, then the skew-line formula.",
  check=_c43, values=[sqrt(2) / 2, 3, Rational(1, 6), sqrt(5)], cognitive="Application", source_class="XII")


def _c44():
    P, Q = _feet((2, 4, 4), (1, 2, 2), (5, 1, 1), (2, -2, 1))
    return sum(P) + sum(Q)
q("U11-C-044", TOP_LSD, "Feet of the common perpendicular", "Difficult", "Multi-step computation MCQ",
  r"Let $P$ on $L_1: \frac{x-2}{1} = \frac{y-4}{2} = \frac{z-4}{2}$ and $Q$ on $L_2: \frac{x-5}{2} = \frac{y-1}{-2} = \frac{z-1}{1}$ be such that $PQ$ is perpendicular to both lines. The sum of all six coordinates of $P$ and $Q$ is",
  r"$11$",
  [(r"$13$", r"Gets $t = +1$ instead of $t = -1$ for $L_2$ (sign slip), so $Q = (7,-1,2)$ with coordinate sum $8$, while $P = (1,2,2)$."),
   (r"$17$", r"Takes the given points $(2,4,4)$ and $(5,1,1)$ as the feet of the common perpendicular."),
   (r"$21$", r"Gets $s = +1$ instead of $s = -1$ for $L_1$ (sign slip), so $P = (3,6,6)$ with coordinate sum $15$, while $Q = (3,3,0)$.")],
  r"Let $P = (2 + s, 4 + 2s, 4 + 2s)$ and $Q = (5 + 2t, 1 - 2t, 1 + t)$. Then $\overrightarrow{PQ} = (3 + 2t - s, -3 - 2t - 2s, -3 + t - 2s)$. Since $(1,2,2)\cdot(2,-2,1) = 0$, the conditions simplify: $\overrightarrow{PQ}\cdot(1,2,2) = -9 - 9s = 0$ gives $s = -1$, and $\overrightarrow{PQ}\cdot(2,-2,1) = 9 + 9t = 0$ gives $t = -1$. So $P = (1,2,2)$ and $Q = (3,3,0)$, and the required sum is $5 + 6 = 11$.",
  "Sign slips in the perpendicularity equations, or assuming the given points are the feet.",
  "U11-C-sd-feet", "Two simultaneous perpendicularity conditions, then coordinates of both feet.",
  check=_c44, values=[11, 13, 17, 21],
  numerical=dict(question=r"Let $P$ on $L_1: \frac{x-2}{1} = \frac{y-4}{2} = \frac{z-4}{2}$ and $Q$ on $L_2: \frac{x-5}{2} = \frac{y-1}{-2} = \frac{z-1}{1}$ be such that $PQ$ is perpendicular to both lines. The sum of all six coordinates of $P$ and $Q$ is", answer=11),
  cognitive="Analysis", source_class="XII")


def _c45():
    a1, b1 = _V(1, -1, 2), _V(2, 1, -2)
    t1 = solve(a1[0] + Symbol('t') * b1[0] - 1, Symbol('t'))[0]
    t2 = solve(a1[0] + Symbol('t') * b1[0] - 5, Symbol('t'))[0]
    P, Q = a1 + t1 * b1, a1 + t2 * b1
    R = _V(4, -1, 2)
    area = (Q - P).cross(R - P).norm() / 2
    assert simplify(area - _sd(a1, b1, R, (-4, -2, 4)) * (Q - P).norm() / 2) == 0
    return simplify(area)
q("U11-C-045", TOP_PAR, "Triangle with a vertex on a parallel line", "Difficult", "Multi-step computation MCQ",
  r"$P$ and $Q$ are the points on $L_1: \frac{x-1}{2} = \frac{y+1}{1} = \frac{z-2}{-2}$ with $x$-coordinates $1$ and $5$ respectively, and $R$ is any point on $L_2: \frac{x-4}{-4} = \frac{y+1}{-2} = \frac{z-2}{4}$. The area of triangle $PQR$ is",
  r"$3\sqrt{5}$",
  [(r"$6\sqrt{5}$", r"Uses $PQ \cdot d = 6\sqrt{5}$, forgetting the factor $\frac{1}{2}$."),
   (r"$9$", r"Uses the distance $3$ between $(1,-1,2)$ and $(4,-1,2)$ as the height, getting $\frac{1}{2} \cdot 6 \cdot 3$."),
   (r"$2\sqrt{5}$", r"Takes $PQ = 5 - 1 = 4$, the difference of $x$-coordinates, so the area is $\frac{1}{2} \cdot 4 \cdot \sqrt{5}$.")],
  r"$L_2$ has direction $(-4,-2,4) = -2(2,1,-2)$, so $L_1 \parallel L_2$ and every $R$ on $L_2$ is at the same distance $d$ from $L_1$. With $\vec{b} = (2,1,-2)$, $|\vec{b}| = 3$, and $(4,-1,2) - (1,-1,2) = (3,0,0)$, $|(3,0,0) \times (2,1,-2)| = |(0, 6, 3)| = 3\sqrt{5}$, so $d = \sqrt{5}$. On $L_1$, $x = 1$ gives $P = (1,-1,2)$ and $x = 5$ gives $Q = (5, 1, -2)$, so $PQ = |(4,2,-4)| = 6$. The area is $\frac{1}{2} \cdot 6 \cdot \sqrt{5} = 3\sqrt{5}$.",
  "Using the wrong base length or the wrong height for a triangle between parallel lines.",
  "U11-C-parallel-area", "Recognise parallel lines, find their distance, find a segment length, combine into an area.",
  check=_c45, values=[3 * sqrt(5), 6 * sqrt(5), 9, 2 * sqrt(5)], cognitive="Analysis", source_class="XII")


def _c46():
    a = Symbol('a', integer=True)
    count = 0
    for av in range(-60, 61):
        if _sd((1, 0, 2), (1, -2, -2), (av, 1, 0), (2, 2, -1)) <= 3:
            count += 1
    return count
q("U11-C-046", TOP_SD, "Counting parameter values from a distance bound", "Difficult", "Inverse/parameter MCQ",
  r"The number of integers $a$ for which the shortest distance between the lines $\vec{r} = (\hat{i} + 2\hat{k}) + \lambda(\hat{i} - 2\hat{j} - 2\hat{k})$ and $\vec{r} = (a\hat{i} + \hat{j}) + \mu(2\hat{i} + 2\hat{j} - \hat{k})$ does not exceed $3$ is",
  r"$10$",
  [(r"$8$", r"Reads does not exceed as strictly less than, solving $|2a - 7| < 9$ to get $0 \le a \le 7$."),
   (r"$4$", r"Forgets to divide by $|\vec{b}_1 \times \vec{b}_2| = 3$ (normal $(2,-1,2)$), solving $|2a - 7| \le 3$ to get $2 \le a \le 5$."),
   (r"$28$", r"Divides by $|(2,-1,2)|^2 = 9$, solving $|2a - 7| \le 27$ to get $-10 \le a \le 17$.")],
  r"$(1,-2,-2) \times (2,2,-1) = (6, -3, 6) = 3(2,-1,2)$, so the unit normal is $\frac{1}{3}(2,-1,2)$. With $\vec{a}_2 - \vec{a}_1 = (a - 1, 1, -2)$, the distance is $\frac{|2a - 2 - 1 - 4|}{3} = \frac{|2a - 7|}{3}$. The condition $\frac{|2a - 7|}{3} \le 3$ gives $-9 \le 2a - 7 \le 9$, i.e. $-1 \le a \le 8$. That is $10$ integers.",
  "Misreading the inequality or the normalising factor when the distance is bounded.",
  "U11-C-sd-count", "Distance with a parameter, an absolute-value inequality, then counting integers.",
  check=_c46, values=[10, 8, 4, 28],
  numerical=dict(question=r"The number of integers $a$ for which the shortest distance between the lines $\vec{r} = (\hat{i} + 2\hat{k}) + \lambda(\hat{i} - 2\hat{j} - 2\hat{k})$ and $\vec{r} = (a\hat{i} + \hat{j}) + \mu(2\hat{i} + 2\hat{j} - \hat{k})$ does not exceed $3$ is", answer=10),
  cognitive="Analysis", source_class="XII")
