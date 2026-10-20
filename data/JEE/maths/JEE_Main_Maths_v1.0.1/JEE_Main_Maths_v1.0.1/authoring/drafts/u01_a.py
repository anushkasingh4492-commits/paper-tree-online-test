import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

from itertools import combinations, product
from sympy.solvers.simplex import lpmin, lpmax

# ---------------------------------------------------------------- helpers
x = Symbol('x', real=True)
y = Symbol('y', real=True)


def subsets(s):
    s = list(s)
    return [frozenset(c) for r in range(len(s) + 1) for c in combinations(s, r)]


U3 = frozenset({1, 2, 3})


def identity_index(lhs, cands, nsets=2, U=U3):
    """Index of the unique candidate expression equal to lhs for ALL choices of nsets subsets of U."""
    ok = [True] * len(cands)
    for sets in product(subsets(U), repeat=nsets):
        L = lhs(U, *sets)
        for i, c in enumerate(cands):
            if c(U, *sets) != L:
                ok[i] = False
    good = [i for i, o in enumerate(ok) if o]
    assert len(good) == 1, good
    return good[0]


def always(stmt, nsets, U=U3):
    """True if stmt(U, *sets) holds for every choice of nsets subsets of U."""
    return all(stmt(U, *s) for s in product(subsets(U), repeat=nsets))


def venn3(nP, nQ, nR, nPQ, nQR, nPR, nPQR):
    a, b, c, pq, qr, pr, t = symbols('a b c pq qr pr t')
    sol = solve([a + pq + pr + t - nP, b + pq + qr + t - nQ, c + qr + pr + t - nR,
                 pq + t - nPQ, qr + t - nQR, pr + t - nPR, t - nPQR],
                [a, b, c, pq, qr, pr, t], dict=True)[0]
    d = {k.name: v for k, v in sol.items()}
    assert all(v >= 0 for v in d.values())
    return d


def int_points(cond, lo=-200, hi=200):
    return FiniteSet(*[k for k in range(lo, hi + 1) if cond(Integer(k))])


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."
NAT = r"(where $\mathbb{N} = \{1, 2, 3, \dots\}$)"

# ================================================================ EASY (14)


def _c1():
    sol = solveset(x**2 - 3*x - 10 < 0, x, S.Reals)
    return len(int_points(lambda k: sol.contains(k) == True))
q("U01-A-001", "Sets and their representation", "Counting elements of a set given in set-builder form", "Easy",
  "Single-step computation MCQ",
  r"The number of elements in the set $P = \{x \in \mathbb{Z} : x^2 - 3x - 10 < 0\}$ is",
  r"$6$",
  [(r"$8$", r"Solves $x^2 - 3x - 10 \le 0$ instead of the strict inequality and counts the integers from $-2$ to $5$."),
   (r"$7$", r"Includes one endpoint, counting the integers from $-2$ to $4$."),
   (r"$4$", r"Counts only the positive integers $1, 2, 3, 4$, reading $\mathbb{Z}$ as $\mathbb{N}$.")],
  r"$x^2 - 3x - 10 = (x - 5)(x + 2) < 0$ gives $-2 < x < 5$. The integers in this open interval are $-1, 0, 1, 2, 3, 4$, so $P$ has $6$ elements.",
  "Including the endpoints of a strict inequality.",
  "U01-A-setbuilder-count", "One quadratic inequality, then counting integers.",
  check=_c1, values=[6, 8, 7, 4], cognitive="Application",
  numerical=dict(question=r"The number of elements in the set $P = \{x \in \mathbb{Z} : x^2 - 3x - 10 < 0\}$ is", answer=6))


def _c2():
    k = Symbol('k', integer=True)
    sols = [v for v in range(-200, 201) if v != 1 and Rational(12, v - 1).is_integer and Rational(12, v - 1) > 0]
    return FiniteSet(*sols)
q("U01-A-002", "Sets and their representation", "Set-builder form with a divisibility condition to roster form", "Easy",
  "Single-step computation MCQ",
  r"In roster form, the set $\left\{x \in \mathbb{Z} : \frac{12}{x - 1} \in \mathbb{N}\right\}$ " + NAT + r" is",
  r"$\{2, 3, 4, 5, 7, 13\}$",
  [(r"$\{1, 2, 3, 4, 6, 12\}$", r"Lists the positive divisors of $12$, which are the values of $x - 1$, instead of the values of $x$."),
   (r"$\{2, 3, 4, 7, 13\}$", r"Misses the divisor $4$ of $12$, so drops $x = 5$."),
   (r"$\{0, -1, -2, -3, -5, -11\}$", r"Sign slip: writes $x = 1 - d$ instead of $x = 1 + d$ for each positive divisor $d$ of $12$.")],
  r"$\frac{12}{x - 1}$ is a natural number exactly when $x - 1$ is a positive divisor of $12$, that is $x - 1 \in \{1, 2, 3, 4, 6, 12\}$. Hence $x \in \{2, 3, 4, 5, 7, 13\}$.",
  "Confusing the values of $x - 1$ with the values of $x$.",
  "U01-A-setbuilder-divisor", "One divisibility condition, then a shift to list the elements.",
  check=_c2, values=[FiniteSet(2, 3, 4, 5, 7, 13), FiniteSet(1, 2, 3, 4, 6, 12), FiniteSet(2, 3, 4, 7, 13),
                     FiniteSet(0, -1, -2, -3, -5, -11)],
  cognitive="Application")

def _c3():
    e = frozenset()
    s = e
    for _ in range(3):
        s = frozenset(subsets(s))
    return len(s)
q("U01-A-003", "Power set", "Iterated power set of the empty set", "Easy",
  "Single-step computation MCQ",
  r"If $\mathcal{P}(X)$ denotes the power set of a set $X$, then the number of elements in $\mathcal{P}(\mathcal{P}(\mathcal{P}(\emptyset)))$ is",
  r"$4$",
  [(r"$2$", r"Stops one level early: $\mathcal{P}(\mathcal{P}(\emptyset)) = \{\emptyset, \{\emptyset\}\}$ has $2$ elements."),
   (r"$8$", r"Takes $2^3$ for three applications of the power set operation."),
   (r"$16$", r"Thinks $\mathcal{P}(\emptyset)$ has $2$ elements, then $2^2 = 4$ and $2^4 = 16$.")],
  r"$\mathcal{P}(\emptyset) = \{\emptyset\}$ has $1$ element, so $\mathcal{P}(\mathcal{P}(\emptyset))$ has $2^1 = 2$ elements and $\mathcal{P}(\mathcal{P}(\mathcal{P}(\emptyset)))$ has $2^2 = 4$ elements.",
  r"Believing that $\mathcal{P}(\emptyset)$ is empty or has two elements.",
  "U01-A-power-set-empty", "Apply $n(\\mathcal{P}(X)) = 2^{n(X)}$ three times.",
  check=_c3, values=[4, 2, 8, 16], cognitive="Understanding")


def _c4():
    return sum(1 for s in subsets(range(1, 7)) if 1 in s and 2 in s and 3 not in s)
q("U01-A-004", "Subsets", "Subsets with forced and forbidden elements", "Easy",
  "Single-step computation MCQ",
  r"The number of subsets of $\{1, 2, 3, 4, 5, 6\}$ that contain both $1$ and $2$ but do not contain $3$ is",
  r"$8$",
  [(r"$16$", r"Ignores the condition on $3$ and lets the four elements $3, 4, 5, 6$ vary freely, $2^4$."),
   (r"$7$", r"Subtracts $1$ for the empty choice of the free elements, $2^3 - 1$."),
   (r"$4$", r"Miscounts the free elements as two, $2^2$.")],
  r"The elements $1$ and $2$ must be present and $3$ must be absent. Each of the remaining elements $4, 5, 6$ may or may not be included, giving $2^3 = 8$ subsets.",
  "Letting a forbidden element vary freely.",
  "U01-A-subsets-forced", "One multiplication-principle step.",
  check=_c4, values=[8, 16, 7, 4], cognitive="Application",
  numerical=dict(question=r"The number of subsets of $\{1, 2, 3, 4, 5, 6\}$ that contain both $1$ and $2$ but do not contain $3$ is", answer=8))


def _c5():
    S7 = frozenset(range(7))
    return sum(1 for s in subsets(S7) if s and s != S7)
q("U01-A-005", "Subsets", "Non-empty proper subsets", "Easy",
  "Single-step computation MCQ",
  r"A set $X$ has $7$ elements. The number of non-empty proper subsets of $X$ is",
  r"$126$",
  [(r"$127$", r"Removes only one of the two excluded subsets, $2^7 - 1$."),
   (r"$128$", r"Counts all subsets, $2^7$."),
   (r"$64$", r"Thinks a proper subset must omit a fixed element, $2^6$.")],
  r"$X$ has $2^7 = 128$ subsets. Excluding the empty set and $X$ itself leaves $128 - 2 = 126$ non-empty proper subsets.",
  "Excluding only one of the empty set and the set itself.",
  "U01-A-proper-subsets", "Direct count with two exclusions.",
  check=_c5, values=[126, 127, 128, 64], cognitive="Recall")


