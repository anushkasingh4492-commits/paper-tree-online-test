import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
A_, D_ = symbols('a d')
N_ = Symbol('n', positive=True, integer=True)
T_ = Symbol('t', real=True)


def term(a, d, k):
    return a + (k - 1)*d


def ssum(a, d, k):
    return k*(2*a + (k - 1)*d)/2


def solve_ad(eqs):
    s = solve(eqs, [A_, D_], dict=True)
    assert len(s) == 1
    return s[0][A_], s[0][D_]


def from_S(S, k):
    """k-th term of the sequence whose sum of first n terms is S(n)."""
    return S(k) - S(k - 1) if k > 1 else S(1)


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."
TOPIC = "Arithmetic progression"

# ================================================================ EASY (18)

q("U06-A-001", TOPIC, "nth term", "Easy", "Single-step computation MCQ",
  r"The $25$th term of the arithmetic progression $-3, 1, 5, 9, \ldots$ is",
  r"$93$",
  [(r"$97$", r"Uses $a + nd = -3 + 25(4)$ in place of $a + (n-1)d$."),
   (r"$89$", r"Uses $a + (n-2)d = -3 + 23(4)$, miscounting the number of steps."),
   (r"$99$", r"Takes the first term as $3$, dropping its sign: $3 + 24(4) = 99$.")],
  r"Here $a = -3$ and $d = 4$, so $a_{25} = a + 24d = -3 + 96 = 93$.",
  r"Using $a + nd$ for the $n$th term.",
  "U06-A-nth-term", "Direct use of $a_n = a + (n-1)d$.",
  check=lambda: term(-3, 1 - (-3), 25), values=[93, 97, 89, 99], cognitive="Application",
  numerical=dict(question=r"The $25$th term of the arithmetic progression $-3, 1, 5, 9, \ldots$ is", answer=93))

def _c2():
    return len([j for j in range(1, 200) if term(120, -4, j) > 0])
q("U06-A-002", TOPIC, "Number of positive terms", "Easy", "Single-step computation MCQ",
  r"How many terms of the arithmetic progression $120, 116, 112, \ldots$ are positive?",
  r"$30$",
  [(r"$31$", r"Counts the term $a_{31} = 0$ as positive."),
   (r"$29$", r"Solves $120 - 4n > 0$, using $a + nd$, and takes the largest $n$ below $30$."),
   (r"$32$", r"Gives the position of the first negative term instead of the number of positive terms.")],
  r"$a_n = 120 - 4(n-1) = 124 - 4n > 0$ gives $n < 31$. Since $a_{31} = 0$ is not positive, the positive terms are $a_1, \ldots, a_{30}$, that is $30$ terms.",
  r"Treating the zero term as positive, or mixing up position of the first negative term with the count.",
  "U06-A-count-positive-terms", "One inequality with a boundary term equal to zero.",
  check=_c2, values=[30, 31, 29, 32], cognitive="Application",
  numerical=dict(question=r"The number of positive terms of the arithmetic progression $120, 116, 112, \ldots$ is", answer=30))

def _c3():
    a, d = solve_ad([term(A_, D_, 4) - 11, term(A_, D_, 10) - 29])
    return term(a, d, 20)
q("U06-A-003", TOPIC, "Term from two given terms", "Easy", "Multi-step computation MCQ",
  r"In an arithmetic progression, the $4$th term is $11$ and the $10$th term is $29$. The $20$th term is",
  r"$59$",
  [(r"$62$", r"Finds $a = 2$, $d = 3$ correctly but then uses $a + 20d$."),
   (r"$56$", r"Finds $a = 2$, $d = 3$ but uses $a + 18d$, miscounting the steps."),
   (r"$58$", r"Assumes the term is proportional to its position and doubles $a_{10}$.")],
  r"$a_{10} - a_4 = 6d = 18$, so $d = 3$ and $a = 11 - 3d = 2$. Then $a_{20} = 2 + 19(3) = 59$.",
  r"Treating terms of an AP as proportional to their positions.",
  "U06-A-term-from-two-terms", "Two linear equations, then one substitution.",
  check=_c3, values=[59, 62, 56, 58], cognitive="Application")

q("U06-A-004", TOPIC, "Sum of n terms", "Easy", "Single-step computation MCQ",
  r"The sum of the first $20$ terms of the arithmetic progression $5, 9, 13, \ldots$ is",
  r"$860$",
  [(r"$900$", r"Uses $\frac{n}{2}[2a + nd] = 10(10 + 80)$."),
   (r"$820$", r"Uses $\frac{n}{2}[2a + (n-2)d] = 10(10 + 72)$."),
   (r"$1720$", r"Drops the factor $\frac{1}{2}$: $20(10 + 76)$.")],
  r"$S_{20} = \frac{20}{2}[2(5) + 19(4)] = 10(10 + 76) = 860$.",
  r"Using $nd$ instead of $(n-1)d$ in the sum formula.",
  "U06-A-sum-basic", "Direct use of the sum formula.",
  check=lambda: ssum(5, 4, 20), values=[860, 900, 820, 1720], cognitive="Application")

def _c5():
    S = lambda k: 3*k**2 + 5*k
    return from_S(S, 10)
q("U06-A-005", TOPIC, "nth term from S_n", "Easy", "Single-step computation MCQ",
  r"The sum of the first $n$ terms of a sequence is $S_n = 3n^2 + 5n$. Its $10$th term is",
  r"$62$",
  [(r"$65$", r"Differentiates $S_n$ to get $6n + 5$ and puts $n = 10$."),
   (r"$35$", r"Divides $S_{10} = 350$ by $10$, finding the average of the first ten terms."),
   (r"$68$", r"Computes $S_{11} - S_{10}$, which is the $11$th term.")],
  r"$a_{10} = S_{10} - S_9 = (300 + 50) - (243 + 45) = 350 - 288 = 62$.",
  r"Treating $a_n$ as the derivative of $S_n$.",
  "U06-A-Sn-to-term", "One subtraction $S_n - S_{n-1}$.",
  check=_c5, values=[62, 65, 35, 68], cognitive="Application",
  numerical=dict(question=r"The sum of the first $n$ terms of a sequence is $S_n = 3n^2 + 5n$. The $10$th term of the sequence is", answer=62))

def _c6():
    S = lambda k: 2*k**2 - 7*k
    return simplify(from_S(S, N_ + 2) - from_S(S, N_ + 1))
q("U06-A-006", TOPIC, "Common difference from S_n", "Easy", "Single-step computation MCQ",
  r"If the sum of the first $n$ terms of an arithmetic progression is $2n^2 - 7n$, then its common difference is",
  r"$4$",
  [(r"$2$", r"Reads the coefficient of $n^2$ as the common difference."),
   (r"$-5$", r"Reports $a_1 = S_1 = -5$, the first term."),
   (r"$-7$", r"Reads the coefficient of $n$ as the common difference.")],
  r"$a_n = S_n - S_{n-1} = 2(2n - 1) - 7 = 4n - 9$, so $d = 4$. In general, for $S_n = pn^2 + qn$, $d = 2p$.",
  r"Taking the coefficient of $n^2$ in $S_n$ as $d$ instead of $2p$.",
  "U06-A-Sn-to-d", "One subtraction and reading off a coefficient.",
  check=_c6, values=[4, 2, -5, -7], cognitive="Understanding")

def _c7():
    m, e = symbols('m e', real=True)
    sols = solve([3*m - 27, (m - e)*m*(m + e) - 504], [m, e], dict=True)
    vals = {simplify((s[m] - s[e])**2 + s[m]**2 + (s[m] + s[e])**2) for s in sols}
    assert len(vals) == 1
    return vals.pop()
q("U06-A-007", TOPIC, "Three numbers in AP", "Easy", "Multi-step computation MCQ",
  r"Three numbers in arithmetic progression have sum $27$ and product $504$. The sum of their squares is",
  r"$293$",
  [(r"$243$", r"Uses $3a^2$ only, dropping the $d^2$ terms from $(a-d)^2 + a^2 + (a+d)^2$."),
   (r"$268$", r"Expands the sum of squares as $3a^2 + d^2$ instead of $3a^2 + 2d^2$."),
   (r"$318$", r"Expands the sum of squares as $3a^2 + 3d^2$.")],
  r"Take the numbers as $a - d, a, a + d$. Then $3a = 27$, so $a = 9$, and $9(81 - d^2) = 504$ gives $d^2 = 25$. The numbers are $4, 9, 14$ and the sum of squares is $3a^2 + 2d^2 = 243 + 50 = 293$.",
  r"Mis-expanding $(a-d)^2 + a^2 + (a+d)^2$.",
  "U06-A-three-terms", "Symmetric choice of terms, then one expansion.",
  check=_c7, values=[293, 243, 268, 318], cognitive="Application")

def _c8():
    x = Symbol('x')
    return solve(2*(x + 4) - (2*x) - (3*x - 5), x)[0]
q("U06-A-008", TOPIC, "Condition for three terms in AP", "Easy", "Inverse/parameter MCQ",
  r"If $2x$, $x + 4$ and $3x - 5$ are three consecutive terms of an arithmetic progression, then $x$ equals",
  r"$\frac{13}{3}$",
  [(r"$5$", r"Equates the two differences in the wrong order, $(x + 4) - 2x = (x + 4) - (3x - 5)$."),
   (r"$3$", r"Expands $2(x + 4)$ as $2x + 4$, getting $2x + 4 = 5x - 5$."),
   (r"$\frac{9}{4}$", r"Sets the middle term equal to the sum of the outer terms, $x + 4 = 5x - 5$, forgetting the factor $2$.")],
  r"For consecutive terms of an AP, $2(x + 4) = 2x + (3x - 5)$, so $2x + 8 = 5x - 5$ and $x = \frac{13}{3}$.",
  r"Dropping the factor $2$ in the condition $2b = a + c$.",
  "U06-A-parameter-in-AP", "One linear equation from $2b = a + c$.",
  check=_c8, values=[Rational(13, 3), 5, 3, Rational(9, 4)], cognitive="Application")

q("U06-A-009", TOPIC, "Counting terms: multiples in a range", "Easy", "Single-step computation MCQ",
  r"The number of three-digit natural numbers divisible by $7$ is",
  r"$128$",
  [(r"$127$", r"Computes $\frac{994 - 105}{7}$ and forgets to add $1$."),
   (r"$142$", r"Counts all multiples of $7$ up to $999$, forgetting to remove the two-digit and one-digit ones."),
   (r"$129$", r"Divides $900$ by $7$ and rounds up.")],
  r"The multiples are $105, 112, \ldots, 994$, an AP with $d = 7$. So $n = \frac{994 - 105}{7} + 1 = 127 + 1 = 128$.",
  r"Forgetting the $+1$ when counting terms from first to last.",
  "U06-A-count-multiples", r"One application of $n = \frac{l - a}{d} + 1$.",
  check=lambda: len([m for m in range(100, 1000) if m % 7 == 0]), values=[128, 127, 142, 129],
  cognitive="Application",
  numerical=dict(question=r"The number of three-digit natural numbers divisible by $7$ is", answer=128))

def _c10():
    a = solve(term(A_, D_, 3) + term(A_, D_, 18) - 50, A_)[0]
    return simplify(ssum(a, D_, 20))
