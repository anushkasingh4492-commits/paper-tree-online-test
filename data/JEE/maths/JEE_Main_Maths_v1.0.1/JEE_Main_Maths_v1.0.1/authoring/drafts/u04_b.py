import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

from itertools import combinations, product
from math import gcd as _gcd

# ---------------------------------------------------------------- helpers
ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"


def C(n, r):
    return binomial(n, r)


def ncount(it):
    """Count items of an iterable, returned as a sympy Integer."""
    return Integer(sum(1 for _ in it))


def _col(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]) == 0


def n_triangles(pts):
    return ncount(t for t in combinations(pts, 3) if not _col(*t))


def n_coltriples(pts):
    return ncount(t for t in combinations(pts, 3) if _col(*t))


def n_lines(pts):
    L = set()
    for p, q in combinations(pts, 2):
        a = q[1] - p[1]; b = p[0] - q[0]; c = -(a * p[0] + b * p[1])
        g = _gcd(_gcd(abs(a), abs(b)), abs(c))
        a, b, c = a // g, b // g, c // g
        if a < 0 or (a == 0 and b < 0):
            a, b, c = -a, -b, -c
        L.add((a, b, c))
    return Integer(len(L))


def generic(ts):
    """Points on y = x^2 + 1000 (no three collinear among themselves)."""
    return [(t, t * t + 1000) for t in ts]


def divisors_of(N):
    return [d for d in range(1, N + 1) if N % d == 0]


def rects(w, h):
    """All axis-parallel rectangles on a w x h board of unit squares, as (x1, x2, y1, y2) grid lines."""
    return [(x1, x2, y1, y2) for x1, x2 in combinations(range(w + 1), 2) for y1, y2 in combinations(range(h + 1), 2)]


def people(tag, n):
    return [(tag, i) for i in range(n)]


TOP_P = "Properties of combinations"
TOP_S = "Selections with restrictions"
TOP_G = "Geometric counting"
TOP_D = "Number of divisors"

# ================================================================ EASY (16)

# 001
def _c001():
    ns = [n for n in range(7, 60) if C(n, 7) == C(n, 5)]
    assert len(ns) == 1
    return C(ns[0], 2)
q("U04-B-001", TOP_P, "Equal combinations", "Easy", "Single-step computation MCQ",
  r"If ${}^{n}C_{7} = {}^{n}C_{5}$, then ${}^{n}C_{2}$ equals",
  r"$66$",
  [(r"$132$", r"Finds $n = 12$ but computes ${}^{12}P_{2} = 132$, forgetting to divide by $2!$."),
   (r"$78$", r"Takes $n = 7 + 5 + 1 = 13$ and computes ${}^{13}C_{2} = 78$."),
   (r"$55$", r"Takes $n = 7 + 5 - 1 = 11$ and computes ${}^{11}C_{2} = 55$.")],
  r"Since $7 \ne 5$, ${}^{n}C_{7} = {}^{n}C_{5}$ forces $7 + 5 = n$, so $n = 12$. Then ${}^{12}C_{2} = \frac{12 \cdot 11}{2} = 66$.",
  r"Misremembering the condition ${}^{n}C_{x} = {}^{n}C_{y} \Rightarrow x + y = n$ by one.",
  "U04-B-symmetry-equation", "One property of ${}^{n}C_{r}$ and one evaluation.",
  check=_c001, values=[66, 132, 78, 55], cognitive="Application",
  numerical=dict(question=r"If ${}^{n}C_{7} = {}^{n}C_{5}$, then the value of ${}^{n}C_{2}$ is", answer=66))

# 002
def _c002():
    return C(10, 4) + C(10, 5) + C(11, 6)
q("U04-B-002", TOP_P, "Pascal's rule", "Easy", "Single-step computation MCQ",
  r"The value of ${}^{10}C_{4} + {}^{10}C_{5} + {}^{11}C_{6}$ is",
  r"${}^{12}C_{6}$",
  [(r"${}^{12}C_{5}$", r"Raises the upper index correctly but keeps the lower index $5$: writes ${}^{11}C_{5} + {}^{11}C_{6} = {}^{12}C_{5}$ ($= 792$)."),
   (r"${}^{11}C_{5}$", r"Applies Pascal's rule to the first two terms only (${}^{10}C_{4} + {}^{10}C_{5} = {}^{11}C_{5} = 462$) and drops the third term."),
   (r"${}^{13}C_{6}$", r"Applies Pascal's rule one time too many, raising the upper index to $13$ ($= 1716$).")],
  r"By Pascal's rule ${}^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$: ${}^{10}C_{4} + {}^{10}C_{5} = {}^{11}C_{5}$, and then ${}^{11}C_{5} + {}^{11}C_{6} = {}^{12}C_{6}$ $(= 924)$.",
  r"Mishandling the lower index in Pascal's rule ${}^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$.",
  "U04-B-pascal-chain", "Pascal's rule applied twice.",
  check=_c002, values=[C(12, 6), C(12, 5), C(11, 5), C(13, 6)], cognitive="Application")

# 003
def _c003():
    sols = [(n, r) for n in range(1, 40) for r in range(0, n + 1) if ff(n, r) == 720 and C(n, r) == 120]
    assert len(sols) == 1
    n, r = sols[0]
    return Integer(n + r)
q("U04-B-003", TOP_P, "Relation between P(n, r) and C(n, r)", "Easy", "Single-step computation MCQ",
  r"If ${}^{n}P_{r} = 720$ and ${}^{n}C_{r} = 120$, then $n + r$ equals",
  r"$13$",
  [(r"$10$", r"Finds $n = 10$ and reports it, without adding $r$."),
   (r"$16$", r"Adds $r! = 6$ to $n = 10$ in place of $r = 3$."),
   (r"$7$", r"Computes $n - r = 10 - 3$.")],
  r"${}^{n}P_{r} = r!\,{}^{n}C_{r}$ gives $r! = \frac{720}{120} = 6$, so $r = 3$. Then $n(n-1)(n-2) = 720 = 10 \cdot 9 \cdot 8$, so $n = 10$ and $n + r = 13$.",
  r"Not using ${}^{n}P_{r} = r!\,{}^{n}C_{r}$ cleanly; confusing $r!$ with $r$.",
  "U04-B-perm-comb-relation", r"Single relation ${}^{n}P_{r} = r!\,{}^{n}C_{r}$ and a product to recognise.",
  check=_c003, values=[13, 10, 16, 7], cognitive="Application")

# 004
def _c004():
    M = people('m', 6); W = people('w', 4)
    return ncount(s for s in combinations(M + W, 5) if sum(1 for p in s if p[0] == 'w') == 2)
q("U04-B-004", TOP_S, "Committee with exact composition", "Easy", "Single-step computation MCQ",
  r"A committee of $5$ is to be chosen from $6$ men and $4$ women. The number of committees containing exactly $2$ women is",
  r"$120$",
  [(r"$26$", r"Adds ${}^{4}C_{2} + {}^{6}C_{3} = 6 + 20$ in place of multiplying."),
   (r"$252$", r"Ignores the restriction and counts ${}^{10}C_{5}$."),
   (r"$240$", r"Uses ${}^{4}P_{2} = 12$ for the women, treating the selection as ordered: $12 \times 20$.")],
  r"Choose the $2$ women in ${}^{4}C_{2} = 6$ ways and the remaining $3$ members from the men in ${}^{6}C_{3} = 20$ ways. By the multiplication principle the count is $6 \times 20 = 120$.",
  "Adding instead of multiplying independent choices, or ordering a selection.",
  "U04-B-committee-exact", "Two independent selections multiplied.",
  check=_c004, values=[120, 26, 252, 240], cognitive="Application")

# 005
def _c005():
    n = 15
    return ncount((i, j) for i, j in combinations(range(n), 2) if (j - i) % n not in (1, n - 1))
q("U04-B-005", TOP_G, "Diagonals of a polygon", "Easy", "Single-step computation MCQ",
  r"The number of diagonals of a convex polygon with $15$ sides is",
  r"$90$",
  [(r"$105$", r"Counts all segments ${}^{15}C_{2}$, not removing the $15$ sides."),
   (r"$180$", r"Uses $n(n-3)$ without halving, counting each diagonal from both ends."),
   (r"$75$", r"Subtracts the sides twice: ${}^{15}C_{2} - 2 \times 15$.")],
  r"Any two vertices determine a segment: ${}^{15}C_{2} = 105$. Of these, $15$ are sides, so the number of diagonals is $105 - 15 = 90$, which agrees with $\frac{n(n-3)}{2} = \frac{15 \cdot 12}{2}$.",
  "Counting each diagonal twice or not removing the sides.",
  "U04-B-diagonals", "Direct use of ${}^{n}C_{2} - n$.",
  check=_c005, values=[90, 105, 180, 75], cognitive="Application")

# 006
def _c006():
    return Integer(len(divisors_of(720)))
q("U04-B-006", TOP_D, "Total number of divisors", "Easy", "Single-step computation MCQ",
  r"The number of positive divisors of $720$ is",
  r"$30$",
  [(r"$28$", r"Excludes $1$ and $720$, counting only the proper divisors other than $1$."),
   (r"$8$", r"Multiplies the exponents $4 \cdot 2 \cdot 1$ without adding $1$ to each."),
   (r"$7$", r"Adds the exponents $4 + 2 + 1$.")],
  r"$720 = 2^4 \cdot 3^2 \cdot 5$. A divisor is $2^a 3^b 5^c$ with $0 \le a \le 4$, $0 \le b \le 2$, $0 \le c \le 1$, giving $(4+1)(2+1)(1+1) = 30$ divisors.",
  r"Using the exponents themselves instead of $(\text{exponent} + 1)$ choices.",
  "U04-B-divisor-count", "Prime factorisation and one product.",
  check=_c006, values=[30, 28, 8, 7], cognitive="Application")

# 007
def _c007():
    pts = [(x, 0) for x in range(1, 6)] + generic([7, 11, 13, 17, 19, 23, 29])
    assert n_coltriples(pts) == C(5, 3)
    return n_lines(pts)
