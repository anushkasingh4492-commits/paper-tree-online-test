import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import random as _random

x, y, z = symbols('x y z')
k, lam, mu, a, b, c, d, th, s = symbols('k lambda mu a b c d theta s')
XYZ = [x, y, z]

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"

TOPIC = "Systems of linear equations"


def det_(rows):
    return expand(Matrix(rows).det())


def subs_rows(rows, p, v):
    return [[sympify(e).subs(p, v) for e in r] for r in rows]


def subs_vec(vec, p, v):
    return [sympify(e).subs(p, v) for e in vec]


def kind(rows, rhs):
    n = len(rows[0])
    unk = XYZ[:n]
    sol = linsolve((Matrix(rows), Matrix(rhs)), unk)
    if sol == S.EmptySet:
        return "none"
    pt = list(sol)[0]
    return "inf" if any(sympify(e).free_symbols & set(unk) for e in pt) else "unique"


def roots_real(expr, p):
    out = solveset(expr, p, S.Reals)
    if out == S.EmptySet:
        return []
    assert isinstance(out, FiniteSet), out
    return list(out)


def param_set(rows, rhs, p, want):
    """Set of real p (among roots of the determinant) for which the system is of kind `want`."""
    return FiniteSet(*[r for r in roots_real(det_(rows), p)
                       if kind(subs_rows(rows, p, r), subs_vec(rhs, p, r)) == want])


def only(fs):
    fs = list(fs)
    assert len(fs) == 1, fs
    return fs[0]


def consist_expr(rows, rhs):
    """For a singular coefficient matrix of rank 2: n . rhs, where n is the left null vector."""
    ns = Matrix(rows).T.nullspace()
    assert len(ns) == 1
    n = ns[0]
    return expand(sum(n[i] * sympify(rhs[i]) for i in range(len(rhs))))


def ratio(rows):
    ns = Matrix(rows).nullspace()
    assert len(ns) == 1
    v = ns[0]
    return tuple(simplify(e / v[0]) for e in v)


def count_sin(svals, lo, hi):
    pts = set()
    for sv in svals:
        if not (sv.is_real and -1 <= sv <= 1):
            continue
        base = asin(sv)
        for n in range(-2, 4):
            for cand in (base + 2 * pi * n, pi - base + 2 * pi * n):
                cand = simplify(cand)
                if bool(cand >= lo) and bool(cand <= hi):
                    pts.add(cand)
    return len(pts)


# ============================ EASY ============================

q("U03-D-001", TOPIC, "Condition for a unique solution", "Easy", "Inverse/parameter MCQ",
  r"The system of equations $x + y + z = 6$, $x + 2y + 3z = 14$ and $x + 4y + kz = 30$, where $k$ is real, has a unique solution if and only if",
  r"$k \ne 7$",
  [(r"$k = 7$", r"Uses $\Delta = 0$, which is the condition for the system NOT to have a unique solution."),
   (r"$k \ne \frac{13}{3}$", r"Expands along the first row with a $+$ sign on the middle cofactor: $(2k - 12) + (k - 3) + 2 = 3k - 13$."),
   (r"$k \ne 11$", r"Writes the third minor as $2 \cdot 1 - 1 \cdot 4 = -2$ (order reversed), so $\Delta = (2k - 12) - (k - 3) - 2 = k - 11$.")],
  r"A unique solution exists if and only if $\Delta \ne 0$. Expanding along the first row, $\Delta = 1(2k - 12) - 1(k - 3) + 1(4 - 2) = k - 7$. Hence the system has a unique solution exactly when $k \ne 7$.",
  r"Mixing up the condition for a unique solution ($\Delta \ne 0$) with $\Delta = 0$, or slipping a cofactor sign.",
  "U03-D-unique-cond", r"One determinant expansion and the criterion $\Delta \ne 0$.",
  check=lambda: Complement(S.Reals, FiniteSet(*roots_real(det_([[1, 1, 1], [1, 2, 3], [1, 4, k]]), k))),
  values=[Complement(S.Reals, FiniteSet(7)), FiniteSet(7), Complement(S.Reals, FiniteSet(Rational(13, 3))),
          Complement(S.Reals, FiniteSet(11))],
  cognitive="Application", source_class="XII")

q("U03-D-002", TOPIC, "Homogeneous system with a non-trivial solution", "Easy", "Inverse/parameter MCQ",
  r"If the system $x + 2y + z = 0$, $2x - y + z = 0$, $3x + y + kz = 0$ has a non-trivial solution, then $k$ equals",
  r"$2$",
  [(r"$\frac{2}{3}$", r"Uses $+$ for the middle cofactor: $(-k - 1) + 2(2k - 3) + 5 = 3k - 2$, giving $k = \frac{2}{3}$."),
   (r"$0$", r"Writes the third minor as $(-1)(3) - (2)(1) = -5$ (order reversed), so $\Delta = (-k - 1) - (4k - 6) - 5 = -5k$."),
   (r"$\frac{12}{5}$", r"Evaluates the first minor as $-k + 1$ instead of $-k - 1$, so $\Delta = -5k + 12$.")],
  r"A homogeneous system has a non-trivial solution if and only if $\Delta = 0$. Here $\Delta = 1(-k - 1) - 2(2k - 3) + 1(2 + 3) = -5k + 10$, so $k = 2$.",
  r"Sign slips in cofactor expansion of a $3 \times 3$ determinant.",
  "U03-D-homog-nontrivial", r"Single criterion $\Delta = 0$ and one expansion.",
  check=lambda: only(roots_real(det_([[1, 2, 1], [2, -1, 1], [3, 1, k]]), k)),
  values=[2, Rational(2, 3), 0, Rational(12, 5)],
  numerical=dict(question=r"If the system $x + 2y + z = 0$, $2x - y + z = 0$, $3x + y + kz = 0$ has a non-trivial solution, then the value of $k$ is", answer=2),
  cognitive="Application", source_class="XII")


def _c3():
    P = Matrix([[2, -1], [3, 2]]); Q = Matrix([3, 8])
    X = P.inv() * Q
    return (X[0], X[1])


q("U03-D-003", TOPIC, "Matrix method for two variables", "Easy", "Single-step computation MCQ",
  r"The system $2x - y = 3$, $3x + 2y = 8$ is written as $PX = Q$ with $P = \begin{bmatrix} 2 & -1 \\ 3 & 2 \end{bmatrix}$, $X = \begin{bmatrix} x \\ y \end{bmatrix}$ and $Q = \begin{bmatrix} 3 \\ 8 \end{bmatrix}$. Using $X = P^{-1}Q$, the solution is",
  r"$x = 2,\ y = 1$",
  [(r"$x = 1,\ y = 2$", r"Builds $P$ with its two columns interchanged, $\begin{bmatrix} -1 & 2 \\ 2 & 3 \end{bmatrix}$, which swaps the roles of $x$ and $y$."),
   (r"$x = 14,\ y = 7$", r"Takes $|P| = 4 - 3 = 1$, so $X = (\operatorname{adj} P)Q = (14, 7)$."),
   (r"$x = -2,\ y = -1$", r"Computes $|P| = (-1)(3) - (2)(2) = -7$, multiplying the diagonals in the wrong order.")],
  r"$|P| = 2 \cdot 2 - (-1)(3) = 7$ and $\operatorname{adj} P = \begin{bmatrix} 2 & 1 \\ -3 & 2 \end{bmatrix}$. So $X = \frac{1}{7}\begin{bmatrix} 6 + 8 \\ -9 + 16 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$, i.e. $x = 2$, $y = 1$.",
  r"Errors in the $2 \times 2$ determinant or adjoint used for $P^{-1}$.",
  "U03-D-matrix-method-2x2", r"Direct use of the $2 \times 2$ inverse formula.",
  check=_c3, values=[(2, 1), (1, 2), (14, 7), (-2, -1)], cognitive="Application", source_class="XII")


def _c4():
    rows = [[2, 3], [4, k]]
    return only(param_set(rows, [5, 7], k, "none"))


q("U03-D-004", TOPIC, "Two-variable system with no solution", "Easy", "Inverse/parameter MCQ",
  r"The system $2x + 3y = 5$, $4x + ky = 7$ has no solution. Then $k$ equals",
  r"$6$",
  [(r"$\frac{3}{2}$", r"Writes the ratio condition upside down, $\frac{2}{4} = \frac{k}{3}$, giving $k = \frac{3}{2}$."),
   (r"$\frac{21}{5}$", r"Equates $\frac{3}{k}$ with the ratio of constants $\frac{5}{7}$, giving $k = \frac{21}{5}$."),
   (r"$-6$", r"Writes $\Delta$ as $2k + 12$ (sign slip in $a_1b_2 - a_2b_1$) and sets it to zero.")],
  r"No solution requires $\frac{2}{4} = \frac{3}{k} \ne \frac{5}{7}$. The first equality gives $k = 6$, and then $\frac{1}{2} \ne \frac{5}{7}$, so the lines are parallel and distinct. Hence $k = 6$.",
  r"Inverting a ratio or comparing the wrong pair of ratios.",
  "U03-D-2var-ratio", "One proportionality condition and a check on constants.",
  check=_c4, values=[6, Rational(3, 2), Rational(21, 5), -6], cognitive="Application", source_class="XII")


def _c5():
    m = symbols('m')
    kv = only(roots_real(det_([[1, 2], [3, k]]), k))
    mv = only(solve(Matrix([[3, 2], [m, kv]]).det(), m))
    assert kind([[1, 2], [3, kv]], [3, mv]) == "inf"
    return kv + mv


q("U03-D-005", TOPIC, "Two-variable system with infinitely many solutions", "Easy", "Inverse/parameter MCQ",
  r"If the system $x + 2y = 3$, $3x + ky = m$ has infinitely many solutions, then $k + m$ equals",
  r"$15$",
  [(r"$9$", r"Scales the coefficients by $3$ to get $k = 6$ but leaves the constant unscaled, $m = 3$."),
   (r"$\frac{5}{3}$", r"Inverts all the ratios, $\frac{1}{3} = \frac{k}{2} = \frac{m}{3}$, so $k = \frac{2}{3}$ and $m = 1$."),
   (r"$6$", r"Imposes only $\frac{a_1}{a_2} = \frac{b_1}{b_2}$ to get $k = 6$ and treats the system as homogeneous, taking $m = 0$.")],
  r"Infinitely many solutions need $\frac{1}{3} = \frac{2}{k} = \frac{3}{m}$, so the second equation is exactly $3$ times the first. Hence $k = 6$, $m = 9$ and $k + m = 15$.",
  r"Scaling the coefficients but not the constant term.",
  "U03-D-2var-ratio", "Two proportionality conditions read off at once.",
  check=_c5, values=[15, 9, Rational(5, 3), 6],
  numerical=dict(question=r"If the system $x + 2y = 3$, $3x + ky = m$ has infinitely many solutions, then the value of $k + m$ is", answer=15),
  cognitive="Application", source_class="XII")

q("U03-D-006", TOPIC, "Consistency of homogeneous systems", "Easy", "Statement-based MCQ",
  r"Let $P$ be a $3 \times 3$ matrix, $X = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$ and $O$ the $3 \times 1$ zero matrix. Statement I: The homogeneous system $PX = O$ is always consistent. Statement II: If $|P| \ne 0$, then the system $PX = O$ has infinitely many solutions. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Believes $|P| \ne 0$ gives infinitely many solutions; in fact it forces the unique solution $X = P^{-1}O = O$."),
   (ST_FF, r"Overlooks that $X = O$ always satisfies $PX = O$, so the system can never be inconsistent."),
   (ST_FT, r"Thinks a homogeneous system can be inconsistent and that $|P| \ne 0$ gives many solutions; both views are reversed.")],
  r"Statement I is true because $X = O$ always satisfies $PX = O$. Statement II is false: if $|P| \ne 0$, then $P^{-1}$ exists and $X = P^{-1}O = O$ is the only solution, so the system has only the trivial solution.",
  r"Confusing the condition $|P| \ne 0$ (only trivial solution) with $|P| = 0$ (non-trivial solutions).",
  "U03-D-concept-homog", "Recall of two standard facts about homogeneous systems.",
  cognitive="Understanding", source_class="XII")


def _c7():
    Pm = Matrix([[1, 1, 1], [1, -1, 1], [2, 1, -1]]); Q = Matrix([6, 2, 1])
    Dz = Pm.copy(); Dz[:, 2] = Q
    return Dz.det() / Pm.det()


q("U03-D-007", TOPIC, "Cramer's rule in three variables", "Easy", "Multi-step computation MCQ",
  r"The system $x + y + z = 6$, $x - y + z = 2$, $2x + y - z = 1$ is solved by Cramer's rule. The value of $z$ is",
  r"$3$",
  [(r"$\frac{1}{3}$", r"Uses $z = \frac{\Delta}{\Delta_3} = \frac{6}{18}$, inverting Cramer's ratio."),
   (r"$2$", r"Replaces the second column (not the third) by the constants, which gives $\frac{\Delta_2}{\Delta} = \frac{12}{6}$."),
   (r"$1$", r"Replaces the first column by the constants, which gives $\frac{\Delta_1}{\Delta} = \frac{6}{6}$.")],
  r"$\Delta = 1(1 - 1) - 1(-1 - 2) + 1(1 + 2) = 6$. Replacing the third column by $(6, 2, 1)$ gives $\Delta_3 = 1(-1 - 2) - 1(1 - 4) + 6(1 + 2) = 18$. Hence $z = \frac{\Delta_3}{\Delta} = 3$.",
  r"Replacing the wrong column, or inverting the ratio, in Cramer's rule.",
  "U03-D-cramer-3var", "Two $3 \\times 3$ determinants and one division.",
  check=_c7, values=[3, Rational(1, 3), 2, 1], cognitive="Application", source_class="XII")

