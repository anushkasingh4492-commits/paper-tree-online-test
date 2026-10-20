import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

from itertools import permutations as _perms, product as _product
from sympy.utilities.iterables import multiset_permutations as _mp

# ---------------------------------------------------------------- helpers


def words(s):
    """All distinct arrangements of the letters of s, in dictionary order."""
    return [''.join(p) for p in _mp(sorted(s))]


def rank(w):
    return words(w).index(w) + 1


def wcode(w):
    """Encode a capital-letter word as an integer so that options can be compared."""
    return Integer(int(''.join('%02d' % (ord(c) - 64) for c in w)))


def adjacent(seq, a, b):
    i, j = seq.index(a), seq.index(b)
    return abs(i - j) == 1


def has_adjacent_equal(seq, ch):
    return any(seq[k] == ch and seq[k + 1] == ch for k in range(len(seq) - 1))


def ff_(n, r):
    return factorial(n) / factorial(n - r)


_n, _r = symbols('n r', positive=True, integer=True)

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."
PDEF = r"Here $P(n, r)$ denotes the number of permutations of $n$ distinct objects taken $r$ at a time. "

T = "Fundamental principle of counting and permutations"

# ================================================================ EASY (16)

q("U04-A-001", T, "Fundamental principle of counting: answer sheets", "Easy",
  "Single-step computation MCQ",
  r"A test has $6$ true/false questions followed by $2$ multiple choice questions, each with $4$ options. A student answers every question, marking exactly one choice for each. The number of different ways of filling the answer sheet is",
  r"$1024$",
  [(r"$80$", r"Adds the counts for the two parts, $2^6 + 4^2 = 64 + 16$, rather than multiplying them."),
   (r"$576$", r"Swaps bases and exponents, computing $6^2 \cdot 2^4 = 36 \cdot 16$."),
   (r"$20$", r"Adds the choices question by question, $6 \cdot 2 + 2 \cdot 4$, rather than multiplying.")],
  r"Each true/false question can be answered in $2$ ways and each multiple choice question in $4$ ways, independently. By the multiplication principle the number of ways is $2^6 \cdot 4^2 = 64 \cdot 16 = 1024$.",
  "Adding the choices of independent stages instead of multiplying them.",
  "U04-A-fpc-product", "One application of the multiplication principle.",
  check=lambda: Integer(len(list(_product(*([range(2)] * 6 + [range(4)] * 2))))),
  values=[1024, 80, 576, 20], cognitive="Application")

q("U04-A-002", T, "Three-digit numbers with distinct digits", "Easy",
  "Single-step computation MCQ",
  r"The number of three-digit natural numbers in which all three digits are different is",
  r"$648$",
  [(r"$720$", r"Uses $P(10, 3) = 720$, allowing $0$ in the hundreds place."),
   (r"$900$", "Counts all three-digit numbers, ignoring the distinct-digit condition."),
   (r"$504$", r"Excludes the digit $0$ altogether, using $P(9, 3) = 504$.")],
  r"The hundreds digit can be any of $1$ to $9$ ($9$ ways). The tens digit can be any of the remaining $9$ digits (now including $0$), and the units digit any of the remaining $8$. Hence $9 \cdot 9 \cdot 8 = 648$.",
  "Forgetting that $0$ cannot occupy the leading place, or excluding $0$ completely.",
  "U04-A-digits-distinct", "Single multiplication with the leading-zero restriction.",
  check=lambda: Integer(sum(1 for m in range(100, 1000) if len(set(str(m))) == 3)),
  values=[648, 720, 900, 504], cognitive="Application",
  numerical=dict(question=r"The number of three-digit natural numbers in which all three digits are different is", answer=648))

q("U04-A-003", T, "Arrangements with repeated letters", "Easy",
  "Single-step computation MCQ",
  r"The number of distinct arrangements of all the letters of the word BANANA is",
  r"$60$",
  [(r"$720$", r"Treats all six letters as distinct, giving $6!$."),
   (r"$120$", r"Divides only by $3!$ for the three A's, ignoring the two N's."),
   (r"$360$", r"Divides only by $2!$ for the two N's, ignoring the three A's.")],
  r"BANANA has $6$ letters with A three times and N twice. The number of distinct arrangements is $\frac{6!}{3!\,2!} = \frac{720}{12} = 60$.",
  "Not dividing by the factorial of every repeated letter.",
  "U04-A-identical-word", "Direct use of the formula for identical objects.",
  check=lambda: Integer(len(set(_perms("BANANA")))),
  values=[60, 720, 120, 360], cognitive="Application",
  numerical=dict(question=r"The number of distinct arrangements of all the letters of the word BANANA is", answer=60))

def _c4():
    n = symbols('n', integer=True)
    sols = solve(expand(n*(n-1)*(n-2)*(n-3) - 20*n*(n-1)), n)
    return [s for s in sols if s >= 4][0]
q("U04-A-004", T, "Equation in P(n, r)", "Easy",
  "Inverse/parameter MCQ",
  PDEF + r"If $P(n, 4) = 20\, P(n, 2)$, where $n \ge 4$ is an integer, then $n$ equals",
  r"$7$",
  [(r"$6$", r"Cancels wrongly and writes $(n-1)(n-2) = 20$, which gives $n = 6$."),
   (r"$8$", r"Takes the leftover factors as $(n-3)(n-4) = 20$, which gives $n = 8$."),
   (r"$5$", r"Treats the ratio $\frac{P(n,4)}{P(n,2)}$ as $n(n-1)$, the factors that should cancel, so $n(n-1) = 20$ gives $n = 5$.")],
  r"$P(n, 4) = n(n-1)(n-2)(n-3)$ and $P(n, 2) = n(n-1)$. Dividing, $(n-2)(n-3) = 20$, so $n^2 - 5n - 14 = 0$, i.e. $(n-7)(n+2) = 0$. With $n \ge 4$, $n = 7$.",
  "Cancelling the wrong factors when dividing two permutation expressions.",
  "U04-A-Pnr-equation", "One cancellation and a quadratic.",
  check=_c4, values=[7, 6, 8, 5], cognitive="Application",
  numerical=dict(question=r"If $P(n, 4) = 20\, P(n, 2)$, where $n \ge 4$ is an integer and $P(n, r)$ denotes the number of permutations of $n$ distinct objects taken $r$ at a time, then $n$ is", answer=7))

q("U04-A-005", T, "Rank of a word with distinct letters", "Easy",
  "Single-step computation MCQ",
  r"All the arrangements of the letters of the word TIME are listed in dictionary order. The position (rank) of the word TIME in this list is",
  r"$22$",
  [(r"$21$", "Counts the $21$ words that come before TIME but does not add $1$ for the word itself."),
   (r"$19$", r"Counts only the $18$ words beginning with E, I or M and then adds $1$, ignoring the words TE.. that precede TIME."),
   (r"$18$", r"Counts only the $3 \cdot 3! = 18$ words beginning with E, I or M.")],
  r"In alphabetical order the letters are E, I, M, T. Words beginning with E, I or M: $3 \cdot 3! = 18$. Among words beginning with T, those beginning TE come before TI: $2! = 2$. Among words beginning TI, the word TIEM comes before TIME: $1$. So $18 + 2 + 1 = 21$ words precede TIME and its rank is $22$.",
  "Forgetting to add $1$ for the word itself, or stopping after the first letter.",
  "U04-A-rank-distinct", "Short positional count with four letters.",
  check=lambda: Integer(rank("TIME")),
  values=[22, 21, 19, 18], cognitive="Application")

q("U04-A-006", T, "Arrangements with a group kept together", "Easy",
  "Single-step computation MCQ",
  r"The number of ways in which $5$ boys and $3$ girls can stand in a row so that all three girls stand together is",
  r"$4320$",
  [(r"$720$", r"Treats the girls as one unit, giving $6!$, but does not arrange the girls within the unit."),
   (r"$36000$", r"Computes $8! - 6!\,3!$, the number of arrangements in which the girls are not all together."),
   (r"$14400$", r"Uses the gap method $5! \cdot P(6, 3)$, which counts arrangements with no two girls together.")],
  r"Tie the three girls into one unit. The $5$ boys and this unit are $6$ units, arranged in $6! = 720$ ways, and the girls inside the unit in $3! = 6$ ways. Total $720 \cdot 6 = 4320$.",
  "Forgetting the internal arrangement of a block of objects kept together.",
  "U04-A-together", "Block method in one step.",
  check=lambda: Integer(sum(
      1 for p in _perms(["b1", "b2", "b3", "b4", "b5", "g1", "g2", "g3"])
      if max(p.index(g) for g in ("g1", "g2", "g3")) - min(p.index(g) for g in ("g1", "g2", "g3")) == 2)),
  values=[4320, 720, 36000, 14400], cognitive="Application")

q("U04-A-007", T, "Signals with flags", "Easy",
  "Single-step computation MCQ",
  r"A signal is made by hoisting some flags one above another on a vertical pole, and the order of the flags matters. Using $5$ different flags, the number of signals that use at least $2$ flags is",
  r"$320$",
  [(r"$325$", r"Also counts the $5$ signals that use a single flag."),
   (r"$120$", r"Counts only the signals using all $5$ flags."),
   (r"$26$", r"Uses selections $C(5,2) + C(5,3) + C(5,4) + C(5,5)$, ignoring the order of the flags.")],
  r"Signals with $r$ flags number $P(5, r)$. So the total is $P(5,2) + P(5,3) + P(5,4) + P(5,5) = 20 + 60 + 120 + 120 = 320$.",
  "Ignoring order, or including signals that use fewer flags than allowed.",
  "U04-A-signals", "Sum of four permutation counts.",
  check=lambda: Integer(sum(len(list(_perms(range(5), k))) for k in range(2, 6))),
  values=[320, 325, 120, 26], cognitive="Application")

