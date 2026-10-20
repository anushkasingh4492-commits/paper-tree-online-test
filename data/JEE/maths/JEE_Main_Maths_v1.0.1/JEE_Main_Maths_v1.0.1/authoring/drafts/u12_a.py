import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools

# ---------------------------------------------------------------- helpers
SC = "XII"
TOPIC = "Vector algebra"

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."


def V(*c):
    return Matrix([nsimplify(x) for x in c])


def mag(v):
    return sqrt(sum(x**2 for x in v))


def tup(v):
    return tuple(simplify(x) for x in v)


def R_(*c):
    return tuple(nsimplify(x) for x in c)


def collinear(*pts):
    """True if all the given column vectors lie on one line."""
    d = [p - pts[0] for p in pts[1:]]
    M = Matrix.hstack(*d)
    return M.rank() <= 1


def sec_int(p, q, m, n):
    """point dividing PQ internally with PR:RQ = m:n"""
    return (m*q + n*p) / (m + n)


def sec_ext(p, q, m, n):
    """point dividing PQ externally with PR:RQ = m:n"""
    return (m*q - n*p) / (m - n)


lam, mu, k_, t_, x_, y_, z_, s_, u_ = symbols('lambda mu k t x y z s u', real=True)

# ================================================================ EASY (16)


def _c001():
    a, b = V(2, -1, 2), V(-1, 3, 1)
    w = a + b
    return tup(w / mag(w))


q("U12-A-001", TOPIC, "Unit vector along a sum", "Easy", "Single-step computation MCQ",
  r"If $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = -\hat{i} + 3\hat{j} + \hat{k}$, then the unit vector in the direction of $\vec{a} + \vec{b}$ is",
  r"$\frac{1}{\sqrt{14}}(\hat{i}+2\hat{j}+3\hat{k})$",
  [(r"$\frac{1}{14}(\hat{i}+2\hat{j}+3\hat{k})$", r"Divides $\vec{a}+\vec{b} = \hat{i}+2\hat{j}+3\hat{k}$ by $|\vec{a}+\vec{b}|^2 = 14$ in place of $|\vec{a}+\vec{b}| = \sqrt{14}$."),
   (r"$\frac{1}{\sqrt{6}}(\hat{i}+2\hat{j}+3\hat{k})$", r"Takes the magnitude as $\sqrt{1+2+3} = \sqrt{6}$, adding the components without squaring them."),
   (r"$\frac{1}{\sqrt{26}}(3\hat{i}-4\hat{j}+\hat{k})$", r"Uses $\vec{a}-\vec{b} = 3\hat{i}-4\hat{j}+\hat{k}$, of magnitude $\sqrt{26}$, in place of the sum.")],
  r"$\vec{a}+\vec{b} = \hat{i}+2\hat{j}+3\hat{k}$ and $|\vec{a}+\vec{b}| = \sqrt{1+4+9} = \sqrt{14}$. The unit vector is $\frac{1}{\sqrt{14}}(\hat{i}+2\hat{j}+3\hat{k})$.",
  r"Dividing by the square of the magnitude, or by the sum of the components, when normalising.",
  "U12-A-unit-vector-of-sum", "One addition and one normalisation.",
  check=_c001,
  values=[R_(1/sqrt(14), 2/sqrt(14), 3/sqrt(14)), R_(Rational(1, 14), Rational(2, 14), Rational(3, 14)),
          R_(1/sqrt(6), 2/sqrt(6), 3/sqrt(6)), R_(3/sqrt(26), -4/sqrt(26), 1/sqrt(26))],
  cognitive="Application", source_class=SC)


def _c002():
    p, qq = V(1, -2, 3), V(4, 2, 3)
    return mag(qq - p)


q("U12-A-002", TOPIC, "Magnitude of a displacement vector", "Easy", "Single-step computation MCQ",
  r"The points $P$ and $Q$ have position vectors $\hat{i} - 2\hat{j} + 3\hat{k}$ and $4\hat{i} + 2\hat{j} + 3\hat{k}$ respectively. Then $|\overrightarrow{PQ}|$ equals",
  r"$5$",
  [(r"$\sqrt{61}$", r"Adds the position vectors: $|5\hat{i} + 6\hat{k}| = \sqrt{61}$, in place of subtracting them."),
   (r"$25$", r"Finds $|\overrightarrow{PQ}|^2 = 9 + 16 + 0 = 25$ and stops without taking the square root."),
   (r"$7$", r"Adds the components $3 + 4 + 0$ of $\overrightarrow{PQ}$ in place of using $\sqrt{3^2+4^2+0^2}$.")],
  r"$\overrightarrow{PQ} = \vec{q} - \vec{p} = 3\hat{i} + 4\hat{j} + 0\hat{k}$, so $|\overrightarrow{PQ}| = \sqrt{9 + 16} = 5$.",
  r"Adding position vectors instead of subtracting them to get a displacement.",
  "U12-A-displacement-magnitude", "One subtraction and one magnitude.",
  check=_c002, values=[5, sqrt(61), 25, 7],
  numerical=dict(question=r"The points $P$ and $Q$ have position vectors $\hat{i} - 2\hat{j} + 3\hat{k}$ and $4\hat{i} + 2\hat{j} + 3\hat{k}$ respectively. Then $|\overrightarrow{PQ}|$ is", answer=5),
  cognitive="Application", source_class=SC)


def _c003():
    a, b = V(1, 2, -3), V(4, -1, 3)
    return tup(sec_int(a, b, 2, 1))


q("U12-A-003", TOPIC, "Section formula (internal)", "Easy", "Single-step computation MCQ",
  r"The points $P$ and $Q$ have position vectors $\hat{i} + 2\hat{j} - 3\hat{k}$ and $4\hat{i} - \hat{j} + 3\hat{k}$. The position vector of the point $R$ on the segment $PQ$ with $PR : RQ = 2 : 1$ is",
  r"$3\hat{i}+\hat{k}$",
  [(r"$2\hat{i}+\hat{j}-\hat{k}$", r"Attaches the weights to the wrong ends: $\frac{2\vec{p}+\vec{q}}{3}$, which is the point with $PR:RQ = 1:2$."),
   (r"$7\hat{i}-4\hat{j}+9\hat{k}$", r"Uses the external division formula $\frac{2\vec{q}-\vec{p}}{2-1}$."),
   (r"$\frac{5}{2}\hat{i}+\frac{1}{2}\hat{j}$", r"Ignores the ratio and takes the midpoint $\frac{\vec{p}+\vec{q}}{2}$.")],
  r"For internal division in the ratio $2:1$, $\vec{r} = \frac{2\vec{q} + 1\cdot\vec{p}}{3} = \frac{(8\hat{i} - 2\hat{j} + 6\hat{k}) + (\hat{i} + 2\hat{j} - 3\hat{k})}{3} = \frac{9\hat{i} + 3\hat{k}}{3} = 3\hat{i} + \hat{k}$.",
  r"Pairing the ratio terms with the wrong position vectors in the section formula.",
  "U12-A-section-internal", "Direct use of the section formula.",
  check=_c003, values=[(3, 0, 1), (2, 1, -1), (7, -4, 9), R_(Rational(5, 2), Rational(1, 2), 0)],
  cognitive="Application", source_class=SC)


def _c004():
    P, Q, R = V(2, -1, 3), V(4, 3, 1), Matrix([lam, 7, -1])
    d1, d2 = Q - P, R - P
    sol = solve([d2[i]*d1[1] - d1[i]*d2[1] for i in range(3)], lam, dict=True)
    return sol[0][lam]


q("U12-A-004", TOPIC, "Collinearity of three points", "Easy", "Inverse/parameter MCQ",
  r"The points with position vectors $2\hat{i} - \hat{j} + 3\hat{k}$, $4\hat{i} + 3\hat{j} + \hat{k}$ and $\lambda\hat{i} + 7\hat{j} - \hat{k}$ are collinear. Then $\lambda$ equals",
  r"$6$",
  [(r"$4$", r"Finds the multiplier $2$ from the $y$-components but then writes $\lambda = 2 + 2$, adding the multiplier itself instead of $2$ times the $x$-component $2$ of $\overrightarrow{PQ}$."),
   (r"$8$", r"Finds $\overrightarrow{PR} = 2\overrightarrow{PQ}$ but adds $2 \times 2$ to the $x$-coordinate of the second point, $4 + 4$, in place of the first."),
   (r"$10$", r"Uses the position vector of the second point as the direction: $\lambda = 2 + 2 \times 4$.")],
  r"Let the points be $P, Q, R$. $\overrightarrow{PQ} = 2\hat{i} + 4\hat{j} - 2\hat{k}$ and $\overrightarrow{PR} = (\lambda - 2)\hat{i} + 8\hat{j} - 4\hat{k}$. The $y$ and $z$ components give $\overrightarrow{PR} = 2\overrightarrow{PQ}$, so $\lambda - 2 = 4$ and $\lambda = 6$.",
  r"Using a position vector in place of a displacement vector when testing collinearity.",
  "U12-A-collinear-parameter", "One ratio of displacements, one step.",
  check=_c004, values=[6, 4, 8, 10],
  numerical=dict(question=r"The points with position vectors $2\hat{i} - \hat{j} + 3\hat{k}$, $4\hat{i} + 3\hat{j} + \hat{k}$ and $\lambda\hat{i} + 7\hat{j} - \hat{k}$ are collinear. The value of $\lambda$ is", answer=6),
  cognitive="Application", source_class=SC)


def _c005():
    PQ, qv = V(3, -2, 1), V(1, 1, -2)
    return tup(qv - PQ)


q("U12-A-005", TOPIC, "Position vector from a displacement", "Easy", "Single-step computation MCQ",
  r"If $\overrightarrow{PQ} = 3\hat{i} - 2\hat{j} + \hat{k}$ and the position vector of $Q$ is $\hat{i} + \hat{j} - 2\hat{k}$, then the position vector of $P$ is",
  r"$-2\hat{i}+3\hat{j}-3\hat{k}$",
  [(r"$4\hat{i}-\hat{j}-\hat{k}$", r"Writes $\overrightarrow{PQ} = \vec{p} - \vec{q}$, so gets $\vec{p} = \vec{q} + \overrightarrow{PQ}$."),
   (r"$2\hat{i}-3\hat{j}+3\hat{k}$", r"Rearranges $\overrightarrow{PQ} = \vec{q} - \vec{p}$ as $\vec{p} = \overrightarrow{PQ} - \vec{q}$, a sign slip."),
   (r"$-2\hat{i}+3\hat{j}-\hat{k}$", r"Correct method but slips in the $\hat{k}$-component, computing $-2 - 1$ as $-1$.")],
  r"$\overrightarrow{PQ} = \vec{q} - \vec{p}$, so $\vec{p} = \vec{q} - \overrightarrow{PQ} = (1-3)\hat{i} + (1+2)\hat{j} + (-2-1)\hat{k} = -2\hat{i} + 3\hat{j} - 3\hat{k}$.",
  r"Writing $\overrightarrow{PQ}$ as initial minus terminal position vector.",
  "U12-A-pv-from-displacement", "One rearrangement of $\\overrightarrow{PQ} = \\vec{q} - \\vec{p}$.",
  check=_c005, values=[(-2, 3, -3), (4, -1, -1), (2, -3, 3), (-2, 3, -1)],
  cognitive="Understanding", source_class=SC)


def _c006():
    a, b = V(2, 1, -2), V(1, -1, 1)
    return mag(2*a - 3*b)


q("U12-A-006", TOPIC, "Magnitude of a linear combination", "Easy", "Single-step computation MCQ",
  r"If $\vec{a} = 2\hat{i} + \hat{j} - 2\hat{k}$ and $\vec{b} = \hat{i} - \hat{j} + \hat{k}$, then $|2\vec{a} - 3\vec{b}|$ equals",
  r"$5\sqrt{3}$",
  [(r"$\sqrt{51}$", r"Computes $|2\vec{a} + 3\vec{b}| = |7\hat{i} - \hat{j} - \hat{k}| = \sqrt{51}$, a sign slip on $3\vec{b}$."),
   (r"$6-3\sqrt{3}$", r"Uses $2|\vec{a}| - 3|\vec{b}| = 6 - 3\sqrt{3}$, treating the magnitude as linear."),
   (r"$75$", r"Finds $|2\vec{a}-3\vec{b}|^2 = 1 + 25 + 49 = 75$ and omits the square root.")],
  r"$2\vec{a} - 3\vec{b} = (4-3)\hat{i} + (2+3)\hat{j} + (-4-3)\hat{k} = \hat{i} + 5\hat{j} - 7\hat{k}$, so the magnitude is $\sqrt{1 + 25 + 49} = \sqrt{75} = 5\sqrt{3}$.",
  r"Assuming $|2\vec{a} - 3\vec{b}| = 2|\vec{a}| - 3|\vec{b}|$.",
  "U12-A-magnitude-of-combination", "Componentwise combination then magnitude.",
  check=_c006, values=[5*sqrt(3), sqrt(51), 6 - 3*sqrt(3), 75],
  cognitive="Application", source_class=SC)


def _c007():
    d = V(2, -1, 2)
    return tup(9 * d / mag(d))


q("U12-A-007", TOPIC, "Vector of given magnitude in a given direction", "Easy", "Single-step computation MCQ",
  r"The vector of magnitude $9$ in the direction of $2\hat{i} - \hat{j} + 2\hat{k}$ is",
  r"$6\hat{i}-3\hat{j}+6\hat{k}$",
  [(r"$18\hat{i}-9\hat{j}+18\hat{k}$", r"Multiplies the given vector by $9$ without first making it a unit vector."),
   (r"$\frac{2}{3}\hat{i}-\frac{1}{3}\hat{j}+\frac{2}{3}\hat{k}$", r"Finds the unit vector and stops, never scaling it to magnitude $9$."),
   (r"$2\hat{i}-\hat{j}+2\hat{k}$", r"Scales the unit vector by $\sqrt{9} = 3$ in place of $9$.")],
  r"$|2\hat{i} - \hat{j} + 2\hat{k}| = 3$, so the unit vector is $\frac{1}{3}(2\hat{i} - \hat{j} + 2\hat{k})$ and the required vector is $9 \cdot \frac{1}{3}(2\hat{i} - \hat{j} + 2\hat{k}) = 6\hat{i} - 3\hat{j} + 6\hat{k}$.",
  r"Scaling the given vector instead of its unit vector.",
  "U12-A-scaled-unit-vector", "Normalise then scale.",
  check=_c007, values=[(6, -3, 6), (18, -9, 18), R_(Rational(2, 3), Rational(-1, 3), Rational(2, 3)), (2, -1, 2)],
  cognitive="Application", source_class=SC)


