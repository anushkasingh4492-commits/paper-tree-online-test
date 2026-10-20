import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x, y = symbols('x y', real=True)
k, m, h, lam, a_ = symbols('k m h lambda a', real=True)
t = Symbol('t', real=True)

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOP_GEN = "Circle: standard and general forms"
TOP_DIA = "Circle: diameter form"
TOP_PTS = "Circle through given points"
TOP_LINE = "Intersection of a line and a circle"
TOP_CHORD = "Length of chord"
TOP_TOUCH = "Conditions for touching"
TOP_POS = "Position of a point"


def canon(e):
    """(D, E, F) of the circle x^2 + y^2 + D x + E y + F = 0 after dividing by the x^2 coefficient."""
    e = expand(e)
    a = e.coeff(x, 2)
    e = expand(e / a)
    return (e.coeff(x, 1).subs(y, 0), e.coeff(y, 1).subs(x, 0), e.subs({x: 0, y: 0}))


def centre_r(e):
    D, E, F = canon(e)
    return (-D / 2, -E / 2, sqrt(D**2 / 4 + E**2 / 4 - F))


def eq_cr(hh, kk, r2):
    return expand((x - hh)**2 + (y - kk)**2 - r2)


def dist_pl(p, L):
    L = expand(L)
    a, b = L.coeff(x, 1), L.coeff(y, 1)
    return simplify(Abs(L.subs({x: p[0], y: p[1]})) / sqrt(a**2 + b**2))


def pts(*eqs):
    return [s for s in solve(list(eqs), [x, y], dict=True)]


def chord_len(circ, line):
    s = pts(circ, line)
    P, Q = s
    return simplify(sqrt((P[x] - Q[x])**2 + (P[y] - Q[y])**2))


# ---------------------------------------------------------------- 001
def _c001():
    return centre_r(2*x**2 + 2*y**2 - 8*x + 12*y + 8)
q("U10-C-001", TOP_GEN, "Centre and radius from the general form", "Easy", "Single-step computation MCQ",
  r"The centre and the radius of the circle $2x^2 + 2y^2 - 8x + 12y + 8 = 0$ are respectively",
  r"$(2, -3)$ and $3$",
  [(r"$(-2, 3)$ and $3$", r"Takes the centre as $(g, f) = (-2, 3)$ instead of $(-g, -f)$; the radius $\sqrt{4 + 9 - 4} = 3$ is unaffected."),
   (r"$(2, -3)$ and $\sqrt{5}$", r"Divides the $x$ and $y$ coefficients by $2$ but keeps the constant as $8$, so $r^2 = 4 + 9 - 8 = 5$."),
   (r"$(4, -6)$ and $4\sqrt{3}$", r"After dividing by $2$, takes the coefficients $-4$ and $6$ themselves as $g$ and $f$ (forgetting the factor $2$ in $2g, 2f$), giving centre $(-g, -f) = (4, -6)$ and $r^2 = 16 + 36 - 4 = 48$.")],
  r"Dividing by $2$: $x^2 + y^2 - 4x + 6y + 4 = 0$, so $g = -2$, $f = 3$, $c = 4$. Centre $(-g, -f) = (2, -3)$ and $r = \sqrt{g^2 + f^2 - c} = \sqrt{4 + 9 - 4} = 3$.",
  r"Reading $g, f, c$ before making the coefficient of $x^2$ equal to $1$.",
  "U10-C-centre-radius-general", "One normalisation and one formula.",
  check=_c001, values=[(2, -3, 3), (-2, 3, 3), (2, -3, sqrt(5)), (4, -6, 4*sqrt(3))], cognitive="Application")

# ---------------------------------------------------------------- 002
def _c002():
    D, E, F = 6, -2, k
    return solve(Eq(D**2/4 + E**2/4 - F, 16), k)[0]
q("U10-C-002", TOP_GEN, "Constant term from a given radius", "Easy", "Inverse/parameter MCQ",
  r"If the circle $x^2 + y^2 + 6x - 2y + k = 0$ has radius $4$, then $k$ equals",
  r"$-6$",
  [(r"$6$", r"Uses $r^2 = g^2 + f^2 + c$: $10 + k = 16$ gives $k = 6$."),
   (r"$24$", r"Takes $g = 6$ and $f = -2$ (the full coefficients): $36 + 4 - k = 16$ gives $k = 24$."),
   (r"$26$", r"Transposes $10 - k = 16$ as $k = 16 + 10 = 26$.")],
  r"Here $g = 3$, $f = -1$, $c = k$, so $r^2 = 9 + 1 - k = 10 - k$. Setting $10 - k = 16$ gives $k = -6$.",
  r"Using the full coefficient of $x$ as $g$ instead of half of it.",
  "U10-C-radius-param", "One formula, solved backwards.",
  check=_c002, values=[-6, 6, 24, 26], cognitive="Application")

# ---------------------------------------------------------------- 003
def _c003():
    P, Q = (2, -3), (-4, 5)
    return canon((x - P[0])*(x - Q[0]) + (y - P[1])*(y - Q[1]))
q("U10-C-003", TOP_DIA, "Equation from the ends of a diameter", "Easy", "Single-step computation MCQ",
  r"The equation of the circle drawn on the segment joining $P(2, -3)$ and $Q(-4, 5)$ as a diameter is",
  r"$x^2 + y^2 + 2x - 2y - 23 = 0$",
  [(r"$x^2 + y^2 - 2x + 2y - 23 = 0$", r"Writes the diameter form as $(x + 2)(x - 4) + (y - 3)(y + 5) = 0$, flipping every sign of the endpoints."),
   (r"$x^2 + y^2 + 2x - 2y - 98 = 0$", r"Uses centre $(-1, 1)$ but takes the radius as the full length $PQ = 10$, so the constant is $1 + 1 - 100 = -98$."),
   (r"$x^2 + y^2 + 2x - 2y - 3 = 0$", r"Uses centre $(-1, 1)$ and radius $5$ but subtracts $5$ rather than $25$: $1 + 1 - 5 = -3$.")],
  r"The diameter form gives $(x - 2)(x + 4) + (y + 3)(y - 5) = 0$, that is $x^2 + 2x - 8 + y^2 - 2y - 15 = 0$, so $x^2 + y^2 + 2x - 2y - 23 = 0$. (Check: centre $(-1, 1)$, $r^2 = 1 + 1 + 23 = 25 = (PQ/2)^2$.)",
  r"Sign slips in $(x - x_1)(x - x_2) + (y - y_1)(y - y_2) = 0$, or using the diameter as the radius.",
  "U10-C-diameter-form", "Direct use of the diameter form.",
  check=_c003, values=[(2, -2, -23), (-2, 2, -23), (2, -2, -98), (2, -2, -3)], cognitive="Application")

# ---------------------------------------------------------------- 004
def _c004():
    S = x**2 + y**2 - 6*x + 4*y - 12
    cands = [(1, 1), (6, 2), (-1, 3), (3, 4)]
    inside = [p for p in cands if S.subs({x: p[0], y: p[1]}) < 0]
    assert len(inside) == 1
    return inside[0]
