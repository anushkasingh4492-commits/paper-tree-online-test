import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
x = Symbol('x')
t = Symbol('t', positive=True)
n = Symbol('n', integer=True, positive=True)
kk = Symbol('k', integer=True, positive=True)
a_, b_, c_ = symbols('a b c')
kp = Symbol('k', positive=True)
kr = Symbol('k')

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TT, FF, TF, FT = (True, True), (False, False), (True, False), (False, True)
DNE = Symbol('DNE')

TOP = "Limits"
GIF = r"where $[\cdot]$ denotes the greatest integer function"


def lim2(e, x0):
    """Two-sided limit; returns DNE if one-sided limits differ."""
    l = limit(e, x, x0, '-'); r = limit(e, x, x0, '+')
    return l if simplify(l - r) == 0 else DNE


def floor_limit(e, x0=0):
    """lim [e] as x -> x0 (two-sided), from the limit of e and the sign of its approach."""
    L = limit(e, x, x0)
    if not L.is_integer:
        return floor(L)
    c, p = (e - L).subs(x, x + x0).leadterm(x)
    assert p % 2 == 0  # same side of L from both directions
    return L - 1 if c < 0 else L


# =================================================================== EASY

q("U07-B-001", TOP, "Algebraic limit by factorisation", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 2} \frac{x^3 - 8}{x^2 - 4}$ equals",
  r"$3$",
  [(r"$2$", r"Factorises $x^3 - 8$ as $(x-2)(x^2+4)$, getting $\frac{8}{4} = 2$."),
   (r"$12$", r"Cancels $x - 2$ but keeps only $x^2 + 2x + 4 = 12$, dropping the factor $x + 2$ of the denominator."),
   (r"$\frac{1}{3}$", r"Inverts the ratio, computing $\frac{x+2}{x^2+2x+4} \to \frac{4}{12}$.")],
  r"$\frac{x^3 - 8}{x^2 - 4} = \frac{(x-2)(x^2+2x+4)}{(x-2)(x+2)} = \frac{x^2+2x+4}{x+2}$ for $x \ne 2$, which tends to $\frac{12}{4} = 3$.",
  r"Misfactorising $x^3 - a^3$ or forgetting a factor after cancelling.",
  "U07-B-factorise", r"One factorisation and one substitution.",
  check=lambda: limit((x**3 - 8)/(x**2 - 4), x, 2), values=[3, 2, 12, Rational(1, 3)], cognitive="Application",
  numerical=dict(question=r"The value of $\lim_{x \to 2} \frac{x^3 - 8}{x^2 - 4}$ is", answer=3))

q("U07-B-002", TOP, "Limit by rationalisation", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} \frac{\sqrt{1+x} - \sqrt{1-x}}{x}$ equals",
  r"$1$",
  [(r"$2$", r"After rationalising, evaluates the conjugate $\sqrt{1+x} + \sqrt{1-x}$ at $x = 0$ as $1$ instead of $2$, getting $\frac{2}{1}$."),
   (r"$\frac{1}{2}$", r"Simplifies $(1+x) - (1-x)$ to $x$ instead of $2x$, getting $\frac{1}{2}$."),
   (r"$-1$", r"Subtracts in the wrong order, $(1-x) - (1+x) = -2x$, getting $\frac{-2}{2}$.")],
  r"Multiply by the conjugate: $\frac{(1+x)-(1-x)}{x(\sqrt{1+x}+\sqrt{1-x})} = \frac{2}{\sqrt{1+x}+\sqrt{1-x}} \to \frac{2}{2} = 1$.",
  r"Arithmetic slips while rationalising a difference of square roots.",
  "U07-B-rationalise", r"One rationalisation step.",
  check=lambda: limit((sqrt(1 + x) - sqrt(1 - x))/x, x, 0), values=[1, 2, Rational(1, 2), -1], cognitive="Application")

q("U07-B-003", TOP, "Standard trigonometric limits", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} \frac{\sin 5x}{\tan 3x}$ equals",
  r"$\frac{5}{3}$",
  [(r"$\frac{3}{5}$", r"Inverts the ratio of the coefficients."),
   (r"$1$", r"Uses $\frac{\sin \theta}{\theta} \to 1$ and $\frac{\tan \theta}{\theta} \to 1$ but ignores the coefficients $5$ and $3$."),
   (r"$15$", r"Multiplies the coefficients instead of dividing them.")],
  r"$\frac{\sin 5x}{\tan 3x} = \frac{\sin 5x}{5x} \cdot \frac{3x}{\tan 3x} \cdot \frac{5}{3} \to 1 \cdot 1 \cdot \frac{5}{3} = \frac{5}{3}$.",
  r"Dropping the scaling factors when using $\frac{\sin \theta}{\theta} \to 1$.",
  "U07-B-std-trig", r"Direct use of two standard limits.",
  check=lambda: limit(sin(5*x)/tan(3*x), x, 0), values=[Rational(5, 3), Rational(3, 5), 1, 15], cognitive="Recall")

q("U07-B-004", TOP, "Limit involving 1 - cos", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} \frac{1 - \cos 4x}{x^2}$ equals",
  r"$8$",
  [(r"$16$", r"Uses $1 - \cos \theta \approx \theta^2$, dropping the factor $\frac{1}{2}$."),
   (r"$2$", r"Takes $\theta^2$ as $4x^2$ instead of $16x^2$, getting $\frac{4}{2}$."),
   (r"$\frac{1}{8}$", r"Inverts the correct value.")],
  r"$1 - \cos 4x = 2\sin^2 2x$, so the limit is $2 \cdot \left(\frac{\sin 2x}{x}\right)^2 \to 2 \cdot 4 = 8$.",
  r"Forgetting the $\frac{1}{2}$ in $1 - \cos \theta \approx \frac{\theta^2}{2}$ or not squaring the coefficient.",
  "U07-B-one-minus-cos", r"One identity and one standard limit.",
  check=lambda: limit((1 - cos(4*x))/x**2, x, 0), values=[8, 16, 2, Rational(1, 8)], cognitive="Application",
  numerical=dict(question=r"The value of $\lim_{x \to 0} \frac{1 - \cos 4x}{x^2}$ is", answer=8))

q("U07-B-005", TOP, "Standard exponential and logarithmic limits", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} \frac{e^{3x} - 1}{\log_e(1 + 2x)}$ equals",
  r"$\frac{3}{2}$",
  [(r"$\frac{2}{3}$", r"Inverts the ratio of the coefficients."),
   (r"$6$", r"Multiplies the coefficients $3$ and $2$."),
   (r"$1$", r"Treats both $\frac{e^{u}-1}{u}$ and $\frac{\log_e(1+u)}{u}$ as $1$ without scaling by $3x$ and $2x$.")],
  r"$\frac{e^{3x}-1}{\log_e(1+2x)} = \frac{e^{3x}-1}{3x} \cdot \frac{2x}{\log_e(1+2x)} \cdot \frac{3}{2} \to \frac{3}{2}$.",
  r"Ignoring the scaling needed to use $\frac{e^u - 1}{u} \to 1$ and $\frac{\log_e(1+u)}{u} \to 1$.",
  "U07-B-exp-log-std", r"Two standard limits in one line.",
  check=lambda: limit((exp(3*x) - 1)/log(1 + 2*x), x, 0), values=[Rational(3, 2), Rational(2, 3), 6, 1], cognitive="Recall")

q("U07-B-006", TOP, "Limit of a rational function at infinity", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to \infty} \frac{(2x+3)^3 (x-1)^2}{x^5 + 4}$ equals",
  r"$8$",
  [(r"$2$", r"Takes the leading coefficient of $(2x+3)^3$ as $2$ instead of $2^3$."),
   (r"$6$", r"Multiplies the leading coefficient $2$ by the power $3$ instead of raising it to that power."),
   (r"$1$", r"Notes that both degrees are $5$ and takes the ratio of leading coefficients as $1$ without expanding.")],
  r"Both numerator and denominator have degree $5$. The leading coefficient of the numerator is $2^3 \cdot 1^2 = 8$, so dividing through by $x^5$ gives $\left(2 + \frac{3}{x}\right)^3\left(1 - \frac{1}{x}\right)^2 \big/ \left(1 + \frac{4}{x^5}\right) \to 8$.",
  r"Mishandling the leading coefficient of a power of a linear factor.",
  "U07-B-infinity-rational", r"Equal degrees; one leading-coefficient calculation.",
  check=lambda: limit((2*x + 3)**3*(x - 1)**2/(x**5 + 4), x, oo), values=[8, 2, 6, 1], cognitive="Application")

q("U07-B-007", TOP, "Standard exponential limits", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} \frac{3^x - 2^x}{x}$ equals",
  r"$\log_e \frac{3}{2}$",
  [(r"$\log_e 6$", r"Adds the two limits $\log_e 3$ and $\log_e 2$ instead of subtracting."),
   (r"$\log_e \frac{2}{3}$", r"Subtracts in the wrong order, $\log_e 2 - \log_e 3$."),
   (r"$\frac{\log_e 3}{\log_e 2}$", r"Divides the two standard limits instead of subtracting them.")],
  r"Write $\frac{3^x - 2^x}{x} = \frac{3^x - 1}{x} - \frac{2^x - 1}{x} \to \log_e 3 - \log_e 2 = \log_e \frac{3}{2}$.",
  r"Combining the standard limits $\frac{a^x - 1}{x} \to \log_e a$ with the wrong operation.",
  "U07-B-exp-log-std", r"Split into two standard limits.",
  check=lambda: limit((3**x - 2**x)/x, x, 0), values=[log(Rational(3, 2)), log(6), log(Rational(2, 3)), log(3)/log(2)], cognitive="Application")

