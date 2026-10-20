import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from functools import reduce

x = Symbol('x')
n = Symbol('n', positive=True, integer=True)

TOPIC_R = "Remainders and divisibility"
TOPIC_L = "Last digits"
TOPIC_A = "Approximation and comparison"
TOPIC_F = "Integral and fractional parts"

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"


def _rnd(r, d):
    # round a positive rational to d decimal places (half up)
    return floor(r * 10**d + Rational(1, 2)) / Integer(10)**d


def _frac(R):
    R = expand(R)
    return R - floor(R)


# ---------------------------------------------------------------- EASY

q("U05-C-001", TOPIC_R, "Remainder using a power close to a multiple", "Easy", "Single-step computation MCQ",
  r"The remainder when $5^{99}$ is divided by $13$ is",
  r"$8$",
  [(r"$5$", r"Takes $(26-1)^{49} \equiv +1$, ignoring that the exponent $49$ is odd, so gets $5 \cdot 1 = 5$."),
   (r"$12$", r"Gets $(26-1)^{49} \equiv -1 \equiv 12$ but drops the extra factor $5$ in $5^{99} = 5 \cdot 25^{49}$."),
   (r"$1$", r"Makes both slips: treats $(-1)^{49}$ as $1$ and drops the factor $5$.")],
  r"$5^{99} = 5 \cdot 25^{49} = 5(26-1)^{49}$. Every term of $(26-1)^{49}$ except the last is a multiple of $26$, hence of $13$, and the last term is $(-1)^{49} = -1$. So $5^{99} = 13k - 5 = 13(k-1) + 8$, and the remainder is $8$.",
  r"Ignoring the sign of $(-1)^{\text{odd}}$ or the leftover factor when the exponent is split.",
  "U05-C-rem-neg-one-odd", "One rewrite $25 = 26 - 1$ and one sign check.",
  check=lambda: Mod(Integer(5)**99, 13), values=[8, 5, 12, 1],
  numerical=dict(question=r"The remainder when $5^{99}$ is divided by $13$ is", answer=8))

q("U05-C-002", TOPIC_R, "Remainder using a power one more than a multiple", "Easy", "Single-step computation MCQ",
  r"The remainder when $2^{2026}$ is divided by $7$ is",
  r"$2$",
  [(r"$1$", r"Writes $2^{2026}$ as a pure power of $8$, overlooking that $2026 = 3 \cdot 675 + 1$ leaves a factor $2$."),
   (r"$5$", r"Uses $8 \equiv -1 \pmod 7$, so gets $2(-1)^{675} = -2 \equiv 5$."),
   (r"$6$", r"Uses $8 \equiv -1$ and also drops the leftover factor $2$, giving $-1 \equiv 6$.")],
  r"$2026 = 3 \cdot 675 + 1$, so $2^{2026} = 2 \cdot 8^{675} = 2(7+1)^{675}$. All terms of $(7+1)^{675}$ except the last are multiples of $7$ and the last is $1$. Hence $2^{2026} = 2(7k+1) = 7(2k) + 2$, remainder $2$.",
  r"Losing the leftover factor when the exponent is not an exact multiple of the cycle.",
  "U05-C-rem-plus-one-split", "Single binomial rewrite with one leftover factor.",
  check=lambda: Mod(Integer(2)**2026, 7), values=[2, 1, 5, 6])

q("U05-C-003", TOPIC_A, "Exact value using conjugate expansions", "Easy", "Single-step computation MCQ",
  r"Using the binomial theorem, the value of $(101)^{4} - (99)^{4}$ is",
  r"$8000800$",
  [(r"$8000000$", r"Keeps only the leading surviving term $2 \cdot 4 \cdot 100^{3}$ and drops $2 \cdot 4 \cdot 100$."),
   (r"$4000400$", r"Adds the odd terms once only, forgetting that they appear twice in the difference."),
   (r"$200120002$", r"Keeps the even-position terms, which give the sum $(101)^4 + (99)^4 = 2(100^4 + 6 \cdot 100^2 + 1)$.")],
  r"With $a = 100$, $(a+1)^4 - (a-1)^4 = 2\left[\binom{4}{1}a^3 + \binom{4}{3}a\right] = 2(4 \cdot 10^6 + 4 \cdot 100) = 8000800$.",
  r"Mixing up which terms cancel in $(a+1)^n - (a-1)^n$.",
  "U05-C-exact-eval", "One expansion with cancellation of alternate terms.",
  check=lambda: Integer(101)**4 - Integer(99)**4, values=[8000800, 8000000, 4000400, 200120002])

q("U05-C-004", TOPIC_R, "Remainder with bases one away from the divisor", "Easy", "Single-step computation MCQ",
  r"The remainder when $47^{38} + 49^{37}$ is divided by $48$ is",
  r"$2$",
  [(r"$0$", r"Takes $(48-1)^{38} \equiv -1$, slipping on the parity of the even exponent, so $-1 + 1 = 0$."),
   (r"$46$", r"Treats both terms as $\equiv -1$, getting $-2 \equiv 46$."),
   (r"$1$", r"Expands both but keeps only the constant term $(-1)^{38} = 1$ of the first, dropping the constant $1$ of $(48+1)^{37}$.")],
  r"$47^{38} = (48-1)^{38} \equiv (-1)^{38} = 1$ and $49^{37} = (48+1)^{37} \equiv 1 \pmod{48}$, since every other term of each expansion contains the factor $48$. So the sum leaves remainder $1 + 1 = 2$.",
  r"Sign of $(-1)^n$ for even $n$.",
  "U05-C-rem-near-divisor-pm", "Two one-line expansions.",
  check=lambda: Mod(Integer(47)**38 + Integer(49)**37, 48), values=[2, 0, 46, 1])

q("U05-C-005", TOPIC_L, "Last two digits of a power of 11", "Easy", "Single-step computation MCQ",
  r"The last two digits of $11^{23}$ are",
  r"$31$",
  [(r"$21$", r"Uses $(n-1)$ in place of $n$ in the second term: $1 + 22 \cdot 10 = 221$."),
   (r"$11$", r"Assumes every power of $11$ ends in $11$, extrapolating from $11^1$."),
   (r"$01$", r"Thinks every term after the first is a multiple of $100$, overlooking $\binom{23}{1}10 = 230$.")],
  r"$11^{23} = (1+10)^{23} = 1 + 23 \cdot 10 + \binom{23}{2}10^2 + \dots$. Every term from the third onward is a multiple of $100$, so $11^{23} \equiv 1 + 230 = 231 \equiv 31 \pmod{100}$.",
  r"Dropping the linear term when working modulo $100$.",
  "U05-C-powers-of-11", "One expansion, keep two terms.",
  check=lambda: Mod(Integer(11)**23, 100), values=[31, 21, 11, 1],
  numerical=dict(question=r"The number formed by the last two digits of $11^{23}$ is", answer=31))

q("U05-C-006", TOPIC_A, "Exact value of a power near a power of 10", "Easy", "Single-step computation MCQ",
  r"Using the binomial theorem, the value of $(99)^{5}$ is",
  r"$9509900499$",
  [(r"$9509899999$", r"Omits the term $\binom{5}{4}100(-1)^4 = 500$."),
   (r"$9510100499$", r"Gives the term $\binom{5}{3}100^2(-1)^3$ a plus sign."),
   (r"$9489899499$", r"Uses a minus sign on every term after the first.")],
  r"$(100-1)^5 = 10^{10} - 5 \cdot 10^8 + 10 \cdot 10^6 - 10 \cdot 10^4 + 5 \cdot 100 - 1 = 10000000000 - 500000000 + 10000000 - 100000 + 500 - 1 = 9509900499$.",
  r"Sign pattern in $(a-b)^n$.",
  "U05-C-exact-eval", "Direct expansion with alternating signs.",
  check=lambda: Integer(99)**5, values=[9509900499, 9509899999, 9510100499, 9489899499])