q("U10-C-004", TOP_POS, "Which point lies inside", "Easy", "Single-step computation MCQ",
  r"Which of the following points lies strictly inside the circle $x^2 + y^2 - 6x + 4y - 12 = 0$?",
  r"$(1, 1)$",
  [(r"$(6, 2)$", r"$S_1 = 36 + 4 - 36 + 8 - 12 = 0$, so the point is on the circle; chosen by treating $S_1 \le 0$ as inside."),
   (r"$(-1, 3)$", r"Takes the centre as $(-3, 2)$ (sign slip); its distance from $(-3, 2)$ is $\sqrt{5} < 5$, but the true $S_1 = 16 > 0$."),
   (r"$(3, 4)$", r"Takes the centre as $(3, 2)$ (sign slip in the $y$ coordinate); distance $2 < 5$, but the true $S_1 = 11 > 0$.")],
  r"For $S = x^2 + y^2 - 6x + 4y - 12$ a point is inside when $S_1 < 0$. At $(1, 1)$: $1 + 1 - 6 + 4 - 12 = -12 < 0$. The other points give $S_1 = 0$, $16$ and $11$, so they are on or outside the circle (centre $(3, -2)$, radius $5$).",
  r"Reading the centre with the wrong signs, or counting a point on the circle as inside.",
  "U10-C-position-point", "One substitution per point.",
  check=_c004, values=[(1, 1), (6, 2), (-1, 3), (3, 4)], cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    s = pts(x**2 + y**2 - 25, y - x - 1)
    return FiniteSet(*[Tuple(d[x], d[y]) for d in s])
q("U10-C-005", TOP_LINE, "Points of intersection with a circle centred at the origin", "Easy", "Single-step computation MCQ",
  r"The line $y = x + 1$ meets the circle $x^2 + y^2 = 25$ at the points",
  r"$(3, 4)$ and $(-4, -3)$",
  [(r"$(-3, -2)$ and $(4, 5)$", r"Solves $x^2 + x - 12 = 0$ with the signs of the roots reversed ($x = -3, 4$)."),
   (r"$(3, 4)$ and $(-3, -4)$", r"Finds $(3, 4)$ and assumes the other point is its reflection in the origin, which is on the circle but not on the line."),
   (r"$(4, 3)$ and $(-3, -4)$", r"Substitutes $x = y + 1$, i.e. solves with the line $y = x - 1$.")],
  r"Substituting $y = x + 1$: $x^2 + (x + 1)^2 = 25$, so $2x^2 + 2x - 24 = 0$, i.e. $x^2 + x - 12 = 0$, giving $x = 3$ or $x = -4$. Then $y = 4$ or $y = -3$, so the points are $(3, 4)$ and $(-4, -3)$.",
  r"Assuming a chord of a circle centred at the origin has endpoints symmetric about the origin.",
  "U10-C-line-origin-circle-points", "One substitution and one quadratic.",
  check=_c005, values=[FiniteSet(Tuple(3, 4), Tuple(-4, -3)), FiniteSet(Tuple(-3, -2), Tuple(4, 5)),
                       FiniteSet(Tuple(3, 4), Tuple(-3, -4)), FiniteSet(Tuple(4, 3), Tuple(-3, -4))],
  cognitive="Application")

# ---------------------------------------------------------------- 006
def _c006():
    c = Symbol('c', positive=True)
    xs = solve(x**2 + (2*x + c)**2 - 20, x)
    disc = discriminant(expand(x**2 + (2*x + c)**2 - 20), x)
    return solve(Eq(disc, 0), c)[0]
q("U10-C-006", TOP_LINE, "Tangency condition from intersection", "Easy", "Inverse/parameter MCQ",
  r"If the line $y = 2x + c$, $c > 0$, meets the circle $x^2 + y^2 = 20$ at exactly one point, then $c$ equals",
  r"$10$",
  [(r"$2\sqrt{15}$", r"Uses $c^2 = a^2(1 + m) = 20 \cdot 3 = 60$, forgetting to square $m$."),
   (r"$4\sqrt{5}$", r"Uses $c^2 = a^2 m^2 = 20 \cdot 4 = 80$."),
   (r"$10\sqrt{5}$", r"Writes the distance condition as $\frac{|c|}{1 + m^2} = r$, omitting the square root: $c = 5 \cdot 2\sqrt{5}$.")],
  r"Substituting, $x^2 + (2x + c)^2 = 20$ gives $5x^2 + 4cx + c^2 - 20 = 0$. Exactly one point means discriminant zero: $16c^2 - 20(c^2 - 20) = 0$, so $c^2 = 100$ and $c = 10$. This is the condition $c^2 = a^2(1 + m^2) = 20 \cdot 5$.",
  r"Misremembering the tangency condition $c^2 = a^2(1 + m^2)$.",
  "U10-C-tangency-condition", "One substitution and the zero discriminant condition.",
  check=_c006, values=[10, 2*sqrt(15), 4*sqrt(5), 10*sqrt(5)],
  numerical=dict(question=r"If the line $y = 2x + c$, $c > 0$, meets the circle $x^2 + y^2 = 20$ at exactly one point, then the value of $c$ is", answer=10),
  cognitive="Application")

# ---------------------------------------------------------------- 007
def _c007():
    r2 = 3**2 + (-4)**2
    return canon(eq_cr(3, -4, r2))
q("U10-C-007", TOP_GEN, "Standard form through a given point", "Easy", "Single-step computation MCQ",
  r"The equation of the circle with centre $(3, -4)$ that passes through the origin is",
  r"$x^2 + y^2 - 6x + 8y = 0$",
  [(r"$x^2 + y^2 + 6x - 8y = 0$", r"Writes $(x + 3)^2 + (y - 4)^2 = 25$, reversing the signs of the centre."),
   (r"$x^2 + y^2 - 6x + 8y - 25 = 0$", r"Expands $(x - 3)^2 + (y + 4)^2 = 25$ but drops the constants $9 + 16$ on the left, leaving $-25$."),
   (r"$x^2 + y^2 - 3x + 4y = 0$", r"Uses $-h$ and $-k$ as the coefficients of $x$ and $y$ instead of $-2h$ and $-2k$.")],
  r"The radius is the distance from $(3, -4)$ to the origin, $5$. So $(x - 3)^2 + (y + 4)^2 = 25$, i.e. $x^2 - 6x + 9 + y^2 + 8y + 16 = 25$, giving $x^2 + y^2 - 6x + 8y = 0$.",
  r"Forgetting that a circle through the origin has zero constant term.",
  "U10-C-standard-form-through-point", "Radius by distance, then expand.",
  check=_c007, values=[(-6, 8, 0), (6, -8, 0), (-6, 8, -25), (-3, 4, 0)], cognitive="Application")

# ---------------------------------------------------------------- 008
def _c008():
    r = 3
    hh, kk = r, -r  # fourth quadrant, touching both axes
    assert dist_pl((hh, kk), x) == r and dist_pl((hh, kk), y) == r
    return canon(eq_cr(hh, kk, r**2))
q("U10-C-008", TOP_TOUCH, "Circle touching both axes", "Easy", "Single-step computation MCQ",
  r"A circle of radius $3$ touches both coordinate axes and its centre lies in the fourth quadrant. Its equation is",
  r"$x^2 + y^2 - 6x + 6y + 9 = 0$",
  [(r"$x^2 + y^2 + 6x - 6y + 9 = 0$", r"Places the centre at $(-3, 3)$, the second quadrant."),
   (r"$x^2 + y^2 - 6x + 6y + 18 = 0$", r"Expands $(x - 3)^2 + (y + 3)^2 = 9$ but does not subtract $9$, keeping the constant $9 + 9 = 18$."),
   (r"$x^2 + y^2 - 6x - 6y + 9 = 0$", r"Places the centre at $(3, 3)$, the first quadrant.")],
  r"Touching both axes with radius $3$ means the centre is $(\pm 3, \pm 3)$; in the fourth quadrant it is $(3, -3)$. So $(x - 3)^2 + (y + 3)^2 = 9$, i.e. $x^2 + y^2 - 6x + 6y + 9 = 0$.",
  r"Getting the signs of the centre wrong for the given quadrant.",
  "U10-C-touch-axes", "One condition (centre at distance $r$ from both axes) and expansion.",
  check=_c008, values=[(-6, 6, 9), (6, -6, 9), (-6, 6, 18), (-6, -6, 9)], cognitive="Application")

# ---------------------------------------------------------------- 009
def _c009():
    return chord_len(x**2 + y**2 - 13, 3*x + 4*y - 10)
q("U10-C-009", TOP_CHORD, "Chord intercepted on a circle centred at the origin", "Easy", "Single-step computation MCQ",
  r"The length of the chord intercepted by the circle $x^2 + y^2 = 13$ on the line $3x + 4y = 10$ is",
  r"$6$",
  [(r"$3$", r"Stops at the half chord $\sqrt{13 - 4} = 3$."),
   (r"$2\sqrt{17}$", r"Adds instead of subtracting: $2\sqrt{13 + 4}$."),
   (r"$2\sqrt{13}$", r"Takes the chord as a diameter, ignoring the distance of the line from the centre.")],
  r"The distance of the origin from the line is $\frac{10}{5} = 2$. The half chord is $\sqrt{13 - 4} = 3$, so the chord has length $6$.",
  r"Forgetting to double the half chord.",
  "U10-C-chord-length", "One distance and the right triangle with the radius.",
  check=_c009, values=[6, 3, 2*sqrt(17), 2*sqrt(13)],
  numerical=dict(question=r"The length of the chord intercepted by the circle $x^2 + y^2 = 13$ on the line $3x + 4y = 10$ is", answer=6),
  cognitive="Application")

# ---------------------------------------------------------------- 010
def _c010():
    p, qq = symbols('p q')
    S = x**2 + y**2 + p*x + qq*y - 20
    s = solve([S.subs({x: 4, y: 2}), S.subs({x: -2, y: 2})], [p, qq], dict=True)[0]
    return centre_r(S.subs(s))[2]
q("U10-C-010", TOP_PTS, "Unknown coefficients from two points on the circle", "Easy", "Single-step computation MCQ",
  r"The circle $x^2 + y^2 + px + qy - 20 = 0$ passes through the points $(4, 2)$ and $(-2, 2)$. The radius of the circle is",
  r"$5$",
  [(r"$3$", r"Assumes the two given points are the ends of a diameter, taking the centre as their midpoint $(1, 2)$ and the radius as half their distance, $\frac{6}{2} = 3$."),
   (r"$2\sqrt{10}$", r"Finds $p = -2$, $q = 4$ correctly but uses $p$ and $q$ themselves as $g$ and $f$: $r^2 = 4 + 16 + 20 = 40$."),
   (r"$\sqrt{5}$", r"Finds the centre $(1, -2)$ correctly but drops the constant term: $r^2 = 1 + 4 = 5$.")],
  r"Putting $(4, 2)$: $16 + 4 + 4p + 2q - 20 = 0$, so $2p + q = 0$. Putting $(-2, 2)$: $4 + 4 - 2p + 2q - 20 = 0$, so $-p + q = 6$. Subtracting, $3p = -6$, so $p = -2$ and $q = 4$. The circle is $x^2 + y^2 - 2x + 4y - 20 = 0$ with centre $(1, -2)$ and $r = \sqrt{1 + 4 + 20} = 5$.",
  r"Treating any two given points on a circle as the ends of a diameter.",
  "U10-C-coefficients-from-points", "Two linear equations for the coefficients, then the radius formula.",
  check=_c010, values=[5, 3, 2*sqrt(10), sqrt(5)],
  numerical=dict(question=r"The circle $x^2 + y^2 + px + qy - 20 = 0$ passes through the points $(4, 2)$ and $(-2, 2)$. The radius of the circle is", answer=5),
  cognitive="Application")

# ---------------------------------------------------------------- 011
def _c011():
    cands = [(3, 4, 20), (3, 4, 16), (3, 4, 4), (3, 4, 28)]
    tang = [L for L in cands if dist_pl((0, 0), L[0]*x + L[1]*y - L[2]) == 4]
    assert len(tang) == 1
    return tang[0]
q("U10-C-011", TOP_LINE, "Identifying a tangent line", "Easy", "Single-step computation MCQ",
  r"Which of the following lines meets the circle $x^2 + y^2 = 16$ at exactly one point?",
  r"$3x + 4y = 20$",
  [(r"$3x + 4y = 16$", r"Takes the condition as $|c| = r^2 = 16$; its distance from the origin is $\frac{16}{5} < 4$, so it cuts the circle twice."),
   (r"$3x + 4y = 4$", r"Takes $|c| = r$, forgetting to divide by $\sqrt{3^2 + 4^2}$; this line cuts the circle twice."),
   (r"$3x + 4y = 28$", r"Divides by $3 + 4$ instead of $\sqrt{3^2 + 4^2}$; its true distance is $\frac{28}{5} > 4$, so it misses the circle.")],
  r"A line touches the circle exactly when its distance from the centre equals the radius $4$. For $3x + 4y = 20$ the distance from the origin is $\frac{20}{\sqrt{9 + 16}} = 4$, so it meets the circle at exactly one point.",
  r"Using $a + b$ or nothing in place of $\sqrt{a^2 + b^2}$ in the perpendicular distance.",
  "U10-C-tangency-condition", "One distance computation per line.",
  check=_c011, values=[(3, 4, 20), (3, 4, 16), (3, 4, 4), (3, 4, 28)], cognitive="Understanding")

# ---------------------------------------------------------------- 012
def _c012():
    r = dist_pl((2, -1), 3*x - 4*y + 5)
    return canon(eq_cr(2, -1, r**2))
q("U10-C-012", TOP_TOUCH, "Circle with given centre touching a line", "Easy", "Single-step computation MCQ",
  r"The circle with centre $(2, -1)$ that touches the line $3x - 4y + 5 = 0$ is",
  r"$x^2 + y^2 - 4x + 2y - 4 = 0$",
  [(r"$x^2 + y^2 - 4x + 2y + 2 = 0$", r"Finds $r = 3$ but subtracts $r$ instead of $r^2$: $4 + 1 - 3 = 2$."),
   (r"$x^2 + y^2 + 4x - 2y - 4 = 0$", r"Uses centre $(-2, 1)$ when writing the equation."),
   (r"$x^2 + y^2 - 4x + 2y + 1 = 0$", r"Drops the $+5$ in the distance: $r = \frac{|6 + 4|}{5} = 2$, constant $5 - 4 = 1$.")],
  r"The radius is the distance from the centre to the line: $\frac{|3(2) - 4(-1) + 5|}{5} = \frac{15}{5} = 3$. So $(x - 2)^2 + (y + 1)^2 = 9$, i.e. $x^2 + y^2 - 4x + 2y - 4 = 0$.",
  r"Subtracting $r$ in place of $r^2$ when expanding.",
  "U10-C-touch-line-centre", "Distance from a point to a line, then expand.",
  check=_c012, values=[(-4, 2, -4), (-4, 2, 2), (4, -2, -4), (-4, 2, 1)], cognitive="Application")

# ---------------------------------------------------------------- 013
def _c013():
    hh, kk, r = centre_r(x**2 + y**2 - 4*x + 6*y - 12)
    P = (-1, 1)
    assert (x**2 + y**2 - 4*x + 6*y - 12).subs({x: -1, y: 1}) == 0
    return (2*hh - P[0], 2*kk - P[1])
q("U10-C-013", TOP_DIA, "Other end of a diameter", "Easy", "Single-step computation MCQ",
  r"One end of a diameter of the circle $x^2 + y^2 - 4x + 6y - 12 = 0$ is $(-1, 1)$. The other end is",
  r"$(5, -7)$",
  [(r"$(-3, 5)$", r"Uses the centre $(-2, 3)$ (sign slip): $(2(-2) + 1, 2(3) - 1)$."),
   (r"$(\frac{1}{2}, -1)$", r"Takes the midpoint of the given end and the centre."),
   (r"$(3, -4)$", r"Subtracts the given end from the centre, $(2 - (-1), -3 - 1)$, instead of reflecting it in the centre.")],
  r"The centre is $(2, -3)$, the midpoint of the diameter. If the other end is $(p, q)$ then $\frac{p - 1}{2} = 2$ and $\frac{q + 1}{2} = -3$, so $(p, q) = (5, -7)$.",
  r"Reading the centre with wrong signs.",
  "U10-C-diameter-end", "Centre and the midpoint formula.",
  check=_c013, values=[(5, -7), (-3, 5), (Rational(1, 2), -1), (3, -4)], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    D, E, F = canon(x**2 + y**2 + 2*x + 4*y + 6)
    s1 = (D**2/4 + E**2/4 - F) < 0  # represents no real circle
    hh, kk, r = centre_r(x**2 + y**2 - 4*x - 6*y + 4)
    s2 = (Abs(hh) == r)  # touches the y-axis
    return (bool(s1), bool(s2))
q("U10-C-014", TOP_GEN, "Reality of a circle; touching an axis", "Easy", "Statement-based MCQ",
  r"Statement I: The equation $x^2 + y^2 + 2x + 4y + 6 = 0$ does not represent a real circle." "\n"
  r"Statement II: The circle $x^2 + y^2 - 4x - 6y + 4 = 0$ touches the $y$-axis." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II by checking $g^2 = c$ ($4 = 4$), which is the condition for touching the $x$-axis."),
   (ST_FF, r"Rejects Statement I by computing $g^2 + f^2 + c = 11 > 0$ with the wrong sign of $c$, and correctly rejects Statement II."),
   (ST_FT, r"Makes both slips: wrong sign of $c$ in Statement I and the $x$-axis condition in Statement II.")],
  r"For the first equation $g^2 + f^2 - c = 1 + 4 - 6 = -1 < 0$, so it is not a real circle; Statement I is true. The second circle has centre $(2, 3)$ and radius $\sqrt{4 + 9 - 4} = 3$. Its distance from the $y$-axis is $2 \ne 3$, so it does not touch the $y$-axis (it touches the $x$-axis, since $|3| = 3$); Statement II is false.",
  r"Mixing up the conditions $g^2 = c$ (touches the $x$-axis) and $f^2 = c$ (touches the $y$-axis).",
  "U10-C-stmt-real-touch-axis", "Two short checks of standard conditions.",
  check=_c014, values=[(T, F_), (T, T), (F_, F_), (F_, T)], cognitive="Understanding")

# ---------------------------------------------------------------- 015
def _c015():
    xs = solve((x**2 + y**2 - 6*x + 4*y - 16).subs(y, 0), x)
    return Abs(xs[0] - xs[1])
q("U10-C-015", TOP_CHORD, "Intercept on the x-axis", "Easy", "Single-step computation MCQ",
  r"The length of the intercept made by the circle $x^2 + y^2 - 6x + 4y - 16 = 0$ on the $x$-axis is",
  r"$10$",
  [(r"$4\sqrt{5}$", r"Finds the intercept on the $y$-axis instead: $2\sqrt{f^2 - c} = 2\sqrt{4 + 16}$."),
   (r"$5$", r"Uses $\sqrt{g^2 - c} = \sqrt{25}$ without the factor $2$."),
   (r"$2\sqrt{29}$", r"Gives the diameter $2\sqrt{9 + 4 + 16}$, as if the $x$-axis passed through the centre.")],
  r"Putting $y = 0$: $x^2 - 6x - 16 = 0$, so $x = 8$ or $x = -2$. The intercept is $8 - (-2) = 10$, which agrees with $2\sqrt{g^2 - c} = 2\sqrt{9 + 16}$.",
  r"Confusing the $x$-intercept $2\sqrt{g^2 - c}$ with the $y$-intercept $2\sqrt{f^2 - c}$.",
  "U10-C-axis-intercepts", "One substitution and one quadratic.",
  check=_c015, values=[10, 4*sqrt(5), 5, 2*sqrt(29)],
  numerical=dict(question=r"The length of the intercept made by the circle $x^2 + y^2 - 6x + 4y - 16 = 0$ on the $x$-axis is", answer=10),
  cognitive="Application")

# ---------------------------------------------------------------- 016
def _c016():
    e = (k - 1)*x**2 + 4*y**2 + (k**2 - 25)*x*y + 8*x - 4*y + 1
    P = Poly(e, x, y)
    ks = solve([P.coeff_monomial(x**2) - P.coeff_monomial(y**2), P.coeff_monomial(x*y)], k)
    kk = [s[0] if isinstance(s, tuple) else s[k] for s in (ks if isinstance(ks, list) else [ks])]
    assert len(kk) == 1
    return centre_r(e.subs(k, kk[0]))[2]
q("U10-C-016", TOP_GEN, "Condition for a second-degree equation to be a circle", "Medium", "Multi-step computation MCQ",
  r"For a real number $k$, the equation $(k - 1)x^2 + 4y^2 + (k^2 - 25)xy + 8x - 4y + 1 = 0$ represents a circle. The radius of this circle is",
  r"$1$",
  [(r"$\frac{\sqrt{19}}{2}$", r"Divides by $4$ but takes $g = 2$ and $f = -1$ (the full coefficients of $x$ and $y$): $r^2 = 4 + 1 - \frac{1}{4} = \frac{19}{4}$."),
   (r"$\frac{1}{2}$", r"Divides the $x$ and $y$ coefficients by $4$ but keeps the constant $1$: $r^2 = 1 + \frac{1}{4} - 1 = \frac{1}{4}$."),
   (r"$\frac{\sqrt{6}}{2}$", r"Uses $r^2 = g^2 + f^2 + c = 1 + \frac{1}{4} + \frac{1}{4} = \frac{3}{2}$.")],
  r"A circle needs equal coefficients of $x^2$ and $y^2$ and no $xy$ term: $k - 1 = 4$ and $k^2 - 25 = 0$, so $k = 5$. The equation is $4x^2 + 4y^2 + 8x - 4y + 1 = 0$, i.e. $x^2 + y^2 + 2x - y + \frac{1}{4} = 0$. Then $r^2 = 1 + \frac{1}{4} - \frac{1}{4} = 1$, so $r = 1$.",
  r"Reading $g, f, c$ before making the coefficient of $x^2$ equal to $1$.",
  "U10-C-circle-condition", "Two conditions for a circle, then normalisation and the radius formula.",
  check=_c016, values=[1, sqrt(19)/2, Rational(1, 2), sqrt(6)/2], cognitive="Application")

# ---------------------------------------------------------------- 017
def _c017():
    g, f, c = symbols('g f c')
    P = [(-1, 2), (3, 4), (5, 0)]
    s = solve([px**2 + py**2 + 2*g*px + 2*f*py + c for px, py in P], [g, f, c])
    return (-s[g], -s[f])
q("U10-C-017", TOP_PTS, "Centre of the circle through three points", "Medium", "Multi-step computation MCQ",
  r"The centre of the circle passing through the points $(-1, 2)$, $(3, 4)$ and $(5, 0)$ is",
  r"$(2, 1)$",
  [(r"$(-2, -1)$", r"Solves correctly for $g = -2$, $f = -1$ but reports $(g, f)$ as the centre."),
   (r"$(\frac{7}{3}, 2)$", r"Takes the centroid of the three points, which is not equidistant from them."),
   (r"$(4, 2)$", r"Reports $(-2g, -2f)$, the negatives of the coefficients of $x$ and $y$.")],
  r"Let the centre be $(p, q)$. Equal distances to $(-1, 2)$ and $(3, 4)$ give $2p + q = 5$; equal distances to $(3, 4)$ and $(5, 0)$ give $p - 2q = 0$. Hence $p = 2$, $q = 1$, and the centre is $(2, 1)$ (radius $\sqrt{10}$).",
  r"Confusing the circumcentre with the centroid.",
  "U10-C-three-points", "Two perpendicular bisector equations solved together.",
  check=_c017, values=[(2, 1), (-2, -1), (Rational(7, 3), 2), (4, 2)], cognitive="Application")

# ---------------------------------------------------------------- 018
def _c018():
    hs = solve(Eq((h - 2)**2 + 0**2, h**2 + 4**2), h)
    hh = hs[0]
    return canon(eq_cr(hh, 0, (hh - 2)**2))
q("U10-C-018", TOP_PTS, "Centre on the x-axis", "Medium", "Multi-step computation MCQ",
  r"A circle passes through $(2, 0)$ and $(0, 4)$ and has its centre on the $x$-axis. Its equation is",
  r"$x^2 + y^2 + 6x - 16 = 0$",
  [(r"$x^2 + y^2 - 6x + 8 = 0$", r"Expands $(h - 2)^2 = h^2 + 16$ as $4h + 4 = 16$, getting $h = 3$ and $r = 1$."),
   (r"$x^2 + y^2 + 6x - 25 = 0$", r"Writes $(x + 3)^2 + y^2 = 25$ as $x^2 + 6x + y^2 = 25$, dropping the $9$."),
   (r"$x^2 + y^2 + 6x + 16 = 0$", r"Gets the constant as $25 - 9$ with the wrong sign after transposing.")],
  r"Let the centre be $(h, 0)$. Then $(h - 2)^2 = h^2 + 16$, so $-4h + 4 = 16$ and $h = -3$; the radius is $|{-3} - 2| = 5$. The circle is $(x + 3)^2 + y^2 = 25$, i.e. $x^2 + y^2 + 6x - 16 = 0$.",
  r"Sign slips in the equal distance equation.",
  "U10-C-centre-on-line", "Equal distances with a constrained centre, then expansion.",
  check=_c018, values=[(6, 0, -16), (-6, 0, 8), (6, 0, -25), (6, 0, 16)], cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    p, qq = symbols('p q', real=True)
    s = solve([Eq((p - 2)**2 + (qq - 3)**2, (p - 4)**2 + (qq - 1)**2), p + 2*qq - 4], [p, qq], dict=True)[0]
    r2 = (s[p] - 2)**2 + (s[qq] - 3)**2
    return canon(eq_cr(s[p], s[qq], r2))
q("U10-C-019", TOP_PTS, "Centre on a given line", "Medium", "Multi-step computation MCQ",
  r"The circle passing through $(2, 3)$ and $(4, 1)$ whose centre lies on the line $x + 2y = 4$ is",
  r"$x^2 + y^2 - 4x - 2y + 1 = 0$",
  [(r"$x^2 + y^2 - 12x + 2y + 5 = 0$", r"Takes the perpendicular bisector of the two points with slope $-1$ (the slope of the chord itself), $x + y = 5$, which meets $x + 2y = 4$ at $(6, -1)$, so $r^2 = 32$."),
   (r"$x^2 + y^2 + 4x + 2y + 1 = 0$", r"Finds the centre $(2, 1)$ but writes the equation with centre $(-2, -1)$."),
   (r"$x^2 + y^2 - 4x - 2y + 3 = 0$", r"Finds $r = 2$ but subtracts $r$ instead of $r^2$: $4 + 1 - 2 = 3$.")],
  r"The perpendicular bisector of the segment from $(2, 3)$ to $(4, 1)$ passes through $(3, 2)$ with slope $1$: $y = x - 1$. With $x + 2y = 4$ this gives $3x - 2 = 4$, so the centre is $(2, 1)$ and $r^2 = 0 + 4 = 4$. Hence $(x - 2)^2 + (y - 1)^2 = 4$, i.e. $x^2 + y^2 - 4x - 2y + 1 = 0$.",
  r"Using the chord's own slope for its perpendicular bisector.",
  "U10-C-centre-on-line", "Perpendicular bisector, intersection with a line, then expansion.",
  check=_c019, values=[(-4, -2, 1), (-12, 2, 5), (4, 2, 1), (-4, -2, 3)], cognitive="Application")

# ---------------------------------------------------------------- 020
def _c020():
    return chord_len(x**2 + y**2 - 25, y - 2*x + 5)
q("U10-C-020", TOP_CHORD, "Chord length from the perpendicular distance", "Medium", "Multi-step computation MCQ",
  r"The length of the chord of the circle $x^2 + y^2 = 25$ along the line $y = 2x - 5$ is",
  r"$4\sqrt{5}$",
  [(r"$2\sqrt{5}$", r"Stops at the half chord $\sqrt{25 - 5}$."),
   (r"$2\sqrt{30}$", r"Adds instead of subtracting: $2\sqrt{25 + 5}$."),
   (r"$4\sqrt{6}$", r"Takes the distance as $\frac{5}{1 + m^2} = 1$, omitting the square root, so the chord is $2\sqrt{24}$.")],
  r"The line is $2x - y - 5 = 0$; its distance from the origin is $\frac{5}{\sqrt{5}} = \sqrt{5}$. The half chord is $\sqrt{25 - 5} = 2\sqrt{5}$, so the chord is $4\sqrt{5}$. (Directly: the line meets the circle at $(0, -5)$ and $(4, 3)$, which are $\sqrt{16 + 64} = 4\sqrt{5}$ apart.)",
  r"Omitting the square root in the perpendicular distance formula.",
  "U10-C-chord-length", "Distance, Pythagoras, doubling.",
  check=_c020, values=[4*sqrt(5), 2*sqrt(5), 2*sqrt(30), 4*sqrt(6)], cognitive="Application")

# ---------------------------------------------------------------- 021
def _c021():
    mm = Symbol('mm', positive=True)
    L = chord_len(x**2 + y**2 - 25, y - mm*x - 5)
    return solve(Eq(L, 6), mm)[0]
q("U10-C-021", TOP_CHORD, "Slope from a given chord length", "Medium", "Inverse/parameter MCQ",
  r"The line $y = mx + 5$, $m > 0$, cuts the circle $x^2 + y^2 = 25$ in a chord of length $6$. Then $m$ equals",
  r"$\frac{3}{4}$",
  [(r"$\frac{4}{3}$", r"Uses the half chord $3$ as the distance from the centre: $\frac{25}{1 + m^2} = 9$, so $m^2 = \frac{16}{9}$."),
   (r"$\frac{1}{2}$", r"Takes the distance as $\frac{5}{1 + m^2} = 4$, omitting the square root, so $m^2 = \frac{1}{4}$."),
   (r"$\frac{9}{16}$", r"Writes the distance as $\frac{5}{\sqrt{1 + m}} = 4$, forgetting to square $m$.")],
  r"Half chord $3$ and radius $5$ give distance $4$ from the centre. So $\frac{5}{\sqrt{1 + m^2}} = 4$, i.e. $1 + m^2 = \frac{25}{16}$, and $m = \frac{3}{4}$ since $m > 0$.",
  r"Swapping the roles of the half chord and the distance from the centre.",
  "U10-C-chord-length-param", "Chord length relation solved backwards for a slope.",
  check=_c021, values=[Rational(3, 4), Rational(4, 3), Rational(1, 2), Rational(9, 16)], cognitive="Application")

# ---------------------------------------------------------------- 022
def _c022():
    s = pts(x**2 + y**2 - 10, x + 2*y - 5)
    return ((s[0][x] + s[1][x]) / 2, (s[0][y] + s[1][y]) / 2)
q("U10-C-022", TOP_LINE, "Midpoint of a chord", "Medium", "Multi-step computation MCQ",
  r"The line $x + 2y = 5$ meets the circle $x^2 + y^2 = 10$ at $P$ and $Q$. The midpoint of $PQ$ is",
  r"$(1, 2)$",
  [(r"$(3, 1)$", r"Solves the quadratic, finds $y = 1$ first and reports the endpoint $P(3, 1)$ of the chord instead of the midpoint."),
   (r"$(\frac{5}{2}, \frac{5}{4})$", r"Takes the midpoint of the intercepts $(5, 0)$ and $(0, \frac{5}{2})$ made by the line on the axes."),
   (r"$(-3, 4)$", r"Uses $y_1 + y_2 = \frac{20}{5} = 4$ as the midpoint ordinate without halving, then $x = 5 - 2(4) = -3$.")],
  r"Substituting $x = 5 - 2y$: $(5 - 2y)^2 + y^2 = 10$, so $5y^2 - 20y + 15 = 0$, giving $y = 1, 3$ and $x = 3, -1$. Thus $P(3, 1)$, $Q(-1, 3)$ and the midpoint is $(1, 2)$. This is the foot of the perpendicular from the centre to the chord.",
  r"Confusing the midpoint of the chord with the midpoint of the axis intercepts of the line.",
  "U10-C-chord-midpoint", "Solve a quadratic for both points, then average.",
  check=_c022, values=[(1, 2), (3, 1), (Rational(5, 2), Rational(5, 4)), (-3, 4)], cognitive="Application")

# ---------------------------------------------------------------- 023
def _c023():
    kk = solve(Eq((3 - 1)**2 + (k - 4)**2, k**2), k)[0]
    return canon(eq_cr(3, kk, kk**2))
q("U10-C-023", TOP_TOUCH, "Circle touching the x-axis at a given point", "Medium", "Multi-step computation MCQ",
  r"A circle touches the $x$-axis at $(3, 0)$ and passes through $(1, 4)$. Its equation is",
  r"$x^2 + y^2 - 6x - 5y + 9 = 0$",
  [(r"$x^2 + y^2 - 6x - 4y + 9 = 0$", r"Drops the $(3 - 1)^2$ term: $(k - 4)^2 = k^2$ gives $k = 2$."),
   (r"$x^2 + y^2 - 6x + 5y + 9 = 0$", r"Finds $k = \frac{5}{2}$ but writes the centre as $(3, -\frac{5}{2})$."),
   (r"$x^2 + y^2 - 6x - 5y + \frac{61}{4} = 0$", r"Expands $(x - 3)^2 + (y - \frac{5}{2})^2 = \frac{25}{4}$ but adds $\frac{25}{4}$ to the constant instead of cancelling it, getting $\frac{61}{4}$.")],
  r"Touching the $x$-axis at $(3, 0)$ puts the centre at $(3, k)$ with radius $|k|$. Then $(3 - 1)^2 + (k - 4)^2 = k^2$ gives $20 - 8k = 0$, so $k = \frac{5}{2}$. The circle is $(x - 3)^2 + (y - \frac{5}{2})^2 = \frac{25}{4}$, i.e. $x^2 + y^2 - 6x - 5y + 9 = 0$.",
  r"Not using that the centre lies vertically above the point of contact.",
  "U10-C-touch-axis-at-point", "Contact condition fixes the centre's line; one equation for $k$.",
  check=_c023, values=[(-6, -5, 9), (-6, -4, 9), (-6, 5, 9), (-6, -5, Rational(61, 4))], cognitive="Application")

# ---------------------------------------------------------------- 024
def _c024():
    hs = solve(Eq((h - 2)**2 + (h - 1)**2, h**2), h)
    assert all(v > 0 for v in hs)
    return sum(hs)
q("U10-C-024", TOP_TOUCH, "Circles touching both axes through a point", "Medium", "Multi-step computation MCQ",
  r"Two distinct circles touch both coordinate axes and pass through the point $(2, 1)$. The sum of their radii is",
  r"$6$",
  [(r"$5$", r"Takes the product of the roots of $h^2 - 6h + 5 = 0$ instead of the sum."),
   (r"$4$", r"Takes the difference $5 - 1$ of the two radii."),
   (r"$12$", r"Adds the diameters $2 + 10$ instead of the radii.")],
  r"The point is in the first quadrant, so each centre is $(h, h)$ with radius $h > 0$. Then $(h - 2)^2 + (h - 1)^2 = h^2$ gives $h^2 - 6h + 5 = 0$, so $h = 1$ or $h = 5$. The sum of the radii is $6$.",
  r"Confusing the sum and product of the roots.",
  "U10-C-touch-axes", "Locate the quadrant, set up a quadratic, use both roots.",
  check=_c024, values=[6, 5, 4, 12],
  numerical=dict(question=r"Two distinct circles touch both coordinate axes and pass through the point $(2, 1)$. The sum of their radii is", answer=6),
  cognitive="Application")

# ---------------------------------------------------------------- 025
def _c025():
    e = x**2 + y**2 - 2*k*x + 4*y + k + 2
    hh, kk, r = centre_r(e)
    ks = solve(Eq(r**2, kk**2), k)  # radius equals distance of centre from the x-axis
    assert all(simplify(r.subs(k, v)**2) > 0 for v in ks)
    return sum(ks)
q("U10-C-025", TOP_TOUCH, "Parameter for touching the x-axis", "Medium", "Inverse/parameter MCQ",
  r"The circle $x^2 + y^2 - 2kx + 4y + k + 2 = 0$ touches the $x$-axis. The sum of all real values of $k$ is",
  r"$1$",
  [(r"$-1$", r"Factorises $k^2 - k - 2 = 0$ as $(k + 2)(k - 1) = 0$, getting $k = -2, 1$."),
   (r"$2$", r"Uses the condition for touching the $y$-axis, $f^2 = c$: $4 = k + 2$."),
   (r"$-2$", r"Takes the product of the roots of $k^2 - k - 2 = 0$.")],
  r"Here $g = -k$, $c = k + 2$. The circle touches the $x$-axis when $g^2 = c$, i.e. $k^2 = k + 2$, so $k = 2$ or $k = -1$. Both give $r^2 = k^2 + 4 - k - 2 = 4 > 0$, so both are valid and their sum is $1$.",
  r"Mixing up the conditions for touching the $x$-axis and the $y$-axis.",
  "U10-C-touch-axis-param", "Contact condition gives a quadratic; check both roots.",
  check=_c025, values=[1, -1, 2, -2],
  numerical=dict(question=r"The circle $x^2 + y^2 - 2kx + 4y + k + 2 = 0$ touches the $x$-axis. The sum of all real values of $k$ is", answer=1),
  cognitive="Application")

# ---------------------------------------------------------------- 026
def _c026():
    hh, kk, r = centre_r(x**2 + y**2 - 2*x - 4*y - 4)
    d = sqrt((7 - hh)**2 + (5 - kk)**2)
    assert d > r
    return d - r
q("U10-C-026", TOP_POS, "Least distance of an external point from a circle", "Medium", "Multi-step computation MCQ",
  r"The least distance of the point $(7, 5)$ from the circle $x^2 + y^2 - 2x - 4y - 4 = 0$ is",
  r"$3\sqrt{5} - 3$",
  [(r"$3\sqrt{5} + 3$", r"Adds the radius, which gives the greatest distance."),
   (r"$3\sqrt{5}$", r"Gives the distance from the point to the centre."),
   (r"$6$", r"Computes $\sqrt{S_1} = \sqrt{36}$, which is the length of the tangent from the point.")],
  r"The centre is $(1, 2)$ and the radius is $\sqrt{1 + 4 + 4} = 3$. The point is at distance $\sqrt{36 + 9} = 3\sqrt{5} > 3$ from the centre, so it is outside and the least distance is $3\sqrt{5} - 3$.",
  r"Using the distance to the centre or the tangent length as the least distance.",
  "U10-C-point-circle-distance", "Centre, radius, distance, then subtract.",
  check=_c026, values=[3*sqrt(5) - 3, 3*sqrt(5) + 3, 3*sqrt(5), 6], cognitive="Application")

# ---------------------------------------------------------------- 027
def _c027():
    d = dist_pl((0, 0), 3*x + 4*y - 40)
    assert d > 5
    return d - 5
q("U10-C-027", TOP_LINE, "Least distance between a line and a circle", "Medium", "Single-step computation MCQ",
  r"The least distance between the line $3x + 4y = 40$ and the circle $x^2 + y^2 = 25$ is",
  r"$3$",
  [(r"$8$", r"Gives the distance from the centre to the line."),
   (r"$13$", r"Adds the radius to the distance from the centre."),
   (r"$\sqrt{39}$", r"Computes $\sqrt{8^2 - 5^2}$, as for a tangent length.")],
  r"The distance of the centre $(0, 0)$ from the line is $\frac{40}{5} = 8 > 5$, so the line does not meet the circle. The least distance is $8 - 5 = 3$.",
  r"Not subtracting the radius from the distance of the centre.",
  "U10-C-line-circle-distance", "One distance; recognising the line misses the circle.",
  check=_c027, values=[3, 8, 13, sqrt(39)],
  numerical=dict(question=r"The least distance between the line $3x + 4y = 40$ and the circle $x^2 + y^2 = 25$ is", answer=3),
  cognitive="Application")

# ---------------------------------------------------------------- 028
def _c028():
    return solveset(a_**2 + (a_ + 1)**2 - 13 < 0, a_, S.Reals)
q("U10-C-028", TOP_POS, "Parameter range for an interior point", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $a$ for which the point $(a, a + 1)$ lies strictly inside the circle $x^2 + y^2 = 13$ is",
  r"$(-3, 2)$",
  [(r"$[-3, 2]$", r"Includes the endpoints, where the point lies on the circle."),
   (r"$(-2, 3)$", r"Factorises $a^2 + a - 6$ as $(a + 2)(a - 3)$."),
   (r"$(-\infty, -3) \cup (2, \infty)$", r"Solves $S_1 > 0$, which describes points outside the circle.")],
  r"Inside means $a^2 + (a + 1)^2 < 13$, i.e. $2a^2 + 2a - 12 < 0$, i.e. $(a + 3)(a - 2) < 0$. Hence $-3 < a < 2$.",
  r"Including boundary points for a strict inequality.",
  "U10-C-position-point", "Position condition becomes a quadratic inequality.",
  check=_c028, values=[Interval.open(-3, 2), Interval(-3, 2), Interval.open(-2, 3),
                       Union(Interval.open(-oo, -3), Interval.open(2, oo))], cognitive="Application")

# ---------------------------------------------------------------- 029
def _c029():
    s1 = chord_len(x**2 + y**2 - 25, x + y - 5) == 5
    e2 = (x - 1)*(x - 4) + (y - 2)*(y + 2)
    s2 = e2.subs({x: 0, y: 0}) == 0
    return (bool(s1), bool(s2))
q("U10-C-029", TOP_DIA, "Chord length and the diameter form", "Medium", "Statement-based MCQ",
  r"Statement I: The chord of the circle $x^2 + y^2 = 25$ along the line $x + y = 5$ has length $5$." "\n"
  r"Statement II: The circle drawn on the segment joining $(1, 2)$ and $(4, -2)$ as a diameter passes through the origin." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Takes the chord length as the intercept $5$ cut on one axis instead of the distance $\sqrt{5^2 + 5^2}$ between $(5, 0)$ and $(0, 5)$; evaluates Statement II correctly."),
   (ST_FF, r"Rejects Statement II by using the full length $PQ = 5$ as the radius about the centre $(\frac{5}{2}, 0)$, so the origin, at distance $\frac{5}{2}$, seems not to lie on the circle."),
   (ST_TF, r"Takes the chord length as the axis intercept $5$ and also uses $PQ = 5$ as the radius in Statement II.")],
  r"The line $x + y = 5$ meets $x^2 + y^2 = 25$ at $(5, 0)$ and $(0, 5)$, so the chord has length $5\sqrt{2}$; Statement I is false. The diameter form gives $(x - 1)(x - 4) + (y - 2)(y + 2) = 0$; at the origin this is $4 - 4 = 0$, so the circle passes through the origin; Statement II is true.",
  r"Sign slips in the diameter form, and confusing a chord with a radius.",
  "U10-C-stmt-chord-diameter", "Two independent short computations.",
  check=_c029, values=[(F_, T), (T, T), (F_, F_), (T, F_)], cognitive="Understanding",
  flags="")

# ---------------------------------------------------------------- 030
def _c030():
    s = pts(x**2 + y**2 - 9, x + y - 1)
    P, Q = s
    return canon((x - P[x])*(x - Q[x]) + (y - P[y])*(y - Q[y]))
q("U10-C-030", TOP_DIA, "Circle on a chord as diameter", "Difficult", "Multi-step computation MCQ",
  r"The line $x + y = 1$ meets the circle $x^2 + y^2 = 9$ at $P$ and $Q$. The equation of the circle drawn on $PQ$ as a diameter is",
  r"$x^2 + y^2 - x - y - 8 = 0$",
  [(r"$2x^2 + 2y^2 - 2x - 2y - 67 = 0$", r"Uses centre $(\frac{1}{2}, \frac{1}{2})$ but takes the radius as the full chord, $r^2 = 34$: constant $\frac{1}{2} - 34$."),
   (r"$x^2 + y^2 + x + y - 8 = 0$", r"Writes the centre as $(-\frac{1}{2}, -\frac{1}{2})$."),
   (r"$2x^2 + 2y^2 - 2x - 2y - 17 = 0$", r"Writes $x^2 + y^2 - x - y = \frac{17}{2}$, forgetting the $\frac{1}{4} + \frac{1}{4}$ from expanding the squares.")],
  r"The centre of the required circle is the midpoint of $PQ$, the foot of the perpendicular from the origin to $x + y = 1$, which is $(\frac{1}{2}, \frac{1}{2})$. Its distance from the origin is $\frac{1}{\sqrt{2}}$, so the half chord is $\sqrt{9 - \frac{1}{2}} = \sqrt{\frac{17}{2}}$. Thus $(x - \frac{1}{2})^2 + (y - \frac{1}{2})^2 = \frac{17}{2}$, i.e. $x^2 + y^2 - x - y + \frac{1}{2} - \frac{17}{2} = 0$, which is $x^2 + y^2 - x - y - 8 = 0$.",
  r"Using the whole chord as the radius of the circle on it as diameter.",
  "U10-C-chord-as-diameter", "Avoiding the surd endpoints needs the midpoint and half chord route; three linked steps.",
  check=_c030, values=[(-1, -1, -8), (-1, -1, Rational(-67, 2)), (1, 1, -8), (-1, -1, Rational(-17, 2))], cognitive="Analysis")

# ---------------------------------------------------------------- 031
def _c031():
    return canon((x - 1)*(x - 5) + (y - 2)*(y + 4))
q("U10-C-031", TOP_DIA, "Smallest circle through two points", "Medium", "Multi-step computation MCQ",
  r"The equation of the circle of least radius passing through the points $(1, 2)$ and $(5, -4)$ is",
  r"$x^2 + y^2 - 6x + 2y - 3 = 0$",
  [(r"$x^2 + y^2 + 6x - 2y - 3 = 0$", r"Uses the diameter form with every endpoint sign reversed, giving centre $(-3, 1)$."),
   (r"$x^2 + y^2 - 6x + 2y - 42 = 0$", r"Uses centre $(3, -1)$ but radius equal to the full distance $\sqrt{52}$: $9 + 1 - 52 = -42$."),
   (r"$x^2 + y^2 - 6x + 2y + 13 = 0$", r"Expands $(y - 2)(y + 4)$ with constant $+8$, so the constant becomes $5 + 8 = 13$.")],
  r"Any circle through the two points has radius at least half the distance between them, with equality when the segment is a diameter. So the circle is $(x - 1)(x - 5) + (y - 2)(y + 4) = 0$, i.e. $x^2 - 6x + 5 + y^2 + 2y - 8 = 0$, which is $x^2 + y^2 - 6x + 2y - 3 = 0$.",
  r"Not recognising that the smallest circle has the segment as its diameter.",
  "U10-C-diameter-form", "Insight (segment is a diameter) plus the diameter form.",
  check=_c031, values=[(-6, 2, -3), (6, -2, -3), (-6, 2, -42), (-6, 2, 13)], cognitive="Analysis")

# ---------------------------------------------------------------- 032
def _c032():
    s = solve([x - y - 1, 2*x + y - 8], [x, y])
    hh, kk = s[x], s[y]
    return canon(eq_cr(hh, kk, (6 - hh)**2 + (6 - kk)**2))
q("U10-C-032", TOP_GEN, "Centre from two diameters", "Medium", "Multi-step computation MCQ",
  r"Two diameters of a circle lie along the lines $x - y = 1$ and $2x + y = 8$, and the circle passes through $(6, 6)$. Its equation is",
  r"$x^2 + y^2 - 6x - 4y - 12 = 0$",
  [(r"$x^2 + y^2 + 6x + 4y - 12 = 0$", r"Finds the centre $(3, 2)$ but writes $(x + 3)^2 + (y + 2)^2 = 25$."),
   (r"$x^2 + y^2 - 6x - 4y + 8 = 0$", r"Subtracts $r = 5$ instead of $r^2 = 25$: $9 + 4 - 5 = 8$."),
   (r"$x^2 + y^2 - 4x - 6y - 12 = 0$", r"Swaps the coordinates of the centre to $(2, 3)$; the radius through $(6, 6)$ is again $5$.")],
  r"The diameters meet at the centre: from $x - y = 1$ and $2x + y = 8$, $3x = 9$, so the centre is $(3, 2)$. The radius is the distance to $(6, 6)$, $\sqrt{9 + 16} = 5$. Hence $(x - 3)^2 + (y - 2)^2 = 25$, i.e. $x^2 + y^2 - 6x - 4y - 12 = 0$.",
  r"Not using that every diameter passes through the centre.",
  "U10-C-diameters-lines", "Intersection of lines, distance, expansion.",
  check=_c032, values=[(-6, -4, -12), (6, 4, -12), (-6, -4, 8), (-4, -6, -12)], cognitive="Application")

# ---------------------------------------------------------------- 033
def _c033():
    S = x**2 + y**2 - 6*x - 4*y - 12
    s1 = bool(S.subs({x: 6, y: -2}) < 0)
    s2 = len(solve([x**2 + y**2 - 8, y - x - 4], [x, y], dict=True)) == 1
    return (s1, s2)
q("U10-C-033", TOP_POS, "Position of a point; line meeting a circle centred at the origin", "Medium", "Statement-based MCQ",
  r"Let $S$ be the circle $x^2 + y^2 - 6x - 4y - 12 = 0$." "\n"
  r"Statement I: The point $(6, -2)$ lies inside $S$." "\n"
  r"Statement II: The line $y = x + 4$ meets the circle $x^2 + y^2 = 8$ at exactly one point." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Evaluates $-4y$ at $y = -2$ as $-8$, getting $36 + 4 - 36 - 8 - 12 = -16 < 0$, so takes the point as inside."),
   (ST_FF, r"Writes the distance of the origin from $x - y + 4 = 0$ as $\frac{4}{2} = 2$, omitting the square root, so $2 < 2\sqrt{2}$ and the line looks like a secant."),
   (ST_TF, r"Makes both slips: $-4y$ evaluated as $-8$ at $y = -2$, and the distance taken as $\frac{4}{2} = 2 < 2\sqrt{2}$.")],
  r"For Statement I, $S(6, -2) = 36 + 4 - 36 + 8 - 12 = 0$, so the point lies on $S$, not inside it; Statement I is false. For Statement II, substituting $y = x + 4$ gives $2x^2 + 8x + 8 = 0$, i.e. $(x + 2)^2 = 0$, a repeated root, so the line meets the circle only at $(-2, 2)$; equivalently its distance from the origin is $\frac{4}{\sqrt{2}} = 2\sqrt{2}$, the radius. Statement II is true.",
  r"Sign slips in evaluating $S(x_1, y_1)$ and omitting the square root in the distance formula.",
  "U10-C-stmt-position-tangency", "Two independent checks: power of a point and a repeated root on substitution.",
  check=_c033, values=[(F_, T), (T, T), (F_, F_), (T, F_)], cognitive="Understanding")

