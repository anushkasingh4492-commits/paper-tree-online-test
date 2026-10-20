import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
x, y = symbols('x y', real=True)
Z = x + I*y
_t = Symbol('t', real=True)


def msq(w):
    """|w|^2 expanded, w built from real x, y."""
    return expand(w*conjugate(w))


def msq_any(w):
    return expand(w*conjugate(w))


def circ(expr):
    """(h, k, r) of the circle expr = 0 (expr a quadratic in real x, y)."""
    P = Poly(expand(expr), x, y)
    a = P.coeff_monomial(x**2)
    D = P.coeff_monomial(x)/a; E = P.coeff_monomial(y)/a; F = P.coeff_monomial(1)/a
    h, k = -D/2, -E/2
    return (simplify(h), simplify(k), sqrt(simplify(h**2 + k**2 - F)))


def ext_on_circle(c, r, g):
    """(min, max) of |g(z)| for z on |z - c| = r, via critical points of the angle."""
    z = c + r*(cos(_t) + I*sin(_t))
    f = simplify(expand(g(z)*conjugate(g(z))))
    cr = solve(diff(f, _t), _t)
    pts = list(cr) + [s + pi for s in cr]
    vals = [simplify(nsimplify(simplify(sqrt(f.subs(_t, s))))) for s in pts]
    return (min(vals, key=lambda v: N(v)), max(vals, key=lambda v: N(v)))


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TT, FF, TF, FT = (True, True), (False, False), (True, False), (False, True)

# =================================================================== EASY

q("U02-B-001", "Modulus and argument", "Modulus of a product", "Easy", "Single-step computation MCQ",
  r"If $z = (1+i)(2-i)(3+4i)$, then $|z|$ equals",
  r"$5\sqrt{10}$",
  [(r"$7\sqrt{10}$", r"Takes $|3+4i|$ as $3 + 4 = 7$, giving $\sqrt{2}\cdot\sqrt{5}\cdot 7 = 7\sqrt{10}$."),
   (r"$250$", r"Multiplies the squared moduli $2 \cdot 5 \cdot 25 = 250$, i.e. finds $|z|^2$."),
   (r"$50$", r"Uses squared moduli for the first two factors only: $2 \cdot 5 \cdot 5 = 50$.")],
  r"$|z| = |1+i|\,|2-i|\,|3+4i| = \sqrt{2}\cdot\sqrt{5}\cdot 5 = 5\sqrt{10}$.",
  r"Adding real and imaginary parts to get the modulus, or forgetting the square root in $|a + bi| = \sqrt{a^2 + b^2}$.",
  "U02-modulus-product", r"One property, $|z_1z_2z_3| = |z_1||z_2||z_3|$, applied once.",
  check=lambda: simplify(Abs((1+I)*(2-I)*(3+4*I))),
  values=[5*sqrt(10), 7*sqrt(10), 250, 50], cognitive="Application")

q("U02-B-002", "Modulus and argument", "Principal argument, third quadrant", "Easy", "Single-step computation MCQ",
  r"The principal argument (in $(-\pi, \pi]$) of $z = -1 - i\sqrt{3}$ is",
  r"$-\frac{2\pi}{3}$",
  [(r"$\frac{\pi}{3}$", r"Uses $\tan^{-1}\sqrt{3} = \frac{\pi}{3}$ directly without locating the quadrant."),
   (r"$\frac{2\pi}{3}$", r"Ignores the sign of the imaginary part and places the point at $(-1, \sqrt{3})$ in the second quadrant."),
   (r"$\frac{4\pi}{3}$", r"Correct direction $\pi + \frac{\pi}{3}$ but outside the principal range $(-\pi, \pi]$.")],
  r"The point $(-1, -\sqrt{3})$ is in the third quadrant with reference angle $\tan^{-1}\sqrt{3} = \frac{\pi}{3}$, so the principal argument is $-\pi + \frac{\pi}{3} = -\frac{2\pi}{3}$.",
  r"Reading the argument as $\tan^{-1}\frac{y}{x}$ without checking the quadrant, or leaving it outside $(-\pi, \pi]$.",
  "U02-arg-quadrant", r"Single quadrant decision plus the principal-range rule.",
  check=lambda: arg(-1 - I*sqrt(3)),
  values=[-2*pi/3, pi/3, 2*pi/3, 4*pi/3], cognitive="Understanding")

q("U02-B-003", "Modulus and argument", "Principal argument, second quadrant", "Easy", "Single-step computation MCQ",
  r"The principal argument (in $(-\pi, \pi]$) of $z = -\sqrt{3} + i$ is",
  r"$\frac{5\pi}{6}$",
  [(r"$-\frac{\pi}{6}$", r"Takes $\tan^{-1}\left(\frac{1}{-\sqrt{3}}\right) = -\frac{\pi}{6}$ from the calculator range, which is a fourth-quadrant angle."),
   (r"$\frac{\pi}{6}$", r"Uses only the reference angle $\tan^{-1}\frac{1}{\sqrt{3}}$."),
   (r"$-\frac{5\pi}{6}$", r"Places the point in the third quadrant: $-\pi + \frac{\pi}{6}$.")],
  r"$z$ lies in the second quadrant with reference angle $\tan^{-1}\frac{1}{\sqrt{3}} = \frac{\pi}{6}$, so $\arg(z) = \pi - \frac{\pi}{6} = \frac{5\pi}{6}$.",
  r"Using $\tan^{-1}\frac{y}{x}$ blindly for a point with negative real part.",
  "U02-arg-quadrant", r"Quadrant identification and one subtraction.",
  check=lambda: arg(-sqrt(3) + I),
  values=[5*pi/6, -pi/6, pi/6, -5*pi/6], cognitive="Understanding")


def _c4():
    zz = 1 - I
    return (Abs(zz), arg(zz))
q("U02-B-004", "Modulus and argument", "Polar form with principal argument", "Easy", "Single-step computation MCQ",
  r"The polar form of $z = 1 - i$, written with the argument equal to the principal value in $(-\pi, \pi]$, is",
  r"$\sqrt{2}\left(\cos\left(-\frac{\pi}{4}\right) + i\sin\left(-\frac{\pi}{4}\right)\right)$",
  [(r"$\sqrt{2}\left(\cos\frac{\pi}{4} + i\sin\frac{\pi}{4}\right)$", r"Ignores the negative imaginary part; this is $1 + i$."),
   (r"$\sqrt{2}\left(\cos\frac{7\pi}{4} + i\sin\frac{7\pi}{4}\right)$", r"Uses the argument $\frac{7\pi}{4}$ from $[0, 2\pi)$, not the principal value."),
   (r"$2\left(\cos\left(-\frac{\pi}{4}\right) + i\sin\left(-\frac{\pi}{4}\right)\right)$", r"Takes the modulus as $1 + 1 = 2$.")],
  r"$|z| = \sqrt{1 + 1} = \sqrt{2}$ and the point $(1, -1)$ is in the fourth quadrant with reference angle $\frac{\pi}{4}$, so the principal argument is $-\frac{\pi}{4}$. Hence $z = \sqrt{2}\left(\cos\left(-\frac{\pi}{4}\right) + i\sin\left(-\frac{\pi}{4}\right)\right)$.",
  r"Giving an argument outside $(-\pi, \pi]$, or dropping the square root in the modulus.",
  "U02-polar-form", r"Modulus and principal argument of one number.",
  check=_c4,
  values=[(sqrt(2), -pi/4), (sqrt(2), pi/4), (sqrt(2), 7*pi/4), (2, -pi/4)], cognitive="Understanding")

q("U02-B-005", "Argand plane", "Distance between two points", "Easy", "Single-step computation MCQ",
  r"The distance between the points representing $z_1 = 3 + 2i$ and $z_2 = -1 - i$ in the Argand plane is",
  r"$5$",
  [(r"$\sqrt{5}$", r"Computes $|z_1 + z_2| = |2 + i| = \sqrt{5}$ instead of $|z_1 - z_2|$."),
   (r"$7$", r"Adds the coordinate differences $4 + 3 = 7$ without squaring."),
   (r"$25$", r"Gives $|z_1 - z_2|^2 = 16 + 9$.")],
  r"Distance $= |z_1 - z_2| = |4 + 3i| = \sqrt{16 + 9} = 5$.",
  r"Using $|z_1 + z_2|$ for the distance.", "U02-distance",
  r"Direct use of $|z_1 - z_2|$ as distance.",
  check=lambda: Abs((3 + 2*I) - (-1 - I)),
  values=[5, sqrt(5), 7, 25], cognitive="Application")

q("U02-B-006", "Loci in the Argand plane", "Circle in modulus form", "Easy", "Direct concept MCQ",
  r"The locus of $z$ satisfying $|z - 2 + i| = 3$ is a circle with",
  r"centre $(2, -1)$ and radius $3$",
  [(r"centre $(-2, 1)$ and radius $3$", r"Reads the centre as $-2 + i$, copying the signs as written in $z - 2 + i$."),
   (r"centre $(2, -1)$ and radius $9$", r"Takes $r^2 = 9$ as the radius."),
   (r"centre $(2, 1)$ and radius $3$", r"Drops the sign of the imaginary part of the centre $2 - i$.")],
  r"$|z - 2 + i| = |z - (2 - i)|$, the distance of $z$ from $2 - i$. So the locus is the circle with centre $(2, -1)$ and radius $3$.",
  r"Misreading the centre $z_0$ from $|z - z_0| = r$ when $z_0$ is written with mixed signs.",
  "U02-locus-circle", r"Single recognition of $|z - z_0| = r$.",
  check=lambda: circ(msq(Z - 2 + I) - 9),
  values=[(2, -1, 3), (-2, 1, 3), (2, -1, 9), (2, 1, 3)], cognitive="Understanding")

q("U02-B-007", "Loci in the Argand plane", "Perpendicular bisector", "Easy", "Single-step computation MCQ",
  r"If $z = x + iy$ satisfies $|z - 1| = |z + i|$, then the locus of $z$ is the line",
  r"$y = -x$",
  [(r"$y = x$", r"Takes the point $-i$ as $i$; $|z - 1| = |z - i|$ gives $y = x$."),
   (r"$x + y = 1$", r"Takes $-i$ as $i$ and joins $1$ and $i$ instead of bisecting."),
   (r"$x - y = 1$", r"Joins the two points $1$ and $-i$, i.e. $(1, 0)$ and $(0, -1)$, instead of bisecting them.")],
  r"$(x - 1)^2 + y^2 = x^2 + (y + 1)^2$ gives $-2x + 1 = 2y + 1$, so $y = -x$. This is the perpendicular bisector of the segment joining $1$ and $-i$.",
  r"Confusing the perpendicular bisector of $z_1 z_2$ with the line through $z_1$ and $z_2$.",
  "U02-locus-perp-bisector", r"One expansion of $|z - a| = |z - b|$.",
  check=lambda: solve(msq(Z - 1) - msq(Z + I), y)[0],
  values=[-x, x, 1 - x, x - 1], cognitive="Application")


def _c8():
    th = Symbol('t', real=True)
    zz = 3*(cos(th) + I*sin(th))
    return simplify(1/zz)
_th8 = Symbol('t', real=True)
_z8 = 3*(cos(_th8) + I*sin(_th8))
q("U02-B-008", "Modulus and argument", "Using |z|^2 = z conj(z)", "Easy", "Single-step computation MCQ",
  r"If $|z| = 3$, then $\frac{1}{z}$ equals",
  r"$\frac{\overline{z}}{9}$",
  [(r"$\frac{\overline{z}}{3}$", r"Divides by $|z| = 3$ instead of $|z|^2 = 9$."),
   (r"$\frac{z}{9}$", r"Forgets to conjugate: uses $z$ in place of $\overline{z}$."),
   (r"$9\overline{z}$", r"Inverts the factor, multiplying by $|z|^2$ instead of dividing.")],
  r"Since $z\overline{z} = |z|^2 = 9$, we get $\frac{1}{z} = \frac{\overline{z}}{z\overline{z}} = \frac{\overline{z}}{9}$.",
  r"Using $|z|$ in place of $|z|^2$ in the identity $z\overline{z} = |z|^2$.",
  "U02-mod-conj-identity", r"One identity, $z\overline{z} = |z|^2$, applied once.",
  check=_c8,
  values=[conjugate(_z8)/9, conjugate(_z8)/3, _z8/9, 9*conjugate(_z8)], cognitive="Understanding")

