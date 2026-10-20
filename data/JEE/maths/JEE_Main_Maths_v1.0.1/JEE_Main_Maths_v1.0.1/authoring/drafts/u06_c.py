import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from sympy.calculus.util import function_range

x = Symbol('x', real=True)
t = Symbol('t', real=True)
r = Symbol('r', real=True)
n = Symbol('n', positive=True)
d = Symbol('d', real=True)
P_, Q_ = symbols('p q', positive=True)

T, F_ = True, False
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TOP_INS = "Insertion of means"
TOP_AMGM = "Relation between AM and GM"
TOP_MIX = "Mixed AP and GP problems"


def _pos_min(f, v, lo=0, hi=oo):
    """Minimum of f over the open interval (lo, hi) from interior critical points."""
    crit = [c for c in solveset(diff(f, v), v, Interval.open(lo, hi))]
    vals = [simplify(f.subs(v, c)) for c in crit]
    return Min(*vals)


def _pos_max(f, v, lo=0, hi=oo):
    crit = [c for c in solveset(diff(f, v), v, Interval.open(lo, hi))]
    vals = [simplify(f.subs(v, c)) for c in crit]
    return Max(*vals)


# ================================================================ EASY
# ---------------------------------------------------------------- 001
def _c001():
    a, b, k = 3, 23, 4
    dd = Rational(b - a, k + 1)
    return a + 3*dd
q("U06-C-001", TOP_INS, "Value of a particular arithmetic mean", "Easy", "Single-step computation MCQ",
  r"Four arithmetic means are inserted between $3$ and $23$. Counting from $3$, the third of these means is",
  r"$15$",
  [(r"$18$", "Divides $23 - 3 = 20$ by $4$ (the number of means) instead of by $5$, so $d = 5$ and the third mean is $3 + 3(5) = 18$."),
   (r"$11$", "Uses the correct $d = 4$ but takes the third term $3 + 2d = 11$ of the progression, which is only the second mean."),
   (r"$13$", "Uses $d = 5$ (dividing by the number of means) and also takes the third term $3 + 2d = 13$.")],
  r"With $4$ means the progression $3, A_1, A_2, A_3, A_4, 23$ has $5$ gaps, so $d = \frac{23-3}{5} = 4$. The third mean is the fourth term: $A_3 = 3 + 3(4) = 15$.",
  "Dividing the gap $b - a$ by the number of means $n$ instead of $n + 1$.",
  "U06-C-am-insert-term", "One idea (common difference with $n+1$ gaps) and one substitution.",
  check=_c001, values=[15, 18, 11, 13], cognitive="Application")

# ---------------------------------------------------------------- 002
def _c002():
    sol = solve(Eq(n*(7 + 43)/2, 200), n)
    return sol[0]
q("U06-C-002", TOP_INS, "Sum of inserted arithmetic means", "Easy", "Inverse/parameter MCQ",
  r"Some arithmetic means are inserted between $7$ and $43$. If the sum of all the inserted means is $200$, the number of means inserted is",
  r"$8$",
  [(r"$6$", r"Treats $200$ as the sum of the whole progression including $7$ and $43$: $(n+2)\cdot 25 = 200$ gives $n = 6$."),
   (r"$4$", r"Uses the sum of the means as $n(a + b) = 50n$, dropping the factor $\frac{1}{2}$, so $n = 4$."),
   (r"$10$", r"Adds the end terms to get $250 = 25 \times 10$ and reports the total number of terms $10$ as the number of means.")],
  r"The sum of $n$ arithmetic means between $a$ and $b$ is $n \cdot \frac{a+b}{2}$. Here $n \cdot \frac{7+43}{2} = 25n = 200$, so $n = 8$.",
  "Including the two given numbers when summing the inserted means.",
  "U06-C-am-insert-sum", "Single property of the sum of AMs applied once.",
  check=_c002, values=[8, 6, 4, 10], cognitive="Application",
  numerical=dict(question=r"Some arithmetic means are inserted between $7$ and $43$. If the sum of all the inserted means is $200$, then the number of means inserted is", answer=8))

# ---------------------------------------------------------------- 003
def _c003():
    rr = [s for s in solve(2*r**4 - 162, r) if s.is_positive][0]
    return sum(2*rr**k for k in (1, 2, 3))
q("U06-C-003", TOP_INS, "Sum of inserted geometric means", "Easy", "Single-step computation MCQ",
  r"Three positive geometric means are inserted between $2$ and $162$. The sum of these three means is",
  r"$78$",
  [(r"$242$", "Adds all five terms $2 + 6 + 18 + 54 + 162$, including the two given numbers."),
   (r"$246$", r"Inserts arithmetic means instead: the sum of three AMs is $3 \cdot \frac{2+162}{2} = 246$."),
   (r"$54$", r"Takes every mean equal to the single geometric mean $\sqrt{2 \cdot 162} = 18$ and adds three of them.")],
  r"The progression $2, G_1, G_2, G_3, 162$ has $162 = 2r^4$, so $r^4 = 81$ and, the means being positive, $r = 3$. The means are $6, 18, 54$, whose sum is $78$.",
  r"Replacing each of several GMs by the single GM $\sqrt{ab}$.",
  "U06-C-gm-insert-term", "Find $r$ from $r^4 = 81$ and add three terms.",
  check=_c003, values=[78, 242, 246, 54], cognitive="Application")

# ---------------------------------------------------------------- 004
def _c004():
    a, b = Rational(1, 3), 243
    rr = [s for s in solve(a*r**6 - b, r) if s.is_positive][0]
    return prod([a*rr**k for k in range(1, 6)])
q("U06-C-004", TOP_INS, "Product of inserted geometric means", "Easy", "Single-step computation MCQ",
  r"Five positive geometric means are inserted between $\frac{1}{3}$ and $243$. The product of these five means is",
  r"$3^{10}$",
  [(r"$3^{20}$", "Uses $(ab)^n = 81^5$ for the product, dropping the half in the exponent."),
   (r"$3^{14}$", "Multiplies all seven terms including the end numbers: $(ab)^{7/2} = 81^{7/2} = 3^{14}$."),
   (r"$3^{8}$", r"Uses the exponent $\frac{n-1}{2} = 2$ in place of $\frac{n}{2}$: $81^{2} = 3^8$.")],
  r"The product of $n$ positive GMs between $a$ and $b$ is $(\sqrt{ab})^n$. Here $ab = \frac{1}{3} \cdot 243 = 81$, so the product is $9^5 = 3^{10}$.",
  "Using $(ab)^n$ instead of $(ab)^{n/2}$ for the product of $n$ GMs.",
  "U06-C-gm-product", "One standard result applied with exponent care.",
  check=_c004, values=[3**10, 3**20, 3**14, 3**8], cognitive="Application")

# ---------------------------------------------------------------- 005
def _c005():
    f = 4**x + 4**(1 - x)
    return _pos_min(f, x, -oo, oo)
q("U06-C-005", TOP_AMGM, "Minimum of a sum of exponentials", "Easy", "Single-step computation MCQ",
  r"The least value of $4^{x} + 4^{1-x}$, $x \in \mathbb{R}$, is",
  r"$4$",
  [(r"$2$", r"Computes $\sqrt{4^x \cdot 4^{1-x}} = 2$ and omits the factor $2$ in $p + q \ge 2\sqrt{pq}$."),
   (r"$5$", "Evaluates the expression at $x = 0$, getting $1 + 4$, without minimising."),
   (r"$8$", r"Takes $2 \cdot 4^x \cdot 4^{1-x} = 8$, dropping the square root in the AM-GM bound.")],
  r"Both terms are positive with product $4^x \cdot 4^{1-x} = 4$. By AM-GM, $4^x + 4^{1-x} \ge 2\sqrt{4} = 4$, with equality when $4^x = 4^{1-x}$, that is $x = \frac{1}{2}$. So the least value is $4$.",
  r"Forgetting the factor $2$ or the square root in $p + q \ge 2\sqrt{pq}$.",
  "U06-C-amgm-exponential", "Direct two-term AM-GM with a constant product.",
  check=_c005, values=[4, 2, 5, 8], cognitive="Application")

# ---------------------------------------------------------------- 006
def _c006():
    a, b = symbols('a b', positive=True)
    sols = solve([a + b - 20, a*b - 64], [a, b], dict=True)
    return Abs(sols[0][a] - sols[0][b])
q("U06-C-006", TOP_AMGM, "Numbers from their AM and GM", "Easy", "Multi-step computation MCQ",
  r"The arithmetic mean of two positive numbers is $10$ and their geometric mean is $8$. The positive difference of the two numbers is",
  r"$12$",
  [(r"$6$", r"Uses $\sqrt{A^2 - G^2} = 6$ and omits the factor $2$ in $|a - b| = 2\sqrt{A^2 - G^2}$."),
   (r"$2$", "Reports $A - G = 10 - 8$ as the difference of the numbers."),
   (r"$36$", "Stops at $A^2 - G^2 = 36$ without the square root or the factor $2$.")],
  r"Here $a + b = 20$ and $ab = 64$. Then $(a-b)^2 = (a+b)^2 - 4ab = 400 - 256 = 144$, so $|a - b| = 12$ (the numbers are $16$ and $4$).",
  "Confusing $A - G$ with the difference of the numbers.",
  "U06-C-numbers-from-means", "Two relations and one identity.",
  check=_c006, values=[12, 6, 2, 36], cognitive="Application",
  numerical=dict(question=r"The arithmetic mean of two positive numbers is $10$ and their geometric mean is $8$. Then the positive difference of the two numbers is", answer=12))

# ---------------------------------------------------------------- 007
def _c007():
    a, b = symbols('a b', positive=True)
    s1 = simplify((a + b)/2 - sqrt(a*b) - (sqrt(a) - sqrt(b))**2/2) == 0
    disc = (2*3)**2 - 4*4**2   # t^2 - (a+b)t + ab with a+b = 6, ab = 16
    s2 = disc >= 0
    return (bool(s1), bool(s2))
q("U06-C-007", TOP_AMGM, "AM greater than GM for distinct numbers", "Easy", "Statement-based MCQ",
  r"Statement I: For any two distinct positive real numbers, their arithmetic mean is greater than their geometric mean. Statement II: There exist two positive real numbers whose arithmetic mean is $3$ and whose geometric mean is $4$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II without testing it against $A \ge G$; the numbers would be roots of $t^2 - 6t + 16 = 0$, which has negative discriminant."),
   (ST_FF, "Thinks AM and GM can be equal for unequal numbers, so rejects Statement I, and also rejects Statement II."),
   (ST_FT, r"Rejects Statement I by allowing equality for distinct numbers and accepts Statement II without checking $A \ge G$.")],
  r"$\frac{a+b}{2} - \sqrt{ab} = \frac{(\sqrt{a} - \sqrt{b})^2}{2} > 0$ when $a \ne b$, so Statement I is true. If the AM were $3$ and the GM $4$, the numbers would satisfy $t^2 - 6t + 16 = 0$, with discriminant $36 - 64 < 0$; also $A < G$ is impossible. Statement II is false.",
  r"Not checking that any proposed pair of AM and GM must satisfy $A \ge G$.",
  "U06-C-amgm-statement-basic", r"Recall of $A \ge G$ and one quick test.",
  check=_c007, values=[(T, F_), (T, T), (F_, F_), (F_, T)], cognitive="Understanding")

# ---------------------------------------------------------------- 008
def _c008():
    xx = [s for s in solve(Eq(x**2, 2*18), x) if s > 0][0]
    yy = solve(Eq(2*Symbol('y'), 2 + 18), Symbol('y'))[0]
    return yy - xx
q("U06-C-008", TOP_INS, "Single AM and single GM", "Easy", "Single-step computation MCQ",
  r"If $2, x, 18$ are in GP with $x > 0$ and $2, y, 18$ are in AP, then $y - x$ equals",
  r"$4$",
  [(r"$16$", "Adds the two means, computing $y + x = 10 + 6$."),
   (r"$7$", r"Takes the GM as $\sqrt{18/2} = 3$, so $y - x = 10 - 3$."),
   (r"$2$", r"Takes the AM as $\frac{18 - 2}{2} = 8$, so $y - x = 8 - 6$.")],
  r"$x = \sqrt{2 \cdot 18} = 6$ and $y = \frac{2 + 18}{2} = 10$, so $y - x = 4$.",
  "Using a quotient or a difference in place of the product or the sum.",
  "U06-C-single-am-gm", "Two one-line means.",
  check=_c008, values=[4, 16, 7, 2], cognitive="Recall")

# ---------------------------------------------------------------- 009
def _c009():
    A, G = 9, 3*sqrt(5)
    a, b = symbols('a b', positive=True)
    s = solve([a + b - 2*A, a*b - G**2], [a, b], dict=True)[0]
    return tuple(Poly(expand((x - s[a])*(x - s[b])), x).all_coeffs())