# ---------------------------------------------------------------- 034
def _c034():
    hh, kk, r = centre_r(x**2 + y**2 - 4*x - 8*y - 5)
    return FiniteSet(*solve(Eq(dist_pl((hh, kk), 3*x - 4*y - lam), r), lam))
q("U10-C-034", TOP_TOUCH, "Values of a parameter for which a line touches a circle", "Medium", "Inverse/parameter MCQ",
  r"The set of all values of $\lambda$ for which the line $3x - 4y = \lambda$ touches the circle $x^2 + y^2 - 4x - 8y - 5 = 0$ is",
  r"$\{15, -35\}$",
  [(r"$\{-15, 35\}$", r"Uses the centre $(-2, -4)$: $|{-6} + 16 - \lambda| = 25$."),
   (r"$\{-5, -15\}$", r"Forgets to divide by $\sqrt{3^2 + 4^2}$: $|{-10} - \lambda| = 5$."),
   (r"$\{115, -135\}$", r"Equates the distance to $r^2 = 25$ instead of $r = 5$: $|{-10} - \lambda| = 125$.")],
  r"The centre is $(2, 4)$ and $r = \sqrt{4 + 16 + 5} = 5$. Touching means $\frac{|6 - 16 - \lambda|}{5} = 5$, i.e. $|\lambda + 10| = 25$, so $\lambda = 15$ or $\lambda = -35$.",
  r"Equating the distance to $r^2$ or omitting the denominator.",
  "U10-C-touch-line-param", "Centre, radius, distance condition with an absolute value.",
  check=_c034, values=[FiniteSet(15, -35), FiniteSet(-15, 35), FiniteSet(-5, -15), FiniteSet(115, -135)],
  cognitive="Application")

