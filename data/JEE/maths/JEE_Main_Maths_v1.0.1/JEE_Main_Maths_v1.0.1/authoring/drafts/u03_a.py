import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from itertools import product as _iprod

# ---------------------------------------------------------------- helpers
SC = "XII"


def bm(rows):
    """LaTeX bmatrix from a list of rows (entries already LaTeX strings or numbers)."""
    return r"\begin{bmatrix} " + r" \\ ".join(" & ".join(str(e) for e in r) for r in rows) + r" \end{bmatrix}"


def M(rows):
    return Matrix(rows)


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

# ================================================================ EASY (17)


def _c001():
    out = []
    for m in range(1, 5):
        for n in range(1, 5):
            Pt = zeros(2, 3)          # P is 3 x 2, so P^T is 2 x 3
            Q = zeros(m, n)
            ok1 = Pt.shape[1] == Q.shape[0]
            ok2 = Q.shape[1] == Pt.shape[0]
            if ok1 and ok2:
                out.append((m, n))
    assert len(out) == 1
    return out[0]


q("U03-A-001", "Algebra of matrices", "Order of a matrix from defined products", "Easy",
  "Single-step computation MCQ",
  r"Let $P$ be a matrix of order $3 \times 2$. If $Q$ is a matrix such that both $P^T Q$ and $Q P^T$ are defined, then the order of $Q$ is",
  r"$3 \times 2$",
  [(r"$2 \times 3$", r"Applies the conditions to $P$ instead of $P^T$, i.e. makes $PQ$ and $QP$ defined."),
   (r"$3 \times 3$", r"Uses only the condition for $P^T Q$ (rows of $Q$ equal 3) and wrongly assumes $Q$ must be square."),
   (r"$2 \times 2$", r"Uses only the condition for $Q P^T$ (columns of $Q$ equal 2) and wrongly assumes $Q$ must be square.")],
  r"$P^T$ has order $2 \times 3$. For $P^T Q$ to be defined, $Q$ must have 3 rows; for $Q P^T$ to be defined, $Q$ must have 2 columns. Hence $Q$ is of order $3 \times 2$.",
  "Matching orders for products using $P$ in place of its transpose.",
  "U03-A-order-defined", "One idea (conformability) applied to two products.",
  check=_c001, values=[(3, 2), (2, 3), (3, 3), (2, 2)], cognitive="Understanding", source_class=SC)


def _c002():
    P = Matrix(3, 3, lambda i, j: (i + 1) ** (j + 1))
    return P.trace()