def _c008():
    P, Q, R = V(1, 2, 3), V(-2, 4, 1), V(4, -3, 5)
    return tup((P + Q + R) / 3)


q("U12-A-008", TOPIC, "Centroid by position vectors", "Easy", "Single-step computation MCQ",
  r"The vertices of a triangle have position vectors $\hat{i} + 2\hat{j} + 3\hat{k}$, $-2\hat{i} + 4\hat{j} + \hat{k}$ and $4\hat{i} - 3\hat{j} + 5\hat{k}$. The position vector of its centroid is",
  r"$\hat{i}+\hat{j}+3\hat{k}$",
  [(r"$3\hat{i}+3\hat{j}+9\hat{k}$", r"Adds the three position vectors and forgets to divide by $3$."),
   (r"$\frac{3}{2}\hat{i}+\frac{3}{2}\hat{j}+\frac{9}{2}\hat{k}$", r"Divides the sum by $2$, mixing the centroid with the midpoint formula."),
   (r"$\hat{i}+\frac{1}{2}\hat{j}+3\hat{k}$", r"Takes the midpoint of the side joining the second and third vertices.")],
  r"The centroid is $\frac{1}{3}$ of the sum of the position vectors: $\frac{1}{3}(3\hat{i} + 3\hat{j} + 9\hat{k}) = \hat{i} + \hat{j} + 3\hat{k}$.",
  r"Using the midpoint divisor $2$ for the centroid.",
  "U12-A-centroid", "Direct formula.",
  check=_c008, values=[(1, 1, 3), (3, 3, 9), R_(Rational(3, 2), Rational(3, 2), Rational(9, 2)), R_(1, Rational(1, 2), 3)],
  cognitive="Recall", source_class=SC)


def _c009():
    a, b = Matrix([2, lam, -3]), Matrix([mu, -2, 6])
    sol = solve([a[0]*b[2] - a[2]*b[0], a[1]*b[2] - a[2]*b[1]], [lam, mu], dict=True)[0]
    return sol[lam] + sol[mu]


q("U12-A-009", TOPIC, "Parallel vectors by components", "Easy", "Inverse/parameter MCQ",
  r"If the vectors $2\hat{i} + \lambda\hat{j} - 3\hat{k}$ and $\mu\hat{i} - 2\hat{j} + 6\hat{k}$ are parallel, then $\lambda + \mu$ equals",
  r"$-3$",
  [(r"$3$", r"Takes the common ratio as $+\frac{1}{2}$ instead of $\frac{-3}{6} = -\frac{1}{2}$, giving $\mu = 4$ and $\lambda = -1$."),
   (r"$-5$", r"Gets $\mu = -4$ correctly but solves $\frac{\lambda}{-2} = -\frac{1}{2}$ as $\lambda = -1$."),
   (r"$5$", r"Gets $\lambda = 1$ correctly but solves $\frac{2}{\mu} = -\frac{1}{2}$ as $\mu = 4$.")],
  r"Parallel vectors have proportional components: $\frac{2}{\mu} = \frac{\lambda}{-2} = \frac{-3}{6} = -\frac{1}{2}$. Hence $\mu = -4$ and $\lambda = 1$, so $\lambda + \mu = -3$.",
  r"Losing the sign of the common ratio of components.",
  "U12-A-parallel-components", "One proportionality, two unknowns.",
  check=_c009, values=[-3, 3, -5, 5], cognitive="Application", source_class=SC)


def _c010():
    th = 2*pi/3
    return (simplify(6*cos(th)), simplify(6*sin(th)))


q("U12-A-010", TOPIC, "Components in two dimensions", "Easy", "Single-step computation MCQ",
  r"A vector in the $xy$-plane has magnitude $6$ and makes an angle of $120^\circ$, measured anticlockwise, with the positive $x$-axis. The vector is",
  r"$-3\hat{i}+3\sqrt{3}\hat{j}$",
  [(r"$3\hat{i}+3\sqrt{3}\hat{j}$", r"Takes $\cos 120^\circ = +\frac{1}{2}$, missing the sign in the second quadrant."),
   (r"$3\sqrt{3}\hat{i}-3\hat{j}$", r"Swaps the roles of cosine and sine: $x = 6\sin 120^\circ$, $y = 6\cos 120^\circ$."),
   (r"$-3\hat{i}-3\sqrt{3}\hat{j}$", r"Takes $\sin 120^\circ = -\frac{\sqrt{3}}{2}$, a sign slip in the second quadrant.")],
  r"The components are $6\cos 120^\circ = -3$ and $6\sin 120^\circ = 3\sqrt{3}$, so the vector is $-3\hat{i} + 3\sqrt{3}\hat{j}$.",
  r"Quadrant sign errors when resolving a vector into components.",
  "U12-A-2D-components", "One resolution into components.",
  check=_c010, values=[(-3, 3*sqrt(3)), (3, 3*sqrt(3)), (3*sqrt(3), -3), (-3, -3*sqrt(3))],
  cognitive="Application", source_class=SC)


def _c011():
    sol = [s for s in solve(x_**2 + Rational(4, 9) + Rational(1, 9) - 1, x_) if s > 0]
    return sol[0]


q("U12-A-011", TOPIC, "Unit vector condition", "Easy", "Inverse/parameter MCQ",
  r"If $x\hat{i} + \frac{2}{3}\hat{j} - \frac{1}{3}\hat{k}$ is a unit vector and $x > 0$, then $x$ equals",
  r"$\frac{2}{3}$",
  [(r"$\frac{4}{9}$", r"Finds $x^2 = 1 - \frac{4}{9} - \frac{1}{9} = \frac{4}{9}$ and does not take the square root."),
   (r"$\frac{\sqrt{5}}{3}$", r"Subtracts only $\left(\frac{2}{3}\right)^2$ from $1$, forgetting the $\hat{k}$-component: $x^2 = \frac{5}{9}$."),
   (r"$\frac{2\sqrt{2}}{3}$", r"Subtracts only $\left(\frac{1}{3}\right)^2$ from $1$, forgetting the $\hat{j}$-component: $x^2 = \frac{8}{9}$.")],
  r"A unit vector has $x^2 + \frac{4}{9} + \frac{1}{9} = 1$, so $x^2 = \frac{4}{9}$ and, as $x > 0$, $x = \frac{2}{3}$.",
  r"Dropping a component from the sum of squares.",
  "U12-A-unit-condition", "One equation from $|\\vec{r}| = 1$.",
  check=_c011, values=[Rational(2, 3), Rational(4, 9), sqrt(5)/3, 2*sqrt(2)/3],
  cognitive="Application", source_class=SC)


q("U12-A-012", TOPIC, "Vector addition and medians", "Easy", "Direct concept MCQ",
  r"In triangle $PQR$, $M$ is the midpoint of side $QR$. Then $\overrightarrow{PQ} + \overrightarrow{PR}$ equals",
  r"$2\overrightarrow{PM}$",
  [(r"$\overrightarrow{PM}$", r"Confuses the sum with the average: it is $\frac{1}{2}(\overrightarrow{PQ} + \overrightarrow{PR})$ that equals $\overrightarrow{PM}$."),
   (r"$2\overrightarrow{MP}$", r"Correct magnitude but reverses the direction of the median vector."),
   (r"$\overrightarrow{QR}$", r"Treats the sum as $\overrightarrow{PR} - \overrightarrow{PQ}$, which is $\overrightarrow{QR}$.")],
  r"Taking $P$ as origin, $\vec{m} = \frac{\vec{q} + \vec{r}}{2}$, so $\overrightarrow{PQ} + \overrightarrow{PR} = \vec{q} + \vec{r} = 2\vec{m} = 2\overrightarrow{PM}$. This is the parallelogram law: the diagonal from $P$ of the parallelogram on $PQ, PR$ is twice the median.",
  r"Mixing up the sum of two vectors with their average or their difference.",
  "U12-A-median-sum", "Single idea: midpoint formula with the parallelogram law.",
  cognitive="Understanding", source_class=SC)


def _c013():
    sol = solve([x_ + 3*y_ - 5, 2*x_ - y_ - 3], [x_, y_], dict=True)[0]
    return (sol[x_], sol[y_])


q("U12-A-013", TOPIC, "Linear combination in two dimensions", "Easy", "Single-step computation MCQ",
  r"If $x(\hat{i} + 2\hat{j}) + y(3\hat{i} - \hat{j}) = 5\hat{i} + 3\hat{j}$, then the ordered pair $(x, y)$ is",
  r"$(2, 1)$",
  [(r"$(1, 2)$", r"Solves correctly but reports the pair in the order $(y, x)$."),
   (r"$\left(\frac{4}{5}, \frac{7}{5}\right)$", r"Writes the $\hat{j}$-equation as $2x + y = 3$, losing the minus sign of $-\hat{j}$."),
   (r"$\left(\frac{18}{7}, \frac{1}{7}\right)$", r"Matches the $\hat{i}$-coefficients with $3$ and the $\hat{j}$-coefficients with $5$: $x + 3y = 3$, $2x - y = 5$.")],
  r"Comparing components: $x + 3y = 5$ and $2x - y = 3$. From the second, $y = 2x - 3$; then $x + 6x - 9 = 5$ gives $x = 2$, $y = 1$.",
  r"Sign or matching slips when equating components.",
  "U12-A-combination-2D", "Two linear equations from components.",
  check=_c013, values=[(2, 1), (1, 2), (Rational(4, 5), Rational(7, 5)), (Rational(18, 7), Rational(1, 7))],
  cognitive="Application", source_class=SC)


def _c014():
    return [s for s in solve(4 + 9 + lam**2 - 49, lam) if s > 0][0]


q("U12-A-014", TOPIC, "Magnitude with a parameter", "Easy", "Inverse/parameter MCQ",
  r"If $|2\hat{i} - 3\hat{j} + \lambda\hat{k}| = 7$ and $\lambda > 0$, then $\lambda$ equals",
  r"$6$",
  [(r"$2$", r"Treats magnitude as the sum of absolute components: $2 + 3 + \lambda = 7$."),
   (r"$36$", r"Finds $\lambda^2 = 36$ and reports $\lambda^2$."),
   (r"$\sqrt{62}$", r"Sign slip: writes $\lambda^2 = 49 + 4 + 9$.")],
  r"$4 + 9 + \lambda^2 = 49$, so $\lambda^2 = 36$ and, since $\lambda > 0$, $\lambda = 6$.",
  r"Treating the magnitude as a linear sum of components.",
  "U12-A-magnitude-parameter", "One equation from the magnitude.",
  check=_c014, values=[6, 2, 36, sqrt(62)],
  numerical=dict(question=r"If $|2\hat{i} - 3\hat{j} + \lambda\hat{k}| = 7$ and $\lambda > 0$, then the value of $\lambda$ is", answer=6),
  cognitive="Application", source_class=SC)


def _c015():
    P, Q = V(2, 3, 0), V(-1, -1, 12)
    d = Q - P
    return tup(d / mag(d))


q("U12-A-015", TOPIC, "Unit vector along a segment", "Easy", "Single-step computation MCQ",
  r"The unit vector in the direction of $\overrightarrow{PQ}$, where $P$ and $Q$ have position vectors $2\hat{i} + 3\hat{j}$ and $-\hat{i} - \hat{j} + 12\hat{k}$, is",
  r"$\frac{1}{13}(-3\hat{i}-4\hat{j}+12\hat{k})$",
  [(r"$\frac{1}{13}(3\hat{i}+4\hat{j}-12\hat{k})$", r"Uses $\vec{p} - \vec{q}$, i.e. the direction of $\overrightarrow{QP}$."),
   (r"$\frac{1}{\sqrt{146}}(-\hat{i}-\hat{j}+12\hat{k})$", r"Normalises the position vector of $Q$ in place of $\overrightarrow{PQ}$."),
   (r"$\frac{1}{169}(-3\hat{i}-4\hat{j}+12\hat{k})$", r"Divides by $|\overrightarrow{PQ}|^2 = 169$ in place of $|\overrightarrow{PQ}| = 13$.")],
  r"$\overrightarrow{PQ} = \vec{q} - \vec{p} = -3\hat{i} - 4\hat{j} + 12\hat{k}$ with magnitude $\sqrt{9 + 16 + 144} = 13$. The unit vector is $\frac{1}{13}(-3\hat{i} - 4\hat{j} + 12\hat{k})$.",
  r"Reversing the order of subtraction for $\overrightarrow{PQ}$.",
  "U12-A-unit-along-segment", "Displacement then normalisation.",
  check=_c015,
  values=[R_(Rational(-3, 13), Rational(-4, 13), Rational(12, 13)), R_(Rational(3, 13), Rational(4, 13), Rational(-12, 13)),
          R_(-1/sqrt(146), -1/sqrt(146), 12/sqrt(146)), R_(Rational(-3, 169), Rational(-4, 169), Rational(12, 169))],
  cognitive="Application", source_class=SC)


q("U12-A-016", TOPIC, "Triangle inequality for vectors", "Easy", "Statement-based MCQ",
  r"Statement I: For any two vectors $\vec{a}$ and $\vec{b}$, $|\vec{a} + \vec{b}| \le |\vec{a}| + |\vec{b}|$. Statement II: If $\vec{a}$ and $\vec{b}$ are nonzero vectors with $|\vec{a} + \vec{b}| = |\vec{a}| + |\vec{b}|$, then $\vec{a}$ and $\vec{b}$ are in opposite directions." + TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II; but equality in the triangle inequality holds when $\vec{a}$ and $\vec{b}$ have the same direction, not opposite."),
   (ST_FF, r"Rejects Statement I, perhaps thinking the inequality fails for parallel vectors; it holds for all vectors, with equality for like parallel vectors."),
   (ST_FT, r"Reverses the truth values of the two statements.")],
  r"The sides of the triangle formed by $\vec{a}$, $\vec{b}$ and $\vec{a} + \vec{b}$ give $|\vec{a} + \vec{b}| \le |\vec{a}| + |\vec{b}|$, so Statement I is true. Equality holds only when the triangle collapses with $\vec{b} = t\vec{a}$, $t > 0$, i.e. same direction; for opposite directions, e.g. $\vec{b} = -\vec{a}$, $|\vec{a} + \vec{b}| = 0 < 2|\vec{a}|$. So Statement II is false.",
  r"Confusing the equality case of the triangle inequality (like vectors) with unlike vectors.",
  "U12-A-statement-triangle-inequality", "Single concept with a direction trap.",
  cognitive="Understanding", source_class=SC)

