import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
X, Y = symbols('x y', real=True)
_U, _V = symbols('u v', nonnegative=True)


def zsols(f):
    """All solutions z of f(z) = 0, found by writing z = x + iy with x, y real.
    Sign cases for x and y are separated so that |z| and conj(z) stay algebraic."""
    out = []
    for sx in (1, -1):
        for sy in (1, -1):
            e = expand(f(sx*_U + I*sy*_V))
            for s in solve([re(e), im(e)], [_U, _V], dict=True):
                uu = s.get(_U, _U); vv = s.get(_V, _V)
                if uu.free_symbols or vv.free_symbols:
                    raise ValueError("one-parameter family of solutions: %s" % s)
                w = simplify(sx*uu + I*sy*vv)
                if not any(simplify(w - t) == 0 for t in out):
                    out.append(w)
    return out


def sqrts(w):
    """Square roots of w, by solving (x + iy)^2 = w with x, y real."""
    e = expand((X + I*Y)**2 - w)
    return FiniteSet(*[s[X] + I*s[Y] for s in solve([re(e), im(e)], [X, Y], dict=True)])


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."

# ================================================================ EASY (17)

q("U02-A-001", "Algebra of complex numbers", "Complex numbers as ordered pairs: product", "Easy",
  "Single-step computation MCQ",
  r"Treating complex numbers as ordered pairs of real numbers, the product $(2, 3) \cdot (1, -1)$ equals",
  r"$(5, 1)$",
  [(r"$(2, -3)$", "Multiplies component by component, $(2)(1)$ and $(3)(-1)$."),
   (r"$(-1, 1)$", "Uses $ac + bd$ for the first component, a sign slip in the definition, giving $(2 - 3, -2 + 3)$."),
   (r"$(5, -5)$", r"Uses $ad - bc$ for the second component, giving $-2 - 3 = -5$.")],
  r"By definition $(a, b)(c, d) = (ac - bd,\ ad + bc)$. Here $ac - bd = 2 - (3)(-1) = 5$ and $ad + bc = -2 + 3 = 1$, so the product is $(5, 1)$, which is $(2+3i)(1-i) = 5 + i$.",
  "Multiplying ordered pairs componentwise as if they were vectors.",
  "U02-A-ordered-pair-product", "Direct use of the ordered-pair product rule.",
  check=lambda: expand((2 + 3*I)*(1 - I)),
  values=[5 + I, 2 - 3*I, -1 + I, 5 - 5*I], cognitive="Application")

q("U02-A-002", "Algebra of complex numbers", "Multiplicative inverse as an ordered pair", "Easy",
  "Single-step computation MCQ",
  r"The multiplicative inverse of the complex number $(3, 4)$, written as an ordered pair, is",
  r"$\left(\frac{3}{25}, -\frac{4}{25}\right)$",
  [(r"$\left(\frac{3}{5}, -\frac{4}{5}\right)$", "Divides the conjugate by the modulus $5$ rather than the squared modulus $25$."),
   (r"$\left(\frac{1}{3}, \frac{1}{4}\right)$", "Takes reciprocals of each component."),
   (r"$\left(\frac{3}{25}, \frac{4}{25}\right)$", "Divides by the squared modulus but does not conjugate.")],
  r"For $(a, b) \ne (0, 0)$ the inverse is $\left(\frac{a}{a^2+b^2}, \frac{-b}{a^2+b^2}\right)$. With $a^2 + b^2 = 25$ this is $\left(\frac{3}{25}, -\frac{4}{25}\right)$; indeed $\frac{1}{3+4i} = \frac{3-4i}{25}$.",
  "Taking componentwise reciprocals of an ordered pair.",
  "U02-A-inverse-ordered-pair", "One formula, one step.",
  check=lambda: expand(1/(3 + 4*I)),
  values=[Rational(3, 25) - Rational(4, 25)*I, Rational(3, 5) - Rational(4, 5)*I,
          Rational(1, 3) + Rational(1, 4)*I, Rational(3, 25) + Rational(4, 25)*I], cognitive="Application")

q("U02-A-003", "Algebra of complex numbers", "Negative integral power of i", "Easy",
  "Single-step computation MCQ",
  r"The value of $i^{-35}$ is",
  r"$i$",
  [(r"$-i$", "Finds $i^{35} = -i$ and does not take the reciprocal."),
   (r"$1$", "Rounds the exponent to the nearby multiple of $4$, using $i^{-36} = 1$."),
   (r"$-1$", r"Reduces $35 \bmod 4$ incorrectly as $2$, so $i^{35} = -1$ and $i^{-35} = -1$.")],
  r"$i^{35} = i^{32} \cdot i^3 = -i$, so $i^{-35} = \frac{1}{-i} = \frac{i}{-i \cdot i} = i$. Equivalently $i^{-35} = i^{-36} \cdot i = i$.",
  "Ignoring the reciprocal in a negative power.",
  "U02-A-power-i-negative", "Single reduction modulo $4$ plus a reciprocal.",
  check=lambda: simplify(I**(-35)),
  values=[I, -I, 1, -1], cognitive="Application")

q("U02-A-004", "Algebra of complex numbers", "Sum of consecutive powers of i", "Easy",
  "Single-step computation MCQ",
  r"The value of $i + i^2 + i^3 + \dots + i^{2027}$ is",
  r"$-1$",
  [(r"$0$", "Assumes all the terms cancel in groups of four."),
   (r"$i$", r"Takes $2027 \bmod 4$ as $1$, keeping only the leftover term $i^{2025} = i$."),
   (r"$-1 + i$", r"Takes $2027 \bmod 4$ as $2$, keeping only $i + i^2$.")],
  r"Every block of four consecutive powers sums to $0$. Since $2027 = 4 \cdot 506 + 3$, the first $2024$ terms cancel and the sum is $i^{2025} + i^{2026} + i^{2027} = i - 1 - i = -1$.",
  "Assuming the whole sum vanishes without checking the leftover terms.",
  "U02-A-sum-powers-i", "Cycle of length four, one remainder computation.",
  check=lambda: sum(I**k for k in range(1, 2028)),
  values=[-1, 0, I, -1 + I], cognitive="Application")

q("U02-A-005", "Algebra of complex numbers", "Equality of complex numbers", "Easy",
  "Single-step computation MCQ",
  r"If $x$ and $y$ are real and $(x + 2y) + i(2x - y) = 4 + 3i$, then $x + y$ equals",
  r"$3$",
  [(r"$1$", "Finds $x = 2$, $y = 1$ but computes $x - y$."),
   (r"$7$", "Adds the real and imaginary parts of the right side, $4 + 3$."),
   (r"$\frac{7}{3}$", r"Copies the imaginary-part equation as $2x + y = 3$, a sign slip, giving $x = \frac{2}{3}$, $y = \frac{5}{3}$.")],
  r"Equating parts, $x + 2y = 4$ and $2x - y = 3$. Doubling the second and adding gives $5x = 10$, so $x = 2$, $y = 1$ and $x + y = 3$.",
  "Not separating real and imaginary parts into two equations.",
  "U02-A-equality-linear", "Two linear equations from one complex equality.",
  check=lambda: (lambda s: s[X] + s[Y])(solve([X + 2*Y - 4, 2*X - Y - 3], [X, Y])),
  values=[3, 1, 7, Rational(7, 3)],
  numerical=dict(question=r"If $x$ and $y$ are real and $(x + 2y) + i(2x - y) = 4 + 3i$, then the value of $x + y$ is", answer=3),
  cognitive="Application")

q("U02-A-006", "Algebra of complex numbers", "Conjugate of a product", "Easy",
  "Single-step computation MCQ",
  r"If $z = (1 + 2i)(2 - i)$, then $\overline{z}$ equals",
  r"$4 - 3i$",
  [(r"$4 + 3i$", "Computes $z$ but does not take the conjugate."),
   (r"$-3i$", "Uses $i^2 = 1$ while expanding, getting $z = 3i$."),
   (r"$-4 + 3i$", "Changes the sign of the real part instead of the imaginary part.")],
  r"$z = 2 - i + 4i - 2i^2 = 4 + 3i$, so $\overline{z} = 4 - 3i$. Alternatively $\overline{z} = (1 - 2i)(2 + i) = 4 - 3i$.",
  "Conjugating by negating the real part.",
  "U02-A-conjugate-product", "One expansion and one conjugation.",
  check=lambda: expand(conjugate((1 + 2*I)*(2 - I))),
  values=[4 - 3*I, 4 + 3*I, -3*I, -4 + 3*I], cognitive="Application")

q("U02-A-007", "Algebra of complex numbers", "Quotient in a + ib form", "Easy",
  "Single-step computation MCQ",
  r"When $\frac{3 + 2i}{1 + i}$ is written in the form $a + ib$ with $a, b$ real, it equals",
  r"$\frac{5}{2} - \frac{1}{2}i$",
  [(r"$\frac{1}{2} + \frac{5}{2}i$", "Multiplies numerator and denominator by $1 + i$ instead of $1 - i$."),
   (r"$5 - i$", "Does not divide by $(1+i)(1-i) = 2$."),
   (r"$\frac{5}{2} + \frac{1}{2}i$", "Sign slip in the imaginary part, $-3i + 2i$ taken as $+i$.")],
  r"$\frac{3+2i}{1+i} = \frac{(3+2i)(1-i)}{2} = \frac{3 - 3i + 2i + 2}{2} = \frac{5 - i}{2}$.",
  "Rationalising with the wrong factor.",
  "U02-A-quotient-a-ib", "Single rationalisation.",
  check=lambda: expand((3 + 2*I)/(1 + I)),
  values=[Rational(5, 2) - I/2, Rational(1, 2) + Rational(5, 2)*I, 5 - I, Rational(5, 2) + I/2],
  cognitive="Application")

