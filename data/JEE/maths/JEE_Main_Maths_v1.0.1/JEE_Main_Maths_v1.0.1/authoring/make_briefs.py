# -*- coding: utf-8 -*-
"""Generate scope briefs and the batch plan for Units 1 and 3 to 14."""
import json, os

UNITS = {}

def unit(n, name, branch, official, inscope, outscope, batches):
    UNITS[n] = dict(name=name, branch=branch, official=official, inscope=inscope, outscope=outscope, batches=batches)

# batches: (letter, size, {class: count}, topic text)
unit(1, "Sets, Relations and Functions", "Algebra",
 "Sets and their representation; Union, intersection and complement of sets and their algebraic properties; Power set; Relations, type of relations, equivalence relations, functions; one-one, into and onto functions, the composition of functions.",
 ["Roster/set-builder forms, subsets, power set and its size, union/intersection/complement/difference, De Morgan and other algebraic laws, Venn-diagram counting n(A union B) and three-set counting",
  "Cartesian product, relations as subsets, domain and range of a relation, number of relations, reflexive/symmetric/transitive/equivalence relations, equivalence classes, counting relations with given properties on small sets",
  "Functions as relations, domain/range for simple functions, one-one, many-one, into, onto, bijective, counting functions/injections/surjections between finite sets, composition f o g and its domain, invertibility of a bijection"],
 ["Inverse trigonometric functions (Unit 14)", "limits/continuity (Unit 7)", "binary operations", "detailed graphs of functions (Unit 7)"],
 [("A", 47, {"XI": 47}, "Sets: representation, subsets, power sets, operations and laws, Venn diagram and cardinality problems (two and three sets, maximum/minimum overlap)."),
  ("B", 47, {"XI": 13, "XII": 34}, "Relations: Cartesian products, number of relations, domain/range (tag these XI); reflexive, symmetric, transitive, equivalence relations, equivalence classes, counting relations with properties on small sets (tag these XII)."),
  ("C", 46, {"XII": 46}, "Functions: one-one, onto, bijective, into; counting functions, injections and surjections between finite sets; composition of functions and composite domain; invertibility of bijections and finding inverses of simple functions.")])

unit(3, "Matrices and Determinants", "Algebra",
 "Matrices, algebra of matrices, type of matrices, determinants and matrices of order two and three, evaluation of determinants, area of triangles using determinants; Adjoint and inverse of a square matrix; Test of consistency and solution of simultaneous linear equations in two or three variables using matrices.",
 ["Order, types (diagonal, scalar, identity, triangular, symmetric, skew-symmetric, orthogonal via A A^T = I, idempotent, nilpotent, involutory), transpose, algebra, powers of matrices, trace, commuting matrices",
  "Determinants of order 2 and 3, properties, evaluation by properties, |kA|, |AB|, |A^T|, determinant equations, area of a triangle and collinearity",
  "Minors, cofactors, adjoint, inverse, |adj A| = |A|^(n-1), adj(adj A), (AB)^-1, inverse via A^2 relations (Cayley-Hamilton style identities for 2x2 given as stated facts only)",
  "Systems in 2 or 3 variables: consistency, unique/infinitely many/no solution, parameter values, homogeneous systems and non-trivial solutions, matrix method"],
 ["Rank of a matrix by name", "eigenvalues by name", "Cramer's rule is allowed only as a method; no 4x4 determinants"],
 [("A", 55, {"XII": 55}, "Matrix algebra and types of matrices: products, powers (including patterns like A^n), transpose, symmetric/skew-symmetric decomposition, trace, idempotent/nilpotent/involutory/orthogonal conditions, counting matrices with given entries and properties."),
  ("B", 55, {"XII": 55}, "Determinants: evaluation (order 2 and 3), properties, factorised determinants, determinant equations, |kA|, |AB|, area of triangles and collinearity using determinants."),
  ("C", 55, {"XII": 55}, "Adjoint and inverse: cofactors, adj A, inverse, |adj A|, |adj(adj A)|, inverse of products, solving for matrices using inverses, matrix equations."),
  ("D", 55, {"XII": 55}, "Systems of linear equations in 2 or 3 variables: consistency tests, unique/infinite/no solution, parameter values, homogeneous systems with non-trivial solutions, solving by the matrix method.")])

