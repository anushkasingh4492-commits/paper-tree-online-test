import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
from itertools import product as _iprod
from sympy.utilities.iterables import multiset_partitions as _mparts

# ---------------------------------------------------------------- helpers


def _pairs(X, Y=None):
    return list(_iprod(X, X if Y is None else Y))


def _rels(X, Y=None):
    """All relations from X to Y (or on X) as frozensets of ordered pairs."""
    P = _pairs(X, Y)
    for m in range(1 << len(P)):
        yield frozenset(P[i] for i in range(len(P)) if m >> i & 1)


def _ref(R, X):
    return all((a, a) in R for a in X)


def _sym(R):
    return all((b, a) in R for (a, b) in R)


def _tr(R):
    return all((a, d) in R for (a, b) in R for (c, d) in R if b == c)


def _props(R, X):
    return (_ref(R, X), _sym(R), _tr(R))


def _eq(R, X):
    return _ref(R, X) and _sym(R) and _tr(R)


def _partitions(X):
    return list(_mparts(list(X)))


def _rel_of(part):
    return frozenset((a, b) for blk in part for a in blk for b in blk)


def _trclose(R):
    R = set(R)
    while True:
        new = {(a, d) for (a, b) in R for (c, d) in R if b == c} - R
        if not new:
            return frozenset(R)
        R |= new


def _rel_on(X, cond):
    return frozenset((a, b) for a in X for b in X if cond(a, b))


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

P_RNN = "reflexive but neither symmetric nor transitive"
P_RT = "reflexive and transitive but not symmetric"
P_RS = "reflexive and symmetric but not transitive"
P_ALL = "reflexive, symmetric and transitive"
P_S = "symmetric but neither reflexive nor transitive"
P_ST = "symmetric and transitive but not reflexive"
P_TT, P_TF, P_FF = True, False, False

u, v = symbols('u v')

# ================================================================ CLASS XI: Cartesian products, number of relations, domain and range

# 001 E
def _c001():
    X, Y = range(3), range(4)
    return Integer(sum(1 for _ in _rels(X, Y)))
q("U01-B-001", "Relations", "Number of relations between two finite sets", "Easy",
  "Single-step computation MCQ",
  r"If $n(X) = 3$ and $n(Y) = 4$, then the number of relations from $X$ to $Y$ is",
  r"$2^{12}$",
  [(r"$2^{7}$", r"Adds the sizes, using $2^{n(X)+n(Y)}$ in place of $2^{n(X)\,n(Y)}$."),
   (r"$12$", r"Gives $n(X \times Y) = 12$, the number of ordered pairs, not the number of subsets of $X \times Y$."),
   (r"$4^{3}$", r"Counts functions from $X$ to $Y$, $n(Y)^{n(X)} = 64$, instead of all relations.")],
  r"A relation from $X$ to $Y$ is any subset of $X \times Y$. Since $n(X \times Y) = 3 \cdot 4 = 12$, the number of subsets, and hence of relations, is $2^{12}$.",
  "Confusing the number of ordered pairs, or the number of functions, with the number of relations.",
  "U01-B-count-relations-basic", "One definition and one count.",
  check=_c001, values=[2**12, 2**7, 12, 4**3], cognitive="Recall", source_class="XI")

# 002 E
def _c002():
    given = [(1, u), (2, v), (3, u)]
    X = {a for a, _ in given}; Y = {b for _, b in given}
    assert len(X) * len(Y) == 6          # so X and Y are exactly these sets
    XY = {(a, b) for a in X for b in Y}
    cands = [(1, v), (u, 1), (4, v), (v, v)]
    inside = [c for c in cands if c in XY]
    assert len(inside) == 1
    return inside[0]
q("U01-B-002", "Cartesian product", "Recovering the sets from part of a Cartesian product", "Easy",
  "Direct concept MCQ",
  r"The Cartesian product $X \times Y$ has exactly $6$ elements, and $(1, u)$, $(2, v)$ and $(3, u)$ are three of them, where $u \ne v$ and neither $u$ nor $v$ belongs to $\{1, 2, 3, 4\}$. Which of the following is also an element of $X \times Y$?",
  r"$(1, v)$",
  [(r"$(u, 1)$", r"Reverses the order in the ordered pair; $(u, 1)$ belongs to $Y \times X$, not $X \times Y$."),
   (r"$(4, v)$", r"Assumes $X$ may contain a further element $4$; but $n(X) \ge 3$, $n(Y) \ge 2$ and $n(X)\,n(Y) = 6$ force $X = \{1, 2, 3\}$."),
   (r"$(v, v)$", r"Pairs an element of $Y$ with itself, treating $X \times Y$ as if it were $Y \times Y$.")],
  r"The first coordinates show $\{1, 2, 3\} \subseteq X$ and the second coordinates show $\{u, v\} \subseteq Y$. Since $n(X)\,n(Y) = 6$, we must have $X = \{1, 2, 3\}$ and $Y = \{u, v\}$. Hence $(1, v) \in X \times Y$, while the other listed pairs are not.",
  "Ignoring the order of coordinates in a Cartesian product.",
  "U01-B-cartesian-recover-sets", "Two observations: coordinates give subsets, the count fixes the sets.",
  check=_c002, values=[(1, v), (u, 1), (4, v), (v, v)], cognitive="Understanding",
  source_class="XI")

# 003 E
def _c003():
    k = [s for s in solve(Symbol('k')**2 - 9) if s > 0][0]
    X = {-1, 0, 1}
    assert len(X) == k
    return Integer(sum(1 for a, b in _pairs(X) if a * b == 0))
q("U01-B-003", "Cartesian product", "Counting elements of a Cartesian square with a condition", "Easy",
  "Single-step computation MCQ",
  r"The set $X \times X$ has $9$ elements, and two of them are $(-1, 0)$ and $(0, 1)$. The number of elements $(a, b)$ of $X \times X$ with $ab = 0$ is",
  r"$5$",
  [(r"$6$", r"Adds the $3$ pairs with $a = 0$ and the $3$ pairs with $b = 0$, counting $(0, 0)$ twice."),
   (r"$3$", r"Counts only the pairs with $a = 0$ and forgets those with $b = 0$."),
   (r"$1$", r"Reads $ab = 0$ as requiring both $a = 0$ and $b = 0$.")],
  r"Since $n(X)^2 = 9$, $n(X) = 3$, and the given pairs show $-1, 0, 1 \in X$, so $X = \{-1, 0, 1\}$. Pairs with $a = 0$: $3$; pairs with $b = 0$: $3$; $(0, 0)$ is common. So the count is $3 + 3 - 1 = 5$.",
  "Double counting the pair common to both cases.",
  "U01-B-cartesian-square-count", "Recover the set, then a small inclusion-exclusion count.",
  check=_c003, values=[5, 6, 3, 1], cognitive="Application", source_class="XI",
  numerical=dict(question=r"The set $X \times X$ has $9$ elements, and two of them are $(-1, 0)$ and $(0, 1)$. The number of elements $(a, b)$ of $X \times X$ with $ab = 0$ is", answer=5))

# 004 E
def _c004():
    X = range(1, 11)
    R = {(x, y) for x in X for y in X if y == 2*x - 1}
    return FiniteSet(*[y for _, y in R])
q("U01-B-004", "Relations", "Range of a relation defined by a rule", "Easy",
  "Single-step computation MCQ",
  r"Let $X = \{1, 2, 3, \ldots, 10\}$ and let $R = \{(x, y) : x, y \in X,\ y = 2x - 1\}$. The range of $R$ is",
  r"$\{1, 3, 5, 7, 9\}$",
  [(r"$\{1, 2, 3, 4, 5\}$", r"Gives the domain of $R$, the set of first coordinates, in place of the range."),
   (r"$\{1, 3, 5, \ldots, 19\}$", r"Lets $x$ run over all of $X$ and ignores the requirement $y \in X$."),
   (r"$\{2, 4, 6, 8, 10\}$", r"Reads the rule as $y = 2x$, taking the even numbers of $X$.")],
  r"We need $y = 2x - 1 \le 10$, so $x \le 5$. Then $R = \{(1,1), (2,3), (3,5), (4,7), (5,9)\}$, and the range (set of second coordinates) is $\{1, 3, 5, 7, 9\}$.",
  "Mixing up domain and range, or ignoring that the image must lie in the codomain set.",
  "U01-B-range-rule", "One rule, one restriction on the codomain.",
  check=_c004, values=[FiniteSet(1, 3, 5, 7, 9), FiniteSet(1, 2, 3, 4, 5), FiniteSet(*range(1, 20, 2)),
                       FiniteSet(2, 4, 6, 8, 10)], cognitive="Application", source_class="XI")

# 005 M
def _c005():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X) if (1, 2) in R and (2, 1) in R and (3, 3) not in R))
q("U01-B-005", "Relations", "Number of relations with prescribed pairs", "Medium",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, 3\}$. The number of relations on $X$ that contain both $(1, 2)$ and $(2, 1)$ but do not contain $(3, 3)$ is",
  r"$64$",
  [(r"$128$", r"Fixes the two required pairs but leaves $(3, 3)$ free, giving $2^{7}$."),
   (r"$256$", r"Excludes $(3, 3)$ but leaves $(1, 2)$ and $(2, 1)$ free, giving $2^{8}$."),
   (r"$6$", r"Counts the $6$ remaining free ordered pairs instead of the subsets they can form.")],
  r"$X \times X$ has $9$ ordered pairs. Three of them are decided: $(1, 2)$ and $(2, 1)$ must be in, $(3, 3)$ must be out. Each of the other $6$ pairs may be included or not, so the number is $2^{6} = 64$.",
  "Fixing only some of the prescribed pairs.",
  "U01-B-relations-prescribed-pairs", "Two kinds of constraints (inclusion and exclusion) handled together.",
  check=_c005, values=[64, 128, 256, 6], cognitive="Application", source_class="XI",
  numerical=dict(question=r"Let $X = \{1, 2, 3\}$. The number of relations on $X$ that contain both $(1, 2)$ and $(2, 1)$ but do not contain $(3, 3)$ is", answer=64))