q("U04-B-007", TOP_G, "Lines through points with collinearity", "Easy", "Single-step computation MCQ",
  r"There are $12$ points in a plane, of which exactly $5$ lie on one straight line, and no other three of the points are collinear. The number of distinct straight lines obtained by joining pairs of these points is",
  r"$57$",
  [(r"$66$", r"Ignores collinearity and counts ${}^{12}C_{2}$."),
   (r"$56$", r"Subtracts ${}^{5}C_{2}$ but does not add back the one line on which the $5$ points lie."),
   (r"$62$", r"Subtracts $5$ (the number of collinear points) in place of ${}^{5}C_{2}$, then adds $1$.")],
  r"If no three were collinear we would get ${}^{12}C_{2} = 66$ lines. The ${}^{5}C_{2} = 10$ pairs from the collinear points all give the same single line, so the count is $66 - 10 + 1 = 57$.",
  "Not adding back the single common line of the collinear points.",
  "U04-B-lines-collinear", "One correction to ${}^{n}C_{2}$.",
  check=_c007, values=[57, 66, 56, 62], cognitive="Application")

# 008
def _c008():
    B = people('b', 5); G = people('g', 4)
    return ncount(s for s in combinations(B + G, 3) if any(p[0] == 'g' for p in s))
q("U04-B-008", TOP_S, "At least one", "Easy", "Single-step computation MCQ",
  r"From $5$ boys and $4$ girls, a group of $3$ is to be selected so that it contains at least one girl. The number of such groups is",
  r"$74$",
  [(r"$112$", r"Fixes one girl (${}^{4}C_{1}$) and then picks any $2$ of the other $8$: $4 \times 28$, which counts groups with several girls more than once."),
   (r"$84$", r"Ignores the condition and counts ${}^{9}C_{3}$."),
   (r"$10$", r"Computes only the complementary count ${}^{5}C_{3}$ of all-boy groups.")],
  r"Use the complement: total groups ${}^{9}C_{3} = 84$, all-boy groups ${}^{5}C_{3} = 10$. Groups with at least one girl $= 84 - 10 = 74$.",
  "Overcounting by fixing one member of an 'at least one' set.",
  "U04-B-at-least-complement", "One complement subtraction.",
  check=_c008, values=[74, 112, 84, 10], cognitive="Application")

# 009
def _c009():
    return C(12, 5) + 2 * C(12, 4) + C(12, 3)
q("U04-B-009", TOP_P, "Pascal's rule", "Easy", "Single-step computation MCQ",
  r"${}^{12}C_{5} + 2\,{}^{12}C_{4} + {}^{12}C_{3}$ is equal to",
  r"${}^{14}C_{5}$",
  [(r"${}^{13}C_{5}$", r"Applies Pascal's rule once (${}^{12}C_{5} + {}^{12}C_{4} = {}^{13}C_{5}$) and drops the remaining ${}^{13}C_{4}$."),
   (r"${}^{14}C_{6}$", r"Splits the middle term correctly to get ${}^{13}C_{5} + {}^{13}C_{4}$, but then raises the lower index as well, writing ${}^{14}C_{6}$ in place of ${}^{14}C_{5}$."),
   (r"${}^{14}C_{4}$", r"Takes the lower index of the middle term, $4$, for the final answer.")],
  r"Split the middle term: $({}^{12}C_{5} + {}^{12}C_{4}) + ({}^{12}C_{4} + {}^{12}C_{3}) = {}^{13}C_{5} + {}^{13}C_{4} = {}^{14}C_{5}$.",
  r"Losing track of the lower index when using ${}^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$.",
  "U04-B-pascal-chain", "Two applications of Pascal's rule after splitting a term.",
  check=_c009, values=[C(14, 5), C(13, 5), C(14, 6), C(14, 4)], cognitive="Application")

# 010
def _c010():
    P = list(range(11))  # 0, 1 always in; 2 never in
    return ncount(s for s in combinations(P, 5) if 0 in s and 1 in s and 2 not in s)
q("U04-B-010", TOP_S, "Particular persons included or excluded", "Easy", "Single-step computation MCQ",
  r"A team of $5$ is to be chosen from $11$ players such that two particular players are always included and one particular player is always excluded. The number of ways is",
  r"$56$",
  [(r"$84$", r"Handles the inclusion but not the exclusion: ${}^{9}C_{3}$."),
   (r"$28$", r"Reduces the team size by $3$ as well as the pool: ${}^{8}C_{2}$."),
   (r"$70$", r"Reduces the team size by only $1$: ${}^{8}C_{4}$.")],
  r"Put the two compulsory players in the team and remove the excluded player. We must choose the remaining $3$ members from $11 - 3 = 8$ players: ${}^{8}C_{3} = 56$.",
  "Not reducing both the pool and the number to be chosen correctly.",
  "U04-B-include-exclude", "One reduction then one combination.",
  check=_c010, values=[56, 84, 28, 70], cognitive="Application")

# 011
def _c011():
    return Integer(len(rects(8, 8)))
q("U04-B-011", TOP_G, "Rectangles on a chessboard", "Easy", "Single-step computation MCQ",
  r"The number of rectangles (squares included) of all sizes on an ordinary $8 \times 8$ chessboard is",
  r"$1296$",
  [(r"$204$", r"Counts only the squares $1^2 + 2^2 + \cdots + 8^2$."),
   (r"$784$", r"Uses $8$ lines in each direction: $({}^{8}C_{2})^2$."),
   (r"$72$", r"Adds the choices ${}^{9}C_{2} + {}^{9}C_{2}$ in place of multiplying.")],
  r"A rectangle is fixed by choosing $2$ of the $9$ vertical lines and $2$ of the $9$ horizontal lines: ${}^{9}C_{2} \times {}^{9}C_{2} = 36 \times 36 = 1296$.",
  r"Using the number of unit squares ($8$) instead of the number of grid lines ($9$).",
  "U04-B-grid-rectangles", "One product of two combinations.",
  check=_c011, values=[1296, 204, 784, 72], cognitive="Application",
  numerical=dict(question=r"The number of rectangles (squares included) of all sizes on an ordinary $8 \times 8$ chessboard is", answer=1296))

# 012
def _c012():
    # Statement I: 8 lines, no two parallel, no three concurrent; count triangles they form.
    lines = [(Integer(k), Integer(k * k * k + 7 * k)) for k in range(1, 9)]  # y = m x + c, distinct slopes
    def meet(L1, L2):
        (m1, c1), (m2, c2) = L1, L2
        x = (c2 - c1) / (m1 - m2)
        return (x, m1 * x + c1)
    pts = {}
    for i, j in combinations(range(8), 2):
        pts[(i, j)] = meet(lines[i], lines[j])
    assert len(set(pts.values())) == C(8, 2)  # no three concurrent
    tri = ncount(t for t in combinations(range(8), 3)
                 if len({pts[(t[0], t[1])], pts[(t[0], t[2])], pts[(t[1], t[2])]}) == 3)
    s1 = tri == 28
    # Statement II: 9 points on a circle (no three collinear); triangles having a given point P as a vertex.
    circ = [(Rational(1 - t * t, 1 + t * t), Rational(2 * t, 1 + t * t)) for t in range(0, 9)]
    P = circ[0]
    s2 = ncount(s for s in combinations(circ, 3) if P in s and not _col(*s)) == 36
    return (bool(s1), bool(s2))
q("U04-B-012", TOP_G, "Triangles from lines and from points on a circle", "Easy", "Statement-based MCQ",
  r"Statement I: If $8$ straight lines are drawn in a plane so that no two are parallel and no three are concurrent, then the number of triangles formed by these lines is $28$. Statement II: If $9$ distinct points are marked on a circle and $P$ is one of them, then the number of triangles with vertices among these $9$ points that have $P$ as a vertex is $36$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Accepts $28 = {}^{8}C_{2}$ in Statement I, counting pairs of lines (the intersection points) in place of triples, and accepts $36 = {}^{9}C_{2}$ in Statement II, choosing the other two vertices from all $9$ points including $P$."),
   (ST_TF, r"Accepts $28 = {}^{8}C_{2}$ by counting pairs of lines in place of triples, while correctly finding ${}^{8}C_{2} = 28$ for Statement II."),
   (ST_FT, r"Correctly finds ${}^{8}C_{3} = 56$ for Statement I but accepts $36 = {}^{9}C_{2}$ in Statement II, choosing the other two vertices from all $9$ points including $P$.")],
  r"Statement I: any $3$ of the lines meet pairwise in $3$ distinct points (no two parallel, no three concurrent), so each triple of lines forms one triangle and the count is ${}^{8}C_{3} = 56$, not $28$; false. Statement II: no three points of a circle are collinear, so with $P$ fixed the other two vertices are any $2$ of the remaining $8$ points: ${}^{8}C_{2} = 28$, not $36$; false.",
  r"Counting pairs of lines in place of triples, and not removing $P$ from the pool when $P$ is already a vertex.",
  "U04-B-statement-lines-circle", "Two short counts, each with a standard trap.",
  check=_c012, values=[(False, False), (True, True), (True, False), (False, True)], cognitive="Understanding")

# 013
def _c013():
    return ncount(d for d in divisors_of(360) if d % 2 == 0)
q("U04-B-013", TOP_D, "Even divisors", "Easy", "Single-step computation MCQ",
  r"The number of even positive divisors of $360$ is",
  r"$18$",
  [(r"$24$", r"Counts all divisors $(3+1)(2+1)(1+1)$."),
   (r"$6$", r"Counts the odd divisors $(2+1)(1+1)$."),
   (r"$17$", r"Counts the even divisors but then excludes $360$ itself.")],
  r"$360 = 2^3 \cdot 3^2 \cdot 5$. An even divisor $2^a 3^b 5^c$ needs $1 \le a \le 3$, so the count is $3 \cdot 3 \cdot 2 = 18$ (equivalently $24 - 6$).",
  r"Allowing the exponent of $2$ to be $0$ for an even divisor.",
  "U04-B-divisor-parity", "One restricted exponent range.",
  check=_c013, values=[18, 24, 6, 17], cognitive="Application")

# 014
def _c014():
    pts = [(x, 0) for x in range(1, 5)] + generic([5, 7, 11, 13, 17, 19])
    assert n_coltriples(pts) == C(4, 3)
    return n_triangles(pts)