q("U05-C-007", TOPIC_F, "Sum of conjugate surd powers", "Easy", "Single-step computation MCQ",
  r"The value of $(\sqrt{2}+1)^{6} + (\sqrt{2}-1)^{6}$ is",
  r"$198$",
  [(r"$99$", r"Adds the even-position terms but forgets the factor $2$ that comes from both expansions."),
   (r"$140\sqrt{2}$", r"Computes the difference: the odd-position terms survive, $2(6\sqrt2 + 40\sqrt2 + 24\sqrt2)$."),
   (r"$378$", r"Uses $\binom{6}{2} = 30$ and $\binom{6}{4} = 30$ (no division by $2$): $2(1 + 60 + 120 + 8)$.")],
  r"In $(1+a)^6 + (1-a)^6$ with $a = \sqrt2$ (note $(\sqrt2-1)^6 = (1-\sqrt2)^6$), odd powers cancel: $2\left[1 + \binom62 a^2 + \binom64 a^4 + a^6\right] = 2[1 + 30 + 60 + 8] = 198$.",
  r"Confusing which terms survive in a sum versus a difference of conjugate expansions.",
  "U05-C-surd-conjugate-sum", "One expansion with cancellation.",
  check=lambda: expand((sqrt(2)+1)**6 + (sqrt(2)-1)**6), values=[198, 99, 140*sqrt(2), 378])

def _c8():
    R = expand((2+sqrt(3))**5)
    I = floor(R)
    f = R - I
    return simplify(expand((I+f)*(1-f)))
q("U05-C-008", TOPIC_F, "Product with the complement of the fractional part", "Easy", "Single-step computation MCQ",
  r"Let $(2+\sqrt{3})^{5} = I + f$, where $I$ is an integer and $0 \le f < 1$. Then $(I+f)(1-f)$ equals",
  r"$1$",
  [(r"$(2+\sqrt{3})^{5}-1$", r"Takes $f = (2-\sqrt3)^5$ (the rule for a negative conjugate), so writes $(I+f)(1-f)$ as $(2+\sqrt3)^5 - (2+\sqrt3)^5(2-\sqrt3)^5$."),
   (r"$7^{5}$", r"Multiplies the conjugates as $4 + 3$ in place of $4 - 3$."),
   (r"$4^{5}$", r"Adds the conjugates $(2+\sqrt3) + (2-\sqrt3) = 4$ where they should be multiplied.")],
  r"Let $f' = (2-\sqrt3)^5$, which lies in $(0,1)$. Then $I + f + f' = (2+\sqrt3)^5 + (2-\sqrt3)^5$ is an integer (odd powers of $\sqrt3$ cancel), so $f + f' = 1$ and $1 - f = f'$. Hence $(I+f)(1-f) = (2+\sqrt3)^5(2-\sqrt3)^5 = (4-3)^5 = 1$.",
  r"Using $f = f'$ when the conjugate is positive.",
  "U05-C-frac-product-unit", "Standard conjugate argument in two lines.",
  check=_c8, values=[1, (2+sqrt(3))**5 - 1, 7**5, 4**5])

q("U05-C-009", TOPIC_A, "Approximation to four decimals", "Easy", "Single-step computation MCQ",
  r"Correct to four decimal places, the value of $(1.002)^{10}$ is",
  r"$1.0202$",
  [(r"$1.0200$", r"Keeps only $1 + 10(0.002)$."),
   (r"$1.0201$", r"Gets $1.02018$ but truncates where it should round."),
   (r"$1.0380$", r"Uses $(0.02)^2$ in place of $(0.002)^2$ in the third term: $1 + 0.02 + 45(0.0004)$.")],
  r"$(1+0.002)^{10} = 1 + 10(0.002) + 45(0.002)^2 + 120(0.002)^3 + \dots = 1 + 0.02 + 0.00018 + 0.00000096 + \dots = 1.02018\dots$, which rounds to $1.0202$.",
  r"Truncating the expansion too early or truncating in place of rounding.",
  "U05-C-approx-decimal", "Three terms and a rounding decision.",
  check=lambda: _rnd(Rational(1002, 1000)**10, 4),
  values=[Rational('1.0202'), Rational('1.0200'), Rational('1.0201'), Rational('1.0380')])

q("U05-C-010", TOPIC_R, "Counting exponents giving divisibility", "Easy", "Inverse/parameter MCQ",
  r"The number of natural numbers $n \le 100$ for which $3^{n} + 1$ is divisible by $4$ is",
  r"$50$",
  [(r"$100$", r"Believes $3^n + 1$ is always a multiple of $4$, generalising from $n = 1$."),
   (r"$25$", r"Assumes a cycle of length $4$, so counts only $n \equiv 1 \pmod 4$."),
   (r"$0$", r"Writes $(4-1)^n \equiv 1$ for every $n$, ignoring the sign, so $3^n + 1 \equiv 2$ always.")],
  r"$3^n = (4-1)^n \equiv (-1)^n \pmod 4$. So $3^n + 1 \equiv 0$ exactly when $n$ is odd, and there are $50$ odd numbers from $1$ to $100$.",
  r"Ignoring the sign of $(-1)^n$.",
  "U05-C-count-n-divisible", "One binomial reduction then a count.",
  check=lambda: Integer(sum(1 for k in range(1, 101) if Mod(Integer(3)**k + 1, 4) == 0)), values=[50, 100, 25, 0],
  numerical=dict(question=r"The number of natural numbers $n \le 100$ for which $3^{n} + 1$ is divisible by $4$ is", answer=50))

q("U05-C-011", TOPIC_R, "Counting exponents giving divisibility", "Easy", "Inverse/parameter MCQ",
  r"The number of integers $n \in \{1, 2, 3, \dots, 60\}$ for which $2^{n} - 1$ is divisible by $7$ is",
  r"$20$",
  [(r"$60$", r"Thinks $2^n - 1$ is always a multiple of $7$."),
   (r"$30$", r"Assumes the condition holds for even $n$, as for $3^n - 1$ and $8$."),
   (r"$10$", r"Takes the cycle of $2^n$ modulo $7$ to have length $6$.")],
  r"If $n = 3m$, then $2^n = 8^m = (7+1)^m \equiv 1 \pmod 7$. If $n = 3m+1$ or $3m+2$, then $2^n \equiv 2$ or $4$. So $7 \mid 2^n - 1$ exactly when $3 \mid n$, giving $20$ values.",
  r"Wrong cycle length for powers of $2$ modulo $7$.",
  "U05-C-count-n-divisible", "One binomial reduction and a count.",
  check=lambda: Integer(sum(1 for k in range(1, 61) if Mod(Integer(2)**k - 1, 7) == 0)), values=[20, 60, 30, 10])

q("U05-C-012", TOPIC_R, "Divisibility of a^n minus a linear term", "Easy", "Single-step computation MCQ",
  r"The largest natural number that divides $8^{n} - 7n - 1$ for every natural number $n$ is",
  r"$49$",
  [(r"$7$", r"Sees only that $8^n - 1$ is a multiple of $7$ and stops there."),
   (r"$343$", r"Expects $7^3$ because the expansion has a $\binom{n}{3}7^3$ term."),
   (r"$14$", r"Sees that $8^n - 7n - 1$ is a multiple of $7$, wrongly believes it is always even, and gives $2 \cdot 7 = 14$.")],
  r"$8^n = (1+7)^n = 1 + 7n + \binom{n}{2}7^2 + \binom n3 7^3 + \dots$, so $8^n - 7n - 1 = 49\left[\binom n2 + 7\binom n3 + \dots\right]$ is a multiple of $49$. At $n = 2$ the value is $64 - 15 = 49$, so nothing larger divides it for every $n$.",
  r"Stopping at the first visible factor.",
  "U05-C-div-gcd-linear", "One expansion plus a test value.",
  check=lambda: reduce(gcd, [Integer(8)**k - 7*k - 1 for k in range(1, 30)]), values=[49, 7, 343, 14],
  numerical=dict(question=r"The largest natural number that divides $8^{n} - 7n - 1$ for every natural number $n$ is", answer=49))