q("U07-B-008", TOP, "One-sided limit with greatest integer function", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 2^-} \left([x^2] - [x]^2\right)$, " + GIF + r", equals",
  r"$2$",
  [(r"$0$", r"Substitutes $x = 2$, getting $[4] - [2]^2 = 0$."),
   (r"$-1$", r"Takes $[x^2] = 3$ correctly but uses $[x] = 2$ for $x$ just below $2$."),
   (r"$3$", r"Uses $[x] = 1$ correctly but takes $[x^2] = 4$ for $x$ just below $2$.")],
  r"For $x$ slightly less than $2$, $x^2$ is slightly less than $4$, so $[x^2] = 3$ and $[x] = 1$. Hence the expression equals $3 - 1 = 2$ near $2^-$, and the limit is $2$.",
  r"Evaluating the greatest integer function at the limit point instead of just to its left.",
  "U07-B-gif-one-sided", r"One-sided values of two greatest integer terms.",
  check=lambda: limit(floor(x**2) - floor(x)**2, x, 2, '-'), values=[2, 0, -1, 3], cognitive="Application",
  numerical=dict(question=r"The value of $\lim_{x \to 2^-} \left([x^2] - [x]^2\right)$, " + GIF + r", is", answer=2))

q("U07-B-009", TOP, "One-sided limit with modulus", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 3^-} \frac{x^2 - 2x - 3}{|x - 3|}$ equals",
  r"$-4$",
  [(r"$4$", r"Replaces $|x - 3|$ by $x - 3$ for $x < 3$, which gives the right-hand limit."),
   (r"$-2$", r"Factorises $x^2 - 2x - 3$ as $(x-3)(x-1)$, getting $-(x-1) \to -2$."),
   (r"$2$", r"Uses the wrong factor $(x-1)$ and also treats $|x-3|$ as $x - 3$.")],
  r"$x^2 - 2x - 3 = (x-3)(x+1)$, and for $x < 3$, $|x-3| = -(x-3)$. So the expression is $-(x+1) \to -4$.",
  r"Dropping the sign of $|x - a|$ on the left of $a$.",
  "U07-B-modulus-one-sided", r"Factorise, then resolve the modulus on one side.",
  check=lambda: limit((x**2 - 2*x - 3)/Abs(x - 3), x, 3, '-'), values=[-4, 4, -2, 2], cognitive="Application")

q("U07-B-010", TOP, "Limits of the form 1 to the power infinity", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} (1 + 3x)^{\frac{2}{x}}$ equals",
  r"$e^{6}$",
  [(r"$e^{\frac{3}{2}}$", r"Divides $3$ by $2$ instead of multiplying."),
   (r"$e^{\frac{2}{3}}$", r"Divides $2$ by $3$, inverting the product."),
   (r"$e^{5}$", r"Adds $3$ and $2$ in the exponent.")],
  r"For the $1^\infty$ form, the limit is $e^{L}$ with $L = \lim_{x \to 0} 3x \cdot \frac{2}{x} = 6$. So the value is $e^6$.",
  r"Combining the base increment and the exponent with the wrong operation.",
  "U07-B-one-inf-basic", r"One application of $\lim (1+u)^{1/u} = e$.",
  check=lambda: limit((1 + 3*x)**(2/x), x, 0), values=[exp(6), exp(Rational(3, 2)), exp(Rational(2, 3)), exp(5)], cognitive="Application")

q("U07-B-011", TOP, "Limit involving 1 - cos", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0} \frac{x \tan 2x}{1 - \cos 2x}$ equals",
  r"$1$",
  [(r"$2$", r"Uses $1 - \cos 2x \approx x^2$, getting $\frac{2x^2}{x^2}$."),
   (r"$4$", r"Uses $1 - \cos 2x \approx \frac{x^2}{2}$, the form for $1 - \cos x$, getting $\frac{2x^2}{x^2/2}$."),
   (r"$\frac{1}{2}$", r"Uses $1 - \cos 2x \approx (2x)^2 = 4x^2$, dropping the $\frac{1}{2}$.")],
  r"$1 - \cos 2x = 2\sin^2 x$ and $\tan 2x \approx 2x$, so the expression is $\frac{x \tan 2x}{2 \sin^2 x} = \frac{\tan 2x}{2x} \cdot \frac{x^2}{\sin^2 x} \cdot 1 \to 1$.",
  r"Using the wrong small-angle approximation for $1 - \cos 2x$.",
  "U07-B-one-minus-cos", r"Two standard approximations combined.",
  check=lambda: limit(x*tan(2*x)/(1 - cos(2*x)), x, 0), values=[1, 2, 4, Rational(1, 2)], cognitive="Application")

q("U07-B-012", TOP, "Limit at infinity with a square root", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to \infty} \left(\sqrt{x^2 + 5x} - x\right)$ equals",
  r"$\frac{5}{2}$",
  [(r"$5$", r"After rationalising to $\frac{5x}{\sqrt{x^2+5x} + x}$, takes the denominator as $x$ instead of $2x$."),
   (r"$0$", r"Treats $\sqrt{x^2 + 5x}$ as $x$ for large $x$, so the difference is taken as $0$."),
   (r"$-\frac{5}{2}$", r"Rationalises with the subtraction reversed, getting $\frac{-5x}{2x}$.")],
  r"$\sqrt{x^2+5x} - x = \frac{5x}{\sqrt{x^2+5x} + x} = \frac{5}{\sqrt{1 + 5/x} + 1} \to \frac{5}{2}$.",
  r"Treating $\infty - \infty$ as $0$, or losing the factor $2$ in the conjugate.",
  "U07-B-infinity-root", r"One rationalisation at infinity.",
  check=lambda: limit(sqrt(x**2 + 5*x) - x, x, oo), values=[Rational(5, 2), 5, 0, Rational(-5, 2)], cognitive="Application")

q("U07-B-013", TOP, "One-sided limits with exponential terms", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 0^-} \frac{1 + 2^{1/x}}{3 - 2^{1/x}}$ equals",
  r"$\frac{1}{3}$",
  [(r"$-1$", r"Treats $2^{1/x} \to \infty$, which happens only for $x \to 0^+$; this is the right-hand limit."),
   (r"$1$", r"Takes $2^{1/x} \to 1$, getting $\frac{2}{2}$."),
   (r"$-\frac{1}{3}$", r"Uses $2^{1/x} \to 0$ but writes the denominator as $0 - 3$.")],
  r"As $x \to 0^-$, $\frac{1}{x} \to -\infty$, so $2^{1/x} \to 0$. The expression tends to $\frac{1 + 0}{3 - 0} = \frac{1}{3}$.",
  r"Treating $a^{1/x}$ the same way on both sides of $0$.",
  "U07-B-exp-one-sided", r"One observation about $2^{1/x}$ from the left.",
  check=lambda: limit((1 + 2**(1/x))/(3 - 2**(1/x)), x, 0, '-'), values=[Rational(1, 3), -1, 1, Rational(-1, 3)], cognitive="Understanding")

q("U07-B-014", TOP, "Standard trigonometric limits", "Easy", "Conceptual/application MCQ",
  r"If $x$ is measured in degrees, then $\lim_{x \to 0} \frac{\sin x}{x}$ equals",
  r"$\frac{\pi}{180}$",
  [(r"$1$", r"Applies the radian result $\frac{\sin \theta}{\theta} \to 1$ directly to degrees."),
   (r"$\frac{180}{\pi}$", r"Converts degrees to radians the wrong way round."),
   (r"$\pi$", r"Writes $x^\circ$ as $\pi x$ radians, forgetting to divide by $180$.")],
  r"$x^\circ = \frac{\pi x}{180}$ radians, so $\frac{\sin(\pi x/180)}{x} = \frac{\sin(\pi x/180)}{\pi x/180} \cdot \frac{\pi}{180} \to \frac{\pi}{180}$.",
  r"Using $\frac{\sin x}{x} \to 1$ without checking the angle is in radians.",
  "U07-B-std-trig", r"One unit conversion and one standard limit.",
  check=lambda: limit(sin(pi*x/180)/x, x, 0), values=[pi/180, 1, 180/pi, pi], cognitive="Understanding")


def _c15():
    a = 2
    return limit((x**5 - a**5)/(x - a), x, a)
q("U07-B-015", TOP, "Limit of the form (x^n - a^n)/(x - a)", "Easy", "Single-step computation MCQ",
  r"$\lim_{x \to 2} \frac{x^5 - 32}{x - 2}$ equals",
  r"$80$",
  [(r"$40$", r"Uses $n a^{n-2} = 5 \cdot 2^3$."),
   (r"$16$", r"Uses $a^{n-1} = 2^4$, forgetting the factor $n$."),
   (r"$160$", r"Uses $n a^{n} = 5 \cdot 32$.")],
  r"$\lim_{x \to a} \frac{x^n - a^n}{x - a} = n a^{n-1}$. With $n = 5$, $a = 2$: $5 \cdot 2^4 = 80$.",
  r"Misremembering the exponent or the factor $n$ in $n a^{n-1}$.",
  "U07-B-xn-an", r"Direct use of one standard result.",
  check=_c15, values=[80, 40, 16, 160], cognitive="Recall",
  numerical=dict(question=r"The value of $\lim_{x \to 2} \frac{x^5 - 32}{x - 2}$ is", answer=80))


def _c16():
    l, r = limit(Abs(x)/x, x, 0, '-'), limit(Abs(x)/x, x, 0, '+')
    s1 = (l == r) and (l == 1)
    s2 = limit((1 + 1/x)**x, x, oo) == 1
    return (bool(s1), bool(s2))
