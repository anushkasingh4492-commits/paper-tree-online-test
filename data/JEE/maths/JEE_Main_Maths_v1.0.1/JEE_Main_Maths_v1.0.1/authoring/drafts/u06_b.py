import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
r = Symbol('r', real=True)
a_ = Symbol('a', real=True)
k = Symbol('k', integer=True, positive=True)
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TT, FF, TF, FT = (True, True), (False, False), (True, False), (False, True)

TOP = "Geometric progression"


def gp_sum(a, q, m):
    return a*(1 - q**m)/(1 - q)


def inf_sum(a, q):
    return summation(a*q**k, (k, 0, oo))


# =================================================================== EASY

q("U06-B-001", TOP, "nth term of a GP", "Easy", "Single-step computation MCQ",
  r"The $10$th term of the geometric progression $2, 6, 18, 54, \ldots$ is",
  r"$2 \cdot 3^{9}$",
  [(r"$2 \cdot 3^{10}$", r"Uses $T_n = ar^{n}$, so $T_{10} = 2 \cdot 3^{10}$."),
   (r"$2 \cdot 3^{8}$", r"Uses the exponent $n - 2 = 8$, i.e. counts one step too few."),
   (r"$6^{9}$", r"Multiplies $a$ and $r$ first, $(2 \cdot 3)^{9} = 6^{9}$, ignoring the order of operations in $ar^{n-1}$.")],
  r"Here $a = 2$, $r = 3$, so $T_{10} = ar^{9} = 2 \cdot 3^{9}$.",
  r"Using $ar^{n}$ for the $n$th term, or computing $ar^{n-1}$ as $(ar)^{n-1}$.",
  "U06-B-nth-term", r"Direct use of $T_n = ar^{n-1}$ once.",
  check=lambda: 2*Integer(3)**9,
  values=[2*Integer(3)**9, 2*Integer(3)**10, 2*Integer(3)**8, Integer(6)**9], cognitive="Recall")


def _c2():
    sol = solve([Eq(a_*r**4, 48), Eq(a_*r**7, 384)], [a_, r], dict=True)
    return [s[a_] for s in sol if s[r].is_real][0]
q("U06-B-002", TOP, "First term from two given terms", "Easy", "Single-step computation MCQ",
  r"In a geometric progression of real numbers, the $5$th term is $48$ and the $8$th term is $384$. The first term is",
  r"$3$",
  [(r"$6$", r"Finds $r = 2$ but divides $48$ by $r^{3} = 8$, using the wrong power for the $5$th term."),
   (r"$\frac{3}{2}$", r"Writes $T_5 = ar^{5}$, so $a = \frac{48}{32} = \frac{3}{2}$."),
   (r"$\frac{3}{4}$", r"Counts the gap from $T_5$ to $T_8$ as two steps, so $r^{2} = 8$, $r^{4} = 64$ and $a = \frac{48}{64} = \frac{3}{4}$.")],
  r"$\frac{T_8}{T_5} = r^{3} = \frac{384}{48} = 8$, so $r = 2$ (the only real cube root). Then $T_5 = ar^{4} = 16a = 48$ gives $a = 3$.",
  r"Using the wrong exponent of $r$ when linking two given terms.",
  "U06-B-term-from-two-terms", r"Two given terms; one division and one substitution.",
  check=_c2, values=[3, 6, Rational(3, 2), Rational(3, 4)], cognitive="Application")


def _c3():
    m = solve(Eq(3*2**(Symbol('m')-1), 384))[0]
    return simplify(gp_sum(3, 2, m))
q("U06-B-003", TOP, "Finite sum of a GP", "Easy", "Single-step computation MCQ",
  r"The sum $3 + 6 + 12 + \cdots + 384$ equals",
  r"$765$",
  [(r"$768$", r"Writes the sum as $3 \cdot 2^{8}$, dropping the $-1$ in $a(r^{n} - 1)$."),
   (r"$1533$", r"Counts $9$ terms, getting $3(2^{9} - 1)$."),
   (r"$381$", r"Counts $7$ terms, getting $3(2^{7} - 1)$.")],
  r"$384 = 3 \cdot 2^{n-1}$ gives $2^{n-1} = 128$, so $n = 8$. The sum is $\frac{3(2^{8} - 1)}{2 - 1} = 3 \cdot 255 = 765$.",
  r"Miscounting the number of terms or dropping the $-1$ in the sum formula.",
  "U06-B-finite-sum-last-term", r"Find $n$, then one formula.",
  check=_c3, values=[765, 768, 1533, 381], cognitive="Application",
  numerical=dict(question=r"The value of the sum $3 + 6 + 12 + \cdots + 384$ is", answer=765))

q("U06-B-004", TOP, "Sum to infinity, negative ratio", "Easy", "Single-step computation MCQ",
  r"The sum of the infinite geometric series $12 - 6 + 3 - \frac{3}{2} + \cdots$ is",
  r"$8$",
  [(r"$24$", r"Ignores the alternating sign and uses $r = \frac{1}{2}$: $\frac{12}{1/2} = 24$."),
   (r"$18$", r"Multiplies by $1 - r$ instead of dividing: $12 \cdot \frac{3}{2} = 18$."),
   (r"$6$", r"Multiplies by $1 + r$: $12 \cdot \frac{1}{2} = 6$.")],
  r"Here $a = 12$ and $r = -\frac{1}{2}$, with $|r| < 1$. So $S_\infty = \frac{12}{1 - (-1/2)} = \frac{12}{3/2} = 8$.",
  r"Dropping the sign of a negative common ratio.",
  "U06-B-infinite-sum-basic", r"One formula with a sign check.",
  check=lambda: inf_sum(12, Rational(-1, 2)), values=[8, 24, 18, 6], cognitive="Application")

q("U06-B-005", TOP, "Pure recurring decimal as a GP", "Easy", "Single-step computation MCQ",
  r"Writing $0.\overline{36} = \frac{36}{100} + \frac{36}{100^2} + \cdots$ as an infinite GP, its value in lowest terms is",
  r"$\frac{4}{11}$",
  [(r"$\frac{9}{25}$", r"Treats the decimal as the terminating $0.36 = \frac{36}{100}$."),
   (r"$\frac{2}{5}$", r"Uses the denominator $90$: $\frac{36}{90} = \frac{2}{5}$."),
   (r"$\frac{4}{111}$", r"Uses a three-digit period, $\frac{36}{999} = \frac{4}{111}$.")],
  r"With $a = \frac{36}{100}$ and $r = \frac{1}{100}$, the sum is $\frac{36/100}{99/100} = \frac{36}{99} = \frac{4}{11}$.",
  r"Using the wrong denominator for a recurring block.",
  "U06-B-recurring-pure", r"One infinite GP sum.",
  check=lambda: inf_sum(Rational(36, 100), Rational(1, 100)),
  values=[Rational(4, 11), Rational(9, 25), Rational(2, 5), Rational(4, 111)], cognitive="Application")


def _c6():
    A, R = symbols('A R', positive=True)
    P = prod([A*R**j for j in range(5)])
    return simplify(P.subs(A, 2/R**2))
q("U06-B-006", TOP, "Product of terms via the middle term", "Easy", "Single-step computation MCQ",
  r"The third term of a geometric progression with positive terms is $2$. The product of its first five terms is",
  r"$32$",
  [(r"$10$", r"Adds instead of multiplying: $5 \times 2$."),
   (r"$16$", r"Raises the middle term to the power $n - 1 = 4$."),
   (r"$8$", r"Multiplies only the three terms $T_2 T_3 T_4 = T_3^{3}$.")],
  r"The five terms are $\frac{2}{r^2}, \frac{2}{r}, 2, 2r, 2r^2$, whose product is $2^{5} = 32$, independent of $r$.",
  r"Not seeing that the product of an odd number of terms is the middle term raised to the number of terms.",
  "U06-B-product-middle-term", r"Symmetric form of terms; one observation.",
  check=_c6, values=[32, 10, 16, 8], cognitive="Understanding")


def _c7():
    s = solve(Eq((x+3)**2, x*(x+9)), x)
    return [v for v in s if v != 0][0]
q("U06-B-007", TOP, "Condition for three terms in GP", "Easy", "Single-step computation MCQ",
  r"If $x$, $x + 3$, $x + 9$ (with $x \ne 0$) are three consecutive terms of a geometric progression, then $x$ equals",
  r"$3$",
  [(r"$1$", r"Expands $(x+3)^2$ as $x^2 + 9$, so $x^2 + 9 = x^2 + 9x$."),
   (r"$-3$", r"Sign slip in $6x + 9 = 9x$, writing $-3x = 9$."),
   (r"$\frac{3}{2}$", r"Expands $(x+3)^2$ as $x^2 + 3x + 9$, so $3x + 9 = 9x$.")],
  r"The GP condition is $(x+3)^2 = x(x+9)$, i.e. $x^2 + 6x + 9 = x^2 + 9x$, so $3x = 9$ and $x = 3$ (giving $3, 6, 12$).",
  r"Expanding $(x+3)^2$ incorrectly in the condition $b^2 = ac$.",
  "U06-B-three-terms-condition", r"One condition $b^2 = ac$ and a linear equation.",
  check=_c7, values=[3, 1, -3, Rational(3, 2)], cognitive="Application")


def _c8():
    return [s for s in solve(Eq(5/(1 - r), 20), r) if abs(s) < 1][0]
q("U06-B-008", TOP, "Common ratio from sum to infinity", "Easy", "Inverse/parameter MCQ",
  r"An infinite geometric progression has first term $5$ and sum $20$. Its common ratio is",
  r"$\frac{3}{4}$",
  [(r"$\frac{1}{4}$", r"Takes $r = \frac{a}{S_\infty} = \frac{5}{20}$."),
   (r"$-\frac{3}{4}$", r"Uses $S_\infty = \frac{a}{1+r}$, so $1 + r = \frac{1}{4}$."),
   (r"$\frac{4}{5}$", r"Uses $S_\infty = \frac{ar}{1-r}$ (sum from the second term): $20 - 20r = 5r$.")],
  r"$\frac{5}{1 - r} = 20$ gives $1 - r = \frac{1}{4}$, so $r = \frac{3}{4}$, which satisfies $|r| < 1$.",
  r"Misremembering the sum-to-infinity formula.",
  "U06-B-infinite-find-ratio", r"Reverse use of one formula.",
  check=_c8, values=[Rational(3, 4), Rational(1, 4), Rational(-3, 4), Rational(4, 5)], cognitive="Application")

q("U06-B-009", TOP, "Sum of n terms as a formula", "Easy", "Single-step computation MCQ",
  r"The sum of the first $n$ terms of the geometric progression $2, \frac{2}{3}, \frac{2}{9}, \ldots$ is",
  r"$3\left(1 - \frac{1}{3^{n}}\right)$",
  [(r"$3\left(1 - \frac{1}{3^{n-1}}\right)$", r"Uses $r^{n-1}$ in place of $r^{n}$ in the sum formula."),
   (r"$2\left(1 - \frac{1}{3^{n}}\right)$", r"Omits the denominator $1 - r = \frac{2}{3}$."),
   (r"$\frac{3}{2}\left(1 - \frac{1}{3^{n}}\right)$", r"Divides by $1 + r = \frac{4}{3}$ instead of $1 - r$.")],
  r"With $a = 2$, $r = \frac{1}{3}$: $S_n = \frac{2\left(1 - (1/3)^{n}\right)}{1 - 1/3} = 3\left(1 - \frac{1}{3^{n}}\right)$.",
  r"Using $r^{n-1}$ instead of $r^{n}$ in $S_n$.",
  "U06-B-sum-formula-n", r"Direct substitution in $S_n$.",
  check=lambda: simplify(summation(2*Rational(1, 3)**(k-1), (k, 1, n))),
  values=[3*(1 - 3**(-n)), 3*(1 - 3**(1-n)), 2*(1 - 3**(-n)), Rational(3, 2)*(1 - 3**(-n))], cognitive="Application")


