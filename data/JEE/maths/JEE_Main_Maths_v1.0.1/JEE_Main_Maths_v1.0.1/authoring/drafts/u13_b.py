import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
SC = "XI"
TOPIC = "Measures of dispersion"
VN = r" (Variance is taken as $\frac{1}{n}\sum (x_i - \bar{x})^2$.)"
VN_FRONT = r"Take the variance of $n$ observations as $\frac{1}{n}\sum (x_i - \bar{x})^2$. "

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."


def mean_(L):
    L = [nsimplify(v) for v in L]
    return Add(*L) / len(L)


def var_(L):
    m = mean_(L)
    return Add(*[(nsimplify(v) - m) ** 2 for v in L]) / len(L)


def md_(L, c):
    return Add(*[Abs(nsimplify(v) - c) for v in L]) / len(L)


def median_(L):
    s = sorted(nsimplify(v) for v in L)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def expand_freq(xs, fs):
    out = []
    for x, f in zip(xs, fs):
        out += [x] * f
    return out


# ================================================================ EASY (14)

def _c001():
    return var_(list(range(1, 11)))


q("U13-B-001", TOPIC, "Variance of first n natural numbers", "Easy", "Single-step computation MCQ",
  r"The variance of the first $10$ natural numbers $1, 2, 3, \ldots, 10$ is" + VN,
  r"$\frac{33}{4}$",
  [(r"$\frac{77}{2}$", r"Computes only the mean of the squares, $\frac{1}{10}\sum k^2 = \frac{385}{10} = \frac{77}{2}$, and never subtracts $\bar{x}^2 = \frac{121}{4}$."),
   (r"$\frac{55}{6}$", r"Divides the sum of squared deviations $\frac{165}{2}$ by $n - 1 = 9$, giving $\frac{55}{6}$."),
   (r"$\frac{\sqrt{33}}{2}$", r"Reports the standard deviation $\sqrt{\frac{33}{4}}$ rather than the variance.")],
  r"For $1, 2, \ldots, n$ the variance is $\frac{1}{n}\sum k^2 - \left(\frac{n+1}{2}\right)^2 = \frac{(n+1)(2n+1)}{6} - \frac{(n+1)^2}{4} = \frac{n^2 - 1}{12}$. With $n = 10$ this is $\frac{99}{12} = \frac{33}{4}$.",
  r"Forgetting to subtract the square of the mean, or using divisor $n-1$.",
  "U13-B-var-natural-numbers", "Direct use of one standard result.",
  check=_c001, values=[Rational(33, 4), Rational(77, 2), Rational(55, 6), sqrt(33) / 2], cognitive="Recall", source_class=SC)


def _c002():
    a, b = 5, -2
    var_x = 9
    return b ** 2 * var_x


q("U13-B-002", TOPIC, "Change of origin and scale", "Easy", "Single-step computation MCQ",
  r"The variance of the observations $x_1, x_2, \ldots, x_n$ is $9$. If $y_i = 5 - 2x_i$ for each $i$, then the variance of $y_1, y_2, \ldots, y_n$ is",
  r"$36$",
  [(r"$18$", r"Multiplies the variance by $|{-2}| = 2$ instead of by $(-2)^2 = 4$."),
   (r"$6$", r"Finds the standard deviation of $y$, $2 \cdot 3 = 6$, and reports it as the variance."),
   (r"$41$", r"Lets the added constant $5$ change the spread: $4 \cdot 9 + 5 = 41$.")],
  r"If $y_i = a + b x_i$ then $\sigma_y^2 = b^2 \sigma_x^2$; the constant $a$ does not affect spread. Here $b = -2$, so $\sigma_y^2 = 4 \cdot 9 = 36$.",
  r"Scaling the variance by $|b|$ instead of $b^2$, or letting a shift change it.",
  "U13-B-origin-scale", "One property of variance applied once.",
  check=_c002, values=[36, 18, 6, 41], cognitive="Application", source_class=SC)


def _c003():
    L = [1, 3, 4, 8, 14]
    return md_(L, mean_(L))


q("U13-B-003", TOPIC, "Mean deviation about mean (ungrouped)", "Easy", "Single-step computation MCQ",
  r"The mean deviation about the mean of the observations $1, 3, 4, 8, 14$ is",
  r"$4$",
  [(r"$\frac{18}{5}$", r"Measures deviations from the median $4$: $\frac{3+1+0+4+10}{5} = \frac{18}{5}$."),
   (r"$5$", r"Divides the total absolute deviation $20$ by $n - 1 = 4$."),
   (r"$\frac{43}{10}$", r"Takes the centre as the mid-range $\frac{1+14}{2} = 7.5$: $\frac{6.5+4.5+3.5+0.5+6.5}{5} = \frac{43}{10}$.")],
  r"The mean is $\frac{30}{5} = 6$. The absolute deviations are $5, 3, 2, 2, 8$, with sum $20$, so the mean deviation about the mean is $\frac{20}{5} = 4$.",
  r"Using the median, or the mid-range, as the centre when the question asks about the mean.",
  "U13-B-md-ungrouped", "Single computation with one centre.",
  check=_c003, values=[4, Rational(18, 5), 5, Rational(43, 10)], cognitive="Application", source_class=SC)


def _c004():
    n, S1, S2 = 10, 60, 400
    return sqrt(Rational(S2, n) - Rational(S1, n) ** 2)


q("U13-B-004", TOPIC, "Variance from sums", "Easy", "Single-step computation MCQ",
  r"For $10$ observations $x_1, x_2, \ldots, x_{10}$, it is given that $\sum x_i = 60$ and $\sum x_i^2 = 400$. The standard deviation of these observations is" + VN,
  r"$2$",
  [(r"$4$", r"Stops at the variance $40 - 36 = 4$ and reports it as the standard deviation."),
   (r"$\sqrt{34}$", r"Subtracts the mean $6$ rather than its square: $\sqrt{40 - 6}$."),
   (r"$\frac{2\sqrt{10}}{3}$", r"Uses divisor $n-1$: $\frac{400 - 360}{9} = \frac{40}{9}$, whose square root is $\frac{2\sqrt{10}}{3}$.")],
  r"$\sigma^2 = \frac{\sum x_i^2}{n} - \left(\frac{\sum x_i}{n}\right)^2 = 40 - 36 = 4$, so $\sigma = 2$.",
  r"Confusing variance with standard deviation, or subtracting $\bar{x}$ instead of $\bar{x}^2$.",
  "U13-B-var-from-sums", "One formula, one square root.",
  check=_c004, values=[2, 4, sqrt(34), 2 * sqrt(10) / 3], cognitive="Application", source_class=SC)


def _c005():
    m, v, a, b = 10, 4, 3, 2
    return (a * m + b, a ** 2 * v)


q("U13-B-005", TOPIC, "Change of origin and scale", "Easy", "Single-step computation MCQ",
  r"A set of observations has mean $10$ and variance $4$. Each observation is multiplied by $3$ and then $2$ is added to it. The mean and variance of the new observations are respectively",
  r"$32$ and $36$",
  [(r"$32$ and $38$", r"Adds the constant $2$ to the variance as well: $9 \cdot 4 + 2 = 38$."),
   (r"$32$ and $12$", r"Multiplies the variance by $3$ instead of $3^2$."),
   (r"$32$ and $14$", r"Multiplies the variance by $3$ and also adds $2$: $12 + 2 = 14$.")],
  r"For $y = 3x + 2$, $\bar{y} = 3\bar{x} + 2 = 32$ and $\sigma_y^2 = 3^2 \sigma_x^2 = 9 \cdot 4 = 36$. Adding a constant shifts the mean but not the spread.",
  r"Treating variance like the mean under a linear change.",
  "U13-B-origin-scale", "One rule for mean and one for variance.",
  check=_c005, values=[(32, 36), (32, 38), (32, 12), (32, 14)], cognitive="Understanding", source_class=SC)


def _c006():
    a, b = symbols('a b', real=True)
    sols = solve([Eq((a + b) / 2, 7), Eq(((a - 7) ** 2 + (b - 7) ** 2) / 2, 9)], [a, b], dict=True)
    prods = {simplify(s[a] * s[b]) for s in sols}
    assert len(prods) == 1
    return prods.pop()


q("U13-B-006", TOPIC, "Standard deviation of two observations", "Easy", "Single-step computation MCQ",
  r"Two observations have mean $7$ and standard deviation $3$. The product of the two observations is" + VN,
  r"$40$",
  [(r"$58$", r"Adds the variance to the square of the mean: $49 + 9$."),
   (r"$46$", r"Subtracts the standard deviation $3$ from $49$ rather than the variance $9$."),
   (r"$\frac{187}{4}$", r"Takes the standard deviation of two numbers as $|a - b|$, so $a, b = 5.5, 8.5$ and the product is $\frac{187}{4}$.")],
  r"For two observations $a, b$, the standard deviation is $\frac{|a - b|}{2}$. So $a + b = 14$ and $|a - b| = 6$, giving $a, b = 4, 10$ and $ab = 40$. Equivalently $ab = \bar{x}^2 - \sigma^2 = 49 - 9$.",
  r"Using $|a - b|$ as the standard deviation of two numbers.",
  "U13-B-two-observations", "Two linear equations from the definitions.",
  check=_c006, values=[40, 58, 46, Rational(187, 4)], cognitive="Application", source_class=SC)


