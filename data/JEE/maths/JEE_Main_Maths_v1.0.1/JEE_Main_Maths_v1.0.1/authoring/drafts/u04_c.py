import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools as it_
from collections import Counter as _Counter
from sympy.utilities.iterables import multiset_partitions, multiset_permutations

T, F_ = True, False
ST = ["Both Statement I and Statement II are true",
      "Both Statement I and Statement II are false",
      "Statement I is true but Statement II is false",
      "Statement I is false but Statement II is true"]
STV = {ST[0]: (T, T), ST[1]: (F_, F_), ST[2]: (T, F_), ST[3]: (F_, T)}


def _st(key, why):
    """Statement options: key first, then the other three with rationales from why."""
    others = [s for s in ST if s != key]
    return [(s, why[s]) for s in others], [STV[key]] + [STV[s] for s in others]


def _nsol(n, k, lows=None, highs=None):
    """Brute-force count of integer k-tuples with sum n and lows <= x_i <= highs."""
    lows = lows or [0] * k
    highs = highs or [n - sum(lows) + l for l in lows]
    cnt = 0
    for t in it_.product(*[range(lows[i], highs[i] + 1) for i in range(k)]):
        if sum(t) == n:
            cnt += 1
    return Integer(cnt)


def _partitions_with_sizes(n, sizes):
    """Number of set partitions of n distinct objects into unlabelled blocks of the given sizes."""
    target = sorted(sizes)
    return Integer(sum(1 for p in multiset_partitions(list(range(n)), len(sizes))
                       if sorted(len(b) for b in p) == target))


# ================================================================ EASY
# ---------------------------------------------------------------- 001
def _c001():
    boys, girls = set(range(6)), set(range(6, 11))
    return Integer(sum(1 for p in it_.permutations(range(11), 5) if len(boys & set(p)) == 3))
q("U04-C-001", "Selection and arrangement", "Select then arrange", "Easy", "Multi-step computation MCQ",
  r"From $6$ boys and $5$ girls, $3$ boys and $2$ girls are selected, and the five selected children are then made to stand in a row. The number of such arrangements is",
  r"$24000$",
  [(r"$200$", r"Counts only the selections ${}^{6}C_{3} \times {}^{5}C_{2} = 20 \times 10 = 200$ and never arranges them."),
   (r"$2400$", r"Arranges the boys among themselves and the girls among themselves only: $200 \times 3! \times 2! = 2400$."),
   (r"$288000$", r"Uses ordered selections ${}^{6}P_{3} \cdot {}^{5}P_{2} = 120 \times 20 = 2400$ and then multiplies by $5!$ again, counting order twice.")],
  r"The children can be selected in ${}^{6}C_{3} \times {}^{5}C_{2} = 20 \times 10 = 200$ ways. Each group of five distinct children can stand in a row in $5! = 120$ ways. Hence the number of arrangements is $200 \times 120 = 24000$.",
  "Stopping after the selection step, or arranging only within each gender.",
  "U04-C-select-then-arrange", "Two selections followed by one arrangement; a standard two-stage product.",
  check=_c001, values=[24000, 200, 2400, 288000], cognitive="Application")

# ---------------------------------------------------------------- 002
def _c002():
    nov, tb = set(range(7)), set(range(7, 11))
    c = 0
    for p in it_.permutations(range(11), 5):
        if len(tb & set(p)) == 2 and p[0] in tb and p[4] in tb:
            c += 1
    return Integer(c)
q("U04-C-002", "Selection and arrangement", "Select then arrange with fixed positions", "Easy", "Multi-step computation MCQ",
  r"From $7$ different novels and $4$ different textbooks, $3$ novels and $2$ textbooks are selected and placed in a row on a shelf so that the two textbooks occupy the two end positions. The number of ways of doing this is",
  r"$2520$",
  [(r"$210$", r"Counts only the selections ${}^{7}C_{3} \times {}^{4}C_{2} = 35 \times 6 = 210$."),
   (r"$25200$", r"Ignores the end condition and arranges all five books freely: $210 \times 5! = 25200$."),
   (r"$1260$", r"Arranges the three novels in the middle ($3!$) but does not let the two textbooks swap ends: $210 \times 6 = 1260$.")],
  r"Select the books in ${}^{7}C_{3} \times {}^{4}C_{2} = 35 \times 6 = 210$ ways. The two textbooks fill the two ends in $2! = 2$ ways and the three novels fill the middle three places in $3! = 6$ ways. Total $= 210 \times 2 \times 6 = 2520$.",
  "Forgetting that the two end books can be interchanged.",
  "U04-C-select-then-arrange", "Selection followed by a restricted arrangement; two short stages.",
  check=_c002, values=[2520, 210, 25200, 1260], cognitive="Application")

# ---------------------------------------------------------------- 003
q("U04-C-003", "Distribution and integer solutions", "Non-negative integer solutions", "Easy", "Single-step computation MCQ",
  r"The number of non-negative integral solutions of $x + y + z = 10$ is",
  r"$66$",
  [(r"$36$", r"Uses the positive-solution count ${}^{10-1}C_{2} = {}^{9}C_{2} = 36$."),
   (r"$45$", r"Uses ${}^{n}C_{r-1} = {}^{10}C_{2} = 45$."),
   (r"$55$", r"Uses ${}^{n+r-2}C_{r-1} = {}^{11}C_{2} = 55$, one short in the top entry.")],
  r"A solution corresponds to arranging $10$ identical stars and $2$ identical bars in a row, that is, choosing the $2$ bar positions out of $12$. Hence the count is ${}^{12}C_{2} = 66$.",
  "Mixing up the formulas for positive and non-negative solutions.",
  "U04-C-stars-bars-basic", "One formula applied directly.",
  check=lambda: _nsol(10, 3), values=[66, 36, 45, 55], cognitive="Application",
  numerical=dict(question=r"The number of non-negative integral solutions of $x + y + z = 10$ is", answer=66))

# ---------------------------------------------------------------- 004
q("U04-C-004", "Distribution and integer solutions", "Positive integer solutions", "Easy", "Single-step computation MCQ",
  r"The number of positive integral solutions of $x_1 + x_2 + x_3 + x_4 = 12$ is",
  r"$165$",
  [(r"$455$", r"Uses the non-negative count ${}^{12+3}C_{3} = {}^{15}C_{3} = 455$."),
   (r"$220$", r"Uses ${}^{n}C_{r-1} = {}^{12}C_{3} = 220$."),
   (r"$330$", r"Uses ${}^{n-1}C_{r} = {}^{11}C_{4} = 330$, choosing $4$ gaps instead of $3$.")],
  r"Place $12$ identical units in a row; there are $11$ gaps between them. Choosing $3$ of these gaps for dividers splits the units into $4$ positive parts, so the count is ${}^{11}C_{3} = 165$.",
  "Using the non-negative formula when each variable must be positive.",
  "U04-C-stars-bars-basic", "Direct use of the positive-solution formula.",
  check=lambda: _nsol(12, 4, [1] * 4), values=[165, 455, 220, 330], cognitive="Application",
  numerical=dict(question=r"The number of positive integral solutions of $x_1 + x_2 + x_3 + x_4 = 12$ is", answer=165))

# ---------------------------------------------------------------- 005
q("U04-C-005", "Distribution and integer solutions", "Distinct objects into distinct boxes", "Easy", "Single-step computation MCQ",
  r"The number of ways in which $4$ distinct balls can be placed in $3$ distinct boxes, where a box may hold any number of balls and may be left empty, is",
  r"$81$",
  [(r"$64$", r"Swaps base and exponent: $4^3 = 64$."),
   (r"$24$", r"Uses ${}^{4}P_{3} = 24$, as if each box received exactly one ball."),
   (r"$15$", r"Treats the balls as identical: ${}^{4+2}C_{2} = 15$.")],
  r"Each ball independently goes into any one of the $3$ boxes. By the multiplication principle the number of ways is $3^4 = 81$.",
  "Writing $4^3$ instead of $3^4$ (choices per object raised to the number of objects).",
  "U04-C-distinct-into-boxes", "Single application of the multiplication principle.",
  check=lambda: Integer(len(list(it_.product(range(3), repeat=4)))), values=[81, 64, 24, 15], cognitive="Understanding")

# ---------------------------------------------------------------- 006
def _c006():
    row = list(range(6)) + ["D"] * 3
    c = 0
    for w in multiset_permutations(row):
        if all(not (w[i] == "D" and w[i + 1] == "D") for i in range(8)):
            c += 1
    return Integer(c)
q("U04-C-006", "Permutations with restrictions", "Gap method with distinct and identical objects", "Easy", "Single-step computation MCQ",
  r"Six different novels and $3$ identical copies of a dictionary are to be arranged in a row on a shelf so that no two copies of the dictionary are next to each other. The number of such arrangements is",
  r"$25200$",
  [(r"$151200$", r"Treats the three copies of the dictionary as distinct: $6! \times {}^{7}P_{3} = 720 \times 210 = 151200$."),
   (r"$7200$", r"Uses only the $5$ gaps between novels, leaving out the two ends: $6! \times {}^{5}C_{3} = 720 \times 10 = 7200$."),
   (r"$60480$", r"Ignores the restriction and counts all arrangements: $\frac{9!}{3!} = 60480$.")],
  r"Arrange the $6$ different novels first in $6! = 720$ ways. They create $7$ gaps (including the two ends), and the dictionaries must go into $3$ different gaps. Since the copies are identical, only the choice of gaps matters: ${}^{7}C_{3} = 35$ ways. Total $= 720 \times 35 = 25200$.",
  "Arranging identical copies among the chosen gaps as if they were distinct, or leaving out the end gaps.",
  "U04-C-gap-mixed-identical", "One gap count with identical separated objects, multiplied by one arrangement.",
  check=_c006, values=[25200, 151200, 7200, 60480], cognitive="Application")

# ---------------------------------------------------------------- 007
def _c007():
    return Integer(sum(1 for w in it_.product(range(6), repeat=3) if len(set(w)) < 3))
q("U04-C-007", "Permutations with restrictions", "Complementary counting", "Easy", "Single-step computation MCQ",
  r"Three-letter codes are formed using the letters $P, Q, R, S, T, U$, with repetition allowed. The number of codes in which at least one letter occurs more than once is",
  r"$96$",
  [(r"$120$", r"Counts the codes with all letters different, ${}^{6}P_{3} = 120$, which is the complement."),
   (r"$90$", r"Counts only codes with exactly two equal letters, $6 \times 5 \times 3 = 90$, missing the $6$ codes with all three equal."),
   (r"$210$", r"Subtracts only the $6$ codes with all three letters equal: $216 - 6 = 210$.")],
  r"Without restriction there are $6^3 = 216$ codes. Codes with all three letters different number ${}^{6}P_{3} = 120$. So codes with some letter repeated number $216 - 120 = 96$.",
  "Taking the complement of 'all same' instead of 'all different'.",
  "U04-C-complement-repetition", "One complement computation.",
  check=_c007, values=[96, 120, 90, 210], cognitive="Application")

