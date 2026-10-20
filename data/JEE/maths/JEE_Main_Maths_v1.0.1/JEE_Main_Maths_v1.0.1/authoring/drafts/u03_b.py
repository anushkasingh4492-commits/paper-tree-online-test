import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools
from sympy.calculus.util import function_range


def Q(*args, **kw):
    kw["source_class"] = "XII"
    q(*args, **kw)


x, k, t, th = symbols('x k t theta', real=True)
a, b, c = symbols('a b c')
w = exp(2*pi*I/3)


def gen3(name='m'):
    s = symbols(name + '1:10')
    return Matrix(3, 3, s)


# ---------------------------------------------------------------- EASY

Q("U03-B-001", "Determinants", "Evaluation of a third order determinant", "Easy", "Single-step computation MCQ",
  r"The value of the determinant $\begin{vmatrix} 2 & 1 & 3 \\ 0 & -1 & 4 \\ 1 & 2 & 5 \end{vmatrix}$ is",
  r"$-19$",
  [(r"$-27$", r"Uses $+a_{12}M_{12}$ instead of $-a_{12}M_{12}$: $2(-13) - 4 + 3 = -27$."),
   (r"$13$", r"Takes the minor of $a_{11}$ as $(-1)(5) + (4)(2) = 3$, adding the diagonal products: $6 + 4 + 3 = 13$."),
   (r"$-25$", r"Takes the third term with a minus sign: $-26 + 4 - 3 = -25$.")],
  r"Expanding along the first row: $2\,[(-1)(5) - (4)(2)] - 1\,[(0)(5) - (4)(1)] + 3\,[(0)(2) - (-1)(1)] = 2(-13) + 4 + 3 = -19$.",
  "Sign pattern of cofactors along the first row, and subtracting the cross product in each minor.",
  "U03-B-eval3-numeric", "Direct expansion of a numeric third order determinant; one idea.",
  check=lambda: Matrix([[2, 1, 3], [0, -1, 4], [1, 2, 5]]).det(), values=[-19, -27, 13, -25],
  cognitive="Application")

Q("U03-B-002", "Determinants", "Second order determinant with trigonometric entries", "Easy", "Single-step computation MCQ",
  r"The value of $\begin{vmatrix} \cos 15^\circ & \sin 15^\circ \\ \sin 15^\circ & \cos 15^\circ \end{vmatrix}$ is",
  r"$\frac{\sqrt{3}}{2}$",
  [(r"$1$", r"Adds the two products: $\cos^2 15^\circ + \sin^2 15^\circ = 1$."),
   (r"$\frac{1}{2}$", r"Multiplies the entries along each row and adds the results: $\cos 15^\circ\sin 15^\circ + \sin 15^\circ\cos 15^\circ = \sin 30^\circ = \frac{1}{2}$."),
   (r"$-\frac{\sqrt{3}}{2}$", r"Computes $bc - ad = \sin^2 15^\circ - \cos^2 15^\circ = -\cos 30^\circ$.")],
  r"The determinant is $\cos^2 15^\circ - \sin^2 15^\circ = \cos 30^\circ = \frac{\sqrt{3}}{2}$.",
  "Using the wrong double angle identity or reversing the order of subtraction.",
  "U03-B-eval2-trig", "One expansion followed by one standard identity.",
  check=lambda: nsimplify(simplify(Matrix([[cos(pi/12), sin(pi/12)], [sin(pi/12), cos(pi/12)]]).det())),
  values=[sqrt(3)/2, 1, Rational(1, 2), -sqrt(3)/2], cognitive="Application")


def _c3():
    A = diag(4, 1, 1)
    return (2*A).det()
Q("U03-B-003", "Properties of determinants", "Determinant of a scalar multiple", "Easy", "Single-step computation MCQ",
  r"If $P$ is a square matrix of order $3$ with $|P| = 4$, then $|2P|$ equals",
  r"$32$",
  [(r"$8$", r"Uses $|kP| = k|P|$, multiplying by $2$ only once."),
   (r"$16$", r"Uses $|kP| = k^2|P|$, the rule for order $2$."),
   (r"$24$", r"Multiplies by $3k = 6$ instead of $k^3 = 8$.")],
  r"Every one of the $3$ rows is multiplied by $2$, so $|2P| = 2^3|P| = 8 \times 4 = 32$.",
  r"Taking $|kP| = k|P|$ instead of $k^n|P|$.",
  "U03-B-kA-basic", "Single property application.",
  check=_c3, values=[32, 8, 16, 24], cognitive="Recall",
  numerical=dict(question=r"If $P$ is a square matrix of order $3$ with $|P| = 4$, then the value of $|2P|$ is", answer=32))


def _c4():
    A = diag(2, 1, 1); B = diag(5, 1, 1)
    return (A.T * B**2).det()
Q("U03-B-004", "Properties of determinants", "Determinant of a product and transpose", "Easy", "Single-step computation MCQ",
  r"Let $P$ and $Q$ be square matrices of order $3$ with $|P| = 2$ and $|Q| = 5$. Then $|P^{T} Q^{2}|$ equals",
  r"$50$",
  [(r"$20$", r"Takes $|Q^2| = 2|Q| = 10$, doubling instead of squaring."),
   (r"$-50$", r"Takes $|P^T| = -|P|$."),
   (r"$10$", r"Ignores the square on $Q$ and computes $|P||Q|$.")],
  r"$|P^T Q^2| = |P^T|\,|Q|^2 = 2 \times 25 = 50$, since $|P^T| = |P|$ and $|Q^2| = |Q|^2$.",
  r"Mishandling $|Q^n| = |Q|^n$ or $|P^T| = |P|$.",
  "U03-B-product-det", "Two standard results applied directly.",
  check=_c4, values=[50, 20, -50, 10], cognitive="Application",
  numerical=dict(question=r"Let $P$ and $Q$ be square matrices of order $3$ with $|P| = 2$ and $|Q| = 5$. Then the value of $|P^{T} Q^{2}|$ is", answer=50))


def _c5():
    D = Matrix([[1, 2, 1], [4, 6, 1], [-2, 3, 1]]).det()
    return Abs(D) / 2
Q("U03-B-005", "Area of a triangle", "Area from vertices", "Easy", "Single-step computation MCQ",
  r"The area (in square units) of the triangle with vertices $(1, 2)$, $(4, 6)$ and $(-2, 3)$ is",
  r"$\frac{15}{2}$",
  [(r"$15$", r"Omits the factor $\frac{1}{2}$ and reports $|\Delta| = 15$."),
   (r"$\frac{39}{2}$", r"Middle cofactor sign slip: $3 + 12 + 24 = 39$."),
   (r"$\frac{9}{2}$", r"Evaluates the last minor as $(4)(3) - (6)(2) = 0$, dropping the sign of $-2$: $|3 - 12| = 9$.")],
  r"$\Delta = \begin{vmatrix} 1 & 2 & 1 \\ 4 & 6 & 1 \\ -2 & 3 & 1 \end{vmatrix} = 1(6-3) - 2(4+2) + 1(12+12) = 15$, so the area is $\frac{1}{2}|\Delta| = \frac{15}{2}$.",
  r"Forgetting the factor $\frac{1}{2}$ in the area formula.",
  "U03-B-area-basic", "Direct use of the area formula.",
  check=_c5, values=[Rational(15, 2), 15, Rational(39, 2), Rational(9, 2)], cognitive="Application")


def _c6():
    s = solve(Matrix([[1, k, 1], [2, 5, 1], [4, 9, 1]]).det(), k)
    return s[0]
Q("U03-B-006", "Area of a triangle", "Collinearity with one unknown", "Easy", "Inverse/parameter MCQ",
  r"If the points $(1, k)$, $(2, 5)$ and $(4, 9)$ are collinear, then $k$ equals",
  r"$3$",
  [(r"$-3$", r"Sign slip on the middle cofactor: $-4 - 2k - 2 = 0$ gives $k = -3$."),
   (r"$7$", r"Uses the slope $2$ but moves in the wrong direction from $(2, 5)$: $5 + 2 = 7$."),
   (r"$1$", r"Takes the last term as $+2$ instead of $-2$: $-4 + 2k + 2 = 0$.")],
  r"Collinearity means $\begin{vmatrix} 1 & k & 1 \\ 2 & 5 & 1 \\ 4 & 9 & 1 \end{vmatrix} = 0$, i.e. $1(5-9) - k(2-4) + (18-20) = 2k - 6 = 0$, so $k = 3$.",
  "Sign errors in the cofactor expansion of the collinearity determinant.",
  "U03-B-collinear-param", "Single determinant equation, linear in the unknown.",
  check=_c6, values=[3, -3, 7, 1], cognitive="Application")

Q("U03-B-007", "Properties of determinants", "Column operations giving zero", "Easy", "Single-step computation MCQ",
  r"For all real $a, b, c$, the value of $\begin{vmatrix} 1 & a & b+c \\ 1 & b & c+a \\ 1 & c & a+b \end{vmatrix}$ is",
  r"$0$",
  [(r"$abc$", r"Multiplies the second column entries, treating the determinant as a product of entries."),
   (r"$a+b+c$", r"Applies $C_3 \to C_3 + C_2$ and takes out $a+b+c$, then forgets that the remaining determinant has two equal columns."),
   (r"$(a-b)(b-c)(c-a)$", r"Confuses it with the Vandermonde determinant $\begin{vmatrix} 1 & a & a^2 \\ 1 & b & b^2 \\ 1 & c & c^2 \end{vmatrix}$.")],
  r"Apply $C_3 \to C_3 + C_2$: the third column becomes $(a+b+c)(1, 1, 1)^T$. Taking out $a+b+c$ leaves two identical columns, so the determinant is $0$.",
  "Not spotting the column operation that creates identical columns.",
  "U03-B-property-zero", "One column operation and one property.",
  check=lambda: simplify(Matrix([[1, a, b+c], [1, b, c+a], [1, c, a+b]]).det()),
  values=[0, a*b*c, a+b+c, (a-b)*(b-c)*(c-a)], cognitive="Understanding")

p_, q_, r_ = symbols('p q r')
Q("U03-B-008", "Properties of determinants", "Skew-symmetric determinant of odd order", "Easy", "Single-step computation MCQ",
  r"For real numbers $p, q, r$, the value of $\begin{vmatrix} 0 & p & -q \\ -p & 0 & r \\ q & -r & 0 \end{vmatrix}$ is",
  r"$0$",
  [(r"$2pqr$", r"Confuses it with the symmetric determinant $\begin{vmatrix} 0 & p & q \\ p & 0 & r \\ q & r & 0 \end{vmatrix} = 2pqr$."),
   (r"$-2pqr$", r"Sign slip on the symmetric-case value $2pqr$."),
   (r"$pqr$", r"Keeps only one of the two non-zero diagonal products, $p \cdot r \cdot q$.")],
  r"The matrix $M$ satisfies $M^T = -M$, so $|M| = |M^T| = |-M| = (-1)^3|M| = -|M|$, giving $|M| = 0$. Directly: $0 - p(0 - rq) - q(pr - 0) = pqr - pqr = 0$.",
  "Not recognising that a skew-symmetric determinant of odd order vanishes.",
  "U03-B-skew-odd", "One property, or a short expansion.",
  check=lambda: expand(Matrix([[0, p_, -q_], [-p_, 0, r_], [q_, -r_, 0]]).det()),
  values=[0, 2*p_*q_*r_, -2*p_*q_*r_, p_*q_*r_], cognitive="Understanding")


def _c9():
    s = solve(Eq(Matrix([[2*x, 5], [8, x]]).det(), Matrix([[6, -2], [7, 3]]).det()), x)
    return FiniteSet(*s)
