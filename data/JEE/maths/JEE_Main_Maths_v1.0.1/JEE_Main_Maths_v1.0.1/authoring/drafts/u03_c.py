import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x, t = symbols('x t', real=True)
k, a, b, c = symbols('k a b c')
I2, I3 = eye(2), eye(3)


def bm(M):
    rows = [" & ".join(latex(e) for e in M.row(i)) for i in range(M.rows)]
    return r"\begin{bmatrix} " + r" \\ ".join(rows) + r" \end{bmatrix}"


def opt(M, pre=""):
    return "$" + pre + bm(M) + "$"


T, F_ = True, False
ST_OPTS = ["Both Statement I and Statement II are true",
           "Both Statement I and Statement II are false",
           "Statement I is true but Statement II is false",
           "Statement I is false but Statement II is true"]
ST_VALS = {ST_OPTS[0]: (T, T), ST_OPTS[1]: (F_, F_), ST_OPTS[2]: (T, F_), ST_OPTS[3]: (F_, T)}


def st_item(key):
    others = [o for o in ST_OPTS if o != key]
    return key, others, [ST_VALS[key]] + [ST_VALS[o] for o in others]


# A sample 3x3 matrix with determinant 3, used where a stem fixes only |A|
S3 = Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 2]])
# A sample 3x3 matrix with determinant 5
S5 = Matrix([[1, 2, 0], [0, 1, 1], [2, 0, 1]])
# A sample 3x3 matrix with determinant 2
S2 = Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])