q("U05-C-013", TOPIC_L, "Units digit by binomial reduction", "Easy", "Single-step computation MCQ",
  r"The units digit of $3^{2025}$ is",
  r"$3$",
  [(r"$7$", r"Takes $(10-1)^{1012} \equiv -1$, slipping on the parity, so $3 \cdot (-1) \equiv 7$."),
   (r"$9$", r"Writes $3^{2025}$ as $9^{1013}$ (an exponent off by one), giving $(10-1)^{1013} \equiv -1 \equiv 9$."),
   (r"$1$", r"Uses $9^{1012} \equiv 1$ but drops the leftover factor $3$.")],
  r"$3^{2025} = 3 \cdot 9^{1012} = 3(10-1)^{1012}$. Modulo $10$ only the last term $(-1)^{1012} = 1$ survives, so $3^{2025} \equiv 3 \pmod{10}$ and the units digit is $3$.",
  r"Mishandling the leftover factor or the parity of the exponent.",
  "U05-C-units-digit", "Single reduction modulo 10.",
  check=lambda: Mod(Integer(3)**2025, 10), values=[3, 7, 9, 1])

q("U05-C-014", TOPIC_A, "Comparing powers with integers", "Easy", "Statement-based MCQ",
  r"Statement I: $(1.01)^{1000} > 10$. Statement II: $(1.1)^{10} < 2$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Believes $(1.1)^{10}$ stays below $2$ because $0.1$ is small."),
   (ST_FF, r"Believes $(1.01)^{1000}$ is close to $1$ because $1.01$ is close to $1$."),
   (ST_FT, r"Reverses both judgements about how fast small bases grow.")],
  r"All terms of $(1+x)^n$ are positive for $x > 0$, so $(1+x)^n > 1 + nx$ for $n \ge 2$. Hence $(1.01)^{1000} > 1 + 1000(0.01) = 11 > 10$, so Statement I is true, and $(1.1)^{10} > 1 + 10(0.1) = 2$, so Statement II is false.",
  r"Underestimating $(1+x)^n$ for small $x$ and large $n$.",
  "U05-C-compare-statement", "First two terms of an expansion suffice for each statement.",
  check=lambda: (bool(Rational(101, 100)**1000 > 10), bool(Rational(11, 10)**10 < 2)),
  values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding")

# ---------------------------------------------------------------- MEDIUM

q("U05-C-015", TOPIC_R, "Remainder modulo 25", "Medium", "Multi-step computation MCQ",
  r"If $7^{205} = 25k + r$, where $k$ is an integer and $0 \le r < 25$, then $r$ equals",
  r"$7$",
  [(r"$18$", r"Takes $(50-1)^{102} \equiv -1$, slipping on the parity, so $r \equiv -7 \equiv 18$."),
   (r"$1$", r"Uses $49^{102} \equiv 1$ but forgets the extra factor $7$."),
   (r"$24$", r"Drops the factor $7$ and also takes $(-1)^{102} = -1$.")],
  r"$7^{205} = 7 \cdot 49^{102} = 7(50-1)^{102}$. Every term except the last has a factor $50$, a multiple of $25$, and the last is $(-1)^{102} = 1$. So $7^{205} = 7(25m + 1) = 25(7m) + 7$, giving $r = 7$.",
  r"Losing the leftover factor or the sign of the last term.",
  "U05-C-rem-mod-25", "Split the exponent, rewrite $49 = 50 - 1$, check parity.",
  check=lambda: Mod(Integer(7)**205, 25), values=[7, 18, 1, 24],
  numerical=dict(question=r"If $7^{205} = 25k + r$, where $k$ is an integer and $0 \le r < 25$, then $r$ is", answer=7))

q("U05-C-016", TOPIC_R, "Remainder with a negative residue", "Medium", "Multi-step computation MCQ",
  r"The remainder when $2^{2023}$ is divided by $17$ is",
  r"$9$",
  [(r"$8$", r"Ignores the sign: takes $(17-1)^{505} \equiv +1$."),
   (r"$16$", r"Gets $(17-1)^{505} \equiv -1$ but drops the factor $2^3 = 8$."),
   (r"$1$", r"Drops the factor $8$ and also ignores the sign.")],
  r"$2023 = 4 \cdot 505 + 3$, so $2^{2023} = 8 \cdot 16^{505} = 8(17-1)^{505} \equiv 8(-1)^{505} = -8 \pmod{17}$. Since $-8 + 17 = 9$, the remainder is $9$.",
  r"Converting a negative residue to a remainder, and the leftover factor.",
  "U05-C-rem-neg-one-odd", "Split exponent, odd power of $-1$, convert $-8$ to a remainder.",
  check=lambda: Mod(Integer(2)**2023, 17), values=[9, 8, 16, 1],
  numerical=dict(question=r"The remainder when $2^{2023}$ is divided by $17$ is", answer=9))

q("U05-C-017", TOPIC_R, "Remainders for two neighbouring divisors", "Medium", "Multi-step computation MCQ",
  r"Let $r_1$ and $r_2$ be the remainders when $2^{2026}$ is divided by $31$ and $33$ respectively. Then $r_1 + r_2$ equals",
  r"$33$",
  [(r"$4$", r"Treats $32$ as one more than a multiple of both divisors, so $r_1 = r_2 = 2$."),
   (r"$60$", r"Treats $32$ as one less than a multiple of both divisors, so $r_1 = 29$ and $r_2 = 31$."),
   (r"$31$", r"Swaps the two cases: $r_1 = 29$ and $r_2 = 2$.")],
  r"$2026 = 5 \cdot 405 + 1$, so $2^{2026} = 2 \cdot 32^{405}$. Since $32 = 31 + 1$, $2^{2026} \equiv 2 \pmod{31}$, so $r_1 = 2$. Since $32 = 33 - 1$, $2^{2026} \equiv 2(-1)^{405} = -2 \equiv 31 \pmod{33}$, so $r_2 = 31$. Hence $r_1 + r_2 = 33$.",
  r"Using the same sign for $32 = 31 + 1$ and $32 = 33 - 1$.",
  "U05-C-rem-pair-moduli", "Two binomial reductions with opposite signs combined.",
  check=lambda: Mod(Integer(2)**2026, 31) + Mod(Integer(2)**2026, 33), values=[33, 4, 60, 31],
  numerical=dict(question=r"Let $r_1$ and $r_2$ be the remainders when $2^{2026}$ is divided by $31$ and $33$ respectively. Then $r_1 + r_2$ is", answer=33))

q("U05-C-018", TOPIC_L, "Last two digits using 50 minus 1", "Medium", "Multi-step computation MCQ",
  r"The last two digits of $7^{2026}$ are",
  r"$49$",
  [(r"$99$", r"Keeps only the last term $(-1)^{1013}$ and drops $\binom{1013}{1}50(-1)^{1012}$."),
   (r"$51$", r"Writes $49 = 50 + 1$ in effect, getting $1 + 1013 \cdot 50 \equiv 51$."),
   (r"$01$", r"Assumes $7^{4} \equiv 1 \pmod{100}$ makes every even power end in $01$.")],
  r"$7^{2026} = 49^{1013} = (50-1)^{1013}$. Modulo $100$, terms with $50^2$ or higher vanish, leaving $\binom{1013}{1}50(-1)^{1012} + (-1)^{1013} = 50650 - 1 = 50649 \equiv 49$. So the last two digits are $49$.",
  r"Dropping the linear term $\binom{n}{1}50$, which is not always a multiple of $100$.",
  "U05-C-last2-near-50", "Two surviving terms with signs, modulo 100.",
  check=lambda: Mod(Integer(7)**2026, 100), values=[49, 99, 51, 1],
  numerical=dict(question=r"The number formed by the last two digits of $7^{2026}$ is", answer=49))

q("U05-C-019", TOPIC_L, "Last two digits using 10 minus 1", "Medium", "Multi-step computation MCQ",
  r"The last two digits of $3^{54}$ are",
  r"$69$",
  [(r"$99$", r"Keeps only $(-1)^{27} = -1$ and drops the term $\binom{27}{1}10(-1)^{26}$."),
   (r"$31$", r"Expands $(1-10)^{27}$ in place of $(-1+10)^{27}$: $1 - 270 \equiv 31$."),
   (r"$09$", r"Assumes odd powers of $9$ end in $09$, extrapolating from $9^1$.")],
  r"$3^{54} = 9^{27} = (10-1)^{27}$. Modulo $100$ only the last two terms survive: $\binom{27}{1}10(-1)^{26} + (-1)^{27} = 270 - 1 = 269 \equiv 69$.",
  r"Sign handling when writing $9 = 10 - 1$.",
  "U05-C-last2-near-10", "Rewrite, keep two terms, track signs.",
  check=lambda: Mod(Integer(3)**54, 100), values=[69, 99, 31, 9])