q("U02-B-009", "Loci in the Argand plane", "Locus from an Im condition", "Easy", "Single-step computation MCQ",
  r"The locus of $z = x + iy$ satisfying $\operatorname{Im}(z^2) = 4$ is",
  r"$xy = 2$",
  [(r"$xy = 4$", r"Takes $\operatorname{Im}(z^2)$ as $xy$, dropping the factor $2$."),
   (r"$x^2 - y^2 = 4$", r"Uses the real part $x^2 - y^2$ of $z^2$."),
   (r"$x^2 + y^2 = 4$", r"Treats $\operatorname{Im}(z^2)$ as $|z|^2$.")],
  r"$z^2 = x^2 - y^2 + 2ixy$, so $\operatorname{Im}(z^2) = 2xy = 4$, i.e. $xy = 2$, a rectangular hyperbola.",
  r"Dropping the factor $2$ in $2xy$ or mixing up the real and imaginary parts of $z^2$.",
  "U02-locus-re-im", r"Expand $z^2$ once and read the imaginary part.",
  check=lambda: expand((im(expand(Z**2)) - 4)/2),
  values=[x*y - 2, x*y - 4, x**2 - y**2 - 4, x**2 + y**2 - 4], cognitive="Application")


def _c10():
    return ext_on_circle(0, 4, lambda w: 3 - w)[1]
q("U02-B-010", "Triangle inequality", "Greatest value of |z1 - z2|", "Easy", "Single-step computation MCQ",
  r"If $|z_1| = 3$ and $|z_2| = 4$, then the greatest possible value of $|z_1 - z_2|$ is",
  r"$7$",
  [(r"$1$", r"Gives the least value $|4 - 3| = 1$."),
   (r"$5$", r"Assumes $z_1$ and $z_2$ are perpendicular: $\sqrt{9 + 16} = 5$."),
   (r"$\sqrt{7}$", r"Takes the square root of the sum of the moduli, $\sqrt{3 + 4}$.")],
  r"By the triangle inequality $|z_1 - z_2| \le |z_1| + |z_2| = 7$, with equality when $z_2 = -\frac{4}{3}z_1$ (opposite directions). So the greatest value is $7$.",
  r"Confusing the greatest value of $|z_1 - z_2|$ with the least value or with the perpendicular case.",
  "U02-triangle-ineq-basic", r"One application of $|z_1 - z_2| \le |z_1| + |z_2|$ with its equality case.",
  check=_c10,
  values=[7, 1, 5, sqrt(7)], cognitive="Application")

q("U02-B-011", "Modulus and argument", "Modulus of a quotient of powers", "Easy", "Single-step computation MCQ",
  r"If $z = \frac{(\sqrt{3} + i)^4}{(1 - i)^6}$, then $|z|$ equals",
  r"$2$",
  [(r"$\frac{1}{2}$", r"Inverts the quotient: $\frac{8}{16}$."),
   (r"$\frac{1}{4}$", r"Takes $|1 - i|^6$ as $2^6 = 64$, forgetting the square root, so $\frac{16}{64}$."),
   (r"$32$", r"Takes $|\sqrt{3} + i|^4$ as $4^4 = 256$, forgetting the square root, so $\frac{256}{8}$.")],
  r"$|\sqrt{3} + i| = 2$ and $|1 - i| = \sqrt{2}$, so $|z| = \frac{2^4}{(\sqrt{2})^6} = \frac{16}{8} = 2$.",
  r"Using $|w|^2$ in place of $|w|$ when raising to powers.",
  "U02-modulus-quotient", r"Two moduli and one division.",
  check=lambda: simplify(Abs((sqrt(3) + I)**4/(1 - I)**6)),
  values=[2, Rational(1, 2), Rational(1, 4), 32], cognitive="Application")

q("U02-B-012", "Modulus and argument", "Argument of minus the conjugate", "Easy", "Single-step computation MCQ",
  r"If the principal argument of a complex number $z$ is $\frac{\pi}{3}$, then the principal argument (in $(-\pi, \pi]$) of $-\overline{z}$ is",
  r"$\frac{2\pi}{3}$",
  [(r"$-\frac{2\pi}{3}$", r"Finds the argument of $-z$, namely $\frac{\pi}{3} - \pi$, not of $-\overline{z}$."),
   (r"$-\frac{\pi}{3}$", r"Takes the argument of $\overline{z}$ and ignores the minus sign."),
   (r"$\frac{4\pi}{3}$", r"Ignores the conjugate, adds $\pi$ to $\frac{\pi}{3}$ and does not reduce into $(-\pi, \pi]$.")],
  r"$\overline{z}$ has argument $-\frac{\pi}{3}$; multiplying by $-1$ adds $\pi$, giving $\frac{2\pi}{3}$, which is already in $(-\pi, \pi]$. Equivalently, $-\overline{z}$ is the reflection of $z$ in the imaginary axis.",
  r"Mixing up $-z$, $\overline{z}$ and $-\overline{z}$.",
  "U02-arg-conj-neg", r"Two simple transformations of the argument.",
  check=lambda: arg(-conjugate(cos(pi/3) + I*sin(pi/3))),
  values=[2*pi/3, -2*pi/3, -pi/3, 4*pi/3], cognitive="Understanding")


def _c13():
    w = expand((1 - 2*I)**2)
    a, b = re(w), im(w)
    if a > 0 and b > 0: return 1
    if a < 0 and b > 0: return 2
    if a < 0 and b < 0: return 3
    return 4
q("U02-B-013", "Argand plane", "Quadrant of a point", "Easy", "Single-step computation MCQ",
  r"The point representing $z = (1 - 2i)^2$ in the Argand plane lies in the",
  r"third quadrant",
  [(r"fourth quadrant", r"Takes $i^2 = +1$, getting $1 - 4i + 4 = 5 - 4i$."),
   (r"second quadrant", r"Drops the minus sign of the middle term, getting $1 + 4i - 4 = -3 + 4i$."),
   (r"first quadrant", r"Makes both slips, $i^2 = +1$ and a $+$ middle term, getting $5 + 4i$.")],
  r"$(1 - 2i)^2 = 1 - 4i + 4i^2 = -3 - 4i$. Both coordinates are negative, so the point $(-3, -4)$ is in the third quadrant.",
  r"Sign slips when squaring a binomial containing $i$.", "U02-argand-quadrant",
  r"One expansion and a sign reading.",
  check=_c13, values=[3, 4, 2, 1], cognitive="Application")


def _c14():
    w = solve(Symbol('s')**2 + Symbol('s') + 1, Symbol('s'))[0]
    return simplify(expand((1 + w - w**2)*(1 - w + w**2)))
q("U02-B-014", "Cube roots of unity", "Simplifying an expression in omega", "Easy", "Single-step computation MCQ",
  r"If $\omega$ is a root of $x^2 + x + 1 = 0$, then $(1 + \omega - \omega^2)(1 - \omega + \omega^2)$ equals",
  r"$4$",
  [(r"$-4$", r"Sign slip in one bracket, writing $1 - \omega + \omega^2 = 2\omega$, so the product is $(-2\omega^2)(2\omega) = -4$."),
   (r"$0$", r"Replaces each bracket by $1 + \omega + \omega^2 = 0$."),
   (r"$2$", r"Writes $1 - \omega + \omega^2$ as $-\omega$, dropping the $-\omega$ term, so the product is $(-2\omega^2)(-\omega) = 2$.")],
  r"From $1 + \omega + \omega^2 = 0$: $1 + \omega - \omega^2 = -2\omega^2$ and $1 - \omega + \omega^2 = -2\omega$. The product is $4\omega^3 = 4$, since $\omega^3 = 1$.",
  r"Sign errors when replacing $1 + \omega$ by $-\omega^2$ or $1 + \omega^2$ by $-\omega$.",
  "U02-omega-product", r"One identity, $1 + \omega + \omega^2 = 0$, used twice.",
  check=_c14, values=[4, -4, 0, 2], cognitive="Application")


def _c15():
    p = [(1, 1), (4, 1), (1, 5)]
    s = sum(p[i][0]*p[(i+1) % 3][1] - p[(i+1) % 3][0]*p[i][1] for i in range(3))
    return Abs(Rational(s, 2))
q("U02-B-015", "Argand plane", "Area of a triangle from given points", "Easy", "Single-step computation MCQ",
  r"The area of the triangle whose vertices are the points representing $z_1 = 1 + i$, $z_2 = 4 + i$ and $z_3 = 1 + 5i$ is",
  r"$6$",
  [(r"$12$", r"Forgets the factor $\frac{1}{2}$: $3 \cdot 4 = 12$."),
   (r"$\frac{15}{2}$", r"Takes $\frac{1}{2}$ of the hypotenuse $5$ times the leg $3$."),
   (r"$10$", r"Takes $\frac{1}{2}$ of the hypotenuse $5$ times the leg $4$.")],
  r"$z_2 - z_1 = 3$ (horizontal) and $z_3 - z_1 = 4i$ (vertical), so the triangle is right-angled at $z_1$ with legs $3$ and $4$. Area $= \frac{1}{2}\cdot 3 \cdot 4 = 6$.",
  r"Using the hypotenuse $|z_3 - z_2|$ as a base with a leg as the height.",
  "U02-area-triangle", r"Reading two perpendicular legs and one formula.",
  check=_c15, values=[6, 12, Rational(15, 2), 10], cognitive="Application",
  numerical=dict(question=r"The area of the triangle whose vertices are the points representing $z_1 = 1 + i$, $z_2 = 4 + i$ and $z_3 = 1 + 5i$ in the Argand plane is", answer=6))

q("U02-B-016", "Triangle inequality", "Least modulus on a circle", "Easy", "Single-step computation MCQ",
  r"If $|z - 3| = 2$, then the least value of $|z|$ is",
  r"$1$",
  [(r"$2$", r"Gives the radius $2$."),
   (r"$3$", r"Gives the distance $3$ of the centre from the origin."),
   (r"$5$", r"Gives the greatest value $3 + 2$.")],
  r"$|z| \ge |3| - |z - 3| = 3 - 2 = 1$, with equality at $z = 1$, which lies on the circle. So the least value is $1$.",
  r"Confusing the least value of $|z|$ with the greatest value or with the radius.",
  "U02-extremal-circle", r"One step of the reverse triangle inequality.",
  check=lambda: ext_on_circle(3, 2, lambda w: w)[0],
  values=[1, 2, 3, 5], cognitive="Application")


def _c17():
    import random
    rnd = random.Random(3)
    ok1 = True
    for _ in range(30):
        a = rnd.randint(-9, 9) + I*rnd.randint(-9, 9); b = rnd.randint(-9, 9) + I*rnd.randint(-9, 9)
        if N(Abs(a + b)) > N(Abs(a) + Abs(b)) + 1e-12: ok1 = False
    z1, z2 = Integer(1), Integer(2)   # counterexample for II
    ok2 = not (Abs(z1 + z2) == Abs(z1) + Abs(z2) and z1 != z2)
    return (ok1, ok2)