def _c6():
    i = Symbol('i')
    s = solve([40 + 26 - i - 50], [i], dict=True)[0]
    return 40 - s[i]
q("U01-A-006", "Venn diagrams and cardinality", "Two sets: only one set", "Easy",
  "Single-step computation MCQ",
  r"In a group of $50$ students, every student plays at least one of chess and carrom. If $40$ students play chess and $26$ play carrom, the number of students who play chess but not carrom is",
  r"$24$",
  [(r"$16$", r"Stops at the number who play both, $40 + 26 - 50$."),
   (r"$10$", r"Finds the number who play carrom but not chess, $26 - 16$."),
   (r"$14$", r"Subtracts the two set sizes, $40 - 26$.")],
  r"Since every student plays at least one game, $n(\text{chess} \cup \text{carrom}) = 50$, so $n(\text{both}) = 40 + 26 - 50 = 16$. Hence chess but not carrom is $40 - 16 = 24$.",
  "Confusing the intersection with the 'only' region.",
  "U01-A-venn2-only", "Inclusion and exclusion once, then one subtraction.",
  check=_c6, values=[24, 16, 10, 14], cognitive="Application")


def _c7():
    Uu = FiniteSet(*range(1, 11))
    P = FiniteSet(*[k for k in range(1, 11) if k % 2 == 0])
    Q = FiniteSet(*[k for k in range(1, 11) if isprime(k)])
    return Complement(Uu, Union(P, Q))
q("U01-A-007", "Operations on sets", "Complement of a union", "Easy",
  "Single-step computation MCQ",
  r"Let $U = \{1, 2, 3, \dots, 10\}$ be the universal set, $P = \{x \in U : x \text{ is even}\}$ and $Q = \{x \in U : x \text{ is prime}\}$. Then $(P \cup Q)'$ is",
  r"$\{1, 9\}$",
  [(r"$\{9\}$", r"Treats $1$ as a prime number."),
   (r"$\{1\}$", r"Treats $9$ as a prime number."),
   (r"$\{1, 3, 5, 7, 9\}$", r"Finds $P'$ only, ignoring $Q$.")],
  r"$P = \{2, 4, 6, 8, 10\}$ and $Q = \{2, 3, 5, 7\}$, so $P \cup Q = \{2, 3, 4, 5, 6, 7, 8, 10\}$ and $(P \cup Q)' = \{1, 9\}$.",
  "Misclassifying $1$ or $9$ as prime.",
  "U01-A-complement-union", "Two small sets, one union and one complement.",
  check=_c7, values=[FiniteSet(1, 9), FiniteSet(9), FiniteSet(1), FiniteSet(1, 3, 5, 7, 9)],
  cognitive="Application")


def _c8():
    P = int_points(lambda k: k**2 <= 9, -20, 20)
    Q = int_points(lambda k: 0 <= k <= 5, -20, 20)
    return Union(Complement(P, Q), Complement(Q, P))
q("U01-A-008", "Operations on sets", "Symmetric difference of two integer sets", "Easy",
  "Single-step computation MCQ",
  r"Let $P = \{x \in \mathbb{Z} : x^2 \le 9\}$ and $Q = \{x \in \mathbb{Z} : 0 \le x \le 5\}$. Then $(P - Q) \cup (Q - P)$ is",
  r"$\{-3, -2, -1, 4, 5\}$",
  [(r"$\{-3, -2, -1\}$", r"Finds $P - Q$ only and omits $Q - P$."),
   (r"$\{0, 1, 2, 3\}$", r"Finds $P \cap Q$, the elements common to both."),
   (r"$\{-3, -2, -1, 0, 4, 5\}$", r"Overlooks that $0 \in Q$ and keeps $0$ in $P - Q$.")],
  r"$P = \{-3, -2, -1, 0, 1, 2, 3\}$ and $Q = \{0, 1, 2, 3, 4, 5\}$. Then $P - Q = \{-3, -2, -1\}$ and $Q - P = \{4, 5\}$, so the union is $\{-3, -2, -1, 4, 5\}$.",
  "Computing only one of the two differences.",
  "U01-A-symmetric-difference", "List two sets and take two differences.",
  check=_c8, values=[FiniteSet(-3, -2, -1, 4, 5), FiniteSet(-3, -2, -1), FiniteSet(0, 1, 2, 3),
                     FiniteSet(-3, -2, -1, 0, 4, 5)], cognitive="Application")


def _c9():
    s0 = solveset(x**2 + 2*x + 3, x, S.Reals)
    s1 = solveset(x**3 + 4*x, x, S.Reals)
    s2 = int_points(lambda k: 2 < k**2 < 5, -20, 20)
    s3 = int_points(lambda k: k**2 < 2, -20, 20)
    sizes = [len(s0), len(s1), len(s2), len(s3)]
    assert sizes.count(0) == 1
    return sizes[0]
q("U01-A-009", "Sets and their representation", "Recognising the empty set", "Easy",
  "Conceptual/application MCQ",
  r"Which of the following sets is the empty set?",
  r"$\{x \in \mathbb{R} : x^2 + 2x + 3 = 0\}$",
  [(r"$\{x \in \mathbb{R} : x^3 + 4x = 0\}$", r"Cancels $x$ to get $x^2 = -4$ and concludes there is no real solution, losing $x = 0$; the set is $\{0\}$."),
   (r"$\{x \in \mathbb{Z} : 2 < x^2 < 5\}$", r"Overlooks the perfect square $4$ between $2$ and $5$; the set is $\{-2, 2\}$."),
   (r"$\{x \in \mathbb{Z} : x^2 < 2\}$", r"Thinks no integer works because $\sqrt{2}$ is irrational, overlooking $-1, 0, 1$.")],
  r"For $x^2 + 2x + 3 = 0$ the discriminant is $4 - 12 = -8 < 0$, so there is no real root and the set is empty. The other sets are $\{0\}$, $\{-2, 2\}$ and $\{-1, 0, 1\}$, all non-empty.",
  "Cancelling a variable factor and losing the zero solution.",
  "U01-A-empty-set", "Check four small sets; one discriminant.",
  check=_c9, values=[0, 1, 2, 3], cognitive="Understanding")

q("U01-A-010", "Operations on sets", "Union equal to intersection", "Easy",
  "Direct concept MCQ",
  r"If $P$ and $Q$ are sets such that $P \cup Q = P \cap Q$, then which of the following must be true?",
  r"$P = Q$",
  [(r"$P \subsetneq Q$", r"Reads the condition as only $P \subseteq Q$ and assumes the inclusion is strict."),
   (r"$Q = \emptyset$", r"Tests only the case $P = Q = \emptyset$ and generalises from it."),
   (r"$P \cap Q = \emptyset$", r"Confuses the condition with disjointness of the sets.")],
  r"Always $P \cap Q \subseteq P \subseteq P \cup Q$. If $P \cup Q = P \cap Q$, the chain forces $P = P \cap Q$, and similarly $Q = P \cap Q$. Hence $P = Q$; conversely $P = Q$ makes the condition hold, so nothing more is forced.",
  "Generalising from the special case of empty sets.",
  "U01-A-union-equals-intersection", "One sandwich argument with the basic inclusions.",
  cognitive="Understanding")


def _c11():
    return identity_index(lambda U, P, Q: (P | Q) & (P | (U - Q)),
                          [lambda U, P, Q: P, lambda U, P, Q: U,
                           lambda U, P, Q: frozenset(), lambda U, P, Q: P | Q])
q("U01-A-011", "Algebra of sets", "Simplification using distributive and complement laws", "Easy",
  "Single-step computation MCQ",
  r"For any two subsets $P$ and $Q$ of a universal set $U$, the set $(P \cup Q) \cap (P \cup Q')$ equals",
  r"$P$",
  [(r"$U$", r"Writes the expression as $P \cup (Q \cup Q') = U$, using union in place of intersection inside."),
   (r"$\emptyset$", r"Notes $Q \cap Q' = \emptyset$ and drops $P$ altogether."),
   (r"$P \cup Q$", r"Stops after observing that the expression is contained in $P \cup Q$.")],
  r"By the distributive law, $(P \cup Q) \cap (P \cup Q') = P \cup (Q \cap Q') = P \cup \emptyset = P$.",
  "Misapplying the distributive law of union over intersection.",
  "U01-A-law-distributive", "One distributive step and one complement law.",
  check=_c11, values=[0, 1, 2, 3], cognitive="Application")


def _c12():
    N = 10000
    pct = Rational(65, 100) + Rational(40, 100) - Rational(20, 100)
    return N * (1 - pct)
