import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

# ---------------------------------------------------------------- helpers
x = Symbol('x')
a_, b_, c_ = symbols('a_ b_ c_')

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TT, FF, TF, FT = (True, True), (False, False), (True, False), (False, True)

TP = "Integration by parts"
TE = r"Integrals of the form e^x [f(x) + f'(x)]"
TF_ = "Integration by partial fractions"
CST = r"(where $C$ is the constant of integration)"

_PTS = [Rational(2, 7), Rational(3, 5), Rational(5, 4), Rational(7, 3), Rational(13, 4),
        Rational(9, 2), Rational(11, 5)]


def dv(*opts):
    """Derivatives of the option antiderivatives (indefinite-integral check pattern)."""
    return [diff(o, x) for o in opts]


def fit(F, f, unk):
    """Solve for the unknown constants in F so that F' = f, using sample points."""
    g = diff(F, x) - f
    zero = {u: 0 for u in unk}
    rows = [[N(diff(g, u).subs(x, p), 60) for u in unk] for p in _PTS]
    rhs = [N(-g.subs(zero).subs(x, p), 60) for p in _PTS]
    n = len(unk)
    sol = Matrix(rows[:n]).LUsolve(Matrix(rhs[:n]))
    for row, r_ in zip(rows[n:], rhs[n:]):
        assert abs(complex(N(sum(c*v for c, v in zip(row, sol)) - r_, 40))) < 1e-25
    return tuple(nsimplify(v, rational=True, tolerance=1e-25) for v in sol)


def is_anti(F, f):
    """True when F' = f identically (symbolic, with a numeric fallback)."""
    d = diff(F, x) - f
    try:
        if simplify(d) == 0:
            return True
    except Exception:
        pass
    return all(abs(complex(N(d.subs(x, p), 30))) < 1e-20 for p in _PTS)


# =================================================================== EASY

q("U08-B-001", TP, "Polynomial times exponential", "Easy", "Single-step computation MCQ",
  r"$\int xe^{2x}\,dx$ equals " + CST,
  r"$\frac{e^{2x}}{4}(2x-1) + C$",
  [(r"$\frac{e^{2x}}{4}(2x+1) + C$", r"Sign slip in the second term: adds $\int\frac{e^{2x}}{2}dx = \frac{e^{2x}}{4}$ rather than subtracting it."),
   (r"$\frac{e^{2x}}{2}(x-1) + C$", r"Takes $v = \frac{e^{2x}}{2}$ correctly but evaluates $\int\frac{e^{2x}}{2}dx$ as $\frac{e^{2x}}{2}$, dropping the chain factor $\frac12$: $\frac{xe^{2x}}{2} - \frac{e^{2x}}{2}$."),
   (r"$\frac{e^{2x}}{2}(2x-1) + C$", r"Takes $v = e^{2x}$ (no factor $\frac12$) in the first step, then integrates correctly: $xe^{2x} - \int e^{2x}dx = xe^{2x} - \frac{e^{2x}}{2}$.")],
  r"Take $u = x$, $dv = e^{2x}dx$, so $v = \frac{e^{2x}}{2}$. Then $\int xe^{2x}dx = \frac{xe^{2x}}{2} - \int\frac{e^{2x}}{2}dx = \frac{xe^{2x}}{2} - \frac{e^{2x}}{4} + C = \frac{e^{2x}}{4}(2x-1) + C$.",
  r"Losing the factor $\frac{1}{k}$ when integrating $e^{kx}$.",
  "U08-B-parts-poly-exp", "One application of integration by parts with a chain factor.",
  check=lambda: x*exp(2*x),
  values=dv(exp(2*x)*(2*x - 1)/4, exp(2*x)*(2*x + 1)/4, exp(2*x)*(x - 1)/2, exp(2*x)*(2*x - 1)/2),
  source_class="XII")

q("U08-B-002", TP, "Polynomial times trigonometric", "Easy", "Single-step computation MCQ",
  r"$\int x\cos 2x\,dx$ equals " + CST,
  r"$\frac{x\sin 2x}{2} + \frac{\cos 2x}{4} + C$",
  [(r"$\frac{x\sin 2x}{2} - \frac{\cos 2x}{4} + C$", r"Takes $\int\sin 2x\,dx = \frac{\cos 2x}{2}$ (sign slip), so $-\int\frac{\sin 2x}{2}dx$ becomes $-\frac{\cos 2x}{4}$."),
   (r"$\frac{x\sin 2x}{2} + \frac{\cos 2x}{2} + C$", r"Integrates $\frac{\sin 2x}{2}$ as $-\frac{\cos 2x}{2}$, forgetting the chain factor $\frac12$ in the second integration."),
   (r"$x\sin 2x + \frac{\cos 2x}{2} + C$", r"Takes $v = \sin 2x$ (no $\frac12$), then $x\sin 2x - \int\sin 2x\,dx = x\sin 2x + \frac{\cos 2x}{2}$.")],
  r"With $u = x$, $v = \frac{\sin 2x}{2}$: $\int x\cos 2x\,dx = \frac{x\sin 2x}{2} - \int\frac{\sin 2x}{2}dx = \frac{x\sin 2x}{2} + \frac{\cos 2x}{4} + C$.",
  r"Dropping the factor $\frac12$ from $\int\cos 2x\,dx$ or $\int\sin 2x\,dx$.",
  "U08-B-parts-poly-trig", "Single integration by parts; two chain factors to track.",
  check=lambda: x*cos(2*x),
  values=dv(x*sin(2*x)/2 + cos(2*x)/4, x*sin(2*x)/2 - cos(2*x)/4, x*sin(2*x)/2 + cos(2*x)/2, x*sin(2*x) + cos(2*x)/2),
  source_class="XII")

q("U08-B-003", TP, "Power times logarithm", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int x^2\log_e x\,dx$ equals " + CST,
  r"$\frac{x^3}{3}\log_e x - \frac{x^3}{9} + C$",
  [(r"$\frac{x^3}{3}\log_e x - \frac{x^3}{3} + C$", r"Drops the factor $\frac13$ of $v$ inside $\int v\,du$, integrating $x^2$ rather than $\frac{x^2}{3}$."),
   (r"$\frac{x^3}{3}\log_e x + \frac{x^3}{9} + C$", r"Sign slip: adds $\int v\,du$ rather than subtracting it."),
   (r"$\frac{x^3}{3}\log_e x - \frac{x^4}{12} + C$", r"Does not multiply by $du = \frac{dx}{x}$, integrating $\frac{x^3}{3}$ rather than $\frac{x^2}{3}$.")],
  r"Take $u = \log_e x$, $dv = x^2dx$, so $v = \frac{x^3}{3}$. Then $\int x^2\log_e x\,dx = \frac{x^3}{3}\log_e x - \int\frac{x^3}{3}\cdot\frac1x dx = \frac{x^3}{3}\log_e x - \frac{x^3}{9} + C$.",
  r"Mishandling $v\,du$ when the logarithm is chosen as $u$.",
  "U08-B-parts-log-power", "One by-parts step with the standard LIATE choice.",
  check=lambda: x**2*log(x),
  values=dv(x**3/3*log(x) - x**3/9, x**3/3*log(x) - x**3/3, x**3/3*log(x) + x**3/9, x**3/3*log(x) - x**4/12),
  source_class="XII", cognitive="Recall")

q("U08-B-004", TP, "Inverse sine by parts", "Easy", "Single-step computation MCQ",
  r"For $-1 < x < 1$, $\int\sin^{-1}x\,dx$ equals " + CST,
  r"$x\sin^{-1}x + \sqrt{1-x^2} + C$",
  [(r"$x\sin^{-1}x - \sqrt{1-x^2} + C$", r"Evaluates $\int\frac{x}{\sqrt{1-x^2}}dx$ as $+\sqrt{1-x^2}$, losing the minus sign from $dt = -2x\,dx$."),
   (r"$x\sin^{-1}x + 2\sqrt{1-x^2} + C$", r"With $t = 1-x^2$, keeps the minus sign but drops the $\frac12$ in $x\,dx = -\frac{dt}{2}$, so $\int\frac{x}{\sqrt{1-x^2}}dx = -2\sqrt{1-x^2}$."),
   (r"$x\sin^{-1}x + \frac{1}{2}\sqrt{1-x^2} + C$", r"Writes $-\frac12\int t^{-1/2}dt$ but integrates $t^{-1/2}$ as $t^{1/2}$ (no division by $\frac12$), getting $-\frac12\sqrt{1-x^2}$.")],
  r"Take $u = \sin^{-1}x$, $dv = dx$: $\int\sin^{-1}x\,dx = x\sin^{-1}x - \int\frac{x}{\sqrt{1-x^2}}dx$. With $t = 1 - x^2$, $\int\frac{x}{\sqrt{1-x^2}}dx = -\sqrt{1-x^2}$, so the answer is $x\sin^{-1}x + \sqrt{1-x^2} + C$.",
  r"Sign and factor errors in $\int\frac{x}{\sqrt{1-x^2}}dx$.",
  "U08-B-parts-inverse-trig", "By parts with unit second function, then one substitution.",
  check=lambda: asin(x),
  values=dv(x*asin(x) + sqrt(1 - x**2), x*asin(x) - sqrt(1 - x**2), x*asin(x) + 2*sqrt(1 - x**2), x*asin(x) + sqrt(1 - x**2)/2),
  source_class="XII")

q("U08-B-005", TE, "Recognising f and f'", "Easy", "Single-step computation MCQ",
  r"$\int e^x(\sin x + \cos x)\,dx$ equals " + CST,
  r"$e^x\sin x + C$",
  [(r"$e^x\cos x + C$", r"Takes $f(x) = \cos x$, although its derivative is $-\sin x$, not $\sin x$."),
   (r"$-e^x\cos x + C$", r"Integrates the $\sin x$ term alone as $-\cos x$ and attaches $e^x$, ignoring the $\cos x$ term."),
   (r"$e^x(\sin x + \cos x) + C$", r"Treats $e^x g(x)$ as its own antiderivative, as though $g$ were constant.")],
  r"Here $f(x) = \sin x$ and $f'(x) = \cos x$, so the integrand is $e^x(f + f')$, whose antiderivative is $e^xf(x)$. Hence the integral is $e^x\sin x + C$.",
  r"Picking the wrong member of the pair as $f$.",
  "U08-B-ex-f-fprime-trig", "Direct recognition of the $e^x(f + f')$ form.",
  check=lambda: exp(x)*(sin(x) + cos(x)),
  values=dv(exp(x)*sin(x), exp(x)*cos(x), -exp(x)*cos(x), exp(x)*(sin(x) + cos(x))),
  source_class="XII", cognitive="Recall")

q("U08-B-006", TE, "Rational f with e^x", "Easy", "Single-step computation MCQ",
  r"For $x \ne 0$, $\int e^x\left(\frac{x-1}{x^2}\right)dx$ equals " + CST,
  r"$\frac{e^x}{x} + C$",
  [(r"$\frac{e^x}{x^2} + C$", r"Splits the bracket as $\frac1x - \frac{1}{x^2}$ but takes the size of the second piece, $\frac{1}{x^2}$, as $f$."),
   (r"$-\frac{e^x}{x^2} + C$", r"Takes the second piece $-\frac{1}{x^2}$ as $f$ rather than the first piece."),
   (r"$e^x\log_e|x| + C$", r"Integrates only the first piece $\frac1x$ to $\log_e|x|$ and multiplies by $e^x$, treating $e^x$ as a constant.")],
  r"$\frac{x-1}{x^2} = \frac1x - \frac{1}{x^2}$. With $f(x) = \frac1x$, $f'(x) = -\frac{1}{x^2}$, so the integrand is $e^x(f + f')$ and the integral is $\frac{e^x}{x} + C$.",
  r"Not splitting the fraction to expose $f + f'$.",
  "U08-B-ex-f-fprime-rational", "One split, then the standard result.",
  check=lambda: exp(x)*(x - 1)/x**2,
  values=dv(exp(x)/x, exp(x)/x**2, -exp(x)/x**2, exp(x)*log(x)),
  source_class="XII")

q("U08-B-007", TE, "Logarithmic f with e^x", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int e^x\left(\frac{x\log_e x + 1}{x}\right)dx$ equals " + CST,
  r"$e^x\log_e x + C$",
  [(r"$\frac{e^x}{x} + C$", r"Splits as $\log_e x + \frac1x$ and takes the derivative piece $\frac1x$ as $f$."),
   (r"$e^x(x\log_e x - x) + C$", r"Replaces $\log_e x$ by its own antiderivative $x\log_e x - x$ and uses that as $f$."),
   (r"$xe^x\log_e x + C$", r"Ignores the denominator $x$, works with $e^x(x\log_e x + 1)$ and takes $f = x\log_e x$, wrongly believing $(x\log_e x)' = 1$.")],
  r"The bracket equals $\log_e x + \frac1x$. With $f(x) = \log_e x$, $f'(x) = \frac1x$, the integrand is $e^x(f + f')$, so the integral is $e^x\log_e x + C$.",
  r"Choosing the derivative piece as $f$.",
  "U08-B-ex-f-fprime-log", "One split exposes the standard form.",
  check=lambda: exp(x)*(x*log(x) + 1)/x,
  values=dv(exp(x)*log(x), exp(x)/x, exp(x)*(x*log(x) - x), x*exp(x)*log(x)),
  source_class="XII")