q("U03-D-008", TOPIC, "Condition for a unique solution", "Easy", "Inverse/parameter MCQ",
  r"The system $kx + 2y = 3$, $2x + ky = 4$, where $k$ is real, has a unique solution if and only if",
  r"$k \notin \{-2, 2\}$",
  [(r"$k \ne 2$", r"Solves $k^2 = 4$ as $k = 2$ only, dropping the negative root."),
   (r"$k \in \{-2, 2\}$", r"Uses $\Delta = 0$, which is where a unique solution fails."),
   (r"$k \ne 4$", r"Sets $k^2 \ne 4$ and then reads it as $k \ne 4$ without taking the square root.")],
  r"A unique solution exists if and only if $\Delta = k \cdot k - 2 \cdot 2 = k^2 - 4 \ne 0$, that is, $k \ne 2$ and $k \ne -2$.",
  r"Losing the negative square root, or reversing the condition $\Delta \ne 0$.",
  "U03-D-unique-cond", r"One $2 \times 2$ determinant and solving $k^2 = 4$.",
  check=lambda: Complement(S.Reals, FiniteSet(*roots_real(det_([[k, 2], [2, k]]), k))),
  values=[Complement(S.Reals, FiniteSet(-2, 2)), Complement(S.Reals, FiniteSet(2)), FiniteSet(-2, 2),
          Complement(S.Reals, FiniteSet(4))],
  cognitive="Application", source_class="XII")

q("U03-D-009", TOPIC, "Cramer's rule: inconsistent case", "Easy", "Direct concept MCQ",
  r"For a system of three linear equations in three unknowns, let $\Delta$ be the determinant of the coefficient matrix and $\Delta_1, \Delta_2, \Delta_3$ the determinants obtained by replacing its first, second and third columns by the constants. If $\Delta = 0$ and at least one of $\Delta_1, \Delta_2, \Delta_3$ is non-zero, then the system",
  r"has no solution",
  [(r"has a unique solution", r"Takes a non-zero $\Delta_i$ as enough for a unique solution; a unique solution needs $\Delta \ne 0$."),
   (r"has infinitely many solutions", r"Treats every case with $\Delta = 0$ as giving infinitely many solutions."),
   (r"has only the trivial solution", r"Applies a homogeneous-system idea; here the constants are not all zero, so $(0, 0, 0)$ is not even a solution.")],
  r"If a solution existed, Cramer's relations $x\Delta = \Delta_1$, $y\Delta = \Delta_2$, $z\Delta = \Delta_3$ would hold. With $\Delta = 0$ the left sides are all $0$, contradicting a non-zero $\Delta_i$. Hence the system is inconsistent and has no solution.",
  r"Believing that $\Delta = 0$ always means infinitely many solutions.",
  "U03-D-concept-cramer", "Direct recall of the inconsistency criterion.",
  cognitive="Recall", source_class="XII")


def _c10():
    rows = [[1, 1, 1], [1, 2, 3], [3, 5, 7]]
    assert det_(rows) == 0
    return only(solve(consist_expr(rows, [1, 2, mu]), mu))


q("U03-D-010", TOPIC, "Infinitely many solutions: finding the constant", "Easy", "Inverse/parameter MCQ",
  r"If the system $x + y + z = 1$, $x + 2y + 3z = 2$, $3x + 5y + 7z = \mu$ has infinitely many solutions, then $\mu$ equals",
  r"$5$",
  [(r"$3$", r"Assumes the third equation is the sum of the first two and adds the constants $1 + 2$."),
   (r"$4$", r"Assumes the third row is $2R_1 + R_2$ and takes $\mu = 2(1) + 2$."),
   (r"$1$", r"Solves $a + b = 3$, $a + 2b = 5$ for $R_3 = aR_1 + bR_2$ with a sign slip, $b = -2$, $a = 5$, then $\mu = 5(1) - 2(2)$.")],
  r"Here $\Delta = 0$, and the coefficients satisfy $(3, 5, 7) = 1(1, 1, 1) + 2(1, 2, 3)$, so $R_3 = R_1 + 2R_2$. For infinitely many solutions the constants must obey the same relation: $\mu = 1 + 2(2) = 5$.",
  r"Guessing the row relation instead of solving for it.",
  "U03-D-infinite-param", "Spotting one linear relation among the rows.",
  check=_c10, values=[5, 3, 4, 1], cognitive="Application", source_class="XII")


def _c11():
    sol = solve([x + 2 * y - 5, 3 * x - y - 1], [x, y])
    return only(solve(k * sol[x] + sol[y] - 4, k))


q("U03-D-011", TOPIC, "Three equations in two unknowns", "Easy", "Inverse/parameter MCQ",
  r"The equations $x + 2y = 5$, $3x - y = 1$ and $kx + y = 4$ have a common solution. Then $k$ equals",
  r"$2$",
  [(r"$-2$", r"Copies the second equation as $3x + y = 1$, getting $x = -\frac{3}{5}$, $y = \frac{14}{5}$, and then $k = -2$."),
   (r"$\frac{3}{2}$", r"Solves the first two equations correctly but substitutes the values interchanged, $x = 2$, $y = 1$."),
   (r"$4$", r"Substitutes $x = 1$ but drops the $y$ term, writing $k(1) = 4$.")],
  r"The first two equations give $x = 1$, $y = 2$ (from $x + 2y = 5$ and $6x - 2y = 2$, adding gives $7x = 7$). Substituting in the third, $k + 2 = 4$, so $k = 2$.",
  r"Careless solving of the first pair before substituting.",
  "U03-D-2var-3eqn", "Solve a $2 \\times 2$ system and substitute.",
  check=_c11, values=[2, -2, Rational(3, 2), 4], cognitive="Application", source_class="XII")

q("U03-D-012", TOPIC, "Parameter for an inconsistent system", "Easy", "Inverse/parameter MCQ",
  r"The system $x + y + z = 2$, $2x + y - z = 3$, $3x + 2y + kz = 4$ has no solution. Then $k$ equals",
  r"$0$",
  [(r"$-2$", r"Uses $+$ for the middle cofactor: $(k + 2) + (2k + 3) + 1 = 3k + 6$."),
   (r"$-4$", r"Evaluates the first minor as $k - 2$ instead of $k + 2$, so $\Delta = -k - 4$."),
   (r"$6$", r"Evaluates the middle minor as $2k - 3$ instead of $2k + 3$, so $\Delta = -k + 6$.")],
  r"$\Delta = 1(k + 2) - 1(2k + 3) + 1(4 - 3) = -k$, so a unique solution exists unless $k = 0$. At $k = 0$, the third coefficient row $(3, 2, 0)$ equals $R_1 + R_2$, but the constants give $2 + 3 = 5 \ne 4$. So the system is inconsistent exactly when $k = 0$.",
  r"Sign slips in the cofactor expansion.",
  "U03-D-none-param", "One expansion and a consistency check at the root.",
  check=lambda: only(param_set([[1, 1, 1], [2, 1, -1], [3, 2, k]], [2, 3, 4], k, "none")),
  values=[0, -2, -4, 6], cognitive="Application", source_class="XII")

q("U03-D-013", TOPIC, "Word problem by the matrix method", "Easy", "Multi-step computation MCQ",
  r"The sum of three numbers is $15$. Twice the first number exceeds the second number by $3$, and the second number added to twice the third number gives $17$. Solving the resulting system, the third number is",
  r"$6$",
  [(r"$\frac{9}{2}$", r"Writes the second condition as $y - 2x = 3$; with $x + y + z = 15$ and $y + 2z = 17$ this gives $z = \frac{9}{2}$."),
   (r"$3$", r"Writes the third condition as $2y + z = 17$; with the other two equations this gives $(5, 7, 3)$."),
   (r"$\frac{39}{5}$", r"Writes the second condition as $x - 2y = 3$; with the other two equations this gives $z = \frac{39}{5}$.")],
  r"With numbers $x, y, z$: $x + y + z = 15$, $2x - y = 3$, $y + 2z = 17$. From the second, $y = 2x - 3$; then $z = \frac{17 - y}{2} = 10 - x$. Substituting, $x + 2x - 3 + 10 - x = 15$, so $x = 4$, $y = 5$, $z = 6$.",
  r"Translating a verbal condition into the wrong equation.",
  "U03-D-word-problem", "Forming and solving a simple $3 \\times 3$ system.",
  check=lambda: list(linsolve([x + y + z - 15, 2 * x - y - 3, y + 2 * z - 17], XYZ))[0][2],
  values=[6, Rational(9, 2), 3, Rational(39, 5)],
  numerical=dict(question=r"The sum of three numbers is $15$. Twice the first number exceeds the second number by $3$, and the second number added to twice the third number gives $17$. The third number is", answer=6),
  cognitive="Application", source_class="XII")


def _c14():
    al, be, ga = list(linsolve([2 * x + y - z - 2, x - y + 2 * z - 7, 3 * x + 2 * y + z - 11], XYZ))[0]
    return al + 2 * be + 3 * ga


q("U03-D-014", TOPIC, "Solving a $3 \\times 3$ system", "Easy", "Multi-step computation MCQ",
  r"If $(\alpha, \beta, \gamma)$ is the solution of $2x + y - z = 2$, $x - y + 2z = 7$, $3x + 2y + z = 11$, then $\alpha + 2\beta + 3\gamma$ equals",
  r"$13$",
  [(r"$11$", r"Finds $(2, 1, 3)$ correctly but attaches the weights in reverse order, $3\alpha + 2\beta + \gamma$."),
   (r"$5$", r"Copies the second equation as $x - y - 2z = 7$, which gives $(8, -9, 5)$."),
   (r"$40$", r"Copies the third equation as $3x + 2y - z = 11$, which gives $(\frac{1}{2}, \frac{17}{2}, \frac{15}{2})$.")],
  r"Adding the first and third equations gives $5x + 3y = 13$; adding twice the first to the second gives $5x + y = 11$. Hence $y = 1$, $x = 2$ and $z = 2x + y - 2 = 3$. So $\alpha + 2\beta + 3\gamma = 2 + 2 + 9 = 13$.",
  r"Sign errors while copying or eliminating.",
  "U03-D-unique-solve", "Routine elimination in three variables.",
  check=_c14, values=[13, 11, 5, 40],
  numerical=dict(question=r"If $(\alpha, \beta, \gamma)$ is the solution of $2x + y - z = 2$, $x - y + 2z = 7$, $3x + 2y + z = 11$, then the value of $\alpha + 2\beta + 3\gamma$ is", answer=13),
  cognitive="Application", source_class="XII")

q("U03-D-015", TOPIC, "Homogeneous system with only the trivial solution", "Easy", "Inverse/parameter MCQ",
  r"The homogeneous system $x + y + z = 0$, $2x - y + 3z = 0$, $x + ky - 2z = 0$, where $k$ is real, has only the trivial solution if and only if",
  r"$k \ne 10$",
  [(r"$k = 10$", r"Uses $\Delta = 0$, which is the condition for non-trivial solutions."),
   (r"$k \ne -4$", r"Uses $+$ for the middle cofactor: $(2 - 3k) + (-7) + (2k + 1) = -k - 4$."),
   (r"$k \ne \frac{8}{5}$", r"Writes the third minor as $-(2k + 1)$ (order reversed), so $\Delta = (2 - 3k) + 7 - (2k + 1) = 8 - 5k$.")],
  r"Only the trivial solution occurs if and only if $\Delta \ne 0$. $\Delta = 1(2 - 3k) - 1(-4 - 3) + 1(2k + 1) = 10 - k$, so the condition is $k \ne 10$.",
  r"Reversing the criterion: $\Delta \ne 0$ gives only the trivial solution.",
  "U03-D-homog-trivial", r"One expansion plus the criterion $\Delta \ne 0$.",
  check=lambda: Complement(S.Reals, FiniteSet(*roots_real(det_([[1, 1, 1], [2, -1, 3], [1, k, -2]]), k))),
  values=[Complement(S.Reals, FiniteSet(10)), FiniteSet(10), Complement(S.Reals, FiniteSet(-4)),
          Complement(S.Reals, FiniteSet(Rational(8, 5)))],
  cognitive="Application", source_class="XII")


def _c16():
    rows = [[1, 1, -1], [1, -2, 1], [3, 6, -5]]
    assert det_(rows) == 0
    return ratio(rows)