Q("U03-B-009", "Determinant equations", "Equation between two second order determinants", "Easy", "Inverse/parameter MCQ",
  r"If $\begin{vmatrix} 2x & 5 \\ 8 & x \end{vmatrix} = \begin{vmatrix} 6 & -2 \\ 7 & 3 \end{vmatrix}$, then $x$ equals",
  r"$\pm 6$",
  [(r"$\pm 6\sqrt{2}$", r"Writes the left side as $x^2 - 40$, dropping the coefficient $2$: $x^2 = 72$."),
   (r"$\pm \sqrt{22}$", r"Evaluates the right side as $18 - 14 = 4$: $2x^2 = 44$."),
   (r"$\pm 3\sqrt{2}$", r"Gets $2x^2 = 72$ but divides by $2$ twice: $x^2 = 18$.")],
  r"$2x^2 - 40 = 18 - (-14) = 32$, so $x^2 = 36$ and $x = \pm 6$.",
  r"Sign of $-(-2)(7)$ on the right side, or the coefficient of $x^2$.",
  "U03-B-deteq-2x2", "One expansion on each side and a quadratic.",
  check=_c9, values=[FiniteSet(6, -6), FiniteSet(6*sqrt(2), -6*sqrt(2)), FiniteSet(sqrt(22), -sqrt(22)), FiniteSet(3*sqrt(2), -3*sqrt(2))],
  cognitive="Application",
  numerical=dict(question=r"If $\begin{vmatrix} 2x & 5 \\ 8 & x \end{vmatrix} = \begin{vmatrix} 6 & -2 \\ 7 & 3 \end{vmatrix}$ and $x > 0$, then the value of $x$ is", answer=6))

Q("U03-B-010", "Properties of determinants", "Evaluation using column operations", "Easy", "Single-step computation MCQ",
  r"The value of $\begin{vmatrix} 23 & 7 & 16 \\ 41 & 9 & 32 \\ 15 & 5 & 11 \end{vmatrix}$ is",
  r"$-80$",
  [(r"$80$", r"After $C_1 \to C_1 - C_2 - C_3$, drops the sign of the entry $-1$ in the first column."),
   (r"$-368$", r"Evaluates the $2 \times 2$ minor as $7 \cdot 32 + 16 \cdot 9 = 368$, adding instead of subtracting."),
   (r"$0$", r"Assumes $C_1 = C_2 + C_3$ in every row, overlooking that $5 + 11 = 16 \ne 15$.")],
  r"$C_1 \to C_1 - C_2 - C_3$ gives the first column $(0, 0, -1)^T$. Expanding along it, the determinant is $(-1)\begin{vmatrix} 7 & 16 \\ 9 & 32 \end{vmatrix} = -(224 - 144) = -80$.",
  "Assuming a pattern holds in every row without checking.",
  "U03-B-property-colop-trap", "One column operation and a $2 \\times 2$ expansion; trap in the last row.",
  check=lambda: Matrix([[23, 7, 16], [41, 9, 32], [15, 5, 11]]).det(), values=[-80, 80, -368, 0],
  cognitive="Application")


def _c11():
    al = symbols('alpha', real=True)
    A = Matrix([[al, 2], [2, al]])
    return FiniteSet(*solve((A**3).det() - 125, al))
Q("U03-B-011", "Properties of determinants", "Determinant of a power", "Easy", "Inverse/parameter MCQ",
  r"If $P = \begin{bmatrix} \alpha & 2 \\ 2 & \alpha \end{bmatrix}$, where $\alpha$ is real, and $|P^3| = 125$, then $\alpha$ equals",
  r"$\pm 3$",
  [(r"$\pm 1$", r"Takes $|P| = \alpha^2 + 4$, adding the off-diagonal product."),
   (r"$\pm \sqrt{129}$", r"Uses $|P^3| = |P|$, setting $\alpha^2 - 4 = 125$."),
   (r"$\pm \sqrt{5}$", r"Drops the off-diagonal product and takes $|P| = \alpha^2 = 5$.")],
  r"$|P^3| = |P|^3 = 125$ gives $|P| = 5$ (the real cube root). So $\alpha^2 - 4 = 5$, $\alpha = \pm 3$.",
  r"Using $|P^n| = |P|^n$ incorrectly or mis-evaluating a $2 \times 2$ determinant.",
  "U03-B-power-det", "Two short steps: power rule, then a quadratic.",
  check=_c11, values=[FiniteSet(3, -3), FiniteSet(1, -1), FiniteSet(sqrt(129), -sqrt(129)), FiniteSet(sqrt(5), -sqrt(5))],
  cognitive="Application")


def _c12():
    M = gen3()
    N = M.copy()
    N.row_swap(0, 1)
    N[2, :] = 2*N[2, :]
    return simplify(N.det() / M.det())
Q("U03-B-012", "Properties of determinants", "Effect of elementary row operations", "Easy", "Direct concept MCQ",
  r"Let $\Delta$ be the value of a determinant of order $3$. A new determinant is formed by interchanging its first and second rows and then multiplying every element of the third row by $2$. The value of the new determinant is",
  r"$-2\Delta$",
  [(r"$2\Delta$", r"Ignores the sign change caused by interchanging two rows."),
   (r"$-8\Delta$", r"Multiplies by $2^3$, as if every element of the determinant were doubled."),
   (r"$8\Delta$", r"Both slips: no sign change and the factor $2^3$.")],
  r"Interchanging two rows multiplies the value by $-1$; multiplying one row by $2$ multiplies it by $2$. The new value is $-2\Delta$.",
  "Confusing scaling one row with scaling the whole matrix, or forgetting the sign from a row swap.",
  "U03-B-row-ops-effect", "Two properties applied in sequence.",
  check=_c12, values=[-2, 2, -8, 8], cognitive="Understanding")


def _c13():
    kk = symbols('kk', real=True)
    D = Matrix([[kk, 0, 1], [4, 0, 1], [0, 2, 1]]).det()
    return FiniteSet(*solve(Abs(D)/2 - 4, kk))
Q("U03-B-013", "Area of a triangle", "Unknown vertex from a given area", "Easy", "Inverse/parameter MCQ",
  r"The area of the triangle with vertices $(k, 0)$, $(4, 0)$ and $(0, 2)$ is $4$ square units. The set of all possible values of $k$ is",
  r"$\{0, 8\}$",
  [(r"$\{8\}$", r"Writes $\Delta = 2k - 8$ with the vertices in the opposite orientation and drops the modulus: $k - 4 = 4$ gives only $k = 8$."),
   (r"$\{2, 6\}$", r"Omits the factor $\frac{1}{2}$: $|8 - 2k| = 4$."),
   (r"$\{-4, 4\}$", r"Takes the base as $|k|$ instead of $|4 - k|$.")],
  r"$\Delta = \begin{vmatrix} k & 0 & 1 \\ 4 & 0 & 1 \\ 0 & 2 & 1 \end{vmatrix} = k(0-2) - 0 + 1(8 - 0) = 8 - 2k$. Area $= \frac{1}{2}|8 - 2k| = |4 - k| = 4$, so $k = 0$ or $k = 8$.",
  "Dropping the modulus in the area formula and losing a solution.",
  "U03-B-area-param", "Area formula with a modulus equation.",
  check=_c13, values=[FiniteSet(0, 8), FiniteSet(8), FiniteSet(2, 6), FiniteSet(-4, 4)], cognitive="Application")

Q("U03-B-014", "Determinants", "Vandermonde type numeric determinant", "Easy", "Single-step computation MCQ",
  r"The value of $\begin{vmatrix} 1 & 1 & 1 \\ 2 & 3 & 5 \\ 4 & 9 & 25 \end{vmatrix}$ is",
  r"$6$",
  [(r"$-6$", r"Uses $(x-y)(y-z)(x-z)$ with the last factor reversed: $(2-3)(3-5)(2-5) = -6$."),
   (r"$30$", r"Multiplies the second-row entries $2 \cdot 3 \cdot 5$."),
   (r"$2$", r"Uses only $(3-2)(5-3)$, missing the factor $(5-2)$.")],
  r"This is $\begin{vmatrix} 1 & 1 & 1 \\ x & y & z \\ x^2 & y^2 & z^2 \end{vmatrix} = (y-x)(z-x)(z-y)$ with $x, y, z = 2, 3, 5$: $(1)(3)(2) = 6$. Direct expansion confirms: $1(75-45) - 1(50-20) + 1(18-12) = 6$.",
  "Sign of the Vandermonde product.",
  "U03-B-vandermonde-numeric", "One known factorisation or a direct expansion.",
  check=lambda: Matrix([[1, 1, 1], [2, 3, 5], [4, 9, 25]]).det(), values=[6, -6, 30, 2], cognitive="Application",
  numerical=dict(question=r"The value of $\begin{vmatrix} 1 & 1 & 1 \\ 2 & 3 & 5 \\ 4 & 9 & 25 \end{vmatrix}$ is", answer=6))


def _c15():
    M = gen3()
    s1 = simplify(M.T.det() - M.det()) == 0
    s2 = simplify((-M).det() - M.det()) == 0
    return (bool(s1), bool(s2))