q("U06-C-009", TOP_AMGM, "Quadratic from AM and GM of roots", "Easy", "Single-step computation MCQ",
  r"Two positive numbers have arithmetic mean $9$ and geometric mean $3\sqrt{5}$. The quadratic equation with leading coefficient $1$ whose roots are these numbers is",
  r"$x^2 - 18x + 45 = 0$",
  [(r"$x^2 - 9x + 45 = 0$", "Uses the AM $9$ itself as the sum of the roots instead of $2A = 18$."),
   (r"$x^2 + 18x + 45 = 0$", r"Sign slip: writes $+(\text{sum})x$ instead of $-(\text{sum})x$."),
   (r"$x^2 - 18x + 3\sqrt{5} = 0$", r"Uses the GM $3\sqrt{5}$ as the product instead of $G^2 = 45$.")],
  r"Sum of roots $= 2A = 18$ and product $= G^2 = 45$, so the equation is $x^2 - 18x + 45 = 0$ (roots $15$ and $3$).",
  "Using $A$ and $G$ directly as the sum and the product of the roots.",
  "U06-C-quadratic-from-means", "Two standard conversions.",
  check=_c009, values=[(1, -18, 45), (1, -9, 45), (1, 18, 45), (1, -18, 3*sqrt(5))], cognitive="Application")

# ---------------------------------------------------------------- 010
def _c010():
    return solve(Eq(5 + (n + 1)*3, 50), n)[0]
q("U06-C-010", TOP_INS, "Number of arithmetic means for a given difference", "Easy", "Inverse/parameter MCQ",
  r"Some arithmetic means are inserted between $5$ and $50$ so that the resulting progression has common difference $3$. The number of means inserted is",
  r"$14$",
  [(r"$15$", r"Takes $\frac{50 - 5}{3} = 15$, the number of gaps, as the number of means."),
   (r"$16$", "Reports the total number of terms $15 + 1 = 16$, which includes $5$ and $50$."),
   (r"$13$", "Subtracts $2$ for the two end numbers from the $15$ gaps, as if the gaps were terms.")],
  r"If $n$ means are inserted, $50$ is the $(n+2)$th term: $50 = 5 + (n+1) \cdot 3$, so $n + 1 = 15$ and $n = 14$.",
  "Mixing up the number of gaps, the number of terms and the number of means.",
  "U06-C-am-insert-count", "One equation with careful counting.",
  check=_c010, values=[14, 15, 16, 13], cognitive="Application",
  numerical=dict(question=r"Some arithmetic means are inserted between $5$ and $50$ so that the resulting progression has common difference $3$. Then the number of means inserted is", answer=14))

# ---------------------------------------------------------------- 011
def _c011():
    b = Symbol('b', positive=True)
    return _pos_min(16/b + 4*b, b)
q("U06-C-011", TOP_AMGM, "Minimum of a linear sum with fixed product", "Easy", "Single-step computation MCQ",
  r"If $a > 0$, $b > 0$ and $ab = 16$, then the least value of $a + 4b$ is",
  r"$16$",
  [(r"$8$", r"Writes $\sqrt{a \cdot 4b} = 8$ and omits the factor $2$ in the AM-GM bound."),
   (r"$20$", "Assumes the minimum occurs at $a = b = 4$, giving $4 + 16$."),
   (r"$32$", r"Simplifies $\sqrt{4ab}$ as $4\sqrt{ab} = 16$ and then doubles it.")],
  r"$a + 4b \ge 2\sqrt{a \cdot 4b} = 2\sqrt{64} = 16$, with equality when $a = 4b$, i.e. $a = 8$, $b = 2$ (and $ab = 16$ holds). So the least value is $16$.",
  "Assuming the extremum occurs when the variables are equal, instead of when the AM-GM terms are equal.",
  "U06-C-amgm-two-term-coeff", "Single AM-GM step with a coefficient.",
  check=_c011, values=[16, 8, 20, 32], cognitive="Application")

# ---------------------------------------------------------------- 012
def _c012():
    rr = [s for s in solve(4*r**3 - 500, r) if s.is_real][0]
    return 4*rr + 4*rr**2
q("U06-C-012", TOP_INS, "Sum of two inserted geometric means", "Easy", "Single-step computation MCQ",
  r"Two real geometric means are inserted between $4$ and $500$. The sum of these two means is",
  r"$120$",
  [(r"$504$", r"Inserts two arithmetic means instead; their sum is $2 \cdot \frac{4+500}{2} = 504$."),
   (r"$624$", "Adds all four terms $4 + 20 + 100 + 500$, including the given numbers."),
   (r"$40\sqrt{5}$", r"Takes each mean as the single GM $\sqrt{4 \cdot 500} = 20\sqrt{5}$.")],
  r"$500 = 4r^3$ gives $r^3 = 125$, and the only real root is $r = 5$. The means are $20$ and $100$, with sum $120$.",
  r"Replacing each GM by $\sqrt{ab}$.",
  "U06-C-gm-insert-term", "Cube root and two terms.",
  check=_c012, values=[120, 504, 624, 40*sqrt(5)], cognitive="Application")

# ---------------------------------------------------------------- 013
def _c013():
    s = Symbol('s', positive=True)
    sol = solve(Eq((s + 4*s)/2 - sqrt(s*4*s), 2), s)[0]
    return 5*sol