# ================================================================ MEDIUM (24)


def _c017():
    p, qq = V(2, 1, -1), V(1, -3, 2)
    return tup(sec_ext(p, qq, 3, 2))


q("U12-A-017", TOPIC, "Section formula (external)", "Medium", "Single-step computation MCQ",
  r"$P$ and $Q$ have position vectors $2\hat{i} + \hat{j} - \hat{k}$ and $\hat{i} - 3\hat{j} + 2\hat{k}$. The point $R$ dividing $PQ$ externally in the ratio $3 : 2$ has position vector",
  r"$-\hat{i}-11\hat{j}+8\hat{k}$",
  [(r"$\frac{7}{5}\hat{i}-\frac{7}{5}\hat{j}+\frac{4}{5}\hat{k}$", r"Uses the internal division formula $\frac{3\vec{q} + 2\vec{p}}{5}$."),
   (r"$4\hat{i}+9\hat{j}-7\hat{k}$", r"Attaches the weights to the wrong points: $\frac{3\vec{p} - 2\vec{q}}{3-2}$."),
   (r"$-\frac{1}{5}\hat{i}-\frac{11}{5}\hat{j}+\frac{8}{5}\hat{k}$", r"Correct numerator $3\vec{q} - 2\vec{p}$ but divides by $3 + 2 = 5$ instead of $3 - 2 = 1$.")],
  r"For external division with $PR : RQ = 3 : 2$, $\vec{r} = \frac{3\vec{q} - 2\vec{p}}{3 - 2} = (3 - 4)\hat{i} + (-9 - 2)\hat{j} + (6 + 2)\hat{k} = -\hat{i} - 11\hat{j} + 8\hat{k}$.",
  r"Mixing internal and external section formulas, or their denominators.",
  "U12-A-section-external", "External division with sign care; two possible slips.",
  check=_c017, values=[(-1, -11, 8), R_(Rational(7, 5), Rational(-7, 5), Rational(4, 5)), (4, 9, -7), R_(Rational(-1, 5), Rational(-11, 5), Rational(8, 5))],
  cognitive="Application", source_class=SC)


def _c018():
    p, qq, r = V(1, 2, -1), V(7, -4, 8), V(3, 0, 2)
    tt = solve(Eq(r[0], p[0] + t_*(qq[0] - p[0])), t_)[0]
    assert simplify(p + tt*(qq - p) - r) == zeros(3, 1)
    return tt / (1 - tt)


q("U12-A-018", TOPIC, "Finding the ratio of division", "Medium", "Multi-step computation MCQ",
  r"The points $P$, $Q$, $R$ have position vectors $\hat{i} + 2\hat{j} - \hat{k}$, $7\hat{i} - 4\hat{j} + 8\hat{k}$ and $3\hat{i} + 2\hat{k}$. Given that $R$ lies on the segment $PQ$, the ratio $PR : RQ$ is",
  r"$1:2$",
  [(r"$2:1$", r"Reverses the ratio, computing $RQ : PR$."),
   (r"$1:3$", r"Computes $PR : PQ$, since $\overrightarrow{PR} = \frac{1}{3}\overrightarrow{PQ}$."),
   (r"$3:1$", r"Computes $PQ : PR$.")],
  r"$\overrightarrow{PR} = 2\hat{i} - 2\hat{j} + 3\hat{k}$ and $\overrightarrow{RQ} = 4\hat{i} - 4\hat{j} + 6\hat{k} = 2\overrightarrow{PR}$. Hence $PR : RQ = 1 : 2$.",
  r"Confusing the part-to-part ratio $PR:RQ$ with the part-to-whole ratio $PR:PQ$.",
  "U12-A-section-ratio-find", "Two displacements compared; orientation of ratio is the trap.",
  check=_c018, values=[Rational(1, 2), 2, Rational(1, 3), 3],
  cognitive="Analysis", source_class=SC)


def _basis3(c1, c2, c3):
    return Matrix([c1, c2, c3])


def _c019():
    P, Q, R = _basis3(1, -2, 3), _basis3(2, lam, -4), _basis3(0, -7, 10)
    d1, d2 = Q - P, R - P
    eqs = [d1[i]*d2[j] - d1[j]*d2[i] for i in range(3) for j in range(i+1, 3)]
    sol = solve(eqs, lam, dict=True)
    return sol[0][lam]


q("U12-A-019", TOPIC, "Collinearity with non-coplanar vectors", "Medium", "Inverse/parameter MCQ",
  r"Let $\vec{a}, \vec{b}, \vec{c}$ be non-coplanar vectors. If the points with position vectors $\vec{a} - 2\vec{b} + 3\vec{c}$, $2\vec{a} + \lambda\vec{b} - 4\vec{c}$ and $-7\vec{b} + 10\vec{c}$ are collinear, then $\lambda$ equals",
  r"$3$",
  [(r"$-7$", r"Equates the $\vec{b}$-coefficient $\lambda + 2$ of $\overrightarrow{PQ}$ directly to $-5$, ignoring the factor $-1$ that relates $\overrightarrow{PQ}$ to $\overrightarrow{PR}$."),
   (r"$5$", r"Takes the $\vec{b}$-coefficient of $\overrightarrow{PQ}$ as $\lambda$, dropping the $+2$ from subtracting $-2\vec{b}$."),
   (r"$7$", r"Writes the $\vec{b}$-coefficient of $\overrightarrow{PQ}$ as $\lambda - 2$, a sign slip, and solves $\lambda - 2 = 5$.")],
  r"Call the points $P, Q, R$. $\overrightarrow{PQ} = \vec{a} + (\lambda + 2)\vec{b} - 7\vec{c}$ and $\overrightarrow{PR} = -\vec{a} - 5\vec{b} + 7\vec{c}$. Since $\vec{a}, \vec{b}, \vec{c}$ are non-coplanar, collinearity forces $\overrightarrow{PQ} = -\overrightarrow{PR}$ (from the $\vec{a}$- and $\vec{c}$-coefficients), so $\lambda + 2 = 5$ and $\lambda = 3$.",
  r"Sign slips when subtracting position vectors expressed in a basis.",
  "U12-A-collinear-abstract", "Two displacements in an abstract basis; coefficient matching.",
  check=_c019, values=[3, -7, 5, 7],
  numerical=dict(question=r"Let $\vec{a}, \vec{b}, \vec{c}$ be non-coplanar vectors. If the points with position vectors $\vec{a} - 2\vec{b} + 3\vec{c}$, $2\vec{a} + \lambda\vec{b} - 4\vec{c}$ and $-7\vec{b} + 10\vec{c}$ are collinear, then the value of $\lambda$ is", answer=3),
  cognitive="Application", source_class=SC)


def _c020():
    a, b, c, d = V(1, 1, 0), V(0, 1, 1), V(1, 0, 1), V(5, 3, 6)
    sol = solve(list(x_*a + y_*b + z_*c - d), [x_, y_, z_], dict=True)[0]
    return (sol[x_], sol[y_], sol[z_])


q("U12-A-020", TOPIC, "Linear combination in three dimensions", "Medium", "Multi-step computation MCQ",
  r"If $5\hat{i} + 3\hat{j} + 6\hat{k} = x(\hat{i} + \hat{j}) + y(\hat{j} + \hat{k}) + z(\hat{i} + \hat{k})$, then $(x, y, z)$ is",
  r"$(1, 2, 4)$",
  [(r"$(8, 9, 11)$", r"Adds the three equations to get $2(x + y + z) = 14$ but uses $x + y + z = 14$, then subtracts each equation from $14$."),
   (r"$(2, 4, 1)$", r"Finds $x + y + z = 7$ but subtracts the wrong equations: $x = 7 - 5$, $y = 7 - 3$, $z = 7 - 6$."),
   (r"$(4, 1, 2)$", r"Finds $x + y + z = 7$ but pairs each unknown with the wrong equation: $x = 7 - 3$, $y = 7 - 6$, $z = 7 - 5$.")],
  r"Comparing components: $x + z = 5$, $x + y = 3$, $y + z = 6$. Adding, $x + y + z = 7$. Then $x = 7 - 6 = 1$, $y = 7 - 5 = 2$, $z = 7 - 3 = 4$.",
  r"Mispairing unknowns with equations after adding a symmetric system.",
  "U12-A-combination-3D", "Three component equations solved with a symmetric trick.",
  check=_c020, values=[(1, 2, 4), (8, 9, 11), (2, 4, 1), (4, 1, 2)],
  cognitive="Application", source_class=SC)


def _c021():
    a, b = V(2, -1, 2), V(0, 3, 4)
    w = a / mag(a) + b / mag(b)
    return tup(w / mag(w))


_s6 = 5*sqrt(6)
_s3 = 5*sqrt(3)
q("U12-A-021", TOPIC, "Unit vector along an angle bisector", "Medium", "Multi-step computation MCQ",
  r"If $\vec{a} = 2\hat{i} - \hat{j} + 2\hat{k}$ and $\vec{b} = 3\hat{j} + 4\hat{k}$, then a unit vector along the internal bisector of the angle between $\vec{a}$ and $\vec{b}$ is",
  r"$\frac{1}{5\sqrt{6}}(5\hat{i}+2\hat{j}+11\hat{k})$",
  [(r"$\frac{1}{\sqrt{11}}(\hat{i}+\hat{j}+3\hat{k})$", r"Normalises $\vec{a} + \vec{b} = 2\hat{i} + 2\hat{j} + 6\hat{k}$; since $|\vec{a}| \ne |\vec{b}|$, this is not along the bisector."),
   (r"$\frac{1}{5\sqrt{3}}(5\hat{i}-7\hat{j}-\hat{k})$", r"Normalises $\hat{a} - \hat{b} = \frac{1}{15}(10\hat{i} - 14\hat{j} - 2\hat{k})$, which is along the external bisector."),
   (r"$\frac{2}{15}(5\hat{i}+2\hat{j}+11\hat{k})$", r"Finds $\hat{a} + \hat{b}$ correctly but does not normalise it.")],
  r"$\hat{a} = \frac{1}{3}(2\hat{i} - \hat{j} + 2\hat{k})$ and $\hat{b} = \frac{1}{5}(3\hat{j} + 4\hat{k})$. The internal bisector is along $\hat{a} + \hat{b} = \frac{1}{15}(10\hat{i} + 4\hat{j} + 22\hat{k}) = \frac{2}{15}(5\hat{i} + 2\hat{j} + 11\hat{k})$. Since $|5\hat{i} + 2\hat{j} + 11\hat{k}| = \sqrt{150} = 5\sqrt{6}$, the unit vector is $\frac{1}{5\sqrt{6}}(5\hat{i} + 2\hat{j} + 11\hat{k})$.",
  r"Using $\vec{a} + \vec{b}$ instead of $\hat{a} + \hat{b}$ for the bisector of vectors of unequal length.",
  "U12-A-bisector-unit-vector", "Two unit vectors, their sum, and a final normalisation.",
  check=_c021,
  values=[R_(5/_s6, 2/_s6, 11/_s6), R_(1/sqrt(11), 1/sqrt(11), 3/sqrt(11)), R_(5/_s3, -7/_s3, -1/_s3),
          R_(Rational(10, 15), Rational(4, 15), Rational(22, 15))],
  cognitive="Application", source_class=SC)


def _c022():
    pts = [Matrix([cos(k*pi/3), sin(k*pi/3)]) for k in range(6)]
    P = pts[0]
    a, b = pts[1] - pts[0], pts[2] - pts[1]
    S = sum((pts[k] - P for k in range(1, 6)), zeros(2, 1))
    sol = solve(list(x_*a + y_*b - S), [x_, y_], dict=True)[0]
    return (sol[x_], sol[y_])


q("U12-A-022", TOPIC, "Vectors in a regular hexagon", "Medium", "Multi-step computation MCQ",
  r"$PQRSTU$ is a regular hexagon with $\overrightarrow{PQ} = \vec{a}$ and $\overrightarrow{QR} = \vec{b}$. Then $\overrightarrow{PQ} + \overrightarrow{PR} + \overrightarrow{PS} + \overrightarrow{PT} + \overrightarrow{PU}$ equals",
  r"$6\vec{b}$",
  [(r"$3\vec{b}$", r"Gets the sum as $3\overrightarrow{PS}$ but takes $\overrightarrow{PS} = \vec{b}$; the long diagonal $PS$ is twice the side $QR$."),
   (r"$5\vec{b}$", r"Takes $\overrightarrow{PR} + \overrightarrow{PT} = \overrightarrow{PS}$ instead of $\frac{3}{2}\overrightarrow{PS}$, getting $\left(\frac{1}{2} + 1 + 1\right)\overrightarrow{PS} = 5\vec{b}$."),
   (r"$3(\vec{a}+\vec{b})$", r"Gets $3\overrightarrow{PS}$ but uses $\overrightarrow{PS} = \vec{a} + \vec{b}$, which is actually $\overrightarrow{PR}$.")],
  r"Let $O$ be the centre. $\overrightarrow{PS} = 2\overrightarrow{PO} = 2\vec{b}$ since $PS$ is parallel to $QR$ and twice as long. By symmetry about $PS$, $\overrightarrow{PQ} + \overrightarrow{PU} = \overrightarrow{PO} = \frac{1}{2}\overrightarrow{PS}$ and $\overrightarrow{PR} + \overrightarrow{PT} = \frac{3}{2}\overrightarrow{PS}$. The total is $\left(\frac{1}{2} + \frac{3}{2} + 1\right)\overrightarrow{PS} = 3\overrightarrow{PS} = 6\vec{b}$.",
  r"Taking the long diagonal of a regular hexagon equal to a side.",
  "U12-A-hexagon-sum", "Hexagon geometry, symmetry pairing and expressing in a basis.",
  check=_c022, values=[(0, 6), (0, 3), (0, 5), (3, 3)],
  cognitive="Analysis", source_class=SC)


