import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from itertools import product as iproduct, combinations, permutations
from sympy.utilities.iterables import multiset_permutations

R = Rational
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
T_CL = "Probability"
T_CD = "Conditional probability and independence"
DICE2 = list(iproduct(range(1, 7), repeat=2))


def QXI(*a, **kw):
    kw["source_class"] = "XI"
    return q(*a, **kw)


def QXII(*a, **kw):
    kw["source_class"] = "XII"
    return q(*a, **kw)


def frac(fav, tot):
    return R(len(fav), len(tot))


# ======================================================================== XI (classical, addition theorem)
# ---------------------------------------------------------------- 001
QXI("U13-C-001", T_CL, "Classical probability with two dice", "Easy", "Single-step computation MCQ",
  r"Two fair dice are thrown. The probability that the sum of the numbers obtained is a prime number is",
  r"$\frac{5}{12}$",
  [(r"$\frac{5}{11}$", r"Treats the $11$ possible sums $2, 3, \ldots, 12$ as equally likely; $5$ of them are prime, giving $\frac{5}{11}$."),
   (r"$\frac{7}{18}$", r"Leaves out the sum $2$ (thinking $2$ is not prime), counting $2+4+6+2 = 14$ outcomes, so $\frac{14}{36}$."),
   (r"$\frac{13}{36}$", r"Leaves out the two outcomes with sum $11$, counting $1+2+4+6 = 13$ outcomes.")],
  r"Prime sums are $2, 3, 5, 7, 11$ with $1, 2, 4, 6, 2$ outcomes respectively, a total of $15$ out of $36$ equally likely outcomes. The probability is $\frac{15}{36} = \frac{5}{12}$.",
  r"Treating the possible sums as equally likely instead of the $36$ ordered outcomes.",
  "U13-C-dice-sum-prime", "Single count over the $36$-outcome sample space.",
  check=lambda: frac([t for t in DICE2 if isprime(sum(t))], DICE2),
  values=[R(5, 12), R(5, 11), R(7, 18), R(13, 36)],
  numerical=dict(question=r"Two fair dice are thrown. If $p$ is the probability that the sum of the numbers obtained is a prime number, then the value of $36p$ is", answer=15),
  cognitive="Application")

# ---------------------------------------------------------------- 002
def _c2():
    people = ["m"] * 5 + ["w"] * 4
    tot = list(combinations(range(9), 4))
    fav = [c for c in tot if sum(1 for i in c if people[i] == "w") == 2]
    return frac(fav, tot)

QXI("U13-C-002", T_CL, "Selection of a committee", "Easy", "Single-step computation MCQ",
  r"A committee of $4$ is chosen at random from $5$ men and $4$ women. The probability that the committee contains exactly $2$ women is",
  r"$\frac{10}{21}$",
  [(r"$\frac{9}{14}$", r"Finds the probability of at least $2$ women: $\frac{60 + 20 + 1}{126} = \frac{81}{126} = \frac{9}{14}$."),
   (r"$\frac{1}{21}$", r"Counts only the choice of the women, $\binom{4}{2} = 6$, giving $\frac{6}{126}$."),
   (r"$\frac{8}{63}$", r"Adds $\binom{5}{2} + \binom{4}{2} = 16$ in place of multiplying, giving $\frac{16}{126}$.")],
  r"Total selections $\binom{9}{4} = 126$. Favourable selections $\binom{4}{2}\binom{5}{2} = 6 \cdot 10 = 60$. The probability is $\frac{60}{126} = \frac{10}{21}$.",
  r"Adding the counts of independent choices instead of multiplying them.",
  "U13-C-committee-selection", "One product of combinations over one total.",
  check=_c2, values=[R(10, 21), R(9, 14), R(1, 21), R(8, 63)],
  numerical=dict(question=r"A committee of $4$ is chosen at random from $5$ men and $4$ women. If $p$ is the probability that the committee contains exactly $2$ women, then the value of $21p$ is", answer=10),
  cognitive="Application")

# ---------------------------------------------------------------- 003
def _c3():
    pE, pF, pEF = R(2, 5), R(1, 2), R(1, 5)
    return 1 - (pE + pF - pEF)

QXI("U13-C-003", T_CL, "Addition theorem", "Easy", "Single-step computation MCQ",
  r"For events $E$ and $F$, $P(E) = \frac{2}{5}$, $P(F) = \frac{1}{2}$ and $P(E \cap F) = \frac{1}{5}$. The probability that neither $E$ nor $F$ occurs is",
  r"$\frac{3}{10}$",
  [(r"$\frac{1}{10}$", r"Takes $P(E \cup F) = P(E) + P(F) = \frac{9}{10}$ without subtracting $P(E \cap F)$, then $1 - \frac{9}{10}$."),
   (r"$\frac{7}{10}$", r"Stops at $P(E \cup F) = \frac{7}{10}$ and does not take the complement."),
   (r"$\frac{4}{5}$", r"Computes $1 - P(E \cap F)$, the probability that not both occur.")],
  r"$P(E \cup F) = \frac{2}{5} + \frac{1}{2} - \frac{1}{5} = \frac{7}{10}$. Neither occurs with probability $P(E' \cap F') = 1 - P(E \cup F) = \frac{3}{10}$.",
  r"Confusing 'neither occurs' with 'not both occur'.",
  "U13-C-addition-neither", "Addition theorem followed by a complement.",
  check=_c3, values=[R(3, 10), R(1, 10), R(7, 10), R(4, 5)], cognitive="Application")

# ---------------------------------------------------------------- 004
QXI("U13-C-004", T_CL, "Addition theorem with divisibility", "Easy", "Single-step computation MCQ",
  r"A number is chosen at random from $\{1, 2, 3, \ldots, 50\}$. The probability that it is a multiple of $4$ or a multiple of $6$ is",
  r"$\frac{8}{25}$",
  [(r"$\frac{2}{5}$", r"Adds $12 + 8 = 20$ without removing the common multiples of $12$."),
   (r"$\frac{9}{25}$", r"Takes the common multiples as multiples of $24$, subtracting only $2$: $12 + 8 - 2 = 18$."),
   (r"$\frac{6}{25}$", r"Subtracts the $4$ common multiples twice: $12 + 8 - 8 = 12$.")],
  r"Multiples of $4$: $12$; multiples of $6$: $8$; common multiples are multiples of $\operatorname{lcm}(4, 6) = 12$: $4$. So the count is $12 + 8 - 4 = 16$ and the probability is $\frac{16}{50} = \frac{8}{25}$.",
  r"Using the product $24$ instead of the LCM $12$ for the overlap.",
  "U13-C-divisibility-or", "Inclusion-exclusion with one overlap.",
  check=lambda: R(len([n for n in range(1, 51) if n % 4 == 0 or n % 6 == 0]), 50),
  values=[R(8, 25), R(2, 5), R(9, 25), R(6, 25)], cognitive="Application")

# ---------------------------------------------------------------- 005
def _c5():
    tot = list(multiset_permutations(list("ASSASSIN")))
    fav = [p for p in tot if all(not (p[i] == "S" and p[i + 1] == "S") for i in range(7))]
    return frac(fav, tot)

QXI("U13-C-005", T_CL, "Arrangements with restriction", "Medium", "Multi-step computation MCQ",
  r"The letters of the word ASSASSIN are arranged at random in a row. The probability that no two S's are adjacent is",
  r"$\frac{1}{14}$",
  [(r"$\frac{13}{14}$", r"Reads 'no two together' as 'not all four together' and finds $1 - \frac{60}{840}$."),
   (r"$\frac{1}{7}$", r"Arranges A, A, I, N as $4! = 24$ ways, not dividing by $2!$, getting $\frac{24 \cdot 5}{840}$."),
   (r"$\frac{1}{28}$", r"Uses $\frac{8!}{4!} = 1680$ total arrangements, not dividing by $2!$ for the two A's, getting $\frac{60}{1680}$.")],
  r"Total arrangements: $\frac{8!}{4!\,2!} = 840$. Arrange A, A, I, N in $\frac{4!}{2!} = 12$ ways, creating $5$ gaps; choose $4$ gaps for the S's in $\binom{5}{4} = 5$ ways. Favourable: $60$, so the probability is $\frac{60}{840} = \frac{1}{14}$.",
  r"Handling repeated letters inconsistently between numerator and denominator.",
  "U13-C-arrangement-gap", "Gap method plus repeated-letter counts in both numerator and denominator.",
  check=_c5, values=[R(1, 14), R(13, 14), R(1, 7), R(1, 28)], cognitive="Application")

# ---------------------------------------------------------------- 006
def _c6():
    tot = list(permutations(range(1, 6), 3))
    fav = [t for t in tot if sum(t) % 3 == 0]
    return frac(fav, tot)

QXI("U13-C-006", T_CL, "Numbers formed from digits", "Medium", "Multi-step computation MCQ",
  r"A three-digit number is formed at random using the digits $1, 2, 3, 4, 5$ without repetition. The probability that the number is divisible by $3$ is",
  r"$\frac{2}{5}$",
  [(r"$\frac{1}{3}$", r"Assumes one in every three such numbers is divisible by $3$ without counting."),
   (r"$\frac{3}{10}$", r"Misses one of the digit sets $\{1,2,3\}, \{1,3,5\}, \{2,3,4\}, \{3,4,5\}$, counting $3 \cdot 6 = 18$ of $60$."),
   (r"$\frac{41}{125}$", r"Allows repetition of digits, counting $41$ of the $5^3 = 125$ numbers.")],
  r"There are $5 \cdot 4 \cdot 3 = 60$ numbers. A number is divisible by $3$ when its digit sum is; the digit sets with sum divisible by $3$ are $\{1,2,3\}, \{1,3,5\}, \{2,3,4\}, \{3,4,5\}$, each giving $3! = 6$ numbers. The probability is $\frac{24}{60} = \frac{2}{5}$.",
  r"Assuming divisibility by $3$ occurs in exactly one third of the cases.",
  "U13-C-digits-divisible", "Divisibility rule plus casework on digit sets.",
  check=_c6, values=[R(2, 5), R(1, 3), R(3, 10), R(41, 125)], cognitive="Application")