q("U06-C-013", TOP_AMGM, "Numbers from AM minus GM", "Easy", "Multi-step computation MCQ",
  r"The arithmetic mean of two positive numbers exceeds their geometric mean by $2$, and the larger number is four times the smaller. The sum of the two numbers is",
  r"$20$",
  [(r"$10$", "Finds the numbers $4$ and $16$ but reports their AM."),
   (r"$\frac{20}{3}$", r"Simplifies the GM $\sqrt{s \cdot 4s}$ as $s$, so $\frac{3s}{2} = 2$, $s = \frac{4}{3}$ and the sum is $5s = \frac{20}{3}$."),
   (r"$16$", "Reports the larger number instead of the sum.")],
  r"Let the numbers be $s$ and $4s$. Then $\frac{5s}{2} - 2s = \frac{s}{2} = 2$, so $s = 4$ and the numbers are $4, 16$ with sum $20$.",
  r"Mis-simplifying $\sqrt{4s^2}$.",
  "U06-C-numbers-from-means", "Set up two means and solve a linear equation.",
  check=_c013, values=[20, 10, Rational(20, 3), 16], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    a, b, c = symbols('a b c', positive=True)
    e = (a + b + c)*(1/a + 1/b + 1/c)
    ident = simplify(e - 9 - ((a - b)**2/(a*b) + (b - c)**2/(b*c) + (c - a)**2/(c*a))) == 0
    return e.subs({a: 1, b: 1, c: 1}) if ident else None
q("U06-C-014", TOP_AMGM, "Product of sum and sum of reciprocals", "Easy", "Single-step computation MCQ",
  r"For positive real numbers $a, b, c$, the least value of $(a + b + c)\left(\frac{1}{a} + \frac{1}{b} + \frac{1}{c}\right)$ is",
  r"$9$",
  [(r"$1$", r"Multiplies the averaged forms $\frac{a+b+c}{3} \ge \sqrt[3]{abc}$ and $\frac{1}{3}\left(\frac{1}{a} + \frac{1}{b} + \frac{1}{c}\right) \ge \frac{1}{\sqrt[3]{abc}}$, losing the factor $3 \cdot 3$."),
   (r"$6$", r"Adds the lower bounds $3\sqrt[3]{abc}$ and $\frac{3}{\sqrt[3]{abc}}$ as $3 + 3$ instead of multiplying them."),
   (r"$15$", "Expands into $3$ plus six cross terms and bounds each cross term by $2$, giving $3 + 12$.")],
  r"By AM-GM, $a + b + c \ge 3\sqrt[3]{abc}$ and $\frac{1}{a} + \frac{1}{b} + \frac{1}{c} \ge \frac{3}{\sqrt[3]{abc}}$. Multiplying, the product is at least $9$, with equality at $a = b = c$.",
  "Bounding cross terms singly instead of in reciprocal pairs.",
  "U06-C-amgm-reciprocal-sum", "Two AM-GM bounds multiplied.",
  check=_c014, values=[9, 1, 6, 15], cognitive="Application")

# ---------------------------------------------------------------- 015
def _c015():
    return solve(Eq(3*2**(n + 1), 96), n)[0]
q("U06-C-015", TOP_INS, "Number of geometric means for a given ratio", "Easy", "Inverse/parameter MCQ",
  r"Some geometric means are inserted between $3$ and $96$ so that the resulting progression has common ratio $2$. The number of means inserted is",
  r"$4$",
  [(r"$5$", "Solves $2^{n} = 32$, treating $96$ as the $(n+1)$th term."),
   (r"$6$", "Reports the total number of terms $6$, which includes $3$ and $96$."),
   (r"$15$", "Treats the power as linear, writing $32 = 2(n + 1)$, so $n = 15$.")],
  r"With $n$ means, $96$ is the $(n+2)$th term: $96 = 3 \cdot 2^{n+1}$, so $2^{n+1} = 32$, $n + 1 = 5$, $n = 4$.",
  "Miscounting terms when the last term is $a r^{n+1}$.",
  "U06-C-gm-insert-count", "One exponential equation.",
  check=_c015, values=[4, 5, 6, 15], cognitive="Application",
  numerical=dict(question=r"Some geometric means are inserted between $3$ and $96$ so that the resulting progression has common ratio $2$. Then the number of means inserted is", answer=4))

# ---------------------------------------------------------------- 016
def _c016():
    a = Symbol('a', positive=True)
    return solve(Eq((9*a)**Rational(3, 2), 216), a)[0]
q("U06-C-016", TOP_INS, "End term from the product of means", "Easy", "Inverse/parameter MCQ",
  r"Three positive geometric means are inserted between a positive number $a$ and $9$. If the product of the three means is $216$, then $a$ equals",
  r"$4$",
  [(r"$24$", "Divides $216$ by $9$, treating the product of means as $9a$."),
   (r"$\frac{2}{3}$", "Uses $(9a)^3 = 216$, so $9a = 6$, dropping the half in the exponent."),
   (r"$36$", "Solves correctly for $9a = 36$ and reports $9a$ instead of $a$.")],
  r"The product of $3$ GMs between $a$ and $9$ is $(\sqrt{9a})^3 = (9a)^{3/2} = 216 = 6^3$. So $\sqrt{9a} = 6$, $9a = 36$ and $a = 4$.",
  "Using $(ab)^n$ for the product of $n$ GMs.",
  "U06-C-gm-product", "Reverse use of one standard result.",
  check=_c016, values=[4, 24, Rational(2, 3), 36], cognitive="Application")

# ---------------------------------------------------------------- 017
def _c017():
    a = Symbol('a', positive=True)
    return _pos_max(a*(12 - a), a, 0, 12)
q("U06-C-017", TOP_AMGM, "Maximum product with fixed sum", "Easy", "Single-step computation MCQ",
  r"If $a > 0$, $b > 0$ and $a + b = 12$, then the greatest value of $ab$ is",
  r"$36$",
  [(r"$144$", "Takes $(a + b)^2$ without dividing by $4$."),
   (r"$72$", r"Uses $\frac{(a + b)^2}{2}$ instead of $\frac{(a+b)^2}{4}$."),
   (r"$6$", r"Reports the greatest value of the GM $\sqrt{ab}$, which is $6$, instead of $ab$.")],
  r"By AM-GM, $\sqrt{ab} \le \frac{a+b}{2} = 6$, so $ab \le 36$, with equality at $a = b = 6$.",
  r"Stopping at the bound for $\sqrt{ab}$.",
  "U06-C-amgm-max-product", "Direct AM-GM.",
  check=_c017, values=[36, 144, 72, 6], cognitive="Recall")

# ---------------------------------------------------------------- 018
def _c018():
    xx, yy = symbols('xx yy', real=True)
    sols = solve([xx + yy - 8, xx*yy - 9], [xx, yy], dict=True)
    return simplify(sols[0][xx]**2 + sols[0][yy]**2)
q("U06-C-018", TOP_MIX, "Same pair in AP and GP", "Easy", "Multi-step computation MCQ",
  r"Positive numbers $x$ and $y$ are such that $x, 4, y$ are in AP and $x, 3, y$ are in GP. Then $x^2 + y^2$ equals",
  r"$46$",
  [(r"$64$", "Uses $(x + y)^2 = 64$ and does not subtract $2xy$."),
   (r"$55$", "Subtracts $xy$ once instead of $2xy$: $64 - 9$."),
   (r"$82$", "Adds $2xy$ instead of subtracting it: $64 + 18$.")],
  r"From the AP, $x + y = 8$; from the GP, $xy = 9$. So $x^2 + y^2 = (x + y)^2 - 2xy = 64 - 18 = 46$.",
  "Sign or factor slip in $(x+y)^2 - 2xy$.",
  "U06-C-ap-gp-same-pair", "Translate two progressions and use one identity.",
  check=_c018, values=[46, 64, 55, 82], cognitive="Application")

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 019
def _c019():
    a, b = 3, 24
    A = Rational(a + b, 2)
    rr = [s for s in solve(a*r**3 - b, r) if s.is_real][0]
    G1, G2 = a*rr, a*rr**2
    return G1**2/G2 + G2**2/G1
q("U06-C-019", TOP_INS, "One AM and two GMs identity", "Medium", "Multi-step computation MCQ",
  r"One arithmetic mean $A$ and two real geometric means $G_1, G_2$ (in that order) are inserted between $3$ and $24$. The value of $\frac{G_1^2}{G_2} + \frac{G_2^2}{G_1}$ is",
  r"$27$",
  [(r"$\frac{27}{2}$", "Recalls the identity value as $A$ rather than $2A$."),
   (r"$18$", r"Interchanges the denominators, computing $\frac{G_1^2}{G_1} + \frac{G_2^2}{G_2} = G_1 + G_2 = 6 + 12$."),
   (r"$54$", "Uses the identity value $2A$ but takes $A = 3 + 24 = 27$ without halving.")],
  r"$24 = 3r^3$ gives $r = 2$, so $G_1 = 6$, $G_2 = 12$. Then $\frac{36}{12} + \frac{144}{6} = 3 + 24 = 27$. This agrees with $\frac{G_1^2}{G_2} + \frac{G_2^2}{G_1} = \frac{G_1^3 + G_2^3}{G_1G_2} = \frac{ab(a+b)}{ab} = a + b = 2A$.",
  "Mixing up the roles of $G_1$ and $G_2$ in the denominators.",
  "U06-C-am-gm-insert-identity", "Find the means, then evaluate a symmetric expression; or recall $2A$.",
  check=_c019, values=[27, Rational(27, 2), 18, 54], cognitive="Application",
  numerical=dict(question=r"One arithmetic mean $A$ and two real geometric means $G_1, G_2$ (in that order) are inserted between $3$ and $24$. Then the value of $\frac{G_1^2}{G_2} + \frac{G_2^2}{G_1}$ is", answer=27))

# ---------------------------------------------------------------- 020
def _c020():
    y = Symbol('y', positive=True)
    return _pos_min(4/y**2 + y, y)
q("U06-C-020", TOP_AMGM, "Splitting terms for AM-GM", "Medium", "Multi-step computation MCQ",
  r"If $x > 0$, $y > 0$ and $xy^2 = 4$, then the least value of $x + y$ is",
  r"$3$",
  [(r"$3\sqrt[3]{4}$", r"Applies three-term AM-GM to $x, y, y$ without halving $y$, i.e. treats $x + y$ as $x + y + y$: $3\sqrt[3]{xy^2} = 3\sqrt[3]{4}$."),
   (r"$2\sqrt[3]{4}$", r"Assumes the minimum occurs at $x = y$, so $x^3 = 4$ and $x + y = 2\sqrt[3]{4}$."),
   (r"$4$", r"Reads the constraint as $xy = 4$ and uses $x + y \ge 2\sqrt{xy} = 4$.")],
  r"Write $x + y = x + \frac{y}{2} + \frac{y}{2} \ge 3\sqrt[3]{\frac{xy^2}{4}} = 3\sqrt[3]{1} = 3$. Equality needs $x = \frac{y}{2}$, which with $xy^2 = 4$ gives $y = 2$, $x = 1$. So the least value is $3$.",
  "Not splitting a term so that the product becomes constant.",
  "U06-C-amgm-split-terms", "Requires the splitting trick and an equality check.",
  check=_c020, values=[3, 3*cbrt(4), 2*cbrt(4), 4], cognitive="Analysis")

# ---------------------------------------------------------------- 021
def _c021():
    sols = solve(Eq((6 - d)*(24 + d), 9**2), d)  # numbers 5-d, 5, 5+d; add 1, 4, 19
    good = [s for s in sols if all(v > 0 for v in (5 - s, 5, 5 + s))]
    s = good[0]
    return Max(5 - s, 5, 5 + s)
q("U06-C-021", TOP_MIX, "AP becomes GP after additions", "Medium", "Multi-step computation MCQ",
  r"Three positive numbers in AP have sum $15$. If $1, 4$ and $19$ are added to them respectively, the resulting numbers are in GP. The largest of the three original numbers is",
  r"$8$",
  [(r"$26$", "Keeps the root $d = -21$, giving $26, 5, -16$, which are not all positive."),
   (r"$27$", "Reports the largest term $8 + 19$ of the GP instead of the original number."),
   (r"$9$", "Reports the middle term $5 + 4$ of the GP as the answer.")],
  r"Let the numbers be $5 - d, 5, 5 + d$. Then $6 - d, 9, 24 + d$ are in GP: $(6 - d)(24 + d) = 81$, so $d^2 + 18d - 63 = 0$, $d = 3$ or $d = -21$. Positivity rejects $d = -21$, so the numbers are $2, 5, 8$ and the largest is $8$.",
  "Not rejecting the root that violates positivity.",
  "U06-C-ap-to-gp-three-numbers", "AP parametrisation, GP condition, quadratic and rejection of a root.",
  check=_c021, values=[8, 26, 27, 9], cognitive="Application")

# ---------------------------------------------------------------- 022
def _c022():
    a = Symbol('a', real=True)
    sols = solve([a*(1 + r + r**2) - 70, 2*5*a*r - (4*a + 4*a*r**2)], [a, r], dict=True)
    mids = {simplify(s[a]*s[r]) for s in sols if s[a] != 0}
    assert len(mids) == 1
    return mids.pop()
q("U06-C-022", TOP_MIX, "GP becomes AP after scaling", "Medium", "Multi-step computation MCQ",
  r"Three numbers are in GP and their sum is $70$. If the first and the third are each multiplied by $4$ and the second by $5$, the resulting numbers are in AP. The middle number of the GP is",
  r"$20$",
  [(r"$\frac{70}{3}$", "Assumes, as for an AP, that the middle term is one third of the sum."),
   (r"$10$", "Finds $r = 2$, $a = 10$ and reports the first term $a$."),
   (r"$40$", "Finds $r = 2$, $a = 10$ and reports the third term $ar^2$.")],
  r"Let the numbers be $a, ar, ar^2$. The AP condition $2(5ar) = 4a + 4ar^2$ gives $2r^2 - 5r + 2 = 0$, so $r = 2$ or $\frac{1}{2}$. Then $a(1 + r + r^2) = 70$ gives $10, 20, 40$ or $40, 20, 10$. Either way the middle number is $20$.",
  "Treating the middle term of a GP as the average.",
  "U06-C-gp-to-ap-three-numbers", "Two conditions, a quadratic in $r$, and noticing both roots give the same middle term.",
  check=_c022, values=[20, Rational(70, 3), 10, 40], cognitive="Application",
  numerical=dict(question=r"Three numbers are in GP and their sum is $70$. If the first and the third are each multiplied by $4$ and the second by $5$, the resulting numbers are in AP. Then the middle number of the GP is", answer=20))

# ---------------------------------------------------------------- 023
def _c023():
    rr = (Q_/P_)**Rational(1, 3)
    A1 = P_ + (Q_ - P_)/3
    A2 = P_ + 2*(Q_ - P_)/3
    G1, G2 = P_*rr, P_*rr**2
    return simplify((A1 + A2)/(G1*G2))
q("U06-C-023", TOP_INS, "Two AMs and two GMs between the same numbers", "Medium", "Multi-step computation MCQ",
  r"Two arithmetic means $A_1, A_2$ and two positive geometric means $G_1, G_2$ are inserted between two positive numbers $p$ and $q$. Then $\frac{A_1 + A_2}{G_1G_2}$ equals",
  r"$\frac{p + q}{pq}$",
  [(r"$\frac{p + q}{2pq}$", r"Takes $A_1 + A_2 = \frac{p+q}{2}$, the single AM, instead of $p + q$."),
   (r"$\frac{2(p + q)}{pq}$", "Takes $A_1 + A_2 = 2(p + q)$, adding the two end numbers for each mean."),
   (r"$\frac{p + q}{\sqrt{pq}}$", r"Takes $G_1G_2 = \sqrt{pq}$, the single GM, instead of $pq$.")],
  r"The AMs are equidistant from the ends, so $A_1 + A_2 = p + q$. With ratio $\rho$, $G_1G_2 = p\rho \cdot p\rho^2 = p^2\rho^3 = p \cdot q$. Hence the ratio is $\frac{p + q}{pq}$.",
  "Replacing the sum of two AMs or the product of two GMs by the single mean.",
  "U06-C-am-gm-insert-identity", "Two separate insertion results combined.",
  check=_c023, values=[(P_ + Q_)/(P_*Q_), (P_ + Q_)/(2*P_*Q_), 2*(P_ + Q_)/(P_*Q_), (P_ + Q_)/sqrt(P_*Q_)], cognitive="Understanding")

# ---------------------------------------------------------------- 024
def _c024():
    xp = Symbol('xp', positive=True)
    return _pos_min((xp + 2)*(xp + 8)/xp, xp)
q("U06-C-024", TOP_AMGM, "Minimum of a rational expression", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, the least value of $\frac{(x + 2)(x + 8)}{x}$ is",
  r"$18$",
  [(r"$8$", r"Minimises only $x + \frac{16}{x} \ge 8$ and drops the constant $10$."),
   (r"$14$", r"Uses $x + \frac{16}{x} \ge \sqrt{16} = 4$, omitting the factor $2$, so gets $10 + 4$."),
   (r"$27$", "Evaluates the expression at $x = 1$ without minimising.")],
  r"$\frac{(x+2)(x+8)}{x} = x + \frac{16}{x} + 10 \ge 2\sqrt{16} + 10 = 18$, with equality at $x = 4$.",
  "Losing the constant term after splitting.",
  "U06-C-amgm-rational-min", "Expand, split and apply AM-GM.",
  check=_c024, values=[18, 8, 14, 27], cognitive="Application",
  numerical=dict(question=r"For $x > 0$, the least value of $\frac{(x + 2)(x + 8)}{x}$ is", answer=18))

# ---------------------------------------------------------------- 025
def _c025():
    a, dd = symbols('a dd', positive=True)
    b, c = a + dd, a + 2*dd
    X, Y = sqrt(a*b), sqrt(b*c)
    tests = [X**2 + Y**2 - 2*b**2, X*Y - b**2, X + Y - 2*b, X**2 + Y**2 - a**2 - c**2]
    return tuple(bool(simplify(e) == 0) for e in tests)
q("U06-C-025", TOP_MIX, "GMs of consecutive AP terms", "Medium", "Conceptual/application MCQ",
  r"Let $a, b, c$ be distinct positive numbers in AP. If $x$ is the positive geometric mean of $a$ and $b$, and $y$ is the positive geometric mean of $b$ and $c$, then which of the following is always true?",
  r"$x^2 + y^2 = 2b^2$",
  [(r"$xy = b^2$", r"Assumes $x, b, y$ are in GP; in fact $x^2y^2 = ab^2c$ and $ac \ne b^2$ for distinct AP terms."),
   (r"$x + y = 2b$", "Assumes $x, b, y$ are in AP; that holds for $x^2, b^2, y^2$, not for $x, b, y$."),
   (r"$x^2 + y^2 = a^2 + c^2$", "Expands $x^2 + y^2 = b(a + c)$ and then replaces $b(a+c)$ by $a^2 + c^2$.")],
  r"$x^2 + y^2 = ab + bc = b(a + c) = b \cdot 2b = 2b^2$, so $x^2, b^2, y^2$ are in AP. The other relations fail, e.g. for $1, 2, 3$: $x = \sqrt{2}$, $y = \sqrt{6}$, $xy = 2\sqrt{3} \ne 4$ and $x + y \ne 4$, $x^2 + y^2 = 8 \ne 10$.",
  "Transferring the AP property from squares to the numbers themselves.",
  "U06-C-ap-gm-squares", "Combines the GM definition with the AP property $a + c = 2b$.",
  check=_c025, values=[(T, F_, F_, F_), (F_, T, F_, F_), (F_, F_, T, F_), (F_, F_, F_, T)], cognitive="Analysis")

# ---------------------------------------------------------------- 026
def _c026():
    t, L = symbols('t L', real=True)
    a, c = 4, 256
    # a^x = b^y = c^z = K, log2 K = L != 0, log2 b = t: x = L/2, y = L/t, z = L/8
    x, y, z = L/log(a, 2), L/t, L/log(c, 2)
    sols = solve(Eq(y**2, simplify(x*z)), t)
    good = [s for s in sols if s > 0]   # b > 1 means log2 b > 0
    return good[0] if len(good) == 1 else None
q("U06-C-026", "Geometric progression", "Exponents in GP, bases unknown", "Medium", "Multi-step computation MCQ",
  r"Let $b > 1$ be a real number and let $x, y, z$ be non-zero real numbers in GP such that $4^x = b^y = 256^z$. Then $\log_2 b$ is",
  r"$4$",
  [(r"$5$", r"Carries the GP of the exponents over to the bases, taking $4, b, 256$ in GP, so $b^2 = 1024$, $b = 32$ and $\log_2 b = 5$."),
   (r"$\frac{16}{5}$", r"Uses the AP condition $2y = x + z$ instead of $y^2 = xz$, giving $\frac{2}{\log_2 b} = \frac{1}{2} + \frac{1}{8}$."),
   (r"$16$", r"Reaches $(\log_2 b)^2 = 2 \cdot 8$ but forgets to take the square root.")],
  r"Let the common value be $K$ and $L = \log_2 K \ne 0$ (since $x \ne 0$). Then $x = \frac{L}{2}$, $y = \frac{L}{\log_2 b}$, $z = \frac{L}{8}$. The GP condition $y^2 = xz$ gives $\frac{L^2}{(\log_2 b)^2} = \frac{L^2}{16}$, so $(\log_2 b)^2 = 16$. Since $b > 1$, $\log_2 b = 4$ (so $b = 16$).",
  r"Mixing up which quantities are in GP: exponents in GP force the logarithms of the bases into GP, not AP.",
  "U06-C-exponents-gp-logs-gp", r"Reverse direction of the usual result: express the exponents through logarithms, apply the GP condition, and use $b > 1$ to pick the sign.",
  check=_c026, values=[4, 5, Rational(16, 5), 16], cognitive="Application",
  numerical=dict(question=r"Let $b > 1$ be a real number and let $x, y, z$ be non-zero real numbers in GP such that $4^x = b^y = 256^z$. Then $\log_2 b$ is", answer=4))

# ---------------------------------------------------------------- 027
def _c027():
    a, b, c = symbols('a b c', positive=True)
    e = (a + b)*(b + c)*(c + a)
    ident = simplify(e - 8*a*b*c - (a*(b - c)**2 + b*(c - a)**2 + c*(a - b)**2)) == 0
    return (e/(a*b*c)).subs({a: 1, b: 1, c: 1}) if ident else None
q("U06-C-027", TOP_AMGM, "Greatest constant in a product inequality", "Medium", "Inverse/parameter MCQ",
  r"The greatest real number $k$ such that $(a + b)(b + c)(c + a) \ge k\,abc$ for all positive real numbers $a, b, c$ is",
  r"$8$",
  [(r"$27$", r"Uses $(a + b + c)^3 \ge 27abc$, a different product."),
   (r"$9$", r"Uses the bound $9$ for $(a + b + c)\left(\frac{1}{a} + \frac{1}{b} + \frac{1}{c}\right)$, a different expression."),
   (r"$6$", r"Adds the three bounds $a + b \ge 2\sqrt{ab}$ etc. as $2 + 2 + 2$ instead of multiplying them.")],
  r"By AM-GM, $a + b \ge 2\sqrt{ab}$, $b + c \ge 2\sqrt{bc}$, $c + a \ge 2\sqrt{ca}$. Multiplying, $(a+b)(b+c)(c+a) \ge 8abc$, and equality at $a = b = c$ shows no larger $k$ works. So $k = 8$.",
  "Multiplying versus adding AM-GM bounds.",
  "U06-C-amgm-cyclic-product", "Three AM-GM bounds multiplied plus a sharpness argument.",
  check=_c027, values=[8, 27, 9, 6], cognitive="Application",
  numerical=dict(question=r"The greatest real number $k$ such that $(a + b)(b + c)(c + a) \ge k\,abc$ for all positive real numbers $a, b, c$ is", answer=8))

# ---------------------------------------------------------------- 028
def _c028():
    X, Y = symbols('X Y', positive=True)
    f = X*Y*(12 - X - 2*Y)/4
    sols = solve([diff(f, X), diff(f, Y)], [X, Y], dict=True)
    vals = [f.subs(s) for s in sols if s[X] > 0 and s[Y] > 0 and (12 - s[X] - 2*s[Y]) > 0]
    return Max(*vals)
q("U06-C-028", TOP_AMGM, "Maximum product with a weighted linear constraint", "Medium", "Multi-step computation MCQ",
  r"If $x, y, z$ are positive real numbers with $x + 2y + 4z = 12$, then the greatest value of $xyz$ is",
  r"$8$",
  [(r"$64$", r"Correctly gets $x \cdot 2y \cdot 4z \le 64$ but does not divide by $8$."),
   (r"$\frac{1728}{343}$", r"Assumes the maximum is at $x = y = z$, so $7x = 12$ and $xyz = \left(\frac{12}{7}\right)^3$."),
   (r"$16$", r"Divides $64$ by $4$ (only the coefficient of $z$) instead of by $2 \cdot 4 = 8$.")],
  r"Apply AM-GM to $x, 2y, 4z$: $\frac{x + 2y + 4z}{3} = 4 \ge \sqrt[3]{8xyz}$, so $8xyz \le 64$ and $xyz \le 8$. Equality at $x = 2y = 4z = 4$, i.e. $(4, 2, 1)$.",
  "Placing equality at equal variables rather than equal AM-GM terms.",
  "U06-C-amgm-max-product", "Choose the right terms for AM-GM, then rescale.",
  check=_c028, values=[8, 64, Rational(1728, 343), 16], cognitive="Application")

# ---------------------------------------------------------------- 029
def _c029():
    rp = Symbol('rp', positive=True)
    sols = solve([3 + 2*d - 3*rp**2, (3 + d) - 3*rp - 6], [d, rp], dict=True)
    return sols[0][d]
q("U06-C-029", TOP_MIX, "AP and GP with common terms", "Medium", "Multi-step computation MCQ",
  r"An AP and a GP with positive terms both have first term $3$ and have equal third terms. If the second term of the AP exceeds the second term of the GP by $6$, then the common difference of the AP is",
  r"$12$",
  [(r"$0$", "Keeps the root $r = -1$, for which the GP $3, -3, 3$ does not have positive terms."),
   (r"$15$", "Writes the third term of the AP as $3 + 3d$; then $d = r^2 - 1$ and $r^2 - 3r - 4 = 0$ give $r = 4$, $d = 15$."),
   (r"$27$", "Finds $r = 3$ and reports the common third term $27$.")],
  r"Third terms: $3 + 2d = 3r^2$. Second terms: $(3 + d) - 3r = 6$. Substituting $d = \frac{3(r^2 - 1)}{2}$ gives $r^2 - 2r - 3 = 0$, so $r = 3$ (positive terms). Then $d = 12$; the sequences are $3, 15, 27$ and $3, 9, 27$.",
  "Ignoring the positivity condition on the GP.",
  "U06-C-ap-gp-shared-terms", "Two simultaneous conditions and a root rejection.",
  check=_c029, values=[12, 0, 15, 27], cognitive="Application",
  numerical=dict(question=r"An AP and a GP with positive terms both have first term $3$ and have equal third terms. If the second term of the AP exceeds the second term of the GP by $6$, then the common difference of the AP is", answer=12))

# ---------------------------------------------------------------- 030
def _c030():
    qq = Symbol('qq', real=True)
    return Intersection(solveset(100 - 4*qq >= 0, qq, S.Reals), solveset(qq > 0, qq, S.Reals))
q("U06-C-030", TOP_AMGM, "AM-GM for roots of a quadratic", "Medium", "Inverse/parameter MCQ",
  r"The equation $x^2 - 10x + q = 0$ has both roots real and positive (the roots may be equal). The set of all possible values of $q$ is",
  r"$(0, 25]$",
  [(r"$(0, 25)$", "Excludes $q = 25$, forgetting that equal roots are allowed (AM equals GM)."),
   (r"$(-\infty, 25]$", r"Uses only the discriminant (or AM $\ge$ GM) and ignores that the product of positive roots must be positive."),
   (r"$[25, \infty)$", r"Reverses the inequality, writing $\sqrt{q} \ge 5$.")],
  r"The roots have AM $5$ and GM $\sqrt{q}$ (with $q > 0$ for positive roots). AM $\ge$ GM gives $\sqrt{q} \le 5$, i.e. $q \le 25$, which is also the discriminant condition $100 - 4q \ge 0$. So $q \in (0, 25]$.",
  "Dropping the positivity of the product of the roots.",
  "U06-C-amgm-quadratic-roots", "Combines AM-GM (or discriminant) with a sign condition.",
  check=_c030, values=[Interval.Lopen(0, 25), Interval.open(0, 25), Interval(-oo, 25), Interval(25, oo)], cognitive="Application")

# ---------------------------------------------------------------- 031
def _c031():
    xp = Symbol('xp', positive=True)
    return _pos_min(xp + 4/(xp - 1), xp, 1, oo)
q("U06-C-031", TOP_AMGM, "Minimum after a shift", "Medium", "Multi-step computation MCQ",
  r"For $x > 1$, the least value of $x + \frac{4}{x - 1}$ is",
  r"$5$",
  [(r"$4$", r"Bounds $(x - 1) + \frac{4}{x-1} \ge 4$ but drops the $+1$ from writing $x = (x - 1) + 1$."),
   (r"$3$", "Writes $x = (x - 1) - 1$, so subtracts $1$ from the bound $4$."),
   (r"$4\sqrt{2}$", r"Applies AM-GM directly to $x$ and $\frac{4}{x-1}$, whose product is not constant, and evaluates $2\sqrt{\frac{4x}{x-1}}$ at $x = 2$.")],
  r"$x + \frac{4}{x-1} = (x - 1) + \frac{4}{x - 1} + 1 \ge 2\sqrt{4} + 1 = 5$, with equality when $x - 1 = 2$, i.e. $x = 3$.",
  "Applying AM-GM to terms whose product is not constant.",
  "U06-C-amgm-rational-min", "Shift to make the product constant, then AM-GM.",
  check=_c031, values=[5, 4, 3, 4*sqrt(2)], cognitive="Application")

# ---------------------------------------------------------------- 032
def _c032():
    rr = [s for s in solve(-2*r**3 - 16, r) if s.is_real][0]
    return -2*rr + (-2)*rr**2
q("U06-C-032", TOP_INS, "Geometric means with a negative end", "Medium", "Multi-step computation MCQ",
  r"Two real geometric means $G_1$ and $G_2$ (in that order) are inserted between $-2$ and $16$. Then $G_1 + G_2$ equals",
  r"$-4$",
  [(r"$-12$", "Takes $r = 2$ from $|r|^3 = 8$, giving $-4$ and $-8$."),
   (r"$12$", "Drops the sign of $-2$ and inserts GMs between $2$ and $16$: $4 + 8$."),
   (r"$14$", "Inserts two arithmetic means instead; their sum is $-2 + 16 = 14$.")],
  r"$16 = -2r^3$ gives $r^3 = -8$, so the real ratio is $r = -2$. The progression is $-2, 4, -8, 16$, hence $G_1 + G_2 = 4 - 8 = -4$.",
  "Ignoring the sign when taking a cube root.",
  "U06-C-gm-insert-sign", "Sign handling with an odd root.",
  check=_c032, values=[-4, -12, 12, 14], cognitive="Application")

# ---------------------------------------------------------------- 033
def _c033():
    a, rr = symbols('a rr', positive=True)
    # Statement I: a + c <= 2b for positive GP; test on a = 1, r = 2
    s1 = bool((1 + 1*2**2) <= 2*(1*2))
    aa, dd = symbols('aa dd', real=True)
    s2 = simplify((aa + dd)**2 - aa*(aa + 2*dd) - dd**2) == 0   # b^2 - ac = d^2 >= 0
    return (s1, bool(s2))
q("U06-C-033", TOP_AMGM, "AM-GM comparisons inside AP and GP", "Medium", "Statement-based MCQ",
  r"Statement I: If $a, b, c$ are positive numbers in GP, then $a + c \le 2b$. Statement II: If $a, b, c$ are real numbers in AP, then $b^2 \ge ac$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I by reversing the AM-GM inequality: in a positive GP $b = \sqrt{ac} \le \frac{a+c}{2}$."),
   (ST_FF, "Rejects Statement II, not noticing $b^2 - ac = d^2$ for any real AP."),
   (ST_TF, r"Reverses both conclusions: takes $a + c \le 2b$ for the GP and $b^2 \le ac$ for the AP.")],
  r"In a positive GP, $b = \sqrt{ac} \le \frac{a + c}{2}$, so $a + c \ge 2b$; for $1, 2, 4$ we get $5 > 4$, so Statement I is false. In an AP with difference $d$, $b^2 - ac = (a + d)^2 - a(a + 2d) = d^2 \ge 0$, so Statement II is true.",
  r"Reversing the direction of AM $\ge$ GM.",
  "U06-C-amgm-statement-ap-gp", "Two inequalities to verify, one needing a counterexample.",
  check=_c033, values=[(F_, T), (T, T), (F_, F_), (T, F_)], cognitive="Analysis")