q("U08-B-008", TF_, "Distinct linear factors", "Easy", "Single-step computation MCQ",
  r"$\int\frac{dx}{(x-1)(x+2)}$ equals " + CST,
  r"$\frac{1}{3}\log_e\left|\frac{x-1}{x+2}\right| + C$",
  [(r"$\log_e\left|\frac{x-1}{x+2}\right| + C$", r"Omits the factor $\frac13$ obtained from the cover-up values $\pm\frac13$."),
   (r"$\frac{1}{3}\log_e\left|\frac{x+2}{x-1}\right| + C$", r"Swaps the signs of the two partial-fraction coefficients."),
   (r"$\frac{1}{3}\log_e|(x-1)(x+2)| + C$", r"Takes both coefficients as $+\frac13$, dropping the sign of $-\frac13$ for $\frac{1}{x+2}$.")],
  r"Cover-up gives $\frac{1}{(x-1)(x+2)} = \frac{1}{3}\cdot\frac{1}{x-1} - \frac{1}{3}\cdot\frac{1}{x+2}$. Integrating, $\frac13\log_e|x-1| - \frac13\log_e|x+2| + C = \frac13\log_e\left|\frac{x-1}{x+2}\right| + C$.",
  r"Sign or scale errors in the cover-up rule.",
  "U08-B-pf-linear-distinct", "Two-term decomposition, then standard logs.",
  check=lambda: 1/((x - 1)*(x + 2)),
  values=dv((log(x - 1) - log(x + 2))/3, log(x - 1) - log(x + 2), (log(x + 2) - log(x - 1))/3, (log(x - 1) + log(x + 2))/3),
  source_class="XII", cognitive="Recall")


def _c9():
    a, b = fit(a_*log(x + 1) + b_*log(x + 2), x/((x + 1)*(x + 2)), [a_, b_])
    return b - a
q("U08-B-009", TF_, "Coefficients of the logarithms", "Easy", "Inverse/parameter MCQ",
  r"If $\int\frac{x}{(x+1)(x+2)}\,dx = a\log_e|x+1| + b\log_e|x+2| + C$, where $a, b$ are constants and $C$ is the constant of integration, then $b - a$ equals",
  r"$3$",
  [(r"$-3$", r"Attaches the two cover-up values to the wrong factors, taking $a = 2$, $b = -1$."),
   (r"$1$", r"Loses the sign at $x = -1$ in the cover-up, taking $a = 1$ with $b = 2$."),
   (r"$\frac{1}{3}$", r"Substitutes $x = 1$ and $x = 2$ in the cover-up, getting $a = \frac{1}{1+2} = \frac13$ and $b = \frac{2}{2+1} = \frac23$.")],
  r"Write $\frac{x}{(x+1)(x+2)} = \frac{a}{x+1} + \frac{b}{x+2}$. Putting $x = -1$: $a = \frac{-1}{1} = -1$; putting $x = -2$: $b = \frac{-2}{-1} = 2$. So $b - a = 3$.",
  r"Evaluating the cover-up at the wrong points or with the wrong sign.",
  "U08-B-pf-coefficients", "One decomposition with two cover-up evaluations.",
  check=_c9, values=[3, -3, 1, Rational(1, 3)],
  numerical=dict(question=r"If $\int\frac{x}{(x+1)(x+2)}\,dx = a\log_e|x+1| + b\log_e|x+2| + C$, where $a, b$ are constants and $C$ is the constant of integration, then the value of $b - a$ is", answer=3),
  source_class="XII")

q("U08-B-010", TF_, "Linear and irreducible quadratic factor", "Easy", "Single-step computation MCQ",
  r"For $x \ne 0$, $\int\frac{dx}{x(x^2+1)}$ equals " + CST,
  r"$\log_e|x| - \frac{1}{2}\log_e(x^2+1) + C$",
  [(r"$\log_e|x| - \log_e(x^2+1) + C$", r"Integrates $\frac{x}{x^2+1}$ as $\log_e(x^2+1)$, dropping the factor $\frac12$."),
   (r"$\log_e|x| + \frac{1}{2}\log_e(x^2+1) + C$", r"Sign slip: takes the second partial fraction as $+\frac{x}{x^2+1}$."),
   (r"$\log_e|x| - \tan^{-1}x + C$", r"Puts a constant numerator over $x^2+1$, writing $\frac1x - \frac{1}{x^2+1}$, rather than the linear numerator $x$.")],
  r"$\frac{1}{x(x^2+1)} = \frac1x - \frac{x}{x^2+1}$ (check: $\frac{x^2 + 1 - x^2}{x(x^2+1)}$). Integrating gives $\log_e|x| - \frac12\log_e(x^2+1) + C$.",
  r"Using a constant numerator over an irreducible quadratic factor.",
  "U08-B-pf-quadratic-factor", "Short decomposition and two standard integrals.",
  check=lambda: 1/(x*(x**2 + 1)),
  values=dv(log(x) - log(x**2 + 1)/2, log(x) - log(x**2 + 1), log(x) + log(x**2 + 1)/2, log(x) - atan(x)),
  source_class="XII")

q("U08-B-011", TF_, "Repeated linear factor", "Easy", "Single-step computation MCQ",
  r"$\int\frac{3x+1}{(x+2)^2}\,dx$ equals " + CST,
  r"$3\log_e|x+2| + \frac{5}{x+2} + C$",
  [(r"$3\log_e|x+2| - \frac{5}{x+2} + C$", r"Integrates $-\frac{5}{(x+2)^2}$ as $-\frac{5}{x+2}$, losing the sign from the power rule."),
   (r"$3\log_e|x+2| - \frac{7}{x+2} + C$", r"Writes $3x + 1 = 3(x+2) + 7$ (adds 6 to 1), then $\int\frac{7}{(x+2)^2}dx = -\frac{7}{x+2}$."),
   (r"$3\log_e|x+2| + \frac{2}{x+2} + C$", r"Compares constants in $A(x+2) + B = 3x + 1$ as $A + B = 1$ (missing the factor 2), so $B = -2$.")],
  r"$3x + 1 = 3(x+2) - 5$, so the integrand is $\frac{3}{x+2} - \frac{5}{(x+2)^2}$. Since $\int\frac{dx}{(x+2)^2} = -\frac{1}{x+2}$, the integral is $3\log_e|x+2| + \frac{5}{x+2} + C$.",
  r"Sign error when integrating $(x+2)^{-2}$.",
  "U08-B-pf-repeated", "One rewrite and two standard integrals.",
  check=lambda: (3*x + 1)/(x + 2)**2,
  values=dv(3*log(x + 2) + 5/(x + 2), 3*log(x + 2) - 5/(x + 2), 3*log(x + 2) - 7/(x + 2), 3*log(x + 2) + 2/(x + 2)),
  source_class="XII")

q("U08-B-012", TP, "Repeated integration by parts", "Easy", "Multi-step computation MCQ",
  r"$\int x^2e^x\,dx$ equals " + CST,
  r"$e^x(x^2 - 2x + 2) + C$",
  [(r"$e^x(x^2 + 2x + 2) + C$", r"Adds every term, missing the alternating signs of repeated integration by parts."),
   (r"$e^x(x^2 - 2x) + C$", r"Uses $\int xe^x\,dx = xe^x$, dropping its $-e^x$, so $x^2e^x - 2xe^x$."),
   (r"$e^x(x^2 - 2x - 2) + C$", r"Expands $-2(xe^x - e^x)$ as $-2xe^x - 2e^x$ (sign slip in the last step).")],
  r"$\int x^2e^xdx = x^2e^x - 2\int xe^xdx = x^2e^x - 2(xe^x - e^x) + C = e^x(x^2 - 2x + 2) + C$.",
  r"Losing the alternating signs in repeated integration by parts.",
  "U08-B-parts-repeated", "Two quick by-parts steps.",
  check=lambda: x**2*exp(x),
  values=dv(exp(x)*(x**2 - 2*x + 2), exp(x)*(x**2 + 2*x + 2), exp(x)*(x**2 - 2*x), exp(x)*(x**2 - 2*x - 2)),
  source_class="XII")

q("U08-B-013", TP, "Logarithm over a power", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int\frac{\log_e x}{x^2}\,dx$ equals " + CST,
  r"$-\frac{1+\log_e x}{x} + C$",
  [(r"$\frac{1-\log_e x}{x} + C$", r"Correct $v = -\frac1x$, but sign slip in $-\int v\,du$: writes $-\frac{\log_e x}{x} - \int\frac{dx}{x^2} = -\frac{\log_e x}{x} + \frac1x$."),
   (r"$\frac{1+\log_e x}{x} + C$", r"Takes $v = +\frac1x$, then $\frac{\log_e x}{x} - \int\frac{dx}{x^2} = \frac{\log_e x}{x} + \frac1x$."),
   (r"$\frac{\log_e x - 1}{x} + C$", r"Takes the antiderivative of $x^{-2}$ as $+x^{-1}$ in both places: $\frac{\log_e x}{x} - \frac1x$.")],
  r"Take $u = \log_e x$, $dv = x^{-2}dx$, $v = -\frac1x$. Then $\int\frac{\log_e x}{x^2}dx = -\frac{\log_e x}{x} + \int\frac{dx}{x^2} = -\frac{\log_e x}{x} - \frac1x + C = -\frac{1+\log_e x}{x} + C$.",
  r"Sign errors with $\int x^{-2}dx = -x^{-1}$.",
  "U08-B-parts-log-power", "One by-parts step with a negative power.",
  check=lambda: log(x)/x**2,
  values=dv(-(1 + log(x))/x, (1 - log(x))/x, (1 + log(x))/x, (log(x) - 1)/x),
  source_class="XII")

q("U08-B-014", TP, "Polynomial times secant squared", "Easy", "Single-step computation MCQ",
  r"$\int x\sec^2x\,dx$ equals " + CST,
  r"$x\tan x + \log_e|\cos x| + C$",
  [(r"$x\tan x - \log_e|\cos x| + C$", r"Uses $\int\tan x\,dx = \log_e|\cos x|$ (sign slip), so subtracting gives $-\log_e|\cos x|$."),
   (r"$x\tan x - \log_e|\sin x| + C$", r"Uses $\int\tan x\,dx = \log_e|\sin x|$, which is the result for $\cot x$."),
   (r"$x\tan x - \log_e|\sec x + \tan x| + C$", r"Uses $\int\tan x\,dx = \log_e|\sec x + \tan x|$, which is the result for $\sec x$.")],
  r"With $u = x$, $v = \tan x$: $\int x\sec^2x\,dx = x\tan x - \int\tan x\,dx = x\tan x - \log_e|\sec x| + C = x\tan x + \log_e|\cos x| + C$.",
  r"Misremembering $\int\tan x\,dx$.",
  "U08-B-parts-poly-trig", "One by-parts step plus a standard integral.",
  check=lambda: x*sec(x)**2,
  values=dv(x*tan(x) + log(cos(x)), x*tan(x) - log(cos(x)), x*tan(x) - log(sin(x)), x*tan(x) - log(sec(x) + tan(x))),
  source_class="XII")


def _c15():
    k = Symbol('k')
    F = integrate(x*exp(x), x) + k
    kv = solve(F.subs(x, 0), k)[0]
    return simplify(F.subs({k: kv, x: 1}))
q("U08-B-015", TP, "Fixing the constant", "Easy", "Multi-step computation MCQ",
  r"Let $f(x) = \int xe^x\,dx$ with $f(0) = 0$. Then $f(1)$ equals",
  r"$1$",
  [(r"$0$", r"Ignores the constant: takes $f(x) = (x-1)e^x$, which has $f(0) = -1 \ne 0$, and gets $f(1) = 0$."),
   (r"$2e - 1$", r"Sign slip gives $f(x) = (x+1)e^x + C$; then $f(0) = 0$ gives $C = -1$ and $f(1) = 2e - 1$."),
   (r"$-1$", r"Finds $(x-1)e^x + C$ but solves $-1 + C = 0$ as $C = -1$, so $f(1) = -1$.")],
  r"$\int xe^xdx = (x-1)e^x + C$. From $f(0) = -1 + C = 0$, $C = 1$, so $f(x) = (x-1)e^x + 1$ and $f(1) = 0 + 1 = 1$.",
  r"Ignoring or mis-solving for the constant of integration.",
  "U08-B-parts-poly-exp", "One by-parts step and one condition.",
  check=_c15, values=[1, 0, 2*E - 1, -1],
  numerical=dict(question=r"Let $f(x) = \int xe^x\,dx$ with $f(0) = 0$. Then the value of $f(1)$ is", answer=1),
  source_class="XII")

q("U08-B-016", TF_, "Partial fractions after a trigonometric substitution", "Easy", "Single-step computation MCQ",
  r"$\int\frac{\cos x}{(1+\sin x)(3+\sin x)}\,dx$, for $\sin x \ne -1$, equals " + CST,
  r"$\frac{1}{2}\log_e\left|\frac{1+\sin x}{3+\sin x}\right| + C$",
  [(r"$\log_e\left|\frac{1+\sin x}{3+\sin x}\right| + C$", r"Omits the factor $\frac{1}{3-1} = \frac12$ in $\frac{1}{(t+1)(t+3)} = \frac12\left(\frac{1}{t+1} - \frac{1}{t+3}\right)$."),
   (r"$\frac{1}{2}\log_e\left|\frac{3+\sin x}{1+\sin x}\right| + C$", r"Reverses the signs of the two partial fractions."),
   (r"$\frac{1}{4}\log_e\left|\frac{1+\sin x}{3+\sin x}\right| + C$", r"Divides by $3 + 1$ rather than $3 - 1$ when splitting.")],
  r"Put $t = \sin x$, $dt = \cos x\,dx$: $\int\frac{dt}{(t+1)(t+3)} = \frac12\int\left(\frac{1}{t+1} - \frac{1}{t+3}\right)dt = \frac12\log_e\left|\frac{t+1}{t+3}\right| + C$. Back-substituting gives $\frac12\log_e\left|\frac{1+\sin x}{3+\sin x}\right| + C$.",
  r"Forgetting the factor $\frac{1}{b-a}$ in $\frac{1}{(t+a)(t+b)}$.",
  "U08-B-pf-trig-sub", "One substitution and one two-term split.",
  check=lambda: cos(x)/((1 + sin(x))*(3 + sin(x))),
  values=dv((log(1 + sin(x)) - log(3 + sin(x)))/2, log(1 + sin(x)) - log(3 + sin(x)),
            (log(3 + sin(x)) - log(1 + sin(x)))/2, (log(1 + sin(x)) - log(3 + sin(x)))/4),
  source_class="XII")