q("U06-A-010", TOPIC, "Terms equidistant from the ends", "Easy", "Conceptual/application MCQ",
  r"In an arithmetic progression, $a_3 + a_{18} = 50$. The sum of its first $20$ terms is",
  r"$500$",
  [(r"$1000$", r"Uses $S_{20} = 20(a_1 + a_{20})$, dropping the factor $\frac{1}{2}$."),
   (r"$525$", r"Takes the number of terms as $3 + 18 = 21$, giving $\frac{21}{2}(50)$."),
   (r"$475$", r"Takes the number of terms as $18 + 3 - 2 = 19$, giving $\frac{19}{2}(50)$.")],
  r"Since $3 + 18 = 1 + 20$, $a_3 + a_{18} = a_1 + a_{20} = 50$. Hence $S_{20} = \frac{20}{2}(a_1 + a_{20}) = 10(50) = 500$.",
  r"Not seeing that terms equidistant from the ends have a constant sum.",
  "U06-A-equidistant-pairs", "One property of equidistant terms, then the sum formula.",
  check=_c10, values=[500, 1000, 525, 475], cognitive="Understanding",
  numerical=dict(question=r"In an arithmetic progression, $a_3 + a_{18} = 50$. The sum of its first $20$ terms is", answer=500))

def _c11():
    a, d = 300, 150
    s3 = ssum(a, d, 3)
    return solve(Eq(term(a, d, N_), s3), N_)[0]
q("U06-A-011", TOPIC, "Word problem: term equal to a partial sum", "Easy", "Multi-step computation MCQ",
  r"A student saves Rs $300$ in the first month and increases the saving by Rs $150$ every month after that. The amount saved in the $n$th month alone equals the total amount saved in the first $3$ months. Then $n$ equals",
  r"$8$",
  [(r"$7$", r"Writes the $n$th month's saving as $a + nd$: $300 + 150n = 1350$ gives $n = 7$."),
   (r"$17$", r"Drops the factor $\frac{1}{2}$ in $S_3$, getting $3(600 + 300) = 2700$, then $300 + 150(n - 1) = 2700$ gives $n = 17$."),
   (r"$5$", r"Ignores the monthly increase when totalling the first three months, taking $3 \times 300 = 900$, then $300 + 150(n - 1) = 900$ gives $n = 5$.")],
  r"The monthly savings form an AP with $a = 300$, $d = 150$. The first three months total $300 + 450 + 600 = 1350$. Then $300 + 150(n - 1) = 1350$ gives $n - 1 = 7$, so $n = 8$.",
  r"Using $a + nd$ for the $n$th term.",
  "U06-A-word-term-equals-sum", r"Two short steps: one small sum, then solve a linear equation for $n$.",
  check=_c11, values=[8, 7, 17, 5], cognitive="Application",
  numerical=dict(question=r"A student saves Rs $300$ in the first month and increases the saving by Rs $150$ every month after that. If the amount saved in the $n$th month alone equals the total amount saved in the first $3$ months, then $n$ is", answer=8))

def _c12():
    S = lambda k: k**2 + 3*k + 2
    t = [from_S(S, k) for k in range(1, 6)]
    s1 = len({t[i + 1] - t[i] for i in range(4)}) == 1
    an = lambda k: 5 - 3*k
    s2 = simplify(an(N_ + 1) - an(N_)) == -3
    return (bool(s1), bool(s2))
q("U06-A-012", TOPIC, "Recognising an AP from S_n or a_n", "Easy", "Statement-based MCQ",
  r"Statement I: If the sum of the first $n$ terms of a sequence is $S_n = n^2 + 3n + 2$, then the sequence is an arithmetic progression. Statement II: The sequence with $n$th term $a_n = 5 - 3n$ is an arithmetic progression with common difference $-3$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Believes every quadratic $S_n$ gives an AP, ignoring the constant term."),
   (ST_TF, r"Accepts the quadratic $S_n$ and rejects Statement II, perhaps reading the common difference as $5$."),
   (ST_FF, r"Rejects Statement II by computing $d$ as $+3$ from a sign slip.")],
  r"From $S_n = n^2 + 3n + 2$: $a_1 = S_1 = 6$, $a_2 = S_2 - S_1 = 12 - 6 = 6$, $a_3 = 20 - 12 = 8$. The differences $0, 2$ are unequal, so Statement I is false (a constant term in $S_n$ breaks the AP at the first term). For Statement II, $a_{n+1} - a_n = -3$ for every $n$, so it is true.",
  r"Assuming any quadratic $S_n$ gives an AP even when it has a nonzero constant term.",
  "U06-A-stmt-Sn-and-an", "Two short checks, one of which hides a trap at $n = 1$.",
  check=_c12, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Understanding")

def _c13():
    n = solve(term(3, 5, N_) - 253, N_)[0]
    return term(3, 5, n - 9)
q("U06-A-013", TOPIC, "Term from the end", "Easy", "Single-step computation MCQ",
  r"The $10$th term from the end of the arithmetic progression $3, 8, 13, \ldots, 253$ is",
  r"$208$",
  [(r"$203$", r"Subtracts $10d$ from the last term instead of $9d$."),
   (r"$48$", r"Finds the $10$th term from the beginning."),
   (r"$213$", r"Subtracts $8d$ from the last term, miscounting the steps.")],
  r"Reading from the end, the AP starts at $253$ with common difference $-5$, so the $10$th term from the end is $253 - 9(5) = 208$.",
  r"Using $9$ or $11$ steps instead of $n - 1$ when counting from the end.",
  "U06-A-term-from-end", "One step: reverse the AP.",
  check=_c13, values=[208, 203, 48, 213], cognitive="Application")

def _c14():
    n = solve(term(7, 6, N_) - 205, N_)[0]
    return ssum(7, 6, n)
q("U06-A-014", TOPIC, "Sum of a finite AP with given last term", "Easy", "Multi-step computation MCQ",
  r"The sum of all the terms of the arithmetic progression $7, 13, 19, \ldots, 205$ is",
  r"$3604$",
  [(r"$3498$", r"Counts $\frac{205 - 7}{6} = 33$ terms, forgetting the $+1$."),
   (r"$3710$", r"Counts $35$ terms, adding $2$ instead of $1$ to $\frac{198}{6}$."),
   (r"$7208$", r"Uses $n(a + l)$, dropping the factor $\frac{1}{2}$.")],
  r"Number of terms $n = \frac{205 - 7}{6} + 1 = 34$. Then $S = \frac{34}{2}(7 + 205) = 17 \times 212 = 3604$.",
  r"Miscounting the number of terms.",
  "U06-A-sum-basic", r"Count the terms, then use $\frac{n}{2}(a + l)$.",
  check=_c14, values=[3604, 3498, 3710, 7208], cognitive="Application",
  numerical=dict(question=r"The sum of all the terms of the arithmetic progression $7, 13, 19, \ldots, 205$ is", answer=3604))

def _c15():
    a = solve(term(A_, D_, 11) - 15, A_)[0]
    return simplify(ssum(a, D_, 21))
q("U06-A-015", TOPIC, "Sum via the middle term", "Easy", "Conceptual/application MCQ",
  r"The $11$th term of an arithmetic progression is $15$. The sum of its first $21$ terms is",
  r"$315$",
  [(r"$\frac{315}{2}$", r"Uses $\frac{21}{2} \times a_{11}$, treating $a_{11}$ as $a_1 + a_{21}$ instead of half of it."),
   (r"$300$", r"Multiplies the middle term by $20$, the number of gaps, instead of the number of terms."),
   (r"$165$", r"Multiplies the middle term by $11$, its position, instead of the number of terms.")],
  r"$a_1 + a_{21} = 2a_{11} = 30$, so $S_{21} = \frac{21}{2}(30) = 21 \times 15 = 315$. The common difference is not needed.",
  r"Not seeing that $S_{2k-1} = (2k - 1)a_k$.",
  "U06-A-middle-term-sum", "One structural observation; no need to find $a$ or $d$.",
  check=_c15, values=[315, Rational(315, 2), 300, 165], cognitive="Understanding",
  numerical=dict(question=r"The $11$th term of an arithmetic progression is $15$. The sum of its first $21$ terms is", answer=315))

def _c16():
    n = solve(N_*(5 + 45)/2 - 400, N_)[0]
    return Rational(45 - 5, n - 1)
q("U06-A-016", TOPIC, "First term, last term and sum", "Easy", "Multi-step computation MCQ",
  r"An arithmetic progression has first term $5$, last term $45$ and the sum of all its terms is $400$. Its common difference is",
  r"$\frac{8}{3}$",
  [(r"$\frac{5}{2}$", r"Finds $n = 16$ correctly but uses $d = \frac{l - a}{n}$ instead of $\frac{l - a}{n - 1}$."),
   (r"$\frac{40}{7}$", r"Drops the $\frac{1}{2}$ in $S = \frac{n}{2}(a + l)$, getting $n = 8$, then uses $\frac{40}{n - 1}$."),
   (r"$5$", r"Gets $n = 8$ by dropping the $\frac{1}{2}$ and then divides $40$ by $n$.")],
  r"$\frac{n}{2}(5 + 45) = 400$ gives $n = 16$. Then $45 = 5 + 15d$, so $d = \frac{40}{15} = \frac{8}{3}$.",
  r"Dividing $l - a$ by $n$ instead of $n - 1$.",
  "U06-A-first-last-sum", "Two short steps: $n$ from the sum, then $d$.",
  check=_c16, values=[Rational(8, 3), Rational(5, 2), Rational(40, 7), 5], cognitive="Application")

def _c17():
    a = solve(Eq(ssum(A_, 2, 16), 800), A_)[0]
    return a
q("U06-A-017", TOPIC, "Word problem: first term from the total", "Easy", "Single-step computation MCQ",
  r"A hall has $16$ rows of seats. Each row has $2$ seats more than the row in front of it, and the hall has $800$ seats in all. The number of seats in the front row is",
  r"$35$",
  [(r"$34$", r"Uses $\frac{n}{2}[2a + nd]$: $8(2a + 32) = 800$ gives $a = 34$."),
   (r"$10$", r"Drops the factor $\frac{1}{2}$: $16(2a + 30) = 800$ gives $2a + 30 = 50$, so $a = 10$."),
   (r"$50$", r"Divides $800$ by $16$, which gives the average row size (the mean of the $8$th and $9$th rows), not the front row.")],
  r"The rows form an AP with $n = 16$, $d = 2$ and $S_{16} = 800$. So $8[2a + 15(2)] = 800$, that is $2a + 30 = 100$, giving $a = 35$. (Check: the back row has $35 + 30 = 65$ seats and $8(35 + 65) = 800$.)",
  r"Using $nd$ instead of $(n-1)d$ in the sum formula when solving for the first term.",
  "U06-A-word-first-term-from-sum", r"One linear equation for $a$ from the sum formula.",
  check=_c17, values=[35, 34, 10, 50], cognitive="Application",
  numerical=dict(question=r"A hall has $16$ rows of seats. Each row has $2$ seats more than the row in front of it, and the hall has $800$ seats in all. The number of seats in the front row is", answer=35))