q("U07-B-016", TOP, "Existence and value of basic limits", "Easy", "Statement-based MCQ",
  r"Statement I: $\lim_{x \to 0} \frac{|x|}{x} = 1$. Statement II: $\lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^{x} = 1$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Takes the right-hand limit $1$ as the limit, and treats $1^\infty$ as $1$."),
   (ST_TF, r"Uses only the right-hand limit of $\frac{|x|}{x}$ for Statement I."),
   (ST_FT, r"Treats the $1^\infty$ form as equal to $1$.")],
  r"For $x > 0$, $\frac{|x|}{x} = 1$; for $x < 0$ it is $-1$. The one-sided limits differ, so the limit does not exist and Statement I is false. Statement II is the standard limit $e \ne 1$, so it is false.",
  r"Ignoring the left-hand limit; treating $1^\infty$ as $1$.",
  "U07-B-limit-concepts", r"Two one-line conceptual checks.",
  check=_c16, values=[FF, TT, TF, FT], cognitive="Understanding")

# =================================================================== MEDIUM


def _c17():
    N = x**2 + a_*x + b_
    bs = solve(N.subs(x, 2), b_)[0]
    L = limit(cancel(N.subs(b_, bs)/(x - 2)), x, 2)
    asol = solve(Eq(L, 7), a_)[0]
    return asol - bs.subs(a_, asol)
q("U07-B-017", TOP, "Parameters from a limit value", "Medium", "Inverse/parameter MCQ",
  r"If $\lim_{x \to 2} \frac{x^2 + ax + b}{x - 2} = 7$, where $a, b$ are real constants, then $a - b$ equals",
  r"$13$",
  [(r"$19$", r"Writes the cofactor as $x + a$ instead of $x + 2 + a$, so the limit is taken as $2 + a = 7$, giving $a = 5$, $b = -14$."),
   (r"$-7$", r"Gets $a = 3$ but solves $4 + 2a + b = 0$ as $b = 10$ (sign slip)."),
   (r"$-5$", r"Writes the limit as $4 - a = 7$, so $a = -3$, $b = 2$.")],
  r"For a finite limit the numerator must vanish at $x = 2$: $4 + 2a + b = 0$. Then $x^2 + ax + b = (x-2)(x + 2 + a)$, so the limit is $4 + a = 7$, giving $a = 3$ and $b = -10$. Hence $a - b = 13$.",
  r"Not using the condition that the numerator must vanish, or slipping on the cofactor.",
  "U07-B-param-poly", r"Two conditions (vanishing numerator, limit value) solved together.",
  check=_c17, values=[13, 19, -7, -5], cognitive="Application",
  numerical=dict(question=r"If $\lim_{x \to 2} \frac{x^2 + ax + b}{x - 2} = 7$, where $a, b$ are real constants, then the value of $a - b$ is", answer=13))

q("U07-B-018", TOP, "Limit by double rationalisation", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 1} \frac{\sqrt{x+3} - 2}{\sqrt{x+8} - 3}$ equals",
  r"$\frac{3}{2}$",
  [(r"$\frac{2}{3}$", r"Inverts the ratio of the conjugate factors, $\frac{4}{6}$."),
   (r"$1$", r"Cancels the common factor $x - 1$ from both after rationalising but drops the conjugate factors $4$ and $6$."),
   (r"$-\frac{3}{2}$", r"Writes the rationalised numerator as $4 - (x+3) = 1 - x$, introducing a sign error.")],
  r"Rationalise both: $\sqrt{x+3} - 2 = \frac{x-1}{\sqrt{x+3}+2}$ and $\sqrt{x+8} - 3 = \frac{x-1}{\sqrt{x+8}+3}$. The ratio is $\frac{\sqrt{x+8}+3}{\sqrt{x+3}+2} \to \frac{6}{4} = \frac{3}{2}$.",
  r"Mishandling the conjugate factors when both numerator and denominator are rationalised.",
  "U07-B-rationalise", r"Two rationalisations, then a ratio of conjugates.",
  check=lambda: limit((sqrt(x + 3) - 2)/(sqrt(x + 8) - 3), x, 1), values=[Rational(3, 2), Rational(2, 3), 1, Rational(-3, 2)], cognitive="Application")

q("U07-B-019", TOP, "Trigonometric limit at a non-zero point", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to \pi/2} \frac{1 - \sin x}{\left(\frac{\pi}{2} - x\right)^2}$ equals",
  r"$\frac{1}{2}$",
  [(r"$1$", r"After $h = \frac{\pi}{2} - x$, uses $1 - \cos h \approx h^2$."),
   (r"$2$", r"Writes $1 - \cos h = 2\sin^2 \frac{h}{2}$ but approximates $\sin \frac{h}{2}$ by $h$."),
   (r"$\frac{1}{4}$", r"Writes $1 - \cos h = \sin^2 \frac{h}{2}$, dropping the factor $2$.")],
  r"Put $h = \frac{\pi}{2} - x \to 0$. Then $1 - \sin x = 1 - \cos h = 2 \sin^2 \frac{h}{2}$, so the expression is $\frac{2\sin^2(h/2)}{h^2} = \frac{1}{2}\left(\frac{\sin(h/2)}{h/2}\right)^2 \to \frac{1}{2}$.",
  r"Losing a factor in the half-angle form of $1 - \cos h$.",
  "U07-B-trig-shift", r"Substitution to shift the point, then a half-angle identity.",
  check=lambda: limit((1 - sin(x))/(pi/2 - x)**2, x, pi/2), values=[Rational(1, 2), 1, 2, Rational(1, 4)], cognitive="Application")

q("U07-B-020", TOP, "Trigonometric limit at a non-zero point", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to \pi/4} \frac{\sqrt{2}\cos x - 1}{\cot x - 1}$ equals",
  r"$\frac{1}{2}$",
  [(r"$2$", r"Inverts the ratio of the derivatives, $\frac{-2}{-1}$."),
   (r"$-\frac{1}{2}$", r"Takes the derivative of $\cot x$ as $+\operatorname{cosec}^2 x$."),
   (r"$\frac{\sqrt{2}}{2}$", r"Takes the derivative of $\cot x$ as $-\operatorname{cosec} x = -\sqrt{2}$ at $\frac{\pi}{4}$.")],
  r"Both numerator and denominator vanish at $\frac{\pi}{4}$. Write $\cot x - 1 = \frac{\cos x - \sin x}{\sin x}$ and $\sqrt{2}\cos x - 1 = \frac{2\cos^2 x - 1}{\sqrt{2}\cos x + 1} = \frac{(\cos x - \sin x)(\cos x + \sin x)}{\sqrt{2}\cos x + 1}$. The ratio becomes $\frac{\sin x(\cos x + \sin x)}{\sqrt{2}\cos x + 1} \to \frac{\frac{1}{\sqrt{2}} \cdot \sqrt{2}}{2} = \frac{1}{2}$.",
  r"Slips in the derivative of $\cot x$ when resolving a $\frac{0}{0}$ form.",
  "U07-B-trig-shift", r"Needs factorising $\cos 2x$ and $\cos x - \sin x$ (or derivatives); several steps.",
  check=lambda: limit((sqrt(2)*cos(x) - 1)/(cot(x) - 1), x, pi/4), values=[Rational(1, 2), 2, Rational(-1, 2), sqrt(2)/2], cognitive="Application")

q("U07-B-021", TOP, "Trigonometric limit of order three", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \frac{\tan x - \sin x}{x^3}$ equals",
  r"$\frac{1}{2}$",
  [(r"$0$", r"Replaces both $\tan x$ and $\sin x$ by $x$, so the numerator is taken as $0$."),
   (r"$1$", r"Writes the numerator as $\tan x (1 - \cos x)$ but uses $1 - \cos x \approx x^2$."),
   (r"$\frac{1}{6}$", r"Uses $\sin x \approx x - \frac{x^3}{6}$ but $\tan x \approx x$, keeping only the sine correction.")],
  r"$\tan x - \sin x = \tan x(1 - \cos x)$. So the expression is $\frac{\tan x}{x} \cdot \frac{1 - \cos x}{x^2} \to 1 \cdot \frac{1}{2} = \frac{1}{2}$.",
  r"Replacing $\tan x$ and $\sin x$ by $x$ in a difference.",
  "U07-B-trig-cubic", r"Factorisation plus two standard limits; a classic trap.",
  check=lambda: limit((tan(x) - sin(x))/x**3, x, 0), values=[Rational(1, 2), 0, 1, Rational(1, 6)], cognitive="Analysis")

q("U07-B-022", TOP, "Limits of the form 1 to the power infinity", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to \infty} \left(\frac{x+3}{x-1}\right)^{x+2}$ equals",
  r"$e^{4}$",
  [(r"$e^{3}$", r"Treats the base as $1 + \frac{3}{x}$, ignoring the $x - 1$ in the denominator."),
   (r"$e^{2}$", r"Writes the base minus $1$ as $\frac{3 - 1}{x - 1}$, subtracting the constants."),
   (r"$e^{-4}$", r"Computes the base minus $1$ as $\frac{(x-1)-(x+3)}{x-1}$.")],
  r"This is a $1^\infty$ form with value $e^{L}$, $L = \lim (x+2)\left(\frac{x+3}{x-1} - 1\right) = \lim \frac{4(x+2)}{x-1} = 4$. So the limit is $e^4$.",
  r"Computing the base minus $1$ incorrectly in the $1^\infty$ formula.",
  "U07-B-one-inf-infty", r"Requires the $e^{\lim g(f-1)}$ form and a rational limit at infinity.",
  check=lambda: limit(((x + 3)/(x - 1))**(x + 2), x, oo), values=[exp(4), exp(3), exp(2), exp(-4)], cognitive="Application")