def _c10():
    m = solve(Eq(7*2**(Symbol('m')-1), 448))[0]
    return simplify(gp_sum(7, 2, m))
q("U06-B-010", TOP, "Sum using first and last terms", "Easy", "Single-step computation MCQ",
  r"A finite geometric progression has first term $7$, last term $448$ and common ratio $2$. The sum of all its terms is",
  r"$889$",
  [(r"$896$", r"Uses $\frac{lr}{r - 1}$, dropping the $-a$ in $\frac{lr - a}{r - 1}$."),
   (r"$1785$", r"Counts $8$ terms: $7(2^{8} - 1)$."),
   (r"$441$", r"Uses $\frac{l - a}{r - 1}$, omitting the factor $r$ on $l$.")],
  r"$S = \frac{lr - a}{r - 1} = \frac{896 - 7}{1} = 889$. (Equivalently $448 = 7 \cdot 2^{6}$ gives $7$ terms and $7(2^{7} - 1) = 889$.)",
  r"Misusing $S = \frac{lr - a}{r - 1}$.",
  "U06-B-finite-sum-last-term", r"One formula in terms of first and last terms.",
  check=_c10, values=[889, 896, 1785, 441], cognitive="Application")

q("U06-B-011", TOP, "Sum of an infinite series of powers", "Easy", "Single-step computation MCQ",
  r"The value of $\displaystyle\sum_{n=1}^{\infty} \left(\frac{2}{5}\right)^{n}$ is",
  r"$\frac{2}{3}$",
  [(r"$\frac{5}{3}$", r"Starts the sum at $n = 0$, using first term $1$."),
   (r"$\frac{3}{2}$", r"Inverts the result, computing $\frac{1 - r}{r}$."),
   (r"$\frac{2}{7}$", r"Divides by $1 + r = \frac{7}{5}$.")],
  r"The first term is $\frac{2}{5}$ and $r = \frac{2}{5}$, so the sum is $\frac{2/5}{1 - 2/5} = \frac{2/5}{3/5} = \frac{2}{3}$.",
  r"Taking the first term as $1$ when the sum starts at $n = 1$.",
  "U06-B-infinite-sum-basic", r"One formula; first term must be read off correctly.",
  check=lambda: summation(Rational(2, 5)**k, (k, 1, oo)),
  values=[Rational(2, 3), Rational(5, 3), Rational(3, 2), Rational(2, 7)], cognitive="Application")

q("U06-B-012", TOP, "Mixed recurring decimal", "Easy", "Single-step computation MCQ",
  r"Expressing the recurring part as an infinite GP, the value of $0.1\overline{6}$ is",
  r"$\frac{1}{6}$",
  [(r"$\frac{16}{99}$", r"Treats both digits as recurring, i.e. computes $0.\overline{16}$."),
   (r"$\frac{8}{45}$", r"Uses denominator $90$ but numerator $16$ in place of $16 - 1 = 15$."),
   (r"$\frac{4}{25}$", r"Treats it as the terminating decimal $0.16$.")],
  r"$0.1\overline{6} = \frac{1}{10} + \left(\frac{6}{100} + \frac{6}{1000} + \cdots\right) = \frac{1}{10} + \frac{6/100}{1 - 1/10} = \frac{1}{10} + \frac{1}{15} = \frac{1}{6}$.",
  r"Not separating the non-recurring digit before summing the GP.",
  "U06-B-recurring-mixed", r"Split into a terminating part and one GP.",
  check=lambda: Rational(1, 10) + inf_sum(Rational(6, 100), Rational(1, 10)),
  values=[Rational(1, 6), Rational(16, 99), Rational(8, 45), Rational(4, 25)], cognitive="Application")


def _c13():
    kk = Symbol('kk')
    s = solve(Eq((2*kk+2)**2, kk*(3*kk+3)), kk)
    return [v for v in s if v not in (-1, 0)][0]
q("U06-B-013", TOP, "Parameter for three terms in GP", "Easy", "Inverse/parameter MCQ",
  r"If $k$, $2k + 2$, $3k + 3$ are three consecutive terms of a geometric progression, where $k \ne 0$ and $k \ne -1$, then $k$ equals",
  r"$-4$",
  [(r"$4$", r"Sign slip in $4(k + 1) = 3k$, writing $4k - 3k = 4$."),
   (r"$2$", r"Writes $(2k + 2)^2$ as $2(k + 1)^2$, then cancels to get $2k + 2 = 3k$."),
   (r"$-\frac{1}{4}$", r"Cancels $(k + 1)$ and also drops $k$, writing $4(k + 1) = 3$.")],
  r"$(2k + 2)^2 = k(3k + 3)$ gives $4(k + 1)^2 = 3k(k + 1)$. As $k \ne -1$, divide by $k + 1$: $4k + 4 = 3k$, so $k = -4$. The terms are $-4, -6, -9$ with $r = \frac{3}{2}$.",
  r"Mishandling the factor $(k + 1)$ when applying $b^2 = ac$.",
  "U06-B-three-terms-condition", r"Condition $b^2 = ac$ with a common factor to cancel.",
  check=_c13, values=[-4, 4, 2, Rational(-1, 4)], cognitive="Application")


def _c14():
    m = Symbol('m')
    return solve(Eq(sqrt(3)*sqrt(3)**(m-1), 729), m)[0]
q("U06-B-014", TOP, "Which term of a GP", "Easy", "Single-step computation MCQ",
  r"Which term of the geometric progression $\sqrt{3}, 3, 3\sqrt{3}, \ldots$ is $729$?",
  r"$12$th",
  [(r"$6$th", r"Equates $T_n$ with $3^{n}$, reading $729 = 3^{6}$ as the term number."),
   (r"$11$th", r"Uses $T_n = ar^{n}$: $(\sqrt{3})^{n+1} = (\sqrt{3})^{12}$."),
   (r"$13$th", r"Uses $r^{n-1}$ but forgets the first term $\sqrt{3}$: $(\sqrt{3})^{n-1} = (\sqrt{3})^{12}$.")],
  r"$T_n = \sqrt{3}(\sqrt{3})^{n-1} = (\sqrt{3})^{n}$, and $729 = 3^{6} = (\sqrt{3})^{12}$, so $n = 12$.",
  r"Working with powers of $3$ instead of powers of $\sqrt{3}$.",
  "U06-B-which-term", r"One exponent equation with a surd ratio.",
  check=_c14, values=[12, 6, 11, 13], cognitive="Application")

q("U06-B-015", TOP, "Finite sum with negative ratio", "Easy", "Single-step computation MCQ",
  r"The sum of the first six terms of the geometric progression $1, -2, 4, -8, \ldots$ is",
  r"$-21$",
  [(r"$63$", r"Ignores the sign of $r$ and uses $r = 2$."),
   (r"$21$", r"Uses $\frac{r^{n} - 1}{r - 1}$ with $r = -2$ but takes the denominator as $3$: $\frac{63}{3}$."),
   (r"$43$", r"Uses seven terms: $\frac{1 - (-2)^{7}}{3} = \frac{129}{3}$.")],
  r"$S_6 = \frac{1 - (-2)^{6}}{1 - (-2)} = \frac{1 - 64}{3} = -21$.",
  r"Mishandling a negative common ratio in the sum formula.",
  "U06-B-finite-sum-negative-ratio", r"One formula with sign care.",
  check=lambda: gp_sum(1, -2, 6), values=[-21, 63, 21, 43], cognitive="Application")


def _c16():
    sol = solve([Eq(a_*r**2, 12), Eq(a_*r**6, 192)], [a_, r], dict=True)
    return FiniteSet(*[s[a_]*s[r]**5 for s in sol if s[r].is_real])
q("U06-B-016", TOP, "Two possible ratios", "Easy", "Multi-step computation MCQ",
  r"In a geometric progression of real numbers, the $3$rd term is $12$ and the $7$th term is $192$. The set of all possible values of the $6$th term is",
  r"$\{-96, 96\}$",
  [(r"$\{96\}$", r"Takes only $r = 2$ from $r^{4} = 16$, missing $r = -2$."),
   (r"$\{48\}$", r"Counts the gap from $T_3$ to $T_6$ as two steps: $12 r^{2} = 48$."),
   (r"$\{-24, 24\}$", r"Finds $r = \pm 2$ but divides $T_7$ by $r^{3}$ instead of $r$.")],
  r"$r^{4} = \frac{192}{12} = 16$, so $r = 2$ or $r = -2$, and in both cases $a = \frac{12}{r^2} = 3$. Then $T_6 = 3r^{5} = 96$ or $-96$.",
  r"Taking only the positive fourth root of $16$.",
  "U06-B-term-from-two-terms", r"Even power of $r$ gives two real ratios; short casework.",
  check=_c16, values=[FiniteSet(-96, 96), FiniteSet(96), FiniteSet(48), FiniteSet(-24, 24)], cognitive="Analysis")

q("U06-B-017", TOP, "Recurring decimal with an integer part", "Easy", "Single-step computation MCQ",
  r"Using an infinite GP for the recurring part, $2.\overline{4}$ equals",
  r"$\frac{22}{9}$",
  [(r"$\frac{12}{5}$", r"Treats it as the terminating decimal $2.4$."),
   (r"$\frac{8}{3}$", r"Puts all digits over $9$: $\frac{24}{9}$."),
   (r"$\frac{202}{99}$", r"Uses denominator $99$ for a one-digit period: $2 + \frac{4}{99}$.")],
  r"$2.\overline{4} = 2 + \left(\frac{4}{10} + \frac{4}{100} + \cdots\right) = 2 + \frac{4/10}{9/10} = 2 + \frac{4}{9} = \frac{22}{9}$.",
  r"Mixing up the period length with the denominator.",
  "U06-B-recurring-pure", r"One GP plus an integer.",
  check=lambda: 2 + inf_sum(Rational(4, 10), Rational(1, 10)),
  values=[Rational(22, 9), Rational(12, 5), Rational(8, 3), Rational(202, 99)], cognitive="Application")


def _c18():
    A, R = symbols('A R', nonzero=True)
    p, q_, s = A, A*R, A*R**2
    s1 = simplify((q_ + 1)**2 - (p + 1)*(s + 1)) == 0
    s2 = simplify((q_ + s)**2 - (p + q_)*(s + p)) == 0
    return (bool(s1), bool(s2))
q("U06-B-018", TOP, "Which operations preserve a GP", "Easy", "Statement-based MCQ",
  r"Let $a, b, c$ be non-zero real numbers in geometric progression with common ratio $\rho \ne 1$." "\n"
  r"Statement I: $a + 1$, $b + 1$, $c + 1$ are always in geometric progression." "\n"
  r"Statement II: $a + b$, $b + c$, $c + a$ are always in geometric progression." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Assumes adding a constant or adding pairs keeps the ratio, as for $a + b$, $b + c$, $c + d$ with four terms."),
   (ST_TF, r"Believes adding the same constant preserves a GP (true only for an AP)."),
   (ST_FT, r"Rejects Statement I correctly but carries over the four-term fact $a + b, b + c, c + d$ to the three sums $a + b, b + c, c + a$.")],
  r"Take $a, a\rho, a\rho^2$. For Statement I, $(a\rho + 1)^2 - (a + 1)(a\rho^2 + 1) = -a(\rho - 1)^2 \ne 0$; e.g. $1, 2, 4$ gives $2, 3, 5$. For Statement II, $1, 2, 4$ gives $3, 6, 5$, which is not a GP since $36 \ne 15$. Both statements are false.",
  r"Transferring AP properties (adding a constant) to a GP.",
  "U06-B-gp-closure-statements", r"Two short checks with a counterexample.",
  check=_c18, values=[FF, TT, TF, FT], cognitive="Understanding")