q("U02-B-017", "Triangle inequality", "Equality case of the triangle inequality", "Easy", "Statement-based MCQ",
  r"Consider the following statements about complex numbers. Statement I: For all complex numbers $z_1, z_2$, $|z_1 + z_2| \le |z_1| + |z_2|$. Statement II: If $z_1, z_2$ are nonzero and $|z_1 + z_2| = |z_1| + |z_2|$, then $z_1 = z_2$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Reads the equality case as $z_1 = z_2$ instead of $z_1 = kz_2$ with $k > 0$."),
   (ST_FF, r"Doubts the triangle inequality for complex numbers and rejects Statement II as well."),
   (ST_FT, r"Doubts the triangle inequality and reads the equality case as $z_1 = z_2$.")],
  r"Statement I is the triangle inequality, always true. For Statement II, equality holds exactly when $z_1$ and $z_2$ point in the same direction, i.e. $z_1 = kz_2$ with $k > 0$; for example $z_1 = 1, z_2 = 2$ gives $|3| = 1 + 2$ but $z_1 \ne z_2$. So Statement II is false.",
  r"Equality in $|z_1 + z_2| \le |z_1| + |z_2|$ means equal arguments, not equal numbers.",
  "U02-triangle-ineq-statements", r"Recall of the inequality and its equality case.",
  check=_c17, values=[TF, TT, FF, FT], cognitive="Understanding")

# ================================================================= MEDIUM


def _c18():
    sols = solve([x**2 + y**2 - 1, msq(1 + Z) - 3], [x, y], dict=True)
    vals = {simplify(Abs(1 - Z.subs(s))) for s in sols}
    assert len(vals) == 1
    return vals.pop()
q("U02-B-018", "Modulus and argument", "Parallelogram law", "Medium", "Multi-step computation MCQ",
  r"If $|z_1| = |z_2| = 1$ and $|z_1 + z_2| = \sqrt{3}$, then $|z_1 - z_2|$ equals",
  r"$1$",
  [(r"$\sqrt{2}$", r"Assumes $z_1 \perp z_2$, so $|z_1 - z_2|^2 = 1 + 1 = 2$."),
   (r"$\sqrt{7}$", r"Adds $|z_1 + z_2|^2$ instead of subtracting: $2(1 + 1) + 3 = 7$."),
   (r"$\sqrt{5}$", r"Drops the factor $2$ and adds: $1 + 1 + 3 = 5$.")],
  r"$|z_1 + z_2|^2 + |z_1 - z_2|^2 = 2(|z_1|^2 + |z_2|^2) = 4$. Hence $|z_1 - z_2|^2 = 4 - 3 = 1$ and $|z_1 - z_2| = 1$.",
  r"Misremembering $|z_1 + z_2|^2 + |z_1 - z_2|^2 = 2(|z_1|^2 + |z_2|^2)$.",
  "U02-parallelogram-law", r"Needs the parallelogram identity $|z_1+z_2|^2 + |z_1-z_2|^2 = 2(|z_1|^2+|z_2|^2)$ and one substitution.",
  check=_c18, values=[1, sqrt(2), sqrt(7), sqrt(5)], cognitive="Application")

q("U02-B-019", "Modulus and argument", "Argument of a product, principal adjustment", "Medium", "Multi-step computation MCQ",
  r"If $z_1 = -1 + i$ and $z_2 = -\sqrt{3} + i$, then the principal argument (in $(-\pi, \pi]$) of $z_1 z_2$ is",
  r"$-\frac{5\pi}{12}$",
  [(r"$\frac{19\pi}{12}$", r"Adds $\frac{3\pi}{4} + \frac{5\pi}{6}$ but does not reduce into $(-\pi, \pi]$."),
   (r"$\frac{5\pi}{12}$", r"Adds only the reference angles $\frac{\pi}{4} + \frac{\pi}{6}$."),
   (r"$-\frac{\pi}{12}$", r"Subtracts the arguments as for a quotient: $\frac{3\pi}{4} - \frac{5\pi}{6}$.")],
  r"$\arg z_1 = \frac{3\pi}{4}$ and $\arg z_2 = \frac{5\pi}{6}$. Their sum is $\frac{19\pi}{12} > \pi$, so subtract $2\pi$: $\arg(z_1z_2) = \frac{19\pi}{12} - 2\pi = -\frac{5\pi}{12}$. Check: $z_1z_2 = (\sqrt{3} - 1) - (\sqrt{3} + 1)i$ lies in the fourth quadrant.",
  r"Forgetting that $\arg(z_1z_2) = \arg z_1 + \arg z_2$ holds only up to a multiple of $2\pi$.",
  "U02-arg-product-principal", r"Two arguments, a sum, and a range adjustment.",
  check=lambda: arg(expand((-1 + I)*(-sqrt(3) + I))),
  values=[-5*pi/12, 19*pi/12, 5*pi/12, -pi/12], cognitive="Application")

q("U02-B-020", "Modulus and argument", "Argument of a quotient, principal adjustment", "Medium", "Multi-step computation MCQ",
  r"If $z_1 = -1 - i$ and $z_2 = 1 + i\sqrt{3}$, then the principal argument (in $(-\pi, \pi]$) of $\frac{z_1}{z_2}$ is",
  r"$\frac{11\pi}{12}$",
  [(r"$-\frac{13\pi}{12}$", r"Computes $-\frac{3\pi}{4} - \frac{\pi}{3}$ but does not add $2\pi$ to return to $(-\pi, \pi]$."),
   (r"$-\frac{\pi}{12}$", r"Takes $\arg z_1 = \tan^{-1}1 = \frac{\pi}{4}$, ignoring the third quadrant: $\frac{\pi}{4} - \frac{\pi}{3}$."),
   (r"$\frac{5\pi}{12}$", r"Places $z_1$ in the second quadrant with argument $\frac{3\pi}{4}$: $\frac{3\pi}{4} - \frac{\pi}{3}$.")],
  r"$\arg z_1 = -\frac{3\pi}{4}$ and $\arg z_2 = \frac{\pi}{3}$. Then $\arg z_1 - \arg z_2 = -\frac{13\pi}{12} < -\pi$, so add $2\pi$ to get $\frac{11\pi}{12}$.",
  r"Not adjusting $\arg z_1 - \arg z_2$ into the principal range $(-\pi, \pi]$.",
  "U02-arg-quotient-principal", r"Two quadrant decisions and a range adjustment.",
  check=lambda: arg(simplify((-1 - I)/(1 + I*sqrt(3)))),
  values=[11*pi/12, -13*pi/12, -pi/12, 5*pi/12], cognitive="Application")


def _c21():
    lo, hi = ext_on_circle(3 - 4*I, 2, lambda w: w)
    return lo + hi
q("U02-B-021", "Triangle inequality", "Sum of greatest and least modulus", "Medium", "Multi-step computation MCQ",
  r"If $|z - 3 + 4i| = 2$, then the sum of the greatest and the least values of $|z|$ is",
  r"$10$",
  [(r"$4$", r"Gives the difference $7 - 3$."),
   (r"$7$", r"Gives only the greatest value $5 + 2$."),
   (r"$14$", r"Takes both extreme values as $|3 - 4i| + 2 = 7$.")],
  r"$z$ lies on the circle with centre $3 - 4i$ (distance $5$ from the origin) and radius $2$. So $5 - 2 \le |z| \le 5 + 2$, both attained on the line through the origin and the centre. The sum is $3 + 7 = 10$.",
  r"Treating the radius as if it only adds to the distance $|z_0|$ of the centre.",
  "U02-extremal-circle", r"Distance of the centre, then two extremes $|z_0| \pm r$, then their sum.",
  check=_c21, values=[10, 4, 7, 14], cognitive="Application",
  numerical=dict(question=r"If $|z - 3 + 4i| = 2$, then the sum of the greatest and the least values of $|z|$ is", answer=10))

q("U02-B-022", "Triangle inequality", "Least distance from a point to a circle", "Medium", "Multi-step computation MCQ",
  r"If $|z - 1 - i| = 1$, then the least value of $|z - 4 - 5i|$ is",
  r"$4$",
  [(r"$6$", r"Gives the greatest value $5 + 1$."),
   (r"$5$", r"Gives the distance $|3 + 4i|$ between the centre $1 + i$ and $4 + 5i$."),
   (r"$\sqrt{41} - 1$", r"Measures from the origin instead of the centre: $|4 + 5i| - 1$.")],
  r"The circle has centre $1 + i$ and radius $1$. The distance from the centre to $4 + 5i$ is $|3 + 4i| = 5$, so the least value of $|z - (4 + 5i)|$ is $5 - 1 = 4$.",
  r"Measuring from the origin instead of from the centre of the circle.",
  "U02-extremal-point-circle", r"Identify the centre, compute a distance, subtract the radius.",
  check=lambda: ext_on_circle(1 + I, 1, lambda w: w - 4 - 5*I)[0],
  values=[4, 6, 5, sqrt(41) - 1], cognitive="Application",
  numerical=dict(question=r"If $|z - 1 - i| = 1$, then the least value of $|z - 4 - 5i|$ is", answer=4))

q("U02-B-023", "Loci in the Argand plane", "Circle of the form |z - a| = k|z - b|", "Medium", "Multi-step computation MCQ",
  r"The locus of $z$ satisfying $|z - 2| = 2|z - 1|$ is a circle with",
  r"centre $\left(\frac{2}{3}, 0\right)$ and radius $\frac{2}{3}$",
  [(r"centre $\left(\frac{4}{3}, 0\right)$ and radius $\frac{4}{3}$", r"Uses the coefficient $\frac{4}{3}$ of $x$ as the centre without halving."),
   (r"centre $\left(-\frac{2}{3}, 0\right)$ and radius $\frac{2}{3}$", r"Sign slip when completing the square in $x^2 - \frac{4}{3}x$."),
   (r"centre $\left(\frac{2}{3}, 0\right)$ and radius $\frac{4}{9}$", r"Gives $r^2 = \frac{4}{9}$ as the radius.")],
  r"With $z = x + iy$: $(x - 2)^2 + y^2 = 4[(x - 1)^2 + y^2]$, i.e. $3x^2 + 3y^2 - 4x = 0$, or $x^2 + y^2 - \frac{4}{3}x = 0$. Centre $\left(\frac{2}{3}, 0\right)$, radius $\frac{2}{3}$.",
  r"Errors in completing the square after dividing by $3$.",
  "U02-locus-apollonius", r"Expansion, division by $3$ and completing the square.",
  check=lambda: circ(msq(Z - 2) - 4*msq(Z - 1)),
  values=[(Rational(2, 3), 0, Rational(2, 3)), (Rational(4, 3), 0, Rational(4, 3)),
          (Rational(-2, 3), 0, Rational(2, 3)), (Rational(2, 3), 0, Rational(4, 9))], cognitive="Application")

q("U02-B-024", "Loci in the Argand plane", "Locus from a sum of squared distances", "Medium", "Multi-step computation MCQ",
  r"The locus of $z$ satisfying $|z - 1|^2 + |z + 1|^2 = 4$ is a circle with centre at the origin and radius",
  r"$1$",
  [(r"$\sqrt{2}$", r"Writes the left side as $2|z|^2$, forgetting the constant $2$, so $|z|^2 = 2$."),
   (r"$2$", r"Drops both constants and the factor $2$, getting $|z|^2 = 4$."),
   (r"$\sqrt{3}$", r"Adds the two expansions as $|z|^2 + 1$, dropping the factor $2$ and one constant, so $|z|^2 = 3$.")],
  r"$|z - 1|^2 + |z + 1|^2 = 2|z|^2 + 2$. Setting this equal to $4$ gives $|z|^2 = 1$, so the locus is $|z| = 1$.",
  r"Dropping the constant terms $|1|^2$ when expanding $|z \pm 1|^2$.",
  "U02-locus-sum-squares", r"Expansion with $z\overline{z} = |z|^2$ and simplification.",
  check=lambda: circ(msq(Z - 1) + msq(Z + 1) - 4)[2],
  values=[1, sqrt(2), 2, sqrt(3)], cognitive="Application")