# ---------------------------------------------------------------- 034
def _c034():
    s1 = bool((-1 + 1/Integer(-1)) >= 2)    # x = -1 gives -2, so 2 is not the minimum
    a = Symbol('a', positive=True)
    m = _pos_min(1/a + 1/(1 - a), a, 0, 1)
    return (s1, bool(m == 2))
q("U06-C-034", TOP_AMGM, "Traps in applying AM-GM", "Medium", "Statement-based MCQ",
  r"Statement I: The minimum value of $x + \frac{1}{x}$ over all non-zero real numbers $x$ is $2$. Statement II: If $a > 0$, $b > 0$ and $a + b = 1$, then the minimum value of $\frac{1}{a} + \frac{1}{b}$ is $2$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Applies AM-GM in Statement I without requiring $x > 0$, and in Statement II uses $\frac{1}{a} + \frac{1}{b} \ge 2\sqrt{\frac{1}{ab}}$ with $ab = 1$."),
   (ST_TF, "Applies AM-GM in Statement I without requiring $x > 0$, but evaluates Statement II correctly."),
   (ST_FT, r"Notices negative $x$ in Statement I, but in Statement II treats $\frac{1}{a} \cdot \frac{1}{b}$ as $1$.")],
  r"For $x < 0$, $x + \frac{1}{x} \le -2$, and the expression is unbounded below, so it has no minimum; Statement I is false. In Statement II, $ab \le \frac{1}{4}$, so $\frac{1}{a} + \frac{1}{b} = \frac{1}{ab} \ge 4$, with equality at $a = b = \frac{1}{2}$; the minimum is $4$, not $2$. Both statements are false.",
  "Using AM-GM for terms that can be negative, or with a product that is not $1$.",
  "U06-C-amgm-statement-traps", "Two separate traps in conditions of AM-GM.",
  check=_c034, values=[(F_, F_), (T, T), (T, F_), (F_, T)], cognitive="Analysis")