# =================================================================== MEDIUM

q("U06-B-019", TOP, "Each term related to the tail", "Medium", "Inverse/parameter MCQ",
  r"In an infinite geometric progression of non-zero terms with a finite sum, every term is equal to $3$ times the sum of all the terms that follow it. The common ratio is",
  r"$\frac{1}{4}$",
  [(r"$\frac{1}{3}$", r"Equates each term to $3$ times only the next term: $T = 3Tr$."),
   (r"$\frac{3}{4}$", r"Reverses the relation, setting the tail equal to $3$ times the term: $\frac{r}{1-r} = 3$."),
   (r"$\frac{1}{2}$", r"Correct equation $1 - r = 3r$ but transposes as $1 = 2r$.")],
  r"The terms after $T$ sum to $\frac{Tr}{1 - r}$. So $T = \frac{3Tr}{1 - r}$, i.e. $1 - r = 3r$, giving $r = \frac{1}{4}$.",
  r"Comparing a term with the next term instead of with the whole tail.",
  "U06-B-term-vs-tail", r"Set up the tail sum, then solve; reading the relation the right way round is the trap.",
  check=lambda: solve(Eq(1, 3*r/(1 - r)), r)[0],
  values=[Rational(1, 4), Rational(1, 3), Rational(3, 4), Rational(1, 2)], cognitive="Application")


def _c20():
    sol = solve([Eq(a_/(1 - r), 4), Eq(a_**2/(1 - r**2), Rational(16, 3))], [a_, r], dict=True)
    return [s[r] for s in sol if abs(s[r]) < 1][0]
q("U06-B-020", TOP, "Sum and sum of squares", "Medium", "Multi-step computation MCQ",
  r"An infinite geometric progression has sum $4$, and the sum of the squares of its terms is $\frac{16}{3}$. Its common ratio is",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{3}$", r"Finds $\frac{1 - r}{1 + r} = \frac{1}{3}$ and takes that ratio itself as $r$."),
   (r"$-\frac{1}{2}$", r"Inverts the ratio, solving $\frac{1 + r}{1 - r} = \frac{1}{3}$."),
   (r"$-\frac{1}{7}$", r"Divides the sum of squares by $4$ instead of $4^{2}$: $\frac{1 - r}{1 + r} = \frac{4}{3}$.")],
  r"$\frac{a^2/(1 - r^2)}{\left(a/(1 - r)\right)^2} = \frac{1 - r}{1 + r} = \frac{16/3}{16} = \frac{1}{3}$, so $3 - 3r = 1 + r$ and $r = \frac{1}{2}$ (then $a = 2$).",
  r"Dividing by the sum rather than its square when eliminating $a$.",
  "U06-B-sum-and-squares", r"Two infinite sums; eliminate $a$ by a ratio.",
  check=_c20, values=[Rational(1, 2), Rational(1, 3), Rational(-1, 2), Rational(-1, 7)], cognitive="Application")


def _c21():
    S = lambda m: 5*(2**m - 1)
    T = lambda m: S(m) - (S(m - 1) if m > 1 else 0)
    return sum(T(m)**2 for m in range(1, 6))
q("U06-B-021", TOP, "nth term from S_n", "Medium", "Multi-step computation MCQ",
  r"The sum of the first $n$ terms of a geometric progression is $S_n = 5(2^{n} - 1)$. The sum of the squares of its first $5$ terms is",
  r"$8525$",
  [(r"$34125$", r"Sums six squares instead of five: $\frac{25(4^{6} - 1)}{3} = 34125$."),
   (r"$1705$", r"Takes the squared progression as $5, 20, 80, \ldots$, squaring the ratio but not the first term: $\frac{5(4^{5} - 1)}{3} = 1705$."),
   (r"$24025$", r"Squares the sum instead of summing the squares: $S_5^{2} = 155^{2} = 24025$.")],
  r"$T_1 = S_1 = 5$ and $T_n = S_n - S_{n-1} = 5 \cdot 2^{n-1}$, so the progression is $5, 10, 20, \ldots$ with ratio $2$. Their squares $25, 100, 400, \ldots$ form a GP with first term $25$ and ratio $4$, so the required sum is $\frac{25(4^{5} - 1)}{4 - 1} = 25 \cdot 341 = 8525$.",
  r"Confusing the sum of squares with the square of the sum, or squaring only the ratio.",
  "U06-B-term-from-Sn", r"Recover $T_n$ from $S_n$, recognise that the squares form a GP with ratio $r^{2}$ and first term $a^{2}$, then sum; three linked steps.",
  check=_c21, values=[8525, 34125, 1705, 24025], cognitive="Application",
  numerical=dict(question=r"The sum of the first $n$ terms of a geometric progression is $S_n = 5(2^{n} - 1)$. The sum of the squares of its first $5$ terms is", answer=8525))


def _c22():
    kk = Symbol('kk')
    S = lambda m: 2**(m + 1) + kk
    T1, T2, T3 = S(1), S(2) - S(1), S(3) - S(2)
    return solve(Eq(T2**2, T1*T3), kk)[0]
q("U06-B-022", TOP, "Constant in S_n for a GP", "Medium", "Inverse/parameter MCQ",
  r"The sum of the first $n$ terms of a sequence is $S_n = 2^{n+1} + k$ for all $n \ge 1$, where $k$ is a constant. The sequence is a geometric progression if and only if $k$ equals",
  r"$-2$",
  [(r"$0$", r"Treats $S_1, S_2, S_3$ as the first three terms: $(8 + k)^2 = (4 + k)(16 + k)$ gives $k = 0$."),
   (r"$4$", r"Finds $T_2 = 4$ and $T_3 = 8$ with ratio $2$, but goes back to the first term by multiplying instead of dividing: $T_1 = 2T_2 = 8$, so $4 + k = 8$ and $k = 4$."),
   (r"$2$", r"Compares with $\frac{a}{r-1}r^{n} - \frac{a}{r-1}$ but loses the minus sign on the constant.")],
  r"$T_1 = S_1 = 4 + k$, $T_2 = S_2 - S_1 = 4$, $T_3 = S_3 - S_2 = 8$, and for $n \ge 2$, $T_n = 2^{n}$ with ratio $2$. A GP needs $T_2^2 = T_1 T_3$: $16 = 8(4 + k)$, so $k = -2$.",
  r"Forgetting that $T_1 = S_1$ carries the constant term.",
  "U06-B-term-from-Sn", r"Generate terms from $S_n$ and impose the GP condition; the first term is the trap.",
  check=_c22, values=[-2, 0, 4, 2], cognitive="Analysis")


def _c23():
    A, R = symbols('A R', positive=True)
    T = lambda m: A*R**(m - 1)
    t8 = solve(Eq(T(3)*T(8)*T(13), 1000).subs(A, Symbol('t')/R**7), Symbol('t'))
    t8 = [v for v in t8 if v.is_positive][0]
    P = prod([T(j) for j in range(1, 16)])
    return simplify(P.subs(A, t8/R**7))
q("U06-B-023", TOP, "Product of terms from a symmetric condition", "Medium", "Multi-step computation MCQ",
  r"In a geometric progression of positive terms, $T_3 \cdot T_8 \cdot T_{13} = 1000$. The product of the first $15$ terms is",
  r"$10^{15}$",
  [(r"$10^{14}$", r"Pairs $T_1T_{15}, \ldots, T_7T_9$ as $7$ pairs of $T_8^2$ but leaves out the middle term."),
   (r"$10^{30}$", r"Counts $15$ pairs, each with product $T_8^2 = 100$."),
   (r"$10^{45}$", r"Raises the given product $1000$ to the power $15$.")],
  r"$T_3T_{13} = T_8^2$, so $T_8^3 = 1000$ and $T_8 = 10$. The first $15$ terms are symmetric about $T_8$, so their product is $T_8^{15} = 10^{15}$.",
  r"Miscounting the pairs when using $T_kT_{16-k} = T_8^2$.",
  "U06-B-product-middle-term", r"Symmetry gives the middle term; then the product of an odd number of terms.",
  check=_c23, values=[Integer(10)**15, Integer(10)**14, Integer(10)**30, Integer(10)**45], cognitive="Application")

q("U06-B-024", TOP, "Sum of recurring decimals", "Medium", "Multi-step computation MCQ",
  r"Writing each recurring decimal as an infinite GP, the value of $0.\overline{12} + 0.\overline{3}$ is",
  r"$\frac{5}{11}$",
  [(r"$\frac{5}{33}$", r"Takes $0.\overline{3}$ as $\frac{3}{99}$, using a two-digit denominator for a one-digit period."),
   (r"$\frac{9}{20}$", r"Adds the terminating decimals $0.12 + 0.33$."),
   (r"$\frac{7}{15}$", r"Takes $0.\overline{12}$ as $\frac{12}{90}$.")],
  r"$0.\overline{12} = \frac{12/100}{1 - 1/100} = \frac{12}{99}$ and $0.\overline{3} = \frac{3/10}{1 - 1/10} = \frac{1}{3} = \frac{33}{99}$. The sum is $\frac{45}{99} = \frac{5}{11}$.",
  r"Using the wrong power of $10$ for the period.",
  "U06-B-recurring-sum", r"Two GPs with different ratios, then addition.",
  check=lambda: inf_sum(Rational(12, 100), Rational(1, 100)) + inf_sum(Rational(3, 10), Rational(1, 10)),
  values=[Rational(5, 11), Rational(5, 33), Rational(9, 20), Rational(7, 15)], cognitive="Application")


def _c25():
    m = 1
    while not 5*(2**m - 1) > 1000:
        m += 1
    return m
q("U06-B-025", TOP, "Least n for a sum to exceed a value", "Medium", "Inverse/parameter MCQ",
  r"The least positive integer $n$ for which $5 + 10 + 20 + \cdots$ ($n$ terms) exceeds $1000$ is",
  r"$8$",
  [(r"$9$", r"Finds the least $n$ for which the $n$th term $5 \cdot 2^{n-1}$ exceeds $1000$."),
   (r"$7$", r"Gives the largest $n$ for which the sum is still at most $1000$ ($S_7 = 635$)."),
   (r"$10$", r"Solves $5(2^{n} - 1) > 1000$ as $2^{n} > 1000$, dropping the factor $5$.")],
  r"$S_n = 5(2^{n} - 1) > 1000$ means $2^{n} > 201$. Since $2^{7} = 128$ and $2^{8} = 256$, the least $n$ is $8$ ($S_8 = 1275$).",
  r"Confusing the $n$th term with the sum of $n$ terms.",
  "U06-B-least-n-sum", r"Sum formula followed by a power inequality.",
  check=_c25, values=[8, 9, 7, 10], cognitive="Application",
  numerical=dict(question=r"The least positive integer $n$ for which the sum of the first $n$ terms of $5 + 10 + 20 + \cdots$ exceeds $1000$ is", answer=8))

