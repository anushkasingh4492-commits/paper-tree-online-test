import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_EQ = "Equation of a line in space"
TOP_PT = "Points on a line"
TOP_FOOT = "Foot of perpendicular and image in a line"
TOP_INT = "Intersection of two lines"
TOP_ANG = "Angle between two lines"

_l, _m, _t = symbols('lambda mu t', real=True)


def _M(v):
    return Matrix([nsimplify(x) for x in v])


def _foot(P, A, d):
    P, A, d = _M(P), _M(A), _M(d)
    t = (P - A).dot(d) / d.dot(d)
    return A + t * d


def _img(P, A, d):
    return 2 * _foot(P, A, d) - _M(P)


def _dist(P, A, d):
    return simplify((_M(P) - _foot(P, A, d)).norm())


def _inter(A1, d1, A2, d2):
    A1, d1, A2, d2 = map(_M, (A1, d1, A2, d2))
    s = solve(list(A1 + _l * d1 - A2 - _m * d2), [_l, _m], dict=True)
    assert len(s) == 1
    return A1 + s[0][_l] * d1, s[0][_l], s[0][_m]


def _cos(d1, d2):
    d1, d2 = _M(d1), _M(d2)
    return simplify(Abs(d1.dot(d2)) / (d1.norm() * d2.norm()))


def _on(P, A, d):
    """True if P lies on the line through A with direction d."""
    v = _M(P) - _M(A)
    return _M(d).cross(v) == zeros(3, 1)


def _lc(P, d):
    """Canonical form of a line: direction scaled so first nonzero entry is 1, and the
    point of the line where that coordinate is 0."""
    P, d = _M(P), _M(d)
    i = [j for j in range(3) if d[j] != 0][0]
    dn = d / d[i]
    P0 = P - (P[i] / d[i]) * d
    return tuple(simplify(x) for x in P0) + tuple(simplify(x) for x in dn)


def _pt(*v):
    return tuple(nsimplify(x) for x in v)


# ---------------------------------------------------------------- EASY

def _c1():
    # (x-2)/3 = (y+1)/(-2) = (z-4)/5
    return _lc((2, -1, 4), (3, -2, 5))
q("U11-B-001", TOP_EQ, "Cartesian to vector form", "Easy", "Single-step computation MCQ",
  r"The vector equation of the line $\frac{x-2}{3} = \frac{y+1}{-2} = \frac{z-4}{5}$ is",
  r"$\vec{r} = (2\hat{i} - \hat{j} + 4\hat{k}) + \lambda(3\hat{i} - 2\hat{j} + 5\hat{k})$",
  [(r"$\vec{r} = (-2\hat{i} + \hat{j} - 4\hat{k}) + \lambda(3\hat{i} - 2\hat{j} + 5\hat{k})$",
    "Reads the point with the signs as they appear in the numerators, taking $(-2, 1, -4)$ instead of $(2, -1, 4)$."),
   (r"$\vec{r} = (3\hat{i} - 2\hat{j} + 5\hat{k}) + \lambda(2\hat{i} - \hat{j} + 4\hat{k})$",
    "Swaps the roles of the point and the direction vector."),
   (r"$\vec{r} = (2\hat{i} - \hat{j} + 4\hat{k}) + \lambda(3\hat{i} + 2\hat{j} + 5\hat{k})$",
    "Drops the negative sign of the middle denominator, using direction $(3, 2, 5)$.")],
  r"The line passes through $(2, -1, 4)$ (the values that make each numerator zero) and has direction ratios equal to the denominators $3, -2, 5$. Hence $\vec{r} = (2\hat{i} - \hat{j} + 4\hat{k}) + \lambda(3\hat{i} - 2\hat{j} + 5\hat{k})$.",
  "Reading the point off the symmetric form with the wrong signs.",
  "U11-B-cart-to-vector", "Direct reading of point and direction from the symmetric form.",
  check=_c1, values=[_lc((2, -1, 4), (3, -2, 5)), _lc((-2, 1, -4), (3, -2, 5)), _lc((3, -2, 5), (2, -1, 4)), _lc((2, -1, 4), (3, 2, 5))],
  cognitive="Recall", source_class="XII")


def _c2():
    P, Q = _M((1, 2, -3)), _M((4, -1, 2))
    return _lc(P, Q - P)
q("U11-B-002", TOP_EQ, "Line through two points", "Easy", "Single-step computation MCQ",
  r"The Cartesian equation of the line passing through the points $P(1, 2, -3)$ and $Q(4, -1, 2)$ is",
  r"$\frac{x-1}{3} = \frac{y-2}{-3} = \frac{z+3}{5}$",
  [(r"$\frac{x-1}{5} = \frac{y-2}{1} = \frac{z+3}{-1}$",
    "Adds the coordinates of $P$ and $Q$ to get direction $(5, 1, -1)$ instead of subtracting."),
   (r"$\frac{x+1}{3} = \frac{y+2}{-3} = \frac{z-3}{5}$",
    "Uses the correct direction but writes the numerators with the signs of the point reversed."),
   (r"$\frac{x-1}{3} = \frac{y-2}{3} = \frac{z+3}{5}$",
    "Loses the sign of the $y$-difference $-1 - 2 = -3$.")],
  r"Direction ratios are $Q - P = (4-1, -1-2, 2+3) = (3, -3, 5)$. Using the point $P(1, 2, -3)$, the line is $\frac{x-1}{3} = \frac{y-2}{-3} = \frac{z+3}{5}$.",
  "Adding position vectors instead of subtracting to get the direction.",
  "U11-B-two-point-form", "One subtraction and substitution into the symmetric form.",
  check=_c2, values=[_lc((1, 2, -3), (3, -3, 5)), _lc((1, 2, -3), (5, 1, -1)), _lc((-1, -2, 3), (3, -3, 5)), _lc((1, 2, -3), (3, 3, 5))],
  cognitive="Application", source_class="XII")


def _c3():
    A, d = (1, -2, 3), (2, 3, -1)
    cands = [(5, 4, 1), (5, 4, 5), (5, 8, 1), (2, 3, -1)]
    on = [c for c in cands if _on(c, A, d)]
    assert len(on) == 1
    return _pt(*on[0])
q("U11-B-003", TOP_PT, "Point on a given line", "Easy", "Single-step computation MCQ",
  r"Which of the following points lies on the line $\frac{x-1}{2} = \frac{y+2}{3} = \frac{z-3}{-1}$?",
  r"$(5, 4, 1)$",
  [(r"$(5, 4, 5)$", "Takes $\\lambda = 2$ but adds $2$ to the $z$-coordinate, ignoring the negative denominator: $3 + 2 = 5$."),
   (r"$(5, 8, 1)$", "Takes $\\lambda = 2$ but uses $y = 2 + 3\\lambda$, reading the point's $y$-coordinate as $+2$."),
   (r"$(2, 3, -1)$", "Picks the triple of direction ratios as if it were a point of the line.")],
  r"A general point of the line is $(1 + 2\lambda, -2 + 3\lambda, 3 - \lambda)$. For $\lambda = 2$ this is $(5, 4, 1)$. The other triples give different values of $\lambda$ from different coordinates, so they are not on the line.",
  "Sign slips in writing the general point of a line.",
  "U11-B-point-on-line", "Write the general point and match one triple.",
  check=_c3, values=[_pt(5, 4, 1), _pt(5, 4, 5), _pt(5, 8, 1), _pt(2, 3, -1)],
  cognitive="Understanding", source_class="XII")


def _c4():
    # L1: (x-3)/2 = (y+1)/(-2) = (z-2)/1 ; L2: (x-1)/1 = (y+2)/2 = (3-z)/2
    return _cos((2, -2, 1), (1, 2, -2))
q("U11-B-004", TOP_ANG, "Angle between lines in symmetric form", "Easy", "Single-step computation MCQ",
  r"If $\theta$ $(0 \le \theta \le \frac{\pi}{2})$ is the angle between the lines $\frac{x-3}{2} = \frac{y+1}{-2} = \frac{z-2}{1}$ and $\frac{x-1}{1} = \frac{y+2}{2} = \frac{3-z}{2}$, then $\cos\theta$ equals",
  r"$\frac{4}{9}$",
  [(r"$0$", "Reads the third ratio of the second line as $\\frac{z-3}{2}$, taking direction $(1, 2, 2)$, which gives dot product $2 - 4 + 2 = 0$."),
   (r"$\frac{11}{14}$", "Uses the position vectors of the given points $(3, -1, 2)$ and $(1, -2, 3)$ in place of the direction vectors: $\\frac{3 + 2 + 6}{14}$."),
   (r"$\frac{4}{81}$", "Divides $|\\vec{b}_1 \\cdot \\vec{b}_2| = 4$ by $|\\vec{b}_1|^2 |\\vec{b}_2|^2 = 81$ instead of $|\\vec{b}_1||\\vec{b}_2| = 9$.")],
  r"Write the second line as $\frac{x-1}{1} = \frac{y+2}{2} = \frac{z-3}{-2}$, so its direction is $(1, 2, -2)$; the first has direction $(2, -2, 1)$. Then $\cos\theta = \frac{|2 - 4 - 2|}{3 \cdot 3} = \frac{4}{9}$.",
  "Not rewriting $3 - z$ as $-(z - 3)$ before reading the direction ratio.",
  "U11-B-angle-cartesian", "One formula, with a sign trap in the form of the second line.",
  check=_c4, values=[Rational(4, 9), 0, Rational(11, 14), Rational(4, 81)],
  cognitive="Application", source_class="XII")


def _c5():
    F = _foot((0, 0, 0), (3, 2, 4), (1, 1, 1))
    return tuple(F)
q("U11-B-005", TOP_FOOT, "Foot of perpendicular from the origin", "Easy", "Single-step computation MCQ",
  r"The foot of the perpendicular drawn from the origin to the line $\frac{x-3}{1} = \frac{y-2}{1} = \frac{z-4}{1}$ is",
  r"$(0, -1, 1)$",
  [(r"$(6, 5, 7)$", "Gets the parameter as $\\lambda = +3$ by a sign slip in $\\lambda = -\\frac{9}{3}$."),
   (r"$(-6, -7, -5)$", "Forgets to divide by $|\\vec{b}|^2 = 3$ and uses $\\lambda = -9$."),
   (r"$(0, -2, 2)$", "Doubles the foot, giving the image of the origin in the line instead of the foot.")],
  r"A general point is $F(3 + \lambda, 2 + \lambda, 4 + \lambda)$. Since $\vec{OF}$ is perpendicular to $(1, 1, 1)$, $(3+\lambda) + (2+\lambda) + (4+\lambda) = 0$, so $\lambda = -3$ and $F = (0, -1, 1)$.",
  "Sign errors in the perpendicularity equation for the parameter.",
  "U11-B-foot-origin", "Single perpendicularity condition, linear in one parameter.",
  check=_c5, values=[_pt(0, -1, 1), _pt(6, 5, 7), _pt(-6, -7, -5), _pt(0, -2, 2)],
  cognitive="Application", source_class="XII")


def _c6():
    return tuple(_img((2, 1, 1), (0, -2, -1), (1, 2, 3)))
q("U11-B-006", TOP_FOOT, "Image of a point in a line", "Easy", "Multi-step computation MCQ",
  r"The image of the point $P(2, 1, 1)$ in the line $\frac{x}{1} = \frac{y+2}{2} = \frac{z+1}{3}$ is",
  r"$(0, -1, 3)$",
  [(r"$(1, 0, 2)$", "Stops at the foot of the perpendicular and reports it as the image."),
   (r"$(-2, -5, -3)$", "Reflects $P$ in the point $(0, -2, -1)$ of the line instead of in the line."),
   (r"$(4, 3, -1)$", "Moves away from the line: uses $P + 2(\\vec{P} - \\vec{F})$ in place of $P + 2(\\vec{F} - \\vec{P})$.")],
  r"General point $F(\lambda, -2 + 2\lambda, -1 + 3\lambda)$; $\vec{PF} = (\lambda - 2, 2\lambda - 3, 3\lambda - 2)$ is perpendicular to $(1, 2, 3)$: $14\lambda - 14 = 0$, so $\lambda = 1$ and $F = (1, 0, 2)$. The image is $2F - P = (0, -1, 3)$.",
  "Confusing the foot of the perpendicular with the image.",
  "U11-B-image-in-line", "Foot then midpoint relation; two short steps.",
  check=_c6, values=[_pt(0, -1, 3), _pt(1, 0, 2), _pt(-2, -5, -3), _pt(4, 3, -1)],
  cognitive="Application", source_class="XII")