q("U04-B-014", TOP_G, "Triangles with collinear points", "Easy", "Single-step computation MCQ",
  r"There are $10$ points in a plane, of which exactly $4$ are collinear, and no other three of the points are collinear. The number of triangles with vertices at these points is",
  r"$116$",
  [(r"$120$", r"Ignores collinearity and counts ${}^{10}C_{3}$."),
   (r"$114$", r"Subtracts ${}^{4}C_{2} = 6$ in place of ${}^{4}C_{3}$."),
   (r"$117$", r"Subtracts ${}^{4}C_{3}$ and then adds $1$ back, copying the rule for counting lines.")],
  r"Any $3$ points give a triangle unless they are collinear. Total triples ${}^{10}C_{3} = 120$; collinear triples ${}^{4}C_{3} = 4$. Triangles $= 120 - 4 = 116$.",
  "Mixing up the corrections for lines and for triangles.",
  "U04-B-triangles-collinear", "One complement subtraction.",
  check=_c014, values=[116, 120, 114, 117], cognitive="Application")

# 015
def _c015():
    return (bool(C(20, 7) == C(20, 13)), bool(C(10, 3) + C(10, 4) == C(11, 3)))
q("U04-B-015", TOP_P, "Symmetry and Pascal's rule", "Easy", "Statement-based MCQ",
  r"Statement I: ${}^{20}C_{7} = {}^{20}C_{13}$. Statement II: ${}^{10}C_{3} + {}^{10}C_{4} = {}^{11}C_{3}$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II, keeping the smaller lower index in Pascal's rule; the sum is ${}^{11}C_{4} = 330$, while ${}^{11}C_{3} = 165$."),
   (ST_FF, r"Rejects Statement I, not recognising ${}^{n}C_{r} = {}^{n}C_{n-r}$ with $7 + 13 = 20$, and also rejects Statement II."),
   (ST_FT, r"Rejects the symmetry in Statement I and accepts the wrong lower index in Statement II.")],
  r"Statement I: ${}^{n}C_{r} = {}^{n}C_{n-r}$ and $20 - 7 = 13$, so it is true. Statement II: ${}^{10}C_{3} + {}^{10}C_{4} = {}^{11}C_{4} = 330$, while ${}^{11}C_{3} = 165$, so it is false.",
  r"Taking the smaller lower index in ${}^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$.",
  "U04-B-statement-properties", "Two one-line property checks.",
  check=_c015, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Recall")

# 016
def _c016():
    return ncount(t for t in product(range(5), range(4), range(3)) if sum(t) > 0)
q("U04-B-016", TOP_S, "Selection of identical objects", "Easy", "Single-step computation MCQ",
  r"A bag has $4$ identical red balls, $3$ identical blue balls and $2$ identical green balls. The number of ways of selecting at least one ball from the bag is",
  r"$59$",
  [(r"$60$", r"Counts $(4+1)(3+1)(2+1)$ but does not remove the empty selection."),
   (r"$511$", r"Treats all $9$ balls as distinct: $2^9 - 1$."),
   (r"$24$", r"Multiplies $4 \cdot 3 \cdot 2$, not allowing zero balls of a colour.")],
  r"From identical balls we only choose how many of each colour: $5$ choices for red ($0$ to $4$), $4$ for blue, $3$ for green, giving $5 \cdot 4 \cdot 3 = 60$ selections. Removing the empty selection leaves $59$.",
  "Treating identical objects as distinct, or excluding the zero choice per colour.",
  "U04-B-identical-selection", "Choice counts per colour and one subtraction.",
  check=_c016, values=[59, 60, 511, 24], cognitive="Application",
  numerical=dict(question=r"A bag has $4$ identical red balls, $3$ identical blue balls and $2$ identical green balls. The number of ways of selecting at least one ball from the bag is", answer=59))

# ================================================================ MEDIUM (24)

# 017
def _c017():
    sols = [(n, r) for n in range(2, 60) for r in range(1, n) if C(n, r - 1) == 36 and C(n, r) == 84 and C(n, r + 1) == 126]
    assert len(sols) == 1
    return Integer(sols[0][0])
q("U04-B-017", TOP_P, "Consecutive combinations", "Medium", "Inverse/parameter MCQ",
  r"If ${}^{n}C_{r-1} = 36$, ${}^{n}C_{r} = 84$ and ${}^{n}C_{r+1} = 126$, then $n$ equals",
  r"$9$",
  [(r"$10$", r"Uses the ratio $\frac{{}^{n}C_{r}}{{}^{n}C_{r-1}} = \frac{n-r}{r}$ (one less in the numerator); this gives $3n = 10r$ and $2n = 5r + 5$, so $r = 3$, $n = 10$."),
   (r"$12$", r"Solves correctly for $n = 9$, $r = 3$ but reports $n + r$."),
   (r"$6$", r"Solves correctly for $n = 9$, $r = 3$ but reports $n - r$.")],
  r"$\frac{{}^{n}C_{r}}{{}^{n}C_{r-1}} = \frac{n-r+1}{r} = \frac{84}{36} = \frac{7}{3}$ gives $3n + 3 = 10r$. $\frac{{}^{n}C_{r+1}}{{}^{n}C_{r}} = \frac{n-r}{r+1} = \frac{126}{84} = \frac{3}{2}$ gives $2n = 5r + 3$. Solving, $r = 3$ and $n = 9$.",
  r"Misremembering the ratio $\frac{{}^{n}C_{r}}{{}^{n}C_{r-1}} = \frac{n-r+1}{r}$.",
  "U04-B-ratio-consecutive", "Two ratio equations solved simultaneously.",
  check=_c017, values=[9, 10, 12, 6], cognitive="Application",
  numerical=dict(question=r"If ${}^{n}C_{r-1} = 36$, ${}^{n}C_{r} = 84$ and ${}^{n}C_{r+1} = 126$, then the value of $n$ is", answer=9))

# 018
def _c018():
    return C(47, 4) + Add(*[C(52 - j, 3) for j in range(1, 6)])
q("U04-B-018", TOP_P, "Telescoping with Pascal's rule", "Medium", "Multi-step computation MCQ",
  r"The value of ${}^{47}C_{4} + \sum_{j=1}^{5} {}^{52-j}C_{3}$ is",
  r"${}^{52}C_{4}$",
  [(r"${}^{51}C_{4}$", r"Telescopes only the terms ${}^{47}C_{3}$ to ${}^{50}C_{3}$, dropping the $j = 1$ term ${}^{51}C_{3}$."),
   (r"${}^{52}C_{3}$", r"Keeps the lower index $3$ of the summands in the final answer."),
   (r"${}^{53}C_{4}$", r"Raises the upper index once more than the number of terms added.")],
  r"The sum is ${}^{47}C_{4} + {}^{47}C_{3} + {}^{48}C_{3} + {}^{49}C_{3} + {}^{50}C_{3} + {}^{51}C_{3}$. Now ${}^{47}C_{4} + {}^{47}C_{3} = {}^{48}C_{4}$, then ${}^{48}C_{4} + {}^{48}C_{3} = {}^{49}C_{4}$, and so on up to ${}^{51}C_{4} + {}^{51}C_{3} = {}^{52}C_{4}$.",
  "Reading the summation in the wrong order or miscounting the telescoping steps.",
  "U04-B-pascal-telescoping", "Rewrite the sum in increasing order, then five applications of Pascal's rule.",
  check=_c018, values=[C(52, 4), C(51, 4), C(52, 3), C(53, 4)], cognitive="Application")

# 019
def _c019():
    T = 80
    def f(n):
        M = people('m', n); W = people('w', 5)
        return ncount(s for s in combinations(M + W, 3) if sum(1 for p in s if p[0] == 'w') >= 2)
    ns = [n for n in range(1, 30) if f(n) == T]
    assert len(ns) == 1
    return Integer(ns[0])
q("U04-B-019", TOP_S, "At least k of a kind", "Medium", "Inverse/parameter MCQ",
  r"A group of $3$ persons is to be selected from $n$ men and $5$ women. If the number of groups that contain at least $2$ women is $80$, then $n$ equals",
  r"$7$",
  [(r"$8$", r"Counts only the groups with exactly $2$ women: ${}^{5}C_{2} \cdot n = 10n = 80$."),
   (r"$5$", r"Chooses $2$ women first and then any $1$ of the remaining $n + 3$ persons: $10(n + 3) = 80$, which counts each all-women group three times."),
   (r"$4$", r"Solves for at least $1$ woman in place of at least $2$: ${}^{n+5}C_{3} - {}^{n}C_{3} = 80$, which holds for $n = 4$ since $84 - 4 = 80$.")],
  r"Groups with exactly $2$ women: ${}^{5}C_{2} \cdot {}^{n}C_{1} = 10n$. Groups with $3$ women: ${}^{5}C_{3} = 10$. So $10n + 10 = 80$, giving $n = 7$.",
  "Dropping the all-women case, or overcounting by fixing the minimum number first and filling freely.",
  "U04-B-at-least-k-inverse", "Inverse problem: set up the case-wise count in terms of $n$, then solve.",
  check=_c019, values=[7, 8, 5, 4], cognitive="Application",
  numerical=dict(question=r"A group of $3$ persons is to be selected from $n$ men and $5$ women. If the number of groups that contain at least $2$ women is $80$, then the value of $n$ is", answer=7))

# 020
def _c020():
    M = people('m', 8); W = people('w', 5)
    return ncount(s for s in combinations(M + W, 6) if sum(1 for p in s if p[0] == 'w') <= 2)
q("U04-B-020", TOP_S, "At most k of a kind", "Medium", "Multi-step computation MCQ",
  r"A group of $6$ is to be selected from $8$ men and $5$ women so that it contains at most $2$ women. The number of ways is",
  r"$1008$",
  [(r"$700$", r"Counts only the case of exactly $2$ women."),
   (r"$980$", r"Adds the cases of $1$ and $2$ women but omits the case of no woman."),
   (r"$1716$", r"Ignores the restriction and counts ${}^{13}C_{6}$.")],
  r"Cases: $0$ women ${}^{8}C_{6} = 28$; $1$ woman ${}^{5}C_{1}\,{}^{8}C_{5} = 280$; $2$ women ${}^{5}C_{2}\,{}^{8}C_{4} = 700$. Total $28 + 280 + 700 = 1008$.",
  "Forgetting the zero case in an 'at most' count.",
  "U04-B-at-most-k", "Three cases added.",
  check=_c020, values=[1008, 700, 980, 1716], cognitive="Application")

# 021
def _c021():
    lines = people('L', 10); circles = people('O', 5)
    tot = 0
    for a, b in combinations(lines + circles, 2):
        tot += 1 if (a[0] == 'L' and b[0] == 'L') else 2
    return Integer(tot)