# ---------------------------------------------------------------- 035
def _c035():
    dd = solve(Eq((20 + d)*3, 80 - d), d)[0]
    return solve(Eq(20 + (n + 1)*dd, 80), n)[0]
q("U06-C-035", TOP_INS, "Number of AMs from a ratio of means", "Medium", "Inverse/parameter MCQ",
  r"Some arithmetic means are inserted between $20$ and $80$. If the ratio of the first mean to the last mean is $1 : 3$, then the number of means inserted is",
  r"$11$",
  [(r"$12$", r"Finds $d = 5$ and takes $\frac{60}{5} = 12$, the number of gaps, as the number of means."),
   (r"$13$", "Reports the total number of terms $13$, which includes $20$ and $80$."),
   (r"$10$", "Subtracts $2$ for the end numbers from the $12$ gaps, as if the gaps were terms.")],
  r"The first mean is $20 + d$ and the last is $80 - d$. From $3(20 + d) = 80 - d$, $d = 5$. Then $80 = 20 + (n + 1) \cdot 5$ gives $n = 11$.",
  "Confusing the number of gaps with the number of means.",
  "U06-C-am-insert-ratio", "Uses the first and last means symmetrically, then counts.",
  check=_c035, values=[11, 12, 13, 10], cognitive="Application",
  numerical=dict(question=r"Some arithmetic means are inserted between $20$ and $80$. If the ratio of the first mean to the last mean is $1 : 3$, then the number of means inserted is", answer=11))

# ---------------------------------------------------------------- 036
def _c036():
    a = Symbol('a', real=True)
    dd = Symbol('dd', real=True, nonzero=True)
    sol = solve(Eq((a + 4*dd)**2, (a + dd)*(a + 8*dd)), a)
    av = sol[0]
    return simplify((av + 4*dd)/(av + dd))
q("U06-C-036", TOP_MIX, "AP terms forming a GP", "Medium", "Multi-step computation MCQ",
  r"The $2$nd, $5$th and $9$th terms of a non-constant AP are, in that order, three consecutive terms of a GP. The common ratio of this GP is",
  r"$\frac{4}{3}$",
  [(r"$\frac{3}{4}$", "Inverts the ratio, dividing the $2$nd term by the $5$th."),
   (r"$\frac{5}{2}$", "Takes the ratio of the term positions $5$ and $2$."),
   (r"$\frac{9}{5}$", "Takes the ratio of the term positions $9$ and $5$.")],
  r"With first term $a$ and difference $d \ne 0$: $(a + 4d)^2 = (a + d)(a + 8d)$ gives $8d^2 = ad$, so $a = 8d$. The terms are $9d, 12d, 16d$, and the ratio is $\frac{12d}{9d} = \frac{4}{3}$.",
  "Using positions of terms in place of the terms themselves.",
  "U06-C-ap-terms-in-gp", "GP condition on AP terms, then a ratio.",
  check=_c036, values=[Rational(4, 3), Rational(3, 4), Rational(5, 2), Rational(9, 5)], cognitive="Application")

# ---------------------------------------------------------------- 037
def _c037():
    a, b = symbols('a b', positive=True)
    k = 1
    sols = solve([a + b - 2*5*k, a*b - (4*k)**2], [a, b], dict=True)
    s = [s for s in sols if s[a] > s[b]][0]
    return s[a]/s[b]
q("U06-C-037", TOP_AMGM, "Ratio of numbers from the ratio A : G", "Medium", "Multi-step computation MCQ",
  r"The arithmetic mean and the geometric mean of two positive numbers $a$ and $b$ $(a > b)$ are in the ratio $5 : 4$. Then $a : b$ is",
  r"$4 : 1$",
  [(r"$5 : 4$", "Takes the ratio of the numbers to be the ratio of their means."),
   (r"$25 : 16$", "Squares the ratio of the means, $A^2 : G^2$."),
   (r"$9 : 1$", r"Uses $(A + G) : (A - G)$ instead of $(A + \sqrt{A^2 - G^2}) : (A - \sqrt{A^2 - G^2})$.")],
  r"Take $A = 5k$, $G = 4k$. Then $a + b = 10k$ and $ab = 16k^2$, so $a, b$ are roots of $t^2 - 10kt + 16k^2 = 0$, i.e. $8k$ and $2k$. Hence $a : b = 4 : 1$.",
  "Equating the ratio of the means with the ratio of the numbers.",
  "U06-C-ratio-from-means", "Convert means to sum and product, then solve a quadratic.",
  check=_c037, values=[4, Rational(5, 4), Rational(25, 16), 9], cognitive="Application")

# ---------------------------------------------------------------- 038
def _c038():
    a, b = symbols('a b', positive=True)
    sols = solve([a + b - 4, a*b - 1], [a, b], dict=True)  # A = 2, G = 1
    s = [s for s in sols if s[a] > s[b]][0]
    return simplify(s[a]/s[b])
q("U06-C-038", TOP_AMGM, "Ratio when AM is twice GM", "Medium", "Multi-step computation MCQ",
  r"The arithmetic mean of two positive numbers $a$ and $b$ $(a > b)$ is twice their geometric mean. Then $a : b$ is",
  r"$(7 + 4\sqrt{3}) : 1$",
  [(r"$(2 + \sqrt{3}) : 1$", r"Solves $u^2 - 4u + 1 = 0$ for $u = \sqrt{a/b}$ and forgets to square $u$."),
   (r"$(9 + 4\sqrt{5}) : 1$", r"Sign slip: solves $u^2 - 4u - 1 = 0$, getting $u = 2 + \sqrt{5}$, and squares it."),
   (r"$4 : 1$", "Takes $a : b = A^2 : G^2 = 4 : 1$.")],
  r"$\frac{a + b}{2} = 2\sqrt{ab}$. Dividing by $b$ and putting $u = \sqrt{a/b}$: $u^2 - 4u + 1 = 0$, so $u = 2 + \sqrt{3}$ (as $a > b$). Hence $\frac{a}{b} = (2 + \sqrt{3})^2 = 7 + 4\sqrt{3}$.",
  r"Forgetting that the quadratic is in $\sqrt{a/b}$, not $a/b$.",
  "U06-C-ratio-from-means", r"Substitution $u = \sqrt{a/b}$, quadratic and squaring.",
  check=_c038, values=[7 + 4*sqrt(3), 2 + sqrt(3), 9 + 4*sqrt(5), 4], cognitive="Application")

# ---------------------------------------------------------------- 039
def _c039():
    xp = Symbol('xp', positive=True)
    return _pos_min(xp**2 + 16/xp, xp)
q("U06-C-039", TOP_AMGM, "Splitting a reciprocal term", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, the least value of $x^2 + \frac{16}{x}$ is",
  r"$12$",
  [(r"$8\sqrt[3]{4}$", r"Sets the two terms equal, $x^2 = \frac{16}{x}$, and evaluates $2x^2$ at $x = \sqrt[3]{16}$."),
   (r"$12\sqrt[3]{4}$", r"Splits as $x^2 + \frac{16}{x} + \frac{16}{x}$ without halving, giving $3\sqrt[3]{256}$."),
   (r"$8$", r"Uses $2\sqrt{x \cdot \frac{16}{x}} = 8$ as if the expression were $x + \frac{16}{x}$.")],
  r"Write $x^2 + \frac{8}{x} + \frac{8}{x} \ge 3\sqrt[3]{x^2 \cdot \frac{64}{x^2}} = 3 \cdot 4 = 12$, with equality when $x^2 = \frac{8}{x}$, i.e. $x = 2$.",
  "Equating the original two terms instead of the split terms.",
  "U06-C-amgm-split-terms", "Needs an unequal split into three terms.",
  check=_c039, values=[12, 8*cbrt(4), 12*cbrt(4), 8], cognitive="Application",
  numerical=dict(question=r"For $x > 0$, the least value of $x^2 + \frac{16}{x}$ is", answer=12))

# ---------------------------------------------------------------- 040
def _c040():
    xp = Symbol('xp', positive=True)
    return function_range(xp/(xp**2 + xp + 1), xp, Interval.open(0, oo))
q("U06-C-040", TOP_AMGM, "Range using AM-GM", "Medium", "Multi-step computation MCQ",
  r"The range of $f(x) = \frac{x}{x^2 + x + 1}$ for $x > 0$ is",
  r"$\left(0, \frac{1}{3}\right]$",
  [(r"$\left(0, \frac{1}{3}\right)$", r"Thinks the bound $x + \frac{1}{x} \ge 2$ is never attained, missing $x = 1$."),
   (r"$\left(0, \frac{1}{2}\right]$", r"Drops the middle term $x$ and bounds $\frac{x}{x^2 + 1} \le \frac{1}{2}$."),
   (r"$\left(0, 3\right]$", r"Finds $\frac{x^2 + x + 1}{x} \ge 3$ but does not take the reciprocal of the bound.")],
  r"$\frac{1}{f(x)} = x + \frac{1}{x} + 1 \ge 3$ for $x > 0$, with equality at $x = 1$, and $\frac{1}{f}$ takes every value in $[3, \infty)$. Hence $f(x) \in \left(0, \frac{1}{3}\right]$.",
  "Inverting an inequality without care.",
  "U06-C-amgm-range", "AM-GM on the reciprocal, then invert.",
  check=_c040, values=[Interval.Lopen(0, Rational(1, 3)), Interval.open(0, Rational(1, 3)), Interval.Lopen(0, Rational(1, 2)), Interval.Lopen(0, 3)], cognitive="Application")

# ---------------------------------------------------------------- 041
def _c041():
    tp = Symbol('tp', positive=True)
    Lk = Symbol('Lk', positive=True)   # log_3 k, must be > 0 for a finite least value
    xx = 3**tp                         # x > 1 means t = log_3 x > 0
    f = expand_log(log(xx, 3) + Lk*log(3)/log(xx), force=True)
    least = _pos_min(simplify(f), tp)
    sol = solve(Eq(least, 6), Lk)
    return 3**sol[0] if len(sol) == 1 else None