def _c7():
    X, l, m = _inter((1, 2, 3), (1, 2, 3), (4, 3, 8), (2, -1, 2))
    return tuple(X)
q("U11-B-007", TOP_INT, "Point of intersection of two lines", "Easy", "Multi-step computation MCQ",
  r"The lines $\frac{x-1}{1} = \frac{y-2}{2} = \frac{z-3}{3}$ and $\frac{x-4}{2} = \frac{y-3}{-1} = \frac{z-8}{2}$ intersect at the point",
  r"$(2, 4, 6)$",
  [(r"$(6, 2, 10)$", "Solves correctly for $\\mu = -1$ but substitutes $\\mu = +1$ into the second line."),
   (r"$(0, 0, 0)$", "Substitutes $\\lambda = -1$ (the value of $\\mu$) into the first line."),
   (r"$(-2, -4, -6)$", "Uses the same parameter for both lines: $1 + \\lambda = 4 + 2\\lambda$ gives $\\lambda = -3$.")],
  r"Points are $(1+\lambda, 2+2\lambda, 3+3\lambda)$ and $(4+2\mu, 3-\mu, 8+2\mu)$. From $x$ and $y$: $\lambda = 3 + 2\mu$ and $2 + 6 + 4\mu = 3 - \mu$, so $\mu = -1$, $\lambda = 1$; the $z$-coordinates agree ($6 = 6$). The point is $(2, 4, 6)$.",
  "Using a single parameter for two different lines.",
  "U11-B-intersection-point", "Two linear equations in two parameters plus a consistency check.",
  check=_c7, values=[_pt(2, 4, 6), _pt(6, 2, 10), _pt(0, 0, 0), _pt(-2, -4, -6)],
  cognitive="Application", source_class="XII")


def _c8():
    # given line (1-x)/2 = (y+3)/1 = (2z-1)/4  ->  (x-1)/(-2) = (y+3)/1 = (z-1/2)/2
    d = (-2, 1, 2)
    return _lc((2, -1, 3), d)
q("U11-B-008", TOP_EQ, "Line through a point parallel to a given line", "Easy", "Single-step computation MCQ",
  r"The vector equation of the line through $(2, -1, 3)$ parallel to the line $\frac{1-x}{2} = \frac{y+3}{1} = \frac{2z-1}{4}$ is",
  r"$\vec{r} = (2\hat{i} - \hat{j} + 3\hat{k}) + \lambda(-2\hat{i} + \hat{j} + 2\hat{k})$",
  [(r"$\vec{r} = (2\hat{i} - \hat{j} + 3\hat{k}) + \lambda(2\hat{i} + \hat{j} + 4\hat{k})$",
    "Reads the denominators $2, 1, 4$ directly without putting the line in standard form."),
   (r"$\vec{r} = (2\hat{i} - \hat{j} + 3\hat{k}) + \lambda(2\hat{i} + \hat{j} + 2\hat{k})$",
    "Divides out the coefficient of $z$ but treats $1 - x$ as $x - 1$."),
   (r"$\vec{r} = (2\hat{i} - \hat{j} + 3\hat{k}) + \lambda(-2\hat{i} + \hat{j} + 4\hat{k})$",
    "Handles $1 - x$ but does not divide by the coefficient $2$ of $z$.")],
  r"In standard form the given line is $\frac{x-1}{-2} = \frac{y+3}{1} = \frac{z - \frac{1}{2}}{2}$, so its direction is $(-2, 1, 2)$. The required line is $\vec{r} = (2\hat{i} - \hat{j} + 3\hat{k}) + \lambda(-2\hat{i} + \hat{j} + 2\hat{k})$.",
  "Reading direction ratios from a symmetric form that is not in standard form.",
  "U11-B-parallel-through-point", "One rewrite to standard form, then direct substitution.",
  check=_c8, values=[_lc((2, -1, 3), (-2, 1, 2)), _lc((2, -1, 3), (2, 1, 4)), _lc((2, -1, 3), (2, 1, 2)), _lc((2, -1, 3), (-2, 1, 4))],
  cognitive="Understanding", source_class="XII")


def _c9():
    # (2x-1)/3 = (4-y)/2 = (3z+2)/6 = s
    s = Symbol('s')
    x = solve(2*Symbol('x') - 1 - 3*s, Symbol('x'))[0]
    y = solve(4 - Symbol('y') - 2*s, Symbol('y'))[0]
    z = solve(3*Symbol('z') + 2 - 6*s, Symbol('z'))[0]
    d = [diff(x, s), diff(y, s), diff(z, s)]
    return tuple(simplify(v / d[0]) for v in d)
q("U11-B-009", TOP_EQ, "Direction ratios from a non-standard form", "Easy", "Single-step computation MCQ",
  r"The direction ratios of the line $\frac{2x-1}{3} = \frac{4-y}{2} = \frac{3z+2}{6}$ are proportional to",
  r"$3, -4, 4$",
  [(r"$3, 2, 6$", "Reads the denominators directly."),
   (r"$3, -2, 6$", "Corrects the sign for $4 - y$ but does not divide by the coefficients $2$ of $x$ and $3$ of $z$."),
   (r"$3, -1, 9$", "Multiplies each denominator by the coefficient of the variable ($3 \\cdot 2, -2, 6 \\cdot 3$) instead of dividing, then simplifies $6, -2, 18$.")],
  r"Rewrite as $\frac{x - \frac{1}{2}}{\frac{3}{2}} = \frac{y-4}{-2} = \frac{z + \frac{2}{3}}{2}$. The direction ratios are $\frac{3}{2}, -2, 2$, which are proportional to $3, -4, 4$.",
  "Not making the coefficients of $x$, $y$, $z$ equal to $1$ before reading the ratios.",
  "U11-B-nonstandard-form", "Single rewrite into standard form.",
  check=_c9, values=[(1, Rational(-4, 3), Rational(4, 3)), (1, Rational(2, 3), 2), (1, Rational(-2, 3), 2), (1, Rational(-1, 3), 3)],
  cognitive="Understanding", source_class="XII")


def _c10():
    k = Symbol('k')
    lam = Rational(5 + 1, 3)
    assert Rational(7 - 3, 2) == lam
    return solve((k - 1) / 2 - lam, k)[0]