# 006 M
def _c006():
    t = symbols('t', positive=True, integer=True)
    ny = [r for r in solve(Eq((t + 1)*t, 20), t) if r > 0][0]
    nx = ny + 1
    assert 2**(nx*ny) == 2**20
    k = symbols('k', integer=True)
    return solve(Eq(2**(nx**2), 2**k * 2**(ny**2)), k)[0]
q("U01-B-006", "Relations", "Comparing numbers of relations on two sets of related size", "Medium",
  "Inverse/parameter MCQ",
  r"Let $X$ and $Y$ be finite sets with $n(X) = n(Y) + 1$. The number of relations from $X$ to $Y$ is $2^{20}$. If the number of relations on $X$ is $2^{k}$ times the number of relations on $Y$, then $k$ equals",
  r"$9$",
  [(r"$1$", r"Uses $\big(n(X) - n(Y)\big)^2 = 1$ as the exponent, in place of $n(X)^2 - n(Y)^2 = 25 - 16$."),
   (r"$41$", r"Multiplies the two counts instead of dividing, adding the exponents $25 + 16$."),
   (r"$5$", r"Compares the relations on $X$, $2^{25}$, with the relations from $X$ to $Y$, $2^{20}$, instead of with the relations on $Y$.")],
  r"Let $n(Y) = m$, so $n(X) = m + 1$. Relations from $X$ to $Y$ number $2^{m(m+1)} = 2^{20}$, so $m^2 + m - 20 = 0$, giving $m = 4$ (as $m > 0$) and $n(X) = 5$. Relations on $X$ number $2^{25}$ and on $Y$ number $2^{16}$, so $2^{k} = \frac{2^{25}}{2^{16}} = 2^{9}$ and $k = 9$.",
  r"Treating $n(X)^2 - n(Y)^2$ as $\big(n(X) - n(Y)\big)^2$.",
  "U01-B-relations-ratio-sizes", "Set up and solve a quadratic in the set size, then compare two relation counts.",
  check=_c006, values=[9, 1, 41, 5], cognitive="Application", source_class="XI",
  numerical=dict(question=r"Let $X$ and $Y$ be finite sets with $n(X) = n(Y) + 1$. The number of relations from $X$ to $Y$ is $2^{20}$. If the number of relations on $X$ is $2^{k}$ times the number of relations on $Y$, then $k$ is", answer=9))

# 007 M
def _c007():
    X = [x for x in range(-5, 6) if abs(x) <= 2]
    return Integer(sum(1 for a, b in _pairs(X) if a**2 + b**2 <= 4))
q("U01-B-007", "Relations", "Number of elements of a relation given by an inequality", "Medium",
  "Multi-step computation MCQ",
  r"Let $X = \{x \in \mathbb{Z} : |x| \le 2\}$ and $R = \{(a, b) \in X \times X : a^2 + b^2 \le 4\}$. The number of elements in $R$ is",
  r"$13$",
  [(r"$9$", r"Uses the strict inequality $a^2 + b^2 < 4$, dropping the four pairs $(\pm 2, 0)$, $(0, \pm 2)$."),
   (r"$25$", r"Takes all of $X \times X$, assuming $|a|, |b| \le 2$ already gives $a^2 + b^2 \le 4$."),
   (r"$6$", r"Counts only pairs with $a, b \ge 0$.")],
  r"$X = \{-2, -1, 0, 1, 2\}$. Pairs with $a^2 + b^2 \in \{0, 1, 2, 4\}$: one with sum $0$, four with sum $1$, four with sum $2$ (namely $(\pm1, \pm1)$) and four with sum $4$ (namely $(\pm 2, 0), (0, \pm 2)$). Pairs such as $(1, 2)$ give $5 > 4$. Total $1 + 4 + 4 + 4 = 13$.",
  "Treating the bound on $|a|$ and $|b|$ as enough for the bound on $a^2 + b^2$.",
  "U01-B-relation-inequality-count", "Systematic case count over the values of $a^2 + b^2$.",
  check=_c007, values=[13, 9, 25, 6], cognitive="Application", source_class="XI",
  numerical=dict(question=r"Let $X = \{x \in \mathbb{Z} : |x| \le 2\}$ and $R = \{(a, b) \in X \times X : a^2 + b^2 \le 4\}$. The number of elements in $R$ is", answer=13))

# 008 M
def _c008():
    return Integer(sum(1 for R in _rels(range(2), range(3)) if len(R) >= 2))
q("U01-B-008", "Relations", "Number of relations with a size condition", "Medium",
  "Multi-step computation MCQ",
  r"If $n(X) = 2$ and $n(Y) = 3$, then the number of relations from $X$ to $Y$ having at least two ordered pairs is",
  r"$57$",
  [(r"$63$", r"Removes only the empty relation, forgetting the $6$ one-element relations."),
   (r"$58$", r"Removes the $6$ one-element relations but keeps the empty relation."),
   (r"$15$", r"Counts relations with exactly two ordered pairs, $\binom{6}{2}$.")],
  r"$n(X \times Y) = 6$, so there are $2^6 = 64$ relations. Those with fewer than two pairs are the empty relation and the $6$ singletons. Hence $64 - 1 - 6 = 57$.",
  "Reading 'at least two' as 'exactly two', or removing only some small cases.",
  "U01-B-relations-size-condition", "Complement counting with two excluded cases.",
  check=_c008, values=[57, 63, 58, 15], cognitive="Application", source_class="XI",
  numerical=dict(question=r"If $n(X) = 2$ and $n(Y) = 3$, then the number of relations from $X$ to $Y$ having at least two ordered pairs is", answer=57))

# 009 M
def _c009():
    x, y = symbols('x y', integer=True, positive=True)
    R = [(a, b) for a in range(1, 16) for b in range(1, 16) if a + 2*b == 15]
    Rinv = [(b, a) for a, b in R]
    return FiniteSet(*[p for p, _ in Rinv])
q("U01-B-009", "Relations", "Domain of an inverse relation", "Medium",
  "Multi-step computation MCQ",
  r"Let $\mathbb{N} = \{1, 2, 3, \ldots\}$ and $R = \{(x, y) : x, y \in \mathbb{N},\ x + 2y = 15\}$. The domain of the inverse relation $R^{-1}$ is",
  r"$\{1, 2, 3, \ldots, 7\}$",
  [(r"$\{1, 3, 5, \ldots, 13\}$", r"Gives the domain of $R$ itself rather than of $R^{-1}$."),
   (r"$\{0, 1, 2, \ldots, 7\}$", r"Allows $y = 0$, which is not in $\mathbb{N}$."),
   (r"$\{1, 3, 5, \ldots, 15\}$", r"Gives the domain of $R$ and also admits $y = 0$, which adds $x = 15$.")],
  r"$x = 15 - 2y \ge 1$ gives $y = 1, 2, \ldots, 7$, so $R = \{(13, 1), (11, 2), \ldots, (1, 7)\}$. The domain of $R^{-1}$ equals the range of $R$, which is $\{1, 2, \ldots, 7\}$.",
  "Not swapping roles: the domain of $R^{-1}$ is the range of $R$.",
  "U01-B-inverse-relation-domain", "Solve a linear equation in naturals, then switch to the inverse relation.",
  check=_c009, values=[FiniteSet(*range(1, 8)), FiniteSet(*range(1, 14, 2)), FiniteSet(*range(0, 8)),
                       FiniteSet(*range(1, 16, 2))], cognitive="Application", source_class="XI")

# 010 D
def _c010():
    X, Y = [1, 2, 3, 4], ['a', 'b']
    return Integer(sum(1 for R in _rels(X, Y)
                       if {p for p, _ in R} == set(X) and {s for _, s in R} == set(Y)))
q("U01-B-010", "Relations", "Relations with full domain and full range", "Difficult",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, 3, 4\}$ and $Y = \{p, q\}$. The number of relations $R$ from $X$ to $Y$ whose domain is $X$ and whose range is $Y$ is",
  r"$79$",
  [(r"$81$", r"Imposes only the domain condition ($3^4$) and forgets that the range must be all of $Y$."),
   (r"$80$", r"Removes only one of the two relations whose range is a single element."),
   (r"$14$", r"Counts only onto functions, $2^4 - 2$, forgetting that an element of $X$ may be related to both $p$ and $q$.")],
  r"For the domain to be $X$, each of the $4$ elements must be related to a non-empty subset of $Y$: $3$ choices each, $3^4 = 81$ relations. Among these, the range is only $\{p\}$ in one case (every element related to $p$ alone) and only $\{q\}$ in one case. So the count is $81 - 2 = 79$.",
  "Treating relations as functions, or forgetting the range condition.",
  "U01-B-relations-full-domain-range", "Counts per element, then removes two exceptional cases; distinguishes relations from functions.",
  check=_c010, values=[79, 81, 80, 14], cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"Let $X = \{1, 2, 3, 4\}$ and $Y = \{p, q\}$. The number of relations $R$ from $X$ to $Y$ whose domain is $X$ and whose range is $Y$ is", answer=79))