q("U06-B-026", TOP, "Splitting into two infinite GPs", "Medium", "Multi-step computation MCQ",
  r"The value of $\displaystyle\sum_{n=1}^{\infty} \frac{2^{n} + (-1)^{n}}{3^{n}}$ is",
  r"$\frac{7}{4}$",
  [(r"$\frac{9}{4}$", r"Adds $\frac{1}{4}$ for the second series, dropping the sign of $-\frac{1}{3}$ in the first term."),
   (r"$\frac{5}{2}$", r"Treats $(-1)^{n}$ as $1$, adding $\frac{1/3}{2/3} = \frac{1}{2}$."),
   (r"$\frac{15}{4}$", r"Starts both series at $n = 0$: $3 + \frac{3}{4}$.")],
  r"$\sum_{n \ge 1} \left(\frac{2}{3}\right)^{n} = \frac{2/3}{1/3} = 2$ and $\sum_{n \ge 1} \left(-\frac{1}{3}\right)^{n} = \frac{-1/3}{4/3} = -\frac{1}{4}$. Total $2 - \frac{1}{4} = \frac{7}{4}$.",
  r"Mishandling the sign of a negative ratio in the first term.",
  "U06-B-split-infinite-sums", r"Split into two GPs, one with negative ratio.",
  check=lambda: summation((2**k + (-1)**k)/3**k, (k, 1, oo)),
  values=[Rational(7, 4), Rational(9, 4), Rational(5, 2), Rational(15, 4)], cognitive="Application")

q("U06-B-027", TOP, "Sum of 5 + 55 + 555 + ...", "Medium", "Multi-step computation MCQ",
  r"The sum of the first $n$ terms of $5 + 55 + 555 + \cdots$ is",
  r"$\frac{5}{81}\left(10^{n+1} - 9n - 10\right)$",
  [(r"$\frac{50}{81}\left(10^{n} - 1\right)$", r"Writes the $k$th term as $\frac{5}{9}(10^{k} - 1)$ but sums only the $10^{k}$ parts, dropping $-n$."),
   (r"$\frac{5}{81}\left(10^{n} - 9n - 1\right)$", r"Sums $1 + 10 + \cdots + 10^{n-1}$ instead of $10 + 10^2 + \cdots + 10^{n}$."),
   (r"$\frac{5}{81}\left(10^{n+1} + 9n - 10\right)$", r"Adds $n$ instead of subtracting it.")],
  r"The $k$th term is $\frac{5}{9}(10^{k} - 1)$. So the sum is $\frac{5}{9}\left(\frac{10(10^{n} - 1)}{9} - n\right) = \frac{5}{81}\left(10^{n+1} - 10 - 9n\right)$.",
  r"Mis-summing the GP part $10 + 10^2 + \cdots + 10^{n}$.",
  "U06-B-repdigit-sum", r"Rewrite each term, then a GP sum and a constant sum.",
  check=lambda: simplify(Rational(5, 9)*summation(10**k - 1, (k, 1, n))),
  values=[Rational(5, 81)*(10**(n+1) - 9*n - 10), Rational(50, 81)*(10**n - 1),
          Rational(5, 81)*(10**n - 9*n - 1), Rational(5, 81)*(10**(n+1) + 9*n - 10)], cognitive="Application")


def _c28():
    rs = [v for v in solve(Eq(gp_sum(2, r, 3), 14), r) if v.is_real]
    return sum(2*v**3 for v in rs)
q("U06-B-028", TOP, "Two ratios from a finite sum", "Medium", "Multi-step computation MCQ",
  r"A geometric progression of real numbers has first term $2$, and the sum of its first three terms is $14$. The sum of all possible values of its fourth term is",
  r"$-38$",
  [(r"$16$", r"Uses only $r = 2$."),
   (r"$-54$", r"Uses only $r = -3$."),
   (r"$70$", r"Sign slip in the second root, using $r = 3$ in place of $r = -3$: $16 + 54$.")],
  r"$2(1 + r + r^2) = 14$ gives $r^2 + r - 6 = 0$, so $r = 2$ or $r = -3$. Then $T_4 = 2r^3 = 16$ or $-54$, and the sum is $-38$.",
  r"Keeping only one root of the quadratic in $r$.",
  "U06-B-two-ratio-cases", r"Quadratic in $r$, two cases, combine.",
  check=_c28, values=[-38, 16, -54, 70], cognitive="Application")


def _c29():
    A, R = symbols('A R', positive=True)
    sol = solve([Eq(A/R + A + A*R, 13), Eq(A**3, 27)], [A, R], dict=True)
    s = sol[0]
    return simplify((s[A]/s[R])**2 + s[A]**2 + (s[A]*s[R])**2)
q("U06-B-029", TOP, "Three numbers in GP from sum and product", "Medium", "Multi-step computation MCQ",
  r"Three positive numbers in geometric progression have sum $13$ and product $27$. The sum of their squares is",
  r"$91$",
  [(r"$115$", r"Uses $13^2 - 2 \cdot 27$, subtracting twice the product instead of twice the sum of pairwise products."),
   (r"$130$", r"Uses $13^2 - 39$, forgetting the factor $2$ on the pairwise products."),
   (r"$169$", r"Squares the sum: $13^2$.")],
  r"Take the numbers as $\frac{3}{r}, 3, 3r$ (product $27$). Then $\frac{3}{r} + 3 + 3r = 13$ gives $3r^2 - 10r + 3 = 0$, so $r = 3$ or $\frac{1}{3}$: the numbers are $1, 3, 9$. Sum of squares $= 1 + 9 + 81 = 91$.",
  r"Using the product in place of the sum of pairwise products.",
  "U06-B-three-terms-sum-product", r"Symmetric choice of terms, a quadratic, then evaluation.",
  check=_c29, values=[91, 115, 130, 169], cognitive="Application",
  numerical=dict(question=r"Three positive numbers in geometric progression have sum $13$ and product $27$. The sum of their squares is", answer=91))


def _c30():
    rs = [v for v in solve(Eq(gp_sum(1, r, 6), 9*gp_sum(1, r, 3)), r) if v.is_real]
    return rs[0]
q("U06-B-030", TOP, "Ratio of sums", "Medium", "Inverse/parameter MCQ",
  r"For a geometric progression with real common ratio $r \ne 1$, the sum of the first $6$ terms is $9$ times the sum of the first $3$ terms. Then $r$ equals",
  r"$2$",
  [(r"$3$", r"Takes $\frac{S_6}{S_3} = r^{2}$."),
   (r"$2\sqrt{2}$", r"Writes $\frac{S_6}{S_3} = 1 + r^{2}$."),
   (r"$8$", r"Writes $\frac{S_6}{S_3} = 1 + r$, i.e. forgets the cube.")],
  r"$\frac{S_6}{S_3} = \frac{r^{6} - 1}{r^{3} - 1} = r^{3} + 1 = 9$, so $r^{3} = 8$ and $r = 2$.",
  r"Simplifying $\frac{r^6 - 1}{r^3 - 1}$ wrongly.",
  "U06-B-ratio-of-sums", r"Factor a difference of squares in powers of $r$.",
  check=_c30, values=[2, 3, 2*sqrt(2), 8], cognitive="Application")


def _c31():
    sol = solve([Eq(a_/(1 - r**2), 36), Eq(a_*r/(1 - r**2), 12)], [a_, r], dict=True)
    return [s[a_] for s in sol if abs(s[r]) < 1][0]
q("U06-B-031", TOP, "Odd-placed and even-placed terms", "Medium", "Multi-step computation MCQ",
  r"In an infinite geometric progression with a finite sum, the sum of the terms in the odd places ($T_1 + T_3 + T_5 + \cdots$) is $36$ and the sum of the terms in the even places is $12$. The first term is",
  r"$32$",
  [(r"$24$", r"Gets $r = \frac{1}{3}$ but uses $\frac{a}{1 - r} = 36$ for the odd-placed sum."),
   (r"$\frac{128}{3}$", r"Uses the total $48$ as $\frac{a}{1 - r^2}$."),
   (r"$\frac{32}{3}$", r"Uses the even-placed sum as $\frac{a}{1 - r^2} = 12$, missing the factor $r$.")],
  r"Odd-placed terms form a GP with first term $a$ and ratio $r^2$; even-placed ones have first term $ar$. So $\frac{a}{1 - r^2} = 36$, $\frac{ar}{1 - r^2} = 12$, giving $r = \frac{1}{3}$ and $a = 36 \cdot \frac{8}{9} = 32$.",
  r"Using ratio $r$ instead of $r^2$ for alternate terms.",
  "U06-B-alternate-terms", r"Recognise two sub-GPs with ratio $r^2$; solve two equations.",
  check=_c31, values=[32, 24, Rational(128, 3), Rational(32, 3)], cognitive="Application",
  numerical=dict(question=r"In an infinite geometric progression with a finite sum, the sum of the terms in the odd places is $36$ and the sum of the terms in the even places is $12$. The first term of the progression is", answer=32))


def _c32():
    P = prod([Rational(1, 8)*2**j for j in range(10)])
    return P
q("U06-B-032", TOP, "Product of the first n terms", "Medium", "Single-step computation MCQ",
  r"The product of the first $10$ terms of the geometric progression $\frac{1}{8}, \frac{1}{4}, \frac{1}{2}, 1, \ldots$ is",
  r"$2^{15}$",
  [(r"$2^{25}$", r"Uses the exponent sum $1 + 2 + \cdots + 10 = 55$ for $r$ instead of $0 + 1 + \cdots + 9 = 45$."),
   (r"$2^{60}$", r"Takes the exponent of $r$ as $n(n - 1) = 90$ instead of $\frac{n(n-1)}{2}$."),
   (r"$2^{75}$", r"Takes $a^{10} = 2^{30}$, losing the negative sign in $a = 2^{-3}$.")],
  r"Product $= a^{10} r^{0 + 1 + \cdots + 9} = (2^{-3})^{10} \cdot 2^{45} = 2^{-30 + 45} = 2^{15}$.",
  r"Using the wrong exponent sum for $r$.",
  "U06-B-product-formula", r"Formula $a^{n} r^{n(n-1)/2}$ with a negative exponent.",
  check=_c32, values=[Integer(2)**15, Integer(2)**25, Integer(2)**60, Integer(2)**75], cognitive="Application")


def _c33():
    X, Z, K, L, M = symbols('X Z K L M', nonzero=True)
    # ln a = L, ln b = L + M, ln c = L + 2M ; common value e^K
    sol = solve([Eq(X, L/K), Eq(Z, (L + 2*M)/K)], [L, M], dict=True)[0]
    Y = ((L + M)/K).subs(sol)
    return simplify(Y)
_X, _Z = symbols('X Z', nonzero=True)
q("U06-B-033", TOP, "Exponents linked to a GP", "Medium", "Conceptual/application MCQ",
  r"Let $a, b, c$ be positive real numbers, none equal to $1$, in geometric progression. If $a^{1/x} = b^{1/y} = c^{1/z} \ne 1$ for non-zero reals $x, y, z$, then",
  r"$2y = x + z$",
  [(r"$y^2 = xz$", r"Assumes the exponents inherit the GP property from $a, b, c$."),
   (r"$\frac{2}{y} = \frac{1}{x} + \frac{1}{z}$", r"Writes $\frac{1}{x} = \log_e a$ (inverting the relation) and then imposes an AP on $\log_e a, \log_e b, \log_e c$."),
   (r"$y = x + z$", r"Uses $\log_e b = \log_e a + \log_e c$ in place of $2\log_e b = \log_e a + \log_e c$.")],
  r"Let the common value be $t$. Then $x = \frac{\log_e a}{\log_e t}$, $y = \frac{\log_e b}{\log_e t}$, $z = \frac{\log_e c}{\log_e t}$. Since $b^2 = ac$, $2\log_e b = \log_e a + \log_e c$, so $2y = x + z$.",
  r"Not converting the GP condition $b^2 = ac$ into an AP condition on logarithms.",
  "U06-B-gp-logs-exponents", r"Take logs, express each variable, apply $b^2 = ac$.",
  check=lambda: _c33().subs({Symbol('X', nonzero=True): _X, Symbol('Z', nonzero=True): _Z}),
  values=[(_X + _Z)/2, sqrt(_X*_Z), 2*_X*_Z/(_X + _Z), _X + _Z], cognitive="Understanding")