q("U04-A-008", T, "Word formation with fixed end letters", "Easy",
  "Single-step computation MCQ",
  r"The number of words, with or without meaning, that can be formed using all the letters of the word ORANGE, each exactly once, which begin with a vowel and end with a consonant, is",
  r"$216$",
  [(r"$432$", "Also counts words that begin with a consonant and end with a vowel, doubling the count."),
   (r"$360$", r"Applies only the first condition, $3 \cdot 5!$."),
   (r"$1080$", r"Fixes both end letters ($3 \cdot 3$ ways) but then arranges the rest as $5!$ although only $4$ letters remain.")],
  r"ORANGE has vowels O, A, E and consonants R, N, G. The first letter can be chosen in $3$ ways, the last letter in $3$ ways, and the remaining $4$ letters fill the middle in $4! = 24$ ways. Total $3 \cdot 3 \cdot 24 = 216$.",
  "Miscounting the letters left after fixing the end positions.",
  "U04-A-fixed-ends", "Fix two positions, arrange the rest.",
  check=lambda: Integer(sum(1 for w in _perms("ORANGE") if w[0] in "OAE" and w[-1] in "RNG")),
  values=[216, 432, 360, 1080], cognitive="Application")

def _c9():
    s1 = all(ff_(n, n) == ff_(n, n - 1) for n in range(1, 13))
    s2 = all(ff_(n, r) == ff_(n - 1, r) + ff_(n - 1, r - 1) for n in range(2, 13) for r in range(1, n))
    return (bool(s1), bool(s2))
q("U04-A-009", T, "Identities in P(n, r)", "Easy",
  "Statement-based MCQ",
  r"Here $P(n, r)$ denotes the number of permutations of $n$ distinct objects taken $r$ at a time. Statement I: $P(n, n) = P(n, n-1)$ for every integer $n \ge 1$. Statement II: $P(n, r) = P(n-1, r) + P(n-1, r-1)$ for all integers $n \ge 2$ and $1 \le r \le n-1$." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II by analogy with Pascal's rule for $C(n, r)$; for permutations the correct rule is $P(n, r) = P(n-1, r) + r\,P(n-1, r-1)$."),
   (ST_FF, r"Rejects Statement I, thinking $P(n, n-1) = (n-1)!$, and also rejects Statement II."),
   (ST_FT, r"Thinks $P(n, n-1) = (n-1)!$, so rejects Statement I, and accepts the Pascal-type rule in Statement II.")],
  r"$P(n, n) = n!$ and $P(n, n-1) = \frac{n!}{1!} = n!$, so Statement I is true. For Statement II take $n = 3$, $r = 2$: $P(3, 2) = 6$ but $P(2, 2) + P(2, 1) = 2 + 2 = 4$, so it is false. The correct relation is $P(n, r) = P(n-1, r) + r\,P(n-1, r-1)$.",
  "Carrying Pascal's rule for combinations over to permutations unchanged.",
  "U04-A-Pnr-statement", "Two short identity checks.",
  check=_c9, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding")

q("U04-A-010", T, "No two of a group together (gap method)", "Easy",
  "Single-step computation MCQ",
  r"The number of ways in which $4$ boys and $3$ girls can stand in a row so that no two girls stand next to each other is",
  r"$1440$",
  [(r"$4320$", r"Computes $7! - 5!\,3!$, which removes only the arrangements with all three girls together."),
   (r"$144$", r"Arranges boys and girls separately, $4! \cdot 3!$, without placing the girls in the gaps."),
   (r"$240$", r"Uses $4! \cdot C(5, 3)$, choosing the gaps but not arranging the girls in them.")],
  r"Arrange the $4$ boys in $4! = 24$ ways. This creates $5$ gaps (including the two ends). Place the $3$ girls in $3$ different gaps in $P(5, 3) = 60$ ways. Total $24 \cdot 60 = 1440$.",
  "Treating 'no two together' as 'not all together'.",
  "U04-A-gap-method", "Standard gap method in two steps.",
  check=lambda: Integer(sum(1 for p in _perms(["b1", "b2", "b3", "b4", "g1", "g2", "g3"])
                            if not any(p[k][0] == "g" and p[k + 1][0] == "g" for k in range(6)))),
  values=[1440, 4320, 144, 240], cognitive="Application")

q("U04-A-011", T, "Number formation with repetition", "Easy",
  "Single-step computation MCQ",
  r"Using the digits $0, 1, 2, 3, 4, 5$, with repetition allowed, the number of four-digit numbers that can be formed is",
  r"$1080$",
  [(r"$1296$", r"Uses $6^4$, allowing $0$ in the thousands place."),
   (r"$300$", r"Counts numbers without repetition, $5 \cdot P(5, 3)$."),
   (r"$625$", r"Uses only $5$ choices for every place, $5^4$, excluding $0$ everywhere.")],
  r"The thousands digit can be any of $1, \dots, 5$ ($5$ ways); each of the other three places can take any of the $6$ digits. Total $5 \cdot 6^3 = 1080$.",
  "Allowing a leading zero, or excluding zero from every place.",
  "U04-A-digits-repetition", "One multiplication with a leading-digit restriction.",
  check=lambda: Integer(sum(1 for t in _product("012345", repeat=4) if t[0] != "0")),
  values=[1080, 1296, 300, 625], cognitive="Application")

q("U04-A-012", T, "Ratio of consecutive P(n, r)", "Easy",
  "Single-step computation MCQ",
  PDEF + r"For integers $1 \le r \le n$, the ratio $\frac{P(n, r)}{P(n, r-1)}$ equals",
  r"$n - r + 1$",
  [(r"$\frac{1}{n - r + 1}$", "Inverts the ratio of the factorials in the denominators."),
   (r"$\frac{n - r + 1}{r}$", r"Uses the ratio $\frac{C(n, r)}{C(n, r-1)}$ for combinations."),
   (r"$n - r$", r"Takes the last factor of $P(n, r) = n(n-1)\cdots$ as $n - r$.")],
  r"$P(n, r) = \frac{n!}{(n-r)!}$ and $P(n, r-1) = \frac{n!}{(n-r+1)!}$. Hence the ratio is $\frac{(n-r+1)!}{(n-r)!} = n - r + 1$; it is the extra factor in $P(n, r) = n(n-1)\cdots(n-r+1)$.",
  "Confusing the last factor of $P(n, r)$ or mixing up with the combination ratio.",
  "U04-A-Pnr-identity", "Single factorial simplification.",
  check=lambda: combsimp(ff_(_n, _r) / ff_(_n, _r - 1)),
  values=[_n - _r + 1, 1 / (_n - _r + 1), (_n - _r + 1) / _r, _n - _r], cognitive="Understanding")

q("U04-A-013", T, "Codes with letters and digits", "Easy",
  "Single-step computation MCQ",
  r"A vehicle code consists of $2$ English letters followed by $3$ digits. Letters may repeat; the three digits must be different from one another, and the first of them must not be $0$. The number of possible codes is",
  r"$438048$",
  [(r"$486720$", r"Uses $26^2 \cdot P(10, 3)$, allowing $0$ as the first digit."),
   (r"$421200$", r"Uses $26 \cdot 25$ for the letters, wrongly forbidding repeated letters."),
   (r"$492804$", r"Uses $26^2 \cdot 9^3$, applying the non-zero rule to every digit and ignoring the distinct-digit rule.")],
  r"The letters can be chosen in $26 \cdot 26 = 676$ ways. The first digit has $9$ choices, the second $9$ (any digit except the first) and the third $8$, giving $648$. Total $676 \cdot 648 = 438048$.",
  "Applying a restriction to the wrong part of the code.",
  "U04-A-fpc-codes", "Multiplication principle across two independent blocks.",
  check=lambda: Integer(26 * 26 * sum(1 for t in _perms("0123456789", 3) if t[0] != "0")),
  values=[438048, 486720, 421200, 492804], cognitive="Application")

q("U04-A-014", T, "Arrangements with repeated letters", "Easy",
  "Single-step computation MCQ",
  r"The number of distinct arrangements of all the letters of the word ALLAHABAD is",
  r"$7560$",
  [(r"$15120$", r"Divides by $4!$ for the A's but ignores the two L's."),
   (r"$181440$", r"Divides by $2!$ for the L's but ignores the four A's."),
   (r"$362880$", r"Treats all nine letters as distinct, giving $9!$.")],
  r"ALLAHABAD has $9$ letters: A four times, L twice, and H, B, D once each. The number of arrangements is $\frac{9!}{4!\,2!} = \frac{362880}{48} = 7560$.",
  "Not dividing by the factorial of every repeated letter.",
  "U04-A-identical-word", "Direct formula with two repeated letters.",
  check=lambda: Integer(len(words("ALLAHABAD"))),
  values=[7560, 15120, 181440, 362880], cognitive="Application")

q("U04-A-015", T, "Repeated letters kept together", "Easy",
  "Single-step computation MCQ",
  r"The number of distinct arrangements of the letters of the word LEADER in which the two E's are next to each other is",
  r"$120$",
  [(r"$240$", r"Multiplies by $2!$ for arranging the two E's inside the block, though they are identical."),
   (r"$360$", r"Counts all arrangements, $\frac{6!}{2!}$, ignoring the condition."),
   (r"$60$", r"Divides $5!$ by $2!$ again after already merging the two E's into one block.")],
  r"Treat EE as a single block. Then the units are EE, L, A, D, R, all different, which can be arranged in $5! = 120$ ways. The two E's inside the block are identical, so there is no further factor.",
  "Multiplying by the internal arrangement of identical objects.",
  "U04-A-together", "Block method with identical letters.",
  check=lambda: Integer(sum(1 for w in words("LEADER") if "EE" in w)),
  values=[120, 240, 360, 60], cognitive="Application")