q("U01-A-012", "Venn diagrams and cardinality", "Two sets: neither, from percentages", "Easy",
  "Single-step computation MCQ",
  r"In a town of $10000$ people, $65\%$ read newspaper $X$, $40\%$ read newspaper $Y$ and $20\%$ read both. The number of people who read neither newspaper is",
  r"$1500$",
  [(r"$3500$", r"Finds the people who do not read $X$, $35\%$ of $10000$."),
   (r"$6000$", r"Finds the people who do not read $Y$, $60\%$ of $10000$."),
   (r"$4500$", r"Finds the people who read only $X$, $65\% - 20\%$.")],
  r"The percentage reading at least one is $65 + 40 - 20 = 85$, so $15\%$ read neither, that is $\frac{15}{100} \times 10000 = 1500$ people.",
  "Taking the complement of one set instead of the union.",
  "U01-A-venn2-neither", "One application of $n(X \\cup Y)$ and a complement.",
  check=_c12, values=[1500, 3500, 6000, 4500], cognitive="Application")


def _c13():
    sol = solveset(Abs(x - 2) < 3, x, S.Reals)
    n = len(int_points(lambda k: sol.contains(k) == True))
    return 2**n
q("U01-A-013", "Power set", "Size of the power set of a set given by a condition", "Easy",
  "Single-step computation MCQ",
  r"If $P = \{x \in \mathbb{Z} : |x - 2| < 3\}$, then the number of elements in the power set of $P$ is",
  r"$32$",
  [(r"$128$", r"Uses $|x - 2| \le 3$, so $P$ has $7$ elements and $2^7 = 128$."),
   (r"$64$", r"Includes one endpoint of $-1 < x < 5$, so takes $6$ elements and $2^6 = 64$."),
   (r"$25$", r"Uses $n^2$ in place of $2^n$ with $n = 5$.")],
  r"$|x - 2| < 3$ gives $-1 < x < 5$, so $P = \{0, 1, 2, 3, 4\}$ with $5$ elements. Its power set has $2^5 = 32$ elements.",
  r"Using $n^2$ for the size of a power set, or including endpoints of a strict inequality.",
  "U01-A-power-set-size", "One modulus inequality and $2^n$.",
  check=_c13, values=[32, 128, 64, 25], cognitive="Application")

q("U01-A-014", "Sets and their representation", "Membership versus subset", "Easy",
  "Direct concept MCQ",
  r"Let $P = \{1, \{2\}, \{1, 2\}\}$. Which of the following is true?",
  r"$\{2\} \in P$",
  [(r"$\{2\} \subseteq P$", r"Confuses membership with inclusion; $\{2\} \subseteq P$ would need $2 \in P$."),
   (r"$2 \in P$", r"Looks inside the element $\{2\}$ and treats $2$ itself as an element of $P$."),
   (r"$\{1, 2\} \subseteq P$", r"Sees $\{1, 2\}$ listed in $P$ and reads membership as inclusion; this would need $2 \in P$.")],
  r"The elements of $P$ are $1$, $\{2\}$ and $\{1, 2\}$. So $\{2\} \in P$ is true. Since $2$ itself is not an element of $P$, both $\{2\} \subseteq P$ and $\{1, 2\} \subseteq P$ fail, and $2 \in P$ is false.",
  r"Confusing $\in$ with $\subseteq$ for sets whose elements are sets.",
  "U01-A-member-vs-subset", "One careful reading of the roster.",
  cognitive="Understanding")

# ================================================================ MEDIUM (21)


def _c15():
    d = venn3(45, 40, 35, 15, 12, 10, 5)
    return 100 - sum(d.values())
q("U01-A-015", "Venn diagrams and cardinality", "Three sets: none of the three", "Medium",
  "Multi-step computation MCQ",
  r"In a survey of $100$ students, $45$ study Mathematics, $40$ study Physics and $35$ study Chemistry; $15$ study Mathematics and Physics, $12$ study Physics and Chemistry, $10$ study Mathematics and Chemistry, and $5$ study all three. The number of students who study none of the three subjects is",
  r"$12$",
  [(r"$17$", r"Omits the $+5$ term for all three, getting a union of $83$."),
   (r"$22$", r"Subtracts the triple intersection instead of adding it, getting a union of $78$."),
   (r"$7$", r"Adds the triple intersection twice, getting a union of $93$.")],
  r"$n(\text{at least one}) = 45 + 40 + 35 - 15 - 12 - 10 + 5 = 88$. Hence $100 - 88 = 12$ students study none of the subjects.",
  "Mishandling the sign of the triple intersection in three-set inclusion and exclusion.",
  "U01-A-venn3-none", "Full three-set inclusion and exclusion, then a complement.",
  check=_c15, values=[12, 17, 22, 7], cognitive="Application",
  numerical=dict(question=r"In a survey of $100$ students, $45$ study Mathematics, $40$ study Physics and $35$ study Chemistry; $15$ study Mathematics and Physics, $12$ study Physics and Chemistry, $10$ study Mathematics and Chemistry, and $5$ study all three. The number of students who study none of the three subjects is", answer=12))


def _c16():
    d = venn3(50, 40, 30, 20, 15, 12, 8)
    return d['a'] + d['b'] + d['c']
q("U01-A-016", "Venn diagrams and cardinality", "Three sets: exactly one", "Medium",
  "Multi-step computation MCQ",
  r"In a housing society, $50$ families read newspaper $X$, $40$ read $Y$ and $30$ read $Z$. Also $20$ read $X$ and $Y$, $15$ read $Y$ and $Z$, $12$ read $X$ and $Z$, and $8$ read all three. The number of families that read exactly one of the three newspapers is",
  r"$50$",
  [(r"$81$", r"Finds the number reading at least one, $120 - 47 + 8$."),
   (r"$34$", r"Uses $\sum n - 2\sum n(\text{pairs}) + n(\text{all})$, adding the triple once instead of three times."),
   (r"$26$", r"Finds only-$X$ as $50 - 20 - 12$ and so on, forgetting to add back the $8$ in each.")],
  r"Only $X$: $50 - 20 - 12 + 8 = 26$; only $Y$: $40 - 20 - 15 + 8 = 13$; only $Z$: $30 - 15 - 12 + 8 = 11$. Exactly one is $26 + 13 + 11 = 50$. Equivalently $\sum n - 2\sum n(\text{pairs}) + 3n(\text{all}) = 120 - 94 + 24 = 50$.",
  "Subtracting the pairwise overlaps without adding back the triple region.",
  "U01-A-venn3-exactly-one", "Region-by-region Venn counting with three sets.",
  check=_c16, values=[50, 81, 34, 26], cognitive="Application")


def _c17():
    vals = [k for k in range(0, 61) if 42 - k >= 0 and 35 - k >= 0 and 60 - (77 - k) >= 0]
    return max(vals) - min(vals)
q("U01-A-017", "Venn diagrams and cardinality", "Two sets: range of the overlap", "Medium",
  "Multi-step computation MCQ",
  r"In a class of $60$ students, $42$ like tea and $35$ like coffee. If $M$ and $m$ are the greatest and least possible numbers of students who like both drinks, then $M - m$ equals",
  r"$18$",
  [(r"$35$", r"Takes the least possible overlap as $0$, ignoring that $42 + 35 > 60$."),
   (r"$25$", r"Takes the greatest overlap as $42$, the larger set, and the least as $17$."),
   (r"$7$", r"Subtracts the set sizes, $42 - 35$.")],
  r"Let $k$ like both. Then $k \le \min(42, 35) = 35$, and $n(\text{tea} \cup \text{coffee}) = 77 - k \le 60$ gives $k \ge 17$. Both bounds are attained, so $M = 35$, $m = 17$ and $M - m = 18$.",
  "Forgetting that the union cannot exceed the class size.",
  "U01-A-venn2-overlap-range", "Two bounds from two different constraints.",
  check=_c17, values=[18, 35, 25, 7], cognitive="Analysis",
  numerical=dict(question=r"In a class of $60$ students, $42$ like tea and $35$ like coffee. If $M$ and $m$ are the greatest and least possible numbers of students who like both drinks, then $M - m$ is", answer=18))


def _c18():
    s1 = always(lambda U, P, Q, R: P - (Q | R) == (P - Q) & (P - R), 3)
    s2 = always(lambda U, P, Q, R: P - (Q & R) == (P - Q) & (P - R), 3)
    return (s1, s2)