def _c18():
    an = lambda k: 7 - 4*k
    return sum(an(k) for k in range(1, 16))
q("U06-A-018", TOPIC, "Sum when a_n is given", "Easy", "Single-step computation MCQ",
  r"The $n$th term of an arithmetic progression is $a_n = 7 - 4n$. The sum of its first $15$ terms is",
  r"$-375$",
  [(r"$-345$", r"Takes the first term as $7$ by putting $n = 0$, giving $\frac{15}{2}(7 - 53)$."),
   (r"$-405$", r"Uses $\frac{n}{2}[2a + nd] = \frac{15}{2}(6 - 60)$."),
   (r"$-750$", r"Drops the factor $\frac{1}{2}$.")],
  r"$a_1 = 3$ and $a_{15} = 7 - 60 = -53$, so $S_{15} = \frac{15}{2}(3 - 53) = \frac{15}{2}(-50) = -375$.",
  r"Reading the constant in $a_n$ as the first term.",
  "U06-A-an-linear-sum", "Two term evaluations, then the sum formula.",
  check=_c18, values=[-375, -345, -405, -750], cognitive="Application")

# ================================================================ MEDIUM (27)

def _c19():
    a = solve(9*term(A_, D_, 9) - 13*term(A_, D_, 13), A_)[0]
    return solve(term(a, D_, N_) / D_, N_)[0]
q("U06-A-019", TOPIC, "m times a_m equals n times a_n", "Medium", "Multi-step computation MCQ",
  r"In an arithmetic progression with nonzero common difference, $9$ times the $9$th term equals $13$ times the $13$th term. Which term of the progression is zero?",
  r"$a_{22}$",
  [(r"$a_{21}$", r"Gets $a = -21d$ correctly and then reads off $a_{21}$, using $a + nd$ for the $n$th term."),
   (r"$a_{4}$", r"Takes the difference $13 - 9$ of the positions."),
   (r"$a_{11}$", r"Takes the position midway between $9$ and $13$.")],
  r"$9(a + 8d) = 13(a + 12d)$ gives $-4a = 84d$, so $a = -21d$. Then $a_n = a + (n-1)d = (n - 22)d = 0$ exactly when $n = 22$.",
  r"Off-by-one error in the position, using $a + nd$.",
  "U06-A-m-am-equals-n-an", "Linear relation between $a$ and $d$, then locating the zero term.",
  check=_c19, values=[22, 21, 4, 11], cognitive="Application")

def _c20():
    lam = Symbol('lam')
    SA = lambda k: lam*k*(3*k + 8)
    SB = lambda k: lam*k*(7*k + 15)
    return simplify(from_S(SA, 12) / from_S(SB, 12))
q("U06-A-020", TOPIC, "Ratio of sums to ratio of terms", "Medium", "Multi-step computation MCQ",
  r"The sums of the first $n$ terms of two arithmetic progressions are in the ratio $(3n + 8) : (7n + 15)$ for every $n$. The ratio of their $12$th terms is",
  r"$\frac{7}{16}$",
  [(r"$\frac{4}{9}$", r"Puts $n = 12$ directly into the ratio of sums."),
   (r"$\frac{80}{183}$", r"Puts $n = 24$, using $2n$ instead of $2n - 1$."),
   (r"$\frac{41}{92}$", r"Puts $n = 11$, using $n - 1$.")],
  r"$\frac{S_n}{S'_n} = \frac{2a + (n-1)d}{2a' + (n-1)d'}$. With $n = 23$ this becomes $\frac{a + 11d}{a' + 11d'} = \frac{a_{12}}{a'_{12}}$. So the ratio is $\frac{3(23) + 8}{7(23) + 15} = \frac{77}{176} = \frac{7}{16}$.",
  r"Substituting the term number directly into the ratio of sums.",
  "U06-A-Sn-ratio-to-term-ratio", "Standard but needs the $n = 2k - 1$ substitution.",
  check=_c20, values=[Rational(7, 16), Rational(4, 9), Rational(80, 183), Rational(41, 92)], cognitive="Application")

def _c21():
    sols = [s for s in solve((T_ - 3)**2 - 2*(T_ + 1), T_) if s > 3]
    assert len(sols) == 1
    return log(sols[0], 2)
q("U06-A-021", TOPIC, "Logarithmic terms in AP", "Medium", "Inverse/parameter MCQ",
  r"If $\log_e 2$, $\log_e(2^x - 3)$ and $\log_e(2^x + 1)$ are in arithmetic progression, then $x$ equals",
  r"$\log_2 7$",
  [(r"$0$", r"Keeps the root $2^x = 1$, for which $2^x - 3 < 0$ and the logarithm is undefined."),
   (r"$\log_2 6$", r"Writes $\log_e 2 + \log_e(2^x + 1)$ as $\log_e(2 + 2^x + 1)$, adding the arguments."),
   (r"$\log_2 9$", r"Puts the arguments $2$, $2^x - 3$, $2^x + 1$ in AP instead of their logarithms.")],
  r"Let $t = 2^x$. The condition $2\log_e(t - 3) = \log_e 2 + \log_e(t + 1)$ gives $(t - 3)^2 = 2(t + 1)$, so $t^2 - 8t + 7 = 0$ and $t = 7$ or $t = 1$. The logarithm needs $t > 3$, so $t = 7$ and $x = \log_2 7$.",
  r"Forgetting the domain of the logarithm when choosing the root.",
  "U06-A-log-terms-AP", "AP condition, log laws, quadratic and a domain check.",
  check=_c21, values=[log(7, 2), 0, log(6, 2), log(9, 2)], cognitive="Application")

def _c22():
    return max(ssum(40, -3, k) for k in range(1, 60))
q("U06-A-022", TOPIC, "Greatest partial sum", "Medium", "Multi-step computation MCQ",
  r"The greatest value of the sum of the first $n$ terms of the arithmetic progression $40, 37, 34, \ldots$ is",
  r"$287$",
  [(r"$286$", r"Stops at $n = 13$, missing the last positive term $a_{14} = 1$."),
   (r"$285$", r"Includes the first negative term $a_{15} = -2$, taking $n = 15$."),
   (r"$266$", r"Finds $n = 14$ correctly but uses $S_n = \frac{n}{2}[2a + nd]$, getting $7(80 - 42)$.")],
  r"$a_n = 43 - 3n > 0$ for $n \le 14$, with $a_{14} = 1$ and $a_{15} = -2$. The sum is greatest when all positive terms are taken: $S_{14} = \frac{14}{2}(40 + 1) = 287$.",
  r"Stopping one term early or one term late when choosing $n$ for the greatest $S_n$.",
  "U06-A-max-partial-sum", "Locate the last positive term, then sum; off-by-one traps.",
  check=_c22, values=[287, 286, 285, 266], cognitive="Analysis",
  numerical=dict(question=r"The greatest value of the sum of the first $n$ terms of the arithmetic progression $40, 37, 34, \ldots$ is", answer=287))

def _c23():
    P = set(range(3, 408, 4)); Q = set(range(2, 710, 7))
    return len(P & Q)
q("U06-A-023", TOPIC, "Common terms of two APs", "Medium", "Multi-step computation MCQ",
  r"The number of terms common to the arithmetic progressions $3, 7, 11, \ldots, 407$ and $2, 9, 16, \ldots, 709$ is",
  r"$14$",
  [(r"$13$", r"Computes $\frac{407 - 23}{28}$ and forgets the $+1$ (after taking the integer part)."),
   (r"$25$", r"Uses the larger last term $709$ as the upper limit for the common terms."),
   (r"$15$", r"Starts the common AP at $3$ instead of the first actual common term $23$.")],
  r"The first common term is $23$ ($23 = 3 + 5 \cdot 4 = 2 + 3 \cdot 7$) and the common terms form an AP with difference $\operatorname{lcm}(4, 7) = 28$. They must not exceed $407$: $23 + 28(k - 1) \le 407$ gives $k \le 14.7$, so there are $14$ common terms (the last is $387$).",
  r"Using the wrong upper limit or the wrong starting term for the common AP.",
  "U06-A-common-terms", "Find first common term, the lcm difference and the binding upper limit.",
  check=_c23, values=[14, 13, 25, 15], cognitive="Application",
  numerical=dict(question=r"The number of terms common to the arithmetic progressions $3, 7, 11, \ldots, 407$ and $2, 9, 16, \ldots, 709$ is", answer=14))

q("U06-A-024", TOPIC, "Sum of numbers in a residue class", "Medium", "Multi-step computation MCQ",
  r"The sum of all two-digit natural numbers that leave remainder $3$ when divided by $5$ is",
  r"$999$",
  [(r"$1010$", r"Includes the one-digit numbers $3$ and $8$, summing $3, 8, \ldots, 98$."),
   (r"$1110$", r"Counts $20$ terms from $\frac{98 - 3}{5} + 1$ while still pairing $13$ with $98$."),
   (r"$1998$", r"Uses $n(a + l)$, dropping the factor $\frac{1}{2}$.")],
  r"The numbers are $13, 18, \ldots, 98$: $n = \frac{98 - 13}{5} + 1 = 18$, so the sum is $\frac{18}{2}(13 + 98) = 9 \times 111 = 999$.",
  r"Including numbers outside the stated range.",
  "U06-A-sum-residue-class", "Identify first and last terms in range, count, sum.",
  check=lambda: sum(m for m in range(10, 100) if m % 5 == 3), values=[999, 1010, 1110, 1998],
  cognitive="Application",
  numerical=dict(question=r"The sum of all two-digit natural numbers that leave remainder $3$ when divided by $5$ is", answer=999))

def _c25():
    k = Symbol('k')
    S = lambda m: 4*m**2 + k*m
    return solve(from_S(S, 5) - 31, k)[0]
q("U06-A-025", TOPIC, "Unknown coefficient in S_n", "Medium", "Inverse/parameter MCQ",
  r"The sum of the first $n$ terms of an arithmetic progression is $S_n = 4n^2 + kn$. If its $5$th term is $31$, then $k$ equals",
  r"$-5$",
  [(r"$11$", r"Uses $a_5 = \frac{S_5}{5} = 20 + k$."),
   (r"$-9$", r"Uses the derivative $8n + k$ for $a_n$, giving $40 + k = 31$."),
   (r"$-\frac{69}{5}$", r"Sets $S_5 = 31$, confusing the $5$th term with the sum of five terms.")],
  r"$a_5 = S_5 - S_4 = (100 + 5k) - (64 + 4k) = 36 + k$. Setting $36 + k = 31$ gives $k = -5$.",
  r"Confusing $a_n$ with $S_n$, $\frac{S_n}{n}$ or $S_n'$.",
  "U06-A-Sn-unknown-coefficient", "Use $a_n = S_n - S_{n-1}$ with a parameter, then solve.",
  check=_c25, values=[-5, 11, -9, Rational(-69, 5)], cognitive="Application")

def _c26():
    a, d = solve_ad([ssum(A_, D_, N_) - 40, ssum(A_, D_, 2*N_) - 120])
    return simplify(ssum(a, d, 3*N_))