q("U04-A-016", T, "Numbers greater than a given number", "Easy",
  "Single-step computation MCQ",
  r"Four-digit numbers are formed using the digits $1, 2, \dots, 9$ without repetition. The number of such numbers that are greater than $5000$ is",
  r"$1680$",
  [(r"$1344$", r"Allows only $6, 7, 8, 9$ as the first digit, missing numbers that begin with $5$."),
   (r"$3024$", r"Counts all such four-digit numbers, $P(9, 4)$."),
   (r"$2016$", r"Allows $4, 5, \dots, 9$ as the first digit.")],
  r"Every number with first digit $5, 6, 7, 8$ or $9$ exceeds $5000$ (and $5000$ itself cannot be formed). The first digit has $5$ choices and the other three places can be filled in $P(8, 3) = 336$ ways. Total $5 \cdot 336 = 1680$.",
  "Mishandling the boundary digit of the leading place.",
  "U04-A-digits-greater", "Restriction on one place only.",
  check=lambda: Integer(sum(1 for t in _perms("123456789", 4) if int(''.join(t)) > 5000)),
  values=[1680, 1344, 3024, 2016], cognitive="Application")

# ================================================================ MEDIUM (24)

q("U04-A-017", T, "Finding r from P(n, r)", "Medium",
  "Inverse/parameter MCQ",
  PDEF + r"If $P(10, r) = 5040$, then $r$ equals",
  r"$4$",
  [(r"$7$", r"Recognises $5040 = 7!$ and takes $r = 7$."),
   (r"$6$", r"Writes $P(10, r) = \frac{10!}{r!}$, so $r! = 720$ and $r = 6$."),
   (r"$3$", r"Writes $P(n, r) = n(n-1)\cdots(n-r)$ with $r + 1$ factors, so $10 \cdot 9 \cdot 8 \cdot 7$ is read as $r = 3$.")],
  r"$P(10, r) = 10 \cdot 9 \cdot 8 \cdots (10 - r + 1)$. Now $10 \cdot 9 = 90$, $90 \cdot 8 = 720$, $720 \cdot 7 = 5040$, which uses $4$ factors. Hence $r = 4$.",
  "Mixing up $\\frac{n!}{(n-r)!}$ with $\\frac{n!}{r!}$, or miscounting factors.",
  "U04-A-Pnr-equation", "Factor counting with a tempting factorial coincidence.",
  check=lambda: [r for r in range(0, 11) if ff_(10, r) == 5040][0],
  values=[4, 7, 6, 3], cognitive="Application")

q("U04-A-018", T, "Divisibility by 4 without repetition", "Medium",
  "Multi-step computation MCQ",
  r"Four-digit numbers are formed using the digits $1, 2, 3, 4, 5, 6$ without repetition. The number of such numbers that are divisible by $4$ is",
  r"$96$",
  [(r"$240$", r"Fills the first two places in $P(6, 2) = 30$ ways for each valid ending, forgetting that the ending already uses two digits."),
   (r"$90$", r"Assumes exactly one quarter of the $P(6, 4) = 360$ numbers are divisible by $4$."),
   (r"$108$", r"Also counts the ending $44$, which repeats a digit, giving $9$ endings.")],
  r"A number is divisible by $4$ when its last two digits form a multiple of $4$. With distinct digits from $1$ to $6$ the possible endings are $12, 16, 24, 32, 36, 52, 56, 64$: $8$ endings. For each, the first two places are filled from the remaining $4$ digits in $P(4, 2) = 12$ ways. Total $8 \cdot 12 = 96$.",
  "Assuming divisible numbers form an exact fraction of all, or allowing a repeated-digit ending.",
  "U04-A-div4", "List endings, then fill the remaining places.",
  check=lambda: Integer(sum(1 for t in _perms("123456", 4) if int(''.join(t)) % 4 == 0)),
  values=[96, 240, 90, 108], cognitive="Application",
  numerical=dict(question=r"Four-digit numbers are formed using the digits $1, 2, 3, 4, 5, 6$ without repetition. The number of such numbers that are divisible by $4$ is", answer=96))

q("U04-A-019", T, "Divisibility by 3 without repetition", "Medium",
  "Multi-step computation MCQ",
  r"Five-digit numbers are formed using five of the digits $0, 1, 2, 3, 4, 5$ without repetition. The number of such numbers that are divisible by $3$ is",
  r"$216$",
  [(r"$240$", r"Arranges the digit set $\{0, 1, 2, 4, 5\}$ in $5!$ ways, allowing a leading zero."),
   (r"$120$", r"Considers only the digit set $\{1, 2, 3, 4, 5\}$ and misses the set containing $0$."),
   (r"$200$", r"Assumes one third of all $5 \cdot 5! = 600$ such five-digit numbers are divisible by $3$.")],
  r"The six digits sum to $15$, so the five chosen digits have a sum divisible by $3$ exactly when the omitted digit is $0$ or $3$. Omitting $0$: digits $1, 2, 3, 4, 5$ give $5! = 120$ numbers. Omitting $3$: digits $0, 1, 2, 4, 5$ give $5! - 4! = 96$ numbers. Total $120 + 96 = 216$.",
  "Forgetting the leading-zero case in one of the digit sets.",
  "U04-A-div3", "Divisibility rule plus two cases, one with a zero.",
  check=lambda: Integer(sum(1 for t in _perms("012345", 5) if t[0] != "0" and int(''.join(t)) % 3 == 0)),
  values=[216, 240, 120, 200], cognitive="Application",
  numerical=dict(question=r"Five-digit numbers are formed using five of the digits $0, 1, 2, 3, 4, 5$ without repetition. The number of such numbers that are divisible by $3$ is", answer=216))

q("U04-A-020", T, "Rank of a word with a repeated letter", "Medium",
  "Multi-step computation MCQ",
  r"All the distinct arrangements of the letters of the word SCHOOL are listed in dictionary order. The rank of the word SCHOOL in this list is",
  r"$303$",
  [(r"$302$", "Counts the words before SCHOOL correctly but does not add $1$ for the word itself."),
   (r"$243$", r"Divides the block of words beginning with O by $2!$ as well, taking it as $60$ instead of $5! = 120$."),
   (r"$300$", "Counts only the words beginning with C, H, L or O and ignores the later positions and the word itself.")],
  r"Alphabetical order: C, H, L, O, O, S. Words beginning with C, H or L: each $\frac{5!}{2!} = 60$, total $180$. Words beginning with O: the rest C, H, L, O, S are distinct, $5! = 120$. So $300$ words begin before S. In SCHOOL, after SCH the next letter is O and L is smaller: $1$ word (SCHLOO). After SCHO the next is O and L is smaller: $1$ word (SCHOLO). Hence $302$ words precede SCHOOL, and its rank is $303$.",
  "Dividing by $2!$ in a block where the repeated letter has already been used.",
  "U04-A-rank-repeated", "Rank with a repeated letter that changes block sizes.",
  check=lambda: Integer(rank("SCHOOL")),
  values=[303, 302, 243, 300], cognitive="Application",
  numerical=dict(question=r"All the distinct arrangements of the letters of the word SCHOOL are listed in dictionary order. The rank of the word SCHOOL in this list is", answer=303))

q("U04-A-021", T, "Word at a given position in dictionary order", "Medium",
  "Inverse/parameter MCQ",
  r"All the arrangements of the letters of the word LATER are listed in dictionary order. The $50$th word in the list is",
  r"LAETR",
  [(r"LAERT", r"Off by one: this is the $49$th word, the first word beginning with L."),
   (r"ETRLA", r"Off by one block: this is the $48$th word, the last word beginning with E."),
   (r"LARET", r"Takes the E-block to end at the $47$th word, so lands one place too far, on the $51$st word.")],
  r"The letters in order are A, E, L, R, T. Each first letter starts $4! = 24$ words: A gives words $1$ to $24$, E gives $25$ to $48$, L gives $49$ to $72$. Among words beginning with L, those beginning LA are $3! = 6$, in order LAERT, LAETR, ... So the $49$th is LAERT and the $50$th is LAETR.",
  "Off-by-one errors when locating a word inside a block.",
  "U04-A-rank-inverse", "Reverse use of block sizes.",
  check=lambda: wcode(words("LATER")[49]),
  values=[wcode("LAETR"), wcode("LAERT"), wcode("ETRLA"), wcode("LARET")], cognitive="Application")

q("U04-A-022", T, "Vowels restricted to odd positions", "Medium",
  "Multi-step computation MCQ",
  r"The number of arrangements of the letters of the word ARTICLE in which the vowels occupy only odd positions (first, third, fifth or seventh) is",
  r"$576$",
  [(r"$144$", r"Assumes there are only $3$ odd positions, giving $3! \cdot 4!$."),
   (r"$96$", r"Chooses the vowel positions by $C(4, 3)$ but does not arrange the vowels in them."),
   (r"$24$", r"Places the vowels in $P(4, 3)$ ways but forgets to arrange the consonants.")],
  r"ARTICLE has vowels A, I, E and consonants R, T, C, L. There are $4$ odd positions. The $3$ vowels go into them in $P(4, 3) = 24$ ways, and the $4$ consonants fill the remaining $4$ positions in $4! = 24$ ways. Total $24 \cdot 24 = 576$.",
  "Miscounting the available odd positions or skipping an arrangement step.",
  "U04-A-positions", "Two arrangement stages with a position restriction.",
  check=lambda: Integer(sum(1 for w in _perms("ARTICLE") if all(i % 2 == 0 for i, c in enumerate(w) if c in "AIE"))),
  values=[576, 144, 96, 24], cognitive="Application")