q("U05-C-020", TOPIC_L, "Tens digit of a large power", "Medium", "Multi-step computation MCQ",
  r"The tens digit of $9^{2026}$ is",
  r"$4$",
  [(r"$0$", r"Keeps only $(-1)^{2026} = 1$, so believes the number ends in $01$."),
   (r"$6$", r"Gives the linear term a plus sign: $1 + 20260 \equiv 61$."),
   (r"$5$", r"Computes $1 - 60$ as $59$ without reducing $-59$ modulo $100$.")],
  r"$9^{2026} = (10-1)^{2026} \equiv \binom{2026}{1}10(-1)^{2025} + 1 = 1 - 20260 \pmod{100}$. Since $20260 \equiv 60$, this is $1 - 60 = -59 \equiv 41$. The last two digits are $41$, so the tens digit is $4$.",
  r"Reducing a negative number modulo 100.",
  "U05-C-last2-near-10", "Two terms, negative residue, read the tens digit.",
  check=lambda: floor(Mod(Integer(9)**2026, 100) / 10), values=[4, 0, 6, 5])

q("U05-C-021", TOPIC_L, "Last three digits of a power of 11", "Medium", "Multi-step computation MCQ",
  r"The last three digits of $11^{37}$ are",
  r"$971$",
  [(r"$371$", r"Keeps only $1 + 37 \cdot 10$, dropping $\binom{37}{2}10^2$, which is not a multiple of $1000$."),
   (r"$571$", r"Uses $\binom{37}{2} = 37 \cdot 36 = 1332$, forgetting to divide by $2$: $1 + 370 + 133200$."),
   (r"$231$", r"Applies alternating signs as if expanding $(1-10)^{37}$: $1 - 370 + 66600 = 66231$.")],
  r"$11^{37} = (1+10)^{37} = 1 + 370 + \binom{37}{2}100 + \binom{37}{3}1000 + \dots$. Modulo $1000$ the terms from $10^3$ on vanish, and $\binom{37}{2} = 666$, so $11^{37} \equiv 1 + 370 + 66600 \equiv 1 + 370 + 600 = 971$.",
  r"Keeping too few terms when working modulo $1000$.",
  "U05-C-powers-of-11", "Three surviving terms modulo 1000.",
  check=lambda: Mod(Integer(11)**37, 1000), values=[971, 371, 571, 231],
  numerical=dict(question=r"The number formed by the last three digits of $11^{37}$ is", answer=971))

q("U05-C-022", TOPIC_R, "Remainder modulo the square of 8", "Medium", "Multi-step computation MCQ",
  r"The remainder when $9^{100}$ is divided by $64$ is",
  r"$33$",
  [(r"$1$", r"Keeps only the first term of $(1+8)^{100}$, as if working modulo $8$."),
   (r"$32$", r"Reduces $8 \cdot 100 = 800 \equiv 32$ but drops the leading $1$."),
   (r"$25$", r"Uses $99$ in place of $100$ in the linear term: $1 + 792 \equiv 25$.")],
  r"$9^{100} = (1+8)^{100} = 1 + 100 \cdot 8 + \binom{100}{2}8^2 + \dots$. Every term from $8^2 = 64$ on is a multiple of $64$, so $9^{100} \equiv 1 + 800 = 801 = 12 \cdot 64 + 33$. The remainder is $33$.",
  r"Treating a modulus $64 = 8^2$ as if it were $8$.",
  "U05-C-rem-mod-64", "Two surviving terms and a reduction.",
  check=lambda: Mod(Integer(9)**100, 64), values=[33, 1, 32, 25],
  numerical=dict(question=r"The remainder when $9^{100}$ is divided by $64$ is", answer=33))

q("U05-C-023", TOPIC_R, "Divisibility of a^n minus a linear term", "Medium", "Multi-step computation MCQ",
  r"The largest natural number that divides $25^{n+1} - 24n - 25$ for every natural number $n$ is",
  r"$576$",
  [(r"$24$", r"Stops after seeing that $25^{n+1} - 25$ and $24n$ are multiples of $24$."),
   (r"$288$", r"Writes $\binom{n+1}{2}24^2 = 288\,n(n+1)$ and keeps only the factor $288$, overlooking that $n(n+1)$ is always even."),
   (r"$625$", r"Expects a factor $25^2$ from the base.")],
  r"$25^{n+1} = (1+24)^{n+1} = 1 + 24(n+1) + \binom{n+1}{2}24^2 + \dots$, so $25^{n+1} - 24n - 25 = 24^2\left[\binom{n+1}{2} + 24\binom{n+1}{3} + \dots\right]$, a multiple of $576$. At $n = 1$ the value is $625 - 49 = 576$, so $576$ is the largest such number.",
  r"Stopping at the first-order factor $24$.",
  "U05-C-div-gcd-linear", "Rewrite in the form $(1+24)^{n+1}$, factor, test $n = 1$.",
  check=lambda: reduce(gcd, [Integer(25)**(k+1) - 24*k - 25 for k in range(1, 30)]), values=[576, 24, 288, 625],
  numerical=dict(question=r"The largest natural number that divides $25^{n+1} - 24n - 25$ for every natural number $n$ is", answer=576))

q("U05-C-024", TOPIC_R, "Finding the exponent from a remainder", "Medium", "Inverse/parameter MCQ",
  r"The least natural number $n$ for which $9^{n}$ leaves remainder $57$ on division by $64$ is",
  r"$7$",
  [(r"$56$", r"Uses $9^n \equiv 1 + n$ in place of $1 + 8n$, so solves $1 + n = 57$."),
   (r"$6$", r"Index slip: uses $1 + 8(n+1)$ for the first two terms."),
   (r"$8$", r"Index slip: uses $1 + 8(n-1)$ for the first two terms.")],
  r"$9^n = (1+8)^n \equiv 1 + 8n \pmod{64}$, since later terms contain $8^2$. We need $1 + 8n \equiv 57$, i.e. $8n \equiv 56 \pmod{64}$, i.e. $n \equiv 7 \pmod 8$. The least such $n$ is $7$; indeed $1 + 56 = 57$.",
  r"Mis-indexing the linear term of the expansion.",
  "U05-C-rem-mod-64", "Reverse use of the expansion with a congruence.",
  check=lambda: Integer(next(k for k in range(1, 500) if Mod(Integer(9)**k, 64) == 57)), values=[7, 56, 6, 8],
  numerical=dict(question=r"The least natural number $n$ for which $9^{n}$ leaves remainder $57$ on division by $64$ is", answer=7))

q("U05-C-025", TOPIC_R, "Remainder modulo a composite number", "Medium", "Multi-step computation MCQ",
  r"The remainder when $27^{40}$ is divided by $12$ is",
  r"$9$",
  [(r"$1$", r"Works modulo $4$ only: $3^{120} = (4-1)^{120} \equiv 1$, and reports that as the remainder modulo $12$."),
   (r"$3$", r"Uses $27 \equiv 3 \pmod{12}$ and then assumes $3^{40} \equiv 3$."),
   (r"$0$", r"Argues that $27^{40}$ is a multiple of $3$, hence of $12$.")],
  r"$27^{40} = 3^{120}$ is a multiple of $3$. Also $3^{120} = 9^{60} = (1+8)^{60} \equiv 1 \pmod 8$, hence $\equiv 1 \pmod 4$. The only residue modulo $12$ that is a multiple of $3$ and $\equiv 1 \pmod 4$ is $9$, so the remainder is $9$.",
  r"Reducing modulo a factor of $12$ and reporting it as the remainder modulo $12$.",
  "U05-C-rem-composite", "Two separate conditions combined.",
  check=lambda: Mod(Integer(27)**40, 12), values=[9, 1, 3, 0],
  numerical=dict(question=r"The remainder when $27^{40}$ is divided by $12$ is", answer=9))