q("U04-B-021", TOP_G, "Maximum intersection points", "Medium", "Multi-step computation MCQ",
  r"The greatest possible number of points of intersection of $10$ straight lines and $5$ circles in a plane is",
  r"$165$",
  [(r"$155$", r"Takes two circles to meet in only one point: $45 + 10 + 100$."),
   (r"$115$", r"Takes a line and a circle to meet in only one point: $45 + 20 + 50$."),
   (r"$105$", r"Counts every pair of curves as giving one point: $45 + 10 + 50$.")],
  r"Two lines meet in at most $1$ point, two circles in at most $2$, and a line and a circle in at most $2$. Maximum $= {}^{10}C_{2} \cdot 1 + {}^{5}C_{2} \cdot 2 + 10 \cdot 5 \cdot 2 = 45 + 20 + 100 = 165$.",
  "Assigning one intersection to every pair of curves.",
  "U04-B-max-intersections", "Three types of pairs, each with its own multiplicity.",
  check=_c021, values=[165, 155, 115, 105], cognitive="Application",
  numerical=dict(question=r"The greatest possible number of points of intersection of $10$ straight lines and $5$ circles in a plane is", answer=165))

# 022
def _c022():
    sides = [('s1', i) for i in range(3)] + [('s2', i) for i in range(4)] + [('s3', i) for i in range(5)]
    return ncount(t for t in combinations(sides, 3) if len({p[0] for p in t}) > 1)
q("U04-B-022", TOP_G, "Triangles from points on the sides of a triangle", "Medium", "Multi-step computation MCQ",
  r"On the three sides of a triangle, $3$, $4$ and $5$ points respectively are marked, none of them being a vertex. Three points not on the same side are never collinear. The number of triangles whose vertices are among these $12$ points is",
  r"$205$",
  [(r"$220$", r"Counts all ${}^{12}C_{3}$ triples, ignoring that points on a side are collinear."),
   (r"$60$", r"Counts only triangles with one vertex on each side, $3 \cdot 4 \cdot 5$."),
   (r"$206$", r"Subtracts ${}^{4}C_{3} + {}^{5}C_{3}$ but not ${}^{3}C_{3} = 1$.")],
  r"Total triples ${}^{12}C_{3} = 220$. A triple fails only if all three points lie on one side: ${}^{3}C_{3} + {}^{4}C_{3} + {}^{5}C_{3} = 1 + 4 + 10 = 15$. Triangles $= 220 - 15 = 205$.",
  r"Overlooking the case ${}^{3}C_{3} = 1$, or counting only one-per-side triangles.",
  "U04-B-triangle-sides-points", "Complement with three collinear groups.",
  check=_c022, values=[205, 220, 60, 206], cognitive="Application",
  numerical=dict(question=r"On the three sides of a triangle, $3$, $4$ and $5$ points respectively are marked, none of them being a vertex. Three points not on the same side are never collinear. The number of triangles whose vertices are among these $12$ points is", answer=205))

# 023
def _c023():
    return ncount(r for r in rects(6, 4) if (r[1] - r[0]) != (r[3] - r[2]))
q("U04-B-023", TOP_G, "Non-square rectangles in a grid", "Medium", "Multi-step computation MCQ",
  r"A rectangular board is divided into $6 \times 4$ unit squares ($6$ columns and $4$ rows). The number of rectangles on the board, made of whole unit squares, that are not squares is",
  r"$160$",
  [(r"$210$", r"Counts all rectangles ${}^{7}C_{2} \cdot {}^{5}C_{2}$ without removing the squares."),
   (r"$50$", r"Counts the squares $24 + 15 + 8 + 3$ in place of the non-squares."),
   (r"$40$", r"Uses ${}^{6}C_{2} \cdot {}^{4}C_{2} = 90$ (unit squares in place of grid lines) and subtracts the $50$ squares.")],
  r"Rectangles: choose $2$ of $7$ vertical and $2$ of $5$ horizontal lines, ${}^{7}C_{2} \cdot {}^{5}C_{2} = 21 \cdot 10 = 210$. Squares of side $k$: $(7-k)(5-k)$, giving $24 + 15 + 8 + 3 = 50$. Non-squares $= 210 - 50 = 160$.",
  "Using unit-square counts instead of grid-line counts.",
  "U04-B-grid-rectangles", "Two separate counts and a subtraction.",
  check=_c023, values=[160, 210, 50, 40], cognitive="Application",
  numerical=dict(question=r"A rectangular board is divided into $6 \times 4$ unit squares ($6$ columns and $4$ rows). The number of rectangles on the board, made of whole unit squares, that are not squares is", answer=160))

# 024
def _c024():
    return ncount(d for d in divisors_of(10800) if d % 6 == 0)
q("U04-B-024", TOP_D, "Divisors that are multiples of a given number", "Medium", "Multi-step computation MCQ",
  r"The number of positive divisors of $10800$ that are multiples of $6$ is",
  r"$36$",
  [(r"$60$", r"Counts all divisors $(4+1)(3+1)(2+1)$."),
   (r"$24$", r"Uses $4 \cdot 3 \cdot 2$, not allowing the exponent of $5$ to be $0$."),
   (r"$48$", r"Removes only the $12$ odd divisors, i.e. counts the even divisors.")],
  r"$10800 = 2^4 \cdot 3^3 \cdot 5^2$. A multiple of $6$ among its divisors is $2^a 3^b 5^c$ with $1 \le a \le 4$, $1 \le b \le 3$, $0 \le c \le 2$: $4 \cdot 3 \cdot 3 = 36$.",
  "Dropping the zero exponent for primes that are not forced.",
  "U04-B-divisor-multiples", "Factorise, then restrict two exponent ranges.",
  check=_c024, values=[36, 60, 24, 48], cognitive="Application",
  numerical=dict(question=r"The number of positive divisors of $10800$ that are multiples of $6$ is", answer=36))