# ================================================================ EASY
# ---------------------------------------------------------------- 001
A001 = Matrix([[2, -1, 3], [4, 0, 5], [1, 6, -2]])
q("U03-C-001", "Adjoint and inverse", "Cofactor of an element", "Easy", "Single-step computation MCQ",
  r"For the matrix $P = " + bm(A001) + r"$, the cofactor $C_{23}$ of the element in the second row and third column is",
  r"$-13$",
  [(r"$13$", "Reports the minor $M_{23} = 13$ and omits the sign factor $(-1)^{2+3}$."),
   (r"$-11$", "Evaluates the minor as $2 \\cdot 6 - 1 = 11$, dropping the sign of $(-1)(1)$, then attaches the minus sign."),
   (r"$2$", "Computes $C_{32}$, deleting the third row and second column: $-(2 \\cdot 5 - 3 \\cdot 4) = 2$.")],
  r"Delete row 2 and column 3 to get $\begin{vmatrix} 2 & -1 \\ 1 & 6 \end{vmatrix} = 12 - (-1) = 13$. Then $C_{23} = (-1)^{2+3} \cdot 13 = -13$.",
  "Confusing the minor with the cofactor or deleting the wrong row and column.",
  "U03-C-cofactor-entry", "One 2 by 2 minor and one sign factor.",
  check=lambda: A001.cofactor(1, 2), values=[-13, 13, -11, 2], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 002
A002 = Matrix([[3, -2], [5, 4]])
q("U03-C-002", "Adjoint and inverse", "Adjoint of a 2 by 2 matrix", "Easy", "Single-step computation MCQ",
  r"If $P = " + bm(A002) + r"$, then $\operatorname{adj} P$ equals",
  opt(Matrix([[4, 2], [-5, 3]])),
  [(opt(Matrix([[4, -5], [2, 3]])), "Writes the cofactor matrix and does not transpose it."),
   (opt(Matrix([[3, 2], [-5, 4]])), "Changes the signs of the off-diagonal entries but does not swap the diagonal entries."),
   (opt(Matrix([[4, -2], [5, 3]])), "Swaps the diagonal entries but keeps the off-diagonal entries unchanged.")],
  r"For $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ the adjoint is $\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$. Here $a = 3, b = -2, c = 5, d = 4$, so $\operatorname{adj} P = \begin{bmatrix} 4 & 2 \\ -5 & 3 \end{bmatrix}$.",
  "Forgetting to transpose the cofactor matrix or applying only half of the swap-and-negate rule.",
  "U03-C-adj-2x2", "Direct use of the 2 by 2 adjoint rule.",
  check=lambda: A002.adjugate(),
  values=[Matrix([[4, 2], [-5, 3]]), Matrix([[4, -5], [2, 3]]), Matrix([[3, 2], [-5, 4]]), Matrix([[4, -2], [5, 3]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 003
def _c003():
    M = S5
    assert M.det() == 5
    return M.adjugate().det()
q("U03-C-003", "Adjoint and inverse", "Determinant of the adjoint", "Easy", "Single-step computation MCQ",
  r"If $P$ is a square matrix of order $3$ with $|P| = 5$, then $|\operatorname{adj} P|$ equals",
  r"$25$",
  [(r"$5$", "Assumes $|\\operatorname{adj} P| = |P|$."),
   (r"$125$", "Uses $|P|^n = 5^3$ instead of $|P|^{n-1}$."),
   (r"$15$", "Multiplies by the order: $n|P| = 3 \\cdot 5$.")],
  r"Since $P \operatorname{adj} P = |P| I_3$, taking determinants gives $|P| \, |\operatorname{adj} P| = |P|^3$, so $|\operatorname{adj} P| = |P|^{2} = 25$.",
  "Using the wrong power of $|P|$ for the determinant of the adjoint.",
  "U03-C-adj-det-power", "One standard result applied once.",
  check=_c003, values=[25, 5, 125, 15], cognitive="Recall", source_class="XII",
  numerical=dict(question=r"If $P$ is a square matrix of order $3$ with $|P| = 5$, then the value of $|\operatorname{adj} P|$ is", answer=25))

# ---------------------------------------------------------------- 004
A004 = Matrix([[2, 5], [1, 3]])
q("U03-C-004", "Adjoint and inverse", "Inverse of a 2 by 2 matrix", "Easy", "Single-step computation MCQ",
  r"If $P = " + bm(A004) + r"$, then $P^{-1}$ equals",
  opt(Matrix([[3, -5], [-1, 2]])),
  [(opt(Matrix([[3, -1], [-5, 2]])), "Divides the untransposed cofactor matrix by $|P| = 1$."),
   (opt(Matrix([[-3, 5], [1, -2]])), "Takes $|P| = 5 - 6 = -1$ by subtracting in the wrong order."),
   (opt(Matrix([[2, -5], [-1, 3]])), "Negates the off-diagonal entries but forgets to swap the diagonal entries.")],
  r"$|P| = 2 \cdot 3 - 5 \cdot 1 = 1$ and $\operatorname{adj} P = \begin{bmatrix} 3 & -5 \\ -1 & 2 \end{bmatrix}$, so $P^{-1} = \frac{1}{|P|}\operatorname{adj} P = \begin{bmatrix} 3 & -5 \\ -1 & 2 \end{bmatrix}$. Check: $P P^{-1} = I$.",
  "Mishandling the swap-and-negate rule or the sign of the determinant.",
  "U03-C-inverse-2x2", "Determinant and adjoint of a 2 by 2 matrix.",
  check=lambda: A004.inv(),
  values=[Matrix([[3, -5], [-1, 2]]), Matrix([[3, -1], [-5, 2]]), Matrix([[-3, 5], [1, -2]]), Matrix([[2, -5], [-1, 3]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 005
def _c005():
    M = Matrix([[2, 0, 0], [0, 1, 1], [0, 1, 3]])
    assert M.det() == 4
    return (2 * M.inv()).det()
q("U03-C-005", "Adjoint and inverse", "Determinant of a scalar multiple of the inverse", "Easy", "Single-step computation MCQ",
  r"If $P$ is a non-singular matrix of order $3$ with $|P| = 4$, then $|2P^{-1}|$ equals",
  r"$2$",
  [(r"$\frac{1}{2}$", "Uses $|2P^{-1}| = 2|P^{-1}| = \\frac{2}{4}$, not raising $2$ to the power $3$."),
   (r"$32$", "Uses $|P^{-1}| = |P|$, giving $8 \\cdot 4$."),
   (r"$\frac{1}{32}$", "Computes $|2P|^{-1} = \\frac{1}{8 \\cdot 4}$, treating $2P^{-1}$ as $(2P)^{-1}$.")],
  r"$|2P^{-1}| = 2^3 |P^{-1}| = \frac{8}{|P|} = \frac{8}{4} = 2$.",
  "Forgetting that a scalar comes out of a determinant of order $n$ as its $n$th power.",
  "U03-C-det-inverse-scaled", "Two determinant rules applied once each.",
  check=_c005, values=[2, Rational(1, 2), 32, Rational(1, 32)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 006
Ai006 = Matrix([[1, 2], [0, 1]]); Bi006 = Matrix([[1, 0], [3, 1]])
def _c006():
    A = Ai006.inv(); B = Bi006.inv()
    return (A * B).inv()
q("U03-C-006", "Adjoint and inverse", "Inverse of a product", "Easy", "Single-step computation MCQ",
  r"If $P$ and $Q$ are invertible matrices with $P^{-1} = " + bm(Ai006) + r"$ and $Q^{-1} = " + bm(Bi006) + r"$, then $(PQ)^{-1}$ equals",
  opt(Matrix([[1, 2], [3, 7]])),
  [(opt(Matrix([[7, 2], [3, 1]])), "Multiplies in the order $P^{-1}Q^{-1}$."),
   (opt(Matrix([[1, 3], [2, 7]])), "Transposes the correct product, mixing up the reversal law with the transpose rule."),
   (opt(Matrix([[7, -2], [-3, 1]])), "Inverts $Q^{-1}P^{-1}$ once more, which gives $PQ$ itself.")],
  r"By the reversal law, $(PQ)^{-1} = Q^{-1}P^{-1} = \begin{bmatrix} 1 & 0 \\ 3 & 1 \end{bmatrix}\begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 2 \\ 3 & 7 \end{bmatrix}$.",
  "Writing $(PQ)^{-1} = P^{-1}Q^{-1}$.",
  "U03-C-inverse-product-order", "One rule and one 2 by 2 product.",
  check=_c006, values=[Matrix([[1, 2], [3, 7]]), Matrix([[7, 2], [3, 1]]), Matrix([[1, 3], [2, 7]]), Matrix([[7, -2], [-3, 1]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 007
A007 = diag(2, -1, 3)
q("U03-C-007", "Adjoint and inverse", "Adjoint of a diagonal matrix", "Easy", "Single-step computation MCQ",
  r"If $P = \operatorname{diag}(2, -1, 3)$, then $\operatorname{adj} P$ equals",
  r"$\operatorname{diag}(-3, 6, -2)$",
  [(r"$\operatorname{diag}\left(\frac{1}{2}, -1, \frac{1}{3}\right)$", "Gives $P^{-1}$, forgetting the factor $|P| = -6$."),
   (r"$\operatorname{diag}(3, -6, 2)$", "Takes $|P| = 6$, losing the sign, and computes $6P^{-1}$."),
   (r"$\operatorname{diag}(-6, -6, -6)$", "Confuses $\\operatorname{adj} P$ with $P \\operatorname{adj} P = |P| I$.")],
  r"$|P| = 2 \cdot (-1) \cdot 3 = -6$ and $P^{-1} = \operatorname{diag}\left(\frac{1}{2}, -1, \frac{1}{3}\right)$. Hence $\operatorname{adj} P = |P| P^{-1} = \operatorname{diag}(-3, 6, -2)$; equivalently each diagonal cofactor is the product of the other two diagonal entries.",
  "Treating the adjoint as the inverse or confusing it with $P\\operatorname{adj} P$.",
  "U03-C-adj-diagonal", "One relation between adjoint and inverse.",
  check=lambda: A007.adjugate(),
  values=[diag(-3, 6, -2), diag(Rational(1, 2), -1, Rational(1, 3)), diag(3, -6, 2), diag(-6, -6, -6)],
  cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 008
def _c008():
    M = Matrix([[2, 0, 0], [0, 1, 1], [0, 1, 3]])
    prod = M * M.adjugate()
    assert prod == 4 * I3
    return M.det() + M.adjugate().det()
q("U03-C-008", "Adjoint and inverse", "Using A adj A = |A| I", "Easy", "Single-step computation MCQ",
  r"If $P$ is a matrix of order $3$ such that $P(\operatorname{adj} P) = 4I_3$, then $|P| + |\operatorname{adj} P|$ equals",
  r"$20$",
  [(r"$68$", "Gets $|P| = 4$ but uses $|\\operatorname{adj} P| = |P|^3 = 64$."),
   (r"$8$", "Gets $|P| = 4$ but takes $|\\operatorname{adj} P| = |P| = 4$."),
   (r"$72$", "Sets $|P|^2 = |4I_3| = 64$, so $|P| = 8$ and $|\\operatorname{adj} P| = 64$.")],
  r"Since $P(\operatorname{adj} P) = |P| I_3$, comparing gives $|P| = 4$. Then $|\operatorname{adj} P| = |P|^{3-1} = 16$, so the sum is $4 + 16 = 20$.",
  "Mixing up $P\\operatorname{adj} P = |P| I$ with a statement about determinants.",
  "U03-C-A-adjA-identity", "Read off $|P|$ and apply one power rule.",
  check=_c008, values=[20, 68, 8, 72], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P$ is a matrix of order $3$ such that $P(\operatorname{adj} P) = 4I_3$, then the value of $|P| + |\operatorname{adj} P|$ is", answer=20))

# ---------------------------------------------------------------- 009
M009 = Matrix([[3, 1], [-1, 2]])  # trace 5, det 7, so M^2 - 5M + 7I = O
def _c009():
    assert M009**2 - 5 * M009 + 7 * I2 == zeros(2)
    return M009.inv()
q("U03-C-009", "Adjoint and inverse", "Inverse from a matrix polynomial relation", "Easy", "Single-step computation MCQ",
  r"If $P$ is a square matrix such that $P^2 - 5P + 7I = O$, then $P^{-1}$ equals",
  r"$\frac{1}{7}(5I - P)$",
  [(r"$\frac{1}{7}(P - 5I)$", "Writes $P(P - 5I) = 7I$, losing the sign when moving $7I$ across."),
   (r"$5I - P$", "Reaches $P(5I - P) = 7I$ but forgets to divide by $7$."),
   (r"$\frac{1}{7}(5I + P)$", "Sign slip on the $P$ term while rearranging.")],
  r"Rewrite the relation as $5P - P^2 = 7I$, that is $P(5I - P) = 7I$. Hence $P \cdot \frac{1}{7}(5I - P) = I$, so $P$ is invertible and $P^{-1} = \frac{1}{7}(5I - P)$.",
  "Sign errors when isolating the constant term.",
  "U03-C-inverse-from-polynomial", "One factorisation of a given relation.",
  check=_c009, values=[(5 * I2 - M009) / 7, (M009 - 5 * I2) / 7, 5 * I2 - M009, (5 * I2 + M009) / 7],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 010
A010 = Matrix([[4, 7], [1, 2]])
q("U03-C-010", "Adjoint and inverse", "Inverse of the transpose", "Easy", "Single-step computation MCQ",
  r"If $P = " + bm(A010) + r"$, then $(P^T)^{-1}$ equals",
  opt(Matrix([[2, -1], [-7, 4]])),
  [(opt(Matrix([[2, -7], [-1, 4]])), "Gives $P^{-1}$ and forgets to transpose."),
   (opt(Matrix([[4, 1], [7, 2]])), "Gives $P^T$ itself, not its inverse."),
   (opt(Matrix([[-2, 1], [7, -4]])), "Takes $|P| = 7 - 8 = -1$ by subtracting in the wrong order.")],
  r"$|P| = 8 - 7 = 1$ and $P^{-1} = \begin{bmatrix} 2 & -7 \\ -1 & 4 \end{bmatrix}$. Since $(P^T)^{-1} = (P^{-1})^T$, the answer is $\begin{bmatrix} 2 & -1 \\ -7 & 4 \end{bmatrix}$.",
  "Not using $(P^T)^{-1} = (P^{-1})^T$.",
  "U03-C-inverse-transpose", "One inverse and one transpose.",
  check=lambda: (A010.T).inv(),
  values=[Matrix([[2, -1], [-7, 4]]), Matrix([[2, -7], [-1, 4]]), Matrix([[4, 1], [7, 2]]), Matrix([[-2, 1], [7, -4]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 011
def _c011():
    assert S2.det() == 2
    return S2.adjugate().adjugate().det()
q("U03-C-011", "Adjoint and inverse", "Determinant of adj(adj A)", "Easy", "Single-step computation MCQ",
  r"If $P$ is a square matrix of order $3$ with $|P| = 2$, then $|\operatorname{adj}(\operatorname{adj} P)|$ equals",
  r"$16$",
  [(r"$8$", "Uses $|P|^{n} = 2^3$."),
   (r"$4$", "Stops at $|\\operatorname{adj} P| = |P|^2 = 4$."),
   (r"$64$", "Computes $|\\operatorname{adj} P|^{n} = 4^3$ instead of $|\\operatorname{adj} P|^{n-1}$.")],
  r"$|\operatorname{adj} P| = |P|^{2} = 4$. Applying the same rule to $\operatorname{adj} P$, $|\operatorname{adj}(\operatorname{adj} P)| = |\operatorname{adj} P|^{2} = 16$, which is $|P|^{(n-1)^2} = 2^4$.",
  "Using the exponent $n$ in place of $n - 1$.",
  "U03-C-adj-adj-det", "One rule applied twice.",
  check=_c011, values=[16, 8, 4, 64], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P$ is a square matrix of order $3$ with $|P| = 2$, then the value of $|\operatorname{adj}(\operatorname{adj} P)|$ is", answer=16))

# ---------------------------------------------------------------- 012
A012 = Matrix([[1, 0, 0], [2, 1, 0], [3, 2, 1]])
q("U03-C-012", "Adjoint and inverse", "Inverse of a triangular matrix", "Easy", "Multi-step computation MCQ",
  r"If $P = " + bm(A012) + r"$, then $P^{-1}$ equals",
  opt(Matrix([[1, 0, 0], [-2, 1, 0], [1, -2, 1]])),
  [(opt(Matrix([[1, 0, 0], [-2, 1, 0], [-3, -2, 1]])), "Negates every off-diagonal entry, as if the inverse of $I + N$ were $I - N$ here."),
   (opt(Matrix([[1, -2, 1], [0, 1, -2], [0, 0, 1]])), "Uses the cofactor matrix without transposing it."),
   (opt(Matrix([[1, 0, 0], [-2, 1, 0], [7, -2, 1]])), "Evaluates the cofactor $C_{13} = 2 \\cdot 2 - 1 \\cdot 3$ as $4 + 3 = 7$.")],
  r"$|P| = 1$. The cofactors are $C_{11} = 1, C_{21} = 0, C_{31} = 0, C_{12} = -2, C_{22} = 1, C_{32} = 0, C_{13} = 4 - 3 = 1, C_{23} = -2, C_{33} = 1$. Transposing the cofactor matrix gives $P^{-1} = \begin{bmatrix} 1 & 0 & 0 \\ -2 & 1 & 0 \\ 1 & -2 & 1 \end{bmatrix}$.",
  "Assuming the inverse of a lower triangular matrix just negates its off-diagonal entries.",
  "U03-C-inverse-triangular", "Cofactors of a triangular matrix, mostly zero.",
  check=lambda: A012.inv(),
  values=[Matrix([[1, 0, 0], [-2, 1, 0], [1, -2, 1]]), Matrix([[1, 0, 0], [-2, 1, 0], [-3, -2, 1]]),
          Matrix([[1, -2, 1], [0, 1, -2], [0, 0, 1]]), Matrix([[1, 0, 0], [-2, 1, 0], [7, -2, 1]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 013
R013 = Matrix([[cos(t), -sin(t)], [sin(t), cos(t)]])
q("U03-C-013", "Adjoint and inverse", "Inverse of a rotation matrix", "Easy", "Single-step computation MCQ",
  r"If $P = \begin{bmatrix} \cos t & -\sin t \\ \sin t & \cos t \end{bmatrix}$, where $0 < t < \frac{\pi}{2}$, then $P^{-1}$ equals",
  r"$\begin{bmatrix} \cos t & \sin t \\ -\sin t & \cos t \end{bmatrix}$",
  [(r"$\begin{bmatrix} \cos t & -\sin t \\ \sin t & \cos t \end{bmatrix}$", "Assumes the matrix is its own inverse."),
   (r"$\begin{bmatrix} -\cos t & -\sin t \\ \sin t & -\cos t \end{bmatrix}$", "Takes $|P| = -(\\cos^2 t + \\sin^2 t) = -1$ by a sign slip in $ad - bc$."),
   (r"$\begin{bmatrix} \sec t & -\operatorname{cosec} t \\ \operatorname{cosec} t & \sec t \end{bmatrix}$", "Takes the reciprocal of each entry.")],
  r"$|P| = \cos^2 t + \sin^2 t = 1$ and $\operatorname{adj} P = \begin{bmatrix} \cos t & \sin t \\ -\sin t & \cos t \end{bmatrix}$, so $P^{-1} = \operatorname{adj} P = P^T$.",
  "Inverting entry by entry or slipping on the sign of the determinant.",
  "U03-C-rotation-inverse", "One 2 by 2 inverse with a trigonometric identity.",
  check=lambda: simplify(R013.inv()),
  values=[Matrix([[cos(t), sin(t)], [-sin(t), cos(t)]]), R013, Matrix([[-cos(t), -sin(t)], [sin(t), -cos(t)]]),
          Matrix([[sec(t), -csc(t)], [csc(t), sec(t)]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 014
Pinv014 = Matrix([[2, -1], [1, 3]]) / 7
q("U03-C-014", "Adjoint and inverse", "Determinant from the inverse", "Easy", "Single-step computation MCQ",
  r"If $P$ is a $2 \times 2$ matrix with $P^{-1} = \frac{1}{7}\begin{bmatrix} 2 & -1 \\ 1 & 3 \end{bmatrix}$, then $|P|$ equals",
  r"$7$",
  [(r"$\frac{1}{7}$", "Reports $|P^{-1}|$ and forgets to take the reciprocal."),
   (r"$1$", "Pulls the factor $\\frac{1}{7}$ out once instead of as $\\frac{1}{7^2}$, getting $|P^{-1}| = 1$."),
   (r"$\frac{49}{5}$", "Evaluates the inner determinant as $6 - 1 = 5$, so $|P^{-1}| = \\frac{5}{49}$.")],
  r"$|P^{-1}| = \left(\frac{1}{7}\right)^2 (6 + 1) = \frac{7}{49} = \frac{1}{7}$. Since $|P| \, |P^{-1}| = 1$, $|P| = 7$.",
  "Pulling a scalar out of a $2 \\times 2$ determinant only once.",
  "U03-C-det-from-inverse", "One determinant and one reciprocal.",
  check=lambda: 1 / Pinv014.det(), values=[7, Rational(1, 7), 1, Rational(49, 5)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P$ is a $2 \times 2$ matrix with $P^{-1} = \frac{1}{7}\begin{bmatrix} 2 & -1 \\ 1 & 3 \end{bmatrix}$, then the value of $|P|$ is", answer=7))

# ---------------------------------------------------------------- 015
def _c015():
    M = S5
    R = (2 * M).adjugate()
    ratio = R[0, 0] / M.adjugate()[0, 0]
    assert R == ratio * M.adjugate()
    return ratio
q("U03-C-015", "Adjoint and inverse", "Adjoint of a scalar multiple", "Easy", "Single-step computation MCQ",
  r"If $P$ is a non-singular matrix of order $3$ and $\operatorname{adj}(2P) = \lambda \operatorname{adj} P$, then $\lambda$ equals",
  r"$4$",
  [(r"$2$", "Pulls the scalar out linearly, as if the adjoint were linear."),
   (r"$8$", "Uses $k^n$ as for the determinant $|2P|$."),
   (r"$\frac{1}{2}$", "Confuses the adjoint with the inverse, using $(2P)^{-1} = \\frac{1}{2}P^{-1}$.")],
  r"Each cofactor of $2P$ is a $2 \times 2$ determinant of entries multiplied by $2$, so it is $2^2$ times the corresponding cofactor of $P$. Hence $\operatorname{adj}(2P) = 2^{3-1}\operatorname{adj} P = 4\operatorname{adj} P$ and $\lambda = 4$.",
  "Treating the adjoint like the determinant or like the inverse under scaling.",
  "U03-C-adj-scalar", "One scaling rule for cofactors.",
  check=_c015, values=[4, 2, 8, Rational(1, 2)], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 016
A016 = Matrix([[2, 1], [5, 3]]); B016 = Matrix([[1, 0], [2, 1]])
def _c016():
    X = MatrixSymbol('X', 2, 2).as_explicit()
    sol = solve(list(A016 * X - B016), list(X), dict=True)[0]
    return X.subs(sol)
q("U03-C-016", "Adjoint and inverse", "Solving AX = B", "Easy", "Multi-step computation MCQ",
  r"If $X$ is a $2 \times 2$ matrix such that $" + bm(A016) + r" X = " + bm(B016) + r"$, then $X$ equals",
  opt(Matrix([[1, -1], [-1, 2]])),
  [(opt(Matrix([[3, -1], [1, 0]])), "Multiplies the inverse on the wrong side, computing $BP^{-1}$ instead of $P^{-1}B$."),
   (opt(Matrix([[4, 1], [11, 3]])), "Multiplies the two given matrices instead of using the inverse."),
   (opt(Matrix([[-1, 1], [1, -2]])), "Takes the determinant as $5 - 6 = -1$, so uses $-P^{-1}$.")],
  r"Let $P = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}$; $|P| = 1$ and $P^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}$. Pre-multiplying by $P^{-1}$, $X = P^{-1}\begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix} = \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$.",
  "Multiplying by the inverse on the wrong side of the right-hand matrix.",
  "U03-C-matrix-eq-AX-B", "One inverse and one product, with order mattering.",
  check=_c016, values=[Matrix([[1, -1], [-1, 2]]), Matrix([[3, -1], [1, 0]]), Matrix([[4, 1], [11, 3]]), Matrix([[-1, 1], [1, -2]])],
  cognitive="Application", source_class="XII")

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 017
A017 = Matrix([[1, 2, 3], [0, 4, 5], [1, 0, 6]])
q("U03-C-017", "Adjoint and inverse", "Elements of one row with cofactors of another", "Medium", "Conceptual/application MCQ",
  r"For $P = " + bm(A017) + r"$, let $C_{ij}$ denote the cofactor of the $(i, j)$ entry $p_{ij}$. Then $p_{11}C_{21} + p_{12}C_{22} + p_{13}C_{23}$ equals",
  r"$0$",
  [(r"$22$", "Treats the sum as an expansion of $|P|$, which needs the cofactors of the same row."),
   (r"$-22$", "Treats it as an expansion of $|P|$ and then attaches the sign of $(-1)^{2+1}$ to the whole sum."),
   (r"$12$", "Uses the minors $M_{21} = 12, M_{22} = 3, M_{23} = -2$ instead of the cofactors.")],
  r"Multiplying the elements of one row by the cofactors of a different row and adding gives the determinant of a matrix with two equal rows, which is $0$. Directly: $C_{21} = -12$, $C_{22} = 3$, $C_{23} = 2$, so $1(-12) + 2(3) + 3(2) = 0$.",
  "Using cofactors of the wrong row as if they expanded the determinant.",
  "U03-C-alien-cofactors", "Needs the alien cofactor property or three cofactors computed carefully.",
  check=lambda: sum(A017[0, j] * A017.cofactor(1, j) for j in range(3)), values=[0, 22, -22, 12],
  cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 018
def _c018():
    M = S3
    return M.inv().adjugate().det()
q("U03-C-018", "Adjoint and inverse", "Determinant of the adjoint of the inverse", "Medium", "Multi-step computation MCQ",
  r"If $P$ is a non-singular matrix of order $3$ with $|P| = 3$, then $|\operatorname{adj}(P^{-1})|$ equals",
  r"$\frac{1}{9}$",
  [(r"$9$", "Computes $|\\operatorname{adj} P|$ instead of $|\\operatorname{adj}(P^{-1})|$."),
   (r"$\frac{1}{3}$", "Stops at $|P^{-1}|$."),
   (r"$\frac{1}{27}$", "Uses $|P^{-1}|^{3}$ instead of $|P^{-1}|^{2}$.")],
  r"$|P^{-1}| = \frac{1}{3}$. Applying $|\operatorname{adj} M| = |M|^{n-1}$ with $M = P^{-1}$ and $n = 3$ gives $|\operatorname{adj}(P^{-1})| = \left(\frac{1}{3}\right)^2 = \frac{1}{9}$.",
  "Applying the adjoint rule to $P$ instead of to $P^{-1}$.",
  "U03-C-adj-inverse-det", "Two rules chained: inverse determinant then adjoint power.",
  check=_c018, values=[Rational(1, 9), 9, Rational(1, 3), Rational(1, 27)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 019
def _c019():
    return (2 * S3).adjugate().det()
q("U03-C-019", "Adjoint and inverse", "Determinant of adj(kA)", "Medium", "Multi-step computation MCQ",
  r"If $P$ is a square matrix of order $3$ with $|P| = 3$, then $|\operatorname{adj}(2P)|$ equals",
  r"$576$",
  [(r"$72$", "Takes $\\operatorname{adj}(2P) = 2\\operatorname{adj} P$, giving $2^3 \\cdot 9$."),
   (r"$36$", "Takes $|2P| = 2|P| = 6$ and squares it."),
   (r"$144$", "Takes $|2P| = 2^2|P| = 12$ and squares it.")],
  r"$|2P| = 2^3 \cdot 3 = 24$, and $|\operatorname{adj} M| = |M|^2$ for order $3$, so $|\operatorname{adj}(2P)| = 24^2 = 576$. Equivalently $\operatorname{adj}(2P) = 4\operatorname{adj} P$ and $|4\operatorname{adj} P| = 64 \cdot 9 = 576$.",
  "Mishandling the scalar inside an adjoint or a determinant.",
  "U03-C-adj-scalar", "Combines the scalar rule with the adjoint power rule.",
  check=_c019, values=[576, 72, 36, 144], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P$ is a square matrix of order $3$ with $|P| = 3$, then the value of $|\operatorname{adj}(2P)|$ is", answer=576))

# ---------------------------------------------------------------- 020
A020 = Matrix([[2, 1, 3], [1, 0, 2], [0, 1, 1]])
q("U03-C-020", "Adjoint and inverse", "A single entry of the inverse", "Medium", "Multi-step computation MCQ",
  r"If $P = " + bm(A020) + r"$, then the entry in the second row and third column of $P^{-1}$ is",
  r"$\frac{1}{2}$",
  [(r"$1$", "Uses $\\frac{C_{23}}{|P|} = \\frac{-2}{-2}$, forgetting that the adjoint is the transposed cofactor matrix."),
   (r"$-\frac{1}{2}$", "Uses the minor $M_{32} = 1$ without the sign $(-1)^{3+2}$."),
   (r"$-1$", "Gives the cofactor $C_{32}$ and forgets to divide by $|P|$.")],
  r"$|P| = 2(0 - 2) - 1(1 - 0) + 3(1 - 0) = -2$. The $(2, 3)$ entry of $P^{-1}$ is $\frac{C_{32}}{|P|}$, where $C_{32} = -\begin{vmatrix} 2 & 3 \\ 1 & 2 \end{vmatrix} = -1$. So the entry is $\frac{-1}{-2} = \frac{1}{2}$.",
  "Forgetting the transpose in the adjoint when reading one entry.",
  "U03-C-inverse-entry", "Determinant plus the correct transposed cofactor.",
  check=lambda: A020.inv()[1, 2], values=[Rational(1, 2), 1, Rational(-1, 2), -1], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 021
A021 = Matrix([[3, 1], [5, 2]]); B021 = Matrix([[1, 2], [0, 1]])
def _c021():
    X = MatrixSymbol('X', 2, 2).as_explicit()
    sol = solve(list(X * A021 - B021), list(X), dict=True)[0]
    return X.subs(sol)
q("U03-C-021", "Adjoint and inverse", "Solving XA = B", "Medium", "Multi-step computation MCQ",
  r"If $X$ is a $2 \times 2$ matrix such that $X " + bm(A021) + r" = " + bm(B021) + r"$, then $X$ equals",
  opt(B021 * A021.inv()),
  [(opt(A021.inv() * B021), "Pre-multiplies by the inverse, computing $P^{-1}Q$ instead of $QP^{-1}$."),
   (opt(B021 * A021), "Multiplies by the given matrix instead of its inverse."),
   (opt(B021 * A021.inv().T), "Uses the cofactor matrix of $P$ without transposing it (here $|P| = 1$).")],
  r"Let $P = \begin{bmatrix} 3 & 1 \\ 5 & 2 \end{bmatrix}$ and $Q = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$. Then $|P| = 1$ and $P^{-1} = \begin{bmatrix} 2 & -1 \\ -5 & 3 \end{bmatrix}$. Post-multiplying $XP = Q$ by $P^{-1}$ gives $X = QP^{-1} = \begin{bmatrix} -8 & 5 \\ -5 & 3 \end{bmatrix}$.",
  "Placing the inverse on the wrong side.",
  "U03-C-matrix-eq-XA-B", "Inverse plus a product whose order is the trap.",
  check=_c021, values=[B021 * A021.inv(), A021.inv() * B021, B021 * A021, B021 * A021.inv().T],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 022
A022 = Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
q("U03-C-022", "Adjoint and inverse", "Inverse via a quadratic relation", "Medium", "Multi-step computation MCQ",
  r"If $P = " + bm(A022) + r"$, then $P^{-1}$ equals",
  r"$\frac{1}{2}(P - I)$",
  [(r"$\frac{1}{2}(P + I)$", "Factorises $P^2 - P = 2I$ wrongly as $P(P + I) = 2I$."),
   (r"$\frac{1}{2}(I - P)$", "Moves $2I$ across with the wrong sign, writing $P(P - I) = -2I$."),
   (r"$P - I$", "Reaches $P(P - I) = 2I$ but forgets to divide by $2$.")],
  r"Squaring, $P^2 = \begin{bmatrix} 2 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2 \end{bmatrix} = P + 2I$. So $P(P - I) = 2I$, and $P^{-1} = \frac{1}{2}(P - I)$.",
  "Sign and scaling slips when turning a matrix relation into an inverse.",
  "U03-C-inverse-from-polynomial", "Discover the relation $P^2 = P + 2I$, then rearrange.",
  check=lambda: A022.inv(), values=[(A022 - I3) / 2, (A022 + I3) / 2, (I3 - A022) / 2, A022 - I3],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 023
P023 = Matrix([[1, tan(x)], [-tan(x), 1]])
q("U03-C-023", "Adjoint and inverse", "Product of transpose and inverse", "Medium", "Multi-step computation MCQ",
  r"If $P = \begin{bmatrix} 1 & \tan x \\ -\tan x & 1 \end{bmatrix}$, where $0 < x < \frac{\pi}{4}$, then $P^T P^{-1}$ equals",
  r"$\begin{bmatrix} \cos 2x & -\sin 2x \\ \sin 2x & \cos 2x \end{bmatrix}$",
  [(r"$\begin{bmatrix} \cos 2x & \sin 2x \\ -\sin 2x & \cos 2x \end{bmatrix}$", "Computes $P(P^T)^{-1}$, interchanging the roles of $P$ and $P^T$, which gives the transposed rotation."),
   (r"$\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$", "Assumes $P^T = P^{-1}$, that is, that $P$ is orthogonal."),
   (r"$\begin{bmatrix} \cos x & -\sin x \\ \sin x & \cos x \end{bmatrix}$", "Simplifies $\\frac{1 - \\tan^2 x}{1 + \\tan^2 x}$ to $\\cos x$ and $\\frac{2\\tan x}{1 + \\tan^2 x}$ to $\\sin x$, dropping the double angle.")],
  r"$|P| = 1 + \tan^2 x = \sec^2 x$ and $P^{-1} = \cos^2 x \begin{bmatrix} 1 & -\tan x \\ \tan x & 1 \end{bmatrix}$, while $P^T = \begin{bmatrix} 1 & -\tan x \\ \tan x & 1 \end{bmatrix}$. Hence $P^T P^{-1} = \cos^2 x \begin{bmatrix} 1 - \tan^2 x & -2\tan x \\ 2\tan x & 1 - \tan^2 x \end{bmatrix} = \begin{bmatrix} \cos 2x & -\sin 2x \\ \sin 2x & \cos 2x \end{bmatrix}$.",
  "Losing the double-angle identities or assuming orthogonality.",
  "U03-C-ATAinv-trig", "Inverse, product and two trigonometric identities.",
  check=lambda: simplify(P023.T * P023.inv()),
  values=[Matrix([[cos(2 * x), -sin(2 * x)], [sin(2 * x), cos(2 * x)]]), Matrix([[cos(2 * x), sin(2 * x)], [-sin(2 * x), cos(2 * x)]]),
          I2, Matrix([[cos(x), -sin(x)], [sin(x), cos(x)]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 024
q("U03-C-024", "Adjoint and inverse", "adj(adj A) as a multiple of A", "Medium", "Multi-step computation MCQ",
  r"If $P = " + bm(S3) + r"$, then $\operatorname{adj}(\operatorname{adj} P)$ equals",
  r"$3P$",
  [(r"$9P$", "Uses $|P|^{n-1}P$ instead of $|P|^{n-2}P$."),
   (r"$P$", "Uses the $2 \\times 2$ result $\\operatorname{adj}(\\operatorname{adj} P) = P$."),
   (r"$\frac{1}{3}P$", "Confuses $\\operatorname{adj}(\\operatorname{adj} P)$ with $(\\operatorname{adj} P)^{-1} = \\frac{P}{|P|}$.")],
  r"$|P| = 1(2 - 0) - 1(0 - 1) + 0 = 3$. For order $n$, $\operatorname{adj}(\operatorname{adj} P) = |P|^{n-2}P$, so with $n = 3$ it equals $3P$.",
  "Using the wrong power of $|P|$ in $\\operatorname{adj}(\\operatorname{adj} P)$.",
  "U03-C-adj-adj-matrix", "Determinant plus the adj(adj) identity.",
  check=lambda: S3.adjugate().adjugate(), values=[3 * S3, 9 * S3, S3, S3 / 3], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 025
def _c025():
    M = Matrix(3, 3, symbols('m0:9'))
    s1 = simplify((M.T).adjugate() - (M.adjugate()).T) == zeros(3)
    A_ = Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]); B_ = Matrix([[2, 1, 0], [0, 1, 3], [1, 0, 1]])
    s2 = (A_ * B_).adjugate() == A_.adjugate() * B_.adjugate()
    return (bool(s1), bool(s2))
key, oth, vals = st_item(ST_OPTS[2])
q("U03-C-025", "Adjoint and inverse", "Properties of the adjoint", "Medium", "Statement-based MCQ",
  r"Statement I: For every square matrix $P$ of order $3$, $\operatorname{adj}(P^T) = (\operatorname{adj} P)^T$. Statement II: For all invertible matrices $P$ and $Q$ of order $3$, $\operatorname{adj}(PQ) = (\operatorname{adj} P)(\operatorname{adj} Q)$. In the light of the above statements, choose the correct answer.",
  key,
  [(oth[0], "Accepts the product rule in Statement II without reversing the order."),
   (oth[1], "Doubts Statement I because transposing changes the cofactor positions, and rejects Statement II correctly."),
   (oth[2], "Rejects Statement I and accepts Statement II, mixing up the transpose rule and the reversal law.")],
  r"The cofactor of the $(i, j)$ entry of $P^T$ equals the cofactor of the $(j, i)$ entry of $P$, so $\operatorname{adj}(P^T) = (\operatorname{adj} P)^T$; Statement I is true. For invertible $P, Q$, $\operatorname{adj}(PQ) = |PQ|(PQ)^{-1} = |Q|Q^{-1} \cdot |P|P^{-1} = (\operatorname{adj} Q)(\operatorname{adj} P)$, with the order reversed, and in general this differs from $(\operatorname{adj} P)(\operatorname{adj} Q)$; Statement II is false.",
  "Forgetting the reversal of order for the adjoint of a product.",
  "U03-C-stmt-adj-props", "Two adjoint properties, one needing the reversal law.",
  check=_c025, values=vals, cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 026
def _c026():
    s, p_, r_ = symbols('s p r')
    Sy = Matrix([[2, s], [s, 3]])
    s1 = simplify(Sy.inv() - Sy.inv().T) == zeros(2)
    U = Matrix([[a, b, c], [0, k, s], [0, 0, p_]])
    Ui = U.inv()
    s2 = all(simplify(Ui[i, j]) == 0 for i in range(3) for j in range(3) if i > j)
    return (bool(s1), bool(s2))
key, oth, vals = st_item(ST_OPTS[0])
q("U03-C-026", "Adjoint and inverse", "Structure preserved by inversion", "Medium", "Statement-based MCQ",
  r"Statement I: If $P$ is an invertible symmetric matrix, then $P^{-1}$ is symmetric. Statement II: If $P$ is an invertible upper triangular matrix of order $3$, then $P^{-1}$ is upper triangular. In the light of the above statements, choose the correct answer.",
  key,
  [(oth[0], "Believes inversion destroys both symmetry and triangular form."),
   (oth[1], "Accepts Statement I but thinks transposing cofactors turns an upper triangular inverse into a lower triangular one."),
   (oth[2], "Thinks the inverse of a symmetric matrix is skew-symmetric, while accepting Statement II.")],
  r"If $P^T = P$, then $(P^{-1})^T = (P^T)^{-1} = P^{-1}$, so Statement I is true. For upper triangular $P$ with non-zero diagonal, each cofactor $C_{ij}$ with $i < j$ is the determinant of a triangular block with a zero on its diagonal, so it vanishes; after transposing, the adjoint and hence $P^{-1} = \frac{\operatorname{adj} P}{|P|}$ have zeros below the diagonal. Statement II is true.",
  "Thinking inversion changes symmetric or triangular structure.",
  "U03-C-stmt-inverse-structure", "Two structural facts about inverses.",
  check=_c026, values=vals, cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 027
def _c027():
    K2 = Matrix([[0, 3], [-3, 0]])
    s1 = K2.inv() == K2.inv().T
    K3 = Matrix([[0, 1, 2], [-1, 0, 3], [-2, -3, 0]])
    Ad = K3.adjugate()
    s2 = Ad == -Ad.T
    return (bool(s1), bool(s2))
key, oth, vals = st_item(ST_OPTS[1])
q("U03-C-027", "Adjoint and inverse", "Inverse and adjoint of skew-symmetric matrices", "Medium", "Statement-based MCQ",
  r"Statement I: If $P$ is a non-zero skew-symmetric matrix of order $2$, then $P^{-1}$ is symmetric. Statement II: If $P$ is a skew-symmetric matrix of order $3$, then $\operatorname{adj} P$ is skew-symmetric. In the light of the above statements, choose the correct answer.",
  key,
  [(oth[0], "Accepts both claims without checking an example."),
   (oth[1], "Accepts Statement I, missing that $(P^{-1})^T = (P^T)^{-1} = -P^{-1}$."),
   (oth[2], "Assumes the adjoint inherits skew-symmetry, as the inverse does.")],
  r"For $P = \begin{bmatrix} 0 & p \\ -p & 0 \end{bmatrix}$ with $p \ne 0$, $(P^{-1})^T = (P^T)^{-1} = -P^{-1}$, so $P^{-1} = \begin{bmatrix} 0 & -\frac{1}{p} \\ \frac{1}{p} & 0 \end{bmatrix}$ is skew-symmetric, not symmetric (it is non-zero). Statement I is false. For order $3$, $\operatorname{adj}(P^T) = (\operatorname{adj} P)^T$ and $\operatorname{adj}(-P) = (-1)^2\operatorname{adj} P$, so $(\operatorname{adj} P)^T = \operatorname{adj}(-P) = \operatorname{adj} P$: the adjoint is symmetric. For example $\begin{bmatrix} 0 & 1 & 2 \\ -1 & 0 & 3 \\ -2 & -3 & 0 \end{bmatrix}$ has the non-zero symmetric adjoint $\begin{bmatrix} 9 & -6 & 3 \\ -6 & 4 & -2 \\ 3 & -2 & 1 \end{bmatrix}$. Statement II is false.",
  "Assuming skew-symmetry behaves the same way under inversion and under taking the adjoint.",
  "U03-C-stmt-skew-adj", "Two transpose arguments with a sign power that depends on the order.",
  check=_c027, values=vals, cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 028
def _c028():
    E = Matrix([[1, 0], [0, 0]])
    s1 = (E**2 == E) and E != zeros(2) and E.det() != 0
    A_ = Matrix([[2, 1], [1, 1]]); Bm = Matrix(2, 2, symbols('b0:4')); Cm = Matrix(2, 2, symbols('c0:4'))
    sol = solve(list(A_ * Bm - A_ * Cm), list(Bm), dict=True)
    s2 = len(sol) == 1 and all(sol[0][Bm[i]] == Cm[i] for i in range(4))
    return (bool(s1), bool(s2))
key, oth, vals = st_item(ST_OPTS[3])
q("U03-C-028", "Adjoint and inverse", "Idempotent matrices and cancellation", "Medium", "Statement-based MCQ",
  r"Statement I: Every non-zero square matrix $P$ with $P^2 = P$ is invertible. Statement II: If $P$ is a non-singular matrix and $PQ = PR$ for matrices $Q, R$ of the same order, then $Q = R$. In the light of the above statements, choose the correct answer.",
  key,
  [(oth[0], "Cancels $P$ in $P^2 = P$ to get $P = I$, so accepts Statement I."),
   (oth[1], "Correctly rejects Statement I, but thinks matrix cancellation is never valid, so also rejects Statement II."),
   (oth[2], "Cancels $P$ in $P^2 = P$ to get $P = I$, so accepts Statement I, and doubts that matrix cancellation is ever valid.")],
  r"$P = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ is non-zero and satisfies $P^2 = P$, but $|P| = 0$; Statement I is false (cancelling $P$ needs $P^{-1}$, which is what is in question). If $P$ is non-singular, pre-multiplying $PQ = PR$ by $P^{-1}$ gives $Q = R$; Statement II is true.",
  "Cancelling a matrix without knowing that it is invertible.",
  "U03-C-stmt-cancellation", "Counterexample for one claim, inverse argument for the other.",
  check=_c028, values=vals, cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 029
A029 = Matrix([[1, 0, 1], [2, k, 0], [0, 1, 1]])
def _c029():
    sols = solve(Eq(A029.adjugate().det(), 64), k)
    return sum(s for s in sols if s.is_real)
q("U03-C-029", "Adjoint and inverse", "Parameter from the determinant of the adjoint", "Medium", "Inverse/parameter MCQ",
  r"If $P = " + bm(A029) + r"$ and $|\operatorname{adj} P| = 64$, then the sum of all real values of $k$ is",
  r"$-4$",
  [(r"$2$", "Uses $|\\operatorname{adj} P| = |P|^3$, so $(k + 2)^3 = 64$ gives $k = 2$."),
   (r"$62$", "Uses $|\\operatorname{adj} P| = |P|$, so $k + 2 = 64$."),
   (r"$6$", "Takes only the positive square root, $k + 2 = 8$.")],
  r"$|P| = 1(k - 0) - 0 + 1(2 - 0) = k + 2$. For order $3$, $|\operatorname{adj} P| = |P|^2 = (k + 2)^2 = 64$, so $k + 2 = \pm 8$, giving $k = 6$ or $k = -10$. The sum is $-4$.",
  "Using the wrong power of $|P|$ or dropping the negative root.",
  "U03-C-adj-det-param", "Determinant with a parameter, adjoint power rule, two roots.",
  check=_c029, values=[-4, 2, 62, 6], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 030
Ai030 = Matrix([[2, -1], [-1, 1]]); B030 = Matrix([[1, 2], [1, 3]])
def _c030():
    A = Ai030.inv()
    return (A * B030).inv()
q("U03-C-030", "Adjoint and inverse", "Inverse of a product when one factor is given directly", "Medium", "Multi-step computation MCQ",
  r"If $P^{-1} = " + bm(Ai030) + r"$ and $Q = " + bm(B030) + r"$, then $(PQ)^{-1}$ equals",
  opt(B030.inv() * Ai030),
  [(opt(Ai030 * B030.inv()), "Uses the order $P^{-1}Q^{-1}$."),
   (opt(B030 * Ai030), "Forgets to invert $Q$ and uses $QP^{-1}$."),
   (opt(Ai030 * B030), "Forgets to invert $Q$ and also keeps the order $P^{-1}Q$.")],
  r"$|Q| = 3 - 2 = 1$, so $Q^{-1} = \begin{bmatrix} 3 & -2 \\ -1 & 1 \end{bmatrix}$. Then $(PQ)^{-1} = Q^{-1}P^{-1} = \begin{bmatrix} 3 & -2 \\ -1 & 1 \end{bmatrix}\begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix} = \begin{bmatrix} 8 & -5 \\ -3 & 2 \end{bmatrix}$.",
  "Reversing the order incorrectly or forgetting to invert the factor given directly.",
  "U03-C-inverse-product-order", "An inverse, the reversal law and a product.",
  check=_c030, values=[B030.inv() * Ai030, Ai030 * B030.inv(), B030 * Ai030, Ai030 * B030],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 031
def _c031():
    a_, b_, c_, d_ = symbols('a_ b_ c_ d_')
    P = Matrix([[a_, b_], [c_, d_]])
    vals_ = set()
    for s in solve(list(P**2 - I2), [a_, b_, c_, d_], dict=True):
        Ps = P.subs(s)
        if simplify(Ps - I2) == zeros(2, 2) or simplify(Ps + I2) == zeros(2, 2):
            continue  # excluded by the stem
        vals_.add(simplify((Ps.adjugate() + 3 * Ps.inv()).det()))
    assert len(vals_) == 1
    return vals_.pop()
q("U03-C-031", "Adjoint and inverse", "Matrix equal to its own inverse", "Medium", "Conceptual/application MCQ",
  r"Every square matrix $P$ of order $2$ satisfies $P^2 - (\operatorname{tr} P)P + |P|I = O$. Let $P$ be a real matrix of order $2$ such that $P^{-1} = P$, $P \ne I$ and $P \ne -I$. Then $\left|\operatorname{adj} P + 3P^{-1}\right|$ equals",
  r"$-4$",
  [(r"$16$", r"Takes $|P| = 1$ from $|P|^2 = 1$, so $\operatorname{adj} P = P$, the sum is $4P$ and $|4P| = 16|P| = 16$."),
   (r"$-2$", r"Finds $\operatorname{adj} P + 3P^{-1} = 2P$ correctly but uses $|2P| = 2|P|$ for order $2$, getting $2(-1) = -2$."),
   (r"$-16$", r"Finds $|P| = -1$ but takes $\operatorname{adj} P = P^{-1} = P$, ignoring the factor $|P|$, so the sum is $4P$ and $|4P| = 16(-1) = -16$.")],
  r"Since $P^2 = I$, the given identity becomes $(\operatorname{tr} P)P = (1 + |P|)I$. If $\operatorname{tr} P \ne 0$, $P$ would be a scalar matrix $\lambda I$ with $\lambda^2 = 1$, i.e. $P = \pm I$, which is excluded. So $\operatorname{tr} P = 0$ and $|P| = -1$. Then $\operatorname{adj} P = |P|P^{-1} = -P$ and $P^{-1} = P$, so $\operatorname{adj} P + 3P^{-1} = 2P$ and $|2P| = 2^2|P| = -4$.",
  r"Assuming $|P| = 1$ for a matrix equal to its own inverse, or forgetting $\operatorname{adj} P = |P|P^{-1}$.",
  "U03-C-involutory-adj-det", r"Must deduce $\operatorname{tr} P = 0$ and $|P| = -1$ from the exclusion $P \ne \pm I$, then combine $\operatorname{adj} P = |P|P^{-1}$ with $|kP| = k^2|P|$.",
  check=_c031, values=[-4, 16, -2, -16], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Every square matrix $P$ of order $2$ satisfies $P^2 - (\operatorname{tr} P)P + |P|I = O$. Let $P$ be a real matrix of order $2$ such that $P^{-1} = P$, $P \ne I$ and $P \ne -I$. Then the value of $\left|\operatorname{adj} P + 3P^{-1}\right|$ is", answer=-4))

# ---------------------------------------------------------------- 032
A032 = Matrix([[2, 3], [5, -2]])
def _c032():
    m = symbols('m')
    return solve(list(A032.inv() - A032 / m), m, dict=True)[0][m]
q("U03-C-032", "Adjoint and inverse", "Inverse as a multiple of the matrix", "Medium", "Inverse/parameter MCQ",
  r"If $P = " + bm(A032) + r"$ and $P^{-1} = \frac{1}{m}P$, then $m$ equals",
  r"$19$",
  [(r"$-19$", "Takes $\\operatorname{adj} P = P$, missing that $\\operatorname{adj} P = -P$, and divides by $|P| = -19$."),
   (r"$\frac{1}{19}$", "From $P^2 = 19I$ writes $P^{-1} = 19P$."),
   (r"$-\frac{1}{19}$", "Combines both slips: $P^{-1} = 19P$ with the sign of $|P|$.")],
  r"$P^2 = \begin{bmatrix} 4 + 15 & 6 - 6 \\ 10 - 10 & 15 + 4 \end{bmatrix} = 19I$. Hence $P \cdot \frac{1}{19}P = I$ and $P^{-1} = \frac{1}{19}P$, so $m = 19$. (Check: $|P| = -19$ and $\operatorname{adj} P = -P$.)",
  "Sign of the determinant versus the sign hidden in the adjoint.",
  "U03-C-inverse-multiple-of-A", "Square the matrix, then read off the scalar.",
  check=_c032, values=[19, -19, Rational(1, 19), Rational(-1, 19)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P = " + bm(A032) + r"$ and $P^{-1} = \frac{1}{m}P$, then the value of $m$ is", answer=19))

# ---------------------------------------------------------------- 033
A033 = Matrix([[2, 3], [1, 4]])
def _c033():
    al, be = symbols('alpha beta')
    s = solve(list(A033.inv() - al * A033 - be * I2), [al, be], dict=True)[0]
    return s[al] + s[be]
q("U03-C-033", "Adjoint and inverse", "Inverse as a linear combination of A and I", "Medium", "Inverse/parameter MCQ",
  r"If $P = " + bm(A033) + r"$ and $P^{-1} = \alpha P + \beta I$, then $\alpha + \beta$ equals",
  r"$1$",
  [(r"$-1$", "Uses $P^2 - 6P - 5I = O$, with the wrong sign on $|P|$, giving $P^{-1} = \\frac{1}{5}(P - 6I)$."),
   (r"$5$", "Reaches $P(6I - P) = 5I$ but forgets to divide by $5$, taking $\\alpha = -1, \\beta = 6$."),
   (r"$-\frac{7}{5}$", "Uses $P^2 + 6P + 5I = O$, so $P^{-1} = -\\frac{1}{5}(P + 6I)$.")],
  r"$\operatorname{tr} P = 6$ and $|P| = 5$, and indeed $P^2 = \begin{bmatrix} 7 & 18 \\ 6 & 19 \end{bmatrix} = 6P - 5I$. So $P(6I - P) = 5I$ and $P^{-1} = -\frac{1}{5}P + \frac{6}{5}I$. Thus $\alpha + \beta = -\frac{1}{5} + \frac{6}{5} = 1$.",
  "Sign errors in the relation $P^2 - (\\operatorname{tr} P)P + |P| I = O$.",
  "U03-C-inverse-from-polynomial", "Derive the quadratic relation, then rearrange and compare.",
  check=_c033, values=[1, -1, 5, Rational(-7, 5)], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P = " + bm(A033) + r"$ and $P^{-1} = \alpha P + \beta I$, then the value of $\alpha + \beta$ is", answer=1))

# ---------------------------------------------------------------- 034
A034 = Matrix([[1, 2], [3, 5]]); B034 = Matrix([[2, 1], [1, 1]]); C034 = Matrix([[1, 0], [2, 3]])
def _c034():
    X = MatrixSymbol('X', 2, 2).as_explicit()
    sol = solve(list(A034 * X * B034 - C034), list(X), dict=True)[0]
    return X.subs(sol)
q("U03-C-034", "Adjoint and inverse", "Solving AXB = C", "Medium", "Multi-step computation MCQ",
  r"If $X$ is a $2 \times 2$ matrix such that $" + bm(A034) + r" X " + bm(B034) + r" = " + bm(C034) + r"$, then $X$ equals",
  opt(A034.inv() * C034 * B034.inv()),
  [(opt(B034.inv() * C034 * A034.inv()), "Places both inverses on the wrong sides of the right-hand matrix."),
   (opt(A034.inv() * B034.inv() * C034), "Pre-multiplies by both inverses, ignoring that one factor stands to the right of $X$."),
   (opt(C034 * A034.inv() * B034.inv()), "Post-multiplies by both inverses, ignoring that one factor stands to the left of $X$.")],
  r"Write $PXQ = R$. Then $X = P^{-1}RQ^{-1}$. Here $|P| = -1$, $P^{-1} = \begin{bmatrix} -5 & 2 \\ 3 & -1 \end{bmatrix}$; $|Q| = 1$, $Q^{-1} = \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$. So $P^{-1}R = \begin{bmatrix} -1 & 6 \\ 1 & -3 \end{bmatrix}$ and $X = \begin{bmatrix} -1 & 6 \\ 1 & -3 \end{bmatrix}\begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix} = \begin{bmatrix} -7 & 13 \\ 4 & -7 \end{bmatrix}$.",
  "Treating matrix equations as if multiplication commuted.",
  "U03-C-matrix-eq-AXB", "Two inverses and two products in the right order.",
  check=_c034, values=[A034.inv() * C034 * B034.inv(), B034.inv() * C034 * A034.inv(), A034.inv() * B034.inv() * C034, C034 * A034.inv() * B034.inv()],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 035
q("U03-C-035", "Adjoint and inverse", "Adjoint of the inverse", "Medium", "Conceptual/application MCQ",
  r"If $P$ is a non-singular matrix of order $3$ with $|P| = 3$, then $\operatorname{adj}(P^{-1})$ equals",
  r"$\frac{1}{3}P$",
  [(r"$3P$", "Uses the factor $|P|$ where $|P^{-1}| = \\frac{1}{3}$ is needed."),
   (r"$\frac{1}{9}P$", "Uses $|P^{-1}|^2$, the factor from $|\\operatorname{adj}(P^{-1})|$, as the scalar."),
   (r"$\frac{1}{3}P^{-1}$", "Writes $\\operatorname{adj} M = |M| M$ with $M = P^{-1}$, forgetting to invert $M$.")],
  r"For any invertible $M$, $\operatorname{adj} M = |M| M^{-1}$. With $M = P^{-1}$: $\operatorname{adj}(P^{-1}) = |P^{-1}| (P^{-1})^{-1} = \frac{1}{3}P$.",
  "Mixing up $|P|$ and $|P^{-1}|$ in the adjoint formula.",
  "U03-C-adj-of-inverse", "One formula applied to $P^{-1}$ with care.",
  check=lambda: S3.inv().adjugate(), values=[S3 / 3, 3 * S3, S3 / 9, S3.inv() / 3], cognitive="Understanding", source_class="XII")

# ---------------------------------------------------------------- 036
A036 = Matrix([[2, 1, 0], [1, 3, 1], [0, 1, 2]])
q("U03-C-036", "Adjoint and inverse", "Trace of the inverse", "Medium", "Multi-step computation MCQ",
  r"If $P = " + bm(A036) + r"$, then the sum of the diagonal entries of $P^{-1}$ is",
  r"$\frac{7}{4}$",
  [(r"$14$", "Adds the diagonal cofactors $5 + 4 + 5$ and forgets to divide by $|P| = 8$."),
   (r"$\frac{1}{7}$", "Takes the reciprocal of $\\operatorname{tr} P = 7$."),
   (r"$\frac{4}{3}$", "Inverts each diagonal entry: $\\frac{1}{2} + \\frac{1}{3} + \\frac{1}{2}$.")],
  r"$|P| = 2(6 - 1) - 1(2 - 0) + 0 = 8$. The diagonal entries of $\operatorname{adj} P$ are $C_{11} = 5$, $C_{22} = 4$, $C_{33} = 5$. So $\operatorname{tr}(P^{-1}) = \frac{5 + 4 + 5}{8} = \frac{7}{4}$.",
  "Treating the inverse entrywise or forgetting the division by $|P|$.",
  "U03-C-inverse-trace", "Determinant and three cofactors.",
  check=lambda: A036.inv().trace(), values=[Rational(7, 4), 14, Rational(1, 7), Rational(4, 3)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 037
q("U03-C-037", "Adjoint and inverse", "Determinant of a product of inverse and adjoint", "Medium", "Multi-step computation MCQ",
  r"If $P$ is a non-singular matrix of order $3$ with $|P| = 3$, then $|2P^{-1} \operatorname{adj} P|$ equals",
  r"$24$",
  [(r"$8$", "Uses $|\\operatorname{adj} P| = |P|$, giving $8 \\cdot \\frac{1}{3} \\cdot 3$."),
   (r"$6$", "Takes $|2M| = 2|M|$, giving $2 \\cdot \\frac{1}{3} \\cdot 9$."),
   (r"$216$", "Uses $|P^{-1}| = |P|$, giving $8 \\cdot 3 \\cdot 9$.")],
  r"$|2P^{-1}\operatorname{adj} P| = 2^3 \, |P^{-1}| \, |\operatorname{adj} P| = 8 \cdot \frac{1}{3} \cdot 3^2 = 24$.",
  "Misapplying one of the three determinant rules.",
  "U03-C-det-chain", "Three determinant rules combined.",
  check=lambda: (2 * S3.inv() * S3.adjugate()).det(), values=[24, 8, 6, 216], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $P$ is a non-singular matrix of order $3$ with $|P| = 3$, then the value of $|2P^{-1} \operatorname{adj} P|$ is", answer=24))

# ---------------------------------------------------------------- 038
U038 = Matrix([[1, a, b], [0, 1, c], [0, 0, 1]])
q("U03-C-038", "Adjoint and inverse", "Inverse of a unit upper triangular matrix", "Medium", "Multi-step computation MCQ",
  r"If $P = \begin{bmatrix} 1 & a & b \\ 0 & 1 & c \\ 0 & 0 & 1 \end{bmatrix}$, then $P^{-1}$ equals",
  r"$\begin{bmatrix} 1 & -a & ac - b \\ 0 & 1 & -c \\ 0 & 0 & 1 \end{bmatrix}$",
  [(r"$\begin{bmatrix} 1 & -a & -b \\ 0 & 1 & -c \\ 0 & 0 & 1 \end{bmatrix}$", "Negates every off-diagonal entry, missing the product term in the corner."),
   (r"$\begin{bmatrix} 1 & -a & b - ac \\ 0 & 1 & -c \\ 0 & 0 & 1 \end{bmatrix}$", "Evaluates the minor $\\begin{vmatrix} a & b \\\\ 1 & c \\end{vmatrix}$ as $b - ac$, cross-multiplying in the wrong order."),
   (r"$\begin{bmatrix} 1 & 0 & 0 \\ -a & 1 & 0 \\ ac - b & -c & 1 \end{bmatrix}$", "Uses the cofactor matrix without transposing it.")],
  r"$|P| = 1$. The non-trivial cofactors are $C_{12} = 0$, $C_{21} = -a$, $C_{32} = -c$, $C_{31} = \begin{vmatrix} a & b \\ 1 & c \end{vmatrix} = ac - b$, and $C_{23} = C_{13} = 0$ with $C_{ii} = 1$. Transposing the cofactor matrix, $P^{-1} = \begin{bmatrix} 1 & -a & ac - b \\ 0 & 1 & -c \\ 0 & 0 & 1 \end{bmatrix}$. Check: the $(1, 3)$ entry of $PP^{-1}$ is $(ac - b) - ac + b = 0$.",
  "Assuming the inverse of $I + N$ is $I - N$ for strictly upper triangular $N$ with $N^2 \\ne O$.",
  "U03-C-inverse-triangular", "Symbolic cofactors with one non-obvious corner entry.",
  check=lambda: simplify(U038.inv()),
  values=[Matrix([[1, -a, a * c - b], [0, 1, -c], [0, 0, 1]]), Matrix([[1, -a, -b], [0, 1, -c], [0, 0, 1]]),
          Matrix([[1, -a, b - a * c], [0, 1, -c], [0, 0, 1]]), Matrix([[1, 0, 0], [-a, 1, 0], [a * c - b, -c, 1]])],
  cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 039
P039 = Matrix([[k, 1, 1], [1, k, 1], [1, 1, k]])
q("U03-C-039", "Adjoint and inverse", "Values of a parameter for which the inverse fails to exist", "Medium", "Inverse/parameter MCQ",
  r"The set of all real values of $k$ for which $P = \begin{bmatrix} k & 1 & 1 \\ 1 & k & 1 \\ 1 & 1 & k \end{bmatrix}$ is not invertible is",
  r"$\{1, -2\}$",
  [(r"$\{-1, 2\}$", "Factorises $|P|$ as $(k + 1)^2(k - 2)$, a sign slip in each factor."),
   (r"$\{1\}$", "Takes out the factor $(k - 1)$ from $R_1 - R_2$ but misses $(k + 2)$ from adding all rows."),
   (r"$\{-2\}$", "Divides by $(k - 1)^2$ while simplifying, losing the value $k = 1$.")],
  r"Adding all columns to the first, $|P| = (k + 2)\begin{vmatrix} 1 & 1 & 1 \\ 1 & k & 1 \\ 1 & 1 & k \end{vmatrix} = (k + 2)(k - 1)^2$. $P^{-1}$ fails to exist exactly when $|P| = 0$, that is $k = 1$ or $k = -2$.",
  "Losing a factor of the determinant while simplifying.",
  "U03-C-singular-param", "Factorising a symmetric determinant and linking it to invertibility.",
  check=lambda: FiniteSet(*solve(P039.det(), k)),
  values=[FiniteSet(1, -2), FiniteSet(-1, 2), FiniteSet(1), FiniteSet(-2)], cognitive="Application", source_class="XII")

# ---------------------------------------------------------------- 040
def _c040():
    Pm = S5
    Bm = Pm.adjugate(); Cm = 5 * Pm
    return Bm.adjugate().det() / Cm.det()
q("U03-C-040", "Adjoint and inverse", "Ratio of determinants built from adjoints", "Medium", "Multi-step computation MCQ",
  r"Let $P$ be a matrix of order $3$ with $|P| = 5$. If $Q = \operatorname{adj} P$ and $R = 5P$, then $\frac{|\operatorname{adj} Q|}{|R|}$ equals",
  r"$1$",
  [(r"$\frac{1}{25}$", "Takes $|\\operatorname{adj} Q| = |Q| = 25$."),
   (r"$25$", "Takes $|R| = 5|P| = 25$."),
   (r"$5$", "Takes $|R| = 5^2|P| = 125$.")],
  r"$|Q| = |P|^2 = 25$, so $|\operatorname{adj} Q| = |Q|^2 = 625$. Also $|R| = 5^3|P| = 625$. The ratio is $1$.",
  "Pulling a scalar out of a determinant with the wrong power, or forgetting the adjoint power rule.",
  "U03-C-det-chain", "Two adjoint power rules and a scalar rule.",
  check=_c040, values=[1, Rational(1, 25), 25, 5], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $P$ be a matrix of order $3$ with $|P| = 5$. If $Q = \operatorname{adj} P$ and $R = 5P$, then the value of $\frac{|\operatorname{adj} Q|}{|R|}$ is", answer=1))

# ---------------------------------------------------------------- 041
Adj041 = Matrix([[5, -2], [3, 1]])
def _c041():
    X = Matrix(2, 2, symbols('x0:4'))
    sol = solve(list(X.adjugate() - Adj041), list(X), dict=True)[0]
    return X.subs(sol)
q("U03-C-041", "Adjoint and inverse", "Recovering a 2 by 2 matrix from its adjoint", "Medium", "Inverse/parameter MCQ",
  r"If $P$ is a $2 \times 2$ matrix with $\operatorname{adj} P = " + bm(Adj041) + r"$, then $P$ equals",
  opt(Matrix([[1, 2], [-3, 5]])),
  [(opt(Matrix([[1, -3], [2, 5]])), "Swaps and negates correctly but then transposes as well."),
   (opt(Matrix([[Rational(1, 11), Rational(2, 11)], [Rational(-3, 11), Rational(5, 11)]])), "Takes $P = (\\operatorname{adj} P)^{-1}$, forgetting the factor $|P|$."),
   (opt(Matrix([[-1, 2], [-3, -5]])), "Swaps the diagonal entries and then negates all four entries instead of only the off-diagonal ones.")],
  r"For a $2 \times 2$ matrix, $\operatorname{adj}(\operatorname{adj} P) = P$. Applying the swap-and-negate rule to $\begin{bmatrix} 5 & -2 \\ 3 & 1 \end{bmatrix}$ gives $P = \begin{bmatrix} 1 & 2 \\ -3 & 5 \end{bmatrix}$. Check: $\operatorname{adj} P = \begin{bmatrix} 5 & -2 \\ 3 & 1 \end{bmatrix}$.",
  "Not knowing that the adjoint operation is self-reversing for order $2$.",
  "U03-C-A-from-adj", "Reversal of the adjoint, with a verification step.",
  check=_c041, values=[Matrix([[1, 2], [-3, 5]]), Matrix([[1, -3], [2, 5]]), Matrix([[Rational(1, 11), Rational(2, 11)], [Rational(-3, 11), Rational(5, 11)]]), Matrix([[-1, 2], [-3, -5]])],
  cognitive="Analysis", source_class="XII")

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 042
Adj042 = Matrix([[6, -5, 1], [-6, 8, -2], [2, -3, 1]])
A042 = Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 9]])
def _c042():
    d = sqrt(Adj042.det())  # |adj P| = |P|^2 and |P| > 0
    P = d * Adj042.inv()
    assert P.adjugate() == Adj042 and P.det() > 0
    return P
q("U03-C-042", "Adjoint and inverse", "Recovering a 3 by 3 matrix from its adjoint", "Difficult", "Multi-step computation MCQ",
  r"If $P$ is a matrix of order $3$ with $|P| > 0$ and $\operatorname{adj} P = " + bm(Adj042) + r"$, then $P$ equals",
  opt(A042),
  [(opt(A042 / 2), "Takes $P = (\\operatorname{adj} P)^{-1}$, forgetting the factor $|P| = 2$."),
   (opt(2 * A042), "Takes $|P| = |\\operatorname{adj} P| = 4$, so computes $4(\\operatorname{adj} P)^{-1}$."),
   (opt(A042.T), "Inverts correctly but writes the cofactors of $\\operatorname{adj} P$ without transposing them.")],
  r"$|\operatorname{adj} P| = 6(8 - 6) + 5(-6 + 4) + 1(18 - 16) = 12 - 10 + 2 = 4 = |P|^2$, so $|P| = 2$. Since $\operatorname{adj} P = |P|P^{-1}$, $P = |P| (\operatorname{adj} P)^{-1} = 2 \cdot \frac{\operatorname{adj}(\operatorname{adj} P)}{4}$. Computing the adjoint of the given matrix gives $\begin{bmatrix} 2 & 2 & 2 \\ 2 & 4 & 6 \\ 2 & 8 & 18 \end{bmatrix}$, so $P = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \\ 1 & 4 & 9 \end{bmatrix}$, which has $|P| = 2 > 0$.",
  "Forgetting that $P = |P|(\\operatorname{adj} P)^{-1}$ and that $|P|$ comes from $|\\operatorname{adj} P| = |P|^2$.",
  "U03-C-A-from-adj", "Sign condition, determinant of the adjoint, then a full 3 by 3 adjoint.",
  check=_c042, values=[A042, A042 / 2, 2 * A042, A042.T], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 043
def _c043():
    M = S2
    assert M.det() == 2
    v = (3 * (M.det() * M).adjugate()).det()
    f = factorint(v)
    return f.get(2, 0) + f.get(3, 0)
q("U03-C-043", "Adjoint and inverse", "Nested scalar, adjoint and determinant", "Difficult", "Multi-step computation MCQ",
  r"Let $P$ be a matrix of order $3$ with $|P| = 2$. If $\left|3\operatorname{adj}(|P|P)\right| = 2^{\alpha}3^{\beta}$, where $\alpha$ and $\beta$ are integers, then $\alpha + \beta$ equals",
  r"$11$",
  [(r"$8$", "Takes $\\operatorname{adj}(2P) = 2\\operatorname{adj} P$, so the value is $3^3 \\cdot 2^3 \\cdot 4 = 2^5 3^3$."),
   (r"$9$", "Takes $|3M| = 3|M|$, so the value is $3 \\cdot 16^2 = 2^8 \\cdot 3$."),
   (r"$15$", "Uses $|\\operatorname{adj} M| = |M|^3$, so the value is $3^3 \\cdot 16^3 = 2^{12}3^3$.")],
  r"$|P|P = 2P$ and $|2P| = 2^3 \cdot 2 = 16$. For order $3$, $|\operatorname{adj}(2P)| = |2P|^2 = 256$. Then $|3\operatorname{adj}(2P)| = 3^3 \cdot 256 = 2^8 \cdot 3^3$, so $\alpha = 8, \beta = 3$ and $\alpha + \beta = 11$.",
  "Mishandling one of the nested scalar factors.",
  "U03-C-det-chain-exponent", "Three nested rules with a scalar that is itself a determinant.",
  check=_c043, values=[11, 8, 9, 15], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $P$ be a matrix of order $3$ with $|P| = 2$. If $\left|3\operatorname{adj}(|P|P)\right| = 2^{\alpha}3^{\beta}$, where $\alpha$ and $\beta$ are integers, then the value of $\alpha + \beta$ is", answer=11))

# ---------------------------------------------------------------- 044
def _c044():
    A = S2  # normal: A A^T = A^T A, non-symmetric, |A| = 2
    assert A * A.T == A.T * A and A != A.T
    Bq = A.inv() * A.T
    return Bq * Bq.T
_B044 = S2.inv() * S2.T
q("U03-C-044", "Adjoint and inverse", "Orthogonality from commuting transpose", "Difficult", "Conceptual/application MCQ",
  r"Let $P$ be a real, non-singular, non-symmetric matrix of order $3$ such that $PP^T = P^TP$, and let $Q = P^{-1}P^T$. Then, for every such $P$, $QQ^T$ necessarily equals",
  r"$I$",
  [(r"$-I$", r"Writes $(P^{-1})^T = -(P^T)^{-1}$, as if transposing an inverse introduced a sign, so $Q^T = -P(P^T)^{-1}$ and $QQ^T = -I$."),
   (r"$Q$", r"Expands $QQ^T = P^{-1}P^T \cdot P(P^T)^{-1}$ and treats the trailing factor $P(P^T)^{-1}$ as $I$."),
   (r"$Q^T$", r"Expands $QQ^T = P^{-1}P^T \cdot P(P^T)^{-1}$ and treats the leading factor $P^{-1}P^T$ as $I$.")],
  r"$Q^T = (P^T)^T(P^{-1})^T = P(P^T)^{-1}$. So $QQ^T = P^{-1}P^T P (P^T)^{-1} = P^{-1}(PP^T)(P^T)^{-1}$, using $P^TP = PP^T$. This is $(P^{-1}P)(P^T(P^T)^{-1}) = I$. (Note $Q \ne I$, since $Q = I$ would force $P^T = P$; so neither $Q$ nor $Q^T = Q^{-1}$ can equal $I$, and $QQ^T$ has non-negative diagonal entries, so it is never $-I$.)",
  "Reversing order incorrectly when transposing a product of an inverse and a transpose.",
  "U03-C-normal-orthogonal", "Transpose of a product, then a substitution using the commuting hypothesis.",
  check=_c044, values=[I3, -I3, _B044, _B044.T], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 045
def _c045():
    al = symbols('alpha')
    Pm = Matrix([[2, al, 1], [1, 3, 2], [1, 1, 3]])
    av = solve(Eq(Pm.det(), 3**2), al)[0]  # |adj Q| = |Q|^2
    Pv = Pm.subs(al, av)
    Qm = Pv.adjugate() / 3                 # adj(adj Q) = |Q| Q
    assert Qm.det() == 3 and Qm.adjugate() == Pv
    return Qm.trace()
q("U03-C-045", "Adjoint and inverse", "Matrix from its adjoint with a parameter", "Difficult", "Multi-step computation MCQ",
  r"Let $Q$ be a matrix of order $3$ with $|Q| = 3$, and let $\operatorname{adj} Q = \begin{bmatrix} 2 & \alpha & 1 \\ 1 & 3 & 2 \\ 1 & 1 & 3 \end{bmatrix}$. Then the sum of the diagonal entries of $Q$ is",
  r"$5$",
  [(r"$15$", "Finds $\\alpha = 3$ but uses the $2 \\times 2$ fact $\\operatorname{adj}(\\operatorname{adj} Q) = Q$, so takes the trace of $\\operatorname{adj}(\\operatorname{adj} Q)$ itself."),
   (r"$\frac{5}{3}$", "Finds $\\alpha = 3$ but takes $Q = (\\operatorname{adj} Q)^{-1}$, forgetting the factor $|Q|$."),
   (r"$45$", "Finds $\\alpha = 3$ but writes $\\operatorname{adj}(\\operatorname{adj} Q) = \\frac{1}{|Q|}Q$, so $Q = 3\\operatorname{adj}(\\operatorname{adj} Q)$.")],
  r"$|\operatorname{adj} Q| = |Q|^2 = 9$, and expanding, $|\operatorname{adj} Q| = 2(9 - 2) - \alpha(3 - 2) + 1(1 - 3) = 12 - \alpha$, so $\alpha = 3$. For order $3$, $\operatorname{adj}(\operatorname{adj} Q) = |Q|Q$, so $Q = \frac{1}{3}\operatorname{adj}(\operatorname{adj} Q)$. The diagonal cofactors of $\operatorname{adj} Q$ are $9 - 2 = 7$, $6 - 1 = 5$ and $6 - 3 = 3$, so $\operatorname{tr} Q = \frac{7 + 5 + 3}{3} = 5$.",
  "Using the wrong form of $\\operatorname{adj}(\\operatorname{adj} Q)$ for order $3$.",
  "U03-C-adj-det-param", "Parameter from the adjoint determinant, then recovering $Q$ via adj(adj).",
  check=_c045, values=[5, 15, Rational(5, 3), 45], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $Q$ be a matrix of order $3$ with $|Q| = 3$, and let $\operatorname{adj} Q = \begin{bmatrix} 2 & \alpha & 1 \\ 1 & 3 & 2 \\ 1 & 1 & 3 \end{bmatrix}$. Then the sum of the diagonal entries of $Q$ is", answer=5))

# ---------------------------------------------------------------- 046
def _c046():
    av, bv = symbols('a_ b_', real=True)
    P = Matrix([[3 * av, -bv], [2, 3]])
    sols = solve(list(P * P.adjugate() - P * P.T), [av, bv], dict=True)
    vals_ = set(s[av] + s[bv] for s in sols)
    assert len(vals_) == 1
    return vals_.pop()
q("U03-C-046", "Adjoint and inverse", "Equating A adj A with A A^T", "Difficult", "Inverse/parameter MCQ",
  r"Let $P = \begin{bmatrix} 3a & -b \\ 2 & 3 \end{bmatrix}$, where $a, b \in \mathbb{R}$. If $P(\operatorname{adj} P) = PP^T$, then $a + b$ equals",
  r"$3$",
  [(r"$\frac{39}{5}$", "Takes $|P| = 9a - 2b$, a sign slip, so $b = 2a$ and $5a = 13$."),
   (r"$-\frac{13}{5}$", "Writes the off-diagonal entry of $PP^T$ as $6a + 3b$, so $b = -2a$ and $5a = 13$."),
   (r"$-3$", "Uses only $9a^2 + b^2 = 13$ and $b = 2a$, accepting $a = -1$ without checking $9a + 2b = 13$.")],
  r"$P(\operatorname{adj} P) = |P|I = (9a + 2b)I$, while $PP^T = \begin{bmatrix} 9a^2 + b^2 & 6a - 3b \\ 6a - 3b & 13 \end{bmatrix}$. Comparing: $6a - 3b = 0$ gives $b = 2a$; the $(2, 2)$ entries give $9a + 2b = 13$, so $13a = 13$, $a = 1$, $b = 2$; and the $(1, 1)$ entry $9 + 4 = 13$ agrees. Hence $a + b = 3$.",
  "Not using all entries of the matrix equation or slipping on $|P|$.",
  "U03-C-AadjA-AAT", "Combines $P\\operatorname{adj}P = |P|I$ with a matrix product and three conditions.",
  check=_c046, values=[3, Rational(39, 5), Rational(-13, 5), -3], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $P = \begin{bmatrix} 3a & -b \\ 2 & 3 \end{bmatrix}$, where $a, b \in \mathbb{R}$. If $P(\operatorname{adj} P) = PP^T$, then the value of $a + b$ is", answer=3))

# ---------------------------------------------------------------- 047
N047 = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
q("U03-C-047", "Adjoint and inverse", "Inverse of I + kN for nilpotent N", "Difficult", "Conceptual/application MCQ",
  r"Let $N$ be a square matrix of order $3$ such that $N^3 = O$ but $N^2 \ne O$. Then $(I + 2N)^{-1}$ equals",
  r"$I - 2N + 4N^2$",
  [(r"$I + 2N + 4N^2$", "Uses the expansion for $(I - 2N)^{-1}$, a sign slip."),
   (r"$I - 2N + 2N^2$", "Does not square the coefficient $2$ in the third term."),
   (r"$I - 2N$", "Truncates the expansion, as if $N^2 = O$.")],
  r"Since $N^3 = O$, $(I + 2N)(I - 2N + 4N^2) = I - 2N + 4N^2 + 2N - 4N^2 + 8N^3 = I + 8N^3 = I$. Hence $(I + 2N)^{-1} = I - 2N + 4N^2$.",
  "Mishandling signs and powers when inverting $I + kN$ for nilpotent $N$.",
  "U03-C-nilpotent-inverse", "Recognise a finite geometric series and verify by multiplication.",
  check=lambda: (I3 + 2 * N047).inv(),
  values=[I3 - 2 * N047 + 4 * N047**2, I3 + 2 * N047 + 4 * N047**2, I3 - 2 * N047 + 2 * N047**2, I3 - 2 * N047],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 048
E048 = Matrix([[1, 1], [0, 0]])
def _c048():
    assert E048**2 == E048
    return (I2 + E048).inv()
q("U03-C-048", "Adjoint and inverse", "Inverse of I + A for idempotent A", "Difficult", "Conceptual/application MCQ",
  r"Let $P$ be a square matrix with $P^2 = P$, $P \ne O$ and $P \ne I$. Then $(I + P)^{-1}$ equals",
  r"$I - \frac{1}{2}P$",
  [(r"$I - P$", "Truncates $I - P + P^2 - \\dots$ after two terms."),
   (r"$I + \frac{1}{2}P$", "Sign slip in the trial inverse."),
   (r"$2I - P$", "Finds $(I + P)(2I - P) = 2I$ but forgets to divide by $2$.")],
  r"Try $(I + P)(I + xP) = I + (1 + 2x)P$, using $P^2 = P$. This equals $I$ when $x = -\frac{1}{2}$. Hence $(I + P)^{-1} = I - \frac{1}{2}P$.",
  "Treating the series for $(I + P)^{-1}$ naively instead of using $P^2 = P$.",
  "U03-C-idempotent-inverse", "Needs an ansatz and the idempotent relation; non-routine.",
  check=_c048, values=[I2 - E048 / 2, I2 - E048, I2 + E048 / 2, 2 * I2 - E048], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 049
A049 = Matrix([[0, 1], [1, -1]]); B049 = Matrix([[3, 1], [2, 4]])
def _c049():
    X = MatrixSymbol('X', 2, 2).as_explicit()
    sol = solve(list(2 * X + A049 * X - B049), list(X), dict=True)[0]
    return X.subs(sol)
q("U03-C-049", "Adjoint and inverse", "Matrix equation needing a common factor", "Difficult", "Multi-step computation MCQ",
  r"If $X$ is a $2 \times 2$ matrix such that $2X + " + bm(A049) + r"X = " + bm(B049) + r"$, then $X$ equals",
  opt((2 * I2 + A049).inv() * B049),
  [(opt(B049 * (2 * I2 + A049).inv()), "Factorises correctly but post-multiplies by the inverse."),
   (opt((2 * A049).inv() * B049), "Combines $2X + PX$ into $2PX$."),
   (opt((A049 + 2 * ones(2, 2)).inv() * B049), "Writes $2X + PX = (2 + P)X$ and adds $2$ to every entry of $P$ instead of using $2I$.")],
  r"Let $P$ be the given coefficient matrix. Then $2X + PX = (2I + P)X$, with $2I + P = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$, determinant $1$ and inverse $\begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$. So $X = \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}\begin{bmatrix} 3 & 1 \\ 2 & 4 \end{bmatrix} = \begin{bmatrix} 1 & -3 \\ 1 & 7 \end{bmatrix}$.",
  "Factoring out $X$ as if $2$ were a matrix of twos, or on the wrong side.",
  "U03-C-matrix-eq-factor", "Factor with $2I$, invert, and multiply on the correct side.",
  check=_c049, values=[(2 * I2 + A049).inv() * B049, B049 * (2 * I2 + A049).inv(), (2 * A049).inv() * B049, (A049 + 2 * ones(2, 2)).inv() * B049],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 050
def _c050():
    import itertools
    cnt = 0
    for p, q_, r, s in itertools.product(range(3), repeat=4):
        M = Matrix([[p, q_], [r, s]])
        if M.det() != 0 and all(e.is_integer for e in M.inv()):
            cnt += 1
    return cnt
q("U03-C-050", "Adjoint and inverse", "Counting matrices with integer inverses", "Difficult", "Multi-step computation MCQ",
  r"The number of $2 \times 2$ matrices with every entry from $\{0, 1, 2\}$ that are invertible and whose inverse has all entries integers is",
  r"$14$",
  [(r"$7$", "Counts only the matrices with determinant $1$, missing determinant $-1$."),
   (r"$50$", "Counts all invertible matrices, ignoring the integer condition."),
   (r"$38$", "Also accepts determinant $\\pm 2$, assuming the even entries make division by $2$ safe.")],
  r"An integer matrix has an integer inverse exactly when its determinant is $\pm 1$ (since $|P||P^{-1}| = 1$ with both integers, and $\operatorname{adj} P$ is an integer matrix). With $P = \begin{bmatrix} p & q \\ r & s \end{bmatrix}$, the product $ps$ takes the values $0, 1, 2, 4$ in $5, 1, 2, 1$ ways respectively, and the same holds for $qr$. $ps - qr = 1$ needs $(ps, qr) = (1, 0)$ or $(2, 1)$: $1 \cdot 5 + 2 \cdot 1 = 7$ ways. By symmetry $ps - qr = -1$ also has $7$. Total $14$.",
  "Missing the negative determinant or forgetting that the integer condition forces $|P| = \\pm 1$.",
  "U03-C-count-integer-inverse", "Needs the determinant criterion and careful casework counting.",
  check=_c050, values=[14, 7, 50, 38], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of $2 \times 2$ matrices with every entry from $\{0, 1, 2\}$ that are invertible and whose inverse has all entries integers is", answer=14))

# ---------------------------------------------------------------- 051
def _c051():
    Sk = Matrix([[0, 1, 2], [-1, 0, 3], [-2, -3, 0]])
    M = (I3 - Sk) * (I3 + Sk).inv()
    return (M * M.T == I3, M.T == M, M * M == I3, M.det() == -1)
q("U03-C-051", "Adjoint and inverse", "Inverse in the Cayley form", "Difficult", "Conceptual/application MCQ",
  r"Let $S$ be a non-zero real skew-symmetric matrix of order $3$ (so that $I + S$ is invertible), and let $M = (I - S)(I + S)^{-1}$. Which of the following is true?",
  r"$MM^T = I$",
  [(r"$M^T = M$", "Transposes $(I - S)(I + S)^{-1}$ without reversing the order and uses $S^T = S$."),
   (r"$M^2 = I$", "Believes $(I + S)^{-1}$ undoes $(I - S)$ in a product of $M$ with itself."),
   (r"$|M| = -1$", "Uses $|I - S| = -|I + S|$, attaching a sign to the transpose.")],
  r"$I - S$ and $(I + S)^{-1}$ commute, since $I - S$ and $I + S$ commute. $M^T = ((I + S)^{-1})^T(I - S)^T = (I - S)^{-1}(I + S)$, using $S^T = -S$. Then $MM^T = (I - S)(I + S)^{-1}(I - S)^{-1}(I + S) = I$. Also $|M| = \frac{|I - S|}{|I + S|} = 1$ because $I - S = (I + S)^T$. Finally $M^2 = I$ would give $(I - S)^2 = (I + S)^2$, that is $S = O$, and $M^T = M$ is equivalent to $M^2 = I$ here; both fail for non-zero $S$.",
  "Mishandling transpose and inverse of products.",
  "U03-C-cayley-transform", "Transpose and inverse of a product with commuting factors, plus exclusion of three claims.",
  check=_c051, values=[(True, False, False, False), (False, True, False, False), (False, False, True, False), (False, False, False, True)],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 052
Ai052 = Matrix([[1, 1], [1, 3]]); Bi052 = Matrix([[2, 1], [1, 2]])
def _c052():
    A = Ai052.inv(); B = Bi052.inv()
    return (A * B).adjugate()
q("U03-C-052", "Adjoint and inverse", "Adjoint of a product from the inverses", "Difficult", "Multi-step computation MCQ",
  r"If $P$ and $Q$ are $2 \times 2$ matrices with $P^{-1} = " + bm(Ai052) + r"$ and $Q^{-1} = " + bm(Bi052) + r"$, then $\operatorname{adj}(PQ)$ equals",
  opt(Bi052 * Ai052, r"\frac{1}{6}"),
  [(opt(Bi052 * Ai052, "6"), "Uses $|PQ| = |P^{-1}||Q^{-1}| = 6$ instead of its reciprocal."),
   (opt(Ai052 * Bi052, r"\frac{1}{6}"), "Uses the order $P^{-1}Q^{-1}$ for $(PQ)^{-1}$."),
   (opt(Bi052 * Ai052), "Takes $\\operatorname{adj}(PQ) = (PQ)^{-1}$, forgetting the factor $|PQ|$.")],
  r"$|P^{-1}| = 3 - 1 = 2$ and $|Q^{-1}| = 4 - 1 = 3$, so $|P| = \frac{1}{2}$, $|Q| = \frac{1}{3}$ and $|PQ| = \frac{1}{6}$. Then $\operatorname{adj}(PQ) = |PQ|(PQ)^{-1} = \frac{1}{6}Q^{-1}P^{-1} = \frac{1}{6}\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}\begin{bmatrix} 1 & 1 \\ 1 & 3 \end{bmatrix} = \frac{1}{6}\begin{bmatrix} 3 & 5 \\ 3 & 7 \end{bmatrix}$.",
  "Confusing adjoint and inverse, or inverting the determinant incorrectly.",
  "U03-C-adj-product", "Determinants of inverses, reversal law and the adjoint formula combined.",
  check=_c052, values=[Bi052 * Ai052 / 6, 6 * Bi052 * Ai052, Ai052 * Bi052 / 6, Bi052 * Ai052],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 053
A053 = Matrix([[3, 1, 1], [1, 3, 1], [1, 1, 3]])
q("U03-C-053", "Adjoint and inverse", "Sum of the entries of an inverse", "Difficult", "Multi-step computation MCQ",
  r"If $P = " + bm(A053) + r"$, then the sum of all the entries of $P^{-1}$ is",
  r"$\frac{3}{5}$",
  [(r"$\frac{1}{5}$", "Finds that each row of $P^{-1}$ sums to $\\frac{1}{5}$ and stops there."),
   (r"$12$", "Adds all the entries of $\\operatorname{adj} P$ and forgets to divide by $|P| = 20$."),
   (r"$\frac{1}{15}$", "Takes the reciprocal of the sum of all entries of $P$, which is $15$.")],
  r"Let $u$ be the column of three ones. Every row of $P$ sums to $5$, so $Pu = 5u$ and hence $P^{-1}u = \frac{1}{5}u$: each row of $P^{-1}$ sums to $\frac{1}{5}$. The sum of all entries is $3 \cdot \frac{1}{5} = \frac{3}{5}$. (Directly, $|P| = 20$ and the entries of $\operatorname{adj} P$ add up to $12$.)",
  "Stopping at a row sum or confusing the inverse with a reciprocal.",
  "U03-C-inverse-sum-entries", "Non-obvious shortcut via row sums, or a full 3 by 3 inverse.",
  check=lambda: sum(A053.inv()), values=[Rational(3, 5), Rational(1, 5), 12, Rational(1, 15)], cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 054
A054 = Matrix([[1, 0, 2], [0, 1, 0], [0, 0, 1]])
def _c054():
    assert A054**2 - 2 * A054 + I3 == zeros(3) and A054 != I3
    return A054.inv()**3
q("U03-C-054", "Adjoint and inverse", "Negative power from a matrix relation", "Difficult", "Multi-step computation MCQ",
  r"Let $P$ be a square matrix with $P^2 - 2P + I = O$ and $P \ne I$. Then $P^{-3}$ equals",
  r"$4I - 3P$",
  [(r"$3I - 2P$", "Stops at $P^{-2}$."),
   (r"$3P - 2I$", "Computes $P^3$ instead of $P^{-3}$."),
   (r"$2I - P$", "Stops at $P^{-1}$.")],
  r"From $P(2I - P) = I$, $P^{-1} = 2I - P$. Write $P = I + N$; the relation gives $N^2 = O$. Then $P^{-1} = I - N$ and $P^{-3} = (I - N)^3 = I - 3N = I - 3(P - I) = 4I - 3P$.",
  "Not iterating the inverse relation correctly to the third power.",
  "U03-C-inverse-power-relation", "Relation to inverse, then a power using $N^2 = O$.",
  check=_c054, values=[4 * I3 - 3 * A054, 3 * I3 - 2 * A054, 3 * A054 - 2 * I3, 2 * I3 - A054],
  cognitive="Analysis", source_class="XII")

# ---------------------------------------------------------------- 055
A055 = Matrix([[3, -4], [1, -1]])
q("U03-C-055", "Adjoint and inverse", "Large negative power of a matrix", "Difficult", "Multi-step computation MCQ",
  r"If $P = " + bm(A055) + r"$, then the sum of all the entries of $P^{-50}$ is",
  r"$152$",
  [(r"$-148$", "Computes $P^{50} = I + 50N$ instead of $P^{-50} = I - 50N$."),
   (r"$149$", "Uses $I - 49N$, an off-by-one in the exponent."),
   (r"$250$", "Takes $50$ times the sum of the entries of $P^{-1}$.")],
  r"Write $P = I + N$ with $N = \begin{bmatrix} 2 & -4 \\ 1 & -2 \end{bmatrix}$; then $N^2 = O$. So $P^{-1} = I - N$ and $P^{-50} = (I - N)^{50} = I - 50N = \begin{bmatrix} -99 & 200 \\ -50 & 101 \end{bmatrix}$. The sum of its entries is $-99 + 200 - 50 + 101 = 152$.",
  "Confusing positive and negative powers when $N^2 = O$.",
  "U03-C-inverse-power-relation", "Spotting $N^2 = O$ and combining inverse with a high power.",
  check=lambda: sum(A055**-50), values=[152, -148, 149, 250], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"If $P = " + bm(A055) + r"$, then the sum of all the entries of $P^{-50}$ is", answer=152))
