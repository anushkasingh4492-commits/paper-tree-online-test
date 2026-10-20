import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
x = Symbol('x', real=True)
TOPIC_F = "Fundamental integrals"
TOPIC_S = "Integration by substitution"
TOPIC_T = "Integration using trigonometric identities"
CI = r"(where $C$ is the constant of integration)"

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
STEM_TAIL = r" In the light of the above statements, choose the correct answer."


def AD(f, opts, pts=None):
    """Indefinite-integral check: check() returns the integrand, values are the
    derivatives of the four option antiderivatives. With pts, both are sampled at
    points inside the stated domain."""
    ds = [diff(o, x) for o in opts]
    if pts is None:
        return dict(check=lambda: f, values=ds)
    return dict(check=lambda: tuple(f.subs(x, p) for p in pts),
                values=[tuple(d.subs(x, p) for p in pts) for d in ds])


def fit(f, ansatz, params, pts, extra=None):
    """Solve diff(ansatz) = f for the (linearly entering) params using sample points,
    then confirm the identity at further points. Returns dict param -> exact value."""
    r = diff(ansatz, x) - f
    A = Matrix([[N(diff(r, p).subs(x, t), 60) for p in params] for t in pts])
    b = Matrix([-N(r.subs({p: 0 for p in params}).subs(x, t), 60) for t in pts])
    sol = A.solve(b) if A.shape[0] == A.shape[1] else (A.T*A).solve(A.T*b)
    vals = {p: nsimplify(sol[i], [sqrt(2), sqrt(3)], tolerance=1e-30) for i, p in enumerate(params)}
    for t in (extra or [Rational(7, 10), Rational(11, 10)]):
        res = N(r.subs(vals).subs(x, t), 40)
        assert abs(res) < 1e-25, ("fit failed", res)
    return vals


p_, q_, r_, k_, m_ = symbols('p q r k m')

# ================================================================ EASY (17)

o = [2*sqrt(x) + Rational(4, 3)*x**Rational(3, 2) + Rational(2, 5)*x**Rational(5, 2),
     2*sqrt(x) + Rational(2, 3)*x**Rational(3, 2) + Rational(2, 5)*x**Rational(5, 2),
     sqrt(x)/2 + 3*x**Rational(3, 2) + Rational(5, 2)*x**Rational(5, 2),
     Rational(2, 3)*x**Rational(3, 2) + Rational(4, 5)*x**Rational(5, 2) + Rational(2, 7)*x**Rational(7, 2)]
q("U08-A-001", TOPIC_F, "Power rule after expansion", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int \frac{(1+x)^2}{\sqrt{x}}\,dx$ " + CI + " equals",
  r"$2\sqrt{x} + \frac{4}{3}x^{3/2} + \frac{2}{5}x^{5/2} + C$",
  [(r"$2\sqrt{x} + \frac{2}{3}x^{3/2} + \frac{2}{5}x^{5/2} + C$", r"Expands $(1+x)^2$ as $1 + x + x^2$, losing the factor $2$ of the middle term, so $\int x^{1/2}dx = \frac{2}{3}x^{3/2}$ appears in place of $\frac{4}{3}x^{3/2}$."),
   (r"$\frac{1}{2}\sqrt{x} + 3x^{3/2} + \frac{5}{2}x^{5/2} + C$", r"Multiplies each term $x^{n}$ by the new exponent $n+1$ in place of dividing by it: $x^{-1/2} \to \frac{1}{2}x^{1/2}$, $2x^{1/2} \to 3x^{3/2}$, $x^{3/2} \to \frac{5}{2}x^{5/2}$."),
   (r"$\frac{2}{3}x^{3/2} + \frac{4}{5}x^{5/2} + \frac{2}{7}x^{7/2} + C$", r"Writes $\frac{1}{\sqrt{x}}$ as $x^{1/2}$, integrating $(1 + 2x + x^2)x^{1/2}$ term by term.")],
  r"$\frac{(1+x)^2}{\sqrt{x}} = x^{-1/2} + 2x^{1/2} + x^{3/2}$. Integrating term by term with $\int x^n dx = \frac{x^{n+1}}{n+1}$ gives $2x^{1/2} + \frac{4}{3}x^{3/2} + \frac{2}{5}x^{5/2} + C$.",
  r"Mishandling fractional exponents when dividing by $\sqrt{x}$.",
  "U08-A-power-expand", "Expand, then apply the power rule to three fractional powers.",
  cognitive="Application", source_class="XII",
  **AD((1 + x)**2/sqrt(x), o))

o = [-3**(-x)/log(3) - 2**(-x)/log(2), 3**(-x)/log(3) + 2**(-x)/log(2),
     -3**(-x)*log(3) - 2**(-x)*log(2), -3**(-x)/log(2) - 2**(-x)/log(3)]
q("U08-A-002", TOPIC_F, "Exponential functions", "Easy", "Single-step computation MCQ",
  r"$\int \frac{2^x + 3^x}{6^x}\,dx$ " + CI + " equals",
  r"$-\frac{3^{-x}}{\log_e 3} - \frac{2^{-x}}{\log_e 2} + C$",
  [(r"$\frac{3^{-x}}{\log_e 3} + \frac{2^{-x}}{\log_e 2} + C$", r"Uses $\int a^{-x}dx = \frac{a^{-x}}{\log_e a}$, ignoring the factor $-1$ from the exponent $-x$."),
   (r"$-3^{-x}\log_e 3 - 2^{-x}\log_e 2 + C$", r"Multiplies by $\log_e a$ in place of dividing by it, confusing the integral of $a^x$ with its derivative."),
   (r"$-\frac{3^{-x}}{\log_e 2} - \frac{2^{-x}}{\log_e 3} + C$", r"Splits correctly into $3^{-x} + 2^{-x}$ but divides each term by the logarithm of the base in the original numerator ($2^x$ gives $\log_e 2$, $3^x$ gives $\log_e 3$).")],
  r"$\frac{2^x}{6^x} = 3^{-x}$ and $\frac{3^x}{6^x} = 2^{-x}$. Since $\int a^{-x}dx = -\frac{a^{-x}}{\log_e a}$, the integral is $-\frac{3^{-x}}{\log_e 3} - \frac{2^{-x}}{\log_e 2} + C$.",
  r"Dropping the sign from the exponent $-x$ when integrating $a^{-x}$.",
  "U08-A-exp-base-split", "Split the fraction and use $\\int a^{-x}dx$ once per term.",
  cognitive="Application", source_class="XII",
  **AD((2**x + 3**x)/6**x, o))

o = [tan(x) - x, tan(x) + x, tan(x)**3/3, x - tan(x)]
q("U08-A-003", TOPIC_T, "Pythagorean identity", "Easy", "Single-step computation MCQ",
  r"$\int \tan^2 x\,dx$ " + CI + " equals",
  r"$\tan x - x + C$",
  [(r"$\tan x + x + C$", r"Writes $\tan^2 x = \sec^2 x + 1$, a sign slip in $1 + \tan^2 x = \sec^2 x$."),
   (r"$\frac{\tan^3 x}{3} + C$", r"Applies the power rule to $\tan x$ as if it were $x$, ignoring that $d(\tan x) = \sec^2 x\,dx$."),
   (r"$x - \tan x + C$", r"Writes $\tan^2 x = 1 - \sec^2 x$, reversing the identity.")],
  r"$\tan^2 x = \sec^2 x - 1$, so $\int \tan^2 x\,dx = \tan x - x + C$.",
  r"Using the power rule on a trigonometric function.",
  "U08-A-pythag-tan-square", "One identity followed by two standard integrals.",
  cognitive="Recall", source_class="XII",
  **AD(tan(x)**2, o))

o = [x/2 - sin(2*x)/4, x/2 + sin(2*x)/4, x/2 - sin(2*x)/2, sin(x)**3/3]
q("U08-A-004", TOPIC_T, "Half-angle reduction", "Easy", "Single-step computation MCQ",
  r"$\int \sin^2 x\,dx$ " + CI + " equals",
  r"$\frac{x}{2} - \frac{\sin 2x}{4} + C$",
  [(r"$\frac{x}{2} + \frac{\sin 2x}{4} + C$", r"Uses $\sin^2 x = \frac{1 + \cos 2x}{2}$, which is the identity for $\cos^2 x$."),
   (r"$\frac{x}{2} - \frac{\sin 2x}{2} + C$", r"Integrates $\frac{\cos 2x}{2}$ as $\frac{\sin 2x}{2}$, dropping the factor $\frac{1}{2}$ from the inner $2x$."),
   (r"$\frac{\sin^3 x}{3} + C$", r"Applies the power rule to $\sin x$ directly.")],
  r"$\sin^2 x = \frac{1 - \cos 2x}{2}$, so $\int \sin^2 x\,dx = \frac{x}{2} - \frac{\sin 2x}{4} + C$.",
  r"Mixing up the half-angle identities for $\sin^2 x$ and $\cos^2 x$.",
  "U08-A-half-angle-square", "One identity and two direct integrals.",
  cognitive="Recall", source_class="XII",
  **AD(sin(x)**2, o))

o = [exp(x**2)/2, exp(x**2), x**2*exp(x**2)/2, 2*exp(x**2)]
q("U08-A-005", TOPIC_S, "Direct substitution", "Easy", "Single-step computation MCQ",
  r"$\int x\,e^{x^2}\,dx$ " + CI + " equals",
  r"$\frac{1}{2}e^{x^2} + C$",
  [(r"$e^{x^2} + C$", r"Substitutes $t = x^2$ but uses $x\,dx = dt$, dropping the factor $\frac{1}{2}$."),
   (r"$\frac{x^2}{2}e^{x^2} + C$", r"Integrates the factor $x$ separately and multiplies by $e^{x^2}$ unchanged."),
   (r"$2e^{x^2} + C$", r"Inverts the substitution factor, writing $x\,dx = 2\,dt$ in place of $\frac{dt}{2}$.")],
  r"Put $t = x^2$, so $x\,dx = \frac{dt}{2}$. The integral becomes $\frac{1}{2}\int e^t dt = \frac{1}{2}e^{x^2} + C$.",
  r"Losing the constant factor in $dt = 2x\,dx$.",
  "U08-A-subst-chain", "Single substitution.",
  cognitive="Application", source_class="XII",
  **AD(x*exp(x**2), o))

o = [log(x)**3/3, log(x)**3, log(x)**3/(3*x), log(x)**3/6]
q("U08-A-006", TOPIC_S, "Substitution t = log x", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int \frac{(\log_e x)^2}{x}\,dx$ " + CI + " equals",
  r"$\frac{(\log_e x)^3}{3} + C$",
  [(r"$(\log_e x)^3 + C$", r"Raises the power to $3$ but forgets to divide by $3$."),
   (r"$\frac{(\log_e x)^3}{3x} + C$", r"Keeps the factor $\frac{1}{x}$ outside after integrating, not seeing that $\frac{dx}{x} = dt$ absorbs it."),
   (r"$\frac{(\log_e x)^3}{6} + C$", r"Inserts a factor $\frac{1}{2}$ by habit from $t = x^2$ substitutions, writing $\frac{dx}{x} = \frac{dt}{2}$.")],
  r"Put $t = \log_e x$, $dt = \frac{dx}{x}$. Then $\int t^2 dt = \frac{t^3}{3} = \frac{(\log_e x)^3}{3} + C$.",
  r"Mishandling the differential $\frac{dx}{x}$ in a logarithmic substitution.",
  "U08-A-subst-log", "Recognise $\\frac{1}{x}$ as $d(\\log_e x)$; one substitution.",
  cognitive="Application", source_class="XII",
  **AD(log(x)**2/x, o))

o = [-1/(3 + x*log(x)), 1/(3 + x*log(x)), -1/(3*(3 + x*log(x))**3), -(1 + log(x))/(3 + x*log(x))]
q("U08-A-007", TOPIC_S, "Recognising the derivative of the inner function", "Easy", "Single-step computation MCQ",
  r"For $x > 1$, $\int \frac{1 + \log_e x}{(3 + x\log_e x)^2}\,dx$ " + CI + " equals",
  r"$-\frac{1}{3 + x\log_e x} + C$",
  [(r"$\frac{1}{3 + x\log_e x} + C$", r"Uses $\int t^{-2}dt = t^{-1}$, dropping the minus sign."),
   (r"$-\frac{1}{3(3 + x\log_e x)^3} + C$", r"Lowers the power from $-2$ to $-3$ and divides by $-3$, running the power rule in the wrong direction."),
   (r"$-\frac{1 + \log_e x}{3 + x\log_e x} + C$", r"Integrates the denominator correctly but keeps the numerator $1 + \log_e x$ as a factor.")],
  r"Let $t = 3 + x\log_e x$; then $dt = (\log_e x + 1)\,dx$. The integral is $\int t^{-2}dt = -\frac{1}{t} = -\frac{1}{3 + x\log_e x} + C$.",
  r"Failing to see $1 + \log_e x$ as the derivative of $x\log_e x$.",
  "U08-A-subst-chain", "Spot the derivative of $x\\log_e x$; one substitution.",
  cognitive="Application", source_class="XII",
  **AD((1 + log(x))/(3 + x*log(x))**2, o))