q("U12-A-023", TOPIC, "Medians and centroid in vector form", "Medium", "Statement-based MCQ",
  r"Let $L, M, N$ be the midpoints of the sides $QR, RP, PQ$ of triangle $PQR$, and let $G$ be its centroid. Statement I: $\overrightarrow{PL} + \overrightarrow{QM} + \overrightarrow{RN} = \vec{0}$. Statement II: For every point $O$, $\overrightarrow{OP} + \overrightarrow{OQ} + \overrightarrow{OR} = 3\overrightarrow{OG}$." + TAIL,
  ST_TT,
  [(ST_TF, r"Doubts Statement II for $O$ not at the origin; but $\overrightarrow{OP} + \overrightarrow{OQ} + \overrightarrow{OR} - 3\overrightarrow{OG} = \vec{p} + \vec{q} + \vec{r} - 3\vec{g} = \vec{0}$ for any $O$."),
   (ST_FT, r"Thinks the three medians add to $3\overrightarrow{PG}$ or similar, missing that their sum is zero."),
   (ST_FF, r"Rejects both identities, not checking them with position vectors.")],
  r"With position vectors, $\overrightarrow{PL} = \frac{\vec{q} + \vec{r}}{2} - \vec{p}$ and similarly for the others; adding gives $(\vec{p} + \vec{q} + \vec{r}) - (\vec{p} + \vec{q} + \vec{r}) = \vec{0}$, so Statement I is true. For any $O$, $\overrightarrow{OP} + \overrightarrow{OQ} + \overrightarrow{OR} = (\vec{p} - \vec{o}) + (\vec{q} - \vec{o}) + (\vec{r} - \vec{o}) = 3\vec{g} - 3\vec{o} = 3\overrightarrow{OG}$, so Statement II is true.",
  r"Believing vector identities about a centroid depend on the choice of origin.",
  "U12-A-statement-medians", "Two identities, each needing a short position-vector proof.",
  cognitive="Understanding", source_class=SC)


def _c024():
    P, Q, R = V(2, 1, -1), Matrix([3, lam, 1]), Matrix([5, 7, mu])
    d1, d2 = Q - P, R - P
    eqs = [d1[i]*d2[j] - d1[j]*d2[i] for i in range(3) for j in range(i+1, 3)]
    sol = solve(eqs, [lam, mu], dict=True)[0]
    return sol[lam] + sol[mu]


q("U12-A-024", TOPIC, "Collinearity with two parameters", "Medium", "Inverse/parameter MCQ",
  r"If the points $P(2, 1, -1)$, $Q(3, \lambda, 1)$ and $R(5, 7, \mu)$ are collinear, then $\lambda + \mu$ equals",
  r"$8$",
  [(r"$6$", r"Writes the $y$-component of $\overrightarrow{PQ}$ as $\lambda + 1$, so $3(\lambda + 1) = 6$ gives $\lambda = 1$; with $\mu = 5$ the sum is $6$."),
   (r"$10$", r"Writes the $z$-component of $\overrightarrow{PR}$ as $\mu - 1$, so $\mu - 1 = 6$ gives $\mu = 7$; with $\lambda = 3$ the sum is $10$."),
   (r"$7$", r"Uses the multiplier $2$ (the ratio of the $x$-components of $\overrightarrow{QR}$ and $\overrightarrow{PQ}$) for $\overrightarrow{PR} = k\overrightarrow{PQ}$: $\lambda - 1 = 3$, $\mu + 1 = 4$.")],
  r"$\overrightarrow{PQ} = \hat{i} + (\lambda - 1)\hat{j} + 2\hat{k}$ and $\overrightarrow{PR} = 3\hat{i} + 6\hat{j} + (\mu + 1)\hat{k}$. The $x$-components give $\overrightarrow{PR} = 3\overrightarrow{PQ}$, so $6 = 3(\lambda - 1)$ and $\mu + 1 = 6$. Thus $\lambda = 3$, $\mu = 5$, $\lambda + \mu = 8$.",
  r"Sign slips in displacement components and using the wrong multiplier.",
  "U12-A-collinear-parameter", "Fix the multiplier from one component, then solve two equations.",
  check=_c024, values=[8, 6, 10, 7],
  numerical=dict(question=r"If the points $P(2, 1, -1)$, $Q(3, \lambda, 1)$ and $R(5, 7, \mu)$ are collinear, then the value of $\lambda + \mu$ is", answer=8),
  cognitive="Application", source_class=SC)


def _c025():
    P, Q, R = V(1, 1, 1), V(2, 3, 3), V(3, 5, -3)
    m, n = mag(Q - P), mag(R - P)
    return tup(sec_int(Q, R, m, n))


q("U12-A-025", TOPIC, "Internal bisector meeting the opposite side", "Medium", "Multi-step computation MCQ",
  r"The vertices $P, Q, R$ of a triangle have position vectors $\hat{i} + \hat{j} + \hat{k}$, $2\hat{i} + 3\hat{j} + 3\hat{k}$ and $3\hat{i} + 5\hat{j} - 3\hat{k}$. The internal bisector of angle $P$ meets $QR$ at $S$. The position vector of $S$ is",
  r"$\frac{7}{3}\hat{i}+\frac{11}{3}\hat{j}+\hat{k}$",
  [(r"$\frac{8}{3}\hat{i}+\frac{13}{3}\hat{j}-\hat{k}$", r"Uses $QS : SR = PR : PQ = 2 : 1$, reversing the bisector ratio."),
   (r"$\frac{5}{2}\hat{i}+4\hat{j}$", r"Assumes the bisector meets $QR$ at its midpoint."),
   (r"$\hat{i}+\hat{j}+9\hat{k}$", r"Divides $QR$ externally in the ratio $1 : 2$, which is where the external bisector meets line $QR$.")],
  r"$|\overrightarrow{PQ}| = |\hat{i} + 2\hat{j} + 2\hat{k}| = 3$ and $|\overrightarrow{PR}| = |2\hat{i} + 4\hat{j} - 4\hat{k}| = 6$. The internal bisector divides $QR$ with $QS : SR = PQ : PR = 1 : 2$, so $\vec{s} = \frac{2\vec{q} + \vec{r}}{3} = \frac{(4 + 3)\hat{i} + (6 + 5)\hat{j} + (6 - 3)\hat{k}}{3} = \frac{7}{3}\hat{i} + \frac{11}{3}\hat{j} + \hat{k}$.",
  r"Reversing the side ratio in the angle bisector theorem.",
  "U12-A-bisector-divides-side", "Two magnitudes, the bisector theorem and the section formula.",
  check=_c025, values=[R_(Rational(7, 3), Rational(11, 3), 1), R_(Rational(8, 3), Rational(13, 3), -1), R_(Rational(5, 2), 4, 0), (1, 1, 9)],
  cognitive="Application", source_class=SC)


def _c026():
    a = 2*Matrix([cos(pi/6), sin(pi/6)])
    b = 2*sqrt(3)*Matrix([cos(2*pi/3), sin(2*pi/3)])
    return tup(a + b)


q("U12-A-026", TOPIC, "Resultant from components", "Medium", "Multi-step computation MCQ",
  r"Two vectors in the $xy$-plane have magnitudes $2$ and $2\sqrt{3}$ and make angles $30^\circ$ and $120^\circ$ respectively with the positive $x$-axis (measured anticlockwise). Their sum is",
  r"$4\hat{j}$",
  [(r"$2\sqrt{3}\hat{i}+4\hat{j}$", r"Takes $\cos 120^\circ = +\frac{1}{2}$, so the second vector becomes $\sqrt{3}\hat{i} + 3\hat{j}$."),
   (r"$4\hat{i}$", r"Swaps cosine and sine for both vectors, getting $\hat{i} + \sqrt{3}\hat{j}$ and $3\hat{i} - \sqrt{3}\hat{j}$."),
   (r"$-2\hat{j}$", r"Takes $\sin 120^\circ = -\frac{\sqrt{3}}{2}$, so the second vector becomes $-\sqrt{3}\hat{i} - 3\hat{j}$.")],
  r"The first vector is $2(\cos 30^\circ\hat{i} + \sin 30^\circ\hat{j}) = \sqrt{3}\hat{i} + \hat{j}$; the second is $2\sqrt{3}(\cos 120^\circ\hat{i} + \sin 120^\circ\hat{j}) = -\sqrt{3}\hat{i} + 3\hat{j}$. The sum is $4\hat{j}$.",
  r"Quadrant sign errors when resolving a vector at an obtuse angle.",
  "U12-A-2D-components", "Two resolutions and an addition.",
  check=_c026, values=[(0, 4), (2*sqrt(3), 4), (4, 0), (0, -2)],
  cognitive="Application", source_class=SC)


def _c027():
    a, b, c = Matrix([1, 2]), Matrix([3, -1]), Matrix([2, 1])
    w = a + lam*b
    return solve(w[0]*c[1] - w[1]*c[0], lam)[0]


q("U12-A-027", TOPIC, "Parallel linear combination", "Medium", "Inverse/parameter MCQ",
  r"Let $\vec{a} = \hat{i} + 2\hat{j}$, $\vec{b} = 3\hat{i} - \hat{j}$ and $\vec{c} = 2\hat{i} + \hat{j}$. If $\vec{a} + \lambda\vec{b}$ is parallel to $\vec{c}$, then $\lambda$ equals",
  r"$\frac{3}{5}$",
  [(r"$\frac{5}{3}$", r"Reaches $5\lambda = 3$ but inverts it to $\lambda = \frac{5}{3}$."),
   (r"$3$", r"Takes the $\hat{j}$-component of $\lambda\vec{b}$ as $+\lambda$: $1 + 3\lambda = 2(2 + \lambda)$."),
   (r"$-3$", r"Takes the $\hat{i}$-component of $\lambda\vec{b}$ as $-3\lambda$: $1 - 3\lambda = 2(2 - \lambda)$.")],
  r"$\vec{a} + \lambda\vec{b} = (1 + 3\lambda)\hat{i} + (2 - \lambda)\hat{j}$. Parallel to $2\hat{i} + \hat{j}$ means $\frac{1 + 3\lambda}{2} = \frac{2 - \lambda}{1}$, so $1 + 3\lambda = 4 - 2\lambda$ and $\lambda = \frac{3}{5}$.",
  r"Sign slips in components when forming a linear combination.",
  "U12-A-parallel-combination", "Form a combination, then impose proportional components.",
  check=_c027, values=[Rational(3, 5), Rational(5, 3), 3, -3],
  cognitive="Application", source_class=SC)


def _c028():
    P, Q, R = V(1, 2, -1), V(3, 0, 2), V(4, -2, 5)
    return tup(P + R - Q)


q("U12-A-028", TOPIC, "Fourth vertex of a parallelogram", "Medium", "Single-step computation MCQ",
  r"Three consecutive vertices $P, Q, R$ of a parallelogram $PQRS$ have position vectors $\hat{i} + 2\hat{j} - \hat{k}$, $3\hat{i} + 2\hat{k}$ and $4\hat{i} - 2\hat{j} + 5\hat{k}$. The position vector of $S$ is",
  r"$2\hat{i}+2\hat{k}$",
  [(r"$6\hat{i}-4\hat{j}+8\hat{k}$", r"Uses $\vec{q} + \vec{r} - \vec{p}$, the fourth vertex when $P$ is opposite to the new vertex, ignoring the order $PQRS$."),
   (r"$4\hat{j}-4\hat{k}$", r"Uses $\vec{p} + \vec{q} - \vec{r}$, which makes $R$ opposite to the new vertex."),
   (r"$\frac{5}{2}\hat{i}+2\hat{k}$", r"Stops at the midpoint of the diagonal $PR$, the intersection of the diagonals.")],
  r"In parallelogram $PQRS$ the diagonals $PR$ and $QS$ bisect each other, so $\vec{p} + \vec{r} = \vec{q} + \vec{s}$. Thus $\vec{s} = \vec{p} + \vec{r} - \vec{q} = (1 + 4 - 3)\hat{i} + (2 - 2 - 0)\hat{j} + (-1 + 5 - 2)\hat{k} = 2\hat{i} + 2\hat{k}$.",
  r"Ignoring the vertex order, which fixes which points are opposite.",
  "U12-A-parallelogram-vertex", "Diagonal bisection with attention to vertex order.",
  check=_c028, values=[(2, 0, 2), (6, -4, 8), (0, 4, -4), R_(Rational(5, 2), 0, 2)],
  cognitive="Application", source_class=SC)


def _c029():
    a = V(3, 0, 0)
    b = -Rational(5, 3) * a  # opposite direction, magnitude 5
    assert mag(b) == 5
    return mag(2*a - b)


q("U12-A-029", TOPIC, "Magnitude for unlike parallel vectors", "Medium", "Conceptual/application MCQ",
  r"Let $\vec{a}$ and $\vec{b}$ be vectors in opposite directions with $|\vec{a}| = 3$ and $|\vec{b}| = 5$. Then $|2\vec{a} - \vec{b}|$ equals",
  r"$11$",
  [(r"$1$", r"Treats $\vec{a}$ and $\vec{b}$ as having the same direction: $|6 - 5| = 1$."),
   (r"$\sqrt{61}$", r"Treats $2\vec{a}$ and $\vec{b}$ as perpendicular: $\sqrt{36 + 25}$."),
   (r"$8$", r"Drops the factor $2$ and computes $|\vec{a} - \vec{b}| = 3 + 5$.")],
  r"Since $\vec{b}$ is opposite to $\vec{a}$, $\vec{b} = -\frac{5}{3}\vec{a}$. Then $2\vec{a} - \vec{b} = \left(2 + \frac{5}{3}\right)\vec{a} = \frac{11}{3}\vec{a}$, whose magnitude is $\frac{11}{3} \cdot 3 = 11$.",
  r"Subtracting magnitudes without accounting for direction.",
  "U12-A-antiparallel-magnitude", "Express one vector as a scalar multiple of the other, then combine.",
  check=_c029, values=[11, 1, sqrt(61), 8],
  numerical=dict(question=r"Let $\vec{a}$ and $\vec{b}$ be vectors in opposite directions with $|\vec{a}| = 3$ and $|\vec{b}| = 5$. Then $|2\vec{a} - \vec{b}|$ is", answer=11),
  cognitive="Understanding", source_class=SC)


