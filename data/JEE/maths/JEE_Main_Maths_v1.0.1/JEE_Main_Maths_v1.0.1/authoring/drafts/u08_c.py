import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

x = Symbol('x')
t = Symbol('t')
A_, B_, k_, l_, m_ = symbols('A B k lambda mu')

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
CC = r"(where $C$ is the constant of integration)"
TOP = "Integrals of special forms"
XII = "XII"


def dv(*exprs):
    """Derivatives of the option antiderivatives (Abs dropped; same derivative)."""
    return [diff(e, x) for e in exprs]


def holds(F, f):
    """True if F is an antiderivative of f (checked symbolically, then at sample points)."""
    dd = simplify(diff(F, x) - f)
    if dd == 0:
        return True
    return False


def solve_coeffs(ansatz, integrand, unknowns):
    """Match d/dx(ansatz) with the integrand identically in x and solve for unknowns."""
    num = numer(together(diff(ansatz, x) - integrand))
    eqs = Poly(expand(num), x).coeffs()
    return solve(eqs, unknowns, dict=True)


# ================================================================ EASY
# ---------------------------------------------------------------- 001
q("U08-C-001", TOP, "Integral of 1/(x^2 + a^2)", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{x^2+2}$ equals " + CC,
  r"$\frac{1}{\sqrt{2}}\tan^{-1}\frac{x}{\sqrt{2}} + C$",
  [(r"$\tan^{-1}\frac{x}{\sqrt{2}} + C$", r"Omits the factor $\frac{1}{a}$ in $\int\frac{dx}{x^2+a^2}=\frac{1}{a}\tan^{-1}\frac{x}{a}$."),
   (r"$\frac{1}{2}\tan^{-1}\frac{x}{\sqrt{2}} + C$", r"Uses $\frac{1}{a^2}=\frac{1}{2}$ in front instead of $\frac{1}{a}$."),
   (r"$\frac{1}{\sqrt{2}}\tan^{-1}\frac{x}{2} + C$", r"Divides $x$ by $a^2=2$ inside the inverse tangent instead of by $a=\sqrt{2}$.")],
  r"With $a=\sqrt{2}$, $\int\frac{dx}{x^2+a^2}=\frac{1}{a}\tan^{-1}\frac{x}{a}+C=\frac{1}{\sqrt{2}}\tan^{-1}\frac{x}{\sqrt{2}}+C$.",
  r"Forgetting or squaring the factor $\frac{1}{a}$ in the standard result.",
  "U08-C-x2-plus-a2", "Direct use of one standard formula with a surd value of $a$.",
  check=lambda: 1/(x**2+2),
  values=dv(atan(x/sqrt(2))/sqrt(2), atan(x/sqrt(2)), atan(x/sqrt(2))/2, atan(x/2)/sqrt(2)),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 002
q("U08-C-002", TOP, "Integral of 1/(x^2 + a^2) with a leading coefficient", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{9x^2+4}$ equals " + CC,
  r"$\frac{1}{6}\tan^{-1}\frac{3x}{2} + C$",
  [(r"$\frac{1}{2}\tan^{-1}\frac{3x}{2} + C$", r"Substitutes $u=3x$ but drops the factor $\frac{1}{3}$ from $dx=\frac{du}{3}$, giving $\frac{1}{2}\tan^{-1}\frac{u}{2}$."),
   (r"$\frac{1}{18}\tan^{-1}\frac{3x}{2} + C$", r"Factors out 9 to get $\frac{1}{9}\int\frac{dx}{x^2+\frac{4}{9}}$ but then uses $a=2$ in $\frac{1}{a}$, giving $\frac{1}{9}\cdot\frac{1}{2}$."),
   (r"$\frac{3}{2}\tan^{-1}\frac{3x}{2} + C$", r"Writes the denominator as $9\left(x^2+\frac{4}{9}\right)$ and uses $\frac{1}{a}=\frac{3}{2}$ but forgets the factor $\frac{1}{9}$ outside.")],
  r"Put $u=3x$, $dx=\frac{du}{3}$: $\frac{1}{3}\int\frac{du}{u^2+4}=\frac{1}{3}\cdot\frac{1}{2}\tan^{-1}\frac{u}{2}+C=\frac{1}{6}\tan^{-1}\frac{3x}{2}+C$.",
  r"Losing the factor from the linear substitution $u=3x$.",
  "U08-C-x2-plus-a2", "One substitution and one standard formula.",
  check=lambda: 1/(9*x**2+4),
  values=dv(atan(3*x/2)/6, atan(3*x/2)/2, atan(3*x/2)/18, 3*atan(3*x/2)/2),
  numerical=dict(question=r"If $\int \frac{dx}{9x^2+4} = k\tan^{-1}\frac{3x}{2} + C$, where $C$ is the constant of integration, then the value of $\frac{1}{k}$ is", answer=6),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 003
q("U08-C-003", TOP, "Integral of 1/(x^2 - a^2)", "Easy", "Single-step computation MCQ",
  r"For $|x| \ne 5$, $\int \frac{dx}{x^2-25}$ equals " + CC,
  r"$\frac{1}{10}\log_e\left|\frac{x-5}{x+5}\right| + C$",
  [(r"$\frac{1}{10}\log_e\left|\frac{x+5}{x-5}\right| + C$", r"Uses the form for $\int\frac{dx}{a^2-x^2}$, which has the ratio inverted."),
   (r"$\frac{1}{5}\log_e\left|\frac{x-5}{x+5}\right| + C$", r"Uses $\frac{1}{a}$ in front instead of $\frac{1}{2a}$."),
   (r"$\frac{1}{2}\log_e\left|\frac{x-5}{x+5}\right| + C$", r"Keeps the $\frac{1}{2}$ from the partial fractions but drops the $a$ in $\frac{1}{2a}$.")],
  r"$\frac{1}{x^2-25}=\frac{1}{10}\left(\frac{1}{x-5}-\frac{1}{x+5}\right)$, so the integral is $\frac{1}{10}\log_e\left|\frac{x-5}{x+5}\right|+C$.",
  r"Mixing up the $x^2-a^2$ and $a^2-x^2$ forms.",
  "U08-C-x2-minus-a2", "One standard formula; the trap is the order of the ratio.",
  check=lambda: 1/(x**2-25),
  values=dv(log((x-5)/(x+5))/10, log((x+5)/(x-5))/10, log((x-5)/(x+5))/5, log((x-5)/(x+5))/2),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 004
q("U08-C-004", TOP, "Integral of 1/(a^2 - x^2)", "Easy", "Single-step computation MCQ",
  r"For $|x| < 4$, $\int \frac{dx}{16-x^2}$ equals " + CC,
  r"$\frac{1}{8}\log_e\left|\frac{4+x}{4-x}\right| + C$",
  [(r"$\frac{1}{8}\log_e\left|\frac{4-x}{4+x}\right| + C$", r"Uses the $x^2-a^2$ form, which inverts the ratio and so gives the negative of the integrand on differentiation."),
   (r"$\frac{1}{4}\log_e\left|\frac{4+x}{4-x}\right| + C$", r"Uses $\frac{1}{a}$ instead of $\frac{1}{2a}$."),
   (r"$\sin^{-1}\frac{x}{4} + C$", r"Treats $\frac{1}{16-x^2}$ as $\frac{1}{\sqrt{16-x^2}}$.")],
  r"$\frac{1}{16-x^2}=\frac{1}{8}\left(\frac{1}{4+x}+\frac{1}{4-x}\right)$, which integrates to $\frac{1}{8}\left(\log_e|4+x|-\log_e|4-x|\right)=\frac{1}{8}\log_e\left|\frac{4+x}{4-x}\right|+C$.",
  r"Confusing $\frac{1}{a^2-x^2}$ with $\frac{1}{\sqrt{a^2-x^2}}$, or inverting the log ratio.",
  "U08-C-a2-minus-x2", "One standard formula.",
  check=lambda: 1/(16-x**2),
  values=dv(log((4+x)/(4-x))/8, log((4-x)/(4+x))/8, log((4+x)/(4-x))/4, asin(x/4)),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 005
q("U08-C-005", TOP, "Integral of 1/sqrt(x^2 + a^2)", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{\sqrt{x^2+9}}$ equals " + CC,
  r"$\log_e\left|x+\sqrt{x^2+9}\right| + C$",
  [(r"$\frac{1}{3}\log_e\left|x+\sqrt{x^2+9}\right| + C$", r"Inserts a factor $\frac{1}{a}$ by analogy with $\int\frac{dx}{x^2+a^2}$; the log form has no such factor."),
   (r"$\frac{1}{3}\tan^{-1}\frac{x}{3} + C$", r"Ignores the square root and integrates $\frac{1}{x^2+9}$."),
   (r"$\log_e\left|x-\sqrt{x^2+9}\right| + C$", r"Sign slip inside the logarithm; this differentiates to $-\frac{1}{\sqrt{x^2+9}}$.")],
  r"$\frac{d}{dx}\log_e\left(x+\sqrt{x^2+9}\right)=\frac{1+\frac{x}{\sqrt{x^2+9}}}{x+\sqrt{x^2+9}}=\frac{1}{\sqrt{x^2+9}}$, so the integral is $\log_e\left|x+\sqrt{x^2+9}\right|+C$.",
  r"Attaching $\frac{1}{a}$ to the logarithmic standard form.",
  "U08-C-sqrt-x2-plus-a2", "Recall of one standard result.",
  check=lambda: 1/sqrt(x**2+9),
  values=dv(log(x+sqrt(x**2+9)), log(x+sqrt(x**2+9))/3, atan(x/3)/3, log(x-sqrt(x**2+9))),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 006
q("U08-C-006", TOP, "Integral of 1/sqrt(a^2 - x^2)", "Easy", "Single-step computation MCQ",
  r"For $|x| < \frac{2}{3}$, $\int \frac{dx}{\sqrt{4-9x^2}}$ equals " + CC,
  r"$\frac{1}{3}\sin^{-1}\frac{3x}{2} + C$",
  [(r"$\sin^{-1}\frac{3x}{2} + C$", r"Puts $u=3x$ but drops the factor $\frac{1}{3}$ from $dx=\frac{du}{3}$."),
   (r"$\frac{1}{2}\sin^{-1}\frac{3x}{2} + C$", r"Writes $\sqrt{4-9x^2}=3\sqrt{\left(\frac{2}{3}\right)^2-x^2}$ and inserts a factor $\frac{1}{a}=\frac{3}{2}$ by analogy with the inverse tangent formula: $\frac{1}{3}\cdot\frac{3}{2}=\frac{1}{2}$."),
   (r"$\frac{1}{3}\sin^{-1}\frac{2x}{3} + C$", r"Writes the argument as $\frac{2x}{3}$, inverting the ratio $\frac{u}{a}=\frac{3x}{2}$.")],
  r"With $u=3x$, $dx=\frac{du}{3}$: $\frac{1}{3}\int\frac{du}{\sqrt{4-u^2}}=\frac{1}{3}\sin^{-1}\frac{u}{2}+C=\frac{1}{3}\sin^{-1}\frac{3x}{2}+C$.",
  r"Dropping the substitution factor or adding a spurious $\frac{1}{a}$.",
  "U08-C-sqrt-a2-minus-x2", "One substitution and one standard formula.",
  check=lambda: 1/sqrt(4-9*x**2),
  values=dv(asin(3*x/2)/3, asin(3*x/2), asin(3*x/2)/2, asin(2*x/3)/3),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 007
q("U08-C-007", TOP, "Integral of sqrt(a^2 - x^2)", "Easy", "Single-step computation MCQ",
  r"For $|x| < 4$, $\int \sqrt{16-x^2}\,dx$ equals " + CC,
  r"$\frac{x}{2}\sqrt{16-x^2} + 8\sin^{-1}\frac{x}{4} + C$",
  [(r"$\frac{x}{2}\sqrt{16-x^2} + 16\sin^{-1}\frac{x}{4} + C$", r"Uses $a^2$ instead of $\frac{a^2}{2}$ as the coefficient of the inverse sine."),
   (r"$\frac{x}{2}\sqrt{16-x^2} - 8\sin^{-1}\frac{x}{4} + C$", r"Borrows the minus sign from the $\sqrt{x^2-a^2}$ formula."),
   (r"$\frac{x}{2}\sqrt{16-x^2} + 2\sin^{-1}\frac{x}{4} + C$", r"Uses $\frac{a}{2}=2$ instead of $\frac{a^2}{2}=8$.")],
  r"$\int\sqrt{a^2-x^2}\,dx=\frac{x}{2}\sqrt{a^2-x^2}+\frac{a^2}{2}\sin^{-1}\frac{x}{a}+C$; with $a=4$ this is $\frac{x}{2}\sqrt{16-x^2}+8\sin^{-1}\frac{x}{4}+C$.",
  r"Misremembering the coefficient $\frac{a^2}{2}$ or its sign.",
  "U08-C-sqrt-a2-x2-integrand", "Direct recall of one standard formula.",
  check=lambda: sqrt(16-x**2),
  values=dv(x/2*sqrt(16-x**2)+8*asin(x/4), x/2*sqrt(16-x**2)+16*asin(x/4),
            x/2*sqrt(16-x**2)-8*asin(x/4), x/2*sqrt(16-x**2)+2*asin(x/4)),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 008
q("U08-C-008", TOP, "Integral of sqrt(x^2 + a^2)", "Easy", "Single-step computation MCQ",
  r"$\int \sqrt{x^2+4}\,dx$ equals " + CC,
  r"$\frac{x}{2}\sqrt{x^2+4} + 2\log_e\left|x+\sqrt{x^2+4}\right| + C$",
  [(r"$\frac{x}{2}\sqrt{x^2+4} - 2\log_e\left|x+\sqrt{x^2+4}\right| + C$", r"Uses the minus sign that belongs to the $\sqrt{x^2-a^2}$ formula."),
   (r"$\frac{x}{2}\sqrt{x^2+4} + 4\log_e\left|x+\sqrt{x^2+4}\right| + C$", r"Uses $a^2$ instead of $\frac{a^2}{2}$ as the log coefficient."),
   (r"$x\sqrt{x^2+4} + 2\log_e\left|x+\sqrt{x^2+4}\right| + C$", r"Forgets the factor $\frac{1}{2}$ on the algebraic term.")],
  r"$\int\sqrt{x^2+a^2}\,dx=\frac{x}{2}\sqrt{x^2+a^2}+\frac{a^2}{2}\log_e\left|x+\sqrt{x^2+a^2}\right|+C$; with $a=2$ the log coefficient is $\frac{4}{2}=2$.",
  r"Mixing the signs of the $\sqrt{x^2+a^2}$ and $\sqrt{x^2-a^2}$ formulas.",
  "U08-C-sqrt-x2-plus-a2-integrand", "Direct recall of one standard formula.",
  check=lambda: sqrt(x**2+4),
  values=dv(x/2*sqrt(x**2+4)+2*log(x+sqrt(x**2+4)), x/2*sqrt(x**2+4)-2*log(x+sqrt(x**2+4)),
            x/2*sqrt(x**2+4)+4*log(x+sqrt(x**2+4)), x*sqrt(x**2+4)+2*log(x+sqrt(x**2+4))),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 009
q("U08-C-009", TOP, "Integral of sqrt(x^2 - a^2)", "Easy", "Single-step computation MCQ",
  r"For $x > 3$, $\int \sqrt{x^2-9}\,dx$ equals " + CC,
  r"$\frac{x}{2}\sqrt{x^2-9} - \frac{9}{2}\log_e\left|x+\sqrt{x^2-9}\right| + C$",
  [(r"$\frac{x}{2}\sqrt{x^2-9} + \frac{9}{2}\log_e\left|x+\sqrt{x^2-9}\right| + C$", r"Uses the plus sign of the $\sqrt{x^2+a^2}$ formula."),
   (r"$\frac{x}{2}\sqrt{x^2-9} - 9\log_e\left|x+\sqrt{x^2-9}\right| + C$", r"Uses $a^2$ instead of $\frac{a^2}{2}$."),
   (r"$\frac{x}{2}\sqrt{x^2-9} - \frac{3}{2}\log_e\left|x+\sqrt{x^2-9}\right| + C$", r"Uses $\frac{a}{2}$ instead of $\frac{a^2}{2}$.")],
  r"$\int\sqrt{x^2-a^2}\,dx=\frac{x}{2}\sqrt{x^2-a^2}-\frac{a^2}{2}\log_e\left|x+\sqrt{x^2-a^2}\right|+C$; with $a=3$ the log coefficient is $-\frac{9}{2}$.",
  r"Getting the sign of the logarithmic term wrong.",
  "U08-C-sqrt-x2-minus-a2-integrand", "Direct recall of one standard formula.",
  check=lambda: sqrt(x**2-9),
  values=dv(x/2*sqrt(x**2-9)-Rational(9,2)*log(x+sqrt(x**2-9)), x/2*sqrt(x**2-9)+Rational(9,2)*log(x+sqrt(x**2-9)),
            x/2*sqrt(x**2-9)-9*log(x+sqrt(x**2-9)), x/2*sqrt(x**2-9)-Rational(3,2)*log(x+sqrt(x**2-9))),
  cognitive="Recall", source_class=XII)

# ---------------------------------------------------------------- 010
q("U08-C-010", TOP, "Integral of 1/(ax^2 + bx + c)", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{x^2-4x+8}$ equals " + CC,
  r"$\frac{1}{2}\tan^{-1}\frac{x-2}{2} + C$",
  [(r"$\tan^{-1}\frac{x-2}{2} + C$", r"Omits the factor $\frac{1}{a}=\frac{1}{2}$."),
   (r"$\frac{1}{2}\tan^{-1}\frac{x+2}{2} + C$", r"Completes the square as $(x+2)^2+4$, a sign slip."),
   (r"$\frac{1}{4}\tan^{-1}\frac{x-2}{2} + C$", r"Uses $\frac{1}{a^2}$ in front instead of $\frac{1}{a}$.")],
  r"$x^2-4x+8=(x-2)^2+4$, so the integral is $\frac{1}{2}\tan^{-1}\frac{x-2}{2}+C$.",
  r"Sign errors while completing the square.",
  "U08-C-quad-complete-square", "Complete the square, then one standard formula.",
  check=lambda: 1/(x**2-4*x+8),
  values=dv(atan((x-2)/2)/2, atan((x-2)/2), atan((x+2)/2)/2, atan((x-2)/2)/4),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 011
q("U08-C-011", TOP, "Integral of 1/sqrt(ax^2 + bx + c)", "Easy", "Single-step computation MCQ",
  r"For $1 < x < 5$, $\int \frac{dx}{\sqrt{6x-x^2-5}}$ equals " + CC,
  r"$\sin^{-1}\frac{x-3}{2} + C$",
  [(r"$\frac{1}{2}\sin^{-1}\frac{x-3}{2} + C$", r"Inserts a factor $\frac{1}{a}$ as in the inverse tangent formula."),
   (r"$\sin^{-1}\frac{x+3}{2} + C$", r"Completes the square as $4-(x+3)^2$, a sign slip."),
   (r"$\sin^{-1}\frac{x-3}{4} + C$", r"Divides by $a^2=4$ instead of $a=2$ inside the inverse sine.")],
  r"$6x-x^2-5=4-(x-3)^2$, so the integral is $\int\frac{dx}{\sqrt{2^2-(x-3)^2}}=\sin^{-1}\frac{x-3}{2}+C$.",
  r"Sign slip when completing the square of a quadratic with negative leading coefficient.",
  "U08-C-sqrt-quad-complete-square", "Complete the square, then one standard formula.",
  check=lambda: 1/sqrt(6*x-x**2-5),
  values=dv(asin((x-3)/2), asin((x-3)/2)/2, asin((x+3)/2), asin((x-3)/4)),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 012
q("U08-C-012", TOP, "Logarithmic substitution leading to 1/sqrt(u^2 + a^2)", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int \frac{dx}{x\sqrt{(\log_e x)^2+4}}$ equals " + CC,
  r"$\log_e\left|\log_e x+\sqrt{(\log_e x)^2+4}\right| + C$",
  [(r"$\frac{1}{2}\log_e\left|\log_e x+\sqrt{(\log_e x)^2+4}\right| + C$", r"Inserts a factor $\frac{1}{a}=\frac{1}{2}$ by analogy with $\int\frac{du}{u^2+a^2}$; the logarithmic form has no such factor."),
   (r"$\frac{1}{2}\tan^{-1}\left(\frac{\log_e x}{2}\right) + C$", r"Ignores the square root and integrates $\frac{1}{u^2+4}$ with $u=\log_e x$."),
   (r"$\log_e\left|\log_e x-\sqrt{(\log_e x)^2+4}\right| + C$", r"Sign slip inside the logarithm; this differentiates to $-\frac{1}{x\sqrt{(\log_e x)^2+4}}$.")],
  r"Put $u=\log_e x$, so $du=\frac{dx}{x}$. The integral becomes $\int\frac{du}{\sqrt{u^2+2^2}}=\log_e\left|u+\sqrt{u^2+4}\right|+C=\log_e\left|\log_e x+\sqrt{(\log_e x)^2+4}\right|+C$.",
  r"Attaching $\frac{1}{a}$ to the logarithmic standard form after a substitution.",
  "U08-C-sub-log-sqrt-standard", r"One substitution $u=\log_e x$ reduces it to a standard form.",
  check=lambda: 1/(x*sqrt(log(x)**2+4)),
  values=dv(log(log(x)+sqrt(log(x)**2+4)), log(log(x)+sqrt(log(x)**2+4))/2, atan(log(x)/2)/2, log(log(x)-sqrt(log(x)**2+4))),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 013
q("U08-C-013", TOP, "Substitution leading to 1/sqrt(u^2 - a^2)", "Easy", "Single-step computation MCQ",
  r"For $x > 0$, $\int \frac{e^x}{\sqrt{e^{2x}-1}}\,dx$ equals " + CC,
  r"$\log_e\left(e^x+\sqrt{e^{2x}-1}\right) + C$",
  [(r"$\log_e\left|e^x-\sqrt{e^{2x}-1}\right| + C$", r"Sign slip inside the logarithm; this differentiates to the negative of the integrand."),
   (r"$\frac{1}{2}\log_e\left(e^x+\sqrt{e^{2x}-1}\right) + C$", r"Inserts a spurious $\frac{1}{2}$, treating $e^{2x}$ as the substitution variable."),
   (r"$\sec^{-1}(e^x) + C$", r"Uses $\int\frac{du}{u\sqrt{u^2-1}}=\sec^{-1}u$, which needs an extra factor $u$ in the denominator.")],
  r"Put $u=e^x$, $du=e^x\,dx$: $\int\frac{du}{\sqrt{u^2-1}}=\log_e\left|u+\sqrt{u^2-1}\right|+C=\log_e\left(e^x+\sqrt{e^{2x}-1}\right)+C$.",
  r"Confusing $\int\frac{du}{\sqrt{u^2-1}}$ with $\int\frac{du}{u\sqrt{u^2-1}}$.",
  "U08-C-sub-to-standard", "One substitution reduces it to a standard form.",
  check=lambda: exp(x)/sqrt(exp(2*x)-1),
  values=dv(log(exp(x)+sqrt(exp(2*x)-1)), log(exp(x)-sqrt(exp(2*x)-1)), log(exp(x)+sqrt(exp(2*x)-1))/2, asec(exp(x))),
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 014
def _c014():
    F = l_*atan((x+3)/m_)
    sols = solve_coeffs(F, 1/(x**2+6*x+13), [l_, m_])
    s = [s for s in sols if s[m_].is_positive][0]
    return 1/s[l_] + s[m_]
q("U08-C-014", TOP, "Identifying constants in 1/(ax^2 + bx + c)", "Easy", "Inverse/parameter MCQ",
  r"If $\int \frac{dx}{x^2+6x+13} = \lambda\tan^{-1}\frac{x+3}{\mu} + C$, where $\mu > 0$ and $C$ is the constant of integration, then $\frac{1}{\lambda} + \mu$ equals",
  r"$4$",
  [(r"$3$", r"Takes $\lambda=1$ by omitting the factor $\frac{1}{a}$, so $1+2=3$."),
   (r"$6$", r"Takes $\lambda=\frac{1}{a^2}=\frac{1}{4}$, so $4+2=6$."),
   (r"$8$", r"Uses $a^2=4$ in place of $a$ throughout: $\mu=4$, $\lambda=\frac{1}{4}$, so $4+4=8$.")],
  r"$x^2+6x+13=(x+3)^2+2^2$, so the integral is $\frac{1}{2}\tan^{-1}\frac{x+3}{2}+C$. Hence $\lambda=\frac{1}{2}$, $\mu=2$ and $\frac{1}{\lambda}+\mu=2+2=4$.",
  r"Confusing $a$ with $a^2$ after completing the square.",
  "U08-C-quad-complete-square", "Complete the square and read off two constants.",
  check=_c014, values=[4, 3, 6, 8],
  numerical=dict(question=r"If $\int \frac{dx}{x^2+6x+13} = \lambda\tan^{-1}\frac{x+3}{\mu} + C$, where $\mu > 0$ and $C$ is the constant of integration, then the value of $\frac{1}{\lambda} + \mu$ is", answer=4),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 015
q("U08-C-015", TOP, "Integral of 1/sqrt(ax^2 + bx + c)", "Easy", "Single-step computation MCQ",
  r"$\int \frac{dx}{\sqrt{x^2-4x+13}}$ equals " + CC,
  r"$\log_e\left|x-2+\sqrt{x^2-4x+13}\right| + C$",
  [(r"$\log_e\left|x+2+\sqrt{x^2-4x+13}\right| + C$", r"Completes the square as $(x+2)^2+9$, a sign slip."),
   (r"$\frac{1}{3}\log_e\left|x-2+\sqrt{x^2-4x+13}\right| + C$", r"Inserts a factor $\frac{1}{a}$ with $a=3$ as in the inverse tangent formula."),
   (r"$\frac{1}{3}\tan^{-1}\frac{x-2}{3} + C$", r"Ignores the square root and integrates $\frac{1}{(x-2)^2+9}$.")],
  r"$x^2-4x+13=(x-2)^2+9$, so with $u=x-2$ the integral is $\log_e\left|u+\sqrt{u^2+9}\right|+C=\log_e\left|x-2+\sqrt{x^2-4x+13}\right|+C$.",
  r"Attaching $\frac{1}{a}$ to the logarithmic form.",
  "U08-C-sqrt-quad-complete-square", "Complete the square, then one standard formula.",
  check=lambda: 1/sqrt(x**2-4*x+13),
  values=dv(log(x-2+sqrt(x**2-4*x+13)), log(x+2+sqrt(x**2-4*x+13)), log(x-2+sqrt(x**2-4*x+13))/3, atan((x-2)/3)/3),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 016
q("U08-C-016", TOP, "Standard forms: true or false", "Easy", "Statement-based MCQ",
  r"Consider the following statements, where $C$ is the constant of integration. Statement I: $\int \frac{dx}{x^2+9} = \frac{1}{3}\tan^{-1}\frac{x}{3} + C$. Statement II: For $|x| < 3$, $\int \frac{dx}{9-x^2} = \frac{1}{6}\log_e\left|\frac{x-3}{x+3}\right| + C$. In the light of the above statements, choose the correct answer.",
  ST_TF,
  [(ST_TT, r"Accepts Statement II without checking the order of the ratio; the given expression differentiates to $\frac{1}{x^2-9}$."),
   (ST_FF, r"Wrongly expects $\frac{1}{9}$ in Statement I and also rejects Statement II."),
   (ST_FT, r"Wrongly expects $\frac{1}{9}$ in Statement I and does not check the ratio in Statement II.")],
  r"Statement I is the standard result with $a=3$. In Statement II, $\frac{d}{dx}\frac{1}{6}\log_e\left|\frac{x-3}{x+3}\right|=\frac{1}{6}\left(\frac{1}{x-3}-\frac{1}{x+3}\right)=\frac{1}{x^2-9}=-\frac{1}{9-x^2}$; the correct result is $\frac{1}{6}\log_e\left|\frac{3+x}{3-x}\right|+C$.",
  r"Using the $x^2-a^2$ ratio for an $a^2-x^2$ denominator.",
  "U08-C-statements-a", "Two standard results to verify by recall or one differentiation.",
  check=lambda: (holds(atan(x/3)/3, 1/(x**2+9)), holds(log((x-3)/(x+3))/6, 1/(9-x**2))),
  values=[(True, False), (True, True), (False, False), (False, True)],
  cognitive="Understanding", source_class=XII)


# ---------------------------------------------------------------- 017
def _c017():
    F = integrate(1/(x**2+3), x)
    return F.subs(x, 3) - F.subs(x, 0)
q("U08-C-017", TOP, "Function value from 1/(x^2 + a^2)", "Easy", "Single-step computation MCQ",
  r"Let $f$ be a function with $f'(x) = \frac{1}{x^2+3}$ for all real $x$ and $f(0) = 0$. Then $f(3)$ equals",
  r"$\frac{\pi}{3\sqrt{3}}$",
  [(r"$\frac{\pi}{3}$", r"Drops the factor $\frac{1}{a}=\frac{1}{\sqrt{3}}$."),
   (r"$\frac{\pi}{9}$", r"Uses $\frac{1}{a^2}=\frac{1}{3}$ in front: $\frac{1}{3}\cdot\frac{\pi}{3}$."),
   (r"$\frac{\pi}{4\sqrt{3}}$", r"Uses $\tan^{-1}\frac{x}{a^2}$, so $\tan^{-1}1=\frac{\pi}{4}$, times $\frac{1}{\sqrt{3}}$.")],
  r"$f(x)=\frac{1}{\sqrt{3}}\tan^{-1}\frac{x}{\sqrt{3}}+C$ and $f(0)=0$ gives $C=0$. Then $f(3)=\frac{1}{\sqrt{3}}\tan^{-1}\sqrt{3}=\frac{1}{\sqrt{3}}\cdot\frac{\pi}{3}=\frac{\pi}{3\sqrt{3}}$.",
  r"Mishandling $a=\sqrt{3}$ in the inverse tangent formula.",
  "U08-C-fvalue-atan", "One standard integral and one evaluation.",
  check=_c017, values=[pi/(3*sqrt(3)), pi/3, pi/9, pi/(4*sqrt(3))],
  cognitive="Application", source_class=XII)


# ================================================================ MEDIUM
# ---------------------------------------------------------------- 018
q("U08-C-018", TOP, "Integral of (px + q)/(ax^2 + bx + c)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{2x+3}{x^2+4x+8}\,dx$ equals " + CC,
  r"$\log_e(x^2+4x+8) - \frac{1}{2}\tan^{-1}\frac{x+2}{2} + C$",
  [(r"$\log_e(x^2+4x+8) + \frac{1}{2}\tan^{-1}\frac{x+2}{2} + C$", r"Writes $2x+3=(2x+4)+1$, a sign slip in the remainder."),
   (r"$\log_e(x^2+4x+8) - \tan^{-1}\frac{x+2}{2} + C$", r"Omits the factor $\frac{1}{a}=\frac{1}{2}$ on the inverse tangent."),
   (r"$\log_e(x^2+4x+8) - \frac{1}{2}\tan^{-1}\frac{x-2}{2} + C$", r"Completes the square as $(x-2)^2+4$.")],
  r"Write $2x+3=(2x+4)-1$. Then $\int\frac{2x+4}{x^2+4x+8}dx=\log_e(x^2+4x+8)$ and $\int\frac{dx}{(x+2)^2+4}=\frac{1}{2}\tan^{-1}\frac{x+2}{2}$, so the result is $\log_e(x^2+4x+8)-\frac{1}{2}\tan^{-1}\frac{x+2}{2}+C$.",
  r"Sign of the remainder after splitting the numerator as a multiple of the derivative of the denominator.",
  "U08-C-linear-over-quad", "Split the numerator, then two standard integrals.",
  check=lambda: (2*x+3)/(x**2+4*x+8),
  values=dv(log(x**2+4*x+8)-atan((x+2)/2)/2, log(x**2+4*x+8)+atan((x+2)/2)/2,
            log(x**2+4*x+8)-atan((x+2)/2), log(x**2+4*x+8)-atan((x-2)/2)/2),
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 019
def _c019():
    s = solve_coeffs(A_*log(x**2+2*x+2) + B_*atan(x+1), (3*x+1)/(x**2+2*x+2), [A_, B_])[0]
    return 2*s[A_] - s[B_]
q("U08-C-019", TOP, "Constants in (px + q)/(ax^2 + bx + c)", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{3x+1}{x^2+2x+2}\,dx = A\log_e(x^2+2x+2) + B\tan^{-1}(x+1) + C$, where $C$ is the constant of integration, then $2A - B$ equals",
  r"$5$",
  [(r"$1$", r"Gets $B=+2$ by computing the remainder as $3-1$ instead of $1-3$."),
   (r"$11$", r"Takes $A=3$, the coefficient of $x$, without dividing by the 2 in $2x+2$: $3x+1=3(2x+2)-5$, so $A=3$, $B=-5$ and $2A-B=11$."),
   (r"$\frac{7}{2}$", r"Computes the remainder as $1-A=1-\frac{3}{2}=-\frac{1}{2}$, forgetting that $A(2x+2)$ contributes $2A$.")],
  r"Write $3x+1=\frac{3}{2}(2x+2)-2$. Then the integral is $\frac{3}{2}\log_e(x^2+2x+2)-2\int\frac{dx}{(x+1)^2+1}=\frac{3}{2}\log_e(x^2+2x+2)-2\tan^{-1}(x+1)+C$. So $A=\frac{3}{2}$, $B=-2$ and $2A-B=3+2=5$.",
  r"Computing the constant remainder incorrectly when splitting the numerator.",
  "U08-C-param-linear-quad", "Split the numerator, two standard forms, then compare constants.",
  check=_c019, values=[5, 1, 11, Rational(7,2)],
  numerical=dict(question=r"If $\int \frac{3x+1}{x^2+2x+2}\,dx = A\log_e(x^2+2x+2) + B\tan^{-1}(x+1) + C$, where $C$ is the constant of integration, then the value of $2A - B$ is", answer=5),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 020
q("U08-C-020", TOP, "Integral of (px + q)/sqrt(ax^2 + bx + c)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{x+2}{\sqrt{x^2+2x+3}}\,dx$ equals " + CC,
  r"$\sqrt{x^2+2x+3} + \log_e\left|x+1+\sqrt{x^2+2x+3}\right| + C$",
  [(r"$\frac{1}{2}\sqrt{x^2+2x+3} + \log_e\left|x+1+\sqrt{x^2+2x+3}\right| + C$", r"Uses $\int\frac{u'}{\sqrt{u}}dx=\sqrt{u}$ instead of $2\sqrt{u}$, then multiplies by $\frac{1}{2}$."),
   (r"$\sqrt{x^2+2x+3} + 2\log_e\left|x+1+\sqrt{x^2+2x+3}\right| + C$", r"Writes $x+2=\frac{1}{2}(2x+2)+2$, not subtracting the 1 already produced by $\frac{1}{2}(2x+2)$."),
   (r"$\sqrt{x^2+2x+3} - \log_e\left|x+1+\sqrt{x^2+2x+3}\right| + C$", r"Sign slip in the remainder, taking $x+2=\frac{1}{2}(2x+2)-1$.")],
  r"Write $x+2=\frac{1}{2}(2x+2)+1$. Then $\frac{1}{2}\int\frac{(2x+2)dx}{\sqrt{x^2+2x+3}}=\sqrt{x^2+2x+3}$ and $\int\frac{dx}{\sqrt{(x+1)^2+2}}=\log_e\left|x+1+\sqrt{x^2+2x+3}\right|$, so the sum plus $C$ is the answer.",
  r"Mishandling $\int\frac{u'}{\sqrt{u}}dx=2\sqrt{u}$.",
  "U08-C-linear-over-sqrt-quad", "Split numerator; two different standard integrals.",
  check=lambda: (x+2)/sqrt(x**2+2*x+3),
  values=dv(sqrt(x**2+2*x+3)+log(x+1+sqrt(x**2+2*x+3)), sqrt(x**2+2*x+3)/2+log(x+1+sqrt(x**2+2*x+3)),
            sqrt(x**2+2*x+3)+2*log(x+1+sqrt(x**2+2*x+3)), sqrt(x**2+2*x+3)-log(x+1+sqrt(x**2+2*x+3))),
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 021
def _c021():
    Q = x**2-4*x+8
    e = diff(A_*sqrt(Q) + B_*log(x-2+sqrt(Q)), x) - (2*x-1)/sqrt(Q)
    s = solve([e.subs(x, 0), e.subs(x, 1)], [A_, B_], dict=True)[0]
    assert simplify(e.subs(s)) == 0
    return s[A_] + s[B_]
q("U08-C-021", TOP, "Constants in (px + q)/sqrt(ax^2 + bx + c)", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{2x-1}{\sqrt{x^2-4x+8}}\,dx = A\sqrt{x^2-4x+8} + B\log_e\left|x-2+\sqrt{x^2-4x+8}\right| + C$, where $C$ is the constant of integration, then $A + B$ equals",
  r"$5$",
  [(r"$4$", r"Takes $A=1$, using $\int\frac{u'}{\sqrt{u}}dx=\sqrt{u}$ instead of $2\sqrt{u}$."),
   (r"$-1$", r"Writes $2x-1=(2x-4)-3$, a sign slip giving $B=-3$."),
   (r"$\frac{7}{2}$", r"Inserts a factor $\frac{1}{a}=\frac{1}{2}$ in the log term, giving $B=\frac{3}{2}$.")],
  r"Write $2x-1=(2x-4)+3$. Then $\int\frac{2x-4}{\sqrt{x^2-4x+8}}dx=2\sqrt{x^2-4x+8}$ and $3\int\frac{dx}{\sqrt{(x-2)^2+4}}=3\log_e\left|x-2+\sqrt{x^2-4x+8}\right|$. So $A=2$, $B=3$, $A+B=5$.",
  r"Using $\sqrt{u}$ instead of $2\sqrt{u}$ for $\int\frac{u'}{\sqrt{u}}dx$.",
  "U08-C-param-linear-sqrt", "Split numerator, two standard forms, compare constants.",
  check=_c021, values=[5, 4, -1, Rational(7,2)],
  numerical=dict(question=r"If $\int \frac{2x-1}{\sqrt{x^2-4x+8}}\,dx = A\sqrt{x^2-4x+8} + B\log_e\left|x-2+\sqrt{x^2-4x+8}\right| + C$, where $C$ is the constant of integration, then the value of $A + B$ is", answer=5),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 022
q("U08-C-022", TOP, "Integral of sqrt(ax^2 + bx + c)", "Medium", "Multi-step computation MCQ",
  r"$\int \sqrt{x^2+2x+5}\,dx$ equals " + CC,
  r"$\frac{x+1}{2}\sqrt{x^2+2x+5} + 2\log_e\left|x+1+\sqrt{x^2+2x+5}\right| + C$",
  [(r"$\frac{x}{2}\sqrt{x^2+2x+5} + 2\log_e\left|x+1+\sqrt{x^2+2x+5}\right| + C$", r"Uses $\frac{x}{2}$ instead of $\frac{x+1}{2}$, not shifting the algebraic term."),
   (r"$\frac{x+1}{2}\sqrt{x^2+2x+5} - 2\log_e\left|x+1+\sqrt{x^2+2x+5}\right| + C$", r"Uses the minus sign of the $\sqrt{u^2-a^2}$ formula."),
   (r"$\frac{x+1}{2}\sqrt{x^2+2x+5} + 4\log_e\left|x+1+\sqrt{x^2+2x+5}\right| + C$", r"Uses $a^2=4$ instead of $\frac{a^2}{2}=2$.")],
  r"$x^2+2x+5=(x+1)^2+2^2$. With $u=x+1$, $\int\sqrt{u^2+4}\,du=\frac{u}{2}\sqrt{u^2+4}+2\log_e\left|u+\sqrt{u^2+4}\right|+C$; substituting back gives the result.",
  r"Not replacing $x$ by $x+1$ in the algebraic term after completing the square.",
  "U08-C-sqrt-quad-integrand", "Complete the square, then a two-term standard formula.",
  check=lambda: sqrt(x**2+2*x+5),
  values=dv((x+1)/2*sqrt(x**2+2*x+5)+2*log(x+1+sqrt(x**2+2*x+5)), x/2*sqrt(x**2+2*x+5)+2*log(x+1+sqrt(x**2+2*x+5)),
            (x+1)/2*sqrt(x**2+2*x+5)-2*log(x+1+sqrt(x**2+2*x+5)), (x+1)/2*sqrt(x**2+2*x+5)+4*log(x+1+sqrt(x**2+2*x+5))),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 023
q("U08-C-023", TOP, "Integral of sqrt(ax^2 + bx + c)", "Medium", "Multi-step computation MCQ",
  r"For $0 < x < 4$, $\int \sqrt{4x-x^2}\,dx$ equals " + CC,
  r"$\frac{x-2}{2}\sqrt{4x-x^2} + 2\sin^{-1}\frac{x-2}{2} + C$",
  [(r"$\frac{x-2}{2}\sqrt{4x-x^2} + 4\sin^{-1}\frac{x-2}{2} + C$", r"Uses $a^2=4$ instead of $\frac{a^2}{2}=2$."),
   (r"$\frac{x}{2}\sqrt{4x-x^2} + 2\sin^{-1}\frac{x-2}{2} + C$", r"Does not shift the algebraic term to $\frac{x-2}{2}$."),
   (r"$\frac{x-2}{2}\sqrt{4x-x^2} - 2\sin^{-1}\frac{x-2}{2} + C$", r"Uses the minus sign of the $\sqrt{u^2-a^2}$ formula.")],
  r"$4x-x^2=4-(x-2)^2$. With $u=x-2$, $\int\sqrt{4-u^2}\,du=\frac{u}{2}\sqrt{4-u^2}+2\sin^{-1}\frac{u}{2}+C$, which gives the result.",
  r"Forgetting to shift $x$ in the algebraic term after completing the square.",
  "U08-C-sqrt-quad-integrand", "Complete the square of a negative-leading quadratic, then a two-term formula.",
  check=lambda: sqrt(4*x-x**2),
  values=dv((x-2)/2*sqrt(4*x-x**2)+2*asin((x-2)/2), (x-2)/2*sqrt(4*x-x**2)+4*asin((x-2)/2),
            x/2*sqrt(4*x-x**2)+2*asin((x-2)/2), (x-2)/2*sqrt(4*x-x**2)-2*asin((x-2)/2)),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 024
q("U08-C-024", TOP, "Integral of 1/(ax^2 + bx + c) with a not 1", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{dx}{2x^2+x+1}$ equals " + CC,
  r"$\frac{2}{\sqrt{7}}\tan^{-1}\frac{4x+1}{\sqrt{7}} + C$",
  [(r"$\frac{4}{\sqrt{7}}\tan^{-1}\frac{4x+1}{\sqrt{7}} + C$", r"Factors out 2 from the denominator but forgets the $\frac{1}{2}$ outside the integral."),
   (r"$\frac{8}{7}\tan^{-1}\frac{4x+1}{\sqrt{7}} + C$", r"Uses $\frac{1}{a^2}=\frac{16}{7}$ instead of $\frac{1}{a}=\frac{4}{\sqrt{7}}$, then the $\frac{1}{2}$."),
   (r"$\frac{2}{\sqrt{7}}\tan^{-1}\frac{4x-1}{\sqrt{7}} + C$", r"Completes the square as $\left(x-\frac{1}{4}\right)^2$.")],
  r"$2x^2+x+1=2\left[\left(x+\frac{1}{4}\right)^2+\frac{7}{16}\right]$, so the integral is $\frac{1}{2}\cdot\frac{4}{\sqrt{7}}\tan^{-1}\frac{x+\frac{1}{4}}{\frac{\sqrt{7}}{4}}+C=\frac{2}{\sqrt{7}}\tan^{-1}\frac{4x+1}{\sqrt{7}}+C$.",
  r"Losing the factor taken out of the leading coefficient.",
  "U08-C-quad-complete-square", "Factor the leading coefficient, complete the square with fractions.",
  check=lambda: 1/(2*x**2+x+1),
  values=dv(2/sqrt(7)*atan((4*x+1)/sqrt(7)), 4/sqrt(7)*atan((4*x+1)/sqrt(7)),
            Rational(8,7)*atan((4*x+1)/sqrt(7)), 2/sqrt(7)*atan((4*x-1)/sqrt(7))),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 025
q("U08-C-025", TOP, "Integral of 1/(c + bx - x^2)", "Medium", "Multi-step computation MCQ",
  r"For $-1 < x < 3$, $\int \frac{dx}{3+2x-x^2}$ equals " + CC,
  r"$\frac{1}{4}\log_e\left|\frac{x+1}{3-x}\right| + C$",
  [(r"$\frac{1}{4}\log_e\left|\frac{3-x}{x+1}\right| + C$", r"Uses the $u^2-a^2$ ratio for an $a^2-u^2$ denominator."),
   (r"$\frac{1}{2}\log_e\left|\frac{x+1}{3-x}\right| + C$", r"Uses $\frac{1}{a}$ instead of $\frac{1}{2a}$."),
   (r"$\frac{1}{4}\log_e\left|\frac{x+3}{1-x}\right| + C$", r"Completes the square as $4-(x+1)^2$, a sign slip.")],
  r"$3+2x-x^2=4-(x-1)^2$. So the integral is $\frac{1}{2\cdot 2}\log_e\left|\frac{2+(x-1)}{2-(x-1)}\right|+C=\frac{1}{4}\log_e\left|\frac{x+1}{3-x}\right|+C$.",
  r"Sign slip in completing the square of a negative-leading quadratic.",
  "U08-C-a2-minus-quad", "Complete the square, then the $a^2-u^2$ formula.",
  check=lambda: 1/(3+2*x-x**2),
  values=dv(log((x+1)/(3-x))/4, log((3-x)/(x+1))/4, log((x+1)/(3-x))/2, log((x+3)/(1-x))/4),
  numerical=dict(question=r"If $\int \frac{dx}{3+2x-x^2} = k\log_e\left|\frac{x+1}{3-x}\right| + C$ for $-1 < x < 3$, where $C$ is the constant of integration, then the value of $\frac{1}{k}$ is", answer=4),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 026
q("U08-C-026", TOP, "Integral of 1/sqrt((x - a)(x - b))", "Medium", "Multi-step computation MCQ",
  r"For $x > 3$, $\int \frac{dx}{\sqrt{(x-1)(x-3)}}$ equals " + CC,
  r"$\log_e\left|x-2+\sqrt{x^2-4x+3}\right| + C$",
  [(r"$\log_e\left|x+2+\sqrt{x^2-4x+3}\right| + C$", r"Completes the square as $(x+2)^2-1$, a sign slip."),
   (r"$\log_e\left|x-1+\sqrt{x^2-4x+3}\right| + C$", r"Shifts by the smaller root: treats $x^2-4x+3$ as $(x-1)^2-a^2$ with $u=x-1$ and writes $\log_e\left|u+\sqrt{x^2-4x+3}\right|$, although in fact $x^2-4x+3=(x-1)^2-2(x-1)$ is not of that form."),
   (r"$\frac{1}{2}\log_e\left|\frac{x-3}{x-1}\right| + C$", r"Ignores the square root and integrates $\frac{1}{(x-1)(x-3)}$.")],
  r"$(x-1)(x-3)=x^2-4x+3=(x-2)^2-1$. Hence the integral is $\log_e\left|(x-2)+\sqrt{(x-2)^2-1}\right|+C=\log_e\left|x-2+\sqrt{x^2-4x+3}\right|+C$.",
  r"Treating the root of a product as a rational function.",
  "U08-C-sqrt-product-form", r"Expand, complete the square, apply the $\sqrt{u^2-a^2}$ form.",
  check=lambda: 1/sqrt((x-1)*(x-3)),
  values=dv(log(x-2+sqrt(x**2-4*x+3)), log(x+2+sqrt(x**2-4*x+3)), log(x-1+sqrt(x**2-4*x+3)), log((x-3)/(x-1))/2),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 027
def _c027():
    F = k_*asin(sqrt((x-2)/m_))
    r = simplify(diff(F, x)**2*(x-2)*(8-x))
    sols = solve(Poly(numer(together(r-1)), x).coeffs(), [k_, m_], dict=True)
    s = [s for s in sols if s[k_].is_positive and s[m_].is_positive][0]
    return s[k_] + s[m_]
q("U08-C-027", TOP, "Integral of 1/sqrt((x - a)(b - x)) in an inverse sine of a root", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{dx}{\sqrt{(x-2)(8-x)}} = k\sin^{-1}\sqrt{\frac{x-2}{m}} + C$ for $2 < x < 8$, where $k > 0$, $m > 0$ and $C$ is the constant of integration, then $k + m$ equals",
  r"$8$",
  [(r"$7$", r"Gets $m=6$ but drops the factor $\frac{1}{2}$ in $\frac{d}{dx}\sqrt{v}=\frac{v'}{2\sqrt{v}}$ when differentiating, so takes $k=1$."),
   (r"$5$", r"Takes $m=3$, the radius in $9-(x-5)^2$, instead of the gap $8-2=6$ between the roots; with $k=2$ this gives $5$."),
   (r"$10$", r"Takes $m=8$, the larger root, instead of the gap $8-2=6$; with $k=2$ this gives $10$.")],
  r"Differentiate the right side: $\frac{d}{dx}\left[k\sin^{-1}\sqrt{\frac{x-2}{m}}\right]=k\cdot\frac{1}{\sqrt{1-\frac{x-2}{m}}}\cdot\frac{1}{2\sqrt{m}\sqrt{x-2}}=\frac{k}{2\sqrt{(x-2)(m+2-x)}}$. This equals $\frac{1}{\sqrt{(x-2)(8-x)}}$ for all $x$ in $(2,8)$ only when $m+2=8$ and $k=2$. (Equivalently, $x=2+6\sin^2\theta$ turns the integral into $\int 2\,d\theta$.) Hence $k+m=2+6=8$.",
  r"Confusing the gap between the roots with the radius of the completed square, or losing the chain-rule factor of the square root.",
  "U08-C-sqrt-product-root-form", "Differentiate a composite answer form and match two constants; the alternative form hides the usual completed square.",
  check=_c027, values=[8, 7, 5, 10],
  numerical=dict(question=r"If $\int \frac{dx}{\sqrt{(x-2)(8-x)}} = k\sin^{-1}\sqrt{\frac{x-2}{m}} + C$ for $2 < x < 8$, where $k > 0$, $m > 0$ and $C$ is the constant of integration, then the value of $k + m$ is", answer=8),
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 028
q("U08-C-028", TOP, "Trigonometric substitution into 1/(u^2 + a^2)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{\cos x}{\sin^2 x + 4\sin x + 5}\,dx$ equals " + CC,
  r"$\tan^{-1}(\sin x + 2) + C$",
  [(r"$\tan^{-1}(\sin x - 2) + C$", r"Completes the square as $(\sin x-2)^2+1$."),
   (r"$\log_e(\sin^2 x + 4\sin x + 5) + C$", r"Treats $\cos x$ as the derivative of the whole denominator."),
   (r"$-\tan^{-1}(\sin x + 2) + C$", r"Takes $d(\sin x)=-\cos x\,dx$, a sign slip.")],
  r"Put $u=\sin x$, $du=\cos x\,dx$: $\int\frac{du}{u^2+4u+5}=\int\frac{du}{(u+2)^2+1}=\tan^{-1}(u+2)+C=\tan^{-1}(\sin x+2)+C$.",
  r"Treating the numerator as the derivative of the denominator.",
  "U08-C-sub-trig-quadratic", "Substitution, then complete the square.",
  check=lambda: cos(x)/(sin(x)**2+4*sin(x)+5),
  values=dv(atan(sin(x)+2), atan(sin(x)-2), log(sin(x)**2+4*sin(x)+5), -atan(sin(x)+2)),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 029
q("U08-C-029", TOP, "Exponential substitution into 1/(u^2 - a^2)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{e^x}{e^{2x}-4e^x+3}\,dx$ equals " + CC,
  r"$\frac{1}{2}\log_e\left|\frac{e^x-3}{e^x-1}\right| + C$",
  [(r"$\frac{1}{2}\log_e\left|\frac{e^x-1}{e^x-3}\right| + C$", r"Inverts the ratio in the $u^2-a^2$ formula."),
   (r"$\log_e\left|\frac{e^x-3}{e^x-1}\right| + C$", r"Uses $\frac{1}{a}=1$ instead of $\frac{1}{2a}=\frac{1}{2}$."),
   (r"$\frac{1}{2}\log_e\left|\frac{e^x+1}{e^x+3}\right| + C$", r"Completes the square as $(u+2)^2-1$, a sign slip.")],
  r"Put $u=e^x$: $\int\frac{du}{u^2-4u+3}=\int\frac{du}{(u-2)^2-1}=\frac{1}{2}\log_e\left|\frac{u-2-1}{u-2+1}\right|+C=\frac{1}{2}\log_e\left|\frac{e^x-3}{e^x-1}\right|+C$.",
  r"Inverting the ratio in the $\frac{1}{u^2-a^2}$ formula.",
  "U08-C-sub-exp-quadratic", "Substitution, complete the square, log form.",
  check=lambda: exp(x)/(exp(2*x)-4*exp(x)+3),
  values=dv(log((exp(x)-3)/(exp(x)-1))/2, log((exp(x)-1)/(exp(x)-3))/2, log((exp(x)-3)/(exp(x)-1)), log((exp(x)+1)/(exp(x)+3))/2),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 030
q("U08-C-030", TOP, "Root substitution into 1/(u^2 + a^2)", "Medium", "Multi-step computation MCQ",
  r"For $x > 0$, $\int \frac{dx}{\sqrt{x}\,(x+9)}$ equals " + CC,
  r"$\frac{2}{3}\tan^{-1}\frac{\sqrt{x}}{3} + C$",
  [(r"$\frac{1}{3}\tan^{-1}\frac{\sqrt{x}}{3} + C$", r"Puts $u=\sqrt{x}$ but forgets that $\frac{dx}{\sqrt{x}}=2\,du$."),
   (r"$2\tan^{-1}\frac{\sqrt{x}}{3} + C$", r"Omits the factor $\frac{1}{a}=\frac{1}{3}$."),
   (r"$\frac{2}{9}\tan^{-1}\frac{\sqrt{x}}{3} + C$", r"Uses $\frac{1}{a^2}=\frac{1}{9}$ instead of $\frac{1}{a}$.")],
  r"Let $u=\sqrt{x}$, $du=\frac{dx}{2\sqrt{x}}$. Then $\int\frac{dx}{\sqrt{x}(x+9)}=2\int\frac{du}{u^2+9}=\frac{2}{3}\tan^{-1}\frac{u}{3}+C=\frac{2}{3}\tan^{-1}\frac{\sqrt{x}}{3}+C$.",
  r"Dropping the factor 2 in $\frac{dx}{\sqrt{x}}=2\,du$.",
  "U08-C-sub-to-standard", "Root substitution then a standard form.",
  check=lambda: 1/(sqrt(x)*(x+9)),
  values=dv(Rational(2,3)*atan(sqrt(x)/3), atan(sqrt(x)/3)/3, 2*atan(sqrt(x)/3), Rational(2,9)*atan(sqrt(x)/3)),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 031
q("U08-C-031", TOP, "Power substitution into 1/(u^2 + a^2)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{x^2}{x^6+16}\,dx$ equals " + CC,
  r"$\frac{1}{12}\tan^{-1}\frac{x^3}{4} + C$",
  [(r"$\frac{1}{4}\tan^{-1}\frac{x^3}{4} + C$", r"Puts $u=x^3$ but forgets $x^2\,dx=\frac{du}{3}$."),
   (r"$\frac{1}{3}\tan^{-1}\frac{x^3}{4} + C$", r"Omits the factor $\frac{1}{a}=\frac{1}{4}$."),
   (r"$\frac{1}{48}\tan^{-1}\frac{x^3}{4} + C$", r"Uses $\frac{1}{a^2}=\frac{1}{16}$ with the $\frac{1}{3}$.")],
  r"Let $u=x^3$, $du=3x^2\,dx$. Then the integral is $\frac{1}{3}\int\frac{du}{u^2+16}=\frac{1}{3}\cdot\frac{1}{4}\tan^{-1}\frac{u}{4}+C=\frac{1}{12}\tan^{-1}\frac{x^3}{4}+C$.",
  r"Dropping one of the two constant factors.",
  "U08-C-sub-power-standard", "Substitution then a standard form; two constant factors to track.",
  check=lambda: x**2/(x**6+16),
  values=dv(atan(x**3/4)/12, atan(x**3/4)/4, atan(x**3/4)/3, atan(x**3/4)/48),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 032
q("U08-C-032", TOP, "Power substitution into 1/sqrt(u^2 - a^2)", "Medium", "Multi-step computation MCQ",
  r"For $|x| > \sqrt{3}$, $\int \frac{x}{\sqrt{x^4-9}}\,dx$ equals " + CC,
  r"$\frac{1}{2}\log_e\left|x^2+\sqrt{x^4-9}\right| + C$",
  [(r"$\log_e\left|x^2+\sqrt{x^4-9}\right| + C$", r"Puts $u=x^2$ but forgets $x\,dx=\frac{du}{2}$."),
   (r"$\frac{1}{6}\log_e\left|x^2+\sqrt{x^4-9}\right| + C$", r"Inserts a factor $\frac{1}{a}=\frac{1}{3}$ into the logarithmic form."),
   (r"$\frac{1}{2}\log_e\left|x^2-\sqrt{x^4-9}\right| + C$", r"Sign slip inside the logarithm; this differentiates to the negative of the integrand.")],
  r"Let $u=x^2$, $du=2x\,dx$. Then $\frac{1}{2}\int\frac{du}{\sqrt{u^2-9}}=\frac{1}{2}\log_e\left|u+\sqrt{u^2-9}\right|+C=\frac{1}{2}\log_e\left|x^2+\sqrt{x^4-9}\right|+C$.",
  r"Attaching $\frac{1}{a}$ to the logarithmic standard form.",
  "U08-C-sub-power-standard", "Substitution then a standard form.",
  check=lambda: x/sqrt(x**4-9),
  values=dv(log(x**2+sqrt(x**4-9))/2, log(x**2+sqrt(x**4-9)), log(x**2+sqrt(x**4-9))/6, log(x**2-sqrt(x**4-9))/2),
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 033
def _c033():
    e = diff(log((x-1)/(x+5))/6, x) - 1/(x**2+4*x+k_)
    return solve(numer(together(e)).subs(x, 0), k_)[0]
q("U08-C-033", TOP, "Recovering the quadratic from the log form", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{dx}{x^2+4x+k} = \frac{1}{6}\log_e\left|\frac{x-1}{x+5}\right| + C$, where $C$ is the constant of integration, then $k$ equals",
  r"$-5$",
  [(r"$5$", r"Takes $k$ as the product of 1 and 5 without the sign, i.e. ignores that the factors are $(x-1)(x+5)$."),
   (r"$13$", r"From $\frac{1}{2a}=\frac{1}{6}$ gets $a=3$ but writes $(x+2)^2+9$ instead of $(x+2)^2-9$."),
   (r"$1$", r"Gets $a=3$ but subtracts $a$ instead of $a^2$: $k=4-3$.")],
  r"Since $\frac{d}{dx}\frac{1}{6}\log_e\left|\frac{x-1}{x+5}\right|=\frac{1}{6}\left(\frac{1}{x-1}-\frac{1}{x+5}\right)=\frac{1}{(x-1)(x+5)}$, we need $x^2+4x+k=(x-1)(x+5)=x^2+4x-5$, so $k=-5$. Equivalently $(x+2)^2-3^2$ gives $k=4-9=-5$.",
  r"Using $+a^2$ when the log form signals $u^2-a^2$.",
  "U08-C-param-k-quadratic", "Reverse reasoning from the answer form to the integrand.",
  check=_c033, values=[-5, 5, 13, 1],
  cognitive="Analysis", source_class=XII)


# ---------------------------------------------------------------- 034
def _c034():
    F = integrate(1/(x**2+2*x+4), x)
    return simplify(F.subs(x, 2) - F.subs(x, 0))
q("U08-C-034", TOP, "Function value from 1/(ax^2 + bx + c)", "Medium", "Multi-step computation MCQ",
  r"Let $f$ be a function with $f'(x) = \frac{1}{x^2+2x+4}$ for all real $x$ and $f(0) = 0$. Then $f(2)$ equals",
  r"$\frac{\pi}{6\sqrt{3}}$",
  [(r"$\frac{\pi}{3\sqrt{3}}$", r"Takes the constant of integration as 0, i.e. ignores $f(0)=0$, and reports $\frac{1}{\sqrt{3}}\tan^{-1}\sqrt{3}$."),
   (r"$\frac{\pi}{2\sqrt{3}}$", r"Finds the constant with the wrong sign, $C=+\frac{\pi}{6\sqrt{3}}$."),
   (r"$\frac{\pi}{6}$", r"Drops the factor $\frac{1}{a}=\frac{1}{\sqrt{3}}$.")],
  r"$x^2+2x+4=(x+1)^2+3$, so $f(x)=\frac{1}{\sqrt{3}}\tan^{-1}\frac{x+1}{\sqrt{3}}+C$. $f(0)=0$ gives $C=-\frac{1}{\sqrt{3}}\cdot\frac{\pi}{6}$. Then $f(2)=\frac{1}{\sqrt{3}}\left(\frac{\pi}{3}-\frac{\pi}{6}\right)=\frac{\pi}{6\sqrt{3}}$.",
  r"Assuming the constant of integration is zero.",
  "U08-C-fvalue-atan", "Complete the square, fix the constant from $f(0)$, evaluate.",
  check=_c034, values=[pi/(6*sqrt(3)), pi/(3*sqrt(3)), pi/(2*sqrt(3)), pi/6],
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 035
def _c035():
    X = Symbol('X', negative=True)
    s = Symbol('s')
    # f(X) = f(0) + integral of f' from 0 to X, with f(0) = 0
    return limit(integrate(1/(s**2-6*s+8), (s, 0, X)), X, -oo)
q("U08-C-035", TOP, "Limiting value of a function from the 1/(x^2 - a^2) form", "Medium", "Multi-step computation MCQ",
  r"Let $f:(-\infty, 2) \to \mathbb{R}$ satisfy $f'(x) = \frac{1}{x^2-6x+8}$ and $f(0) = 0$. Then $\lim_{x \to -\infty} f(x)$ equals",
  r"$-\frac{1}{2}\log_e 2$",
  [(r"$0$", r"Takes the constant of integration as $0$, ignoring $f(0)=0$; then the logarithm of a ratio tending to $1$ gives $0$."),
   (r"$\frac{1}{2}\log_e 2$", r"Uses the inverted ratio $\frac{1}{2}\log_e\left|\frac{x-2}{x-4}\right|$, so $f(0)=0$ gives $C=\frac{1}{2}\log_e 2$, which is the limit."),
   (r"$-\log_e 2$", r"Uses $\frac{1}{a}=1$ instead of $\frac{1}{2a}=\frac{1}{2}$, so $f(x)=\log_e\left|\frac{x-4}{x-2}\right|+C$ and $C=-\log_e 2$.")],
  r"$x^2-6x+8=(x-3)^2-1$, so $f(x)=\frac{1}{2}\log_e\left|\frac{x-4}{x-2}\right|+C$. From $f(0)=\frac{1}{2}\log_e 2+C=0$, $C=-\frac{1}{2}\log_e 2$. As $x\to-\infty$, $\frac{x-4}{x-2}\to 1$, so the logarithmic term tends to $0$ and $f(x)\to-\frac{1}{2}\log_e 2$.",
  r"Ignoring the condition $f(0)=0$, or inverting the ratio in the $u^2-a^2$ form.",
  "U08-C-fvalue-log-limit", "Standard form, a constant fixed by a condition, then a limit at infinity of the log term.",
  check=_c035, values=[-log(2)/2, 0, log(2)/2, -log(2)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 036
def _c036():
    return simplify(integrate(1/sqrt(x**2+16), (x, 0, 3)))
q("U08-C-036", TOP, "Function value from 1/sqrt(x^2 + a^2)", "Medium", "Multi-step computation MCQ",
  r"Let $f$ be a function with $f'(x) = \frac{1}{\sqrt{x^2+16}}$ for all real $x$ and $f(0) = 0$. Then $f(3)$ equals",
  r"$\log_e 2$",
  [(r"$\log_e 8$", r"Takes the constant of integration as 0, giving $\log_e(3+5)$."),
   (r"$\frac{1}{4}\log_e 2$", r"Inserts a factor $\frac{1}{a}=\frac{1}{4}$ into the logarithmic form."),
   (r"$-\log_e 2$", r"Uses $\log_e\left|x-\sqrt{x^2+16}\right|$, giving $\log_e 2-\log_e 4$.")],
  r"$f(x)=\log_e\left(x+\sqrt{x^2+16}\right)+C$ and $f(0)=\log_e 4+C=0$, so $C=-\log_e 4$. Then $f(3)=\log_e(3+5)-\log_e 4=\log_e 2$.",
  r"Forgetting that $\log_e\left(x+\sqrt{x^2+a^2}\right)$ is not zero at $x=0$.",
  "U08-C-fvalue-sqrt", "Standard form, constant from a condition that is not trivially zero.",
  check=_c036, values=[log(2), log(8), log(2)/4, -log(2)],
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 037
q("U08-C-037", TOP, "Standard forms: true or false", "Medium", "Statement-based MCQ",
  r"Consider the following statements, where $C$ is the constant of integration. Statement I: For $x > 2$, $\int \frac{dx}{\sqrt{x^2-4}} = \log_e\left|x+\sqrt{x^2-4}\right| + C$. Statement II: $\int \frac{dx}{x^2+x+1} = \frac{2}{\sqrt{3}}\tan^{-1}\frac{2x+1}{\sqrt{3}} + C$. In the light of the above statements, choose the correct answer.",
  ST_TT,
  [(ST_FF, r"Expects a factor $\frac{1}{2}$ in Statement I and $\frac{1}{\sqrt{3}}$ in Statement II."),
   (ST_TF, r"Uses $a=\frac{3}{4}$ instead of $a=\frac{\sqrt{3}}{2}$ in Statement II and so rejects it."),
   (ST_FT, r"Attaches $\frac{1}{a}=\frac{1}{2}$ to the logarithmic form in Statement I.")],
  r"Statement I is the standard result $\int\frac{dx}{\sqrt{x^2-a^2}}=\log_e\left|x+\sqrt{x^2-a^2}\right|+C$. For Statement II, $x^2+x+1=\left(x+\frac{1}{2}\right)^2+\left(\frac{\sqrt{3}}{2}\right)^2$, so the integral is $\frac{2}{\sqrt{3}}\tan^{-1}\frac{x+\frac{1}{2}}{\frac{\sqrt{3}}{2}}+C=\frac{2}{\sqrt{3}}\tan^{-1}\frac{2x+1}{\sqrt{3}}+C$. Both are true.",
  r"Attaching $\frac{1}{a}$ to the log form, or mishandling fractional $a$.",
  "U08-C-statements-a", "Verify a standard form and a completed-square integral with fractions.",
  check=lambda: (holds(log(x+sqrt(x**2-4)), 1/sqrt(x**2-4)), holds(2/sqrt(3)*atan((2*x+1)/sqrt(3)), 1/(x**2+x+1))),
  values=[(True, True), (False, False), (True, False), (False, True)],
  cognitive="Understanding", source_class=XII)

# ---------------------------------------------------------------- 038
q("U08-C-038", TOP, "Standard forms: true or false", "Medium", "Statement-based MCQ",
  r"Consider the following statements, where $C$ is the constant of integration. Statement I: $\int \sqrt{x^2+1}\,dx = \frac{x}{2}\sqrt{x^2+1} - \frac{1}{2}\log_e\left|x+\sqrt{x^2+1}\right| + C$. Statement II: For $0 < x < 2$, $\int \frac{dx}{\sqrt{2x-x^2}} = \sin^{-1}(x-1) + C$. In the light of the above statements, choose the correct answer.",
  ST_FT,
  [(ST_TT, r"Accepts the minus sign in Statement I, which belongs to the $\sqrt{x^2-a^2}$ formula."),
   (ST_FF, r"Completes $2x-x^2$ as $1-(x+1)^2$ and so rejects Statement II, while also rejecting Statement I."),
   (ST_TF, r"Accepts the minus sign in Statement I and mis-completes the square in Statement II.")],
  r"The correct result is $\int\sqrt{x^2+1}\,dx=\frac{x}{2}\sqrt{x^2+1}+\frac{1}{2}\log_e\left|x+\sqrt{x^2+1}\right|+C$, so Statement I is false. Since $2x-x^2=1-(x-1)^2$, $\int\frac{dx}{\sqrt{1-(x-1)^2}}=\sin^{-1}(x-1)+C$, so Statement II is true.",
  r"Mixing the signs of the $\sqrt{x^2+a^2}$ and $\sqrt{x^2-a^2}$ formulas.",
  "U08-C-statements-b", "Two results, one needing completion of the square.",
  check=lambda: (holds(x/2*sqrt(x**2+1)-log(x+sqrt(x**2+1))/2, sqrt(x**2+1)), holds(asin(x-1), 1/sqrt(2*x-x**2))),
  values=[(False, True), (True, True), (False, False), (True, False)],
  cognitive="Understanding", source_class=XII)


# ---------------------------------------------------------------- 039
def _c039():
    e = diff(x/2*sqrt(9-4*x**2) + k_*asin(2*x/3), x) - sqrt(9-4*x**2)
    sol = solve(e.subs(x, Rational(1, 2)), k_)[0]
    assert simplify(e.subs(k_, sol)) == 0
    return sol
q("U08-C-039", TOP, "Coefficient in the integral of sqrt(a^2 - b^2 x^2)", "Medium", "Inverse/parameter MCQ",
  r"If $\int \sqrt{9-4x^2}\,dx = \frac{x}{2}\sqrt{9-4x^2} + k\sin^{-1}\frac{2x}{3} + C$ for $|x| < \frac{3}{2}$, where $C$ is the constant of integration, then $k$ equals",
  r"$\frac{9}{4}$",
  [(r"$\frac{9}{8}$", r"Writes $\sqrt{9-4x^2}=2\sqrt{\frac{9}{4}-x^2}$ and applies the formula, but forgets to multiply the inverse sine term by 2."),
   (r"$\frac{9}{2}$", r"Uses $\frac{a^2}{2}$ with $a=3$ as if the integrand were $\sqrt{9-x^2}$, ignoring the factor from $u=2x$."),
   (r"$\frac{3}{4}$", r"With $u=2x$ uses $\frac{1}{2}\cdot\frac{a}{2}$ instead of $\frac{1}{2}\cdot\frac{a^2}{2}$.")],
  r"Put $u=2x$: $\int\sqrt{9-4x^2}\,dx=\frac{1}{2}\int\sqrt{9-u^2}\,du=\frac{1}{2}\left[\frac{u}{2}\sqrt{9-u^2}+\frac{9}{2}\sin^{-1}\frac{u}{3}\right]+C=\frac{x}{2}\sqrt{9-4x^2}+\frac{9}{4}\sin^{-1}\frac{2x}{3}+C$. So $k=\frac{9}{4}$.",
  r"Dropping the substitution factor in one of the two terms.",
  "U08-C-param-sqrt-integrand", "Substitution plus a two-term formula; track the factor in each term.",
  check=_c039, values=[Rational(9,4), Rational(9,8), Rational(9,2), Rational(3,4)],
  numerical=dict(question=r"If $\int \sqrt{9-4x^2}\,dx = \frac{x}{2}\sqrt{9-4x^2} + k\sin^{-1}\frac{2x}{3} + C$ for $|x| < \frac{3}{2}$, where $C$ is the constant of integration, then the value of $4k$ is", answer=9),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 040
q("U08-C-040", TOP, "Integral of 1/sqrt(ax^2 + bx + c) with a not 1", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{dx}{\sqrt{4x^2+4x+5}}$ equals " + CC,
  r"$\frac{1}{2}\log_e\left|2x+1+\sqrt{4x^2+4x+5}\right| + C$",
  [(r"$\log_e\left|2x+1+\sqrt{4x^2+4x+5}\right| + C$", r"Puts $u=2x+1$ but forgets $dx=\frac{du}{2}$."),
   (r"$\frac{1}{4}\log_e\left|2x+1+\sqrt{4x^2+4x+5}\right| + C$", r"Also inserts a factor $\frac{1}{a}=\frac{1}{2}$ into the logarithmic form."),
   (r"$\frac{1}{2}\log_e\left|2x-1+\sqrt{4x^2+4x+5}\right| + C$", r"Completes the square as $(2x-1)^2+4$.")],
  r"$4x^2+4x+5=(2x+1)^2+4$. With $u=2x+1$, $dx=\frac{du}{2}$: $\frac{1}{2}\int\frac{du}{\sqrt{u^2+4}}=\frac{1}{2}\log_e\left|u+\sqrt{u^2+4}\right|+C$, which is the result.",
  r"Losing the factor from the linear substitution.",
  "U08-C-sqrt-quad-leading-coeff", "Complete the square with leading coefficient 4, substitution factor.",
  check=lambda: 1/sqrt(4*x**2+4*x+5),
  values=dv(log(2*x+1+sqrt(4*x**2+4*x+5))/2, log(2*x+1+sqrt(4*x**2+4*x+5)),
            log(2*x+1+sqrt(4*x**2+4*x+5))/4, log(2*x-1+sqrt(4*x**2+4*x+5))/2),
  numerical=dict(question=r"If $\int \frac{dx}{\sqrt{4x^2+4x+5}} = k\log_e\left|2x+1+\sqrt{4x^2+4x+5}\right| + C$, where $C$ is the constant of integration, then the value of $\frac{1}{k}$ is", answer=2),
  cognitive="Application", source_class=XII)

# ---------------------------------------------------------------- 041
q("U08-C-041", TOP, "Exponential substitution into 1/(u^2 + a^2)", "Medium", "Multi-step computation MCQ",
  r"$\int \frac{dx}{e^x + 4e^{-x}}$ equals " + CC,
  r"$\frac{1}{2}\tan^{-1}\frac{e^x}{2} + C$",
  [(r"$\tan^{-1}\frac{e^x}{2} + C$", r"Omits the factor $\frac{1}{a}=\frac{1}{2}$."),
   (r"$\frac{1}{4}\tan^{-1}\frac{e^x}{2} + C$", r"Uses $\frac{1}{a^2}=\frac{1}{4}$ instead of $\frac{1}{a}$."),
   (r"$\frac{1}{2}\log_e(e^{2x}+4) + C$", r"Treats $\frac{e^x}{e^{2x}+4}$ as a derivative-over-function form.")],
  r"Multiply numerator and denominator by $e^x$: $\int\frac{e^x\,dx}{e^{2x}+4}$. With $u=e^x$ this is $\int\frac{du}{u^2+4}=\frac{1}{2}\tan^{-1}\frac{u}{2}+C=\frac{1}{2}\tan^{-1}\frac{e^x}{2}+C$.",
  r"Not recognising the hidden $\frac{1}{u^2+a^2}$ form.",
  "U08-C-sub-exp-quadratic", "Rewrite, substitute, apply a standard form.",
  check=lambda: 1/(exp(x)+4*exp(-x)),
  values=dv(atan(exp(x)/2)/2, atan(exp(x)/2), atan(exp(x)/2)/4, log(exp(2*x)+4)/2),
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 042
def _c042():
    a = Symbol('a')
    s = solve_coeffs(log(x**2+2*x+5)/2 + Rational(3, 2)*atan((x+1)/2), (x+a)/(x**2+2*x+5), [a])
    return s[0][a]
q("U08-C-042", TOP, "Recovering the numerator in (px + q)/(ax^2 + bx + c)", "Medium", "Inverse/parameter MCQ",
  r"If $\int \frac{x+a}{x^2+2x+5}\,dx = \frac{1}{2}\log_e(x^2+2x+5) + \frac{3}{2}\tan^{-1}\frac{x+1}{2} + C$, where $a$ is a constant and $C$ is the constant of integration, then $a$ equals",
  r"$4$",
  [(r"$3$", r"Equates $a$ directly to the remainder 3, forgetting that $\frac{1}{2}(2x+2)$ already contributes 1."),
   (r"$2$", r"Subtracts instead of adding: $a=3-1$."),
   (r"$\frac{5}{2}$", r"Omits the factor $\frac{1}{2}$ from $\frac{1}{2}\tan^{-1}\frac{x+1}{2}$, so takes the remainder as $\frac{3}{2}$ and $a=1+\frac{3}{2}$.")],
  r"Write $x+a=\frac{1}{2}(2x+2)+(a-1)$. Then the integral is $\frac{1}{2}\log_e(x^2+2x+5)+(a-1)\cdot\frac{1}{2}\tan^{-1}\frac{x+1}{2}+C$. Comparing, $\frac{a-1}{2}=\frac{3}{2}$, so $a=4$.",
  r"Forgetting the constant already produced by $\frac{1}{2}(2x+2)$.",
  "U08-C-param-linear-quad", "Reverse the split of the numerator; compare coefficients.",
  check=_c042, values=[4, 3, 2, Rational(5,2)],
  numerical=dict(question=r"If $\int \frac{x+a}{x^2+2x+5}\,dx = \frac{1}{2}\log_e(x^2+2x+5) + \frac{3}{2}\tan^{-1}\frac{x+1}{2} + C$, where $a$ is a constant and $C$ is the constant of integration, then the value of $a$ is", answer=4),
  cognitive="Analysis", source_class=XII)


# ================================================================ DIFFICULT
# ---------------------------------------------------------------- 043
q("U08-C-043", TOP, "Integral of (px + q)/(c + bx - x^2)", "Difficult", "Multi-step computation MCQ",
  r"For $-5 < x < 1$, $\int \frac{x+1}{5-4x-x^2}\,dx$ equals " + CC,
  r"$-\frac{1}{2}\log_e|5-4x-x^2| - \frac{1}{6}\log_e\left|\frac{x+5}{1-x}\right| + C$",
  [(r"$-\frac{1}{2}\log_e|5-4x-x^2| + \frac{1}{6}\log_e\left|\frac{x+5}{1-x}\right| + C$", r"Takes the remainder as $+1$, writing $x+1=-\frac{1}{2}(-4-2x)+1$."),
   (r"$\frac{1}{2}\log_e|5-4x-x^2| - \frac{1}{6}\log_e\left|\frac{x+5}{1-x}\right| + C$", r"Takes the derivative of $5-4x-x^2$ as $4+2x$, a sign slip."),
   (r"$-\frac{1}{2}\log_e|5-4x-x^2| - \frac{1}{3}\log_e\left|\frac{x+5}{1-x}\right| + C$", r"Uses $\frac{1}{a}$ instead of $\frac{1}{2a}$ in the $a^2-u^2$ form.")],
  r"Since $\frac{d}{dx}(5-4x-x^2)=-(2x+4)$, write $x+1=-\frac{1}{2}(-4-2x)-1$. The first part gives $-\frac{1}{2}\log_e|5-4x-x^2|$. For the rest, $5-4x-x^2=9-(x+2)^2$, so $-\int\frac{dx}{9-(x+2)^2}=-\frac{1}{6}\log_e\left|\frac{3+(x+2)}{3-(x+2)}\right|=-\frac{1}{6}\log_e\left|\frac{x+5}{1-x}\right|$.",
  r"Sign errors with a negative leading coefficient in both the split and the remainder.",
  "U08-C-linear-over-neg-quad", "Negative leading coefficient creates two sign traps across a split and a log form.",
  check=lambda: (x+1)/(5-4*x-x**2),
  values=dv(-log(5-4*x-x**2)/2-log((x+5)/(1-x))/6, -log(5-4*x-x**2)/2+log((x+5)/(1-x))/6,
            log(5-4*x-x**2)/2-log((x+5)/(1-x))/6, -log(5-4*x-x**2)/2-log((x+5)/(1-x))/3),
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 044
q("U08-C-044", TOP, "Integral of (x^2 + 1)/(x^4 + 1)", "Difficult", "Multi-step computation MCQ",
  r"For $x \ne 0$, $\int \frac{x^2+1}{x^4+1}\,dx$ equals " + CC,
  r"$\frac{1}{\sqrt{2}}\tan^{-1}\frac{x^2-1}{\sqrt{2}\,x} + C$",
  [(r"$\frac{1}{\sqrt{2}}\tan^{-1}\frac{x^2+1}{\sqrt{2}\,x} + C$", r"Substitutes $u=x+\frac{1}{x}$ instead of $x-\frac{1}{x}$, whose differential does not match $\left(1+\frac{1}{x^2}\right)dx$."),
   (r"$\frac{1}{2\sqrt{2}}\log_e\left|\frac{x^2-\sqrt{2}x+1}{x^2+\sqrt{2}x+1}\right| + C$", r"Uses the $u^2-2$ result that belongs to $\int\frac{x^2-1}{x^4+1}dx$."),
   (r"$\frac{1}{2}\tan^{-1}\frac{x^2-1}{2x} + C$", r"Takes $a=2$ instead of $a=\sqrt{2}$ in $u^2+a^2$.")],
  r"Divide by $x^2$: $\int\frac{1+\frac{1}{x^2}}{x^2+\frac{1}{x^2}}dx$. With $u=x-\frac{1}{x}$, $du=\left(1+\frac{1}{x^2}\right)dx$ and $x^2+\frac{1}{x^2}=u^2+2$. So the integral is $\frac{1}{\sqrt{2}}\tan^{-1}\frac{u}{\sqrt{2}}+C=\frac{1}{\sqrt{2}}\tan^{-1}\frac{x^2-1}{\sqrt{2}x}+C$.",
  r"Choosing $x+\frac{1}{x}$ instead of $x-\frac{1}{x}$.",
  "U08-C-x4-trick", "Non-obvious division by $x^2$ and choice of substitution, then a standard form.",
  check=lambda: (x**2+1)/(x**4+1),
  values=dv(atan((x**2-1)/(sqrt(2)*x))/sqrt(2), atan((x**2+1)/(sqrt(2)*x))/sqrt(2),
            log((x**2-sqrt(2)*x+1)/(x**2+sqrt(2)*x+1))/(2*sqrt(2)), atan((x**2-1)/(2*x))/2),
  cognitive="Analysis", source_class=XII)


# ---------------------------------------------------------------- 045
def _c045():
    s = solve_coeffs(k_*log((x**2-sqrt(2)*x+1)/(x**2+sqrt(2)*x+1)), (x**2-1)/(x**4+1), [k_])
    return s[0][k_]
q("U08-C-045", TOP, "Integral of (x^2 - 1)/(x^4 + 1)", "Difficult", "Inverse/parameter MCQ",
  r"If $\int \frac{x^2-1}{x^4+1}\,dx = k\log_e\left|\frac{x^2-\sqrt{2}x+1}{x^2+\sqrt{2}x+1}\right| + C$, where $C$ is the constant of integration, then $k$ equals",
  r"$\frac{1}{2\sqrt{2}}$",
  [(r"$-\frac{1}{2\sqrt{2}}$", r"Uses the $a^2-u^2$ ratio, i.e. inverts the log, which flips the sign of $k$."),
   (r"$\frac{1}{\sqrt{2}}$", r"Uses $\frac{1}{a}$ instead of $\frac{1}{2a}$ with $a=\sqrt{2}$."),
   (r"$\frac{1}{4}$", r"Takes $a=2$ instead of $a=\sqrt{2}$ in $u^2-a^2$.")],
  r"Divide by $x^2$ and put $u=x+\frac{1}{x}$, $du=\left(1-\frac{1}{x^2}\right)dx$, $x^2+\frac{1}{x^2}=u^2-2$. Then $\int\frac{du}{u^2-2}=\frac{1}{2\sqrt{2}}\log_e\left|\frac{u-\sqrt{2}}{u+\sqrt{2}}\right|=\frac{1}{2\sqrt{2}}\log_e\left|\frac{x^2-\sqrt{2}x+1}{x^2+\sqrt{2}x+1}\right|$, so $k=\frac{1}{2\sqrt{2}}$.",
  r"Inverting the ratio in the $\frac{1}{u^2-a^2}$ formula.",
  "U08-C-x4-trick", "Non-obvious substitution, then a log form with a surd.",
  check=_c045, values=[1/(2*sqrt(2)), -1/(2*sqrt(2)), 1/sqrt(2), Rational(1,4)],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 046
q("U08-C-046", TOP, "Trigonometric integrand reduced to 1/(1 + b^2 t^2)", "Difficult", "Multi-step computation MCQ",
  r"For $|x| < \frac{\pi}{2}$, $\int \frac{dx}{1+3\sin^2 x}$ equals " + CC,
  r"$\frac{1}{2}\tan^{-1}(2\tan x) + C$",
  [(r"$\tan^{-1}(2\tan x) + C$", r"Integrates $\frac{1}{1+4t^2}$ as $\tan^{-1}(2t)$, forgetting the factor $\frac{1}{2}$ from $u=2t$."),
   (r"$\frac{1}{8}\tan^{-1}\frac{\tan x}{2} + C$", r"Factors $1+4t^2$ as $4(t^2+4)$ instead of $4\left(t^2+\frac{1}{4}\right)$."),
   (r"$\frac{1}{\sqrt{3}}\tan^{-1}(\sqrt{3}\tan x) + C$", r"After dividing by $\cos^2 x$, writes the denominator as $1+3\tan^2 x$, forgetting that $\sec^2 x=1+\tan^2 x$.")],
  r"Divide numerator and denominator by $\cos^2 x$: $\int\frac{\sec^2 x\,dx}{\sec^2 x+3\tan^2 x}=\int\frac{\sec^2 x\,dx}{1+4\tan^2 x}$. With $t=\tan x$ this is $\int\frac{dt}{1+4t^2}=\frac{1}{2}\tan^{-1}(2t)+C=\frac{1}{2}\tan^{-1}(2\tan x)+C$.",
  r"Not converting $\sec^2 x$ to $1+\tan^2 x$ in the denominator.",
  "U08-C-sub-trig-quadratic", r"Non-obvious division by $\cos^2 x$, identity, substitution, standard form.",
  check=lambda: 1/(1+3*sin(x)**2),
  values=dv(atan(2*tan(x))/2, atan(2*tan(x)), atan(tan(x)/2)/8, atan(sqrt(3)*tan(x))/sqrt(3)),
  cognitive="Analysis", source_class=XII)


# ---------------------------------------------------------------- 047
def _c047():
    # f(x) = integral of sec^2 x/(3 + tan^2 x); with t = tan x the value is the t-integral from 0 to tan(pi/3)
    return integrate(1/(3+t**2), (t, 0, tan(pi/3)))
q("U08-C-047", TOP, "Function value from a trigonometric integrand", "Difficult", "Multi-step computation MCQ",
  r"Let $f:\left(-\frac{\pi}{2}, \frac{\pi}{2}\right) \to \mathbb{R}$ satisfy $f'(x) = \frac{1}{3\cos^2 x + \sin^2 x}$ and $f(0) = 0$. Then $f\left(\frac{\pi}{3}\right)$ equals",
  r"$\frac{\pi}{4\sqrt{3}}$",
  [(r"$\frac{\pi}{4}$", r"Omits the factor $\frac{1}{a}=\frac{1}{\sqrt{3}}$."),
   (r"$\frac{\sqrt{3}\pi}{4}$", r"Multiplies by $a=\sqrt{3}$ instead of dividing."),
   (r"$\frac{\pi}{18}$", r"Uses $a^2=3$ in place of $a$: $\frac{1}{3}\tan^{-1}\frac{\tan x}{3}$, giving $\frac{1}{3}\cdot\frac{\pi}{6}$.")],
  r"Dividing by $\cos^2 x$, $f'(x)=\frac{\sec^2 x}{3+\tan^2 x}$, so $f(x)=\frac{1}{\sqrt{3}}\tan^{-1}\frac{\tan x}{\sqrt{3}}+C$ and $f(0)=0$ gives $C=0$. Then $f\left(\frac{\pi}{3}\right)=\frac{1}{\sqrt{3}}\tan^{-1}1=\frac{\pi}{4\sqrt{3}}$.",
  r"Confusing $a$ and $a^2$ after the tangent substitution.",
  "U08-C-fvalue-trig-sub", r"Rewrite in $\tan x$, substitute, standard form, then evaluate.",
  check=_c047, values=[pi/(4*sqrt(3)), pi/4, sqrt(3)*pi/4, pi/18],
  cognitive="Application", source_class=XII)


# ---------------------------------------------------------------- 048
def _c048():
    Q = 8-2*x-x**2
    e = diff(A_*sqrt(Q) + B_*asin((x+1)/3), x) - (x+3)/sqrt(Q)
    s = solve([e.subs(x, 0), e.subs(x, 1)], [A_, B_], dict=True)[0]
    assert simplify(e.subs(s)) == 0
    return (s[A_], s[B_])
q("U08-C-048", TOP, "Integral of (px + q)/sqrt(c + bx - x^2)", "Difficult", "Multi-step computation MCQ",
  r"For $-4 < x < 2$, $\int \frac{x+3}{\sqrt{8-2x-x^2}}\,dx$ equals " + CC,
  r"$-\sqrt{8-2x-x^2} + 2\sin^{-1}\frac{x+1}{3} + C$",
  [(r"$\sqrt{8-2x-x^2} + 2\sin^{-1}\frac{x+1}{3} + C$", r"Takes the derivative of $8-2x-x^2$ as $2+2x$, a sign slip, so the root term gets a plus sign."),
   (r"$-\sqrt{8-2x-x^2} + 4\sin^{-1}\frac{x+1}{3} + C$", r"Computes the remainder as $3+1$ instead of $3-1$."),
   (r"$-2\sqrt{8-2x-x^2} + 2\sin^{-1}\frac{x+1}{3} + C$", r"Forgets the factor $\frac{1}{2}$ in $x+1=-\frac{1}{2}(-2-2x)$.")],
  r"Since $\frac{d}{dx}(8-2x-x^2)=-2-2x$, write $x+3=-\frac{1}{2}(-2-2x)+2$. Then $-\frac{1}{2}\int\frac{(-2-2x)dx}{\sqrt{8-2x-x^2}}=-\sqrt{8-2x-x^2}$, and with $8-2x-x^2=9-(x+1)^2$, $2\int\frac{dx}{\sqrt{9-(x+1)^2}}=2\sin^{-1}\frac{x+1}{3}$.",
  r"Sign errors when the leading coefficient under the root is negative.",
  "U08-C-linear-over-sqrt-neg-quad", "Negative leading coefficient; split, two different standard forms.",
  check=_c048, values=[(-1, 2), (1, 2), (-1, 4), (-2, 2)],
  numerical=dict(question=r"If $\int \frac{x+3}{\sqrt{8-2x-x^2}}\,dx = A\sqrt{8-2x-x^2} + B\sin^{-1}\frac{x+1}{3} + C$ for $-4 < x < 2$, where $C$ is the constant of integration, then the value of $B - A$ is", answer=3),
  cognitive="Analysis", source_class=XII)


# ---------------------------------------------------------------- 049
def _c049():
    return integrate(sqrt(x**2-2*x+2), (x, 0, 1))
q("U08-C-049", TOP, "Function value from sqrt(ax^2 + bx + c)", "Difficult", "Multi-step computation MCQ",
  r"Let $f$ be a function with $f'(x) = \sqrt{x^2-2x+2}$ for all real $x$ and $f(0) = 0$. Then $f(1)$ equals",
  r"$\frac{1}{\sqrt{2}} + \frac{1}{2}\log_e(1+\sqrt{2})$",
  [(r"$\frac{1}{\sqrt{2}} - \frac{1}{2}\log_e(1+\sqrt{2})$", r"Uses the minus sign of the $\sqrt{u^2-a^2}$ formula for the log term."),
   (r"$\sqrt{2} + \log_e(1+\sqrt{2})$", r"Drops both factors $\frac{1}{2}$, using $u\sqrt{u^2+1}+\log_e\left|u+\sqrt{u^2+1}\right|$."),
   (r"$\frac{1}{\sqrt{2}} + \log_e(1+\sqrt{2})$", r"Uses $a^2=1$ instead of $\frac{a^2}{2}=\frac{1}{2}$ for the log coefficient.")],
  r"With $u=x-1$, $f(x)=\frac{x-1}{2}\sqrt{x^2-2x+2}+\frac{1}{2}\log_e\left|x-1+\sqrt{x^2-2x+2}\right|+C$. Then $f(1)-f(0)=0-\left[-\frac{\sqrt{2}}{2}+\frac{1}{2}\log_e(\sqrt{2}-1)\right]=\frac{1}{\sqrt{2}}+\frac{1}{2}\log_e(\sqrt{2}+1)$, using $\log_e(\sqrt{2}-1)=-\log_e(\sqrt{2}+1)$. Since $f(0)=0$, this is $f(1)$.",
  r"Mishandling the sign of the log term and the negative value $u=-1$ at $x=0$.",
  "U08-C-fvalue-sqrt-quad", "Completed square, two-term formula, evaluation at a point where $u<0$, log simplification.",
  check=_c049, values=[1/sqrt(2)+log(1+sqrt(2))/2, 1/sqrt(2)-log(1+sqrt(2))/2, sqrt(2)+log(1+sqrt(2)), 1/sqrt(2)+log(1+sqrt(2))],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 050
q("U08-C-050", TOP, "Rationalising to standard forms", "Difficult", "Multi-step computation MCQ",
  r"For $-1 < x < 1$, $\int \sqrt{\frac{1+x}{1-x}}\,dx$ equals " + CC,
  r"$\sin^{-1}x - \sqrt{1-x^2} + C$",
  [(r"$\sin^{-1}x + \sqrt{1-x^2} + C$", r"Integrates $\frac{x}{\sqrt{1-x^2}}$ as $+\sqrt{1-x^2}$, a sign slip."),
   (r"$\sin^{-1}x - 2\sqrt{1-x^2} + C$", r"Integrates $\frac{x}{\sqrt{1-x^2}}$ as $-2\sqrt{1-x^2}$, using $2\sqrt{u}$ without the factor $\frac{1}{2}$ from $du=-2x\,dx$."),
   (r"$-\sqrt{1-x^2} + C$", r"After splitting, drops the term $\int\frac{dx}{\sqrt{1-x^2}}$.")],
  r"Multiply inside by $\frac{1+x}{1+x}$: $\sqrt{\frac{1+x}{1-x}}=\frac{1+x}{\sqrt{1-x^2}}$ for $-1<x<1$. Then $\int\frac{dx}{\sqrt{1-x^2}}+\int\frac{x\,dx}{\sqrt{1-x^2}}=\sin^{-1}x-\sqrt{1-x^2}+C$.",
  r"Sign of $\int\frac{x}{\sqrt{1-x^2}}dx$.",
  "U08-C-rationalise-to-standard", "Rationalising step, then two standard integrals with a sign trap.",
  check=lambda: sqrt(1+x)/sqrt(1-x),
  values=dv(asin(x)-sqrt(1-x**2), asin(x)+sqrt(1-x**2), asin(x)-2*sqrt(1-x**2), -sqrt(1-x**2)),
  cognitive="Analysis", source_class=XII)


# ---------------------------------------------------------------- 051
def _c051():
    s = solve_coeffs(x + A_*log(x**2+2*x+5) + B_*atan((x+1)/2), x**2/(x**2+2*x+5), [A_, B_])[0]
    return (s[A_], s[B_])
q("U08-C-051", TOP, "Improper rational function leading to special forms", "Difficult", "Multi-step computation MCQ",
  r"$\int \frac{x^2}{x^2+2x+5}\,dx$ equals " + CC,
  r"$x - \log_e(x^2+2x+5) - \frac{3}{2}\tan^{-1}\frac{x+1}{2} + C$",
  [(r"$x - \log_e(x^2+2x+5) + \frac{3}{2}\tan^{-1}\frac{x+1}{2} + C$", r"After dividing, forgets that the minus sign applies to the remainder 3 as well."),
   (r"$x - \log_e(x^2+2x+5) - 3\tan^{-1}\frac{x+1}{2} + C$", r"Omits the factor $\frac{1}{a}=\frac{1}{2}$ on the inverse tangent."),
   (r"$x - \log_e(x^2+2x+5) - \frac{5}{2}\tan^{-1}\frac{x+1}{2} + C$", r"Takes the remainder as 5, not subtracting the 2 from $2x+2$.")],
  r"$\frac{x^2}{x^2+2x+5}=1-\frac{2x+5}{x^2+2x+5}$ and $2x+5=(2x+2)+3$. So the integral is $x-\log_e(x^2+2x+5)-3\int\frac{dx}{(x+1)^2+4}=x-\log_e(x^2+2x+5)-\frac{3}{2}\tan^{-1}\frac{x+1}{2}+C$.",
  r"Distributing the minus sign only to the first part of the split.",
  "U08-C-improper-rational-quad", "Division first, then split and two standard forms; sign trap.",
  check=_c051, values=[(-1, Rational(-3,2)), (-1, Rational(3,2)), (-1, -3), (-1, Rational(-5,2))],
  numerical=dict(question=r"If $\int \frac{x^2}{x^2+2x+5}\,dx = x + A\log_e(x^2+2x+5) + B\tan^{-1}\frac{x+1}{2} + C$, where $C$ is the constant of integration, then the value of $4AB$ is", answer=6),
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 052
q("U08-C-052", TOP, "Standard forms: true or false", "Difficult", "Statement-based MCQ",
  r"Consider the following statements, where $C$ is the constant of integration. Statement I: $\int \frac{dx}{2x^2+2x+1} = \frac{1}{2}\tan^{-1}(2x+1) + C$. Statement II: For $|x| < \frac{1}{2}$, $\int \sqrt{1-4x^2}\,dx = \frac{x}{2}\sqrt{1-4x^2} + \frac{1}{2}\sin^{-1}(2x) + C$. In the light of the above statements, choose the correct answer.",
  ST_FF,
  [(ST_TT, r"Factors out 2 in Statement I but does not then multiply by $\frac{1}{a}=2$, so accepts it; in Statement II copies the $\sqrt{a^2-x^2}$ formula with $a=1$, putting $2x$ only inside the radical and the inverse sine and keeping $\frac{x}{2}$ and $\frac{a^2}{2}=\frac{1}{2}$ unchanged (no substitution at all), so accepts it too."),
   (ST_TF, r"Factors out 2 in Statement I but does not then multiply by $\frac{1}{a}=2$, so accepts it; checks Statement II correctly."),
   (ST_FT, r"Handles Statement I correctly; in Statement II copies the $\sqrt{a^2-x^2}$ formula with $a=1$, putting $2x$ only inside the radical and the inverse sine and keeping $\frac{x}{2}$ and $\frac{a^2}{2}=\frac{1}{2}$ unchanged (no substitution at all), so accepts it.")],
  r"Statement I: $2x^2+2x+1=2\left[\left(x+\frac{1}{2}\right)^2+\frac{1}{4}\right]$, so the integral is $\frac{1}{2}\cdot 2\tan^{-1}(2x+1)+C=\tan^{-1}(2x+1)+C$; the statement is false. Statement II: with $u=2x$, $\frac{1}{2}\int\sqrt{1-u^2}du=\frac{1}{2}\left[\frac{u}{2}\sqrt{1-u^2}+\frac{1}{2}\sin^{-1}u\right]=\frac{x}{2}\sqrt{1-4x^2}+\frac{1}{4}\sin^{-1}(2x)$; the statement is false.",
  r"Losing the substitution or leading-coefficient factor in one term.",
  "U08-C-statements-b", "Two careful factor computations, each with a plausible-looking wrong constant.",
  check=lambda: (holds(atan(2*x+1)/2, 1/(2*x**2+2*x+1)), holds(x/2*sqrt(1-4*x**2)+asin(2*x)/2, sqrt(1-4*x**2))),
  values=[(False, False), (True, True), (True, False), (False, True)],
  cognitive="Analysis", source_class=XII)


# ---------------------------------------------------------------- 053
def _c053():
    # f(0) = f(1) + integral from 1 to 0 of f', with f(1) = 0
    return simplify(0 + integrate((x+5)/(3+2*x-x**2), (x, 1, 0)))
q("U08-C-053", TOP, "Function value from (px + q)/(c + bx - x^2)", "Difficult", "Multi-step computation MCQ",
  r"Let $f:(-1, 3) \to \mathbb{R}$ be a differentiable function with $f'(x) = \frac{x+5}{3+2x-x^2}$ and $f(1) = 0$. Then $f(0)$ equals",
  r"$\log_e\frac{2}{9}$",
  [(r"$\log_e 6$", r"Uses the $u^2-a^2$ ratio for the $a^2-u^2$ form, writing the second part as $\frac{3}{2}\log_e\left|\frac{3-x}{x+1}\right|$; then $C=\log_e 2$ and $f(0)=-\frac{1}{2}\log_e 3+\frac{3}{2}\log_e 3+\log_e 2=\log_e 6$."),
   (r"$\log_e\frac{1}{6}$", r"Takes $2x-2$ as the derivative of $3+2x-x^2$, so writes $x+5=\frac{1}{2}(2x-2)+6$ and the log term as $+\frac{1}{2}\log_e(3+2x-x^2)$; then $C=-\log_e 2$ and $f(0)=\frac{1}{2}\log_e 3-\frac{3}{2}\log_e 3-\log_e 2=\log_e\frac{1}{6}$."),
   (r"$\log_e\frac{1}{9}$", r"Integrates correctly but takes the constant of integration as 0, ignoring $f(1)=0$: $-\frac{1}{2}\log_e 3+\frac{3}{2}\log_e\frac{1}{3}=-2\log_e 3$.")],
  r"The derivative of $3+2x-x^2$ is $2-2x$, so $x+5=-\frac{1}{2}(2-2x)+6$. Also $3+2x-x^2=4-(x-1)^2$, so $\int\frac{6\,dx}{2^2-(x-1)^2}=\frac{6}{4}\log_e\left|\frac{2+(x-1)}{2-(x-1)}\right|$. Hence $f(x)=-\frac{1}{2}\log_e(3+2x-x^2)+\frac{3}{2}\log_e\frac{x+1}{3-x}+C$ on $(-1,3)$. $f(1)=-\frac{1}{2}\log_e 4+0+C=0$ gives $C=\log_e 2$, so $f(0)=-\frac{1}{2}\log_e 3+\frac{3}{2}\log_e\frac{1}{3}+\log_e 2=\log_e 2-2\log_e 3=\log_e\frac{2}{9}$.",
  r"Sign of the derivative of a negative-leading quadratic, and the orientation of the $a^2-u^2$ log ratio.",
  "U08-C-fvalue-linear-quad", "Negative leading coefficient: split against $2-2x$ with a negative factor, complete the square to the $a^2-u^2$ log form, fix a nonzero constant from $f(1)$, then evaluate; two sign traps.",
  check=_c053, values=[log(Rational(2,9)), log(6), log(Rational(1,6)), log(Rational(1,9))],
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 054
q("U08-C-054", TOP, "Substitution of a root of an exponential", "Difficult", "Multi-step computation MCQ",
  r"For $x > 0$, $\int \frac{dx}{\sqrt{e^x-1}}$ equals " + CC,
  r"$2\tan^{-1}\sqrt{e^x-1} + C$",
  [(r"$\tan^{-1}\sqrt{e^x-1} + C$", r"Puts $t=\sqrt{e^x-1}$ but takes $dx=\frac{t\,dt}{1+t^2}$ instead of $\frac{2t\,dt}{1+t^2}$."),
   (r"$2\sqrt{e^x-1} + C$", r"Integrates as if the numerator were $e^x\,dx$, treating it as $\int\frac{du}{\sqrt{u}}$."),
   (r"$\log_e\left|\frac{\sqrt{e^x-1}-1}{\sqrt{e^x-1}+1}\right| + C$", r"Writes $e^x=t^2-1$ instead of $t^2+1$, leading to $\int\frac{2\,dt}{t^2-1}$.")],
  r"Let $t=\sqrt{e^x-1}$, so $e^x=1+t^2$ and $e^x\,dx=2t\,dt$, giving $dx=\frac{2t\,dt}{1+t^2}$. Then $\int\frac{1}{t}\cdot\frac{2t\,dt}{1+t^2}=2\tan^{-1}t+C=2\tan^{-1}\sqrt{e^x-1}+C$.",
  r"Losing the factor 2 in $dx=\frac{2t\,dt}{1+t^2}$.",
  "U08-C-sub-root-exp", "Non-obvious substitution of the whole root; requires expressing $dx$ in $t$.",
  check=lambda: 1/sqrt(exp(x)-1),
  values=dv(2*atan(sqrt(exp(x)-1)), atan(sqrt(exp(x)-1)), 2*sqrt(exp(x)-1), log((sqrt(exp(x)-1)-1)/(sqrt(exp(x)-1)+1))),
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 055
q("U08-C-055", TOP, "Power substitution into 1/sqrt(a^2 - u^2)", "Difficult", "Multi-step computation MCQ",
  r"For $0 < x < 1$, $\int \sqrt{\frac{x}{1-x^3}}\,dx$ equals " + CC,
  r"$\frac{2}{3}\sin^{-1}\left(x^{3/2}\right) + C$",
  [(r"$\frac{3}{2}\sin^{-1}\left(x^{3/2}\right) + C$", r"Multiplies by $\frac{3}{2}$ instead of dividing when converting $\sqrt{x}\,dx$ to $du$."),
   (r"$\frac{1}{3}\sin^{-1}\left(x^{3/2}\right) + C$", r"Takes $d\left(x^{3/2}\right)=3\sqrt{x}\,dx$ instead of $\frac{3}{2}\sqrt{x}\,dx$."),
   (r"$\frac{2}{3}\cos^{-1}\left(x^{3/2}\right) + C$", r"Uses $\cos^{-1}$ and forgets the minus sign in its derivative.")],
  r"Write the integrand as $\frac{\sqrt{x}}{\sqrt{1-\left(x^{3/2}\right)^2}}$. With $u=x^{3/2}$, $du=\frac{3}{2}\sqrt{x}\,dx$, the integral becomes $\frac{2}{3}\int\frac{du}{\sqrt{1-u^2}}=\frac{2}{3}\sin^{-1}u+C=\frac{2}{3}\sin^{-1}\left(x^{3/2}\right)+C$.",
  r"Not seeing $x^3$ as $\left(x^{3/2}\right)^2$, or mis-scaling the substitution.",
  "U08-C-sub-power-standard", "Non-obvious fractional-power substitution into a standard form.",
  check=lambda: sqrt(x)/sqrt(1-x**3),
  values=dv(Rational(2,3)*asin(x**Rational(3,2)), Rational(3,2)*asin(x**Rational(3,2)),
            asin(x**Rational(3,2))/3, Rational(2,3)*acos(x**Rational(3,2))),
  cognitive="Analysis", source_class=XII)

# ---------------------------------------------------------------- 056
q("U08-C-056", TOP, "Power substitution leading to (pu + q)/(u^2 + bu + c)", "Difficult", "Multi-step computation MCQ",
  r"$\int \frac{x^3}{x^4+6x^2+10}\,dx$ equals " + CC,
  r"$\frac{1}{4}\log_e(x^4+6x^2+10) - \frac{3}{2}\tan^{-1}(x^2+3) + C$",
  [(r"$\frac{1}{4}\log_e(x^4+6x^2+10) + \frac{3}{2}\tan^{-1}(x^2+3) + C$", r"Writes $u=\frac{1}{2}(2u+6)+3$, a sign slip in the remainder."),
   (r"$\frac{1}{2}\log_e(x^4+6x^2+10) - 3\tan^{-1}(x^2+3) + C$", r"Puts $u=x^2$ but forgets that $x^3\,dx=\frac{u\,du}{2}$, losing the factor $\frac{1}{2}$ in both terms."),
   (r"$\frac{1}{4}\log_e(x^4+6x^2+10) - \frac{3}{2}\tan^{-1}(x+3) + C$", r"Back-substitutes $x$ instead of $x^2$ for $u$ in the inverse tangent.")],
  r"Let $u=x^2$, $du=2x\,dx$, so $x^3\,dx=\frac{u\,du}{2}$ and the integral is $\frac{1}{2}\int\frac{u\,du}{u^2+6u+10}$. Write $u=\frac{1}{2}(2u+6)-3$ and $u^2+6u+10=(u+3)^2+1$: $\frac{1}{2}\left[\frac{1}{2}\log_e(u^2+6u+10)-3\tan^{-1}(u+3)\right]+C=\frac{1}{4}\log_e(x^4+6x^2+10)-\frac{3}{2}\tan^{-1}(x^2+3)+C$.",
  r"Losing the factor $\frac{1}{2}$ from the substitution, or the sign of the remainder in the split.",
  "U08-C-sub-power-linear-quad", "Substitution, then a split of a linear numerator against the derivative of a quadratic, completing the square; three factors and a sign to track.",
  check=lambda: x**3/(x**4+6*x**2+10),
  values=dv(log(x**4+6*x**2+10)/4-Rational(3,2)*atan(x**2+3), log(x**4+6*x**2+10)/4+Rational(3,2)*atan(x**2+3),
            log(x**4+6*x**2+10)/2-3*atan(x**2+3), log(x**4+6*x**2+10)/4-Rational(3,2)*atan(x+3)),
  cognitive="Analysis", source_class=XII)