Q("U03-B-015", "Properties of determinants", "Transpose and negative of a matrix", "Easy", "Statement-based MCQ",
  r"Let $P$ be any square matrix of order $3$. Statement I: $|P^{T}| = |P|$. Statement II: $|-P| = |P|$. In the light of the above statements, choose the correct answer.",
  r"Statement I is true but Statement II is false",
  [(r"Both Statement I and Statement II are true", r"Applies $|kP| = k^2|P|$, valid for order $2$, so $(-1)^2 = 1$."),
   (r"Both Statement I and Statement II are false", r"Believes transposing changes the sign of a determinant (rejects Statement I) and correctly uses $(-1)^3 = -1$ (rejects Statement II)."),
   (r"Statement I is false but Statement II is true", r"Believes transposing changes the sign of a determinant (rejects Statement I) and uses $(-1)^2 = 1$ for the scalar factor (accepts Statement II).")],
  r"Transposing does not change a determinant, so Statement I is true. For order $3$, $|-P| = (-1)^3|P| = -|P|$, which differs from $|P|$ whenever $|P| \ne 0$, so Statement II is false.",
  r"Using $(-1)^2$ instead of $(-1)^3$ for a matrix of order $3$.",
  "U03-B-statement-basic-props", "Two basic properties checked.",
  check=_c15, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding")

Q("U03-B-016", "Properties of determinants", "Evaluation of a patterned determinant", "Easy", "Single-step computation MCQ",
  r"The value of $\begin{vmatrix} x+1 & x & x \\ x & x+1 & x \\ x & x & x+1 \end{vmatrix}$ is",
  r"$3x+1$",
  [(r"$(x+1)^3$", r"Treats the determinant as triangular and multiplies the diagonal entries."),
   (r"$1$", r"Splits it as $|I| + |xJ|$ where $J$ is the all-ones matrix, assuming determinants add."),
   (r"$3x-1$", r"Sign slip after $C_1 \to C_1 + C_2 + C_3$: writes the common factor as $3x - 1$.")],
  r"$C_1 \to C_1 + C_2 + C_3$ makes every first-column entry $3x+1$; take it out. Then $R_2 \to R_2 - R_1$, $R_3 \to R_3 - R_1$ give $\begin{vmatrix} 1 & x & x \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{vmatrix} = 1$. Value $= 3x+1$.",
  "Treating determinants as additive or reading the diagonal as if triangular.",
  "U03-B-eval-symmetric-pattern", "Standard sum-of-columns trick in two operations.",
  check=lambda: expand(Matrix([[x+1, x, x], [x, x+1, x], [x, x, x+1]]).det()),
  values=[3*x+1, (x+1)**3, 1, 3*x-1], cognitive="Application")

Q("U03-B-017", "Determinants", "Second order determinant with logarithms", "Easy", "Single-step computation MCQ",
  r"The value of $\begin{vmatrix} \log_2 8 & \log_3 9 \\ \log_2 4 & \log_3 27 \end{vmatrix}$ is",
  r"$5$",
  [(r"$13$", r"Adds the two products: $9 + 4$."),
   (r"$-5$", r"Computes $bc - ad = 4 - 9$."),
   (r"$9$", r"Keeps only the leading diagonal product $3 \times 3$.")],
  r"$\log_2 8 = 3$, $\log_3 9 = 2$, $\log_2 4 = 2$, $\log_3 27 = 3$. The determinant is $3 \cdot 3 - 2 \cdot 2 = 5$.",
  r"Order of subtraction in $ad - bc$.",
  "U03-B-eval2-log", "Evaluate four logarithms and one $2 \\times 2$ determinant.",
  check=lambda: simplify(Matrix([[log(8, 2), log(9, 3)], [log(4, 2), log(27, 3)]]).det()),
  values=[5, 13, -5, 9], cognitive="Application")

# ---------------------------------------------------------------- MEDIUM

Q("U03-B-018", "Factorised determinants", "Vandermonde type with cubes", "Medium", "Multi-step computation MCQ",
  r"The determinant $\begin{vmatrix} 1 & 1 & 1 \\ a & b & c \\ a^3 & b^3 & c^3 \end{vmatrix}$ equals",
  r"$(a-b)(b-c)(c-a)(a+b+c)$",
  [(r"$(a-b)(b-c)(c-a)(ab+bc+ca)$", r"Removes $(b-a)(c-a)$ correctly but factorises the remaining $2 \times 2$ determinant wrongly, getting $ab+bc+ca$ as the symmetric factor instead of $a+b+c$."),
   (r"$(a-b)(b-c)(c-a)(a^2+b^2+c^2)$", r"Assumes the extra factor is the sum of squares by analogy with the cube power."),
   (r"$(b-a)(b-c)(c-a)(a+b+c)$", r"Correct factors but one sign reversed while pulling out $(b-a)$.")],
  r"$C_2 \to C_2 - C_1$, $C_3 \to C_3 - C_1$ and take out $(b-a)(c-a)$, leaving $\begin{vmatrix} 1 & 1 \\ a^2+ab+b^2 & a^2+ac+c^2 \end{vmatrix} = (c-b)(a+b+c)$. So the value is $(b-a)(c-a)(c-b)(a+b+c) = (a-b)(b-c)(c-a)(a+b+c)$.",
  "Losing a sign in the product of differences, or misidentifying the symmetric factor.",
  "U03-B-vandermonde-sym", "Two column operations, two factorisations and sign bookkeeping.",
  check=lambda: factor(Matrix([[1, 1, 1], [a, b, c], [a**3, b**3, c**3]]).det()),
  values=[(a-b)*(b-c)*(c-a)*(a+b+c), (a-b)*(b-c)*(c-a)*(a*b+b*c+c*a), (a-b)*(b-c)*(c-a)*(a**2+b**2+c**2), (b-a)*(b-c)*(c-a)*(a+b+c)],
  cognitive="Analysis")


def _c19():
    rts = Poly(x**3 - 2*x**2 + 3*x - 1, x).all_roots()
    A1, B1, C1 = rts
    return N(Matrix([[A1, B1, C1], [B1, C1, A1], [C1, A1, B1]]).det(), 40)
Q("U03-B-019", "Factorised determinants", "Circulant determinant with roots of a cubic", "Medium", "Multi-step computation MCQ",
  r"If $\alpha, \beta, \gamma$ are the roots of $x^3 - 2x^2 + 3x - 1 = 0$, then $\begin{vmatrix} \alpha & \beta & \gamma \\ \beta & \gamma & \alpha \\ \gamma & \alpha & \beta \end{vmatrix}$ equals",
  r"$10$",
  [(r"$-10$", r"Takes the determinant as $+(\alpha^3 + \beta^3 + \gamma^3 - 3\alpha\beta\gamma)$, missing the minus sign."),
   (r"$-2$", r"Uses $\alpha^2+\beta^2+\gamma^2 = (\alpha+\beta+\gamma)^2 = 4$, forgetting $-2\sum\alpha\beta$: $-(2)(4 - 3) = -2$."),
   (r"$-26$", r"Takes $\sum\alpha\beta = -3$: $\sum\alpha^2 = 10$, so $-(2)(10 + 3) = -26$.")],
  r"$C_1 \to C_1 + C_2 + C_3$ shows the determinant equals $-(\alpha^3+\beta^3+\gamma^3 - 3\alpha\beta\gamma) = -(\alpha+\beta+\gamma)\left[(\alpha+\beta+\gamma)^2 - 3\sum\alpha\beta\right]$. With $\sum\alpha = 2$, $\sum\alpha\beta = 3$: $-(2)(4 - 9) = 10$.",
  "Sign of the circulant determinant and Vieta sums.",
  "U03-B-circulant-roots", "Circulant identity combined with Vieta relations.",
  check=_c19, values=[10, -10, -2, -26], cognitive="Application",
  numerical=dict(question=r"If $\alpha, \beta, \gamma$ are the roots of $x^3 - 2x^2 + 3x - 1 = 0$, then the value of $\begin{vmatrix} \alpha & \beta & \gamma \\ \beta & \gamma & \alpha \\ \gamma & \alpha & \beta \end{vmatrix}$ is", answer=10))


def _c20():
    A = diag(-2, 1, 1)
    return (3*A.T*A**2).det()
Q("U03-B-020", "Properties of determinants", "Combining scalar, transpose and power rules", "Medium", "Multi-step computation MCQ",
  r"Let $P$ be a square matrix of order $3$ with $|P| = -2$. Then $|3P^{T}P^{2}|$ equals",
  r"$-216$",
  [(r"$-24$", r"Takes the scalar $3$ out only once: $3|P|^3 = -24$."),
   (r"$-72$", r"Uses $3^2$ instead of $3^3$: $9 \times (-8)$."),
   (r"$216$", r"Takes $|P^T| = -|P| = 2$: $27 \times 2 \times 4$.")],
  r"$|3P^TP^2| = 3^3\,|P^T|\,|P|^2 = 27|P|^3 = 27 \times (-8) = -216$.",
  r"$|kP| = k^n|P|$ and $|P^T| = |P|$ used together.",
  "U03-B-kA-combo", "Three determinant rules combined.",
  check=_c20, values=[-216, -24, -72, 216], cognitive="Application")


def _c21():
    A = Matrix([[1, 2], [3, 4], [5, 6]]); B = Matrix([[2, 1, 0], [1, 3, 1]])
    return (A*B).det()
Q("U03-B-021", "Properties of determinants", "Product of non-square matrices", "Medium", "Conceptual/application MCQ",
  r"Let $P = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}$ and $Q = \begin{bmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \end{bmatrix}$. Then $|PQ|$ equals",
  r"$0$",
  [(r"$-20$", r"Computes $|QP|$, the $2 \times 2$ product, instead of $|PQ|$."),
   (r"$-10$", r"Multiplies $\begin{vmatrix} 1 & 2 \\ 3 & 4 \end{vmatrix} = -2$ by $\begin{vmatrix} 2 & 1 \\ 1 & 3 \end{vmatrix} = 5$, as if $|PQ| = |P||Q|$ applied to leading blocks."),
   (r"$20$", r"Computes $|QP|$ and also reverses the subtraction.")],
  r"Pad with zeros to get square factors: $PQ = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 4 & 0 \\ 5 & 6 & 0 \end{bmatrix}\begin{bmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 0 & 0 \end{bmatrix}$, since the zero column and zero row add nothing to any entry. Both factors are $3 \times 3$, so $|PQ| = 0 \times 0 = 0$, as each factor has a zero column or row. (Directly, $PQ = \begin{bmatrix} 4 & 7 & 2 \\ 10 & 15 & 4 \\ 16 & 23 & 6 \end{bmatrix}$, whose determinant is $0$. Note $|QP| = \begin{vmatrix} 5 & 8 \\ 15 & 20 \end{vmatrix} = -20$, which is different.)",
  r"Assuming $|PQ| = |QP|$ or a product rule for non-square matrices.",
  "U03-B-nonsquare-product", r"Requires writing $PQ$ as a product of square matrices with a zero column or row; trap value $|QP|$.",
  check=_c21, values=[0, -20, -10, 20], cognitive="Analysis")


def _c22():
    s = solve(Matrix([[x, 3, 7], [2, x, 2], [7, 6, x]]).det(), x)
    assert -9 in s
    others = [v for v in s if v != -9]
    return others[0]*others[1]
Q("U03-B-022", "Determinant equations", "Cubic determinant equation with one root given", "Medium", "Multi-step computation MCQ",
  r"One root of $\begin{vmatrix} x & 3 & 7 \\ 2 & x & 2 \\ 7 & 6 & x \end{vmatrix} = 0$ is $x = -9$. The product of the other two roots is",
  r"$14$",
  [(r"$-14$", r"Takes the product of all three roots as $+126$ (sign of the constant term)."),
   (r"$-126$", r"Reports the product of all three roots."),
   (r"$9$", r"Gives the sum of the other two roots instead of their product.")],
  r"Expanding: $x(x^2 - 12) - 3(2x - 14) + 7(12 - 7x) = x^3 - 67x + 126$. The product of all roots is $-126$, so the other two have product $\frac{-126}{-9} = 14$ (they are $2$ and $7$).",
  "Vieta sign conventions for a cubic.",
  "U03-B-deteq-cubic", "Expansion to a cubic followed by Vieta.",
  check=_c22, values=[14, -14, -126, 9], cognitive="Application",
  numerical=dict(question=r"One root of $\begin{vmatrix} x & 3 & 7 \\ 2 & x & 2 \\ 7 & 6 & x \end{vmatrix} = 0$ is $x = -9$. The product of the other two roots is", answer=14))

Q("U03-B-023", "Determinant equations", "Equation with a common-pattern determinant", "Medium", "Multi-step computation MCQ",
  r"The set of all real $x$ satisfying $\begin{vmatrix} x+1 & 2 & 3 \\ 1 & x+2 & 3 \\ 1 & 2 & x+3 \end{vmatrix} = 0$ is",
  r"$\{0, -6\}$",
  [(r"$\{-6\}$", r"Cancels the factor $x^2$ as if it were non-zero."),
   (r"$\{0, 6\}$", r"Sign slip in the factor: writes $x - 6$ for $x + 6$."),
   (r"$\{-1, -2, -3\}$", r"Sets each diagonal entry equal to zero.")],
  r"$C_1 \to C_1 + C_2 + C_3$ gives a first column of $x+6$; take it out. Then $R_2 - R_1$, $R_3 - R_1$ give $\begin{vmatrix} 1 & 2 & 3 \\ 0 & x & 0 \\ 0 & 0 & x \end{vmatrix} = x^2$. So the equation is $x^2(x+6) = 0$, giving $x \in \{0, -6\}$.",
  "Dividing by a factor that can be zero.",
  "U03-B-deteq-pattern", "Two operations plus care with a repeated root.",
  check=lambda: solveset(Matrix([[x+1, 2, 3], [1, x+2, 3], [1, 2, x+3]]).det(), x, S.Reals),
  values=[FiniteSet(0, -6), FiniteSet(-6), FiniteSet(0, 6), FiniteSet(-1, -2, -3)], cognitive="Application")


def _c24():
    D = Matrix([[sin(x), cos(x), cos(x)], [cos(x), sin(x), cos(x)], [cos(x), cos(x), sin(x)]]).det()
    s = solveset(D, x, Interval(-pi/2, pi/4))
    return len(s)
Q("U03-B-024", "Determinant equations", "Trigonometric determinant equation on an interval", "Medium", "Multi-step computation MCQ",
  r"The number of distinct real $x$ in $\left[-\frac{\pi}{2}, \frac{\pi}{4}\right]$ satisfying $\begin{vmatrix} \sin x & \cos x & \cos x \\ \cos x & \sin x & \cos x \\ \cos x & \cos x & \sin x \end{vmatrix} = 0$ is",
  r"$2$",
  [(r"$1$", r"Keeps only $\tan x = 1$ and misses $\tan x = -2$, which has a root $x = -\tan^{-1}2$ in the interval."),
   (r"$3$", r"Counts $x = \frac{\pi}{4}$ twice because of the squared factor $(\sin x - \cos x)^2$."),
   (r"$4$", r"Solves $\tan x = 1$ and $\tan x = -2$ over a whole period, $x = \frac{\pi}{4}, -\frac{3\pi}{4}, -\tan^{-1}2, \pi - \tan^{-1}2$, ignoring the interval.")],
  r"$C_1 \to C_1 + C_2 + C_3$ takes out $\sin x + 2\cos x$; then subtracting rows leaves $(\sin x - \cos x)^2$. So $(\sin x + 2\cos x)(\sin x - \cos x)^2 = 0$, i.e. $\tan x = -2$ or $\tan x = 1$ ($\cos x = 0$ is not a solution). In $\left[-\frac{\pi}{2}, \frac{\pi}{4}\right]$ these give $x = -\tan^{-1}2$ and $x = \frac{\pi}{4}$: two values.",
  "Ignoring a factor or the interval when counting roots.",
  "U03-B-deteq-trig", "Factorisation, two trigonometric equations and interval counting.",
  check=_c24, values=[2, 1, 3, 4], cognitive="Analysis",
  numerical=dict(question=r"The number of distinct real $x$ in $\left[-\frac{\pi}{2}, \frac{\pi}{4}\right]$ satisfying $\begin{vmatrix} \sin x & \cos x & \cos x \\ \cos x & \sin x & \cos x \\ \cos x & \cos x & \sin x \end{vmatrix} = 0$ is", answer=2))


def _c25():
    D = Matrix([[2, -6, 1], [5, 4, 1], [k, 4, 1]]).det()
    s = solve(Abs(D)/2 - 35, k)
    return s[0]*s[1]
Q("U03-B-025", "Area of a triangle", "Unknown vertex from a given area", "Medium", "Inverse/parameter MCQ",
  r"The triangle with vertices $(2, -6)$, $(5, 4)$ and $(k, 4)$ has area $35$ square units. The product of all possible values of $k$ is",
  r"$-24$",
  [(r"$\frac{51}{4}$", r"Omits the factor $\frac{1}{2}$: $|50 - 10k| = 35$ gives $k = \frac{17}{2}, \frac{3}{2}$."),
   (r"$12$", r"Drops the modulus and keeps only $k = 12$."),
   (r"$24$", r"Drops the minus sign of the root $k = -2$ before multiplying.")],
  r"$\Delta = 2(4-4) + 6(5-k) + (20-4k) = 50 - 10k$. Area $= \frac{1}{2}|50 - 10k| = 35$, so $50 - 10k = \pm 70$, giving $k = -2$ or $k = 12$. Product $= -24$.",
  "Dropping the modulus or the factor one-half.",
  "U03-B-area-param", "Area determinant, modulus equation with two cases.",
  check=_c25, values=[-24, Rational(51, 4), 12, 24], cognitive="Application")


def _c26():
    s = solve(Matrix([[k, 1, 1], [-3, k, 1], [-1, 4, 1]]).det(), k)
    return sum(v**2 for v in s)
Q("U03-B-026", "Area of a triangle", "Collinearity leading to a quadratic", "Medium", "Inverse/parameter MCQ",
  r"The points $(k, 1)$, $(-3, k)$ and $(-1, 4)$ are collinear. The sum of the squares of all real values of $k$ is",
  r"$29$",
  [(r"$9$", r"Squares the sum of the roots, $(5 - 2)^2$, instead of summing their squares."),
   (r"$37$", r"Middle cofactor sign slip gives $k^2 - 3k - 14 = 0$; then $9 + 28 = 37$."),
   (r"$19$", r"Uses $\alpha^2 + \beta^2 = (\alpha+\beta)^2 - \alpha\beta = 9 + 10$.")],
  r"$\begin{vmatrix} k & 1 & 1 \\ -3 & k & 1 \\ -1 & 4 & 1 \end{vmatrix} = k(k-4) - 1(-3+1) + (-12+k) = k^2 - 3k - 10 = 0$, so $k = 5$ or $k = -2$. Sum of squares $= 25 + 4 = 29$.",
  "Sign slips in the determinant or the identity for a sum of squares.",
  "U03-B-collinear-param", "Collinearity determinant producing a quadratic, then Vieta.",
  check=_c26, values=[29, 9, 37, 19], cognitive="Application",
  numerical=dict(question=r"The points $(k, 1)$, $(-3, k)$ and $(-1, 4)$ are collinear. The sum of the squares of all real values of $k$ is", answer=29))


def _c27():
    P, Q_, R, X, Y, Z = symbols('P Q R X Y Z')
    M1 = Matrix([[b+c, c+a, a+b], [Q_+R, R+P, P+Q_], [Y+Z, Z+X, X+Y]])
    M2 = Matrix([[a, b, c], [P, Q_, R], [X, Y, Z]])
    return simplify(M1.det()/M2.det()) * 5
Q("U03-B-027", "Properties of determinants", "Splitting a determinant with sums", "Medium", "Multi-step computation MCQ",
  r"If $\begin{vmatrix} a & b & c \\ p & q & r \\ x & y & z \end{vmatrix} = 5$, then $\begin{vmatrix} b+c & c+a & a+b \\ q+r & r+p & p+q \\ y+z & z+x & x+y \end{vmatrix}$ equals",
  r"$10$",
  [(r"$5$", r"Uses column operations but loses the factor $2$ taken out of the column sum."),
   (r"$40$", r"Splits each column into two and counts all $8$ pieces as $5$, ignoring that six of them vanish and one has a sign."),
   (r"$-10$", r"Gets the factor $2$ but takes $-1$ out of only one of the two negated columns.")],
  r"$C_1 \to C_1 + C_2 + C_3$ makes the first column $2(a+b+c, p+q+r, x+y+z)^T$; take out $2$. Now $C_2 \to C_2 - C_1$ and $C_3 \to C_3 - C_1$ turn the other columns into $(-b, -q, -y)^T$ and $(-c, -r, -z)^T$, and then $C_1 \to C_1 + C_2 + C_3$ turns the first column into $(a, p, x)^T$. So the value is $2\begin{vmatrix} a & -b & -c \\ p & -q & -r \\ x & -y & -z \end{vmatrix} = 2(-1)^2(5) = 10$.",
  "Mishandling the factor 2 or the sign of column permutations.",
  "U03-B-property-split", "Three column operations with factor tracking.",
  check=_c27, values=[10, 5, 40, -10], cognitive="Application",
  numerical=dict(question=r"If $\begin{vmatrix} a & b & c \\ p & q & r \\ x & y & z \end{vmatrix} = 5$, then the value of $\begin{vmatrix} b+c & c+a & a+b \\ q+r & r+p & p+q \\ y+z & z+x & x+y \end{vmatrix}$ is", answer=10))


def _c28():
    rts = Poly(x**3 - 4*x**2 + 5*x - 3, x).all_roots()
    A1, B1, C1 = rts
    return N(Matrix([[1+A1, 1, 1], [1, 1+B1, 1], [1, 1, 1+C1]]).det(), 40)
Q("U03-B-028", "Properties of determinants", "Determinant of the form 1 plus a diagonal, with Vieta", "Medium", "Multi-step computation MCQ",
  r"If $\alpha, \beta, \gamma$ are the roots of $x^3 - 4x^2 + 5x - 3 = 0$, then $\begin{vmatrix} 1+\alpha & 1 & 1 \\ 1 & 1+\beta & 1 \\ 1 & 1 & 1+\gamma \end{vmatrix}$ equals",
  r"$8$",
  [(r"$3$", r"Keeps only the product term $\alpha\beta\gamma$."),
   (r"$12$", r"Also adds $\alpha+\beta+\gamma = 4$, writing the value as $\alpha\beta\gamma + \sum\alpha\beta + \sum\alpha$."),
   (r"$2$", r"Takes $\alpha\beta\gamma = -3$ (sign of the constant term): $-3 + 5$.")],
  r"Expanding, the determinant equals $\alpha\beta\gamma + \alpha\beta + \beta\gamma + \gamma\alpha$ (the linear terms cancel). By Vieta, $\alpha\beta\gamma = 3$ and $\sum\alpha\beta = 5$, so the value is $8$.",
  "Vieta signs, or assuming the linear terms survive.",
  "U03-B-eval-1plus-pattern", "Known expansion combined with Vieta.",
  check=_c28, values=[8, 3, 12, 2], cognitive="Application",
  numerical=dict(question=r"If $\alpha, \beta, \gamma$ are the roots of $x^3 - 4x^2 + 5x - 3 = 0$, then the value of $\begin{vmatrix} 1+\alpha & 1 & 1 \\ 1 & 1+\beta & 1 \\ 1 & 1 & 1+\gamma \end{vmatrix}$ is", answer=8))


def _c29():
    M = Matrix([[x**2+1, x-2, x+3], [x+1, 2*x, x-4], [x-3, x+4, 3*x+2]])
    return Poly(expand(M.det()), x).coeff_monomial(1)
Q("U03-B-029", "Determinants", "Constant term of a polynomial determinant", "Medium", "Multi-step computation MCQ",
  r"If $\begin{vmatrix} x^2+1 & x-2 & x+3 \\ x+1 & 2x & x-4 \\ x-3 & x+4 & 3x+2 \end{vmatrix} = ax^4 + bx^3 + cx^2 + dx + e$ for all real $x$, then $e$ equals",
  r"$8$",
  [(r"$0$", r"Assumes, as in a familiar problem, that the matrix at $x = 0$ is skew-symmetric; here the diagonal is $1, 0, 2$."),
   (r"$48$", r"At $x = 0$, uses $+a_{12}M_{12}$: $16 + 20 + 12$."),
   (r"$-16$", r"At $x = 0$, takes the third term with the wrong sign: $16 - 20 - 12$.")],
  r"Put $x = 0$: $e = \begin{vmatrix} 1 & -2 & 3 \\ 1 & 0 & -4 \\ -3 & 4 & 2 \end{vmatrix} = 1(0+16) + 2(2-12) + 3(4-0) = 16 - 20 + 12 = 8$.",
  r"Not using the substitution $x = 0$, or assuming the answer from a similar looking problem.",
  "U03-B-poly-constant-term", "Recognise the substitution, then evaluate carefully.",
  check=_c29, values=[8, 0, 48, -16], cognitive="Application",
  numerical=dict(question=r"If $\begin{vmatrix} x^2+1 & x-2 & x+3 \\ x+1 & 2x & x-4 \\ x-3 & x+4 & 3x+2 \end{vmatrix} = ax^4 + bx^3 + cx^2 + dx + e$ for all real $x$, then the value of $e$ is", answer=8))


def _c30():
    M = Matrix([[1, 1, 1], [1, -1-w**2, w**2], [1, w**2, w**4]])
    return N(M.det(), 40)
Q("U03-B-030", "Determinants", "Determinant with cube roots of unity", "Medium", "Multi-step computation MCQ",
  r"If $\omega \ne 1$ is a cube root of unity, then $\begin{vmatrix} 1 & 1 & 1 \\ 1 & -1-\omega^2 & \omega^2 \\ 1 & \omega^2 & \omega^4 \end{vmatrix}$ equals",
  r"$3\omega(\omega - 1)$",
  [(r"$3\omega(1 - \omega)$", r"Correct method but one sign lost when expanding $\omega^2 - \omega$ terms."),
   (r"$0$", r"Assumes a row sum $1 + \omega + \omega^2 = 0$ forces the determinant to vanish."),
   (r"$3\omega^2$", r"Keeps $3\omega^2$ from $3\omega^2 - 3\omega$ and drops the $-3\omega$ term.")],
  r"Since $-1-\omega^2 = \omega$ and $\omega^4 = \omega$, the determinant is $\begin{vmatrix} 1 & 1 & 1 \\ 1 & \omega & \omega^2 \\ 1 & \omega^2 & \omega \end{vmatrix} = 1(\omega^2 - \omega^4) - 1(\omega - \omega^2) + 1(\omega^2 - \omega) = 3(\omega^2 - \omega) = 3\omega(\omega - 1)$.",
  "Simplifying powers of omega and sign handling.",
  "U03-B-omega-det", "Reduction with omega identities followed by expansion.",
  check=_c30, values=[N(3*w*(w-1), 40), N(3*w*(1-w), 40), 0, N(3*w**2, 40)], cognitive="Application")


def _c31():
    D = simplify(Matrix([[1, 1, 1], [1, 1+sin(th), 1], [1, 1, 1+cos(th)]]).det())
    return maximum(D, th, Interval(0, 2*pi))
Q("U03-B-031", "Determinants", "Maximum value of a trigonometric determinant", "Medium", "Multi-step computation MCQ",
  r"The maximum value of $\begin{vmatrix} 1 & 1 & 1 \\ 1 & 1+\sin\theta & 1 \\ 1 & 1 & 1+\cos\theta \end{vmatrix}$, as $\theta$ varies over real numbers, is",
  r"$\frac{1}{2}$",
  [(r"$1$", r"Takes the maximum of $\sin\theta\cos\theta$ as $1$."),
   (r"$\sqrt{2}$", r"Evaluates the determinant as $\sin\theta + \cos\theta$."),
   (r"$\frac{3}{2}$", r"Writes the value as $1 + \sin\theta\cos\theta$, keeping a $1$ that cancels.")],
  r"$R_2 \to R_2 - R_1$, $R_3 \to R_3 - R_1$ give $\begin{vmatrix} 1 & 1 & 1 \\ 0 & \sin\theta & 0 \\ 0 & 0 & \cos\theta \end{vmatrix} = \sin\theta\cos\theta = \frac{1}{2}\sin 2\theta$, whose maximum is $\frac{1}{2}$.",
  r"Maximum of $\sin\theta\cos\theta$.",
  "U03-B-trig-extremum", "Row reduction then a trigonometric maximum.",
  check=_c31, values=[Rational(1, 2), 1, sqrt(2), Rational(3, 2)], cognitive="Application")

Q("U03-B-032", "Determinants", "Determinant independent of a parameter", "Medium", "Multi-step computation MCQ",
  r"For real $x$ and $\theta$, the determinant $\begin{vmatrix} x & \sin\theta & \cos\theta \\ -\sin\theta & -x & 1 \\ \cos\theta & 1 & x \end{vmatrix}$ equals",
  r"$-x^3$",
  [(r"$x^3$", r"Uses the cofactor sign pattern $-, +, -$ along the first row, which negates the whole result."),
   (r"$-x^3 - x$", r"Omits the contribution $x\sin^2\theta + x\cos^2\theta = x$ from the second and third terms."),
   (r"$-x^3 + x$", r"Counts $x(\sin^2\theta + \cos^2\theta)$ twice.")],
  r"Expanding along the first row: $x(-x^2 - 1) - \sin\theta(-x\sin\theta - \cos\theta) + \cos\theta(-\sin\theta + x\cos\theta) = -x^3 - x + x\sin^2\theta + \sin\theta\cos\theta - \sin\theta\cos\theta + x\cos^2\theta = -x^3$.",
  "Sign bookkeeping in a symbolic expansion.",
  "U03-B-independent-param", "Full symbolic expansion with cancellations.",
  check=lambda: simplify(Matrix([[x, sin(th), cos(th)], [-sin(th), -x, 1], [cos(th), 1, x]]).det()),
  values=[-x**3, x**3, -x**3 - x, -x**3 + x], cognitive="Application")


def _c33():
    A = Matrix([[2, 1], [1, 3]]); B = Matrix([[1, -1], [2, 1]])
    return (A + B).det()
Q("U03-B-033", "Properties of determinants", "Determinant of a sum", "Medium", "Conceptual/application MCQ",
  r"Let $P = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}$ and $Q = \begin{bmatrix} 1 & -1 \\ 2 & 1 \end{bmatrix}$. Then $|P + Q|$ equals",
  r"$12$",
  [(r"$8$", r"Assumes $|P+Q| = |P| + |Q| = 5 + 3$."),
   (r"$15$", r"Uses the product rule $|P||Q|$ for a sum."),
   (r"$-12$", r"Computes $bc - ad$ for $P + Q$.")],
  r"$P + Q = \begin{bmatrix} 3 & 0 \\ 3 & 4 \end{bmatrix}$, so $|P+Q| = 12 - 0 = 12$. Note $|P| + |Q| = 8 \ne 12$: determinants are not additive.",
  "Treating the determinant as additive.",
  "U03-B-sum-trap", "Trap: additivity is false; the computation itself is short.",
  check=_c33, values=[12, 8, 15, -12], cognitive="Understanding")


def _c34():
    A = diag(3, 1, 1)
    s1 = (-2*A).det() == 24
    s2 = (A.T*A).det() == 9
    return (bool(s1), bool(s2))
Q("U03-B-034", "Properties of determinants", "Scalar multiple and product with transpose", "Medium", "Statement-based MCQ",
  r"Let $P$ be a square matrix of order $3$ with $|P| = 3$. Statement I: $|-2P| = 24$. Statement II: $|P^{T}P| = 9$. In the light of the above statements, choose the correct answer.",
  r"Statement I is false but Statement II is true",
  [(r"Both Statement I and Statement II are true", r"Uses $(-2)^3 = 8$, losing the sign, so $|-2P|$ seems to be $24$."),
   (r"Both Statement I and Statement II are false", r"Evaluates $|-2P| = -24$ correctly but thinks $|P^T| = -|P|$, giving $|P^TP| = -9$."),
   (r"Statement I is true but Statement II is false", r"Both slips above together.")],
  r"$|-2P| = (-2)^3|P| = -8 \times 3 = -24$, so Statement I is false. $|P^TP| = |P^T||P| = 3 \times 3 = 9$, so Statement II is true.",
  r"Sign of $(-2)^3$.",
  "U03-B-statement-kA", "Two rules with a sign trap.",
  check=_c34, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Understanding")


def _c35():
    D1 = Matrix([[log(32, 3), log(3, 4)], [log(4, 3), log(9, 4)]]).det()
    D2 = Matrix([[log(3, 2), log(3, 4)], [log(8, 3), log(4, 3)]]).det()
    return nsimplify(N(D1*D2, 50), rational=True)
Q("U03-B-035", "Determinants", "Product of determinants with logarithmic entries", "Medium", "Multi-step computation MCQ",
  r"The value of $\begin{vmatrix} \log_3 32 & \log_4 3 \\ \log_3 4 & \log_4 9 \end{vmatrix} \times \begin{vmatrix} \log_2 3 & \log_4 3 \\ \log_3 8 & \log_3 4 \end{vmatrix}$ is",
  r"$2$",
  [(r"$-4$", r"Takes $\log_4 3 = 2\log_2 3$ (inverts the change of base): the factors become $1$ and $-4$."),
   (r"$\frac{9}{2}$", r"Takes $\log_4 9 = 2\log_2 3$: the first factor becomes $10 - 1 = 9$."),
   (r"$-2$", r"Evaluates the second determinant as $bc - ad = -\frac{1}{2}$.")],
  r"Using $\log_4 3 = \frac{1}{2}\log_2 3$, $\log_4 9 = \log_2 3$ and $\log_2 3 \cdot \log_3 2 = 1$: the first determinant is $5\log_3 2 \cdot \log_2 3 - \frac{1}{2}\log_2 3 \cdot 2\log_3 2 = 5 - 1 = 4$; the second is $\log_2 3 \cdot 2\log_3 2 - \frac{1}{2}\log_2 3 \cdot 3\log_3 2 = 2 - \frac{3}{2} = \frac{1}{2}$. Product $= 2$.",
  "Change of base for logarithms with base 4.",
  "U03-B-log-det-product", "Several change-of-base steps across two determinants.",
  check=_c35, values=[2, -4, Rational(9, 2), -2], cognitive="Application")


def _c36():
    A = Matrix([[2, 1, 0], [0, 2, 1], [0, 0, 1]])
    assert A.det() == 4
    B = A.copy(); B.row_swap(0, 2)
    B[1, :] = 3*B[1, :] + B[0, :]
    return B.det()
Q("U03-B-036", "Properties of determinants", "Sequence of row operations", "Medium", "Multi-step computation MCQ",
  r"Let $P$ be a square matrix of order $3$ with $|P| = 4$. A matrix $Q$ is obtained from $P$ by first interchanging the first and third rows, and then applying $R_2 \to 3R_2 + R_1$. Then $|Q|$ equals",
  r"$-12$",
  [(r"$-4$", r"Treats $R_2 \to 3R_2 + R_1$ like $R_2 \to R_2 + 3R_1$, which leaves the value unchanged."),
   (r"$12$", r"Forgets the sign change from the row interchange."),
   (r"$4$", r"Makes both slips: no sign change and no factor $3$.")],
  r"The interchange multiplies the determinant by $-1$, giving $-4$. The operation $R_2 \to 3R_2 + R_1$ scales $R_2$ by $3$ and adds a multiple of another row, so it multiplies the value by $3$: $|Q| = -12$.",
  r"Confusing $R_i \to kR_i + R_j$ with $R_i \to R_i + kR_j$.",
  "U03-B-row-ops-effect", "Two operations, one of which is a subtle scaling.",
  check=_c36, values=[-12, -4, 12, 4], cognitive="Analysis")


def _c37():
    D = Matrix([[-1, 1, 1], [2, 4, 1], [4, 16, 1]]).det()
    return Abs(D)/2
Q("U03-B-037", "Area of a triangle", "Triangle with vertices on a parabola", "Medium", "Multi-step computation MCQ",
  r"The area (in square units) of the triangle whose vertices are the points of the parabola $y = x^2$ with $x = -1$, $x = 2$ and $x = 4$ is",
  r"$15$",
  [(r"$30$", r"Omits the factor $\frac{1}{2}$."),
   (r"$13$", r"Middle cofactor sign slip: $12 - 2 + 16 = 26$."),
   (r"$9$", r"Uses $\frac{1}{2}|(x_1 - x_2)(x_2 - x_3)(x_3 - x_1)|$ but takes $4 - (-1)$ as $3$.")],
  r"The vertices are $(-1, 1)$, $(2, 4)$, $(4, 16)$. $\Delta = -1(4 - 16) - 1(2 - 4) + 1(32 - 16) = 12 + 2 + 16 = 30$, so the area is $15$. Equivalently $\frac{1}{2}|(-1-2)(2-4)(4+1)| = 15$.",
  r"Forgetting the factor one-half, or sign slips with negative coordinates.",
  "U03-B-area-parabola", "Find vertices, then evaluate the area determinant.",
  check=_c37, values=[15, 30, 13, 9], cognitive="Application",
  numerical=dict(question=r"The area (in square units) of the triangle whose vertices are the points of the parabola $y = x^2$ with $x = -1$, $x = 2$ and $x = 4$ is", answer=15))


def _c38():
    P = (1, 1); Qp = (5, 2); R = (6, 6); S_ = (2, 6)
    def tri(u, v, z):
        return Abs(Matrix([[u[0], u[1], 1], [v[0], v[1], 1], [z[0], z[1], 1]]).det())/2
    return tri(P, Qp, R) + tri(P, R, S_)
Q("U03-B-038", "Area of a triangle", "Area of a quadrilateral by splitting into triangles", "Medium", "Multi-step computation MCQ",
  r"The area (in square units) of the convex quadrilateral $PQRS$ with $P(1, 1)$, $Q(5, 2)$, $R(6, 6)$ and $S(2, 6)$ is",
  r"$\frac{35}{2}$",
  [(r"$35$", r"Adds the two triangle determinants but omits the factor $\frac{1}{2}$."),
   (r"$10$", r"Finds only the area of triangle $PRS$."),
   (r"$\frac{1}{2}$", r"Takes the vertices in the order $P, Q, S, R$ in a single shoelace sum, which crosses itself.")],
  r"Split along $PR$. Triangle $PQR$: $\frac{1}{2}|1(2-6) - 1(5-6) + (30-12)| = \frac{1}{2}(15) = \frac{15}{2}$. Triangle $PRS$: $\frac{1}{2}|1(6-6) - 1(6-2) + (36-12)| = \frac{1}{2}(20) = 10$. Total $= \frac{35}{2}$.",
  "Missing a triangle or taking vertices out of cyclic order.",
  "U03-B-area-quadrilateral", "Two area determinants combined.",
  check=_c38, values=[Rational(35, 2), 35, 10, Rational(1, 2)], cognitive="Application")


def _c39():
    D = Matrix([[x+2, x+3, x+2*a], [x+3, x+4, x+2*b], [x+4, x+5, x+2*c]]).det()
    return solve(D, b)[0]
Q("U03-B-039", "Properties of determinants", "Condition for a determinant to vanish identically", "Medium", "Inverse/parameter MCQ",
  r"Let $a, b, c$ be non-zero real numbers with $a + c \ne 0$. The determinant $\begin{vmatrix} x+2 & x+3 & x+2a \\ x+3 & x+4 & x+2b \\ x+4 & x+5 & x+2c \end{vmatrix}$ is zero for every real $x$ if and only if",
  r"$a, b, c$ are in A.P.",
  [(r"$a, b, c$ are in G.P.", r"Associates the middle-term condition with $b^2 = ac$ instead of $2b = a + c$."),
   (r"$a, b, c$ are in H.P.", r"Associates the condition with $b = \frac{2ac}{a+c}$."),
   (r"$a + b + c = 0$", r"Thinks the column sum must vanish for the determinant to be zero.")],
  r"$R_1 \to R_1 - 2R_2 + R_3$ makes the first row $(0, 0, 2a - 4b + 2c)$. Expanding, the determinant is $2(a - 2b + c)\begin{vmatrix} x+3 & x+4 \\ x+4 & x+5 \end{vmatrix} = 2(a-2b+c)(-1)$, which is zero for all $x$ exactly when $2b = a + c$, i.e. $a, b, c$ are in A.P.",
  r"Choosing the right row combination to eliminate $x$.",
  "U03-B-AP-det", r"Requires the operation $R_1 \to R_1 - 2R_2 + R_3$ and recognising the A.P. condition.",
  check=_c39, values=[(a+c)/2, sqrt(a*c), 2*a*c/(a+c), -(a+c)], cognitive="Analysis")

Q("U03-B-040", "Determinants", "Determinant of a matrix defined by a formula", "Medium", "Multi-step computation MCQ",
  r"Let $M = [m_{ij}]$ be the $3 \times 3$ matrix with $m_{ij} = (i + j)^2$. Then $|M|$ equals",
  r"$-8$",
  [(r"$8$", r"Correct reduction but a sign slip in the final $2 \times 2$ expansion."),
   (r"$0$", r"Assumes the rows are in A.P. as they would be for $m_{ij} = i + j$, making the determinant vanish."),
   (r"$-4$", r"Takes the common factor $2$ out of $R_3 - R_2 = (2, 2, 2)$ and then forgets it.")],
  r"$M = \begin{bmatrix} 4 & 9 & 16 \\ 9 & 16 & 25 \\ 16 & 25 & 36 \end{bmatrix}$. $R_3 \to R_3 - R_2$ and then $R_2 \to R_2 - R_1$ give rows $(4, 9, 16)$, $(5, 7, 9)$, $(7, 9, 11)$; then $R_3 \to R_3 - R_2$ gives $(2, 2, 2)$. Taking out $2$ and using $C_3 \to C_3 - C_2$ and then $C_2 \to C_2 - C_1$: $2\begin{vmatrix} 4 & 5 & 7 \\ 5 & 2 & 2 \\ 1 & 0 & 0 \end{vmatrix} = 2(10 - 14) = -8$.",
  "Assuming a quadratic pattern behaves like a linear one.",
  "U03-B-formula-entries", "Build the matrix, then several row and column operations.",
  check=lambda: Matrix(3, 3, lambda i, j: (i + 1 + j + 1)**2).det(), values=[-8, 8, 0, -4], cognitive="Application")


def _c41():
    A = diag(Rational(1, 2), 1, 1)
    s = (2*A).det()
    return (s*A.T).det()
Q("U03-B-041", "Properties of determinants", "Determinant of a determinant-scaled matrix", "Medium", "Multi-step computation MCQ",
  r"Let $P$ be a square matrix of order $3$ with $|P| = \frac{1}{2}$. Then the value of $\big|\,|2P|\,P^{T}\big|$ is",
  r"$32$",
  [(r"$2$", r"Correctly finds $|2P| = 4$ but then takes the scalar $4$ out only once: $4 \times \frac{1}{2}$."),
   (r"$4$", r"Takes $|2P| = 2^2|P| = 2$, then $2^3 \times \frac{1}{2}$."),
   (r"$8$", r"Finds $|2P| = 4$ but then uses $4^2|P^T|$.")],
  r"$|2P| = 2^3 \cdot \frac{1}{2} = 4$, a scalar. Then $|4P^T| = 4^3|P^T| = 64 \times \frac{1}{2} = 32$.",
  "Treating the inner determinant as a scalar and applying the order-3 rule twice.",
  "U03-B-kA-nested", "Two nested applications of the scalar rule.",
  check=_c41, values=[32, 2, 4, 8], cognitive="Application",
  numerical=dict(question=r"Let $P$ be a square matrix of order $3$ with $|P| = \frac{1}{2}$. Then the value of $\big|\,|2P|\,P^{T}\big|$ is", answer=32))


def _c42():
    d = symbols('d', real=True)
    A = diag(d, 1, 1)
    return FiniteSet(*solve((A.T*(2*A)).det() - 72, d))
Q("U03-B-042", "Properties of determinants", "Finding a determinant from a product condition", "Medium", "Inverse/parameter MCQ",
  r"Let $P$ be a real square matrix of order $3$ such that $|P^{T}(2P)| = 72$. The set of all possible values of $|P|$ is",
  r"$\{-3, 3\}$",
  [(r"$\{3\}$", r"Assumes $|P|$ must be positive because $|P^T(2P)| > 0$."),
   (r"$\{-6, 6\}$", r"Uses $|2P| = 2|P|$: $2|P|^2 = 72$."),
   (r"$\{-3\sqrt{2}, 3\sqrt{2}\}$", r"Uses $|2P| = 2^2|P|$: $4|P|^2 = 72$.")],
  r"$|P^T(2P)| = |P^T| \cdot 2^3|P| = 8|P|^2 = 72$, so $|P|^2 = 9$ and $|P| = \pm 3$. Both signs occur, e.g. $P = \operatorname{diag}(\pm 3, 1, 1)$.",
  r"The factor $k^n$ and losing the negative root of $|P|^2 = 9$.",
  "U03-B-kA-combo", "Reverse use of product and scalar rules with a sign trap.",
  check=_c42, values=[FiniteSet(-3, 3), FiniteSet(3), FiniteSet(-6, 6), FiniteSet(-3*sqrt(2), 3*sqrt(2))],
  cognitive="Analysis")

# ---------------------------------------------------------------- DIFFICULT


def _c43():
    g = 2*sin(2*x) + cos(4*x)
    M = Matrix([[1+sin(x)**2, cos(x)**2, g], [sin(x)**2, 1+cos(x)**2, g], [sin(x)**2, cos(x)**2, 1+g]])
    f = simplify(M.det())
    return maximum(f, x, Interval(0, 2*pi))
Q("U03-B-043", "Determinants", "Maximum of a trigonometric determinant", "Difficult", "Multi-step computation MCQ",
  r"The maximum value of $f(x) = \begin{vmatrix} 1+\sin^2 x & \cos^2 x & 2\sin 2x + \cos 4x \\ \sin^2 x & 1+\cos^2 x & 2\sin 2x + \cos 4x \\ \sin^2 x & \cos^2 x & 1 + 2\sin 2x + \cos 4x \end{vmatrix}$, $x \in \mathbb{R}$, is",
  r"$\frac{7}{2}$",
  [(r"$3$", r"Assumes the maximum occurs where $\sin 2x$ is largest: with $s = \sin 2x = 1$, $f = 3 + 2s - 2s^2 = 3$."),
   (r"$5$", r"Maximises the terms separately: $2 + 2(1) + 1 = 5$, although $\sin 2x = 1$ and $\cos 4x = 1$ cannot hold together."),
   (r"$\frac{5}{2}$", r"Takes the column sum as $1 + 2\sin 2x + \cos 4x$, dropping the $1$ from $\sin^2 x + \cos^2 x$, so $f = 2 + 2s - 2s^2$ with maximum $\frac{5}{2}$ at $s = \frac{1}{2}$.")],
  r"Let $g = 2\sin 2x + \cos 4x$. $C_1 \to C_1 + C_2 + C_3$ makes the first column $(2 + g)(1, 1, 1)^T$. Taking it out and using $R_2 - R_1$, $R_3 - R_1$ leaves $\begin{vmatrix} 1 & \cos^2 x & g \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{vmatrix} = 1$, so $f(x) = 2 + 2\sin 2x + \cos 4x$. With $s = \sin 2x \in [-1, 1]$ and $\cos 4x = 1 - 2s^2$, $f = 3 + 2s - 2s^2 = \frac{7}{2} - 2\left(s - \frac{1}{2}\right)^2$, whose maximum is $\frac{7}{2}$ at $s = \frac{1}{2}$.",
  "Bounding each trigonometric term separately instead of reducing to one variable and completing the square.",
  "U03-B-trig-extremum", r"Column-sum reduction, then rewriting $\cos 4x$ in terms of $\sin 2x$ and a quadratic maximum at an interior vertex (trap: $\sin 2x = 1$ is not optimal).",
  check=_c43, values=[Rational(7, 2), 3, 5, Rational(5, 2)], cognitive="Analysis",
  numerical=dict(question=r"If $M$ is the maximum value of $f(x) = \begin{vmatrix} 1+\sin^2 x & \cos^2 x & 2\sin 2x + \cos 4x \\ \sin^2 x & 1+\cos^2 x & 2\sin 2x + \cos 4x \\ \sin^2 x & \cos^2 x & 1 + 2\sin 2x + \cos 4x \end{vmatrix}$, $x \in \mathbb{R}$, then $2M$ is", answer=7))


def _c44():
    return max(Matrix(3, 3, list(e)).det() for e in itertools.product([0, 1], repeat=9))
Q("U03-B-044", "Determinants", "Maximum determinant with entries 0 and 1", "Difficult", "Conceptual/application MCQ",
  r"Among all $3 \times 3$ matrices whose every entry is $0$ or $1$, the maximum possible value of the determinant is",
  r"$2$",
  [(r"$1$", r"Assumes the identity matrix (or a permutation matrix) gives the largest value."),
   (r"$3$", r"Assumes all three positive terms of the expansion can equal $1$ while all three negative terms are $0$."),
   (r"$4$", r"Recalls the maximum $4$ for entries $\pm 1$.")],
  r"The expansion is $P - N$, where the positive terms $a_{11}a_{22}a_{33}$, $a_{12}a_{23}a_{31}$, $a_{13}a_{21}a_{32}$ together use all nine positions, and so do the negative terms; each term is $0$ or $1$. If all three positive terms are $1$, every entry is $1$ and the determinant is $0$. Otherwise $P \le 2$, so the determinant is at most $2$, and $\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{bmatrix}$ attains $1 + 1 - 0 = 2$.",
  "Assuming the positive terms can be made 1 independently of the negative ones.",
  "U03-B-max-det-entries", "Requires a structural argument about the six terms of the expansion.",
  check=_c44, values=[2, 1, 3, 4], cognitive="Analysis",
  numerical=dict(question=r"Among all $3 \times 3$ matrices whose every entry is $0$ or $1$, the maximum possible value of the determinant is", answer=2))


def _c45():
    return sum(1 for e in itertools.product([-1, 0, 1], repeat=4) if e[0]*e[3] - e[1]*e[2] > 0)
Q("U03-B-045", "Determinants", "Counting second order matrices with positive determinant", "Difficult", "Multi-step computation MCQ",
  r"The number of $2 \times 2$ matrices with every entry from the set $\{-1, 0, 1\}$ whose determinant is positive is",
  r"$24$",
  [(r"$48$", r"Counts all non-singular matrices, $81 - 33 = 48$, forgetting that only half of them have a positive determinant."),
   (r"$28$", r"Counts the ordered pairs with product $0$ as $3 + 3 = 6$, double counting $(0, 0)$: $2 \cdot 6 + 2 \cdot 2 + 6 \cdot 2 = 28$."),
   (r"$20$", r"Misses the case $ad = 1$, $bc = -1$, counting only $2 \cdot 5 + 5 \cdot 2 = 20$.")],
  r"For $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ we need $ad > bc$. Ordered pairs from $\{-1, 0, 1\}$ have product $1$ in $2$ ways, $0$ in $5$ ways and $-1$ in $2$ ways. The cases $(ad, bc) = (1, 0), (1, -1), (0, -1)$ give $2 \cdot 5 + 2 \cdot 2 + 5 \cdot 2 = 24$. Check: $5^2 + 2^2 + 2^2 = 33$ matrices are singular, and swapping the rows pairs positive with negative determinants, so $\frac{81 - 33}{2} = 24$.",
  "Not counting ordered pairs for each product value, or forgetting the sign symmetry.",
  "U03-B-count-det-positive", "Casework on product values with ordered counting and an inequality, or a symmetry argument.",
  check=_c45, values=[24, 48, 28, 20], cognitive="Analysis",
  numerical=dict(question=r"The number of $2 \times 2$ matrices with every entry from the set $\{-1, 0, 1\}$ whose determinant is positive is", answer=24))

nf = symbols('n', positive=True, integer=True)


def _c46():
    M = Matrix(3, 3, lambda i, j: factorial(nf + i + j))
    return factor(combsimp(M.det() / factorial(nf)**3))
Q("U03-B-046", "Factorised determinants", "Determinant of consecutive factorials", "Difficult", "Multi-step computation MCQ",
  r"For a positive integer $n$, let $D = \begin{vmatrix} n! & (n+1)! & (n+2)! \\ (n+1)! & (n+2)! & (n+3)! \\ (n+2)! & (n+3)! & (n+4)! \end{vmatrix}$. Then $\frac{D}{(n!)^3}$ equals",
  r"$2(n+1)^2(n+2)$",
  [(r"$-2(n+1)^2(n+2)$", r"Sign slip in the final $2 \times 2$ expansion: $2(n+2) - 2(n+3) = -2$."),
   (r"$2(n+1)(n+2)$", r"Takes $n!$, $(n+1)!$, $(n+2)!$ out of the rows but writes their product as $(n!)^3(n+1)(n+2)$, losing one factor $n+1$."),
   (r"$(n+1)^2(n+2)$", r"Writes $(n+2)(n+3) - (n+1)(n+2) = n + 2$ and $(n+3)(n+4) - (n+2)(n+3) = n + 3$, dropping the factor $2$, so the reduced determinant is $1$.")],
  r"Take $n!$, $(n+1)!$, $(n+2)!$ out of $R_1, R_2, R_3$; their product is $(n!)^3(n+1)^2(n+2)$. The rows become $(1, n+1, (n+1)(n+2))$, $(1, n+2, (n+2)(n+3))$, $(1, n+3, (n+3)(n+4))$. $R_3 \to R_3 - R_2$ and then $R_2 \to R_2 - R_1$ give $(0, 1, 2(n+2))$ and $(0, 1, 2(n+3))$, so the reduced determinant is $2(n+3) - 2(n+2) = 2$. Hence $\frac{D}{(n!)^3} = 2(n+1)^2(n+2)$.",
  r"Mishandling the factorial factors taken out of the rows, or losing the factor $2$ in the row differences.",
  "U03-B-eval-consecutive", "Factorial extraction from rows, row differences of quadratic entries and careful bookkeeping of the extracted factors.",
  check=_c46, values=[2*(nf+1)**2*(nf+2), -2*(nf+1)**2*(nf+2), 2*(nf+1)*(nf+2), (nf+1)**2*(nf+2)], cognitive="Analysis")

Q("U03-B-047", "Factorised determinants", "Homogeneous symmetric determinant", "Difficult", "Multi-step computation MCQ",
  r"For non-zero real $a, b, c$, the determinant $\begin{vmatrix} b^2+c^2 & ab & ac \\ ab & c^2+a^2 & bc \\ ac & bc & a^2+b^2 \end{vmatrix}$ equals",
  r"$4a^2b^2c^2$",
  [(r"$2a^2b^2c^2$", r"After $R_1 \to aR_1$ etc. and the reduction, keeps the factor $2$ from the row operation but misses the second factor $2$ from the final expansion."),
   (r"$-4a^2b^2c^2$", r"Sign slip when expanding the reduced determinant."),
   (r"$a^2b^2c^2$", r"Drops both factors of $2$ produced in the reduction.")],
  r"Multiply $R_1, R_2, R_3$ by $a, b, c$ and divide by $abc$; then take $a, b, c$ out of $C_1, C_2, C_3$: $\begin{vmatrix} b^2+c^2 & a^2 & a^2 \\ b^2 & c^2+a^2 & b^2 \\ c^2 & c^2 & a^2+b^2 \end{vmatrix}$. $R_1 \to R_1 - R_2 - R_3$ gives $(0, -2c^2, -2b^2)$; take out $-2$ and evaluate: $-2[-c^2(b^2(a^2+b^2) - b^2c^2) + b^2(b^2c^2 - c^2(c^2+a^2))] = -2(-2a^2b^2c^2) = 4a^2b^2c^2$.",
  "Losing factors of 2 or signs in a symbolic reduction.",
  "U03-B-factor-homog", "Scaling rows and columns, a row combination and a symbolic expansion.",
  check=lambda: factor(Matrix([[b**2+c**2, a*b, a*c], [a*b, c**2+a**2, b*c], [a*c, b*c, a**2+b**2]]).det()),
  values=[4*a**2*b**2*c**2, 2*a**2*b**2*c**2, -4*a**2*b**2*c**2, a**2*b**2*c**2], cognitive="Analysis")


def _c48():
    D = factor(Matrix([[a-b-c, 2*a, 2*a], [2*b, b-c-a, 2*b], [2*c, 2*c, c-a-b]]).det())
    s = symbols('s', real=True)
    Ds = D.subs(a, s - b - c)
    return solve(Eq(simplify(Ds), 27), s)[0]
Q("U03-B-048", "Factorised determinants", "Determinant equal to a perfect cube", "Difficult", "Inverse/parameter MCQ",
  r"For real numbers $a, b, c$, if $\begin{vmatrix} a-b-c & 2a & 2a \\ 2b & b-c-a & 2b \\ 2c & 2c & c-a-b \end{vmatrix} = 27$, then $a + b + c$ equals",
  r"$3$",
  [(r"$9$", r"Simplifies the determinant to $3(a+b+c)$ instead of $(a+b+c)^3$."),
   (r"$27$", r"Takes the determinant to be $a + b + c$, extracting the common factor but losing the remaining factor $(a+b+c)^2$."),
   (r"$-3$", r"Gets $-(a+b+c)^3$ from a sign slip in the final triangular determinant.")],
  r"$R_1 \to R_1 + R_2 + R_3$ makes the first row $(a+b+c)(1, 1, 1)$. Taking it out and using $C_2 - C_1$, $C_3 - C_1$ gives the lower triangular $\begin{vmatrix} 1 & 0 & 0 \\ 2b & -(a+b+c) & 0 \\ 2c & 0 & -(a+b+c) \end{vmatrix} = (a+b+c)^2$. So the determinant is $(a+b+c)^3 = 27$, and since $a+b+c$ is real, $a + b + c = 3$.",
  r"Missing that two further factors of $(a+b+c)$ appear after the first.",
  "U03-B-factor-sum-cube", "Row sum, column reduction and a cube equation.",
  check=_c48, values=[3, 9, 27, -3], cognitive="Analysis",
  numerical=dict(question=r"For real numbers $a, b, c$, if $\begin{vmatrix} a-b-c & 2a & 2a \\ 2b & b-c-a & 2b \\ 2c & 2c & c-a-b \end{vmatrix} = 27$, then the value of $a + b + c$ is", answer=3))


def _c49():
    M = Matrix([[x-2, 2*x-3, 3*x-4], [x-4, 2*x-9, 3*x-16], [x-8, 2*x-27, 3*x-64]])
    s = solve(M.det(), x)
    assert len(s) == 1
    return s[0]
Q("U03-B-049", "Determinant equations", "Determinant equation that is only linear", "Difficult", "Multi-step computation MCQ",
  r"The real number $x$ satisfying $\begin{vmatrix} x-2 & 2x-3 & 3x-4 \\ x-4 & 2x-9 & 3x-16 \\ x-8 & 2x-27 & 3x-64 \end{vmatrix} = 0$ is",
  r"$4$",
  [(r"$2$", r"Reads a root off the first entry $x - 2$, as if a column vanishing at one entry made the determinant zero."),
   (r"$8$", r"Reads a root off the last entry $x - 8$ of the first column."),
   (r"$-4$", r"Sign slip in the constant term of the final linear expression, getting $12(x+4)$.")],
  r"$C_2 \to C_2 - 2C_1$ and $C_3 \to C_3 - 3C_1$ give $\begin{vmatrix} x-2 & 1 & 2 \\ x-4 & -1 & -4 \\ x-8 & -11 & -40 \end{vmatrix}$, with $x$ only in the first column. Expanding: $(x-2)(40 - 44) - (x-4)(-40 + 22) + (x-8)(-4 + 2) = -4x + 8 + 18x - 72 - 2x + 16 = 12x - 48$. So $12(x - 4) = 0$ and $x = 4$.",
  "Expecting a cubic and guessing roots from the entries.",
  "U03-B-deteq-linear", "Column operations reveal the equation is linear; heavy arithmetic.",
  check=_c49, values=[4, 2, 8, -4], cognitive="Analysis")

al, be, ga, t1, t2, t3 = symbols('alpha beta gamma theta1 theta2 theta3', real=True)


def _c50():
    rows = [al, be, ga]; cols = [t1, t2, t3]
    M = Matrix(3, 3, lambda i, j: cos(rows[i] - cols[j]))
    return simplify(expand_trig(M.det()))
Q("U03-B-050", "Properties of determinants", "Determinant of a product of thin matrices (trigonometric)", "Difficult", "Conceptual/application MCQ",
  r"For real $\alpha, \beta, \gamma, \theta_1, \theta_2, \theta_3$, the value of $\begin{vmatrix} \cos(\alpha-\theta_1) & \cos(\alpha-\theta_2) & \cos(\alpha-\theta_3) \\ \cos(\beta-\theta_1) & \cos(\beta-\theta_2) & \cos(\beta-\theta_3) \\ \cos(\gamma-\theta_1) & \cos(\gamma-\theta_2) & \cos(\gamma-\theta_3) \end{vmatrix}$ is",
  r"$0$",
  [(r"$1$", r"Takes the special case $\theta_1 = \alpha, \theta_2 = \beta, \theta_3 = \gamma$ and reads off the diagonal entries $\cos 0 = 1$ as if the determinant were diagonal."),
   (r"$\cos(\alpha-\beta)\cos(\beta-\gamma)\cos(\gamma-\alpha)$", r"Guesses a cyclic product by analogy with the Vandermonde factorisation."),
   (r"$\sin(\alpha-\beta)\sin(\beta-\gamma)\sin(\gamma-\alpha)$", r"Guesses a product of sines, which vanishes when two angles coincide, by analogy with Vandermonde.")],
  r"$\cos(\alpha - \theta) = \cos\alpha\cos\theta + \sin\alpha\sin\theta$, so the matrix equals $\begin{bmatrix} \cos\alpha & \sin\alpha & 0 \\ \cos\beta & \sin\beta & 0 \\ \cos\gamma & \sin\gamma & 0 \end{bmatrix}\begin{bmatrix} \cos\theta_1 & \cos\theta_2 & \cos\theta_3 \\ \sin\theta_1 & \sin\theta_2 & \sin\theta_3 \\ 0 & 0 & 0 \end{bmatrix}$. The first factor has a zero column, so its determinant is $0$ and the product rule gives $0$.",
  "Not writing the matrix as a product with a zero column.",
  "U03-B-trig-product-zero", "Needs the factorisation idea; direct expansion is impractical.",
  check=_c50, values=[0, 1, cos(al-be)*cos(be-ga)*cos(ga-al), sin(al-be)*sin(be-ga)*sin(ga-al)], cognitive="Analysis")


def _c51():
    D1 = Matrix([[a, a**2, 1], [b, b**2, 1], [c, c**2, 1]]).det()
    D2 = Matrix([[a, 1/a, 1], [b, 1/b, 1], [c, 1/c, 1]]).det()
    prod = (a-b)*(b-c)*(c-a)
    s1 = simplify(D1**2 - prod**2) == 0
    s2 = simplify(D2**2 - (prod/(a*b*c))**2) == 0
    return (bool(s1), bool(s2))
Q("U03-B-051", "Area of a triangle", "Collinearity of points on curves", "Difficult", "Statement-based MCQ",
  r"Statement I: No three distinct points on the parabola $y = x^2$ are collinear. Statement II: No three distinct points on the hyperbola $xy = 1$ are collinear. In the light of the above statements, choose the correct answer.",
  r"Both Statement I and Statement II are true",
  [(r"Both Statement I and Statement II are false", r"Thinks a line can cut any conic in three points."),
   (r"Statement I is true but Statement II is false", r"Believes the two branches of the hyperbola allow a line to meet it three times."),
   (r"Statement I is false but Statement II is true", r"Mis-evaluates the parabola determinant as identically zero.")],
  r"For $(a, a^2), (b, b^2), (c, c^2)$ the collinearity determinant is $\pm(a-b)(b-c)(c-a) \ne 0$ for distinct $a, b, c$. For $\left(a, \frac{1}{a}\right), \left(b, \frac{1}{b}\right), \left(c, \frac{1}{c}\right)$ it is $\pm\frac{(a-b)(b-c)(c-a)}{abc} \ne 0$. So both statements are true.",
  "Not factorising the collinearity determinant.",
  "U03-B-statement-collinear-curves", "Two symbolic determinants to factorise and interpret.",
  check=_c51, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis")


def _c52():
    M = gen3()
    s1 = simplify((M + M.T).det() - 2*M.det()) == 0
    C = Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]])
    zero_row = any(all(v == 0 for v in C.row(i)) for i in range(3))
    prop = any(C.row(i).cross(C.row(j)).norm() == 0 for i in range(3) for j in range(i+1, 3))
    s2 = not (C.det() == 0 and not zero_row and not prop)
    return (bool(s1), bool(s2))