q("U03-D-016", TOPIC, "Ratio of a non-trivial solution", "Easy", "Single-step computation MCQ",
  r"The system $x + y - z = 0$, $x - 2y + z = 0$, $3x + 6y - 5z = 0$ has non-trivial solutions. For any such solution, $x : y : z$ equals",
  r"$1 : 2 : 3$",
  [(r"$3 : 2 : 1$", r"Finds the right numbers but lists them as $z : y : x$."),
   (r"$1 : -2 : 3$", r"Cross-multiplies the first two equations with a sign slip in the middle component, getting $(-1, 2, -3)$."),
   (r"$1 : 2 : -3$", r"Cross-multiplies with the last component as $a_2b_1 - a_1b_2 = 3$, getting $(-1, -2, 3)$.")],
  r"Cross-multiplying the first two equations: $\frac{x}{(1)(1) - (-1)(-2)} = \frac{y}{(-1)(1) - (1)(1)} = \frac{z}{(1)(-2) - (1)(1)}$, i.e. $\frac{x}{-1} = \frac{y}{-2} = \frac{z}{-3}$. So $x : y : z = 1 : 2 : 3$, which also satisfies $3 + 12 - 15 = 0$.",
  r"Sign slips in the cross-multiplication rule.",
  "U03-D-homog-ratio", "One cross-multiplication.",
  check=_c16, values=[(1, 2, 3), (1, Rational(2, 3), Rational(1, 3)), (1, -2, 3), (1, 2, -3)],
  cognitive="Application", source_class="XII")

# ============================ MEDIUM ============================

q("U03-D-017", TOPIC, "Homogeneous system with the parameter on the diagonal", "Medium", "Inverse/parameter MCQ",
  r"The system $x + 2y + 2z = \lambda x$, $2x + y + 2z = \lambda y$, $2x + 2y + z = \lambda z$ has a non-trivial solution. The set of all real $\lambda$ for which this happens is",
  r"$\{-1, 5\}$",
  [(r"$\{1, -5\}$", r"Moves $\lambda$ to the wrong side, so the diagonal becomes $1 + \lambda$ and the roots change sign."),
   (r"$\{5\}$", r"Takes out the factor $(5 - \lambda)$ from the row sum and stops, not solving $(1 + \lambda)^2 = 0$."),
   (r"$\{1\}$", r"Sets each diagonal entry $1 - \lambda$ equal to $0$ instead of the determinant.")],
  r"Rewrite as $(1 - \lambda)x + 2y + 2z = 0$ and so on. Adding all rows of the coefficient determinant gives the common factor $(5 - \lambda)$; then subtracting the first column from the others leaves $(1 + \lambda)^2$. So $\Delta = (5 - \lambda)(1 + \lambda)^2 = 0$, giving $\lambda = 5$ or $\lambda = -1$.",
  r"Not rewriting the system as a homogeneous one, or losing a factor while simplifying.",
  "U03-D-homog-lambda-diag", "Rearranging into homogeneous form and factorising a cubic determinant.",
  check=lambda: FiniteSet(*roots_real(det_([[1 - lam, 2, 2], [2, 1 - lam, 2], [2, 2, 1 - lam]]), lam)),
  values=[FiniteSet(-1, 5), FiniteSet(1, -5), FiniteSet(5), FiniteSet(1)],
  cognitive="Application", source_class="XII")


def _c18():
    P = Matrix([[1, 2, 1], [2, -1, 1], [1, 1, -1]]); R = Matrix([[0, 3, 3], [3, -2, 1], [3, 1, -5]])
    assert P * R == 9 * eye(3)
    sol = list(linsolve([x + 2 * y + z - 5, 2 * x - y + z - 3, x + y - z], XYZ))[0]
    return sum(sol)


q("U03-D-018", TOPIC, "Matrix method using a given product", "Medium", "Multi-step computation MCQ",
  r"Let $P = \begin{bmatrix} 1 & 2 & 1 \\ 2 & -1 & 1 \\ 1 & 1 & -1 \end{bmatrix}$ and $R = \begin{bmatrix} 0 & 3 & 3 \\ 3 & -2 & 1 \\ 3 & 1 & -5 \end{bmatrix}$, so that $PR = 9I$. If $x + 2y + z = 5$, $2x - y + z = 3$ and $x + y - z = 0$, then $x + y + z$ equals",
  r"$4$",
  [(r"$36$", r"Takes $X = R\begin{bmatrix} 5 \\ 3 \\ 0 \end{bmatrix}$, forgetting that $P^{-1} = \frac{1}{9}R$."),
   (r"$\frac{26}{9}$", r"Multiplies the constants by $\frac{1}{9}P$ instead of $\frac{1}{9}R$."),
   (r"$\frac{4}{9}$", r"Divides $R\begin{bmatrix} 5 \\ 3 \\ 0 \end{bmatrix}$ by $81$, confusing $9$ with $|\operatorname{adj} P| = 81$.")],
  r"The system is $PX = \begin{bmatrix} 5 \\ 3 \\ 0 \end{bmatrix}$. From $PR = 9I$, $P^{-1} = \frac{1}{9}R$, so $X = \frac{1}{9}\begin{bmatrix} 0 + 9 + 0 \\ 15 - 6 + 0 \\ 15 + 3 + 0 \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \\ 2 \end{bmatrix}$. Hence $x + y + z = 4$.",
  r"Using $R$ itself as the inverse, ignoring the scalar.",
  "U03-D-matrix-method-given-inverse", "Reading the inverse from $PR = 9I$ and one matrix product.",
  check=_c18, values=[4, 36, Rational(26, 9), Rational(4, 9)], cognitive="Application", source_class="XII")


def _c19():
    rows = [[1, 2, 1], [2, 1, 3], [3, 3, lam]]
    l0 = only(roots_real(det_(rows), lam))
    m0 = only(solve(consist_expr(subs_rows(rows, lam, l0), [4, 5, mu]), mu))
    assert kind(subs_rows(rows, lam, l0), [4, 5, m0 + 1]) == "none"
    return (FiniteSet(l0), Complement(S.Reals, FiniteSet(m0)))


q("U03-D-019", TOPIC, "Classifying by two parameters", "Medium", "Inverse/parameter MCQ",
  r"The system $x + 2y + z = 4$, $2x + y + 3z = 5$, $3x + 3y + \lambda z = \mu$ has no solution if and only if",
  r"$\lambda = 4,\ \mu \ne 9$",
  [(r"$\lambda = 4,\ \mu = 9$", r"Gives the condition for infinitely many solutions instead."),
   (r"$\lambda \ne 4,\ \mu = 9$", r"Takes $\Delta \ne 0$ as the failing case; then the solution is in fact unique."),
   (r"$\lambda = 2,\ \mu \ne 9$", r"Writes the third minor of $\Delta$ as $3 - 6 = -3$ (order reversed), so $\Delta = (\lambda - 9) - 2(2\lambda - 9) - 3 = -3\lambda + 6$.")],
  r"$\Delta = 1(\lambda - 9) - 2(2\lambda - 9) + 1(6 - 3) = -3\lambda + 12$, so a unique solution exists unless $\lambda = 4$. At $\lambda = 4$ the third coefficient row $(3, 3, 4)$ equals $R_1 + R_2$, so the system is consistent only when $\mu = 4 + 5 = 9$. Hence there is no solution exactly when $\lambda = 4$ and $\mu \ne 9$.",
  r"Mixing up the conditions for no solution and for infinitely many solutions.",
  "U03-D-lambda-mu-classify", "Determinant condition plus a row relation for the constants.",
  check=_c19,
  values=[(FiniteSet(4), Complement(S.Reals, FiniteSet(9))), (FiniteSet(4), FiniteSet(9)),
          (Complement(S.Reals, FiniteSet(4)), FiniteSet(9)), (FiniteSet(2), Complement(S.Reals, FiniteSet(9)))],
  cognitive="Analysis", source_class="XII")


def _c20():
    rows = [[1, 1, -1], [1, -1, 3], [3, 1, lam]]
    l0 = only(roots_real(det_(rows), lam))
    m0 = only(solve(consist_expr(subs_rows(rows, lam, l0), [2, 3, mu]), mu))
    return l0 + m0


q("U03-D-020", TOPIC, "Infinitely many solutions with two parameters", "Medium", "Inverse/parameter MCQ",
  r"If the system $x + y - z = 2$, $x - y + 3z = 3$, $3x + y + \lambda z = \mu$ has infinitely many solutions, then $\lambda + \mu$ equals",
  r"$8$",
  [(r"$6$", r"Finds $\lambda = 1$ but takes $\mu = 2 + 3 = 5$, assuming $R_3 = R_1 + R_2$ for the constants."),
   (r"$11$", r"Evaluates the first minor as $-\lambda + 3$ instead of $-\lambda - 3$, so $\Delta = -2\lambda + 8$ and $\lambda = 4$; then takes $\mu = 7$ by matching only the $x$ and $y$ coefficients ($R_3 = 2R_1 + R_2$ on the first two columns), giving $4 + 7 = 11$."),
   (r"$9$", r"Finds $\lambda = 1$ but swaps the multipliers for the constants, $\mu = 2 + 2(3) = 8$.")],
  r"$\Delta = 1(-\lambda - 3) - 1(\lambda - 9) - 1(1 + 3) = -2\lambda + 2$, so $\lambda = 1$. Then $(3, 1, 1) = 2(1, 1, -1) + 1(1, -1, 3)$, so $R_3 = 2R_1 + R_2$ and the constants require $\mu = 2(2) + 3 = 7$. Hence $\lambda + \mu = 8$.",
  r"Assuming the row relation instead of finding the multipliers.",
  "U03-D-lambda-mu-classify", "Determinant equation plus a row combination for the constants.",
  check=_c20, values=[8, 6, 11, 9],
  numerical=dict(question=r"If the system $x + y - z = 2$, $x - y + 3z = 3$, $3x + y + \lambda z = \mu$ has infinitely many solutions, then the value of $\lambda + \mu$ is", answer=8),
  cognitive="Application", source_class="XII")

q("U03-D-021", TOPIC, "Cyclic system with a parameter", "Medium", "Inverse/parameter MCQ",
  r"The system $kx + y + z = 1$, $x + ky + z = k$, $x + y + kz = k^2$, where $k$ is real, has no solution",
  r"only when $k = -2$",
  [(r"only when $k = 1$", r"Treats $k = 1$ as inconsistent; there all three equations become $x + y + z = 1$, giving infinitely many solutions."),
   (r"when $k = 1$ or $k = -2$", r"Takes every root of $\Delta = 0$ as a case of no solution without checking the constants."),
   (r"only when $k = 2$", r"Factorises $\Delta = (k - 1)^2(k + 2)$ correctly but reads the root of $k + 2 = 0$ as $2$.")],
  r"$\Delta = (k - 1)^2(k + 2)$. For $k = 1$ every equation is $x + y + z = 1$, so there are infinitely many solutions. For $k = -2$, adding the equations gives $(k + 2)(x + y + z) = 1 + k + k^2$, i.e. $0 = 3$, a contradiction. So the system has no solution only for $k = -2$.",
  r"Assuming $\Delta = 0$ always means no solution.",
  "U03-D-cyclic-k", "Factorising a symmetric determinant and checking each root.",
  check=lambda: param_set([[k, 1, 1], [1, k, 1], [1, 1, k]], [1, k, k**2], k, "none"),
  values=[FiniteSet(-2), FiniteSet(1), FiniteSet(1, -2), FiniteSet(2)],
  cognitive="Analysis", source_class="XII")


def _c22():
    rows = [[1, 1, 1], [1, 2, 3], [1, 3, 5]]
    assert det_(rows) == 0
    e = consist_expr(rows, [a, b, c])
    return expand(e / e.coeff(a))


q("U03-D-022", TOPIC, "Consistency condition on the constants", "Medium", "Conceptual/application MCQ",
  r"The system $x + y + z = a$, $x + 2y + 3z = b$, $x + 3y + 5z = c$ is consistent if and only if",
  r"$a, b, c$ are in A.P.",
  [(r"$a, b, c$ are in G.P.", r"Mixes up the arithmetic-mean relation $2b = a + c$ with the geometric-mean relation $b^2 = ac$."),
   (r"$a, b, c$ are in H.P.", r"Mixes up the arithmetic-mean relation with the harmonic-mean relation $b = \frac{2ac}{a + c}$."),
   (r"$a + b = c$", r"Assumes $R_3 = R_1 + R_2$ without checking: $R_1 + R_2 = (2, 3, 4) \ne (1, 3, 5)$.")],
  r"The coefficient rows satisfy $R_1 + R_3 = (2, 4, 6) = 2R_2$, so $\Delta = 0$ and every solution would force $a + c = 2b$. Conversely, if $a + c = 2b$, the third equation follows from the first two, which are independent, so solutions exist. Hence the system is consistent exactly when $a, b, c$ are in A.P.",
  r"Guessing a row relation instead of finding it.",
  "U03-D-consistency-constants", "Finding the row relation and translating it into a progression.",
  check=_c22, values=[a - 2 * b + c, b**2 - a * c, b * (a + c) - 2 * a * c, a + b - c],
  cognitive="Analysis", source_class="XII")