def _c25():
    num, den = fraction(together(simplify(re(1/Z)) - Rational(1, 2)))
    # den = 2(x^2+y^2) > 0 off the origin, so the region is num > 0
    expr, sgn = expand(num), 1
    a = Poly(expr, x, y).coeff_monomial(x**2)
    if a < 0:
        expr, sgn = -expr, -1
        a = -a
    return (expand(expr/a), sgn)
q("U02-B-025", "Loci in the Argand plane", "Region defined by Re(1/z)", "Medium", "Graph/diagram MCQ",
  r"For $z \ne 0$, the set of points $z$ satisfying $\operatorname{Re}\left(\frac{1}{z}\right) > \frac{1}{2}$ is the",
  r"interior of the circle $|z - 1| = 1$",
  [(r"exterior of the circle $|z - 1| = 1$", r"Reverses the inequality when clearing the denominator, getting $x^2 + y^2 - 2x > 0$."),
   (r"interior of the circle $|z - 2| = 2$", r"Clears the denominator as $x > \frac{x^2 + y^2}{4}$, i.e. uses $\frac{1}{4}$ for $\frac{1}{2}$, getting $x^2 + y^2 < 4x$."),
   (r"half-plane $\operatorname{Re}(z) < 2$", r"Treats $\operatorname{Re}\left(\frac{1}{z}\right)$ as $\frac{1}{x}$ and inverts $\frac{1}{x} > \frac{1}{2}$ to $x < 2$.")],
  r"$\operatorname{Re}\left(\frac{1}{z}\right) = \frac{x}{x^2 + y^2} > \frac{1}{2}$ gives $x^2 + y^2 - 2x < 0$, i.e. $(x - 1)^2 + y^2 < 1$. This is the interior of the circle $|z - 1| = 1$ (the origin is on its boundary).",
  r"Treating $\operatorname{Re}\left(\frac{1}{z}\right)$ as $\frac{1}{\operatorname{Re}(z)}$.",
  "U02-region-reciprocal", r"Rationalise, clear a positive denominator $x^2 + y^2$, complete the square.",
  check=_c25,
  values=[(x**2 + y**2 - 2*x, -1), (x**2 + y**2 - 2*x, 1), (x**2 + y**2 - 4*x, -1), (x - 2, -1)], cognitive="Analysis")


def _c26():
    num, den = fraction(together(simplify(re((Z - 2*I)/(Z + 2)))))
    return circ(num)
q("U02-B-026", "Loci in the Argand plane", "Locus from Re of a quotient", "Medium", "Multi-step computation MCQ",
  r"If $z \ne -2$ and $\operatorname{Re}\left(\frac{z - 2i}{z + 2}\right) = 0$, then $z$ lies on the circle with",
  r"centre $(-1, 1)$ and radius $\sqrt{2}$",
  [(r"centre $(1, -1)$ and radius $\sqrt{2}$", r"Sign slip in both coordinates when completing the square in $x^2 + y^2 + 2x - 2y = 0$."),
   (r"centre $(-1, 1)$ and radius $2$", r"Takes $r^2 = 2$ as the radius."),
   (r"centre $(-1, -1)$ and radius $\sqrt{2}$", r"Uses $z + 2i$ in place of $z - 2i$, getting $x^2 + y^2 + 2x + 2y = 0$.")],
  r"With $z = x + iy$, the real part of $\frac{z - 2i}{z + 2}$ has numerator $\operatorname{Re}\left[(x + i(y - 2))((x + 2) - iy)\right] = x(x + 2) + y(y - 2)$. Setting it to $0$: $x^2 + y^2 + 2x - 2y = 0$, centre $(-1, 1)$, radius $\sqrt{2}$.",
  r"Sign errors in the real part of the product with $\overline{z + 2}$.",
  "U02-locus-purely-imaginary", r"Multiply by the conjugate, extract the real part, identify the circle.",
  check=_c26,
  values=[(-1, 1, sqrt(2)), (1, -1, sqrt(2)), (-1, 1, 2), (-1, -1, sqrt(2))], cognitive="Application")


def _c27():
    r = Symbol('r', positive=True)
    X = 1 + r*cos(pi/4); Y = r*sin(pi/4)
    slope = simplify(diff(Y, r)/diff(X, r))
    icpt = simplify(Y - slope*X)
    side = sign(simplify(X - 1))
    return (slope, icpt, side)
q("U02-B-027", "Loci in the Argand plane", "Locus from an argument condition", "Medium", "Conceptual/application MCQ",
  r"The locus of $z = x + iy$ satisfying $\arg(z - 1) = \frac{\pi}{4}$ is",
  r"the part of the line $y = x - 1$ for which $x > 1$",
  [(r"the whole line $y = x - 1$", r"Includes the opposite ray, on which $\arg(z - 1) = -\frac{3\pi}{4}$."),
   (r"the part of the line $y = x - 1$ for which $x < 1$", r"Takes the ray in the wrong direction, which has $\arg(z - 1) = -\frac{3\pi}{4}$."),
   (r"the part of the line $y = x + 1$ for which $x > -1$", r"Uses $z + 1$ instead of $z - 1$, i.e. a ray from $-1$.")],
  r"$z - 1 = t\left(\cos\frac{\pi}{4} + i\sin\frac{\pi}{4}\right)$ with $t > 0$, so $x = 1 + \frac{t}{\sqrt{2}}$, $y = \frac{t}{\sqrt{2}}$. Thus $y = x - 1$ with $x > 1$; the point $z = 1$ is excluded since $\arg 0$ is undefined.",
  r"Treating $\arg(z - z_0) = \theta$ as a full line instead of a ray from $z_0$.",
  "U02-locus-arg-ray", r"Converting an argument condition to a ray and fixing its direction.",
  check=_c27,
  values=[(1, -1, 1), (1, -1, 0), (1, -1, -1), (1, 1, 1)], cognitive="Understanding")

q("U02-B-028", "Modulus and argument", "Principal argument from a non-standard polar form", "Medium", "Multi-step computation MCQ",
  r"The principal argument (in $(-\pi, \pi]$) of $z = -2\left(\cos\frac{\pi}{5} - i\sin\frac{\pi}{5}\right)$ is",
  r"$\frac{4\pi}{5}$",
  [(r"$\frac{\pi}{5}$", r"Reads the angle $\frac{\pi}{5}$ shown in the brackets as the argument."),
   (r"$-\frac{\pi}{5}$", r"Accounts for the minus inside the bracket but ignores the factor $-2$."),
   (r"$-\frac{4\pi}{5}$", r"Places $z$ in the third quadrant, taking $\frac{\pi}{5} - \pi$.")],
  r"$z = -2\cos\frac{\pi}{5} + 2i\sin\frac{\pi}{5}$ has negative real part and positive imaginary part, so it is in the second quadrant. Writing $z = 2\left(\cos\left(\pi - \frac{\pi}{5}\right) + i\sin\left(\pi - \frac{\pi}{5}\right)\right)$ gives $\arg z = \frac{4\pi}{5}$.",
  r"Taking the angle in a non-standard form $-r(\cos\theta - i\sin\theta)$ as the argument.",
  "U02-polar-nonstandard", r"Recognise the non-standard form, locate the quadrant, rewrite as $r(\cos\theta + i\sin\theta)$.",
  check=lambda: arg(-2*(cos(pi/5) - I*sin(pi/5))),
  values=[4*pi/5, pi/5, -pi/5, -4*pi/5], cognitive="Analysis")


def _c29():
    z1 = cos(2*pi/3) + I*sin(2*pi/3); z2 = I
    s1 = bool(simplify(arg(expand(z1*z2)) - 7*pi/6) == 0)
    samples = [1 + I, -2 + 3*I, -1 - I, 3 - 4*I, 5, 2*I, -3*I]
    s2 = all(simplify(arg(simplify(1/w)) + arg(w)) == 0 for w in samples)
    return (s1, s2)
q("U02-B-029", "Modulus and argument", "Principal argument of products and reciprocals", "Medium", "Statement-based MCQ",
  r"Arguments are principal values in $(-\pi, \pi]$. Statement I: If $\arg(z_1) = \frac{2\pi}{3}$ and $\arg(z_2) = \frac{\pi}{2}$, then $\arg(z_1z_2) = \frac{7\pi}{6}$. Statement II: If $z$ is nonzero and not a negative real number, then $\arg\left(\frac{1}{z}\right) = -\arg(z)$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts $\frac{7\pi}{6}$ without reducing it into $(-\pi, \pi]$."),
   (ST_FF, r"Rejects Statement I correctly but thinks $\arg\left(\frac{1}{z}\right) = -\arg z$ also fails for non-real $z$."),
   (ST_TF, r"Accepts $\frac{7\pi}{6}$ and also thinks $\arg\left(\frac{1}{z}\right) \ne -\arg z$.")],
  r"In Statement I, $\frac{2\pi}{3} + \frac{\pi}{2} = \frac{7\pi}{6} > \pi$, so the principal argument is $\frac{7\pi}{6} - 2\pi = -\frac{5\pi}{6}$; Statement I is false. In Statement II, $\frac{1}{z} = \frac{\overline{z}}{|z|^2}$ has the argument of $\overline{z}$, which is $-\arg z$ whenever $\arg z \ne \pi$; Statement II is true.",
  r"Forgetting the principal-range reduction for $\arg z_1 + \arg z_2$.",
  "U02-arg-product-statements", r"Two separate argument facts with a range trap.",
  check=_c29, values=[FT, TT, FF, TF], cognitive="Analysis")


def _c30():
    z1 = 1 + I*sqrt(3)
    sols = solve([msq(Z) - 9, msq(z1 + Z) - 25], [x, y], dict=True)
    assert len(sols) == 1
    return simplify(Z.subs(sols[0]))
q("U02-B-030", "Triangle inequality", "Equality case |z1 + z2| = |z1| + |z2|", "Medium", "Multi-step computation MCQ",
  r"If $z_1 = 1 + i\sqrt{3}$, $|z_2| = 3$ and $|z_1 + z_2| = 5$, then $z_2$ equals",
  r"$\frac{3}{2} + \frac{3\sqrt{3}}{2}i$",
  [(r"$-\frac{3}{2} - \frac{3\sqrt{3}}{2}i$", r"Takes $z_2 = -\frac{3}{2}z_1$, opposite to $z_1$ (that gives $|z_1 + z_2| = 1$)."),
   (r"$\frac{3\sqrt{3}}{2} + \frac{3}{2}i$", r"Uses $3\left(\cos\frac{\pi}{3} + i\sin\frac{\pi}{3}\right)$ with $\cos$ and $\sin$ swapped."),
   (r"$3 + 3\sqrt{3}i$", r"Takes $z_2 = 3z_1$, ignoring $|z_1| = 2$.")],
  r"$|z_1| = 2$, so $|z_1 + z_2| = 5 = |z_1| + |z_2|$. Equality in the triangle inequality forces $z_2 = kz_1$ with $k > 0$, and $|z_2| = 3$ gives $k = \frac{3}{2}$. Hence $z_2 = \frac{3}{2}(1 + i\sqrt{3})$.",
  r"Not recognising the equality case of $|z_1 + z_2| \le |z_1| + |z_2|$.",
  "U02-equality-triangle", r"Spot the equality case, then scale by the modulus ratio $\frac{3}{2}$.",
  check=_c30,
  values=[Rational(3, 2) + 3*sqrt(3)/2*I, -Rational(3, 2) - 3*sqrt(3)/2*I, 3*sqrt(3)/2 + Rational(3, 2)*I, 3 + 3*sqrt(3)*I],
  cognitive="Analysis")


def _c31():
    return 2*ext_on_circle(2*I, 1, lambda w: w - 3)[1]