q("U07-B-023", TOP, "Limits of the form 1 to the power infinity", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} (\cos x)^{\frac{1}{x^2}}$ equals",
  r"$e^{-\frac{1}{2}}$",
  [(r"$1$", r"Treats $1^\infty$ as $1$."),
   (r"$e^{\frac{1}{2}}$", r"Takes $\cos x - 1 \approx +\frac{x^2}{2}$, losing the sign."),
   (r"$e^{-1}$", r"Takes $\cos x - 1 \approx -x^2$, dropping the $\frac{1}{2}$.")],
  r"$1^\infty$ form: the limit is $e^{L}$ with $L = \lim \frac{\cos x - 1}{x^2} = -\frac{1}{2}$. So the value is $e^{-1/2}$.",
  r"Treating $1^\infty$ as $1$, or a slip in $\cos x - 1 \approx -\frac{x^2}{2}$.",
  "U07-B-one-inf-trig", r"$1^\infty$ form combined with a trigonometric standard limit.",
  check=lambda: limit(cos(x)**(1/x**2), x, 0), values=[exp(Rational(-1, 2)), 1, exp(Rational(1, 2)), exp(-1)], cognitive="Application")

q("U07-B-024", TOP, "Limits of the form 1 to the power infinity", "Medium", "Conceptual/application MCQ",
  r"$\lim_{x \to \pi/2} (\sin x)^{\tan x}$ equals",
  r"$1$",
  [(r"$e^{-1}$", r"Uses $1 - \sin x \approx \frac{\pi}{2} - x$ (first order) with $\tan x \approx \frac{1}{\pi/2 - x}$, getting $L = -1$."),
   (r"$e$", r"Makes the first-order error for $1 - \sin x$ and also loses the sign, getting $L = 1$."),
   (r"$0$", r"Treats a base less than $1$ raised to a large power as tending to $0$, ignoring that the base tends to $1$.")],
  r"$1^\infty$ form: limit $= e^{L}$ with $L = \lim (\sin x - 1)\tan x$. Put $h = \frac{\pi}{2} - x$: $(\cos h - 1)\cot h = -\frac{2\sin^2(h/2)\cos h}{\sin h} \approx -\frac{h^2/2}{h} \to 0$. So the limit is $e^0 = 1$.",
  r"Assuming $1 - \sin x$ is first order in $\frac{\pi}{2} - x$.",
  "U07-B-one-inf-trig", r"$1^\infty$ form at a non-zero point with a second-order numerator; easy to misjudge the order.",
  check=lambda: lim2(sin(x)**tan(x), pi/2), values=[1, exp(-1), E, 0], cognitive="Analysis")

q("U07-B-025", TOP, "Limits of the form 1 to the power infinity", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \left(\frac{4^x + 9^x}{2}\right)^{\frac{1}{x}}$ equals",
  r"$6$",
  [(r"$36$", r"Gets $L = \log_e 4 + \log_e 9$, forgetting to divide by $2$."),
   (r"$\frac{13}{2}$", r"Takes the arithmetic mean of $4$ and $9$."),
   (r"$1$", r"Treats the $1^\infty$ form as $1$.")],
  r"$1^\infty$ form: $L = \lim \frac{1}{x}\left(\frac{4^x + 9^x}{2} - 1\right) = \frac{1}{2}\left(\lim \frac{4^x - 1}{x} + \lim \frac{9^x - 1}{x}\right) = \frac{\log_e 4 + \log_e 9}{2} = \log_e 6$. So the limit is $e^{\log_e 6} = 6$.",
  r"Dropping the factor $\frac{1}{2}$ or treating $1^\infty$ as $1$.",
  "U07-B-one-inf-exp", r"$1^\infty$ form with two exponential standard limits.",
  check=lambda: limit(((4**x + 9**x)/2)**(1/x), x, 0), values=[6, 36, Rational(13, 2), 1], cognitive="Application",
  numerical=dict(question=r"The value of $\lim_{x \to 0} \left(\frac{4^x + 9^x}{2}\right)^{\frac{1}{x}}$ is", answer=6))

q("U07-B-026", TOP, "Limit at negative infinity with a square root", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to -\infty} \left(\sqrt{x^2 + 2x} + x\right)$ equals",
  r"$-1$",
  [(r"$1$", r"Copies the value of $\lim_{x \to \infty}\left(\sqrt{x^2+2x} - x\right) = 1$ without adjusting for $x < 0$."),
   (r"$0$", r"Takes $\sqrt{x^2 + 2x} \approx |x| = -x$, so the sum is taken as $0$."),
   (r"$-2$", r"Uses $\sqrt{1 + \frac{2}{x}} \approx 1 + \frac{2}{x}$, forgetting the $\frac{1}{2}$.")],
  r"For $x < 0$, $\sqrt{x^2 + 2x} = |x|\sqrt{1 + \frac{2}{x}} = -x\sqrt{1 + \frac{2}{x}}$. Rationalising, $\sqrt{x^2+2x} + x = \frac{2x}{\sqrt{x^2+2x} - x} = \frac{2x}{-x\left(\sqrt{1+2/x} + 1\right)} \to \frac{2}{-2} = -1$.",
  r"Using $\sqrt{x^2} = x$ when $x$ is negative.",
  "U07-B-infinity-root", r"Rationalisation plus the sign of $\sqrt{x^2}$ for negative $x$; a trap.",
  check=lambda: limit(sqrt(x**2 + 2*x) + x, x, -oo), values=[-1, 1, 0, -2], cognitive="Analysis")


def _c27():
    s1 = floor_limit(sin(x)/x) == 0
    s2 = floor_limit(tan(x)/x) == 1
    return (bool(s1), bool(s2))
q("U07-B-027", TOP, "Greatest integer of standard trigonometric ratios", "Medium", "Statement-based MCQ",
  r"Let $[\cdot]$ denote the greatest integer function. Statement I: $\lim_{x \to 0} \left[\frac{\sin x}{x}\right] = 0$. Statement II: $\lim_{x \to 0} \left[\frac{\tan x}{x}\right] = 1$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Swaps the inequalities, believing $\frac{\sin x}{x} > 1$ and $\frac{\tan x}{x} < 1$ near $0$, so gets greatest integers $1$ and $0$."),
   (ST_FT, r"Takes $\left[\frac{\sin x}{x}\right] \to [1] = 1$, ignoring that $\frac{\sin x}{x} < 1$ near $0$."),
   (ST_TF, r"Believes $\frac{\tan x}{x} < 1$ near $0$, so takes its greatest integer as $0$.")],
  r"For $0 < |x| < \frac{\pi}{2}$, $|\sin x| < |x| < |\tan x|$ and the ratios are positive, so $\frac{\sin x}{x}$ lies just below $1$ and $\frac{\tan x}{x}$ just above $1$. Hence $\left[\frac{\sin x}{x}\right] = 0$ and $\left[\frac{\tan x}{x}\right] = 1$ near $0$; both statements are true.",
  r"Replacing $[f(x)]$ by $[\lim f(x)]$ without checking the side of approach.",
  "U07-B-gif-std-ratio", r"Needs the inequality $\sin x < x < \tan x$ applied inside the greatest integer function.",
  check=_c27, values=[TT, FF, FT, TF], cognitive="Analysis")


def _c28():
    lo = limit(x*(1/x - 1), x, 0)
    hi = limit(x*(1/x), x, 0)
    assert lo == hi
    return lo
q("U07-B-028", TOP, "Limit with greatest integer by squeezing", "Medium", "Conceptual/application MCQ",
  r"$\lim_{x \to 0} x\left[\frac{1}{x}\right]$, " + GIF + r", equals",
  r"$1$",
  [(r"$0$", r"Treats $x[\cdot]$ as $0 \times$ (something bounded), but $\left[\frac{1}{x}\right]$ is unbounded."),
   (r"$-1$", r"Uses $\left[\frac{1}{x}\right] \approx -\frac{1}{x}$ for $x < 0$, mishandling the sign."),
   (r"does not exist", r"Assumes the jumps of the greatest integer function make the left and right limits differ.")],
  r"Since $\frac{1}{x} - 1 < \left[\frac{1}{x}\right] \le \frac{1}{x}$, for $x > 0$ we get $1 - x < x\left[\frac{1}{x}\right] \le 1$, and for $x < 0$ the inequalities reverse to $1 \le x\left[\frac{1}{x}\right] < 1 - x$. Both bounds tend to $1$, so by the sandwich theorem the limit is $1$.",
  r"Treating $\left[\frac{1}{x}\right]$ as bounded, or expecting the jumps to destroy the limit.",
  "U07-B-gif-squeeze", r"Sandwich argument on both sides of $0$.",
  check=_c28, values=[1, 0, -1, DNE], cognitive="Analysis")


def _c29():
    f = (exp(1/x) - 1)/(exp(1/x) + 1)
    s1 = lim2(f, 0) == 1
    s2 = limit(f, x, 0, '-') == -1
    return (bool(s1), bool(s2))