def _c23():
    D = factor(det_([[a, b, c], [b, c, a], [c, a, b]]))
    lin = [f for f, _ in factor_list(D)[1] if Poly(f, a, b, c).total_degree() == 1]
    assert len(lin) == 1
    cval = only(solve(lin[0], c))
    return simplify((a**3 + b**3 + cval**3) / (a * b * cval))


q("U03-D-023", TOPIC, "Cyclic homogeneous system", "Medium", "Multi-step computation MCQ",
  r"Let $a$, $b$, $c$ be distinct non-zero real numbers such that the system $ax + by + cz = 0$, $bx + cy + az = 0$, $cx + ay + bz = 0$ has a non-trivial solution. Then $\frac{a^3 + b^3 + c^3}{abc}$ equals",
  r"$3$",
  [(r"$-3$", r"Expands the determinant as $a^3 + b^3 + c^3 + 3abc$ (sign slip on the $abc$ terms) and sets it to zero."),
   (r"$0$", r"Correctly gets $a + b + c = 0$ but then assumes $a^3 + b^3 + c^3 = 0$ as well."),
   (r"$1$", r"Counts the $abc$ term once instead of three times, writing $\Delta = abc - (a^3 + b^3 + c^3)$.")],
  r"$\Delta = 3abc - a^3 - b^3 - c^3 = -(a + b + c)(a^2 + b^2 + c^2 - ab - bc - ca)$. Since $a, b, c$ are distinct, the second factor $\frac{1}{2}[(a - b)^2 + (b - c)^2 + (c - a)^2]$ is positive, so a non-trivial solution forces $a + b + c = 0$. Then $a^3 + b^3 + c^3 = 3abc$, and the ratio is $3$.",
  r"Believing $a + b + c = 0$ makes the sum of cubes vanish.",
  "U03-D-homog-cyclic", "Factorising a circulant determinant and using an algebraic identity.",
  check=_c23, values=[3, -3, 0, 1], cognitive="Analysis", source_class="XII")

q("U03-D-024", TOPIC, "Parameter set for an inconsistent system", "Medium", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which the system $2x + y + z = 1$, $x + 3y + 2z = 2$, $x - y + k^2 z = 3$ has no solution is",
  r"$\emptyset$",
  [(r"$\left\{-\sqrt{\frac{2}{7}}, \sqrt{\frac{2}{7}}\right\}$", r"Uses $+$ for the middle cofactor: $2(3k^2 + 2) + (k^2 - 2) - 4 = 7k^2 - 2$."),
   (r"$\left\{-\sqrt{\frac{6}{5}}, \sqrt{\frac{6}{5}}\right\}$", r"Evaluates the first minor as $3k^2 - 2$, so $\Delta = 2(3k^2 - 2) - (k^2 - 2) - 4 = 5k^2 - 6$."),
   (r"$\{0\}$", r"Thinks that $k = 0$, which removes $z$ from the third equation, makes the system inconsistent.")],
  r"$\Delta = 2(3k^2 + 2) - 1(k^2 - 2) + 1(-1 - 3) = 5k^2 + 2$, which is positive for every real $k$. So the system always has a unique solution, and the required set is empty.",
  r"Expecting every parametric system to fail for some value.",
  "U03-D-none-param", "Expansion followed by recognising a sum of squares that never vanishes.",
  check=lambda: param_set([[2, 1, 1], [1, 3, 2], [1, -1, k**2]], [1, 2, 3], k, "none"),
  values=[S.EmptySet, FiniteSet(-sqrt(Rational(2, 7)), sqrt(Rational(2, 7))),
          FiniteSet(-sqrt(Rational(6, 5)), sqrt(Rational(6, 5))), FiniteSet(0)],
  cognitive="Analysis", source_class="XII")


def _c25():
    rows = [[1, 1, 1], [1, 2, 3], [2, 3, lam]]
    l0 = only(roots_real(det_(rows), lam))
    assert kind(subs_rows(rows, lam, l0), [3, 4, 7]) == "inf"
    sol = solve([x + y + 1 - 3, x + 2 * y + 3 - 4, 2 * x + 3 * y + l0 - 7], [x, y])
    return l0 + sol[x]


q("U03-D-025", TOPIC, "A particular solution in the infinite case", "Medium", "Multi-step computation MCQ",
  r"The system $x + y + z = 3$, $x + 2y + 3z = 4$, $2x + 3y + \lambda z = 7$ has infinitely many solutions, and $(\alpha, \beta, 1)$ is one of them. Then $\lambda + \alpha$ equals",
  r"$7$",
  [(r"$6$", r"Finds $\lambda = 4$ but ignores $z$ in the first two equations, solving $x + y = 3$, $x + 2y = 4$ to get $\alpha = 2$."),
   (r"$5$", r"Finds $\lambda = 4$ but moves the $z$ terms with the wrong sign, solving $x + y = 4$, $x + 2y = 7$ to get $\alpha = 1$."),
   (r"$\frac{25}{3}$", r"Uses $+$ for the middle cofactor: $(2\lambda - 9) + (\lambda - 6) - 1 = 3\lambda - 16$, so $\lambda = \frac{16}{3}$; with $\alpha = 3$ this gives $\frac{25}{3}$.")],
  r"$\Delta = 1(2\lambda - 9) - 1(\lambda - 6) + 1(3 - 4) = \lambda - 4$, so $\lambda = 4$, and then $R_3 = R_1 + R_2$ with $7 = 3 + 4$, so the system indeed has infinitely many solutions. With $z = 1$: $x + y = 2$ and $x + 2y = 1$, so $y = -1$, $x = 3$. Hence $\lambda + \alpha = 4 + 3 = 7$.",
  r"Mishandling the known value of $z$ while solving.",
  "U03-D-infinite-solution-set", "Determinant condition plus solving for a particular solution.",
  check=_c25, values=[7, 6, 5, Rational(25, 3)], cognitive="Application", source_class="XII")


def _c26():
    rows = [[1, 1, 1], [1, -1, k], [1, 1, k**2]]
    return sum(1 for kv in range(-10, 11) if Matrix(subs_rows(rows, k, kv)).det() != 0)


q("U03-D-026", TOPIC, "Counting parameter values for a unique solution", "Medium", "Multi-step computation MCQ",
  r"The number of integers $k$ in $[-10, 10]$ for which the system $x + y + z = 1$, $x - y + kz = 2$, $x + y + k^2 z = 3$ has a unique solution is",
  r"$19$",
  [(r"$20$", r"Uses $+$ for the middle cofactor, getting $\Delta = -2k + 2$, so only $k = 1$ is excluded."),
   (r"$21$", r"Writes the third minor as $-2$ (order reversed), getting $\Delta = -2k^2 - 2$, which never vanishes."),
   (r"$2$", r"Counts the excluded values $k = \pm 1$ instead of the allowed ones.")],
  r"$\Delta = 1(-k^2 - k) - 1(k^2 - k) + 1(1 + 1) = 2 - 2k^2 = -2(k - 1)(k + 1)$. A unique solution needs $k \ne \pm 1$. Of the $21$ integers in $[-10, 10]$, two are excluded, leaving $19$.",
  r"Sign slips in the expansion, or counting the wrong set.",
  "U03-D-count-unique", "Expansion, factorisation and counting.",
  check=_c26, values=[19, 20, 21, 2],
  numerical=dict(question=r"The number of integers $k$ in $[-10, 10]$ for which the system $x + y + z = 1$, $x - y + kz = 2$, $x + y + k^2 z = 3$ has a unique solution is", answer=19),
  cognitive="Application", source_class="XII")

q("U03-D-027", TOPIC, "Homogeneous system with a parameter", "Medium", "Inverse/parameter MCQ",
  r"If the system $kx + y + 2z = 0$, $x + ky + z = 0$, $x + y + z = 0$ has a non-trivial solution, then the sum of all possible values of $k$ is",
  r"$3$",
  [(r"$-3$", r"Gets $\Delta = k^2 - 3k + 2$ but takes the sum of roots as $+\frac{b}{a} = -3$."),
   (r"$2$", r"Gives the product of the roots of $k^2 - 3k + 2 = 0$ instead of their sum."),
   (r"$1$", r"Notices that $k = 1$ makes the second and third equations identical and stops, missing $k = 2$.")],
  r"$\Delta = k(k - 1) - 1(1 - 1) + 2(1 - k) = k^2 - 3k + 2 = (k - 1)(k - 2)$. Non-trivial solutions need $\Delta = 0$, so $k = 1$ or $k = 2$, and the sum is $3$.",
  r"Sign error in the sum of roots.",
  "U03-D-homog-nontrivial", "Expansion to a quadratic and sum of its roots.",
  check=lambda: sum(roots_real(det_([[k, 1, 2], [1, k, 1], [1, 1, 1]]), k)),
  values=[3, -3, 2, 1],
  numerical=dict(question=r"If the system $kx + y + 2z = 0$, $x + ky + z = 0$, $x + y + z = 0$ has a non-trivial solution, then the sum of all possible values of $k$ is", answer=3),
  cognitive="Application", source_class="XII")

q("U03-D-028", TOPIC, "Two-variable system with a quadratic determinant", "Medium", "Inverse/parameter MCQ",
  r"The system $(k + 3)x + 4y = k + 3$, $kx + (k - 1)y = 2k - 3$, where $k$ is real, has no solution",
  r"only when $k = -1$",
  [(r"only when $k = 3$", r"Swaps the two cases: at $k = 3$ the equations are $6x + 4y = 6$ and $3x + 2y = 3$, which coincide."),
   (r"when $k = -1$ or $k = 3$", r"Treats both roots of $\Delta = 0$ as inconsistent without comparing the constants."),
   (r"for no real $k$", r"Checks only $\frac{a_1}{a_2} = \frac{b_1}{b_2}$ at both roots and concludes that both give infinitely many solutions.")],
  r"$\Delta = (k + 3)(k - 1) - 4k = k^2 - 2k - 3 = (k - 3)(k + 1)$. At $k = 3$: $6x + 4y = 6$ and $3x + 2y = 3$ are the same line, so infinitely many solutions. At $k = -1$: $2x + 4y = 2$ and $-x - 2y = -5$, i.e. $x + 2y = 1$ and $x + 2y = 5$, which are parallel and distinct. So there is no solution only when $k = -1$.",
  r"Not checking the constants at each root of $\Delta$.",
  "U03-D-2var-quadratic", "Quadratic determinant plus casework at both roots.",
  check=lambda: param_set([[k + 3, 4], [k, k - 1]], [k + 3, 2 * k - 3], k, "none"),
  values=[FiniteSet(-1), FiniteSet(3), FiniteSet(-1, 3), S.EmptySet],
  cognitive="Analysis", source_class="XII")


def _c29():
    Pm = Matrix([[1, 1, 1]] * 3); Q = Matrix([1, 2, 3])
    adj_ok = (Pm.adjugate() * Q == zeros(3, 1))
    s1 = not (Pm.det() == 0 and adj_ok and kind(Pm.tolist(), list(Q)) == "none")
    # Statement II: |P| != 0 gives X = P^{-1}Q; verify on a generic invertible instance
    P2 = Matrix([[2, 1, 0], [1, 3, 1], [0, 1, 4]]); Q2 = Matrix([1, 2, 3])
    s2 = (P2.det() != 0 and kind(P2.tolist(), list(Q2)) == "unique"
          and list(linsolve((P2, Q2), XYZ))[0] == tuple(P2.inv() * Q2))
    return (s1, s2)


q("U03-D-029", TOPIC, "Adjoint test for consistency", "Medium", "Statement-based MCQ",
  r"Let $P$ be a $3 \times 3$ matrix, $Q$ a $3 \times 1$ matrix and $X = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$. Statement I: If $|P| = 0$ and $(\operatorname{adj} P)Q = O$, then the system $PX = Q$ has infinitely many solutions. Statement II: If $|P| \ne 0$, then the system $PX = Q$ has the unique solution $X = P^{-1}Q$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts the common textbook shortcut in Statement I without testing it on a system whose equations are all parallel planes."),
   (ST_TF, r"Accepts Statement I and also rejects the standard matrix-method result in Statement II."),
   (ST_FF, r"Rejects Statement II, perhaps thinking $P^{-1}Q$ need not satisfy $PX = Q$.")],
  r"Statement I is false. Take $x + y + z = 1$, $x + y + z = 2$, $x + y + z = 3$: every $2 \times 2$ minor of the all-ones matrix $P$ is $0$, so $\operatorname{adj} P = O$, $|P| = 0$ and $(\operatorname{adj} P)Q = O$, yet the system is clearly inconsistent. Statement II is true: if $|P| \ne 0$, then $P^{-1}$ exists, $X = P^{-1}Q$ satisfies $PX = Q$, and any solution must equal $P^{-1}Q$.",
  r"Treating $(\operatorname{adj} P)Q = O$ as sufficient for infinitely many solutions.",
  "U03-D-concept-adj", "Needs a counterexample to a widely quoted shortcut.",
  check=_c29, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Analysis", source_class="XII")


def _c30():
    P = Matrix([[4, 3, 3], [-1, 0, -1], [-4, -4, -3]])
    assert P * P == eye(3)
    return list(linsolve([4 * x + 3 * y + 3 * z - 1, -x - z, -4 * x - 4 * y - 3 * z + 2], XYZ))[0][1]