unit(4, "Permutations and Combinations", "Algebra",
 "The fundamental principle of counting, permutations and combinations; Meaning of P(n, r) and C(n, r). Simple applications.",
 ["Fundamental principle of counting, permutations with and without repetition, arrangements with identical objects, restrictions (together/never together/fixed positions), digit and word formation, rank of a word in dictionary order",
  "Combinations, properties of C(n, r), selections with restrictions, committees, at least/at most, geometric counting (lines, triangles, diagonals), number of divisors, distribution into groups of given sizes, simple identical-object distributions via selection"],
 ["Circular permutations beyond a one-line note (avoid)", "derangement formula", "multinomial/generating functions", "inclusion-exclusion beyond three sets", "probability (Unit 13)"],
 [("A", 54, {"XI": 54}, "Fundamental principle of counting and permutations: arrangements with restrictions, identical objects, digit/number formation with divisibility conditions, word formation, rank of a word, P(n, r) identities and equations."),
  ("B", 53, {"XI": 53}, "Combinations: C(n, r) properties and equations, selections with restrictions, committees, at least/at most, geometric counting (points, lines, triangles, diagonals, rectangles in a grid), divisors."),
  ("C", 53, {"XI": 53}, "Mixed applications combining selection and arrangement: select-then-arrange, division into groups, distributing distinct objects, arrangements with gaps method, counting with complementary counting, integer solutions of x1 + x2 + ... = n (stars and bars as a selection argument).")])

unit(5, "Binomial Theorem and its Simple Applications", "Algebra",
 "Binomial theorem for a positive integral index, general term and middle term and simple applications.",
 ["Expansion for positive integer index, general term, specific coefficients, term independent of x, middle term(s), number of terms, coefficients in products like (1 + x)^m (1 - x)^n",
  "Sum of binomial coefficients and simple coefficient identities, numerically greatest term only in simple cases, remainder and divisibility applications, last digits, approximations, comparison of large numbers, rational terms in expansions involving surds"],
 ["Binomial theorem for negative or fractional index", "multinomial theorem", "summations requiring calculus beyond basic"],
 [("A", 47, {"XI": 47}, "General term and specific coefficients: term independent of x, coefficient of x^k, ratio of consecutive coefficients, terms in products of two binomials, number of rational terms."),
  ("B", 47, {"XI": 47}, "Middle terms, number of terms, sums of coefficients, alternating sums, simple binomial coefficient identities (sum of C(n,r), sum of C(n,r)^2 via coefficient comparison), greatest coefficient."),
  ("C", 46, {"XI": 46}, "Simple applications: remainders and divisibility (e.g. 7^103 mod 25), last two digits, approximations, comparing 1.01^1000 with 2 type questions, integral and fractional parts of (a + sqrt b)^n.")])

unit(6, "Sequence and Series", "Algebra",
 "Arithmetic and Geometric progressions, insertion of arithmetic, geometric means between two given numbers, Relation between A.M and G.M.",
 ["AP: nth term, sum of n terms, properties, conditions for terms in AP, problems with S_n given as a function of n",
  "GP: nth term, sum of n terms, sum to infinity for |r| < 1, properties, recurring decimals as GP",
  "Insertion of arithmetic and geometric means, relation between AM and GM, AM-GM inequality for minimum/maximum problems, mixed AP-GP problems"],
 ["Harmonic progression as a separate topic", "arithmetico-geometric series", "sums of n^2, n^3 and method of differences", "Sigma of special series"],
 [("A", 60, {"XI": 60}, "Arithmetic progressions: nth term, S_n, S_n as a quadratic in n, terms in AP conditions, word problems, mixed conditions on terms and sums."),
  ("B", 60, {"XI": 60}, "Geometric progressions: nth term, finite sums, infinite sums, recurring decimals, products of terms, conditions for terms in GP."),
  ("C", 60, {"XI": 60}, "Inserting arithmetic and geometric means, AM-GM relation and inequality (minimum values, constraints), problems mixing AP and GP (three numbers in AP become GP after changes, etc.).")])