# 025
def _c025():
    N = 360
    return ncount((a, N // a) for a in divisors_of(N) if a <= N // a and _gcd(a, N // a) == 1)
q("U04-B-025", TOP_D, "Coprime factorisations", "Medium", "Multi-step computation MCQ",
  r"The number of ways of writing $360$ as a product of two coprime positive integers, the order of the factors being immaterial, is",
  r"$4$",
  [(r"$8$", r"Counts ordered pairs, $2^3$, without halving."),
   (r"$12$", r"Counts all unordered factorisations, $\frac{24}{2}$, ignoring coprimality."),
   (r"$3$", r"Excludes the factorisation $1 \times 360$.")],
  r"$360 = 2^3 \cdot 3^2 \cdot 5$. In coprime factors each prime power $2^3, 3^2, 5$ goes wholly to one factor, giving $2^3 = 8$ ordered pairs. Since $360$ is not a square, unordered pairs number $\frac{8}{2} = 4$.",
  "Splitting a prime power between coprime factors, or not halving for order.",
  "U04-B-coprime-factorisation", "Two ideas: whole prime powers, then halving for order.",
  check=_c025, values=[4, 8, 12, 3], cognitive="Analysis",
  numerical=dict(question=r"The number of ways of writing $360$ as a product of two coprime positive integers, the order of the factors being immaterial, is", answer=4))

# 026
def _c026():
    return ncount(s for s in combinations(range(10), 4) if not (0 in s and 1 in s))
q("U04-B-026", TOP_S, "Two persons never together", "Medium", "Multi-step computation MCQ",
  r"A committee of $4$ is to be chosen from $10$ persons, two of whom, $P$ and $Q$, refuse to serve together. The number of possible committees is",
  r"$182$",
  [(r"$210$", r"Ignores the restriction and counts ${}^{10}C_{4}$."),
   (r"$28$", r"Computes only the committees containing both, ${}^{8}C_{2}$."),
   (r"$154$", r"Subtracts the $28$ committees containing both twice: $210 - 56$.")],
  r"Total ${}^{10}C_{4} = 210$. Committees containing both $P$ and $Q$: choose the other $2$ from $8$, ${}^{8}C_{2} = 28$. Required count $= 210 - 28 = 182$.",
  "Double subtraction of the 'both together' case.",
  "U04-B-never-together", "Complement of a fixed pair.",
  check=_c026, values=[182, 210, 28, 154], cognitive="Application")

# 027
def _c027():
    P1 = people('a', 6); P2 = people('b', 5)
    return ncount(s for s in combinations(P1 + P2, 7)
                  if sum(1 for p in s if p[0] == 'a') >= 3 and sum(1 for p in s if p[0] == 'b') >= 3)
q("U04-B-027", TOP_S, "Selections from two groups with minimums", "Medium", "Multi-step computation MCQ",
  r"A question paper has two parts: Part I with $6$ questions and Part II with $5$ questions. A student must attempt $7$ questions, choosing at least $3$ from each part. The number of ways of choosing the questions is",
  r"$250$",
  [(r"$330$", r"Ignores the restriction and counts ${}^{11}C_{7}$."),
   (r"$1000$", r"Chooses $3$ from each part and then any $1$ of the remaining $5$: $20 \cdot 10 \cdot 5$, which overcounts."),
   (r"$150$", r"Considers only the split $4$ from Part I and $3$ from Part II.")],
  r"Possible splits are $(3, 4)$ and $(4, 3)$. $(3,4)$: ${}^{6}C_{3}\,{}^{5}C_{4} = 20 \cdot 5 = 100$. $(4,3)$: ${}^{6}C_{4}\,{}^{5}C_{3} = 15 \cdot 10 = 150$. Total $250$.",
  "Fixing the minimums first and then choosing the rest freely (overcounting).",
  "U04-B-two-part-minimum", "Casework on two admissible splits.",
  check=_c027, values=[250, 330, 1000, 150], cognitive="Application",
  numerical=dict(question=r"A question paper has two parts: Part I with $6$ questions and Part II with $5$ questions. A student must attempt $7$ questions, choosing at least $3$ from each part. The number of ways of choosing the questions is", answer=250))

# 028
def _c028():
    n = 10
    chords = list(combinations(range(n), 2))
    def cross(c1, c2):
        a, b = c1; c, d = c2
        if len({a, b, c, d}) < 4:
            return False
        return (a < c < b) != (a < d < b)
    return ncount(p for p in combinations(chords, 2) if cross(*p))
q("U04-B-028", TOP_G, "Intersections of chords", "Medium", "Conceptual/application MCQ",
  r"Ten points are marked on a circle and every pair of them is joined by a chord. If no three chords pass through a common point inside the circle, the number of points of intersection of the chords lying inside the circle is",
  r"$210$",
  [(r"$990$", r"Counts all pairs of chords, ${}^{45}C_{2}$, including pairs that meet on the circle or not at all."),
   (r"$45$", r"Counts the chords ${}^{10}C_{2}$."),
   (r"$420$", r"Takes each set of $4$ points to give two interior intersections.")],
  r"Two chords cross inside the circle exactly when their four endpoints are distinct and alternate around the circle. Each set of $4$ points has exactly one such pairing (the two diagonals of the quadrilateral), so the count is ${}^{10}C_{4} = 210$.",
  r"Not seeing the bijection between interior intersection points and $4$-point subsets.",
  "U04-B-chord-intersections", "Needs a bijection to 4-point subsets.",
  check=_c028, values=[210, 990, 45, 420], cognitive="Analysis",
  numerical=dict(question=r"Ten points are marked on a circle and every pair of them is joined by a chord. If no three chords pass through a common point inside the circle, the number of points of intersection of the chords lying inside the circle is", answer=210))

# 029
def _c029():
    n = 10
    def adj(i, j):
        return (i - j) % n in (1, n - 1)
    return ncount(t for t in combinations(range(n), 3)
                  if sum(1 for i, j in combinations(t, 2) if adj(i, j)) == 1)
q("U04-B-029", TOP_G, "Triangles sharing sides with a polygon", "Medium", "Multi-step computation MCQ",
  r"The number of triangles whose vertices are vertices of a regular decagon ($10$ sides) and which have exactly one side in common with the decagon is",
  r"$60$",
  [(r"$80$", r"Uses $10 \times 8$: for each side, any of the other $8$ vertices, which includes the triangles with two common sides."),
   (r"$50$", r"Uses $10 \times 5$, excluding one vertex too many for each side."),
   (r"$70$", r"Starts from $80$ and subtracts the $10$ two-side triangles only once, though each was counted twice.")],
  r"Fix a side of the decagon. The third vertex must not be either endpoint nor adjacent to either endpoint, else a second side is shared. That leaves $10 - 4 = 6$ vertices, so the count is $10 \times 6 = 60$.",
  "Not excluding the vertices adjacent to the chosen side.",
  "U04-B-polygon-triangle-sides", "Exclusion of adjacent vertices for each side.",
  check=_c029, values=[60, 80, 50, 70], cognitive="Analysis")

# 030
def _c030():
    ns = [n for n in range(4, 60) if n * (n - 3) / 2 == 44]
    assert len(ns) == 1
    return C(ns[0], 3)
q("U04-B-030", TOP_G, "Diagonals and triangles of a polygon", "Medium", "Multi-step computation MCQ",
  r"A convex polygon has $44$ diagonals. The number of triangles whose vertices are vertices of this polygon is",
  r"$165$",
  [(r"$990$", r"Finds $n = 11$ but counts ordered triples ${}^{11}P_{3}$."),
   (r"$55$", r"Finds $n = 11$ but computes ${}^{11}C_{2}$."),
   (r"$330$", r"Finds $n = 11$ but computes ${}^{11}C_{4}$.")],
  r"$\frac{n(n-3)}{2} = 44$ gives $n^2 - 3n - 88 = 0$, so $n = 11$. No three vertices of a convex polygon are collinear, so the number of triangles is ${}^{11}C_{3} = 165$.",
  "Ordering a selection of vertices, or using the wrong r.",
  "U04-B-diagonals", "Inverse step to find n, then one selection.",
  check=_c030, values=[165, 990, 55, 330], cognitive="Application")

# 031
def _c031():
    L1 = [(x, 0) for x in range(1, 7)]
    L2 = [(x, 3 * x + 1) for x in range(1, 6)]
    pts = L1 + L2 + generic([41, 53, 67, 79])
    assert n_coltriples(pts) == C(6, 3) + C(5, 3)
    return n_lines(pts)
q("U04-B-031", TOP_G, "Lines with two collinear groups", "Medium", "Multi-step computation MCQ",
  r"Of $15$ points in a plane, $6$ lie on a line $\ell_1$ and $5$ others lie on a different line $\ell_2$; the point where $\ell_1$ and $\ell_2$ meet is not one of the $15$ points. Apart from these, no three of the points are collinear. The number of distinct lines through at least two of the points is",
  r"$82$",
  [(r"$105$", r"Counts ${}^{15}C_{2}$, ignoring both collinear groups."),
   (r"$80$", r"Subtracts ${}^{6}C_{2} + {}^{5}C_{2}$ but does not add back the lines $\ell_1$ and $\ell_2$."),
   (r"$81$", r"Subtracts both groups but adds back only one line.")],
  r"Start with ${}^{15}C_{2} = 105$. The ${}^{6}C_{2} = 15$ pairs on $\ell_1$ give one line, and the ${}^{5}C_{2} = 10$ pairs on $\ell_2$ give one line. So the count is $105 - 15 - 10 + 2 = 82$.",
  "Not adding back each collinear line once.",
  "U04-B-lines-collinear", "Two collinear groups, each corrected separately.",
  check=_c031, values=[82, 105, 80, 81], cognitive="Application",
  numerical=dict(question=r"Of $15$ points in a plane, $6$ lie on a line $\ell_1$ and $5$ others lie on a different line $\ell_2$; the point where $\ell_1$ and $\ell_2$ meet is not one of the $15$ points. Apart from these, no three of the points are collinear. The number of distinct lines through at least two of the points is", answer=82))

# 032
def _c032():
    pts = [(x, 0) for x in range(1, 8)] + [(x, 1) for x in range(1, 6)]
    return n_triangles(pts)
q("U04-B-032", TOP_G, "Triangles from points on two parallel lines", "Medium", "Multi-step computation MCQ",
  r"There are $7$ points on a line $\ell_1$ and $5$ points on a line $\ell_2$ parallel to $\ell_1$. The number of triangles whose vertices are among these $12$ points is",
  r"$175$",
  [(r"$220$", r"Counts all ${}^{12}C_{3}$ triples, ignoring collinearity."),
   (r"$105$", r"Counts only triangles with two vertices on $\ell_1$, ${}^{7}C_{2} \cdot 5$."),
   (r"$185$", r"Subtracts ${}^{7}C_{3} = 35$ but not ${}^{5}C_{3} = 10$.")],
  r"A triangle needs two vertices on one line and one on the other: ${}^{7}C_{2} \cdot 5 + {}^{5}C_{2} \cdot 7 = 105 + 70 = 175$. (Check: $220 - 35 - 10 = 175$.)",
  "Missing one of the two configurations or one collinear group.",
  "U04-B-triangles-two-lines", "Two cases or a double complement.",
  check=_c032, values=[175, 220, 105, 185], cognitive="Application",
  numerical=dict(question=r"There are $7$ points on a line $\ell_1$ and $5$ points on a line $\ell_2$ parallel to $\ell_1$. The number of triangles whose vertices are among these $12$ points is", answer=175))

# 033
def _c033():
    sq = ncount(r for r in rects(5, 5) if r[1] - r[0] == r[3] - r[2])
    lat = [(i, j) for i in range(3) for j in range(3)]
    return (bool(sq == 55), bool(n_lines(lat) == 20))
q("U04-B-033", TOP_G, "Squares in a grid and lines through lattice points", "Medium", "Statement-based MCQ",
  r"Statement I: The number of squares of all sizes on a $5 \times 5$ board of unit squares is $55$. Statement II: The number of distinct straight lines that pass through at least two of the $9$ points $(x, y)$ with $x, y \in \{0, 1, 2\}$ is $20$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Rejects $55$ by counting only $5^2 = 25$ unit squares, and rejects $20$ by using ${}^{9}C_{2} = 36$, ignoring collinearity."),
   (ST_TF, r"Accepts $55$ but corrects only for the $3$ rows and $3$ columns, getting $36 - 6 \cdot 3 + 6 = 24$ lines, so rejects $20$."),
   (ST_FT, r"Rejects $55$ (for example, using $({}^{6}C_{2})^2 = 225$ rectangles) while accepting $20$.")],
  r"Statement I: squares of side $k$ number $(6-k)^2$, so the total is $25 + 16 + 9 + 4 + 1 = 55$; true. Statement II: there are ${}^{9}C_{2} = 36$ pairs. Exactly $8$ lines contain $3$ of the points ($3$ rows, $3$ columns, $2$ diagonals); each accounts for ${}^{3}C_{2} = 3$ pairs but is one line, and every other line contains exactly $2$ points. So the number of lines is $36 - 8 \cdot 3 + 8 = 20$; true.",
  "Forgetting the diagonal lines that carry three points; confusing squares with rectangles.",
  "U04-B-statement-grid-lines", "Two independent counts, each with a trap.",
  check=_c033, values=[(True, True), (False, False), (True, False), (False, True)], cognitive="Analysis")

# 034
def _c034():
    return ncount(t for t in combinations(range(1, 22), 3) if sum(t) % 2 == 0)
q("U04-B-034", TOP_S, "Selections with a parity condition", "Medium", "Multi-step computation MCQ",
  r"The number of ways of choosing three distinct numbers from $\{1, 2, 3, \ldots, 21\}$ so that their sum is even is",
  r"$670$",
  [(r"$665$", r"Assumes half of the ${}^{21}C_{3} = 1330$ selections have an even sum."),
   (r"$120$", r"Counts only the case of three even numbers, ${}^{10}C_{3}$."),
   (r"$550$", r"Counts only the case of two odd and one even number, ${}^{11}C_{2} \cdot 10$.")],
  r"There are $11$ odd and $10$ even numbers. An even sum needs $0$ or $2$ odd numbers: ${}^{10}C_{3} + {}^{11}C_{2} \cdot {}^{10}C_{1} = 120 + 550 = 670$.",
  "Assuming symmetry between even and odd sums when the classes are unequal.",
  "U04-B-parity-selection", "Classify by parity, then two cases.",
  check=_c034, values=[670, 665, 120, 550], cognitive="Analysis",
  numerical=dict(question=r"The number of ways of choosing three distinct numbers from $\{1, 2, 3, \ldots, 21\}$ so that their sum is even is", answer=670))

# 035
def _c035():
    ok = [n for n in range(10, 80) if all(C(n, 10) >= C(n, r) for r in range(n + 1))]
    return Integer(sum(ok))