q("U03-D-030", TOPIC, "Matrix method with an involutory matrix", "Medium", "Multi-step computation MCQ",
  r"Let $P = \begin{bmatrix} 4 & 3 & 3 \\ -1 & 0 & -1 \\ -4 & -4 & -3 \end{bmatrix}$, for which $P^2 = I$. If $4x + 3y + 3z = 1$, $-x - z = 0$ and $-4x - 4y - 3z = -2$, then $y$ equals",
  r"$1$",
  [(r"$0$", r"Treats $P^2 = I$ as $P = I$ and takes $X$ equal to the constant column $(1, 0, -2)$."),
   (r"$-1$", r"Since $|P| = -1$, takes $P^{-1} = -P$, so $X = -P\begin{bmatrix} 1 \\ 0 \\ -2 \end{bmatrix}$."),
   (r"$11$", r"Uses $P^{-1} = P^T$, as if $P$ were orthogonal, and takes the second entry of $P^T\begin{bmatrix} 1 \\ 0 \\ -2 \end{bmatrix}$.")],
  r"The system is $PX = \begin{bmatrix} 1 \\ 0 \\ -2 \end{bmatrix}$. Since $P^2 = I$, $P^{-1} = P$, so $X = P\begin{bmatrix} 1 \\ 0 \\ -2 \end{bmatrix} = \begin{bmatrix} 4 - 6 \\ -1 + 2 \\ -4 + 6 \end{bmatrix} = \begin{bmatrix} -2 \\ 1 \\ 2 \end{bmatrix}$. Hence $y = 1$.",
  r"Confusing $P^2 = I$ with $P = I$ or with $PP^T = I$.",
  "U03-D-matrix-method-given-inverse", "Recognising $P^{-1} = P$ from $P^2 = I$, then one product.",
  check=_c30, values=[1, 0, -1, 11], cognitive="Application", source_class="XII")


def _c31():
    sol = list(linsolve([2 * x + 3 * y + z - 85, x + 2 * y + 3 * z - 65, 3 * x + y + 2 * z - 60], XYZ))[0]
    return sol[1]


q("U03-D-031", TOPIC, "Word problem by Cramer's rule", "Medium", "Multi-step computation MCQ",
  r"A shop sells pens, notebooks and erasers. $2$ pens, $3$ notebooks and $1$ eraser cost Rs $85$; $1$ pen, $2$ notebooks and $3$ erasers cost Rs $65$; $3$ pens, $1$ notebook and $2$ erasers cost Rs $60$. Using Cramer's rule, the cost (in Rs) of one notebook is",
  r"$20$",
  [(r"$10$", r"Replaces the first column of $\Delta$ by the constants; $\frac{\Delta_1}{\Delta}$ is the price of a pen."),
   (r"$5$", r"Replaces the third column of $\Delta$ by the constants; $\frac{\Delta_3}{\Delta}$ is the price of an eraser."),
   (r"$35$", r"Adds the three equations to get $6(p + n + e) = 210$ and stops at $p + n + e = 35$.")],
  r"With prices $p, n, e$: $2p + 3n + e = 85$, $p + 2n + 3e = 65$, $3p + n + 2e = 60$. Here $\Delta = 2(4 - 3) - 3(2 - 9) + 1(1 - 6) = 18$ and $\Delta_2 = 2(130 - 180) - 85(2 - 9) + 1(60 - 195) = 360$. So $n = \frac{360}{18} = 20$.",
  r"Replacing the wrong column in Cramer's rule.",
  "U03-D-word-problem", "Forming a $3 \\times 3$ system and two determinants.",
  check=_c31, values=[20, 10, 5, 35],
  numerical=dict(question=r"A shop sells pens, notebooks and erasers. $2$ pens, $3$ notebooks and $1$ eraser cost Rs $85$; $1$ pen, $2$ notebooks and $3$ erasers cost Rs $65$; $3$ pens, $1$ notebook and $2$ erasers cost Rs $60$. The cost (in Rs) of one notebook is", answer=20),
  cognitive="Application", source_class="XII")


def _c32():
    sol = solve([a * 1 - b + c - 6, 4 * a + 2 * b + c - 3, 9 * a + 3 * b + c - 10], [a, b, c])
    return sol[a] * 4 - 2 * sol[b] + sol[c]


q("U03-D-032", TOPIC, "Fitting a quadratic through three points", "Medium", "Multi-step computation MCQ",
  r"A quadratic $f(x) = ax^2 + bx + c$ satisfies $f(-1) = 6$, $f(2) = 3$ and $f(3) = 10$. Solving the resulting linear system for $a$, $b$, $c$, the value of $f(-2)$ is",
  r"$15$",
  [(r"$75$", r"Writes $f(-1) = 6$ as $a + b + c = 6$, which gives $a = 5$, $b = -18$, $c = 19$."),
   (r"$-1$", r"Finds $f(x) = 2x^2 - 3x + 1$ but evaluates $(-2)^2$ as $-4$."),
   (r"$3$", r"Finds $f(x) = 2x^2 - 3x + 1$ but evaluates $-3(-2)$ as $-6$.")],
  r"The conditions give $a - b + c = 6$, $4a + 2b + c = 3$, $9a + 3b + c = 10$. Subtracting in pairs: $3a + 3b = -3$ and $5a + b = 7$, so $a = 2$, $b = -3$, $c = 1$. Then $f(-2) = 8 + 6 + 1 = 15$.",
  r"Sign slips with negative arguments.",
  "U03-D-curve-fitting", "Setting up and solving a $3 \\times 3$ system, then evaluating.",
  check=_c32, values=[15, 75, -1, 3],
  numerical=dict(question=r"A quadratic $f(x) = ax^2 + bx + c$ satisfies $f(-1) = 6$, $f(2) = 3$ and $f(3) = 10$. The value of $f(-2)$ is", answer=15),
  cognitive="Application", source_class="XII")


def _c33():
    rows = [[1, 1, 1], [1, 2, 3], [1, 5, 9]]
    assert det_(rows) == 0
    return sum(roots_real(consist_expr(rows, [1, a, a**2]), a))


q("U03-D-033", TOPIC, "Consistency with a quadratic condition", "Medium", "Inverse/parameter MCQ",
  r"The system $x + y + z = 1$, $x + 2y + 3z = a$, $x + 5y + 9z = a^2$ is consistent. The sum of all real values of $a$ is",
  r"$4$",
  [(r"$3$", r"Solves $a^2 - 4a + 3 = 0$ correctly but gives the product of the roots, $3$, instead of their sum."),
   (r"$-4$", r"Reads the sum of the roots of $a^2 - 4a + 3 = 0$ as $-4$."),
   (r"$1$", r"Spots $a = 1$ (when all constants equal $1$) and misses $a = 3$.")],
  r"Here $\Delta = 0$ and $(1, 5, 9) = 4(1, 2, 3) - 3(1, 1, 1)$, so $R_3 = 4R_2 - 3R_1$. Consistency requires $a^2 = 4a - 3$, i.e. $(a - 1)(a - 3) = 0$. So $a = 1$ or $3$, with sum $4$.",
  r"Stopping at the obvious value of the parameter.",
  "U03-D-consistency-constants", "Row relation leading to a quadratic in the parameter.",
  check=_c33, values=[4, 3, -4, 1],
  numerical=dict(question=r"The system $x + y + z = 1$, $x + 2y + 3z = a$, $x + 5y + 9z = a^2$ is consistent. The sum of all real values of $a$ is", answer=4),
  cognitive="Application", source_class="XII")


def _c34():
    sol = list(linsolve([x + y + z - 3, x - y + z - 1, x + y + k * z - 5], XYZ))[0]
    return simplify(sol[2])


q("U03-D-034", TOPIC, "Solution in terms of a parameter", "Medium", "Single-step computation MCQ",
  r"For $k \ne 1$, the system $x + y + z = 3$, $x - y + z = 1$, $x + y + kz = 5$ has a unique solution, in which $z$ equals",
  r"$\frac{2}{k - 1}$",
  [(r"$\frac{2}{1 - k}$", r"Computes $\Delta = 2k - 2$ (sign slip) with $\Delta_3 = -4$."),
   (r"$\frac{k - 1}{2}$", r"Uses $\frac{\Delta}{\Delta_3}$, inverting Cramer's ratio."),
   (r"$\frac{2k - 4}{k - 1}$", r"Replaces the first column instead of the third, which gives $\frac{\Delta_1}{\Delta} = x$.")],
  r"Subtracting the first equation from the third gives $(k - 1)z = 2$, so $z = \frac{2}{k - 1}$. (By Cramer's rule, $\Delta = 2 - 2k$ and $\Delta_3 = -4$, giving the same value.)",
  r"Sign or column errors in Cramer's rule.",
  "U03-D-cramer-param", "One elimination, or two determinants.",
  check=_c34, values=[2 / (k - 1), 2 / (1 - k), (k - 1) / 2, (2 * k - 4) / (k - 1)],
  cognitive="Application", source_class="XII")

q("U03-D-035", TOPIC, "Structure of the solution set", "Medium", "Statement-based MCQ",
  r"Let $P$ be a $3 \times 3$ matrix, $Q$ a non-zero $3 \times 1$ matrix and $O$ the $3 \times 1$ zero matrix. Statement I: If $X_1$ and $X_2$ are two distinct solutions of $PX = Q$, then $X_1 + t(X_2 - X_1)$ is a solution of $PX = Q$ for every real $t$. Statement II: If $PX = Q$ has two distinct solutions, then $PX = O$ has a non-trivial solution. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Accepts Statement I but misses that $X_2 - X_1 \ne O$ is itself a non-trivial solution of $PX = O$."),
   (ST_FT, r"Thinks only $X_1$ and $X_2$ themselves can be solutions, overlooking linearity."),
   (ST_FF, r"Believes a linear system can have exactly two solutions.")],
  r"Since $PX_1 = PX_2 = Q$, we get $P(X_2 - X_1) = O$. Then $P(X_1 + t(X_2 - X_1)) = Q + tO = Q$ for all real $t$, so Statement I is true. Also $X_2 - X_1 \ne O$ satisfies $PX = O$, so Statement II is true.",
  r"Thinking a linear system can have exactly two solutions.",
  "U03-D-concept-solution-set", "Uses linearity to link non-homogeneous and homogeneous systems.",
  cognitive="Understanding", source_class="XII")


def _c36():
    P = Matrix([[2, -1, 3], [-1, 1, -2], [1, 1, 1]])
    Pinv = Matrix([[3, 4, -1], [-1, -1, 1], [-2, -3, 1]])
    assert P * Pinv == eye(3)
    sol = list(linsolve([2 * x - y + z - 3, -x + y + z - 4, 3 * x - 2 * y + z - 2], XYZ))[0]
    return sum(sol)


q("U03-D-036", TOPIC, "System whose coefficient matrix is a transpose", "Medium", "Multi-step computation MCQ",
  r"Let $P = \begin{bmatrix} 2 & -1 & 3 \\ -1 & 1 & -2 \\ 1 & 1 & 1 \end{bmatrix}$, for which $P^{-1} = \begin{bmatrix} 3 & 4 & -1 \\ -1 & -1 & 1 \\ -2 & -3 & 1 \end{bmatrix}$. If $2x - y + z = 3$, $-x + y + z = 4$ and $3x - 2y + z = 2$, then $x + y + z$ equals",
  r"$6$",
  [(r"$2$", r"Does not notice that the coefficient matrix is $P^T$ and uses $X = P^{-1}\begin{bmatrix} 3 \\ 4 \\ 2 \end{bmatrix} = (23, -5, -16)$."),
   (r"$14$", r"Multiplies the constants by $P$ itself, getting $(8, -3, 9)$."),
   (r"$10$", r"Multiplies the constants by $P^T$ (the coefficient matrix itself), getting $(4, 3, 3)$.")],
  r"The coefficient matrix of the system is $P^T$, so $X = (P^T)^{-1}Q = (P^{-1})^T Q$ with $Q = (3, 4, 2)$. Now $(P^{-1})^T = \begin{bmatrix} 3 & -1 & -2 \\ 4 & -1 & -3 \\ -1 & 1 & 1 \end{bmatrix}$, giving $X = (9 - 4 - 4,\ 12 - 4 - 6,\ -3 + 4 + 2) = (1, 2, 3)$. Hence $x + y + z = 6$.",
  r"Assuming the coefficient matrix is $P$ when it is $P^T$.",
  "U03-D-matrix-method-transpose", r"Recognising $P^T$ and using $(P^T)^{-1} = (P^{-1})^T$.",
  check=_c36, values=[6, 2, 14, 10], cognitive="Analysis", source_class="XII")


def _c37():
    return sum(r**2 for r in roots_real(det_([[lam, 1, 1], [1, lam, 2], [2, 2, lam]]), lam))