unit(7, "Limit, Continuity and Differentiability", "Calculus",
 "Real-valued functions, algebra of functions; polynomial, rational, trigonometric, logarithmic and exponential functions; inverse functions. Graphs of simple functions. Limits, continuity and differentiability. Differentiation of the sum, difference, product and quotient of two functions. Differentiation of trigonometric, inverse trigonometric, logarithmic, exponential, composite and implicit functions; derivatives of order upto two, Applications of derivatives: Rate of change of quantities, monotonic-Increasing and decreasing functions, Maxima and minima of functions of one variable.",
 ["Real functions: domain, range, algebra of functions, even/odd, periodicity of simple functions, inverse of a function, graphs of simple functions (modulus, greatest integer, signum, exponential, log)",
  "Limits: algebraic, trigonometric, exponential and logarithmic standard limits, 1^infinity form, left and right limits, limits at infinity",
  "Continuity and differentiability at a point and on intervals, piecewise functions, greatest integer and modulus functions, parameter values for continuity/differentiability",
  "Differentiation rules, chain rule, implicit, inverse trigonometric, logarithmic differentiation, second derivatives",
  "Applications: rate of change, increasing/decreasing, local and absolute maxima/minima of one-variable functions"],
 ["Parametric differentiation (not listed)", "L'Hospital's rule may be used in solutions but not named as required", "tangents and normals (not listed)", "Rolle's and mean value theorems (not listed)", "approximations by differentials"],
 [("A", 56, {"XI": 28, "XII": 28}, "Real-valued functions: domains and ranges of polynomial, rational, root, log, exponential and trigonometric expressions (tag XI); inverse functions, composition-based graphs, even/odd and periodic functions, graphs of modulus/greatest integer/signum (tag XII)."),
  ("B", 52, {"XI": 52}, "Limits: algebraic factorisation and rationalisation, standard trigonometric, exponential and logarithmic limits, 1^infinity form, limits at infinity, left/right limits with greatest integer and modulus, finding parameters from limit values."),
  ("C", 57, {"XII": 57}, "Continuity and differentiability: continuity at a point, removable discontinuities, piecewise functions with parameters, greatest integer and modulus functions, number of points of discontinuity/non-differentiability on an interval, differentiability of products like |x| g(x)."),
  ("D", 57, {"XII": 57}, "Differentiation: product, quotient and chain rules, implicit differentiation, inverse trigonometric functions (with simplifying substitutions), logarithmic differentiation, second derivatives and relations like y'' + y = 0, derivative of one function with respect to another only via chain rule."),
  ("E", 58, {"XII": 58}, "Applications of derivatives: rates of change in geometry contexts, intervals of increase/decrease, parameter for monotonicity, local maxima/minima, absolute extrema on closed intervals, optimisation problems (areas, volumes, distances).")])

unit(8, "Integral Calculus", "Calculus",
 "Integral as an anti-derivative, Fundamental integrals involving algebraic, trigonometric, exponential and logarithmic functions. Integration by substitution, by parts and by partial fractions. Integration using trigonometric identities. Evaluation of simple integrals of the type dx/(x^2 +/- a^2), dx/sqrt(x^2 +/- a^2), dx/(a^2 - x^2), dx/sqrt(a^2 - x^2), dx/(ax^2 + bx + c), dx/sqrt(ax^2 + bx + c), (px + q)/(ax^2 + bx + c) dx, (px + q)/sqrt(ax^2 + bx + c) dx, sqrt(a^2 +/- x^2) dx, sqrt(x^2 - a^2) dx. The fundamental theorem of calculus, properties of definite integrals. Evaluation of definite integrals, determining areas of the regions bounded by simple curves in standard forms.",
 ["Indefinite integrals: fundamental integrals, substitution, trigonometric identities, by parts, e^x(f + f') form, partial fractions, the listed special forms",
  "Definite integrals: fundamental theorem, properties (King's property, even/odd, periodicity, splitting at points of non-smoothness), greatest integer and modulus integrands, derivative of an integral with variable limits",
  "Areas bounded by simple curves: lines, parabolas, circles, ellipses, modulus curves, between two curves"],
 ["Reduction formulae", "definite integral as a limit of a sum (avoid)", "Walli's formula by name", "double integrals"],
 [("A", 56, {"XII": 56}, "Indefinite integrals by fundamental formulas and substitution (including trig substitutions and integrals using trigonometric identities such as sin^m cos^n with simple powers)."),
  ("B", 56, {"XII": 56}, "Indefinite integrals by parts (including e^x(f + f') and log/inverse-trig integrands) and by partial fractions."),
  ("C", 56, {"XII": 56}, "The listed special integrals: 1/(x^2 +/- a^2), 1/sqrt(...), 1/(ax^2+bx+c), (px+q)/(ax^2+bx+c), (px+q)/sqrt(ax^2+bx+c), sqrt(a^2 +/- x^2), sqrt(x^2 - a^2); include questions where the answer is a parameter or a function value f(x) given f(0)."),
  ("D", 56, {"XII": 56}, "Definite integrals: fundamental theorem, King's property, even/odd and periodic properties, modulus and greatest-integer integrands, derivatives of integrals with variable limits, finding f from an integral equation, limits evaluated via known integrals only if stated."),
  ("E", 56, {"XII": 56}, "Areas of regions bounded by simple curves: under curves, between a line and a parabola, between two parabolas, circle and line, ellipse, modulus curves, regions defined by inequalities; parameter values for a given area.")])