def _c030():
    P, d = V(1, -1, 2), V(2, 1, -2)
    return tup(P + 6 * d / mag(d))


q("U12-A-030", TOPIC, "Point at a given distance along a direction", "Medium", "Multi-step computation MCQ",
  r"A particle starts at the point with position vector $\hat{i} - \hat{j} + 2\hat{k}$ and moves a distance of $6$ units in the direction of the vector $2\hat{i} + \hat{j} - 2\hat{k}$. Its final position vector is",
  r"$5\hat{i}+\hat{j}-2\hat{k}$",
  [(r"$13\hat{i}+5\hat{j}-10\hat{k}$", r"Adds $6(2\hat{i} + \hat{j} - 2\hat{k})$ without converting the direction to a unit vector."),
   (r"$-3\hat{i}-3\hat{j}+6\hat{k}$", r"Moves in the opposite direction, subtracting $2(2\hat{i} + \hat{j} - 2\hat{k})$."),
   (r"$4\hat{i}+2\hat{j}-4\hat{k}$", r"Finds the displacement $2(2\hat{i} + \hat{j} - 2\hat{k})$ but forgets to add the starting position vector.")],
  r"$|2\hat{i} + \hat{j} - 2\hat{k}| = 3$, so the displacement is $6 \cdot \frac{1}{3}(2\hat{i} + \hat{j} - 2\hat{k}) = 4\hat{i} + 2\hat{j} - 4\hat{k}$. The final position is $(\hat{i} - \hat{j} + 2\hat{k}) + (4\hat{i} + 2\hat{j} - 4\hat{k}) = 5\hat{i} + \hat{j} - 2\hat{k}$.",
  r"Using the direction vector itself as a unit vector.",
  "U12-A-point-at-distance", "Unit vector, scaling and adding to a position.",
  check=_c030, values=[(5, 1, -2), (13, 5, -10), (-3, -3, 6), (4, 2, -4)],
  cognitive="Application", source_class=SC)


def _c031():
    L, M, Nn = V(2, 1, 0), V(1, 2, 1), V(3, 0, 2)
    P = M + Nn - L
    Q, R = 2*Nn - P, 2*M - P
    assert (Q + R) / 2 == L
    return tup(P)


q("U12-A-031", TOPIC, "Vertices from midpoints", "Medium", "Multi-step computation MCQ",
  r"In triangle $PQR$, the midpoints of $QR$, $RP$ and $PQ$ have position vectors $2\hat{i} + \hat{j}$, $\hat{i} + 2\hat{j} + \hat{k}$ and $3\hat{i} + 2\hat{k}$ respectively. The position vector of $P$ is",
  r"$2\hat{i}+\hat{j}+3\hat{k}$",
  [(r"$3\hat{j}-\hat{k}$", r"Computes (midpoint of $QR$) $+$ (midpoint of $RP$) $-$ (midpoint of $PQ$), which gives the vertex $R$."),
   (r"$4\hat{i}-\hat{j}+\hat{k}$", r"Computes (midpoint of $QR$) $+$ (midpoint of $PQ$) $-$ (midpoint of $RP$), which gives the vertex $Q$."),
   (r"$2\hat{i}+\hat{j}+\hat{k}$", r"Averages the three midpoints, which gives the centroid, not a vertex.")],
  r"If $L, M, N$ are the midpoints of $QR, RP, PQ$, then $\vec{m} + \vec{n} - \vec{l} = \frac{\vec{r} + \vec{p}}{2} + \frac{\vec{p} + \vec{q}}{2} - \frac{\vec{q} + \vec{r}}{2} = \vec{p}$. So $\vec{p} = (1 + 3 - 2)\hat{i} + (2 + 0 - 1)\hat{j} + (1 + 2 - 0)\hat{k} = 2\hat{i} + \hat{j} + 3\hat{k}$.",
  r"Choosing the wrong midpoint to subtract.",
  "U12-A-vertices-from-midpoints", "Set up and combine three midpoint relations.",
  check=_c031, values=[(2, 1, 3), (0, 3, -1), (4, -1, 1), (2, 1, 1)],
  cognitive="Analysis", source_class=SC)


def _c032():
    p, qq = V(1, 4, -2), V(9, 0, 6)
    r = (3*p + 5*qq) / 8
    return mag(r - p) / mag(qq - r)


q("U12-A-032", TOPIC, "Ratio from a vector relation", "Medium", "Conceptual/application MCQ",
  r"$O$ is the origin and $P, Q, R$ are distinct points such that $3\overrightarrow{OP} + 5\overrightarrow{OQ} - 8\overrightarrow{OR} = \vec{0}$. Then $R$ lies on segment $PQ$ and the ratio $PR : RQ$ is",
  r"$5:3$",
  [(r"$3:5$", r"Reads $\vec{r} = \frac{3\vec{p} + 5\vec{q}}{8}$ as dividing in the ratio of the coefficients in order, $3:5$; the weight on $\vec{q}$ goes with $PR$."),
   (r"$5:8$", r"Computes $PR : PQ$."),
   (r"$3:8$", r"Computes $RQ : PQ$.")],
  r"$\vec{r} = \frac{3\vec{p} + 5\vec{q}}{3 + 5}$. Comparing with $\frac{m\vec{q} + n\vec{p}}{m + n}$ for $PR : RQ = m : n$ gives $m = 5$, $n = 3$, so $PR : RQ = 5 : 3$.",
  r"Matching the section formula weights to the wrong segments.",
  "U12-A-relation-to-ratio", "Rewrite in section form and orient the ratio.",
  check=_c032, values=[Rational(5, 3), Rational(3, 5), Rational(5, 8), Rational(3, 8)],
  cognitive="Understanding", source_class=SC)


def _c033():
    c, d = Matrix([x_ - 2, 1]), Matrix([2*x_ + 1, -1])
    return solve(c[0]*d[1] - c[1]*d[0], x_)[0]


q("U12-A-033", TOPIC, "Collinear combinations of non-collinear vectors", "Medium", "Inverse/parameter MCQ",
  r"Let $\vec{a}$ and $\vec{b}$ be non-collinear vectors. If $\vec{u} = (x - 2)\vec{a} + \vec{b}$ and $\vec{v} = (2x + 1)\vec{a} - \vec{b}$ are collinear, then $x$ equals",
  r"$\frac{1}{3}$",
  [(r"$-3$", r"Takes the ratio of the $\vec{b}$-coefficients as $+1$: $x - 2 = 2x + 1$."),
   (r"$1$", r"Sets up $x - 2 = -(2x + 1)$ but expands it as $-2x + 1$."),
   (r"$-1$", r"Copies the $\vec{a}$-coefficient of $\vec{u}$ as $x + 2$: $x + 2 = -(2x + 1)$.")],
  r"Collinear means $\vec{u} = t\vec{v}$ for some scalar $t$. As $\vec{a}, \vec{b}$ are non-collinear, compare coefficients: from $\vec{b}$, $1 = -t$, so $t = -1$; then $x - 2 = -(2x + 1)$, giving $3x = 1$ and $x = \frac{1}{3}$.",
  r"Ignoring the sign of the ratio fixed by the $\vec{b}$-coefficients.",
  "U12-A-noncollinear-coefficients", "Coefficient comparison in a non-collinear basis.",
  check=_c033, values=[Rational(1, 3), -3, 1, -1],
  cognitive="Application", source_class=SC)


def _c034():
    P, Q, R = V(1, 2, 3), Matrix([k_, 4, 7]), Matrix([k_**2, 8, 15])
    d1, d2 = Q - P, R - P
    eqs = [d1[i]*d2[j] - d1[j]*d2[i] for i in range(3) for j in range(i+1, 3)]
    sols = solve(eqs, k_, dict=True)
    ks = [s[k_] for s in sols if len({tuple(P), tuple(Q.subs(k_, s[k_])), tuple(R.subs(k_, s[k_]))}) == 3]
    return sum(ks)


q("U12-A-034", TOPIC, "Collinearity leading to a quadratic", "Medium", "Inverse/parameter MCQ",
  r"The points $P(1, 2, 3)$, $Q(k, 4, 7)$ and $R(k^2, 8, 15)$ are collinear. The sum of all real values of $k$ is",
  r"$3$",
  [(r"$2$", r"Cancels the factor $k - 1$ from $k^2 - 1 = 3(k - 1)$, losing the root $k = 1$."),
   (r"$1$", r"Takes the multiplier as $\frac{8}{4} = 2$ from the position vectors' $y$-coordinates rather than the displacements, getting $k^2 - 1 = 2(k - 1)$, i.e. $(k - 1)^2 = 0$."),
   (r"$-3$", r"Solves $k^2 - 3k + 2 = 0$ but takes the sum of roots as $-3$, a sign slip in $-\frac{b}{a}$.")],
  r"$\overrightarrow{PQ} = (k - 1)\hat{i} + 2\hat{j} + 4\hat{k}$ and $\overrightarrow{PR} = (k^2 - 1)\hat{i} + 6\hat{j} + 12\hat{k}$. The $y$- and $z$-components give $\overrightarrow{PR} = 3\overrightarrow{PQ}$, so $k^2 - 1 = 3(k - 1)$, i.e. $k^2 - 3k + 2 = 0$, so $k = 1$ or $k = 2$. Both give three distinct collinear points, so the sum is $3$.",
  r"Dividing by an expression that can be zero, losing a root.",
  "U12-A-collinear-quadratic", "Collinearity condition becomes a quadratic; a root is easily lost.",
  check=_c034, values=[3, 2, 1, -3],
  numerical=dict(question=r"The points $P(1, 2, 3)$, $Q(k, 4, 7)$ and $R(k^2, 8, 15)$ are collinear. The sum of all real values of $k$ is", answer=3),
  cognitive="Analysis", source_class=SC)


def _c035():
    a, b = V(3, 1, 2), V(1, -1, 0)
    f = expand(sum(c**2 for c in (a + t_*b)))
    tm = solve(diff(f, t_), t_)[0]
    return sqrt(f.subs(t_, tm))


q("U12-A-035", TOPIC, "Least magnitude of a linear combination", "Medium", "Multi-step computation MCQ",
  r"Let $\vec{a} = 3\hat{i} + \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} - \hat{j}$. As $t$ varies over the real numbers, the least value of $|\vec{a} + t\vec{b}|$ is",
  r"$2\sqrt{3}$",
  [(r"$\sqrt{14}$", r"Evaluates at $t = 0$, i.e. gives $|\vec{a}|$, assuming any added multiple of $\vec{b}$ increases the length."),
   (r"$2\sqrt{5}$", r"Places the vertex of $2t^2 + 4t + 14$ at $t = +1$ (sign slip), giving $\sqrt{20}$."),
   (r"$\frac{5\sqrt{2}}{2}$", r"Places the vertex at $t = -\frac{1}{2}$, dividing $4$ by $8$ instead of by $2 \cdot 2$, giving $\sqrt{\frac{25}{2}}$.")],
  r"$\vec{a} + t\vec{b} = (3 + t)\hat{i} + (1 - t)\hat{j} + 2\hat{k}$, so $|\vec{a} + t\vec{b}|^2 = (3 + t)^2 + (1 - t)^2 + 4 = 2t^2 + 4t + 14 = 2(t + 1)^2 + 12$. The least value is $12$ at $t = -1$, so the least magnitude is $\sqrt{12} = 2\sqrt{3}$.",
  r"Locating the vertex of the quadratic in $t$ incorrectly.",
  "U12-A-least-magnitude", "Form the quadratic in $t$ from components, then minimise.",
  check=_c035, values=[2*sqrt(3), sqrt(14), 2*sqrt(5), 5*sqrt(2)/2],
  numerical=dict(question=r"Let $\vec{a} = 3\hat{i} + \hat{j} + 2\hat{k}$ and $\vec{b} = \hat{i} - \hat{j}$. As $t$ varies over the real numbers, the least value of $|\vec{a} + t\vec{b}|^2$ is", answer=12),
  cognitive="Analysis", source_class=SC)


def _c036():
    u, w = V(2, -3, 4), V(-4, 6, -8)
    ratio = w[0] / u[0]
    s1 = bool(all(w[i] == ratio*u[i] for i in range(3)) and ratio > 0)
    cnt = sum(1 for v in itertools.product(range(-2, 3), repeat=3) if sum(c*c for c in v) == 3)
    s2 = (cnt == 6)
    return (s1, s2)