q("U02-B-031", "Triangle inequality", "Greatest value of a scaled distance", "Medium", "Multi-step computation MCQ",
  r"If $|z - 2i| \le 1$, then the greatest value of $|2z - 6|$ is",
  r"$2\sqrt{13} + 2$",
  [(r"$2\sqrt{13} + 1$", r"Doubles the centre distance $\sqrt{13}$ but not the radius $1$."),
   (r"$\sqrt{13} + 1$", r"Finds the greatest $|z - 3|$ and forgets the factor $2$."),
   (r"$2\sqrt{13} - 2$", r"Gives the least value $2(\sqrt{13} - 1)$.")],
  r"$|2z - 6| = 2|z - 3|$. The disc has centre $2i$ and radius $1$, and $|2i - 3| = \sqrt{13}$, so the greatest $|z - 3|$ is $\sqrt{13} + 1$ (on the boundary). Hence the greatest value is $2\sqrt{13} + 2$.",
  r"Not applying the factor $2$ in $|2z - 6| = 2|z - 3|$ consistently.",
  "U02-extremal-scaled", r"Factor out a constant, then the distance from a point to a disc.",
  check=_c31, values=[2*sqrt(13) + 2, 2*sqrt(13) + 1, sqrt(13) + 1, 2*sqrt(13) - 2], cognitive="Application")


def _c32():
    p = [(2, 1), (-1, 5), (-5, 2), (-2, -2)]
    s = sum(p[i][0]*p[(i+1) % 4][1] - p[(i+1) % 4][0]*p[i][1] for i in range(4))
    return Abs(Rational(s, 2))
q("U02-B-032", "Argand plane", "Area of a quadrilateral from given points", "Medium", "Multi-step computation MCQ",
  r"The points $2 + i$, $-1 + 5i$, $-5 + 2i$ and $-2 - 2i$, taken in order, are the vertices of a quadrilateral in the Argand plane. Its area is",
  r"$25$",
  [(r"$50$", r"Forgets the factor $\frac{1}{2}$ in the shoelace formula."),
   (r"$\frac{25}{2}$", r"Finds the area of only one of the two triangles cut off by a diagonal."),
   (r"$20$", r"Gives the perimeter $4 \cdot 5$.")],
  r"Consecutive differences are $-3 + 4i$, $-4 - 3i$, $3 - 4i$ and $4 + 3i$, each of modulus $5$, and $-4 - 3i = i(-3 + 4i)$ shows consecutive sides are perpendicular. So it is a square of side $5$ and area $25$.",
  r"Confusing area with perimeter or halving twice.",
  "U02-area-quadrilateral", r"Several side computations plus recognising perpendicularity.",
  check=_c32, values=[25, 50, Rational(25, 2), 20], cognitive="Analysis",
  numerical=dict(question=r"The points $2 + i$, $-1 + 5i$, $-5 + 2i$ and $-2 - 2i$, taken in order, are the vertices of a quadrilateral in the Argand plane. Its area is", answer=25))


def _c33():
    P = [1 + 2*I, 4 + 6*I, 8 + 3*I]
    s = sorted([simplify(Abs(P[i] - P[(i+1) % 3])**2) for i in range(3)])
    d = s[0] + s[1] - s[2]
    kind = 1 if d == 0 else (0 if d > 0 else 2)   # 0 acute, 1 right, 2 obtuse
    isos = bool(s[0] == s[1] or s[1] == s[2])
    equi = bool(s[0] == s[2])
    return (kind, isos, equi)
q("U02-B-033", "Argand plane", "Shape of a triangle from given points", "Medium", "Multi-step computation MCQ",
  r"The triangle with vertices at the points $1 + 2i$, $4 + 6i$ and $8 + 3i$ in the Argand plane is",
  r"right-angled and isosceles",
  [(r"equilateral", r"Sees two sides of length $5$ and assumes the third is also $5$."),
   (r"obtuse-angled and isosceles", r"Compares $(\sqrt{50})^2 = 50$ with $5 + 5$ instead of $5^2 + 5^2$, so judges the largest angle obtuse."),
   (r"acute-angled and isosceles, not equilateral", r"Takes $|7 + i|^2$ as $49 - 1 = 48$ (using $i^2 = -1$ inside the modulus), and $48 < 5^2 + 5^2$.")],
  r"The sides are $|3 + 4i| = 5$, $|4 - 3i| = 5$ and $|7 + i| = \sqrt{50}$. Two sides are equal and $5^2 + 5^2 = 50$, so the triangle is right-angled and isosceles.",
  r"Stopping after finding two equal sides.",
  "U02-triangle-shape", r"Three moduli and a comparison of $c^2$ with $a^2 + b^2$.",
  check=_c33, values=[(1, True, False), (0, True, True), (2, True, False), (0, True, False)],
  cognitive="Analysis")


def _c34():
    sols = solve([msq(Z - 1) - 4, msq(Z - 4*I) - 9], [x, y], dict=True)
    return len({(simplify(s[x]), simplify(s[y])) for s in sols})
q("U02-B-034", "Loci in the Argand plane", "Number of common points of two circles", "Medium", "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying both $|z - 1| = 2$ and $|z - 4i| = 3$ is",
  r"$2$",
  [(r"$1$", r"Takes the distance between the centres as $1 + 4 = 5 = 2 + 3$ and concludes the circles touch."),
   (r"$0$", r"Takes the distance between the centres as $1^2 + 4^2 = 17 > 2 + 3$ and concludes the circles are apart."),
   (r"$4$", r"Thinks two circles can meet in as many as $4$ points, as two general conics can.")],
  r"Centres $1$ and $4i$ are $|1 - 4i| = \sqrt{17}$ apart. Since $|3 - 2| = 1 < \sqrt{17} < 5 = 2 + 3$, the circles cut in exactly two points.",
  r"Adding coordinates, or forgetting the square root, when finding the distance between centres.",
  "U02-two-circles-count", r"Distance between centres compared with $r_1 + r_2$ and $|r_1 - r_2|$.",
  check=_c34, values=[2, 1, 0, 4], cognitive="Application")

q("U02-B-035", "Loci in the Argand plane", "Degenerate locus |z - a| + |z - b| = |a - b|", "Medium", "Conceptual/application MCQ",
  r"The set of points $z$ in the Argand plane satisfying $|z - 3| + |z + 3| = 6$ is",
  r"the line segment joining $-3$ and $3$",
  [(r"an ellipse with foci $-3$ and $3$", r"Applies the ellipse picture without checking that the sum $6$ equals the distance between the fixed points."),
   (r"the whole real axis", r"Includes points beyond the endpoints, where the sum exceeds $6$."),
   (r"the imaginary axis", r"Confuses the condition with $|z - 3| = |z + 3|$.")],
  r"By the triangle inequality, $|z - 3| + |z + 3| \ge |(z + 3) - (z - 3)| = 6$, with equality exactly when $z$ lies between $-3$ and $3$ on the segment joining them. So the locus is that segment.",
  r"Treating every condition $|z - a| + |z - b| = k$ as an ellipse, even when $k = |a - b|$.",
  "U02-locus-degenerate", r"Needs the equality case of the triangle inequality, a known trap.",
  cognitive="Analysis")


def _c36():
    s = Symbol('s')
    w = solve(s**2 + s + 1, s)[0]
    return sum(1 for n in range(1, 21) if simplify(expand((1 + w)**n + (1 + w**2)**n)) == 2)
q("U02-B-036", "Cube roots of unity", "Counting exponents in a power sum of omega", "Medium", "Multi-step computation MCQ",
  r"Let $\omega$ be a non-real root of $x^2 + x + 1 = 0$. The number of integers $n$ with $1 \le n \le 20$ for which $(1 + \omega)^n + (1 + \omega^2)^n = 2$ is",
  r"$3$",
  [(r"$6$", r"Drops the minus signs, writing $1 + \omega = \omega^2$ and $1 + \omega^2 = \omega$, so only needs $n$ to be a multiple of $3$: $n = 3, 6, \ldots, 18$."),
   (r"$10$", r"Handles the sign $(-1)^n$ but takes $\omega^n + \omega^{2n} = 2$ for every $n$, so only needs $n$ even."),
   (r"$7$", r"Swaps the two cases, taking $\omega^n + \omega^{2n} = 2$ when $3 \nmid n$, so counts the even $n$ that are not multiples of $3$.")],
  r"Since $1 + \omega + \omega^2 = 0$, $1 + \omega = -\omega^2$ and $1 + \omega^2 = -\omega$. So the sum is $(-1)^n(\omega^n + \omega^{2n})$, and $\omega^n + \omega^{2n}$ is $2$ when $3 \mid n$ and $-1$ otherwise. The sum equals $2$ exactly when $n$ is even and a multiple of $3$, i.e. $n = 6, 12, 18$, giving $3$ values.",
  r"Losing the minus signs in $1 + \omega = -\omega^2$, or mixing up when $\omega^n + \omega^{2n}$ equals $2$ and when it equals $-1$.",
  "U02-omega-power-count", r"Two substitutions, a sign factor $(-1)^n$ and the two-case value of $\omega^n + \omega^{2n}$, combined in a count.",
  check=_c36, values=[3, 6, 10, 7], cognitive="Analysis",
  numerical=dict(question=r"Let $\omega$ be a non-real root of $x^2 + x + 1 = 0$. The number of integers $n$ with $1 \le n \le 20$ for which $(1 + \omega)^n + (1 + \omega^2)^n = 2$ is", answer=3))


def _c37():
    s = Symbol('s')
    w = solve(s**2 + s + 1, s)[0]
    return simplify(expand((2 + 5*w + 2*w**2)**6))
_w37 = solve(Symbol('s')**2 + Symbol('s') + 1, Symbol('s'))[0]
q("U02-B-037", "Cube roots of unity", "Reducing an expression to a power of omega", "Medium", "Multi-step computation MCQ",
  r"If $\omega$ is a root of $x^2 + x + 1 = 0$, then $(2 + 5\omega + 2\omega^2)^6$ equals",
  r"$729$",
  [(r"$729\omega$", r"Raises only the $3$ to the sixth power, leaving $\omega$ unpowered: $3^6\omega$."),
   (r"$729\omega^2$", r"Reduces $\omega^6$ by taking the exponent modulo $4$ (as for powers of $i$), giving $\omega^2$."),
   (r"$1$", r"Takes the bracket as $\omega$, dropping the factor $3$, so the answer is $\omega^6 = 1$.")],
  r"$2 + 5\omega + 2\omega^2 = 2(1 + \omega + \omega^2) + 3\omega = 3\omega$. Hence $(3\omega)^6 = 729\,\omega^6 = 729$, since $\omega^3 = 1$.",
  r"Incorrect reduction of powers of $\omega$ (the cycle length is $3$).",
  "U02-omega-simplify", r"Regrouping into $1 + \omega + \omega^2$, then powering.",
  check=_c37, values=[729, 729*_w37, 729*_w37**2, 1], cognitive="Application",
  numerical=dict(question=r"If $\omega$ is a root of $x^2 + x + 1 = 0$, then the value of $(2 + 5\omega + 2\omega^2)^6$ is", answer=729))


def _c38():
    a = Symbol('a', real=True)
    w = expand((a + 3*I)*(2 + I)/5)
    sols = solve(Eq(re(w), im(w)), a)
    good = [s for s in sols if re(w).subs(a, s) > 0]
    assert len(good) == 1
    assert simplify(arg(w.subs(a, good[0])) - pi/4) == 0
    return good[0]
