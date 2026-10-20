import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
SC = "XI"
TOPIC = "Trigonometric identities"


def dg(x):
    """degrees -> radians (exact)"""
    return x * pi / 180


def close(a, b):
    return abs(N(a - b, 60)) < 1e-40


ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."

# ================================================================ EASY (17)


def _c001():
    return simplify(sin(dg(75)) ** 2 - sin(dg(15)) ** 2)


q("U14-A-001", TOPIC, "Difference of squares of sines", "Easy", "Single-step computation MCQ",
  r"The value of $\sin^2 75^\circ - \sin^2 15^\circ$ is",
  r"$\frac{\sqrt{3}}{2}$",
  [(r"$\frac{1}{2}$", r"Treats $\sin^2 75^\circ - \sin^2 15^\circ$ as $(\sin 75^\circ - \sin 15^\circ)^2$; since $\sin 75^\circ - \sin 15^\circ = 2\cos 45^\circ \sin 30^\circ = \frac{1}{\sqrt{2}}$, the square is $\frac{1}{2}$."),
   (r"$\frac{\sqrt{3}}{4}$", r"Inserts a spurious factor $\frac{1}{2}$: writes $\sin^2 A - \sin^2 B = \frac{1}{2}\sin(A+B)\sin(A-B) = \frac{1}{2}\cdot 1 \cdot \frac{\sqrt{3}}{2}$."),
   (r"$1$", r"Converts $-\sin^2 15^\circ$ into $+\cos^2 75^\circ$ (sign slip) and then uses $\sin^2 75^\circ + \cos^2 75^\circ = 1$.")],
  r"Using $\sin^2 A - \sin^2 B = \sin(A+B)\sin(A-B)$, the value is $\sin 90^\circ \sin 60^\circ = \frac{\sqrt{3}}{2}$. Equivalently $\sin^2 75^\circ - \sin^2 15^\circ = \cos^2 15^\circ - \sin^2 15^\circ = \cos 30^\circ$.",
  r"Confusing $a^2 - b^2$ with $(a-b)^2$ when $a, b$ are trigonometric values.",
  "U14-A-sin-square-difference", "One standard identity applied once.",
  check=_c001, values=[sqrt(3) / 2, Rational(1, 2), sqrt(3) / 4, 1], cognitive="Application", source_class=SC)


def _c002():
    return nsimplify(simplify(tan(dg(75)) - tan(dg(15))))


q("U14-A-002", TOPIC, "Special values of tangent", "Easy", "Single-step computation MCQ",
  r"The value of $\tan 75^\circ - \tan 15^\circ$ is",
  r"$2\sqrt{3}$",
  [(r"$4$", r"Takes $\tan 15^\circ = \sqrt{3} - 2$ (sign slip), so $(2+\sqrt{3}) - (\sqrt{3}-2) = 4$."),
   (r"$\sqrt{3}$", r"Uses the false rule $\tan A - \tan B = \tan(A - B) = \tan 60^\circ$."),
   (r"$\frac{\sqrt{3}}{2}$", r"Writes $\tan A - \tan B = \frac{\sin(A-B)}{\cos A \cos B}$ but drops the denominator, giving $\sin 60^\circ$.")],
  r"$\tan 75^\circ - \tan 15^\circ = \frac{\sin 60^\circ}{\cos 75^\circ \cos 15^\circ}$ and $\cos 75^\circ \cos 15^\circ = \frac{1}{2}(\cos 90^\circ + \cos 60^\circ) = \frac{1}{4}$. Hence the value is $\frac{\sqrt{3}/2}{1/4} = 2\sqrt{3}$ (also $(2+\sqrt{3}) - (2-\sqrt{3}) = 2\sqrt{3}$).",
  r"Treating $\tan A - \tan B$ as $\tan(A-B)$.",
  "U14-A-tan75-tan15", "Two special values, or one identity, in one or two steps.",
  check=_c002, values=[2 * sqrt(3), 4, sqrt(3), sqrt(3) / 2], cognitive="Application", source_class=SC)


def _c003():
    return nsimplify(simplify(cos(dg(36)) - cos(dg(72))))


q("U14-A-003", TOPIC, "Values of cos 36 and cos 72", "Easy", "Single-step computation MCQ",
  r"The value of $\cos 36^\circ - \cos 72^\circ$ is",
  r"$\frac{1}{2}$",
  [(r"$\frac{\sqrt{5}}{2}$", r"Takes $\cos 72^\circ = -\frac{\sqrt{5}-1}{4}$ (sign slip), so the difference becomes $\frac{\sqrt{5}+1}{4} + \frac{\sqrt{5}-1}{4} = \frac{\sqrt{5}}{2}$."),
   (r"$-\frac{1}{2}$", r"Swaps the two standard values, using $\cos 36^\circ = \frac{\sqrt{5}-1}{4}$ and $\cos 72^\circ = \frac{\sqrt{5}+1}{4}$."),
   (r"$\frac{1}{4}$", r"Writes $\cos 36^\circ - \cos 72^\circ = 2\sin 54^\circ \sin 18^\circ$ but drops the factor 2, getting $\cos 36^\circ \sin 18^\circ = \frac{1}{4}$.")],
  r"$\cos 36^\circ = \frac{\sqrt{5}+1}{4}$ and $\cos 72^\circ = \sin 18^\circ = \frac{\sqrt{5}-1}{4}$, so the difference is $\frac{2}{4} = \frac{1}{2}$.",
  r"Mixing up the standard values of $\cos 36^\circ$ and $\sin 18^\circ$.",
  "U14-A-cos36-cos72", "Recall of two special values and one subtraction.",
  check=_c003, values=[Rational(1, 2), sqrt(5) / 2, -Rational(1, 2), Rational(1, 4)], cognitive="Recall", source_class=SC)


def _c004():
    tA, tB = Rational(1, 2), Rational(1, 3)
    A, B = atan(tA), atan(tB)
    return simplify(expand_trig(tan(2 * A - B)))


q("U14-A-004", TOPIC, "Compound and double angle of tangent", "Easy", "Multi-step computation MCQ",
  r"If $\tan A = \frac{1}{2}$ and $\tan B = \frac{1}{3}$, then $\tan(2A - B)$ equals",
  r"$\frac{9}{13}$",
  [(r"$\frac{1}{2}$", r"Takes $\tan 2A = 2\tan A = 1$, then $\tan(2A-B) = \frac{1 - \frac{1}{3}}{1 + \frac{1}{3}} = \frac{1}{2}$."),
   (r"$\frac{9}{5}$", r"Uses $1 - \tan 2A \tan B$ in the denominator of $\tan(2A - B)$: $\frac{1}{1 - \frac{4}{9}} = \frac{9}{5}$."),
   (r"$\frac{7}{19}$", r"Uses $\tan 2A = \frac{2\tan A}{1+\tan^2 A} = \frac{4}{5}$ (the formula for $\sin 2A$), then $\frac{\frac{4}{5} - \frac{1}{3}}{1 + \frac{4}{15}} = \frac{7}{19}$.")],
  r"$\tan 2A = \frac{2 \cdot \frac{1}{2}}{1 - \frac{1}{4}} = \frac{4}{3}$. Then $\tan(2A - B) = \frac{\frac{4}{3} - \frac{1}{3}}{1 + \frac{4}{3}\cdot\frac{1}{3}} = \frac{1}{13/9} = \frac{9}{13}$.",
  r"Using $\tan 2A = 2\tan A$ or the wrong sign in the compound-angle denominator.",
  "U14-A-tan-compound-double", "Two formulas (double angle, then difference) in sequence.",
  check=_c004, values=[Rational(9, 13), Rational(1, 2), Rational(9, 5), Rational(7, 19)], cognitive="Application", source_class=SC)


def _c005():
    return cos(dg(20)) * cos(dg(40)) * cos(dg(80))


q("U14-A-005", TOPIC, "Product of cosines with doubling angles", "Easy", "Single-step computation MCQ",
  r"The value of $\cos 20^\circ \cos 40^\circ \cos 80^\circ$ is",
  r"$\frac{1}{8}$",
  [(r"$\frac{1}{4}$", r"Uses $\frac{\sin 2^n\theta}{2^{n-1}\sin\theta}$, i.e. divides by $4$ instead of $8$ for three factors."),
   (r"$\frac{1}{16}$", r"Uses $2^4$ in the denominator for three factors, i.e. one doubling too many."),
   (r"$\frac{\sqrt{3}}{8}$", r"Uses the triple-product route $\cos\theta\cos(60^\circ-\theta)\cos(60^\circ+\theta) = \frac{1}{4}\cos 3\theta$ with $\theta = 20^\circ$ but writes $\sin 3\theta$ in place of $\cos 3\theta$, getting $\frac{1}{4}\sin 60^\circ = \frac{\sqrt{3}}{8}$.")],
  r"Multiply and divide by $2\sin 20^\circ$ and use $2\sin x\cos x = \sin 2x$ three times: the product equals $\frac{\sin 160^\circ}{8\sin 20^\circ} = \frac{\sin 20^\circ}{8\sin 20^\circ} = \frac{1}{8}$.",
  r"Miscounting the power of 2 in $\cos\theta\cos 2\theta\cos 4\theta = \frac{\sin 8\theta}{8\sin\theta}$.",
  "U14-A-telescoping-cos-product", "Standard telescoping product, one idea.",
  check=_c005, values=[Rational(1, 8), Rational(1, 4), Rational(1, 16), sqrt(3) / 8], cognitive="Application", source_class=SC)


def _c006():
    return sin(dg(600)) * cos(dg(330)) + cos(dg(120)) * sin(dg(150))


q("U14-A-006", TOPIC, "Allied angles: reduction to acute angles", "Easy", "Single-step computation MCQ",
  r"The value of $\sin 600^\circ \cos 330^\circ + \cos 120^\circ \sin 150^\circ$ is",
  r"$-1$",
  [(r"$\frac{1}{2}$", r"Takes $\sin 600^\circ = \sin 240^\circ = +\frac{\sqrt{3}}{2}$ (wrong sign in the third quadrant), giving $\frac{3}{4} - \frac{1}{4}$."),
   (r"$-\frac{1}{2}$", r"Takes $\cos 120^\circ = +\frac{1}{2}$, giving $-\frac{3}{4} + \frac{1}{4}$."),
   (r"$1$", r"Ignores all quadrant signs, treating every ratio as positive: $\frac{3}{4} + \frac{1}{4}$.")],
  r"$\sin 600^\circ = \sin 240^\circ = -\frac{\sqrt{3}}{2}$, $\cos 330^\circ = \frac{\sqrt{3}}{2}$, $\cos 120^\circ = -\frac{1}{2}$, $\sin 150^\circ = \frac{1}{2}$. So the value is $-\frac{3}{4} - \frac{1}{4} = -1$.",
  r"Wrong signs when reducing angles beyond $90^\circ$.",
  "U14-A-allied-reduction", "Four direct reductions of allied angles.",
  check=_c006, values=[-1, Rational(1, 2), -Rational(1, 2), 1], cognitive="Application", source_class=SC)


def _c007():
    return nsimplify(sum(sin(dg(10 * k)) ** 2 for k in range(1, 10)))