def _c17():
    s1 = is_anti(exp(x)*sin(x), exp(x)*(cos(x) - sin(x)))
    s2 = is_anti(x*log(x/E), log(x))
    return (s1, s2)
q("U08-B-017", TE, "Checking claimed antiderivatives", "Easy", "Statement-based MCQ",
  r"Statement I: $\int e^x(\cos x - \sin x)\,dx = e^x\sin x + C$. Statement II: For $x > 0$, $\int\log_e x\,dx = x\log_e\left(\frac{x}{e}\right) + C$. (Here $C$ is the constant of integration.) In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts Statement I by matching the pair $\sin x$, $\cos x$ without checking the sign: $(e^x\sin x)' = e^x(\sin x + \cos x)$."),
   (ST_FF, r"Does not recognise $x\log_e\frac{x}{e} = x\log_e x - x$, the standard antiderivative of $\log_e x$."),
   (ST_TF, r"Gets both judgements reversed: accepts the sign-wrong Statement I and rejects the rewritten form in Statement II.")],
  r"$\frac{d}{dx}(e^x\sin x) = e^x(\sin x + \cos x) \ne e^x(\cos x - \sin x)$; the correct antiderivative is $e^x\cos x$, so Statement I is false. $x\log_e\frac{x}{e} = x\log_e x - x$, and $\frac{d}{dx}(x\log_e x - x) = \log_e x$, so Statement II is true.",
  r"Applying the $e^x(f + f')$ result without checking the sign of $f'$.",
  "U08-B-statements-ex-log", "Two independent one-line verifications.",
  check=_c17, values=[FT, TT, FF, TF], cognitive="Understanding", source_class="XII")

# =================================================================== MEDIUM

q("U08-B-018", TE, "Hidden f + f' via an identity", "Medium", "Multi-step computation MCQ",
  r"$\int e^x(1 + \tan x + \tan^2x)\,dx$ equals " + CST,
  r"$e^x\tan x + C$",
  [(r"$e^x\sec^2x + C$", r"Rewrites the bracket as $\tan x + \sec^2x$ but takes the derivative piece $\sec^2x$ as $f$."),
   (r"$e^x(1 + \tan x) + C$", r"Takes $f = 1 + \tan x$ and assumes the leftover $\tan^2x$ is its derivative, though $(1 + \tan x)' = \sec^2x$."),
   (r"$e^x\tan^2x + C$", r"Takes $f = \tan^2x$ and assumes the leftover $1 + \tan x$ is its derivative.")],
  r"Since $1 + \tan^2x = \sec^2x$, the bracket is $\tan x + \sec^2x = f + f'$ with $f = \tan x$. Hence the integral is $e^x\tan x + C$.",
  r"Not using $1 + \tan^2x = \sec^2x$ to expose the pair.",
  "U08-B-ex-f-fprime-trig", "Needs a trigonometric identity before the standard form appears.",
  check=lambda: exp(x)*(1 + tan(x) + tan(x)**2),
  values=dv(exp(x)*tan(x), exp(x)*sec(x)**2, exp(x)*(1 + tan(x)), exp(x)*tan(x)**2),
  source_class="XII")

q("U08-B-019", TE, "Half-angle form", "Medium", "Multi-step computation MCQ",
  r"For $\cos x \ne -1$, $\int e^x\left(\frac{1+\sin x}{1+\cos x}\right)dx$ equals " + CST,
  r"$e^x\tan\frac{x}{2} + C$",
  [(r"$e^x\cot\frac{x}{2} + C$", r"Uses $1 + \cos x = 2\sin^2\frac x2$ (wrong identity), so the bracket becomes $\frac12\operatorname{cosec}^2\frac x2 + \cot\frac x2$, and takes $f = \cot\frac x2$."),
   (r"$-e^x\cot\frac{x}{2} + C$", r"Uses $1 + \cos x = 2\sin^2\frac x2$ (wrong identity), reaches $\frac12\operatorname{cosec}^2\frac x2 + \cot\frac x2$, integrates only the piece $\frac12\operatorname{cosec}^2\frac x2$ to $-\cot\frac x2$, drops the $\cot\frac x2$ term, and attaches $e^x$."),
   (r"$\frac{1}{2}e^x\sec^2\frac{x}{2} + C$", r"Takes the derivative piece $\frac12\sec^2\frac x2$ as $f$.")],
  r"$1 + \cos x = 2\cos^2\frac x2$ and $\sin x = 2\sin\frac x2\cos\frac x2$, so $\frac{1+\sin x}{1+\cos x} = \frac12\sec^2\frac x2 + \tan\frac x2$. With $f = \tan\frac x2$, $f' = \frac12\sec^2\frac x2$, so the integral is $e^x\tan\frac x2 + C$.",
  r"Using the wrong half-angle identity or the wrong member as $f$.",
  "U08-B-ex-f-fprime-trig", "Half-angle identities, a split, then the standard form.",
  check=lambda: exp(x)*(1 + sin(x))/(1 + cos(x)),
  values=dv(exp(x)*tan(x/2), exp(x)*cot(x/2), -exp(x)*cot(x/2), exp(x)*sec(x/2)**2/2),
  source_class="XII")

q("U08-B-020", TE, "Rational f found by splitting", "Medium", "Multi-step computation MCQ",
  r"For $x \ne -1$, $\int\frac{xe^x}{(1+x)^2}\,dx$ equals " + CST,
  r"$\frac{e^x}{1+x} + C$",
  [(r"$\frac{e^x}{(1+x)^2} + C$", r"Writes $\frac{x}{(1+x)^2} = \frac{1}{1+x} - \frac{1}{(1+x)^2}$ but takes the size of the second piece as $f$."),
   (r"$-\frac{e^x}{1+x} + C$", r"Sign slip in the split, $\frac{x}{(1+x)^2} = -\frac{1}{1+x} + \frac{1}{(1+x)^2}$, which reads as $f + f'$ with $f = -\frac{1}{1+x}$."),
   (r"$\frac{xe^x}{1+x} + C$", r"Keeps the numerator and takes $f = \frac{x}{1+x}$ without checking that $f + f'$ matches.")],
  r"$\frac{x}{(1+x)^2} = \frac{(1+x) - 1}{(1+x)^2} = \frac{1}{1+x} - \frac{1}{(1+x)^2}$. With $f = \frac{1}{1+x}$, $f' = -\frac{1}{(1+x)^2}$, so the integral is $\frac{e^x}{1+x} + C$.",
  r"Not writing $x = (1+x) - 1$ to split the fraction.",
  "U08-B-ex-f-fprime-rational", "Algebraic split then the $e^x(f+f')$ result.",
  check=lambda: x*exp(x)/(1 + x)**2,
  values=dv(exp(x)/(1 + x), exp(x)/(1 + x)**2, -exp(x)/(1 + x), x*exp(x)/(1 + x)),
  source_class="XII")

q("U08-B-021", TE, "Exponent other than x", "Medium", "Multi-step computation MCQ",
  r"$\int e^{\tan^{-1}x}\left(\frac{1 + x + x^2}{1 + x^2}\right)dx$ equals " + CST,
  r"$xe^{\tan^{-1}x} + C$",
  [(r"$(1+x)e^{\tan^{-1}x} + C$", r"Splits the bracket as $(1 + x)\cdot\frac{1}{1+x^2} + \frac{x^2}{1+x^2}$, takes $f = 1 + x$ from the numerator and does not check that $\frac{d}{dx}\left[(1+x)e^{\tan^{-1}x}\right] = e^{\tan^{-1}x}\left(1 + \frac{1+x}{1+x^2}\right)$ differs from the integrand."),
   (r"$\frac{x}{1+x^2}e^{\tan^{-1}x} + C$", r"Takes the extra term $\frac{x}{1+x^2}$ in the bracket as the function $f$."),
   (r"$(1+x^2)e^{\tan^{-1}x} + C$", r"With $x = \tan t$ the integral becomes $\int e^t(\tan t + \sec^2t)\,dt$; takes the derivative piece $\sec^2t = 1 + x^2$ as $f$.")],
  r"Put $x = \tan t$, $dx = \sec^2t\,dt$: the integral becomes $\int e^t\frac{1 + \tan t + \tan^2t}{\sec^2t}\sec^2t\,dt = \int e^t(\tan t + \sec^2t)\,dt = e^t\tan t + C$. Back-substituting gives $xe^{\tan^{-1}x} + C$.",
  r"Picking the wrong function after the substitution.",
  "U08-B-ex-f-fprime-composite", "Substitution, an identity, then the standard form.",
  check=lambda: exp(atan(x))*(1 + x + x**2)/(1 + x**2),
  values=dv(x*exp(atan(x)), (1 + x)*exp(atan(x)), x/(1 + x**2)*exp(atan(x)), (1 + x**2)*exp(atan(x))),
  source_class="XII")

q("U08-B-022", TP, "Logarithm of a quadratic", "Medium", "Multi-step computation MCQ",
  r"$\int\log_e(1 + x^2)\,dx$ equals " + CST,
  r"$x\log_e(1+x^2) - 2x + 2\tan^{-1}x + C$",
  [(r"$x\log_e(1+x^2) - 2x - 2\tan^{-1}x + C$", r"Splits $\frac{2x^2}{1+x^2}$ as $2 + \frac{2}{1+x^2}$ (sign slip)."),
   (r"$x\log_e(1+x^2) - 2\tan^{-1}x + C$", r"Treats $\frac{2x^2}{1+x^2}$ as $\frac{2}{1+x^2}$, losing the polynomial part."),
   (r"$x\log_e(1+x^2) - \log_e(1+x^2) + C$", r"Treats $\int\frac{2x^2}{1+x^2}dx$ as $\int\frac{2x}{1+x^2}dx = \log_e(1+x^2)$.")],
  r"With $u = \log_e(1+x^2)$, $v = x$: $\int\log_e(1+x^2)dx = x\log_e(1+x^2) - \int\frac{2x^2}{1+x^2}dx$. Since $\frac{2x^2}{1+x^2} = 2 - \frac{2}{1+x^2}$, this is $x\log_e(1+x^2) - 2x + 2\tan^{-1}x + C$.",
  r"Mishandling the improper fraction $\frac{2x^2}{1+x^2}$.",
  "U08-B-parts-log-composite", "By parts followed by division of an improper fraction.",
  check=lambda: log(1 + x**2),
  values=dv(x*log(1 + x**2) - 2*x + 2*atan(x), x*log(1 + x**2) - 2*x - 2*atan(x), x*log(1 + x**2) - 2*atan(x), x*log(1 + x**2) - log(1 + x**2)),
  source_class="XII")

q("U08-B-023", TP, "Polynomial times inverse tangent", "Medium", "Multi-step computation MCQ",
  r"$\int x\tan^{-1}x\,dx$ equals " + CST,
  r"$\frac{(x^2+1)\tan^{-1}x - x}{2} + C$",
  [(r"$\frac{(x^2-1)\tan^{-1}x + x}{2} + C$", r"Sign slip on $-\int v\,du$: adds $\frac12\int\frac{x^2}{1+x^2}dx = \frac12(x - \tan^{-1}x)$."),
   (r"$\frac{x^2\tan^{-1}x}{2} - \frac{1}{4}\log_e(1+x^2) + C$", r"Replaces $\frac{x^2}{1+x^2}$ by $\frac{x}{1+x^2}$ inside $\int v\,du$."),
   (r"$\frac{(x^2-1)\tan^{-1}x - x}{2} + C$", r"Splits $\frac{x^2}{1+x^2}$ as $1 + \frac{1}{1+x^2}$ (sign slip).")],
  r"With $u = \tan^{-1}x$, $v = \frac{x^2}{2}$: $\int x\tan^{-1}x\,dx = \frac{x^2}{2}\tan^{-1}x - \frac12\int\frac{x^2}{1+x^2}dx = \frac{x^2}{2}\tan^{-1}x - \frac12(x - \tan^{-1}x) + C = \frac{(x^2+1)\tan^{-1}x - x}{2} + C$.",
  r"Errors in splitting $\frac{x^2}{1+x^2}$.",
  "U08-B-parts-inverse-trig", "By parts, then an algebraic split, then collecting terms.",
  check=lambda: x*atan(x),
  values=dv(((x**2 + 1)*atan(x) - x)/2, ((x**2 - 1)*atan(x) + x)/2, x**2*atan(x)/2 - log(1 + x**2)/4, ((x**2 - 1)*atan(x) - x)/2),
  source_class="XII")

q("U08-B-024", TP, "Cyclic integration by parts", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\sin(\log_e x)\,dx$ equals " + CST,
  r"$\frac{x}{2}\left(\sin(\log_e x) - \cos(\log_e x)\right) + C$",
  [(r"$\frac{x}{2}\left(\sin(\log_e x) + \cos(\log_e x)\right) + C$", r"Writes down the standard result for $\int\cos(\log_e x)\,dx$ in place of $\int\sin(\log_e x)\,dx$."),
   (r"$x\left(\sin(\log_e x) - \cos(\log_e x)\right) + C$", r"Reaches $2I = x(\sin(\log_e x) - \cos(\log_e x))$ and forgets to divide by 2."),
   (r"$\frac{x}{2}\left(\cos(\log_e x) - \sin(\log_e x)\right) + C$", r"Transposes with a sign slip: from $I = x\sin(\log_e x) - x\cos(\log_e x) - I$ writes $-2I = x(\sin(\log_e x) - \cos(\log_e x))$.")],
  r"With $u = \sin(\log_e x)$, $v = x$: $I = x\sin(\log_e x) - \int\cos(\log_e x)dx = x\sin(\log_e x) - x\cos(\log_e x) - I$. Hence $2I = x(\sin(\log_e x) - \cos(\log_e x))$ and $I = \frac x2(\sin(\log_e x) - \cos(\log_e x)) + C$.",
  r"Mistakes when solving for the integral that reappears.",
  "U08-B-parts-cyclic", "Two by-parts steps and solving for the repeated integral.",
  check=lambda: sin(log(x)),
  values=dv(x/2*(sin(log(x)) - cos(log(x))), x/2*(sin(log(x)) + cos(log(x))), x*(sin(log(x)) - cos(log(x))), x/2*(cos(log(x)) - sin(log(x)))),
  source_class="XII")