q("U06-C-041", TOP_AMGM, "AM-GM with logarithms, unknown base constant", "Medium", "Inverse/parameter MCQ",
  r"Let $k > 1$. If the least value of $\log_3 x + \log_x k$ over all $x > 1$ is $6$, then $k$ equals",
  r"$3^{9}$",
  [(r"$3^{36}$", r"Writes the least value of $t + \frac{c}{t}$ as $\sqrt{c}$, dropping the factor $2$, so $\sqrt{c} = 6$ and $\log_3 k = 36$."),
   (r"$3^{3}$", r"Writes the least value as $2c$, dropping the square root, so $2c = 6$ and $\log_3 k = 3$."),
   (r"$3^{2}$", r"Finds $\log_3 k = 9$ correctly but then takes $k = 9$, forgetting to exponentiate.")],
  r"Let $t = \log_3 x > 0$ and $c = \log_3 k > 0$. Then $\log_x k = \frac{\log_3 k}{\log_3 x} = \frac{c}{t}$, so the expression is $t + \frac{c}{t} \ge 2\sqrt{c}$, with equality at $t = \sqrt{c}$, which is attainable. Hence $2\sqrt{c} = 6$, $c = 9$ and $k = 3^{9}$.",
  r"Misapplying $p + q \ge 2\sqrt{pq}$ (dropping the $2$ or the root), or confusing $\log_3 k$ with $k$.",
  "U06-C-amgm-logs-param", "Reverse AM-GM: the least value is given and the constant inside the logarithm is found.",
  check=_c041, values=[3**9, 3**36, 3**3, 3**2], cognitive="Application")

# ---------------------------------------------------------------- 042
def _c042():
    return solve(Eq(n*Rational(13, 6)/2, n + 1), n)[0]
q("U06-C-042", TOP_INS, "Count of means from their sum", "Medium", "Inverse/parameter MCQ",
  r"Some arithmetic means are inserted between two numbers whose sum is $\frac{13}{6}$. If the sum of the inserted means exceeds the number of means by $1$, then the number of means is",
  r"$12$",
  [(r"$14$", "Reports the total number of terms $n + 2$."),
   (r"$13$", "Reports the number of gaps $n + 1$."),
   (r"$6$", "Halves the answer, counting pairs of means equidistant from the ends.")],
  r"If $n$ means are inserted, their sum is $n \cdot \frac{13/6}{2} = \frac{13n}{12}$. So $\frac{13n}{12} = n + 1$, giving $\frac{n}{12} = 1$ and $n = 12$.",
  "Confusing the number of means with the number of terms.",
  "U06-C-am-insert-sum", "Set up an equation with the sum of AMs.",
  check=_c042, values=[12, 14, 13, 6], cognitive="Application",
  numerical=dict(question=r"Some arithmetic means are inserted between two numbers whose sum is $\frac{13}{6}$. If the sum of the inserted means exceeds the number of means by $1$, then the number of means is", answer=12))

# ---------------------------------------------------------------- 043
def _c043():
    a, b = 1, 64
    dd = Rational(b - a, 4)
    A2 = a + 2*dd
    rr = [s for s in solve(a*r**4 - b, r) if s.is_positive][0]
    G2 = a*rr**2
    return A2 - G2
q("U06-C-043", TOP_INS, "Comparing a middle AM and a middle GM", "Medium", "Multi-step computation MCQ",
  r"Three arithmetic means $A_1, A_2, A_3$ and three positive geometric means $G_1, G_2, G_3$ are inserted between $1$ and $64$ (each set in increasing order). Then $A_2 - G_2$ equals",
  r"$\frac{49}{2}$",
  [(r"$\frac{33}{2}$", "Takes $r^3 = 64$, so $r = 4$ and $G_2 = 16$, using one gap too few."),
   (r"$35$", r"Takes $d = \frac{63}{3} = 21$, so $A_2 = 43$, using one gap too few, and $43 - 8$."),
   (r"$27$", "Uses one gap too few in both: $A_2 = 43$ and $G_2 = 16$.")],
  r"With $3$ means there are $4$ gaps. $d = \frac{63}{4}$, so $A_2 = 1 + \frac{63}{2} = \frac{65}{2}$ (the AM of $1$ and $64$). $r^4 = 64$ gives $r = 2\sqrt{2}$, so $G_2 = r^2 = 8 = \sqrt{64}$. Hence $A_2 - G_2 = \frac{65}{2} - 8 = \frac{49}{2}$.",
  "Using $n$ gaps instead of $n + 1$ when inserting $n$ means.",
  "U06-C-middle-am-gm", "Insert both kinds of means and compare.",
  check=_c043, values=[Rational(49, 2), Rational(33, 2), 35, 27], cognitive="Application")

# ---------------------------------------------------------------- 044
def _c044():
    sols = solve(Eq(2*3*r, 1 + 5*r**2), r)  # a, ar, ar^2 with a, 3b, 5c in AP (a cancels, a != 0)
    good = [s for s in sols if s != 1]
    return good[0]
q("U06-C-044", TOP_MIX, "GP terms with weighted AP", "Medium", "Inverse/parameter MCQ",
  r"Three distinct non-zero real numbers $a, b, c$ are in GP, and $a, 3b, 5c$ are in AP. The common ratio of the GP is",
  r"$\frac{1}{5}$",
  [(r"$5$", r"Divides $5r^2 - 6r + 1 = 0$ by $r^2$, solves $s^2 - 6s + 5 = 0$ for $s = \frac{1}{r}$ and reports $s = 5$ as the ratio."),
   (r"$-\frac{1}{5}$", "Sign slip when factorising $5r^2 - 6r + 1 = (5r - 1)(r - 1)$."),
   (r"$\frac{6}{5}$", "Reports the sum of the roots of $5r^2 - 6r + 1 = 0$ instead of rejecting $r = 1$.")],
  r"Write $b = ar$, $c = ar^2$. The AP condition $2(3ar) = a + 5ar^2$ gives $5r^2 - 6r + 1 = 0$, so $r = 1$ or $\frac{1}{5}$. Since the numbers are distinct, $r \ne 1$, so $r = \frac{1}{5}$.",
  "Forgetting to reject $r = 1$ for distinct terms.",
  "U06-C-gp-weighted-ap", "Two progression conditions and a rejected root.",
  check=_c044, values=[Rational(1, 5), 5, Rational(-1, 5), Rational(6, 5)], cognitive="Application")

# ---------------------------------------------------------------- 045
def _c045():
    xp = Symbol('xp', positive=True)
    return _pos_max(xp**2*(6 - xp), xp, 0, 6)
q("U06-C-045", TOP_AMGM, "Maximum of a weighted product", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < 6$, the greatest value of $x^2(6 - x)$ is",
  r"$32$",
  [(r"$27$", "Assumes the maximum is at the midpoint $x = 3$."),
   (r"$8$", "Applies AM-GM to $x, x, 6 - x$ as if their sum were $6$, getting $2^3$."),
   (r"$64$", r"Splits as $x, x, 12 - 2x$ (sum $12$), gets $x^2(12 - 2x) \le 64$ and forgets to divide by $2$.")],
  r"Write $x^2(6 - x) = 4 \cdot \frac{x}{2} \cdot \frac{x}{2} \cdot (6 - x)$. The three factors have sum $6$, so their product is at most $2^3 = 8$. Hence $x^2(6 - x) \le 32$, with equality at $\frac{x}{2} = 6 - x$, i.e. $x = 4$.",
  "Not adjusting the factors so that their sum is constant.",
  "U06-C-amgm-weighted", "Weighted splitting for a constant sum.",
  check=_c045, values=[32, 27, 8, 64], cognitive="Application",
  numerical=dict(question=r"For $0 < x < 6$, the greatest value of $x^2(6 - x)$ is", answer=32))

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 046
def _c046():
    a, b = symbols('a b', real=True)
    f = a*b**2*(6 - a - b)**3
    sols = solve([diff(f, a), diff(f, b)], [a, b], dict=True)
    sols = [s for s in sols if a in s and b in s and s[a].is_number and s[b].is_number]
    vals = [f.subs(s) for s in sols if s[a] > 0 and s[b] > 0 and 6 - s[a] - s[b] > 0]
    return Max(*vals)
q("U06-C-046", TOP_AMGM, "Weighted AM-GM with three variables", "Difficult", "Multi-step computation MCQ",
  r"If $a, b, c$ are positive real numbers with $a + b + c = 6$, then the greatest value of $ab^2c^3$ is",
  r"$108$",
  [(r"$8$", r"Applies AM-GM to $a, b, c$ directly and reports the bound $abc \le 8$."),
   (r"$64$", r"Assumes the maximum is at $a = b = c = 2$, giving $2 \cdot 4 \cdot 8$."),
   (r"$1$", r"Gets $a\left(\frac{b}{2}\right)^2\left(\frac{c}{3}\right)^3 \le 1$ and forgets to multiply by $2^2 \cdot 3^3$.")],
  r"Split into six terms: $a, \frac{b}{2}, \frac{b}{2}, \frac{c}{3}, \frac{c}{3}, \frac{c}{3}$, with sum $6$. AM-GM gives $a \cdot \frac{b^2}{4} \cdot \frac{c^3}{27} \le 1$, so $ab^2c^3 \le 108$. Equality at $a = \frac{b}{2} = \frac{c}{3} = 1$, i.e. $(1, 2, 3)$.",
  "Placing equality at equal variables in a weighted product.",
  "U06-C-amgm-weighted", "Weighted splitting into six terms and rescaling.",
  check=_c046, values=[108, 8, 64, 1], cognitive="Analysis",
  numerical=dict(question=r"If $a, b, c$ are positive real numbers with $a + b + c = 6$, then the greatest value of $ab^2c^3$ is", answer=108))

# ---------------------------------------------------------------- 047
def _c047():
    f = 2**sin(x) + 2**cos(x)
    cand = simplify(f.subs(x, 5*pi/4))
    grid = min(float(f.subs(x, 2*pi*k/2000).evalf()) for k in range(2000))
    assert grid >= float(cand) - 1e-9 and grid - float(cand) < 1e-4
    return cand
q("U06-C-047", TOP_AMGM, "Two-stage AM-GM with trigonometric exponents", "Difficult", "Multi-step computation MCQ",
  r"The least value of $2^{\sin x} + 2^{\cos x}$, $x \in \mathbb{R}$, is",
  r"$2^{1 - \frac{1}{\sqrt{2}}}$",
  [(r"$2^{1 - \sqrt{2}}$", r"Uses $\sin x + \cos x \ge -\sqrt{2}$ but forgets to halve the exponent under the square root."),
   (r"$1$", "Adds the separate minima $2^{-1} + 2^{-1}$, which cannot occur at the same $x$."),
   (r"$2^{1 + \frac{1}{\sqrt{2}}}$", r"Uses the maximum $\sqrt{2}$ of $\sin x + \cos x$ in place of the minimum $-\sqrt{2}$.")],
  r"By AM-GM, $2^{\sin x} + 2^{\cos x} \ge 2\sqrt{2^{\sin x + \cos x}} = 2^{1 + \frac{\sin x + \cos x}{2}}$. Since $\sin x + \cos x \ge -\sqrt{2}$, this is at least $2^{1 - \frac{1}{\sqrt{2}}}$. Both equalities hold at $x = \frac{5\pi}{4}$, where $\sin x = \cos x = -\frac{1}{\sqrt{2}}$.",
  "Combining bounds that are not attained simultaneously.",
  "U06-C-amgm-trig-exponential", "AM-GM followed by a trigonometric bound, with a simultaneous-equality check.",
  check=_c047, values=[2**(1 - 1/sqrt(2)), 2**(1 - sqrt(2)), 1, 2**(1 + 1/sqrt(2))], cognitive="Analysis")

# ---------------------------------------------------------------- 048
def _c048():
    a, b, c = symbols('a b c', real=True)
    sols = solve([a + b + c - Rational(3, 2), 2*b - a - c, b**4 - a**2*c**2], [a, b, c], dict=True)
    good = [s for s in sols if s[a] < s[b] < s[c]]
    assert len(good) == 1
    return simplify(good[0][a])
q("U06-C-048", TOP_MIX, "AP whose squares form a GP", "Difficult", "Multi-step computation MCQ",
  r"Real numbers $a, b, c$ with $a < b < c$ are in AP, and $a^2, b^2, c^2$ are in GP. If $a + b + c = \frac{3}{2}$, then $a$ equals",
  r"$\frac{1}{2} - \frac{1}{\sqrt{2}}$",
  [(r"$\frac{1 - \sqrt{3}}{2}$", r"Writes $ac = -b = -\frac{1}{2}$ instead of $ac = -b^2$, solving $t^2 - t - \frac{1}{2} = 0$."),
   (r"$-\frac{1}{2} - \frac{1}{\sqrt{2}}$", r"Sign slip in the quadratic: uses $t^2 + t - \frac{1}{4} = 0$ for $a, c$."),
   (r"$\frac{1}{2} - \sqrt{2}$", r"Solves $t^2 - t - \frac{1}{4} = 0$ but halves only the $1$, writing $t = \frac{1}{2} \pm \sqrt{2}$.")],
  r"From the AP, $b = \frac{1}{2}$ and $a + c = 1$. From the GP, $b^4 = a^2c^2$, so $ac = \pm\frac{1}{4}$. If $ac = \frac{1}{4}$ then $a = c = \frac{1}{2}$, contradicting $a < c$. So $ac = -\frac{1}{4}$ and $a, c$ are roots of $t^2 - t - \frac{1}{4} = 0$, i.e. $\frac{1 \pm \sqrt{2}}{2}$. Thus $a = \frac{1}{2} - \frac{1}{\sqrt{2}}$.",
  "Taking only $ac = b^2$ from $b^4 = a^2c^2$.",
  "U06-C-ap-squares-gp", r"Casework on $ac = \pm b^2$ with a strict-order condition.",
  check=_c048, values=[Rational(1, 2) - 1/sqrt(2), (1 - sqrt(3))/2, -Rational(1, 2) - 1/sqrt(2), Rational(1, 2) - sqrt(2)], cognitive="Analysis")