q("U03-D-037", TOPIC, "Homogeneous system with a cubic in the parameter", "Medium", "Multi-step computation MCQ",
  r"Let $S$ be the set of all real $\lambda$ for which the system $\lambda x + y + z = 0$, $x + \lambda y + 2z = 0$, $2x + 2y + \lambda z = 0$ has a non-trivial solution. The sum of the squares of the elements of $S$ is",
  r"$14$",
  [(r"$-14$", r"Uses $\sum \lambda^2 = (\sum \lambda)^2 + 2\sum \lambda_i\lambda_j = 0 + 2(-7)$."),
   (r"$0$", r"Computes $(\sum \lambda)^2$ instead of $\sum \lambda^2$."),
   (r"$7$", r"Uses $\sum \lambda^2 = -\sum \lambda_i\lambda_j$, dropping the factor $2$.")],
  r"$\Delta = \lambda(\lambda^2 - 4) - 1(\lambda - 4) + 1(2 - 2\lambda) = \lambda^3 - 7\lambda + 6 = (\lambda - 1)(\lambda - 2)(\lambda + 3)$. So $S = \{1, 2, -3\}$ and the sum of squares is $1 + 4 + 9 = 14$.",
  r"Misusing the identity for the sum of squares of roots.",
  "U03-D-homog-lambda-sum", "Cubic determinant, factorisation and a symmetric function.",
  check=_c37, values=[14, -14, 0, 7],
  numerical=dict(question=r"Let $S$ be the set of all real $\lambda$ for which the system $\lambda x + y + z = 0$, $x + \lambda y + 2z = 0$, $2x + 2y + \lambda z = 0$ has a non-trivial solution. The sum of the squares of the elements of $S$ is", answer=14),
  cognitive="Application", source_class="XII")


def _c38():
    rows = [[1, -1, 2], [2, 1, -1], [5, 4, a]]
    a0 = only(roots_real(det_(rows), a))
    b0 = only(solve(consist_expr(subs_rows(rows, a, a0), [1, 3, b]), b))
    return a0 + b0


q("U03-D-038", TOPIC, "Infinitely many solutions: coefficient and constant", "Medium", "Inverse/parameter MCQ",
  r"If the system $x - y + 2z = 1$, $2x + y - z = 3$, $5x + 4y + az = b$ has infinitely many solutions, then $a + b$ equals",
  r"$3$",
  [(r"$7$", r"Matches only the $x$-coefficient and assumes $R_3 = R_1 + 2R_2$, taking $a = 2 - 2 = 0$ and $b = 1 + 6 = 7$."),
   (r"$-5$", r"Finds $R_3 = -R_1 + 3R_2$ and $a = -5$ but swaps the multipliers on the constants, $b = -3 + 3 = 0$."),
   (r"$9$", r"Finds $R_3 = -R_1 + 3R_2$ but computes $a = -2 + 3 = 1$ (sign slip), with $b = 8$.")],
  r"Write $(5, 4) = p(1, -1) + q(2, 1)$: $p + 2q = 5$ and $-p + q = 4$ give $q = 3$, $p = -1$. Then $a = -1(2) + 3(-1) = -5$, which makes $\Delta = 0$, and infinitely many solutions require $b = -1(1) + 3(3) = 8$. Hence $a + b = 3$.",
  r"Assuming a row relation from one coefficient.",
  "U03-D-infinite-param", "Finding multipliers for the row relation, then applying it twice.",
  check=_c38, values=[3, 7, -5, 9],
  numerical=dict(question=r"If the system $x - y + 2z = 1$, $2x + y - z = 3$, $5x + 4y + az = b$ has infinitely many solutions, then the value of $a + b$ is", answer=3),
  cognitive="Application", source_class="XII")


def _c39():
    aug = Matrix([[1, 1, 3], [k, -1, 1], [1, k, 3]])
    good = [r for r in roots_real(aug.det(), k)
            if kind([[1, 1], [r, -1], [1, r]], [3, 1, 3]) != "none"]
    return 3 * sum(good)


q("U03-D-039", TOPIC, "Three equations in two unknowns", "Medium", "Inverse/parameter MCQ",
  r"Let $S$ be the sum of all real values of $k$ for which the equations $x + y = 3$, $kx - y = 1$ and $x + ky = 3$ have a common solution. Then $3S$ equals",
  r"$4$",
  [(r"$-4$", r"Gets $3k^2 - 4k + 1 = 0$ but takes the sum of roots as $-\frac{4}{3}$."),
   (r"$1$", r"Uses the product of the roots, $\frac{1}{3}$, instead of their sum."),
   (r"$3$", r"Keeps only $k = 1$, assuming a fractional $k$ cannot make the lines concurrent.")],
  r"Three equations in $x, y$ are consistent only if the $3 \times 3$ determinant of coefficients and constants vanishes: $1(-3 - k) - 1(3k - 1) + 3(k^2 + 1) = 3k^2 - 4k + 1 = (3k - 1)(k - 1) = 0$. For $k = 1$ the common solution is $(2, 1)$; for $k = \frac{1}{3}$ it is $(3, 0)$. So $S = \frac{4}{3}$ and $3S = 4$.",
  r"Dropping a valid root or using the wrong root relation.",
  "U03-D-2var-3eqn", "Augmented determinant, quadratic, and checking both roots.",
  check=_c39, values=[4, -4, 1, 3],
  numerical=dict(question=r"Let $S$ be the sum of all real values of $k$ for which the equations $x + y = 3$, $kx - y = 1$ and $x + ky = 3$ have a common solution. Then the value of $3S$ is", answer=4),
  cognitive="Application", source_class="XII")


def _c40():
    sol = solve([1 + y + z - 6, 1 - y + 2 * z - 5, 2 + y - z - k], [y, z, k])
    return sol[k]


q("U03-D-040", TOPIC, "Parameter from a known component", "Medium", "Inverse/parameter MCQ",
  r"The system $x + y + z = 6$, $x - y + 2z = 5$, $2x + y - z = k$ has a unique solution in which $x = 1$. Then $k$ equals",
  r"$1$",
  [(r"$3$", r"Finds $y = 2$, $z = 3$ but substitutes them interchanged in the third equation: $2 + 3 - 2$."),
   (r"$7$", r"Finds $y = 2$, $z = 3$ but evaluates $2x + y - z$ as $2 + 2 + 3$."),
   (r"$-\frac{1}{3}$", r"Moves $x$ with the wrong sign in the second equation, $-y + 2z = 6$, giving $z = \frac{11}{3}$, $y = \frac{4}{3}$.")],
  r"Put $x = 1$: $y + z = 5$ and $-y + 2z = 4$. Adding, $3z = 9$, so $z = 3$ and $y = 2$. Then $k = 2(1) + 2 - 3 = 1$. (The coefficient determinant is $7 \ne 0$, so the solution is indeed unique.)",
  r"Careless substitution after solving.",
  "U03-D-unique-extra-cond", "Substitute, solve a $2 \\times 2$ system, then evaluate.",
  check=_c40, values=[1, 3, 7, Rational(-1, 3)], cognitive="Application", source_class="XII")

# ============================ DIFFICULT ============================


def _c41():
    rows = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]; rhs = [1, 3, 5]
    P = Matrix(rows); Ds = []
    for j in range(3):
        M = P.copy(); M[:, j] = Matrix(rhs); Ds.append(M.det())
    all_zero = P.det() == 0 and all(v == 0 for v in Ds)
    kd = kind(rows, rhs)
    s1 = all_zero and kd == "inf"
    s2 = not (all_zero and kd == "none")
    return (s1, s2)


q("U03-D-041", TOPIC, "When all Cramer determinants vanish", "Difficult", "Statement-based MCQ",
  r"For a system of three linear equations in $x, y, z$, let $\Delta$ be the coefficient determinant and $\Delta_1, \Delta_2, \Delta_3$ the determinants obtained by replacing its columns by the constants. Statement I: For the system $x + y + z = 1$, $2x + 2y + 2z = 3$, $3x + 3y + 3z = 5$, we have $\Delta = \Delta_1 = \Delta_2 = \Delta_3 = 0$, so the system has infinitely many solutions. Statement II: For any such system, $\Delta = \Delta_1 = \Delta_2 = \Delta_3 = 0$ guarantees that the system is consistent. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts the popular shortcut that all four determinants being zero means infinitely many solutions."),
   (ST_TF, r"Verifies that the four determinants vanish and takes the conclusion of Statement I on trust."),
   (ST_FT, r"Sees that Statement I is inconsistent but still trusts the general shortcut in Statement II.")],
  r"In the given system all coefficient columns are equal, so $\Delta = 0$; in each $\Delta_i$ the two remaining coefficient columns are equal, so $\Delta_1 = \Delta_2 = \Delta_3 = 0$. Yet the first two equations say $x + y + z = 1$ and $x + y + z = \frac{3}{2}$, so the system has no solution. Statement I is false, and this same system is a counterexample to Statement II, which is also false.",
  r"Believing $\Delta = \Delta_1 = \Delta_2 = \Delta_3 = 0$ always gives infinitely many solutions.",
  "U03-D-concept-cramer-trap", "Requires seeing through a widely taught but false shortcut, with a counterexample.",
  check=_c41, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Analysis", source_class="XII")


def _c42():
    D = det_([[2 * sin(th), 1, 0], [1, 2 * sin(th), 1], [0, 1, 2 * sin(th)]])
    poly = expand(D.subs(sin(th), s))
    return count_sin(roots_real(poly, s), 0, 2 * pi)


q("U03-D-042", TOPIC, "Homogeneous system with a trigonometric parameter", "Difficult", "Multi-step computation MCQ",
  r"The number of values of $\theta \in [0, 2\pi]$ for which the system $(2\sin\theta)x + y = 0$, $x + (2\sin\theta)y + z = 0$, $y + (2\sin\theta)z = 0$ has a non-trivial solution is",
  r"$7$",
  [(r"$4$", r"Cancels the factor $\sin\theta$ from $\Delta = 4\sin\theta(2\sin^2\theta - 1)$, losing $\theta = 0, \pi, 2\pi$."),
   (r"$6$", r"Counts the solutions of $\sin\theta = 0$ as only $0$ and $\pi$, omitting the endpoint $2\pi$."),
   (r"$5$", r"Solves $2\sin^2\theta = 1$ as $\sin\theta = \frac{1}{\sqrt{2}}$ only, dropping $\sin\theta = -\frac{1}{\sqrt{2}}$.")],
  r"With $t = 2\sin\theta$, $\Delta = t(t^2 - 1) - 1(t) = t^3 - 2t = 4\sin\theta(2\sin^2\theta - 1)$. So $\sin\theta = 0$ gives $\theta = 0, \pi, 2\pi$, and $\sin\theta = \pm\frac{1}{\sqrt{2}}$ gives $\frac{\pi}{4}, \frac{3\pi}{4}, \frac{5\pi}{4}, \frac{7\pi}{4}$. In total $7$ values.",
  r"Cancelling a trigonometric factor, or missing endpoints or signs.",
  "U03-D-homog-trig", "Determinant in a trigonometric parameter, factorisation and careful counting on a closed interval.",
  check=_c42, values=[7, 4, 6, 5],
  numerical=dict(question=r"The number of values of $\theta \in [0, 2\pi]$ for which the system $(2\sin\theta)x + y = 0$, $x + (2\sin\theta)y + z = 0$, $y + (2\sin\theta)z = 0$ has a non-trivial solution is", answer=7),
  cognitive="Analysis", source_class="XII")


def _c43():
    rows = [[1, 1, -1], [2, -1, 1], [1, -2, lam]]
    cnt = 0
    for lv in range(1, 11):
        for mv in range(1, 11):
            if kind(subs_rows(rows, lam, lv), [2, 3, mv]) == "none":
                cnt += 1
    return cnt


q("U03-D-043", TOPIC, "Counting parameter pairs for no solution", "Difficult", "Multi-step computation MCQ",
  r"Let $\lambda, \mu \in \{1, 2, 3, \ldots, 10\}$. The number of ordered pairs $(\lambda, \mu)$ for which the system $x + y - z = 2$, $2x - y + z = 3$, $x - 2y + \lambda z = \mu$ has no solution is",
  r"$9$",
  [(r"$10$", r"Finds $\lambda = 2$ but counts every $\mu$, including $\mu = 1$, which gives infinitely many solutions."),
   (r"$1$", r"Counts only the pair $(2, 1)$, which is the case of infinitely many solutions."),
   (r"$90$", r"Counts the pairs with $\lambda \ne 2$, which give a unique solution.")],
  r"$\Delta = 1(-\lambda + 2) - 1(2\lambda - 1) - 1(-4 + 1) = -3\lambda + 6$, so only $\lambda = 2$ can fail. Then $(1, -2, 2) = R_2 - R_1$, so consistency needs $\mu = 3 - 2 = 1$. No solution occurs for $\lambda = 2$ and $\mu \in \{2, \ldots, 10\}$: $9$ pairs.",
  r"Not separating the infinitely-many case from the no-solution case.",
  "U03-D-lambda-mu-count", "Classification by two parameters followed by careful counting.",
  check=_c43, values=[9, 10, 1, 90],
  numerical=dict(question=r"Let $\lambda, \mu \in \{1, 2, 3, \ldots, 10\}$. The number of ordered pairs $(\lambda, \mu)$ for which the system $x + y - z = 2$, $2x - y + z = 3$, $x - 2y + \lambda z = \mu$ has no solution is", answer=9),
  cognitive="Analysis", source_class="XII")