# ---------------------------------------------------------------- 008
q("U04-C-008", "Division into groups", "Division into equal unlabelled groups", "Easy", "Single-step computation MCQ",
  r"The number of ways of dividing $6$ distinct books into $3$ groups of $2$ books each (the groups are not distinguished from one another) is",
  r"$15$",
  [(r"$90$", r"Treats the groups as labelled: $\frac{6!}{2!\,2!\,2!} = 90$."),
   (r"$45$", r"Divides $90$ by $2!$ instead of by $3!$."),
   (r"$30$", r"Divides $90$ by $3$ instead of by $3!$.")],
  r"If the three groups were labelled, the count would be $\frac{6!}{2!\,2!\,2!} = 90$. Since the three equal-sized groups are interchangeable, divide by $3! = 6$ to get $15$. Equivalently, pair the first book in $5$ ways, then the next unpaired book in $3$ ways: $5 \times 3 = 15$.",
  "Not dividing by the factorial of the number of equal-sized groups.",
  "U04-C-groups-unlabelled", "One formula with the equal-group correction.",
  check=lambda: _partitions_with_sizes(6, [2, 2, 2]), values=[15, 90, 45, 30], cognitive="Understanding",
  numerical=dict(question=r"The number of ways of dividing $6$ distinct books into $3$ groups of $2$ books each, where the groups are not distinguished from one another, is", answer=15))

# ---------------------------------------------------------------- 009
def _c009():
    # books 0..7 (book 0 = atlas, book 1 = dictionary), students 0..3
    return Integer(sum(1 for a in it_.product(range(4), repeat=8)
                       if all(a.count(s) == 2 for s in range(4)) and a[0] == a[1]))
q("U04-C-009", "Division into groups", "Equal distribution to distinct persons with a pair together", "Easy", "Multi-step computation MCQ",
  r"Eight different books, among them an atlas and a dictionary, are to be distributed among $4$ students so that each student receives exactly $2$ books. The number of distributions in which the atlas and the dictionary go to the same student is",
  r"$360$",
  [(r"$2520$", r"Ignores the condition on the atlas and the dictionary: $\frac{8!}{(2!)^4} = 2520$."),
   (r"$90$", r"Distributes the other $6$ books among $3$ students ($\frac{6!}{(2!)^3} = 90$) but forgets to choose which student gets the atlas and the dictionary."),
   (r"$60$", r"Chooses the student for the atlas and the dictionary ($4$ ways) but only splits the other $6$ books into $15$ unlabelled pairs, never handing them to the $3$ remaining students: $4 \times 15 = 60$.")],
  r"The atlas and the dictionary together form one student's full share; that student can be chosen in $4$ ways. The remaining $6$ books are then given $2$ each to the other $3$ students in ${}^{6}C_{2} \times {}^{4}C_{2} = 15 \times 6 = 90$ ways. Total $= 4 \times 90 = 360$.",
  "Forgetting that the recipients are distinct, either for the fixed pair or for the remaining books.",
  "U04-C-groups-labelled-pair", "A forced pair fixes one share; two short stages with labelled recipients.",
  check=_c009, values=[360, 2520, 90, 60], cognitive="Application",
  numerical=dict(question=r"Eight different books, among them an atlas and a dictionary, are to be distributed among $4$ students so that each student receives exactly $2$ books. The number of distributions in which the atlas and the dictionary go to the same student is", answer=360))

# ---------------------------------------------------------------- 010
def _c010():
    return Integer(sum(1 for p in it_.permutations(range(8), 5) if 0 in p))
q("U04-C-010", "Selection and arrangement", "Select then arrange with an included member", "Easy", "Multi-step computation MCQ",
  r"From a group of $8$ persons that includes a particular person $P$, $5$ persons are to be selected and seated in a row of $5$ chairs, with $P$ always among those selected. The number of ways of doing this is",
  r"$4200$",
  [(r"$840$", r"Selects the other four in ${}^{7}C_{4} = 35$ ways and arranges only them: $35 \times 4! = 840$, leaving $P$ unplaced."),
   (r"$6720$", r"Ignores the condition on $P$: ${}^{8}P_{5} = 6720$."),
   (r"$35$", r"Counts only the selections ${}^{7}C_{4} = 35$.")],
  r"Since $P$ must be selected, choose the remaining $4$ persons from the other $7$ in ${}^{7}C_{4} = 35$ ways. The $5$ selected persons, $P$ included, can be seated in $5! = 120$ ways. Total $= 35 \times 120 = 4200$.",
  "Forgetting to arrange the compulsory member along with the others.",
  "U04-C-select-then-arrange", "Selection with one forced member followed by arrangement.",
  check=_c010, values=[4200, 840, 6720, 35], cognitive="Application")

# ---------------------------------------------------------------- 011
q("U04-C-011", "Distribution and integer solutions", "Identical objects, each recipient non-empty", "Easy", "Single-step computation MCQ",
  r"The number of ways of distributing $8$ identical chocolates among $3$ children so that each child gets at least one chocolate is",
  r"$21$",
  [(r"$45$", r"Allows a child to get none: ${}^{8+2}C_{2} = 45$."),
   (r"$28$", r"Uses ${}^{n}C_{r-1} = {}^{8}C_{2} = 28$."),
   (r"$56$", r"Uses ${}^{n}C_{r} = {}^{8}C_{3} = 56$, as if choosing $3$ of the chocolates.")],
  r"If the children get $x, y, z \ge 1$ chocolates, then $x + y + z = 8$. The $8$ chocolates in a row have $7$ gaps; choosing $2$ of them for dividers gives ${}^{7}C_{2} = 21$ ways.",
  "Using the non-negative formula when each child must receive at least one.",
  "U04-C-identical-distribution", "Direct positive stars and bars.",
  check=lambda: _nsol(8, 3, [1] * 3), values=[21, 45, 28, 56], cognitive="Application",
  numerical=dict(question=r"The number of ways of distributing $8$ identical chocolates among $3$ children so that each child gets at least one chocolate is", answer=21))

# ---------------------------------------------------------------- 012
def _c012():
    c = 0
    for pos in it_.combinations(range(10), 4):
        if all(pos[i + 1] - pos[i] > 1 for i in range(3)):
            c += 1
    return Integer(c)
q("U04-C-012", "Permutations with restrictions", "Gap method with identical objects", "Easy", "Single-step computation MCQ",
  r"The number of ways of arranging $6$ identical plus signs and $4$ identical minus signs in a row so that no two minus signs are adjacent is",
  r"$35$",
  [(r"$15$", r"Counts only $6$ gaps for $6$ plus signs: ${}^{6}C_{4} = 15$."),
   (r"$5$", r"Uses only the $5$ gaps between plus signs, leaving out the ends: ${}^{5}C_{4} = 5$."),
   (r"$840$", r"Treats the minus signs as distinct: ${}^{7}P_{4} = 840$.")],
  r"Place the $6$ plus signs first (one way, since they are identical). They create $7$ gaps, including both ends. The minus signs must occupy $4$ different gaps, and since they are identical this can be done in ${}^{7}C_{4} = 35$ ways.",
  "Miscounting the gaps created by a row of objects.",
  "U04-C-gap-method", "One gap count and one selection.",
  check=_c012, values=[35, 15, 5, 840], cognitive="Application")

# ---------------------------------------------------------------- 013
def _c013():
    # persons 0..5 men, 6..9 women; chairs left, middle, right
    return Integer(sum(1 for p in it_.permutations(range(10), 3) if not (p[0] < 6 and p[2] < 6)))