q("U08-B-025", TP, "Exponential times cosine, coefficients", "Medium", "Inverse/parameter MCQ",
  r"If $\int e^{2x}\cos x\,dx = e^{2x}(a\cos x + b\sin x) + C$, where $a, b$ are constants and $C$ is the constant of integration, then the ordered pair $(a, b)$ is",
  r"$\left(\frac{2}{5}, \frac{1}{5}\right)$",
  [(r"$\left(\frac{1}{5}, \frac{2}{5}\right)$", r"Recalls $\frac{e^{ax}}{a^2+b^2}(a\cos bx + b\sin bx)$ with the two constants interchanged."),
   (r"$\left(\frac{2}{3}, \frac{1}{3}\right)$", r"Divides by $2 + 1 = 3$ rather than $2^2 + 1^2 = 5$."),
   (r"$\left(\frac{2}{3}, -\frac{1}{3}\right)$", r"Differentiates the right side using $\frac{d}{dx}\cos x = \sin x$, giving $2a + b = 1$, $a + 2b = 0$.")],
  r"Differentiate: $\frac{d}{dx}[e^{2x}(a\cos x + b\sin x)] = e^{2x}[(2a + b)\cos x + (2b - a)\sin x]$. Matching with $e^{2x}\cos x$: $2a + b = 1$, $2b - a = 0$, so $b = \frac15$, $a = \frac25$.",
  r"Misremembering the $e^{ax}\cos bx$ formula.",
  "U08-B-parts-cyclic", "Set up and solve a two-equation linear system.",
  check=lambda: fit(exp(2*x)*(a_*cos(x) + b_*sin(x)), exp(2*x)*cos(x), [a_, b_]),
  values=[(Rational(2, 5), Rational(1, 5)), (Rational(1, 5), Rational(2, 5)), (Rational(2, 3), Rational(1, 3)), (Rational(2, 3), Rational(-1, 3))],
  numerical=dict(question=r"If $\int e^{2x}\cos x\,dx = e^{2x}(a\cos x + b\sin x) + C$, where $a, b$ are constants and $C$ is the constant of integration, then the value of $5(a + b)$ is", answer=3),
  source_class="XII")

q("U08-B-026", TP, "Secant cubed", "Medium", "Multi-step computation MCQ",
  r"$\int\sec^3x\,dx$ equals " + CST,
  r"$\frac{1}{2}\left(\sec x\tan x + \log_e|\sec x + \tan x|\right) + C$",
  [(r"$\frac{1}{2}\left(\sec x\tan x - \log_e|\sec x + \tan x|\right) + C$", r"Uses $\tan^2x = \sec^2x + 1$, which flips the sign of the $\int\sec x\,dx$ term."),
   (r"$\sec x\tan x + \log_e|\sec x + \tan x| + C$", r"Reaches $2I = \sec x\tan x + \log_e|\sec x + \tan x|$ and forgets to divide by 2."),
   (r"$\frac{1}{2}\sec x\tan x + \log_e|\sec x + \tan x| + C$", r"Divides only the first term by 2 when solving for $I$.")],
  r"With $u = \sec x$, $dv = \sec^2x\,dx$: $I = \sec x\tan x - \int\sec x\tan^2x\,dx = \sec x\tan x - \int\sec x(\sec^2x - 1)dx = \sec x\tan x - I + \log_e|\sec x + \tan x|$. So $I = \frac12(\sec x\tan x + \log_e|\sec x + \tan x|) + C$.",
  r"Using $\tan^2x = \sec^2x + 1$ or not halving fully.",
  "U08-B-parts-sec-cube", "By parts, an identity, and solving for the repeated integral.",
  check=lambda: sec(x)**3,
  values=dv((sec(x)*tan(x) + log(sec(x) + tan(x)))/2, (sec(x)*tan(x) - log(sec(x) + tan(x)))/2,
            sec(x)*tan(x) + log(sec(x) + tan(x)), sec(x)*tan(x)/2 + log(sec(x) + tan(x))),
  source_class="XII")

q("U08-B-027", TP, "Parts after substitution", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\cos\sqrt{x}\,dx$ equals " + CST,
  r"$2\left(\sqrt{x}\sin\sqrt{x} + \cos\sqrt{x}\right) + C$",
  [(r"$2\left(\sqrt{x}\sin\sqrt{x} - \cos\sqrt{x}\right) + C$", r"Uses $\int\sin t\,dt = \cos t$ in the by-parts step."),
   (r"$\sqrt{x}\sin\sqrt{x} + \cos\sqrt{x} + C$", r"Uses $dx = t\,dt$ rather than $2t\,dt$, losing the factor 2."),
   (r"$2\sin\sqrt{x} + C$", r"Writes $dx = 2\,dt$, dropping the $t$, so $\int 2\cos t\,dt = 2\sin t$.")],
  r"Put $t = \sqrt x$, $dx = 2t\,dt$: $\int 2t\cos t\,dt = 2(t\sin t - \int\sin t\,dt) = 2(t\sin t + \cos t) + C = 2(\sqrt x\sin\sqrt x + \cos\sqrt x) + C$.",
  r"Mishandling $dx$ when substituting $t = \sqrt x$.",
  "U08-B-parts-after-sub", "Substitution followed by integration by parts.",
  check=lambda: cos(sqrt(x)),
  values=dv(2*(sqrt(x)*sin(sqrt(x)) + cos(sqrt(x))), 2*(sqrt(x)*sin(sqrt(x)) - cos(sqrt(x))), sqrt(x)*sin(sqrt(x)) + cos(sqrt(x)), 2*sin(sqrt(x))),
  source_class="XII")

q("U08-B-028", TP, "Square of the logarithm", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int(\log_e x)^2\,dx$ equals " + CST,
  r"$x(\log_e x)^2 - 2x\log_e x + 2x + C$",
  [(r"$x(\log_e x)^2 - 2x\log_e x - 2x + C$", r"Expands $-2(x\log_e x - x)$ as $-2x\log_e x - 2x$ (sign slip)."),
   (r"$x(\log_e x)^2 - 2x\log_e x + C$", r"Uses $\int\log_e x\,dx = x\log_e x$, dropping its $-x$."),
   (r"$x(\log_e x)^2 - x\log_e x + x + C$", r"Takes $\frac{d}{dx}(\log_e x)^2 = \frac{\log_e x}{x}$, missing the factor 2.")],
  r"With $u = (\log_e x)^2$, $v = x$: $\int(\log_e x)^2dx = x(\log_e x)^2 - \int 2\log_e x\,dx = x(\log_e x)^2 - 2(x\log_e x - x) + C = x(\log_e x)^2 - 2x\log_e x + 2x + C$.",
  r"Dropping the chain factor or the $-x$ in $\int\log_e x\,dx$.",
  "U08-B-parts-log-power", "Two nested by-parts steps.",
  check=lambda: log(x)**2,
  values=dv(x*log(x)**2 - 2*x*log(x) + 2*x, x*log(x)**2 - 2*x*log(x) - 2*x, x*log(x)**2 - 2*x*log(x), x*log(x)**2 - x*log(x) + x),
  source_class="XII")

q("U08-B-029", TP, "Inverse sine with an algebraic factor", "Medium", "Multi-step computation MCQ",
  r"For $-1 < x < 1$, $\int\frac{x\sin^{-1}x}{\sqrt{1-x^2}}\,dx$ equals " + CST,
  r"$x - \sqrt{1-x^2}\,\sin^{-1}x + C$",
  [(r"$-x + \sqrt{1-x^2}\,\sin^{-1}x + C$", r"Takes $v = +\sqrt{1-x^2}$ for $\int\frac{x}{\sqrt{1-x^2}}dx$, then $\sqrt{1-x^2}\sin^{-1}x - \int 1\,dx$."),
   (r"$-x - \sqrt{1-x^2}\,\sin^{-1}x + C$", r"Correct $v = -\sqrt{1-x^2}$, but sign slip in $-\int v\,du$."),
   (r"$\frac{x}{2} - \frac{1}{2}\sqrt{1-x^2}\,\sin^{-1}x + C$", r"Integrates $t^{-1/2}$ as $t^{1/2}$ when finding $v$, so $v = -\frac12\sqrt{1-x^2}$.")],
  r"Take $u = \sin^{-1}x$, $dv = \frac{x}{\sqrt{1-x^2}}dx$, so $v = -\sqrt{1-x^2}$. Then the integral is $-\sqrt{1-x^2}\sin^{-1}x + \int\sqrt{1-x^2}\cdot\frac{1}{\sqrt{1-x^2}}dx = x - \sqrt{1-x^2}\sin^{-1}x + C$.",
  r"Choosing $dv$ but mis-integrating it.",
  "U08-B-parts-inverse-trig", "Non-standard choice of $dv$; the leftover integral collapses.",
  check=lambda: x*asin(x)/sqrt(1 - x**2),
  values=dv(x - sqrt(1 - x**2)*asin(x), -x + sqrt(1 - x**2)*asin(x), -x - sqrt(1 - x**2)*asin(x), x/2 - sqrt(1 - x**2)*asin(x)/2),
  source_class="XII", cognitive="Analysis")

q("U08-B-030", TF_, "Improper rational function", "Medium", "Multi-step computation MCQ",
  r"$\int\frac{x^2+1}{(x-1)(x-2)}\,dx$ equals " + CST,
  r"$x - 2\log_e|x-1| + 5\log_e|x-2| + C$",
  [(r"$-2\log_e|x-1| + 5\log_e|x-2| + C$", r"Skips the long division and applies the cover-up rule directly to the improper fraction."),
   (r"$x + 2\log_e|x-1| + 5\log_e|x-2| + C$", r"Drops the sign of $(1 - 2)$ in the cover-up at $x = 1$."),
   (r"$x - 5\log_e|x-1| + 2\log_e|x-2| + C$", r"Attaches each cover-up value to the wrong factor.")],
  r"Divide: $\frac{x^2+1}{x^2-3x+2} = 1 + \frac{3x-1}{(x-1)(x-2)}$. Cover-up: at $x = 1$, $\frac{2}{-1} = -2$; at $x = 2$, $\frac{5}{1} = 5$. So the integral is $x - 2\log_e|x-1| + 5\log_e|x-2| + C$.",
  r"Applying partial fractions to an improper fraction without dividing first.",
  "U08-B-pf-improper", "Division then a two-term decomposition.",
  check=lambda: (x**2 + 1)/((x - 1)*(x - 2)),
  values=dv(x - 2*log(x - 1) + 5*log(x - 2), -2*log(x - 1) + 5*log(x - 2), x + 2*log(x - 1) + 5*log(x - 2), x - 5*log(x - 1) + 2*log(x - 2)),
  source_class="XII")

q("U08-B-031", TF_, "Repeated factor, coefficients", "Medium", "Inverse/parameter MCQ",
  r"If $\int\frac{dx}{(x-1)^2(x+2)} = a\log_e\left|\frac{x-1}{x+2}\right| + \frac{b}{x-1} + C$, where $a, b$ are constants and $C$ is the constant of integration, then the ordered pair $(a, b)$ is",
  r"$\left(-\frac{1}{9}, -\frac{1}{3}\right)$",
  [(r"$\left(-\frac{1}{9}, \frac{1}{3}\right)$", r"Integrates $\frac{1}{3(x-1)^2}$ as $+\frac{1}{3(x-1)}$, losing the sign from the power rule."),
   (r"$\left(\frac{1}{9}, -\frac{1}{3}\right)$", r"Evaluates $(-2-1)^2$ as $-9$ in the cover-up for $x + 2$, making that coefficient $-\frac19$ and the coefficient of $\frac{1}{x-1}$ equal to $+\frac19$."),
   (r"$\left(-\frac{1}{9}, -\frac{1}{6}\right)$", r"Integrates $(x-1)^{-2}$ as $\frac{(x-1)^{-1}}{-2}$, dividing by the old exponent rather than the new one.")],
  r"Write $\frac{1}{(x-1)^2(x+2)} = \frac{P}{x-1} + \frac{Q}{(x-1)^2} + \frac{R}{x+2}$. Cover-up: $Q = \frac13$, $R = \frac19$, and comparing $x^2$ terms $P + R = 0$, so $P = -\frac19$. Integrating: $-\frac19\log_e|x-1| - \frac{1}{3(x-1)} + \frac19\log_e|x+2| = -\frac19\log_e\left|\frac{x-1}{x+2}\right| - \frac{1}{3(x-1)}$, so $(a, b) = \left(-\frac19, -\frac13\right)$.",
  r"Sign error when integrating the repeated-factor term.",
  "U08-B-pf-repeated", "Three-term decomposition with a repeated factor, then matching a given form.",
  check=lambda: fit(a_*log(x - 1) - a_*log(x + 2) + b_/(x - 1), 1/((x - 1)**2*(x + 2)), [a_, b_]),
  values=[(Rational(-1, 9), Rational(-1, 3)), (Rational(-1, 9), Rational(1, 3)), (Rational(1, 9), Rational(-1, 3)), (Rational(-1, 9), Rational(-1, 6))],
  numerical=dict(question=r"If $\int\frac{dx}{(x-1)^2(x+2)} = a\log_e\left|\frac{x-1}{x+2}\right| + \frac{b}{x-1} + C$, where $a, b$ are constants and $C$ is the constant of integration, then the value of $\frac{1}{ab}$ is", answer=27),
  source_class="XII")

