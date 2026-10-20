import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *
import itertools

# ---------------------------------------------------------------- helpers
SC = "XII"
TB = "Total probability and Bayes' theorem"
RV = "Probability distribution of a random variable"
R_ = Rational

ST_TT = "Both Statement I and Statement II are true"
ST_FF = "Both Statement I and Statement II are false"
ST_TF = "Statement I is true but Statement II is false"
ST_FT = "Statement I is false but Statement II is true"
TAIL = r" In the light of the above statements, choose the correct answer."


def total(priors, likes):
    return sum(Rational(p) * Rational(l) for p, l in zip(priors, likes))


def bayes(priors, likes, i):
    return Rational(priors[i]) * Rational(likes[i]) / total(priors, likes)


def E(d, f=lambda x: x):
    return sum(sympify(p) * f(x) for x, p in d.items())


def Var(d):
    return simplify(E(d, lambda x: x**2) - E(d)**2)


def dist_from(outcomes, fn):
    """outcomes: list of equally likely outcomes; returns {value: prob}."""
    d = {}
    n = len(outcomes)
    for o in outcomes:
        v = fn(o)
        d[v] = d.get(v, 0) + Rational(1, n)
    return d


DIE = range(1, 7)

# ================================================================ EASY (13)


def _c001():
    return total([R_(1, 2), R_(1, 2)], [R_(3, 8), R_(4, 6)])


q("U13-D-001", TB, "Total probability with two bags", "Easy", "Single-step computation MCQ",
  r"Bag I contains $3$ red and $5$ black balls, and Bag II contains $4$ red and $2$ black balls. A fair coin is tossed; if it shows head, a ball is drawn at random from Bag I, otherwise from Bag II. The probability that the ball drawn is red is",
  r"$\frac{25}{48}$",
  [(r"$\frac{1}{2}$", r"Pools both bags into one bag of $14$ balls with $7$ red, ignoring that each bag is chosen with probability $\frac{1}{2}$: $\frac{7}{14} = \frac{1}{2}$."),
   (r"$\frac{1}{4}$", r"Multiplies the two conditional probabilities: $\frac{3}{8} \cdot \frac{2}{3} = \frac{1}{4}$."),
   (r"$\frac{17}{48}$", r"Uses the black count of Bag II as its red count: $\frac{1}{2} \cdot \frac{3}{8} + \frac{1}{2} \cdot \frac{2}{6} = \frac{3}{16} + \frac{1}{6} = \frac{17}{48}$.")],
  r"By the theorem of total probability, $P(R) = P(\text{I})P(R \mid \text{I}) + P(\text{II})P(R \mid \text{II}) = \frac{1}{2} \cdot \frac{3}{8} + \frac{1}{2} \cdot \frac{4}{6} = \frac{3}{16} + \frac{1}{3} = \frac{25}{48}$.",
  r"Pooling the balls of both bags instead of weighting each bag by the probability of choosing it.",
  "U13-D-total-prob-two-bags", "One application of total probability with two cases.",
  check=_c001, values=[R_(25, 48), R_(1, 2), R_(1, 4), R_(17, 48)], cognitive="Application", source_class=SC)


def _c002():
    k = Symbol('k')
    probs = [k, 2*k, 2*k**2, 3*k**2 + k]
    sols = [s for s in solve(sum(probs) - 1, k) if all(0 <= p.subs(k, s) <= 1 for p in probs)]
    assert len(sols) == 1
    s = sols[0]
    return probs[2].subs(k, s) + probs[3].subs(k, s)


