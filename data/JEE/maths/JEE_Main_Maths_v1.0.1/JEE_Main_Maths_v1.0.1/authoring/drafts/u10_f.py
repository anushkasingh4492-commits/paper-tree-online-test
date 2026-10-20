import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools

X, Y = symbols('x y', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STV = [(True, True), (False, False), (True, False), (False, True)]
TOP_STD = "Hyperbola: standard forms"
TOP_SHIFT = "Hyperbola: shifted standard forms"
TOP_EQN = "Hyperbola: equation from data"
TOP_FOC = "Hyperbola: focal distances"
TOP_ASY = "Hyperbola: asymptotes"
TOP_CONJ = "Hyperbola: conjugate and rectangular hyperbolas"
TOP_ID = "Identifying conics"


def _ln(a, b, c):
    """Line a x + b y + c = 0 as a normalised coefficient Tuple."""
    a, b, c = sympify(a), sympify(b), sympify(c)
    lead = a if a != 0 else b
    return Tuple(*[simplify(v / lead) for v in (a, b, c)])


def _pm(m, h=0, k=0):
    """The pair of lines y - k = +/- m (x - h) as a FiniteSet."""
    m, h, k = sympify(m), sympify(h), sympify(k)
    return FiniteSet(_ln(m, -1, k - m*h), _ln(-m, -1, k + m*h))


def _key(expr):
    """Canonical coefficient tuple of a second-degree curve expr = 0."""
    p = Poly(expand(expr), X, Y)
    mons = [X**2, X*Y, Y**2, X, Y, Integer(1)]
    cs = [p.coeff_monomial(m) for m in mons]
    lead = [c for c in cs if c != 0][0]
    return tuple(simplify(c / lead) for c in cs)


def _hyp(expr):
    """Data of an axis-parallel hyperbola expr = 0 (no xy term), by completing squares."""
    p = Poly(expand(expr), X, Y)
    A, C = p.coeff_monomial(X**2), p.coeff_monomial(Y**2)
    D, E = p.coeff_monomial(X), p.coeff_monomial(Y)
    assert A * C < 0
    h, k = -D / (2*A), -E / (2*C)
    K = expand(expr).subs({X: h, Y: k})
    px, py = -K / A, -K / C          # (x-h)^2/px + (y-k)^2/py = 1
    if px > 0:
        ax, a2, b2 = 'x', px, -py
    else:
        ax, a2, b2 = 'y', py, -px
    a, b = sqrt(a2), sqrt(b2)
    c = sqrt(a2 + b2)
    e = c / a
    if ax == 'x':
        foci = FiniteSet(Tuple(h + c, k), Tuple(h - c, k))
        verts = FiniteSet(Tuple(h + a, k), Tuple(h - a, k))
        dirs = FiniteSet(_ln(1, 0, -(h + a/e)), _ln(1, 0, -(h - a/e)))
        asy = _pm(b/a, h, k)
    else:
        foci = FiniteSet(Tuple(h, k + c), Tuple(h, k - c))
        verts = FiniteSet(Tuple(h, k + a), Tuple(h, k - a))
        dirs = FiniteSet(_ln(0, 1, -(k + a/e)), _ln(0, 1, -(k - a/e)))
        asy = _pm(a/b, h, k)
    return dict(axis=ax, centre=(h, k), a=a, b=b, c=c, e=simplify(e), foci=foci, vertices=verts,
                directrices=dirs, asymptotes=asy, lr=simplify(2*b2/a))


def _dist(P, Q):
    return sqrt((P[0] - Q[0])**2 + (P[1] - Q[1])**2)


def _pts(P):
    return FiniteSet(*[Tuple(*t) for t in P])


# ================================================================ EASY
# ---------------------------------------------------------------- 001
q("U10-F-001", TOP_STD, "Eccentricity of a standard hyperbola", "Easy", "Single-step computation MCQ",
  r"The eccentricity of the hyperbola $\frac{x^2}{16} - \frac{y^2}{9} = 1$ is",
  r"$\frac{5}{4}$",
  [(r"$\frac{5}{3}$", r"Uses $e^2 = 1 + \frac{a^2}{b^2} = 1 + \frac{16}{9}$, swapping the roles of $a$ and $b$."),
   (r"$\frac{25}{16}$", r"Stops at $e^2 = 1 + \frac{9}{16} = \frac{25}{16}$ and reports $e^2$ as $e$."),
   (r"$\frac{\sqrt{7}}{2}$", r"Uses $e^2 = 1 + \frac{b}{a} = 1 + \frac{3}{4}$, with the ratio of the semi-axes in place of the ratio of their squares.")],
  r"Here $a^2 = 16$, $b^2 = 9$. For a hyperbola $e^2 = 1 + \frac{b^2}{a^2} = 1 + \frac{9}{16} = \frac{25}{16}$, so $e = \frac{5}{4}$.",
  r"Swapping $a$ and $b$ in $e^2 = 1 + \frac{b^2}{a^2}$, or reporting $e^2$.",
  "U10-F-ecc-basic", "One formula applied once.",
  check=lambda: _hyp(X**2/16 - Y**2/9 - 1)["e"],
  values=[Rational(5, 4), Rational(5, 3), Rational(25, 16), sqrt(7)/2], cognitive="Recall")

# ---------------------------------------------------------------- 002
def _c002():
    F = list(_hyp(5*X**2 - 4*Y**2 - 20)["foci"])
    return _dist(F[0], F[1])
q("U10-F-002", TOP_STD, "Distance between the foci after reducing to standard form", "Easy", "Single-step computation MCQ",
  r"The distance between the foci of the hyperbola $5x^2 - 4y^2 = 20$ is",
  r"$6$",
  [(r"$2$", r"Uses the ellipse relation $c^2 = |a^2 - b^2| = 5 - 4 = 1$, giving $2c = 2$."),
   (r"$4$", r"Gives the length $2a$ of the transverse axis, the distance between the vertices."),
   (r"$3$", r"Finds $c = 3$ and reports it in place of $2c$.")],
  r"Dividing by $20$: $\frac{x^2}{4} - \frac{y^2}{5} = 1$, so $a^2 = 4$, $b^2 = 5$ and $c^2 = a^2 + b^2 = 9$. The foci are $(\pm 3, 0)$, so they are $2c = 6$ apart.",
  r"Using the ellipse relation $c^2 = a^2 - b^2$ for a hyperbola, or stopping at $c$.",
  "U10-F-focal-separation", r"Reduce to standard form, then $c^2 = a^2 + b^2$ and double.",
  check=_c002, values=[6, 2, 4, 3], cognitive="Application",
  numerical=dict(question=r"The distance between the foci of the hyperbola $5x^2 - 4y^2 = 20$ is", answer=6))

# ---------------------------------------------------------------- 003
q("U10-F-003", TOP_STD, "Length of latus rectum", "Easy", "Single-step computation MCQ",
  r"The length of the latus rectum of the hyperbola $\frac{x^2}{9} - \frac{y^2}{4} = 1$ is",
  r"$\frac{8}{3}$",
  [(r"$9$", r"Uses $\frac{2a^2}{b} = \frac{18}{2}$, interchanging $a$ and $b$ in the formula."),
   (r"$\frac{4}{3}$", r"Uses $\frac{b^2}{a}$, which is only half the latus rectum."),
   (r"$\frac{8}{9}$", r"Divides $2b^2$ by $a^2 = 9$ in place of $a = 3$.")],
  r"Here $a = 3$, $b^2 = 4$. The latus rectum has length $\frac{2b^2}{a} = \frac{8}{3}$.",
  r"Interchanging $a$ and $b$ in $\frac{2b^2}{a}$ or taking only the semi-latus rectum.",
  "U10-F-lr-basic", r"Direct use of $\frac{2b^2}{a}$.",
  check=lambda: _hyp(X**2/9 - Y**2/4 - 1)["lr"],
  values=[Rational(8, 3), 9, Rational(4, 3), Rational(8, 9)], cognitive="Recall")

# ---------------------------------------------------------------- 004
q("U10-F-004", TOP_STD, "Directrices of a standard hyperbola", "Easy", "Single-step computation MCQ",
  r"The directrices of the hyperbola $\frac{x^2}{25} - \frac{y^2}{144} = 1$ are",
  r"$x = \pm\frac{25}{13}$",
  [(r"$x = \pm\frac{25}{12}$", r"Uses $\frac{a^2}{b} = \frac{25}{12}$ in place of $\frac{a^2}{c}$."),
   (r"$y = \pm\frac{25}{13}$", r"Gets $\frac{a}{e}$ right but writes the directrices perpendicular to the $y$-axis."),
   (r"$x = \pm\frac{5}{13}$", r"Uses $x = \pm\frac{a}{c}$, dividing $a$ by $c$ instead of by $e = \frac{c}{a}$.")],
  r"$a = 5$, $b = 12$, $c = \sqrt{25 + 144} = 13$, so $e = \frac{13}{5}$. The directrices are $x = \pm\frac{a}{e} = \pm\frac{25}{13}$.",
  r"Dividing by $c$ or by $b$ instead of by $e$.",
  "U10-F-directrix", r"One relation $x = \pm\frac{a}{e}$ after finding $e$.",
  check=lambda: _hyp(X**2/25 - Y**2/144 - 1)["directrices"],
  values=[FiniteSet(_ln(1, 0, -Rational(25, 13)), _ln(1, 0, Rational(25, 13))),
          FiniteSet(_ln(1, 0, -Rational(25, 12)), _ln(1, 0, Rational(25, 12))),
          FiniteSet(_ln(0, 1, -Rational(25, 13)), _ln(0, 1, Rational(25, 13))),
          FiniteSet(_ln(1, 0, -Rational(5, 13)), _ln(1, 0, Rational(5, 13)))],
  cognitive="Application")

# ---------------------------------------------------------------- 005
q("U10-F-005", TOP_ASY, "Asymptotes of a standard hyperbola", "Easy", "Single-step computation MCQ",
  r"The asymptotes of the hyperbola $\frac{x^2}{4} - \frac{y^2}{25} = 1$ are",
  r"$y = \pm\frac{5}{2}x$",
  [(r"$y = \pm\frac{2}{5}x$", r"Uses slopes $\pm\frac{a}{b}$, interchanging the semi-axes."),
   (r"$y = \pm\frac{25}{4}x$", r"Uses slopes $\pm\frac{b^2}{a^2}$, the ratio of the denominators."),
   (r"$y = \pm\frac{\sqrt{29}}{2}x$", r"Uses slopes $\pm\frac{c}{a} = \pm e$.")],
  r"For $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ the asymptotes are $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 0$, that is $y = \pm\frac{b}{a}x$. With $a = 2$, $b = 5$ they are $y = \pm\frac{5}{2}x$.",
  r"Using $\frac{a}{b}$ or $\frac{b^2}{a^2}$ as the slope of an asymptote.",
  "U10-F-asymptote-std", "One standard result.",
  check=lambda: _hyp(X**2/4 - Y**2/25 - 1)["asymptotes"],
  values=[_pm(Rational(5, 2)), _pm(Rational(2, 5)), _pm(Rational(25, 4)), _pm(sqrt(29)/2)], cognitive="Recall")

# ---------------------------------------------------------------- 006
def _c006():
    h = X**2/144 - Y**2/25 - 1
    conj = -(h + 1) - 1          # y^2/25 - x^2/144 = 1
    return _hyp(conj)["e"]
q("U10-F-006", TOP_CONJ, "Eccentricity of the conjugate hyperbola", "Easy", "Single-step computation MCQ",
  r"The eccentricity of the hyperbola conjugate to $\frac{x^2}{144} - \frac{y^2}{25} = 1$ is",
  r"$\frac{13}{5}$",
  [(r"$\frac{13}{12}$", r"Gives the eccentricity of the given hyperbola itself."),
   (r"$\frac{169}{25}$", r"Reports $e'^2 = 1 + \frac{144}{25}$ as the eccentricity."),
   (r"$\frac{\sqrt{85}}{5}$", r"Uses $e'^2 = 1 + \frac{12}{5}$, the ratio of the semi-axes in place of the ratio of their squares.")],
  r"The conjugate hyperbola is $\frac{y^2}{25} - \frac{x^2}{144} = 1$, whose transverse semi-axis is $5$ and conjugate semi-axis is $12$. So $e'^2 = 1 + \frac{144}{25} = \frac{169}{25}$ and $e' = \frac{13}{5}$.",
  r"Believing a hyperbola and its conjugate have the same eccentricity.",
  "U10-F-conjugate-ecc", "Write the conjugate and apply one formula.",
  check=_c006, values=[Rational(13, 5), Rational(13, 12), Rational(169, 25), sqrt(85)/5], cognitive="Understanding")

# ---------------------------------------------------------------- 007
q("U10-F-007", TOP_CONJ, "Foci of a rectangular hyperbola", "Easy", "Single-step computation MCQ",
  r"The foci of the rectangular hyperbola $x^2 - y^2 = 8$ are",
  r"$(\pm 4, 0)$",
  [(r"$(\pm 2\sqrt{2}, 0)$", r"Gives the vertices $(\pm a, 0)$ with $a = 2\sqrt{2}$."),
   (r"$(0, \pm 4)$", r"Finds $c = 4$ but places the foci on the $y$-axis."),
   (r"$(\pm 2, 0)$", r"Takes $c = \frac{a}{\sqrt{2}}$, dividing by $e = \sqrt{2}$ instead of multiplying.")],
  r"$\frac{x^2}{8} - \frac{y^2}{8} = 1$, so $a^2 = b^2 = 8$, $c^2 = 16$ and $c = 4$ (equivalently $e = \sqrt{2}$, $c = ae = 2\sqrt{2}\cdot\sqrt{2}$). The foci are $(\pm 4, 0)$.",
  r"Confusing the vertices with the foci, or using $c = \frac{a}{e}$.",
  "U10-F-rect-basic", "One relation $c^2 = 2a^2$.",
  check=lambda: _hyp(X**2 - Y**2 - 8)["foci"],
  values=[_pts([(4, 0), (-4, 0)]), _pts([(2*sqrt(2), 0), (-2*sqrt(2), 0)]), _pts([(0, 4), (0, -4)]), _pts([(2, 0), (-2, 0)])],
  cognitive="Application")

# ---------------------------------------------------------------- 008
def _c008():
    P = (10, sqrt(64*(Rational(100, 36) - 1)))
    assert simplify(P[0]**2/36 - P[1]**2/64 - 1) == 0
    F = list(_hyp(X**2/36 - Y**2/64 - 1)["foci"])
    return Abs(simplify(_dist(P, F[0]) - _dist(P, F[1])))
q("U10-F-008", TOP_FOC, "Difference of focal distances", "Easy", "Single-step computation MCQ",
  r"$P$ is any point on the hyperbola $\frac{x^2}{36} - \frac{y^2}{64} = 1$, and $S$, $S'$ are its foci. Then $|PS - PS'|$ equals",
  r"$12$",
  [(r"$20$", r"Gives the distance $2c$ between the foci."),
   (r"$16$", r"Gives the length $2b$ of the conjugate axis."),
   (r"$6$", r"Uses $a$ in place of $2a$.")],
  r"For every point of a hyperbola the difference of focal distances equals the length of the transverse axis, $2a$. Here $a = 6$, so $|PS - PS'| = 12$.",
  r"Using $2c$ or $2b$ in place of $2a$.",
  "U10-F-focal-diff", "One defining property.",
  check=_c008, values=[12, 20, 16, 6], cognitive="Recall",
  numerical=dict(question=r"$P$ is any point on the hyperbola $\frac{x^2}{36} - \frac{y^2}{64} = 1$, and $S$, $S'$ are its foci. The value of $|PS - PS'|$ is", answer=12))

# ---------------------------------------------------------------- 009
def _c009():
    d = _hyp(5*Y**2 - 3*X**2 - 15)
    return (1 if d["axis"] == 'y' else 0, 2*d["a"])
q("U10-F-009", TOP_ID, "Orientation and transverse axis from the equation", "Easy", "Conceptual/application MCQ",
  r"The equation $5y^2 - 3x^2 = 15$ represents",
  r"a hyperbola with transverse axis along the $y$-axis, of length $2\sqrt{3}$",
  [(r"a hyperbola with transverse axis along the $x$-axis, of length $2\sqrt{5}$", r"Picks the axis carrying the larger denominator $5$ in $\frac{y^2}{3} - \frac{x^2}{5} = 1$, ignoring which term is positive."),
   (r"a hyperbola with transverse axis along the $y$-axis, of length $2\sqrt{5}$", r"Gets the axis right but uses the denominator $5$ of $x^2$ for the transverse semi-axis."),
   (r"a hyperbola with transverse axis along the $x$-axis, of length $2\sqrt{3}$", r"Uses the right semi-axis $\sqrt{3}$ but attaches it to the $x$-axis by habit from the form $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$.")],
  r"Dividing by $15$: $\frac{y^2}{3} - \frac{x^2}{5} = 1$. The positive term is in $y$, so the transverse axis is along the $y$-axis with semi-axis $\sqrt{3}$; its length is $2\sqrt{3}$.",
  r"Deciding the transverse axis from the larger denominator instead of from the positive term.",
  "U10-F-identify-orientation", "Reduce and read off the positive term.",
  check=_c009, values=[(1, 2*sqrt(3)), (0, 2*sqrt(5)), (1, 2*sqrt(5)), (0, 2*sqrt(3))], cognitive="Understanding")

# ---------------------------------------------------------------- 010
def _c010():
    a, c = 3, 5
    return _key(X**2/a**2 - Y**2/(c**2 - a**2) - 1)
q("U10-F-010", TOP_EQN, "Equation from vertices and foci", "Easy", "Single-step computation MCQ",
  r"The hyperbola with vertices $(\pm 3, 0)$ and foci $(\pm 5, 0)$ has equation",
  r"$\frac{x^2}{9} - \frac{y^2}{16} = 1$",
  [(r"$\frac{x^2}{9} - \frac{y^2}{25} = 1$", r"Takes $b = c = 5$."),
   (r"$\frac{x^2}{16} - \frac{y^2}{9} = 1$", r"Finds $b^2 = 16$ but puts it under $x^2$, interchanging $a^2$ and $b^2$."),
   (r"$\frac{x^2}{9} - \frac{y^2}{34} = 1$", r"Uses $b^2 = a^2 + c^2 = 9 + 25$.")],
  r"$a = 3$ and $c = 5$, so $b^2 = c^2 - a^2 = 16$. The transverse axis is the $x$-axis, giving $\frac{x^2}{9} - \frac{y^2}{16} = 1$.",
  r"Using $b^2 = a^2 + c^2$ or $b = c$.",
  "U10-F-eqn-vertex-focus", "One relation $b^2 = c^2 - a^2$.",
  check=_c010, values=[_key(X**2/9 - Y**2/16 - 1), _key(X**2/9 - Y**2/25 - 1), _key(X**2/16 - Y**2/9 - 1), _key(X**2/9 - Y**2/34 - 1)],
  cognitive="Application")

# ---------------------------------------------------------------- 011
q("U10-F-011", TOP_STD, "Foci when the transverse axis is vertical", "Easy", "Single-step computation MCQ",
  r"The foci of the hyperbola $\frac{y^2}{9} - \frac{x^2}{27} = 1$ are",
  r"$(0, \pm 6)$",
  [(r"$(\pm 6, 0)$", r"Finds $c = 6$ but places the foci on the $x$-axis."),
   (r"$(0, \pm 3\sqrt{2})$", r"Uses $c^2 = 27 - 9$, subtracting the denominators as for an ellipse."),
   (r"$(0, \pm 3\sqrt{3})$", r"Takes $c$ equal to the conjugate semi-axis $\sqrt{27}$.")],
  r"The positive term is in $y$, so the transverse axis is the $y$-axis with $a^2 = 9$, $b^2 = 27$. Then $c^2 = 9 + 27 = 36$ and the foci are $(0, \pm 6)$.",
  r"Placing the foci on the $x$-axis by habit.",
  "U10-F-foci-basic", "Orientation plus one relation.",
  check=lambda: _hyp(Y**2/9 - X**2/27 - 1)["foci"],
  values=[_pts([(0, 6), (0, -6)]), _pts([(6, 0), (-6, 0)]), _pts([(0, 3*sqrt(2)), (0, -3*sqrt(2))]), _pts([(0, 3*sqrt(3)), (0, -3*sqrt(3))])],
  cognitive="Application")

# ---------------------------------------------------------------- 012
def _c012():
    a2 = Symbol('a2', positive=True)
    return solve(Eq(1 + 45/a2, Rational(3, 2)**2), a2)[0]
q("U10-F-012", TOP_EQN, "Transverse semi-axis from eccentricity", "Easy", "Inverse/parameter MCQ",
  r"If the eccentricity of the hyperbola $\frac{x^2}{a^2} - \frac{y^2}{45} = 1$ is $\frac{3}{2}$, then $a^2$ equals",
  r"$36$",
  [(r"$90$", r"Uses $e = 1 + \frac{b^2}{a^2}$ without squaring $e$: $\frac{45}{a^2} = \frac{1}{2}$."),
   (r"$\frac{225}{4}$", r"Inverts the relation, writing $a^2 = b^2(e^2 - 1) = 45 \cdot \frac{5}{4}$."),
   (r"$6$", r"Finds $a = 6$ and reports it as $a^2$.")],
  r"$e^2 = 1 + \frac{b^2}{a^2}$ gives $\frac{9}{4} = 1 + \frac{45}{a^2}$, so $\frac{45}{a^2} = \frac{5}{4}$ and $a^2 = 36$.",
  r"Dropping the square on $e$ or inverting $b^2 = a^2(e^2 - 1)$.",
  "U10-F-transverse-from-ecc", "One relation rearranged for the transverse semi-axis.",
  check=_c012, values=[36, 90, Rational(225, 4), 6], cognitive="Application",
  numerical=dict(question=r"If the eccentricity of the hyperbola $\frac{x^2}{a^2} - \frac{y^2}{45} = 1$ is $\frac{3}{2}$, then the value of $a^2$ is", answer=36))

# ---------------------------------------------------------------- 013
q("U10-F-013", TOP_STD, "Latus rectum with vertical transverse axis", "Easy", "Single-step computation MCQ",
  r"The length of the latus rectum of the hyperbola $\frac{y^2}{16} - \frac{x^2}{9} = 1$ is",
  r"$\frac{9}{2}$",
  [(r"$\frac{32}{3}$", r"Takes the transverse semi-axis as $3$ from the $x^2$ term, giving $\frac{2 \cdot 16}{3}$."),
   (r"$\frac{9}{4}$", r"Uses $\frac{b^2}{a}$, half the latus rectum."),
   (r"$\frac{3}{2}$", r"Uses $\frac{2b}{a} = \frac{6}{4}$, with $b$ in place of $b^2$.")],
  r"The positive term is in $y$, so the transverse semi-axis is $a = 4$ and the conjugate semi-axis is $b = 3$. The latus rectum is $\frac{2b^2}{a} = \frac{18}{4} = \frac{9}{2}$.",
  r"Taking $a$ from the $x^2$ term regardless of orientation.",
  "U10-F-lr-basic", "Orientation plus one formula.",
  check=lambda: _hyp(Y**2/16 - X**2/9 - 1)["lr"],
  values=[Rational(9, 2), Rational(32, 3), Rational(9, 4), Rational(3, 2)], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    d = _hyp(16*Y**2 - 9*X**2 - 576)
    F = list(d["foci"]); V = list(d["vertices"])
    return min(_dist(F[0], v) for v in V)
q("U10-F-014", TOP_STD, "Focus to nearer vertex, vertical transverse axis", "Easy", "Single-step computation MCQ",
  r"The distance from a focus of the hyperbola $16y^2 - 9x^2 = 576$ to the nearer vertex is",
  r"$4$",
  [(r"$16$", r"Gives $c + a = 10 + 6$, the distance to the farther vertex."),
   (r"$2$", r"Takes the semi-transverse axis as $8$ (from the larger denominator $64$) and gives $c - 8 = 10 - 8$."),
   (r"$8 - 2\sqrt{7}$", r"Takes the semi-transverse axis as $8$ and uses the ellipse relation $c^2 = 64 - 36 = 28$, giving $8 - 2\sqrt{7}$.")],
  r"Dividing by $576$: $\frac{y^2}{36} - \frac{x^2}{64} = 1$, so the transverse axis is the $y$-axis with $a = 6$, $b = 8$ and $c = \sqrt{36 + 64} = 10$. The focus $(0, 10)$ is nearest to the vertex $(0, 6)$, at distance $c - a = 4$.",
  r"Treating the larger denominator as $a^2$ instead of reading the orientation from the positive term.",
  "U10-F-focus-vertex-gap", "Reduce to standard form, read the orientation, then $c - a$.",
  check=_c014, values=[4, 16, 2, 8 - 2*sqrt(7)], cognitive="Application",
  numerical=dict(question=r"The distance from a focus of the hyperbola $16y^2 - 9x^2 = 576$ to the nearer vertex is", answer=4))

# ---------------------------------------------------------------- 015
def _c015():
    d = _hyp(X**2/64 - Y**2/36 - 1)
    xs = [-l[2] for l in d["directrices"]]
    return Abs(xs[0] - xs[1])
q("U10-F-015", TOP_STD, "Distance between the directrices", "Easy", "Single-step computation MCQ",
  r"The distance between the directrices of the hyperbola $\frac{x^2}{64} - \frac{y^2}{36} = 1$ is",
  r"$\frac{64}{5}$",
  [(r"$20$", r"Gives the distance $2ae$ between the foci."),
   (r"$16$", r"Gives the length $2a$ of the transverse axis."),
   (r"$\frac{32}{5}$", r"Gives $\frac{a}{e}$, the distance of one directrix from the centre.")],
  r"$a = 8$, $c = \sqrt{64 + 36} = 10$, $e = \frac{5}{4}$. The directrices are $x = \pm\frac{a}{e} = \pm\frac{32}{5}$, so they are $\frac{2a}{e} = \frac{64}{5}$ apart.",
  r"Confusing $\frac{2a}{e}$ with $2ae$.",
  "U10-F-directrix", "Two short steps.",
  check=_c015, values=[Rational(64, 5), 20, 16, Rational(32, 5)], cognitive="Application")

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 016
def _c016():
    S, S2, P = (6, 0), (-6, 0), (6, Rational(11, 5))
    a = Abs(_dist(P, S) - _dist(P, S2)) / 2
    return _key(X**2/a**2 - Y**2/(36 - a**2) - 1)
q("U10-F-016", TOP_EQN, "Equation from foci and a point", "Medium", "Multi-step computation MCQ",
  r"A hyperbola has foci $(\pm 6, 0)$ and passes through the point $P\left(6, \frac{11}{5}\right)$. Its equation is",
  r"$\frac{x^2}{25} - \frac{y^2}{11} = 1$",
  [(r"$\frac{x^2}{11} - \frac{y^2}{25} = 1$", r"Finds $a^2 = 25$, $b^2 = 11$ and then interchanges them."),
   (r"$\frac{x^2}{25} - \frac{y^2}{36} = 1$", r"Finds $a = 5$ but takes $b = c = 6$."),
   (r"$\frac{x^2}{25} - \frac{y^2}{61} = 1$", r"Finds $a = 5$ but uses $b^2 = a^2 + c^2$.")],
  r"$PS = \frac{11}{5}$ and $PS' = \sqrt{144 + \frac{121}{25}} = \frac{61}{5}$, so $2a = |PS - PS'| = 10$ and $a = 5$. Then $b^2 = c^2 - a^2 = 36 - 25 = 11$, giving $\frac{x^2}{25} - \frac{y^2}{11} = 1$.",
  r"Mishandling $b^2 = c^2 - a^2$ after finding $a$.",
  "U10-F-eqn-focal-diff", "Two focal distances, then the relation for $b^2$.",
  check=_c016, values=[_key(X**2/25 - Y**2/11 - 1), _key(X**2/11 - Y**2/25 - 1), _key(X**2/25 - Y**2/36 - 1), _key(X**2/25 - Y**2/61 - 1)])

# ---------------------------------------------------------------- 017
def _c017():
    a, b, e = symbols('a b e', positive=True)
    bs = solve(Eq(2*b**2/a, a), b)[0]
    return simplify(sqrt(1 + bs**2/a**2))
q("U10-F-017", TOP_STD, "Eccentricity from a latus rectum condition", "Medium", "Inverse/parameter MCQ",
  r"The length of the latus rectum of a hyperbola is half the length of its transverse axis. The eccentricity of the hyperbola is",
  r"$\frac{\sqrt{6}}{2}$",
  [(r"$\sqrt{2}$", r"Equates the latus rectum $\frac{2b^2}{a}$ to the full transverse axis $2a$, giving $b = a$."),
   (r"$\frac{\sqrt{5}}{2}$", r"Equates $\frac{2b^2}{a}$ to $\frac{a}{2}$, half of the semi-transverse axis, giving $b^2 = \frac{a^2}{4}$."),
   (r"$\sqrt{5}$", r"Uses $\frac{2a^2}{b}$ for the latus rectum; $\frac{2a^2}{b} = a$ gives $b = 2a$.")],
  r"$\frac{2b^2}{a} = \frac{1}{2}(2a) = a$ gives $b^2 = \frac{a^2}{2}$. Then $e^2 = 1 + \frac{b^2}{a^2} = \frac{3}{2}$, so $e = \frac{\sqrt{6}}{2}$.",
  r"Equating the latus rectum to the wrong length.",
  "U10-F-ecc-from-lr", "Translate the condition, then the eccentricity relation.",
  check=_c017, values=[sqrt(6)/2, sqrt(2), sqrt(5)/2, sqrt(5)])

# ---------------------------------------------------------------- 018
def _c018():
    E = Symbol('E', positive=True)
    e = sqrt(3)
    return [s for s in solve(Eq(1/e**2 + 1/E**2, 1), E) if s > 1][0]
q("U10-F-018", TOP_CONJ, "Relation between conjugate eccentricities", "Medium", "Single-step computation MCQ",
  r"The eccentricity of a hyperbola is $\sqrt{3}$. The eccentricity of its conjugate hyperbola is",
  r"$\frac{\sqrt{6}}{2}$",
  [(r"$\sqrt{2}$", r"Uses $e'^2 = e^2 - 1$."),
   (r"$2$", r"Uses $e'^2 = e^2 + 1$."),
   (r"$\frac{3}{2}$", r"Finds $e'^2 = \frac{3}{2}$ and reports it as $e'$.")],
  r"If $e^2 = 1 + \frac{b^2}{a^2}$ and $e'^2 = 1 + \frac{a^2}{b^2}$, then $\frac{1}{e^2} + \frac{1}{e'^2} = 1$. With $e^2 = 3$: $\frac{1}{e'^2} = \frac{2}{3}$, so $e' = \sqrt{\frac{3}{2}} = \frac{\sqrt{6}}{2}$.",
  r"Guessing an additive relation between $e^2$ and $e'^2$.",
  "U10-F-conjugate-relation", "Recall and apply the reciprocal-square relation.",
  check=_c018, values=[sqrt(6)/2, sqrt(2), 2, Rational(3, 2)], cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    h = X**2/25 - Y**2/16 - 1
    conj = Y**2/16 - X**2/25 - 1
    d1, d2 = _hyp(h), _hyp(conj)
    return (d1["asymptotes"] == d2["asymptotes"], bool(simplify(d1["e"] - d2["e"]) == 0))
q("U10-F-019", TOP_CONJ, "Hyperbola and its conjugate compared", "Medium", "Statement-based MCQ",
  r"Let $H$ be the hyperbola $\frac{x^2}{25} - \frac{y^2}{16} = 1$ and $H'$ its conjugate hyperbola. Statement I: $H$ and $H'$ have the same pair of asymptotes. Statement II: $H$ and $H'$ have the same eccentricity. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II; in fact $e = \frac{\sqrt{41}}{5}$ for $H$ and $e' = \frac{\sqrt{41}}{4}$ for $H'$."),
   (ST_FF, r"Rejects Statement I, perhaps thinking the slopes of the asymptotes of $H'$ are $\pm\frac{5}{4}$."),
   (ST_FT, r"Interchanges the truth values: thinks the asymptotes change but the eccentricity does not.")],
  r"$H'$ is $\frac{y^2}{16} - \frac{x^2}{25} = 1$. Both $H$ and $H'$ have asymptotes $\frac{x^2}{25} - \frac{y^2}{16} = 0$, that is $y = \pm\frac{4}{5}x$, so Statement I is true. $e^2 = 1 + \frac{16}{25} = \frac{41}{25}$ for $H$ and $e'^2 = 1 + \frac{25}{16} = \frac{41}{16}$ for $H'$, so Statement II is false.",
  r"Assuming a hyperbola and its conjugate share the eccentricity.",
  "U10-F-conjugate-compare", "Two separate properties checked.",
  check=_c019, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 020
def _c020():
    a = Symbol('a', positive=True)
    e = 3
    a0 = solve(Eq(a*e - a/e, 8), a)[0]          # focus (ae, 0) to its directrix x = a/e
    d = _hyp(X**2/a0**2 - Y**2/(a0**2*(e**2 - 1)) - 1)
    assert simplify(d["c"] - d["a"]/d["e"] - 8) == 0
    return d["lr"]
q("U10-F-020", TOP_STD, "Latus rectum from the focus-directrix gap", "Medium", "Multi-step computation MCQ",
  r"The hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ has eccentricity $3$, and the distance of each focus from the directrix nearer to it is $8$. The length of the latus rectum of the hyperbola is",
  r"$48$",
  [(r"$\frac{192}{5}$", r"Measures to the farther directrix: $ae + \frac{a}{e} = \frac{10a}{3} = 8$ gives $a = \frac{12}{5}$, and then $\frac{2b^2}{a} = 16a$."),
   (r"$24$", r"Finds $a = 3$, $b^2 = 72$ correctly but gives the semi-latus rectum $\frac{b^2}{a}$."),
   (r"$64$", r"Uses the focus to vertex distance $ae - a = 2a = 8$, so $a = 4$ and $\frac{2b^2}{a} = 16a$.")],
  r"The focus $(ae, 0)$ and the directrix $x = \frac{a}{e}$ are $ae - \frac{a}{e} = 3a - \frac{a}{3} = \frac{8a}{3}$ apart, so $\frac{8a}{3} = 8$ and $a = 3$. Then $b^2 = a^2(e^2 - 1) = 72$ and the latus rectum is $\frac{2b^2}{a} = \frac{144}{3} = 48$.",
  r"Measuring the focus to the wrong directrix or to the vertex, or stopping at the semi-latus rectum.",
  "U10-F-focus-directrix-lr", "Translate the gap into $a$, then $b^2$, then the latus rectum.",
  check=_c020, values=[48, Rational(192, 5), 24, 64],
  numerical=dict(question=r"The hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ has eccentricity $3$, and the distance of each focus from the directrix nearer to it is $8$. The length of the latus rectum of the hyperbola is", answer=48))

# ---------------------------------------------------------------- 021
def _c021():
    a, e = symbols('a e', positive=True)
    s = solve([Eq(a*e, 6), Eq(a/e, Rational(3, 2))], [a, e], dict=True)[0]
    a2 = s[a]**2
    b2 = a2*(s[e]**2 - 1)
    return _key(X**2/a2 - Y**2/b2 - 1)
q("U10-F-021", TOP_EQN, "Equation from a focus and its directrix", "Medium", "Multi-step computation MCQ",
  r"A hyperbola has its centre at the origin and its transverse axis along the $x$-axis. One focus is $(6, 0)$ and the corresponding directrix is $x = \frac{3}{2}$. The equation of the hyperbola is",
  r"$\frac{x^2}{9} - \frac{y^2}{27} = 1$",
  [(r"$\frac{x^2}{27} - \frac{y^2}{9} = 1$", r"Finds $a^2 = 9$, $b^2 = 27$ and interchanges them."),
   (r"$\frac{x^2}{9} - \frac{y^2}{36} = 1$", r"Finds $a^2 = 9$ but takes $b^2 = c^2 = 36$."),
   (r"$\frac{x^2}{9} - \frac{y^2}{45} = 1$", r"Finds $a^2 = 9$ but uses $b^2 = a^2 + c^2$.")],
  r"$ae = 6$ and $\frac{a}{e} = \frac{3}{2}$. Multiplying, $a^2 = 9$; dividing, $e^2 = 4$. Then $b^2 = a^2(e^2 - 1) = 27$, so the hyperbola is $\frac{x^2}{9} - \frac{y^2}{27} = 1$.",
  r"Mishandling $b^2$ after finding $a$ and $e$.",
  "U10-F-eqn-focus-directrix", "Solve two relations for $a$ and $e$, then find $b^2$.",
  check=_c021, values=[_key(X**2/9 - Y**2/27 - 1), _key(X**2/27 - Y**2/9 - 1), _key(X**2/9 - Y**2/36 - 1), _key(X**2/9 - Y**2/45 - 1)])

# ---------------------------------------------------------------- 022
def _c022():
    x1 = 8
    y1 = sqrt(9*(Rational(x1**2, 16) - 1))
    F = list(_hyp(X**2/16 - Y**2/9 - 1)["foci"])
    return simplify(_dist((x1, y1), F[0]) * _dist((x1, y1), F[1]))
q("U10-F-022", TOP_FOC, "Product of focal distances", "Medium", "Multi-step computation MCQ",
  r"$P$ is a point on the hyperbola $\frac{x^2}{16} - \frac{y^2}{9} = 1$ with abscissa $8$, and $S$, $S'$ are the foci. Then $PS \cdot PS'$ equals",
  r"$84$",
  [(r"$116$", r"Expands $(ex - a)(ex + a)$ as $(ex)^2 + a^2 = 100 + 16$."),
   (r"$91$", r"Uses focal distances $ex \pm b = 10 \pm 3$."),
   (r"$36$", r"Takes both focal distances equal to $ex - a = 6$.")],
  r"$e = \frac{5}{4}$, so the focal distances of a point with abscissa $x > 0$ are $ex - a$ and $ex + a$, here $10 - 4 = 6$ and $10 + 4 = 14$. Their product is $84$.",
  r"Using $ex \pm b$ for the focal distances.",
  "U10-F-focal-dist-ex", "Find $e$, then both focal distances.",
  check=_c022, values=[84, 116, 91, 36],
  numerical=dict(question=r"$P$ is a point on the hyperbola $\frac{x^2}{16} - \frac{y^2}{9} = 1$ with abscissa $8$, and $S$, $S'$ are the foci. The value of $PS \cdot PS'$ is", answer=84))

# ---------------------------------------------------------------- 023
def _c023():
    S = (4, 0)
    sols = solve([X**2/4 - Y**2/12 - 1, (X - S[0])**2 + Y**2 - 36], [X, Y], dict=True)
    xs = [s[X] for s in sols if s[X].is_real and s[Y].is_real and s[X] > 0 and s[Y] > 0]
    return xs[0]
q("U10-F-023", TOP_FOC, "Point from a given focal distance", "Medium", "Inverse/parameter MCQ",
  r"$P$ is a point in the first quadrant on the hyperbola $\frac{x^2}{4} - \frac{y^2}{12} = 1$ whose distance from the focus $S(4, 0)$ is $6$. The abscissa of $P$ is",
  r"$4$",
  [(r"$8$", r"Uses $PS = x - a$, so $x - 2 = 6$."),
   (r"$3$", r"Uses $PS = ex$, so $2x = 6$."),
   (r"$4\sqrt{3}$", r"Takes $e = \frac{c}{b} = \frac{2}{\sqrt{3}}$ in $ex - a = 6$.")],
  r"$a = 2$, $c = 4$, $e = 2$. For a point on the right branch, $PS = ex - a = 2x - 2$. Setting $2x - 2 = 6$ gives $x = 4$; then $y^2 = 12(4 - 1) = 36$, $y = 6$, so $P = (4, 6)$ is an end of the latus rectum.",
  r"Using $x - a$ or $ex$ for the focal distance.",
  "U10-F-focal-dist-ex", "Reverse use of the focal distance formula.",
  check=_c023, values=[4, 8, 3, 4*sqrt(3)],
  numerical=dict(question=r"$P$ is a point in the first quadrant on the hyperbola $\frac{x^2}{4} - \frac{y^2}{12} = 1$ whose distance from the focus $S(4, 0)$ is $6$. The abscissa of $P$ is", answer=4))

# ---------------------------------------------------------------- 024
def _c024():
    k = Symbol('k', real=True)
    return solve_univariate_inequality((12 - k)*(k - 4) < 0, k, relational=False)
q("U10-F-024", TOP_ID, "Parameter range for a hyperbola", "Medium", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which $\frac{x^2}{12 - k} + \frac{y^2}{k - 4} = 1$ represents a hyperbola is",
  r"$(-\infty, 4) \cup (12, \infty)$",
  [(r"$(4, 12)$", r"Requires both denominators positive, which gives an ellipse (or circle)."),
   (r"$(4, 8) \cup (8, 12)$", r"Takes the ellipse range and removes the circle case $k = 8$."),
   (r"$(-\infty, 4)$", r"Considers only the case where the coefficient of $y^2$ is negative.")],
  r"The equation is a hyperbola exactly when the two denominators have opposite signs: $(12 - k)(k - 4) < 0$, that is $k < 4$ or $k > 12$.",
  r"Missing one of the two sign cases.",
  "U10-F-identify-param", "Sign analysis of two denominators.",
  check=_c024, values=[Union(Interval.open(-oo, 4), Interval.open(12, oo)), Interval.open(4, 12),
                       Union(Interval.open(4, 8), Interval.open(8, 12)), Interval.open(-oo, 4)], cognitive="Understanding")

# ---------------------------------------------------------------- 025
q("U10-F-025", TOP_SHIFT, "Foci of a shifted hyperbola", "Medium", "Multi-step computation MCQ",
  r"The foci of the hyperbola $9x^2 - 16y^2 - 18x - 64y - 199 = 0$ are",
  r"$(6, -2)$ and $(-4, -2)$",
  [(r"$(6, 2)$ and $(-4, 2)$", r"Reads $(y + 2)^2$ as a shift to $y = 2$."),
   (r"$(4, -2)$ and $(-6, -2)$", r"Reads $(x - 1)^2$ as a shift to $x = -1$."),
   (r"$(1 + \sqrt{7}, -2)$ and $(1 - \sqrt{7}, -2)$", r"Uses $c^2 = a^2 - b^2 = 16 - 9$ as for an ellipse.")],
  r"Completing squares: $9(x - 1)^2 - 16(y + 2)^2 = 199 + 9 - 64 = 144$, so $\frac{(x - 1)^2}{16} - \frac{(y + 2)^2}{9} = 1$. The centre is $(1, -2)$, $c^2 = 16 + 9 = 25$, and the foci are $(1 \pm 5, -2)$, that is $(6, -2)$ and $(-4, -2)$.",
  r"Sign slips when reading the centre after completing squares.",
  "U10-F-shifted-foci", "Completing two squares, then the foci.",
  check=lambda: _hyp(9*X**2 - 16*Y**2 - 18*X - 64*Y - 199)["foci"],
  values=[_pts([(6, -2), (-4, -2)]), _pts([(6, 2), (-4, 2)]), _pts([(4, -2), (-6, -2)]), _pts([(1 + sqrt(7), -2), (1 - sqrt(7), -2)])])

# ---------------------------------------------------------------- 026
q("U10-F-026", TOP_ASY, "Asymptotes of a shifted hyperbola", "Medium", "Multi-step computation MCQ",
  r"The asymptotes of the hyperbola $4x^2 - y^2 - 8x - 4y - 4 = 0$ are",
  r"$y = 2x - 4$ and $y = -2x$",
  [(r"$y = 2x + 4$ and $y = -2x$", r"Takes the centre as $(-1, 2)$ by sign slips, giving $y - 2 = \pm 2(x + 1)$."),
   (r"$2y = x - 5$ and $2y = -x - 3$", r"Uses slopes $\pm\frac{a}{b} = \pm\frac{1}{2}$ through the correct centre $(1, -2)$."),
   (r"$y = 4x - 6$ and $y = -4x + 2$", r"Uses slopes $\pm\frac{b^2}{a^2} = \pm 4$ through the correct centre.")],
  r"$4(x - 1)^2 - (y + 2)^2 = 4$, that is $(x - 1)^2 - \frac{(y + 2)^2}{4} = 1$, with centre $(1, -2)$, $a = 1$, $b = 2$. The asymptotes are $y + 2 = \pm 2(x - 1)$, namely $y = 2x - 4$ and $y = -2x$.",
  r"Using slope $\frac{a}{b}$, or the wrong centre.",
  "U10-F-shifted-asymptotes", "Complete squares, then the asymptote pair through the centre.",
  check=lambda: _hyp(4*X**2 - Y**2 - 8*X - 4*Y - 4)["asymptotes"],
  values=[_pm(2, 1, -2), _pm(2, -1, 2), _pm(Rational(1, 2), 1, -2), _pm(4, 1, -2)])

# ---------------------------------------------------------------- 027
def _c027():
    a2 = Symbol('a2', positive=True)
    s = solve(Eq(a2 + a2, 36), a2)[0]      # b = a, c^2 = a^2 + b^2
    return _key(X**2 - Y**2 - s)
q("U10-F-027", TOP_CONJ, "Equation of a rectangular hyperbola", "Medium", "Multi-step computation MCQ",
  r"A hyperbola has its centre at the origin, its foci at $(\pm 6, 0)$, and its asymptotes perpendicular to each other. Its equation is",
  r"$x^2 - y^2 = 18$",
  [(r"$x^2 - y^2 = 36$", r"Takes $a = c = 6$."),
   (r"$x^2 - y^2 = 72$", r"Takes $a = c\sqrt{2}$, multiplying by $\sqrt{2}$ instead of dividing."),
   (r"$x^2 - y^2 = 6$", r"Takes $a^2 = c = 6$.")],
  r"Perpendicular asymptotes $y = \pm\frac{b}{a}x$ need $\frac{b^2}{a^2} = 1$, so $b = a$. Then $c^2 = 2a^2 = 36$ gives $a^2 = 18$, and the hyperbola is $x^2 - y^2 = 18$.",
  r"Forgetting that $c = a\sqrt{2}$ for a rectangular hyperbola.",
  "U10-F-rect-equation", "Perpendicular asymptotes give $b = a$, then $c^2 = 2a^2$.",
  check=_c027, values=[_key(X**2 - Y**2 - 18), _key(X**2 - Y**2 - 36), _key(X**2 - Y**2 - 72), _key(X**2 - Y**2 - 6)])

# ---------------------------------------------------------------- 028
def _c028():
    a2, b2 = symbols('a2 b2', positive=True)
    s = solve([Eq(b2, a2*(2**2 - 1)), Eq(16/a2 - 36/b2, 1)], [a2, b2], dict=True)[0]
    return simplify(2*s[b2]/sqrt(s[a2]))
q("U10-F-028", TOP_EQN, "Latus rectum from eccentricity and a point", "Medium", "Multi-step computation MCQ",
  r"The hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ has eccentricity $2$ and passes through the point $(4, 6)$. The length of its latus rectum is",
  r"$12$",
  [(r"$8\sqrt{7}$", r"Takes $\frac{b^2}{a^2} = e^2 = 4$, giving $a^2 = 7$, $b^2 = 28$ and $\frac{2b^2}{a} = \frac{56}{\sqrt{7}}$."),
   (r"$6$", r"Finds $a = 2$, $b^2 = 12$ but uses $\frac{b^2}{a}$."),
   (r"$\frac{4\sqrt{3}}{3}$", r"Finds $a = 2$, $b = 2\sqrt{3}$ but uses $\frac{2a^2}{b}$.")],
  r"$b^2 = a^2(e^2 - 1) = 3a^2$. Substituting $(4, 6)$: $\frac{16}{a^2} - \frac{36}{3a^2} = \frac{4}{a^2} = 1$, so $a = 2$ and $b^2 = 12$. The latus rectum is $\frac{2b^2}{a} = 12$.",
  r"Writing $\frac{b^2}{a^2} = e^2$ instead of $e^2 - 1$.",
  "U10-F-eqn-ecc-point", "Eccentricity relation, substitution, then the latus rectum.",
  check=_c028, values=[12, 8*sqrt(7), 6, 4*sqrt(3)/3],
  numerical=dict(question=r"The hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ has eccentricity $2$ and passes through the point $(4, 6)$. The length of its latus rectum is", answer=12))

# ---------------------------------------------------------------- 029
def _c029():
    e = Symbol('e', positive=True)
    a = 1
    return [s for s in solve(Eq(2*a*e, 4*(2*a/e)), e) if s > 1][0]
q("U10-F-029", TOP_STD, "Eccentricity from foci and directrices", "Medium", "Inverse/parameter MCQ",
  r"For a hyperbola, the distance between the foci is $4$ times the distance between the directrices. The eccentricity of the hyperbola is",
  r"$2$",
  [(r"$4$", r"Finds $e^2 = 4$ and reports $e^2$."),
   (r"$2\sqrt{2}$", r"Takes the distance between the foci as $ae$, so $ae = 4\cdot\frac{2a}{e}$ and $e^2 = 8$."),
   (r"$\sqrt{2}$", r"Takes the distance between the directrices as $\frac{a}{e}$, so $2ae = \frac{4a}{e}$ and $e^2 = 2$.")],
  r"The foci are $2ae$ apart and the directrices are $\frac{2a}{e}$ apart. So $2ae = 4\cdot\frac{2a}{e}$, giving $e^2 = 4$ and $e = 2$.",
  r"Halving only one of the two distances.",
  "U10-F-ecc-foci-directrix", "Two distances compared.",
  check=_c029, values=[2, 4, 2*sqrt(2), sqrt(2)],
  numerical=dict(question=r"For a hyperbola, the distance between the foci is $4$ times the distance between the directrices. The eccentricity of the hyperbola is", answer=2))

# ---------------------------------------------------------------- 030
def _c030():
    al = Symbol('alpha', positive=True)
    a, b = cos(al), sin(al)
    c = sqrt(a**2 + b**2)
    e = c / a
    quantities = [c, e, a, a/e]          # foci abscissa, eccentricity, vertex abscissa, directrix
    for i, v in enumerate(quantities):
        if simplify(diff(v, al)) == 0:
            return i
q("U10-F-030", TOP_STD, "Invariant under a parameter", "Medium", "Conceptual/application MCQ",
  r"For $0 < \alpha < \frac{\pi}{2}$, consider the hyperbola $\frac{x^2}{\cos^2\alpha} - \frac{y^2}{\sin^2\alpha} = 1$. As $\alpha$ varies, which of the following remains unchanged?",
  r"the foci",
  [(r"the eccentricity", r"Thinks the ratio is fixed; actually $e = \sec\alpha$ varies with $\alpha$."),
   (r"the vertices", r"Thinks the vertices stay put; they are $(\pm\cos\alpha, 0)$."),
   (r"the directrices", r"Thinks the directrices stay put; they are $x = \pm\cos^2\alpha$.")],
  r"Here $a = \cos\alpha$, $b = \sin\alpha$, so $c^2 = a^2 + b^2 = 1$ for every $\alpha$. The foci are always $(\pm 1, 0)$. On the other hand $e = \frac{1}{\cos\alpha}$, the vertices $(\pm\cos\alpha, 0)$ and the directrices $x = \pm\frac{a}{e} = \pm\cos^2\alpha$ all change.",
  r"Assuming the eccentricity is the fixed quantity in such a family.",
  "U10-F-param-invariant", r"Compute four quantities in terms of $\alpha$ and compare.",
  check=_c030, values=[0, 1, 2, 3], cognitive="Analysis")

# ---------------------------------------------------------------- 031
def _c031():
    P = (Rational(16, 3), 5)
    assert simplify(P[1]**2/9 - P[0]**2/16 - 1) == 0
    F = list(_hyp(16*Y**2 - 9*X**2 - 144)["foci"])
    return Abs(simplify(_dist(P, F[0]) - _dist(P, F[1])))
q("U10-F-031", TOP_FOC, "Focal difference with vertical transverse axis", "Medium", "Single-step computation MCQ",
  r"$P$ is a point on the hyperbola $16y^2 - 9x^2 = 144$, and $S$, $S'$ are its foci. Then $|PS - PS'|$ equals",
  r"$6$",
  [(r"$8$", r"Takes the transverse semi-axis as $4$, from the $x^2$ term."),
   (r"$10$", r"Gives the distance $2c$ between the foci."),
   (r"$3$", r"Uses $a$ in place of $2a$.")],
  r"Dividing by $144$: $\frac{y^2}{9} - \frac{x^2}{16} = 1$. The transverse axis is along the $y$-axis with $a = 3$, so $|PS - PS'| = 2a = 6$.",
  r"Taking $a$ from the $x^2$ term regardless of orientation.",
  "U10-F-focal-diff", "Orientation, then one property.",
  check=_c031, values=[6, 8, 10, 3], cognitive="Application",
  numerical=dict(question=r"$P$ is a point on the hyperbola $16y^2 - 9x^2 = 144$, and $S$, $S'$ are its foci. The value of $|PS - PS'|$ is", answer=6))

# ---------------------------------------------------------------- 032
def _c032():
    d = _hyp(X**2/36 - Y**2/12 - 1)
    xs = [-l[2] for l in d["directrices"]]
    return (bool(simplify(d["lr"] - 2) == 0), bool(simplify(Abs(xs[0] - xs[1]) - 8*sqrt(3)) == 0))
q("U10-F-032", TOP_STD, "Latus rectum and directrices checked", "Medium", "Statement-based MCQ",
  r"Consider the hyperbola $H: \frac{x^2}{36} - \frac{y^2}{12} = 1$. Statement I: The length of the latus rectum of $H$ is $2$. Statement II: The distance between the directrices of $H$ is $8\sqrt{3}$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts both values: $2 = \frac{b^2}{a}$ is only half the latus rectum, and $8\sqrt{3} = 2c$ is the distance between the foci."),
   (ST_TF, r"Accepts the semi-latus rectum $\frac{b^2}{a} = 2$ as the latus rectum."),
   (ST_FT, r"Accepts $2c = 8\sqrt{3}$ as the distance between the directrices.")],
  r"$a = 6$, $b^2 = 12$, $c^2 = 48$, $c = 4\sqrt{3}$, $e = \frac{2}{\sqrt{3}}$. The latus rectum is $\frac{2b^2}{a} = 4$, so Statement I is false. The directrices are $x = \pm\frac{a}{e} = \pm 3\sqrt{3}$, which are $6\sqrt{3}$ apart, so Statement II is false.",
  r"Confusing the semi-latus rectum with the latus rectum and $2c$ with $\frac{2a}{e}$.",
  "U10-F-statement-lr-directrix", "Two separate computations to verify.",
  check=_c032, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 033
def _c033():
    A2, B2 = 289, 225
    ce = sqrt(A2 - B2)             # foci of the ellipse
    a, c = ce, sqrt(A2)            # hyperbola: vertices at ellipse foci, foci at ellipse vertices
    d = _hyp(X**2/a**2 - Y**2/(c**2 - a**2) - 1)
    xs = [-l[2] for l in d["directrices"]]
    return Abs(xs[0] - xs[1])
q("U10-F-033", TOP_EQN, "Hyperbola built from an ellipse: directrices", "Medium", "Multi-step computation MCQ",
  r"A hyperbola has its vertices at the foci of the ellipse $\frac{x^2}{289} + \frac{y^2}{225} = 1$ and its foci at the end points of the major axis of this ellipse. The distance between the directrices of the hyperbola is",
  r"$\frac{128}{17}$",
  [(r"$\frac{64}{17}$", r"Gives $\frac{a}{e}$, the distance of one directrix from the centre."),
   (r"$\frac{289}{4}$", r"Gives the distance $\frac{2 \cdot 17}{8/17}$ between the directrices of the ellipse."),
   (r"$34$", r"Uses $2ae$, the distance between the foci, in place of $\frac{2a}{e}$.")],
  r"The ellipse has $c^2 = 289 - 225 = 64$, so its foci are $(\pm 8, 0)$ and its vertices are $(\pm 17, 0)$. The hyperbola therefore has $a = 8$ and $c = 17$, so $e = \frac{17}{8}$, and its directrices $x = \pm\frac{a}{e} = \pm\frac{64}{17}$ are $\frac{128}{17}$ apart.",
  r"Answering for the ellipse, or confusing $\frac{2a}{e}$ with $2ae$.",
  "U10-F-from-ellipse-directrix", "Ellipse data feed the hyperbola data, then the directrices.",
  check=_c033, values=[Rational(128, 17), Rational(64, 17), Rational(289, 4), 34])

# ---------------------------------------------------------------- 034
def _c034():
    d = _hyp(2*X**2 - 3*Y**2 - 4*X - 12*Y - 16)
    return (d["centre"][0], d["centre"][1], 2*d["a"])
q("U10-F-034", TOP_ID, "Identifying a shifted hyperbola", "Medium", "Multi-step computation MCQ",
  r"The equation $2x^2 - 3y^2 - 4x - 12y - 16 = 0$ represents",
  r"a hyperbola with centre $(1, -2)$ and transverse axis of length $2\sqrt{3}$",
  [(r"a hyperbola with centre $(1, -2)$ and transverse axis of length $2\sqrt{2}$", r"Uses the denominator $2$ of the $y$-term for the transverse semi-axis."),
   (r"a hyperbola with centre $(-1, 2)$ and transverse axis of length $2\sqrt{3}$", r"Reads the centre with both signs reversed."),
   (r"a hyperbola with centre $(1, -2)$ and transverse axis of length $\sqrt{3}$", r"Gives the semi-axis $a$ as the length of the axis.")],
  r"$2(x - 1)^2 - 2 - 3(y + 2)^2 + 12 - 16 = 0$, that is $2(x - 1)^2 - 3(y + 2)^2 = 6$, or $\frac{(x - 1)^2}{3} - \frac{(y + 2)^2}{2} = 1$. This is a hyperbola with centre $(1, -2)$, transverse axis parallel to the $x$-axis, and $a = \sqrt{3}$, so the transverse axis has length $2\sqrt{3}$.",
  r"Sign slips in the centre, or reporting $a$ instead of $2a$.",
  "U10-F-shifted-identify", "Complete two squares and read the data.",
  check=_c034, values=[(1, -2, 2*sqrt(3)), (1, -2, 2*sqrt(2)), (-1, 2, 2*sqrt(3)), (1, -2, sqrt(3))])

# ---------------------------------------------------------------- 035
def _c035():
    c, e = 15, Rational(5, 3)
    a = c / e
    return _key(Y**2/a**2 - X**2/(c**2 - a**2) - 1)
q("U10-F-035", TOP_EQN, "Equation from foci on the y-axis and eccentricity", "Medium", "Multi-step computation MCQ",
  r"The hyperbola with foci $(0, \pm 15)$ and eccentricity $\frac{5}{3}$ has equation",
  r"$\frac{y^2}{81} - \frac{x^2}{144} = 1$",
  [(r"$\frac{x^2}{81} - \frac{y^2}{144} = 1$", r"Finds $a^2 = 81$, $b^2 = 144$ but puts the transverse axis along the $x$-axis."),
   (r"$\frac{y^2}{144} - \frac{x^2}{81} = 1$", r"Finds the right numbers but interchanges $a^2$ and $b^2$."),
   (r"$\frac{y^2}{81} - \frac{x^2}{306} = 1$", r"Uses $b^2 = a^2 + c^2 = 81 + 225$.")],
  r"$c = ae = 15$ with $e = \frac{5}{3}$ gives $a = 9$. Then $b^2 = c^2 - a^2 = 225 - 81 = 144$. The foci are on the $y$-axis, so the hyperbola is $\frac{y^2}{81} - \frac{x^2}{144} = 1$.",
  r"Ignoring the orientation fixed by the foci.",
  "U10-F-eqn-foci-ecc", "Find $a$ from $c = ae$, then $b^2$, then orientation.",
  check=_c035, values=[_key(Y**2/81 - X**2/144 - 1), _key(X**2/81 - Y**2/144 - 1), _key(Y**2/144 - X**2/81 - 1), _key(Y**2/81 - X**2/306 - 1)])

# ---------------------------------------------------------------- 036
def _c036():
    a2 = Symbol('a2', positive=True)
    b2 = 4*a2                      # asymptotes y = +/- 2x
    s = solve(Eq(9/a2 - 16/b2, 1), a2)[0]
    return 2*sqrt(s + 4*s)
q("U10-F-036", TOP_ASY, "Equation from asymptotes and a point", "Medium", "Multi-step computation MCQ",
  r"A hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ has asymptotes $y = \pm 2x$ and passes through the point $(3, 4)$. The distance between its foci is",
  r"$10$",
  [(r"$2\sqrt{5}$", r"Gives the length $2a$ of the transverse axis."),
   (r"$4\sqrt{5}$", r"Gives the length $2b$ of the conjugate axis."),
   (r"$5$", r"Gives $c$ in place of $2c$.")],
  r"The asymptotes give $\frac{b}{a} = 2$, so $b^2 = 4a^2$. Substituting $(3, 4)$: $\frac{9}{a^2} - \frac{16}{4a^2} = \frac{5}{a^2} = 1$, so $a^2 = 5$, $b^2 = 20$, $c^2 = 25$. The foci are $2c = 10$ apart.",
  r"Stopping at $a$, $b$ or $c$ instead of $2c$.",
  "U10-F-eqn-asymptote-point", "Asymptote slope, substitution, then $c$.",
  check=_c036, values=[10, 2*sqrt(5), 4*sqrt(5), 5],
  numerical=dict(question=r"A hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ has asymptotes $y = \pm 2x$ and passes through the point $(3, 4)$. The distance between its foci is", answer=10))

# ---------------------------------------------------------------- 037
def _c037():
    S1, S2 = (6, 0), (-6, 0)
    sols = solve([X**2/16 - Y**2/20 - 1, (X - 6)**2 + Y**2 - 9], [X, Y], dict=True)
    ds = {simplify(_dist((s[X], s[Y]), S2)) for s in sols if s[X].is_real and s[Y].is_real}
    assert len(ds) == 1
    return ds.pop()
q("U10-F-037", TOP_FOC, "Other focal distance with a branch check", "Medium", "Multi-step computation MCQ",
  r"$S_1(6, 0)$ and $S_2(-6, 0)$ are the foci of the hyperbola $\frac{x^2}{16} - \frac{y^2}{20} = 1$. If $P$ is a point on the hyperbola with $PS_1 = 3$, then $PS_2$ equals",
  r"$11$",
  [(r"$5$", r"Writes $PS_2 = 2a - PS_1 = 8 - 3$, subtracting in the wrong order."),
   (r"$15$", r"Adds the distance $2c = 12$ between the foci to $PS_1$."),
   (r"$7$", r"Uses $|PS_1 - PS_2| = a = 4$.")],
  r"$|PS_1 - PS_2| = 2a = 8$, so $PS_2 = 11$ or $PS_2 = -5$; the negative value is impossible. (Indeed, every point of the left branch is at least $c + a = 10$ from $S_1$, so $P$ is on the right branch, nearer $S_1$.) Hence $PS_2 = 11$.",
  r"Taking $2a - PS_1$ instead of $PS_1 + 2a$.",
  "U10-F-focal-diff-branch", "Two cases from the absolute value, one rejected.",
  check=_c037, values=[11, 5, 15, 7],
  numerical=dict(question=r"$S_1(6, 0)$ and $S_2(-6, 0)$ are the foci of the hyperbola $\frac{x^2}{16} - \frac{y^2}{20} = 1$. If $P$ is a point on the hyperbola with $PS_1 = 3$, then $PS_2$ is", answer=11))

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 038
def _c038():
    k = Symbol('k', real=True)
    s1 = solve_univariate_inequality(k**2 - 16 < 0, k, relational=False)
    s2 = solve_univariate_inequality(k + 4 > 0, k, relational=False)
    a2, b2 = k + 4, 16 - k**2           # y^2/a2 - x^2/b2 = 1 on s1 and s2
    s3 = solve_univariate_inequality(1 + b2/a2 > 2, k, relational=False)
    return Intersection(s1, s2, s3)
q("U10-F-038", TOP_ID, "Parameter range for a vertical transverse axis and eccentricity", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which $\frac{x^2}{k^2 - 16} + \frac{y^2}{k + 4} = 1$ represents a hyperbola whose transverse axis is along the $y$-axis and whose eccentricity is greater than $\sqrt{2}$ is",
  r"$(-4, 3)$",
  [(r"$(-4, 4)$", r"Imposes the orientation conditions $k + 4 > 0$, $k^2 - 16 < 0$ but ignores the eccentricity condition."),
   (r"$(3, 4)$", r"Uses $e^2 = 1 + \frac{a^2}{b^2}$, so $e > \sqrt{2}$ becomes $k + 4 > 16 - k^2$, giving $k > 3$ within $(-4, 4)$."),
   (r"$(-3, 4)$", r"Reaches $k^2 + k - 12 < 0$ but factorises it as $(k + 3)(k - 4)$, giving $-3 < k < 4$.")],
  r"For the transverse axis along the $y$-axis we need $k + 4 > 0$ and $k^2 - 16 < 0$, so $-4 < k < 4$, and then $\frac{y^2}{k + 4} - \frac{x^2}{16 - k^2} = 1$ with $a^2 = k + 4$, $b^2 = 16 - k^2$. Now $e^2 = 1 + \frac{b^2}{a^2} > 2$ means $b^2 > a^2$: $16 - k^2 > k + 4$, i.e. $k^2 + k - 12 < 0$, i.e. $(k + 4)(k - 3) < 0$, so $-4 < k < 3$. Together, $k \in (-4, 3)$.",
  r"Ignoring the eccentricity condition, or using $\frac{a^2}{b^2}$ in place of $\frac{b^2}{a^2}$ when $a^2$ sits under $y^2$.",
  "U10-F-identify-param", "Three conditions: two sign conditions for orientation, then an eccentricity inequality reduced to a quadratic, with the trap of which denominator is $a^2$.",
  check=_c038, values=[Interval.open(-4, 3), Interval.open(-4, 4), Interval.open(3, 4), Interval.open(-3, 4)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 039
def _c039():
    e = Symbol('e', positive=True)
    a = 1
    b2 = a**2*(e**2 - 1)
    L1, L2 = (a*e, b2/a), (a*e, -b2/a)
    dot = L1[0]*L2[0] + L1[1]*L2[1]
    return [s for s in solve(dot, e) if s > 1][0]
q("U10-F-039", TOP_STD, "Latus rectum subtending a right angle", "Difficult", "Inverse/parameter MCQ",
  r"The latus rectum of the hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ subtends a right angle at the centre of the hyperbola. The eccentricity of the hyperbola is",
  r"$\frac{1 + \sqrt{5}}{2}$",
  [(r"$1 + \sqrt{2}$", r"Imposes the right angle at the other focus $(-ae, 0)$, giving $\frac{b^2}{a} = 2ae$ and $e^2 - 2e - 1 = 0$."),
   (r"$\frac{1 + \sqrt{17}}{4}$", r"Takes the ends of the latus rectum as $\left(ae, \pm\frac{2b^2}{a}\right)$, giving $2(e^2 - 1) = e$."),
   (r"$\sqrt{2}$", r"Places the latus rectum at $x = a$, so the right angle gives $\frac{b^2}{a} = a$ and $b = a$.")],
  r"The ends are $L\left(ae, \frac{b^2}{a}\right)$ and $L'\left(ae, -\frac{b^2}{a}\right)$. A right angle at the origin needs $\overrightarrow{OL}\cdot\overrightarrow{OL'} = a^2e^2 - \frac{b^4}{a^2} = 0$, so $\frac{b^2}{a} = ae$, that is $e^2 - 1 = e$. The root greater than $1$ is $e = \frac{1 + \sqrt{5}}{2}$.",
  r"Using the wrong half-length of the latus rectum or the wrong vertex for the angle.",
  "U10-F-lr-right-angle", "Coordinates of the latus rectum ends, a perpendicularity condition, then a quadratic in $e$.",
  check=_c039, values=[(1 + sqrt(5))/2, 1 + sqrt(2), (1 + sqrt(17))/4, sqrt(2)], cognitive="Analysis")

# ---------------------------------------------------------------- 040
def _c040():
    x1, y1 = symbols('x1 y1', real=True)
    lines = list(_hyp(X**2/12 - Y**2/4 - 1)["asymptotes"])
    prod = 1
    for (p, r, s) in lines:
        prod *= (p*x1 + r*y1 + s) / sqrt(p**2 + r**2)
    prod = expand(prod).subs(y1**2, 4*(x1**2/12 - 1))
    return Abs(simplify(prod))
q("U10-F-040", TOP_ASY, "Product of distances from the asymptotes", "Difficult", "Multi-step computation MCQ",
  r"$P$ is any point on the hyperbola $\frac{x^2}{12} - \frac{y^2}{4} = 1$. The product of the perpendicular distances of $P$ from the two asymptotes of the hyperbola is",
  r"$3$",
  [(r"$\sqrt{3}$", r"Takes $P$ at the vertex $(2\sqrt{3}, 0)$ and gives only its distance $\frac{ab}{c} = \sqrt{3}$ from one asymptote, not the product of both distances."),
   (r"$6$", r"Uses $\frac{a^2b^2}{a^2 - b^2} = \frac{48}{8}$, the ellipse type denominator."),
   (r"$12$", r"Reaches $|x_1^2 - 3y_1^2| = 12$ but forgets to divide by the normalising factors $2 \cdot 2$.")],
  r"The asymptotes are $x \pm \sqrt{3}y = 0$. For $P(x_1, y_1)$ the distances are $\frac{|x_1 - \sqrt{3}y_1|}{2}$ and $\frac{|x_1 + \sqrt{3}y_1|}{2}$, whose product is $\frac{|x_1^2 - 3y_1^2|}{4}$. Since $x_1^2 - 3y_1^2 = 12$ on the hyperbola, the product is $3$, independent of $P$.",
  r"Not using the curve equation to simplify $|x_1^2 - 3y_1^2|$.",
  "U10-F-asymptote-distance-product", "Two point-line distances combined with the curve equation; non-obvious route.",
  check=_c040, values=[3, sqrt(3), 6, 12], cognitive="Analysis",
  numerical=dict(question=r"$P$ is any point on the hyperbola $\frac{x^2}{12} - \frac{y^2}{4} = 1$. The product of the perpendicular distances of $P$ from the two asymptotes of the hyperbola is", answer=3))

# ---------------------------------------------------------------- 041
def _c041():
    S, e = (3, 0), 2
    locus = (X - S[0])**2 + (Y - S[1])**2 - e**2*(X - 1)**2
    F = _hyp(locus)["foci"]
    other = [p for p in F if p != Tuple(3, 0)]
    return tuple(other[0])
q("U10-F-041", TOP_EQN, "Second focus from focus, directrix and eccentricity", "Difficult", "Multi-step computation MCQ",
  r"A hyperbola has a focus at $S(3, 0)$, the corresponding directrix $x = 1$, and eccentricity $2$. Its other focus is",
  r"$(-\frac{7}{3}, 0)$",
  [(r"$(-3, 0)$", r"Assumes the centre is at the origin and reflects $S$ in it."),
   (r"$(-1, 0)$", r"Reflects $S$ in the directrix $x = 1$."),
   (r"$(-\frac{1}{3}, 0)$", r"Finds the centre $\left(\frac{1}{3}, 0\right)$ and $a = \frac{4}{3}$ but uses $c = \frac{a}{e} = \frac{2}{3}$ (the centre-to-directrix distance), giving $\frac{1}{3} - \frac{2}{3}$.")],
  r"By the focus-directrix property, $(x - 3)^2 + y^2 = 4(x - 1)^2$, which simplifies to $3x^2 - y^2 - 2x - 5 = 0$, or $\frac{\left(x - \frac{1}{3}\right)^2}{16/9} - \frac{y^2}{16/3} = 1$. The centre is $\left(\frac{1}{3}, 0\right)$, $a = \frac{4}{3}$ and $c = ae = \frac{8}{3}$, so the foci are $\left(\frac{1}{3} \pm \frac{8}{3}, 0\right)$: $(3, 0)$ and $\left(-\frac{7}{3}, 0\right)$.",
  r"Assuming the centre is at the origin when only a focus and directrix are given.",
  "U10-F-focus-directrix-locus", "Form the locus, complete the square, then locate both foci.",
  check=_c041, values=[(-Rational(7, 3), 0), (-3, 0), (-1, 0), (-Rational(1, 3), 0)], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c042():
    d = _hyp(X**2/9 - Y**2/16 - 1)
    a, b, c = d["a"], d["b"], d["c"]
    xd = a / d["e"]
    meets = [(xd, (b/a)*xd), (xd, -(b/a)*xd)]
    s1 = all(simplify(p[0]**2 + p[1]**2 - 9) == 0 for p in meets)
    S = Matrix([c, 0])
    feet = []
    for m in (b/a, -b/a):
        u = Matrix([1, m]) / sqrt(1 + m**2)
        feet.append(tuple(simplify(v) for v in (S.dot(u)) * u))
    s2 = all(any(simplify(f[0] - p[0]) == 0 and simplify(f[1] - p[1]) == 0 for f in feet) for p in meets)
    return (bool(s1), bool(s2))
q("U10-F-042", TOP_ASY, "Directrix, asymptotes and the auxiliary circle", "Difficult", "Statement-based MCQ",
  r"For the hyperbola $\frac{x^2}{9} - \frac{y^2}{16} = 1$, let the directrix $x = \frac{9}{5}$ meet the asymptotes at $M$ and $N$. Statement I: $M$ and $N$ lie on the circle $x^2 + y^2 = 9$. Statement II: $M$ and $N$ are the feet of the perpendiculars drawn from the focus $(5, 0)$ to the asymptotes. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Rejects both, perhaps evaluating the asymptotes with slopes $\pm\frac{3}{4}$, which gives points not on the circle."),
   (ST_TF, r"Verifies the circle but does not check the foot of the perpendicular, assuming it is a different point."),
   (ST_FT, r"Checks the feet correctly but tests the points against $x^2 + y^2 = 25$ instead of $9$.")],
  r"The asymptotes are $y = \pm\frac{4}{3}x$, so $M, N = \left(\frac{9}{5}, \pm\frac{12}{5}\right)$, and $\frac{81 + 144}{25} = 9$: Statement I is true. The foot of the perpendicular from $(5, 0)$ to $4x - 3y = 0$ is $(5, 0) - \frac{20}{25}(4, -3) = \left(\frac{9}{5}, \frac{12}{5}\right)$, and by symmetry the other foot is $\left(\frac{9}{5}, -\frac{12}{5}\right)$: Statement II is true.",
  r"Not recognising that the directrix, the asymptotes and the auxiliary circle are concurrent at the feet of perpendiculars from the foci.",
  "U10-F-directrix-asymptote-circle", "Three objects intersected and a foot of perpendicular computed.",
  check=_c042, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 043
def _c043():
    sols = solve([X**2/9 - Y**2/16 - 1, X**2 + Y**2 - 25], [X, Y], dict=True)   # angle SPS' = 90 deg
    y = [s[Y] for s in sols if s[X].is_real and s[Y].is_real][0]
    return simplify(Rational(1, 2) * 10 * Abs(y))
q("U10-F-043", TOP_FOC, "Right angle at a point of the hyperbola", "Difficult", "Multi-step computation MCQ",
  r"$S$ and $S'$ are the foci of the hyperbola $\frac{x^2}{9} - \frac{y^2}{16} = 1$, and $P$ is a point on the hyperbola with $\angle SPS' = 90^\circ$. The area of triangle $SPS'$ is",
  r"$16$",
  [(r"$32$", r"Finds $PS \cdot PS' = 32$ and forgets the factor $\frac{1}{2}$."),
   (r"$9$", r"Uses $|PS - PS'| = 2b = 8$, so $2\,PS\cdot PS' = 100 - 64$."),
   (r"$\frac{91}{4}$", r"Uses $|PS - PS'| = a = 3$, so $2\,PS\cdot PS' = 100 - 9$.")],
  r"$SS' = 2c = 10$. With the right angle at $P$, $PS^2 + PS'^2 = 100$, and $|PS - PS'| = 2a = 6$ gives $PS^2 + PS'^2 - 2\,PS\cdot PS' = 36$. So $PS \cdot PS' = 32$ and the area is $\frac{1}{2}\cdot 32 = 16$.",
  r"Using $2b$ for the focal difference or forgetting the half in the area.",
  "U10-F-focal-right-angle", "Combines the focal difference with Pythagoras and an area; non-obvious route.",
  check=_c043, values=[16, 32, 9, Rational(91, 4)], cognitive="Analysis",
  numerical=dict(question=r"$S$ and $S'$ are the foci of the hyperbola $\frac{x^2}{9} - \frac{y^2}{16} = 1$, and $P$ is a point on the hyperbola with $\angle SPS' = 90^\circ$. The area of triangle $SPS'$ is", answer=16))

# ---------------------------------------------------------------- 044
def _c044():
    k = Symbol('k', real=True)
    expr = expand(16*(X**2/4 - (2*X + k)**2/16 - 1))
    p = Poly(expr, X)
    assert p.coeff_monomial(X**2) == 0
    a1, a0 = p.coeff_monomial(X), p.coeff_monomial(1)
    bad = solveset(Eq(a1, 0), k, S.Reals)
    for kv in bad:
        assert a0.subs(k, kv) != 0      # no solution there
    return Complement(S.Reals, bad)
q("U10-F-044", TOP_ASY, "Lines parallel to an asymptote", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which the line $y = 2x + k$ meets the hyperbola $\frac{x^2}{4} - \frac{y^2}{16} = 1$ in exactly one point is",
  r"$\mathbb{R} \setminus \{0\}$",
  [(r"$\{0\}$", r"Applies the tangency condition $k^2 = a^2m^2 - b^2 = 0$, but $y = 2x$ is the asymptote and never meets the curve."),
   (r"$\mathbb{R}$", r"Sees that the equation is linear in $x$ and overlooks that for $k = 0$ it reduces to $-16 = 0$."),
   (r"$\{-4\sqrt{2}, 4\sqrt{2}\}$", r"Uses $k^2 = a^2m^2 + b^2 = 32$, the condition for an ellipse.")],
  r"Substituting, $4x^2 - (2x + k)^2 = 16$, that is $-4kx - k^2 - 16 = 0$. The $x^2$ terms cancel because the line is parallel to the asymptote $y = 2x$. For $k \ne 0$ there is exactly one solution $x = -\frac{k^2 + 16}{4k}$; for $k = 0$ the equation reads $-16 = 0$ and there is none. So $k \in \mathbb{R} \setminus \{0\}$.",
  r"Treating every single intersection point as tangency.",
  "U10-F-asymptote-parallel-line", "Recognise the degenerate quadratic and handle the special case.",
  check=_c044, values=[Complement(S.Reals, FiniteSet(0)), FiniteSet(0), S.Reals, FiniteSet(-4*sqrt(2), 4*sqrt(2))],
  cognitive="Analysis")

# ---------------------------------------------------------------- 045
def _c045():
    t = Symbol('t', positive=True)     # t = b^2/a^2
    f = (1 + t)*(1 + 1/t)              # (e e')^2
    crit = [s for s in solve(diff(f, t), t) if s > 0]
    return sqrt(min(f.subs(t, s) for s in crit))
q("U10-F-045", TOP_CONJ, "Least product of conjugate eccentricities", "Difficult", "Multi-step computation MCQ",
  r"If $e_1$ and $e_2$ are the eccentricities of a hyperbola and its conjugate hyperbola, then the least possible value of $e_1 e_2$ is",
  r"$2$",
  [(r"$\sqrt{2}$", r"Gives the common eccentricity $\sqrt{2}$ of the rectangular case instead of the product $\sqrt{2}\cdot\sqrt{2}$."),
   (r"$4$", r"Gives the least value of $e_1^2 e_2^2$."),
   (r"$2\sqrt{2}$", r"Gives the least value of the sum $e_1 + e_2$.")],
  r"From $\frac{1}{e_1^2} + \frac{1}{e_2^2} = 1$ we get $e_1^2 e_2^2 = e_1^2 + e_2^2 \ge 2e_1e_2$, so $e_1e_2 \ge 2$, with equality when $e_1 = e_2 = \sqrt{2}$ (a rectangular hyperbola). The least value is $2$.",
  r"Confusing the least value of the product with that of the sum or the square.",
  "U10-F-conjugate-relation", "Relation between $e_1$, $e_2$ followed by an AM-GM type bound.",
  check=_c045, values=[2, sqrt(2), 4, 2*sqrt(2)], cognitive="Analysis",
  numerical=dict(question=r"If $e_1$ and $e_2$ are the eccentricities of a hyperbola and its conjugate hyperbola, then the least possible value of $e_1 e_2$ is", answer=2))

# ---------------------------------------------------------------- 046
def _c046():
    h, k = symbols('h k', real=True)
    cen = solve([2*X - Y - 3, 2*X + Y - 5], [X, Y])
    h0, k0 = cen[X], cen[Y]
    F = (2, 6)
    assert F[0] == h0                  # transverse axis vertical
    c = Abs(F[1] - k0)
    # vertical: asymptote slopes +/- a/b = 2
    b2 = Symbol('b2', positive=True)
    b2v = solve(Eq(4*b2 + b2, c**2), b2)[0]
    a2v = 4*b2v
    return _key((Y - k0)**2/a2v - (X - h0)**2/b2v - 1)
q("U10-F-046", TOP_SHIFT, "Equation from asymptotes and a focus", "Difficult", "Multi-step computation MCQ",
  r"The asymptotes of a hyperbola are $2x - y - 3 = 0$ and $2x + y - 5 = 0$, and one of its foci is $(2, 6)$. The equation of the hyperbola is",
  r"$\frac{(y - 1)^2}{20} - \frac{(x - 2)^2}{5} = 1$",
  [(r"$\frac{(y - 1)^2}{5} - \frac{(x - 2)^2}{20} = 1$", r"Treats the slope $2$ as $\frac{b}{a}$ even though the transverse axis is vertical, giving $a^2 = 5$, $b^2 = 20$."),
   (r"$\frac{(x - 2)^2}{5} - \frac{(y - 1)^2}{20} = 1$", r"Assumes the transverse axis is horizontal, as in the standard form, with $\frac{b}{a} = 2$."),
   (r"$\frac{(y + 1)^2}{20} - \frac{(x + 2)^2}{5} = 1$", r"Finds the centre as $(2, 1)$ but writes the shifts with the wrong sign.")],
  r"The asymptotes meet at the centre $(2, 1)$. The focus $(2, 6)$ is directly above it, so the transverse axis is vertical and $c = 5$. For $\frac{(y - 1)^2}{a^2} - \frac{(x - 2)^2}{b^2} = 1$ the asymptotes are $y - 1 = \pm\frac{a}{b}(x - 2)$, so $\frac{a}{b} = 2$, $a^2 = 4b^2$. Then $a^2 + b^2 = 5b^2 = 25$ gives $b^2 = 5$, $a^2 = 20$.",
  r"Using slope $\frac{b}{a}$ for asymptotes of a hyperbola with vertical transverse axis.",
  "U10-F-asymptote-focus-shifted", "Centre from two lines, orientation from the focus, slope relation, then $c^2 = a^2 + b^2$.",
  check=_c046, values=[_key((Y - 1)**2/20 - (X - 2)**2/5 - 1), _key((Y - 1)**2/5 - (X - 2)**2/20 - 1),
                       _key((X - 2)**2/5 - (Y - 1)**2/20 - 1), _key((Y + 1)**2/20 - (X + 2)**2/5 - 1)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 047
def _c047():
    pts = [(x, y) for x in range(-60, 61) for y in range(-60, 61) if x*x - y*y == 45]
    return len(pts)
q("U10-F-047", TOP_CONJ, "Lattice points on a rectangular hyperbola", "Difficult", "Multi-step computation MCQ",
  r"The number of points with both coordinates integers on the rectangular hyperbola $x^2 - y^2 = 45$ is",
  r"$12$",
  [(r"$8$", r"Ignores the factorisation $x - y = 1$, $x + y = 45$ as trivial, keeping only $3 \cdot 15$ and $5 \cdot 9$, and so misses the points $(\pm 23, \pm 22)$."),
   (r"$16$", r"Runs through the divisors $d = 1, 3, 5, 9$ (taking the cut-off $\sqrt{45}$ to be about $9$) with four sign choices each, so the points $(\pm 7, \pm 2)$ from $d = 5$ and $d = 9$ are counted twice."),
   (r"$24$", r"Takes the $6$ positive divisor pairs and attaches all four sign choices to each, counting every point twice.")],
  r"$(x - y)(x + y) = 45$. All divisors of $45$ are odd, so $x = \frac{d + 45/d}{2}$ and $y = \frac{45/d - d}{2}$ are integers for every divisor $d$, positive or negative. There are $12$ such divisors $d \in \{\pm 1, \pm 3, \pm 5, \pm 9, \pm 15, \pm 45\}$, each giving a different point: $(\pm 23, \pm 22)$, $(\pm 9, \pm 6)$, $(\pm 7, \pm 2)$. So there are $12$ points.",
  r"Restricting to positive divisors or double counting sign choices.",
  "U10-F-rect-lattice", "Factorisation and parity casework with careful counting.",
  check=_c047, values=[12, 8, 16, 24], cognitive="Analysis",
  numerical=dict(question=r"The number of points with both coordinates integers on the rectangular hyperbola $x^2 - y^2 = 45$ is", answer=12))

# ---------------------------------------------------------------- 048
def _c048():
    a, b = symbols('a b', positive=True)
    conj = _hyp(Y**2/4 - X**2/12 - 1)
    s1 = bool(simplify(conj["e"] - 2/sqrt(3)) == 0)
    c = sqrt(a**2 + b**2)
    P = [Matrix([c, 0]), Matrix([0, c]), Matrix([-c, 0]), Matrix([0, -c])]
    sides = [simplify((P[(i + 1) % 4] - P[i]).norm()) for i in range(4)]
    diag_dot = simplify((P[2] - P[0]).dot(P[3] - P[1]))
    square = all(simplify(s - sides[0]) == 0 for s in sides) and diag_dot == 0
    area = simplify(sides[0]**2)
    s2 = bool(square and simplify(area - 2*(a**2 + b**2)) == 0)
    return (s1, s2)
q("U10-F-048", TOP_CONJ, "Conjugate hyperbola: eccentricity and foci", "Difficult", "Statement-based MCQ",
  r"Statement I: The eccentricity of the hyperbola conjugate to $\frac{x^2}{12} - \frac{y^2}{4} = 1$ is $\frac{2}{\sqrt{3}}$. Statement II: For every hyperbola $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$, the foci of the hyperbola and the foci of its conjugate hyperbola are the vertices of a square of area $2(a^2 + b^2)$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I; $\frac{2}{\sqrt{3}}$ is the eccentricity of the given hyperbola, not of its conjugate."),
   (ST_FF, r"Rejects Statement II, perhaps taking the area of the square as $(2c)^2 = 4(a^2 + b^2)$ from the diagonal."),
   (ST_TF, r"Accepts Statement I and also squares the diagonal $2c$ for the area in Statement II.")],
  r"The conjugate is $\frac{y^2}{4} - \frac{x^2}{12} = 1$ with transverse semi-axis $2$, so $e'^2 = 1 + \frac{12}{4} = 4$ and $e' = 2$; Statement I is false (the value $\frac{2}{\sqrt{3}}$ belongs to the original hyperbola). The four foci $(\pm c, 0)$, $(0, \pm c)$ with $c^2 = a^2 + b^2$ form a square whose diagonals both have length $2c$, so its area is $\frac{1}{2}(2c)^2 = 2c^2 = 2(a^2 + b^2)$; Statement II is true.",
  r"Mixing up the eccentricity of a hyperbola with that of its conjugate.",
  "U10-F-conjugate-foci-square", "Two separate facts, one numerical and one general.",
  check=_c048, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis")

# ---------------------------------------------------------------- 049
def _c049():
    c2 = _hyp(X**2/36 - Y**2/28 - Rational(1, 4))["c"]**2
    b2 = Symbol('b2', positive=True)
    return solve(Eq(100 - b2, c2), b2)[0]
q("U10-F-049", TOP_EQN, "Confocal ellipse and hyperbola", "Difficult", "Inverse/parameter MCQ",
  r"The foci of the ellipse $\frac{x^2}{100} + \frac{y^2}{b^2} = 1$ (with $b^2 < 100$) coincide with the foci of the hyperbola $\frac{x^2}{36} - \frac{y^2}{28} = \frac{1}{4}$. Then $b^2$ equals",
  r"$84$",
  [(r"$36$", r"Reads $c^2 = 36 + 28 = 64$ without first making the right side $1$."),
   (r"$98$", r"Rescales correctly to $\frac{x^2}{9} - \frac{y^2}{7} = 1$ but uses $c^2 = 9 - 7 = 2$."),
   (r"$96$", r"Finds $c = 4$ for the hyperbola but subtracts $c$ instead of $c^2$ from $100$.")],
  r"Multiplying by $4$, the hyperbola is $\frac{x^2}{9} - \frac{y^2}{7} = 1$, so $c^2 = 9 + 7 = 16$ and its foci are $(\pm 4, 0)$. For the ellipse, $c^2 = 100 - b^2 = 16$, so $b^2 = 84$.",
  r"Reading $a^2$ and $b^2$ before making the right side equal to $1$.",
  "U10-F-confocal", "Rescaling trap plus combining two conics.",
  check=_c049, values=[84, 36, 98, 96], cognitive="Analysis",
  numerical=dict(question=r"The foci of the ellipse $\frac{x^2}{100} + \frac{y^2}{b^2} = 1$ (with $b^2 < 100$) coincide with the foci of the hyperbola $\frac{x^2}{36} - \frac{y^2}{28} = \frac{1}{4}$. The value of $b^2$ is", answer=84))

# ---------------------------------------------------------------- 050
def _c050():
    S1, S2, diff_ = (1, -2), (1, 8), 6
    h, k = (S1[0] + S2[0]) / Integer(2), (S1[1] + S2[1]) / Integer(2)
    c = _dist(S1, S2) / 2
    a = Integer(diff_) / 2
    b2 = c**2 - a**2
    expr = (Y - k)**2/a**2 - (X - h)**2/b2 - 1
    # verify with a point on the curve: vertex (1, k + a) and a general point
    P = (h, k + a)
    assert simplify(Abs(_dist(P, S1) - _dist(P, S2)) - diff_) == 0
    return _key(expr)
q("U10-F-050", TOP_SHIFT, "Locus from a focal difference", "Difficult", "Multi-step computation MCQ",
  r"A point $P$ moves so that the difference of its distances from $(1, -2)$ and $(1, 8)$ is always $6$ in absolute value. The locus of $P$ is",
  r"$\frac{(y - 3)^2}{9} - \frac{(x - 1)^2}{16} = 1$",
  [(r"$\frac{(x - 1)^2}{9} - \frac{(y - 3)^2}{16} = 1$", r"Finds $a^2 = 9$, $b^2 = 16$ and the centre, but makes the transverse axis horizontal."),
   (r"$\frac{(y - 3)^2}{16} - \frac{(x - 1)^2}{9} = 1$", r"Finds the right orientation but interchanges $a^2$ and $b^2$."),
   (r"$\frac{(y - 3)^2}{9} - \frac{(x - 1)^2}{25} = 1$", r"Takes $b = c = 5$.")],
  r"The locus is a hyperbola with these points as foci. The centre is the midpoint $(1, 3)$, the foci lie on the vertical line $x = 1$ with $2c = 10$, and $2a = 6$. So $a^2 = 9$, $b^2 = c^2 - a^2 = 16$, and the locus is $\frac{(y - 3)^2}{9} - \frac{(x - 1)^2}{16} = 1$.",
  r"Defaulting to a horizontal transverse axis.",
  "U10-F-locus-focal-diff", "Recognise the definition, then centre, orientation and $b^2$ for a shifted vertical hyperbola.",
  check=_c050, values=[_key((Y - 3)**2/9 - (X - 1)**2/16 - 1), _key((X - 1)**2/9 - (Y - 3)**2/16 - 1),
                       _key((Y - 3)**2/16 - (X - 1)**2/9 - 1), _key((Y - 3)**2/9 - (X - 1)**2/25 - 1)],
  cognitive="Analysis")