# ---------------------------------------------------------------- 007
QXI("U13-C-007", T_CL, "Addition theorem for three events", "Medium", "Multi-step computation MCQ",
  r"A number is chosen at random from $\{1, 2, 3, \ldots, 100\}$. The probability that it is divisible by at least one of $2, 3$ and $5$ is",
  r"$\frac{37}{50}$",
  [(r"$\frac{11}{15}$", r"Uses the ideal densities: $1 - \frac{1}{2}\cdot\frac{2}{3}\cdot\frac{4}{5} = \frac{11}{15}$, ignoring that $100$ is not a multiple of $30$."),
   (r"$\frac{71}{100}$", r"Drops the triple term: $50 + 33 + 20 - 16 - 10 - 6 = 71$."),
   (r"$\frac{13}{50}$", r"Finds the probability of being divisible by none of them, $\frac{26}{100}$.")],
  r"By inclusion-exclusion the count is $50 + 33 + 20 - 16 - 10 - 6 + 3 = 74$, using $\lfloor 100/6 \rfloor = 16$, $\lfloor 100/10 \rfloor = 10$, $\lfloor 100/15 \rfloor = 6$, $\lfloor 100/30 \rfloor = 3$. The probability is $\frac{74}{100} = \frac{37}{50}$.",
  r"Omitting the triple-intersection term in the addition theorem for three events.",
  "U13-C-inclusion-exclusion-three", "Addition theorem for three events with floor counts.",
  check=lambda: R(len([n for n in range(1, 101) if n % 2 == 0 or n % 3 == 0 or n % 5 == 0]), 100),
  values=[R(37, 50), R(11, 15), R(71, 100), R(13, 50)],
  numerical=dict(question=r"A number is chosen at random from $\{1, 2, 3, \ldots, 100\}$. If $p$ is the probability that it is divisible by at least one of $2, 3$ and $5$, then the value of $100p$ is", answer=74),
  cognitive="Application")

# ---------------------------------------------------------------- 008
def _c8():
    pts = [(cos(2 * pi * k / 8), sin(2 * pi * k / 8)) for k in range(8)]
    def right(t):
        a, b, c = [pts[i] for i in t]
        for p, u, v in ((a, b, c), (b, a, c), (c, a, b)):
            if simplify((u[0] - p[0]) * (v[0] - p[0]) + (u[1] - p[1]) * (v[1] - p[1])) == 0:
                return True
        return False
    tot = list(combinations(range(8), 3))
    return frac([t for t in tot if right(t)], tot)

QXI("U13-C-008", T_CL, "Geometric counting", "Medium", "Multi-step computation MCQ",
  r"Three distinct vertices of a regular octagon are chosen at random. The probability that they form a right-angled triangle is",
  r"$\frac{3}{7}$",
  [(r"$\frac{6}{7}$", r"Counts $8$ diameters (one per vertex) instead of $4$, getting $\frac{8 \cdot 6}{56}$."),
   (r"$\frac{1}{14}$", r"Uses ordered selections $8 \cdot 7 \cdot 6 = 336$ as the total with the unordered count $24$."),
   (r"$\frac{1}{7}$", r"Counts only the isosceles right triangles, $2$ per diameter, giving $\frac{8}{56}$.")],
  r"A triangle inscribed in a circle is right-angled exactly when one side is a diameter. The octagon has $4$ diameters, and each combines with any of the other $6$ vertices, giving $24$ right triangles (none counted twice). The probability is $\frac{24}{\binom{8}{3}} = \frac{24}{56} = \frac{3}{7}$.",
  r"Double counting diameters by counting them once from each end.",
  "U13-C-polygon-triangle", "Needs the diameter criterion plus a careful count.",
  check=_c8, values=[R(3, 7), R(6, 7), R(1, 14), R(1, 7)], cognitive="Analysis")

# ---------------------------------------------------------------- 009
def _c9():
    tot = list(combinations(range(1, 31), 2))
    fav = [t for t in tot if (t[0] ** 2 - t[1] ** 2) % 3 == 0]
    return frac(fav, tot)

QXI("U13-C-009", T_CL, "Classical probability with residues", "Difficult", "Multi-step computation MCQ",
  r"Two distinct numbers $x$ and $y$ are chosen at random from $\{1, 2, 3, \ldots, 30\}$. The probability that $x^2 - y^2$ is divisible by $3$ is",
  r"$\frac{47}{87}$",
  [(r"$\frac{5}{9}$", r"Treats the choices as independent with replacement: $\left(\frac{1}{3}\right)^2 + \left(\frac{2}{3}\right)^2 = \frac{5}{9}$."),
   (r"$\frac{3}{29}$", r"Counts only pairs where both are multiples of $3$: $\frac{\binom{10}{2}}{\binom{30}{2}} = \frac{45}{435}$."),
   (r"$\frac{1}{3}$", r"Assumes $x^2 - y^2$ is equally likely to leave each remainder modulo $3$.")],
  r"Squares are $\equiv 0 \pmod 3$ for multiples of $3$ and $\equiv 1$ otherwise, so $3 \mid x^2 - y^2$ exactly when both are multiples of $3$ ($10$ numbers) or both are not ($20$ numbers). Favourable pairs: $\binom{10}{2} + \binom{20}{2} = 45 + 190 = 235$ out of $\binom{30}{2} = 435$, giving $\frac{235}{435} = \frac{47}{87}$.",
  r"Missing the case where neither number is a multiple of $3$.",
  "U13-C-residue-pairs", "Residue argument for squares plus two-case counting without replacement.",
  check=_c9, values=[R(47, 87), R(5, 9), R(3, 29), R(1, 3)],
  numerical=dict(question=r"Two distinct numbers $x$ and $y$ are chosen at random from $\{1, 2, 3, \ldots, 30\}$. If $p$ is the probability that $x^2 - y^2$ is divisible by $3$, then the value of $87p$ is", answer=47),
  cognitive="Analysis")

# ---------------------------------------------------------------- 010
def _c10():
    pE, pF = R(3, 4), R(5, 8)
    min_int = Max(0, pE + pF - 1)        # least possible P(E n F)
    min_union = Max(pE, pF)              # least possible P(E u F)
    s1 = bool(min_int >= R(3, 8))
    s2 = bool(R(5, 8) >= min_union)
    return (s1, s2)

QXI("U13-C-010", T_CL, "Bounds from the addition theorem", "Medium", "Statement-based MCQ",
  r"Let $E$ and $F$ be events with $P(E) = \frac{3}{4}$ and $P(F) = \frac{5}{8}$." "\n"
  r"Statement I: $P(E \cap F) \ge \frac{3}{8}$ necessarily." "\n"
  r"Statement II: It is possible that $P(E \cup F) = \frac{5}{8}$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Thinks $P(E \cup F)$ can be as small as $P(F)$, overlooking $P(E \cup F) \ge P(E) = \frac{3}{4}$."),
   (ST_FF, r"Thinks $P(E \cap F)$ can be $0$ for any two events, ignoring $P(E \cap F) = P(E) + P(F) - P(E \cup F) \ge \frac{3}{4} + \frac{5}{8} - 1$."),
   (ST_FT, r"Rejects the lower bound on the intersection and accepts the impossible union value.")],
  r"Since $P(E \cup F) \le 1$, $P(E \cap F) = P(E) + P(F) - P(E \cup F) \ge \frac{3}{4} + \frac{5}{8} - 1 = \frac{3}{8}$, so Statement I is true. Since $E \subseteq E \cup F$, $P(E \cup F) \ge \frac{3}{4} > \frac{5}{8}$, so Statement II is false.",
  r"Forgetting that a union is at least as probable as each of its parts.",
  "U13-C-addition-bounds", "Two bounds from the addition theorem, one of which is a trap.",
  check=_c10, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis")

# ======================================================================== XII (multiplication, conditional, independence)
# ---------------------------------------------------------------- 011
QXII("U13-C-011", T_CD, "Union of independent events", "Easy", "Single-step computation MCQ",
  r"If $E$ and $F$ are independent events with $P(E) = \frac{1}{3}$ and $P(F) = \frac{1}{4}$, then $P(E \cup F)$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{7}{12}$", r"Adds $P(E) + P(F)$, treating the events as mutually exclusive."),
   (r"$\frac{1}{12}$", r"Gives $P(E \cap F) = \frac{1}{3}\cdot\frac{1}{4}$ instead of the union."),
   (r"$\frac{11}{12}$", r"Computes $1 - P(E)P(F)$ instead of $1 - P(E')P(F')$.")],
  r"By independence $P(E \cap F) = \frac{1}{12}$, so $P(E \cup F) = \frac{1}{3} + \frac{1}{4} - \frac{1}{12} = \frac{1}{2}$. Equivalently $1 - \frac{2}{3}\cdot\frac{3}{4} = \frac{1}{2}$.",
  r"Treating independent events as mutually exclusive.",
  "U13-C-independent-union", "Addition theorem with the product rule.",
  check=lambda: 1 - (1 - R(1, 3)) * (1 - R(1, 4)),
  values=[R(1, 2), R(7, 12), R(1, 12), R(11, 12)], cognitive="Application")

