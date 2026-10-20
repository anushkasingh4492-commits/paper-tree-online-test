import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools

SC = "XI"
TOPIC = "Measures of central tendency"

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."


# ---------------------------------------------------------------- helpers
def R(x):
    return Rational(x)


def mean_list(xs):
    return Rational(sum(R(x) for x in xs), len(xs))


def median_list(xs):
    s = sorted(R(x) for x in xs)
    n = len(s)
    if n % 2:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def expand_freq(xs, fs):
    out = []
    for x, f in zip(xs, fs):
        out += [R(x)] * int(f)
    return out


def g_mean(lows, h, fs):
    """grouped mean with class marks; lows = lower limits, h = width (scalar or list)"""
    hs = h if isinstance(h, (list, tuple)) else [h] * len(lows)
    mids = [R(l) + R(w) / 2 for l, w in zip(lows, hs)]
    return sum(m * f for m, f in zip(mids, fs)) / sum(fs)


def g_median(lows, h, fs):
    hs = h if isinstance(h, (list, tuple)) else [h] * len(lows)
    N = sum(fs)
    half = R(N) / 2
    cf = 0
    for l, w, f in zip(lows, hs, fs):
        if cf + f >= half and f > 0:
            return R(l) + (half - cf) / R(f) * R(w)
        cf += f


def g_mode(lows, h, fs):
    i = max(range(len(fs)), key=lambda j: fs[j])
    f1 = R(fs[i])
    f0 = R(fs[i - 1]) if i > 0 else R(0)
    f2 = R(fs[i + 1]) if i + 1 < len(fs) else R(0)
    return R(lows[i]) + (f1 - f0) / (2 * f1 - f0 - f2) * R(h)


# ================================================================ EASY (14)

def _c001():
    return mean_list([k**2 for k in range(1, 11)])


q("U13-A-001", TOPIC, "Mean of ungrouped data", "Easy", "Single-step computation MCQ",
  r"The arithmetic mean of the squares of the first ten natural numbers, that is of $1^2, 2^2, 3^2, \ldots, 10^2$, is",
  r"$\frac{77}{2}$",
  [(r"$\frac{121}{4}$", r"Squares the mean of $1, 2, \ldots, 10$: $\left(\frac{11}{2}\right)^2 = \frac{121}{4}$, treating the mean of squares as the square of the mean."),
   (r"$\frac{11}{2}$", r"Finds the mean of $1, 2, \ldots, 10$ and never squares the data."),
   (r"$35$", r"Uses $\sum k^2 = 385$ correctly but divides by $11$ terms instead of $10$: $\frac{385}{11} = 35$.")],
  r"$\sum_{k=1}^{10} k^2 = \frac{10 \cdot 11 \cdot 21}{6} = 385$, so the mean is $\frac{385}{10} = \frac{77}{2}$.",
  r"Assuming the mean of the squares equals the square of the mean.",
  "U13-A-mean-of-squares", "One standard sum formula followed by one division.",
  check=_c001, values=[Rational(77, 2), Rational(121, 4), Rational(11, 2), 35], cognitive="Application", source_class=SC)


def _c002():
    return median_list(expand_freq([1, 2, 3, 4, 5, 6], [3, 5, 7, 6, 4, 5]))


q("U13-A-002", TOPIC, "Median of a discrete frequency distribution", "Easy", "Single-step computation MCQ",
  r"For the frequency distribution below, the median is (when the number of observations is even, take the median as the mean of the two middle observations)" "\n\n"
  r"$x_i$: $1, 2, 3, 4, 5, 6$ with frequencies $f_i$: $3, 5, 7, 6, 4, 5$ respectively.",
  r"$\frac{7}{2}$",
  [(r"$3$", r"Takes only the $\frac{N}{2} = 15$th observation, which is $3$, ignoring that $N = 30$ is even so the $16$th observation must be averaged in."),
   (r"$4$", r"Takes only the $16$th observation (or rounds $\frac{N+1}{2} = 15.5$ up to $16$)."),
   (r"$\frac{18}{5}$", r"Computes the mean $\frac{\sum f_i x_i}{N} = \frac{108}{30} = \frac{18}{5}$ in place of the median.")],
  r"$N = 30$ is even, so the median is the average of the $15$th and $16$th observations. The cumulative frequencies are $3, 8, 15, 21, 25, 30$, so the $15$th observation is $3$ and the $16$th is $4$. Median $= \frac{3+4}{2} = \frac{7}{2}$.",
  r"Using a single middle position when the number of observations is even.",
  "U13-A-median-discrete-even", "Cumulative frequencies and the even-$N$ rule, two short steps.",
  check=_c002, values=[Rational(7, 2), 3, 4, Rational(18, 5)], cognitive="Application", source_class=SC)


def _c003():
    x = symbols('x1:11')
    m = Rational(15)
    # take a concrete dataset with mean 15 and apply the transformation
    data = [15 + d for d in (-5, -3, -1, 0, 0, 1, 2, 2, 1, 3)]
    assert mean_list(data) == m
    return mean_list([3 * v - 4 for v in data])


q("U13-A-003", TOPIC, "Effect of change of origin and scale on mean", "Easy", "Single-step computation MCQ",
  r"The mean of $10$ observations is $15$. If each observation is multiplied by $3$ and then $4$ is subtracted from the result, the mean of the new observations is",
  r"$41$",
  [(r"$45$", r"Applies the multiplication by $3$ but not the subtraction of $4$."),
   (r"$33$", r"Subtracts $4$ before multiplying: $3(15 - 4) = 33$, reversing the order of operations."),
   (r"$49$", r"Adds $4$ in place of subtracting it: $3 \cdot 15 + 4 = 49$ (sign slip).")],
  r"If $y_i = 3x_i - 4$, then $\bar{y} = 3\bar{x} - 4 = 3(15) - 4 = 41$.",
  r"Applying only part of a linear transformation to the mean, or in the wrong order.",
  "U13-A-mean-linear-transform", "Single rule $\\bar{y} = a\\bar{x} + b$ applied once.",
  check=_c003, values=[41, 45, 33, 49], cognitive="Application", source_class=SC)


def _c004():
    n = 10
    S = symbols('S')
    s = solve(Eq(S - 5 * n, 30), S)[0]
    return Rational(s, n)


q("U13-A-004", TOPIC, "Sum of deviations and mean", "Easy", "Single-step computation MCQ",
  r"For ten observations $x_1, x_2, \ldots, x_{10}$, it is given that $\sum_{i=1}^{10} (x_i - 5) = 30$. The mean of these observations is",
  r"$8$",
  [(r"$3$", r"Divides $30$ by $10$ and stops, giving the mean of the deviations $x_i - 5$, not of $x_i$."),
   (r"$35$", r"Adds $5$ to $30$ directly: treats $\sum (x_i - 5) = \sum x_i - 5$, subtracting $5$ only once."),
   (r"$2$", r"Subtracts in the wrong direction: $5 - \frac{30}{10} = 2$.")],
  r"$\sum (x_i - 5) = \sum x_i - 50 = 30$, so $\sum x_i = 80$ and the mean is $\frac{80}{10} = 8$. Equivalently, mean $= 5 + \frac{30}{10}$.",
  r"Forgetting that the constant is subtracted from every observation.",
  "U13-A-deviation-sum-mean", "One identity $\\sum(x_i - a) = \\sum x_i - na$.",
  check=_c004, values=[8, 3, 35, 2], cognitive="Understanding", source_class=SC,
  numerical=dict(question=r"For ten observations $x_1, x_2, \ldots, x_{10}$, it is given that $\sum_{i=1}^{10} (x_i - 5) = 30$. The mean of these observations is", answer=8))


def _c005():
    ns = [10, 20, 30]; ms = [12, 15, 20]
    return Rational(sum(n * m for n, m in zip(ns, ms)), sum(ns))


q("U13-A-005", TOPIC, "Combined mean of several groups", "Easy", "Single-step computation MCQ",
  r"Three sections of a class have $10$, $20$ and $30$ students, and their mean scores in a test are $12$, $15$ and $20$ respectively. The mean score of all $60$ students together is",
  r"$17$",
  [(r"$\frac{47}{3}$", r"Takes the simple average of the three section means, $\frac{12+15+20}{3}$, ignoring the section sizes."),
   (r"$\frac{43}{3}$", r"Pairs the sizes with the means in reverse order: $\frac{30 \cdot 12 + 20 \cdot 15 + 10 \cdot 20}{60} = \frac{860}{60}$."),
   (r"$15$", r"Takes the mean of the middle section as representative of the whole class.")],
  r"Total score $= 10(12) + 20(15) + 30(20) = 120 + 300 + 600 = 1020$, so the combined mean is $\frac{1020}{60} = 17$.",
  r"Averaging group means without weighting by group sizes.",
  "U13-A-combined-mean-direct", "Direct weighted average, one computation.",
  check=_c005, values=[17, Rational(47, 3), Rational(43, 3), 15], cognitive="Application", source_class=SC,
  numerical=dict(question=r"Three sections of a class have $10$, $20$ and $30$ students, and their mean scores in a test are $12$, $15$ and $20$ respectively. The mean score of all $60$ students together is", answer=17))


