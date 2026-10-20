import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

X, Y = symbols('x y', real=True)
T_ = Symbol('t', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TOP_STD = "Parabola: standard forms"
TOP_SHIFT = "Parabola: shifted forms"
TOP_EQN = "Parabola: equation from data"
TOP_FOC = "Parabola: focal distance"
TOP_INT = "Parabola: intersection with lines"


def _ln(a, b, c):
    """Line a x + b y + c = 0 as a normalised coefficient tuple."""
    a, b, c = sympify(a), sympify(b), sympify(c)
    lead = a if a != 0 else b
    return tuple(simplify(v / lead) for v in (a, b, c))


def _key(expr):
    """Canonical coefficient tuple of a second-degree curve expr = 0."""
    p = Poly(expand(expr), X, Y)
    mons = [X**2, X*Y, Y**2, X, Y, Integer(1)]
    cs = [p.coeff_monomial(m) for m in mons]
    lead = [c for c in cs if c != 0][0]
    return tuple(simplify(c / lead) for c in cs)


def _par(expr):
    """Data of an axis-parallel parabola expr = 0, computed by completing the square."""
    p = Poly(expand(expr), X, Y)
    if p.coeff_monomial(Y**2) != 0 and p.coeff_monomial(X**2) == 0:
        xs = solve(expr, X)[0]
        A = diff(xs, Y, 2) / 2
        y0 = solve(diff(xs, Y), Y)[0]
        x0 = simplify(xs.subs(Y, y0))
        a = 1 / (4 * A)
        return dict(vertex=(x0, y0), focus=(x0 + a, y0), directrix=_ln(1, 0, -(x0 - a)),
                    axis=_ln(0, 1, -y0), a=a, lr=Abs(4 * a))
    ys = solve(expr, Y)[0]
    A = diff(ys, X, 2) / 2
    x0 = solve(diff(ys, X), X)[0]
    y0 = simplify(ys.subs(X, x0))
    a = 1 / (4 * A)
    return dict(vertex=(x0, y0), focus=(x0, y0 + a), directrix=_ln(0, 1, -(y0 - a)),
                axis=_ln(1, 0, -x0), a=a, lr=Abs(4 * a))


def _dist(P, Q):
    return sqrt((P[0] - Q[0])**2 + (P[1] - Q[1])**2)


def _meet(curve, line):
    """Real intersection points of curve = 0 and line = 0."""
    sols = solve([curve, line], [X, Y], dict=True)
    return [(s[X], s[Y]) for s in sols if s[X].is_real and s[Y].is_real]


def _area(P, Q, R):
    return Abs(P[0]*(Q[1]-R[1]) + Q[0]*(R[1]-P[1]) + R[0]*(P[1]-Q[1])) / 2


# ================================================================ EASY
# ---------------------------------------------------------------- 001
q("U10-D-001", TOP_STD, "Focus of y^2 = -4ax", "Easy", "Single-step computation MCQ",
  r"The focus of the parabola $y^2 = -12x$ is",
  r"$(-3, 0)$",
  [(r"$(3, 0)$", r"Ignores the negative sign: treats $y^2 = -12x$ as $y^2 = 12x$, which opens to the right."),
   (r"$(-12, 0)$", r"Takes $a = 12$, reading the coefficient $4a$ as $a$."),
   (r"$(0, -3)$", r"Places the focus on the $y$-axis, mixing up the forms $y^2 = -4ax$ and $x^2 = -4ay$.")],
  r"Comparing with $y^2 = -4ax$ gives $4a = 12$, so $a = 3$. The parabola opens towards the negative $x$-axis, so the focus is $(-a, 0) = (-3, 0)$.",
  r"Reading $4a$ as $a$, or ignoring the sign that fixes the direction of opening.",
  "U10-D-std-focus", "One comparison with a standard form and one sign decision.",
  check=lambda: _par(Y**2 + 12*X)["focus"], values=[(-3, 0), (3, 0), (-12, 0), (0, -3)], cognitive="Recall")

# ---------------------------------------------------------------- 002
q("U10-D-002", TOP_STD, "Directrix of x^2 = 4ay", "Easy", "Single-step computation MCQ",
  r"The equation of the directrix of the parabola $x^2 = 10y$ is",
  r"$y = -\frac{5}{2}$",
  [(r"$y = \frac{5}{2}$", r"Gives the line $y = a$ through the focus $(0, \frac{5}{2})$ rather than the line on the opposite side of the vertex."),
   (r"$x = -\frac{5}{2}$", r"Uses the directrix $x = -a$ of $y^2 = 4ax$, mixing up the two standard forms."),
   (r"$y = -10$", r"Takes $a = 10$, reading $4a$ as $a$.")],
  r"Comparing with $x^2 = 4ay$, $4a = 10$ so $a = \frac{5}{2}$. The parabola opens upward with focus $(0, \frac{5}{2})$, so the directrix is $y = -a$, that is $y = -\frac{5}{2}$.",
  r"Confusing the directrix with the line through the focus, or reading $4a$ as $a$.",
  "U10-D-std-directrix", "Single comparison with $x^2 = 4ay$.",
  check=lambda: _par(X**2 - 10*Y)["directrix"],
  values=[_ln(0, 1, Rational(5, 2)), _ln(0, 1, -Rational(5, 2)), _ln(1, 0, Rational(5, 2)), _ln(0, 1, 10)],
  cognitive="Recall")

# ---------------------------------------------------------------- 003
q("U10-D-003", TOP_STD, "Latus rectum when y^2 has a coefficient", "Easy", "Single-step computation MCQ",
  r"The length of the latus rectum of the parabola $3y^2 = 16x$ is",
  r"$\frac{16}{3}$",
  [(r"$16$", r"Ignores the coefficient $3$ of $y^2$ and reads $4a = 16$ directly."),
   (r"$\frac{4}{3}$", r"Gives $a = \frac{4}{3}$ instead of the latus rectum $4a$."),
   (r"$\frac{64}{3}$", r"Takes $a = \frac{16}{3}$ and then multiplies by $4$.")],
  r"Dividing by $3$, $y^2 = \frac{16}{3}x$, so $4a = \frac{16}{3}$. The latus rectum has length $4a = \frac{16}{3}$.",
  r"Reading the latus rectum from the equation before reducing it to the form $y^2 = 4ax$.",
  "U10-D-std-latus-rectum", "One reduction to standard form and one recall.",
  check=lambda: _par(3*Y**2 - 16*X)["lr"], values=[Rational(16, 3), 16, Rational(4, 3), Rational(64, 3)],
  cognitive="Application")

# ---------------------------------------------------------------- 004
def _c004():
    d = _par(Y**2 - 8*X)
    P = (6, sqrt(8*6))
    return simplify(_dist(P, d["focus"]))
q("U10-D-004", TOP_FOC, "Focal distance from the abscissa", "Easy", "Single-step computation MCQ",
  r"A point $P$ on the parabola $y^2 = 8x$ has abscissa $6$. The distance of $P$ from the focus of the parabola is",
  r"$8$",
  [(r"$4$", r"Uses $x_1 - a = 6 - 2$ for the focal distance, subtracting $a$."),
   (r"$14$", r"Uses $x_1 + 4a = 6 + 8$, adding the latus rectum length."),
   (r"$2\sqrt{21}$", r"Finds the distance of $P(6, 4\sqrt{3})$ from the vertex: $\sqrt{36 + 48} = \sqrt{84}$.")],
  r"Here $a = 2$. By the focus-directrix property, the focal distance of $(x_1, y_1)$ on $y^2 = 4ax$ equals its distance from the directrix $x = -a$, namely $x_1 + a = 6 + 2 = 8$.",
  r"Using $x_1 - a$ for the focal distance, or measuring from the vertex.",
  "U10-D-focal-distance-direct", "One property (focal distance $= x_1 + a$) used once.",
  check=_c004, values=[8, 4, 14, 2*sqrt(21)], cognitive="Application",
  numerical=dict(question=r"A point $P$ on the parabola $y^2 = 8x$ has abscissa $6$. The distance of $P$ from the focus of the parabola is", answer=8))

# ---------------------------------------------------------------- 005
q("U10-D-005", TOP_SHIFT, "Vertex by completing the square", "Easy", "Single-step computation MCQ",
  r"The vertex of the parabola $y^2 - 4y - 8x + 28 = 0$ is",
  r"$(3, 2)$",
  [(r"$(2, 3)$", r"Completes the square correctly to $(y - 2)^2 = 8(x - 3)$ but writes the coordinates in the order $(k, h)$."),
   (r"$(-3, 2)$", r"Reads $(y-2)^2 = 8(x-3)$ with a sign slip in the $x$-shift."),
   (r"$(3, -2)$", r"Reads $(y-2)^2$ as a shift of $-2$ in $y$.")],
  r"$y^2 - 4y = (y - 2)^2 - 4$, so the equation becomes $(y - 2)^2 = 8x - 24 = 8(x - 3)$. The vertex is $(3, 2)$.",
  r"Sign slips when reading the shifts from $(y - k)^2 = 4a(x - h)$.",
  "U10-D-shift-vertex", "One completion of the square.",
  check=lambda: _par(Y**2 - 4*Y - 8*X + 28)["vertex"], values=[(3, 2), (2, 3), (-3, 2), (3, -2)],
  cognitive="Application")

# ---------------------------------------------------------------- 006
def _c006():
    S = (0, -4)
    return _key((X - S[0])**2 + (Y - S[1])**2 - (Y - 4)**2)
q("U10-D-006", TOP_EQN, "Equation from focus and directrix (origin vertex)", "Easy", "Single-step computation MCQ",
  r"The parabola with focus $(0, -4)$ and directrix $y = 4$ has equation",
  r"$x^2 = -16y$",
  [(r"$x^2 = 16y$", r"Uses the correct $a = 4$ but makes the parabola open upward, towards the directrix."),
   (r"$y^2 = -16x$", r"Uses the form $y^2 = -4ax$, placing the axis along the $x$-axis."),
   (r"$x^2 = -8y$", r"Takes the focus-to-directrix distance $8$ as $4a$, so $a = 2$.")],
  r"The vertex is midway between the focus and the directrix, at the origin, with $a = 4$. The focus is below the vertex, so the parabola opens downward: $x^2 = -4ay = -16y$. Equivalently, $x^2 + (y + 4)^2 = (y - 4)^2$ simplifies to $x^2 = -16y$.",
  r"Taking the focus-to-directrix distance as $4a$ instead of $2a$.",
  "U10-D-eqn-focus-directrix", "Locate the vertex and $a$, then pick the form.",
  check=_c006, values=[_key(X**2 + 16*Y), _key(X**2 - 16*Y), _key(Y**2 + 16*X), _key(X**2 + 8*Y)],
  cognitive="Application")

# ---------------------------------------------------------------- 007
def _c007():
    a = Rational(12, 4)
    x1 = solve(Eq(X + a, 9), X)[0]
    return [s for s in solve(Y**2 - 12*x1, Y) if s > 0][0]
q("U10-D-007", TOP_FOC, "Point from a given focal distance", "Easy", "Inverse/parameter MCQ",
  r"A point $P$ in the first quadrant lies on the parabola $y^2 = 12x$, and its distance from the focus is $9$. The ordinate of $P$ is",
  r"$6\sqrt{2}$",
  [(r"$6\sqrt{3}$", r"Takes the abscissa itself as $9$, so $y^2 = 108$."),
   (r"$12$", r"Uses $x - a = 9$, giving $x = 12$ and $y^2 = 144$."),
   (r"$6$", r"Uses $x + 2a = 9$, giving $x = 3$ and $y^2 = 36$.")],
  r"Here $a = 3$ and the focal distance is $x + a$. So $x + 3 = 9$ gives $x = 6$, and $y^2 = 72$, so $y = 6\sqrt{2}$ in the first quadrant.",
  r"Equating the abscissa itself, or $x - a$, to the focal distance.",
  "U10-D-focal-distance-reverse", "Reverse use of the focal distance formula, then one substitution.",
  check=_c007, values=[6*sqrt(2), 6*sqrt(3), 12, 6], cognitive="Application")

# ---------------------------------------------------------------- 008
def _c008():
    d = _par(X**2 + 8*Y)
    pts = _meet(X**2 + 8*Y, Y - d["focus"][1])
    return FiniteSet(*[Tuple(*p) for p in pts])
q("U10-D-008", TOP_STD, "Ends of the latus rectum", "Easy", "Single-step computation MCQ",
  r"The end points of the latus rectum of the parabola $x^2 = -8y$ are",
  r"$(4, -2)$ and $(-4, -2)$",
  [(r"$(4, 2)$ and $(-4, 2)$", r"Takes the focus at $(0, 2)$, as if the parabola opened upward."),
   (r"$(-2, 4)$ and $(-2, -4)$", r"Uses the end points $(-a, \pm 2a)$ of $y^2 = -4ax$, mixing up the forms."),
   (r"$(8, -2)$ and $(-8, -2)$", r"Takes the half-length of the latus rectum as $4a = 8$ instead of $2a = 4$.")],
  r"Here $4a = 8$, so $a = 2$ and the focus is $(0, -2)$. The latus rectum is the chord $y = -2$; then $x^2 = 16$ gives $x = \pm 4$. The end points are $(\pm 4, -2)$.",
  r"Using $4a$ instead of $2a$ for the half-length of the latus rectum.",
  "U10-D-lr-endpoints", "Recall of the focus and one substitution.",
  check=_c008,
  values=[FiniteSet(Tuple(4, -2), Tuple(-4, -2)), FiniteSet(Tuple(4, 2), Tuple(-4, 2)),
          FiniteSet(Tuple(-2, 4), Tuple(-2, -4)), FiniteSet(Tuple(8, -2), Tuple(-8, -2))],
  cognitive="Application")

# ---------------------------------------------------------------- 009
q("U10-D-009", TOP_SHIFT, "Axis of a shifted parabola", "Easy", "Direct concept MCQ",
  r"The axis of the parabola $(x + 1)^2 = -6(y - 3)$ is the line",
  r"$x = -1$",
  [(r"$y = 3$", r"Gives the line through the vertex perpendicular to the axis."),
   (r"$x = 1$", r"Reads $(x + 1)^2$ as a shift of $+1$ in $x$."),
   (r"$y = \frac{9}{2}$", r"Gives the directrix $y = 3 + \frac{3}{2}$, which is perpendicular to the axis.")],
  r"The squared term is in $x$, so the axis is parallel to the $y$-axis and passes through the vertex $(-1, 3)$. The axis is $x = -1$.",
  r"Confusing the axis with the line through the vertex perpendicular to it.",
  "U10-D-shift-axis", "One recognition step.",
  check=lambda: _par((X + 1)**2 + 6*(Y - 3))["axis"],
  values=[_ln(1, 0, 1), _ln(0, 1, -3), _ln(1, 0, -1), _ln(0, 1, -Rational(9, 2))], cognitive="Understanding")

# ---------------------------------------------------------------- 010
def _c010():
    a = Symbol('a')
    av = solve(Eq((-6)**2, 4*a*2), a)[0]
    return 4*av
q("U10-D-010", TOP_EQN, "Latus rectum from a point on the curve", "Easy", "Single-step computation MCQ",
  r"If the parabola $y^2 = 4ax$ passes through the point $(2, -6)$, then the length of its latus rectum is",
  r"$18$",
  [(r"$\frac{9}{2}$", r"Stops at $a = \frac{9}{2}$ and reports it as the latus rectum."),
   (r"$9$", r"Reports $2a$, the semi-latus rectum."),
   (r"$72$", r"Solves $36 = 2a$, taking $a = 18$, and then gives $4a$.")],
  r"Substituting, $36 = 4a(2)$, so $4a = 18$. The latus rectum is $4a = 18$.",
  r"Reporting $a$ or $2a$ when the latus rectum $4a$ is asked.",
  "U10-D-lr-from-point", "One substitution.",
  check=_c010, values=[18, Rational(9, 2), 9, 72], cognitive="Application",
  numerical=dict(question=r"If the parabola $y^2 = 4ax$ passes through the point $(2, -6)$, then the length of its latus rectum is", answer=18))

# ---------------------------------------------------------------- 011
q("U10-D-011", TOP_SHIFT, "Directrix of a horizontally shifted parabola", "Easy", "Single-step computation MCQ",
  r"The directrix of the parabola $y^2 = 4(x - 2)$ is",
  r"$x = 1$",
  [(r"$x = -1$", r"Uses the directrix $x = -a$ of $y^2 = 4x$, ignoring the shift of the vertex to $(2, 0)$."),
   (r"$x = 3$", r"Gives the line $x = 2 + a$ through the focus."),
   (r"$x = -3$", r"Writes the directrix as $x = -(h + a) = -(2 + 1)$.")],
  r"The vertex is $(2, 0)$ and $4a = 4$ gives $a = 1$. The parabola opens to the right, so the directrix is $x = 2 - 1 = 1$.",
  r"Forgetting to shift the directrix with the vertex.",
  "U10-D-shift-directrix", "One shift applied to a standard result.",
  check=lambda: _par(Y**2 - 4*(X - 2))["directrix"],
  values=[_ln(1, 0, -1), _ln(1, 0, 1), _ln(1, 0, -3), _ln(1, 0, 3)], cognitive="Application")

# ---------------------------------------------------------------- 012
def _c012():
    pts = [p for p in _meet(Y**2 - 4*X, Y - X) if p != (0, 0)]
    return simplify(_dist(pts[0], _par(Y**2 - 4*X)["focus"]))
q("U10-D-012", TOP_INT, "Second intersection with a line through the vertex", "Easy", "Multi-step computation MCQ",
  r"The line $y = x$ meets the parabola $y^2 = 4x$ at the origin and at one more point $P$. The distance of $P$ from the focus of the parabola is",
  r"$5$",
  [(r"$4\sqrt{2}$", r"Finds $P(4, 4)$ but gives its distance $OP$ from the vertex."),
   (r"$4$", r"Takes the abscissa of $P$ as the focal distance."),
   (r"$3$", r"Uses $x_1 - a = 4 - 1$.")],
  r"Substituting $y = x$ gives $x^2 = 4x$, so $x = 0$ or $x = 4$, and $P = (4, 4)$. With $a = 1$, the focal distance is $x_1 + a = 5$.",
  r"Measuring from the vertex instead of the focus.",
  "U10-D-int-line-focal", "Intersection with a line, then the focal distance rule.",
  check=_c012, values=[5, 4*sqrt(2), 4, 3], cognitive="Application",
  numerical=dict(question=r"The line $y = x$ meets the parabola $y^2 = 4x$ at the origin and at one more point $P$. The distance of $P$ from the focus of the parabola is", answer=5))

# ---------------------------------------------------------------- 013
def _c013():
    fy = solve(Eq(3*0 + 2*Y - 12, 0), Y)[0]   # focus: where the line meets the y-axis
    return _key(X**2 - 4*fy*Y)
q("U10-D-013", TOP_EQN, "Equation when the focus lies on a given line", "Easy", "Single-step computation MCQ",
  r"A parabola has its vertex at the origin and its axis along the $y$-axis, and its focus lies on the line $3x + 2y - 12 = 0$. The equation of the parabola is",
  r"$x^2 = 24y$",
  [(r"$x^2 = -24y$", r"Sign slip: finds the focus $(0, 6)$ but uses the downward form $x^2 = -4ay$ with $a = 6$."),
   (r"$x^2 = 6y$", r"Takes $4a = 6$ from the focus $(0, 6)$ instead of $a = 6$."),
   (r"$x^2 = 16y$", r"Uses the $x$-intercept $4$ of the line as $a$, giving $x^2 = 4(4)y$.")],
  r"The focus lies on the axis, the $y$-axis, so it is where $3x + 2y - 12 = 0$ meets $x = 0$: $2y = 12$, focus $(0, 6)$. Thus $a = 6$ and the parabola opens upward: $x^2 = 4(6)y = 24y$.",
  r"Equating $4a$ (instead of $a$) to the distance of the focus from the vertex, or locating the focus at the wrong intercept.",
  "U10-D-eqn-focus-on-line", "Locate the focus as an axis intercept, then one substitution into the standard form.",
  check=_c013, values=[_key(X**2 - 24*Y), _key(X**2 + 24*Y), _key(X**2 - 6*Y), _key(X**2 - 16*Y)],
  cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    d = _par(X**2 + 20*Y)
    ends = _meet(X**2 + 20*Y, Y - d["focus"][1])
    return _area(d["vertex"], ends[0], ends[1])
q("U10-D-014", TOP_STD, "Triangle on the latus rectum", "Easy", "Multi-step computation MCQ",
  r"The area of the triangle whose vertices are the vertex of the parabola $x^2 = -20y$ and the two end points of its latus rectum is",
  r"$50$",
  [(r"$100$", r"Uses base $\times$ height without the factor $\frac{1}{2}$."),
   (r"$25$", r"Takes the base as $2a = 10$ (half the latus rectum)."),
   (r"$200$", r"Takes the height as $4a = 20$ instead of $a = 5$.")],
  r"Here $a = 5$; the latus rectum lies on $y = -5$ and has length $4a = 20$. The vertex is at distance $5$ from it, so the area is $\frac{1}{2}(20)(5) = 50$.",
  r"Mixing $a$, $2a$ and $4a$ for the height and the base.",
  "U10-D-lr-triangle", "Two recalled lengths and the triangle area formula.",
  check=_c014, values=[50, 100, 25, 200], cognitive="Application",
  numerical=dict(question=r"The area of the triangle whose vertices are the vertex of the parabola $x^2 = -20y$ and the two end points of its latus rectum is", answer=50))

# ---------------------------------------------------------------- 015
def _c015():
    d = _par(2*X**2 + 7*Y)
    S = d["focus"]
    A_, B_, C_ = d["directrix"]
    return Abs(A_*S[0] + B_*S[1] + C_) / sqrt(A_**2 + B_**2)
q("U10-D-015", TOP_STD, "Focus to directrix distance", "Easy", "Single-step computation MCQ",
  r"The distance between the focus and the directrix of the parabola $2x^2 = -7y$ is",
  r"$\frac{7}{4}$",
  [(r"$\frac{7}{8}$", r"Gives $a = \frac{7}{8}$, the vertex-to-focus distance."),
   (r"$\frac{7}{2}$", r"Ignores the coefficient $2$ of $x^2$, so $a = \frac{7}{4}$ and $2a = \frac{7}{2}$."),
   (r"$7$", r"Ignores the coefficient $2$ and reports $4a = 7$.")],
  r"Writing $x^2 = -\frac{7}{2}y$, $4a = \frac{7}{2}$ so $a = \frac{7}{8}$. The focus and directrix are each at distance $a$ from the vertex on opposite sides, so they are $2a = \frac{7}{4}$ apart.",
  r"Using $a$ for the focus-directrix distance, which is $2a$.",
  "U10-D-std-focus-directrix-gap", "Reduce to standard form, then one recalled relation.",
  check=_c015, values=[Rational(7, 4), Rational(7, 8), Rational(7, 2), 7], cognitive="Application")


# ================================================================ MEDIUM
# ---------------------------------------------------------------- 016
q("U10-D-016", TOP_SHIFT, "Focus of a left-opening shifted parabola", "Medium", "Multi-step computation MCQ",
  r"The focus of the parabola $y^2 + 6y + 4x + 5 = 0$ is",
  r"$(0, -3)$",
  [(r"$(2, -3)$", r"Gets the vertex $(1, -3)$ and $a = 1$ but moves to the right, as if the parabola opened towards positive $x$."),
   (r"$(-1, -3)$", r"Uses the focus $(-a, 0)$ of $y^2 = -4ax$ and shifts only the $y$-coordinate, ignoring the vertex abscissa $1$."),
   (r"$(1, -4)$", r"Moves a distance $a$ from the vertex along the $y$-direction, taking the wrong axis.")],
  r"$y^2 + 6y = (y + 3)^2 - 9$, so $(y + 3)^2 = -4x + 4 = -4(x - 1)$. The vertex is $(1, -3)$, $a = 1$, and the parabola opens to the left, so the focus is $(1 - 1, -3) = (0, -3)$.",
  r"Losing the direction of opening after completing the square.",
  "U10-D-shift-focus", "Completing the square, reading the sign of $4a$, then shifting the focus.",
  check=lambda: _par(Y**2 + 6*Y + 4*X + 5)["focus"], values=[(0, -3), (2, -3), (-1, -3), (1, -4)])

# ---------------------------------------------------------------- 017
q("U10-D-017", TOP_SHIFT, "Directrix of an upward shifted parabola", "Medium", "Multi-step computation MCQ",
  r"The directrix of the parabola $x^2 - 4x - 8y + 12 = 0$ is",
  r"$y = -1$",
  [(r"$y = 3$", r"Gives the line $y = 1 + a$ through the focus $(2, 3)$."),
   (r"$y = -2$", r"Uses the directrix $y = -a$ of $x^2 = 8y$, ignoring the vertex shift."),
   (r"$y = -3$", r"Places the directrix at distance $2a = 4$ below the vertex $(2, 1)$.")],
  r"$x^2 - 4x = (x - 2)^2 - 4$, so $(x - 2)^2 = 8y - 8 = 8(y - 1)$. The vertex is $(2, 1)$ and $a = 2$; the parabola opens upward, so the directrix is $y = 1 - 2 = -1$.",
  r"Forgetting the vertex shift, or using $2a$ for the vertex-directrix distance.",
  "U10-D-shift-directrix", "Completing the square and placing the directrix relative to the vertex.",
  check=lambda: _par(X**2 - 4*X - 8*Y + 12)["directrix"],
  values=[_ln(0, 1, 1), _ln(0, 1, -3), _ln(0, 1, 2), _ln(0, 1, 3)])

# ---------------------------------------------------------------- 018
def _c018():
    V, S = (2, 3), (2, 5)
    a = S[1] - V[1]
    return _key((X - V[0])**2 - 4*a*(Y - V[1]))
q("U10-D-018", TOP_EQN, "Equation from vertex and focus", "Medium", "Multi-step computation MCQ",
  r"The equation of the parabola whose vertex is $(2, 3)$ and focus is $(2, 5)$ is",
  r"$x^2 - 4x - 8y + 28 = 0$",
  [(r"$y^2 - 6y - 8x + 25 = 0$", r"Uses $(y - 3)^2 = 8(x - 2)$, taking the axis horizontal although the vertex and focus lie on $x = 2$."),
   (r"$x^2 - 4x - 4y + 16 = 0$", r"Takes $a = 1$, half the vertex-focus distance, giving $(x - 2)^2 = 4(y - 3)$."),
   (r"$x^2 - 4x + 8y - 20 = 0$", r"Uses $(x - 2)^2 = -8(y - 3)$, making the parabola open away from the focus.")],
  r"The vertex and focus lie on $x = 2$, so the axis is vertical, with $a = 5 - 3 = 2$ and the parabola opening upward. Hence $(x - 2)^2 = 8(y - 3)$, which expands to $x^2 - 4x - 8y + 28 = 0$.",
  r"Choosing the orientation of the axis or the sign of $4a$ incorrectly.",
  "U10-D-eqn-vertex-focus", "Fix orientation, find $a$, expand.",
  check=_c018,
  values=[_key(X**2 - 4*X - 8*Y + 28), _key(Y**2 - 6*Y - 8*X + 25), _key(X**2 - 4*X - 4*Y + 16), _key(X**2 - 4*X + 8*Y - 20)])

# ---------------------------------------------------------------- 019
def _c019():
    d = _par(Y**2 - 16*X)
    x1 = solve(Eq(X + d["a"], 10), X)[0]
    P = (x1, sqrt(16*x1))
    return simplify(_area((0, 0), d["focus"], P))
q("U10-D-019", TOP_FOC, "Triangle with vertex, focus and a point", "Medium", "Multi-step computation MCQ",
  r"$P$ is a point in the first quadrant on the parabola $y^2 = 16x$ whose distance from the focus $S$ is $10$. If $O$ is the vertex, the area of triangle $OPS$ is",
  r"$8\sqrt{6}$",
  [(r"$16\sqrt{6}$", r"Uses base $\times$ height without the factor $\frac{1}{2}$."),
   (r"$12\sqrt{6}$", r"Takes the base as the abscissa $6$ of $P$ instead of $OS = 4$."),
   (r"$8\sqrt{10}$", r"Takes the abscissa of $P$ as $10$, so $y = 4\sqrt{10}$.")],
  r"Here $a = 4$, $S = (4, 0)$. Focal distance $x + 4 = 10$ gives $x = 6$, $y^2 = 96$, $y = 4\sqrt{6}$. With base $OS = 4$ on the $x$-axis and height $4\sqrt{6}$, the area is $\frac{1}{2}(4)(4\sqrt{6}) = 8\sqrt{6}$.",
  r"Equating the abscissa to the focal distance.",
  "U10-D-focal-distance-area", "Focal distance, then coordinates, then an area.",
  check=_c019, values=[8*sqrt(6), 16*sqrt(6), 12*sqrt(6), 8*sqrt(10)])

# ---------------------------------------------------------------- 020
def _c020():
    P, Q = _meet(Y**2 - 8*X, Y - X + 6)
    return simplify(_dist(P, Q))
q("U10-D-020", TOP_INT, "Length of a chord cut by a line", "Medium", "Multi-step computation MCQ",
  r"The length of the chord of the parabola $y^2 = 8x$ cut off by the line $y = x - 6$ is",
  r"$16\sqrt{2}$",
  [(r"$16$", r"Finds the intersections $(2, -4)$ and $(18, 12)$ but reports only the difference of the abscissae."),
   (r"$32$", r"Adds the differences of the coordinates, $16 + 16$, instead of using the distance formula."),
   (r"$8\sqrt{2}$", r"Gives the distance from the midpoint $(10, 4)$ to one end, half the chord.")],
  r"Substituting $x = y + 6$: $y^2 = 8y + 48$, so $y = 12$ or $y = -4$, giving $(18, 12)$ and $(2, -4)$. The chord length is $\sqrt{16^2 + 16^2} = 16\sqrt{2}$.",
  r"Using only one coordinate difference for a slanted chord.",
  "U10-D-int-chord-length", "Solve a quadratic, then the distance formula.",
  check=_c020, values=[16*sqrt(2), 16, 32, 8*sqrt(2)])

# ---------------------------------------------------------------- 021
def _c021():
    a = Symbol('a', positive=True)
    av = solve(Eq(_dist((0, 0), (a, 2*a)), 3*sqrt(5)), a)[0]
    return 4*av
q("U10-D-021", TOP_STD, "Latus rectum from the distance of its ends", "Medium", "Inverse/parameter MCQ",
  r"For the parabola $y^2 = 4ax$ $(a > 0)$, each end point of the latus rectum is at a distance $3\sqrt{5}$ from the vertex. The length of the latus rectum is",
  r"$12$",
  [(r"$6$", r"Solves correctly for $a = 3$ but reports $2a$."),
   (r"$3$", r"Solves correctly for $a = 3$ but reports $a$."),
   (r"$6\sqrt{5}$", r"Takes the vertex distance equal to the focal distance $2a$, so $a = \frac{3\sqrt{5}}{2}$ and $4a = 6\sqrt{5}$.")],
  r"An end of the latus rectum is $(a, 2a)$, at distance $\sqrt{a^2 + 4a^2} = a\sqrt{5}$ from the vertex. So $a\sqrt{5} = 3\sqrt{5}$, $a = 3$, and the latus rectum is $4a = 12$.",
  r"Confusing the distance from the vertex with the focal distance of the end point.",
  "U10-D-lr-reverse", "Coordinates of the ends of the latus rectum, then solving for $a$.",
  check=_c021, values=[12, 6, 3, 6*sqrt(5)])

# ---------------------------------------------------------------- 022
def _c022():
    a, b, c = symbols('a b c')
    s = solve([Eq(c, 2), Eq(a + b + c, 1), Eq(4*a + 2*b + c, 2)], [a, b, c])
    return _par(Y - (s[a]*X**2 + s[b]*X + s[c]))["focus"]
q("U10-D-022", TOP_EQN, "Parabola through three points, then focus", "Medium", "Multi-step computation MCQ",
  r"A parabola whose axis is parallel to the $y$-axis passes through $(0, 2)$, $(1, 1)$ and $(2, 2)$. Its focus is",
  r"$\left(1, \frac{5}{4}\right)$",
  [(r"$\left(1, \frac{3}{4}\right)$", r"Finds $(x - 1)^2 = y - 1$ but moves $a = \frac{1}{4}$ downward from the vertex."),
   (r"$(1, 2)$", r"Reads $(x - 1)^2 = y - 1$ as $a = 1$, taking $4a$ as $a$."),
   (r"$\left(\frac{5}{4}, 1\right)$", r"Moves $a = \frac{1}{4}$ along the $x$-direction, taking the axis horizontal.")],
  r"Write $y = px^2 + qx + r$. Then $r = 2$, $p + q = -1$ and $4p + 2q = 0$, so $p = 1$, $q = -2$: $y = x^2 - 2x + 2$, that is $(x - 1)^2 = y - 1$. Vertex $(1, 1)$, $4a = 1$, so the focus is $\left(1, 1 + \frac{1}{4}\right) = \left(1, \frac{5}{4}\right)$.",
  r"Taking $a = 1$ from $(x-1)^2 = 1\cdot(y-1)$ when actually $4a = 1$.",
  "U10-D-eqn-three-points", "Solve a linear system, complete the square, place the focus.",
  check=_c022, values=[(1, Rational(5, 4)), (1, Rational(3, 4)), (1, 2), (Rational(5, 4), 1)])

# ---------------------------------------------------------------- 023
def _c023():
    curve = (Y - 1)**2 - 8*(X + 2)
    P = (3, 1 + sqrt(8*5))
    return simplify(_dist(P, _par(curve)["focus"]))
q("U10-D-023", TOP_FOC, "Focal distance on a shifted parabola", "Medium", "Multi-step computation MCQ",
  r"A point $P$ with abscissa $3$ lies on the parabola $(y - 1)^2 = 8(x + 2)$. The distance of $P$ from the focus of this parabola is",
  r"$7$",
  [(r"$5$", r"Uses $x_1 + a = 3 + 2$, the rule for $y^2 = 4ax$, ignoring the shift of the vertex to $(-2, 1)$."),
   (r"$3$", r"Shifts in the wrong direction: uses $x_1 + h + a = 3 + (-2) + 2$."),
   (r"$9$", r"Uses $(x_1 - h) + 2a = 5 + 4$.")],
  r"The vertex is $(-2, 1)$ and $a = 2$, so the directrix is $x = -4$. The focal distance equals the distance from the directrix: $3 - (-4) = 7$.",
  r"Applying $x_1 + a$ to a parabola whose vertex is not at the origin.",
  "U10-D-focal-distance-shifted", "Locate the directrix of a shifted parabola, then use the focus-directrix property.",
  check=_c023, values=[7, 5, 3, 9],
  numerical=dict(question=r"A point $P$ with abscissa $3$ lies on the parabola $(y - 1)^2 = 8(x + 2)$. The distance of $P$ from the focus of this parabola is", answer=7))

# ---------------------------------------------------------------- 024
def _c024():
    k = Symbol('k', positive=True)
    S = _par(Y**2 - k*(X - 1))["focus"]
    return solve(Eq(S[0], 4), k)[0]
q("U10-D-024", TOP_SHIFT, "Parameter from a given focus", "Medium", "Inverse/parameter MCQ",
  r"If the focus of the parabola $y^2 = k(x - 1)$, $k > 0$, is the point $(4, 0)$, then $k$ equals",
  r"$12$",
  [(r"$3$", r"Finds $a = 3$ correctly but reports $a$ instead of $k = 4a$."),
   (r"$16$", r"Ignores the vertex shift and sets $\frac{k}{4} = 4$."),
   (r"$20$", r"Shifts the wrong way: sets $\frac{k}{4} = 4 + 1$.")],
  r"The vertex is $(1, 0)$ and $4a = k$. The focus is $\left(1 + \frac{k}{4}, 0\right)$, so $1 + \frac{k}{4} = 4$, giving $k = 12$.",
  r"Forgetting that the focus is measured from the shifted vertex.",
  "U10-D-shift-parameter", "Locate the focus in terms of $k$, then solve.",
  check=_c024, values=[12, 3, 16, 20],
  numerical=dict(question=r"If the focus of the parabola $y^2 = k(x - 1)$, $k > 0$, is the point $(4, 0)$, then the value of $k$ is", answer=12))

# ---------------------------------------------------------------- 025
def _c025():
    a = Symbol('a', positive=True)
    L1, L2 = (a, 2*a), (a, -2*a)
    def dot_at(P):
        return simplify((L1[0]-P[0])*(L2[0]-P[0]) + (L1[1]-P[1])*(L2[1]-P[1]))
    return (bool(dot_at((-a, 0)) == 0), bool(dot_at((0, 0)) == 0))
q("U10-D-025", TOP_STD, "Angle subtended by the latus rectum", "Medium", "Statement-based MCQ",
  r"Consider the parabola $y^2 = 4ax$, $a > 0$, and let $L$ and $L'$ be the end points of its latus rectum. Statement I: $LL'$ subtends a right angle at the point where the directrix meets the axis of the parabola. Statement II: $LL'$ subtends a right angle at the vertex of the parabola. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Assumes the vertex also sees $LL'$ at a right angle; in fact $\overrightarrow{OL}\cdot\overrightarrow{OL'} = a^2 - 4a^2 \ne 0$."),
   (ST_FF, r"Rejects Statement I, perhaps checking the vertex instead of the point $(-a, 0)$."),
   (ST_FT, r"Swaps the two points: the right angle is at $(-a, 0)$, not at the vertex.")],
  r"$L = (a, 2a)$, $L' = (a, -2a)$. From $Z = (-a, 0)$: $\overrightarrow{ZL} = (2a, 2a)$, $\overrightarrow{ZL'} = (2a, -2a)$, dot product $4a^2 - 4a^2 = 0$, so Statement I is true. From $O$: $(a, 2a)\cdot(a, -2a) = -3a^2 \ne 0$, so Statement II is false.",
  r"Assuming the vertex is the special point for the right angle.",
  "U10-D-lr-right-angle", "Two dot-product checks on the latus rectum ends.",
  check=_c025, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 026
def _c026():
    c = Symbol('c', real=True)
    quad = expand((2*X + c)**2 - 8*X)
    D = discriminant(quad, X)
    return solveset(D > 0, c, S.Reals)
q("U10-D-026", TOP_INT, "Condition for two intersection points", "Medium", "Inverse/parameter MCQ",
  r"The set of all real values of $c$ for which the line $y = 2x + c$ meets the parabola $y^2 = 8x$ at two distinct points is",
  r"$(-\infty, 1)$",
  [(r"$(1, \infty)$", r"Reverses the inequality while solving $16 - 16c > 0$."),
   (r"$(-\infty, 1]$", r"Includes $c = 1$, where the two intersection points coincide."),
   (r"$(-2, 2)$", r"Expands $(2x + c)^2$ as $4x^2 + c^2$, dropping $4cx$, so the discriminant is $64 - 16c^2$.")],
  r"Substituting, $(2x + c)^2 = 8x$, i.e. $4x^2 + (4c - 8)x + c^2 = 0$. Two distinct points need $(4c - 8)^2 - 16c^2 > 0$, i.e. $64 - 64c > 0$, so $c < 1$.",
  r"Including the equality case that gives a single common point.",
  "U10-D-int-two-points", "Substitute, form the quadratic, apply the discriminant.",
  check=_c026, values=[Interval.open(-oo, 1), Interval.open(1, oo), Interval(-oo, 1), Interval.open(-2, 2)])

# ---------------------------------------------------------------- 027
def _c027():
    S = _par(Y**2 - 12*X)["focus"]
    P, Q = _meet(Y**2 - 12*X, Y - (X - S[0]))
    return simplify(_dist(P, Q))
q("U10-D-027", TOP_FOC, "Length of a focal chord of given slope", "Medium", "Multi-step computation MCQ",
  r"A line of slope $1$ through the focus of the parabola $y^2 = 12x$ meets the parabola at $P$ and $Q$. The length $PQ$ is",
  r"$24$",
  [(r"$18$", r"Uses only $x_1 + x_2 = 18$ from the quadratic, forgetting to add $a$ for each focal distance."),
   (r"$21$", r"Adds $a = 3$ only once: $x_1 + x_2 + a$."),
   (r"$12$", r"Assumes every focal chord equals the latus rectum $4a$.")],
  r"The focus is $(3, 0)$, so the line is $y = x - 3$. Then $(x - 3)^2 = 12x$, i.e. $x^2 - 18x + 9 = 0$, so $x_1 + x_2 = 18$. Since $PQ = SP + SQ = (x_1 + 3) + (x_2 + 3)$, $PQ = 24$.",
  r"Treating every focal chord as the latus rectum.",
  "U10-D-focal-chord", "Intersection quadratic plus the focal distance rule for both ends.",
  check=_c027, values=[24, 18, 21, 12],
  numerical=dict(question=r"A line of slope $1$ through the focus of the parabola $y^2 = 12x$ meets the parabola at $P$ and $Q$. The length $PQ$ is", answer=24))

# ---------------------------------------------------------------- 028
q("U10-D-028", TOP_SHIFT, "Focus of a quadratic graph", "Medium", "Multi-step computation MCQ",
  r"The focus of the parabola $y = x^2 - 4x + 3$ is",
  r"$\left(2, -\frac{3}{4}\right)$",
  [(r"$\left(2, -\frac{5}{4}\right)$", r"Moves $a = \frac{1}{4}$ downward from the vertex $(2, -1)$; this point lies on the directrix."),
   (r"$(2, 0)$", r"Reads $(x - 2)^2 = y + 1$ as $a = 1$."),
   (r"$\left(2, -\frac{1}{2}\right)$", r"Moves $2a = \frac{1}{2}$ from the vertex.")],
  r"$y = (x - 2)^2 - 1$, so $(x - 2)^2 = y + 1$. The vertex is $(2, -1)$ and $4a = 1$, so $a = \frac{1}{4}$, opening upward. The focus is $\left(2, -1 + \frac{1}{4}\right) = \left(2, -\frac{3}{4}\right)$.",
  r"Taking $a$ as the coefficient on the right instead of a quarter of it.",
  "U10-D-shift-focus", "Completing the square and reading $a$ from $4a = 1$.",
  check=lambda: _par(Y - (X**2 - 4*X + 3))["focus"],
  values=[(2, -Rational(3, 4)), (2, -Rational(5, 4)), (2, 0), (2, -Rational(1, 2))])

# ---------------------------------------------------------------- 029
def _c029():
    a = Symbol('a', positive=True)
    x1 = 10 - a
    return sum(solve(Eq(8**2, 4*a*x1), a))
q("U10-D-029", TOP_FOC, "Two possible parabolas from focal data", "Medium", "Inverse/parameter MCQ",
  r"A point $P$ on the parabola $y^2 = 4ax$, $a > 0$, is at distance $10$ from the focus and at distance $8$ from the axis of the parabola. The sum of all possible values of $a$ is",
  r"$10$",
  [(r"$8$", r"Keeps only the larger root of $a^2 - 10a + 16 = 0$."),
   (r"$2$", r"Keeps only the smaller root of $a^2 - 10a + 16 = 0$."),
   (r"$16$", r"Gives the product of the roots of $a^2 - 10a + 16 = 0$.")],
  r"If $P = (x_1, y_1)$ then $x_1 + a = 10$ and $|y_1| = 8$. So $64 = 4a(10 - a)$, i.e. $a^2 - 10a + 16 = 0$, giving $a = 2$ or $a = 8$; both give $x_1 > 0$. The sum is $10$.",
  r"Stopping at one root when both satisfy every condition.",
  "U10-D-focal-distance-two-cases", "Two conditions give a quadratic in $a$; both roots are admissible.",
  check=_c029, values=[10, 8, 2, 16],
  numerical=dict(question=r"A point $P$ on the parabola $y^2 = 4ax$, $a > 0$, is at distance $10$ from the focus and at distance $8$ from the axis of the parabola. The sum of all possible values of $a$ is", answer=10))

# ---------------------------------------------------------------- 030
def _c030():
    a = Symbol('a')
    av = solve(Eq(2**2, 4*a*(3 - 2)), a)[0]
    pts = _meet(Y**2 - 4*av*X, X + Y - 3)
    return [p for p in pts if p[1] != 2][0]
q("U10-D-030", TOP_INT, "Second intersection after finding the parameter", "Medium", "Multi-step computation MCQ",
  r"The line $x + y = 3$ meets the parabola $y^2 = 4ax$ at a point whose ordinate is $2$. The other point of intersection of the line and the parabola is",
  r"$(9, -6)$",
  [(r"$(9, 6)$", r"Finds $x = 9$ but takes the ordinate with the wrong sign; $(9, 6)$ is not on $x + y = 3$."),
   (r"$(1, -2)$", r"Reflects the first point $(1, 2)$ in the axis; this lies on the parabola but not on the line."),
   (r"$(-3, 6)$", r"Factorises $y^2 + 4y - 12 = 0$ with a sign slip as $(y - 6)(y + 2)$, takes $y = 6$ and then $x = 3 - 6$.")],
  r"At $y = 2$ the line gives $x = 1$, so $4 = 4a$, $a = 1$. Then $y^2 = 4(3 - y)$, i.e. $y^2 + 4y - 12 = 0$, giving $y = 2$ or $y = -6$. The other point is $(9, -6)$.",
  r"Not checking that the second point lies on the line.",
  "U10-D-int-second-point", "Find the parameter, then solve the intersection quadratic.",
  check=_c030, values=[(9, -6), (9, 6), (1, -2), (-3, 6)])

# ---------------------------------------------------------------- 031
def _c031():
    a = Symbol('a')
    av = solve(Eq((6 - 2)**2, 4*a*(3 + 1)), a)[0]
    return _par((Y - 2)**2 - 4*av*(X + 1))["focus"]
q("U10-D-031", TOP_EQN, "Shifted parabola through a point, then focus", "Medium", "Multi-step computation MCQ",
  r"A parabola has its axis parallel to the $x$-axis, its vertex at $(-1, 2)$, and passes through $(3, 6)$. Its focus is",
  r"$(0, 2)$",
  [(r"$(-2, 2)$", r"Finds $a = 1$ but moves to the left, although the curve passes through a point to the right of the vertex."),
   (r"$(3, 2)$", r"Moves $4a = 4$ from the vertex instead of $a$."),
   (r"$(-1, 3)$", r"Moves $a = 1$ along the $y$-direction, taking the axis vertical.")],
  r"The form is $(y - 2)^2 = 4a(x + 1)$. Substituting $(3, 6)$: $16 = 16a$, so $a = 1$ and the parabola opens to the right. The focus is $(-1 + 1, 2) = (0, 2)$.",
  r"Shifting by $4a$ instead of $a$.",
  "U10-D-eqn-through-point", "Find $a$ from a point, then place the focus from the vertex.",
  check=_c031, values=[(0, 2), (-2, 2), (3, 2), (-1, 3)])

# ---------------------------------------------------------------- 032
def _c032():
    d = _par((X - 1)**2 + 8*(Y + 2))
    return (d["focus"] == (1, 0), d["directrix"] == _ln(0, 1, 0))
q("U10-D-032", TOP_SHIFT, "Focus and directrix of a downward parabola", "Medium", "Statement-based MCQ",
  r"For the parabola $(x - 1)^2 = -8(y + 2)$: Statement I: Its focus is $(1, 0)$. Statement II: Its directrix is the $x$-axis. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts $(1, 0)$, which is the point where the axis meets the directrix, as the focus."),
   (ST_FF, r"Reads $a = 8$ from $4a = 8$, getting focus $(1, -10)$ and directrix $y = 6$, and so rejects both."),
   (ST_TF, r"Moves the focus upward from the vertex to $(1, 0)$ and the directrix downward to $y = -4$.")],
  r"The vertex is $(1, -2)$ and $4a = 8$, $a = 2$, opening downward. The focus is $(1, -2 - 2) = (1, -4)$, so Statement I is false. The directrix is $y = -2 + 2 = 0$, the $x$-axis, so Statement II is true.",
  r"Moving the focus in the wrong direction for a downward-opening parabola.",
  "U10-D-shift-statement", "Two placements around a shifted vertex with a sign decision.",
  check=_c032, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis")