# 011 D
def _c011():
    k = [s for s in solve(Symbol('k')**2 - 9) if s > 0][0]
    X = set(range(1, 6)); Y = set(range(6 - int(k), 6 - int(k) + 4))
    assert len(X) == 5 and len(Y) == 4 and len(X & Y) == k
    XY = set(_pairs(X, Y)); YX = set(_pairs(Y, X))
    assert len(XY & YX) == 9
    return Integer(len(XY | YX))
q("U01-B-011", "Cartesian product", "Union of $X \\times Y$ and $Y \\times X$", "Difficult",
  "Multi-step computation MCQ",
  r"Let $X$ and $Y$ be sets with $n(X) = 5$ and $n(Y) = 4$. If $(X \times Y) \cap (Y \times X)$ has $9$ elements, then the number of elements in $(X \times Y) \cup (Y \times X)$ is",
  r"$31$",
  [(r"$40$", r"Adds $20 + 20$ without subtracting the common part."),
   (r"$37$", r"Subtracts $n(X \cap Y) = 3$ instead of the $9$ common ordered pairs."),
   (r"$36$", r"Computes $n\big((X \cup Y) \times (X \cup Y)\big) = 6^2$, assuming the union of the products is the product of the unions.")],
  r"$(X \times Y) \cap (Y \times X) = (X \cap Y) \times (X \cap Y)$, so $n(X \cap Y)^2 = 9$ and $n(X \cap Y) = 3$. Then $n\big((X \times Y) \cup (Y \times X)\big) = 20 + 20 - 9 = 31$.",
  "Treating the union of Cartesian products as a Cartesian product of unions.",
  "U01-B-cartesian-union-intersection", "Needs the identity for the intersection of products, then inclusion-exclusion; a tempting false identity for the union.",
  check=_c011, values=[31, 40, 37, 36], cognitive="Analysis", source_class="XI",
  numerical=dict(question=r"Let $X$ and $Y$ be sets with $n(X) = 5$ and $n(Y) = 4$. If $(X \times Y) \cap (Y \times X)$ has $9$ elements, then the number of elements in $(X \times Y) \cup (Y \times X)$ is", answer=31))

# 012 E
def _c012():
    P, Q, S = {1, 2}, {3, 4}, {4, 5}
    return Integer(len(set(_pairs(P, Q)) & set(_pairs(P, S))))
q("U01-B-012", "Cartesian product", "Intersection of Cartesian products", "Easy",
  "Single-step computation MCQ",
  r"Let $P = \{1, 2\}$, $Q = \{3, 4\}$ and $S = \{4, 5\}$. The number of elements in $(P \times Q) \cap (P \times S)$ is",
  r"$2$",
  [(r"$6$", r"Counts $P \times (Q \cup S)$, the union, instead of the intersection."),
   (r"$4$", r"Gives $n(P \times Q)$ and does not intersect."),
   (r"$0$", r"Assumes the two products are disjoint because $Q \ne S$.")],
  r"$(P \times Q) \cap (P \times S) = P \times (Q \cap S) = \{1, 2\} \times \{4\} = \{(1, 4), (2, 4)\}$, which has $2$ elements.",
  "Assuming products over different second sets cannot share pairs.",
  "U01-B-cartesian-distributive", "One distributive identity.",
  check=_c012, values=[2, 6, 4, 0], cognitive="Understanding", source_class="XI")

# 013 E
def _c013():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X) if {a for a, _ in R} == {1}))
q("U01-B-013", "Relations", "Relations with a prescribed domain", "Easy",
  "Single-step computation MCQ",
  r"Let $X = \{1, 2, 3\}$. The number of relations $R$ on $X$ whose domain is exactly $\{1\}$ is",
  r"$7$",
  [(r"$8$", r"Counts all subsets of $\{1\} \times X$, including the empty relation, whose domain is empty."),
   (r"$3$", r"Counts only the one-element relations $\{(1, 1)\}, \{(1, 2)\}, \{(1, 3)\}$."),
   (r"$1$", r"Takes the only such relation to be $\{1\} \times X$.")],
  r"Such an $R$ is a non-empty subset of $\{1\} \times X = \{(1,1), (1,2), (1,3)\}$. There are $2^3 - 1 = 7$ of them.",
  "Including the empty relation, whose domain is empty.",
  "U01-B-relations-given-domain", "One reformulation and one count.",
  check=_c013, values=[7, 8, 3, 1], cognitive="Application", source_class="XI")

# ================================================================ CLASS XII: types of relations, equivalence

# 014 E
def _c014():
    X = [1, 2, 3]
    R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 3)}
    return _props(R, X)
q("U01-B-014", "Types of relations", "Testing a finite relation", "Easy",
  "Direct concept MCQ",
  r"On $X = \{1, 2, 3\}$, the relation $R = \{(1, 1), (2, 2), (3, 3), (1, 2), (2, 3)\}$ is",
  P_RNN,
  [(P_RT, r"Checks transitivity only on pairs involving diagonal elements and misses the chain $(1, 2), (2, 3)$, which needs $(1, 3)$."),
   (P_ALL, r"Assumes a reflexive relation is automatically symmetric and transitive."),
   (P_RS, r"Treats $(1, 2) \in R$ as if $(2, 1)$ were also present.")],
  r"All of $(1,1), (2,2), (3,3)$ are present, so $R$ is reflexive. $(1, 2) \in R$ but $(2, 1) \notin R$, so it is not symmetric. $(1, 2), (2, 3) \in R$ but $(1, 3) \notin R$, so it is not transitive.",
  "Not testing every chain $(a, b), (b, c)$ for transitivity.",
  "U01-B-finite-relation-type", "Three direct property checks on a listed relation.",
  check=_c014, values=[(True, False, False), (True, False, True), (True, True, True), (True, True, False)],
  cognitive="Understanding", source_class="XII")

# 015 E
def _c015():
    X = [1, 2, 3, 4]
    R = {(1, 1), (2, 2), (3, 3), (4, 4), (1, 2), (1, 3), (3, 2)}
    return _props(R, X)
q("U01-B-015", "Types of relations", "Testing a finite relation", "Easy",
  "Direct concept MCQ",
  r"On $X = \{1, 2, 3, 4\}$, the relation $R = \{(1, 1), (2, 2), (3, 3), (4, 4), (1, 2), (1, 3), (3, 2)\}$ is",
  P_RT,
  [(P_RNN, r"Applies transitivity to the chain $(1, 3), (3, 2)$ but looks for $(2, 1)$ rather than $(1, 2)$, wrongly concluding it fails."),
   (P_ALL, r"Assumes a relation that is reflexive and transitive must also be symmetric."),
   (P_RS, r"Swaps the two definitions: tests symmetry with the chain condition, which holds, and transitivity with the reversal condition, which fails because $(2, 1) \notin R$, so calls $R$ symmetric but not transitive.")],
  r"Every $(a, a)$ is present, so $R$ is reflexive. $(1, 2) \in R$ but $(2, 1) \notin R$, so it is not symmetric. The only chains through distinct elements are $(1, 3), (3, 2)$, needing $(1, 2) \in R$, which holds; chains using a diagonal pair are automatic. So $R$ is transitive.",
  "Reading transitivity backwards along a chain.",
  "U01-B-finite-relation-type", "Three direct checks; one chain to verify.",
  check=_c015, values=[(True, False, True), (True, False, False), (True, True, True), (True, True, False)],
  cognitive="Understanding", source_class="XII")

# 016 E
def _c016():
    X = [1, 2, 3, 4]
    return Integer(sum(1 for R in _rels(X) if _ref(R, X)))
q("U01-B-016", "Counting relations with properties", "Number of reflexive relations", "Easy",
  "Single-step computation MCQ",
  r"The number of reflexive relations on a set with $4$ elements is",
  r"$2^{12}$",
  [(r"$2^{16}$", r"Counts all relations on the set, ignoring that the $4$ diagonal pairs are forced."),
   (r"$2^{10}$", r"Gives the number of symmetric relations, $2^{4 + 6}$."),
   (r"$2^{4}$", r"Treats only the $4$ diagonal pairs as free choices, though they are exactly the forced ones.")],
  r"A reflexive relation must contain all $4$ pairs $(a, a)$. Each of the remaining $16 - 4 = 12$ ordered pairs may be included or not, giving $2^{12}$ reflexive relations.",
  "Confusing which pairs are forced and which are free.",
  "U01-B-count-reflexive", "One formula, $2^{n^2 - n}$.",
  check=_c016, values=[2**12, 2**16, 2**10, 2**4], cognitive="Recall", source_class="XII")

# 017 E
def _c017():
    X = range(1, 16)
    return FiniteSet(*[b for b in X if (3 - b) % 4 == 0])
q("U01-B-017", "Equivalence relations", "Equivalence class in a congruence relation", "Easy",
  "Single-step computation MCQ",
  r"On $X = \{1, 2, 3, \ldots, 15\}$, the relation $R = \{(a, b) : a - b \text{ is divisible by } 4\}$ is an equivalence relation. The equivalence class of $3$ is",
  r"$\{3, 7, 11, 15\}$",
  [(r"$\{7, 11, 15\}$", r"Leaves out $3$ itself, though $(3, 3) \in R$."),
   (r"$\{4, 8, 12\}$", r"Uses '$4$ divides $b$' in place of '$4$ divides $3 - b$'."),
   (r"$\{3, 6, 9, 12, 15\}$", r"Takes the multiples of the representative $3$.")],
  r"$[3] = \{b \in X : 4 \mid (3 - b)\}$, that is, $b \equiv 3 \pmod 4$. In $X$ these are $3, 7, 11, 15$.",
  "Forgetting that an element belongs to its own class.",
  "U01-B-congruence-class", "Direct reading of the class from the definition.",
  check=_c017, values=[FiniteSet(3, 7, 11, 15), FiniteSet(7, 11, 15), FiniteSet(4, 8, 12), FiniteSet(3, 6, 9, 12, 15)],
  cognitive="Understanding", source_class="XII")