# ---------------------------------------------------------------- 035
def _c035():
    mm = Symbol('mm', real=True)
    disc = discriminant(expand(x**2 + (mm*x + 2)**2 - 1), x)
    return solveset(disc > 0, mm, S.Reals)
q("U10-C-035", TOP_LINE, "Slopes for two points of intersection", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $m$ for which the line $y = mx + 2$ meets the circle $x^2 + y^2 = 1$ at two distinct points is",
  r"$(-\infty, -\sqrt{3}) \cup (\sqrt{3}, \infty)$",
  [(r"$(-\sqrt{3}, \sqrt{3})$", r"Reverses the inequality, giving the slopes for which the line misses the circle."),
   (r"$(-\infty, -1) \cup (1, \infty)$", r"Writes the condition as $|c| < 1 + m^2$ without squaring $c$: $2 < 1 + m^2$."),
   (r"$(-\infty, -3) \cup (3, \infty)$", r"Reaches $m^2 > 3$ and then writes $|m| > 3$.")],
  r"Substituting gives $(1 + m^2)x^2 + 4mx + 3 = 0$. Two distinct points need discriminant $16m^2 - 12(1 + m^2) > 0$, i.e. $m^2 > 3$, so $m < -\sqrt{3}$ or $m > \sqrt{3}$.",
  r"Reversing the inequality $c^2 < a^2(1 + m^2)$ for secants.",
  "U10-C-line-origin-circle-discriminant", "Substitution, discriminant, quadratic inequality.",
  check=_c035, values=[Union(Interval.open(-oo, -sqrt(3)), Interval.open(sqrt(3), oo)), Interval.open(-sqrt(3), sqrt(3)),
                       Union(Interval.open(-oo, -1), Interval.open(1, oo)), Union(Interval.open(-oo, -3), Interval.open(3, oo))],
  cognitive="Application")