q("U01-A-018", "Algebra of sets", "De Morgan laws for set difference", "Medium",
  "Statement-based MCQ",
  r"Let $P$, $Q$, $R$ be any three sets. Statement I: $P - (Q \cup R) = (P - Q) \cap (P - R)$. Statement II: $P - (Q \cap R) = (P - Q) \cap (P - R)$." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II by analogy with Statement I, not switching $\cap$ to $\cup$."),
   (ST_FF, r"Thinks a difference never distributes over a union."),
   (ST_FT, "Swaps the two De Morgan forms.")],
  r"$x \in P - (Q \cup R)$ means $x \in P$, $x \notin Q$ and $x \notin R$, which is exactly $x \in (P - Q) \cap (P - R)$; so Statement I is true. By De Morgan, $P - (Q \cap R) = (P - Q) \cup (P - R)$. For $P = \{1, 2\}$, $Q = \{1\}$, $R = \{2\}$ we get $P - (Q \cap R) = \{1, 2\}$ but $(P - Q) \cap (P - R) = \emptyset$, so Statement II is false.",
  "Not switching intersection and union when applying De Morgan's law.",
  "U01-A-stmt-difference-demorgan", "One proof and one counterexample.",
  check=_c18, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Analysis")


def _c19():
    S = list(range(1, 11))
    return sum(1 for m in range(1 << 10) if any((m >> (k - 1)) & 1 and k % 2 == 1 for k in S))
q("U01-A-019", "Subsets", "Subsets containing at least one element of a kind", "Medium",
  "Single-step computation MCQ",
  r"The number of subsets of $\{1, 2, 3, \dots, 10\}$ that contain at least one odd number is",
  r"$992$",
  [(r"$1023$", r"Counts the non-empty subsets, $2^{10} - 1$."),
   (r"$31$", r"Counts only the non-empty sets of odd numbers, $2^5 - 1$, ignoring the free choice of even numbers."),
   (r"$512$", r"Assumes exactly half of all subsets contain an odd number.")],
  r"Subsets with no odd number are the subsets of $\{2, 4, 6, 8, 10\}$, and there are $2^5 = 32$ of them. Hence $2^{10} - 2^5 = 1024 - 32 = 992$ subsets contain at least one odd number.",
  "Ignoring the free choice of the other elements, or counting non-empty subsets.",
  "U01-A-subsets-at-least-one", "Complementary counting on subsets.",
  check=_c19, values=[992, 1023, 31, 512], cognitive="Application")


def _c20():
    pw = lambda S: frozenset(subsets(S))
    s1 = always(lambda U, X, Y: pw(X) | pw(Y) == pw(X | Y), 2)
    s2 = always(lambda U, X, Y: pw(X) & pw(Y) == pw(X & Y), 2)
    return (s1, s2)
q("U01-A-020", "Power set", "Power set of a union and of an intersection", "Medium",
  "Statement-based MCQ",
  r"For a set $X$, let $\mathcal{P}(X)$ denote its power set. Let $X$ and $Y$ be any two sets. Statement I: $\mathcal{P}(X) \cup \mathcal{P}(Y) = \mathcal{P}(X \cup Y)$. Statement II: $\mathcal{P}(X) \cap \mathcal{P}(Y) = \mathcal{P}(X \cap Y)$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Assumes the power set respects union as it respects intersection."),
   (ST_FF, r"Doubts Statement II, not seeing that $S \subseteq X$ and $S \subseteq Y$ is the same as $S \subseteq X \cap Y$."),
   (ST_TF, "Reverses the truth values of the two statements.")],
  r"$S \in \mathcal{P}(X) \cap \mathcal{P}(Y)$ means $S \subseteq X$ and $S \subseteq Y$, that is $S \subseteq X \cap Y$; so Statement II is true. For $X = \{1\}$, $Y = \{2\}$, the set $\{1, 2\}$ lies in $\mathcal{P}(X \cup Y)$ but in neither $\mathcal{P}(X)$ nor $\mathcal{P}(Y)$, so Statement I is false.",
  r"Believing $\mathcal{P}$ distributes over union.",
  "U01-A-stmt-power-set-ops", "A proof and a counterexample with power sets.",
  check=_c20, values=[(False, True), (True, True), (False, False), (True, False)],
  cognitive="Analysis")


def _c21():
    nI = log(4, 2)
    return 2**(5 + 4 - nI)
q("U01-A-021", "Power set", "Power set of a union from given cardinalities", "Medium",
  "Multi-step computation MCQ",
  r"Let $X$ and $Y$ be finite sets with $n(X) = 5$ and $n(Y) = 4$. If the power set of $X \cap Y$ has $4$ elements, then the number of elements in the power set of $X \cup Y$ is",
  r"$128$",
  [(r"$512$", r"Ignores the common elements and takes $n(X \cup Y) = 9$."),
   (r"$32$", r"Uses $4$ itself as $n(X \cap Y)$, so $n(X \cup Y) = 5$."),
   (r"$44$", r"Applies inclusion and exclusion to the power set sizes, $2^5 + 2^4 - 4$.")],
  r"$2^{n(X \cap Y)} = 4$ gives $n(X \cap Y) = 2$. Then $n(X \cup Y) = 5 + 4 - 2 = 7$ and its power set has $2^7 = 128$ elements.",
  "Confusing the size of a power set with the size of the set.",
  "U01-A-power-set-union", "Logarithm of a power set size, inclusion and exclusion, then $2^n$.",
  check=_c21, values=[128, 512, 32, 44], cognitive="Application",
  numerical=dict(question=r"Let $X$ and $Y$ be finite sets with $n(X) = 5$ and $n(Y) = 4$. If the power set of $X \cap Y$ has $4$ elements, then the number of elements in the power set of $X \cup Y$ is", answer=128))


def _c22():
    P = solveset(x**2 - 5*Abs(x) + 6, x, S.Reals)
    Q = solveset(x**2 - x - 6 <= 0, x, S.Reals)
    return Intersection(P, Q)
q("U01-A-022", "Operations on sets", "Intersection of a solution set and an interval", "Medium",
  "Multi-step computation MCQ",
  r"Let $P = \{x \in \mathbb{R} : x^2 - 5|x| + 6 = 0\}$ and $Q = \{x \in \mathbb{R} : x^2 - x - 6 \le 0\}$. Then $P \cap Q$ is",
  r"$\{-2, 2, 3\}$",
  [(r"$\{2, 3\}$", r"Solves $x^2 - 5x + 6 = 0$ only, dropping the negative roots coming from $|x|$."),
   (r"$\{-3, -2, 2, 3\}$", r"Finds $P$ correctly but does not intersect with $Q$, keeping $-3$."),
   (r"$\{-2, 3\}$", r"Lists only the boundary points of $Q$ that appear in $P$, ignoring the interior point $2$.")],
  r"$|x|^2 - 5|x| + 6 = 0$ gives $|x| = 2$ or $3$, so $P = \{-3, -2, 2, 3\}$. Also $(x - 3)(x + 2) \le 0$ gives $Q = [-2, 3]$. Hence $P \cap Q = \{-2, 2, 3\}$.",
  r"Forgetting the negative solutions of an equation in $|x|$.",
  "U01-A-intersection-modulus", "Equation in $|x|$ combined with a quadratic inequality.",
  check=_c22, values=[FiniteSet(-2, 2, 3), FiniteSet(2, 3), FiniteSet(-3, -2, 2, 3), FiniteSet(-2, 3)],
  cognitive="Application")


def _c23():
    P = Interval.Ropen(-2, 3)
    Q = Interval.Lopen(1, 5)
    return Complement(P, Q)
q("U01-A-023", "Operations on sets", "Difference of intervals", "Medium",
  "Single-step computation MCQ",
  r"Let $P = [-2, 3)$ and $Q = (1, 5]$ be subsets of $\mathbb{R}$. Then $P - Q$ is",
  r"$[-2, 1]$",
  [(r"$[-2, 1)$", r"Excludes $1$, overlooking that $1 \notin Q$ because $Q$ is open at $1$."),
   (r"$(1, 3)$", r"Finds $P \cap Q$ instead of $P - Q$."),
   (r"$[3, 5]$", r"Finds $Q - P$ instead of $P - Q$.")],
  r"$P - Q$ consists of points of $[-2, 3)$ not in $(1, 5]$. Points of $P$ greater than $1$ lie in $Q$, while $1$ itself does not lie in $Q$. Hence $P - Q = [-2, 1]$.",
  "Mishandling open and closed endpoints when removing an interval.",
  "U01-A-interval-difference", "Endpoint bookkeeping for a set difference.",
  check=_c23, values=[Interval(-2, 1), Interval.Ropen(-2, 1), Interval.open(1, 3), Interval(3, 5)],
  cognitive="Application")


def _c24():
    return identity_index(lambda U, P, Q: (P & (U - Q)) | ((U - P) & (U - Q)) | (P & Q),
                          [lambda U, P, Q: P | (U - Q), lambda U, P, Q: P & (U - Q),
                           lambda U, P, Q: U, lambda U, P, Q: U - Q])