# 018 E
def _c018():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X) if _eq(R, X)))
q("U01-B-018", "Counting relations with properties", "Number of equivalence relations on a small set", "Easy",
  "Single-step computation MCQ",
  r"The number of equivalence relations on the set $\{1, 2, 3\}$ is",
  r"$5$",
  [(r"$4$", r"Omits the universal relation $X \times X$ (the partition with one class)."),
   (r"$6$", r"Counts the $3! = 6$ arrangements of the elements instead of the partitions."),
   (r"$8$", r"Counts the $2^3$ subsets of the set.")],
  r"Equivalence relations correspond to partitions: $\{1\}\{2\}\{3\}$; $\{1,2\}\{3\}$; $\{1,3\}\{2\}$; $\{2,3\}\{1\}$; $\{1,2,3\}$. That is $5$ equivalence relations.",
  "Missing the identity or universal relation when listing.",
  "U01-B-count-equivalence-small", "Listing partitions of a three-element set.",
  check=_c018, values=[5, 4, 6, 8], cognitive="Recall", source_class="XII",
  numerical=dict(question=r"The number of equivalence relations on the set $\{1, 2, 3\}$ is", answer=5))

# 019 E statement (T, T)
def _c019():
    X = [1, 2, 3]
    I_X = frozenset((a, a) for a in X)
    E = frozenset()
    return (_eq(I_X, X), _sym(E) and _tr(E))
q("U01-B-019", "Types of relations", "Identity and empty relations", "Easy",
  "Statement-based MCQ",
  r"Let $X$ be a non-empty set. Statement I: The identity relation $I_X = \{(a, a) : a \in X\}$ is an equivalence relation on $X$. Statement II: The empty relation on $X$ is symmetric and transitive." + STEM_TAIL,
  ST_TT,
  [(ST_TF, r"Thinks the empty relation fails symmetry and transitivity because it has no pairs to check, missing that these conditions hold vacuously."),
   (ST_FT, r"Thinks the identity relation is not transitive or not symmetric because it relates no two distinct elements."),
   (ST_FF, r"Rejects both on the grounds that each relation 'has too few pairs'.")],
  r"$I_X$ contains every $(a, a)$, so it is reflexive; $(a, b) \in I_X$ means $a = b$, so symmetry and transitivity hold. The empty relation has no pair $(a, b)$, so the conditions 'if $(a, b) \in R$ then ...' are vacuously true; it is symmetric and transitive (though not reflexive on a non-empty set). Both statements are true.",
  "Thinking vacuous conditions fail.",
  "U01-B-identity-empty-relations", "Direct use of definitions, including the vacuous case.",
  check=_c019, values=[(True, True), (True, False), (False, True), (False, False)],
  cognitive="Understanding", source_class="XII")

# 020 E
q("U01-B-020", "Types of relations", "Perpendicularity of lines", "Easy",
  "Conceptual/application MCQ",
  r"Let $L$ be the set of all lines in a plane, and let $R = \{(\ell_1, \ell_2) : \ell_1 \perp \ell_2\}$ on $L$. Then $R$ is",
  P_S,
  [(P_RS, r"Assumes every line is perpendicular to itself."),
   (P_ST, r"Chains $\ell_1 \perp \ell_2$ and $\ell_2 \perp \ell_3$ into $\ell_1 \perp \ell_3$, though then $\ell_1 \parallel \ell_3$."),
   (P_ALL, r"Treats perpendicularity like parallelism, which is an equivalence relation when a line is taken parallel to itself.")],
  r"No line is perpendicular to itself, so $R$ is not reflexive. If $\ell_1 \perp \ell_2$ then $\ell_2 \perp \ell_1$, so $R$ is symmetric. If $\ell_1 \perp \ell_2$ and $\ell_2 \perp \ell_3$, then $\ell_1 \parallel \ell_3$, not perpendicular, so $R$ is not transitive.",
  "Transferring the properties of parallelism to perpendicularity.",
  "U01-B-geometric-relation", "One geometric fact for each property.",
  check=None, values=None, cognitive="Understanding", source_class="XII")

# 021 E
def _c021():
    S = [Rational(k, 2) for k in range(-6, 7)]
    R = _rel_on(S, lambda a, b: Abs(a - b) <= 1)
    return _props(R, S)
q("U01-B-021", "Types of relations", "Relation defined by a distance condition", "Easy",
  "Conceptual/application MCQ",
  r"On $\mathbb{R}$, define $a\,R\,b$ if and only if $|a - b| \le 1$. Then $R$ is",
  P_RS,
  [(P_ALL, r"Assumes that if $a$ is close to $b$ and $b$ is close to $c$ then $a$ is close to $c$; but $0\,R\,1$, $1\,R\,2$ and $|0 - 2| = 2$."),
   (P_RNN, r"Treats $|a - b|$ and $|b - a|$ as different quantities."),
   (P_S, r"Reads the condition as $0 < |a - b| \le 1$, so that $(a, a)$ fails.")],
  r"$|a - a| = 0 \le 1$, so $R$ is reflexive. $|a - b| = |b - a|$, so it is symmetric. But $0\,R\,1$ and $1\,R\,2$ while $|0 - 2| = 2 > 1$, so it is not transitive.",
  "Assuming 'closeness' chains transitively.",
  "U01-B-distance-relation", "Two quick checks and one counterexample.",
  check=_c021, values=[(True, True, False), (True, True, True), (True, False, False), (False, True, False)],
  cognitive="Understanding", source_class="XII")

# 022 M
def _c022():
    X = [1, 2, 3]
    R = frozenset({(1, 2), (2, 3)})
    closure = _trclose(R | {(a, a) for a in X})
    assert _ref(closure, X) and _tr(closure)
    return Integer(len(closure - R))
q("U01-B-022", "Types of relations", "Minimum pairs to add for reflexive and transitive", "Medium",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, 3\}$ and $R = \{(1, 2), (2, 3)\}$. The minimum number of ordered pairs that must be added to $R$ so that the enlarged relation is reflexive and transitive is",
  r"$4$",
  [(r"$3$", r"Adds only $(1,1), (2,2), (3,3)$ for reflexivity and forgets $(1, 3)$ for transitivity."),
   (r"$1$", r"Adds only $(1, 3)$ for transitivity and forgets the diagonal pairs."),
   (r"$7$", r"Also adds $(2, 1), (3, 2), (3, 1)$, making it an equivalence relation though symmetry is not required.")],
  r"Reflexivity needs $(1,1), (2,2), (3,3)$. Transitivity with $(1, 2), (2, 3)$ needs $(1, 3)$. The relation $\{(1,1), (2,2), (3,3), (1,2), (2,3), (1,3)\}$ is reflexive and transitive, so the minimum number added is $4$.",
  "Making the relation symmetric when only reflexivity and transitivity are asked.",
  "U01-B-minimal-closure", "Two closure requirements combined; a symmetric-closure trap.",
  check=_c022, values=[4, 3, 1, 7], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $X = \{1, 2, 3\}$ and $R = \{(1, 2), (2, 3)\}$. The minimum number of ordered pairs that must be added to $R$ so that the enlarged relation is reflexive and transitive is", answer=4))

# 023 M
def _c023():
    X = [1, 2, 3, 4]
    return Integer(sum(1 for R in _rels(X) if _ref(R, X) and _sym(R)))