q("U07-B-029", TOP, "One-sided limits with exponential terms", "Medium", "Statement-based MCQ",
  r"Let $f(x) = \frac{e^{1/x} - 1}{e^{1/x} + 1}$ for $x \ne 0$. Statement I: $\lim_{x \to 0} f(x) = 1$. Statement II: $\lim_{x \to 0^-} f(x) = -1$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Takes the right-hand limit $1$ as the two-sided limit."),
   (ST_TF, r"Uses $e^{1/x} \to \infty$ on both sides of $0$."),
   (ST_FF, r"Correctly rejects Statement I, but also takes $e^{1/x} \to \infty$ from the left.")],
  r"As $x \to 0^+$, $e^{1/x} \to \infty$ and $f(x) = \frac{1 - e^{-1/x}}{1 + e^{-1/x}} \to 1$. As $x \to 0^-$, $e^{1/x} \to 0$ and $f(x) \to \frac{-1}{1} = -1$. The one-sided limits differ, so the limit at $0$ does not exist: Statement I is false and Statement II is true.",
  r"Not distinguishing $e^{1/x}$ for $x \to 0^+$ and $x \to 0^-$.",
  "U07-B-exp-one-sided", r"Two one-sided limits and the existence criterion.",
  check=_c29, values=[FT, TT, TF, FF], cognitive="Understanding")

q("U07-B-030", TOP, "Splitting into standard limits", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \frac{e^{x^2} - \cos x}{x^2}$ equals",
  r"$\frac{3}{2}$",
  [(r"$\frac{1}{2}$", r"Splits as $\frac{e^{x^2} - 1}{x^2} - \frac{1 - \cos x}{x^2}$, subtracting instead of adding."),
   (r"$1$", r"Treats $\cos x$ as $1$, keeping only $\frac{e^{x^2} - 1}{x^2}$."),
   (r"$2$", r"Uses $1 - \cos x \approx x^2$.")],
  r"Write $e^{x^2} - \cos x = (e^{x^2} - 1) + (1 - \cos x)$. Then the limit is $\lim \frac{e^{x^2}-1}{x^2} + \lim \frac{1 - \cos x}{x^2} = 1 + \frac{1}{2} = \frac{3}{2}$.",
  r"Sign or approximation slips when splitting into standard limits.",
  "U07-B-split-std", r"Add and subtract $1$, then two standard limits.",
  check=lambda: limit((exp(x**2) - cos(x))/x**2, x, 0), values=[Rational(3, 2), Rational(1, 2), 1, 2], cognitive="Application")

q("U07-B-031", TOP, "Exponential limit at infinity", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to \infty} \frac{3^{x+1} - 2^{x}}{3^{x} + 2^{x+1}}$ equals",
  r"$3$",
  [(r"$-\frac{1}{2}$", r"Divides through by $2^x$ and treats $\left(\frac{3}{2}\right)^x \to 0$."),
   (r"$1$", r"Keeps only $3^x$ terms but ignores the coefficient $3$ in $3^{x+1}$."),
   (r"$\frac{1}{3}$", r"Inverts the ratio of the dominant terms.")],
  r"Divide numerator and denominator by $3^x$: $\frac{3 - (2/3)^x}{1 + 2(2/3)^x}$. Since $\left(\frac{2}{3}\right)^x \to 0$, the limit is $3$.",
  r"Dividing by the non-dominant exponential and mishandling which ratio tends to $0$.",
  "U07-B-infinity-exp", r"Identify the dominant term and divide; two short steps.",
  check=lambda: limit((3**(x + 1) - 2**x)/(3**x + 2**(x + 1)), x, oo), values=[3, Rational(-1, 2), 1, Rational(1, 3)], cognitive="Application")

q("U07-B-032", TOP, "Limit involving 1 - cos", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \frac{(1 - \cos 2x)(3 + \cos x)}{x \tan 4x}$ equals",
  r"$2$",
  [(r"$4$", r"Uses $1 - \cos 2x \approx (2x)^2 = 4x^2$, dropping the $\frac{1}{2}$."),
   (r"$\frac{3}{2}$", r"Takes $3 + \cos x \to 3$, forgetting $\cos 0 = 1$."),
   (r"$8$", r"Replaces $\tan 4x$ by $x$, missing the factor $4$.")],
  r"$1 - \cos 2x = 2\sin^2 x \approx 2x^2$, $3 + \cos x \to 4$ and $x\tan 4x \approx 4x^2$. So the limit is $\frac{2 \cdot 4}{4} = 2$.",
  r"Slips in the small-angle forms or the constant factor.",
  "U07-B-one-minus-cos", r"Three factors each needing a separate standard limit.",
  check=lambda: limit((1 - cos(2*x))*(3 + cos(x))/(x*tan(4*x)), x, 0), values=[2, 4, Rational(3, 2), 8], cognitive="Application",
  numerical=dict(question=r"The value of $\lim_{x \to 0} \frac{(1 - \cos 2x)(3 + \cos x)}{x \tan 4x}$ is", answer=2))


def _c33():
    L = limit(x*((x**2 + kr*x + 1)/(x**2 + 2*x - 3) - 1), x, oo)
    return solve(Eq(L, 5), kr)[0]
q("U07-B-033", TOP, "Parameter in a 1 to the power infinity limit", "Medium", "Inverse/parameter MCQ",
  r"If $\lim_{x \to \infty} \left(\frac{x^2 + kx + 1}{x^2 + 2x - 3}\right)^{x} = e^{5}$, where $k$ is a real constant, then $k$ equals",
  r"$7$",
  [(r"$5$", r"Ignores the $2x$ in the denominator, taking the exponent limit as $k$."),
   (r"$3$", r"Takes the exponent limit as $k + 2$."),
   (r"$-3$", r"Subtracts in the wrong order, taking the exponent limit as $2 - k$.")],
  r"$1^\infty$ form: the limit is $e^{L}$ with $L = \lim x \cdot \frac{(k-2)x + 4}{x^2 + 2x - 3} = k - 2$. Setting $k - 2 = 5$ gives $k = 7$.",
  r"Mishandling the base minus $1$ in the $1^\infty$ formula.",
  "U07-B-one-inf-param", r"Reverse use of the $1^\infty$ formula with a parameter.",
  check=_c33, values=[7, 5, 3, -3], cognitive="Application",
  numerical=dict(question=r"If $\lim_{x \to \infty} \left(\frac{x^2 + kx + 1}{x^2 + 2x - 3}\right)^{x} = e^{5}$, where $k$ is a real constant, then the value of $k$ is", answer=7))

q("U07-B-034", TOP, "Two-sided limit with greatest integer function", "Medium", "Conceptual/application MCQ",
  r"Let $f(x) = [x] + [-x]$, " + GIF + r". Then $\lim_{x \to 2} f(x)$ equals",
  r"$-1$",
  [(r"$0$", r"Gives the value $f(2) = 2 + (-2) = 0$ instead of the limit."),
   (r"$1$", r"Uses $[-x] = -[x] + 1$ for non-integer $x$ instead of $-[x] - 1$."),
   (r"does not exist", r"Assumes the jumps of $[x]$ and $[-x]$ at $2$ make the one-sided limits different.")],
  r"For $x$ just above $2$: $[x] = 2$, $[-x] = -3$, sum $-1$. For $x$ just below $2$: $[x] = 1$, $[-x] = -2$, sum $-1$. Both one-sided limits are $-1$, so the limit is $-1$ (even though $f(2) = 0$).",
  r"Confusing the limit with the function value at an integer.",
  "U07-B-gif-one-sided", r"Two one-sided evaluations; trap in the function value.",
  check=lambda: lim2(floor(x) + floor(-x), 2), values=[-1, 0, 1, DNE], cognitive="Analysis")

q("U07-B-035", TOP, "One-sided limit with modulus", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 0^-} \frac{\sqrt{1 - \cos 2x}}{x}$ equals",
  r"$-\sqrt{2}$",
  [(r"$\sqrt{2}$", r"Writes $\sqrt{2\sin^2 x} = \sqrt{2}\sin x$ instead of $\sqrt{2}|\sin x|$."),
   (r"$-1$", r"Uses $1 - \cos 2x \approx x^2$, getting $\frac{|x|}{x}$."),
   (r"$-\frac{1}{\sqrt{2}}$", r"Uses $1 - \cos 2x \approx \frac{x^2}{2}$, the form for $1 - \cos x$.")],
  r"$\sqrt{1 - \cos 2x} = \sqrt{2\sin^2 x} = \sqrt{2}|\sin x|$. For $x < 0$ near $0$, $|\sin x| = -\sin x$, so the expression is $-\sqrt{2}\frac{\sin x}{x} \to -\sqrt{2}$.",
  r"Writing $\sqrt{\sin^2 x} = \sin x$ on the left of $0$.",
  "U07-B-modulus-one-sided", r"Identity, then the hidden modulus on one side.",
  check=lambda: limit(sqrt(1 - cos(2*x))/x, x, 0, '-'), values=[-sqrt(2), sqrt(2), -1, -1/sqrt(2)], cognitive="Analysis")

q("U07-B-036", TOP, "Logarithmic limit at infinity", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to \infty} x\left(\log_e(x + 2) - \log_e x\right)$ equals",
  r"$2$",
  [(r"$0$", r"Notes $\log_e(x+2) - \log_e x \to 0$ and takes the product as $0$, ignoring the $\infty \cdot 0$ form."),
   (r"$1$", r"Uses $\log_e\left(1 + \frac{2}{x}\right) \approx \frac{1}{x}$."),
   (r"$\frac{1}{2}$", r"Uses $\log_e\left(1 + \frac{2}{x}\right) \approx \frac{1}{2x}$, inverting the coefficient.")],
  r"$x\log_e\frac{x+2}{x} = x\log_e\left(1 + \frac{2}{x}\right) = 2 \cdot \frac{\log_e(1 + u)}{u}$ with $u = \frac{2}{x} \to 0$. So the limit is $2$.",
  r"Treating $\infty \cdot 0$ as $0$.",
  "U07-B-infinity-log", r"Convert to a standard log limit by substitution.",
  check=lambda: limit(x*(log(x + 2) - log(x)), x, oo), values=[2, 0, 1, Rational(1, 2)], cognitive="Application")