o = [log(x**2 + 3*x + 5), log(x**2 + 3*x + 5)/2, log(2*x + 3), (2*x + 3)*log(x**2 + 3*x + 5)]
q("U08-A-008", TOPIC_S, "Integral of f'(x)/f(x)", "Easy", "Single-step computation MCQ",
  r"$\int \frac{2x + 3}{x^2 + 3x + 5}\,dx$ " + CI + " equals",
  r"$\log_e(x^2 + 3x + 5) + C$",
  [(r"$\frac{1}{2}\log_e(x^2 + 3x + 5) + C$", r"Inserts a factor $\frac{1}{2}$ by habit from $\int \frac{x}{x^2 + a}dx$, though the numerator is already the full derivative."),
   (r"$\log_e|2x + 3| + C$", r"Takes the logarithm of the numerator in place of the denominator."),
   (r"$(2x + 3)\log_e(x^2 + 3x + 5) + C$", r"Treats the numerator as a constant and pulls it outside the integral.")],
  r"The numerator $2x + 3$ is the derivative of $x^2 + 3x + 5$, which is always positive (discriminant $9 - 20 < 0$). Hence the integral is $\log_e(x^2 + 3x + 5) + C$.",
  r"Not recognising the $\frac{f'(x)}{f(x)}$ form exactly.",
  "U08-A-fprime-over-f", "Direct recognition of the $f'/f$ pattern.",
  cognitive="Recall", source_class="XII",
  **AD((2*x + 3)/(x**2 + 3*x + 5), o))

o = [asin(exp(x)), asin(exp(2*x))/2, -sqrt(1 - exp(2*x)), acos(exp(x))]
q("U08-A-009", TOPIC_S, "Substitution leading to inverse sine", "Easy", "Single-step computation MCQ",
  r"For $x < 0$, $\int \frac{e^x}{\sqrt{1 - e^{2x}}}\,dx$ " + CI + " equals",
  r"$\sin^{-1}(e^x) + C$",
  [(r"$\frac{1}{2}\sin^{-1}(e^{2x}) + C$", r"Writes $e^x\,dx$ as $\frac{1}{2}d(e^{2x})$ and $1 - e^{2x}$ as $1 - (e^{2x})^2$, mixing two substitutions."),
   (r"$-\sqrt{1 - e^{2x}} + C$", r"Uses the pattern $\int \frac{t}{\sqrt{1 - t^2}}dt = -\sqrt{1 - t^2}$, as if the numerator were $e^{2x}$."),
   (r"$\cos^{-1}(e^x) + C$", r"Uses $\int \frac{dt}{\sqrt{1 - t^2}} = \cos^{-1}t$, a sign error.")],
  r"Put $t = e^x$, $dt = e^x dx$; for $x < 0$, $0 < t < 1$. The integral is $\int \frac{dt}{\sqrt{1 - t^2}} = \sin^{-1}t = \sin^{-1}(e^x) + C$.",
  r"Choosing the wrong substitution variable inside the root.",
  "U08-A-subst-to-arcsin", "Single substitution to a standard form.",
  cognitive="Application", source_class="XII",
  **AD(exp(x)/sqrt(1 - exp(2*x)), o, pts=[Rational(-1, 2), -1, Rational(-3, 2)]))

o = [sin(x)**4/4, -cos(x)**4/4, sin(x)**4/3, -sin(x)**4/4]
q("U08-A-010", TOPIC_S, "Odd power with a matching derivative", "Easy", "Single-step computation MCQ",
  r"$\int \sin^3 x\cos x\,dx$ " + CI + " equals",
  r"$\frac{\sin^4 x}{4} + C$",
  [(r"$-\frac{\cos^4 x}{4} + C$", r"Substitutes $t = \cos x$ as if the integrand were $\cos^3 x\sin x$, swapping the roles of sine and cosine."),
   (r"$\frac{\sin^4 x}{3} + C$", r"Raises the power to $4$ but divides by the old exponent $3$."),
   (r"$-\frac{\sin^4 x}{4} + C$", r"Takes $\frac{d}{dx}\sin x = -\cos x$, a sign slip.")],
  r"Put $t = \sin x$, $dt = \cos x\,dx$. Then $\int t^3 dt = \frac{t^4}{4} = \frac{\sin^4 x}{4} + C$.",
  r"Choosing the wrong function for $t$.",
  "U08-A-sin-cos-odd-direct", "Single substitution.",
  cognitive="Recall", source_class="XII",
  **AD(sin(x)**3*cos(x), o))

o = [tan(x/2), 2*tan(x/2), tan(x/2)/2, -cot(x/2)]
q("U08-A-011", TOPIC_T, "Half-angle in the denominator", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{1 + \cos x}$ " + CI + " equals",
  r"$\tan\frac{x}{2} + C$",
  [(r"$2\tan\frac{x}{2} + C$", r"Writes $1 + \cos x = 2\cos^2\frac{x}{2}$ but drops the $\frac{1}{2}$ outside, integrating $\sec^2\frac{x}{2}$ correctly as $2\tan\frac{x}{2}$."),
   (r"$\frac{1}{2}\tan\frac{x}{2} + C$", r"Keeps the $\frac{1}{2}$ but integrates $\sec^2\frac{x}{2}$ as $\tan\frac{x}{2}$, missing the factor $2$ from the inner $\frac{x}{2}$."),
   (r"$-\cot\frac{x}{2} + C$", r"Uses the result for $\int \frac{dx}{1 - \cos x}$, confusing $2\cos^2\frac{x}{2}$ with $2\sin^2\frac{x}{2}$.")],
  r"$1 + \cos x = 2\cos^2\frac{x}{2}$, so the integral is $\frac{1}{2}\int \sec^2\frac{x}{2}\,dx = \frac{1}{2}\cdot 2\tan\frac{x}{2} = \tan\frac{x}{2} + C$.",
  r"Losing a factor of $2$ from the half angle.",
  "U08-A-half-angle-denominator", "One identity and one standard integral with a linear inner function.",
  cognitive="Application", source_class="XII",
  **AD(1/(1 + cos(x)), o))

o = [x**4/4, x**3/3, 3*x**2/2, x**4/12]
q("U08-A-012", TOPIC_F, "Simplify before integrating", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int e^{3\log_e x}\,dx$ " + CI + " equals",
  r"$\frac{x^4}{4} + C$",
  [(r"$\frac{x^3}{3} + C$", r"Treats $e^{3\log_e x}$ like $e^{3x}$ and writes $\frac{e^{3\log_e x}}{3} = \frac{x^3}{3}$."),
   (r"$\frac{3x^2}{2} + C$", r"Simplifies $e^{3\log_e x}$ as $3x$ and integrates."),
   (r"$\frac{x^4}{12} + C$", r"Simplifies to $x^3$ correctly but also divides by the $3$ from the exponent, as if applying a chain-rule factor.")],
  r"$e^{3\log_e x} = e^{\log_e x^3} = x^3$ for $x > 0$, so $\int x^3 dx = \frac{x^4}{4} + C$.",
  r"Not simplifying $e^{k\log_e x}$ to $x^k$ first.",
  "U08-A-log-exp-simplify", "One simplification, then the power rule.",
  cognitive="Understanding", source_class="XII",
  **AD(exp(3*log(x)), o))

o = [tan(x) - cot(x), tan(x) + cot(x), cot(x) - tan(x), -4*cot(2*x)]
q("U08-A-013", TOPIC_T, "Splitting with sin^2 x + cos^2 x = 1", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{\sin^2 x\cos^2 x}$ " + CI + " equals",
  r"$\tan x - \cot x + C$",
  [(r"$\tan x + \cot x + C$", r"Uses $\int \operatorname{cosec}^2 x\,dx = \cot x$, a sign error."),
   (r"$\cot x - \tan x + C$", r"Takes $\int \sec^2 x\,dx = -\tan x$ and $\int \operatorname{cosec}^2 x\,dx = \cot x$, reversing both signs."),
   (r"$-4\cot 2x + C$", r"Writes the integrand as $4\operatorname{cosec}^2 2x$ but forgets the factor $\frac{1}{2}$ from the inner $2x$.")],
  r"Write $1 = \sin^2 x + \cos^2 x$: $\frac{1}{\sin^2 x\cos^2 x} = \sec^2 x + \operatorname{cosec}^2 x$. Hence the integral is $\tan x - \cot x + C$.",
  r"Sign of $\int \operatorname{cosec}^2 x\,dx$.",
  "U08-A-pythag-split", "One identity, two standard integrals.",
  cognitive="Application", source_class="XII",
  **AD(1/(sin(x)**2*cos(x)**2), o))

o = [-sqrt(1 - x**2), sqrt(1 - x**2), -2*sqrt(1 - x**2), -sqrt(1 - x**2)/2]
q("U08-A-014", TOPIC_S, "Substitution under a square root", "Easy", "Single-step computation MCQ",
  r"For $-1 < x < 1$, $\int \frac{x}{\sqrt{1 - x^2}}\,dx$ " + CI + " equals",
  r"$-\sqrt{1 - x^2} + C$",
  [(r"$\sqrt{1 - x^2} + C$", r"Takes $dt = 2x\,dx$ for $t = 1 - x^2$, losing the minus sign."),
   (r"$-2\sqrt{1 - x^2} + C$", r"Uses $x\,dx = -dt$ in place of $-\frac{dt}{2}$."),
   (r"$-\frac{1}{2}\sqrt{1 - x^2} + C$", r"Writes $\int t^{-1/2}dt = t^{1/2}$, forgetting to divide by $\frac{1}{2}$, and keeps the $-\frac{1}{2}$.")],
  r"Let $t = 1 - x^2$, $dt = -2x\,dx$. Then the integral is $-\frac{1}{2}\int t^{-1/2}dt = -\frac{1}{2}\cdot 2t^{1/2} = -\sqrt{1 - x^2} + C$.",
  r"Mishandling the factor and sign in $dt = -2x\,dx$.",
  "U08-A-subst-chain", "One substitution with sign care.",
  cognitive="Application", source_class="XII",
  **AD(x/sqrt(1 - x**2), o, pts=[Rational(1, 2), Rational(1, 3), Rational(-2, 5)]))

o = [sin(4*x)/8 + sin(2*x)/4, sin(4*x)/4 + sin(2*x)/2, sin(4*x)/8 - sin(2*x)/4, sin(3*x)*sin(x)/3]
q("U08-A-015", TOPIC_T, "Product to sum", "Easy", "Single-step computation MCQ",
  r"$\int \cos 3x\cos x\,dx$ " + CI + " equals",
  r"$\frac{\sin 4x}{8} + \frac{\sin 2x}{4} + C$",
  [(r"$\frac{\sin 4x}{4} + \frac{\sin 2x}{2} + C$", r"Uses $\cos A\cos B = \cos(A+B) + \cos(A-B)$, missing the factor $\frac{1}{2}$."),
   (r"$\frac{\sin 4x}{8} - \frac{\sin 2x}{4} + C$", r"Writes $2\cos A\cos B = \cos(A+B) - \cos(A-B)$, a sign error in the identity."),
   (r"$\frac{\sin 3x\sin x}{3} + C$", r"Integrates each factor separately ($\frac{\sin 3x}{3}$ and $\sin x$) and multiplies the results.")],
  r"$2\cos 3x\cos x = \cos 4x + \cos 2x$, so the integral is $\frac{1}{2}\left(\frac{\sin 4x}{4} + \frac{\sin 2x}{2}\right) = \frac{\sin 4x}{8} + \frac{\sin 2x}{4} + C$.",
  r"Integrating a product as a product of integrals.",
  "U08-A-product-to-sum", "One product-to-sum identity and two direct integrals.",
  cognitive="Application", source_class="XII",
  **AD(cos(3*x)*cos(x), o))

def _c16():
    v = fit(cos(x)/sin(x)**3, -m_/sin(x)**2, [m_], [pi/6], extra=[pi/5, pi/3])
    return 1/v[m_]