# ---------------------------------------------------------------- 033
def _c033():
    pts = solve([Y**2 - 8*X, X**2 - 8*Y], [X, Y], dict=True)
    real = [(s[X], s[Y]) for s in pts if s[X].is_real and s[Y].is_real]
    return simplify(_dist(real[0], real[1]))
q("U10-D-033", TOP_INT, "Common chord of two parabolas", "Medium", "Multi-step computation MCQ",
  r"The parabolas $y^2 = 8x$ and $x^2 = 8y$ meet at two points. The distance between these points is",
  r"$8\sqrt{2}$",
  [(r"$8$", r"Finds $(0, 0)$ and $(8, 8)$ but reports only the difference of abscissae."),
   (r"$16$", r"Adds the coordinate differences $8 + 8$."),
   (r"$32\sqrt{2}$", r"Treats $8$ as $a$ and uses the meeting point $(4a, 4a) = (32, 32)$.")],
  r"From $x^2 = 8y$, $y = \frac{x^2}{8}$; then $\frac{x^4}{64} = 8x$, so $x = 0$ or $x^3 = 512$, $x = 8$. The real meeting points are $(0, 0)$ and $(8, 8)$, at distance $8\sqrt{2}$.",
  r"Confusing $4a$ with $a$ when using the known meeting point $(4a, 4a)$.",
  "U10-D-int-two-parabolas", "Eliminate one variable, solve, apply the distance formula.",
  check=_c033, values=[8*sqrt(2), 8, 16, 32*sqrt(2)])