q("U01-A-024", "Algebra of sets", "Union of Venn regions in set notation", "Medium",
  "Conceptual/application MCQ",
  r"For subsets $P$ and $Q$ of a universal set $U$, the set $(P \cap Q') \cup (P' \cap Q') \cup (P \cap Q)$ equals",
  r"$P \cup Q'$",
  [(r"$P \cap Q'$", r"Keeps only the first term, treating the other two as contained in it."),
   (r"$U$", r"Assumes the three pieces exhaust the Venn diagram, forgetting the region $Q - P$."),
   (r"$Q'$", r"Combines the first two terms to $Q'$ correctly but then drops $P \cap Q$.")],
  r"$(P \cap Q') \cup (P' \cap Q') = (P \cup P') \cap Q' = Q'$. Then $Q' \cup (P \cap Q) = (Q' \cup P) \cap (Q' \cup Q) = P \cup Q'$. In Venn terms, every region except $Q - P$ is included, and $(Q - P)' = P \cup Q'$.",
  "Assuming the listed regions cover the whole universal set.",
  "U01-A-law-regions", "Two distributive steps or a four-region Venn reading.",
  check=_c24, values=[0, 1, 2, 3], cognitive="Analysis")


def _c25():
    nQ, nP = symbols('nQ nP')
    s = solve([nP - 2*nQ, nP + nQ - 10 - 50], [nP, nQ], dict=True)[0]
    return s[nP] - 10
q("U01-A-025", "Venn diagrams and cardinality", "Two sets: reversed unknown with a ratio", "Medium",
  "Inverse/parameter MCQ",
  r"For finite sets $P$ and $Q$, $n(P) = 2\,n(Q)$, $n(P \cap Q) = 10$ and $n(P \cup Q) = 50$. Then $n(P - Q)$ equals",
  r"$30$",
  [(r"$40$", r"Stops at $n(P)$ without removing the common elements."),
   (r"$20$", r"Reports $n(Q)$, the first unknown found."),
   (r"$10$", r"Finds $n(Q - P) = 20 - 10$ instead of $n(P - Q)$.")],
  r"Let $n(Q) = k$, so $n(P) = 2k$. Then $50 = 2k + k - 10$ gives $k = 20$ and $n(P) = 40$. Hence $n(P - Q) = 40 - 10 = 30$.",
  "Reporting an intermediate quantity instead of the asked difference.",
  "U01-A-venn2-ratio", "Set up and solve one linear equation, then subtract.",
  check=_c25, values=[30, 40, 20, 10], cognitive="Application")


def _c26():
    vals = set()
    for k in range(0, 11):
        vals.add(10 + 15 - k)
    return len(vals)
q("U01-A-026", "Venn diagrams and cardinality", "Possible sizes of a union", "Medium",
  "Multi-step computation MCQ",
  r"$P$ and $Q$ are finite sets with $n(P) = 10$ and $n(Q) = 15$. The number of different possible values of $n(P \cup Q)$ is",
  r"$11$",
  [(r"$10$", r"Counts $25 - 15$, missing one endpoint of the range $15$ to $25$."),
   (r"$16$", r"Takes the least possible union as $10$ instead of $15$."),
   (r"$25$", r"Counts values from $1$ to $25$, ignoring that the union contains $Q$.")],
  r"$n(P \cup Q) = 25 - n(P \cap Q)$ and $0 \le n(P \cap Q) \le 10$, with every value possible. So $n(P \cup Q)$ takes the values $15, 16, \dots, 25$, which are $11$ values.",
  "Off-by-one when counting the integers in a closed range.",
  "U01-A-union-size-range", "Bound the intersection, then count integers in a range.",
  check=_c26, values=[11, 10, 16, 25], cognitive="Analysis",
  numerical=dict(question=r"$P$ and $Q$ are finite sets with $n(P) = 10$ and $n(Q) = 15$. The number of different possible values of $n(P \cup Q)$ is", answer=11))


def _c27():
    S = subsets(range(1, 5))
    return sum(1 for P in S for Q in S if P <= Q)
q("U01-A-027", "Subsets", "Ordered pairs of nested subsets", "Medium",
  "Multi-step computation MCQ",
  r"The number of ordered pairs $(P, Q)$ of subsets of $\{1, 2, 3, 4\}$ such that $P \subseteq Q$ is",
  r"$81$",
  [(r"$256$", r"Counts all ordered pairs of subsets, $16 \times 16$, ignoring the condition."),
   (r"$65$", r"Treats $\subseteq$ as proper inclusion and removes the $16$ pairs with $P = Q$."),
   (r"$16$", r"Counts only the choices of $Q$.")],
  r"For each element there are exactly three admissible options: in neither set, in $Q$ only, or in both. Since $P \subseteq Q$ forbids being in $P$ only, the count is $3^4 = 81$.",
  "Not recognising the three-choices-per-element structure.",
  "U01-A-nested-subset-pairs", "Element-wise counting with a restriction.",
  check=_c27, values=[81, 256, 65, 16], cognitive="Analysis",
  numerical=dict(question=r"The number of ordered pairs $(P, Q)$ of subsets of $\{1, 2, 3, 4\}$ such that $P \subseteq Q$ is", answer=81))


def _c28():
    s1 = always(lambda U, P, Q, R: not ((P & Q) == (P & R) and (P | Q) == (P | R)) or Q == R, 3)
    s2 = always(lambda U, P, Q: (P <= Q) == (len(P & (U - Q)) == 0), 2)
    return (s1, s2)
q("U01-A-028", "Algebra of sets", "Cancellation and subset characterisation", "Medium",
  "Statement-based MCQ",
  r"Let $P$, $Q$, $R$ be subsets of a universal set $U$. Statement I: If $P \cap Q = P \cap R$ and $P \cup Q = P \cup R$, then $Q = R$. Statement II: $P \subseteq Q$ if and only if $P \cap Q' = \emptyset$." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Thinks Statement II fails in one direction, for example when $P = \emptyset$."),
   (ST_FT, r"Recalls that neither condition alone allows cancellation and wrongly extends this to both together."),
   (ST_FF, r"Rejects both, testing Statement I with only one of its two conditions.")],
  r"For Statement I, $Q = Q \cap (P \cup Q) = Q \cap (P \cup R) = (Q \cap P) \cup (Q \cap R) = (P \cap R) \cup (Q \cap R) = R \cap (P \cup Q) = R \cap (P \cup R) = R$; so it is true. For Statement II, $P \cap Q' = \emptyset$ says no element of $P$ lies outside $Q$, which is exactly $P \subseteq Q$; so it is true.",
  "Believing set equations can never be cancelled.",
  "U01-A-stmt-cancellation", "A chain of laws for one statement and a definition check for the other.",
  check=_c28, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Analysis")


def _c29():
    nPc, nQc, nNone, N = 25, 30, 10, 60
    nP, nQ = N - nPc, N - nQc
    return nP + nQ - (N - nNone)
q("U01-A-029", "Venn diagrams and cardinality", "Working with complements and De Morgan", "Medium",
  "Multi-step computation MCQ",
  r"$P$ and $Q$ are subsets of a universal set $U$ with $n(U) = 60$, $n(P') = 25$, $n(Q') = 30$ and $n(P' \cap Q') = 10$. Then $n(P \cap Q)$ equals",
  r"$15$",
  [(r"$5$", r"Uses $n(P') = 25$ and $n(Q') = 30$ as $n(P)$ and $n(Q)$, with $n(P \cup Q) = 50$."),
   (r"$10$", r"Takes $n(P \cap Q) = n(P' \cap Q')$."),
   (r"$20$", r"Takes $n(P \cup Q) = n(P' \cup Q') = 45$, then $35 + 30 - 45$.")],
  r"$n(P) = 35$ and $n(Q) = 30$. By De Morgan, $P' \cap Q' = (P \cup Q)'$, so $n(P \cup Q) = 60 - 10 = 50$. Hence $n(P \cap Q) = 35 + 30 - 50 = 15$.",
  "Mixing up a set with its complement under De Morgan's law.",
  "U01-A-venn2-complements", "De Morgan, two complements and inclusion and exclusion.",
  check=_c29, values=[15, 5, 10, 20], cognitive="Application")


def _c30():
    S = subsets(range(1, 6))
    return sum(1 for P in S for Q in S if P & Q == frozenset({2}) and P | Q == frozenset({1, 2, 3, 4}))
q("U01-A-030", "Operations on sets", "Counting pairs with given union and intersection", "Medium",
  "Multi-step computation MCQ",
  r"The number of ordered pairs $(P, Q)$ of subsets of $\{1, 2, 3, 4, 5\}$ such that $P \cap Q = \{2\}$ and $P \cup Q = \{1, 2, 3, 4\}$ is",
  r"$8$",
  [(r"$16$", r"Lets the element $2$ also vary, using $2^4$."),
   (r"$27$", r"Allows three choices for each of $1, 3, 4$, including being in both sets."),
   (r"$4$", r"Divides by $2$, counting unordered pairs.")],
  r"$2$ must lie in both sets and $5$ in neither. Each of $1, 3, 4$ lies in the union but not the intersection, so it is in exactly one of $P$, $Q$: $2$ choices each. The count is $2^3 = 8$.",
  "Allowing extra elements into the intersection.",
  "U01-A-pairs-union-intersection", "Element-wise analysis with two constraints.",
  check=_c30, values=[8, 16, 27, 4], cognitive="Analysis")


