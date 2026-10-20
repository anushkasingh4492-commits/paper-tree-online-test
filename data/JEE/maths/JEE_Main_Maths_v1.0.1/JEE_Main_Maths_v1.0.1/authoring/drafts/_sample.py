import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qlib import *

def _c1():
    z = (3 + 4*I) / (1 - 2*I)
    return Abs(z)
q("U02-X-001", "Modulus and argument", "Modulus of a quotient", "Easy", "Single-step computation MCQ",
  r"If $z = \frac{3+4i}{1-2i}$, then $|z|$ equals",
  r"$\sqrt{5}$",
  [(r"$5$", "Takes the modulus of the numerator only."),
   (r"$\frac{5}{3}$", "Divides by 3, using 1+2 instead of the modulus of the denominator."),
   (r"$5\sqrt{5}$", "Multiplies the moduli instead of dividing.")],
  r"$|z| = \frac{|3+4i|}{|1-2i|} = \frac{5}{\sqrt{5}} = \sqrt{5}$.",
  "Treating the modulus of a quotient as the modulus of the numerator.",
  "U02-modulus-quotient", "One property of modulus applied once.",
  check=_c1, values=[sqrt(5), 5, Rational(5,3), 5*sqrt(5)], cognitive="Application")

q("U02-X-002", "Roots and coefficients", "Sum of squares of roots", "Medium", "Multi-step computation MCQ",
  r"If $\alpha$ and $\beta$ are the roots of $x^2 - 5x + 3 = 0$, then $\alpha^2 + \beta^2$ equals",
  r"$19$",
  [(r"$31$", "Adds 2 alpha beta."), (r"$25$", "Squares the sum only."), (r"$22$", "Subtracts the product once.")],
  r"$\alpha+\beta=5$, $\alpha\beta=3$, so $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta=25-6=19$.",
  "Forgetting the cross term.", "U02-symmetric-sum-squares", "Two identities.",
  check=lambda: sum(r**2 for r in solve(Symbol('x')**2-5*Symbol('x')+3)), values=[19,31,25,22],
  numerical=dict(question=r"If $\alpha$ and $\beta$ are the roots of $x^2 - 5x + 3 = 0$, then the value of $\alpha^2 + \beta^2$ is", answer=19))