def _c007():
    return var_([2 * k - 1 for k in range(1, 11)])


q("U13-B-007", TOPIC, "Variance of an arithmetic progression", "Easy", "Single-step computation MCQ",
  r"The variance of the first $10$ odd natural numbers $1, 3, 5, \ldots, 19$ is" + VN,
  r"$33$",
  [(r"$\frac{33}{4}$", r"Uses the variance $\frac{n^2-1}{12}$ of consecutive integers and ignores the common difference $2$."),
   (r"$\frac{33}{2}$", r"Multiplies $\frac{33}{4}$ by the common difference $2$ instead of by its square $4$."),
   (r"$133$", r"Computes the mean of the squares $\frac{1330}{10} = 133$ and does not subtract $\bar{x}^2 = 100$.")],
  r"The numbers are $2k - 1$ for $k = 1, \ldots, 10$, a change of scale by $2$ of $1, \ldots, 10$. Hence the variance is $2^2 \cdot \frac{10^2 - 1}{12} = 4 \cdot \frac{33}{4} = 33$.",
  r"Scaling the variance by the common difference instead of its square.",
  "U13-B-ap-variance", "One standard result with one scaling.",
  check=_c007, values=[33, Rational(33, 4), Rational(33, 2), 133], cognitive="Application", source_class=SC)


def _c008():
    return var_([1001, 1003, 1005, 1007, 1009])


q("U13-B-008", TOPIC, "Invariance under change of origin", "Easy", "Single-step computation MCQ",
  r"The variance of the observations $1001, 1003, 1005, 1007, 1009$ is" + VN,
  r"$8$",
  [(r"$10$", r"Divides the sum of squared deviations $40$ by $n - 1 = 4$."),
   (r"$2\sqrt{2}$", r"Reports the standard deviation $\sqrt{8}$."),
   (r"$4$", r"Shifts to $1, 2, 3, 4, 5$ (variance $2$) and then multiplies by the spacing $2$ instead of $2^2$.")],
  r"Subtracting $1005$ from each value gives $-4, -2, 0, 2, 4$, which has the same variance. Its mean is $0$, so the variance is $\frac{16+4+0+4+16}{5} = 8$.",
  r"Not using the shift, or scaling the variance by the spacing instead of its square.",
  "U13-B-shift-invariance", "One shift and a short sum.",
  check=_c008, values=[8, 10, 2 * sqrt(2), 4], cognitive="Application", source_class=SC)


def _c009():
    mP, sP, mQ, sQ = 40, 8, 50, 12
    return (Rational(sP, mP)) / (Rational(sQ, mQ))


q("U13-B-009", TOPIC, "Coefficient of variation as a ratio", "Easy", "Single-step computation MCQ",
  r"Series P has mean $40$ and standard deviation $8$; series Q has mean $50$ and standard deviation $12$. The ratio of the coefficient of variation of P to that of Q is",
  r"$\frac{5}{6}$",
  [(r"$\frac{2}{3}$", r"Compares only the standard deviations, $\frac{8}{12}$."),
   (r"$\frac{4}{5}$", r"Compares only the means, $\frac{40}{50}$."),
   (r"$\frac{6}{5}$", r"Inverts the ratio, giving Q to P.")],
  r"The coefficient of variation is $\frac{\sigma}{\bar{x}} \times 100$. For P it is $20$ and for Q it is $24$, so the ratio is $\frac{20}{24} = \frac{5}{6}$.",
  r"Comparing standard deviations directly when the means differ.",
  "U13-B-cv-ratio", "One definition, one division.",
  check=_c009, values=[Rational(5, 6), Rational(2, 3), Rational(4, 5), Rational(6, 5)], cognitive="Application", source_class=SC)


def _c010():
    L = [1, 3, 4, 8, 14, 2, 21]
    sd = sqrt(var_(L))
    sd2 = sqrt(var_([-2 * v for v in L]))
    s1 = simplify(sd2 - (-2) * sd) == 0
    ok = True
    for D in ([1, 3, 4, 8, 14], [2, 6, 7, 9, 16], [1, 2, 3, 4, 10, 30], [5, 5, 6, 20]):
        ok = ok and (md_(D, median_(D)) <= md_(D, mean_(D)))
    return (s1, bool(ok))