q("U03-A-002", "Algebra of matrices", "Matrix from an entry formula; trace", "Easy",
  "Single-step computation MCQ",
  r"Let $P = [p_{ij}]$ be the $3 \times 3$ matrix with $p_{ij} = i^{\,j}$ for $1 \le i, j \le 3$. Then the trace of $P$ equals",
  r"$32$",
  [(r"$8$", r"Adds the anti-diagonal entries $p_{13} + p_{22} + p_{31} = 1 + 4 + 3$."),
   (r"$14$", r"Takes the diagonal entries as $i^2$, giving $1 + 4 + 9$."),
   (r"$56$", r"Adds all nine entries: $3 + 14 + 39$.")],
  r"The trace is $p_{11} + p_{22} + p_{33} = 1^1 + 2^2 + 3^3 = 1 + 4 + 27 = 32$.",
  "Confusing the main diagonal with the anti-diagonal or with the whole matrix.",
  "U03-A-entry-formula", "Construct the diagonal from a formula and add.",
  check=_c002, values=[32, 8, 14, 56], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = [p_{ij}]$ be the $3 \times 3$ matrix with $p_{ij} = i^{\,j}$ for $1 \le i, j \le 3$. Then the trace of $P$ is", answer=32))


def _c003():
    P = M([[1, 2], [0, -1]]); Q = M([[3, 1], [2, 0]])
    return (P * Q).T


q("U03-A-003", "Transpose and symmetric matrices", "Transpose of a product", "Easy",
  "Single-step computation MCQ",
  r"If $P = " + bm([[1, 2], [0, -1]]) + r"$ and $Q = " + bm([[3, 1], [2, 0]]) + r"$, then $(PQ)^T$ equals",
  "$" + bm([[7, -2], [1, 0]]) + "$",
  [("$" + bm([[3, 2], [5, 4]]) + "$", r"Uses $(PQ)^T = P^T Q^T$ without reversing the order."),
   ("$" + bm([[7, 1], [-2, 0]]) + "$", r"Computes $PQ$ correctly but forgets to transpose."),
   ("$" + bm([[3, 5], [2, 4]]) + "$", r"Computes $QP$, taking the transpose of a product to be the product in reverse order without transposing the factors.")],
  r"$PQ = " + bm([["3 + 4", "1 + 0"], ["0 - 2", "0"]]) + " = " + bm([[7, 1], [-2, 0]]) + r"$, so $(PQ)^T = " + bm([[7, -2], [1, 0]]) + r"$. Equivalently $(PQ)^T = Q^T P^T$.",
  r"Believing $(PQ)^T = P^T Q^T$.",
  "U03-A-transpose-product", "One product and one transpose.",
  check=_c003, values=[M([[7, -2], [1, 0]]), M([[3, 2], [5, 4]]), M([[7, 1], [-2, 0]]), M([[3, 5], [2, 4]])],
  cognitive="Application", source_class=SC)


def _c004():
    x, y = symbols('x y')
    P = M([[1, x + 2*y, 3], [7, 0, 2*x - y], [3, 4, 2]])
    s = solve(list(P - P.T), [x, y], dict=True)[0]
    return s[x] + s[y]


q("U03-A-004", "Types of matrices", "Symmetric matrix: unknown entries", "Easy",
  "Inverse/parameter MCQ",
  r"If the matrix $P = " + bm([[1, "x + 2y", 3], [7, 0, "2x - y"], [3, 4, 2]]) + r"$ is symmetric, where $x, y \in \mathbb{R}$, then $x + y$ equals",
  r"$5$",
  [(r"$-5$", r"Uses the skew-symmetric condition $p_{ij} = -p_{ji}$, giving $x = -3$, $y = -2$."),
   (r"$\frac{19}{5}$", r"Pairs entries wrongly: sets $x + 2y = p_{32} = 4$ and $2x - y = p_{21} = 7$, giving $x = \frac{18}{5}$, $y = \frac{1}{5}$."),
   (r"$1$", r"Solves correctly for $x = 3$, $y = 2$ but reports $x - y$.")],
  r"Symmetry needs $p_{12} = p_{21}$ and $p_{23} = p_{32}$: $x + 2y = 7$ and $2x - y = 4$. From the second, $y = 2x - 4$, so $x + 4x - 8 = 7$, giving $x = 3$, $y = 2$ and $x + y = 5$. (Also $p_{13} = p_{31} = 3$ holds.)",
  "Pairing an entry with the wrong mirror entry across the diagonal.",
  "U03-A-symmetric-param", "Two linear conditions from the definition of symmetry.",
  check=_c004, values=[5, -5, Rational(19, 5), 1], cognitive="Application", source_class=SC)


def _c005():
    a, b, c = symbols('alpha beta gamma')
    P = M([[0, a, -3], [2, b, c], [3, 4, 0]])
    s = solve(list(P + P.T), [a, b, c], dict=True)[0]
    return s[a] + s[b] + s[c]


q("U03-A-005", "Types of matrices", "Skew-symmetric matrix: unknown entries", "Easy",
  "Inverse/parameter MCQ",
  r"If $P = " + bm([[0, r"\alpha", -3], [2, r"\beta", r"\gamma"], [3, 4, 0]]) + r"$ is a skew-symmetric matrix, then $\alpha + \beta + \gamma$ equals",
  r"$-6$",
  [(r"$6$", r"Uses the symmetric condition $p_{ij} = p_{ji}$: $\alpha = 2$, $\gamma = 4$, with $\beta = 0$."),
   (r"$-5$", r"Gets $\alpha = -2$, $\gamma = -4$ but takes the diagonal entry $\beta = 1$."),
   (r"$2$", r"Gets $\alpha = -2$, $\beta = 0$ but copies $\gamma = 4$ without changing sign.")],
  r"For a skew-symmetric matrix $p_{ji} = -p_{ij}$, so every diagonal entry is $0$: $\beta = 0$. Also $\alpha = -p_{21} = -2$ and $\gamma = p_{23} = -p_{32} = -4$; the pair $p_{13} = -3$, $p_{31} = 3$ is consistent. Hence $\alpha + \beta + \gamma = -2 + 0 - 4 = -6$.",
  "Forgetting that diagonal entries of a skew-symmetric matrix are zero, or the sign change.",
  "U03-A-skew-param", "Direct use of the definition entry by entry.",
  check=_c005, values=[-6, 6, -5, 2], cognitive="Application", source_class=SC)


def _c006():
    P = Matrix(3, 3, symbols('p0:9')); Q = Matrix(3, 3, symbols('q0:9'))
    expr = (2*P.T - 3*Q).trace()
    trP, trQ = symbols('trP trQ')
    expr = expr.subs(P[8], trP - P[0] - P[4]).subs(Q[8], trQ - Q[0] - Q[4])
    return simplify(expr).subs({trP: 3, trQ: -2})


q("U03-A-006", "Algebra of matrices", "Linearity of trace", "Easy",
  "Single-step computation MCQ",
  r"Let $P$ and $Q$ be $3 \times 3$ matrices with $\operatorname{tr}(P) = 3$ and $\operatorname{tr}(Q) = -2$, where $\operatorname{tr}$ denotes the trace. Then $\operatorname{tr}(2P^T - 3Q)$ equals",
  r"$12$",
  [(r"$0$", r"Takes $\operatorname{tr}(P^T) = -\operatorname{tr}(P)$, getting $-6 + 6$."),
   (r"$5$", r"Ignores the scalar multipliers: $3 - (-2)$."),
   (r"$-12$", r"Takes $\operatorname{tr}(P^T) = -\operatorname{tr}(P)$ and also evaluates $-3(-2)$ as $-6$.")],
  r"Trace is linear and $\operatorname{tr}(P^T) = \operatorname{tr}(P)$. So $\operatorname{tr}(2P^T - 3Q) = 2(3) - 3(-2) = 6 + 6 = 12$.",
  "Thinking transposition changes the trace.",
  "U03-A-trace-linear", "Two trace properties applied once.",
  check=_c006, values=[12, 0, 5, -12], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P$ and $Q$ be $3 \times 3$ matrices with $\operatorname{tr}(P) = 3$ and $\operatorname{tr}(Q) = -2$, where $\operatorname{tr}$ denotes the trace. Then the value of $\operatorname{tr}(2P^T - 3Q)$ is", answer=12))


def _c007():
    P = M([[2, -2], [1, -1]])            # a concrete non-trivial idempotent
    assert P * P == P
    k = symbols('k')
    E = (eye(2) + P) ** 3 - (eye(2) + k * P)
    return solve(list(E), k)[k] if isinstance(solve(list(E), k), dict) else solve(list(E), k)[0]


q("U03-A-007", "Types of matrices", "Idempotent matrix: binomial power", "Easy",
  "Single-step computation MCQ",
  r"Let $P$ be a non-zero square matrix with $P^2 = P$, and let $I$ be the identity matrix of the same order. If $(I + P)^3 = I + kP$, then $k$ equals",
  r"$7$",
  [(r"$3$", r"Treats $P$ as if $P^2 = O$, keeping only $I + 3P$."),
   (r"$6$", r"Expands to $I + 3P + 3P^2 + P^3$ but drops the $P^3$ term."),
   (r"$8$", r"Writes $(I+P)^3 = I + 2^3 P$ by analogy with $(1+1)^3$.")],
  r"Since $P$ and $I$ commute, $(I+P)^3 = I + 3P + 3P^2 + P^3$. With $P^2 = P$ we get $P^3 = P$, so $(I+P)^3 = I + (3 + 3 + 1)P = I + 7P$; thus $k = 7$.",
  r"Mishandling $P^n = P$ in a binomial expansion.",
  "U03-A-idempotent-binomial", "One binomial expansion with one substitution.",
  check=_c007, values=[7, 3, 6, 8], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P$ be a non-zero square matrix with $P^2 = P$, and let $I$ be the identity matrix of the same order. If $(I + P)^3 = I + kP$, then the value of $k$ is", answer=7))


def _c008():
    a, b = symbols('a b')
    P = M([[a, 4], [-6, b]])
    sols = solve(list(P * P - eye(2)), [a, b], dict=True)
    vals = {simplify(t[a] * t[b]) for t in sols}
    assert len(sols) >= 1 and len(vals) == 1
    return vals.pop()


q("U03-A-008", "Types of matrices", "Involutory matrix: two unknown diagonal entries", "Easy",
  "Inverse/parameter MCQ",
  r"Let $P = " + bm([["a", 4], [-6, "b"]]) + r"$, where $a, b \in \mathbb{R}$. If $P^2 = I$, where $I$ is the $2 \times 2$ identity matrix, then $ab$ equals",
  r"$-25$",
  [(r"$25$", r"Compares only the diagonal entries, getting $a^2 = b^2 = 25$, and takes $b = a$, ignoring the off-diagonal condition $4(a + b) = 0$."),
   (r"$-23$", r"Imposes $P^2 = -I$ instead of $P^2 = I$: with $b = -a$, $a^2 - 24 = -1$ gives $a^2 = 23$ and $ab = -23$."),
   (r"$-24$", r"Imposes $P^2 = O$ (nilpotent) instead of $P^2 = I$: with $b = -a$, $a^2 - 24 = 0$ gives $ab = -24$.")],
  r"$P^2 = " + bm([["a^2 - 24", "4(a + b)"], ["-6(a + b)", "b^2 - 24"]]) + r"$. Equating with $I$, the off-diagonal entries give $a + b = 0$, so $b = -a$, and the diagonal gives $a^2 - 24 = 1$, so $a^2 = 25$. Hence $ab = -a^2 = -25$ (for both $a = 5, b = -5$ and $a = -5, b = 5$).",
  "Ignoring the off-diagonal entries of $P^2$, or confusing the involutory condition with $P^2 = O$ or $P^2 = -I$.",
  "U03-A-involutory-trace-zero", "One matrix square; the off-diagonal entries force $b = -a$ before the diagonal equation.",
  check=_c008, values=[-25, 25, -23, -24], cognitive="Application", source_class=SC)


def _c009():
    P = M([[6, -9], [4, -6]])
    return P ** 2026


q("U03-A-009", "Types of matrices", "Nilpotent matrix: high power", "Easy",
  "Single-step computation MCQ",
  r"Let $P = " + bm([[6, -9], [4, -6]]) + r"$, and let $I$ and $O$ be the $2 \times 2$ identity and null matrices. Then $P^{2026}$ equals",
  r"$O$",
  [(r"$I$", r"Assumes $P^2 = I$ (involutory) and uses the even exponent."),
   (r"$P$", r"Assumes $P^2 = P$ (idempotent), so every power equals $P$."),
   (r"$-I$", r"Assumes $P^2 = -I$ and computes $(-I)^{1013} = -I$.")],
  r"$P^2 = " + bm([["36 - 36", "-54 + 54"], ["24 - 24", "-36 + 36"]]) + r" = O$. Hence $P^{2026} = (P^2)^{1013} = O$.",
  "Guessing the type of matrix instead of computing $P^2$.",
  "U03-A-nilpotent-power", "One product reveals $P^2 = O$.",
  check=_c009, values=[zeros(2), eye(2), M([[6, -9], [4, -6]]), -eye(2)], cognitive="Application", source_class=SC)


def _c010():
    D = diag(2, -1, 3)
    return (D ** 4).trace()


q("U03-A-010", "Powers of matrices", "Power of a diagonal matrix", "Easy",
  "Single-step computation MCQ",
  r"If $D = \operatorname{diag}(2, -1, 3)$, then the trace of $D^4$ equals",
  r"$98$",
  [(r"$256$", r"Computes $(\operatorname{tr} D)^4 = 4^4$."),
   (r"$96$", r"Keeps the sign of $-1$: $16 - 1 + 81$."),
   (r"$16$", r"Multiplies the trace by the exponent: $4 \times 4$.")],
  r"Powers of a diagonal matrix are taken entrywise on the diagonal: $D^4 = \operatorname{diag}(16, 1, 81)$, so its trace is $16 + 1 + 81 = 98$.",
  r"Assuming $\operatorname{tr}(D^n) = (\operatorname{tr} D)^n$.",
  "U03-A-diagonal-power", "One property of diagonal matrices.",
  check=_c010, values=[98, 256, 96, 16], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $D = \operatorname{diag}(2, -1, 3)$, then the trace of $D^4$ is", answer=98))


def _c011():
    return sum(1 for t in _iprod([0, 1], repeat=9) if Matrix(3, 3, t) == Matrix(3, 3, t).T)


q("U03-A-011", "Counting matrices", "Number of symmetric matrices", "Easy",
  "Single-step computation MCQ",
  r"The number of $3 \times 3$ symmetric matrices whose entries are all from the set $\{0, 1\}$ is",
  r"$64$",
  [(r"$512$", r"Counts all $3 \times 3$ matrices, $2^9$, ignoring symmetry."),
   (r"$8$", r"Counts only diagonal matrices, $2^3$."),
   (r"$256$", r"Assumes half of all $2^9$ matrices are symmetric.")],
  r"A symmetric $3 \times 3$ matrix is fixed by its 3 diagonal entries and the 3 entries above the diagonal; the rest are mirror copies. Each of these 6 entries has 2 choices, giving $2^6 = 64$.",
  "Not identifying the independent entries of a symmetric matrix.",
  "U03-A-count-symmetric", "Identify 6 free entries and count.",
  check=_c011, values=[64, 512, 8, 256], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The number of $3 \times 3$ symmetric matrices whose entries are all from the set $\{0, 1\}$ is", answer=64))


def _c012():
    k = symbols('k', positive=True)
    P = M([[3, 4], [-4, 3]]) / k
    return solve((P * P.T - eye(2))[0, 0], k)[0]


q("U03-A-012", "Types of matrices", "Orthogonal matrix: scaling factor", "Easy",
  "Inverse/parameter MCQ",
  r"If $P = \frac{1}{k} " + bm([[3, 4], [-4, 3]]) + r"$ with $k > 0$ satisfies $P P^T = I$, then $k$ equals",
  r"$5$",
  [(r"$25$", r"Writes the condition as $\frac{25}{k} = 1$, not squaring the factor $\frac{1}{k}$."),
   (r"$7$", r"Makes two slips together: takes the row length as $3 + 4$ instead of $\sqrt{3^2 + 4^2}$ and does not square the factor $\frac{1}{k}$, so solves $\frac{7}{k} = 1$."),
   (r"$\frac{1}{5}$", r"Treats the factor as $k$ instead of $\frac{1}{k}$, solving $25k^2 = 1$.")],
  r"$" + bm([[3, 4], [-4, 3]]) + bm([[3, -4], [4, 3]]) + r" = 25 I$, so $P P^T = \frac{25}{k^2} I$. Setting this equal to $I$ gives $k^2 = 25$, and $k > 0$ gives $k = 5$.",
  "Forgetting that the scalar factor appears twice in $P P^T$.",
  "U03-A-orthogonal-scale", "One product and one equation.",
  check=_c012, values=[5, 25, 7, Rational(1, 5)], cognitive="Application", source_class=SC)


def _c013():
    # Statement I: P + P^T symmetric for every square P; Statement II: P P^T skew-symmetric for every P
    p = Matrix(3, 3, symbols('p0:9'))
    s1 = simplify((p + p.T) - (p + p.T).T) == zeros(3)
    pt = M([[1, 2, 0], [0, 1, 3], [4, 0, 1]])
    s2 = (pt * pt.T).T == -(pt * pt.T)
    return (bool(s1), bool(s2))


q("U03-A-013", "Transpose and symmetric matrices", "Symmetry of P + P^T and P P^T", "Easy",
  "Statement-based MCQ",
  r"Statement I: For every square matrix $P$, the matrix $P + P^T$ is symmetric. Statement II: For every square matrix $P$, the matrix $P P^T$ is skew-symmetric." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II, confusing $P P^T$ with $P - P^T$."),
   (ST_FF, r"Rejects Statement I, thinking $(P + P^T)^T = P^T - P$."),
   (ST_FT, r"Swaps the two facts: thinks $P + P^T$ is skew-symmetric (so Statement I is false) and $P P^T$ is skew-symmetric (so Statement II is true), confusing both with $P - P^T$.")],
  r"$(P + P^T)^T = P^T + P$, so Statement I is true. $(P P^T)^T = (P^T)^T P^T = P P^T$, so $P P^T$ is symmetric, not skew-symmetric (for example, if $P = I$ then $P P^T = I \ne -I$); Statement II is false.",
  r"Confusing $P P^T$ (symmetric) with $P - P^T$ (skew-symmetric).",
  "U03-A-stmt-sym-constructions", "Two one-line transpose checks.",
  check=_c013, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Understanding", source_class=SC)


def _c014():
    P = M([[1, 2, -1], [0, 3, 2]]); Q = M([[2, 1], [-1, 0], [4, 3]])
    return (P * Q)[1, 0]


q("U03-A-014", "Algebra of matrices", "Single entry of a product", "Easy",
  "Single-step computation MCQ",
  r"If $P = " + bm([[1, 2, -1], [0, 3, 2]]) + r"$ and $Q = " + bm([[2, 1], [-1, 0], [4, 3]]) + r"$, then the entry in the second row and first column of $PQ$ is",
  r"$5$",
  [(r"$-2$", r"Computes the entry in the first row and second column instead."),
   (r"$-1$", r"Computes the $(2, 1)$ entry of $QP$ instead of $PQ$."),
   (r"$6$", r"Multiplies the second row of $P$ by the second column of $Q$.")],
  r"The $(2,1)$ entry of $PQ$ is (row 2 of $P$) $\cdot$ (column 1 of $Q$) $= 0(2) + 3(-1) + 2(4) = 5$.",
  "Mixing up row and column indices in a product.",
  "U03-A-product-entry", "One row-by-column product.",
  check=_c014, values=[5, -2, -1, 6], cognitive="Application", source_class=SC)


def _c015():
    X, Y = symbols('X Y', commutative=False)
    S = M([[5, 2], [0, 9]]); Dm = M([[3, 6], [0, -1]])
    Xm = (S + Dm) / 2; Ym = (S - Dm) / 2
    assert Xm + Ym == S and Xm - Ym == Dm
    return Xm * Ym


q("U03-A-015", "Algebra of matrices", "Solving simultaneous matrix equations, then a product", "Easy",
  "Multi-step computation MCQ",
  r"If $X + Y = " + bm([[5, 2], [0, 9]]) + r"$ and $X - Y = " + bm([[3, 6], [0, -1]]) + r"$, then $XY$ equals",
  "$" + bm([[4, 12], [0, 20]]) + "$",
  [("$" + bm([[4, -4], [0, 20]]) + "$", r"Finds $X$ and $Y$ correctly but computes $YX$."),
   ("$" + bm([[4, -8], [0, 20]]) + "$", r"Multiplies $X$ and $Y$ entry by entry."),
   ("$" + bm([[16, 48], [0, 80]]) + "$", r"Forgets to halve, using $2X$ and $2Y$ in the product.")],
  r"Adding and subtracting, $X = \frac{1}{2}" + bm([[8, 8], [0, 8]]) + " = " + bm([[4, 4], [0, 4]]) + r"$ and $Y = \frac{1}{2}" + bm([[2, -4], [0, 10]]) + " = " + bm([[1, -2], [0, 5]]) + r"$. Then $XY = " + bm([["4", "-8 + 20"], ["0", "20"]]) + " = " + bm([[4, 12], [0, 20]]) + "$.",
  "Treating matrix multiplication as commutative or entrywise.",
  "U03-A-linear-matrix-eqs", "Solve two linear matrix equations, then one product.",
  check=_c015, values=[M([[4, 12], [0, 20]]), M([[4, -4], [0, 20]]), M([[4, -8], [0, 20]]), M([[16, 48], [0, 80]])],
  cognitive="Application", source_class=SC)


def _c016():
    P = M([[1, 4], [2, 3]])
    return (P + P.T) / 2


q("U03-A-016", "Transpose and symmetric matrices", "Symmetric part of a matrix", "Easy",
  "Single-step computation MCQ",
  r"The matrix $P = " + bm([[1, 4], [2, 3]]) + r"$ is written as $P = S + K$, where $S$ is symmetric and $K$ is skew-symmetric. Then $S$ equals",
  "$" + bm([[1, 3], [3, 3]]) + "$",
  [("$" + bm([[2, 6], [6, 6]]) + "$", r"Uses $S = P + P^T$, forgetting the factor $\frac{1}{2}$."),
   ("$" + bm([[0, 1], [-1, 0]]) + "$", r"Gives the skew-symmetric part $\frac{1}{2}(P - P^T)$."),
   ("$" + bm([[1, 2], [4, 3]]) + "$", r"Takes $S = P^T$.")],
  r"$S = \frac{1}{2}(P + P^T) = \frac{1}{2}" + bm([[2, 6], [6, 6]]) + " = " + bm([[1, 3], [3, 3]]) + r"$, and $K = \frac{1}{2}(P - P^T) = " + bm([[0, 1], [-1, 0]]) + "$.",
  r"Forgetting the factor $\frac{1}{2}$ in the decomposition.",
  "U03-A-sym-part", "Direct formula, one step.",
  check=_c016, values=[M([[1, 3], [3, 3]]), M([[2, 6], [6, 6]]), M([[0, 1], [-1, 0]]), M([[1, 2], [4, 3]])],
  cognitive="Application", source_class=SC)


def _c017():
    c = 0
    for a, b, d in _iprod([-1, 0, 1], repeat=3):
        for diagv in _iprod([-1, 0, 1], repeat=3):
            P = M([[diagv[0], a, b], [-a, diagv[1], d], [-b, -d, diagv[2]]])
            if P.T == -P:
                c += 1
    return c


q("U03-A-017", "Counting matrices", "Number of skew-symmetric matrices", "Easy",
  "Single-step computation MCQ",
  r"The number of $3 \times 3$ skew-symmetric matrices whose entries are all from the set $\{-1, 0, 1\}$ is",
  r"$27$",
  [(r"$729$", r"Treats the diagonal as free too, counting $3^6$ as for symmetric matrices."),
   (r"$19683$", r"Counts all $3^9$ matrices, ignoring skew-symmetry."),
   (r"$8$", r"Allows each above-diagonal entry only the values $0$ or $1$.")],
  r"For a skew-symmetric matrix the diagonal entries are $0$ and each entry below the diagonal is the negative of its mirror entry. The 3 entries above the diagonal are free, each with 3 choices (their negatives also lie in the set), giving $3^3 = 27$.",
  "Forgetting that diagonal entries of a skew-symmetric matrix must be zero.",
  "U03-A-count-skew", "Identify the free entries and count.",
  check=_c017, values=[27, 729, 19683, 8], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The number of $3 \times 3$ skew-symmetric matrices whose entries are all from the set $\{-1, 0, 1\}$ is", answer=27))

# ================================================================ MEDIUM (25)


def _c018():
    a, b = symbols('a b')
    P = M([[1, 2], [3, 4]]); Q = M([[a, 4], [6, b]])
    E = P * Q - Q * P
    s = solve(list(E), [a, b], dict=True)[0]      # one-parameter family
    return simplify((b - a).subs(s))


q("U03-A-018", "Algebra of matrices", "Commuting matrices: unknown entries", "Medium",
  "Inverse/parameter MCQ",
  r"Let $P = " + bm([[1, 2], [3, 4]]) + r"$ and $Q = " + bm([["a", 4], [6, "b"]]) + r"$, where $a, b \in \mathbb{R}$. If $PQ = QP$, then $b - a$ equals",
  r"$6$",
  [(r"$-6$", r"Sign slip when equating the $(1,2)$ entries, writing $2b - 2a = -12$."),
   (r"$12$", r"Equates the $(1,2)$ entries, $4 + 2b = 2a + 16$, and stops at $2b - 2a = 12$."),
   (r"$18$", r"Equates the $(2,1)$ entries, $3a + 24 = 6 + 3b$, and stops at $3b - 3a = 18$.")],
  r"$PQ = " + bm([["a + 12", "4 + 2b"], ["3a + 24", "12 + 4b"]]) + r"$ and $QP = " + bm([["a + 12", "2a + 16"], ["6 + 3b", "12 + 4b"]]) + r"$. The $(1,2)$ entries give $2b - 2a = 12$ and the $(2,1)$ entries give $3b - 3a = 18$; both say $b - a = 6$. So $a, b$ are not unique, but $b - a = 6$.",
  "Leaving the relation as a multiple of $b - a$, or sign errors in comparing entries.",
  "U03-A-commute-param", "Two products and entrywise comparison; recognise a one-parameter family.",
  check=_c018, values=[6, -6, 12, 18], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 2], [3, 4]]) + r"$ and $Q = " + bm([["a", 4], [6, "b"]]) + r"$, where $a, b \in \mathbb{R}$. If $PQ = QP$, then the value of $b - a$ is", answer=6))


def _c019():
    P = M([[2, 1], [0, 2]])
    sols = [n for n in range(1, 200) if (P ** n)[0, 1] == 6 * (P ** n)[0, 0]]
    assert len(sols) == 1 and all((P ** n)[1, 0] == 0 and (P ** n)[0, 0] == (P ** n)[1, 1] for n in range(1, 30))
    return sols[0]


q("U03-A-019", "Powers of matrices", "Powers of a scalar matrix plus a nilpotent matrix", "Medium",
  "Inverse/parameter MCQ",
  r"Let $P = " + bm([[2, 1], [0, 2]]) + r"$. For a positive integer $n$, write $P^n = " + bm([[r"\alpha", r"\beta"], [0, r"\alpha"]]) + r"$. If $\beta = 6\alpha$, then $n$ equals",
  r"$12$",
  [(r"$6$", r"Writes $P^n = 2^n I + n 2^n N$ with $N = " + bm([[0, 1], [0, 0]]) + r"$, giving $\beta = n\alpha$ and $n = 6$."),
   (r"$3$", r"Writes the coefficient of $N$ as $n 2^{n+1}$ instead of $n 2^{n-1}$, giving $\beta = 2n\alpha$ and $2n = 6$."),
   (r"$13$", r"Uses $n - 1$ for the binomial coefficient $\binom{n}{1}$, writing $\beta = (n - 1)2^{n-1}$, so $\frac{n - 1}{2} = 6$.")],
  r"Write $P = 2I + N$ with $N = " + bm([[0, 1], [0, 0]]) + r"$. Since $N^2 = O$ and $2I$ commutes with $N$, the binomial expansion gives $P^n = 2^n I + n 2^{n-1} N = " + bm([["2^n", "n 2^{n-1}"], [0, "2^n"]]) + r"$. So $\alpha = 2^n$, $\beta = n 2^{n-1}$ and $\frac{\beta}{\alpha} = \frac{n}{2} = 6$, giving $n = 12$.",
  r"Mishandling the power of $2$ attached to $N$ in $(2I + N)^n$.",
  "U03-A-power-scalar-plus-nilpotent", "Split into scalar plus nilpotent, expand binomially, then form a ratio.",
  check=_c019, values=[12, 6, 3, 13], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[2, 1], [0, 2]]) + r"$. For a positive integer $n$, write $P^n = " + bm([[r"\alpha", r"\beta"], [0, r"\alpha"]]) + r"$. If $\beta = 6\alpha$, then the value of $n$ is", answer=12))