Q("U03-B-052", "Properties of determinants", "Testing general claims about determinants", "Difficult", "Statement-based MCQ",
  r"Statement I: For every square matrix $P$ of order $3$, $|P + P^{T}| = 2|P|$. Statement II: If a square matrix of order $3$ has determinant zero, then it has a zero row or two proportional rows. In the light of the above statements, choose the correct answer.",
  r"Both Statement I and Statement II are false",
  [(r"Both Statement I and Statement II are true", r"Treats the determinant as additive and believes the converse of the zero-row and proportional-row properties."),
   (r"Statement I is true but Statement II is false", r"Uses $|P + P^T| = |P| + |P^T|$."),
   (r"Statement I is false but Statement II is true", r"Believes the converse of the proportional-row property.")],
  r"Statement I: for $P = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}$, $|P| = 0$ but $|P + P^T| = \begin{vmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 2 \end{vmatrix} = -2$, so it is false. Statement II: $\begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 1 & 1 & 2 \end{bmatrix}$ has $R_3 = R_1 + R_2$, so its determinant is $0$, yet no row is zero and no two rows are proportional. Both are false.",
  "Believing converses of determinant properties and additivity.",
  "U03-B-statement-false-claims", "Requires constructing counterexamples for two general claims.",
  check=_c52, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")


def _c53():
    D = Matrix([[0, 0, 1], [3, 0, 1], [0, 4, 1]]).det()
    return D**2
Q("U03-B-053", "Area of a triangle", "Square of the area determinant from side lengths", "Difficult", "Conceptual/application MCQ",
  r"The vertices $(x_1, y_1)$, $(x_2, y_2)$, $(x_3, y_3)$ of a triangle are such that its sides have lengths $3$, $4$ and $5$. Then $\begin{vmatrix} x_1 & y_1 & 1 \\ x_2 & y_2 & 1 \\ x_3 & y_3 & 1 \end{vmatrix}^2$ equals",
  r"$144$",
  [(r"$36$", r"Equates the determinant to the area $6$ instead of twice the area."),
   (r"$9$", r"Takes the determinant as half the area, $3$."),
   (r"$50$", r"Confuses it with the sum of the squares of the sides, $9 + 16 + 25$.")],
  r"The sides $3, 4, 5$ form a right triangle of area $\frac{1}{2} \cdot 3 \cdot 4 = 6$. The determinant equals $\pm 2 \times \text{area} = \pm 12$, so its square is $144$, independent of position and orientation.",
  "Mixing up the determinant and the area by the factor 2.",
  "U03-B-area-sides", "Links side lengths, area and the determinant, which is only fixed up to sign.",
  check=_c53, values=[144, 36, 9, 50], cognitive="Analysis",
  numerical=dict(question=r"The vertices $(x_1, y_1)$, $(x_2, y_2)$, $(x_3, y_3)$ of a triangle are such that its sides have lengths $3$, $4$ and $5$. Then the value of $\begin{vmatrix} x_1 & y_1 & 1 \\ x_2 & y_2 & 1 \\ x_3 & y_3 & 1 \end{vmatrix}^2$ is", answer=144))

pp, qq = symbols('a b', positive=True)


def _c54():
    D = Matrix([[pp*cos(th), qq*sin(th), 1], [-pp*sin(th), qq*cos(th), 1], [-pp*cos(th), -qq*sin(th), 1]]).det()
    return simplify(Abs(simplify(D))/2)
Q("U03-B-054", "Area of a triangle", "Area with parametric vertices", "Difficult", "Multi-step computation MCQ",
  r"For $a > 0$, $b > 0$, the area of the triangle with vertices $(a\cos\theta, b\sin\theta)$, $(-a\sin\theta, b\cos\theta)$ and $(-a\cos\theta, -b\sin\theta)$ is",
  r"$ab$",
  [(r"$2ab$", r"Reports $|\Delta|$, omitting the factor $\frac{1}{2}$."),
   (r"$\frac{ab}{2}$", r"Halves twice, taking the area as $\frac{1}{4}|\Delta|$."),
   (r"$ab|\cos 2\theta|$", r"After $R_1 \to R_1 + R_3$, evaluates the minor $\begin{vmatrix} -\sin\theta & \cos\theta \\ -\cos\theta & -\sin\theta \end{vmatrix}$ as $\sin^2\theta - \cos^2\theta$, so $|\Delta| = 2ab|\cos 2\theta|$ and the area is $ab|\cos 2\theta|$.")],
  r"Take $a$ out of $C_1$ and $b$ out of $C_2$: $\Delta = ab\begin{vmatrix} \cos\theta & \sin\theta & 1 \\ -\sin\theta & \cos\theta & 1 \\ -\cos\theta & -\sin\theta & 1 \end{vmatrix}$. $R_1 \to R_1 + R_3$ gives $(0, 0, 2)$, so $\Delta = ab \cdot 2(\cos^2\theta + \sin^2\theta) = 2ab$. Area $= \frac{1}{2}|\Delta| = ab$, independent of $\theta$.",
  "Missing the row operation that makes the result independent of the parameter.",
  "U03-B-area-param-ellipse", "Factor extraction, a row operation and simplification with a parameter.",
  check=_c54, values=[pp*qq, 2*pp*qq, pp*qq/2, pp*qq*Abs(cos(2*th))], cognitive="Analysis")


def _c55():
    D = expand(Matrix([[1, cos(th), 1], [-cos(th), 2, cos(th)], [-1, -cos(th), 1]]).det())
    u = symbols('u', real=True)
    Du = D.subs(cos(th), u)
    assert not Du.has(th)
    return function_range(Du, u, Interval(-1, 1))
Q("U03-B-055", "Determinants", "Range of a trigonometric determinant", "Difficult", "Multi-step computation MCQ",
  r"If $\Delta(\theta) = \begin{vmatrix} 1 & \cos\theta & 1 \\ -\cos\theta & 2 & \cos\theta \\ -1 & -\cos\theta & 1 \end{vmatrix}$, then as $\theta$ varies over $\mathbb{R}$, the set of all values of $\Delta(\theta)$ is",
  r"$[4, 6]$",
  [(r"$(4, 6)$", r"Excludes the end points, overlooking that $\cos^2\theta$ attains $0$ and $1$."),
   (r"$[2, 6]$", r"Uses $\cos^2\theta \in [-1, 1]$."),
   (r"$[2, 4]$", r"Sign slip giving $\Delta = 4 - 2\cos^2\theta$.")],
  r"$R_1 \to R_1 + R_3$ gives $(0, 0, 2)$. Expanding along it: $\Delta = 2\begin{vmatrix} -\cos\theta & 2 \\ -1 & -\cos\theta \end{vmatrix} = 2(\cos^2\theta + 2) = 4 + 2\cos^2\theta$. As $\cos^2\theta \in [0, 1]$, $\Delta \in [4, 6]$.",
  r"Range of $\cos^2\theta$ and end point inclusion.",
  "U03-B-trig-range", "Row operation, expansion and a range argument with end points.",
  check=_c55, values=[Interval(4, 6), Interval.open(4, 6), Interval(2, 6), Interval(2, 4)], cognitive="Analysis")