def _c34():
    sol = solve([Eq(a_/(1 - r), 9), Eq(a_*r, 2)], [a_, r], dict=True)
    return sum(s[a_] for s in sol if abs(s[r]) < 1)
q("U06-B-034", TOP, "Sum to infinity and second term", "Medium", "Multi-step computation MCQ",
  r"An infinite geometric progression has sum $9$ and second term $2$. The sum of all possible values of its first term is",
  r"$9$",
  [(r"$18$", r"Multiplies the two possible first terms $6$ and $3$ instead of adding."),
   (r"$6$", r"Keeps only the root $r = \frac{1}{3}$."),
   (r"$3$", r"Keeps only the root $r = \frac{2}{3}$.")],
  r"$a = \frac{2}{r}$ and $\frac{a}{1 - r} = 9$ give $2 = 9r(1 - r)$, i.e. $9r^2 - 9r + 2 = 0$, so $r = \frac{1}{3}$ or $\frac{2}{3}$ (both with $|r| < 1$). Then $a = 6$ or $3$, with sum $9$.",
  r"Discarding a valid root of the quadratic in $r$.",
  "U06-B-two-ratio-cases", r"Quadratic in $r$ with two admissible roots.",
  check=_c34, values=[9, 18, 6, 3], cognitive="Application",
  numerical=dict(question=r"An infinite geometric progression has sum $9$ and second term $2$. The sum of all possible values of its first term is", answer=9))


def _c35():
    v = Rational(2, 10) + inf_sum(Rational(45, 1000), Rational(1, 100))
    return v.p + v.q
q("U06-B-035", TOP, "Mixed recurring decimal in lowest terms", "Medium", "Multi-step computation MCQ",
  r"If $0.2\overline{45} = \frac{p}{q}$, where $p$ and $q$ are coprime positive integers, then $p + q$ equals",
  r"$137$",
  [(r"$46$", r"Uses denominator $999$: $\frac{243}{999} = \frac{9}{37}$."),
   (r"$1244$", r"Treats all three digits as recurring: $\frac{245}{999}$."),
   (r"$127$", r"Uses denominator $900$: $\frac{243}{900} = \frac{27}{100}$.")],
  r"$0.2\overline{45} = \frac{2}{10} + \frac{45/1000}{1 - 1/100} = \frac{2}{10} + \frac{45}{990} = \frac{198 + 45}{990} = \frac{243}{990} = \frac{27}{110}$. So $p + q = 137$.",
  r"Choosing the wrong denominator for a mixed recurring decimal.",
  "U06-B-recurring-mixed", r"Split into terminating part and a GP, add, reduce.",
  check=_c35, values=[137, 46, 1244, 127], cognitive="Application",
  numerical=dict(question=r"If $0.2\overline{45} = \frac{p}{q}$, where $p$ and $q$ are coprime positive integers, then $p + q$ is", answer=137))


def _c36():
    Rn, A, R = symbols('Rn A R', positive=True)
    S = lambda mult: A*(Rn**mult - 1)/(R - 1)
    rn = solve(Eq(S(2), 5*S(1)), Rn)
    rn = [v for v in rn if v != 1][0]
    return simplify((S(3)/S(1)).subs(Rn, rn))
q("U06-B-036", TOP, "Ratio of block sums", "Medium", "Multi-step computation MCQ",
  r"For a geometric progression with common ratio $r \ne 1$, the sum of the first $2n$ terms is $5$ times the sum of the first $n$ terms. Then $\frac{S_{3n}}{S_n}$ equals",
  r"$21$",
  [(r"$25$", r"Assumes $\frac{S_{3n}}{S_n} = \left(\frac{S_{2n}}{S_n}\right)^2$."),
   (r"$16$", r"Gives $r^{2n}$ instead of $1 + r^{n} + r^{2n}$."),
   (r"$63$", r"Takes $\frac{S_{3n}}{S_n} = r^{3n} - 1$.")],
  r"$\frac{S_{2n}}{S_n} = \frac{r^{2n} - 1}{r^{n} - 1} = 1 + r^{n} = 5$, so $r^{n} = 4$. Then $\frac{S_{3n}}{S_n} = \frac{r^{3n} - 1}{r^{n} - 1} = 1 + r^{n} + r^{2n} = 1 + 4 + 16 = 21$.",
  r"Not factoring $r^{3n} - 1$ correctly.",
  "U06-B-ratio-of-sums", r"Two factorizations in the variable $r^{n}$.",
  check=_c36, values=[21, 25, 16, 63], cognitive="Application",
  numerical=dict(question=r"For a geometric progression with common ratio $r \ne 1$, the sum of the first $2n$ terms is $5$ times the sum of the first $n$ terms. The value of $\frac{S_{3n}}{S_n}$ is", answer=21))


def _c37():
    A, R = symbols('A R', positive=True)
    p_, q2, r2 = symbols('p q r', integer=True, positive=True)
    T = lambda m: A*R**(m - 1)
    e1 = expand_log(log(T(p_)**(q2 - r2)*T(q2)**(r2 - p_)*T(r2)**(p_ - q2)), force=True)
    s1 = simplify(e1) == 0
    vals = {A: 1, R: 2, p_: 1, q2: 2, r2: 3}
    e2 = ((q2 - r2)*T(p_) + (r2 - p_)*T(q2) + (p_ - q2)*T(r2)).subs(vals)
    s2 = e2 == 0
    return (bool(s1), bool(s2))
q("U06-B-037", TOP, "Terms at positions p, q, r", "Medium", "Statement-based MCQ",
  r"The $p$th, $q$th and $r$th terms of a geometric progression of positive terms are $a$, $b$, $c$ respectively, where $p, q, r$ are distinct positive integers." "\n"
  r"Statement I: $a^{q-r}\, b^{r-p}\, c^{p-q} = 1$." "\n"
  r"Statement II: $(q - r)a + (r - p)b + (p - q)c = 0$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Carries over the AP identity $(q - r)a + (r - p)b + (p - q)c = 0$ to a GP."),
   (ST_FF, r"Expects the product to vanish rather than equal $1$, and rejects both."),
   (ST_FT, r"Mixes up the two identities, believing the linear one holds for a GP and the power one does not.")],
  r"With $a = AR^{p-1}$, $b = AR^{q-1}$, $c = AR^{r-1}$: the powers of $A$ add to $(q - r) + (r - p) + (p - q) = 0$ and those of $R$ to $(p-1)(q-r) + (q-1)(r-p) + (r-1)(p-q) = 0$, so Statement I is true. For Statement II, the GP $1, 2, 4$ with $p, q, r = 1, 2, 3$ gives $-1 + 4 - 4 = -1 \ne 0$, so it is false.",
  r"Confusing the AP identity with the GP identity for terms at given positions.",
  "U06-B-pqr-terms", r"Exponent bookkeeping plus a counterexample.",
  check=_c37, values=[TF, TT, FF, FT], cognitive="Analysis")


def _c38():
    sol = solve([Eq(a_*(1 + r), 5), Eq(a_/(1 - r), 9)], [a_, r], dict=True)
    return [s[r] for s in sol if s[r] > 0 and s[a_] > 0][0]
q("U06-B-038", TOP, "Ratio from partial sum and infinite sum", "Medium", "Inverse/parameter MCQ",
  r"An infinite geometric progression of positive terms has sum $9$, and the sum of its first two terms is $5$. Its common ratio is",
  r"$\frac{2}{3}$",
  [(r"$\frac{4}{9}$", r"Stops at $r^2 = \frac{4}{9}$ without taking the square root."),
   (r"$\frac{\sqrt{5}}{3}$", r"Solves $1 - r^2 = \frac{5}{9}$ as $r^2 = \frac{5}{9}$."),
   (r"$\frac{5}{9}$", r"Takes $r$ as the ratio of the two given sums, $\frac{5}{9}$.")],
  r"$a(1 + r) = 5$ and $a = 9(1 - r)$ give $9(1 - r^2) = 5$, so $r^2 = \frac{4}{9}$; positive terms force $r = \frac{2}{3}$ (and $a = 3$).",
  r"Mishandling $1 - r^2 = \frac{5}{9}$.",
  "U06-B-infinite-find-ratio", r"Two equations, eliminate $a$, sign condition picks the root.",
  check=_c38, values=[Rational(2, 3), Rational(4, 9), sqrt(5)/3, Rational(5, 9)], cognitive="Application")


def _c39():
    A, R = symbols('A R', positive=True)
    s = solve([Eq((A*R)**3, 64), Eq((A*R**4)**3, 1728)], [A, R], dict=True)[0]
    return ((A*R**7)**3).subs(s)
q("U06-B-039", TOP, "Products of consecutive blocks", "Medium", "Multi-step computation MCQ",
  r"In a geometric progression of positive terms, $T_1T_2T_3 = 64$ and $T_4T_5T_6 = 1728$. Then $T_7T_8T_9$ equals",
  r"$46656$",
  [(r"$5184$", r"Finds $r^{9} = 27$, so $r^{3} = 3$, then multiplies $1728$ by $r^{3}$ instead of $r^{9}$."),
   (r"$3392$", r"Treats the block products as an AP: $1728 + (1728 - 64)$."),
   (r"$15552$", r"Multiplies $1728$ by $r^{6} = 9$ instead of $r^{9} = 27$.")],
  r"Each term of the second block is $r^{3}$ times the corresponding term of the first, so $\frac{T_4T_5T_6}{T_1T_2T_3} = r^{9} = 27$. The third block is again $r^{9}$ times the second: $1728 \cdot 27 = 46656$.",
  r"Using $r^{3}$ instead of $r^{9}$ for the ratio of block products.",
  "U06-B-block-products", r"Recognise that block products form a GP with ratio $r^9$.",
  check=_c39, values=[46656, 5184, 3392, 15552], cognitive="Application")

q("U06-B-040", TOP, "Convergence condition", "Medium", "Inverse/parameter MCQ",
  r"The set of all real $x$ for which the infinite geometric series $1 + \frac{2x - 1}{3} + \left(\frac{2x - 1}{3}\right)^2 + \cdots$ has a finite sum is",
  r"$(-1, 2)$",
  [(r"$[-1, 2]$", r"Includes the endpoints, where $|r| = 1$ and the series diverges."),
   (r"$\left(\frac{1}{2}, 2\right)$", r"Allows only $0 < r < 1$, forgetting negative ratios."),
   (r"$(-2, 1)$", r"Sign slip, solving $|2x + 1| < 3$.")],
  r"Convergence needs $\left|\frac{2x - 1}{3}\right| < 1$, i.e. $-3 < 2x - 1 < 3$, so $-1 < x < 2$.",
  r"Including $|r| = 1$ or ignoring negative ratios.",
  "U06-B-convergence-range", r"One modulus inequality from $|r| < 1$.",
  check=lambda: solveset(Abs((2*x - 1)/3) < 1, x, S.Reals),
  values=[Interval.open(-1, 2), Interval(-1, 2), Interval.open(Rational(1, 2), 2), Interval.open(-2, 1)], cognitive="Application")


def _c41():
    A, R, m = symbols('A R m', positive=True)
    total = A*(R**(2*m) - 1)/(R - 1)
    odd = A*(R**(2*m) - 1)/(R**2 - 1)
    ratio = simplify(total/odd)
    return solve(Eq(ratio, 5), R)[0]