def _c020():
    P = M([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    return (P ** 10)[2, 0]


q("U03-A-020", "Powers of matrices", "Powers of a lower triangular matrix", "Medium",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[1, 0, 0], [1, 1, 0], [1, 1, 1]]) + r"$. The entry in the third row and first column of $P^{10}$ is",
  r"$55$",
  [(r"$45$", r"Keeps only the $\binom{10}{2}N^2$ contribution and drops the $10N$ term."),
   (r"$10$", r"Keeps only the $10N$ term and drops the $\binom{10}{2}N^2$ term."),
   (r"$66$", r"Uses the correct formula $\frac{n(n+1)}{2}$ but with $n = 11$ (off by one).")],
  r"Write $P = I + N$ with $N = " + bm([[0, 0, 0], [1, 0, 0], [1, 1, 0]]) + r"$. Then $N^2$ has a single non-zero entry $1$ in position $(3,1)$ and $N^3 = O$. Since $I$ and $N$ commute, $P^{10} = I + 10N + \binom{10}{2}N^2$, whose $(3,1)$ entry is $10 + 45 = 55$.",
  "Truncating the binomial expansion of $(I + N)^n$ too early.",
  "U03-A-power-triangular", "Split into identity plus nilpotent and use the binomial theorem.",
  check=_c020, values=[55, 45, 10, 66], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 0, 0], [1, 1, 0], [1, 1, 1]]) + r"$. The entry in the third row and first column of $P^{10}$ is", answer=55))


def _c021():
    t = pi / 12
    P = M([[cos(t), -sin(t)], [sin(t), cos(t)]])
    Pn = eye(2)
    for n in range(1, 100):
        Pn = (Pn * P).applyfunc(lambda e: radsimp(expand(e)))
        if all(abs(N(e, 40)) < 1e-30 for e in (Pn - eye(2))):
            return n


q("U03-A-021", "Powers of matrices", "Powers of a rotation matrix", "Medium",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[r"\cos\frac{\pi}{12}", r"-\sin\frac{\pi}{12}"], [r"\sin\frac{\pi}{12}", r"\cos\frac{\pi}{12}"]]) + r"$. The least positive integer $n$ for which $P^n = I$ is",
  r"$24$",
  [(r"$12$", r"Stops at $n\theta = \pi$, where $P^{12} = -I$, not $I$."),
   (r"$6$", r"Stops at $n\theta = \frac{\pi}{2}$, where $P^6$ is a quarter turn."),
   (r"$48$", r"Takes the rotation angle as half of $\frac{\pi}{12}$, i.e. $\frac{\pi}{24}$.")],
  r"$P$ is the rotation matrix $R(\theta)$ with $\theta = \frac{\pi}{12}$, and $R(\alpha)R(\beta) = R(\alpha + \beta)$, so $P^n = R\left(\frac{n\pi}{12}\right)$. This is $I$ exactly when $\frac{n\pi}{12}$ is a multiple of $2\pi$, so the least $n$ is $24$.",
  r"Confusing $P^n = -I$ with $P^n = I$.",
  "U03-A-rotation-power", "Recognise the rotation structure and use angle addition.",
  check=_c021, values=[24, 12, 6, 48], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[r"\cos\frac{\pi}{12}", r"-\sin\frac{\pi}{12}"], [r"\sin\frac{\pi}{12}", r"\cos\frac{\pi}{12}"]]) + r"$. The least positive integer $n$ for which $P^n = I$ is", answer=24))


def _c022():
    P = ones(3, 3)
    k = symbols('k')
    return solve((P ** 5 - k * P)[0, 0], k)[0]