q("U04-B-035", TOP_P, "Greatest value of C(n, r)", "Medium", "Inverse/parameter MCQ",
  r"For a positive integer $n \ge 10$, ${}^{n}C_{10} \ge {}^{n}C_{r}$ holds for every $r = 0, 1, \ldots, n$. The sum of all possible values of $n$ is",
  r"$60$",
  [(r"$20$", r"Takes only $n = 20$, where ${}^{n}C_{10}$ is the unique largest term."),
   (r"$41$", r"Requires $\lfloor n/2 \rfloor = 10$, giving $n = 20, 21$ and missing $n = 19$."),
   (r"$39$", r"Requires $\lceil n/2 \rceil = 10$, giving $n = 19, 20$ and missing $n = 21$.")],
  r"${}^{n}C_{r}$ is largest at $r = \frac{n}{2}$ for even $n$, and at both $r = \frac{n-1}{2}$ and $r = \frac{n+1}{2}$ for odd $n$. So $r = 10$ gives a largest value when $n = 20$, or $n = 19$ (as $\frac{n+1}{2} = 10$), or $n = 21$ (as $\frac{n-1}{2} = 10$). Sum $= 19 + 20 + 21 = 60$.",
  "Forgetting that odd n has two equal middle coefficients.",
  "U04-B-greatest-ncr", "Parity casework on where the maximum occurs.",
  check=_c035, values=[60, 20, 41, 39], cognitive="Analysis",
  numerical=dict(question=r"For a positive integer $n \ge 10$, ${}^{n}C_{10} \ge {}^{n}C_{r}$ holds for every $r = 0, 1, \ldots, n$. The sum of all possible values of $n$ is", answer=60))

# 036
def _c036():
    cells = [(r, c) for r in range(8) for c in range(8)]
    return ncount(p for p in combinations(cells, 2) if p[0][0] != p[1][0] and p[0][1] != p[1][1])
q("U04-B-036", TOP_G, "Squares on a chessboard", "Medium", "Multi-step computation MCQ",
  r"Two distinct squares are chosen from the $64$ squares of an $8 \times 8$ chessboard. The number of ways of choosing them so that they are neither in the same row nor in the same column is",
  r"$1568$",
  [(r"$2016$", r"Counts all ${}^{64}C_{2}$ pairs, ignoring the condition."),
   (r"$1792$", r"Subtracts only the same-row pairs $8 \cdot {}^{8}C_{2} = 224$."),
   (r"$3136$", r"Counts $64 \times 49$ ordered choices without halving.")],
  r"Choose the first square in $64$ ways and the second outside its row and column in $49$ ways; each unordered pair is counted twice, giving $\frac{64 \cdot 49}{2} = 1568$. Equivalently ${}^{64}C_{2} - 2 \cdot 8 \cdot {}^{8}C_{2} = 2016 - 448 = 1568$.",
  "Treating an unordered selection as ordered, or removing only one kind of bad pair.",
  "U04-B-chessboard-pairs", "Complement with two exclusions, or ordered count halved.",
  check=_c036, values=[1568, 2016, 1792, 3136], cognitive="Application",
  numerical=dict(question=r"Two distinct squares are chosen from the $64$ squares of an $8 \times 8$ chessboard. The number of ways of choosing them so that they are neither in the same row nor in the same column is", answer=1568))

# 037
def _c037():
    Bk = people('p', 3) + people('c', 4) + people('m', 5)
    return ncount(s for s in combinations(Bk, 4) if {p[0] for p in s} == {'p', 'c', 'm'})
q("U04-B-037", TOP_S, "At least one from each group", "Medium", "Multi-step computation MCQ",
  r"There are $3$ different Physics books, $4$ different Chemistry books and $5$ different Mathematics books. The number of ways of selecting $4$ books so that there is at least one book of each subject is",
  r"$270$",
  [(r"$540$", r"Picks one book of each subject ($3 \cdot 4 \cdot 5$) and then any $1$ of the remaining $9$, double counting."),
   (r"$495$", r"Ignores the condition and counts ${}^{12}C_{4}$."),
   (r"$120$", r"Counts only the case with two Mathematics books, $3 \cdot 4 \cdot {}^{5}C_{2}$.")],
  r"One subject contributes $2$ books. Two Physics: ${}^{3}C_{2} \cdot 4 \cdot 5 = 60$; two Chemistry: $3 \cdot {}^{4}C_{2} \cdot 5 = 90$; two Mathematics: $3 \cdot 4 \cdot {}^{5}C_{2} = 120$. Total $270$.",
  "Fill-the-minimum-then-choose-freely overcount.",
  "U04-B-each-group-minimum", "Three cases after identifying the repeated subject.",
  check=_c037, values=[270, 540, 495, 120], cognitive="Application",
  numerical=dict(question=r"There are $3$ different Physics books, $4$ different Chemistry books and $5$ different Mathematics books. The number of ways of selecting $4$ books so that there is at least one book of each subject is", answer=270))

# 038
def _c038():
    N = 2**6 * 3**5
    D = divisors_of(N)
    is_sq = lambda d: integer_nthroot(d, 2)[1]
    is_cu = lambda d: integer_nthroot(d, 3)[1]
    s1 = ncount(d for d in D if is_cu(d)) == 2
    s2 = ncount(d for d in D if is_sq(d) or is_cu(d)) == 16
    return (bool(s1), bool(s2))
q("U04-B-038", TOP_D, "Square and cube divisors", "Medium", "Statement-based MCQ",
  r"Let $N = 2^6 \cdot 3^5$. Statement I: The number of positive divisors of $N$ that are perfect cubes is $2$. Statement II: The number of positive divisors of $N$ that are perfect squares or perfect cubes (or both) is $16$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts $2$ in Statement I by taking $\lfloor 6/3 \rfloor \cdot \lfloor 5/3 \rfloor = 2 \cdot 1$, forgetting the exponent $0$, and accepts Statement II."),
   (ST_FF, r"Gets $6$ cube divisors for Statement I correctly but adds the squares and cubes, $12 + 6 = 18$, without removing the $2$ divisors that are both, and so rejects Statement II."),
   (ST_TF, r"Accepts $2$ in Statement I by forgetting the exponent $0$, and rejects Statement II after adding $12 + 6 = 18$ without removing the overlap.")],
  r"A divisor is $2^a 3^b$ with $0 \le a \le 6$, $0 \le b \le 5$. Cubes need $a \in \{0, 3, 6\}$ and $b \in \{0, 3\}$: $3 \cdot 2 = 6$ divisors, so Statement I is false. Squares need $a \in \{0, 2, 4, 6\}$ and $b \in \{0, 2, 4\}$: $12$ divisors. Both (sixth powers) need $a \in \{0, 6\}$, $b = 0$: $2$ divisors. Squares or cubes: $12 + 6 - 2 = 16$, so Statement II is true.",
  "Omitting the zero exponent, or not removing the overlap when counting squares or cubes.",
  "U04-B-statement-power-divisors", "Two restricted exponent counts and an overlap correction.",
  check=_c038, values=[(False, True), (True, True), (False, False), (True, False)], cognitive="Analysis")

# 039
def _c039():
    N = factorial(10)
    return ncount(d for d in divisors(N) if integer_nthroot(d, 2)[1])
q("U04-B-039", TOP_D, "Perfect-square divisors", "Medium", "Multi-step computation MCQ",
  r"The number of positive divisors of $10!$ that are perfect squares is",
  r"$30$",
  [(r"$270$", r"Counts all divisors $(8+1)(4+1)(2+1)(1+1)$."),
   (r"$60$", r"Allows two choices for the exponent of $7$ (that is, $0$ or $1$)."),
   (r"$12$", r"Finds the exponents in $10!$ using only $\lfloor 10/p \rfloor$, getting $2^5 3^3 5^2 7$, and then counts $3 \cdot 2 \cdot 2 \cdot 1$.")],
  r"By Legendre's formula $10! = 2^8 \cdot 3^4 \cdot 5^2 \cdot 7$. A square divisor needs even exponents: $2$ has $\{0,2,4,6,8\}$ ($5$ choices), $3$ has $3$, $5$ has $2$, and $7$ only $0$. So the count is $5 \cdot 3 \cdot 2 \cdot 1 = 30$.",
  "Wrong prime exponents in a factorial, or allowing odd exponents.",
  "U04-B-square-divisors", "Legendre's formula then restricted exponents.",
  check=_c039, values=[30, 270, 60, 12], cognitive="Application",
  numerical=dict(question=r"The number of positive divisors of $10!$ that are perfect squares is", answer=30))

# 040
def _c040():
    return Add(*[k * C(10, k) / C(10, k - 1) for k in range(1, 11)])
q("U04-B-040", TOP_P, "Ratio of consecutive combinations", "Medium", "Multi-step computation MCQ",
  r"The value of $\sum_{r=1}^{10} r \cdot \frac{{}^{10}C_{r}}{{}^{10}C_{r-1}}$ is",
  r"$55$",
  [(r"$45$", r"Uses $\frac{{}^{n}C_{r}}{{}^{n}C_{r-1}} = \frac{n-r}{r}$, so each term is $10 - r$ and the sum is $45$."),
   (r"$110$", r"Uses the ratio $\frac{n+1}{r}$, so every term is $11$."),
   (r"$100$", r"Uses the ratio $\frac{n}{r}$, so every term is $10$.")],
  r"$\frac{{}^{10}C_{r}}{{}^{10}C_{r-1}} = \frac{11 - r}{r}$, so $r \cdot \frac{{}^{10}C_{r}}{{}^{10}C_{r-1}} = 11 - r$. Summing over $r = 1$ to $10$ gives $10 + 9 + \cdots + 1 = 55$.",
  r"Misremembering $\frac{{}^{n}C_{r}}{{}^{n}C_{r-1}} = \frac{n-r+1}{r}$.",
  "U04-B-ratio-consecutive", "Ratio identity then an arithmetic series.",
  check=_c040, values=[55, 45, 110, 100], cognitive="Application",
  numerical=dict(question=r"The value of $\sum_{r=1}^{10} r \cdot \frac{{}^{10}C_{r}}{{}^{10}C_{r-1}}$ is", answer=55))

# ================================================================ DIFFICULT (13)

# 041
def _c041():
    letters = list("EXAMINATION")
    return Integer(len({tuple(sorted(s)) for s in combinations(letters, 4)}))