q("U04-A-023", T, "Fixed relative order of some letters", "Medium",
  "Multi-step computation MCQ",
  r"The number of arrangements of the letters of the word INVOLUTE in which the vowels appear in alphabetical order from left to right (not necessarily together) is",
  r"$1680$",
  [(r"$576$", r"Arranges vowels and consonants in separate fixed blocks, $4! \cdot 4!$."),
   (r"$20160$", r"Divides $8!$ by $2$, as if only two vowels had a fixed order."),
   (r"$70$", r"Chooses the vowel positions by $C(8, 4)$ but does not arrange the consonants.")],
  r"INVOLUTE has $8$ distinct letters, with vowels I, O, U, E. In all $8!$ arrangements the $4$ vowels appear in each of their $4!$ orders equally often, so exactly $\frac{8!}{4!} = 1680$ have them in the order E, I, O, U.",
  "Mishandling a fixed relative order, which acts like identical objects.",
  "U04-A-relative-order", "Equivalent to treating the ordered letters as identical.",
  check=lambda: Integer(sum(1 for w in _perms("INVOLUTE") if [c for c in w if c in "IOUE"] == ["E", "I", "O", "U"])),
  values=[1680, 576, 20160, 70], cognitive="Understanding")

q("U04-A-024", T, "Numbers from repeated digits including zero", "Medium",
  "Multi-step computation MCQ",
  r"The number of six-digit numbers that can be formed using all the digits $1, 1, 2, 2, 2, 0$ is",
  r"$50$",
  [(r"$60$", r"Counts $\frac{6!}{2!\,3!}$, including arrangements that begin with $0$."),
   (r"$600$", r"Treats all digits as distinct, $6! - 5!$."),
   (r"$40$", r"Counts the arrangements beginning with $0$ as $\frac{5!}{3!} = 20$, forgetting to divide by $2!$ for the two $1$s.")],
  r"All arrangements of $1, 1, 2, 2, 2, 0$: $\frac{6!}{2!\,3!} = 60$. Those beginning with $0$ arrange $1, 1, 2, 2, 2$ behind it: $\frac{5!}{2!\,3!} = 10$. So the number of six-digit numbers is $60 - 10 = 50$.",
  "Ignoring the leading-zero restriction with identical digits.",
  "U04-A-identical-digits", "Identical objects plus leading-zero subtraction.",
  check=lambda: Integer(sum(1 for w in words("112220") if w[0] != "0")),
  values=[50, 60, 600, 40], cognitive="Application",
  numerical=dict(question=r"The number of six-digit numbers that can be formed using all the digits $1, 1, 2, 2, 2, 0$ is", answer=50))

q("U04-A-025", T, "Sum of all numbers formed", "Medium",
  "Multi-step computation MCQ",
  r"The sum of all four-digit numbers that can be formed using the digits $1, 2, 3, 4, 5$ without repetition is",
  r"$399960$",
  [(r"$99990$", r"Takes each digit to appear $3! = 6$ times in each place instead of $P(4, 3) = 24$ times."),
   (r"$499950$", r"Takes each digit to appear $\frac{120}{4} = 30$ times in each place, dividing the number of numbers by the number of places."),
   (r"$1999800$", r"Takes each digit to appear $5! = 120$ times in each place.")],
  r"There are $P(5, 4) = 120$ such numbers. A fixed digit sits in a given place in $P(4, 3) = 24$ of them. So each place contributes $24(1 + 2 + 3 + 4 + 5) = 360$ times its place value, and the sum is $360 \cdot 1111 = 399960$.",
  "Miscounting how often each digit occupies a given place.",
  "U04-A-sum-numbers", "Place-value counting argument.",
  check=lambda: Integer(sum(int(''.join(t)) for t in _perms("12345", 4))),
  values=[399960, 99990, 499950, 1999800], cognitive="Application")

q("U04-A-026", T, "At least one repeated digit", "Medium",
  "Multi-step computation MCQ",
  r"The number of four-digit natural numbers in which at least one digit is repeated is",
  r"$4464$",
  [(r"$4960$", r"Uses $10^4 - P(10, 4)$, treating strings with a leading zero as four-digit numbers."),
   (r"$3960$", r"Subtracts $P(10, 4) = 5040$ from $9000$, mixing the leading-zero rule into only one count."),
   (r"$4536$", r"Reports the number of four-digit numbers with all digits distinct.")],
  r"There are $9000$ four-digit numbers. Those with all digits distinct number $9 \cdot 9 \cdot 8 \cdot 7 = 4536$. Hence at least one digit is repeated in $9000 - 4536 = 4464$ numbers.",
  "Applying the leading-zero restriction inconsistently in a complement count.",
  "U04-A-complement-repeat", "Complement method with a leading-digit restriction.",
  check=lambda: Integer(sum(1 for m in range(1000, 10000) if len(set(str(m))) < 4)),
  values=[4464, 4960, 3960, 4536], cognitive="Application",
  numerical=dict(question=r"The number of four-digit natural numbers in which at least one digit is repeated is", answer=4464))

q("U04-A-027", T, "Identical letters kept together", "Medium",
  "Multi-step computation MCQ",
  r"The number of distinct arrangements of the letters of the word ASSASSIN in which all the S's are together is",
  r"$60$",
  [(r"$1440$", r"Multiplies by $4!$ for arranging the S's inside the block, though they are identical."),
   (r"$840$", r"Counts all arrangements, $\frac{8!}{4!\,2!}$, ignoring the condition."),
   (r"$120$", r"Arranges the $5$ units in $5!$ ways, forgetting the two identical A's.")],
  r"ASSASSIN has S four times, A twice, and I, N once. Treat SSSS as one block. The units are the block, A, A, I, N, which can be arranged in $\frac{5!}{2!} = 60$ ways. The block has only one internal order.",
  "Treating identical letters inside a block as distinguishable.",
  "U04-A-together-identical", "Block method combined with identical letters.",
  check=lambda: Integer(sum(1 for w in words("ASSASSIN") if "SSSS" in w)),
  values=[60, 1440, 840, 120], cognitive="Application")

q("U04-A-028", T, "No two identical letters together", "Medium",
  "Multi-step computation MCQ",
  r"The number of distinct arrangements of the letters of the word BALLOON in which the two L's are not next to each other is",
  r"$900$",
  [(r"$360$", r"Counts the arrangements in which the two L's are together, $\frac{6!}{2!} = 360$."),
   (r"$1800$", r"Places the L's in the gaps by $P(6, 2) = 30$, treating the identical L's as distinct: $60 \cdot 30$."),
   (r"$540$", r"Uses the complement but multiplies the LL-together count by $2!$ for the identical L's: $1260 - 720$.")],
  r"Arrange B, A, O, O, N in $\frac{5!}{2!} = 60$ ways. These $5$ letters create $6$ gaps (including both ends). Choose $2$ of them for the identical L's in $C(6, 2) = 15$ ways. Total $60 \cdot 15 = 900$. (Check: all arrangements number $\frac{7!}{2!\,2!} = 1260$ and those with LL together number $\frac{6!}{2!} = 360$; $1260 - 360 = 900$.)",
  "Treating identical letters as distinct, in the gap method or inside a block.",
  "U04-A-gap-identical", "Gap method with identical objects and a second repeated letter.",
  check=lambda: Integer(sum(1 for w in words("BALLOON") if "LL" not in w)),
  values=[900, 360, 1800, 540], cognitive="Application",
  numerical=dict(question=r"The number of distinct arrangements of the letters of the word BALLOON in which the two L's are not next to each other is", answer=900))

q("U04-A-029", T, "Relative positions of vowels and consonants unchanged", "Medium",
  "Multi-step computation MCQ",
  r"The number of arrangements of the letters of the word EQUATION, counting the word EQUATION itself, in which the positions occupied by vowels and by consonants stay the same as in EQUATION, is",
  r"$720$",
  [(r"$719$", r"Excludes the original word, although the stem asks to count it."),
   (r"$126$", r"Adds the two counts, $5! + 3!$, instead of multiplying."),
   (r"$40320$", r"Counts all $8!$ arrangements, ignoring the condition.")],
  r"EQUATION has vowels E, U, A, I, O and consonants Q, T, N. The $5$ vowel positions can be filled by the vowels in $5! = 120$ ways and the $3$ consonant positions by the consonants in $3! = 6$ ways. Total $120 \cdot 6 = 720$, including EQUATION itself.",
  "Adding independent counts, or excluding the original arrangement.",
  "U04-A-positions", "Two independent arrangements combined.",
  check=lambda: Integer(sum(1 for w in _perms("EQUATION") if all((c in "EUAIO") == (o in "EUAIO") for c, o in zip(w, "EQUATION")))),
  values=[720, 719, 126, 40320], cognitive="Application")

q("U04-A-030", T, "Numbers in a range, repetition allowed", "Medium",
  "Multi-step computation MCQ",
  r"Using the digits $0, 1, 2, 3, 4, 5$, with repetition allowed, the number of four-digit numbers greater than $2000$ and not greater than $5000$ is",
  r"$648$",
  [(r"$647$", r"Removes $2000$ correctly but forgets that $5000$ is allowed."),
   (r"$649$", r"Adds $5000$ but forgets to remove $2000$, which is not greater than $2000$."),
   (r"$864$", r"Allows $2, 3, 4, 5$ as the first digit with $6^3$ completions each, including numbers above $5000$.")],
  r"Numbers with first digit $2, 3$ or $4$: $3 \cdot 6^3 = 648$, running from $2000$ to $4555$. Remove $2000$ (not greater than $2000$) and add $5000$ (allowed), giving $648 - 1 + 1 = 648$.",
  "Mishandling the endpoints of the range.",
  "U04-A-digits-range", "Boundary cases at both ends.",
  check=lambda: Integer(sum(1 for t in _product("012345", repeat=4) if t[0] != "0" and 2000 < int(''.join(t)) <= 5000)),
  values=[648, 647, 649, 864], cognitive="Analysis",
  numerical=dict(question=r"Using the digits $0, 1, 2, 3, 4, 5$, with repetition allowed, the number of four-digit numbers greater than $2000$ and not greater than $5000$ is", answer=648))