def _c31():
    sets = [FiniteSet(*range(n, 3*n + 1)) for n in range(4, 10)]
    return len(Intersection(*sets))
q("U01-A-031", "Operations on sets", "Intersection of an indexed family", "Medium",
  "Multi-step computation MCQ",
  r"For each $n \in \mathbb{N}$, let $P_n = \{x \in \mathbb{N} : n \le x \le 3n\}$. The number of elements in $P_4 \cap P_5 \cap P_6 \cap P_7 \cap P_8 \cap P_9$ is",
  r"$4$",
  [(r"$3$", r"Computes $12 - 9$ for the integers from $9$ to $12$, missing one."),
   (r"$6$", r"Counts the number of sets being intersected."),
   (r"$24$", r"Finds the union $\{4, 5, \dots, 27\}$ instead of the intersection.")],
  r"The intersection consists of $x$ with $x \ge \max n = 9$ and $x \le \min 3n = 12$, that is $\{9, 10, 11, 12\}$, which has $4$ elements.",
  "Confusing the largest lower bound with the smallest upper bound.",
  "U01-A-indexed-family", "Reduce a family of conditions to two bounds.",
  check=_c31, values=[4, 3, 6, 24], cognitive="Application")


def _c32():
    d = venn3(20, 25, 18, 8, 10, 7, 4)
    return d['a'] + d['b'] + d['pq']
q("U01-A-032", "Venn diagrams and cardinality", "Three sets: union of two outside the third", "Medium",
  "Multi-step computation MCQ",
  r"For finite sets $P$, $Q$, $R$: $n(P) = 20$, $n(Q) = 25$, $n(R) = 18$, $n(P \cap Q) = 8$, $n(Q \cap R) = 10$, $n(P \cap R) = 7$ and $n(P \cap Q \cap R) = 4$. Then $n((P \cup Q) \cap R')$ equals",
  r"$24$",
  [(r"$20$", r"Adds only-$P$ and only-$Q$, $9 + 11$, missing the part of $P \cap Q$ outside $R$."),
   (r"$28$", r"Includes the triple region, $24 + 4$."),
   (r"$37$", r"Finds $n(P \cup Q)$ and does not remove $R$.")],
  r"$n(P \cup Q) = 20 + 25 - 8 = 37$ and $n((P \cup Q) \cap R) = n(P \cap R) + n(Q \cap R) - n(P \cap Q \cap R) = 7 + 10 - 4 = 13$. Hence $n((P \cup Q) \cap R') = 37 - 13 = 24$.",
  r"Missing the region $P \cap Q \cap R'$.",
  "U01-A-venn3-region", "Two inclusion and exclusion steps on related sets.",
  check=_c32, values=[24, 20, 28, 37], cognitive="Analysis")


def _c33():
    P = {(s[x], s[y]) for s in solve([x**2 + y**2 - 25, y - x**2 + 5], [x, y], dict=True)}
    return len(P)
q("U01-A-033", "Operations on sets", "Intersection of point sets", "Medium",
  "Multi-step computation MCQ",
  r"Let $P = \{(x, y) \in \mathbb{R} \times \mathbb{R} : x^2 + y^2 = 25\}$ and $Q = \{(x, y) \in \mathbb{R} \times \mathbb{R} : y = x^2 - 5\}$. The number of elements in $P \cap Q$ is",
  r"$3$",
  [(r"$4$", r"Assumes a circle and a parabola meet in four points, counting the double root $x = 0$ twice."),
   (r"$2$", r"Divides $x^4 - 9x^2 = 0$ by $x^2$ and loses $x = 0$."),
   (r"$1$", r"Notices only the vertex $(0, -5)$ of the parabola on the circle and assumes the curves just touch there.")],
  r"Substituting $y = x^2 - 5$: $x^2 + (x^2 - 5)^2 = 25$, so $x^4 - 9x^2 = 0$, giving $x = 0, \pm 3$. The points are $(0, -5)$, $(3, 4)$, $(-3, 4)$, so $P \cap Q$ has $3$ elements.",
  "Dividing by a variable factor and losing a solution.",
  "U01-A-point-sets", "Substitution, a biquadratic and a count of distinct points.",
  check=_c33, values=[3, 4, 2, 1], cognitive="Application")


def _c34():
    return sum(1 for s in subsets(range(1, 7)) if sum(s) % 2 == 0)
q("U01-A-034", "Subsets", "Subsets with even element sum", "Medium",
  "Multi-step computation MCQ",
  r"The number of subsets of $\{1, 2, 3, 4, 5, 6\}$ (including the empty set) whose elements have an even sum is",
  r"$32$",
  [(r"$31$", r"Excludes the empty set, whose sum $0$ is even."),
   (r"$4$", r"Counts only the even-size choices of odd numbers, forgetting the free choice of even numbers."),
   (r"$8$", r"Counts only the subsets of $\{2, 4, 6\}$.")],
  r"The sum is even exactly when the subset contains an even number of the odd elements $1, 3, 5$: $\binom{3}{0} + \binom{3}{2} = 4$ ways. The even elements $2, 4, 6$ are free: $2^3 = 8$ ways. Total $4 \times 8 = 32$.",
  "Ignoring the free choice of elements that do not affect the condition.",
  "U01-A-subsets-even-sum", "Parity analysis plus the multiplication principle.",
  check=_c34, values=[32, 31, 4, 8], cognitive="Analysis")


def _c35():
    n = Symbol('n', positive=True, integer=True)
    nn = int(solve(n*(n - 1)/2 - 28, n)[0])
    return Integer(sum(1 for s in subsets(range(nn)) if 3 <= len(s) <= 6))
q("U01-A-035", "Subsets", "Subsets with size in a given band", "Medium",
  "Multi-step computation MCQ",
  r"A finite set $X$ has exactly $28$ subsets with two elements. The number of subsets of $X$ having at least three and at most six elements is",
  r"$210$",
  [(r"$219$", r"Removes only the subsets with at most two elements, $256 - 1 - 8 - 28$, and ignores the upper bound."),
   (r"$182$", r"Reads 'at most six' as 'fewer than six' and also removes the $28$ six-element subsets, $210 - 28$."),
   (r"$211$", r"Forgets the empty set among the excluded small subsets, $256 - 8 - 28 - 8 - 1$.")],
  r"$\binom{n}{2} = 28$ gives $n(n - 1) = 56$, so $n = 8$ and $X$ has $2^8 = 256$ subsets. Taking complements pairs each $k$-element subset with an $(8 - k)$-element subset, so there are $8$ subsets with seven elements and $1$ with eight. Excluding sizes $0, 1, 2$ ($1 + 8 + 28 = 37$) and sizes $7, 8$ ($8 + 1 = 9$) leaves $256 - 37 - 9 = 210$.",
  "Ignoring one end of a two-sided size condition, or using complementation carelessly.",
  "U01-A-subsets-size-band", "Find $n$ from a count, then exclude both tails using complementation.",
  check=_c35, values=[210, 219, 182, 211], cognitive="Application",
  numerical=dict(question=r"A finite set $X$ has exactly $28$ subsets with two elements. The number of subsets of $X$ having at least three and at most six elements is", answer=210))

# ================================================================ DIFFICULT (12)


def _c36():
    a, b, c, pq, qr, pr, t, z = symbols('a b c pq qr pr t z')
    cons = [a + pq + pr + t - 70, b + pq + qr + t - 75, c + qr + pr + t - 80,
            a + b + c + pq + qr + pr + t + z - 100]
    cons = [Eq(e, 0) for e in cons] + [v >= 0 for v in (a, b, c, pq, qr, pr, t, z)]
    return lpmin(t, cons)[0]
q("U01-A-036", "Venn diagrams and cardinality", "Three sets: least possible triple overlap", "Difficult",
  "Multi-step computation MCQ",
  r"In a group of $100$ people, $70$ like tea, $75$ like coffee and $80$ like juice. The least possible number of people who like all three drinks is",
  r"$25$",
  [(r"$45$", r"Finds the least overlap of tea and coffee, $70 + 75 - 100$, and stops."),
   (r"$55$", r"Finds the least overlap of coffee and juice, $75 + 80 - 100$, and stops."),
   (r"$0$", r"Assumes the sets can be arranged so that no one likes all three.")],
  r"Each person who does not like all three misses at least one drink. The total number of misses is $30 + 25 + 20 = 75$, so at most $75$ people miss something and at least $100 - 75 = 25$ like all three. This is attained when the $30$, $25$ and $20$ non-likers are disjoint groups, so the least value is $25$.",
  "Reasoning with only two of the three sets.",
  "U01-A-venn3-min-triple", "Complement counting with an attainability check.",
  check=_c36, values=[25, 45, 55, 0], cognitive="Analysis")