q("U05-C-026", TOPIC_F, "Integral part for an even power", "Medium", "Multi-step computation MCQ",
  r"The greatest integer less than or equal to $(\sqrt{3}+1)^{6}$ is",
  r"$415$",
  [(r"$416$", r"Finds $(\sqrt3+1)^6 + (\sqrt3-1)^6 = 416$ but forgets that the small term must be subtracted."),
   (r"$208$", r"Takes the rational part $208$ of $208 + 120\sqrt3$ as the integer part."),
   (r"$207$", r"Halves the integer sum $416$ and subtracts $1$.")],
  r"Let $S = (\sqrt3+1)^6 + (\sqrt3-1)^6 = (4+2\sqrt3)^3 + (4-2\sqrt3)^3 = 2(64 + 3 \cdot 4 \cdot 12) = 416$. Since $0 < (\sqrt3-1)^6 < 1$, we get $415 < (\sqrt3+1)^6 < 416$, so the greatest integer is $415$.",
  r"Forgetting that the conjugate term is positive and must be removed.",
  "U05-C-int-part-even", "Conjugate sum, then locate between integers.",
  check=lambda: floor(expand((sqrt(3)+1)**6)), values=[415, 416, 208, 207],
  numerical=dict(question=r"The greatest integer less than or equal to $(\sqrt{3}+1)^{6}$ is", answer=415))

q("U05-C-027", TOPIC_F, "Integral part for an odd power", "Medium", "Multi-step computation MCQ",
  r"The greatest integer less than or equal to $(\sqrt{2}+1)^{7}$ is",
  r"$478$",
  [(r"$477$", r"Applies the even-power method: assumes $(\sqrt2+1)^7 + (\sqrt2-1)^7$ is an integer and subtracts $1$."),
   (r"$239$", r"Takes the rational part of $239 + 169\sqrt2$ as the integer part."),
   (r"$479$", r"Rounds $478.002\dots$ up.")],
  r"Here $(\sqrt2+1)^7 - (\sqrt2-1)^7 = (1+\sqrt2)^7 + (1-\sqrt2)^7 = 2\left[1 + \binom72 2 + \binom74 4 + \binom76 8\right] = 2(1 + 42 + 140 + 56) = 478$. Since $0 < (\sqrt2-1)^7 < 1$, $(\sqrt2+1)^7 = 478 + (\sqrt2-1)^7$ lies in $(478, 479)$, so the answer is $478$.",
  r"Using the even-power rule for an odd power where the conjugate is negative.",
  "U05-C-int-part-odd", "Parity of the exponent decides sum versus difference; trap of subtracting 1.",
  check=lambda: floor(expand((sqrt(2)+1)**7)), values=[478, 477, 239, 479],
  numerical=dict(question=r"The greatest integer less than or equal to $(\sqrt{2}+1)^{7}$ is", answer=478))

def _c28():
    return _frac((sqrt(2)+1)**6)
q("U05-C-028", TOPIC_F, "Closed form of the fractional part", "Medium", "Multi-step computation MCQ",
  r"If $(\sqrt{2}+1)^{6} = I + f$, where $I$ is an integer and $0 \le f < 1$, then $f$ equals",
  r"$1-(\sqrt{2}-1)^{6}$",
  [(r"$(\sqrt{2}-1)^{6}$", r"Uses the odd-power result $f = (\sqrt2-1)^n$ for an even power."),
   (r"$1-(3-2\sqrt{2})^{6}$", r"Rewrites $(\sqrt2+1)^6$ as $(3+2\sqrt2)^6$, squaring the base without halving the exponent."),
   (r"$(3-2\sqrt{2})^{6}$", r"Squares the base without halving the exponent and also uses the odd-power rule.")],
  r"$(\sqrt2+1)^6 + (\sqrt2-1)^6 = 198$ is an integer and $0 < (\sqrt2-1)^6 < 1$. So $I + f = 198 - (\sqrt2-1)^6$, which gives $I = 197$ and $f = 1 - (\sqrt2-1)^6$.",
  r"Not distinguishing even and odd powers when the conjugate is $1 - \sqrt2 < 0$.",
  "U05-C-frac-closed-form", "Conjugate sum, then identify $f$ with the right parity rule.",
  check=_c28, values=[1-(sqrt(2)-1)**6, (sqrt(2)-1)**6, 1-(3-2*sqrt(2))**6, (3-2*sqrt(2))**6])

def _c29():
    R = (5*sqrt(5)+11)**7
    return expand(expand(R) * _frac(R))
q("U05-C-029", TOPIC_F, "Product of a number and its fractional part", "Medium", "Multi-step computation MCQ",
  r"Let $R = (5\sqrt{5}+11)^{7}$ and let $f = R - [R]$, where $[\,\cdot\,]$ denotes the greatest integer function. Then $Rf$ equals",
  r"$16384$",
  [(r"$1$", r"Assumes the conjugates multiply to $1$, as for $2 \pm \sqrt3$."),
   (r"$4$", r"Finds $(5\sqrt5+11)(5\sqrt5-11) = 4$ but forgets the seventh power."),
   (r"$128$", r"Takes the conjugate product as $\sqrt{125 - 121} = 2$ and raises it to the seventh power.")],
  r"Let $f' = (5\sqrt5 - 11)^7$; since $0 < 5\sqrt5 - 11 < 1$, $0 < f' < 1$. Now $R - f' = (11+5\sqrt5)^7 + (11-5\sqrt5)^7$ is an integer, so $f = f'$. Hence $Rf = \left[(5\sqrt5+11)(5\sqrt5-11)\right]^7 = (125-121)^7 = 4^7 = 16384$.",
  r"Mixing up when $f = f'$ and when $f = 1 - f'$.",
  "U05-C-frac-product-power", "Sign of the conjugate, integrality of the difference, then product.",
  check=_c29, values=[16384, 1, 4, 128],
  numerical=dict(question=r"Let $R = (5\sqrt{5}+11)^{7}$ and let $f = R - [R]$, where $[\,\cdot\,]$ denotes the greatest integer function. Then the value of $Rf$ is", answer=16384))

q("U05-C-030", TOPIC_R, "Polynomial remainder by a squared linear factor", "Medium", "Multi-step computation MCQ",
  r"The remainder when $x^{100}$ is divided by $(x-1)^{2}$ is",
  r"$100x-99$",
  [(r"$99x-98$", r"Uses $\binom{100}{1} = 99$, an index slip, giving $1 + 99(x-1)$."),
   (r"$101x-100$", r"Uses $101$ as the coefficient of $(x-1)$, giving $1 + 101(x-1)$."),
   (r"$-100x+101$", r"Gives the linear term a minus sign: $1 - 100(x-1)$.")],
  r"Write $x = 1 + (x-1)$. Then $x^{100} = 1 + 100(x-1) + \binom{100}{2}(x-1)^2 + \dots$, and every term from the third on is divisible by $(x-1)^2$. So the remainder is $1 + 100(x-1) = 100x - 99$.",
  r"Mis-indexing the binomial coefficient of the linear term.",
  "U05-C-poly-remainder", "Substitute and truncate the expansion.",
  check=lambda: rem(x**100, (x-1)**2, x), values=[100*x-99, 99*x-98, 101*x-100, -100*x+101])

q("U05-C-031", TOPIC_A, "Approximation to four decimals", "Medium", "Multi-step computation MCQ",
  r"Correct to four decimal places, the value of $(0.99)^{10}$ is",
  r"$0.9044$",
  [(r"$0.9045$", r"Stops after three terms: $1 - 0.1 + 0.0045$, omitting $-\binom{10}{3}(0.01)^3 = -0.00012$."),
   (r"$0.9000$", r"Keeps only $1 - 10(0.01)$."),
   (r"$0.9043$", r"Gets $0.904382$ but truncates where it should round.")],
  r"$(1-0.01)^{10} = 1 - 0.1 + 45(0.0001) - 120(0.000001) + 210(10^{-8}) - \dots = 1 - 0.1 + 0.0045 - 0.00012 + 0.0000021 - \dots = 0.904382\dots$, which rounds to $0.9044$.",
  r"Stopping the expansion before the terms that affect the fourth decimal place.",
  "U05-C-approx-decimal", "Four terms are needed and then rounding.",
  check=lambda: _rnd(Rational(99, 100)**10, 4),
  values=[Rational('0.9044'), Rational('0.9045'), Rational('0.9000'), Rational('0.9043')])