# ---------------------------------------------------------------- 034
def _c034():
    L1, L2 = (3, 5), (3, -3)
    lr = _dist(L1, L2)
    a = lr / 4
    S = ((L1[0] + L2[0]) / 2, Rational(L1[1] + L2[1], 2))
    return (S[0] + a, S[1])
q("U10-D-034", TOP_EQN, "Vertex from the latus rectum", "Medium", "Multi-step computation MCQ",
  r"The end points of the latus rectum of a parabola are $(3, 5)$ and $(3, -3)$, and the parabola opens towards the negative $x$-direction. Its vertex is",
  r"$(5, 1)$",
  [(r"$(1, 1)$", r"Places the vertex on the side towards which the parabola opens."),
   (r"$(7, 1)$", r"Takes $a$ as half the latus rectum, $4$."),
   (r"$(11, 1)$", r"Takes $a$ equal to the whole latus rectum, $8$.")],
  r"The latus rectum has length $8 = 4a$, so $a = 2$, and its midpoint $(3, 1)$ is the focus. The axis is $y = 1$. A parabola opening towards negative $x$ has its vertex at distance $a$ to the right of the focus: $(5, 1)$.",
  r"Using $2a$ or $4a$ as the focus-vertex distance.",
  "U10-D-lr-reverse", "Latus rectum gives the focus and $a$; orientation fixes the vertex.",
  check=_c034, values=[(5, 1), (1, 1), (7, 1), (11, 1)])