# ---------------------------------------------------------------- 012
def _c12():
    balls = ["r"] * 5 + ["b"] * 3
    tot = list(permutations(range(8), 2))
    return frac([t for t in tot if balls[t[0]] == "r" and balls[t[1]] == "r"], tot)

QXII("U13-C-012", T_CD, "Multiplication theorem without replacement", "Easy", "Single-step computation MCQ",
  r"A bag contains $5$ red and $3$ black balls. Two balls are drawn one after the other without replacement. The probability that both are red is",
  r"$\frac{5}{14}$",
  [(r"$\frac{25}{64}$", r"Draws with replacement: $\left(\frac{5}{8}\right)^2$."),
   (r"$\frac{5}{16}$", r"Reduces the red count but not the total: $\frac{5}{8}\cdot\frac{4}{8}$."),
   (r"$\frac{15}{28}$", r"Finds the probability of one red and one black, $2 \cdot \frac{5}{8}\cdot\frac{3}{7}$.")],
  r"By the multiplication theorem, $P(R_1 \cap R_2) = P(R_1)P(R_2 \mid R_1) = \frac{5}{8}\cdot\frac{4}{7} = \frac{5}{14}$.",
  r"Not updating the total after the first draw.",
  "U13-C-multiplication-draws", "One application of the multiplication theorem.",
  check=_c12, values=[R(5, 14), R(25, 64), R(5, 16), R(15, 28)], cognitive="Application")

# ---------------------------------------------------------------- 013
def _c13():
    B = [t for t in DICE2 if sum(t) == 8]
    return frac([t for t in B if 3 in t], B)

QXII("U13-C-013", T_CD, "Conditional probability with dice", "Easy", "Single-step computation MCQ",
  r"Two fair dice are thrown. Given that the sum of the numbers obtained is $8$, the probability that at least one die shows $3$ is",
  r"$\frac{2}{5}$",
  [(r"$\frac{1}{18}$", r"Finds the joint probability $\frac{2}{36}$ instead of conditioning on sum $8$."),
   (r"$\frac{5}{36}$", r"Gives the probability of the condition, sum $8$, itself."),
   (r"$\frac{1}{3}$", r"Uses unordered pairs $\{2,6\}, \{3,5\}, \{4,4\}$ as equally likely.")],
  r"Sum $8$ occurs for $(2,6), (3,5), (4,4), (5,3), (6,2)$: $5$ outcomes. Of these, $(3,5)$ and $(5,3)$ contain a $3$. So the probability is $\frac{2}{5}$.",
  r"Using unordered outcomes as if they were equally likely.",
  "U13-C-conditional-dice-sum", "Reduced sample space of $5$ outcomes.",
  check=_c13, values=[R(2, 5), R(1, 18), R(5, 36), R(1, 3)], cognitive="Application")

# ---------------------------------------------------------------- 014
def _c14():
    pE, pF, pEF = R(1, 2), R(1, 3), R(1, 4)
    return (pE - pEF) / (1 - pF)

QXII("U13-C-014", T_CD, "Conditional probability with complements", "Easy", "Single-step computation MCQ",
  r"For events $E$ and $F$, $P(E) = \frac{1}{2}$, $P(F) = \frac{1}{3}$ and $P(E \cap F) = \frac{1}{4}$. Then $P(E \mid F')$ equals",
  r"$\frac{3}{8}$",
  [(r"$\frac{3}{4}$", r"Computes $P(E \mid F) = \frac{1/4}{1/3}$ instead."),
   (r"$\frac{1}{2}$", r"Assumes conditioning on $F'$ does not change $P(E)$."),
   (r"$\frac{1}{6}$", r"Multiplies $P(E \cap F')$ by $P(F')$: $\frac{1}{4}\cdot\frac{2}{3}$.")],
  r"$P(E \cap F') = P(E) - P(E \cap F) = \frac{1}{4}$ and $P(F') = \frac{2}{3}$. So $P(E \mid F') = \frac{1/4}{2/3} = \frac{3}{8}$.",
  r"Using the wrong conditioning event or multiplying instead of dividing.",
  "U13-C-conditional-complement", "Two short steps from the definition.",
  check=_c14, values=[R(3, 8), R(3, 4), R(1, 2), R(1, 6)], cognitive="Application")

# ---------------------------------------------------------------- 015
QXII("U13-C-015", T_CD, "At least one of independent events", "Easy", "Single-step computation MCQ",
  r"Three marksmen P, Q and R independently fire one shot each at a target. Their probabilities of hitting it are $\frac{1}{2}$, $\frac{1}{3}$ and $\frac{1}{4}$ respectively. The probability that the target is hit is",
  r"$\frac{3}{4}$",
  [(r"$\frac{1}{24}$", r"Finds the probability that all three hit, $\frac{1}{2}\cdot\frac{1}{3}\cdot\frac{1}{4}$."),
   (r"$\frac{1}{4}$", r"Finds the probability that nobody hits, $\frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4}$, and stops."),
   (r"$\frac{11}{24}$", r"Finds the probability that exactly one marksman hits.")],
  r"The target is missed only if all three miss: $\frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4} = \frac{1}{4}$. So it is hit with probability $1 - \frac{1}{4} = \frac{3}{4}$.",
  r"Not taking the complement of the 'all miss' event.",
  "U13-C-at-least-one-hit", "One complement and one product.",
  check=lambda: 1 - (1 - R(1, 2)) * (1 - R(1, 3)) * (1 - R(1, 4)),
  values=[R(3, 4), R(1, 24), R(1, 4), R(11, 24)], cognitive="Application")

# ---------------------------------------------------------------- 016
def _c16():
    tot = list(iproduct(range(1, 7), repeat=3))
    return frac([t for t in tot if t[0] != 6 and t[1] != 6 and t[2] == 6], tot)

QXII("U13-C-016", T_CD, "Independent repeated trials", "Easy", "Single-step computation MCQ",
  r"A fair die is thrown three times. The probability that a six appears for the first time on the third throw is",
  r"$\frac{25}{216}$",
  [(r"$\frac{25}{72}$", r"Finds the probability of exactly one six in three throws, multiplying by $3$."),
   (r"$\frac{1}{216}$", r"Takes the probability of a six on all three throws."),
   (r"$\frac{5}{36}$", r"Uses only one non-six factor, $\frac{5}{6}\cdot\frac{1}{6}$, the case of the second throw.")],
  r"The throws are independent; we need non-six, non-six, six: $\frac{5}{6}\cdot\frac{5}{6}\cdot\frac{1}{6} = \frac{25}{216}$.",
  r"Including arrangements when the position of the six is fixed.",
  "U13-C-first-success", "Product of three independent factors.",
  check=_c16, values=[R(25, 216), R(25, 72), R(1, 216), R(5, 36)],
  numerical=dict(question=r"A fair die is thrown three times. If $p$ is the probability that a six appears for the first time on the third throw, then the value of $216p$ is", answer=25),
  cognitive="Application")

# ---------------------------------------------------------------- 017
QXII("U13-C-017", T_CD, "Conditional probability from survey data", "Easy", "Single-step computation MCQ",
  r"In a class of $40$ students, $25$ study Mathematics, $18$ study Physics and $10$ study both. A student chosen at random is found to study Physics. The probability that the student also studies Mathematics is",
  r"$\frac{5}{9}$",
  [(r"$\frac{2}{5}$", r"Conditions on Mathematics instead of Physics: $\frac{10}{25}$."),
   (r"$\frac{1}{4}$", r"Finds the unconditional probability of studying both, $\frac{10}{40}$."),
   (r"$\frac{5}{8}$", r"Ignores the condition and gives $\frac{25}{40}$.")],
  r"Restrict to the $18$ Physics students; $10$ of them study Mathematics. The probability is $\frac{10}{18} = \frac{5}{9}$.",
  r"Reversing the conditioning event.",
  "U13-C-conditional-survey", "Direct use of the reduced sample space.",
  check=lambda: R(10, 40) / R(18, 40),
  values=[R(5, 9), R(2, 5), R(1, 4), R(5, 8)], cognitive="Application")

# ---------------------------------------------------------------- 018
QXII("U13-C-018", T_CD, "Mutually exclusive versus independent", "Easy", "Statement-based MCQ",
  r"Statement I: If $E$ and $F$ are mutually exclusive events with $P(E) > 0$ and $P(F) > 0$, then $E$ and $F$ are independent." "\n"
  r"Statement II: If $E$ and $F$ are independent events, then $E'$ and $F'$ are also independent." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Treats 'mutually exclusive' as meaning 'independent'."),
   (ST_FF, r"Rejects the complement property, thinking independence is not inherited by complements."),
   (ST_TF, r"Accepts the confusion of exclusivity with independence and rejects the complement property.")],
  r"For mutually exclusive events $P(E \cap F) = 0$, but $P(E)P(F) > 0$, so they are not independent; Statement I is false. If $E, F$ are independent, $P(E' \cap F') = 1 - P(E) - P(F) + P(E)P(F) = (1 - P(E))(1 - P(F)) = P(E')P(F')$, so Statement II is true.",
  r"Confusing mutually exclusive events with independent events.",
  "U13-C-exclusive-vs-independent", "Recall of two definitions and one identity.",
  check=None, cognitive="Understanding")