q("U02-A-008", "Algebra of complex numbers", "Modulus of a multiplicative inverse", "Easy",
  "Single-step computation MCQ",
  r"If $w$ is the multiplicative inverse of $z = (3 - i)^2$, then $|w|$ equals",
  r"$\frac{1}{10}$",
  [(r"$\frac{1}{\sqrt{10}}$", r"Uses $|z| = |3 - i| = \sqrt{10}$, forgetting that $z$ is the square of $3 - i$."),
   (r"$\frac{1}{100}$", r"Confuses $|w|$ with the denominator of the inverse formula, taking $|w| = \frac{1}{|z|^2}$ with $|z|^2 = 100$."),
   (r"$\frac{1}{2\sqrt{7}}$", r"Expands $z = 8 - 6i$ correctly but computes its modulus as $\sqrt{8^2 - 6^2} = \sqrt{28}$.")],
  r"Since $zw = 1$, $|w| = \frac{1}{|z|}$. Here $|z| = |3 - i|^2 = 9 + 1 = 10$ (equivalently $z = 8 - 6i$ and $\sqrt{64 + 36} = 10$), so $|w| = \frac{1}{10}$.",
  r"Forgetting that $|z^2| = |z|^2$, or confusing $|z^{-1}|$ with $\frac{1}{|z|^2}$.",
  "U02-A-inverse-modulus", r"One property, $|z^{-1}| = \frac{1}{|z|}$, applied to a square.",
  check=lambda: simplify(Abs(1/expand((3 - I)**2))),
  values=[Rational(1, 10), 1/sqrt(10), Rational(1, 100), 1/(2*sqrt(7))], cognitive="Application")

q("U02-A-009", "Algebra of complex numbers", "Condition for a quotient to be purely real", "Easy",
  "Inverse/parameter MCQ",
  r"If $a$ is real and $\frac{a + 3i}{2 + i}$ is purely real, then $a$ equals",
  r"$6$",
  [(r"$-\frac{3}{2}$", "Sets the real part $2a + 3$ to zero, the condition for a purely imaginary quotient."),
   (r"$-6$", "Rationalises with $2 + i$, giving imaginary part $a + 6$."),
   (r"$\frac{3}{2}$", "Sets the real part $2a + 3$ to zero and slips the sign of $a$.")],
  r"$\frac{a+3i}{2+i} = \frac{(a+3i)(2-i)}{5} = \frac{(2a + 3) + (6 - a)i}{5}$. It is purely real when $6 - a = 0$, that is $a = 6$ (the quotient is then $3$).",
  "Mixing up the conditions for purely real and purely imaginary.",
  "U02-A-param-purely-real", "One rationalisation and one condition.",
  check=lambda: (lambda a: solve(im(expand((a + 3*I)*(2 - I)/5)), a)[0])(symbols('a', real=True)),
  values=[6, Rational(-3, 2), -6, Rational(3, 2)], cognitive="Application")

q("U02-A-010", "Algebra of complex numbers", "Square roots of a complex number", "Easy",
  "Single-step computation MCQ",
  r"The square roots of $-5 + 12i$ are",
  r"$\pm(2 + 3i)$",
  [(r"$\pm(3 + 2i)$", "Writes $x^2 - y^2 = 5$ instead of $-5$, so $x^2 = 9$, $y^2 = 4$."),
   (r"$\pm(2 - 3i)$", "Ignores that $xy$ must be positive because the imaginary part $12$ is positive."),
   (r"$\pm(3 - 2i)$", "Both slips together: writes $x^2 - y^2 = 5$ and ignores the sign of $xy$.")],
  r"Let $(x + iy)^2 = -5 + 12i$. Then $x^2 - y^2 = -5$, $2xy = 12$ and $x^2 + y^2 = |{-5 + 12i}| = 13$. So $x^2 = 4$, $y^2 = 9$, and $xy > 0$ gives $\pm(2 + 3i)$.",
  "Ignoring the sign of $xy$ when pairing the values of $x$ and $y$.",
  "U02-A-sqrt-basic", "Standard three-equation method.",
  check=lambda: sqrts(-5 + 12*I),
  values=[FiniteSet(2 + 3*I, -2 - 3*I), FiniteSet(3 + 2*I, -3 - 2*I),
          FiniteSet(2 - 3*I, -2 + 3*I), FiniteSet(3 - 2*I, -3 + 2*I)], cognitive="Application")

q("U02-A-011", "Algebra of complex numbers", "Conjugate: z times conjugate and z plus conjugate", "Easy",
  "Single-step computation MCQ",
  r"If $z = 3 - 4i$, then $z\overline{z} + z + \overline{z}$ equals",
  r"$31$",
  [(r"$19$", r"Takes $z + \overline{z} = -6$, a sign slip."),
   (r"$-1$", r"Takes $z\overline{z} = 9 - 16 = -7$."),
   (r"$17$", r"Takes $z + \overline{z} = 2\operatorname{Im}(z) = -8$.")],
  r"$z\overline{z} = |z|^2 = 9 + 16 = 25$ and $z + \overline{z} = 2\operatorname{Re}(z) = 6$, so the value is $31$.",
  r"Computing $z\overline{z}$ as $a^2 - b^2$.",
  "U02-A-conjugate-identities", "Two standard conjugate identities.",
  check=lambda: expand((3 - 4*I)*conjugate(3 - 4*I) + (3 - 4*I) + conjugate(3 - 4*I)),
  values=[31, 19, -1, 17], cognitive="Application")

q("U02-A-012", "Algebra of complex numbers", "Product with a conjugate", "Easy",
  "Single-step computation MCQ",
  r"If $z_1 = 2 + i$ and $z_2 = 1 - 3i$, then $\operatorname{Re}(z_1\overline{z_2})$ equals",
  r"$-1$",
  [(r"$5$", r"Computes $\operatorname{Re}(z_1 z_2)$, not conjugating $z_2$."),
   (r"$2$", "Multiplies the real parts only."),
   (r"$7$", r"Reports the imaginary part of $z_1\overline{z_2}$.")],
  r"$\overline{z_2} = 1 + 3i$, so $z_1\overline{z_2} = (2 + i)(1 + 3i) = 2 + 6i + i + 3i^2 = -1 + 7i$. The real part is $-1$.",
  "Treating the real part of a product as the product of real parts.",
  "U02-A-conjugate-product-re", "One conjugation and one product.",
  check=lambda: re(expand((2 + I)*conjugate(1 - 3*I))),
  values=[-1, 5, 2, 7], cognitive="Application")

q("U02-A-013", "Algebra of complex numbers", "Ordered pair (0, 1) as i", "Easy",
  "Direct concept MCQ",
  r"In the ordered-pair representation of complex numbers, $(0, 1) \cdot (0, 1)$ equals",
  r"$(-1, 0)$",
  [(r"$(0, 1)$", "Multiplies componentwise: $(0)(0)$ and $(1)(1)$."),
   (r"$(1, 0)$", "Uses $ac + bd$ for the first component."),
   (r"$(0, 2)$", "Adds the pairs instead of multiplying them.")],
  r"$(a, b)(c, d) = (ac - bd, ad + bc)$ gives $(0 - 1, 0 + 0) = (-1, 0)$. This is the statement $i^2 = -1$, since $(0, 1)$ represents $i$.",
  "Treating ordered-pair multiplication as componentwise.",
  "U02-A-ordered-pair-i", "Recognising that $(0, 1)$ is $i$.",
  check=lambda: expand(I*I),
  values=[-1, I, 1, 2*I], cognitive="Recall")

q("U02-A-014", "Algebra of complex numbers", "Powers of i with reciprocal", "Easy",
  "Single-step computation MCQ",
  r"The value of $i^{57} + \frac{1}{i^{125}}$ is",
  r"$0$",
  [(r"$2i$", r"Takes $\frac{1}{i^{125}}$ to be $i^{125} = i$."),
   (r"$-2i$", r"Takes $i^{57} = -i$ by reducing $57 \bmod 4$ as $3$."),
   (r"$1 - i$", "Takes $i^{57} = 1$, treating $57$ as a multiple of $4$.")],
  r"$57 = 4 \cdot 14 + 1$ and $125 = 4 \cdot 31 + 1$, so $i^{57} = i$ and $\frac{1}{i^{125}} = \frac{1}{i} = -i$. The sum is $0$.",
  r"Forgetting that $\frac{1}{i} = -i$.",
  "U02-A-power-i-reciprocal", "Two reductions modulo $4$ and one reciprocal.",
  check=lambda: simplify(I**57 + 1/I**125),
  values=[0, 2*I, -2*I, 1 - I], cognitive="Application")

q("U02-A-015", "Algebra of complex numbers", "Expression in a + ib form", "Easy",
  "Single-step computation MCQ",
  r"The complex number $\frac{(1 + i)^2}{2 - i}$ equals",
  r"$-\frac{2}{5} + \frac{4}{5}i$",
  [(r"$\frac{2}{5} + \frac{4}{5}i$", "Rationalises with $2 - i$ instead of $2 + i$."),
   (r"$\frac{2}{5} + \frac{6}{5}i$", "Expands $(1+i)^2$ as $2 + 2i$, using $i^2 = 1$."),
   (r"$-\frac{2}{3} + \frac{4}{3}i$", "Divides by $2^2 - 1^2 = 3$ instead of $2^2 + 1^2 = 5$.")],
  r"$(1 + i)^2 = 2i$, so the number is $\frac{2i}{2 - i} = \frac{2i(2 + i)}{5} = \frac{4i - 2}{5} = -\frac{2}{5} + \frac{4}{5}i$.",
  "Using $a^2 - b^2$ for $(a+ib)(a-ib)$.",
  "U02-A-quotient-a-ib", "Square then one rationalisation.",
  check=lambda: expand((1 + I)**2/(2 - I)),
  values=[Rational(-2, 5) + Rational(4, 5)*I, Rational(2, 5) + Rational(4, 5)*I,
          Rational(2, 5) + Rational(6, 5)*I, Rational(-2, 3) + Rational(4, 3)*I], cognitive="Application")