def _c006():
    return g_mode([10, 20, 30, 40, 50], 10, [5, 8, 12, 6, 4])


q("U13-A-006", TOPIC, "Mode of grouped data", "Easy", "Single-step computation MCQ",
  r"The mode of the following grouped frequency distribution is" "\n\n"
  r"Classes: $10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50, 50\text{-}60$ with frequencies $5, 8, 12, 6, 4$ respectively.",
  r"$34$",
  [(r"$36$", r"Uses $f_1 - f_2 = 6$ in the numerator of the mode formula: $30 + \frac{6}{10} \cdot 10 = 36$."),
   (r"$35$", r"Takes the class mark of the modal class as the mode."),
   (r"$\frac{110}{3}$", r"Uses $\frac{f_1 - f_0}{f_1 - f_2}$ in place of $\frac{f_1 - f_0}{2f_1 - f_0 - f_2}$: $30 + \frac{4}{6} \cdot 10 = \frac{110}{3}$.")],
  r"The modal class is $30\text{-}40$ with $l = 30$, $f_1 = 12$, $f_0 = 8$, $f_2 = 6$, $h = 10$. Mode $= l + \frac{f_1 - f_0}{2f_1 - f_0 - f_2} h = 30 + \frac{4}{24 - 14} \cdot 10 = 34$.",
  r"Mixing up $f_0$ and $f_2$ in the grouped mode formula.",
  "U13-A-grouped-mode-direct", "Direct use of the mode formula.",
  check=_c006, values=[34, 36, 35, Rational(110, 3)], cognitive="Application", source_class=SC)


def _c007():
    return g_median([0, 10, 20, 30, 40], 10, [4, 6, 10, 7, 3])


q("U13-A-007", TOPIC, "Median of grouped data", "Easy", "Single-step computation MCQ",
  r"The median of the following grouped frequency distribution is" "\n\n"
  r"Classes: $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ with frequencies $4, 6, 10, 7, 3$ respectively.",
  r"$25$",
  [(r"$15$", r"Uses the cumulative frequency up to and including the median class ($20$) as $cf$: $20 + \frac{15 - 20}{10} \cdot 10 = 15$."),
   (r"$\frac{51}{2}$", r"Uses $\frac{N+1}{2} = 15.5$ in place of $\frac{N}{2} = 15$: $20 + \frac{5.5}{10} \cdot 10$."),
   (r"$\frac{85}{3}$", r"Uses the frequency $6$ of the preceding class as $f$: $20 + \frac{5}{6} \cdot 10 = \frac{85}{3}$.")],
  r"$N = 30$, $\frac{N}{2} = 15$. Cumulative frequencies: $4, 10, 20, 27, 30$, so the median class is $20\text{-}30$ with $cf = 10$, $f = 10$. Median $= 20 + \frac{15 - 10}{10} \cdot 10 = 25$.",
  r"Using the wrong cumulative frequency in the grouped median formula.",
  "U13-A-grouped-median-direct", "Direct use of the median formula after one cumulative table.",
  check=_c007, values=[25, 15, Rational(51, 2), Rational(85, 3)], cognitive="Application", source_class=SC)


def _c008():
    return g_mean([0, 10, 20, 30, 40], 10, [3, 5, 8, 3, 1])


q("U13-A-008", TOPIC, "Mean of grouped data", "Easy", "Single-step computation MCQ",
  r"The mean of the following grouped frequency distribution is" "\n\n"
  r"Classes: $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ with frequencies $3, 5, 8, 3, 1$ respectively.",
  r"$22$",
  [(r"$17$", r"Uses the lower class limits $0, 10, 20, 30, 40$ in place of the class marks."),
   (r"$27$", r"Uses the upper class limits $10, 20, 30, 40, 50$ in place of the class marks."),
   (r"$88$", r"Divides $\sum f_i x_i = 440$ by the number of classes, $5$, not by $N = 20$.")],
  r"Class marks are $5, 15, 25, 35, 45$. $\sum f_i x_i = 15 + 75 + 200 + 105 + 45 = 440$ and $N = 20$, so the mean is $\frac{440}{20} = 22$.",
  r"Using class limits rather than class marks for grouped data.",
  "U13-A-grouped-mean-direct", "Direct computation with class marks.",
  check=_c008, values=[22, 17, 27, 88], cognitive="Application", source_class=SC,
  numerical=dict(question=r"For the grouped distribution with classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ and frequencies $3, 5, 8, 3, 1$ respectively, the mean is", answer=22))


def _c009():
    k = symbols('k', positive=True)
    xs = [1, 2, 3, 4, 5]; fs = [2, 8, 3, 2, k]
    return solve(Eq(sum(x * f for x, f in zip(xs, fs)), 3 * sum(fs)), k)[0]