# ---------------------------------------------------------------- 019
QXII("U13-C-019", T_CD, "Conditional probability with divisibility", "Easy", "Single-step computation MCQ",
  r"A number is chosen at random from $\{1, 2, 3, \ldots, 100\}$. Given that it is divisible by $6$, the probability that it is divisible by $9$ is",
  r"$\frac{5}{16}$",
  [(r"$\frac{1}{20}$", r"Gives the joint probability $\frac{5}{100}$ of being divisible by both, without conditioning."),
   (r"$\frac{1}{16}$", r"Takes the numbers divisible by both $6$ and $9$ to be multiples of $6 \cdot 9 = 54$; only $54$ itself qualifies, giving $\frac{1}{16}$."),
   (r"$\frac{1}{9}$", r"Assumes the condition has no effect and uses the density $\frac{1}{9}$ of multiples of $9$.")],
  r"There are $\lfloor 100/6 \rfloor = 16$ multiples of $6$. A multiple of $6$ is divisible by $9$ exactly when it is a multiple of $\operatorname{lcm}(6, 9) = 18$; there are $\lfloor 100/18 \rfloor = 5$ such numbers. So the probability is $\frac{5}{16}$.",
  r"Ignoring that the condition changes the sample space, or using the product $54$ instead of $\operatorname{lcm}(6, 9) = 18$.",
  "U13-C-conditional-divisibility", "Reduced sample space with an LCM of non-coprime numbers.",
  check=lambda: R(len([n for n in range(1, 101) if n % 6 == 0 and n % 9 == 0]), len([n for n in range(1, 101) if n % 6 == 0])),
  values=[R(5, 16), R(1, 20), R(1, 16), R(1, 9)], cognitive="Application")

# ---------------------------------------------------------------- 020
def _c20():
    p = Symbol('p')
    s = [r for r in solve(Eq(R(1, 5) + p - R(1, 5) * p, R(3, 5)), p) if 0 <= r <= 1]
    return s[0]

QXII("U13-C-020", T_CD, "Finding a probability from independence", "Medium", "Inverse/parameter MCQ",
  r"$E$ and $F$ are independent events with $P(E) = \frac{1}{5}$ and $P(E \cup F) = \frac{3}{5}$. Then $P(F)$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{2}{5}$", r"Treats the events as mutually exclusive: $\frac{3}{5} - \frac{1}{5}$."),
   (r"$\frac{1}{3}$", r"Adds the product term: $\frac{3}{5} = \frac{1}{5} + p + \frac{p}{5}$, giving $p = \frac{1}{3}$."),
   (r"$\frac{1}{4}$", r"Uses $P(E')P(F') = P(E \cup F)$: $\frac{4}{5}(1 - p) = \frac{3}{5}$, giving $p = \frac{1}{4}$.")],
  r"Let $P(F) = p$. Then $P(E \cup F) = \frac{1}{5} + p - \frac{p}{5} = \frac{1}{5} + \frac{4p}{5} = \frac{3}{5}$, so $p = \frac{1}{2}$. Check: $1 - \frac{4}{5}\cdot\frac{1}{2} = \frac{3}{5}$.",
  r"Equating $P(E' \cap F')$ with $P(E \cup F)$ instead of $1 - P(E \cup F)$.",
  "U13-C-independent-inverse", "Sets up and solves a linear equation from independence.",
  check=_c20, values=[R(1, 2), R(2, 5), R(1, 3), R(1, 4)], cognitive="Application")

# ---------------------------------------------------------------- 021
def _c21():
    a, b = symbols('a b')
    sols = solve([Eq(a * b, R(1, 6)), Eq((1 - a) * (1 - b), R(1, 3))], [a, b], dict=True)
    return max(s[a] for s in sols if s[a] > s[b])

QXII("U13-C-021", T_CD, "Independent events from joint data", "Medium", "Inverse/parameter MCQ",
  r"$E$ and $F$ are independent events such that the probability that both occur is $\frac{1}{6}$ and the probability that neither occurs is $\frac{1}{3}$. If $P(E) > P(F)$, then $P(E)$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{3}$", r"Takes the smaller root of $6t^2 - 5t + 1 = 0$, which is $P(F)$."),
   (r"$\frac{5}{6}$", r"Gives the sum $P(E) + P(F)$ from $1 - (a + b) + ab = \frac{1}{3}$."),
   (r"$\frac{2}{3}$", r"Takes $P(E) = 1 - P(F) = 1 - \frac{1}{3}$, treating the events as complementary.")],
  r"Let $P(E) = a$, $P(F) = b$. Then $ab = \frac{1}{6}$ and $(1-a)(1-b) = 1 - (a+b) + ab = \frac{1}{3}$, so $a + b = \frac{5}{6}$. Hence $a, b$ are roots of $t^2 - \frac{5}{6}t + \frac{1}{6} = 0$, i.e. $6t^2 - 5t + 1 = 0$, giving $\frac{1}{2}$ and $\frac{1}{3}$. Since $a > b$, $P(E) = \frac{1}{2}$.",
  r"Not using the condition $P(E) > P(F)$ to pick the root.",
  "U13-C-independent-quadratic", "Two equations reduced to a quadratic in the probabilities.",
  check=_c21, values=[R(1, 2), R(1, 3), R(5, 6), R(2, 3)], cognitive="Application")

# ---------------------------------------------------------------- 022
def _c22():
    B = [t for t in DICE2 if 6 in t]
    return frac([t for t in B if sum(t) >= 10], B)

QXII("U13-C-022", T_CD, "Conditional probability with 'at least one'", "Medium", "Multi-step computation MCQ",
  r"Two fair dice are thrown. Given that at least one die shows $6$, the probability that the sum of the numbers is at least $10$ is",
  r"$\frac{5}{11}$",
  [(r"$\frac{5}{36}$", r"Finds the joint probability of a six and sum at least $10$ without dividing by $P(\text{at least one six})$."),
   (r"$\frac{6}{11}$", r"Counts all $6$ outcomes with sum at least $10$, including $(5,5)$, which has no six."),
   (r"$\frac{1}{6}$", r"Ignores the condition and gives $P(\text{sum} \ge 10) = \frac{6}{36}$.")],
  r"Outcomes with at least one $6$: $11$. Among them, sum at least $10$: $(4,6), (6,4), (5,6), (6,5), (6,6)$, which is $5$. So the probability is $\frac{5}{11}$.",
  r"Counting favourable outcomes outside the conditioning event.",
  "U13-C-conditional-at-least-one", "Builds the $11$-outcome reduced space and filters it.",
  check=_c22, values=[R(5, 11), R(5, 36), R(6, 11), R(1, 6)], cognitive="Application")

# ---------------------------------------------------------------- 023
def _c23():
    tot = list(iproduct("BG", repeat=3))
    cond = [t for t in tot if "B" in t]
    return frac([t for t in cond if t.count("G") >= 2], cond)

QXII("U13-C-023", T_CD, "Conditional probability for families", "Medium", "Multi-step computation MCQ",
  r"A family has three children, each equally likely to be a boy or a girl independently of the others. Given that at least one child is a boy, the probability that the family has at least two girls is",
  r"$\frac{3}{7}$",
  [(r"$\frac{1}{2}$", r"Ignores the condition: $P(\text{at least two girls}) = \frac{4}{8}$."),
   (r"$\frac{4}{7}$", r"Counts GGG among the favourable cases although it has no boy."),
   (r"$\frac{3}{8}$", r"Gives the joint probability $\frac{3}{8}$ without conditioning.")],
  r"The condition removes GGG, leaving $7$ equally likely outcomes. At least two girls together with a boy means exactly two girls: BGG, GBG, GGB, so $3$ outcomes. The probability is $\frac{3}{7}$.",
  r"Keeping outcomes that violate the condition.",
  "U13-C-conditional-children", "Conditioning removes one outcome; then a count.",
  check=_c23, values=[R(3, 7), R(1, 2), R(4, 7), R(3, 8)],
  numerical=dict(question=r"A family has three children, each equally likely to be a boy or a girl independently of the others. If $p$ is the probability that the family has at least two girls given that at least one child is a boy, then the value of $7p$ is", answer=3),
  cognitive="Application")

# ---------------------------------------------------------------- 024
def _c24():
    balls = ["w"] * 4 + ["b"] * 6
    tot = list(permutations(range(10), 3))
    fav = [t for t in tot if balls[t[0]] == "w" and balls[t[1]] == "w" and balls[t[2]] == "b"]
    return frac(fav, tot)

QXII("U13-C-024", T_CD, "Sequential draws", "Medium", "Multi-step computation MCQ",
  r"A box contains $4$ white and $6$ black balls. Balls are drawn one at a time at random without replacement. The probability that the first black ball appears on the third draw is",
  r"$\frac{1}{10}$",
  [(r"$\frac{12}{125}$", r"Draws with replacement: $\left(\frac{2}{5}\right)^2\cdot\frac{3}{5}$."),
   (r"$\frac{2}{15}$", r"Stops after the two white draws, $\frac{4}{10}\cdot\frac{3}{9}$, omitting the third factor."),
   (r"$\frac{3}{10}$", r"Finds the probability of exactly two white balls among the first three in any order, $\frac{\binom{4}{2}\binom{6}{1}}{\binom{10}{3}}$.")],
  r"We need white, white, black in that order: $\frac{4}{10}\cdot\frac{3}{9}\cdot\frac{6}{8} = \frac{72}{720} = \frac{1}{10}$.",
  r"Ignoring the order requirement in 'first black on the third draw'.",
  "U13-C-sequential-first-black", "Three-factor multiplication theorem with order.",
  check=_c24, values=[R(1, 10), R(12, 125), R(2, 15), R(3, 10)], cognitive="Application")

# ---------------------------------------------------------------- 025
def _c25():
    p, q_ = R(3, 4), R(4, 5)
    return p * (1 - q_) + (1 - p) * q_