def _c31():
    st1 = sum(1 for m in range(1000, 10000) if len(set(str(m))) == 4 and m % 5 == 0) == 1008
    st2 = sum(1 for w in words("MISSISSIPPI") if "SS" not in w) == 7350
    return (st1, st2)
q("U04-A-031", T, "Divisibility and arrangements: statements", "Medium",
  "Statement-based MCQ",
  r"Statement I: The number of four-digit numbers with all digits distinct that are divisible by $5$ is $1008$. Statement II: The number of distinct arrangements of the letters of the word MISSISSIPPI in which no two S's are next to each other is $7350$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Accepts $1008 = 2 \cdot 504$, treating last digit $5$ like last digit $0$ and allowing $0$ to lead."),
   (ST_FF, r"Rejects Statement II, placing the S's in the gaps with $P(8, 4)$ as if they were distinct, which gives $105 \cdot 1680 = 176400$."),
   (ST_TF, r"Accepts Statement I with the $2 \cdot 504$ count and rejects Statement II.")],
  r"Statement I: last digit $0$ gives $P(9, 3) = 504$; last digit $5$ gives $8 \cdot 8 \cdot 7 = 448$ (first digit not $0$ or $5$). Total $952$, not $1008$, so it is false. Statement II: arrange M, I, I, I, I, P, P in $\frac{7!}{4!\,2!} = 105$ ways; choose $4$ of the $8$ gaps for the identical S's in $C(8, 4) = 70$ ways; $105 \cdot 70 = 7350$, so it is true.",
  "Treating the cases of last digit $0$ and $5$ alike.",
  "U04-A-div5-statement", "Two separate counts, one with a leading-zero trap.",
  check=_c31, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis")

q("U04-A-032", T, "Two together and a third separated", "Medium",
  "Multi-step computation MCQ",
  r"Six persons, including $P$, $Q$ and $R$, stand in a row. The number of arrangements in which $P$ and $Q$ stand next to each other but $R$ stands next to neither $P$ nor $Q$ is",
  r"$144$",
  [(r"$240$", r"Counts all arrangements with $P$ and $Q$ together, $5! \cdot 2$, ignoring the condition on $R$."),
   (r"$96$", r"Counts the arrangements in which $R$ is next to the $PQ$ block."),
   (r"$72$", r"Does the subtraction correctly but forgets the factor $2$ for the order of $P$ and $Q$.")],
  r"With $P, Q$ as a block there are $5$ units, so $5! \cdot 2 = 240$ arrangements. $R$ is next to $P$ or $Q$ exactly when $R$ is adjacent to the block: treat block plus $R$ as one unit ($R$ on either side, $P, Q$ in either order) giving $4! \cdot 2 \cdot 2 = 96$. Hence $240 - 96 = 144$.",
  "Forgetting the internal order of the pair.",
  "U04-A-together-mixed", "Block method followed by a complement.",
  check=lambda: Integer(sum(1 for p in _perms("PQRuvw") if adjacent(p, "P", "Q") and not adjacent(p, "R", "P") and not adjacent(p, "R", "Q"))),
  values=[144, 240, 96, 72], cognitive="Application")

q("U04-A-033", T, "Containing a given digit, digits distinct", "Medium",
  "Multi-step computation MCQ",
  r"The number of four-digit numbers with all digits distinct that contain the digit $5$ is",
  r"$1848$",
  [(r"$3168$", r"Uses $9000 - 8 \cdot 9^3$, ignoring the distinct-digit condition."),
   (r"$1512$", r"Subtracts $P(9, 4) = 3024$, allowing a leading zero in the numbers without $5$."),
   (r"$2016$", r"Places $5$ in any of $4$ positions and fills the rest in $P(9, 3)$ ways, ignoring the leading-zero restriction.")],
  r"Four-digit numbers with distinct digits: $9 \cdot 9 \cdot 8 \cdot 7 = 4536$. Those without $5$: the first digit from $1$ to $9$ except $5$ ($8$ ways), then $P(8, 3) = 336$ ways for the rest, giving $2688$. Hence $4536 - 2688 = 1848$.",
  "Applying the leading-zero rule inconsistently in a complement count.",
  "U04-A-complement-digit", "Complement with two restrictions.",
  check=lambda: Integer(sum(1 for m in range(1000, 10000) if len(set(str(m))) == 4 and "5" in str(m))),
  values=[1848, 3168, 1512, 2016], cognitive="Application",
  numerical=dict(question=r"The number of four-digit numbers with all digits distinct that contain the digit $5$ is", answer=1848))

def _c34():
    vowels = "EUAIO"
    cons = "PRMTTN"
    # units: vowel block V and the consonants; arrange units, then vowels inside the block
    units = len(set(_perms("V" + cons)))
    inside = len(set(_perms(vowels)))
    return Integer(units * inside)
q("U04-A-034", T, "Vowels together with a repeated consonant", "Medium",
  "Multi-step computation MCQ",
  r"The number of distinct arrangements of the letters of the word PERMUTATION in which all the vowels are together is",
  r"$302400$",
  [(r"$604800$", r"Forgets that T occurs twice, using $7! \cdot 5!$."),
   (r"$43200$", r"Arranges only the $6$ consonants, $\frac{6!}{2!} = 360$, then multiplies by $5!$, forgetting that the vowel block is also a unit."),
   (r"$2520$", r"Arranges the $7$ units but not the vowels inside the block.")],
  r"PERMUTATION has vowels E, U, A, I, O (all different) and consonants P, R, M, T, T, N. Treating the vowels as one block gives $7$ units with T repeated: $\frac{7!}{2!} = 2520$ arrangements. The vowels inside the block: $5! = 120$. Total $2520 \cdot 120 = 302400$.",
  "Ignoring a repeated letter outside the block.",
  "U04-A-together-identical", "Block method with a repeated letter outside the block.",
  check=_c34, values=[302400, 604800, 43200, 2520], cognitive="Application")

q("U04-A-035", T, "Telescoping sum with P(k, k)", "Medium",
  "Multi-step computation MCQ",
  PDEF + r"The value of $1 + 1 \cdot P(1, 1) + 2 \cdot P(2, 2) + 3 \cdot P(3, 3) + \dots + 10 \cdot P(10, 10)$ is",
  r"$11!$",
  [(r"$11! - 1$", "Sums the telescoping series correctly but drops the leading $1$."),
   (r"$11! + 1$", r"Telescopes the sum to $11!$, dropping the $-1!$ term, and then adds the leading $1$."),
   (r"$12! - 1$", r"Telescopes with the last surviving term taken as $12!$, getting $12! - 1$, and then drops the leading $1$.")],
  r"$P(k, k) = k!$ and $k \cdot k! = (k+1)! - k!$. So $\sum_{k=1}^{10} k \cdot k! = 11! - 1! = 11! - 1$, and adding the leading $1$ gives $11!$.",
  "Mishandling the end terms of a telescoping sum.",
  "U04-A-Pnr-identity", "Recognising and telescoping $k \\cdot k!$.",
  check=lambda: 1 + sum(k * ff_(k, k) for k in range(1, 11)),
  values=[factorial(11), factorial(11) - 1, factorial(11) + 1, factorial(12) - 1], cognitive="Analysis")

def _c36():
    m, n = symbols('m n', integer=True, positive=True)
    k = symbols('k', integer=True)
    s1 = [v for v in solve(k * (k - 1) - 90, k) if v >= 2][0]
    s2 = [v for v in solve(k * (k - 1) - 30, k) if v >= 2][0]
    sol = solve([m + n - s1, m - n - s2], [m, n], dict=True)[0]
    return ff_(sol[m], sol[n])
q("U04-A-036", T, "Simultaneous equations in P(n, r)", "Medium",
  "Multi-step computation MCQ",
  PDEF + r"If $m$ and $n$ are positive integers with $P(m + n, 2) = 90$ and $P(m - n, 2) = 30$, then $P(m, n)$ equals",
  r"$56$",
  [(r"$42$", r"Writes $P(k, 2) = k(k+1)$, so $k(k+1) = 90$ and $k(k+1) = 30$ give $m + n = 9$, $m - n = 5$; then $m = 7$, $n = 2$ and $P(7, 2) = 42$."),
   (r"$28$", r"Finds $m = 8$, $n = 2$ correctly but evaluates $C(8, 2) = 28$, dividing by $2!$ as for a selection."),
   (r"$64$", r"Finds $m = 8$, $n = 2$ correctly but evaluates $8^2 = 64$, as if repetition were allowed.")],
  r"$P(k, 2) = k(k-1)$. From $k(k-1) = 90$ the admissible root is $k = 10$, and from $k(k-1) = 30$ it is $k = 6$. So $m + n = 10$ and $m - n = 6$, giving $m = 8$, $n = 2$. Hence $P(8, 2) = 8 \cdot 7 = 56$.",
  "Mis-writing $P(k, 2)$ or evaluating $P(m, n)$ as a selection or with repetition.",
  "U04-A-Pnr-system", "Two quadratic equations in $P(k, 2)$, a linear system, then an evaluation.",
  check=_c36, values=[Integer(56), Integer(42), Integer(28), Integer(64)], cognitive="Application",
  numerical=dict(question=r"Here $P(n, r)$ denotes the number of permutations of $n$ distinct objects taken $r$ at a time. If $m$ and $n$ are positive integers with $P(m + n, 2) = 90$ and $P(m - n, 2) = 30$, then $P(m, n)$ is", answer=56))