q("U03-A-022", "Powers of matrices", "Power of the all-ones matrix", "Medium",
  "Single-step computation MCQ",
  r"Let $P$ be the $3 \times 3$ matrix in which every entry is $1$. If $P^5 = kP$, then $k$ equals",
  r"$81$",
  [(r"$243$", r"Uses $P^n = 3^n P$ instead of $3^{n-1} P$."),
   (r"$27$", r"Uses $P^n = 3^{n-2} P$, an off-by-one in the exponent."),
   (r"$15$", r"Uses $P^n = 3n\,P$, treating each multiplication as adding 3.")],
  r"$P^2 = 3P$, since each entry of $P^2$ is $1 + 1 + 1$. Then $P^3 = 3P^2 = 9P$ and in general $P^n = 3^{n-1}P$, so $P^5 = 81P$ and $k = 81$.",
  "Off-by-one in the exponent of the scaling pattern.",
  "U03-A-power-rank-one", "Find $P^2 = 3P$ and extend by induction.",
  check=_c022, values=[81, 243, 27, 15], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P$ be the $3 \times 3$ matrix in which every entry is $1$. If $P^5 = kP$, then the value of $k$ is", answer=81))


def _c023():
    al, be = symbols('alpha beta')
    P = M([[3, 1], [-1, 2]])
    s = solve(list(P ** 2 - al * P - be * eye(2)), [al, be], dict=True)[0]
    return s[al] + s[be]


q("U03-A-023", "Powers of matrices", "Square of a 2 by 2 matrix as a linear combination", "Medium",
  "Inverse/parameter MCQ",
  r"Let $P = " + bm([[3, 1], [-1, 2]]) + r"$. If $P^2 = \alpha P + \beta I$ for real numbers $\alpha$ and $\beta$, then $\alpha + \beta$ equals",
  r"$-2$",
  [(r"$12$", r"Gets $\alpha = 5$ but takes $\beta = 7$ with the wrong sign."),
   (r"$2$", r"Gets $\beta = 7$ and $\alpha = -5$, both signs reversed."),
   (r"$-12$", r"Gets $\beta = -7$ but takes $\alpha = -5$.")],
  r"$P^2 = " + bm([["9 - 1", "3 + 2"], ["-3 - 2", "-1 + 4"]]) + " = " + bm([[8, 5], [-5, 3]]) + r"$. Comparing with $\alpha P + \beta I = " + bm([[r"3\alpha + \beta", r"\alpha"], [r"-\alpha", r"2\alpha + \beta"]]) + r"$ gives $\alpha = 5$ and $15 + \beta = 8$, so $\beta = -7$. Hence $\alpha + \beta = -2$.",
  "Sign errors when matching entries, especially the constant term.",
  "U03-A-square-linear-relation", "One square and a two-unknown entry comparison.",
  check=_c023, values=[-2, 12, 2, -12], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[3, 1], [-1, 2]]) + r"$. If $P^2 = \alpha P + \beta I$ for real numbers $\alpha$ and $\beta$, then the value of $\alpha + \beta$ is", answer=-2))


def _c024():
    P = M([[2, 5, -1], [3, 0, 4], [7, -2, 1]])
    K = (P - P.T) / 2
    return sum(e ** 2 for e in K)


q("U03-A-024", "Transpose and symmetric matrices", "Skew-symmetric part of a 3 by 3 matrix", "Medium",
  "Multi-step computation MCQ",
  r"The matrix $P = " + bm([[2, 5, -1], [3, 0, 4], [7, -2, 1]]) + r"$ is written as $S + K$, where $S$ is symmetric and $K$ is skew-symmetric. The sum of the squares of all nine entries of $K$ is",
  r"$52$",
  [(r"$26$", r"Squares only the three entries above the diagonal of $K$."),
   (r"$208$", r"Uses $K = P - P^T$ without the factor $\frac{1}{2}$."),
   (r"$104$", r"Uses $K = P - P^T$ and squares only the entries above the diagonal.")],
  r"$K = \frac{1}{2}(P - P^T)$. Its entries above the diagonal are $k_{12} = \frac{5 - 3}{2} = 1$, $k_{13} = \frac{-1 - 7}{2} = -4$, $k_{23} = \frac{4 + 2}{2} = 3$; the diagonal is zero and the entries below are the negatives. The sum of squares is $2(1 + 16 + 9) = 52$.",
  r"Forgetting the factor $\frac{1}{2}$ or the mirror entries.",
  "U03-A-skew-part", "Decomposition then a careful sum over mirrored entries.",
  check=_c024, values=[52, 26, 208, 104], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The matrix $P = " + bm([[2, 5, -1], [3, 0, 4], [7, -2, 1]]) + r"$ is written as $S + K$, where $S$ is symmetric and $K$ is skew-symmetric. The sum of the squares of all nine entries of $K$ is", answer=52))


def _c025():
    # Statement I on a concrete commuting symmetric pair; Statement II symbolically
    P1 = M([[1, 2, 0], [2, 1, 0], [0, 0, 3]]); Q1 = P1 ** 2 + 2 * P1
    assert P1.T == P1 and Q1.T == Q1
    s1 = (P1 * Q1 == Q1 * P1) and ((P1 * Q1).T == P1 * Q1)
    a, b, c = symbols('a b c')
    Kk = M([[0, a, b], [-a, 0, c], [-b, -c, 0]])
    s2 = expand((Kk ** 3).T + Kk ** 3) == zeros(3)
    return (bool(s1), bool(s2))


q("U03-A-025", "Transpose and symmetric matrices", "Symmetry of products and powers", "Medium",
  "Statement-based MCQ",
  r"Statement I: If $P$ and $Q$ are symmetric matrices of the same order with $PQ = QP$, then $PQ$ is symmetric. Statement II: If $P$ is a skew-symmetric matrix, then $P^3$ is skew-symmetric." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Thinks every power of a skew-symmetric matrix is symmetric, so rejects Statement II."),
   (ST_FT, r"Rejects Statement I, believing a product of symmetric matrices is never symmetric."),
   (ST_FF, r"Rejects both: believes a product of symmetric matrices is never symmetric, and that odd powers of a skew-symmetric matrix are symmetric, as $P^2$ is.")],
  r"Statement I: $(PQ)^T = Q^T P^T = QP = PQ$, so $PQ$ is symmetric; true. Statement II: $(P^3)^T = (P^T)^3 = (-P)^3 = -P^3$, so $P^3$ is skew-symmetric; true.",
  "Assuming all powers of a skew-symmetric matrix are symmetric (only even powers are).",
  "U03-A-stmt-sym-products", "Two short transpose arguments, one needing the commuting hypothesis.",
  check=_c025, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Understanding", source_class=SC)


def _c026():
    P = M([[1, 0], [0, 0]]); Q = M([[0, 1], [0, 1]])
    assert P * P == P and Q * Q == Q
    s1 = (P * Q) ** 2 == P * Q
    X = Matrix(2, 2, symbols('x0:4'))
    # (I - X)^2 - (I - X) reduces to X^2 - X, which is O whenever X is idempotent
    s2 = expand((eye(2) - X) ** 2 - (eye(2) - X) - (X ** 2 - X)) == zeros(2)
    return (bool(s1), bool(s2))


q("U03-A-026", "Types of matrices", "Idempotent matrices: products and complements", "Medium",
  "Statement-based MCQ",
  r"Statement I: If $P$ and $Q$ are idempotent matrices of the same order (that is, $P^2 = P$ and $Q^2 = Q$), then $PQ$ is idempotent. Statement II: If $P$ is idempotent, then $I - P$ is idempotent, where $I$ is the identity matrix of the same order." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement I by writing $(PQ)^2 = P^2 Q^2$, which needs $PQ = QP$."),
   (ST_TF, r"Accepts Statement I via $(PQ)^2 = P^2Q^2$ and rejects Statement II after a sign slip, expanding $(I - P)^2$ as $I + 2P + P^2 = I + 3P$."),
   (ST_FF, r"Rejects Statement II after expanding $(I - P)^2 = I - 2P + P^2$ and not substituting $P^2 = P$.")],
  r"Statement I is false: $P = " + bm([[1, 0], [0, 0]]) + r"$ and $Q = " + bm([[0, 1], [0, 1]]) + r"$ are idempotent, but $PQ = " + bm([[0, 1], [0, 0]]) + r"$ has $(PQ)^2 = O \ne PQ$. Statement II is true: $(I - P)^2 = I - 2P + P^2 = I - 2P + P = I - P$.",
  r"Using $(PQ)^2 = P^2Q^2$, valid only when $P$ and $Q$ commute.",
  "U03-A-stmt-idempotent", "Needs a counterexample for one statement and a short expansion for the other.",
  check=_c026, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Analysis", source_class=SC, flags="")


def _c027():
    P = M([[0, 1], [0, 0]]); Q = M([[0, 0], [1, 0]])
    s1 = (P + Q) ** 2 == P ** 2 + 2 * P * Q + Q ** 2
    R = M([[1, 0], [0, 0]]); T = M([[0, 0], [0, 1]])
    s2 = not (R * T == zeros(2) and R != zeros(2) and T != zeros(2))
    return (bool(s1), bool(s2))


q("U03-A-027", "Algebra of matrices", "Non-commutativity and zero divisors", "Medium",
  "Statement-based MCQ",
  r"Statement I: For all square matrices $P$ and $Q$ of the same order, $(P + Q)^2 = P^2 + 2PQ + Q^2$. Statement II: If $P$ and $Q$ are square matrices of the same order with $PQ = O$, then $P = O$ or $Q = O$." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Carries over the real-number identities, ignoring non-commutativity and zero divisors."),
   (ST_TF, r"Accepts the binomial square as for numbers but recalls that $PQ = O$ is possible with non-zero factors."),
   (ST_FT, r"Rejects the square identity but still treats matrices as having no zero divisors.")],
  r"$(P + Q)^2 = P^2 + PQ + QP + Q^2$, which equals $P^2 + 2PQ + Q^2$ only when $PQ = QP$; for $P = " + bm([[0, 1], [0, 0]]) + r"$, $Q = " + bm([[0, 0], [1, 0]]) + r"$ it fails, so Statement I is false. For $P = " + bm([[1, 0], [0, 0]]) + r"$, $Q = " + bm([[0, 0], [0, 1]]) + r"$ we have $PQ = O$ with both non-zero, so Statement II is false.",
  "Applying real-number algebra rules to matrices.",
  "U03-A-stmt-noncommutative", "Requires constructing two counterexamples.",
  check=_c027, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Understanding", source_class=SC)


def _c028():
    a, b = symbols('a b', real=True)
    P = M([[1, 2, 2], [2, 1, -2], [a, 2, b]]) / 3
    E = P * P.T - eye(3)
    s = solve([E[0, 2], E[1, 2], E[2, 2]], [a, b], dict=True)
    assert len(s) == 1
    return s[0][a] + s[0][b]


q("U03-A-028", "Types of matrices", "Orthogonal 3 by 3 matrix with unknown entries", "Medium",
  "Inverse/parameter MCQ",
  r"If $P = \frac{1}{3}" + bm([[1, 2, 2], [2, 1, -2], ["a", 2, "b"]]) + r"$ satisfies $P P^T = I$, where $a, b \in \mathbb{R}$, then $a + b$ equals",
  r"$-3$",
  [(r"$3$", r"Uses only the unit-length condition with $a = b - 1$, solving $(b-1)^2 + b^2 = 5$ and picking $b = 2$, $a = 1$ without checking orthogonality to the first row."),
   (r"$1$", r"Sign slip in the second-row condition, writing $a = 1 - b$, which gives $b = -5$, $a = 6$."),
   (r"$-\frac{1}{3}$", r"Drops the $2 \times 2 = 4$ term in the first-row condition, solving $a + 2b = 0$ with $a = b - 1$.")],
  r"$P P^T = I$ means the rows of $3P$ are mutually orthogonal and each has length $3$. Orthogonality of row 3 to rows 1 and 2 gives $a + 4 + 2b = 0$ and $2a + 2 - 2b = 0$, i.e. $a = b - 1$ and then $3b + 3 = 0$, so $b = -1$, $a = -2$. The length check $4 + 4 + 1 = 9$ holds. Hence $a + b = -3$.",
  "Using only part of the orthogonality conditions.",
  "U03-A-orthogonal-unknowns", "Two orthogonality equations plus a consistency check.",
  check=_c028, values=[-3, 3, 1, Rational(-1, 3)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $P = \frac{1}{3}" + bm([[1, 2, 2], [2, 1, -2], ["a", 2, "b"]]) + r"$ satisfies $P P^T = I$, where $a, b \in \mathbb{R}$, then the value of $a + b$ is", answer=-3))


def _c029():
    c = 0
    for t in _iprod([0, 1], repeat=9):
        P = Matrix(3, 3, t)
        if P == P.T and P.trace() == 2:
            c += 1
    return c


q("U03-A-029", "Counting matrices", "Symmetric matrices with a given trace", "Medium",
  "Multi-step computation MCQ",
  r"The number of $3 \times 3$ symmetric matrices with entries from $\{0, 1\}$ and trace equal to $2$ is",
  r"$24$",
  [(r"$64$", r"Counts all symmetric matrices with entries from $\{0, 1\}$, ignoring the trace condition."),
   (r"$3$", r"Counts only the choices of the diagonal and forgets the free off-diagonal entries."),
   (r"$48$", r"Chooses the two diagonal 1s as an ordered pair ($6$ ways) instead of $\binom{3}{2} = 3$ ways.")],
  r"Trace $2$ means exactly two diagonal entries are $1$: $\binom{3}{2} = 3$ ways. The three entries above the diagonal are free ($2^3 = 8$ ways) and fix those below. Total $3 \times 8 = 24$.",
  "Counting ordered selections or ignoring the free off-diagonal entries.",
  "U03-A-count-symmetric", "Two independent counting steps.",
  check=_c029, values=[24, 64, 3, 48], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The number of $3 \times 3$ symmetric matrices with entries from $\{0, 1\}$ and trace equal to $2$ is", answer=24))


def _c030():
    P = M([[2, 1], [0, 1]])
    return (P ** 6)[0, 1]


q("U03-A-030", "Powers of matrices", "Powers of an upper triangular matrix", "Medium",
  "Multi-step computation MCQ",
  r"If $P = " + bm([[2, 1], [0, 1]]) + r"$, then the entry in the first row and second column of $P^6$ is",
  r"$63$",
  [(r"$64$", r"Assumes the $(1,2)$ entry follows the diagonal and equals $2^6$."),
   (r"$6$", r"Assumes the $(1,2)$ entry grows by $1$ each time, as for $" + bm([[1, 1], [0, 1]]) + r"$."),
   (r"$32$", r"Takes the $(1,2)$ entry of $P^n$ as $2^{n-1}$.")],
  r"$P^2 = " + bm([[4, 3], [0, 1]]) + r"$, $P^3 = " + bm([[8, 7], [0, 1]]) + r"$; by induction $P^n = " + bm([["2^n", "2^n - 1"], [0, 1]]) + r"$ because the $(1,2)$ entry of $P^n P$ is $2^n \cdot 1 + (2^n - 1) \cdot 1 = 2^{n+1} - 1$. So the required entry is $2^6 - 1 = 63$.",
  "Guessing the off-diagonal pattern from the diagonal.",
  "U03-A-power-affine", "Compute two powers, spot and justify the pattern.",
  check=_c030, values=[63, 64, 6, 32], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $P = " + bm([[2, 1], [0, 1]]) + r"$, then the entry in the first row and second column of $P^6$ is", answer=63))


def _c031():
    P = M([[2, 1], [-1, 3]])
    return P ** 2 - 5 * P + 6 * eye(2)


q("U03-A-031", "Algebra of matrices", "Matrix polynomial", "Medium",
  "Multi-step computation MCQ",
  r"If $f(x) = x^2 - 5x + 6$ and $P = " + bm([[2, 1], [-1, 3]]) + r"$, then $f(P)$ equals",
  "$" + bm([[-1, 0], [0, -1]]) + "$",
  [("$" + bm([[-1, 6], [6, -1]]) + "$", r"Adds the constant $6$ to every entry instead of using $6I$."),
   ("$" + bm([[0, -4], [6, 0]]) + "$", r"Squares $P$ entry by entry instead of computing $P \cdot P$."),
   ("$" + bm([[-7, 0], [0, -7]]) + "$", r"Drops the constant term $6I$.")],
  r"$P^2 = " + bm([["4 - 1", "2 + 3"], ["-2 - 3", "-1 + 9"]]) + " = " + bm([[3, 5], [-5, 8]]) + r"$. Then $f(P) = P^2 - 5P + 6I = " + bm([["3 - 10 + 6", "5 - 5"], ["-5 + 5", "8 - 15 + 6"]]) + " = " + bm([[-1, 0], [0, -1]]) + "$.",
  r"Interpreting the constant term of a matrix polynomial as a scalar added to each entry.",
  "U03-A-matrix-polynomial", "One product and a linear combination with the $6I$ convention.",
  check=_c031, values=[M([[-1, 0], [0, -1]]), M([[-1, 6], [6, -1]]), M([[0, -4], [6, 0]]), M([[-7, 0], [0, -7]])],
  cognitive="Application", source_class=SC)


def _P_id():
    P = M([[2, -2], [1, -1]])
    assert P * P == P
    return P


def _c032():
    P = _P_id()
    return (eye(2) - 2 * P) ** 2027


q("U03-A-032", "Types of matrices", "Idempotent matrix gives an involutory matrix", "Medium",
  "Conceptual/application MCQ",
  r"Let $P$ be a square matrix with $P^2 = P$, $P \ne O$ and $P \ne I$, where $I$ is the identity matrix of the same order. Then $(I - 2P)^{2027}$ equals",
  r"$I - 2P$",
  [(r"$I$", r"Finds $(I - 2P)^2 = I$ but then takes every power, including odd ones, to be $I$."),
   (r"$I - 4054P$", r"Keeps only the first-order term of the binomial expansion, $I + 2027(-2P)$."),
   (r"$2P - I$", r"Finds $(I - 2P)^2 = I$ but then reduces as if $(I - 2P)^2 = -I$, giving $(-1)^{1013}(I - 2P)$.")],
  r"$(I - 2P)^2 = I - 4P + 4P^2 = I - 4P + 4P = I$. Hence $(I - 2P)^{2027} = \left[(I - 2P)^2\right]^{1013}(I - 2P) = I - 2P$.",
  "Not exploiting $Q^2 = I$ to reduce an odd power.",
  "U03-A-idempotent-involutory", "Two ideas: idempotence gives an involutory matrix, then parity of the exponent.",
  check=_c032, values=[eye(2) - 2 * _P_id(), eye(2), eye(2) - 4054 * _P_id(), 2 * _P_id() - eye(2)],
  cognitive="Analysis", source_class=SC)


def _c033():
    Sm = M([[4, 6], [6, -2]]); Km = M([[0, 2], [-2, 0]])
    X = Matrix(2, 2, symbols('x0:4'))
    s = solve(list(X + X.T - Sm) + list(X - X.T - Km), list(X), dict=True)[0]
    return X.subs(s)


q("U03-A-033", "Transpose and symmetric matrices", "Recovering a matrix from P + P^T and P - P^T", "Medium",
  "Single-step computation MCQ",
  r"If $P + P^T = " + bm([[4, 6], [6, -2]]) + r"$ and $P - P^T = " + bm([[0, 2], [-2, 0]]) + r"$, then $P$ equals",
  "$" + bm([[2, 4], [2, -1]]) + "$",
  [("$" + bm([[2, 2], [4, -1]]) + "$", r"Subtracts the second equation from the first, which gives $2P^T$, and halves it."),
   ("$" + bm([[4, 8], [4, -2]]) + "$", r"Adds the two equations but does not divide by 2."),
   ("$" + bm([[2, 3], [3, -1]]) + "$", r"Keeps only the symmetric part $\frac{1}{2}(P + P^T)$.")],
  r"Adding the equations, $2P = " + bm([[4, 8], [4, -2]]) + r"$, so $P = " + bm([[2, 4], [2, -1]]) + r"$. Check: $P^T = " + bm([[2, 2], [4, -1]]) + r"$ satisfies both equations.",
  r"Mixing up which combination gives $P$ and which gives $P^T$.",
  "U03-A-sym-skew-recover", "Adding equations and halving; two short steps.",
  check=_c033, values=[M([[2, 4], [2, -1]]), M([[2, 2], [4, -1]]), M([[4, 8], [4, -2]]), M([[2, 3], [3, -1]])],
  cognitive="Application", source_class=SC)


def _c034():
    P = M([[1, 2, 0], [0, -1, 3]]); Q = M([[2, 1], [1, 0], [-1, 4]])
    return (Q * P).trace()


q("U03-A-034", "Algebra of matrices", "Trace of a product of rectangular matrices", "Medium",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[1, 2, 0], [0, -1, 3]]) + r"$ and $Q = " + bm([[2, 1], [1, 0], [-1, 4]]) + r"$. Then the trace of the $3 \times 3$ matrix $QP$ equals",
  r"$16$",
  [(r"$13$", r"Computes $PQ = " + bm([[4, 1], [-4, 12]]) + r"$ and adds all its entries instead of the diagonal."),
   (r"$4$", r"Adds only the first two diagonal entries of $QP$, $2 + 2$, forgetting the third."),
   (r"$-3$", r"Computes $PQ$ and adds its off-diagonal entries $1 + (-4)$.")],
  r"Either compute the diagonal of $QP$: $2(1) + 1(0) = 2$, $1(2) + 0(-1) = 2$, $-1(0) + 4(3) = 12$, total $16$; or use $\operatorname{tr}(QP) = \operatorname{tr}(PQ)$ with $PQ = " + bm([[4, 1], [-4, 12]]) + r"$, trace $16$.",
  r"Not knowing $\operatorname{tr}(QP) = \operatorname{tr}(PQ)$ and then slipping in the larger product.",
  "U03-A-trace-cyclic", "Choose the efficient route via the cyclic property; a few products.",
  check=_c034, values=[16, 13, 4, -3], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 2, 0], [0, -1, 3]]) + r"$ and $Q = " + bm([[2, 1], [1, 0], [-1, 4]]) + r"$. Then the trace of the $3 \times 3$ matrix $QP$ is", answer=16))