q("U05-C-032", TOPIC_A, "Approximation of a conjugate sum", "Medium", "Multi-step computation MCQ",
  r"Correct to four decimal places, the value of $(1.01)^{10} + (0.99)^{10}$ is",
  r"$2.0090$",
  [(r"$2.0000$", r"Believes every term except the constant cancels in the sum."),
   (r"$2.0045$", r"Keeps $\binom{10}{2}(0.01)^2 = 0.0045$ only once, forgetting it occurs in both expansions."),
   (r"$2.2000$", r"Keeps the terms $\pm 10(0.01)$ with the same sign so they add: $2 + 0.2$.")],
  r"In $(1+h)^{10} + (1-h)^{10}$ the odd powers of $h$ cancel: the sum is $2\left[1 + 45h^2 + 210h^4 + \dots\right]$ with $h = 0.01$, i.e. $2[1 + 0.0045 + 0.0000021 + \dots] = 2.0090042\dots$, which is $2.0090$ to four decimal places.",
  r"Misjudging which terms cancel in a sum of conjugate expansions.",
  "U05-C-approx-sum-cancel", "Cancellation pattern plus approximation.",
  check=lambda: _rnd(Rational(101, 100)**10 + Rational(99, 100)**10, 4),
  values=[Rational('2.0090'), Rational('2.0000'), Rational('2.0045'), Rational('2.2000')])

q("U05-C-033", TOPIC_A, "Least exponent for a comparison", "Medium", "Inverse/parameter MCQ",
  r"The least natural number $n$ for which $(1.01)^{n} > 1.1$ is",
  r"$10$",
  [(r"$11$", r"Uses only $(1.01)^n \ge 1 + 0.01n$ and demands $1 + 0.01n > 1.1$, ignoring the positive higher terms at $n = 10$."),
   (r"$5$", r"Uses $\binom{n}{2}(0.01)$ in place of $\binom n2 (0.01)^2$ for the third term."),
   (r"$12$", r"Index slip: uses $1 + 0.01(n-1)$ for the first two terms, then needs $n - 1 > 10$.")],
  r"For $n = 10$: $(1.01)^{10} = 1 + 0.1 + 45(0.0001) + \dots > 1.1$. For $n = 9$: $(1.01)^9 = 1 + 0.09 + 36(0.0001) + 84(10^{-6}) + \dots \approx 1.0937 < 1.1$, and smaller $n$ give smaller values. So the least $n$ is $10$.",
  r"Treating the two-term bound as an equality.",
  "U05-C-compare-least-n", "Check both the bound at $n = 10$ and failure at $n = 9$.",
  check=lambda: Integer(next(k for k in range(1, 200) if Rational(101, 100)**k > Rational(11, 10))),
  values=[10, 11, 5, 12])

q("U05-C-034", TOPIC_A, "Locating a power between integers", "Medium", "Multi-step computation MCQ",
  r"The number $(1.1)^{10}$ lies in the interval",
  r"$(2, 3)$",
  [(r"$(1, 2)$", r"Uses $(1+x)^n \approx 1 + x^n$, i.e. $1 + (0.1)^{10}$."),
   (r"$(3, 4)$", r"Uses $\binom{10}{2} = 90$ (no division by $2$): $1 + 1 + 0.9 + 0.12 > 3$."),
   (r"$(4, 5)$", r"Uses permutations $^{10}P_r$ in place of $\binom{10}{r}$: $1 + 1 + 0.9 + 0.72 + 0.504 > 4$.")],
  r"$(1.1)^{10} = 1 + 10(0.1) + 45(0.01) + \dots > 2$. Also $\binom{10}{r}(0.1)^r \le \frac{1}{r!}$, so $(1.1)^{10} < 1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \dots < 1 + 1 + \frac12 + \frac14 + \dots = 3$. Hence $(1.1)^{10} \in (2, 3)$.",
  r"Treating small-base powers as nearly constant, or misusing binomial coefficients.",
  "U05-C-compare-interval", "Lower bound from two terms, upper bound by comparing with a geometric series.",
  check=lambda: Interval.open(floor(Rational(11, 10)**10), floor(Rational(11, 10)**10) + 1),
  values=[Interval.open(2, 3), Interval.open(1, 2), Interval.open(3, 4), Interval.open(4, 5)])

def _c35():
    codes = set()
    for m in range(1, 7):
        v = expand((sqrt(3)+1)**(2*m) - (sqrt(3)-1)**(2*m))
        if not v.is_rational:
            codes.add(1)
        elif v.is_integer and v > 0:
            codes.add(2 if v % 2 == 0 else 3)
        else:
            codes.add(4)
    return Integer(codes.pop()) if len(codes) == 1 else None
q("U05-C-035", TOPIC_F, "Nature of a conjugate difference", "Medium", "Conceptual/application MCQ",
  r"For every natural number $n$, the number $(\sqrt{3}+1)^{2n} - (\sqrt{3}-1)^{2n}$ is",
  r"an irrational number",
  [(r"an even natural number", r"Confuses the difference with the sum $(\sqrt3+1)^{2n} + (\sqrt3-1)^{2n}$, which is an even integer."),
   (r"an odd natural number", r"Uses the integer-part result for the sum and subtracts $1$."),
   (r"a non-integer rational number", r"Thinks the surds cancel but a fraction is left over.")],
  r"$(\sqrt3+1)^{2n} - (\sqrt3-1)^{2n} = (4+2\sqrt3)^n - (4-2\sqrt3)^n = 2\sum_{k \text{ odd}}\binom nk 4^{n-k}(2\sqrt3)^k$. Each surviving term is a positive integer times $\sqrt3$, so the number equals $\sqrt3$ times a positive integer, which is irrational.",
  r"Confusing the sum and the difference of conjugate powers.",
  "U05-C-surd-nature", "Identify which terms survive and their surd factor.",
  check=_c35, values=[1, 2, 3, 4], cognitive="Understanding")

# ---------------------------------------------------------------- DIFFICULT

q("U05-C-036", TOPIC_R, "Sum of powers of 7 plus and minus 1", "Difficult", "Multi-step computation MCQ",
  r"The remainder when $6^{2025} + 8^{2025}$ is divided by $49$ is",
  r"$28$",
  [(r"$2$", r"Uses the even-exponent pattern, where the constants add to $2$ and the $7n$ terms cancel."),
   (r"$0$", r"Takes the sign of the linear term of $(7-1)^{2025}$ as negative, so the $7n$ terms cancel and the constants give $0$."),
   (r"$14$", r"Counts the linear term $7 \cdot 2025$ from only one of the two expansions.")],
  r"Modulo $49$, $(7+1)^n \equiv 1 + 7n$ and $(7-1)^n \equiv (-1)^n + 7n(-1)^{n-1}$. For $n = 2025$ (odd) the sum is $1 + 7n - 1 + 7n = 14n$. Now $14 \cdot 2025 = 7 \cdot 4050$ and $4050 = 7 \cdot 578 + 4$, so $14n \equiv 7 \cdot 4 = 28 \pmod{49}$.",
  r"Sign of $(-1)^{n-1}$ in the linear term, and reducing $14n$ modulo $49$.",
  "U05-C-rem-sum-pm-49", "Two expansions to second order, parity casework and a reduction.",
  check=lambda: Mod(Integer(6)**2025 + Integer(8)**2025, 49), values=[28, 2, 0, 14],
  numerical=dict(question=r"The remainder when $6^{2025} + 8^{2025}$ is divided by $49$ is", answer=28))