q("U08-B-032", TF_, "Quadratic factor, three coefficients", "Medium", "Inverse/parameter MCQ",
  r"If $\int\frac{dx}{(x+1)(x^2+1)} = a\log_e|x+1| + b\log_e(x^2+1) + c\tan^{-1}x + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then the ordered triple $(a, b, c)$ is",
  r"$\left(\frac{1}{2}, -\frac{1}{4}, \frac{1}{2}\right)$",
  [(r"$\left(\frac{1}{2}, -\frac{1}{2}, \frac{1}{2}\right)$", r"Integrates $-\frac{x}{2(x^2+1)}$ as $-\frac12\log_e(x^2+1)$, dropping a factor $\frac12$."),
   (r"$\left(\frac{1}{2}, \frac{1}{4}, \frac{1}{2}\right)$", r"Solves $P + Q = 0$ (the $x^2$ coefficients) as $Q = P = \frac12$."),
   (r"$\left(1, -\frac{1}{2}, 0\right)$", r"Takes $P = 1$ in the cover-up at $x = -1$, forgetting that $x^2 + 1 = 2$ there; then $Q = -1$, $R = 0$.")],
  r"Let $\frac{1}{(x+1)(x^2+1)} = \frac{P}{x+1} + \frac{Qx + R}{x^2+1}$. Then $P = \frac12$; comparing $x^2$ terms $P + Q = 0$ gives $Q = -\frac12$; comparing constants $P + R = 1$ gives $R = \frac12$. Integrating: $\frac12\log_e|x+1| - \frac14\log_e(x^2+1) + \frac12\tan^{-1}x$, so $(a, b, c) = \left(\frac12, -\frac14, \frac12\right)$.",
  r"Errors in the linear numerator over the quadratic factor.",
  "U08-B-pf-quadratic-factor", "Three unknowns, then two different standard integrals.",
  check=lambda: fit(a_*log(x + 1) + b_*log(x**2 + 1) + c_*atan(x), 1/((x + 1)*(x**2 + 1)), [a_, b_, c_]),
  values=[(Rational(1, 2), Rational(-1, 4), Rational(1, 2)), (Rational(1, 2), Rational(-1, 2), Rational(1, 2)),
          (Rational(1, 2), Rational(1, 4), Rational(1, 2)), (1, Rational(-1, 2), 0)],
  numerical=dict(question=r"If $\int\frac{dx}{(x+1)(x^2+1)} = a\log_e|x+1| + b\log_e(x^2+1) + c\tan^{-1}x + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then the value of $4(a + b + c)$ is", answer=3),
  source_class="XII")


def _c33():
    a, b, c = fit(a_*log(x - 1) + b_*atan(x) + c_*log(x**2 + 1), (3*x**2 + 2*x + 1)/((x - 1)*(x**2 + 1)), [a_, b_, c_])
    return a + b + c
q("U08-B-033", TF_, "A coefficient that vanishes", "Medium", "Inverse/parameter MCQ",
  r"If $\int\frac{3x^2 + 2x + 1}{(x-1)(x^2+1)}\,dx = a\log_e|x-1| + b\tan^{-1}x + c\log_e(x^2+1) + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then $a + b + c$ equals",
  r"$5$",
  [(r"$1$", r"Compares constant terms as $P + R = 1$ rather than $P - R = 1$, getting $R = -2$, so $b = -2$."),
   (r"$\frac{13}{2}$", r"Compares $x^2$ coefficients as $Q = 3$, ignoring the contribution of $P$; then $c = \frac32$, $b = 2$, $a = 3$."),
   (r"$\frac{19}{2}$", r"Takes $P = \frac{6}{1} = 6$ in the cover-up, forgetting $x^2 + 1 = 2$ at $x = 1$; then $Q = -3$, $R = 5$, so $(a, b, c) = \left(6, 5, -\frac32\right)$.")],
  r"Let the integrand be $\frac{P}{x-1} + \frac{Qx + R}{x^2+1}$. At $x = 1$: $P = \frac{6}{2} = 3$. Comparing $x^2$ terms, $P + Q = 3$, so $Q = 0$; comparing constants, $P - R = 1$, so $R = 2$. The integral is $3\log_e|x-1| + 2\tan^{-1}x$, so $a = 3$, $b = 2$, $c = 0$ and $a + b + c = 5$.",
  r"Expecting a nonzero logarithmic term from every quadratic factor.",
  "U08-B-pf-coefficients", "Three unknowns; one turns out to be zero.",
  check=_c33, values=[5, 1, Rational(13, 2), Rational(19, 2)],
  numerical=dict(question=r"If $\int\frac{3x^2 + 2x + 1}{(x-1)(x^2+1)}\,dx = a\log_e|x-1| + b\tan^{-1}x + c\log_e(x^2+1) + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then the value of $a + b + c$ is", answer=5),
  source_class="XII", cognitive="Analysis")

q("U08-B-034", TF_, "Treating x^2 as a single variable", "Medium", "Inverse/parameter MCQ",
  r"If $\int\frac{x^2}{(x^2+1)(x^2+4)}\,dx = a\tan^{-1}x + b\tan^{-1}\frac{x}{2} + C$, where $a, b$ are constants and $C$ is the constant of integration, then the ordered pair $(a, b)$ is",
  r"$\left(-\frac{1}{3}, \frac{2}{3}\right)$",
  [(r"$\left(\frac{1}{3}, -\frac{2}{3}\right)$", r"Swaps the signs of the partial fractions in $y = x^2$, writing $\frac{1}{3(y+1)} - \frac{4}{3(y+4)}$."),
   (r"$\left(-\frac{1}{3}, \frac{4}{3}\right)$", r"Integrates $\frac{4}{3(x^2+4)}$ as $\frac43\tan^{-1}\frac x2$, missing the factor $\frac12$."),
   (r"$\left(-\frac{1}{3}, \frac{1}{3}\right)$", r"Uses $\int\frac{dx}{x^2+4} = \frac14\tan^{-1}\frac x2$.")],
  r"With $y = x^2$, $\frac{y}{(y+1)(y+4)} = -\frac{1}{3(y+1)} + \frac{4}{3(y+4)}$. So the integral is $-\frac13\tan^{-1}x + \frac43\cdot\frac12\tan^{-1}\frac x2 + C$, giving $(a, b) = \left(-\frac13, \frac23\right)$.",
  r"Losing the factor $\frac1a$ in $\int\frac{dx}{x^2+a^2}$.",
  "U08-B-pf-biquadratic", "Substitute $y = x^2$ for the split, then two arctangent integrals.",
  check=lambda: fit(a_*atan(x) + b_*atan(x/2), x**2/((x**2 + 1)*(x**2 + 4)), [a_, b_]),
  values=[(Rational(-1, 3), Rational(2, 3)), (Rational(1, 3), Rational(-2, 3)), (Rational(-1, 3), Rational(4, 3)), (Rational(-1, 3), Rational(1, 3))],
  numerical=dict(question=r"If $\int\frac{x^2}{(x^2+1)(x^2+4)}\,dx = a\tan^{-1}x + b\tan^{-1}\frac{x}{2} + C$, where $a, b$ are constants and $C$ is the constant of integration, then the value of $3(b - a)$ is", answer=3),
  source_class="XII")

q("U08-B-035", TF_, "Odd power: substituting t = x^2 before splitting", "Medium", "Multi-step computation MCQ",
  r"$\int\frac{x^3}{(x^2+1)(x^2+3)}\,dx$ equals " + CST,
  r"$\frac{3}{4}\log_e(x^2+3) - \frac{1}{4}\log_e(x^2+1) + C$",
  [(r"$\frac{3}{2}\log_e(x^2+3) - \frac{1}{2}\log_e(x^2+1) + C$", r"Puts $t = x^2$ but drops the $\frac12$ from $x\,dx = \frac{dt}{2}$, so integrates $\frac{t}{(t+1)(t+3)}$ with no factor $\frac12$."),
   (r"$\frac{3}{4}\log_e(x^2+1) - \frac{1}{4}\log_e(x^2+3) + C$", r"Finds the cover-up values $-\frac12$ and $\frac32$ correctly but attaches $\frac32$ to $\frac{1}{t+1}$ and $-\frac12$ to $\frac{1}{t+3}$."),
   (r"$\frac{3}{4}\log_e(x^2+3) + \frac{1}{4}\log_e(x^2+1) + C$", r"In the cover-up at $t = -1$, takes the numerator $t$ as $+1$, so the coefficient of $\frac{1}{t+1}$ becomes $\frac{1}{2}$ instead of $-\frac12$.")],
  r"Write $x^3\,dx = x^2\cdot x\,dx$ and put $t = x^2$, $dt = 2x\,dx$: the integral is $\frac12\int\frac{t\,dt}{(t+1)(t+3)}$. By cover-up, $\frac{t}{(t+1)(t+3)} = -\frac{1}{2(t+1)} + \frac{3}{2(t+3)}$. Hence the integral is $\frac12\left[-\frac12\log_e(t+1) + \frac32\log_e(t+3)\right] + C = \frac34\log_e(x^2+3) - \frac14\log_e(x^2+1) + C$.",
  r"Losing the factor $\frac12$ from $x\,dx = \frac{dt}{2}$ or the sign of the numerator in the cover-up.",
  "U08-B-pf-odd-power-sub", r"Spotting the substitution $t = x^2$ for an odd integrand, then a split with a variable numerator.",
  check=lambda: x**3/((x**2 + 1)*(x**2 + 3)),
  values=dv(Rational(3, 4)*log(x**2 + 3) - log(x**2 + 1)/4, Rational(3, 2)*log(x**2 + 3) - log(x**2 + 1)/2,
            Rational(3, 4)*log(x**2 + 1) - log(x**2 + 3)/4, Rational(3, 4)*log(x**2 + 3) + log(x**2 + 1)/4),
  source_class="XII")

q("U08-B-036", TF_, "Logarithmic substitution giving an improper fraction", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$ with $\log_e x \ne -1, -2$, $\int\frac{(\log_e x)^2}{x(\log_e x + 1)(\log_e x + 2)}\,dx$ equals " + CST,
  r"$\log_e x + \log_e|\log_e x + 1| - 4\log_e|\log_e x + 2| + C$",
  [(r"$\log_e|\log_e x + 1| - 4\log_e|\log_e x + 2| + C$", r"Applies the cover-up directly to $\frac{t^2}{(t+1)(t+2)}$ without first dividing, so the quotient $1$ (and hence the $\log_e x$ term) is lost."),
   (r"$\log_e x - \log_e|\log_e x + 1| + 4\log_e|\log_e x + 2| + C$", r"Writes $t^2 = (t+1)(t+2) + (3t+2)$, a sign slip in the remainder, which reverses the signs of both partial fractions."),
   (r"$x + \log_e|\log_e x + 1| - 4\log_e|\log_e x + 2| + C$", r"Integrates the quotient $1$ to $t$ correctly but back-substitutes it as $x$ instead of $\log_e x$.")],
  r"Put $t = \log_e x$, $dt = \frac{dx}{x}$: the integral is $\int\frac{t^2\,dt}{(t+1)(t+2)}$. Since $t^2 = (t+1)(t+2) - (3t+2)$ and $\frac{3t+2}{(t+1)(t+2)} = -\frac{1}{t+1} + \frac{4}{t+2}$, the integrand is $1 + \frac{1}{t+1} - \frac{4}{t+2}$. Integrating, $t + \log_e|t+1| - 4\log_e|t+2| + C = \log_e x + \log_e|\log_e x + 1| - 4\log_e|\log_e x + 2| + C$.",
  r"Splitting an improper fraction into partial fractions without dividing first.",
  "U08-B-pf-log-sub-improper", "Substitution, polynomial division, then a two-term split; three steps with sign traps.",
  check=lambda: log(x)**2/(x*(log(x) + 1)*(log(x) + 2)),
  values=dv(log(x) + log(log(x) + 1) - 4*log(log(x) + 2), log(log(x) + 1) - 4*log(log(x) + 2),
            log(x) - log(log(x) + 1) + 4*log(log(x) + 2), x + log(log(x) + 1) - 4*log(log(x) + 2)),
  source_class="XII")

q("U08-B-037", TP, "Parts leading to partial fractions", "Medium", "Multi-step computation MCQ",
  r"For $x \ne 0$, $\int\frac{\tan^{-1}x}{x^2}\,dx$ equals " + CST,
  r"$-\frac{\tan^{-1}x}{x} + \log_e|x| - \frac{1}{2}\log_e(1+x^2) + C$",
  [(r"$-\frac{\tan^{-1}x}{x} + \log_e|x| + \frac{1}{2}\log_e(1+x^2) + C$", r"Writes $\frac{1}{x(1+x^2)} = \frac1x + \frac{x}{1+x^2}$ (sign slip)."),
   (r"$-\frac{\tan^{-1}x}{x} - \log_e|x| + \frac{1}{2}\log_e(1+x^2) + C$", r"Correct $v = -\frac1x$, but subtracts $\int\frac{dx}{x(1+x^2)}$ rather than adding it."),
   (r"$\frac{\tan^{-1}x}{x} - \log_e|x| + \frac{1}{2}\log_e(1+x^2) + C$", r"Takes $v = +\frac1x$ for $\int x^{-2}dx$.")],
  r"With $u = \tan^{-1}x$, $v = -\frac1x$: $I = -\frac{\tan^{-1}x}{x} + \int\frac{dx}{x(1+x^2)}$. Since $\frac{1}{x(1+x^2)} = \frac1x - \frac{x}{1+x^2}$, $I = -\frac{\tan^{-1}x}{x} + \log_e|x| - \frac12\log_e(1+x^2) + C$.",
  r"Sign errors in combining by parts with partial fractions.",
  "U08-B-parts-then-pf", "By parts produces a rational integral that needs partial fractions.",
  check=lambda: atan(x)/x**2,
  values=dv(-atan(x)/x + log(x) - log(1 + x**2)/2, -atan(x)/x + log(x) + log(1 + x**2)/2,
            -atan(x)/x - log(x) + log(1 + x**2)/2, atan(x)/x - log(x) + log(1 + x**2)/2),
  source_class="XII")