QXII("U13-C-025", T_CD, "Independent truth-tellers", "Medium", "Multi-step computation MCQ",
  r"P speaks the truth in $75\%$ of cases and Q in $80\%$ of cases, independently. The probability that they contradict each other when stating the same fact is",
  r"$\frac{7}{20}$",
  [(r"$\frac{3}{5}$", r"Finds the probability that both speak the truth, $\frac{3}{4}\cdot\frac{4}{5}$."),
   (r"$\frac{1}{20}$", r"Finds the probability that both lie, $\frac{1}{4}\cdot\frac{1}{5}$."),
   (r"$\frac{13}{20}$", r"Finds the probability that they agree, $\frac{3}{5} + \frac{1}{20}$.")],
  r"They contradict when exactly one tells the truth: $\frac{3}{4}\cdot\frac{1}{5} + \frac{1}{4}\cdot\frac{4}{5} = \frac{3}{20} + \frac{4}{20} = \frac{7}{20}$.",
  r"Thinking contradiction means both lie.",
  "U13-C-truth-contradict", "Two disjoint cases of independent events.",
  check=_c25, values=[R(7, 20), R(3, 5), R(1, 20), R(13, 20)], cognitive="Application")

# ---------------------------------------------------------------- 026
def _c26():
    S = set(range(1, 7))
    E, F, G = {2, 4, 6}, {3, 6}, {1, 2, 3, 4}
    P = lambda X: R(len(X), 6)
    ind = lambda X, Y: P(X & Y) == P(X) * P(Y)
    return (ind(E, F), ind(E, G), ind(F, G))

QXII("U13-C-026", T_CD, "Testing independence", "Medium", "Conceptual/application MCQ",
  r"A fair die is thrown once. Let $E = \{2, 4, 6\}$, $F = \{3, 6\}$ and $G = \{1, 2, 3, 4\}$. The pairs of events that are independent are",
  r"$(E, F)$ and $(E, G)$ only",
  [(r"$(E, F)$ only", r"Thinks $E$ and $G$ are dependent because they overlap in $\{2, 4\}$, without checking $P(E \cap G) = \frac{1}{3} = \frac{1}{2}\cdot\frac{2}{3}$."),
   (r"$(E, F)$, $(E, G)$ and $(F, G)$", r"Assumes all pairs are independent, not checking $P(F \cap G) = \frac{1}{6} \ne \frac{1}{3}\cdot\frac{2}{3}$."),
   (r"$(E, G)$ only", r"Thinks $E$ and $F$ are dependent because both contain $6$, though $P(E \cap F) = \frac{1}{6} = \frac{1}{2}\cdot\frac{1}{3}$.")],
  r"$P(E) = \frac{1}{2}$, $P(F) = \frac{1}{3}$, $P(G) = \frac{2}{3}$. $P(E \cap F) = P(\{6\}) = \frac{1}{6} = P(E)P(F)$; $P(E \cap G) = P(\{2,4\}) = \frac{1}{3} = P(E)P(G)$; $P(F \cap G) = P(\{3\}) = \frac{1}{6} \ne \frac{2}{9}$. So only $(E, F)$ and $(E, G)$ are independent.",
  r"Judging independence by whether events overlap instead of by the product rule.",
  "U13-C-independence-test", "Three product checks; overlap intuition is a trap.",
  check=_c26, values=[(True, True, False), (True, False, False), (True, True, True), (False, True, False)],
  cognitive="Analysis")

# ---------------------------------------------------------------- 027
def _c27():
    x = Symbol('x', positive=True)
    # P(E n F) = x, P(F) = x/(1/2), P(E) = x/(1/3)
    pE, pF = 3 * x, 2 * x
    xs = solve(Eq(pE + pF - x, R(2, 3)), x)
    return pE.subs(x, xs[0])

QXII("U13-C-027", T_CD, "Two conditional probabilities", "Medium", "Inverse/parameter MCQ",
  r"For events $E$ and $F$, $P(E \mid F) = \frac{1}{2}$, $P(F \mid E) = \frac{1}{3}$ and $P(E \cup F) = \frac{2}{3}$. Then $P(E)$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{3}$", r"Finds $P(F) = 2x = \frac{1}{3}$ instead of $P(E)$."),
   (r"$\frac{1}{6}$", r"Gives $P(E \cap F) = x = \frac{1}{6}$."),
   (r"$\frac{2}{5}$", r"Writes $P(E \cup F) = P(E) + P(F) = 5x$, so $x = \frac{2}{15}$ and $P(E) = \frac{2}{5}$.")],
  r"Let $P(E \cap F) = x$. Then $P(F) = \frac{x}{1/2} = 2x$ and $P(E) = \frac{x}{1/3} = 3x$. So $P(E \cup F) = 3x + 2x - x = 4x = \frac{2}{3}$, giving $x = \frac{1}{6}$ and $P(E) = \frac{1}{2}$.",
  r"Inverting the conditioning, i.e. reading $P(E \mid F)$ as $\frac{P(E \cap F)}{P(E)}$.",
  "U13-C-two-conditionals", "Expresses three probabilities through one unknown, then the addition theorem.",
  check=_c27, values=[R(1, 2), R(1, 3), R(1, 6), R(2, 5)], cognitive="Application")

# ---------------------------------------------------------------- 028
def _c28():
    pH = R(2, 3)
    tot = list(iproduct("HT", repeat=3))
    return sum(prod(pH if c == "H" else 1 - pH for c in t) for t in tot if t.count("H") == 2)

QXII("U13-C-028", T_CD, "Biased coin, independent tosses", "Medium", "Multi-step computation MCQ",
  r"A coin is biased so that a head is twice as likely as a tail. It is tossed three times. The probability of getting exactly two heads is",
  r"$\frac{4}{9}$",
  [(r"$\frac{3}{8}$", r"Treats the coin as fair: $\frac{3}{8}$."),
   (r"$\frac{4}{27}$", r"Finds one arrangement, $\left(\frac{2}{3}\right)^2\cdot\frac{1}{3}$, and forgets the $3$ positions for the tail."),
   (r"$\frac{8}{27}$", r"Finds the probability of three heads, $\left(\frac{2}{3}\right)^3$.")],
  r"$P(H) = \frac{2}{3}$, $P(T) = \frac{1}{3}$. Exactly two heads occur as HHT, HTH, THH, each with probability $\frac{4}{9}\cdot\frac{1}{3} = \frac{4}{27}$. Total $3\cdot\frac{4}{27} = \frac{4}{9}$.",
  r"Forgetting the arrangements of the tail among the three tosses.",
  "U13-C-biased-coin", "Find the bias, then add three independent products.",
  check=_c28, values=[R(4, 9), R(3, 8), R(4, 27), R(8, 27)], cognitive="Application")

# ---------------------------------------------------------------- 029
def _c29():
    items = ["d"] * 3 + ["g"] * 7
    tot = list(permutations(range(10), 2))
    B = [t for t in tot if items[t[1]] == "d"]
    return frac([t for t in B if items[t[0]] == "d"], B)

QXII("U13-C-029", T_CD, "Conditioning on a later draw", "Medium", "Multi-step computation MCQ",
  r"A lot of $10$ items contains $3$ defective ones. Two items are drawn one after the other without replacement. Given that the second item drawn is defective, the probability that the first item drawn was also defective is",
  r"$\frac{2}{9}$",
  [(r"$\frac{3}{10}$", r"Assumes the first draw is unaffected by information about the second."),
   (r"$\frac{1}{15}$", r"Finds the joint probability $\frac{3}{10}\cdot\frac{2}{9}$ of both being defective."),
   (r"$\frac{1}{3}$", r"Removes one item from the lot but keeps all $3$ defectives available for the first draw: $\frac{3}{9}$.")],
  r"Count ordered pairs. Second defective: $9 \cdot 3 = 27$ pairs (choose the defective second item in $3$ ways, then any of the other $9$ first). Both defective: $3 \cdot 2 = 6$ pairs. So the probability is $\frac{6}{27} = \frac{2}{9}$, the same as conditioning the second draw on the first.",
  r"Believing a later draw carries no information about an earlier one.",
  "U13-C-condition-on-later", "Conditioning backwards in time is a trap; needs symmetry or counting.",
  check=_c29, values=[R(2, 9), R(3, 10), R(1, 15), R(1, 3)], cognitive="Analysis")

# ---------------------------------------------------------------- 030
def _c30():
    pE, pF, pU = R(3, 5), R(1, 2), R(4, 5)
    pEF = pE + pF - pU
    s1 = (pEF == pE * pF)
    s2 = ((pF - pEF) / pF == R(2, 5))
    return (bool(s1), bool(s2))

QXII("U13-C-030", T_CD, "Independence from given data", "Medium", "Statement-based MCQ",
  r"For events $E$ and $F$, $P(E) = \frac{3}{5}$, $P(F) = \frac{1}{2}$ and $P(E \cup F) = \frac{4}{5}$." "\n"
  r"Statement I: $E$ and $F$ are independent." "\n"
  r"Statement II: $P(E' \mid F) = \frac{2}{5}$." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_TF, r"Computes $P(E' \mid F)$ as $\frac{P(E')}{P(F)} = \frac{2/5}{1/2} = \frac{4}{5}$ and rejects Statement II."),
   (ST_FT, r"Believes independent events must satisfy $P(E \cup F) = P(E) + P(F)$, so rejects Statement I, while computing $P(E' \mid F)$ correctly."),
   (ST_FF, r"Uses $P(E \cap F) = P(E) + P(F) - 1 = \frac{1}{10}$, rejecting Statement I, and then $P(E' \mid F) = \frac{1/2 - 1/10}{1/2} = \frac{4}{5}$, rejecting Statement II.")],
  r"$P(E \cap F) = \frac{3}{5} + \frac{1}{2} - \frac{4}{5} = \frac{3}{10} = \frac{3}{5}\cdot\frac{1}{2}$, so $E$ and $F$ are independent; Statement I is true. Then $P(E' \cap F) = \frac{1}{2} - \frac{3}{10} = \frac{1}{5}$ and $P(E' \mid F) = \frac{1/5}{1/2} = \frac{2}{5}$; Statement II is true.",
  r"Dividing $P(E')$ by $P(F)$ instead of $P(E' \cap F)$ by $P(F)$.",
  "U13-C-independence-statements", "Two short computations each tested as a statement.",
  check=_c30, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Application")