q("U05-C-037", TOPIC_R, "Remainder of a tower of powers", "Difficult", "Multi-step computation MCQ",
  r"The remainder when $32^{32^{32}}$ is divided by $7$ is",
  r"$4$",
  [(r"$2$", r"Takes $32^{32} = (33-1)^{32} \equiv -1 \pmod 3$, a parity slip, so the exponent is $\equiv 2$ and $4^2 = 16 \equiv 2$."),
   (r"$1$", r"Assumes the exponent $32^{32}$ is a multiple of $3$, so $4^{3k} \equiv 1$."),
   (r"$3$", r"Writes $32 \equiv -3 \pmod 7$ and treats the exponent as odd, getting $-3^{32^{32}} \equiv -4 \equiv 3$.")],
  r"$32 \equiv 4 \pmod 7$ and $4^3 = 64 = 63 + 1$, so powers of $4$ repeat with period $3$. The exponent $32^{32} = (33-1)^{32} \equiv (-1)^{32} = 1 \pmod 3$, so $32^{32} = 3k + 1$. Then $32^{32^{32}} \equiv 4^{3k+1} = 4(63+1)^k \equiv 4 \pmod 7$.",
  r"Reducing the exponent modulo the wrong number or with the wrong sign.",
  "U05-C-rem-tower", "Two nested binomial reductions.",
  check=lambda: Integer(pow(32, 32**32, 7)), values=[4, 2, 1, 3],
  numerical=dict(question=r"The remainder when $32^{32^{32}}$ is divided by $7$ is", answer=4))

q("U05-C-038", TOPIC_L, "Last two digits of a power of 2", "Difficult", "Multi-step computation MCQ",
  r"The last two digits of $2^{100}$ are",
  r"$76$",
  [(r"$51$", r"Keeps only two terms of $(25-1)^{10}$: $1 - 250 \equiv 51$, assuming higher powers of $25$ vanish modulo $100$."),
   (r"$26$", r"Gets $\sum_{k \ge 1}\binom{10}{k}(-1)^{10-k} = +1$ in place of $-1$, so $1 + 25 = 26$."),
   (r"$24$", r"Reaches $1 - 25 = -24$ and drops the minus sign.")],
  r"$2^{100} = 1024^{10} \equiv 24^{10} = (25-1)^{10} \pmod{100}$. Since $25^k \equiv 25 \pmod{100}$ for $k \ge 1$, $(25-1)^{10} \equiv 1 + 25\sum_{k=1}^{10}\binom{10}{k}(-1)^{10-k} = 1 + 25(0 - 1) = -24 \equiv 76$. So the last two digits are $76$.",
  r"Assuming $25^2$ vanishes modulo $100$ as $50^2$ does.",
  "U05-C-last2-power-of-2", "Non-obvious base choice and the behaviour of powers of 25.",
  check=lambda: Mod(Integer(2)**100, 100), values=[76, 51, 26, 24],
  numerical=dict(question=r"The number formed by the last two digits of $2^{100}$ is", answer=76))

q("U05-C-039", TOPIC_R, "Remainder of a negative-offset base modulo a square", "Difficult", "Multi-step computation MCQ",
  r"The remainder when $2023^{2026}$ is divided by $2024^{2}$ is",
  r"$4092529$",
  [(r"$4049$", r"Expands as if the base were $1 + 2024$, taking the linear term with a plus sign: $1 + 2 \cdot 2024$."),
   (r"$4047$", r"Reaches $1 - 4048 = -4047$ and drops the minus sign in place of adding $2024^2$."),
   (r"$4094553$", r"Reduces $2026 \cdot 2024$ as $1 \cdot 2024$, getting $1 - 2024 = -2023$ and then $2024^2 - 2023$.")],
  r"$2023^{2026} = (2024-1)^{2026} = \sum_k \binom{2026}{k}2024^k(-1)^{2026-k} \equiv 1 - 2026 \cdot 2024 \pmod{2024^2}$, since terms with $k \ge 2$ are multiples of $2024^2$. As $2026 = 2024 + 2$, $2026 \cdot 2024 \equiv 2 \cdot 2024 = 4048$, so $2023^{2026} \equiv 1 - 4048 = -4047$. Adding $2024^2 = 4096576$ gives the remainder $4096576 - 4047 = 4092529$.",
  r"Mishandling the negative residue, or the sign of the linear term for a base just below the modulus root.",
  "U05-C-rem-square-modulus", "Expansion modulo a square with a negative constant, reduction of the linear multiplier, and conversion of a negative residue.",
  check=lambda: Mod(Integer(2023)**2026, Integer(2024)**2), values=[4092529, 4049, 4047, 4094553],
  numerical=dict(question=r"The remainder when $2023^{2026}$ is divided by $2024^{2}$ is", answer=4092529))

def _c40():
    I = floor(expand((sqrt(3)+1)**8))
    return Integer(multiplicity(2, I + 1))
q("U05-C-040", TOPIC_F, "Power of 2 dividing the integer just above", "Difficult", "Multi-step computation MCQ",
  r"Let $I$ be the greatest integer less than or equal to $(\sqrt{3}+1)^{8}$. If $2^{k}$ is the highest power of $2$ that divides $I + 1$, then $k$ equals",
  r"$5$",
  [(r"$4$", r"Pulls out $2^4$ from $(4 \pm 2\sqrt3)^4$ but misses that $(2+\sqrt3)^4 + (2-\sqrt3)^4 = 194$ is even."),
   (r"$9$", r"Uses the general bound $2^{n+1}$ for $(\sqrt3+1)^{2n}$ with $n = 8$ in place of $n = 4$."),
   (r"$0$", r"Takes $I = 3104$, forgetting to subtract $1$, so $I + 1 = 3105$ is odd.")],
  r"$(\sqrt3+1)^8 + (\sqrt3-1)^8 = (4+2\sqrt3)^4 + (4-2\sqrt3)^4 = 2^4\left[(2+\sqrt3)^4 + (2-\sqrt3)^4\right] = 16 \cdot 194 = 3104$. As $0 < (\sqrt3-1)^8 < 1$, $I = 3103$ and $I + 1 = 3104 = 2^5 \cdot 97$. So $k = 5$.",
  r"Losing a factor of 2 from the even conjugate sum.",
  "U05-C-int-part-power2", "Integer part, factoring the conjugate sum, and exact power of 2.",
  check=_c40, values=[5, 4, 9, 0],
  numerical=dict(question=r"Let $I$ be the greatest integer less than or equal to $(\sqrt{3}+1)^{8}$. If $2^{k}$ is the highest power of $2$ that divides $I + 1$, then $k$ is", answer=5))

def _c41():
    vals = []
    for m in (1, 2, 3):
        R = (6*sqrt(6)+14)**(2*m+1)
        vals.append(expand(expand(R) * _frac(R)))
    base = integer_nthroot(int(vals[0]), 3)[0]
    assert all(vals[m-1] == Integer(base)**(2*m+1) for m in (1, 2, 3))
    return Integer(base)**(2*n+1)
q("U05-C-041", TOPIC_F, "Product of a number and its fractional part", "Difficult", "Multi-step computation MCQ",
  r"For a natural number $n$, let $R = (6\sqrt{6}+14)^{2n+1}$ and $f = R - [R]$, where $[\,\cdot\,]$ denotes the greatest integer function. Then $Rf$ equals",
  r"$20^{2n+1}$",
  [(r"$1$", r"Assumes the conjugate product is $1$, as for $2 \pm \sqrt3$."),
   (r"$412^{2n+1}$", r"Adds $216 + 196$ in place of subtracting when multiplying the conjugates."),
   (r"$20^{n}$", r"Finds the conjugate product $20$ but halves the exponent, confusing $(6\sqrt6 \pm 14)^{2n+1}$ with a square.")],
  r"Let $f' = (6\sqrt6 - 14)^{2n+1}$; since $6\sqrt6 = \sqrt{216}$ lies between $14$ and $15$, $0 < f' < 1$. Because the exponent is odd, $R - f' = (14+6\sqrt6)^{2n+1} + (14-6\sqrt6)^{2n+1}$, in which the $\sqrt6$ terms cancel, so it is an integer. Hence $f = f'$ and $Rf = (216 - 196)^{2n+1} = 20^{2n+1}$.",
  r"Using $f = 1 - f'$ or mishandling the sign of the conjugate for odd powers.",
  "U05-C-frac-product-power", "General odd exponent; needs the sign analysis and the integrality argument.",
  check=_c41, values=[20**(2*n+1), 1, 412**(2*n+1), 20**n])