# ---------------------------------------------------------------- 035
def _c035():
    S, dx = (3, 0), -1
    return _key((X - S[0])**2 + (Y - S[1])**2 - (X - dx)**2)
q("U10-D-035", TOP_EQN, "Equation from focus and directrix (shifted vertex)", "Medium", "Multi-step computation MCQ",
  r"The equation of the parabola whose focus is $(3, 0)$ and directrix is $x = -1$ is",
  r"$y^2 = 8(x - 1)$",
  [(r"$y^2 = 12x$", r"Assumes the vertex is at the origin and uses $a = 3$ from the focus."),
   (r"$y^2 = 16(x - 1)$", r"Takes $a$ as the focus-directrix distance $4$."),
   (r"$y^2 = 8(x + 1)$", r"Finds $a = 2$ but places the vertex at $(-1, 0)$ on the directrix.")],
  r"By definition, $(x - 3)^2 + y^2 = (x + 1)^2$, which gives $y^2 = 8x - 8 = 8(x - 1)$. The vertex $(1, 0)$ is midway between focus and directrix and $a = 2$.",
  r"Assuming the vertex is at the origin whenever the focus is on an axis.",
  "U10-D-eqn-focus-directrix", "Focus-directrix definition with a vertex away from the origin.",
  check=_c035, values=[_key(Y**2 - 8*(X - 1)), _key(Y**2 - 12*X), _key(Y**2 - 16*(X - 1)), _key(Y**2 - 8*(X + 1))])