q("U06-B-041", TOP, "Odd-placed terms of a finite GP", "Medium", "Inverse/parameter MCQ",
  r"A geometric progression with positive terms has an even number of terms. The sum of all its terms is $5$ times the sum of the terms in the odd places. The common ratio is",
  r"$4$",
  [(r"$5$", r"Equates the common ratio to the given factor $5$."),
   (r"$2$", r"Writes the ratio of sums as $1 + r^{2}$."),
   (r"$\frac{1}{4}$", r"Takes the even-placed sum as $\frac{1}{r}$ times the odd-placed sum.")],
  r"Pair each odd-placed term with the next: $T_{2k} = rT_{2k-1}$, so the even-placed sum is $r$ times the odd-placed sum. Total $= (1 + r) \times$ odd-placed sum, so $1 + r = 5$ and $r = 4$.",
  r"Not seeing that the even-placed terms are $r$ times the odd-placed ones.",
  "U06-B-alternate-terms", r"Pairing argument, one equation.",
  check=_c41, values=[4, 5, 2, Rational(1, 4)], cognitive="Understanding")


def _c42():
    s = summation(Rational(9, 10)**0*9/Integer(10)**k, (k, 1, oo))
    t = summation(3/Integer(10)**k, (k, 1, oo))
    return (bool(s < 1), bool(Eq(t, Rational(1, 3))))
q("U06-B-042", TOP, "Recurring nines", "Medium", "Statement-based MCQ",
  r"Statement I: $0.\overline{9} < 1$." "\n"
  r"Statement II: The infinite geometric series $0.3 + 0.03 + 0.003 + \cdots$ has sum $\frac{1}{3}$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Believes $0.\overline{9}$ falls short of $1$ since every partial sum does."),
   (ST_TF, r"Accepts $0.\overline{9} < 1$ and also miscomputes the second series as $\frac{3}{10}$."),
   (ST_FF, r"Rejects Statement II, taking the sum as $\frac{3}{10}$ (first term only).")],
  r"$0.\overline{9} = \frac{9/10}{1 - 1/10} = 1$, so Statement I is false. $0.3 + 0.03 + \cdots = \frac{3/10}{9/10} = \frac{1}{3}$, so Statement II is true.",
  r"Confusing partial sums with the limit of an infinite GP.",
  "U06-B-recurring-statements", r"Two infinite GP sums, one counter-intuitive.",
  check=_c42, values=[FT, TT, TF, FF], cognitive="Understanding")


def _c43():
    pp, qq, u = symbols('p q u', positive=True)
    uu = [v for v in solve(Eq(qq*u**2, pp), u) if v.is_positive][0]  # u = R^n
    return simplify(qq*uu)
_p, _q = symbols('p q', positive=True)
q("U06-B-043", TOP, "Term midway between two given terms", "Medium", "Single-step computation MCQ",
  r"In a geometric progression of positive terms, the $(m + n)$th term is $p$ and the $(m - n)$th term is $q$, where $m > n \ge 1$. The $m$th term is",
  r"$\sqrt{pq}$",
  [(r"$\frac{p + q}{2}$", r"Uses the AP rule for the term midway between two terms."),
   (r"$\sqrt{\frac{p}{q}}$", r"Computes $r^{n} = \sqrt{\frac{p}{q}}$ and stops."),
   (r"$\left(\frac{p}{q}\right)^{\frac{1}{2n}}$", r"Computes the common ratio $r$ instead of $T_m$.")],
  r"$\frac{p}{q} = r^{2n}$, so $r^{n} = \sqrt{\frac{p}{q}}$. Then $T_m = T_{m-n} r^{n} = q\sqrt{\frac{p}{q}} = \sqrt{pq}$.",
  r"Using the arithmetic mean of equally spaced terms in a GP.",
  "U06-B-equidistant-terms", r"One ratio, one substitution.",
  check=lambda: _c43().subs({Symbol('p', positive=True): _p, Symbol('q', positive=True): _q}),
  values=[sqrt(_p*_q), (_p + _q)/2, sqrt(_p/_q), (_p/_q)**(1/(2*Symbol('n', integer=True, positive=True)))], cognitive="Application")

q("U06-B-044", TOP, "Bouncing ball", "Medium", "Multi-step computation MCQ",
  r"A ball is dropped from a height of $10$ m. After each bounce it rises to $\frac{3}{5}$ of the height from which it last fell. The total vertical distance (in m) travelled by the ball before it comes to rest is",
  r"$40$",
  [(r"$25$", r"Sums only the falls: $\frac{10}{1 - 3/5}$."),
   (r"$50$", r"Doubles every height including the first drop: $2 \cdot 25$."),
   (r"$30$", r"Counts each rebound up and down but omits the initial drop of $10$ m.")],
  r"The rebound heights are $6, \frac{18}{5}, \ldots$ with sum $\frac{6}{1 - 3/5} = 15$; each is travelled up and down. Total $= 10 + 2 \cdot 15 = 40$ m.",
  r"Counting the initial drop twice or not at all.",
  "U06-B-bouncing-ball", r"Model as a GP, handle the first drop separately.",
  check=lambda: 10 + 2*summation(10*Rational(3, 5)**k, (k, 1, oo)), values=[40, 25, 50, 30], cognitive="Application",
  numerical=dict(question=r"A ball is dropped from a height of $10$ m. After each bounce it rises to $\frac{3}{5}$ of the height from which it last fell. The total vertical distance, in metres, travelled by the ball before it comes to rest is", answer=40))

q("U06-B-045", TOP, "Nested squares", "Medium", "Multi-step computation MCQ",
  r"A square has side $8$ cm. A second square is formed by joining the midpoints of its sides, a third by joining the midpoints of the second, and so on indefinitely. The sum of the areas (in $\text{cm}^2$) of all the squares, including the first, is",
  r"$128$",
  [(r"$\frac{256}{3}$", r"Takes each new side as half the previous side, so the area ratio is $\frac{1}{4}$."),
   (r"$128 + 64\sqrt{2}$", r"Uses the side ratio $\frac{1}{\sqrt{2}}$ as the ratio of areas."),
   (r"$64$", r"Leaves out the first square, summing $32 + 16 + \cdots$.")],
  r"Joining midpoints gives side $\frac{s}{\sqrt{2}}$, so each area is half the previous one: $64, 32, 16, \ldots$. The sum is $\frac{64}{1 - 1/2} = 128$.",
  r"Using the side ratio instead of the area ratio.",
  "U06-B-nested-figures", r"Geometry gives the ratio; then an infinite GP.",
  check=lambda: summation(64*Rational(1, 2)**k, (k, 0, oo)), values=[128, Rational(256, 3), 128 + 64*sqrt(2), 64], cognitive="Application",
  numerical=dict(question=r"A square has side $8$ cm. A second square is formed by joining the midpoints of its sides, a third by joining the midpoints of the second, and so on indefinitely. The sum of the areas, in $\text{cm}^2$, of all the squares, including the first, is", answer=128))

# =================================================================== DIFFICULT


def _c46():
    sol = solve([Eq(a_ + a_*r, 4), Eq(a_*r**2 + a_*r**3, 16)], [a_, r], dict=True)
    return sum(s[a_]*s[r]**4 for s in sol if s[r].is_real)
q("U06-B-046", TOP, "Casework on the ratio", "Difficult", "Multi-step computation MCQ",
  r"In a geometric progression of real numbers, $a_1 + a_2 = 4$ and $a_3 + a_4 = 16$. The sum of all possible values of $a_5$ is",
  r"$-\frac{128}{3}$",
  [(r"$\frac{64}{3}$", r"Takes only $r = 2$ from $r^2 = 4$."),
   (r"$-64$", r"Takes only $r = -2$."),
   (r"$\frac{256}{3}$", r"For $r = -2$, writes $a(1 + r) = a$ and gets $a = 4$, so $a_5 = 64$; then $\frac{64}{3} + 64$.")],
  r"$\frac{a_3 + a_4}{a_1 + a_2} = r^2 = 4$, so $r = \pm 2$. If $r = 2$: $3a = 4$, $a = \frac{4}{3}$, $a_5 = \frac{64}{3}$. If $r = -2$: $-a = 4$, $a = -4$, $a_5 = -64$. Sum $= \frac{64}{3} - 64 = -\frac{128}{3}$.",
  r"Ignoring the negative ratio, or mishandling $1 + r$ when $r = -2$.",
  "U06-B-two-ratio-cases", r"Two cases from $r^2 = 4$, each needing its own first term; sign trap in the negative case.",
  check=_c46, values=[Rational(-128, 3), Rational(64, 3), -64, Rational(256, 3)], cognitive="Analysis")


def _c47():
    a, r = symbols('a r', real=True)
    sols = solve([Eq(a/(1 - r), Rational(4, 3)), Eq(a**2/(1 - r**2), Rational(16, 3))], [a, r], dict=True)
    sols = [d for d in sols if d[r].is_real and abs(d[r]) < 1 and d[a] != 0]
    assert len(sols) == 1
    A, R = sols[0][a], sols[0][r]
    S = A/(1 - R)
    m = 1
    while not Abs(S - gp_sum(A, R, m)) < Rational(1, 1000):
        m += 1
    return m
q("U06-B-047", TOP, "Tail of an infinite GP", "Difficult", "Inverse/parameter MCQ",
  r"An infinite geometric progression of real terms has sum $\frac{4}{3}$, and the sum of the squares of its terms is $\frac{16}{3}$. If $S_n$ is the sum of its first $n$ terms and $S$ its sum to infinity, the least $n$ for which $|S - S_n| < 10^{-3}$ is",
  r"$11$",
  [(r"$10$", r"Finds $r = -\frac{1}{2}$ but takes the error as just $|r|^{n} = \frac{1}{2^{n}}$, dropping the factor $\frac{a}{1 - r} = \frac{4}{3}$; $2^{n} > 1000$ gives $n = 10$."),
   (r"$12$", r"Uses $\frac{a|r|^{n}}{1 - |r|} = \frac{4}{2^{n}}$, i.e. $1 - r = \frac{1}{2}$ as if $r = \frac{1}{2}$; $2^{n} > 4000$ gives $n = 12$."),
   (r"$7$", r"Applies the tail bound to the series of squares: $\frac{16}{3}\cdot\frac{1}{4^{n}} < 10^{-3}$, i.e. $4^{n} > \frac{16000}{3}$, giving $n = 7$.")],
  r"From $\frac{a}{1 - r} = \frac{4}{3}$ and $\frac{a^{2}}{1 - r^{2}} = \frac{16}{3}$, dividing gives $\frac{a}{1 + r} = 4$, so $4(1 + r) = \frac{4}{3}(1 - r)$, $r = -\frac{1}{2}$ and $a = 2$. Then $|S - S_n| = \left|\frac{ar^{n}}{1 - r}\right| = \frac{4}{3}\cdot\frac{1}{2^{n}}$. We need $2^{n} > \frac{4000}{3} \approx 1333.3$; since $2^{10} = 1024$ and $2^{11} = 2048$, the least $n$ is $11$.",
  r"Mis-stating the tail $\frac{ar^{n}}{1 - r}$ of an infinite GP when the ratio is negative.",
  "U06-B-tail-estimate", r"Two infinite sums must be solved for $a$ and a negative $r$ first, then the tail with $|r|$ and $1 - r$ handled correctly, then a power-of-2 bound; three linked steps with sign traps.",
  check=_c47, values=[11, 10, 12, 7], cognitive="Analysis",
  numerical=dict(question=r"An infinite geometric progression of real terms has sum $\frac{4}{3}$, and the sum of the squares of its terms is $\frac{16}{3}$. If $S_n$ is the sum of its first $n$ terms and $S$ its sum to infinity, the least positive integer $n$ for which $|S - S_n| < 10^{-3}$ is", answer=11))