q("U04-C-013", "Selection and arrangement", "Complement on positions in select and arrange", "Easy", "Multi-step computation MCQ",
  r"From $6$ men and $4$ women, $3$ persons are selected and seated in a row of $3$ chairs. The number of such seatings in which the two end chairs are not both occupied by men is",
  r"$480$",
  [(r"$600$", r"Removes only the seatings with three men, ${}^{6}P_{3} = 120$: $720 - 120 = 600$."),
   (r"$240$", r"Reports the excluded seatings themselves, $6 \times 5 \times 8 = 240$."),
   (r"$690$", r"Seats men at both ends in $6 \times 5 = 30$ ways but forgets to fill the middle chair: $720 - 30 = 690$.")],
  r"All seatings of $3$ out of $10$ persons number ${}^{10}P_{3} = 720$. Seatings with men at both ends: the ends in $6 \times 5 = 30$ ways and the middle chair by any of the remaining $8$ persons, giving $240$. Hence the required number is $720 - 240 = 480$.",
  "Confusing 'both ends men' with 'all three men', or leaving a chair unfilled in the excluded count.",
  "U04-C-complement-positions", "One complement on a positional condition in an arrangement count.",
  check=_c013, values=[480, 600, 240, 690], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c014():
    for n in range(3, 60):
        if _nsol(n, 3, [1] * 3) == 28:
            return Integer(n)
q("U04-C-014", "Distribution and integer solutions", "Reverse stars and bars", "Easy", "Inverse/parameter MCQ",
  r"If the number of positive integral solutions of $x_1 + x_2 + x_3 = n$ is $28$, then $n$ equals",
  r"$9$",
  [(r"$8$", r"Solves ${}^{n-1}C_{2} = 28$ correctly to get $n - 1 = 8$ but reports $8$."),
   (r"$6$", r"Uses the non-negative formula ${}^{n+2}C_{2} = 28$, giving $n + 2 = 8$."),
   (r"$7$", r"Uses ${}^{n+1}C_{2} = 28$, mixing the two formulas, giving $n + 1 = 8$.")],
  r"The number of positive solutions is ${}^{n-1}C_{2}$. Setting $\frac{(n-1)(n-2)}{2} = 28$ gives $(n-1)(n-2) = 56 = 8 \times 7$, so $n - 1 = 8$ and $n = 9$.",
  "Using the wrong stars and bars formula when working backwards.",
  "U04-C-stars-bars-inverse", "Single equation in $n$ from a known formula.",
  check=_c014, values=[9, 8, 6, 7], cognitive="Application")

# ---------------------------------------------------------------- 015
def _c015():
    return Integer(sum(1 for a in it_.product(range(4), repeat=5) if len(set(a)) > 1))
q("U04-C-015", "Distribution and integer solutions", "Complement with distinct objects", "Easy", "Single-step computation MCQ",
  r"Five distinct letters are to be posted in $4$ letter boxes. The number of ways of posting them so that not all the letters go into the same box is",
  r"$1020$",
  [(r"$1024$", r"Counts all postings $4^5 = 1024$ without removing the excluded ones."),
   (r"$620$", r"Swaps base and exponent, $5^4 = 625$, then subtracts $5$."),
   (r"$1019$", r"Treats 'all in the same box' as a single case: $1024 - 1 = 1019$.")],
  r"Each letter can go into any of the $4$ boxes, giving $4^5 = 1024$ postings. All five letters go into the same box in exactly $4$ ways (one for each box). Hence the required number is $1024 - 4 = 1020$.",
  "Counting the excluded case as one instead of one per box.",
  "U04-C-distinct-into-boxes", "One power and one subtraction.",
  check=_c015, values=[1020, 1024, 620, 1019], cognitive="Application")

# ---------------------------------------------------------------- 016
q("U04-C-016", "Division into groups", "Division into unequal groups", "Easy", "Single-step computation MCQ",
  r"The number of ways of dividing $7$ distinct objects into three groups containing $1$, $2$ and $4$ objects respectively is",
  r"$105$",
  [(r"$630$", r"Multiplies by $3!$ as if the groups were to be assigned to three distinct persons."),
   (r"$35$", r"Only chooses the group of four: ${}^{7}C_{4} = 35$, and stops."),
   (r"$210$", r"Divides $7!$ by $4!$ only, omitting the $2!$ for the group of two: $\frac{5040}{24} = 210$.")],
  r"Choose the group of $4$ in ${}^{7}C_{4} = 35$ ways, then the group of $2$ from the remaining $3$ in ${}^{3}C_{2} = 3$ ways; the last object forms the group of $1$. Since the group sizes are all different, no further division is needed: $35 \times 3 = 105 = \frac{7!}{1!\,2!\,4!}$.",
  "Dividing or multiplying by $3!$ when the group sizes are already all different.",
  "U04-C-groups-unlabelled", "One multinomial-type quotient with no symmetry correction.",
  check=lambda: _partitions_with_sizes(7, [1, 2, 4]), values=[105, 630, 35, 210], cognitive="Understanding")

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 017
q("U04-C-017", "Selection and arrangement", "Words from a word with repeated letters", "Medium", "Multi-step computation MCQ",
  r"The number of three-letter words (meaningful or not) that can be formed using the letters of the word BALLOON, each letter being used at most as many times as it appears in BALLOON, is",
  r"$84$",
  [(r"$60$", r"Counts only words with three different letters, ${}^{5}P_{3} = 60$, missing the words with a repeated L or O."),
   (r"$210$", r"Treats all seven letters as distinct: ${}^{7}P_{3} = 210$."),
   (r"$68$", r"Counts the repeated-letter case as $2 \times 4 = 8$ selections but does not arrange them.")],
  r"The letters are B, A, N once each and L, O twice each, so there are $5$ distinct letters. All different: ${}^{5}P_{3} = 60$. Two alike and one different: choose the pair (L or O) in $2$ ways, the other letter from the remaining $4$ in $4$ ways, and arrange in $\frac{3!}{2!} = 3$ ways, giving $24$. Total $= 60 + 24 = 84$.",
  "Ignoring the case with a repeated letter, or not arranging it.",
  "U04-C-words-from-multiset", "Two cases, each a selection followed by an arrangement.",
  check=lambda: Integer(len(set(it_.permutations("BALLOON", 3)))), values=[84, 60, 210, 68], cognitive="Analysis")

# ---------------------------------------------------------------- 018
def _c018():
    c = 0
    for com in it_.combinations(range(12), 5):
        if sum(1 for x in com if x >= 7) == 2:
            c += len(list(it_.permutations(com, 2)))
    return Integer(c)
q("U04-C-018", "Selection and arrangement", "Selection followed by assignment of posts", "Medium", "Multi-step computation MCQ",
  r"A committee of $5$ is to be formed from $7$ men and $5$ women so that it contains exactly $2$ women. The committee then chooses a chairperson and a secretary from among its members, the two being different persons. The number of ways of completing both steps is",
  r"$7000$",
  [(r"$350$", r"Counts only the committees ${}^{5}C_{2} \times {}^{7}C_{3} = 10 \times 35 = 350$."),
   (r"$3500$", r"Chooses the two office bearers as an unordered pair: $350 \times {}^{5}C_{2} = 3500$."),
   (r"$8750$", r"Allows the same member to hold both posts: $350 \times 5 \times 5 = 8750$.")],
  r"The committee can be formed in ${}^{5}C_{2} \times {}^{7}C_{3} = 10 \times 35 = 350$ ways. From its $5$ members the chairperson and the secretary (distinct roles) are chosen in ${}^{5}P_{2} = 20$ ways. Total $= 350 \times 20 = 7000$.",
  "Treating two distinct posts as an unordered selection.",
  "U04-C-select-then-assign", "Two stages: a restricted selection, then an ordered choice.",
  check=_c018, values=[7000, 350, 3500, 8750], cognitive="Application")

# ---------------------------------------------------------------- 019
def _c019():
    c = 0
    for p in it_.permutations(range(10), 4):
        s = sorted(p)
        if all(s[i + 1] - s[i] > 1 for i in range(3)):
            c += 1
    return Integer(c)
q("U04-C-019", "Permutations with restrictions", "Gap method for seating", "Medium", "Multi-step computation MCQ",
  r"Four different persons are to be seated in a row of $10$ chairs so that no two of them occupy adjacent chairs. Two seatings are different if some person occupies a different chair. The number of ways of doing this is",
  r"$840$",
  [(r"$35$", r"Chooses the chairs, ${}^{7}C_{4} = 35$, but does not arrange the four persons on them."),
   (r"$5040$", r"Ignores the restriction: ${}^{10}P_{4} = 5040$."),
   (r"$360$", r"Takes only $6$ gaps around the $6$ empty chairs: ${}^{6}C_{4} \times 4! = 15 \times 24 = 360$.")],
  r"Line up the $6$ empty chairs; they create $7$ gaps including both ends. The occupied chairs must lie in $4$ different gaps, chosen in ${}^{7}C_{4} = 35$ ways. The four persons are then arranged on these chairs in $4! = 24$ ways. Total $= 35 \times 24 = 840$.",
  "Miscounting the gaps, or forgetting that the persons are distinct.",
  "U04-C-gap-method", "Recognising empty chairs as separators, then arranging.",
  check=_c019, values=[840, 35, 5040, 360], cognitive="Application")

# ---------------------------------------------------------------- 020
q("U04-C-020", "Distribution and integer solutions", "Solutions with lower bounds", "Medium", "Multi-step computation MCQ",
  r"The number of integral solutions of $x + y + z + w = 20$ with $x \ge 1$, $y \ge 2$, $z \ge 3$ and $w \ge 0$ is",
  r"$680$",
  [(r"$1771$", r"Ignores the lower bounds and counts all non-negative solutions: ${}^{20+3}C_{3} = {}^{23}C_{3} = 1771$."),
   (r"$286$", r"Substitutes correctly to get a total of $14$ but then counts positive solutions: ${}^{13}C_{3} = 286$."),
   (r"$560$", r"Also treats $w$ as positive, reducing the total to $13$: ${}^{13+3}C_{3} = {}^{16}C_{3} = 560$.")],
  r"Put $x = x' + 1$, $y = y' + 2$, $z = z' + 3$ with $x', y', z', w \ge 0$. Then $x' + y' + z' + w = 20 - 6 = 14$, whose number of non-negative solutions is ${}^{14+3}C_{3} = {}^{17}C_{3} = 680$.",
  "Mishandling the shift that converts lower bounds to non-negative variables.",
  "U04-C-stars-bars-bounds", "Substitution for three different lower bounds, then stars and bars.",
  check=lambda: _nsol(20, 4, [1, 2, 3, 0]), values=[680, 1771, 286, 560], cognitive="Application",
  numerical=dict(question=r"The number of integral solutions of $x + y + z + w = 20$ with $x \ge 1$, $y \ge 2$, $z \ge 3$ and $w \ge 0$ is", answer=680))

# ---------------------------------------------------------------- 021
q("U04-C-021", "Distribution and integer solutions", "Solutions with lower and upper bounds", "Medium", "Multi-step computation MCQ",
  r"Three dice, coloured red, blue and green, are thrown, and each shows a number from $1$ to $6$. The number of outcomes (ordered by colour) in which the three numbers shown add up to $12$ is",
  r"$25$",
  [(r"$55$", r"Shifts to $a' + b' + c' = 9$ with $a', b', c' \ge 0$ but ignores the upper limit $6$: ${}^{11}C_{2} = 55$."),
   (r"$45$", r"Removes the excess cases for one die only: $55 - 10 = 45$."),
   (r"$10$", r"Treats a face value of $6$ as exceeding the limit, removing $3 \times {}^{6}C_{2} = 45$: $55 - 45 = 10$.")],
  r"Let the dice show $a, b, c$ with $1 \le a, b, c \le 6$ and $a + b + c = 12$. Put $a' = a - 1$ etc., so $a' + b' + c' = 9$ with $0 \le a', b', c' \le 5$. Without the upper limit there are ${}^{11}C_{2} = 55$ solutions. If $a' \ge 6$, then $a'' + b' + c' = 3$ has ${}^{5}C_{2} = 10$ solutions; likewise for $b'$ and $c'$. Two variables cannot both be at least $6$ since $12 > 9$. Hence the count is $55 - 30 = 25$.",
  "Handling the lower bound but not the upper bound, or removing the excess for only one variable.",
  "U04-C-stars-bars-two-sided", "Lower-bound shift followed by an upper-bound complement over three variables.",
  check=lambda: _nsol(12, 3, [1] * 3, [6] * 3), values=[25, 55, 45, 10], cognitive="Analysis",
  numerical=dict(question=r"Three dice, coloured red, blue and green, are thrown, and each shows a number from $1$ to $6$. The number of outcomes (ordered by colour) in which the three numbers shown add up to $12$ is", answer=25))

# ---------------------------------------------------------------- 022
def _c022():
    return Integer(sum(1 for a in it_.product(range(3), repeat=5) if len(set(a)) == 3))
q("U04-C-022", "Distribution and integer solutions", "Distinct objects, no box empty", "Medium", "Multi-step computation MCQ",
  r"The number of ways of placing $5$ distinct balls in $3$ distinct boxes so that no box is empty is",
  r"$150$",
  [(r"$540$", r"Puts one chosen ball in each box (${}^{5}P_{3} = 60$) and then places the remaining two freely ($3^2 = 9$): $540$, which counts each placement several times."),
   (r"$243$", r"Ignores the non-empty condition: $3^5 = 243$."),
   (r"$90$", r"Considers only the split $(2, 2, 1)$, missing the split $(3, 1, 1)$ which gives $60$ more.")],
  r"The possible box sizes are $(3,1,1)$ and $(2,2,1)$ in some order. For $(3,1,1)$: choose the box holding three ($3$ ways) and its balls (${}^{5}C_{3} = 10$ ways), then put the other two balls one in each remaining box ($2! = 2$ ways), giving $60$. For $(2,2,1)$: $\frac{5!}{2!\,2!\,1!\,2!} = 15$ groupings times $3!$ assignments, giving $90$. Total $= 60 + 90 = 150$, which also equals $3^5 - 3 \cdot 2^5 + 3 = 150$.",
  "Fixing one ball per box first and then distributing the rest, which overcounts.",
  "U04-C-distinct-onto", "Case split by box sizes, or complement over three boxes.",
  check=_c022, values=[150, 540, 243, 90], cognitive="Analysis")

# ---------------------------------------------------------------- 023
def _c023():
    c = 0
    for w in multiset_permutations(list("RRRRRRBBBGG")):
        if all(not (w[i] != "R" and w[i + 1] != "R") for i in range(10)):
            c += 1
    return Integer(c)
q("U04-C-023", "Permutations with restrictions", "Gap method with two kinds of separated objects", "Medium", "Multi-step computation MCQ",
  r"Six identical red balls, three identical blue balls and two identical green balls are to be arranged in a row so that no two non-red balls are adjacent. The number of such arrangements is",
  r"$210$",
  [(r"$21$", r"Chooses the $5$ gaps, ${}^{7}C_{5} = 21$, but forgets to decide which of them get blue and which get green."),
   (r"$2520$", r"Treats the five non-red balls as distinct: ${}^{7}P_{5} = 2520$."),
   (r"$60$", r"Uses only $6$ gaps: ${}^{6}C_{5} \times \frac{5!}{3!\,2!} = 6 \times 10 = 60$.")],
  r"Place the $6$ red balls; they create $7$ gaps. The $5$ non-red balls must occupy $5$ different gaps, chosen in ${}^{7}C_{5} = 21$ ways. In the chosen gaps (taken left to right) the $3$ blue and $2$ green balls can be placed in $\frac{5!}{3!\,2!} = 10$ ways. Total $= 21 \times 10 = 210$.",
  "Forgetting the internal arrangement of two colours of identical balls.",
  "U04-C-gap-method-identical", "Gap selection combined with arranging identical objects of two kinds.",
  check=_c023, values=[210, 21, 2520, 60], cognitive="Analysis")

# ---------------------------------------------------------------- 024
def _c024():
    c = 0
    for p in it_.permutations(range(11), 4):
        s = sum(1 for x in p if x < 5)
        if 0 < s < 4:
            c += 1
    return Integer(c)
q("U04-C-024", "Selection and arrangement", "Complement for a mixed line-up", "Medium", "Multi-step computation MCQ",
  r"Four students are selected from $5$ seniors and $6$ juniors and lined up in a row for a photograph. The number of line-ups that contain at least one senior and at least one junior is",
  r"$7440$",
  [(r"$310$", r"Counts selections only: ${}^{11}C_{4} - {}^{5}C_{4} - {}^{6}C_{4} = 330 - 5 - 15 = 310$."),
   (r"$7800$", r"Removes only the all-senior line-ups: $7920 - 120 = 7800$."),
   (r"$7560$", r"Removes only the all-junior line-ups: $7920 - 360 = 7560$.")],
  r"All line-ups of $4$ from $11$ students number ${}^{11}P_{4} = 7920$. All-senior line-ups number ${}^{5}P_{4} = 120$ and all-junior line-ups ${}^{6}P_{4} = 360$; these two sets do not overlap. Hence the required number is $7920 - 120 - 360 = 7440$.",
  "Removing only one of the two excluded cases.",
  "U04-C-complement-select-arrange", "Complement with two disjoint excluded cases in an arrangement count.",
  check=_c024, values=[7440, 310, 7800, 7560], cognitive="Application")

# ---------------------------------------------------------------- 025
q("U04-C-025", "Distribution and integer solutions", "Identical objects with a minimum per box", "Medium", "Multi-step computation MCQ",
  r"The number of ways of distributing $15$ identical balls into $4$ distinct boxes so that each box receives at least $2$ balls is",
  r"$120$",
  [(r"$364$", r"Uses 'at least one' instead of 'at least two': ${}^{14}C_{3} = 364$."),
   (r"$816$", r"Ignores the condition: ${}^{15+3}C_{3} = {}^{18}C_{3} = 816$."),
   (r"$165$", r"After placing $2$ in each box, uses ${}^{7+4}C_{3} = {}^{11}C_{3} = 165$ instead of ${}^{7+3}C_{3}$.")],
  r"First put $2$ balls in each box, using $8$ balls. The remaining $7$ identical balls go into $4$ boxes freely, which is the number of non-negative solutions of $y_1 + y_2 + y_3 + y_4 = 7$, namely ${}^{7+3}C_{3} = {}^{10}C_{3} = 120$.",
  "Not converting the minimum to a pre-allocation before using stars and bars.",
  "U04-C-stars-bars-bounds", "Pre-allocation followed by non-negative stars and bars.",
  check=lambda: _nsol(15, 4, [2] * 4), values=[120, 364, 816, 165], cognitive="Application",
  numerical=dict(question=r"The number of ways of distributing $15$ identical balls into $4$ distinct boxes so that each box receives at least $2$ balls is", answer=120))

# ---------------------------------------------------------------- 026
def _c026():
    return Integer(sum(1 for t in it_.product(range(1, 12, 2), repeat=3) if sum(t) == 11))
q("U04-C-026", "Distribution and integer solutions", "Solutions in odd positive integers", "Medium", "Multi-step computation MCQ",
  r"The number of ordered triples $(x, y, z)$ of odd positive integers satisfying $x + y + z = 11$ is",
  r"$15$",
  [(r"$45$", r"Drops the 'odd' condition and counts all positive solutions: ${}^{10}C_{2} = 45$."),
   (r"$21$", r"Writes $x = 2a + 1$ etc. but gets $a + b + c = \frac{11 - 1}{2} = 5$, giving ${}^{7}C_{2} = 21$."),
   (r"$3$", r"Reaches $a + b + c = 4$ correctly but counts positive solutions: ${}^{3}C_{2} = 3$.")],
  r"Write $x = 2a + 1$, $y = 2b + 1$, $z = 2c + 1$ with $a, b, c \ge 0$. Then $2(a + b + c) + 3 = 11$, so $a + b + c = 4$. The number of non-negative solutions is ${}^{4+2}C_{2} = 15$.",
  "Mishandling the substitution for odd values.",
  "U04-C-stars-bars-parity", "Parity substitution followed by stars and bars.",
  check=_c026, values=[15, 45, 21, 3], cognitive="Application",
  numerical=dict(question=r"The number of ordered triples $(x, y, z)$ of odd positive integers satisfying $x + y + z = 11$ is", answer=15))

# ---------------------------------------------------------------- 027
def _c027():
    return Integer(sum(1 for t in it_.product(range(7), repeat=4) if sum(t) <= 6))
q("U04-C-027", "Distribution and integer solutions", "Solutions of an inequality", "Medium", "Multi-step computation MCQ",
  r"The number of ordered quadruples $(x, y, z, w)$ of non-negative integers satisfying $x + y + z + w \le 6$ is",
  r"$210$",
  [(r"$84$", r"Counts only the equality $x + y + z + w = 6$: ${}^{9}C_{3} = 84$."),
   (r"$120$", r"Introduces a slack variable (five variables, total $6$) but uses ${}^{10}C_{3}$ instead of ${}^{10}C_{4}$."),
   (r"$126$", r"Treats the inequality as strict, $x + y + z + w \le 5$: ${}^{9}C_{4} = 126$.")],
  r"Introduce a slack variable $s = 6 - (x + y + z + w) \ge 0$. Then $x + y + z + w + s = 6$ in non-negative integers, which has ${}^{6+4}C_{4} = {}^{10}C_{4} = 210$ solutions.",
  "Forgetting that the slack variable adds one to the number of variables.",
  "U04-C-stars-bars-inequality", "Slack-variable conversion then stars and bars.",
  check=_c027, values=[210, 84, 120, 126], cognitive="Application")

# ---------------------------------------------------------------- 028
def _c028():
    return Integer(sum(1 for a in it_.product(range(3), repeat=12) if all(v == 4 for v in _Counter(a).values()) and len(set(a)) == 3))
q("U04-C-028", "Division into groups", "Equal groups assigned to distinct tasks", "Medium", "Multi-step computation MCQ",
  r"Twelve distinct students are to be divided into three groups of $4$ students each, and the groups are to be assigned to three different projects, one project per group. The number of ways of doing this is",
  r"$34650$",
  [(r"$5775$", r"Forms the three unlabelled groups but does not assign them to the projects: $\frac{12!}{(4!)^3\,3!} = 5775$."),
   (r"$495$", r"Selects only the first group: ${}^{12}C_{4} = 495$."),
   (r"$207900$", r"Computes the labelled count $\frac{12!}{(4!)^3} = 34650$ and then multiplies by $3!$ again.")],
  r"Choose the students for the first project in ${}^{12}C_{4} = 495$ ways, for the second in ${}^{8}C_{4} = 70$ ways, and the remaining $4$ go to the third. Total $= 495 \times 70 = 34650 = \frac{12!}{(4!)^3}$.",
  "Confusing unlabelled division with distribution to distinct recipients.",
  "U04-C-groups-labelled", "Successive selections for labelled groups; recognising no symmetry division is needed.",
  check=_c028, values=[34650, 5775, 495, 207900], cognitive="Application")

# ---------------------------------------------------------------- 029
q("U04-C-029", "Division into groups", "Many equal unlabelled groups", "Medium", "Multi-step computation MCQ",
  r"The number of ways of dividing $12$ distinct objects into $4$ groups of $3$ objects each (the groups are not distinguished from one another) is",
  r"$15400$",
  [(r"$369600$", r"Treats the groups as labelled: $\frac{12!}{(3!)^4} = 369600$."),
   (r"$61600$", r"Divides the labelled count by $3!$ instead of $4!$."),
   (r"$220$", r"Forms only one group: ${}^{12}C_{3} = 220$.")],
  r"Labelled groups would give $\frac{12!}{(3!)^4} = 369600$. The $4$ groups are of equal size and interchangeable, so divide by $4! = 24$: $\frac{369600}{24} = 15400$. Equivalently, the group of the lowest-numbered object is completed in ${}^{11}C_{2} = 55$ ways, then ${}^{8}C_{2} = 28$, then ${}^{5}C_{2} = 10$: $55 \times 28 \times 10 = 15400$.",
  "Dividing by the factorial of the group size instead of the number of groups.",
  "U04-C-groups-unlabelled", "Labelled count followed by the correct symmetry factor.",
  check=lambda: _partitions_with_sizes(12, [3, 3, 3, 3]), values=[15400, 369600, 61600, 220], cognitive="Application")

# ---------------------------------------------------------------- 030
def _c030():
    return Integer(sum(1 for a in it_.product(range(4), repeat=4) if len(set(a)) == 3))
q("U04-C-030", "Distribution and integer solutions", "Exactly one empty box", "Medium", "Multi-step computation MCQ",
  r"The number of ways of placing $4$ distinct balls in $4$ distinct boxes so that exactly one box remains empty is",
  r"$144$",
  [(r"$324$", r"Chooses the empty box ($4$ ways) and then places the balls freely in the other three ($3^4 = 81$), allowing further empty boxes: $4 \times 81 = 324$."),
   (r"$36$", r"Counts the placements in $3$ chosen boxes with none empty but forgets to choose which box is empty."),
   (r"$232$", r"Counts placements with at least one empty box: $4^4 - 4! = 256 - 24 = 232$.")],
  r"Choose the empty box in $4$ ways. The $4$ balls must then fill the other $3$ boxes with none empty, so the sizes are $2, 1, 1$: choose the pair in ${}^{4}C_{2} = 6$ ways and arrange the three parts in the three boxes in $3! = 6$ ways, giving $36$. Total $= 4 \times 36 = 144$.",
  "Reading 'exactly one empty' as 'at least one empty'.",
  "U04-C-distinct-onto", "Choice of empty box combined with an onto distribution.",
  check=_c030, values=[144, 324, 36, 232], cognitive="Analysis")

# ---------------------------------------------------------------- 031
def _c031():
    c = 0
    for s in it_.combinations(range(1, 21), 4):
        if s[0] == 1 and all(s[i + 1] - s[i] > 1 for i in range(3)):
            c += 1
    return Integer(c)
q("U04-C-031", "Selections with restrictions", "Non-consecutive selection with a fixed element", "Medium", "Multi-step computation MCQ",
  r"A coach chooses $4$ training days from the days numbered $1, 2, \ldots, 20$ of a month so that day $1$ is one of the chosen days and no two chosen days are consecutive. The number of possible choices is",
  r"$560$",
  [(r"$680$", r"After fixing day $1$, chooses the other $3$ non-consecutive days from days $2$ to $20$, forgetting that day $2$ is now excluded: ${}^{19 - 2}C_{3} = {}^{17}C_{3} = 680$."),
   (r"$455$", r"Reduces correctly to $3$ non-consecutive days from the $18$ days $3$ to $20$ but uses ${}^{n - r}C_{r} = {}^{15}C_{3} = 455$."),
   (r"$2380$", r"Ignores the condition on day $1$ and counts all non-consecutive choices: ${}^{17}C_{4} = 2380$.")],
  r"Since day $1$ is chosen, day $2$ cannot be, so the other $3$ days are chosen from days $3, 4, \ldots, 20$ ($18$ days) with no two consecutive. For $d_1 < d_2 < d_3$ from these, put $e_i = d_i - (i - 1)$; then $3 \le e_1 < e_2 < e_3 \le 18$, a one-to-one correspondence with $3$-subsets of $16$ days. Hence the count is ${}^{16}C_{3} = 560$.",
  "Forgetting that a fixed chosen element also removes its neighbour, or using an off-by-one non-consecutive formula.",
  "U04-C-nonconsecutive-fixed", "Two ideas: the fixed element removes its neighbour, then the non-consecutive bijection on the reduced range.",
  check=_c031, values=[560, 680, 455, 2380], cognitive="Analysis",
  numerical=dict(question=r"A coach chooses $4$ training days from the days numbered $1, 2, \ldots, 20$ of a month so that day $1$ is one of the chosen days and no two chosen days are consecutive. The number of possible choices is", answer=560))

# ---------------------------------------------------------------- 032
def _c032():
    s1 = _nsol(9, 4, [1] * 4) == 56
    s2 = _partitions_with_sizes(4, [2, 2]) == 6
    return (bool(s1), bool(s2))
_d032, _v032 = _st(ST[2], {
    ST[0]: r"Accepts Statement II by using the labelled count ${}^{4}C_{2} = 6$ without dividing by $2!$.",
    ST[1]: r"Rejects Statement I by using the non-negative formula ${}^{12}C_{3} = 220$.",
    ST[3]: r"Rejects Statement I with the non-negative formula and accepts Statement II with the labelled count."})
q("U04-C-032", "Distribution and integer solutions", "Identical and distinct distributions compared", "Medium", "Statement-based MCQ",
  r"Statement I: The number of ways of distributing $9$ identical balls into $4$ distinct boxes so that no box is empty is $56$. Statement II: The number of ways of dividing $4$ distinct balls into two groups of $2$ balls each (the groups not distinguished) is $6$. In the light of the above statements, choose the correct answer.",
  ST[2], _d032,
  r"Statement I: the count is the number of positive solutions of $x_1 + x_2 + x_3 + x_4 = 9$, which is ${}^{8}C_{3} = 56$, so it is true. Statement II: choosing $2$ balls in ${}^{4}C_{2} = 6$ ways counts each split twice (the chosen pair and its complement give the same split), so the number is $\frac{6}{2} = 3$; the statement is false.",
  "Forgetting to divide by $2!$ when two equal groups are unlabelled.",
  "U04-C-statement-distribution", "Two separate counts, each with a typical trap.",
  check=_c032, values=_v032, cognitive="Analysis")

# ---------------------------------------------------------------- 033
def _c033():
    s1 = _nsol(6, 3) == _nsol(8, 3, [1] * 3)
    s2 = _nsol(15, 3, [3, 4, 5]) == 10
    return (bool(s1), bool(s2))
_d033, _v033 = _st(ST[3], {
    ST[0]: r"Accepts Statement I by using ${}^{8}C_{2} = 28$ instead of ${}^{7}C_{2}$ for the positive count of $x + y + z = 8$.",
    ST[1]: r"Rejects Statement I correctly but rejects Statement II by counting positive solutions after the shift: ${}^{2}C_{2} = 1$ instead of ${}^{5}C_{2} = 10$.",
    ST[2]: r"Accepts Statement I by using ${}^{8}C_{2} = 28$ for the positive count, and rejects Statement II by counting positive solutions of $x' + y' + z' = 3$, getting ${}^{2}C_{2} = 1$."})
q("U04-C-033", "Distribution and integer solutions", "Comparing stars and bars counts", "Medium", "Statement-based MCQ",
  r"Statement I: The number of non-negative integral solutions of $x + y + z = 6$ is equal to the number of positive integral solutions of $x + y + z = 8$. Statement II: The number of integral solutions of $x + y + z = 15$ with $x \ge 3$, $y \ge 4$ and $z \ge 5$ is $10$. In the light of the above statements, choose the correct answer.",
  ST[3], _d033,
  r"Statement I: non-negative solutions of $x + y + z = 6$ number ${}^{8}C_{2} = 28$, while positive solutions of $x + y + z = 8$ number ${}^{7}C_{2} = 21$; so it is false. (Equality would need total $9$ on the right.) Statement II: put $x = x' + 3$, $y = y' + 4$, $z = z' + 5$ with $x', y', z' \ge 0$; then $x' + y' + z' = 15 - 12 = 3$, which has ${}^{5}C_{2} = 10$ solutions; true.",
  "Off-by-one errors when converting between positive and non-negative solutions.",
  "U04-C-statement-stars-bars", "Two independent conversions, each prone to an off-by-one error.",
  check=_c033, values=_v033, cognitive="Analysis")

# ---------------------------------------------------------------- 034
def _c034():
    c = 0
    for p in it_.permutations(range(9), 4):
        g = [i for i, x in enumerate(p) if x >= 5]
        if len(g) == 2 and g[1] - g[0] == 1:
            c += 1
    return Integer(c)
q("U04-C-034", "Selection and arrangement", "Select then arrange with a block", "Medium", "Multi-step computation MCQ",
  r"From $5$ boys and $4$ girls, $2$ boys and $2$ girls are selected and arranged in a row so that the two selected girls stand next to each other. The number of ways of doing this is",
  r"$720$",
  [(r"$1440$", r"Ignores the adjacency condition: ${}^{5}C_{2} \times {}^{4}C_{2} \times 4! = 60 \times 24 = 1440$."),
   (r"$360$", r"Treats the girls as a block but does not arrange the two girls within it: $60 \times 3! = 360$."),
   (r"$60$", r"Counts only the selections ${}^{5}C_{2} \times {}^{4}C_{2} = 60$.")],
  r"The selection can be made in ${}^{5}C_{2} \times {}^{4}C_{2} = 10 \times 6 = 60$ ways. Treat the two girls as one block: the block and the two boys are arranged in $3! = 6$ ways, and the girls inside the block in $2! = 2$ ways. Total $= 60 \times 6 \times 2 = 720$.",
  "Forgetting the internal arrangement of the block.",
  "U04-C-select-arrange-block", "Selection combined with the block method.",
  check=_c034, values=[720, 1440, 360, 60], cognitive="Application")

# ---------------------------------------------------------------- 035
def _c035():
    return Integer(sum(1 for a in it_.product(range(3), repeat=5) if a.count(0) == 2))
q("U04-C-035", "Distribution and integer solutions", "Distribution with an exact share", "Medium", "Multi-step computation MCQ",
  r"Five distinct prizes are to be given to three students $P$, $Q$ and $R$, a student being allowed to receive any number of prizes (including none). The number of ways in which $P$ receives exactly $2$ prizes is",
  r"$80$",
  [(r"$270$", r"After giving $2$ prizes to $P$, lets the other $3$ prizes go to any of the three students: $10 \times 3^3 = 270$."),
   (r"$10$", r"Counts only the choice of $P$'s two prizes, ${}^{5}C_{2} = 10$."),
   (r"$240$", r"Multiplies $80$ by $3$, as if one also had to choose which student receives exactly two prizes.")],
  r"Choose $P$'s two prizes in ${}^{5}C_{2} = 10$ ways. Each of the remaining $3$ prizes must go to $Q$ or $R$ (not to $P$, otherwise $P$ would get more than $2$), giving $2^3 = 8$ ways. Total $= 10 \times 8 = 80$.",
  "Allowing the remaining prizes to go to $P$ as well.",
  "U04-C-distinct-into-boxes", "Selection followed by a restricted free distribution.",
  check=_c035, values=[80, 270, 10, 240], cognitive="Application")

# ---------------------------------------------------------------- 036
def _c036():
    return Integer(sum(1 for t in it_.product(range(13), repeat=3) if sum(t) == 12 and t[0] % 2 == 0))
q("U04-C-036", "Distribution and integer solutions", "Solutions with one even variable", "Medium", "Multi-step computation MCQ",
  r"The number of non-negative integral solutions of $x + y + z = 12$ in which $x$ is even is",
  r"$49$",
  [(r"$91$", r"Ignores the parity condition: ${}^{14}C_{2} = 91$."),
   (r"$36$", r"Treats $0$ as not even, summing only over $x = 2, 4, \ldots, 12$: $11 + 9 + 7 + 5 + 3 + 1 = 36$."),
   (r"$25$", r"Takes $x = 2, 4, \ldots, 10$ and makes $y, z$ positive: $9 + 7 + 5 + 3 + 1 = 25$.")],
  r"For $x = 2k$ ($k = 0, 1, \ldots, 6$), $y + z = 12 - 2k$ has $13 - 2k$ non-negative solutions. Summing, $13 + 11 + 9 + 7 + 5 + 3 + 1 = 49$.",
  "Leaving out $x = 0$ as an even value.",
  "U04-C-stars-bars-parity", "Casework over one variable with a stars and bars count in each case.",
  check=_c036, values=[49, 91, 36, 25], cognitive="Application",
  numerical=dict(question=r"The number of non-negative integral solutions of $x + y + z = 12$ in which $x$ is even is", answer=49))

# ---------------------------------------------------------------- 037
def _c037():
    p2 = sum(1 for b in multiset_partitions(list(range(6)), 2))
    s1 = p2 == 62
    s2 = _nsol(6, 2, [1, 1]) == 6
    return (bool(s1), bool(s2))
_d037, _v037 = _st(ST[1], {
    ST[0]: r"Accepts Statement I using the labelled count $2^6 - 2 = 62$, and accepts Statement II by letting the first child's share run over $1, 2, \ldots, 6$, forgetting that the second child then gets none.",
    ST[2]: r"Accepts Statement I, forgetting that unlabelled piles halve the labelled count $62$.",
    ST[3]: r"Accepts Statement II by miscounting $x + y = 6$ with $x, y \ge 1$ as $6$ instead of ${}^{5}C_{1} = 5$."})
q("U04-C-037", "Division into groups", "Two non-empty piles", "Medium", "Statement-based MCQ",
  r"Statement I: The number of ways of dividing $6$ distinct books into two non-empty piles (the piles not distinguished from each other) is $62$. Statement II: The number of ways of distributing $6$ identical books between $2$ children so that each child gets at least one book is $6$. In the light of the above statements, choose the correct answer.",
  ST[1], _d037,
  r"Statement I: into two labelled piles the books go in $2^6 = 64$ ways, of which $2$ leave a pile empty, giving $62$; since the piles are not distinguished, each division is counted twice, so the answer is $31$. False. Statement II: $x + y = 6$ with $x, y \ge 1$ has ${}^{5}C_{1} = 5$ solutions. False.",
  "Forgetting to halve for unlabelled piles; off-by-one in a two-variable count.",
  "U04-C-statement-distribution", "Two traps, labelled versus unlabelled and positive versus non-negative.",
  check=_c037, values=_v037, cognitive="Analysis")

# ---------------------------------------------------------------- 038
def _c038():
    # a, b, c: Rs 1, Rs 2, Rs 5 coins (unlimited); d: Rs 10 coins (only 2 available)
    return _nsol(8, 4, [0] * 4, [8, 8, 8, 2])
q("U04-C-038", "Distribution and integer solutions", "Selection with repetition and a limited supply", "Medium", "Multi-step computation MCQ",
  r"A child picks $8$ coins from a box that has an unlimited supply of $\text{Rs}\ 1$, $\text{Rs}\ 2$ and $\text{Rs}\ 5$ coins but only two $\text{Rs}\ 10$ coins. Coins of the same denomination are identical and only the collection matters. The number of different collections the child can pick is",
  r"$109$",
  [(r"$165$", r"Ignores the limited supply of $\text{Rs}\ 10$ coins: ${}^{8+3}C_{3} = {}^{11}C_{3} = 165$."),
   (r"$81$", r"Removes collections with at least two $\text{Rs}\ 10$ coins instead of at least three: $165 - {}^{9}C_{3} = 165 - 84 = 81$."),
   (r"$45$", r"Leaves the $\text{Rs}\ 10$ coins out altogether: ${}^{8+2}C_{2} = {}^{10}C_{2} = 45$.")],
  r"Let $a, b, c, d$ be the numbers of $\text{Rs}\ 1$, $\text{Rs}\ 2$, $\text{Rs}\ 5$ and $\text{Rs}\ 10$ coins, so $a + b + c + d = 8$ with all non-negative and $d \le 2$. For $d = 0, 1, 2$ the remaining $a + b + c = 8 - d$ has ${}^{10}C_{2} = 45$, ${}^{9}C_{2} = 36$ and ${}^{8}C_{2} = 28$ solutions. Total $= 45 + 36 + 28 = 109$ (equivalently ${}^{11}C_{3} - {}^{8}C_{3} = 165 - 56 = 109$).",
  "Forgetting a supply limit, or shifting the excluded case by the wrong amount.",
  "U04-C-selection-limited-supply", "Modelling a selection with repetition as stars and bars, then handling an upper limit on one variable.",
  check=_c038, values=[109, 165, 81, 45], cognitive="Application",
  numerical=dict(question=r"A child picks $8$ coins from a box that has an unlimited supply of $\text{Rs}\ 1$, $\text{Rs}\ 2$ and $\text{Rs}\ 5$ coins but only two $\text{Rs}\ 10$ coins. Coins of the same denomination are identical and only the collection matters. The number of different collections the child can pick is", answer=109))

# ---------------------------------------------------------------- 039
def _c039():
    return Integer(sum(1 for p in it_.permutations(range(7), 3) if not (0 in p and 1 in p)))
q("U04-C-039", "Selection and arrangement", "Complement for ordered posts", "Medium", "Multi-step computation MCQ",
  r"A president, a vice-president and a secretary, all different persons, are to be chosen from $7$ members of a club that include two members $P$ and $Q$. If $P$ and $Q$ are not to be chosen together, the number of ways of choosing the three office bearers is",
  r"$180$",
  [(r"$205$", r"Subtracts only the $5$ selections containing both $P$ and $Q$, not their $30$ arrangements: $210 - 5 = 205$."),
   (r"$210$", r"Ignores the restriction: ${}^{7}P_{3} = 210$."),
   (r"$150$", r"Counts the bad cases as $2 \times 5 \times 3! = 60$, treating the order of $P$ and $Q$ as an extra factor: $210 - 60 = 150$.")],
  r"Without restriction there are ${}^{7}P_{3} = 210$ ways. If both $P$ and $Q$ are chosen, the third person can be chosen from the other $5$ in $5$ ways and the three persons assigned to the three posts in $3! = 6$ ways, giving $30$. Hence the answer is $210 - 30 = 180$.",
  "Subtracting selections from arrangements.",
  "U04-C-complement-select-arrange", "Complement where the bad case needs its own selection and arrangement.",
  check=_c039, values=[180, 205, 210, 150], cognitive="Application")

# ---------------------------------------------------------------- 040
q("U04-C-040", "Distribution and integer solutions", "Solutions with negative lower bounds", "Medium", "Multi-step computation MCQ",
  r"The number of integral solutions of $x + y + z = 5$ with $x \ge -2$, $y \ge -1$ and $z \ge 0$ is",
  r"$45$",
  [(r"$21$", r"Ignores the negative lower bounds and counts non-negative solutions: ${}^{7}C_{2} = 21$."),
   (r"$6$", r"Shifts in the wrong direction, reducing the total to $5 - 3 = 2$: ${}^{4}C_{2} = 6$."),
   (r"$36$", r"Shifts only $x$, getting a total of $7$: ${}^{9}C_{2} = 36$.")],
  r"Put $x = x' - 2$, $y = y' - 1$ with $x', y' \ge 0$. Then $x' + y' + z = 5 + 2 + 1 = 8$ in non-negative integers, which has ${}^{8+2}C_{2} = {}^{10}C_{2} = 45$ solutions.",
  "Shifting the total the wrong way for negative lower bounds.",
  "U04-C-stars-bars-bounds", "Shift with negative bounds, a less familiar direction of substitution.",
  check=lambda: _nsol(5, 3, [-2, -1, 0]), values=[45, 21, 6, 36], cognitive="Application")

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 041
q("U04-C-041", "Selection and arrangement", "Words from a word with a tripled letter", "Difficult", "Multi-step computation MCQ",
  r"The number of four-letter words (meaningful or not) that can be formed using the letters of the word PROPORTION, each letter being used at most as many times as it appears in PROPORTION, is",
  r"$758$",
  [(r"$360$", r"Counts only words with four different letters, ${}^{6}P_{4} = 360$."),
   (r"$738$", r"Misses the case of three O's with one other letter ($5 \times 4 = 20$ words)."),
   (r"$740$", r"Misses the case of two pairs ($3 \times \frac{4!}{2!\,2!} = 18$ words).")],
  r"The letters are O (three times), P and R (twice each), T, I, N (once each): $6$ distinct letters. All different: ${}^{6}P_{4} = 360$. One pair and two different: $3 \times {}^{5}C_{2} \times \frac{4!}{2!} = 3 \times 10 \times 12 = 360$. Two pairs: ${}^{3}C_{2} \times \frac{4!}{2!\,2!} = 18$. Three alike (O) and one other: $5 \times \frac{4!}{3!} = 20$. Total $= 360 + 360 + 18 + 20 = 758$.",
  "Missing a pattern case (two pairs or a triple) in multiset word counting.",
  "U04-C-words-from-multiset", "Four-case analysis, each case a selection followed by an arrangement with repetitions.",
  check=lambda: Integer(len(set(it_.permutations("PROPORTION", 4)))), values=[758, 360, 738, 740], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c042():
    return Integer(sum(1 for a in it_.product(range(3), repeat=6) if all(1 <= a.count(b) <= 3 for b in range(3))))
q("U04-C-042", "Distribution and integer solutions", "Distinct objects with lower and upper bounds", "Difficult", "Multi-step computation MCQ",
  r"Six distinct balls are placed in three distinct boxes so that every box receives at least one ball and no box receives more than three balls. The number of ways of doing this is",
  r"$450$",
  [(r"$540$", r"Ignores the upper bound and counts all placements with no box empty: $3^6 - 3 \cdot 2^6 + 3 = 540$."),
   (r"$360$", r"Considers only the split $(3, 2, 1)$ and misses $(2, 2, 2)$."),
   (r"$75$", r"Counts the unlabelled divisions $60 + 15 = 75$ and does not assign the groups to the distinct boxes.")],
  r"The allowed box sizes are $(3,2,1)$ in some order and $(2,2,2)$. For $(3,2,1)$: $\frac{6!}{3!\,2!\,1!} = 60$ divisions and $3! = 6$ ways to assign the sizes to boxes, giving $360$. For $(2,2,2)$: $\frac{6!}{2!\,2!\,2!} = 90$ labelled placements. Total $= 360 + 90 = 450$. (The excluded split $(4,1,1)$ accounts for the $90$ difference from $540$.)",
  "Forgetting a size pattern, or forgetting that the boxes are distinct.",
  "U04-C-distinct-onto", "Enumerating size patterns under two bounds, with labelled assignment.",
  check=_c042, values=[450, 540, 360, 75], cognitive="Analysis",
  numerical=dict(question=r"Six distinct balls are placed in three distinct boxes so that every box receives at least one ball and no box receives more than three balls. The number of ways of doing this is", answer=450))

# ---------------------------------------------------------------- 043
q("U04-C-043", "Distribution and integer solutions", "Upper bounds with overlapping excess", "Difficult", "Multi-step computation MCQ",
  r"The number of ways of distributing $20$ identical sweets among $3$ children so that no child gets more than $9$ sweets is",
  r"$36$",
  [(r"$33$", r"Subtracts $3 \times 66 = 198$ from $231$ but forgets to add back the $3$ cases where two children each get at least $10$."),
   (r"$30$", r"Subtracts the $3$ overlap cases instead of adding them back: $231 - 198 - 3 = 30$."),
   (r"$39$", r"Adds back $6$ overlap cases, counting each pair of children twice: $231 - 198 + 6 = 39$.")],
  r"Without the bound there are ${}^{22}C_{2} = 231$ ways. If a particular child gets at least $10$, the rest is ${}^{12}C_{2} = 66$ ways, so $3 \times 66 = 198$ to remove. If two particular children each get at least $10$, they get exactly $10$ each and the third gets $0$: $1$ way for each of the $3$ pairs, which were removed twice, so add $3$. Answer $= 231 - 198 + 3 = 36$.",
  "Missing the overlap term when subtracting excess cases.",
  "U04-C-stars-bars-upper", "Complement with a non-empty pairwise overlap; easy to miss or mis-sign.",
  check=lambda: _nsol(20, 3, [0] * 3, [9] * 3), values=[36, 33, 30, 39], cognitive="Analysis",
  numerical=dict(question=r"The number of ways of distributing $20$ identical sweets among $3$ children so that no child gets more than $9$ sweets is", answer=36))

# ---------------------------------------------------------------- 044
def _c044():
    c = 0
    for a in it_.product(range(3), repeat=10):
        if sorted(_Counter(a).values()) == [3, 3, 4] and a[0] == a[1]:
            c += 1
    return Integer(c)
q("U04-C-044", "Division into groups", "Labelled unequal groups with a togetherness condition", "Difficult", "Multi-step computation MCQ",
  r"Ten distinct students, including $P$ and $Q$, are divided into three teams, two of $3$ students and one of $4$ students, and the three teams are assigned to three different laboratories (one team per laboratory; any laboratory may get the team of $4$). The number of ways of doing this so that $P$ and $Q$ are in the same team is",
  r"$3360$",
  [(r"$1120$", r"Fixes in advance which laboratory gets the team of $4$, missing the factor $3$."),
   (r"$1680$", r"Counts only the case where $P$ and $Q$ are in the team of $4$: $3 \times 560 = 1680$."),
   (r"$12600$", r"Ignores the condition on $P$ and $Q$: $3 \times \frac{10!}{3!\,3!\,4!} = 12600$.")],
  r"First fix which laboratory gets $4$ students ($3$ ways). With sizes now fixed: if $P, Q$ are in the team of $4$, choose $2$ more from $8$ ($28$) and split the other $6$ into the two labelled teams of $3$ ($20$), giving $560$; if $P, Q$ are in a team of $3$ ($2$ choices of that team), choose $1$ more ($8$) and split the other $7$ into $3$ and $4$ ($35$), giving $2 \times 280 = 560$. So each size assignment gives $1120$, and the total is $3 \times 1120 = 3360$.",
  "Missing a case for where the pair can go, or fixing the team sizes to laboratories.",
  "U04-C-groups-labelled", "Labelled groups of unequal sizes with casework on a pair; several factors to track.",
  check=_c044, values=[3360, 1120, 1680, 12600], cognitive="Analysis")

# ---------------------------------------------------------------- 045
def _c045():
    return Integer(sum(1 for p in multiset_partitions(list(range(7)), 3) if any(len(b) == 3 for b in p)))
q("U04-C-045", "Division into groups", "Distinct objects into identical boxes with a size condition", "Difficult", "Multi-step computation MCQ",
  r"Seven distinct balls are placed in $3$ identical boxes so that no box is empty and at least one box contains exactly $3$ balls. The number of ways of doing this is",
  r"$175$",
  [(r"$350$", r"Forgets to divide by $2!$ for the two equal groups in both splits: $140 + 210 = 350$."),
   (r"$301$", r"Ignores the condition on a box of $3$ and counts every split into $3$ non-empty groups: $21 + 105 + 70 + 105 = 301$."),
   (r"$245$", r"Divides by $2!$ for the split $(3, 2, 2)$ but not for $(3, 3, 1)$: $140 + 105 = 245$.")],
  r"Identical boxes mean we only divide the balls into $3$ non-empty unlabelled groups, one of which has exactly $3$ balls. The possible splits are $(3,3,1)$ and $(3,2,2)$. Split $(3,3,1)$: $\frac{7!}{3!\,3!\,1!\,2!} = 70$. Split $(3,2,2)$: $\frac{7!}{3!\,2!\,2!\,2!} = 105$. Total $= 70 + 105 = 175$.",
  "Missing the symmetry factor for equal-sized groups in one of the cases, or not restricting the splits.",
  "U04-C-identical-boxes-condition", "Listing the admissible splits under a size condition, each with its own symmetry correction.",
  check=_c045, values=[175, 350, 301, 245], cognitive="Analysis",
  numerical=dict(question=r"Seven distinct balls are placed in $3$ identical boxes so that no box is empty and at least one box contains exactly $3$ balls. The number of ways of doing this is", answer=175))

# ---------------------------------------------------------------- 046
def _c046():
    return Integer(sum(1 for s in it_.combinations(range(1, 13), 4) if all(s[i + 1] - s[i] >= 3 for i in range(3))))
q("U04-C-046", "Distribution and integer solutions", "Selections with a minimum spacing", "Difficult", "Multi-step computation MCQ",
  r"Four of the squares in a row of $12$ squares, numbered $1$ to $12$, are to be shaded so that between any two shaded squares there are at least two unshaded squares. The number of ways of choosing the squares to shade is",
  r"$15$",
  [(r"$126$", r"Requires only one unshaded square between shaded ones: ${}^{12 - 3}C_{4} = {}^{9}C_{4} = 126$."),
   (r"$5$", r"Removes $2$ squares for each of the $4$ shaded squares instead of each of the $3$ gaps: ${}^{12 - 8 + 1}C_{4} = {}^{5}C_{4} = 5$."),
   (r"$35$", r"Uses ${}^{12 - 2 \cdot 3 + 1}C_{4} = {}^{7}C_{4} = 35$, adding $1$ to the top entry.")],
  r"Let the shaded squares be $a_1 < a_2 < a_3 < a_4$ with $a_{i+1} - a_i \ge 3$. Put $b_i = a_i - 2(i - 1)$; then $1 \le b_1 < b_2 < b_3 < b_4 \le 12 - 6 = 6$, and the map is one-to-one. Hence the count is ${}^{6}C_{4} = 15$. Equivalently, the $8$ unshaded squares give $x_0 + x_1 + \cdots + x_4 = 8$ with $x_1, x_2, x_3 \ge 2$, whose count is ${}^{2+4}C_{4} = 15$.",
  "Applying the 'no two consecutive' formula without adjusting for the larger gap.",
  "U04-C-nonconsecutive", "Requires a shifting bijection or a stars and bars model with interior minima.",
  check=_c046, values=[15, 126, 5, 35], cognitive="Analysis",
  numerical=dict(question=r"Four of the squares in a row of $12$ squares, numbered $1$ to $12$, are to be shaded so that between any two shaded squares there are at least two unshaded squares. The number of ways of choosing the squares to shade is", answer=15))

# ---------------------------------------------------------------- 047
def _c047():
    return Integer(sum(1 for n in range(1000, 10000) if sum(int(d) for d in str(n)) == 10))
q("U04-C-047", "Distribution and integer solutions", "Digit sums as integer solutions", "Difficult", "Multi-step computation MCQ",
  r"The number of four-digit natural numbers whose digits add up to $10$ is",
  r"$219$",
  [(r"$220$", r"Handles the leading digit by $d_1 - 1 \ge 0$ but forgets that $d_1 - 1 = 9$ would make $d_1 = 10$, which is not a digit."),
   (r"$286$", r"Allows a leading zero and ignores the digit cap: ${}^{13}C_{3} = 286$."),
   (r"$282$", r"Applies the digit cap but allows a leading zero: $286 - 4 = 282$.")],
  r"Let the digits be $d_1 d_2 d_3 d_4$ with $d_1 \ge 1$. Put $d_1 = e + 1$; then $e + d_2 + d_3 + d_4 = 9$ with all variables non-negative, giving ${}^{12}C_{3} = 220$ solutions. Here $d_2, d_3, d_4 \le 9$ automatically, but $e = 9$ gives $d_1 = 10$, which is invalid; this happens in exactly $1$ solution. Hence the answer is $220 - 1 = 219$.",
  "Forgetting the digit cap on the leading digit after the shift.",
  "U04-C-digit-sum-stars-bars", "Combines a leading-digit shift with an upper-bound correction that is easy to miss.",
  check=_c047, values=[219, 220, 286, 282], cognitive="Analysis",
  numerical=dict(question=r"The number of four-digit natural numbers whose digits add up to $10$ is", answer=219))

# ---------------------------------------------------------------- 048
def _c048():
    return Integer(sum(1 for a in it_.product(range(3), repeat=8) if all(a.count(b) >= 2 for b in range(3))))
q("U04-C-048", "Division into groups", "Distinct objects with a minimum per person", "Difficult", "Multi-step computation MCQ",
  r"The number of ways of distributing $8$ distinct toys among $3$ children so that each child gets at least $2$ toys is",
  r"$2940$",
  [(r"$1680$", r"Considers only the split $(3, 3, 2)$ and misses $(4, 2, 2)$."),
   (r"$490$", r"Counts unlabelled divisions $210 + 280 = 490$ and does not hand them to the distinct children."),
   (r"$5880$", r"Multiplies each case by $3!$ instead of $3$, ignoring the two equal shares: $6 \times (420 + 560)$.")],
  r"The possible shares are $(4,2,2)$ and $(3,3,2)$ in some order. For $(4,2,2)$: choose the child with $4$ toys ($3$ ways), then $\frac{8!}{4!\,2!\,2!} = 420$, giving $1260$. For $(3,3,2)$: choose the child with $2$ toys ($3$ ways), then $\frac{8!}{3!\,3!\,2!} = 560$, giving $1680$. Total $= 1260 + 1680 = 2940$.",
  "Over-assigning when two shares are equal, or missing a share pattern.",
  "U04-C-distinct-min-share", "Enumerating share patterns and handling equal shares in the labelling factor.",
  check=_c048, values=[2940, 1680, 490, 5880], cognitive="Analysis")

# ---------------------------------------------------------------- 049
def _c049():
    c = 0
    for p in it_.permutations(range(11), 6):
        b = sum(1 for x in p if x < 6)
        if b == 3 and all(not (p[i] >= 6 and p[i + 1] >= 6) for i in range(5)):
            c += 1
    return Integer(c)
q("U04-C-049", "Selection and arrangement", "Select then arrange with the gap method", "Difficult", "Multi-step computation MCQ",
  r"From $6$ boys and $5$ girls, $3$ boys and $3$ girls are selected and then arranged in a row so that no two girls are adjacent. The number of ways of doing this is",
  r"$28800$",
  [(r"$144000$", r"Ignores the adjacency condition: $200 \times 6! = 144000$."),
   (r"$14400$", r"Allows only strictly alternating rows (two patterns): $200 \times 3! \times 3! \times 2 = 14400$."),
   (r"$4800$", r"Chooses the gaps ${}^{4}C_{3} = 4$ but does not arrange the girls in them: $200 \times 3! \times 4 = 4800$.")],
  r"Select in ${}^{6}C_{3} \times {}^{5}C_{3} = 20 \times 10 = 200$ ways. Arrange the $3$ boys in $3! = 6$ ways; they create $4$ gaps, and the $3$ girls occupy $3$ different gaps in ${}^{4}P_{3} = 24$ ways. Total $= 200 \times 6 \times 24 = 28800$.",
  "Equating 'no two girls adjacent' with strict alternation.",
  "U04-C-select-arrange-gap", "Selection combined with the gap method; the alternation trap is tempting.",
  check=_c049, values=[28800, 144000, 14400, 4800], cognitive="Analysis")

# ---------------------------------------------------------------- 050
def _c050():
    s1 = sum(1 for a in it_.product(range(2), repeat=10) if 2 <= sum(a) <= 8) == 1002
    s2 = sum(1 for a in it_.product(range(3), repeat=9) if all(a.count(b) == 3 for b in range(3))) == 1680
    return (bool(s1), bool(s2))
_d050, _v050 = _st(ST[0], {
    ST[1]: r"Rejects Statement I by removing only the $2$ cases with an empty box ($1022$), and rejects Statement II by dividing $1680$ by $3!$.",
    ST[2]: r"Rejects Statement II by dividing $\frac{9!}{(3!)^3} = 1680$ by $3!$, treating the persons as identical.",
    ST[3]: r"Rejects Statement I by removing only the cases with an empty box, getting $1022$."})
q("U04-C-050", "Division into groups", "Distribution counts with bounds and equal groups", "Difficult", "Statement-based MCQ",
  r"Statement I: The number of ways of placing $10$ distinct balls in $2$ distinct boxes so that each box gets at least $2$ balls is $1002$. Statement II: The number of ways of dividing $9$ distinct objects into three groups of $3$ and giving one group to each of $3$ different persons is $1680$. In the light of the above statements, choose the correct answer.",
  ST[0], _d050,
  r"Statement I: of the $2^{10} = 1024$ placements, a box gets $0$ balls in $2$ placements and exactly $1$ ball in $2 \times 10 = 20$ placements; these $22$ are disjoint since $10 > 2$. So the count is $1024 - 22 = 1002$; true. Statement II: the first person's group in ${}^{9}C_{3} = 84$ ways and the second's in ${}^{6}C_{3} = 20$ ways, giving $84 \times 20 = 1680 = \frac{9!}{(3!)^3}$; true.",
  "Removing only the empty-box cases, or dividing by $3!$ when the recipients are distinct.",
  "U04-C-statement-distribution", "Two separate multi-step counts, each with a plausible trap.",
  check=_c050, values=_v050, cognitive="Analysis")

# ---------------------------------------------------------------- 051
def _c051():
    return Integer(sum(1 for s in it_.product(range(10), repeat=4) if 0 in s and 9 in s))
q("U04-C-051", "Permutations with restrictions", "Complement with two conditions", "Difficult", "Multi-step computation MCQ",
  r"A four-digit PIN is any string of $4$ digits from $0000$ to $9999$. The number of PINs that contain at least one digit $0$ and at least one digit $9$ is",
  r"$974$",
  [(r"$1200$", r"Places a $0$ and a $9$ in two chosen positions (${}^{4}P_{2} = 12$) and fills the rest freely ($10^2$), counting many PINs more than once."),
   (r"$3439$", r"Counts only PINs with at least one $0$: $10^4 - 9^4 = 3439$."),
   (r"$5904$", r"Removes only PINs with neither $0$ nor $9$: $10^4 - 8^4 = 5904$.")],
  r"Let $U = 10^4 = 10000$. PINs with no $0$: $9^4 = 6561$; with no $9$: $6561$; with neither: $8^4 = 4096$. PINs missing $0$ or $9$ number $6561 + 6561 - 4096 = 9026$. Hence the required count is $10000 - 9026 = 974$.",
  "Fixing positions for the required digits, which overcounts.",
  "U04-C-complement-two-conditions", "Complement over a union of two events with an overlap term.",
  check=_c051, values=[974, 1200, 3439, 5904], cognitive="Analysis",
  numerical=dict(question=r"A four-digit PIN is any string of $4$ digits from $0000$ to $9999$. The number of PINs that contain at least one digit $0$ and at least one digit $9$ is", answer=974))

# ---------------------------------------------------------------- 052
def _c052():
    # persons 0..9, couple k = {2k, 2k+1}
    return Integer(sum(1 for p in it_.permutations(range(10), 3) if len({x // 2 for x in p}) == 3))
q("U04-C-052", "Selection and arrangement", "Select then arrange avoiding pairs", "Difficult", "Multi-step computation MCQ",
  r"From $5$ married couples, $3$ persons are selected and seated in a row of $3$ chairs so that no husband and his wife are both among the selected persons. The number of ways of doing this is",
  r"$480$",
  [(r"$720$", r"Ignores the restriction: ${}^{10}P_{3} = 720$."),
   (r"$80$", r"Counts the valid selections ${}^{5}C_{3} \times 2^3 = 80$ but does not seat them."),
   (r"$680$", r"Removes only the $5 \times 8 = 40$ selections containing a couple from the $720$ seatings, mixing selections with arrangements.")],
  r"Choose the $3$ couples that are represented in ${}^{5}C_{3} = 10$ ways, and one spouse from each in $2^3 = 8$ ways, giving $80$ selections. Seat them in $3! = 6$ ways. Total $= 80 \times 6 = 480$. Check: seatings containing a couple number $5 \times 8 \times 3! = 240$, and $720 - 240 = 480$.",
  "Subtracting selections from arrangements in the complement.",
  "U04-C-select-arrange-avoid-pairs", "Two-level selection (couples, then spouse) followed by arrangement.",
  check=_c052, values=[480, 720, 80, 680], cognitive="Analysis")

# ---------------------------------------------------------------- 053
def _c053():
    configs = set()
    comps = [t for t in it_.product(range(6), repeat=4) if sum(t) == 5]
    for perm in it_.permutations(range(5)):
        for c in comps:
            out, k = [], 0
            for size in c:
                out.append(tuple(perm[k:k + size]))
                k += size
            configs.add(tuple(out))
    return Integer(len(configs))
q("U04-C-053", "Distribution and integer solutions", "Distinct objects in boxes where order matters", "Difficult", "Multi-step computation MCQ",
  r"Five distinct rings are to be worn on the $4$ fingers of one hand (thumb excluded). A finger may carry any number of rings, including none, and the order of the rings on a finger matters. The number of ways of wearing the rings is",
  r"$6720$",
  [(r"$1024$", r"Ignores the order of rings on a finger: $4^5 = 1024$."),
   (r"$56$", r"Treats the rings as identical: ${}^{5+3}C_{3} = 56$."),
   (r"$480$", r"Forces every finger to carry at least one ring: $5! \times {}^{4}C_{3} = 480$.")],
  r"Line up the $5$ distinct rings and $3$ identical separators (between the $4$ fingers) in a row. Each such row gives exactly one way of wearing the rings, in order, on fingers $1$ to $4$. The number of rows is $\frac{8!}{3!} = 6720$, which also equals $5! \times {}^{8}C_{3} = 120 \times 56$.",
  "Treating the placement as an independent choice of finger per ring, which loses the order.",
  "U04-C-ordered-distribution", "Requires combining stars and bars with an arrangement of distinct objects; non-standard model.",
  check=_c053, values=[6720, 1024, 56, 480], cognitive="Analysis")