def _c37():
    from math import prod
    return Integer(sum(1 for s in subsets(range(1, 13)) if s and prod(s) % 6 == 0))
q("U01-A-037", "Subsets", "Subsets whose product is divisible by 6", "Difficult",
  "Multi-step computation MCQ",
  r"The number of non-empty subsets of $\{1, 2, 3, \dots, 12\}$ the product of whose elements is divisible by $6$ is",
  r"$3792$",
  [(r"$3776$", r"Subtracts the $2^6$ subsets with no even element and the $2^8$ subsets with no multiple of $3$ from $2^{12}$, but does not add back the $2^4$ subsets with neither."),
   (r"$3072$", r"Counts only the subsets containing $6$ or $12$, $2^{12} - 2^{10}$, missing products such as $2 \times 3$."),
   (r"$3791$", r"Removes the empty set from $2^{12}$ and then subtracts $304$, a complement count that already contains the empty set, so the empty set is removed twice.")],
  r"Count all subsets, including the empty one, whose product is not divisible by $6$: either no element is even ($2^6 = 64$ subsets of $\{1, 3, 5, 7, 9, 11\}$) or no element is a multiple of $3$ ($2^8 = 256$ subsets of the other eight numbers), and both happen for the $2^4 = 16$ subsets of $\{1, 5, 7, 11\}$. So $64 + 256 - 16 = 304$ subsets fail, the empty set among them. Hence $2^{12} - 304 = 3792$ non-empty subsets have product divisible by $6$.",
  "Forgetting the add-back term, or mishandling the empty set in a complement count.",
  "U01-A-subsets-product-divisible", "Complementary counting combined with inclusion and exclusion on two overlapping conditions, plus an empty-set trap.",
  check=_c37, values=[3792, 3776, 3072, 3791], cognitive="Analysis",
  numerical=dict(question=r"The number of non-empty subsets of $\{1, 2, 3, \dots, 12\}$ the product of whose elements is divisible by $6$ is", answer=3792))

def _c38():
    e1, e2, e3 = symbols('e1 e2 e3')
    s = solve([e1 - 120, e2 - 60, e1 + e2 + e3 - 200], [e1, e2, e3], dict=True)[0]
    return s[e1] + 2*s[e2] + 3*s[e3]
q("U01-A-038", "Venn diagrams and cardinality", "Three sets: sum of sizes from exact counts", "Difficult",
  "Multi-step computation MCQ",
  r"Each of $200$ students studies at least one of three languages $X$, $Y$, $Z$. Exactly $120$ students study exactly one language and $60$ study exactly two. Then $n(X) + n(Y) + n(Z)$ equals",
  r"$300$",
  [(r"$200$", r"Assumes the sum of the set sizes equals the number of students."),
   (r"$260$", r"Counts the students who study all three only once in the sum."),
   (r"$240$", r"Forgets the students who study all three, $120 + 2 \times 60$.")],
  r"The number studying all three is $200 - 120 - 60 = 20$. In $n(X) + n(Y) + n(Z)$ a student is counted once for each language studied, so the sum is $120 \times 1 + 60 \times 2 + 20 \times 3 = 300$.",
  "Counting each student once regardless of how many sets contain them.",
  "U01-A-venn3-exact-counts", "Find the hidden triple count, then weight each group.",
  check=_c38, values=[300, 200, 260, 240], cognitive="Analysis",
  numerical=dict(question=r"Each of $200$ students studies at least one of three languages $X$, $Y$, $Z$. Exactly $120$ students study exactly one language and $60$ study exactly two. Then the value of $n(X) + n(Y) + n(Z)$ is", answer=300))


def _c39():
    e1, e3 = symbols('e1 e3')
    s = solve([e1 + 20 + e3 - 100, e1 + 2*20 + 3*e3 - (60 + 50 + 44)], [e1, e3], dict=True)[0]
    return s[e3]
q("U01-A-039", "Venn diagrams and cardinality", "Three sets: all three from exact counts", "Difficult",
  "Inverse/parameter MCQ",
  r"In a group of $100$ people, each likes at least one of the games $X$, $Y$, $Z$. $60$ like $X$, $50$ like $Y$ and $44$ like $Z$. If exactly $20$ people like exactly two of the games, the number of people who like all three is",
  r"$17$",
  [(r"$34$", r"Finds $154 - 100 - 20 = 34$ but forgets that each person liking all three is counted twice in the excess."),
   (r"$54$", r"Takes the whole excess $154 - 100$ as the number liking all three."),
   (r"$14$", r"Subtracts $2 \times 20$ for the exactly-two group, $154 - 100 - 40$, and does not halve.")],
  r"Let $e_1$, $e_3$ be the numbers liking exactly one and all three. Then $e_1 + 20 + e_3 = 100$ and $e_1 + 2(20) + 3e_3 = 60 + 50 + 44 = 154$. Subtracting, $20 + 2e_3 = 54$, so $e_3 = 17$.",
  "Not weighting the exactly-two and all-three groups correctly in the sum of sizes.",
  "U01-A-venn3-exact-counts", "Two weighted counting equations solved together.",
  check=_c39, values=[17, 34, 54, 14], cognitive="Analysis")


def _c40():
    ok = [k for k in range(0, 81) if 50 - k >= 0 and 45 - k >= 0 and 0 <= 80 - (95 - k) <= 10]
    return len(ok)
q("U01-A-040", "Venn diagrams and cardinality", "Two sets: overlap under a bound on the outside", "Difficult",
  "Multi-step computation MCQ",
  r"In a group of $80$ people, $50$ play cricket and $45$ play football. It is known that at most $10$ people play neither game. The number of possible values of the number of people who play both games is",
  r"$11$",
  [(r"$26$", r"Ignores that the number playing neither cannot be negative, allowing $0$ to $25$."),
   (r"$31$", r"Ignores the bound of $10$ on the outside, allowing $15$ to $45$."),
   (r"$10$", r"Finds the range $15$ to $25$ and computes $25 - 15$.")],
  r"Let $k$ play both. Then the number playing neither is $80 - (95 - k) = k - 15$. The conditions $0 \le k - 15 \le 10$ give $15 \le k \le 25$, and $k \le 45$ is automatic. So $k$ has $11$ possible values.",
  "Ignoring one of the two constraints on the region outside both sets.",
  "U01-A-venn2-bounded-outside", "Translate two constraints into bounds and count.",
  check=_c40, values=[11, 26, 31, 10], cognitive="Analysis",
  numerical=dict(question=r"In a group of $80$ people, $50$ play cricket and $45$ play football. It is known that at most $10$ people play neither game. The number of possible values of the number of people who play both games is", answer=11))


def _c41():
    S = subsets(range(1, 5))
    return sum(1 for P in S for Q in S if len(P & Q) == 1)
q("U01-A-041", "Subsets", "Ordered pairs of subsets with one common element", "Difficult",
  "Multi-step computation MCQ",
  r"The number of ordered pairs $(P, Q)$ of subsets of $\{1, 2, 3, 4\}$ such that $P \cap Q$ has exactly one element is",
  r"$108$",
  [(r"$256$", r"Chooses the common element and then lets each other element be in $P$, $Q$, both or neither, $4 \times 4^3$."),
   (r"$81$", r"Counts the pairs with $P \cap Q = \emptyset$, $3^4$."),
   (r"$32$", r"Chooses the common element and then gives only two choices to each other element, $4 \times 2^3$.")],
  r"Choose the common element in $4$ ways. Each of the other $3$ elements must not be in both sets, so it has $3$ options: neither, $P$ only, $Q$ only. Total $4 \times 3^3 = 108$.",
  "Allowing other elements into both sets.",
  "U01-A-pairs-one-common", "Choice of the common element plus three-way element counting.",
  check=_c41, values=[108, 256, 81, 32], cognitive="Analysis")


def _c42():
    return sum(1 for s in subsets(range(1, 11)) if s & {1, 2, 3} and s & {8, 9, 10})