q("U12-A-036", TOPIC, "Parallel vectors and integer components", "Medium", "Statement-based MCQ",
  r"Statement I: The vectors $2\hat{i} - 3\hat{j} + 4\hat{k}$ and $-4\hat{i} + 6\hat{j} - 8\hat{k}$ are parallel and have the same direction. Statement II: The number of vectors of magnitude $\sqrt{3}$ whose $\hat{i}, \hat{j}, \hat{k}$ components are all integers is $6$." + TAIL,
  ST_FF,
  [(ST_TT, r"Accepts that the vectors have the same direction, missing that the multiplier $-2$ is negative, and counts only $6$ sign patterns."),
   (ST_TF, r"Treats any proportional vectors as like vectors, ignoring the negative multiplier, and correctly rejects the count $6$."),
   (ST_FT, r"Rejects Statement I correctly but miscounts the sign patterns of $(\pm 1, \pm 1, \pm 1)$ as $6$ instead of $2^3 = 8$.")],
  r"$-4\hat{i} + 6\hat{j} - 8\hat{k} = -2(2\hat{i} - 3\hat{j} + 4\hat{k})$; the multiplier is negative, so they are parallel but opposite, and Statement I is false. Integer components with $x^2 + y^2 + z^2 = 3$ force each of $x, y, z$ to be $\pm 1$, giving $2^3 = 8$ vectors, so Statement II is false.",
  r"Equating parallel with like (same-direction) vectors.",
  "U12-A-statement-parallel-count", "Two separate checks, one with a sign trap and one a small count.",
  check=_c036, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Understanding", source_class=SC)


def _c037():
    S = zeros(3, 1)
    for v in itertools.product((0, 1), repeat=3):
        if v != (0, 0, 0):
            S += Matrix(v)
    return mag(S)


q("U12-A-037", TOPIC, "Sum of vectors to the vertices of a cube", "Medium", "Multi-step computation MCQ",
  r"Let $O$ be one vertex of a cube of edge $1$, and let $V_1, V_2, \ldots, V_7$ be the other seven vertices. Then $|\overrightarrow{OV_1} + \overrightarrow{OV_2} + \cdots + \overrightarrow{OV_7}|$ equals",
  r"$4\sqrt{3}$",
  [(r"$3\sqrt{3}$", r"Leaves out the vertex opposite to $O$, getting the sum $3(\hat{i} + \hat{j} + \hat{k})$."),
   (r"$\sqrt{3}$", r"Adds only the three vertices adjacent to $O$, getting $\hat{i} + \hat{j} + \hat{k}$."),
   (r"$3+3\sqrt{2}+\sqrt{3}$", r"Adds the lengths $3 \cdot 1 + 3\sqrt{2} + \sqrt{3}$ instead of finding the length of the vector sum.")],
  r"Take $O$ as origin with edges along $\hat{i}, \hat{j}, \hat{k}$. The other vertices are $(x, y, z)$ with each coordinate $0$ or $1$, not all $0$. Each coordinate equals $1$ at exactly $4$ of them, so the sum is $4\hat{i} + 4\hat{j} + 4\hat{k}$, of magnitude $4\sqrt{3}$.",
  r"Confusing the magnitude of a sum with the sum of magnitudes.",
  "U12-A-cube-vertex-sum", "Set up coordinates and count contributions per axis.",
  check=_c037, values=[4*sqrt(3), 3*sqrt(3), sqrt(3), 3 + 3*sqrt(2) + sqrt(3)],
  numerical=dict(question=r"Let $O$ be one vertex of a cube of edge $1$, and let $V_1, V_2, \ldots, V_7$ be the other seven vertices. Then $|\overrightarrow{OV_1} + \overrightarrow{OV_2} + \cdots + \overrightarrow{OV_7}|^2$ is", answer=48),
  cognitive="Analysis", source_class=SC)


def _c038():
    d1, d2 = V(3, 1, -2), V(1, -3, 4)
    return Max(mag((d1 + d2) / 2), mag((d1 - d2) / 2))


q("U12-A-038", TOPIC, "Sides of a parallelogram from its diagonals", "Medium", "Multi-step computation MCQ",
  r"The diagonals of a parallelogram are represented by the vectors $3\hat{i} + \hat{j} - 2\hat{k}$ and $\hat{i} - 3\hat{j} + 4\hat{k}$. The length of the longer side of the parallelogram is",
  r"$\sqrt{14}$",
  [(r"$2\sqrt{14}$", r"Takes the side as $\vec{d_1} - \vec{d_2} = 2\hat{i} + 4\hat{j} - 6\hat{k}$, forgetting to halve."),
   (r"$\sqrt{6}$", r"Gives the shorter side, $|\frac{1}{2}(\vec{d_1} + \vec{d_2})| = |2\hat{i} - \hat{j} + \hat{k}|$."),
   (r"$2\sqrt{6}$", r"Takes the side as $\vec{d_1} + \vec{d_2} = 4\hat{i} - 2\hat{j} + 2\hat{k}$ without halving.")],
  r"If the sides are $\vec{u}, \vec{v}$, the diagonals are $\vec{u} + \vec{v}$ and $\vec{u} - \vec{v}$, so the sides are $\frac{1}{2}(\vec{d_1} + \vec{d_2}) = 2\hat{i} - \hat{j} + \hat{k}$ and $\frac{1}{2}(\vec{d_1} - \vec{d_2}) = \hat{i} + 2\hat{j} - 3\hat{k}$, of lengths $\sqrt{6}$ and $\sqrt{14}$. The longer side is $\sqrt{14}$.",
  r"Forgetting the factor $\frac{1}{2}$ when recovering sides from diagonals.",
  "U12-A-parallelogram-diagonals", "Invert the diagonal relations, then compare two magnitudes.",
  check=_c038, values=[sqrt(14), 2*sqrt(14), sqrt(6), 2*sqrt(6)],
  cognitive="Application", source_class=SC)


def _c039():
    P, Q, R = V(2, -1, 4), V(1, 3, -2), V(5, 1, 0)
    G = (P + Q + R) / 3
    return mag(G - P)


q("U12-A-039", TOPIC, "Distance from a vertex to the centroid", "Medium", "Multi-step computation MCQ",
  r"The vertices $P, Q, R$ of a triangle have position vectors $2\hat{i} - \hat{j} + 4\hat{k}$, $\hat{i} + 3\hat{j} - 2\hat{k}$ and $5\hat{i} + \hat{j}$. If $G$ is the centroid, then $|\overrightarrow{PG}|$ equals",
  r"$\frac{2\sqrt{35}}{3}$",
  [(r"$\sqrt{35}$", r"Gives the length of the whole median $PL$, where $L$ is the midpoint of $QR$."),
   (r"$\frac{\sqrt{35}}{3}$", r"Gives $|\overrightarrow{GL}|$, the part of the median beyond the centroid."),
   (r"$\frac{\sqrt{77}}{3}$", r"Gives $|\vec{g}|$, the magnitude of the position vector of $G$, rather than $|\vec{g} - \vec{p}|$.")],
  r"$\vec{g} = \frac{1}{3}(8\hat{i} + 3\hat{j} + 2\hat{k})$, so $\overrightarrow{PG} = \vec{g} - \vec{p} = \frac{1}{3}(2\hat{i} + 6\hat{j} - 10\hat{k})$ and $|\overrightarrow{PG}| = \frac{\sqrt{4 + 36 + 100}}{3} = \frac{\sqrt{140}}{3} = \frac{2\sqrt{35}}{3}$. This is $\frac{2}{3}$ of the median $\sqrt{35}$.",
  r"Using the full median length for the vertex-to-centroid distance.",
  "U12-A-vertex-centroid-distance", "Centroid, displacement and magnitude.",
  check=_c039, values=[2*sqrt(35)/3, sqrt(35), sqrt(35)/3, sqrt(77)/3],
  cognitive="Application", source_class=SC)


def _c040():
    a, b = V(3, 3, 3), V(-2, 5, -9)
    X = Matrix(symbols('x1 x2 x3'))
    Y = Matrix(symbols('y1 y2 y3'))
    sol = solve(list(2*X + Y - a) + list(X - 3*Y - b), list(X) + list(Y), dict=True)[0]
    return tup(X.subs(sol))


q("U12-A-040", TOPIC, "Solving simultaneous vector equations", "Medium", "Multi-step computation MCQ",
  r"Vectors $\vec{x}$ and $\vec{y}$ satisfy $2\vec{x} + \vec{y} = 3\hat{i} + 3\hat{j} + 3\hat{k}$ and $\vec{x} - 3\vec{y} = -2\hat{i} + 5\hat{j} - 9\hat{k}$. Then $\vec{x}$ is",
  r"$\hat{i}+2\hat{j}$",
  [(r"$\hat{i}-\hat{j}+3\hat{k}$", r"Eliminates correctly but reports $\vec{y}$ instead of $\vec{x}$."),
   (r"$\frac{1}{7}(11\hat{i}+4\hat{j}+18\hat{k})$", r"Eliminates $\vec{y}$ with a sign slip, taking $\vec{x} = \frac{3\vec{p} - \vec{q}}{7}$ where $\vec{p}, \vec{q}$ are the right sides."),
   (r"$\frac{1}{5}(7\hat{i}+14\hat{j})$", r"Forms $3\vec{p} + \vec{q}$ correctly but divides by $5$, adding $2 + 3$, instead of $7$.")],
  r"Multiply the first equation by $3$ and add the second: $7\vec{x} = 3(3\hat{i} + 3\hat{j} + 3\hat{k}) + (-2\hat{i} + 5\hat{j} - 9\hat{k}) = 7\hat{i} + 14\hat{j}$, so $\vec{x} = \hat{i} + 2\hat{j}$. (Then $\vec{y} = \hat{i} - \hat{j} + 3\hat{k}$.)",
  r"Sign slips when eliminating one vector from a linear system.",
  "U12-A-vector-linear-system", "Elimination in vector form with two equations.",
  check=_c040, values=[(1, 2, 0), (1, -1, 3), R_(Rational(11, 7), Rational(4, 7), Rational(18, 7)), R_(Rational(7, 5), Rational(14, 5), 0)],
  cognitive="Application", source_class=SC)

# ================================================================ DIFFICULT (14)


def _c041():
    return sum(1 for v in itertools.product(range(-3, 4), repeat=3) if sum(c*c for c in v) == 9)


q("U12-A-041", TOPIC, "Counting integer vectors of given magnitude", "Difficult", "Multi-step computation MCQ",
  r"The number of vectors $\vec{r} = x\hat{i} + y\hat{j} + z\hat{k}$, with $x, y, z$ integers, such that $|\vec{r}| = 3$ is",
  r"$30$",
  [(r"$6$", r"Counts only the vectors along the axes, $\pm 3\hat{i}, \pm 3\hat{j}, \pm 3\hat{k}$, missing $x^2 + y^2 + z^2 = 4 + 4 + 1$."),
   (r"$24$", r"Counts the $(\pm 2, \pm 2, \pm 1)$ type correctly but forgets the $6$ axis vectors."),
   (r"$14$", r"Counts the $6$ axis vectors and the $8$ sign patterns of $(2, 2, 1)$, but forgets that the entry $1$ can be in any of $3$ positions.")],
  r"We need integer solutions of $x^2 + y^2 + z^2 = 9$. Either one entry is $\pm 3$ and the rest $0$: $3 \times 2 = 6$ vectors; or the squares are $4, 4, 1$: choose the position of the $\pm 1$ in $3$ ways and the signs in $2^3$ ways, giving $24$. Total $30$.",
  r"Missing a decomposition of $9$ into three squares, or the arrangements of one.",
  "U12-A-integer-vectors-count", "Case analysis of sums of squares with arrangements and signs.",
  check=_c041, values=[30, 6, 24, 14],
  numerical=dict(question=r"The number of vectors $\vec{r} = x\hat{i} + y\hat{j} + z\hat{k}$, with $x, y, z$ integers, such that $|\vec{r}| = 3$ is", answer=30),
  cognitive="Analysis", source_class=SC)


def _c042():
    P, Q, R = V(1, 2, 0), V(7, 5, 6), V(9, -6, -4)
    a, b, c = mag(R - Q), mag(R - P), mag(Q - P)
    return tup((a*P + b*Q + c*R) / (a + b + c))


q("U12-A-042", TOPIC, "Incentre by position vectors", "Difficult", "Multi-step computation MCQ",
  r"The vertices $P, Q, R$ of a triangle have position vectors $\hat{i} + 2\hat{j}$, $7\hat{i} + 5\hat{j} + 6\hat{k}$ and $9\hat{i} - 6\hat{j} - 4\hat{k}$. The position vector of the incentre of the triangle is",
  r"$5\hat{i}+\hat{j}+\hat{k}$",
  [(r"$\frac{17}{3}\hat{i}+\frac{1}{3}\hat{j}+\frac{2}{3}\hat{k}$", r"Gives the centroid $\frac{\vec{p} + \vec{q} + \vec{r}}{3}$, using equal weights."),
   (r"$\frac{19}{3}\hat{i}-\frac{1}{3}\hat{j}+\frac{1}{3}\hat{k}$", r"Weights each vertex by an adjacent side instead of the opposite side: $\frac{9\vec{p} + 12\vec{q} + 15\vec{r}}{36}$."),
   (r"$8\hat{i}-\frac{1}{2}\hat{j}+\hat{k}$", r"Notices the right angle at $P$ and gives the midpoint of the hypotenuse $QR$, which is the circumcentre.")],
  r"$|\overrightarrow{QR}| = |2\hat{i} - 11\hat{j} - 10\hat{k}| = 15$, $|\overrightarrow{PR}| = |8\hat{i} - 8\hat{j} - 4\hat{k}| = 12$, $|\overrightarrow{PQ}| = |6\hat{i} + 3\hat{j} + 6\hat{k}| = 9$. The incentre is $\frac{15\vec{p} + 12\vec{q} + 9\vec{r}}{36} = \vec{p} + \frac{12(6\hat{i} + 3\hat{j} + 6\hat{k}) + 9(8\hat{i} - 8\hat{j} - 4\hat{k})}{36} = \vec{p} + (4\hat{i} - \hat{j} + \hat{k}) = 5\hat{i} + \hat{j} + \hat{k}$.",
  r"Weighting vertices by adjacent rather than opposite side lengths.",
  "U12-A-incentre", "Three magnitudes, the weighted formula, and careful arithmetic.",
  check=_c042, values=[(5, 1, 1), R_(Rational(17, 3), Rational(1, 3), Rational(2, 3)), R_(Rational(19, 3), Rational(-1, 3), Rational(1, 3)), R_(8, Rational(-1, 2), 1)],
  cognitive="Application", source_class=SC)


def _c043():
    P, Q = V(1, 0, 2), V(4, 3, -1)
    pts = []
    for tt in solve(Eq((t_)**2, 4*(1 - t_)**2), t_):  # R = P + t(Q - P), PR = 2 RQ
        pts.append(P + tt*(Q - P))
    assert len(pts) == 2
    return mag(pts[0] - pts[1])


q("U12-A-043", TOPIC, "Points dividing a line in a given ratio", "Difficult", "Multi-step computation MCQ",
  r"$P$ and $Q$ have position vectors $\hat{i} + 2\hat{k}$ and $4\hat{i} + 3\hat{j} - \hat{k}$. There are exactly two points $R$ on the line $PQ$ such that $PR = 2RQ$ (lengths). The distance between these two points is",
  r"$4\sqrt{3}$",
  [(r"$2\sqrt{13}$", r"Takes the external point as $2\vec{q} + \vec{p}$ (sign slip in $\frac{2\vec{q} - \vec{p}}{2 - 1}$), getting $9\hat{i} + 6\hat{j}$, and measures from $3\hat{i} + 2\hat{j}$."),
   (r"$5\sqrt{3}$", r"Takes the external point on the wrong side, $2\vec{p} - \vec{q}$, which has $RQ = 2PR$ instead of $PR = 2RQ$."),
   (r"$\frac{2\sqrt{5}}{3}$", r"Uses the external numerator $2\vec{q} - \vec{p}$ but divides by $3$ as in the internal formula.")],
  r"The internal point is $\frac{\vec{p} + 2\vec{q}}{3} = 3\hat{i} + 2\hat{j}$. The external point is $\frac{2\vec{q} - \vec{p}}{2 - 1} = 7\hat{i} + 6\hat{j} - 4\hat{k}$. Their difference is $4\hat{i} + 4\hat{j} - 4\hat{k}$, of length $4\sqrt{3}$.",
  r"Forgetting the external point, or using the wrong numerator or denominator for it.",
  "U12-A-two-division-points", "Both internal and external division, then a magnitude.",
  check=_c043, values=[4*sqrt(3), 2*sqrt(13), 5*sqrt(3), 2*sqrt(5)/3],
  numerical=dict(question=r"$P$ and $Q$ have position vectors $\hat{i} + 2\hat{k}$ and $4\hat{i} + 3\hat{j} - \hat{k}$. There are exactly two points $R$ on the line $PQ$ such that $PR = 2RQ$ (lengths). If $d$ is the distance between these two points, then $d^2$ is", answer=48),
  cognitive="Analysis", source_class=SC)


def _c044():
    P, Q, R = Matrix([1, -2]), Matrix([2, lam]), Matrix([lam, 2])
    d1, d2 = Q - P, R - P
    roots = solve(d1[0]*d2[1] - d1[1]*d2[0], lam)
    good = [r for r in roots if len({tuple(P), tuple(Q.subs(lam, r)), tuple(R.subs(lam, r))}) == 3]
    assert len(good) == 1
    return good[0]


q("U12-A-044", TOPIC, "Collinearity of distinct points with a parameter", "Difficult", "Inverse/parameter MCQ",
  r"Let $\vec{a}$ and $\vec{b}$ be non-collinear vectors. The points $P, Q, R$ with position vectors $\vec{a} - 2\vec{b}$, $2\vec{a} + \lambda\vec{b}$ and $\lambda\vec{a} + 2\vec{b}$ are distinct and collinear. Then $\lambda$ equals",
  r"$-3$",
  [(r"$2$", r"Solves $\lambda^2 + \lambda - 6 = 0$ and keeps $\lambda = 2$, for which $Q$ and $R$ coincide at $2\vec{a} + 2\vec{b}$, so the points are not distinct."),
   (r"$3$", r"Sign slip in the $\lambda$-term gives $\lambda^2 - \lambda - 6 = 0$, with roots $3$ and $-2$; picks $3$."),
   (r"$-2$", r"Sign slip in the $\lambda$-term gives $\lambda^2 - \lambda - 6 = 0$, with roots $3$ and $-2$; picks $-2$.")],
  r"$\overrightarrow{PQ} = \vec{a} + (\lambda + 2)\vec{b}$ and $\overrightarrow{PR} = (\lambda - 1)\vec{a} + 4\vec{b}$. Since $\vec{a}, \vec{b}$ are non-collinear, collinearity needs $\frac{\lambda - 1}{1} = \frac{4}{\lambda + 2}$, i.e. $\lambda^2 + \lambda - 6 = 0$, so $\lambda = 2$ or $-3$. For $\lambda = 2$, $Q = R$, which is excluded. Hence $\lambda = -3$; check: $\overrightarrow{PQ} = \vec{a} - \vec{b}$ and $\overrightarrow{PR} = -4\vec{a} + 4\vec{b}$.",
  r"Not testing roots against the distinctness condition.",
  "U12-A-collinear-abstract", "Quadratic from collinearity plus a degenerate root to reject.",
  check=_c044, values=[-3, 2, 3, -2],
  cognitive="Analysis", source_class=SC)


def _c045():
    P, Q, R = Matrix([0, 0]), Matrix([1, 0]), Matrix([0, 1])
    S = sec_int(Q, R, 1, 2)
    T = (P + R) / 2
    sol = solve(list(P + s_*(S - P) - (Q + u_*(T - Q))), [s_, u_], dict=True)[0]
    return sol[s_] / (1 - sol[s_])


q("U12-A-045", TOPIC, "Intersection of two cevians", "Difficult", "Multi-step computation MCQ",
  r"In triangle $PQR$, $S$ is the point on $QR$ with $QS : SR = 1 : 2$ and $T$ is the midpoint of $PR$. The segments $PS$ and $QT$ meet at $X$. Then $PX : XS$ is",
  r"$3:1$",
  [(r"$1:3$", r"Solves correctly for $\overrightarrow{PX} = \frac{3}{4}\overrightarrow{PS}$ but writes the ratio reversed."),
   (r"$2:1$", r"Assumes $X$ divides $PS$ like a centroid divides a median, though $PS$ is not a median."),
   (r"$1:1$", r"Reports $QX : XT$, the ratio in which $X$ divides the other segment.")],
  r"Take $P$ as origin, $\overrightarrow{PQ} = \vec{q}$, $\overrightarrow{PR} = \vec{r}$. Then $\vec{s} = \frac{2\vec{q} + \vec{r}}{3}$ and $\vec{t} = \frac{\vec{r}}{2}$. A point of $PS$ is $\frac{\alpha}{3}(2\vec{q} + \vec{r})$ and a point of $QT$ is $(1 - \beta)\vec{q} + \frac{\beta}{2}\vec{r}$. Comparing coefficients: $\frac{2\alpha}{3} = 1 - \beta$ and $\frac{\alpha}{3} = \frac{\beta}{2}$, so $\beta = \frac{2\alpha}{3}$ and $\alpha = \frac{3}{4}$. Thus $PX : XS = \frac{3}{4} : \frac{1}{4} = 3 : 1$.",
  r"Assuming every intersection of cevians divides them in $2:1$.",
  "U12-A-cevian-intersection", "Two parametrisations and coefficient comparison in a non-collinear basis.",
  check=_c045, values=[3, Rational(1, 3), 2, 1],
  cognitive="Analysis", source_class=SC)


def _c046():
    P, Q, R, S = V(1, 1, 1), V(4, 0, 2), V(7, 4, 4), V(1, 6, 2)
    sol = solve(list(P + s_*(R - P) - (Q + u_*(S - Q))), [s_, u_], dict=True)[0]
    assert 0 < sol[s_] < 1 and 0 < sol[u_] < 1
    return tup(P + sol[s_]*(R - P))


q("U12-A-046", TOPIC, "Intersection of the diagonals of a quadrilateral", "Difficult", "Multi-step computation MCQ",
  r"The vertices of a quadrilateral $PQRS$ have position vectors $\vec{p} = \hat{i} + \hat{j} + \hat{k}$, $\vec{q} = 4\hat{i} + 2\hat{k}$, $\vec{r} = 7\hat{i} + 4\hat{j} + 4\hat{k}$ and $\vec{s} = \hat{i} + 6\hat{j} + 2\hat{k}$. The diagonals $PR$ and $QS$ meet at the point with position vector",
  r"$3\hat{i}+2\hat{j}+2\hat{k}$",
  [(r"$4\hat{i}+\frac{5}{2}\hat{j}+\frac{5}{2}\hat{k}$", r"Assumes the diagonals bisect each other, as in a parallelogram, and takes the midpoint of $PR$."),
   (r"$\frac{5}{2}\hat{i}+3\hat{j}+2\hat{k}$", r"Same parallelogram assumption, taking the midpoint of $QS$."),
   (r"$\frac{13}{4}\hat{i}+\frac{11}{4}\hat{j}+\frac{9}{4}\hat{k}$", r"Averages the four position vectors, which is not the intersection of the diagonals of a general quadrilateral.")],
  r"Points of $PR$: $\vec{p} + \alpha(6\hat{i} + 3\hat{j} + 3\hat{k})$; points of $QS$: $\vec{q} + \beta(-3\hat{i} + 6\hat{j})$. Equating components: $1 + 6\alpha = 4 - 3\beta$, $1 + 3\alpha = 6\beta$, $1 + 3\alpha = 2$. So $\alpha = \frac{1}{3}$, $\beta = \frac{1}{3}$ (all three equations hold), and the point is $\hat{i} + \hat{j} + \hat{k} + (2\hat{i} + \hat{j} + \hat{k}) = 3\hat{i} + 2\hat{j} + 2\hat{k}$.",
  r"Assuming the diagonals of any quadrilateral bisect each other.",
  "U12-A-diagonals-intersection", "Two lines in vector form, a $3 \\times 2$ system and a consistency check.",
  check=_c046, values=[(3, 2, 2), R_(4, Rational(5, 2), Rational(5, 2)), R_(Rational(5, 2), 3, 2), R_(Rational(13, 4), Rational(11, 4), Rational(9, 4))],
  cognitive="Application", source_class=SC)


def _c047():
    u, v = _basis3(1, 2, -1), _basis3(2, 1, 3)
    w = _basis3(5, lam, 5)
    al, be = symbols('al be')
    sol = solve(list(al*u + be*v - w), [al, be, lam], dict=True)[0]
    return sol[lam]


q("U12-A-047", TOPIC, "Expressing a vector as a combination of two others", "Difficult", "Inverse/parameter MCQ",
  r"Let $\vec{a}, \vec{b}, \vec{c}$ be non-coplanar vectors, and let $\vec{u} = \vec{a} + 2\vec{b} - \vec{c}$, $\vec{v} = 2\vec{a} + \vec{b} + 3\vec{c}$, $\vec{w} = 5\vec{a} + \lambda\vec{b} + 5\vec{c}$. If $\vec{w} = \alpha\vec{u} + \beta\vec{v}$ for some real $\alpha, \beta$, then $\lambda$ equals",
  r"$4$",
  [(r"$10$", r"Drops the minus sign of $-\vec{c}$ in $\vec{u}$: $\alpha + 3\beta = 5$ with $\alpha + 2\beta = 5$ gives $\beta = 0$, $\alpha = 5$, $\lambda = 2\alpha + \beta = 10$."),
   (r"$5$", r"Finds $\alpha = 1$, $\beta = 2$ but swaps the $\vec{b}$-coefficients of $\vec{u}$ and $\vec{v}$: $\lambda = \alpha + 2\beta$."),
   (r"$0$", r"Finds $\alpha = 1$, $\beta = 2$ but takes the $\vec{b}$-coefficient of $\vec{v}$ as $-1$: $\lambda = 2\alpha - \beta$.")],
  r"Since $\vec{a}, \vec{b}, \vec{c}$ are non-coplanar, compare coefficients in $\alpha\vec{u} + \beta\vec{v} = \vec{w}$: $\vec{a}$: $\alpha + 2\beta = 5$; $\vec{c}$: $-\alpha + 3\beta = 5$. Adding, $5\beta = 10$, so $\beta = 2$ and $\alpha = 1$. Then the $\vec{b}$-coefficient gives $\lambda = 2\alpha + \beta = 4$.",
  r"Sign slips when matching coefficients in a non-coplanar basis.",
  "U12-A-combination-parameter", "Choose which coefficient equations to solve first, then substitute.",
  check=_c047, values=[4, 10, 5, 0],
  numerical=dict(question=r"Let $\vec{a}, \vec{b}, \vec{c}$ be non-coplanar vectors, and let $\vec{u} = \vec{a} + 2\vec{b} - \vec{c}$, $\vec{v} = 2\vec{a} + \vec{b} + 3\vec{c}$, $\vec{w} = 5\vec{a} + \lambda\vec{b} + 5\vec{c}$. If $\vec{w} = \alpha\vec{u} + \beta\vec{v}$ for some real $\alpha, \beta$, then the value of $\lambda$ is", answer=4),
  cognitive="Application", source_class=SC)


def _c048():
    P, Q, R = V(1, 0, 1), V(3, 2, 2), V(5, 4, -1)
    m, n = mag(Q - P), mag(R - P)
    S = sec_ext(Q, R, m, n)
    # confirm PS is along the external bisector direction
    e = (Q - P)/m - (R - P)/n
    assert Matrix.hstack(S - P, e).rank() == 1
    return tup(S)


q("U12-A-048", TOPIC, "External bisector meeting the opposite side", "Difficult", "Multi-step computation MCQ",
  r"The vertices $P, Q, R$ of a triangle have position vectors $\hat{i} + \hat{k}$, $3\hat{i} + 2\hat{j} + 2\hat{k}$ and $5\hat{i} + 4\hat{j} - \hat{k}$. The external bisector of angle $P$ meets the line $QR$ (extended) at $S$. The position vector of $S$ is",
  r"$\hat{i}+5\hat{k}$",
  [(r"$\frac{11}{3}\hat{i}+\frac{8}{3}\hat{j}+\hat{k}$", r"Divides $QR$ internally in the ratio $1 : 2$, which is where the internal bisector meets $QR$."),
   (r"$7\hat{i}+6\hat{j}-4\hat{k}$", r"Divides $QR$ externally in the reversed ratio $2 : 1$, i.e. uses $PR : PQ$."),
   (r"$4\hat{i}+3\hat{j}+\frac{1}{2}\hat{k}$", r"Takes the midpoint of $QR$.")],
  r"$|\overrightarrow{PQ}| = |2\hat{i} + 2\hat{j} + \hat{k}| = 3$ and $|\overrightarrow{PR}| = |4\hat{i} + 4\hat{j} - 2\hat{k}| = 6$. The external bisector divides $QR$ externally with $QS : SR = 1 : 2$, so $\vec{s} = \frac{1\cdot\vec{r} - 2\vec{q}}{1 - 2} = 2\vec{q} - \vec{r} = \hat{i} + 5\hat{k}$. Check: $\overrightarrow{PS} = 4\hat{k}$ is parallel to $\hat{u}_{PQ} - \hat{u}_{PR} = \frac{1}{3}(2\hat{i} + 2\hat{j} + \hat{k}) - \frac{1}{3}(2\hat{i} + 2\hat{j} - \hat{k}) = \frac{2}{3}\hat{k}$.",
  r"Mixing up internal and external division for angle bisectors.",
  "U12-A-bisector-divides-side", "External bisector theorem with external section formula; ratio orientation trap.",
  check=_c048, values=[(1, 0, 5), R_(Rational(11, 3), Rational(8, 3), 1), (7, 6, -4), R_(4, 3, Rational(1, 2))],
  cognitive="Analysis", source_class=SC)


def _c049():
    # Statement I: counterexample with collinear nonzero vectors
    a, b = V(1, 0, 0), V(2, 0, 0)
    s1 = not (2*a - b == zeros(3, 1))  # x=2, y=-1 nonzero yet 2a - b = 0, so the claim fails
    p, r = V(0, 0, 0), V(5, 0, 0)
    qq = (2*p + 3*r) / 5
    assert 2*p - 5*qq + 3*r == zeros(3, 1)
    s2 = (mag(qq - p) / mag(r - qq) == Rational(3, 2))
    return (s1, s2)


q("U12-A-049", TOPIC, "Linear relations and section ratios", "Difficult", "Statement-based MCQ",
  r"Statement I: If $\vec{a}$ and $\vec{b}$ are nonzero vectors and $x\vec{a} + y\vec{b} = \vec{0}$ for real numbers $x, y$, then $x = y = 0$. Statement II: If the position vectors $\vec{p}, \vec{q}, \vec{r}$ of three distinct points $P, Q, R$ satisfy $2\vec{p} - 5\vec{q} + 3\vec{r} = \vec{0}$, then $Q$ lies on segment $PR$ with $PQ : QR = 3 : 2$." + TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement I, missing that it needs $\vec{a}, \vec{b}$ to be non-collinear; with $\vec{b} = 2\vec{a}$, $2\vec{a} - \vec{b} = \vec{0}$."),
   (ST_FF, r"Rejects Statement II by reading $\vec{q} = \frac{2\vec{p} + 3\vec{r}}{5}$ as giving $PQ : QR = 2 : 3$."),
   (ST_TF, r"Accepts Statement I without the non-collinearity condition and also reverses the ratio in Statement II.")],
  r"Statement I is false: for $\vec{b} = 2\vec{a} \ne \vec{0}$, $x = 2, y = -1$ gives $x\vec{a} + y\vec{b} = \vec{0}$; the conclusion holds only for non-collinear $\vec{a}, \vec{b}$. For Statement II, $\vec{q} = \frac{3\vec{r} + 2\vec{p}}{3 + 2}$, which is the point dividing $PR$ internally with $PQ : QR = 3 : 2$ (the weight on $\vec{r}$ goes with $PQ$). So Statement II is true.",
  r"Dropping the non-collinearity hypothesis, and reversing section weights.",
  "U12-A-statement-linear-relation", "Needs a counterexample for one claim and careful ratio orientation for the other.",
  check=_c049, values=[(False, True), (True, True), (False, False), (True, False)],
  cognitive="Analysis", source_class=SC)


