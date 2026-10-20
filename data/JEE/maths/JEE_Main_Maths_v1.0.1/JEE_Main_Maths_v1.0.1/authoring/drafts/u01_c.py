import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools as it
from sympy.calculus.util import function_range

x = Symbol('x', real=True)
y = Symbol('y', real=True)
t = Symbol('t', real=True)
R = S.Reals
XII = "XII"

T, F_ = True, False
ST_OPTS = ["Both Statement I and Statement II are true",
           "Both Statement I and Statement II are false",
           "Statement I is true but Statement II is false",
           "Statement I is false but Statement II is true"]

CL = {"oi": "one-one but not onto", "on": "onto but not one-one",
      "bij": "bijective", "nei": "neither one-one nor onto"}
CLV = {"oi": (T, F_), "on": (F_, T), "bij": (T, T), "nei": (F_, F_)}


def _mono(expr, dom):
    """Strictly monotonic on dom: f' keeps one sign and vanishes only at isolated points."""
    weak = bool(is_increasing(expr, dom, x)) or bool(is_decreasing(expr, dom, x))
    zeros = solveset(diff(expr, x), x, dom)
    return weak and bool(zeros.is_finite_set)


def _classify_R(expr, codomain):
    """(one-one, onto) for a continuous expr on R."""
    return (_mono(expr, R), function_range(expr, x, R) == codomain)


def _classify_pieces(right, left, codomain):
    """f = right on [0, oo), left on (-oo, 0); both polynomial pieces."""
    r1 = function_range(right, x, Interval(0, oo))
    r2 = function_range(left, x, Interval.open(-oo, 0))
    inj = _mono(right, Interval(0, oo)) and _mono(left, Interval.open(-oo, 0)) and Intersection(r1, r2) == S.EmptySet
    return (inj, Union(r1, r2) == codomain)


def _onto_count(m, n):
    return sum(1 for f in it.product(range(n), repeat=m) if len(set(f)) == n)


# ================================================================ EASY
# ---------------------------------------------------------------- 001
def _c001():
    return sum(1 for f in it.product(range(4), repeat=3))
q("U01-C-001", "Functions", "Number of functions between finite sets", "Easy", "Single-step computation MCQ",
  r"Let $P = \{1, 2, 3\}$ and $Q = \{a, b, c, d\}$. The number of functions from $P$ to $Q$ is",
  r"$64$",
  [(r"$81$", r"Uses $n(P)^{n(Q)} = 3^4$, reversing the roles of domain and codomain."),
   (r"$12$", r"Multiplies $n(P) \cdot n(Q) = 3 \cdot 4$, which counts ordered pairs in $P \times Q$, not functions."),
   (r"$24$", r"Counts only one-one functions, ${}^4P_3 = 24$.")],
  r"Each of the $3$ elements of $P$ can be sent to any of the $4$ elements of $Q$ independently, so the number of functions is $4 \cdot 4 \cdot 4 = 4^3 = 64$.",
  r"Writing $n(P)^{n(Q)}$ instead of $n(Q)^{n(P)}$.",
  "U01-C-count-functions", "Single multiplication-principle step.",
  check=_c001, values=[64, 81, 12, 24], cognitive="Recall", source_class=XII,
  numerical=dict(question=r"Let $P = \{1, 2, 3\}$ and $Q = \{a, b, c, d\}$. The number of functions from $P$ to $Q$ is", answer=64))

# ---------------------------------------------------------------- 002
def _c002():
    return sum(1 for f in it.product(range(5), repeat=3) if len(set(f)) == 3)