q("U01-A-042", "Subsets", "Subsets meeting two given sets", "Difficult",
  "Multi-step computation MCQ",
  r"The number of subsets of $\{1, 2, 3, \dots, 10\}$ that contain at least one element of $\{1, 2, 3\}$ and at least one element of $\{8, 9, 10\}$ is",
  r"$784$",
  [(r"$768$", r"Subtracts the $2^7$ subsets missing each block but does not add back the $2^4$ subsets missing both."),
   (r"$896$", r"Subtracts only the subsets missing $\{1, 2, 3\}$, $2^{10} - 2^7$."),
   (r"$49$", r"Multiplies the non-empty choices $7 \times 7$ and forgets the free elements $4, 5, 6, 7$.")],
  r"The elements $4, 5, 6, 7$ are free: $2^4 = 16$ ways. From $\{1, 2, 3\}$ a non-empty choice: $2^3 - 1 = 7$ ways, and likewise $7$ from $\{8, 9, 10\}$. Total $16 \times 49 = 784$. Equivalently $2^{10} - 2 \cdot 2^7 + 2^4 = 784$.",
  "Forgetting the add-back term in inclusion and exclusion.",
  "U01-A-subsets-meet-two", "Inclusion and exclusion on subsets, or a product argument.",
  check=_c42, values=[784, 768, 896, 49], cognitive="Analysis",
  numerical=dict(question=r"The number of subsets of $\{1, 2, 3, \dots, 10\}$ that contain at least one element of $\{1, 2, 3\}$ and at least one element of $\{8, 9, 10\}$ is", answer=784))


def _c43():
    return len(int_points(lambda k: (k % 2 == 0 or k % 3 == 0) and k % 5 != 0, 1, 100))
q("U01-A-043", "Venn diagrams and cardinality", "Inclusion and exclusion with divisibility sets", "Difficult",
  "Multi-step computation MCQ",
  r"The number of integers $n$ with $1 \le n \le 100$ that are divisible by $2$ or $3$ but not by $5$ is",
  r"$54$",
  [(r"$67$", r"Counts the multiples of $2$ or $3$ and ignores the condition on $5$."),
   (r"$47$", r"Subtracts all $20$ multiples of $5$ from $67$, though many are not multiples of $2$ or $3$."),
   (r"$51$", r"Removes multiples of $10$ and of $15$ as $10 + 6$ without adding back the $3$ multiples of $30$.")],
  r"Multiples of $2$ or $3$: $50 + 33 - 16 = 67$. Among these, the multiples of $5$ are the multiples of $10$ or $15$: $10 + 6 - 3 = 13$. Hence $67 - 13 = 54$.",
  "Subtracting all multiples of $5$ instead of only those already counted.",
  "U01-A-divisibility-sets", "Two rounds of inclusion and exclusion.",
  check=_c43, values=[54, 67, 47, 51], cognitive="Analysis",
  numerical=dict(question=r"The number of integers $n$ with $1 \le n \le 100$ that are divisible by $2$ or $3$ but not by $5$ is", answer=54))


def _c44():
    best = max(28 + 32 - 2*k for k in range(0, 29) if 50 - (60 - k) >= 0)
    return best
q("U01-A-044", "Venn diagrams and cardinality", "Two sets: greatest number in exactly one", "Difficult",
  "Multi-step computation MCQ",
  r"In a group of $50$ people, $28$ like tea and $32$ like coffee. The greatest possible number of people who like exactly one of the two drinks is",
  r"$40$",
  [(r"$4$", r"Finds the least value, taking the overlap as large as possible, $28$."),
   (r"$50$", r"Computes $n(\text{tea} \cup \text{coffee}) = 60 - 10$, subtracting the overlap only once."),
   (r"$32$", r"Uses $60 - k$ with the overlap $k = 28$, subtracting the overlap once and at the wrong end.")],
  r"If $k$ people like both, exactly one is $(28 - k) + (32 - k) = 60 - 2k$. This is largest when $k$ is smallest. Since $60 - k \le 50$, $k \ge 10$, and $k = 10$ is possible. So the greatest value is $60 - 20 = 40$.",
  "Subtracting the overlap once when counting exactly one.",
  "U01-A-venn2-exactly-one-max", "Optimise a linear count under a union bound.",
  check=_c44, values=[40, 4, 50, 32], cognitive="Analysis")


def _c45():
    return identity_index(lambda U, P, Q, R: (P - Q) | (Q - R) | (R - P),
                          [lambda U, P, Q, R: (P | Q | R) - (P & Q & R),
                           lambda U, P, Q, R: P | Q | R,
                           lambda U, P, Q, R: (P | Q | R) - ((P & Q) | (Q & R) | (R & P)),
                           lambda U, P, Q, R: U - (P & Q & R)], nsets=3)
q("U01-A-045", "Algebra of sets", "Cyclic union of differences", "Difficult",
  "Conceptual/application MCQ",
  r"For subsets $P$, $Q$, $R$ of a universal set $U$, the set $(P - Q) \cup (Q - R) \cup (R - P)$ equals",
  r"$(P \cup Q \cup R) - (P \cap Q \cap R)$",
  [(r"$P \cup Q \cup R$", r"Thinks every element of the union lies in one of the differences, missing elements in all three sets."),
   (r"$(P \cup Q \cup R) - [(P \cap Q) \cup (Q \cap R) \cup (R \cap P)]$", r"Thinks the differences keep only elements in exactly one set, missing for example $x \in P \cap Q$, $x \notin R$, which lies in $Q - R$."),
   (r"$(P \cap Q \cap R)'$", r"Takes the complement of the triple intersection, wrongly including elements outside all three sets.")],
  r"An element in none of the sets lies in no difference. An element in all three lies in no difference. If $x$ lies in some but not all of the sets, then going round $P \to Q \to R \to P$ there is a step from a set containing $x$ to one not containing it, so $x$ lies in the corresponding difference. Hence the set is $(P \cup Q \cup R) - (P \cap Q \cap R)$.",
  "Ignoring elements lying in exactly two of the sets.",
  "U01-A-law-cyclic-difference", "Casework on Venn regions for three sets.",
  check=_c45, values=[0, 1, 2, 3], cognitive="Analysis")


def _c46():
    for t in range(45, -1, -1):
        rest = 155 - 100 - 2*t          # pq + qr + pr forced by the total of 100
        if rest < 0:
            continue
        for pq in range(rest + 1):
            for qr in range(rest - pq + 1):
                pr = rest - pq - qr
                a = 60 - t - pq - pr; b = 50 - t - pq - qr; c = 45 - t - qr - pr
                if min(a, b, c) >= 0 and a + b + c + pq + qr + pr + t == 100:
                    return t
q("U01-A-046", "Venn diagrams and cardinality", "Three sets: greatest possible triple overlap", "Difficult",
  "Multi-step computation MCQ",
  r"Each of the $100$ members of a club joins at least one of three activities $X$, $Y$, $Z$; $60$ join $X$, $50$ join $Y$ and $45$ join $Z$. The greatest possible number of members who join all three activities is",
  r"$27$",
  [(r"$28$", r"Reaches $e_2 + 2e_3 = 55$ and rounds $\frac{55}{2}$ up instead of down."),
   (r"$45$", r"Takes the size of the smallest set, ignoring that every member joins at least one activity."),
   (r"$55$", r"Takes the whole excess $155 - 100$ as the number joining all three.")],
  r"With $e_1, e_2, e_3$ the numbers joining exactly one, two, three activities, $e_1 + e_2 + e_3 = 100$ and $e_1 + 2e_2 + 3e_3 = 60 + 50 + 45 = 155$, so $e_2 + 2e_3 = 55$ and $e_3 \le 27$. The value $27$ is attained: all three $27$, $X$ and $Y$ only $1$, only $X$ $32$, only $Y$ $22$, only $Z$ $18$, which gives the sizes $60, 50, 45$ and total $100$. So the greatest value is $27$.",
  "Ignoring the at-least-one condition, which limits the triple overlap.",
  "U01-A-venn3-max-triple", "Weighted counting gives a bound, integrality trims it, and a construction shows it is attained.",
  check=_c46, values=[27, 28, 45, 55], cognitive="Analysis")


def _c47():
    S = subsets(range(1, 6))
    return sum(1 for P in S for Q in S if P <= Q and len(Q) - len(P) == 2)
q("U01-A-047", "Subsets", "Nested subsets with a fixed size gap", "Difficult",
  "Multi-step computation MCQ",
  r"The number of ordered pairs $(P, Q)$ of subsets of $\{1, 2, 3, 4, 5\}$ such that $P \subseteq Q$ and $n(Q) - n(P) = 2$ is",
  r"$80$",
  [(r"$243$", r"Counts all pairs with $P \subseteq Q$, $3^5$, ignoring the size condition."),
   (r"$160$", r"Chooses the two elements of $Q - P$ but miscounts the remaining elements as four, $10 \times 2^4$."),
   (r"$10$", r"Counts only the choices of the two elements of $Q - P$.")],
  r"Each element is in neither set, in $Q$ only, or in both. Exactly $2$ elements must be in $Q$ only: $\binom{5}{2} = 10$ ways. Each of the other $3$ elements is either in both or in neither: $2^3 = 8$ ways. Total $10 \times 8 = 80$.",
  "Ignoring the freedom of the remaining elements, or the size condition.",
  "U01-A-nested-pairs-gap", "Element-wise classification with a size constraint.",
  check=_c47, values=[80, 243, 160, 10], cognitive="Analysis")