q("U01-B-023", "Counting relations with properties", "Reflexive and symmetric relations", "Medium",
  "Multi-step computation MCQ",
  r"The number of relations on $\{1, 2, 3, 4\}$ that are both reflexive and symmetric is",
  r"$64$",
  [(r"$1024$", r"Counts symmetric relations only, $2^{4 + 6}$, leaving the diagonal pairs free."),
   (r"$4096$", r"Counts reflexive relations only, $2^{12}$, treating $(a, b)$ and $(b, a)$ as independent."),
   (r"$729$", r"Gives each of the $6$ unordered pairs three states (neither, one direction, both), though symmetry rules out one direction alone.")],
  r"Reflexivity fixes all $4$ diagonal pairs. Symmetry ties $(a, b)$ to $(b, a)$, so each of the $\binom{4}{2} = 6$ unordered pairs $\{a, b\}$ is either fully in or fully out. Hence the count is $2^{6} = 64$.",
  "Applying only one of the two conditions.",
  "U01-B-count-ref-sym", "Two conditions combined into one free-choice count.",
  check=_c023, values=[64, 1024, 4096, 729], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The number of relations on $\{1, 2, 3, 4\}$ that are both reflexive and symmetric is", answer=64))

# 024 M
def _c024():
    X = [1, 2, 3, 4]
    return Integer(sum(1 for p in _partitions(X) if (1, 2) in _rel_of(p)))
q("U01-B-024", "Counting relations with properties", "Equivalence relations containing a given pair", "Medium",
  "Multi-step computation MCQ",
  r"The number of equivalence relations on $\{1, 2, 3, 4\}$ that contain the ordered pair $(1, 2)$ is",
  r"$5$",
  [(r"$15$", r"Counts all equivalence relations on the set and ignores the condition."),
   (r"$10$", r"Counts the equivalence relations that do not contain $(1, 2)$."),
   (r"$4$", r"Lists $\{1,2\}\{3\}\{4\}$, $\{1,2,3\}\{4\}$, $\{1,2,4\}\{3\}$, $\{1,2,3,4\}$ and misses $\{1,2\}\{3,4\}$.")],
  r"An equivalence relation containing $(1, 2)$ puts $1$ and $2$ in the same class. Merging them into one object, we need partitions of the three objects $\{12\}, 3, 4$, of which there are $5$: all separate; $\{12, 3\}$; $\{12, 4\}$; $\{3, 4\}$; all together.",
  "Missing the partition in which the other two elements form their own class.",
  "U01-B-equivalence-containing-pair", "Reduces to partitions of a smaller set.",
  check=_c024, values=[5, 15, 10, 4], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The number of equivalence relations on $\{1, 2, 3, 4\}$ that contain the ordered pair $(1, 2)$ is", answer=5))

# 025 M
def _c025():
    X = range(1, 11)
    R = _rel_on(X, lambda a, b: (a*a - b*b) % 3 == 0)
    assert _eq(R, X)
    return Integer(len(R))
q("U01-B-025", "Equivalence relations", "Size of an equivalence relation from its classes", "Medium",
  "Multi-step computation MCQ",
  r"On $X = \{1, 2, 3, \ldots, 10\}$, let $R = \{(a, b) : a^2 - b^2 \text{ is divisible by } 3\}$. The number of ordered pairs in $R$ is",
  r"$58$",
  [(r"$34$", r"Replaces the condition by '$a - b$ divisible by $3$', giving classes of sizes $4, 3, 3$ and $16 + 9 + 9$."),
   (r"$48$", r"Leaves out the $10$ pairs $(a, a)$."),
   (r"$24$", r"Counts unordered pairs of distinct elements in the same class, $\binom{3}{2} + \binom{7}{2}$.")],
  r"$a^2 \equiv 0 \pmod 3$ if $3 \mid a$ and $a^2 \equiv 1 \pmod 3$ otherwise. So $a\,R\,b$ exactly when $a, b$ are both multiples of $3$ or both are not. The classes are $\{3, 6, 9\}$ (size $3$) and the other $7$ numbers. Hence $n(R) = 3^2 + 7^2 = 58$.",
  r"Treating $3 \mid (a^2 - b^2)$ as $3 \mid (a - b)$.",
  "U01-B-equivalence-size-squares", "Identify the classes via residues of squares, then sum of squares of class sizes.",
  check=_c025, values=[58, 34, 48, 24], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"On $X = \{1, 2, 3, \ldots, 10\}$, let $R = \{(a, b) : a^2 - b^2 \text{ is divisible by } 3\}$. The number of ordered pairs in $R$ is", answer=58))

# 026 M statement (T, F)
def _c026():
    S = range(1, 13)
    R = _rel_on(S, lambda a, b: b % a == 0)
    return (_ref(R, S) and _tr(R), _sym(R))
q("U01-B-026", "Types of relations", "Divisibility relation on natural numbers", "Medium",
  "Statement-based MCQ",
  r"On $\mathbb{N}$, define $a\,R\,b$ if and only if $a$ divides $b$. Statement I: $R$ is reflexive and transitive. Statement II: $R$ is symmetric." + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Assumes '$a$ divides $b$' implies '$b$ divides $a$', though $1 \mid 2$ and $2 \nmid 1$."),
   (ST_FT, r"Wrongly doubts transitivity of divisibility and also accepts symmetry."),
   (ST_FF, r"Rejects transitivity, thinking $a \mid b$ and $b \mid c$ need not give $a \mid c$.")],
  r"$a \mid a$, so $R$ is reflexive. If $b = ka$ and $c = mb$ then $c = (km)a$, so $R$ is transitive; Statement I is true. But $1 \mid 2$ while $2 \nmid 1$, so $R$ is not symmetric; Statement II is false.",
  "Treating divisibility as symmetric.",
  "U01-B-divisibility-relation", "Two short proofs and one counterexample.",
  check=_c026, values=[(True, False), (True, True), (False, True), (False, False)],
  cognitive="Understanding", source_class="XII")

# 027 M
def _c027():
    X = [1, 2, 3, 4]
    G = {(1, 2), (2, 3)}
    best = [p for p in _partitions(X) if G <= _rel_of(p)]
    return Integer(min(len(_rel_of(p)) for p in best))
q("U01-B-027", "Equivalence relations", "Smallest equivalence relation containing given pairs", "Medium",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, 3, 4\}$. The number of ordered pairs in the smallest equivalence relation on $X$ containing $(1, 2)$ and $(2, 3)$ is",
  r"$10$",
  [(r"$8$", r"Adds the diagonal and the reverses $(2, 1), (3, 2)$ but not $(1, 3), (3, 1)$, so transitivity fails."),
   (r"$9$", r"Builds the class $\{1, 2, 3\}$ correctly but forgets $(4, 4)$."),
   (r"$16$", r"Takes the universal relation $X \times X$, which is an equivalence relation but not the smallest one.")],
  r"The pairs force $1, 2, 3$ into one class, and $4$ may stay alone. The smallest such relation has classes $\{1, 2, 3\}$ and $\{4\}$, so it has $3^2 + 1^2 = 10$ ordered pairs.",
  "Stopping after symmetric closure without completing transitivity, or forgetting reflexive pairs of untouched elements.",
  "U01-B-smallest-equivalence", "Closure under three properties, counted through classes.",
  check=_c027, values=[10, 8, 9, 16], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $X = \{1, 2, 3, 4\}$. The number of ordered pairs in the smallest equivalence relation on $X$ containing $(1, 2)$ and $(2, 3)$ is", answer=10))

# 028 M
q("U01-B-028", "Types of relations", "Relation defined through irrational numbers", "Medium",
  "Conceptual/application MCQ",
  r"On $\mathbb{R}$, define $x\,R\,y$ if and only if $x - y + \sqrt{3}$ is irrational. Then $R$ is",
  P_RNN,
  [(P_RS, r"Assumes $y - x + \sqrt{3}$ is irrational whenever $x - y + \sqrt{3}$ is; but $x = \sqrt{3}, y = 0$ gives $2\sqrt{3}$ and $0$."),
   (P_ALL, r"Checks only reflexivity and assumes the other properties follow."),
   (P_RT, r"Spots the failure of symmetry but assumes transitivity; yet $0\,R\,\sqrt{2}$ and $\sqrt{2}\,R\,\sqrt{3}$ while $0 - \sqrt{3} + \sqrt{3} = 0$.")],
  r"$x - x + \sqrt{3} = \sqrt{3}$ is irrational, so $R$ is reflexive. With $x = \sqrt{3}, y = 0$: $x - y + \sqrt{3} = 2\sqrt{3}$ (irrational) but $y - x + \sqrt{3} = 0$, so $R$ is not symmetric. With $x = 0, y = \sqrt{2}, z = \sqrt{3}$: $\sqrt{3} - \sqrt{2}$ and $\sqrt{2}$ are irrational, so $x\,R\,y$ and $y\,R\,z$, but $x - z + \sqrt{3} = 0$, so $R$ is not transitive.",
  "Assuming symmetry or transitivity without testing a counterexample.",
  "U01-B-irrational-relation", "Needs two well-chosen counterexamples.",
  check=None, values=None, cognitive="Analysis", source_class="XII")

# 029 M
def _c029():
    a, b = symbols('a b', positive=True, integer=True)
    sols = solve([a + b - 6, a**2 + b**2 - 20], [a, b], dict=True)
    return min(min(s[a], s[b]) for s in sols)
q("U01-B-029", "Equivalence relations", "Class sizes from the size of an equivalence relation", "Medium",
  "Inverse/parameter MCQ",
  r"An equivalence relation $R$ on a set with $6$ elements has exactly two equivalence classes, and $R$ contains $20$ ordered pairs. The number of elements in the smaller equivalence class is",
  r"$2$",
  [(r"$4$", r"Solves correctly but reports the larger class."),
   (r"$3$", r"Assumes the two classes are of equal size without using $n(R) = 20$."),
   (r"$1$", r"Counts only pairs with distinct entries, $a(a - 1) + b(b - 1) = 20$, which gives $a^2 + b^2 = 26$ and sizes $1, 5$.")],
  r"If the classes have sizes $a$ and $b$, then $a + b = 6$ and $n(R) = a^2 + b^2 = 20$. So $2ab = 36 - 20 = 16$, $ab = 8$, giving sizes $2$ and $4$. The smaller class has $2$ elements.",
  "Forgetting that $R$ includes the pairs $(x, x)$.",
  "U01-B-class-sizes-reverse", "Reverse use of $n(R) = \\sum (\\text{class size})^2$ with a system of equations.",
  check=_c029, values=[2, 4, 3, 1], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"An equivalence relation $R$ on a set with $6$ elements has exactly two equivalence classes, and $R$ contains $20$ ordered pairs. The number of elements in the smaller equivalence class is", answer=2))

# 030 M
def _c030():
    X = range(1, 11)
    return Integer(sum(1 for a in X for b in X if 2 + b == 5 + a))
q("U01-B-030", "Equivalence relations", "Equivalence class on ordered pairs", "Medium",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, \ldots, 10\}$. On $X \times X$, define $(a, b)\,R\,(c, d)$ if and only if $a + d = b + c$. This is an equivalence relation. The number of elements in the equivalence class of $(2, 5)$ is",
  r"$7$",
  [(r"$6$", r"Leaves out $(2, 5)$ itself."),
   (r"$14$", r"Includes pairs with $a - b = 3$ as well as $b - a = 3$, mixing up the order."),
   (r"$10$", r"Lets $a$ run over all of $X$ without checking $b = a + 3 \le 10$.")],
  r"$(a, b)\,R\,(2, 5)$ means $a + 5 = b + 2$, that is, $b = a + 3$. With $1 \le a$ and $a + 3 \le 10$, $a = 1, 2, \ldots, 7$, so the class $\{(1,4), (2,5), \ldots, (7,10)\}$ has $7$ elements.",
  "Reversing the condition or ignoring the bound on the second entry.",
  "U01-B-class-ordered-pairs", "Translate the relation into a difference condition, then count within bounds.",
  check=_c030, values=[7, 6, 14, 10], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $X = \{1, 2, \ldots, 10\}$. On $X \times X$, define $(a, b)\,R\,(c, d)$ if and only if $a + d = b + c$. This is an equivalence relation. The number of elements in the equivalence class of $(2, 5)$ is", answer=7))