unit(9, "Differential Equations", "Calculus",
 "Ordinary differential equations, their order and degree, the solution of differential equation by the method of separation of variables, solution of a homogeneous and linear differential equation.",
 ["Order and degree (including when degree is undefined)", "variables separable, including substitutions reducing to separable", "homogeneous equations", "linear first-order equations, integrating factor", "simple applications (growth/decay, curves with given slope property) solved by these methods"],
 ["Formation of differential equations by eliminating constants (not listed)", "Bernoulli equations", "exact equations", "second-order equations"],
 [("A", 47, {"XII": 47}, "Order and degree; variables separable equations, including those needing a substitution like y = vx is NOT used here (that is batch B) but substitutions like x + y = t are allowed; particular solutions through a point."),
  ("B", 47, {"XII": 47}, "Homogeneous differential equations: identifying homogeneity, solving with y = vx, particular solutions, curves through given points."),
  ("C", 46, {"XII": 46}, "Linear first-order equations: integrating factor, solutions, values y(a) from initial conditions, equations linear in x, simple applications (growth, decay, cooling given as an ODE, slope conditions on curves).")])

unit(10, "Co-ordinate Geometry", "Coordinate Geometry",
 "Cartesian system of rectangular coordinates in a plane, distance formula, sections formula, locus and its equation, the slope of a line, parallel and perpendicular lines, intercepts of a line on the co-ordinate axis. Straight line: Various forms of equations of a line, intersection of lines, angles between two lines, conditions for concurrence of three lines, the distance of a point from a line, co-ordinate of the centroid, orthocentre and circumcentre of a triangle. Circle, conic sections: A standard form of equations of a circle, the general form of the equation of a circle, its radius and centre, equation of a circle when the endpoints of a diameter are given, points of intersection of a line and a circle with the centre at the origin and sections of conics, equations of conic sections (parabola, ellipse and hyperbola) in standard forms.",
 ["Distance, section formula, locus, slope, parallel/perpendicular, intercepts, centroid/orthocentre/circumcentre/incentre of a triangle, area of triangle by coordinates",
  "Lines: all standard forms, intersection, angle between lines, concurrency, distance of a point from a line, distance between parallel lines, foot of perpendicular and image of a point in a line, family of lines through an intersection",
  "Circles: standard and general forms, centre and radius, diameter form, circle through three points, intersection of a line with a circle centred at the origin (including the tangency condition c^2 = a^2(1 + m^2) derived from intersection), position of a point",
  "Parabola, ellipse, hyperbola in standard forms: focus, directrix, vertex, axes, eccentricity, latus rectum, focal distances, identifying a conic from its equation, finding equation from given data, intersection of a line with a conic as a quadratic"],
 ["Tangents and normals to conics as a separate theory (not listed)", "chord of contact, pole/polar", "family of circles and radical axis", "parametric forms beyond simple use", "pair of straight lines", "rotation of axes"],
 [("A", 50, {"XI": 50}, "Cartesian basics: distance and section formulas, locus equations, slopes, parallel and perpendicular conditions, intercepts, area of a triangle, centroid, circumcentre, orthocentre and incentre."),
  ("B", 50, {"XI": 50}, "Straight lines: forms of equations, intersection, angle between lines, concurrency, distance from a point, distance between parallel lines, foot of the perpendicular, image of a point, lines through an intersection satisfying a condition."),
  ("C", 50, {"XI": 50}, "Circles: standard and general forms, centre and radius, diameter form, circle through given points, intersection with lines through a circle centred at the origin, length of chord, conditions for touching, position of a point."),
  ("D", 50, {"XI": 50}, "Parabola in standard forms y^2 = +/-4ax, x^2 = +/-4ay, and shifted forms: focus, directrix, vertex, latus rectum, focal distance, equation from data, intersection with lines."),
  ("E", 50, {"XI": 50}, "Ellipse in standard form: foci, eccentricity, directrices, latus rectum, focal distances (sum = 2a), equation from data, intersection with lines, points on the ellipse."),
  ("F", 50, {"XI": 50}, "Hyperbola in standard forms: foci, eccentricity, directrices, latus rectum, asymptotes as a property of the standard form, rectangular hyperbola, conjugate hyperbola, focal distance difference, equation from data, identifying conics from second-degree equations in standard position.")])