def _c37():
    odd_distinct = sum(1 for m in range(100, 1000) if set(str(m)) <= set("13579") and len(set(str(m))) == 3)
    some_even = sum(1 for m in range(100, 1000) if any(int(d) % 2 == 0 for d in str(m)))
    return (odd_distinct == 60, some_even == 775)
q("U04-A-037", T, "Odd and even digits: statements", "Medium",
  "Statement-based MCQ",
  r"Statement I: The number of three-digit numbers whose digits are all odd and all different is $60$. Statement II: The number of three-digit numbers having at least one even digit is $775$." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Rejects Statement II by computing $1000 - 125 = 875$, counting strings with a leading zero."),
   (ST_FT, r"Rejects Statement I by allowing repetition, getting $5^3 = 125$."),
   (ST_FF, r"Rejects both, using $5^3$ for Statement I and $1000 - 125$ for Statement II.")],
  r"Statement I: the digits come from $1, 3, 5, 7, 9$ without repetition, $5 \cdot 4 \cdot 3 = 60$; true. Statement II: three-digit numbers with all digits odd number $5^3 = 125$ (no zero is involved), so at least one even digit occurs in $900 - 125 = 775$; true.",
  "Using $1000$ instead of $900$ as the total of three-digit numbers.",
  "U04-A-parity-statement", "Two short counts, one by complement.",
  check=_c37, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Application")

q("U04-A-038", T, "Rank of a word with distinct letters", "Medium",
  "Multi-step computation MCQ",
  r"All the arrangements of the letters of the word DOCUMENT are listed in dictionary order. The rank of the word DOCUMENT is",
  r"$8023$",
  [(r"$8022$", r"Counts the words before DOCUMENT correctly but does not add $1$ for the word itself."),
   (r"$8743$", r"At the second place counts D among the letters smaller than O although D is already used, giving $5 \cdot 6!$."),
   (r"$8047$", r"At the fourth place counts the already used C among the letters smaller than U, giving $5 \cdot 4!$.")],
  r"Order: C, D, E, M, N, O, T, U. First letter: C before D gives $7! = 5040$. Second letter O, with C, E, M, N smaller and unused: $4 \cdot 6! = 2880$. Third letter C: nothing smaller is left. Fourth letter U, with E, M, N, T smaller: $4 \cdot 4! = 96$. Fifth letter M, with E smaller: $1 \cdot 3! = 6$. The rest E, N, T are already in order. So $5040 + 2880 + 96 + 6 = 8022$ words precede, and the rank is $8023$.",
  "Counting letters already used when finding smaller letters at a position.",
  "U04-A-rank-distinct", "Positional count over eight letters.",
  check=lambda: Integer(rank("DOCUMENT")),
  values=[8023, 8022, 8743, 8047], cognitive="Application",
  numerical=dict(question=r"All the arrangements of the letters of the word DOCUMENT are listed in dictionary order. The rank of the word DOCUMENT is", answer=8023))

q("U04-A-039", T, "Fixed order combined with adjacency", "Medium",
  "Multi-step computation MCQ",
  r"The six letters $a, b, c, d, e, f$ are arranged in a row. The number of arrangements in which $a$ comes before $b$ and $b$ comes before $c$ (not necessarily next to each other), and $d$ and $e$ are next to each other, is",
  r"$40$",
  [(r"$20$", r"Forgets that $d$ and $e$ can be in either order inside their block."),
   (r"$120$", r"Ignores the adjacency of $d$ and $e$, giving $\frac{6!}{3!}$."),
   (r"$240$", r"Ignores the order condition on $a, b, c$, giving $5! \cdot 2$.")],
  r"Treat $de$ as a block in $2$ internal orders; with $a, b, c, f$ there are $5$ units and $5! \cdot 2 = 240$ arrangements. In these, $a, b, c$ occur in each of their $3! = 6$ orders equally often, so the required number is $\frac{240}{6} = 40$.",
  "Forgetting the internal order of a block when a fixed order is also imposed.",
  "U04-A-relative-order", "Combines a block with a fixed relative order.",
  check=lambda: Integer(sum(1 for p in _perms("abcdef") if p.index("a") < p.index("b") < p.index("c") and adjacent(p, "d", "e"))),
  values=[40, 20, 120, 240], cognitive="Application")

q("U04-A-040", T, "Exactly two equal digits", "Medium",
  "Multi-step computation MCQ",
  r"The number of three-digit numbers in which exactly two of the three digits are equal is",
  r"$243$",
  [(r"$252$", r"Computes $900 - 648$, which also includes the $9$ numbers with all three digits equal."),
   (r"$270$", r"Counts $3 \cdot 10 \cdot 9$ patterns, allowing a leading zero."),
   (r"$261$", r"Adds the $9$ numbers with all digits equal instead of subtracting them: $252 + 9$.")],
  r"Of the $900$ three-digit numbers, $9 \cdot 9 \cdot 8 = 648$ have all digits distinct and $9$ (such as $111$) have all digits equal. So exactly two digits are equal in $900 - 648 - 9 = 243$ numbers.",
  "Forgetting the all-equal case when taking a complement.",
  "U04-A-exactly-two-equal", "Complement with two excluded classes.",
  check=lambda: Integer(sum(1 for m in range(100, 1000) if len(set(str(m))) == 2)),
  values=[243, 252, 270, 261], cognitive="Application",
  numerical=dict(question=r"The number of three-digit numbers in which exactly two of the three digits are equal is", answer=243))

# ================================================================ DIFFICULT (14)

q("U04-A-041", T, "Divisibility by 6 without repetition", "Difficult",
  "Multi-step computation MCQ",
  r"Six-digit numbers are formed using six of the seven digits $0, 1, 2, 3, 4, 5, 6$ without repetition. The number of such numbers that are divisible by $6$ is",
  r"$1080$",
  [(r"$1200$", r"Counts $5!$ arrangements for every admissible last digit in all three digit sets, allowing a leading zero in the sets that contain $0$: $360 + 480 + 360 = 1200$."),
   (r"$768$", r"Omits only $0$ or $3$ to keep the digit sum a multiple of $3$, missing the set obtained by omitting $6$: $360 + 408 = 768$."),
   (r"$840$", r"Takes the last digit only from the nonzero even digits, missing the numbers ending in $0$: $360 + 288 + 192 = 840$.")],
  r"The seven digits sum to $21$, so the six chosen digits have a sum divisible by $3$ exactly when the omitted digit is $0$, $3$ or $6$. Omit $0$: digits $1, \ldots, 6$, last digit $2, 4$ or $6$, giving $3 \cdot 5! = 360$. Omit $3$: last digit $0$ gives $5! = 120$; last digit $2, 4$ or $6$ gives $4 \cdot 4! = 96$ each (first digit not $0$), so $120 + 288 = 408$. Omit $6$: last digit $0$ gives $120$; last digit $2$ or $4$ gives $96$ each, so $120 + 192 = 312$. Total $360 + 408 + 312 = 1080$.",
  "Missing a digit set or the leading-zero restriction when the zero is not used at the end.",
  "U04-A-div6", "Two divisibility rules, three digit sets, zero casework in two of them.",
  check=lambda: Integer(sum(1 for t in _perms("0123456", 6) if t[0] != "0" and int(''.join(t)) % 6 == 0)),
  values=[1080, 1200, 768, 840], cognitive="Analysis",
  numerical=dict(question=r"Six-digit numbers are formed using six of the seven digits $0, 1, 2, 3, 4, 5, 6$ without repetition. The number of such numbers that are divisible by $6$ is", answer=1080))

q("U04-A-042", T, "Sum of all numbers formed, with zero", "Difficult",
  "Multi-step computation MCQ",
  r"The sum of all four-digit numbers that can be formed using four of the digits $0, 1, 2, 3, 4$ without repetition is",
  r"$259980$",
  [(r"$266640$", r"Lets each digit appear $24$ times in every place, including arrangements with a leading zero."),
   (r"$199980$", r"Uses $18$ appearances per digit in every place, including the thousands place."),
   (r"$240000$", r"Subtracts the leading-zero arrangements as $24 \cdot 10 \cdot 111 = 26640$ instead of $6 \cdot 10 \cdot 111 = 6660$.")],
  r"Thousands place: a nonzero digit appears there in $P(4, 3) = 24$ numbers, contributing $24 \cdot 10 \cdot 1000 = 240000$. Any other place: fix a nonzero digit there; the first digit has $3$ choices and the remaining two places $3 \cdot 2$, so $18$ numbers, contributing $18 \cdot 10 \cdot 111 = 19980$. Total $240000 + 19980 = 259980$.",
  "Ignoring that zero cannot lead when counting digit appearances.",
  "U04-A-sum-numbers", "Place-value counting with a zero restriction.",
  check=lambda: Integer(sum(int(''.join(t)) for t in _perms("01234", 4) if t[0] != "0")),
  values=[259980, 266640, 199980, 240000], cognitive="Analysis")