# ---------------------------------------------------------------- 031
def _c31():
    tot = list(iproduct(range(12), repeat=4))
    fav = [t for t in tot if len(set(t)) == 4]
    return frac(fav, tot)

QXII("U13-C-031", T_CD, "Multiplication theorem: distinct outcomes", "Medium", "Multi-step computation MCQ",
  r"Four people are chosen at random. Assuming each person is equally likely to be born in any of the $12$ months, independently of the others, the probability that no two of them are born in the same month is",
  r"$\frac{55}{96}$",
  [(r"$\frac{41}{96}$", r"Finds the probability that at least two share a birth month."),
   (r"$\frac{55}{2304}$", r"Uses the unordered count $\binom{12}{4} = 495$ over the ordered total $12^4$."),
   (r"$\frac{1331}{1728}$", r"Requires each of the last three only to differ from the first person: $\left(\frac{11}{12}\right)^3$.")],
  r"By the multiplication theorem, $1\cdot\frac{11}{12}\cdot\frac{10}{12}\cdot\frac{9}{12} = \frac{990}{1728} = \frac{55}{96}$.",
  r"Mixing ordered and unordered counts.",
  "U13-C-distinct-months", "Chain of conditional factors; mixing ordered/unordered is a trap.",
  check=_c31, values=[R(55, 96), R(41, 96), R(55, 2304), R(1331, 1728)], cognitive="Application")

# ---------------------------------------------------------------- 032
def _c32():
    pE, pF, pEgF = R(2, 5), R(1, 2), R(3, 5)
    pEF = pEgF * pF
    neither = 1 - (pE + pF - pEF)
    return neither / (1 - pF)

QXII("U13-C-032", T_CD, "Conditional probability of complements", "Medium", "Multi-step computation MCQ",
  r"For events $E$ and $F$, $P(E) = \frac{2}{5}$, $P(F) = \frac{1}{2}$ and $P(E \mid F) = \frac{3}{5}$. Then $P(E' \mid F')$ equals",
  r"$\frac{4}{5}$",
  [(r"$\frac{2}{5}$", r"Takes $P(E' \mid F') = 1 - P(E \mid F)$."),
   (r"$\frac{2}{3}$", r"Divides $P(E' \cap F') = \frac{2}{5}$ by $P(E') = \frac{3}{5}$, finding $P(F' \mid E')$."),
   (r"$\frac{3}{5}$", r"Assumes $P(E' \mid F') = P(E \mid F)$.")],
  r"$P(E \cap F) = \frac{3}{5}\cdot\frac{1}{2} = \frac{3}{10}$, so $P(E \cup F) = \frac{2}{5} + \frac{1}{2} - \frac{3}{10} = \frac{3}{5}$ and $P(E' \cap F') = \frac{2}{5}$. Hence $P(E' \mid F') = \frac{2/5}{1/2} = \frac{4}{5}$.",
  r"Believing $P(E' \mid F') = 1 - P(E \mid F)$.",
  "U13-C-complement-conditional", "Chain of multiplication theorem, addition theorem, complement and division.",
  check=_c32, values=[R(4, 5), R(2, 5), R(2, 3), R(3, 5)], cognitive="Application")

# ---------------------------------------------------------------- 033
def _c33():
    r, b = 3, 2
    p1 = R(r, r + b)
    p2 = R(r + 2, r + b + 2)
    return p1 * p2

QXII("U13-C-033", T_CD, "Multiplication theorem with changing urn", "Medium", "Multi-step computation MCQ",
  r"An urn contains $3$ red and $2$ black balls. A ball is drawn at random, its colour is noted, and it is returned to the urn together with $2$ more balls of the same colour. A second ball is then drawn at random. The probability that both balls drawn are red is",
  r"$\frac{3}{7}$",
  [(r"$\frac{9}{25}$", r"Ignores the added balls and uses $\left(\frac{3}{5}\right)^2$."),
   (r"$\frac{3}{10}$", r"Treats the draws as without replacement: $\frac{3}{5}\cdot\frac{2}{4}$."),
   (r"$\frac{2}{5}$", r"Adds only one red ball, so the second factor is $\frac{4}{6}$.")],
  r"$P(R_1) = \frac{3}{5}$. After a red draw the urn has $5$ red and $2$ black, so $P(R_2 \mid R_1) = \frac{5}{7}$. Hence $P(R_1 \cap R_2) = \frac{3}{5}\cdot\frac{5}{7} = \frac{3}{7}$.",
  r"Not updating the urn composition for the second draw.",
  "U13-C-polya-urn", "Updates the urn correctly before the second factor.",
  check=_c33, values=[R(3, 7), R(9, 25), R(3, 10), R(2, 5)], cognitive="Application")

# ---------------------------------------------------------------- 034
def _c34():
    ps = [R(1, 2), R(2, 3), R(3, 4)]
    tot = 0
    for t in iproduct([0, 1], repeat=3):
        if sum(t) == 2:
            tot += prod(ps[i] if t[i] else 1 - ps[i] for i in range(3))
    return tot

QXII("U13-C-034", T_CD, "Exactly two of three independent events", "Medium", "Multi-step computation MCQ",
  r"Three students P, Q and R independently attempt a problem. Their probabilities of solving it are $\frac{1}{2}$, $\frac{2}{3}$ and $\frac{3}{4}$ respectively. The probability that exactly two of them solve it is",
  r"$\frac{11}{24}$",
  [(r"$\frac{1}{4}$", r"Finds the probability that all three solve it, $\frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4}$."),
   (r"$\frac{17}{24}$", r"Finds the probability that at least two solve it, adding the all-three case."),
   (r"$\frac{23}{24}$", r"Finds the probability that at least one solves it, $1 - \frac{1}{2}\cdot\frac{1}{3}\cdot\frac{1}{4}$.")],
  r"Exactly two: $\frac{1}{2}\cdot\frac{2}{3}\cdot\frac{1}{4} + \frac{1}{2}\cdot\frac{1}{3}\cdot\frac{3}{4} + \frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4} = \frac{2 + 3 + 6}{24} = \frac{11}{24}$.",
  r"Confusing 'exactly two' with 'at least two'.",
  "U13-C-exactly-two", "Three cases of products of independent events.",
  check=_c34, values=[R(11, 24), R(1, 4), R(17, 24), R(23, 24)],
  numerical=dict(question=r"Three students P, Q and R independently attempt a problem. Their probabilities of solving it are $\frac{1}{2}$, $\frac{2}{3}$ and $\frac{3}{4}$ respectively. If $p$ is the probability that exactly two of them solve it, then the value of $24p$ is", answer=11),
  cognitive="Application")

# ---------------------------------------------------------------- 035
def _c35():
    deck = [(r_, s) for r_ in range(13) for s in range(4)]
    tot = list(combinations(range(52), 2))
    isace = lambda i: deck[i][0] == 0
    B = [t for t in tot if isace(t[0]) or isace(t[1])]
    return frac([t for t in B if isace(t[0]) and isace(t[1])], B)

QXII("U13-C-035", T_CD, "Conditional probability with cards", "Difficult", "Multi-step computation MCQ",
  r"Two cards are drawn at random without replacement from a well-shuffled pack of $52$ cards. Given that at least one of them is an ace, the probability that both are aces is",
  r"$\frac{1}{33}$",
  [(r"$\frac{1}{221}$", r"Finds the unconditional probability $\frac{\binom{4}{2}}{\binom{52}{2}}$ of two aces."),
   (r"$\frac{1}{17}$", r"Conditions on the first card being an ace: $\frac{3}{51}$."),
   (r"$\frac{1}{25}$", r"Draws with replacement: $\frac{(1/13)^2}{1 - (12/13)^2} = \frac{1}{25}$.")],
  r"$P(\text{both aces}) = \frac{\binom{4}{2}}{\binom{52}{2}} = \frac{6}{1326}$ and $P(\text{at least one ace}) = 1 - \frac{\binom{48}{2}}{\binom{52}{2}} = \frac{1326 - 1128}{1326} = \frac{198}{1326}$. So the conditional probability is $\frac{6}{198} = \frac{1}{33}$.",
  r"Treating 'at least one is an ace' as 'the first is an ace'.",
  "U13-C-at-least-one-ace", "Condition 'at least one' is a classic trap versus 'a specific one'.",
  check=_c35, values=[R(1, 33), R(1, 221), R(1, 17), R(1, 25)], cognitive="Analysis")

# ---------------------------------------------------------------- 036
def _c36():
    cnt = 0
    for n in range(1, 41):
        S = range(1, n + 1)
        pE = R(len([k for k in S if k % 3 == 0]), n)
        pF = R(len([k for k in S if k % 5 == 0]), n)
        pEF = R(len([k for k in S if k % 15 == 0]), n)
        if pEF == pE * pF:
            cnt += 1
    return Integer(cnt)