q("U06-A-026", TOPIC, "Sums of consecutive blocks", "Medium", "Multi-step computation MCQ",
  r"For an arithmetic progression, the sum of the first $n$ terms is $40$ and the sum of the first $2n$ terms is $120$. The sum of the first $3n$ terms is",
  r"$240$",
  [(r"$280$", r"Assumes the block sums $40, 80, \ldots$ double each time, giving a third block of $160$."),
   (r"$160$", r"Uses $S_{3n} = S_{2n} + S_n$."),
   (r"$180$", r"Scales $S_{2n}$ by $\frac{3}{2}$, treating $S_n$ as proportional to $n$.")],
  r"The block sums $S_n$, $S_{2n} - S_n$, $S_{3n} - S_{2n}$ are in AP (each block exceeds the previous one by $n^2 d$). They are $40, 80$, so the third is $120$ and $S_{3n} = 120 + 120 = 240$. Equivalently $S_{3n} = 3(S_{2n} - S_n)$.",
  r"Treating block sums as proportional to $n$ or as a GP.",
  "U06-A-block-sums", "Needs the block-sum property or two-equation elimination.",
  check=_c26, values=[240, 280, 160, 180], cognitive="Application",
  numerical=dict(question=r"For an arithmetic progression, the sum of the first $n$ terms is $40$ and the sum of the first $2n$ terms is $120$. The sum of the first $3n$ terms is", answer=240))

def _c27():
    a = solve(ssum(A_, D_, 2*N_) - 3*ssum(A_, D_, N_), A_)[0]
    return simplify(ssum(a, D_, 3*N_) / ssum(a, D_, N_))
q("U06-A-027", TOPIC, "Sums of consecutive blocks", "Medium", "Multi-step computation MCQ",
  r"In an arithmetic progression, the sum of the first $n$ terms is half the sum of the next $n$ terms. Then $\frac{S_{3n}}{S_n}$, where $S_k$ denotes the sum of the first $k$ terms, equals",
  r"$6$",
  [(r"$7$", r"Assumes each block of $n$ terms is double the previous block: $1 + 2 + 4$."),
   (r"$9$", r"Assumes $S_n$ is proportional to $n^2$, so $S_{3n} = 9S_n$."),
   (r"$3$", r"Reports $\frac{S_{2n}}{S_n} = 3$ instead of $\frac{S_{3n}}{S_n}$.")],
  r"The blocks $S_n$, $S_{2n} - S_n$, $S_{3n} - S_{2n}$ form an AP. With the first two equal to $S_n$ and $2S_n$, the third is $3S_n$, so $S_{3n} = S_n + 2S_n + 3S_n = 6S_n$.",
  r"Assuming block sums grow geometrically.",
  "U06-A-block-sums", "Translate the condition, then use block sums in AP.",
  check=_c27, values=[6, 7, 9, 3], cognitive="Analysis",
  numerical=dict(question=r"In an arithmetic progression, the sum of the first $n$ terms is half the sum of the next $n$ terms. If $S_k$ denotes the sum of the first $k$ terms, then the value of $\frac{S_{3n}}{S_n}$ is", answer=6))

def _c28():
    m, e = symbols('m e', real=True)
    sols = solve([3*m - 24, (m - e)**2 + m**2 + (m + e)**2 - 210], [m, e], dict=True)
    vals = {simplify((s[m] - s[e])*s[m]*(s[m] + s[e])) for s in sols}
    assert len(vals) == 1
    return vals.pop()
q("U06-A-028", TOPIC, "Three numbers in AP", "Medium", "Multi-step computation MCQ",
  r"Three numbers in arithmetic progression have sum $24$ and the sum of their squares is $210$. Their product is",
  r"$440$",
  [(r"$512$", r"Takes all three numbers equal to the middle term $8$."),
   (r"$368$", r"Writes the sum of squares as $3a^2 + d^2$, getting $d^2 = 18$ and product $8(64 - 18)$."),
   (r"$464$", r"Writes the sum of squares as $3a^2 + 3d^2$, getting $d^2 = 6$ and product $8(64 - 6)$.")],
  r"With $a - d, a, a + d$: $3a = 24$ so $a = 8$; $3a^2 + 2d^2 = 210$ gives $d^2 = 9$. The numbers are $5, 8, 11$ and the product is $a(a^2 - d^2) = 8 \times 55 = 440$.",
  r"Mis-expanding the sum of squares of symmetric terms.",
  "U06-A-three-terms", "Symmetric terms, sum of squares, product.",
  check=_c28, values=[440, 512, 368, 464], cognitive="Application",
  numerical=dict(question=r"Three numbers in arithmetic progression have sum $24$ and the sum of their squares is $210$. The product of the three numbers is", answer=440))

def _c29():
    a = solve(sum(term(A_, D_, k) for k in (2, 6, 11, 15, 20, 24)) - 168, A_)[0]
    return simplify(ssum(a, D_, 25))
q("U06-A-029", TOPIC, "Terms equidistant from the ends", "Medium", "Multi-step computation MCQ",
  r"In an arithmetic progression, $a_2 + a_6 + a_{11} + a_{15} + a_{20} + a_{24} = 168$. The sum of its first $25$ terms is",
  r"$700$",
  [(r"$1400$", r"Uses $25(a_1 + a_{25})$, dropping the factor $\frac{1}{2}$."),
   (r"$672$", r"Pairs the terms correctly but finds $S_{24} = 12 \times 56$, as $24$ is the largest index shown."),
   (r"$728$", r"Pairs the terms correctly but uses $26$ terms, $13 \times 56$, since each pair has index sum $26$.")],
  r"The pairs $(a_2, a_{24})$, $(a_6, a_{20})$, $(a_{11}, a_{15})$ each have index sum $26$, so each pair equals $a_1 + a_{25}$. Hence $3(a_1 + a_{25}) = 168$, $a_1 + a_{25} = 56$, and $S_{25} = \frac{25}{2}(56) = 700$.",
  r"Mismatching the number of terms with the index sum.",
  "U06-A-equidistant-pairs", "Spot three equal pair sums, then the sum formula with the right $n$.",
  check=_c29, values=[700, 1400, 672, 728], cognitive="Analysis",
  numerical=dict(question=r"In an arithmetic progression, $a_2 + a_6 + a_{11} + a_{15} + a_{20} + a_{24} = 168$. The sum of its first $25$ terms is", answer=700))

def _c30():
    n = [s for s in solve(ssum(20, 15, N_) - 3250, N_)][0]
    return term(20, 15, n)
q("U06-A-030", TOPIC, "Word problem: instalments", "Medium", "Multi-step computation MCQ",
  r"A loan of Rs $3250$ is repaid in monthly instalments. The first instalment is Rs $20$ and each instalment is Rs $15$ more than the previous one. The last instalment is",
  r"Rs $305$",
  [(r"Rs $320$", r"Finds $n = 20$ correctly but uses $a + nd$ for the last instalment."),
   (r"Rs $290$", r"Finds $n = 20$ correctly but uses $a + (n-2)d$."),
   (r"Rs $\frac{325}{2}$", r"Divides $3250$ by $20$, giving the average instalment, not the last one.")],
  r"$\frac{n}{2}[40 + 15(n-1)] = 3250$ gives $15n^2 + 25n - 6500 = 0$, that is $3n^2 + 5n - 1300 = 0$, so $n = 20$. The last instalment is $20 + 19(15) = 305$.",
  r"Off-by-one in the last term after finding $n$.",
  "U06-A-word-instalments", "Quadratic for $n$, then the last term.",
  check=_c30, values=[305, 320, 290, Rational(325, 2)], cognitive="Application",
  numerical=dict(question=r"A loan of Rs $3250$ is repaid in monthly instalments. The first instalment is Rs $20$ and each instalment is Rs $15$ more than the previous one. The amount (in rupees) of the last instalment is", answer=305))

def _c31():
    a, b = symbols('a b')
    c = 2*b - a
    s1 = expand(2*b**2*(c + a) - a**2*(b + c) - c**2*(a + b)) == 0
    aa, bb, cc = 0, 1, 2
    s2 = 2*3**bb == 3**aa + 3**cc
    return (bool(s1), bool(s2))
q("U06-A-031", TOPIC, "Expressions built from terms in AP", "Medium", "Statement-based MCQ",
  r"Let $a, b, c$ be real numbers in arithmetic progression. Statement I: $a^2(b + c)$, $b^2(c + a)$, $c^2(a + b)$ are in arithmetic progression. Statement II: $3^a$, $3^b$, $3^c$ are in arithmetic progression." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Assumes any function applied to an AP gives an AP, accepting $3^a, 3^b, 3^c$."),
   (ST_FF, r"Tests Statement I with a careless substitution and rejects it."),
   (ST_FT, r"Reverses the two truth values.")],
  r"Put $c = 2b - a$. Then $2b^2(c + a) - a^2(b + c) - c^2(a + b)$ expands to $0$ identically (for instance $a, b, c = 1, 2, 3$ gives $5, 16, 27$), so Statement I is true. For Statement II, $a, b, c = 0, 1, 2$ gives $1, 3, 9$, which is not an AP ($3^a, 3^b, 3^c$ are in GP), so it is false.",
  r"Believing that every function of AP terms is again in AP.",
  "U06-A-stmt-AP-transforms", "One identity check and one counterexample.",
  check=_c31, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Analysis")

def _c32():
    S = lambda k: 2*k**2 + 3*k + 5
    return from_S(S, 1) + from_S(S, 10)
q("U06-A-032", TOPIC, "S_n with a constant term", "Medium", "Multi-step computation MCQ",
  r"The sum of the first $n$ terms of a sequence is $S_n = 2n^2 + 3n + 5$. The value of $a_1 + a_{10}$ is",
  r"$51$",
  [(r"$46$", r"Uses $a_n = 4n + 1$ for $n = 1$ as well, getting $a_1 = 5$ instead of $S_1 = 10$."),
   (r"$53$", r"Takes $a_1 = 10$ but uses the derivative $4n + 3$ for $a_{10}$."),
   (r"$\frac{67}{2}$", r"Takes $a_1 = 10$ but uses $a_{10} = \frac{S_{10}}{10} = \frac{47}{2}$.")],
  r"$a_1 = S_1 = 10$. For $n \ge 2$, $a_n = S_n - S_{n-1} = 2(2n - 1) + 3 = 4n + 1$, so $a_{10} = 41$. Hence $a_1 + a_{10} = 51$. (Because of the constant $5$, the formula $4n + 1$ fails at $n = 1$.)",
  r"Applying $a_n = S_n - S_{n-1}$ at $n = 1$.",
  "U06-A-Sn-with-constant", "Needs to see that the first term is exceptional.",
  check=_c32, values=[51, 46, 53, Rational(67, 2)], cognitive="Analysis",
  numerical=dict(question=r"The sum of the first $n$ terms of a sequence is $S_n = 2n^2 + 3n + 5$. The value of $a_1 + a_{10}$ is", answer=51))

def _c33():
    a = solve(sum(term(A_, D_, k) for k in range(1, 22, 2)) - 330, A_)[0]
    return simplify(sum(term(a, D_, k) for k in range(2, 22, 2)))