q("U14-A-007", TOPIC, "Complementary pairs in a sum of squares", "Easy", "Single-step computation MCQ",
  r"The value of $\sin^2 10^\circ + \sin^2 20^\circ + \sin^2 30^\circ + \cdots + \sin^2 90^\circ$ (angles increasing in steps of $10^\circ$) is",
  r"$5$",
  [(r"$4$", r"Pairs $10^\circ$ with $80^\circ$, ..., $40^\circ$ with $50^\circ$ to get 4, but leaves out the last term $\sin^2 90^\circ = 1$."),
   (r"$\frac{9}{2}$", r"Assumes each $\sin^2$ term contributes $\frac{1}{2}$ on average, giving $9 \times \frac{1}{2}$."),
   (r"$\frac{11}{2}$", r"Pairs correctly and adds $\sin^2 90^\circ$, but also adds a middle term $\sin^2 45^\circ = \frac{1}{2}$ that is not in the sum.")],
  r"Since $\sin^2(90^\circ - \theta) = \cos^2\theta$, the pairs $(10^\circ, 80^\circ), (20^\circ, 70^\circ), (30^\circ, 60^\circ), (40^\circ, 50^\circ)$ each contribute $1$. Adding $\sin^2 90^\circ = 1$ gives $4 + 1 = 5$.",
  r"Dropping the unpaired term or inventing a middle term.",
  "U14-A-allied-sum-squares", "One pairing idea.",
  check=_c007, values=[5, 4, Rational(9, 2), Rational(11, 2)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The value of $\sin^2 10^\circ + \sin^2 20^\circ + \sin^2 30^\circ + \cdots + \sin^2 90^\circ$, where the angles increase in steps of $10^\circ$, is", answer=5))


def _c008():
    sA = Rational(3, 5); cA = -sqrt(1 - sA ** 2)       # A in second quadrant
    cB = Rational(5, 13); sB = sqrt(1 - cB ** 2)       # B acute
    return cA * cB - sA * sB


q("U14-A-008", TOPIC, "Compound angle with quadrant information", "Easy", "Multi-step computation MCQ",
  r"If $\sin A = \frac{3}{5}$ with $\frac{\pi}{2} < A < \pi$, and $\cos B = \frac{5}{13}$ with $0 < B < \frac{\pi}{2}$, then $\cos(A + B)$ equals",
  r"$-\frac{56}{65}$",
  [(r"$-\frac{16}{65}$", r"Takes $\cos A = +\frac{4}{5}$, ignoring the second quadrant: $\frac{20}{65} - \frac{36}{65}$."),
   (r"$\frac{16}{65}$", r"Uses $\cos A\cos B + \sin A \sin B$ (the formula for $\cos(A-B)$): $-\frac{20}{65} + \frac{36}{65}$."),
   (r"$\frac{56}{65}$", r"Takes $\cos A = +\frac{4}{5}$ and also uses the plus sign: $\frac{20}{65} + \frac{36}{65}$.")],
  r"$\cos A = -\frac{4}{5}$ (second quadrant) and $\sin B = \frac{12}{13}$. So $\cos(A+B) = \cos A\cos B - \sin A\sin B = -\frac{20}{65} - \frac{36}{65} = -\frac{56}{65}$.",
  r"Forgetting that cosine is negative in the second quadrant.",
  "U14-A-compound-quadrant", "Two values found with signs, then one formula.",
  check=_c008, values=[-Rational(56, 65), -Rational(16, 65), Rational(16, 65), Rational(56, 65)], cognitive="Application", source_class=SC)


def _c009():
    th = acos(Rational(1, 3))
    return simplify(expand_trig(cos(3 * th)))


q("U14-A-009", TOPIC, "Triple angle formula", "Easy", "Single-step computation MCQ",
  r"If $\cos\theta = \frac{1}{3}$, then $\cos 3\theta$ equals",
  r"$-\frac{23}{27}$",
  [(r"$\frac{23}{27}$", r"Uses the sine pattern $3\cos\theta - 4\cos^3\theta = 1 - \frac{4}{27}$."),
   (r"$-\frac{5}{9}$", r"Computes $\cos^3\theta$ as $\frac{1}{9}$, giving $\frac{4}{9} - 1$."),
   (r"$-\frac{26}{27}$", r"Omits the coefficient 4: $\cos^3\theta - 3\cos\theta = \frac{1}{27} - 1$.")],
  r"$\cos 3\theta = 4\cos^3\theta - 3\cos\theta = \frac{4}{27} - 1 = -\frac{23}{27}$.",
  r"Interchanging the triple angle formulas for sine and cosine.",
  "U14-A-triple-angle-value", "Direct use of one formula.",
  check=_c009, values=[-Rational(23, 27), Rational(23, 27), -Rational(5, 9), -Rational(26, 27)], cognitive="Recall", source_class=SC)


def _c010():
    th = atan(3)
    return simplify(cos(2 * th))


q("U14-A-010", TOPIC, "Double angle in terms of tangent", "Easy", "Single-step computation MCQ",
  r"If $\tan\theta = 3$, then $\cos 2\theta$ equals",
  r"$-\frac{4}{5}$",
  [(r"$\frac{4}{5}$", r"Writes $\cos 2\theta = \frac{\tan^2\theta - 1}{1 + \tan^2\theta}$ (numerator reversed)."),
   (r"$\frac{3}{5}$", r"Uses $\frac{2\tan\theta}{1+\tan^2\theta}$, which is $\sin 2\theta$."),
   (r"$-\frac{3}{4}$", r"Uses $\frac{2\tan\theta}{1-\tan^2\theta}$, which is $\tan 2\theta$.")],
  r"$\cos 2\theta = \frac{1-\tan^2\theta}{1+\tan^2\theta} = \frac{1-9}{1+9} = -\frac{4}{5}$. This depends only on $\tan\theta$, so no quadrant information is needed.",
  r"Mixing up the three tangent-form double angle formulas.",
  "U14-A-double-angle-tan", "One formula, one substitution.",
  check=_c010, values=[-Rational(4, 5), Rational(4, 5), Rational(3, 5), -Rational(3, 4)], cognitive="Recall", source_class=SC)


def _c011():
    return nsimplify(simplify(sin(dg(15)) ** 4 + cos(dg(15)) ** 4))


q("U14-A-011", TOPIC, "Fourth powers via double angle", "Easy", "Single-step computation MCQ",
  r"The value of $\sin^4 15^\circ + \cos^4 15^\circ$ is",
  r"$\frac{7}{8}$",
  [(r"$\frac{3}{4}$", r"Writes $2\sin^2\theta\cos^2\theta = \sin^2 2\theta$ (no factor $\frac{1}{2}$), giving $1 - \frac{1}{4}$."),
   (r"$1$", r"Treats $\sin^4\theta + \cos^4\theta$ as $(\sin^2\theta + \cos^2\theta)^2$, dropping the cross term."),
   (r"$\frac{15}{16}$", r"Uses $2\sin^2\theta\cos^2\theta = \frac{1}{4}\sin^2 2\theta$, giving $1 - \frac{1}{16}$.")],
  r"$\sin^4\theta + \cos^4\theta = 1 - 2\sin^2\theta\cos^2\theta = 1 - \frac{1}{2}\sin^2 2\theta$. With $\theta = 15^\circ$: $1 - \frac{1}{2}\cdot\frac{1}{4} = \frac{7}{8}$.",
  r"Losing the cross term or the factor $\frac{1}{2}$ in $\sin^2\theta\cos^2\theta = \frac{1}{4}\sin^2 2\theta$.",
  "U14-A-sin4-cos4", "One algebraic identity and one double angle step.",
  check=_c011, values=[Rational(7, 8), Rational(3, 4), 1, Rational(15, 16)], cognitive="Application", source_class=SC)


_x = Symbol('x')


def _c012():
    return (sin(7 * _x) - sin(5 * _x)) / (cos(7 * _x) + cos(5 * _x))


q("U14-A-012", TOPIC, "Sum-to-product simplification", "Easy", "Single-step computation MCQ",
  r"For all $x$ for which the expression is defined, $\frac{\sin 7x - \sin 5x}{\cos 7x + \cos 5x}$ equals",
  r"$\tan x$",
  [(r"$\tan 6x$", r"Writes $\sin 7x - \sin 5x = 2\sin 6x\cos x$ (the sum formula), so the ratio becomes $\frac{2\sin 6x\cos x}{2\cos 6x\cos x}$."),
   (r"$-\tan x$", r"Uses $\sin C - \sin D = 2\cos\frac{C+D}{2}\sin\frac{D-C}{2}$ (half-difference reversed), giving $\frac{-2\cos 6x\sin x}{2\cos 6x\cos x}$."),
   (r"$\cot 6x$", r"Uses the form $2\sin\frac{C+D}{2}\sin\frac{C-D}{2}$ for $\cos 7x + \cos 5x$ in the denominator, giving $\frac{2\cos 6x\sin x}{2\sin 6x\sin x}$.")],
  r"$\sin 7x - \sin 5x = 2\cos 6x\sin x$ and $\cos 7x + \cos 5x = 2\cos 6x\cos x$, so the ratio is $\frac{\sin x}{\cos x} = \tan x$.",
  r"Interchanging the four sum-to-product formulas.",
  "U14-A-sum-to-product-simplify", "Two sum-to-product formulas, then cancellation.",
  check=_c012, values=[tan(_x), tan(6 * _x), -tan(_x), cot(6 * _x)], cognitive="Application", source_class=SC)


_B = Symbol('B')


def _c013():
    t = (1 - cos(_B)) / sin(_B)
    return 2 * t / (1 - t ** 2)


q("U14-A-013", TOPIC, "Half angle form of tangent", "Easy", "Conceptual/application MCQ",
  r"If $\tan A = \frac{1 - \cos B}{\sin B}$, where all the expressions involved are defined, then $\tan 2A$ equals",
  r"$\tan B$",
  [(r"$\tan\frac{B}{2}$", r"Recognises $\tan A = \tan\frac{B}{2}$ but reports $\tan A$, not $\tan 2A$."),
   (r"$2\tan\frac{B}{2}$", r"Uses $\tan 2A = 2\tan A$."),
   (r"$-\tan B$", r"Inverts the half angle form, taking $\frac{1-\cos B}{\sin B} = \cot\frac{B}{2}$; then $\frac{2\cot(B/2)}{1-\cot^2(B/2)} = -\tan B$.")],
  r"$\frac{1-\cos B}{\sin B} = \frac{2\sin^2(B/2)}{2\sin(B/2)\cos(B/2)} = \tan\frac{B}{2}$. So $\tan A = \tan\frac{B}{2}$ and $\tan 2A = \frac{2\tan(B/2)}{1-\tan^2(B/2)} = \tan B$.",
  r"Mixing up $\frac{1-\cos B}{\sin B}$ with $\cot\frac{B}{2}$.",
  "U14-A-half-angle-tan-form", "Recognise one half-angle form, apply double angle.",
  check=_c013, values=[tan(_B), tan(_B / 2), 2 * tan(_B / 2), -tan(_B)], cognitive="Understanding", source_class=SC)


def _c014():
    A, B = atan(2), atan(3)
    C = pi - A - B
    return simplify(tan(C))


q("U14-A-014", TOPIC, "Conditional identity: A + B + C = pi", "Easy", "Single-step computation MCQ",
  r"If $A + B + C = \pi$, $\tan A = 2$ and $\tan B = 3$, then $\tan C$ equals",
  r"$1$",
  [(r"$-1$", r"Computes $\tan(A + B) = -1$ and stops, forgetting that $\tan C = -\tan(A+B)$."),
   (r"$-\frac{5}{7}$", r"Uses $1 + \tan A\tan B$ in the denominator, getting $\tan(A+B) = \frac{5}{7}$, and then $\tan C = -\frac{5}{7}$."),
   (r"$\frac{5}{7}$", r"Uses $1 + \tan A\tan B$ in the denominator and also forgets the minus sign in $\tan C = -\tan(A+B)$.")],
  r"$\tan C = \tan(\pi - (A+B)) = -\tan(A+B) = -\frac{2+3}{1-6} = 1$. (Check: $\tan A + \tan B + \tan C = 6 = \tan A\tan B\tan C$.)",
  r"Forgetting $\tan(\pi - \theta) = -\tan\theta$.",
  "U14-A-tan-sum-pi", "One compound angle formula and one allied angle step.",
  check=_c014, values=[1, -1, -Rational(5, 7), Rational(5, 7)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $A + B + C = \pi$, $\tan A = 2$ and $\tan B = 3$, then the value of $\tan C$ is", answer=1))


def _c015():
    t = tan(dg(Rational(45, 2)))
    return nsimplify(simplify(t ** 2 + 1 / t ** 2))


q("U14-A-015", TOPIC, "tan + cot as a double angle", "Easy", "Single-step computation MCQ",
  r"The value of $\tan^2 22.5^\circ + \cot^2 22.5^\circ$ is",
  r"$6$",
  [(r"$8$", r"Finds $\tan 22.5^\circ + \cot 22.5^\circ = \frac{2}{\sin 45^\circ} = 2\sqrt{2}$ and squares it, forgetting to subtract $2\tan\theta\cot\theta = 2$."),
   (r"$10$", r"Uses $a^2 + b^2 = (a+b)^2 + 2ab$ (sign slip): $8 + 2 = 10$."),
   (r"$4$", r"Uses $a^2 + b^2 = (a+b)^2 - 4ab$, confusing it with $(a-b)^2 = (a+b)^2 - 4ab$: $8 - 4 = 4$.")],
  r"$\tan\theta + \cot\theta = \frac{\sin^2\theta + \cos^2\theta}{\sin\theta\cos\theta} = \frac{2}{\sin 2\theta}$, so with $\theta = 22.5^\circ$ it equals $\frac{2}{\sin 45^\circ} = 2\sqrt{2}$. Since $\tan\theta\cot\theta = 1$, $\tan^2\theta + \cot^2\theta = (2\sqrt{2})^2 - 2 = 6$. (Directly: $(\sqrt{2}-1)^2 + (\sqrt{2}+1)^2 = 6$.)",
  r"Forgetting the cross term $2\tan\theta\cot\theta$ when passing from $\tan\theta + \cot\theta$ to $\tan^2\theta + \cot^2\theta$.",
  "U14-A-tan-plus-cot", "One double-angle identity and one algebraic step.",
  check=_c015, values=[6, 8, 10, 4], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The value of $\tan^2 22.5^\circ + \cot^2 22.5^\circ$ is", answer=6))


def _c016():
    c = Rational(-3, 5)
    th = 2 * pi - acos(c)   # the angle in (pi, 3pi/2) with cos = -3/5
    assert pi < th < 3 * pi / 2
    return simplify(tan(th / 2))


q("U14-A-016", TOPIC, "Half angle with quadrant", "Easy", "Single-step computation MCQ",
  r"If $\cos\theta = -\frac{3}{5}$ and $\pi < \theta < \frac{3\pi}{2}$, then $\tan\frac{\theta}{2}$ equals",
  r"$-2$",
  [(r"$2$", r"Takes the positive root of $\tan^2\frac{\theta}{2} = 4$, not noticing that $\frac{\theta}{2}$ lies in the second quadrant."),
   (r"$-\frac{1}{2}$", r"Inverts the half angle formula, using $\tan^2\frac{\theta}{2} = \frac{1+\cos\theta}{1-\cos\theta} = \frac{1}{4}$, then takes the negative root."),
   (r"$\frac{1}{2}$", r"Inverts the half angle formula and also takes the positive root.")],
  r"$\tan^2\frac{\theta}{2} = \frac{1-\cos\theta}{1+\cos\theta} = \frac{8/5}{2/5} = 4$. Since $\frac{\pi}{2} < \frac{\theta}{2} < \frac{3\pi}{4}$, $\tan\frac{\theta}{2} < 0$, so $\tan\frac{\theta}{2} = -2$.",
  r"Ignoring the quadrant of $\frac{\theta}{2}$ when taking a square root.",
  "U14-A-half-angle-quadrant", "One formula plus a sign decision.",
  check=_c016, values=[-2, 2, -Rational(1, 2), Rational(1, 2)], cognitive="Application", source_class=SC)


def _c017():
    return nsimplify(simplify(cos(dg(15)) - sin(dg(15))))


q("U14-A-017", TOPIC, "a cos x - b sin x as a single cosine", "Easy", "Single-step computation MCQ",
  r"The value of $\cos 15^\circ - \sin 15^\circ$ is",
  r"$\frac{1}{\sqrt{2}}$",
  [(r"$\frac{\sqrt{3}}{2}$", r"Treats $\cos 15^\circ - \sin 15^\circ$ as $\cos^2 15^\circ - \sin^2 15^\circ = \cos 30^\circ$."),
   (r"$\sqrt{\frac{3}{2}}$", r"Computes $\cos 15^\circ + \sin 15^\circ = \sqrt{2}\sin 60^\circ$ (sign slip)."),
   (r"$\frac{1}{2}$", r"Writes $\cos 15^\circ - \sin 15^\circ = \cos(15^\circ + 45^\circ)$, dropping the factor $\sqrt{2}$.")],
  r"$\cos 15^\circ - \sin 15^\circ = \sqrt{2}\left(\cos 15^\circ\cos 45^\circ - \sin 15^\circ \sin 45^\circ\right) = \sqrt{2}\cos 60^\circ = \frac{\sqrt{2}}{2} = \frac{1}{\sqrt{2}}$.",
  r"Forgetting the factor $\sqrt{2}$ when combining $\cos x - \sin x$.",
  "U14-A-cos-minus-sin-15", "One compound-angle rewrite.",
  check=_c017, values=[1 / sqrt(2), sqrt(3) / 2, sqrt(Rational(3, 2)), Rational(1, 2)], cognitive="Application", source_class=SC)


# ================================================================ MEDIUM (25)

_t = Symbol('t')


def _c018():
    A = atan(Rational(1, 7))
    T2 = simplify(tan(pi / 4 - A))            # tan 2B
    sols = [s for s in solve(Eq(2 * _t / (1 - _t ** 2), T2), _t) if 0 < s < 1]
    assert len(sols) == 1
    return sols[0]


q("U14-A-018", TOPIC, "Reverse use of double angle", "Medium", "Inverse/parameter MCQ",
  r"Let $\tan A = \frac{1}{7}$ with $0 < A < \frac{\pi}{2}$, and let $A + 2B = \frac{\pi}{4}$ where $0 < B < \frac{\pi}{4}$. Then $\tan B$ equals",
  r"$\frac{1}{3}$",
  [(r"$\frac{3}{4}$", r"Finds $\tan 2B = \tan\left(\frac{\pi}{4} - A\right) = \frac{3}{4}$ and stops."),
   (r"$\frac{3}{8}$", r"Finds $\tan 2B = \frac{3}{4}$ and then uses $\tan 2B = 2\tan B$."),
   (r"$\frac{1}{2}$", r"Uses $\tan\left(\frac{\pi}{4} - A\right) = \frac{1+\tan A}{1-\tan A} = \frac{4}{3}$; solving $\frac{2t}{1-t^2} = \frac{4}{3}$ gives $t = \frac{1}{2}$.")],
  r"$\tan 2B = \tan\left(\frac{\pi}{4} - A\right) = \frac{1 - \frac{1}{7}}{1 + \frac{1}{7}} = \frac{3}{4}$. With $t = \tan B$: $\frac{2t}{1-t^2} = \frac{3}{4}$, i.e. $3t^2 + 8t - 3 = 0$, so $t = \frac{1}{3}$ or $t = -3$. As $0 < B < \frac{\pi}{4}$, $\tan B = \frac{1}{3}$.",
  r"Stopping at $\tan 2B$, or treating $\tan 2B$ as $2\tan B$.",
  "U14-A-tan-double-reverse", "Compound angle, then a quadratic from the double angle formula, then a root selection.",
  check=_c018, values=[Rational(1, 3), Rational(3, 4), Rational(3, 8), Rational(1, 2)], cognitive="Application", source_class=SC)


def _c019():
    return sin(dg(47)) + sin(dg(61)) - sin(dg(11)) - sin(dg(25))


q("U14-A-019", TOPIC, "Sum-to-product with special values", "Medium", "Multi-step computation MCQ",
  r"The value of $\sin 47^\circ + \sin 61^\circ - \sin 11^\circ - \sin 25^\circ$ is",
  r"$\cos 7^\circ$",
  [(r"$\frac{1}{2}\cos 7^\circ$", r"Drops the factor 2 in $\sin C + \sin D = 2\sin\frac{C+D}{2}\cos\frac{C-D}{2}$, getting $\cos 7^\circ(\sin 54^\circ - \sin 18^\circ)$."),
   (r"$\sqrt{5}\cos 7^\circ$", r"Sign slip: adds the second group, getting $2\cos 7^\circ(\sin 54^\circ + \sin 18^\circ) = 2\cos 7^\circ\cdot\frac{\sqrt{5}}{2}$."),
   (r"$\frac{\sqrt{5}}{2}\cos 7^\circ$", r"Makes both slips: drops the factor 2 and adds the second group, getting $\cos 7^\circ(\sin 54^\circ + \sin 18^\circ)$.")],
  r"Group as $(\sin 47^\circ + \sin 61^\circ) - (\sin 11^\circ + \sin 25^\circ) = 2\sin 54^\circ\cos 7^\circ - 2\sin 18^\circ\cos 7^\circ = 2\cos 7^\circ(\sin 54^\circ - \sin 18^\circ)$. Since $\sin 54^\circ - \sin 18^\circ = \frac{\sqrt{5}+1}{4} - \frac{\sqrt{5}-1}{4} = \frac{1}{2}$, the value is $\cos 7^\circ$.",
  r"Losing the factor 2 in sum-to-product, or mis-signing a group.",
  "U14-A-sum-to-product-numeric", "Choosing the right grouping, two sum-to-product steps and special values.",
  check=_c019, values=[cos(dg(7)), cos(dg(7)) / 2, sqrt(5) * cos(dg(7)), sqrt(5) / 2 * cos(dg(7))], cognitive="Analysis", source_class=SC)


def _c020():
    out = set()
    for A, B in [(Rational(7, 10), Rational(13, 10)), (Rational(1, 3), Rational(1, 2)), (Rational(9, 10), Rational(2, 5))]:
        C = pi - A - B
        r = (sin(2 * A) + sin(2 * B) + sin(2 * C)) / (sin(A) * sin(B) * sin(C))
        out.add(round(float(N(r, 40)), 12))
    assert len(out) == 1
    return nsimplify(out.pop())


q("U14-A-020", TOPIC, "Conditional identity for sin 2A + sin 2B + sin 2C", "Medium", "Multi-step computation MCQ",
  r"If $A$, $B$, $C$ are the angles of a triangle, then $\frac{\sin 2A + \sin 2B + \sin 2C}{\sin A \sin B \sin C}$ equals",
  r"$4$",
  [(r"$2$", r"Drops every factor 2: uses $\sin 2\theta = \sin\theta\cos\theta$ and $\sin C + \sin D = \sin\frac{C+D}{2}\cos\frac{C-D}{2}$, which halves the numerator to $2\sin A\sin B\sin C$."),
   (r"$-4$", r"Uses the wrong sign in $\cos(A-B) - \cos(A+B) = -2\sin A\sin B$ at the last step."),
   (r"$6$", r"Tests with $A = 90^\circ$, $B = C = 45^\circ$ but takes $\sin 180^\circ = 1$, getting $\frac{3}{1/2}$.")],
  r"$\sin 2A + \sin 2B = 2\sin(A+B)\cos(A-B) = 2\sin C\cos(A-B)$ and $\sin 2C = 2\sin C\cos C = -2\sin C\cos(A+B)$. So the numerator is $2\sin C[\cos(A-B) - \cos(A+B)] = 4\sin A\sin B\sin C$, and the ratio is $4$.",
  r"Sign errors with $\sin(\pi - C)$ and $\cos(\pi - C)$.",
  "U14-A-pi-sin2A-sum", "Sum-to-product plus two allied-angle substitutions under $A+B+C=\\pi$.",
  check=_c020, values=[4, 2, -4, 6], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $A$, $B$, $C$ are the angles of a triangle, then the value of $\frac{\sin 2A + \sin 2B + \sin 2C}{\sin A \sin B \sin C}$ is", answer=4))


def _c021():
    a, b = Rational(1, 3), Rational(1, 4)
    A, B = 2 * atan(a), 2 * atan(b)
    C = pi - A - B
    assert N(C) > 0
    return nsimplify(simplify(tan(C / 2)))


q("U14-A-021", TOPIC, "Half angle identity in a triangle", "Medium", "Multi-step computation MCQ",
  r"In a triangle $PQR$, $\tan\frac{P}{2} = \frac{1}{3}$ and $\tan\frac{Q}{2} = \frac{1}{4}$. Then $\tan\frac{R}{2}$ equals",
  r"$\frac{11}{7}$",
  [(r"$\frac{12}{7}$", r"Uses $\tan\frac{R}{2}\left(\tan\frac{P}{2} + \tan\frac{Q}{2}\right) = 1$, dropping the term $\tan\frac{P}{2}\tan\frac{Q}{2}$."),
   (r"$\frac{7}{11}$", r"Takes $\tan\frac{R}{2} = \tan\frac{P+Q}{2} = \frac{7/12}{11/12}$, forgetting that $\frac{R}{2} = \frac{\pi}{2} - \frac{P+Q}{2}$."),
   (r"$\frac{13}{7}$", r"Uses $\cot\frac{P+Q}{2}$ but with $1 + \tan\frac{P}{2}\tan\frac{Q}{2}$ in the numerator: $\frac{13/12}{7/12}$.")],
  r"Since $\frac{R}{2} = \frac{\pi}{2} - \frac{P+Q}{2}$, $\tan\frac{P}{2}\tan\frac{Q}{2} + \tan\frac{Q}{2}\tan\frac{R}{2} + \tan\frac{R}{2}\tan\frac{P}{2} = 1$. So $\frac{1}{12} + \frac{7}{12}\tan\frac{R}{2} = 1$, giving $\tan\frac{R}{2} = \frac{11}{7}$.",
  r"Treating $\frac{R}{2}$ as $\frac{P+Q}{2}$ instead of its complement.",
  "U14-A-half-angle-pi", "Conditional identity for half angles, with a linear solve.",
  check=_c021, values=[Rational(11, 7), Rational(12, 7), Rational(7, 11), Rational(13, 7)], cognitive="Application", source_class=SC)


def _c022():
    s1 = s2 = True
    for A, B in [(Rational(7, 10), Rational(13, 10)), (Rational(1, 3), Rational(11, 10))]:
        C = pi - A - B
        s1 = s1 and close(cos(A) ** 2 + cos(B) ** 2 + cos(C) ** 2 + 2 * cos(A) * cos(B) * cos(C), 1)
        s2 = s2 and close(sin(A) ** 2 + sin(B) ** 2 + sin(C) ** 2, 2 - 2 * cos(A) * cos(B) * cos(C))
    return (bool(s1), bool(s2))


q("U14-A-022", TOPIC, "Squares of cosines and sines under A + B + C = pi", "Medium", "Statement-based MCQ",
  r"Let $A + B + C = \pi$. Statement I: $\cos^2 A + \cos^2 B + \cos^2 C + 2\cos A\cos B\cos C = 1$. Statement II: $\sin^2 A + \sin^2 B + \sin^2 C = 2 - 2\cos A\cos B\cos C$." + TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement I, but when converting it transposes $2\cos A\cos B\cos C$ without changing its sign, taking $\sum\cos^2 A = 1 + 2\cos A\cos B\cos C$; then $\sum\sin^2 A = 3 - \sum\cos^2 A$ gives Statement II."),
   (ST_FF, r"Rejects Statement I, typically after expanding $\cos C = \cos(A+B)$ without the minus sign."),
   (ST_FT, r"Interchanges the signs: believes the cosine identity has $-2\cos A\cos B\cos C$ and the sine one has $-$ as well.")],
  r"Statement I: $\cos^2 A + \cos^2 B = 1 + \cos(A+B)\cos(A-B) = 1 - \cos C\cos(A-B)$, so $\cos^2 A + \cos^2 B + \cos^2 C = 1 - \cos C[\cos(A-B) + \cos(A+B)] = 1 - 2\cos A\cos B\cos C$; Statement I is true. Then $\sin^2 A + \sin^2 B + \sin^2 C = 3 - (1 - 2\cos A\cos B\cos C) = 2 + 2\cos A\cos B\cos C$, so Statement II is false (for example $A = B = C = \frac{\pi}{3}$ gives $\frac{9}{4} \ne \frac{7}{4}$).",
  r"Sign errors when converting the cosine identity to sines.",
  "U14-A-pi-squares-statement", "Two conditional identities to verify, with a sign trap.",
  check=_c022, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis", source_class=SC)


def _c023():
    return cos(pi / 15) * cos(2 * pi / 15) * cos(4 * pi / 15) * cos(8 * pi / 15)


q("U14-A-023", TOPIC, "Telescoping cosine product with a sign", "Medium", "Multi-step computation MCQ",
  r"The value of $\cos\frac{\pi}{15}\cos\frac{2\pi}{15}\cos\frac{4\pi}{15}\cos\frac{8\pi}{15}$ is",
  r"$-\frac{1}{16}$",
  [(r"$\frac{1}{16}$", r"Reaches $\frac{\sin(16\pi/15)}{16\sin(\pi/15)}$ but takes $\sin\frac{16\pi}{15} = \sin\frac{\pi}{15}$."),
   (r"$-\frac{1}{8}$", r"Uses $2^3$ in the denominator for four factors."),
   (r"$-\frac{1}{32}$", r"Uses $2^5$ in the denominator for four factors.")],
  r"Multiplying and dividing by $2\sin\frac{\pi}{15}$ and doubling four times gives $\frac{\sin(16\pi/15)}{16\sin(\pi/15)}$. Since $\sin\frac{16\pi}{15} = \sin\left(\pi + \frac{\pi}{15}\right) = -\sin\frac{\pi}{15}$, the product is $-\frac{1}{16}$.",
  r"Missing the sign of $\sin(\pi + x)$ at the end of the telescoping.",
  "U14-A-telescoping-negative", "Telescoping plus an allied-angle sign that is easy to miss.",
  check=_c023, values=[-Rational(1, 16), Rational(1, 16), -Rational(1, 8), -Rational(1, 32)], cognitive="Application", source_class=SC)


def _c024():
    P = Mul(*[cos(2 ** r * pi / 65) for r in range(6)])
    k = round(float(-log(N(P, 50), 2)))
    assert close(P * 2 ** k, 1)
    return k


q("U14-A-024", TOPIC, "Telescoping cosine product: exponent", "Medium", "Inverse/parameter MCQ",
  r"If $\cos\frac{\pi}{65}\cos\frac{2\pi}{65}\cos\frac{4\pi}{65}\cos\frac{8\pi}{65}\cos\frac{16\pi}{65}\cos\frac{32\pi}{65} = \frac{1}{2^k}$, then $k$ equals",
  r"$6$",
  [(r"$5$", r"Uses $2^{n-1}$ in the telescoping denominator for $n = 6$ factors."),
   (r"$7$", r"Uses $2^{n+1}$ in the denominator, doubling once too often."),
   (r"$64$", r"Finds the product $\frac{1}{64}$ correctly but reports $2^k$ instead of $k$.")],
  r"The product equals $\frac{\sin(64\pi/65)}{2^6\sin(\pi/65)}$. Since $\sin\frac{64\pi}{65} = \sin\left(\pi - \frac{\pi}{65}\right) = \sin\frac{\pi}{65}$, the product is $\frac{1}{64} = \frac{1}{2^6}$, so $k = 6$.",
  r"Miscounting the power of 2 in a telescoping product.",
  "U14-A-telescoping-cos-product", "Spotting the doubling pattern and that $64\\pi/65$ is supplementary to $\\pi/65$.",
  check=_c024, values=[6, 5, 7, 64], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $\cos\frac{\pi}{65}\cos\frac{2\pi}{65}\cos\frac{4\pi}{65}\cos\frac{8\pi}{65}\cos\frac{16\pi}{65}\cos\frac{32\pi}{65} = \frac{1}{2^k}$, then the value of $k$ is", answer=6))


def _c025():
    return sin(dg(20)) * sin(dg(40)) * sin(dg(60)) * sin(dg(80))


q("U14-A-025", TOPIC, "Product identity sin x sin(60 - x) sin(60 + x)", "Medium", "Multi-step computation MCQ",
  r"The value of $\sin 20^\circ \sin 40^\circ \sin 60^\circ \sin 80^\circ$ is",
  r"$\frac{3}{16}$",
  [(r"$\frac{\sqrt{3}}{8}$", r"Evaluates $\sin 20^\circ\sin 40^\circ\sin 80^\circ = \frac{\sqrt{3}}{8}$ but forgets the factor $\sin 60^\circ$."),
   (r"$\frac{3}{8}$", r"Uses $\sin\theta\sin(60^\circ-\theta)\sin(60^\circ+\theta) = \frac{1}{2}\sin 3\theta$, getting $\frac{\sqrt{3}}{4}\cdot\frac{\sqrt{3}}{2}$."),
   (r"$\frac{\sqrt{3}}{16}$", r"Uses the value $\frac{1}{8}$ of $\cos 20^\circ\cos 40^\circ\cos 80^\circ$ for the sine product, then multiplies by $\frac{\sqrt{3}}{2}$.")],
  r"With $\theta = 20^\circ$, $\sin\theta\sin(60^\circ - \theta)\sin(60^\circ + \theta) = \frac{1}{4}\sin 3\theta$ gives $\sin 20^\circ\sin 40^\circ\sin 80^\circ = \frac{1}{4}\cdot\frac{\sqrt{3}}{2} = \frac{\sqrt{3}}{8}$. Multiplying by $\sin 60^\circ = \frac{\sqrt{3}}{2}$ gives $\frac{3}{16}$.",
  r"Misremembering the constant $\frac{1}{4}$ in the triple product identity.",
  "U14-A-sine-product-60", "Recognise the triple-product pattern and keep the extra factor.",
  check=_c025, values=[Rational(3, 16), sqrt(3) / 8, Rational(3, 8), sqrt(3) / 16], cognitive="Application", source_class=SC)


def _c026():
    P = Integer(1)
    for k in range(1, 46):
        P = P * (1 + tan(dg(k)))
    n = round(float(log(N(P, 60), 2)))
    assert close(P, 2 ** n)
    return n


q("U14-A-026", TOPIC, "(1 + tan A)(1 + tan B) with A + B = 45 degrees", "Medium", "Inverse/parameter MCQ",
  r"If $(1 + \tan 1^\circ)(1 + \tan 2^\circ)(1 + \tan 3^\circ)\cdots(1 + \tan 45^\circ) = 2^n$, then $n$ equals",
  r"$23$",
  [(r"$22$", r"Pairs $k^\circ$ with $(45-k)^\circ$ correctly to get $2^{22}$ but forgets the last factor $1 + \tan 45^\circ = 2$."),
   (r"$45$", r"Assumes every one of the 45 factors equals 2."),
   (r"$44$", r"Takes each pair product $(1+\tan A)(1+\tan B)$ as $2^2$ and leaves out the factor $1 + \tan 45^\circ$.")],
  r"If $A + B = 45^\circ$, then $\tan A + \tan B = 1 - \tan A\tan B$, so $(1+\tan A)(1+\tan B) = 1 + \tan A + \tan B + \tan A\tan B = 2$. The 44 factors for $1^\circ$ to $44^\circ$ form 22 such pairs, giving $2^{22}$, and $1 + \tan 45^\circ = 2$. So the product is $2^{23}$ and $n = 23$.",
  r"Forgetting the unpaired factor $1 + \tan 45^\circ$.",
  "U14-A-one-plus-tan-product", "Compound-angle condition turned into a pairing argument across 45 factors.",
  check=_c026, values=[23, 22, 45, 44], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"If $(1 + \tan 1^\circ)(1 + \tan 2^\circ)(1 + \tan 3^\circ)\cdots(1 + \tan 45^\circ) = 2^n$, then the value of $n$ is", answer=23))


def _c027():
    u = Rational(1, 3) + I * Rational(1, 2)     # e^{iA} + e^{iB}
    return simplify(im(u ** 2) / Abs(u) ** 2)   # since u = 2cos((A-B)/2) e^{i(A+B)/2}


q("U14-A-027", TOPIC, "Sums of sines and cosines given", "Medium", "Multi-step computation MCQ",
  r"If $\sin A + \sin B = \frac{1}{2}$ and $\cos A + \cos B = \frac{1}{3}$, then $\sin(A + B)$ equals",
  r"$\frac{12}{13}$",
  [(r"$-\frac{5}{13}$", r"Uses $\frac{1-t^2}{1+t^2}$ with $t = \tan\frac{A+B}{2} = \frac{3}{2}$, which is $\cos(A+B)$."),
   (r"$\frac{6}{13}$", r"Uses $\frac{t}{1+t^2}$, dropping the factor 2 in $\sin(A+B) = \frac{2t}{1+t^2}$."),
   (r"$\frac{3}{\sqrt{13}}$", r"Finds $\sin\frac{A+B}{2} = \frac{t}{\sqrt{1+t^2}}$ and stops at the half angle.")],
  r"$\sin A + \sin B = 2\sin\frac{A+B}{2}\cos\frac{A-B}{2}$ and $\cos A + \cos B = 2\cos\frac{A+B}{2}\cos\frac{A-B}{2}$; dividing, $\tan\frac{A+B}{2} = \frac{3}{2}$. Hence $\sin(A+B) = \frac{2t}{1+t^2} = \frac{3}{13/4} = \frac{12}{13}$.",
  r"Using the cosine form or stopping at the half angle.",
  "U14-A-sum-sin-cos-given", "Sum-to-product, division, then a tangent half-angle substitution.",
  check=_c027, values=[Rational(12, 13), -Rational(5, 13), Rational(6, 13), 3 / sqrt(13)], cognitive="Application", source_class=SC)


def _c028():
    u = Rational(1, 3) + I * Rational(1, 2)
    return simplify((Abs(u) ** 2 - 2) / 2)      # |e^{iA}+e^{iB}|^2 = 2 + 2cos(A-B)


q("U14-A-028", TOPIC, "Sums of sines and cosines given", "Medium", "Multi-step computation MCQ",
  r"If $\sin\alpha + \sin\beta = \frac{1}{2}$ and $\cos\alpha + \cos\beta = \frac{1}{3}$, then $\cos(\alpha - \beta)$ equals",
  r"$-\frac{59}{72}$",
  [(r"$\frac{59}{72}$", r"Takes the sum of the squares to be $2 - 2\cos(\alpha - \beta)$ (sign slip in the cross terms)."),
   (r"$-\frac{23}{72}$", r"Takes the sum of the squares to be $1 + 2\cos(\alpha-\beta)$, counting $\sin^2 + \cos^2$ only once."),
   (r"$\frac{13}{72}$", r"Takes the sum of the squares to be $2\cos(\alpha-\beta)$, omitting the constant 2.")],
  r"Squaring and adding: $(\sin\alpha + \sin\beta)^2 + (\cos\alpha + \cos\beta)^2 = 2 + 2(\cos\alpha\cos\beta + \sin\alpha\sin\beta) = 2 + 2\cos(\alpha - \beta)$. So $\frac{1}{4} + \frac{1}{9} = \frac{13}{36} = 2 + 2\cos(\alpha - \beta)$, giving $\cos(\alpha-\beta) = -\frac{59}{72}$.",
  r"Losing the constant term when squaring and adding.",
  "U14-A-sum-sin-cos-given", "Square-and-add with careful bookkeeping.",
  check=_c028, values=[-Rational(59, 72), Rational(59, 72), -Rational(23, 72), Rational(13, 72)], cognitive="Application", source_class=SC)


def _c029():
    s = acos(Rational(4, 5))      # alpha + beta in (0, pi/2)
    d = asin(Rational(5, 13))     # alpha - beta in (-pi/4, pi/4)
    return simplify(expand_trig(tan(s + d)))


q("U14-A-029", TOPIC, "Splitting 2 alpha into sum and difference", "Medium", "Multi-step computation MCQ",
  r"If $\cos(\alpha + \beta) = \frac{4}{5}$ and $\sin(\alpha - \beta) = \frac{5}{13}$, where $0 < \alpha, \beta < \frac{\pi}{4}$, then $\tan 2\alpha$ equals",
  r"$\frac{56}{33}$",
  [(r"$\frac{16}{63}$", r"Computes $\tan[(\alpha+\beta) - (\alpha-\beta)] = \tan 2\beta$ instead of $\tan 2\alpha$."),
   (r"$\frac{8}{9}$", r"Uses $1 + \tan(\alpha+\beta)\tan(\alpha-\beta)$ in the denominator: $\frac{14/12}{63/48}$."),
   (r"$\frac{63}{16}$", r"Takes $\tan(\alpha+\beta) = \frac{4}{3}$ (inverting $\frac{\sin}{\cos}$), then $\frac{\frac{4}{3}+\frac{5}{12}}{1-\frac{5}{9}}$.")],
  r"Here $0 < \alpha + \beta < \frac{\pi}{2}$ and $-\frac{\pi}{4} < \alpha - \beta < \frac{\pi}{4}$, so $\tan(\alpha+\beta) = \frac{3}{4}$ and $\tan(\alpha-\beta) = \frac{5}{12}$. Then $\tan 2\alpha = \frac{\frac{3}{4} + \frac{5}{12}}{1 - \frac{3}{4}\cdot\frac{5}{12}} = \frac{14/12}{33/48} = \frac{56}{33}$.",
  r"Combining the two angles in the wrong order or with the wrong sign.",
  "U14-A-compound-split-angle", "Write $2\\alpha$ as a sum, find two tangents with quadrant care, combine.",
  check=_c029, values=[Rational(56, 33), Rational(16, 63), Rational(8, 9), Rational(63, 16)], cognitive="Application", source_class=SC)


def _c030():
    Bv = Integer(1)
    C = Symbol('C')
    Cv = nsolve(cos(pi - Bv - C) - cos(Bv) * cos(C), C, 0.9, prec=50)
    assert 0 < Cv < pi - 1
    return nsimplify(round(float(N(tan(Bv) * tan(Cv), 40)), 12))


q("U14-A-030", TOPIC, "Condition cos A = cos B cos C in a triangle", "Medium", "Inverse/parameter MCQ",
  r"If $A$, $B$, $C$ are the angles of a triangle such that $\cos A = \cos B\cos C$, then $\tan B\tan C$ equals",
  r"$2$",
  [(r"$\frac{1}{2}$", r"Derives $\sin B\sin C = 2\cos B\cos C$ but reports $\cot B\cot C$."),
   (r"$-2$", r"Expands $-\cos(B+C)$ as $-\cos B\cos C - \sin B\sin C$ (sign slip inside the compound formula), getting $\sin B\sin C = -2\cos B\cos C$."),
   (r"$1$", r"Writes $-\cos B\cos C + \sin B\sin C = \cos B\cos C$ and then loses one $\cos B\cos C$ term when transposing.")],
  r"$\cos A = -\cos(B + C) = -\cos B\cos C + \sin B\sin C$. Setting this equal to $\cos B\cos C$ gives $\sin B\sin C = 2\cos B\cos C$, so $\tan B\tan C = 2$.",
  r"Forgetting $\cos A = -\cos(B+C)$ in a triangle.",
  "U14-A-pi-cos-condition", "Allied angle plus compound angle, then rearrangement.",
  check=_c030, values=[2, Rational(1, 2), -2, 1], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $A$, $B$, $C$ are the angles of a triangle such that $\cos A = \cos B\cos C$, then the value of $\tan B\tan C$ is", answer=2))


_al = Integer(1)
_be = pi / 2 - _al
_ga = _al - _be


def _c031():
    return tan(_al)


q("U14-A-031", TOPIC, "Relation among tangents from angle conditions", "Medium", "Multi-step computation MCQ",
  r"If $\alpha + \beta = \frac{\pi}{2}$ and $\beta + \gamma = \alpha$, where all the tangents involved are defined, then $\tan\alpha$ equals",
  r"$\tan\beta + 2\tan\gamma$",
  [(r"$\tan\beta + \tan\gamma$", r"Uses $\tan\gamma = \tan\alpha - \tan\beta$, forgetting the denominator $1 + \tan\alpha\tan\beta = 2$."),
   (r"$2\tan\beta + \tan\gamma$", r"Reaches $\tan\gamma = \frac{\tan\alpha - \tan\beta}{2}$ but, clearing the 2, attaches it to $\tan\beta$ instead of $\tan\gamma$."),
   (r"$\tan\beta - 2\tan\gamma$", r"Takes $\gamma = \beta - \alpha$ (order reversed), so $\tan\gamma = \frac{\tan\beta - \tan\alpha}{2}$.")],
  r"$\gamma = \alpha - \beta$, so $\tan\gamma = \frac{\tan\alpha - \tan\beta}{1 + \tan\alpha\tan\beta}$. Since $\alpha + \beta = \frac{\pi}{2}$, $\tan\alpha\tan\beta = 1$, so $\tan\gamma = \frac{\tan\alpha - \tan\beta}{2}$, i.e. $\tan\alpha = \tan\beta + 2\tan\gamma$.",
  r"Not using $\tan\alpha\tan\beta = 1$ for complementary angles.",
  "U14-A-complementary-tan-relation", "Two conditions combined: complementary angles and a difference formula.",
  check=_c031, values=[tan(_be) + 2 * tan(_ga), tan(_be) + tan(_ga), 2 * tan(_be) + tan(_ga), tan(_be) - 2 * tan(_ga)],
  cognitive="Analysis", source_class=SC)


def _c032():
    return cos(2 * pi / 7) + cos(4 * pi / 7) + cos(6 * pi / 7)


q("U14-A-032", TOPIC, "Cosine sum by telescoping", "Medium", "Multi-step computation MCQ",
  r"The value of $\cos\frac{2\pi}{7} + \cos\frac{4\pi}{7} + \cos\frac{6\pi}{7}$ is",
  r"$-\frac{1}{2}$",
  [(r"$\frac{1}{2}$", r"Telescopes to $\sin\frac{\pi}{7} - \sin\pi$ instead of $\sin\pi - \sin\frac{\pi}{7}$ (sign slip in $2\sin A\cos B$)."),
   (r"$-1$", r"Multiplies by $\sin\frac{\pi}{7}$ but uses $\sin A\cos B = \sin(A+B) + \sin(A-B)$ without the $\frac{1}{2}$."),
   (r"$-\frac{1}{4}$", r"Multiplies by $2\sin\frac{\pi}{7}$ and also inserts an extra $\frac{1}{2}$ when converting each product.")],
  r"Let $S$ be the sum. Using $2\sin\frac{\pi}{7}\cos\frac{2k\pi}{7} = \sin\frac{(2k+1)\pi}{7} - \sin\frac{(2k-1)\pi}{7}$ for $k = 1, 2, 3$, the terms telescope: $2\sin\frac{\pi}{7}\, S = \sin\pi - \sin\frac{\pi}{7} = -\sin\frac{\pi}{7}$. Hence $S = -\frac{1}{2}$.",
  r"Losing the factor 2 or the sign in the product-to-sum step.",
  "U14-A-cos-sum-sevenths", "Choosing the multiplier $2\\sin(\\pi/7)$ and telescoping three products.",
  check=_c032, values=[-Rational(1, 2), Rational(1, 2), -1, -Rational(1, 4)], cognitive="Application", source_class=SC)


def _c033():
    return nsimplify(simplify(sum(sin(k * pi / 8) ** 4 for k in (1, 3, 5, 7))))


q("U14-A-033", TOPIC, "Fourth powers at odd multiples of pi/8", "Medium", "Multi-step computation MCQ",
  r"The value of $\sin^4\frac{\pi}{8} + \sin^4\frac{3\pi}{8} + \sin^4\frac{5\pi}{8} + \sin^4\frac{7\pi}{8}$ is",
  r"$\frac{3}{2}$",
  [(r"$2$", r"Reduces correctly to $2\left(\sin^4\frac{\pi}{8} + \cos^4\frac{\pi}{8}\right)$ but treats the bracket as $(\sin^2 + \cos^2)^2 = 1$."),
   (r"$1$", r"Writes $\sin^4 x + \cos^4 x = 1 - \sin^2 2x$, getting $2\left(1 - \frac{1}{2}\right)$."),
   (r"$\frac{7}{4}$", r"Writes $\sin^4 x + \cos^4 x = 1 - \frac{1}{4}\sin^2 2x$, getting $2\left(1 - \frac{1}{8}\right)$.")],
  r"$\sin\frac{7\pi}{8} = \sin\frac{\pi}{8}$, $\sin\frac{5\pi}{8} = \sin\frac{3\pi}{8} = \cos\frac{\pi}{8}$. So the sum is $2\left(\sin^4\frac{\pi}{8} + \cos^4\frac{\pi}{8}\right) = 2\left(1 - \frac{1}{2}\sin^2\frac{\pi}{4}\right) = 2\cdot\frac{3}{4} = \frac{3}{2}$.",
  r"Losing the factor $\frac{1}{2}$ in $2\sin^2x\cos^2x = \frac{1}{2}\sin^2 2x$.",
  "U14-A-sin4-cos4", "Allied-angle reduction of four terms, then the fourth-power identity.",
  check=_c033, values=[Rational(3, 2), 2, 1, Rational(7, 4)], cognitive="Application", source_class=SC)


def _c034():
    S = Symbol('S', positive=True)
    th = Symbol('th')
    ratio = expand_trig(sin(3 * th)) / sin(th)
    ratio = simplify(ratio).subs(cos(th) ** 2, 1 - sin(th) ** 2).subs(sin(th), S)
    s2 = solve(Eq(simplify(ratio), Rational(11, 9)), S)
    vals = set(simplify(1 - 8 * s ** 2 * (1 - s ** 2)) for s in s2)
    assert len(vals) == 1
    return vals.pop()


q("U14-A-034", TOPIC, "From sin 3x / sin x to cos 4x", "Medium", "Multi-step computation MCQ",
  r"If $\frac{\sin 3\theta}{\sin\theta} = \frac{11}{9}$, then $\cos 4\theta$ equals",
  r"$-\frac{79}{81}$",
  [(r"$\frac{1}{9}$", r"Finds $\cos 2\theta = \frac{1}{9}$ and stops there."),
   (r"$\frac{79}{81}$", r"Uses $\cos 4\theta = 1 - 2\cos^2 2\theta$ (sign slip in the double angle formula)."),
   (r"$-\frac{7}{9}$", r"Treats $\cos 4\theta$ as $2\cos 2\theta - 1$, i.e. forgets to square.")],
  r"$\frac{\sin 3\theta}{\sin\theta} = 3 - 4\sin^2\theta = 1 + 2\cos 2\theta$. So $1 + 2\cos 2\theta = \frac{11}{9}$ gives $\cos 2\theta = \frac{1}{9}$. Then $\cos 4\theta = 2\cos^2 2\theta - 1 = \frac{2}{81} - 1 = -\frac{79}{81}$.",
  r"Stopping at $\cos 2\theta$ or misusing the double angle formula.",
  "U14-A-triple-ratio", "Triple angle, rewrite in $\\cos 2\\theta$, then double angle again.",
  check=_c034, values=[-Rational(79, 81), Rational(1, 9), Rational(79, 81), -Rational(7, 9)], cognitive="Application", source_class=SC)


def _c035():
    return nsimplify(simplify(tan(dg(9)) - tan(dg(27)) - tan(dg(63)) + tan(dg(81))))


q("U14-A-035", TOPIC, "tan + cot pairs with 18 and 54 degrees", "Medium", "Multi-step computation MCQ",
  r"The value of $\tan 9^\circ - \tan 27^\circ - \tan 63^\circ + \tan 81^\circ$ is",
  r"$4$",
  [(r"$2$", r"Uses $\tan\theta + \cot\theta = \frac{1}{\sin 2\theta}$: $\frac{1}{\sin 18^\circ} - \frac{1}{\sin 54^\circ} = (\sqrt{5}+1) - (\sqrt{5}-1)$."),
   (r"$4\sqrt{5}$", r"Sign slip: adds the two groups, $2(\sqrt{5}+1) + 2(\sqrt{5}-1)$."),
   (r"$8$", r"Uses $\tan\theta + \cot\theta = \frac{4}{\sin 2\theta}$: $4(\sqrt{5}+1) - 4(\sqrt{5}-1)$.")],
  r"Since $\tan 81^\circ = \cot 9^\circ$ and $\tan 63^\circ = \cot 27^\circ$, the value is $(\tan 9^\circ + \cot 9^\circ) - (\tan 27^\circ + \cot 27^\circ) = \frac{2}{\sin 18^\circ} - \frac{2}{\sin 54^\circ} = \frac{8}{\sqrt{5}-1} - \frac{8}{\sqrt{5}+1} = 2(\sqrt{5}+1) - 2(\sqrt{5}-1) = 4$.",
  r"Losing the factor 2 in $\tan\theta + \cot\theta = \frac{2}{\sin 2\theta}$.",
  "U14-A-tan-cot-pairs", "Complementary pairing, a double-angle identity and two special values.",
  check=_c035, values=[4, 2, 4 * sqrt(5), 8], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The value of $\tan 9^\circ - \tan 27^\circ - \tan 63^\circ + \tan 81^\circ$ is", answer=4))


def _c036():
    s1 = close(tan(dg(70)), tan(dg(20)) + 2 * tan(dg(50)))
    s2 = close(cos(dg(10)) * cos(dg(50)) * cos(dg(70)), sqrt(3) / 8)
    return (bool(s1), bool(s2))


q("U14-A-036", TOPIC, "Special-angle identities", "Medium", "Statement-based MCQ",
  r"Statement I: $\tan 70^\circ = \tan 20^\circ + 2\tan 50^\circ$. Statement II: $\cos 10^\circ\cos 50^\circ\cos 70^\circ = \frac{\sqrt{3}}{8}$." + TAIL,
  ST_TT,
  [(ST_TF, r"Accepts Statement I but uses the value $\frac{1}{8}$ of $\cos 20^\circ\cos 40^\circ\cos 80^\circ$ for the product in Statement II."),
   (ST_FT, r"Rejects Statement I by treating $\tan 70^\circ - \tan 20^\circ$ as $\tan 50^\circ$ (difference of tangents as tangent of difference)."),
   (ST_FF, r"Makes both of the above slips.")],
  r"Statement I: $\tan 70^\circ = \tan(50^\circ + 20^\circ) = \frac{\tan 50^\circ + \tan 20^\circ}{1 - \tan 50^\circ\tan 20^\circ}$ and $\tan 70^\circ\tan 20^\circ = 1$, so $\tan 70^\circ - \tan 50^\circ\tan 20^\circ\tan 70^\circ = \tan 50^\circ + \tan 20^\circ$ becomes $\tan 70^\circ = \tan 20^\circ + 2\tan 50^\circ$; true. Statement II: $\cos\theta\cos(60^\circ - \theta)\cos(60^\circ + \theta) = \frac{1}{4}\cos 3\theta$ with $\theta = 10^\circ$ gives $\frac{1}{4}\cos 30^\circ = \frac{\sqrt{3}}{8}$; true.",
  r"Confusing the triple-product values for $10^\circ$ and $20^\circ$.",
  "U14-A-statement-special-products", "Two separate identities to verify, each needing a non-obvious step.",
  check=_c036, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Analysis", source_class=SC)


def _c037():
    s1 = close(sin(dg(10)) ** 3 + sin(dg(50)) ** 3 - sin(dg(70)) ** 3, -Rational(1, 8))
    th = Symbol('th')
    s2 = all(close(sin(v) ** 3, (3 * sin(v) - sin(3 * v)) / 4) for v in (Rational(3, 10), Rational(17, 7), -Rational(5, 4)))
    s2 = s2 and simplify(expand_trig(sin(th) ** 3 - (3 * sin(th) - sin(3 * th)) / 4)) == 0
    return (bool(s1), bool(s2))


q("U14-A-037", TOPIC, "Cubes of sines via the triple angle formula", "Medium", "Statement-based MCQ",
  r"Statement I: $\sin^3 10^\circ + \sin^3 50^\circ - \sin^3 70^\circ = -\frac{1}{8}$. Statement II: $\sin^3\theta = \frac{3\sin\theta - \sin 3\theta}{4}$ for every real $\theta$." + TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement II and uses it, but takes $\sin 210^\circ = \frac{1}{2}$ (sign slip), so the constant part becomes $-\frac{1}{4}\left(\frac{1}{2} + \frac{1}{2} - \frac{1}{2}\right) = -\frac{1}{8}$ and Statement I is accepted."),
   (ST_TF, r"Makes the same $\sin 210^\circ$ slip in Statement I, and rejects Statement II by mixing it up with $\cos 3\theta = 4\cos^3\theta - 3\cos\theta$, believing $\sin^3\theta = \frac{\sin 3\theta + 3\sin\theta}{4}$."),
   (ST_FF, r"Evaluates Statement I correctly as $-\frac{3}{8}$ but rejects Statement II, believing $\sin^3\theta = \frac{\sin 3\theta + 3\sin\theta}{4}$ by analogy with $\cos 3\theta = 4\cos^3\theta - 3\cos\theta$.")],
  r"Statement II: $\sin 3\theta = 3\sin\theta - 4\sin^3\theta$ for all real $\theta$, so $\sin^3\theta = \frac{3\sin\theta - \sin 3\theta}{4}$; true. Statement I: the expression equals $\frac{3}{4}(\sin 10^\circ + \sin 50^\circ - \sin 70^\circ) - \frac{1}{4}(\sin 30^\circ + \sin 150^\circ - \sin 210^\circ)$. Here $\sin 10^\circ + \sin 50^\circ = 2\sin 30^\circ\cos 20^\circ = \sin 70^\circ$, so the first bracket is $0$, and the second bracket is $\frac{1}{2} + \frac{1}{2} + \frac{1}{2} = \frac{3}{2}$. The value is $-\frac{3}{8}$, not $-\frac{1}{8}$; false.",
  r"Taking $\sin 210^\circ$ as positive, or confusing the sine and cosine triple-angle formulas.",
  "U14-A-statement-sine-cubes", r"Triple angle formula applied to three cubes, a sum-to-product cancellation and a sign trap at $210^\circ$.",
  check=_c037, values=[(False, True), (True, True), (True, False), (False, False)], cognitive="Analysis", source_class=SC)


def _c038():
    A1 = Rational(3, 10)
    B1 = pi / 4 - A1
    s1 = close((cot(A1) - 1) * (cot(B1) - 1), 2)
    A2 = Rational(1, 5)
    B2 = 3 * pi / 4 - A2
    s2 = close((1 - tan(A2)) * (1 - tan(B2)), 1)
    return (bool(s1), bool(s2))


q("U14-A-038", TOPIC, "Products (cot A - 1)(cot B - 1) and (1 - tan A)(1 - tan B)", "Medium", "Statement-based MCQ",
  r"Assume all tangents and cotangents involved are defined. Statement I: If $A + B = \frac{\pi}{4}$, then $(\cot A - 1)(\cot B - 1) = 2$. Statement II: If $A + B = \frac{3\pi}{4}$, then $(1 - \tan A)(1 - \tan B) = 1$." + TAIL,
  ST_TF,
  [(ST_TT, r"Evaluates Statement I correctly as 2, but in Statement II expands $(1-\tan A)(1-\tan B)$, substitutes $\tan A + \tan B = -(1 - \tan A\tan B)$ and drops the leading 1, getting 1."),
   (ST_FF, r"In Statement I expands $\cot A\cot B - (\cot A + \cot B) + 1$, substitutes $\cot A + \cot B = \cot A\cot B - 1$ and drops the trailing $+1$, getting 1; evaluates Statement II correctly as 2."),
   (ST_FT, r"Drops the constant 1 in both expansions, getting 1 in each, so rejects Statement I and accepts Statement II.")],
  r"If $A + B = \frac{\pi}{4}$: $\cot(A+B) = \frac{\cot A\cot B - 1}{\cot A + \cot B} = 1$, so $\cot A + \cot B = \cot A\cot B - 1$ and $(\cot A - 1)(\cot B - 1) = \cot A\cot B - (\cot A\cot B - 1) + 1 = 2$; Statement I is true. If $A + B = \frac{3\pi}{4}$: $\tan(A+B) = -1$ gives $\tan A + \tan B = -(1 - \tan A\tan B)$, so $(1 - \tan A)(1 - \tan B) = 1 - (\tan A + \tan B) + \tan A\tan B = 1 + 1 - \tan A\tan B + \tan A\tan B = 2$; Statement II is false.",
  r"Dropping the constant 1 when expanding the product.",
  "U14-A-statement-tan-products", "Two compound-angle consequences (one in cotangents) to evaluate, both with the same trap.",
  check=_c038, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Analysis", source_class=SC)


def _c039():
    sv, cv = symbols('sv cv', real=True)
    sols = solve([sv + cv - Rational(1, 5), sv ** 2 + cv ** 2 - 1], [sv, cv], dict=True)
    sols = [d for d in sols if d[sv] > 0]          # 0 < theta < pi
    assert len(sols) == 1
    d = sols[0]
    return simplify((1 - d[cv]) / d[sv])


q("U14-A-039", TOPIC, "Half angle from sin + cos", "Medium", "Multi-step computation MCQ",
  r"If $\sin\theta + \cos\theta = \frac{1}{5}$ and $0 < \theta < \pi$, then $\tan\frac{\theta}{2}$ equals",
  r"$2$",
  [(r"$\frac{1}{2}$", r"Uses $\frac{1+\cos\theta}{\sin\theta}$, which is $\cot\frac{\theta}{2}$."),
   (r"$3$", r"Assigns $\sin\theta = \frac{3}{5}$, $\cos\theta = -\frac{4}{5}$ without checking the given sum, then $\frac{1 + 4/5}{3/5}$."),
   (r"$\frac{1}{3}$", r"Assigns $\sin\theta = \frac{3}{5}$, $\cos\theta = -\frac{4}{5}$ and also uses $\frac{1+\cos\theta}{\sin\theta}$.")],
  r"Squaring, $1 + 2\sin\theta\cos\theta = \frac{1}{25}$, so $\sin\theta\cos\theta = -\frac{12}{25}$; thus $\sin\theta, \cos\theta$ are the roots of $u^2 - \frac{1}{5}u - \frac{12}{25} = 0$, namely $\frac{4}{5}$ and $-\frac{3}{5}$. As $\sin\theta > 0$, $\sin\theta = \frac{4}{5}$, $\cos\theta = -\frac{3}{5}$. Then $\tan\frac{\theta}{2} = \frac{1-\cos\theta}{\sin\theta} = \frac{8/5}{4/5} = 2$.",
  r"Assigning the two values to $\sin\theta$ and $\cos\theta$ the wrong way round.",
  "U14-A-sin-plus-cos-half-angle", "Solve for both ratios with a sign decision, then a half angle formula.",
  check=_c039, values=[2, Rational(1, 2), 3, Rational(1, 3)], cognitive="Application", source_class=SC)


_a, _b = symbols('a b')


def _c040():
    c = (cos(_a) - cos(_b)) / (1 - cos(_a) * cos(_b))
    return (1 - c) / (1 + c)


q("U14-A-040", TOPIC, "Half angle relation from a cosine condition", "Medium", "Multi-step computation MCQ",
  r"If $\cos\theta = \frac{\cos\alpha - \cos\beta}{1 - \cos\alpha\cos\beta}$, where all the expressions involved are defined, then $\tan^2\frac{\theta}{2}$ equals",
  r"$\tan^2\frac{\alpha}{2}\cot^2\frac{\beta}{2}$",
  [(r"$\tan^2\frac{\alpha}{2}\tan^2\frac{\beta}{2}$", r"Factorises $1 - \cos\alpha + \cos\beta - \cos\alpha\cos\beta$ as $(1-\cos\alpha)(1-\cos\beta)$ and the denominator as $(1+\cos\alpha)(1+\cos\beta)$ (sign slips)."),
   (r"$\cot^2\frac{\alpha}{2}\tan^2\frac{\beta}{2}$", r"Uses $\tan^2\frac{\theta}{2} = \frac{1+\cos\theta}{1-\cos\theta}$ (inverted half angle formula)."),
   (r"$\cot^2\frac{\alpha}{2}\cot^2\frac{\beta}{2}$", r"Makes both the inverted half angle formula and the factorising sign slips.")],
  r"$\tan^2\frac{\theta}{2} = \frac{1-\cos\theta}{1+\cos\theta} = \frac{1 - \cos\alpha\cos\beta - \cos\alpha + \cos\beta}{1 - \cos\alpha\cos\beta + \cos\alpha - \cos\beta} = \frac{(1-\cos\alpha)(1+\cos\beta)}{(1+\cos\alpha)(1-\cos\beta)} = \tan^2\frac{\alpha}{2}\cot^2\frac{\beta}{2}$.",
  r"Factorising the numerator and denominator with wrong signs.",
  "U14-A-half-angle-condition", "Half angle formula plus a non-obvious factorisation.",
  check=_c040, values=[tan(_a / 2) ** 2 * cot(_b / 2) ** 2, tan(_a / 2) ** 2 * tan(_b / 2) ** 2,
                       cot(_a / 2) ** 2 * tan(_b / 2) ** 2, cot(_a / 2) ** 2 * cot(_b / 2) ** 2],
  cognitive="Application", source_class=SC)


def _c041():
    return nsimplify(simplify(1 / sin(dg(10)) - sqrt(3) / cos(dg(10))))


q("U14-A-041", TOPIC, "Combining into a single sine", "Medium", "Multi-step computation MCQ",
  r"The value of $\frac{1}{\sin 10^\circ} - \frac{\sqrt{3}}{\cos 10^\circ}$ is",
  r"$4$",
  [(r"$2$", r"Writes $\sin 10^\circ\cos 10^\circ = \sin 20^\circ$, missing the factor $\frac{1}{2}$."),
   (r"$1$", r"Misses both factors of 2: writes $\cos 10^\circ - \sqrt{3}\sin 10^\circ = \sin 20^\circ$ and $\sin 10^\circ\cos 10^\circ = \sin 20^\circ$."),
   (r"$8$", r"Writes $\sin 10^\circ\cos 10^\circ = \frac{1}{4}\sin 20^\circ$.")],
  r"The expression is $\frac{\cos 10^\circ - \sqrt{3}\sin 10^\circ}{\sin 10^\circ\cos 10^\circ}$. The numerator is $2\left(\frac{1}{2}\cos 10^\circ - \frac{\sqrt{3}}{2}\sin 10^\circ\right) = 2\sin(30^\circ - 10^\circ) = 2\sin 20^\circ$, and the denominator is $\frac{1}{2}\sin 20^\circ$. So the value is $4$.",
  r"Losing factors of 2 when combining $a\cos x - b\sin x$ and in $\sin x\cos x$.",
  "U14-A-auxiliary-angle-value", "Combine two terms via a compound angle, then a double angle in the denominator.",
  check=_c041, values=[4, 2, 1, 8], cognitive="Application", source_class=SC,
  numerical=dict(question=r"The value of $\frac{1}{\sin 10^\circ} - \frac{\sqrt{3}}{\cos 10^\circ}$ is", answer=4))


def _c042():
    A = Rational(2, 5)
    B = atan(1 / (3 * tan(A)))          # any A, B with 3 tan A tan B = 1
    assert close(3 * tan(A) * tan(B), 1)
    return nsimplify(round(float(N(cos(A - B) / cos(A + B), 40)), 12))


q("U14-A-042", TOPIC, "Ratio of cos(A - B) to cos(A + B)", "Medium", "Multi-step computation MCQ",
  r"If $3\tan A\tan B = 1$, then $\frac{\cos(A - B)}{\cos(A + B)}$ equals",
  r"$2$",
  [(r"$\frac{1}{2}$", r"Interchanges the expansions of $\cos(A-B)$ and $\cos(A+B)$, obtaining $\frac{1 - \tan A\tan B}{1 + \tan A\tan B}$."),
   (r"$-2$", r"Reads the condition as $\tan A\tan B = 3$, giving $\frac{1+3}{1-3}$."),
   (r"$\frac{4}{3}$", r"Divides only the numerator by $\cos A\cos B$, reporting $1 + \tan A\tan B$.")],
  r"Dividing numerator and denominator by $\cos A\cos B$: $\frac{\cos(A-B)}{\cos(A+B)} = \frac{1 + \tan A\tan B}{1 - \tan A\tan B} = \frac{1 + \frac{1}{3}}{1 - \frac{1}{3}} = 2$.",
  r"Mixing up the signs in the expansions of $\cos(A \pm B)$.",
  "U14-A-cos-ratio-tan-product", "Two compound-angle expansions and a division by $\\cos A\\cos B$.",
  check=_c042, values=[2, Rational(1, 2), -2, Rational(4, 3)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"If $3\tan A\tan B = 1$, then the value of $\frac{\cos(A - B)}{\cos(A + B)}$ is", answer=2))


# ================================================================ DIFFICULT (13)


def _c043():
    return nsimplify(round(float(N(1 / (sin(pi / 14) * sin(3 * pi / 14) * sin(5 * pi / 14)), 40)), 12))


q("U14-A-043", TOPIC, "Sine product at odd multiples of pi/14", "Difficult", "Multi-step computation MCQ",
  r"The value of $\frac{1}{\sin\frac{\pi}{14}\sin\frac{3\pi}{14}\sin\frac{5\pi}{14}}$ is",
  r"$8$",
  [(r"$\frac{1}{8}$", r"Evaluates the product $\sin\frac{\pi}{14}\sin\frac{3\pi}{14}\sin\frac{5\pi}{14} = \frac{1}{8}$ correctly but forgets to take the reciprocal."),
   (r"$16$", r"Uses $2^4$ in the telescoping denominator for three factors."),
   (r"$4$", r"Uses $2^2$ in the telescoping denominator for three factors.")],
  r"$\sin\frac{\pi}{14} = \cos\frac{3\pi}{7}$, $\sin\frac{3\pi}{14} = \cos\frac{2\pi}{7}$, $\sin\frac{5\pi}{14} = \cos\frac{\pi}{7}$. Since $\cos\frac{3\pi}{7} = -\cos\frac{4\pi}{7}$, the product is $-\cos\frac{\pi}{7}\cos\frac{2\pi}{7}\cos\frac{4\pi}{7} = -\frac{\sin(8\pi/7)}{8\sin(\pi/7)} = -\left(-\frac{1}{8}\right) = \frac{1}{8}$. The required value is $8$.",
  r"Losing a sign when converting $\cos\frac{3\pi}{7}$ to $\cos\frac{4\pi}{7}$ or in $\sin\frac{8\pi}{7}$.",
  "U14-A-sine-product-sevenths", "Complementary conversion, a supplementary-angle sign and telescoping, with two sign traps.",
  check=_c043, values=[8, Rational(1, 8), 16, 4], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The value of $\frac{1}{\sin\frac{\pi}{14}\sin\frac{3\pi}{14}\sin\frac{5\pi}{14}}$ is", answer=8))


def _c044():
    y = Integer(2)
    x = Symbol('x')
    xv = nsolve(2 / cos(x) - 1 / cos(x - y) - 1 / cos(x + y), x, 0.7, prec=50)
    return nsimplify(round(float(N(cos(xv) ** 2 / cos(y / 2) ** 2, 40)), 12))


q("U14-A-044", TOPIC, "Harmonic progression of cosines", "Difficult", "Inverse/parameter MCQ",
  r"If $\cos(x - y)$, $\cos x$ and $\cos(x + y)$ are in harmonic progression (all non-zero) and $\cos y \ne 1$, then $\cos^2 x = k\cos^2\frac{y}{2}$, where $k$ equals",
  r"$2$",
  [(r"$1$", r"Reaches $\cos^2 x = 1 + \cos y$ and then takes $1 + \cos y = \cos^2\frac{y}{2}$."),
   (r"$\frac{1}{2}$", r"Reaches $\cos^2 x = 1 + \cos y$ and then uses $\cos^2\frac{y}{2} = 2(1 + \cos y)$ (inverted half angle relation)."),
   (r"$\sqrt{2}$", r"Takes square roots too early and reports the value of $|\cos x \sec\frac{y}{2}|$ instead of $k$.")],
  r"HP means $\cos x = \frac{2\cos(x-y)\cos(x+y)}{\cos(x-y) + \cos(x+y)} = \frac{2(\cos^2 x - \sin^2 y)}{2\cos x\cos y}$. So $\cos^2 x\cos y = \cos^2 x - \sin^2 y$, i.e. $\cos^2 x(1 - \cos y) = (1-\cos y)(1+\cos y)$. As $\cos y \ne 1$, $\cos^2 x = 1 + \cos y = 2\cos^2\frac{y}{2}$, so $k = 2$.",
  r"Misremembering $1 + \cos y = 2\cos^2\frac{y}{2}$.",
  "U14-A-hp-cos-condition", "HP condition, product-to-sum, cancellation of $1-\\cos y$, then a half angle identity.",
  check=_c044, values=[2, 1, Rational(1, 2), sqrt(2)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"If $\cos(x - y)$, $\cos x$ and $\cos(x + y)$ are in harmonic progression (all non-zero), $\cos y \ne 1$, and $\cos^2 x = k\cos^2\frac{y}{2}$, then the value of $k$ is", answer=2))


def _c045():
    # identity cotA cotB + cotB cotC + cotC cotA = 1 for a triangle (checked numerically)
    A, B = Rational(7, 10), Rational(6, 5)
    C = pi - A - B
    assert close(cot(A) * cot(B) + cot(B) * cot(C) + cot(C) * cot(A), 1)
    # (sum cot)^2 - 3 = (1/2) * sum (cotA - cotB)^2 = 0  => all cot equal, sum = sqrt(3)
    c = Symbol('c')
    cv = solve(Eq(3 * c, sqrt(3)), c)[0]
    ang = acot(cv)
    assert close(3 * ang, pi)
    return nsimplify(simplify(3 * sin(ang) ** 2))


q("U14-A-045", TOPIC, "Equality case of a conditional identity", "Difficult", "Multi-step computation MCQ",
  r"If $A$, $B$, $C$ are the angles of a triangle and $\cot A + \cot B + \cot C = \sqrt{3}$, then $\sin^2 A + \sin^2 B + \sin^2 C$ equals",
  r"$\frac{9}{4}$",
  [(r"$\frac{7}{4}$", r"Identifies the equilateral triangle but uses $\sin^2 A + \sin^2 B + \sin^2 C = 2 - 2\cos A\cos B\cos C$ with $\cos A\cos B\cos C = \frac{1}{8}$."),
   (r"$\frac{17}{8}$", r"Uses $2 + \cos A\cos B\cos C$, dropping the factor 2 in the identity."),
   (r"$\frac{3}{4}$", r"Identifies the equilateral triangle but takes $\sin 60^\circ = \frac{1}{2}$.")],
  r"For a triangle, $\cot A\cot B + \cot B\cot C + \cot C\cot A = 1$. Then $(\cot A + \cot B + \cot C)^2 - 3 = \frac{1}{2}\left[(\cot A - \cot B)^2 + (\cot B - \cot C)^2 + (\cot C - \cot A)^2\right]$, and the left side is $3 - 3 = 0$, so all three cotangents are equal, each $\frac{1}{\sqrt{3}}$. Hence $A = B = C = \frac{\pi}{3}$ and the sum is $3\cdot\frac{3}{4} = \frac{9}{4}$.",
  r"Not recognising that equality forces an equilateral triangle, or misusing $\sin^2$ identities.",
  "U14-A-cot-sum-equilateral", "Conditional identity plus a sum-of-squares argument, then evaluation.",
  check=_c045, values=[Rational(9, 4), Rational(7, 4), Rational(17, 8), Rational(3, 4)], cognitive="Analysis", source_class=SC)


def _c046():
    return (1 + sec(pi / 16)) * (1 + sec(pi / 8)) * (1 + sec(pi / 4))


q("U14-A-046", TOPIC, "Telescoping product (1 + sec x)", "Difficult", "Multi-step computation MCQ",
  r"The value of $\left(1 + \sec\frac{\pi}{16}\right)\left(1 + \sec\frac{\pi}{8}\right)\left(1 + \sec\frac{\pi}{4}\right)$ is",
  r"$\cot\frac{\pi}{32}$",
  [(r"$\cot\frac{\pi}{16}$", r"Telescopes using $1 + \sec x = \frac{\tan x}{\tan(x/2)}$ but leaves out the first factor, getting $\frac{\tan(\pi/4)}{\tan(\pi/16)}$."),
   (r"$\tan\frac{\pi}{32}$", r"Uses the inverted relation $1 + \sec x = \frac{\tan(x/2)}{\tan x}$."),
   (r"$\frac{1}{\sqrt{2}}\cot\frac{\pi}{32}$", r"Telescopes the first two factors to $\frac{\tan(\pi/8)}{\tan(\pi/32)}$ but evaluates the last factor with $\sec\frac{\pi}{4} = \frac{1}{\sqrt{2}}$.")],
  r"$1 + \sec x = \frac{1+\cos x}{\cos x} = \frac{2\cos^2(x/2)}{\cos x} = \frac{\tan x}{\tan(x/2)}$. So the product is $\frac{\tan(\pi/16)}{\tan(\pi/32)}\cdot\frac{\tan(\pi/8)}{\tan(\pi/16)}\cdot\frac{\tan(\pi/4)}{\tan(\pi/8)} = \frac{1}{\tan(\pi/32)} = \cot\frac{\pi}{32}$.",
  r"Not spotting the telescoping form $1 + \sec x = \frac{\tan x}{\tan(x/2)}$.",
  "U14-A-one-plus-sec-product", "Requires discovering a non-standard telescoping identity.",
  check=_c046, values=[cot(pi / 32), cot(pi / 16), tan(pi / 32), cot(pi / 32) / sqrt(2)], cognitive="Analysis", source_class=SC)


def _c047():
    return cos(pi / 7) - cos(2 * pi / 7) + cos(3 * pi / 7)


q("U14-A-047", TOPIC, "Alternating cosine sum", "Difficult", "Multi-step computation MCQ",
  r"The value of $\cos\frac{\pi}{7} - \cos\frac{2\pi}{7} + \cos\frac{3\pi}{7}$ is",
  r"$\frac{1}{2}$",
  [(r"$1$", r"Multiplies by $\sin\frac{\pi}{7}$ and uses $\sin A\cos B = \sin(A+B) + \sin(A-B)$ without the $\frac{1}{2}$."),
   (r"$-\frac{1}{2}$", r"Telescopes to $\sin\frac{6\pi}{7}$ but takes $\sin\frac{6\pi}{7} = -\sin\frac{\pi}{7}$."),
   (r"$\frac{1}{4}$", r"Multiplies by $2\sin\frac{\pi}{7}$ and also inserts an extra $\frac{1}{2}$ when converting each product.")],
  r"Since $-\cos\frac{2\pi}{7} = \cos\frac{5\pi}{7}$, the sum $S = \cos\frac{\pi}{7} + \cos\frac{3\pi}{7} + \cos\frac{5\pi}{7}$. Then $2\sin\frac{\pi}{7}\,S = \sin\frac{2\pi}{7} + \left(\sin\frac{4\pi}{7} - \sin\frac{2\pi}{7}\right) + \left(\sin\frac{6\pi}{7} - \sin\frac{4\pi}{7}\right) = \sin\frac{6\pi}{7} = \sin\frac{\pi}{7}$. Hence $S = \frac{1}{2}$.",
  r"Not converting $-\cos\frac{2\pi}{7}$ into $\cos\frac{5\pi}{7}$, or sign slips in $\sin\frac{6\pi}{7}$.",
  "U14-A-cos-sum-sevenths", "Allied-angle rewrite to an arithmetic progression of angles, then telescoping.",
  check=_c047, values=[Rational(1, 2), 1, -Rational(1, 2), Rational(1, 4)], cognitive="Analysis", source_class=SC)


def _c048():
    return nsimplify(round(float(N(sum(tan(k * pi / 16) ** 2 for k in (1, 3, 5, 7)), 40)), 12))


q("U14-A-048", TOPIC, "Sum of squares of tangents at odd multiples of pi/16", "Difficult", "Multi-step computation MCQ",
  r"The value of $\tan^2\frac{\pi}{16} + \tan^2\frac{3\pi}{16} + \tan^2\frac{5\pi}{16} + \tan^2\frac{7\pi}{16}$ is",
  r"$28$",
  [(r"$32$", r"Pairs into $(\tan x + \cot x)^2$ terms but forgets to subtract $2$ from each pair."),
   (r"$24$", r"Uses $\tan^2 x + \cot^2 x = (\tan x + \cot x)^2 - 4$, subtracting 4 per pair."),
   (r"$4$", r"Uses $\tan x + \cot x = \frac{1}{\sin 2x}$, which gives $\frac{1}{\sin^2(\pi/8)\cos^2(\pi/8)} - 4 = 8 - 4$.")],
  r"Since $\tan\frac{7\pi}{16} = \cot\frac{\pi}{16}$ and $\tan\frac{5\pi}{16} = \cot\frac{3\pi}{16}$, use $\tan^2 x + \cot^2 x = (\tan x + \cot x)^2 - 2 = \frac{4}{\sin^2 2x} - 2$. The sum is $\frac{4}{\sin^2(\pi/8)} + \frac{4}{\cos^2(\pi/8)} - 4 = \frac{4}{\sin^2(\pi/8)\cos^2(\pi/8)} - 4 = \frac{16}{\sin^2(\pi/4)} - 4 = 32 - 4 = 28$.",
  r"Forgetting the $-2$ in $\tan^2 x + \cot^2 x = (\tan x + \cot x)^2 - 2$.",
  "U14-A-tan-square-sixteenths", "Complementary pairing, a square identity, a double-angle step and a second pairing.",
  check=_c048, values=[28, 32, 24, 4], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The value of $\tan^2\frac{\pi}{16} + \tan^2\frac{3\pi}{16} + \tan^2\frac{5\pi}{16} + \tan^2\frac{7\pi}{16}$ is", answer=28))


def _c049():
    return Mul(*[1 + cos(k * pi / 8) for k in (1, 3, 5, 7)])


q("U14-A-049", TOPIC, "Product of (1 + cos) at odd multiples of pi/8", "Difficult", "Multi-step computation MCQ",
  r"The value of $\left(1 + \cos\frac{\pi}{8}\right)\left(1 + \cos\frac{3\pi}{8}\right)\left(1 + \cos\frac{5\pi}{8}\right)\left(1 + \cos\frac{7\pi}{8}\right)$ is",
  r"$\frac{1}{8}$",
  [(r"$\frac{1}{4}$", r"Reaches $\sin^2\frac{\pi}{8}\cos^2\frac{\pi}{8}$ but writes it as $\frac{1}{2}\sin^2\frac{\pi}{4}$."),
   (r"$\frac{1}{16}$", r"Reaches $\frac{1}{4}\sin^2\frac{\pi}{4}$ but takes $\sin\frac{\pi}{4} = \frac{1}{2}$."),
   (r"$\frac{\sqrt{2}}{4}$", r"Drops the squares, computing $\sin\frac{\pi}{8}\cos\frac{\pi}{8} = \frac{1}{2}\sin\frac{\pi}{4}$.")],
  r"$\cos\frac{7\pi}{8} = -\cos\frac{\pi}{8}$ and $\cos\frac{5\pi}{8} = -\cos\frac{3\pi}{8}$, so the product is $\left(1 - \cos^2\frac{\pi}{8}\right)\left(1 - \cos^2\frac{3\pi}{8}\right) = \sin^2\frac{\pi}{8}\sin^2\frac{3\pi}{8} = \sin^2\frac{\pi}{8}\cos^2\frac{\pi}{8} = \frac{1}{4}\sin^2\frac{\pi}{4} = \frac{1}{8}$.",
  r"Losing a factor in $\sin^2 x\cos^2 x = \frac{1}{4}\sin^2 2x$.",
  "U14-A-one-plus-cos-product", "Allied-angle pairing, difference of squares, complementary angles and a double angle.",
  check=_c049, values=[Rational(1, 8), Rational(1, 4), Rational(1, 16), sqrt(2) / 4], cognitive="Analysis", source_class=SC)


def _c050():
    return sin(dg(12)) * sin(dg(48)) * sin(dg(54))


q("U14-A-050", TOPIC, "Product to sum with 36 and 54 degrees", "Difficult", "Multi-step computation MCQ",
  r"The value of $\sin 12^\circ\sin 48^\circ\sin 54^\circ$ is",
  r"$\frac{1}{8}$",
  [(r"$\frac{1}{4}$", r"Writes $\sin 12^\circ\sin 48^\circ = \cos 36^\circ - \cos 60^\circ$, missing the factor $\frac{1}{2}$."),
   (r"$\frac{3-\sqrt{5}}{16}$", r"Finds $\sin 12^\circ\sin 48^\circ = \frac{\sqrt{5}-1}{8}$ but takes $\sin 54^\circ = \frac{\sqrt{5}-1}{4}$ (the value of $\sin 18^\circ$)."),
   (r"$\frac{\sqrt{5}-1}{8}$", r"Evaluates $\sin 12^\circ\sin 48^\circ$ and forgets to multiply by $\sin 54^\circ$.")],
  r"$\sin 12^\circ\sin 48^\circ = \frac{1}{2}(\cos 36^\circ - \cos 60^\circ) = \frac{1}{2}\left(\frac{\sqrt{5}+1}{4} - \frac{1}{2}\right) = \frac{\sqrt{5}-1}{8}$. Since $\sin 54^\circ = \cos 36^\circ = \frac{\sqrt{5}+1}{4}$, the product is $\frac{(\sqrt{5}-1)(\sqrt{5}+1)}{32} = \frac{4}{32} = \frac{1}{8}$.",
  r"Confusing $\sin 54^\circ$ with $\sin 18^\circ$.",
  "U14-A-sin12-48-54", "Product-to-sum, two special values and a conjugate product.",
  check=_c050, values=[Rational(1, 8), Rational(1, 4), (3 - sqrt(5)) / 16, (sqrt(5) - 1) / 8], cognitive="Analysis", source_class=SC)


_th, _e = symbols('theta e')


def _c051():
    T = (1 + _e) / (1 - _e) * (1 - cos(_th)) / (1 + cos(_th))   # tan^2(phi/2)
    return simplify((1 - T) / (1 + T))


q("U14-A-051", TOPIC, "Half angle relation with a parameter", "Difficult", "Multi-step computation MCQ",
  r"Let $0 < e < 1$ and $\tan\frac{\theta}{2} = \sqrt{\frac{1-e}{1+e}}\,\tan\frac{\phi}{2}$, where all the expressions are defined. Then $\cos\phi$ equals",
  r"$\frac{\cos\theta - e}{1 - e\cos\theta}$",
  [(r"$\frac{\cos\theta + e}{1 + e\cos\theta}$", r"Inverts the factor, using $\tan^2\frac{\phi}{2} = \frac{1-e}{1+e}\tan^2\frac{\theta}{2}$."),
   (r"$\frac{\cos\theta - e}{1 + e\cos\theta}$", r"Expands $(1-e)(1+\cos\theta) + (1+e)(1-\cos\theta)$ as $2 + 2e\cos\theta$ (sign slip)."),
   (r"$\frac{e - \cos\theta}{1 - e\cos\theta}$", r"Uses $\cos\phi = \frac{\tan^2(\phi/2) - 1}{\tan^2(\phi/2) + 1}$ (numerator reversed).")],
  r"Squaring, $\tan^2\frac{\phi}{2} = \frac{1+e}{1-e}\cdot\frac{1-\cos\theta}{1+\cos\theta} = T$. Then $\cos\phi = \frac{1-T}{1+T} = \frac{(1-e)(1+\cos\theta) - (1+e)(1-\cos\theta)}{(1-e)(1+\cos\theta) + (1+e)(1-\cos\theta)} = \frac{2\cos\theta - 2e}{2 - 2e\cos\theta} = \frac{\cos\theta - e}{1 - e\cos\theta}$.",
  r"Solving for the wrong angle or inverting the given factor.",
  "U14-A-half-angle-eccentric", "Rearranging a half-angle relation, conversion to cosine and careful algebra.",
  check=_c051, values=[(cos(_th) - _e) / (1 - _e * cos(_th)), (cos(_th) + _e) / (1 + _e * cos(_th)),
                       (cos(_th) - _e) / (1 + _e * cos(_th)), (_e - cos(_th)) / (1 - _e * cos(_th))],
  cognitive="Analysis", source_class=SC)


_t1, _a1, _b1 = symbols('t1 a1 b1')
_A1 = sin(_t1 + _a1)
_B1 = sin(_t1 + _b1)


def _c052():
    return cos(2 * (_a1 - _b1)) - 4 * _A1 * _B1 * cos(_a1 - _b1)


q("U14-A-052", TOPIC, "Eliminating the angle from two shifted sines", "Difficult", "Multi-step computation MCQ",
  r"If $\sin(\theta + \alpha) = a$ and $\sin(\theta + \beta) = b$, then $\cos 2(\alpha - \beta) - 4ab\cos(\alpha - \beta)$ equals",
  r"$1 - 2a^2 - 2b^2$",
  [(r"$2 - 2a^2 - 2b^2$", r"Uses $\cos 2X = 2\cos^2 X$ (drops the $-1$) with $X = \alpha - \beta$."),
   (r"$1 - 2a^2 - 2b^2 - 2a^2b^2$", r"Expands $(1-a^2)(1-b^2)$ as $1 - a^2 - b^2$, dropping the $a^2b^2$ term."),
   (r"$1 - 2a^2 - 2b^2 + 4a^2b^2$", r"Sign slip: writes $\cos X(\cos X - 2ab)$ as $\cos^2 P\cos^2 Q + a^2b^2$ instead of $\cos^2 P\cos^2 Q - a^2b^2$.")],
  r"Let $P = \theta + \alpha$, $Q = \theta + \beta$, so $X = \alpha - \beta = P - Q$ and $\cos X = \cos P\cos Q + ab$. Then $\cos 2X - 4ab\cos X = 2\cos X(\cos X - 2ab) - 1 = 2(\cos P\cos Q + ab)(\cos P\cos Q - ab) - 1 = 2[(1-a^2)(1-b^2) - a^2b^2] - 1 = 1 - 2a^2 - 2b^2$.",
  r"Not recognising $\alpha - \beta$ as a difference of the two given angles.",
  "U14-A-sin-shift-identity", "Re-expressing the angle, double angle, a difference of squares and careful expansion.",
  check=_c052, values=[1 - 2 * _A1 ** 2 - 2 * _B1 ** 2, 2 - 2 * _A1 ** 2 - 2 * _B1 ** 2,
                       1 - 2 * _A1 ** 2 - 2 * _B1 ** 2 - 2 * _A1 ** 2 * _B1 ** 2,
                       1 - 2 * _A1 ** 2 - 2 * _B1 ** 2 + 4 * _A1 ** 2 * _B1 ** 2],
  cognitive="Analysis", source_class=SC)


_p, _qq, _X = symbols('p q X')


def _c053():
    r1, r2 = solve(_X ** 2 - _p * _X + _qq, _X)
    T = simplify((r1 + r2) / (1 - r1 * r2))
    return simplify(T ** 2 / (1 + T ** 2))


q("U14-A-053", TOPIC, "tan A and tan B as roots of a quadratic", "Difficult", "Multi-step computation MCQ",
  r"If $\tan A$ and $\tan B$ are the roots of $x^2 - px + q = 0$, where $q \ne 1$, then $\sin^2(A + B)$ equals",
  r"$\frac{p^2}{p^2 + (1-q)^2}$",
  [(r"$\frac{p^2}{(1-q)^2}$", r"Finds $\tan^2(A+B)$ and stops."),
   (r"$\frac{p^2}{p^2 + (1+q)^2}$", r"Uses $1 + \tan A\tan B$ in the denominator of $\tan(A+B)$."),
   (r"$\frac{(1-q)^2}{p^2 + (1-q)^2}$", r"Computes $\cos^2(A+B) = \frac{1}{1+\tan^2(A+B)}$ instead of $\sin^2(A+B)$.")],
  r"By Vieta, $\tan A + \tan B = p$ and $\tan A\tan B = q$, so $\tan(A+B) = \frac{p}{1-q}$. Then $\sin^2(A+B) = \frac{\tan^2(A+B)}{1 + \tan^2(A+B)} = \frac{p^2/(1-q)^2}{1 + p^2/(1-q)^2} = \frac{p^2}{p^2 + (1-q)^2}$.",
  r"Stopping at $\tan^2(A+B)$ or converting to the wrong ratio.",
  "U14-A-tan-roots-quadratic", "Vieta, compound angle, then conversion from tangent to sine.",
  check=_c053, values=[_p ** 2 / (_p ** 2 + (1 - _qq) ** 2), _p ** 2 / (1 - _qq) ** 2,
                       _p ** 2 / (_p ** 2 + (1 + _qq) ** 2), (1 - _qq) ** 2 / (_p ** 2 + (1 - _qq) ** 2)],
  cognitive="Analysis", source_class=SC)


def _c054():
    # tan(3x) = sqrt(3) for x = 20, 80, 140 degrees; build the cubic and use Vieta
    x = Symbol('x')
    num, den = fraction(together(expand_trig(tan(3 * atan(x))) - sqrt(3)))
    poly = Poly(expand(num), x)
    a3, a2, a1, a0 = poly.all_coeffs()
    s1 = -a2 / a3
    s2 = a1 / a3
    val = simplify(s1 ** 2 - 2 * s2)
    # roots are tan20, tan80, tan140 = -tan40
    assert close(val, tan(dg(20)) ** 2 + tan(dg(40)) ** 2 + tan(dg(80)) ** 2)
    return val


q("U14-A-054", TOPIC, "Sum of squares of tangents via tan 3x", "Difficult", "Multi-step computation MCQ",
  r"The value of $\tan^2 20^\circ + \tan^2 40^\circ + \tan^2 80^\circ$ is",
  r"$33$",
  [(r"$21$", r"Uses the right cubic but takes the sum of products of roots two at a time as $+3$."),
   (r"$27$", r"Uses only $(\sum\tan\theta)^2 = 27$, forgetting to subtract twice the pairwise sum."),
   (r"$9$", r"Takes the sum of the roots as $\sqrt{3}$ (the value of $\tan 3\theta$), so $3 + 6$.")],
  r"For $\theta = 20^\circ, 80^\circ, 140^\circ$, $\tan 3\theta = \sqrt{3}$, so $t = \tan\theta$ satisfies $3t - t^3 = \sqrt{3}(1 - 3t^2)$, i.e. $t^3 - 3\sqrt{3}t^2 - 3t + \sqrt{3} = 0$, with roots $\tan 20^\circ$, $\tan 80^\circ$, $\tan 140^\circ = -\tan 40^\circ$. Then $\sum t = 3\sqrt{3}$ and $\sum t_i t_j = -3$, so $\sum t^2 = 27 + 6 = 33$.",
  r"Sign errors with Vieta's relations for the cubic from $\tan 3\theta$.",
  "U14-A-tan-square-ninths", "Requires building a cubic from $\\tan 3\\theta$ and applying Vieta; non-obvious route.",
  check=_c054, values=[33, 21, 27, 9], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The value of $\tan^2 20^\circ + \tan^2 40^\circ + \tan^2 80^\circ$ is", answer=33))


def _c055():
    return nsimplify(round(float(N(tan(dg(20)) * tan(dg(40)) * tan(dg(60)) * tan(dg(80)), 40)), 12))


q("U14-A-055", TOPIC, "Triple product identity for tangents", "Difficult", "Multi-step computation MCQ",
  r"The value of $\tan 20^\circ\tan 40^\circ\tan 60^\circ\tan 80^\circ$ is",
  r"$3$",
  [(r"$\sqrt{3}$", r"Finds $\tan 20^\circ\tan 40^\circ\tan 80^\circ = \sqrt{3}$ and forgets the factor $\tan 60^\circ$."),
   (r"$1$", r"Uses $\tan\theta\tan(60^\circ-\theta)\tan(60^\circ+\theta) = \cot 3\theta$, getting $\frac{1}{\sqrt{3}}\cdot\sqrt{3}$."),
   (r"$9$", r"Uses $\tan\theta\tan(60^\circ-\theta)\tan(60^\circ+\theta) = 3\tan 3\theta$ (confusing it with the sum identity), getting $3\sqrt{3}\cdot\sqrt{3}$.")],
  r"$\tan\theta\tan(60^\circ - \theta)\tan(60^\circ + \theta) = \tan 3\theta$, since $\tan(60^\circ-\theta)\tan(60^\circ+\theta) = \frac{3 - \tan^2\theta}{1 - 3\tan^2\theta}$. With $\theta = 20^\circ$: $\tan 20^\circ\tan 40^\circ\tan 80^\circ = \tan 60^\circ = \sqrt{3}$. Multiplying by $\tan 60^\circ = \sqrt{3}$ gives $3$.",
  r"Mixing the product identity with the sum identity $\tan\theta + \tan(\theta + 60^\circ) + \tan(\theta + 120^\circ) = 3\tan 3\theta$.",
  "U14-A-tan-triple-product", "Needs the non-standard triple-product identity and recognising $40^\\circ, 80^\\circ$ as $60^\\circ \\mp 20^\\circ$.",
  check=_c055, values=[3, sqrt(3), 1, 9], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"The value of $\tan 20^\circ\tan 40^\circ\tan 60^\circ\tan 80^\circ$ is", answer=3))