QXII("U13-C-036", T_CD, "Independence depending on the sample space", "Difficult", "Multi-step computation MCQ",
  r"A number is chosen at random from $\{1, 2, \ldots, n\}$. Let $E$ be the event that it is a multiple of $3$ and $F$ the event that it is a multiple of $5$. Using the definition that $E$ and $F$ are independent when $P(E \cap F) = P(E)P(F)$ (applied as stated, including values of $n$ for which $P(E)$ or $P(F)$ is $0$), the number of values of $n \in \{1, 2, \ldots, 40\}$ for which $E$ and $F$ are independent is",
  r"$8$",
  [(r"$4$", r"Finds $n = 15, 18, 30, 33$ but ignores $n = 1, 2, 3, 4$, where $P(F) = 0$ and the product rule holds trivially."),
   (r"$2$", r"Assumes independence needs $n$ to be a multiple of $15$, getting only $n = 15, 30$."),
   (r"$6$", r"Takes the multiples of $15$ together with $n = 1, 2, 3, 4$, missing $n = 18$ and $n = 33$.")],
  r"The condition is $\lfloor n/3 \rfloor \lfloor n/5 \rfloor = n \lfloor n/15 \rfloor$. For $n \le 4$, $\lfloor n/5 \rfloor = 0 = \lfloor n/15 \rfloor$, so it holds. For $5 \le n \le 14$ the right side is $0$ but the left is positive. For $15 \le n \le 29$, need $\lfloor n/3 \rfloor \lfloor n/5 \rfloor = n$: true for $n = 15$ ($5 \cdot 3$) and $n = 18$ ($6 \cdot 3$). For $30 \le n \le 40$, need the product to equal $2n$: true for $n = 30$ ($10 \cdot 6$) and $n = 33$ ($11 \cdot 6$). Total $4 + 2 + 2 = 8$.",
  r"Assuming independence of divisibility events holds only when $n$ is a multiple of the LCM.",
  "U13-C-independence-sample-size", "Floor-function casework plus the trivial zero-probability case.",
  check=_c36, values=[Integer(8), Integer(4), Integer(2), Integer(6)],
  numerical=dict(question=r"A number is chosen at random from $\{1, 2, \ldots, n\}$. Let $E$ be the event that it is a multiple of $3$ and $F$ the event that it is a multiple of $5$. Using the definition that $E$ and $F$ are independent when $P(E \cap F) = P(E)P(F)$ (applied as stated, including values of $n$ for which $P(E)$ or $P(F)$ is $0$), the number of values of $n \in \{1, 2, \ldots, 40\}$ for which $E$ and $F$ are independent is", answer=8),
  cognitive="Analysis")

# ---------------------------------------------------------------- 037
def _c37():
    a = R(len([t for t in DICE2 if sum(t) == 6]), 36)
    b = R(len([t for t in DICE2 if sum(t) == 7]), 36)
    k = Symbol('k', integer=True, nonnegative=True)
    return summation(((1 - a) * (1 - b)) ** k * a, (k, 0, oo))

QXII("U13-C-037", T_CD, "Alternate trials game", "Difficult", "Multi-step computation MCQ",
  r"P and Q throw a pair of fair dice alternately, P starting. P wins if he throws a sum of $6$ before Q throws a sum of $7$, and Q wins if he throws a sum of $7$ before P throws a sum of $6$. The game continues until one of them wins. The probability that P wins is",
  r"$\frac{30}{61}$",
  [(r"$\frac{31}{61}$", r"Finds the probability that Q wins, $1 - \frac{30}{61}$."),
   (r"$\frac{5}{11}$", r"Compares single-throw chances only: $\frac{5/36}{5/36 + 6/36}$."),
   (r"$\frac{36}{67}$", r"Uses P's failure probability for both players: $\frac{5/36}{1 - (31/36)^2}$.")],
  r"Per throw, P succeeds with probability $\frac{5}{36}$ and Q with $\frac{6}{36}$. P wins on his $(k+1)$th throw with probability $\left(\frac{31}{36}\cdot\frac{30}{36}\right)^k\frac{5}{36}$. Summing, $P = \frac{5/36}{1 - \frac{930}{1296}} = \frac{5}{36}\cdot\frac{1296}{366} = \frac{30}{61}$.",
  r"Using the same failure probability for both players in each round.",
  "U13-C-alternate-throws", "Two different success probabilities plus a geometric series of independent rounds.",
  check=_c37, values=[R(30, 61), R(31, 61), R(5, 11), R(36, 67)],
  numerical=dict(question=r"P and Q throw a pair of fair dice alternately, P starting. P wins if he throws a sum of $6$ before Q throws a sum of $7$, and Q wins if he throws a sum of $7$ before P throws a sum of $6$. If $p$ is the probability that P wins, then the value of $61p$ is", answer=30),
  cognitive="Analysis")

# ---------------------------------------------------------------- 038
def _c38():
    p = Symbol('p')
    roots = solve(Eq(p * (1 - 2 * p) + 2 * p * (1 - p), R(5, 9)), p)
    valid = [r for r in roots if r.is_real and 0 <= r and 2 * r <= 1]
    return sum(valid)

QXII("U13-C-038", T_CD, "Parameter from 'exactly one'", "Difficult", "Inverse/parameter MCQ",
  r"$E$ and $F$ are independent events with $P(E) = p$ and $P(F) = 2p$. If the probability that exactly one of $E$, $F$ occurs is $\frac{5}{9}$, then the sum of all possible values of $p$ is",
  r"$\frac{3}{4}$",
  [(r"$\frac{3}{2}$", r"Writes $P(\text{exactly one}) = P(E) + P(F) - P(E \cap F) = 3p - 2p^2$, getting $18p^2 - 27p + 5 = 0$ with root sum $\frac{3}{2}$."),
   (r"$\frac{1}{3}$", r"Keeps only one root of $36p^2 - 27p + 5 = 0$, rejecting $p = \frac{5}{12}$ without reason."),
   (r"$\frac{5}{36}$", r"Gives the product of the roots of $36p^2 - 27p + 5 = 0$ instead of the sum.")],
  r"$P(\text{exactly one}) = p(1 - 2p) + 2p(1 - p) = 3p - 4p^2 = \frac{5}{9}$, so $36p^2 - 27p + 5 = 0$, giving $p = \frac{1}{3}$ or $p = \frac{5}{12}$. Both satisfy $0 \le 2p \le 1$ ($2p = \frac{2}{3}$ or $\frac{5}{6}$). The sum is $\frac{3}{4}$.",
  r"Using $P(E \cup F)$ for 'exactly one' (subtracting the intersection once instead of twice).",
  "U13-C-exactly-one-parameter", "Quadratic from independence plus validity check of both roots.",
  check=_c38, values=[R(3, 4), R(3, 2), R(1, 3), R(5, 36)], cognitive="Analysis")

# ---------------------------------------------------------------- 039
def _c39():
    tot = list(combinations(range(1, 21), 2))
    B = [t for t in tot if (t[0] * t[1]) % 2 == 0]
    return frac([t for t in B if (t[0] + t[1]) % 2 == 0], B)

QXII("U13-C-039", T_CD, "Conditional probability with parity", "Difficult", "Multi-step computation MCQ",
  r"Two distinct numbers are chosen at random from $\{1, 2, 3, \ldots, 20\}$. Given that their product is even, the probability that their sum is even is",
  r"$\frac{9}{29}$",
  [(r"$\frac{9}{38}$", r"Finds the joint probability $\frac{45}{190}$ without conditioning."),
   (r"$\frac{1}{2}$", r"Assumes the parity of the sum is unaffected by the condition."),
   (r"$\frac{18}{29}$", r"Counts both-odd pairs as favourable too, $\frac{90}{145}$, although their product is odd.")],
  r"Total pairs $\binom{20}{2} = 190$. Product odd only when both are odd: $\binom{10}{2} = 45$, so product even: $145$. With product even, the sum is even only when both are even: $\binom{10}{2} = 45$. The probability is $\frac{45}{145} = \frac{9}{29}$.",
  r"Keeping both-odd pairs, which the condition excludes.",
  "U13-C-parity-conditional", "Parity casework within a reduced sample space.",
  check=_c39, values=[R(9, 29), R(9, 38), R(1, 2), R(18, 29)], cognitive="Analysis")

# ---------------------------------------------------------------- 040
def _c40():
    a, b, c = symbols('a b c')
    eqs = [Eq(a * (1 - b) * (1 - c), R(1, 4)), Eq((1 - a) * b * (1 - c), R(1, 8)),
           Eq((1 - a) * (1 - b) * c, R(1, 12)), Eq((1 - a) * (1 - b) * (1 - c), R(1, 4))]
    sols = [s for s in solve(eqs, [a, b, c], dict=True) if all(0 <= v <= 1 for v in s.values())]
    return sols[0][b]