def _c44():
    rows = [[1, 1, 1], [2, 3, lam], [3, 4, 5]]
    l0 = only(roots_real(det_(rows), lam))
    r0 = subs_rows(rows, lam, l0)
    m0 = only(solve(consist_expr(r0, [2, 5, mu]), mu))
    sol = list(linsolve((Matrix(r0), Matrix([2, 5, m0])), XYZ))[0]
    val = simplify(sol[0] - sol[2])
    assert not val.free_symbols
    return val


q("U03-D-044", TOPIC, "An invariant of the solution set", "Difficult", "Multi-step computation MCQ",
  r"The system $x + y + z = 2$, $2x + 3y + \lambda z = 5$, $3x + 4y + 5z = \mu$ has infinitely many solutions. Then, for every solution $(x, y, z)$, the value of $x - z$ is",
  r"$1$",
  [(r"$3$", r"Finds $\lambda = 4$ but writes $R_2 - 2R_1$ as $y + 2z = -1$, so $x = 3 + z$."),
   (r"$-1$", r"Finds $x = 1 + z$ correctly but reports $z - x$."),
   (r"$2$", r"Takes the particular point $y = z = 0$ from the first equation alone, $x = 2$, without checking the second equation.")],
  r"$\Delta = 1(15 - 4\lambda) - 1(10 - 3\lambda) + 1(8 - 9) = 4 - \lambda$, so $\lambda = 4$; then $R_3 = R_1 + R_2$ and $\mu = 7$. With $\lambda = 4$, $R_2 - 2R_1$ gives $y + 2z = 1$, so $y = 1 - 2z$ and $x = 2 - y - z = 1 + z$. Hence $x - z = 1$ for every solution.",
  r"Assuming a particular solution represents the whole solution set.",
  "U03-D-infinite-invariant", "Determinant condition, consistency, and a parametric solution.",
  check=_c44, values=[1, 3, -1, 2],
  numerical=dict(question=r"The system $x + y + z = 2$, $2x + 3y + \lambda z = 5$, $3x + 4y + 5z = \mu$ has infinitely many solutions. For every solution $(x, y, z)$, the value of $x - z$ is", answer=1),
  cognitive="Analysis", source_class="XII")


def _c45():
    rows = [[1, k, 1], [1, 1, k], [3, 2, -2]]
    kp = only([r for r in roots_real(det_(rows), k) if r > 0])
    v = ratio(subs_rows(rows, k, kp))
    return simplify((v[0] + 2 * v[1]) / v[2])


q("U03-D-045", TOPIC, "Non-trivial solution and an expression", "Difficult", "Multi-step computation MCQ",
  r"For $k > 0$, the system $x + ky + z = 0$, $x + y + kz = 0$, $3x + 2y - 2z = 0$ has a non-trivial solution $(x, y, z)$. Then $\frac{x + 2y}{z}$ equals",
  r"$-6$",
  [(r"$14$", r"Cross-multiplies with a sign slip in the middle component, getting the direction $(4, 5, 1)$."),
   (r"$-14$", r"Cross-multiplies with a sign slip in the first component, getting the direction $(4, 5, -1)$."),
   (r"$2$", r"Uses the root $k = -1$, which violates $k > 0$; it gives solutions along $(0, 1, 1)$.")],
  r"$\Delta = 1(-2 - 2k) - k(-2 - 3k) + 1(2 - 3) = 3k^2 - 3 = 3(k - 1)(k + 1)$, so $k = 1$. The equations become $x + y + z = 0$ and $3x + 2y - 2z = 0$. Cross-multiplying: $x : y : z = (-2 - 2) : (3 + 2) : (2 - 3) = -4 : 5 : -1$, i.e. $4 : -5 : 1$. So $\frac{x + 2y}{z} = \frac{4 - 10}{1} = -6$.",
  r"Sign slips in cross-multiplication, or ignoring the condition $k > 0$.",
  "U03-D-homog-solution", "Determinant, root selection, direction of solutions and evaluation.",
  check=_c45, values=[-6, 14, -14, 2], cognitive="Analysis", source_class="XII")


def _c46():
    rows = [[1, 1, k], [k, 2, 1], [1, -1, 1]]
    good = []
    for r in roots_real(det_(rows), k):
        v = ratio(subs_rows(rows, k, r))
        if all(e > 0 for e in v) or all(e < 0 for e in v):
            good.append(r)
    return only(good)


q("U03-D-046", TOPIC, "Choosing the parameter from the sign of the solution", "Difficult", "Inverse/parameter MCQ",
  r"The system $x + y + kz = 0$, $kx + 2y + z = 0$, $x - y + z = 0$ has a non-trivial solution in which $x$, $y$ and $z$ are all positive. Then $k$ equals",
  r"$-4$",
  [(r"$1$", r"Takes the other root of $\Delta = 0$; for $k = 1$ the solutions are multiples of $(-1, 0, 1)$, which are never all positive."),
   (r"$-2$", r"Uses $+$ for the middle cofactor, getting $\Delta = -k^2 - k + 2$ with roots $-2$ and $1$, and rejects $1$."),
   (r"$4$", r"Solves $k^2 + 3k - 4 = 0$ with the signs of the roots reversed, getting $4$ and $-1$, and keeps the positive one, $4$, thinking a positive $k$ is needed for positive $x, y, z$.")],
  r"$\Delta = 1(2 + 1) - 1(k - 1) + k(-k - 2) = -k^2 - 3k + 4 = -(k - 1)(k + 4)$, so $k = 1$ or $k = -4$. For $k = 1$, the solutions are multiples of $(-1, 0, 1)$, not all positive. For $k = -4$, the equations $x + y - 4z = 0$ and $x - y + z = 0$ give $x : y : z = 3 : 5 : 2$, all positive. Hence $k = -4$.",
  r"Stopping at $\Delta = 0$ without testing each root against the extra condition.",
  "U03-D-homog-solution", "Two roots, each tested via the direction of the solution set.",
  check=_c46, values=[-4, 1, -2, 4], cognitive="Analysis", source_class="XII")


def _c47():
    rows = [[1, k, 1], [k, 1, -1], [1, 1, k]]
    return sum(1 for kv in range(-5, 6) if kind(subs_rows(rows, k, kv), [1, 0, 1]) != "none")


q("U03-D-047", TOPIC, "Counting parameter values with at least one solution", "Difficult", "Multi-step computation MCQ",
  r"The number of integers $k$ in $[-5, 5]$ for which the system $x + ky + z = 1$, $kx + y - z = 0$, $x + y + kz = 1$ has at least one solution is",
  r"$10$",
  [(r"$8$", r"Keeps only the values with $\Delta \ne 0$, discarding $k = 0, 1, -1$ without checking consistency."),
   (r"$11$", r"Assumes the system is consistent for every $k$, never testing the roots of $\Delta$."),
   (r"$2$", r"Counts only the values $k = 0$ and $k = 1$, where there are infinitely many solutions.")],
  r"$\Delta = 1(k + 1) - k(k^2 + 1) + 1(k - 1) = -k^3 + k = -k(k - 1)(k + 1)$. For $k = 0$: $x + z = 1$, $y - z = 0$, $x + y = 1$, consistent (infinitely many). For $k = 1$: $x + y + z = 1$ and $x + y - z = 0$, consistent. For $k = -1$: the first two equations are $x - y + z = 1$ and $-x + y - z = 0$, and adding them gives $0 = 1$, so the system is inconsistent. So $11 - 1 = 10$ integers work.",
  r"Treating every root of $\Delta$ as a failure of solvability.",
  "U03-D-at-least-one", "Cubic determinant and consistency tests at three roots, then counting.",
  check=_c47, values=[10, 8, 11, 2],
  numerical=dict(question=r"The number of integers $k$ in $[-5, 5]$ for which the system $x + ky + z = 1$, $kx + y - z = 0$, $x + y + kz = 1$ has at least one solution is", answer=10),
  cognitive="Analysis", source_class="XII")


def _c48():
    p, q = symbols('p q', integer=True)
    rows = [[1, 2, -1], [2, -1, 3], [4, 3, 1]]
    assert det_(rows) == 0 and Matrix(rows).rank() == 2
    e = consist_expr(rows, [p, q, p * q - 4])
    # (p - 1)(q - 2) = 6 bounds p, q by 8; scan well beyond that
    return sum(1 for pv in range(1, 41) for qv in range(1, 41) if e.subs({p: pv, q: qv}) == 0)


q("U03-D-048", TOPIC, "Consistency leading to integer pairs", "Difficult", "Multi-step computation MCQ",
  r"Let $p$ and $q$ be positive integers. The number of ordered pairs $(p, q)$ for which the system $x + 2y - z = p$, $2x - y + 3z = q$, $4x + 3y + z = pq - 4$ is consistent is",
  r"$4$",
  [(r"$8$", r"Counts every integer solution of $(p - 1)(q - 2) = 6$, including the four pairs $(0, -4)$, $(-1, -1)$, $(-2, 0)$, $(-5, 1)$ that are not pairs of positive integers."),
   (r"$3$", r"Rewrites $pq - 2p - q = 4$ as $(p - 1)(q - 2) = 4$, forgetting to add $2$ to the right side, and finds $(2, 6)$, $(3, 4)$, $(5, 3)$."),
   (r"$0$", r"Sees $\Delta = 0$ and concludes that the system can never be consistent.")],
  r"Since $2(1, 2, -1) + (2, -1, 3) = (4, 3, 1)$, the rows satisfy $R_3 = 2R_1 + R_2$, so $\Delta = 0$; as $R_1$ and $R_2$ are independent, the system is consistent if and only if $pq - 4 = 2p + q$. Adding $2$ to both sides of $pq - 2p - q = 4$ gives $(p - 1)(q - 2) = 6$. For positive integers $p - 1 \ge 0$ and the product is positive, so $p - 1$ and $q - 2$ form a positive divisor pair of $6$: $(1, 6)$, $(2, 3)$, $(3, 2)$, $(6, 1)$. Hence $(p, q) = (2, 8)$, $(3, 5)$, $(4, 4)$, $(7, 3)$, which is $4$ pairs.",
  r"Mishandling the factorisation $pq - 2p - q = (p - 1)(q - 2) - 2$, or ignoring the positivity condition.",
  "U03-D-consistency-integer-pairs", r"Row relation for a singular system, a factorisation trick on the constants, and a constrained divisor count.",
  check=_c48, values=[4, 8, 3, 0],
  numerical=dict(question=r"Let $p$ and $q$ be positive integers. The number of ordered pairs $(p, q)$ for which the system $x + 2y - z = p$, $2x - y + 3z = q$, $4x + 3y + z = pq - 4$ is consistent is", answer=4),
  cognitive="Analysis", source_class="XII")

q("U03-D-049", TOPIC, "Casework at the roots of a cubic determinant", "Difficult", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which the system $x + 2y + 3z = 1$, $2x + ky + 6z = 2$, $3x + 6y + k^2 z = 4$ has no solution is",
  r"$\{-3, 3\}$",
  [(r"$\{-3, 3, 4\}$", r"Takes every root of $\Delta = (k - 4)(k - 3)(k + 3)$ as a case of no solution, without checking the constants."),
   (r"$\{4\}$", r"Compares only the first two equations: at $k = 4$ they are dependent and this is taken as inconsistency, while at $k = \pm 3$ they are independent and the system is assumed solvable."),
   (r"$\{3\}$", r"Solves $k^2 = 9$ as $k = 3$ only, losing $k = -3$.")],
  r"$\Delta = 1(k^3 - 36) - 2(2k^2 - 18) + 3(12 - 3k) = k^3 - 4k^2 - 9k + 36 = (k - 4)(k - 3)(k + 3)$. At $k = 4$ the second equation is twice the first, and the remaining two equations are independent, so there are infinitely many solutions. At $k = \pm 3$ the third coefficient row is $(3, 6, 9) = 3R_1$, but the constant is $4 \ne 3$, so there is no solution. Hence the set is $\{-3, 3\}$.",
  r"Equating $\Delta = 0$ with no solution.",
  "U03-D-none-casework", "Cubic determinant and a separate consistency check at each of three roots.",
  check=lambda: param_set([[1, 2, 3], [2, k, 6], [3, 6, k**2]], [1, 2, 4], k, "none"),
  values=[FiniteSet(-3, 3), FiniteSet(-3, 3, 4), FiniteSet(4), FiniteSet(3)],
  cognitive="Analysis", source_class="XII")


def _c50():
    P = Matrix([[1, -2, 1], [-2, 3, -1], [1, 1, -1]])
    Pinv = Matrix([[2, 1, 1], [3, 2, 1], [5, 3, 1]])
    assert P * Pinv == eye(3)
    sol = list(linsolve((P * P, Matrix([17, -29, 0])), XYZ))[0]
    return sum(sol)