# ---------------------------------------------------------------- 036
def _c036():
    k = Symbol('k', positive=True)
    lr = _par(Y**2 - 12*X)["lr"]
    chord = 2*sqrt(12*k)
    return solve(Eq(chord, 3*lr), k)[0]
q("U10-D-036", TOP_INT, "Double ordinate in terms of the latus rectum", "Medium", "Inverse/parameter MCQ",
  r"The line $x = k$ $(k > 0)$ meets the parabola $y^2 = 12x$ at $P$ and $Q$. If $PQ$ is three times the length of the latus rectum, then $k$ equals",
  r"$27$",
  [(r"$108$", r"Takes $PQ = \sqrt{12k}$, forgetting that $PQ$ is twice the ordinate."),
   (r"$9$", r"Assumes $PQ$ grows in proportion to $k$, so $k = 3a$."),
   (r"$81$", r"Uses $a = 1$, writing $PQ = 4\sqrt{k}$.")],
  r"At $x = k$, $y = \pm\sqrt{12k}$, so $PQ = 2\sqrt{12k}$. The latus rectum is $12$, so $2\sqrt{12k} = 36$, $\sqrt{12k} = 18$, $12k = 324$, $k = 27$.",
  r"Treating the length of a double ordinate as proportional to $k$.",
  "U10-D-int-double-ordinate", "Chord along $x = k$ compared with the latus rectum.",
  check=_c036, values=[27, 108, 9, 81],
  numerical=dict(question=r"The line $x = k$ $(k > 0)$ meets the parabola $y^2 = 12x$ at $P$ and $Q$. If $PQ$ is three times the length of the latus rectum, then the value of $k$ is", answer=27))