q("U02-B-038", "Modulus and argument", "Parameter from a given argument", "Medium", "Inverse/parameter MCQ",
  r"If $a$ is real and the principal argument of $\frac{a + 3i}{2 - i}$ is $\frac{\pi}{4}$, then $a$ equals",
  r"$9$",
  [(r"$1$", r"Multiplies by $2 - i$ instead of its conjugate: $(a + 3i)(2 - i) = (2a + 3) + (6 - a)i$, then $2a + 3 = 6 - a$."),
   (r"$3$", r"Sets the argument of the numerator $a + 3i$ alone equal to $\frac{\pi}{4}$."),
   (r"$-1$", r"Uses $2a - 3 = -(a + 6)$, i.e. $|\text{Re}| = |\text{Im}|$ with opposite signs, which gives argument $\frac{3\pi}{4}$.")],
  r"$\frac{a + 3i}{2 - i} = \frac{(a + 3i)(2 + i)}{5} = \frac{(2a - 3) + (a + 6)i}{5}$. Argument $\frac{\pi}{4}$ needs real part $=$ imaginary part $> 0$: $2a - 3 = a + 6$ gives $a = 9$, and then both parts equal $3 > 0$.",
  r"Ignoring the condition $\operatorname{Re} = \operatorname{Im} > 0$ attached to an argument of $\frac{\pi}{4}$.",
  "U02-arg-parameter", r"Rationalise, equate parts, check the sign.",
  check=_c38, values=[9, 1, 3, -1], cognitive="Application",
  numerical=dict(question=r"If $a$ is real and the principal argument of $\frac{a + 3i}{2 - i}$ is $\frac{\pi}{4}$, then the value of $a$ is", answer=9))


def _c39():
    sols = solve([msq(Z) - 16, msq(3 - Z) - 13], [x, y], dict=True)
    vals = {simplify(re(expand(3*conjugate(Z.subs(s))))) for s in sols}
    assert len(vals) == 1
    return vals.pop()
q("U02-B-039", "Modulus and argument", "Expanding |z1 - z2|^2", "Medium", "Multi-step computation MCQ",
  r"If $|z_1| = 3$, $|z_2| = 4$ and $|z_1 - z_2| = \sqrt{13}$, then $\operatorname{Re}(z_1\overline{z_2})$ equals",
  r"$6$",
  [(r"$12$", r"Finds $2\operatorname{Re}(z_1\overline{z_2}) = 12$ and does not halve."),
   (r"$-6$", r"Uses $|z_1 + z_2|^2 = |z_1|^2 + |z_2|^2 + 2\operatorname{Re}(z_1\overline{z_2})$: $13 = 25 + 2\operatorname{Re}(z_1\overline{z_2})$."),
   (r"$3$", r"Divides $12$ by $4$ instead of $2$.")],
  r"$|z_1 - z_2|^2 = |z_1|^2 + |z_2|^2 - 2\operatorname{Re}(z_1\overline{z_2})$, so $13 = 9 + 16 - 2\operatorname{Re}(z_1\overline{z_2})$, giving $\operatorname{Re}(z_1\overline{z_2}) = 6$.",
  r"Wrong sign of the cross term $2\operatorname{Re}(z_1\overline{z_2})$ in $|z_1 - z_2|^2$.",
  "U02-expand-modulus-square", r"One identity and a linear equation.",
  check=_c39, values=[6, 12, -6, 3], cognitive="Application",
  numerical=dict(question=r"If $|z_1| = 3$, $|z_2| = 4$ and $|z_1 - z_2| = \sqrt{13}$, then $\operatorname{Re}(z_1\overline{z_2})$ is", answer=6))


def _c40():
    ys = solve(msq(Z - 2) - msq(Z - 4*I), y)[0]
    f = x**2 + ys**2
    c = solve(diff(f, x), x)
    return simplify(sqrt(f.subs(x, c[0])))
q("U02-B-040", "Loci in the Argand plane", "Least modulus on a perpendicular bisector", "Medium", "Multi-step computation MCQ",
  r"If $z$ satisfies $|z - 2| = |z - 4i|$, then the least value of $|z|$ is",
  r"$\frac{3}{\sqrt{5}}$",
  [(r"$\frac{3}{5}$", r"Divides by $1^2 + 2^2 = 5$ instead of $\sqrt{5}$ in the distance formula."),
   (r"$\sqrt{5}$", r"Gives the distance of the midpoint $1 + 2i$ from the origin."),
   (r"$\frac{3}{2}$", r"Gives the $y$-intercept of the line $x - 2y + 3 = 0$.")],
  r"With $z = x + iy$: $(x - 2)^2 + y^2 = x^2 + (y - 4)^2$ gives $x - 2y + 3 = 0$. The least $|z|$ is the distance from the origin to this line, $\frac{|3|}{\sqrt{1 + 4}} = \frac{3}{\sqrt{5}}$.",
  r"Using the midpoint or an intercept instead of the perpendicular distance.",
  "U02-min-modulus-line", r"Find the bisector, then a perpendicular distance.",
  check=_c40, values=[3/sqrt(5), Rational(3, 5), sqrt(5), Rational(3, 2)], cognitive="Application")


def _c41():
    cnt = 0
    for a in range(-4, 5):
        for b in range(-4, 5):
            if N(Abs(a + I*b)) < 3 and a > b:
                cnt += 1
    return cnt
q("U02-B-041", "Loci in the Argand plane", "Lattice points in a region", "Medium", "Multi-step computation MCQ",
  r"The number of complex numbers $z$ with integer real and imaginary parts satisfying $|z| < 3$ and $\operatorname{Re}(z) > \operatorname{Im}(z)$ is",
  r"$10$",
  [(r"$15$", r"Includes the $5$ points on the line $\operatorname{Re}(z) = \operatorname{Im}(z)$."),
   (r"$12$", r"Uses $|z| \le 3$, adding the two points $3$ and $-3i$ of modulus exactly $3$ that satisfy $\operatorname{Re}(z) > \operatorname{Im}(z)$."),
   (r"$20$", r"Counts all $20$ points off the line $y = x$, forgetting to halve.")],
  r"Integer points with $x^2 + y^2 < 9$ have $|x|, |y| \le 2$, giving $25$ points. Five of them lie on $y = x$. By symmetry in $y = x$, the remaining $20$ split equally, so $10$ satisfy $x > y$.",
  r"Including boundary points in a strict inequality.",
  "U02-lattice-region", r"Counting with two conditions and a symmetry argument.",
  check=_c41, values=[10, 15, 12, 20], cognitive="Analysis",
  numerical=dict(question=r"The number of complex numbers $z$ with integer real and imaginary parts satisfying $|z| < 3$ and $\operatorname{Re}(z) > \operatorname{Im}(z)$ is", answer=10))


def _c42():
    z1 = 2*(cos(pi/12) + I*sin(pi/12))
    z2 = 3*(cos(5*pi/12) + I*sin(5*pi/12))
    return nsimplify(simplify(expand_complex(z1/z2)))
q("U02-B-042", "Modulus and argument", "Quotient in polar form", "Medium", "Multi-step computation MCQ",
  r"If $z_1 = 2\left(\cos\frac{\pi}{12} + i\sin\frac{\pi}{12}\right)$ and $z_2 = 3\left(\cos\frac{5\pi}{12} + i\sin\frac{5\pi}{12}\right)$, then $\frac{z_1}{z_2}$ equals",
  r"$\frac{1}{3} - \frac{\sqrt{3}}{3}i$",
  [(r"$\frac{1}{3} + \frac{\sqrt{3}}{3}i$", r"Subtracts the arguments in the wrong order, using $\frac{5\pi}{12} - \frac{\pi}{12} = \frac{\pi}{3}$ with modulus $\frac{2}{3}$."),
   (r"$\frac{3}{4} - \frac{3\sqrt{3}}{4}i$", r"Uses the modulus ratio $\frac{3}{2}$ instead of $\frac{2}{3}$."),
   (r"$\frac{\sqrt{3}}{3} - \frac{1}{3}i$", r"Swaps $\cos\frac{\pi}{3}$ and $\sin\frac{\pi}{3}$.")],
  r"$\left|\frac{z_1}{z_2}\right| = \frac{2}{3}$ and $\arg\frac{z_1}{z_2} = \frac{\pi}{12} - \frac{5\pi}{12} = -\frac{\pi}{3}$. So $\frac{z_1}{z_2} = \frac{2}{3}\left(\frac{1}{2} - \frac{\sqrt{3}}{2}i\right) = \frac{1}{3} - \frac{\sqrt{3}}{3}i$.",
  r"Order of subtraction of arguments in $\frac{z_1}{z_2}$.",
  "U02-polar-quotient", r"Divide moduli, subtract arguments, convert back.",
  check=_c42,
  values=[Rational(1, 3) - sqrt(3)/3*I, Rational(1, 3) + sqrt(3)/3*I, Rational(3, 4) - 3*sqrt(3)/4*I, sqrt(3)/3 - Rational(1, 3)*I],
  cognitive="Application")

# ============================================================== DIFFICULT


def _c43():
    R, U = symbols('R U', real=True)
    w = Z**2 - 6
    F = expand(msq(w) - msq(Z))           # |z^2 - 6|^2 = |z|^2  <=>  |z - 6/z| = 1
    F = expand(F.subs({x**2: (R + U)/2, y**2: (R - U)/2}))
    Fx = expand(F.subs({x**4: ((R + U)/2)**2, y**4: ((R - U)/2)**2}))
    u = solve(Fx, U)[0]                   # u = x^2 - y^2 must lie in [-R, R]
    sol = Intersection(solveset(u - R <= 0, R, S.Reals), solveset(u + R >= 0, R, S.Reals), Interval.open(0, oo))
    return sqrt(sol.sup)
q("U02-B-043", "Triangle inequality", "Greatest modulus under |z - k/z| = c", "Difficult", "Multi-step computation MCQ",
  r"If $z$ is a nonzero complex number with $\left|z - \frac{6}{z}\right| = 1$, then the greatest value of $|z|$ is",
  r"$3$",
  [(r"$2$", r"Uses $\frac{6}{r} - r \le 1$, i.e. $r^2 + r - 6 \ge 0$, whose boundary $r = 2$ is the least value."),
   (r"$\sqrt{6}$", r"Sets $|z|^2 = 6$ so that the two terms $|z|$ and $\frac{6}{|z|}$ balance."),
   (r"$7$", r"Adds $1$ and $6$, as if $|z| \le 1 + 6$.")],
  r"Let $r = |z|$. Then $r - \frac{6}{r} \le \left|z - \frac{6}{z}\right| = 1$, so $r^2 - r - 6 \le 0$, i.e. $r \le 3$. Equality holds at $z = 3$: $\left|3 - 2\right| = 1$. Hence the greatest value is $3$.",
  r"Choosing the wrong sign in the reverse triangle inequality $\left|z - \frac{6}{z}\right| \ge \left||z| - \frac{6}{|z|}\right|$.",
  "U02-extremal-z-minus-k-over-z", r"Reverse triangle inequality, a quadratic in $r = |z|$, and an attainment check.",
  check=_c43, values=[3, 2, sqrt(6), 7], cognitive="Analysis",
  numerical=dict(question=r"If $z$ is a nonzero complex number with $\left|z - \frac{6}{z}\right| = 1$, then the greatest value of $|z|$ is", answer=3))


_th = Symbol('theta', real=True)
_cands44 = [(sgn*2*cos(_th/2), a) for sgn in (1, -1) for a in (_th/2, _th/2 - pi, _th/2 + pi, pi - _th/2)]


def _c44():
    samples = [7*pi/6, 3*pi/2, 5*pi/3, 11*pi/10, 19*pi/10]
    hits = []
    for m, a in _cands44:
        ok = True
        for s0 in samples:
            zz = 1 + cos(s0) + I*sin(s0)
            if abs(N(m.subs(_th, s0) - Abs(zz))) > 1e-9 or abs(N(a.subs(_th, s0) - arg(zz))) > 1e-9:
                ok = False
                break
        if ok:
            hits.append((m, a))
    assert len(hits) == 1
    return hits[0]