q("U06-A-033", TOPIC, "Odd-placed and even-placed terms", "Medium", "Multi-step computation MCQ",
  r"An arithmetic progression has $21$ terms. The sum of its terms in the odd positions ($a_1 + a_3 + \cdots + a_{21}$) is $330$. The sum of its terms in the even positions is",
  r"$300$",
  [(r"$330$", r"Assumes the odd-placed and even-placed sums are equal."),
   (r"$315$", r"Splits the total $630$ equally between the two groups."),
   (r"$360$", r"Thinks the even-placed sum exceeds the odd-placed sum by $a_{11} = 30$.")],
  r"The $11$ odd-placed terms form an AP whose middle term is $a_{11}$, so $11a_{11} = 330$ and $a_{11} = 30$. The $10$ even-placed terms form an AP with middle value $a_{11}$ as well ($a_{10} + a_{12} = 2a_{11}$), so their sum is $10 \times 30 = 300$.",
  r"Ignoring that the two groups have different numbers of terms.",
  "U06-A-odd-even-placed", "Two sub-APs with different lengths and a common middle value.",
  check=_c33, values=[300, 330, 315, 360], cognitive="Analysis",
  numerical=dict(question=r"An arithmetic progression has $21$ terms. The sum of its terms in the odd positions is $330$. The sum of its terms in the even positions is", answer=300))

def _c34():
    s1 = sum(m for m in range(1, 101) if m % 3 == 0) == 1683
    s2 = len(range(11, 404, 4)) == 99
    return (bool(s1), bool(s2))
q("U06-A-034", TOPIC, "Counting and summing terms", "Medium", "Statement-based MCQ",
  r"Statement I: The sum of all natural numbers from $1$ to $100$ that are multiples of $3$ is $1683$. Statement II: The arithmetic progression $11, 15, 19, \ldots, 403$ has $99$ terms." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Counts $\frac{403 - 11}{4} = 98$ terms, forgetting the $+1$, and rejects Statement II."),
   (ST_FT, r"Counts $34$ multiples of $3$ (up to $102$) and rejects Statement I."),
   (ST_FF, r"Makes both counting slips above.")],
  r"Multiples of $3$ up to $100$ are $3, 6, \ldots, 99$: $33$ terms with sum $\frac{33}{2}(3 + 99) = 1683$, so Statement I is true. For Statement II, $n = \frac{403 - 11}{4} + 1 = 98 + 1 = 99$, so it is true.",
  r"Off-by-one errors when counting terms.",
  "U06-A-stmt-counting", "Two independent counting computations.",
  check=_c34, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Application")

def _c35():
    d = solve(3*ssum(2, D_, 4) - (ssum(2, D_, 8) - ssum(2, D_, 4)), D_)[0]
    return term(2, d, 20)
q("U06-A-035", TOPIC, "Sums of consecutive blocks", "Medium", "Inverse/parameter MCQ",
  r"The first term of an arithmetic progression is $2$, and the sum of its first four terms is one-third of the sum of the next four terms. The $20$th term of the progression is",
  r"$78$",
  [(r"$\frac{86}{5}$", r"Uses $S_8$ in place of the sum of the next four terms, getting $d = \frac{4}{5}$."),
   (r"$82$", r"Finds $d = 4$ correctly but uses $a + 20d$."),
   (r"$-\frac{46}{15}$", r"Reverses the relation, taking the next four terms as one-third of the first four, so $d = -\frac{4}{15}$.")],
  r"$S_4 = 2(4 + 3d) = 8 + 6d$ and $a_5 + \cdots + a_8 = S_8 - S_4 = (16 + 28d) - (8 + 6d) = 8 + 22d$. So $3(8 + 6d) = 8 + 22d$, giving $d = 4$, and $a_{20} = 2 + 19(4) = 78$.",
  r"Confusing the sum of the next four terms with $S_8$.",
  "U06-A-block-sums", "Translate a word condition into two sums and solve for $d$.",
  check=_c35, values=[78, Rational(86, 5), 82, Rational(-46, 15)], cognitive="Application",
  numerical=dict(question=r"The first term of an arithmetic progression is $2$, and the sum of its first four terms is one-third of the sum of the next four terms. The $20$th term of the progression is", answer=78))

def _c36():
    sols = solve(ssum(24, -3, N_) - 78, N_)
    return sum(sols)
q("U06-A-036", TOPIC, "Number of terms for a given sum", "Medium", "Inverse/parameter MCQ",
  r"For the arithmetic progression $24, 21, 18, \ldots$, the sum of the first $n$ terms equals $78$. The sum of all possible values of $n$ is",
  r"$17$",
  [(r"$4$", r"Keeps only the smaller root, believing the sum cannot return to $78$ once it passes it."),
   (r"$13$", r"Keeps only the larger root."),
   (r"$16$", r"Uses $\frac{n}{2}[2a + nd]$, giving $n^2 - 16n + 52 = 0$, and adds its roots.")],
  r"$\frac{n}{2}[48 - 3(n - 1)] = 78$ gives $3n^2 - 51n + 156 = 0$, that is $n^2 - 17n + 52 = 0$, so $n = 4$ or $n = 13$. Both are valid: the terms after $a_9 = 0$ are negative and $a_{10} + a_{11} + a_{12} + a_{13} = -3 - 6 - 9 - 12 = -30$ cancels $a_5 + \cdots + a_8 = 12 + 9 + 6 + 3 = 30$. The sum of the values is $17$.",
  r"Rejecting a valid root of the quadratic in $n$.",
  "U06-A-n-from-sum", "Quadratic in $n$ with two admissible roots.",
  check=_c36, values=[17, 4, 13, 16], cognitive="Analysis",
  numerical=dict(question=r"For the arithmetic progression $24, 21, 18, \ldots$, the sum of the first $n$ terms equals $78$. The sum of all possible values of $n$ is", answer=17))

def _c37():
    a, d = solve_ad([ssum(A_, D_, 6) - 57, term(A_, D_, 10) - 29])
    return ssum(a, d, 10)
q("U06-A-037", TOPIC, "a and d from two conditions", "Medium", "Multi-step computation MCQ",
  r"In an arithmetic progression, the sum of the first $6$ terms is $57$ and the $10$th term is $29$. The sum of the first $10$ terms is",
  r"$155$",
  [(r"$290$", r"Uses $10 \times a_{10}$, treating $a_{10}$ as the average of the first ten terms."),
   (r"$310$", r"Uses $10(a_1 + a_{10})$, dropping the factor $\frac{1}{2}$."),
   (r"$140$", r"Finds $a = 2$, $d = 3$ but uses $a_9 = 26$ as the last term: $5(2 + 26)$.")],
  r"$3(2a + 5d) = 57$ gives $2a + 5d = 19$, and $a + 9d = 29$. Eliminating, $2(29 - 9d) + 5d = 19$, so $d = 3$, $a = 2$. Then $S_{10} = 5(2 + 29) = 155$.",
  r"Using the last term as the mean of all terms.",
  "U06-A-two-conditions", "Two linear equations in $a, d$, then the sum.",
  check=_c37, values=[155, 290, 310, 140], cognitive="Application",
  numerical=dict(question=r"In an arithmetic progression, the sum of the first $6$ terms is $57$ and the $10$th term is $29$. The sum of the first $10$ terms is", answer=155))

def _c38():
    n = [s for s in solve(ssum(3, 4, N_) - 210, N_)][0]
    return term(3, 4, n)
q("U06-A-038", TOPIC, "Last term from the sum", "Medium", "Inverse/parameter MCQ",
  r"If $3 + 7 + 11 + \cdots + x = 210$, where the terms on the left are in arithmetic progression, then $x$ equals",
  r"$39$",
  [(r"$43$", r"Finds $n = 10$ correctly but takes $x = a + nd$."),
   (r"$27$", r"Drops the $\frac{1}{2}$ in the sum, getting $2n^2 + n - 105 = 0$, $n = 7$, and $x = 3 + 6(4)$."),
   (r"$35$", r"Finds $n = 10$ but takes $x = a + (n - 2)d$.")],
  r"$\frac{n}{2}[6 + 4(n - 1)] = n(2n + 1) = 210$ gives $2n^2 + n - 210 = 0$, so $n = 10$ (the other root is negative). Then $x = a_{10} = 3 + 9(4) = 39$.",
  r"Off-by-one in the last term after solving for $n$.",
  "U06-A-n-from-sum", "Quadratic in $n$, reject the negative root, then the last term.",
  check=_c38, values=[39, 43, 27, 35], cognitive="Application",
  numerical=dict(question=r"If $3 + 7 + 11 + \cdots + x = 210$, where the terms on the left are in arithmetic progression, then the value of $x$ is", answer=39))

def _c39():
    a, d = solve_ad([ssum(A_, D_, 4) - 48, ssum(A_, D_, 7) - 147])
    return ssum(a, d, 12)
q("U06-A-039", TOPIC, "S_n from two given sums", "Medium", "Multi-step computation MCQ",
  r"For an arithmetic progression, $S_4 = 48$ and $S_7 = 147$, where $S_n$ is the sum of the first $n$ terms. Then $S_{12}$ equals",
  r"$432$",
  [(r"$396$", r"Solves for $a, d$ using $\frac{n}{2}[2a + nd]$ (getting $a = 0$, $d = 6$), then uses the correct formula for $S_{12}$."),
   (r"$864$", r"Drops the factor $\frac{1}{2}$ in the final sum."),
   (r"$252$", r"Assumes $S_n$ is proportional to $n$, scaling $147$ by $\frac{12}{7}$.")],
  r"$2(2a + 3d) = 48$ and $\frac{7}{2}(2a + 6d) = 147$ give $2a + 3d = 24$ and $a + 3d = 21$, so $a = 3$, $d = 6$. Then $S_{12} = 6(6 + 66) = 432$. (Here $S_n = 3n^2$.)",
  r"Assuming $S_n$ grows linearly with $n$.",
  "U06-A-Sn-two-values", "Two sum equations, then a third sum.",
  check=_c39, values=[432, 396, 864, 252], cognitive="Application",
  numerical=dict(question=r"For an arithmetic progression, $S_4 = 48$ and $S_7 = 147$, where $S_n$ is the sum of the first $n$ terms. The value of $S_{12}$ is", answer=432))

def _c40():
    m, e = symbols('m e', positive=True)
    sols = solve([3*m - 60, (m + e)**2 - m**2 - (m - e)**2], [m, e], dict=True)
    assert len(sols) == 1
    s = sols[0]
    return (s[m] - s[e])*s[m]/2
q("U06-A-040", TOPIC, "Sides of a right triangle in AP", "Medium", "Multi-step computation MCQ",
  r"The sides of a right-angled triangle are in arithmetic progression and its perimeter is $60$. The area of the triangle is",
  r"$150$",
  [(r"$300$", r"Multiplies the two legs $15 \times 20$ and forgets the factor $\frac{1}{2}$."),
   (r"$250$", r"Takes $20$ and $25$ as the legs, using the hypotenuse as a leg."),
   (r"$\frac{375}{2}$", r"Uses half the product of the hypotenuse $25$ and the shortest side $15$.")],
  r"Take the sides as $a - d, a, a + d$ with $d > 0$, so $3a = 60$ and $a = 20$. The hypotenuse is $a + d$: $(a + d)^2 = a^2 + (a - d)^2$ gives $4ad = a^2$, so $d = 5$. The sides are $15, 20, 25$ and the area is $\frac{1}{2}(15)(20) = 150$.",
  r"Using the hypotenuse as one of the legs.",
  "U06-A-right-triangle-sides", "AP parametrisation plus Pythagoras.",
  check=_c40, values=[150, 300, 250, Rational(375, 2)], cognitive="Application",
  numerical=dict(question=r"The sides of a right-angled triangle are in arithmetic progression and its perimeter is $60$. The area of the triangle is", answer=150))