q("U04-B-041", TOP_S, "Selections from a word with repeated letters", "Difficult", "Multi-step computation MCQ",
  r"The number of different selections (not arrangements) of $4$ letters that can be made from the letters of the word EXAMINATION is",
  r"$136$",
  [(r"$70$", r"Counts only selections of $4$ different letters, ${}^{8}C_{4}$."),
   (r"$133$", r"Counts all-different and one-pair selections ($70 + 63$) but misses the $3$ two-pair selections."),
   (r"$330$", r"Treats the $11$ letters as distinct and counts ${}^{11}C_{4}$.")],
  r"EXAMINATION has $11$ letters: A, I, N twice each and E, X, M, T, O once, so $8$ distinct letters. All different: ${}^{8}C_{4} = 70$. One pair and two other different letters: ${}^{3}C_{1} \cdot {}^{7}C_{2} = 63$. Two pairs: ${}^{3}C_{2} = 3$. Total $70 + 63 + 3 = 136$.",
  "Treating repeated letters as distinct or missing a case of the repetition pattern.",
  "U04-B-word-selection", "Three-case split on repeated letters.",
  check=_c041, values=[136, 70, 133, 330], cognitive="Analysis",
  numerical=dict(question=r"The number of different selections (not arrangements) of $4$ letters that can be made from the letters of the word EXAMINATION is", answer=136))

# 042
def _c042():
    return ncount(t for t in combinations(range(1, 21), 3) if t[1] - t[0] > 1 and t[2] - t[1] > 1)
q("U04-B-042", TOP_S, "No two consecutive", "Difficult", "Multi-step computation MCQ",
  r"The number of ways of choosing three numbers from $\{1, 2, 3, \ldots, 20\}$ such that no two of the chosen numbers are consecutive integers is",
  r"$816$",
  [(r"$680$", r"Uses ${}^{n-r}C_{r} = {}^{17}C_{3}$ for the gap method."),
   (r"$798$", r"Subtracts $19 \cdot 18 = 342$ triples containing a consecutive pair from $1140$, not adding back the $18$ triples of three consecutive numbers counted twice."),
   (r"$969$", r"Uses ${}^{n-r+2}C_{r} = {}^{19}C_{3}$ for the gap method.")],
  r"If $a < b < c$ are chosen with gaps of at least $2$, put $a' = a$, $b' = b - 1$, $c' = c - 2$; then $1 \le a' < b' < c' \le 18$ and the map is a bijection. So the count is ${}^{18}C_{3} = 816$, that is ${}^{n-r+1}C_{r}$ with $n = 20$, $r = 3$.",
  "Misapplying the shift in the gap method, or one-sided inclusion-exclusion.",
  "U04-B-no-consecutive", "Needs the shifting bijection or careful inclusion-exclusion.",
  check=_c042, values=[816, 680, 798, 969], cognitive="Analysis",
  numerical=dict(question=r"The number of ways of choosing three numbers from $\{1, 2, 3, \ldots, 20\}$ such that no two of the chosen numbers are consecutive integers is", answer=816))

# 043
def _c043():
    n = 12
    def adj(i, j):
        return (i - j) % n in (1, n - 1)
    return ncount(t for t in combinations(range(n), 3) if not any(adj(i, j) for i, j in combinations(t, 2)))
q("U04-B-043", TOP_G, "Triangles with no side common with a polygon", "Difficult", "Multi-step computation MCQ",
  r"The number of triangles whose vertices are vertices of a regular $12$-sided polygon and none of whose sides is a side of the polygon is",
  r"$112$",
  [(r"$124$", r"Removes the $12 \cdot 8 = 96$ triangles with exactly one common side but not the $12$ with two common sides."),
   (r"$100$", r"Removes $12 \cdot 10 = 120$ (side plus any third vertex), which removes each two-side triangle twice."),
   (r"$208$", r"Removes only the $12$ triangles with two common sides.")],
  r"Total ${}^{12}C_{3} = 220$. Two common sides (three consecutive vertices): $12$. Exactly one common side: for each side, the third vertex avoids the $2$ endpoints and their $2$ neighbours, so $12 \cdot 8 = 96$. Required count $= 220 - 96 - 12 = 112$ (agreeing with $\frac{n(n-4)(n-5)}{6}$).",
  "Overlapping cases when removing triangles that share sides.",
  "U04-B-polygon-triangle-sides", "Case split with overlap control.",
  check=_c043, values=[112, 124, 100, 208], cognitive="Analysis",
  numerical=dict(question=r"The number of triangles whose vertices are vertices of a regular $12$-sided polygon and none of whose sides is a side of the polygon is", answer=112))

# 044
def _c044():
    lat = [(i, j) for i in range(4) for j in range(4)]
    return n_triangles(lat)
q("U04-B-044", TOP_G, "Triangles on a lattice", "Difficult", "Multi-step computation MCQ",
  r"The number of triangles whose vertices are among the $16$ points $(x, y)$ with $x, y \in \{0, 1, 2, 3\}$ is",
  r"$516$",
  [(r"$528$", r"Removes the $32$ collinear triples on rows and columns but none on the diagonals."),
   (r"$520$", r"Removes rows, columns and the two main diagonals ($40$) but misses the four diagonals of length $3$."),
   (r"$560$", r"Counts all ${}^{16}C_{3}$ triples.")],
  r"Total ${}^{16}C_{3} = 560$. Collinear triples: each of the $4$ rows and $4$ columns gives ${}^{4}C_{3} = 4$ (total $32$); the $2$ main diagonals give $4$ each ($8$); the $4$ diagonals with $3$ points give $1$ each ($4$). No other line contains $3$ of the points. So $560 - 44 = 516$.",
  "Missing the shorter diagonals when listing collinear triples.",
  "U04-B-lattice-triangles", "Careful enumeration of all collinear triples.",
  check=_c044, values=[516, 528, 520, 560], cognitive="Analysis",
  numerical=dict(question=r"The number of triangles whose vertices are among the $16$ points $(x, y)$ with $x, y \in \{0, 1, 2, 3\}$ is", answer=516))

# 045
def _c045():
    return ncount(r for r in rects(6, 6) if ((r[1] - r[0]) * (r[3] - r[2])) % 2 == 0)
q("U04-B-045", TOP_G, "Rectangles with a parity condition", "Difficult", "Multi-step computation MCQ",
  r"On a $6 \times 6$ board of unit squares, the number of rectangles (squares included) made of whole unit squares whose area, in square units, is even is",
  r"$297$",
  [(r"$144$", r"Counts the rectangles of odd area, $12 \times 12$."),
   (r"$378$", r"Adds rectangles with even width and those with even height, $2 \cdot 9 \cdot 21$, not subtracting those with both even."),
   (r"$441$", r"Counts all rectangles $({}^{7}C_{2})^2$.")],
  r"There are ${}^{7}C_{2} = 21$ choices of a horizontal side; of these, lengths $1, 3, 5$ occur $6 + 4 + 2 = 12$ times (odd). Odd area needs both sides odd: $12 \cdot 12 = 144$. Total rectangles $21^2 = 441$, so even area: $441 - 144 = 297$.",
  "Inclusion-exclusion slip when combining two 'even' conditions.",
  "U04-B-grid-parity", "Count side lengths by parity, then complement.",
  check=_c045, values=[297, 144, 378, 441], cognitive="Analysis",
  numerical=dict(question=r"On a $6 \times 6$ board of unit squares, the number of rectangles (squares included) made of whole unit squares whose area, in square units, is even is", answer=297))

# 046
def _c046():
    M = people('m', 6); W = people('w', 5)
    P = ('m', 0); Q = ('w', 0)
    def ok(s):
        nm = sum(1 for p in s if p[0] == 'm')
        return nm >= 2 and 5 - nm >= 2 and not (P in s and Q in s)
    return ncount(s for s in combinations(M + W, 5) if ok(s))
q("U04-B-046", TOP_S, "Committee with composition and a conflict", "Difficult", "Multi-step computation MCQ",
  r"A committee of $5$ is to be formed from $6$ men and $5$ women so that it has at least $2$ men and at least $2$ women. A particular man $P$ and a particular woman $Q$ refuse to serve together. The number of such committees is",
  r"$280$",
  [(r"$350$", r"Counts the committees with at least $2$ men and $2$ women but ignores the conflict."),
   (r"$266$", r"Subtracts ${}^{9}C_{3} = 84$, all committees containing $P$ and $Q$, ignoring the composition rule for them."),
   (r"$70$", r"Counts only the committees that contain both $P$ and $Q$.")],
  r"Without the conflict: $(2\text{ men}, 3\text{ women})$ gives ${}^{6}C_{2}\,{}^{5}C_{3} = 150$ and $(3, 2)$ gives ${}^{6}C_{3}\,{}^{5}C_{2} = 200$; total $350$. With both $P$ and $Q$: $(2,3)$ gives ${}^{5}C_{1}\,{}^{4}C_{2} = 30$ and $(3,2)$ gives ${}^{5}C_{2}\,{}^{4}C_{1} = 40$, total $70$. Answer $350 - 70 = 280$.",
  "Subtracting the forbidden pair without respecting the other constraint.",
  "U04-B-committee-conflict", "Two constraints; the subtraction must respect both.",
  check=_c046, values=[280, 350, 266, 70], cognitive="Analysis",
  numerical=dict(question=r"A committee of $5$ is to be formed from $6$ men and $5$ women so that it has at least $2$ men and at least $2$ women. A particular man $P$ and a particular woman $Q$ refuse to serve together. The number of such committees is", answer=280))

# 047
def _c047():
    return ncount(t for t in combinations(range(1, 31), 3) if sum(t) % 3 == 0)
q("U04-B-047", TOP_S, "Selections with a divisibility condition", "Difficult", "Multi-step computation MCQ",
  r"The number of ways of choosing three distinct numbers from $\{1, 2, 3, \ldots, 30\}$ such that their sum is divisible by $3$ is",
  r"$1360$",
  [(r"$1000$", r"Counts only one number from each residue class, $10^3$."),
   (r"$1120$", r"Counts one from each class and only one class with all three, $1000 + 120$."),
   (r"$360$", r"Counts only the selections with all three from the same residue class.")],
  r"Split the numbers by remainder mod $3$: three classes of $10$ each. The sum is divisible by $3$ when all three come from one class, $3 \cdot {}^{10}C_{3} = 360$, or one from each class, $10^3 = 1000$. Total $1360$.",
  r"Missing one of the residue patterns that give a multiple of $3$.",
  "U04-B-residue-selection", "Residue classification with two patterns.",
  check=_c047, values=[1360, 1000, 1120, 360], cognitive="Analysis",
  numerical=dict(question=r"The number of ways of choosing three distinct numbers from $\{1, 2, 3, \ldots, 30\}$ such that their sum is divisible by $3$ is", answer=1360))