# ---------------------------------------------------------------- 036
def _c036():
    d = dist_pl((1, 2), 3*x + 4*y + 4)
    return canon(eq_cr(1, 2, d**2 + 3**2))
q("U10-C-036", TOP_CHORD, "Circle from a chord of given length", "Medium", "Multi-step computation MCQ",
  r"A circle with centre $(1, 2)$ cuts off a chord of length $6$ on the line $3x + 4y + 4 = 0$. Its equation is",
  r"$x^2 + y^2 - 2x - 4y - 13 = 0$",
  [(r"$x^2 + y^2 - 2x - 4y - 40 = 0$", r"Uses the whole chord $6$ in Pythagoras: $r^2 = 9 + 36 = 45$."),
   (r"$x^2 + y^2 - 2x - 4y - 4 = 0$", r"Takes the radius equal to the half chord, $r^2 = 9$."),
   (r"$x^2 + y^2 + 2x + 4y - 13 = 0$", r"Finds $r^2 = 18$ but writes the circle with centre $(-1, -2)$.")],
  r"The distance of $(1, 2)$ from the line is $\frac{|3 + 8 + 4|}{5} = 3$. With half chord $3$, $r^2 = 3^2 + 3^2 = 18$. So $(x - 1)^2 + (y - 2)^2 = 18$, i.e. $x^2 + y^2 - 2x - 4y - 13 = 0$.",
  r"Using the full chord instead of the half chord in the right triangle.",
  "U10-C-chord-length-circle-eq", "Distance, Pythagoras with the half chord, expansion.",
  check=_c036, values=[(-2, -4, -13), (-2, -4, -40), (-2, -4, -4), (2, 4, -13)], cognitive="Application")