# ---------------------------------------------------------------- 037
def _c037():
    V, S = (1, 1), (-1, 1)
    a = S[0] - V[0]
    curve = (Y - V[1])**2 - 4*a*(X - V[0])
    P, Q = _meet(curve, X)
    return simplify(_dist(P, Q))
q("U10-D-037", TOP_INT, "Chord on the y-axis of a shifted parabola", "Medium", "Multi-step computation MCQ",
  r"A parabola has vertex $(1, 1)$ and focus $(-1, 1)$. The length of the chord it cuts off on the $y$-axis is",
  r"$4\sqrt{2}$",
  [(r"$2\sqrt{2}$", r"Finds $y = 1 \pm 2\sqrt{2}$ but reports the distance from $(0, 1)$ to one end."),
   (r"$4$", r"Takes $4a = 4$ (so $a = 1$, half the vertex-focus distance), giving $(y - 1)^2 = 4$."),
   (r"$8$", r"Takes $a = 4$, the focus-directrix distance, giving $(y - 1)^2 = 16$.")],
  r"Here $a = 2$ and the parabola opens to the left: $(y - 1)^2 = -8(x - 1)$. At $x = 0$, $(y - 1)^2 = 8$, so $y = 1 \pm 2\sqrt{2}$, and the chord has length $4\sqrt{2}$.",
  r"Mis-identifying $a$ from the vertex and focus.",
  "U10-D-int-axis-chord", "Build the equation, then intersect with a line.",
  check=_c037, values=[4*sqrt(2), 2*sqrt(2), 4, 8])


# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 038
def _c038():
    S = (1, 1)
    return _key(((X - S[0])**2 + (Y - S[1])**2) * 2 - (X + Y)**2)
q("U10-D-038", TOP_EQN, "Parabola with an oblique directrix", "Difficult", "Multi-step computation MCQ",
  r"The equation of the parabola whose focus is $(1, 1)$ and whose directrix is the line $x + y = 0$ is",
  r"$x^2 - 2xy + y^2 - 4x - 4y + 4 = 0$",
  [(r"$xy + x + y - 1 = 0$", r"Uses the distance from the directrix as $|x + y|$, dropping the divisor $\sqrt{2}$; the $x^2$ and $y^2$ terms then cancel."),
   (r"$x^2 + 2xy + y^2 - 4x - 4y + 4 = 0$", r"Sign slip in the $xy$ term when moving $(x + y)^2$ across."),
   (r"$x^2 - 2xy + y^2 - 2x - 2y + 2 = 0$", r"Multiplies only the squared terms of the left side by $2$ when clearing the denominator.")],
  r"For $P(x, y)$, $PS^2 = \frac{(x + y)^2}{2}$, so $2[(x - 1)^2 + (y - 1)^2] = (x + y)^2$. Then $2x^2 + 2y^2 - 4x - 4y + 4 = x^2 + 2xy + y^2$, which gives $x^2 - 2xy + y^2 - 4x - 4y + 4 = 0$.",
  r"Forgetting to divide by $\sqrt{a^2 + b^2}$ in the distance from a line.",
  "U10-D-eqn-oblique-directrix", "Focus-directrix definition with an oblique directrix; a normalising factor and careful expansion.",
  check=_c038,
  values=[_key(X**2 - 2*X*Y + Y**2 - 4*X - 4*Y + 4), _key(X*Y + X + Y - 1),
          _key(X**2 + 2*X*Y + Y**2 - 4*X - 4*Y + 4), _key(X**2 - 2*X*Y + Y**2 - 2*X - 2*Y + 2)],
  cognitive="Application")

# ---------------------------------------------------------------- 039
def _c039():
    S = _par(Y**2 - 8*X)["focus"]
    P = (8, 8)
    line = (Y - S[1]) * (P[0] - S[0]) - (X - S[0]) * (P[1] - S[1])
    pts = _meet(Y**2 - 8*X, line)
    Q = [p for p in pts if p != P][0]
    return simplify(_dist(P, Q))
q("U10-D-039", TOP_FOC, "Focal chord through a given point", "Difficult", "Multi-step computation MCQ",
  r"A chord of the parabola $y^2 = 8x$ passes through its focus and has one end at $(8, 8)$. The length of this chord is",
  r"$\frac{25}{2}$",
  [(r"$10$", r"Gives only the focal distance $8 + 2$ of the known end."),
   (r"$\frac{17}{2}$", r"Finds the other end $\left(\frac{1}{2}, -2\right)$ but adds only the abscissae, $8 + \frac{1}{2}$."),
   (r"$\frac{21}{2}$", r"Adds $a = 2$ only once: $8 + \frac{1}{2} + 2$.")],
  r"The focus is $(2, 0)$, so the chord is $y = \frac{4}{3}(x - 2)$, i.e. $x = \frac{3y}{4} + 2$. Then $y^2 = 6y + 16$, so $y = 8$ or $y = -2$; the other end is $\left(\frac{1}{2}, -2\right)$. The length is $(8 + 2) + \left(\frac{1}{2} + 2\right) = \frac{25}{2}$.",
  r"Adding abscissae without the $a$ for each focal distance.",
  "U10-D-focal-chord", "Line through two points, intersection quadratic, focal distances of both ends.",
  check=_c039, values=[Rational(25, 2), 10, Rational(17, 2), Rational(21, 2)])

# ---------------------------------------------------------------- 040
def _c040():
    pts = [p for p in _meet(Y**2 - 12*X, Y - X / sqrt(3)) if p != (0, 0)]
    P = pts[0]
    return simplify(2 * Abs(P[1]))