q("U03-D-050", TOPIC, "Matrix method with a squared coefficient matrix", "Difficult", "Multi-step computation MCQ",
  r"Let $P = \begin{bmatrix} 1 & -2 & 1 \\ -2 & 3 & -1 \\ 1 & 1 & -1 \end{bmatrix}$, for which $P^{-1} = \begin{bmatrix} 2 & 1 & 1 \\ 3 & 2 & 1 \\ 5 & 3 & 1 \end{bmatrix}$. If $X = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$ satisfies $P^2 X = \begin{bmatrix} 17 \\ -29 \\ 0 \end{bmatrix}$, then $x + y + z$ equals",
  r"$2$",
  [(r"$-4$", r"Multiplies by $P^{-1}$ only once, taking $X = P^{-1}Q = (5, -7, -2)$."),
   (r"$-12$", r"Multiplies by $P^{-1}$ and then by $P$ instead of $P^{-1}$ again, which returns the column $(17, -29, 0)$ itself."),
   (r"$-2$", r"Takes $(P^2)^{-1}$ as $\frac{1}{2}P^{-1}$, as if $P^2$ were $2P$, giving $(\frac{5}{2}, -\frac{7}{2}, -1)$.")],
  r"$X = (P^2)^{-1}Q = P^{-1}(P^{-1}Q)$ with $Q = (17, -29, 0)$. First $P^{-1}Q = (34 - 29,\ 51 - 58,\ 85 - 87) = (5, -7, -2)$. Then $P^{-1}(5, -7, -2) = (10 - 7 - 2,\ 15 - 14 - 2,\ 25 - 21 - 2) = (1, -1, 2)$. Hence $x + y + z = 2$.",
  r"Treating $(P^2)^{-1}$ as $P^{-1}$ or as $\frac{1}{2}P^{-1}$.",
  "U03-D-matrix-method-power", r"Two successive multiplications by $P^{-1}$ with the identity $(P^2)^{-1} = (P^{-1})^2$.",
  check=_c50, values=[2, -4, -12, -2], cognitive="Analysis", source_class="XII")


def _c51():
    aug = Matrix([[k, 1, 1], [1, k, 1], [1, 1, k]])
    good = [r for r in roots_real(aug.det(), k)
            if kind([[r, 1], [1, r], [1, 1]], [1, 1, r]) != "none"]
    return sum(good)


q("U03-D-051", TOPIC, "Concurrency of three lines with a parameter", "Difficult", "Multi-step computation MCQ",
  r"The sum of all distinct real values of $k$ for which the equations $kx + y = 1$, $x + ky = 1$ and $x + y = k$ have a common solution is",
  r"$-1$",
  [(r"$0$", r"Takes the roots of $(k - 1)^2(k + 2) = 0$ with multiplicity, adding $1 + 1 - 2$."),
   (r"$-2$", r"Rejects $k = 1$ because the three equations coincide there, although they then have infinitely many common solutions."),
   (r"$1$", r"Keeps only $k = 1$, where the equations coincide, and does not test the concurrent case $k = -2$.")],
  r"A common solution needs $\begin{vmatrix} k & 1 & 1 \\ 1 & k & 1 \\ 1 & 1 & k \end{vmatrix} = (k - 1)^2(k + 2) = 0$. For $k = 1$ all three equations are $x + y = 1$, so they have common solutions. For $k = -2$: $-2x + y = 1$ and $x - 2y = 1$ give $x = y = -1$, and $x + y = -2 = k$ holds. Both values work, and their sum is $1 + (-2) = -1$.",
  r"Counting a repeated root twice or discarding the coincident case.",
  "U03-D-2var-3eqn", "Augmented determinant, factorisation and checking each root.",
  check=_c51, values=[-1, 0, -2, 1], cognitive="Analysis", source_class="XII")


def _c52():
    rows = [[1, 1, 1], [1, 2, 3], [3, 4, lam]]
    l0 = only(roots_real(det_(rows), lam))
    r0 = subs_rows(rows, lam, l0)
    m0 = only(solve(consist_expr(r0, [10, 15, mu]), mu))
    cnt = 0
    for xv in range(0, 16):
        for yv in range(0, 16):
            for zv in range(0, 16):
                if all(r0[i][0] * xv + r0[i][1] * yv + r0[i][2] * zv == [10, 15, m0][i] for i in range(3)):
                    cnt += 1
    return cnt


q("U03-D-052", TOPIC, "Integer points of an infinite solution set", "Difficult", "Multi-step computation MCQ",
  r"The system $x + y + z = 10$, $x + 2y + 3z = 15$, $3x + 4y + \lambda z = \mu$ has infinitely many solutions. The number of these solutions $(x, y, z)$ in which $x$, $y$, $z$ are all non-negative integers is",
  r"$3$",
  [(r"$6$", r"Uses $y = 5 - 2z \ge 0$ as $z \le 5$, forgetting the factor $2$, and counts $z = 0, 1, \ldots, 5$."),
   (r"$2$", r"Counts only positive integers, dropping $z = 0$."),
   (r"$4$", r"Rounds $z \le \frac{5}{2}$ up to $z \le 3$ and counts $z = 0, 1, 2, 3$.")],
  r"$\Delta = 1(2\lambda - 12) - 1(\lambda - 9) + 1(4 - 6) = \lambda - 5$, so $\lambda = 5$, with $R_3 = 2R_1 + R_2$ and $\mu = 35$. The solutions satisfy $R_2 - R_1$: $y + 2z = 5$, so $y = 5 - 2z$ and $x = 10 - y - z = 5 + z$. Non-negativity needs $0 \le z \le \frac{5}{2}$, so $z = 0, 1, 2$, giving $(5, 5, 0)$, $(6, 3, 1)$, $(7, 1, 2)$. That is $3$ solutions.",
  r"Mishandling the inequality bounds when counting integer points.",
  "U03-D-infinite-integer-points", "Parameter determination, parametric solution and an integer count with bounds.",
  check=_c52, values=[3, 6, 2, 4],
  numerical=dict(question=r"The system $x + y + z = 10$, $x + 2y + 3z = 15$, $3x + 4y + \lambda z = \mu$ has infinitely many solutions. The number of these solutions $(x, y, z)$ in which $x$, $y$, $z$ are all non-negative integers is", answer=3),
  cognitive="Analysis", source_class="XII")


def _c53():
    sol = list(linsolve([x + y + z - 1, x + 2 * y + 3 * z - d, x + 4 * y + 9 * z - d**2], XYZ))[0]
    return Intersection(solveset(sol[0] > 0, d, S.Reals), solveset(sol[1] > 0, d, S.Reals))


q("U03-D-053", TOPIC, "Sign conditions on the solution", "Difficult", "Multi-step computation MCQ",
  r"For real $d$, let $(x, y, z)$ be the solution of $x + y + z = 1$, $x + 2y + 3z = d$, $x + 4y + 9z = d^2$. The set of all $d$ for which $x > 0$ and $y > 0$ is",
  r"$(1, 2)$",
  [(r"$(2, 3)$", r"Uses Cramer's rule with the sign of $x$ reversed, $x = -\frac{(d - 2)(d - 3)}{2}$, so $x > 0$ becomes $2 < d < 3$."),
   (r"$(1, 3)$", r"Imposes only $y = -(d - 1)(d - 3) > 0$ and forgets the condition on $x$."),
   (r"$(-\infty, 2) \cup (3, \infty)$", r"Imposes only $x = \frac{(d - 2)(d - 3)}{2} > 0$ and forgets the condition on $y$.")],
  r"$\Delta = (2 - 1)(3 - 1)(3 - 2) = 2$ (a Vandermonde determinant). Cramer's rule gives $x = \frac{(d - 2)(d - 3)}{2}$ and $y = -(d - 1)(d - 3)$. Then $y > 0 \iff 1 < d < 3$, and $x > 0 \iff d < 2$ or $d > 3$. Both hold exactly for $1 < d < 2$.",
  r"Dropping one of the two sign conditions, or a sign slip in Cramer's rule.",
  "U03-D-vandermonde-cramer", "Solving with a parameter, then combining two quadratic inequalities.",
  check=_c53,
  values=[Interval.open(1, 2), Interval.open(2, 3), Interval.open(1, 3),
          Union(Interval.open(-oo, 2), Interval.open(3, oo))],
  cognitive="Analysis", source_class="XII")


def _c54():
    al, be = symbols('alpha beta')
    X1 = Matrix([1, 1, 1]); X2 = Matrix([2, -1, 2])
    P = Matrix([[1, 1, 1], [1, 2, al], [2, be, 4]])
    sol = solve(list(P * X1 - P * X2), [al, be], dict=True)
    assert len(sol) == 1
    P0 = P.subs(sol[0])
    good = [kv for kv in roots_real(consist_expr(P0.tolist(), [2, k, 7]), k)
            if P0.rank() == P0.row_join(Matrix([2, kv, 7])).rank()]
    return only(good)


q("U03-D-054", TOPIC, "Recovering the coefficient matrix from two solutions", "Difficult", "Inverse/parameter MCQ",
  r"Let $P = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & \alpha \\ 2 & \beta & 4 \end{bmatrix}$, where $\alpha, \beta$ are real. If $X_1 = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$ and $X_2 = \begin{bmatrix} 2 \\ -1 \\ 2 \end{bmatrix}$ are both solutions of $PX = Q$ for some $3 \times 1$ matrix $Q$, then the system $PX = \begin{bmatrix} 2 \\ k \\ 7 \end{bmatrix}$ is consistent if and only if $k$ equals",
  r"$5$",
  [(r"$\frac{9}{2}$", r"Applies the null vector $(1, -2, 1)$ of $P$, which is a relation among the columns, to the right-hand side: $2 - 2k + 7 = 0$."),
   (r"$9$", r"Reads the row relation as $R_2 = R_1 + R_3$, so takes $k = 2 + 7$."),
   (r"$-5$", r"Finds $R_1 + R_2 - R_3 = O$ but slips a sign on the constants, writing $2 - k - 7 = 0$.")],
  r"From $PX_1 = PX_2 = Q$ we get $P(X_2 - X_1) = O$ with $X_2 - X_1 = (1, -2, 1)$. The second row gives $1 - 4 + \alpha = 0$, so $\alpha = 3$; the third gives $2 - 2\beta + 4 = 0$, so $\beta = 3$. Now the rows $(1, 1, 1)$, $(1, 2, 3)$, $(2, 3, 4)$ satisfy $R_3 = R_1 + R_2$ while $R_1$ and $R_2$ are independent, so $PX = (2, k, 7)^T$ is consistent exactly when $7 = 2 + k$, that is $k = 5$.",
  r"Confusing the column relation $P(X_2 - X_1) = O$ with the row relation that governs consistency.",
  "U03-D-solutions-fix-matrix", r"Uses two solutions to recover unknown entries, then switches from a column relation to a row relation for a new right-hand side.",
  check=_c54, values=[5, Rational(9, 2), 9, -5],
  numerical=dict(question=r"Let $P = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & \alpha \\ 2 & \beta & 4 \end{bmatrix}$, where $\alpha, \beta$ are real. If $X_1 = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$ and $X_2 = \begin{bmatrix} 2 \\ -1 \\ 2 \end{bmatrix}$ are both solutions of $PX = Q$ for some $3 \times 1$ matrix $Q$, then the value of $k$ for which the system $PX = \begin{bmatrix} 2 \\ k \\ 7 \end{bmatrix}$ is consistent is", answer=5),
  cognitive="Analysis", source_class="XII")


def _c55():
    rows = [[1, 1, 1], [1, 2, 3], [1, -1, 2]]
    cnt = 0
    for kv in range(1, 51):
        sol = list(linsolve((Matrix(rows), Matrix([6, kv, 5])), XYZ))[0]
        if all(e.is_integer for e in sol):
            cnt += 1
    return cnt


q("U03-D-055", TOPIC, "Integer solutions of a parametric system", "Difficult", "Multi-step computation MCQ",
  r"The number of integers $k$ with $1 \le k \le 50$ for which the solution of the system $x + y + z = 6$, $x + 2y + 3z = k$, $x - y + 2z = 5$ has $x$, $y$, $z$ all integers is",
  r"$10$",
  [(r"$50$", r"Assumes that integer coefficients and constants always give an integer solution."),
   (r"$40$", r"Counts the values of $k$ for which the solution is not integral."),
   (r"$9$", r"Writes $k = 5n + 4$ but counts only $n = 1, \ldots, 9$, missing $k = 4$.")],
  r"$\Delta = 1(4 + 3) - 1(2 - 3) + 1(-1 - 2) = 5$. Cramer's rule gives $x = \frac{47 - 3k}{5}$, $y = \frac{k - 4}{5}$, $z = \frac{2k - 13}{5}$. All three are integers exactly when $k \equiv 4 \pmod 5$ (then $47 - 3k \equiv 35$ and $2k - 13 \equiv -5$, both multiples of $5$). In $[1, 50]$ these are $k = 4, 9, \ldots, 49$: $10$ values.",
  r"Assuming integer data always give integer solutions.",
  "U03-D-integer-solutions", "Cramer's rule with a parameter, a divisibility condition and a count.",
  check=_c55, values=[10, 50, 40, 9],
  numerical=dict(question=r"The number of integers $k$ with $1 \le k \le 50$ for which the solution of the system $x + y + z = 6$, $x + 2y + 3z = k$, $x - y + 2z = 5$ has $x$, $y$, $z$ all integers is", answer=10),
  cognitive="Analysis", source_class="XII")