def _c035():
    S = M([[1, 2, 0], [2, -1, 3], [0, 3, 4]]); K = M([[0, 1, -2], [-1, 0, 5], [2, -5, 0]])
    assert S.T == S and K.T == -K
    T1 = S * K - K * S; T2 = S * K + K * S
    lam, mu = symbols('lam mu')
    l = solve(list(T1.T - lam * T1), lam)
    m = solve(list(T2.T - mu * T2), mu)
    l = l[lam] if isinstance(l, dict) else l[0]
    m = m[mu] if isinstance(m, dict) else m[0]
    return (l, m)


q("U03-A-035", "Transpose and symmetric matrices", "Transpose of PQ - QP and PQ + QP", "Medium",
  "Conceptual/application MCQ",
  r"Let $P$ be a symmetric matrix and $Q$ a skew-symmetric matrix of the same order such that $PQ - QP$ and $PQ + QP$ are both non-zero. If $(PQ - QP)^T = \lambda(PQ - QP)$ and $(PQ + QP)^T = \mu(PQ + QP)$, then $(\lambda, \mu)$ equals",
  r"$(1, -1)$",
  [(r"$(-1, 1)$", r"Swaps the two conclusions, taking $PQ - QP$ skew-symmetric and $PQ + QP$ symmetric."),
   (r"$(1, 1)$", r"Transposes each product in place as if both matrices were symmetric, $(PQ)^T = PQ$ and $(QP)^T = QP$, so both combinations look symmetric."),
   (r"$(-1, -1)$", r"Transposes a product without reversing order: $(PQ)^T = P^T Q^T = -PQ$.")],
  r"$(PQ)^T = Q^T P^T = -QP$ and $(QP)^T = P^T Q^T = -PQ$. So $(PQ - QP)^T = -QP + PQ = PQ - QP$, giving $\lambda = 1$, and $(PQ + QP)^T = -QP - PQ = -(PQ + QP)$, giving $\mu = -1$.",
  "Dropping the reversal of order or the sign from $Q^T = -Q$.",
  "U03-A-transpose-sym-skew-products", "Two transposes of products with sign tracking.",
  check=_c035, values=[(1, -1), (-1, 1), (1, 1), (-1, -1)], cognitive="Analysis", source_class=SC)


def _c036():
    P = M([[1, 2], [0, 1]])
    S = zeros(2); Pk = eye(2)
    for n in range(1, 60):
        Pk = Pk * P; S = S + Pk
        if S[0, 1] == 30:
            return n


q("U03-A-036", "Powers of matrices", "Sum of successive powers", "Medium",
  "Inverse/parameter MCQ",
  r"Let $P = " + bm([[1, 2], [0, 1]]) + r"$ and $S_n = P + P^2 + \cdots + P^n$. If the entry in the first row and second column of $S_n$ is $30$, then $n$ equals",
  r"$5$",
  [(r"$4$", r"Takes the $(1,2)$ entry of $P^k$ as $2^k$, so $2^{n+1} - 2 = 30$."),
   (r"$6$", r"Takes the $(1,2)$ entry of $P^k$ as $2(k-1)$, so $n(n-1) = 30$."),
   (r"$15$", r"Takes the $(1,2)$ entry of every power as $2$, so $2n = 30$.")],
  r"$P^k = " + bm([[1, "2k"], [0, 1]]) + r"$, so the $(1,2)$ entry of $S_n$ is $2(1 + 2 + \cdots + n) = n(n+1)$. Setting $n(n+1) = 30$ gives $n = 5$ (the positive root).",
  "Wrong general term for the powers.",
  "U03-A-power-sum", "Pattern of powers plus an arithmetic series and a quadratic.",
  check=_c036, values=[5, 4, 6, 15], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 2], [0, 1]]) + r"$ and $S_n = P + P^2 + \cdots + P^n$. If the entry in the first row and second column of $S_n$ is $30$, then the value of $n$ is", answer=5))