unit(11, "Three Dimensional Geometry", "Vectors and 3D Geometry",
 "Coordinates of a point in space, the distance between two points, section formula, direction ratios and direction cosines and the angle between two intersecting lines. Equation of a line; Skew lines, the shortest distance between them and its equation.",
 ["Coordinates, distance, section formula, centroid in space, direction ratios and cosines (l^2 + m^2 + n^2 = 1), angle between two lines",
  "Equation of a line in vector and Cartesian forms, point on a line, foot of perpendicular from a point to a line, image of a point in a line, intersection of two lines, collinearity",
  "Skew lines, shortest distance between two lines (skew and parallel), condition for coplanarity/intersection of two lines, equation of the line of shortest distance (only in simple cases)"],
 ["Planes (not in the 2026 syllabus): no plane equations, angle between line and plane, distance from a plane", "spheres"],
 [("A", 47, {"XII": 47}, "Points in space: distance, section formula, centroid, direction ratios and direction cosines, angle between lines given by direction ratios, angles made with axes."),
  ("B", 47, {"XII": 47}, "Equation of a line in vector and Cartesian forms, points on lines, foot of perpendicular and image of a point in a line, intersection point of two lines, parameter for intersection, angle between two lines."),
  ("C", 46, {"XII": 46}, "Skew lines: shortest distance between skew lines and between parallel lines, deciding skew/intersecting/parallel, parameter values for intersecting lines, line of shortest distance in simple cases.")])

unit(12, "Vector Algebra", "Vectors and 3D Geometry",
 "Vectors and scalars, the addition of vectors, components of a vector in two dimensions and three-dimensional spaces, scalar and vector products.",
 ["Vectors and scalars, addition, components, position vectors, section formula, unit vectors, collinearity, linear combinations",
  "Scalar product: angle, projection, perpendicularity, |a + b| and |a - b| relations, work-type applications",
  "Vector product: area of parallelogram and triangle, unit vector perpendicular to two vectors, |a x b|^2 + (a.b)^2 = |a|^2|b|^2, solving simple vector equations using cross product"],
 ["Scalar triple product and vector triple product (not listed)", "coplanarity via triple products", "reciprocal systems"],
 [("A", 54, {"XII": 54}, "Vector basics: addition, components, position vectors, section formula, unit vectors, collinearity of points, linear combinations, magnitudes."),
  ("B", 53, {"XII": 53}, "Scalar (dot) product: angle between vectors, projections, perpendicularity conditions, magnitudes of sums and differences, vectors at given angles, parameter questions."),
  ("C", 53, {"XII": 53}, "Vector (cross) product: areas of triangles and parallelograms, perpendicular unit vectors, Lagrange identity, simple vector equations like a x r = b, combined dot and cross product questions.")])

unit(13, "Statistics and Probability", "Statistics and Probability",
 "Measures of dispersion; calculation of mean, median, mode of grouped and ungrouped data, calculation of standard deviation, variance and mean deviation for grouped and ungrouped data. Probability: Probability of an event, addition and multiplication theorems of probability, Baye's theorem, probability distribution of a random variable.",
 ["Mean, median, mode of grouped and ungrouped data, mean deviation about mean/median, variance and standard deviation, effect of change of origin and scale, combined mean and variance, corrected values after a wrong observation",
  "Probability of events, addition theorem, multiplication theorem, conditional probability, independent events",
  "Total probability and Bayes' theorem, probability distribution of a discrete random variable, its mean and variance"],
 ["Binomial distribution by name (the 2026 syllabus does not list it); Bernoulli trials only as a plain probability calculation", "correlation and regression", "continuous distributions", "coefficient of variation is allowed as a ratio only"],
 [("A", 45, {"XI": 45}, "Measures of central tendency for grouped and ungrouped data: mean, median, mode, combined mean, effect of changes in data, missing frequencies."),
  ("B", 45, {"XI": 45}, "Dispersion: mean deviation, variance and standard deviation for grouped and ungrouped data, change of origin and scale, combined variance, corrected variance after replacing an observation."),
  ("C", 45, {"XI": 10, "XII": 35}, "Probability: classical probability with counting and addition theorem (tag these XI); multiplication theorem, conditional probability, independent events (tag these XII)."),
  ("D", 45, {"XII": 45}, "Total probability, Bayes' theorem, probability distribution of a discrete random variable (validity, mean, variance, finding unknown probabilities).")])