def _c37():
    t = Symbol('t', positive=True)
    L = limit((1 - cos(x)*cos(2*x))/sin(sqrt(t)*x)**2, x, 0)
    return solve(Eq(L, Rational(1, 2)), t)[0]
q("U07-B-037", TOP, "Parameter from a trigonometric limit", "Medium", "Inverse/parameter MCQ",
  r"If $\lim_{x \to 0} \frac{1 - \cos x \cos 2x}{\sin^2 kx} = \frac{1}{2}$, where $k$ is a nonzero real constant, then $k^2$ equals",
  r"$5$",
  [(r"$10$", r"Uses $1 - \cos \theta \approx \theta^2$, dropping the $\frac{1}{2}$, so the numerator becomes $5x^2$ and $\frac{5}{k^2} = \frac{1}{2}$."),
   (r"$3$", r"Takes $1 - \cos 2x \approx \frac{2x^2}{2}$ without squaring the $2$, so the numerator becomes $\frac{3x^2}{2}$ and $\frac{3}{2k^2} = \frac{1}{2}$."),
   (r"$9$", r"Treats $\cos x \cos 2x$ as $\cos 3x$, so the numerator becomes $\frac{9x^2}{2}$ and $\frac{9}{2k^2} = \frac{1}{2}$.")],
  r"Write $1 - \cos x \cos 2x = (1 - \cos x) + \cos x\,(1 - \cos 2x)$. Dividing by $x^2$, this tends to $\frac{1}{2} + 1 \cdot 2 = \frac{5}{2}$, while $\frac{\sin^2 kx}{x^2} \to k^2$. So the limit is $\frac{5}{2k^2} = \frac{1}{2}$, giving $k^2 = 5$.",
  r"Mishandling $1 - \cos x \cos 2x$ by treating the product of cosines as a single cosine or slipping in $1 - \cos \theta \approx \frac{\theta^2}{2}$.",
  "U07-B-param-cos-product", r"Splitting a product of cosines into two standard limits, then solving for a parameter placed in the denominator.",
  check=_c37, values=[5, 10, 3, 9], cognitive="Application",
  numerical=dict(question=r"If $\lim_{x \to 0} \frac{1 - \cos x \cos 2x}{\sin^2 kx} = \frac{1}{2}$, where $k$ is a nonzero real constant, then the value of $k^2$ is", answer=5))

q("U07-B-038", TOP, "Limit of the form (x^m - 1)/(x^n - 1)", "Medium", "Multi-step computation MCQ",
  r"$\lim_{x \to 1} \frac{x^{1/3} - 1}{x^{1/4} - 1}$ equals",
  r"$\frac{4}{3}$",
  [(r"$\frac{3}{4}$", r"Inverts the ratio $\frac{1/3}{1/4}$."),
   (r"$\frac{1}{12}$", r"Multiplies $\frac{1}{3}$ and $\frac{1}{4}$ instead of dividing."),
   (r"$1$", r"Cancels the $-1$ terms and treats the ratio of roots of $1$ as $1$.")],
  r"Divide numerator and denominator by $x - 1$: $\lim \frac{x^{1/3}-1}{x-1} = \frac{1}{3}$ and $\lim \frac{x^{1/4}-1}{x-1} = \frac{1}{4}$. The limit is $\frac{1/3}{1/4} = \frac{4}{3}$.",
  r"Combining the two $n a^{n-1}$ values with the wrong operation.",
  "U07-B-xn-an", r"Two uses of $\frac{x^n - a^n}{x - a} \to na^{n-1}$ with fractional $n$.",
  check=lambda: limit((x**Rational(1, 3) - 1)/(x**Rational(1, 4) - 1), x, 1), values=[Rational(4, 3), Rational(3, 4), Rational(1, 12), 1], cognitive="Application")

q("U07-B-039", TOP, "Greatest integer of standard trigonometric ratios", "Medium", "Conceptual/application MCQ",
  r"$\lim_{x \to 0} \left(\left[\frac{100 \sin x}{x}\right] + \left[\frac{100 \tan x}{x}\right]\right)$, " + GIF + r", equals",
  r"$199$",
  [(r"$200$", r"Replaces each ratio by its limit $100$ before taking the greatest integer."),
   (r"$198$", r"Assumes both $\frac{100\sin x}{x}$ and $\frac{100\tan x}{x}$ approach $100$ from below."),
   (r"$100$", r"Pulls the constant out, writing $\left[\frac{100\sin x}{x}\right] = 100\left[\frac{\sin x}{x}\right] \to 0$ and $\left[\frac{100\tan x}{x}\right] = 100\left[\frac{\tan x}{x}\right] \to 100$.")],
  r"Near $0$ (both sides), $\frac{\sin x}{x} < 1 < \frac{\tan x}{x}$. So $\frac{100\sin x}{x}$ is just below $100$ with greatest integer $99$, and $\frac{100\tan x}{x}$ is just above $100$ with greatest integer $100$. The limit is $99 + 100 = 199$.",
  r"Taking $[\lim f]$ for $\lim [f]$.",
  "U07-B-gif-std-ratio", r"Requires the direction of approach of two ratios inside greatest integer functions.",
  check=lambda: floor_limit(100*sin(x)/x) + floor_limit(100*tan(x)/x), values=[199, 200, 198, 100], cognitive="Analysis",
  numerical=dict(question=r"The value of $\lim_{x \to 0} \left(\left[\frac{100 \sin x}{x}\right] + \left[\frac{100 \tan x}{x}\right]\right)$, " + GIF + r", is", answer=199))

# =================================================================== DIFFICULT


def _c40():
    N = a_*exp(x) - b_*cos(x) + c_*exp(-x)
    s = series(N, x, 0, 3).removeO()
    sol = solve([s.coeff(x, 0), s.coeff(x, 1), s.coeff(x, 2) - 2], [a_, b_, c_], dict=True)[0]
    assert limit(N.subs(sol)/(x*sin(x)), x, 0) == 2
    return sol[b_]
q("U07-B-040", TOP, "Parameters from a limit by expansion", "Difficult", "Inverse/parameter MCQ",
  r"If $\lim_{x \to 0} \frac{a e^{x} - b \cos x + c e^{-x}}{x \sin x} = 2$, where $a, b, c$ are real constants, then $b$ equals",
  r"$2$",
  [(r"$1$", r"Uses $e^{\pm x} \approx 1 \pm x + x^2$ and $\cos x \approx 1 - x^2$ (no $\frac{1}{2}$ anywhere), so $a + b + c = 2$ with $b = 2a$, giving $a = \frac{1}{2}$, $b = 1$."),
   (r"$\frac{4}{3}$", r"Uses $\cos x \approx 1 - x^2$ but the correct exponential series, so $\frac{a}{2} + b + \frac{c}{2} = 2$, i.e. $3a = 2$, $b = \frac{4}{3}$."),
   (r"$4$", r"Finds $a + b + c = 4$ correctly and reports this sum instead of $b$.")],
  r"Expand: $a(1 + x + \frac{x^2}{2}) - b(1 - \frac{x^2}{2}) + c(1 - x + \frac{x^2}{2}) + \ldots$. Since $x\sin x \approx x^2$, need $a - b + c = 0$ and $a - c = 0$, and then the limit is $\frac{a + b + c}{2} = 2$. So $a = c$, $b = 2a$, $4a = 4$, giving $a = c = 1$ and $b = 2$.",
  r"Dropping the $\frac{1}{2}$ in second-order terms of $e^x$ or $\cos x$.",
  "U07-B-param-series", r"Three conditions from a series expansion; three unknowns.",
  check=_c40, values=[2, 1, Rational(4, 3), 4], cognitive="Analysis",
  numerical=dict(question=r"If $\lim_{x \to 0} \frac{a e^{x} - b \cos x + c e^{-x}}{x \sin x} = 2$, where $a, b, c$ are real constants, then the value of $b$ is", answer=2))


def _c41():
    N = x*(1 + a_*cos(x)) - b_*sin(x)
    s = series(N, x, 0, 5).removeO()
    sol = solve([s.coeff(x, 1), s.coeff(x, 3) - 1], [a_, b_], dict=True)[0]
    assert limit(N.subs(sol)/x**3, x, 0) == 1
    return sol[a_] + sol[b_]
q("U07-B-041", TOP, "Parameters from a limit by expansion", "Difficult", "Inverse/parameter MCQ",
  r"If $\lim_{x \to 0} \frac{x(1 + a\cos x) - b\sin x}{x^3} = 1$, where $a, b$ are real constants, then $a + b$ equals",
  r"$-4$",
  [(r"$-7$", r"Uses $\sin x \approx x - \frac{x^3}{3}$, so $-\frac{a}{2} + \frac{b}{3} = 1$, giving $a = -4$, $b = -3$."),
   (r"$-1$", r"Uses $\cos x \approx 1 - x^2$, so $-a + \frac{b}{6} = 1$, giving $a = -1$, $b = 0$."),
   (r"$-\frac{5}{2}$", r"Uses $\sin x \approx x + \frac{x^3}{6}$, so $-\frac{a}{2} - \frac{b}{6} = 1$, giving $a = -\frac{7}{4}$, $b = -\frac{3}{4}$.")],
  r"Expand: $x + ax\left(1 - \frac{x^2}{2}\right) - b\left(x - \frac{x^3}{6}\right) + \ldots = (1 + a - b)x + \left(-\frac{a}{2} + \frac{b}{6}\right)x^3 + \ldots$. So $1 + a - b = 0$ and $-\frac{a}{2} + \frac{b}{6} = 1$. With $b = 1 + a$: $-3a + 1 + a = 6$, so $a = -\frac{5}{2}$, $b = -\frac{3}{2}$, and $a + b = -4$.",
  r"Wrong coefficients in the series of $\sin x$ or $\cos x$.",
  "U07-B-param-series", r"Expansion to third order, two simultaneous conditions.",
  check=_c41, values=[-4, -7, -1, Rational(-5, 2)], cognitive="Analysis")