def _c037():
    a, b = symbols('a b')
    P = M([[2, -1], [3, -2]]); Q = M([[a, 1], [b, -1]])
    s = solve(list((P + Q) ** 2 - P ** 2 - Q ** 2), [a, b], dict=True)
    assert len(s) == 1
    return s[0][a] + s[0][b]


q("U03-A-037", "Algebra of matrices", "Square of a sum: anticommuting condition", "Medium",
  "Inverse/parameter MCQ",
  r"Let $P = " + bm([[2, -1], [3, -2]]) + r"$ and $Q = " + bm([["a", 1], ["b", -1]]) + r"$, where $a, b \in \mathbb{R}$. If $(P + Q)^2 = P^2 + Q^2$, then $a + b$ equals",
  r"$8$",
  [(r"$-8$", r"Imposes $PQ = QP$ instead of $PQ + QP = O$, giving $a = -5$, $b = -3$."),
   (r"$-6$", r"Sign slip in the $(2,2)$ entry of $QP$, writing $b + 2$ for $-b + 2$, so $7 + b = 0$."),
   (r"$2$", r"Sign slip in the $(1,1)$ entry of $QP$, writing $2a - 3$ for $2a + 3$, so $b = 4a - 3 = 1$.")],
  r"$(P+Q)^2 = P^2 + PQ + QP + Q^2$, so the condition is $PQ + QP = O$. Here $PQ = " + bm([["2a - b", 3], ["3a - 2b", 5]]) + r"$ and $QP = " + bm([["2a + 3", "-a - 2"], ["2b - 3", "-b + 2"]]) + r"$, so $PQ + QP = " + bm([["4a - b + 3", "1 - a"], ["3a - 3", "7 - b"]]) + r" = O$. Thus $a = 1$, $b = 7$ and $a + b = 8$.",
  r"Using $2PQ$ (commuting) in place of $PQ + QP$.",
  "U03-A-anticommute-param", "Two products, a sum, and four entry equations.",
  check=_c037, values=[8, -8, -6, 2], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[2, -1], [3, -2]]) + r"$ and $Q = " + bm([["a", 1], ["b", -1]]) + r"$, where $a, b \in \mathbb{R}$. If $(P + Q)^2 = P^2 + Q^2$, then the value of $a + b$ is", answer=8))


def _c038():
    x = symbols('x')
    R = M([[1, x, 1]]); Mm = M([[1, 0, 2], [2, 1, 0], [0, 3, 1]]); C = M([[1], [x], [1]])
    e = expand((R * Mm * C)[0])
    r = solve(e, x)
    return Mul(*r)


q("U03-A-038", "Algebra of matrices", "Row matrix times square matrix times column matrix", "Medium",
  "Multi-step computation MCQ",
  r"If $" + bm([[1, "x", 1]]) + bm([[1, 0, 2], [2, 1, 0], [0, 3, 1]]) + bm([[1], ["x"], [1]]) + r" = O$, where $O$ is the $1 \times 1$ null matrix, then the product of all real values of $x$ is",
  r"$4$",
  [(r"$-5$", r"Gives the sum of the roots of $x^2 + 5x + 4 = 0$ instead of the product."),
   (r"$3$", r"Drops the $1 \cdot 1$ term in the third entry of the row product, getting $x^2 + 5x + 3 = 0$."),
   (r"$-4$", r"Takes the product of the roots as $-\frac{c}{a}$.")],
  r"The row product is $" + bm([[1, "x", 1]]) + bm([[1, 0, 2], [2, 1, 0], [0, 3, 1]]) + " = " + bm([["1 + 2x", "x + 3", 3]]) + r"$. Multiplying by the column gives $(1 + 2x) + x(x + 3) + 3 = x^2 + 5x + 4$. Setting this to $0$ gives $x = -1$ or $x = -4$, whose product is $4$.",
  "Arithmetic slips in a triple product, or confusing sum and product of roots.",
  "U03-A-row-matrix-column", "Two products giving a quadratic, then roots.",
  check=_c038, values=[4, -5, 3, -4], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $" + bm([[1, "x", 1]]) + bm([[1, 0, 2], [2, 1, 0], [0, 3, 1]]) + bm([[1], ["x"], [1]]) + r" = O$, where $O$ is the $1 \times 1$ null matrix, then the product of all real values of $x$ is", answer=4))


def _c039():
    P = M([[0, 1, -2], [-1, 0, 3], [2, -3, 0]])
    assert P.T == -P
    return (P ** 2).trace()


q("U03-A-039", "Transpose and symmetric matrices", "Trace of the square of a skew-symmetric matrix", "Medium",
  "Single-step computation MCQ",
  r"Let $P = [p_{ij}]$ be a $3 \times 3$ skew-symmetric matrix with $p_{12} = 1$, $p_{13} = -2$ and $p_{23} = 3$. Then the trace of $P^2$ equals",
  r"$-28$",
  [(r"$28$", r"Uses $p_{ij} p_{ji} = p_{ij}^2$, forgetting the sign from skew-symmetry."),
   (r"$-14$", r"Adds each product $p_{ij}p_{ji}$ only once instead of twice."),
   (r"$14$", r"Both forgets the sign and counts each pair once.")],
  r"The $(i,i)$ entry of $P^2$ is $\sum_j p_{ij}p_{ji} = -\sum_j p_{ij}^2$. Summing over $i$, each above-diagonal entry appears twice, so $\operatorname{tr}(P^2) = -2(1^2 + 2^2 + 3^2) = -28$.",
  r"Forgetting $p_{ji} = -p_{ij}$ inside the product.",
  "U03-A-skew-square-trace", "Structure of a skew-symmetric square, summed carefully.",
  check=_c039, values=[-28, 28, -14, 14], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = [p_{ij}]$ be a $3 \times 3$ skew-symmetric matrix with $p_{12} = 1$, $p_{13} = -2$ and $p_{23} = 3$. Then the trace of $P^2$ is", answer=-28))


def _c040():
    P = M([[0, 1, -1], [4, -3, 4], [3, -3, 4]])
    k = symbols('k')
    E = (eye(3) + P) ** 10 - k * (eye(3) + P)
    return solve(E[0, 0], k)[0] if all(simplify(e.subs(k, solve(E[0, 0], k)[0])) == 0 for e in E) else None


q("U03-A-040", "Types of matrices", "Involutory matrix: binomial power", "Medium",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[0, 1, -1], [4, -3, 4], [3, -3, 4]]) + r"$. If $(I + P)^{10} = k(I + P)$, where $I$ is the $3 \times 3$ identity matrix, then $k$ equals",
  r"$512$",
  [(r"$1024$", r"Uses $(I + P)^n = 2^n (I + P)$ instead of $2^{n-1}(I+P)$."),
   (r"$256$", r"Uses $2^{n-2}$, an off-by-one in the other direction."),
   (r"$10$", r"Adds instead of multiplying: treats each power as adding one copy of $I + P$.")],
  r"Direct multiplication gives $P^2 = I$. Then $(I + P)^2 = I + 2P + P^2 = 2(I + P)$, and by induction $(I + P)^n = 2^{n-1}(I + P)$. So $(I + P)^{10} = 2^9 (I + P)$ and $k = 512$.",
  "Off-by-one in the exponent after finding $(I+P)^2 = 2(I+P)$.",
  "U03-A-involutory-binomial", "Verify $P^2 = I$, then a binomial reduction and induction.",
  check=_c040, values=[512, 1024, 256, 10], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[0, 1, -1], [4, -3, 4], [3, -3, 4]]) + r"$. If $(I + P)^{10} = k(I + P)$, where $I$ is the $3 \times 3$ identity matrix, then the value of $k$ is", answer=512))


def _c041():
    return sum(1 for t in _iprod([0, 1, 2], repeat=4) if Matrix(2, 2, t) ** 2 == Matrix(2, 2, t))