q("U10-D-040", TOP_INT, "Equilateral triangle with a vertex at the parabola's vertex", "Difficult", "Multi-step computation MCQ",
  r"An equilateral triangle is inscribed in the parabola $y^2 = 12x$ with one vertex at the vertex of the parabola. The length of a side of the triangle is",
  r"$24\sqrt{3}$",
  [(r"$12\sqrt{3}$", r"Finds the other vertices $(36, \pm 12\sqrt{3})$ but gives the ordinate $12\sqrt{3}$, half the side."),
   (r"$8\sqrt{3}$", r"Uses the side through the origin as $y = \sqrt{3}x$ (angle $60^\circ$ with the axis), giving $x = 4$ and side $2(4\sqrt{3})$."),
   (r"$96\sqrt{3}$", r"Treats $12$ as $a$, i.e. uses $y^2 = 48x$.")],
  r"By symmetry the other two vertices are $(h, \pm k)$ and each side through the origin makes $30^\circ$ with the axis, so $k = \frac{h}{\sqrt{3}}$. Then $\frac{h^2}{3} = 12h$ gives $h = 36$, $k = 12\sqrt{3}$. The side is $2k = 24\sqrt{3}$.",
  r"Using $60^\circ$ with the axis instead of $30^\circ$.",
  "U10-D-int-equilateral", "Symmetry argument, correct angle with the axis, intersection with a line.",
  check=_c040, values=[24*sqrt(3), 12*sqrt(3), 8*sqrt(3), 96*sqrt(3)])

# ---------------------------------------------------------------- 041
def _c041():
    m = Symbol('m', real=True)
    good = set()
    # line parallel to the axis
    if len(_meet(Y**2 - 4*X, Y - 1)) == 1:
        good.add(0)
    quad = expand((m*X + 1)**2 - 4*X)
    for mv in solve(discriminant(quad, X), m):
        if mv != 0 and len(_meet(Y**2 - 4*X, Y - mv*X - 1)) == 1:
            good.add(mv)
    return FiniteSet(*good)
q("U10-D-041", TOP_INT, "Exactly one common point: the parallel case", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real values of $m$ for which the line $y = mx + 1$ meets the parabola $y^2 = 4x$ at exactly one point is",
  r"$\{0, 1\}$",
  [(r"$\{1\}$", r"Sets the discriminant of $m^2x^2 + (2m - 4)x + 1 = 0$ to zero but misses $m = 0$, where the equation is linear and the line $y = 1$ (parallel to the axis) meets the parabola once."),
   (r"$\{-1\}$", r"Sign slip in the discriminant, $16 + 16m = 0$, and also misses the linear case."),
   (r"$\{0, -1\}$", r"Includes the linear case $m = 0$ but makes the sign slip $16 + 16m = 0$.")],
  r"Substituting, $m^2x^2 + (2m - 4)x + 1 = 0$. If $m = 0$ this is $-4x + 1 = 0$, a single point $\left(\frac{1}{4}, 1\right)$. If $m \ne 0$, one point needs $(2m - 4)^2 - 4m^2 = 16 - 16m = 0$, so $m = 1$. The set is $\{0, 1\}$.",
  r"Ignoring that a line parallel to the axis meets a parabola exactly once.",
  "U10-D-int-one-point", "Casework on the leading coefficient plus a discriminant condition.",
  check=_c041, values=[FiniteSet(0, 1), FiniteSet(1), FiniteSet(-1), FiniteSet(0, -1)], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c042():
    a = Symbol('a')
    av = solve(Eq((6 - 2)**2, 4*a*(-1 - 3)), a)[0]
    P, Q = _meet((X - 2)**2 - 4*av*(Y - 3), Y)
    return simplify(_dist(P, Q))
q("U10-D-042", TOP_INT, "Chord on the x-axis after building the equation", "Difficult", "Multi-step computation MCQ",
  r"A parabola has its axis along the line $x = 2$, its vertex on the line $y = 3$, and passes through the point $(6, -1)$. The length of the chord it cuts off on the $x$-axis is",
  r"$4\sqrt{3}$",
  [(r"$2\sqrt{3}$", r"Finds $x = 2 \pm 2\sqrt{3}$ but reports the distance from $(2, 0)$ to one end."),
   (r"$4\sqrt{6}$", r"Writes the vertex shift as $(y + 3)$, so $16 = 8a$, $a = 2$ and $(x - 2)^2 = 8(y + 3)$."),
   (r"$8\sqrt{3}$", r"Solves $16 = a(-4)$ from $(x - 2)^2 = a(y - 3)$, gets $a = -4$, and then uses $(x - 2)^2 = 4a(y - 3) = -16(y - 3)$.")],
  r"The vertex is $(2, 3)$ and the form is $(x - 2)^2 = 4a(y - 3)$. Substituting $(6, -1)$: $16 = -16a$, so $a = -1$ and $(x - 2)^2 = -4(y - 3)$ (opening downward). At $y = 0$, $(x - 2)^2 = 12$, so $x = 2 \pm 2\sqrt{3}$ and the chord is $4\sqrt{3}$.",
  r"Sign slips in the vertex shift, or mixing the forms $a(y - k)$ and $4a(y - k)$.",
  "U10-D-int-axis-chord", "Vertex from two lines, $a$ from a point (negative), then a chord.",
  check=_c042, values=[4*sqrt(3), 2*sqrt(3), 4*sqrt(6), 8*sqrt(3)])

# ---------------------------------------------------------------- 043
def _c043():
    a = Symbol('a', positive=True)
    t = T_
    P = (a*t**2, 2*a*t)
    S = (a, 0)
    C = ((P[0] + S[0]) / 2, (P[1] + S[1]) / 2)
    r1sq = expand((_dist(P, S) / 2)**2)
    st1 = simplify(r1sq - C[0]**2) == 0 and (C[0] > 0) == True
    r2 = _dist((a, 2*a), (a, -2*a)) / 2
    st2 = simplify(r2 - Abs(a - (-a))) == 0
    return (bool(st1), bool(st2))
q("U10-D-043", TOP_FOC, "Circles on focal segments", "Difficult", "Statement-based MCQ",
  r"For the parabola $y^2 = 4ax$, $a > 0$, with focus $S$: Statement I: For every point $P$ on the parabola, the circle with $SP$ as diameter touches the $y$-axis. Statement II: The circle with the latus rectum as diameter touches the directrix. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Checks Statement II with radius $a$ (half of $2a$) instead of $2a$, finds it does not reach the directrix at distance $2a$."),
   (ST_FT, r"Computes the radius in Statement I as half the distance from the vertex to $P$ instead of $\frac{SP}{2} = \frac{x_1 + a}{2}$."),
   (ST_FF, r"Makes both radius slips above.")],
  r"Statement I: for $P(x_1, y_1)$, the centre is $\left(\frac{x_1 + a}{2}, \frac{y_1}{2}\right)$ and the radius is $\frac{SP}{2} = \frac{x_1 + a}{2}$, which equals the distance of the centre from the $y$-axis; true. Statement II: the centre is $(a, 0)$ and the radius is $2a$; the directrix $x = -a$ is at distance $2a$ from the centre; true.",
  r"Not using the focal distance $x_1 + a$ for $SP$.",
  "U10-D-focal-circle-statement", "Two general proofs with the focal distance and the latus rectum.",
  check=_c043, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Analysis")

# ---------------------------------------------------------------- 044
def _c044():
    h, k = symbols('h k', real=True)
    S = _par(Y**2 - 8*X)["focus"]
    x1, y1 = 2*h - S[0], 2*k - S[1]
    locus = (y1**2 - 8*x1).subs({h: X, k: Y})
    return _par(locus)["directrix"]
q("U10-D-044", TOP_EQN, "Locus of the midpoint of a focal segment", "Difficult", "Multi-step computation MCQ",
  r"$S$ is the focus of the parabola $y^2 = 8x$ and $P$ moves on the parabola. The locus of the midpoint of $SP$ is a parabola whose directrix is",
  r"$x = 0$",
  [(r"$x = -1$", r"Uses the midpoint of $OP$ ($O$ the vertex), getting $y^2 = 4x$."),
   (r"$x = -2$", r"Assumes the locus has the same directrix as the original parabola."),
   (r"$x = -3$", r"Takes $y_1 = k$ instead of $2k$, getting $y^2 = 16(x - 1)$ with $a = 4$.")],
  r"Let the midpoint be $(h, k)$ with $S = (2, 0)$. Then $P = (2h - 2, 2k)$, and $4k^2 = 8(2h - 2)$ gives $k^2 = 4(h - 1)$. The locus $y^2 = 4(x - 1)$ has vertex $(1, 0)$ and $a = 1$, so its directrix is $x = 0$.",
  r"Forgetting to double both coordinates when expressing $P$ from the midpoint.",
  "U10-D-eqn-locus-midpoint", "Locus by parametrising through the midpoint, then a shifted directrix.",
  check=_c044, values=[_ln(1, 0, 0), _ln(1, 0, 1), _ln(1, 0, 2), _ln(1, 0, 3)])

# ---------------------------------------------------------------- 045
def _c045():
    V, dx = (2, 3), -1
    a = V[0] - dx
    P, Q = _meet((Y - V[1])**2 - 4*a*(X - V[0]), Y - X)
    return simplify(_dist(P, Q))