q("U11-B-010", TOP_PT, "Unknown coordinate of a point on a line", "Easy", "Inverse/parameter MCQ",
  r"If the point $(k, 5, 7)$ lies on the line $\frac{x-1}{2} = \frac{y+1}{3} = \frac{z-3}{2}$, then $k$ equals",
  r"$5$",
  [(r"$3$", "Finds $\\lambda = 2$ but sets $k - 1 = \\lambda$, ignoring the denominator $2$."),
   (r"$4$", "Uses $k = 2\\lambda = 4$, forgetting to add the $x$-coordinate $1$ of the given point."),
   (r"$\frac{11}{3}$", "Uses $y - 1$ instead of $y + 1$, giving $\\lambda = \\frac{4}{3}$ and $k = 1 + \\frac{8}{3}$.")],
  r"From the $y$ and $z$ coordinates, $\frac{5+1}{3} = \frac{7-3}{2} = 2$, so $\lambda = 2$. Then $\frac{k-1}{2} = 2$ gives $k = 5$.",
  "Equating a numerator to the parameter without its denominator.",
  "U11-B-point-on-line-param", "One parameter value then one linear equation.",
  check=_c10, values=[5, 3, 4, Rational(11, 3)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If the point $(k, 5, 7)$ lies on the line $\frac{x-1}{2} = \frac{y+1}{3} = \frac{z-3}{2}$, then the value of $k$ is", answer=5))


def _c11():
    return _dist((3, 3, 0), (5, -1, 5), (2, -1, 2))
q("U11-B-011", TOP_FOOT, "Perpendicular distance of a point from a line", "Easy", "Multi-step computation MCQ",
  r"The perpendicular distance of the point $P(3, 3, 0)$ from the line $\frac{x-5}{2} = \frac{y+1}{-1} = \frac{z-5}{2}$ is",
  r"$3$",
  [(r"$3\sqrt{5}$", "Gives the distance from $P$ to the point $(5, -1, 5)$ of the line, not the perpendicular distance."),
   (r"$6$", "Gives the length of the projection of $\\vec{AP}$ on the line, $\\frac{|(-2, 4, -5) \\cdot (2, -1, 2)|}{3} = 6$."),
   (r"$9$", "Computes $|\\vec{AP}|^2 - 6^2 = 9$ and forgets to take the square root.")],
  r"With $A(5, -1, 5)$, $\vec{AP} = (-2, 4, -5)$, $|\vec{AP}|^2 = 45$ and the projection on $(2, -1, 2)$ is $\frac{|-4 - 4 - 10|}{3} = 6$. So the distance is $\sqrt{45 - 36} = 3$. Equivalently, the foot is $(1, 1, 1)$ and $|\vec{PF}| = \sqrt{4 + 4 + 1} = 3$.",
  "Taking the distance to a given point of the line as the distance from the line.",
  "U11-B-point-line-distance", "Projection and Pythagoras, or foot then distance.",
  check=_c11, values=[3, 3*sqrt(5), 6, 9], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The perpendicular distance of the point $P(3, 3, 0)$ from the line $\frac{x-5}{2} = \frac{y+1}{-1} = \frac{z-5}{2}$ is", answer=3))


def _c12():
    A, d = _M((1, -2, 3)), _M((2, -1, 2))
    sols = solve(((_t * d).norm())**2 - 36, _t)
    pts = [tuple(A + s * d) for s in sols]
    cands = [_pt(5, -4, 7), _pt(13, -8, 15), _pt(5, 0, 7), _pt(7, -5, 9)]
    found = [c for c in cands if c in pts]
    assert len(found) == 1
    return found[0]
q("U11-B-012", TOP_PT, "Point on a line at a given distance", "Easy", "Multi-step computation MCQ",
  r"A point on the line $\frac{x-1}{2} = \frac{y+2}{-1} = \frac{z-3}{2}$ at a distance of $6$ units from the point $(1, -2, 3)$ is",
  r"$(5, -4, 7)$",
  [(r"$(13, -8, 15)$", "Takes $\\lambda = 6$, treating the direction $(2, -1, 2)$ as if it were a unit vector."),
   (r"$(5, 0, 7)$", "Uses $\\lambda = 2$ but adds $2$ to the $y$-coordinate, ignoring the negative ratio."),
   (r"$(7, -5, 9)$", "Takes $\\lambda = 3$ by dividing $6$ by the $x$-ratio $2$ instead of by $|(2, -1, 2)| = 3$.")],
  r"A point of the line is $(1 + 2\lambda, -2 - \lambda, 3 + 2\lambda)$ and its distance from $(1, -2, 3)$ is $|\lambda| \sqrt{4 + 1 + 4} = 3|\lambda|$. So $\lambda = \pm 2$, giving $(5, -4, 7)$ or $(-3, 0, -1)$; only $(5, -4, 7)$ is offered.",
  "Treating direction ratios as direction cosines when measuring distance along a line.",
  "U11-B-point-at-distance", "One distance equation along the line.",
  check=_c12, values=[_pt(5, -4, 7), _pt(13, -8, 15), _pt(5, 0, 7), _pt(7, -5, 9)],
  cognitive="Application", source_class="XII")


def _c13():
    A, d = _M((2, -1, 4)), _M((3, 2, -2))
    s = solve(A[2] + _t * d[2], _t)[0]
    return tuple(A + s * d)
q("U11-B-013", TOP_PT, "Point of a line with a given coordinate", "Easy", "Single-step computation MCQ",
  r"The point on the line $\frac{x-2}{3} = \frac{y+1}{2} = \frac{z-4}{-2}$ whose $z$-coordinate is zero is",
  r"$(8, 3, 0)$",
  [(r"$(-4, -5, 0)$", "Gets $\\lambda = -2$ by a sign slip in $\\frac{0-4}{-2}$."),
   (r"$(-10, -9, 0)$", "Takes $\\lambda = z - 4 = -4$, forgetting the denominator $-2$."),
   (r"$(2, -1, 0)$", "Keeps the $x$ and $y$ coordinates of the given point and only changes $z$ to $0$.")],
  r"Put $\frac{0-4}{-2} = 2 = \lambda$. Then $x = 2 + 3(2) = 8$ and $y = -1 + 2(2) = 3$, so the point is $(8, 3, 0)$.",
  "Sign errors with a negative denominator.",
  "U11-B-coordinate-crossing", "One parameter value from one coordinate.",
  check=_c13, values=[_pt(8, 3, 0), _pt(-4, -5, 0), _pt(-10, -9, 0), _pt(2, -1, 0)],
  cognitive="Application", source_class="XII")


def _c14():
    k = Symbol('k')
    return solve(_M((k, 2, -3)).dot(_M((2, 1, 2))), k)[0]
q("U11-B-014", TOP_ANG, "Perpendicular lines with a parameter", "Easy", "Inverse/parameter MCQ",
  r"If the lines $\frac{x-1}{k} = \frac{y-2}{2} = \frac{z-3}{-3}$ and $\frac{x+2}{2} = \frac{y-1}{1} = \frac{z+4}{2}$ are perpendicular, then $k$ equals",
  r"$2$",
  [(r"$-4$", "Treats the ratio $-3$ as $+3$: $2k + 2 + 6 = 0$."),
   (r"$4$", "Transposes $2$ with the wrong sign: $2k = 2 + 6$."),
   (r"$3$", "Drops the middle product and solves $2k - 6 = 0$.")],
  r"Perpendicular lines need $a_1 a_2 + b_1 b_2 + c_1 c_2 = 0$: $2k + 2 - 6 = 0$, so $k = 2$.",
  "Sign errors in the perpendicularity condition.",
  "U11-B-perpendicular-param", "Single condition, one linear equation.",
  check=_c14, values=[2, -4, 4, 3], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If the lines $\frac{x-1}{k} = \frac{y-2}{2} = \frac{z-3}{-3}$ and $\frac{x+2}{2} = \frac{y-1}{1} = \frac{z+4}{2}$ are perpendicular, then the value of $k$ is", answer=2))

# ---------------------------------------------------------------- MEDIUM

def _c15():
    F = _foot((4, -3, 2), (-1, -4, -4), (2, 3, 6))
    return sum(F)
q("U11-B-015", TOP_FOOT, "Foot of perpendicular from a point", "Medium", "Multi-step computation MCQ",
  r"If $(\alpha, \beta, \gamma)$ is the foot of the perpendicular from $P(4, -3, 2)$ to the line $\frac{x+1}{2} = \frac{y+4}{3} = \frac{z+4}{6}$, then $\alpha + \beta + \gamma$ equals",
  r"$2$",
  [(r"$-20$", "Gets the parameter as $\\lambda = -1$ by a sign slip, giving foot $(-3, -7, -10)$."),
   (r"$1$", "Finds the image $(-2, 1, 2)$ of $P$ instead of the foot."),
   (r"$68$", "Divides $\\vec{AP} \\cdot \\vec{b} = 49$ by $|\\vec{b}| = 7$ instead of $|\\vec{b}|^2 = 49$, taking $\\lambda = 7$ and foot $(13, 17, 38)$.")],
  r"General point $F(-1 + 2\lambda, -4 + 3\lambda, -4 + 6\lambda)$. Then $\vec{PF} = (2\lambda - 5, 3\lambda - 1, 6\lambda - 6)$ and $\vec{PF} \cdot (2, 3, 6) = 49\lambda - 49 = 0$, so $\lambda = 1$ and $F = (1, -1, 2)$. Hence $\alpha + \beta + \gamma = 2$.",
  r"Dividing by $|\vec{b}|$ instead of $|\vec{b}|^2$ when finding the foot parameter.",
  "U11-B-foot-general", "Set up the general point, impose perpendicularity, then evaluate.",
  check=_c15, values=[2, -20, 1, 68], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $(\alpha, \beta, \gamma)$ is the foot of the perpendicular from $P(4, -3, 2)$ to the line $\frac{x+1}{2} = \frac{y+4}{3} = \frac{z+4}{6}$, then $\alpha + \beta + \gamma$ is", answer=2))


def _c16():
    return tuple(_img((4, 3, 0), (4, -3, 3), (1, -2, 2)))
q("U11-B-016", TOP_FOOT, "Image of a point in a line in vector form", "Medium", "Multi-step computation MCQ",
  r"The image of the point $P(4, 3, 0)$ in the line $\vec{r} = (4\hat{i} - 3\hat{j} + 3\hat{k}) + \lambda(\hat{i} - 2\hat{j} + 2\hat{k})$ is",
  r"$(0, -1, -2)$",
  [(r"$(2, 1, -1)$", "Reports the foot of the perpendicular as the image."),
   (r"$(4, -9, 6)$", "Reflects $P$ in the point $(4, -3, 3)$ of the line instead of in the line."),
   (r"$(8, -17, 14)$", "Takes $\\lambda = +2$ for the foot by a sign slip, getting foot $(6, -7, 7)$ and then image $2F - P$.")],
  r"With $A(4, -3, 3)$, $\vec{AP} = (0, 6, -3)$ and $\lambda = \frac{\vec{AP} \cdot \vec{b}}{|\vec{b}|^2} = \frac{-12 - 6}{9} = -2$. The foot is $F = (2, 1, -1)$ and the image is $2F - P = (0, -1, -2)$.",
  "Reflecting in a point of the line instead of in the line.",
  "U11-B-image-in-line", "Foot by projection with a negative parameter, then the midpoint relation.",
  check=_c16, values=[_pt(0, -1, -2), _pt(2, 1, -1), _pt(4, -9, 6), _pt(8, -17, 14)],
  cognitive="Application", source_class="XII")


def _c17():
    X, l, m = _inter((1, 1, 0), (2, -1, 1), (5, 2, -3), (1, 1, -2))
    return X.norm()
q("U11-B-017", TOP_INT, "Distance of the point of intersection", "Medium", "Multi-step computation MCQ",
  r"The lines $\vec{r} = (\hat{i} + \hat{j}) + \lambda(2\hat{i} - \hat{j} + \hat{k})$ and $\vec{r} = (5\hat{i} + 2\hat{j} - 3\hat{k}) + \mu(\hat{i} + \hat{j} - 2\hat{k})$ intersect at a point $R$. The distance of $R$ from the origin is",
  r"$\sqrt{10}$",
  [(r"$\sqrt{70}$", "Finds $\\lambda = 1$ and substitutes it for $\\mu$ in the second line, getting $(6, 3, -5)$."),
   (r"$\sqrt{6}$", "Measures the distance of $R$ from the point $(1, 1, 0)$ instead of from the origin."),
   (r"$\sqrt{114}$", "Takes $\\mu = +2$ by a sign slip, getting $(7, 4, -7)$.")],
  r"Equate: $1 + 2\lambda = 5 + \mu$, $1 - \lambda = 2 + \mu$, $\lambda = -3 - 2\mu$. Subtracting the first two gives $3\lambda = 3$, so $\lambda = 1$, $\mu = -2$, and the third equation holds. $R = (3, 0, 1)$, so $OR = \sqrt{10}$.",
  "Mixing up the two parameters when substituting back.",
  "U11-B-intersection-distance", "Solve for two parameters, verify, then a distance.",
  check=_c17, values=[sqrt(10), sqrt(70), sqrt(6), sqrt(114)], cognitive="Application", source_class="XII")


def _c18():
    k = Symbol('k')
    A1, d1, A2, d2 = _M((2, 1, -1)), _M((1, 2, 3)), Matrix([1, -k, 3]), _M((2, 1, -1))
    e = A1 + _l * d1 - A2 - _m * d2
    s = solve(list(e), [_l, _m, k], dict=True)
    assert len(s) == 1
    return s[0][k]
q("U11-B-018", TOP_INT, "Parameter for which two lines intersect", "Medium", "Inverse/parameter MCQ",
  r"If the lines $\frac{x-2}{1} = \frac{y-1}{2} = \frac{z+1}{3}$ and $\frac{x-1}{2} = \frac{y+k}{1} = \frac{z-3}{-1}$ intersect, then $k$ equals",
  r"$-2$",
  [(r"$2$", "Reads the point of the second line as $(1, k, 3)$ instead of $(1, -k, 3)$."),
   (r"$-\frac{16}{5}$", "Reads $\\frac{z-3}{-1}$ as $z = 3 + \\mu$, giving $\\mu = \\frac{7}{5}$, $\\lambda = \\frac{9}{5}$ and then $k$ from the $y$-equation."),
   (r"$4$", "Gets the point $(3, 3, 2)$ correctly but solves $3 + k = 1$ as $k = 1 + 3$.")],
  r"Equate $x$ and $z$: $2 + \lambda = 1 + 2\mu$ and $-1 + 3\lambda = 3 - \mu$. These give $\lambda = 1$, $\mu = 1$ and the common point $(3, 3, 2)$. The $y$-equation $1 + 2\lambda = -k + \mu$ gives $3 = -k + 1$, so $k = -2$.",
  "Sign errors in reading the point of a line written as $y + k$.",
  "U11-B-intersect-param", "Solve two equations, substitute in the third to find the parameter.",
  check=_c18, values=[-2, 2, Rational(-16, 5), 4], cognitive="Application", source_class="XII")


def _c19():
    return _cos((1, 1, 2), (2, -1, 2))
q("U11-B-019", TOP_ANG, "Angle between lines in the form ax = by = cz", "Medium", "Multi-step computation MCQ",
  r"If $\theta$ is the acute angle between the lines $2x = 2y = z$ and $x = -2y = z$, then $\cos\theta$ equals",
  r"$\frac{5\sqrt{6}}{18}$",
  [(r"$\frac{4}{9}$", "Takes the coefficients $2, 2, 1$ of the first line as its direction ratios instead of $1, 1, 2$."),
   (r"$\frac{\sqrt{6}}{18}$", "Takes the coefficients as direction ratios for both lines: $(2, 2, 1)$ and $(1, -2, 1)$."),
   (r"$\frac{1}{6}$", "Takes the coefficients $1, -2, 1$ of the second line as its direction ratios instead of $2, -1, 2$.")],
  r"Writing $2x = 2y = z = t$ gives $(x, y, z) = t(\frac{1}{2}, \frac{1}{2}, 1)$, so the direction is $(1, 1, 2)$. Similarly $x = -2y = z = s$ gives direction $(2, -1, 2)$. Then $\cos\theta = \frac{|2 - 1 + 4|}{\sqrt{6} \cdot 3} = \frac{5}{3\sqrt{6}} = \frac{5\sqrt{6}}{18}$.",
  "Using the coefficients in $ax = by = cz$ as direction ratios instead of their reciprocals.",
  "U11-B-angle-nonstandard", "Convert two non-standard forms, then the angle formula; a reciprocal trap.",
  check=_c19, values=[5*sqrt(6)/18, Rational(4, 9), sqrt(6)/18, Rational(1, 6)], cognitive="Application", source_class="XII")


def _c20():
    s1 = _on((5, 2, 1), (1, -2, -1), (2, 2, -1))
    s2 = _M((2, 2, -1)).dot(_M((1, -2, -2))) == 0   # x/1 = y/(-2) = (2-z)/2
    return (bool(s1), bool(s2))
q("U11-B-020", TOP_EQ, "Point on a line and perpendicularity", "Medium", "Statement-based MCQ",
  r"Statement I: The point $(5, 2, 1)$ lies on the line $\frac{x-1}{2} = \frac{y+2}{2} = \frac{z+1}{-1}$. Statement II: The lines $\frac{x-1}{2} = \frac{y+2}{2} = \frac{z+1}{-1}$ and $\frac{x}{1} = \frac{y}{-2} = \frac{2-z}{2}$ are perpendicular. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, "Accepts Statement I after taking $\\lambda = 2$ and computing $z = -1 + 2 = 1$, ignoring the ratio $-1$."),
   (ST_FF, "Reads the second line's direction as $(1, -2, 2)$, getting dot product $2 - 4 - 2 \\ne 0$, so rejects Statement II."),
   (ST_TF, "Makes both of the above slips.")],
  r"A point of the first line is $(1 + 2\lambda, -2 + 2\lambda, -1 - \lambda)$; $x = 5$ and $y = 2$ need $\lambda = 2$, which gives $z = -3 \ne 1$. So Statement I is false. The second line is $\frac{x}{1} = \frac{y}{-2} = \frac{z-2}{-2}$ with direction $(1, -2, -2)$, and $(2, 2, -1) \cdot (1, -2, -2) = 2 - 4 + 2 = 0$, so Statement II is true.",
  "Sign errors with negative ratios and with $2 - z$ in a symmetric form.",
  "U11-B-statement-line-facts", "Two independent checks, each with a sign trap.",
  check=_c20, values=[(False, True), (True, True), (False, False), (True, False)],
  cognitive="Analysis", source_class="XII")


def _c21():
    P = _M((2, 2, 1))
    Q = _img(P, (-1, -1, 1), (1, 2, 2))
    return (Q - P).norm()
q("U11-B-021", TOP_FOOT, "Distance between a point and its image", "Medium", "Multi-step computation MCQ",
  r"If $Q$ is the image of the point $P(2, 2, 1)$ in the line $\frac{x+1}{1} = \frac{y+1}{2} = \frac{z-1}{2}$, then the length $PQ$ is",
  r"$6$",
  [(r"$3$", "Finds the distance from $P$ to the foot $(0, 1, 3)$ and does not double it."),
   (r"$3\sqrt{2}$", "Uses the distance from $P$ to the given point $(-1, -1, 1)$ of the line as the distance from the line."),
   (r"$6\sqrt{2}$", "Doubles the distance from $P$ to the given point $(-1, -1, 1)$ instead of to the foot.")],
  r"General point $F(-1 + \lambda, -1 + 2\lambda, 1 + 2\lambda)$. $\vec{PF} \cdot (1, 2, 2) = (\lambda - 3) + 2(2\lambda - 3) + 2(2\lambda) = 9\lambda - 9 = 0$, so $\lambda = 1$ and $F = (0, 1, 3)$. $PF = \sqrt{4 + 1 + 4} = 3$, and $PQ = 2PF = 6$.",
  "Forgetting that the image is twice as far as the foot.",
  "U11-B-image-distance", "Foot, distance, then doubling.",
  check=_c21, values=[6, 3, 3*sqrt(2), 6*sqrt(2)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $Q$ is the image of the point $P(2, 2, 1)$ in the line $\frac{x+1}{1} = \frac{y+1}{2} = \frac{z-1}{2}$, then the length $PQ$ is", answer=6))


def _c22():
    k = Symbol('k')
    P, Q, d = Matrix([k, 2, 5]), _M((3, 2, 0)), _M((1, 1, -1))
    assert _on(Q, (1, 0, 2), d)
    return solve((Q - P).dot(d), k)[0]
q("U11-B-022", TOP_FOOT, "Unknown coordinate from a given foot", "Medium", "Inverse/parameter MCQ",
  r"If the foot of the perpendicular from $P(k, 2, 5)$ to the line $x - 1 = y = 2 - z$ is $Q(3, 2, 0)$, then $k$ equals",
  r"$8$",
  [(r"$-2$", "Takes the direction of the line as $(1, 1, 1)$, reading $2 - z$ as $z - 2$: $(3 - k) - 5 = 0$."),
   (r"$4$", "Uses $\\lambda = \\vec{AP} \\cdot \\vec{b} = k - 2$ without dividing by $|\\vec{b}|^2 = 3$, then sets $\\lambda = 2$."),
   (r"$2$", "Imposes perpendicularity on the vector from $P$ to the point $(1, 0, 2)$ of the line instead of to $Q$.")],
  r"The line is $\frac{x-1}{1} = \frac{y}{1} = \frac{z-2}{-1}$ with direction $(1, 1, -1)$, and $Q$ lies on it. $\vec{PQ} = (3 - k, 0, -5)$ must be perpendicular to $(1, 1, -1)$: $(3 - k) + 0 + 5 = 0$, so $k = 8$.",
  "Misreading the direction of a line written as $x - 1 = y = 2 - z$.",
  "U11-B-foot-reverse", "Rewrite the line, then one perpendicularity condition with the unknown reversed.",
  check=_c22, values=[8, -2, 4, 2], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If the foot of the perpendicular from $P(k, 2, 5)$ to the line $x - 1 = y = 2 - z$ is $Q(3, 2, 0)$, then the value of $k$ is", answer=8))


def _c23():
    d = _M((1, 2, 3)).cross(_M((2, -1, 1)))
    return _lc((1, 2, -1), d)
q("U11-B-023", TOP_EQ, "Line perpendicular to two given lines", "Medium", "Multi-step computation MCQ",
  r"The equation of the line through $(1, 2, -1)$ that is perpendicular to both the lines $\frac{x-3}{1} = \frac{y+1}{2} = \frac{z}{3}$ and $\frac{x+2}{2} = \frac{y-1}{-1} = \frac{z+1}{1}$ is",
  r"$\frac{x-1}{1} = \frac{y-2}{1} = \frac{z+1}{-1}$",
  [(r"$\frac{x-1}{1} = \frac{y-2}{-1} = \frac{z+1}{-1}$", "Forgets the minus sign on the $\\hat{j}$ component of the cross product, getting $(5, -5, -5)$."),
   (r"$\frac{x-1}{3} = \frac{y-2}{1} = \frac{z+1}{4}$", "Adds the two direction vectors instead of taking their cross product."),
   (r"$\frac{x+1}{1} = \frac{y+2}{1} = \frac{z-1}{-1}$", "Uses the right direction but writes the point with reversed signs.")],
  r"The direction is $(1, 2, 3) \times (2, -1, 1) = (2 \cdot 1 - 3 \cdot (-1), 3 \cdot 2 - 1 \cdot 1, 1 \cdot (-1) - 2 \cdot 2) = (5, 5, -5)$, proportional to $(1, 1, -1)$. Through $(1, 2, -1)$ the line is $\frac{x-1}{1} = \frac{y-2}{1} = \frac{z+1}{-1}$.",
  "Sign error in the middle component of a cross product.",
  "U11-B-perp-to-two-lines", "Cross product of two directions, then the symmetric form.",
  check=_c23, values=[_lc((1, 2, -1), (1, 1, -1)), _lc((1, 2, -1), (1, -1, -1)), _lc((1, 2, -1), (3, 1, 4)), _lc((-1, -2, 1), (1, 1, -1))],
  cognitive="Application", source_class="XII")


def _c24():
    P = _M((1, 2, 6))
    F = _foot(P, (0, 0, 0), (1, 1, 1))
    return _lc(P, F - P)
q("U11-B-024", TOP_FOOT, "Equation of the perpendicular from a point to a line", "Medium", "Multi-step computation MCQ",
  r"The equation of the line through $P(1, 2, 6)$ that meets the line $x = y = z$ at right angles is",
  r"$\frac{x-1}{2} = \frac{y-2}{1} = \frac{z-6}{-3}$",
  [(r"$\frac{x-1}{1} = \frac{y-2}{2} = \frac{z-6}{6}$", "Joins $P$ to the origin, a point of the given line, instead of to the foot of the perpendicular."),
   (r"$\frac{x-1}{4} = \frac{y-2}{5} = \frac{z-6}{9}$", "Gets the foot as $(-3, -3, -3)$ by a sign slip in $\\lambda = 3$."),
   (r"$\frac{x-1}{1} = \frac{y-2}{1} = \frac{z-6}{1}$", "Writes the line through $P$ parallel to the given line instead of perpendicular to it.")],
  r"A point of $x = y = z$ is $F(\lambda, \lambda, \lambda)$. $\vec{PF} = (\lambda - 1, \lambda - 2, \lambda - 6)$ is perpendicular to $(1, 1, 1)$ when $3\lambda - 9 = 0$, so $F = (3, 3, 3)$ and $\vec{PF} = (2, 1, -3)$. The line is $\frac{x-1}{2} = \frac{y-2}{1} = \frac{z-6}{-3}$.",
  "Using an arbitrary point of the line instead of the foot.",
  "U11-B-perp-line-through-point", "Foot of perpendicular, then the line through two points.",
  check=_c24, values=[_lc((1, 2, 6), (2, 1, -3)), _lc((1, 2, 6), (1, 2, 6)), _lc((1, 2, 6), (4, 5, 9)), _lc((1, 2, 6), (1, 1, 1))],
  cognitive="Application", source_class="XII")


def _c25():
    a = Symbol('a', real=True)
    d1, d2 = _M((2, -1, 2)), Matrix([-1, a, 2])
    sa = solve(d1.dot(d2), a)
    assert len(sa) == 1
    return _cos(d2.subs(a, sa[0]), (2, 3, 6))
q("U11-B-025", TOP_ANG, "Angle after fixing a parameter by perpendicularity", "Medium", "Multi-step computation MCQ",
  r"The line $L_2: \vec{r} = (\hat{i} + \hat{j}) + \mu(-\hat{i} + a\hat{j} + 2\hat{k})$ is perpendicular to the line $L_1: \frac{x-1}{2} = \frac{y+2}{-1} = \frac{z-3}{2}$. If $\theta$ is the acute angle between $L_2$ and the line $L_3: \frac{x-1}{2} = \frac{y+1}{3} = \frac{z}{6}$, then $\cos\theta$ equals",
  r"$\frac{16}{21}$",
  [(r"$\frac{4}{21}$", "Solves $-2 - a + 4 = 0$ as $a = -2$ by a sign slip, so uses the direction $(-1, -2, 2)$ and gets $\\frac{|-2 - 6 + 12|}{3 \\cdot 7} = \\frac{4}{21}$."),
   (r"$\frac{13}{21}$", "Finds the angle between $L_1$ and $L_3$ instead of $L_2$ and $L_3$: $\\frac{|4 - 3 + 12|}{3 \\cdot 7} = \\frac{13}{21}$."),
   (r"$\frac{20}{21}$", "Finds $a = 2$ correctly but drops the minus sign of $-\\hat{i}$ in the direction of $L_2$, using $(1, 2, 2)$: $\\frac{2 + 6 + 12}{3 \\cdot 7} = \\frac{20}{21}$.")],
  r"Perpendicularity of $L_1$ and $L_2$: $(2)(-1) + (-1)(a) + (2)(2) = 0$, so $2 - a = 0$ and $a = 2$. Then $L_2$ has direction $(-1, 2, 2)$ with magnitude $3$, and $L_3$ has direction $(2, 3, 6)$ with magnitude $7$. Hence $\cos\theta = \frac{|-2 + 6 + 12|}{3 \cdot 7} = \frac{16}{21}$.",
  "Mixing up which pair of lines the final angle is asked for, or losing a sign when reading the direction from vector form.",
  "U11-B-perp-then-angle", "Two linked steps: a perpendicularity condition fixes the parameter, then the angle formula is applied to a different pair of lines.",
  check=_c25, values=[Rational(16, 21), Rational(4, 21), Rational(13, 21), Rational(20, 21)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The line $L_2: \vec{r} = (\hat{i} + \hat{j}) + \mu(-\hat{i} + a\hat{j} + 2\hat{k})$ is perpendicular to the line $L_1: \frac{x-1}{2} = \frac{y+2}{-1} = \frac{z-3}{2}$. If $\theta$ is the acute angle between $L_2$ and the line $L_3: \frac{x-1}{2} = \frac{y+1}{3} = \frac{z}{6}$, then $21\cos\theta$ is", answer=16))


def _c26():
    P = _M((2, 2, 1))
    A, d = (3, 3, -2), (2, 1, -2)
    s1 = _img(P, A, d) == _M((0, 2, -1))
    s2 = simplify(_dist(P, A, d) - 2*sqrt(2)) == 0
    return (bool(s1), bool(s2))
q("U11-B-026", TOP_FOOT, "Image and distance from a line", "Medium", "Statement-based MCQ",
  r"Let $L$ be the line $\frac{x-3}{2} = \frac{y-3}{1} = \frac{z+2}{-2}$ and $P$ be the point $(2, 2, 1)$. Statement I: The image of $P$ in $L$ is $(0, 2, -1)$. Statement II: The perpendicular distance of $P$ from $L$ is $2\sqrt{2}$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, "Takes the distance between $P$ and its image, $2\\sqrt{2}$, as the distance of $P$ from $L$."),
   (ST_FF, "Gets the foot parameter as $\\lambda = +1$ by a sign slip, getting foot $(5, 4, -4)$, and so rejects both statements."),
   (ST_FT, "Mistakes the foot $(1, 2, 0)$ for the image and so rejects Statement I, while taking $2PF = 2\\sqrt{2}$ as the distance from $L$.")],
  r"General point $(3 + 2\lambda, 3 + \lambda, -2 - 2\lambda)$; perpendicularity: $2(1 + 2\lambda) + (1 + \lambda) - 2(-3 - 2\lambda) = 9\lambda + 9 = 0$, so $\lambda = -1$ and the foot is $F(1, 2, 0)$. The image is $2F - P = (0, 2, -1)$, so Statement I is true. The distance is $PF = \sqrt{1 + 0 + 1} = \sqrt{2}$, not $2\sqrt{2}$, so Statement II is false.",
  "Using the distance between a point and its image as the distance from the line.",
  "U11-B-statement-image", "Foot, image and distance all needed; trap between $PF$ and $PQ$.",
  check=_c26, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Analysis", source_class="XII")


def _c27():
    k = Symbol('k')
    P, Q = _M((1, -1, 2)), Matrix([3, 1, k])
    d = Q - P
    s = solve([d[0] - 2*_t, d[1] - 2*_t, d[2] - 6*_t], [k, _t], dict=True)
    return s[0][k]
q("U11-B-027", TOP_EQ, "Parallel lines with an unknown point", "Medium", "Inverse/parameter MCQ",
  r"If the line through the points $(1, -1, 2)$ and $(3, 1, k)$ is parallel to the line $\frac{x}{1} = \frac{y-2}{1} = \frac{z+1}{3}$, then $k$ equals",
  r"$8$",
  [(r"$6$", "Sets $k = 2 \\cdot 3$, forgetting that the $z$-difference is $k - 2$."),
   (r"$5$", "Equates $k - 2$ to $3$ without the scale factor $2$ coming from the $x$ and $y$ differences."),
   (r"$4$", "Writes the $z$-difference as $k + 2$ and solves $k + 2 = 6$.")],
  r"The direction of the line is $(2, 2, k - 2)$. For it to be parallel to $(1, 1, 3)$ we need $\frac{2}{1} = \frac{2}{1} = \frac{k-2}{3}$, so $k - 2 = 6$ and $k = 8$.",
  "Dropping the common scale factor when equating proportional direction ratios.",
  "U11-B-parallel-param", "Proportionality of direction ratios with one unknown.",
  check=_c27, values=[8, 6, 5, 4], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If the line through the points $(1, -1, 2)$ and $(3, 1, k)$ is parallel to the line $\frac{x}{1} = \frac{y-2}{1} = \frac{z+1}{3}$, then the value of $k$ is", answer=8))


def _c28():
    k = Symbol('k')
    A1, d1 = _M((1, 2, 3)), Matrix([2, k, 1])
    A2, d2 = _M((5, 3, 2)), _M((2, -1, -2))
    e = A1 + _l * d1 - A2 - _m * d2
    s = solve(list(e), [_l, _m, k], dict=True)
    assert len(s) == 1
    return s[0][k]
q("U11-B-028", TOP_INT, "Unknown direction ratio for intersecting lines", "Medium", "Inverse/parameter MCQ",
  r"If the lines $\frac{x-1}{2} = \frac{y-2}{k} = \frac{z-3}{1}$ and $\frac{x-5}{2} = \frac{y-3}{-1} = \frac{z-2}{-2}$ intersect, then $k$ equals",
  r"$2$",
  [(r"$0$", "Solves for $\\lambda = 1$, $\\mu = -1$ but evaluates the $y$-coordinate of the second line as $3 + \\mu = 2$."),
   (r"$-\frac{2}{5}$", "Writes the $z$-equation as $3 + \\lambda = 2 + 2\\mu$, getting $\\mu = 3$, $\\lambda = 5$ and then $2 + 5k = 0$."),
   (r"$\frac{1}{2}$", "Finds the correct values but inverts the last step, writing $k = \\frac{\\lambda}{y - 2} = \\frac{1}{2}$.")],
  r"Equate $x$ and $z$: $1 + 2\lambda = 5 + 2\mu$ and $3 + \lambda = 2 - 2\mu$. Substituting $\lambda = -1 - 2\mu$ in the first gives $\mu = -1$, $\lambda = 1$. The common point is $(3, 4, 4)$, and the $y$-equation $2 + k = 4$ gives $k = 2$.",
  "Sign slips with negative direction ratios while solving the pair of equations.",
  "U11-B-intersect-param", "Two equations without the unknown, then the third fixes it.",
  check=_c28, values=[2, 0, Rational(-2, 5), Rational(1, 2)], cognitive="Application", source_class="XII")


def _c29():
    P, Q = _M((1, 0, 2)), _M((3, -1, 4))
    return acos(_cos(Q - P, (1, 1, 4)))
q("U11-B-029", TOP_ANG, "Angle between a two-point line and a given line", "Medium", "Multi-step computation MCQ",
  r"The acute angle between the line joining $P(1, 0, 2)$ and $Q(3, -1, 4)$ and the line $\frac{x-1}{1} = \frac{y}{1} = \frac{z+1}{4}$ is",
  r"$\frac{\pi}{4}$",
  [(r"$\frac{\pi}{3}$", "Divides the dot product $9$ by $|\\vec{b}_2|^2 = 18$ instead of by $|\\vec{b}_1||\\vec{b}_2| = 9\\sqrt{2}$, getting $\\frac{1}{2}$."),
   (r"$\cos^{-1}\left(\frac{11\sqrt{2}}{18}\right)$", "Takes $\\vec{PQ} = (2, 1, 2)$, losing the sign of the $y$-difference: $\\frac{2 + 1 + 8}{9\\sqrt{2}}$."),
   (r"$\cos^{-1}\left(\frac{3}{\sqrt{13}}\right)$", "Uses the position vector of $Q$, $(3, -1, 4)$, as the direction of $PQ$: $\\frac{18}{\\sqrt{26} \\cdot 3\\sqrt{2}}$.")],
  r"$\vec{PQ} = (2, -1, 2)$ with length $3$, and the other direction is $(1, 1, 4)$ with length $3\sqrt{2}$. Then $\cos\theta = \frac{|2 - 1 + 8|}{3 \cdot 3\sqrt{2}} = \frac{1}{\sqrt{2}}$, so $\theta = \frac{\pi}{4}$.",
  "Using a position vector instead of the difference of position vectors as a direction.",
  "U11-B-angle-two-point-line", "Direction from two points, then the angle formula.",
  check=_c29, values=[pi/4, pi/3, acos(11*sqrt(2)/18), acos(3/sqrt(13))], cognitive="Application", source_class="XII")


def _c30():
    Q, R = _M((1, 1, 1)), _M((3, 2, 3))
    return tuple(_foot((6, 3, 4), Q, R - Q))
q("U11-B-030", TOP_FOOT, "Foot of perpendicular on a line through two points", "Medium", "Multi-step computation MCQ",
  r"The foot of the perpendicular from $P(6, 3, 4)$ to the line passing through $Q(1, 1, 1)$ and $R(3, 2, 3)$ is",
  r"$(5, 3, 5)$",
  [(r"$(13, 7, 13)$", "Divides $\\vec{QP} \\cdot \\vec{QR} = 18$ by $|\\vec{QR}| = 3$ instead of $|\\vec{QR}|^2 = 9$, taking $\\lambda = 6$."),
   (r"$(4, 3, 6)$", "Gives the image of $P$ in the line instead of the foot."),
   (r"$(-3, -1, -3)$", "Gets $\\lambda = -2$ by a sign slip.")],
  r"Direction $\vec{QR} = (2, 1, 2)$. A point of the line is $F = Q + \lambda(2, 1, 2)$ and $\lambda = \frac{\vec{QP} \cdot \vec{QR}}{|\vec{QR}|^2} = \frac{(5, 2, 3) \cdot (2, 1, 2)}{9} = 2$. So $F = (5, 3, 5)$.",
  r"Normalising the projection by $|\vec{b}|$ instead of $|\vec{b}|^2$.",
  "U11-B-foot-two-point-line", "Line from two points, then the projection formula for the foot.",
  check=_c30, values=[_pt(5, 3, 5), _pt(13, 7, 13), _pt(4, 3, 6), _pt(-3, -1, -3)],
  cognitive="Application", source_class="XII")


def _c31():
    a, b = symbols('a b')
    P, Q = _M((3, 4, 4)), _M((1, 2, -2))
    d = _M((1, 2, -1))
    assert (Q - P).dot(d) == 0
    Mid = (P + Q) / 2
    s = solve(list(Matrix([1, a, b]) + _t * d - Mid), [a, b, _t], dict=True)
    return s[0][a] + s[0][b]
q("U11-B-031", TOP_FOOT, "Line from a point and its image", "Medium", "Inverse/parameter MCQ",
  r"The point $Q(1, 2, -2)$ is the image of the point $P(3, 4, 4)$ in the line $\frac{x-1}{1} = \frac{y-a}{2} = \frac{z-b}{-1}$. Then $a + b$ equals",
  r"$3$",
  [(r"$6$", "Makes $P$ itself lie on the line instead of the midpoint of $PQ$."),
   (r"$0$", "Makes $Q$ lie on the line instead of the midpoint of $PQ$."),
   (r"$1$", "Uses the midpoint $(2, 3, 1)$ but reads the third ratio as $\\frac{z-b}{1}$, getting $b = 0$ with $a = 1$.")],
  r"$\vec{PQ} = (-2, -2, -6)$ is perpendicular to $(1, 2, -1)$, as it must be. The midpoint $(2, 3, 1)$ of $PQ$ lies on the line, so $\frac{2-1}{1} = \frac{3-a}{2} = \frac{1-b}{-1} = 1$. Hence $a = 1$, $b = 2$ and $a + b = 3$.",
  "Putting the given point, rather than the midpoint of the point and its image, on the mirror line.",
  "U11-B-image-reverse", "Uses the midpoint property of an image in reverse to recover the line.",
  check=_c31, values=[3, 6, 0, 1], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The point $Q(1, 2, -2)$ is the image of the point $P(3, 4, 4)$ in the line $\frac{x-1}{1} = \frac{y-a}{2} = \frac{z-b}{-1}$. Then the value of $a + b$ is", answer=3))


def _c32():
    k, m = symbols('k m')
    P, Q = _M((2, -1, 3)), _M((4, 0, 1))
    R = Matrix([k, m, -7])
    s = solve(list(P + _t * (Q - P) - R), [k, m, _t], dict=True)
    return s[0][k] + s[0][m]
q("U11-B-032", TOP_PT, "Collinear points", "Medium", "Inverse/parameter MCQ",
  r"If the points $P(2, -1, 3)$, $Q(4, 0, 1)$ and $R(k, m, -7)$ are collinear, then $k + m$ equals",
  r"$16$",
  [(r"$-14$", "Gets $\\lambda = -5$ from $3 - 2\\lambda = -7$ by a sign slip."),
   (r"$7$", "Uses $\\frac{z+3}{-2}$ instead of $\\frac{z-3}{-2}$, so $\\lambda = 2$, $k = 6$, $m = 1$."),
   (r"$11$", "Gets $\\lambda = 5$ but writes $k = 2 + \\lambda$, forgetting the $x$-ratio $2$.")],
  r"The line $PQ$ is $\frac{x-2}{2} = \frac{y+1}{1} = \frac{z-3}{-2} = \lambda$. For $R$, $\lambda = \frac{-7-3}{-2} = 5$, so $k = 2 + 10 = 12$ and $m = -1 + 5 = 4$. Thus $k + m = 16$.",
  "Sign errors with a negative direction ratio.",
  "U11-B-collinear-param", "Write the line through two points, then use the known coordinate.",
  check=_c32, values=[16, -14, 7, 11], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If the points $P(2, -1, 3)$, $Q(4, 0, 1)$ and $R(k, m, -7)$ are collinear, then the value of $k + m$ is", answer=16))


def _c33():
    F = _foot((4, 3, 4), (0, 0, 0), (1, 2, 2))
    return sum(F)
q("U11-B-033", TOP_FOOT, "Nearest point of a line", "Medium", "Multi-step computation MCQ",
  r"Let $(\alpha, \beta, \gamma)$ be the point on the line $x = \frac{y}{2} = \frac{z}{2}$ that is nearest to the point $(4, 3, 4)$. Then $\alpha + \beta + \gamma$ equals",
  r"$10$",
  [(r"$30$", "Divides $(4, 3, 4) \\cdot (1, 2, 2) = 18$ by $|\\vec{b}| = 3$ instead of $9$, taking $\\lambda = 6$."),
   (r"$-10$", "Gets $\\lambda = -2$ by a sign slip in the perpendicularity equation."),
   (r"$9$", "Finds the image $(0, 5, 4)$ of the point in the line instead of the foot.")],
  r"The nearest point is the foot of the perpendicular. A point of the line is $(\lambda, 2\lambda, 2\lambda)$, and $(\lambda - 4) + 2(2\lambda - 3) + 2(2\lambda - 4) = 9\lambda - 18 = 0$ gives $\lambda = 2$. The point is $(2, 4, 4)$, so $\alpha + \beta + \gamma = 10$.",
  "Not recognising the nearest point as the foot of the perpendicular, or mis-normalising the projection.",
  "U11-B-nearest-point", "Recognise minimum distance as the foot, then compute it.",
  check=_c33, values=[10, 30, -10, 9], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $(\alpha, \beta, \gamma)$ be the point on the line $x = \frac{y}{2} = \frac{z}{2}$ that is nearest to the point $(4, 3, 4)$. Then $\alpha + \beta + \gamma$ is", answer=10))


def _c34():
    A, d = _M((1, -1, 2)), _M((1, 1, 1))
    P, Q = _M((-1, -1, 1)), _M((3, -1, -1))
    X = A + _t * d
    s = solve((X - P).dot(X - P) - (X - Q).dot(X - Q), _t)
    assert len(s) == 1
    return tuple(X.subs(_t, s[0]))
q("U11-B-034", TOP_PT, "Point of a line equidistant from two points", "Medium", "Multi-step computation MCQ",
  r"The point on the line $\frac{x-1}{1} = \frac{y+1}{1} = \frac{z-2}{1}$ that is equidistant from $P(-1, -1, 1)$ and $Q(3, -1, -1)$ is",
  r"$(3, 1, 4)$",
  [(r"$(-1, -3, 0)$", "Solves $4\\lambda - 8 = 0$ as $\\lambda = -2$ by a sign slip."),
   (r"$(1, -1, 0)$", "Gives the midpoint of $PQ$, which is equidistant from $P$ and $Q$ but is not on the line."),
   (r"$\left(\frac{3}{2}, -\frac{1}{2}, \frac{5}{2}\right)$", "Solves $4\\lambda = 8$ as $\\lambda = \\frac{4}{8}$.")],
  r"Let $X = (1 + \lambda, -1 + \lambda, 2 + \lambda)$. Then $XP^2 = (2 + \lambda)^2 + \lambda^2 + (1 + \lambda)^2$ and $XQ^2 = (\lambda - 2)^2 + \lambda^2 + (3 + \lambda)^2$. Expanding, $3\lambda^2 + 6\lambda + 5 = 3\lambda^2 + 2\lambda + 13$, i.e. $4\lambda = 8$, so $\lambda = 2$ and $X = (3, 1, 4)$.",
  "Forgetting that the required point must lie on the given line.",
  "U11-B-equidistant-point", "Distance equation reduces to linear in the parameter; two ideas combined.",
  check=_c34, values=[_pt(3, 1, 4), _pt(-1, -3, 0), _pt(1, -1, 0), (Rational(3, 2), Rational(-1, 2), Rational(5, 2))],
  cognitive="Application", source_class="XII")


def _c35():
    P, Q, R = _M((2, -1, 4)), _M((1, 3, 0)), _M((5, 1, 2))
    M = (Q + R) / 2
    return _lc(P, M - P)
q("U11-B-035", TOP_EQ, "Equation of a median", "Medium", "Multi-step computation MCQ",
  r"For the triangle with vertices $P(2, -1, 4)$, $Q(1, 3, 0)$ and $R(5, 1, 2)$, the equation of the median through $P$ is",
  r"$\frac{x-2}{1} = \frac{y+1}{3} = \frac{z-4}{-3}$",
  [(r"$\frac{x-2}{4} = \frac{y+1}{5} = \frac{z-4}{-2}$", "Uses $Q + R = (6, 4, 2)$ without halving, so the direction is $(6, 4, 2) - (2, -1, 4)$."),
   (r"$\frac{x-2}{2} = \frac{y+1}{-1} = \frac{z-4}{1}$", "Writes the line through $P$ parallel to $QR$ instead of the median."),
   (r"$\frac{x-3}{2} = \frac{y-2}{-1} = \frac{z-1}{4}$", "Passes through the midpoint $(3, 2, 1)$ but uses the position vector of $P$ as the direction.")],
  r"The midpoint of $QR$ is $M(3, 2, 1)$ and $\vec{PM} = (1, 3, -3)$. The median is $\frac{x-2}{1} = \frac{y+1}{3} = \frac{z-4}{-3}$.",
  "Using the sum of position vectors instead of their average for the midpoint.",
  "U11-B-median-line", "Midpoint then line through two points.",
  check=_c35, values=[_lc((2, -1, 4), (1, 3, -3)), _lc((2, -1, 4), (4, 5, -2)), _lc((2, -1, 4), (2, -1, 1)), _lc((3, 2, 1), (2, -1, 4))],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- DIFFICULT

def _c36():
    A, d, P = _M((-1, -2, 4)), _M((2, 1, -2)), _M((2, 1, 4))
    X = A + _t * d
    s = solve((X - P).dot(X - P) - 25, _t)
    assert len(s) == 2
    return simplify((X.subs(_t, s[0]) - X.subs(_t, s[1])).norm())
q("U11-B-036", TOP_PT, "Two points of a line at a given distance from an external point", "Difficult", "Multi-step computation MCQ",
  r"The line $\frac{x+1}{2} = \frac{y+2}{1} = \frac{z-4}{-2}$ contains exactly two points $R_1$ and $R_2$ at a distance $5$ from $P(2, 1, 4)$. Then $R_1R_2$ equals",
  r"$8$",
  [(r"$4$", "Finds the half-chord $\\sqrt{25 - 9} = 4$ and stops."),
   (r"$10$", "Assumes $P$ lies on the line, so the two points are $5$ on either side of $P$."),
   (r"$2\sqrt{34}$", "Adds instead of subtracting in Pythagoras: $2\\sqrt{25 + 9}$.")],
  r"Take $R = (-1 + 2\lambda, -2 + \lambda, 4 - 2\lambda)$. Then $PR^2 = (2\lambda - 3)^2 + (\lambda - 3)^2 + 4\lambda^2 = 9\lambda^2 - 18\lambda + 18 = 25$, so $9\lambda^2 - 18\lambda - 7 = 0$ with roots $\lambda = \frac{7}{3}, -\frac{1}{3}$. Hence $R_1R_2 = |\lambda_1 - \lambda_2| \cdot |(2, 1, -2)| = \frac{8}{3} \cdot 3 = 8$. (Equivalently, $P$ is at distance $3$ from the line, so $R_1R_2 = 2\sqrt{25 - 9} = 8$.)",
  "Treating the external point as if it were on the line.",
  "U11-B-points-at-distance-external", "Quadratic in the parameter or foot plus Pythagoras; geometric insight needed.",
  check=_c36, values=[8, 4, 10, 2*sqrt(34)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The line $\frac{x+1}{2} = \frac{y+2}{1} = \frac{z-4}{-2}$ contains exactly two points $R_1$ and $R_2$ at a distance $5$ from $P(2, 1, 4)$. Then the length $R_1R_2$ is", answer=8))


def _c37():
    A1, d1, d2, P = _M((1, 0, -1)), _M((1, 2, 2)), _M((2, -1, 1)), _M((3, 1, 0))
    Q = A1 + _t * d1
    s = solve((Q - P).dot(d2), _t)
    assert len(s) == 1
    return tuple(Q.subs(_t, s[0]))
q("U11-B-037", TOP_INT, "Line through a point meeting a line and perpendicular to another", "Difficult", "Multi-step computation MCQ",
  r"A line through $P(3, 1, 0)$ is perpendicular to the line $\frac{x+2}{2} = \frac{y-5}{-1} = \frac{z-1}{1}$ and meets the line $\frac{x-1}{1} = \frac{y}{2} = \frac{z+1}{2}$ at the point $Q$. Then $Q$ is",
  r"$(3, 4, 3)$",
  [(r"$(2, 2, 1)$", r"Drops the minus sign of the direction ratio $-1$ in the dot product: $2(\lambda - 2) + (2\lambda - 1) + (2\lambda - 1) = 6\lambda - 6 = 0$, so $\lambda = 1$."),
   (r"$(-1, -4, -5)$", "Gets $\\lambda = -2$ by a sign slip."),
   (r"$\left(\frac{5}{3}, \frac{4}{3}, \frac{1}{3}\right)$", "Imposes $\\vec{PQ}$ perpendicular to the line it meets instead of to the other line, getting $9\\lambda - 6 = 0$.")],
  r"Let $Q = (1 + \lambda, 2\lambda, -1 + 2\lambda)$, so $\vec{PQ} = (\lambda - 2, 2\lambda - 1, 2\lambda - 1)$. Perpendicular to $(2, -1, 1)$: $2(\lambda - 2) - (2\lambda - 1) + (2\lambda - 1) = 2\lambda - 4 = 0$, so $\lambda = 2$ and $Q = (3, 4, 3)$.",
  "Applying the perpendicularity condition to the wrong line.",
  "U11-B-line-meeting-line-perp", "Two lines play different roles; parameterise one and impose a condition from the other.",
  check=_c37, values=[_pt(3, 4, 3), _pt(2, 2, 1), _pt(-1, -4, -5), (Rational(5, 3), Rational(4, 3), Rational(1, 3))],
  cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"A line through $P(3, 1, 0)$ is perpendicular to the line $\frac{x+2}{2} = \frac{y-5}{-1} = \frac{z-1}{1}$ and meets the line $\frac{x-1}{1} = \frac{y}{2} = \frac{z+1}{2}$ at the point $Q(\alpha, \beta, \gamma)$. Then $\alpha + \beta + \gamma$ is", answer=10))


def _c38():
    # mirror L2: x/1 = (y+3)/2 = z/2 ; L1: (x-3)/2 = y/1 = (z-3)/1
    A2, d2 = _M((0, -3, 0)), _M((1, 2, 2))
    A1, d1 = _M((3, 0, 3)), _M((2, 1, 1))
    X, l, m = _inter(A1, d1, A2, d2)
    Pimg = _img(A1, A2, d2)
    return _lc(X, Pimg - X)
q("U11-B-038", TOP_FOOT, "Image of a line in an intersecting line", "Difficult", "Multi-step computation MCQ",
  r"The lines $L_1: \frac{x-3}{2} = \frac{y}{1} = \frac{z-3}{1}$ and $L_2: \frac{x}{1} = \frac{y+3}{2} = \frac{z}{2}$ intersect. The image of $L_1$ in $L_2$ (the line formed by the images in $L_2$ of all points of $L_1$) is",
  r"$\frac{x-1}{-2} = \frac{y+1}{5} = \frac{z-2}{5}$",
  [(r"$\frac{x-1}{-4} = \frac{y+1}{1} = \frac{z-2}{1}$", "Uses $(\\vec{b}_1 \\cdot \\hat{u})\\hat{u} - \\vec{b}_1$ for the reflected direction, missing the factor $2$."),
   (r"$\frac{x-1}{10} = \frac{y+1}{23} = \frac{z-2}{23}$", "Uses $2(\\vec{b}_1 \\cdot \\vec{b}_2)\\vec{b}_2 - \\vec{b}_1$ without dividing by $|\\vec{b}_2|^2 = 9$."),
   (r"$\frac{x-1}{22} = \frac{y+1}{35} = \frac{z-2}{35}$", "Gets the foot parameter of $(3, 0, 3)$ on $L_2$ as $-\\frac{5}{3}$ by a sign slip, so the image point is $\\left(-\\frac{19}{3}, -\\frac{38}{3}, -\\frac{29}{3}\\right)$, and joins it to $(1, -1, 2)$.")],
  r"Solving $3 + 2\lambda = \mu$, $\lambda = -3 + 2\mu$, $3 + \lambda = 2\mu$ gives $\lambda = -1$, $\mu = 1$, so the lines meet at $X(1, -1, 2)$. The foot of $(3, 0, 3)$ on $L_2$ has parameter $\frac{(3, 3, 3) \cdot (1, 2, 2)}{9} = \frac{5}{3}$, i.e. $\left(\frac{5}{3}, \frac{1}{3}, \frac{10}{3}\right)$, so its image is $\left(\frac{1}{3}, \frac{2}{3}, \frac{11}{3}\right)$. The image line passes through $X$ and this point, with direction $\left(-\frac{2}{3}, \frac{5}{3}, \frac{5}{3}\right)$, proportional to $(-2, 5, 5)$.",
  "Mis-normalising the reflection of a direction vector about a line.",
  "U11-B-image-of-line", "Intersection, then image of a point, then a line through two points.",
  check=_c38, values=[_lc((1, -1, 2), (-2, 5, 5)), _lc((1, -1, 2), (-4, 1, 1)), _lc((1, -1, 2), (10, 23, 23)), _lc((1, -1, 2), (22, 35, 35))],
  cognitive="Analysis", source_class="XII")


def _c39():
    A, d, P = _M((1, -1, 2)), _M((2, 1, -2)), _M((7, -1, -1))
    F = _foot(P, A, d)
    Q = 2 * F - P
    return simplify(((Q - P).cross(A - P)).norm() / 2)
q("U11-B-039", TOP_FOOT, "Area with a point and its image", "Difficult", "Multi-step computation MCQ",
  r"Let $Q$ be the image of the point $P(7, -1, -1)$ in the line $L: \frac{x-1}{2} = \frac{y+1}{1} = \frac{z-2}{-2}$, and let $S$ be the point $(1, -1, 2)$ on $L$. The area of triangle $PQS$ is",
  r"$18$",
  [(r"$36$", "Computes base times height, $6 \\cdot 6$, forgetting the factor $\\frac{1}{2}$."),
   (r"$9$", "Takes the base as $PF = 3$ (distance to the foot) instead of $PQ = 6$."),
   (r"$9\sqrt{5}$", "Takes the height as $SP = 3\\sqrt{5}$ instead of the distance $SF = 6$ from $S$ to the foot.")],
  r"Foot: $F = (1 + 2\lambda, -1 + \lambda, 2 - 2\lambda)$ with $\vec{PF} \cdot (2, 1, -2) = 2(2\lambda - 6) + \lambda - 2(3 - 2\lambda) = 9\lambda - 18 = 0$, so $\lambda = 2$ and $F = (5, 1, -2)$. Then $PF = \sqrt{4 + 4 + 1} = 3$, so $PQ = 6$, and $SF = 2 \cdot 3 = 6$ along the line. $PQ$ is perpendicular to $L$ at $F$, so the area is $\frac{1}{2} \cdot 6 \cdot 6 = 18$.",
  "Mixing up the distances to the foot, to the image, and to the given point of the line.",
  "U11-B-image-triangle-area", "Foot, image and a right-angle area argument combined.",
  check=_c39, values=[18, 36, 9, 9*sqrt(5)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $Q$ be the image of the point $P(7, -1, -1)$ in the line $L: \frac{x-1}{2} = \frac{y+1}{1} = \frac{z-2}{-2}$, and let $S$ be the point $(1, -1, 2)$ on $L$. The area of triangle $PQS$ is", answer=18))


def _c40():
    k = Symbol('k')
    A1, d1 = _M((1, -1, 2)), Matrix([2, 3, k])
    A2, d2 = _M((3, 4, 2)), _M((2, 1, -2))
    s = solve(list(A1 + _l * d1 - A2 - _m * d2), [_l, _m, k], dict=True)
    assert len(s) == 1
    return _cos(d1.subs(k, s[0][k]), d2)
q("U11-B-040", TOP_ANG, "Angle between lines that are forced to intersect", "Difficult", "Multi-step computation MCQ",
  r"The lines $\frac{x-1}{2} = \frac{y+1}{3} = \frac{z-2}{k}$ and $\frac{x-3}{2} = \frac{y-4}{1} = \frac{z-2}{-2}$ intersect. If $\theta$ is the acute angle between them, then $\cos\theta$ equals",
  r"$\frac{3}{\sqrt{14}}$",
  [(r"$\frac{5}{3\sqrt{14}}$", "Evaluates the $z$-coordinate of the second line as $2 + 2\\mu = 4$, so $k = 1$ and the dot product becomes $4 + 3 - 2 = 5$."),
   (r"$\frac{3}{14}$", "Finds $k = -1$ but divides $9$ by $|\\vec{b}_1|^2 |\\vec{b}_2| = 42$."),
   (r"$\frac{1}{\sqrt{14}}$", "Finds $k = -1$ but divides $9$ by $|\\vec{b}_1| |\\vec{b}_2|^2 = 9\\sqrt{14}$.")],
  r"From $x$ and $y$: $1 + 2\lambda = 3 + 2\mu$ and $-1 + 3\lambda = 4 + \mu$, giving $\lambda = 2$, $\mu = 1$, and the point $(5, 5, 0)$. The $z$-equation $2 + 2k = 0$ gives $k = -1$. Then $\cos\theta = \frac{|4 + 3 + 2|}{\sqrt{14} \cdot 3} = \frac{3}{\sqrt{14}}$.",
  "Sign slip with the negative ratio when finding the parameter that makes lines meet.",
  "U11-B-intersect-then-angle", "Parameter from intersection condition, then the angle; two chained ideas.",
  check=_c40, values=[3/sqrt(14), 5/(3*sqrt(14)), Rational(3, 14), 1/sqrt(14)], cognitive="Analysis", source_class="XII")


def _c41():
    A1, d1 = _M((2, 0, 1)), _M((1, -1, 1))
    A2, d2 = _M((2, -2, 2)), _M((1, 1, 2))
    s1 = _on(_img((4, 0, 2), A1, d1), A2, d2)
    s2 = simplify(_cos(d1, d2) - sqrt(2)/3) == 0
    return (bool(s1), bool(s2))
q("U11-B-041", TOP_FOOT, "Image and angle between two lines", "Difficult", "Statement-based MCQ",
  r"Let $L_1: \frac{x-2}{1} = \frac{y}{-1} = \frac{z-1}{1}$ and $L_2: \frac{x-2}{1} = \frac{y+2}{1} = \frac{z-2}{2}$. Statement I: The image of the point $(4, 0, 2)$ in $L_1$ lies on $L_2$. Statement II: The acute angle between $L_1$ and $L_2$ is $\cos^{-1}\left(\frac{\sqrt{2}}{3}\right)$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, "Takes the foot $(3, -1, 2)$ as the image, which is not on $L_2$, and divides the dot product $2$ by $|\\vec{b}_2|^2 = 6$, getting $\\frac{1}{3}$."),
   (ST_TF, "Finds the image correctly but divides the dot product by $|\\vec{b}_2|^2 = 6$, getting $\\cos\\theta = \\frac{1}{3}$."),
   (ST_FT, "Takes the foot $(3, -1, 2)$ as the image and finds it is not on $L_2$.")],
  r"On $L_1$, $F = (2 + \lambda, -\lambda, 1 + \lambda)$ and $\vec{PF} \cdot (1, -1, 1) = (\lambda - 2) + \lambda + (\lambda - 1) = 3\lambda - 3 = 0$, so $F = (3, -1, 2)$ and the image is $(2, -2, 2)$, which is the given point of $L_2$. So Statement I is true. Also $\cos\theta = \frac{|1 - 1 + 2|}{\sqrt{3}\sqrt{6}} = \frac{2}{3\sqrt{2}} = \frac{\sqrt{2}}{3}$, so Statement II is true.",
  "Confusing the foot with the image, and mis-normalising the angle formula.",
  "U11-B-statement-image-angle", "Image computation and membership plus an angle; both must be exact.",
  check=_c41, values=[(True, True), (False, False), (True, False), (False, True)],
  cognitive="Analysis", source_class="XII")


def _c42():
    A1, d1 = _M((1, 0, -1)), _M((1, 2, 2))
    A2, d2 = _M((12, 10, -3)), _M((11, 10, -2))
    X, l, m = _inter(A1, d1, A2, d2)
    Q = A2 + _t * d2
    dist2 = ((Q - A1).cross(d1)).dot((Q - A1).cross(d1)) / d1.dot(d1)
    s = solve(dist2 - 16, _t)
    assert len(s) == 2
    return simplify((Q.subs(_t, s[0]) - Q.subs(_t, s[1])).norm())
q("U11-B-042", TOP_ANG, "Points of one line at a given distance from another", "Difficult", "Multi-step computation MCQ",
  r"The lines $L_1: \frac{x-1}{1} = \frac{y}{2} = \frac{z+1}{2}$ and $L_2: \frac{x-12}{11} = \frac{y-10}{10} = \frac{z+3}{-2}$ intersect. $Q_1$ and $Q_2$ are the two points of $L_2$ whose perpendicular distance from $L_1$ is $4$. Then $Q_1Q_2$ equals",
  r"$10$",
  [(r"$8$", "Treats the lines as perpendicular, so each point is $4$ from the intersection point."),
   (r"$\frac{40}{3}$", "Uses $\\cos\\theta = \\frac{3}{5}$ in place of $\\sin\\theta$: $2 \\cdot \\frac{4}{3/5}$."),
   (r"$5$", "Finds the distance $\\frac{4}{\\sin\\theta} = 5$ of one point from the intersection and does not double it.")],
  r"The lines meet at $X(1, 0, -1)$. With directions $(1, 2, 2)$ and $(11, 10, -2)$, $\cos\theta = \frac{11 + 20 - 4}{3 \cdot 15} = \frac{3}{5}$, so $\sin\theta = \frac{4}{5}$. A point of $L_2$ at distance $s$ from $X$ is at distance $s\sin\theta$ from $L_1$, so $s = \frac{4}{4/5} = 5$ on each side of $X$, and $Q_1Q_2 = 10$.",
  "Using the cosine of the angle instead of the sine for perpendicular distance.",
  "U11-B-angle-distance-combo", "Intersection, angle, and a trigonometric distance argument.",
  check=_c42, values=[10, 8, Rational(40, 3), 5], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The lines $L_1: \frac{x-1}{1} = \frac{y}{2} = \frac{z+1}{2}$ and $L_2: \frac{x-12}{11} = \frac{y-10}{10} = \frac{z+3}{-2}$ intersect. $Q_1$ and $Q_2$ are the two points of $L_2$ whose perpendicular distance from $L_1$ is $4$. Then the length $Q_1Q_2$ is", answer=10))


def _c43():
    A1, d1 = _M((3, 3, 6)), _M((1, 2, 2))
    A2, d2 = _M((5, -5, 0)), _M((4, -4, -2))
    X, l, m = _inter(A1, d1, A2, d2)
    u1, u2 = d1 / d1.norm(), d2 / d2.norm()
    b = u1 + u2 if d1.dot(d2) > 0 else u1 - u2
    return _lc(X, b)
q("U11-B-043", TOP_ANG, "Bisector of the acute angle between two lines", "Difficult", "Multi-step computation MCQ",
  r"The lines $\frac{x-3}{1} = \frac{y-3}{2} = \frac{z-6}{2}$ and $\frac{x-5}{4} = \frac{y+5}{-4} = \frac{z}{-2}$ intersect at a point $X$. The line through $X$ that bisects the acute angle between them is",
  r"$\frac{x-1}{-1} = \frac{y+1}{4} = \frac{z-2}{3}$",
  [(r"$\frac{x-1}{3} = \frac{y+1}{0} = \frac{z-2}{1}$", "Adds the unit vectors $\\frac{1}{3}(1, 2, 2) + \\frac{1}{3}(2, -2, -1)$ without checking the sign of their dot product, which gives the bisector of the obtuse angle."),
   (r"$\frac{x-1}{-3} = \frac{y+1}{6} = \frac{z-2}{4}$", "Subtracts the direction vectors $(1, 2, 2) - (4, -4, -2)$ without first making them unit vectors."),
   (r"$\frac{x-1}{5} = \frac{y+1}{-2} = \frac{z-2}{0}$", "Adds the direction vectors $(1, 2, 2) + (4, -4, -2)$ without making them unit vectors and without checking the angle.")],
  r"Equating $x$ and $y$: $3 + \lambda = 5 + 4\mu$ and $3 + 2\lambda = -5 - 4\mu$; adding gives $\lambda = -2$, so $\mu = -1$, and the $z$-coordinates agree ($6 - 4 = 2 = 0 + 2$). So $X = (1, -1, 2)$. The unit directions are $\hat{u}_1 = \frac{1}{3}(1, 2, 2)$ and $\hat{u}_2 = \frac{1}{3}(2, -2, -1)$, with $\hat{u}_1 \cdot \hat{u}_2 = -\frac{4}{9} < 0$, so the acute angle is bisected by $\hat{u}_1 - \hat{u}_2 = \frac{1}{3}(-1, 4, 3)$. The bisector is $\frac{x-1}{-1} = \frac{y+1}{4} = \frac{z-2}{3}$.",
  "Adding unit vectors when their dot product is negative, which gives the obtuse bisector.",
  "U11-B-angle-bisector-line", "Intersection, unit vectors, and a sign test to pick the acute bisector.",
  check=_c43, values=[_lc((1, -1, 2), (-1, 4, 3)), _lc((1, -1, 2), (3, 0, 1)), _lc((1, -1, 2), (-3, 6, 4)), _lc((1, -1, 2), (5, -2, 0))],
  cognitive="Analysis", source_class="XII")


def _c44():
    k = Symbol('k')
    P = Matrix([k, 2, 1])
    Q = _img(P, (0, 0, 0), (1, 1, 1))
    return solve(Q[0], k)[0]
q("U11-B-044", TOP_FOOT, "Parameter fixed by a condition on the image", "Difficult", "Inverse/parameter MCQ",
  r"The image of the point $P(k, 2, 1)$ in the line $x = y = z$ has $x$-coordinate equal to $0$. Then $k$ equals",
  r"$6$",
  [(r"$\frac{3}{2}$", "Writes the image as $F - P$, forgetting the factor $2$: $\\frac{k+3}{3} - k = 0$."),
   (r"$-6$", "Takes the foot parameter as $k + 3$, forgetting to divide by $|\\vec{b}|^2 = 3$, and solves $2(k + 3) - k = 0$."),
   (r"$\frac{3}{5}$", "Takes $P$ as the midpoint of the foot and the image, writing the image as $2P - F$: $2k - \\frac{k+3}{3} = 0$.")],
  r"The foot is $F(\lambda, \lambda, \lambda)$ with $(\lambda - k) + (\lambda - 2) + (\lambda - 1) = 0$, so $\lambda = \frac{k+3}{3}$. The image is $2F - P$, whose $x$-coordinate is $\frac{2(k+3)}{3} - k$. Setting it to $0$: $2k + 6 = 3k$, so $k = 6$ (the image is $(0, 4, 5)$).",
  "Applying a condition meant for the image to the foot, or reversing the midpoint relation.",
  "U11-B-image-param", "Image as a function of the parameter, then a condition on it.",
  check=_c44, values=[6, Rational(3, 2), -6, Rational(3, 5)], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The image of the point $P(k, 2, 1)$ in the line $x = y = z$ has $x$-coordinate equal to $0$. Then the value of $k$ is", answer=6))


def _c45():
    A1, d1 = _M((1, 2, -1)), _M((1, -1, 2))
    A2, d2 = _M((0, 0, 2)), _M((2, 1, -1))
    X, l, m = _inter(A1, d1, A2, d2)
    return _lc(X, d1.cross(d2))
q("U11-B-045", TOP_INT, "Line through the intersection perpendicular to both lines", "Difficult", "Multi-step computation MCQ",
  r"The lines $\frac{x-1}{1} = \frac{y-2}{-1} = \frac{z+1}{2}$ and $\frac{x}{2} = \frac{y}{1} = \frac{z-2}{-1}$ intersect at a point $X$. The line through $X$ perpendicular to both of them is",
  r"$\frac{x-2}{-1} = \frac{y-1}{5} = \frac{z-1}{3}$",
  [(r"$\frac{x-2}{-1} = \frac{y-1}{-5} = \frac{z-1}{3}$", "Forgets the minus sign on the $\\hat{j}$ component of the cross product."),
   (r"$\frac{x-2}{3} = \frac{y-1}{0} = \frac{z-1}{1}$", "Adds the two direction vectors instead of taking their cross product."),
   (r"$\frac{x-1}{-1} = \frac{y-2}{5} = \frac{z+1}{3}$", "Uses the correct direction but passes the line through the given point $(1, 2, -1)$ of the first line instead of through $X$.")],
  r"Solving $1 + \lambda = 2\mu$, $2 - \lambda = \mu$ gives $\mu = 1$, $\lambda = 1$, and the $z$-coordinates agree: $-1 + 2 = 1 = 2 - 1$. So $X = (2, 1, 1)$. The direction is $(1, -1, 2) \times (2, 1, -1) = (1 - 2, 4 + 1, 1 + 2) = (-1, 5, 3)$, giving $\frac{x-2}{-1} = \frac{y-1}{5} = \frac{z-1}{3}$.",
  "Sign error in the cross product, or anchoring the line at the wrong point.",
  "U11-B-perp-at-intersection", "Intersection, cross product, then line equation; three chained steps.",
  check=_c45, values=[_lc((2, 1, 1), (-1, 5, 3)), _lc((2, 1, 1), (-1, -5, 3)), _lc((2, 1, 1), (3, 0, 1)), _lc((1, 2, -1), (-1, 5, 3))],
  cognitive="Analysis", source_class="XII")


def _c46():
    k = Symbol('k')
    P, Q = _M((-1, 0, 4)), Matrix([4, 5, k])
    A2, d2 = _M((3, 13, -12)), _M((2, -1, 2))
    s = solve(list(P + _l * (Q - P) - A2 - _m * d2), [_l, _m, k], dict=True)
    assert len(s) == 1
    l = s[0][_l]
    return simplify(l / (1 - l))  # signed ratio PR : RQ (negative means external)
q("U11-B-046", TOP_INT, "Ratio in which an intersection point divides a segment", "Difficult", "Multi-step computation MCQ",
  r"The line through $P(-1, 0, 4)$ and $Q(4, 5, k)$ meets the line $\frac{x-3}{2} = \frac{y-13}{-1} = \frac{z+12}{2}$ at the point $R$. Then $R$ divides the segment $PQ$ in the ratio",
  r"$2 : 1$ externally",
  [(r"$2 : 1$ internally", "Finds the parameter $\\lambda = 2$ correctly and takes $PR : RQ = 2 : 1$ without noticing that $\\lambda > 1$ puts $R$ beyond $Q$."),
   (r"$1 : 2$ externally", "Writes the ratio as $RQ : PR$ instead of $PR : RQ$."),
   (r"$1 : 2$ internally", "Writes the ratio as $RQ : PR$ and also ignores that $R$ lies outside the segment.")],
  r"Points of $PQ$ are $(-1 + 5\lambda, 5\lambda, 4 + (k - 4)\lambda)$ and of the other line $(3 + 2\mu, 13 - \mu, -12 + 2\mu)$. The $x$ and $y$ equations $5\lambda - 4 = 2\mu$ and $5\lambda = 13 - \mu$ give $\lambda = 2$, $\mu = 3$, so $R = (9, 10, -6)$, and the $z$ equation $4 + 2(k - 4) = -6$ fixes $k = -1$. Since $\vec{PR} = 2\vec{PQ}$, $R$ lies beyond $Q$ with $PR = 2PQ$ and $RQ = PQ$, so $R$ divides $PQ$ externally in the ratio $2 : 1$.",
  "Reading the parameter as an internal ratio without checking whether the point lies between $P$ and $Q$.",
  "U11-B-intersection-ratio", "Intersection with an unknown coordinate fixed by the consistency equation, then recognising external division from $\\lambda > 1$; a deliberate internal/external trap.",
  check=_c46, values=[Integer(-2), Integer(2), Rational(-1, 2), Rational(1, 2)], cognitive="Analysis", source_class="XII")


def _c47():
    P, A, d = _M((2, -2, 4)), _M((-1, -2, 1)), _M((2, 2, 1))
    h = _dist(P, A, d)
    s = Symbol('s', positive=True)
    side = solve(s * sqrt(3) / 2 - h, s)[0]
    return simplify(side**2)
q("U11-B-047", TOP_FOOT, "Equilateral triangle with a side on a line", "Difficult", "Multi-step computation MCQ",
  r"Points $Q$ and $R$ lie on the line $\frac{x+1}{2} = \frac{y+2}{2} = \frac{z-1}{1}$ such that $PQR$ is an equilateral triangle, where $P$ is the point $(2, -2, 4)$. Then $QR^2$ equals",
  r"$12$",
  [(r"$9$", "Takes the side equal to the altitude, the distance $3$ of $P$ from the line."),
   (r"$36$", "Takes the side as twice the altitude, $6$."),
   (r"$27$", "Uses side $= \\sqrt{3} \\times$ altitude instead of $\\frac{2}{\\sqrt{3}} \\times$ altitude.")],
  r"Foot of $P$: $F = (-1 + 2\lambda, -2 + 2\lambda, 1 + \lambda)$ with $\vec{PF} \cdot (2, 2, 1) = 2(2\lambda - 3) + 2(2\lambda) + (\lambda - 3) = 9\lambda - 9 = 0$, so $F = (1, 0, 2)$ and the altitude is $PF = \sqrt{1 + 4 + 4} = 3$. For an equilateral triangle, altitude $= \frac{\sqrt{3}}{2} \times$ side, so side $= 2\sqrt{3}$ and $QR^2 = 12$.",
  "Mixing up the altitude and side of an equilateral triangle.",
  "U11-B-equilateral-on-line", "Perpendicular distance then equilateral triangle geometry.",
  check=_c47, values=[12, 9, 36, 27], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Points $Q$ and $R$ lie on the line $\frac{x+1}{2} = \frac{y+2}{2} = \frac{z-1}{1}$ such that $PQR$ is an equilateral triangle, where $P$ is the point $(2, -2, 4)$. Then the value of $QR^2$ is", answer=12))
