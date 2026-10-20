import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
SC = "XII"
TOPIC = "Vector (cross) product"


def V(*x):
    return Matrix(x)


def cr(a, b):
    return Matrix(a).cross(Matrix(b))


def nm(v):
    v = Matrix(v)
    return sqrt(simplify(v.dot(v)))


def unit(v):
    v = Matrix(v)
    return simplify(v / nm(v))


def posfirst(v):
    """fix the sign of a direction so that its first nonzero component is positive"""
    v = Matrix(v)
    for c in v:
        if c != 0:
            return v if c > 0 else -v
    return v


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."
VS = [(True, True), (False, False), (True, False), (False, True)]

# ================================================================ EASY (16)


def _c001():
    a, b = V(2, -1, 1), V(1, 3, -2)
    return nm(cr(a, b))


q("U12-C-001", TOPIC, "Magnitude of a cross product", "Easy", "Single-step computation MCQ",
  r"If $\vec{a} = 2\hat{i} - \hat{j} + \hat{k}$ and $\vec{b} = \hat{i} + 3\hat{j} - 2\hat{k}$, then $|\vec{a} \times \vec{b}|$ equals",
  r"$5\sqrt{3}$",
  [(r"$\frac{5\sqrt{3}}{2}$", r"Halves the magnitude as if finding the area of a triangle: $\frac{1}{2}\sqrt{75}$."),
   (r"$2\sqrt{21}$", r"Multiplies the magnitudes, $|\vec{a}||\vec{b}| = \sqrt{6}\sqrt{14} = \sqrt{84}$, ignoring the factor $\sin\theta$."),
   (r"$3\sqrt{11}$", r"Adds instead of subtracting in the $\hat{i}$ minor: $(-1)(-2) + (1)(3) = 5$, giving $(5, 5, 7)$ with magnitude $\sqrt{99}$.")],
  r"$\vec{a} \times \vec{b} = ((-1)(-2) - (1)(3))\hat{i} - ((2)(-2) - (1)(1))\hat{j} + ((2)(3) - (-1)(1))\hat{k} = -\hat{i} + 5\hat{j} + 7\hat{k}$. Hence $|\vec{a} \times \vec{b}| = \sqrt{1 + 25 + 49} = \sqrt{75} = 5\sqrt{3}$.",
  r"Confusing $|\vec{a} \times \vec{b}|$ with $|\vec{a}||\vec{b}|$ or with the triangle area.",
  "U12-C-cross-magnitude", "One determinant expansion and a magnitude.",
  check=_c001, values=[5 * sqrt(3), 5 * sqrt(3) / 2, 2 * sqrt(21), 3 * sqrt(11)], cognitive="Application", source_class=SC)


def _c002():
    a, b = V(1, 2, 3), V(3, -2, 1)
    return nm(cr(a, b))


q("U12-C-002", TOPIC, "Area of a parallelogram from adjacent sides", "Easy", "Single-step computation MCQ",
  r"The area of the parallelogram whose adjacent sides are represented by $\vec{a} = \hat{i} + 2\hat{j} + 3\hat{k}$ and $\vec{b} = 3\hat{i} - 2\hat{j} + \hat{k}$ is",
  r"$8\sqrt{3}$",
  [(r"$4\sqrt{3}$", r"Uses the triangle formula $\frac{1}{2}|\vec{a} \times \vec{b}|$ for a parallelogram."),
   (r"$14$", r"Takes the area as $|\vec{a}||\vec{b}| = \sqrt{14}\sqrt{14}$, treating the sides as perpendicular."),
   (r"$10\sqrt{2}$", r"Uses $|\vec{a} \times \vec{b}|^2 = |\vec{a}|^2|\vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = 196 + 4 = 200$, a sign error in the Lagrange identity.")],
  r"$\vec{a} \times \vec{b} = (2 + 6)\hat{i} - (1 - 9)\hat{j} + (-2 - 6)\hat{k} = 8\hat{i} + 8\hat{j} - 8\hat{k}$, so the area is $|\vec{a} \times \vec{b}| = 8\sqrt{3}$. (Check: $|\vec{a}|^2|\vec{b}|^2 - (\vec{a}\cdot\vec{b})^2 = 196 - 4 = 192$.)",
  r"Mixing up the parallelogram and triangle area formulas.",
  "U12-C-area-parallelogram-sides", r"Direct application of area $= |\vec{a} \times \vec{b}|$.",
  check=_c002, values=[8 * sqrt(3), 4 * sqrt(3), 14, 10 * sqrt(2)], cognitive="Application", source_class=SC)


def _c003():
    P, Q, R = V(1, 1, 1), V(1, 2, 3), V(2, 3, 1)
    return nm(cr(Q - P, R - P)) / 2


q("U12-C-003", TOPIC, "Area of a triangle from its vertices", "Easy", "Single-step computation MCQ",
  r"The area of the triangle with vertices $P(1, 1, 1)$, $Q(1, 2, 3)$ and $R(2, 3, 1)$ is",
  r"$\frac{\sqrt{21}}{2}$",
  [(r"$\sqrt{21}$", r"Forgets the factor $\frac{1}{2}$ and reports $|\overrightarrow{PQ} \times \overrightarrow{PR}|$."),
   (r"$\frac{5\sqrt{3}}{2}$", r"Uses the position vectors of $Q$ and $R$ directly: $\frac{1}{2}|\overrightarrow{OQ} \times \overrightarrow{OR}| = \frac{1}{2}|(-7, 5, -1)| = \frac{\sqrt{75}}{2}$."),
   (r"$\frac{5}{2}$", r"Takes $\frac{1}{2}|\overrightarrow{PQ}||\overrightarrow{PR}| = \frac{1}{2}\sqrt{5}\sqrt{5}$, assuming a right angle at $P$.")],
  r"$\overrightarrow{PQ} = \hat{j} + 2\hat{k}$ and $\overrightarrow{PR} = \hat{i} + 2\hat{j}$. Then $\overrightarrow{PQ} \times \overrightarrow{PR} = (0 - 4)\hat{i} - (0 - 2)\hat{j} + (0 - 1)\hat{k} = -4\hat{i} + 2\hat{j} - \hat{k}$, of magnitude $\sqrt{21}$. The area is $\frac{\sqrt{21}}{2}$.",
  r"Crossing position vectors instead of side vectors.",
  "U12-C-triangle-vertices", "Two side vectors and one cross product.",
  check=_c003, values=[sqrt(21) / 2, sqrt(21), 5 * sqrt(3) / 2, Rational(5, 2)], cognitive="Application", source_class=SC)


def _c004():
    a, b = V(1, 1, 1), V(1, -1, 1)
    return posfirst(unit(cr(a, b)))


q("U12-C-004", TOPIC, "Unit vector perpendicular to two vectors", "Easy", "Single-step computation MCQ",
  r"A unit vector perpendicular to both $\vec{a} = \hat{i} + \hat{j} + \hat{k}$ and $\vec{b} = \hat{i} - \hat{j} + \hat{k}$ is",
  r"$\frac{1}{\sqrt{2}}(\hat{i} - \hat{k})$",
  [(r"$\frac{1}{\sqrt{2}}(\hat{i} + \hat{k})$", r"Sign slip in the $\hat{k}$ minor, writing $a_2b_1 - a_1b_2 = 2$, so the cross product becomes $2\hat{i} + 2\hat{k}$."),
   (r"$\hat{j}$", r"Normalises $\vec{a} - \vec{b} = 2\hat{j}$ instead of $\vec{a} \times \vec{b}$."),
   (r"$\frac{1}{\sqrt{6}}(\hat{i} - 2\hat{j} + \hat{k})$", r"Picks a unit vector perpendicular to $\vec{a}$ only; its dot product with $\vec{b}$ is $\frac{4}{\sqrt{6}} \ne 0$.")],
  r"$\vec{a} \times \vec{b} = (1 + 1)\hat{i} - (1 - 1)\hat{j} + (-1 - 1)\hat{k} = 2\hat{i} - 2\hat{k}$, with magnitude $2\sqrt{2}$. Hence $\pm\frac{1}{\sqrt{2}}(\hat{i} - \hat{k})$ are the required unit vectors, and $\frac{1}{\sqrt{2}}(\hat{i} - \hat{k})$ is one of them.",
  r"Using a vector perpendicular to only one of the two given vectors.",
  "U12-C-unit-perp", "One cross product followed by normalisation.",
  check=_c004, values=[V(1, 0, -1) / sqrt(2), V(1, 0, 1) / sqrt(2), V(0, 1, 0), V(1, -2, 1) / sqrt(6)], cognitive="Application", source_class=SC)


def _c005():
    A, B, d = 3, 4, 6
    return (A * B) ** 2 - d ** 2