def _c050():
    n = 8
    pts = [Matrix([cos(2*pi*k/n), sin(2*pi*k/n)]) for k in range(n)]
    S = sum((pts[k] - pts[0] for k in range(1, n)), zeros(2, 1))
    P1O = -pts[0]
    return simplify(S[0] / P1O[0])


q("U12-A-050", TOPIC, "Vector sums in a regular polygon", "Difficult", "Conceptual/application MCQ",
  r"$P_1P_2\ldots P_8$ is a regular octagon with centre $O$. If $\overrightarrow{P_1P_2} + \overrightarrow{P_1P_3} + \cdots + \overrightarrow{P_1P_8} = \lambda\,\overrightarrow{P_1O}$, then $\lambda$ equals",
  r"$8$",
  [(r"$7$", r"Writes the sum as $\sum_{k=2}^{8}\overrightarrow{OP_k} - 7\overrightarrow{OP_1}$ and then takes $\sum_{k=2}^{8}\overrightarrow{OP_k} = \vec{0}$, though the zero sum needs all eight vertices."),
   (r"$0$", r"Applies $\sum\overrightarrow{OP_k} = \vec{0}$ directly to the vectors from $P_1$, as if they were drawn from the centre."),
   (r"$2$", r"Assumes by symmetry that only the diametral vector $\overrightarrow{P_1P_5} = 2\overrightarrow{P_1O}$ survives, as if the symmetric pairs cancelled.")],
  r"$\overrightarrow{P_1P_k} = \overrightarrow{OP_k} - \overrightarrow{OP_1}$. Summing over $k = 1$ to $8$ (the $k = 1$ term is $\vec{0}$): $\sum_{k=1}^{8}\overrightarrow{OP_k} - 8\overrightarrow{OP_1} = \vec{0} - 8\overrightarrow{OP_1} = 8\overrightarrow{P_1O}$, since the position vectors of the vertices of a regular polygon from its centre add to $\vec{0}$. So $\lambda = 8$.",
  r"Using the zero-sum property for vectors not drawn from the centre.",
  "U12-A-polygon-vertex-sum", "Change of origin plus the symmetric zero-sum, with an off-by-one trap.",
  check=_c050, values=[8, 7, 0, 2],
  numerical=dict(question=r"$P_1P_2\ldots P_8$ is a regular octagon with centre $O$. If $\overrightarrow{P_1P_2} + \overrightarrow{P_1P_3} + \cdots + \overrightarrow{P_1P_8} = \lambda\,\overrightarrow{P_1O}$, then the value of $\lambda$ is", answer=8),
  cognitive="Analysis", source_class=SC)