def _c41():
    a, d = solve_ad([term(A_, D_, 4) - Rational(1, 6), term(A_, D_, 6) - Rational(1, 4)])
    return ssum(a, d, 24)
q("U06-A-041", TOPIC, "Fractional terms", "Medium", "Multi-step computation MCQ",
  r"In an arithmetic progression, the $4$th term is $\frac{1}{6}$ and the $6$th term is $\frac{1}{4}$. The sum of its first $24$ terms is",
  r"$\frac{25}{2}$",
  [(r"$12$", r"Uses $\frac{n}{2} \times a_{24} = 12 \times 1$, forgetting to add the first term."),
   (r"$25$", r"Drops the factor $\frac{1}{2}$: $24\left(\frac{1}{24} + 1\right)$."),
   (r"$13$", r"Uses $\frac{n}{2}[2a + nd] = 12\left(\frac{2}{24} + 1\right)$.")],
  r"$2d = \frac{1}{4} - \frac{1}{6} = \frac{1}{12}$, so $d = \frac{1}{24}$ and $a = \frac{1}{6} - \frac{3}{24} = \frac{1}{24}$. Thus $a_n = \frac{n}{24}$, $a_{24} = 1$, and $S_{24} = 12\left(\frac{1}{24} + 1\right) = \frac{25}{2}$.",
  r"Using only the last term in $\frac{n}{2}(a + l)$.",
  "U06-A-reciprocal-terms", "Fractions, two equations, then the sum.",
  check=_c41, values=[Rational(25, 2), 12, 25, 13], cognitive="Application")

def _c42():
    sols = [s for s in solve(ssum(10, 2, N_) - 30*N_, N_) if s > 0]
    return sols[0]
q("U06-A-042", TOPIC, "Word problem: catching up", "Medium", "Inverse/parameter MCQ",
  r"Two runners start together from the same point along the same track. Runner $P$ covers $10$ m in the first minute, $12$ m in the second minute, $14$ m in the third minute, and so on. Runner $Q$ covers $30$ m every minute. After how many minutes will $P$ catch up with $Q$?",
  r"$21$",
  [(r"$11$", r"Finds when the speeds become equal ($10 + 2(n - 1) = 30$), not when the distances become equal."),
   (r"$20$", r"Uses $\frac{n}{2}[2a + nd]$, so $n(10 + n) = 30n$."),
   (r"$6$", r"Drops the factor $\frac{1}{2}$ in $P$'s distance, so $n(2n + 18) = 30n$.")],
  r"After $n$ minutes, $P$ has covered $\frac{n}{2}[20 + 2(n - 1)] = n(n + 9)$ m and $Q$ has covered $30n$ m. Equal distances (with $n > 0$) need $n + 9 = 30$, so $n = 21$.",
  r"Confusing equal speeds with equal distances.",
  "U06-A-word-catch-up", "Model two motions, equate totals.",
  check=_c42, values=[21, 11, 20, 6], cognitive="Application",
  numerical=dict(question=r"Two runners start together from the same point along the same track. Runner $P$ covers $10$ m in the first minute, $12$ m in the second minute, $14$ m in the third minute, and so on. Runner $Q$ covers $30$ m every minute. The number of minutes after which $P$ catches up with $Q$ is", answer=21))

def _c43():
    k = 1
    while ssum(1, 3, k) <= 1000:
        k += 1
    return k
q("U06-A-043", TOPIC, "Least n for a sum to exceed a bound", "Medium", "Inverse/parameter MCQ",
  r"The least number of terms of the arithmetic progression $1, 4, 7, 10, \ldots$ that must be added so that the sum exceeds $1000$ is",
  r"$26$",
  [(r"$25$", r"Solves $3n^2 - n - 2000 = 0$ and takes the integer part of the positive root, about $25.98$."),
   (r"$19$", r"Drops the $\frac{1}{2}$, solving $n(3n - 1) > 1000$."),
   (r"$18$", r"Drops the $\frac{1}{2}$ and also takes the integer part of the root, about $18.4$.")],
  r"$S_n = \frac{n}{2}[2 + 3(n - 1)] = \frac{n(3n - 1)}{2}$. Then $S_{25} = \frac{25 \times 74}{2} = 925$ and $S_{26} = \frac{26 \times 77}{2} = 1001 > 1000$, so the least $n$ is $26$.",
  r"Rounding the root of the quadratic down instead of up.",
  "U06-A-least-n-sum-exceeds", "Quadratic inequality in $n$ and correct rounding.",
  check=_c43, values=[26, 25, 19, 18], cognitive="Application",
  numerical=dict(question=r"The least number of terms of the arithmetic progression $1, 4, 7, 10, \ldots$ that must be added so that the sum exceeds $1000$ is", answer=26))

def _c44():
    avg = [simplify(ssum(A_, D_, k)/k) for k in range(1, 6)]
    diffs = {simplify(avg[i + 1] - avg[i]) for i in range(4)}
    s1 = diffs == {D_}
    d = Rational(0 - 10, 10)
    s2 = ssum(10, d, 20) == 0
    return (bool(s1), bool(s2))
q("U06-A-044", TOPIC, "Facts about S_n", "Medium", "Statement-based MCQ",
  r"Statement I: If $a_1, a_2, a_3, \ldots$ is an arithmetic progression with common difference $d \ne 0$ and $S_n = a_1 + a_2 + \cdots + a_n$, then $\frac{S_1}{1}, \frac{S_2}{2}, \frac{S_3}{3}, \ldots$ is an arithmetic progression with common difference $d$. Statement II: If an arithmetic progression has first term $10$ and $11$th term $0$, then the sum of its first $20$ terms is $0$." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Assumes the averages $\frac{S_n}{n}$ step by $d$ like the terms, and confuses $S_{21} = 21a_{11} = 0$ with $S_{20}$."),
   (ST_TF, r"Assumes the averages $\frac{S_n}{n}$ step by $d$ like the terms, but checks Statement II correctly."),
   (ST_FT, r"Finds the common difference $\frac{d}{2}$ of the averages correctly but assumes $S_{20} = 0$ because $a_{11} = 0$.")],
  r"$\frac{S_n}{n} = \frac{a_1 + a_n}{2} = a_1 + \frac{(n - 1)d}{2}$, which is an AP with common difference $\frac{d}{2} \ne d$, so Statement I is false. In Statement II, $10d = -10$ gives $d = -1$, so $a_{20} = -9$ and $S_{20} = 10(10 - 9) = 10 \ne 0$; it is $S_{21} = 21a_{11}$ that vanishes. So Statement II is false.",
  r"Assuming the running averages $\frac{S_n}{n}$ have the same common difference as the terms, and mixing up $S_{2k-1} = (2k - 1)a_k$ with $S_{2k}$.",
  "U06-A-stmt-Sn-facts", r"Two checks, each with a tempting shortcut: averages of an AP step by $\frac{d}{2}$, and the zero middle term belongs to $S_{21}$.",
  check=_c44, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Analysis")

def _c45():
    a, b, c, x = symbols('a b c x')
    disc = discriminant((b - c)*x**2 + (c - a)*x + (a - b), x)
    fl = factor_list(disc)[1]
    assert len(fl) == 1 and fl[0][1] == 2
    return fl[0][0]
q("U06-A-045", TOPIC, "AP condition from equal roots", "Medium", "Conceptual/application MCQ",
  r"Let $a, b, c$ be real numbers with $b \ne c$. If the quadratic equation $(b - c)x^2 + (c - a)x + (a - b) = 0$ has equal roots, then",
  r"$2b = a + c$",
  [(r"$b^2 = ac$", r"Guesses the geometric-mean relation from the symmetric look of the coefficients."),
   (r"$a = c$", r"Sets the product of the roots $\frac{a - b}{b - c}$ equal to $-1$, giving $a - b = c - b$."),
   (r"$2c = a + b$", r"Uses the coefficient of $x$ as the middle term of the AP condition.")],
  r"The coefficients add to $0$, so $x = 1$ is a root. Equal roots means both roots are $1$, so the product $\frac{a - b}{b - c} = 1$, giving $a - b = b - c$, that is $2b = a + c$. (Equivalently, the discriminant is $(a + c - 2b)^2$.)",
  r"Not noticing that $x = 1$ is always a root.",
  "U06-A-equal-roots-AP", "Spotting a root, then product of roots.",
  check=_c45, values=[symbols('a') + symbols('c') - 2*symbols('b'),
                      symbols('b')**2 - symbols('a')*symbols('c'),
                      symbols('a') - symbols('c'),
                      symbols('a') + symbols('b') - 2*symbols('c')],
  cognitive="Analysis")

# ================================================================ DIFFICULT (15)

def _c46():
    d = solve(ssum(48, D_, 10) - ssum(48, D_, 15), D_)[0]
    return max(ssum(48, d, k) for k in range(1, 60))
q("U06-A-046", TOPIC, "Equal partial sums and the maximum sum", "Difficult", "Multi-step computation MCQ",
  r"An arithmetic progression has first term $48$, and the sum of its first $10$ terms equals the sum of its first $15$ terms. The greatest value of the sum of its first $n$ terms is",
  r"$312$",
  [(r"$308$", r"Writes $a_n = a + nd = 48 - 4n$, so takes the terms positive only for $n \le 11$ and reports $S_{11} = \frac{11}{2}(96 - 40)$."),
   (r"$300$", r"Assumes the maximum occurs at $S_{10} = S_{15}$ itself."),
   (r"$624$", r"Finds the right $n = 12$ but drops the $\frac{1}{2}$: $12(96 - 44)$.")],
  r"$5(96 + 9d) = \frac{15}{2}(96 + 14d)$ gives $480 + 45d = 720 + 105d$, so $d = -4$. Then $a_n = 52 - 4n$ is positive up to $n = 12$ and $a_{13} = 0$, so $S_{12} = S_{13} = 6(48 + 4) = 312$ is the greatest sum.",
  r"Misindexing the $n$th term as $a + nd$ when locating the last positive term.",
  "U06-A-Sp-equals-Sq", "Find $d$ from equal sums, then integer maximisation with a zero term.",
  check=_c46, values=[312, 308, 300, 624], cognitive="Analysis",
  numerical=dict(question=r"An arithmetic progression has first term $48$, and the sum of its first $10$ terms equals the sum of its first $15$ terms. The greatest value of the sum of its first $n$ terms is", answer=312))