q("U03-A-041", "Counting matrices", "Number of idempotent 2 by 2 matrices", "Medium",
  "Multi-step computation MCQ",
  r"The number of $2 \times 2$ matrices $P$ with all entries from $\{0, 1, 2\}$ such that $P^2 = P$ is",
  r"$12$",
  [(r"$10$", r"Counts only the trace-one case and forgets $P = O$ and $P = I$."),
   (r"$14$", r"In each trace-one case counts the pairs with $bc = 0$ as $3 + 3$, double counting $b = c = 0$."),
   (r"$4$", r"Considers only diagonal matrices: $O$, $I$, $\operatorname{diag}(1, 0)$, $\operatorname{diag}(0, 1)$.")],
  r"Let $P = " + bm([["a", "b"], ["c", "d"]]) + r"$. Comparing entries of $P^2 = P$ gives $b(a + d - 1) = 0$, $c(a + d - 1) = 0$, $a^2 + bc = a$ and $d^2 + bc = d$. If $a + d \ne 1$, then $b = c = 0$ and $a^2 = a$, $d^2 = d$, so $a, d \in \{0, 1\}$ with $a = d$ (since $a + d \ne 1$): only $O$ and $I$. If $a + d = 1$, then $bc = a - a^2 = a(1 - a) = ad$; with entries in $\{0,1,2\}$, $a + d = 1$ forces $(a, d) = (1, 0)$ or $(0, 1)$, so $ad = 0$ and $bc = 0$: $5$ pairs $(b, c)$ each, giving $10$. Total $10 + 2 = 12$.",
  r"Missing the trivial idempotents or double counting $bc = 0$ pairs.",
  "U03-A-count-idempotent", "Entry equations, case split, careful counting.",
  check=_c041, values=[12, 10, 14, 4], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The number of $2 \times 2$ matrices $P$ with all entries from $\{0, 1, 2\}$ such that $P^2 = P$ is", answer=12))


def _c042():
    lam = symbols('lambda')
    X = Matrix(2, 2, symbols('x0:4'))
    E = X.T - lam * X
    A_, _ = linear_eq_to_matrix(list(E), list(X))
    return FiniteSet(*solve(A_.det(), lam))


q("U03-A-042", "Transpose and symmetric matrices", "Matrices with transpose a scalar multiple", "Medium",
  "Conceptual/application MCQ",
  r"If $P$ is a non-zero square matrix and $\lambda$ is a real number such that $P^T = \lambda P$, then the set of all possible values of $\lambda$ is",
  r"$\{-1, 1\}$",
  [(r"$\{1\}$", r"Considers only symmetric matrices."),
   (r"$\{-1\}$", r"Considers only skew-symmetric matrices."),
   (r"$\{-1, 0, 1\}$", r"Includes $\lambda = 0$, overlooking that $P^T = O$ forces $P = O$.")],
  r"Transposing $P^T = \lambda P$ gives $P = \lambda P^T = \lambda^2 P$, so $(\lambda^2 - 1)P = O$ and, since $P \ne O$, $\lambda^2 = 1$. Both values occur: $\lambda = 1$ for a non-zero symmetric matrix and $\lambda = -1$ for a non-zero skew-symmetric one.",
  r"Not transposing the relation a second time to get $\lambda^2 = 1$.",
  "U03-A-transpose-scalar", "Apply transpose twice and check both values are attained.",
  check=_c042, values=[FiniteSet(-1, 1), FiniteSet(1), FiniteSet(-1), FiniteSet(-1, 0, 1)],
  cognitive="Analysis", source_class=SC)

# ================================================================ DIFFICULT (13)


def _c043():
    return sum(1 for t in _iprod([0, 1, 2], repeat=9) if sum(v * v for v in t) == 6)


q("U03-A-043", "Counting matrices", "Counting with the trace of P P^T", "Difficult",
  "Multi-step computation MCQ",
  r"The number of $3 \times 3$ matrices $P$ with all entries from $\{0, 1, 2\}$ such that the trace of $P P^T$ equals $6$ is",
  r"$336$",
  [(r"$84$", r"Considers only the case of six entries equal to $1$, missing $4 + 1 + 1$."),
   (r"$252$", r"Considers only the case $4 + 1 + 1$, missing six entries equal to $1$."),
   (r"$588$", r"In the $4 + 1 + 1$ case places the two 1s as an ordered pair ($9 \times 8 \times 7 = 504$), then adds $84$.")],
  r"$\operatorname{tr}(P P^T)$ is the sum of the squares of all nine entries, each square being $0$, $1$ or $4$. A total of $6$ arises as $1 \times 6$ (six entries equal to $1$, the rest $0$): $\binom{9}{6} = 84$ ways; or $4 + 1 + 1$ (one entry $2$ and two entries $1$): $9 \times \binom{8}{2} = 252$ ways. Total $84 + 252 = 336$.",
  "Missing a case in the decomposition of the sum of squares.",
  "U03-A-count-trace-PPT", "Recognise $\\operatorname{tr}(PP^T)$ as a sum of squares, then two-case counting.",
  check=_c043, values=[336, 84, 252, 588], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The number of $3 \times 3$ matrices $P$ with all entries from $\{0, 1, 2\}$ such that the trace of $P P^T$ equals $6$ is", answer=336))


def _c044():
    return sum(1 for t in _iprod([-1, 0, 1], repeat=4) if Matrix(2, 2, t) ** 2 == eye(2))


q("U03-A-044", "Counting matrices", "Number of involutory 2 by 2 matrices", "Difficult",
  "Multi-step computation MCQ",
  r"The number of $2 \times 2$ matrices $P$ with all entries from $\{-1, 0, 1\}$ such that $P^2 = I$ is",
  r"$14$",
  [(r"$12$", r"Counts only the trace-zero solutions and forgets $P = I$ and $P = -I$."),
   (r"$13$", r"Includes $P = I$ but forgets $P = -I$."),
   (r"$10$", r"Counts only trace-zero matrices with $a = \pm 1$, missing $a = 0$ and the two scalar matrices.")],
  r"Let $P = " + bm([["a", "b"], ["c", "d"]]) + r"$. $P^2 = I$ gives $b(a + d) = 0$, $c(a + d) = 0$, $a^2 + bc = 1$, $d^2 + bc = 1$. If $a + d \ne 0$ then $b = c = 0$ and $a^2 = d^2 = 1$ with $a = d$: $P = \pm I$ (2 matrices). If $a + d = 0$: for $a = \pm 1$ we need $bc = 0$, $5$ pairs each, giving $10$; for $a = 0$ we need $bc = 1$, i.e. $(1, 1)$ or $(-1, -1)$, giving $2$. Total $2 + 10 + 2 = 14$.",
  "Missing the scalar solutions or the $a = 0$ case.",
  "U03-A-count-involutory", "Entry equations with casework on the trace.",
  check=_c044, values=[14, 12, 13, 10], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The number of $2 \times 2$ matrices $P$ with all entries from $\{-1, 0, 1\}$ such that $P^2 = I$ is", answer=14))


def _c045():
    P = M([[1, 0, 0], [2, 0, 1], [0, 1, 0]])
    Q = P ** 50
    assert Q[0, :] == M([[1, 0, 0]]) and Q[1, 1:] == M([[1, 0]]) and Q[2, 1:] == M([[0, 1]])
    return Q[1, 0] + Q[2, 0]


q("U03-A-045", "Powers of matrices", "High power via a recurrence", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[1, 0, 0], [2, 0, 1], [0, 1, 0]]) + r"$. If $P^{50} = " + bm([[1, 0, 0], [r"\alpha", 1, 0], [r"\beta", 0, 1]]) + r"$, then $\alpha + \beta$ equals",
  r"$100$",
  [(r"$50$", r"Recalls the result for the similar matrix with $(2,1)$ entry $1$, where the corresponding entries are $25$ each."),
   (r"$200$", r"Finds $P^2 = I + N$ with $N^2 = O$ but then writes $P^{50} = I + 50N$, using the exponent $50$ instead of $25$, giving $100$ each."),
   (r"$98$", r"Off by one: uses the first-column entries $50$ and $48$ of $P^{49}$.")],
  r"Compute $P^2 = " + bm([[1, 0, 0], [2, 1, 0], [2, 0, 1]]) + r"$, which is $I + N$ with $N = " + bm([[0, 0, 0], [2, 0, 0], [2, 0, 0]]) + r"$ and $N^2 = O$. Hence $P^{50} = (I + N)^{25} = I + 25N = " + bm([[1, 0, 0], [50, 1, 0], [50, 0, 1]]) + r"$, so $\alpha + \beta = 100$.",
  "Extrapolating a pattern from two data points instead of proving it.",
  "U03-A-power-recursive", "Non-obvious route: square first, then identity plus nilpotent.",
  check=_c045, values=[100, 50, 200, 98], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 0, 0], [2, 0, 1], [0, 1, 0]]) + r"$. If $P^{50} = " + bm([[1, 0, 0], [r"\alpha", 1, 0], [r"\beta", 0, 1]]) + r"$, then the value of $\alpha + \beta$ is", answer=100))


def _c046():
    P = M([[1, 2], [-1, -1]])
    k = symbols('k')
    E = (eye(2) + P) ** 8 - k * eye(2)
    s = solve(E[0, 0], k)[0]
    assert all(e.subs(k, s) == 0 for e in E)
    return s


q("U03-A-046", "Powers of matrices", "Matrix with square equal to minus identity", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[1, 2], [-1, -1]]) + r"$ and let $I$ be the $2 \times 2$ identity matrix. If $(I + P)^8 = kI$, then $k$ equals",
  r"$16$",
  [(r"$-16$", r"Sign slip: takes $P^4 = -I$ from $P^2 = -I$."),
   (r"$256$", r"Treats $P$ as the scalar $1$, computing $(1 + 1)^8$."),
   (r"$8$", r"Finds $(I + P)^2 = 2P$ but evaluates $(2P)^4$ as $2 \times 4 \, P^4$.")],
  r"$P^2 = " + bm([["1 - 2", "2 - 2"], ["-1 + 1", "-2 + 1"]]) + r" = -I$. Hence $(I + P)^2 = I + 2P + P^2 = 2P$, and $(I + P)^8 = (2P)^4 = 16P^4 = 16(P^2)^2 = 16I$. So $k = 16$.",
  r"Mishandling powers of a matrix with $P^2 = -I$.",
  "U03-A-square-minus-identity", "Find $P^2 = -I$, then a non-obvious reduction of $(I+P)^2$.",
  check=_c046, values=[16, -16, 256, 8], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 2], [-1, -1]]) + r"$ and let $I$ be the $2 \times 2$ identity matrix. If $(I + P)^8 = kI$, then the value of $k$ is", answer=16))


def _c047():
    P = M([[2, 1, 0], [0, 2, 1], [0, 0, 2]])
    return (P ** 6)[0, 2]


q("U03-A-047", "Powers of matrices", "Scalar plus nilpotent: binomial expansion", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[2, 1, 0], [0, 2, 1], [0, 0, 2]]) + r"$. The entry in the first row and third column of $P^6$ is",
  r"$240$",
  [(r"$192$", r"Uses the first-order term $6 \cdot 2^5 N$ only, which gives the $(1,2)$ entry, not the $(1,3)$ entry."),
   (r"$120$", r"Uses $\binom{6}{2} 2^3$, an exponent slip in $2^{n-2}$."),
   (r"$64$", r"Takes the corner entry from the diagonal pattern $2^6$.")],
  r"Write $P = 2I + N$ with $N = " + bm([[0, 1, 0], [0, 0, 1], [0, 0, 0]]) + r"$, $N^2$ having a single $1$ in position $(1,3)$ and $N^3 = O$. As $2I$ and $N$ commute, $P^6 = 2^6 I + 6 \cdot 2^5 N + \binom{6}{2} 2^4 N^2$. The $(1,3)$ entry comes only from the last term: $15 \times 16 = 240$.",
  "Not tracking which power of $N$ contributes to which position.",
  "U03-A-power-scalar-plus-nilpotent", "Decompose, binomial with commuting terms, locate the entry.",
  check=_c047, values=[240, 192, 120, 64], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[2, 1, 0], [0, 2, 1], [0, 0, 2]]) + r"$. The entry in the first row and third column of $P^6$ is", answer=240))


def _c048():
    a, b, c = symbols('a b c', real=True)
    P = M([[a, b, c], [b, c, a], [c, a, b]])
    E = P.T * P - eye(3)
    # elementary symmetric functions from the conditions
    e1, e2 = symbols('e1 e2')
    sq = E[0, 0] + 1        # a^2 + b^2 + c^2
    cr = E[0, 1]            # ab + bc + ca
    s = solve([e1 ** 2 - 2 * e2 - 1, e2], [e1, e2], dict=True)
    s = [d for d in s if d[e1] > 0][0]
    e3 = Rational(-4, 27)
    p3 = s[e1] ** 3 - 3 * s[e1] * s[e2] + 3 * e3
    # confirm a real triple exists and gives the same value
    tri = {a: Rational(2, 3), b: Rational(2, 3), c: Rational(-1, 3)}
    assert E.subs(tri) == zeros(3) and (a * b * c).subs(tri) == e3
    assert (a ** 3 + b ** 3 + c ** 3).subs(tri) == p3
    return p3


q("U03-A-048", "Types of matrices", "Orthogonal circulant matrix", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([["a", "b", "c"], ["b", "c", "a"], ["c", "a", "b"]]) + r"$, where $a, b, c$ are real numbers with $a + b + c > 0$ and $abc = -\frac{4}{27}$. If $P^T P = I$, then $a^3 + b^3 + c^3$ equals",
  r"$\frac{5}{9}$",
  [(r"$\frac{13}{9}$", r"Uses $a^3 + b^3 + c^3 = (a+b+c)(\cdots) - 3abc$, a sign slip in the identity."),
   (r"$-\frac{13}{9}$", r"Takes $a + b + c = -1$, ignoring the condition $a + b + c > 0$."),
   (r"$-\frac{4}{9}$", r"Reads the off-diagonal entries of $P^T P$ as $1$, so $a^2 + b^2 + c^2 - (ab + bc + ca) = 0$, leaving only $3abc$.")],
  r"$P^T P$ has diagonal entries $a^2 + b^2 + c^2$ and off-diagonal entries $ab + bc + ca$, so $a^2 + b^2 + c^2 = 1$ and $ab + bc + ca = 0$. Then $(a + b + c)^2 = 1$, and $a + b + c > 0$ gives $a + b + c = 1$. Using $a^3 + b^3 + c^3 - 3abc = (a + b + c)(a^2 + b^2 + c^2 - ab - bc - ca) = 1$, we get $a^3 + b^3 + c^3 = 1 + 3\left(-\frac{4}{27}\right) = \frac{5}{9}$. (For instance $a = b = \frac{2}{3}$, $c = -\frac{1}{3}$.)",
  "Sign slips in the identity for $a^3 + b^3 + c^3 - 3abc$.",
  "U03-A-orthogonal-circulant", "Translate orthogonality into symmetric functions, then an algebraic identity.",
  check=_c048, values=[Rational(5, 9), Rational(13, 9), Rational(-13, 9), Rational(-4, 9)],
  cognitive="Analysis", source_class=SC)


def _c049():
    return sum(1 for t in _iprod([-1, 0, 1], repeat=9) if Matrix(3, 3, t) * Matrix(3, 3, t).T == eye(3))