q("U02-A-016", "Algebra of complex numbers", "Equality: solving for real x, y", "Easy",
  "Single-step computation MCQ",
  r"If $x$ and $y$ are real and $(x + iy)(1 + i) = 2 - 4i$, then the ordered pair $(x, y)$ is",
  r"$(-1, -3)$",
  [(r"$(3, -1)$", r"Multiplies by $1 + i$ instead of $1 - i$ while rationalising, getting $\frac{(2 - 4i)(1 + i)}{2} = 3 - i$."),
   (r"$(1, 3)$", "Sign slip in both components of $-1 - 3i$."),
   (r"$(-2, -6)$", "Does not divide by $(1+i)(1-i) = 2$.")],
  r"$x + iy = \frac{2 - 4i}{1 + i} = \frac{(2 - 4i)(1 - i)}{2} = \frac{2 - 2i - 4i - 4}{2} = -1 - 3i$, so $(x, y) = (-1, -3)$.",
  "Rationalising with the wrong conjugate.",
  "U02-A-equality-division", "One division in $a + ib$ form.",
  check=lambda: (lambda s: s[X] + I*s[Y])(solve([re(expand((X + I*Y)*(1 + I) - 2 + 4*I)),
                                                  im(expand((X + I*Y)*(1 + I) - 2 + 4*I))], [X, Y])),
  values=[-1 - 3*I, 3 - I, 1 + 3*I, -2 - 6*I], cognitive="Application")

q("U02-A-017", "Algebra of complex numbers", "Powers of 1 + i and 1 - i", "Easy",
  "Single-step computation MCQ",
  r"The value of $(1 + i)^6 + (1 - i)^6$ is",
  r"$0$",
  [(r"$-16i$", "Assumes $(1 - i)^6 = (1 + i)^6$."),
   (r"$16$", r"Adds the moduli, taking $|1 \pm i|^6 = 8$ for each term."),
   (r"$-16$", "Takes $(1 - i)^2 = 2i$ as well (dropping the sign) and uses $i^3 = -1$, so each sixth power is $-8$.")],
  r"$(1 + i)^2 = 2i$ and $(1 - i)^2 = -2i$. Hence $(1 + i)^6 = (2i)^3 = -8i$ and $(1 - i)^6 = (-2i)^3 = 8i$, and the sum is $0$.",
  "Mishandling $i^3 = -i$.",
  "U02-A-binomial-power-i", "Squaring first, then a cube of a pure imaginary.",
  check=lambda: expand((1 + I)**6 + (1 - I)**6),
  values=[0, -16*I, 16, -16], cognitive="Application")

# ================================================================ MEDIUM (25)

q("U02-A-018", "Algebra of complex numbers", "Sum of i raised to factorials", "Medium",
  "Multi-step computation MCQ",
  r"The value of $\sum_{k=1}^{100} i^{k!}$ is",
  r"$95 + i$",
  [(r"$96$", "Takes $i^{3!}$ as $i^3 = -i$, confusing $3!$ with $3$."),
   (r"$94 + i$", "Counts $96$ terms from $k = 4$ to $k = 100$ instead of $97$."),
   (r"$99 + i$", "Takes every even power of $i$ to be $1$, so $i^{2!} = i^{3!} = 1$.")],
  r"For $k \ge 4$, $k!$ is a multiple of 4, so $i^{k!} = 1$; there are 97 such terms. The first three are $i^1 = i$, $i^2 = -1$, $i^6 = -1$. The sum is $i - 2 + 97 = 95 + i$.",
  "Treating every even exponent of $i$ as giving $1$.",
  "U02-A-sum-power-i-factorial", "Divisibility of $k!$ by $4$ plus careful counting and three exceptional terms.",
  check=lambda: sum(I**factorial(k) for k in range(1, 101)),
  values=[95 + I, 96, 94 + I, 99 + I], cognitive="Application")

q("U02-A-019", "Algebra of complex numbers", "Sum of pairs of powers of i", "Medium",
  "Multi-step computation MCQ",
  r"The value of $\sum_{n=1}^{13} \left(i^n + i^{n+1}\right)$ is",
  r"$-1 + i$",
  [(r"$1 + i$", r"Factors the sum as $(1 - i)\sum i^n$, a sign slip."),
   (r"$0$", "Assumes each of the two sums is $0$ over $13$ terms."),
   (r"$i$", r"Evaluates only $\sum_{n=1}^{13} i^n$.")],
  r"The sum is $(1 + i)\sum_{n=1}^{13} i^n$. The first 12 powers cancel in blocks of four, leaving $i^{13} = i$. So the value is $(1 + i)i = -1 + i$.",
  "Assuming any sum of powers of $i$ is zero.",
  "U02-A-sum-powers-i", "Factorisation plus cycle reduction.",
  check=lambda: expand(sum(I**n + I**(n + 1) for n in range(1, 14))),
  values=[-1 + I, 1 + I, 0, I], cognitive="Application")

def _c20():
    w = simplify((1 + I)/(1 - I))
    return next(n for n in range(1, 50) if simplify(w**n - 1) == 0)
q("U02-A-020", "Algebra of complex numbers", "Least n with a power of a quotient equal to 1", "Medium",
  "Inverse/parameter MCQ",
  r"The least positive integer $n$ for which $\left(\frac{1 + i}{1 - i}\right)^n = 1$ is",
  r"$4$",
  [(r"$2$", "Takes $i^2 = 1$."),
   (r"$8$", r"Simplifies the quotient to $\frac{1+i}{\sqrt{2}}$, whose powers repeat every $8$."),
   (r"$1$", "Assumes the quotient equals $1$ because numerator and denominator have equal modulus.")],
  r"$\frac{1 + i}{1 - i} = \frac{(1 + i)^2}{2} = \frac{2i}{2} = i$. Powers of $i$ first equal 1 at $n = 4$.",
  "Equal modulus taken to mean equal numbers.",
  "U02-A-least-n-power-i", "Simplify the quotient to $i$, then use the cycle of $i$.",
  check=_c20, values=[4, 2, 8, 1],
  numerical=dict(question=r"The least positive integer $n$ for which $\left(\frac{1 + i}{1 - i}\right)^n = 1$ is", answer=4),
  cognitive="Application")

def _c21():
    return next(n for n in range(1, 50) if expand((1 + I)**(2*n) - (1 - I)**(2*n)) == 0)
q("U02-A-021", "Algebra of complex numbers", "Least n with equal even powers", "Medium",
  "Inverse/parameter MCQ",
  r"The least positive integer $n$ such that $(1 + i)^{2n} = (1 - i)^{2n}$ is",
  r"$2$",
  [(r"$4$", "Solves $(1+i)^n = (1-i)^n$, ignoring the factor $2$ in the exponent."),
   (r"$1$", "Assumes $(1+i)^2 = (1-i)^2$ since both have modulus $2$."),
   (r"$8$", r"Writes the condition as $\left(\frac{1+i}{1-i}\right)^{2n} = 1$ but simplifies the ratio to $\frac{1+i}{\sqrt{2}}$, whose powers repeat every $8$, and ignores the factor $2$.")],
  r"$(1 + i)^2 = 2i$ and $(1 - i)^2 = -2i$, so the condition is $(2i)^n = (-2i)^n$, that is $(-1)^n = 1$. The least positive $n$ is $2$.",
  "Ignoring the factor $2$ in the exponent.",
  "U02-A-least-n-power-i", "Reduce both sides by squaring, then a parity argument.",
  check=_c21, values=[2, 4, 1, 8],
  numerical=dict(question=r"The least positive integer $n$ such that $(1 + i)^{2n} = (1 - i)^{2n}$ is", answer=2),
  cognitive="Application")

def _c22():
    e = expand(((1 + I)*X - 2*I)/(3 + I) + ((2 - 3*I)*Y + I)/(3 - I) - I)
    s = solve([re(e), im(e)], [X, Y])
    return s[X] + I*s[Y]
q("U02-A-022", "Algebra of complex numbers", "Equality with two quotients", "Medium",
  "Multi-step computation MCQ",
  r"If $x$ and $y$ are real and $\frac{(1 + i)x - 2i}{3 + i} + \frac{(2 - 3i)y + i}{3 - i} = i$, then $(x, y)$ is",
  r"$(3, -1)$",
  [(r"$(-1, 3)$", "Solves correctly but swaps the order of $x$ and $y$."),
   (r"$(3, 1)$", "Solves the system correctly but drops the sign of $y = -1$ at the end."),
   (r"$(-3, 1)$", "Solves the system correctly but drops the signs of both values at the end.")],
  r"Multiply by $(3 + i)(3 - i) = 10$: $(3 - i)[(1 + i)x - 2i] + (3 + i)[(2 - 3i)y + i] = 10i$. This expands to $(4x + 9y - 3) + i(2x - 7y - 3) = 10i$. So $4x + 9y = 3$ and $2x - 7y = 13$, giving $x = 3$, $y = -1$.",
  "Not clearing both denominators before equating parts.",
  "U02-A-equality-quotients", r"Clearing two complex denominators, then a $2 \times 2$ linear system.",
  check=_c22, values=[3 - I, -1 + 3*I, 3 + I, -3 + I], cognitive="Application")

_A, _B = symbols('a b', real=True, nonzero=True)
def _c23():
    a, b = _A, _B
    w = expand((a + I*b)**3)
    return simplify(re(w)/a + im(w)/b)
q("U02-A-023", "Algebra of complex numbers", "Equality after cubing a + ib", "Medium",
  "Multi-step computation MCQ",
  r"Let $a, b, x, y$ be real with $a \ne 0$, $b \ne 0$ and $x + iy = (a + ib)^3$. Then $\frac{x}{a} + \frac{y}{b}$ equals",
  r"$4(a^2 - b^2)$",
  [(r"$2(a^2 - b^2)$", "Expands the cube with coefficient $1$ instead of $3$ on the middle terms."),
   (r"$4(a^2 + b^2)$", "Sign slip, taking $i^2 = 1$ in the expansion."),
   (r"$-2(a^2 + b^2)$", r"Computes $\frac{x}{a} - \frac{y}{b}$.")],
  r"$(a + ib)^3 = a^3 + 3a^2(ib) + 3a(ib)^2 + (ib)^3 = (a^3 - 3ab^2) + i(3a^2b - b^3)$. So $\frac{x}{a} = a^2 - 3b^2$ and $\frac{y}{b} = 3a^2 - b^2$, whose sum is $4a^2 - 4b^2$.",
  "Mishandling $i^2$ and $i^3$ in a binomial expansion.",
  "U02-A-equality-cube", "Binomial expansion with powers of $i$, then equating parts.",
  check=_c23,
  values=[4*(_A**2 - _B**2), 2*(_A**2 - _B**2), 4*(_A**2 + _B**2), -2*(_A**2 + _B**2)],
  cognitive="Application")

def _c24():
    e = expand(conjugate((3 + 4*I)*(X + I*Y)) - (2 - 11*I))
    s = solve([re(e), im(e)], [X, Y])
    return s[X] + I*s[Y]