def _c48():
    R = Symbol('R', positive=True)
    terms = [2/R**2, 2/R, 2, 2*R, 2*R**2]
    rs = solve(Eq(sum(terms), Rational(31, 2)), R)
    vals = {simplify(sum(1/t for t in terms).subs(R, v)) for v in rs}
    assert len(vals) == 1
    return vals.pop()
q("U06-B-048", TOP, "Sum of reciprocals from sum and product", "Difficult", "Multi-step computation MCQ",
  r"Five positive numbers are in geometric progression. Their product is $32$ and their sum is $\frac{31}{2}$. The sum of their reciprocals is",
  r"$\frac{31}{8}$",
  [(r"$\frac{31}{4}$", r"Divides the sum by $T_3 = 2$ instead of $T_3^2 = T_1T_5 = 4$."),
   (r"$\frac{31}{64}$", r"Uses the product of all five terms, $32$, in place of $T_1T_5$."),
   (r"$\frac{2}{31}$", r"Takes the reciprocal of the sum.")],
  r"The product gives $T_3^5 = 32$, so $T_3 = 2$. Reciprocals of a GP form a GP, and pairing $\frac{1}{T_1} + \frac{1}{T_5} = \frac{T_1 + T_5}{T_1T_5}$ (similarly for $T_2, T_4$) with $T_1T_5 = T_2T_4 = T_3^2 = 4$ gives $\sum \frac{1}{T_i} = \frac{\sum T_i}{T_3^2} = \frac{31/2}{4} = \frac{31}{8}$.",
  r"Not using $T_iT_{6-i} = T_3^2$ to link the two sums.",
  "U06-B-reciprocal-sum-product", r"Non-obvious route: product fixes the middle term, pairing links reciprocal sum to sum.",
  check=_c48, values=[Rational(31, 8), Rational(31, 4), Rational(31, 64), Rational(2, 31)], cognitive="Analysis",
  numerical=dict(question=r"Five positive numbers are in geometric progression. Their product is $32$ and their sum is $\frac{31}{2}$. If $T$ is the sum of their reciprocals, then $T$ multiplied by $8$ equals", answer=31))


def _c49():
    sol = solve([Eq(a_/(1 - r), 57), Eq(a_**3/(1 - r**3), 9747)], [a_, r], dict=True)
    return [s[a_] for s in sol if s[r].is_real and abs(s[r]) < 1][0]
q("U06-B-049", TOP, "Sum and sum of cubes", "Difficult", "Multi-step computation MCQ",
  r"An infinite geometric progression has sum $57$, and the sum of the cubes of its terms is $9747$. Its first term is",
  r"$19$",
  [(r"$-\frac{57}{2}$", r"Accepts the root $r = \frac{3}{2}$ of $6r^2 - 13r + 6 = 0$, which fails $|r| < 1$."),
   (r"$38$", r"Finds $r = \frac{2}{3}$ but uses $a = Sr$ instead of $a = S(1 - r)$."),
   (r"$3\sqrt{19}$", r"Takes $\frac{9747}{57} = 171$ as $a^2$, ignoring the factors of $r$.")],
  r"$\frac{a^3/(1 - r^3)}{\left(a/(1 - r)\right)^3} = \frac{(1 - r)^2}{1 + r + r^2} = \frac{9747}{57^3} = \frac{1}{19}$. So $19(1 - 2r + r^2) = 1 + r + r^2$, i.e. $6r^2 - 13r + 6 = 0$, giving $r = \frac{2}{3}$ or $\frac{3}{2}$. Only $r = \frac{2}{3}$ has $|r| < 1$, so $a = 57 \cdot \frac{1}{3} = 19$.",
  r"Keeping a ratio with $|r| \ge 1$ for an infinite sum.",
  "U06-B-sum-and-cubes", r"Eliminate $a$ via a ratio of sums, factor $1 - r^3$, reject a root using convergence.",
  check=_c49, values=[19, Rational(-57, 2), 38, 3*sqrt(19)], cognitive="Analysis",
  numerical=dict(question=r"An infinite geometric progression has sum $57$, and the sum of the cubes of its terms is $9747$. The first term of the progression is", answer=19))


def _c50():
    A, R = symbols('A R', nonzero=True)
    a1, b1, c1, d1 = A, A*R, A*R**2, A*R**3
    s1 = simplify((a1**2 + b1**2 + c1**2)*(b1**2 + c1**2 + d1**2) - (a1*b1 + b1*c1 + c1*d1)**2) == 0
    s2 = simplify((b1 - c1)**2 + (c1 - a1)**2 + (d1 - b1)**2 - (a1 - d1)**2) == 0
    return (bool(s1), bool(s2))
q("U06-B-050", TOP, "Identities for four terms in GP", "Difficult", "Statement-based MCQ",
  r"Let $a, b, c, d$ be real numbers in geometric progression." "\n"
  r"Statement I: $(a^2 + b^2 + c^2)(b^2 + c^2 + d^2) = (ab + bc + cd)^2$." "\n"
  r"Statement II: $(b - c)^2 + (c - a)^2 + (d - b)^2 = (a - d)^2$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Verifies Statement I but expands $(a - d)^2$ without the cross term $-2ad$ and rejects Statement II."),
   (ST_FT, r"Treats Statement I as a Cauchy-Schwarz inequality that is always strict, missing the equality case for proportional triples."),
   (ST_FF, r"Tests with an AP such as $1, 2, 3, 4$ instead of a GP and rejects both.")],
  r"Write $b = a\rho$, $c = a\rho^2$, $d = a\rho^3$. Then $(b, c, d) = \rho(a, b, c)$, so the left side of Statement I is $\rho^2(a^2 + b^2 + c^2)^2$ and the right side is $\left(\rho(a^2 + b^2 + c^2)\right)^2$: equal. For Statement II, expanding gives $2(b^2 + c^2) - 2bc - 2ca - 2bd + a^2 + d^2$; using $b^2 = ac$, $c^2 = bd$, $bc = ad$ this reduces to $a^2 + d^2 - 2ad = (a - d)^2$. Both are true.",
  r"Not using $b^2 = ac$, $c^2 = bd$, $bc = ad$ to simplify.",
  "U06-B-four-term-identities", r"Two algebraic identities needing the GP relations in the right combination.",
  check=_c50, values=[TT, TF, FT, FF], cognitive="Analysis")

_x, _y = symbols('x y', positive=True)


def _c51():
    X, Y = symbols('x y', positive=True)
    A = 1 - 1/X
    B = 1 - 1/Y
    return simplify(1/(1 - A*B))
q("U06-B-051", TOP, "Sums of related infinite GPs", "Difficult", "Multi-step computation MCQ",
  r"Let $|\alpha| < 1$ and $|\beta| < 1$. If $x = \sum_{n=0}^{\infty} \alpha^{n}$, $y = \sum_{n=0}^{\infty} \beta^{n}$ and $z = \sum_{n=0}^{\infty} (\alpha\beta)^{n}$, then $z$ equals",
  r"$\frac{xy}{x + y - 1}$",
  [(r"$\frac{xy}{x + y + 1}$", r"Expands $(x - 1)(y - 1)$ as $xy - x - y - 1$."),
   (r"$\frac{xy}{x + y}$", r"Drops the constant $1$ in $(x - 1)(y - 1) = xy - x - y + 1$."),
   (r"$\frac{x + y - 1}{xy}$", r"Finds $1 - \alpha\beta$ and stops, without taking the reciprocal.")],
  r"$x = \frac{1}{1 - \alpha}$ gives $\alpha = \frac{x - 1}{x}$; similarly $\beta = \frac{y - 1}{y}$. Then $1 - \alpha\beta = \frac{xy - (x - 1)(y - 1)}{xy} = \frac{x + y - 1}{xy}$, so $z = \frac{xy}{x + y - 1}$.",
  r"Algebra slips while eliminating $\alpha$ and $\beta$.",
  "U06-B-related-infinite-sums", r"Invert two sum formulas and recombine; careful expansion.",
  check=_c51, values=[_x*_y/(_x + _y - 1), _x*_y/(_x + _y + 1), _x*_y/(_x + _y), (_x + _y - 1)/(_x*_y)], cognitive="Analysis")


def _c52():
    A, R = symbols('A R', positive=True)
    Aexpr = 189/sum(R**j for j in range(6))
    eq2 = together(sum(1/(Aexpr*R**j) for j in range(6)) - Rational(21, 32))
    Rs = [v for v in Poly(numer(eq2), R).real_roots() if v > 0]
    prods = {simplify(prod([Aexpr.subs(R, v)*v**j for j in range(6)])) for v in Rs}
    assert len(prods) == 1
    return prods.pop()
q("U06-B-052", TOP, "Product from sum and sum of reciprocals", "Difficult", "Multi-step computation MCQ",
  r"A geometric progression has six positive terms. The sum of the terms is $189$ and the sum of their reciprocals is $\frac{21}{32}$. The product of the six terms is",
  r"$288^{3}$",
  [(r"$288^{6}$", r"Finds $\left(\frac{S}{R}\right)^{n} = P^2$ and forgets the square root."),
   (r"$288^{\frac{5}{2}}$", r"Uses $P^2 = \left(\frac{S}{R}\right)^{n-1}$."),
   (r"$\left(\frac{3969}{32}\right)^{3}$", r"Uses the product $SR$ in place of the quotient $\frac{S}{R}$.")],
  r"If $S$ and $R$ are the sums of the terms and of their reciprocals, then $\frac{S}{R} = a^2 r^{n-1} = T_1T_n$, and $P^2 = (T_1T_n)^{n}$. Here $\frac{S}{R} = 189 \cdot \frac{32}{21} = 288$, so $P^2 = 288^{6}$ and $P = 288^{3}$ (terms positive).",
  r"Not recognising $\frac{S}{R} = T_1T_n$.",
  "U06-B-reciprocal-sum-product", r"Needs the identity $\frac{S}{R} = T_1T_n$ and the pairing of terms for the product.",
  check=_c52, values=[Integer(288)**3, Integer(288)**6, Integer(288)**Rational(5, 2), Rational(3969, 32)**3], cognitive="Analysis")


def _c53():
    A, R = symbols('A R', positive=True)
    sol = solve([Eq(A*A*R**4, 16), Eq(A*R + A*R**3, 10)], [A, R], dict=True)
    return sum(s[A] for s in sol)
q("U06-B-053", TOP, "Possible first terms", "Difficult", "Multi-step computation MCQ",
  r"In a geometric progression of positive terms, $a_1a_5 = 16$ and $a_2 + a_4 = 10$. The sum of all possible values of $a_1$ is",
  r"$17$",
  [(r"$1$", r"Takes only $r = 2$."),
   (r"$16$", r"Takes only $r = \frac{1}{2}$."),
   (r"$10$", r"Finds $r = 2, \frac{1}{2}$ but uses $a_1 = \frac{a_3}{r}$: $2 + 8$.")],
  r"$a_1a_5 = a_3^2 = 16$, so $a_3 = 4$. Then $a_2 + a_4 = \frac{4}{r} + 4r = 10$, i.e. $2r^2 - 5r + 2 = 0$, so $r = 2$ or $\frac{1}{2}$. Then $a_1 = \frac{4}{r^2} = 1$ or $16$, with sum $17$.",
  r"Losing one admissible ratio, or the wrong power of $r$ when going back to $a_1$.",
  "U06-B-two-ratio-cases-positive", r"Middle-term trick, quadratic in $r$, two cases back-substituted.",
  check=_c53, values=[17, 1, 16, 10], cognitive="Analysis",
  numerical=dict(question=r"In a geometric progression of positive terms, $a_1a_5 = 16$ and $a_2 + a_4 = 10$. The sum of all possible values of $a_1$ is", answer=17))