q("U05-C-042", TOPIC_A, "Comparing very large powers", "Difficult", "Statement-based MCQ",
  r"Statement I: $1001^{999} < 1000^{1000}$. Statement II: $\left(1 + \frac{1}{m}\right)^{m} < 3$ for every natural number $m$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Bounds each term $\binom mr \frac{1}{m^r}$ only by $1$ and so doubts the bound $3$."),
   (ST_FT, r"Thinks the larger base $1001$ dominates despite the smaller exponent."),
   (ST_FF, r"Makes both misjudgements.")],
  r"For Statement II, $\binom mr \frac{1}{m^r} \le \frac{1}{r!} \le \frac{1}{2^{r-1}}$, so $\left(1+\frac1m\right)^m < 1 + 1 + \frac12 + \frac14 + \dots = 3$; it is true. For Statement I, $\frac{1001^{999}}{1000^{1000}} = \frac{1}{1001}\left(1 + \frac{1}{1000}\right)^{1000} < \frac{3}{1001} < 1$, so it is true as well.",
  r"Judging large powers by the base alone.",
  "U05-C-compare-large-powers", "Requires the bound $(1+1/m)^m < 3$ and rewriting the ratio.",
  check=lambda: (bool(Integer(1001)**999 < Integer(1000)**1000),
                 all(Rational(m+1, m)**m < 3 for m in range(1, 400))),
  values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Analysis")

def _c43():
    R = expand((8+3*sqrt(7))**20)
    fp = expand((8-3*sqrt(7))**20)
    I = floor(R)
    f = R - I
    return (bool(simplify(f - fp) == 0), bool(I % 4 == 1))
q("U05-C-043", TOPIC_F, "Fractional part and the integral part modulo 4", "Difficult", "Statement-based MCQ",
  r"Let $(8+3\sqrt{7})^{20} = I + f$, where $I$ is an integer and $0 \le f < 1$. Statement I: $f = (8-3\sqrt{7})^{20}$. Statement II: $I$ leaves remainder $1$ when divided by $4$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Applies the odd-exponent rule $f = f'$ to the even exponent $20$ for Statement I, but handles Statement II correctly."),
   (ST_TF, r"Takes $f = (8-3\sqrt7)^{20}$ and then $I$ equal to the even conjugate sum $S \equiv 2 \pmod 4$, so rejects Statement II."),
   (ST_FF, r"Gets $f = 1 - (8-3\sqrt7)^{20}$ and $I = S - 1$ right, but treats every term of $S/2$ as even, overlooking the odd last term $63^{10}$, so takes $S \equiv 0$ and $I \equiv 3 \pmod 4$.")],
  r"Let $f' = (8-3\sqrt7)^{20} \in (0,1)$ and $S = (8+3\sqrt7)^{20} + f' = 2\sum_{r \text{ even}}\binom{20}{r}8^{20-r}(3\sqrt7)^r$, an integer. Then $f + f' = S - I$ is an integer in $(0,2)$, so $f + f' = 1$ and $f = 1 - f' \ne f'$ (as $f' \ne \frac12$); Statement I is false. In $S/2$ every term with $r < 20$ has a positive power of $8$ and is even, while the $r = 20$ term is $(3\sqrt7)^{20} = 63^{10}$, odd. So $S/2$ is odd, $S \equiv 2 \pmod 4$, and $I = S - 1 \equiv 1 \pmod 4$; Statement II is true.",
  r"Using $f = f'$ for an even exponent, and taking $I$ equal to the conjugate sum.",
  "U05-C-frac-statement", "Fractional-part argument plus a parity analysis of the conjugate sum modulo 4.",
  check=_c43, values=[(False, True), (True, True), (True, False), (False, False)], cognitive="Analysis")

q("U05-C-044", TOPIC_L, "Last two digits after reducing the base", "Difficult", "Multi-step computation MCQ",
  r"The last two digits of $13^{2026}$ are",
  r"$09$",
  [(r"$91$", r"Expands $(1-70)^{1013}$ in place of $(-1+70)^{1013}$: $1 - 1013 \cdot 70 \equiv 1 - 10 \equiv 91$."),
   (r"$99$", r"Keeps only $(-1)^{1013}$, assuming the $70$ term vanishes modulo $100$."),
   (r"$11$", r"Takes the constant term as $+1$, ignoring that $1013$ is odd: $1 + 10 = 11$.")],
  r"$13^{2026} = 169^{1013} \equiv 69^{1013} = (70-1)^{1013} \pmod{100}$. Terms with $70^2$ or higher vanish, leaving $\binom{1013}{1}70(-1)^{1012} + (-1)^{1013} = 70910 - 1 \equiv 10 - 1 = 9$. So the last two digits are $09$.",
  r"Sign of the constant term and keeping the $70$ term.",
  "U05-C-last2-reduce-base", "Reduce the base, choose a near multiple of 10, then track two signed terms.",
  check=lambda: Mod(Integer(13)**2026, 100), values=[9, 91, 99, 11],
  numerical=dict(question=r"The number formed by the last two digits of $13^{2026}$ is", answer=9))

q("U05-C-045", TOPIC_R, "Polynomial remainder by a squared linear factor", "Difficult", "Multi-step computation MCQ",
  r"The remainder when $x^{2026}$ is divided by $(x+1)^{2}$ is",
  r"$-2026x-2025$",
  [(r"$2026x+2027$", r"Takes the linear term $\binom{2026}{1}(x+1)(-1)^{2025}$ with a plus sign: $1 + 2026(x+1)$."),
   (r"$-2025x-2024$", r"Uses $2025$ as the coefficient of $(x+1)$, an index slip."),
   (r"$-2026x+1$", r"Writes the remainder as $1 - 2026x$, replacing $(x+1)$ by $x$ in the linear term.")],
  r"Write $x = (x+1) - 1$. Then $x^{2026} = \sum_k \binom{2026}{k}(x+1)^k(-1)^{2026-k}$, and modulo $(x+1)^2$ only $k = 0, 1$ remain: $1 + 2026(x+1)(-1)^{2025} = 1 - 2026x - 2026 = -2026x - 2025$.",
  r"Sign of $(-1)^{n-1}$ in the linear term.",
  "U05-C-poly-remainder", "Substitution with a negative constant and sign tracking.",
  check=lambda: rem(x**2026, (x+1)**2, x), values=[-2026*x-2025, 2026*x+2027, -2025*x-2024, -2026*x+1])

q("U05-C-046", TOPIC_R, "Counting exponents for divisibility by 128", "Difficult", "Inverse/parameter MCQ",
  r"The number of natural numbers $n \le 100$ for which $9^{n} - 8n - 1$ is divisible by $128$ is",
  r"$50$",
  [(r"$100$", r"Recalls that $9^n - 8n - 1$ is always divisible by $64$ and assumes the same for $128$."),
   (r"$25$", r"Requires $4 \mid n$, missing the case $n \equiv 1 \pmod 4$ where $\binom n2$ is also even."),
   (r"$49$", r"Excludes $n = 1$, forgetting that $0$ is divisible by $128$.")],
  r"$9^n - 8n - 1 = \binom n2 8^2 + \binom n3 8^3 + \dots \equiv 64\binom n2 \pmod{128}$, since $8^3 = 512$ is a multiple of $128$. So we need $\binom n2 = \frac{n(n-1)}{2}$ even, i.e. $n \equiv 0$ or $1 \pmod 4$. From $1$ to $100$ there are $25 + 25 = 50$ such $n$ (including $n = 1$, where the value is $0$).",
  r"Overgeneralising the divisibility by $64$.",
  "U05-C-div-count-128", r"Expansion modulo 128 then a parity condition on $\binom n2$ and a count.",
  check=lambda: Integer(sum(1 for k in range(1, 101) if Mod(Integer(9)**k - 8*k - 1, 128) == 0)), values=[50, 100, 25, 49],
  numerical=dict(question=r"The number of natural numbers $n \le 100$ for which $9^{n} - 8n - 1$ is divisible by $128$ is", answer=50))