# ---------------------------------------------------------------- 049
def _c049():
    a, b, c, e = symbols('a b c e', positive=True)
    expr = expand((1 + a)*(1 + b)*(1 + c)*(1 + e))
    at_eq = expr.subs({a: 2, b: 2, c: 2, e: 2})
    bound = sum(binomial(4, k)*Integer(16)**Rational(k, 4) for k in range(5))
    assert at_eq == bound
    return bound
q("U06-C-049", TOP_AMGM, "Minimum of a product with fixed abcd", "Difficult", "Multi-step computation MCQ",
  r"If $a, b, c, d$ are positive real numbers with $abcd = 16$, then the least value of $(1 + a)(1 + b)(1 + c)(1 + d)$ is",
  r"$81$",
  [(r"$64$", r"Uses $1 + a \ge 2\sqrt{a}$ for each factor, giving $16\sqrt{abcd} = 64$; equality would need $a = b = c = d = 1$, which violates $abcd = 16$."),
   (r"$17$", "Keeps only the terms $1$ and $abcd$ of the expansion."),
   (r"$73$", "Expands but counts only $4$ pairwise products instead of $6$: $1 + 8 + 16 + 32 + 16$.")],
  r"Expanding, the product is $1 + \sum a + \sum ab + \sum abc + abcd$. By AM-GM, $\sum a \ge 4(abcd)^{1/4} = 8$, $\sum ab \ge 6(abcd)^{1/2} = 24$, $\sum abc \ge 4(abcd)^{3/4} = 32$. So the product is at least $1 + 8 + 24 + 32 + 16 = 81$, attained at $a = b = c = d = 2$.",
  "Using an AM-GM bound whose equality case is incompatible with the constraint.",
  "U06-C-amgm-product-expansion", "Expansion plus three AM-GM bounds, and a trap with an unattainable bound.",
  check=_c049, values=[81, 64, 17, 73], cognitive="Analysis",
  numerical=dict(question=r"If $a, b, c, d$ are positive real numbers with $abcd = 16$, then the least value of $(1 + a)(1 + b)(1 + c)(1 + d)$ is", answer=81))

# ---------------------------------------------------------------- 050
def _c050():
    g = r + 1 + 1/r
    neg = function_range(g, r, Interval.open(-oo, 0))
    pos = function_range(g, r, Interval.open(0, oo))
    return Union(neg, pos)
q("U06-C-050", TOP_AMGM, "Range of sum over middle term in a GP", "Difficult", "Inverse/parameter MCQ",
  r"Let $a, b, c$ be non-zero real numbers in GP (with real common ratio). If $a + b + c = kb$, then the set of all possible values of $k$ is",
  r"$(-\infty, -1] \cup [3, \infty)$",
  [(r"$[3, \infty)$", "Assumes the common ratio is positive and loses the negative branch."),
   (r"$(-\infty, -1) \cup (3, \infty)$", "Excludes the endpoints, forgetting $r = 1$ and $r = -1$ are allowed."),
   (r"$(-\infty, -3] \cup [1, \infty)$", r"Sign slip: writes $k = r + \frac{1}{r} - 1$ instead of $r + \frac{1}{r} + 1$.")],
  r"With ratio $r$, $k = \frac{a + ar + ar^2}{ar} = r + \frac{1}{r} + 1$. For real $r \ne 0$, $r + \frac{1}{r} \ge 2$ (if $r > 0$) or $\le -2$ (if $r < 0$), with equality at $r = \pm 1$. So $k \ge 3$ or $k \le -1$.",
  "Ignoring negative common ratios when using AM-GM.",
  "U06-C-gp-sum-range", "AM-GM with sign casework on the ratio.",
  check=_c050, values=[Union(Interval(-oo, -1), Interval(3, oo)), Interval(3, oo), Union(Interval.open(-oo, -1), Interval.open(3, oo)), Union(Interval(-oo, -3), Interval(1, oo))], cognitive="Analysis")

# ---------------------------------------------------------------- 051
def _c051():
    a, b = symbols('a b', positive=True)
    nn, m = 10, 4
    first = a + m*(2*b - a)/(nn + 1)
    second = 2*a + m*(b - 2*a)/(nn + 1)
    sol = solve(Eq(first, second), a)[0]
    return simplify(sol/b)
q("U06-C-051", TOP_INS, "Equal means in two insertions", "Difficult", "Inverse/parameter MCQ",
  r"Ten arithmetic means are inserted between $a$ and $2b$, and ten arithmetic means are inserted between $2a$ and $b$, where $a, b > 0$. If the $4$th mean (counting from $a$ and from $2a$ respectively) is the same in both cases, then $a : b$ is",
  r"$4 : 7$",
  [(r"$7 : 4$", "Solves $4b = 7a$ correctly but writes the ratio the other way round."),
   (r"$2 : 3$", r"Uses $d = \frac{2b - a}{10}$ (dividing by the number of means), which gives $4b = 6a$."),
   (r"$3 : 8$", "Takes the $4$th mean as the $4$th term, i.e. $3$ steps from the start, giving $3b = 8a$.")],
  r"The $m$th mean in each case is $a + \frac{m(2b - a)}{11}$ and $2a + \frac{m(b - 2a)}{11}$. With $m = 4$: $11a + 8b - 4a = 22a + 4b - 8a$, so $4b = 7a$ and $a : b = 4 : 7$.",
  "Using $n$ instead of $n + 1$ gaps.",
  "U06-C-am-two-insertions", "Two insertions, careful indexing and a ratio.",
  check=_c051, values=[Rational(4, 7), Rational(7, 4), Rational(2, 3), Rational(3, 8)], cognitive="Analysis")

# ---------------------------------------------------------------- 052
def _c052():
    X, Y, Z = symbols('X Y Z', positive=True)
    e = (X + 3*Y)*(Y + 3*Z)*(X*Z + 1)
    bound = 8*sqrt(3*X*Y*3*Y*Z*X*Z)
    bound = simplify(bound.subs(Z, 1/(X*Y)))
    pt = {X: 3, Y: 1, Z: Rational(1, 3)}
    assert pt[X]*pt[Y]*pt[Z] == 1 and e.subs(pt) == bound
    return bound
q("U06-C-052", TOP_AMGM, "Chained AM-GM with a product constraint", "Difficult", "Multi-step computation MCQ",
  r"If $x, y, z$ are positive real numbers with $xyz = 1$, then the least value of $(x + 3y)(y + 3z)(xz + 1)$ is",
  r"$24$",
  [(r"$8$", r"Drops the coefficients $3$ inside the square roots, using $x + 3y \ge 2\sqrt{xy}$ and $y + 3z \ge 2\sqrt{yz}$."),
   (r"$72$", r"Writes $x + 3y \ge 6\sqrt{xy}$ and $y + 3z \ge 6\sqrt{yz}$, putting the $3$ outside the root."),
   (r"$12$", r"Forgets the factor $2$ in $xz + 1 \ge 2\sqrt{xz}$.")],
  r"$x + 3y \ge 2\sqrt{3xy}$, $y + 3z \ge 2\sqrt{3yz}$, $xz + 1 \ge 2\sqrt{xz}$. Multiplying, the product is at least $8\sqrt{9x^2y^2z^2} = 24$. Equality needs $x = 3y$, $y = 3z$, $xz = 1$, which gives $x = 3$, $y = 1$, $z = \frac{1}{3}$ (and $xyz = 1$). So the least value is $24$.",
  "Mishandling coefficients inside AM-GM.",
  "U06-C-amgm-chained-product", "Three AM-GM bounds plus checking a common equality point.",
  check=_c052, values=[24, 8, 72, 12], cognitive="Analysis",
  numerical=dict(question=r"If $x, y, z$ are positive real numbers with $xyz = 1$, then the least value of $(x + 3y)(y + 3z)(xz + 1)$ is", answer=24))

# ---------------------------------------------------------------- 053
def _c053():
    a = Symbol('a', positive=True)
    f = (a + 1/a)**2 + ((1 - a) + 1/(1 - a))**2
    return _pos_min(f, a, 0, 1)
q("U06-C-053", TOP_AMGM, "Sum of squares with reciprocal terms", "Difficult", "Multi-step computation MCQ",
  r"If $a > 0$, $b > 0$ and $a + b = 1$, then the least value of $\left(a + \frac{1}{a}\right)^2 + \left(b + \frac{1}{b}\right)^2$ is",
  r"$\frac{25}{2}$",
  [(r"$8$", r"Uses $a + \frac{1}{a} \ge 2$ for each bracket; equality needs $a = b = 1$, impossible with $a + b = 1$."),
   (r"$25$", r"Uses $p^2 + q^2 \ge (p + q)^2$, omitting the division by $2$."),
   (r"$\frac{25}{4}$", r"Uses $p^2 + q^2 \ge \frac{(p + q)^2}{4}$, dividing by $4$ instead of $2$.")],
  r"Since $p^2 + q^2 \ge \frac{(p+q)^2}{2}$, the expression is at least $\frac{1}{2}\left(1 + \frac{1}{a} + \frac{1}{b}\right)^2$. Also $\frac{1}{a} + \frac{1}{b} = \frac{1}{ab} \ge 4$ because $ab \le \frac{1}{4}$. So it is at least $\frac{25}{2}$, attained at $a = b = \frac{1}{2}$.",
  "Using a bound whose equality case violates the constraint.",
  "U06-C-amgm-sum-squares", "Two inequalities chained, with an unattainable-bound trap.",
  check=_c053, values=[Rational(25, 2), 8, 25, Rational(25, 4)], cognitive="Analysis")

# ---------------------------------------------------------------- 054
def _c054():
    a, b, c = symbols('a b c', positive=True)
    lhs = (1/a - 1)*(1/b - 1)*(1/c - 1)
    rhs = (b + c)*(c + a)*(a + b)/(a*b*c)
    sub = {c: 1 - a - b}
    same = simplify(lhs.subs(sub) - rhs.subs(sub)) == 0
    ident = simplify((a + b)*(b + c)*(c + a) - 8*a*b*c - (a*(b - c)**2 + b*(c - a)**2 + c*(a - b)**2)) == 0
    assert same and ident
    return lhs.subs({a: Rational(1, 3), b: Rational(1, 3), c: Rational(1, 3)})
q("U06-C-054", TOP_AMGM, "Product of reciprocal minus one", "Difficult", "Multi-step computation MCQ",
  r"If $a, b, c$ are positive real numbers with $a + b + c = 1$, then the least value of $\left(\frac{1}{a} - 1\right)\left(\frac{1}{b} - 1\right)\left(\frac{1}{c} - 1\right)$ is",
  r"$8$",
  [(r"$26$", r"Expands the product as $\frac{1}{abc} - 1$ and uses $\frac{1}{abc} \ge 27$."),
   (r"$27$", r"Minimises $\frac{1}{abc}$ instead, forgetting the $-1$ in each factor."),
   (r"$6$", r"Adds the three bounds $\frac{b + c}{a} \ge \frac{2\sqrt{bc}}{a}$ etc. as $2 + 2 + 2$ instead of multiplying.")],
  r"Since $1 - a = b + c$, the product is $\frac{(b + c)(c + a)(a + b)}{abc}$. By AM-GM each factor $b + c \ge 2\sqrt{bc}$, so the numerator is at least $8abc$. The least value is $8$, at $a = b = c = \frac{1}{3}$.",
  "Mis-expanding a product of binomials.",
  "U06-C-amgm-cyclic-product", "Needs the substitution $1 - a = b + c$ before AM-GM.",
  check=_c054, values=[8, 26, 27, 6], cognitive="Analysis",
  numerical=dict(question=r"If $a, b, c$ are positive real numbers with $a + b + c = 1$, then the least value of $\left(\frac{1}{a} - 1\right)\left(\frac{1}{b} - 1\right)\left(\frac{1}{c} - 1\right)$ is", answer=8))