# 031 M
def _c031():
    X = [1, 2]
    return Integer(sum(1 for R in _rels(X) if _tr(R)))
q("U01-B-031", "Counting relations with properties", "Number of transitive relations on a two-element set", "Medium",
  "Multi-step computation MCQ",
  r"The number of transitive relations on the set $\{1, 2\}$ is",
  r"$13$",
  [(r"$15$", r"Rejects only $\{(1, 2), (2, 1)\}$ and misses the two relations that contain both and exactly one diagonal pair."),
   (r"$16$", r"Assumes every relation on a two-element set is transitive."),
   (r"$12$", r"Rejects all four relations containing both $(1, 2)$ and $(2, 1)$, overlooking that the universal relation is transitive.")],
  r"There are $2^4 = 16$ relations. A relation fails transitivity only if it contains both $(1, 2)$ and $(2, 1)$ and misses $(1, 1)$ or $(2, 2)$. Of the $4$ relations containing both, only the universal one has both diagonal pairs, so $3$ fail. Hence $16 - 3 = 13$.",
  "Not checking all chains such as $(1, 2), (2, 1)$ requiring $(1, 1)$.",
  "U01-B-count-transitive-small", "Complementary counting with careful casework.",
  check=_c031, values=[13, 15, 16, 12], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of transitive relations on the set $\{1, 2\}$ is", answer=13))

# 032 M
def _c032():
    from itertools import combinations
    base = [1, 2, 3]
    PS = [frozenset(c) for k in range(4) for c in combinations(base, k)]
    R = _rel_on(PS, lambda P, Q: len(P) == len(Q))
    assert _eq(R, PS)
    return Integer(len(R))
q("U01-B-032", "Equivalence relations", "Equivalence relation on a power set", "Medium",
  "Multi-step computation MCQ",
  r"Let $T$ be the set of all subsets of $\{1, 2, 3\}$. On $T$, define $P\,R\,Q$ if and only if $P$ and $Q$ have the same number of elements. The number of ordered pairs in $R$ is",
  r"$20$",
  [(r"$8$", r"Counts only the pairs $(P, P)$."),
   (r"$4$", r"Gives the number of equivalence classes instead of the number of pairs."),
   (r"$14$", r"Counts unordered pairs within each class, $1 + 6 + 6 + 1$.")],
  r"The classes are the subsets of size $0, 1, 2, 3$, with $1, 3, 3, 1$ members. Within a class every ordered pair is related, so $n(R) = 1^2 + 3^2 + 3^2 + 1^2 = 20$.",
  "Counting classes or unordered pairs instead of ordered pairs.",
  "U01-B-equivalence-power-set", "Recognise classes via binomial sizes, then sum of squares.",
  check=_c032, values=[20, 8, 4, 14], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $T$ be the set of all subsets of $\{1, 2, 3\}$. On $T$, define $P\,R\,Q$ if and only if $P$ and $Q$ have the same number of elements. The number of ordered pairs in $R$ is", answer=20))

# 033 M
def _c033():
    X = range(1, 51)
    ds = lambda n: sum(int(c) for c in str(n))
    R = _rel_on(X, lambda a, b: ds(a) == ds(b))
    assert _eq(R, X)
    classes = {frozenset(b for b in X if (a, b) in R) for a in X}
    return Integer(len(classes))
q("U01-B-033", "Equivalence relations", "Number of equivalence classes", "Medium",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, 3, \ldots, 50\}$. On $X$, define $a\,R\,b$ if and only if $a$ and $b$ have the same sum of decimal digits. This is an equivalence relation. The number of distinct equivalence classes of $R$ is",
  r"$13$",
  [(r"$9$", r"Keeps adding digits until one digit is left (for example $49 \to 13 \to 4$), so only the values $1$ to $9$ appear."),
   (r"$18$", r"Takes every digit sum from $1$ to $9 + 9 = 18$ possible for two-digit numbers, ignoring that $a \le 50$."),
   (r"$14$", r"Counts the digit sums $0, 1, \ldots, 13$, including $0$ although no element of $X$ has digit sum $0$.")],
  r"Each class is the set of elements with one common digit sum, so the number of classes equals the number of distinct digit sums on $X$. The digit sums of $1, \ldots, 9$ give $1$ to $9$; $19, 29, 39, 49$ give $10, 11, 12, 13$; and nothing in $X$ exceeds $4 + 9 = 13$ (for $50$ the sum is $5$). Every value from $1$ to $13$ occurs, so there are $13$ classes.",
  r"Confusing the digit sum with the repeated digit sum (digital root), or allowing digit sums not attained in $X$.",
  "U01-B-classes-digit-sum", "Classes must be identified with the attained values of an invariant, with a range check at both ends.",
  check=_c033, values=[13, 9, 18, 14], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $X = \{1, 2, 3, \ldots, 50\}$. On $X$, define $a\,R\,b$ if and only if $a$ and $b$ have the same sum of decimal digits. The number of distinct equivalence classes of this equivalence relation is", answer=13))

# 034 M
def _c034():
    X = [1, 2, 3, 4]
    return Integer(sum(1 for p in _partitions(X) if len(p) == 2))
q("U01-B-034", "Counting relations with properties", "Equivalence relations with a fixed number of classes", "Medium",
  "Multi-step computation MCQ",
  r"The number of equivalence relations on $\{1, 2, 3, 4\}$ having exactly two equivalence classes is",
  r"$7$",
  [(r"$6$", r"Counts only the splits into two classes of size $2$ and $2$ as $\binom{4}{2}$, without halving and without the $3 + 1$ splits."),
   (r"$14$", r"Counts ordered splits, $2^4 - 2$, treating the two classes as labelled."),
   (r"$8$", r"Fixes the class of $1$ and lets $2, 3, 4$ join it or not ($2^3$ ways), forgetting to exclude the case where all join.")],
  r"Two classes of sizes $3$ and $1$: choose the singleton, $4$ ways. Sizes $2$ and $2$: $\frac{1}{2}\binom{4}{2} = 3$ ways. Total $4 + 3 = 7$.",
  "Treating the classes as labelled.",
  "U01-B-equivalence-k-classes", "Casework on class sizes with an unordered-pair adjustment.",
  check=_c034, values=[7, 6, 14, 8], cognitive="Application", source_class="XII",
  numerical=dict(question=r"The number of equivalence relations on $\{1, 2, 3, 4\}$ having exactly two equivalence classes is", answer=7))

# 035 M
def _c035():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X) if _ref(R, X) and _sym(R) and not _tr(R)))
q("U01-B-035", "Counting relations with properties", "Reflexive, symmetric but not transitive", "Medium",
  "Multi-step computation MCQ",
  r"The number of relations on $\{1, 2, 3\}$ that are reflexive and symmetric but not transitive is",
  r"$3$",
  [(r"$8$", r"Counts all reflexive symmetric relations and ignores 'not transitive'."),
   (r"$5$", r"Counts the equivalence relations, the transitive ones, instead of the non-transitive ones."),
   (r"$6$", r"Assumes only the identity and universal relations are transitive and subtracts $2$ from $8$.")],
  r"A reflexive symmetric relation is fixed by which of the $3$ unordered pairs $\{1,2\}, \{1,3\}, \{2,3\}$ it contains: $2^3 = 8$ relations. It is transitive exactly when it comes from a partition: $0$, $1$ or all $3$ pairs, that is $5$ relations. With exactly $2$ pairs, say $\{1,2\}, \{2,3\}$, transitivity fails. So $3$ relations.",
  "Forgetting that a single linked pair still gives an equivalence relation.",
  "U01-B-count-ref-sym-not-tr", "Combines a count with an equivalence-relation count by complement.",
  check=_c035, values=[3, 8, 5, 6], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of relations on $\{1, 2, 3\}$ that are reflexive and symmetric but not transitive is", answer=3))

# 036 M statement (F, T)
def _c036():
    X = [1, 2, 3]
    E = [_rel_of(p) for p in _partitions(X)]
    union_ok = all(_eq(R1 | R2, X) for R1 in E for R2 in E)
    inter_ok = all(_eq(R1 & R2, X) for R1 in E for R2 in E)
    return (union_ok, inter_ok)
q("U01-B-036", "Equivalence relations", "Union and intersection of equivalence relations", "Medium",
  "Statement-based MCQ",
  r"Let $R_1$ and $R_2$ be equivalence relations on a non-empty set $X$. Statement I: $R_1 \cup R_2$ is always an equivalence relation on $X$. Statement II: $R_1 \cap R_2$ is always an equivalence relation on $X$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Checks that the union is reflexive and symmetric and assumes it is transitive too."),
   (ST_TF, r"Interchanges the roles of union and intersection."),
   (ST_FF, r"Doubts that the intersection keeps transitivity.")],
  r"Intersection: every $(a, a)$ lies in both, symmetry passes to the intersection, and if $(a, b), (b, c)$ lie in both, then $(a, c)$ lies in both; so Statement II is true. Union: on $\{1, 2, 3\}$ take $R_1$ with classes $\{1, 2\}, \{3\}$ and $R_2$ with classes $\{2, 3\}, \{1\}$. Then $(1, 2), (2, 3) \in R_1 \cup R_2$ but $(1, 3) \notin R_1 \cup R_2$, so Statement I is false.",
  "Assuming transitivity survives unions.",
  "U01-B-union-intersection-equivalence", "A general proof and a counterexample.",
  check=_c036, values=[(False, True), (True, True), (True, False), (False, False)],
  cognitive="Analysis", source_class="XII")