q("U08-A-016", TOPIC_S, "Power of sine in the denominator", "Easy", "Inverse/parameter MCQ",
  r"If $\int \frac{\cos x}{\sin^3 x}\,dx = -\frac{1}{k\sin^2 x} + C$ " + CI + r", then $k$ equals",
  r"$2$",
  [(r"$-2$", r"Integrates $t^{-3}$ as $\frac{t^{-2}}{2}$, losing the sign, so the result is $+\frac{1}{2\sin^2 x}$."),
   (r"$3$", r"Lowers the power correctly to $t^{-2}$ but divides by the old exponent, giving $-\frac{1}{3\sin^2 x}$."),
   (r"$1$", r"Lowers the power to $t^{-2}$ and attaches the minus sign but never divides by the exponent.")],
  r"Put $t = \sin x$, $dt = \cos x\,dx$: $\int t^{-3}dt = \frac{t^{-2}}{-2} = -\frac{1}{2\sin^2 x} + C$. Hence $k = 2$.",
  r"Power rule with a negative exponent.",
  "U08-A-sin-cos-odd-direct", "Single substitution and a negative power.",
  check=_c16, values=[2, -2, 3, 1], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $\int \frac{\cos x}{\sin^3 x}\,dx = -\frac{1}{k\sin^2 x} + C$, where $C$ is the constant of integration, then $k$ is", answer=2))

def _c17():
    s1 = simplify(diff(2**x*log(2), x) - 2**x) == 0
    s2 = simplify(diff(log(sin(x)), x) - cot(x)) == 0
    return (s1, s2)
q("U08-A-017", TOPIC_F, "Standard formulae", "Easy", "Statement-based MCQ",
  r"Statement I: $\int 2^x\,dx = 2^x\log_e 2 + C$. Statement II: $\int \cot x\,dx = \log_e|\sin x| + C$. (Here $C$ is the constant of integration.)" + STEM_TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement I, confusing $\frac{d}{dx}2^x = 2^x\log_e 2$ with the integral."),
   (ST_FF, r"Rejects Statement II, recalling $\int \cot x\,dx$ as $\log_e|\cos x|$ or $-\log_e|\sin x|$."),
   (ST_TF, r"Swaps the two judgements: trusts the derivative formula in I and doubts the correct log form in II.")],
  r"Since $\frac{d}{dx}\left(\frac{2^x}{\log_e 2}\right) = 2^x$, the correct result is $\int 2^x dx = \frac{2^x}{\log_e 2} + C$, so Statement I is false. As $\frac{d}{dx}\log_e|\sin x| = \frac{\cos x}{\sin x} = \cot x$, Statement II is true.",
  r"Mixing up the derivative and the integral of $a^x$.",
  "U08-A-stmt-standard-formulas", "Two standard formulae checked by differentiation.",
  check=_c17, values=[(False, True), (True, True), (False, False), (True, False)],
  cognitive="Recall", source_class="XII")

# ================================================================ MEDIUM (26)

o = [sin(x) + cos(x), -sin(x) - cos(x), sin(x) - cos(x), Rational(2, 3)*(1 - sin(2*x))**Rational(3, 2)]
q("U08-A-018", TOPIC_T, "Square root of 1 - sin 2x", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < \frac{\pi}{4}$, $\int \sqrt{1 - \sin 2x}\,dx$ " + CI + " equals",
  r"$\sin x + \cos x + C$",
  [(r"$-\sin x - \cos x + C$", r"Writes $\sqrt{(\sin x - \cos x)^2} = \sin x - \cos x$, but on $\left(0, \frac{\pi}{4}\right)$ we have $\cos x > \sin x$, so this square root is negative."),
   (r"$\sin x - \cos x + C$", r"Uses $1 - \sin 2x = (\sin x + \cos x)^2$, the identity for $1 + \sin 2x$."),
   (r"$\frac{2}{3}(1 - \sin 2x)^{3/2} + C$", r"Applies the power rule to $(1 - \sin 2x)^{1/2}$ directly, ignoring the derivative of the inner function.")],
  r"$1 - \sin 2x = (\cos x - \sin x)^2$. On $\left(0, \frac{\pi}{4}\right)$, $\cos x > \sin x$, so $\sqrt{1 - \sin 2x} = \cos x - \sin x$. Integrating, $\sin x + \cos x + C$.",
  r"Taking $\sqrt{u^2} = u$ without checking the sign of $u$ on the interval.",
  "U08-A-root-identity", "Identity plus a sign decision on the given interval.",
  cognitive="Analysis", source_class="XII",
  **AD(sqrt(1 - sin(2*x)), o, pts=[pi/8, pi/10, pi/6]))

o = [Rational(2, 3)*((x + 1)**Rational(3, 2) - x**Rational(3, 2)),
     Rational(2, 3)*((x + 1)**Rational(3, 2) + x**Rational(3, 2)),
     Rational(2, 3)*(x**Rational(3, 2) - (x + 1)**Rational(3, 2)),
     Rational(3, 2)*((x + 1)**Rational(3, 2) - x**Rational(3, 2))]
q("U08-A-019", TOPIC_S, "Rationalising the denominator", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int \frac{dx}{\sqrt{x + 1} + \sqrt{x}}$ " + CI + " equals",
  r"$\frac{2}{3}\left[(x + 1)^{3/2} - x^{3/2}\right] + C$",
  [(r"$\frac{2}{3}\left[(x + 1)^{3/2} + x^{3/2}\right] + C$", r"Multiplies by the conjugate but writes the new numerator as $\sqrt{x + 1} + \sqrt{x}$."),
   (r"$\frac{2}{3}\left[x^{3/2} - (x + 1)^{3/2}\right] + C$", r"Multiplies by $\frac{\sqrt{x} - \sqrt{x + 1}}{\sqrt{x} - \sqrt{x + 1}}$ and ignores that the new denominator is $-1$."),
   (r"$\frac{3}{2}\left[(x + 1)^{3/2} - x^{3/2}\right] + C$", r"Multiplies by the new exponent $\frac{3}{2}$ in place of dividing by it.")],
  r"Multiplying by $\sqrt{x + 1} - \sqrt{x}$ gives a denominator $(x + 1) - x = 1$, so the integrand is $\sqrt{x + 1} - \sqrt{x}$. Integrating, $\frac{2}{3}(x + 1)^{3/2} - \frac{2}{3}x^{3/2} + C$.",
  r"Sign errors when rationalising.",
  "U08-A-rationalize", "Rationalise, then two power-rule integrals.",
  cognitive="Application", source_class="XII",
  **AD(1/(sqrt(x + 1) + sqrt(x)), o))

o = [sin(x)**3/3 - sin(x)**5/5, sin(x)**3/3 + sin(x)**5/5, sin(x)**3*cos(x)**4/12, cos(x)**3/3 - cos(x)**5/5]
q("U08-A-020", TOPIC_T, "sin^m x cos^n x with an odd power", "Medium", "Multi-step computation MCQ",
  r"$\int \sin^2 x\cos^3 x\,dx$ " + CI + " equals",
  r"$\frac{\sin^3 x}{3} - \frac{\sin^5 x}{5} + C$",
  [(r"$\frac{\sin^3 x}{3} + \frac{\sin^5 x}{5} + C$", r"Writes $\cos^2 x = 1 + \sin^2 x$, a sign slip in the Pythagorean identity."),
   (r"$\frac{\sin^3 x\cos^4 x}{12} + C$", r"Integrates $\sin^2 x$ and $\cos^3 x$ separately by the power rule and multiplies."),
   (r"$\frac{\cos^3 x}{3} - \frac{\cos^5 x}{5} + C$", r"Uses the same pattern with $t = \cos x$, swapping the roles of sine and cosine.")],
  r"Keep one $\cos x$ for $dt$: with $t = \sin x$, $\sin^2 x\cos^3 x\,dx = t^2(1 - t^2)\,dt$. Integrating, $\frac{t^3}{3} - \frac{t^5}{5} = \frac{\sin^3 x}{3} - \frac{\sin^5 x}{5} + C$.",
  r"Not reserving one factor of the odd power for the differential.",
  "U08-A-odd-power-expand", "Identity, substitution and expansion.",
  cognitive="Application", source_class="XII",
  **AD(sin(x)**2*cos(x)**3, o))

def _c21():
    v = fit(cos(x)**5, sin(x) + p_*sin(x)**3 + q_*sin(x)**5, [p_, q_], [pi/6, pi/4])
    return 15*(v[q_] - v[p_])