q("U02-B-044", "Modulus and argument", "Polar form via half-angles with sign trap", "Difficult", "Multi-step computation MCQ",
  r"If $\pi < \theta < 2\pi$ and $z = 1 + \cos\theta + i\sin\theta$, then $|z|$ and the principal argument (in $(-\pi, \pi]$) of $z$ are",
  r"$|z| = -2\cos\frac{\theta}{2}$, $\arg(z) = \frac{\theta}{2} - \pi$",
  [(r"$|z| = 2\cos\frac{\theta}{2}$, $\arg(z) = \frac{\theta}{2}$", r"Uses the half-angle form $2\cos\frac{\theta}{2}\left(\cos\frac{\theta}{2} + i\sin\frac{\theta}{2}\right)$ directly; this 'modulus' is negative here."),
   (r"$|z| = -2\cos\frac{\theta}{2}$, $\arg(z) = \frac{\theta}{2}$", r"Fixes the sign of the modulus but does not shift the argument by $\pi$."),
   (r"$|z| = -2\cos\frac{\theta}{2}$, $\arg(z) = \pi - \frac{\theta}{2}$", r"Shifts by $\pi$ with the wrong sign, which gives a first-quadrant angle, while $z$ is in the fourth quadrant.")],
  r"$z = 2\cos^2\frac{\theta}{2} + 2i\sin\frac{\theta}{2}\cos\frac{\theta}{2} = 2\cos\frac{\theta}{2}\left(\cos\frac{\theta}{2} + i\sin\frac{\theta}{2}\right)$. For $\frac{\pi}{2} < \frac{\theta}{2} < \pi$, $\cos\frac{\theta}{2} < 0$, so write $z = \left(-2\cos\frac{\theta}{2}\right)\left(\cos\left(\frac{\theta}{2} - \pi\right) + i\sin\left(\frac{\theta}{2} - \pi\right)\right)$. Thus $|z| = -2\cos\frac{\theta}{2}$ and $\arg z = \frac{\theta}{2} - \pi \in \left(-\frac{\pi}{2}, 0\right)$.",
  r"Accepting a negative 'modulus' $2\cos\frac{\theta}{2}$ from the half-angle factorisation.",
  "U02-polar-half-angle", r"Half-angle identities, sign of $\cos\frac{\theta}{2}$ on an interval, and the principal range.",
  check=_c44, values=[_cands44[5], _cands44[0], _cands44[4], _cands44[7]], cognitive="Analysis")


def _c45():
    sols = solve([re(expand(Z**2)), msq(Z - 2) - 2], [x, y], dict=True)
    return len({(simplify(s[x]), simplify(s[y])) for s in sols})
q("U02-B-045", "Loci in the Argand plane", "Counting common points of a line pair and a circle", "Difficult", "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying both $\operatorname{Re}(z^2) = 0$ and $|z - 2| = \sqrt{2}$ is",
  r"$2$",
  [(r"$4$", r"Assumes each of the two lines $y = x$ and $y = -x$ cuts the circle twice."),
   (r"$1$", r"Uses only the line $y = x$, forgetting $y = -x$."),
   (r"$3$", r"Finds the tangency on one line but thinks the other line cuts the circle twice.")],
  r"$\operatorname{Re}(z^2) = x^2 - y^2 = 0$ is the pair of lines $y = \pm x$. The circle has centre $(2, 0)$ and radius $\sqrt{2}$; the distance from the centre to each line is $\frac{2}{\sqrt{2}} = \sqrt{2}$, so each line touches the circle once, at $1 + i$ and $1 - i$. Total $2$.",
  r"Assuming a line meets a circle in two points without comparing the distance from the centre with the radius.",
  "U02-loci-intersection-count", r"Identify a line pair, compute two distances, detect tangency.",
  check=_c45, values=[2, 4, 1, 3], cognitive="Analysis",
  numerical=dict(question=r"The number of complex numbers $z$ satisfying both $\operatorname{Re}(z^2) = 0$ and $|z - 2| = \sqrt{2}$ is", answer=2))


def _c46():
    pts = set()
    for th in (pi/3, -pi/3, pi/2):
        sols = solve([msq(Z - 1) - 1, x*sin(th) - y*cos(th)], [x, y], dict=True)
        for s in sols:
            zz = simplify(Z.subs(s))
            if zz != 0 and simplify(arg(zz) - th) == 0:
                pts.add(zz)
    return len(pts)
q("U02-B-046", "Loci in the Argand plane", "Rays meeting a circle through the origin", "Difficult", "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying $|z - 1| = 1$ and $\arg(z) \in \left\{\frac{\pi}{3}, -\frac{\pi}{3}, \frac{\pi}{2}\right\}$ (principal argument) is",
  r"$2$",
  [(r"$3$", r"Accepts $z = 0$ as a solution, although $\arg 0$ is undefined: $2 + 1$."),
   (r"$5$", r"Counts $z = 0$ once for each of the three rays: $2 + 3$."),
   (r"$6$", r"Assumes each of the three rays cuts the circle in two points.")],
  r"The circle passes through the origin. On the ray $\arg z = \frac{\pi}{3}$, $z = t\left(\frac{1}{2} + \frac{\sqrt{3}}{2}i\right)$ with $t > 0$; substituting gives $t^2 - t = 0$, so $t = 1$ only. Similarly $\arg z = -\frac{\pi}{3}$ gives one point. On $\arg z = \frac{\pi}{2}$, $z = ti$ gives $1 + t^2 = 1$, so $t = 0$, which is excluded. Total $2$.",
  r"Forgetting that $z = 0$ has no argument, so it never lies on a ray $\arg z = \theta$.",
  "U02-arg-ray-circle-count", r"Three cases, each with an excluded root $t = 0$ at the origin.",
  check=_c46, values=[2, 3, 5, 6], cognitive="Analysis",
  numerical=dict(question=r"The number of complex numbers $z$ satisfying $|z - 1| = 1$ and $\arg(z) \in \left\{\frac{\pi}{3}, -\frac{\pi}{3}, \frac{\pi}{2}\right\}$, where $\arg$ denotes the principal argument, is", answer=2))


def _c47():
    import random
    rnd = random.Random(11)
    s1 = s2 = True
    for _ in range(40):
        z2 = rnd.choice([-1, 0, 1, 2, -3]) + I*rnd.choice([-2, -1, 0, 1, 3])
        if z2 == 0:
            continue
        k = Rational(rnd.randint(1, 9), rnd.randint(1, 5))
        za = k*z2           # |za + z2| = |za| + |z2|
        zb = -k*z2          # |zb - z2| = |zb| + |z2|
        assert simplify(Abs(za + z2) - Abs(za) - Abs(z2)) == 0
        assert simplify(Abs(zb - z2) - Abs(zb) - Abs(z2)) == 0
        if simplify(arg(za) - arg(z2)) != 0: s1 = False
        if simplify(Abs(arg(zb) - arg(z2)) - pi) != 0: s2 = False
    return (s1, s2)
q("U02-B-047", "Triangle inequality", "Equality cases and principal arguments", "Difficult", "Statement-based MCQ",
  r"Let $z_1, z_2$ be nonzero complex numbers, with arguments taken as principal values in $(-\pi, \pi]$. Statement I: If $|z_1 + z_2| = |z_1| + |z_2|$, then $\arg(z_1) = \arg(z_2)$. Statement II: If $|z_1 - z_2| = |z_1| + |z_2|$, then $|\arg(z_1) - \arg(z_2)| = \pi$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Thinks the principal-range cut can make $|\arg z_1 - \arg z_2|$ differ from $\pi$ for opposite directions."),
   (ST_FT, r"Thinks equal directions can still give principal arguments differing by $2\pi$."),
   (ST_FF, r"Believes the principal-range restriction breaks both equality-case conclusions.")],
  r"In Statement I, equality means $z_1 = kz_2$ with $k > 0$, so both have the same direction and hence the same principal argument. In Statement II, $|z_1 + (-z_2)| = |z_1| + |-z_2|$ means $z_1 = -kz_2$ with $k > 0$, so $z_1$ and $z_2$ point in opposite directions. If $\arg z_2 = \theta \in (-\pi, \pi]$, then $\arg z_1 = \theta - \pi$ (for $\theta > 0$) or $\theta + \pi$ (for $\theta \le 0$); either way $|\arg z_1 - \arg z_2| = \pi$. Both statements are true.",
  r"Thinking the principal range $(-\pi, \pi]$ breaks the equality-case conclusions.",
  "U02-equality-case-statements", r"Equality cases of the triangle inequality combined with principal-range casework.",
  check=_c47, values=[TT, TF, FT, FF], cognitive="Analysis")


def _c48():
    sols = solve([msq(Z - 2 - 2*I) - 2, x*(x - 2) + y*(y - 2)], [x, y], dict=True)
    args = [arg(simplify(Z.subs(s))) for s in sols]
    return max(args, key=lambda v: N(v))
q("U02-B-048", "Modulus and argument", "Greatest argument on a circle", "Difficult", "Multi-step computation MCQ",
  r"If $|z - 2 - 2i| = \sqrt{2}$, then the greatest value of the principal argument (in $(-\pi, \pi]$) of $z$ is",
  r"$\frac{5\pi}{12}$",
  [(r"$\frac{\pi}{12}$", r"Gives the least value $\frac{\pi}{4} - \frac{\pi}{6}$."),
   (r"$\frac{7\pi}{12}$", r"Takes the half-angle as $\cos^{-1}\frac{1}{2} = \frac{\pi}{3}$ instead of $\sin^{-1}\frac{1}{2} = \frac{\pi}{6}$: $\frac{\pi}{4} + \frac{\pi}{3}$."),
   (r"$\frac{\pi}{3}$", r"Gives the width $\frac{5\pi}{12} - \frac{\pi}{12}$ of the range of arguments.")],
  r"The centre $2 + 2i$ is at distance $2\sqrt{2}$ from the origin, in direction $\frac{\pi}{4}$. A tangent from the origin makes angle $\alpha$ with this direction where $\sin\alpha = \frac{\sqrt{2}}{2\sqrt{2}} = \frac{1}{2}$, so $\alpha = \frac{\pi}{6}$. The argument of $z$ ranges over $\left[\frac{\pi}{4} - \frac{\pi}{6}, \frac{\pi}{4} + \frac{\pi}{6}\right]$, so the greatest value is $\frac{5\pi}{12}$.",
  r"Using $\cos$ instead of $\sin$ for the tangent half-angle $\alpha$.",
  "U02-extremal-arg-circle", r"Geometry of tangents from the origin combined with the argument.",
  check=_c48, values=[5*pi/12, pi/12, 7*pi/12, pi/3], cognitive="Analysis")


def _c49():
    a = Symbol('a', real=True)
    c2, r2 = 3 + 4*I, 7
    z1 = cos(a) + I*sin(a)
    d2 = simplify(expand(msq_any(z1 - c2)))
    cr = solve(diff(d2, a), a)
    pts = list(cr) + [s + pi for s in cr]
    ds = [sqrt(simplify(d2.subs(a, s))) for s in pts]
    dmin, dmax = min(ds, key=lambda v: N(v)), max(ds, key=lambda v: N(v))
    if r2 >= dmax:
        return simplify(r2 - dmax)
    if r2 <= dmin:
        return simplify(dmin - r2)
    return 0
q("U02-B-049", "Triangle inequality", "Least distance between points on two circles", "Difficult", "Multi-step computation MCQ",
  r"If $|z_1| = 1$ and $|z_2 - 3 - 4i| = 7$, then the least value of $|z_1 - z_2|$ is",
  r"$1$",
  [(r"$0$", r"Assumes the circles intersect because $5 < 1 + 7$."),
   (r"$3$", r"Takes $|5 - 1 - 7| = 3$ without noticing that one circle lies inside the other."),
   (r"$13$", r"Gives the greatest value $5 + 1 + 7$.")],
  r"The centres $0$ and $3 + 4i$ are $5$ apart. Since $5 + 1 = 6 < 7$, the circle $|z_1| = 1$ lies entirely inside the circle of radius $7$. The least gap is along the line of centres: $7 - (5 + 1) = 1$.",
  r"Not checking whether one circle lies inside the other before using $d - r_1 - r_2$.",
  "U02-extremal-two-circles", r"Relative position of two circles must be diagnosed before the formula.",
  check=_c49, values=[1, 0, 3, 13], cognitive="Analysis")