q("U13-A-009", TOPIC, "Missing frequency from the mean", "Easy", "Inverse/parameter MCQ",
  r"The values $1, 2, 3, 4, 5$ occur with frequencies $2, 8, 3, 2, k$ respectively. If the mean of the distribution is $3$, then $k$ equals",
  r"$5$",
  [(r"$2$", r"Leaves $k$ out of $N$: solves $35 + 5k = 3 \cdot 15$."),
   (r"$10$", r"Writes $\sum f_i(x_i - 3) = -4 - 8 + 0 + 2 + 2k = 0$ but drops the factor $2$ on $k$, solving $-10 + k = 0$."),
   (r"$7$", r"Takes the deviation term for $x = 4$ with the wrong sign: $-4 - 8 - 2 + 2k = 0$ gives $k = 7$.")],
  r"$\sum f_i x_i = 2 + 16 + 9 + 8 + 5k = 35 + 5k$ and $N = 15 + k$. Setting $35 + 5k = 3(15 + k)$ gives $2k = 10$, so $k = 5$.",
  r"Forgetting that the unknown frequency also enters the total $N$.",
  "U13-A-missing-freq-mean-discrete", "One linear equation from the definition of mean.",
  check=_c009, values=[5, 2, 10, 7], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The values $1, 2, 3, 4, 5$ occur with frequencies $2, 8, 3, 2, k$ respectively. If the mean of the distribution is $3$, then $k$ is", answer=5))


def _c010():
    return mean_list([2**j for j in range(10)])


q("U13-A-010", TOPIC, "Mean of ungrouped data", "Easy", "Single-step computation MCQ",
  r"The mean of the ten observations $1, 2, 2^2, 2^3, \ldots, 2^9$ is",
  r"$\frac{1023}{10}$",
  [(r"$\frac{512}{5}$", r"Takes the sum as $2^{10} = 1024$, forgetting the $-1$ in $2^{10} - 1$."),
   (r"$\frac{341}{3}$", r"Counts only $9$ observations because the last exponent is $9$: $\frac{1023}{9} = \frac{341}{3}$."),
   (r"$\frac{2047}{10}$", r"Uses the sum formula with one extra term, $2^{11} - 1$.")],
  r"The sum is a geometric series: $1 + 2 + \cdots + 2^9 = 2^{10} - 1 = 1023$. There are $10$ observations, so the mean is $\frac{1023}{10}$.",
  r"Miscounting terms in a GP whose exponents start at $0$.",
  "U13-A-mean-gp-data", "One GP sum and one division.",
  check=_c010, values=[Rational(1023, 10), Rational(512, 5), Rational(341, 3), Rational(2047, 10)], cognitive="Application", source_class=SC)


def _c011():
    mo = symbols('mo')
    return solve(Eq(mo, 3 * 28 - 2 * 30), mo)[0]


q("U13-A-011", TOPIC, "Empirical relation between mean, median and mode", "Easy", "Single-step computation MCQ",
  r"For a moderately skewed distribution the mean is $30$ and the median is $28$. Using the empirical relation between mean, median and mode, the mode is",
  r"$24$",
  [(r"$34$", r"Swaps the roles of mean and median: $3(30) - 2(28) = 34$."),
   (r"$26$", r"Treats the median as the midpoint of mean and mode: $2(28) - 30 = 26$."),
   (r"$32$", r"Treats the mean as the midpoint of median and mode: $2(30) - 28 = 32$.")],
  r"The empirical relation is Mode $= 3\,$Median $- 2\,$Mean $= 3(28) - 2(30) = 84 - 60 = 24$.",
  r"Misremembering the coefficients in Mode $= 3\,$Median $- 2\,$Mean.",
  "U13-A-empirical-relation", "Recall of one relation and one substitution.",
  check=_c011, values=[24, 34, 26, 32], cognitive="Recall", source_class=SC,
  numerical=dict(question=r"For a moderately skewed distribution the mean is $30$ and the median is $28$. Using the empirical relation between mean, median and mode, the mode is", answer=24))


def _c012():
    return median_list(list(primerange(2, 30)))


q("U13-A-012", TOPIC, "Median of ungrouped data", "Easy", "Single-step computation MCQ",
  r"The median of the first ten prime numbers is",
  r"$12$",
  [(r"$11$", r"Takes the $5$th prime alone as the middle value, overlooking that $10$ is even."),
   (r"$13$", r"Takes the $6$th prime alone as the middle value."),
   (r"$\frac{129}{10}$", r"Computes the mean $\frac{2+3+5+7+11+13+17+19+23+29}{10}$ in place of the median.")],
  r"The first ten primes are $2, 3, 5, 7, 11, 13, 17, 19, 23, 29$. With $10$ values the median is the average of the $5$th and $6$th: $\frac{11 + 13}{2} = 12$.",
  r"Picking one middle value when the count is even.",
  "U13-A-median-primes", "List the data and apply the even-count rule.",
  check=_c012, values=[12, 11, 13, Rational(129, 10)], cognitive="Application", source_class=SC)


def _c013():
    data = [3, 7, 9, 12, 15, 20, 24]
    assert median_list(data) == 12
    return median_list([-2 * v + 5 for v in data])


q("U13-A-013", TOPIC, "Effect of change of origin and scale on median", "Easy", "Single-step computation MCQ",
  r"The median of seven observations $x_1, x_2, \ldots, x_7$ is $12$. If each observation is replaced by $-2x_i + 5$, the median of the new observations is",
  r"$-19$",
  [(r"$29$", r"Ignores the negative sign of the multiplier: $2(12) + 5$."),
   (r"$-34$", r"Adds $5$ before multiplying: $-2(12 + 5) = -34$."),
   (r"$19$", r"Gets $-24 + 5$ but drops the sign of the result.")],
  r"A linear map $y = -2x + 5$ reverses the order of the data but keeps the middle observation in the middle, so the new median is $-2(12) + 5 = -19$.",
  r"Believing a negative multiplier changes which observation is in the middle, or mishandling the order of operations.",
  "U13-A-median-linear-transform", "One rule for medians under $y = ax + b$.",
  check=_c013, values=[-19, 29, -34, 19], cognitive="Application", source_class=SC)


def _c014():
    x = symbols('x')
    xv = solve(Eq((5 + 8 + x + 11 + 12 + 7) / Integer(6), 9), x)[0]
    return median_list([5, 8, xv, 11, 12, 7])


q("U13-A-014", TOPIC, "Mean and median of ungrouped data", "Easy", "Multi-step computation MCQ",
  r"The mean of the six observations $5, 8, x, 11, 12, 7$ is $9$. The median of these observations is",
  r"$\frac{19}{2}$",
  [(r"$11$", r"Averages the 3rd and 4th observations in the order written ($x$ and $11$) without arranging the data."),
   (r"$8$", r"Drops $x$ and takes the median of the remaining five values."),
   (r"$9$", r"Assumes the median equals the mean.")],
  r"$43 + x = 54$ gives $x = 11$. Arranged: $5, 7, 8, 11, 11, 12$. The median is $\frac{8 + 11}{2} = \frac{19}{2}$.",
  r"Taking the median without first arranging the data.",
  "U13-A-mean-then-median", "Find $x$ from the mean, then sort and take the median.",
  check=_c014, values=[Rational(19, 2), 11, 8, 9], cognitive="Application", source_class=SC)


# ================================================================ MEDIUM (21)

def _c015():
    n, m = 30, 50
    S = n * m - 28 - 54 + 82 + 45
    return Rational(S, n)


q("U13-A-015", TOPIC, "Corrected mean", "Medium", "Multi-step computation MCQ",
  r"The mean of $30$ observations was found to be $50$. Later it was discovered that the observation $82$ had been recorded as $28$ and the observation $45$ had been recorded as $54$. The correct mean is",
  r"$\frac{103}{2}$",
  [(r"$\frac{97}{2}$", r"Applies both corrections in the opposite direction: $1500 - 54 + 9 = 1455$."),
   (r"$\frac{259}{5}$", r"Corrects only the first entry: $\frac{1500 + 54}{30}$."),
   (r"$\frac{497}{10}$", r"Corrects only the second entry: $\frac{1500 - 9}{30}$.")],
  r"Recorded sum $= 30 \cdot 50 = 1500$. Correct sum $= 1500 - 28 - 54 + 82 + 45 = 1545$. Correct mean $= \frac{1545}{30} = \frac{103}{2}$.",
  r"Reversing the direction of a correction or correcting only one entry.",
  "U13-A-corrected-mean", "Two corrections with opposite effects on the sum.",
  check=_c015, values=[Rational(103, 2), Rational(97, 2), Rational(259, 5), Rational(497, 10)], cognitive="Application", source_class=SC)


def _c016():
    d = symbols('d')
    return solve(Eq(20 * 15 - d, 19 * 14), d)[0]


q("U13-A-016", TOPIC, "Mean after deleting an observation", "Medium", "Inverse/parameter MCQ",
  r"The mean of $20$ observations is $15$. When one observation is deleted, the mean of the remaining observations becomes $14$. The deleted observation is",
  r"$34$",
  [(r"$20$", r"Keeps $20$ in the new count: $300 - 20 \cdot 14 = 20$."),
   (r"$35$", r"Uses the shortcut deleted value $= $ old mean $+ n \times$ drop with $n = 20$ in place of $n - 1 = 19$: $15 + 20$."),
   (r"$1$", r"Takes the drop in the mean, $15 - 14$, as the deleted value.")],
  r"Original sum $= 20 \cdot 15 = 300$. New sum $= 19 \cdot 14 = 266$. The deleted observation is $300 - 266 = 34$.",
  r"Not reducing the number of observations after deletion.",
  "U13-A-deleted-observation", "Two totals and a difference with a changed count.",
  check=_c016, values=[34, 20, 35, 1], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean of $20$ observations is $15$. When one observation is deleted, the mean of the remaining observations becomes $14$. The deleted observation is", answer=34))


def _c017():
    g = symbols('g')
    return solve(Eq(20 * 68 + 30 * g, 50 * 62), g)[0]


q("U13-A-017", TOPIC, "Combined mean with an unknown group mean", "Medium", "Inverse/parameter MCQ",
  r"In a class of $50$ students the mean mark is $62$. The $20$ boys in the class have a mean mark of $68$. The mean mark of the girls is",
  r"$58$",
  [(r"$56$", r"Treats $62$ as the simple average of the two group means: $2(62) - 68 = 56$."),
   (r"$53$", r"Gives $30$ students the mean $68$: $\frac{3100 - 30 \cdot 68}{20} = 53$."),
   (r"$\frac{174}{5}$", r"Finds the girls' total $1740$ but divides by all $50$ students.")],
  r"Total $= 50 \cdot 62 = 3100$; boys' total $= 20 \cdot 68 = 1360$. The $30$ girls have total $1740$, so their mean is $\frac{1740}{30} = 58$.",
  r"Treating the combined mean as an unweighted average of group means.",
  "U13-A-combined-mean-reverse", "Reverse use of the combined mean formula, two steps.",
  check=_c017, values=[58, 56, 53, Rational(174, 5)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"In a class of $50$ students the mean mark is $62$. The $20$ boys in the class have a mean mark of $68$. The mean mark of the girls is", answer=58))


def _c018():
    b, g = symbols('b g', positive=True)
    r = symbols('r', positive=True)
    s = solve(Eq(52 * r + 42, 48 * (r + 1)), r)
    return s[0]


q("U13-A-018", TOPIC, "Ratio of group sizes from means", "Medium", "Inverse/parameter MCQ",
  r"The mean score of the boys in a class is $52$, of the girls is $42$, and of the whole class is $48$. The ratio of the number of boys to the number of girls is",
  r"$3:2$",
  [(r"$2:3$", r"Matches the gap $52 - 48 = 4$ with the boys and $48 - 42 = 6$ with the girls, inverting the ratio."),
   (r"$26:21$", r"Takes the ratio of the two group means, $52:42$."),
   (r"$3:5$", r"Gets $\frac{48 - 42}{52 - 42} = \frac{6}{10}$, which is the fraction of boys in the class, and writes it as the boys to girls ratio.")],
  r"Let the ratio be $r = b:g$. Then $\frac{52b + 42g}{b + g} = 48$ gives $4b = 6g$, so $b : g = 6 : 4 = 3 : 2$.",
  r"Inverting the distance-to-mean ratio, or confusing a part-to-whole fraction with a part-to-part ratio.",
  "U13-A-combined-mean-ratio", "Set up the weighted mean and solve for a ratio; a classic inversion trap.",
  check=_c018, values=[Rational(3, 2), Rational(2, 3), Rational(26, 21), Rational(3, 5)], cognitive="Application", source_class=SC)


def _c019():
    k = symbols('k', positive=True)
    fs = [4, 5, 8, 7, k]
    mids = [10, 30, 50, 70, 90]
    return solve(Eq(sum(f * m for f, m in zip(fs, mids)), 60 * sum(fs)), k)[0]


q("U13-A-019", TOPIC, "Missing frequency in grouped data from the mean", "Medium", "Inverse/parameter MCQ",
  r"The classes $0\text{-}20, 20\text{-}40, 40\text{-}60, 60\text{-}80, 80\text{-}100$ have frequencies $4, 5, 8, 7, k$ respectively. If the mean of the distribution is $60$, then $k$ equals",
  r"$12$",
  [(r"$4$", r"Leaves $k$ out of $N$: solves $1080 + 90k = 60 \cdot 24$."),
   (r"$30$", r"Uses the lower class limits $0, 20, 40, 60, 80$ in place of the class marks."),
   (r"$3$", r"Uses the upper class limits $20, 40, 60, 80, 100$ in place of the class marks.")],
  r"Class marks $10, 30, 50, 70, 90$ give $\sum f_i x_i = 40 + 150 + 400 + 490 + 90k = 1080 + 90k$ and $N = 24 + k$. Setting $1080 + 90k = 60(24 + k)$ gives $30k = 360$, so $k = 12$.",
  r"Using class limits for grouped data, or leaving the unknown out of $N$.",
  "U13-A-missing-freq-mean-grouped", "Class marks, a sum and a linear equation.",
  check=_c019, values=[12, 4, 30, 3], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The classes $0\text{-}20, 20\text{-}40, 40\text{-}60, 60\text{-}80, 80\text{-}100$ have frequencies $4, 5, 8, 7, k$ respectively. If the mean of the distribution is $60$, then $k$ is", answer=12))


def _c020():
    a, b = symbols('a b', positive=True)
    sol = solve([Eq(4 + a + 12 + b + 6, 40), Eq(20 + (20 - (4 + a)) * Rational(10, 12), 25)], [a, b], dict=True)[0]
    assert g_median([0, 10, 20, 30, 40], 10, [4, sol[a], 12, sol[b], 6]) == 25
    return (sol[a], sol[b])


q("U13-A-020", TOPIC, "Missing frequencies from the median", "Medium", "Inverse/parameter MCQ",
  r"The classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ have frequencies $4, a, 12, b, 6$ respectively, and the total frequency is $40$. If the median of the distribution is $25$, then $(a, b)$ equals",
  r"$(10, 8)$",
  [(r"$(8, 10)$", r"Solves correctly but interchanges the two unknowns when reporting."),
   (r"$(14, 4)$", r"Takes $cf = a$ for the median class, omitting the first class frequency $4$: $20 + \frac{20 - a}{12} \cdot 10 = 25$."),
   (r"$(10, 14)$", r"Finds $a = 10$ but then $b = 40 - (4 + 10 + 12)$, leaving out the last class frequency $6$.")],
  r"Median $25$ lies in $20\text{-}30$ with $cf = 4 + a$, $f = 12$, $\frac{N}{2} = 20$. So $20 + \frac{20 - 4 - a}{12} \cdot 10 = 25$, giving $16 - a = 6$, $a = 10$. Then $b = 40 - 4 - 10 - 12 - 6 = 8$.",
  r"Using an incomplete cumulative frequency before the median class.",
  "U13-A-missing-freq-median", "Median formula plus the total, two unknowns.",
  check=_c020, values=[(10, 8), (8, 10), (14, 4), (10, 14)], cognitive="Application", source_class=SC)


def _c021():
    k = symbols('k', positive=True)
    sols = solve(Eq(20 + (k - 6) * 10 / (2 * k - 6 - 3), 24), k)
    kv = [s for s in sols if s > 6][0]
    assert g_mode([0, 10, 20, 30, 40], 10, [5, 6, kv, 3, 2]) == 24
    return kv


q("U13-A-021", TOPIC, "Missing frequency from the mode", "Medium", "Inverse/parameter MCQ",
  r"The classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ have frequencies $5, 6, k, 3, 2$ respectively. If the mode of the distribution is $24$, then $k$ equals",
  r"$12$",
  [(r"$8$", r"Writes the denominator as $(f_1 - f_0) + f_2$ in place of $(f_1 - f_0) + (f_1 - f_2)$: $\frac{k - 6}{k - 3} \cdot 10 = 4$."),
   (r"$10$", r"Uses $f_1$ alone as the denominator: $\frac{k - 6}{k} \cdot 10 = 4$."),
   (r"$18$", r"Drops $f_2$ from the denominator, using $2f_1 - f_0$: $\frac{k - 6}{2k - 6} \cdot 10 = 4$.")],
  r"Mode $24$ lies in $20\text{-}30$, so $f_1 = k$, $f_0 = 6$, $f_2 = 3$. Then $20 + \frac{k - 6}{2k - 9} \cdot 10 = 24$ gives $10k - 60 = 8k - 36$, so $k = 12$ (which indeed exceeds $6$ and $3$).",
  r"Misremembering the denominator $2f_1 - f_0 - f_2$ of the mode formula.",
  "U13-A-missing-freq-mode", "Mode formula with an unknown, solve a linear equation.",
  check=_c021, values=[12, 8, 10, 18], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ have frequencies $5, 6, k, 3, 2$ respectively. If the mode of the distribution is $24$, then $k$ is", answer=12))


def _c022():
    data = [10, 12, 14, 16, 18, 22, 25, 28, 35]
    assert mean_list(data) == 20 and median_list(data) == 18
    s = sorted(data)
    new = s[:5] + [v + 5 for v in s[5:]]
    return (mean_list(new), median_list(new))


q("U13-A-022", TOPIC, "Effect of changing some observations", "Medium", "Multi-step computation MCQ",
  r"Nine observations have mean $20$ and median $18$. If each of the four largest observations is increased by $5$, the new mean and the new median are respectively",
  r"$\frac{200}{9}$ and $18$",
  [(r"$25$ and $23$", r"Adds $5$ to both measures as though every observation had been increased."),
   (r"$\frac{200}{9}$ and $\frac{182}{9}$", r"Finds the new mean correctly but shifts the median by the same $\frac{20}{9}$."),
   (r"$25$ and $18$", r"Keeps the median but adds the full $5$ to the mean.")],
  r"The sum rises by $4 \cdot 5 = 20$, so the new mean is $\frac{180 + 20}{9} = \frac{200}{9}$. The median is the $5$th observation in order; only the $6$th to $9$th are increased and they stay above it, so the median stays $18$.",
  r"Assuming any change in the data shifts mean and median equally.",
  "U13-A-partial-change-mean-median", "Two measures, each reacting differently to the change.",
  check=_c022, values=[(Rational(200, 9), 18), (25, 23), (Rational(200, 9), Rational(182, 9)), (25, 18)], cognitive="Understanding", source_class=SC)


def _c023():
    n, S = symbols('n S', positive=True)
    sol = solve([Eq(S - 2 * n, 110), Eq(S - 5 * n, 20)], [n, S], dict=True)[0]
    return sol[S] / sol[n]


q("U13-A-023", TOPIC, "Mean from sums of deviations", "Medium", "Multi-step computation MCQ",
  r"For $n$ observations $x_1, x_2, \ldots, x_n$, it is given that $\sum_{i=1}^{n} (x_i - 2) = 110$ and $\sum_{i=1}^{n} (x_i - 5) = 20$. The mean of the observations is",
  r"$\frac{17}{3}$",
  [(r"$\frac{11}{3}$", r"Finds $n = 30$ but reports $\frac{110}{30}$, the mean of $x_i - 2$, forgetting to add $2$."),
   (r"$\frac{2}{3}$", r"Finds $n = 30$ but reports $\frac{20}{30}$, the mean of $x_i - 5$, forgetting to add $5$."),
   (r"$\frac{13}{3}$", r"Adds the two given sums and divides by $n$: $\frac{110 + 20}{30}$.")],
  r"Subtracting, $3n = 90$, so $n = 30$. Then $\sum x_i = 110 + 2 \cdot 30 = 170$, and the mean is $\frac{170}{30} = \frac{17}{3}$ (check: $5 + \frac{20}{30} = \frac{17}{3}$).",
  r"Reporting the mean of the deviations as the mean of the data.",
  "U13-A-deviation-sums-two", "Two equations to find $n$ and then the mean.",
  check=_c023, values=[Rational(17, 3), Rational(11, 3), Rational(2, 3), Rational(13, 3)], cognitive="Application", source_class=SC)


def _c024():
    return median_list([binomial(10, r) for r in range(11)])


q("U13-A-024", TOPIC, "Median of ungrouped data", "Medium", "Multi-step computation MCQ",
  r"The median of the eleven numbers $\binom{10}{0}, \binom{10}{1}, \binom{10}{2}, \ldots, \binom{10}{10}$ is",
  r"$45$",
  [(r"$252$", r"Takes the middle term $\binom{10}{5}$ in the order written, without arranging the numbers by size."),
   (r"$\frac{1024}{11}$", r"Computes the mean $\frac{2^{10}}{11}$ in place of the median."),
   (r"$\frac{165}{2}$", r"Takes the median of the six distinct values $1, 10, 45, 120, 210, 252$, ignoring repetitions: $\frac{45 + 120}{2}$.")],
  r"Arranged in increasing order the numbers are $1, 1, 10, 10, 45, 45, 120, 120, 210, 210, 252$. The $6$th of these $11$ values is $45$, so the median is $45$.",
  r"Taking the middle term in the given order rather than in sorted order.",
  "U13-A-median-binomial-coeffs", "Requires sorting a symmetric list with repeats; tempting middle term.",
  check=_c024, values=[45, 252, Rational(1024, 11), Rational(165, 2)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The median of the eleven numbers $\binom{10}{0}, \binom{10}{1}, \binom{10}{2}, \ldots, \binom{10}{10}$ is", answer=45))


def _c025():
    data = expand_freq(range(1, 21), range(1, 21))
    return mean_list(data)


q("U13-A-025", TOPIC, "Mean of a frequency distribution", "Medium", "Multi-step computation MCQ",
  r"In a data set, each natural number $k$ with $1 \le k \le 20$ occurs exactly $k$ times (so $1$ occurs once, $2$ occurs twice, and so on). The mean of the data set is",
  r"$\frac{41}{3}$",
  [(r"$\frac{21}{2}$", r"Ignores the frequencies and takes the mean of $1, 2, \ldots, 20$."),
   (r"$\frac{287}{2}$", r"Uses the correct $\sum k^2 = 2870$ but divides by $20$ in place of $\sum k = 210$."),
   (r"$\frac{82}{3}$", r"Uses $\sum k^2 = \frac{n(n+1)(2n+1)}{3}$ (wrong denominator), doubling the mean.")],
  r"$\sum f_k x_k = \sum k^2 = \frac{20 \cdot 21 \cdot 41}{6} = 2870$ and $N = \sum k = 210$. Mean $= \frac{2870}{210} = \frac{41}{3}$.",
  r"Dividing by the number of distinct values instead of the total frequency.",
  "U13-A-weighted-mean-k-times", "Two standard sums and a ratio.",
  check=_c025, values=[Rational(41, 3), Rational(21, 2), Rational(287, 2), Rational(82, 3)], cognitive="Application", source_class=SC)


def _c026():
    cum = [5, 12, 25, 33, 40]
    fs = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, 5)]
    return g_median([0, 10, 20, 30, 40], 10, fs)


q("U13-A-026", TOPIC, "Median from a cumulative frequency table", "Medium", "Multi-step computation MCQ",
  r"The less than cumulative frequencies of a distribution are: less than $10$: $5$; less than $20$: $12$; less than $30$: $25$; less than $40$: $33$; less than $50$: $40$. The median of the distribution is",
  r"$\frac{340}{13}$",
  [(r"$\frac{116}{5}$", r"Uses the cumulative frequency $25$ as the frequency of the median class: $20 + \frac{8}{25} \cdot 10$."),
   (r"$\frac{345}{13}$", r"Uses $\frac{N+1}{2} = 20.5$ in place of $\frac{N}{2} = 20$."),
   (r"$\frac{310}{13}$", r"Subtracts the correction from the upper boundary: $30 - \frac{8}{13} \cdot 10$.")],
  r"$N = 40$, $\frac{N}{2} = 20$. The median class is $20\text{-}30$ with frequency $25 - 12 = 13$ and $cf = 12$. Median $= 20 + \frac{20 - 12}{13} \cdot 10 = \frac{340}{13}$.",
  r"Reading cumulative frequencies as class frequencies.",
  "U13-A-median-from-ogive-table", "Recover class frequencies, then apply the median formula.",
  check=_c026, values=[Rational(340, 13), Rational(116, 5), Rational(345, 13), Rational(310, 13)], cognitive="Application", source_class=SC)


def _c027():
    return g_mode([0, 10, 20, 30], 10, [15, 9, 6, 4])


q("U13-A-027", TOPIC, "Mode when the modal class is the first class", "Medium", "Multi-step computation MCQ",
  r"The classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40$ have frequencies $15, 9, 6, 4$ respectively. Taking the frequency of the (nonexistent) class before the first class as $0$, the mode of the distribution is",
  r"$\frac{50}{7}$",
  [(r"$5$", r"Takes the class mark of the modal class."),
   (r"$\frac{25}{4}$", r"Uses $f_2 = 9$ in place of $f_1 - f_2 = 6$ in the denominator: $\frac{15}{15 + 9} \cdot 10$."),
   (r"$\frac{20}{7}$", r"Subtracts the correction from the upper limit: $10 - \frac{50}{7}$.")],
  r"The modal class is $0\text{-}10$ with $l = 0$, $f_1 = 15$, $f_0 = 0$, $f_2 = 9$. Mode $= 0 + \frac{15 - 0}{30 - 0 - 9} \cdot 10 = \frac{150}{21} = \frac{50}{7}$.",
  r"Not knowing how to handle a modal class at the end of the table.",
  "U13-A-mode-first-class", "Mode formula with the boundary case $f_0 = 0$.",
  check=_c027, values=[Rational(50, 7), 5, Rational(25, 4), Rational(20, 7)], cognitive="Application", source_class=SC)


def _c028():
    A, h, N, Sfu = 45, 10, 50, -15
    return A + h * Rational(Sfu, N)


q("U13-A-028", TOPIC, "Step deviation method", "Medium", "Single-step computation MCQ",
  r"In a grouped distribution with equal class width $10$ and total frequency $50$, the step deviations are taken as $u_i = \frac{x_i - 45}{10}$, where $x_i$ are the class marks. If $\sum f_i u_i = -15$, the mean of the distribution is",
  r"$42$",
  [(r"$\frac{447}{10}$", r"Forgets to multiply by the class width: $45 - \frac{15}{50}$."),
   (r"$48$", r"Adds the correction in place of subtracting it (sign slip): $45 + 3$."),
   (r"$30$", r"Subtracts $\sum f_i u_i$ itself from $45$ without dividing by $N$ or multiplying by $h$.")],
  r"$\bar{x} = 45 + h \cdot \frac{\sum f_i u_i}{N} = 45 + 10 \cdot \frac{-15}{50} = 45 - 3 = 42$.",
  r"Forgetting to rescale by $h$ in the step deviation method.",
  "U13-A-step-deviation", "Reconstruct the mean from coded data; scale and sign traps.",
  check=_c028, values=[42, Rational(447, 10), 48, 30], cognitive="Application", source_class=SC,
  numerical=dict(question=r"In a grouped distribution with equal class width $10$ and total frequency $50$, the step deviations are $u_i = \frac{x_i - 45}{10}$, where $x_i$ are the class marks. If $\sum f_i u_i = -15$, then the mean of the distribution is", answer=42))


def _c029():
    x4 = symbols('x4')
    return solve(Eq(4 * 13 + 4 * 16 - x4, 7 * 15), x4)[0]


q("U13-A-029", TOPIC, "Overlapping partial means", "Medium", "Multi-step computation MCQ",
  r"The mean of seven observations $x_1, x_2, \ldots, x_7$ is $15$. The mean of $x_1, x_2, x_3, x_4$ is $13$ and the mean of $x_4, x_5, x_6, x_7$ is $16$. Then $x_4$ equals",
  r"$11$",
  [(r"$-11$", r"Writes $x_4 = 105 - 52 - 64$, reversing the sign of the overlap equation."),
   (r"$\frac{29}{2}$", r"Takes $x_4$ as the average of the two partial means, $\frac{13 + 16}{2}$."),
   (r"$12$", r"Takes the difference of the two partial sums, $64 - 52$.")],
  r"$x_1 + \cdots + x_4 = 52$ and $x_4 + \cdots + x_7 = 64$. Adding counts $x_4$ twice: $52 + 64 = 105 + x_4$, so $x_4 = 11$.",
  r"Not recognising that the shared observation is counted twice.",
  "U13-A-overlap-single", "Two partial sums with a shared term.",
  check=_c029, values=[11, -11, Rational(29, 2), 12], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean of seven observations $x_1, x_2, \ldots, x_7$ is $15$. The mean of $x_1, x_2, x_3, x_4$ is $13$ and the mean of $x_4, x_5, x_6, x_7$ is $16$. The value of $x_4$ is", answer=11))


def _c030():
    cge = [50, 46, 38, 22, 10, 0]
    fs = [cge[i] - cge[i + 1] for i in range(5)]
    return g_mean([0, 10, 20, 30, 40], 10, fs)


q("U13-A-030", TOPIC, "Mean from a more than cumulative table", "Medium", "Multi-step computation MCQ",
  r"For a distribution with classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$, the more than cumulative frequencies are: $0$ or more: $50$; $10$ or more: $46$; $20$ or more: $38$; $30$ or more: $22$; $40$ or more: $10$. The mean of the distribution is",
  r"$\frac{141}{5}$",
  [(r"$\frac{116}{5}$", r"Recovers the frequencies $4, 8, 16, 12, 10$ but uses the lower limits as $x_i$."),
   (r"$\frac{166}{5}$", r"Recovers the frequencies but uses the upper limits as $x_i$."),
   (r"$\frac{111}{5}$", r"Assigns each difference to the class one step too early, using frequencies $8, 16, 12, 10, 4$.")],
  r"Frequencies are successive differences: $4, 8, 16, 12, 10$. With class marks $5, 15, 25, 35, 45$: $\sum f_i x_i = 20 + 120 + 400 + 420 + 450 = 1410$, so the mean is $\frac{1410}{50} = \frac{141}{5}$.",
  r"Misreading a more than cumulative table.",
  "U13-A-mean-from-more-than", "Convert cumulative to class frequencies, then compute the mean.",
  check=_c030, values=[Rational(141, 5), Rational(116, 5), Rational(166, 5), Rational(111, 5)], cognitive="Application", source_class=SC)


def _c031():
    s = symbols('s')
    return solve(Eq(30 * 18000 + s, 31 * 18500), s)[0]


q("U13-A-031", TOPIC, "Mean after adding an observation", "Medium", "Inverse/parameter MCQ",
  r"The mean monthly salary of $30$ workers in a workshop is Rs $18000$. When the manager's salary is included, the mean salary rises by Rs $500$. The manager's monthly salary (in Rs) is",
  r"$33500$",
  [(r"$33000$", r"Adds the total rise $30 \cdot 500$ to the old mean $18000$ in place of the new mean $18500$."),
   (r"$18500$", r"Takes the manager's salary as the new mean."),
   (r"$15000$", r"Takes only the total increase $30 \cdot 500$ as the manager's salary.")],
  r"New total $= 31 \cdot 18500 = 573500$; old total $= 30 \cdot 18000 = 540000$. Manager's salary $= 573500 - 540000 = 33500$ (equivalently $18500 + 30 \cdot 500$).",
  r"Using the old count when computing the new total.",
  "U13-A-added-observation", "Two totals with a changed count.",
  check=_c031, values=[33500, 33000, 18500, 15000], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean monthly salary of $30$ workers is Rs $18000$. When the manager's salary is included, the mean salary rises by Rs $500$. The manager's monthly salary, in Rs, is", answer=33500))


def _c032():
    return mean_list([k * (k + 1) for k in range(1, 11)])


q("U13-A-032", TOPIC, "Mean of a sequence-defined data set", "Medium", "Multi-step computation MCQ",
  r"The mean of the ten observations $1 \cdot 2, 2 \cdot 3, 3 \cdot 4, \ldots, 10 \cdot 11$ is",
  r"$44$",
  [(r"$\frac{143}{4}$", r"Multiplies the mean of $1, \ldots, 10$ by the mean of $2, \ldots, 11$: $\frac{11}{2} \cdot \frac{13}{2}$."),
   (r"$\frac{77}{2}$", r"Uses only $\sum k^2 = 385$, dropping the $\sum k$ part of $k(k+1) = k^2 + k$."),
   (r"$40$", r"Gets the sum $440$ but divides by $11$, the last factor.")],
  r"$\sum_{k=1}^{10} k(k+1) = \sum k^2 + \sum k = 385 + 55 = 440$, so the mean is $\frac{440}{10} = 44$.",
  r"Assuming the mean of products equals the product of means.",
  "U13-A-mean-product-terms", "Split into two standard sums.",
  check=_c032, values=[44, Rational(143, 4), Rational(77, 2), 40], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The mean of the ten observations $1 \cdot 2, 2 \cdot 3, 3 \cdot 4, \ldots, 10 \cdot 11$ is", answer=44))


def _c033():
    return g_median([0, 10, 30, 40], [10, 20, 10, 20], [6, 16, 10, 8])


q("U13-A-033", TOPIC, "Median of grouped data with unequal classes", "Medium", "Multi-step computation MCQ",
  r"The classes $0\text{-}10, 10\text{-}30, 30\text{-}40, 40\text{-}60$ have frequencies $6, 16, 10, 8$ respectively. The median of the distribution is",
  r"$\frac{55}{2}$",
  [(r"$\frac{75}{4}$", r"Uses width $10$ for every class: $10 + \frac{14}{16} \cdot 10$."),
   (r"$\frac{225}{8}$", r"Uses $\frac{N+1}{2} = 20.5$ in place of $\frac{N}{2} = 20$: $10 + \frac{14.5}{16} \cdot 20$."),
   (r"$\frac{35}{2}$", r"Computes the correction $\frac{14}{16} \cdot 20$ but forgets to add the lower limit $10$.")],
  r"$N = 40$, $\frac{N}{2} = 20$. Cumulative frequencies $6, 22, 32, 40$ put the median in $10\text{-}30$ with $cf = 6$, $f = 16$, $h = 20$. Median $= 10 + \frac{20 - 6}{16} \cdot 20 = 10 + \frac{35}{2} = \frac{55}{2}$.",
  r"Assuming all classes have the same width.",
  "U13-A-median-unequal-width", "Median formula with the median class's own width.",
  check=_c033, values=[Rational(55, 2), Rational(75, 4), Rational(225, 8), Rational(35, 2)], cognitive="Application", source_class=SC)


def _c034():
    n = symbols('n', positive=True, integer=True)
    k = symbols('k', integer=True)
    s1 = simplify(summation(2 * k - 1, (k, 1, n)) / n - n) == 0
    s2 = median_list([3, 9, 4, 8, 5, 12, 1]) == 8
    return (bool(s1), bool(s2))


q("U13-A-034", TOPIC, "Mean and median facts", "Medium", "Statement-based MCQ",
  r"Statement I: For every natural number $n$, the mean of the first $n$ odd natural numbers is $n$." "\n\n"
  r"Statement II: The median of the observations $3, 9, 4, 8, 5, 12, 1$ is $8$." + TAIL,
  ST_TF,
  [(ST_TT, r"Takes the 4th observation in the given order, $8$, as the median and so accepts Statement II."),
   (ST_FF, r"Rejects Statement I by confusing the mean $n$ with the sum $n^2$, and rejects Statement II correctly."),
   (ST_FT, r"Rejects Statement I by confusing mean and sum, and accepts Statement II by not sorting the data.")],
  r"$1 + 3 + \cdots + (2n - 1) = n^2$, so the mean is $\frac{n^2}{n} = n$; Statement I is true. Sorted, the data are $1, 3, 4, 5, 8, 9, 12$, whose middle value is $5$, not $8$; Statement II is false.",
  r"Taking the middle value without sorting.",
  "U13-A-stmt-odd-mean-median", "Two quick checks, one with a sorting trap.",
  check=_c034, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding", source_class=SC)


def _c035():
    s1 = Rational(10 * 20 + 30 * 40, 40) == 30
    data = [2, 5, 7, 11, 13]
    M = median_list(data)
    s2 = median_list([3 * v - 2 for v in data]) == 3 * M - 2
    return (bool(s1), bool(s2))


q("U13-A-035", TOPIC, "Combined mean and transformed median", "Medium", "Statement-based MCQ",
  r"Statement I: If two groups have $10$ and $30$ observations with means $20$ and $40$ respectively, then the mean of all $40$ observations is $30$." "\n\n"
  r"Statement II: If the median of a set of observations is $M$, and every observation is multiplied by $3$ and then decreased by $2$, the median of the new set is $3M - 2$." + TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement I by averaging the two means without weights."),
   (ST_FF, r"Rejects Statement II, believing only the mean follows a linear change of the data."),
   (ST_TF, r"Averages the means without weights for Statement I and wrongly rejects Statement II.")],
  r"The combined mean is $\frac{10 \cdot 20 + 30 \cdot 40}{40} = \frac{1400}{40} = 35$, not $30$, so Statement I is false. The map $y = 3x - 2$ is increasing, so it preserves order and the middle observation maps to $3M - 2$; Statement II is true.",
  r"Averaging group means without weights.",
  "U13-A-stmt-combined-transform", "Two conceptual checks, one numeric.",
  check=_c035, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Understanding", source_class=SC)


# ================================================================ DIFFICULT (10)

def _c036():
    good = []
    for k in range(1, 200):
        data = expand_freq([1, 2, 3, 4, 5], [3, 2, k, 6, 5])
        if median_list(data) == 4:
            good.append(k)
    return len(good)


q("U13-A-036", TOPIC, "Median with an unknown frequency", "Difficult", "Inverse/parameter MCQ",
  r"The values $1, 2, 3, 4, 5$ occur with frequencies $3, 2, k, 6, 5$ respectively, where $k$ is a positive integer. When the total frequency is even, the median is taken as the mean of the two middle observations. The number of possible values of $k$ for which the median of the distribution is $4$ is",
  r"$5$",
  [(r"$6$", r"Uses the odd-$N$ position $\frac{N+1}{2}$ for every $k$; $\frac{17+k}{2} > 5 + k$ gives $k < 7$, which wrongly admits $k = 6$ (median $\frac{7}{2}$)."),
   (r"$4$", r"Uses the condition $\frac{N}{2} \ge 6 + k$ for every $k$, including odd $N$, which gives $k \le 4$ and loses $k = 5$."),
   (r"$3$", r"Considers only odd $k$ (so that $N$ is odd and there is a single middle value), getting $k = 1, 3, 5$.")],
  r"$N = 16 + k$ and the cumulative frequency up to the value $3$ is $5 + k$; the values $4$ occupy positions $6 + k$ to $11 + k$. For odd $k$, the middle position $\frac{17 + k}{2}$ must be at least $6 + k$, giving $k \le 5$: $k = 1, 3, 5$. For even $k$, both positions $\frac{16 + k}{2}$ and $\frac{18 + k}{2}$ must hold the value $4$, needing $\frac{16 + k}{2} \ge 6 + k$, so $k \le 4$: $k = 2, 4$. At $k = 6$ the middle pair is $3, 4$ and the median is $\frac{7}{2}$. Hence $k \in \{1, 2, 3, 4, 5\}$, giving $5$ values.",
  r"Handling the even-$N$ case of the median carelessly.",
  "U13-A-median-unknown-freq-count", "Parity casework on $N$ with a boundary value.",
  check=_c036, values=[5, 6, 4, 3], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The values $1, 2, 3, 4, 5$ occur with frequencies $3, 2, k, 6, 5$ respectively, where $k$ is a positive integer. When the total frequency is even, the median is taken as the mean of the two middle observations. The number of possible values of $k$ for which the median of the distribution is $4$ is", answer=5))


def _c037():
    cubes = [k**3 for k in range(1, 11)]
    s1 = mean_list(cubes) > median_list(cubes)
    data = expand_freq(range(1, 11), [2 * k - 1 for k in range(1, 11)])
    s2 = mean_list(data) == median_list(data)
    return (bool(s1), bool(s2))


q("U13-A-037", TOPIC, "Comparing mean and median", "Difficult", "Statement-based MCQ",
  r"Statement I: For the ten observations $1^3, 2^3, 3^3, \ldots, 10^3$, the mean is greater than the median." "\n\n"
  r"Statement II: For the data set in which each natural number $k$ with $1 \le k \le 10$ occurs exactly $2k - 1$ times, the mean equals the median." + TAIL,
  ST_TF,
  [(ST_TT, r"Ignores the frequencies in Statement II and works with $1, 2, \ldots, 10$ alone, whose mean and median are both $\frac{11}{2}$, and so accepts it."),
   (ST_FT, r"Takes the mean in Statement I as the cube of the mean of $1, \ldots, 10$, namely $\frac{1331}{8}$, which is below the median $\frac{341}{2}$, and so rejects Statement I; and ignores the frequencies in Statement II, accepting it."),
   (ST_FF, r"Takes the mean in Statement I as $\left(\frac{11}{2}\right)^3 = \frac{1331}{8}$, below the median $\frac{341}{2}$, and so rejects Statement I, while handling Statement II correctly.")],
  r"Statement I: $\sum k^3 = 55^2 = 3025$, so the mean is $\frac{605}{2}$; the median is $\frac{5^3 + 6^3}{2} = \frac{341}{2}$; true. Statement II: $N = \sum (2k - 1) = 100$ and $\sum k(2k - 1) = 2(385) - 55 = 715$, so the mean is $\frac{143}{20}$. The cumulative frequency up to $k$ is $k^2$, so positions $50$ and $51$ lie in the block of $8$s (positions $50$ to $64$); the median is $8 \ne \frac{143}{20}$; false.",
  r"Assuming the mean of cubes is the cube of the mean, and ignoring frequencies in a weighted data set.",
  "U13-A-stmt-mean-vs-median", "Two independent computations, one requiring a weighted median from cumulative frequencies $k^2$.",
  check=_c037, values=[(True, False), (True, True), (False, True), (False, False)], cognitive="Analysis", source_class=SC)


def _c038():
    f1, f2 = symbols('f1 f2', positive=True)
    lows = [0, 20, 40, 60, 80]
    fs = [5, f1, 10, f2, 7]
    mids = [10, 30, 50, 70, 90]
    sol = solve([Eq(sum(fs), 50), Eq(sum(f * m for f, m in zip(fs, mids)), 50 * 50)], [f1, f2], dict=True)[0]
    return g_median(lows, 20, [5, sol[f1], 10, sol[f2], 7])


q("U13-A-038", TOPIC, "Missing frequencies, then median", "Difficult", "Multi-step computation MCQ",
  r"The classes $0\text{-}20, 20\text{-}40, 40\text{-}60, 60\text{-}80, 80\text{-}100$ have frequencies $5, f_1, 10, f_2, 7$ respectively. The total frequency is $50$ and the mean of the distribution is $50$. The median of the distribution is",
  r"$48$",
  [(r"$56$", r"Solves for the frequencies but interchanges them ($f_1 = 12$, $f_2 = 16$), giving $cf = 17$: $40 + \frac{8}{10} \cdot 20$."),
   (r"$44$", r"Uses class width $10$ in the median formula: $40 + \frac{4}{10} \cdot 10$."),
   (r"$49$", r"Uses $\frac{N+1}{2} = 25.5$ in place of $\frac{N}{2} = 25$: $40 + \frac{4.5}{10} \cdot 20$.")],
  r"$f_1 + f_2 = 28$ and $50 + 30f_1 + 500 + 70f_2 + 630 = 2500$, so $3f_1 + 7f_2 = 132$. With $f_1 = 28 - f_2$: $84 + 4f_2 = 132$, $f_2 = 12$, $f_1 = 16$. Cumulative frequencies $5, 21, 31, \ldots$ put the $25$th observation in $40\text{-}60$: median $= 40 + \frac{25 - 21}{10} \cdot 20 = 48$.",
  r"Losing track of which unknown belongs to which class after solving.",
  "U13-A-missing-freq-then-median", "Two equations for two frequencies, then a median computation.",
  check=_c038, values=[48, 56, 44, 49], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The classes $0\text{-}20, 20\text{-}40, 40\text{-}60, 60\text{-}80, 80\text{-}100$ have frequencies $5, f_1, 10, f_2, 7$ respectively. The total frequency is $50$ and the mean of the distribution is $50$. The median of the distribution is", answer=48))


def _c039():
    x, y = symbols('x y', positive=True)
    sol = solve([Eq(6 + x + 16 + y + 4, 48), Eq(20 + (16 - x) * 10 / (32 - x - y), 26)], [x, y], dict=True)[0]
    fs = [6, sol[x], 16, sol[y], 4]
    assert g_mode([0, 10, 20, 30, 40], 10, fs) == 26
    return g_median([0, 10, 20, 30, 40], 10, fs)


q("U13-A-039", TOPIC, "Missing frequencies from the mode, then median", "Difficult", "Multi-step computation MCQ",
  r"The classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ have frequencies $6, x, 16, y, 4$ respectively, with total frequency $48$. If the mode of the distribution is $26$, the median of the distribution is",
  r"$25$",
  [(r"$\frac{95}{4}$", r"Interchanges $x$ and $y$ ($x = 12$, $y = 10$), giving $cf = 18$: $20 + \frac{6}{16} \cdot 10$."),
   (r"$\frac{41}{2}$", r"Omits the class width: $20 + \frac{8}{16}$."),
   (r"$\frac{405}{16}$", r"Uses $\frac{N+1}{2} = 24.5$ in place of $\frac{N}{2} = 24$.")],
  r"$x + y = 22$, so $2f_1 - f_0 - f_2 = 32 - 22 = 10$ and mode $= 20 + \frac{16 - x}{10} \cdot 10 = 36 - x = 26$, giving $x = 10$, $y = 12$. Cumulative frequencies $6, 16, 32, \ldots$ put the $24$th value in $20\text{-}30$: median $= 20 + \frac{24 - 16}{16} \cdot 10 = 25$.",
  r"Mixing up which neighbouring frequency is $f_0$ and which is $f_2$.",
  "U13-A-mode-then-median", "Mode equation with the total, then a median; three linked steps.",
  check=_c039, values=[25, Rational(95, 4), Rational(41, 2), Rational(405, 16)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The classes $0\text{-}10, 10\text{-}20, 20\text{-}30, 30\text{-}40, 40\text{-}50$ have frequencies $6, x, 16, y, 4$ respectively, with total frequency $48$. If the mode of the distribution is $26$, then the median of the distribution is", answer=25))


def _c040():
    total = 100 * 50
    first = 60 * 48
    last = 60 * 55
    overlap = 60 + 60 - 100
    return Rational(first + last - total, overlap)


q("U13-A-040", TOPIC, "Overlapping partial means", "Difficult", "Multi-step computation MCQ",
  r"The mean of $100$ observations is $50$. The mean of the first $60$ observations is $48$ and the mean of the last $60$ observations is $55$. The mean of the $41$st to the $60$th observations (inclusive) is",
  r"$59$",
  [(r"$\frac{103}{2}$", r"Averages the two partial means, $\frac{48 + 55}{2}$."),
   (r"$\frac{59}{2}$", r"Finds the excess $1180$ but divides by $40$, counting the overlap from both ends."),
   (r"$53$", r"Computes $\frac{5000 - 2880}{40} = 53$, the mean of the last $40$ observations, and stops.")],
  r"The first $60$ and the last $60$ overlap in the $20$ observations numbered $41$ to $60$. So (sum of first $60$) $+$ (sum of last $60$) $=$ (total) $+$ (sum of overlap): $2880 + 3300 = 5000 + S$, giving $S = 1180$ and mean $\frac{1180}{20} = 59$.",
  r"Not identifying the overlap size or double counting.",
  "U13-A-overlap-block", "Inclusion-exclusion on sums with a 20-term overlap.",
  check=_c040, values=[59, Rational(103, 2), Rational(59, 2), 53], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The mean of $100$ observations is $50$. The mean of the first $60$ observations is $48$ and the mean of the last $60$ observations is $55$. The mean of the $41$st to the $60$th observations (inclusive) is", answer=59))


def _c041():
    ys = set()
    for xv in range(1, 40):
        for yv in range(xv + 1, 40):
            data = [4, 6, 6, 9, xv, yv, 15]
            if mean_list(data) != 9 or median_list(data) != 9:
                continue
            c = {v: data.count(v) for v in data}
            mx = max(c.values())
            modes = [v for v in c if c[v] == mx]
            if modes == [6]:
                ys.add(yv)
    return sum(ys)


q("U13-A-041", TOPIC, "Mean, median and mode together", "Difficult", "Multi-step computation MCQ",
  r"The seven observations $4, 6, 6, 9, x, y, 15$, where $x$ and $y$ are positive integers with $x < y$, have mean $9$, median $9$ and a unique mode $6$. The sum of all possible values of $y$ is",
  r"$25$",
  [(r"$39$", r"Also accepts $(x, y) = (9, 14)$, overlooking that $9$ would then occur twice and the data would have two modes."),
   (r"$13$", r"Finds only the pair $(10, 13)$ and stops."),
   (r"$12$", r"Finds only the pair $(11, 12)$ and stops.")],
  r"The mean gives $x + y = 23$. For the median ($4$th value) to be $9$, neither $x$ nor $y$ may be below $9$, so $9 \le x \le 11$. If $x = 9$ then $9$ appears twice alongside $6$, so the mode is not unique. Hence $(x, y) = (10, 13)$ or $(11, 12)$, both with median $9$ and unique mode $6$. The sum of possible $y$ is $13 + 12 = 25$.",
  r"Forgetting that a unique mode rules out ties in frequency.",
  "U13-A-mean-median-mode-casework", "Three conditions with casework and a uniqueness trap.",
  check=_c041, values=[25, 39, 13, 12], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The seven observations $4, 6, 6, 9, x, y, 15$, where $x$ and $y$ are positive integers with $x < y$, have mean $9$, median $9$ and a unique mode $6$. The sum of all possible values of $y$ is", answer=25))


def _c042():
    n = symbols('n', positive=True, integer=True)
    k = symbols('k', integer=True)
    m = simplify(summation(k * (n - k + 1), (k, 1, n)) / summation(n - k + 1, (k, 1, n)))
    sols = [s for s in solve(Eq(m, 7), n) if s.is_integer and s > 0]
    return sols[0]


q("U13-A-042", TOPIC, "Mean of a frequency distribution with a parameter", "Difficult", "Inverse/parameter MCQ",
  r"For a natural number $n$, a data set contains each value $k \in \{1, 2, \ldots, n\}$ exactly $n - k + 1$ times (so $1$ occurs $n$ times and $n$ occurs once). If the mean of the data set is $7$, then $n$ equals",
  r"$19$",
  [(r"$10$", r"Takes the frequency of $k$ as $k$ (reversed weights), giving mean $\frac{2n+1}{3} = 7$."),
   (r"$13$", r"Ignores the frequencies and uses the mean $\frac{n+1}{2} = 7$ of $1, \ldots, n$."),
   (r"$20$", r"Takes the frequency of $k$ as $n - k$ (an off-by-one in the weights): $\sum k(n-k) = \frac{n(n+1)(n-1)}{6}$ and $\sum (n-k) = \frac{n(n-1)}{2}$, so the mean is $\frac{n+1}{3} = 7$.")],
  r"$\sum (n - k + 1) = \frac{n(n+1)}{2}$ and $\sum k(n - k + 1) = (n+1)\frac{n(n+1)}{2} - \frac{n(n+1)(2n+1)}{6} = \frac{n(n+1)(n+2)}{6}$. The mean is $\frac{n+2}{3} = 7$, so $n = 19$.",
  r"Mis-setting up weights when frequencies decrease with the value.",
  "U13-A-weighted-mean-parameter", "Two sums with a parameter, simplification, then solve.",
  check=_c042, values=[19, 10, 13, 20], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"For a natural number $n$, a data set contains each value $k \in \{1, 2, \ldots, n\}$ exactly $n - k + 1$ times. If the mean of the data set is $7$, then $n$ is", answer=19))


def _c043():
    best = 0
    for t in itertools.combinations_with_replacement(range(1, 26), 5):
        if sum(t) == 25 and t[2] == 6:
            best = max(best, t[4])
    return best


q("U13-A-043", TOPIC, "Extremal value under mean and median constraints", "Difficult", "Multi-step computation MCQ",
  r"Five positive integers, not necessarily distinct, have mean $5$ and median $6$. The largest possible value of the greatest of these integers is",
  r"$11$",
  [(r"$13$", r"Allows the two smallest numbers to be $0$, which are not positive: $25 - 0 - 0 - 6 - 6$."),
   (r"$10$", r"Insists the two smallest numbers be distinct ($1$ and $2$): $25 - 1 - 2 - 6 - 6$."),
   (r"$16$", r"Takes the fourth number as $1$, forgetting that it must be at least the median $6$: $25 - 1 - 1 - 6 - 1$.")],
  r"Write the numbers in order as $a \le b \le c \le d \le e$ with $c = 6$ and sum $25$. To make $e$ largest, take $a = b = 1$ and $d = 6$ (the least allowed, since $d \ge c$). Then $e = 25 - 1 - 1 - 6 - 6 = 11$.",
  r"Forgetting that values above the median must be at least the median.",
  "U13-A-extremal-mean-median", "Optimisation under ordering constraints with several traps.",
  check=_c043, values=[11, 13, 10, 16], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Five positive integers, not necessarily distinct, have mean $5$ and median $6$. The largest possible value of the greatest of these integers is", answer=11))


def _c044():
    k = symbols('k', positive=True, integer=True)
    S = k * (k**2 + 1)                      # sum of the first k observations
    xk = expand(S - S.subs(k, k - 1))       # k-th observation
    xs = [xk.subs(k, j) for j in range(1, 11)]
    return median_list(xs)


q("U13-A-044", TOPIC, "Observations recovered from running means", "Difficult", "Multi-step computation MCQ",
  r"A sequence of observations $x_1, x_2, x_3, \ldots$ is such that, for every natural number $k$, the mean of the first $k$ observations $x_1, \ldots, x_k$ is $k^2 + 1$. The median of the ten observations $x_1, x_2, \ldots, x_{10}$ is",
  r"$77$",
  [(r"$\frac{63}{2}$", r"Treats the running means $k^2 + 1$ themselves as the observations and averages the $5$th and $6$th: $\frac{26 + 37}{2}$."),
   (r"$10$", r"Takes $x_k$ as the difference of consecutive means, $(k^2 + 1) - ((k-1)^2 + 1) = 2k - 1$, instead of the difference of consecutive sums, giving $\frac{9 + 11}{2}$."),
   (r"$101$", r"Finds the mean of the ten observations, $10^2 + 1$, in place of their median.")],
  r"The sum of the first $k$ observations is $S_k = k(k^2 + 1) = k^3 + k$, so $x_k = S_k - S_{k-1} = 3k^2 - 3k + 2$. This is increasing for $k \ge 1$ ($2, 8, 20, 38, 62, 92, \ldots$), so the ten observations are already in order. With $10$ observations the median is $\frac{x_5 + x_6}{2} = \frac{62 + 92}{2} = 77$.",
  r"Differencing the running means instead of the running sums to recover individual observations.",
  "U13-A-running-mean-term", "Convert running means to sums, difference to get the general term, check monotonicity, then an even-$N$ median.",
  check=_c044, values=[77, Rational(63, 2), 10, 101], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"A sequence of observations $x_1, x_2, x_3, \ldots$ is such that, for every natural number $k$, the mean of the first $k$ observations $x_1, \ldots, x_k$ is $k^2 + 1$. The median of the ten observations $x_1, x_2, \ldots, x_{10}$ is", answer=77))


def _c045():
    good = []
    for p in range(1, 200):
        if median_list(expand_freq([10, 20, 30, 40, 50], [2, 3, p, 4, 6])) == 35:
            good.append(p)
    assert len(good) == 1
    return good[0]


q("U13-A-045", TOPIC, "Missing frequency from a median between two values", "Difficult", "Inverse/parameter MCQ",
  r"The values $10, 20, 30, 40, 50$ occur with frequencies $2, 3, p, 4, 6$ respectively, where $p$ is a positive integer. If the median of the distribution is $35$, then $p$ equals",
  r"$5$",
  [(r"$6$", r"Sets the cumulative frequency $5 + p$ equal to $\frac{N+1}{2} = \frac{16 + p}{2}$, the odd-$N$ position."),
   (r"$15$", r"Takes the cumulative frequency up to $30$ as $p$ alone, solving $p = \frac{15 + p}{2}$."),
   (r"$4$", r"Assumes the two middle values $30$ and $40$ must have equal frequencies.")],
  r"A median of $35$ is not a data value, so $N$ must be even and the two middle observations must be $30$ and $40$. That needs the cumulative frequency up to $30$ to equal exactly $\frac{N}{2}$: $5 + p = \frac{15 + p}{2}$, so $p = 5$. Check: $N = 20$, the $10$th value is $30$ and the $11$th is $40$, median $35$.",
  r"Not realising that a median between two data values forces the cumulative frequency to equal exactly $\frac{N}{2}$.",
  "U13-A-median-between-values", "Insight that the median is a midpoint, plus a parity argument.",
  check=_c045, values=[5, 6, 15, 4], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The values $10, 20, 30, 40, 50$ occur with frequencies $2, 3, p, 4, 6$ respectively, where $p$ is a positive integer. If the median of the distribution is $35$, then $p$ is", answer=5))