q("U08-A-021", TOPIC_T, "Odd power of cosine", "Medium", "Inverse/parameter MCQ",
  r"If $\int \cos^5 x\,dx = \sin x + p\sin^3 x + q\sin^5 x + C$ " + CI + r", then $15(q - p)$ equals",
  r"$13$",
  [(r"$8$", r"Expands $(1 - t^2)^2$ as $1 - t^2 + t^4$, getting $p = -\frac{1}{3}$, $q = \frac{1}{5}$."),
   (r"$-7$", r"Uses $\cos^2 x = 1 + \sin^2 x$, getting $p = \frac{2}{3}$, $q = \frac{1}{5}$."),
   (r"$45$", r"Expands correctly but does not divide by the new exponents, getting $p = -2$, $q = 1$.")],
  r"With $t = \sin x$, $\cos^5 x\,dx = (1 - t^2)^2 dt = (1 - 2t^2 + t^4)dt$, so the integral is $t - \frac{2}{3}t^3 + \frac{1}{5}t^5$. Thus $p = -\frac{2}{3}$, $q = \frac{1}{5}$ and $15(q - p) = 3 + 10 = 13$.",
  r"Expanding $(1 - t^2)^2$ without the middle term.",
  "U08-A-odd-power-expand", "Substitution, binomial expansion and coefficient matching.",
  check=_c21, values=[13, 8, -7, 45], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $\int \cos^5 x\,dx = \sin x + p\sin^3 x + q\sin^5 x + C$, where $C$ is the constant of integration, then $15(q - p)$ is", answer=13))

def _c22():
    v = fit(sin(x)**4, p_*x + q_*sin(2*x) + r_*sin(4*x), [p_, q_, r_], [pi/6, pi/4, pi/3])
    return 32*(v[p_] + v[q_] + v[r_])
q("U08-A-022", TOPIC_T, "Even power of sine", "Medium", "Inverse/parameter MCQ",
  r"If $\int \sin^4 x\,dx = px + q\sin 2x + r\sin 4x + C$ " + CI + r", then $32(p + q + r)$ equals",
  r"$5$",
  [(r"$3$", r"Uses $\cos^2 2x = \frac{1 - \cos 4x}{2}$, getting $r = -\frac{1}{32}$ with $p = \frac{3}{8}$, $q = -\frac{1}{4}$."),
   (r"$8$", r"Integrates $\cos 4x$ as $\sin 4x$ without dividing by $4$, getting $r = \frac{1}{8}$."),
   (r"$21$", r"Starts from $\sin^2 x = \frac{1 + \cos 2x}{2}$, getting $q = +\frac{1}{4}$ with $p = \frac{3}{8}$, $r = \frac{1}{32}$.")],
  r"$\sin^4 x = \frac{(1 - \cos 2x)^2}{4} = \frac{1}{4} - \frac{\cos 2x}{2} + \frac{1 + \cos 4x}{8} = \frac{3}{8} - \frac{\cos 2x}{2} + \frac{\cos 4x}{8}$. Integrating, $p = \frac{3}{8}$, $q = -\frac{1}{4}$, $r = \frac{1}{32}$, so $32(p + q + r) = 12 - 8 + 1 = 5$.",
  r"Using the wrong double-angle identity at one of the two reduction steps.",
  "U08-A-even-power-reduce", "Two successive power reductions and three coefficients.",
  check=_c22, values=[5, 3, 8, 21], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $\int \sin^4 x\,dx = px + q\sin 2x + r\sin 4x + C$, where $C$ is the constant of integration, then $32(p + q + r)$ is", answer=5))

o = [tan(x) + tan(x)**3/3, sec(x)**5/5, tan(x) - tan(x)**3/3, tan(x)**3/3]
q("U08-A-023", TOPIC_T, "Even power of secant", "Medium", "Multi-step computation MCQ",
  r"$\int \sec^4 x\,dx$ " + CI + " equals",
  r"$\tan x + \frac{\tan^3 x}{3} + C$",
  [(r"$\frac{\sec^5 x}{5} + C$", r"Applies the power rule to $\sec x$ as if it were $x$."),
   (r"$\tan x - \frac{\tan^3 x}{3} + C$", r"Writes $\sec^2 x = 1 - \tan^2 x$, reversing the identity."),
   (r"$\frac{\tan^3 x}{3} + C$", r"Replaces $\sec^4 x$ by $\tan^2 x\sec^2 x$, dropping the $1$ in $\sec^2 x = 1 + \tan^2 x$.")],
  r"$\sec^4 x = (1 + \tan^2 x)\sec^2 x$. With $t = \tan x$, $dt = \sec^2 x\,dx$, the integral is $\int (1 + t^2)dt = \tan x + \frac{\tan^3 x}{3} + C$.",
  r"Misusing $1 + \tan^2 x = \sec^2 x$.",
  "U08-A-tan-sec-powers", "Identity, substitution, two power-rule terms.",
  cognitive="Application", source_class="XII",
  **AD(sec(x)**4, o))

o = [tan(x)**2/2 + log(cos(x)), tan(x)**2/2 - log(cos(x)), tan(x)**4/4, tan(x)**2/2 + log(sin(x))]
q("U08-A-024", TOPIC_T, "Odd power of tangent", "Medium", "Multi-step computation MCQ",
  r"$\int \tan^3 x\,dx$ " + CI + " equals",
  r"$\frac{\tan^2 x}{2} + \log_e|\cos x| + C$",
  [(r"$\frac{\tan^2 x}{2} - \log_e|\cos x| + C$", r"Splits correctly but uses $\int \tan x\,dx = \log_e|\cos x|$, a sign error."),
   (r"$\frac{\tan^4 x}{4} + C$", r"Applies the power rule to $\tan x$ directly."),
   (r"$\frac{\tan^2 x}{2} + \log_e|\sin x| + C$", r"Recalls $\int \tan x\,dx$ as $-\log_e|\sin x|$, mixing it with $\int \cot x\,dx$.")],
  r"$\tan^3 x = \tan x(\sec^2 x - 1) = \tan x\sec^2 x - \tan x$. So the integral is $\frac{\tan^2 x}{2} - \log_e|\sec x| = \frac{\tan^2 x}{2} + \log_e|\cos x| + C$.",
  r"Sign of $\int \tan x\,dx$.",
  "U08-A-tan-sec-powers", "Split by identity, then substitution plus a standard integral.",
  cognitive="Application", source_class="XII",
  **AD(tan(x)**3, o))

o = [log(tan(x)) + tan(x)**2/2, log(tan(x)) - tan(x)**2/2, log(tan(x)) + tan(x)**2, log(sin(x)) + tan(x)**2/2]
q("U08-A-025", TOPIC_T, "Dividing by a power of cos x", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{dx}{\sin x\cos^3 x}$ " + CI + " equals",
  r"$\log_e|\tan x| + \frac{\tan^2 x}{2} + C$",
  [(r"$\log_e|\tan x| - \frac{\tan^2 x}{2} + C$", r"Writes $\sec^2 x = 1 - \tan^2 x$ after dividing by $\cos^4 x$."),
   (r"$\log_e|\tan x| + \tan^2 x + C$", r"Integrates $t$ as $t^2$, forgetting to divide by $2$."),
   (r"$\log_e|\sin x| + \frac{\tan^2 x}{2} + C$", r"Splits $1 = \sin^2 x + \cos^2 x$ but simplifies $\frac{\cos^2 x}{\sin x\cos^3 x}$ to $\cot x$ in place of $\frac{1}{\sin x\cos x}$.")],
  r"Divide numerator and denominator by $\cos^4 x$: the integrand becomes $\frac{\sec^4 x}{\tan x} = \frac{(1 + \tan^2 x)\sec^2 x}{\tan x}$. With $t = \tan x$ this is $\int \left(\frac{1}{t} + t\right)dt = \log_e|\tan x| + \frac{\tan^2 x}{2} + C$.",
  r"Not converting to a function of $\tan x$ with a $\sec^2 x$ factor.",
  "U08-A-divide-by-cos-power", "Rewrite in $\\tan x$, substitute, split into two terms.",
  cognitive="Application", source_class="XII",
  **AD(1/(sin(x)*cos(x)**3), o))

o = [4*tan(x)**Rational(1, 4), Rational(4, 7)*tan(x)**Rational(7, 4), tan(x)**Rational(1, 4)/4, Rational(4, 3)*tan(x)**Rational(3, 4)]
q("U08-A-026", TOPIC_T, "Fractional powers of sin x and cos x", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < \frac{\pi}{2}$, $\int \frac{dx}{\sqrt[4]{\sin^3 x\cos^5 x}}$ " + CI + " equals",
  r"$4\tan^{1/4}x + C$",
  [(r"$\frac{4}{7}\tan^{7/4}x + C$", r"Writes the integrand as $\sec^2 x\tan^{3/4}x$, using $+\frac{3}{4}$ for the exponent of $\tan x$."),
   (r"$\frac{1}{4}\tan^{1/4}x + C$", r"Multiplies by the new exponent $\frac{1}{4}$ in place of dividing by it."),
   (r"$\frac{4}{3}\tan^{3/4}x + C$", r"Writes $\sin^{3/4}x\cos^{5/4}x = \cos^2 x\tan^{1/4}x$, miscounting the powers, and integrates $t^{-1/4}$.")],
  r"$\sin^{3/4}x\cos^{5/4}x = \cos^2 x\left(\frac{\sin x}{\cos x}\right)^{3/4}$, so the integrand is $\sec^2 x\,(\tan x)^{-3/4}$. With $t = \tan x$, $\int t^{-3/4}dt = 4t^{1/4} = 4\tan^{1/4}x + C$.",
  r"Mishandling negative fractional exponents.",
  "U08-A-divide-by-cos-power", "Total degree $-2$ trick, then a fractional power.",
  cognitive="Application", source_class="XII",
  **AD(1/(sin(x)**3*cos(x)**5)**Rational(1, 4), o, pts=[pi/6, pi/4, pi/5]))

def _c27():
    f = x**3/(1 + x**8)
    for m in range(1, 13):
        try:
            v = fit(f, k_*atan(x**m), [k_], [Rational(1, 2)], extra=[Rational(3, 2), Rational(2, 3)])
        except AssertionError:
            continue
        return Integer(m) + 1/v[k_]
q("U08-A-027", TOPIC_S, "Substitution leading to inverse tangent", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{x^3}{1 + x^8}\,dx = \frac{1}{k}\tan^{-1}(x^m) + C$ " + CI + r", where $k$ and $m$ are positive integers, then $k + m$ equals",
  r"$8$",
  [(r"$5$", r"Substitutes $t = x^4$ but takes $x^3 dx = dt$, so $k = 1$, $m = 4$."),
   (r"$7$", r"Divides by $3$, the exponent of $x$ in the numerator, in place of $4$ from $dt = 4x^3 dx$, so $k = 3$, $m = 4$."),
   (r"$6$", r"Inserts $\frac{1}{2}$ by habit from $\int \frac{x}{1 + x^4}dx = \frac{1}{2}\tan^{-1}x^2$, so $k = 2$, $m = 4$.")],
  r"Put $t = x^4$, $dt = 4x^3 dx$. Then the integral is $\frac{1}{4}\int \frac{dt}{1 + t^2} = \frac{1}{4}\tan^{-1}(x^4) + C$, so $k = 4$, $m = 4$ and $k + m = 8$.",
  r"Wrong constant from the substitution $t = x^4$.",
  "U08-A-subst-to-arctan", "Spot $x^8 = (x^4)^2$ and the matching numerator.",
  check=_c27, values=[8, 5, 7, 6], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $\int \frac{x^3}{1 + x^8}\,dx = \frac{1}{k}\tan^{-1}(x^m) + C$, where $C$ is the constant of integration and $k$, $m$ are positive integers, then $k + m$ is", answer=8))

o = [tan(x) - sec(x), tan(x) + sec(x), sec(x) - tan(x), log(1 + sin(x))]
q("U08-A-028", TOPIC_T, "Multiplying by the conjugate", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{dx}{1 + \sin x}$ " + CI + " equals",
  r"$\tan x - \sec x + C$",
  [(r"$\tan x + \sec x + C$", r"Gets $\sec^2 x - \sec x\tan x$ but integrates $\sec x\tan x$ as $-\sec x$."),
   (r"$\sec x - \tan x + C$", r"Reverses both signs, giving the negative of the correct antiderivative."),
   (r"$\log_e(1 + \sin x) + C$", r"Treats the integrand as $\frac{f'(x)}{f(x)}$ though the numerator is $1$, not $\cos x$.")],
  r"Multiply by $1 - \sin x$: $\frac{1 - \sin x}{\cos^2 x} = \sec^2 x - \sec x\tan x$. Integrating, $\tan x - \sec x + C$.",
  r"Sign of $\int \sec x\tan x\,dx$.",
  "U08-A-conjugate-multiply", "Conjugate trick, then two standard integrals.",
  cognitive="Application", source_class="XII",
  **AD(1/(1 + sin(x)), o))

o = [log(cos(x) + sin(x)), log(cos(x) - sin(x)), -1/(cos(x) + sin(x)), log(1 + sin(2*x))]
q("U08-A-029", TOPIC_T, "Identity then f'(x)/f(x)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{\cos 2x}{(\cos x + \sin x)^2}\,dx$ " + CI + " equals",
  r"$\log_e|\cos x + \sin x| + C$",
  [(r"$\log_e|\cos x - \sin x| + C$", r"Reduces correctly to $\frac{\cos x - \sin x}{\cos x + \sin x}$ but takes the logarithm of the numerator in place of the denominator."),
   (r"$-\frac{1}{\cos x + \sin x} + C$", r"Treats the numerator as the derivative of $\cos x + \sin x$ and integrates $t^{-2}$."),
   (r"$\log_e|1 + \sin 2x| + C$", r"Writes $(\cos x + \sin x)^2 = 1 + \sin 2x$ and takes the logarithm without the factor $\frac{1}{2}$.")],
  r"$\cos 2x = (\cos x - \sin x)(\cos x + \sin x)$, so the integrand is $\frac{\cos x - \sin x}{\cos x + \sin x}$, whose numerator is the derivative of the denominator. Hence the integral is $\log_e|\cos x + \sin x| + C$.",
  r"Not factorising $\cos 2x$ as a difference of squares.",
  "U08-A-identity-then-fprime", "Factorise, cancel, recognise $f'/f$.",
  cognitive="Application", source_class="XII",
  **AD(cos(2*x)/(cos(x) + sin(x))**2, o))

def _c30():
    res = set()
    for av in (pi/5, pi/7):
        f = (cos(2*x) - cos(2*av))/(cos(x) - cos(av))
        v = fit(f, p_*sin(x) + q_*x*cos(av), [p_, q_], [pi/6, pi/3])
        res.add(v[p_] + v[q_])
    assert len(res) == 1
    return res.pop()
q("U08-A-030", TOPIC_T, "Cancelling after a double-angle identity", "Medium", "Inverse/parameter MCQ",
  r"Let $\alpha \in \left(0, \frac{\pi}{2}\right)$ be a constant. If $\int \frac{\cos 2x - \cos 2\alpha}{\cos x - \cos\alpha}\,dx = p\sin x + qx\cos\alpha + C$ " + CI + r", then $p + q$ equals",
  r"$4$",
  [(r"$2$", r"Simplifies $\frac{\cos^2 x - \cos^2\alpha}{\cos x - \cos\alpha}$ correctly but forgets the factor $2$ in $\cos 2x - \cos 2\alpha = 2(\cos^2 x - \cos^2\alpha)$."),
   (r"$-4$", r"Writes $\cos 2x - \cos 2\alpha = 2(\cos^2\alpha - \cos^2 x)$, a sign slip, so the integrand becomes $-2(\cos x + \cos\alpha)$."),
   (r"$0$", r"Factors $\cos^2 x - \cos^2\alpha$ as $(\cos x - \cos\alpha)^2$ wrongly, then reaches $2(\cos x - \cos\alpha)$ and $p = 2$, $q = -2$.")],
  r"$\cos 2x - \cos 2\alpha = 2\cos^2 x - 2\cos^2\alpha = 2(\cos x - \cos\alpha)(\cos x + \cos\alpha)$. So the integrand is $2\cos x + 2\cos\alpha$, whose integral is $2\sin x + 2x\cos\alpha + C$. Thus $p = q = 2$ and $p + q = 4$.",
  r"Losing the factor $2$ when converting $\cos 2\theta$ to $\cos^2\theta$.",
  "U08-A-identity-cancel", "Identity, factorisation and cancellation; $\\alpha$ is a constant.",
  check=_c30, values=[4, 2, -4, 0], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $\alpha \in \left(0, \frac{\pi}{2}\right)$ be a constant. If $\int \frac{\cos 2x - \cos 2\alpha}{\cos x - \cos\alpha}\,dx = p\sin x + qx\cos\alpha + C$, where $C$ is the constant of integration, then $p + q$ is", answer=4))

o = [sqrt(3)/2*x + log(sin(x - pi/6))/2, x/2 + sqrt(3)/2*log(sin(x - pi/6)),
     sqrt(3)/2*x - log(sin(x - pi/6))/2, sqrt(3)/2*x + log(cos(x - pi/6))/2]
q("U08-A-031", TOPIC_T, "Shifting the angle", "Medium", "Multi-step computation MCQ",
  r"For $\frac{\pi}{6} < x < \frac{7\pi}{6}$, $\int \frac{\sin x}{\sin\left(x - \frac{\pi}{6}\right)}\,dx$ " + CI + " equals",
  r"$\frac{\sqrt{3}}{2}x + \frac{1}{2}\log_e\left|\sin\left(x - \frac{\pi}{6}\right)\right| + C$",
  [(r"$\frac{1}{2}x + \frac{\sqrt{3}}{2}\log_e\left|\sin\left(x - \frac{\pi}{6}\right)\right| + C$", r"Swaps $\cos\frac{\pi}{6}$ and $\sin\frac{\pi}{6}$ in the expansion of $\sin\left(\left(x - \frac{\pi}{6}\right) + \frac{\pi}{6}\right)$."),
   (r"$\frac{\sqrt{3}}{2}x - \frac{1}{2}\log_e\left|\sin\left(x - \frac{\pi}{6}\right)\right| + C$", r"Expands $\sin(A + B)$ as $\sin A\cos B - \cos A\sin B$."),
   (r"$\frac{\sqrt{3}}{2}x + \frac{1}{2}\log_e\left|\cos\left(x - \frac{\pi}{6}\right)\right| + C$", r"Integrates $\cot\left(x - \frac{\pi}{6}\right)$ as $\log_e|\cos(\ldots)|$.")],
  r"Write $x = \left(x - \frac{\pi}{6}\right) + \frac{\pi}{6}$: $\sin x = \sin\left(x - \frac{\pi}{6}\right)\frac{\sqrt{3}}{2} + \cos\left(x - \frac{\pi}{6}\right)\frac{1}{2}$. Dividing, the integrand is $\frac{\sqrt{3}}{2} + \frac{1}{2}\cot\left(x - \frac{\pi}{6}\right)$, which integrates to $\frac{\sqrt{3}}{2}x + \frac{1}{2}\log_e\left|\sin\left(x - \frac{\pi}{6}\right)\right| + C$.",
  r"Expanding $\sin(A + B)$ with the wrong pairing of terms.",
  "U08-A-shift-angle", "Rewrite the angle, expand, split into a constant and a cotangent.",
  cognitive="Application", source_class="XII",
  **AD(sin(x)/sin(x - pi/6), o))

def _c32():
    v = fit(x**3/sqrt(1 + x**2), p_*(1 + x**2)**Rational(3, 2) + q_*sqrt(1 + x**2), [p_, q_], [1, 2])
    return 3*(v[p_] - v[q_])
q("U08-A-032", TOPIC_S, "Substituting and back-substituting", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{x^3}{\sqrt{1 + x^2}}\,dx = p(1 + x^2)^{3/2} + q\sqrt{1 + x^2} + C$ " + CI + r", then $3(p - q)$ equals",
  r"$4$",
  [(r"$-2$", r"Writes $x^2 = t + 1$ in place of $t - 1$, getting $p = \frac{1}{3}$, $q = 1$."),
   (r"$8$", r"Uses $x\,dx = dt$ for $t = 1 + x^2$, dropping the $\frac{1}{2}$, so $p = \frac{2}{3}$, $q = -2$."),
   (r"$3$", r"Multiplies by the new exponents in place of dividing, getting $p = \frac{3}{4}$, $q = -\frac{1}{4}$.")],
  r"Let $t = 1 + x^2$, $x\,dx = \frac{dt}{2}$, $x^2 = t - 1$. The integral is $\frac{1}{2}\int (t^{1/2} - t^{-1/2})dt = \frac{1}{3}t^{3/2} - t^{1/2}$. So $p = \frac{1}{3}$, $q = -1$ and $3(p - q) = 1 + 3 = 4$.",
  r"Not expressing the leftover $x^2$ in terms of $t$ correctly.",
  "U08-A-subst-back", "Substitution with back-substitution of $x^2$ and two power terms.",
  check=_c32, values=[4, -2, 8, 3], cognitive="Application", source_class="XII",
  numerical=dict(question=r"If $\int \frac{x^3}{\sqrt{1 + x^2}}\,dx = p(1 + x^2)^{3/2} + q\sqrt{1 + x^2} + C$, where $C$ is the constant of integration, then $3(p - q)$ is", answer=4))

o = [2*sqrt(x) - 2*atan(sqrt(x)), sqrt(x) - atan(sqrt(x)), 2*sqrt(x) + 2*atan(sqrt(x)), 2*log(1 + sqrt(x))]
q("U08-A-033", TOPIC_S, "Root substitution", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int \frac{\sqrt{x}}{1 + x}\,dx$ " + CI + " equals",
  r"$2\sqrt{x} - 2\tan^{-1}\sqrt{x} + C$",
  [(r"$\sqrt{x} - \tan^{-1}\sqrt{x} + C$", r"Substitutes $x = t^2$ but uses $dx = t\,dt$, losing the factor $2$."),
   (r"$2\sqrt{x} + 2\tan^{-1}\sqrt{x} + C$", r"Writes $\frac{t^2}{1 + t^2} = 1 + \frac{1}{1 + t^2}$, a sign slip in the division."),
   (r"$2\log_e(1 + \sqrt{x}) + C$", r"Treats the integrand as if $\frac{d}{dx}(1 + \sqrt{x})$ appeared in the numerator, a false $\frac{f'}{f}$ pattern.")],
  r"Let $x = t^2$, $dx = 2t\,dt$ ($t > 0$). The integral becomes $\int \frac{2t^2}{1 + t^2}dt = 2\int\left(1 - \frac{1}{1 + t^2}\right)dt = 2t - 2\tan^{-1}t = 2\sqrt{x} - 2\tan^{-1}\sqrt{x} + C$.",
  r"Dropping the Jacobian factor $2t$ in $dx = 2t\,dt$.",
  "U08-A-root-subst", "Substitution, polynomial division, standard integral.",
  cognitive="Application", source_class="XII",
  **AD(sqrt(x)/(1 + x), o))

def _c34():
    F = integrate(3*x**2/sqrt(x**3 + 1), x)
    c = Symbol('c')
    cv = solve(F.subs(x, 0) + c - 1, c)[0]
    return simplify(F.subs(x, 2) + cv)
q("U08-A-034", TOPIC_S, "Fixing the constant of integration", "Medium", "Multi-step computation MCQ",
  r"Let $f(x) = \int \frac{3x^2}{\sqrt{x^3 + 1}}\,dx$ for $x \geq 0$, with $f(0) = 1$. Then $f(2)$ equals",
  r"$5$",
  [(r"$3$", r"Integrates as $\sqrt{x^3 + 1} + c$, losing the factor $2$ from $\int t^{-1/2}dt$; then $c = 0$ and $f(2) = 3$."),
   (r"$6$", r"Finds $2\sqrt{x^3 + 1}$ correctly but ignores the condition $f(0) = 1$, taking the constant as $0$."),
   (r"$7$", r"Solves $2 + c = 1$ as $c = 1$, a sign slip, so $f(2) = 6 + 1$.")],
  r"With $t = x^3 + 1$, $dt = 3x^2 dx$: $f(x) = \int t^{-1/2}dt = 2\sqrt{x^3 + 1} + c$. From $f(0) = 2 + c = 1$, $c = -1$. Hence $f(2) = 2\cdot 3 - 1 = 5$.",
  r"Ignoring the initial condition when evaluating an antiderivative.",
  "U08-A-const-determination", "Substitution followed by use of an initial condition.",
  check=_c34, values=[5, 3, 6, 7], cognitive="Application", source_class="XII",
  numerical=dict(question=r"Let $f(x) = \int \frac{3x^2}{\sqrt{x^3 + 1}}\,dx$ for $x \geq 0$, with $f(0) = 1$. Then $f(2)$ is", answer=5))

def _c35():
    s1 = simplify(diff(sin(x)**2, x) - sin(2*x)) == 0 and simplify(diff(-cos(x)**2, x) - sin(2*x)) == 0
    s2 = simplify(diff(tan(x)**2/2, x) - sec(x)**2*tan(x)) == 0 and simplify(diff(sec(x)**2/2, x) - sec(x)**2*tan(x)) == 0
    return (bool(s1), bool(s2))
q("U08-A-035", TOPIC_F, "Antiderivatives differ by a constant", "Medium", "Statement-based MCQ",
  r"Statement I: Both $\sin^2 x$ and $-\cos^2 x$ are antiderivatives of $\sin 2x$ on $\mathbb{R}$. Statement II: $\int \sec^2 x\tan x\,dx$ can be written both as $\frac{1}{2}\tan^2 x + C$ and as $\frac{1}{2}\sec^2 x + C$ (where $C$ is the constant of integration)." + STEM_TAIL,
  ST_TT,
  [(ST_FF, r"Believes an integral has only one correct closed form, rejecting both pairs because the expressions look different."),
   (ST_TF, r"Accepts I by differentiating but rejects II, not noticing $\frac{1}{2}\sec^2 x - \frac{1}{2}\tan^2 x = \frac{1}{2}$ is a constant."),
   (ST_FT, r"Rejects I because $\sin^2 x \neq -\cos^2 x$, missing that they differ by the constant $1$.")],
  r"$\frac{d}{dx}\sin^2 x = 2\sin x\cos x = \sin 2x$ and $\frac{d}{dx}(-\cos^2 x) = 2\cos x\sin x = \sin 2x$, so Statement I is true (they differ by $1$). Also $\frac{d}{dx}\frac{\tan^2 x}{2} = \tan x\sec^2 x$ and $\frac{d}{dx}\frac{\sec^2 x}{2} = \sec^2 x\tan x$, and the two forms differ by $\frac{1}{2}$, so Statement II is true.",
  r"Thinking two different-looking antiderivatives cannot both be correct.",
  "U08-A-stmt-antiderivative-family", "Two verifications by differentiation plus the idea of an arbitrary constant.",
  check=_c35, values=[(True, True), (False, False), (True, False), (False, True)],
  cognitive="Understanding", source_class="XII")

_psi = lambda t: t**4 + t       # witness antiderivative psi
_f = lambda t: 4*t**3 + 1        # its derivative f
o = [_psi(x**3)/3, 3*_psi(x**3), _psi(x**3), x**3*_psi(x**3)/3]
q("U08-A-036", TOPIC_S, "Substitution with an unspecified function", "Medium", "Conceptual/application MCQ",
  r"If $\int f(x)\,dx = \psi(x) + C$ " + CI + r", then $\int x^2 f(x^3)\,dx$ equals",
  r"$\frac{1}{3}\psi(x^3) + C$",
  [(r"$3\psi(x^3) + C$", r"Uses $x^2 dx = 3\,dt$ for $t = x^3$, inverting the factor."),
   (r"$\psi(x^3) + C$", r"Substitutes $t = x^3$ but treats $x^2 dx$ as $dt$."),
   (r"$\frac{x^3}{3}\psi(x^3) + C$", r"Integrates $x^2$ separately to $\frac{x^3}{3}$ and multiplies by $\psi(x^3)$.")],
  r"Put $t = x^3$, $dt = 3x^2 dx$. Then $\int x^2 f(x^3)\,dx = \frac{1}{3}\int f(t)\,dt = \frac{1}{3}\psi(t) = \frac{1}{3}\psi(x^3) + C$.",
  r"Losing the constant in $dt = 3x^2 dx$ when the integrand is abstract.",
  "U08-A-composite-reverse", "Substitution in an abstract integrand; check uses a sample $\\psi$.",
  cognitive="Understanding", source_class="XII",
  **AD(x**2*_f(x**3), o))

o = [x - log(1 + exp(x)), x + log(1 + exp(x)), log(1 + exp(x)), log(1 + exp(-x))]
q("U08-A-037", TOPIC_S, "Rewriting an exponential integrand", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{dx}{1 + e^x}$ " + CI + " equals",
  r"$x - \log_e(1 + e^x) + C$",
  [(r"$x + \log_e(1 + e^x) + C$", r"Writes $\frac{1}{1 + e^x} = 1 + \frac{e^x}{1 + e^x}$, a sign slip in adding and subtracting $e^x$."),
   (r"$\log_e(1 + e^x) + C$", r"Treats the integrand as $\frac{f'}{f}$ though the numerator is $1$, not $e^x$."),
   (r"$\log_e(1 + e^{-x}) + C$", r"Divides through by $e^x$ to get $\frac{e^{-x}}{e^{-x} + 1}$ but drops the minus sign from $d(e^{-x}) = -e^{-x}dx$.")],
  r"$\frac{1}{1 + e^x} = \frac{(1 + e^x) - e^x}{1 + e^x} = 1 - \frac{e^x}{1 + e^x}$. Integrating, $x - \log_e(1 + e^x) + C$ (equivalently $-\log_e(1 + e^{-x}) + C$).",
  r"Applying the $\frac{f'}{f}$ rule without checking the numerator.",
  "U08-A-subst-exp-divide", "Algebraic rewrite before a log integral; a sign trap.",
  cognitive="Application", source_class="XII",
  **AD(1/(1 + exp(x)), o))

o = [tan(x*exp(x)), -cot(x*exp(x)), log(sec(x*exp(x))), sec(x*exp(x))]
q("U08-A-038", TOPIC_S, "Recognising a product rule derivative", "Medium", "Single-step computation MCQ",
  r"$\int \frac{e^x(1 + x)}{\cos^2(xe^x)}\,dx$ " + CI + " equals",
  r"$\tan(xe^x) + C$",
  [(r"$-\cot(xe^x) + C$", r"Uses $\int \operatorname{cosec}^2 t\,dt$ in place of $\int \sec^2 t\,dt$."),
   (r"$\log_e|\sec(xe^x)| + C$", r"Recalls $\int \sec^2 t\,dt$ as $\log_e|\sec t|$, mixing it with $\int \tan t\,dt$."),
   (r"$\sec(xe^x) + C$", r"Takes $\int \sec^2 t\,dt = \sec t$, as if the power rule applied.")],
  r"Since $\frac{d}{dx}(xe^x) = e^x(1 + x)$, put $t = xe^x$. The integral is $\int \sec^2 t\,dt = \tan t = \tan(xe^x) + C$.",
  r"Not spotting $e^x(1 + x)$ as the derivative of $xe^x$.",
  "U08-A-subst-composite", "Recognise a product-rule derivative, then a standard integral.",
  cognitive="Application", source_class="XII",
  **AD(exp(x)*(1 + x)/cos(x*exp(x))**2, o))

o = [-cos(2*x)/8 - cos(4*x)/16 + cos(6*x)/24, -cos(2*x)/4 - cos(4*x)/8 + cos(6*x)/12,
     cos(2*x)/8 + cos(4*x)/16 - cos(6*x)/24, -cos(2*x)/4 - cos(4*x)/4 + cos(6*x)/4]
q("U08-A-039", TOPIC_T, "Product of three sines", "Medium", "Multi-step computation MCQ",
  r"$\int \sin x\sin 2x\sin 3x\,dx$ " + CI + " equals",
  r"$-\frac{\cos 2x}{8} - \frac{\cos 4x}{16} + \frac{\cos 6x}{24} + C$",
  [(r"$-\frac{\cos 2x}{4} - \frac{\cos 4x}{8} + \frac{\cos 6x}{12} + C$", r"Drops one factor $\frac{1}{2}$ from the two product-to-sum steps, doubling every term."),
   (r"$\frac{\cos 2x}{8} + \frac{\cos 4x}{16} - \frac{\cos 6x}{24} + C$", r"Uses $2\sin A\sin B = \cos(A+B) - \cos(A-B)$, reversing the sign of the whole integrand."),
   (r"$-\frac{\cos 2x}{4} - \frac{\cos 4x}{4} + \frac{\cos 6x}{4} + C$", r"Reduces correctly to $\frac{\sin 2x + \sin 4x - \sin 6x}{4}$ but forgets to divide by $2$, $4$, $6$ when integrating.")],
  r"$2\sin x\sin 3x = \cos 2x - \cos 4x$, so the integrand is $\frac{1}{2}(\sin 2x\cos 2x - \sin 2x\cos 4x) = \frac{1}{4}\left(\sin 4x - \sin 6x + \sin 2x\right)$. Integrating, $\frac{1}{4}\left(-\frac{\cos 4x}{4} + \frac{\cos 6x}{6} - \frac{\cos 2x}{2}\right) = -\frac{\cos 2x}{8} - \frac{\cos 4x}{16} + \frac{\cos 6x}{24} + C$.",
  r"Losing the factor $\frac{1}{2}$ at a product-to-sum step.",
  "U08-A-product-to-sum", "Two product-to-sum conversions, three integrals.",
  cognitive="Application", source_class="XII",
  **AD(sin(x)*sin(2*x)*sin(3*x), o))

o = [log(tan(x/2 + pi/6))/2, log(tan(x/2 + pi/6)), log(tan(x/2 + pi/3))/2, log(tan(x/2 + pi/12))/2]
q("U08-A-040", TOPIC_T, "Auxiliary angle", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < \frac{\pi}{2}$, $\int \frac{dx}{\sin x + \sqrt{3}\cos x}$ " + CI + " equals",
  r"$\frac{1}{2}\log_e\left|\tan\left(\frac{x}{2} + \frac{\pi}{6}\right)\right| + C$",
  [(r"$\log_e\left|\tan\left(\frac{x}{2} + \frac{\pi}{6}\right)\right| + C$", r"Writes $\sin x + \sqrt{3}\cos x = \sin\left(x + \frac{\pi}{3}\right)$, missing the amplitude $2$."),
   (r"$\frac{1}{2}\log_e\left|\tan\left(\frac{x}{2} + \frac{\pi}{3}\right)\right| + C$", r"Halves $x$ in $\log_e\left|\tan\frac{\theta}{2}\right|$ but not the phase $\frac{\pi}{3}$."),
   (r"$\frac{1}{2}\log_e\left|\tan\left(\frac{x}{2} + \frac{\pi}{12}\right)\right| + C$", r"Uses the phase $\frac{\pi}{6}$, writing $\sin x + \sqrt{3}\cos x = 2\sin\left(x + \frac{\pi}{6}\right)$.")],
  r"$\sin x + \sqrt{3}\cos x = 2\sin\left(x + \frac{\pi}{3}\right)$. Since $\int \operatorname{cosec}\theta\,d\theta = \log_e\left|\tan\frac{\theta}{2}\right|$, the integral is $\frac{1}{2}\log_e\left|\tan\left(\frac{x}{2} + \frac{\pi}{6}\right)\right| + C$.",
  r"Wrong amplitude or phase in $a\sin x + b\cos x = R\sin(x + \phi)$.",
  "U08-A-aux-angle", "Auxiliary angle form plus the cosec integral.",
  cognitive="Application", source_class="XII",
  **AD(1/(sin(x) + sqrt(3)*cos(x)), o, pts=[Rational(1, 2), 1, Rational(3, 2)]))

def _c41():
    s1 = simplify(diff(-csc(x), x) - cos(x)/sin(x)**2) == 0
    s2 = simplify(diff(tan(x) - sec(x), x) - 1/(1 - sin(x))) == 0
    return (bool(s1), bool(s2))
q("U08-A-041", TOPIC_T, "Checking results by differentiation", "Medium", "Statement-based MCQ",
  r"Statement I: $\int \frac{\cos x}{\sin^2 x}\,dx = -\operatorname{cosec} x + C$. Statement II: $\int \frac{dx}{1 - \sin x} = \tan x - \sec x + C$. (Here $C$ is the constant of integration.)" + STEM_TAIL,
  ST_TF,
  [(ST_TT, r"Accepts II by copying the result for $\int \frac{dx}{1 + \sin x}$ without adjusting the sign."),
   (ST_FF, r"Rejects I, expecting $+\operatorname{cosec} x$ by integrating $t^{-2}$ as $+t^{-1}$ after putting $t = \sin x$, a sign slip in the power rule."),
   (ST_FT, r"Reverses both judgements: doubts the correct power-rule result and trusts the copied conjugate result.")],
  r"With $t = \sin x$, $dt = \cos x\,dx$, $\int \frac{\cos x}{\sin^2 x}\,dx = \int t^{-2}dt = -\frac{1}{t} = -\operatorname{cosec} x + C$; Statement I is true. Multiplying by $1 + \sin x$, $\frac{1}{1 - \sin x} = \sec^2 x + \sec x\tan x$, which integrates to $\tan x + \sec x + C$, not $\tan x - \sec x + C$; Statement II is false.",
  r"Reusing the conjugate result for $1 + \sin x$ with the wrong sign.",
  "U08-A-conjugate-multiply", "A substitution check and a conjugate computation with a sign trap.",
  check=_c41, values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Analysis", source_class="XII")

def _c42():
    s1 = simplify(diff(x/2 - sin(2*x)/4, x) - cos(x)**2) == 0
    s2 = simplify(diff(9**x/log(3), x) - 3**(2*x)) == 0
    return (bool(s1), bool(s2))
q("U08-A-042", TOPIC_F, "Two common slips", "Medium", "Statement-based MCQ",
  r"Statement I: $\int \cos^2 x\,dx = \frac{x}{2} - \frac{\sin 2x}{4} + C$. Statement II: $\int 3^{2x}\,dx = \frac{9^x}{\log_e 3} + C$. (Here $C$ is the constant of integration.)" + STEM_TAIL,
  ST_FF,
  [(ST_TT, r"Accepts I using the $\sin^2 x$ identity and accepts II treating $3^{2x}$ as having base $3$."),
   (ST_TF, r"Accepts I, mixing up $\cos^2 x = \frac{1 + \cos 2x}{2}$ with $\frac{1 - \cos 2x}{2}$."),
   (ST_FT, r"Rejects I correctly but accepts II, forgetting that $3^{2x} = 9^x$ needs $\log_e 9 = 2\log_e 3$.")],
  r"$\cos^2 x = \frac{1 + \cos 2x}{2}$ gives $\int \cos^2 x\,dx = \frac{x}{2} + \frac{\sin 2x}{4} + C$, so Statement I is false. Also $3^{2x} = 9^x$ and $\int 9^x dx = \frac{9^x}{\log_e 9} = \frac{9^x}{2\log_e 3} + C$, so Statement II is false.",
  r"Using the wrong base for the logarithm in $\int a^x dx$.",
  "U08-A-stmt-standard-formulas", "Two independent checks, each with a common trap.",
  check=_c42, values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Understanding", source_class="XII")

o = [-sqrt(1 - x**2)/x, sqrt(1 - x**2)/x, -x/sqrt(1 - x**2), x/sqrt(1 - x**2)]
q("U08-A-043", TOPIC_S, "Trigonometric substitution", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < 1$, $\int \frac{dx}{x^2\sqrt{1 - x^2}}$ " + CI + " equals",
  r"$-\frac{\sqrt{1 - x^2}}{x} + C$",
  [(r"$\frac{\sqrt{1 - x^2}}{x} + C$", r"Uses $\int \operatorname{cosec}^2\theta\,d\theta = \cot\theta$, a sign error."),
   (r"$-\frac{x}{\sqrt{1 - x^2}} + C$", r"Integrates to $-\cot\theta$ correctly but converts back using $\cot\theta = \frac{x}{\sqrt{1 - x^2}}$, inverting the ratio."),
   (r"$\frac{x}{\sqrt{1 - x^2}} + C$", r"Makes both slips: the sign of $\int \operatorname{cosec}^2\theta\,d\theta$ and the inverted ratio for $\cot\theta$.")],
  r"Put $x = \sin\theta$, $dx = \cos\theta\,d\theta$, $\theta \in \left(0, \frac{\pi}{2}\right)$. The integral becomes $\int \frac{\cos\theta\,d\theta}{\sin^2\theta\cos\theta} = \int \operatorname{cosec}^2\theta\,d\theta = -\cot\theta = -\frac{\sqrt{1 - x^2}}{x} + C$.",
  r"Back-substituting $\cot\theta$ incorrectly.",
  "U08-A-trig-subst", "Trigonometric substitution, standard integral, back-substitution.",
  cognitive="Application", source_class="XII",
  **AD(1/(x**2*sqrt(1 - x**2)), o, pts=[Rational(1, 2), Rational(1, 3), Rational(3, 5)]))

# ================================================================ DIFFICULT (13)

def _c44():
    f = (2*x**12 + 5*x**9)/(x**5 + x**3 + 1)**3
    pts = [Rational(1, 2), Rational(3, 2), 2]
    for m in range(0, 21):
        for n in [i for i in range(-12, 13) if i != 0]:
            F = x**m/(n*(x**5 + x**3 + 1)**2)
            d = diff(F, x) - f
            if all(d.subs(x, t) == 0 for t in pts) and simplify(d) == 0:
                return Integer(m + n)
q("U08-A-044", TOPIC_S, "Dividing by a power of x", "Difficult", "Inverse/parameter MCQ",
  r"If $\int \frac{2x^{12} + 5x^9}{(x^5 + x^3 + 1)^3}\,dx = \frac{x^m}{n(x^5 + x^3 + 1)^2} + C$ " + CI + r", where $m$ and $n$ are integers, then $m + n$ equals",
  r"$12$",
  [(r"$8$", r"Integrates $-t^{-3}$ as $-\frac{t^{-2}}{2}$, a sign slip, giving $n = -2$, $m = 10$."),
   (r"$7$", r"Writes $t^2 = \frac{(x^5 + x^3 + 1)^2}{x^5}$, not squaring the $x^5$, so $m = 5$, $n = 2$."),
   (r"$13$", r"Lowers the power to $t^{-2}$ but divides by the old exponent $3$, giving $n = 3$, $m = 10$.")],
  r"Divide numerator and denominator by $x^{15}$: the integrand is $\frac{2x^{-3} + 5x^{-6}}{(1 + x^{-2} + x^{-5})^3}$. With $t = 1 + x^{-2} + x^{-5}$, $dt = -(2x^{-3} + 5x^{-6})dx$, so the integral is $-\int t^{-3}dt = \frac{1}{2t^2} = \frac{x^{10}}{2(x^5 + x^3 + 1)^2} + C$. Hence $m = 10$, $n = 2$ and $m + n = 12$.",
  r"Not seeing that dividing by $x^{15}$ makes the numerator an exact derivative.",
  "U08-A-algebraic-power-subst", "Non-obvious division by $x^{15}$, substitution and reconversion.",
  check=_c44, values=[12, 8, 7, 13], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"If $\int \frac{2x^{12} + 5x^9}{(x^5 + x^3 + 1)^3}\,dx = \frac{x^m}{n(x^5 + x^3 + 1)^2} + C$, where $C$ is the constant of integration and $m$, $n$ are integers, then $m + n$ is", answer=12))

o = [-(1 + x**4)**Rational(1, 4)/x, (1 + x**4)**Rational(1, 4)/x,
     -(1 + x**4)**Rational(1, 4)/(16*x), -4*(1 + x**4)**Rational(1, 4)/x]
q("U08-A-045", TOPIC_S, "Taking out the highest power", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int \frac{dx}{x^2(x^4 + 1)^{3/4}}$ " + CI + " equals",
  r"$-\frac{(1 + x^4)^{1/4}}{x} + C$",
  [(r"$\frac{(1 + x^4)^{1/4}}{x} + C$", r"Takes $dt = 4x^{-5}dx$ for $t = 1 + x^{-4}$, losing the minus sign."),
   (r"$-\frac{(1 + x^4)^{1/4}}{16x} + C$", r"Multiplies by the new exponent $\frac{1}{4}$ in place of dividing, so $-\frac{1}{4}\int t^{-3/4}dt$ becomes $-\frac{1}{16}t^{1/4}$."),
   (r"$-\frac{4(1 + x^4)^{1/4}}{x} + C$", r"Keeps the sign but drops the $\frac{1}{4}$ in $x^{-5}dx = -\frac{dt}{4}$.")],
  r"$x^2(x^4 + 1)^{3/4} = x^2\cdot x^3(1 + x^{-4})^{3/4} = x^5(1 + x^{-4})^{3/4}$. With $t = 1 + x^{-4}$, $dt = -4x^{-5}dx$, the integral is $-\frac{1}{4}\int t^{-3/4}dt = -t^{1/4} = -\left(1 + \frac{1}{x^4}\right)^{1/4} = -\frac{(1 + x^4)^{1/4}}{x} + C$.",
  r"Not factoring out the highest power before substituting.",
  "U08-A-algebraic-power-subst", "Factor out $x^3$ from the bracket, substitute in $x^{-4}$, reconvert.",
  cognitive="Analysis", source_class="XII",
  **AD(1/(x**2*(x**4 + 1)**Rational(3, 4)), o))

o = [atan(tan(x)**2), atan(tan(x)**2)/2, 2*atan(tan(x)**2), atan(cos(2*x))]
q("U08-A-046", TOPIC_T, "Fourth powers in the denominator", "Difficult", "Multi-step computation MCQ",
  r"For $0 < x < \frac{\pi}{2}$, $\int \frac{\sin 2x}{\sin^4 x + \cos^4 x}\,dx$ " + CI + " equals",
  r"$\tan^{-1}(\tan^2 x) + C$",
  [(r"$\frac{1}{2}\tan^{-1}(\tan^2 x) + C$", r"Writes $\sin 2x = \sin x\cos x$, losing the factor $2$, before dividing by $\cos^4 x$."),
   (r"$2\tan^{-1}(\tan^2 x) + C$", r"Puts $t = \tan^2 x$ but writes $dt = \tan x\sec^2 x\,dx$, dropping the $2$ from the chain rule."),
   (r"$\tan^{-1}(\cos 2x) + C$", r"Follows the $\cos 2x$ route correctly but takes $d(\cos 2x) = 2\sin 2x\,dx$, losing the sign.")],
  r"Divide by $\cos^4 x$: the integrand becomes $\frac{2\tan x\sec^2 x}{\tan^4 x + 1}$. With $t = \tan^2 x$, $dt = 2\tan x\sec^2 x\,dx$, so the integral is $\int \frac{dt}{1 + t^2} = \tan^{-1}(\tan^2 x) + C$. (Equivalently $-\tan^{-1}(\cos 2x) + C$, which differs by a constant.)",
  r"Losing constant factors when converting $\sin 2x$ or $\sin^4 x + \cos^4 x$.",
  "U08-A-trig-to-arctan", "Choose a substitution that turns quartic trig into $1 + t^2$; two equivalent routes.",
  cognitive="Analysis", source_class="XII",
  **AD(sin(2*x)/(sin(x)**4 + cos(x)**4), o, pts=[pi/6, pi/5, pi/3]))

o = [tan(x) - cot(x) - 3*x, tan(x) - cot(x) + 3*x, tan(x) - cot(x) - 2*x, tan(x) + cot(x) - 3*x]
q("U08-A-047", TOPIC_T, "Sixth powers simplified", "Difficult", "Multi-step computation MCQ",
  r"$\int \frac{\sin^6 x + \cos^6 x}{\sin^2 x\cos^2 x}\,dx$ " + CI + " equals",
  r"$\tan x - \cot x - 3x + C$",
  [(r"$\tan x - \cot x + 3x + C$", r"Writes $\sin^6 x + \cos^6 x = 1 + 3\sin^2 x\cos^2 x$, a sign slip in the cube expansion."),
   (r"$\tan x - \cot x - 2x + C$", r"Uses $\sin^6 x + \cos^6 x = 1 - 2\sin^2 x\cos^2 x$, which is the identity for fourth powers."),
   (r"$\tan x + \cot x - 3x + C$", r"Simplifies correctly but takes $\int \operatorname{cosec}^2 x\,dx = \cot x$.")],
  r"$\sin^6 x + \cos^6 x = (\sin^2 x + \cos^2 x)^3 - 3\sin^2 x\cos^2 x(\sin^2 x + \cos^2 x) = 1 - 3\sin^2 x\cos^2 x$. So the integrand is $\frac{1}{\sin^2 x\cos^2 x} - 3 = \sec^2 x + \operatorname{cosec}^2 x - 3$, giving $\tan x - \cot x - 3x + C$.",
  r"Confusing the identities for $\sin^4 x + \cos^4 x$ and $\sin^6 x + \cos^6 x$.",
  "U08-A-identity-cancel", "Cube identity, splitting, three standard integrals.",
  cognitive="Analysis", source_class="XII",
  **AD((sin(x)**6 + cos(x)**6)/(sin(x)**2*cos(x)**2), o))

a_, b_ = symbols('a b', real=True)
o = [log(sin(x - a_)/sin(x - b_))/sin(a_ - b_), log(sin(x - b_)/sin(x - a_))/sin(a_ - b_),
     sin(a_ - b_)*log(sin(x - a_)/sin(x - b_)), log(cos(x - a_)/cos(x - b_))/sin(a_ - b_)]
q("U08-A-048", TOPIC_T, "Product of two shifted sines", "Difficult", "Multi-step computation MCQ",
  r"Let $a$ and $b$ be constants with $\sin(a - b) \neq 0$. Then $\int \frac{dx}{\sin(x - a)\sin(x - b)}$ " + CI + " equals",
  r"$\frac{1}{\sin(a - b)}\log_e\left|\frac{\sin(x - a)}{\sin(x - b)}\right| + C$",
  [(r"$\frac{1}{\sin(a - b)}\log_e\left|\frac{\sin(x - b)}{\sin(x - a)}\right| + C$", r"Writes $\sin(a - b) = \sin((x - a) - (x - b))$, reversing the order, which flips the sign of the result."),
   (r"$\sin(a - b)\log_e\left|\frac{\sin(x - a)}{\sin(x - b)}\right| + C$", r"Multiplies by $\sin(a - b)$ after splitting but never divides by it to compensate."),
   (r"$\frac{1}{\sin(a - b)}\log_e\left|\frac{\cos(x - a)}{\cos(x - b)}\right| + C$", r"Splits correctly into $\cot(x - a) - \cot(x - b)$ but integrates $\cot\theta$ as $\log_e|\cos\theta|$.")],
  r"Write $\sin(a - b) = \sin((x - b) - (x - a)) = \sin(x - b)\cos(x - a) - \cos(x - b)\sin(x - a)$. Then $\frac{1}{\sin(x - a)\sin(x - b)} = \frac{1}{\sin(a - b)}\left[\cot(x - a) - \cot(x - b)\right]$, which integrates to $\frac{1}{\sin(a - b)}\left[\log_e|\sin(x - a)| - \log_e|\sin(x - b)|\right] + C$.",
  r"Choosing the wrong order when writing $a - b$ as a difference of the two angles.",
  "U08-A-shift-angle", "Non-obvious multiply-and-divide trick, sign bookkeeping.",
  cognitive="Analysis", source_class="XII",
  **AD(1/(sin(x - a_)*sin(x - b_)), o))

s6 = x**Rational(1, 6)
o = [2*sqrt(x) - 3*x**Rational(1, 3) + 6*s6 - 6*log(1 + s6),
     2*sqrt(x) + 3*x**Rational(1, 3) + 6*s6 + 6*log(1 + s6),
     2*sqrt(x) - 3*x**Rational(1, 3) + 6*s6 + 6*log(1 + s6),
     sqrt(x)/3 - x**Rational(1, 3)/2 + s6 - log(1 + s6)]
q("U08-A-049", TOPIC_S, "Two different roots", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int \frac{dx}{\sqrt{x} + \sqrt[3]{x}}$ " + CI + " equals",
  r"$2\sqrt{x} - 3\sqrt[3]{x} + 6\sqrt[6]{x} - 6\log_e\left(1 + \sqrt[6]{x}\right) + C$",
  [(r"$2\sqrt{x} + 3\sqrt[3]{x} + 6\sqrt[6]{x} + 6\log_e\left(1 + \sqrt[6]{x}\right) + C$", r"Divides $t^3$ by $t + 1$ as if by $t - 1$, getting $t^2 + t + 1$ with remainder $+1$."),
   (r"$2\sqrt{x} - 3\sqrt[3]{x} + 6\sqrt[6]{x} + 6\log_e\left(1 + \sqrt[6]{x}\right) + C$", r"Gets the quotient $t^2 - t + 1$ but takes the remainder as $+1$, though $t^3 = (t + 1)(t^2 - t + 1) - 1$."),
   (r"$\frac{1}{3}\sqrt{x} - \frac{1}{2}\sqrt[3]{x} + \sqrt[6]{x} - \log_e\left(1 + \sqrt[6]{x}\right) + C$", r"Substitutes $x = t^6$ but uses $dx = t^5dt$, dropping the factor $6$.")],
  r"Put $x = t^6$ ($t > 0$), $dx = 6t^5dt$, $\sqrt{x} + \sqrt[3]{x} = t^3 + t^2$. The integral is $6\int \frac{t^3}{t + 1}dt = 6\int\left(t^2 - t + 1 - \frac{1}{t + 1}\right)dt = 2t^3 - 3t^2 + 6t - 6\log_e(1 + t) + C$, with $t = \sqrt[6]{x}$.",
  r"Choosing $t$ from only one of the two roots, or slipping in the long division.",
  "U08-A-root-subst", "LCM substitution, polynomial division, four-term back-substitution.",
  cognitive="Analysis", source_class="XII",
  **AD(1/(sqrt(x) + x**Rational(1, 3)), o))

E3 = 2**(2**(2**x))
o = [E3/log(2)**3, E3/log(2)**2, E3/log(2), E3*log(2)**3]
q("U08-A-050", TOPIC_S, "Nested exponentials", "Difficult", "Multi-step computation MCQ",
  r"$\int 2^{2^{2^x}}\cdot 2^{2^x}\cdot 2^x\,dx$ " + CI + " equals",
  r"$\frac{2^{2^{2^x}}}{(\log_e 2)^3} + C$",
  [(r"$\frac{2^{2^{2^x}}}{(\log_e 2)^2} + C$", r"Counts only two factors of $\log_e 2$, missing one layer of the chain rule."),
   (r"$\frac{2^{2^{2^x}}}{\log_e 2} + C$", r"Treats the integrand like $\int 2^u du$ with $u = 2^{2^x}$ and the rest as $du$, ignoring the $\log_e 2$ factors in $du$."),
   (r"$(\log_e 2)^3\,2^{2^{2^x}} + C$", r"Multiplies by the $\log_e 2$ factors in place of dividing, confusing differentiation with integration.")],
  r"Let $t = 2^{2^{2^x}}$. Then $\frac{dt}{dx} = 2^{2^{2^x}}\log_e 2\cdot 2^{2^x}\log_e 2\cdot 2^x\log_e 2$, so the integrand equals $\frac{1}{(\log_e 2)^3}\frac{dt}{dx}$. The integral is $\frac{2^{2^{2^x}}}{(\log_e 2)^3} + C$.",
  r"Missing a chain-rule factor in nested exponentials.",
  "U08-A-subst-nested-exp", "Three-level chain rule in reverse.",
  cognitive="Analysis", source_class="XII",
  **AD(2**(2**(2**x))*2**(2**x)*2**x, o, pts=[0, Rational(1, 2), 1]))

def _c51():
    v = fit(sin(5*x)/sin(x), x + p_*sin(2*x) + q_*sin(4*x), [p_, q_], [pi/6, pi/5])
    return v[p_] + 2*v[q_]
q("U08-A-051", TOPIC_T, "Ratio of multiple-angle sines", "Difficult", "Inverse/parameter MCQ",
  r"If $\int \frac{\sin 5x}{\sin x}\,dx = x + p\sin 2x + q\sin 4x + C$ " + CI + r", then $p + 2q$ equals",
  r"$2$",
  [(r"$6$", r"Reaches $1 + 2\cos 2x + 2\cos 4x$ but integrates $2\cos kx$ as $2\sin kx$, so $p = 2$, $q = 2$."),
   (r"$1$", r"Writes $\frac{\sin 5x}{\sin x} = 1 + \cos 2x + \cos 4x$, missing the factors $2$, so $p = \frac{1}{2}$, $q = \frac{1}{4}$."),
   (r"$0$", r"Uses $\sin 3x - \sin x = -2\cos 2x\sin x$, a sign slip, so $p = -1$, $q = \frac{1}{2}$.")],
  r"$\sin 5x - \sin 3x = 2\cos 4x\sin x$ and $\sin 3x - \sin x = 2\cos 2x\sin x$, so $\sin 5x = \sin x(1 + 2\cos 2x + 2\cos 4x)$. Integrating $1 + 2\cos 2x + 2\cos 4x$ gives $x + \sin 2x + \frac{1}{2}\sin 4x$, so $p = 1$, $q = \frac{1}{2}$ and $p + 2q = 2$.",
  r"Not telescoping $\sin 5x$ into multiples of $\sin x$.",
  "U08-A-multiple-angle-ratio", "Telescoping sum-to-product identities, then integration and matching.",
  check=_c51, values=[2, 6, 1, 0], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"If $\int \frac{\sin 5x}{\sin x}\,dx = x + p\sin 2x + q\sin 4x + C$, where $C$ is the constant of integration, then $p + 2q$ is", answer=2))

o = [-sin(x) - sin(2*x)/2, sin(x) + sin(2*x)/2, -sin(x) - sin(2*x), -sin(x) + sin(2*x)/2]
q("U08-A-052", TOPIC_T, "Simplifying a multiple-angle quotient", "Difficult", "Multi-step computation MCQ",
  r"$\int \frac{\cos 5x + \cos 4x}{1 - 2\cos 3x}\,dx$ " + CI + " equals",
  r"$-\sin x - \frac{\sin 2x}{2} + C$",
  [(r"$\sin x + \frac{\sin 2x}{2} + C$", r"Simplifies the integrand to $\cos x + \cos 2x$, losing the overall minus sign."),
   (r"$-\sin x - \sin 2x + C$", r"Simplifies correctly to $-(\cos x + \cos 2x)$ but integrates $\cos 2x$ as $\sin 2x$."),
   (r"$-\sin x + \frac{\sin 2x}{2} + C$", r"Gets the integrand as $-\cos x + \cos 2x$, a sign slip in one term.")],
  r"By product-to-sum, $(\cos x + \cos 2x)(1 - 2\cos 3x) = \cos x + \cos 2x - (\cos 4x + \cos 2x) - (\cos 5x + \cos x) = -(\cos 5x + \cos 4x)$. Hence $\frac{\cos 5x + \cos 4x}{1 - 2\cos 3x} = -(\cos x + \cos 2x)$ wherever $1 - 2\cos 3x \neq 0$, and the integral is $-\sin x - \frac{\sin 2x}{2} + C$.",
  r"Sign errors while reducing a multiple-angle quotient.",
  "U08-A-multiple-angle-ratio", "Non-obvious simplification by product-to-sum, then two integrals.",
  cognitive="Analysis", source_class="XII",
  **AD((cos(5*x) + cos(4*x))/(1 - 2*cos(3*x)), o))

R = (x - 1)/(x + 2)
o = [Rational(4, 3)*R**Rational(1, 4), 4*R**Rational(1, 4), R**Rational(1, 4)/12, Rational(4, 3)*(1/R)**Rational(1, 4)]
q("U08-A-053", TOPIC_S, "Substituting a ratio", "Difficult", "Multi-step computation MCQ",
  r"For $x > 1$, $\int \frac{dx}{(x - 1)^{3/4}(x + 2)^{5/4}}$ " + CI + " equals",
  r"$\frac{4}{3}\left(\frac{x - 1}{x + 2}\right)^{1/4} + C$",
  [(r"$4\left(\frac{x - 1}{x + 2}\right)^{1/4} + C$", r"Uses $dt = \frac{dx}{(x + 2)^2}$, forgetting the factor $3$ in $\frac{d}{dx}\frac{x - 1}{x + 2} = \frac{3}{(x + 2)^2}$."),
   (r"$\frac{1}{12}\left(\frac{x - 1}{x + 2}\right)^{1/4} + C$", r"Multiplies by the new exponent $\frac{1}{4}$ in place of dividing by it."),
   (r"$\frac{4}{3}\left(\frac{x + 2}{x - 1}\right)^{1/4} + C$", r"Integrates correctly in $t$ but substitutes back the reciprocal ratio.")],
  r"Write the denominator as $(x + 2)^2\left(\frac{x - 1}{x + 2}\right)^{3/4}$. Put $t = \frac{x - 1}{x + 2}$, $dt = \frac{3\,dx}{(x + 2)^2}$. The integral becomes $\frac{1}{3}\int t^{-3/4}dt = \frac{4}{3}t^{1/4} = \frac{4}{3}\left(\frac{x - 1}{x + 2}\right)^{1/4} + C$.",
  r"Not seeing the exponents add to $2$, which suggests the ratio substitution.",
  "U08-A-algebraic-ratio-subst", "Spot exponent sum $2$, ratio substitution and its derivative.",
  cognitive="Analysis", source_class="XII",
  **AD(1/((x - 1)**Rational(3, 4)*(x + 2)**Rational(5, 4)), o, pts=[2, 3, Rational(5, 2)]))

def _c54():
    f = 1/(cos(x)**3*sqrt(sin(2*x)))
    v = fit(f, p_*sqrt(tan(x)) + q_*tan(x)**Rational(5, 2), [p_, q_], [pi/6, pi/4], extra=[pi/5, pi/3])
    return simplify(5*v[p_]*v[q_])
q("U08-A-054", TOPIC_T, "Converting to tan x with a root", "Difficult", "Inverse/parameter MCQ",
  r"For $0 < x < \frac{\pi}{2}$, if $\int \frac{dx}{\cos^3 x\sqrt{\sin 2x}} = p(\tan x)^{1/2} + q(\tan x)^{5/2} + C$ " + CI + r", then $5pq$ equals",
  r"$2$",
  [(r"$4$", r"Writes $\sqrt{\sin 2x}$ as $\sqrt{\sin x\cos x}$, losing the $\sqrt{2}$, so $p = 2$, $q = \frac{2}{5}$."),
   (r"$8$", r"Writes the integrand with $\sqrt{2}$ in the numerator, so $p = 2\sqrt{2}$, $q = \frac{2\sqrt{2}}{5}$."),
   (r"$-2$", r"Uses $\sec^2 x = 1 - \tan^2 x$, so $q = -\frac{\sqrt{2}}{5}$ while $p = \sqrt{2}$.")],
  r"$\cos^3 x\sqrt{2\sin x\cos x} = \sqrt{2}\cos^4 x\sqrt{\tan x}$, so the integrand is $\frac{\sec^4 x}{\sqrt{2}\sqrt{\tan x}} = \frac{(1 + \tan^2 x)\sec^2 x}{\sqrt{2}\sqrt{\tan x}}$. With $t = \tan x$: $\frac{1}{\sqrt{2}}\int (t^{-1/2} + t^{3/2})dt = \frac{1}{\sqrt{2}}\left(2t^{1/2} + \frac{2}{5}t^{5/2}\right)$. So $p = \sqrt{2}$, $q = \frac{\sqrt{2}}{5}$ and $5pq = 2$.",
  r"Losing the $\sqrt{2}$ from $\sin 2x = 2\sin x\cos x$ under the root.",
  "U08-A-divide-by-cos-power", "Rewrite in $\\tan x$ with a root, substitution, two coefficients.",
  check=_c54, values=[2, 4, 8, -2], cognitive="Analysis", source_class="XII",
  numerical=dict(question=r"For $0 < x < \frac{\pi}{2}$, if $\int \frac{dx}{\cos^3 x\sqrt{\sin 2x}} = p(\tan x)^{1/2} + q(\tan x)^{5/2} + C$, where $C$ is the constant of integration, then $5pq$ is", answer=2))

def _c55():
    f = (5*x**8 + 7*x**6)/(x**2 + 1 + 2*x**7)**2
    F = integrate(f, x)
    c = Symbol('c')
    cv = solve(F.subs(x, 0) + c, c)[0]
    return simplify(F.subs(x, 1) + cv)
q("U08-A-055", TOPIC_S, "Hidden quotient rule", "Difficult", "Multi-step computation MCQ",
  r"Let $f(x) = \int \frac{5x^8 + 7x^6}{(x^2 + 1 + 2x^7)^2}\,dx$ for $x \geq 0$, with $f(0) = 0$. Then $f(1)$ equals",
  r"$\frac{1}{4}$",
  [(r"$-\frac{1}{4}$", r"Integrates $-t^{-2}$ as $-\frac{1}{t}$, a sign slip, so $f(x) = -\frac{x^7}{2x^7 + x^2 + 1}$."),
   (r"$\frac{1}{16}$", r"Keeps the square in the denominator, taking $f(x) = \frac{x^7}{(2x^7 + x^2 + 1)^2}$."),
   (r"$\frac{1}{8}$", r"Lowers the power of $t^{-2}$ but divides by the old exponent, getting $\frac{1}{2t}$.")],
  r"Divide numerator and denominator by $x^{14}$: the integrand is $\frac{5x^{-6} + 7x^{-8}}{(2 + x^{-5} + x^{-7})^2}$. With $t = 2 + x^{-5} + x^{-7}$, $dt = -(5x^{-6} + 7x^{-8})dx$, so $f(x) = \frac{1}{t} + c = \frac{x^7}{2x^7 + x^2 + 1} + c$. Then $f(0) = 0$ gives $c = 0$, and $f(1) = \frac{1}{4}$.",
  r"Not dividing by the right power of $x$ to expose the derivative.",
  "U08-A-algebraic-power-subst", "Non-obvious division by $x^{14}$, substitution, initial condition.",
  check=_c55, values=[Rational(1, 4), Rational(-1, 4), Rational(1, 16), Rational(1, 8)],
  cognitive="Analysis", source_class="XII")

o = [log(sec(x) + tan(x)) + log(sec(x)), log(sec(x) + tan(x)) - log(sec(x)), tan(x) + sec(x), 2*log(sec(x) + tan(x))]
q("U08-A-056", TOPIC_T, "Recognising a perfect square", "Difficult", "Multi-step computation MCQ",
  r"For $0 < x < \frac{\pi}{2}$, $\int \sqrt{1 + 2\tan x(\sec x + \tan x)}\,dx$ " + CI + " equals",
  r"$\log_e|\sec x + \tan x| + \log_e|\sec x| + C$",
  [(r"$\log_e|\sec x + \tan x| - \log_e|\sec x| + C$", r"Finds $\sec x + \tan x$ under the root but integrates $\tan x$ as $-\log_e|\sec x|$."),
   (r"$\tan x + \sec x + C$", r"Gets $\sec x + \tan x$ and integrates it as if it were $\sec^2 x + \sec x\tan x$."),
   (r"$2\log_e|\sec x + \tan x| + C$", r"Uses $\int \tan x\,dx = \log_e|\sec x + \tan x|$, copying the result for $\sec x$.")],
  r"$1 + 2\tan x\sec x + 2\tan^2 x = (1 + \tan^2 x) + 2\sec x\tan x + \tan^2 x = \sec^2 x + 2\sec x\tan x + \tan^2 x = (\sec x + \tan x)^2$. On $\left(0, \frac{\pi}{2}\right)$, $\sec x + \tan x > 0$, so the integrand is $\sec x + \tan x$, giving $\log_e|\sec x + \tan x| + \log_e|\sec x| + C$.",
  r"Not recognising the expression under the root as a perfect square.",
  "U08-A-root-identity", "Hidden perfect square, sign check, two standard integrals.",
  cognitive="Analysis", source_class="XII",
  **AD(sqrt(1 + 2*tan(x)*(sec(x) + tan(x))), o, pts=[pi/6, pi/4, pi/3]))