q("U03-A-049", "Counting matrices", "Counting orthogonal matrices with small entries", "Difficult",
  "Multi-step computation MCQ",
  r"The number of $3 \times 3$ matrices $P$ with all entries from $\{-1, 0, 1\}$ such that $P P^T = I$ is",
  r"$48$",
  [(r"$6$", r"Counts only permutation matrices with entries $0$ and $1$, ignoring the sign choices."),
   (r"$8$", r"Counts only diagonal matrices with entries $\pm 1$."),
   (r"$12$", r"Allows only an overall sign $\pm 1$ for each permutation matrix, $6 \times 2$.")],
  r"$P P^T = I$ means each row has squared length $1$, so each row has exactly one non-zero entry, equal to $\pm 1$; distinct rows must be orthogonal, so their non-zero entries lie in different columns. Hence $P$ is a permutation matrix with each $1$ replaced by $\pm 1$: $3! \times 2^3 = 48$.",
  "Ignoring independent sign choices in each row.",
  "U03-A-count-orthogonal", "Translate $PP^T = I$ into structure, then count permutations and signs.",
  check=_c049, values=[48, 6, 8, 12], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The number of $3 \times 3$ matrices $P$ with all entries from $\{-1, 0, 1\}$ such that $P P^T = I$ is", answer=48))


def _c050():
    return sum(1 for t in _iprod(range(-2, 3), repeat=4) if Matrix(2, 2, t) ** 2 == zeros(2))


q("U03-A-050", "Counting matrices", "Number of nilpotent 2 by 2 matrices", "Difficult",
  "Multi-step computation MCQ",
  r"The number of $2 \times 2$ matrices $P$ with all entries from $\{-2, -1, 0, 1, 2\}$ such that $P^2 = O$ is",
  r"$17$",
  [(r"$9$", r"Considers only $a = d = 0$ with $bc = 0$."),
   (r"$13$", r"Handles $a = 0$ and $a = \pm 1$ but misses $a = \pm 2$ with $bc = -4$."),
   (r"$25$", r"Takes $P^2 = O$ to mean only $a = d = 0$, leaving $b$ and $c$ free.")],
  r"For $P = " + bm([["a", "b"], ["c", "d"]]) + r"$, $P^2 = O$ gives $b(a + d) = 0$, $c(a + d) = 0$, $a^2 + bc = 0$, $d^2 + bc = 0$. If $a + d \ne 0$ then $b = c = 0$ and $a = d = 0$, a contradiction; so $d = -a$ and $bc = -a^2$. $a = 0$: $bc = 0$, $9$ pairs. $a = \pm 1$: $bc = -1$, pairs $(1, -1), (-1, 1)$, giving $4$. $a = \pm 2$: $bc = -4$, pairs $(2, -2), (-2, 2)$, giving $4$. Total $17$.",
  "Missing cases with non-zero diagonal.",
  "U03-A-count-nilpotent", "Derive the conditions, then three-case counting.",
  check=_c050, values=[17, 9, 13, 25], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The number of $2 \times 2$ matrices $P$ with all entries from $\{-2, -1, 0, 1, 2\}$ such that $P^2 = O$ is", answer=17))


def _c051():
    c = 0
    for a, b, d in _iprod(range(-2, 3), repeat=3):
        P = M([[0, a, b], [-a, 0, d], [-b, -d, 0]])
        if (P ** 2).trace() == -4:
            c += 1
    return c


q("U03-A-051", "Counting matrices", "Skew-symmetric matrices with a given trace of the square", "Difficult",
  "Multi-step computation MCQ",
  r"The number of $3 \times 3$ skew-symmetric matrices $P$ with all entries from $\{-2, -1, 0, 1, 2\}$ such that the trace of $P^2$ equals $-4$ is",
  r"$12$",
  [(r"$6$", r"Uses $\operatorname{tr}(P^2) = -(p_{12}^2 + p_{13}^2 + p_{23}^2)$, missing the factor $2$, and counts one entry $\pm 2$."),
   (r"$3$", r"Chooses the two non-zero positions but ignores the sign choices."),
   (r"$24$", r"Chooses the two non-zero positions as an ordered pair ($6$ ways) with $4$ sign patterns.")],
  r"For a skew-symmetric $P$ with above-diagonal entries $x, y, z$, $\operatorname{tr}(P^2) = -2(x^2 + y^2 + z^2)$. So $x^2 + y^2 + z^2 = 2$, which with entries in $\{-2, \ldots, 2\}$ means exactly two of $x, y, z$ are $\pm 1$ and one is $0$: $\binom{3}{2} \times 2^2 = 12$.",
  r"Forgetting the factor $2$ in $\operatorname{tr}(P^2)$ for skew-symmetric $P$.",
  "U03-A-count-skew-trace", "Structural trace identity, then counting with signs.",
  check=_c051, values=[12, 6, 3, 24], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The number of $3 \times 3$ skew-symmetric matrices $P$ with all entries from $\{-2, -1, 0, 1, 2\}$ such that the trace of $P^2$ equals $-4$ is", answer=12))


def _c052():
    P = M([[1, 1], [0, 2]])
    return sum(1 for t in _iprod(range(4), repeat=4) if P * Matrix(2, 2, t) == Matrix(2, 2, t) * P)


q("U03-A-052", "Counting matrices", "Counting matrices that commute with a given matrix", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[1, 1], [0, 2]]) + r"$. The number of $2 \times 2$ matrices $Q$ with all entries from $\{0, 1, 2, 3\}$ such that $PQ = QP$ is",
  r"$10$",
  [(r"$16$", r"Finds $c = 0$ and $d = a + b$ but lets $a$ and $b$ range freely, ignoring that $d \le 3$."),
   (r"$40$", r"Finds $d = a + b$ but misses the condition $c = 0$, letting $c$ take 4 values."),
   (r"$6$", r"Excludes the four scalar matrices $aI$, counting only $b \ne 0$.")],
  r"For $Q = " + bm([["a", "b"], ["c", "d"]]) + r"$: $PQ = " + bm([["a + c", "b + d"], ["2c", "2d"]]) + r"$ and $QP = " + bm([["a", "a + 2b"], ["c", "c + 2d"]]) + r"$. Equality gives $c = 0$ and $d = a + b$. With $a, b \ge 0$ and $a + b = d \le 3$, the number of pairs $(a, b)$ is $4 + 3 + 2 + 1 = 10$.",
  "Ignoring the range restriction on the dependent entry.",
  "U03-A-count-commuting", "Derive commuting conditions, then a bounded count.",
  check=_c052, values=[10, 16, 40, 6], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $P = " + bm([[1, 1], [0, 2]]) + r"$. The number of $2 \times 2$ matrices $Q$ with all entries from $\{0, 1, 2, 3\}$ such that $PQ = QP$ is", answer=10))


def _c053():
    P = M([[1, 0], [0, 0]]); Q = M([[1, 0], [1, 0]])
    assert P * Q == P and Q * P == Q
    k = symbols('k')
    E = (P + Q) ** 7 - k * (P + Q)
    s = solve(E[0, 0], k)[0]
    assert all(e.subs(k, s) == 0 for e in E)
    return s


q("U03-A-053", "Types of matrices", "Pair of matrices with PQ = P and QP = Q", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P$ and $Q$ be non-zero square matrices of the same order such that $PQ = P$ and $QP = Q$. If $(P + Q)^7 = k(P + Q)$, then $k$ equals",
  r"$64$",
  [(r"$128$", r"Finds $(P+Q)^2 = 2(P+Q)$ but uses $(P+Q)^n = 2^n(P+Q)$."),
   (r"$1$", r"Treats $P + Q$ as idempotent, missing the cross terms $PQ + QP = P + Q$."),
   (r"$32$", r"Uses $(P+Q)^n = 2^{n-2}(P+Q)$, an off-by-one in the exponent.")],
  r"$P^2 = (PQ)P = P(QP) = PQ = P$ and similarly $Q^2 = (QP)Q = Q(PQ) = QP = Q$. Then $(P+Q)^2 = P^2 + PQ + QP + Q^2 = P + P + Q + Q = 2(P+Q)$, so $(P+Q)^n = 2^{n-1}(P+Q)$ and $(P+Q)^7 = 64(P+Q)$. (Here $P + Q \ne O$, since $P = -Q$ would force $Q = O$.)",
  "Missing the hidden idempotence of $P$ and $Q$.",
  "U03-A-idempotent-pair", "Non-obvious route: deduce idempotence, then a square of a sum, then induction.",
  check=_c053, values=[64, 128, 1, 32], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $P$ and $Q$ be non-zero square matrices of the same order such that $PQ = P$ and $QP = Q$. If $(P + Q)^7 = k(P + Q)$, then the value of $k$ is", answer=64))


def _c054():
    th = symbols('theta', real=True)
    R = M([[cos(th), sin(th)], [-sin(th), cos(th)]])
    E = (R ** 3 - R.T).applyfunc(simplify)
    S = Interval.Ropen(0, 2 * pi)
    sol = Intersection(*[solveset(e, th, S) for e in E])
    return len(sol)


q("U03-A-054", "Powers of matrices", "Rotation matrix equation", "Difficult",
  "Multi-step computation MCQ",
  r"Let $R(\theta) = " + bm([[r"\cos\theta", r"\sin\theta"], [r"-\sin\theta", r"\cos\theta"]]) + r"$. The number of values of $\theta$ in $[0, 2\pi)$ for which $R(\theta)^3 = R(\theta)^T$ is",
  r"$4$",
  [(r"$2$", r"Takes $R(\theta)^T = R(\theta)$, solving $3\theta = \theta + 2k\pi$, which gives $\theta = 0, \pi$."),
   (r"$5$", r"Solves $4\theta = 2k\pi$ but counts $k = 0, 1, 2, 3, 4$, including $\theta = 2\pi$."),
   (r"$1$", r"Solves $3\theta = -\theta$ as an equation of angles, without adding multiples of $2\pi$.")],
  r"$R(\alpha)R(\beta) = R(\alpha + \beta)$, so $R(\theta)^3 = R(3\theta)$, and $R(\theta)^T = R(-\theta)$. Thus $R(3\theta) = R(-\theta)$, i.e. $\cos 3\theta = \cos\theta$ and $\sin 3\theta = -\sin\theta$, which means $4\theta = 2k\pi$. In $[0, 2\pi)$: $\theta = 0, \frac{\pi}{2}, \pi, \frac{3\pi}{2}$, so there are $4$ values.",
  "Forgetting periodicity or mis-identifying the transpose of a rotation.",
  "U03-A-rotation-equation", "Combine powers and transpose of rotations with periodic solutions.",
  check=_c054, values=[4, 2, 5, 1], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Let $R(\theta) = " + bm([[r"\cos\theta", r"\sin\theta"], [r"-\sin\theta", r"\cos\theta"]]) + r"$. The number of values of $\theta$ in $[0, 2\pi)$ for which $R(\theta)^3 = R(\theta)^T$ is", answer=4))


def _c055():
    P = M([[2, 1], [1, 2]])
    b20 = (P ** 20)[0, 1]
    # (last three digits, value): harness compares numbers with a relative tolerance, and the key and the diagonal-entry distractor differ by 1
    return (b20 % 1000, b20)


q("U03-A-055", "Powers of matrices", "Powers of a symmetric 2 by 2 matrix via sum and difference", "Difficult",
  "Multi-step computation MCQ",
  r"Let $P = " + bm([[2, 1], [1, 2]]) + r"$. The entry in the first row and second column of $P^{20}$ is",
  r"$\frac{3^{20} - 1}{2}$",
  [(r"$\frac{3^{20} + 1}{2}$", r"Gives the diagonal entry $\frac{3^{20} + 1}{2}$ instead of the off-diagonal one."),
   (r"$3^{19}$", r"Assumes $P^2 = 3P$ because every row sum is $3$, so $P^{20} = 3^{19} P$ with off-diagonal entry $3^{19}$."),
   (r"$20 \cdot 2^{19}$", r"Writes $P = 2I + N$ and assumes $N^2 = O$, keeping only $2^{20} I + 20 \cdot 2^{19} N$; in fact $N^2 = I$.")],
  r"Every power of $P$ has the form $" + bm([[r"\alpha_n", r"\beta_n"], [r"\beta_n", r"\alpha_n"]]) + r"$. Multiplying by $P$ gives $\alpha_{n+1} = 2\alpha_n + \beta_n$ and $\beta_{n+1} = \alpha_n + 2\beta_n$, so $\alpha_{n+1} + \beta_{n+1} = 3(\alpha_n + \beta_n)$ and $\alpha_{n+1} - \beta_{n+1} = \alpha_n - \beta_n$. With $\alpha_1 = 2, \beta_1 = 1$ this gives $\alpha_n + \beta_n = 3^n$ and $\alpha_n - \beta_n = 1$. Hence $\beta_{20} = \frac{3^{20} - 1}{2}$.",
  "Assuming the off-diagonal part is nilpotent, or that $P^2$ is a multiple of $P$.",
  "U03-A-power-symmetric-pattern", "Exponent too large for direct multiplication; needs the sum/difference decoupling (or the binomial expansion with $N^2 = I$), with traps from a false nilpotent split and a false $P^2 = 3P$.",
  check=_c055, values=[(v % 1000, v) for v in [(3 ** 20 - 1) // 2, (3 ** 20 + 1) // 2, 3 ** 19, 20 * 2 ** 19]], cognitive="Analysis", source_class=SC)