q("U04-A-043", T, "Odd digits in even positions", "Difficult",
  "Multi-step computation MCQ",
  r"Nine-digit numbers are formed using all the digits $1, 1, 3, 2, 2, 2, 4, 4, 6$, each used as many times as listed. The number of such numbers in which every odd digit occupies an even position (second, fourth, sixth or eighth) is",
  r"$720$",
  [(r"$180$", r"Arranges $1, 1, 3$ in $3$ ways but forgets to choose which $3$ of the $4$ even positions they occupy."),
   (r"$1440$", r"Places the odd digits in $P(4, 3) = 24$ ways without dividing by $2!$ for the two $1$s."),
   (r"$240$", r"Chooses the positions for the odd digits by $C(4, 3)$ but does not arrange $1, 1, 3$ in them.")],
  r"The odd digits are $1, 1, 3$. Choose $3$ of the $4$ even positions in $C(4, 3) = 4$ ways and arrange $1, 1, 3$ there in $3$ ways: $12$. The remaining $6$ positions take $2, 2, 2, 4, 4, 6$ in $\frac{6!}{3!\,2!} = 60$ ways. Total $12 \cdot 60 = 720$.",
  "Forgetting that one even position is left over for an even digit.",
  "U04-A-parity-positions", "Identical objects with position restrictions and a leftover slot.",
  check=lambda: Integer(sum(1 for w in words("113222446") if all(i % 2 == 1 for i, c in enumerate(w) if c in "13"))),
  values=[720, 180, 1440, 240], cognitive="Analysis")

q("U04-A-044", T, "Rank of a word with several repeated letters", "Difficult",
  "Multi-step computation MCQ",
  r"All the distinct arrangements of the letters of the word SUCCESS are listed in dictionary order. The rank of the word SUCCESS is",
  r"$331$",
  [(r"$330$", r"Counts the words before SUCCESS correctly but does not add $1$ for the word itself."),
   (r"$391$", r"Takes the words beginning with E as $\frac{6!}{3!} = 120$, forgetting the repeated C."),
   (r"$271$", r"At the second place counts only C and E as smaller than U, missing S.")],
  r"Order: C, C, E, S, S, S, U. First letter C: arrange C, E, S, S, S, U in $\frac{6!}{3!} = 120$ ways; E: arrange C, C, S, S, S, U in $\frac{6!}{2!\,3!} = 60$ ways. Words SC..: $\frac{5!}{2!} = 60$; SE..: $\frac{5!}{2!\,2!} = 30$; SS..: $\frac{5!}{2!} = 60$. After SU the letters C, C, E, S, S follow in increasing order. Hence $120 + 60 + 60 + 30 + 60 = 330$ words precede and the rank is $331$.",
  "Dividing by the wrong factorials when several letters repeat.",
  "U04-A-rank-repeated", "Rank with three repeated letters across two positions.",
  check=lambda: Integer(rank("SUCCESS")),
  values=[331, 330, 391, 271], cognitive="Analysis",
  numerical=dict(question=r"All the distinct arrangements of the letters of the word SUCCESS are listed in dictionary order. The rank of the word SUCCESS is", answer=331))

q("U04-A-045", T, "Word at a given position, repeated letter", "Difficult",
  "Inverse/parameter MCQ",
  r"All the distinct arrangements of the letters of the word BALLOT are listed in dictionary order. The $200$th word in the list is",
  r"LOBATL",
  [(r"LOBALT", r"Off by one: this is the $199$th word."),
   (r"LOBLAT", r"Off by one: this is the $201$st word."),
   (r"OBLTAL", r"Takes the block of words beginning with L as $\frac{5!}{2!} = 60$, although only one L remains after the first letter.")],
  r"Letters A, B, L, L, O, T. Words beginning with A: $\frac{5!}{2!} = 60$ (words $1$ to $60$); with B: $60$ (words $61$ to $120$); with L: the rest A, B, L, O, T are distinct, $5! = 120$ (words $121$ to $240$). The $200$th is the $80$th L-word. Second letters A, B, L each give $4! = 24$, covering $72$; the $80$th is the $8$th word beginning LO. Third letter A gives $6$, so it is the $2$nd word beginning LOB, i.e. after LOBALT comes LOBATL.",
  "Using the wrong block size when a repeated letter is used up.",
  "U04-A-rank-inverse", "Reverse rank with a block-size change.",
  check=lambda: wcode(words("BALLOT")[199]),
  values=[wcode("LOBATL"), wcode("LOBALT"), wcode("LOBLAT"), wcode("OBLTAL")], cognitive="Analysis")

q("U04-A-046", T, "Gap method with a block", "Difficult",
  "Multi-step computation MCQ",
  r"Five boys, including $B_1$ and $B_2$, and three girls stand in a row. The number of arrangements in which no two girls are next to each other and $B_1, B_2$ are next to each other is",
  r"$2880$",
  [(r"$14400$", r"Ignores the condition on $B_1, B_2$ and counts only no two girls together, $5! \cdot P(6, 3)$."),
   (r"$5760$", r"Treats $B_1 B_2$ as a block but still uses $6$ gaps, $4! \cdot 2 \cdot P(6, 3)$."),
   (r"$1440$", r"Uses the block and $5$ gaps correctly but forgets that $B_1, B_2$ can be in either order.")],
  r"A girl may not stand between $B_1$ and $B_2$, so treat them as one block ($2$ internal orders). With the other $3$ boys there are $4$ boy-units, arranged in $4! \cdot 2 = 48$ ways, creating $5$ gaps. The girls go into $3$ different gaps in $P(5, 3) = 60$ ways. Total $48 \cdot 60 = 2880$.",
  "Not reducing the number of gaps after forming a block.",
  "U04-A-gap-method", "Block and gap methods combined.",
  check=lambda: Integer(sum(1 for p in _perms(["B1", "B2", "b3", "b4", "b5", "g1", "g2", "g3"])
                            if adjacent(p, "B1", "B2") and not any(p[k][0] == "g" and p[k + 1][0] == "g" for k in range(7)))),
  values=[2880, 14400, 5760, 1440], cognitive="Analysis",
  numerical=dict(question=r"Five boys, including $B_1$ and $B_2$, and three girls stand in a row. The number of arrangements in which no two girls are next to each other and $B_1, B_2$ are next to each other is", answer=2880))

q("U04-A-047", T, "Every digit used at least once, with zero", "Difficult",
  "Multi-step computation MCQ",
  r"The number of five-digit numbers whose digits are all from $\{0, 1, 2, 3\}$ and in which each of $0, 1, 2, 3$ appears at least once is",
  r"$180$",
  [(r"$240$", r"Counts $4 \cdot \frac{5!}{2!} = 240$ strings, forgetting that the first digit cannot be $0$."),
   (r"$144$", r"Fixes a nonzero first digit ($3$ ways), then takes the other four places as the remaining three digits plus one of $4$ extra digits arranged in $\frac{4!}{2!}$ ways every time: $3 \cdot 4 \cdot 12$; when the extra digit equals the first digit there is no repeat among the four places, so $4!$ is needed."),
   (r"$360$", r"Handles the leading zero by taking $\frac{3}{4}$ of the strings but does not divide by $2!$ for the repeated digit: $\frac{3}{4} \cdot 4 \cdot 5!$.")],
  r"Five places with all four digits present means exactly one digit occurs twice and the others once. Ignoring the leading-zero rule: choose the repeated digit in $4$ ways and arrange in $\frac{5!}{2!} = 60$ ways, giving $240$ strings. Strings starting with $0$: the last four places hold $1, 2, 3$ and one more digit; if that digit is $0$ there are $4! = 24$ arrangements, and if it is $1$, $2$ or $3$ there are $3 \cdot \frac{4!}{2!} = 36$, so $60$ in all. Hence $240 - 60 = 180$.",
  "Forgetting the leading-zero restriction, or treating the repeated digit as two different digits.",
  "U04-A-every-digit-zero", "Repetition pattern forced by counting, then a leading-zero correction split into two cases.",
  check=lambda: Integer(sum(1 for t in _product("0123", repeat=5) if set(t) == set("0123") and t[0] != "0")),
  values=[180, 240, 144, 360], cognitive="Analysis",
  numerical=dict(question=r"The number of five-digit numbers whose digits are all from $\{0, 1, 2, 3\}$ and in which each of $0, 1, 2, 3$ appears at least once is", answer=180))

q("U04-A-048", T, "Divisibility by 4 with zero", "Difficult",
  "Multi-step computation MCQ",
  r"Four-digit numbers are formed using four of the digits $0, 1, 2, 3, 4, 5$ without repetition. The number of such numbers that are divisible by $4$ is",
  r"$72$",
  [(r"$84$", r"Fills the first two places in $P(4, 2) = 12$ ways for every ending, allowing a leading zero."),
   (r"$75$", r"Assumes exactly one quarter of the $300$ such four-digit numbers are divisible by $4$."),
   (r"$60$", r"Misses the ending $04$, treating it as not a valid two-digit ending.")],
  r"Possible endings (distinct digits, multiple of $4$): $04, 20, 40$ (containing $0$) and $12, 24, 32, 52$ (without $0$). For an ending with $0$, the first two places come from $4$ nonzero digits: $P(4, 2) = 12$ each, so $36$. For an ending without $0$, the first digit has $3$ nonzero choices and the second $3$, so $9$ each, giving $36$. Total $72$.",
  "Forgetting the leading-zero restriction, or the ending $04$.",
  "U04-A-div4", "Endings split by whether they use zero.",
  check=lambda: Integer(sum(1 for t in _perms("012345", 4) if t[0] != "0" and int(''.join(t)) % 4 == 0)),
  values=[72, 84, 75, 60], cognitive="Analysis",
  numerical=dict(question=r"Four-digit numbers are formed using four of the digits $0, 1, 2, 3, 4, 5$ without repetition. The number of such numbers that are divisible by $4$ is", answer=72))

def _c49():
    st1 = rank("SMALL") == 57
    st2 = sum(1 for w in words("112233") if not any(w[k] == w[k + 1] for k in range(5))) == 36
    return (st1, st2)