# ---------------------------------------------------------------- 037
def _c037():
    P = [(0, 0), (4, 0), (0, 3)]
    assert all(3*px + 4*py - 12 == 0 for px, py in P[1:])
    return canon((x - 4)*(x - 0) + (y - 0)*(y - 3))
q("U10-C-037", TOP_DIA, "Circumcircle of a right triangle", "Medium", "Multi-step computation MCQ",
  r"The circle passing through the vertices of the triangle formed by the coordinate axes and the line $3x + 4y = 12$ is",
  r"$x^2 + y^2 - 4x - 3y = 0$",
  [(r"$x^2 + y^2 - 8x - 6y = 0$", r"Takes the centre at $(4, 3)$, using the intercepts themselves rather than half of them."),
   (r"$x^2 + y^2 + 4x + 3y = 0$", r"Writes the centre as $(-2, -\frac{3}{2})$."),
   (r"$x^2 + y^2 - 3x - 4y = 0$", r"Interchanges the intercepts, taking the vertices as $(3, 0)$ and $(0, 4)$, so the diameter form gives $(x - 3)x + y(y - 4) = 0$.")],
  r"The vertices are $(0, 0)$, $(4, 0)$, $(0, 3)$, and the angle at the origin is a right angle, so the hypotenuse joining $(4, 0)$ and $(0, 3)$ is a diameter. The diameter form gives $(x - 4)x + y(y - 3) = 0$, i.e. $x^2 + y^2 - 4x - 3y = 0$.",
  r"Not using that the hypotenuse of a right triangle is a diameter of its circumcircle.",
  "U10-C-right-triangle-circumcircle", "Right angle insight plus the diameter form.",
  check=_c037, values=[(-4, -3, 0), (-8, -6, 0), (4, 3, 0), (-3, -4, 0)], cognitive="Application")

# ---------------------------------------------------------------- 038
def _c038():
    s = pts(x**2 + y**2 - 20, x - 2*y)  # line through centre perpendicular to 2x + y = 15
    best = min(s, key=lambda d: dist_pl((d[x], d[y]), 2*x + y - 15))
    return (best[x], best[y])
q("U10-C-038", TOP_LINE, "Point of a circle nearest to a line", "Medium", "Multi-step computation MCQ",
  r"The point on the circle $x^2 + y^2 = 20$ that is nearest to the line $2x + y = 15$ is",
  r"$(4, 2)$",
  [(r"$(2, 4)$", r"Moves along the direction $(1, 2)$ instead of the normal direction $(2, 1)$."),
   (r"$(-4, -2)$", r"Takes the other end of the diameter, which is the farthest point."),
   (r"$(2, -4)$", r"Moves from the centre along the line's own direction $(1, -2)$ instead of its normal $(2, 1)$, so $5t^2 = 20$ gives $(2, -4)$.")],
  r"The nearest point lies on the perpendicular from the centre to the line, i.e. on $x = 2t$, $y = t$. On the circle $5t^2 = 20$, so $t = \pm 2$; the point on the side of the line is $t = 2$, giving $(4, 2)$.",
  r"Moving along the wrong direction from the centre, or taking the farther end of the diameter.",
  "U10-C-nearest-point", "Normal direction, intersection with the circle, choose the correct end.",
  check=_c038, values=[(4, 2), (2, 4), (-4, -2), (2, -4)], cognitive="Analysis")

# ---------------------------------------------------------------- 039
def _c039():
    total = 0
    for c in (10 + 15, 10 - 15):
        total += len(solve([x**2 + y**2 - 25, 3*x + 4*y - c], [x, y], dict=True))
    return total
q("U10-C-039", TOP_LINE, "Points of a circle at a given distance from a line", "Difficult", "Multi-step computation MCQ",
  r"The number of points on the circle $x^2 + y^2 = 25$ whose perpendicular distance from the line $3x + 4y = 10$ is $3$ is",
  r"$3$",
  [(r"$4$", r"Assumes both parallel lines at distance $3$ cut the circle at two points each, without checking that one is a tangent."),
   (r"$2$", r"Considers only the parallel line $3x + 4y = -5$ on the side of the origin."),
   (r"$1$", r"Considers only the parallel line $3x + 4y = 25$ on the far side, which touches the circle.")],
  r"Such points lie on the lines $3x + 4y = 10 \pm 15$, i.e. $3x + 4y = 25$ and $3x + 4y = -5$. Their distances from the origin are $5$ and $1$. The first equals the radius, so it touches the circle at one point; the second is less than $5$, so it meets the circle at two points. The total is $3$.",
  r"Forgetting the parallel line on the other side, or not checking for tangency.",
  "U10-C-points-at-distance", "Two parallel lines, each compared with the radius; tangency trap.",
  check=_c039, values=[3, 4, 2, 1],
  numerical=dict(question=r"The number of points on the circle $x^2 + y^2 = 25$ whose perpendicular distance from the line $3x + 4y = 10$ is $3$ is", answer=3),
  cognitive="Analysis")

# ---------------------------------------------------------------- 040
def _c040():
    c = Symbol('c', real=True)
    sets = []
    for sh in (5, -5):  # lines 4x - 3y = c + 5 and 4x - 3y = c - 5 are at distance 1 from 4x - 3y = c
        d = Abs(c + sh) / 5
        sets.append((solveset(d < 4, c, S.Reals), solveset(Eq(d, 4), c, S.Reals), solveset(d > 4, c, S.Reals)))
    (A2, A1, A0), (B2, B1, B0) = sets
    return Union(Intersection(A2, B0), Intersection(A0, B2), Intersection(A1, B1))