q("U07-B-042", TOP, "Limits of the form 1 to the power infinity", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \left(\frac{1 + \tan x}{1 + \sin x}\right)^{\frac{1}{x^3}}$ equals",
  r"$e^{\frac{1}{2}}$",
  [(r"$1$", r"Replaces $\tan x$ and $\sin x$ by $x$, so the base minus $1$ is taken as $0$."),
   (r"$e$", r"Takes $\tan x - \sin x \approx x^3$, dropping the $\frac{1}{2}$."),
   (r"$e^{\frac{1}{6}}$", r"Takes $\tan x - \sin x \approx x - \sin x \approx \frac{x^3}{6}$, treating $\tan x$ as $x$.")],
  r"$1^\infty$ form: $L = \lim \frac{1}{x^3}\cdot\frac{\tan x - \sin x}{1 + \sin x}$. Since $\tan x - \sin x = \tan x(1 - \cos x) \approx \frac{x^3}{2}$ and $1 + \sin x \to 1$, $L = \frac{1}{2}$. The limit is $e^{1/2}$.",
  r"Replacing $\tan x$ and $\sin x$ by $x$ inside a difference.",
  "U07-B-one-inf-trig", r"$1^\infty$ form whose exponent needs a third-order trigonometric limit.",
  check=lambda: limit(((1 + tan(x))/(1 + sin(x)))**(1/x**3), x, 0), values=[exp(Rational(1, 2)), 1, E, exp(Rational(1, 6))], cognitive="Analysis")


def _c43():
    r3 = sqrt(3)
    lo = limit(summation(kk*r3 - 1, (kk, 1, n))/n**2, n, oo)
    hi = limit(summation(kk*r3, (kk, 1, n))/n**2, n, oo)
    assert simplify(lo - hi) == 0
    return hi
q("U07-B-043", TOP, "Limit with greatest integer by squeezing", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{n \to \infty} \frac{[\sqrt{3}] + [2\sqrt{3}] + [3\sqrt{3}] + \cdots + [n\sqrt{3}]}{n^2}$, " + GIF + r", equals",
  r"$\frac{\sqrt{3}}{2}$",
  [(r"$\sqrt{3}$", r"Squeezes correctly but uses $\sum_{k=1}^{n} k \approx n^2$ instead of $\frac{n^2}{2}$."),
   (r"$\frac{1}{2}$", r"Uses $[k\sqrt{3}] = k[\sqrt{3}] = k$, so the sum is $\frac{n(n+1)}{2}$."),
   (r"$0$", r"Splits into $\sum \frac{[k\sqrt{3}]}{n^2}$ and lets each term tend to $0$, ignoring that the number of terms grows.")],
  r"Since $k\sqrt{3} - 1 < [k\sqrt{3}] \le k\sqrt{3}$, summing gives $\frac{\sqrt{3}n(n+1)}{2} - n < S_n \le \frac{\sqrt{3}n(n+1)}{2}$. Dividing by $n^2$, both bounds tend to $\frac{\sqrt{3}}{2}$, so by the sandwich theorem the limit is $\frac{\sqrt{3}}{2}$.",
  r"Using $[kx] = k[x]$, which is false for non-integer $x$.",
  "U07-B-gif-squeeze", r"Requires bounding a sum of greatest integers and the sandwich theorem.",
  check=_c43, values=[sqrt(3)/2, sqrt(3), Rational(1, 2), 0], cognitive="Analysis")

q("U07-B-044", TOP, "Logarithmic limit at infinity by expansion", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to \infty} \left(x - x^2 \log_e\left(1 + \frac{1}{x}\right)\right)$ equals",
  r"$\frac{1}{2}$",
  [(r"$0$", r"Uses only $\log_e\left(1 + \frac{1}{x}\right) \approx \frac{1}{x}$, so the bracket is taken as $x - x = 0$."),
   (r"$-\frac{1}{2}$", r"Uses $\log_e(1 + u) \approx u + \frac{u^2}{2}$, with the wrong sign on the second term."),
   (r"$\frac{1}{3}$", r"Takes the coefficient of the third term $\frac{u^3}{3}$ of the logarithm series instead of the second.")],
  r"Put $u = \frac{1}{x} \to 0^+$. The expression is $\frac{u - \log_e(1 + u)}{u^2}$. Since $\log_e(1+u) = u - \frac{u^2}{2} + \frac{u^3}{3} - \ldots$, this equals $\frac{1}{2} - \frac{u}{3} + \ldots \to \frac{1}{2}$.",
  r"Stopping the log series at first order in an $\infty - \infty$ form.",
  "U07-B-log-series", r"Substitution to $u \to 0$ plus a second-order expansion; first-order work gives a wrong answer.",
  check=lambda: limit(x - x**2*log(1 + 1/x), x, oo), values=[Rational(1, 2), 0, Rational(-1, 2), Rational(1, 3)], cognitive="Analysis")

q("U07-B-045", TOP, "Composite trigonometric limit", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \frac{\sin\left(\pi \cos^2 x\right)}{x^2}$ equals",
  r"$\pi$",
  [(r"$-\pi$", r"Writes $\sin(\pi - \theta) = -\sin \theta$."),
   (r"$2\pi$", r"Writes $\cos^2 x = 1 - 2\sin^2 x$ (confusing it with $\cos 2x$), getting $\sin(2\pi\sin^2 x) \approx 2\pi x^2$."),
   (r"$\frac{\pi}{2}$", r"Writes $\pi\cos^2 x = \frac{\pi}{2}(1 + \cos 2x)$ and then uses $1 - \cos 2x \approx x^2$.")],
  r"$\pi \cos^2 x = \pi - \pi\sin^2 x$, so $\sin(\pi\cos^2 x) = \sin(\pi\sin^2 x)$. Hence the expression is $\frac{\sin(\pi\sin^2 x)}{\pi\sin^2 x}\cdot\frac{\pi\sin^2 x}{x^2} \to 1 \cdot \pi = \pi$.",
  r"Sign slip in $\sin(\pi - \theta)$ or a wrong identity for $\cos^2 x$.",
  "U07-B-trig-composite", r"Needs an angle reduction before any standard limit applies.",
  check=lambda: limit(sin(pi*cos(x)**2)/x**2, x, 0), values=[pi, -pi, 2*pi, pi/2], cognitive="Analysis")


def _c46():
    f_in = limit((Rational(1, 2)**(2*n) - 1)/(Rational(1, 2)**(2*n) + 1), n, oo)   # value for |x| < 1
    f_out = limit((Integer(2)**(2*n) - 1)/(Integer(2)**(2*n) + 1), n, oo)          # value for |x| > 1
    left, right = f_in, f_out
    return (bool(left == -1), bool(left == right))
q("U07-B-046", TOP, "One-sided limits of a function defined by a limit", "Difficult", "Statement-based MCQ",
  r"Let $f(x) = \lim_{n \to \infty} \frac{x^{2n} - 1}{x^{2n} + 1}$ for $x \in \mathbb{R}$. Statement I: $\lim_{x \to 1^-} f(x) = -1$. Statement II: $\lim_{x \to 1} f(x)$ exists. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Takes $f(x) = -1$ on both sides of $1$, overlooking that $x^{2n} \to \infty$ for $x > 1$."),
   (ST_FT, r"Uses $f(1) = 0$ as the left-hand limit and assumes the limit exists."),
   (ST_FF, r"Uses $f(1) = 0$ as the left-hand limit, and correctly rejects Statement II.")],
  r"For $|x| < 1$, $x^{2n} \to 0$ so $f(x) = -1$; for $|x| > 1$, divide by $x^{2n}$ to get $f(x) = 1$; and $f(\pm 1) = 0$. So $\lim_{x \to 1^-} f(x) = -1$ and $\lim_{x \to 1^+} f(x) = 1$. Statement I is true; the one-sided limits differ, so Statement II is false.",
  r"Using the value at the point, or the same branch on both sides.",
  "U07-B-limit-defined-fn", r"Function defined by a limit; casework on $|x|$, then one-sided limits.",
  check=_c46, values=[TF, TT, FT, FF], cognitive="Analysis")

q("U07-B-047", TOP, "Composite trigonometric limit", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \frac{\cos(\sin x) - \cos x}{x^4}$ equals",
  r"$\frac{1}{6}$",
  [(r"$\frac{1}{12}$", r"Writes $\cos P - \cos Q = -\sin\frac{P+Q}{2}\sin\frac{P-Q}{2}$, dropping the factor $2$."),
   (r"$-\frac{1}{6}$", r"Uses $\cos P - \cos Q = 2\sin\frac{P+Q}{2}\sin\frac{P-Q}{2}$, a sign error."),
   (r"$0$", r"Replaces $\sin x$ by $x$, making the numerator $0$.")],
  r"$\cos(\sin x) - \cos x = -2\sin\frac{\sin x + x}{2}\sin\frac{\sin x - x}{2}$. As $x \to 0$, $\frac{\sin x + x}{2} \approx x$ and $\frac{\sin x - x}{2} \approx -\frac{x^3}{12}$. So the numerator is $\approx -2 \cdot x \cdot \left(-\frac{x^3}{12}\right) = \frac{x^4}{6}$, and the limit is $\frac{1}{6}$.",
  r"Replacing $\sin x$ by $x$ in a difference that cancels at leading order.",
  "U07-B-trig-composite", r"Sum-to-product identity plus a third-order estimate of $x - \sin x$.",
  check=lambda: limit((cos(sin(x)) - cos(x))/x**4, x, 0), values=[Rational(1, 6), Rational(1, 12), Rational(-1, 6), 0], cognitive="Analysis")