q("U06-A-047", TOPIC, "Sum excluding multiples", "Difficult", "Multi-step computation MCQ",
  r"The sum of all natural numbers from $1$ to $300$ that are divisible by neither $3$ nor $5$ is",
  r"$24000$",
  [(r"$20850$", r"Subtracts the multiples of $3$ and of $5$ but does not add back the multiples of $15$."),
   (r"$27150$", r"Adds back the multiples of $15$ twice."),
   (r"$42000$", r"Removes only the multiples of $15$.")],
  r"$\sum_{1}^{300} k = 45150$. Multiples of $3$: $3(1 + \cdots + 100) = 15150$; of $5$: $5(1 + \cdots + 60) = 9150$; of $15$: $15(1 + \cdots + 20) = 3150$. The required sum is $45150 - 15150 - 9150 + 3150 = 24000$.",
  r"Omitting the inclusion-exclusion correction.",
  "U06-A-sum-inclusion-exclusion", "Four AP sums combined by inclusion-exclusion.",
  check=lambda: sum(k for k in range(1, 301) if k % 3 and k % 5), values=[24000, 20850, 27150, 42000],
  cognitive="Analysis",
  numerical=dict(question=r"The sum of all natural numbers from $1$ to $300$ that are divisible by neither $3$ nor $5$ is", answer=24000))

def _c48():
    cnt = 0
    for d in range(1, 100):
        if (101 - 2) % d == 0 and (101 - 2)//d + 1 >= 3:
            cnt += 1
    return cnt
q("U06-A-048", TOPIC, "Counting integer APs", "Difficult", "Multi-step computation MCQ",
  r"The number of increasing arithmetic progressions of integers that have first term $2$, last term $101$ and at least three terms is",
  r"$5$",
  [(r"$6$", r"Also counts $d = 99$, which gives only the two terms $2, 101$."),
   (r"$8$", r"Uses $101 - 1 = 100$ in place of $101 - 2$ and counts divisors of $100$ other than $100$."),
   (r"$10$", r"Counts positive and negative divisors of $99$ except $\pm 99$, ignoring that the AP is increasing.")],
  r"If there are $n$ terms, $(n - 1)d = 99$ with $d$ a positive integer and $n - 1 \ge 2$. So $d$ is a divisor of $99 = 3^2 \cdot 11$ other than $99$: $d \in \{1, 3, 9, 11, 33\}$, giving $5$ progressions.",
  r"Forgetting the 'at least three terms' condition.",
  "U06-A-count-integer-APs", "Turns into a divisor count with an excluded case.",
  check=_c48, values=[5, 6, 8, 10], cognitive="Analysis",
  numerical=dict(question=r"The number of increasing arithmetic progressions of integers that have first term $2$, last term $101$ and at least three terms is", answer=5))

def _c49():
    sol = solve([ssum(3, D_, 2)*1 - 4*ssum(3, D_, 1)], D_)
    d = sol[D_] if isinstance(sol, dict) else sol[0]
    # confirm S_n/S_m = n^2/m^2 for all n, m
    assert simplify(ssum(3, d, N_) - 3*N_**2) == 0
    return term(3, d, 10)
q("U06-A-049", TOPIC, "S_n proportional to n squared", "Difficult", "Multi-step computation MCQ",
  r"For an arithmetic progression with first term $3$, $\frac{S_m}{S_n} = \frac{m^2}{n^2}$ for all $m \ne n$, where $S_k$ is the sum of the first $k$ terms. The $10$th term is",
  r"$57$",
  [(r"$30$", r"Assumes the terms are in the ratio of their positions, so $d = a$ and $a_{10} = 10a$."),
   (r"$60$", r"Gets $S_n = 3n^2$ but takes $a_n$ as the derivative $6n$."),
   (r"$63$", r"Finds $d = 6$ correctly but uses $a + nd$.")],
  r"The condition forces $S_n = cn^2$ for a constant $c$. Then $c = S_1 = 3$, and $a_n = S_n - S_{n-1} = 3(2n - 1)$, so $d = 6$ and $a_{10} = 3(19) = 57$.",
  r"Confusing $S_n \propto n^2$ with $a_n \propto n$.",
  "U06-A-Sn-ratio-squares", "Recognise $S_n = cn^2$, then derive the terms.",
  check=_c49, values=[57, 30, 60, 63], cognitive="Analysis")

def _c50():
    S = sum(term(A_, D_, k) for k in range(1, 41))
    T = sum(term(A_, D_, 2*k - 1) for k in range(1, 21))
    d = solve(expand(S - 2*T) - 60, D_)[0]
    a = solve(term(A_, d, 7) - 20, A_)[0]
    return term(a, d, 15)
q("U06-A-050", TOPIC, "Even-placed minus odd-placed terms", "Difficult", "Multi-step computation MCQ",
  r"Let $a_1, a_2, \ldots, a_{40}$ be in arithmetic progression, $S = \sum_{i=1}^{40} a_i$ and $T = \sum_{i=1}^{20} a_{2i-1}$. If $a_7 = 20$ and $S - 2T = 60$, then $a_{15}$ equals",
  r"$44$",
  [(r"$68$", r"Writes $S - 2T = 10d$, counting only half the pairs, so $d = 6$."),
   (r"$32$", r"Writes $S - 2T = 40d$, using the number of terms instead of the number of pairs, so $d = \frac{3}{2}$."),
   (r"$47$", r"Finds $d = 3$ correctly but uses $a_{15} = a_7 + 9d$.")],
  r"$S - 2T$ is the sum of the even-placed terms minus the sum of the odd-placed terms, $\sum_{i=1}^{20}(a_{2i} - a_{2i-1}) = 20d$. So $20d = 60$, $d = 3$, and $a_{15} = a_7 + 8d = 20 + 24 = 44$.",
  r"Not rewriting $S - 2T$ as a difference of paired terms.",
  "U06-A-even-minus-odd", "Needs the pairing insight before any formula.",
  check=_c50, values=[44, 68, 32, 47], cognitive="Analysis",
  numerical=dict(question=r"Let $a_1, a_2, \ldots, a_{40}$ be in arithmetic progression, $S = \sum_{i=1}^{40} a_i$ and $T = \sum_{i=1}^{20} a_{2i-1}$. If $a_7 = 20$ and $S - 2T = 60$, then the value of $a_{15}$ is", answer=44))

def _c51():
    P = set(range(17, 418, 4)); Q = set(range(16, 467, 5))
    return sum(P & Q)
q("U06-A-051", TOPIC, "Sum of common terms", "Difficult", "Multi-step computation MCQ",
  r"The sum of the terms common to the arithmetic progressions $17, 21, 25, \ldots, 417$ and $16, 21, 26, \ldots, 466$ is",
  r"$4220$",
  [(r"$4641$", r"Counts $21$ common terms, letting the last one be $421$, which exceeds $417$."),
   (r"$8440$", r"Drops the factor $\frac{1}{2}$ in the sum."),
   (r"$5543$", r"Uses $466$ as the upper limit, taking $23$ common terms up to $461$.")],
  r"The first common term is $21$ and the common difference is $\operatorname{lcm}(4, 5) = 20$. Common terms cannot exceed $417$: $21 + 20(k - 1) \le 417$ gives $k \le 20.8$, so $k = 20$ and the last is $401$. The sum is $\frac{20}{2}(21 + 401) = 4220$.",
  r"Using the wrong upper limit for the common terms.",
  "U06-A-common-terms", "First common term, lcm difference, binding limit, then a sum.",
  check=_c51, values=[4220, 4641, 8440, 5543], cognitive="Analysis")

q("U06-A-052", TOPIC, "Sum excluding multiples", "Difficult", "Multi-step computation MCQ",
  r"The sum of all natural numbers $k$ with $1 \le k \le 100$ that are divisible by neither $2$ nor $3$ is",
  r"$1633$",
  [(r"$817$", r"Subtracts the multiples of $2$ and of $3$ but does not add back the multiples of $6$."),
   (r"$2449$", r"Adds back the multiples of $6$ twice."),
   (r"$1650$", r"Counts $33$ such numbers correctly but assumes their average is $50$.")],
  r"Such $k$ are $1, 7, \ldots, 97$ ($17$ terms, sum $\frac{17}{2}(98) = 833$) and $5, 11, \ldots, 95$ ($16$ terms, sum $8(100) = 800$). Total $1633$. By inclusion-exclusion: $5050 - 2550 - 1683 + 816 = 1633$.",
  r"Omitting the inclusion-exclusion correction.",
  "U06-A-sum-inclusion-exclusion", "Split into two APs or use inclusion-exclusion.",
  check=lambda: sum(k for k in range(1, 101) if k % 2 and k % 3), values=[1633, 817, 2449, 1650],
  cognitive="Analysis",
  numerical=dict(question=r"The sum of all natural numbers $k$ with $1 \le k \le 100$ that are divisible by neither $2$ nor $3$ is", answer=1633))

def _c53():
    k = Symbol('k')
    expr = expand(term(5, D_, 3*N_) - k*term(5, D_, N_))
    sols = solve(Poly(expr, N_).coeffs(), [k, D_], dict=True)
    sols = [s for s in sols if s[D_] != 0]
    assert len(sols) == 1
    return ssum(5, sols[0][D_], 20)
q("U06-A-053", TOPIC, "Term ratio independent of n", "Difficult", "Multi-step computation MCQ",
  r"An arithmetic progression with first term $5$ and nonzero common difference has the property that $\frac{a_{3n}}{a_n}$ is the same for every natural number $n$. The sum of its first $20$ terms is",
  r"$1050$",
  [(r"$2000$", r"Uses the condition for $\frac{S_{3n}}{S_n}$ to be constant, $d = 2a$, instead of the one for terms."),
   (r"$1000$", r"Finds $a_{20} = 100$ correctly but takes the sum as $\frac{20}{2} \times a_{20}$."),
   (r"$2100$", r"Drops the factor $\frac{1}{2}$ in the sum.")],
  r"$a_{3n} = k\,a_n$ for all $n$ means $5 + (3n - 1)d = k[5 + (n - 1)d]$. Comparing coefficients of $n$: $3d = kd$, so $k = 3$; constants: $5 - d = 3(5 - d)$, so $d = 5$. Then $a_n = 5n$ and $S_{20} = 5 \cdot \frac{20 \cdot 21}{2} = 1050$.",
  r"Mixing the term condition ($d = a$) with the sum condition ($d = 2a$).",
  "U06-A-term-ratio-independent", "Identity in $n$, comparison of coefficients, then a sum.",
  check=_c53, values=[1050, 2000, 1000, 2100], cognitive="Analysis",
  numerical=dict(question=r"An arithmetic progression with first term $5$ and nonzero common difference has the property that $\frac{a_{3n}}{a_n}$ is the same for every natural number $n$. The sum of its first $20$ terms is", answer=1050))