q("U12-C-005", TOPIC, "Lagrange identity", "Easy", "Single-step computation MCQ",
  r"If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and $\vec{a}\cdot\vec{b} = 6$, then $|\vec{a} \times \vec{b}|^2$ equals",
  r"$108$",
  [(r"$180$", r"Adds instead of subtracting: $|\vec{a}|^2|\vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = 144 + 36$."),
   (r"$36$", r"Finds $\cos\theta = \frac{1}{2}$ and then uses $\sin\theta = \frac{1}{2}$ as well, giving $144 \cdot \frac{1}{4}$."),
   (r"$72$", r"Writes $\sin^2\theta = 1 - \cos\theta = \frac{1}{2}$ instead of $1 - \cos^2\theta$, giving $144 \cdot \frac{1}{2}$.")],
  r"By the identity $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = |\vec{a}|^2|\vec{b}|^2$, we get $|\vec{a} \times \vec{b}|^2 = 9 \cdot 16 - 36 = 108$.",
  r"Sign error in $|\vec{a} \times \vec{b}|^2 = |\vec{a}|^2|\vec{b}|^2 - (\vec{a}\cdot\vec{b})^2$.",
  "U12-C-lagrange-identity", "One identity, one substitution.",
  check=_c005, values=[108, 180, 36, 72], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and $\vec{a}\cdot\vec{b} = 6$, then the value of $|\vec{a} \times \vec{b}|^2$ is", answer=108))


def _c006():
    lam, mu = symbols('lam mu')
    s = solve(list(cr(V(2, lam, 3), V(4, -6, mu))), [lam, mu], dict=True)
    return s[0][lam] + s[0][mu]


q("U12-C-006", TOPIC, "Zero cross product and parallel vectors", "Easy", "Inverse/parameter MCQ",
  r"If $(2\hat{i} + \lambda\hat{j} + 3\hat{k}) \times (4\hat{i} - 6\hat{j} + \mu\hat{k}) = \vec{0}$, where $\lambda, \mu \in \mathbb{R}$, then $\lambda + \mu$ equals",
  r"$3$",
  [(r"$9$", r"Sign slip in the ratio: takes $\frac{2}{4} = \frac{\lambda}{6}$, so $\lambda = 3$, and with $\mu = 6$ gets $9$."),
   (r"$-9$", r"Gets $\lambda = -3$ correctly but takes $\frac{2}{4} = \frac{3}{-\mu}$, so $\mu = -6$."),
   (r"$-\frac{3}{2}$", r"Inverts the ratio for $\mu$, writing $\frac{2}{4} = \frac{\mu}{3}$, so $\mu = \frac{3}{2}$, and adds $\lambda = -3$.")],
  r"A zero cross product of non-zero vectors means they are parallel, so $\frac{2}{4} = \frac{\lambda}{-6} = \frac{3}{\mu}$. Hence $\lambda = -3$ and $\mu = 6$, giving $\lambda + \mu = 3$.",
  r"Mishandling signs when equating ratios of components.",
  "U12-C-parallel-cross-zero", "Recognise parallelism, then two proportions.",
  check=_c006, values=[3, 9, -9, Rational(-3, 2)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $(2\hat{i} + \lambda\hat{j} + 3\hat{k}) \times (4\hat{i} - 6\hat{j} + \mu\hat{k}) = \vec{0}$, where $\lambda, \mu \in \mathbb{R}$, then the value of $\lambda + \mu$ is", answer=3))


def _c007():
    th = symbols('theta')
    sols = solveset(Eq(sin(th), sqrt(3) * cos(th)), th, Interval(0, pi))
    return list(sols)[0]


q("U12-C-007", TOPIC, "Angle from cross and dot products", "Easy", "Single-step computation MCQ",
  r"Let $\vec{a}$ and $\vec{b}$ be non-zero, non-parallel vectors such that $|\vec{a} \times \vec{b}| = \sqrt{3}\,(\vec{a}\cdot\vec{b})$. The angle between $\vec{a}$ and $\vec{b}$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{\pi}{6}$", r"Inverts the ratio and solves $\tan\theta = \frac{1}{\sqrt{3}}$."),
   (r"$\frac{2\pi}{3}$", r"Solves $|\tan\theta| = \sqrt{3}$ and picks the obtuse angle, ignoring that $\vec{a}\cdot\vec{b} > 0$ here."),
   (r"$\frac{5\pi}{6}$", r"Inverts the ratio to $\tan\theta = \frac{1}{\sqrt{3}}$ in magnitude and then picks the obtuse angle.")],
  r"$|\vec{a}||\vec{b}|\sin\theta = \sqrt{3}|\vec{a}||\vec{b}|\cos\theta$. Since the left side is positive, $\cos\theta > 0$ and $\tan\theta = \sqrt{3}$, so $\theta = \frac{\pi}{3}$.",
  r"Inverting $\tan\theta = \frac{|\vec{a} \times \vec{b}|}{\vec{a}\cdot\vec{b}}$.",
  "U12-C-angle-from-cross-dot", "One ratio of the two products.",
  check=_c007, values=[pi / 3, pi / 6, 2 * pi / 3, 5 * pi / 6], cognitive="Understanding", source_class=SC)


def _c008():
    i, j, k = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
    return cr(i, i + j) + cr(j, j + k) + cr(k, k + i)


q("U12-C-008", TOPIC, "Cross products of unit vectors", "Easy", "Single-step computation MCQ",
  r"The vector $\hat{i} \times (\hat{i} + \hat{j}) + \hat{j} \times (\hat{j} + \hat{k}) + \hat{k} \times (\hat{k} + \hat{i})$ equals",
  r"$\hat{i} + \hat{j} + \hat{k}$",
  [(r"$-(\hat{i} + \hat{j} + \hat{k})$", r"Uses the reversed cyclic order, taking $\hat{i} \times \hat{j} = -\hat{k}$ and so on."),
   (r"$\vec{0}$", r"Assumes the cyclic terms cancel each other, as they would in $\hat{i} \times \hat{j} + \hat{j} \times \hat{i}$."),
   (r"$2(\hat{i} + \hat{j} + \hat{k})$", r"Takes $\hat{i} \times \hat{i} = \hat{i}$ (and similarly) instead of $\vec{0}$, adding an extra $\hat{i} + \hat{j} + \hat{k}$.")],
  r"Since $\hat{i} \times \hat{i} = \hat{j} \times \hat{j} = \hat{k} \times \hat{k} = \vec{0}$, the sum is $\hat{i} \times \hat{j} + \hat{j} \times \hat{k} + \hat{k} \times \hat{i} = \hat{k} + \hat{i} + \hat{j}$.",
  r"Treating $\hat{i} \times \hat{i}$ as non-zero or reversing the cyclic order.",
  "U12-C-unit-vector-products", "Recall of the basic cross product table.",
  check=_c008, values=[V(1, 1, 1), V(-1, -1, -1), V(0, 0, 0), V(2, 2, 2)], cognitive="Recall", source_class=SC)


def _c009():
    return nm(cr(V(3, 4, 0), V(-5, 7, 0))) / 2


q("U12-C-009", TOPIC, "Area of a triangle in a plane", "Easy", "Single-step computation MCQ",
  r"Two sides of a triangle are represented by the vectors $3\hat{i} + 4\hat{j}$ and $-5\hat{i} + 7\hat{j}$. The area of the triangle is",
  r"$\frac{41}{2}$",
  [(r"$41$", r"Forgets the factor $\frac{1}{2}$ and gives the parallelogram area."),
   (r"$\frac{1}{2}$", r"Sign slip in the $\hat{k}$ component: $3 \cdot 7 + 4 \cdot (-5) = 1$ instead of $21 + 20$."),
   (r"$\frac{13}{2}$", r"Uses the dot product $-15 + 28 = 13$ in place of the cross product.")],
  r"$(3\hat{i} + 4\hat{j}) \times (-5\hat{i} + 7\hat{j}) = (3 \cdot 7 - 4 \cdot (-5))\hat{k} = 41\hat{k}$, so the area is $\frac{41}{2}$.",
  r"Mixing the dot product with the cross product for planar vectors.",
  "U12-C-triangle-sides-2d", "One 2 by 2 determinant.",
  check=_c009, values=[Rational(41, 2), 41, Rational(1, 2), Rational(13, 2)], cognitive="Application", source_class=SC)


def _c010():
    d1, d2 = V(3, 1, -2), V(1, -3, 4)
    return nm(cr(d1, d2)) / 2


q("U12-C-010", TOPIC, "Area of a parallelogram from its diagonals", "Easy", "Single-step computation MCQ",
  r"The diagonals of a parallelogram are represented by $3\hat{i} + \hat{j} - 2\hat{k}$ and $\hat{i} - 3\hat{j} + 4\hat{k}$. The area of the parallelogram is",
  r"$5\sqrt{3}$",
  [(r"$10\sqrt{3}$", r"Treats the diagonals as adjacent sides and reports $|\vec{d}_1 \times \vec{d}_2|$."),
   (r"$\frac{5\sqrt{3}}{2}$", r"Applies the factor $\frac{1}{2}$ twice, as for a triangle on top of the diagonal formula."),
   (r"$\sqrt{91}$", r"Uses the rhombus rule $\frac{1}{2}|\vec{d}_1||\vec{d}_2| = \frac{1}{2}\sqrt{14}\sqrt{26}$, assuming perpendicular diagonals.")],
  r"Area $= \frac{1}{2}|\vec{d}_1 \times \vec{d}_2|$. Here $\vec{d}_1 \times \vec{d}_2 = (4 - 6)\hat{i} - (12 + 2)\hat{j} + (-9 - 1)\hat{k} = -2\hat{i} - 14\hat{j} - 10\hat{k}$, of magnitude $\sqrt{300} = 10\sqrt{3}$, so the area is $5\sqrt{3}$.",
  r"Using the side formula when the diagonals are given.",
  "U12-C-area-diagonals", "One cross product with the diagonal formula.",
  check=_c010, values=[5 * sqrt(3), 10 * sqrt(3), 5 * sqrt(3) / 2, sqrt(91)], cognitive="Application", source_class=SC)


def _c011():
    a, b = V(1, 2, 2), V(2, 1, -2)
    return posfirst(6 * unit(cr(a, b)))


q("U12-C-011", TOPIC, "Vector of given magnitude perpendicular to two vectors", "Easy", "Single-step computation MCQ",
  r"A vector of magnitude $6$ that is perpendicular to both $\hat{i} + 2\hat{j} + 2\hat{k}$ and $2\hat{i} + \hat{j} - 2\hat{k}$ is",
  r"$4\hat{i} - 4\hat{j} + 2\hat{k}$",
  [(r"$4\hat{i} + 4\hat{j} + 2\hat{k}$", r"Omits the minus sign on the $\hat{j}$ minor, so the cross product comes out parallel to $2\hat{i} + 2\hat{j} + \hat{k}$."),
   (r"$-6\hat{i} + 6\hat{j} - 3\hat{k}$", r"Stops at the cross product itself, whose magnitude is $9$, not $6$."),
   (r"$2\hat{i} - 2\hat{j} + \hat{k}$", r"Removes the common factor $-3$ from the cross product and stops; this vector has magnitude $3$.")],
  r"The cross product is $(-4 - 2)\hat{i} - (-2 - 4)\hat{j} + (1 - 4)\hat{k} = -6\hat{i} + 6\hat{j} - 3\hat{k}$, of magnitude $9$. The required vectors are $\pm\frac{6}{9}(-6\hat{i} + 6\hat{j} - 3\hat{k}) = \pm(4\hat{i} - 4\hat{j} + 2\hat{k})$.",
  r"Not scaling the unit normal to the required magnitude.",
  "U12-C-unit-perp", "Cross product, normalise, scale.",
  check=_c011, values=[V(4, -4, 2), V(4, 4, 2), V(-6, 6, -3), V(2, -2, 1)], cognitive="Application", source_class=SC)


def _c012():
    b = symbols('b', positive=True)
    return solve(Eq(4 ** 2 * b ** 2, 144), b)[0]


q("U12-C-012", TOPIC, "Lagrange identity", "Easy", "Inverse/parameter MCQ",
  r"If $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = 144$ and $|\vec{a}| = 4$, then $|\vec{b}|$ equals",
  r"$3$",
  [(r"$9$", r"Solves for $|\vec{b}|^2 = 9$ and forgets to take the square root."),
   (r"$6$", r"Uses $|\vec{a}|$ instead of $|\vec{a}|^2$: $4|\vec{b}|^2 = 144$ gives $|\vec{b}| = 6$."),
   (r"$12$", r"Takes $\sqrt{144} = 12$ itself as $|\vec{b}|$, ignoring the factor $|\vec{a}|$.")],
  r"The left side equals $|\vec{a}|^2|\vec{b}|^2$ for all vectors. So $16|\vec{b}|^2 = 144$, giving $|\vec{b}| = 3$.",
  r"Not recognising $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = |\vec{a}|^2|\vec{b}|^2$.",
  "U12-C-lagrange-identity", "Recognise the identity, one equation.",
  check=_c012, values=[3, 9, 6, 12], cognitive="Understanding", source_class=SC,
  numerical=dict(question=r"If $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = 144$ and $|\vec{a}| = 4$, then the value of $|\vec{b}|$ is", answer=3))


def _c013():
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4')
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    lhs = expand(cr(a + b, a - b))
    axb = cr(a, b)
    k = simplify(lhs[0] / axb[0])  # scalar multiple of a x b
    return k * V(2, -1, 2)


q("U12-C-013", TOPIC, "Algebra of cross products", "Easy", "Single-step computation MCQ",
  r"If $\vec{a} \times \vec{b} = 2\hat{i} - \hat{j} + 2\hat{k}$, then $(\vec{a} + \vec{b}) \times (\vec{a} - \vec{b})$ equals",
  r"$-4\hat{i} + 2\hat{j} - 4\hat{k}$",
  [(r"$4\hat{i} - 2\hat{j} + 4\hat{k}$", r"Expands to $-\vec{a} \times \vec{b} + \vec{b} \times \vec{a}$ but then treats both terms as $+\vec{a} \times \vec{b}$, giving $2(\vec{a} \times \vec{b})$."),
   (r"$\vec{0}$", r"Takes $\vec{b} \times \vec{a} = \vec{a} \times \vec{b}$, so that $-\vec{a} \times \vec{b} + \vec{b} \times \vec{a}$ cancels."),
   (r"$-2\hat{i} + \hat{j} - 2\hat{k}$", r"Drops the $\vec{b} \times \vec{a}$ term and keeps only $-\vec{a} \times \vec{b}$.")],
  r"$(\vec{a} + \vec{b}) \times (\vec{a} - \vec{b}) = \vec{a} \times \vec{a} - \vec{a} \times \vec{b} + \vec{b} \times \vec{a} - \vec{b} \times \vec{b} = -2(\vec{a} \times \vec{b}) = -4\hat{i} + 2\hat{j} - 4\hat{k}$.",
  r"Treating the cross product as commutative.",
  "U12-C-expand-cross-algebra", "One expansion using anticommutativity.",
  check=_c013, values=[V(-4, 2, -4), V(4, -2, 4), V(0, 0, 0), V(-2, 1, -2)], cognitive="Understanding", source_class=SC)


def _c014():
    a, b = V(1, 2, 0), V(0, 1, 3)
    s1 = cr(a, b) == cr(b, a)
    s2 = simplify(nm(cr(a, b)) - nm(cr(b, a))) == 0
    return (bool(s1), bool(s2))


q("U12-C-014", TOPIC, "Properties of the cross product", "Easy", "Statement-based MCQ",
  r"Statement I: For all vectors $\vec{a}$ and $\vec{b}$, $\vec{a} \times \vec{b} = \vec{b} \times \vec{a}$. Statement II: For all vectors $\vec{a}$ and $\vec{b}$, $|\vec{a} \times \vec{b}| = |\vec{b} \times \vec{a}|$." + TAIL,
  ST_FT,
  [(ST_TT, r"Believes the cross product is commutative like the dot product."),
   (ST_FF, r"Thinks that since $\vec{b} \times \vec{a} = -\vec{a} \times \vec{b}$, even the magnitudes differ."),
   (ST_TF, r"Reverses the two facts: accepts commutativity and rejects equal magnitudes.")],
  r"$\vec{b} \times \vec{a} = -(\vec{a} \times \vec{b})$, so Statement I fails whenever $\vec{a} \times \vec{b} \ne \vec{0}$; for example $\hat{i} \times \hat{j} = \hat{k}$ but $\hat{j} \times \hat{i} = -\hat{k}$. A vector and its negative have the same magnitude, so Statement II is true.",
  r"Assuming the cross product is commutative.",
  "U12-C-cross-properties-statement", "Recall of anticommutativity.",
  check=_c014, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Recall", source_class=SC)


def _c015():
    P, Q, R = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
    return nm(cr(Q - P, R - P)) / 2


q("U12-C-015", TOPIC, "Area of a triangle from its vertices", "Easy", "Single-step computation MCQ",
  r"The area of the triangle whose vertices have position vectors $\hat{i}$, $\hat{j}$ and $\hat{k}$ is",
  r"$\frac{\sqrt{3}}{2}$",
  [(r"$\sqrt{3}$", r"Forgets the factor $\frac{1}{2}$."),
   (r"$\frac{1}{2}$", r"Computes $\frac{1}{2}|\hat{i} \times \hat{j}|$, the area of the triangle with vertices $O$, $\hat{i}$, $\hat{j}$."),
   (r"$\frac{3}{2}$", r"Adds the areas $\frac{1}{2}$ of the three coordinate-plane projections instead of combining them as a vector.")],
  r"With $P(1,0,0)$, $Q(0,1,0)$, $R(0,0,1)$: $\overrightarrow{PQ} = -\hat{i} + \hat{j}$, $\overrightarrow{PR} = -\hat{i} + \hat{k}$, and $\overrightarrow{PQ} \times \overrightarrow{PR} = \hat{i} + \hat{j} + \hat{k}$. The area is $\frac{\sqrt{3}}{2}$.",
  r"Using position vectors from the origin instead of side vectors.",
  "U12-C-triangle-vertices", "Two side vectors and one cross product.",
  check=_c015, values=[sqrt(3) / 2, sqrt(3), Rational(1, 2), Rational(3, 2)], cognitive="Application", source_class=SC)


def _c016():
    A, B, P = 4, 5, 3
    a1, b1, b2 = symbols('a1 b1 b2', real=True)
    a = V(A, 0, 0)
    sols = solve([Eq(a.dot(V(b1, b2, 0)) / A, P), Eq(b1 ** 2 + b2 ** 2, B ** 2)], [b1, b2], dict=True)
    vals = {simplify(nm(cr(a, V(sl[b1], sl[b2], 0)))) for sl in sols}
    assert len(vals) == 1
    return vals.pop()


q("U12-C-016", TOPIC, "Cross product from a projection", "Easy", "Multi-step computation MCQ",
  r"Let $|\vec{a}| = 4$ and $|\vec{b}| = 5$, and let the scalar projection of $\vec{b}$ on $\vec{a}$ be $3$. Then $|\vec{a} \times \vec{b}|$ equals",
  r"$16$",
  [(r"$12$", r"Multiplies $|\vec{a}|$ by the projection $3$, which gives $\vec{a}\cdot\vec{b} = 12$ rather than $|\vec{a} \times \vec{b}|$."),
   (r"$20$", r"Takes $|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}| = 4 \cdot 5$, as if $\vec{a} \perp \vec{b}$."),
   (r"$4$", r"Finds the component of $\vec{b}$ perpendicular to $\vec{a}$, $\sqrt{25 - 9} = 4$, and stops without multiplying by $|\vec{a}| = 4$.")],
  r"The scalar projection gives $\frac{\vec{a}\cdot\vec{b}}{|\vec{a}|} = 3$, so $\vec{a}\cdot\vec{b} = 12$. By Lagrange's identity, $|\vec{a} \times \vec{b}|^2 = |\vec{a}|^2|\vec{b}|^2 - (\vec{a}\cdot\vec{b})^2 = 400 - 144 = 256$, so $|\vec{a} \times \vec{b}| = 16$. Equivalently, the component of $\vec{b}$ perpendicular to $\vec{a}$ has length $\sqrt{25 - 9} = 4$, and $|\vec{a} \times \vec{b}| = 4 \cdot 4 = 16$.",
  r"Confusing the projection product $|\vec{a}|\,(\text{projection})$, which is $\vec{a}\cdot\vec{b}$, with $|\vec{a} \times \vec{b}|$.",
  "U12-C-cross-from-projection", r"Convert the projection to $\vec{a}\cdot\vec{b}$, then one use of Lagrange's identity.",
  check=_c016, values=[16, 12, 20, 4], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $|\vec{a}| = 4$ and $|\vec{b}| = 5$, and let the scalar projection of $\vec{b}$ on $\vec{a}$ be $3$. Then the value of $|\vec{a} \times \vec{b}|$ is", answer=16))

# ================================================================ MEDIUM (24)


def _c017():
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4')
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    w = expand(cr(2 * a + b, a - 3 * b))
    k = simplify(w[0] / cr(a, b)[0])
    return Abs(k) * 5


q("U12-C-017", TOPIC, "Area with sides given as combinations", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a} \times \vec{b}| = 5$, then the area of the parallelogram whose adjacent sides are $2\vec{a} + \vec{b}$ and $\vec{a} - 3\vec{b}$ is",
  r"$35$",
  [(r"$25$", r"Takes $\vec{b} \times \vec{a} = +\vec{a} \times \vec{b}$, so the product becomes $-6\vec{a} \times \vec{b} + \vec{a} \times \vec{b} = -5\vec{a} \times \vec{b}$."),
   (r"$30$", r"Keeps $-6\vec{a} \times \vec{b}$ but drops the cross term $\vec{b} \times \vec{a}$."),
   (r"$\frac{35}{2}$", r"Uses the triangle factor $\frac{1}{2}$ for a parallelogram.")],
  r"$(2\vec{a} + \vec{b}) \times (\vec{a} - 3\vec{b}) = -6\,\vec{a} \times \vec{b} + \vec{b} \times \vec{a} = -7\,\vec{a} \times \vec{b}$, since $\vec{a} \times \vec{a} = \vec{b} \times \vec{b} = \vec{0}$. The area is $7 \cdot 5 = 35$.",
  r"Forgetting $\vec{b} \times \vec{a} = -\vec{a} \times \vec{b}$.",
  "U12-C-area-combination", "Bilinear expansion with anticommutativity, then area.",
  check=_c017, values=[35, 25, 30, Rational(35, 2)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $|\vec{a} \times \vec{b}| = 5$, then the area of the parallelogram whose adjacent sides are $2\vec{a} + \vec{b}$ and $\vec{a} - 3\vec{b}$ is", answer=35))


q("U12-C-018", TOPIC, "Vector identities from cross products", "Medium", "Conceptual/application MCQ",
  r"Let $\vec{a}, \vec{b}, \vec{c}, \vec{d}$ be vectors such that $\vec{a} \times \vec{b} = \vec{c} \times \vec{d}$ and $\vec{a} \times \vec{c} = \vec{b} \times \vec{d}$. Which of the following is necessarily true?",
  r"$\vec{a} - \vec{d}$ is parallel to $\vec{b} - \vec{c}$",
  [(r"$\vec{a} - \vec{d}$ is perpendicular to $\vec{b} - \vec{c}$", r"Subtracts the equations and concludes a zero dot product, mixing up $\times$ with $\cdot$."),
   (r"$\vec{a} + \vec{b}$ is parallel to $\vec{c} + \vec{d}$", r"Groups the vectors by the left and right sides of the first equation and assumes the sums inherit the relation; in fact $(\vec{a} + \vec{b}) \times (\vec{c} + \vec{d})$ contains $\vec{a} \times \vec{d}$ and $\vec{b} \times \vec{c}$, which the conditions do not control (for $\vec{a} = \hat{i}$, $\vec{b} = \hat{j}$, $\vec{c} = \frac{1}{2}\hat{i}$, $\vec{d} = 2\hat{j}$ it equals $\frac{3}{2}\hat{k}$)."),
   (r"$\vec{a} - \vec{b}$ is parallel to $\vec{c} - \vec{d}$", r"Pairs the vectors in the order they appear in the first equation instead of testing the cross product that actually vanishes.")],
  r"$(\vec{a} - \vec{d}) \times (\vec{b} - \vec{c}) = \vec{a} \times \vec{b} - \vec{a} \times \vec{c} - \vec{d} \times \vec{b} + \vec{d} \times \vec{c} = \vec{a} \times \vec{b} - \vec{a} \times \vec{c} + \vec{b} \times \vec{d} - \vec{c} \times \vec{d}$. Using the two given equations this is $\vec{0}$, so $\vec{a} - \vec{d}$ and $\vec{b} - \vec{c}$ are parallel (one of them may be zero). The other relations do not follow in general.",
  r"Losing track of signs when reversing the order of a cross product.",
  "U12-C-vector-identity-parallel", "Choose the right combination and expand with anticommutativity.",
  check=None, values=None, cognitive="Analysis", source_class=SC)


def _c019():
    P, Q, R = V(1, -1, 2), V(2, 0, -1), V(0, 2, 1)
    return posfirst(unit(cr(Q - P, R - P)))


q("U12-C-019", TOPIC, "Unit normal to the plane of three points", "Medium", "Multi-step computation MCQ",
  r"A unit vector perpendicular to the plane containing the points $P(1, -1, 2)$, $Q(2, 0, -1)$ and $R(0, 2, 1)$ is",
  r"$\frac{1}{\sqrt{6}}(2\hat{i} + \hat{j} + \hat{k})$",
  [(r"$\frac{1}{\sqrt{6}}(-2\hat{i} + \hat{j} + \hat{k})$", r"Reverses the order in the $\hat{i}$ minor, computing $a_3b_2 - a_2b_3 = -8$."),
   (r"$\frac{1}{\sqrt{6}}(2\hat{i} - \hat{j} + \hat{k})$", r"Omits the minus sign in front of the $\hat{j}$ minor."),
   (r"$\frac{1}{\sqrt{6}}(\hat{i} - \hat{j} + 2\hat{k})$", r"Crosses the position vectors $\overrightarrow{OQ} \times \overrightarrow{OR} = 2\hat{i} - 2\hat{j} + 4\hat{k}$ instead of side vectors.")],
  r"$\overrightarrow{PQ} = \hat{i} + \hat{j} - 3\hat{k}$, $\overrightarrow{PR} = -\hat{i} + 3\hat{j} - \hat{k}$. Then $\overrightarrow{PQ} \times \overrightarrow{PR} = (-1 + 9)\hat{i} - (-1 - 3)\hat{j} + (3 + 1)\hat{k} = 8\hat{i} + 4\hat{j} + 4\hat{k} = 4(2\hat{i} + \hat{j} + \hat{k})$. Normalising gives $\pm\frac{1}{\sqrt{6}}(2\hat{i} + \hat{j} + \hat{k})$.",
  r"Using position vectors of the points instead of vectors along the sides.",
  "U12-C-unit-normal-points", "Side vectors, cross product with signs, normalisation.",
  check=_c019, values=[V(2, 1, 1) / sqrt(6), V(-2, 1, 1) / sqrt(6), V(2, -1, 1) / sqrt(6), V(1, -1, 2) / sqrt(6)], cognitive="Application", source_class=SC)


def _c020():
    l = symbols('l', positive=True)
    c = cr(V(1, 1, l), V(1, -1, 0))
    return solve(Eq(c.dot(c), 36), l)[0]


q("U12-C-020", TOPIC, "Parameter from a given area", "Medium", "Inverse/parameter MCQ",
  r"The area of the parallelogram with adjacent sides $\hat{i} + \hat{j} + \lambda\hat{k}$ and $\hat{i} - \hat{j}$ is $6$. If $\lambda > 0$, then $\lambda$ equals",
  r"$4$",
  [(r"$\sqrt{70}$", r"Treats $6$ as a triangle area, so $|\vec{a} \times \vec{b}| = 12$ and $2\lambda^2 + 4 = 144$."),
   (r"$3\sqrt{2}$", r"Drops the constant $4$ from $|\vec{a} \times \vec{b}|^2 = 2\lambda^2 + 4$ and solves $2\lambda^2 = 36$."),
   (r"$4\sqrt{2}$", r"Misses the factor $2$, writing $|\vec{a} \times \vec{b}|^2 = \lambda^2 + 4 = 36$.")],
  r"$(\hat{i} + \hat{j} + \lambda\hat{k}) \times (\hat{i} - \hat{j}) = \lambda\hat{i} + \lambda\hat{j} - 2\hat{k}$, so the area is $\sqrt{2\lambda^2 + 4} = 6$. Then $\lambda^2 = 16$ and, as $\lambda > 0$, $\lambda = 4$.",
  r"Mixing the triangle and parallelogram area formulas in a reverse problem.",
  "U12-C-area-parameter", "Cross product in a parameter, then solve a quadratic.",
  check=_c020, values=[4, sqrt(70), 3 * sqrt(2), 4 * sqrt(2)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The area of the parallelogram with adjacent sides $\hat{i} + \hat{j} + \lambda\hat{k}$ and $\hat{i} - \hat{j}$ is $6$. If $\lambda > 0$, then the value of $\lambda$ is", answer=4))


def _c021():
    th = symbols('theta')
    A, B = 2, 3
    ts = [t for t in solveset(Eq(A * B * sin(th), 3 * sqrt(3)), th, Interval(0, pi)) if cos(t) > 0]
    t = ts[0]
    return sqrt(A ** 2 + B ** 2 - 2 * A * B * cos(t))


q("U12-C-021", TOPIC, "Combining cross and dot products", "Medium", "Multi-step computation MCQ",
  r"Let $|\vec{a}| = 2$, $|\vec{b}| = 3$ and $|\vec{a} \times \vec{b}| = 3\sqrt{3}$. If $\vec{a}\cdot\vec{b} > 0$, then $|\vec{a} - \vec{b}|$ equals",
  r"$\sqrt{7}$",
  [(r"$\sqrt{19}$", r"Takes $\theta = \frac{2\pi}{3}$ (ignoring $\vec{a}\cdot\vec{b} > 0$), so $\vec{a}\cdot\vec{b} = -3$ and $|\vec{a} - \vec{b}|^2 = 13 + 6$."),
   (r"$\sqrt{13}$", r"Assumes $\vec{a} \perp \vec{b}$ and drops the $-2\vec{a}\cdot\vec{b}$ term."),
   (r"$\sqrt{13 - 6\sqrt{3}}$", r"Uses $|\vec{a} \times \vec{b}| = 3\sqrt{3}$ in place of $\vec{a}\cdot\vec{b}$ in $|\vec{a}|^2 + |\vec{b}|^2 - 2\vec{a}\cdot\vec{b}$.")],
  r"$6\sin\theta = 3\sqrt{3}$ gives $\sin\theta = \frac{\sqrt{3}}{2}$; with $\vec{a}\cdot\vec{b} > 0$, $\theta = \frac{\pi}{3}$ and $\vec{a}\cdot\vec{b} = 3$. Then $|\vec{a} - \vec{b}|^2 = 4 + 9 - 6 = 7$, so $|\vec{a} - \vec{b}| = \sqrt{7}$.",
  r"Ignoring the sign condition that decides between $\theta$ and $\pi - \theta$.",
  "U12-C-cross-then-dot-magnitude", "Angle from the cross product, then a dot product expansion.",
  check=_c021, values=[sqrt(7), sqrt(19), sqrt(13), sqrt(13 - 6 * sqrt(3))], cognitive="Application", source_class=SC)


def _c022():
    x, y, z = symbols('x y z')
    a, b, c = V(1, 1, 1), V(1, 0, 1), V(2, 1, 3)
    r = V(x, y, z)
    eqs = list(cr(r, b) - cr(c, b)) + [r.dot(a)]
    s = solve(eqs, [x, y, z], dict=True)[0]
    return r.subs(s)


q("U12-C-022", TOPIC, "Solving a vector equation with a cross product", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = \hat{i} + \hat{j} + \hat{k}$, $\vec{b} = \hat{i} + \hat{k}$ and $\vec{c} = 2\hat{i} + \hat{j} + 3\hat{k}$. If $\vec{r}$ satisfies $\vec{r} \times \vec{b} = \vec{c} \times \vec{b}$ and $\vec{r}\cdot\vec{a} = 0$, then $\vec{r}$ equals",
  r"$-\hat{i} + \hat{j}$",
  [(r"$5\hat{i} + \hat{j} + 6\hat{k}$", r"Sign slip in solving $(\vec{c} + t\vec{b})\cdot\vec{a} = 6 + 2t = 0$, taking $t = 3$."),
   (r"$2\hat{i} + \hat{j} + 3\hat{k}$", r"Cancels $\times\,\vec{b}$ from both sides and takes $\vec{r} = \vec{c}$, ignoring $\vec{r}\cdot\vec{a} = 0$."),
   (r"$-\hat{j} + \hat{k}$", r"Writes $\vec{r} - \vec{c}$ parallel to $\vec{a}$ instead of $\vec{b}$: $\vec{r} = \vec{c} + t\vec{a}$ with $6 + 3t = 0$.")],
  r"$(\vec{r} - \vec{c}) \times \vec{b} = \vec{0}$, so $\vec{r} = \vec{c} + t\vec{b}$. Then $\vec{r}\cdot\vec{a} = \vec{c}\cdot\vec{a} + t\,\vec{b}\cdot\vec{a} = 6 + 2t = 0$, so $t = -3$ and $\vec{r} = (2 - 3)\hat{i} + \hat{j} + (3 - 3)\hat{k} = -\hat{i} + \hat{j}$.",
  r"Cancelling a cross product as if it were ordinary multiplication.",
  "U12-C-r-cross-dot-condition", "Parallel condition from a zero cross product, then a dot condition.",
  check=_c022, values=[V(-1, 1, 0), V(5, 1, 6), V(2, 1, 3), V(0, -1, 1)], cognitive="Application", source_class=SC)


def _c023():
    # sample a != 0; dimension of solution space of d = b - c
    d1, d2, d3 = symbols('d1:4')
    a, d = V(1, 2, 3), V(d1, d2, d3)
    s1 = solve(list(cr(a, d)) + [a.dot(d)], [d1, d2, d3], dict=True)
    s2 = solve(list(cr(a, d)), [d1, d2, d3], dict=True)
    st1 = len(s1) == 1 and all(v == 0 for v in s1[0].values()) and len(s1[0]) == 3
    st2 = len(s2) == 1 and len(s2[0]) == 3 and all(v == 0 for v in s2[0].values())
    return (bool(st1), bool(st2))


q("U12-C-023", TOPIC, "Cancellation in cross products", "Medium", "Statement-based MCQ",
  r"Let $\vec{a} \ne \vec{0}$. Statement I: If $\vec{a} \times \vec{b} = \vec{a} \times \vec{c}$ and $\vec{a}\cdot\vec{b} = \vec{a}\cdot\vec{c}$, then $\vec{b} = \vec{c}$. Statement II: If $\vec{a} \times \vec{b} = \vec{a} \times \vec{c}$, then $\vec{b} = \vec{c}$." + TAIL,
  ST_TF,
  [(ST_TT, r"Cancels $\vec{a}$ from $\vec{a} \times \vec{b} = \vec{a} \times \vec{c}$ as in ordinary algebra, so accepts Statement II too."),
   (ST_FF, r"Thinks that even both conditions together only force $\vec{b} - \vec{c}$ to be parallel to $\vec{a}$."),
   (ST_FT, r"Swaps the roles of the two statements, believing the dot condition spoils the conclusion.")],
  r"Let $\vec{d} = \vec{b} - \vec{c}$. Then $\vec{a} \times \vec{d} = \vec{0}$ means $\vec{d}$ is parallel to $\vec{a}$, and $\vec{a}\cdot\vec{d} = 0$ means $\vec{d}$ is perpendicular to $\vec{a}$; both together force $\vec{d} = \vec{0}$, so Statement I is true. With only the cross condition, $\vec{d}$ can be any multiple of $\vec{a}$; for instance $\vec{c} = \vec{b} + \vec{a}$ gives $\vec{a} \times \vec{c} = \vec{a} \times \vec{b}$ with $\vec{b} \ne \vec{c}$. So Statement II is false.",
  r"Cancelling a common factor in a cross product equation.",
  "U12-C-cancellation-statement", "Two conditions combined to pin down a vector.",
  check=_c023, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding", source_class=SC)


def _c024():
    th = symbols('theta')
    ts = [t for t in solveset(Eq(sin(th), Rational(1, 2)), th, Interval(0, pi)) if cos(t) < 0]
    return sqrt(2 + 2 * cos(ts[0]))


q("U12-C-024", TOPIC, "Combining cross and dot products", "Medium", "Multi-step computation MCQ",
  r"Let $\hat{a}$ and $\hat{b}$ be unit vectors with $|\hat{a} \times \hat{b}| = \frac{1}{2}$ and $\hat{a}\cdot\hat{b} < 0$. Then $|\hat{a} + \hat{b}|$ equals",
  r"$\frac{\sqrt{6} - \sqrt{2}}{2}$",
  [(r"$\frac{\sqrt{6} + \sqrt{2}}{2}$", r"Takes the acute angle $\theta = \frac{\pi}{6}$, ignoring $\hat{a}\cdot\hat{b} < 0$."),
   (r"$1$", r"Uses $\cos\theta = -\frac{1}{2}$ (confusing the given sine value with the cosine), so $|\hat{a} + \hat{b}|^2 = 2 - 1$."),
   (r"$\sqrt{2}$", r"Treats the vectors as perpendicular and drops $2\hat{a}\cdot\hat{b}$.")],
  r"$\sin\theta = \frac{1}{2}$ with $\cos\theta < 0$ gives $\theta = \frac{5\pi}{6}$. Then $|\hat{a} + \hat{b}|^2 = 2 + 2\cos\theta = 2 - \sqrt{3} = \left(\frac{\sqrt{6} - \sqrt{2}}{2}\right)^2$, so $|\hat{a} + \hat{b}| = \frac{\sqrt{6} - \sqrt{2}}{2}$.",
  r"Choosing the wrong one of $\theta$ and $\pi - \theta$ from a sine value.",
  "U12-C-cross-then-dot-magnitude", "Angle from the cross product with a sign condition, then denesting.",
  check=_c024, values=[(sqrt(6) - sqrt(2)) / 2, (sqrt(6) + sqrt(2)) / 2, 1, sqrt(2)], cognitive="Application", source_class=SC)


q("U12-C-025", TOPIC, "Collinearity through cross products", "Medium", "Conceptual/application MCQ",
  r"Let $\vec{a}, \vec{b}, \vec{c}$ be the position vectors of three distinct points $P, Q, R$. If $\vec{a} \times \vec{b} + \vec{b} \times \vec{c} + \vec{c} \times \vec{a} = \vec{0}$, then",
  r"$P$, $Q$, $R$ are collinear",
  [(r"$P$, $Q$, $R$ form an equilateral triangle", r"Reads the cyclic symmetry of the expression as symmetry of the triangle."),
   (r"$\vec{a}$, $\vec{b}$, $\vec{c}$ are mutually perpendicular", r"Thinks each cross product must vanish separately in a special arrangement, mixing up cross and dot conditions."),
   (r"the origin is the centroid of triangle $PQR$", r"Recalls that $\vec{a} + \vec{b} + \vec{c} = \vec{0}$ makes the three cross products equal and wrongly assumes they then cancel; in fact the sum becomes $3\,\vec{a} \times \vec{b}$.")],
  r"$\overrightarrow{PQ} \times \overrightarrow{PR} = (\vec{b} - \vec{a}) \times (\vec{c} - \vec{a}) = \vec{b} \times \vec{c} - \vec{b} \times \vec{a} - \vec{a} \times \vec{c} = \vec{a} \times \vec{b} + \vec{b} \times \vec{c} + \vec{c} \times \vec{a}$. This is twice the vector area of triangle $PQR$, so it vanishes exactly when $P$, $Q$, $R$ are collinear.",
  r"Not linking the cyclic sum to the area of triangle $PQR$.",
  "U12-C-collinear-cross", "Interpreting a cyclic cross-product sum as an area vector.",
  check=None, values=None, cognitive="Understanding", source_class=SC)


def _c026():
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4')
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    k = simplify(expand(cr(a + 2 * b, 2 * a + b))[0] / cr(a, b)[0])
    return Abs(k) * 1 * 1 * sin(pi / 6)


q("U12-C-026", TOPIC, "Area with sides given as combinations", "Medium", "Multi-step computation MCQ",
  r"Let $\hat{a}$ and $\hat{b}$ be unit vectors inclined at an angle $\frac{\pi}{6}$. The area of the parallelogram with adjacent sides $\hat{a} + 2\hat{b}$ and $2\hat{a} + \hat{b}$ is",
  r"$\frac{3}{2}$",
  [(r"$\frac{5}{2}$", r"Takes $\hat{b} \times \hat{a} = +\hat{a} \times \hat{b}$, so the product becomes $5\,\hat{a} \times \hat{b}$."),
   (r"$\frac{3\sqrt{3}}{2}$", r"Uses $\cos\frac{\pi}{6}$ instead of $\sin\frac{\pi}{6}$ for $|\hat{a} \times \hat{b}|$."),
   (r"$\frac{3}{4}$", r"Applies the triangle factor $\frac{1}{2}$ to a parallelogram.")],
  r"$(\hat{a} + 2\hat{b}) \times (2\hat{a} + \hat{b}) = \hat{a} \times \hat{b} + 4\,\hat{b} \times \hat{a} = -3\,\hat{a} \times \hat{b}$. Since $|\hat{a} \times \hat{b}| = \sin\frac{\pi}{6} = \frac{1}{2}$, the area is $\frac{3}{2}$.",
  r"Treating $\hat{b} \times \hat{a}$ as equal to $\hat{a} \times \hat{b}$.",
  "U12-C-area-combination", "Expansion with anticommutativity plus the sine formula.",
  check=_c026, values=[Rational(3, 2), Rational(5, 2), 3 * sqrt(3) / 2, Rational(3, 4)], cognitive="Application", source_class=SC)


def _c027():
    a1, a2, a3 = symbols('a1:4')
    a = V(a1, a2, a3)
    eqs = list(cr(a, V(1, 0, 0)) - V(0, 3, 1)) + list(cr(a, V(0, 1, 0)) - V(-3, 0, 2))
    sol = solve(eqs, [a1, a2, a3], dict=True)
    assert len(sol) == 1
    return a.subs(sol[0]).dot(V(1, 1, 1))


q("U12-C-027", TOPIC, "Recovering a vector from its cross products with unit vectors", "Medium", "Multi-step computation MCQ",
  r"If $\vec{a}$ is a vector such that $\vec{a} \times \hat{i} = 3\hat{j} + \hat{k}$ and $\vec{a} \times \hat{j} = -3\hat{i} + 2\hat{k}$, then $\vec{a}\cdot(\hat{i} + \hat{j} + \hat{k})$ equals",
  r"$4$",
  [(r"$-4$", r"Computes $\hat{i} \times \vec{a}$ and $\hat{j} \times \vec{a}$ instead, reversing every sign, so $\vec{a} = -2\hat{i} + \hat{j} - 3\hat{k}$."),
   (r"$6$", r"Takes $\hat{j} \times \hat{i} = \hat{k}$ in $\vec{a} \times \hat{i}$, so the $\hat{k}$ component gives $a_2 = 1$ and $\vec{a} = 2\hat{i} + \hat{j} + 3\hat{k}$."),
   (r"$0$", r"Takes $\hat{i} \times \hat{j} = -\hat{k}$ in $\vec{a} \times \hat{j}$, so the $\hat{k}$ component gives $a_1 = -2$ and $\vec{a} = -2\hat{i} - \hat{j} + 3\hat{k}$.")],
  r"Write $\vec{a} = a_1\hat{i} + a_2\hat{j} + a_3\hat{k}$. Then $\vec{a} \times \hat{i} = a_2(\hat{j} \times \hat{i}) + a_3(\hat{k} \times \hat{i}) = a_3\hat{j} - a_2\hat{k}$, so $a_3 = 3$ and $a_2 = -1$. Also $\vec{a} \times \hat{j} = a_1(\hat{i} \times \hat{j}) + a_3(\hat{k} \times \hat{j}) = -a_3\hat{i} + a_1\hat{k}$, so $a_3 = 3$ (consistent) and $a_1 = 2$. Hence $\vec{a} = 2\hat{i} - \hat{j} + 3\hat{k}$ and $\vec{a}\cdot(\hat{i} + \hat{j} + \hat{k}) = 2 - 1 + 3 = 4$.",
  r"Sign slips in the cyclic products $\hat{j} \times \hat{i} = -\hat{k}$, $\hat{k} \times \hat{j} = -\hat{i}$, or reversing the order of the cross product.",
  "U12-C-recover-from-unit-cross", "Two cross products with unit vectors, careful sign bookkeeping and a consistency check on the shared component.",
  check=_c027, values=[4, -4, 6, 0], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $\vec{a}$ is a vector such that $\vec{a} \times \hat{i} = 3\hat{j} + \hat{k}$ and $\vec{a} \times \hat{j} = -3\hat{i} + 2\hat{k}$, then the value of $\vec{a}\cdot(\hat{i} + \hat{j} + \hat{k})$ is", answer=4))


def _c028():
    A, B, D = 3, 5, 7
    ab = Rational(A ** 2 + B ** 2 - D ** 2, 2)
    return sqrt(A ** 2 * B ** 2 - ab ** 2)


q("U12-C-028", TOPIC, "Cross product from lengths", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 3$, $|\vec{b}| = 5$ and $|\vec{a} - \vec{b}| = 7$, then the area of the parallelogram with adjacent sides $\vec{a}$ and $\vec{b}$ is",
  r"$\frac{15\sqrt{3}}{2}$",
  [(r"$\frac{15\sqrt{3}}{4}$", r"Uses the triangle factor $\frac{1}{2}$, giving the area of the triangle on $\vec{a}$ and $\vec{b}$."),
   (r"$\frac{15}{2}$", r"Reports $|\vec{a}\cdot\vec{b}| = \frac{15}{2}$, using $\cos\theta$ in place of $\sin\theta$."),
   (r"$15$", r"Takes the area as $|\vec{a}||\vec{b}|$, as though $\vec{a} \perp \vec{b}$.")],
  r"$49 = 9 + 25 - 2\vec{a}\cdot\vec{b}$ gives $\vec{a}\cdot\vec{b} = -\frac{15}{2}$. Then $|\vec{a} \times \vec{b}|^2 = 225 - \frac{225}{4} = \frac{675}{4}$, so the area is $\frac{15\sqrt{3}}{2}$.",
  r"Using $\cos\theta$ for the area or forgetting to find $\vec{a}\cdot\vec{b}$ first.",
  "U12-C-cross-from-lengths", "Dot product from a length, then the Lagrange identity.",
  check=_c028, values=[15 * sqrt(3) / 2, 15 * sqrt(3) / 4, Rational(15, 2), 15], cognitive="Application", source_class=SC)


def _c029():
    x, y, z = symbols('x y z')
    a, c = V(1, 1, 1), V(0, 1, -1)
    b = V(x, y, z)
    s = solve(list(cr(a, b) - c) + [a.dot(b) - 3], [x, y, z], dict=True)[0]
    return b.subs(s)


q("U12-C-029", TOPIC, "Vector from its cross and dot products", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = \hat{i} + \hat{j} + \hat{k}$ and $\vec{c} = \hat{j} - \hat{k}$. If $\vec{b}$ is a vector such that $\vec{a} \times \vec{b} = \vec{c}$ and $\vec{a}\cdot\vec{b} = 3$, then $\vec{b}$ equals",
  r"$\frac{1}{3}(5\hat{i} + 2\hat{j} + 2\hat{k})$",
  [(r"$\frac{1}{3}(\hat{i} + 4\hat{j} + 4\hat{k})$", r"Solves $\vec{a} \times \vec{b} = -\vec{c}$ by a sign slip, giving $x - z = -1$ and $z = y$, so $3y - 1 = 3$."),
   (r"$5\hat{i} + 2\hat{j} + 2\hat{k}$", r"Gets the right direction but forgets to divide by $|\vec{a}|^2 = 3$."),
   (r"$\hat{i} + \hat{j} + \hat{k}$", r"Takes $\vec{b} = \vec{a}$ because $\vec{a}\cdot\vec{a} = 3$, ignoring that then $\vec{a} \times \vec{b} = \vec{0}$.")],
  r"Let $\vec{b} = x\hat{i} + y\hat{j} + z\hat{k}$. Then $\vec{a} \times \vec{b} = (z - y)\hat{i} + (x - z)\hat{j} + (y - x)\hat{k} = \hat{j} - \hat{k}$, so $z = y$ and $x = y + 1$. With $x + y + z = 3$: $3y + 1 = 3$, $y = \frac{2}{3}$, so $\vec{b} = \frac{5}{3}\hat{i} + \frac{2}{3}\hat{j} + \frac{2}{3}\hat{k}$.",
  r"Sign errors when equating components of $\vec{a} \times \vec{b}$.",
  "U12-C-solve-cross-dot-eq", "Component equations from a cross product plus a dot condition.",
  check=_c029, values=[V(5, 2, 2) / 3, V(1, 4, 4) / 3, V(5, 2, 2), V(1, 1, 1)], cognitive="Application", source_class=SC)


def _c030():
    th = pi / 6
    s = Abs(sin(th))  # |b x c| for unit b, c
    lam = symbols('lam', real=True)
    return FiniteSet(*solve(Eq(lam ** 2 * s ** 2, 1), lam))


q("U12-C-030", TOPIC, "Vector perpendicular to two unit vectors", "Medium", "Multi-step computation MCQ",
  r"Let $\hat{a}, \hat{b}, \hat{c}$ be unit vectors such that $\hat{a}\cdot\hat{b} = \hat{a}\cdot\hat{c} = 0$ and the angle between $\hat{b}$ and $\hat{c}$ is $\frac{\pi}{6}$. If $\hat{a} = \lambda(\hat{b} \times \hat{c})$, then $\lambda$ equals",
  r"$\pm 2$",
  [(r"$\pm \frac{1}{2}$", r"Sets $\lambda = \pm|\hat{b} \times \hat{c}|$ instead of its reciprocal."),
   (r"$\pm 1$", r"Assumes $\hat{b} \times \hat{c}$ is already a unit vector because $\hat{b}$ and $\hat{c}$ are."),
   (r"$\pm \frac{2}{\sqrt{3}}$", r"Uses $|\hat{b} \times \hat{c}| = \cos\frac{\pi}{6}$ instead of $\sin\frac{\pi}{6}$.")],
  r"$\hat{a}$ is perpendicular to both $\hat{b}$ and $\hat{c}$, so it is parallel to $\hat{b} \times \hat{c}$, whose magnitude is $\sin\frac{\pi}{6} = \frac{1}{2}$. Since $|\hat{a}| = 1$, $|\lambda| \cdot \frac{1}{2} = 1$, so $\lambda = \pm 2$.",
  r"Assuming the cross product of two unit vectors is a unit vector.",
  "U12-C-perp-to-two-unit", "Direction from perpendicularity, magnitude from the angle.",
  check=_c030, values=[FiniteSet(2, -2), FiniteSet(Rational(1, 2), Rational(-1, 2)), FiniteSet(1, -1), FiniteSet(2 / sqrt(3), -2 / sqrt(3))], cognitive="Application", source_class=SC)


def _c031():
    x, y, z = symbols('x y z')
    a, b = V(1, 2, -1), V(-3, 2, 1)
    c = V(x, y, z)
    s = solve(list(cr(a, c) + b) + [a.dot(c) - 8], [x, y, z], dict=True)[0]
    cc = c.subs(s)
    return cc.dot(cc)


q("U12-C-031", TOPIC, "Vector from its cross and dot products", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = \hat{i} + 2\hat{j} - \hat{k}$ and $\vec{b} = -3\hat{i} + 2\hat{j} + \hat{k}$. If $\vec{c}$ is a vector such that $\vec{a} \times \vec{c} + \vec{b} = \vec{0}$ and $\vec{a}\cdot\vec{c} = 8$, then $|\vec{c}|^2$ equals",
  r"$13$",
  [(r"$3$", r"Stops at the particular solution $\hat{i} + \hat{j} + \hat{k}$ of $\vec{a} \times \vec{c} = -\vec{b}$, for which $\vec{a}\cdot\vec{c} = 2$, ignoring the condition $\vec{a}\cdot\vec{c} = 8$."),
   (r"$\frac{32}{3}$", r"Assumes $\vec{c}$ is parallel to $\vec{a}$, so $\vec{c} = \frac{8}{6}\vec{a}$ and $|\vec{c}|^2 = \frac{16}{9} \cdot 6$."),
   (r"$9$", r"Finds $\vec{c} = (\hat{i} + \hat{j} + \hat{k}) + \vec{a}$ but expands $|\vec{c}|^2$ as $3 + 6$, omitting the cross term $2(\hat{i} + \hat{j} + \hat{k})\cdot\vec{a} = 4$.")],
  r"With $\vec{c} = x\hat{i} + y\hat{j} + z\hat{k}$, $\vec{a} \times \vec{c} = (2z + y)\hat{i} - (z + x)\hat{j} + (y - 2x)\hat{k} = 3\hat{i} - 2\hat{j} - \hat{k}$. One solution is $\hat{i} + \hat{j} + \hat{k}$, so in general $\vec{c} = (\hat{i} + \hat{j} + \hat{k}) + t\vec{a}$. Then $\vec{a}\cdot\vec{c} = 2 + 6t = 8$ gives $t = 1$, $\vec{c} = 2\hat{i} + 3\hat{j}$ and $|\vec{c}|^2 = 13$.",
  r"Forgetting that $\vec{a} \times \vec{c} = \vec{d}$ determines $\vec{c}$ only up to a multiple of $\vec{a}$.",
  "U12-C-solve-cross-dot-eq", "General solution of a cross equation, then a dot condition.",
  check=_c031, values=[13, 3, Rational(32, 3), 9], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $\vec{a} = \hat{i} + 2\hat{j} - \hat{k}$ and $\vec{b} = -3\hat{i} + 2\hat{j} + \hat{k}$. If $\vec{c}$ is a vector such that $\vec{a} \times \vec{c} + \vec{b} = \vec{0}$ and $\vec{a}\cdot\vec{c} = 8$, then the value of $|\vec{c}|^2$ is", answer=13))


def _c032():
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4')
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    c = -a - b
    s = cr(a, b) + cr(b, c) + cr(c, a)
    return simplify(expand(s)[0] / cr(a, b)[0])  # multiple of a x b


q("U12-C-032", TOPIC, "Cyclic cross products", "Medium", "Conceptual/application MCQ",
  r"If $\vec{a} + \vec{b} + \vec{c} = \vec{0}$, then $\vec{a} \times \vec{b} + \vec{b} \times \vec{c} + \vec{c} \times \vec{a}$ equals",
  r"$3(\vec{a} \times \vec{b})$",
  [(r"$\vec{0}$", r"Assumes the cyclic terms cancel because $\vec{a} + \vec{b} + \vec{c} = \vec{0}$."),
   (r"$\vec{a} \times \vec{b}$", r"Shows that each term equals $\vec{a} \times \vec{b}$ but then reports a single term instead of the sum."),
   (r"$-3(\vec{a} \times \vec{b})$", r"Shows that the three terms are equal but writes each one as $\vec{b} \times \vec{a}$ (reversing the order), reporting $3(\vec{b} \times \vec{a}) = -3(\vec{a} \times \vec{b})$.")],
  r"Substituting $\vec{c} = -\vec{a} - \vec{b}$: $\vec{b} \times \vec{c} = -\vec{b} \times \vec{a} = \vec{a} \times \vec{b}$ and $\vec{c} \times \vec{a} = -\vec{b} \times \vec{a} = \vec{a} \times \vec{b}$. The sum is $3(\vec{a} \times \vec{b})$.",
  r"Assuming cyclic sums of cross products vanish.",
  "U12-C-cyclic-cross", "Substitution and two applications of anticommutativity.",
  check=_c032, values=[3, 0, 1, -3], cognitive="Understanding", source_class=SC)


def _c033():
    P, Q, R = V(2, -1, 1), V(4, 1, 0), V(1, 1, 3)
    L, Mq, N = (P + Q) / 2, (Q + R) / 2, (R + P) / 2
    return nm(cr(Mq - L, N - L)) / 2


q("U12-C-033", TOPIC, "Area of the medial triangle", "Medium", "Multi-step computation MCQ",
  r"The area of the triangle formed by joining the midpoints of the sides of the triangle with vertices $P(2, -1, 1)$, $Q(4, 1, 0)$ and $R(1, 1, 3)$ is",
  r"$\frac{9}{8}$",
  [(r"$\frac{9}{2}$", r"Gives the area of triangle $PQR$ itself."),
   (r"$\frac{9}{4}$", r"Assumes the midpoint triangle has half the area of $PQR$."),
   (r"$\frac{27}{8}$", r"Computes the remaining region, $\frac{3}{4}$ of the area of $PQR$, instead of the inner triangle.")],
  r"$\overrightarrow{PQ} = 2\hat{i} + 2\hat{j} - \hat{k}$, $\overrightarrow{PR} = -\hat{i} + 2\hat{j} + 2\hat{k}$, and $\overrightarrow{PQ} \times \overrightarrow{PR} = 6\hat{i} - 3\hat{j} + 6\hat{k}$, of magnitude $9$. So triangle $PQR$ has area $\frac{9}{2}$. The sides of the midpoint triangle are half the sides of $PQR$, so its area is $\frac{1}{4} \cdot \frac{9}{2} = \frac{9}{8}$.",
  r"Using a ratio of $\frac{1}{2}$ instead of $\frac{1}{4}$ for the medial triangle.",
  "U12-C-midpoint-triangle-area", "Triangle area by cross product, then a scaling idea.",
  check=_c033, values=[Rational(9, 8), Rational(9, 2), Rational(9, 4), Rational(27, 8)], cognitive="Application", source_class=SC)


def _c034():
    P, Q, R = V(1, 1, 1), V(-1, 2, -1), V(-1, 3, 1)
    return nm(cr(Q - P, R - P)) / nm(Q - P)


q("U12-C-034", TOPIC, "Altitude of a triangle via area", "Medium", "Multi-step computation MCQ",
  r"In the triangle with vertices $P(1, 1, 1)$, $Q(-1, 2, -1)$ and $R(-1, 3, 1)$, the length of the perpendicular from $R$ to the side $PQ$ is",
  r"$2$",
  [(r"$1$", r"Divides the triangle area $\frac{1}{2}|\overrightarrow{PQ} \times \overrightarrow{PR}| = 3$ by $|PQ| = 3$, forgetting the factor $2$ in $h = \frac{2 \cdot \text{area}}{\text{base}}$."),
   (r"$2\sqrt{2}$", r"Takes the side $|PR| = 2\sqrt{2}$ as the altitude."),
   (r"$4$", r"Uses $h = \frac{2|\overrightarrow{PQ} \times \overrightarrow{PR}|}{|PQ|}$, doubling the parallelogram area.")],
  r"$\overrightarrow{PQ} = -2\hat{i} + \hat{j} - 2\hat{k}$, $\overrightarrow{PR} = -2\hat{i} + 2\hat{j}$, and $\overrightarrow{PQ} \times \overrightarrow{PR} = 4\hat{i} + 4\hat{j} - 2\hat{k}$, of magnitude $6$. The required length is $\frac{|\overrightarrow{PQ} \times \overrightarrow{PR}|}{|\overrightarrow{PQ}|} = \frac{6}{3} = 2$.",
  r"Mixing the triangle area and the parallelogram area when finding a height.",
  "U12-C-altitude-via-area", "Cross product for area, then height from area and base.",
  check=_c034, values=[2, 1, 2 * sqrt(2), 4], cognitive="Application", source_class=SC,
  numerical=dict(question=r"In the triangle with vertices $P(1, 1, 1)$, $Q(-1, 2, -1)$ and $R(-1, 3, 1)$, the length of the perpendicular from $R$ to the side $PQ$ is", answer=2))


def _c035():
    a, b = V(2, -1, 2), V(1, 2, 2)
    c = cr(a, b)
    return nm(c) / a.dot(b)


q("U12-C-035", TOPIC, "Angle from cross and dot products", "Medium", "Multi-step computation MCQ",
  r"If $\theta$ is the angle between $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + 2\hat{j} + 2\hat{k}$, then $\tan\theta$ equals",
  r"$\frac{\sqrt{65}}{4}$",
  [(r"$\frac{4\sqrt{65}}{65}$", r"Inverts the ratio, computing $\frac{\vec{a}\cdot\vec{b}}{|\vec{a} \times \vec{b}|} = \cot\theta$."),
   (r"$\frac{\sqrt{65}}{9}$", r"Stops at $\sin\theta = \frac{|\vec{a} \times \vec{b}|}{|\vec{a}||\vec{b}|}$."),
   (r"$\frac{9}{4}$", r"Uses $|\vec{a}||\vec{b}| = 9$ in place of $|\vec{a} \times \vec{b}|$ in the numerator.")],
  r"$\vec{a} \times \vec{b} = (-2 - 4)\hat{i} - (4 - 2)\hat{j} + (4 + 1)\hat{k} = -6\hat{i} - 2\hat{j} + 5\hat{k}$, so $|\vec{a} \times \vec{b}| = \sqrt{65}$; and $\vec{a}\cdot\vec{b} = 2 - 2 + 4 = 4 > 0$. Hence $\tan\theta = \frac{\sqrt{65}}{4}$.",
  r"Using $|\vec{a}||\vec{b}|$ where $|\vec{a} \times \vec{b}|$ is needed.",
  "U12-C-angle-from-cross-dot", "Both products computed and combined.",
  check=_c035, values=[sqrt(65) / 4, 4 * sqrt(65) / 65, sqrt(65) / 9, Rational(9, 4)], cognitive="Application", source_class=SC)


def _c036():
    x, y, z = symbols('x y z')
    a, b = V(1, 2, -1), V(2, -1, 3)
    r = V(x, y, z)
    s = solve(list(cr(r, a) - cr(b, a)) + list(cr(r, b) - cr(a, b)), [x, y, z], dict=True)[0]
    return r.subs(s)


q("U12-C-036", TOPIC, "System of cross product equations", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = \hat{i} + 2\hat{j} - \hat{k}$ and $\vec{b} = 2\hat{i} - \hat{j} + 3\hat{k}$. If $\vec{r} \times \vec{a} = \vec{b} \times \vec{a}$ and $\vec{r} \times \vec{b} = \vec{a} \times \vec{b}$, then $\vec{r}$ equals",
  r"$3\hat{i} + \hat{j} + 2\hat{k}$",
  [(r"$\hat{i} - 3\hat{j} + 4\hat{k}$", r"Reads the second equation as $(\vec{r} + \vec{a}) \times \vec{b} = \vec{0}$, a sign slip, and combines with $\vec{r} = \vec{b} + \lambda\vec{a}$ to get $\vec{b} - \vec{a}$."),
   (r"$-\hat{i} + 3\hat{j} - 4\hat{k}$", r"Reads the first equation as $(\vec{r} + \vec{b}) \times \vec{a} = \vec{0}$ and combines with $\vec{r} = \vec{a} + \mu\vec{b}$ to get $\vec{a} - \vec{b}$."),
   (r"$\frac{3}{2}\hat{i} + \frac{1}{2}\hat{j} + \hat{k}$", r"Cancels the cross products to get $\vec{r} = \vec{b}$ and $\vec{r} = \vec{a}$, then averages the two.")],
  r"$(\vec{r} - \vec{b}) \times \vec{a} = \vec{0}$ gives $\vec{r} = \vec{b} + \lambda\vec{a}$; $(\vec{r} - \vec{a}) \times \vec{b} = \vec{0}$ gives $\vec{r} = \vec{a} + \mu\vec{b}$. Since $\vec{a}$, $\vec{b}$ are not parallel, comparing gives $\lambda = \mu = 1$, so $\vec{r} = \vec{a} + \vec{b} = 3\hat{i} + \hat{j} + 2\hat{k}$.",
  r"Cancelling vectors across a cross product.",
  "U12-C-r-cross-system", r"Two parallel conditions combined using independence of $\vec{a}$, $\vec{b}$.",
  check=_c036, values=[V(3, 1, 2), V(1, -3, 4), V(-1, 3, -4), V(Rational(3, 2), Rational(1, 2), 1)], cognitive="Analysis", source_class=SC)


def _c037():
    l = symbols('l', real=True)
    a, b = V(1, 0, 1), V(l, 1, 1)
    c = cr(a, b)
    sols = [s for s in solve(Eq(c.dot(c), a.dot(b) ** 2), l) if a.dot(b).subs(l, s) > 0]
    return sols[0]


q("U12-C-037", TOPIC, "Parameter from a cross and dot condition", "Medium", "Inverse/parameter MCQ",
  r"For $\vec{a} = \hat{i} + \hat{k}$ and $\vec{b} = \lambda\hat{i} + \hat{j} + \hat{k}$, it is given that $|\vec{a} \times \vec{b}| = \vec{a}\cdot\vec{b}$. Then $\lambda$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{4}$", r"Drops the $\hat{i}$ component $-1$ of $\vec{a} \times \vec{b}$, solving $1 + (\lambda - 1)^2 = (\lambda + 1)^2$."),
   (r"$\frac{3}{2}$", r"Writes $\vec{a}\cdot\vec{b} = \lambda$, forgetting the $\hat{k}$ terms, and solves $2 + (\lambda - 1)^2 = \lambda^2$."),
   (r"$2$", r"Forgets to square the dot product: $2 + (\lambda - 1)^2 = \lambda + 1$, whose roots are $1$ and $2$, and keeps $2$.")],
  r"$\vec{a} \times \vec{b} = (0 - 1)\hat{i} - (1 - \lambda)\hat{j} + (1 - 0)\hat{k} = -\hat{i} + (\lambda - 1)\hat{j} + \hat{k}$ and $\vec{a}\cdot\vec{b} = \lambda + 1$. Squaring, $2 + (\lambda - 1)^2 = (\lambda + 1)^2$, so $3 - 2\lambda = 2\lambda + 1$ and $\lambda = \frac{1}{2}$; then $\vec{a}\cdot\vec{b} = \frac{3}{2} > 0$, as required.",
  r"Dropping a component of the cross product when squaring.",
  "U12-C-angle-param-cross", "Cross and dot products in a parameter, then an equation.",
  check=_c037, values=[Rational(1, 2), Rational(1, 4), Rational(3, 2), 2], cognitive="Application", source_class=SC)


def _c038():
    a, b = V(3, 0, 4), V(1, 1, 1)
    s1 = simplify(nm(cr(a, b)) ** 2 + a.dot(b) ** 2 - 75) == 0
    d1, d2, d3 = symbols('d1:4')
    d = V(d1, d2, d3)
    sol = solve(list(cr(V(2, -1, 5), d)) + [V(2, -1, 5).dot(d)], [d1, d2, d3], dict=True)
    s2 = len(sol) == 1 and all(v == 0 for v in sol[0].values())
    return (bool(s1), bool(s2))


q("U12-C-038", TOPIC, "Lagrange identity and zero products", "Medium", "Statement-based MCQ",
  r"Statement I: If $\vec{a} = 3\hat{i} + 4\hat{k}$ and $\vec{b} = \hat{i} + \hat{j} + \hat{k}$, then $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = 75$. Statement II: If $\vec{a} \times \vec{b} = \vec{0}$ and $\vec{a}\cdot\vec{b} = 0$, then $\vec{a} = \vec{0}$ or $\vec{b} = \vec{0}$." + TAIL,
  ST_TT,
  [(ST_FF, r"Computes $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2$ as $|\vec{a}|^2 + |\vec{b}|^2 = 28$ and also believes non-zero vectors can be both parallel and perpendicular."),
   (ST_TF, r"Accepts the identity but thinks non-zero vectors can have both products zero."),
   (ST_FT, r"Evaluates $|\vec{a}|^2|\vec{b}|^2$ as $5 \cdot 3$ (using $|\vec{a}|$ instead of $|\vec{a}|^2$) and so rejects Statement I.")],
  r"By the identity $|\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = |\vec{a}|^2|\vec{b}|^2 = 25 \cdot 3 = 75$, Statement I is true. For Statement II, $|\vec{a}|^2|\vec{b}|^2 = |\vec{a} \times \vec{b}|^2 + (\vec{a}\cdot\vec{b})^2 = 0$, so one of the vectors is zero; Statement II is true.",
  r"Thinking a non-zero pair can be both parallel and perpendicular.",
  "U12-C-lagrange-statement", "Evaluate the identity and apply it to a zero case.",
  check=_c038, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Understanding", source_class=SC)


def _c039():
    a, b, c = V(2, -1, 1), V(1, 1, -2), V(1, -1, 2)
    n = cr(a, b)
    lam = solve(Eq(symbols('t') * n.dot(c), 6), symbols('t'))[0]
    return lam * n


q("U12-C-039", TOPIC, "Vector perpendicular to two vectors with a dot condition", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} - \hat{j} + \hat{k}$, $\vec{b} = \hat{i} + \hat{j} - 2\hat{k}$ and $\vec{c} = \hat{i} - \hat{j} + 2\hat{k}$. If $\vec{d}$ is perpendicular to both $\vec{a}$ and $\vec{b}$, and $\vec{d}\cdot\vec{c} = 6$, then $\vec{d}$ equals",
  r"$3\hat{i} + 15\hat{j} + 9\hat{k}$",
  [(r"$-3\hat{i} - 15\hat{j} - 9\hat{k}$", r"Uses $\vec{b} \times \vec{a} = -\hat{i} - 5\hat{j} - 3\hat{k}$ as the direction but still takes the multiplier $3$, so $\vec{d}\cdot\vec{c} = -6$."),
   (r"$\hat{i} + 5\hat{j} + 3\hat{k}$", r"Stops at $\vec{a} \times \vec{b}$, which gives $\vec{d}\cdot\vec{c} = 2$, not $6$."),
   (r"$6\hat{i} + 30\hat{j} + 18\hat{k}$", r"Takes the multiplier as $6$ itself, forgetting to divide by $(\vec{a} \times \vec{b})\cdot\vec{c} = 2$.")],
  r"$\vec{a} \times \vec{b} = (2 - 1)\hat{i} - (-4 - 1)\hat{j} + (2 + 1)\hat{k} = \hat{i} + 5\hat{j} + 3\hat{k}$, so $\vec{d} = \lambda(\hat{i} + 5\hat{j} + 3\hat{k})$. Then $\vec{d}\cdot\vec{c} = \lambda(1 - 5 + 6) = 2\lambda = 6$, so $\lambda = 3$ and $\vec{d} = 3\hat{i} + 15\hat{j} + 9\hat{k}$.",
  r"Not using the extra condition to fix the scalar multiple.",
  "U12-C-perp-vector-condition", "Direction from a cross product, multiplier from a dot condition.",
  check=_c039, values=[V(3, 15, 9), V(-3, -15, -9), V(1, 5, 3), V(6, 30, 18)], cognitive="Application", source_class=SC)


def _c040():
    a, b = V(2, -3, 2), V(2, 1, -2)
    u = 9 * unit(cr(a, b))
    return u if u[1] < 0 else -u


q("U12-C-040", TOPIC, "Perpendicular vector with an orientation condition", "Medium", "Multi-step computation MCQ",
  r"A vector $\vec{v}$ of magnitude $9$ is perpendicular to both $2\hat{i} - 3\hat{j} + 2\hat{k}$ and $2\hat{i} + \hat{j} - 2\hat{k}$, and makes an obtuse angle with the positive $y$-axis. Then $\vec{v}$ equals",
  r"$-3\hat{i} - 6\hat{j} - 6\hat{k}$",
  [(r"$3\hat{i} - 6\hat{j} + 6\hat{k}$", r"Omits the minus sign in front of the $\hat{j}$ minor, getting a cross product parallel to $\hat{i} - 2\hat{j} + 2\hat{k}$, then chooses the sign with negative $\hat{j}$ component."),
   (r"$3\hat{i} - 6\hat{j} - 6\hat{k}$", r"Reverses the order in the $\hat{i}$ minor, getting a cross product parallel to $-\hat{i} + 2\hat{j} + 2\hat{k}$, then chooses the sign with negative $\hat{j}$ component."),
   (r"$-6\hat{i} - 3\hat{j} - 6\hat{k}$", r"Interchanges the $\hat{i}$ and $\hat{j}$ components of the cross product, writing it as $8\hat{i} + 4\hat{j} + 8\hat{k}$.")],
  r"The cross product is $(6 - 2)\hat{i} - (-4 - 4)\hat{j} + (2 + 6)\hat{k} = 4\hat{i} + 8\hat{j} + 8\hat{k} = 4(\hat{i} + 2\hat{j} + 2\hat{k})$, so $\vec{v} = \pm 3(\hat{i} + 2\hat{j} + 2\hat{k})$. An obtuse angle with the positive $y$-axis needs a negative $\hat{j}$ component, so $\vec{v} = -3\hat{i} - 6\hat{j} - 6\hat{k}$.",
  r"Ignoring the orientation condition or slipping a sign in the cross product.",
  "U12-C-unit-perp", "Cross product, scaling, and a sign choice from a condition.",
  check=_c040, values=[V(-3, -6, -6), V(3, -6, 6), V(3, -6, -6), V(-6, -3, -6)], cognitive="Application", source_class=SC)

# ================================================================ DIFFICULT (13)


def _c041():
    p, qv = V(3, 1, 1), V(1, 1, 0)
    w = cr(p, qv)
    s = symbols('s', nonnegative=True)
    # |p - r|^2 = |p|^2 + s^2 - 2 p.r with p.r = 2|r| = 2s, and |p - r| = sqrt(7)
    rs = solve(Eq(p.dot(p) + s ** 2 - 4 * s, 7), s)
    assert len(rs) == 1
    rr = rs[0]
    area = 3 * sqrt(2)
    wr2 = w.dot(w) * rr ** 2 - area ** 2  # Lagrange identity
    # confirm such r exists: components along p-hat and w-hat fit inside |r|
    assert (2 * rr) ** 2 / p.dot(p) + wr2 / w.dot(w) <= rr ** 2
    return sqrt(wr2)


q("U12-C-041", TOPIC, "Dot product from an area with conditions", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{p} = 3\hat{i} + \hat{j} + \hat{k}$, $\vec{q} = \hat{i} + \hat{j}$ and $\vec{w} = \vec{p} \times \vec{q}$. A vector $\vec{r}$ satisfies $\vec{p}\cdot\vec{r} = 2|\vec{r}|$ and $|\vec{p} - \vec{r}| = \sqrt{7}$, and the parallelogram with adjacent sides $\vec{w}$ and $\vec{r}$ has area $3\sqrt{2}$. Then $|\vec{w}\cdot\vec{r}|$ equals",
  r"$\sqrt{6}$",
  [(r"$\sqrt{42}$", r"Sign slip in the Lagrange identity: $(\vec{w}\cdot\vec{r})^2 = |\vec{w}|^2|\vec{r}|^2 + |\vec{w} \times \vec{r}|^2 = 24 + 18 = 42$."),
   (r"$\sqrt{26}$", r"Uses $|\vec{p}|^2 = 11$ in place of $|\vec{w}|^2$ in the Lagrange identity: $11 \cdot 4 - 18 = 26$."),
   (r"$2\sqrt{6}$", r"Takes $|\vec{r}| = |\vec{p} - \vec{r}| = \sqrt{7}$ instead of solving for $|\vec{r}|$: $6 \cdot 7 - 18 = 24$.")],
  r"$|\vec{p}|^2 = 11$, so $|\vec{p} - \vec{r}|^2 = 11 + |\vec{r}|^2 - 2\vec{p}\cdot\vec{r} = |\vec{r}|^2 - 4|\vec{r}| + 11 = 7$, that is $(|\vec{r}| - 2)^2 = 0$ and $|\vec{r}| = 2$. Next $\vec{w} = \vec{p} \times \vec{q} = -\hat{i} + \hat{j} + 2\hat{k}$, so $|\vec{w}|^2 = 6$. The area condition gives $|\vec{w} \times \vec{r}| = 3\sqrt{2}$, and by the Lagrange identity $(\vec{w}\cdot\vec{r})^2 = |\vec{w}|^2|\vec{r}|^2 - |\vec{w} \times \vec{r}|^2 = 24 - 18 = 6$. Hence $|\vec{w}\cdot\vec{r}| = \sqrt{6}$.",
  r"Not noticing that the length condition is a perfect square that fixes $|\vec{r}|$, and sign errors in the Lagrange identity.",
  "U12-C-cross-magnitude-multi", r"Three linked steps: a hidden perfect square for $|\vec{r}|$, a cross product, and the Lagrange identity used in reverse from an area.",
  check=_c041, values=[sqrt(6), sqrt(42), sqrt(26), 2 * sqrt(6)], cognitive="Analysis", source_class=SC)


def _c042():
    P, Q, R, S = V(1, 1, 1), V(3, 0, 0), V(2, 2, -1), V(0, 2, 1)
    return nm(cr(Q - P, R - P)) / 2 + nm(cr(R - P, S - P)) / 2


q("U12-C-042", TOPIC, "Area of a quadrilateral", "Difficult", "Multi-step computation MCQ",
  r"The points $P(1, 1, 1)$, $Q(3, 0, 0)$, $R(2, 2, -1)$ and $S(0, 2, 1)$ lie in a plane and, taken in this order, form a convex quadrilateral $PQRS$. The area of $PQRS$ is",
  r"$\frac{5\sqrt{3}}{2}$",
  [(r"$5\sqrt{3}$", r"Uses $|\overrightarrow{PR} \times \overrightarrow{QS}|$ without the factor $\frac{1}{2}$."),
   (r"$\frac{3\sqrt{3}}{2}$", r"Finds only the area of triangle $PQR$ and stops."),
   (r"$\sqrt{3}$", r"Treats $PQRS$ as a parallelogram on sides $\overrightarrow{PQ}$ and $\overrightarrow{PS}$, computing $|\overrightarrow{PQ} \times \overrightarrow{PS}|$.")],
  r"For a convex planar quadrilateral the area is $\frac{1}{2}|\overrightarrow{PR} \times \overrightarrow{QS}|$. Here $\overrightarrow{PR} = \hat{i} + \hat{j} - 2\hat{k}$ and $\overrightarrow{QS} = -3\hat{i} + 2\hat{j} + \hat{k}$, so $\overrightarrow{PR} \times \overrightarrow{QS} = 5\hat{i} + 5\hat{j} + 5\hat{k}$, of magnitude $5\sqrt{3}$. The area is $\frac{5\sqrt{3}}{2}$ (equivalently, triangles $PQR$ and $PRS$ have areas $\frac{3\sqrt{3}}{2}$ and $\sqrt{3}$).",
  r"Treating a general quadrilateral as a parallelogram.",
  "U12-C-quadrilateral-area", "Needs the diagonal formula or a split into two triangles.",
  check=_c042, values=[5 * sqrt(3) / 2, 5 * sqrt(3), 3 * sqrt(3) / 2, sqrt(3)], cognitive="Analysis", source_class=SC)


def _c043():
    x, y, z = symbols('x y z')
    a, b = V(2, 1, 2), V(-1, 4, -1)
    r = V(x, y, z)
    s = solve(list(cr(a, r) - b) + [a.dot(r) - 9], [x, y, z], dict=True)[0]
    return nm(r.subs(s))


q("U12-C-043", TOPIC, "Vector from its cross and dot products", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} + \hat{j} + 2\hat{k}$. If $\vec{r}$ satisfies $\vec{a} \times \vec{r} = -\hat{i} + 4\hat{j} - \hat{k}$ and $\vec{a}\cdot\vec{r} = 9$, then $|\vec{r}|$ equals",
  r"$\sqrt{11}$",
  [(r"$\sqrt{2}$", r"Finds the particular solution $\hat{i} - \hat{k}$ of the cross equation and ignores $\vec{a}\cdot\vec{r} = 9$."),
   (r"$\sqrt{3}$", r"Writes $\vec{r} = (\hat{i} - \hat{k}) + t\vec{a}$ with $t = 1$ but adds $t^2 = 1$ instead of $t^2|\vec{a}|^2 = 9$ to $|\hat{i} - \hat{k}|^2 = 2$."),
   (r"$\sqrt{83}$", r"Takes the component of $\vec{r}$ along $\vec{a}$ as $\vec{a}\cdot\vec{r} = 9$ itself instead of $\frac{9}{|\vec{a}|} = 3$, so $|\vec{r}|^2 = 2 + 81$.")],
  r"Let $\vec{r} = x\hat{i} + y\hat{j} + z\hat{k}$. Then $\vec{a} \times \vec{r} = (z - 2y)\hat{i} + (2x - 2z)\hat{j} + (2y - x)\hat{k}$, and one solution is $\hat{i} - \hat{k}$, which is perpendicular to $\vec{a}$. So $\vec{r} = \hat{i} - \hat{k} + t\vec{a}$ and $\vec{a}\cdot\vec{r} = 9t = 9$ gives $t = 1$, $\vec{r} = 3\hat{i} + \hat{j} + \hat{k}$ and $|\vec{r}| = \sqrt{11}$.",
  r"Ignoring the free multiple of $\vec{a}$ in the solution of $\vec{a} \times \vec{r} = \vec{b}$.",
  "U12-C-solve-cross-dot-eq", "General solution, a dot condition, and a magnitude with a Pythagorean split.",
  check=_c043, values=[sqrt(11), sqrt(2), sqrt(3), sqrt(83)], cognitive="Analysis", source_class=SC)


def _c044():
    l = symbols('l', real=True)
    a, b = V(2, l, 1), V(1, 2, -1)
    f = expand(cr(a, b).dot(cr(a, b)))
    lm = solve(diff(f, l), l)[0]
    return sqrt(f.subs(l, lm)) / 2


q("U12-C-044", TOPIC, "Least area of a triangle", "Difficult", "Multi-step computation MCQ",
  r"For real $\lambda$, two sides of a triangle are represented by $2\hat{i} + \lambda\hat{j} + \hat{k}$ and $\hat{i} + 2\hat{j} - \hat{k}$. The least possible area of the triangle is",
  r"$\frac{3\sqrt{3}}{2}$",
  [(r"$3\sqrt{3}$", r"Minimises $|\vec{a} \times \vec{b}|$ correctly but forgets the factor $\frac{1}{2}$."),
   (r"$\frac{\sqrt{29}}{2}$", r"Assumes the minimum occurs at $\lambda = 0$ and evaluates $\frac{1}{2}\sqrt{29}$."),
   (r"$\frac{\sqrt{35}}{2}$", r"Takes the vertex at $\lambda = -1$ (sign slip in $-\frac{b}{2a}$), giving $2 + 4 + 29 = 35$.")],
  r"$(2\hat{i} + \lambda\hat{j} + \hat{k}) \times (\hat{i} + 2\hat{j} - \hat{k}) = (-\lambda - 2)\hat{i} + 3\hat{j} + (4 - \lambda)\hat{k}$, so $|\vec{a} \times \vec{b}|^2 = 2\lambda^2 - 4\lambda + 29 = 2(\lambda - 1)^2 + 27$. The least value is $27$ at $\lambda = 1$, so the least area is $\frac{\sqrt{27}}{2} = \frac{3\sqrt{3}}{2}$.",
  r"Minimising at the wrong point of the quadratic.",
  "U12-C-area-extremum", "Cross product in a parameter, then completing the square.",
  check=_c044, values=[3 * sqrt(3) / 2, 3 * sqrt(3), sqrt(29) / 2, sqrt(35) / 2], cognitive="Analysis", source_class=SC)


def _c045():
    # Statement I: a x b = c, b x c = a (all nonzero) forces |b| = 1 but not |a| = |c| = 1
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4', real=True)
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    resid = expand(cr(b, cr(a, b)) - a - ((b.dot(b) - 1) * a - a.dot(b) * b))
    assert resid == zeros(3, 1)  # b x c - a = (|b|^2 - 1) a - (a.b) b
    A, B = V(0, 0, 2), V(0, 1, 0)
    C = cr(A, B)
    counter = (cr(B, C) == A) and C != zeros(3, 1) and A.dot(A) != 1
    s1 = not counter
    a = V(a1, a2, a3)
    E = [V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]
    tot = expand(sum(cr(a, e).dot(cr(a, e)) for e in E))
    s2 = simplify(tot - a.dot(a)) == 0
    return (bool(s1), bool(s2))


q("U12-C-045", TOPIC, "Cross product facts", "Difficult", "Statement-based MCQ",
  r"Statement I: If $\vec{a}, \vec{b}, \vec{c}$ are non-zero vectors such that $\vec{a} \times \vec{b} = \vec{c}$ and $\vec{b} \times \vec{c} = \vec{a}$, then $|\vec{a}| = |\vec{b}| = |\vec{c}| = 1$. Statement II: For every vector $\vec{a}$, $|\vec{a} \times \hat{i}|^2 + |\vec{a} \times \hat{j}|^2 + |\vec{a} \times \hat{k}|^2 = |\vec{a}|^2$." + TAIL,
  ST_FF,
  [(ST_TT, r"In Statement I derives $|\vec{b}| = 1$ and assumes by symmetry that $\vec{a}$ and $\vec{c}$ are unit vectors too; in Statement II treats $|\vec{a} \times \hat{i}|^2$ as $a_1^2$."),
   (ST_TF, r"Assumes by symmetry that all three are unit vectors in Statement I, but correctly finds the sum $2|\vec{a}|^2$ in Statement II."),
   (ST_FT, r"Sees that only $|\vec{b}| = 1$ is forced in Statement I, but treats $|\vec{a} \times \hat{i}|^2$ as $a_1^2$, so the sum appears to be $|\vec{a}|^2$.")],
  r"In Statement I, $\vec{c} = \vec{a} \times \vec{b}$ is perpendicular to $\vec{a}$ and $\vec{b}$, and $\vec{a} = \vec{b} \times \vec{c}$ is perpendicular to $\vec{b}$, so the three vectors are mutually perpendicular. Then $|\vec{c}| = |\vec{a}||\vec{b}|$ and $|\vec{a}| = |\vec{b}||\vec{c}| = |\vec{b}|^2|\vec{a}|$, so $|\vec{b}| = 1$ and $|\vec{c}| = |\vec{a}|$, but $|\vec{a}|$ is free: $\vec{a} = 2\hat{k}$, $\vec{b} = \hat{j}$, $\vec{c} = -2\hat{i}$ satisfies both equations. So Statement I is false. In Statement II, $|\vec{a} \times \hat{i}|^2 = a_2^2 + a_3^2$ and similarly, so the sum is $2|\vec{a}|^2$, which differs from $|\vec{a}|^2$ for $\vec{a} \ne \vec{0}$; false.",
  r"Reading symmetry into the system $\vec{a} \times \vec{b} = \vec{c}$, $\vec{b} \times \vec{c} = \vec{a}$, and losing the factor $2$ in the sum.",
  "U12-C-cross-facts-statement", r"Statement I needs perpendicularity and a magnitude chain to see only $|\vec{b}|$ is fixed; Statement II has a factor-2 trap.",
  check=_c045, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis", source_class=SC)


def _c046():
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4')
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    PQ, PR = b - a, (2 * a + 3 * b) - a
    k = simplify(expand(cr(PQ, PR))[0] / cr(a, b)[0])
    axb = 2 * 5  # area of triangle OPQ is 5
    return Abs(k) * axb / 2


q("U12-C-046", TOPIC, "Area with vertices given as combinations", "Difficult", "Multi-step computation MCQ",
  r"Points $P$ and $Q$ have position vectors $\vec{a}$ and $\vec{b}$ with respect to the origin $O$, and the area of triangle $OPQ$ is $5$. If $R$ has position vector $2\vec{a} + 3\vec{b}$, then the area of triangle $PQR$ is",
  r"$20$",
  [(r"$10$", r"Takes $\vec{b} \times \vec{a} = +\vec{a} \times \vec{b}$, so $\overrightarrow{PQ} \times \overrightarrow{PR}$ becomes $-2\,\vec{a} \times \vec{b}$."),
   (r"$40$", r"Forgets the factor $\frac{1}{2}$ in the area of triangle $PQR$."),
   (r"$25$", r"Uses $\overrightarrow{PR} = 2\vec{a} + 3\vec{b}$ without subtracting $\vec{a}$, giving $-5\,\vec{a} \times \vec{b}$.")],
  r"$|\vec{a} \times \vec{b}| = 2 \cdot 5 = 10$. Now $\overrightarrow{PQ} = \vec{b} - \vec{a}$ and $\overrightarrow{PR} = \vec{a} + 3\vec{b}$, so $\overrightarrow{PQ} \times \overrightarrow{PR} = \vec{b} \times \vec{a} - 3\,\vec{a} \times \vec{b} = -4\,\vec{a} \times \vec{b}$. The area is $\frac{1}{2} \cdot 4 \cdot 10 = 20$.",
  r"Forgetting to subtract the position vector of $P$ when forming a side.",
  "U12-C-area-combination", "Area to cross product, side vectors, expansion, back to area.",
  check=_c046, values=[20, 10, 40, 25], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Points $P$ and $Q$ have position vectors $\vec{a}$ and $\vec{b}$ with respect to the origin $O$, and the area of triangle $OPQ$ is $5$. If $R$ has position vector $2\vec{a} + 3\vec{b}$, then the area of triangle $PQR$ is", answer=20))


def _c047():
    # realise three unit vectors summing to zero
    a = V(1, 0, 0)
    b = V(-Rational(1, 2), sqrt(3) / 2, 0)
    c = -a - b
    assert simplify(nm(c) - 1) == 0
    return nm(cr(a, b) + cr(b, c) + cr(c, a))


q("U12-C-047", TOPIC, "Cyclic cross products", "Difficult", "Multi-step computation MCQ",
  r"If $\hat{a}$, $\hat{b}$, $\hat{c}$ are unit vectors such that $\hat{a} + \hat{b} + \hat{c} = \vec{0}$, then $|\hat{a} \times \hat{b} + \hat{b} \times \hat{c} + \hat{c} \times \hat{a}|$ equals",
  r"$\frac{3\sqrt{3}}{2}$",
  [(r"$0$", r"Assumes the cyclic sum vanishes because the vectors add to zero."),
   (r"$\frac{\sqrt{3}}{2}$", r"Finds each term equal to $\hat{a} \times \hat{b}$ but reports one term instead of three."),
   (r"$\frac{3}{2}$", r"Uses $|\cos\frac{2\pi}{3}| = \frac{1}{2}$ instead of $\sin\frac{2\pi}{3}$ for $|\hat{a} \times \hat{b}|$.")],
  r"With $\hat{c} = -\hat{a} - \hat{b}$, $\hat{b} \times \hat{c} = \hat{a} \times \hat{b}$ and $\hat{c} \times \hat{a} = \hat{a} \times \hat{b}$, so the sum is $3\,\hat{a} \times \hat{b}$. From $|\hat{a} + \hat{b}|^2 = |\hat{c}|^2 = 1$ we get $\hat{a}\cdot\hat{b} = -\frac{1}{2}$, so the angle is $\frac{2\pi}{3}$ and $|\hat{a} \times \hat{b}| = \frac{\sqrt{3}}{2}$. The answer is $\frac{3\sqrt{3}}{2}$.",
  r"Assuming cyclic cross product sums vanish.",
  "U12-C-cyclic-cross", "Combines cyclic reduction, a dot product step and the sine formula.",
  check=_c047, values=[3 * sqrt(3) / 2, 0, sqrt(3) / 2, Rational(3, 2)], cognitive="Analysis", source_class=SC)


def _c048():
    a1, a2, a3, b1, b2, b3 = symbols('a1:4 b1:4')
    a, b = V(a1, a2, a3), V(b1, b2, b3)
    k = simplify(expand(cr(3 * a - b, a + 3 * b))[0] / cr(a, b)[0])
    axb = 2 * 2 * sin(pi / 6)
    return Abs(k) * axb / 2


q("U12-C-048", TOPIC, "Area of a parallelogram from its diagonals", "Difficult", "Multi-step computation MCQ",
  r"Let $|\vec{a}| = |\vec{b}| = 2$, with the angle between $\vec{a}$ and $\vec{b}$ equal to $\frac{\pi}{6}$. The diagonals of a parallelogram are $3\vec{a} - \vec{b}$ and $\vec{a} + 3\vec{b}$. The area of the parallelogram is",
  r"$10$",
  [(r"$20$", r"Treats the diagonals as adjacent sides and reports $|\vec{d}_1 \times \vec{d}_2|$."),
   (r"$8$", r"Takes $\vec{b} \times \vec{a} = +\vec{a} \times \vec{b}$, so $\vec{d}_1 \times \vec{d}_2 = 8\,\vec{a} \times \vec{b}$."),
   (r"$10\sqrt{3}$", r"Uses $\cos\frac{\pi}{6}$ for $|\vec{a} \times \vec{b}|$, getting $2\sqrt{3}$.")],
  r"$(3\vec{a} - \vec{b}) \times (\vec{a} + 3\vec{b}) = 9\,\vec{a} \times \vec{b} - \vec{b} \times \vec{a} = 10\,\vec{a} \times \vec{b}$, and $|\vec{a} \times \vec{b}| = 2 \cdot 2 \cdot \sin\frac{\pi}{6} = 2$. The area is $\frac{1}{2}|\vec{d}_1 \times \vec{d}_2| = \frac{1}{2} \cdot 20 = 10$.",
  r"Using the side formula for diagonals.",
  "U12-C-area-diagonals", "Diagonal formula, bilinear expansion and the sine formula together.",
  check=_c048, values=[10, 20, 8, 10 * sqrt(3)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $|\vec{a}| = |\vec{b}| = 2$, with the angle between $\vec{a}$ and $\vec{b}$ equal to $\frac{\pi}{6}$. The diagonals of a parallelogram are $3\vec{a} - \vec{b}$ and $\vec{a} + 3\vec{b}$. The area of the parallelogram is", answer=10))


def _c049():
    P, Q, R = V(1, -1, 2), V(-2, -1, 3), V(4, 1, 0)
    A2 = nm(cr(Q - P, R - P))
    sides = [nm(Q - P), nm(R - P), nm(R - Q)]
    return Min(*[A2 / s for s in sides])


q("U12-C-049", TOPIC, "Altitude of a triangle via area", "Difficult", "Multi-step computation MCQ",
  r"For the triangle with vertices $P(1, -1, 2)$, $Q(-2, -1, 3)$ and $R(4, 1, 0)$, the length of the shortest altitude is",
  r"$1$",
  [(r"$\frac{7\sqrt{10}}{10}$", r"Takes the altitude on the shortest side $PQ = \sqrt{10}$, which is the longest altitude."),
   (r"$\frac{7\sqrt{17}}{17}$", r"Takes the altitude on the side $PR = \sqrt{17}$ without comparing all three sides."),
   (r"$\frac{1}{2}$", r"Divides the triangle area $\frac{7}{2}$ by the longest side $7$, forgetting the factor $2$.")],
  r"$\overrightarrow{PQ} = -3\hat{i} + \hat{k}$, $\overrightarrow{PR} = 3\hat{i} + 2\hat{j} - 2\hat{k}$, and $\overrightarrow{PQ} \times \overrightarrow{PR} = -2\hat{i} - 3\hat{j} - 6\hat{k}$, of magnitude $7$. The sides are $\sqrt{10}$, $\sqrt{17}$ and $QR = 7$. Each altitude equals $\frac{7}{\text{side}}$, so the shortest one is on the longest side: $\frac{7}{7} = 1$.",
  r"Not realising the shortest altitude falls on the longest side.",
  "U12-C-altitude-via-area", "Area by cross product, all three sides, and a comparison.",
  check=_c049, values=[1, 7 * sqrt(10) / 10, 7 * sqrt(17) / 17, Rational(1, 2)], cognitive="Analysis", source_class=SC)


def _c050():
    cnt = 0
    for l in range(-100, 101):
        c = cr(V(l, 1, 2), V(1, 2, -1))
        if c.dot(c) <= 275:  # (area)^2 <= (5 sqrt(11)/2)^2  <=>  |c|^2 <= 275
            cnt += 1
    return cnt


q("U12-C-050", TOPIC, "Integer parameters under an area bound", "Difficult", "Inverse/parameter MCQ",
  r"Two sides of a triangle are represented by $\lambda\hat{i} + \hat{j} + 2\hat{k}$ and $\hat{i} + 2\hat{j} - \hat{k}$. The number of integers $\lambda$ for which the area of the triangle does not exceed $\frac{5\sqrt{11}}{2}$ is",
  r"$15$",
  [(r"$13$", r"Uses a strict inequality $\lambda^2 < 49$, losing $\lambda = \pm 7$."),
   (r"$8$", r"Counts only $\lambda = 0, 1, \ldots, 7$, ignoring negative integers."),
   (r"$5$", r"Forgets the factor $\frac{1}{2}$, requiring $5\lambda^2 + 30 \le \frac{275}{4}$, so $|\lambda| \le 2$.")],
  r"The cross product is $-5\hat{i} + (\lambda + 2)\hat{j} + (2\lambda - 1)\hat{k}$, so $|\vec{a} \times \vec{b}|^2 = 25 + (\lambda + 2)^2 + (2\lambda - 1)^2 = 5\lambda^2 + 30$. The condition $\frac{1}{2}\sqrt{5\lambda^2 + 30} \le \frac{5\sqrt{11}}{2}$ gives $5\lambda^2 + 30 \le 275$, i.e. $\lambda^2 \le 49$. So $\lambda \in \{-7, \ldots, 7\}$: $15$ integers.",
  r"Dropping boundary or negative values when counting.",
  "U12-C-area-integer-count", "Cross product in a parameter, inequality, then careful counting.",
  check=_c050, values=[15, 13, 8, 5], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Two sides of a triangle are represented by $\lambda\hat{i} + \hat{j} + 2\hat{k}$ and $\hat{i} + 2\hat{j} - \hat{k}$. The number of integers $\lambda$ for which the area of the triangle does not exceed $\frac{5\sqrt{11}}{2}$ is", answer=15))


def _c051():
    x, y, z = symbols('x y z', real=True)
    a, b = V(1, 2, 2), V(2, 4, -5)
    r = V(x, y, z)
    sol = solve(list(cr(a, r) - b), [x, y, z], dict=True)[0]
    rr = r.subs(sol)
    free = list(rr.free_symbols)[0]
    f = expand(rr.dot(rr))
    t0 = solve(diff(f, free), free)[0]
    return sqrt(f.subs(free, t0))


q("U12-C-051", TOPIC, "Least magnitude solution of a cross equation", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{a} = \hat{i} + 2\hat{j} + 2\hat{k}$ and $\vec{b} = 2\hat{i} + 4\hat{j} - 5\hat{k}$. Among all vectors $\vec{r}$ satisfying $\vec{a} \times \vec{r} = \vec{b}$, the least possible value of $|\vec{r}|$ is",
  r"$\sqrt{5}$",
  [(r"$3\sqrt{5}$", r"Takes $|\vec{r}| = |\vec{b}|$, ignoring the factor $|\vec{a}|$."),
   (r"$\frac{\sqrt{5}}{3}$", r"Divides $|\vec{b}|$ by $|\vec{a}|^2 = 9$ instead of $|\vec{a}| = 3$."),
   (r"$5$", r"Gets $|\vec{r}|^2 = \frac{|\vec{b}|^2}{|\vec{a}|^2} = 5$ and forgets the square root.")],
  r"Here $\vec{a}\cdot\vec{b} = 2 + 8 - 10 = 0$, so solutions exist; they are $\vec{r} = \vec{r}_0 + t\vec{a}$, where $\vec{r}_0 = 2\hat{i} - \hat{j}$ is the solution perpendicular to $\vec{a}$ (check: $\vec{a} \times \vec{r}_0 = 2\hat{i} + 4\hat{j} - 5\hat{k}$). Then $|\vec{r}|^2 = |\vec{r}_0|^2 + 9t^2$ is least at $t = 0$, so the least value is $|\vec{r}_0| = \frac{|\vec{b}|}{|\vec{a}|} = \frac{\sqrt{45}}{3} = \sqrt{5}$.",
  r"Forgetting that $|\vec{a} \times \vec{r}| = |\vec{a}||\vec{r}|\sin\theta$ is at most $|\vec{a}||\vec{r}|$.",
  "U12-C-r-cross-min-norm", "Structure of the solution set plus a minimisation.",
  check=_c051, values=[sqrt(5), 3 * sqrt(5), sqrt(5) / 3, 5], cognitive="Analysis", source_class=SC)


def _c052():
    x, y, z = symbols('x y z', real=True)
    a, b = V(2, -1, 2), V(1, 4, 1)
    r = V(x, y, z)
    sol = solve(list(cr(a, r) - b), [x, y, z], dict=True)[0]
    rr = r.subs(sol)
    free = list(rr.free_symbols)[0]
    return len(solveset(Eq(expand(rr.dot(rr)), 1), free, S.Reals))


q("U12-C-052", TOPIC, "Counting solutions of a cross equation", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + 4\hat{j} + \hat{k}$. The number of vectors $\vec{r}$ with $|\vec{r}| = 1$ and $\vec{a} \times \vec{r} = \vec{b}$ is",
  r"$0$",
  [(r"$1$", r"Assumes the cross equation has exactly one solution, which can then be scaled to unit length."),
   (r"$2$", r"Writes $\vec{r} = \vec{r}_0 + t\vec{a}$ and expects the quadratic $|\vec{r}|^2 = 1$ to give two values of $t$ without checking its discriminant."),
   (r"infinitely many", r"Notes that $\vec{a} \times \vec{r} = \vec{b}$ has infinitely many solutions and overlooks the length condition.")],
  r"$\vec{a}\cdot\vec{b} = 2 - 4 + 2 = 0$, so solutions exist: $\vec{r} = \hat{i} - \hat{k} + t\vec{a}$, since $\vec{a} \times (\hat{i} - \hat{k}) = \hat{i} + 4\hat{j} + \hat{k}$ and $\hat{i} - \hat{k}$ is perpendicular to $\vec{a}$. Then $|\vec{r}|^2 = 2 + 9t^2 \ge 2 > 1$ for every $t$ (equivalently $|\vec{r}| \ge \frac{|\vec{b}|}{|\vec{a}|} = \sqrt{2}$). So no such $\vec{r}$ exists.",
  r"Not using $|\vec{b}| = |\vec{a}||\vec{r}|\sin\theta \le |\vec{a}||\vec{r}|$ as a lower bound on $|\vec{r}|$.",
  "U12-C-r-cross-min-norm", "Structure of the solution set plus a bound that rules out all solutions.",
  check=_c052, values=[0, 1, 2, 10**9]  # 10**9 encodes 'infinitely many'
, cognitive="Analysis", source_class=SC)


def _c053():
    t = symbols('t', real=True)
    PQ, PR = V(1, 2, 2), V(t, 1, 0)
    c = cr(PQ, PR)
    sols = solve(Eq(c.dot(c), 29), t)
    return sum(sols)


q("U12-C-053", TOPIC, "Parameter from a given area", "Difficult", "Inverse/parameter MCQ",
  r"The triangle with vertices $P(1, 1, 0)$, $Q(2, 3, 2)$ and $R(1 + t, 2, 0)$, $t \in \mathbb{R}$, has area $\frac{\sqrt{29}}{2}$. The sum of all possible values of $t$ is",
  r"$\frac{1}{2}$",
  [(r"$-\frac{1}{2}$", r"Sign slip in the $\hat{k}$ component, writing $1 + 2t$ instead of $1 - 2t$, which leads to $8t^2 + 4t - 24 = 0$."),
   (r"$2$", r"Keeps only the integer root $t = 2$ of $2t^2 - t - 6 = 0$."),
   (r"$-\frac{3}{2}$", r"Keeps only the root $t = -\frac{3}{2}$, discarding the other.")],
  r"$\overrightarrow{PQ} = \hat{i} + 2\hat{j} + 2\hat{k}$ and $\overrightarrow{PR} = t\hat{i} + \hat{j}$, so $\overrightarrow{PQ} \times \overrightarrow{PR} = -2\hat{i} + 2t\hat{j} + (1 - 2t)\hat{k}$ and $|\overrightarrow{PQ} \times \overrightarrow{PR}|^2 = 8t^2 - 4t + 5$. Area $\frac{\sqrt{29}}{2}$ means $8t^2 - 4t + 5 = 29$, i.e. $2t^2 - t - 6 = 0$, with roots $2$ and $-\frac{3}{2}$. Their sum is $\frac{1}{2}$.",
  r"Keeping only one root of the quadratic.",
  "U12-C-area-parameter", "Cross product with a parameter, a quadratic, and both roots.",
  check=_c053, values=[Rational(1, 2), Rational(-1, 2), 2, Rational(-3, 2)], cognitive="Analysis", source_class=SC)
