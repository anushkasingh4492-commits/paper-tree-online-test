import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools

X, Y = symbols('x y', real=True)
K_ = Symbol('k', real=True)
C_ = Symbol('c', real=True)
E_ = Symbol('e', positive=True)
A_ = Symbol('a', positive=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TOP_STD = "Ellipse: standard form"
TOP_EQN = "Ellipse: equation from data"
TOP_FOC = "Ellipse: focal distances"
TOP_INT = "Ellipse: intersection with lines"
TOP_PTS = "Ellipse: points on the ellipse"
TOP_ECC = "Ellipse: eccentricity from conditions"


def _ln(a, b, c):
    """Line a x + b y + c = 0 as a normalised coefficient tuple."""
    a, b, c = sympify(a), sympify(b), sympify(c)
    lead = a if a != 0 else b
    return tuple(simplify(v / lead) for v in (a, b, c))


def _key(expr):
    """Canonical coefficient tuple of a second-degree curve expr = 0."""
    p = Poly(expand(expr), X, Y)
    mons = [X**2, X*Y, Y**2, X, Y, Integer(1)]
    cs = [p.coeff_monomial(mm) for mm in mons]
    lead = [c for c in cs if c != 0][0]
    return tuple(simplify(c / lead) for c in cs)


def _AB(expr):
    """Denominators (A, B) of x^2/A + y^2/B = 1 from expr = 0 of the form p x^2 + q y^2 - r."""
    p = Poly(expand(expr), X, Y)
    r = -p.coeff_monomial(Integer(1))
    return (r / p.coeff_monomial(X**2), r / p.coeff_monomial(Y**2))


def _ell(A, B):
    """Data of x^2/A + y^2/B = 1 (A, B > 0, A != B)."""
    A, B = sympify(A), sympify(B)
    if A > B:
        a, b = sqrt(A), sqrt(B)
        c = sqrt(A - B)
        e = c / a
        foci = FiniteSet(Tuple(c, 0), Tuple(-c, 0))
        dirs = FiniteSet(Tuple(*_ln(1, 0, -a / e)), Tuple(*_ln(1, 0, a / e)))
        ax = 'x'
    else:
        a, b = sqrt(B), sqrt(A)
        c = sqrt(B - A)
        e = c / a
        foci = FiniteSet(Tuple(0, c), Tuple(0, -c))
        dirs = FiniteSet(Tuple(*_ln(0, 1, -a / e)), Tuple(*_ln(0, 1, a / e)))
        ax = 'y'
    return dict(a=a, b=b, c=c, e=simplify(e), foci=foci, dirs=dirs, lr=simplify(2 * b**2 / a), axis=ax)


def _dist(P, Q):
    return sqrt((P[0] - Q[0])**2 + (P[1] - Q[1])**2)


def _meet(curve, line):
    sols = solve([curve, line], [X, Y], dict=True)
    return [(s[X], s[Y]) for s in sols if s[X].is_real and s[Y].is_real]


def _pair(p1, p2):
    return FiniteSet(Tuple(*p1), Tuple(*p2))


# ================================================================ EASY
# ---------------------------------------------------------------- 001
q("U10-E-001", TOP_STD, "Eccentricity when the major axis is vertical", "Easy", "Single-step computation MCQ",
  r"The eccentricity of the ellipse $\frac{x^2}{40} + \frac{y^2}{49} = 1$ is",
  r"$\frac{3}{7}$",
  [(r"$\frac{2\sqrt{10}}{7}$", r"Gives $\frac{b}{a} = \frac{\sqrt{40}}{7} = \frac{2\sqrt{10}}{7}$, the ratio of the semi-axes."),
   (r"$\frac{3\sqrt{10}}{20}$", r"Finds $c = 3$ but divides by the semi-minor axis: $\frac{c}{b} = \frac{3}{\sqrt{40}} = \frac{3\sqrt{10}}{20}$."),
   (r"$\frac{9}{49}$", r"Stops at $e^2 = 1 - \frac{40}{49} = \frac{9}{49}$ and does not take the square root.")],
  r"The larger denominator $49$ is under $y^2$, so the major axis is along the $y$-axis with $a^2 = 49$, $b^2 = 40$. Then $e^2 = 1 - \frac{b^2}{a^2} = 1 - \frac{40}{49} = \frac{9}{49}$ and $e = \frac{3}{7}$.",
  r"Using $\frac{b}{a}$ or $\frac{c}{b}$ for the eccentricity, or forgetting the square root in $e^2 = 1 - \frac{b^2}{a^2}$.",
  "U10-E-ecc-vertical", "One orientation check and one formula applied once.",
  check=lambda: _ell(40, 49)["e"], values=[Rational(3, 7), 2*sqrt(10)/7, 3*sqrt(10)/20, Rational(9, 49)],
  cognitive="Recall")

# ---------------------------------------------------------------- 002
def _c002():
    A, B = _AB(9*X**2 + 4*Y**2 - 36)
    return _ell(A, B)["foci"]
q("U10-E-002", TOP_STD, "Foci when the major axis is vertical", "Easy", "Single-step computation MCQ",
  r"The foci of the ellipse $9x^2 + 4y^2 = 36$ are",
  r"$(0, \pm\sqrt{5})$",
  [(r"$(\pm\sqrt{5}, 0)$", r"Finds $c = \sqrt{9 - 4} = \sqrt{5}$ but puts the foci on the $x$-axis, not noticing that the larger denominator is under $y^2$."),
   (r"$(0, \pm\sqrt{13})$", r"Uses $c^2 = a^2 + b^2 = 9 + 4$."),
   (r"$(0, \pm\sqrt{65})$", r"Uses the coefficients $9$ and $4$ of the given equation as $a$ and $b$ in $c^2 = a^2 - b^2$: $81 - 16 = 65$.")],
  r"Dividing by $36$: $\frac{x^2}{4} + \frac{y^2}{9} = 1$. The larger denominator is under $y^2$, so the major axis lies along the $y$-axis with $a^2 = 9$, $b^2 = 4$. Then $c^2 = a^2 - b^2 = 5$ and the foci are $(0, \pm\sqrt{5})$.",
  r"Placing the foci on the $x$-axis by habit, without checking which denominator is larger.",
  "U10-E-foci-vertical", "One reduction to standard form and one orientation decision.",
  check=_c002,
  values=[FiniteSet(Tuple(0, sqrt(5)), Tuple(0, -sqrt(5))), FiniteSet(Tuple(sqrt(5), 0), Tuple(-sqrt(5), 0)),
          FiniteSet(Tuple(0, sqrt(13)), Tuple(0, -sqrt(13))), FiniteSet(Tuple(0, sqrt(65)), Tuple(0, -sqrt(65)))],
  cognitive="Application")

# ---------------------------------------------------------------- 003
q("U10-E-003", TOP_STD, "Length of the latus rectum", "Easy", "Single-step computation MCQ",
  r"The length of the latus rectum of the ellipse $\frac{x^2}{16} + \frac{y^2}{9} = 1$ is",
  r"$\frac{9}{2}$",
  [(r"$\frac{9}{4}$", r"Gives the semi-latus rectum $\frac{b^2}{a} = \frac{9}{4}$."),
   (r"$\frac{32}{3}$", r"Uses $\frac{2a^2}{b} = \frac{32}{3}$, swapping the roles of $a$ and $b$."),
   (r"$\frac{3}{2}$", r"Uses $\frac{2b}{a} = \frac{6}{4}$, forgetting to square $b$.")],
  r"Here $a = 4$, $b = 3$ with the major axis along the $x$-axis. The latus rectum has length $\frac{2b^2}{a} = \frac{2 \cdot 9}{4} = \frac{9}{2}$.",
  r"Using $\frac{b^2}{a}$ (half the latus rectum) or swapping $a$ and $b$ in $\frac{2b^2}{a}$.",
  "U10-E-lr-direct", "One formula applied once.",
  check=lambda: _ell(16, 9)["lr"], values=[Rational(9, 2), Rational(9, 4), Rational(32, 3), Rational(3, 2)],
  cognitive="Recall")

# ---------------------------------------------------------------- 004
q("U10-E-004", TOP_STD, "Equations of the directrices", "Easy", "Single-step computation MCQ",
  r"The directrices of the ellipse $\frac{x^2}{36} + \frac{y^2}{20} = 1$ are",
  r"$x = \pm 9$",
  [(r"$x = \pm 4$", r"Gives $x = \pm ae = \pm 4$, the lines through the foci."),
   (r"$x = \pm 6$", r"Gives $x = \pm a$, the tangents at the vertices."),
   (r"$y = \pm 9$", r"Computes $\frac{a}{e} = 9$ correctly but treats the major axis as vertical, writing the directrices as $y = \pm 9$.")],
  r"Here $a^2 = 36$, $b^2 = 20$, so $c^2 = 16$, $c = 4$ and $e = \frac{4}{6} = \frac{2}{3}$. The directrices are $x = \pm\frac{a}{e} = \pm\frac{6}{2/3} = \pm 9$.",
  r"Confusing the directrices $x = \pm\frac{a}{e}$ with the lines $x = \pm ae$ through the foci.",
  "U10-E-directrix-direct", "Find $e$, then one formula.",
  check=lambda: _ell(36, 20)["dirs"],
  values=[FiniteSet(*[Tuple(*_ln(1, 0, v)) for v in (-9, 9)]), FiniteSet(*[Tuple(*_ln(1, 0, v)) for v in (-4, 4)]),
          FiniteSet(*[Tuple(*_ln(1, 0, v)) for v in (-6, 6)]), FiniteSet(*[Tuple(*_ln(0, 1, v)) for v in (-9, 9)])],
  cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    A, B = _AB(4*X**2 + 9*Y**2 - 144)
    d = _ell(A, B)
    P = (3, sqrt(B * (1 - Rational(9) / A)))
    return simplify(sum(_dist(P, f) for f in d["foci"].args))
q("U10-E-005", TOP_FOC, "Sum of focal distances", "Easy", "Single-step computation MCQ",
  r"If $P$ is any point on the ellipse $4x^2 + 9y^2 = 144$ and $S$, $S'$ are its foci, then $PS + PS'$ equals",
  r"$12$",
  [(r"$8$", r"Gives the length of the minor axis $2b = 8$."),
   (r"$6$", r"Gives the semi-major axis $a = 6$ rather than $2a$."),
   (r"$4\sqrt{5}$", r"Gives the distance between the foci, $2c = 2\sqrt{20}$.")],
  r"Dividing by $144$: $\frac{x^2}{36} + \frac{y^2}{16} = 1$, so $a = 6$. For every point on an ellipse the sum of the focal distances is the length of the major axis, $2a = 12$.",
  r"Using $a$ or $2b$ for the constant sum of focal distances.",
  "U10-E-focal-sum", "One defining property after reducing to standard form.",
  check=_c005, values=[12, 8, 6, 4*sqrt(5)], cognitive="Recall",
  numerical=dict(question=r"If $P$ is any point on the ellipse $4x^2 + 9y^2 = 144$ and $S$, $S'$ are its foci, then $PS + PS'$ is", answer=12))

# ---------------------------------------------------------------- 006
q("U10-E-006", TOP_STD, "Major axis when it is vertical", "Easy", "Single-step computation MCQ",
  r"The length of the major axis of the ellipse $16x^2 + y^2 = 16$ is",
  r"$8$",
  [(r"$2$", r"Gives the minor axis $2b = 2$, taking the axis along $x$ as the major axis."),
   (r"$4$", r"Gives the semi-major axis $a = 4$."),
   (r"$32$", r"Reads $a = 16$ from the coefficient and doubles it.")],
  r"Dividing by $16$: $\frac{x^2}{1} + \frac{y^2}{16} = 1$. The larger denominator $16$ is under $y^2$, so $a = 4$ along the $y$-axis and the major axis has length $2a = 8$.",
  r"Assuming the major axis is always along the $x$-axis.",
  "U10-E-axis-length", "One reduction and one comparison.",
  check=lambda: 2 * _ell(*_AB(16*X**2 + Y**2 - 16))["a"], values=[8, 2, 4, 32], cognitive="Application",
  numerical=dict(question=r"The length of the major axis of the ellipse $16x^2 + y^2 = 16$ is", answer=8))

# ---------------------------------------------------------------- 007
def _c007():
    a, c = 10, 8   # vertices (+-10, 0), foci (+-8, 0)
    b2 = a**2 - c**2
    return _key(X**2 / a**2 + Y**2 / b2 - 1)
q("U10-E-007", TOP_EQN, "Equation from vertices and foci", "Easy", "Single-step computation MCQ",
  r"The ellipse with vertices $(\pm 10, 0)$ and foci $(\pm 8, 0)$ has equation",
  r"$\frac{x^2}{100} + \frac{y^2}{36} = 1$",
  [(r"$\frac{x^2}{100} + \frac{y^2}{64} = 1$", r"Puts $c^2 = 64$ in place of $b^2$."),
   (r"$\frac{x^2}{100} + \frac{y^2}{164} = 1$", r"Uses $b^2 = a^2 + c^2 = 164$."),
   (r"$\frac{x^2}{36} + \frac{y^2}{100} = 1$", r"Finds $b^2 = 36$ but places $a^2 = 100$ under $y^2$.")],
  r"From the vertices $a = 10$ and from the foci $c = 8$. Then $b^2 = a^2 - c^2 = 100 - 64 = 36$, and the major axis is along the $x$-axis, so the ellipse is $\frac{x^2}{100} + \frac{y^2}{36} = 1$.",
  r"Using $c^2$ as $b^2$, or adding instead of subtracting in $b^2 = a^2 - c^2$.",
  "U10-E-eqn-vertices-foci", r"One relation $b^2 = a^2 - c^2$.",
  check=_c007,
  values=[_key(X**2/100 + Y**2/36 - 1), _key(X**2/100 + Y**2/64 - 1), _key(X**2/100 + Y**2/164 - 1), _key(X**2/36 + Y**2/100 - 1)],
  cognitive="Application")

# ---------------------------------------------------------------- 008
def _c008():
    sols = [s for s in solve(Rational(4, 8) + K_**2 / 18 - 1, K_) if s > 0]
    return sols[0]
q("U10-E-008", TOP_PTS, "Missing coordinate of a point on the ellipse", "Easy", "Inverse/parameter MCQ",
  r"If the point $(2, k)$ with $k > 0$ lies on the ellipse $\frac{x^2}{8} + \frac{y^2}{18} = 1$, then $k$ equals",
  r"$3$",
  [(r"$9$", r"Solves correctly for $k^2 = 9$ and stops there."),
   (r"$3\sqrt{2}$", r"Drops the $x$-term and solves $\frac{k^2}{18} = 1$."),
   (r"$\frac{3\sqrt{6}}{2}$", r"Uses $\frac{2}{8}$ instead of $\frac{2^2}{8}$, so $\frac{k^2}{18} = \frac{3}{4}$ and $k^2 = \frac{27}{2}$.")],
  r"Substituting: $\frac{4}{8} + \frac{k^2}{18} = 1$, so $\frac{k^2}{18} = \frac{1}{2}$, $k^2 = 9$ and $k = 3$ since $k > 0$.",
  r"Not squaring the given coordinate, or reporting $k^2$.",
  "U10-E-point-on-curve", "Direct substitution and one square root.",
  check=_c008, values=[3, 9, 3*sqrt(2), 3*sqrt(6)/2], cognitive="Application",
  numerical=dict(question=r"If the point $(2, k)$ with $k > 0$ lies on the ellipse $\frac{x^2}{8} + \frac{y^2}{18} = 1$, then $k$ is", answer=3))

# ---------------------------------------------------------------- 009
def _c009():
    b, c = symbols('b c', positive=True)
    # 2c = 2b
    a = sqrt(b**2 + c**2)
    return simplify((c / a).subs(b, c))
q("U10-E-009", TOP_ECC, "Minor axis equal to the focal distance", "Easy", "Single-step computation MCQ",
  r"For an ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ with $a > b$, the distance between the foci equals the length of the minor axis. The eccentricity of the ellipse is",
  r"$\frac{1}{\sqrt{2}}$",
  [(r"$\frac{1}{2}$", r"Gets $e^2 = \frac{1}{2}$ and reports it as $e$."),
   (r"$\frac{1}{\sqrt{5}}$", r"Equates $2c$ with the semi-minor axis $b$, so $b = 2c$, $a^2 = 5c^2$."),
   (r"$\frac{2}{\sqrt{5}}$", r"Equates the semi-focal distance $c$ with the full minor axis $2b$, so $c = 2b$, $a^2 = 5b^2$.")],
  r"The condition is $2c = 2b$, so $b = c$. Then $a^2 = b^2 + c^2 = 2c^2$, so $e = \frac{c}{a} = \frac{1}{\sqrt{2}}$.",
  r"Mixing full lengths ($2b$, $2c$) with semi-lengths ($b$, $c$).",
  "U10-E-ecc-b-equals-c", "One equation and one relation.",
  check=_c009, values=[1/sqrt(2), Rational(1, 2), 1/sqrt(5), 2/sqrt(5)], cognitive="Application")

# ---------------------------------------------------------------- 010
def _c010():
    d = _ell(9, 5)
    pts = _meet(X**2/9 + Y**2/5 - 1, X - d["c"])
    return [tuple(p) for p in pts if p[1] > 0][0]
q("U10-E-010", TOP_STD, "End of a latus rectum", "Easy", "Single-step computation MCQ",
  r"The end of a latus rectum of the ellipse $\frac{x^2}{9} + \frac{y^2}{5} = 1$ that lies in the first quadrant is",
  r"$\left(2, \frac{5}{3}\right)$",
  [(r"$\left(2, \frac{10}{3}\right)$", r"Uses the full latus rectum $\frac{2b^2}{a}$ as the ordinate of the end point."),
   (r"$\left(\frac{5}{3}, 2\right)$", r"Writes the coordinates in the wrong order."),
   (r"$\left(2, \frac{\sqrt{5}}{3}\right)$", r"Uses $\frac{b}{a}$ instead of $\frac{b^2}{a}$ for the ordinate.")],
  r"Here $a = 3$, $b^2 = 5$, $c = \sqrt{9 - 5} = 2$. The latus rectum through the focus $(2, 0)$ is the chord $x = 2$; putting $x = 2$ gives $\frac{y^2}{5} = \frac{5}{9}$, so $y = \pm\frac{5}{3}$. The first quadrant end is $\left(2, \frac{5}{3}\right)$.",
  r"Using the full latus rectum, rather than half of it, as the ordinate of an end point.",
  "U10-E-lr-endpoint", "Find the focus, then substitute once.",
  check=_c010,
  values=[(2, Rational(5, 3)), (2, Rational(10, 3)), (Rational(5, 3), 2), (2, sqrt(5)/3)],
  cognitive="Application")

# ---------------------------------------------------------------- 011
def _c011():
    b = Symbol('b', positive=True)
    sol = [s for s in solve(Eq(1 - b**2/16, Rational(3, 4)), b) if s < 4]
    return 2 * sol[0]
q("U10-E-011", TOP_STD, "Minor axis from eccentricity", "Easy", "Inverse/parameter MCQ",
  r"The ellipse $\frac{x^2}{16} + \frac{y^2}{b^2} = 1$, where $0 < b < 4$, has eccentricity $\frac{\sqrt{3}}{2}$. The length of its minor axis is",
  r"$4$",
  [(r"$2$", r"Finds $b = 2$ and reports the semi-minor axis."),
   (r"$4\sqrt{3}$", r"Uses $b^2 = a^2 e^2 = 12$, so $2b = 4\sqrt{3}$."),
   (r"$2\sqrt{3}$", r"Uses $b^2 = a^2 e^2 = 12$ and reports $b = 2\sqrt{3}$.")],
  r"With $a^2 = 16$, $e^2 = 1 - \frac{b^2}{16} = \frac{3}{4}$ gives $b^2 = 4$, so $b = 2$ and the minor axis is $2b = 4$.",
  r"Writing $b^2 = a^2e^2$ instead of $b^2 = a^2(1 - e^2)$.",
  "U10-E-b-from-e", "Reverse use of the eccentricity formula.",
  check=_c011, values=[4, 2, 4*sqrt(3), 2*sqrt(3)], cognitive="Application",
  numerical=dict(question=r"The ellipse $\frac{x^2}{16} + \frac{y^2}{b^2} = 1$, where $0 < b < 4$, has eccentricity $\frac{\sqrt{3}}{2}$. The length of its minor axis is", answer=4))

# ---------------------------------------------------------------- 012
def _c012():
    major, minor = 34, 16
    a, b = Rational(major, 2), Rational(minor, 2)
    d = _ell(a**2, b**2)
    f = list(d["foci"].args)
    return _dist(f[0], f[1])
q("U10-E-012", TOP_STD, "Distance between the foci from the axis lengths", "Easy", "Single-step computation MCQ",
  r"An ellipse has a major axis of length $34$ and a minor axis of length $16$. The distance between its foci is",
  r"$30$",
  [(r"$15$", r"Finds $c = 15$, the distance from the centre to one focus, and stops."),
   (r"$2\sqrt{353}$", r"Uses $c^2 = a^2 + b^2 = 289 + 64 = 353$ and doubles $c$."),
   (r"$60$", r"Puts the full lengths into $c^2 = 34^2 - 16^2 = 900$, getting $30$, and then doubles it again.")],
  r"The semi-axes are $a = 17$ and $b = 8$, so $c^2 = a^2 - b^2 = 289 - 64 = 225$ and $c = 15$. The foci are $2c = 30$ apart.",
  r"Reporting $c$ instead of $2c$, adding $a^2$ and $b^2$, or mixing full lengths with semi-lengths.",
  "U10-E-focal-gap-from-axes", "Halve the given lengths, then one relation.",
  check=_c012, values=[30, 15, 2*sqrt(353), 60], cognitive="Application",
  numerical=dict(question=r"An ellipse has a major axis of length $34$ and a minor axis of length $16$. The distance between its foci is", answer=30))

# ---------------------------------------------------------------- 013
def _c013():
    P = (4, Rational(12, 5))
    assert simplify(P[0]**2/25 + P[1]**2/16 - 1) == 0
    return _dist(P, (3, 0))
q("U10-E-013", TOP_FOC, "Focal distance of a given point", "Easy", "Single-step computation MCQ",
  r"The point $P\left(4, \frac{12}{5}\right)$ lies on the ellipse $\frac{x^2}{25} + \frac{y^2}{16} = 1$. The distance of $P$ from the focus $(3, 0)$ is",
  r"$\frac{13}{5}$",
  [(r"$\frac{37}{5}$", r"Uses $a + ex_1 = 5 + \frac{12}{5}$, the distance from the other focus $(-3, 0)$."),
   (r"$\frac{12}{5}$", r"Takes only the term $ex_1 = \frac{3}{5} \cdot 4$."),
   (r"$\frac{13}{3}$", r"Gives the distance from the directrix $x = \frac{25}{3}$, namely $\frac{25}{3} - 4$, without multiplying by $e$.")],
  r"Here $a = 5$, $c = 3$, $e = \frac{3}{5}$. The distance of $(x_1, y_1)$ from the focus $(ae, 0)$ is $a - ex_1 = 5 - \frac{3}{5} \cdot 4 = \frac{13}{5}$. Directly: $\sqrt{1 + \frac{144}{25}} = \frac{13}{5}$.",
  r"Using $a + ex_1$ for the focus on the same side as $P$.",
  "U10-E-focal-distance-point", "One focal distance formula.",
  check=_c013, values=[Rational(13, 5), Rational(37, 5), Rational(12, 5), Rational(13, 3)], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    b, c = 3, 2  # end of minor axis (3, 0), focus (0, 2): major axis along y
    a2 = b**2 + c**2
    return _key(X**2 / b**2 + Y**2 / a2 - 1)
q("U10-E-014", TOP_EQN, "Equation from a focus and an end of the minor axis", "Easy", "Single-step computation MCQ",
  r"An ellipse has its centre at the origin, one focus at $(0, 2)$ and one end of its minor axis at $(3, 0)$. Its equation is",
  r"$\frac{x^2}{9} + \frac{y^2}{13} = 1$",
  [(r"$\frac{x^2}{9} + \frac{y^2}{5} = 1$", r"Uses $a^2 = b^2 - c^2 = 9 - 4$."),
   (r"$\frac{x^2}{13} + \frac{y^2}{9} = 1$", r"Finds $a^2 = 13$ but places it under $x^2$."),
   (r"$\frac{x^2}{9} + \frac{y^2}{4} = 1$", r"Treats the focus $(0, 2)$ as an end of the major axis, taking $a = 2$.")],
  r"The focus is on the $y$-axis, so the major axis is along the $y$-axis with $c = 2$, and $b = 3$. Then $a^2 = b^2 + c^2 = 13$ and the ellipse is $\frac{x^2}{9} + \frac{y^2}{13} = 1$.",
  r"Subtracting instead of adding in $a^2 = b^2 + c^2$, or putting $a^2$ under the wrong variable.",
  "U10-E-eqn-focus-minor-end", "One relation and an orientation decision.",
  check=_c014,
  values=[_key(X**2/9 + Y**2/13 - 1), _key(X**2/9 + Y**2/5 - 1), _key(X**2/13 + Y**2/9 - 1), _key(X**2/9 + Y**2/4 - 1)],
  cognitive="Application")

# ---------------------------------------------------------------- 015
def _c015():
    d = _ell(25, 9)
    P = (3, Rational(12, 5))
    assert simplify(P[0]**2/25 + P[1]**2/9 - 1) == 0
    f = list(d["foci"].args)
    return simplify(_dist(P, f[0]) + _dist(P, f[1]) + _dist(f[0], f[1]))
q("U10-E-015", TOP_FOC, "Perimeter of the focal triangle", "Easy", "Single-step computation MCQ",
  r"$P$ is a point on the ellipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$, not on the major axis, and $S$, $S'$ are the foci. The perimeter of triangle $PSS'$ is",
  r"$18$",
  [(r"$10$", r"Counts only $PS + PS' = 2a$ and leaves out the side $SS'$."),
   (r"$14$", r"Uses $c = 4$ for the side $SS'$ instead of $2c = 8$."),
   (r"$16$", r"Uses the minor axis $2b = 6$ for the side $SS'$.")],
  r"$PS + PS' = 2a = 10$ for every point of the ellipse, and $SS' = 2c$ with $c^2 = 25 - 9 = 16$, so $SS' = 8$. The perimeter is $10 + 8 = 18$.",
  r"Forgetting the third side $SS' = 2c$, or using $c$ for it.",
  "U10-E-focal-triangle-perimeter", "Two standard facts added.",
  check=_c015, values=[18, 10, 14, 16], cognitive="Application",
  numerical=dict(question=r"$P$ is a point on the ellipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$, not on the major axis, and $S$, $S'$ are the foci. The perimeter of triangle $PSS'$ is", answer=18))

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 016
def _c016():
    b, a = symbols('b a', positive=True)
    r = solve(Eq(2*b**2/a, Rational(1, 3) * 2*b), b)[0]
    return simplify(sqrt(1 - (r/a)**2))
q("U10-E-016", TOP_ECC, "Latus rectum a fraction of the minor axis", "Medium", "Multi-step computation MCQ",
  r"The latus rectum of an ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ is one third of its minor axis. The eccentricity of the ellipse is",
  r"$\frac{2\sqrt{2}}{3}$",
  [(r"$\frac{1}{3}$", r"Gets $\frac{b}{a} = \frac{1}{3}$ and reports it as $e$."),
   (r"$\frac{\sqrt{6}}{3}$", r"Compares the latus rectum with the major axis: $\frac{2b^2}{a} = \frac{2a}{3}$ gives $\frac{b^2}{a^2} = \frac{1}{3}$ and $e = \sqrt{\frac{2}{3}}$."),
   (r"$\frac{8}{9}$", r"Gets $e^2 = 1 - \frac{1}{9} = \frac{8}{9}$ and does not take the square root.")],
  r"$\frac{2b^2}{a} = \frac{1}{3}(2b)$ gives $\frac{b}{a} = \frac{1}{3}$. Then $e^2 = 1 - \frac{b^2}{a^2} = 1 - \frac{1}{9} = \frac{8}{9}$, so $e = \frac{2\sqrt{2}}{3}$.",
  r"Stopping at $\frac{b}{a}$ or at $e^2$.",
  "U10-E-ecc-lr-condition", "Translate the condition, then two steps to $e$.",
  check=_c016, values=[2*sqrt(2)/3, Rational(1, 3), sqrt(6)/3, Rational(8, 9)], cognitive="Application")

# ---------------------------------------------------------------- 017
def _c017():
    a, e = symbols('a e', positive=True)
    s = [t for t in solve([a*e - 2, a/e - 8], [a, e], dict=True)][0]
    a2 = s[a]**2
    b2 = a2 * (1 - s[e]**2)
    return _key(X**2 / a2 + Y**2 / b2 - 1)
q("U10-E-017", TOP_EQN, "Equation from a focus and its directrix", "Medium", "Multi-step computation MCQ",
  r"An ellipse with centre at the origin and major axis along the $x$-axis has a focus at $(2, 0)$ and the corresponding directrix $x = 8$. Its equation is",
  r"$\frac{x^2}{16} + \frac{y^2}{12} = 1$",
  [(r"$\frac{x^2}{16} + \frac{y^2}{20} = 1$", r"Finds $a^2 = 16$ but uses $b^2 = a^2 + c^2 = 20$."),
   (r"$\frac{x^2}{64} + \frac{y^2}{60} = 1$", r"Takes the directrix distance $8$ as $a$, then $b^2 = 64 - 4$."),
   (r"$\frac{x^2}{12} + \frac{y^2}{16} = 1$", r"Finds $a^2 = 16$, $b^2 = 12$ but places $a^2$ under $y^2$.")],
  r"$ae = 2$ and $\frac{a}{e} = 8$. Multiplying, $a^2 = 16$; dividing, $e^2 = \frac{1}{4}$. Then $b^2 = a^2(1 - e^2) = 12$, so the ellipse is $\frac{x^2}{16} + \frac{y^2}{12} = 1$.",
  r"Treating the distance of the directrix from the centre as $a$ instead of $\frac{a}{e}$.",
  "U10-E-eqn-focus-directrix", "Two equations in $a$ and $e$, then $b^2$.",
  check=_c017,
  values=[_key(X**2/16 + Y**2/12 - 1), _key(X**2/16 + Y**2/20 - 1), _key(X**2/64 + Y**2/60 - 1), _key(X**2/12 + Y**2/16 - 1)],
  cognitive="Application")

# ---------------------------------------------------------------- 018
def _c018():
    pts = _meet(X**2 + 2*Y**2 - 8, Y - X + 2)
    return simplify(_dist(pts[0], pts[1]))
q("U10-E-018", TOP_INT, "Length of a chord cut by a line", "Medium", "Multi-step computation MCQ",
  r"The line $y = x - 2$ meets the ellipse $x^2 + 2y^2 = 8$ at the points $P$ and $Q$. The length $PQ$ is",
  r"$\frac{8\sqrt{2}}{3}$",
  [(r"$\frac{8}{3}$", r"Takes the difference of the abscissae, $|x_1 - x_2| = \frac{8}{3}$, as the chord length."),
   (r"$\frac{4\sqrt{2}}{3}$", r"Halves the correct length, treating the midpoint-to-end distance as the chord."),
   (r"$2\sqrt{6}$", r"Drops the coefficient $2$ of $y^2$ when substituting, solving $x^2 + (x - 2)^2 = 8$.")],
  r"Substituting $y = x - 2$: $x^2 + 2(x - 2)^2 = 8$, so $3x^2 - 8x = 0$ and $x = 0$ or $\frac{8}{3}$. The points are $(0, -2)$ and $\left(\frac{8}{3}, \frac{2}{3}\right)$, and $PQ = \sqrt{2} \cdot \frac{8}{3} = \frac{8\sqrt{2}}{3}$.",
  r"Using only the horizontal separation of the intersection points.",
  "U10-E-chord-length", "Solve a quadratic, then a distance.",
  check=_c018, values=[8*sqrt(2)/3, Rational(8, 3), 4*sqrt(2)/3, 2*sqrt(6)], cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    pts = _meet(4*X**2 + 9*Y**2 - 36, Y - X - 1)
    return (simplify((pts[0][0] + pts[1][0]) / 2), simplify((pts[0][1] + pts[1][1]) / 2))
q("U10-E-019", TOP_INT, "Midpoint of a chord cut by a line", "Medium", "Multi-step computation MCQ",
  r"The line $y = x + 1$ cuts the ellipse $4x^2 + 9y^2 = 36$ at $P$ and $Q$. The midpoint of $PQ$ is",
  r"$\left(-\frac{9}{13}, \frac{4}{13}\right)$",
  [(r"$\left(-\frac{18}{13}, -\frac{5}{13}\right)$", r"Uses the sum of the roots $x_1 + x_2 = -\frac{18}{13}$ itself as the abscissa of the midpoint."),
   (r"$\left(\frac{9}{13}, \frac{22}{13}\right)$", r"Sign slip in the sum of roots, taking $x_1 + x_2 = +\frac{18}{13}$."),
   (r"$(0, 1)$", r"Expands $9(x + 1)^2$ as $9x^2 + 9$, losing the $x$-term, so the roots are symmetric about $x = 0$.")],
  r"Substituting: $4x^2 + 9(x + 1)^2 = 36$, i.e. $13x^2 + 18x - 27 = 0$. So $x_1 + x_2 = -\frac{18}{13}$ and the midpoint has $x = -\frac{9}{13}$, $y = x + 1 = \frac{4}{13}$.",
  r"Using the sum of roots, not half of it, for the midpoint.",
  "U10-E-chord-midpoint", "Form a quadratic and use the sum of roots.",
  check=_c019,
  values=[(-Rational(9, 13), Rational(4, 13)), (-Rational(18, 13), -Rational(5, 13)),
          (Rational(9, 13), Rational(22, 13)), (0, 1)],
  cognitive="Application")

# ---------------------------------------------------------------- 020
def _c020():
    eq = expand(9*X**2 + 16*(X + C_)**2 - 144)
    p = Poly(eq, X)
    disc = p.coeff_monomial(X)**2 - 4*p.coeff_monomial(X**2)*p.coeff_monomial(1)
    return [s for s in solve(disc, C_) if s > 0][0]
q("U10-E-020", TOP_INT, "Line meeting the ellipse at exactly one point", "Medium", "Inverse/parameter MCQ",
  r"For $c > 0$, the line $y = x + c$ meets the ellipse $\frac{x^2}{16} + \frac{y^2}{9} = 1$ at exactly one point. Then $c$ equals",
  r"$5$",
  [(r"$7$", r"Takes $c = a + b$."),
   (r"$\sqrt{7}$", r"Uses $c^2 = a^2m^2 - b^2 = 16 - 9$."),
   (r"$25$", r"Gets $c^2 = 25$ and does not take the square root.")],
  r"Substituting: $9x^2 + 16(x + c)^2 = 144$, i.e. $25x^2 + 32cx + 16c^2 - 144 = 0$. Exactly one common point needs discriminant zero: $1024c^2 - 100(16c^2 - 144) = 0$, so $576c^2 = 14400$, $c^2 = 25$ and $c = 5$.",
  r"Misremembering the condition as $c^2 = a^2m^2 - b^2$.",
  "U10-E-line-one-point", "Form a quadratic and set its discriminant to zero.",
  check=_c020, values=[5, 7, sqrt(7), 25], cognitive="Application",
  numerical=dict(question=r"For $c > 0$, the line $y = x + c$ meets the ellipse $\frac{x^2}{16} + \frac{y^2}{9} = 1$ at exactly one point. The value of $c$ is", answer=5))

# ---------------------------------------------------------------- 021
def _c021():
    S2 = (3, 0)
    xs = symbols('xs', real=True)
    PS = 5 - Rational(3, 5) * xs   # distance from (3, 0)
    sol = solve(Eq(10 - PS, 3 * PS), xs)
    return [s for s in sol if -5 <= s <= 5][0]
q("U10-E-021", TOP_FOC, "Point from a ratio of focal distances", "Medium", "Inverse/parameter MCQ",
  r"$P$ is a point on the ellipse $\frac{x^2}{25} + \frac{y^2}{16} = 1$ with foci $S(3, 0)$ and $S'(-3, 0)$. If $PS' = 3\,PS$, then the abscissa of $P$ is",
  r"$\frac{25}{6}$",
  [(r"$-\frac{25}{6}$", r"Uses $PS = a + ex$ for the focus $(3, 0)$, swapping the two focal distance formulas."),
   (r"$\frac{5}{2}$", r"Finds $PS = \frac{5}{2}$ correctly but then sets $PS = a - x$, leaving out $e$."),
   (r"$\frac{25}{8}$", r"Uses $e = \frac{b}{a} = \frac{4}{5}$ in $PS = a - ex$.")],
  r"$PS + PS' = 2a = 10$ and $PS' = 3PS$ give $PS = \frac{5}{2}$. With $e = \frac{3}{5}$, $PS = a - ex = 5 - \frac{3x}{5}$, so $5 - \frac{3x}{5} = \frac{5}{2}$ and $x = \frac{25}{6}$, which lies in $[-5, 5]$.",
  r"Attaching $a + ex$ to the focus on the positive $x$-axis.",
  "U10-E-focal-ratio", "Sum property, then the focal distance formula in reverse.",
  check=_c021, values=[Rational(25, 6), -Rational(25, 6), Rational(5, 2), Rational(25, 8)], cognitive="Application")

# ---------------------------------------------------------------- 022
def _c022():
    b, c = symbols('b c', positive=True)
    a = sqrt(b**2 + c**2)
    # B(0,b), S(c,0), S'(-c,0) equilateral: BS = SS'
    sol = solve(Eq(a, 2*c), b)
    return simplify(c / a.subs(b, sol[0]))
q("U10-E-022", TOP_ECC, "Equilateral triangle on the foci", "Medium", "Multi-step computation MCQ",
  r"For the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$, the foci and one end of the minor axis are the vertices of an equilateral triangle. The eccentricity of the ellipse is",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{\sqrt{3}}$", r"Finds $b = \sqrt{3}c$ from the altitude and then takes $e = \frac{c}{b}$."),
   (r"$\frac{\sqrt{3}}{2}$", r"Gives $\frac{b}{a} = \frac{\sqrt{3}}{2}$ rather than $\frac{c}{a}$."),
   (r"$\frac{1}{4}$", r"Gets $e^2 = \frac{1}{4}$ and reports it as $e$.")],
  r"Let $B(0, b)$ and the foci $S(\pm c, 0)$. Then $BS = \sqrt{b^2 + c^2} = a$ and $SS' = 2c$. Equilateral means $a = 2c$, so $e = \frac{c}{a} = \frac{1}{2}$.",
  r"Not recognising that the distance from an end of the minor axis to a focus is $a$.",
  "U10-E-ecc-triangle", "Use $BS = a$, then one equation.",
  check=_c022, values=[Rational(1, 2), 1/sqrt(3), sqrt(3)/2, Rational(1, 4)], cognitive="Analysis")

# ---------------------------------------------------------------- 023
def _c023():
    d = _ell(16, 25)
    s1 = (d["foci"] == FiniteSet(Tuple(3, 0), Tuple(-3, 0)))
    s2 = (d["lr"] == Rational(32, 5))
    return (bool(s1), bool(s2))
q("U10-E-023", TOP_STD, "Vertical major axis: foci and latus rectum", "Medium", "Statement-based MCQ",
  r"Consider the ellipse $\frac{x^2}{16} + \frac{y^2}{25} = 1$." "\n"
  r"Statement I: The foci of the ellipse are $(\pm 3, 0)$." "\n"
  r"Statement II: The length of the latus rectum of the ellipse is $\frac{32}{5}$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts the foci $(\pm 3, 0)$ by assuming the major axis is along the $x$-axis."),
   (ST_FF, r"Rejects the foci correctly but computes the latus rectum as $\frac{2a^2}{b} = \frac{50}{4}$, swapping $a$ and $b$."),
   (ST_TF, r"Places the foci on the $x$-axis by habit and also uses $\frac{2a^2}{b} = \frac{25}{2}$ for the latus rectum.")],
  r"Here $25 > 16$, so the major axis is along the $y$-axis with $a = 5$, $b = 4$, $c = 3$. The foci are $(0, \pm 3)$, so Statement I is false. The latus rectum is $\frac{2b^2}{a} = \frac{32}{5}$, so Statement II is true.",
  r"Assuming the foci always lie on the $x$-axis.",
  "U10-E-stmt-vertical", "Orientation check and one formula, judged separately.",
  check=_c023, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis")

# ---------------------------------------------------------------- 024
def _c024():
    a2, b2 = symbols('A B', positive=True)
    s = solve([16/a2 + 9/b2 - 1, 36/a2 + 4/b2 - 1], [a2, b2], dict=True)[0]
    return _ell(s[a2], s[b2])["lr"]
q("U10-E-024", TOP_EQN, "Ellipse through two points", "Medium", "Multi-step computation MCQ",
  r"The ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ passes through the points $(4, 3)$ and $(6, 2)$. The length of its latus rectum is",
  r"$\sqrt{13}$",
  [(r"$\frac{\sqrt{13}}{2}$", r"Gives $\frac{b^2}{a} = \frac{13}{2\sqrt{13}}$, half the latus rectum."),
   (r"$8\sqrt{13}$", r"Uses $\frac{2a^2}{b} = \frac{104}{\sqrt{13}}$, swapping $a$ and $b$."),
   (r"$2\sqrt{13}$", r"Gives the minor axis $2b = 2\sqrt{13}$.")],
  r"Put $u = \frac{1}{a^2}$, $v = \frac{1}{b^2}$: $16u + 9v = 1$ and $36u + 4v = 1$. Solving, $u = \frac{1}{52}$, $v = \frac{1}{13}$, so $a^2 = 52 > b^2 = 13$. The latus rectum is $\frac{2b^2}{a} = \frac{26}{2\sqrt{13}} = \sqrt{13}$.",
  r"Using half the latus rectum, or swapping the roles of $a$ and $b$.",
  "U10-E-eqn-two-points", r"A linear system in $\frac{1}{a^2}$, $\frac{1}{b^2}$, then a formula.",
  check=_c024, values=[sqrt(13), sqrt(13)/2, 8*sqrt(13), 2*sqrt(13)], cognitive="Application")

# ---------------------------------------------------------------- 025
def _c025():
    xs = Symbol('xs', real=True)
    e = Rational(4, 5)
    prod = (5 - e*xs) * (5 + e*xs)
    from sympy.calculus.util import maximum
    return maximum(prod, xs, Interval(-5, 5))
q("U10-E-025", TOP_FOC, "Greatest product of focal distances", "Medium", "Multi-step computation MCQ",
  r"$P$ is a variable point on the ellipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$ and $S$, $S'$ are its foci. The greatest value of $PS \cdot PS'$ is",
  r"$25$",
  [(r"$9$", r"Evaluates $a^2 - e^2x^2$ at $x = \pm 5$, which gives the least value."),
   (r"$41$", r"Writes the product as $a^2 + e^2x^2$ and takes $x = \pm 5$: $25 + 16$."),
   (r"$81$", r"Uses the largest focal distance $a + c = 9$ for both factors.")],
  r"Here $a = 5$, $e = \frac{4}{5}$. For $P(x, y)$, $PS \cdot PS' = (a - ex)(a + ex) = 25 - \frac{16}{25}x^2$, which is greatest when $x = 0$, giving $25$ (at the ends of the minor axis, where both distances equal $a$).",
  r"Expecting the extreme product at the vertices rather than at the ends of the minor axis.",
  "U10-E-focal-product", "Write the product with focal distance formulas, then optimise over $x$.",
  check=_c025, values=[25, 9, 41, 81], cognitive="Analysis",
  numerical=dict(question=r"$P$ is a variable point on the ellipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$ and $S$, $S'$ are its foci. The greatest value of $PS \cdot PS'$ is", answer=25))

# ---------------------------------------------------------------- 026
def _c026():
    s = solve(Eq(2*A_/E_, 3 * 2*A_*E_), E_)
    return [v for v in s if v < 1][0]
q("U10-E-026", TOP_ECC, "Directrices and foci distances compared", "Medium", "Multi-step computation MCQ",
  r"For an ellipse, the distance between the directrices is three times the distance between the foci. The eccentricity of the ellipse is",
  r"$\frac{1}{\sqrt{3}}$",
  [(r"$\frac{1}{3}$", r"Reads $e^2 = \frac{1}{3}$ as $e = \frac{1}{3}$."),
   (r"$\frac{1}{\sqrt{6}}$", r"Takes the distance between the directrices as $\frac{a}{e}$: $\frac{a}{e} = 3 \cdot 2ae$."),
   (r"$\frac{\sqrt{6}}{3}$", r"Takes the distance between the foci as $ae$: $\frac{2a}{e} = 3ae$ gives $e^2 = \frac{2}{3}$.")],
  r"The directrices are $x = \pm\frac{a}{e}$ and the foci $(\pm ae, 0)$, so $\frac{2a}{e} = 3 \cdot 2ae$. Hence $e^2 = \frac{1}{3}$ and $e = \frac{1}{\sqrt{3}}$.",
  r"Using one-sided distances $\frac{a}{e}$ or $ae$ in place of the full gaps.",
  "U10-E-ecc-directrix-ratio", "Set up one equation with two distances, solve for $e$.",
  check=_c026, values=[1/sqrt(3), Rational(1, 3), 1/sqrt(6), sqrt(6)/3], cognitive="Application")

# ---------------------------------------------------------------- 027
def _c027():
    S, S2 = (0, 4), (0, -4)
    P = (Rational(9, 5), 4)
    a = (_dist(P, S) + _dist(P, S2)) / 2
    c = 4
    return simplify(2 * sqrt(a**2 - c**2))
q("U10-E-027", TOP_EQN, "Ellipse through a point with given foci", "Medium", "Multi-step computation MCQ",
  r"An ellipse has foci $(0, \pm 4)$ and passes through the point $\left(\frac{9}{5}, 4\right)$. The length of its minor axis is",
  r"$6$",
  [(r"$10$", r"Finds $2a = 10$ from the sum of focal distances and reports the major axis."),
   (r"$3$", r"Finds $b = 3$ and reports the semi-minor axis."),
   (r"$2\sqrt{41}$", r"Finds $a = 5$ but uses $b^2 = a^2 + c^2 = 41$.")],
  r"The distances of $\left(\frac{9}{5}, 4\right)$ from $(0, 4)$ and $(0, -4)$ are $\frac{9}{5}$ and $\sqrt{\frac{81}{25} + 64} = \frac{41}{5}$, so $2a = 10$, $a = 5$. With $c = 4$, $b^2 = 25 - 16 = 9$, and the minor axis is $2b = 6$.",
  r"Adding $c^2$ to $a^2$ instead of subtracting.",
  "U10-E-eqn-foci-point", "Sum of focal distances gives $a$, then $b$.",
  check=_c027, values=[6, 10, 3, 2*sqrt(41)], cognitive="Application",
  numerical=dict(question=r"An ellipse has foci $(0, \pm 4)$ and passes through the point $\left(\frac{9}{5}, 4\right)$. The length of its minor axis is", answer=6))

# ---------------------------------------------------------------- 028
def _c028():
    a, b, e = symbols('a b e', positive=True)
    xs, ys = symbols('xs ys', real=True)
    s1 = True  # PS + PS' = (a - e x) + (a + e x) = 2a
    s1 = simplify((a - e*xs) + (a + e*xs) - 2*a) == 0
    s2 = simplify(2*a/e - 2*a*e) == 0
    return (bool(s1), bool(s2))
q("U10-E-028", TOP_FOC, "Focal sum and directrix gap", "Medium", "Statement-based MCQ",
  r"For the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ with $a > b$, eccentricity $e$ and foci $S$, $S'$:" "\n"
  r"Statement I: For every point $P$ on the ellipse, $PS + PS' = 2a$." "\n"
  r"Statement II: The distance between the two directrices is $2ae$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Confuses the directrices $x = \pm\frac{a}{e}$ with the lines $x = \pm ae$ through the foci."),
   (ST_FF, r"Believes the focal sum equals $2b$ and also rejects Statement II."),
   (ST_FT, r"Believes the focal sum equals the distance between the foci and accepts $2ae$ for the directrices.")],
  r"For $P(x, y)$ on the ellipse, $PS = a - ex$ and $PS' = a + ex$, so $PS + PS' = 2a$; Statement I is true. The directrices are $x = \pm\frac{a}{e}$, so they are $\frac{2a}{e}$ apart, not $2ae$ (which is the distance between the foci, and $\frac{2a}{e} \neq 2ae$ since $e < 1$); Statement II is false.",
  r"Mixing up the positions of the foci and the directrices.",
  "U10-E-stmt-focal-directrix", "Two standard facts, one of them misquoted.",
  check=_c028, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding")

# ---------------------------------------------------------------- 029
def _c029():
    a, b, c = symbols('a b c', positive=True)
    s = solve([Eq(2*b**2/a, 10), Eq(b, c), Eq(a**2, b**2 + c**2)], [a, b, c], dict=True)[0]
    return 2 * s[a]
q("U10-E-029", TOP_EQN, "Major axis from latus rectum and a shape condition", "Medium", "Multi-step computation MCQ",
  r"An ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ has latus rectum of length $10$, and the distance between its foci equals the length of its minor axis. The length of its major axis is",
  r"$20$",
  [(r"$40$", r"Uses $\frac{b^2}{a} = 10$ for the latus rectum, so $\frac{a}{2} = 10$."),
   (r"$10$", r"Finds $a = 10$ and reports the semi-major axis."),
   (r"$\frac{25}{2}$", r"Reads the condition as $2c = b$, so $a^2 = \frac{5b^2}{4}$ and $\frac{2b^2}{a} = \frac{8a}{5} = 10$.")],
  r"$2c = 2b$ gives $b = c$ and $a^2 = b^2 + c^2 = 2b^2$. Then $\frac{2b^2}{a} = \frac{a^2}{a} = a = 10$, so the major axis is $2a = 20$.",
  r"Using half the latus rectum in place of the whole.",
  "U10-E-axis-from-lr", "Combine a shape condition with the latus rectum formula.",
  check=_c029, values=[20, 40, 10, Rational(25, 2)], cognitive="Application",
  numerical=dict(question=r"An ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ has latus rectum of length $10$, and the distance between its foci equals the length of its minor axis. The length of its major axis is", answer=20))

# ---------------------------------------------------------------- 030
def _c030():
    curve = X**2/25 + Y**2/16 - 1
    pts = _meet(curve, X - 3)
    S2 = (-3, 0)
    P, Q = pts
    return Abs(P[0]*(Q[1]-S2[1]) + Q[0]*(S2[1]-P[1]) + S2[0]*(P[1]-Q[1])) / 2
q("U10-E-030", TOP_STD, "Triangle on a latus rectum and the other focus", "Medium", "Multi-step computation MCQ",
  r"The latus rectum through the focus $S(3, 0)$ of the ellipse $\frac{x^2}{25} + \frac{y^2}{16} = 1$ has end points $P$ and $Q$. If $S'$ is the other focus, the area of triangle $PQS'$ is",
  r"$\frac{96}{5}$",
  [(r"$\frac{48}{5}$", r"Uses half the latus rectum, $\frac{16}{5}$, as the base."),
   (r"$\frac{192}{5}$", r"Omits the factor $\frac{1}{2}$ in the area of a triangle."),
   (r"$\frac{75}{2}$", r"Uses $\frac{2a^2}{b} = \frac{25}{2}$ for the latus rectum.")],
  r"Here $c = 3$, so $S' = (-3, 0)$. The latus rectum $x = 3$ meets the ellipse where $y^2 = 16\left(1 - \frac{9}{25}\right)$, so $y = \pm\frac{16}{5}$ and $PQ = \frac{32}{5}$. The height from $S'$ is $2c = 6$, so the area is $\frac{1}{2} \cdot \frac{32}{5} \cdot 6 = \frac{96}{5}$.",
  r"Using half the latus rectum as the full base.",
  "U10-E-lr-triangle", "Latus rectum, distance between foci, area formula.",
  check=_c030, values=[Rational(96, 5), Rational(48, 5), Rational(192, 5), Rational(75, 2)], cognitive="Application")

# ---------------------------------------------------------------- 031
def _c031():
    a2 = Symbol('A', positive=True)
    b2 = a2 * (1 - Rational(1, 4))
    s = solve(Eq(1/a2 + Rational(9, 4)/b2, 1), a2)[0]
    return _ell(s, s * Rational(3, 4))["lr"]
q("U10-E-031", TOP_EQN, "Latus rectum from eccentricity and a point", "Medium", "Multi-step computation MCQ",
  r"The ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ has eccentricity $\frac{1}{2}$ and passes through the point $\left(1, \frac{3}{2}\right)$. The length of its latus rectum is",
  r"$3$",
  [(r"$\frac{3}{2}$", r"Gives $\frac{b^2}{a} = \frac{3}{2}$, half the latus rectum."),
   (r"$\frac{8\sqrt{3}}{3}$", r"Uses $\frac{2a^2}{b} = \frac{8}{\sqrt{3}}$, swapping $a$ and $b$."),
   (r"$2\sqrt{3}$", r"Gives the minor axis $2b = 2\sqrt{3}$.")],
  r"$b^2 = a^2(1 - e^2) = \frac{3a^2}{4}$. Substituting the point: $\frac{1}{a^2} + \frac{9/4}{3a^2/4} = \frac{1}{a^2} + \frac{3}{a^2} = 1$, so $a^2 = 4$, $b^2 = 3$. The latus rectum is $\frac{2b^2}{a} = \frac{6}{2} = 3$.",
  r"Using half the latus rectum or swapping $a$ and $b$.",
  "U10-E-eqn-e-point", "Express $b^2$ via $e$, substitute the point, then a formula.",
  check=_c031, values=[3, Rational(3, 2), 8*sqrt(3)/3, 2*sqrt(3)], cognitive="Application",
  numerical=dict(question=r"The ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ has eccentricity $\frac{1}{2}$ and passes through the point $\left(1, \frac{3}{2}\right)$. The length of its latus rectum is", answer=3))

# ---------------------------------------------------------------- 032
def _c032():
    d = _ell(36, 32)
    # P on the ellipse, distance 15 from the line x = 18, |x| <= a
    xs = [v for v in solve(Eq(Abs(18 - X), 15), X) if Abs(v) <= d["a"]]
    assert len(xs) == 1
    x1 = xs[0]
    ys = solve(Eq(x1**2/36 + Y**2/32, 1), Y)
    assert all(v.is_real for v in ys)
    return simplify(_dist((x1, ys[0]), (-2, 0)))
q("U10-E-032", TOP_FOC, "Far focal distance from the distance to a directrix", "Medium", "Multi-step computation MCQ",
  r"$P$ is a point on the ellipse $\frac{x^2}{36} + \frac{y^2}{32} = 1$ whose distance from the line $x = 18$ is $15$. If $S'$ is the focus $(-2, 0)$, then $PS'$ equals",
  r"$7$",
  [(r"$5$", r"Finds $PS = e \cdot 15 = 5$ for the focus $S(2, 0)$ belonging to the line $x = 18$ and stops, giving the nearer focal distance."),
   (r"$9$", r"Finds $x = 3$ correctly but drops $e$ in the focal distance formula: $PS' = a + x = 6 + 3$."),
   (r"$\frac{31}{3}$", r"Uses $e^2 = \frac{1}{9}$ in place of $e$, so $PS = \frac{15}{9} = \frac{5}{3}$ and $PS' = 12 - \frac{5}{3}$.")],
  r"Here $a = 6$, $b^2 = 32$, $c = 2$, $e = \frac{1}{3}$, and $x = 18 = \frac{a}{e}$ is the directrix belonging to the focus $S(2, 0)$. By the focus-directrix property, $PS = e \cdot 15 = 5$, and then $PS' = 2a - PS = 12 - 5 = 7$. (Check: $18 - x = 15$ gives $x = 3$, and $PS' = a + ex = 6 + 1 = 7$.)",
  r"Stopping at the focal distance from the focus that matches the given directrix.",
  "U10-E-directrix-to-far-focus", r"Match the directrix to its focus, use $PS = e \cdot PM$, then the focal sum.",
  check=_c032, values=[7, 5, 9, Rational(31, 3)], cognitive="Application",
  numerical=dict(question=r"$P$ is a point on the ellipse $\frac{x^2}{36} + \frac{y^2}{32} = 1$ whose distance from the line $x = 18$ is $15$. If $S'$ is the focus $(-2, 0)$, then $PS'$ is", answer=7))

# ---------------------------------------------------------------- 033
def _c033():
    n = 0
    for xx in range(-10, 11):
        for yy in range(-5, 6):
            if xx**2 + 4*yy**2 == 100:
                n += 1
    return n
q("U10-E-033", TOP_PTS, "Lattice points on an ellipse", "Medium", "Multi-step computation MCQ",
  r"The number of points with both coordinates integers that lie on the ellipse $x^2 + 4y^2 = 100$ is",
  r"$12$",
  [(r"$8$", r"Counts only the points $(\pm 8, \pm 3)$ and $(\pm 6, \pm 4)$, missing the vertices."),
   (r"$4$", r"Counts only the four vertices $(\pm 10, 0)$, $(0, \pm 5)$."),
   (r"$16$", r"Counts each vertex as if it gave four sign combinations like the other points.")],
  r"Here $|y| \le 5$. Checking: $y = 0$ gives $x = \pm 10$; $y = \pm 3$ gives $x^2 = 64$, $x = \pm 8$; $y = \pm 4$ gives $x^2 = 36$, $x = \pm 6$; $y = \pm 5$ gives $x = 0$; $y = \pm 1, \pm 2$ give $96$, $84$, not squares. Total $2 + 4 + 4 + 2 = 12$.",
  r"Treating every solution as producing four sign combinations.",
  "U10-E-lattice-points", "Systematic casework over the bounded range of $y$.",
  check=_c033, values=[12, 8, 4, 16], cognitive="Analysis",
  numerical=dict(question=r"The number of points with both coordinates integers that lie on the ellipse $x^2 + 4y^2 = 100$ is", answer=12))

# ---------------------------------------------------------------- 034
def _c034():
    return reduce_inequalities([10 - K_ > K_ - 4, K_ - 4 > 0], K_).as_set()
q("U10-E-034", TOP_STD, "Parameter range for a horizontal major axis", "Medium", "Inverse/parameter MCQ",
  r"The equation $\frac{x^2}{10 - k} + \frac{y^2}{k - 4} = 1$ represents an ellipse whose major axis lies along the $x$-axis exactly when $k$ belongs to",
  r"$(4, 7)$",
  [(r"$(4, 10)$", r"Imposes only that both denominators are positive, which also allows a circle at $k = 7$ and a vertical major axis."),
   (r"$(7, 10)$", r"Reverses the comparison, requiring $k - 4 > 10 - k$, which puts the major axis along the $y$-axis."),
   (r"$(-\infty, 7)$", r"Imposes only $10 - k > k - 4$ and forgets that $k - 4$ must be positive.")],
  r"We need both denominators positive and the larger one under $x^2$: $k - 4 > 0$ and $10 - k > k - 4$. These give $k > 4$ and $k < 7$, so $k \in (4, 7)$.",
  r"Forgetting either the positivity of the denominators or the comparison that fixes the major axis.",
  "U10-E-param-range", "Two inequalities combined.",
  check=_c034, values=[Interval.open(4, 7), Interval.open(4, 10), Interval.open(7, 10), Interval.open(-oo, 7)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 035
def _c035():
    a, e = symbols('a e', positive=True)
    sols = solve([2*a**2*(1 - e**2)/a - 16, a/e - a*e - 24], [a, e], dict=True)
    sols = [t for t in sols if t[e].is_positive and t[e] < 1 and t[a].is_positive]
    assert len(sols) == 1
    return simplify(2*sols[0][a])
q("U10-E-035", TOP_STD, "Major axis from the latus rectum and the focus-directrix gap", "Medium", "Multi-step computation MCQ",
  r"For an ellipse in standard form, the length of the latus rectum is $16$ and the distance between a focus and its corresponding directrix is $24$. The length of its major axis is",
  r"$18$",
  [(r"$9$", r"Finds $a = 9$ correctly but reports $a$ instead of $2a$."),
   (r"$\frac{144}{5}$", r"Takes $e = \frac{16}{24} = \frac{2}{3}$ using the full latus rectum, then $a\left(1 - \frac{4}{9}\right) = 8$ gives $a = \frac{72}{5}$ and $2a = \frac{144}{5}$."),
   (r"$36$", r"Finds $e = \frac{1}{3}$ correctly but then sets $\frac{b^2}{a} = a(1 - e^2)$ equal to the full latus rectum $16$, getting $a = 18$ and $2a = 36$.")],
  r"An end $L$ of the latus rectum through the focus $S$ is at distance $\frac{b^2}{a} = 8$ from $S$ and at distance $24$ (the focus-directrix gap) from the directrix, so by $SL = e \cdot (\text{distance to directrix})$, $e = \frac{8}{24} = \frac{1}{3}$. Then $\frac{b^2}{a} = a(1 - e^2) = \frac{8a}{9} = 8$ gives $a = 9$, so the major axis is $2a = 18$. (Check: $\frac{a}{e} - ae = 27 - 3 = 24$.)",
  r"Dividing the full latus rectum, instead of the semi-latus rectum, by the focus-directrix distance to get $e$.",
  "U10-E-major-axis-lr-gap", r"Needs the focus-directrix property at an end of the latus rectum to get $e$, then $a$ from $\frac{b^2}{a}$.",
  check=_c035, values=[Integer(18), Integer(9), Rational(144, 5), Integer(36)], cognitive="Application")

# ---------------------------------------------------------------- 036
def _c036():
    d1 = _ell(*_AB(2*X**2 + 3*Y**2 - 6))
    d2 = _ell(9, 4)
    return (bool(simplify(d1["e"] - sqrt(Rational(2, 3))) == 0), bool(simplify(d2["lr"] - Rational(4, 3)) == 0))
q("U10-E-036", TOP_STD, "Eccentricity and latus rectum claims", "Medium", "Statement-based MCQ",
  r"Statement I: The eccentricity of the ellipse $2x^2 + 3y^2 = 6$ is $\sqrt{\frac{2}{3}}$." "\n"
  r"Statement II: The length of the latus rectum of the ellipse $\frac{x^2}{9} + \frac{y^2}{4} = 1$ is $\frac{4}{3}$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts $e = \sqrt{\frac{b^2}{a^2}} = \sqrt{\frac{2}{3}}$ and the semi-latus rectum $\frac{b^2}{a} = \frac{4}{3}$ as the latus rectum."),
   (ST_TF, r"Uses $e = \frac{b}{a}$ for Statement I but evaluates the latus rectum correctly."),
   (ST_FT, r"Evaluates $e$ correctly but takes the semi-latus rectum $\frac{4}{3}$ as the latus rectum.")],
  r"$2x^2 + 3y^2 = 6$ is $\frac{x^2}{3} + \frac{y^2}{2} = 1$, so $e^2 = 1 - \frac{2}{3} = \frac{1}{3}$ and $e = \frac{1}{\sqrt{3}}$; Statement I is false. For $\frac{x^2}{9} + \frac{y^2}{4} = 1$ the latus rectum is $\frac{2b^2}{a} = \frac{8}{3}$; Statement II is false.",
  r"Using $\frac{b}{a}$ for $e$ and $\frac{b^2}{a}$ for the latus rectum.",
  "U10-E-stmt-ecc-lr", "Two independent computations, each with a common slip.",
  check=_c036, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 037
def _c037():
    S, S2 = (1, 2), (1, -4)
    d1 = sqrt((X - S[0])**2 + (Y - S[1])**2)
    d2 = sqrt((X - S2[0])**2 + (Y - S2[1])**2)
    # Remove the radicals: d1 + d2 = 10  =>  (d2^2 - d1^2 - 100)^2 = 400 d1^2
    D1, D2 = expand(d1**2), expand(d2**2)
    locus = expand((D2 - D1 - 100)**2 - 400*D1)
    # confirm on sample points that the squared curve is the genuine locus (sum exactly 10)
    for yy in [-1, 0, 2, Rational(-7, 2), 3]:
        for xx in solve(locus.subs(Y, yy), X):
            assert simplify(d1.subs({X: xx, Y: yy}) + d2.subs({X: xx, Y: yy}) - 10) == 0
    return _key(locus)
q("U10-E-037", TOP_EQN, "Locus from the focal sum, centre not at the origin", "Medium", "Multi-step computation MCQ",
  r"A point $P$ moves so that the sum of its distances from $(1, 2)$ and $(1, -4)$ is always $10$. The locus of $P$ is",
  r"$\frac{(x - 1)^2}{16} + \frac{(y + 1)^2}{25} = 1$",
  [(r"$\frac{(x - 1)^2}{25} + \frac{(y + 1)^2}{16} = 1$", r"Finds the centre $(1, -1)$, $a = 5$, $b = 4$ correctly but puts $a^2$ under the $x$-term, although the foci lie on the vertical line $x = 1$."),
   (r"$\frac{(x + 1)^2}{16} + \frac{(y - 1)^2}{25} = 1$", r"Finds the centre $(1, -1)$ but writes $(x + 1)$ and $(y - 1)$, a sign slip in the shift."),
   (r"$\frac{(x - 1)^2}{9} + \frac{(y + 1)^2}{25} = 1$", r"Puts $c^2 = 9$ in place of $b^2 = a^2 - c^2 = 16$.")],
  r"The locus is an ellipse with these points as foci. Its centre is the midpoint $(1, -1)$, and the foci lie on the vertical line $x = 1$, so the major axis is vertical. Here $2a = 10$, so $a = 5$; $2c = 6$, so $c = 3$; and $b^2 = a^2 - c^2 = 16$. Hence the locus is $\frac{(x - 1)^2}{16} + \frac{(y + 1)^2}{25} = 1$.",
  r"Losing track of the shifted centre or of the orientation of the major axis.",
  "U10-E-locus-focal-sum-shifted", r"Recognise the ellipse definition, locate the shifted centre and orientation, then find $b$.",
  check=_c037,
  values=[_key(25*(X - 1)**2 + 16*(Y + 1)**2 - 400), _key(16*(X - 1)**2 + 25*(Y + 1)**2 - 400),
          _key(25*(X + 1)**2 + 16*(Y - 1)**2 - 400), _key(25*(X - 1)**2 + 9*(Y + 1)**2 - 225)],
  cognitive="Application")

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 038
def _c038():
    kk = Symbol('kk', positive=True)
    vals = []
    for s in solve(Eq(1 - 9/kk, Rational(1, 4)), kk):   # k > 9
        if s > 9:
            vals.append(s)
    for s in solve(Eq(1 - kk/9, Rational(1, 4)), kk):   # k < 9
        if s < 9:
            vals.append(s)
    return sum(vals)
q("U10-E-038", TOP_ECC, "Parameter from eccentricity, both orientations", "Difficult", "Inverse/parameter MCQ",
  r"The ellipse $\frac{x^2}{k} + \frac{y^2}{9} = 1$, where $k > 0$ and $k \neq 9$, has eccentricity $\frac{1}{2}$. The sum of all possible values of $k$ is",
  r"$\frac{75}{4}$",
  [(r"$12$", r"Assumes the major axis is along the $x$-axis and finds only $k = 12$."),
   (r"$\frac{27}{4}$", r"Assumes the major axis is along the $y$-axis and finds only $k = \frac{27}{4}$."),
   (r"$\frac{93}{4}$", r"Finds $k = 12$, but for $k < 9$ uses $e^2 = \frac{k}{9} - 1$, getting $k = \frac{45}{4}$, and adds.")],
  r"If $k > 9$: $e^2 = 1 - \frac{9}{k} = \frac{1}{4}$ gives $k = 12$. If $k < 9$, the major axis is along the $y$-axis and $e^2 = 1 - \frac{k}{9} = \frac{1}{4}$ gives $k = \frac{27}{4}$. Both are valid, so the sum is $12 + \frac{27}{4} = \frac{75}{4}$.",
  r"Assuming the larger denominator is always under $x^2$.",
  "U10-E-param-both-orientations", "Casework on the orientation; one case is easily missed.",
  check=_c038, values=[Rational(75, 4), 12, Rational(27, 4), Rational(93, 4)], cognitive="Analysis")

# ---------------------------------------------------------------- 039
def _c039():
    b, c = symbols('b c', positive=True)
    # B(0,b), S(c,0), S'(-c,0); angle SBS' = 90 deg and area 8
    s = solve([(c)*(-c) + (-b)*(-b), Rational(1, 2) * 2*c * b - 8], [b, c], dict=True)[0]
    a = sqrt(s[b]**2 + s[c]**2)
    return simplify(2 * s[b]**2 / a)
q("U10-E-039", TOP_ECC, "Right-angled focal triangle with given area", "Difficult", "Multi-step computation MCQ",
  r"For the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ with foci $S$ and $S'$, let $B$ be an end of the minor axis. If $\angle SBS' = 90^\circ$ and the area of triangle $SBS'$ is $8$, the length of the latus rectum is",
  r"$4$",
  [(r"$2\sqrt{2}$", r"Uses area $= 2c \cdot b$ without the $\frac{1}{2}$, so $c^2 = 4$, $a^2 = 8$ and $\frac{2b^2}{a} = \frac{8}{2\sqrt{2}}$."),
   (r"$2$", r"Finds $a = 4$, $b^2 = 8$ and gives $\frac{b^2}{a}$."),
   (r"$8\sqrt{2}$", r"Uses $\frac{2a^2}{b} = \frac{32}{2\sqrt{2}}$, swapping $a$ and $b$.")],
  r"With $B(0, b)$ and $S(\pm c, 0)$, $\angle SBS' = 90^\circ$ means $\overrightarrow{BS} \cdot \overrightarrow{BS'} = -c^2 + b^2 = 0$, so $b = c$. The area is $\frac{1}{2} \cdot 2c \cdot b = c^2 = 8$, so $b^2 = c^2 = 8$ and $a^2 = 16$. The latus rectum is $\frac{2b^2}{a} = \frac{16}{4} = 4$.",
  r"Dropping the factor $\frac{1}{2}$ in the area, or swapping $a$ and $b$ in the latus rectum.",
  "U10-E-right-focal-triangle", "Angle condition, area condition, then the latus rectum.",
  check=_c039, values=[4, 2*sqrt(2), 2, 8*sqrt(2)], cognitive="Analysis",
  numerical=dict(question=r"For the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ with foci $S$ and $S'$, let $B$ be an end of the minor axis. If $\angle SBS' = 90^\circ$ and the area of triangle $SBS'$ is $8$, the length of the latus rectum is", answer=4))

# ---------------------------------------------------------------- 040
def _c040():
    sols = solve([X**2/25 + Y**2/9 - 1, X**2 + Y**2 - 16], [X, Y], dict=True)
    s = [t for t in sols if t[X] > 0 and t[Y] > 0][0]
    return simplify(Rational(1, 2) * 8 * s[Y])
q("U10-E-040", TOP_FOC, "Point seeing the foci at a right angle", "Difficult", "Multi-step computation MCQ",
  r"$P$ is a point on the ellipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$ such that $\angle SPS' = 90^\circ$, where $S$ and $S'$ are the foci. The area of triangle $SPS'$ is",
  r"$9$",
  [(r"$18$", r"Finds $PS \cdot PS' = 18$ and omits the factor $\frac{1}{2}$ in the area."),
   (r"$\frac{9}{2}$", r"Finds $|y| = \frac{9}{4}$ but uses $c = 4$ as the base instead of $2c = 8$."),
   (r"$5\sqrt{7}$", r"Uses the abscissa $|x| = \frac{5\sqrt{7}}{4}$ as the height of the triangle.")],
  r"Here $c = 4$. Since $\angle SPS' = 90^\circ$, $P$ lies on the circle with diameter $SS'$: $x^2 + y^2 = 16$. With $\frac{x^2}{25} + \frac{y^2}{9} = 1$ this gives $x^2 = \frac{175}{16}$, $y^2 = \frac{81}{16}$, so $|y| = \frac{9}{4}$. The area is $\frac{1}{2} \cdot 8 \cdot \frac{9}{4} = 9$. (Alternatively, $PS + PS' = 10$ and $PS^2 + PS'^2 = 64$ give $PS \cdot PS' = 18$.)",
  r"Forgetting the $\frac{1}{2}$ after computing $PS \cdot PS'$.",
  "U10-E-right-angle-at-P", "Combine the right-angle condition with the ellipse; several routes.",
  check=_c040, values=[9, 18, Rational(9, 2), 5*sqrt(7)], cognitive="Analysis",
  numerical=dict(question=r"$P$ is a point on the ellipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$ such that $\angle SPS' = 90^\circ$, where $S$ and $S'$ are the foci. The area of triangle $SPS'$ is", answer=9))

# ---------------------------------------------------------------- 041
def _c041():
    def count(A, B):
        c2 = A - B
        sols = solve([X**2/A + Y**2/B - 1, X**2 + Y**2 - c2], [X, Y], dict=True)
        return len([t for t in sols if t[X].is_real and t[Y].is_real])
    return (count(25, 16) == 0, count(16, 8) == 2)
q("U10-E-041", TOP_PTS, "Existence of right-angle points", "Difficult", "Statement-based MCQ",
  r"For an ellipse with foci $S$ and $S'$, call a point $P$ on it special if $\angle SPS' = 90^\circ$." "\n"
  r"Statement I: The ellipse $\frac{x^2}{25} + \frac{y^2}{16} = 1$ has no special point." "\n"
  r"Statement II: The ellipse $\frac{x^2}{16} + \frac{y^2}{8} = 1$ has exactly two special points." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Believes every ellipse has four such points, one in each quadrant."),
   (ST_TF, r"Expects four special points whenever any exist, missing that $b = c$ gives only the ends of the minor axis."),
   (ST_FT, r"Believes the circle $x^2 + y^2 = c^2$ always meets the ellipse.")],
  r"$\angle SPS' = 90^\circ$ means $P$ is on the circle $x^2 + y^2 = c^2$. For the first ellipse $c = 3 < b = 4$, so this circle lies inside the ellipse and there is no special point; Statement I is true. For the second, $c^2 = 8 = b^2$, so the circle touches the ellipse only at $(0, \pm 2\sqrt{2})$; exactly two special points, so Statement II is true.",
  r"Not comparing $c$ with $b$ to decide whether the circle on $SS'$ as diameter meets the ellipse.",
  "U10-E-stmt-right-angle", "Reformulate the angle as a circle and compare $c$ with $b$ in two cases.",
  check=_c041, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c042():
    m = Symbol('m', real=True)
    eq = expand(9*X**2 + 16*(1 + m*(X - 2))**2 - 144)
    p = Poly(eq, X)
    ssum = -p.coeff_monomial(X) / p.coeff_monomial(X**2)
    mm = solve(Eq(ssum, 4), m)[0]
    return _ln(-mm, 1, mm*2 - 1)
q("U10-E-042", TOP_INT, "Chord with a given midpoint", "Difficult", "Multi-step computation MCQ",
  r"A chord of the ellipse $\frac{x^2}{16} + \frac{y^2}{9} = 1$ has its midpoint at $(2, 1)$. The equation of the line containing the chord is",
  r"$9x + 8y = 26$",
  [(r"$8x + 9y = 25$", r"Takes the slope as $-\frac{8}{9}$, the reciprocal of the correct slope."),
   (r"$9x - 8y = 10$", r"Sign slip in the sum of roots gives the slope $+\frac{9}{8}$."),
   (r"$32x + 9y = 73$", r"Interchanges $16$ and $9$ in the equation of the ellipse, giving slope $-\frac{32}{9}$.")],
  r"Let the chord be $y - 1 = m(x - 2)$. Substituting into $9x^2 + 16y^2 = 144$ gives $(9 + 16m^2)x^2 + 32m(1 - 2m)x + \dots = 0$. The midpoint condition $x_1 + x_2 = 4$ gives $-32m(1 - 2m) = 4(9 + 16m^2)$, so $-32m = 36$ and $m = -\frac{9}{8}$. The line is $y - 1 = -\frac{9}{8}(x - 2)$, i.e. $9x + 8y = 26$.",
  r"Inverting the slope, or a sign slip in the sum of roots.",
  "U10-E-chord-given-midpoint", "Set up the quadratic with a parameter and use the sum of roots; the $m^2$ terms cancel.",
  check=_c042, values=[_ln(9, 8, -26), _ln(8, 9, -25), _ln(9, -8, -10), _ln(32, 9, -73)], cognitive="Analysis")

# ---------------------------------------------------------------- 043
def _c043():
    xP = Rational(10, 3)
    a = Rational(3 + 7, 2)
    e = (7 - 3) / (2 * xP)     # a + e x - (a - e x) = 2 e x
    b2 = a**2 * (1 - e**2)
    assert b2 * (1 - xP**2 / a**2) > 0
    return 2 * sqrt(b2)
q("U10-E-043", TOP_FOC, "Ellipse from the focal distances of one point", "Difficult", "Multi-step computation MCQ",
  r"An ellipse has its centre at the origin and foci on the $x$-axis. A point $P$ on it has abscissa $\frac{10}{3}$, and the distances of $P$ from the two foci are $3$ and $7$. The length of the minor axis of the ellipse is",
  r"$8$",
  [(r"$6$", r"Finds $c = 3$ and gives the distance between the foci, $2c = 6$."),
   (r"$10$", r"Gives the major axis $PS + PS' = 10$."),
   (r"$2\sqrt{21}$", r"Takes $c = ex_1 = 2$, so $b^2 = 25 - 4 = 21$.")],
  r"$PS + PS' = 10$ gives $a = 5$. Also $PS' - PS = (a + ex) - (a - ex) = 2ex = 4$, so $e \cdot \frac{10}{3} = 2$ and $e = \frac{3}{5}$. Then $c = 3$, $b^2 = 25 - 9 = 16$, and the minor axis is $2b = 8$.",
  r"Confusing $ex_1$ with $c = ae$.",
  "U10-E-ellipse-from-focal-pair", "Use both the sum and the difference of focal distances, then $b$.",
  check=_c043, values=[8, 6, 10, 2*sqrt(21)], cognitive="Analysis",
  numerical=dict(question=r"An ellipse has its centre at the origin and foci on the $x$-axis. A point $P$ on it has abscissa $\frac{10}{3}$, and the distances of $P$ from the two foci are $3$ and $7$. The length of the minor axis of the ellipse is", answer=8))

# ---------------------------------------------------------------- 044
def _c044():
    cc = Symbol('cc', positive=True)
    pts = solve([X**2 + 2*Y**2 - 4, Y - X - cc], [X, Y], dict=True)
    dot = simplify(pts[0][X]*pts[1][X] + pts[0][Y]*pts[1][Y])
    s = [v for v in solve(dot, cc) if v.is_positive]
    return simplify(s[0]**2)
q("U10-E-044", TOP_INT, "Chord subtending a right angle at the centre", "Difficult", "Inverse/parameter MCQ",
  r"The line $y = x + c$ meets the ellipse $x^2 + 2y^2 = 4$ at two points $P$ and $Q$. If $O$ is the origin and $OP \perp OQ$, then $c^2$ equals",
  r"$\frac{8}{3}$",
  [(r"$\frac{8}{7}$", r"Writes $y_1y_2 = x_1x_2 + c^2$, dropping the term $c(x_1 + x_2)$."),
   (r"$\frac{8}{11}$", r"Takes $x_1 + x_2 = +\frac{4c}{3}$ (sign slip) in $y_1y_2 = x_1x_2 + c(x_1 + x_2) + c^2$."),
   (r"$2$", r"Imposes only $x_1x_2 = 0$, forgetting the term $y_1y_2$ in the perpendicularity condition.")],
  r"Substituting: $x^2 + 2(x + c)^2 = 4$, i.e. $3x^2 + 4cx + 2c^2 - 4 = 0$, so $x_1 + x_2 = -\frac{4c}{3}$, $x_1x_2 = \frac{2c^2 - 4}{3}$. Then $y_1y_2 = x_1x_2 + c(x_1 + x_2) + c^2 = \frac{c^2 - 4}{3}$. $OP \perp OQ$ means $x_1x_2 + y_1y_2 = 0$: $\frac{3c^2 - 8}{3} = 0$, so $c^2 = \frac{8}{3}$. The discriminant $48 - 8c^2 > 0$ confirms two real points.",
  r"Expanding $y_1y_2$ incompletely.",
  "U10-E-chord-right-angle-centre", "Vieta on the intersection quadratic plus a perpendicularity condition.",
  check=_c044, values=[Rational(8, 3), Rational(8, 7), Rational(8, 11), 2], cognitive="Analysis",
  numerical=dict(question=r"The line $y = x + c$ meets the ellipse $x^2 + 2y^2 = 4$ at two points $P$ and $Q$. If $O$ is the origin and $OP \perp OQ$, then the value of $3c^2$ is", answer=8))

# ---------------------------------------------------------------- 045
def _c045():
    a, b, c = symbols('a b c', positive=True)
    # S'(-c, 0), L(c, b^2/a), L'(c, -b^2/a): right angle at S'
    cond = (2*c)**2 - (b**2/a)**2
    e = Symbol('ee', positive=True)
    ex = simplify(cond.subs(b, sqrt(a**2 - c**2)).subs(c, e*a) / a**2)
    return [s for s in solve(ex, e) if s < 1][0]
q("U10-E-045", TOP_ECC, "Latus rectum subtending a right angle at the other focus", "Difficult", "Multi-step computation MCQ",
  r"A latus rectum of an ellipse subtends a right angle at the other focus. The eccentricity of the ellipse is",
  r"$\sqrt{2} - 1$",
  [(r"$\frac{\sqrt{5} - 1}{2}$", r"Uses the right angle at the centre: $\frac{b^2}{a} = c$ gives $e^2 + e - 1 = 0$."),
   (r"$\frac{1}{\sqrt{2}}$", r"Takes the right angle at the other focus to mean $b = c$, the condition for a right angle at an end of the minor axis."),
   (r"$3 - 2\sqrt{2}$", r"Solves correctly but reports $e^2 = (\sqrt{2} - 1)^2$.")],
  r"Let the latus rectum through $S(c, 0)$ have ends $(c, \pm\frac{b^2}{a})$, and $S' = (-c, 0)$. By symmetry the right angle at $S'$ means each half makes $45^\circ$, so $\frac{b^2}{a} = 2c$. Then $a^2 - c^2 = 2ac$, i.e. $1 - e^2 = 2e$, so $e^2 + 2e - 1 = 0$ and $e = \sqrt{2} - 1$.",
  r"Measuring the angle from the centre instead of from the other focus.",
  "U10-E-ecc-lr-right-angle", "Geometry turned into a quadratic in $e$.",
  check=_c045, values=[sqrt(2) - 1, (sqrt(5) - 1)/2, 1/sqrt(2), 3 - 2*sqrt(2)], cognitive="Analysis")

# ---------------------------------------------------------------- 046
def _c046():
    d = _ell(16, 7)
    xs = Symbol('xs', real=True)
    x2 = solve(Eq((d["a"] - d["e"]*xs) * (d["a"] + d["e"]*xs), 12), xs)
    v = x2[0]
    y2 = 7 * (1 - v**2 / 16)
    assert y2 > 0
    return simplify(v**2 + y2)
q("U10-E-046", TOP_FOC, "Distance from the centre via the focal product", "Difficult", "Multi-step computation MCQ",
  r"$P$ is a point on the ellipse $\frac{x^2}{16} + \frac{y^2}{7} = 1$ with foci $S$ and $S'$. If $PS \cdot PS' = 12$ and $O$ is the centre, then $OP^2$ equals",
  r"$11$",
  [(r"$4$", r"Uses $OP^2 = a^2 - PS \cdot PS' = 16 - 12$, leaving out $b^2$."),
   (r"$\frac{64}{9}$", r"Finds $x^2 = \frac{64}{9}$ and stops, forgetting the $y^2$ part of $OP^2$."),
   (r"$13$", r"Uses $OP^2 = a^2 + c^2 - PS \cdot PS' = 16 + 9 - 12$.")],
  r"Here $a = 4$, $c = 3$, $e = \frac{3}{4}$. $PS \cdot PS' = a^2 - e^2x^2 = 16 - \frac{9}{16}x^2 = 12$ gives $x^2 = \frac{64}{9}$. Then $y^2 = 7\left(1 - \frac{4}{9}\right) = \frac{35}{9}$, so $OP^2 = \frac{64 + 35}{9} = 11$. (In general $OP^2 = a^2 + b^2 - PS \cdot PS' = 23 - 12$.)",
  r"Computing only the $x$-coordinate and forgetting $y^2$.",
  "U10-E-focal-product-centre", "Focal product formula reversed, then the point on the curve.",
  check=_c046, values=[11, 4, Rational(64, 9), 13], cognitive="Analysis",
  numerical=dict(question=r"$P$ is a point on the ellipse $\frac{x^2}{16} + \frac{y^2}{7} = 1$ with foci $S$ and $S'$. If $PS \cdot PS' = 12$ and $O$ is the centre, then $OP^2$ is", answer=11))

# ---------------------------------------------------------------- 047
def _c047():
    d = _ell(4, 3)
    pts = _meet(X**2/4 + Y**2/3 - 1, Y - (X - d["c"]))
    return simplify(_dist(pts[0], pts[1]))
q("U10-E-047", TOP_INT, "Length of a focal chord", "Difficult", "Multi-step computation MCQ",
  r"A line of slope $1$ through the focus $(1, 0)$ of the ellipse $\frac{x^2}{4} + \frac{y^2}{3} = 1$ meets the ellipse at $P$ and $Q$. The length $PQ$ is",
  r"$\frac{24}{7}$",
  [(r"$\frac{32}{7}$", r"Uses $PQ = 2a + e(x_1 + x_2)$, taking $a + ex$ for the distance from the focus $(1, 0)$."),
   (r"$\frac{12\sqrt{2}}{7}$", r"Takes $|x_1 - x_2| = \frac{12\sqrt{2}}{7}$ as the chord length, without the factor $\sqrt{2}$."),
   (r"$\frac{20}{7}$", r"Uses $PQ = 2a - (x_1 + x_2)$, leaving out the factor $e$.")],
  r"Here $a = 2$, $e = \frac{1}{2}$. The line $y = x - 1$ gives $3x^2 + 4(x - 1)^2 = 12$, i.e. $7x^2 - 8x - 8 = 0$, so $x_1 + x_2 = \frac{8}{7}$. Since the chord passes through the focus, $PQ = PS + SQ = (a - ex_1) + (a - ex_2) = 4 - \frac{1}{2} \cdot \frac{8}{7} = \frac{24}{7}$.",
  r"Using the wrong sign in the focal distance formula.",
  "U10-E-focal-chord", "Intersection quadratic combined with focal distances.",
  check=_c047, values=[Rational(24, 7), Rational(32, 7), 12*sqrt(2)/7, Rational(20, 7)], cognitive="Analysis",
  numerical=dict(question=r"A line of slope $1$ through the focus $(1, 0)$ of the ellipse $\frac{x^2}{4} + \frac{y^2}{3} = 1$ meets the ellipse at $P$ and $Q$. Then the value of $7 \cdot PQ$ is", answer=24))

# ---------------------------------------------------------------- 048
def _c048():
    n = 0
    for c in range(-20, 21):
        eq = expand(X**2/4 + (2*X + c)**2 - 1)
        if len([r for r in Poly(eq * 4, X).real_roots()]) == 2 and len(set(Poly(eq * 4, X).real_roots())) == 2:
            n += 1
    return n
q("U10-E-048", TOP_INT, "Integer intercepts giving two intersection points", "Difficult", "Multi-step computation MCQ",
  r"The number of integer values of $c$ for which the line $y = 2x + c$ meets the ellipse $\frac{x^2}{4} + y^2 = 1$ at two distinct points is",
  r"$9$",
  [(r"$7$", r"Uses $c^2 < a^2m^2 - b^2 = 15$."),
   (r"$5$", r"Uses $c^2 < a^2 + b^2m^2 = 8$, swapping the roles of $a^2$ and $b^2$."),
   (r"$1$", r"Drops the cross term when expanding, writing $(2x + c)^2 = 4x^2 + c^2$; then $17x^2 + 4c^2 - 4 = 0$ has two distinct roots only for $c^2 < 1$, i.e. $c = 0$.")],
  r"Substituting: $x^2 + 4(2x + c)^2 = 4$, i.e. $17x^2 + 16cx + 4c^2 - 4 = 0$. Two distinct points need $256c^2 - 68(4c^2 - 4) > 0$, i.e. $272 - 16c^2 > 0$, so $c^2 < 17$. The integers are $c = -4, \dots, 4$, which is $9$ values.",
  r"Misremembering the intersection condition, or dropping the cross term when substituting the line.",
  "U10-E-count-intercepts", "Discriminant inequality, then counting integers including $0$ and negatives.",
  check=_c048, values=[9, 7, 5, 1], cognitive="Analysis",
  numerical=dict(question=r"The number of integer values of $c$ for which the line $y = 2x + c$ meets the ellipse $\frac{x^2}{4} + y^2 = 1$ at two distinct points is", answer=9))

# ---------------------------------------------------------------- 049
def _c049():
    a = Symbol('a', positive=True)
    c = 4
    b2 = a**2 - c**2
    s = [v for v in solve(Eq(b2 / a, Rational(9, 5)), a) if v > c][0]
    return Rational(c) / s
q("U10-E-049", TOP_ECC, "Eccentricity from the ends of a latus rectum", "Difficult", "Inverse/parameter MCQ",
  r"The ends of one latus rectum of the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ $(a > b)$ are $\left(4, \pm\frac{9}{5}\right)$. The eccentricity of the ellipse is",
  r"$\frac{4}{5}$",
  [(r"$\frac{3}{5}$", r"Finds $a = 5$, $b = 3$ and gives $\frac{b}{a}$."),
   (r"$\frac{16}{25}$", r"Finds $e = \frac{4}{5}$ and reports $e^2$."),
   (r"$\frac{9}{25}$", r"Computes $\frac{b^2/a}{a} = \frac{b^2}{a^2} = 1 - e^2 = \frac{9}{25}$ and reports it as $e$.")],
  r"The latus rectum is $x = c$ with half-length $\frac{b^2}{a}$, so $c = 4$ and $\frac{b^2}{a} = \frac{9}{5}$. With $b^2 = a^2 - 16$: $5a^2 - 9a - 80 = 0$, so $(a - 5)(5a + 16) = 0$ and $a = 5$. Hence $e = \frac{c}{a} = \frac{4}{5}$.",
  r"Reporting $\frac{b}{a}$ or $1 - e^2$ for the eccentricity.",
  "U10-E-ecc-from-lr-ends", "Two pieces of data from the end points, a quadratic in $a$, then $e$.",
  check=_c049, values=[Rational(4, 5), Rational(3, 5), Rational(16, 25), Rational(9, 25)], cognitive="Analysis")

# ---------------------------------------------------------------- 050
def _c050():
    b = Symbol('b', positive=True)
    a1 = 13
    c1 = sqrt(a1**2 - b**2)
    # E2: foci (0, +-b), minor axis ends (+-c1, 0): semi-minor c1, semi-major a2 = sqrt(c1^2 + b^2), e2 = b / a2
    a2 = sqrt(c1**2 + b**2)
    bs = [v for v in solve(Eq(b / a2, Rational(12, 13)), b) if 0 < v < a1]
    assert len(bs) == 1
    A2, B2 = simplify(a2.subs(b, bs[0])), simplify(c1.subs(b, bs[0]))
    assert A2 > B2
    return simplify(2 * B2**2 / A2)
q("U10-E-050", TOP_ECC, "Two ellipses sharing axes data", "Difficult", "Multi-step computation MCQ",
  r"$E_1$ is the ellipse $\frac{x^2}{169} + \frac{y^2}{b^2} = 1$ with $0 < b < 13$. $E_2$ is an ellipse centred at the origin whose foci are the ends of the minor axis of $E_1$ and whose minor axis has the foci of $E_1$ as its ends. If the eccentricity of $E_2$ is $\frac{12}{13}$, then the length of the latus rectum of $E_2$ is",
  r"$\frac{50}{13}$",
  [(r"$\frac{288}{13}$", r"Finds $b = 12$ and then gives the latus rectum of $E_1$, $\frac{2b^2}{13} = \frac{288}{13}$, instead of that of $E_2$."),
   (r"$\frac{25}{13}$", r"Finds the semi-axes $13$ and $5$ of $E_2$ correctly but gives the semi-latus rectum $\frac{25}{13}$."),
   (r"$\frac{338}{5}$", r"Swaps the roles of the semi-axes of $E_2$ in the formula: $\frac{2 \cdot 13^2}{5}$.")],
  r"For $E_1$, $a_1 = 13$ and $c_1^2 = 169 - b^2$. $E_2$ has semi-minor axis $c_1$ (on the $x$-axis) and focal distance $b$ (on the $y$-axis), so its semi-major axis is $\sqrt{c_1^2 + b^2} = 13$. Then $e_2 = \frac{b}{13} = \frac{12}{13}$ gives $b = 12$ and $c_1 = 5$. So $E_2$ is $\frac{x^2}{25} + \frac{y^2}{169} = 1$, and its latus rectum is $\frac{2 \cdot 5^2}{13} = \frac{50}{13}$.",
  r"Not seeing that the semi-major axis of $E_2$ equals that of $E_1$, or answering for the wrong ellipse.",
  "U10-E-two-ellipses-lr", r"Translate the description of $E_2$, see that its semi-major axis is $13$, find $b$, then the latus rectum of $E_2$.",
  check=_c050, values=[Rational(50, 13), Rational(288, 13), Rational(25, 13), Rational(338, 5)], cognitive="Analysis",
  numerical=dict(question=r"$E_1$ is the ellipse $\frac{x^2}{169} + \frac{y^2}{b^2} = 1$ with $0 < b < 13$. $E_2$ is an ellipse centred at the origin whose foci are the ends of the minor axis of $E_1$ and whose minor axis has the foci of $E_1$ as its ends. If the eccentricity of $E_2$ is $\frac{12}{13}$ and $\ell$ is the length of the latus rectum of $E_2$, then $13\ell$ is", answer=50))