def _c54():
    return imageset(Lambda(r, 5*(1 - r)), Union(Interval.open(-1, 0), Interval.open(0, 1)))
q("U06-B-054", TOP, "Range of the first term", "Difficult", "Conceptual/application MCQ",
  r"An infinite geometric progression with non-zero common ratio has sum $5$. The set of all possible values of its first term is",
  r"$(0, 5) \cup (5, 10)$",
  [(r"$(0, 10)$", r"Allows $r = 0$, which gives $a = 5$."),
   (r"$(0, 5)$", r"Allows only $0 < r < 1$."),
   (r"$(0, 5) \cup (5, 10]$", r"Allows $r = -1$, for which the series does not converge.")],
  r"$a = 5(1 - r)$ with $r \in (-1, 0) \cup (0, 1)$. As $r$ runs over $(0, 1)$, $a$ runs over $(0, 5)$; over $(-1, 0)$, $a$ runs over $(5, 10)$. So $a \in (0, 5) \cup (5, 10)$; the value $5$ (from $r = 0$) and $10$ (from $r = -1$) are excluded.",
  r"Ignoring the exclusions $r \ne 0$ and $|r| < 1$ at the endpoints.",
  "U06-B-range-from-sum", r"Map an open punctured interval of $r$ to $a$; two boundary traps.",
  check=_c54, values=[Union(Interval.open(0, 5), Interval.open(5, 10)), Interval.open(0, 10), Interval.open(0, 5),
                      Union(Interval.open(0, 5), Interval.Lopen(5, 10))], cognitive="Analysis")

q("U06-B-055", TOP, "Squaring a sum of two GP terms", "Difficult", "Multi-step computation MCQ",
  r"The value of $\displaystyle\sum_{n=1}^{\infty} \left(\frac{1}{2^{n}} + \frac{1}{3^{n}}\right)^{2}$ is",
  r"$\frac{103}{120}$",
  [(r"$\frac{9}{4}$", r"Squares the sum of the two series, $\left(1 + \frac{1}{2}\right)^2$, instead of summing the squares."),
   (r"$\frac{11}{24}$", r"Drops the cross term $\frac{2}{6^{n}}$: $\frac{1}{3} + \frac{1}{8}$."),
   (r"$\frac{79}{120}$", r"Takes the cross term as $\frac{1}{6^{n}}$, missing the factor $2$.")],
  r"Expand: $\frac{1}{4^{n}} + \frac{2}{6^{n}} + \frac{1}{9^{n}}$. The three GP sums from $n = 1$ are $\frac{1}{3}$, $2 \cdot \frac{1}{5} = \frac{2}{5}$ and $\frac{1}{8}$. Total $= \frac{40 + 48 + 15}{120} = \frac{103}{120}$.",
  r"Treating the sum of squares as the square of the sum.",
  "U06-B-split-infinite-sums", r"Expansion into three GPs, each started at $n = 1$; cross term is the trap.",
  check=lambda: summation((1/Integer(2)**k + 1/Integer(3)**k)**2, (k, 1, oo)),
  values=[Rational(103, 120), Rational(9, 4), Rational(11, 24), Rational(79, 120)], cognitive="Analysis")


def _c56():
    A, R = symbols('A R', positive=True)
    sol = solve([Eq(A/R + A + A*R, 7), Eq(R/A + 1/A + 1/(A*R), Rational(7, 4))], [A, R], dict=True)
    ps = {simplify(s[A]**3) for s in sol}
    assert len(ps) == 1
    return ps.pop()
q("U06-B-056", TOP, "Product from sum and reciprocal sum", "Difficult", "Inverse/parameter MCQ",
  r"Three positive numbers in geometric progression have sum $7$, and the sum of their reciprocals is $\frac{7}{4}$. Their product is",
  r"$8$",
  [(r"$4$", r"Stops at $T_2^2 = \frac{7}{7/4} = 4$."),
   (r"$2$", r"Gives the middle term $T_2$ instead of the product."),
   (r"$64$", r"Cubes $T_2^2 = 4$ instead of $T_2 = 2$.")],
  r"For $\frac{T_2}{r}, T_2, T_2r$, the reciprocal sum is $\frac{1}{T_2^2}\left(T_2r + T_2 + \frac{T_2}{r}\right) = \frac{7}{T_2^2}$. So $\frac{7}{T_2^2} = \frac{7}{4}$, $T_2 = 2$, and the product is $T_2^3 = 8$ (the numbers are $1, 2, 4$).",
  r"Confusing $T_2^2$ with $T_2$ or with the product.",
  "U06-B-reciprocal-sum-product", r"Hidden relation between sum and reciprocal sum; reverse unknown.",
  check=_c56, values=[8, 4, 2, 64], cognitive="Analysis",
  numerical=dict(question=r"Three positive numbers in geometric progression have sum $7$, and the sum of their reciprocals is $\frac{7}{4}$. The product of the three numbers is", answer=8))


def _c57():
    f = 4*r*(1 - r)
    from sympy.calculus.util import function_range
    return Union(function_range(f, r, Interval.open(-1, 0)), function_range(f, r, Interval.open(0, 1)))
q("U06-B-057", TOP, "Range of the second term", "Difficult", "Conceptual/application MCQ",
  r"An infinite geometric progression with non-zero common ratio has sum $4$. The set of all possible values of its second term is",
  r"$(-8, 0) \cup (0, 1]$",
  [(r"$(0, 1]$", r"Considers only $0 < r < 1$."),
   (r"$(-8, 1]$", r"Allows $r = 0$, letting the second term be $0$."),
   (r"$[-8, 0) \cup (0, 1]$", r"Allows $r = -1$, for which the series does not converge.")],
  r"$a = 4(1 - r)$, so $T_2 = 4r(1 - r)$ with $r \in (-1, 0) \cup (0, 1)$. On $(0, 1)$ this rises to its maximum $1$ at $r = \frac{1}{2}$ and tends to $0$ at both ends: values $(0, 1]$. On $(-1, 0)$ it is increasing from $-8$ to $0$: values $(-8, 0)$. Hence $(-8, 0) \cup (0, 1]$.",
  r"Ignoring negative ratios or the open endpoints.",
  "U06-B-range-from-sum", r"Quadratic in $r$ over two open intervals; endpoint and vertex analysis.",
  check=_c57, values=[Union(Interval.open(-8, 0), Interval.Lopen(0, 1)), Interval.Lopen(0, 1), Interval.Lopen(-8, 1),
                      Union(Interval.Ropen(-8, 0), Interval.Lopen(0, 1))], cognitive="Analysis")


def _c58():
    m = 1
    while prod([Rational(1, 8)*2**j for j in range(m)]) != 1:
        m += 1
    return m
q("U06-B-058", TOP, "Product of first n terms equal to 1", "Difficult", "Inverse/parameter MCQ",
  r"For the geometric progression $\frac{1}{8}, \frac{1}{4}, \frac{1}{2}, 1, 2, \ldots$, the positive integer $n$ for which the product of the first $n$ terms equals $1$ is",
  r"$7$",
  [(r"$4$", r"Stops at the term that equals $1$, i.e. $T_4$."),
   (r"$5$", r"Uses the exponent sum $\frac{n(n+1)}{2}$ for $r$: $-3n + \frac{n(n+1)}{2} = 0$."),
   (r"$6$", r"Uses the exponent $\frac{n^2}{2}$ for $r$: $-3n + \frac{n^2}{2} = 0$.")],
  r"The product is $a^{n}r^{n(n-1)/2} = 2^{-3n + n(n-1)/2}$. Setting the exponent to $0$ gives $n - 1 = 6$, so $n = 7$ (the terms $2^{-3}, \ldots, 2^{3}$ are symmetric about $1$).",
  r"Using the wrong exponent sum for $r$ in the product of terms.",
  "U06-B-product-formula", r"Product formula as an equation in $n$; symmetry insight helps.",
  check=_c58, values=[7, 4, 5, 6], cognitive="Analysis",
  numerical=dict(question=r"For the geometric progression $\frac{1}{8}, \frac{1}{4}, \frac{1}{2}, 1, 2, \ldots$, the positive integer $n$ for which the product of the first $n$ terms equals $1$ is", answer=7))

q("U06-B-059", TOP, "GP of recurring decimals", "Difficult", "Multi-step computation MCQ",
  r"The value of $0.\overline{7} + 0.0\overline{7} + 0.00\overline{7} + \cdots$ (infinitely many terms, each obtained from the previous by shifting the digits one place to the right) is",
  r"$\frac{70}{81}$",
  [(r"$\frac{7}{8}$", r"Uses the common ratio $\frac{1}{9}$ instead of $\frac{1}{10}$: $\frac{7/9}{8/9}$."),
   (r"$\frac{7}{10}$", r"Multiplies $\frac{7}{9}$ by $1 - r = \frac{9}{10}$ instead of dividing."),
   (r"$\frac{700}{891}$", r"Uses the common ratio $\frac{1}{100}$: $\frac{7/9}{99/100}$.")],
  r"$0.\overline{7} = \frac{7}{9}$, and each later term is $\frac{1}{10}$ of the previous, so the terms form a GP $\frac{7}{9}, \frac{7}{90}, \ldots$ with $r = \frac{1}{10}$. The sum is $\frac{7/9}{9/10} = \frac{70}{81}$.",
  r"Misidentifying the ratio between successive shifted decimals.",
  "U06-B-recurring-gp-of-gps", r"Each term is itself an infinite GP; then a second GP over the terms.",
  check=lambda: summation(inf_sum(Rational(7, 10), Rational(1, 10))/Integer(10)**k, (k, 0, oo)),
  values=[Rational(70, 81), Rational(7, 8), Rational(7, 10), Rational(700, 891)], cognitive="Analysis")


def _c60():
    import itertools
    cnt = 0
    for a1, c1 in itertools.product(range(1, 145), repeat=2):
        if a1*c1 == 144 and a1 != c1:
            cnt += 1
    return cnt
q("U06-B-060", TOP, "Counting integer GPs with a given middle term", "Difficult", "Multi-step computation MCQ",
  r"The number of ordered triples $(a, 12, c)$ of positive integers, with $a \ne c$, that are three consecutive terms of a geometric progression is",
  r"$14$",
  [(r"$15$", r"Counts all divisors of $144$, including $a = c = 12$."),
   (r"$7$", r"Counts unordered pairs $\{a, c\}$, treating $(a, 12, c)$ and $(c, 12, a)$ as the same."),
   (r"$8$", r"Counts unordered pairs and also includes the constant triple $(12, 12, 12)$.")],
  r"The condition is $ac = 12^2 = 144$, so $a$ is any positive divisor of $144 = 2^4 \cdot 3^2$, which has $5 \cdot 3 = 15$ divisors. Excluding $a = 12$ (which gives $c = 12$) leaves $14$ ordered triples.",
  r"Overlooking the order of the triple or the excluded constant case.",
  "U06-B-integer-gp-count", r"Translate to $ac = 144$, count divisors, handle order and the excluded case.",
  check=_c60, values=[14, 15, 7, 8], cognitive="Analysis",
  numerical=dict(question=r"The number of ordered triples $(a, 12, c)$ of positive integers, with $a \ne c$, that are three consecutive terms of a geometric progression is", answer=14))
