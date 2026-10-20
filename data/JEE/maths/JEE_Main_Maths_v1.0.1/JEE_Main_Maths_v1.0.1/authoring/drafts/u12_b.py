import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
SC = "XII"
TOPIC = "Scalar product of vectors"


def V(*c):
    return Matrix(c)


def dot(u, v):
    return expand((u.T * v)[0])


def mag(u):
    return sqrt(dot(u, u))


def ang(u, v):
    return acos(simplify(dot(u, v) / (mag(u) * mag(v))))


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."

t, lam, p, x, y, z, k = symbols('t lambda p x y z k', real=True)

# ================================================================ EASY (16)


def _c001():
    a, b = V(2, -1, 1), V(1, 1, 2)
    return ang(a, b)


q("U12-B-001", TOPIC, "Angle between two vectors from components", "Easy", "Single-step computation MCQ",
  r"The angle between the vectors $\vec{a} = 2\hat{i} - \hat{j} + \hat{k}$ and $\vec{b} = \hat{i} + \hat{j} + 2\hat{k}$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{\pi}{6}$", r"Gets $\frac{\vec a\cdot\vec b}{|\vec a||\vec b|} = \frac{1}{2}$ correctly but reads it as $\sin\theta = \frac{1}{2}$."),
   (r"$\cos^{-1}\frac{5}{6}$", r"Sign slip in the $\hat j$ product, taking $(-1)(1) = +1$, so $\vec a\cdot\vec b = 2 + 1 + 2 = 5$ and $\cos\theta = \frac{5}{6}$."),
   (r"$\cos^{-1}\frac{1}{12}$", r"Divides $\vec a\cdot\vec b = 3$ by $|\vec a|^2|\vec b|^2 = 36$ in place of $|\vec a||\vec b| = 6$, giving $\frac{1}{12}$.")],
  r"$\vec a\cdot\vec b = 2 - 1 + 2 = 3$ and $|\vec a| = |\vec b| = \sqrt{6}$. Hence $\cos\theta = \frac{3}{6} = \frac{1}{2}$, so $\theta = \frac{\pi}{3}$.",
  r"Using squared magnitudes in the denominator of $\cos\theta$, or sign slips in the component products.",
  "U12-B-angle-components", "One formula, three products and two magnitudes.",
  check=_c001, values=[pi / 3, pi / 6, acos(Rational(5, 6)), acos(Rational(1, 12))], cognitive="Application", source_class=SC)


def _c002():
    a, b = V(2, lam, 1), V(1, -2, 4)
    return solve(dot(a, b), lam)[0]