def _c38():
    a, b, c = fit(exp(3*x)*(a_*x**2 + b_*x + c_), x**2*exp(3*x), [a_, b_, c_])
    return a + b + c
q("U08-B-038", TP, "Undetermined coefficients for repeated parts", "Medium", "Inverse/parameter MCQ",
  r"If $\int x^2e^{3x}\,dx = e^{3x}(ax^2 + bx + c) + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then $a + b + c$ equals",
  r"$\frac{5}{27}$",
  [(r"$\frac{17}{27}$", r"Ignores the alternating signs, taking $a = \frac13$, $b = \frac29$, $c = \frac{2}{27}$."),
   (r"$\frac{1}{3}$", r"Gets $a = \frac13$ but then uses $\int xe^{3x}dx = (x-1)e^{3x}$, dropping the factors $\frac13$: $b = -\frac23$, $c = \frac23$."),
   (r"$\frac{1}{27}$", r"Sign slip in the last step, taking $c = -\frac{2}{27}$.")],
  r"By parts twice: $\int x^2e^{3x}dx = \frac{x^2e^{3x}}{3} - \frac23\int xe^{3x}dx = \frac{x^2e^{3x}}{3} - \frac23\left(\frac{xe^{3x}}{3} - \frac{e^{3x}}{9}\right) + C$. So $a = \frac13$, $b = -\frac29$, $c = \frac{2}{27}$, and $a + b + c = \frac{9 - 6 + 2}{27} = \frac{5}{27}$.",
  r"Losing the alternating signs or the powers of $\frac13$.",
  "U08-B-parts-repeated", r"Two by-parts steps with factors of $\frac13$ to track.",
  check=_c38, values=[Rational(5, 27), Rational(17, 27), Rational(1, 3), Rational(1, 27)],
  numerical=dict(question=r"If $\int x^2e^{3x}\,dx = e^{3x}(ax^2 + bx + c) + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then the value of $27(a + b + c)$ is", answer=5),
  source_class="XII")


def _c39():
    # concrete instance: f = cos, psi = sin (any antiderivative pair works)
    return x**5*cos(x**3)
_ps = sin(x**3)
q("U08-B-039", TP, "Abstract function by parts", "Medium", "Conceptual/application MCQ",
  r"If $\int f(x)\,dx = \psi(x)$, then $\int x^5f(x^3)\,dx$ equals " + CST,
  r"$\frac{1}{3}x^3\psi(x^3) - \int x^2\psi(x^3)\,dx + C$",
  [(r"$\frac{1}{3}\left[x^3\psi(x^3) - \int x^2\psi(x^3)\,dx\right] + C$", r"Writes $\frac13\left[t\psi(t) - \int\psi(t)\,dt\right]$ but converts $dt$ back as $x^2dx$ rather than $3x^2dx$."),
   (r"$x^3\psi(x^3) - 3\int x^2\psi(x^3)\,dx + C$", r"Drops the $\frac13$ from $x^2dx = \frac{dt}{3}$, so works with $\int tf(t)\,dt$ and then converts $\int\psi(t)\,dt = 3\int x^2\psi(x^3)\,dx$."),
   (r"$\frac{1}{3}x^3\psi(x^3) + \int x^2\psi(x^3)\,dx + C$", r"Sign slip on the $-\int v\,du$ term.")],
  r"Put $t = x^3$, $dt = 3x^2dx$: $\int x^5f(x^3)dx = \frac13\int tf(t)\,dt = \frac13\left[t\psi(t) - \int\psi(t)\,dt\right]$. Converting back, $\int\psi(t)\,dt = \int\psi(x^3)\,3x^2dx$, so the integral is $\frac13x^3\psi(x^3) - \int x^2\psi(x^3)\,dx + C$.",
  r"Forgetting to convert $dt$ back when returning to $x$.",
  "U08-B-parts-abstract", "Substitution and by parts on an unspecified function; careful back-conversion.",
  check=_c39,
  values=[diff(x**3*_ps/3, x) - x**2*_ps, (diff(x**3*_ps, x) - x**2*_ps)/3, diff(x**3*_ps, x) - 3*x**2*_ps, diff(x**3*_ps/3, x) + x**2*_ps],
  source_class="XII", cognitive="Understanding")


def _c40():
    s1 = is_anti(log(x/(x + 1)), 1/(x**2 + x))
    s2 = is_anti(x*atan(x) + log(1 + x**2)/2, atan(x))
    return (s1, s2)
q("U08-B-040", TF_, "Checking a decomposition and a by-parts result", "Medium", "Statement-based MCQ",
  r"Statement I: For $x \ne 0, -1$, $\int\frac{dx}{x^2 + x} = \log_e\left|\frac{x}{x+1}\right| + C$. Statement II: $\int\tan^{-1}x\,dx = x\tan^{-1}x + \frac{1}{2}\log_e(1+x^2) + C$. (Here $C$ is the constant of integration.) In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II without noticing the sign: the correct term is $-\frac12\log_e(1+x^2)$."),
   (ST_FF, r"Reverses the partial fractions in Statement I, believing the answer is $\log_e\left|\frac{x+1}{x}\right|$."),
   (ST_FT, r"Gets both judgements reversed.")],
  r"$\frac{1}{x(x+1)} = \frac1x - \frac{1}{x+1}$, so $\int\frac{dx}{x^2+x} = \log_e\left|\frac{x}{x+1}\right| + C$; Statement I is true. By parts, $\int\tan^{-1}x\,dx = x\tan^{-1}x - \int\frac{x}{1+x^2}dx = x\tan^{-1}x - \frac12\log_e(1+x^2) + C$, so Statement II is false.",
  r"Sign slip in the $-\int v\,du$ term for $\tan^{-1}x$.",
  "U08-B-statements-pf-parts", "Two independent checks of standard results.",
  check=_c40, values=[TF, TT, FF, FT], cognitive="Understanding", source_class="XII")


def _c41():
    pf = apart(x**3/(x + 1), x)
    c = simplify(sum(t*(x + 1) for t in Add.make_args(pf) if t.as_numer_denom()[1].has(x)))
    s1 = (c == 1)
    s2 = is_anti(x**2/4 + x*sin(2*x)/4 - cos(2*x)/8, x*cos(x)**2)
    return (s1, s2)
q("U08-B-041", TF_, "Division before integrating; a by-parts claim", "Medium", "Statement-based MCQ",
  r"Statement I: An antiderivative of $\frac{x^3}{x+1}$ $(x \ne -1)$ contains the term $\log_e|x+1|$ with coefficient $1$. Statement II: $\int x\cos^2x\,dx = \frac{x^2}{4} + \frac{x\sin 2x}{4} - \frac{\cos 2x}{8} + C$, where $C$ is the constant of integration. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Assumes the remainder after division is $+1$ and slips the sign of $\int\sin 2x\,dx$ in Statement II."),
   (ST_TF, r"Writes $x^3 = (x+1)(x^2 - x + 1) + 1$, so takes the remainder as $+1$."),
   (ST_FT, r"Uses $\int\sin 2x\,dx = \frac{\cos 2x}{2}$, which makes the $\cos 2x$ term negative.")],
  r"$x^3 = (x+1)(x^2 - x + 1) - 1$, so $\frac{x^3}{x+1} = x^2 - x + 1 - \frac{1}{x+1}$ and the coefficient of $\log_e|x+1|$ is $-1$: Statement I is false. $x\cos^2x = \frac x2 + \frac{x\cos 2x}{2}$ and $\int x\cos 2x\,dx = \frac{x\sin 2x}{2} + \frac{\cos 2x}{4}$, so $\int x\cos^2x\,dx = \frac{x^2}{4} + \frac{x\sin 2x}{4} + \frac{\cos 2x}{8} + C$: Statement II is false.",
  r"Sign errors in the remainder and in $\int\sin 2x\,dx$.",
  "U08-B-statements-division-parts", "Two checks, each with a sign trap.",
  check=_c41, values=[FF, TT, TF, FT], cognitive="Analysis", source_class="XII")

q("U08-B-042", TE, "Logarithmic substitution to the standard form", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\left[\sin(\log_e x) + \cos(\log_e x)\right]dx$ equals " + CST,
  r"$x\sin(\log_e x) + C$",
  [(r"$x\cos(\log_e x) + C$", r"After $x = e^t$, takes $f(t) = \cos t$, whose derivative is $-\sin t$."),
   (r"$\sin(\log_e x) - \cos(\log_e x) + C$", r"Substitutes $x = e^t$ but forgets $dx = e^tdt$, integrating $\sin t + \cos t$ alone."),
   (r"$x\left[\sin(\log_e x) + \cos(\log_e x)\right] + C$", r"After $x = e^t$, treats $e^tg(t)$ as its own antiderivative.")],
  r"Put $x = e^t$, $dx = e^tdt$: the integral becomes $\int e^t(\sin t + \cos t)\,dt = e^t\sin t + C$, since $(\sin t)' = \cos t$. Back-substituting gives $x\sin(\log_e x) + C$.",
  r"Forgetting the Jacobian $e^t$ under $x = e^t$.",
  "U08-B-parts-logs-ln-sub", "Substitution reveals the $e^t(f + f')$ form.",
  check=lambda: sin(log(x)) + cos(log(x)),
  values=dv(x*sin(log(x)), x*cos(log(x)), sin(log(x)) - cos(log(x)), x*(sin(log(x)) + cos(log(x)))),
  source_class="XII")

# =================================================================== DIFFICULT

q("U08-B-043", TE, "Logarithm of a logarithm", "Difficult", "Multi-step computation MCQ",
  r"For $x > 1$, $\int\left[\log_e(\log_e x) + \frac{1}{(\log_e x)^2}\right]dx$ equals " + CST,
  r"$x\log_e(\log_e x) - \frac{x}{\log_e x} + C$",
  [(r"$x\log_e(\log_e x) + \frac{x}{\log_e x} + C$", r"With $t = \log_e x$, evaluates the leftover $\int e^t\left(\frac{1}{t^2} - \frac1t\right)dt$ as $+\frac{e^t}{t}$ (sign slip)."),
   (r"$x\log_e(\log_e x) + C$", r"With $x = e^t$, uses $e^t(f + f')$ with $f = \log_e t$, overlooking that $f' = \frac1t$, not $\frac{1}{t^2}$."),
   (r"$x\log_e(\log_e x) - \frac{x}{(\log_e x)^2} + C$", r"Evaluates the leftover $\int e^t\left(\frac{1}{t^2} - \frac1t\right)dt$ as $-\frac{e^t}{t^2}$, pairing $e^t$ with the wrong power of $t$.")],
  r"Put $x = e^t$: $\int e^t\left(\log_e t + \frac{1}{t^2}\right)dt = \int e^t\left(\log_e t + \frac1t\right)dt - \int e^t\left(\frac1t - \frac{1}{t^2}\right)dt = e^t\log_e t - \frac{e^t}{t} + C$, using $f = \log_e t$ and $f = \frac1t$. Back-substituting, $x\log_e(\log_e x) - \frac{x}{\log_e x} + C$.",
  r"Not adding and subtracting $\frac1t$ to create two $e^t(f + f')$ pairs.",
  "U08-B-parts-logs-ln-sub", "Substitution plus an add-and-subtract trick to make two standard pairs.",
  check=lambda: log(log(x)) + 1/log(x)**2,
  values=dv(x*log(log(x)) - x/log(x), x*log(log(x)) + x/log(x), x*log(log(x)), x*log(log(x)) - x/log(x)**2),
  source_class="XII", cognitive="Analysis")

q("U08-B-044", TE, "Squared rational of a logarithm", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\left(\frac{\log_e x - 1}{1 + (\log_e x)^2}\right)^2dx$ equals " + CST,
  r"$\frac{x}{1 + (\log_e x)^2} + C$",
  [(r"$\tan^{-1}(\log_e x) + \frac{1}{1 + (\log_e x)^2} + C$", r"Forgets the factor $e^t$ from $dx = e^tdt$ and integrates $\frac{(t-1)^2}{(1+t^2)^2} = \frac{1}{1+t^2} - \frac{2t}{(1+t^2)^2}$ directly."),
   (r"$-\frac{2x\log_e x}{\left(1 + (\log_e x)^2\right)^2} + C$", r"Takes the derivative piece $-\frac{2t}{(1+t^2)^2}$ as $f$."),
   (r"$\frac{x\log_e x}{1 + (\log_e x)^2} + C$", r"Expands $(t-1)^2$ and takes $f = \frac{t}{1+t^2}$ from the cross term without checking $f + f'$.")],
  r"Put $x = e^t$, $dx = e^tdt$: the integral is $\int e^t\frac{(t-1)^2}{(1+t^2)^2}dt = \int e^t\left[\frac{1}{1+t^2} - \frac{2t}{(1+t^2)^2}\right]dt$. With $f = \frac{1}{1+t^2}$, $f' = -\frac{2t}{(1+t^2)^2}$, so it equals $\frac{e^t}{1+t^2} + C = \frac{x}{1 + (\log_e x)^2} + C$.",
  r"Not expanding $(t-1)^2 = (1+t^2) - 2t$ to reveal $f + f'$.",
  "U08-B-parts-logs-ln-sub", "Substitution, an algebraic rewrite, then the standard form.",
  check=lambda: ((log(x) - 1)/(1 + log(x)**2))**2,
  values=dv(x/(1 + log(x)**2), atan(log(x)) + 1/(1 + log(x)**2), -2*x*log(x)/(1 + log(x)**2)**2, x*log(x)/(1 + log(x)**2)),
  source_class="XII", cognitive="Analysis")