# 037 M
def _c037():
    S = range(-40, 41)
    R = _rel_on(S, lambda a, b: a*a - 7*a*b + 6*b*b == 0)
    return _props(R, S)
q("U01-B-037", "Types of relations", "Relation given by a quadratic condition", "Medium",
  "Conceptual/application MCQ",
  r"On $\mathbb{Z}$, define $a\,R\,b$ if and only if $a^2 - 7ab + 6b^2 = 0$. Then $R$ is",
  P_RNN,
  [(P_RS, r"Assumes the condition is symmetric in $a$ and $b$, though the coefficients of $a^2$ and $b^2$ differ; $(6, 1) \in R$ but $(1, 6) \notin R$."),
   (P_RT, r"Spots the failure of symmetry but assumes transitivity; yet $(36, 6), (6, 1) \in R$ and $(36, 1) \notin R$."),
   (P_ALL, r"Checks only $a = b$ and concludes that $R$ is an equivalence relation.")],
  r"$a^2 - 7ab + 6b^2 = (a - b)(a - 6b)$, so $a\,R\,b$ means $a = b$ or $a = 6b$. Reflexive: $a = a$. Not symmetric: $6 = 6 \cdot 1$ but $1 \ne 6$ and $1 \ne 36$. Not transitive: $36\,R\,6$ and $6\,R\,1$, but $36 \ne 1$ and $36 \ne 6$.",
  "Not factorising the condition before testing properties.",
  "U01-B-quadratic-relation", "Factorise, then build two counterexamples.",
  check=_c037, values=[(True, False, False), (True, True, False), (True, False, True), (True, True, True)],
  cognitive="Analysis", source_class="XII")

# 038 D
def _c038():
    X = range(1, 13)
    R = _rel_on(X, lambda a, b: (a - b) % 3 == 0)
    S = _rel_on(X, lambda a, b: (a - b) % 4 == 0)
    return Integer(len(R | S))
q("U01-B-038", "Equivalence relations", "Union of two congruence relations", "Difficult",
  "Multi-step computation MCQ",
  r"On $X = \{1, 2, 3, \ldots, 12\}$, let $R = \{(a, b) : 3 \text{ divides } a - b\}$ and $S = \{(a, b) : 4 \text{ divides } a - b\}$. The number of ordered pairs in $R \cup S$ is",
  r"$72$",
  [(r"$84$", r"Adds $n(R) = 48$ and $n(S) = 36$ without subtracting the common pairs."),
   (r"$60$", r"Subtracts the $12$ common pairs twice."),
   (r"$62$", r"Takes $R \cap S$ to be the pairs with $7 \mid (a - b)$, adding the moduli, which gives $22$ common pairs.")],
  r"$R$ has classes of sizes $4, 4, 4$ (residues modulo $3$), so $n(R) = 48$. $S$ has classes of sizes $3, 3, 3, 3$, so $n(S) = 36$. $(a, b) \in R \cap S$ means $12 \mid (a - b)$, which in $X$ forces $a = b$, so $n(R \cap S) = 12$. Hence $n(R \cup S) = 48 + 36 - 12 = 72$.",
  "Mishandling the intersection of two congruence relations.",
  "U01-B-union-congruence-count", "Class sizes for two relations, then inclusion-exclusion with an lcm insight.",
  check=_c038, values=[72, 84, 60, 62], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"On $X = \{1, 2, 3, \ldots, 12\}$, let $R = \{(a, b) : 3 \text{ divides } a - b\}$ and $S = \{(a, b) : 4 \text{ divides } a - b\}$. The number of ordered pairs in $R \cup S$ is", answer=72))

# ================================================================ CLASS XII Difficult