q("U04-A-049", T, "Rank and no-adjacent identical digits: statements", "Difficult",
  "Statement-based MCQ",
  r"Statement I: When all the distinct arrangements of the letters of the word SMALL are listed in dictionary order, the word SMALL is at position $57$. Statement II: The number of six-digit numbers formed using all the digits $1, 1, 2, 2, 3, 3$ in which no two equal digits are next to each other is $36$." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Accepts $57$ by forgetting to add $1$ for SMALL itself, and accepts $36$ by not subtracting the $6$ arrangements where all three pairs are together."),
   (ST_TF, r"Accepts $57$ by forgetting to add $1$ for the word itself, but evaluates Statement II correctly."),
   (ST_FT, r"Evaluates Statement I correctly but accepts $36$, stopping inclusion-exclusion after the pairwise terms.")],
  r"Statement I: words beginning with A: $\frac{4!}{2!} = 12$; with L: $4! = 24$; with M: $12$; SA..: $\frac{3!}{2!} = 3$; SL..: $3! = 6$. So $57$ words precede SMALL and its rank is $58$; false. Statement II: total $\frac{6!}{2!\,2!\,2!} = 90$. With a given pair together: $\frac{5!}{2!\,2!} = 30$; two given pairs: $\frac{4!}{2!} = 12$; all three: $3! = 6$. So $90 - 3 \cdot 30 + 3 \cdot 12 - 6 = 30$, not $36$; false.",
  "Stopping inclusion-exclusion early, and the off-by-one in rank.",
  "U04-A-rank-ie-statement", "Two multi-step counts including three-set inclusion-exclusion.",
  check=_c49, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")

q("U04-A-050", T, "Divisible by 5 within a range, digits distinct", "Difficult",
  "Multi-step computation MCQ",
  r"The number of integers from $3000$ to $7999$ (both inclusive) that have all four digits distinct and are divisible by $5$ is",
  r"$504$",
  [(r"$560$", r"Allows last digit $5$ even when the first digit is $5$, using $5 \cdot 2 \cdot 56$."),
   (r"$448$", r"Excludes the numbers with first digit $5$ completely."),
   (r"$1000$", r"Counts all multiples of $5$ in the range, ignoring the distinct-digit condition.")],
  r"The first digit is one of $3, 4, 5, 6, 7$ and the last digit is $0$ or $5$. First digit $3, 4, 6$ or $7$: last digit $0$ or $5$ ($2$ ways), middle two digits in $P(8, 2) = 56$ ways, so $4 \cdot 2 \cdot 56 = 448$. First digit $5$: last digit must be $0$, middle in $56$ ways. Total $448 + 56 = 504$.",
  "Not noticing that the leading digit $5$ blocks the ending $5$.",
  "U04-A-div5-range", "Casework where the leading digit interacts with the divisibility digit.",
  check=lambda: Integer(sum(1 for m in range(3000, 8000) if len(set(str(m))) == 4 and m % 5 == 0)),
  values=[504, 560, 448, 1000], cognitive="Analysis",
  numerical=dict(question=r"The number of integers from $3000$ to $7999$ (both inclusive) that have all four digits distinct and are divisible by $5$ is", answer=504))

q("U04-A-051", T, "Two pairs of identical letters kept apart", "Difficult",
  "Multi-step computation MCQ",
  r"The number of distinct arrangements of the letters of the word ARRANGE in which neither the two A's nor the two R's are next to each other is",
  r"$660$",
  [(r"$900$", r"Only keeps the two R's apart: $1260 - 360$."),
   (r"$540$", r"Subtracts both $360$'s from $1260$ but does not add back the $120$ arrangements with both pairs together."),
   (r"$1140$", r"Removes only the arrangements in which both pairs are together: $1260 - 120$.")],
  r"Total: $\frac{7!}{2!\,2!} = 1260$. A's together: $\frac{6!}{2!} = 360$; R's together: $360$; both together: $5! = 120$. By inclusion-exclusion the required number is $1260 - 360 - 360 + 120 = 660$.",
  "Forgetting to add back the overlap in inclusion-exclusion.",
  "U04-A-not-together-ie", "Two-set inclusion-exclusion with identical letters.",
  check=lambda: Integer(sum(1 for w in words("ARRANGE") if "AA" not in w and "RR" not in w)),
  values=[660, 900, 540, 1140], cognitive="Analysis",
  numerical=dict(question=r"The number of distinct arrangements of the letters of the word ARRANGE in which neither the two A's nor the two R's are next to each other is", answer=660))

def _c52():
    boys = ["b0", "b1", "b2", "b3", "b4"]   # b0 is the particular boy
    girls = ["g0", "g1", "g2", "g3", "g4"]  # g0 is the particular girl
    c = 0
    for bp in _perms(boys):
        for gp in _perms(girls):
            for row in (sum(zip(bp, gp), ()), sum(zip(gp, bp), ())):
                if adjacent(row, "b0", "g0"):
                    c += 1
    return Integer(c)
q("U04-A-052", T, "Alternate arrangement with a particular pair adjacent", "Difficult",
  "Multi-step computation MCQ",
  r"Five boys and five girls stand in a row so that boys and girls alternate. A particular boy $X$ and a particular girl $Y$ must stand next to each other. The number of such arrangements is",
  r"$10368$",
  [(r"$5184$", r"Considers only arrangements beginning with a boy, forgetting those beginning with a girl."),
   (r"$28800$", r"Counts all alternating arrangements, $2 \cdot 5! \cdot 5!$, ignoring the condition on $X$ and $Y$."),
   (r"$20736$", r"Multiplies by $2$ again for the order of $X$ and $Y$, although the pattern already fixes it.")],
  r"Fix the pattern (boy first or girl first): $2$ ways. In a fixed alternating pattern of $10$ places, each of the $9$ pairs of neighbouring places has one boy place and one girl place, so $X, Y$ can be placed in $9$ ways (their order is forced by the pattern). The other $4$ boys and $4$ girls fill their places in $4! \cdot 4! = 576$ ways. Total $2 \cdot 9 \cdot 576 = 10368$.",
  "Double counting the order of the pair when the alternating pattern already fixes it.",
  "U04-A-alternate", "Alternation plus an adjacency condition; careful counting of slots.",
  check=_c52, values=[10368, 5184, 28800, 20736], cognitive="Analysis",
  numerical=dict(question=r"Five boys and five girls stand in a row so that boys and girls alternate. A particular boy $X$ and a particular girl $Y$ must stand next to each other. The number of such arrangements is", answer=10368))

q("U04-A-053", T, "Divisibility by 4 with a non-adjacency condition", "Difficult",
  "Multi-step computation MCQ",
  r"Six-digit numbers are formed using each of the digits $1, 2, 3, 4, 5, 6$ exactly once. The number of such numbers that are divisible by $4$ and in which the digits $5$ and $6$ are not next to each other is",
  r"$120$",
  [(r"$108$", r"For the endings $16$ and $36$ wrongly removes the $3! = 6$ numbers with $5$ in the fourth place, as if $5$ were then next to $6$, giving $2(24 - 6) = 36$ instead of $48$ and total $108$."),
   (r"$168$", r"Removes only the $24$ numbers ending in $56$ and ignores adjacency in the other cases."),
   (r"$192$", r"Counts all numbers divisible by $4$, ignoring the condition on $5$ and $6$.")],
  r"Endings that are multiples of $4$: $12, 16, 24, 32, 36, 52, 56, 64$, each with $4! = 24$ completions. Ending $56$: always adjacent, $0$. Endings $12, 24, 32$: $5, 6$ are among the first four places, adjacent in $3! \cdot 2 = 12$ cases, so $12$ each, total $36$. Endings $16, 36$: $6$ is last and its neighbour is fixed, so all $24$ count, total $48$. Ending $64$: $6$ is fifth, adjacent if $5$ is fourth ($6$ cases), so $18$. Ending $52$: $5$ is fifth, adjacent if $6$ is fourth, so $18$. Total $36 + 48 + 18 + 18 = 120$.",
  "Assuming a digit in the ending can always be adjacent to the free part.",
  "U04-A-div-adj", "Divisibility casework combined with an adjacency condition.",
  check=lambda: Integer(sum(1 for t in _perms("123456") if int(''.join(t)) % 4 == 0 and not adjacent(t, "5", "6"))),
  values=[120, 108, 168, 192], cognitive="Analysis")

q("U04-A-054", T, "Block of identical letters with another pair apart", "Difficult",
  "Multi-step computation MCQ",
  r"The number of distinct arrangements of the letters of the word MISSISSIPPI in which the four S's are together and the two P's are not next to each other is",
  r"$630$",
  [(r"$840$", r"Counts all arrangements with the S's together, $\frac{8!}{4!\,2!}$, ignoring the condition on the P's."),
   (r"$210$", r"Counts the arrangements in which the S's are together and the P's are also together."),
   (r"$15120$", r"Multiplies the correct count by $4!$ for arranging the identical S's inside their block.")],
  r"Treat SSSS as one block. The units are the block, M, I, I, I, I, P, P: $\frac{8!}{4!\,2!} = 840$ arrangements. Those with PP together as well: units block, M, I, I, I, I, PP give $\frac{7!}{4!} = 210$. Hence $840 - 210 = 630$.",
  "Treating identical letters in a block as arrangeable.",
  "U04-A-together-identical", "Block method followed by a complement with identical letters.",
  check=lambda: Integer(sum(1 for w in words("MISSISSIPPI") if "SSSS" in w and "PP" not in w)),
  values=[630, 840, 210, 15120], cognitive="Analysis",
  numerical=dict(question=r"The number of distinct arrangements of the letters of the word MISSISSIPPI in which the four S's are together and the two P's are not next to each other is", answer=630))