unit(14, "Trigonometry", "Trigonometry",
 "Trigonometrical identities and trigonometrical functions, inverse trigonometrical functions their properties.",
 ["Trigonometric ratios of allied and compound angles, multiple and sub-multiple angles, sum-to-product and product-to-sum, conditional identities (A + B + C = pi), values of special angles like 15, 18, 36 degrees",
  "Trigonometric functions: domain, range, period, signs, maximum and minimum of expressions like a sin x + b cos x and quadratic expressions in sin x, products of cosines in GP",
  "Inverse trigonometric functions: principal values, domains and ranges, properties, sum/difference formulas, simplification, equations in inverse trigonometric functions"],
 ["Trigonometric equations and general solutions (not listed)", "heights and distances", "properties of triangles (sine/cosine rule, not listed)"],
 [("A", 55, {"XI": 55}, "Trigonometric identities: allied and compound angles, multiple and half angles, sum-to-product, values of special angles, conditional identities with A + B + C = pi, telescoping products like cos A cos 2A cos 4A."),
  ("B", 55, {"XI": 55}, "Trigonometric functions: domains, ranges, periods, max/min of a sin x + b cos x + c and quadratic-in-sin expressions, signs in quadrants, number of solutions only via graphs within an interval (no general solution formulas), comparisons of values."),
  ("C", 50, {"XII": 50}, "Inverse trigonometric functions: principal values, domain and range, properties like sin^-1 x + cos^-1 x = pi/2, tan^-1 sums with the xy < 1 condition, simplification, sums of series of tan^-1 terms by telescoping, equations in inverse trigonometric functions.")])


def quotas(n_unit, sizes):
    tot = {"Easy": round(n_unit * 0.30), "Medium": round(n_unit * 0.45)}
    tot["Difficult"] = n_unit - tot["Easy"] - tot["Medium"]
    out = [dict() for _ in sizes]
    for lvl in ("Easy", "Medium"):
        raw = [tot[lvl] * s / n_unit for s in sizes]
        base = [int(r) for r in raw]
        rem = tot[lvl] - sum(base)
        for i in sorted(range(len(sizes)), key=lambda i: -(raw[i] - base[i]))[:rem]:
            base[i] += 1
        for i, b in enumerate(base):
            out[i][lvl] = b
    for i, s in enumerate(sizes):
        out[i]["Difficult"] = s - out[i]["Easy"] - out[i]["Medium"]
    return out, tot


plan = {}
os.makedirs("briefs", exist_ok=True)
for n, u in UNITS.items():
    sizes = [b[1] for b in u["batches"]]
    q, tot = quotas(sum(sizes), sizes)
    md = [f"# Unit {n}: {u['name']}", "", f"Official 2026 text: \"{u['official']}\"", "", "In scope (interpretation used for this bank):"]
    md += [f"- {x}" for x in u["inscope"]]
    md += ["", "Out of scope (do not write):"] + [f"- {x}" for x in u["outscope"]]
    open(f"briefs/U{n:02d}_scope.md", "w").write("\n".join(md) + "\n")
    plan[f"U{n:02d}"] = dict(unit_number=n, unit_name=u["name"], branch=u["branch"], count=sum(sizes), totals=tot, batches=[
        dict(letter=b[0], size=b[1], classes=b[2], topic=b[3], quotas=qq, file=f"drafts/u{n:02d}_{b[0].lower()}.py", prefix=f"U{n:02d}-{b[0]}",
             min_numerical=max(8, round(b[1] * 0.18)))
        for b, qq in zip(u["batches"], q)])
json.dump(plan, open("config/batch_plan.json", "w"), indent=1)
tb = sum(len(p["batches"]) for p in plan.values())
print("units", len(plan), "batches", tb, "questions", sum(p["count"] for p in plan.values()))
for k, p in plan.items():
    print(k, p["count"], p["totals"], [(b["letter"], b["size"], b["quotas"]) for b in p["batches"]])