# 039 D
def _c039():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X) if _sym(R) and _tr(R) and not _ref(R, X)))
q("U01-B-039", "Counting relations with properties", "Symmetric and transitive but not reflexive", "Difficult",
  "Multi-step computation MCQ",
  r"The number of relations on $\{1, 2, 3\}$ that are symmetric and transitive but not reflexive is",
  r"$10$",
  [(r"$15$", r"Counts all symmetric transitive relations and ignores 'not reflexive'."),
   (r"$9$", r"Leaves out the empty relation, which is symmetric and transitive but not reflexive."),
   (r"$5$", r"Gives the number of equivalence relations instead.")],
  r"A symmetric transitive relation is an equivalence relation on the subset $Y$ of elements $a$ with $(a, a) \in R$, since $(a, b) \in R$ forces $(a, a), (b, b) \in R$. So the count is $\sum_k \binom{3}{k} B_k = 1 + 3 \cdot 1 + 3 \cdot 2 + 1 \cdot 5 = 15$, where $B_k$ is the number of partitions of a $k$-set. Those with $Y$ the whole set are the $5$ equivalence relations, so $15 - 5 = 10$ are not reflexive.",
  "Believing symmetry and transitivity force reflexivity, or forgetting the empty relation.",
  "U01-B-count-sym-tr-not-ref", "Requires the structure of symmetric transitive relations and a careful sum over subsets.",
  check=_c039, values=[10, 15, 9, 5], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of relations on $\{1, 2, 3\}$ that are symmetric and transitive but not reflexive is", answer=10))

# 040 D
def _c040():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X) if _ref(R, X) and _tr(R)))
q("U01-B-040", "Counting relations with properties", "Reflexive and transitive relations", "Difficult",
  "Multi-step computation MCQ",
  r"The number of relations on $\{1, 2, 3\}$ that are both reflexive and transitive is",
  r"$29$",
  [(r"$64$", r"Counts all reflexive relations, $2^6$, ignoring transitivity."),
   (r"$19$", r"Counts only those reflexive transitive relations with no two-way pair $(a, b), (b, a)$ for $a \ne b$, missing the $10$ others."),
   (r"$5$", r"Counts only the equivalence relations, adding symmetry.")],
  r"Group by the classes of mutually related elements. All three distinct and no two-way pairs: the off-diagonal part must be a transitive 'one-way' pattern, giving $19$: the identity ($1$), one extra pair ($6$), two extra pairs with a common smallest or common largest element ($6$), and a full chain such as $(1,2), (2,3), (1,3)$ ($6$). With exactly one two-way pair, say $\{1, 2\}$, the block $\{1, 2\}$ relates to $3$ in one of $3$ ways (no link, block to $3$, $3$ to block), giving $3 \times 3 = 9$. With all three mutually related: $1$. Total $19 + 9 + 1 = 29$.",
  "Ignoring two-way pairs or adding symmetry that is not required.",
  "U01-B-count-ref-tr", "Casework over the block structure; easy to miss a family of cases.",
  check=_c040, values=[29, 64, 19, 5], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of relations on $\{1, 2, 3\}$ that are both reflexive and transitive is", answer=29))

# 041 D
def _c041():
    X = [1, 2, 3]
    return Integer(sum(1 for R in _rels(X)
                       if {(1, 2), (2, 3)} <= R and _ref(R, X) and _tr(R) and not _sym(R)))
q("U01-B-041", "Counting relations with properties", "Reflexive transitive extensions of a chain", "Difficult",
  "Multi-step computation MCQ",
  r"The number of relations on $\{1, 2, 3\}$ that contain $(1, 2)$ and $(2, 3)$ and are reflexive and transitive but not symmetric is",
  r"$3$",
  [(r"$4$", r"Includes the universal relation, which is symmetric."),
   (r"$8$", r"Allows every subset of $\{(2,1), (3,2), (3,1)\}$ to be added, without checking transitivity or symmetry."),
   (r"$5$", r"Accepts adding any one of $(2,1), (3,2), (3,1)$ alone, plus the no-addition case and the universal relation, without checking transitivity.")],
  r"Such an $R$ contains the diagonal, $(1,2), (2,3)$ and, by transitivity, $(1,3)$. The only other possible pairs are $(2,1), (3,2), (3,1)$. Adding $(3,1)$ forces $(3,2)$ via $(3,1),(1,2)$ and $(2,1)$ via $(2,3),(3,1)$, giving the universal (symmetric) relation. Adding $(2,1)$ and $(3,2)$ together forces $(3,1)$. So the valid choices are: nothing, $(2,1)$ alone, or $(3,2)$ alone, each of which is transitive and not symmetric. The count is $3$.",
  "Not following forced pairs through transitivity.",
  "U01-B-chain-extensions", "Casework where each addition forces others through transitivity.",
  check=_c041, values=[3, 4, 8, 5], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of relations on $\{1, 2, 3\}$ that contain $(1, 2)$ and $(2, 3)$ and are reflexive and transitive but not symmetric is", answer=3))

# 042 D
def _c042():
    X = [1, 2, 3, 4, 5]
    return Integer(sum(1 for p in _partitions(X) if (1, 2) not in _rel_of(p)))
q("U01-B-042", "Counting relations with properties", "Equivalence relations separating two elements", "Difficult",
  "Multi-step computation MCQ",
  r"The number of equivalence relations on $\{1, 2, 3, 4, 5\}$ in which $1$ and $2$ lie in different equivalence classes is",
  r"$37$",
  [(r"$52$", r"Counts all equivalence relations on the five-element set."),
   (r"$15$", r"Counts the equivalence relations in which $1$ and $2$ lie in the same class."),
   (r"$27$", r"Lets each of $3, 4, 5$ join the class of $1$, the class of $2$ or 'a new class', $3^3$ ways, which misses the different ways $3, 4, 5$ can share new classes.")],
  r"There are $B_5 = 52$ equivalence relations on a five-element set. Those with $1, 2$ in the same class correspond to partitions of the four objects $\{12\}, 3, 4, 5$, so there are $B_4 = 15$ of them. Hence $52 - 15 = 37$.",
  "Undercounting the ways the remaining elements can form new classes.",
  "U01-B-equivalence-separate-pair", "Complementary counting with Bell numbers for $4$ and $5$ elements.",
  check=_c042, values=[37, 52, 15, 27], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of equivalence relations on $\{1, 2, 3, 4, 5\}$ in which $1$ and $2$ lie in different equivalence classes is", answer=37))

# 043 D
def _c043():
    X = range(1, 21)
    def is_pow2_ratio(a, b):
        r = Rational(a, b)
        k = log(r, 2)
        return simplify(2**floor(k) - r) == 0
    R = _rel_on(X, is_pow2_ratio)
    assert _eq(R, X)
    return Integer(len(R))
q("U01-B-043", "Equivalence relations", "Size of an equivalence relation via odd parts", "Difficult",
  "Multi-step computation MCQ",
  r"On $X = \{1, 2, 3, \ldots, 20\}$, define $a\,R\,b$ if and only if $\frac{a}{b} = 2^k$ for some integer $k$ (zero or negative allowed). This is an equivalence relation. The number of ordered pairs in $R$ is",
  r"$56$",
  [(r"$36$", r"Counts only the pairs with $a \ne b$, dropping the $20$ diagonal pairs."),
   (r"$38$", r"Counts unordered pairs, $\frac{56 - 20}{2} + 20$."),
   (r"$10$", r"Gives the number of equivalence classes, one per odd number up to $19$.")],
  r"$a\,R\,b$ exactly when $a$ and $b$ have the same odd part. The classes are $\{1,2,4,8,16\}$, $\{3,6,12\}$, $\{5,10,20\}$, $\{7,14\}$, $\{9,18\}$ and the singletons $\{11\}, \{13\}, \{15\}, \{17\}, \{19\}$. So $n(R) = 25 + 9 + 9 + 4 + 4 + 5 = 56$.",
  "Counting classes or unordered pairs instead of ordered pairs.",
  "U01-B-equivalence-odd-part", "Identify classes by a non-obvious invariant, list them, sum squares.",
  check=_c043, values=[56, 36, 38, 10], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"On $X = \{1, 2, 3, \ldots, 20\}$, define $a\,R\,b$ if and only if $\frac{a}{b} = 2^k$ for some integer $k$ (zero or negative allowed). The number of ordered pairs in this equivalence relation $R$ is", answer=56))

# 044 D
def _c044():
    X = range(1, 7)
    return Integer(sum(1 for p in _partitions(X) if len(_rel_of(p)) == 14))
q("U01-B-044", "Counting relations with properties", "Equivalence relations of a given size", "Difficult",
  "Multi-step computation MCQ",
  r"The number of equivalence relations $R$ on $\{1, 2, 3, 4, 5, 6\}$ such that $R$ contains exactly $14$ ordered pairs is",
  r"$60$",
  [(r"$20$", r"Chooses the three-element class, $\binom{6}{3}$, and forgets to split the remaining three into classes of sizes $2$ and $1$."),
   (r"$120$", r"Computes $\frac{6!}{3!}$ and forgets to divide by $2!$ for the order within the two-element class."),
   (r"$30$", r"Divides by $2$ as if the classes of sizes $2$ and $1$ could be interchanged, though their sizes differ.")],
  r"If the class sizes are $s_1, s_2, \ldots$ with $\sum s_i = 6$, then $n(R) = \sum s_i^2$. Checking partitions of $6$, only $3 + 2 + 1$ gives $9 + 4 + 1 = 14$. The number of ways to split six elements into classes of sizes $3, 2, 1$ is $\frac{6!}{3!\,2!\,1!} = 60$.",
  "Mishandling division by symmetries when class sizes are distinct.",
  "U01-B-equivalence-given-size", "Search over partitions of 6 combined with a multinomial count.",
  check=_c044, values=[60, 20, 120, 30], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of equivalence relations $R$ on $\{1, 2, 3, 4, 5, 6\}$ such that $R$ contains exactly $14$ ordered pairs is", answer=60))

# 045 D statement (F, F)
def _c045():
    S = range(-15, 16)
    R = _rel_on(S, lambda a, b: (a + 2*b) % 3 == 0)
    T = _rel_on(S, lambda a, b: (a + 3*b) % 5 == 0)
    return (not _eq(R, S), _eq(T, S))
q("U01-B-045", "Equivalence relations", "Linear divisibility relations on integers", "Difficult",
  "Statement-based MCQ",
  r"Statement I: The relation $R$ on $\mathbb{Z}$ given by $a\,R\,b$ if and only if $a + 2b$ is divisible by $3$ is not an equivalence relation. Statement II: The relation $T$ on $\mathbb{Z}$ given by $a\,T\,b$ if and only if $a + 3b$ is divisible by $5$ is an equivalence relation." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Judges both relations by appearance, assuming the first is not symmetric because $a + 2b \ne b + 2a$ and the second works because $a + 3b$ resembles a congruence."),
   (ST_TF, r"Doubts the first relation because $a + 2b$ is not symmetric in form, and correctly finds that $T$ fails reflexivity at $a = 1$."),
   (ST_FT, r"Rewrites the first condition correctly as $3 \mid (a - b)$ but does not test $a\,T\,a$, which needs $5 \mid 4a$.")],
  r"Since $a + 2b = (a - b) + 3b$, $3 \mid (a + 2b)$ if and only if $3 \mid (a - b)$, which is congruence modulo $3$, an equivalence relation; so Statement I is false. For $T$, $a\,T\,a$ needs $5 \mid 4a$, which fails for $a = 1$; so $T$ is not reflexive and Statement II is false.",
  "Judging symmetry from the form of the expression rather than from the divisibility condition.",
  "U01-B-linear-divisibility-relations", "Two relations, each needing a rewrite or a reflexivity test; a trap in each.",
  check=_c045, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Analysis", source_class="XII")

# 046 D
def _c046():
    X = [1, 2, 3, 4, 5]
    G = {(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)}
    C = _trclose(G)
    assert _tr(C)
    return Integer(len(C))
q("U01-B-046", "Types of relations", "Smallest transitive relation containing a cycle", "Difficult",
  "Multi-step computation MCQ",
  r"Let $X = \{1, 2, 3, 4, 5\}$. The number of ordered pairs in the smallest transitive relation on $X$ that contains $(1, 2), (2, 3), (3, 4), (4, 5)$ and $(5, 1)$ is",
  r"$25$",
  [(r"$20$", r"Adds every $(a, b)$ with $a \ne b$ but not the pairs $(a, a)$, though for example $(1, 2), (2, 1)$ force $(1, 1)$."),
   (r"$10$", r"Ignores $(5, 1)$ and closes only the chain $1, 2, 3, 4, 5$, giving pairs $(a, b)$ with $a < b$."),
   (r"$15$", r"Takes the pairs $(a, b)$ with $a \le b$, treating the cycle like a chain plus the diagonal.")],
  r"Following the cycle, every element reaches every other element, so $(a, b)$ must be in the relation for all $a \ne b$. Then $(a, b), (b, a)$ force $(a, a)$. So the smallest transitive relation is all of $X \times X$, with $25$ ordered pairs.",
  "Missing that a cycle forces the diagonal pairs.",
  "U01-B-transitive-closure-cycle", "Transitive closure of a cycle; the diagonal is a hidden consequence.",
  check=_c046, values=[25, 20, 10, 15], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"Let $X = \{1, 2, 3, 4, 5\}$. The number of ordered pairs in the smallest transitive relation on $X$ that contains $(1, 2), (2, 3), (3, 4), (4, 5)$ and $(5, 1)$ is", answer=25))

# 047 D
def _c047():
    X = [1, 2, 3, 4]
    return Integer(sum(1 for R in _rels(X) if _sym(R) and len(R) == 6))
q("U01-B-047", "Counting relations with properties", "Symmetric relations of a given size", "Difficult",
  "Multi-step computation MCQ",
  r"The number of symmetric relations on $\{1, 2, 3, 4\}$ containing exactly $6$ ordered pairs is",
  r"$116$",
  [(r"$110$", r"Misses the case of $4$ diagonal pairs with $1$ off-diagonal pair."),
   (r"$96$", r"Misses the case of no diagonal pairs with $3$ off-diagonal pairs."),
   (r"$26$", r"Misses the case of $2$ diagonal pairs with $2$ off-diagonal pairs.")],
  r"A symmetric relation consists of $d$ diagonal pairs and $u$ unordered off-diagonal pairs, each contributing $2$ ordered pairs, so $d + 2u = 6$ with $d \le 4$, $u \le 6$. Cases: $d = 0, u = 3$: $\binom{6}{3} = 20$; $d = 2, u = 2$: $\binom{4}{2}\binom{6}{2} = 90$; $d = 4, u = 1$: $\binom{6}{1} = 6$. Total $20 + 90 + 6 = 116$.",
  "Missing a case in the equation $d + 2u = 6$.",
  "U01-B-count-symmetric-size", "Three-case analysis with binomial counts.",
  check=_c047, values=[116, 110, 96, 26], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"The number of symmetric relations on $\{1, 2, 3, 4\}$ containing exactly $6$ ordered pairs is", answer=116))