def _c50():
    w = conjugate(Z)/Z + Z/conjugate(Z)
    num, den = fraction(together(expand(w*conjugate(w)) - 1))
    sols = solve([x**2 + y**2 - 1, expand(num)], [x, y], dict=True)
    return len({(simplify(s[x]), simplify(s[y])) for s in sols})
q("U02-B-050", "Loci in the Argand plane", "Counting points on the unit circle", "Difficult", "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying $|z| = 1$ and $\left|\frac{\overline{z}}{z} + \frac{z}{\overline{z}}\right| = 1$ is",
  r"$8$",
  [(r"$4$", r"Solves only $x^2 - y^2 = \frac{1}{2}$, ignoring the case $x^2 - y^2 = -\frac{1}{2}$."),
   (r"$2$", r"Solves only $x^2 - y^2 = \frac{1}{2}$ and also ignores the two signs of $y$, keeping $x = \pm\frac{\sqrt{3}}{2}$."),
   (r"$16$", r"Allows $x^2$ and $y^2$ to be $\frac{1}{4}$ or $\frac{3}{4}$ independently, ignoring $x^2 + y^2 = 1$: $4 \times 4$ points.")],
  r"With $z = x + iy$, $|z| = 1$ gives $\overline{z} = \frac{1}{z}$, so $\frac{\overline{z}}{z} + \frac{z}{\overline{z}} = z^2 + \overline{z}^2 = 2(x^2 - y^2)$. The condition is $|x^2 - y^2| = \frac{1}{2}$ with $x^2 + y^2 = 1$, so $x^2 = \frac{3}{4}$ or $x^2 = \frac{1}{4}$. Each gives $4$ points $(\pm x, \pm y)$, so $8$ in all.",
  r"Dropping the negative case of $|x^2 - y^2| = \frac{1}{2}$.",
  "U02-unit-circle-count", r"Conjugate on the unit circle, absolute value casework, and counting sign combinations.",
  check=_c50, values=[8, 4, 2, 16], cognitive="Analysis",
  numerical=dict(question=r"The number of complex numbers $z$ satisfying $|z| = 1$ and $\left|\frac{\overline{z}}{z} + \frac{z}{\overline{z}}\right| = 1$ is", answer=8))


def _c51():
    assert Abs(3 - 4*I) == 5      # sum of distances equals distance between 3 and 4i: segment
    s = Symbol('s', real=True)
    zz = 3*(1 - s) + 4*I*s
    f = expand(msq_any(zz))
    cands = [Integer(0), Integer(1)] + [c for c in solve(diff(f, s), s) if 0 <= c <= 1]
    return min([sqrt(f.subs(s, c)) for c in cands], key=lambda v: N(v))
q("U02-B-051", "Loci in the Argand plane", "Least modulus on a degenerate locus", "Difficult", "Multi-step computation MCQ",
  r"If $z$ satisfies $|z - 3| + |z - 4i| = 5$, then the least value of $|z|$ is",
  r"$\frac{12}{5}$",
  [(r"$3$", r"Checks only the endpoints $3$ and $4i$ of the segment and takes the smaller modulus."),
   (r"$\frac{5}{2}$", r"Uses the distance of the midpoint $\frac{3}{2} + 2i$ from the origin."),
   (r"$4$", r"Takes the greatest value, $|4i|$.")],
  r"Since $|3 - 4i| = 5$, equality in the triangle inequality shows $z$ lies on the segment joining $3$ and $4i$, i.e. on $4x + 3y = 12$ between the axes. The foot of the perpendicular from the origin lies on this segment, so the least $|z|$ is $\frac{12}{\sqrt{16 + 9}} = \frac{12}{5}$.",
  r"Treating the locus as an ellipse or checking only the endpoints.",
  "U02-segment-locus-extremal", r"Recognise a degenerate locus, then a perpendicular distance with a feasibility check.",
  check=_c51, values=[Rational(12, 5), 3, Rational(5, 2), 4], cognitive="Analysis")


def _c52():
    sols = solve([msq(Z) - 4, y - sqrt(3)*(x + 2)], [x, y], dict=True)
    good = []
    for s in sols:
        zz = simplify(Z.subs(s))
        if simplify(zz + 2) != 0 and simplify(arg(zz + 2) - pi/3) == 0:
            good.append(zz)
    assert len(good) == 1
    return arg(good[0])
q("U02-B-052", "Modulus and argument", "Argument condition combined with modulus", "Difficult", "Multi-step computation MCQ",
  r"If $|z| = 2$ and the principal argument of $z + 2$ is $\frac{\pi}{3}$, then the principal argument (in $(-\pi, \pi]$) of $z$ is",
  r"$\frac{2\pi}{3}$",
  [(r"$\frac{\pi}{3}$", r"Assumes $\arg z = \arg(z + 2)$."),
   (r"$-\frac{2\pi}{3}$", r"Takes the conjugate point $-1 - i\sqrt{3}$, for which $\arg(z + 2) = -\frac{\pi}{3}$."),
   (r"$\frac{5\pi}{6}$", r"Swaps the real and imaginary parts of $-1 + i\sqrt{3}$, reading the argument of $-\sqrt{3} + i$.")],
  r"Write $z + 2 = t\left(\frac{1}{2} + \frac{\sqrt{3}}{2}i\right)$ with $t > 0$, so $z = \left(\frac{t}{2} - 2\right) + \frac{\sqrt{3}t}{2}i$. Then $|z|^2 = t^2 - 2t + 4 = 4$ gives $t = 2$ ($t = 0$ is excluded). So $z = -1 + i\sqrt{3}$ and $\arg z = \frac{2\pi}{3}$.",
  r"Ignoring the excluded root $t = 0$ or misreading the quadrant of $z$.",
  "U02-arg-modulus-combined", r"Ray parametrisation, a quadratic in $t$ with an excluded root, then a principal argument.",
  check=_c52, values=[2*pi/3, pi/3, -2*pi/3, 5*pi/6], cognitive="Analysis")


def _c53():
    r = Symbol('r', positive=True)
    d = Abs(3 + 4*I) - Abs(0)
    s1 = solveset(Abs(r - 2) < d, r, S.Reals)
    s2 = solveset(d < r + 2, r, S.Reals)
    return Intersection(s1, s2, Interval.open(0, oo))
q("U02-B-053", "Loci in the Argand plane", "Parameter for two circles to cut", "Difficult", "Inverse/parameter MCQ",
  r"The set of all values of $r > 0$ for which the circles $|z| = 2$ and $|z - 3 - 4i| = r$ meet in exactly two points is",
  r"$(3, 7)$",
  [(r"$[3, 7]$", r"Includes $r = 3$ and $r = 7$, where the circles only touch."),
   (r"$(3, \infty)$", r"Uses only $5 < r + 2$ and drops the condition $|r - 2| < 5$."),
   (r"$(2, 7)$", r"Replaces the lower condition $r + 2 > 5$ by $r > 2$, the other radius.")],
  r"The centres are $5$ apart. Two common points require $|r - 2| < 5 < r + 2$. The right inequality gives $r > 3$ and the left gives $-3 < r < 7$. So $3 < r < 7$.",
  r"Including tangency or using only one of the two conditions $|r_1 - r_2| < d < r_1 + r_2$.",
  "U02-circle-circle-parameter", r"Two-sided condition $|r - 2| < 5 < r + 2$ with strict inequalities.",
  check=_c53, values=[Interval.open(3, 7), Interval(3, 7), Interval.open(3, oo), Interval.open(2, 7)],
  cognitive="Analysis")


def _c54():
    f1 = expand(msq(Z - 1)).subs(y**2, 1 - x**2)
    f2 = expand(msq(Z + 1)).subs(y**2, 1 - x**2)
    f = sqrt(f1) + sqrt(f2)
    cands = [Integer(-1), Integer(1)] + [c for c in solve(diff(f, x), x) if -1 <= c <= 1]
    return max([simplify(f.subs(x, c)) for c in cands], key=lambda v: N(v))
q("U02-B-054", "Triangle inequality", "Greatest sum of distances on the unit circle", "Difficult", "Multi-step computation MCQ",
  r"If $|z| = 1$, then the greatest value of $|z - 1| + |z + 1|$ is",
  r"$2\sqrt{2}$",
  [(r"$4$", r"Uses the triangle-inequality bound $(|z| + 1) + (|z| + 1) = 4$, which is never attained."),
   (r"$2$", r"Gives the least value, attained at $z = 1$ or $z = -1$."),
   (r"$\sqrt{2}$", r"Finds $|z - 1| = \sqrt{2}$ at $z = i$ but forgets to add $|z + 1|$.")],
  r"$|z - 1|^2 + |z + 1|^2 = 2|z|^2 + 2 = 4$. By the inequality $(a + b)^2 \le 2(a^2 + b^2)$, $(|z - 1| + |z + 1|)^2 \le 8$, so the sum is at most $2\sqrt{2}$, with equality when $|z - 1| = |z + 1|$, i.e. $z = \pm i$.",
  r"Accepting an upper bound from $|z \pm 1| \le |z| + 1$ that cannot be attained.",
  "U02-unit-circle-sum-distances", r"Needs the bound $(a + b)^2 \le 2(a^2 + b^2)$ and an attainment check; the naive bound $4$ is a trap.",
  check=_c54, values=[2*sqrt(2), 4, 2, sqrt(2)], cognitive="Analysis")


def _c55():
    # Statement I: examples meeting the hypothesis
    ex = [(Integer(-2), Integer(3)), (Integer(2), Integer(-3)), (2*I, -3*I), (-2*I, 3*I)]
    for a, b in ex:
        assert Abs(a) == 2 and Abs(b) == 3 and Abs(a + b) == 1
    s1 = all(simplify(Abs(arg(a) - arg(b)) - pi) == 0 for a, b in ex)
    sols = solve([msq(Z - 1) - msq(Z - I), msq(Z) - 1], [x, y], dict=True)
    pts = {simplify(Z.subs(s)) for s in sols}
    s2 = (len(pts) == 1 and simplify(list(pts)[0] - (1 + I)/sqrt(2)) == 0)
    return (bool(s1), bool(s2))
q("U02-B-055", "Loci in the Argand plane", "Equality case and locus intersection", "Difficult", "Statement-based MCQ",
  r"Arguments are principal values in $(-\pi, \pi]$. Statement I: If $|z_1| = 2$, $|z_2| = 3$ and $|z_1 + z_2| = 1$, then $|\arg(z_1) - \arg(z_2)| = \pi$. Statement II: If $|z - 1| = |z - i|$ and $|z| = 1$, then $z = \frac{1 + i}{\sqrt{2}}$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Finds one intersection point of the line $y = x$ with $|z| = 1$ and misses the second."),
   (ST_FF, r"Doubts Statement I because $z_1, z_2$ are not fixed, without using the equality case of the triangle inequality."),
   (ST_FT, r"Reads $|z_1 + z_2| = 1$ as $z_1, z_2$ in the same direction, and also misses the second intersection point.")],
  r"In Statement I, $|z_1 + z_2| = 1 = |z_2| - |z_1|$ is the equality case of the triangle inequality, so $z_1$ and $z_2$ point in opposite directions. Their principal arguments then differ by $\pi$ or $-\pi$ (for example $z_1 = 2, z_2 = -3$ gives $-\pi$), so $|\arg(z_1) - \arg(z_2)| = \pi$ and Statement I is true. In Statement II, $|z - 1| = |z - i|$ is the line $y = x$, which meets $|z| = 1$ at $\pm\frac{1 + i}{\sqrt{2}}$, so $z$ is not determined uniquely and Statement II is false.",
  "Missing the second intersection of a line through the origin with a circle centred at the origin.",
  "U02-statement-traps-mixed", "Equality case of the triangle inequality plus a two-point locus intersection.",
  check=_c55, values=[TF, TT, FF, FT], cognitive="Analysis")
