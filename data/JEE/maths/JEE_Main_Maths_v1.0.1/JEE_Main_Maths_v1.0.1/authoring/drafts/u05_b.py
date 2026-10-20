import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from itertools import combinations

# ---------------------------------------------------------------- helpers
x, y, a = symbols('x y a')
_n = symbols('n', positive=True, integer=True)


def gterms(p, s, n):
    """General terms T_{k+1} = C(n,k) p^(n-k) s^k, k = 0..n, verified against the expansion."""
    ts = [binomial(n, k) * p**(n - k) * s**k for k in range(n + 1)]
    assert expand(sum(ts) - (p + s)**n) == 0
    return ts


def middles(p, s, n):
    ts = gterms(p, s, n)
    m = len(ts)
    return [ts[m // 2]] if m % 2 else [ts[m // 2 - 1], ts[m // 2]]


def nterms(e):
    return len(Add.make_args(expand(e)))


def coeffs(e):
    """Coefficients a_0, a_1, ... of a polynomial in x."""
    return Poly(expand(e), x).all_coeffs()[::-1]


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

T_NUM = "Number of terms"
T_MID = "Middle terms"
T_SUM = "Sums of binomial coefficients"
T_GRT = "Greatest coefficient"

# ================================================================ EASY (14)

q("U05-B-001", T_NUM, "Number of terms in a binomial expansion", "Easy", "Direct concept MCQ",
  r"The number of terms in the expansion of $(2x - 3y)^{11}$ is",
  r"$12$",
  [(r"$11$", r"Takes the number of terms equal to the index $n = 11$ rather than $n + 1$."),
   (r"$24$", r"Treats $(2x)^{11}$ and $(-3y)^{11}$ as giving separate expansions, counts $n + 1 = 12$ terms for each part and adds them to get $24$."),
   (r"$6$", r"Assumes the negative sign makes alternate terms cancel, as happens in $(x+a)^{n} - (x-a)^{n}$, and keeps only $\frac{12}{2} = 6$ terms.")],
  r"An expansion $(p + s)^n$ with $n$ a positive integer has $n + 1$ terms, and here no two terms combine because each has a different power of $x$. With $n = 11$ the expansion of $(2x - 3y)^{11}$ has $12$ terms; the signs alternate but nothing cancels.",
  "Confusing the index $n$ with the number of terms $n+1$.",
  "U05-B-numterms-basic", "One fact, applied once.",
  check=lambda: nterms((2*x - 3*y)**11), values=[12, 11, 24, 6], cognitive="Recall", source_class="XI")

q("U05-B-002", T_MID, "Single middle term", "Easy", "Single-step computation MCQ",
  r"The middle term in the expansion of $\left(2x - \frac{y}{3}\right)^{6}$ is",
  r"$-\frac{160}{27}x^3y^3$",
  [(r"$\frac{160}{27}x^3y^3$", r"Treats $\left(-\frac{y}{3}\right)^3$ as positive, a sign slip on the odd power."),
   (r"$\frac{80}{3}x^4y^2$", r"Takes $T_3 = \binom{6}{2}(2x)^4\left(-\frac{y}{3}\right)^2 = \frac{80}{3}x^4y^2$, using $\frac{n}{2}$ as the term number instead of $\frac{n}{2} + 1$."),
   (r"$-\frac{8}{27}x^3y^3$", r"Raises $2x$ and $-\frac{y}{3}$ to the powers but omits the binomial coefficient $\binom{6}{3} = 20$.")],
  r"With $n = 6$ there are $7$ terms, so the middle term is $T_4 = \binom{6}{3}(2x)^3\left(-\frac{y}{3}\right)^3 = 20 \cdot 8x^3 \cdot \left(-\frac{y^3}{27}\right) = -\frac{160}{27}x^3y^3$.",
  "Picking the wrong term number for the middle term or losing the sign of an odd power.",
  "U05-B-middle-single", "Locate the middle term and evaluate one general term.",
  check=lambda: middles(2*x, -y/3, 6)[0],
  values=[Rational(-160, 27)*x**3*y**3, Rational(160, 27)*x**3*y**3, Rational(80, 3)*x**4*y**2, Rational(-8, 27)*x**3*y**3],
  cognitive="Application", source_class="XI")

q("U05-B-003", T_SUM, "Sum of coefficients by substitution", "Easy", "Single-step computation MCQ",
  r"The sum of the coefficients of all the terms in the expansion of $(2x - 5y)^{3}$ is",
  r"$-27$",
  [(r"$27$", r"Drops the sign: computes $(2-5)^3$ as $3^3$."),
   (r"$343$", r"Adds the absolute values of the coefficients, i.e. computes $(2+5)^3$."),
   (r"$8$", r"Gives the sum of the binomial coefficients $2^3$, ignoring the numerical factors $2$ and $-5$.")],
  r"The sum of the coefficients is the value of the expression at $x = y = 1$, namely $(2 - 5)^3 = (-3)^3 = -27$.",
  "Confusing the sum of coefficients with the sum of binomial coefficients $2^n$.",
  "U05-B-sumcoeff-eval", "One substitution.",
  check=lambda: expand((2*x - 5*y)**3).subs({x: 1, y: 1}), values=[-27, 27, 343, 8],
  cognitive="Application", source_class="XI")

def _c4():
    n = solve(Eq(2**_n, 256), _n)[0]
    return nterms((x**2 + 1/x)**n)
q("U05-B-004", T_NUM, "Index from the sum of binomial coefficients", "Easy", "Inverse/parameter MCQ",
  r"If the sum of the binomial coefficients in the expansion of $\left(x^2 + \frac{1}{x}\right)^{n}$ is $256$, then the number of terms in the expansion is",
  r"$9$",
  [(r"$8$", r"Finds $n = 8$ correctly but reports $n$ as the number of terms."),
   (r"$10$", r"Uses $2^{n-1} = 256$, getting $n = 9$ and hence $10$ terms."),
   (r"$5$", r"Finds $n = 8$ but reports the position $\frac{n}{2} + 1 = 5$ of the middle term.")],
  r"The binomial coefficients sum to $2^n$, so $2^n = 256$ gives $n = 8$. The powers of $x$ in $T_{r+1}$ are $16 - 3r$, all distinct, so the expansion has $n + 1 = 9$ terms.",
  "Reporting $n$ instead of $n+1$ as the number of terms.",
  "U05-B-sum-binom-coeff", "Two short steps: $2^n$ then $n + 1$.",
  check=_c4, values=[9, 8, 10, 5], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If the sum of the binomial coefficients in the expansion of $\left(x^2 + \frac{1}{x}\right)^{n}$ is $256$, then the number of terms in the expansion is", answer=9))

q("U05-B-005", T_SUM, "Sum of even-indexed binomial coefficients", "Easy", "Single-step computation MCQ",
  r"The value of $\binom{10}{0} + \binom{10}{2} + \binom{10}{4} + \cdots + \binom{10}{10}$ is",
  r"$512$",
  [(r"$1024$", r"Gives the sum of all the binomial coefficients $2^{10}$."),
   (r"$256$", r"Uses $2^{n-2}$, halving twice."),
   (r"$511$", r"Leaves out $\binom{10}{0} = 1$ from the sum $2^{9}$.")],
  r"Adding $(1+1)^{10} = \sum \binom{10}{r}$ and $(1-1)^{10} = \sum (-1)^r\binom{10}{r}$ gives $2\left[\binom{10}{0} + \binom{10}{2} + \cdots + \binom{10}{10}\right] = 2^{10}$, so the sum is $2^9 = 512$.",
  "Not halving the total, or halving it twice.",
  "U05-B-odd-even-binom", "Standard identity, one step.",
  check=lambda: sum(binomial(10, r) for r in range(0, 11, 2)), values=[512, 1024, 256, 511],
  cognitive="Recall", source_class="XI")

q("U05-B-006", T_NUM, "Terms surviving in a difference of expansions", "Easy", "Single-step computation MCQ",
  r"The number of terms in the expansion of $(x + a)^{15} - (x - a)^{15}$, after simplification, is",
  r"$8$",
  [(r"$16$", r"Counts all $n + 1 = 16$ terms of one expansion, ignoring the cancellation."),
   (r"$7$", r"Uses $\frac{n-1}{2} = 7$ for the number of odd powers from $1$ to $15$, missing one of them."),
   (r"$32$", r"Adds the $16$ terms of each expansion without combining anything.")],
  r"In the difference, terms with even powers of $a$ cancel and terms with odd powers double: $2\left[\binom{15}{1}x^{14}a + \binom{15}{3}x^{12}a^3 + \cdots + \binom{15}{15}a^{15}\right]$. The odd powers $1, 3, \ldots, 15$ give $8$ terms.",
  "Forgetting which terms cancel in a difference of conjugate expansions.",
  "U05-B-numterms-conjugate", "One observation about cancellation, then a count.",
  check=lambda: nterms((x + a)**15 - (x - a)**15), values=[8, 16, 7, 32], cognitive="Understanding", source_class="XI")

q("U05-B-007", T_GRT, "Greatest binomial coefficient, odd index", "Easy", "Single-step computation MCQ",
  r"The greatest binomial coefficient in the expansion of $(1 + x)^{9}$ is",
  r"$126$",
  [(r"$84$", r"Uses $r = 3$, taking $\binom{9}{3}$ instead of a middle coefficient."),
   (r"$252$", r"Uses $\binom{10}{5}$, the greatest coefficient for index $10$."),
   (r"$36$", r"Uses $\binom{9}{2}$, the third coefficient.")],
  r"For odd $n = 9$ the greatest binomial coefficients are the two middle ones, $\binom{9}{4} = \binom{9}{5} = 126$.",
  "Using $\\binom{n+1}{(n+1)/2}$ for odd $n$.",
  "U05-B-greatest-binom", "Direct use of the middle-coefficient rule.",
  check=lambda: max(binomial(9, r) for r in range(10)), values=[126, 84, 252, 36],
  cognitive="Recall", source_class="XI")

q("U05-B-008", T_SUM, "Sum of squares of binomial coefficients", "Easy", "Single-step computation MCQ",
  r"The value of $\binom{8}{0}^2 + \binom{8}{1}^2 + \binom{8}{2}^2 + \cdots + \binom{8}{8}^2$ is",
  r"$12870$",
  [(r"$65536$", r"Squares the sum: $\left(2^8\right)^2 = 2^{16}$."),
   (r"$4900$", r"Squares only the largest coefficient, $\binom{8}{4}^2 = 70^2$."),
   (r"$256$", r"Sums the coefficients without squaring, $2^8$.")],
  r"Comparing the coefficient of $x^8$ on both sides of $(1+x)^8(1+x)^8 = (1+x)^{16}$ gives $\sum_{r=0}^{8}\binom{8}{r}\binom{8}{8-r} = \binom{16}{8}$, and since $\binom{8}{8-r} = \binom{8}{r}$, the sum of squares is $\binom{16}{8} = 12870$.",
  "Treating the sum of squares as the square of the sum.",
  "U05-B-sum-squares", "Recall of one identity.",
  check=lambda: sum(binomial(8, r)**2 for r in range(9)), values=[12870, 65536, 4900, 256],
  cognitive="Recall", source_class="XI")

def _c9():
    n = 15
    pos = list(range(1, n + 2))
    m = len(pos)
    return tuple(pos[m // 2 - 1:m // 2 + 1]) if m % 2 == 0 else (pos[m // 2],)
q("U05-B-009", T_MID, "Position of middle terms, odd index", "Easy", "Direct concept MCQ",
  r"In the expansion of $(p + s)^{15}$, the middle term or terms are",
  r"the $8$th and $9$th terms",
  [(r"the $7$th and $8$th terms", r"Uses positions $\frac{n-1}{2}$ and $\frac{n+1}{2}$, one place too early."),
   (r"the $8$th term only", r"Assumes there is a single middle term, at position $\frac{n+1}{2}$, as if the index were even."),
   (r"the $9$th and $10$th terms", r"Uses positions $\frac{n+3}{2}$ and $\frac{n+5}{2}$, one place too late.")],
  r"With $n = 15$ there are $16$ terms, an even number, so there are two middle terms, at positions $\frac{n+1}{2} = 8$ and $\frac{n+3}{2} = 9$.",
  "Counting $n$ terms instead of $n+1$ when locating the middle.",
  "U05-B-middle-position", "One counting fact.",
  check=_c9, values=[(8, 9), (7, 8), (8,), (9, 10)], cognitive="Recall", source_class="XI")

q("U05-B-010", T_SUM, "Index from the sum of coefficients", "Easy", "Inverse/parameter MCQ",
  r"If the sum of the coefficients in the expansion of $(2x + 1)^{n}$ is $729$, then $n$ equals",
  r"$6$",
  [(r"$3$", r"Takes the sum as $(2+1)^{2n}$, squaring the base, so $9^n = 729$."),
   (r"$5$", r"Finds $3^6 = 729$ but then sets the number of terms $n + 1$ equal to $6$."),
   (r"$9$", r"Writes $729 = 9^3$ and reports the base $9$.")],
  r"Putting $x = 1$, the sum of the coefficients is $3^n$. So $3^n = 729 = 3^6$ and $n = 6$.",
  "Using $2^n$ (sum of binomial coefficients) or mixing up base and exponent.",
  "U05-B-sumcoeff-eval", "One substitution and one exponent comparison.",
  check=lambda: solve(Eq((2*1 + 1)**_n, 729), _n)[0], values=[6, 3, 5, 9],
  cognitive="Application", source_class="XI")

def _c11():
    c = [binomial(12, r) for r in range(13)]
    s1 = sum(c[0::2]) == sum(c[1::2])
    ts = gterms(x**2, 1/x, 12)
    mid_pos = len(ts) // 2 + 1
    s2 = mid_pos == 6
    return (bool(s1), bool(s2))
q("U05-B-011", T_SUM, "Odd and even position sums; middle term position", "Easy", "Statement-based MCQ",
  r"Statement I: In the expansion of $(1 + x)^{12}$, the sum of the coefficients of the terms in odd positions ($1$st, $3$rd, $5$th, $\ldots$) equals the sum of the coefficients of the terms in even positions. Statement II: The middle term of the expansion of $\left(x^2 + \frac{1}{x}\right)^{12}$ is its $6$th term." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Verifies Statement I correctly but accepts the $6$th term as the middle term, using $\frac{n}{2}$ instead of $\frac{n}{2} + 1$."),
   (ST_FF, r"Thinks the odd-position sum is larger because it contains one more coefficient ($7$ terms against $6$), so rejects Statement I; finds the middle term correctly as the $7$th and rejects Statement II."),
   (ST_FT, r"Thinks the odd-position sum is larger because it contains one more coefficient ($7$ terms against $6$), so rejects Statement I; and accepts the $6$th term as the middle term using $\frac{n}{2}$.")],
  r"Statement I: putting $x = -1$ in $(1+x)^{12}$ gives $\sum(-1)^r\binom{12}{r} = 0$, so both sums are equal (each is $2^{11}$); true. Statement II: there are $13$ terms, so the middle term is the $\frac{12}{2} + 1 = 7$th term, not the $6$th; false.",
  "Locating the middle term at position $\\frac{n}{2}$.",
  "U05-B-statement-basic", "Two independent one-step checks.",
  check=_c11, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Understanding", source_class="XI")

q("U05-B-012", T_NUM, "Number of terms after recognising a perfect square", "Easy", "Single-step computation MCQ",
  r"The number of terms in the expansion of $(1 + 2x + x^2)^{8}$, after simplification, is",
  r"$17$",
  [(r"$9$", r"Uses $n + 1$ with $n = 8$ without noticing that $1 + 2x + x^2 = (1+x)^2$."),
   (r"$45$", r"Uses the trinomial count $\binom{n+2}{2} = \binom{10}{2}$, forgetting that terms with equal powers of $x$ combine."),
   (r"$16$", r"Finds the degree $16$ and takes it as the number of terms, missing the constant term.")],
  r"Since $1 + 2x + x^2 = (1+x)^2$, the expression is $(1 + x)^{16}$, which has $16 + 1 = 17$ terms.",
  "Counting terms of a trinomial power without combining like terms.",
  "U05-B-numterms-basic", "One recognition step, then $n + 1$.",
  check=lambda: nterms((1 + 2*x + x**2)**8), values=[17, 9, 45, 16], cognitive="Application", source_class="XI",
  numerical=dict(question=r"The number of terms in the expansion of $(1 + 2x + x^2)^{8}$, after simplification, is", answer=17))

q("U05-B-013", T_MID, "Single middle term with negative powers", "Easy", "Single-step computation MCQ",
  r"The middle term in the expansion of $\left(x^2 - \frac{2}{x}\right)^{8}$ is",
  r"$1120x^4$",
  [(r"$-1120x^4$", r"Treats $\left(-\frac{2}{x}\right)^4$ as negative."),
   (r"$-448x^7$", r"Takes $T_4 = \binom{8}{3}(x^2)^5\left(-\frac{2}{x}\right)^3$, using $\frac{n}{2}$ as the term number."),
   (r"$70x^4$", r"Uses $\binom{8}{4} = 70$ and $(x^2)^4\left(\frac{1}{x}\right)^4 = x^4$ but drops the factor $(-2)^4 = 16$ from $\left(-\frac{2}{x}\right)^4$.")],
  r"There are $9$ terms, so the middle term is $T_5 = \binom{8}{4}(x^2)^4\left(-\frac{2}{x}\right)^4 = 70 \cdot x^8 \cdot \frac{16}{x^4} = 1120x^4$.",
  "Mislocating the middle term or mishandling the sign of an even power.",
  "U05-B-middle-single", "One general term evaluated.",
  check=lambda: middles(x**2, -2/x, 8)[0], values=[1120*x**4, -1120*x**4, -448*x**7, 70*x**4],
  cognitive="Application", source_class="XI")

q("U05-B-014", T_SUM, "Alternating sum of coefficients", "Easy", "Single-step computation MCQ",
  r"If $(2x - 3)^5 = a_0 + a_1x + a_2x^2 + \cdots + a_5x^5$, then $a_0 - a_1 + a_2 - a_3 + a_4 - a_5$ equals",
  r"$-3125$",
  [(r"$3125$", r"Evaluates $(2 + 3)^5$ instead of $(-2 - 3)^5$, losing the sign."),
   (r"$-1$", r"Puts $x = 1$, which gives the plain sum $(2-3)^5$."),
   (r"$-243$", r"Gives only the constant term $a_0 = (-3)^5$.")],
  r"The alternating sum is the value at $x = -1$: $(2(-1) - 3)^5 = (-5)^5 = -3125$.",
  "Substituting $x = 1$ when the alternating sum needs $x = -1$.",
  "U05-B-alternating-eval", "One substitution.",
  check=lambda: sum((-1)**i * c for i, c in enumerate(coeffs((2*x - 3)**5))), values=[-3125, 3125, -1, -243],
  cognitive="Application", source_class="XI")

# ================================================================ MEDIUM (21)

q("U05-B-015", T_SUM, "Sum of r times binomial coefficient", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{10}{1} + 2\binom{10}{2} + 3\binom{10}{3} + \cdots + 10\binom{10}{10}$ is",
  r"$5120$",
  [(r"$10240$", r"Uses $n \cdot 2^{n}$, not reducing the index of the remaining sum to $n - 1$."),
   (r"$4608$", r"Uses $(n-1)2^{n-1} = 9 \cdot 512$, taking the factor pulled out as $n - 1$."),
   (r"$1024$", r"Ignores the weights $r$ and sums the coefficients, $2^{10}$.")],
  r"Since $r\binom{n}{r} = n\binom{n-1}{r-1}$, the sum is $10\sum_{r=1}^{10}\binom{9}{r-1} = 10 \cdot 2^9 = 5120$.",
  "Not reducing the index after using $r\\binom{n}{r} = n\\binom{n-1}{r-1}$.",
  "U05-B-rCr", "One identity transformation plus a known sum.",
  check=lambda: sum(r*binomial(10, r) for r in range(11)), values=[5120, 10240, 4608, 1024],
  cognitive="Application", source_class="XI",
  numerical=dict(question=r"The value of $\binom{10}{1} + 2\binom{10}{2} + 3\binom{10}{3} + \cdots + 10\binom{10}{10}$ is", answer=5120))

q("U05-B-016", T_SUM, "Sum of coefficients of odd powers", "Medium", "Multi-step computation MCQ",
  r"The sum of the coefficients of the odd powers of $x$ in the expansion of $(1 - 2x)^{9}$ is",
  r"$-9842$",
  [(r"$9841$", r"Computes $\frac{f(1) + f(-1)}{2}$, which is the sum for even powers."),
   (r"$9842$", r"Computes $\frac{f(-1) - f(1)}{2}$, reversing the order of subtraction."),
   (r"$-19684$", r"Computes $f(1) - f(-1)$ but does not divide by $2$.")],
  r"Let $f(x) = (1 - 2x)^9$. Then $f(1) = -1$ and $f(-1) = 3^9 = 19683$. The odd-power sum is $\frac{f(1) - f(-1)}{2} = \frac{-1 - 19683}{2} = -9842$.",
  "Swapping the roles of $f(1) + f(-1)$ and $f(1) - f(-1)$, or not halving.",
  "U05-B-odd-even-sum", "Two evaluations combined with the right sign, then halved.",
  check=lambda: sum(c for i, c in enumerate(coeffs((1 - 2*x)**9)) if i % 2 == 1),
  values=[-9842, 9841, 9842, -19684], cognitive="Application", source_class="XI")

q("U05-B-017", T_SUM, "Sum of products of adjacent coefficients", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{10}{0}\binom{10}{1} + \binom{10}{1}\binom{10}{2} + \binom{10}{2}\binom{10}{3} + \cdots + \binom{10}{9}\binom{10}{10}$ is",
  r"$\binom{20}{9}$",
  [(r"$\binom{20}{10}$", r"Treats the sum as the sum of squares $\sum\binom{10}{r}^2$."),
   (r"$\binom{20}{8}$", r"Matches the exponents with an offset of $2$ instead of $1$, reading off the coefficient of $x^{8}$."),
   (r"$\binom{19}{9}$", r"Takes the sum to be half the sum of squares, $\frac{1}{2}\binom{20}{10}$, which equals $\binom{19}{9}$.")],
  r"Write $(1+x)^{10} = \sum \binom{10}{r}x^r$ and $(x+1)^{10} = \sum \binom{10}{s}x^{10-s}$. In the product $(1+x)^{20}$, the coefficient of $x^{9}$ collects $\binom{10}{r}\binom{10}{s}$ with $r + 10 - s = 9$, i.e. $s = r + 1$. Hence the sum is $\binom{20}{9}$.",
  "Not tracking the offset between the indices when comparing coefficients.",
  "U05-B-coeff-compare", "Set up a product and match the exponent with an offset.",
  check=lambda: sum(binomial(10, r)*binomial(10, r + 1) for r in range(10)),
  values=[binomial(20, 9), binomial(20, 10), binomial(20, 8), binomial(19, 9)],
  cognitive="Application", source_class="XI")

def _c18():
    return [n for n in range(1, 40) if max(binomial(n, r) for r in range(n + 1)) == 252][0]
q("U05-B-018", T_GRT, "Index from the greatest binomial coefficient", "Medium", "Inverse/parameter MCQ",
  r"If the greatest binomial coefficient in the expansion of $(1 + x)^{n}$ is $252$, then $n$ equals",
  r"$10$",
  [(r"$9$", r"Adds the two equal middle coefficients of $(1+x)^9$, $126 + 126 = 252$, and takes that as the greatest coefficient."),
   (r"$5$", r"Finds $\binom{10}{5} = 252$ but reports $r = 5$ instead of $n$."),
   (r"$6$", r"Finds $n = 10$ but reports the position $\frac{n}{2} + 1 = 6$ of the middle term.")],
  r"The greatest binomial coefficient is the middle one. Testing: $\binom{8}{4} = 70$, $\binom{9}{4} = 126$, $\binom{10}{5} = 252$, $\binom{11}{5} = 462$. Since these increase with $n$, only $n = 10$ works.",
  "Confusing $n$ with $r$ or with the position of the middle term.",
  "U05-B-greatest-binom", "Reverse use of the middle-coefficient rule with a monotonicity check.",
  check=_c18, values=[10, 9, 5, 6], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If the greatest binomial coefficient in the expansion of $(1 + x)^{n}$ is $252$, then $n$ is", answer=10))

q("U05-B-019", T_GRT, "Greatest coefficient with a numerical factor", "Medium", "Multi-step computation MCQ",
  r"The greatest coefficient in the expansion of $(1 + 2x)^{10}$ is",
  r"$15360$",
  [(r"$8064$", r"Takes the middle term $\binom{10}{5}2^5$, as if the greatest binomial coefficient gave the greatest coefficient."),
   (r"$13440$", r"Writes the ratio as $\frac{2(10 - r)}{r}$, so $r \le \frac{20}{3}$ and $r = 6$, giving $\binom{10}{6}2^6$."),
   (r"$11520$", r"Writes the ratio as $\frac{2(12 - r)}{r}$, so $r \le 8$, giving $\binom{10}{8}2^8$.")],
  r"Let $c_r = \binom{10}{r}2^r$. Then $\frac{c_{r}}{c_{r-1}} = \frac{2(11 - r)}{r} \ge 1$ iff $r \le \frac{22}{3}$, so $c_r$ increases up to $r = 7$ and then decreases. The greatest coefficient is $c_7 = 120 \cdot 128 = 15360$.",
  "Assuming the greatest coefficient sits at the middle term even when the terms carry unequal numerical factors.",
  "U05-B-greatest-coeff", "Ratio test of consecutive coefficients, then evaluation.",
  check=lambda: max(coeffs((1 + 2*x)**10)), values=[15360, 8064, 13440, 11520],
  cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The greatest coefficient in the expansion of $(1 + 2x)^{10}$ is", answer=15360))

q("U05-B-020", T_NUM, "Terms in a sum of conjugate surd expansions", "Medium", "Multi-step computation MCQ",
  r"The number of terms in the expansion of $\left(x + \sqrt{x^2 - 1}\right)^{7} + \left(x - \sqrt{x^2 - 1}\right)^{7}$, written as a polynomial in $x$ after simplification, is",
  r"$4$",
  [(r"$8$", r"Counts the $n + 1 = 8$ terms of a single binomial expansion."),
   (r"$10$", r"Expands each surviving $(x^2-1)^k$ but does not combine like powers of $x$, counting $1 + 2 + 3 + 4$ terms."),
   (r"$5$", r"Uses $\frac{n+1}{2} + 1$ for $n = 7$, adding one term too many.")],
  r"The odd powers of $\sqrt{x^2-1}$ cancel, leaving $2\left[x^7 + \binom{7}{2}x^5(x^2-1) + \binom{7}{4}x^3(x^2-1)^2 + \binom{7}{6}x(x^2-1)^3\right]$. Every piece is an odd polynomial of degree at most $7$, so only $x^7, x^5, x^3, x$ can appear; collecting gives $128x^7 - 224x^5 + 112x^3 - 14x$, which has $4$ terms.",
  "Counting terms before combining like powers.",
  "U05-B-numterms-conjugate", "Cancellation plus collecting like powers.",
  check=lambda: nterms((x + sqrt(x**2 - 1))**7 + (x - sqrt(x**2 - 1))**7), values=[4, 8, 10, 5],
  cognitive="Analysis", source_class="XI")

q("U05-B-021", T_NUM, "Terms in a product of expansions", "Medium", "Multi-step computation MCQ",
  r"The number of terms in the expansion of $(1 + x)^{10}(1 - x)^{10}$, after simplification, is",
  r"$11$",
  [(r"$21$", r"Takes the degree $20$ and assumes every power from $x^0$ to $x^{20}$ appears."),
   (r"$22$", r"Adds the $11$ terms of each factor."),
   (r"$10$", r"Finds $(1 - x^2)^{10}$ but counts $n$ instead of $n + 1$ terms.")],
  r"$(1 + x)^{10}(1 - x)^{10} = (1 - x^2)^{10}$, which has $10 + 1 = 11$ terms (powers $x^0, x^2, \ldots, x^{20}$).",
  "Assuming all powers up to the degree occur.",
  "U05-B-numterms-product", "Combine factors, then count.",
  check=lambda: nterms((1 + x)**10*(1 - x)**10), values=[11, 21, 22, 10],
  cognitive="Application", source_class="XI")

q("U05-B-022", T_SUM, "Weighted sum with weights r + 1", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{8}{0} + 2\binom{8}{1} + 3\binom{8}{2} + \cdots + 9\binom{8}{8}$ is",
  r"$1280$",
  [(r"$2304$", r"Uses $(n+1)2^n$, as if every coefficient carried the weight $n+1$."),
   (r"$1024$", r"Finds only $\sum r\binom{8}{r} = 8 \cdot 2^7$ and forgets the $\sum\binom{8}{r}$ part."),
   (r"$1152$", r"Uses $(n+1)2^{n-1}$, applying the $r\binom{n}{r}$ formula with weight $n+1$.")],
  r"Write the sum as $\sum (r + 1)\binom{8}{r} = \sum r\binom{8}{r} + \sum\binom{8}{r} = 8 \cdot 2^7 + 2^8 = 1024 + 256 = 1280$.",
  "Not splitting the weight $r+1$ into two standard sums.",
  "U05-B-weighted-sum", "Split into two identities and add.",
  check=lambda: sum((r + 1)*binomial(8, r) for r in range(9)), values=[1280, 2304, 1024, 1152],
  cognitive="Application", source_class="XI",
  numerical=dict(question=r"The value of $\binom{8}{0} + 2\binom{8}{1} + 3\binom{8}{2} + \cdots + 9\binom{8}{8}$ is", answer=1280))

q("U05-B-023", T_SUM, "Sum of binomial coefficients divided by r + 1", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{9}{0} + \frac{1}{2}\binom{9}{1} + \frac{1}{3}\binom{9}{2} + \cdots + \frac{1}{10}\binom{9}{9}$ is",
  r"$\frac{1023}{10}$",
  [(r"$\frac{512}{5}$", r"Uses $\frac{2^{10}}{10}$, forgetting to subtract the missing $\binom{10}{0}$."),
   (r"$\frac{1023}{9}$", r"Divides by $n = 9$ instead of $n + 1 = 10$."),
   (r"$\frac{511}{5}$", r"Subtracts both $\binom{10}{0}$ and $\binom{10}{10}$ from $2^{10}$, getting $\frac{1022}{10}$.")],
  r"Since $\frac{1}{r+1}\binom{9}{r} = \frac{1}{10}\binom{10}{r+1}$, the sum is $\frac{1}{10}\left[\binom{10}{1} + \cdots + \binom{10}{10}\right] = \frac{2^{10} - 1}{10} = \frac{1023}{10}$.",
  "Forgetting the term $\\binom{n+1}{0}$ that is missing from the shifted sum.",
  "U05-B-Cr-over-r1", "Identity rewrite with an index shift.",
  check=lambda: sum(Rational(1, r + 1)*binomial(9, r) for r in range(10)),
  values=[Rational(1023, 10), Rational(512, 5), Rational(1023, 9), Rational(511, 5)],
  cognitive="Application", source_class="XI")

def _c24():
    m = middles(Integer(3), -x**3/6, 7)
    return tuple(t.coeff(x, k) for t, k in zip(m, (9, 12)))
q("U05-B-024", T_MID, "Two middle terms, odd index", "Medium", "Multi-step computation MCQ",
  r"In the expansion of $\left(3 - \frac{x^3}{6}\right)^{7}$, the coefficients of the two middle terms, taken in increasing powers of $x$, are",
  r"$-\frac{105}{8}$ and $\frac{35}{48}$",
  [(r"$\frac{105}{8}$ and $\frac{35}{48}$", r"Treats $\left(-\frac{1}{6}\right)^3$ as positive."),
   (r"$-\frac{105}{8}$ and $-\frac{35}{48}$", r"Attaches the minus sign to every term after the first instead of only to odd powers."),
   (r"$\frac{567}{4}$ and $-\frac{105}{8}$", r"Takes $T_3$ and $T_4$ as the middle terms, using positions $\frac{n}{2}$ rounded down.")],
  r"With $8$ terms, the middle terms are $T_4$ and $T_5$. $T_4 = \binom{7}{3}3^4\left(-\frac{x^3}{6}\right)^3 = 35 \cdot 81 \cdot \left(-\frac{1}{216}\right)x^9 = -\frac{105}{8}x^9$ and $T_5 = \binom{7}{4}3^3\left(-\frac{x^3}{6}\right)^4 = 35 \cdot 27 \cdot \frac{1}{1296}x^{12} = \frac{35}{48}x^{12}$.",
  "Sign errors on odd powers and wrong positions for the two middle terms.",
  "U05-B-middle-two", "Two general terms with fractional factors and signs.",
  check=_c24,
  values=[(Rational(-105, 8), Rational(35, 48)), (Rational(105, 8), Rational(35, 48)),
          (Rational(-105, 8), Rational(-35, 48)), (Rational(567, 4), Rational(-105, 8))],
  cognitive="Application", source_class="XI")

def _c25():
    ap = symbols('ap', positive=True)
    mid = middles(1, ap*x, 8)[0]
    return solve(Eq(mid.coeff(x, 4), 1120), ap)[0]
q("U05-B-025", T_MID, "Parameter from the middle term", "Medium", "Inverse/parameter MCQ",
  r"If the middle term in the expansion of $(1 + ax)^{8}$ is $1120x^4$, where $a > 0$, then $a$ equals",
  r"$2$",
  [(r"$4$", r"Solves correctly for $a^4 = 16$ but stops at $a^2 = 4$."),
   (r"$16$", r"Reports $a^4 = 16$ as the value of $a$."),
   (r"$\sqrt{2}$", r"Raises $a$ to the power $8$ instead of $4$, solving $a^8 = 16$.")],
  r"There are $9$ terms, so the middle term is $T_5 = \binom{8}{4}(ax)^4 = 70a^4x^4$. Then $70a^4 = 1120$ gives $a^4 = 16$, and since $a > 0$, $a = 2$.",
  "Stopping before the fourth root, or using the wrong power of $a$.",
  "U05-B-middle-param", "Middle term, then solve a power equation.",
  check=_c25, values=[2, 4, 16, sqrt(2)], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If the middle term in the expansion of $(1 + ax)^{8}$ is $1120x^4$, where $a > 0$, then $a$ is", answer=2))

def _c26():
    n = solve(Eq(expand(3*1**2 - 1/Integer(1))**_n, 64), _n)[0]
    return middles(3*x**2, -1/x, int(n))[0]
q("U05-B-026", T_MID, "Middle term after finding the index", "Medium", "Multi-step computation MCQ",
  r"If the sum of the coefficients in the expansion of $\left(3x^2 - \frac{1}{x}\right)^{n}$ is $64$, then the middle term of the expansion is",
  r"$-540x^3$",
  [(r"$540x^3$", r"Treats $\left(-\frac{1}{x}\right)^3$ as positive."),
   (r"$1215x^6$", r"Takes $T_3 = \binom{6}{2}(3x^2)^4\left(-\frac{1}{x}\right)^2$, one place before the middle."),
   (r"$-60x^3$", r"Does not raise the $3$ to the third power, using $\binom{6}{3} \cdot 3 \cdot (-1)$.")],
  r"Putting $x = 1$, the sum of coefficients is $(3 - 1)^n = 2^n = 64$, so $n = 6$. With $7$ terms the middle term is $T_4 = \binom{6}{3}(3x^2)^3\left(-\frac{1}{x}\right)^3 = 20 \cdot 27x^6 \cdot \left(-\frac{1}{x^3}\right) = -540x^3$.",
  "Losing the sign on the odd power or the numerical factor on the power.",
  "U05-B-middle-param", "Sum of coefficients gives $n$, then a middle term.",
  check=_c26, values=[-540*x**3, 540*x**3, 1215*x**6, -60*x**3], cognitive="Application", source_class="XI")

q("U05-B-027", T_SUM, "Sum of coefficients of even powers", "Medium", "Multi-step computation MCQ",
  r"If $(1 + 2x)^{8} = a_0 + a_1x + a_2x^2 + \cdots + a_8x^8$, then $a_0 + a_2 + a_4 + a_6 + a_8$ equals",
  r"$3281$",
  [(r"$3280$", r"Computes $\frac{f(1) - f(-1)}{2}$, the odd-power sum."),
   (r"$6562$", r"Computes $f(1) + f(-1) = 3^8 + 1$ without halving."),
   (r"$128$", r"Uses half the sum of the binomial coefficients, $2^7$, ignoring the factor $2$ in $2x$.")],
  r"With $f(x) = (1+2x)^8$, $f(1) = 3^8 = 6561$ and $f(-1) = 1$. The even-power sum is $\frac{f(1) + f(-1)}{2} = \frac{6562}{2} = 3281$.",
  "Ignoring numerical factors and using only $2^{n-1}$.",
  "U05-B-odd-even-sum", "Two evaluations, combined and halved.",
  check=lambda: sum(c for i, c in enumerate(coeffs((1 + 2*x)**8)) if i % 2 == 0),
  values=[3281, 3280, 6562, 128], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If $(1 + 2x)^{8} = a_0 + a_1x + a_2x^2 + \cdots + a_8x^8$, then the value of $a_0 + a_2 + a_4 + a_6 + a_8$ is", answer=3281))

q("U05-B-028", T_SUM, "Products of coefficients two apart", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{8}{0}\binom{8}{2} + \binom{8}{1}\binom{8}{3} + \binom{8}{2}\binom{8}{4} + \cdots + \binom{8}{6}\binom{8}{8}$ is",
  r"$\binom{16}{6}$",
  [(r"$\binom{16}{8}$", r"Treats the sum as the sum of squares $\sum\binom{8}{r}^2$."),
   (r"$\binom{16}{7}$", r"Uses an offset of $1$, as for adjacent products."),
   (r"$\binom{16}{4}$", r"Applies the offset of $2$ twice, reading off the coefficient of $x^{8-4}$.")],
  r"In $(1+x)^8(x+1)^8 = (1+x)^{16}$, write the first factor as $\sum\binom{8}{r}x^r$ and the second as $\sum\binom{8}{s}x^{8-s}$. The coefficient of $x^6$ collects $r + 8 - s = 6$, i.e. $s = r + 2$, which is exactly the given sum. So it equals $\binom{16}{6}$.",
  "Mismatching the offset when comparing coefficients.",
  "U05-B-coeff-compare", "Choose the right product and the right power.",
  check=lambda: sum(binomial(8, r)*binomial(8, r + 2) for r in range(7)),
  values=[binomial(16, 6), binomial(16, 8), binomial(16, 7), binomial(16, 4)],
  cognitive="Application", source_class="XI")

def _c29():
    return [n for n in range(1, 30) if sum(binomial(2*n + 1, r) for r in range(n + 1)) == 256][0]
q("U05-B-029", T_SUM, "Index from a half sum of coefficients", "Medium", "Inverse/parameter MCQ",
  r"If $\binom{2n+1}{0} + \binom{2n+1}{1} + \binom{2n+1}{2} + \cdots + \binom{2n+1}{n} = 256$, then $n$ equals",
  r"$4$",
  [(r"$8$", r"Takes the half sum to be $2^{n}$ and solves $2^n = 256$."),
   (r"$9$", r"Finds $n = 4$ but reports the index $2n + 1 = 9$."),
   (r"$3$", r"Writes the half sum as $2^{2n+2}$ instead of $2^{2n}$, so $2n + 2 = 8$.")],
  r"Since $\binom{2n+1}{r} = \binom{2n+1}{2n+1-r}$, the coefficients for $r = 0, \ldots, n$ and $r = n+1, \ldots, 2n+1$ have equal sums, each $\frac{2^{2n+1}}{2} = 2^{2n}$. So $2^{2n} = 256 = 2^8$ and $n = 4$.",
  "Not using the symmetry to see that the half sum is exactly $2^{2n}$.",
  "U05-B-half-sum", "Symmetry argument plus an exponent equation.",
  check=_c29, values=[4, 8, 9, 3], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If $\binom{2n+1}{0} + \binom{2n+1}{1} + \binom{2n+1}{2} + \cdots + \binom{2n+1}{n} = 256$, then $n$ is", answer=4))

def _c30():
    out = []
    for n in range(1, 11):
        g1 = max(binomial(2*n, r) for r in range(2*n + 1))
        g2 = max(binomial(2*n - 1, r) for r in range(2*n))
        out.append(Rational(g1, g2))
    return tuple(out)
q("U05-B-030", T_GRT, "Ratio of greatest coefficients", "Medium", "Multi-step computation MCQ",
  r"For every positive integer $n$, the ratio of the greatest binomial coefficient in the expansion of $(1 + x)^{2n}$ to the greatest binomial coefficient in the expansion of $(1 + x)^{2n-1}$ is",
  r"$2$",
  [(r"$\frac{1}{2}$", r"Inverts the ratio, dividing the greatest coefficient of $(1+x)^{2n-1}$ by that of $(1+x)^{2n}$."),
   (r"$\frac{2n+1}{n+1}$", r"Uses the indices $2n + 1$ and $2n$, one more than given in both expansions, getting $\binom{2n+1}{n} \div \binom{2n}{n} = \frac{2n+1}{n+1}$."),
   (r"$\frac{2n-1}{n}$", r"Uses the indices $2n - 1$ and $2n - 2$, one less than given in both expansions, getting $\binom{2n-1}{n-1} \div \binom{2n-2}{n-1} = \frac{2n-1}{n}$.")],
  r"The greatest coefficients are $\binom{2n}{n}$ and $\binom{2n-1}{n-1}$. Their ratio is $\frac{(2n)!}{n!\,n!} \cdot \frac{(n-1)!\,n!}{(2n-1)!} = \frac{2n}{n} = 2$.",
  "Factorial slips when cancelling.",
  "U05-B-greatest-binom", "Identify both greatest coefficients and simplify factorials.",
  check=_c30,
  values=[tuple(Integer(2) for n in range(1, 11)), tuple(Rational(1, 2) for n in range(1, 11)),
          tuple(Rational(2*n + 1, n + 1) for n in range(1, 11)), tuple(Rational(2*n - 1, n) for n in range(1, 11))],
  cognitive="Understanding", source_class="XI")

q("U05-B-031", T_SUM, "Vandermonde-type coefficient comparison", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{10}{0}\binom{5}{5} + \binom{10}{1}\binom{5}{4} + \binom{10}{2}\binom{5}{3} + \binom{10}{3}\binom{5}{2} + \binom{10}{4}\binom{5}{1} + \binom{10}{5}\binom{5}{0}$ is",
  r"$\binom{15}{5}$",
  [(r"$\binom{15}{6}$", r"Counts the number of products (six) and reads off the coefficient of $x^6$."),
   (r"$\binom{10}{5}$", r"Keeps only the last product $\binom{10}{5}\binom{5}{0}$, thinking the others are small."),
   (r"$\binom{15}{7}$", r"Takes the greatest coefficient of $(1+x)^{15}$.")],
  r"Each product $\binom{10}{r}\binom{5}{5-r}$ is a way of getting $x^5$ from $(1+x)^{10}(1+x)^5$, taking $x^r$ from the first factor and $x^{5-r}$ from the second. So the sum is the coefficient of $x^5$ in $(1+x)^{15}$, namely $\binom{15}{5} = 3003$.",
  "Not recognising the sum as a single coefficient in a product.",
  "U05-B-vandermonde", "Interpret the sum as coefficient extraction in a product.",
  check=lambda: sum(binomial(10, r)*binomial(5, 5 - r) for r in range(6)),
  values=[binomial(15, 5), binomial(15, 6), binomial(10, 5), binomial(15, 7)],
  cognitive="Application", source_class="XI")

def _c32():
    n = [n for n in range(1, 30) if sum(binomial(n, r)**2 for r in range(n + 1)) == 924][0]
    return max(binomial(n, r) for r in range(n + 1))
q("U05-B-032", T_GRT, "Greatest coefficient after finding the index", "Medium", "Multi-step computation MCQ",
  r"If $\binom{n}{0}^2 + \binom{n}{1}^2 + \cdots + \binom{n}{n}^2 = 924$, then the greatest binomial coefficient in the expansion of $(1 + x)^{n}$ is",
  r"$20$",
  [(r"$924$", r"Takes $\binom{2n}{n} = 924$ itself as the answer without finding $n$."),
   (r"$462$", r"Takes the greatest coefficient as half the sum of squares, $\frac{924}{2}$."),
   (r"$15$", r"Finds $n = 6$ but uses $\binom{6}{2}$ instead of the middle coefficient $\binom{6}{3}$.")],
  r"The sum of squares is $\binom{2n}{n}$. Since $\binom{12}{6} = 924$ (and $\binom{2n}{n}$ increases with $n$), $n = 6$. The greatest binomial coefficient of $(1+x)^6$ is $\binom{6}{3} = 20$.",
  "Stopping at the value of the sum of squares instead of finding $n$.",
  "U05-B-sum-squares", "Two identities chained: sum of squares then middle coefficient.",
  check=_c32, values=[20, 924, 462, 15], cognitive="Application", source_class="XI")

q("U05-B-033", T_NUM, "Distinct terms in a sum of two expansions", "Medium", "Multi-step computation MCQ",
  r"The number of distinct terms in the expansion of $(1 + x)^{10} + (1 - x^2)^{10}$, after simplification, is",
  r"$16$",
  [(r"$21$", r"Takes the degree $20$ and assumes every power from $x^0$ to $x^{20}$ appears."),
   (r"$22$", r"Adds the $11$ terms of each expansion without combining equal powers."),
   (r"$11$", r"Counts only the terms of one expansion, as if the other merely changed coefficients.")],
  r"$(1+x)^{10}$ contributes $x^0, x^1, \ldots, x^{10}$ and $(1-x^2)^{10}$ contributes $x^0, x^2, \ldots, x^{20}$. The new powers from the second are $x^{12}, x^{14}, \ldots, x^{20}$, i.e. $5$ of them. No common power cancels: for $x^{2k}$ with $k \le 5$ the coefficient is $\binom{10}{2k} + (-1)^k\binom{10}{k}$, which is $2, 35, 255, 90, 255, -251$ for $k = 0, \ldots, 5$. So there are $11 + 5 = 16$ terms.",
  "Forgetting that overlapping powers combine, or assuming all powers up to the degree occur.",
  "U05-B-numterms-sum", "Union of exponent sets plus a cancellation check.",
  check=lambda: nterms((1 + x)**10 + (1 - x**2)**10), values=[16, 21, 22, 11],
  cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The number of distinct terms in the expansion of $(1 + x)^{10} + (1 - x^2)^{10}$, after simplification, is", answer=16))

q("U05-B-034", T_SUM, "Alternating sum of coefficients divided by r + 1", "Medium", "Multi-step computation MCQ",
  r"The value of $\binom{9}{0} - \frac{1}{2}\binom{9}{1} + \frac{1}{3}\binom{9}{2} - \cdots - \frac{1}{10}\binom{9}{9}$ is",
  r"$\frac{1}{10}$",
  [(r"$\frac{1}{9}$", r"Divides by $n = 9$ instead of $n + 1 = 10$."),
   (r"$-\frac{1}{10}$", r"Writes the sum as $\frac{(1-1)^{10} - 1}{10}$, reversing the sign."),
   (r"$0$", r"Assumes every alternating sum of binomial coefficients vanishes.")],
  r"Using $\frac{1}{r+1}\binom{9}{r} = \frac{1}{10}\binom{10}{r+1}$, the sum is $\frac{1}{10}\sum_{r=0}^{9}(-1)^r\binom{10}{r+1} = -\frac{1}{10}\sum_{s=1}^{10}(-1)^s\binom{10}{s} = -\frac{1}{10}\left[(1-1)^{10} - 1\right] = \frac{1}{10}$.",
  "Assuming the alternating sum is zero without accounting for the missing first term.",
  "U05-B-Cr-over-r1", "Identity rewrite, index shift and a sign check.",
  check=lambda: sum((-1)**r*Rational(1, r + 1)*binomial(9, r) for r in range(10)),
  values=[Rational(1, 10), Rational(1, 9), Rational(-1, 10), 0], cognitive="Application", source_class="XI")

def _c35():
    s1 = sum(binomial(5, r)**2 for r in range(6)) == 252
    s2 = sum(binomial(9, r) for r in range(0, 10, 2)) == sum(binomial(9, r) for r in range(1, 10, 2))
    return (bool(s1), bool(s2))
q("U05-B-035", T_SUM, "Sum of squares and odd/even sums", "Medium", "Statement-based MCQ",
  r"Statement I: $\binom{5}{0}^2 + \binom{5}{1}^2 + \binom{5}{2}^2 + \binom{5}{3}^2 + \binom{5}{4}^2 + \binom{5}{5}^2 = 252$. Statement II: $\binom{9}{0} + \binom{9}{2} + \binom{9}{4} + \binom{9}{6} + \binom{9}{8} = \binom{9}{1} + \binom{9}{3} + \binom{9}{5} + \binom{9}{7} + \binom{9}{9}$." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Thinks the even-index sum must exceed the odd-index sum because it starts with $\binom{9}{0}$, rejecting Statement II."),
   (ST_FT, r"Takes the sum of squares as $\left(2^5\right)^2 = 1024$, rejecting Statement I."),
   (ST_FF, r"Takes the sum of squares as $\left(2^5\right)^2 = 1024$ and thinks the even-index sum exceeds the odd-index sum because it starts with $\binom{9}{0}$, rejecting both statements.")],
  r"Statement I: the sum of squares is $\binom{10}{5} = 252$; true. Statement II: $(1-1)^9 = 0$ gives that the even-index and odd-index sums are equal (each $2^8 = 256$); true.",
  "Treating a sum of squares as a square of a sum.",
  "U05-B-statement-identities", "Two identity checks.",
  check=_c35, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Understanding", source_class="XI")

# ================================================================ DIFFICULT (12)

q("U05-B-036", T_SUM, "Weighted sum of squares of coefficients", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sum_{r=1}^{5} r\binom{5}{r}^2$ is",
  r"$630$",
  [(r"$1260$", r"Uses $n\binom{2n}{n} = 5 \cdot 252$, not reducing to $\binom{2n-1}{n-1}$."),
   (r"$252$", r"Ignores the weight $r$ and gives $\sum\binom{5}{r}^2 = \binom{10}{5}$."),
   (r"$80$", r"Drops the squares and computes $\sum r\binom{5}{r} = 5 \cdot 2^4$.")],
  r"Write $r\binom{5}{r}^2 = 5\binom{4}{r-1}\binom{5}{r} = 5\binom{4}{r-1}\binom{5}{5-r}$. Summing over $r$ gives $5$ times the coefficient of $x^{4}$ in $(1+x)^4(1+x)^5 = (1+x)^9$, i.e. $5\binom{9}{4} = 5 \cdot 126 = 630$.",
  "Not reducing one factor before comparing coefficients.",
  "U05-B-r-squares-weighted", "Identity reduction combined with coefficient comparison in a product.",
  check=lambda: sum(r*binomial(5, r)**2 for r in range(1, 6)), values=[630, 1260, 252, 80],
  cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The value of $\sum_{r=1}^{5} r\binom{5}{r}^2$ is", answer=630))

q("U05-B-037", T_SUM, "Sum of r squared times binomial coefficient", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sum_{r=1}^{6} r^2\binom{6}{r}$ is",
  r"$672$",
  [(r"$1152$", r"Pulls out $r^2$ as $n^2$, getting $n^2 2^{n-1} = 36 \cdot 32$."),
   (r"$192$", r"Treats $r^2$ as $r$, computing $n2^{n-1}$."),
   (r"$480$", r"Computes only the $r(r-1)$ part, $n(n-1)2^{n-2}$, and forgets to add $\sum r\binom{6}{r}$.")],
  r"Write $r^2 = r(r-1) + r$. Then $\sum r(r-1)\binom{6}{r} = 6 \cdot 5 \cdot 2^4 = 480$ and $\sum r\binom{6}{r} = 6 \cdot 2^5 = 192$, so the total is $480 + 192 = 672$.",
  "Not splitting $r^2$ into $r(r-1) + r$.",
  "U05-B-rCr", "Split weight, apply two identities, add.",
  check=lambda: sum(r**2*binomial(6, r) for r in range(1, 7)), values=[672, 1152, 192, 480],
  cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The value of $\sum_{r=1}^{6} r^2\binom{6}{r}$ is", answer=672))

q("U05-B-038", T_SUM, "Alternating sum of every second coefficient", "Difficult", "Multi-step computation MCQ",
  r"The value of $\binom{20}{0} - \binom{20}{2} + \binom{20}{4} - \binom{20}{6} + \cdots + \binom{20}{20}$ is",
  r"$-2^{10}$",
  [(r"$2^{10}$", r"Gets $(1+i)^{20} = (2i)^{10} = 2^{10}i^{10}$ correctly but takes $i^{10} = 1$, losing the sign."),
   (r"$0$", r"Assumes every alternating sum of binomial coefficients is zero, as for $\sum(-1)^r\binom{20}{r}$."),
   (r"$2^{19}$", r"Ignores the alternating signs and gives the even-index sum $\binom{20}{0} + \binom{20}{2} + \cdots + \binom{20}{20} = 2^{19}$.")],
  r"In $(1+i)^{20} = \sum_{r=0}^{20}\binom{20}{r}i^r$, the terms with even $r = 2k$ are real and equal $(-1)^k\binom{20}{2k}$, so the required sum is $\operatorname{Re}\left((1+i)^{20}\right)$. Since $(1+i)^2 = 2i$, $(1+i)^{20} = (2i)^{10} = 2^{10}i^{10} = -2^{10}$, because $i^{10} = i^2 = -1$. Hence the sum is $-2^{10} = -1024$.",
  "Assuming alternating sums vanish, or losing the sign of $i^{10}$.",
  "U05-B-complex-alt", "Eleven large coefficients make direct evaluation impractical; needs the substitution $x = i$, reading off a real part and a careful power of $i$.",
  check=lambda: sum((-1)**k*binomial(20, 2*k) for k in range(11)), values=[-2**10, 2**10, 0, 2**19],
  cognitive="Analysis", source_class="XI")

q("U05-B-039", T_GRT, "Greatest coefficient with a tie", "Difficult", "Multi-step computation MCQ",
  r"The greatest coefficient in the expansion of $(2 + 3x)^{9}$ is",
  r"$7 \cdot 2^5 \cdot 3^7$",
  [(r"$7 \cdot 2^6 \cdot 3^6$", r"Takes the middle term $T_5$, $\binom{9}{4}2^5 3^4$, as the greatest."),
   (r"$2^4 \cdot 3^9$", r"Uses the ratio $\frac{3(10-r)}{r} \ge 1$, ignoring the factor $2$, and gets $r = 7$: $\binom{9}{7}2^2 3^7$."),
   (r"$7 \cdot 2^6 \cdot 3^7$", r"Notices that $T_6$ and $T_7$ have equal coefficients and adds them.")],
  r"Let $c_r = \binom{9}{r}2^{9-r}3^r$. Then $\frac{c_r}{c_{r-1}} = \frac{10 - r}{r} \cdot \frac{3}{2} \ge 1$ iff $r \le 6$, with equality at $r = 6$. So $c_5 = c_6$ is the greatest: $c_6 = \binom{9}{6}2^3 3^6 = 84 \cdot 8 \cdot 729 = 7 \cdot 2^5 \cdot 3^7$.",
  "Assuming the greatest coefficient is at the middle term when the two parts carry different numbers.",
  "U05-B-greatest-coeff", "Ratio test with an equality case and prime-power bookkeeping.",
  check=lambda: max(coeffs((2 + 3*x)**9)),
  values=[7*2**5*3**7, 7*2**6*3**6, 2**4*3**9, 7*2**6*3**7], cognitive="Analysis", source_class="XI")

q("U05-B-040", T_SUM, "Weighted sum of coefficients divided by r + 1", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sum_{r=0}^{4}\frac{2^{r+1}}{r+1}\binom{4}{r}$ is",
  r"$\frac{242}{5}$",
  [(r"$\frac{243}{5}$", r"Uses $\frac{3^5}{5}$, forgetting to subtract the $s = 0$ term."),
   (r"$\frac{121}{2}$", r"Divides $3^5 - 1$ by $n = 4$ instead of $n + 1 = 5$."),
   (r"$\frac{211}{5}$", r"Subtracts $2^5$ instead of $1$, i.e. evaluates $\frac{3^5 - 2^5}{5}$.")],
  r"Since $\frac{1}{r+1}\binom{4}{r} = \frac{1}{5}\binom{5}{r+1}$, the sum is $\frac{1}{5}\sum_{s=1}^{5}\binom{5}{s}2^s = \frac{1}{5}\left[(1+2)^5 - 1\right] = \frac{242}{5}$.",
  "Forgetting the missing $s = 0$ term after the index shift.",
  "U05-B-Cr-over-r1", "Identity rewrite, index shift, and a binomial sum with a factor.",
  check=lambda: sum(Rational(2**(r + 1), r + 1)*binomial(4, r) for r in range(5)),
  values=[Rational(242, 5), Rational(243, 5), Rational(121, 2), Rational(211, 5)],
  cognitive="Analysis", source_class="XI")

def _c41():
    out = []
    for n in range(1, 8):
        out.append(binomial(2*n, n))
    return tuple(out)
def _odd(n, top):
    return prod([2*k - 1 for k in range(1, top + 1)])
q("U05-B-041", T_MID, "Coefficient of the middle term in closed form", "Difficult", "Conceptual/application MCQ",
  r"For every positive integer $n$, the coefficient of the middle term in the expansion of $(1 + x)^{2n}$ equals",
  r"$\frac{1 \cdot 3 \cdot 5 \cdots (2n-1)}{n!}\,2^n$",
  [(r"$\frac{1 \cdot 3 \cdot 5 \cdots (2n-1)}{n!}$", r"Splits $(2n)!$ into odd and even factors but drops the $2^n$ from $2 \cdot 4 \cdots 2n = 2^n n!$."),
   (r"$\frac{1 \cdot 3 \cdot 5 \cdots (2n+1)}{n!}\,2^n$", r"Runs the odd product one factor too far, to $2n + 1$."),
   (r"$\frac{1 \cdot 3 \cdot 5 \cdots (2n-1)}{(n!)^2}\,2^n$", r"Cancels $n!$ from the even factors but keeps both $n!$ in the denominator.")],
  r"The middle term is $T_{n+1}$ with coefficient $\binom{2n}{n} = \frac{(2n)!}{n!\,n!}$. Now $(2n)! = [1 \cdot 3 \cdots (2n-1)][2 \cdot 4 \cdots 2n] = [1 \cdot 3 \cdots (2n-1)]\,2^n n!$, so $\binom{2n}{n} = \frac{1 \cdot 3 \cdots (2n-1)}{n!}2^n$.",
  "Mishandling the factor $2^n n!$ when splitting $(2n)!$.",
  "U05-B-middle-formula", "Symbolic factorial manipulation with a common trap.",
  check=_c41,
  values=[tuple(Rational(_odd(n, n)*2**n, factorial(n)) for n in range(1, 8)),
          tuple(Rational(_odd(n, n), factorial(n)) for n in range(1, 8)),
          tuple(Rational(_odd(n, n + 1)*2**n, factorial(n)) for n in range(1, 8)),
          tuple(Rational(_odd(n, n)*2**n, factorial(n)**2) for n in range(1, 8))],
  cognitive="Analysis", source_class="XI")

def _c42():
    p = Poly(1 + x, x)**101 * Poly(1 - x + x**2, x)**100
    return len(p.terms())
q("U05-B-042", T_NUM, "Terms in a product after factor regrouping", "Difficult", "Multi-step computation MCQ",
  r"The number of terms in the expansion of $(1 + x)^{101}(1 - x + x^2)^{100}$, after simplification, is",
  r"$202$",
  [(r"$302$", r"Takes the degree $301$ and assumes every power from $x^0$ to $x^{301}$ appears."),
   (r"$101$", r"Counts only the terms of $(1 + x^3)^{100}$ and ignores the leftover factor $1 + x$."),
   (r"$102$", r"Adds one term for the leftover factor $1 + x$ instead of doubling the count.")],
  r"Group as $(1+x)\left[(1+x)(1 - x + x^2)\right]^{100} = (1 + x)(1 + x^3)^{100}$. The factor $(1+x^3)^{100}$ has the $101$ powers $x^{3k}$, $0 \le k \le 100$; multiplying by $1 + x$ gives powers $x^{3k}$ and $x^{3k+1}$, which never coincide. So there are $2 \times 101 = 202$ terms.",
  "Assuming all powers up to the degree occur.",
  "U05-B-numterms-factor", "Non-obvious regrouping, then counting with residues modulo $3$.",
  check=_c42, values=[202, 302, 101, 102], cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The number of terms in the expansion of $(1 + x)^{101}(1 - x + x^2)^{100}$, after simplification, is", answer=202))

q("U05-B-043", T_SUM, "Sum of products of distinct pairs of coefficients", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sum_{0 \le i < j \le 5}\binom{5}{i}\binom{5}{j}$ is",
  r"$386$",
  [(r"$772$", r"Computes $\left(\sum\binom{5}{r}\right)^2 - \sum\binom{5}{r}^2$ but does not halve it."),
   (r"$638$", r"Adds the sum of squares instead of subtracting it: $\frac{1024 + 252}{2}$."),
   (r"$512$", r"Takes half of $\left(2^5\right)^2$, ignoring the diagonal terms.")],
  r"$\left(\sum_{r}\binom{5}{r}\right)^2 = \sum_r\binom{5}{r}^2 + 2\sum_{i<j}\binom{5}{i}\binom{5}{j}$. So the sum is $\frac{2^{10} - \binom{10}{5}}{2} = \frac{1024 - 252}{2} = 386$.",
  "Forgetting the diagonal terms or the factor $2$ in the square of a sum.",
  "U05-B-pair-product-sum", "Square of a sum combined with the sum of squares identity.",
  check=lambda: sum(binomial(5, i)*binomial(5, j) for i, j in combinations(range(6), 2)),
  values=[386, 772, 638, 512], cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The value of $\sum_{0 \le i < j \le 5}\binom{5}{i}\binom{5}{j}$ is", answer=386))

q("U05-B-044", T_SUM, "Even-index coefficient sum excluding the constant", "Difficult", "Multi-step computation MCQ",
  r"If $(1 + 2x - 3x^2)^{6} = a_0 + a_1x + a_2x^2 + \cdots + a_{12}x^{12}$, then $a_2 + a_4 + a_6 + \cdots + a_{12}$ equals",
  r"$2047$",
  [(r"$2048$", r"Gives $\frac{f(1) + f(-1)}{2}$ but forgets to remove $a_0 = 1$."),
   (r"$4095$", r"Uses $f(1) + f(-1) - a_0$ without halving."),
   (r"$4096$", r"Takes $f(-1) = 4096$ alone as the even-index sum.")],
  r"Let $f(x) = (1 + 2x - 3x^2)^6$. Then $f(1) = 0^6 = 0$, $f(-1) = (1 - 2 - 3)^6 = (-4)^6 = 4096$ and $a_0 = f(0) = 1$. So $a_0 + a_2 + \cdots + a_{12} = \frac{0 + 4096}{2} = 2048$, and removing $a_0$ gives $2047$.",
  "Not excluding $a_0$, which the required sum starts after.",
  "U05-B-odd-even-sum", "Three evaluations combined, with a trap on the constant term.",
  check=lambda: sum(c for i, c in enumerate(coeffs((1 + 2*x - 3*x**2)**6)) if i % 2 == 0 and i >= 2),
  values=[2047, 2048, 4095, 4096], cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"If $(1 + 2x - 3x^2)^{6} = a_0 + a_1x + a_2x^2 + \cdots + a_{12}x^{12}$, then the value of $a_2 + a_4 + a_6 + \cdots + a_{12}$ is", answer=2047))

def _c45():
    s1 = sum((-1)**r*binomial(10, r)**2 for r in range(11)) == binomial(10, 5)
    s2 = sum(binomial(14, r) for r in range(8)) > 2**13
    return (bool(s1), bool(s2))
q("U05-B-045", T_SUM, "Alternating sum of squares; half sum for even index", "Difficult", "Statement-based MCQ",
  r"Statement I: $\binom{10}{0}^2 - \binom{10}{1}^2 + \binom{10}{2}^2 - \cdots + \binom{10}{10}^2 = \binom{10}{5}$. Statement II: $\binom{14}{0} + \binom{14}{1} + \binom{14}{2} + \cdots + \binom{14}{7} > 2^{13}$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement I by ignoring the sign factor $(-1)^5$ in the value $(-1)^{5}\binom{10}{5}$."),
   (ST_TF, r"Accepts Statement I as above and also takes the half sum to be exactly $2^{13}$, forgetting that the middle coefficient $\binom{14}{7}$ is counted only once."),
   (ST_FF, r"Rejects Statement I correctly but takes the half sum to be exactly $2^{13}$.")],
  r"Statement I: the sum is the coefficient of $x^{10}$ in $(1-x)^{10}(1+x)^{10} = (1-x^2)^{10}$, which is $(-1)^5\binom{10}{5} = -252 \ne 252$; false. Statement II: by symmetry, $2\sum_{r=0}^{6}\binom{14}{r} + \binom{14}{7} = 2^{14}$, so $\sum_{r=0}^{7}\binom{14}{r} = 2^{13} + \frac{1}{2}\binom{14}{7} = 8192 + 1716 > 2^{13}$; true.",
  "Dropping the sign in the alternating square sum and mishandling the middle coefficient in a half sum.",
  "U05-B-statement-squares", "Two non-routine identity checks, each with a trap.",
  check=_c45, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Analysis", source_class="XI")

q("U05-B-046", T_SUM, "Sum with odd weights 2r + 1", "Difficult", "Multi-step computation MCQ",
  r"The value of $\binom{10}{0} + 3\binom{10}{1} + 5\binom{10}{2} + \cdots + 21\binom{10}{10}$ is",
  r"$11264$",
  [(r"$21504$", r"Uses $(2n+1)2^n$, as if every coefficient carried the largest weight."),
   (r"$10752$", r"Uses $(2n+1)2^{n-1}$, averaging the weights wrongly."),
   (r"$10240$", r"Computes $2\sum r\binom{10}{r} = n2^n$ and forgets the $\sum\binom{10}{r}$ part.")],
  r"The general term is $(2r + 1)\binom{10}{r}$, so the sum is $2\sum r\binom{10}{r} + \sum\binom{10}{r} = 2 \cdot 10 \cdot 2^9 + 2^{10} = 10240 + 1024 = 11264$. Equivalently, pairing $r$ with $10 - r$ gives weights summing to $22$, so the sum is $11 \cdot 2^{10}$.",
  "Not splitting the linear weight into two standard sums.",
  "U05-B-weighted-sum", "Identify the weight pattern, split and use two identities.",
  check=lambda: sum((2*r + 1)*binomial(10, r) for r in range(11)), values=[11264, 21504, 10752, 10240],
  cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"The value of $\binom{10}{0} + 3\binom{10}{1} + 5\binom{10}{2} + \cdots + 21\binom{10}{10}$ is", answer=11264))

def _c47():
    out = []
    for n in range(2, 8):
        s = sum(Rational(1, binomial(n, r)) for r in range(n + 1))
        t = sum(Rational(r, binomial(n, r)) for r in range(n + 1))
        out.append(t / s)
    return tuple(out)
q("U05-B-047", T_SUM, "Sums of reciprocals of binomial coefficients", "Difficult", "Multi-step computation MCQ",
  r"For a positive integer $n$, let $s_n = \sum_{r=0}^{n}\frac{1}{\binom{n}{r}}$ and $t_n = \sum_{r=0}^{n}\frac{r}{\binom{n}{r}}$. Then $\frac{t_n}{s_n}$ equals",
  r"$\frac{n}{2}$",
  [(r"$n$", r"Adds $t_n$ to its reversed form to get $n s_n$ but forgets to divide by $2$."),
   (r"$\frac{n-1}{2}$", r"Pairs $r$ with $n - 1 - r$ instead of $n - r$."),
   (r"$\frac{n+1}{2}$", r"Pairs $r$ with $n + 1 - r$, counting one term too many.")],
  r"Replacing $r$ by $n - r$ and using $\binom{n}{n-r} = \binom{n}{r}$ gives $t_n = \sum\frac{n - r}{\binom{n}{r}} = n s_n - t_n$. So $2t_n = n s_n$ and $\frac{t_n}{s_n} = \frac{n}{2}$.",
  "Not using the symmetry $\\binom{n}{r} = \\binom{n}{n-r}$ to reverse the sum.",
  "U05-B-reciprocal-symmetry", "Non-obvious reversal trick on an unfamiliar sum.",
  check=_c47,
  values=[tuple(Rational(n, 2) for n in range(2, 8)), tuple(Integer(n) for n in range(2, 8)),
          tuple(Rational(n - 1, 2) for n in range(2, 8)), tuple(Rational(n + 1, 2) for n in range(2, 8))],
  cognitive="Analysis", source_class="XI")