q("U13-D-002", RV, "Validity of a distribution with an unknown constant", "Easy", "Single-step computation MCQ",
  r"A random variable $X$ takes the values $0, 1, 2, 3$ with $P(X=0) = k$, $P(X=1) = 2k$, $P(X=2) = 2k^2$ and $P(X=3) = 3k^2 + k$, where $k$ is a constant. Then $P(X \ge 2)$ equals",
  r"$\frac{2}{5}$",
  [(r"$\frac{3}{5}$", r"Finds $k = \frac{1}{5}$ correctly but computes $P(X < 2) = k + 2k = \frac{3}{5}$."),
   (r"$\frac{8}{25}$", r"Uses only $P(X = 3) = \frac{3}{25} + \frac{1}{5} = \frac{8}{25}$ and leaves out $P(X = 2)$."),
   (r"$\frac{1}{5}$", r"Stops after solving $5k^2 + 4k - 1 = 0$ and reports $k = \frac{1}{5}$ as the answer.")],
  r"The probabilities must add to $1$: $5k^2 + 4k - 1 = 0$, so $(5k-1)(k+1) = 0$ and, since probabilities are non-negative, $k = \frac{1}{5}$. Then $P(X \ge 2) = 2k^2 + 3k^2 + k = \frac{2}{25} + \frac{8}{25} = \frac{2}{5}$.",
  r"Not rejecting the negative root, or answering a different probability than the one asked.",
  "U13-D-rv-find-k-quadratic", "One equation from total probability, then a sum of two terms.",
  check=_c002, values=[R_(2, 5), R_(3, 5), R_(8, 25), R_(1, 5)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A random variable $X$ takes the values $0, 1, 2, 3$ with $P(X=0) = k$, $P(X=1) = 2k$, $P(X=2) = 2k^2$ and $P(X=3) = 3k^2 + k$, where $k$ is a constant. Then $P(X \ge 2)$ multiplied by $25$ is", answer=10))


def _c003():
    return E({-1: R_(1, 6), 0: R_(1, 3), 1: R_(1, 4), 2: R_(1, 4)})


q("U13-D-003", RV, "Mean from a probability table", "Easy", "Single-step computation MCQ",
  r"A random variable $X$ has the distribution $P(X=-1) = \frac{1}{6}$, $P(X=0) = \frac{1}{3}$, $P(X=1) = \frac{1}{4}$, $P(X=2) = \frac{1}{4}$. The mean of $X$ is",
  r"$\frac{7}{12}$",
  [(r"$\frac{1}{2}$", r"Takes the plain average of the values: $\frac{-1+0+1+2}{4} = \frac{1}{2}$."),
   (r"$\frac{11}{12}$", r"Drops the sign of $-1$: $\frac{1}{6} + \frac{1}{4} + \frac{2}{4} = \frac{11}{12}$."),
   (r"$\frac{3}{4}$", r"Omits the term for $X = -1$: $\frac{1}{4} + \frac{2}{4} = \frac{3}{4}$.")],
  r"$E(X) = \sum x\,P(X=x) = (-1)\frac{1}{6} + 0 + 1 \cdot \frac{1}{4} + 2 \cdot \frac{1}{4} = -\frac{1}{6} + \frac{3}{4} = \frac{7}{12}$.",
  r"Averaging the values without the probability weights, or losing the negative value.",
  "U13-D-rv-mean-table", "Direct use of the definition of mean.",
  check=_c003, values=[R_(7, 12), R_(1, 2), R_(11, 12), R_(3, 4)], cognitive="Application", source_class=SC)


def _c004():
    return Var({0: R_(1, 5), 1: R_(2, 5), 2: R_(2, 5)})


q("U13-D-004", RV, "Variance from a probability table", "Easy", "Single-step computation MCQ",
  r"A random variable $X$ takes the values $0, 1, 2$ with probabilities $\frac{1}{5}, \frac{2}{5}, \frac{2}{5}$ respectively. The variance of $X$ is",
  r"$\frac{14}{25}$",
  [(r"$2$", r"Reports $E(X^2) = \frac{2}{5} + \frac{8}{5} = 2$ and does not subtract the square of the mean."),
   (r"$\frac{4}{5}$", r"Subtracts the mean instead of its square: $2 - \frac{6}{5} = \frac{4}{5}$."),
   (r"$\frac{86}{25}$", r"Adds the square of the mean: $2 + \frac{36}{25} = \frac{86}{25}$.")],
  r"$E(X) = \frac{2}{5} + \frac{4}{5} = \frac{6}{5}$ and $E(X^2) = \frac{2}{5} + \frac{8}{5} = 2$. Hence $\operatorname{Var}(X) = E(X^2) - [E(X)]^2 = 2 - \frac{36}{25} = \frac{14}{25}$.",
  r"Using $E(X^2)$ or $E(X^2) - E(X)$ as the variance.",
  "U13-D-rv-variance-table", "Two expectations and one subtraction.",
  check=_c004, values=[R_(14, 25), 2, R_(4, 5), R_(86, 25)], cognitive="Application", source_class=SC)


def _c005():
    return bayes([R_(1, 2), R_(1, 2)], [R_(4, 10), R_(5, 8)], 0)


q("U13-D-005", TB, "Bayes' theorem with two bags", "Easy", "Single-step computation MCQ",
  r"Bag I contains $4$ red and $6$ white balls, and Bag II contains $5$ red and $3$ white balls. One of the bags is chosen at random and a ball drawn from it is found to be red. The probability that it was drawn from Bag I is",
  r"$\frac{16}{41}$",
  [(r"$\frac{2}{5}$", r"Reports $P(\text{red} \mid \text{Bag I}) = \frac{4}{10}$, reversing the conditioning."),
   (r"$\frac{1}{5}$", r"Reports the joint probability $P(\text{Bag I and red}) = \frac{1}{2} \cdot \frac{2}{5}$ without dividing by $P(\text{red})$."),
   (r"$\frac{25}{41}$", r"Computes the posterior probability of Bag II, $\frac{5/8}{2/5 + 5/8}$, instead of Bag I.")],
  r"With equal priors, $P(\text{I} \mid R) = \frac{\frac{1}{2} \cdot \frac{2}{5}}{\frac{1}{2} \cdot \frac{2}{5} + \frac{1}{2} \cdot \frac{5}{8}} = \frac{2/5}{41/40} = \frac{16}{41}$.",
  r"Confusing $P(\text{Bag I} \mid \text{red})$ with $P(\text{red} \mid \text{Bag I})$.",
  "U13-D-bayes-two-bags", "Direct single application of Bayes' theorem.",
  check=_c005, values=[R_(16, 41), R_(2, 5), R_(1, 5), R_(25, 41)], cognitive="Application", source_class=SC)


def _c006():
    return total([R_(60, 100), R_(40, 100)], [R_(2, 100), R_(3, 100)])


q("U13-D-006", TB, "Total probability in production", "Easy", "Single-step computation MCQ",
  r"A factory has two machines $M_1$ and $M_2$ producing $60\%$ and $40\%$ of its bolts respectively. Of the bolts produced, $2\%$ from $M_1$ and $3\%$ from $M_2$ are defective. A bolt is chosen at random from the total output. If $p$ is the probability that it is defective, then $p$ equals",
  r"$\frac{3}{125}$",
  [(r"$\frac{1}{40}$", r"Averages the two defect rates without weights: $\frac{2\% + 3\%}{2} = 2.5\% = \frac{1}{40}$."),
   (r"$\frac{1}{20}$", r"Adds the defect rates: $2\% + 3\% = 5\% = \frac{1}{20}$."),
   (r"$\frac{3}{250}$", r"Keeps only one of the two terms, $0.6 \times 0.02 = 0.012 = \frac{3}{250}$.")],
  r"$p = P(M_1)P(D \mid M_1) + P(M_2)P(D \mid M_2) = 0.6 \times 0.02 + 0.4 \times 0.03 = 0.012 + 0.012 = 0.024 = \frac{3}{125}$.",
  r"Averaging the conditional rates instead of weighting them by the production shares.",
  "U13-D-total-prob-machines", "One weighted sum of two terms.",
  check=_c006, values=[R_(3, 125), R_(1, 40), R_(1, 20), R_(3, 250)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A factory has two machines $M_1$ and $M_2$ producing $60\%$ and $40\%$ of its bolts respectively. Of the bolts produced, $2\%$ from $M_1$ and $3\%$ from $M_2$ are defective. A bolt is chosen at random from the total output. If $p$ is the probability that it is defective, then $p$ multiplied by $1000$ is", answer=24))


def _c007():
    d = dist_from(list(itertools.product(DIE, DIE)), lambda o: sum(1 for v in o if v == 6))
    return E(d)


q("U13-D-007", RV, "Mean of the number of sixes", "Easy", "Single-step computation MCQ",
  r"A fair die is thrown twice. If $X$ denotes the number of sixes obtained, then $E(X)$ equals",
  r"$\frac{1}{3}$",
  [(r"$\frac{1}{6}$", r"Uses the probability of a six on a single throw as the mean for two throws."),
   (r"$\frac{11}{36}$", r"Adds $P(X=1) + P(X=2) = \frac{10}{36} + \frac{1}{36}$ without multiplying by the values $1$ and $2$."),
   (r"$\frac{7}{36}$", r"Counts only one order for exactly one six, $P(X=1) = \frac{5}{36}$, then $\frac{5}{36} + 2 \cdot \frac{1}{36} = \frac{7}{36}$.")],
  r"$P(X=0) = \frac{25}{36}$, $P(X=1) = \frac{10}{36}$, $P(X=2) = \frac{1}{36}$. Hence $E(X) = \frac{10}{36} + \frac{2}{36} = \frac{12}{36} = \frac{1}{3}$.",
  r"Forgetting the two orders in which exactly one six can occur.",
  "U13-D-rv-dice-sixes", "Small distribution built from 36 outcomes, then a mean.",
  check=_c007, values=[R_(1, 3), R_(1, 6), R_(11, 36), R_(7, 36)], cognitive="Application", source_class=SC)


def _c008():
    d = {x: R_(x, 10) for x in range(1, 5)}
    s1 = (sum(d.values()) == 1) and all(0 <= p <= 1 for p in d.values())
    d2 = {2*x + 3: p for x, p in d.items()}
    s2 = simplify(Var(d2) - (4*Var(d) + 3)) == 0
    return (bool(s1), bool(s2))


q("U13-D-008", RV, "Validity of a distribution and variance of a linear function", "Easy", "Statement-based MCQ",
  r"Statement I: The function $P(X = x) = \frac{x}{10}$, $x = 1, 2, 3, 4$, is a valid probability distribution of a random variable $X$. Statement II: For every random variable $X$ with finite variance, $\operatorname{Var}(2X + 3) = 4\operatorname{Var}(X) + 3$." + TAIL,
  ST_TF,
  [(ST_TT, r"Accepts Statement II, wrongly carrying the additive constant into the variance."),
   (ST_FF, r"Rejects Statement I, perhaps thinking the probabilities must be equal, and also rejects Statement II."),
   (ST_FT, r"Rejects the valid distribution in Statement I and accepts the false rule in Statement II.")],
  r"In Statement I each value is in $[0, 1]$ and $\frac{1+2+3+4}{10} = 1$, so it is valid. In Statement II, adding a constant does not change spread, so $\operatorname{Var}(2X+3) = 4\operatorname{Var}(X)$, not $4\operatorname{Var}(X) + 3$; for the distribution of Statement I, $\operatorname{Var}(X) = 1$ and $\operatorname{Var}(2X+3) = 4 \ne 7$.",
  r"Believing a shift of origin changes the variance.",
  "U13-D-statement-rv", "Two quick checks of basic facts.",
  check=_c008, values=[(True, False), (True, True), (False, False), (False, True)], cognitive="Understanding", source_class=SC)


def _c009():
    return total([R_(2, 6), R_(4, 6)], [R_(2, 5), R_(4, 5)])


q("U13-D-009", TB, "Total probability with a die choosing the urn", "Easy", "Single-step computation MCQ",
  r"Urn $U_1$ contains $2$ white and $3$ black balls, and urn $U_2$ contains $4$ white and $1$ black ball. A fair die is thrown; if it shows $1$ or $2$, a ball is drawn at random from $U_1$, otherwise from $U_2$. The probability that the ball drawn is white is",
  r"$\frac{2}{3}$",
  [(r"$\frac{3}{5}$", r"Treats the two urns as equally likely: $\frac{1}{2}\left(\frac{2}{5} + \frac{4}{5}\right) = \frac{3}{5}$."),
   (r"$\frac{8}{15}$", r"Swaps the urn probabilities: $\frac{1}{3} \cdot \frac{4}{5} + \frac{2}{3} \cdot \frac{2}{5} = \frac{8}{15}$."),
   (r"$\frac{8}{25}$", r"Multiplies the two conditional probabilities: $\frac{2}{5} \cdot \frac{4}{5} = \frac{8}{25}$.")],
  r"$P(U_1) = \frac{2}{6} = \frac{1}{3}$ and $P(U_2) = \frac{2}{3}$. So $P(W) = \frac{1}{3} \cdot \frac{2}{5} + \frac{2}{3} \cdot \frac{4}{5} = \frac{2}{15} + \frac{8}{15} = \frac{2}{3}$.",
  r"Giving the urns equal weight when the die makes them unequally likely.",
  "U13-D-total-prob-two-bags", "One weighted sum; the only care is the unequal priors.",
  check=_c009, values=[R_(2, 3), R_(3, 5), R_(8, 15), R_(8, 25)], cognitive="Application", source_class=SC)


def _c010():
    d = {1: R_(1, 2), 2: R_(1, 3)}
    d[3] = 1 - sum(d.values())
    return E(d, lambda x: 2*x + 1)


q("U13-D-010", RV, "Mean of a linear function of a random variable", "Easy", "Single-step computation MCQ",
  r"A random variable $X$ takes only the values $1, 2, 3$, with $P(X=1) = \frac{1}{2}$ and $P(X=2) = \frac{1}{3}$. Then $E(2X + 1)$ equals",
  r"$\frac{13}{3}$",
  [(r"$\frac{10}{3}$", r"Computes $2E(X) = \frac{10}{3}$ and drops the $+1$."),
   (r"$\frac{8}{3}$", r"Computes $E(X) + 1 = \frac{8}{3}$, dropping the factor $2$."),
   (r"$5$", r"Uses the unweighted average $2$ of the values as $E(X)$, giving $2 \cdot 2 + 1 = 5$.")],
  r"$P(X=3) = 1 - \frac{1}{2} - \frac{1}{3} = \frac{1}{6}$, so $E(X) = \frac{1}{2} + \frac{2}{3} + \frac{1}{2} = \frac{5}{3}$. Then $E(2X+1) = 2E(X) + 1 = \frac{13}{3}$.",
  r"Applying linearity of expectation only partly.",
  "U13-D-rv-linear-mean", "Find the missing probability, then use linearity.",
  check=_c010, values=[R_(13, 3), R_(10, 3), R_(8, 3), 5], cognitive="Application", source_class=SC)


def _c011():
    return bayes([R_(40, 100), R_(60, 100)], [R_(30, 100), R_(20, 100)], 0)


q("U13-D-011", TB, "Bayes' theorem in a survey", "Easy", "Single-step computation MCQ",
  r"In a class, $40\%$ of the students are girls. $30\%$ of the girls and $20\%$ of the boys wear spectacles. A student chosen at random is found to wear spectacles. The probability that the student is a girl is",
  r"$\frac{1}{2}$",
  [(r"$\frac{2}{5}$", r"Reports the prior $P(\text{girl}) = 0.4$ and ignores the information about spectacles."),
   (r"$\frac{3}{10}$", r"Reports $P(\text{spectacles} \mid \text{girl}) = 0.3$, reversing the conditioning."),
   (r"$\frac{3}{25}$", r"Reports the joint probability $0.4 \times 0.3 = 0.12$ without dividing by $P(\text{spectacles})$.")],
  r"$P(S) = 0.4 \times 0.3 + 0.6 \times 0.2 = 0.12 + 0.12 = 0.24$. Hence $P(G \mid S) = \frac{0.12}{0.24} = \frac{1}{2}$.",
  r"Ignoring the evidence and keeping the prior probability.",
  "U13-D-bayes-class-survey", "Single application of Bayes' theorem with percentages.",
  check=_c011, values=[R_(1, 2), R_(2, 5), R_(3, 10), R_(3, 25)], cognitive="Application", source_class=SC)


def _c012():
    F = {1: R_(1, 5), 2: R_(1, 2), 3: R_(4, 5), 4: Integer(1)}
    pmf = {x: F[x] - F.get(x - 1, 0) for x in F}
    return pmf[2] + pmf[3]


q("U13-D-012", RV, "Probabilities from cumulative probabilities", "Easy", "Single-step computation MCQ",
  r"A random variable $X$ takes only the values $1, 2, 3, 4$, and $P(X \le 1) = \frac{1}{5}$, $P(X \le 2) = \frac{1}{2}$, $P(X \le 3) = \frac{4}{5}$. Then $P(2 \le X \le 3)$ equals",
  r"$\frac{3}{5}$",
  [(r"$\frac{3}{10}$", r"Computes $P(X \le 3) - P(X \le 2) = P(X = 3)$ only, leaving out $X = 2$."),
   (r"$\frac{4}{5}$", r"Uses $P(X \le 3)$ directly, without removing $P(X = 1)$."),
   (r"$\frac{1}{2}$", r"Shifts the indices and computes $P(X \le 4) - P(X \le 2) = 1 - \frac{1}{2}$.")],
  r"$P(2 \le X \le 3) = P(X \le 3) - P(X \le 1) = \frac{4}{5} - \frac{1}{5} = \frac{3}{5}$.",
  r"Subtracting the wrong cumulative value at the lower end.",
  "U13-D-rv-cumulative", "One subtraction once the cumulative idea is clear.",
  check=_c012, values=[R_(3, 5), R_(3, 10), R_(4, 5), R_(1, 2)], cognitive="Understanding", source_class=SC)


def _c013():
    return total([R_(3, 5), R_(2, 5)], [1, R_(1, 4)])


q("U13-D-013", TB, "Total probability in answering a question", "Easy", "Single-step computation MCQ",
  r"In a test, a student either knows the answer to a multiple choice question with $4$ options or guesses. The probability that the student knows the answer is $\frac{3}{5}$. A guess is correct with probability $\frac{1}{4}$, and an answer that is known is always correct. If $p$ is the probability that the student answers the question correctly, then $p$ equals",
  r"$\frac{7}{10}$",
  [(r"$\frac{17}{20}$", r"Adds $\frac{1}{4}$ without weighting it by $\frac{2}{5}$: $\frac{3}{5} + \frac{1}{4} = \frac{17}{20}$."),
   (r"$\frac{3}{5}$", r"Ignores the chance of a correct guess."),
   (r"$\frac{1}{10}$", r"Keeps only the guessing term $\frac{2}{5} \cdot \frac{1}{4}$.")],
  r"$p = P(K) \cdot 1 + P(K')\cdot\frac{1}{4} = \frac{3}{5} + \frac{2}{5} \cdot \frac{1}{4} = \frac{3}{5} + \frac{1}{10} = \frac{7}{10}$.",
  r"Not weighting the guessing probability by the chance of guessing.",
  "U13-D-total-prob-guess", "Two-case total probability.",
  check=_c013, values=[R_(7, 10), R_(17, 20), R_(3, 5), R_(1, 10)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"In a test, a student either knows the answer to a multiple choice question with $4$ options or guesses. The probability that the student knows the answer is $\frac{3}{5}$. A guess is correct with probability $\frac{1}{4}$, and an answer that is known is always correct. If $p$ is the probability that the student answers the question correctly, then $p$ multiplied by $10$ is", answer=7))

# ================================================================ MEDIUM (20)


def _c014():
    return bayes([R_(2, 3), R_(1, 3)], [1, R_(1, 5)], 0)


q("U13-D-014", TB, "Bayes' theorem: knowing versus guessing", "Medium", "Multi-step computation MCQ",
  r"A multiple choice question has $5$ options, exactly one of which is correct. A student knows the answer with probability $\frac{2}{3}$; otherwise the student guesses one option at random. An answer that is known is always correct. Given that the student answered correctly, the probability that the student actually knew the answer is",
  r"$\frac{10}{11}$",
  [(r"$\frac{2}{3}$", r"Keeps the prior probability of knowing and ignores the evidence of a correct answer."),
   (r"$\frac{1}{11}$", r"Computes the posterior probability of having guessed instead of having known."),
   (r"$\frac{4}{5}$", r"Takes a guess to be right with probability $\frac{1}{2}$ (right or wrong): $\frac{2/3}{2/3 + 1/6} = \frac{4}{5}$.")],
  r"$P(S) = \frac{2}{3} \cdot 1 + \frac{1}{3} \cdot \frac{1}{5} = \frac{11}{15}$, where $S$ is the event of a correct answer. By Bayes' theorem, $P(K \mid S) = \frac{2/3}{11/15} = \frac{10}{11}$.",
  r"Taking the chance of a correct guess as $\frac{1}{2}$ instead of $\frac{1}{\text{number of options}}$.",
  "U13-D-bayes-guess", "Total probability followed by Bayes, with a guessing trap.",
  check=_c014, values=[R_(10, 11), R_(2, 3), R_(1, 11), R_(4, 5)], cognitive="Application", source_class=SC)


def _c015():
    return bayes([R_(30, 100), R_(30, 100), R_(40, 100)], [R_(3, 100), R_(4, 100), R_(2, 100)], 1)


q("U13-D-015", TB, "Bayes' theorem with three machines", "Medium", "Multi-step computation MCQ",
  r"Machines $M_1$, $M_2$, $M_3$ produce $30\%$, $30\%$ and $40\%$ of the items in a factory, and $3\%$, $4\%$ and $2\%$ of their respective outputs are defective. An item chosen at random from the total output is found to be defective. The probability that it was produced by $M_2$ is",
  r"$\frac{12}{29}$",
  [(r"$\frac{3}{10}$", r"Reports the prior share of $M_2$ and ignores the defect information."),
   (r"$\frac{4}{9}$", r"Ignores the production shares and uses only defect rates: $\frac{4}{3+4+2} = \frac{4}{9}$."),
   (r"$\frac{8}{29}$", r"Uses the term of $M_3$, $\frac{0.4 \times 0.02}{0.029}$, in the numerator instead of that of $M_2$.")],
  r"With $F$ the event that the item is defective, $P(F) = 0.3(0.03) + 0.3(0.04) + 0.4(0.02) = 0.009 + 0.012 + 0.008 = 0.029$. Hence $P(M_2 \mid F) = \frac{0.012}{0.029} = \frac{12}{29}$.",
  r"Using only the conditional defect rates and ignoring the priors.",
  "U13-D-bayes-machines", "Three-hypothesis Bayes with percentages.",
  check=_c015, values=[R_(12, 29), R_(3, 10), R_(4, 9), R_(8, 29)], cognitive="Application", source_class=SC)


def _c016():
    return bayes([R_(2, 100), R_(98, 100)], [R_(95, 100), R_(5, 100)], 0)


q("U13-D-016", TB, "Bayes' theorem in a medical test", "Medium", "Multi-step computation MCQ",
  r"A disease affects $2\%$ of a population. A test for it gives a positive result for $95\%$ of people who have the disease and also for $5\%$ of people who do not. A person chosen at random tests positive. The probability that the person has the disease is",
  r"$\frac{19}{68}$",
  [(r"$\frac{19}{20}$", r"Reports the detection rate $P(+ \mid \text{disease}) = 0.95$, reversing the conditioning."),
   (r"$\frac{1}{50}$", r"Keeps the prior $2\%$ and ignores the test result."),
   (r"$\frac{19}{49}$", r"Divides $0.019$ by the false positive part $0.049$ alone instead of by $P(+) = 0.068$.")],
  r"$P(+) = 0.02 \times 0.95 + 0.98 \times 0.05 = 0.019 + 0.049 = 0.068$. Then $P(\text{disease} \mid +) = \frac{0.019}{0.068} = \frac{19}{68}$.",
  r"Confusing the accuracy of the test with the probability of disease given a positive result.",
  "U13-D-bayes-medical-test", "Total probability with a small prior, then Bayes; the base-rate trap.",
  check=_c016, values=[R_(19, 68), R_(19, 20), R_(1, 50), R_(19, 49)], cognitive="Analysis", source_class=SC)


def _c017():
    return bayes([R_(1, 6), R_(5, 6)], [R_(3, 4), R_(1, 4)], 0)


q("U13-D-017", TB, "Bayes' theorem with a reported outcome", "Medium", "Multi-step computation MCQ",
  r"A man reports the truth with probability $\frac{3}{4}$. He throws a fair die and reports that it shows a six. Assume that when the die does not show a six, he reports a six exactly when he lies. If $p$ is the probability that the die actually shows a six, then $p$ equals",
  r"$\frac{3}{8}$",
  [(r"$\frac{3}{4}$", r"Takes the probability that the report is true to be the man's truthfulness, ignoring how rare a six is."),
   (r"$\frac{1}{8}$", r"Reports the joint probability $\frac{1}{6} \cdot \frac{3}{4}$ without dividing by $P(\text{reports six})$."),
   (r"$\frac{5}{8}$", r"Computes the posterior probability that the die does not show a six.")],
  r"$P(\text{reports six}) = \frac{1}{6} \cdot \frac{3}{4} + \frac{5}{6} \cdot \frac{1}{4} = \frac{3}{24} + \frac{5}{24} = \frac{1}{3}$. Hence $p = \frac{3/24}{8/24} = \frac{3}{8}$.",
  r"Equating the reliability of the reporter with the probability that the reported event happened.",
  "U13-D-bayes-truth-report", "Total probability then Bayes; counterintuitive answer below one half.",
  check=_c017, values=[R_(3, 8), R_(3, 4), R_(1, 8), R_(5, 8)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"A man reports the truth with probability $\frac{3}{4}$. He throws a fair die and reports that it shows a six. Assume that when the die does not show a six, he reports a six exactly when he lies. If $p$ is the probability that the die actually shows a six, then $p$ multiplied by $8$ is", answer=3))


def _c018():
    # bag I: 3 red, 2 black; bag II: 2 red, 4 black; one ball moved I -> II
    return total([R_(3, 5), R_(2, 5)], [R_(3, 7), R_(2, 7)])


q("U13-D-018", TB, "Total probability after a transfer", "Medium", "Multi-step computation MCQ",
  r"Bag I contains $3$ red and $2$ black balls, and Bag II contains $2$ red and $4$ black balls. One ball is drawn at random from Bag I and put into Bag II without noting its colour. A ball is then drawn at random from Bag II. The probability that this ball is red is",
  r"$\frac{13}{35}$",
  [(r"$\frac{1}{3}$", r"Ignores the transfer and uses Bag II as it was: $\frac{2}{6}$."),
   (r"$\frac{13}{30}$", r"Adds the transferred ball to the red count but keeps the total in Bag II as $6$: $\frac{3}{5}\cdot\frac{3}{6} + \frac{2}{5}\cdot\frac{2}{6}$."),
   (r"$\frac{9}{35}$", r"Keeps only the case in which the transferred ball is red: $\frac{3}{5} \cdot \frac{3}{7}$.")],
  r"Condition on the colour of the transferred ball. $P(R) = \frac{3}{5} \cdot \frac{3}{7} + \frac{2}{5} \cdot \frac{2}{7} = \frac{9}{35} + \frac{4}{35} = \frac{13}{35}$.",
  r"Forgetting that Bag II has $7$ balls after the transfer.",
  "U13-D-total-prob-transfer", "Two-stage experiment needing a partition on the transferred ball.",
  check=_c018, values=[R_(13, 35), R_(1, 3), R_(13, 30), R_(9, 35)], cognitive="Application", source_class=SC)


def _c019():
    # bag I: 4 white, 2 black; bag II: 3 white, 5 black; transfer one I -> II; drawn white
    return bayes([R_(4, 6), R_(2, 6)], [R_(4, 9), R_(3, 9)], 1)


q("U13-D-019", TB, "Bayes' theorem after a transfer", "Medium", "Multi-step computation MCQ",
  r"Bag I contains $4$ white and $2$ black balls, and Bag II contains $3$ white and $5$ black balls. One ball is transferred at random from Bag I to Bag II, and then a ball drawn at random from Bag II is found to be white. The probability that the transferred ball was black is",
  r"$\frac{3}{11}$",
  [(r"$\frac{1}{3}$", r"Reports the prior probability $\frac{2}{6}$ that the transferred ball is black."),
   (r"$\frac{8}{11}$", r"Computes the posterior probability that the transferred ball was white."),
   (r"$\frac{1}{9}$", r"Reports the joint probability $\frac{2}{6} \cdot \frac{3}{9}$ without dividing by $P(\text{white})$.")],
  r"$P(W) = \frac{4}{6} \cdot \frac{4}{9} + \frac{2}{6} \cdot \frac{3}{9} = \frac{16}{54} + \frac{6}{54} = \frac{22}{54}$. Then $P(\text{black transferred} \mid W) = \frac{6/54}{22/54} = \frac{3}{11}$.",
  r"Stopping at the joint probability instead of dividing by the total probability of the evidence.",
  "U13-D-bayes-transfer", "Transfer experiment plus Bayes.",
  check=_c019, values=[R_(3, 11), R_(1, 3), R_(8, 11), R_(1, 9)], cognitive="Application", source_class=SC)


def _c020():
    a, b = symbols('a b')
    d = {0: R_(1, 6), 1: a, 2: b, 3: R_(1, 4)}
    s = solve([sum(d.values()) - 1, E(d) - R_(3, 2)], [a, b], dict=True)[0]
    return s[a]


q("U13-D-020", RV, "Unknown probabilities from the mean", "Medium", "Inverse/parameter MCQ",
  r"A random variable $X$ takes the values $0, 1, 2, 3$ with $P(X=0) = \frac{1}{6}$, $P(X=1) = a$, $P(X=2) = b$, $P(X=3) = \frac{1}{4}$. If $E(X) = \frac{3}{2}$, then $a$ equals",
  r"$\frac{5}{12}$",
  [(r"$\frac{1}{6}$", r"Solves correctly but reports $b = \frac{1}{6}$ instead of $a$."),
   (r"$\frac{7}{24}$", r"Uses only $a + b = \frac{7}{12}$ and assumes $a = b$, never using the mean."),
   (r"$\frac{3}{4}$", r"Leaves out $P(X=0)$ in the total, taking $a + b = \frac{3}{4}$; with $a + 2b = \frac{3}{4}$ this gives $b = 0$, $a = \frac{3}{4}$.")],
  r"Total probability gives $a + b = 1 - \frac{1}{6} - \frac{1}{4} = \frac{7}{12}$. The mean gives $a + 2b + \frac{3}{4} = \frac{3}{2}$, so $a + 2b = \frac{3}{4}$. Subtracting, $b = \frac{1}{6}$ and $a = \frac{5}{12}$.",
  r"Using only one of the two conditions needed for two unknowns.",
  "U13-D-rv-unknowns-mean", "Two linear conditions in two unknowns.",
  check=_c020, values=[R_(5, 12), R_(1, 6), R_(7, 24), R_(3, 4)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A random variable $X$ takes the values $0, 1, 2, 3$ with $P(X=0) = \frac{1}{6}$, $P(X=1) = a$, $P(X=2) = b$, $P(X=3) = \frac{1}{4}$. If $E(X) = \frac{3}{2}$, then $a$ multiplied by $12$ is", answer=5))


def _c021():
    k = Symbol('k')
    d = {x: k*x**2 for x in (1, 2, 3)}
    kv = solve(sum(d.values()) - 1, k)[0]
    d = {x: p.subs(k, kv) for x, p in d.items()}
    return Var(d)


q("U13-D-021", RV, "Variance after finding the constant", "Medium", "Multi-step computation MCQ",
  r"A random variable $X$ takes the values $1, 2, 3$ with $P(X = x) = kx^2$, where $k$ is a constant. The variance of $X$ is",
  r"$\frac{19}{49}$",
  [(r"$7$", r"Reports $E(X^2) = \frac{1 + 16 + 81}{14} = 7$ and forgets to subtract the square of the mean."),
   (r"$\frac{31}{7}$", r"Subtracts the mean instead of its square: $7 - \frac{18}{7} = \frac{31}{7}$."),
   (r"$\frac{2}{3}$", r"Treats the values $1, 2, 3$ as equally likely and gives their variance $\frac{2}{3}$.")],
  r"$k(1 + 4 + 9) = 1$ gives $k = \frac{1}{14}$. Then $E(X) = \frac{1 + 8 + 27}{14} = \frac{18}{7}$ and $E(X^2) = \frac{1 + 16 + 81}{14} = 7$, so $\operatorname{Var}(X) = 7 - \frac{324}{49} = \frac{19}{49}$.",
  r"Using $E(X^2)$ as the variance.",
  "U13-D-rv-pmf-formula-variance", "Normalise, then two moments, then a subtraction.",
  check=_c021, values=[R_(19, 49), 7, R_(31, 7), R_(2, 3)], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A random variable $X$ takes the values $1, 2, 3$ with $P(X = x) = kx^2$, where $k$ is a constant. Then $\operatorname{Var}(X)$ multiplied by $49$ is", answer=19))


def _c022():
    x = Symbol('x')
    d = dist_from(list(itertools.product(DIE, DIE)), lambda o: 'D' if o[0] == o[1] else ('S' if sum(o) == 7 else 'L'))
    gain = d['D'] * 10 + d['S'] * 2 - d['L'] * x
    return solve(gain, x)[0]


q("U13-D-022", RV, "Fair game", "Medium", "Inverse/parameter MCQ",
  r"In a game, two fair dice are thrown. A player wins Rs $10$ if the two numbers are equal, wins Rs $2$ if the sum of the numbers is $7$, and loses Rs $x$ in every other case. If the game is fair (the expected gain of the player is zero), then $x$ equals",
  r"$3$",
  [(r"$\frac{12}{5}$", r"Takes the losing probability as $\frac{30}{36}$ (only excluding doublets): $\frac{30}{36}x = 2$."),
   (r"$\frac{5}{2}$", r"Ignores the Rs $2$ prize: $\frac{6}{36}\cdot 10 = \frac{24}{36}x$."),
   (r"$2$", r"Equates the expected winnings $2$ directly to $x$ without multiplying $x$ by its probability $\frac{24}{36}$.")],
  r"$P(\text{doublet}) = \frac{6}{36}$, $P(\text{sum } 7) = \frac{6}{36}$ (these cannot overlap) and the remaining probability is $\frac{24}{36}$. Fairness requires $10 \cdot \frac{6}{36} + 2 \cdot \frac{6}{36} - x \cdot \frac{24}{36} = 0$, i.e. $72 = 24x$, so $x = 3$.",
  r"Not weighting the loss by its probability.",
  "U13-D-rv-fair-game", "Build a three-outcome distribution, then solve an expectation equation.",
  check=_c022, values=[3, R_(12, 5), R_(5, 2), 2], cognitive="Application", source_class=SC,
  numerical=dict(question=r"In a game, two fair dice are thrown. A player wins Rs $10$ if the two numbers are equal, wins Rs $2$ if the sum of the numbers is $7$, and loses Rs $x$ in every other case. If the game is fair (the expected gain of the player is zero), then $x$ is", answer=3))


def _c023():
    # urn: 3 red, 5 black; drawn ball kept out and replaced by a ball of the other colour
    red, black = 3, 5
    tot = red + black
    num = Rational(0); den = Rational(0)
    for first in ['R', 'B']:
        p1 = Rational(red if first == 'R' else black, tot)
        r2 = red - 1 if first == 'R' else red + 1
        p2 = Rational(r2, tot)
        den += p1 * p2
        if first == 'R':
            num += p1 * p2
    return num / den


q("U13-D-023", TB, "Inferring the first draw from the second", "Medium", "Multi-step computation MCQ",
  r"An urn contains $3$ red and $5$ black balls. A ball is drawn at random and is not returned; instead, a ball of the other colour is put into the urn in its place. A second ball is then drawn at random. Given that the second ball drawn is red, the probability that the first ball drawn was red is",
  r"$\frac{3}{13}$",
  [(r"$\frac{3}{8}$", r"Uses the unconditional probability $\frac{3}{8}$ that the first ball is red, ignoring the information from the second draw."),
   (r"$\frac{2}{7}$", r"Ignores the substitute ball and treats the draws as plain without replacement: $\frac{\frac{3}{8} \cdot \frac{2}{7}}{\frac{3}{8} \cdot \frac{2}{7} + \frac{5}{8} \cdot \frac{3}{7}} = \frac{6}{21}$."),
   (r"$\frac{3}{32}$", r"Reports the joint probability $\frac{3}{8} \cdot \frac{2}{8}$ without dividing by $P(\text{second red})$.")],
  r"If the first ball is red, the urn becomes $2$ red and $6$ black; if black, it becomes $4$ red and $4$ black. So $P(\text{2nd red}) = \frac{3}{8} \cdot \frac{2}{8} + \frac{5}{8} \cdot \frac{4}{8} = \frac{6 + 20}{64} = \frac{26}{64}$. By Bayes' theorem, $P(\text{1st red} \mid \text{2nd red}) = \frac{6}{26} = \frac{3}{13}$.",
  r"Believing the second draw carries no information about the first, or not updating the urn after the swap.",
  "U13-D-bayes-swap-draw", "Two-stage urn with a swap; total probability for the second draw, then Bayes backward in time.",
  check=_c023, values=[R_(3, 13), R_(3, 8), R_(2, 7), R_(3, 32)], cognitive="Analysis", source_class=SC)


def _c024():
    pri = [R_(1, 6), R_(2, 6), R_(3, 6)]
    lik = [R_(2, 3), R_(1, 3), R_(3, 6)]
    return bayes(pri, lik, 2)


q("U13-D-024", TB, "Bayes' theorem with three urns of unequal priors", "Medium", "Multi-step computation MCQ",
  r"A fair die is thrown. If it shows $1$, a ball is drawn from urn $U_1$ ($2$ white, $1$ red); if it shows $2$ or $3$, from urn $U_2$ ($1$ white, $2$ red); otherwise from urn $U_3$ ($3$ white, $3$ red). The ball drawn is white. The probability that it came from $U_3$ is",
  r"$\frac{9}{17}$",
  [(r"$\frac{1}{2}$", r"Reports the prior $P(U_3) = \frac{3}{6}$, ignoring the colour."),
   (r"$\frac{1}{3}$", r"Treats the three urns as equally likely: $\frac{1/2}{2/3 + 1/3 + 1/2} = \frac{1}{3}$."),
   (r"$\frac{1}{4}$", r"Reports the joint probability $\frac{1}{2} \cdot \frac{1}{2}$ without dividing by $P(W)$.")],
  r"$P(W) = \frac{1}{6} \cdot \frac{2}{3} + \frac{1}{3} \cdot \frac{1}{3} + \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{9} + \frac{1}{9} + \frac{1}{4} = \frac{17}{36}$. So $P(U_3 \mid W) = \frac{1/4}{17/36} = \frac{9}{17}$.",
  r"Treating the urns as equally likely when the die gives them different probabilities.",
  "U13-D-bayes-three-urns", "Three hypotheses with unequal priors.",
  check=_c024, values=[R_(9, 17), R_(1, 2), R_(1, 3), R_(1, 4)], cognitive="Application", source_class=SC)


def _c025():
    mu, v = Integer(2), Integer(3)
    EX2 = v + mu**2
    x = Symbol('x')
    poly = Poly(expand((2*x - 1)**2), x)
    moments = {0: 1, 1: mu, 2: EX2}
    return sum(c * moments[m[0]] for m, c in poly.terms())


q("U13-D-025", RV, "Expectation of a quadratic function from mean and variance", "Medium", "Multi-step computation MCQ",
  r"A random variable $X$ has mean $2$ and variance $3$. Then $E\left[(2X - 1)^2\right]$ equals",
  r"$21$",
  [(r"$12$", r"Computes $\operatorname{Var}(2X - 1) = 4 \cdot 3 = 12$ instead of $E[(2X-1)^2]$."),
   (r"$9$", r"Substitutes the mean: $(2 \cdot 2 - 1)^2 = 9$, as if $E[g(X)] = g(E(X))$."),
   (r"$5$", r"Takes $E(X^2) = \operatorname{Var}(X) = 3$: $4 \cdot 3 - 4 \cdot 2 + 1 = 5$.")],
  r"$E(X^2) = \operatorname{Var}(X) + [E(X)]^2 = 3 + 4 = 7$. Expanding, $E[(2X-1)^2] = 4E(X^2) - 4E(X) + 1 = 28 - 8 + 1 = 21$.",
  r"Assuming $E[g(X)] = g(E[X])$ for a non-linear $g$.",
  "U13-D-rv-moments-transform", "Recover $E(X^2)$, expand, apply linearity.",
  check=_c025, values=[21, 12, 9, 5], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A random variable $X$ has mean $2$ and variance $3$. Then the value of $E\left[(2X - 1)^2\right]$ is", answer=21))


def _c026():
    s1 = total([R_(1, 2), R_(1, 2)], [R_(2, 5), R_(3, 5)]) == R_(1, 2)
    s2 = bayes([R_(1, 2), R_(1, 2)], [R_(2, 5), R_(3, 5)], 1) == R_(3, 5)
    return (bool(s1), bool(s2))


q("U13-D-026", TB, "Total probability and Bayes' theorem together", "Medium", "Statement-based MCQ",
  r"Bag I contains $2$ red and $3$ white balls, and Bag II contains $3$ red and $2$ white balls. A bag is chosen at random and a ball is drawn from it. Statement I: The probability that the ball is red is $\frac{1}{2}$. Statement II: Given that the ball is red, the probability that it came from Bag II is $\frac{3}{5}$." + TAIL,
  ST_TT,
  [(ST_TF, r"Accepts Statement I but rejects Statement II, thinking the posterior must equal the prior $\frac{1}{2}$."),
   (ST_FT, r"Rejects Statement I, perhaps computing $\frac{2}{5} \cdot \frac{3}{5}$, while accepting Statement II."),
   (ST_FF, r"Rejects both, treating the posterior as $\frac{1}{2}$ and the total as a product.")],
  r"Statement I: $P(R) = \frac{1}{2} \cdot \frac{2}{5} + \frac{1}{2} \cdot \frac{3}{5} = \frac{1}{2}$, true. Statement II: $P(\text{II} \mid R) = \frac{\frac{1}{2} \cdot \frac{3}{5}}{\frac{1}{2}} = \frac{3}{5}$, true.",
  r"Believing that equal priors force equal posteriors.",
  "U13-D-statement-total-bayes", "Two short computations, one of each theorem.",
  check=_c026, values=[(True, True), (True, False), (False, True), (False, False)], cognitive="Application", source_class=SC)


def _c027():
    c, k = symbols('c k', positive=True)
    cv = solve(summation(c * R_(1, 3)**k, (k, 1, oo)) - 1, c)[0]
    return summation(cv * R_(1, 3)**k, (k, 3, oo))


q("U13-D-027", RV, "Distribution on infinitely many values", "Medium", "Multi-step computation MCQ",
  r"A random variable $X$ takes the values $1, 2, 3, \ldots$ with $P(X = k) = c\left(\frac{1}{3}\right)^k$, where $c$ is a constant. Then $P(X \ge 3)$ equals",
  r"$\frac{1}{9}$",
  [(r"$\frac{2}{27}$", r"Finds $c = 2$ but computes only $P(X = 3) = \frac{2}{27}$."),
   (r"$\frac{1}{18}$", r"Takes $c = 1$ without normalising: $\sum_{k \ge 3} \left(\frac{1}{3}\right)^k = \frac{1}{18}$."),
   (r"$\frac{1}{3}$", r"Starts the tail sum at $k = 2$, computing $P(X \ge 2) = \frac{1}{3}$.")],
  r"$\sum_{k=1}^{\infty} \left(\frac{1}{3}\right)^k = \frac{1/3}{1 - 1/3} = \frac{1}{2}$, so $c = 2$. Then $P(X \ge 3) = 2 \cdot \frac{(1/3)^3}{1 - 1/3} = 2 \cdot \frac{1}{27} \cdot \frac{3}{2} = \frac{1}{9}$.",
  r"Forgetting to normalise before computing a tail probability.",
  "U13-D-rv-infinite-gp", "Normalise with an infinite GP, then a tail sum.",
  check=_c027, values=[R_(1, 9), R_(2, 27), R_(1, 18), R_(1, 3)], cognitive="Application", source_class=SC)


def _c028():
    seqs = list(itertools.product('HT', repeat=4))

    def tosses(s):
        for i, c in enumerate(s):
            if c == 'H':
                return i + 1
        return 4
    return E(dist_from(seqs, tosses))


q("U13-D-028", RV, "Mean of a stopped experiment", "Medium", "Multi-step computation MCQ",
  r"A fair coin is tossed until a head appears or until it has been tossed $4$ times, whichever happens first. If $X$ is the number of tosses made, then $E(X)$ equals",
  r"$\frac{15}{8}$",
  [(r"$2$", r"Uses the mean $2$ of the unlimited experiment (toss until the first head), ignoring the cap of $4$ tosses."),
   (r"$\frac{13}{8}$", r"Takes $P(X = 4) = \frac{1}{16}$ (only $TTTH$), missing the case $TTTT$, which also gives $X = 4$."),
   (r"$\frac{5}{2}$", r"Treats the values $1, 2, 3, 4$ as equally likely.")],
  r"$P(X=1) = \frac{1}{2}$, $P(X=2) = \frac{1}{4}$, $P(X=3) = \frac{1}{8}$, and $P(X=4) = \frac{1}{8}$ (both $TTTH$ and $TTTT$). So $E(X) = \frac{1}{2} + \frac{2}{4} + \frac{3}{8} + \frac{4}{8} = \frac{15}{8}$.",
  r"Missing an outcome that ends the experiment, so the probabilities do not add to $1$.",
  "U13-D-rv-stopped-tosses", "Construct the distribution with a stopping rule, then the mean.",
  check=_c028, values=[R_(15, 8), 2, R_(13, 8), R_(5, 2)], cognitive="Analysis", source_class=SC)


def _c029():
    p = Symbol('p')
    d = {-1: p, 0: R_(1, 2), 2: R_(1, 2) - p}
    pv = solve(E(d) - R_(1, 4), p)[0]
    d = {x: pr.subs(p, pv) for x, pr in d.items()}
    assert all(0 <= v <= 1 for v in d.values())
    return Var(d)


q("U13-D-029", RV, "Variance with an unknown probability", "Medium", "Multi-step computation MCQ",
  r"A random variable $X$ takes the values $-1, 0, 2$ with $P(X = -1) = p$, $P(X = 0) = \frac{1}{2}$ and $P(X = 2) = \frac{1}{2} - p$. If $E(X) = \frac{1}{4}$, then $\operatorname{Var}(X)$ equals",
  r"$\frac{19}{16}$",
  [(r"$\frac{5}{4}$", r"Finds $p = \frac{1}{4}$ and reports $E(X^2) = \frac{1}{4} + 1 = \frac{5}{4}$ without subtracting the square of the mean."),
   (r"$\frac{21}{16}$", r"Adds the square of the mean: $\frac{5}{4} + \frac{1}{16}$."),
   (r"$\frac{11}{16}$", r"Uses $x$ instead of $x^2$ for the value $-1$ in $E(X^2)$: $-\frac{1}{4} + 1 - \frac{1}{16} = \frac{11}{16}$.")],
  r"$E(X) = -p + 2\left(\frac{1}{2} - p\right) = 1 - 3p = \frac{1}{4}$ gives $p = \frac{1}{4}$. Then $E(X^2) = \frac{1}{4} + 4 \cdot \frac{1}{4} = \frac{5}{4}$ and $\operatorname{Var}(X) = \frac{5}{4} - \frac{1}{16} = \frac{19}{16}$.",
  r"Losing the sign handling when squaring negative values.",
  "U13-D-rv-param-variance", "Solve for the parameter, then the variance.",
  check=_c029, values=[R_(19, 16), R_(5, 4), R_(21, 16), R_(11, 16)], cognitive="Application", source_class=SC)


def _c030():
    return bayes([R_(1, 5), R_(4, 5)], [R_(1, 2), R_(1, 10)], 0)


q("U13-D-030", TB, "Bayes' theorem in an everyday setting", "Medium", "Multi-step computation MCQ",
  r"On any day, it rains with probability $\frac{1}{5}$. A student is late for school with probability $\frac{1}{2}$ on a rainy day and with probability $\frac{1}{10}$ on a day without rain. On a particular day the student is late. The probability that it rained that day is",
  r"$\frac{5}{9}$",
  [(r"$\frac{1}{2}$", r"Reports $P(\text{late} \mid \text{rain})$, reversing the conditioning."),
   (r"$\frac{1}{5}$", r"Keeps the prior probability of rain, ignoring that the student was late."),
   (r"$\frac{9}{50}$", r"Reports the total probability of being late, $\frac{1}{10} + \frac{8}{100}$, as the answer.")],
  r"$P(L) = \frac{1}{5} \cdot \frac{1}{2} + \frac{4}{5} \cdot \frac{1}{10} = \frac{1}{10} + \frac{2}{25} = \frac{9}{50}$. Then $P(\text{rain} \mid L) = \frac{1/10}{9/50} = \frac{5}{9}$.",
  r"Reporting the total probability of the evidence instead of the posterior.",
  "U13-D-bayes-everyday", "Total probability then Bayes.",
  check=_c030, values=[R_(5, 9), R_(1, 2), R_(1, 5), R_(9, 50)], cognitive="Application", source_class=SC)


def _c031():
    deck = ['F'] * 12 + ['N'] * 40
    pairs = list(itertools.combinations(range(52), 2))
    good = sum(1 for i, j in pairs if (deck[i] == 'F') + (deck[j] == 'F') == 1)
    return Rational(good, len(pairs))


q("U13-D-031", RV, "Distribution of the number of face cards", "Medium", "Multi-step computation MCQ",
  r"Two cards are drawn at random without replacement from a well-shuffled pack of $52$ playing cards. If $X$ denotes the number of face cards (jacks, queens and kings) drawn, then $P(X = 1)$ equals",
  r"$\frac{80}{221}$",
  [(r"$\frac{60}{169}$", r"Treats the draws as with replacement: $2 \cdot \frac{12}{52} \cdot \frac{40}{52} = \frac{60}{169}$."),
   (r"$\frac{40}{221}$", r"Finds only the order face card then other card, $\frac{12}{52} \cdot \frac{40}{51}$, and does not double for the reverse order."),
   (r"$\frac{7}{17}$", r"Computes $P(X \ge 1) = 1 - \frac{\binom{40}{2}}{\binom{52}{2}} = \frac{91}{221}$, including the case of two face cards.")],
  r"There are $12$ face cards and $40$ other cards. $P(X = 1) = \frac{\binom{12}{1}\binom{40}{1}}{\binom{52}{2}} = \frac{480}{1326} = \frac{80}{221}$.",
  r"Ignoring that the draws are without replacement, or counting only one order.",
  "U13-D-rv-cards-face", "Combinations without replacement with two tempting shortcuts.",
  check=_c031, values=[R_(80, 221), R_(60, 169), R_(40, 221), R_(7, 17)], cognitive="Application", source_class=SC)


def _c032():
    s1 = R_(3)**2 <= 8  # need E(X^2) >= E(X)^2 for existence
    d = {x: R_(x, 6) for x in (1, 2, 3)}
    s2 = E(d) == R_(7, 3)
    return (bool(s1), bool(s2))


q("U13-D-032", RV, "Consistency of moments", "Medium", "Statement-based MCQ",
  r"Statement I: There exists a random variable $X$ with $E(X) = 3$ and $E(X^2) = 8$. Statement II: If $X$ takes the values $1, 2, 3$ with $P(X = x) = \frac{x}{6}$, then $E(X) = \frac{7}{3}$." + TAIL,
  ST_FT,
  [(ST_TT, r"Accepts Statement I without checking that $\operatorname{Var}(X) = 8 - 9$ would be negative."),
   (ST_TF, r"Accepts Statement I and computes the mean in Statement II as the plain average $2$."),
   (ST_FF, r"Correctly rejects Statement I but uses the plain average $2$ in Statement II.")],
  r"Since $\operatorname{Var}(X) = E(X^2) - [E(X)]^2 \ge 0$, the values in Statement I would give $8 - 9 = -1 < 0$, which is impossible; Statement I is false. In Statement II, $E(X) = \frac{1 \cdot 1 + 2 \cdot 2 + 3 \cdot 3}{6} = \frac{14}{6} = \frac{7}{3}$, true.",
  r"Not checking that $E(X^2) \ge [E(X)]^2$.",
  "U13-D-statement-rv", "Uses non-negativity of variance plus a short computation.",
  check=_c032, values=[(False, True), (True, True), (True, False), (False, False)], cognitive="Analysis", source_class=SC)


def _c033():
    balls = 'RRBBB'
    perms = set(itertools.permutations(balls))
    return E(dist_from(sorted(perms), lambda s: s.index('R') + 1))


q("U13-D-033", RV, "Number of draws until the first success without replacement", "Medium", "Multi-step computation MCQ",
  r"A box contains $2$ red and $3$ black balls. Balls are drawn one at a time at random without replacement until a red ball is drawn. If $X$ is the number of draws made, then $E(X)$ equals",
  r"$2$",
  [(r"$\frac{5}{2}$", r"Treats the draws as with replacement and uses $\frac{1}{p} = \frac{5}{2}$."),
   (r"$\frac{8}{5}$", r"Lists $X = 1, 2, 3$ only, missing $X = 4$ (all three black balls first): $\frac{2}{5} + \frac{6}{10} + \frac{3}{5}$."),
   (r"$1$", r"Computes the expected number of black balls drawn before the first red and forgets to count the red draw itself.")],
  r"$P(X=1) = \frac{2}{5}$, $P(X=2) = \frac{3}{5} \cdot \frac{2}{4} = \frac{3}{10}$, $P(X=3) = \frac{3}{5} \cdot \frac{2}{4} \cdot \frac{2}{3} = \frac{1}{5}$, $P(X=4) = \frac{3}{5} \cdot \frac{2}{4} \cdot \frac{1}{3} = \frac{1}{10}$. So $E(X) = \frac{2}{5} + \frac{6}{10} + \frac{3}{5} + \frac{4}{10} = 2$.",
  r"Using with-replacement reasoning in a without-replacement experiment.",
  "U13-D-rv-draw-until", "Builds a four-value distribution with changing probabilities.",
  check=_c033, values=[2, R_(5, 2), R_(8, 5), 1], cognitive="Application", source_class=SC,
  numerical=dict(question=r"A box contains $2$ red and $3$ black balls. Balls are drawn one at a time at random without replacement until a red ball is drawn. If $X$ is the number of draws made, then $E(X)$ is", answer=2))

# ================================================================ DIFFICULT (12)


def _c034():
    items = ['D'] * 3 + ['G'] * 7
    d = dist_from(list(itertools.combinations(range(10), 2)), lambda c: sum(1 for i in c if items[i] == 'D'))
    return Var(d)


q("U13-D-034", RV, "Variance when drawing without replacement", "Difficult", "Multi-step computation MCQ",
  r"A lot of $10$ items contains $3$ defective items. Two items are drawn at random without replacement. If $X$ is the number of defective items drawn, then $\operatorname{Var}(X)$ equals",
  r"$\frac{28}{75}$",
  [(r"$\frac{21}{50}$", r"Treats the draws as independent (with replacement): $2 \cdot \frac{3}{10} \cdot \frac{7}{10} = \frac{21}{50}$."),
   (r"$\frac{3}{5}$", r"Reports the mean $E(X) = \frac{3}{5}$ instead of the variance."),
   (r"$\frac{11}{15}$", r"Reports $E(X^2) = \frac{33}{45}$ without subtracting $[E(X)]^2$.")],
  r"$P(X=0) = \frac{\binom{7}{2}}{\binom{10}{2}} = \frac{21}{45}$, $P(X=1) = \frac{3 \cdot 7}{45} = \frac{21}{45}$, $P(X=2) = \frac{3}{45}$. So $E(X) = \frac{27}{45} = \frac{3}{5}$, $E(X^2) = \frac{21 + 12}{45} = \frac{11}{15}$, and $\operatorname{Var}(X) = \frac{11}{15} - \frac{9}{25} = \frac{28}{75}$.",
  r"Using an independent-trials variance when the draws are without replacement.",
  "U13-D-rv-without-replacement-variance", "Full distribution, two moments, and a with-replacement trap.",
  check=_c034, values=[R_(28, 75), R_(21, 50), R_(3, 5), R_(11, 15)], cognitive="Analysis", source_class=SC)


def _c035():
    pri = [R_(1, 3)] * 3
    lik = [Integer(1), R_(1, 2)**2, R_(1, 4)**2]
    return bayes(pri, lik, 0)


q("U13-D-035", TB, "Bayes' theorem with repeated tosses", "Difficult", "Multi-step computation MCQ",
  r"A box contains three coins: one with heads on both faces, one fair coin, and one biased coin that shows head with probability $\frac{1}{4}$. A coin is chosen at random and tossed twice, showing head both times. The probability that the chosen coin is the two-headed coin is",
  r"$\frac{16}{21}$",
  [(r"$\frac{1}{3}$", r"Keeps the prior probability of choosing the two-headed coin."),
   (r"$\frac{4}{7}$", r"Uses the evidence of a single head only: $\frac{1}{1 + \frac{1}{2} + \frac{1}{4}} = \frac{4}{7}$."),
   (r"$\frac{4}{5}$", r"Leaves out the biased coin's term in the denominator: $\frac{1}{1 + \frac{1}{4}} = \frac{4}{5}$.")],
  r"The likelihoods of two heads are $1$, $\frac{1}{4}$ and $\frac{1}{16}$, with equal priors $\frac{1}{3}$. Hence $P(\text{two-headed} \mid HH) = \frac{1}{1 + \frac{1}{4} + \frac{1}{16}} = \frac{16}{21}$.",
  r"Using the likelihood of one head when the evidence is two heads.",
  "U13-D-bayes-coins-repeated", "Three hypotheses; the likelihood must be squared for two tosses.",
  check=_c035, values=[R_(16, 21), R_(1, 3), R_(4, 7), R_(4, 5)], cognitive="Analysis", source_class=SC)


def _c036():
    d = dist_from(list(itertools.product(DIE, DIE)), max)
    return E(d)


q("U13-D-036", RV, "Mean of the larger number on two dice", "Difficult", "Multi-step computation MCQ",
  r"Two fair dice are thrown. If $X$ denotes the larger of the two numbers obtained (the common number if they are equal), then $E(X)$ equals",
  r"$\frac{161}{36}$",
  [(r"$\frac{7}{2}$", r"Uses the mean of a single die, ignoring that the larger number favours high values."),
   (r"$\frac{91}{36}$", r"Computes the mean of the smaller number, using $P(X = k) = \frac{13 - 2k}{36}$."),
   (r"$\frac{91}{18}$", r"Counts $2k$ outcomes with maximum $k$, double counting $(k, k)$: $\sum \frac{2k \cdot k}{36} = \frac{182}{36}$.")],
  r"The number of outcomes with larger number $k$ is $k^2 - (k-1)^2 = 2k - 1$, so $P(X = k) = \frac{2k-1}{36}$. Then $E(X) = \frac{1}{36}\sum_{k=1}^{6} k(2k-1) = \frac{2 \cdot 91 - 21}{36} = \frac{161}{36}$.",
  r"Double counting the outcome $(k, k)$ when counting outcomes with maximum $k$.",
  "U13-D-rv-max-dice", "Needs a counting argument for the distribution, then a sum of squares.",
  check=_c036, values=[R_(161, 36), R_(7, 2), R_(91, 36), R_(91, 18)], cognitive="Analysis", source_class=SC)


def _c037():
    pri = [R_(1, 10), R_(9, 10)]
    lik = [R_(9, 10)**2, R_(1, 10)**2]
    return bayes(pri, lik, 0)


q("U13-D-037", TB, "Bayes' theorem with two independent tests", "Difficult", "Multi-step computation MCQ",
  r"$10\%$ of the people in a town have a certain infection. A test detects the infection in $90\%$ of infected people and wrongly shows positive for $10\%$ of uninfected people. A person chosen at random is tested twice, the results of the two tests being independent given the person's actual condition, and both results are positive. If $p$ is the probability that the person is infected, then $p$ equals",
  r"$\frac{9}{10}$",
  [(r"$\frac{1}{2}$", r"Uses only one positive test: $\frac{0.1 \times 0.9}{0.1 \times 0.9 + 0.9 \times 0.1} = \frac{1}{2}$."),
   (r"$\frac{81}{100}$", r"Reports $P(\text{both positive} \mid \text{infected}) = 0.9^2$, reversing the conditioning."),
   (r"$\frac{81}{1000}$", r"Reports the joint probability $0.1 \times 0.81$ without dividing by $P(\text{both positive})$.")],
  r"$P(++ \mid I) = 0.81$ and $P(++ \mid I') = 0.01$. So $p = \frac{0.1 \times 0.81}{0.1 \times 0.81 + 0.9 \times 0.01} = \frac{0.081}{0.090} = \frac{9}{10}$.",
  r"Treating two positive results as no stronger than one.",
  "U13-D-bayes-repeated-test", "Conditional independence, squared likelihoods, then Bayes.",
  check=_c037, values=[R_(9, 10), R_(1, 2), R_(81, 100), R_(81, 1000)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"$10\%$ of the people in a town have a certain infection. A test detects the infection in $90\%$ of infected people and wrongly shows positive for $10\%$ of uninfected people. A person chosen at random is tested twice, the results of the two tests being independent given the person's actual condition, and both results are positive. If $p$ is the probability that the person is infected, then $p$ multiplied by $10$ is", answer=9))


def _c038():
    bag1 = ['W'] * 3 + ['B'] * 2
    num = Integer(0); den = Integer(0)
    pairs = list(itertools.combinations(range(5), 2))
    for pr in pairs:
        moved = [bag1[i] for i in pr]
        bag2 = ['W'] * 2 + ['B'] * 3 + moved
        pw = Rational(bag2.count('W'), len(bag2)) / len(pairs)
        den += pw
        if moved == ['W', 'W']:
            num += pw
    return num / den


q("U13-D-038", TB, "Bayes' theorem after transferring two balls", "Difficult", "Multi-step computation MCQ",
  r"Bag I contains $3$ white and $2$ black balls, and Bag II contains $2$ white and $3$ black balls. Two balls are drawn at random from Bag I and put into Bag II. A ball is then drawn at random from Bag II and is found to be white. The probability that both transferred balls were white is",
  r"$\frac{3}{8}$",
  [(r"$\frac{3}{10}$", r"Reports the prior $\frac{\binom{3}{2}}{\binom{5}{2}} = \frac{3}{10}$ and ignores the white draw."),
   (r"$\frac{9}{16}$", r"Computes the posterior probability that one white and one black ball were transferred."),
   (r"$\frac{1}{16}$", r"Computes the posterior probability that both transferred balls were black.")],
  r"Transfers: two white with probability $\frac{3}{10}$, one of each $\frac{6}{10}$, two black $\frac{1}{10}$; Bag II then gives white with probability $\frac{4}{7}$, $\frac{3}{7}$, $\frac{2}{7}$. So $P(W) = \frac{12 + 18 + 2}{70} = \frac{32}{70}$ and $P(WW \mid W) = \frac{12}{32} = \frac{3}{8}$.",
  r"Mixing up which hypothesis's term goes in the numerator.",
  "U13-D-bayes-transfer", "Three hypotheses from a combinatorial transfer, then Bayes.",
  check=_c038, values=[R_(3, 8), R_(3, 10), R_(9, 16), R_(1, 16)], cognitive="Analysis", source_class=SC)


def _c039():
    bags = [['R'] * 3 + ['B'], ['R'] + ['B'] * 3]
    d = {}
    for bag in bags:
        prs = list(itertools.combinations(range(4), 2))
        for pr in prs:
            v = sum(1 for i in pr if bag[i] == 'R')
            d[v] = d.get(v, 0) + R_(1, 2) * Rational(1, len(prs))
    return Var(d)


q("U13-D-039", RV, "Distribution built from a random choice of bag", "Difficult", "Multi-step computation MCQ",
  r"Bag I contains $3$ red and $1$ black ball, and Bag II contains $1$ red and $3$ black balls. A bag is chosen at random and two balls are drawn from it without replacement. If $X$ is the number of red balls drawn, then $\operatorname{Var}(X)$ equals",
  r"$\frac{1}{2}$",
  [(r"$\frac{1}{4}$", r"Averages the variances within each bag ($\frac{1}{4}$ each), ignoring the spread between the two bags' means."),
   (r"$1$", r"Reports the mean $E(X) = 1$ instead of the variance."),
   (r"$\frac{3}{2}$", r"Reports $E(X^2) = \frac{1}{2} + 4 \cdot \frac{1}{4}$ without subtracting $[E(X)]^2$.")],
  r"From Bag I, $X$ is $1$ or $2$, each with probability $\frac{1}{2}$; from Bag II, $X$ is $0$ or $1$, each with probability $\frac{1}{2}$. By total probability, $P(X=0) = \frac{1}{4}$, $P(X=1) = \frac{1}{2}$, $P(X=2) = \frac{1}{4}$. So $E(X) = 1$, $E(X^2) = \frac{3}{2}$ and $\operatorname{Var}(X) = \frac{1}{2}$.",
  r"Averaging conditional variances instead of finding the distribution by total probability.",
  "U13-D-rv-mixture-variance", "Combines total probability with a variance; the averaging trap is strong.",
  check=_c039, values=[R_(1, 2), R_(1, 4), 1, R_(3, 2)], cognitive="Analysis", source_class=SC)


def _c040():
    a, b, c = symbols('a b c')
    d = {-1: a, 0: b, 1: c}
    mu = E(d)
    s = solve([a + b + c - 1, mu - R_(1, 5), E(d, lambda x: x**2) - mu**2 - R_(16, 25)], [a, b, c], dict=True)[0]
    return s[b]


q("U13-D-040", RV, "Unknown probabilities from the mean and variance", "Difficult", "Inverse/parameter MCQ",
  r"A random variable $X$ takes only the values $-1, 0, 1$. If $E(X) = \frac{1}{5}$ and $\operatorname{Var}(X) = \frac{16}{25}$, then $P(X = 0)$ equals",
  r"$\frac{8}{25}$",
  [(r"$\frac{9}{25}$", r"Uses the variance $\frac{16}{25}$ as $E(X^2)$: $P(X=0) = 1 - \frac{16}{25}$."),
   (r"$\frac{2}{5}$", r"Takes $E(X^2) = \operatorname{Var}(X) - [E(X)]^2 = \frac{15}{25}$ (sign slip), so $P(X=0) = \frac{10}{25}$."),
   (r"$\frac{11}{25}$", r"Solves correctly but reports $P(X = 1) = \frac{11}{25}$.")],
  r"Let $P(X=-1) = a$, $P(X=1) = c$. Then $c - a = \frac{1}{5}$ and $E(X^2) = a + c = \frac{16}{25} + \frac{1}{25} = \frac{17}{25}$. So $P(X = 0) = 1 - (a + c) = \frac{8}{25}$ (with $a = \frac{6}{25}$, $c = \frac{11}{25}$).",
  r"Confusing $\operatorname{Var}(X)$ with $E(X^2)$.",
  "U13-D-rv-unknowns-mean-variance", "Three unknowns from three conditions; the key is $E(X^2) = a + c$.",
  check=_c040, values=[R_(8, 25), R_(9, 25), R_(2, 5), R_(11, 25)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"A random variable $X$ takes only the values $-1, 0, 1$. If $E(X) = \frac{1}{5}$ and $\operatorname{Var}(X) = \frac{16}{25}$, then $P(X = 0)$ multiplied by $25$ is", answer=8))


def _c041():
    pri = [R_(20, 100), R_(30, 100), R_(50, 100)]
    lik = [1 - R_(1, 5), 1 - R_(1, 10), 1 - R_(1, 50)]
    return bayes(pri, lik, 0)


q("U13-D-041", TB, "Bayes' theorem with evidence of no event", "Difficult", "Multi-step computation MCQ",
  r"An insurer classifies drivers as high risk, medium risk and low risk, forming $20\%$, $30\%$ and $50\%$ of its drivers. The probabilities that a driver of these classes has an accident in a year are $\frac{1}{5}$, $\frac{1}{10}$ and $\frac{1}{50}$ respectively. A driver chosen at random had no accident in the year. The probability that the driver is high risk is",
  r"$\frac{4}{23}$",
  [(r"$\frac{1}{2}$", r"Uses the accident probabilities as the likelihoods, computing $P(\text{high} \mid \text{accident}) = \frac{0.04}{0.08}$."),
   (r"$\frac{1}{5}$", r"Keeps the prior $20\%$, thinking that no accident gives no information."),
   (r"$\frac{4}{25}$", r"Reports the joint probability $0.2 \times 0.8$ without dividing by $P(\text{no accident}) = 0.92$.")],
  r"$P(N) = 0.2 \times 0.8 + 0.3 \times 0.9 + 0.5 \times 0.98 = 0.16 + 0.27 + 0.49 = 0.92$. So $P(\text{high} \mid N) = \frac{0.16}{0.92} = \frac{4}{23}$.",
  r"Using the probabilities of the event instead of its complement as likelihoods.",
  "U13-D-bayes-complement-evidence", "Three hypotheses with complementary likelihoods; easy to use the wrong ones.",
  check=_c041, values=[R_(4, 23), R_(1, 2), R_(1, 5), R_(4, 25)], cognitive="Analysis", source_class=SC)


def _c042():
    d = dist_from(list(itertools.combinations(range(1, 7), 3)), sum)
    return Var(d)


q("U13-D-042", RV, "Variance of a sum drawn without replacement", "Difficult", "Multi-step computation MCQ",
  r"Three numbers are chosen at random, without replacement, from $\{1, 2, 3, 4, 5, 6\}$. If $X$ is the sum of the three numbers chosen, then $\operatorname{Var}(X)$ equals",
  r"$\frac{21}{4}$",
  [(r"$\frac{35}{4}$", r"Adds the variances of three independent draws, $3 \cdot \frac{35}{12} = \frac{35}{4}$, which is valid only with replacement."),
   (r"$\frac{35}{12}$", r"Gives the variance of a single number chosen from $\{1, 2, \ldots, 6\}$."),
   (r"$\frac{21}{2}$", r"Finds $\sum f(x - \frac{21}{2})^2 = 105$ correctly but divides by the $10$ distinct sums instead of the $20$ equally likely selections.")],
  r"There are $\binom{6}{3} = 20$ equally likely selections. The sums $6, 7, \ldots, 15$ occur $1, 1, 2, 3, 3, 3, 3, 2, 1, 1$ times; the distribution is symmetric (a selection and its complement have sums adding to $21$), so $E(X) = \frac{21}{2}$. The deviations $\pm\frac{9}{2}, \pm\frac{7}{2}, \pm\frac{5}{2}, \pm\frac{3}{2}, \pm\frac{1}{2}$ have frequencies $1, 1, 2, 3, 3$ on each side, so $\sum f(x - \frac{21}{2})^2 = 2\left(\frac{81}{4} + \frac{49}{4} + 2 \cdot \frac{25}{4} + 3 \cdot \frac{9}{4} + 3 \cdot \frac{1}{4}\right) = 105$. Hence $\operatorname{Var}(X) = \frac{105}{20} = \frac{21}{4}$.",
  r"Adding variances for dependent draws.",
  "U13-D-rv-sum-drawn", "Twenty selections to organise into a ten-value distribution, symmetry to get the mean, and the independence trap; about 3 minutes.",
  check=_c042, values=[R_(21, 4), R_(35, 4), R_(35, 12), R_(21, 2)], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"Three numbers are chosen at random, without replacement, from $\{1, 2, 3, 4, 5, 6\}$. If $X$ is the sum of the three numbers chosen, then $4\operatorname{Var}(X)$ is", answer=21))


def _c043():
    n, k = symbols('n k', positive=True, integer=True)
    c = 1 / summation(1 / (k * (k + 1)), (k, 1, n))
    tail = simplify(c * summation(1 / (k * (k + 1)), (k, 2, n)))
    sols = [s for s in solve(Eq(tail, Rational(9, 20)), n) if s.is_integer and s > 0]
    # brute-force confirmation over a range of n
    hits = [m for m in range(1, 200)
            if sum(Rational(1, j * (j + 1)) for j in range(2, m + 1)) / sum(Rational(1, j * (j + 1)) for j in range(1, m + 1)) == Rational(9, 20)]
    assert hits == sols
    return sols[0]


q("U13-D-043", RV, "Finding the range of a distribution from a tail probability", "Difficult", "Inverse/parameter MCQ",
  r"For a positive integer $n \ge 2$, a random variable $X$ takes the values $1, 2, \ldots, n$ with $P(X = k) = \frac{c}{k(k+1)}$, where $c$ is a constant. If $P(X \ge 2) = \frac{9}{20}$, then $n$ equals",
  r"$10$",
  [(r"$19$", r"Forgets to normalise and takes $c = 1$: $\frac{1}{2} - \frac{1}{n+1} = \frac{9}{20}$ gives $n + 1 = 20$."),
   (r"$9$", r"Telescopes the total as $1 - \frac{1}{n}$ (one term short), so $c = \frac{n}{n-1}$ and $P(X \ge 2) = \frac{n}{n-1}\left(\frac{1}{2} - \frac{1}{n+1}\right) = \frac{n}{2(n+1)} = \frac{9}{20}$."),
   (r"$8$", r"Telescopes the tail as $\frac{1}{2} - \frac{1}{n+2}$ (one term too many), so $P(X \ge 2) = \frac{n+1}{n} \cdot \frac{n}{2(n+2)} = \frac{n+1}{2(n+2)} = \frac{9}{20}$.")],
  r"Since $\frac{1}{k(k+1)} = \frac{1}{k} - \frac{1}{k+1}$, the total is $c\left(1 - \frac{1}{n+1}\right) = \frac{cn}{n+1} = 1$, so $c = \frac{n+1}{n}$. Then $P(X \ge 2) = c\left(\frac{1}{2} - \frac{1}{n+1}\right) = \frac{n+1}{n} \cdot \frac{n-1}{2(n+1)} = \frac{n-1}{2n}$. Setting $\frac{n-1}{2n} = \frac{9}{20}$ gives $20n - 20 = 18n$, so $n = 10$.",
  r"Skipping the normalisation of $c$, or slipping by one term in a telescoping sum.",
  "U13-D-rv-pmf-telescoping-find-n", "Normalisation needs a telescoping sum with general $n$; a second telescoping sum for the tail; then solve, with two off-by-one traps.",
  check=_c043, values=[10, 19, 9, 8], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"For a positive integer $n \ge 2$, a random variable $X$ takes the values $1, 2, \ldots, n$ with $P(X = k) = \frac{c}{k(k+1)}$, where $c$ is a constant. If $P(X \ge 2) = \frac{9}{20}$, then $n$ is", answer=10))


def _c044():
    pH = Rational(sum(1 for v in DIE if v <= 3), 6)
    pT = Rational(sum(1 for a, b in itertools.product(DIE, DIE) if a + b <= 3), 36)
    return bayes([R_(1, 2), R_(1, 2)], [pH, pT], 0)


q("U13-D-044", TB, "Bayes' theorem with a two-stage experiment", "Difficult", "Multi-step computation MCQ",
  r"A fair coin is tossed. If it shows head, a fair die is thrown once and $X$ is the number shown; if it shows tail, a fair die is thrown twice and $X$ is the sum of the two numbers. Given that $X \le 3$, the probability that the coin showed head is",
  r"$\frac{6}{7}$",
  [(r"$\frac{1}{2}$", r"Keeps the prior probability of head and ignores the information $X \le 3$."),
   (r"$\frac{7}{24}$", r"Reports the total probability $P(X \le 3) = \frac{1}{4} + \frac{1}{24}$ instead of the posterior."),
   (r"$\frac{1}{7}$", r"Computes the posterior probability of tail instead of head.")],
  r"$P(X \le 3 \mid H) = \frac{3}{6} = \frac{1}{2}$ and $P(X \le 3 \mid T) = \frac{3}{36} = \frac{1}{12}$ (outcomes $(1,1), (1,2), (2,1)$). So $P(X \le 3) = \frac{1}{4} + \frac{1}{24} = \frac{7}{24}$ and $P(H \mid X \le 3) = \frac{1/4}{7/24} = \frac{6}{7}$.",
  r"Not computing the likelihoods separately for the two branches.",
  "U13-D-bayes-two-stage", "Two different sample spaces combined by total probability, then Bayes.",
  check=_c044, values=[R_(6, 7), R_(1, 2), R_(7, 24), R_(1, 7)], cognitive="Analysis", source_class=SC)


def _c045():
    x = Symbol('x')
    balls = ['W'] * 3 + ['R'] * 2
    pay = {0: 0, 1: 20, 2: 60}
    d1 = dist_from(list(itertools.combinations(range(5), 1)), lambda c: sum(1 for i in c if balls[i] == 'R'))
    d2 = dist_from(list(itertools.combinations(range(5), 2)), lambda c: sum(1 for i in c if balls[i] == 'R'))
    ev = R_(1, 2) * E(d1, lambda v: pay[v]) + R_(1, 2) * E(d2, lambda v: pay[v])
    return solve(ev - x, x)[0]


q("U13-D-045", RV, "Fair entry fee from a two-stage game", "Difficult", "Inverse/parameter MCQ",
  r"A bag contains $3$ white and $2$ red balls. A player pays Rs $x$ to play the following game. A fair coin is tossed; if it shows head, one ball is drawn at random from the bag, and if it shows tail, two balls are drawn together at random from the bag. The player receives Rs $20$ if exactly one red ball is drawn, Rs $60$ if two red balls are drawn, and nothing otherwise. If the game is fair (the expected net gain of the player is zero), then $x$ equals",
  r"$13$",
  [(r"$12$", r"Pays Rs $20$ per red ball (Rs $40$ for two reds) instead of Rs $60$: $20 \cdot \frac{3}{5} = 12$."),
   (r"$18$", r"Ignores the coin and always draws two balls: $20 \cdot \frac{6}{10} + 60 \cdot \frac{1}{10} = 18$."),
   (r"$26$", r"Adds the two branch expectations $8$ and $18$ without weighting each by $\frac{1}{2}$.")],
  r"Let $W$ be the amount received. Head branch: $P(\text{one red}) = \frac{2}{5}$, so the expected receipt is $8$. Tail branch: $P(\text{one red}) = \frac{3 \cdot 2}{10} = \frac{6}{10}$ and $P(\text{two red}) = \frac{1}{10}$, so the expected receipt is $12 + 6 = 18$. By total probability, $P(W = 20) = \frac{1}{2} \cdot \frac{2}{5} + \frac{1}{2} \cdot \frac{6}{10} = \frac{1}{2}$ and $P(W = 60) = \frac{1}{20}$, so $E(W) = 10 + 3 = 13$. Fairness needs $x = E(W) = 13$.",
  r"Treating the payout as linear in the number of red balls, or not weighting the two branches.",
  "U13-D-rv-fair-game-two-stage", "Total probability over two branches with different sample spaces, then a nonlinear payout distribution and an expectation equation; about 3 minutes.",
  check=_c045, values=[13, 12, 18, 26], cognitive="Analysis", source_class=SC,
  numerical=dict(question=r"A bag contains $3$ white and $2$ red balls. A player pays Rs $x$ to play the following game. A fair coin is tossed; if it shows head, one ball is drawn at random from the bag, and if it shows tail, two balls are drawn together at random from the bag. The player receives Rs $20$ if exactly one red ball is drawn, Rs $60$ if two red balls are drawn, and nothing otherwise. If the game is fair (the expected net gain of the player is zero), then $x$ is", answer=13))