q("U13-B-010", TOPIC, "Properties of dispersion", "Easy", "Statement-based MCQ",
  r"Statement I: If every observation of a data set is multiplied by $-2$, then its standard deviation is also multiplied by $-2$. Statement II: For any data set, the mean deviation about the median does not exceed the mean deviation about the mean." + TAIL,
  ST_FT,
  [(ST_TT, r"Carries the factor $-2$ over to the standard deviation as it carries over to the mean; but standard deviation is never negative."),
   (ST_FF, r"Rejects Statement II, not recalling that $\sum |x_i - a|$ is least when $a$ is the median."),
   (ST_TF, r"Accepts the sign carry-over in Statement I and rejects the minimum property in Statement II.")],
  r"If $y_i = -2x_i$ then $\sigma_y = |-2|\,\sigma_x = 2\sigma_x$, so Statement I is false. The function $a \mapsto \sum |x_i - a|$ attains its least value at the median, so the mean deviation about the median is at most that about the mean (or about any other point); Statement II is true.",
  r"Believing standard deviation picks up the sign of the scaling factor.",
  "U13-B-statement-scale-median", "Two standard properties recalled.",
  check=_c010, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Understanding", source_class=SC)


def _c011():
    n, m, v = 5, 6, 4
    return n * (v + m ** 2)


q("U13-B-011", TOPIC, "Sum of squares from mean and variance", "Easy", "Single-step computation MCQ",
  r"The mean and variance of $5$ observations are $6$ and $4$ respectively. The sum of the squares of the observations is" + VN,
  r"$200$",
  [(r"$160$", r"Subtracts the variance: $5(36 - 4)$."),
   (r"$190$", r"Uses the standard deviation $2$ in place of the variance: $5(36 + 2)$."),
   (r"$40$", r"Finds the mean of the squares $4 + 36$ and does not multiply by $n = 5$.")],
  r"Since $\sigma^2 = \frac{\sum x_i^2}{n} - \bar{x}^2$, we get $\sum x_i^2 = n(\sigma^2 + \bar{x}^2) = 5(4 + 36) = 200$.",
  r"Rearranging the variance formula with the wrong sign or forgetting the factor $n$.",
  "U13-B-sum-squares-reverse", "One rearranged formula.",
  check=_c011, values=[200, 160, 190, 40], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean and variance of $5$ observations are $6$ and $4$ respectively, where variance is taken as $\frac{1}{n}\sum (x_i - \bar{x})^2$. The sum of the squares of the observations is", answer=200))


def _c012():
    n = 10
    # two groups of equal size, common mean 10, variances 4 and 16
    sx2 = n * (4 + 100) + n * (16 + 100)
    sx = 2 * n * 10
    return sqrt(Rational(sx2, 2 * n) - Rational(sx, 2 * n) ** 2)


q("U13-B-012", TOPIC, "Combined standard deviation with equal means", "Easy", "Single-step computation MCQ",
  r"Two groups of $10$ observations each have the same mean $10$. Their variances are $4$ and $16$. The standard deviation of all $20$ observations taken together is" + VN,
  r"$\sqrt{10}$",
  [(r"$3$", r"Averages the two standard deviations, $\frac{2 + 4}{2}$."),
   (r"$2\sqrt{5}$", r"Adds the variances, $\sqrt{4 + 16}$."),
   (r"$6$", r"Adds the two standard deviations, $2 + 4$.")],
  r"With equal means, the combined variance is the size-weighted average of the variances: $\frac{10 \cdot 4 + 10 \cdot 16}{20} = 10$. Hence the combined standard deviation is $\sqrt{10}$.",
  r"Averaging or adding standard deviations instead of variances.",
  "U13-B-combined-equal-means", "One weighted average of variances.",
  check=_c012, values=[sqrt(10), 3, 2 * sqrt(5), 6], cognitive="Application", source_class=SC)


def _c013():
    n, s1, s2 = 10, 20, 100
    return Rational(s2, n) - Rational(s1, n) ** 2


q("U13-B-013", TOPIC, "Variance from deviations about an assumed value", "Easy", "Single-step computation MCQ",
  r"For $10$ observations, $\sum (x_i - 5) = 20$ and $\sum (x_i - 5)^2 = 100$. The variance of the observations is" + VN,
  r"$6$",
  [(r"$10$", r"Takes $\frac{1}{n}\sum (x_i - 5)^2$ as the variance, treating $5$ as the mean."),
   (r"$8$", r"Subtracts the mean of the deviations $2$ instead of its square $4$."),
   (r"$\frac{20}{3}$", r"Uses divisor $n - 1$: $\frac{100 - 10 \cdot 4}{9}$.")],
  r"With $d_i = x_i - 5$, the variance is unchanged by the shift: $\sigma^2 = \frac{\sum d_i^2}{n} - \left(\frac{\sum d_i}{n}\right)^2 = 10 - 4 = 6$.",
  r"Treating the assumed value as the actual mean.",
  "U13-B-deviation-sums", "One shift and one formula.",
  check=_c013, values=[6, 10, 8, Rational(20, 3)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"For $10$ observations, $\sum (x_i - 5) = 20$ and $\sum (x_i - 5)^2 = 100$. Taking variance as $\frac{1}{n}\sum (x_i - \bar{x})^2$, the variance of the observations is", answer=6))


def _c014():
    L = [Rational(v) for v in (1, 3, 4, 8, 14)]
    base = md_(L, mean_(L))
    L2 = [4 - 3 * v for v in L]
    return simplify(md_(L2, mean_(L2)) / base * 2)


q("U13-B-014", TOPIC, "Mean deviation under change of origin and scale", "Easy", "Single-step computation MCQ",
  r"The mean deviation about the mean of $x_1, x_2, \ldots, x_n$ is $2$. The mean deviation about the mean of $4 - 3x_1, 4 - 3x_2, \ldots, 4 - 3x_n$ is",
  r"$6$",
  [(r"$18$", r"Multiplies by $(-3)^2 = 9$, the factor that applies to variance."),
   (r"$2$", r"Assumes mean deviation is unaffected by any linear change."),
   (r"$10$", r"Lets the shift $4$ add to the result: $3 \cdot 2 + 4$.")],
  r"If $y_i = a + b x_i$ then $\bar{y} = a + b\bar{x}$ and $|y_i - \bar{y}| = |b|\,|x_i - \bar{x}|$. So the mean deviation is multiplied by $|-3| = 3$, giving $6$.",
  r"Using $b^2$ (as for variance) for the mean deviation.",
  "U13-B-md-origin-scale", "One property applied once.",
  check=_c014, values=[6, 18, 2, 10], cognitive="Understanding", source_class=SC)


# ================================================================ MEDIUM (20)

def _c015():
    xs, fs = [3, 5, 7, 9, 11], [2, 4, 6, 5, 3]
    L = expand_freq(xs, fs)
    return md_(L, median_(L))


q("U13-B-015", TOPIC, "Mean deviation about median (discrete frequency)", "Medium", "Multi-step computation MCQ",
  r"The values $x$: $3, 5, 7, 9, 11$ occur with frequencies $f$: $2, 4, 6, 5, 3$ respectively. The mean deviation about the median is",
  r"$\frac{19}{10}$",
  [(r"$\frac{49}{25}$", r"Takes deviations about the mean $7.3$ instead of the median: $\frac{39.2}{20}$."),
   (r"$\frac{38}{5}$", r"Divides $\sum f|x - 7| = 38$ by the number of distinct values $5$ instead of $N = 20$."),
   (r"$\frac{12}{5}$", r"Ignores the frequencies: $\frac{4+2+0+2+4}{5}$.")],
  r"$N = 20$; cumulative frequencies are $2, 6, 12, 17, 20$, so the $10$th and $11$th values are both $7$ and the median is $7$. Then $\sum f|x - 7| = 2 \cdot 4 + 4 \cdot 2 + 0 + 5 \cdot 2 + 3 \cdot 4 = 38$, and the mean deviation is $\frac{38}{20} = \frac{19}{10}$.",
  r"Dividing by the number of classes instead of the total frequency.",
  "U13-B-md-median-discrete", "Median from cumulative frequency, then a weighted sum.",
  check=_c015, values=[Rational(19, 10), Rational(49, 25), Rational(38, 5), Rational(12, 5)], cognitive="Application", source_class=SC)


def _c016():
    n, m, v = 10, 20, 9
    S1, S2 = n * m, n * (v + m ** 2)
    S1c, S2c = S1 - 15 + 25, S2 - 15 ** 2 + 25 ** 2
    return Rational(S2c, n) - Rational(S1c, n) ** 2


q("U13-B-016", TOPIC, "Corrected variance after a misrecorded observation", "Medium", "Multi-step computation MCQ",
  r"The mean and variance of $10$ observations were found to be $20$ and $9$. Later it was found that one observation, $25$, had been recorded as $15$. The correct variance is" + VN,
  r"$8$",
  [(r"$49$", r"Corrects $\sum x^2$ to $4490$ but subtracts the old mean squared: $449 - 400$."),
   (r"$9$", r"Assumes a misrecorded value changes only the mean, not the variance."),
   (r"$2\sqrt{2}$", r"Reports the corrected standard deviation $\sqrt{8}$.")],
  r"Wrong $\sum x = 200$ and $\sum x^2 = 10(9 + 400) = 4090$. Correcting: $\sum x = 210$, so $\bar{x} = 21$; $\sum x^2 = 4090 - 225 + 625 = 4490$. Hence $\sigma^2 = 449 - 441 = 8$.",
  r"Correcting $\sum x^2$ but not the mean.",
  "U13-B-corrected-replace", "Correct two sums, then recompute.",
  check=_c016, values=[8, 49, 9, 2 * sqrt(2)], cognitive="Application", source_class=SC)


def _c017():
    n, m, v = 20, 10, 4
    S1, S2 = n * m, n * (v + m ** 2)
    S1c, S2c = S1 - 10, S2 - 100
    return Rational(S2c, n - 1) - Rational(S1c, n - 1) ** 2


q("U13-B-017", TOPIC, "Variance after removing an observation", "Medium", "Multi-step computation MCQ",
  r"The mean and standard deviation of $20$ observations are $10$ and $2$. One observation equal to $10$ is found to be invalid and is removed. The variance of the remaining $19$ observations is" + VN,
  r"$\frac{80}{19}$",
  [(r"$4$", r"Assumes that removing a value equal to the mean leaves the variance unchanged."),
   (r"$\frac{35}{4}$", r"Removes the value from both sums but keeps $n = 20$: $\frac{1980}{20} - \left(\frac{190}{20}\right)^2$."),
   (r"$\frac{170}{19}$", r"Subtracts $10$ rather than $10^2$ from $\sum x^2$: $\frac{2070}{19} - 100$.")],
  r"$\sum x = 200$ and $\sum x^2 = 20(4 + 100) = 2080$. After removal, $\sum x = 190$ (mean still $10$) and $\sum x^2 = 1980$. So $\sigma^2 = \frac{1980}{19} - 100 = \frac{80}{19}$. The sum of squared deviations stays $80$ but is now shared by $19$ values.",
  r"Thinking that deleting a value equal to the mean cannot change the variance.",
  "U13-B-corrected-remove", "Two sums updated and a changed count; a trap on the mean.",
  check=_c017, values=[Rational(80, 19), 4, Rational(35, 4), Rational(170, 19)], cognitive="Analysis", source_class=SC)


def _c018():
    n1, m1, v1, n2, m2, v2 = 10, 12, 4, 15, 17, 9
    N = n1 + n2
    S1 = n1 * m1 + n2 * m2
    S2 = n1 * (v1 + m1 ** 2) + n2 * (v2 + m2 ** 2)
    return Rational(S2, N) - Rational(S1, N) ** 2


q("U13-B-018", TOPIC, "Combined variance of two groups", "Medium", "Multi-step computation MCQ",
  r"One group of $10$ observations has mean $12$ and variance $4$; another group of $15$ observations has mean $17$ and variance $9$. The variance of all $25$ observations taken together is" + VN,
  r"$13$",
  [(r"$7$", r"Takes only the weighted average of the variances, $\frac{40 + 135}{25}$, ignoring the difference of means."),
   (r"$\frac{13}{2}$", r"Takes the simple average of the two variances."),
   (r"$32$", r"Adds the full squared difference of means $25$ to $7$ instead of $\frac{n_1 n_2}{(n_1+n_2)^2}(12-17)^2 = 6$.")],
  r"Combined mean $= \frac{120 + 255}{25} = 15$. Then $\sigma^2 = \frac{n_1(\sigma_1^2 + d_1^2) + n_2(\sigma_2^2 + d_2^2)}{n_1 + n_2}$ with $d_1 = -3$, $d_2 = 2$: $\frac{10(4 + 9) + 15(9 + 4)}{25} = \frac{325}{25} = 13$.",
  r"Ignoring the spread between group means.",
  "U13-B-combined-variance", "Combined mean, then the combined-variance formula.",
  check=_c018, values=[13, 7, Rational(13, 2), 32], cognitive="Application", source_class=SC)


def _c019():
    m = symbols('m', positive=True)
    n = 10
    S1 = n * 5 + n * m
    S2 = n * (4 + 25) + n * (4 + m ** 2)
    sol = [s for s in solve(Eq(S2 / (2 * n) - (S1 / (2 * n)) ** 2, 13), m) if s > 5]
    assert len(sol) == 1
    return sol[0]


q("U13-B-019", TOPIC, "Combined variance with an unknown mean", "Medium", "Inverse/parameter MCQ",
  r"Groups P and Q have $10$ observations each. Group P has mean $5$ and variance $4$; group Q has variance $4$ and mean $m$, where $m > 5$. If the variance of all $20$ observations together is $13$, then $m$ equals" + VN,
  r"$11$",
  [(r"$8$", r"Uses $4 + (m-5)^2 = 13$, dropping the factor $\frac{n_1 n_2}{(n_1+n_2)^2} = \frac{1}{4}$."),
   (r"$23$", r"Uses $4 + \frac{m - 5}{2} = 13$, taking half the difference of means without squaring."),
   (r"$5 + 2\sqrt{5}$", r"Adds the two variances: $8 + \frac{(m-5)^2}{4} = 13$, so $(m-5)^2 = 20$.")],
  r"For equal group sizes, $\sigma^2 = \frac{\sigma_1^2 + \sigma_2^2}{2} + \frac{(m_1 - m_2)^2}{4}$. So $4 + \frac{(m - 5)^2}{4} = 13$, giving $(m - 5)^2 = 36$ and, since $m > 5$, $m = 11$.",
  r"Forgetting the weight on the between-group term.",
  "U13-B-combined-variance-reverse", "Combined-variance formula used backwards with a sign condition.",
  check=_c019, values=[11, 8, 23, 5 + 2 * sqrt(5)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Groups P and Q have $10$ observations each. Group P has mean $5$ and variance $4$; group Q has variance $4$ and mean $m$, where $m > 5$. If the variance of all $20$ observations together is $13$ (variance taken with divisor $n$), then $m$ is", answer=11))


def _c020():
    mids, fs = [5, 15, 25, 35], [2, 3, 3, 2]
    return var_(expand_freq(mids, fs))


q("U13-B-020", TOPIC, "Variance of grouped continuous data", "Medium", "Multi-step computation MCQ",
  r"For the distribution with classes $0\text{-}10$, $10\text{-}20$, $20\text{-}30$, $30\text{-}40$ and frequencies $2, 3, 3, 2$ respectively, the variance (using class mid-points) is" + VN,
  r"$105$",
  [(r"$125$", r"Ignores the frequencies and finds the variance of the mid-points $5, 15, 25, 35$."),
   (r"$\frac{350}{3}$", r"Divides $\sum f(x - 20)^2 = 1050$ by $N - 1 = 9$."),
   (r"$\sqrt{105}$", r"Reports the standard deviation.")],
  r"Mid-points $5, 15, 25, 35$; the distribution is symmetric, so $\bar{x} = 20$. $\sum f (x - 20)^2 = 2 \cdot 225 + 3 \cdot 25 + 3 \cdot 25 + 2 \cdot 225 = 1050$, so $\sigma^2 = \frac{1050}{10} = 105$.",
  r"Ignoring frequencies when computing a grouped variance.",
  "U13-B-grouped-continuous-var", "Mid-points, mean, weighted squared deviations.",
  check=_c020, values=[105, 125, Rational(350, 3), sqrt(105)], cognitive="Application", source_class=SC)


def _c021():
    mids, fs = [2, 6, 10, 14], [1, 3, 4, 2]
    L = expand_freq(mids, fs)
    return md_(L, mean_(L))


q("U13-B-021", TOPIC, "Mean deviation about mean (grouped continuous)", "Medium", "Multi-step computation MCQ",
  r"For the distribution with classes $0\text{-}4$, $4\text{-}8$, $8\text{-}12$, $12\text{-}16$ and frequencies $1, 3, 4, 2$ respectively, the mean deviation about the mean (using class mid-points) is",
  r"$\frac{76}{25}$",
  [(r"$3$", r"Takes deviations about the median $8 + \frac{5 - 4}{4} \cdot 4 = 9$: $\frac{7 + 9 + 4 + 10}{10}$."),
   (r"$\frac{38}{5}$", r"Divides $\sum f|x - \bar{x}| = 30.4$ by the number of classes $4$."),
   (r"$\frac{16}{5}$", r"Uses the unweighted mean $8$ of the mid-points as the centre: $\frac{6 + 6 + 8 + 12}{10}$.")],
  r"Mid-points $2, 6, 10, 14$; $\bar{x} = \frac{2 + 18 + 40 + 28}{10} = 8.8$. Then $\sum f|x - 8.8| = 6.8 + 3(2.8) + 4(1.2) + 2(5.2) = 30.4$, so the mean deviation is $3.04 = \frac{76}{25}$.",
  r"Using the wrong centre or the wrong divisor in grouped mean deviation.",
  "U13-B-md-mean-grouped", "Weighted mean, then weighted absolute deviations.",
  check=_c021, values=[Rational(76, 25), 3, Rational(38, 5), Rational(16, 5)], cognitive="Application", source_class=SC)


def _c022():
    n, Su, Su2, h = 20, 10, 120, 5
    vu = Rational(Su2, n) - Rational(Su, n) ** 2
    return h ** 2 * vu


q("U13-B-022", TOPIC, "Step-deviation (coded) variance", "Medium", "Multi-step computation MCQ",
  r"For $20$ observations $x_i$, let $u_i = \frac{x_i - 50}{5}$. If $\sum u_i = 10$ and $\sum u_i^2 = 120$, then the variance of the $x_i$ is" + VN,
  r"$\frac{575}{4}$",
  [(r"$\frac{23}{4}$", r"Finds the variance of $u$ and forgets to multiply by $5^2$."),
   (r"$\frac{115}{4}$", r"Multiplies the variance of $u$ by $5$ instead of $25$."),
   (r"$150$", r"Multiplies the mean of $u^2$, which is $6$, by $25$ without subtracting $\bar{u}^2$.")],
  r"$\sigma_u^2 = \frac{120}{20} - \left(\frac{10}{20}\right)^2 = 6 - \frac{1}{4} = \frac{23}{4}$. Since $x = 50 + 5u$, $\sigma_x^2 = 25 \sigma_u^2 = \frac{575}{4}$.",
  r"Not undoing the change of scale with its square.",
  "U13-B-coded-variance", "Coded variance, then reverse scaling.",
  check=_c022, values=[Rational(575, 4), Rational(23, 4), Rational(115, 4), 150], cognitive="Application", source_class=SC)


def _c023():
    a, b = symbols('a b', real=True)
    n, m, v = 5, 6, 6
    known = [2, 5, 9]
    S1 = n * m - sum(known)
    S2 = n * (v + m ** 2) - sum(k ** 2 for k in known)
    sols = solve([a + b - S1, a ** 2 + b ** 2 - S2], [a, b], dict=True)
    prods = {simplify(s[a] * s[b]) for s in sols}
    assert len(prods) == 1
    return prods.pop()


q("U13-B-023", TOPIC, "Missing observations from mean and variance", "Medium", "Inverse/parameter MCQ",
  r"The mean and variance of $5$ observations are $6$ and $6$ respectively. Three of the observations are $2, 5$ and $9$. If the other two are $a$ and $b$, then $ab$ equals" + VN,
  r"$48$",
  [(r"$60$", r"Writes $\sum x^2 = n\bar{x}^2 + \sigma^2 = 186$, so $a^2 + b^2 = 76$ and $ab = \frac{196 - 76}{2}$."),
   (r"$51$", r"Uses divisor $n-1$: $\sum x^2 = 4 \cdot 6 + 5 \cdot 36 = 204$, so $a^2 + b^2 = 94$ and $ab = \frac{196 - 94}{2}$."),
   (r"$96$", r"Writes $ab = (a+b)^2 - (a^2+b^2) = 196 - 100$, forgetting to halve.")],
  r"$a + b = 30 - 16 = 14$ and $\sum x^2 = 5(6 + 36) = 210$, so $a^2 + b^2 = 210 - (4 + 25 + 81) = 100$. Then $2ab = 196 - 100 = 96$, so $ab = 48$ (the values are $6$ and $8$).",
  r"Rebuilding $\sum x^2$ incorrectly from the mean and variance.",
  "U13-B-missing-observations", "Two sums rebuilt, then a symmetric-function step.",
  check=_c023, values=[48, 60, 51, 96], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean and variance of $5$ observations are $6$ and $6$ respectively (variance taken with divisor $n$). Three of the observations are $2, 5$ and $9$. If the other two are $a$ and $b$, then $ab$ is", answer=48))


def _c024():
    m, n = symbols('m n', positive=True, integer=True)
    mm = [s for s in solve(Eq(4 * (m ** 2 - 1) / 12, 8), m) if s > 0]
    nn = [s for s in solve(Eq((n ** 2 - 1) / 12, 30), n) if s > 0]
    # brute-force confirmation
    assert var_([2 * k for k in range(1, mm[0] + 1)]) == 8
    assert var_(list(range(1, nn[0] + 1))) == 30
    return mm[0] + nn[0]


q("U13-B-024", TOPIC, "Variance of natural and even numbers", "Medium", "Inverse/parameter MCQ",
  r"Take the variance of any set of observations with divisor equal to the number of observations. The variance of the first $m$ even natural numbers is $8$ and the variance of the first $n$ natural numbers is $30$. Then $m + n$ equals",
  r"$24$",
  [(r"$26$", r"Scales the variance of $1, \ldots, m$ by $2$ instead of $4$: $\frac{2(m^2-1)}{12} = 8$ gives $m = 7$."),
   (r"$29$", r"Reports the largest even number $10$ in place of the count $m = 5$."),
   (r"$44$", r"Stops at $m^2 = 25$ and adds it to $n = 19$.")],
  r"First $m$ even numbers $2, 4, \ldots, 2m$ have variance $4 \cdot \frac{m^2 - 1}{12} = 8$, so $m^2 = 25$, $m = 5$. First $n$ natural numbers: $\frac{n^2 - 1}{12} = 30$, so $n^2 = 361$, $n = 19$. Hence $m + n = 24$.",
  r"Scaling the variance by the factor $2$ instead of $2^2$.",
  "U13-B-natural-even-variance", "Two inverse uses of the standard result.",
  check=_c024, values=[24, 26, 29, 44], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The variance of the first $m$ even natural numbers is $8$ and the variance of the first $n$ natural numbers is $30$ (variance taken with divisor equal to the number of observations). The value of $m + n$ is", answer=24))


def _c025():
    n = symbols('n', positive=True, integer=True)
    k = symbols('k', integer=True)
    Vn = summation(k ** 2, (k, 1, n)) / n - (summation(k, (k, 1, n)) / n) ** 2
    Ve = summation((2 * k) ** 2, (k, 1, n)) / n - (summation(2 * k, (k, 1, n)) / n) ** 2
    s1 = simplify(Vn - (n ** 2 - 1) / 12) == 0
    s2 = simplify(Ve - 2 * Vn) == 0
    return (s1, s2)


q("U13-B-025", TOPIC, "Variance of natural and even numbers", "Medium", "Statement-based MCQ",
  r"Statement I: The variance of the first $n$ natural numbers is $\frac{n^2 - 1}{12}$. Statement II: The variance of the first $n$ even natural numbers is twice the variance of the first $n$ natural numbers. (Variance is taken with divisor $n$.)" + TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II, applying the scale factor $2$ to the variance instead of $2^2$."),
   (ST_FT, r"Confuses $\frac{n^2-1}{12}$ with the sample-variance form $\frac{n(n+1)}{12}$, and also accepts the factor $2$."),
   (ST_FF, r"Rejects the standard result in Statement I and correctly rejects Statement II.")],
  r"$\frac{1}{n}\sum k^2 - \left(\frac{n+1}{2}\right)^2 = \frac{(n+1)(2n+1)}{6} - \frac{(n+1)^2}{4} = \frac{n^2-1}{12}$, so Statement I is true. The even numbers are $2k$, so their variance is $2^2 \cdot \frac{n^2-1}{12}$, four times (not twice) the first; Statement II is false.",
  r"Scaling variance by the scale factor rather than its square.",
  "U13-B-statement-natural-variance", "A derivation plus a scaling property.",
  check=_c025, values=[(True, False), (True, True), (False, True), (False, False)], cognitive="Understanding", source_class=SC)


def _c026():
    x = symbols('x', real=True)
    known = [1, 3, 5, 7]
    expr = (sum(abs(k - 5) for k in known) + (x - 5)) / 5  # median 5 when x > 7
    sol = [s for s in solve(Eq(expr, 3), x) if s > 7]
    assert len(sol) == 1
    L = known + [sol[0]]
    assert md_(L, median_(L)) == 3
    return sol[0]


q("U13-B-026", TOPIC, "Mean deviation about median with an unknown", "Medium", "Inverse/parameter MCQ",
  r"The mean deviation about the median of the observations $1, 3, 5, 7, x$, where $x > 7$, is $3$. Then $x$ equals",
  r"$12$",
  [(r"$9$", r"Divides by $n - 1 = 4$: $\frac{x + 3}{4} = 3$."),
   (r"$24$", r"Uses signed deviations: $\frac{-4 - 2 + 0 + 2 + (x - 5)}{5} = 3$."),
   (r"$11$", r"Takes the median of $1, 3, 5, 7$ alone, $4$, as the centre: $\frac{8 + (x - 4)}{5} = 3$.")],
  r"Since $x > 7$, the ordered data is $1, 3, 5, 7, x$ and the median is $5$. The absolute deviations are $4, 2, 0, 2, x - 5$, so $\frac{x + 3}{5} = 3$, giving $x = 12$.",
  r"Dropping the absolute values or misplacing the median.",
  "U13-B-md-median-inverse", "Locating the median, then solving a linear equation.",
  check=_c026, values=[12, 9, 24, 11], cognitive="Application", source_class=SC)


def _c027():
    n, m, v = 10, 8, 5
    S1 = n * m + 6 + 10
    S2 = n * (v + m ** 2) + 36 + 100
    return Rational(S2, n + 2) - Rational(S1, n + 2) ** 2


q("U13-B-027", TOPIC, "Variance after adding observations", "Medium", "Multi-step computation MCQ",
  r"The mean and variance of $10$ observations are $8$ and $5$. Two more observations, $6$ and $10$, are included. The variance of the $12$ observations is" + VN,
  r"$\frac{29}{6}$",
  [(r"$5$", r"Assumes the variance is unchanged because the mean stays $8$."),
   (r"$\frac{29}{5}$", r"Adds the new squared deviations $4 + 4$ to $50$ but still divides by $10$."),
   (r"$\frac{9}{2}$", r"Averages the old variance $5$ and the variance $4$ of the two new values.")],
  r"The new sum is $80 + 16 = 96$, so the mean is still $8$. The sum of squared deviations from $8$ becomes $10 \cdot 5 + 2^2 + 2^2 = 58$, so the variance is $\frac{58}{12} = \frac{29}{6}$.",
  r"Believing that an unchanged mean implies an unchanged variance.",
  "U13-B-add-observations", "Update sums and the count; a trap on the unchanged mean.",
  check=_c027, values=[Rational(29, 6), 5, Rational(29, 5), Rational(9, 2)], cognitive="Analysis", source_class=SC)


def _c028():
    a, b = symbols('a b', real=True)
    mx, vx, my, vy = 10, 4, 2, 16
    sols = solve([Eq(a ** 2 * vx, vy), Eq(a * mx + b, my)], [a, b], dict=True)
    sols = [s for s in sols if s[a] < 0]
    assert len(sols) == 1
    return sols[0][a] + sols[0][b]


q("U13-B-028", TOPIC, "Linear transformation with unknown constants", "Medium", "Inverse/parameter MCQ",
  r"The observations $x_i$ have mean $10$ and variance $4$. The observations $y_i = a x_i + b$, where $a < 0$, have mean $2$ and variance $16$. Then $a + b$ equals",
  r"$20$",
  [(r"$-16$", r"Takes $a = 2$, ignoring the condition $a < 0$; then $b = 2 - 20 = -18$."),
   (r"$-34$", r"Takes $a = 4$, the ratio of the variances, with positive sign; then $b = 2 - 40 = -38$."),
   (r"$38$", r"Takes $a = -4$, the ratio of variances rather than of standard deviations; then $b = 2 + 40 = 42$.")],
  r"$\sigma_y^2 = a^2 \sigma_x^2$ gives $a^2 = 4$, and $a < 0$ gives $a = -2$. Then $\bar{y} = a\bar{x} + b$ gives $2 = -20 + b$, so $b = 22$ and $a + b = 20$.",
  r"Using the variance ratio for $a$, or ignoring the sign condition.",
  "U13-B-linear-transform-inverse", "Two transformation rules used backwards, with a sign condition.",
  check=_c028, values=[20, -16, -34, 38], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The observations $x_i$ have mean $10$ and variance $4$. The observations $y_i = a x_i + b$, where $a < 0$, have mean $2$ and variance $16$. The value of $a + b$ is", answer=20))


def _c029():
    k = symbols('k', positive=True)
    xs = [2, 4, 6]
    fs = [3, k, 3]
    N = sum(fs)
    mbar = sum(x * f for x, f in zip(xs, fs)) / N
    assert simplify(mbar - 4) == 0
    md = sum(f * Abs(x - 4) for x, f in zip(xs, fs)) / N
    sol = solve(Eq(md, 1), k)
    assert len(sol) == 1
    return sol[0]


q("U13-B-029", TOPIC, "Unknown frequency from mean deviation", "Medium", "Inverse/parameter MCQ",
  r"The values $2, 4, 6$ occur with frequencies $3, k, 3$ respectively, where $k$ is a positive integer. If the mean deviation about the mean is $1$, then $k$ equals",
  r"$6$",
  [(r"$12$", r"Divides $\sum f|x - \bar{x}| = 12$ by $k$ alone instead of by $N = 6 + k$."),
   (r"$18$", r"Uses squared deviations: $\frac{3 \cdot 4 + 3 \cdot 4}{6 + k} = 1$."),
   (r"$7$", r"Divides by $N - 1 = 5 + k$: $\frac{12}{5 + k} = 1$.")],
  r"By symmetry the mean is $4$ for every $k$. Then $\sum f|x - 4| = 3 \cdot 2 + k \cdot 0 + 3 \cdot 2 = 12$, so $\frac{12}{6 + k} = 1$ and $k = 6$.",
  r"Using the wrong total frequency in the denominator.",
  "U13-B-md-unknown-frequency", "Symmetry for the mean, then an equation in $k$.",
  check=_c029, values=[6, 12, 18, 7], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The values $2, 4, 6$ occur with frequencies $3, k, 3$ respectively, where $k$ is a positive integer. If the mean deviation about the mean is $1$, then $k$ is", answer=6))


def _c030():
    L = [2, 6, 7, 9, 16]
    return md_(L, median_(L)) / md_(L, mean_(L))


q("U13-B-030", TOPIC, "Mean deviation about mean and median", "Medium", "Multi-step computation MCQ",
  r"For the observations $2, 6, 7, 9, 16$, the ratio of the mean deviation about the median to the mean deviation about the mean is",
  r"$\frac{17}{18}$",
  [(r"$\frac{18}{17}$", r"Inverts the ratio."),
   (r"$\frac{7}{8}$", r"Takes the ratio of the centres, median $7$ to mean $8$."),
   (r"$1$", r"Assumes the mean deviation is the same about any central value.")],
  r"Mean $= \frac{40}{5} = 8$, median $= 7$. About the mean: $6 + 2 + 1 + 1 + 8 = 18$; about the median: $5 + 1 + 0 + 2 + 9 = 17$. The ratio is $\frac{17/5}{18/5} = \frac{17}{18}$, consistent with the median minimising $\sum |x_i - a|$.",
  r"Treating mean deviations about different centres as equal.",
  "U13-B-md-mean-vs-median", "Two mean deviations compared.",
  check=_c030, values=[Rational(17, 18), Rational(18, 17), Rational(7, 8), 1], cognitive="Application", source_class=SC)


def _c031():
    k = symbols('k', real=True)
    L = [4] * 10 + [k] * 40
    sol = [s for s in solve(Eq(var_(L), 4), k) if s > 4]
    assert len(sol) == 1
    return sol[0]


q("U13-B-031", TOPIC, "Variance of two-valued data", "Medium", "Inverse/parameter MCQ",
  r"Of $50$ observations, $10$ are equal to $4$ and the remaining $40$ are equal to $k$, where $k > 4$. If the variance of the $50$ observations is $4$, then $k$ equals" + VN,
  r"$9$",
  [(r"$8$", r"Uses equal weights, $\frac{1}{4}(k - 4)^2 = 4$, as if the two values were equally frequent."),
   (r"$6$", r"Forgets the weight $pq = \frac{1}{5} \cdot \frac{4}{5}$ and sets $(k - 4)^2 = 4$."),
   (r"$14$", r"Treats $4$ as the standard deviation: $\frac{4}{25}(k - 4)^2 = 16$.")],
  r"With proportions $p = \frac{1}{5}$ and $q = \frac{4}{5}$ of two values $a, b$, the variance is $pq(b - a)^2$. So $\frac{4}{25}(k - 4)^2 = 4$, $(k - 4)^2 = 25$, and with $k > 4$, $k = 9$.",
  r"Ignoring unequal frequencies in two-valued data.",
  "U13-B-two-valued-data", "Recognising the $pq(b-a)^2$ structure and solving.",
  check=_c031, values=[9, 8, 6, 14], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Of $50$ observations, $10$ are equal to $4$ and the remaining $40$ are equal to $k$, where $k > 4$. If the variance of the $50$ observations (divisor $n$) is $4$, then $k$ is", answer=9))


def _c032():
    x = symbols('x', real=True)
    V = var_([2, 4, 6, 8, x])
    crit = solve(diff(V, x), x)
    assert len(crit) == 1 and diff(V, x, 2) > 0
    return simplify(V.subs(x, crit[0]))


q("U13-B-032", TOPIC, "Least possible variance", "Medium", "Multi-step computation MCQ",
  r"The observations are $2, 4, 6, 8$ and $x$, where $x$ is a real number. The least possible value of their variance is" + VN,
  r"$4$",
  [(r"$5$", r"Gives the variance of $2, 4, 6, 8$ alone, without accounting for the fifth value."),
   (r"$2$", r"Reports the least standard deviation."),
   (r"$\frac{104}{25}$", r"Takes $x = 4$, repeating a data value, instead of $x = 5$: the variance of $2, 4, 4, 6, 8$.")],
  r"The sum of squared deviations is least when $x$ equals the mean $5$ of the other four (then the overall mean is also $5$). The squared deviations are $9, 1, 1, 9, 0$, so the least variance is $\frac{20}{5} = 4$.",
  r"Forgetting that the extra value at the mean still increases $n$.",
  "U13-B-least-variance", "Optimisation of a quadratic in $x$ with an insight.",
  check=_c032, values=[4, 5, 2, Rational(104, 25)], cognitive="Analysis", source_class=SC)


def _c033():
    n, m, v = 10, 12, 4
    m2, v2 = 2 * m - 3, 4 * v
    S1 = n * m2 + m2
    S2 = n * (v2 + m2 ** 2) + m2 ** 2
    return Rational(S2, n + 1) - Rational(S1, n + 1) ** 2


q("U13-B-033", TOPIC, "Change of scale followed by an added observation", "Medium", "Multi-step computation MCQ",
  r"Ten observations have mean $12$ and variance $4$. Each observation is doubled and then $3$ is subtracted from it. An eleventh observation equal to $21$ is then included. The variance of the $11$ observations is" + VN,
  r"$\frac{160}{11}$",
  [(r"$16$", r"Notes that $21$ equals the new mean and assumes the variance stays $16$."),
   (r"$\frac{80}{11}$", r"Multiplies the variance by $2$ instead of $4$, getting $8$, then $\frac{10 \cdot 8}{11}$."),
   (r"$\frac{130}{11}$", r"Also subtracts $3$ from the variance, $16 - 3 = 13$, then $\frac{10 \cdot 13}{11}$.")],
  r"After $y = 2x - 3$: mean $21$, variance $16$, so the sum of squared deviations is $160$. The added value $21$ equals the mean, so the mean stays $21$ and the sum of squared deviations stays $160$, now over $11$ values: $\frac{160}{11}$.",
  r"Assuming a value at the mean leaves the variance unchanged.",
  "U13-B-scale-then-add", "Transformation rule plus an added observation.",
  check=_c033, values=[Rational(160, 11), 16, Rational(80, 11), Rational(130, 11)], cognitive="Analysis", source_class=SC)


def _c034():
    a = symbols('a', real=True)
    d = symbols('d', positive=True)
    L = [a + k * d for k in range(9)]
    m = mean_(L)
    md = Add(*[Abs(simplify(x - m)) for x in L]) / 9
    sol = solve(Eq(md, Rational(20, 3)), d)
    assert len(sol) == 1
    return sol[0]


q("U13-B-034", TOPIC, "Mean deviation of an arithmetic progression", "Medium", "Inverse/parameter MCQ",
  r"The mean deviation about the mean of the $9$ observations $a, a + d, a + 2d, \ldots, a + 8d$, where $d > 0$, is $\frac{20}{3}$. Then $d$ equals",
  r"$3$",
  [(r"$\frac{8}{3}$", r"Divides the total absolute deviation $20d$ by $n - 1 = 8$: $\frac{20d}{8} = \frac{20}{3}$."),
   (r"$6$", r"Adds the deviations on one side of the mean only: $\frac{(1+2+3+4)d}{9} = \frac{20}{3}$."),
   (r"$\frac{2\sqrt{15}}{3}$", r"Uses the standard deviation $d\sqrt{\frac{n^2-1}{12}} = d\sqrt{\frac{20}{3}}$ in place of the mean deviation.")],
  r"The mean is the middle term $a + 4d$. The absolute deviations are $4d, 3d, 2d, d, 0, d, 2d, 3d, 4d$, with sum $20d$. So $\frac{20d}{9} = \frac{20}{3}$, giving $d = 3$.",
  r"Counting only one side of the symmetric deviations.",
  "U13-B-md-ap", "Symmetry of an AP, then a linear equation.",
  check=_c034, values=[3, Rational(8, 3), 6, 2 * sqrt(15) / 3], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean deviation about the mean of the $9$ observations $a, a + d, a + 2d, \ldots, a + 8d$, where $d > 0$, is $\frac{20}{3}$. The value of $d$ is", answer=3))


# ================================================================ DIFFICULT (11)

def _c035():
    n, m, v = 20, 15, 9
    S1, S2 = n * m, n * (v + m ** 2)
    S1c = S1 - 21 - 9 + 12 + 18
    S2c = S2 - 21 ** 2 - 9 ** 2 + 12 ** 2 + 18 ** 2
    return Rational(S2c, n) - Rational(S1c, n) ** 2


q("U13-B-035", TOPIC, "Corrected variance with two errors", "Difficult", "Multi-step computation MCQ",
  r"The mean and variance of $20$ observations were computed as $15$ and $9$. It was later found that the value $12$ had been copied as $21$ and the value $18$ had been copied as $9$. The correct variance is" + VN,
  r"$\frac{63}{10}$",
  [(r"$9$", r"Notices that $\sum x$ is unchanged ($21 + 9 = 12 + 18$) and concludes the variance is unchanged too."),
   (r"$\frac{9}{10}$", r"Subtracts the squared copying errors $\frac{9^2 + 9^2}{20} = \frac{81}{10}$ from $9$."),
   (r"$\frac{126}{19}$", r"Finds the corrected sum of squared deviations $126$ but divides by $n - 1 = 19$.")],
  r"$\sum x$ is unchanged, so the mean stays $15$. Wrong $\sum x^2 = 20(9 + 225) = 4680$; corrected $\sum x^2 = 4680 - 441 - 81 + 144 + 324 = 4626$. So $\sigma^2 = \frac{4626}{20} - 225 = 6.3 = \frac{63}{10}$. (Equivalently the squared deviations $36 + 36$ are replaced by $9 + 9$: $\frac{180 - 54}{20}$.)",
  r"Assuming that an unchanged mean means an unchanged variance.",
  "U13-B-corrected-two-errors", "Two corrections with a trap: the sum is unchanged but the spread is not.",
  check=_c035, values=[Rational(63, 10), 9, Rational(9, 10), Rational(126, 19)], cognitive="Analysis", source_class=SC)


def _c036():
    groups = [(10, 50, 25), (20, 55, 16), (20, 60, 9)]
    N = sum(g[0] for g in groups)
    S1 = sum(n * m for n, m, v in groups)
    S2 = sum(n * (v + m ** 2) for n, m, v in groups)
    return Rational(S2, N) - Rational(S1, N) ** 2


q("U13-B-036", TOPIC, "Combined variance of three groups", "Difficult", "Multi-step computation MCQ",
  r"Three sections of a class have $10$, $20$ and $20$ students, with mean marks $50$, $55$ and $60$ and variances $25$, $16$ and $9$ respectively. The variance of the marks of all $50$ students is" + VN,
  r"$29$",
  [(r"$15$", r"Takes only the size-weighted average of the variances, $\frac{250 + 320 + 180}{50}$."),
   (r"$\frac{50}{3}$", r"Takes the simple average of the three variances."),
   (r"$14$", r"Computes only the spread of the section means about $56$, $\frac{10 \cdot 36 + 20 \cdot 1 + 20 \cdot 16}{50}$.")],
  r"Combined mean $= \frac{500 + 1100 + 1200}{50} = 56$. Within-section part: $\frac{10 \cdot 25 + 20 \cdot 16 + 20 \cdot 9}{50} = 15$. Between-section part: $\frac{10(50-56)^2 + 20(55-56)^2 + 20(60-56)^2}{50} = 14$. Total variance $= 15 + 14 = 29$.",
  r"Dropping either the within-group or the between-group part.",
  "U13-B-combined-three-groups", "Three groups, combined mean, two components.",
  check=_c036, values=[29, 15, Rational(50, 3), 14], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Three sections of a class have $10$, $20$ and $20$ students, with mean marks $50$, $55$ and $60$ and variances $25$, $16$ and $9$ respectively (variance taken with divisor $n$). The variance of the marks of all $50$ students is", answer=29))


def _c037():
    a = symbols('a', real=True)
    L = [1, 2, 3, 4, 10, 30]
    f = Add(*[Abs(x - a) for x in L]) / 6
    # piecewise linear: minimum occurs at a data point
    return Min(*[f.subs(a, x) for x in L])


q("U13-B-037", TOPIC, "Minimum property of mean deviation", "Difficult", "Multi-step computation MCQ",
  r"For the observations $1, 2, 3, 4, 10, 30$, let $S(a) = \frac{1}{6}\sum_{i=1}^{6} |x_i - a|$ for real $a$. The least value of $S(a)$ is",
  r"$\frac{19}{3}$",
  [(r"$\frac{70}{9}$", r"Evaluates $S$ at the mean $a = \frac{25}{3}$, assuming the mean minimises the mean deviation."),
   (r"$\frac{38}{5}$", r"Finds the minimum total $38$ correctly but divides by $5$ instead of $6$."),
   (r"$12$", r"Evaluates $S$ at the mid-range $a = 15.5$.")],
  r"$\sum |x_i - a|$ is least for any $a$ between the two middle values $3$ and $4$ (the median interval). At $a = 3$: $2 + 1 + 0 + 1 + 7 + 27 = 38$. So the least value of $S(a)$ is $\frac{38}{6} = \frac{19}{3}$, smaller than the value $\frac{70}{9}$ at the mean.",
  r"Believing the mean minimises the sum of absolute deviations.",
  "U13-B-md-minimum-property", "Recognising the median property with skewed data; a trap at the mean.",
  check=_c037, values=[Rational(19, 3), Rational(70, 9), Rational(38, 5), 12], cognitive="Analysis", source_class=SC)


def _c038():
    L = []
    for k in range(1, 11):
        L += [k] * k
    return var_(L)


q("U13-B-038", TOPIC, "Variance of a frequency distribution with frequency equal to value", "Difficult", "Multi-step computation MCQ",
  r"In a data set, the value $k$ occurs exactly $k$ times for each $k = 1, 2, \ldots, 10$, and no other values occur. The variance of the data set is" + VN,
  r"$6$",
  [(r"$\frac{33}{4}$", r"Ignores the frequencies and gives the variance of $1, 2, \ldots, 10$."),
   (r"$55$", r"Computes $\frac{\sum f x^2}{N} = \frac{\sum k^3}{\sum k} = \frac{3025}{55}$ and does not subtract the square of the mean."),
   (r"$\frac{99}{4}$", r"Uses the unweighted mean $\frac{11}{2}$ with the weighted mean of squares: $55 - \frac{121}{4}$.")],
  r"$N = \sum k = 55$, $\sum f x = \sum k^2 = 385$ and $\sum f x^2 = \sum k^3 = 3025$. So $\bar{x} = 7$ and the mean of squares is $55$, giving $\sigma^2 = 55 - 49 = 6$.",
  r"Mixing the unweighted mean with weighted sums.",
  "U13-B-weighted-natural-variance", "Three standard sums combined with frequency weights.",
  check=_c038, values=[6, Rational(33, 4), 55, Rational(99, 4)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"In a data set, the value $k$ occurs exactly $k$ times for each $k = 1, 2, \ldots, 10$, and no other values occur. The variance of the data set (divisor equal to the number of observations) is", answer=6))


def _c039():
    import random
    rnd = random.Random(7)
    ok1 = ok2 = True
    for _ in range(200):
        n = rnd.randint(2, 8)
        L = [Rational(rnd.randint(-20, 20)) for _ in range(n)]
        sd = sqrt(var_(L))
        ok1 = ok1 and bool(md_(L, mean_(L)) <= sd)
        ok2 = ok2 and bool(sd <= (max(L) - min(L)) / 2)
    return (ok1, ok2)


q("U13-B-039", TOPIC, "Inequalities between measures of dispersion", "Difficult", "Statement-based MCQ",
  r"Statement I: For any set of real observations, the mean deviation about the mean does not exceed the standard deviation. Statement II: For any set of real observations, the standard deviation does not exceed half the range (largest value minus smallest value). (Standard deviation uses divisor $n$.)" + TAIL,
  ST_TT,
  [(ST_FT, r"Thinks squaring deviations makes the standard deviation smaller than the mean deviation for small deviations, rejecting Statement I."),
   (ST_TF, r"Thinks a single extreme value can push the standard deviation above half the range, rejecting Statement II."),
   (ST_FF, r"Rejects both general inequalities.")],
  r"Statement I: $\left(\frac{1}{n}\sum |x_i - \bar{x}|\right)^2 \le \frac{1}{n}\sum (x_i - \bar{x})^2$ because the variance of the numbers $|x_i - \bar{x}|$ is non-negative; so mean deviation $\le \sigma$. Statement II: with $c$ the mid-range and $R$ the range, every $|x_i - c| \le \frac{R}{2}$, and $\sigma^2 \le \frac{1}{n}\sum (x_i - c)^2 \le \frac{R^2}{4}$ since the mean minimises the sum of squared deviations. Both are true.",
  r"Not knowing the standard ordering mean deviation $\le$ standard deviation $\le$ half range.",
  "U13-B-statement-dispersion-inequalities", "Two general inequalities needing short proofs.",
  check=_c039, values=[(True, True), (False, True), (True, False), (False, False)], cognitive="Analysis", source_class=SC)


def _c040():
    n, wm, wv = 10, 11, 16
    wrong, cm = 10, 12
    correct = wrong + n * (cm - wm)
    S2 = n * (wv + wm ** 2) - wrong ** 2 + correct ** 2
    S1 = n * wm - wrong + correct
    assert Rational(S1, n) == cm
    return Rational(S2, n) - Rational(S1, n) ** 2


q("U13-B-040", TOPIC, "Corrected variance with the correct value unknown", "Difficult", "Multi-step computation MCQ",
  r"For $10$ observations, the mean and variance were computed as $11$ and $16$. It was then found that one observation had been recorded as $10$ instead of its true value, and with the true value the mean is $12$. The correct variance is" + VN,
  r"$23$",
  [(r"$16$", r"Assumes correcting one value only shifts the mean and leaves the variance as it was."),
   (r"$46$", r"Corrects $\sum x^2$ to $1670$ but subtracts the old mean squared: $167 - 121$."),
   (r"$3$", r"Adds $(20 - 10)^2 = 100$ to $\sum x^2$ instead of replacing $10^2$ by $20^2$: $\frac{1470}{10} - 144$.")],
  r"The mean rises by $1$, so $\sum x$ rises by $10$ and the true value is $20$. Wrong $\sum x^2 = 10(16 + 121) = 1370$; corrected $\sum x^2 = 1370 - 100 + 400 = 1670$. Hence $\sigma^2 = 167 - 144 = 23$.",
  r"Correcting $\sum x^2$ by the square of the difference instead of the difference of squares.",
  "U13-B-corrected-replace", "Recover the true value from the mean, then correct both sums.",
  check=_c040, values=[23, 16, 46, 3], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"For $10$ observations, the mean and variance (divisor $n$) were computed as $11$ and $16$. It was then found that one observation had been recorded as $10$ instead of its true value, and with the true value the mean is $12$. The correct variance is", answer=23))


def _c041():
    x = symbols('x', positive=True)
    mids = [5, 15, 25, 35, 45]
    fs = [4, x, 8, 6, 2]
    N = sum(fs)
    sol = solve(Eq(sum(m * f for m, f in zip(mids, fs)) / N, 25), x)
    assert len(sol) == 1
    xv = sol[0]
    return var_(expand_freq(mids, [4, int(xv), 8, 6, 2]))


q("U13-B-041", TOPIC, "Grouped variance with an unknown frequency", "Difficult", "Multi-step computation MCQ",
  r"For the classes $0\text{-}10$, $10\text{-}20$, $20\text{-}30$, $30\text{-}40$, $40\text{-}50$ the frequencies are $4, x, 8, 6, 2$ respectively, and the mean (using class mid-points) is $25$. The variance of the distribution is" + VN,
  r"$\frac{1600}{11}$",
  [(r"$\frac{16}{11}$", r"Finds the variance of the step deviations $u = \frac{x - 25}{10}$ and forgets to multiply by $10^2$."),
   (r"$\frac{160}{11}$", r"Multiplies the step-deviation variance $\frac{16}{11}$ by $10$ instead of $100$."),
   (r"$\frac{3200}{21}$", r"Divides $\sum f(x - 25)^2 = 3200$ by $N - 1 = 21$.")],
  r"Mid-points $5, 15, 25, 35, 45$. $\frac{20 + 15x + 200 + 210 + 90}{20 + x} = 25$ gives $520 + 15x = 500 + 25x$, so $x = 2$ and $N = 22$. With $u = \frac{x-25}{10} \in \{-2, -1, 0, 1, 2\}$: $\sum f u = 0$, $\sum f u^2 = 16 + 2 + 0 + 6 + 8 = 32$, so $\sigma_u^2 = \frac{16}{11}$ and $\sigma^2 = 100 \cdot \frac{16}{11} = \frac{1600}{11}$.",
  r"Forgetting to rescale a step-deviation variance by $h^2$.",
  "U13-B-grouped-unknown-frequency", "Unknown frequency from the mean, then a coded variance.",
  check=_c041, values=[Rational(1600, 11), Rational(16, 11), Rational(160, 11), Rational(3200, 21)], cognitive="Analysis", source_class=SC)


def _c042():
    full = list(range(1, 12))
    ks = [k for k in full if mean_([v for v in full if v != k]) == Rational(31, 5)]
    assert len(ks) == 1
    return var_([v for v in full if v != ks[0]])


q("U13-B-042", TOPIC, "Variance after deleting one number", "Difficult", "Multi-step computation MCQ",
  r"One number is removed from $1, 2, 3, \ldots, 11$, and the mean of the remaining ten numbers is $\frac{31}{5}$. The variance of the remaining ten numbers is" + VN,
  r"$\frac{264}{25}$",
  [(r"$10$", r"Gives the variance $\frac{11^2 - 1}{12}$ of all eleven numbers."),
   (r"$13$", r"Uses the corrected $\sum x^2 = 490$ but the old mean $6$: $49 - 36$."),
   (r"$\frac{294}{25}$", r"Subtracts $4$ instead of $4^2$ from $\sum x^2$: $\frac{502}{10} - \left(\frac{31}{5}\right)^2$.")],
  r"The remaining sum is $10 \cdot \frac{31}{5} = 62$, and $1 + \cdots + 11 = 66$, so $4$ was removed. Then $\sum x^2 = 506 - 16 = 490$, and the variance is $49 - \frac{961}{25} = \frac{264}{25}$.",
  r"Not updating both the mean and the sum of squares after deletion.",
  "U13-B-delete-from-naturals", "Identify the removed number, then recompute with standard sums.",
  check=_c042, values=[Rational(264, 25), 10, 13, Rational(294, 25)], cognitive="Analysis", source_class=SC)


def _c043():
    N, M, V = 100, 50, 100
    n1, m1, v1 = 60, 54, 64
    n2 = N - n1
    S1 = N * M - n1 * m1
    S2 = N * (V + M ** 2) - n1 * (v1 + m1 ** 2)
    return Rational(S2, n2) - Rational(S1, n2) ** 2


q("U13-B-043", TOPIC, "Variance of the remaining part of a data set", "Difficult", "Multi-step computation MCQ",
  r"A set of $100$ observations has mean $50$ and variance $100$. A subset of $60$ of these observations has mean $54$ and variance $64$. The variance of the remaining $40$ observations is" + VN,
  r"$94$",
  [(r"$154$", r"Treats the total variance as a weighted average of the parts' variances only: $\frac{100 \cdot 100 - 60 \cdot 64}{40}$."),
   (r"$36$", r"Subtracts the variances: $100 - 64$."),
   (r"$136$", r"Treats the total variance as the simple average of the two parts' variances: $\frac{64 + v}{2} = 100$.")],
  r"Remaining $\sum x = 5000 - 3240 = 1760$, so their mean is $44$. Total $\sum x^2 = 100(100 + 2500) = 260000$; subset $\sum x^2 = 60(64 + 2916) = 178800$. Remaining $\sum x^2 = 81200$, so the variance is $\frac{81200}{40} - 44^2 = 2030 - 1936 = 94$.",
  r"Ignoring the between-group contribution when splitting a variance.",
  "U13-B-combined-split", "Reverse of combined variance via sums; the between-group term is a trap.",
  check=_c043, values=[94, 154, 36, 136], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"A set of $100$ observations has mean $50$ and variance $100$ (divisor $n$). A subset of $60$ of these observations has mean $54$ and variance $64$. The variance of the remaining $40$ observations is", answer=94))


def _c044():
    d = symbols('d', positive=True)
    n1, s1, n2, s2 = 30, 4, 20, 3
    N = n1 + n2
    within = Rational(n1 * s1 ** 2 + n2 * s2 ** 2, N)
    between = Rational(n1 * n2, N ** 2) * d ** 2
    sol = solve(Eq(within + between, Rational(96, 5)), d)
    assert len(sol) == 1
    return sol[0]


q("U13-B-044", TOPIC, "Difference of group means from combined variance", "Difficult", "Inverse/parameter MCQ",
  r"Two groups of $30$ and $20$ observations have standard deviations $4$ and $3$ respectively. If the variance of all $50$ observations together is $\frac{96}{5}$, then the positive difference between the two group means is" + VN,
  r"$5$",
  [(r"$2\sqrt{6}$", r"Uses the equal-size weight $\frac{1}{4}$ on the squared difference: $\frac{d^2}{4} = 6$."),
   (r"$4\sqrt{5}$", r"Omits the within-group part: $\frac{6}{25}d^2 = \frac{96}{5}$."),
   (r"$25$", r"Does not square the difference of means in the between-group term: $\frac{6}{25}d = 6$.")],
  r"$\sigma^2 = \frac{n_1\sigma_1^2 + n_2\sigma_2^2}{n_1+n_2} + \frac{n_1 n_2}{(n_1+n_2)^2}d^2$. Here the within part is $\frac{480 + 180}{50} = \frac{66}{5}$ and the weight is $\frac{600}{2500} = \frac{6}{25}$. So $\frac{6}{25}d^2 = \frac{96}{5} - \frac{66}{5} = 6$, $d^2 = 25$, $d = 5$.",
  r"Using the wrong weight on the between-group term.",
  "U13-B-combined-variance-reverse", "Combined-variance decomposition used backwards with unequal sizes.",
  check=_c044, values=[5, 2 * sqrt(6), 4 * sqrt(5), 25], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Two groups of $30$ and $20$ observations have standard deviations $4$ and $3$ respectively (divisor $n$). If the variance of all $50$ observations together is $\frac{96}{5}$, then the positive difference between the two group means is", answer=5))


def _c045():
    k = symbols('k', real=True)
    sols = solve(Eq(var_([2, 4, 6, 8, k]), 10), k)
    assert len(sols) == 2 and all(s.is_real for s in sols)
    return simplify(sum(s ** 2 for s in sols))


q("U13-B-045", TOPIC, "Unknown observation from variance", "Difficult", "Inverse/parameter MCQ",
  r"The variance of the five observations $2, 4, 6, 8, k$ is $10$, where $k$ is real. The sum of the squares of all possible values of $k$ is" + VN,
  r"$125$",
  [(r"$100$", r"Squares the sum of the roots, $10^2$, instead of finding the sum of their squares."),
   (r"$75$", r"Uses $(\alpha + \beta)^2 - 2\alpha\beta$ with $\alpha\beta = +\frac{25}{2}$, a sign slip."),
   (r"$150$", r"Reads the product of roots of $2k^2 - 20k - 25 = 0$ as $-25$, forgetting to divide by the leading coefficient $2$.")],
  r"$\bar{x} = \frac{20 + k}{5}$ and $\sum x^2 = 120 + k^2$. The condition $\frac{120 + k^2}{5} - \frac{(20 + k)^2}{25} = 10$ simplifies to $4k^2 - 40k - 50 = 0$, i.e. $2k^2 - 20k - 25 = 0$, with two real roots. Their sum is $10$ and product $-\frac{25}{2}$, so the sum of squares is $100 + 25 = 125$.",
  r"Mishandling the symmetric functions of the roots of the resulting quadratic.",
  "U13-B-unknown-observation-quadratic", "Variance condition becomes a quadratic; then symmetric functions of roots.",
  check=_c045, values=[125, 100, 75, 150], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The variance (divisor $n$) of the five observations $2, 4, 6, 8, k$ is $10$, where $k$ is real. The sum of the squares of all possible values of $k$ is", answer=125))


# move the variance convention to the front of the stem so the stem still ends naturally
for _x in QUESTIONS:
    if _x["question"].endswith(VN):
        _x["question"] = VN_FRONT + _x["question"][:-len(VN)]