def _c051():
    a, b = Matrix([1, 0]), Matrix([0, 1])
    P, Q, Sv = zeros(2, 1), a, b
    R = Sv + 3*a
    sol = solve(list(P + s_*(R - P) - (Q + u_*(Sv - Q))), [s_, u_], dict=True)[0]
    X = P + sol[s_]*(R - P)
    return (X[0], X[1])


q("U12-A-051", TOPIC, "Diagonals of a trapezium", "Difficult", "Multi-step computation MCQ",
  r"$PQRS$ is a trapezium with $SR$ parallel to $PQ$ and $\overrightarrow{SR} = 3\overrightarrow{PQ}$. Taking $P$ as the origin, let $\overrightarrow{PQ} = \vec{a}$ and $\overrightarrow{PS} = \vec{b}$. The diagonals $PR$ and $QS$ meet at the point with position vector",
  r"$\frac{3\vec{a}+\vec{b}}{4}$",
  [(r"$\frac{\vec{a}+\vec{b}}{2}$", r"Assumes the diagonals bisect each other, as in a parallelogram."),
   (r"$\frac{3\vec{a}+\vec{b}}{2}$", r"Takes the midpoint of the diagonal $PR$, whose end is $\vec{r} = 3\vec{a} + \vec{b}$."),
   (r"$\frac{\vec{a}+3\vec{b}}{4}$", r"Solves for the right parameter but attaches the coefficients $\frac{3}{4}$ and $\frac{1}{4}$ to the wrong vectors.")],
  r"$\vec{r} = \vec{b} + 3\vec{a}$. A point of $PR$ is $\alpha(3\vec{a} + \vec{b})$; a point of $QS$ is $\vec{a} + \beta(\vec{b} - \vec{a})$. As $\vec{a}, \vec{b}$ are non-collinear, $3\alpha = 1 - \beta$ and $\alpha = \beta$, so $\alpha = \frac{1}{4}$. The intersection is $\frac{3\vec{a} + \vec{b}}{4}$, dividing $PR$ in the ratio $1 : 3$ of the parallel sides.",
  r"Treating every quadrilateral like a parallelogram.",
  "U12-A-trapezium-diagonals", "Two parametrised lines in an abstract basis.",
  check=_c051, values=[(Rational(3, 4), Rational(1, 4)), (Rational(1, 2), Rational(1, 2)), (Rational(3, 2), Rational(1, 2)), (Rational(1, 4), Rational(3, 4))],
  cognitive="Analysis", source_class=SC)


def _c052():
    return sum(1 for L in range(-20, 21) if L**2 + (L - 1)**2 + 4 <= 25)


q("U12-A-052", TOPIC, "Integer parameters with a magnitude bound", "Difficult", "Multi-step computation MCQ",
  r"The number of integers $\lambda$ for which $|\lambda\hat{i} + (\lambda - 1)\hat{j} + 2\hat{k}| \le 5$ is",
  r"$6$",
  [(r"$8$", r"Leaves out the $\hat{k}$-component, solving $\lambda^2 + (\lambda - 1)^2 \le 25$, i.e. $-3 \le \lambda \le 4$."),
   (r"$7$", r"Writes the $\hat{j}$-component as $\lambda$, solving $2\lambda^2 + 4 \le 25$, i.e. $|\lambda| \le 3$."),
   (r"$4$", r"Counts only the non-negative solutions $0, 1, 2, 3$.")],
  r"$\lambda^2 + (\lambda - 1)^2 + 4 \le 25$ gives $2\lambda^2 - 2\lambda - 20 \le 0$, i.e. $\lambda^2 - \lambda - 10 \le 0$. The roots are $\frac{1 \pm \sqrt{41}}{2} \approx -2.70$ and $3.70$, so the integers are $-2, -1, 0, 1, 2, 3$: six values.",
  r"Dropping a component when forming the magnitude inequality.",
  "U12-A-magnitude-integer-count", "Quadratic inequality with irrational roots, then an integer count.",
  check=_c052, values=[6, 8, 7, 4],
  numerical=dict(question=r"The number of integers $\lambda$ for which $|\lambda\hat{i} + (\lambda - 1)\hat{j} + 2\hat{k}| \le 5$ is", answer=6),
  cognitive="Application", source_class=SC)


def _c053():
    a, b = Matrix([2, 1]), Matrix([1, -2])
    return sum(1 for m in range(-15, 16) for n in range(-15, 16) if sum(c**2 for c in (m*a + n*b)) == 125)


q("U12-A-053", TOPIC, "Integer combinations of given magnitude", "Difficult", "Multi-step computation MCQ",
  r"Let $\vec{a} = 2\hat{i} + \hat{j}$ and $\vec{b} = \hat{i} - 2\hat{j}$. The number of ordered pairs of integers $(m, n)$ such that $|m\vec{a} + n\vec{b}| = 5\sqrt{5}$ is",
  r"$12$",
  [(r"$8$", r"Reduces correctly to $m^2 + n^2 = 25$ but counts only $(\pm 3, \pm 4)$ and $(\pm 4, \pm 3)$, missing the pairs with a zero entry."),
   (r"$4$", r"Counts only pairs with $m, n \ge 0$: $(0, 5), (5, 0), (3, 4), (4, 3)$."),
   (r"$10$", r"Counts the $8$ pairs with no zero entry but only $2$ of the $4$ pairs $(\pm 5, 0), (0, \pm 5)$, forgetting the sign choices.")],
  r"$m\vec{a} + n\vec{b} = (2m + n)\hat{i} + (m - 2n)\hat{j}$, so $|m\vec{a} + n\vec{b}|^2 = (2m + n)^2 + (m - 2n)^2 = 5(m^2 + n^2)$. Setting this to $125$ gives $m^2 + n^2 = 25$, whose integer solutions are $(\pm 5, 0), (0, \pm 5)$ (four) and $(\pm 3, \pm 4), (\pm 4, \pm 3)$ (eight). Total $12$.",
  r"Missing lattice points with a zero coordinate or sign choices.",
  "U12-A-integer-combination-count", "Simplify the magnitude to $5(m^2 + n^2)$, then a careful lattice count.",
  check=_c053, values=[12, 8, 4, 10],
  numerical=dict(question=r"Let $\vec{a} = 2\hat{i} + \hat{j}$ and $\vec{b} = \hat{i} - 2\hat{j}$. The number of ordered pairs of integers $(m, n)$ such that $|m\vec{a} + n\vec{b}| = 5\sqrt{5}$ is", answer=12),
  cognitive="Analysis", source_class=SC)


def _c054():
    P, Q, R = V(2, 0, 1), V(4, 2, -3), V(-2, 6, 3)
    L = (Q + R) / 2
    M, Nn = (P + R) / 2, (P + Q) / 2
    sol = solve(list(P + s_*(L - P) - (Nn + u_*(M - Nn))), [s_, u_], dict=True)[0]
    return tup(P + sol[s_]*(L - P))


q("U12-A-054", TOPIC, "Median meeting the midline", "Difficult", "Multi-step computation MCQ",
  r"The vertices $P, Q, R$ of a triangle have position vectors $2\hat{i} + \hat{k}$, $4\hat{i} + 2\hat{j} - 3\hat{k}$ and $-2\hat{i} + 6\hat{j} + 3\hat{k}$. The median from $P$ meets the segment joining the midpoints of $PQ$ and $PR$ at the point with position vector",
  r"$\frac{3}{2}\hat{i}+2\hat{j}+\frac{1}{2}\hat{k}$",
  [(r"$\frac{4}{3}\hat{i}+\frac{8}{3}\hat{j}+\frac{1}{3}\hat{k}$", r"Assumes the meeting point is the centroid of triangle $PQR$."),
   (r"$\frac{5}{3}\hat{i}+\frac{4}{3}\hat{j}+\frac{2}{3}\hat{k}$", r"Takes the point one third of the way from $P$ along the median, $\frac{2\vec{p} + \vec{l}}{3}$, as if the midline cut the median in $1 : 2$."),
   (r"$3\hat{i}+4\hat{j}+\hat{k}$", r"Correctly identifies the midpoint of the two side midpoints but adds them without halving.")],
  r"Let $L, M, N$ be the midpoints of $QR, PR, PQ$. The midline $NM$ is parallel to $QR$ and halfway from $P$, so it cuts the median $PL$ at its midpoint, which is also the midpoint of $NM$: $\frac{\vec{m} + \vec{n}}{2} = \frac{2\vec{p} + \vec{q} + \vec{r}}{4} = \frac{(4 + 4 - 2)\hat{i} + (0 + 2 + 6)\hat{j} + (2 - 3 + 3)\hat{k}}{4} = \frac{3}{2}\hat{i} + 2\hat{j} + \frac{1}{2}\hat{k}$.",
  r"Assuming any notable point on a median is the centroid.",
  "U12-A-median-midline", "Midpoint theorem in vector form, then intersection of two segments.",
  check=_c054, values=[R_(Rational(3, 2), 2, Rational(1, 2)), R_(Rational(4, 3), Rational(8, 3), Rational(1, 3)), R_(Rational(5, 3), Rational(4, 3), Rational(2, 3)), (3, 4, 1)],
  cognitive="Analysis", source_class=SC)