# 048
def _c048():
    # target cell: column 3 from the left (x in [2,3]), row 5 from the top (y in [3,4] with y measured from the bottom)
    return ncount(r for r in rects(8, 8) if r[0] <= 2 and r[1] >= 3 and r[2] <= 3 and r[3] >= 4)
q("U04-B-048", TOP_G, "Rectangles containing a given square", "Difficult", "Multi-step computation MCQ",
  r"On an $8 \times 8$ chessboard, consider the unit square in the $3$rd column from the left and the $5$th row from the top. The number of rectangles (squares included) made of whole unit squares that contain this unit square is",
  r"$360$",
  [(r"$1296$", r"Counts all rectangles on the board, $({}^{9}C_{2})^2$."),
   (r"$38$", r"Adds the horizontal and vertical counts $18 + 20$ in place of multiplying."),
   (r"$120$", r"Uses one fewer line on each side in each direction: $(2 \cdot 5)(4 \cdot 3)$.")],
  r"The rectangle's left edge must be one of the $3$ vertical lines on or to the left of the square's left edge, and its right edge one of the $6$ lines on or to the right of its right edge: $3 \cdot 6 = 18$. Vertically, $5$ choices above and $4$ below: $20$. Total $18 \cdot 20 = 360$.",
  "Off-by-one in counting the available grid lines on each side.",
  "U04-B-grid-containing-cell", "Independent line choices on four sides with off-by-one trap.",
  check=_c048, values=[360, 1296, 38, 120], cognitive="Analysis",
  numerical=dict(question=r"On an $8 \times 8$ chessboard, consider the unit square in the $3$rd column from the left and the $5$th row from the top. The number of rectangles (squares included) made of whole unit squares that contain this unit square is", answer=360))

# 049
def _c049():
    ns = [m for m in range(6, 100) if 2 * C(m, 5) == C(m, 4) + C(m, 6)]
    return Integer(sum(ns))
q("U04-B-049", TOP_P, "Combinations in arithmetic progression", "Difficult", "Inverse/parameter MCQ",
  r"If ${}^{n}C_{4}$, ${}^{n}C_{5}$ and ${}^{n}C_{6}$ are in arithmetic progression, then the sum of all possible values of $n$ is",
  r"$21$",
  [(r"$14$", r"Keeps only the larger root $n = 14$."),
   (r"$7$", r"Keeps only the smaller root $n = 7$."),
   (r"$98$", r"Takes the product of the roots of $n^2 - 21n + 98 = 0$ in place of the sum.")],
  r"$2\,{}^{n}C_{5} = {}^{n}C_{4} + {}^{n}C_{6}$. Divide by ${}^{n}C_{5}$: $2 = \frac{5}{n-4} + \frac{n-5}{6}$. Multiplying by $6(n-4)$: $12(n-4) = 30 + (n-5)(n-4)$, i.e. $n^2 - 21n + 98 = 0$, so $n = 7$ or $n = 14$. Both are valid ($n \ge 6$), and the sum is $21$.",
  "Discarding a valid root or using the product of roots.",
  "U04-B-ap-combinations", "Ratio manipulation to a quadratic and checking both roots.",
  check=_c049, values=[21, 14, 7, 98], cognitive="Analysis",
  numerical=dict(question=r"If ${}^{n}C_{4}$, ${}^{n}C_{5}$ and ${}^{n}C_{6}$ are in arithmetic progression, then the sum of all possible values of $n$ is", answer=21))

# 050
def _c050():
    N = 2**4 * 3**4 * 5**2
    return ncount(d for d in divisors_of(N) if d % 4 == 1)
q("U04-B-050", TOP_D, "Divisors in a residue class", "Difficult", "Multi-step computation MCQ",
  r"The number of positive divisors of $N = 2^4 \cdot 3^4 \cdot 5^2$ that are of the form $4k + 1$, where $k$ is a non-negative integer, is",
  r"$9$",
  [(r"$15$", r"Counts all odd divisors, $5 \cdot 3$."),
   (r"$6$", r"Counts the odd divisors with an odd power of $3$, which are of the form $4k + 3$."),
   (r"$27$", r"Also allows even powers of $2$, thinking $2^2$ and $2^4$ are $1 \pmod 4$ like odd squares.")],
  r"A divisor of the form $4k + 1$ is odd, so it is $3^b 5^c$. Since $5 \equiv 1$ and $3 \equiv -1 \pmod 4$, $3^b 5^c \equiv (-1)^b$. So $b$ must be even: $b \in \{0, 2, 4\}$, and $c \in \{0, 1, 2\}$, giving $3 \cdot 3 = 9$.",
  r"Not reducing the prime factors modulo $4$.",
  "U04-B-divisor-residue", "Combines divisor counting with residues mod 4.",
  check=_c050, values=[9, 15, 6, 27], cognitive="Analysis",
  numerical=dict(question=r"The number of positive divisors of $N = 2^4 \cdot 3^4 \cdot 5^2$ that are of the form $4k + 1$, where $k$ is a non-negative integer, is", answer=9))

# 051
def _c051():
    N = 7200
    return ncount(a for a in divisors_of(N) if a <= N // a and a % 2 == 0 and (N // a) % 2 == 0)
q("U04-B-051", TOP_D, "Factorisation into even factors", "Difficult", "Multi-step computation MCQ",
  r"The number of ways of writing $7200$ as a product of two even positive integers, the order of the factors being immaterial, is",
  r"$18$",
  [(r"$36$", r"Counts ordered pairs $4 \cdot 3 \cdot 3$ without halving."),
   (r"$27$", r"Halves the total divisor count $54$, ignoring the evenness condition."),
   (r"$54$", r"Counts all divisors of $7200$.")],
  r"$7200 = 2^5 \cdot 3^2 \cdot 5^2$. If $7200 = d \cdot e$ with $d = 2^a 3^b 5^c$ and both even, then $1 \le a \le 4$, giving $4 \cdot 3 \cdot 3 = 36$ ordered pairs. As $7200$ is not a perfect square (the exponent of $2$ is odd), no pair has $d = e$, so unordered pairs number $18$.",
  "Forgetting that both factors must be even, or not halving for order.",
  "U04-B-even-factorisation", "Restrict an exponent for both factors, then handle order.",
  check=_c051, values=[18, 36, 27, 54], cognitive="Analysis",
  numerical=dict(question=r"The number of ways of writing $7200$ as a product of two even positive integers, the order of the factors being immaterial, is", answer=18))

# 052
def _c052():
    lat = [(i, j) for i in range(4) for j in range(4)]
    def d2(p, q):
        return (p[0] - q[0])**2 + (p[1] - q[1])**2
    def is_sq(s):
        ds = sorted(d2(p, q) for p, q in combinations(s, 2))
        return ds[0] > 0 and ds[0] == ds[1] == ds[2] == ds[3] and ds[4] == ds[5] == 2 * ds[0]
    return ncount(s for s in combinations(lat, 4) if is_sq(s))
q("U04-B-052", TOP_G, "Squares on a lattice in any orientation", "Difficult", "Multi-step computation MCQ",
  r"Consider the $16$ points $(x, y)$ with $x, y \in \{0, 1, 2, 3\}$. The number of squares (in any orientation) all four of whose vertices are among these points is",
  r"$20$",
  [(r"$14$", r"Counts only squares with sides parallel to the axes, $9 + 4 + 1$."),
   (r"$18$", r"Adds the $4$ tilted squares with side vector $(1, 1)$ but misses the $2$ with side vector $(1, 2)$."),
   (r"$22$", r"Counts the tilted squares in each $3 \times 3$ box twice, once for $(1, 2)$ and once for $(2, 1)$, adding $4$ in place of $2$.")],
  r"Every such square sits in an axis-parallel bounding box of side $s$, and each $s \times s$ box contains exactly $s$ inscribed squares (one axis-parallel and $s - 1$ tilted). Boxes of side $s$ number $(4 - s)^2$. Total $= 9 \cdot 1 + 4 \cdot 2 + 1 \cdot 3 = 20$.",
  "Ignoring tilted squares or double-counting their orientations.",
  "U04-B-lattice-squares", "Needs the bounding-box idea for tilted squares.",
  check=_c052, values=[20, 14, 18, 22], cognitive="Analysis",
  numerical=dict(question=r"Consider the $16$ points $(x, y)$ with $x, y \in \{0, 1, 2, 3\}$. The number of squares (in any orientation) all four of whose vertices are among these points is", answer=20))

# 053
def _c053():
    n = 12
    def step(i, j):
        d = abs(i - j) % n
        return min(d, n - d)
    return ncount(t for t in combinations(range(n), 3)
                  if len({step(t[0], t[1]), step(t[1], t[2]), step(t[0], t[2])}) < 3)
q("U04-B-053", TOP_G, "Isosceles triangles in a regular polygon", "Difficult", "Multi-step computation MCQ",
  r"The number of isosceles triangles (equilateral triangles included) whose vertices are vertices of a regular $12$-sided polygon is",
  r"$52$",
  [(r"$60$", r"Counts $12 \times 5$ (apex and equal sides) but does not correct for each equilateral triangle being counted three times."),
   (r"$56$", r"Subtracts the $4$ equilateral triangles once, though each was counted three times and should be reduced by $2$."),
   (r"$48$", r"Subtracts $3 \times 4 = 12$, removing the equilateral triangles altogether.")],
  r"Choose the apex ($12$ ways) and a pair of vertices symmetric about the axis through it: $5$ pairs. This gives $60$, but each of the $4$ equilateral triangles is counted once from each of its $3$ vertices. Correct count $= 60 - 2 \cdot 4 = 52$.",
  "Overcounting equilateral triangles in an apex-based count.",
  "U04-B-regular-polygon-isosceles", "Symmetry count plus a multiplicity correction.",
  check=_c053, values=[52, 60, 56, 48], cognitive="Analysis",
  numerical=dict(question=r"The number of isosceles triangles (equilateral triangles included) whose vertices are vertices of a regular $12$-sided polygon is", answer=52))