q("U12-B-002", TOPIC, "Perpendicularity condition", "Easy", "Inverse/parameter MCQ",
  r"If the vectors $2\hat{i} + \lambda\hat{j} + \hat{k}$ and $\hat{i} - 2\hat{j} + 4\hat{k}$ are perpendicular, then $\lambda$ equals",
  r"$3$",
  [(r"$-3$", r"Sign slip in the $\hat j$ product, writing $2 + 2\lambda + 4 = 0$, so $\lambda = -3$."),
   (r"$1$", r"Leaves out the $\hat k$ product and solves $2 - 2\lambda = 0$."),
   (r"$6$", r"Drops the coefficient $-2$ of $\hat j$, solving $2 - \lambda + 4 = 0$.")],
  r"Perpendicular vectors have zero dot product: $2(1) + \lambda(-2) + 1(4) = 6 - 2\lambda = 0$, so $\lambda = 3$.",
  "Missing one component product or its sign when writing the dot product.",
  "U12-B-perp-parameter", "Single linear equation from the dot product.",
  check=_c002, values=[3, -3, 1, 6], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If the vectors $2\hat{i} + \lambda\hat{j} + \hat{k}$ and $\hat{i} - 2\hat{j} + 4\hat{k}$ are perpendicular, then the value of $\lambda$ is", answer=3))


def _c003():
    a, b = V(2, 3, 2), V(1, 2, 1)
    return simplify(dot(a, b) / mag(b))


q("U12-B-003", TOPIC, "Scalar projection", "Easy", "Single-step computation MCQ",
  r"The scalar projection of $\vec{a} = 2\hat{i} + 3\hat{j} + 2\hat{k}$ on $\vec{b} = \hat{i} + 2\hat{j} + \hat{k}$ is",
  r"$\frac{5\sqrt{6}}{3}$",
  [(r"$\frac{10}{\sqrt{17}}$", r"Divides $\vec a\cdot\vec b = 10$ by $|\vec a| = \sqrt{17}$, which gives the projection of $\vec b$ on $\vec a$."),
   (r"$\frac{5}{3}$", r"Divides by $|\vec b|^2 = 6$ in place of $|\vec b| = \sqrt{6}$: $\frac{10}{6} = \frac{5}{3}$."),
   (r"$10$", r"Stops at $\vec a\cdot\vec b = 10$ without dividing by $|\vec b|$.")],
  r"$\vec a\cdot\vec b = 2 + 6 + 2 = 10$ and $|\vec b| = \sqrt{6}$, so the projection is $\frac{10}{\sqrt{6}} = \frac{5\sqrt{6}}{3}$.",
  r"Dividing by the magnitude of the wrong vector, or by $|\vec b|^2$.",
  "U12-B-scalar-projection", "Direct use of the projection formula.",
  check=_c003, values=[5 * sqrt(6) / 3, 10 / sqrt(17), Rational(5, 3), 10], cognitive="Application", source_class=SC)


def _c004():
    A, B, th = 3, 5, pi / 3
    return sqrt(A**2 + B**2 + 2 * A * B * cos(th))


q("U12-B-004", TOPIC, "Magnitude of a sum from magnitudes and angle", "Easy", "Single-step computation MCQ",
  r"If $|\vec{a}| = 3$, $|\vec{b}| = 5$ and the angle between $\vec{a}$ and $\vec{b}$ is $\frac{\pi}{3}$, then $|\vec{a} + \vec{b}|$ equals",
  r"$7$",
  [(r"$\sqrt{19}$", r"Uses $|\vec a|^2 + |\vec b|^2 - 2\vec a\cdot\vec b = 34 - 15$, which is $|\vec a - \vec b|^2$."),
   (r"$8$", r"Adds the magnitudes, $3 + 5$, as if the vectors were in the same direction."),
   (r"$\sqrt{34}$", r"Drops the cross term $2\vec a\cdot\vec b$, as if the vectors were perpendicular.")],
  r"$|\vec a + \vec b|^2 = 9 + 25 + 2(3)(5)\cos\frac{\pi}{3} = 34 + 15 = 49$, so $|\vec a + \vec b| = 7$.",
  "Ignoring or mis-signing the cross term when squaring a sum of vectors.",
  "U12-B-magnitude-sum-angle", "Single expansion of a squared magnitude.",
  check=_c004, values=[7, sqrt(19), 8, sqrt(34)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $|\vec{a}| = 3$, $|\vec{b}| = 5$ and the angle between $\vec{a}$ and $\vec{b}$ is $\frac{\pi}{3}$, then the value of $|\vec{a} + \vec{b}|$ is", answer=7))


def _c005():
    th = symbols('th')
    sols = [s for s in solve(1 + 1 + 2 * cos(th) - 3, th) if 0 <= s <= pi]
    return sols[0]


q("U12-B-005", TOPIC, "Angle between unit vectors from the magnitude of their sum", "Easy", "Inverse/parameter MCQ",
  r"If $\hat{a}$ and $\hat{b}$ are unit vectors such that $|\hat{a} + \hat{b}| = \sqrt{3}$, then the angle between $\hat{a}$ and $\hat{b}$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{2\pi}{3}$", r"Uses $|\hat a + \hat b|^2 = 2 - 2\cos\theta$ (the formula for the difference), so $\cos\theta = -\frac{1}{2}$."),
   (r"$\frac{\pi}{6}$", r"Writes $|\hat a + \hat b| = 2\cos\theta$ in place of $2\cos\frac{\theta}{2}$, so $\cos\theta = \frac{\sqrt{3}}{2}$."),
   (r"$0$", r"Drops the factor $2$ in the cross term: $3 = 2 + \cos\theta$ gives $\cos\theta = 1$.")],
  r"$|\hat a + \hat b|^2 = 1 + 1 + 2\cos\theta = 3$, so $\cos\theta = \frac{1}{2}$ and $\theta = \frac{\pi}{3}$.",
  "Mixing up the expansions of the squared sum and squared difference.",
  "U12-B-unit-angle-from-sum", "One expansion, then one inverse cosine.",
  check=_c005, values=[pi / 3, 2 * pi / 3, pi / 6, 0], cognitive="Application", source_class=SC)


def _c006():
    ab = solve((9 + 16 + 2 * k) - (9 + 16 - 2 * k), k)[0]
    return sqrt(9 + 16 + 2 * ab)


q("U12-B-006", TOPIC, "Equal magnitudes of sum and difference", "Easy", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and $|\vec{a} + \vec{b}| = |\vec{a} - \vec{b}|$, then $|\vec{a} + \vec{b}|$ equals",
  r"$5$",
  [(r"$7$", r"Adds the magnitudes $3 + 4$, ignoring the condition."),
   (r"$1$", r"Takes $|\vec a - \vec b| = |\vec b| - |\vec a| = 1$ and equates the sum to it."),
   (r"$\sqrt{7}$", r"Computes $\sqrt{|\vec b|^2 - |\vec a|^2} = \sqrt{16 - 9}$, as if the vectors formed a right angle with $\vec b$ as hypotenuse.")],
  r"Squaring $|\vec a + \vec b| = |\vec a - \vec b|$ gives $4\,\vec a\cdot\vec b = 0$, so $\vec a \perp \vec b$. Then $|\vec a + \vec b|^2 = 9 + 16 = 25$ and $|\vec a + \vec b| = 5$.",
  r"Not recognising that $|\vec a + \vec b| = |\vec a - \vec b|$ means $\vec a\cdot\vec b = 0$.",
  "U12-B-equal-sum-diff", "Two steps: deduce perpendicularity, then compute.",
  check=_c006, values=[5, 7, 1, sqrt(7)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and $|\vec{a} + \vec{b}| = |\vec{a} - \vec{b}|$, then the value of $|\vec{a} + \vec{b}|$ is", answer=5))


def _c007():
    F, P, Q = V(3, 2, -1), V(1, 2, 3), V(4, 0, 5)
    return dot(F, Q - P)


q("U12-B-007", TOPIC, "Work done by a constant force", "Easy", "Single-step computation MCQ",
  r"A constant force $\vec{F} = 3\hat{i} + 2\hat{j} - \hat{k}$ moves a particle from the point $P(1, 2, 3)$ to the point $Q(4, 0, 5)$. The work done (in appropriate units) is",
  r"$3$",
  [(r"$-3$", r"Takes the displacement as $\overrightarrow{OP} - \overrightarrow{OQ} = -3\hat i + 2\hat j - 2\hat k$, reversing its direction."),
   (r"$7$", r"Dots $\vec F$ with the position vector of $Q$, $4\hat i + 5\hat k$, in place of the displacement: $12 + 0 - 5 = 7$."),
   (r"$11$", r"Dots $\vec F$ with $\overrightarrow{OP} + \overrightarrow{OQ} = 5\hat i + 2\hat j + 8\hat k$: $15 + 4 - 8 = 11$.")],
  r"Displacement $\overrightarrow{PQ} = 3\hat i - 2\hat j + 2\hat k$. Work $= \vec F\cdot\overrightarrow{PQ} = 9 - 4 - 2 = 3$.",
  "Using a position vector, or the reversed displacement, in place of the displacement.",
  "U12-B-work-done", "One displacement and one dot product.",
  check=_c007, values=[3, -3, 7, 11], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A constant force $\vec{F} = 3\hat{i} + 2\hat{j} - \hat{k}$ moves a particle from the point $P(1, 2, 3)$ to the point $Q(4, 0, 5)$. The work done (in appropriate units) is", answer=3))


def _c008():
    A, B, ab = 5, 3, symbols('ab')
    return expand(A**2 - ab + ab - B**2)


q("U12-B-008", TOPIC, "Dot product of sum and difference", "Easy", "Single-step computation MCQ",
  r"If $|\vec{a}| = 5$ and $|\vec{b}| = 3$, then $(\vec{a} + \vec{b})\cdot(\vec{a} - \vec{b})$ equals",
  r"$16$",
  [(r"$34$", r"Sign slip in the expansion, writing $|\vec a|^2 + |\vec b|^2$."),
   (r"$4$", r"Computes $(|\vec a| - |\vec b|)^2 = 4$, treating the product as a squared difference of magnitudes."),
   (r"$2$", r"Takes the product as $|\vec a| - |\vec b| = 2$, confusing it with a difference of magnitudes.")],
  r"$(\vec a + \vec b)\cdot(\vec a - \vec b) = |\vec a|^2 - \vec a\cdot\vec b + \vec b\cdot\vec a - |\vec b|^2 = 25 - 9 = 16$, since the dot product is commutative.",
  "Not seeing that the cross terms cancel by commutativity of the dot product.",
  "U12-B-sum-diff-dot", "Single algebraic identity.",
  check=_c008, values=[16, 34, 4, 2], cognitive="Understanding", source_class=SC,
  numerical=dict(question=r"If $|\vec{a}| = 5$ and $|\vec{b}| = 3$, then the value of $(\vec{a} + \vec{b})\cdot(\vec{a} - \vec{b})$ is", answer=16))


def _c009():
    a, b = V(2, 1, 3), V(1, -1, 1)
    return dot(a, b) / dot(b, b) * b


q("U12-B-009", TOPIC, "Vector projection", "Easy", "Single-step computation MCQ",
  r"The vector projection of $\vec{a} = 2\hat{i} + \hat{j} + 3\hat{k}$ on $\vec{b} = \hat{i} - \hat{j} + \hat{k}$ is",
  r"$\frac{4}{3}(\hat{i} - \hat{j} + \hat{k})$",
  [(r"$\frac{4}{\sqrt{3}}(\hat{i} - \hat{j} + \hat{k})$", r"Multiplies the scalar projection $\frac{4}{\sqrt 3}$ by $\vec b$ itself, not by the unit vector $\hat b$."),
   (r"$\frac{2}{7}(2\hat{i} + \hat{j} + 3\hat{k})$", r"Projects $\vec b$ on $\vec a$: $\frac{\vec a\cdot\vec b}{|\vec a|^2}\vec a = \frac{4}{14}\vec a$."),
   (r"$\frac{4}{3}(2\hat{i} + \hat{j} + 3\hat{k})$", r"Uses the correct factor $\frac{\vec a\cdot\vec b}{|\vec b|^2} = \frac{4}{3}$ but multiplies it by $\vec a$ in place of $\vec b$.")],
  r"$\vec a\cdot\vec b = 2 - 1 + 3 = 4$ and $|\vec b|^2 = 3$. The vector projection is $\frac{\vec a\cdot\vec b}{|\vec b|^2}\vec b = \frac{4}{3}(\hat i - \hat j + \hat k)$.",
  "Confusing the scalar and vector projection formulas, or the roles of the two vectors.",
  "U12-B-vector-projection", "One formula with two quantities.",
  check=_c009, values=[Rational(4, 3) * V(1, -1, 1), 4 / sqrt(3) * V(1, -1, 1), Rational(2, 7) * V(2, 1, 3), Rational(4, 3) * V(2, 1, 3)],
  cognitive="Application", source_class=SC)


def _c010():
    return ang(V(2, 2, 1), V(0, 0, 1))


q("U12-B-010", TOPIC, "Angle with a coordinate axis", "Easy", "Single-step computation MCQ",
  r"The angle which the vector $2\hat{i} + 2\hat{j} + \hat{k}$ makes with the positive $z$-axis is",
  r"$\cos^{-1}\frac{1}{3}$",
  [(r"$\cos^{-1}\frac{2}{3}$", r"Uses the $\hat i$ component, which gives the angle with the $x$-axis."),
   (r"$\cos^{-1}\frac{1}{9}$", r"Divides by $|\vec a|^2 = 9$ in place of $|\vec a| = 3$."),
   (r"$\cos^{-1}\frac{1}{5}$", r"Divides by the sum of the components $2 + 2 + 1 = 5$ in place of the magnitude.")],
  r"The dot product with $\hat k$ is $1$ and the magnitude is $\sqrt{4 + 4 + 1} = 3$, so $\cos\theta = \frac{1}{3}$ and $\theta = \cos^{-1}\frac{1}{3}$.",
  r"Using the wrong component or the wrong normaliser for the angle with an axis.",
  "U12-B-angle-with-axis", "Dot product with a unit axis vector.",
  check=_c010, values=[acos(Rational(1, 3)), acos(Rational(2, 3)), acos(Rational(1, 9)), acos(Rational(1, 5))], cognitive="Application", source_class=SC)


def _c011():
    a, b, c = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
    s1 = not (dot(a, b) == dot(a, c) and b != c)   # counterexample exists -> statement false
    u = Matrix(symbols('u1:4')); w = Matrix(symbols('w1:4'))
    s2 = expand(dot(u + w, u + w) - dot(u - w, u - w) - 4 * dot(u, w)) == 0
    return (bool(s1), bool(s2))


q("U12-B-011", TOPIC, "Properties of the dot product", "Easy", "Statement-based MCQ",
  r"Statement I: If $\vec{a} \ne \vec{0}$ and $\vec{a}\cdot\vec{b} = \vec{a}\cdot\vec{c}$, then $\vec{b} = \vec{c}$. Statement II: If $\vec{a}$ and $\vec{b}$ are non-zero vectors with $|\vec{a} + \vec{b}| = |\vec{a} - \vec{b}|$, then $\vec{a}$ is perpendicular to $\vec{b}$." + TAIL,
  ST_FT,
  [(ST_TT, r"Treats $\vec a$ as a factor that can be cancelled from a dot product equation."),
   (ST_FF, r"Rejects Statement II, not expanding $|\vec a \pm \vec b|^2$ to see that the difference is $4\,\vec a\cdot\vec b$."),
   (ST_TF, r"Cancels $\vec a$ in Statement I and also doubts Statement II.")],
  r"Statement I is false: $\vec a\cdot\vec b = \vec a\cdot\vec c$ only says $\vec a \perp (\vec b - \vec c)$; for example $\vec a = \hat i$, $\vec b = \hat j$, $\vec c = \hat k$. Statement II is true: $|\vec a + \vec b|^2 - |\vec a - \vec b|^2 = 4\,\vec a\cdot\vec b = 0$.",
  "Cancelling a vector from both sides of a dot product equation.",
  "U12-B-statements-concept", "Two short property checks.",
  check=_c011, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Understanding", source_class=SC)


def _c012():
    A, B, ab = 2, 3, 3
    return sqrt(4 * A**2 + B**2 - 4 * ab)


q("U12-B-012", TOPIC, "Magnitude of a linear combination", "Easy", "Single-step computation MCQ",
  r"If $|\vec{a}| = 2$, $|\vec{b}| = 3$ and $\vec{a}\cdot\vec{b} = 3$, then $|2\vec{a} - \vec{b}|$ equals",
  r"$\sqrt{13}$",
  [(r"$\sqrt{37}$", r"Sign slip: $16 + 9 + 4(3) = 37$."),
   (r"$\sqrt{19}$", r"Takes the cross term as $-2\,\vec a\cdot\vec b = -6$ in place of $-4\,\vec a\cdot\vec b = -12$: $16 + 9 - 6 = 19$."),
   (r"$1$", r"Computes $2|\vec a| - |\vec b| = 4 - 3$, as if the vectors were parallel.")],
  r"$|2\vec a - \vec b|^2 = 4|\vec a|^2 - 4\,\vec a\cdot\vec b + |\vec b|^2 = 16 - 12 + 9 = 13$, so the magnitude is $\sqrt{13}$.",
  "Mishandling the coefficient of the cross term when a vector is scaled.",
  "U12-B-magnitude-combination", "Single expansion with a scalar multiple.",
  check=_c012, values=[sqrt(13), sqrt(37), sqrt(19), 1], cognitive="Application", source_class=SC)


def _c013():
    a, b = V(lam, 2, 2), V(1, 4, 4)
    sols = [s for s in solve(dot(a + b, a - b), lam) if s > 0]
    return sols[0]


q("U12-B-013", TOPIC, "Sum perpendicular to difference", "Easy", "Inverse/parameter MCQ",
  r"Let $\vec{a} = \lambda\hat{i} + 2\hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + 4\hat{j} + 4\hat{k}$, where $\lambda > 0$. If $\vec{a} + \vec{b}$ is perpendicular to $\vec{a} - \vec{b}$, then $\lambda$ equals",
  r"$5$",
  [(r"$25$", r"Solves $\lambda^2 = 25$ correctly but reports $\lambda^2$."),
   (r"$\sqrt{33}$", r"Equates $\lambda^2$ to $|\vec b|^2 = 33$, forgetting the other components of $\vec a$."),
   (r"$\sqrt{41}$", r"Sign slip moving $8$ across: $\lambda^2 = 33 + 8$.")],
  r"$(\vec a + \vec b)\cdot(\vec a - \vec b) = |\vec a|^2 - |\vec b|^2 = 0$, so $\lambda^2 + 8 = 1 + 16 + 16 = 33$, giving $\lambda^2 = 25$ and $\lambda = 5$.",
  r"Not converting the perpendicularity of $\vec a \pm \vec b$ into $|\vec a| = |\vec b|$.",
  "U12-B-sum-diff-perp-parameter", "Identity followed by a quadratic.",
  check=_c013, values=[5, 25, sqrt(33), sqrt(41)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $\vec{a} = \lambda\hat{i} + 2\hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + 4\hat{j} + 4\hat{k}$, where $\lambda > 0$. If $\vec{a} + \vec{b}$ is perpendicular to $\vec{a} - \vec{b}$, then the value of $\lambda$ is", answer=5))


def _c014():
    sols = solve([3 * x - 4 * y, x**2 + y**2 - 1], [x, y], dict=True)
    s = [d for d in sols if d[x] > 0][0]
    return V(s[x], s[y], 0)


q("U12-B-014", TOPIC, "Unit vector perpendicular to a given vector", "Easy", "Multi-step computation MCQ",
  r"A unit vector $x\hat{i} + y\hat{j}$ with $x > 0$ is perpendicular to $3\hat{i} - 4\hat{j} + 5\hat{k}$. This unit vector is",
  r"$\frac{1}{5}(4\hat{i} + 3\hat{j})$",
  [(r"$\frac{1}{5}(3\hat{i} - 4\hat{j})$", r"Normalises the $xy$-part of the given vector, which is parallel to it rather than perpendicular."),
   (r"$\frac{1}{5}(4\hat{i} - 3\hat{j})$", r"Drops the minus sign and solves $3x + 4y = 0$, giving $y = -\frac{3}{4}x$."),
   (r"$\frac{1}{5}(3\hat{i} + 4\hat{j})$", r"Inverts the ratio from $3x = 4y$, taking $\frac{y}{x} = \frac{4}{3}$.")],
  r"Perpendicularity gives $3x - 4y = 0$, so $y = \frac{3}{4}x$. With $x^2 + y^2 = 1$ and $x > 0$: $x = \frac{4}{5}$, $y = \frac{3}{5}$.",
  "Confusing a vector parallel to the projection with one perpendicular to the vector.",
  "U12-B-unit-perp-vector", "Dot condition plus normalisation.",
  check=_c014, values=[V(Rational(4, 5), Rational(3, 5), 0), V(Rational(3, 5), Rational(-4, 5), 0), V(Rational(4, 5), Rational(-3, 5), 0), V(Rational(3, 5), Rational(4, 5), 0)],
  cognitive="Application", source_class=SC)


def _c015():
    a, b = V(1, lam, 1), V(2, 2, 1)
    return solve(dot(a, b) / mag(b) - 3, lam)[0]


q("U12-B-015", TOPIC, "Parameter from a given projection", "Easy", "Inverse/parameter MCQ",
  r"If the scalar projection of $\hat{i} + \lambda\hat{j} + \hat{k}$ on $2\hat{i} + 2\hat{j} + \hat{k}$ is $3$, then $\lambda$ equals",
  r"$3$",
  [(r"$0$", r"Forgets to divide by $|\vec b| = 3$, solving $3 + 2\lambda = 3$."),
   (r"$12$", r"Divides by $|\vec b|^2 = 9$, solving $\frac{3 + 2\lambda}{9} = 3$."),
   (r"$\frac{7}{2}$", r"Leaves out the $\hat k$ product, solving $2 + 2\lambda = 9$.")],
  r"The dot product is $2 + 2\lambda + 1 = 3 + 2\lambda$ and $|\vec b| = 3$, so $\frac{3 + 2\lambda}{3} = 3$, giving $\lambda = 3$.",
  "Wrong normaliser in the projection formula.",
  "U12-B-projection-parameter", "Projection formula inverted for one unknown.",
  check=_c015, values=[3, 0, 12, Rational(7, 2)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If the scalar projection of $\hat{i} + \lambda\hat{j} + \hat{k}$ on $2\hat{i} + 2\hat{j} + \hat{k}$ is $3$, then the value of $\lambda$ is", answer=3))


def _c016():
    return ang(V(1, 1, 1), V(1, 0, 0))


q("U12-B-016", TOPIC, "Angles in a cube", "Easy", "Single-step computation MCQ",
  r"A unit cube has one vertex at the origin $O$ and edges along the positive coordinate axes. The angle between the diagonal from $O$ to $(1, 1, 1)$ and the edge along the $x$-axis is",
  r"$\cos^{-1}\frac{1}{\sqrt{3}}$",
  [(r"$\cos^{-1}\frac{1}{3}$", r"This is the angle between two body diagonals, e.g. $\hat i + \hat j + \hat k$ and $-\hat i + \hat j + \hat k$."),
   (r"$\cos^{-1}\sqrt{\frac{2}{3}}$", r"This is the angle between the body diagonal and the face diagonal $\hat i + \hat j$."),
   (r"$\cos^{-1}\frac{1}{\sqrt{2}}$", r"This is the angle between the face diagonal $\hat i + \hat j$ and the edge $\hat i$.")],
  r"The diagonal is $\hat i + \hat j + \hat k$ with magnitude $\sqrt 3$ and the edge is $\hat i$. Their dot product is $1$, so $\cos\theta = \frac{1}{\sqrt 3}$.",
  "Picking the wrong pair of lines in the cube.",
  "U12-B-cube-angles", "Choose two direction vectors and apply the angle formula.",
  check=_c016, values=[acos(1 / sqrt(3)), acos(Rational(1, 3)), acos(sqrt(Rational(2, 3))), acos(1 / sqrt(2))], cognitive="Application", source_class=SC)

# ================================================================ MEDIUM (24)


def _c017():
    a, b = V(lam, 1, -2), V(lam, -3, 1)
    S = solve_univariate_inequality(dot(a, b) < 0, lam, relational=False)
    # antiparallel case: a = k b with k < 0
    anti = solve(list(a - k * b), [lam, k], dict=True)
    assert all(d[k] >= 0 for d in anti)
    return S


q("U12-B-017", TOPIC, "Parameter range for an obtuse angle", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $\lambda$ for which the angle between $\vec{a} = \lambda\hat{i} + \hat{j} - 2\hat{k}$ and $\vec{b} = \lambda\hat{i} - 3\hat{j} + \hat{k}$ is obtuse is",
  r"$(-\sqrt{5}, \sqrt{5})$",
  [(r"$(-\infty, -\sqrt{5}) \cup (\sqrt{5}, \infty)$", r"Reverses the inequality, solving $\lambda^2 - 5 > 0$, which is the acute case."),
   (r"$(0, \sqrt{5})$", r"Keeps only positive $\lambda$, discarding the negative half of $\lambda^2 < 5$."),
   (r"$[-\sqrt{5}, \sqrt{5}]$", r"Includes $\lambda = \pm\sqrt 5$, where $\vec a\cdot\vec b = 0$ and the angle is a right angle.")],
  r"$\vec a\cdot\vec b = \lambda^2 - 3 - 2 = \lambda^2 - 5$. The angle is obtuse when $\vec a\cdot\vec b < 0$ and the vectors are not antiparallel. Antiparallel would need $1 = -3k$ and $-2 = k$ at once, which is impossible, so the answer is $\lambda^2 < 5$, i.e. $(-\sqrt 5, \sqrt 5)$.",
  r"Including the perpendicular case, or forgetting that $\lambda^2 < 5$ has a negative half.",
  "U12-B-angle-sign-range", "Quadratic inequality plus an antiparallel check.",
  check=_c017, values=[Interval.open(-sqrt(5), sqrt(5)), Union(Interval.open(-oo, -sqrt(5)), Interval.open(sqrt(5), oo)), Interval.open(0, sqrt(5)), Interval(-sqrt(5), sqrt(5))],
  cognitive="Application", source_class=SC)


def _c018():
    ab = solve(9 + 16 + 2 * k - 37, k)[0]
    return sqrt(4 * 9 + 9 * 16 - 12 * ab)


q("U12-B-018", TOPIC, "Magnitude of a combination from given data", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and $|\vec{a} + \vec{b}| = \sqrt{37}$, then $|2\vec{a} - 3\vec{b}|$ equals",
  r"$6\sqrt{3}$",
  [(r"$6\sqrt{7}$", r"Sign slip giving $\vec a\cdot\vec b = -6$: $36 + 144 + 72 = 252$."),
   (r"$6$", r"Forgets the factor $2$ in $2\,\vec a\cdot\vec b = 12$, so takes $\vec a\cdot\vec b = 12$: $180 - 144 = 36$."),
   (r"$12$", r"Uses the cross term $-6\,\vec a\cdot\vec b$ in place of $-12\,\vec a\cdot\vec b$: $180 - 36 = 144$.")],
  r"From $37 = 9 + 16 + 2\,\vec a\cdot\vec b$, $\vec a\cdot\vec b = 6$. Then $|2\vec a - 3\vec b|^2 = 4(9) + 9(16) - 12(6) = 108$, so the magnitude is $6\sqrt 3$.",
  "Mis-scaling the cross term in a squared linear combination.",
  "U12-B-magnitude-combination", "Two expansions: find the dot product, then use it.",
  check=_c018, values=[6 * sqrt(3), 6 * sqrt(7), 6, 12], cognitive="Application", source_class=SC)


def _c019():
    a, b = V(1, 1, 1), V(2, -1, 1)
    s1 = simplify(dot(a, b) / mag(b) - Rational(2, 3)) == 0
    th = 2 * pi / 3
    s2 = simplify(sqrt(2 - 2 * cos(th)) - 1) == 0
    return (bool(s1), bool(s2))


q("U12-B-019", TOPIC, "Projection and magnitude of difference", "Medium", "Statement-based MCQ",
  r"Statement I: The scalar projection of $\hat{i} + \hat{j} + \hat{k}$ on $2\hat{i} - \hat{j} + \hat{k}$ is $\frac{2}{3}$. Statement II: If $\hat{a}$ and $\hat{b}$ are unit vectors inclined at an angle $\frac{2\pi}{3}$, then $|\hat{a} - \hat{b}| = 1$." + TAIL,
  ST_FF,
  [(ST_TT, r"Accepts $\frac{2}{3}$ by dividing the dot product $2$ by $|\hat{i} + \hat{j} + \hat{k}|^2 = 3$, and uses the sum formula $|\hat a - \hat b|^2 = 2 + 2\cos\frac{2\pi}{3} = 1$."),
   (ST_TF, r"Accepts the projection $\frac{2}{3}$ by dividing the dot product $2$ by $|\hat{i} + \hat{j} + \hat{k}|^2 = 3$, but evaluates $|\hat a - \hat b| = \sqrt 3$ correctly."),
   (ST_FT, r"Computes the projection $\frac{\sqrt 6}{3}$ correctly but uses the sum formula $|\hat a - \hat b|^2 = 2 + 2\cos\frac{2\pi}{3} = 1$.")],
  r"Statement I: the dot product is $2 - 1 + 1 = 2$ and the magnitude of $2\hat i - \hat j + \hat k$ is $\sqrt 6$, so the projection is $\frac{2}{\sqrt 6} = \frac{\sqrt 6}{3} \ne \frac{2}{3}$; false. Statement II: $|\hat a - \hat b|^2 = 2 - 2\cos\frac{2\pi}{3} = 3$, so $|\hat a - \hat b| = \sqrt 3 \ne 1$; false.",
  "Using the wrong normaliser in a projection and the sum formula for a difference.",
  "U12-B-statements-compute", "Two independent computations to verify.",
  check=_c019, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis", source_class=SC)


def _c020():
    ab = solve(9 + 25 + 2 * k - 49, k)[0]
    return acos(ab / 15)


q("U12-B-020", TOPIC, "Three vectors with zero sum", "Medium", "Multi-step computation MCQ",
  r"If $\vec{a} + \vec{b} + \vec{c} = \vec{0}$ with $|\vec{a}| = 3$, $|\vec{b}| = 5$ and $|\vec{c}| = 7$, then the angle between $\vec{a}$ and $\vec{b}$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{2\pi}{3}$", r"Finds the interior angle of the triangle with sides $3$, $5$, $7$ by the cosine rule; that angle is between $\vec a$ and $-\vec b$."),
   (r"$0$", r"Forgets the factor $2$ in $2\,\vec a\cdot\vec b$: $49 = 34 + \vec a\cdot\vec b$ gives $\vec a\cdot\vec b = 15$ and $\cos\theta = 1$."),
   (r"$\cos^{-1}\frac{1}{4}$", r"Halves twice: takes $\vec a\cdot\vec b = \frac{15}{2}$ and then divides by $2|\vec a||\vec b| = 30$.")],
  r"$\vec c = -(\vec a + \vec b)$, so $49 = 9 + 25 + 2\,\vec a\cdot\vec b$, giving $\vec a\cdot\vec b = \frac{15}{2}$. Then $\cos\theta = \frac{15/2}{15} = \frac{1}{2}$ and $\theta = \frac{\pi}{3}$.",
  "Confusing the angle between two vectors with the interior angle of the triangle they form.",
  "U12-B-sum-zero-angle", "Rearrangement, expansion and an angle-versus-triangle trap.",
  check=_c020, values=[pi / 3, 2 * pi / 3, 0, acos(Rational(1, 4))], cognitive="Analysis", source_class=SC)


def _c021():
    a, b = V(2, -1, 2), V(3, 1, 2)
    b1 = dot(a, b) / dot(a, a) * a
    return b - b1


q("U12-B-021", TOPIC, "Resolving a vector along and perpendicular to another", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = 3\hat{i} + \hat{j} + 2\hat{k}$. If $\vec{b} = \vec{b}_1 + \vec{b}_2$, where $\vec{b}_1$ is parallel to $\vec{a}$ and $\vec{b}_2$ is perpendicular to $\vec{a}$, then $\vec{b}_2$ equals",
  r"$\hat{i} + 2\hat{j}$",
  [(r"$-\hat{i} - 2\hat{j}$", r"Computes $\vec b_1 - \vec b$ in place of $\vec b - \vec b_1$."),
   (r"$-3\hat{i} + 4\hat{j} - 4\hat{k}$", r"Uses the scalar projection $\frac{\vec a\cdot\vec b}{|\vec a|} = 3$ as the coefficient of $\vec a$: $\vec b - 3\vec a$."),
   (r"$5\hat{i} + 4\hat{k}$", r"Sign slip, adding $\vec b_1$: $\vec b + \vec a$.")],
  r"$\vec b_1 = \frac{\vec a\cdot\vec b}{|\vec a|^2}\vec a = \frac{6 - 1 + 4}{9}\vec a = \vec a$. Hence $\vec b_2 = \vec b - \vec a = \hat i + 2\hat j$; indeed $(\hat i + 2\hat j)\cdot\vec a = 2 - 2 = 0$.",
  r"Using the scalar projection in place of the coefficient $\frac{\vec a\cdot\vec b}{|\vec a|^2}$.",
  "U12-B-perpendicular-component", "Vector projection then subtraction, with a check.",
  check=_c021, values=[V(1, 2, 0), V(-1, -2, 0), V(-3, 4, -4), V(5, 0, 4)], cognitive="Application", source_class=SC)


def _c022():
    c = V(1, 2, 2)
    L = symbols('L')
    r = V(x, y, z)
    G = dot(c, r) - L * (dot(r, r) - 9)
    sols = solve([diff(G, s) for s in (x, y, z)] + [dot(r, r) - 9], [x, y, z, L], dict=True)
    return max(dot(c, r).subs(s) for s in sols)


q("U12-B-022", TOPIC, "Maximum of a dot product", "Medium", "Conceptual/application MCQ",
  r"If $\vec{r}$ is a vector with $|\vec{r}| = 3$, then the maximum value of $\vec{r}\cdot(\hat{i} + 2\hat{j} + 2\hat{k})$ is",
  r"$9$",
  [(r"$15$", r"Multiplies the sum of the components $1 + 2 + 2 = 5$ by $|\vec r| = 3$, in place of the magnitude $3$."),
   (r"$27$", r"Multiplies $|\vec r|$ by the squared magnitude $9$ of $\hat i + 2\hat j + 2\hat k$."),
   (r"$3$", r"Takes the magnitude of $\hat i + 2\hat j + 2\hat k$ only, forgetting the factor $|\vec r|$.")],
  r"$\vec r\cdot\vec c = |\vec r||\vec c|\cos\theta \le |\vec r||\vec c| = 3 \cdot 3 = 9$, with equality when $\vec r = \hat i + 2\hat j + 2\hat k$ (same direction).",
  r"Not using $\vec r\cdot\vec c \le |\vec r||\vec c|$.",
  "U12-B-cauchy-schwarz", "Recognise the bound and check it is attained.",
  check=_c022, values=[9, 15, 27, 3], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $\vec{r}$ is a vector with $|\vec{r}| = 3$, then the maximum value of $\vec{r}\cdot(\hat{i} + 2\hat{j} + 2\hat{k})$ is", answer=9))


def _c023():
    c = solve(2 + 2 * k - 1, k)[0]          # |a|=|b|=1 scale, cos of angle
    return acos(simplify((1 - c) / sqrt(2 - 2 * c)))


q("U12-B-023", TOPIC, "Equal magnitudes and an angle", "Medium", "Multi-step computation MCQ",
  r"If $\vec{a}$ and $\vec{b}$ are non-zero vectors with $|\vec{a}| = |\vec{b}| = |\vec{a} + \vec{b}|$, then the angle between $\vec{a}$ and $\vec{a} - \vec{b}$ is",
  r"$\frac{\pi}{6}$",
  [(r"$\frac{\pi}{3}$", r"Sign slip giving $\vec a\cdot\vec b = +\frac{1}{2}|\vec a|^2$; then $|\vec a - \vec b| = |\vec a|$ and $\cos\theta = \frac{1}{2}$."),
   (r"$\frac{2\pi}{3}$", r"Gives the angle between $\vec a$ and $\vec b$, not between $\vec a$ and $\vec a - \vec b$."),
   (r"$\frac{5\pi}{6}$", r"Writes $\vec a\cdot(\vec a - \vec b)$ as $\vec a\cdot\vec b - |\vec a|^2 = -\frac{3}{2}|\vec a|^2$, so $\cos\theta = -\frac{\sqrt 3}{2}$.")],
  r"Let $|\vec a| = |\vec b| = m$. From $m^2 = 2m^2 + 2\,\vec a\cdot\vec b$, $\vec a\cdot\vec b = -\frac{m^2}{2}$. Then $\vec a\cdot(\vec a - \vec b) = \frac{3m^2}{2}$ and $|\vec a - \vec b|^2 = 2m^2 + m^2 = 3m^2$, so $\cos\theta = \frac{3m^2/2}{m \cdot \sqrt 3 m} = \frac{\sqrt 3}{2}$ and $\theta = \frac{\pi}{6}$.",
  "Answering with the angle between the original vectors.",
  "U12-B-equal-magnitude-angle", "Two derived quantities combined in the angle formula.",
  check=_c023, values=[pi / 6, pi / 3, 2 * pi / 3, 5 * pi / 6], cognitive="Analysis", source_class=SC)


def _c024():
    a, b, c = V(2, -1, 1), V(1, 1, 1), V(1, 2, -1)
    tt = solve(dot(a, b + t * c), t)[0]
    return mag(b + tt * c)


q("U12-B-024", TOPIC, "Combination perpendicular to a vector", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} - \hat{j} + \hat{k}$, $\vec{b} = \hat{i} + \hat{j} + \hat{k}$ and $\vec{c} = \hat{i} + 2\hat{j} - \hat{k}$. If $\vec{r} = \vec{b} + t\vec{c}$ is perpendicular to $\vec{a}$, then $|\vec{r}|$ equals",
  r"$\sqrt{35}$",
  [(r"$\sqrt{19}$", r"Sign slip giving $t = -2$, so $\vec r = -\hat i - 3\hat j + 3\hat k$."),
   (r"$\sqrt{\frac{13}{2}}$", r"Inverts the ratio and takes $t = \frac{1}{2}$, so $\vec r = \frac{3}{2}\hat i + 2\hat j + \frac{1}{2}\hat k$."),
   (r"$2\sqrt{6}$", r"Finds $t = 2$ but then reports $|t\vec c| = |2\vec c|$, forgetting $\vec b$.")],
  r"$\vec a\cdot\vec b = 2 - 1 + 1 = 2$ and $\vec a\cdot\vec c = 2 - 2 - 1 = -1$. So $\vec a\cdot\vec r = 2 - t = 0$ and $t = 2$. Then $\vec r = 3\hat i + 5\hat j - \hat k$ and $|\vec r| = \sqrt{35}$.",
  "Sign errors when solving the linear equation for the parameter.",
  "U12-B-combination-perp", "Two dot products, a linear equation, then a magnitude.",
  check=_c024, values=[sqrt(35), sqrt(19), sqrt(Rational(13, 2)), 2 * sqrt(6)], cognitive="Application", source_class=SC)


def _c025():
    a, b = V(1, 1, p), V(1, 1, 0)
    sols = [s for s in solve(dot(a, b) / (mag(a) * mag(b)) - Rational(1, 2), p) if s > 0]
    return sols[0]


q("U12-B-025", TOPIC, "Parameter from a given angle", "Medium", "Inverse/parameter MCQ",
  r"If the angle between $\hat{i} + \hat{j} + p\hat{k}$ and $\hat{i} + \hat{j}$ is $\frac{\pi}{3}$ and $p > 0$, then $p$ equals",
  r"$\sqrt{6}$",
  [(r"$\sqrt{14}$", r"Leaves out $|\hat i + \hat j| = \sqrt 2$: solves $\frac{2}{\sqrt{2 + p^2}} = \frac{1}{2}$."),
   (r"$\frac{\sqrt{6}}{3}$", r"Uses $\cos\frac{\pi}{3} = \frac{\sqrt 3}{2}$, which gives $2 + p^2 = \frac{8}{3}$."),
   (r"$6$", r"Solves $p^2 = 6$ correctly but reports $p^2$.")],
  r"$\cos\frac{\pi}{3} = \frac{2}{\sqrt{2 + p^2}\,\sqrt 2} = \frac{1}{2}$, so $\sqrt{2(2 + p^2)} = 4$, i.e. $2 + p^2 = 8$ and $p = \sqrt 6$.",
  "Dropping one magnitude from the angle formula.",
  "U12-B-angle-parameter", "Angle formula inverted, then a quadratic.",
  check=_c025, values=[sqrt(6), sqrt(14), sqrt(6) / 3, 6], cognitive="Application", source_class=SC)


def _c026():
    A, B, ab = 2, 1, 2 * 1 * cos(pi / 3)
    num = A**2 - B**2
    den = sqrt(A**2 + B**2 - 2 * ab)
    return simplify(num / den)


q("U12-B-026", TOPIC, "Projection of a sum on a difference", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 2$, $|\vec{b}| = 1$ and the angle between $\vec{a}$ and $\vec{b}$ is $\frac{\pi}{3}$, then the scalar projection of $\vec{a} + \vec{b}$ on $\vec{a} - \vec{b}$ is",
  r"$\sqrt{3}$",
  [(r"$3$", r"Stops at the dot product $(\vec a + \vec b)\cdot(\vec a - \vec b) = 3$."),
   (r"$\frac{3}{\sqrt{7}}$", r"Divides by $|\vec a + \vec b| = \sqrt 7$, which projects the other way."),
   (r"$1$", r"Divides by $|\vec a - \vec b|^2 = 3$ in place of $|\vec a - \vec b| = \sqrt 3$.")],
  r"$(\vec a + \vec b)\cdot(\vec a - \vec b) = 4 - 1 = 3$ and $|\vec a - \vec b|^2 = 4 + 1 - 2(1) = 3$. So the projection is $\frac{3}{\sqrt 3} = \sqrt 3$.",
  "Dividing by the wrong magnitude in a projection.",
  "U12-B-projection-combination", "Dot product and a magnitude, each from an expansion.",
  check=_c026, values=[sqrt(3), 3, 3 / sqrt(7), 1], cognitive="Application", source_class=SC)


def _c027():
    th = symbols('th')
    s1 = simplify((2 - 2 * cos(th)) - (2 * sin(th / 2))**2) == 0   # and sin(th/2) >= 0 on [0, pi]
    a = b = V(1, 0, 0)
    s2 = not (mag(a + b) > mag(a - b) and dot(a, b) >= 0)          # counterexample -> false
    return (bool(s1), bool(s2))


q("U12-B-027", TOPIC, "Magnitude of difference of unit vectors", "Medium", "Statement-based MCQ",
  r"Statement I: If $\hat{a}$ and $\hat{b}$ are unit vectors inclined at an angle $\theta \in [0, \pi]$, then $|\hat{a} - \hat{b}| = 2\sin\frac{\theta}{2}$. Statement II: If $\vec{a}$ and $\vec{b}$ are non-zero vectors with $|\vec{a} + \vec{b}| > |\vec{a} - \vec{b}|$, then $\vec{a}\cdot\vec{b} < 0$." + TAIL,
  ST_TF,
  [(ST_TT, r"Gets the sign wrong in $|\vec a + \vec b|^2 - |\vec a - \vec b|^2 = 4\,\vec a\cdot\vec b$ and so accepts Statement II."),
   (ST_FF, r"Rejects Statement I by writing $|\hat a - \hat b| = 2\cos\frac{\theta}{2}$, the formula for the sum."),
   (ST_FT, r"Swaps the sum and difference formulas in both statements.")],
  r"Statement I: $|\hat a - \hat b|^2 = 2 - 2\cos\theta = 4\sin^2\frac{\theta}{2}$, and $\sin\frac{\theta}{2} \ge 0$ on $[0, \pi]$, so it is true. Statement II: $|\vec a + \vec b|^2 - |\vec a - \vec b|^2 = 4\,\vec a\cdot\vec b > 0$, so $\vec a\cdot\vec b > 0$; e.g. $\vec a = \vec b = \hat i$. It is false.",
  "Swapping the half-angle forms for the sum and the difference of unit vectors.",
  "U12-B-statements-concept", "Two identities to verify, one with a sign trap.",
  check=_c027, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis", source_class=SC)


def _c028():
    P, Q, R = V(3, 2, 0), V(1, 1, 1), V(2, 0, 2)
    return simplify(dot(Q - P, R - P) / (mag(Q - P) * mag(R - P)))


q("U12-B-028", TOPIC, "Angle of a triangle from position vectors", "Medium", "Multi-step computation MCQ",
  r"The points $P$, $Q$, $R$ have position vectors $3\hat{i} + 2\hat{j}$, $\hat{i} + \hat{j} + \hat{k}$ and $2\hat{i} + 2\hat{k}$ respectively. Then $\cos\angle QPR$ equals",
  r"$\frac{\sqrt{6}}{3}$",
  [(r"$-\frac{\sqrt{6}}{3}$", r"Uses $\overrightarrow{QP}$ with $\overrightarrow{PR}$, one side pointing into $P$ and one out of it."),
   (r"$\frac{2}{3}$", r"Divides the dot product $6$ by $|\overrightarrow{PR}|^2 = 9$."),
   (r"$\frac{\sqrt{3}}{3}$", r"Computes the angle at $R$: $\frac{\overrightarrow{RP}\cdot\overrightarrow{RQ}}{|\overrightarrow{RP}||\overrightarrow{RQ}|} = \frac{3}{3\sqrt 3}$.")],
  r"$\overrightarrow{PQ} = -2\hat i - \hat j + \hat k$ and $\overrightarrow{PR} = -\hat i - 2\hat j + 2\hat k$. Their dot product is $2 + 2 + 2 = 6$, with $|\overrightarrow{PQ}| = \sqrt 6$ and $|\overrightarrow{PR}| = 3$. So $\cos\angle QPR = \frac{6}{3\sqrt 6} = \frac{\sqrt 6}{3}$.",
  "Using side vectors that do not both start at the vertex.",
  "U12-B-triangle-angle-position", "Two side vectors, a dot product, two magnitudes.",
  check=_c028, values=[sqrt(6) / 3, -sqrt(6) / 3, Rational(2, 3), sqrt(3) / 3], cognitive="Application", source_class=SC)


def _c029():
    F1, F2, P, Q = V(4, 1, -3), V(3, 1, -1), V(1, 2, 3), V(5, 4, 1)
    return dot(F1 + F2, Q - P)


q("U12-B-029", TOPIC, "Work done by two forces", "Medium", "Multi-step computation MCQ",
  r"Two forces $4\hat{i} + \hat{j} - 3\hat{k}$ and $3\hat{i} + \hat{j} - \hat{k}$ act together on a particle and move it from $P(1, 2, 3)$ to $Q(5, 4, 1)$. The total work done (in appropriate units) is",
  r"$40$",
  [(r"$-40$", r"Takes the displacement as $\overrightarrow{OP} - \overrightarrow{OQ}$, reversing it."),
   (r"$39$", r"Dots the resultant $7\hat i + 2\hat j - 4\hat k$ with the position vector of $Q$: $35 + 8 - 4$."),
   (r"$24$", r"Uses only the first force: $(4\hat i + \hat j - 3\hat k)\cdot(4\hat i + 2\hat j - 2\hat k) = 16 + 2 + 6$.")],
  r"The resultant is $7\hat i + 2\hat j - 4\hat k$ and the displacement is $\overrightarrow{PQ} = 4\hat i + 2\hat j - 2\hat k$. Work $= 28 + 4 + 8 = 40$.",
  "Using a position vector in place of the displacement, or only one force.",
  "U12-B-work-done", "Resultant force, displacement, dot product.",
  check=_c029, values=[40, -40, 39, 24], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Two forces $4\hat{i} + \hat{j} - 3\hat{k}$ and $3\hat{i} + \hat{j} - \hat{k}$ act together on a particle and move it from $P(1, 2, 3)$ to $Q(5, 4, 1)$. The total work done (in appropriate units) is", answer=40))


def _c030():
    c = cos(pi / 3)
    return sqrt(3 + 2 * 3 * c)


q("U12-B-030", TOPIC, "Three unit vectors at equal angles", "Medium", "Multi-step computation MCQ",
  r"If $\hat{a}$, $\hat{b}$, $\hat{c}$ are unit vectors such that the angle between each pair of them is $\frac{\pi}{3}$, then $|\hat{a} + \hat{b} + \hat{c}|$ equals",
  r"$\sqrt{6}$",
  [(r"$3$", r"Adds the magnitudes, as if all three were in the same direction."),
   (r"$\sqrt{3}$", r"Drops all the cross terms, as if the vectors were mutually perpendicular."),
   (r"$\frac{3}{\sqrt{2}}$", r"Forgets the factor $2$ on the cross terms: $3 + 3\cdot\frac{1}{2} = \frac{9}{2}$.")],
  r"$|\hat a + \hat b + \hat c|^2 = 3 + 2(\hat a\cdot\hat b + \hat b\cdot\hat c + \hat c\cdot\hat a) = 3 + 2\cdot\frac{3}{2} = 6$, so the magnitude is $\sqrt 6$.",
  "Leaving out or halving the cross terms of a squared sum of three vectors.",
  "U12-B-equal-angle-three-vectors", "Three-term expansion with given angles.",
  check=_c030, values=[sqrt(6), 3, sqrt(3), 3 / sqrt(2)], cognitive="Application", source_class=SC)


def _c031():
    a, b, c = V(1, 0, 0), V(0, 2, 0), V(0, 0, 3)
    return ang(a + b + c, c)


q("U12-B-031", TOPIC, "Angle with a sum of perpendicular vectors", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a}$, $\vec{b}$, $\vec{c}$ be mutually perpendicular vectors with $|\vec{a}| = 1$, $|\vec{b}| = 2$ and $|\vec{c}| = 3$. The angle between $\vec{a} + \vec{b} + \vec{c}$ and $\vec{c}$ is",
  r"$\cos^{-1}\frac{3}{\sqrt{14}}$",
  [(r"$\cos^{-1}\frac{1}{\sqrt{14}}$", r"Computes the angle with $\vec a$ in place of $\vec c$."),
   (r"$\cos^{-1}\frac{3}{14}$", r"Divides $9$ by $|\vec c|\,|\vec a + \vec b + \vec c|^2 = 3 \cdot 14$."),
   (r"$\frac{\pi}{3}$", r"Takes $|\vec a + \vec b + \vec c| = 1 + 2 + 3 = 6$, so $\cos\theta = \frac{9}{18}$.")],
  r"$(\vec a + \vec b + \vec c)\cdot\vec c = |\vec c|^2 = 9$ and $|\vec a + \vec b + \vec c| = \sqrt{1 + 4 + 9} = \sqrt{14}$. So $\cos\theta = \frac{9}{3\sqrt{14}} = \frac{3}{\sqrt{14}}$.",
  "Adding magnitudes of perpendicular vectors.",
  "U12-B-mutually-perp-angle", "Uses perpendicularity twice in one angle computation.",
  check=_c031, values=[acos(3 / sqrt(14)), acos(1 / sqrt(14)), acos(Rational(3, 14)), pi / 3], cognitive="Application", source_class=SC)


def _c032():
    a, b = V(2, -1, 2), V(1, 1, -1)
    return solve(dot(a + t * b, a), t)[0]


q("U12-B-032", TOPIC, "Parameter for a perpendicular combination", "Medium", "Inverse/parameter MCQ",
  r"Let $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + \hat{j} - \hat{k}$. If $\vec{a} + t\vec{b}$ is perpendicular to $\vec{a}$, then $t$ equals",
  r"$9$",
  [(r"$-9$", r"Sign slip in $\vec a\cdot\vec b$, taking it as $+1$."),
   (r"$3$", r"Uses $|\vec a| = 3$ in place of $\vec a\cdot\vec a = 9$."),
   (r"$\frac{1}{3}$", r"Imposes perpendicularity to $\vec b$: $\vec a\cdot\vec b + t|\vec b|^2 = -1 + 3t = 0$.")],
  r"$(\vec a + t\vec b)\cdot\vec a = |\vec a|^2 + t\,\vec a\cdot\vec b = 9 + t(2 - 1 - 2) = 9 - t = 0$, so $t = 9$.",
  r"Writing $\vec a\cdot\vec a$ as $|\vec a|$, or using the wrong vector for perpendicularity.",
  "U12-B-combination-perp", "Linear equation from two dot products.",
  check=_c032, values=[9, -9, 3, Rational(1, 3)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + \hat{j} - \hat{k}$. If $\vec{a} + t\vec{b}$ is perpendicular to $\vec{a}$, then the value of $t$ is", answer=9))


def _c033():
    s2 = 2 * (4 + 9) - 16
    return sqrt(s2)


q("U12-B-033", TOPIC, "Parallelogram law", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 2$, $|\vec{b}| = 3$ and $|\vec{a} + \vec{b}| = 4$, then $|\vec{a} - \vec{b}|$ equals",
  r"$\sqrt{10}$",
  [(r"$\sqrt{7}$", r"Forgets the factor $2$ in $16 = 13 + 2\,\vec a\cdot\vec b$, taking $\vec a\cdot\vec b = 3$; then $13 - 6 = 7$."),
   (r"$\sqrt{3}$", r"Computes $|\vec a + \vec b|^2 - (|\vec a|^2 + |\vec b|^2) = 3$ and takes it as $|\vec a - \vec b|^2$."),
   (r"$4$", r"Assumes $|\vec a - \vec b| = |\vec a + \vec b|$ for any two vectors.")],
  r"$|\vec a + \vec b|^2 + |\vec a - \vec b|^2 = 2(|\vec a|^2 + |\vec b|^2) = 26$, so $|\vec a - \vec b|^2 = 26 - 16 = 10$ and $|\vec a - \vec b| = \sqrt{10}$.",
  "Mishandling the cross term when moving from the sum to the difference.",
  "U12-B-parallelogram-law", "Identity or two expansions.",
  check=_c033, values=[sqrt(10), sqrt(7), sqrt(3), 4], cognitive="Application", source_class=SC)


def _c034():
    r = V(x, y, z)
    s = solve([dot(r, V(1, 1, 0)) - 3, dot(r, V(0, 1, 1)) - 5, dot(r, V(1, 0, 1)) - 4], [x, y, z], dict=True)[0]
    return dot(r, r).subs(s)


q("U12-B-034", TOPIC, "Vector from given dot products", "Medium", "Multi-step computation MCQ",
  r"A vector $\vec{r}$ satisfies $\vec{r}\cdot(\hat{i} + \hat{j}) = 3$, $\vec{r}\cdot(\hat{j} + \hat{k}) = 5$ and $\vec{r}\cdot(\hat{k} + \hat{i}) = 4$. Then $|\vec{r}|^2$ equals",
  r"$14$",
  [(r"$50$", r"Takes $3$, $5$, $4$ as the components of $\vec r$: $9 + 25 + 16$."),
   (r"$36$", r"Squares $x + y + z = 6$, which is not $x^2 + y^2 + z^2$."),
   (r"$12$", r"Adds the three given dot products, $3 + 5 + 4$, and takes the sum as $|\vec r|^2$.")],
  r"With $\vec r = x\hat i + y\hat j + z\hat k$: $x + y = 3$, $y + z = 5$, $z + x = 4$. Adding, $x + y + z = 6$, so $z = 3$, $x = 1$, $y = 2$. Hence $|\vec r|^2 = 1 + 4 + 9 = 14$.",
  "Confusing dot-product values with components.",
  "U12-B-dot-system", "Linear system from dot products, then a magnitude.",
  check=_c034, values=[14, 50, 36, 12], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A vector $\vec{r}$ satisfies $\vec{r}\cdot(\hat{i} + \hat{j}) = 3$, $\vec{r}\cdot(\hat{j} + \hat{k}) = 5$ and $\vec{r}\cdot(\hat{k} + \hat{i}) = 4$. Then the value of $|\vec{r}|^2$ is", answer=14))


def _c035():
    return solve((2 + 2 * k) - 4 * (2 - 2 * k), k)[0]


q("U12-B-035", TOPIC, "Unit vectors with a ratio of sum and difference", "Medium", "Inverse/parameter MCQ",
  r"If $\hat{a}$ and $\hat{b}$ are unit vectors inclined at an angle $\theta$ and $|\hat{a} + \hat{b}| = 2|\hat{a} - \hat{b}|$, then $\cos\theta$ equals",
  r"$\frac{3}{5}$",
  [(r"$\frac{1}{3}$", r"Squares one side only: $2 + 2\cos\theta = 2(2 - 2\cos\theta)$."),
   (r"$-\frac{3}{5}$", r"Swaps the expansions of sum and difference: $2 - 2\cos\theta = 4(2 + 2\cos\theta)$."),
   (r"$\frac{4}{5}$", r"Finds $\cos\theta = \frac{3}{5}$ and then reports $\sin\theta$.")],
  r"Squaring, $2 + 2\cos\theta = 4(2 - 2\cos\theta)$, so $10\cos\theta = 6$ and $\cos\theta = \frac{3}{5}$.",
  "Squaring only one side of a scaled equation of magnitudes.",
  "U12-B-unit-ratio-sum-diff", "Squaring both sides then a linear equation.",
  check=_c035, values=[Rational(3, 5), Rational(1, 3), Rational(-3, 5), Rational(4, 5)], cognitive="Application", source_class=SC)


def _c036():
    ab = solve(4 + k, k)[0]       # (a+b).a = |a|^2 + a.b = 0
    return sqrt(4 + 9 - 2 * ab)


q("U12-B-036", TOPIC, "Sum perpendicular to one vector", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 2$, $|\vec{b}| = 3$ and $\vec{a} + \vec{b}$ is perpendicular to $\vec{a}$, then $|\vec{a} - \vec{b}|$ equals",
  r"$\sqrt{21}$",
  [(r"$\sqrt{5}$", r"Sign slip giving $\vec a\cdot\vec b = +4$: $13 - 8 = 5$."),
   (r"$\sqrt{13}$", r"Treats $\vec a$ and $\vec b$ themselves as perpendicular."),
   (r"$\sqrt{17}$", r"Uses $|\vec a|$ in place of $|\vec a|^2$, so $\vec a\cdot\vec b = -2$ and $13 + 4 = 17$.")],
  r"$(\vec a + \vec b)\cdot\vec a = 4 + \vec a\cdot\vec b = 0$ gives $\vec a\cdot\vec b = -4$. Then $|\vec a - \vec b|^2 = 4 + 9 + 8 = 21$, so $|\vec a - \vec b| = \sqrt{21}$.",
  "Reading the perpendicularity condition as being about the original vectors.",
  "U12-B-perp-sum-magnitude", "Perpendicularity condition then an expansion.",
  check=_c036, values=[sqrt(21), sqrt(5), sqrt(13), sqrt(17)], cognitive="Application", source_class=SC)


def _c037():
    ab = solve(2 * 4 - k + 6 * k - 3 * 1, k)[0]
    return acos(ab / (2 * 1))


q("U12-B-037", TOPIC, "Angle from a perpendicularity condition", "Medium", "Inverse/parameter MCQ",
  r"If $|\vec{a}| = 2$, $|\vec{b}| = 1$ and $\vec{a} + 3\vec{b}$ is perpendicular to $2\vec{a} - \vec{b}$, then the angle between $\vec{a}$ and $\vec{b}$ is",
  r"$\frac{2\pi}{3}$",
  [(r"$\frac{\pi}{3}$", r"Takes the cross terms as $+\vec a\cdot\vec b - 6\,\vec a\cdot\vec b$, so $5 - 5\,\vec a\cdot\vec b = 0$ and $\vec a\cdot\vec b = 1$."),
   (r"$\cos^{-1}\left(-\frac{5}{14}\right)$", r"Combines $-\vec a\cdot\vec b$ and $6\,\vec a\cdot\vec b$ as $7\,\vec a\cdot\vec b$: $5 + 7\,\vec a\cdot\vec b = 0$."),
   (r"$\cos^{-1}\left(-\frac{1}{10}\right)$", r"Uses $|\vec a| = 2$ in place of $|\vec a|^2 = 4$: $4 + 5\,\vec a\cdot\vec b - 3 = 0$.")],
  r"$(\vec a + 3\vec b)\cdot(2\vec a - \vec b) = 2|\vec a|^2 + 5\,\vec a\cdot\vec b - 3|\vec b|^2 = 8 + 5\,\vec a\cdot\vec b - 3 = 0$, so $\vec a\cdot\vec b = -1$ and $\cos\theta = \frac{-1}{2} $, giving $\theta = \frac{2\pi}{3}$.",
  "Collecting the mixed terms of a product of combinations with the wrong coefficient.",
  "U12-B-perp-combination-angle", "Expansion of a product of combinations, then angle.",
  check=_c037, values=[2 * pi / 3, pi / 3, acos(Rational(-5, 14)), acos(Rational(-1, 10))], cognitive="Application", source_class=SC)


def _c038():
    A, B, proj = 3, 4, 2
    ab = proj * A
    return sqrt(A**2 + B**2 - 2 * ab)


q("U12-B-038", TOPIC, "Magnitude from a given projection", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and the scalar projection of $\vec{b}$ on $\vec{a}$ is $2$, then $|\vec{a} - \vec{b}|$ equals",
  r"$\sqrt{13}$",
  [(r"$\sqrt{21}$", r"Takes $\vec a\cdot\vec b$ equal to the projection $2$, without multiplying by $|\vec a|$: $25 - 4$."),
   (r"$3$", r"Multiplies the projection by $|\vec b|$, so $\vec a\cdot\vec b = 8$ and $25 - 16 = 9$."),
   (r"$\sqrt{37}$", r"Sign slip: $25 + 12 = 37$.")],
  r"The projection of $\vec b$ on $\vec a$ is $\frac{\vec a\cdot\vec b}{|\vec a|} = 2$, so $\vec a\cdot\vec b = 6$. Then $|\vec a - \vec b|^2 = 9 + 16 - 12 = 13$.",
  "Using the wrong magnitude to recover the dot product from a projection.",
  "U12-B-projection-to-magnitude", "Inverting the projection and then expanding.",
  check=_c038, values=[sqrt(13), sqrt(21), 3, sqrt(37)], cognitive="Application", source_class=SC)


def _c039():
    ab = solve(2 + 2 * k - 3, k)[0]
    return expand(6 * 1 + 2 * ab - 15 * ab - 5 * 1)


q("U12-B-039", TOPIC, "Dot product of two combinations", "Medium", "Multi-step computation MCQ",
  r"If $\hat{a}$ and $\hat{b}$ are unit vectors with $|\hat{a} + \hat{b}| = \sqrt{3}$, then $(2\hat{a} - 5\hat{b})\cdot(3\hat{a} + \hat{b})$ equals",
  r"$-\frac{11}{2}$",
  [(r"$\frac{15}{2}$", r"Sign slip giving $\hat a\cdot\hat b = -\frac{1}{2}$: $1 + \frac{13}{2}$."),
   (r"$1$", r"Drops the mixed terms, keeping only $6 - 5$."),
   (r"$-\frac{15}{2}$", r"Collects the mixed terms as $-17\,\hat a\cdot\hat b$ in place of $-13\,\hat a\cdot\hat b$.")],
  r"From $3 = 2 + 2\,\hat a\cdot\hat b$, $\hat a\cdot\hat b = \frac{1}{2}$. Then $(2\hat a - 5\hat b)\cdot(3\hat a + \hat b) = 6 + 2\,\hat a\cdot\hat b - 15\,\hat a\cdot\hat b - 5 = 1 - 13\cdot\frac{1}{2} = -\frac{11}{2}$.",
  "Sign errors in the mixed terms of a product of combinations.",
  "U12-B-expansion-dot", "Find the dot product, then a four-term expansion.",
  check=_c039, values=[Rational(-11, 2), Rational(15, 2), 1, Rational(-15, 2)], cognitive="Application", source_class=SC)


def _c040():
    A, B, C = 1, 2, 3
    c = cos(pi / 3)
    return sqrt(A**2 + B**2 + C**2 + 2 * (A * B + B * C + C * A) * c)


q("U12-B-040", TOPIC, "Three vectors at given angles", "Medium", "Multi-step computation MCQ",
  r"If $|\vec{a}| = 1$, $|\vec{b}| = 2$, $|\vec{c}| = 3$ and the angle between each pair of these vectors is $\frac{\pi}{3}$, then $|\vec{a} + \vec{b} + \vec{c}|$ equals",
  r"$5$",
  [(r"$6$", r"Adds the magnitudes, as if the vectors were in the same direction."),
   (r"$\sqrt{14}$", r"Drops the cross terms, as if the vectors were mutually perpendicular."),
   (r"$\sqrt{\frac{39}{2}}$", r"Forgets the factor $2$ on the cross terms: $14 + \frac{11}{2}$.")],
  r"$\vec a\cdot\vec b = 1$, $\vec b\cdot\vec c = 3$, $\vec c\cdot\vec a = \frac{3}{2}$. So $|\vec a + \vec b + \vec c|^2 = 1 + 4 + 9 + 2\left(1 + 3 + \frac{3}{2}\right) = 25$, giving $5$.",
  "Leaving out the factor $2$ on the cross terms.",
  "U12-B-equal-angle-three-vectors", "Three different dot products in one expansion.",
  check=_c040, values=[5, 6, sqrt(14), sqrt(Rational(39, 2))], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $|\vec{a}| = 1$, $|\vec{b}| = 2$, $|\vec{c}| = 3$ and the angle between each pair of these vectors is $\frac{\pi}{3}$, then the value of $|\vec{a} + \vec{b} + \vec{c}|$ is", answer=5))

# ================================================================ DIFFICULT (13)


def _c041():
    a = Matrix(symbols('a1:4')); b = Matrix(symbols('b1:4')); c = Matrix(symbols('c1:4'))
    S = dot(a - b, a - b) + dot(b - c, b - c) + dot(c - a, c - a)
    ident = expand(S + dot(a + b + c, a + b + c) - 3 * (dot(a, a) + dot(b, b) + dot(c, c)))
    assert ident == 0
    # S = 9 - |a+b+c|^2 <= 9 for unit vectors; attained when a+b+c = 0
    ex = {a[0]: 1, a[1]: 0, a[2]: 0, b[0]: Rational(-1, 2), b[1]: sqrt(3) / 2, b[2]: 0,
          c[0]: Rational(-1, 2), c[1]: -sqrt(3) / 2, c[2]: 0}
    return simplify(S.subs(ex))


q("U12-B-041", TOPIC, "Extremum of a sum of squared distances", "Difficult", "Conceptual/application MCQ",
  r"If $\hat{a}$, $\hat{b}$, $\hat{c}$ are unit vectors, then the maximum value of $|\hat{a} - \hat{b}|^2 + |\hat{b} - \hat{c}|^2 + |\hat{c} - \hat{a}|^2$ is",
  r"$9$",
  [(r"$12$", r"Takes each term at its own maximum $4$, but no three unit vectors can be pairwise opposite."),
   (r"$6$", r"Assumes the pairwise dot products cannot be negative in total, so the maximum is at mutually perpendicular vectors."),
   (r"$\frac{15}{2}$", r"Forgets the factor $2$: writes the sum as $6 - (\hat a\cdot\hat b + \hat b\cdot\hat c + \hat c\cdot\hat a)$ and uses the lower bound $-\frac{3}{2}$.")],
  r"The sum equals $6 - 2(\hat a\cdot\hat b + \hat b\cdot\hat c + \hat c\cdot\hat a)$. Since $|\hat a + \hat b + \hat c|^2 = 3 + 2(\hat a\cdot\hat b + \hat b\cdot\hat c + \hat c\cdot\hat a) \ge 0$, the sum equals $9 - |\hat a + \hat b + \hat c|^2 \le 9$. Equality holds when $\hat a + \hat b + \hat c = \vec 0$ (three coplanar unit vectors at $120^\circ$ to each other).",
  "Maximising each term separately when the terms are linked.",
  "U12-B-extremum-dot-sums", r"Needs the identity with $|\hat a + \hat b + \hat c|^2$ and an attainability check.",
  check=_c041, values=[9, 12, 6, Rational(15, 2)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"If $\hat{a}$, $\hat{b}$, $\hat{c}$ are unit vectors, then the maximum value of $|\hat{a} - \hat{b}|^2 + |\hat{b} - \hat{c}|^2 + |\hat{c} - \hat{a}|^2$ is", answer=9))


def _c042():
    X, Y, Z = symbols('X Y Z')   # X = a.b, Y = b.c, Z = c.a
    s = solve([X + Z, Y + X, Z + Y], [X, Y, Z])
    return sqrt(1 + 4 + 9 + 2 * (s[X] + s[Y] + s[Z]))


q("U12-B-042", TOPIC, "Each vector perpendicular to the sum of the others", "Difficult", "Multi-step computation MCQ",
  r"Let $|\vec{a}| = 1$, $|\vec{b}| = 2$ and $|\vec{c}| = 3$. If each of $\vec{a}$, $\vec{b}$, $\vec{c}$ is perpendicular to the sum of the other two, then $|\vec{a} + \vec{b} + \vec{c}|$ equals",
  r"$\sqrt{14}$",
  [(r"$6$", r"Adds the magnitudes $1 + 2 + 3$."),
   (r"$14$", r"Finds $|\vec a + \vec b + \vec c|^2 = 14$ and reports it as the magnitude."),
   (r"$\sqrt{6}$", r"Takes the square root of $|\vec a| + |\vec b| + |\vec c| = 6$, mixing magnitudes with squared magnitudes.")],
  r"The conditions are $\vec a\cdot\vec b + \vec a\cdot\vec c = 0$, $\vec b\cdot\vec c + \vec b\cdot\vec a = 0$, $\vec c\cdot\vec a + \vec c\cdot\vec b = 0$. Adding, $\vec a\cdot\vec b + \vec b\cdot\vec c + \vec c\cdot\vec a = 0$. So $|\vec a + \vec b + \vec c|^2 = 1 + 4 + 9 + 0 = 14$ and the magnitude is $\sqrt{14}$.",
  "Not combining the three conditions into one statement about the sum of dot products.",
  "U12-B-perp-to-sum-of-others", "Combine three conditions, then expand.",
  check=_c042, values=[sqrt(14), 6, 14, sqrt(6)], cognitive="Analysis", source_class=SC)


def _c043():
    a, b = V(lam, 1, 2), V(1, lam, 2)
    S = solve_univariate_inequality(dot(a, b) > 0, lam, relational=False)
    par = [d[lam] for d in solve(list(a - k * b), [lam, k], dict=True) if d[k] > 0]
    return Complement(S, FiniteSet(*par))


q("U12-B-043", TOPIC, "Parameter range for an acute angle", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real $\lambda$ for which the angle $\theta$ between $\vec{a} = \lambda\hat{i} + \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} + \lambda\hat{j} + 2\hat{k}$ satisfies $0 < \theta < \frac{\pi}{2}$ is",
  r"$(-2, 1) \cup (1, \infty)$",
  [(r"$(-2, \infty)$", r"Solves $\vec a\cdot\vec b > 0$ only and keeps $\lambda = 1$, where $\vec a = \vec b$ and $\theta = 0$."),
   (r"$[-2, 1) \cup (1, \infty)$", r"Includes $\lambda = -2$, where $\vec a\cdot\vec b = 0$ and $\theta = \frac{\pi}{2}$."),
   (r"$(-\infty, -2)$", r"Reverses the inequality and solves $2\lambda + 4 < 0$.")],
  r"$\vec a\cdot\vec b = \lambda + \lambda + 4 = 2\lambda + 4 > 0$ gives $\lambda > -2$. We must also exclude $\theta = 0$: $\vec a = k\vec b$ with $k > 0$ forces $k = 1$ (from the $\hat k$ components) and $\lambda = 1$. So the set is $(-2, 1) \cup (1, \infty)$.",
  r"Forgetting that $\vec a\cdot\vec b > 0$ also allows $\theta = 0$.",
  "U12-B-angle-sign-range", "Inequality plus an exclusion for parallel vectors.",
  check=_c043, values=[Union(Interval.open(-2, 1), Interval.open(1, oo)), Interval.open(-2, oo), Union(Interval.Ropen(-2, 1), Interval.open(1, oo)), Interval.open(-oo, -2)],
  cognitive="Analysis", source_class=SC)


def _c044():
    A, B, C = 2, 3, 4
    bc = solve(B**2 + C**2 + 2 * k - A**2, k)[0]     # a = -(b + c)
    return acos(bc / (B * C))


q("U12-B-044", TOPIC, "Three vectors with zero sum", "Difficult", "Multi-step computation MCQ",
  r"If $\vec{a} + \vec{b} + \vec{c} = \vec{0}$ with $|\vec{a}| = 2$, $|\vec{b}| = 3$ and $|\vec{c}| = 4$, then the angle between $\vec{b}$ and $\vec{c}$ is",
  r"$\cos^{-1}\left(-\frac{7}{8}\right)$",
  [(r"$\cos^{-1}\frac{7}{8}$", r"Uses the cosine rule for the interior angle of the triangle with sides $2$, $3$, $4$; that is the angle between $\vec b$ and $-\vec c$."),
   (r"$\cos^{-1}\left(-\frac{11}{16}\right)$", r"Computes the angle between $\vec c$ and $\vec a$: from $\vec b = -(\vec c + \vec a)$, $\vec c\cdot\vec a = -\frac{11}{2}$, then divides by $8$."),
   (r"$\cos^{-1}\frac{1}{4}$", r"Computes the angle between $\vec a$ and $\vec b$: $\vec a\cdot\vec b = \frac{3}{2}$, divided by $6$.")],
  r"Write $\vec a = -(\vec b + \vec c)$. Then $4 = 9 + 16 + 2\,\vec b\cdot\vec c$, so $\vec b\cdot\vec c = -\frac{21}{2}$ and $\cos\theta = \frac{-21/2}{12} = -\frac{7}{8}$.",
  "Confusing the angle between vectors with the triangle's interior angle, or isolating the wrong vector.",
  "U12-B-sum-zero-angle", "Choose which vector to isolate; sign trap with the triangle angle.",
  check=_c044, values=[acos(Rational(-7, 8)), acos(Rational(7, 8)), acos(Rational(-11, 16)), acos(Rational(1, 4))], cognitive="Analysis", source_class=SC)


def _c045():
    a, b = V(lam, 1, -1), V(1, 2, 2)
    f = dot(a + t * b, a + t * b)
    t0 = solve(diff(f, t), t)[0]
    fmin = simplify(f.subs(t, t0))
    return [s for s in solve(fmin - 18, lam) if s > 0][0]


q("U12-B-045", TOPIC, "Parameter from the least magnitude of a one-parameter family", "Difficult", "Inverse/parameter MCQ",
  r"Let $\vec{a} = \lambda\hat{i} + \hat{j} - \hat{k}$, where $\lambda > 0$, and $\vec{b} = \hat{i} + 2\hat{j} + 2\hat{k}$. If the least value of $|\vec{a} + t\vec{b}|$ as $t$ varies over the real numbers is $3\sqrt{2}$, then $\lambda$ equals",
  r"$3\sqrt{2}$",
  [(r"$4$", r"Assumes the least value occurs at $t = 0$, so sets $|\vec a|^2 = \lambda^2 + 2 = 18$."),
   (r"$2\sqrt{6}$", r"Divides $(\vec a\cdot\vec b)^2 = \lambda^2$ by $|\vec b| = 3$ in place of $|\vec b|^2 = 9$: $\lambda^2 + 2 - \frac{\lambda^2}{3} = 18$ gives $\lambda^2 = 24$."),
   (r"$2\sqrt{3}$", r"Sign slip in the minimiser, taking $t = +\frac{\lambda}{9}$: $\lambda^2 + 2 + \frac{2\lambda^2}{9} + \frac{\lambda^2}{9} = 18$ gives $\lambda^2 = 12$.")],
  r"$\vec a\cdot\vec b = \lambda + 2 - 2 = \lambda$, $|\vec a|^2 = \lambda^2 + 2$ and $|\vec b|^2 = 9$, so $|\vec a + t\vec b|^2 = 9t^2 + 2\lambda t + \lambda^2 + 2$. This is least at $t = -\frac{\lambda}{9}$, where it equals $\lambda^2 + 2 - \frac{\lambda^2}{9} = \frac{8\lambda^2}{9} + 2$. Setting this equal to $18$ gives $\lambda^2 = 18$, and since $\lambda > 0$, $\lambda = 3\sqrt 2$.",
  r"Taking the least value of $|\vec a + t\vec b|$ to be $|\vec a|$, or mis-locating the minimiser of the quadratic in $t$.",
  "U12-B-least-magnitude-inverse", r"Reverse problem: build the quadratic in $t$ with a parameter, minimise it, then solve for the parameter with a sign condition.",
  check=_c045, values=[3 * sqrt(2), 4, 2 * sqrt(6), 2 * sqrt(3)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $\vec{a} = \lambda\hat{i} + \hat{j} - \hat{k}$, where $\lambda > 0$, and $\vec{b} = \hat{i} + 2\hat{j} + 2\hat{k}$. If the least value of $|\vec{a} + t\vec{b}|$ as $t$ varies over the real numbers is $3\sqrt{2}$, then the value of $\lambda^2$ is", answer=18))


def _c046():
    X = symbols('X')
    s1 = solve(3 + 2 * X, X)[0] == Rational(-3, 2)
    th = symbols('th', real=True)
    S = solve_univariate_inequality(2 + 2 * cos(th) > 1, th, relational=False, domain=Interval(0, pi))
    s2 = S == Interval.Ropen(0, 2 * pi / 3)
    return (bool(s1), bool(s2))


q("U12-B-046", TOPIC, "Unit vector configurations", "Difficult", "Statement-based MCQ",
  r"Statement I: If $\hat{a}$, $\hat{b}$, $\hat{c}$ are unit vectors with $\hat{a} + \hat{b} + \hat{c} = \vec{0}$, then $\hat{a}\cdot\hat{b} + \hat{b}\cdot\hat{c} + \hat{c}\cdot\hat{a} = -\frac{3}{2}$. Statement II: If $\hat{a}$ and $\hat{b}$ are unit vectors inclined at an angle $\theta \in [0, \pi]$, then $|\hat{a} + \hat{b}| > 1$ if and only if $0 \le \theta < \frac{2\pi}{3}$." + TAIL,
  ST_TT,
  [(ST_FF, r"Forgets the factor $2$ in $|\hat a + \hat b + \hat c|^2$ (getting $-3$) and solves $2 + 2\cos\theta > 1$ with the inequality reversed."),
   (ST_TF, r"Solves $\cos\theta > -\frac{1}{2}$ as $\theta < \frac{\pi}{3}$, taking the reference angle in place of $\frac{2\pi}{3}$."),
   (ST_FT, r"Forgets the factor $2$ in Statement I, getting $\hat a\cdot\hat b + \hat b\cdot\hat c + \hat c\cdot\hat a = -3$.")],
  r"Statement I: $0 = |\hat a + \hat b + \hat c|^2 = 3 + 2(\hat a\cdot\hat b + \hat b\cdot\hat c + \hat c\cdot\hat a)$, so the sum is $-\frac{3}{2}$; true. Statement II: $|\hat a + \hat b|^2 = 2 + 2\cos\theta > 1$ iff $\cos\theta > -\frac{1}{2}$ iff $0 \le \theta < \frac{2\pi}{3}$ on $[0, \pi]$; true.",
  "Solving a cosine inequality with the reference angle in the wrong quadrant.",
  "U12-B-statements-compute", "Two independent arguments, one an inequality on an interval.",
  check=_c046, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis", source_class=SC)


def _c047():
    a, b = V(2, 1, -2), V(lam, 1, 1)
    sols = solve(dot(a, b) / mag(b) - dot(a, b) / mag(a), lam)
    sols = list(set(simplify(s) for s in sols))
    return nsimplify(simplify(sum(sols)))


q("U12-B-047", TOPIC, "Equal mutual projections", "Difficult", "Inverse/parameter MCQ",
  r"Let $\vec{a} = 2\hat{i} + \hat{j} - 2\hat{k}$ and $\vec{b} = \lambda\hat{i} + \hat{j} + \hat{k}$, $\lambda \in \mathbb{R}$. If the scalar projection of $\vec{a}$ on $\vec{b}$ equals the scalar projection of $\vec{b}$ on $\vec{a}$, then the sum of all possible values of $\lambda$ is",
  r"$\frac{1}{2}$",
  [(r"$0$", r"Cancels $\vec a\cdot\vec b$ to get $|\vec a| = |\vec b|$ only, losing the case $\vec a\cdot\vec b = 0$; then $\sqrt 7 + (-\sqrt 7) = 0$."),
   (r"$\frac{1}{2} + \sqrt{7}$", r"Keeps both cases but takes only the positive root of $\lambda^2 = 7$."),
   (r"$-\frac{3}{2}$", r"Sign slip in the $\hat k$ product, so $\vec a\cdot\vec b = 2\lambda + 3$ and the perpendicular case gives $\lambda = -\frac{3}{2}$; adding $\pm\sqrt 7$ gives $-\frac{3}{2}$.")],
  r"The condition is $\frac{\vec a\cdot\vec b}{|\vec b|} = \frac{\vec a\cdot\vec b}{|\vec a|}$, i.e. $\vec a\cdot\vec b = 0$ or $|\vec a| = |\vec b|$. Here $\vec a\cdot\vec b = 2\lambda - 1$, giving $\lambda = \frac{1}{2}$; and $|\vec b|^2 = \lambda^2 + 2 = 9$ gives $\lambda = \pm\sqrt 7$. The sum is $\frac{1}{2} + \sqrt 7 - \sqrt 7 = \frac{1}{2}$.",
  "Cancelling a quantity that may be zero.",
  "U12-B-equal-projection-casework", "Casework trap from cancelling a possibly zero factor.",
  check=_c047, values=[Rational(1, 2), 0, Rational(1, 2) + sqrt(7), Rational(-3, 2)], cognitive="Analysis", source_class=SC)


def _c048():
    a = V(2, -1, 2)
    m = symbols('m', positive=True)              # m = |c|, and a.c = m
    eq = m**2 - 2 * m + dot(a, a) - 13           # |c - a|^2 = |c|^2 - 2 a.c + |a|^2
    return solve(eq, m)[0]


q("U12-B-048", TOPIC, "Magnitude from mixed conditions", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and let $\vec{c}$ be a non-zero vector such that $\vec{a}\cdot\vec{c} = |\vec{c}|$ and $|\vec{c} - \vec{a}| = \sqrt{13}$. Then $|\vec{c}|$ equals",
  r"$1 + \sqrt{5}$",
  [(r"$\frac{1 + \sqrt{17}}{2}$", r"Forgets the factor $2$ in the cross term: $|\vec c|^2 - |\vec c| + 9 = 13$."),
   (r"$\sqrt{5} - 1$", r"Sign slip in the cross term: $|\vec c|^2 + 2|\vec c| + 9 = 13$."),
   (r"$1 + \sqrt{11}$", r"Uses $|\vec a| = 3$ in place of $|\vec a|^2 = 9$: $|\vec c|^2 - 2|\vec c| + 3 = 13$.")],
  r"$|\vec c - \vec a|^2 = |\vec c|^2 - 2\,\vec a\cdot\vec c + |\vec a|^2 = |\vec c|^2 - 2|\vec c| + 9 = 13$. So $|\vec c|^2 - 2|\vec c| - 4 = 0$ and, taking the positive root, $|\vec c| = 1 + \sqrt 5$.",
  r"Mishandling the cross term when the dot product is given in terms of $|\vec c|$.",
  "U12-B-dot-equals-magnitude", "Substitute a dot condition into an expansion, then a quadratic with a sign choice.",
  check=_c048, values=[1 + sqrt(5), (1 + sqrt(17)) / 2, sqrt(5) - 1, 1 + sqrt(11)], cognitive="Analysis", source_class=SC)


def _c049():
    u1, u2 = V(1, 2, 2), V(2, -3, 6)
    F = 6 * u1 / mag(u1) + 14 * u2 / mag(u2)
    P, Q = V(1, 1, 1), V(3, 4, 2)
    return dot(F, Q - P)


q("U12-B-049", TOPIC, "Work done by forces given by magnitude and direction", "Difficult", "Multi-step computation MCQ",
  r"A force of magnitude $6$ along $\hat{i} + 2\hat{j} + 2\hat{k}$ and a force of magnitude $14$ along $2\hat{i} - 3\hat{j} + 6\hat{k}$ act together on a particle and move it from $P(1, 1, 1)$ to $Q(3, 4, 2)$. The total work done (in appropriate units) is",
  r"$22$",
  [(r"$11$", r"Uses the direction vectors themselves as the forces, without scaling to the given magnitudes."),
   (r"$42$", r"Dots the resultant $6\hat i - 2\hat j + 16\hat k$ with the position vector of $Q$ in place of $\overrightarrow{PQ}$."),
   (r"$74$", r"Multiplies each direction vector by its magnitude without first making it a unit vector: $34\hat i - 30\hat j + 96\hat k$.")],
  r"The forces are $6\cdot\frac{\hat i + 2\hat j + 2\hat k}{3} = 2\hat i + 4\hat j + 4\hat k$ and $14\cdot\frac{2\hat i - 3\hat j + 6\hat k}{7} = 4\hat i - 6\hat j + 12\hat k$, with resultant $6\hat i - 2\hat j + 16\hat k$. The displacement is $2\hat i + 3\hat j + \hat k$, so the work is $12 - 6 + 16 = 22$.",
  "Not converting a direction into a unit vector before scaling to the given magnitude.",
  "U12-B-work-done", "Unit vectors, resultant, displacement and dot product with several traps.",
  check=_c049, values=[22, 11, 42, 74], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A force of magnitude $6$ along $\hat{i} + 2\hat{j} + 2\hat{k}$ and a force of magnitude $14$ along $2\hat{i} - 3\hat{j} + 6\hat{k}$ act together on a particle and move it from $P(1, 1, 1)$ to $Q(3, 4, 2)$. The total work done (in appropriate units) is", answer=22))


def _c050():
    c = symbols('c', real=True)
    allowed = solve_univariate_inequality(2 + 2 * c >= 2, c, relational=False, domain=Interval(-1, 1))
    return imageset(Lambda(c, sqrt(2 - 2 * c)), allowed)


q("U12-B-050", TOPIC, "Range of the magnitude of a difference", "Difficult", "Inverse/parameter MCQ",
  r"If $\hat{a}$ and $\hat{b}$ are unit vectors such that $|\hat{a} + \hat{b}| \ge \sqrt{2}$, then the set of all possible values of $|\hat{a} - \hat{b}|$ is",
  r"$[0, \sqrt{2}]$",
  [(r"$[\sqrt{2}, 2]$", r"Reverses the inequality when passing to the difference, taking $|\hat a - \hat b| \ge \sqrt 2$."),
   (r"$[0, 2]$", r"Ignores the condition and gives the range for all pairs of unit vectors."),
   (r"$[0, 2 - \sqrt{2}]$", r"Uses $|\hat a + \hat b| + |\hat a - \hat b| = 2$ in place of $|\hat a + \hat b|^2 + |\hat a - \hat b|^2 = 4$.")],
  r"$|\hat a + \hat b|^2 + |\hat a - \hat b|^2 = 4$. The condition $|\hat a + \hat b|^2 \ge 2$ gives $|\hat a - \hat b|^2 \le 2$. Writing $\cos\theta \in [0, 1]$, $|\hat a - \hat b| = \sqrt{2 - 2\cos\theta}$ takes every value in $[0, \sqrt 2]$ ($0$ when $\hat a = \hat b$).",
  "Adding magnitudes where squared magnitudes add.",
  "U12-B-sum-diff-range", "Identity, inequality and the full range check.",
  check=_c050, values=[Interval(0, sqrt(2)), Interval(sqrt(2), 2), Interval(0, 2), Interval(0, 2 - sqrt(2))], cognitive="Analysis", source_class=SC)


def _c051():
    al, be = symbols('alpha beta', real=True)
    a, b, c = V(al, 3, -1), V(4, -be, 1), V(1, 2, -2)
    s = solve([dot(a, c) / mag(c) - Rational(10, 3), dot(b, c)], [al, be], dict=True)[0]
    d = (a - b).subs(s)
    return dot(d, d)


q("U12-B-051", TOPIC, "Two parameters from projection and perpendicularity", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{a} = \alpha\hat{i} + 3\hat{j} - \hat{k}$, $\vec{b} = 4\hat{i} - \beta\hat{j} + \hat{k}$ and $\vec{c} = \hat{i} + 2\hat{j} - 2\hat{k}$. If the scalar projection of $\vec{a}$ on $\vec{c}$ is $\frac{10}{3}$ and $\vec{b}$ is perpendicular to $\vec{c}$, then $|\vec{a} - \vec{b}|^2$ equals",
  r"$24$",
  [(r"$344$", r"Divides by $|\vec c|^2 = 9$ in the projection, so $\alpha + 8 = 30$ and $\alpha = 22$."),
   (r"$12$", r"Sign slip in $\vec b\cdot\vec c$, solving $4 + 2\beta - 2 = 0$ to get $\beta = -1$."),
   (r"$20$", r"Leaves out the $\hat k$ product in $\vec a\cdot\vec c$, so $\alpha + 6 = 10$ and $\alpha = 4$.")],
  r"$|\vec c| = 3$, so $\frac{\alpha + 6 + 2}{3} = \frac{10}{3}$ gives $\alpha = 2$. Also $\vec b\cdot\vec c = 4 - 2\beta - 2 = 0$ gives $\beta = 1$. Then $\vec a - \vec b = -2\hat i + 4\hat j - 2\hat k$ and $|\vec a - \vec b|^2 = 4 + 16 + 4 = 24$.",
  "Wrong normaliser in the projection, or sign slips with a negative parameter coefficient.",
  "U12-B-projection-perp-two-params", "Two conditions give two parameters, then a magnitude.",
  check=_c051, values=[24, 344, 12, 20], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $\vec{a} = \alpha\hat{i} + 3\hat{j} - \hat{k}$, $\vec{b} = 4\hat{i} - \beta\hat{j} + \hat{k}$ and $\vec{c} = \hat{i} + 2\hat{j} - 2\hat{k}$. If the scalar projection of $\vec{a}$ on $\vec{c}$ is $\frac{10}{3}$ and $\vec{b}$ is perpendicular to $\vec{c}$, then the value of $|\vec{a} - \vec{b}|^2$ is", answer=24))


def _c052():
    X = symbols('X')                    # X = a.b
    f = 4 - 2 * t * X + t**2            # |a - t b|^2 with |a| = 2, |b| = 1
    tmin = solve(diff(f, t), t)[0]      # minimiser
    ab = solve(tmin - 1, X)[0]          # minimum must occur at t = 1
    return acos(ab / 2)


q("U12-B-052", TOPIC, "Angle from a minimum condition", "Difficult", "Inverse/parameter MCQ",
  r"Let $|\vec{a}| = 2$ and $|\vec{b}| = 1$. If $|\vec{a} - \vec{b}| \le |\vec{a} - t\vec{b}|$ for every real number $t$, then the angle between $\vec{a}$ and $\vec{b}$ is",
  r"$\frac{\pi}{3}$",
  [(r"$\frac{\pi}{2}$", r"Assumes the minimum of $|\vec a - t\vec b|$ is always at $t = 0$ and reads the condition as $\vec a \perp \vec b$."),
   (r"$\frac{2\pi}{3}$", r"Sign slip in the minimiser, taking $t = -\vec a\cdot\vec b$, so $\vec a\cdot\vec b = -1$."),
   (r"$\cos^{-1}\frac{1}{4}$", r"Finds $\vec a\cdot\vec b = 1$ but divides by $|\vec a|^2|\vec b| = 4$ in place of $|\vec a||\vec b| = 2$.")],
  r"$|\vec a - t\vec b|^2 = 4 - 2t\,(\vec a\cdot\vec b) + t^2$ is a quadratic in $t$ with minimum at $t = \vec a\cdot\vec b$. The condition says the minimum is at $t = 1$, so $\vec a\cdot\vec b = 1$ and $\cos\theta = \frac{1}{2}$, i.e. $\theta = \frac{\pi}{3}$.",
  "Not converting a 'for all t' condition into the location of the minimum of a quadratic.",
  "U12-B-min-condition-angle", "Turn an inequality for all t into a vertex condition, then an angle.",
  check=_c052, values=[pi / 3, pi / 2, 2 * pi / 3, acos(Rational(1, 4))], cognitive="Analysis", source_class=SC)


def _c053():
    a = Matrix(symbols('a1:4')); b = Matrix(symbols('b1:4')); c = Matrix(symbols('c1:4'))
    S = dot(a, b) + dot(b, c) + dot(c, a)
    ident = expand(2 * S - (dot(a + b + c, a + b + c) - dot(a, a) - dot(b, b) - dot(c, c)))
    assert ident == 0
    # S = (|a+b+c|^2 - 14)/2 >= -7; attained by a = i, b = 2i, c = -3i
    ex = {a[0]: 1, a[1]: 0, a[2]: 0, b[0]: 2, b[1]: 0, b[2]: 0, c[0]: -3, c[1]: 0, c[2]: 0}
    return S.subs(ex)


q("U12-B-053", TOPIC, "Minimum of a sum of dot products", "Difficult", "Conceptual/application MCQ",
  r"If $|\vec{a}| = 1$, $|\vec{b}| = 2$ and $|\vec{c}| = 3$, then the minimum value of $\vec{a}\cdot\vec{b} + \vec{b}\cdot\vec{c} + \vec{c}\cdot\vec{a}$ is",
  r"$-7$",
  [(r"$-11$", r"Takes each dot product at its own minimum, $-(2 + 6 + 3)$, but the three pairs cannot all be opposite."),
   (r"$-14$", r"Uses $|\vec a + \vec b + \vec c|^2 \ge 0$ but forgets to halve: writes the sum as $\ge -(1 + 4 + 9)$."),
   (r"$0$", r"Assumes the minimum occurs when the vectors are mutually perpendicular.")],
  r"$0 \le |\vec a + \vec b + \vec c|^2 = 14 + 2(\vec a\cdot\vec b + \vec b\cdot\vec c + \vec c\cdot\vec a)$, so the sum is at least $-7$. It equals $-7$ when $\vec a + \vec b + \vec c = \vec 0$, e.g. $\vec a = \hat i$, $\vec b = 2\hat i$, $\vec c = -3\hat i$, which is possible because $1 + 2 = 3$.",
  "Minimising each term separately; or not checking that the bound is attained.",
  "U12-B-extremum-dot-sums", "Identity, a bound, and an attainability argument.",
  check=_c053, values=[-7, -11, -14, 0], cognitive="Analysis", source_class=SC)