QXII("U13-C-040", T_CD, "Three independent events from 'only' probabilities", "Difficult", "Inverse/parameter MCQ",
  r"$E$, $F$, $G$ are mutually independent events. The probability that only $E$ occurs is $\frac{1}{4}$, that only $F$ occurs is $\frac{1}{8}$, that only $G$ occurs is $\frac{1}{12}$, and that none of them occurs is $\frac{1}{4}$. Then $P(F)$ equals",
  r"$\frac{1}{3}$",
  [(r"$\frac{1}{8}$", r"Equates $P(F)$ with the probability that only $F$ occurs."),
   (r"$\frac{1}{2}$", r"Takes the ratio $\frac{1/8}{1/4}$ as $P(F)$ itself instead of $\frac{P(F)}{P(F')}$."),
   (r"$\frac{3}{8}$", r"Adds the probabilities of 'only $F$' and 'none'.")],
  r"Let $P(E) = a$, $P(F) = b$, $P(G) = c$. Dividing 'only $F$' by 'none': $\frac{b(1-a)(1-c)}{(1-a)(1-b)(1-c)} = \frac{b}{1-b} = \frac{1/8}{1/4} = \frac{1}{2}$, so $b = \frac{1}{3}$. (Similarly $a = \frac{1}{2}$, $c = \frac{1}{4}$, and $(1-a)(1-b)(1-c) = \frac{1}{4}$ confirms consistency.)",
  r"Confusing $P(F)$ with $P(\text{only } F)$.",
  "U13-C-only-events", "Requires the ratio trick across three independent events.",
  check=_c40, values=[R(1, 3), R(1, 8), R(1, 2), R(3, 8)], cognitive="Analysis")

# ---------------------------------------------------------------- 041
def _c41():
    S = list(iproduct("HT", repeat=2))
    E = {s for s in S if s[0] == "H"}
    F = {s for s in S if s[1] == "H"}
    G = {s for s in S if s.count("H") == 1}
    P = lambda X: R(len(X), 4)
    mutual = (P(E & F) == P(E) * P(F) and P(E & G) == P(E) * P(G) and P(F & G) == P(F) * P(G)
              and P(E & F & G) == P(E) * P(F) * P(G))
    eg_not_indep = P(E & G) != P(E) * P(G)
    return (bool(mutual), bool(eg_not_indep))

QXII("U13-C-041", T_CD, "Pairwise versus mutual independence", "Difficult", "Statement-based MCQ",
  r"A fair coin is tossed twice. Let $E$: head on the first toss, $F$: head on the second toss, $G$: exactly one head in the two tosses." "\n"
  r"Statement I: $E$, $F$, $G$ are mutually independent." "\n"
  r"Statement II: $E$ and $G$ are not independent." "\n"
  r"In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Checks only pairs for Statement I and believes $G$ depends on $E$ for Statement II."),
   (ST_TF, r"Verifies the three pairwise product rules and wrongly concludes mutual independence."),
   (ST_FT, r"Rejects mutual independence correctly but thinks $E$ influences $G$ since $G$ depends on the first toss.")],
  r"$P(E) = P(F) = P(G) = \frac{1}{2}$. $E \cap G = \{HT\}$, so $P(E \cap G) = \frac{1}{4} = P(E)P(G)$; $E$ and $G$ are independent, so Statement II is false. Similarly $E, F$ and $F, G$ are independent, but $E \cap F \cap G = \emptyset$, so $P(E \cap F \cap G) = 0 \ne \frac{1}{8}$; the events are not mutually independent, and Statement I is false.",
  r"Equating pairwise independence with mutual independence.",
  "U13-C-pairwise-mutual", "Needs both pairwise checks and the triple check; intuition misleads twice.",
  check=_c41, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Analysis")

# ---------------------------------------------------------------- 042
def _c42():
    tot = list(permutations(range(1, 7)))
    B = [p for p in tot if p.index(1) < p.index(2)]
    return frac([p for p in B if p.index(3) < p.index(2)], B)

QXII("U13-C-042", T_CD, "Conditional probability in permutations", "Difficult", "Multi-step computation MCQ",
  r"The numbers $1, 2, 3, 4, 5, 6$ are arranged in a row at random. Given that $1$ appears somewhere before $2$, the probability that $3$ also appears somewhere before $2$ is",
  r"$\frac{2}{3}$",
  [(r"$\frac{1}{2}$", r"Assumes the relative order of $3$ and $2$ is unaffected by the condition."),
   (r"$\frac{1}{3}$", r"Finds the joint probability that $2$ comes after both $1$ and $3$, without conditioning."),
   (r"$\frac{1}{6}$", r"Counts only the single relative order $1, 3, 2$ out of the $3! = 6$ orders of $1, 2, 3$.")],
  r"Only the relative order of $1, 2, 3$ matters, and all $3! = 6$ orders are equally likely. '$1$ before $2$' holds in $3$ of them; '$1$ and $3$ both before $2$' holds in $2$ of them ($1,3,2$ and $3,1,2$). So the probability is $\frac{2/6}{3/6} = \frac{2}{3}$.",
  r"Assuming the two order relations are independent.",
  "U13-C-permutation-order", "Reduce to relative orders, then condition; independence intuition is wrong.",
  check=_c42, values=[R(2, 3), R(1, 2), R(1, 3), R(1, 6)], cognitive="Analysis")

# ---------------------------------------------------------------- 043
def _c43():
    B = [t for t in DICE2 if (t[0] * t[1]) % 4 == 0]
    return frac([t for t in B if (t[0] + t[1]) % 2 == 0], B)

QXII("U13-C-043", T_CD, "Conditional probability with divisibility of a product", "Difficult", "Multi-step computation MCQ",
  r"Two fair dice are thrown. Given that the product of the numbers obtained is a multiple of $4$, the probability that their sum is even is",
  r"$\frac{3}{5}$",
  [(r"$\frac{1}{4}$", r"Finds the joint probability $\frac{9}{36}$ without conditioning."),
   (r"$\frac{1}{3}$", r"Conditions on the product being even ($27$ outcomes) instead of a multiple of $4$, getting $\frac{9}{27}$."),
   (r"$\frac{1}{2}$", r"Assumes the parity of the sum is unaffected by the condition.")],
  r"Product is a multiple of $4$ when both numbers are even ($3 \cdot 3 = 9$ outcomes) or one is $4$ and the other odd ($2 \cdot 3 = 6$ outcomes): $15$ outcomes. The sum is even only in the both-even case (an odd and an even give an odd sum), so $9$ outcomes. The probability is $\frac{9}{15} = \frac{3}{5}$.",
  r"Missing the 'one factor is $4$' case of a product divisible by $4$.",
  "U13-C-product-multiple-four", "Casework on divisibility by $4$ then parity within the reduced space.",
  check=_c43, values=[R(3, 5), R(1, 4), R(1, 3), R(1, 2)], cognitive="Analysis")

# ---------------------------------------------------------------- 044
def _c44():
    tot = list(combinations(range(1, 9), 3))   # positions of the 3 red balls among 8 draws
    return frac([t for t in tot if max(t) == 5], tot)

QXII("U13-C-044", T_CD, "Position of the last success", "Difficult", "Multi-step computation MCQ",
  r"An urn contains $3$ red and $5$ white balls. The balls are drawn one at a time at random without replacement until the urn is empty. The probability that the last red ball is drawn on the fifth draw is",
  r"$\frac{3}{28}$",
  [(r"$\frac{5}{28}$", r"Finds the probability that all three red balls are among the first five draws, $\frac{\binom{5}{3}}{\binom{8}{3}}$."),
   (r"$\frac{3}{8}$", r"Finds the probability that the fifth ball drawn is red."),
   (r"$\frac{1}{8}$", r"Assumes the last red ball is equally likely to be at any of the $8$ draws.")],
  r"All $\binom{8}{3} = 56$ sets of positions for the red balls are equally likely. The last red is at position $5$ when one red is at $5$ and the other two are among positions $1$ to $4$: $\binom{4}{2} = 6$ ways. The probability is $\frac{6}{56} = \frac{3}{28}$.",
  r"Confusing 'last red on the fifth draw' with 'all reds by the fifth draw'.",
  "U13-C-last-red-position", "Reformulation as positions plus a careful count.",
  check=_c44, values=[R(3, 28), R(5, 28), R(3, 8), R(1, 8)],
  numerical=dict(question=r"An urn contains $3$ red and $5$ white balls. The balls are drawn one at a time at random without replacement until the urn is empty. If $p$ is the probability that the last red ball is drawn on the fifth draw, then the value of $28p$ is", answer=3),
  cognitive="Analysis")

# ---------------------------------------------------------------- 045
def _c45():
    k = Symbol('k', integer=True, positive=True)
    f = lambda n: R(5, 6) ** (n - 1) * R(1, 6)          # P(first six on throw n)
    p_more_than_2 = summation(R(5, 6) ** (k - 1) * R(1, 6), (k, 3, oo))
    return f(4) / p_more_than_2

QXII("U13-C-045", T_CD, "Conditioning on waiting time", "Difficult", "Multi-step computation MCQ",
  r"A fair die is thrown repeatedly until a six appears. Given that more than two throws are needed, the probability that exactly four throws are needed is",
  r"$\frac{5}{36}$",
  [(r"$\frac{125}{1296}$", r"Finds the unconditional probability $\left(\frac{5}{6}\right)^3\frac{1}{6}$ of needing exactly four throws."),
   (r"$\frac{1}{6}$", r"Finds the probability that exactly three throws are needed given more than two, i.e. a six on the very next throw."),
   (r"$\frac{25}{216}$", r"Uses $\left(\frac{5}{6}\right)^2\frac{1}{6}$, the unconditional probability of needing exactly three throws.")],
  r"$P(\text{exactly 4}) = \left(\frac{5}{6}\right)^3\frac{1}{6}$ and $P(\text{more than 2}) = P(\text{first two not six}) = \left(\frac{5}{6}\right)^2$. So the conditional probability is $\frac{5}{6}\cdot\frac{1}{6} = \frac{5}{36}$: a non-six on the third throw and a six on the fourth.",
  r"Not dividing by the probability of the conditioning event.",
  "U13-C-waiting-time-conditional", "Infinite sample space; conditioning reduces to two fresh throws.",
  check=_c45, values=[R(5, 36), R(125, 1296), R(1, 6), R(25, 216)], cognitive="Analysis")