q("U06-A-054", TOPIC, "Positive partial sums", "Difficult", "Multi-step computation MCQ",
  r"For the arithmetic progression $50, 47, 44, \ldots$, let $S_n$ be the sum of the first $n$ terms. The number of natural numbers $n$ for which $S_n > 0$ is",
  r"$34$",
  [(r"$17$", r"Counts the positive terms instead of the positive partial sums."),
   (r"$33$", r"Uses $\frac{n}{2}[2a + nd] > 0$, giving $n < \frac{100}{3}$."),
   (r"$35$", r"Rounds $\frac{103}{3}$ up instead of down.")],
  r"$S_n = \frac{n}{2}[100 - 3(n - 1)] = \frac{n(103 - 3n)}{2} > 0$ exactly when $n < \frac{103}{3} = 34.33$. So $n = 1, 2, \ldots, 34$. Check: $S_{34} = 17 > 0$ and $S_{35} = -35 < 0$.",
  r"Confusing positive terms with positive sums.",
  "U06-A-positive-partial-sums", "Inequality on $S_n$, a trap with positive terms, careful rounding.",
  check=lambda: len([k for k in range(1, 200) if ssum(50, -3, k) > 0]), values=[34, 17, 33, 35],
  cognitive="Analysis",
  numerical=dict(question=r"For the arithmetic progression $50, 47, 44, \ldots$, let $S_n$ be the sum of the first $n$ terms. The number of natural numbers $n$ for which $S_n > 0$ is", answer=34))

q("U06-A-055", TOPIC, "Sum of a sub-progression", "Difficult", "Multi-step computation MCQ",
  r"The sum of all odd natural numbers from $1$ to $500$ that leave remainder $3$ when divided by $7$ is",
  r"$8928$",
  [(r"$9054$", r"Takes half the sum of all numbers of the form $7k + 3$ up to $500$, assuming the odd ones contribute half."),
   (r"$9180$", r"Uses $d = 14$ and $36$ terms but takes the last term as $3 + 14 \times 36 = 507$."),
   (r"$18108$", r"Ignores the odd condition and sums all $72$ numbers $3, 10, \ldots, 500$.")],
  r"Numbers $\equiv 3 \pmod 7$ alternate in parity, so the odd ones are $3, 17, 31, \ldots$ with $d = 14$. The last one not exceeding $500$ is $493$ ($3 + 14 \cdot 35$), so there are $36$ terms and the sum is $\frac{36}{2}(3 + 493) = 18 \times 496 = 8928$.",
  r"Assuming a parity filter halves the sum exactly.",
  "U06-A-sum-residue-class", "Combine two conditions into one AP with difference $14$.",
  check=lambda: sum(k for k in range(1, 501) if k % 2 == 1 and k % 7 == 3), values=[8928, 9054, 9180, 18108],
  cognitive="Analysis")

def _c56():
    lam = Symbol('lam')
    an = lambda k: lam*(4*k - 1)
    bn = lambda k: lam*(2*k + 5)
    return simplify(sum(an(k) for k in range(1, 11)) / sum(bn(k) for k in range(1, 11)))
q("U06-A-056", TOPIC, "Ratio of terms to ratio of sums", "Difficult", "Multi-step computation MCQ",
  r"The $n$th terms of two arithmetic progressions are in the ratio $(4n - 1) : (2n + 5)$ for every $n$. The ratio of the sums of their first $10$ terms is",
  r"$\frac{21}{16}$",
  [(r"$\frac{39}{25}$", r"Uses the ratio of the $10$th terms as the ratio of the sums."),
   (r"$\frac{75}{43}$", r"Applies the sum-to-term rule in the wrong direction, putting $n = 2(10) - 1 = 19$."),
   (r"$\frac{19}{15}$", r"Puts $n = \frac{10}{2} = 5$ instead of $\frac{10 + 1}{2}$.")],
  r"$\frac{S_n}{S'_n} = \frac{a_1 + a_n}{a'_1 + a'_n}$ and $\frac{a_1 + a_n}{2}$ equals the term in position $\frac{n+1}{2}$ (or the mean of the two middle terms). With $n = 10$ this is position $\frac{11}{2}$, and since the term ratio is a ratio of linear expressions, $\frac{4 \cdot \frac{11}{2} - 1}{2 \cdot \frac{11}{2} + 5} = \frac{21}{16}$. Directly, $\sum (4k - 1) = 210$ and $\sum (2k + 5) = 160$ for $k = 1, \ldots, 10$.",
  r"Applying the $2n - 1$ substitution in the wrong direction.",
  "U06-A-term-ratio-to-sum-ratio", "Reverse of the standard substitution; must justify the half-integer position.",
  check=_c56, values=[Rational(21, 16), Rational(39, 25), Rational(75, 43), Rational(19, 15)],
  cognitive="Analysis")

q("U06-A-057", TOPIC, "Sum of absolute values of terms", "Difficult", "Multi-step computation MCQ",
  r"The $n$th term of an arithmetic progression is $a_n = 3n - 20$. The value of $|a_1| + |a_2| + \cdots + |a_{15}|$ is",
  r"$174$",
  [(r"$60$", r"Computes $a_1 + \cdots + a_{15}$, ignoring the absolute values."),
   (r"$117$", r"Adds only the positive terms $a_7, \ldots, a_{15}$, dropping the negative ones."),
   (r"$172$", r"Treats the first seven terms as negative, computing $S_{15} - 2S_7$.")],
  r"$a_n < 0$ for $n \le 6$ and $a_n > 0$ for $n \ge 7$. The negative terms $-17, -14, \ldots, -2$ have sum $-57$, and $a_7, \ldots, a_{15} = 1, 4, \ldots, 25$ have sum $\frac{9}{2}(26) = 117$. So the required value is $117 + 57 = 174$, that is $S_{15} - 2S_6 = 60 + 114$.",
  r"Splitting the sum at the wrong index.",
  "U06-A-abs-sum", "Split at the sign change, then two AP sums.",
  check=lambda: sum(Abs(3*k - 20) for k in range(1, 16)), values=[174, 60, 117, 172],
  cognitive="Analysis",
  numerical=dict(question=r"The $n$th term of an arithmetic progression is $a_n = 3n - 20$. The value of $|a_1| + |a_2| + \cdots + |a_{15}|$ is", answer=174))

def _c58():
    sols = solve([term(A_, D_, 1) + term(A_, D_, 3) + term(A_, D_, 5) - 21,
                  term(A_, D_, 1)*term(A_, D_, 3)*term(A_, D_, 5) - 231], [A_, D_], dict=True)
    sols = [s for s in sols if s[D_] > 0]
    assert len(sols) == 1
    a, d = sols[0][A_], sols[0][D_]
    return term(a, d, 2) + term(a, d, 4) + term(a, d, 6)
q("U06-A-058", TOPIC, "Alternate terms of an AP", "Difficult", "Multi-step computation MCQ",
  r"For an increasing arithmetic progression, $a_1 + a_3 + a_5 = 21$ and $a_1 a_3 a_5 = 231$. Then $a_2 + a_4 + a_6$ equals",
  r"$27$",
  [(r"$15$", r"Takes the decreasing choice $d = -2$, ignoring that the AP is increasing."),
   (r"$21$", r"Assumes the even-placed sum equals the odd-placed sum."),
   (r"$33$", r"Writes $a_1, a_5$ as $a_3 \mp d$ instead of $a_3 \mp 2d$, getting $d = 4$.")],
  r"$3a_3 = 21$ so $a_3 = 7$. Then $(7 - 2d)(7)(7 + 2d) = 231$ gives $49 - 4d^2 = 33$, so $d^2 = 4$ and, the AP being increasing, $d = 2$. Hence $a_2 + a_4 + a_6 = 3a_4 = 3(9) = 27$.",
  r"Treating $a_1, a_3, a_5$ as consecutive terms with difference $d$.",
  "U06-A-alternate-terms-trap", "Symmetric alternate terms, a sign choice, then a new sum.",
  check=_c58, values=[27, 15, 21, 33], cognitive="Analysis",
  numerical=dict(question=r"For an increasing arithmetic progression, $a_1 + a_3 + a_5 = 21$ and $a_1 a_3 a_5 = 231$. The value of $a_2 + a_4 + a_6$ is", answer=27))

def _c59():
    d = Symbol('d', real=True)
    # S_9 > S_n for all n != 9 iff a_9 > 0 and a_10 < 0
    c1 = solve_univariate_inequality(term(40, d, 9) > 0, d, relational=False)
    c2 = solve_univariate_inequality(term(40, d, 10) < 0, d, relational=False)
    return Intersection(c1, c2)
q("U06-A-059", TOPIC, "Where the maximum sum occurs", "Difficult", "Inverse/parameter MCQ",
  r"An arithmetic progression has first term $40$ and common difference $d$. The sum $S_9$ of its first $9$ terms is strictly greater than $S_n$ for every natural number $n \ne 9$. The set of all possible values of $d$ is",
  r"$\left(-5, -\frac{40}{9}\right)$",
  [(r"$\left[-5, -\frac{40}{9}\right]$", r"Uses $a_9 \ge 0$ and $a_{10} \le 0$, allowing ties such as $S_8 = S_9$ or $S_9 = S_{10}$."),
   (r"$\left(-\frac{40}{9}, -4\right)$", r"Uses $a + nd$ for the $n$th term, writing $40 + 9d > 0$ and $40 + 10d < 0$."),
   (r"$\left(-\frac{40}{7}, -5\right)$", r"Shifts the index, requiring $a_8 > 0$ and $a_9 < 0$.")],
  r"$S_9$ is the unique maximum exactly when $a_9 > 0$ and $a_{10} < 0$ (then $d < 0$, terms up to $a_9$ are positive and the rest negative). So $40 + 8d > 0$, giving $d > -5$, and $40 + 9d < 0$, giving $d < -\frac{40}{9}$. Hence $d \in \left(-5, -\frac{40}{9}\right)$.",
  r"Allowing a zero term, which creates a tie for the maximum.",
  "U06-A-max-sum-interval", "Translate a strict-maximum condition into strict sign conditions on two terms.",
  check=_c59, values=[Interval.open(-5, Rational(-40, 9)), Interval(-5, Rational(-40, 9)),
                      Interval.open(Rational(-40, 9), -4), Interval.open(Rational(-40, 7), -5)],
  cognitive="Analysis")

q("U06-A-060", TOPIC, "Terms of an AP divisible by a number", "Difficult", "Multi-step computation MCQ",
  r"Consider the first $100$ terms of the arithmetic progression $1, 5, 9, 13, \ldots$. The sum of those among them that are divisible by $3$ is",
  r"$6633$",
  [(r"$7038$", r"Uses the sub-progression $9, 21, \ldots$ but runs it to $405$, which lies beyond the $100$th term $397$."),
   (r"$6435$", r"Uses difference $12$ and $33$ terms but starts at $3$, which is not a term of the given AP."),
   (r"$13266$", r"Drops the factor $\frac{1}{2}$ in the sum.")],
  r"$a_k = 4k - 3$ is divisible by $3$ exactly when $k \equiv 0 \pmod 3$, so the terms are $a_3, a_6, \ldots, a_{99}$, that is $9, 21, \ldots, 393$: $33$ terms with difference $12$. Their sum is $\frac{33}{2}(9 + 393) = 33 \times 201 = 6633$.",
  r"Running the sub-progression past the last available term.",
  "U06-A-sub-AP", "Extract a sub-AP by a divisibility condition and bound it correctly.",
  check=lambda: sum(4*k - 3 for k in range(1, 101) if (4*k - 3) % 3 == 0), values=[6633, 7038, 6435, 13266],
  cognitive="Analysis",
  numerical=dict(question=r"Consider the first $100$ terms of the arithmetic progression $1, 5, 9, 13, \ldots$. The sum of those among them that are divisible by $3$ is", answer=6633))