def _c48():
    e = sqrt(x**2 - x + 1)
    a = limit(e/x, x, oo)
    b = limit(e - a*x, x, oo)
    return (a, b)
q("U07-B-048", TOP, "Parameters from a limit at infinity", "Difficult", "Inverse/parameter MCQ",
  r"If $\lim_{x \to \infty} \left(\sqrt{x^2 - x + 1} - ax - b\right) = 0$, where $a, b$ are real constants, then $(a, b)$ equals",
  r"$\left(1, -\frac{1}{2}\right)$",
  [(r"$\left(1, \frac{1}{2}\right)$", r"Expands $\sqrt{x^2 - x + 1} \approx x + \frac{1}{2}$, losing the sign of the $-x$ term."),
   (r"$\left(-1, \frac{1}{2}\right)$", r"Takes $\sqrt{x^2} = -x$, so $\sqrt{x^2 - x + 1} \approx -x\left(1 - \frac{1}{2x}\right) = -x + \frac{1}{2}$."),
   (r"$(1, -1)$", r"Uses $\sqrt{1 + u} \approx 1 + u$, forgetting the $\frac{1}{2}$, so $b = -1$.")],
  r"For large positive $x$, $\sqrt{x^2 - x + 1} = x\sqrt{1 - \frac{1}{x} + \frac{1}{x^2}} = x - \frac{1}{2} + O\left(\frac{1}{x}\right)$. For the difference to tend to $0$ we need $a = 1$ (else it diverges), and then $b = \lim\left(\sqrt{x^2 - x + 1} - x\right) = \lim \frac{-x + 1}{\sqrt{x^2-x+1} + x} = -\frac{1}{2}$.",
  r"Losing the factor $\frac{1}{2}$ or a sign in the binomial expansion.",
  "U07-B-infinity-param", r"Two parameters fixed in sequence: growth rate, then constant term.",
  check=_c48, values=[(1, Rational(-1, 2)), (1, Rational(1, 2)), (-1, Rational(1, 2)), (1, -1)], cognitive="Analysis")

q("U07-B-049", TOP, "Limits of the form 1 to the power infinity", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to 1} (2 - x)^{\tan \frac{\pi x}{2}}$ equals",
  r"$e^{\frac{2}{\pi}}$",
  [(r"$e^{-\frac{2}{\pi}}$", r"Takes the base minus $1$ as $x - 1$ instead of $1 - x$."),
   (r"$e^{\frac{\pi}{2}}$", r"Approximates $\cot\frac{\pi h}{2}$ by $\frac{\pi}{2h}$ instead of $\frac{2}{\pi h}$, so $L = \frac{\pi}{2}$."),
   (r"$1$", r"Treats the $1^\infty$ form as $1$.")],
  r"$1^\infty$ form: $L = \lim_{x \to 1}(1 - x)\tan\frac{\pi x}{2}$. Put $h = 1 - x$: $\tan\left(\frac{\pi}{2} - \frac{\pi h}{2}\right) = \cot\frac{\pi h}{2} \approx \frac{2}{\pi h}$, so $L = \lim h \cdot \frac{2}{\pi h} = \frac{2}{\pi}$. The limit is $e^{2/\pi}$.",
  r"Sign or reciprocal slips when converting $\tan$ near $\frac{\pi}{2}$ to $\cot$ of a small angle.",
  "U07-B-one-inf-shift", r"$1^\infty$ form at a non-zero point with a shift and a cotangent approximation.",
  check=lambda: lim2((2 - x)**tan(pi*x/2), 1), values=[exp(2/pi), exp(-2/pi), exp(pi/2), 1], cognitive="Analysis")


def _c50():
    S = summation(kk**2, (kk, 1, n))
    base = 3*S/n**3
    L = limit(n*(base - 1), n, oo)
    direct = limit(base**n, n, oo)
    assert simplify(direct - exp(L)) == 0
    return exp(L)
q("U07-B-050", TOP, "Limit at infinity of a sum", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{n \to \infty} \left(\frac{3\left(1^2 + 2^2 + \cdots + n^2\right)}{n^3}\right)^{n}$ equals",
  r"$e^{3/2}$",
  [(r"$1$", r"Keeps only the leading term $\frac{n^3}{3}$ of the sum, so the base is taken as exactly $1$ and $1^n = 1$."),
   (r"$e$", r"Approximates $\frac{n(n+1)(2n+1)}{6}$ by $\frac{n(n+1)(2n)}{6} = \frac{n^3 + n^2}{3}$, dropping the $1$ in $2n+1$, so the base is $1 + \frac{1}{n}$."),
   (r"$\sqrt{e}$", r"Approximates $\frac{n(n+1)(2n+1)}{6}$ by $\frac{n \cdot n(2n+1)}{6} = \frac{2n^3 + n^2}{6}$, dropping the $1$ in $n+1$, so the base is $1 + \frac{1}{2n}$.")],
  r"$1^2 + \cdots + n^2 = \frac{n(n+1)(2n+1)}{6} = \frac{2n^3 + 3n^2 + n}{6}$, so the base is $\frac{3}{n^3} \cdot \frac{2n^3 + 3n^2 + n}{6} = 1 + \frac{3}{2n} + \frac{1}{2n^2} \to 1$. This is a $1^\infty$ form, so the limit is $e^{L}$ with $L = \lim n\left(\frac{3}{2n} + \frac{1}{2n^2}\right) = \frac{3}{2}$. Hence the limit is $e^{3/2}$.",
  r"Keeping only the leading term of the sum, or dropping a lower-order term, in a $1^\infty$ form where the second term decides the answer.",
  "U07-B-infinity-sum", r"Combines the exact sum-of-squares formula with the $1^\infty$ rule; the answer depends on the second-order term of the sum, which any approximation of the sum destroys.",
  check=_c50, values=[exp(Rational(3, 2)), 1, E, sqrt(E)], cognitive="Analysis")

q("U07-B-051", TOP, "Logarithmic limit by expansion", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to 0} \frac{\log_e(1 + 2x) - 2\log_e(1 + x)}{x^2}$ equals",
  r"$-1$",
  [(r"$0$", r"Uses $\log_e(1 + u) \approx u$ for both terms, so the numerator is taken as $0$."),
   (r"$-3$", r"Adds the second-order terms with the same sign: $-2 - 1$."),
   (r"$1$", r"Gets the second-order terms with reversed signs, $+2x^2$ and $+x^2$, so the numerator is $x^2$.")],
  r"$\log_e(1 + 2x) = 2x - 2x^2 + \ldots$ and $2\log_e(1 + x) = 2x - x^2 + \ldots$. The numerator is $-x^2 + \ldots$, so the limit is $-1$. (Equivalently, the numerator is $\log_e\frac{1+2x}{(1+x)^2} = \log_e\left(1 - \frac{x^2}{(1+x)^2}\right)$.)",
  r"Stopping at first order when the first-order terms cancel.",
  "U07-B-log-series", r"Leading terms cancel; second-order expansion needed.",
  check=lambda: limit((log(1 + 2*x) - 2*log(1 + x))/x**2, x, 0), values=[-1, 0, -3, 1], cognitive="Analysis")


def _c52():
    # x -> 0+ means t = 1/x -> +oo
    return limit(((1 + 2**t + 3**t)/3)**(1/t), t, oo)
q("U07-B-052", TOP, "Exponential limit with a dominant term", "Difficult", "Multi-step computation MCQ",
  r"$\lim_{x \to 0^+} \left(\frac{1^{1/x} + 2^{1/x} + 3^{1/x}}{3}\right)^{x}$ equals",
  r"$3$",
  [(r"$\sqrt[3]{6}$", r"Uses the result $\left(\frac{a^x + b^x + c^x}{3}\right)^{1/x} \to \sqrt[3]{abc}$, which holds for $x \to 0$ inside, not here."),
   (r"$2$", r"Takes the arithmetic mean of $1, 2, 3$."),
   (r"$1$", r"Treats the indeterminate form $\infty^0$ as $1$.")],
  r"Put $t = \frac{1}{x} \to \infty$. Then $\frac{1 + 2^t + 3^t}{3} = \frac{3^t}{3}\left(\left(\tfrac{1}{3}\right)^t + \left(\tfrac{2}{3}\right)^t + 1\right)$, so the expression equals $3 \cdot 3^{-1/t}\left(\left(\tfrac{1}{3}\right)^t + \left(\tfrac{2}{3}\right)^t + 1\right)^{1/t}$. As $t \to \infty$, $3^{-1/t} \to 1$ and the last factor tends to $1^0 = 1$. Hence the limit is $3$.",
  r"Confusing this with the $1^\infty$ power-mean limit.",
  "U07-B-power-mean", r"Factor out the dominant exponential; looks like a known $1^\infty$ pattern but is not.",
  check=_c52, values=[3, 6**Rational(1, 3), 2, 1], cognitive="Analysis")