def _c45():
    f = Function('f')
    sol = dsolve(f(x).diff(x) + f(x) - (x**2 + 1)/(x + 1)**2, f(x)).rhs
    return simplify(sol.subs(Symbol('C1'), 0))
q("U08-B-045", TE, "Finding the rational f", "Difficult", "Inverse/parameter MCQ",
  r"If $\int e^x\frac{x^2 + 1}{(x+1)^2}\,dx = e^xf(x) + C$ for $x \ne -1$, where $f$ is a rational function and $C$ is the constant of integration, then $f(x)$ equals",
  r"$\frac{x-1}{x+1}$",
  [(r"$\frac{x}{x+1}$", r"Writes $x^2 + 1 = (x+1)^2 - (x+1) + 2$ (halving the middle term), so the bracket becomes $1 - \frac{1}{x+1} + \frac{2}{(x+1)^2}$; takes $f = 1 - \frac{1}{x+1} = \frac{x}{x+1}$ without checking that $f' = \frac{1}{(x+1)^2}$ does not match $\frac{2}{(x+1)^2}$."),
   (r"$\frac{1-x}{1+x}$", r"Sign slip when combining $1 - \frac{2}{x+1}$ into a single fraction."),
   (r"$\frac{2}{(x+1)^2}$", r"Takes the derivative piece $\frac{2}{(x+1)^2}$ as $f$.")],
  r"$\frac{x^2+1}{(x+1)^2} = \frac{(x+1)^2 - 2(x+1) + 2}{(x+1)^2} = 1 - \frac{2}{x+1} + \frac{2}{(x+1)^2}$. With $f = 1 - \frac{2}{x+1} = \frac{x-1}{x+1}$, $f' = \frac{2}{(x+1)^2}$, so the integrand is $e^x(f + f')$ and $f(x) = \frac{x-1}{x+1}$.",
  r"Not rewriting the numerator in powers of $(x+1)$.",
  "U08-B-ex-f-fprime-reverse", "Reverse problem: rewrite in powers of $x+1$ and identify $f$; rationality fixes $f$ uniquely.",
  check=_c45, values=[(x - 1)/(x + 1), x/(x + 1), (1 - x)/(1 + x), 2/(x + 1)**2],
  numerical=dict(question=r"If $\int e^x\frac{x^2 + 1}{(x+1)^2}\,dx = e^xf(x) + C$ for $x \ne -1$, where $f$ is a rational function and $C$ is the constant of integration, then the value of $5f(4)$ is", answer=3),
  source_class="XII", cognitive="Analysis")


def _c46():
    f = Function('f')
    lhs = diff(exp(sec(x))*f(x), x)
    rhs = exp(sec(x))*(sec(x)*tan(x)*f(x) + sec(x)*tan(x) + sec(x)**2)
    return solve(Eq(lhs, rhs), Derivative(f(x), x))[0]
q("U08-B-046", TE, "Generalised form e^g(fg' + f')", "Difficult", "Inverse/parameter MCQ",
  r"If $\int e^{\sec x}\left(\sec x\tan x\,f(x) + \sec x\tan x + \sec^2x\right)dx = e^{\sec x}f(x) + C$, where $C$ is the constant of integration, then a possible choice of $f(x)$ is",
  r"$\sec x + \tan x$",
  [(r"$\sec x - \tan x$", r"Believes $\frac{d}{dx}\tan x = -\sec^2x$, so thinks $(\sec x - \tan x)' = \sec x\tan x + \sec^2x$."),
   (r"$\tan x$", r"Matches only the $\sec^2x$ term as $f'$, ignoring $\sec x\tan x$."),
   (r"$\sec x\tan x + \sec^2x$", r"Takes the added expression itself as $f$ rather than as $f'$.")],
  r"$\frac{d}{dx}\left[e^{\sec x}f(x)\right] = e^{\sec x}\left(\sec x\tan x\,f(x) + f'(x)\right)$. Comparing with the integrand, $f'(x) = \sec x\tan x + \sec^2x$, so $f(x) = \sec x + \tan x$ (up to an additive constant), which is the listed choice.",
  r"Not recognising $\frac{d}{dx}[e^{g}f] = e^{g}(fg' + f')$.",
  "U08-B-ex-f-fprime-composite", "Needs the generalised product form and a reverse identification.",
  check=_c46, values=dv(sec(x) + tan(x), sec(x) - tan(x), tan(x), sec(x)*tan(x) + sec(x)**2),
  source_class="XII", cognitive="Analysis")

q("U08-B-047", TP, "Clever split for a squared denominator", "Difficult", "Multi-step computation MCQ",
  r"$\int\frac{x^2}{(x\sin x + \cos x)^2}\,dx$ equals " + CST,
  r"$\frac{\sin x - x\cos x}{x\sin x + \cos x} + C$",
  [(r"$\frac{x\cos x - \sin x}{x\sin x + \cos x} + C$", r"Takes $v = +\frac{1}{x\sin x + \cos x}$ for $\int\frac{x\cos x}{(x\sin x + \cos x)^2}dx$."),
   (r"$\frac{\sin x + x\cos x}{x\sin x + \cos x} + C$", r"Combines $\tan x - \frac{x\sec x}{x\sin x + \cos x}$ using $\sin^2x = 1 + \cos^2x$."),
   (r"$-\frac{x\sec x}{x\sin x + \cos x} + C$", r"Stops at $uv$ and drops the $-\int v\,du$ term, which contributes $\tan x$.")],
  r"Since $\frac{d}{dx}(x\sin x + \cos x) = x\cos x$, write the integrand as $x\sec x\cdot\frac{x\cos x}{(x\sin x + \cos x)^2}$ and take $u = x\sec x$, $v = -\frac{1}{x\sin x + \cos x}$. Then $I = -\frac{x\sec x}{x\sin x + \cos x} + \int\sec^2x\,dx = \tan x - \frac{x\sec x}{x\sin x + \cos x}$. Over a common denominator the numerator is $x\sin^2x + \sin x\cos x - x = \cos x(\sin x - x\cos x)$, giving $\frac{\sin x - x\cos x}{x\sin x + \cos x} + C$.",
  r"Not spotting that $x\cos x$ is the derivative of the denominator's base.",
  "U08-B-parts-quotient-trick", "Non-obvious choice of $u$ and $dv$, then simplification.",
  check=lambda: x**2/(x*sin(x) + cos(x))**2,
  values=dv((sin(x) - x*cos(x))/(x*sin(x) + cos(x)), (x*cos(x) - sin(x))/(x*sin(x) + cos(x)),
            (sin(x) + x*cos(x))/(x*sin(x) + cos(x)), -x*sec(x)/(x*sin(x) + cos(x))),
  source_class="XII", cognitive="Analysis")

q("U08-B-048", TP, "Half-angle split with cancelling terms", "Difficult", "Multi-step computation MCQ",
  r"For $\cos x \ne -1$, $\int\frac{x + \sin x}{1 + \cos x}\,dx$ equals " + CST,
  r"$x\tan\frac{x}{2} + C$",
  [(r"$x\tan\frac{x}{2} + 2\log_e\left|\cos\frac{x}{2}\right| + C$", r"Integrates the piece $\frac x2\sec^2\frac x2$ by parts but forgets to add $\int\tan\frac x2\,dx$ from the second piece."),
   (r"$x\tan\frac{x}{2} - 4\log_e\left|\cos\frac{x}{2}\right| + C$", r"Sign slip in $-\int v\,du$ for the first piece, so the two logarithms add rather than cancel."),
   (r"$2x\tan\frac{x}{2} + C$", r"Uses $1 + \cos x = \cos^2\frac x2$ (missing the 2), which doubles the integrand's split.")],
  r"$1 + \cos x = 2\cos^2\frac x2$, so the integrand is $\frac x2\sec^2\frac x2 + \tan\frac x2$. By parts, $\int\frac x2\sec^2\frac x2\,dx = x\tan\frac x2 - \int\tan\frac x2\,dx$, and the leftover cancels the second piece. Hence the integral is $x\tan\frac x2 + C$.",
  r"Not seeing that the two pieces form $\frac{d}{dx}\left(x\tan\frac x2\right)$.",
  "U08-B-parts-quotient-trick", "Identity, split, by parts, and a cancellation.",
  check=lambda: (x + sin(x))/(1 + cos(x)),
  values=dv(x*tan(x/2), x*tan(x/2) + 2*log(cos(x/2)), x*tan(x/2) - 4*log(cos(x/2)), 2*x*tan(x/2)),
  source_class="XII")

q("U08-B-049", TF_, "Trigonometric integrand reduced to three linear factors", "Difficult", "Inverse/parameter MCQ",
  r"If $\int\frac{dx}{\sin x - \sin 2x} = a\log_e|1 - \cos x| + b\log_e|1 + \cos x| + c\log_e|1 - 2\cos x| + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then the ordered triple $(a, b, c)$ is",
  r"$\left(-\frac{1}{2}, -\frac{1}{6}, \frac{2}{3}\right)$",
  [(r"$\left(\frac{1}{2}, \frac{1}{6}, -\frac{2}{3}\right)$", r"Forgets the minus sign in $dt = -\sin x\,dx$ for $t = \cos x$."),
   (r"$\left(-\frac{1}{2}, -\frac{1}{6}, \frac{4}{3}\right)$", r"Integrates $\frac{1}{1-2t}$ as $-\log_e|1-2t|$, missing the factor $\frac12$."),
   (r"$\left(\frac{1}{2}, -\frac{1}{6}, \frac{2}{3}\right)$", r"Integrates $\frac{1}{1-t}$ as $+\log_e|1-t|$ (sign slip).")],
  r"$\sin x - \sin 2x = \sin x(1 - 2\cos x)$. Multiply by $\frac{\sin x}{\sin x}$ and put $t = \cos x$: $\int\frac{dx}{\sin x - \sin 2x} = -\int\frac{dt}{(1-t)(1+t)(1-2t)}$. Partial fractions: $\frac{1}{(1-t)(1+t)(1-2t)} = -\frac{1}{2(1-t)} + \frac{1}{6(1+t)} + \frac{4}{3(1-2t)}$. Integrating and applying the outer minus sign gives $-\frac12\log_e|1-t| - \frac16\log_e|1+t| + \frac23\log_e|1-2t|$, so $(a, b, c) = \left(-\frac12, -\frac16, \frac23\right)$.",
  r"Losing the sign of $dt = -\sin x\,dx$ or the factor $\frac12$ in $\int\frac{dt}{1-2t}$.",
  "U08-B-pf-trig-sub", "Factorisation, a substitution, a three-term decomposition and sign tracking.",
  check=lambda: fit(a_*log(1 - cos(x)) + b_*log(1 + cos(x)) + c_*log(1 - 2*cos(x)), 1/(sin(x) - sin(2*x)), [a_, b_, c_]),
  values=[(Rational(-1, 2), Rational(-1, 6), Rational(2, 3)), (Rational(1, 2), Rational(1, 6), Rational(-2, 3)),
          (Rational(-1, 2), Rational(-1, 6), Rational(4, 3)), (Rational(1, 2), Rational(-1, 6), Rational(2, 3))],
  numerical=dict(question=r"If $\int\frac{dx}{\sin x - \sin 2x} = a\log_e|1 - \cos x| + b\log_e|1 + \cos x| + c\log_e|1 - 2\cos x| + C$, where $a, b, c$ are constants and $C$ is the constant of integration, then the value of $6(c - a - b)$ is", answer=8),
  source_class="XII", cognitive="Analysis")

q("U08-B-050", TP, "Logarithm of a rational argument", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int x\log_e\left(1 + \frac{1}{x}\right)dx$ equals " + CST,
  r"$\frac{x^2}{2}\log_e\left(1 + \frac{1}{x}\right) + \frac{x}{2} - \frac{1}{2}\log_e(x+1) + C$",
  [(r"$\frac{x^2}{2}\log_e\left(1 + \frac{1}{x}\right) - \frac{x}{2} + \frac{1}{2}\log_e(x+1) + C$", r"Takes $\frac{d}{dx}\log_e\left(1 + \frac1x\right) = +\frac{1}{x(x+1)}$, losing the sign."),
   (r"$\frac{x^2}{2}\log_e\left(1 + \frac{1}{x}\right) + \frac{x}{2} + \frac{1}{2}\log_e(x+1) + C$", r"Writes $\frac{x}{x+1} = 1 + \frac{1}{x+1}$ (sign slip)."),
   (r"$\frac{x^2}{2}\log_e\left(1 + \frac{1}{x}\right) + \frac{x}{2} - \log_e(x+1) + C$", r"Drops the $\frac12$ on the logarithmic part when integrating $\frac12\cdot\frac{x}{x+1}$.")],
  r"$\frac{d}{dx}\log_e\frac{x+1}{x} = \frac{1}{x+1} - \frac1x = -\frac{1}{x(x+1)}$. With $v = \frac{x^2}{2}$: $I = \frac{x^2}{2}\log_e\left(1 + \frac1x\right) + \frac12\int\frac{x}{x+1}dx = \frac{x^2}{2}\log_e\left(1 + \frac1x\right) + \frac12\left(x - \log_e(x+1)\right) + C$.",
  r"Sign error in differentiating $\log_e\left(1 + \frac1x\right)$.",
  "U08-B-parts-then-pf", "By parts, a derivative via log rules, then a split.",
  check=lambda: x*log(1 + 1/x),
  values=dv(x**2/2*log(1 + 1/x) + x/2 - log(x + 1)/2, x**2/2*log(1 + 1/x) - x/2 + log(x + 1)/2,
            x**2/2*log(1 + 1/x) + x/2 + log(x + 1)/2, x**2/2*log(1 + 1/x) + x/2 - log(x + 1)),
  source_class="XII")