q("U01-C-002", "Functions", "Counting one-one functions", "Easy", "Single-step computation MCQ",
  r"Let $P = \{1, 2, 3\}$ and $Q = \{p, q, r, s, t\}$. The number of one-one functions from $P$ to $Q$ is",
  r"$60$",
  [(r"$125$", r"Counts all functions, $5^3 = 125$, without requiring distinct images."),
   (r"$10$", r"Uses ${}^5C_3 = 10$, choosing the image set but not assigning it to $1, 2, 3$ in order."),
   (r"$243$", r"Uses $3^5$, reversing domain and codomain in the count of all functions.")],
  r"The image of $1$ can be chosen in $5$ ways, then the image of $2$ in $4$ ways and the image of $3$ in $3$ ways, since images must be distinct. So the number is ${}^5P_3 = 5 \cdot 4 \cdot 3 = 60$.",
  r"Counting the image set as a combination instead of an arrangement.",
  "U01-C-count-injections", "One permutation count.",
  check=_c002, values=[60, 125, 10, 243], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Let $P = \{1, 2, 3\}$ and $Q = \{p, q, r, s, t\}$. The number of one-one functions from $P$ to $Q$ is", answer=60))

# ---------------------------------------------------------------- 003
def _c003():
    allf = list(it.product(range(6), repeat=3))
    return sum(1 for f in allf if len(set(f)) < 6)
q("U01-C-003", "Functions", r"Onto functions impossible when $n(P) < n(Q)$", "Easy", "Conceptual/application MCQ",
  r"Let $P$ be a set with $3$ elements and $Q$ a set with $6$ elements. The number of functions from $P$ to $Q$ that are NOT onto is",
  r"$216$",
  [(r"$96$", r"Subtracts the ${}^6P_3 = 120$ one-one functions from $6^3 = 216$, treating one-one as onto."),
   (r"$210$", r"Subtracts only the $6$ constant functions from $6^3 = 216$, as if every non-constant function were onto."),
   (r"$729$", r"Uses $3^6 = 729$ for the total, reversing domain and codomain, and then correctly notes that none is onto.")],
  r"A function from a $3$-element set has at most $3$ distinct images, so it can never cover all $6$ elements of $Q$. Hence no function from $P$ to $Q$ is onto, and all $6^3 = 216$ functions are not onto.",
  r"Not noticing that onto maps need $n(P) \ge n(Q)$.",
  "U01-C-onto-impossible", "One observation about range size plus a total count.",
  check=_c003, values=[216, 96, 210, 729], cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 004
def _c004():
    return solve(Eq(3*y + 2, x), y)[0]
q("U01-C-004", "Functions", "Inverse of a linear bijection", "Easy", "Single-step computation MCQ",
  r"The function $f: \mathbb{R} \to \mathbb{R}$, $f(x) = 3x + 2$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\frac{x - 2}{3}$",
  [(r"$\frac{x + 2}{3}$", r"Sign slip: from $y = 3x + 2$ writes $x = \frac{y + 2}{3}$."),
   (r"$\frac{1}{3x + 2}$", r"Takes the reciprocal $\frac{1}{f(x)}$ as the inverse function."),
   (r"$\frac{x}{3} - 2$", r"Undoes the steps in the wrong order: divides by $3$ first and then subtracts $2$.")],
  r"Put $y = 3x + 2$; then $x = \frac{y - 2}{3}$. Interchanging the letters, $f^{-1}(x) = \frac{x - 2}{3}$. Check: $f\left(\frac{x-2}{3}\right) = (x - 2) + 2 = x$.",
  r"Confusing $f^{-1}(x)$ with $\frac{1}{f(x)}$, or undoing operations in the wrong order.",
  "U01-C-inverse-linear", "One equation solved for $x$.",
  check=_c004, values=[(x - 2)/3, (x + 2)/3, 1/(3*x + 2), x/3 - 2], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 005
def _c005():
    f = Lambda(x, x**2 + 1); g = Lambda(x, 2*x - 3)
    return g(f(2))
q("U01-C-005", "Functions", "Value of a composite function", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = x^2 + 1$ and $g(x) = 2x - 3$ for all real $x$. Then $(g \circ f)(2)$ equals",
  r"$7$",
  [(r"$2$", r"Evaluates $(f \circ g)(2) = f(1) = 2$, applying the functions in the wrong order."),
   (r"$5$", r"Multiplies $f(2) \cdot g(2) = 5 \cdot 1$, treating composition as a product."),
   (r"$6$", r"Adds $f(2) + g(2) = 5 + 1$.")],
  r"$(g \circ f)(2) = g(f(2))$. First $f(2) = 4 + 1 = 5$, then $g(5) = 10 - 3 = 7$.",
  r"Applying the outer function first in $g \circ f$.",
  "U01-C-composition-value", "Two direct evaluations in the correct order.",
  check=_c005, values=[7, 2, 5, 6], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 006
_c6 = [x**3 - 3*x**2 + 3*x, x**3 - x**2, x**2 + 2*x, x**3 - 4*x]
def _c006():
    good = [e for e in _c6 if _mono(e, R)]
    return good[0] if len(good) == 1 else None
q("U01-C-006", "Functions", "Identifying a one-one function", "Easy", "Direct concept MCQ",
  r"Which one of the following functions $f: \mathbb{R} \to \mathbb{R}$ is one-one?",
  r"$f(x) = x^3 - 3x^2 + 3x$",
  [(r"$f(x) = x^3 - x^2$", r"Assumes every cubic is one-one; but $f(0) = f(1) = 0$."),
   (r"$f(x) = x^2 + 2x$", r"Overlooks that $f(0) = f(-2) = 0$, so two inputs share an image."),
   (r"$f(x) = x^3 - 4x$", r"Assumes every cubic is one-one; but $f(0) = f(2) = f(-2) = 0$.")],
  r"$x^3 - 3x^2 + 3x = (x - 1)^3 + 1$. If $(a - 1)^3 + 1 = (b - 1)^3 + 1$ then $(a-1)^3 = (b-1)^3$, so $a = b$; hence it is one-one. Each of the other three takes the value $0$ at two different points: $x^3 - x^2$ at $0, 1$; $x^2 + 2x$ at $0, -2$; $x^3 - 4x$ at $0, \pm 2$.",
  r"Believing that every cubic polynomial is one-one on $\mathbb{R}$.",
  "U01-C-identify-one-one", "Spot a perfect cube or find two equal values; one idea.",
  check=_c006, values=_c6, cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 007
def _c007():
    n = Symbol('n', integer=True)
    a, b = symbols('a b', integer=True)
    inj = solve(Eq(2*a + 3, 2*b + 3), a) == [b]
    image = {2*k + 3 for k in range(1, 200)}
    onto = all(m in image for m in range(1, 100))
    return (inj, onto)
q("U01-C-007", "Functions", "One-one and onto on natural numbers", "Easy", "Conceptual/application MCQ",
  r"Let $\mathbb{N} = \{1, 2, 3, \ldots\}$ and let $f: \mathbb{N} \to \mathbb{N}$ be defined by $f(n) = 2n + 3$. Then $f$ is",
  CL["oi"],
  [(CL["on"], r"Interchanges the two definitions: reads the missing pre-images of $1, 2, 3, 4$ as a failure of one-one, and reads $2a + 3 = 2b + 3 \Rightarrow a = b$ as a proof of onto."),
   (CL["bij"], r"Proves one-one correctly and then assumes onto as for $f: \mathbb{R} \to \mathbb{R}$."),
   (CL["nei"], r"Sees that $f$ is not onto and wrongly concludes it cannot be one-one either, as would hold for a map from a finite set to itself.")],
  r"If $2a + 3 = 2b + 3$ then $a = b$, so $f$ is one-one. But $f(n) \ge 5$ and is always odd, so for example $1$ (or $6$) has no pre-image in $\mathbb{N}$; thus $f$ is not onto.",
  r"Carrying over the fact that $2x + 3$ is onto $\mathbb{R}$ to the codomain $\mathbb{N}$.",
  "U01-C-classify-N", "Two short checks, one for each property.",
  check=_c007, values=[CLV["oi"], CLV["on"], CLV["bij"], CLV["nei"]], cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 008
q("U01-C-008", "Functions", "Effect of the codomain on onto", "Easy", "Conceptual/application MCQ",
  r"Let $f: \mathbb{R} \to [1, \infty)$ be defined by $f(x) = x^2 + 1$. Then $f$ is",
  CL["on"],
  [(CL["bij"], r"Sees that the range equals the codomain and assumes one-one too, ignoring $f(1) = f(-1)$."),
   (CL["oi"], r"Reverses the two properties: the range is all of $[1, \infty)$ but $f(-1) = f(1)$."),
   (CL["nei"], r"Treats the codomain as $\mathbb{R}$, so concludes it is not onto.")],
  r"Since $x^2 \ge 0$, $f(x) \ge 1$, and for any $y \ge 1$ we have $f(\sqrt{y - 1}) = y$, so the range is $[1, \infty)$, which equals the codomain: $f$ is onto. But $f(1) = f(-1) = 2$, so $f$ is not one-one.",
  r"Judging onto against $\mathbb{R}$ instead of the stated codomain.",
  "U01-C-classify-codomain", "Range of a simple quadratic and one counterexample.",
  check=lambda: _classify_R(x**2 + 1, Interval(1, oo)), values=[CLV["on"], CLV["bij"], CLV["oi"], CLV["nei"]],
  cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 009
q("U01-C-009", "Functions", "Counting onto functions, small case", "Easy", "Single-step computation MCQ",
  r"The number of onto functions from $\{1, 2, 3\}$ to $\{a, b\}$ is",
  r"$6$",
  [(r"$8$", r"Counts all $2^3$ functions, not removing the two constant functions."),
   (r"$9$", r"Uses $3^2$, reversing domain and codomain."),
   (r"$7$", r"Removes only one constant function from $2^3 = 8$.")],
  r"There are $2^3 = 8$ functions in all. A function fails to be onto only if it misses $a$ or misses $b$, that is, it is one of the $2$ constant functions. So the number of onto functions is $8 - 2 = 6$.",
  r"Forgetting to remove both constant functions.",
  "U01-C-count-surjections-small", "Total minus constants; one step.",
  check=lambda: _onto_count(3, 2), values=[6, 8, 9, 7], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The number of onto functions from $\{1, 2, 3\}$ to $\{a, b\}$ is", answer=6))

# ---------------------------------------------------------------- 010
def _c010():
    u = Symbol('u', real=True)  # u = y^3
    usol = solve(Eq(u + 2, x), u)[0]
    return real_root(usol, 3)
q("U01-C-010", "Functions", "Inverse of a cubic bijection", "Easy", "Single-step computation MCQ",
  r"The function $f: \mathbb{R} \to \mathbb{R}$, $f(x) = x^3 + 2$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\sqrt[3]{x - 2}$",
  [(r"$\sqrt[3]{x} - 2$", r"Undoes the steps in the wrong order: takes the cube root first, then subtracts $2$."),
   (r"$\sqrt[3]{x + 2}$", r"Sign slip: from $y = x^3 + 2$ writes $x^3 = y + 2$."),
   (r"$\frac{1}{x^3 + 2}$", r"Takes the reciprocal $\frac{1}{f(x)}$ as the inverse.")],
  r"Put $y = x^3 + 2$, so $x^3 = y - 2$ and $x = \sqrt[3]{y - 2}$ (the real cube root, which exists for every real $y$). Hence $f^{-1}(x) = \sqrt[3]{x - 2}$; indeed $f\left(\sqrt[3]{x-2}\right) = x - 2 + 2 = x$.",
  r"Reversing the order in which the operations are undone.",
  "U01-C-inverse-power", "Solve one equation for $x$.",
  check=_c010, values=[real_root(x - 2, 3), real_root(x, 3) - 2, real_root(x + 2, 3), 1/(x**3 + 2)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 011
def _c011():
    return solveset(1 - x**2 >= 0, x, R)
q("U01-C-011", "Functions", "Domain of a composite function", "Easy", "Single-step computation MCQ",
  r"Let $f(x) = \sqrt{x}$ for $x \ge 0$ and $g(x) = 1 - x^2$ for all real $x$. The domain of $f \circ g$ is",
  r"$[-1, 1]$",
  [(r"$[0, 1]$", r"Also imposes $x \ge 0$ (the domain of $f$) on $x$ itself, instead of on $g(x)$."),
   (r"$(-1, 1)$", r"Uses the strict inequality $1 - x^2 > 0$, dropping the points where $\sqrt{0} = 0$ is defined."),
   (r"$(-\infty, -1] \cup [1, \infty)$", r"Reverses the inequality, solving $1 - x^2 \le 0$.")],
  r"$(f \circ g)(x) = \sqrt{1 - x^2}$ is defined when $g(x) = 1 - x^2 \ge 0$, that is, $x^2 \le 1$, i.e. $-1 \le x \le 1$. Since $g$ is defined for all real $x$, the domain is $[-1, 1]$.",
  r"Applying the domain of the outer function to $x$ instead of to $g(x)$.",
  "U01-C-composite-domain", "One inequality on the inner function.",
  check=_c011, values=[Interval(-1, 1), Interval(0, 1), Interval.open(-1, 1), Union(Interval(-oo, -1), Interval(1, oo))],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 012
def _c012():
    g = Symbol('g')
    return solve(Eq(2*g + 3, 6*x - 1), g)[0]
q("U01-C-012", "Functions", "Finding the inner function", "Easy", "Inverse/parameter MCQ",
  r"Let $f(x) = 2x + 3$ and let $g: \mathbb{R} \to \mathbb{R}$ be such that $(f \circ g)(x) = 6x - 1$ for all real $x$. Then $g(x)$ equals",
  r"$3x - 2$",
  [(r"$3x + 1$", r"Sign slip: writes $2g(x) = 6x - 1 + 3$."),
   (r"$12x + 1$", r"Computes $f(6x - 1) = 12x + 1$, composing in the wrong direction."),
   (r"$3x - \frac{1}{2}$", r"Halves $6x - 1$ without first subtracting $3$.")],
  r"$(f \circ g)(x) = f(g(x)) = 2g(x) + 3 = 6x - 1$, so $2g(x) = 6x - 4$ and $g(x) = 3x - 2$. Check: $f(3x - 2) = 6x - 4 + 3 = 6x - 1$.",
  r"Reading $f \circ g$ as $g \circ f$, or mishandling the constant.",
  "U01-C-find-inner-function", "One linear equation in $g(x)$.",
  check=_c012, values=[3*x - 2, 3*x + 1, 12*x + 1, 3*x - Rational(1, 2)], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 013
def _c013():
    return sum(1 for p in it.permutations(range(1, 6)) if p[0] == 1)
q("U01-C-013", "Functions", "Counting bijections with a fixed value", "Easy", "Single-step computation MCQ",
  r"Let $P = \{1, 2, 3, 4, 5\}$. The number of bijections $f: P \to P$ with $f(1) = 1$ is",
  r"$24$",
  [(r"$120$", r"Counts all $5!$ bijections, ignoring the condition $f(1) = 1$."),
   (r"$625$", r"Counts all functions with $f(1) = 1$, i.e. $5^4$, not requiring bijectivity."),
   (r"$256$", r"Maps the remaining $4$ elements into the remaining $4$ values freely, $4^4$, not requiring distinct images.")],
  r"With $f(1) = 1$ fixed, $f$ must map $\{2, 3, 4, 5\}$ bijectively onto $\{2, 3, 4, 5\}$, since $1$ is already used. The number of such bijections is $4! = 24$.",
  r"Counting functions instead of bijections, or ignoring the given condition.",
  "U01-C-count-bijections-fixed", "One factorial after fixing one image.",
  check=_c013, values=[24, 120, 625, 256], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 014
def _c014():
    s1 = function_range(x**3, x, R) == R
    s2 = _mono(x**2, Interval(0, oo))
    return (s1, s2)
q("U01-C-014", "Functions", "One-one and onto: statements", "Easy", "Statement-based MCQ",
  r"Statement I: The function $f: \mathbb{R} \to \mathbb{R}$, $f(x) = x^3$, is onto. Statement II: The function $g: [0, \infty) \to [0, \infty)$, $g(x) = x^2$, is one-one. In the light of the above statements, choose the correct answer.",
  ST_OPTS[0],
  [(ST_OPTS[1], r"Rejects both, using the facts that $x^2$ is not one-one on $\mathbb{R}$ and wrongly that $x^3$ misses negative values."),
   (ST_OPTS[2], r"Uses $g(1) = g(-1)$ to reject Statement II, ignoring that $-1$ is not in the domain $[0, \infty)$."),
   (ST_OPTS[3], r"Thinks $x^3$ cannot reach every real number, while accepting Statement II.")],
  r"For any real $y$, $x = \sqrt[3]{y}$ is real and $x^3 = y$, so $f$ is onto. For $a, b \ge 0$, $a^2 = b^2$ gives $(a - b)(a + b) = 0$; if $a + b = 0$ then $a = b = 0$, so in all cases $a = b$ and $g$ is one-one. Both statements are true.",
  r"Testing one-one with points outside the given domain.",
  "U01-C-statement-restricted-domain", "Two quick checks with a domain trap.",
  check=_c014, values=[(T, T), (F_, F_), (T, F_), (F_, T)], cognitive="Understanding", source_class=XII)

# ================================================================ MEDIUM
# ---------------------------------------------------------------- 015
def _c015():
    sols = [(m, n) for m in range(1, 10) for n in range(1, 300)
            if n**m == 256 and (factorial(n)/factorial(n - m) if n >= m else 0) == 240]
    return sols[0] if len(sols) == 1 else None
q("U01-C-015", "Functions", "Recovering set sizes from counts", "Medium", "Inverse/parameter MCQ",
  r"For finite non-empty sets $P$ and $Q$, the number of functions from $P$ to $Q$ is $256$ and the number of one-one functions from $P$ to $Q$ is $240$. Then $(n(P), n(Q))$ equals",
  r"$(2, 16)$",
  [(r"$(16, 2)$", r"Writes the counts as $n(P)^{n(Q)}$ and ${}^{n(P)}P_{n(Q)}$, swapping domain and codomain; then $16^2 = 256$ and ${}^{16}P_2 = 240$."),
   (r"$(4, 4)$", r"Uses only $4^4 = 256$, ignoring the one-one count (${}^4P_4 = 24$)."),
   (r"$(8, 2)$", r"Uses only $2^8 = 256$, ignoring that no one-one map from $8$ elements into $2$ exists.")],
  r"Let $n(P) = m$, $n(Q) = n$. Then $n^m = 256$ and ${}^nP_m = 240$. From $n^m = 256$: $(m, n) \in \{(1, 256), (2, 16), (4, 4), (8, 2)\}$, with ${}^nP_m$ equal to $256, 240, 24, 0$ respectively. Only $(2, 16)$ gives $240$.",
  r"Swapping the roles of domain and codomain in $n(Q)^{n(P)}$.",
  "U01-C-count-reverse", "Factorising $256$ as a power and testing each case against a second count.",
  check=_c015, values=[(2, 16), (16, 2), (4, 4), (8, 2)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 016
q("U01-C-016", "Functions", "Counting onto functions by inclusion-exclusion", "Medium", "Multi-step computation MCQ",
  r"The number of onto functions from $\{1, 2, 3, 4\}$ to $\{a, b, c\}$ is",
  r"$36$",
  [(r"$81$", r"Counts all $3^4$ functions."),
   (r"$72$", r"Maps $3$ chosen elements bijectively (${}^4P_3 = 24$ ways) and the fourth anywhere ($3$ ways), double counting each map."),
   (r"$24$", r"Counts ${}^4P_3$, as if the map were one-one from a $3$-element set.")],
  r"Total functions $= 3^4 = 81$. Functions missing a given element: $2^4 = 16$, three choices; missing two given elements: $1$, three choices. By inclusion-exclusion, onto functions $= 81 - 3 \cdot 16 + 3 \cdot 1 = 36$. Equivalently, choose the pair sharing an image, ${}^4C_2 = 6$, then assign three blocks to three letters, $3! = 6$: $36$.",
  r"Double counting by fixing a bijection first and then placing the extra element.",
  "U01-C-count-surjections-ie", "Inclusion-exclusion over three missing images.",
  check=lambda: _onto_count(4, 3), values=[36, 81, 72, 24], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The number of onto functions from $\{1, 2, 3, 4\}$ to $\{a, b, c\}$ is", answer=36))

# ---------------------------------------------------------------- 017
def _c017():
    return sum(1 for f in it.product(range(1, 4), repeat=5) if 1 in f and 2 in f)
q("U01-C-017", "Functions", "Functions whose range contains given elements", "Medium", "Multi-step computation MCQ",
  r"The number of functions $f: \{1, 2, 3, 4, 5\} \to \{1, 2, 3\}$ whose range contains both $1$ and $2$ is",
  r"$180$",
  [(r"$150$", r"Counts onto functions, also forcing $3$ into the range."),
   (r"$179$", r"Subtracts $2^5 + 2^5 = 64$ from $243$ but forgets to add back the $1$ function missing both."),
   (r"$211$", r"Subtracts only the $2^5 = 32$ functions missing $1$.")],
  r"Total $= 3^5 = 243$. Functions missing $1$: $2^5 = 32$; missing $2$: $32$; missing both (constant $3$): $1$. So the count is $243 - 32 - 32 + 1 = 180$.",
  r"Dropping the add-back term in inclusion-exclusion.",
  "U01-C-range-contains", "Two-set inclusion-exclusion on functions.",
  check=_c017, values=[180, 150, 179, 211], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The number of functions $f: \{1, 2, 3, 4, 5\} \to \{1, 2, 3\}$ whose range contains both $1$ and $2$ is", answer=180))

# ---------------------------------------------------------------- 018
def _c018():
    return sum(1 for f in it.product(range(4), repeat=4) if len(set(f)) < 4)
q("U01-C-018", "Functions", "Counting functions that are not one-one", "Medium", "Multi-step computation MCQ",
  r"Let $P = \{1, 2, 3, 4\}$. The number of functions $f: P \to P$ that are NOT one-one is",
  r"$232$",
  [(r"$252$", r"Subtracts only the $4$ constant functions from $4^4 = 256$."),
   (r"$24$", r"Counts the one-one functions $4! = 24$ instead of the rest."),
   (r"$255$", r"Thinks the identity is the only one-one map from $P$ to itself and subtracts $1$.")],
  r"There are $4^4 = 256$ functions from $P$ to $P$. A function from a finite set to itself is one-one exactly when it is a bijection, and there are $4! = 24$ of these. Hence $256 - 24 = 232$ functions are not one-one.",
  r"Equating not one-one with constant.",
  "U01-C-count-not-injective", "Total minus injections; two counts.",
  check=_c018, values=[232, 252, 24, 255], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Let $P = \{1, 2, 3, 4\}$. The number of functions $f: P \to P$ that are not one-one is", answer=232))

# ---------------------------------------------------------------- 019
def _c019():
    return sum(1 for f in it.product(range(1, 7), repeat=3) if f[0] < f[1] < f[2])
q("U01-C-019", "Functions", "Strictly increasing functions", "Medium", "Multi-step computation MCQ",
  r"The number of functions $f: \{1, 2, 3\} \to \{1, 2, 3, 4, 5, 6\}$ such that $f(1) < f(2) < f(3)$ is",
  r"$20$",
  [(r"$120$", r"Counts all one-one functions ${}^6P_3$, not using the order condition."),
   (r"$216$", r"Counts all functions $6^3$."),
   (r"$56$", r"Uses ${}^8C_3$, the count for $f(1) \le f(2) \le f(3)$.")],
  r"Such a function is one-one, and each $3$-element subset of $\{1, \ldots, 6\}$ gives exactly one increasing assignment (smallest to $1$, next to $2$, largest to $3$). So the count is ${}^6C_3 = 20$.",
  r"Counting arrangements instead of selections when order is forced.",
  "U01-C-count-increasing", "Recognise a selection problem.",
  check=_c019, values=[20, 120, 216, 56], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The number of functions $f: \{1, 2, 3\} \to \{1, 2, 3, 4, 5, 6\}$ such that $f(1) < f(2) < f(3)$ is", answer=20))

# ---------------------------------------------------------------- 020
q("U01-C-020", "Functions", "Classifying a modulus-based function", "Medium", "Conceptual/application MCQ",
  r"Let $f: \mathbb{R} \to \mathbb{R}$ be defined by $f(x) = x|x|$. Then $f$ is",
  CL["bij"],
  [(CL["on"], r"Thinks $|x|$ makes $f$ even, so that $f(-a) = f(a)$; actually $f(-a) = -f(a)$."),
   (CL["oi"], r"Thinks the range is $[0, \infty)$, as for $|x|$ or $x^2$."),
   (CL["nei"], r"Applies both wrong ideas: $f$ treated as even and non-negative.")],
  r"$f(x) = x^2$ for $x \ge 0$ and $f(x) = -x^2$ for $x < 0$. On $[0, \infty)$ it increases and takes all values in $[0, \infty)$; on $(-\infty, 0)$ it increases and takes all values in $(-\infty, 0)$. These ranges are disjoint and together give $\mathbb{R}$, so $f$ is one-one and onto, i.e. bijective.",
  r"Treating $x|x|$ like the even function $x^2$.",
  "U01-C-classify-R", "Split into two cases and combine ranges.",
  check=lambda: _classify_pieces(x**2, -x**2, R), values=[CLV["bij"], CLV["on"], CLV["oi"], CLV["nei"]],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 021
q("U01-C-021", "Functions", "Classifying a cubic", "Medium", "Conceptual/application MCQ",
  r"Let $f: \mathbb{R} \to \mathbb{R}$ be defined by $f(x) = x^3 - 3x$. Then $f$ is",
  CL["on"],
  [(CL["bij"], r"Assumes every cubic is a bijection; but $f(0) = f(\sqrt{3}) = 0$."),
   (CL["oi"], r"Tests one-one only on $x \ge 1$, where $f$ is increasing, and reads the turning-point values $f(-1) = 2$, $f(1) = -2$ as bounding the range to $[-2, 2]$, so rejects onto."),
   (CL["nei"], r"Finds the repeated value correctly but thinks a cubic with turning points cannot take all real values.")],
  r"$f(0) = 0$ and $f(\sqrt{3}) = 3\sqrt{3} - 3\sqrt{3} = 0$, so $f$ is not one-one. For any real $c$, the cubic equation $x^3 - 3x - c = 0$ has real coefficients, so its non-real roots occur in conjugate pairs; with three roots in all, at least one root is real. That real root is a pre-image of $c$, so $f$ is onto.",
  r"Believing every cubic is one-one, or that turning points reduce the range.",
  "U01-C-classify-R", "Find a repeated value and argue the range of an odd-degree polynomial.",
  check=lambda: _classify_R(x**3 - 3*x, R), values=[CLV["on"], CLV["bij"], CLV["oi"], CLV["nei"]],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 022
q("U01-C-022", "Functions", "Classifying a rational function", "Medium", "Conceptual/application MCQ",
  r"Let $f: \mathbb{R} \to \mathbb{R}$ be defined by $f(x) = \frac{2x}{1 + x^2}$. Then $f$ is",
  CL["nei"],
  [(CL["oi"], r"Notes $f$ is odd and assumes odd functions are one-one, while seeing $f$ is bounded."),
   (CL["on"], r"Spots $f(2) = f(\frac{1}{2})$ but assumes a rational function takes all real values."),
   (CL["bij"], r"Treats $f$ like the linear function $2x$ for both properties.")],
  r"$f(2) = \frac{4}{5} = f\left(\frac{1}{2}\right)$, so $f$ is not one-one. Also $1 + x^2 - 2|x| = (1 - |x|)^2 \ge 0$ gives $|f(x)| \le 1$, so for example $2$ has no pre-image; $f$ is not onto. (Its range is $[-1, 1]$.)",
  r"Assuming odd functions are one-one, or that rational functions are onto $\mathbb{R}$.",
  "U01-C-classify-R", "Find two inputs with equal value and bound the range.",
  check=lambda: _classify_R(2*x/(1 + x**2), R), values=[CLV["nei"], CLV["oi"], CLV["on"], CLV["bij"]],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 023
def _c023():
    return simplify(solve(Eq((y - 1)/(y - 2), x), y)[0])
q("U01-C-023", "Functions", "Inverse of a rational bijection", "Medium", "Multi-step computation MCQ",
  r"The function $f: \mathbb{R} - \{2\} \to \mathbb{R} - \{1\}$, $f(x) = \frac{x - 1}{x - 2}$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\frac{2x - 1}{x - 1}$",
  [(r"$\frac{x - 2}{x - 1}$", r"Takes the reciprocal $\frac{1}{f(x)}$ as the inverse."),
   (r"$\frac{2x + 1}{x - 1}$", r"Sign slip moving terms: writes $x(y - 1) = 2y + 1$ from $xy - 2y = x - 1$."),
   (r"$\frac{x - 1}{2x - 1}$", r"Solves correctly but then inverts the resulting fraction.")],
  r"Let $y = \frac{x - 1}{x - 2}$. Then $xy - 2y = x - 1$, so $x(y - 1) = 2y - 1$ and $x = \frac{2y - 1}{y - 1}$, valid since $y \ne 1$. Hence $f^{-1}(x) = \frac{2x - 1}{x - 1}$, with domain $\mathbb{R} - \{1\}$ as expected.",
  r"Confusing $f^{-1}$ with $\frac{1}{f}$, or sign errors in collecting terms.",
  "U01-C-inverse-mobius", "Cross-multiply, collect terms and solve: three steps.",
  check=_c023, values=[(2*x - 1)/(x - 1), (x - 2)/(x - 1), (2*x + 1)/(x - 1), (x - 1)/(2*x - 1)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 024
def _c024():
    k = Symbol('k')
    f = (3*x + 2)/(5*x + k)
    inv = solve(Eq((3*y + 2)/(5*y + k), x), y)[0]
    sols = solve(Poly(numer(together(inv - f)), x).coeffs(), k, dict=True)
    return sols[0][k] if len(sols) == 1 else None
q("U01-C-024", "Functions", "Self-inverse function", "Medium", "Inverse/parameter MCQ",
  r"For a real constant $k$, let $f(x) = \frac{3x + 2}{5x + k}$, where $3k - 10 \ne 0$ and $x \ne -\frac{k}{5}$, so that $f$ is a bijection onto its range. If $f^{-1}(x) = f(x)$ for all $x$ in the range of $f$, then $k$ equals",
  r"$-3$",
  [(r"$3$", r"Uses the condition $d = a$ instead of $a + d = 0$ for a self-inverse function."),
   (r"$-2$", r"Uses $b + d = 0$, pairing the wrong coefficients."),
   (r"$2$", r"Uses $d = b$.")],
  r"Solving $x = \frac{3y + 2}{5y + k}$ gives $y(5x - 3) = 2 - kx$, so $f^{-1}(x) = \frac{-kx + 2}{5x - 3}$. For this to equal $\frac{3x + 2}{5x + k}$ identically we need $-k = 3$ (then the denominators $5x - 3$ and $5x + k$ also agree). So $k = -3$.",
  r"Misremembering the condition $a + d = 0$ for $\frac{ax + b}{cx + d}$ to be its own inverse.",
  "U01-C-inverse-mobius", "Find the inverse and compare coefficients.",
  check=_c024, values=[-3, 3, -2, 2], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 025
def _c025():
    sols = solve(Eq(y**2 - 2*y + 3, x), y)
    good = [s for s in sols if s.subs(x, 3) >= 1]
    return good[0] if len(good) == 1 else None
q("U01-C-025", "Functions", "Inverse of a restricted quadratic", "Medium", "Multi-step computation MCQ",
  r"The function $f: [1, \infty) \to [2, \infty)$, $f(x) = x^2 - 2x + 3$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$1 + \sqrt{x - 2}$",
  [(r"$1 - \sqrt{x - 2}$", r"Takes the negative square root, which gives values $\le 1$, outside the domain $[1, \infty)$."),
   (r"$\sqrt{x - 2} - 1$", r"Completes the square as $(x + 1)^2 + 2$, a sign slip in the vertex."),
   (r"$1 + \sqrt{x - 3}$", r"Completes the square as $(x - 1)^2 + 3$, forgetting to subtract the $1$ added.")],
  r"$f(x) = (x - 1)^2 + 2$. Put $y = (x - 1)^2 + 2$; then $(x - 1)^2 = y - 2$, and since $x \ge 1$, $x - 1 = \sqrt{y - 2}$. Hence $f^{-1}(x) = 1 + \sqrt{x - 2}$ for $x \ge 2$.",
  r"Choosing the wrong square-root branch for the restricted domain.",
  "U01-C-inverse-quadratic-restricted", "Complete the square, solve, and select the branch.",
  check=_c025, values=[1 + sqrt(x - 2), 1 - sqrt(x - 2), sqrt(x - 2) - 1, 1 + sqrt(x - 3)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 026
def _c026():
    inner = solveset(sqrt(4 - x) - 1 >= 0, x, R)
    return Intersection(inner, Interval(-oo, 4))
q("U01-C-026", "Functions", "Domain of a composite of square roots", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \sqrt{x - 1}$ and $g(x) = \sqrt{4 - x}$, each defined where the square root is real. The domain of $f \circ g$ is",
  r"$(-\infty, 3]$",
  [(r"$(-\infty, 4]$", r"Uses only the domain of $g$, ignoring the condition $g(x) \ge 1$ needed for $f$."),
   (r"$[1, 4]$", r"Intersects the domains of $f$ and $g$ instead of requiring $g(x)$ to lie in the domain of $f$."),
   (r"$[3, 4]$", r"Reverses the inequality: solves $\sqrt{4 - x} \le 1$.")],
  r"$(f \circ g)(x) = \sqrt{\sqrt{4 - x} - 1}$ needs $4 - x \ge 0$ and $\sqrt{4 - x} \ge 1$, i.e. $4 - x \ge 1$, so $x \le 3$. The domain is $(-\infty, 3]$.",
  r"Intersecting the two domains instead of using $g(x) \in \operatorname{dom} f$.",
  "U01-C-composite-domain", "Two conditions, one nested.",
  check=_c026, values=[Interval(-oo, 3), Interval(-oo, 4), Interval(1, 4), Interval(3, 4)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 027
def _c027():
    g = (x + 1)/(x - 1)
    bad = Union(FiniteSet(1), solveset(Eq(g, 2), x, R))
    return Complement(R, bad)
q("U01-C-027", "Functions", "Domain of a composite of rational functions", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \frac{1}{x - 2}$ for $x \ne 2$ and $g(x) = \frac{x + 1}{x - 1}$ for $x \ne 1$. The domain of $f \circ g$ is",
  r"$\mathbb{R} - \{1, 3\}$",
  [(r"$\mathbb{R} - \{1\}$", r"Imposes only the restriction $x \ne 1$ from $g$, forgetting that $f$ needs $g(x) \ne 2$."),
   (r"$\mathbb{R} - \{1, 2\}$", r"Excludes $x = 2$ (the domain restriction of $f$) for $x$ itself, instead of $g(x) = 2$."),
   (r"$\mathbb{R} - \{2, 3\}$", r"Excludes $x = 2$ and the point where $g(x) = 2$ but forgets that $g$ itself needs $x \ne 1$.")],
  r"We need $x \ne 1$ for $g$, and $g(x) \ne 2$ for $f$. Now $\frac{x + 1}{x - 1} = 2$ gives $x + 1 = 2x - 2$, i.e. $x = 3$. So the domain is $\mathbb{R} - \{1, 3\}$. (The simplified form $\frac{x - 1}{3 - x}$ hides the restriction $x \ne 1$.)",
  r"Reading the domain off the simplified formula, or excluding the wrong point.",
  "U01-C-composite-domain", "Two exclusions, one found by solving an equation; simplification trap.",
  check=_c027, values=[Complement(R, FiniteSet(1, 3)), Complement(R, FiniteSet(1)), Complement(R, FiniteSet(1, 2)), Complement(R, FiniteSet(2, 3))],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 028
def _c028():
    f = Lambda(x, 2*x + 3); g = Lambda(x, x**2 - 1)
    p = Poly(f(g(x)) - g(f(x)), x)
    r = solve(p.as_expr(), x)
    return simplify(r[0]*r[1])
q("U01-C-028", "Functions", "Equation involving fog and gof", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = 2x + 3$ and $g(x) = x^2 - 1$ for all real $x$. The product of the real values of $x$ satisfying $(f \circ g)(x) = (g \circ f)(x)$ is",
  r"$\frac{7}{2}$",
  [(r"$4$", r"Writes $(g \circ f)(x) = (2x + 3)^2$, dropping the $-1$, which gives $2x^2 + 12x + 8 = 0$."),
   (r"$-\frac{7}{2}$", r"Sign slip in the product of roots, using $-\frac{c}{a}$."),
   (r"$7$", r"Forgets to divide by the leading coefficient $2$.")],
  r"$(f \circ g)(x) = 2(x^2 - 1) + 3 = 2x^2 + 1$ and $(g \circ f)(x) = (2x + 3)^2 - 1 = 4x^2 + 12x + 8$. Equating, $2x^2 + 12x + 7 = 0$, whose discriminant $144 - 56 = 88 > 0$, so both roots are real, with product $\frac{7}{2}$.",
  r"Mis-expanding the composite or misusing the product-of-roots formula.",
  "U01-C-compose-equation", "Two composites, a quadratic and Vieta.",
  check=_c028, values=[Rational(7, 2), 4, -Rational(7, 2), 7], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 029
q("U01-C-029", "Functions", "One-one and onto properties of composites", "Medium", "Statement-based MCQ",
  r"Let $f: P \to Q$ and $g: Q \to S$ be functions, where $P, Q, S$ are non-empty sets. Statement I: If $g \circ f$ is one-one, then $g$ must be one-one. Statement II: If $g \circ f$ is onto, then $g$ must be onto. In the light of the above statements, choose the correct answer.",
  ST_OPTS[3],
  [(ST_OPTS[0], r"Assumes both properties pass to $g$; one-one actually passes to the inner function $f$."),
   (ST_OPTS[1], r"Assumes neither property passes to either function."),
   (ST_OPTS[2], r"Swaps the roles: thinks one-one passes to the outer function and onto to the inner one.")],
  r"Statement I is false: take $P = \{1\}$, $Q = \{1, 2\}$, $S = \{1\}$, $f(1) = 1$, $g(1) = g(2) = 1$; then $g \circ f$ is one-one but $g$ is not. Statement II is true: for any $s \in S$ there is $p \in P$ with $g(f(p)) = s$, so $f(p) \in Q$ is a pre-image of $s$ under $g$.",
  r"Mixing up which of $f$, $g$ inherits one-one and which inherits onto from $g \circ f$.",
  "U01-C-composition-properties", "Requires a counterexample and a short proof.",
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 030
def _c030():
    return sum(1 for f in it.permutations(range(1, 7), 4) if f[0] % 2 == 0)
q("U01-C-030", "Functions", "One-one functions with a condition", "Medium", "Multi-step computation MCQ",
  r"The number of one-one functions $f: \{1, 2, 3, 4\} \to \{1, 2, 3, 4, 5, 6\}$ such that $f(1)$ is even is",
  r"$180$",
  [(r"$360$", r"Counts all ${}^6P_4 = 360$ one-one functions, ignoring the condition on $f(1)$."),
   (r"$375$", r"Takes $3$ choices for $f(1)$ and then $5^3$, allowing repeated images among $f(2), f(3), f(4)$."),
   (r"$30$", r"Takes $3 \cdot {}^5C_3$, choosing the remaining images without arranging them.")],
  r"$f(1)$ can be $2, 4$ or $6$: $3$ ways. The remaining $3$ elements must go one-one into the remaining $5$ values: ${}^5P_3 = 60$ ways. Total $3 \cdot 60 = 180$.",
  r"Dropping distinctness after fixing the restricted image.",
  "U01-C-count-injections-constraint", "Fix the constrained image, then a permutation count.",
  check=_c030, values=[180, 360, 375, 30], cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 031
def _c031():
    return sum(1 for f in it.product(range(3), repeat=4) if len(set(f)) == 2)
q("U01-C-031", "Functions", "Functions with range of given size", "Medium", "Multi-step computation MCQ",
  r"The number of functions $f: \{1, 2, 3, 4\} \to \{a, b, c\}$ whose range has exactly two elements is",
  r"$42$",
  [(r"$48$", r"Chooses the two values (${}^3C_2 = 3$) and counts all $2^4 = 16$ maps into them, not removing the constant maps."),
   (r"$36$", r"Counts the onto functions, i.e. range of size three."),
   (r"$14$", r"Counts maps onto one fixed pair, $2^4 - 2$, forgetting to choose the pair.")],
  r"Choose the two values in the range: ${}^3C_2 = 3$ ways. The number of functions from a $4$-element set onto a given $2$-element set is $2^4 - 2 = 14$. Total $3 \cdot 14 = 42$. (Check: $3 + 42 + 36 = 81 = 3^4$.)",
  r"Not excluding the constant maps when counting maps onto a chosen pair.",
  "U01-C-range-exact-size", "Choose the range, then count onto maps.",
  check=_c031, values=[42, 48, 36, 14], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The number of functions $f: \{1, 2, 3, 4\} \to \{a, b, c\}$ whose range has exactly two elements is", answer=42))

# ---------------------------------------------------------------- 032
def _c032():
    def f(n):
        return n + 1 if n % 2 == 1 else n - 1
    N = 1000
    imgs = [f(n) for n in range(1, N + 1)]
    inj = len(set(imgs)) == len(imgs)
    onto = set(range(1, N)) <= set(imgs)
    return (inj, onto)
q("U01-C-032", "Functions", "A piecewise map on natural numbers", "Medium", "Conceptual/application MCQ",
  r"Let $\mathbb{N} = \{1, 2, 3, \ldots\}$ and let $f: \mathbb{N} \to \mathbb{N}$ be defined by $f(n) = n + 1$ if $n$ is odd and $f(n) = n - 1$ if $n$ is even. Then $f$ is",
  CL["bij"],
  [(CL["oi"], r"Thinks $1$ has no pre-image as with $n + 1$ alone; but $f(2) = 1$."),
   (CL["on"], r"Thinks two different inputs collide, e.g. confusing $f(1) = 2$ with $f(2) = 1$."),
   (CL["nei"], r"Thinks two inputs collide (confusing $f(1) = 2$ with $f(2) = 1$) and also that $1$ has no pre-image, as for $n + 1$ alone, so rejects both properties.")],
  r"$f$ swaps $1 \leftrightarrow 2$, $3 \leftrightarrow 4$, and so on. Odd inputs go to even outputs and even inputs to odd outputs, each branch is one-one, so $f$ is one-one. Every even $m$ equals $f(m - 1)$ and every odd $m$ equals $f(m + 1)$, so $f$ is onto. Indeed $f(f(n)) = n$. Hence $f$ is bijective.",
  r"Judging a piecewise map by one branch only.",
  "U01-C-classify-N", "Casework on parity for both properties.",
  check=_c032, values=[CLV["bij"], CLV["oi"], CLV["on"], CLV["nei"]], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 033
def _c033():
    s_ = Symbol('s', real=True)
    back = solve(Eq(2*s_ - 1, t), s_)[0]          # x in terms of t = 2x - 1
    return expand((4*x**2 - 2*x + 3).subs(x, back).subs(t, x))
q("U01-C-033", "Functions", "Finding a function from a composite", "Medium", "Multi-step computation MCQ",
  r"Let $f: \mathbb{R} \to \mathbb{R}$ satisfy $f(2x - 1) = 4x^2 - 2x + 3$ for all real $x$. Then $f(x)$ equals",
  r"$x^2 + x + 3$",
  [(r"$16x^2 - 20x + 9$", r"Substitutes $2x - 1$ into the right side instead of solving $t = 2x - 1$ for $x$."),
   (r"$x^2 - 3x + 5$", r"Sign slip: uses $x = \frac{t - 1}{2}$ instead of $\frac{t + 1}{2}$."),
   (r"$4x^2 + 6x + 5$", r"Uses $x = t + 1$, forgetting to divide by $2$.")],
  r"Put $t = 2x - 1$, so $x = \frac{t + 1}{2}$. Then $f(t) = 4 \cdot \frac{(t + 1)^2}{4} - (t + 1) + 3 = t^2 + 2t + 1 - t - 1 + 3 = t^2 + t + 3$. Hence $f(x) = x^2 + x + 3$.",
  r"Substituting in the wrong direction.",
  "U01-C-find-outer-function", "Change of variable and expansion.",
  check=_c033, values=[x**2 + x + 3, 16*x**2 - 20*x + 9, x**2 - 3*x + 5, 4*x**2 + 6*x + 5],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 034
q("U01-C-034", "Functions", "Counting into functions", "Medium", "Multi-step computation MCQ",
  r"The number of into functions (functions that are not onto) from $\{1, 2, 3, 4, 5\}$ to $\{a, b, c\}$ is",
  r"$93$",
  [(r"$150$", r"Gives the number of onto functions instead."),
   (r"$96$", r"Counts $3 \cdot 2^5$ maps missing at least one element without subtracting the $3$ constant maps counted twice."),
   (r"$3$", r"Counts only the constant functions as into.")],
  r"Total $= 3^5 = 243$. Onto functions $= 243 - 3 \cdot 2^5 + 3 \cdot 1 = 150$. So into functions $= 243 - 150 = 93$. (Directly: $3 \cdot 32 - 3 = 93$.)",
  r"Forgetting the overlap correction when counting maps that miss an element.",
  "U01-C-count-into", "Inclusion-exclusion and complement.",
  check=lambda: 3**5 - _onto_count(5, 3), values=[93, 150, 96, 3], cognitive="Application", source_class=XII,
  numerical=dict(question=r"The number of into functions (functions that are not onto) from $\{1, 2, 3, 4, 5\}$ to $\{a, b, c\}$ is", answer=93))

# ---------------------------------------------------------------- 035
def _c035():
    f = x**2 - 4*x + 7
    a = solve(diff(f, x), x)[0]
    b = function_range(f, x, Interval(a, oo)).inf
    return a + b
q("U01-C-035", "Functions", "Restricting a quadratic to make it bijective", "Medium", "Inverse/parameter MCQ",
  r"Let $f(x) = x^2 - 4x + 7$. Let $a$ be the least real number such that $f$ is one-one on $[a, \infty)$, and let $b$ be such that $f: [a, \infty) \to [b, \infty)$ is onto. Then $a + b$ equals",
  r"$5$",
  [(r"$17$", r"Sign slip in the vertex: takes $a = -2$, so $b = f(-2) = 19$."),
   (r"$9$", r"Takes $a = 2$ correctly but $b = f(0) = 7$."),
   (r"$11$", r"Uses $-\frac{b}{a} = 4$ for the vertex, so $a = 4$ and $b = f(4) = 7$.")],
  r"$f(x) = (x - 2)^2 + 3$. It decreases on $(-\infty, 2]$ and increases on $[2, \infty)$, so the least $a$ with $f$ one-one on $[a, \infty)$ is $a = 2$, and then the range is $[3, \infty)$, so $b = 3$. Thus $a + b = 5$.",
  r"Misplacing the vertex of the parabola.",
  "U01-C-restrict-to-bijection", "Completing the square, then reading off both parameters.",
  check=_c035, values=[5, 17, 9, 11], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Let $f(x) = x^2 - 4x + 7$. Let $a$ be the least real number such that $f$ is one-one on $[a, \infty)$, and let $b$ be such that $f: [a, \infty) \to [b, \infty)$ is onto. Then $a + b$ is", answer=5))

# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 036
def _c036():
    v = Integer(3)
    for _ in range(2026):
        v = 1/(1 - v)
    return v
q("U01-C-036", "Functions", "Repeated composition with period three", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = \frac{1}{1 - x}$ for real $x \ne 0, 1$, and let $f^{[n]}$ denote $f$ composed with itself $n$ times, so $f^{[1]} = f$ and $f^{[n+1]} = f \circ f^{[n]}$. Then $f^{[2026]}(3)$ equals",
  r"$-\frac{1}{2}$",
  [(r"$\frac{2}{3}$", r"Takes $2026 \equiv 2 \pmod 3$ (arithmetic slip), giving $f^{[2]}(3) = \frac{3 - 1}{3}$."),
   (r"$3$", r"Assumes $f \circ f$ is the identity (period $2$), so an even number of compositions returns $3$."),
   (r"$\frac{1}{2}$", r"Correct period, but evaluates $\frac{1}{1 - 3}$ with a sign slip.")],
  r"$f(f(x)) = \frac{1}{1 - \frac{1}{1 - x}} = \frac{1 - x}{-x} = \frac{x - 1}{x}$ and $f(f(f(x))) = \frac{1}{1 - \frac{x - 1}{x}} = x$. So $f^{[3]}$ is the identity and $f^{[n]}$ depends on $n \bmod 3$. Since $2026 = 3 \cdot 675 + 1$, $f^{[2026]}(3) = f(3) = \frac{1}{1 - 3} = -\frac{1}{2}$.",
  r"Guessing the period instead of computing $f \circ f$ and $f \circ f \circ f$.",
  "U01-C-iterate-composition", "Two composites to find the period, then modular reduction.",
  check=_c036, values=[-Rational(1, 2), Rational(2, 3), 3, Rational(1, 2)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 037
def _c037():
    return sum(1 for f in it.product(range(1, 4), repeat=5) if set(f) == {1, 2, 3} and f[0] == 1)
q("U01-C-037", "Functions", "Onto functions with a prescribed value", "Difficult", "Multi-step computation MCQ",
  r"The number of onto functions $f: \{1, 2, 3, 4, 5\} \to \{1, 2, 3\}$ with $f(1) = 1$ is",
  r"$50$",
  [(r"$150$", r"Counts all onto functions, ignoring $f(1) = 1$."),
   (r"$36$", r"Requires $\{2, 3, 4, 5\}$ to map onto all of $\{1, 2, 3\}$, though $1$ is already covered."),
   (r"$14$", r"Requires $\{2, 3, 4, 5\}$ to map onto $\{2, 3\}$ only, not allowing further elements to map to $1$.")],
  r"Since $f(1) = 1$, $f$ is onto exactly when the images of $2, 3, 4, 5$ (each in $\{1, 2, 3\}$) include both $2$ and $3$. Of the $3^4 = 81$ such maps, $2^4 = 16$ miss $2$, $16$ miss $3$, and $1$ misses both. So the count is $81 - 16 - 16 + 1 = 50$. (By symmetry this is also $\frac{150}{3}$.)",
  r"Over- or under-restricting the remaining elements after fixing one image.",
  "U01-C-onto-with-condition", "Reformulate the condition, then inclusion-exclusion; two traps.",
  check=_c037, values=[50, 150, 36, 14], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The number of onto functions $f: \{1, 2, 3, 4, 5\} \to \{1, 2, 3\}$ with $f(1) = 1$ is", answer=50))

# ---------------------------------------------------------------- 038
def _c038():
    return sum(1 for p in it.permutations(range(1, 6)) if all(p[i] != i + 1 for i in range(5)))
q("U01-C-038", "Functions", "Bijections with no fixed point", "Difficult", "Multi-step computation MCQ",
  r"Let $P = \{1, 2, 3, 4, 5\}$. The number of bijections $f: P \to P$ such that $f(i) \ne i$ for every $i \in P$ is",
  r"$44$",
  [(r"$76$", r"Computes the bijections with at least one fixed point, $120 - 44$."),
   (r"$1024$", r"Counts all functions with $f(i) \ne i$, $4^5$, not requiring bijectivity."),
   (r"$96$", r"Multiplies $4 \cdot 4 \cdot 3 \cdot 2 \cdot 1$, assuming each later element always loses exactly one option.")],
  r"By inclusion-exclusion, the number is $5! - {}^5C_1 4! + {}^5C_2 3! - {}^5C_3 2! + {}^5C_4 1! - {}^5C_5 0! = 120 - 120 + 60 - 20 + 5 - 1 = 44$.",
  r"Using a naive product rule where the number of choices depends on earlier choices.",
  "U01-C-derangement", "Inclusion-exclusion with five terms.",
  check=_c038, values=[44, 76, 1024, 96], cognitive="Application", source_class=XII,
  numerical=dict(question=r"Let $P = \{1, 2, 3, 4, 5\}$. The number of bijections $f: P \to P$ such that $f(i) \ne i$ for every $i \in P$ is", answer=44))

# ---------------------------------------------------------------- 039
def _c039():
    return sum(1 for f in it.product(range(4), repeat=4) if all(f[f[i]] == i for i in range(4)))
q("U01-C-039", "Functions", "Functions equal to their own inverse", "Difficult", "Multi-step computation MCQ",
  r"Let $P = \{1, 2, 3, 4\}$. The number of functions $f: P \to P$ such that $f(f(x)) = x$ for every $x \in P$ is",
  r"$10$",
  [(r"$9$", r"Omits the identity function."),
   (r"$7$", r"Counts the identity and the $6$ single swaps but misses the $3$ maps made of two swaps."),
   (r"$24$", r"Notes that such $f$ must be a bijection and counts all $4!$ bijections.")],
  r"$f(f(x)) = x$ forces $f$ to be a bijection whose inverse is itself, so $f$ fixes some elements and swaps the rest in pairs. No swap: $1$ (identity). One swap: ${}^4C_2 = 6$. Two swaps: $\frac{{}^4C_2}{2} = 3$. Total $1 + 6 + 3 = 10$.",
  r"Missing a case (identity or double swaps) in the casework.",
  "U01-C-involution-count", "Casework on the cycle structure.",
  check=_c039, values=[10, 9, 7, 24], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"Let $P = \{1, 2, 3, 4\}$. The number of functions $f: P \to P$ such that $f(f(x)) = x$ for every $x \in P$ is", answer=10))

# ---------------------------------------------------------------- 040
def _c040():
    fs = list(it.product(range(4), repeat=4))
    s1 = sum(1 for f in fs if all(f[f[i]] == f[i] for i in range(4))) == 41
    s2 = sum(1 for f in fs if len({f[f[i]] for i in range(4)}) == 1) == 92
    return (s1, s2)
q("U01-C-040", "Functions", "Counting functions with composition conditions", "Difficult", "Statement-based MCQ",
  r"Let $P = \{1, 2, 3, 4\}$. Statement I: The number of functions $f: P \to P$ with $f(f(x)) = f(x)$ for every $x \in P$ is $41$. Statement II: The number of functions $f: P \to P$ for which $f \circ f$ is a constant function is $92$. In the light of the above statements, choose the correct answer.",
  ST_OPTS[2],
  [(ST_OPTS[0], r"Accepts Statement II by fixing $c$ with $f(c) = c$, choosing the set $S$ of other elements sent to $c$, and then letting each remaining element go anywhere in $S \cup \{c\}$; this gives $4(1 + 12 + 9 + 1) = 92$, so a map that sends a remaining element to $c$ is counted under more than one choice of $S$."),
   (ST_OPTS[1], r"Rejects Statement I by writing the count for a range of size $k$ as ${}^4C_k (4 - k)^k$ instead of ${}^4C_k k^{4 - k}$, getting $12 + 24 + 4 + 0 = 40$, and rejects Statement II correctly."),
   (ST_OPTS[3], r"Rejects Statement I by counting only the maps with range of size $1$ or $4$ (the $4$ constants and the identity), $5$ in all, and accepts Statement II through the overcount $92$.")],
  r"Statement I: $f(f(x)) = f(x)$ means $f$ fixes every element of its range. For a range of $k$ elements, choose it in ${}^4C_k$ ways and send each of the other $4 - k$ elements into it in $k^{4-k}$ ways: $4 \cdot 1 + 6 \cdot 4 + 4 \cdot 3 + 1 \cdot 1 = 41$, so Statement I is true. Statement II: if $f(f(x)) = c$ for all $x$, then $f(c) = f(f(f(c))) = c$. Let $S$ be the set of elements other than $c$ with $f(x) = c$; every other element $x \ne c$ has $f(x) \ne c$ and $f(f(x)) = c$, so $f(x) \in S$, and conversely every such map works. With $s = |S|$ out of the $3$ elements other than $c$, the count is ${}^3C_s s^{3-s}$, i.e. $0 + 3 + 6 + 1 = 10$ for each $c$, so $4 \cdot 10 = 40 \ne 92$. Statement II is false.",
  r"Letting an element outside $f^{-1}(c)$ map directly to $c$, which overcounts, or interchanging base and exponent in ${}^nC_k k^{n-k}$.",
  "U01-C-idempotent-constant-square", "Two separate casework counts on a $4$-element set, one needing a structural argument about $f^{-1}(c)$.",
  check=_c040, values=[(T, F_), (T, T), (F_, F_), (F_, T)], cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 041
def _c041():
    cnt = 0
    for kk in range(-10, 11):
        inj, onto = _classify_pieces((kk + 3)*x, (kk - 3)*x, R)
        cnt += int(inj and onto)
    return cnt
q("U01-C-041", "Functions", "Parameter values making a function bijective", "Difficult", "Inverse/parameter MCQ",
  r"For an integer $k$, let $f_k: \mathbb{R} \to \mathbb{R}$ be defined by $f_k(x) = kx + 3|x|$. The number of integers $k$ with $-10 \le k \le 10$ for which $f_k$ is bijective is",
  r"$14$",
  [(r"$16$", r"Uses $|k| \ge 3$, including $k = \pm 3$, where one piece is constant ($0$ on a half-line)."),
   (r"$7$", r"Counts the integers with $|k| \le 3$, i.e. the values where the slopes differ in sign or one vanishes, which is the complement."),
   (r"$8$", r"Accepts only non-negative slopes and includes the boundary, counting $k = 3, 4, \ldots, 10$.")],
  r"For $x \ge 0$, $f_k(x) = (k + 3)x$; for $x < 0$, $f_k(x) = (k - 3)x$. If the two slopes have the same sign (both non-zero), $f_k$ is strictly monotonic with range $\mathbb{R}$, hence bijective. If they have opposite signs or one is zero, $f_k$ is not one-one (and its range is a half-line). So we need $(k + 3)(k - 3) > 0$, i.e. $|k| > 3$: $k = 4, \ldots, 10$ and $k = -10, \ldots, -4$, which is $7 + 7 = 14$ values.",
  r"Including the boundary case where a piece becomes constant.",
  "U01-C-param-bijective-abs", "Split by sign of $x$, sign analysis of slopes, boundary trap and counting.",
  check=_c041, values=[14, 16, 7, 8], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"For an integer $k$, let $f_k: \mathbb{R} \to \mathbb{R}$ be defined by $f_k(x) = kx + 3|x|$. The number of integers $k$ with $-10 \le k \le 10$ for which $f_k$ is bijective is", answer=14))

# ---------------------------------------------------------------- 042
def _c042():
    sols = solve(Eq((exp(y) - exp(-y))/2, x), y)
    good = [s for s in sols if im(N(s.subs(x, 1))) == 0 and im(N(s.subs(x, -1))) == 0]
    return good[0] if len(good) == 1 else None
q("U01-C-042", "Functions", "Inverse of an exponential bijection", "Difficult", "Multi-step computation MCQ",
  r"The function $f: \mathbb{R} \to \mathbb{R}$, $f(x) = \frac{e^x - e^{-x}}{2}$, is a bijection. Then $f^{-1}(x)$ equals",
  r"$\log_e\left(x + \sqrt{x^2 + 1}\right)$",
  [(r"$\log_e\left(\sqrt{x^2 + 1} - x\right)$", r"Takes the root $x - \sqrt{x^2 + 1}$, sees it is negative and replaces it by its absolute value."),
   (r"$\log_e\left(\frac{x + \sqrt{x^2 + 4}}{2}\right)$", r"Writes the quadratic as $e^{2y} - x e^y - 1 = 0$, dropping the factor $2$."),
   (r"$\log_e\left(x + \sqrt{x^2 - 1}\right)$", r"Sign slip in the discriminant: uses $4x^2 - 4$ instead of $4x^2 + 4$.")],
  r"Let $y = \frac{e^x - e^{-x}}{2}$ and $u = e^x > 0$. Then $u^2 - 2yu - 1 = 0$, so $u = y \pm \sqrt{y^2 + 1}$. Since $\sqrt{y^2 + 1} > |y|$, only $u = y + \sqrt{y^2 + 1}$ is positive. Hence $x = \log_e\left(y + \sqrt{y^2 + 1}\right)$ and $f^{-1}(x) = \log_e\left(x + \sqrt{x^2 + 1}\right)$.",
  r"Mishandling the quadratic in $e^x$ or the choice of the positive root.",
  "U01-C-inverse-exponential", "Substitution to a quadratic, solving, and rejecting a root.",
  check=_c042, values=[log(x + sqrt(x**2 + 1)), log(sqrt(x**2 + 1) - x), log((x + sqrt(x**2 + 4))/2), log(x + sqrt(x**2 - 1))],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 043
q("U01-C-043", "Functions", "Codomain that makes a function onto", "Difficult", "Multi-step computation MCQ",
  r"Let $f: \mathbb{R} \to S$ be defined by $f(x) = \frac{x^2 - x + 1}{x^2 + x + 1}$. If $f$ is onto, then $S$ equals",
  r"$\left[\frac{1}{3}, 3\right]$",
  [(r"$\left(\frac{1}{3}, 3\right)$", r"Solves the discriminant condition with strict inequality, excluding the attained values at $x = 1$ and $x = -1$."),
   (r"$\left[\frac{1}{3}, 1\right]$", r"Considers only $x \ge 0$, where the numerator does not exceed the denominator."),
   (r"$\left[1, 3\right]$", r"Considers only $x \le 0$.")],
  r"Put $y = f(x)$: $(y - 1)x^2 + (y + 1)x + (y - 1) = 0$. For $y \ne 1$, a real $x$ exists iff $(y + 1)^2 - 4(y - 1)^2 \ge 0$, i.e. $(3 - y)(3y - 1) \ge 0$, so $\frac{1}{3} \le y \le 3$; $y = 1$ is attained at $x = 0$. Also $f(1) = \frac{1}{3}$ and $f(-1) = 3$. So the range is $\left[\frac{1}{3}, 3\right]$, and onto requires $S$ to equal it.",
  r"Dropping end points or half of the domain when finding a range.",
  "U01-C-onto-codomain", "Quadratic in $x$, discriminant inequality, endpoint check.",
  check=lambda: function_range((x**2 - x + 1)/(x**2 + x + 1), x, R),
  values=[Interval(Rational(1, 3), 3), Interval.open(Rational(1, 3), 3), Interval(Rational(1, 3), 1), Interval(1, 3)],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 044
def _c044():
    fpw = Piecewise((x + 2, x < 0), (x**2 - 1, True))
    ys = solveset(fpw, x, R)
    total = set()
    for yv in ys:
        total |= set(solveset(Eq(fpw, yv), x, R))
    return len(total)
q("U01-C-044", "Functions", "Solving an equation with a piecewise composite", "Difficult", "Multi-step computation MCQ",
  r"Let $f: \mathbb{R} \to \mathbb{R}$ be defined by $f(x) = x + 2$ for $x < 0$ and $f(x) = x^2 - 1$ for $x \ge 0$. The number of real solutions of $(f \circ f)(x) = 0$ is",
  r"$3$",
  [(r"$4$", r"Accepts $x = -\sqrt{2}$ from $x^2 - 1 = 1$ without checking $x \ge 0$."),
   (r"$5$", r"Accepts $y = -1$ as a root of $f(y) = 0$ from $y^2 - 1 = 0$ without checking $y \ge 0$, adding $x = -3$ and $x = 0$."),
   (r"$2$", r"Uses only the root $y = 1$ of $f(y) = 0$, missing $y = -2$ from the first branch.")],
  r"First $f(y) = 0$: for $y < 0$, $y = -2$; for $y \ge 0$, $y = 1$. Now $f(x) = -2$: $x + 2 = -2$ gives $x = -4$; $x^2 - 1 = -2$ has no solution. And $f(x) = 1$: $x + 2 = 1$ gives $x = -1$; $x^2 - 1 = 1$ with $x \ge 0$ gives $x = \sqrt{2}$. So the solutions are $-4, -1, \sqrt{2}$: three in all.",
  r"Not checking branch conditions at each stage of a composite.",
  "U01-C-piecewise-composite-equation", "Two-stage casework with branch conditions.",
  check=_c044, values=[3, 4, 5, 2], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"Let $f: \mathbb{R} \to \mathbb{R}$ be defined by $f(x) = x + 2$ for $x < 0$ and $f(x) = x^2 - 1$ for $x \ge 0$. The number of real solutions of $(f \circ f)(x) = 0$ is", answer=3))

# ---------------------------------------------------------------- 045
def _c045():
    return sum(1 for p in it.permutations(range(1, 6), 3) if all(p[i] != i + 1 for i in range(3)))
q("U01-C-045", "Functions", "One-one functions avoiding fixed values", "Difficult", "Multi-step computation MCQ",
  r"The number of one-one functions $f: \{1, 2, 3\} \to \{1, 2, 3, 4, 5\}$ such that $f(i) \ne i$ for $i = 1, 2, 3$ is",
  r"$32$",
  [(r"$24$", r"Assumes each step loses exactly one more option: $4 \cdot 3 \cdot 2$."),
   (r"$34$", r"Sign slip in the last inclusion-exclusion term: $60 - 36 + 9 + 1$."),
   (r"$60$", r"Counts all one-one functions ${}^5P_3$, ignoring the condition.")],
  r"Total one-one functions: ${}^5P_3 = 60$. With $f(i) = i$ for a given $i$: ${}^4P_2 = 12$, three choices of $i$. For two given fixed points: ${}^3P_1 = 3$, three pairs. All three fixed: $1$. By inclusion-exclusion, $60 - 36 + 9 - 1 = 32$.",
  r"Treating the choices as independent of earlier choices.",
  "U01-C-injection-no-fixed", "Four-term inclusion-exclusion with permutations.",
  check=_c045, values=[32, 24, 34, 60], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The number of one-one functions $f: \{1, 2, 3\} \to \{1, 2, 3, 4, 5\}$ such that $f(i) \ne i$ for $i = 1, 2, 3$ is", answer=32))

# ---------------------------------------------------------------- 046
def _c046():
    return sum(1 for f in it.product(range(1, 7), repeat=4) if f[0] <= f[1] <= f[2] <= f[3])
q("U01-C-046", "Functions", "Non-decreasing functions", "Difficult", "Multi-step computation MCQ",
  r"The number of functions $f: \{1, 2, 3, 4\} \to \{1, 2, 3, 4, 5, 6\}$ such that $f(1) \le f(2) \le f(3) \le f(4)$ is",
  r"$126$",
  [(r"$15$", r"Counts strictly increasing functions, ${}^6C_4$."),
   (r"$210$", r"Off by one in stars and bars, using ${}^{10}C_4$."),
   (r"$84$", r"Uses ${}^9C_3$ instead of ${}^9C_4$, choosing the wrong lower index.")],
  r"A non-decreasing $f$ is determined by how many of the $4$ inputs take each value $1, \ldots, 6$, i.e. by non-negative integers $n_1 + \cdots + n_6 = 4$. The number of solutions is ${}^{4 + 6 - 1}C_{4} = {}^9C_4 = 126$. Equivalently, $g(i) = f(i) + i - 1$ is strictly increasing into $\{1, \ldots, 9\}$, giving ${}^9C_4$.",
  r"Treating non-decreasing as strictly increasing, or misapplying stars and bars.",
  "U01-C-count-nondecreasing", "Bijection to multisets or stars and bars; non-obvious route.",
  check=_c046, values=[126, 15, 210, 84], cognitive="Analysis", source_class=XII,
  numerical=dict(question=r"The number of functions $f: \{1, 2, 3, 4\} \to \{1, 2, 3, 4, 5, 6\}$ such that $f(1) \le f(2) \le f(3) \le f(4)$ is", answer=126))