# ---------------------------------------------------------------- 055
def _c055():
    import itertools
    pairs = [(Rational(p), Rational(q)) for p, q in itertools.product([1, 2, 5, Rational(1, 3), 9, 100], repeat=2)]
    def ap(a, b, k):
        return a + (k - 1)*(b - a)/10
    def gp(a, b, k):
        return a*(b/a)**Rational(k - 1, 10)
    s1 = all(N(ap(a, b, 6) - gp(a, b, 6), 30) >= -1e-25 for a, b in pairs)
    s2 = all(N(ap(a, b, 4) - gp(a, b, 4), 30) >= -1e-25 for a, b in pairs)
    return (bool(s1), bool(s2))
q("U06-C-055", TOP_MIX, "Comparing terms of an AP and a GP", "Difficult", "Statement-based MCQ",
  r"An AP and a GP, both with positive terms, have the same first term and the same $11$th term. Statement I: The $6$th term of the AP is greater than or equal to the $6$th term of the GP. Statement II: The $4$th term of the AP is greater than or equal to the $4$th term of the GP. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Believes the AP-GP comparison works only for the middle term, where it is plain AM $\ge$ GM."),
   (ST_FF, r"Reverses AM $\ge$ GM for the middle term and also for the other term."),
   (ST_FT, r"Reverses AM $\ge$ GM for the middle term but accepts the comparison for the $4$th term.")],
  r"Let the common first and $11$th terms be $p$ and $q$. The $6$th terms are $\frac{p + q}{2}$ and $\sqrt{pq}$, so Statement I is AM $\ge$ GM. The $4$th terms are $\frac{7p + 3q}{10}$ and $p^{7/10}q^{3/10}$: this is AM $\ge$ GM for ten numbers, seven equal to $p$ and three equal to $q$. So Statement II is also true.",
  "Thinking AM-GM applies only to two equal weights.",
  "U06-C-ap-gp-term-compare", "Recognising an unequal-weight AM-GM in the second statement.",
  check=_c055, values=[(T, T), (T, F_), (F_, F_), (F_, T)], cognitive="Analysis")

# ---------------------------------------------------------------- 056
def _c056():
    a, rr, dv, ev = 1, 2, 1, 3
    b, c = a*rr, a*rr**2
    root = [s for s in solve(a*x**2 + 2*b*x + c, x)][0]   # repeated root -b/a
    fv = solve(dv*root**2 + 2*ev*root + Symbol('f'), Symbol('f'))[0]
    tests = [Rational(dv, a) + fv/c - 2*Rational(ev, b), Rational(ev, b)**2 - dv*fv/(a*c),
             Rational(dv, a) + Rational(ev, b) + fv/c, Rational(dv, a) - fv/c - 2*Rational(ev, b)]
    # general symbolic confirmation of the keyed relation
    A_, R_, D_, E_ = symbols('A_ R_ D_ E_', nonzero=True)
    rt = -R_
    F_s = -(D_*rt**2 + 2*E_*rt)
    gen = simplify(D_/A_ + F_s/(A_*R_**2) - 2*E_/(A_*R_)) == 0
    assert gen
    return tuple(bool(simplify(e) == 0) for e in tests)
q("U06-C-056", TOP_MIX, "Common root when coefficients are in GP", "Difficult", "Conceptual/application MCQ",
  r"Let $a, b, c$ be non-zero real numbers in GP, and let $d, e, f$ be non-zero real numbers. If the equations $ax^2 + 2bx + c = 0$ and $dx^2 + 2ex + f = 0$ have a common root, then which of the following must hold?",
  r"$\frac{d}{a} + \frac{f}{c} = \frac{2e}{b}$",
  [(r"$\left(\frac{e}{b}\right)^2 = \frac{d}{a} \cdot \frac{f}{c}$", "Assumes the ratios inherit the GP of $a, b, c$; the common-root condition gives an AP instead."),
   (r"$\frac{d}{a} + \frac{e}{b} + \frac{f}{c} = 0$", "Substitutes $x = -r$ but drops the factor $2$ and a sign in the middle term."),
   (r"$\frac{d}{a} - \frac{f}{c} = \frac{2e}{b}$", "Sign slip in the constant term, writing $dr^2 - 2er - f = 0$ before dividing by $ar^2$.")],
  r"With $b = ar$, $c = ar^2$, the first equation is $a(x + r)^2 = 0$, so its only root is $x = -r$. This must satisfy the second: $dr^2 - 2er + f = 0$. Dividing by $ar^2$: $\frac{d}{a} - \frac{2e}{ar} + \frac{f}{ar^2} = 0$, i.e. $\frac{d}{a} + \frac{f}{c} = \frac{2e}{b}$. So $\frac{d}{a}, \frac{e}{b}, \frac{f}{c}$ are in AP.",
  "Not noticing the GP makes the first quadratic a perfect square.",
  "U06-C-gp-common-root", "Combines a GP, a repeated root and substitution into a second quadratic.",
  check=_c056, values=[(T, F_, F_, F_), (F_, T, F_, F_), (F_, F_, T, F_), (F_, F_, F_, T)], cognitive="Analysis")

# ---------------------------------------------------------------- 057
INF_MANY = Integer(-1)   # sentinel value for the option "infinitely many"
def _c057():
    cand = solveset(2**x + 2**(-x) - 2, x, S.Reals)
    good = [s for s in cand if simplify(2*cos(s**2) - 2) == 0]
    return len(good)
q("U06-C-057", TOP_AMGM, "Counting solutions using AM-GM bounds", "Difficult", "Multi-step computation MCQ",
  r"The number of real solutions of the equation $2^{x} + 2^{-x} = 2\cos\left(x^2\right)$ is",
  r"$1$",
  [(r"$0$", r"Concludes from $2^x + 2^{-x} \ge 2 \ge 2\cos(x^2)$ that the two sides can never be equal, missing the equality case."),
   (r"$2$", "Solves $2^x + 2^{-x} = 2$ as a quadratic in $2^x$ and counts its double root $2^x = 1$ twice."),
   (r"infinitely many", "Assumes the periodicity of cosine gives infinitely many solutions without checking the left side.")],
  r"By AM-GM, $2^x + 2^{-x} \ge 2$, with equality only at $x = 0$, while $2\cos(x^2) \le 2$. So equality forces both sides to equal $2$: $x = 0$, and indeed $2\cos 0 = 2$. Exactly one solution.",
  "Treating non-strict inequalities as strict.",
  "U06-C-amgm-equation-count", "Bounding both sides and analysing the equality case.",
  check=_c057, values=[1, 0, 2, INF_MANY], cognitive="Analysis")

# ---------------------------------------------------------------- 058
def _c058():
    rp = Symbol('rp', positive=True)
    a = 3*rp**Rational(-9, 2)      # a^2 r^9 = 9
    Ssum = sum(a*rp**k for k in range(10))
    val = Ssum.subs(rp, 1)
    assert simplify(diff(Ssum, rp).subs(rp, 1)) == 0
    assert all(N(Ssum.subs(rp, v)) >= val for v in [Rational(1, 3), Rational(1, 2), Rational(9, 10), Rational(11, 10), 2, 3])
    return val
q("U06-C-058", TOP_AMGM, "Least sum of a positive GP", "Difficult", "Multi-step computation MCQ",
  r"A GP has $10$ terms, all positive, with common ratio $r > 0$. If the product of its $5$th and $6$th terms is $9$, then the least possible value of the sum of its $10$ terms is",
  r"$30$",
  [(r"$6$", r"Bounds only $a_5 + a_6 \ge 2\sqrt{9}$ and ignores the other terms."),
   (r"$90$", r"Uses $10 \cdot 9$, taking each term to be at least the product $9$ instead of $\sqrt{9}$."),
   (r"$15$", r"Pairs terms equidistant from the ends but bounds each pair by $\sqrt{9} = 3$ instead of $2\sqrt{9} = 6$.")],
  r"Terms equidistant from the ends have product $a_5a_6 = 9$, so the product of all ten terms is $9^5$. By AM-GM, the sum is at least $10\sqrt[10]{9^5} = 10 \cdot 3 = 30$, with equality when all terms are equal to $3$ (that is, $r = 1$).",
  "Not using the equal products of terms equidistant from the ends.",
  "U06-C-gp-sum-min", "Combines a GP property with ten-term AM-GM.",
  check=_c058, values=[30, 6, 90, 15], cognitive="Analysis",
  numerical=dict(question=r"A GP has $10$ terms, all positive, with common ratio $r > 0$. If the product of its $5$th and $6$th terms is $9$, then the least possible value of the sum of its $10$ terms is", answer=30))

# ---------------------------------------------------------------- 059
def _c059():
    roots = [s for s in solve(2*t**3 - 3*t**2 + 1, t) if s != 1]   # b = t^3, A2 = (1 + 2b)/3, G2 = t^2
    bs = {simplify(s**3) for s in roots}
    assert len(bs) == 1
    bv = bs.pop()
    # verify directly
    A2 = 1 + 2*(bv - 1)/3
    rr = [s for s in solve(r**3 - bv, r) if s.is_real][0]
    assert simplify(A2 - rr**2) == 0
    return bv
q("U06-C-059", TOP_INS, "Equal AM and GM positions", "Difficult", "Inverse/parameter MCQ",
  r"Two arithmetic means $A_1, A_2$ and two real geometric means $G_1, G_2$ are inserted between $1$ and a real number $b \ne 1$ (each in order from $1$ towards $b$). If $A_2 = G_2$, then $b$ equals",
  r"$-\frac{1}{8}$",
  [(r"$\frac{1}{8}$", r"Drops the sign of the root $u = -\frac{1}{2}$ of $2u^3 - 3u^2 + 1 = 0$, using $u = \frac{1}{2}$."),
   (r"$-8$", r"Finds $u = -\frac{1}{2}$ but inverts the cube, writing $b = u^{-3}$."),
   (r"$-\frac{1}{2}$", "Reports $u$, the common ratio of the GP, instead of $b = u^3$.")],
  r"Let $u$ be the real common ratio, so $b = u^3$ and $G_2 = u^2$. Also $A_2 = 1 + \frac{2(b - 1)}{3} = \frac{1 + 2u^3}{3}$. Then $1 + 2u^3 = 3u^2$, i.e. $(u - 1)^2(2u + 1) = 0$. Since $b \ne 1$, $u = -\frac{1}{2}$ and $b = -\frac{1}{8}$. Check: $1, \frac{5}{8}, \frac{1}{4}, -\frac{1}{8}$ and $1, -\frac{1}{2}, \frac{1}{4}, -\frac{1}{8}$.",
  "Discarding a negative common ratio for real GMs.",
  "U06-C-am-equals-gm-position", "Cubic in the ratio with a repeated root to reject.",
  check=_c059, values=[Rational(-1, 8), Rational(1, 8), -8, Rational(-1, 2)], cognitive="Analysis")

# ---------------------------------------------------------------- 060
def _c060():
    th = Symbol('th', positive=True)
    f = (sin(th) + 1/sin(th))**2 + (cos(th) + 1/cos(th))**2
    g = 7 + tan(th)**2 + cot(th)**2
    assert simplify(f - g) == 0
    val = simplify(f.subs(th, pi/4))
    grid = min(float(f.subs(th, pi/2*k/400)) for k in range(1, 400))
    assert grid >= float(val) - 1e-9
    return val
q("U06-C-060", TOP_AMGM, "Trigonometric sum of squares", "Difficult", "Multi-step computation MCQ",
  r"For $\theta \in \left(0, \frac{\pi}{2}\right)$, the least value of $(\sin\theta + \operatorname{cosec}\theta)^2 + (\cos\theta + \sec\theta)^2$ is",
  r"$9$",
  [(r"$8$", r"Uses $\sin\theta + \operatorname{cosec}\theta \ge 2$ and $\cos\theta + \sec\theta \ge 2$, which cannot both be equalities."),
   (r"$7$", r"Takes $\operatorname{cosec}^2\theta + \sec^2\theta \ge 2$, treating their product as $1$."),
   (r"$5$", r"Omits the cross terms $2\sin\theta\operatorname{cosec}\theta = 2$ when squaring, getting $1 + 4$.")],
  r"Expanding, the expression is $1 + 4 + \operatorname{cosec}^2\theta + \sec^2\theta = 5 + 2 + \cot^2\theta + \tan^2\theta = 7 + \tan^2\theta + \cot^2\theta$. By AM-GM, $\tan^2\theta + \cot^2\theta \ge 2$, so the least value is $9$, at $\theta = \frac{\pi}{4}$.",
  "Combining AM-GM bounds that are not simultaneously attainable.",
  "U06-C-amgm-trig-squares", "Expansion, identities and AM-GM, with a trap.",
  check=_c060, values=[9, 8, 7, 5], cognitive="Analysis",
  numerical=dict(question=r"For $\theta \in \left(0, \frac{\pi}{2}\right)$, the least value of $(\sin\theta + \operatorname{cosec}\theta)^2 + (\cos\theta + \sec\theta)^2$ is", answer=9))