q("U02-A-024", "Algebra of complex numbers", "Conjugate of a product: solving for z", "Medium",
  "Multi-step computation MCQ",
  r"If $z$ is a complex number with $\overline{(3 + 4i)z} = 2 - 11i$, then $z$ equals",
  r"$2 + i$",
  [(r"$2 - i$", r"Finds $\overline{z} = 2 - i$ and stops."),
   (r"$\frac{-38 + 41i}{25}$", r"Writes the left side as $(3 + 4i)\overline{z}$, conjugating only $z$."),
   (r"$\frac{-38 - 41i}{25}$", "Ignores the bar and solves $(3 + 4i)z = 2 - 11i$.")],
  r"$\overline{(3 + 4i)z} = (3 - 4i)\overline{z}$, so $\overline{z} = \frac{2 - 11i}{3 - 4i} = \frac{(2 - 11i)(3 + 4i)}{25} = \frac{50 - 25i}{25} = 2 - i$. Hence $z = 2 + i$.",
  "Conjugating only one factor of a product.",
  "U02-A-conjugate-equation-linear", "Conjugate of a product, a division, then a final conjugation.",
  check=_c24, values=[2 + I, 2 - I, (-38 + 41*I)/25, (-38 - 41*I)/25], cognitive="Application")

def _c25():
    a, b, c, d = symbols('a b c d', real=True)
    z1, z2 = a + I*b, c + I*d
    p = expand(z1*conjugate(z1))
    s1 = (simplify(im(p)) == 0) and (simplify(re(p) - (a**2 + b**2)) == 0)
    s2 = simplify(re(expand(z1*z2)) - re(z1)*re(z2)) == 0
    return (bool(s1), bool(s2))