q("U10-C-040", TOP_LINE, "Parameter for exactly two points at a given distance from a line", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $c$ for which exactly two points of the circle $x^2 + y^2 = 16$ are at a perpendicular distance $1$ from the line $4x - 3y = c$ is",
  r"$(-25, -15) \cup (15, 25)$",
  [(r"$[-25, -15) \cup (15, 25]$", r"Counts the single point of contact of a tangent line as two points, so $c = \pm 25$ (one line touching, the other missing) is wrongly included."),
   (r"$(-15, 25)$", r"Considers only the parallel line $4x - 3y = c - 5$ and requires it to cut the circle, $|c - 5| < 20$, forgetting the line on the other side."),
   (r"$(-21, -19) \cup (19, 21)$", r"Takes the parallel lines at distance $1$ as $4x - 3y = c \pm 1$, forgetting the factor $\sqrt{4^2 + 3^2} = 5$.")],
  r"The required points lie on $4x - 3y = c + 5$ and $4x - 3y = c - 5$, whose distances from the origin are $\frac{|c + 5|}{5}$ and $\frac{|c - 5|}{5}$; each line gives $2$, $1$ or $0$ points as this distance is less than, equal to or greater than $4$. Exactly two points occur when one line cuts the circle and the other misses it: $|c + 5| < 20$ with $|c - 5| > 20$ gives $-25 < c < -15$, and $|c - 5| < 20$ with $|c + 5| > 20$ gives $15 < c < 25$. Both lines cannot be tangents together, and at $c = \pm 15$ one line touches while the other cuts ($3$ points), at $c = \pm 25$ one touches while the other misses ($1$ point). Hence $c \in (-25, -15) \cup (15, 25)$.",
  r"Forgetting one of the two parallel lines, or mishandling the tangent endpoints.",
  "U10-C-exactly-two-points-param", "Two parallel lines, each compared with the radius, casework with tangent endpoints excluded.",
  check=_c040, values=[Union(Interval.open(-25, -15), Interval.open(15, 25)),
                       Union(Interval.Ropen(-25, -15), Interval.Lopen(15, 25)),
                       Interval.open(-15, 25),
                       Union(Interval.open(-21, -19), Interval.open(19, 21))], cognitive="Analysis")

# ---------------------------------------------------------------- 041
def _c041():
    A = solveset(a_**2 + 1 - 10 < 0, a_, S.Reals)
    B = solveset(a_**2 + 1 - 4*a_ > 0, a_, S.Reals)
    return Intersection(A, B)