q("U10-D-045", TOP_INT, "Chord after building from vertex and directrix", "Difficult", "Multi-step computation MCQ",
  r"A parabola has vertex $(2, 3)$ and directrix $x = -1$. The length of the chord of this parabola along the line $y = x$ is",
  r"$8\sqrt{6}$",
  [(r"$8\sqrt{3}$", r"Uses $(y - 3)^2 = -12(x - 2)$, opening towards the directrix; then $x^2 + 6x - 15 = 0$."),
   (r"$2\sqrt{30}$", r"Takes the vertex-directrix distance $3$ as $2a$, so $(y - 3)^2 = 6(x - 2)$."),
   (r"$8\sqrt{21}$", r"Takes $a = 6$, double the vertex-directrix distance, so $(y - 3)^2 = 24(x - 2)$.")],
  r"The vertex is $3$ units to the right of the directrix, so $a = 3$ and the parabola opens to the right: $(y - 3)^2 = 12(x - 2)$. With $y = x$: $x^2 - 18x + 33 = 0$, so $|x_1 - x_2| = \sqrt{324 - 132} = 8\sqrt{3}$. The chord is $\sqrt{2}\cdot 8\sqrt{3} = 8\sqrt{6}$.",
  r"Choosing the opening direction towards the directrix.",
  "U10-D-int-chord-length", "Equation from data, intersection quadratic, chord length on a slanted line.",
  check=_c045, values=[8*sqrt(6), 8*sqrt(3), 2*sqrt(30), 8*sqrt(21)])

# ---------------------------------------------------------------- 046
def _c046():
    k = Symbol('k', real=True)
    yy = Symbol('yy')
    quad = Poly(yy**2 - 8*(T_*yy + k), yy)
    c2, c1, c0 = quad.all_coeffs()
    y1y2 = c0 / c2
    x1x2 = y1y2**2 / 64
    sols = [s for s in solve(Eq(simplify(x1x2 + y1y2), 0), k) if s != 0]
    return sols[0]
q("U10-D-046", TOP_INT, "Chords subtending a right angle at the vertex", "Difficult", "Inverse/parameter MCQ",
  r"Every chord of the parabola $y^2 = 8x$ that passes through the fixed point $(k, 0)$, $k \ne 0$, subtends a right angle at the vertex. Then $k$ equals",
  r"$8$",
  [(r"$2$", r"Assumes the fixed point is the focus $(a, 0)$."),
   (r"$4$", r"Uses $2a$ for the fixed point."),
   (r"$-8$", r"Sign slip: takes the product of the ordinates as $+8k$.")],
  r"Write the chord as $x = ty + k$. Then $y^2 - 8ty - 8k = 0$, so $y_1y_2 = -8k$ and $x_1x_2 = \frac{(y_1y_2)^2}{64} = k^2$. A right angle at the origin needs $x_1x_2 + y_1y_2 = 0$: $k^2 - 8k = 0$, so $k = 8$, independent of $t$.",
  r"Assuming the special point is the focus.",
  "U10-D-int-right-angle-chord", "Product of roots of the intersection quadratic and a perpendicularity condition.",
  check=_c046, values=[8, 2, 4, -8], cognitive="Analysis",
  numerical=dict(question=r"Every chord of the parabola $y^2 = 8x$ that passes through the fixed point $(k, 0)$, $k \ne 0$, subtends a right angle at the vertex. The value of $k$ is", answer=8))

# ---------------------------------------------------------------- 047
def _c047():
    d = _par(Y**2 - 16*X)
    x1 = solve(Eq(X + d["a"], 8), X)[0]
    P = (x1, sqrt(16*x1))
    Q = (-d["directrix"][2], P[1])
    return _area(P, Q, d["focus"])
q("U10-D-047", TOP_FOC, "Triangle with the foot on the directrix", "Difficult", "Multi-step computation MCQ",
  r"$P$ is a point in the first quadrant on the parabola $y^2 = 16x$ with $SP = 8$, where $S$ is the focus. If $M$ is the foot of the perpendicular from $P$ to the directrix, the area of triangle $PMS$ is",
  r"$32$",
  [(r"$64$", r"Omits the factor $\frac{1}{2}$ in the area of the right triangle."),
   (r"$16\sqrt{3}$", r"Assumes the triangle is equilateral with side $8$, since $SP = PM$."),
   (r"$16$", r"Uses the abscissa $4$ of $P$ as the height instead of its ordinate $8$.")],
  r"Here $a = 4$, $S = (4, 0)$, directrix $x = -4$. $SP = x + 4 = 8$ gives $P = (4, 8)$, and $M = (-4, 8)$. Then $PM = 8$ is horizontal and $PS = 8$ is vertical, so the triangle is right-angled at $P$ with area $\frac{1}{2}(8)(8) = 32$.",
  r"Assuming $SP = PM$ makes the triangle equilateral.",
  "U10-D-focal-distance-area", "Focal distance, coordinates of a foot on the directrix, recognising a right angle.",
  check=_c047, values=[32, 64, 16*sqrt(3), 16],
  numerical=dict(question=r"$P$ is a point in the first quadrant on the parabola $y^2 = 16x$ with $SP = 8$, where $S$ is the focus. If $M$ is the foot of the perpendicular from $P$ to the directrix, the area of triangle $PMS$ is", answer=32))

# ---------------------------------------------------------------- 048
def _c048():
    d = _par(Y**2 - 4*X)
    def pt(fd):
        x1 = solve(Eq(X + d["a"], fd), X)[0]
        return (x1, sqrt(4*x1))
    return _area(pt(5), pt(10), d["focus"])
q("U10-D-048", TOP_FOC, "Area from two focal distances", "Difficult", "Multi-step computation MCQ",
  r"$P$ and $Q$ are points in the first quadrant on the parabola $y^2 = 4x$ whose distances from the focus $S$ are $5$ and $10$ respectively. The area of triangle $SPQ$ is",
  r"$7$",
  [(r"$14$", r"Omits the factor $\frac{1}{2}$ in the coordinate area formula."),
   (r"$25$", r"Takes $Q$ below the axis, $(9, -6)$, ignoring the first-quadrant condition."),
   (r"$6$", r"Uses the vertex $O$ in place of the focus $S$.")],
  r"Here $a = 1$, $S = (1, 0)$. $x + 1 = 5$ gives $P = (4, 4)$; $x + 1 = 10$ gives $Q = (9, 6)$. Area $= \frac{1}{2}\left|1(4 - 6) + 4(6 - 0) + 9(0 - 4)\right| = \frac{1}{2}|-14| = 7$.",
  r"Replacing the focus by the vertex.",
  "U10-D-focal-distance-area", "Two reverse focal distances and a coordinate area.",
  check=_c048, values=[7, 14, 25, 6],
  numerical=dict(question=r"$P$ and $Q$ are points in the first quadrant on the parabola $y^2 = 4x$ whose distances from the focus $S$ are $5$ and $10$ respectively. The area of triangle $SPQ$ is", answer=7))

# ---------------------------------------------------------------- 049
def _c049():
    S, dy = (-1, 2), 6
    curve = (X - S[0])**2 + (Y - S[1])**2 - (Y - dy)**2
    P = _meet(curve, X)[0]
    return simplify(_dist(P, S))
q("U10-D-049", TOP_FOC, "Focal distance of a y-intercept point", "Difficult", "Multi-step computation MCQ",
  r"A parabola has focus $(-1, 2)$ and directrix $y = 6$. It meets the $y$-axis at the point $P$. The distance of $P$ from the focus is",
  r"$\frac{17}{8}$",
  [(r"$\frac{31}{8}$", r"Finds $P = \left(0, \frac{31}{8}\right)$ and gives its ordinate."),
   (r"$\frac{15}{8}$", r"Uses only the vertical separation $\frac{31}{8} - 2$ from the focus."),
   (r"$\frac{1}{8}$", r"Gives the vertical distance $4 - \frac{31}{8}$ of $P$ below the vertex.")],
  r"The vertex is $(-1, 4)$ with $a = 2$, opening downward: $(x + 1)^2 = -8(y - 4)$. At $x = 0$: $1 = -8(y - 4)$, so $y = \frac{31}{8}$. The focal distance equals the distance from the directrix: $6 - \frac{31}{8} = \frac{17}{8}$.",
  r"Using a single coordinate difference as a distance.",
  "U10-D-focal-distance-shifted", "Build a downward parabola, intersect with an axis, use the directrix property.",
  check=_c049, values=[Rational(17, 8), Rational(31, 8), Rational(15, 8), Rational(1, 8)])

# ---------------------------------------------------------------- 050
def _c050():
    a = Symbol('a', real=True)
    yy = Symbol('yy')
    # chord on 2x - y = 4: x = (y + 4)/2, y^2 = 4a x
    quad = Poly(yy**2 - 4*a*(yy + 4)/2, yy)
    c2, c1, c0 = quad.all_coeffs()
    dy2 = (c1**2 - 4*c2*c0) / c2**2
    length2 = Rational(5, 4) * dy2
    sols = [s for s in solve(Eq(length2, 45), a) if s != 0]
    return sum(Abs(4*s) for s in sols)
q("U10-D-050", TOP_INT, "All parabolas cutting a chord of given length", "Difficult", "Inverse/parameter MCQ",
  r"Parabolas of the form $y^2 = 4ax$, $a \ne 0$, cut off a chord of length $3\sqrt{5}$ on the line $2x - y = 4$. The sum of the lengths of the latera recta of all such parabolas is",
  r"$40$",
  [(r"$4$", r"Discards $a = -9$ as inadmissible, although $y^2 = -36x$ is a valid parabola that meets the line."),
   (r"$32$", r"Adds the signed values $4a$: $4 + (-36)$, then drops the sign."),
   (r"$36$", r"Keeps only the parabola with $a = -9$.")],
  r"With $x = \frac{y + 4}{2}$: $y^2 - 2ay - 8a = 0$, so $(y_1 - y_2)^2 = 4a^2 + 32a$. The chord length is $\sqrt{1 + \frac{1}{4}}\,|y_1 - y_2|$, so $\frac{5}{4}(4a^2 + 32a) = 45$, i.e. $a^2 + 8a - 9 = 0$, $a = 1$ or $a = -9$. Both give real chords, so the latera recta are $4$ and $36$, with sum $40$.",
  r"Rejecting a negative $a$ when the stem allows $a \ne 0$.",
  "U10-D-int-chord-parameter", "Chord length in terms of $a$, a quadratic with a negative root that must be kept.",
  check=_c050, values=[40, 4, 32, 36], cognitive="Analysis",
  numerical=dict(question=r"Parabolas of the form $y^2 = 4ax$, $a \ne 0$, cut off a chord of length $3\sqrt{5}$ on the line $2x - y = 4$. The sum of the lengths of the latera recta of all such parabolas is", answer=40))