q("U02-A-025", "Algebra of complex numbers", "Properties of conjugate and real part", "Medium",
  "Statement-based MCQ",
  r"Statement I: For every complex number $z$, the number $z\overline{z}$ is real and non-negative. Statement II: For all complex numbers $z_1, z_2$, $\operatorname{Re}(z_1 z_2) = \operatorname{Re}(z_1)\operatorname{Re}(z_2)$." + STEM_TAIL,
  ST_TF,
  [(ST_TT, "Accepts the real-part product rule by analogy with the conjugate product rule."),
   (ST_FF, r"Doubts Statement I, perhaps thinking $z\overline{z}$ can carry an imaginary part."),
   (ST_FT, "Reverses the truth values of the two statements.")],
  r"With $z = a + ib$, $z\overline{z} = a^2 + b^2 \ge 0$, so Statement I is true. For Statement II, $\operatorname{Re}(z_1 z_2) = ac - bd$ when $z_1 = a + ib$, $z_2 = c + id$, which differs from $ac$ whenever $bd \ne 0$; for example $z_1 = z_2 = i$ gives $\operatorname{Re}(i^2) = -1 \ne 0$. So Statement II is false.",
  r"Assuming $\operatorname{Re}$ is multiplicative.",
  "U02-A-stmt-conjugate-re", "Needs one proof and one counterexample.",
  check=_c25, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Understanding")

def _c26():
    e = expand((1 + I)*(X + I*Y) - (1 - I)*(X - I*Y))
    return simplify(e/(2*I))
q("U02-A-026", "Algebra of complex numbers", "Equation involving z and its conjugate", "Medium",
  "Multi-step computation MCQ",
  r"Let $z = x + iy$, with $x, y$ real and $z \ne 0$, satisfy $(1 + i)z = (1 - i)\overline{z}$. Then",
  r"$x + y = 0$",
  [(r"$x - y = 0$", r"Takes $\overline{z} = -x + iy$, negating the real part, which leads to $x - y = y - x$."),
   (r"$x = 0$", "Concludes that $z$ must be purely imaginary because the two coefficients are conjugates."),
   (r"$y = 0$", "Concludes that $z$ must be real by comparing the two sides as conjugates.")],
  r"$(1 + i)(x + iy) = (x - y) + i(x + y)$ and $(1 - i)(x - iy) = (x - y) - i(x + y)$. Equating, $2i(x + y) = 0$, so $x + y = 0$.",
  "Deciding the nature of $z$ by symmetry without expanding.",
  "U02-A-conjugate-equation-relation", "Two expansions and comparison of parts.",
  check=_c26, values=[X + Y, X - Y, X, Y], cognitive="Analysis")

def _c27():
    t = symbols('theta', real=True)
    w = (3 + 2*I*sin(t))/(1 - 2*I*sin(t))
    sols = solveset(simplify(re(expand_complex(w))), t, Interval.open(0, pi))
    return FiniteSet(*[s for s in sols if simplify(im(expand_complex(w)).subs(t, s)) != 0])
q("U02-A-027", "Algebra of complex numbers", "Parameter making a quotient purely imaginary", "Medium",
  "Inverse/parameter MCQ",
  r"The set of all $\theta \in (0, \pi)$ for which $\frac{3 + 2i\sin\theta}{1 - 2i\sin\theta}$ is purely imaginary is",
  r"$\left\{\frac{\pi}{3}, \frac{2\pi}{3}\right\}$",
  [(r"$\left\{\frac{\pi}{6}, \frac{5\pi}{6}\right\}$", r"Writes the real part as $3 - 12\sin^2\theta$, getting $\sin\theta = \frac{1}{2}$."),
   (r"$\left\{\frac{\pi}{3}\right\}$", r"Solves $\sin\theta = \frac{\sqrt{3}}{2}$ but keeps only the acute angle."),
   (r"$\left\{\frac{\pi}{4}, \frac{3\pi}{4}\right\}$", r"Writes the real part as $3 - 6\sin^2\theta$, getting $\sin^2\theta = \frac{1}{2}$.")],
  r"Multiply by $1 + 2i\sin\theta$: the numerator becomes $3 + 6i\sin\theta + 2i\sin\theta - 4\sin^2\theta = (3 - 4\sin^2\theta) + 8i\sin\theta$. Purely imaginary needs $\sin^2\theta = \frac{3}{4}$, and then $8\sin\theta \ne 0$. In $(0, \pi)$ this gives $\theta = \frac{\pi}{3}, \frac{2\pi}{3}$.",
  "Dropping the obtuse solution of a sine equation.",
  "U02-A-param-purely-imag-trig", "Rationalisation, a trigonometric equation and an interval restriction.",
  check=_c27,
  values=[FiniteSet(pi/3, 2*pi/3), FiniteSet(pi/6, 5*pi/6), FiniteSet(pi/3), FiniteSet(pi/4, 3*pi/4)],
  cognitive="Application")

def _c28():
    a = symbols('a', real=True)
    w = expand((a + 3*I)*(2 - a*I))  # numerator after multiplying by conjugate of 2 + ai
    return FiniteSet(*solve(im(w), a))
q("U02-A-028", "Algebra of complex numbers", "Parameter making a quotient purely real", "Medium",
  "Inverse/parameter MCQ",
  r"The set of all real $a$ for which $\frac{a + 3i}{2 + ai}$ is purely real is",
  r"$\{-\sqrt{6}, \sqrt{6}\}$",
  [(r"$\{0\}$", "Sets the real part $5a$ to zero, which is the purely imaginary condition."),
   (r"$\{\sqrt{6}\}$", "Solves $a^2 = 6$ but keeps only the positive root."),
   (r"$\{-6, 6\}$", r"Solves $a^2 = 6$ as $a = \pm 6$.")],
  r"$\frac{a + 3i}{2 + ai} = \frac{(a + 3i)(2 - ai)}{4 + a^2} = \frac{5a + (6 - a^2)i}{4 + a^2}$. It is purely real when $a^2 = 6$, so $a = \pm\sqrt{6}$.",
  "Confusing the purely real and purely imaginary conditions.",
  "U02-A-param-purely-real", "Rationalisation with a parameter in the denominator, then a quadratic condition.",
  check=_c28, values=[FiniteSet(-sqrt(6), sqrt(6)), FiniteSet(0), FiniteSet(sqrt(6)), FiniteSet(-6, 6)],
  cognitive="Application")

def _c29():
    w = expand(1/((1 + 2*I)/(1 - I)))
    return re(w) + im(w)
q("U02-A-029", "Algebra of complex numbers", "Inverse of a quotient", "Medium",
  "Multi-step computation MCQ",
  r"If $z = \frac{1 + 2i}{1 - i}$, then $\operatorname{Re}(z^{-1}) + \operatorname{Im}(z^{-1})$ equals",
  r"$-\frac{4}{5}$",
  [(r"$\frac{2}{5}$", r"Takes $z^{-1} = \frac{z}{|z|^2}$, omitting the conjugate."),
   (r"$-\frac{2}{5}$", "Divides by $1^2 + 3^2 = 10$ but forgets the factor $2$ in the numerator."),
   (r"$\frac{4}{5}$", "Sign slip in both parts of $z^{-1}$.")],
  r"$z^{-1} = \frac{1 - i}{1 + 2i} = \frac{(1 - i)(1 - 2i)}{5} = \frac{1 - 2i - i - 2}{5} = \frac{-1 - 3i}{5}$. So the required sum is $-\frac{1}{5} - \frac{3}{5} = -\frac{4}{5}$.",
  "Forgetting the conjugate in the inverse formula.",
  "U02-A-inverse-quotient", "Invert the quotient directly, rationalise, then combine parts.",
  check=_c29, values=[Rational(-4, 5), Rational(2, 5), Rational(-2, 5), Rational(4, 5)], cognitive="Application")

def _c30():
    e = expand((X + I*Y)*(2 + I) - (1 + 3*I))
    s = solve([re(e), im(e)], [X, Y])
    return s[X] + I*s[Y]
q("U02-A-030", "Algebra of complex numbers", "Ordered pairs: division", "Medium",
  "Multi-step computation MCQ",
  r"Treating complex numbers as ordered pairs of reals, if $(x, y) \cdot (2, 1) = (1, 3)$, then $(x, y)$ equals",
  r"$(1, 1)$",
  [(r"$\left(\frac{1}{2}, 3\right)$", "Divides component by component."),
   (r"$\left(-\frac{1}{5}, \frac{7}{5}\right)$", "Multiplies $(1, 3)$ by $(2, 1)$ and divides by $5$, instead of multiplying by the inverse."),
   (r"$(5, 5)$", "Multiplies by the conjugate $(2, -1)$ but forgets to divide by $2^2 + 1^2$.")],
  r"The equation is $(x + iy)(2 + i) = 1 + 3i$, so $x + iy = \frac{1 + 3i}{2 + i} = \frac{(1 + 3i)(2 - i)}{5} = \frac{5 + 5i}{5} = 1 + i$. Hence $(x, y) = (1, 1)$; check: $(2 - 1, 1 + 2) = (1, 3)$.",
  "Dividing ordered pairs componentwise.",
  "U02-A-ordered-pair-division", "Translate to $a + ib$, divide, translate back.",
  check=_c30, values=[1 + I, Rational(1, 2) + 3*I, Rational(-1, 5) + Rational(7, 5)*I, 5 + 5*I],
  cognitive="Application")

def _c31():
    p = expand((1 + 2*I)*(3 + 4*I))
    s1 = (p == 3 + 8*I)
    s2 = (expand(1/(2 + 0*I)) == Rational(1, 2))
    return (bool(s1), bool(s2))
q("U02-A-031", "Algebra of complex numbers", "Ordered-pair product and inverse", "Medium",
  "Statement-based MCQ",
  r"Complex numbers are treated as ordered pairs of reals. Statement I: $(1, 2) \cdot (3, 4) = (3, 8)$. Statement II: The multiplicative inverse of $(2, 0)$ is $\left(\frac{1}{2}, 0\right)$." + STEM_TAIL,
  ST_FT,
  [(ST_TT, "Accepts the componentwise product in Statement I."),
   (ST_FF, "Thinks the inverse of $(2, 0)$ must have a non-zero second component."),
   (ST_TF, "Reverses the truth values of the two statements.")],
  r"$(1, 2)(3, 4) = (3 - 8, 4 + 6) = (-5, 10)$, so Statement I is false. The inverse of $(a, b)$ is $\left(\frac{a}{a^2+b^2}, \frac{-b}{a^2+b^2}\right)$, which for $(2, 0)$ is $\left(\frac{1}{2}, 0\right)$, so Statement II is true.",
  "Multiplying ordered pairs componentwise.",
  "U02-A-stmt-ordered-pair", "Two short computations under the ordered-pair rules.",
  check=_c31, values=[(False, True), (True, True), (False, False), (True, False)],
  cognitive="Understanding")

def _c32():
    r = [s for s in sqrts(7 - 24*I) if re(s) > 0][0]
    return re(r) - im(r)
q("U02-A-032", "Algebra of complex numbers", "Square root with sign condition", "Medium",
  "Multi-step computation MCQ",
  r"If $a + ib$ ($a, b$ real, $a > 0$) is a square root of $7 - 24i$, then $a - b$ equals",
  r"$7$",
  [(r"$1$", "Takes $b = 3$ instead of $b = -3$, ignoring that $ab$ must be negative."),
   (r"$5$", "Reports the modulus of the square root."),
   (r"$-7$", "Uses the other root $-4 + 3i$, ignoring the condition $a > 0$.")],
  r"Let $(a + ib)^2 = 7 - 24i$. Then $a^2 - b^2 = 7$, $a^2 + b^2 = 25$ and $2ab = -24$. So $a^2 = 16$, $b^2 = 9$, and with $a > 0$, $ab < 0$ we get $a = 4$, $b = -3$. Hence $a - b = 7$.",
  r"Ignoring the sign of $ab$.",
  "U02-A-sqrt-sign-condition", "Three equations plus two sign conditions.",
  check=_c32, values=[7, 1, 5, -7],
  numerical=dict(question=r"If $a + ib$ ($a, b$ real, $a > 0$) is a square root of $7 - 24i$, then the value of $a - b$ is", answer=7),
  cognitive="Application")

q("U02-A-033", "Algebra of complex numbers", "Square roots of a quotient", "Medium",
  "Multi-step computation MCQ",
  r"The square roots of $\frac{1 + i}{1 - i}$ are",
  r"$\pm\frac{1 + i}{\sqrt{2}}$",
  [(r"$\pm\frac{1 - i}{\sqrt{2}}$", "Takes the quotient to be $-i$."),
   (r"$\pm\frac{1 + i}{2}$", r"Uses $x^2 + y^2 = \frac{1}{2}$ instead of $1$."),
   (r"$\pm(1 + i)$", r"Simplifies the quotient as $(1 + i)^2 = 2i$, forgetting to divide by $(1 - i)(1 + i) = 2$; the square roots of $2i$ are $\pm(1 + i)$.")],
  r"$\frac{1 + i}{1 - i} = \frac{(1 + i)^2}{2} = i$. If $(x + iy)^2 = i$, then $x^2 - y^2 = 0$ and $2xy = 1$, so $x = y = \pm\frac{1}{\sqrt{2}}$. The roots are $\pm\frac{1 + i}{\sqrt{2}}$.",
  "Not simplifying the quotient before taking roots.",
  "U02-A-sqrt-of-quotient", "Simplify a quotient to $i$, then extract a square root.",
  check=lambda: sqrts(simplify((1 + I)/(1 - I))),
  values=[FiniteSet((1 + I)/sqrt(2), -(1 + I)/sqrt(2)), FiniteSet((1 - I)/sqrt(2), -(1 - I)/sqrt(2)),
          FiniteSet((1 + I)/2, -(1 + I)/2), FiniteSet(1 + I, -1 - I)],
  cognitive="Application")

def _c34():
    a = X**2 - Y**2; b = 2*X*Y  # (x + iy)^2 = a + ib
    cands = [X - I*Y, Y + I*X, Y - I*X, X + I*Y]
    good = [c for c in cands if expand(c**2 - (a - I*b)) == 0]
    return good[0] if len(good) == 1 else None
q("U02-A-034", "Algebra of complex numbers", "Square root of the conjugate", "Medium",
  "Conceptual/application MCQ",
  r"Let $a, b, x, y$ be real with $a \ne 0$, $b \ne 0$, and $(x + iy)^2 = a + ib$. Which of the following is a square root of $a - ib$?",
  r"$x - iy$",
  [(r"$y + ix$", "Swaps the parts; its square is $-a + ib$."),
   (r"$y - ix$", "Swaps the parts and conjugates; its square is $-a - ib$."),
   (r"$x + iy$", "Assumes the square root is unchanged when the imaginary part changes sign.")],
  r"Taking conjugates of $(x + iy)^2 = a + ib$ gives $(x - iy)^2 = a - ib$. Directly, $(x - iy)^2 = x^2 - y^2 - 2ixy = a - ib$. For the other expressions, $(y + ix)^2 = -a + ib$, $(y - ix)^2 = -a - ib$ and $(x + iy)^2 = a + ib$, none equal to $a - ib$ since $a, b \ne 0$.",
  "Swapping real and imaginary parts when conjugating.",
  "U02-A-sqrt-conjugate", "Uses $\\overline{w^2} = \\overline{w}^2$ and rules out three look-alike options.",
  check=_c34, values=[X - I*Y, Y + I*X, Y - I*X, X + I*Y], cognitive="Understanding")

q("U02-A-035", "Algebra of complex numbers", "Counting solutions of z squared equals conjugate", "Medium",
  "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying $z^2 = \overline{z}$ is",
  r"$4$",
  [(r"$3$", "Divides by $z$ and loses the solution $z = 0$."),
   (r"$2$", "Finds only the real solutions $0$ and $1$."),
   (r"$1$", "Finds only $z = 1$ by inspection.")],
  r"With $z = x + iy$: $x^2 - y^2 = x$ and $2xy = -y$. If $y = 0$, then $x^2 = x$, giving $z = 0, 1$. If $y \ne 0$, then $x = -\frac{1}{2}$ and $y^2 = \frac{1}{4} + \frac{1}{2} = \frac{3}{4}$, giving $z = -\frac{1}{2} \pm \frac{\sqrt{3}}{2}i$. In all there are 4 solutions.",
  "Cancelling a factor that can be zero.",
  "U02-A-count-z2-conj", "Casework from the imaginary-part equation.",
  check=lambda: len(zsols(lambda z: z**2 - conjugate(z))), values=[4, 3, 2, 1],
  numerical=dict(question=r"The number of complex numbers $z$ satisfying $z^2 = \overline{z}$ is", answer=4),
  cognitive="Analysis")

q("U02-A-036", "Algebra of complex numbers", "Equation z + |z| = a + ib", "Medium",
  "Multi-step computation MCQ",
  r"If $z$ is a complex number such that $z + |z| = 2 + 8i$, then $|z|$ equals",
  r"$17$",
  [(r"$15$", r"Reports $|\operatorname{Re}(z)|$, where $\operatorname{Re}(z) = -15$."),
   (r"$8$", r"Reports $\operatorname{Im}(z)$."),
   (r"$2\sqrt{17}$", "Takes $z = 2 + 8i$, ignoring the $|z|$ term.")],
  r"Let $z = x + iy$. Then $y = 8$ and $x + \sqrt{x^2 + 64} = 2$. So $\sqrt{x^2 + 64} = 2 - x$, giving $x^2 + 64 = 4 - 4x + x^2$, so $x = -15$ (and $2 - x = 17 > 0$). Hence $|z| = \sqrt{225 + 64} = 17$.",
  "Treating $|z|$ as if it changed the imaginary part.",
  "U02-A-z-plus-mod", "Equating parts, then a radical equation.",
  check=lambda: Abs(zsols(lambda z: z + Abs(z) - 2 - 8*I)[0]), values=[17, 15, 8, 2*sqrt(17)],
  numerical=dict(question=r"If $z$ is a complex number such that $z + |z| = 2 + 8i$, then the value of $|z|$ is", answer=17),
  cognitive="Application")

q("U02-A-037", "Algebra of complex numbers", "Counting solutions of z squared plus |z| = 0", "Medium",
  "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying $z^2 + |z| = 0$ is",
  r"$3$",
  [(r"$1$", "Finds only $z = 0$."),
   (r"$2$", r"Finds $z = \pm i$ but misses $z = 0$."),
   (r"$5$", r"Also accepts $x = \pm 1$ from the real case by solving $x^2 = |x|$ instead of $x^2 = -|x|$.")],
  r"Let $z = x + iy$. Then $x^2 - y^2 + \sqrt{x^2 + y^2} = 0$ and $2xy = 0$. If $y = 0$: $x^2 + |x| = 0$, so $x = 0$. If $x = 0$: $-y^2 + |y| = 0$, so $y = 0$ or $|y| = 1$. The solutions are $0, i, -i$, so there are 3.",
  "Missing $z = 0$ or the negative of a solution.",
  "U02-A-count-z2-mod", "Casework on the imaginary part with an absolute-value equation in each case.",
  check=lambda: len(zsols(lambda z: z**2 + Abs(z))), values=[3, 1, 2, 5],
  numerical=dict(question=r"The number of complex numbers $z$ satisfying $z^2 + |z| = 0$ is", answer=3),
  cognitive="Analysis")

q("U02-A-038", "Algebra of complex numbers", "Equation |z| - z = a + ib", "Medium",
  "Multi-step computation MCQ",
  r"If $z$ is a complex number such that $|z| - z = 1 + 2i$, then $z$ equals",
  r"$\frac{3}{2} - 2i$",
  [(r"$\frac{3}{2} + 2i$", "Equates the imaginary parts as $y = 2$, missing the minus sign on $z$."),
   (r"$-\frac{3}{2} - 2i$", "Sign slip when solving $x^2 + 4 = (1 + x)^2$, writing $3 = -2x$."),
   (r"$3 - 2i$", "Expands $(1 + x)^2$ as $1 + x + x^2$.")],
  r"Let $z = x + iy$. Then $\sqrt{x^2 + y^2} - x = 1$ and $-y = 2$, so $y = -2$. Now $\sqrt{x^2 + 4} = 1 + x$ gives $x^2 + 4 = 1 + 2x + x^2$, so $x = \frac{3}{2}$ (and $1 + x > 0$). Hence $z = \frac{3}{2} - 2i$.",
  "Sign errors when $z$ is subtracted.",
  "U02-A-z-plus-mod", "Equating parts with a sign twist, then a radical equation.",
  check=lambda: zsols(lambda z: Abs(z) - z - 1 - 2*I)[0],
  values=[Rational(3, 2) - 2*I, Rational(3, 2) + 2*I, Rational(-3, 2) - 2*I, 3 - 2*I], cognitive="Application")

q("U02-A-039", "Algebra of complex numbers", "Linear equation in z and its conjugate", "Medium",
  "Multi-step computation MCQ",
  r"If $z$ is a complex number such that $3z + 2i\overline{z} = 5 + 5i$, then $z$ equals",
  r"$1 + i$",
  [(r"$\frac{25 + 5i}{13}$", r"Replaces $\overline{z}$ by $z$ and solves $(3 + 2i)z = 5 + 5i$."),
   (r"$1 - i$", r"Solves correctly for $z$, then reports $\overline{z}$."),
   (r"$\frac{5 + 25i}{13}$", "Treats the equation as $(3 - 2i)z = 5 + 5i$.")],
  r"With $z = x + iy$: $3x + 3iy + 2i(x - iy) = (3x + 2y) + i(2x + 3y)$. So $3x + 2y = 5$ and $2x + 3y = 5$, giving $x = y = 1$ and $z = 1 + i$.",
  r"Treating $\overline{z}$ as $z$.",
  "U02-A-conjugate-equation-linear", "Substitution $z = x + iy$, then a linear system.",
  check=lambda: zsols(lambda z: 3*z + 2*I*conjugate(z) - 5 - 5*I)[0],
  values=[1 + I, (25 + 5*I)/13, 1 - I, (5 + 25*I)/13], cognitive="Application")

q("U02-A-040", "Algebra of complex numbers", "Product of consecutive powers of i", "Medium",
  "Multi-step computation MCQ",
  r"The value of $i \cdot i^2 \cdot i^3 \cdots i^{100}$ is",
  r"$-1$",
  [(r"$1$", "Notes that the exponent $5050$ is even and concludes the value is $1$."),
   (r"$i$", r"Reduces $5050 \bmod 4$ incorrectly as $1$."),
   (r"$-i$", r"Reduces $5050 \bmod 4$ incorrectly as $3$.")],
  r"The product is $i^{1 + 2 + \dots + 100} = i^{5050}$. Since $5050 = 4 \cdot 1262 + 2$, the value is $i^2 = -1$.",
  "Thinking every even power of $i$ equals $1$.",
  "U02-A-product-powers-i", "Sum of an arithmetic series, then reduction modulo $4$.",
  check=lambda: simplify(prod([I**k for k in range(1, 101)])), values=[-1, 1, I, -I], cognitive="Application")

q("U02-A-041", "Algebra of complex numbers", "Number from its multiplicative inverse", "Medium",
  "Inverse/parameter MCQ",
  r"If the multiplicative inverse of a complex number $z$ is $\frac{\sqrt{3} + 4i}{19}$, then $z$ equals",
  r"$\sqrt{3} - 4i$",
  [(r"$\sqrt{3} + 4i$", r"Thinks the inverse of $z$ is $\frac{z}{|z|^2}$, so drops the conjugate."),
   (r"$\frac{\sqrt{3} - 4i}{19}$", "Conjugates the given inverse without inverting it."),
   (r"$-\sqrt{3} + 4i$", r"Rationalises correctly but negates the whole result, $-(\sqrt{3} - 4i)$.")],
  r"$z = \frac{19}{\sqrt{3} + 4i} = \frac{19(\sqrt{3} - 4i)}{3 + 16} = \sqrt{3} - 4i$.",
  "Confusing the inverse with the conjugate.",
  "U02-A-inverse-reverse", "Inverting the inverse with a surd in the real part.",
  check=lambda: expand(1/((sqrt(3) + 4*I)/19)),
  values=[sqrt(3) - 4*I, sqrt(3) + 4*I, (sqrt(3) - 4*I)/19, -sqrt(3) + 4*I], cognitive="Application")

def _c42():
    k = symbols('k', real=True)
    return FiniteSet(*[s for s in solve(im(expand((1 + k*I)**3)), k) if s != 0])
q("U02-A-042", "Algebra of complex numbers", "Parameter making a cube purely real", "Medium",
  "Inverse/parameter MCQ",
  r"The set of all non-zero real $k$ for which $(1 + ki)^3$ is purely real is",
  r"$\{-\sqrt{3}, \sqrt{3}\}$",
  [(r"$\left\{-\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}\right\}$", "Sets the real part $1 - 3k^2$ to zero, the purely imaginary condition."),
   (r"$\{-3, 3\}$", r"Solves $k^2 = 3$ as $k = \pm 3$."),
   (r"$\{\sqrt{3}\}$", "Keeps only the positive root of $k^2 = 3$.")],
  r"$(1 + ki)^3 = 1 + 3ki - 3k^2 - k^3 i = (1 - 3k^2) + i(3k - k^3)$. It is purely real when $k(3 - k^2) = 0$; with $k \ne 0$ this gives $k = \pm\sqrt{3}$.",
  "Confusing purely real with purely imaginary.",
  "U02-A-param-power-real", "Binomial expansion with powers of $i$, then a factorised condition.",
  check=_c42, values=[FiniteSet(-sqrt(3), sqrt(3)), FiniteSet(-1/sqrt(3), 1/sqrt(3)), FiniteSet(-3, 3), FiniteSet(sqrt(3))],
  cognitive="Application")

# ================================================================ DIFFICULT (13)

def _c43():
    nz = [s for s in zsols(lambda z: conjugate(z) - I*z**2) if s != 0]
    return simplify(prod(nz))
q("U02-A-043", "Algebra of complex numbers", "Conjugate equation with casework: product of solutions", "Difficult",
  "Multi-step computation MCQ",
  r"The product of all non-zero complex numbers $z$ satisfying $\overline{z} = iz^2$ is",
  r"$-i$",
  [(r"$-1$", "Misses the solution $z = i$ from the case $x = 0$, so the product is $-1$."),
   (r"$i$", "Sign slip in the case $x = 0$, taking $z = -i$ instead of $z = i$."),
   (r"$0$", "Includes $z = 0$ in the product.")],
  r"Let $z = x + iy$. Then $iz^2 = -2xy + i(x^2 - y^2)$, so $x = -2xy$ and $-y = x^2 - y^2$. If $x = 0$: $y^2 = y$, giving $z = 0$ or $z = i$. If $x \ne 0$: $y = -\frac{1}{2}$ and $x^2 = \frac{3}{4}$, giving $z = \pm\frac{\sqrt{3}}{2} - \frac{i}{2}$. The non-zero solutions are $i$ and $\pm\frac{\sqrt{3}}{2} - \frac{i}{2}$; their product is $i\left(-\frac{i}{2} + \frac{\sqrt{3}}{2}\right)\left(-\frac{i}{2} - \frac{\sqrt{3}}{2}\right) = i\left(-\frac{1}{4} - \frac{3}{4}\right) = -i$.",
  "Missing one branch of the casework.",
  "U02-A-conj-equation-casework", "Two cases from the real-part equation, each with its own solutions, then a product.",
  check=_c43, values=[-I, -1, I, 0], cognitive="Analysis")

q("U02-A-044", "Algebra of complex numbers", "Counting solutions with modulus", "Difficult",
  "Multi-step computation MCQ",
  r"The number of complex numbers $z$ satisfying $z^2 - 2|z| + 1 = 0$ is",
  r"$4$",
  [(r"$2$", r"Finds only the real solutions $z = \pm 1$."),
   (r"$6$", r"Also accepts $|y| = -1 - \sqrt{2}$, which is negative."),
   (r"$3$", r"Finds $\pm 1$ but takes only $y = \sqrt{2} - 1$ in the imaginary case.")],
  r"Let $z = x + iy$. The imaginary part gives $2xy = 0$. If $y = 0$: $x^2 - 2|x| + 1 = 0$, so $(|x| - 1)^2 = 0$ and $x = \pm 1$. If $x = 0$: $-y^2 - 2|y| + 1 = 0$, so $|y| = -1 + \sqrt{2}$ (the other root is negative), giving $y = \pm(\sqrt{2} - 1)$. The point $z = 0$ fails. Total: 4.",
  "Ignoring the purely imaginary branch.",
  "U02-A-count-z2-mod", "Casework with a quadratic in $|x|$ and in $|y|$, rejecting a negative root.",
  check=lambda: len(zsols(lambda z: z**2 - 2*Abs(z) + 1)), values=[4, 2, 6, 3],
  numerical=dict(question=r"The number of complex numbers $z$ satisfying $z^2 - 2|z| + 1 = 0$ is", answer=4),
  cognitive="Analysis")

def _c45():
    a, b = symbols('a b', real=True)
    w = (a + I)/(b + 2*I)
    num = expand((a + I)*(b - 2*I))
    sols = solve([re(num), 4*(a**2 + 1) - (b**2 + 4)], [a, b], dict=True)
    good = [s for s in sols if simplify(im(num).subs(s)) != 0]
    return len(good)
q("U02-A-045", "Algebra of complex numbers", "Purely imaginary quotient with a modulus condition", "Difficult",
  "Inverse/parameter MCQ",
  r"The number of ordered pairs $(a, b)$ of real numbers for which $z = \frac{a + i}{b + 2i}$ is purely imaginary (that is, $\operatorname{Re}(z) = 0$ and $z \ne 0$) and $|z| = \frac{1}{2}$ is",
  r"$2$",
  [(r"$4$", r"Takes $b = \pm 2a$ with $a = \pm 1$ without checking $ab = -2$."),
   (r"$1$", r"Keeps only $a > 0$, taking $a = \sqrt{1}$ as positive only."),
   (r"$0$", "Takes $b = 2a$ only (positive square root) and then finds $ab = -2$ impossible.")],
  r"$z = \frac{(a + i)(b - 2i)}{b^2 + 4} = \frac{(ab + 2) + i(b - 2a)}{b^2 + 4}$. Purely imaginary needs $ab = -2$. Next $|z| = \frac{\sqrt{a^2 + 1}}{\sqrt{b^2 + 4}} = \frac{1}{2}$ gives $b^2 = 4a^2$, so $b = \pm 2a$; with $ab = -2$ only $b = -2a$, $a^2 = 1$ works. So $(a, b) = (1, -2)$ or $(-1, 2)$, and in both $b - 2a \ne 0$. There are 2 pairs.",
  r"Not combining the sign information from $ab = -2$ with $b = \pm 2a$.",
  "U02-A-param-imag-modulus", "Two conditions, each producing an equation, with a sign check.",
  check=_c45, values=[2, 4, 1, 0],
  numerical=dict(question=r"The number of ordered pairs $(a, b)$ of real numbers for which $z = \frac{a + i}{b + 2i}$ is purely imaginary (that is, $\operatorname{Re}(z) = 0$ and $z \ne 0$) and $|z| = \frac{1}{2}$ is", answer=2),
  cognitive="Analysis")

q("U02-A-046", "Algebra of complex numbers", "Equation with z squared and |z| squared", "Difficult",
  "Multi-step computation MCQ",
  r"The set of all complex numbers $z$ satisfying $z^2 + |z|^2 = 2 + 2i$ is",
  r"$\{1 + i,\ -1 - i\}$",
  [(r"$\{1 + i\}$", "Solves $x^2 = 1$ taking only $x = 1$."),
   (r"$\{1 + i,\ 1 - i\}$", r"Takes $x = 1$ and then $y = \pm 1$ from $y^2 = 1$, ignoring the sign of $xy$."),
   (r"$\{1 + i,\ -1 - i,\ 1 - i,\ -1 + i\}$", "Solves $x^2 = 1$ and $y^2 = 1$ independently, ignoring $xy = 1$.")],
  r"With $z = x + iy$: $z^2 + |z|^2 = (x^2 - y^2 + x^2 + y^2) + 2ixy = 2x^2 + 2ixy$. So $x^2 = 1$ and $xy = 1$, giving $(x, y) = (1, 1)$ or $(-1, -1)$. The set is $\{1 + i, -1 - i\}$.",
  "Pairing values of $x$ and $y$ without using the condition $xy = 1$.",
  "U02-A-z2-plus-mod2", "Cancellation of $y^2$ is non-obvious; then paired sign conditions.",
  check=lambda: FiniteSet(*zsols(lambda z: z**2 + Abs(z)**2 - 2 - 2*I)),
  values=[FiniteSet(1 + I, -1 - I), FiniteSet(1 + I), FiniteSet(1 + I, 1 - I), FiniteSet(1 + I, -1 - I, 1 - I, -1 + I)],
  cognitive="Analysis")

def _c47():
    cnt = 0
    for n in range(1, 101):
        if im(expand(sum(I**k for k in range(1, n + 1)))) == 0:
            cnt += 1
    return cnt
q("U02-A-047", "Algebra of complex numbers", "Counting n for which a sum of powers of i is real", "Difficult",
  "Multi-step computation MCQ",
  r"For a positive integer $n$, let $S_n = i + i^2 + \dots + i^n$. The number of $n \in \{1, 2, \dots, 100\}$ for which $S_n$ is a real number is",
  r"$50$",
  [(r"$25$", "Counts only $n$ with $S_n = -1$, forgetting that $S_n = 0$ is also real."),
   (r"$75$", "Treats $S_n = -1 + i$ as real as well."),
   (r"$49$", "Counts the multiples of $4$ as $24$, missing $n = 100$, so $25 + 24$.")],
  r"$S_n$ depends on $n \bmod 4$: remainders 1, 2, 3, 0 give $i$, $-1 + i$, $-1$, $0$. It is real for remainders 3 and 0. Each remainder occurs 25 times in $1, \dots, 100$, so the count is $50$.",
  "Forgetting that $0$ is a real number.",
  "U02-A-sum-powers-i-count", "Classify the four partial sums, then count residues; trap with $0$ being real.",
  check=_c47, values=[50, 25, 75, 49],
  numerical=dict(question=r"For a positive integer $n$, let $S_n = i + i^2 + \dots + i^n$. The number of $n \in \{1, 2, \dots, 100\}$ for which $S_n$ is a real number is", answer=50),
  cognitive="Analysis")

def _c48():
    c, d = symbols('c d', real=True)
    z2 = c + I*d
    # Statement I: z1^2 + z2^2 = 0 forces z1 = +-i z2; test whether z1*conj(z2) is then real
    s1 = True
    for z1 in (I*z2, -I*z2):
        assert expand(z1**2 + z2**2) == 0
        if simplify(im(expand(z1*conjugate(z2)))) != 0:
            s1 = False
    # Statement II: z^2 real means z real or purely imaginary; look for a non-real z = iy
    y = symbols('y', real=True, nonzero=True)
    zz = I*y
    ys = solve(simplify(im(expand_complex(zz + 1/zz))), y)
    s2 = not any(im(expand(zz.subs(y, v)**2)) == 0 for v in ys)
    return (bool(s1), bool(s2))
q("U02-A-048", "Algebra of complex numbers", "Real-number habits that fail in C", "Difficult",
  "Statement-based MCQ",
  r"Statement I: If $z_1, z_2$ are non-zero complex numbers with $z_1^2 + z_2^2 = 0$, then $z_1\overline{z_2}$ is real. Statement II: If $z$ is a non-zero complex number such that both $z^2$ and $z + \frac{1}{z}$ are real, then $z$ is real." + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Treats $z_1\overline{z_2}$ like a product of reals, and in Statement II tests only real $z$, missing $z = \pm i$."),
   (ST_TF, r"Assumes $\frac{z_1}{z_2}$ is real in Statement I, but finds the counterexample $z = i$ in Statement II."),
   (ST_FT, r"Finds $z_1 = \pm i z_2$ in Statement I, but in Statement II checks $z = iy$ and wrongly concludes $y - \frac{1}{y} \ne 0$.")],
  r"From $z_1^2 = -z_2^2$ we get $z_1 = \pm iz_2$, so $z_1\overline{z_2} = \pm i|z_2|^2$, which is non-zero and purely imaginary; Statement I is false. In Statement II, $z^2$ real forces $z$ real or purely imaginary. For $z = iy$ ($y \ne 0$), $z + \frac{1}{z} = i\left(y - \frac{1}{y}\right)$ is real when $y = \pm 1$. So $z = i$ satisfies both conditions and is not real; Statement II is false.",
  r"Carrying real-number facts about squares into $\mathbb{C}$.",
  "U02-A-stmt-squares-in-C", r"Statement I needs $z_1 = \pm iz_2$ and a conjugate product; Statement II needs casework on $z^2$ real plus a second condition with a hidden solution $z = \pm i$.",
  check=_c48, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Analysis")

def _c49():
    sols = zsols(lambda z: z**2 - conjugate(z))
    s1 = all(simplify(Abs(s) - 1) == 0 for s in sols if s != 0)
    t = symbols('t', real=True)
    s2 = simplify((I*t)**2 + Abs(I*t)**2) == 0   # every purely imaginary z works
    return (bool(s1), bool(s2))
q("U02-A-049", "Algebra of complex numbers", "Properties of solution sets of conjugate and modulus equations", "Difficult",
  "Statement-based MCQ",
  r"Statement I: If $z \ne 0$ and $z^2 = \overline{z}$, then $|z| = 1$. Statement II: The equation $z^2 + |z|^2 = 0$ has infinitely many solutions in $\mathbb{C}$." + STEM_TAIL,
  ST_TT,
  [(ST_FF, "Thinks Statement I fails for the non-real solutions and that Statement II has only $z = 0$."),
   (ST_TF, "Believes $z^2 + |z|^2 = 0$ forces $z = 0$, as for real numbers."),
   (ST_FT, r"Doubts that the non-real solutions of $z^2 = \overline{z}$ have modulus $1$.")],
  r"Taking moduli in $z^2 = \overline{z}$ gives $|z|^2 = |z|$, so $|z| = 1$ when $z \ne 0$; Statement I is true. For $z = x + iy$, $z^2 + |z|^2 = 2x^2 + 2ixy$, which is $0$ whenever $x = 0$. Every purely imaginary $z$ is a solution, so Statement II is true.",
  "Assuming a sum involving squares vanishes only at $0$.",
  "U02-A-stmt-conj-mod-equations", "Two independent arguments, one via moduli and one via an infinite family.",
  check=_c49, values=[(True, True), (False, False), (True, False), (False, True)],
  cognitive="Analysis")

def _c50():
    a, b = symbols('a b', real=True)
    r2 = a**2 + b**2
    sols = solve([a - b*r2, -b - a*r2], [a, b], dict=True)  # (a,b)^{-1} = (b,a), cleared of r2
    return len([s for s in sols if not (s[a] == 0 and s[b] == 0)])
q("U02-A-050", "Algebra of complex numbers", "Ordered pairs: inverse equal to swapped pair", "Difficult",
  "Conceptual/application MCQ",
  r"Complex numbers are treated as ordered pairs of reals. The number of ordered pairs $(a, b) \ne (0, 0)$ whose multiplicative inverse is $(b, a)$ is",
  r"zero",
  [(r"two", r"Solves only $a = b$ with $a^2 + b^2 = 1$, from matching the first components loosely."),
   (r"four", r"Takes $a = \pm b$ with $a^2 + b^2 = 1$ without checking both component equations."),
   (r"infinitely many", r"Confuses $(b, a)$ with $(a, -b)$, for which $|z| = 1$ gives infinitely many.")],
  r"Let $z = a + ib$. The pair $(b, a)$ is $b + ia = i(a - ib) = i\overline{z}$. The condition $z^{-1} = i\overline{z}$ gives $z\overline{z} = \frac{1}{i} = -i$, that is $|z|^2 = -i$, impossible since $|z|^2$ is real and positive. Hence there are no such pairs.",
  "Not translating the swapped pair into conjugate form.",
  "U02-A-ordered-pair-inverse-swap", r"Recognising $(b, a)$ as $i\overline{z}$, then a modulus contradiction.",
  check=_c50, values=[0, 2, 4, Symbol('infinitely_many')], cognitive="Analysis")

def _c51():
    # z = x + iy with y != 0; z + conj(z) = 1 gives x = 1/2; then impose Im(z + 1/z) = 0
    x = Rational(1, 2)
    y = symbols('y', real=True, nonzero=True)
    z = x + I*y
    ys = solve(simplify(im(expand_complex(z + 1/z))/y), y)
    vals = {simplify(expand(z.subs(y, s)**2 + conjugate(z.subs(y, s))**2)) for s in ys}
    assert len(vals) == 1
    return vals.pop()
q("U02-A-051", "Algebra of complex numbers", "Non-real z with z + 1/z real", "Difficult",
  "Multi-step computation MCQ",
  r"Let $z$ be a non-real complex number such that $z + \frac{1}{z}$ is real and $z + \overline{z} = 1$. Then $z^2 + \overline{z}^2$ equals",
  r"$-1$",
  [(r"$0$", r"Uses $z^2 + \overline{z}^2 = (z + \overline{z})^2 - z\overline{z}$, missing the factor $2$."),
   (r"$3$", r"Uses $(z + \overline{z})^2 + 2z\overline{z}$, a sign slip."),
   (r"$-\frac{1}{2}$", "Computes $x^2 - y^2$ but omits the factor $2$ in $2(x^2 - y^2)$.")],
  r"With $z = x + iy$, $y \ne 0$: $\operatorname{Im}\left(z + \frac{1}{z}\right) = y - \frac{y}{x^2 + y^2} = 0$ forces $|z|^2 = 1$. Then $z^2 + \overline{z}^2 = (z + \overline{z})^2 - 2z\overline{z} = 1 - 2 = -1$.",
  "Not extracting $|z| = 1$ from the reality condition.",
  "U02-A-z-plus-inverse-real", "Derive $|z| = 1$ from a reality condition, then a conjugate identity.",
  check=_c51, values=[-1, 0, 3, Rational(-1, 2)], cognitive="Analysis")

def _c52():
    s = sum(I**(k**2) for k in range(1, 31))
    w = expand(s/(2 - I))
    return simplify(re(w)**2 + im(w)**2)
q("U02-A-052", "Algebra of complex numbers", "Equality with a sum of powers of i with square exponents", "Difficult",
  "Multi-step computation MCQ",
  r"If $x$ and $y$ are real and $(2 - i)(x + iy) = \sum_{k=1}^{30} i^{k^2}$, then $x^2 + y^2$ equals",
  r"$90$",
  [(r"$\frac{2}{5}$", r"Reads $i^{k^2}$ as $i^k$, so the sum becomes $i + i^2 = -1 + i$ (as $30 = 4 \cdot 7 + 2$) and $x^2 + y^2 = \frac{2}{5}$."),
   (r"$450$", r"Multiplies $15 + 15i$ by $2 + i$ but divides by $|2 - i| = \sqrt{5}$ instead of $|2 - i|^2 = 5$, getting $\frac{2250}{5}$."),
   (r"$18$", r"Divides $|15 + 15i|^2 = 450$ by $|2 - i|^4 = 25$ instead of $|2 - i|^2 = 5$.")],
  r"For odd $k$, $k^2 \equiv 1 \pmod 4$, so $i^{k^2} = i$; for even $k$, $k^2 \equiv 0 \pmod 4$, so $i^{k^2} = 1$. Among $k = 1, \dots, 30$ there are $15$ odd and $15$ even values, so the sum is $15 + 15i$. Then $x + iy = \frac{15(1 + i)}{2 - i} = \frac{15(1 + i)(2 + i)}{5} = 3(1 + 3i) = 3 + 9i$, so $x^2 + y^2 = 9 + 81 = 90$.",
  r"Treating $i^{k^2}$ as if it followed the cycle of $i^k$.",
  "U02-A-sum-square-powers-equality", r"Trap: the exponent $k^2$ has only two residues modulo $4$, so the usual period-$4$ cancellation does not apply; then a complex division and a squared modulus.",
  check=_c52, values=[90, Rational(2, 5), 450, 18],
  numerical=dict(question=r"If $x$ and $y$ are real and $(2 - i)(x + iy) = \sum_{k=1}^{30} i^{k^2}$, then the value of $x^2 + y^2$ is", answer=90),
  cognitive="Analysis")

def _c53():
    w = sqrts(simplify((3 + 4*I)/(3 - 4*I)))
    return w
q("U02-A-053", "Algebra of complex numbers", "Square roots of a quotient of conjugates", "Difficult",
  "Multi-step computation MCQ",
  r"The square roots of $\frac{3 + 4i}{3 - 4i}$ are",
  r"$\pm\frac{3 + 4i}{5}$",
  [(r"$\pm\frac{4 + 3i}{5}$", r"Swaps the real and imaginary parts while solving $x^2 - y^2 = -\frac{7}{25}$."),
   (r"$\pm\frac{3 - 4i}{5}$", "Ignores that $xy$ must be positive since the imaginary part is positive."),
   (r"$\pm\frac{2 + i}{\sqrt{5}}$", r"Takes the square root of the numerator only, $\sqrt{3 + 4i} = 2 + i$, and divides by $\sqrt{|3 - 4i|}$.")],
  r"$\frac{3 + 4i}{3 - 4i} = \frac{(3 + 4i)^2}{|3 + 4i|^2} = \left(\frac{3 + 4i}{5}\right)^2$. So the square roots are $\pm\frac{3 + 4i}{5}$. As a check, the quotient is $\frac{-7 + 24i}{25}$ and $\left(\frac{3 + 4i}{5}\right)^2 = \frac{9 - 16 + 24i}{25}$.",
  "Taking square roots of numerator and denominator separately.",
  "U02-A-sqrt-of-quotient", "Spotting that the quotient is a perfect square; direct method is lengthy.",
  check=_c53,
  values=[FiniteSet((3 + 4*I)/5, -(3 + 4*I)/5), FiniteSet((4 + 3*I)/5, -(4 + 3*I)/5),
          FiniteSet((3 - 4*I)/5, -(3 - 4*I)/5), FiniteSet((2 + I)/sqrt(5), -(2 + I)/sqrt(5))],
  cognitive="Analysis")

q("U02-A-054", "Algebra of complex numbers", "Weighted sum of powers of i", "Difficult",
  "Multi-step computation MCQ",
  r"The value of $\sum_{k=1}^{20} k\, i^k$ is",
  r"$10 - 10i$",
  [(r"$0$", "Assumes the weighted terms cancel in blocks of four like plain powers of $i$."),
   (r"$10 + 10i$", "Sign slip in each block, taking $(4m+1)i - (4m+3)i$ as $+2i$."),
   (r"$20 - 20i$", "Counts ten blocks of four instead of five.")],
  r"Group the terms in blocks $k = 4m+1, \dots, 4m+4$: $(4m+1)i - (4m+2) - (4m+3)i + (4m+4) = 2 - 2i$. There are 5 blocks ($m = 0, \dots, 4$), so the sum is $10 - 10i$.",
  "Believing any sum built on powers of $i$ telescopes to zero.",
  "U02-A-weighted-sum-i", "Non-obvious grouping of a weighted series, then counting blocks.",
  check=lambda: expand(sum(k*I**k for k in range(1, 21))), values=[10 - 10*I, 0, 10 + 10*I, 20 - 20*I],
  cognitive="Analysis")

def _c55():
    a = symbols('a', real=True)
    z = simplify((a + 2*I)/(2 - a*I))
    assert not z.free_symbols
    return expand(sum(z**k for k in range(0, 2026)))
q("U02-A-055", "Algebra of complex numbers", "Hidden constant quotient and a sum of powers", "Difficult",
  "Multi-step computation MCQ",
  r"For a real number $a$, let $z = \frac{a + 2i}{2 - ai}$. Then $1 + z + z^2 + \dots + z^{2025}$ equals",
  r"$1 + i$",
  [(r"$0$", "Assumes all the terms cancel in blocks of four."),
   (r"$1$", "Miscounts the terms as $2025$, leaving only $z^{2024} = 1$."),
   (r"$i$", "Starts the sum at $z^1$, so only $z^{2025} = i$ remains.")],
  r"Since $i(2 - ai) = a + 2i$, we have $z = i$ for every real $a$. The sum has 2026 terms $i^0, \dots, i^{2025}$; the first 2024 cancel in blocks of four, leaving $i^{2024} + i^{2025} = 1 + i$.",
  "Treating $z$ as depending on $a$ and attempting a parametric computation.",
  "U02-A-hidden-i-sum", "Requires spotting that the quotient is identically $i$, then a careful term count.",
  check=_c55, values=[1 + I, 0, 1, I], cognitive="Analysis")