q("U10-C-041", TOP_POS, "Point inside one circle and outside another", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $a$ for which the point $(a, 1)$ lies inside the circle $x^2 + y^2 = 10$ and outside the circle $x^2 + y^2 - 4x = 0$ is",
  r"$(-3, 2 - \sqrt{3})$",
  [(r"$(2 - \sqrt{3}, 3)$", r"Uses $a^2 - 4a + 1 < 0$ (inside) for the second circle, then intersects with $(-3, 3)$."),
   (r"$(-3, 3)$", r"Uses only the first condition."),
   (r"$(-\infty, 2 - \sqrt{3})$", r"Solves $a^2 < 9$ as $a < 3$ only, then intersects $(-\infty, 3)$ with $(-\infty, 2 - \sqrt{3}) \cup (2 + \sqrt{3}, \infty)$.")],
  r"Inside the first circle: $a^2 + 1 < 10$, so $-3 < a < 3$. Outside the second: $a^2 + 1 - 4a > 0$, so $a < 2 - \sqrt{3}$ or $a > 2 + \sqrt{3}$. Since $2 + \sqrt{3} > 3$, the second branch contributes nothing, and the answer is $-3 < a < 2 - \sqrt{3}$.",
  r"Not intersecting the two conditions, or missing that $2 + \sqrt{3} > 3$.",
  "U10-C-position-point", "Two quadratic inequalities, a comparison of surds, and an intersection.",
  check=_c041, values=[Interval.open(-3, 2 - sqrt(3)), Interval.open(2 - sqrt(3), 3), Interval.open(-3, 3),
                       Interval.open(-oo, 2 - sqrt(3))], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c042():
    s = pts(x**2 + y**2 - 4, y - x - 1)
    P, Q = s
    dot = P[x]*Q[x] + P[y]*Q[y]
    return simplify(dot / 4)
q("U10-C-042", TOP_LINE, "Angle subtended at the centre by a chord", "Difficult", "Multi-step computation MCQ",
  r"The line $y = x + 1$ meets the circle $x^2 + y^2 = 4$ at $P$ and $Q$, and $O$ is the origin. Then $\cos \angle POQ$ equals",
  r"$-\frac{3}{4}$",
  [(r"$\frac{3}{4}$", r"Uses $\cos \angle POQ = 1 - 2\cos^2 \frac{\angle POQ}{2}$, reversing the double angle formula."),
   (r"$\frac{\sqrt{2}}{4}$", r"Stops at $\cos \frac{\angle POQ}{2} = \frac{d}{r} = \frac{1/\sqrt{2}}{2}$."),
   (r"$-\frac{1}{2}$", r"Takes $y_1 y_2 = x_1 x_2 + 1$, dropping $x_1 + x_2$, so $\overrightarrow{OP} \cdot \overrightarrow{OQ} = -2$.")],
  r"Substituting, $2x^2 + 2x - 3 = 0$, so $x_1 + x_2 = -1$ and $x_1 x_2 = -\frac{3}{2}$. Then $y_1 y_2 = x_1 x_2 + (x_1 + x_2) + 1 = -\frac{3}{2}$, so $\overrightarrow{OP} \cdot \overrightarrow{OQ} = -3$. Since $OP = OQ = 2$, $\cos \angle POQ = \frac{-3}{4}$.",
  r"Stopping at the half angle, or dropping a term in $y_1 y_2$.",
  "U10-C-chord-angle-origin", "Sum and product of roots combined with the dot product; obtuse angle trap.",
  check=_c042, values=[Rational(-3, 4), Rational(3, 4), sqrt(2)/4, Rational(-1, 2)], cognitive="Analysis")

# ---------------------------------------------------------------- 043
def _c043():
    c = Symbol('c', positive=True)
    P, Q = pts(x**2 + y**2 - 16, sqrt(3)*x + y - c)
    cosang = simplify((P[x]*Q[x] + P[y]*Q[y]) / 16)
    return solve(Eq(cosang, -Rational(1, 2)), c)[0]
q("U10-C-043", TOP_LINE, "Chord subtending a given angle at the centre", "Difficult", "Inverse/parameter MCQ",
  r"The line $\sqrt{3}x + y = c$, $c > 0$, meets the circle $x^2 + y^2 = 16$ at $P$ and $Q$ such that $\angle POQ = 120^\circ$, where $O$ is the origin. Then $c$ equals",
  r"$4$",
  [(r"$4\sqrt{3}$", r"Takes the distance from the centre as $r \sin 60^\circ = 2\sqrt{3}$ (the half chord) instead of $r \cos 60^\circ$."),
   (r"$2$", r"Gets the distance $2$ correctly but sets $c = 2$, forgetting to divide by $\sqrt{3 + 1} = 2$."),
   (r"$2\sqrt{3}$", r"Takes the distance as $r\sin 60^\circ$ and also forgets to divide by $\sqrt{3 + 1}$.")],
  r"In the isosceles triangle $OPQ$ the perpendicular from $O$ bisects $\angle POQ$, so the distance of $O$ from the line is $4\cos 60^\circ = 2$. The distance is also $\frac{c}{\sqrt{3 + 1}} = \frac{c}{2}$, so $c = 4$.",
  r"Using sine in place of cosine for the distance of the chord from the centre.",
  "U10-C-chord-angle-origin", "Geometry of the isosceles triangle plus the distance formula, solved backwards.",
  check=_c043, values=[4, 4*sqrt(3), 2, 2*sqrt(3)],
  numerical=dict(question=r"The line $\sqrt{3}x + y = c$, $c > 0$, meets the circle $x^2 + y^2 = 16$ at $P$ and $Q$ such that $\angle POQ = 120^\circ$, where $O$ is the origin. The value of $c$ is", answer=4),
  cognitive="Analysis")

# ---------------------------------------------------------------- 044
def _c044():
    mm = Symbol('mm', positive=True)
    P, Q = pts(x**2 + y**2 - 16, y - mm*x - 4)
    area = simplify(Abs(P[x]*Q[y] - Q[x]*P[y]) / 2)
    crit = solve(diff(area, mm), mm)
    best = max(crit, key=lambda v: area.subs(mm, v))
    return best
q("U10-C-044", TOP_LINE, "Maximum area of the triangle formed with the centre", "Difficult", "Inverse/parameter MCQ",
  r"The line $y = mx + 4$, $m > 0$, meets the circle $x^2 + y^2 = 16$ at $P$ and $Q$, and $O$ is the origin. The area of triangle $OPQ$ is greatest when $m$ equals",
  r"$1$",
  [(r"$\sqrt{3}$", r"Takes the best distance of the chord from the centre as $\frac{r}{2} = 2$, so $\frac{16}{1 + m^2} = 4$."),
   (r"$\frac{1}{\sqrt{3}}$", r"Assumes the triangle should be equilateral, with distance $\frac{\sqrt{3}}{2} r = 2\sqrt{3}$, so $\frac{16}{1 + m^2} = 12$."),
   (r"$\sqrt{7}$", r"Halves the optimal distance $\frac{r}{\sqrt{2}}$ again, taking it as $\sqrt{2}$, so $\frac{16}{1 + m^2} = 2$.")],
  r"The area is $\frac{1}{2} \cdot OP \cdot OQ \sin \angle POQ = 8 \sin \angle POQ$, greatest when $\angle POQ = 90^\circ$. Then the distance of $O$ from the line is $\frac{4}{\sqrt{2}} = 2\sqrt{2}$, so $\frac{4}{\sqrt{1 + m^2}} = 2\sqrt{2}$, giving $1 + m^2 = 2$ and $m = 1$.",
  r"Assuming the equilateral triangle has the largest area.",
  "U10-C-max-area-chord", "Area as a function of the angle, then the distance condition solved for $m$.",
  check=_c044, values=[1, sqrt(3), 1/sqrt(3), sqrt(7)],
  numerical=dict(question=r"The line $y = mx + 4$, $m > 0$, meets the circle $x^2 + y^2 = 16$ at $P$ and $Q$, and $O$ is the origin. If the area of triangle $OPQ$ is the greatest possible, then the value of $m$ is", answer=1),
  cognitive="Analysis")

# ---------------------------------------------------------------- 045
def _c045():
    P, Q = pts(x**2 + y**2 - 25, x - y - 1)
    D, E, F0 = symbols('D E F0')
    eqs = [px**2 + py**2 + D*px + E*py + F0 for px, py in ((0, 0), (P[x], P[y]), (Q[x], Q[y]))]
    s = solve(eqs, [D, E, F0], dict=True)[0]
    return canon(x**2 + y**2 + s[D]*x + s[E]*y + s[F0])
q("U10-C-045", TOP_PTS, "Circle through the origin and the points where a line meets a circle", "Difficult", "Multi-step computation MCQ",
  r"The line $x - y = 1$ meets the circle $x^2 + y^2 = 25$ at $P$ and $Q$. The equation of the circle passing through $P$, $Q$ and the origin is",
  r"$x^2 + y^2 - 25x + 25y = 0$",
  [(r"$x^2 + y^2 - x + y - 24 = 0$", r"Assumes $PQ$ is a diameter of the required circle and uses the diameter form $(x - 4)(x + 3) + (y - 3)(y + 4) = 0$; but $\overrightarrow{OP} \cdot \overrightarrow{OQ} = -24 \ne 0$."),
   (r"$x^2 + y^2 + 25x - 25y = 0$", r"Finds the centre $(\frac{25}{2}, -\frac{25}{2})$ but writes the equation with centre $(-\frac{25}{2}, \frac{25}{2})$."),
   (r"$x^2 + y^2 - 25x + 21y = 0$", r"Factorises $y^2 + y - 12 = 0$ as $(y + 3)(y - 4) = 0$, taking the points $(-2, -3)$ and $(5, 4)$.")],
  r"Substituting $x = y + 1$: $(y + 1)^2 + y^2 = 25$, so $y^2 + y - 12 = 0$, $y = 3$ or $-4$, giving $P(4, 3)$ and $Q(-3, -4)$. A circle through the origin is $x^2 + y^2 + Dx + Ey = 0$. Then $25 + 4D + 3E = 0$ and $25 - 3D - 4E = 0$; adding gives $D - E = -50$ and subtracting gives $D + E = 0$, so $D = -25$, $E = 25$. The circle is $x^2 + y^2 - 25x + 25y = 0$.",
  r"Treating the chord $PQ$ as a diameter without checking for a right angle at the origin.",
  "U10-C-circle-through-intersections", "Intersection quadratic, then a circle through three points; a tempting diameter shortcut that fails.",
  check=_c045, values=[(-25, 25, 0), (-1, 1, -24), (25, -25, 0), (-25, 21, 0)], cognitive="Analysis")

# ---------------------------------------------------------------- 046
def _c046():
    p, qq = symbols('p q', real=True)
    s = solve([Eq((p - 1)**2 + (qq - 2)**2, qq**2), Eq((p - 3)**2 + (qq - 4)**2, qq**2)], [p, qq], dict=True)
    assert len(s) == 2
    A, B = s
    return sqrt((A[p] - B[p])**2 + (A[qq] - B[qq])**2)
q("U10-C-046", TOP_TOUCH, "Two circles touching the x-axis through two points", "Difficult", "Multi-step computation MCQ",
  r"Two distinct circles pass through the points $(1, 2)$ and $(3, 4)$ and touch the $x$-axis. The distance between their centres is",
  r"$8\sqrt{2}$",
  [(r"$8$", r"Solves $h^2 + 2h - 15 = 0$ as $h = -3, 5$, giving centres $(-3, 5)$ and $(5, 5)$."),
   (r"$12$", r"Adds the radii $2 + 10$, as if the circles touched each other."),
   (r"$2\sqrt{17}$", r"Writes the second centre as $(5, 10)$, losing the sign of $h = -5$; the distance from $(3, 2)$ is then $\sqrt{4 + 64}$.")],
  r"Let the centre be $(h, k)$ with $k > 0$ and radius $k$. From the two points, $(h - 1)^2 + (k - 2)^2 = k^2$ and $(h - 3)^2 + (k - 4)^2 = k^2$, i.e. $4k = h^2 - 2h + 5$ and $8k = h^2 - 6h + 25$. Eliminating $k$: $h^2 + 2h - 15 = 0$, so $h = 3$ or $h = -5$, giving centres $(3, 2)$ and $(-5, 10)$. Their distance is $\sqrt{64 + 64} = 8\sqrt{2}$.",
  r"Sign slips in factorising, and misreading the configuration as touching circles.",
  "U10-C-touch-axis-two-points", "Two simultaneous conditions eliminated to a quadratic; two circles to handle.",
  check=_c046, values=[8*sqrt(2), 8, 12, 2*sqrt(17)], cognitive="Analysis")

# ---------------------------------------------------------------- 047
def _c047():
    e = x**2 + y**2 - 2*x - 4*y - 4
    cnt = 0
    for X in range(-10, 11):
        for Y in range(-10, 11):
            if e.subs({x: X, y: Y}) < 0:
                cnt += 1
    return cnt
q("U10-C-047", TOP_POS, "Lattice points inside a circle", "Difficult", "Multi-step computation MCQ",
  r"The number of points with integer coordinates lying strictly inside the circle $x^2 + y^2 - 2x - 4y - 4 = 0$ is",
  r"$25$",
  [(r"$29$", r"Also counts the four lattice points on the circle, $(1 \pm 3, 2)$ and $(1, 2 \pm 3)$."),
   (r"$36$", r"Counts the $9$ points with $0 \le X, Y \le 2$ (relative to the centre) and multiplies by $4$, counting points on the lines through the centre more than once."),
   (r"$49$", r"Counts every lattice point in the square $|X| \le 3$, $|Y| \le 3$ around the centre.")],
  r"The circle is $(x - 1)^2 + (y - 2)^2 = 9$. With $X = x - 1$, $Y = y - 2$ (integers), we need $X^2 + Y^2 < 9$. For $X = 0, \pm 1, \pm 2$, $Y^2 < 9, 8, 5$, so $Y \in \{-2, \dots, 2\}$ in each case ($5$ values); $X = \pm 3$ gives none. Total $5 \times 5 = 25$.",
  r"Including boundary points or double counting points on the axes through the centre.",
  "U10-C-lattice-points", "Shift to the centre, casework on $X$, careful boundary handling.",
  check=_c047, values=[25, 29, 36, 49],
  numerical=dict(question=r"The number of points with integer coordinates lying strictly inside the circle $x^2 + y^2 - 2x - 4y - 4 = 0$ is", answer=25),
  cognitive="Analysis")

# ---------------------------------------------------------------- 048
def _c048():
    g, f, c = symbols('g f c')
    P = [(2, 0), (0, 1), (4, 5)]
    s = solve([px**2 + py**2 + 2*g*px + 2*f*py + c for px, py in P], [g, f, c])
    ys = solve(y**2 + 2*s[f]*y + s[c], y)
    other = [v for v in ys if v != 1]
    assert len(other) == 1
    return other[0]
q("U10-C-048", TOP_PTS, "Concyclic points", "Difficult", "Inverse/parameter MCQ",
  r"The points $(2, 0)$, $(0, 1)$, $(4, 5)$ and $(0, k)$, where $k \ne 1$, lie on a circle. Then $k$ equals",
  r"$\frac{14}{3}$",
  [(r"$\frac{17}{3}$", r"Takes the sum of the roots of $3y^2 - 17y + 14 = 0$ instead of the second root."),
   (r"$\frac{7}{3}$", r"Finds the second intercept on the $x$-axis, from $3x^2 - 13x + 14 = 0$, instead of the $y$-axis."),
   (r"$-\frac{14}{3}$", r"Takes the product of the $y$-intercepts as $-c$, so $1 \cdot k = -\frac{14}{3}$.")],
  r"Let the circle be $x^2 + y^2 + 2gx + 2fy + c = 0$. The three points give $4 + 4g + c = 0$, $1 + 2f + c = 0$, $41 + 8g + 10f + c = 0$, whence $g = -\frac{13}{6}$, $f = -\frac{17}{6}$, $c = \frac{14}{3}$. On the $y$-axis, $y^2 - \frac{17}{3}y + \frac{14}{3} = 0$, i.e. $3y^2 - 17y + 14 = 0$, with roots $1$ and $\frac{14}{3}$. So $k = \frac{14}{3}$.",
  r"Using the sum instead of the product of the $y$-intercepts.",
  "U10-C-concyclic", r"Solve a $3 \times 3$ system, then use the intercept quadratic with one known root.",
  check=_c048, values=[Rational(14, 3), Rational(17, 3), Rational(7, 3), Rational(-14, 3)], cognitive="Analysis")

# ---------------------------------------------------------------- 049
def _c049():
    hh, kk, r = centre_r(x**2 + y**2 - 4*x + 6*y - 3)
    side = sqrt(2) * r  # diagonal of the inscribed square is the diameter 2r
    return simplify(side**2)
q("U10-C-049", TOP_GEN, "Square inscribed in a circle", "Medium", "Multi-step computation MCQ",
  r"A square is inscribed in the circle $x^2 + y^2 - 4x + 6y - 3 = 0$. The area of the square is",
  r"$32$",
  [(r"$64$", r"Takes the side of the square equal to the diameter $8$, which is the circumscribed square."),
   (r"$16$", r"Takes the side of the square equal to the radius $4$."),
   (r"$20$", r"Finds $r^2 = 4 + 9 - 3 = 10$ with the wrong sign of the constant, then uses area $= 2r^2$.")],
  r"The centre is $(2, -3)$ and $r = \sqrt{4 + 9 + 3} = 4$. The diagonal of an inscribed square is a diameter, so the diagonal is $8$ and the area is $\frac{8^2}{2} = 32$.",
  r"Confusing the inscribed square with the circumscribed one.",
  "U10-C-inscribed-square", "Radius from the general form, then the diagonal equals the diameter.",
  check=_c049, values=[32, 64, 16, 20],
  numerical=dict(question=r"A square is inscribed in the circle $x^2 + y^2 - 4x + 6y - 3 = 0$. The area of the square is", answer=32),
  cognitive="Application")

# ---------------------------------------------------------------- 050
def _c050():
    e = x**2 + y**2 - 4*x - 6*y - 12
    assert e.subs({x: 4, y: 1}) < 0
    hh, kk, r = centre_r(e)
    d2 = (4 - hh)**2 + (1 - kk)**2
    # verify minimum over all lines through (4, 1) by brute force on the slope parameter
    th = Symbol('th', real=True)
    dist2 = ((hh - 4)*sin(th) - (kk - 1)*cos(th))**2  # squared distance from centre to line through (4,1) with direction (cos, sin)
    maxd2 = maximum(dist2, th, Interval(0, pi))
    assert simplify(maxd2 - d2) == 0
    return 2*sqrt(r**2 - d2)
q("U10-C-050", TOP_CHORD, "Shortest chord through an interior point", "Difficult", "Multi-step computation MCQ",
  r"The length of the shortest chord of the circle $x^2 + y^2 - 4x - 6y - 12 = 0$ that passes through the point $(4, 1)$ is",
  r"$2\sqrt{17}$",
  [(r"$10$", r"Gives the diameter, which is the longest chord through the point."),
   (r"$\sqrt{17}$", r"Stops at the half chord $\sqrt{25 - 8}$."),
   (r"$2\sqrt{33}$", r"Adds instead of subtracting: $2\sqrt{25 + 8}$.")],
  r"The centre is $C(2, 3)$ and $r = \sqrt{4 + 9 + 12} = 5$; the point $P(4, 1)$ is inside since $16 + 1 - 16 - 6 - 12 = -17 < 0$. A chord through $P$ is shortest when its distance from $C$ is greatest, i.e. when it is perpendicular to $CP$, with distance $CP = \sqrt{4 + 4} = 2\sqrt{2}$. Its length is $2\sqrt{25 - 8} = 2\sqrt{17}$.",
  r"Thinking the shortest chord is the one through the centre, or not doubling the half chord.",
  "U10-C-shortest-chord", "Requires the extremal insight (chord perpendicular to $CP$) before computing.",
  check=_c050, values=[2*sqrt(17), 10, sqrt(17), 2*sqrt(33)], cognitive="Analysis")