q("U08-B-051", TP, "Logarithm over a squared binomial", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\frac{\log_e x}{(1+x)^2}\,dx$ equals " + CST,
  r"$-\frac{\log_e x}{1+x} + \log_e\frac{x}{1+x} + C$",
  [(r"$-\frac{\log_e x}{1+x} + \log_e\left(x(1+x)\right) + C$", r"Writes $\frac{1}{x(1+x)} = \frac1x + \frac{1}{1+x}$."),
   (r"$\frac{\log_e x}{1+x} - \log_e\frac{x}{1+x} + C$", r"Takes $v = +\frac{1}{1+x}$ for $\int(1+x)^{-2}dx$."),
   (r"$-\frac{\log_e x}{1+x} + \log_e\frac{1+x}{x} + C$", r"Reverses the signs: $\frac{1}{x(1+x)} = \frac{1}{1+x} - \frac1x$.")],
  r"With $u = \log_e x$, $v = -\frac{1}{1+x}$: $I = -\frac{\log_e x}{1+x} + \int\frac{dx}{x(1+x)}$. Since $\frac{1}{x(1+x)} = \frac1x - \frac{1}{1+x}$, $I = -\frac{\log_e x}{1+x} + \log_e\frac{x}{1+x} + C$.",
  r"Sign errors in combining by parts with partial fractions.",
  "U08-B-parts-then-pf", "By parts produces a rational integral needing a split; several sign traps.",
  check=lambda: log(x)/(1 + x)**2,
  values=dv(-log(x)/(1 + x) + log(x/(1 + x)), -log(x)/(1 + x) + log(x*(1 + x)), log(x)/(1 + x) - log(x/(1 + x)), -log(x)/(1 + x) + log((1 + x)/x)),
  source_class="XII")

q("U08-B-052", TP, "Inverse trigonometric simplification before parts", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\sin^{-1}\sqrt{\frac{x}{1+x}}\,dx$ equals " + CST,
  r"$(x+1)\tan^{-1}\sqrt{x} - \sqrt{x} + C$",
  [(r"$(x-1)\tan^{-1}\sqrt{x} + \sqrt{x} + C$", r"Sign slip on $-\int v\,du$, adding $\sqrt x - \tan^{-1}\sqrt x$."),
   (r"$x\tan^{-1}\sqrt{x} - \frac{1}{4}\log_e(1+x) + C$", r"Forgets $dx = 2t\,dt$ when substituting $t = \sqrt x$ in $\int\frac{\sqrt x}{2(1+x)}dx$."),
   (r"$(x-1)\tan^{-1}\sqrt{x} - \sqrt{x} + C$", r"Writes $\frac{t^2}{1+t^2} = 1 + \frac{1}{1+t^2}$ (sign slip).")],
  r"For $x > 0$, if $\theta = \tan^{-1}\sqrt x$ then $\sin\theta = \sqrt{\frac{x}{1+x}}$, so the integrand is $\tan^{-1}\sqrt x$. By parts, $I = x\tan^{-1}\sqrt x - \int\frac{\sqrt x}{2(1+x)}dx$; with $t = \sqrt x$ the last integral is $\int\frac{t^2}{1+t^2}dt = t - \tan^{-1}t$. Hence $I = (x+1)\tan^{-1}\sqrt x - \sqrt x + C$.",
  r"Not simplifying the inverse sine first, or mishandling $dx = 2t\,dt$.",
  "U08-B-parts-inverse-trig-sub", "Inverse-trig simplification, by parts, then a substitution.",
  check=lambda: asin(sqrt(x/(1 + x))),
  values=dv((x + 1)*atan(sqrt(x)) - sqrt(x), (x - 1)*atan(sqrt(x)) + sqrt(x), x*atan(sqrt(x)) - log(1 + x)/4, (x - 1)*atan(sqrt(x)) - sqrt(x)),
  source_class="XII", cognitive="Analysis")

q("U08-B-053", TF_, "Substitution t = xe^x then a repeated factor", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int\frac{x+1}{x(1 + xe^x)^2}\,dx$ equals " + CST,
  r"$\log_e\left|\frac{xe^x}{1 + xe^x}\right| + \frac{1}{1 + xe^x} + C$",
  [(r"$\log_e\left|\frac{xe^x}{1 + xe^x}\right| - \frac{1}{1 + xe^x} + C$", r"Integrates $-\frac{1}{(1+t)^2}$ as $-\frac{1}{1+t}$, losing the sign from the power rule."),
   (r"$\log_e\left|\frac{1 + xe^x}{xe^x}\right| + \frac{1}{1 + xe^x} + C$", r"Reverses the signs of the two logarithmic partial fractions."),
   (r"$\log_e\left|\frac{xe^x}{1 + xe^x}\right| + C$", r"Omits the repeated-factor term $\frac{1}{(1+t)^2}$ from the decomposition.")],
  r"Multiply by $\frac{e^x}{e^x}$ and put $t = xe^x$, $dt = (x+1)e^xdx$: the integral becomes $\int\frac{dt}{t(1+t)^2}$. Partial fractions: $\frac{1}{t(1+t)^2} = \frac1t - \frac{1}{1+t} - \frac{1}{(1+t)^2}$, so the integral is $\log_e\left|\frac{t}{1+t}\right| + \frac{1}{1+t} + C$, i.e. $\log_e\left|\frac{xe^x}{1 + xe^x}\right| + \frac{1}{1 + xe^x} + C$.",
  r"Missing the repeated-factor term or its sign.",
  "U08-B-pf-product-sub", "Non-obvious substitution, then a three-term decomposition with a repeated factor.",
  check=lambda: (x + 1)/(x*(1 + x*exp(x))**2),
  values=dv(log(x*exp(x)/(1 + x*exp(x))) + 1/(1 + x*exp(x)), log(x*exp(x)/(1 + x*exp(x))) - 1/(1 + x*exp(x)),
            log((1 + x*exp(x))/(x*exp(x))) + 1/(1 + x*exp(x)), log(x*exp(x)/(1 + x*exp(x)))),
  source_class="XII", cognitive="Analysis")

q("U08-B-054", TF_, "Exponential quadratic in the denominator", "Difficult", "Inverse/parameter MCQ",
  r"If $\int\frac{dx}{e^{2x} + e^x - 2} = \alpha x + \beta\log_e|e^x - 1| + \gamma\log_e(e^x + 2) + C$, where $\alpha, \beta, \gamma$ are constants and $C$ is the constant of integration, then the ordered triple $(\alpha, \beta, \gamma)$ is",
  r"$\left(-\frac{1}{2}, \frac{1}{3}, \frac{1}{6}\right)$",
  [(r"$\left(0, \frac{1}{3}, -\frac{1}{3}\right)$", r"Puts $t = e^x$ but forgets $dx = \frac{dt}{t}$, so decomposes $\frac{1}{(t-1)(t+2)}$ only."),
   (r"$\left(\frac{1}{2}, \frac{1}{3}, \frac{1}{6}\right)$", r"Sign slip in the cover-up at $t = 0$, taking $\frac{1}{(0-1)(0+2)}$ as $+\frac12$."),
   (r"$\left(-\frac{1}{2}, \frac{1}{3}, \frac{1}{2}\right)$", r"In the cover-up at $t = -2$, evaluates $t - 1$ as $-1$, getting $\frac{1}{(-2)(-1)} = \frac12$.")],
  r"Put $t = e^x$, $dx = \frac{dt}{t}$: $\int\frac{dt}{t(t-1)(t+2)}$. Cover-up gives coefficients $-\frac12$ at $t = 0$, $\frac13$ at $t = 1$, $\frac16$ at $t = -2$. So the integral is $-\frac12\log_e t + \frac13\log_e|t-1| + \frac16\log_e(t+2) = -\frac x2 + \frac13\log_e|e^x - 1| + \frac16\log_e(e^x + 2) + C$.",
  r"Forgetting the extra factor $t$ from $dx = \frac{dt}{t}$.",
  "U08-B-pf-exp-sub", "Substitution creates a third factor; three cover-up evaluations.",
  check=lambda: fit(a_*x + b_*log(exp(x) - 1) + c_*log(exp(x) + 2), 1/(exp(2*x) + exp(x) - 2), [a_, b_, c_]),
  values=[(Rational(-1, 2), Rational(1, 3), Rational(1, 6)), (0, Rational(1, 3), Rational(-1, 3)),
          (Rational(1, 2), Rational(1, 3), Rational(1, 6)), (Rational(-1, 2), Rational(1, 3), Rational(1, 2))],
  numerical=dict(question=r"If $\int\frac{dx}{e^{2x} + e^x - 2} = \alpha x + \beta\log_e|e^x - 1| + \gamma\log_e(e^x + 2) + C$, where $\alpha, \beta, \gamma$ are constants and $C$ is the constant of integration, then the value of $6(\beta + \gamma - \alpha)$ is", answer=6),
  source_class="XII")

q("U08-B-055", TP, "Trigonometric times log of sine", "Difficult", "Multi-step computation MCQ",
  r"For $0 < x < \pi$, $\int\cos 2x\,\log_e(\sin x)\,dx$ equals " + CST,
  r"$\frac{\sin 2x}{2}\log_e(\sin x) - \frac{x}{2} - \frac{\sin 2x}{4} + C$",
  [(r"$\frac{\sin 2x}{2}\log_e(\sin x) + \frac{x}{2} + \frac{\sin 2x}{4} + C$", r"Sign slip: adds $\int v\,du$ rather than subtracting it."),
   (r"$\frac{\sin 2x}{2}\log_e(\sin x) - \frac{x}{2} + \frac{\sin 2x}{4} + C$", r"Uses $\cos^2x = \frac{1 - \cos 2x}{2}$ when integrating $\cos^2x$."),
   (r"$\sin 2x\log_e(\sin x) - x - \frac{\sin 2x}{2} + C$", r"Takes $v = \sin 2x$ (missing the $\frac12$), then $\int\sin 2x\cot x\,dx = \int 2\cos^2x\,dx$.")],
  r"With $u = \log_e(\sin x)$, $v = \frac{\sin 2x}{2}$: $\int v\,du = \int\frac{\sin 2x}{2}\cdot\frac{\cos x}{\sin x}dx = \int\cos^2x\,dx = \frac x2 + \frac{\sin 2x}{4}$. Hence the integral is $\frac{\sin 2x}{2}\log_e(\sin x) - \frac x2 - \frac{\sin 2x}{4} + C$.",
  r"Mishandling $\sin 2x\cot x = 2\cos^2x$ or the identity for $\cos^2x$.",
  "U08-B-parts-log-composite", r"By parts, a simplification $\sin 2x\cot x$, then a power-reduction identity.",
  check=lambda: cos(2*x)*log(sin(x)),
  values=dv(sin(2*x)/2*log(sin(x)) - x/2 - sin(2*x)/4, sin(2*x)/2*log(sin(x)) + x/2 + sin(2*x)/4,
            sin(2*x)/2*log(sin(x)) - x/2 + sin(2*x)/4, sin(2*x)*log(sin(x)) - x - sin(2*x)/2),
  source_class="XII")


def _c56():
    s1 = is_anti(exp(3*x)*sin(x), exp(3*x)*(3*sin(x) + cos(x)))
    ok = True
    for deg in (1, 2, 3, 4):
        cs = symbols('p0:%d' % (deg + 1))
        p = sum(cs[i]*x**i for i in range(deg + 1))
        F = exp(x)*sum((-1)**k*diff(p, x, k) for k in range(deg + 1))
        ok = ok and simplify(diff(F, x) - exp(x)*p) == 0
    return (s1, bool(ok))
q("U08-B-056", TE, "Generalisations of the e^x results", "Difficult", "Statement-based MCQ",
  r"Statement I: $\int e^{3x}(3\sin x + \cos x)\,dx = e^{3x}\sin x + C$. Statement II: For every polynomial $p(x)$ of degree $n \ge 1$, $\int e^xp(x)\,dx = e^x\left(p(x) - p'(x) + p''(x) - \cdots + (-1)^np^{(n)}(x)\right) + C$. (Here $C$ is the constant of integration.) In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Rejects both, believing the $e^x(f + f')$ idea works only for $e^x$ and only for a two-term bracket."),
   (ST_TF, r"Thinks the signs in Statement II should all be $+$, missing the alternation from repeated integration by parts."),
   (ST_FT, r"Believes the pattern $e^{kx}(kf + f')$ is not an exact derivative when $k \ne 1$.")],
  r"$\frac{d}{dx}(e^{3x}\sin x) = e^{3x}(3\sin x + \cos x)$, so Statement I is true; it is the case $k = 3$ of $\int e^{kx}(kf + f')dx = e^{kx}f + C$. For Statement II, let $F = p - p' + p'' - \cdots + (-1)^np^{(n)}$; then $F + F' = p$ because the terms telescope and $p^{(n+1)} = 0$. Hence $\frac{d}{dx}(e^xF) = e^x(F + F') = e^xp$, so Statement II is true.",
  r"Not seeing that both are instances of $\frac{d}{dx}[e^{kx}f] = e^{kx}(kf + f')$.",
  "U08-B-statements-general", "General statements need a telescoping argument, not a single computation.",
  check=_c56, values=[TT, FF, TF, FT], cognitive="Analysis", source_class="XII")
