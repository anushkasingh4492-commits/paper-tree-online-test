"""Independent chemical-arithmetic evaluators for the packaged release."""
import math
import numpy as np
def solve(a, b, c, d, u, v):
    return tuple(np.linalg.solve([[a, b], [c, d]], [u, v]))

def positive(a, b, c):
    return (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)

def calc(m, d):
    v = lambda k: d[k]
    if m == 'carbonate-mixture':
        return solve(106, 84, 2, 1, v('mass'), v('hcl'))[1] * 84
    if m == 'metal-mixture':
        return solve(24, 27, 1, 1.5, v('mass'), v('h2'))[1] * 27 / v('mass') * 100
    if m == 'calcination-residue':
        return v('loss') / 44 / (v('hcl') / 2) * 100
    if m == 'purity-yield':
        return v('mass') * 0.8 / 100 * 44 * 0.9
    if m == 'combustion-mixture':
        return solve(1, 1, 0.5, 2, v('co2'), v('o2'))[1] / v('co2') * 100
    if m == 'aliquot-dilution':
        return v('mass') / v('M') * v('ali') / v('V') / (v('out') / 1000)
    if m == 'hydrogen-transition':
        return 13.6 * (1 / v('nf') ** 2 - 1 / v('ni') ** 2)
    if m == 'orbital-node-inverse':
        return sum((2 for n in range(1, v('N') + 1) for l in range(n) for ml in range(-l, l + 1) if abs(ml) == 1 and n - l - 1 >= 1))
    if m == 'photoelectric-inverse':
        return (v('ratio') - 2) * v('k')
    if m == 'spectrum-inverse-Z':
        z = v('nf') * math.sqrt((v('emission') + v('ionisation')) / 13.6)
        return z * z * math.sqrt(13.6 / v('ionisation'))
    if m == 'MO-addition':
        return (v('nb') - v('na') - 2) / 2
    if m == 'MO-population-change':
        return solve(1, 1, 1, v('ratio'), v('hc') - 108 - 121 + 349, v('hf') - 108 - 79 + 328)[0]
    if m == 'gibbs-two-temperatures':
        h, s = solve(1, -v('T1'), 1, -v('T2'), v('g1'), v('g2'))
        return h / s
    if m == 'gibbs-substitution':
        return v('H') - v('T') * v('S') / 1000
    if m == 'Hess-calorimetric-amount':
        x, y = solve(16, 28, 891, 284, v('mass'), v('heat'))
        return 100 * y / (x + y)
    if m == 'gibbs-Q':
        return 0.008314 * v('T2') * (v('lnQ') - v('lnK') + v('H') / 0.008314 * (1 / v('T2') - 1 / v('T1')))
    if m == 'heat-work-capacity':
        return 8.314 / (v('qp') / (v('mp') * v('tp')) - v('qv') / (v('mv') * v('tv')))
    if m == 'PV-first-law':
        return v('q') - 100 * v('P') * v('dv')
    if m == 'osmotic-pressure':
        return v('mass') / v('M') * 0.082057 * v('T') / v('V')
    if m == 'evaporation-Raoult':
        return v('mass') * 18 / v('lost') * (v('P1') / (v('P0') - v('P1')) - v('P2') / (v('P0') - v('P2')))
    if m == 'colligative-M':
        return v('w') * v('Kf') / (v('kg') * v('dt'))
    if m == 'molality-density-dilution':
        return solve(60, 180, 1, 1, v('w'), v('m') * (v('rho') * v('V') - v('w')) / 1000)[0] * 60 / v('w') * 100
    if m == 'Henry-exact-moles':
        roots = np.roots([v('delta'), -v('delta') * (v('p1') + v('p2')) - v('nw') * (v('p2') - v('p1')), v('delta') * v('p1') * v('p2')])
        return max(roots)
    if m == 'osmotic-mixture':
        return solve(60, 180, 1, 1, v('mass'), v('pi') * v('V') / (0.082057 * v('T')))[0] * 60
    if m == 'Raoult-total':
        return v('x') * v('PA') + (1 - v('x')) * v('PB')
    if m == 'Raoult-Dalton-inverse':
        return 100 * (v('P') - v('PB')) / (v('PA') - v('PB')) * v('PA') / v('P')
    if m == 'salt-dissociation-ions':
        return v('b') / (2 * solve(111, 180, 1, 1, v('w'), v('dt') * 0.2 / 1.86 - v('b'))[0]) * 100
    if m == 'dimerisation-inverse':
        M = v('w2') * 0.08314 * v('T') / (v('pi') * v('V'))
        return 200 * (1 - v('dt') * M * v('kg') / (v('Kf') * v('w')))
    if m == 'buffer-formation':
        return v('pka') + math.log10(v('base') / (v('acid') - v('base')))
    if m == 'dissociation-compression':
        k = 4 * v('x') ** 2 / (v('V') * (v('n0') - v('x')))
        return positive(4, k * v('V') / 2, -k * v('V') * v('n0') / 2)
    if m == 'acid-base-regime':
        r = 10 ** (v('ph2') - v('ph1'))
        return 1000 * v('b1') * v('b2') * (r - 1) / (r * v('b1') - v('b2'))
    if m == 'weak-acid-quadratic':
        return positive(1, v('ka'), -v('ka') * v('C')) * 1000
    if m == 'weak-acid-dilution':
        ka = v('c') * v('alpha') ** 2 / (1 - v('alpha'))
        return 100 * positive(v('c') / v('dilution'), ka, -ka)
    if m == 'buffer-two-additions':
        r0 = 10 ** (v('ph0') - v('pka'))
        r1 = 10 ** (v('ph1') - v('pka'))
        return (1 + r0) * v('b') * (1 + r1) / (r1 - r0) * 1000
    if m == 'Ksp-stoichiometry':
        return 4 * v('s') ** 3 * 1000000000000.0
    if m == 'Ksp-dilution':
        vol = (v('va') + v('vc')) / 1000
        a = v('va') / 1000 * v('ca') / vol
        c = v('vc') / 1000 * v('cc') / vol
        s = 2 * v('K') / (math.sqrt((c - a) ** 2 + 4 * v('K')) + c - a)
        return (a - s) * vol * 143500
    if m == 'cell-discharge-Nernst':
        return 1.1 - 0.02958 * math.log10((v('initial') * v('V') + v('electrons') / 2) / (v('initial') * v('V') - v('electrons') / 2))
    if m == 'Nernst-direct':
        return v('E0') - 0.02958 * math.log10(v('ratio'))
    if m == 'conductance-Ka':
        alpha = 1000 * v('kappa') / (v('c') * v('lam'))
        return v('c') * alpha ** 2 / (1 - alpha) * 1000000.0
    if m == 'Nernst-dilution-inverse':
        return 10 * 10 ** ((v('E0') - v('E')) / v('coefficient'))
    if m == 'cell-Gibbs':
        return -v('n') * 96500 * v('E') / 1000
    if m == 'molar-conductivity':
        return 1000 * v('kappa') / v('C')
    if m == 'weighted-electrode-potential':
        return 3 * (v('et') - v('e1')) / 0.05916
    if m == 'Kohlrausch-cell-ionisation':
        return 100000 * v('cell') / (v('res') * v('c') * (v('acid') + v('base') - v('salt')))
    if m == 'mixed-redox-assay':
        return solve(56, 90, 1, 2, v('mass'), 5 * v('mn'))[1] * 1000
    if m == 'first-order-inverse':
        return v('c1') * (v('c1') / v('c2')) ** (v('t1') / (v('t2') - v('t1')))
    if m == 'first-order-pressure':
        return 3 * v('P0') - (3 * v('P0') - v('Pt')) ** 2 / (2 * v('P0'))
    if m == 'kinetics-baseline':
        return math.log(10) * v('t') / math.log((v('Sinfty') - v('S0')) / (v('Sinfty') - v('St')))
    if m == 'Arrhenius-extrapolation':
        return v('k1') * (v('k2') / v('k1')) ** ((1 / v('T1') - 1 / v('T3')) / (1 / v('T1') - 1 / v('T2'))) * 1000
    if m == 'kinetic-regime-switch':
        return (v('c0') - v('k0') * v('t1')) * math.exp(-v('k1') * v('t2'))
    if m == 'Arrhenius-two-T':
        return 0.008314 * math.log(v('factor')) / (1 / v('T1') - 1 / v('T2'))
    if m == 'coupled-initial-rates':
        candidates = [m + 2 * n for m in range(3) for n in range(3) if math.isclose(2 ** m * 3 ** n, v('r2') / v('r')) and math.isclose(3 ** m * 2 ** n, v('r3') / v('r'))]
        assert len(candidates) == 1
        return candidates[0]
    if m == 'zero-order-depletion':
        return v('C0') / v('k')
    if m == 'first-order-conversion':
        return v('half') * 3
    if m == 'complex-metal-identity':
        return (v('mean') - 15) / 20 * 100
    if m == 'Werner-mass-ions':
        return solve(260.5, 243.5, 4, 3, v('mass'), v('ions'))[0] * 1000
    if m == 'CFT-inverse-spin':
        lookup = {(4, 2): 4, (5, 1): 5, (4, 0): 6, (3, 1): 7}
        dcount = lookup[v('hs'), v('ls')]
        return (-0.4 * min(dcount, 6) + 0.6 * max(dcount - 6, 0)) * v('delta')
    if m == 'CFT-spin-crossover':
        dc = v('d')
        hs_t = min(dc, 3) + max(0, dc - 5)
        hs_e = min(max(dc - 3, 0), 2)
        ls_t = min(dc, 6)
        ls_e = max(dc - 6, 0)
        return (-0.4 * (ls_t - hs_t) + 0.6 * (ls_e - hs_e)) * v('delta') + (max(ls_t - 3, 0) + max(ls_e - 2, 0) - max(dc - 5, 0)) * v('P')
    if m == 'Werner-chloride-count':
        return solve(3, 2, 6, 5, v('ag'), v('nh'))[0] * 1000
    if m == 'chelate-entity-count':
        return solve(3, 3, 3, 6, v('cl'), v('lig'))[0] * 3000
    if m == 'organic-combustion-mixture':
        return solve(46, 60, 2, 3, v('mass'), v('co2') / 44)[0] * 46 / v('mass') * 100
    if m == 'extraction-inverse':
        return v('Vw') / v('Vo') * ((v('mass') / v('remaining')) ** 0.5 - 1)
    if m == 'Dumas-mixture-oxygen':
        return solve(93, 123, 1, 1, v('mass'), 2 * v('n2'))[1] * 32 / v('mass') * 100
    if m == 'formula-hydrogenation':
        nc = v('M') * v('carbon_percent') / 1200
        nh = v('M') - 12 * nc
        return (2 * nc + 2 - nh) / 2
    if m == 'hydrogen-uptake-mixture':
        x, y = solve(14 * v('nc'), 14 * v('nc') - 2, 1, 2, v('mass'), v('hyd'))
        return y / (x + y) * 100
    if m == 'bromination-mixture':
        return sum(solve(14 * v('nc'), 14 * v('nc') - 2, 1, 2, v('mass'), v('bromine'))) * 1000
    if m == 'SN1-mixed-rates':
        x, y = solve(v('A'), v('B'), 3 * v('A'), v('B') / 2, v('r1'), v('r2'))
        return x / y
    if m == 'haloalkane-mixture':
        x, y = solve(14 * v('nc') + 36.5, 14 * v('nc') + 71, 1, 2, v('mass'), v('cl'))
        return y / (x + y) * 100
    if m == 'acid-aldehyde-aliquots':
        return v('naoh') * 10 * 60 + v('ag25') / 2 * 4 * 44
    if m == 'iodoform-mixture':
        return solve(46, 60, 1, 1, v('mass'), v('iodoform'))[1] * 60
    if m == 'amine-mixture':
        return solve(45, 59, 1, 1, v('mass'), v('n2'))[0] * 45 / v('mass') * 100
    if m == 'peptide-composition':
        return (v('M') - 75 * v('res') + 18 * (v('res') - 1)) / 14
    raise ValueError(m)

def recompute(q, d):
    m = q['calculation']['model'].removeprefix('rev11-')
    if not q['calculation']['model'].startswith('rev11-'):
        return float(calc(m, d))
    if m == 'limiting-carbonate':
        return 44 * min(d['m'] / 100, d['n'])
    if m == 'aliquot-dilution':
        return d['mass'] * d['pur'] / 40 * (d['ali'] / 250) * 1000 / d['out']
    if m == 'alkane-combustion':
        return d['mass'] / (14 * d['n'] + 2) * (1.5 * d['n'] + 0.5)
    if m == 'purity-yield':
        return 0.44 * d['mass'] * d['pur'] * d['y']
    if m == 'atomic-photon-photoelectric':
        return 13.6 * d['z'] ** 2 * (0.25 - 1 / d['ni'] ** 2) - d['w']
    if m == 'node-subshell-capacity':
        l = d['n'] - d['rad'] - 1
        return 4 * l + 2
    if m == 'hydrogen-level-change':
        return 10.2 * d['z'] ** 2 / d['n'] ** 2
    if m == 'bond-count-acyclic':
        return d['n'] - 1 + (2 * d['n'] - 2)
    if m == 'MO-occupancy':
        return (d['nb'] - 1 - d['na']) / 2
    if m == 'hybridisation-chain':
        return d['n'] + 3 - 2
    if m == 'ideal-gas-heat-path':
        return d['n'] * d['t'] * 29.114
    if m == 'Gibbs-equilibrium':
        return (d['T'] * d['S'] - 1000 * d['H']) / (8.314 * d['T'])
    if m == 'reaction-enthalpy-scaling':
        return -8 * d['heat'] / d['mass']
    if m == 'first-law-expansion':
        return d['q'] - 100 * d['P'] * d['dv']
    if m == 'osmotic-dilution':
        return d['mass'] / d['M'] * 24.942 / (d['V'] * d['dil'])
    if m == 'association-colligative':
        return (2 - d['alpha']) * d['mass'] / (0.1 * d['M'])
    if m == 'Raoult-vapour':
        return 9000 * d['x'] / (30 + 60 * d['x'])
    if m == 'molality-density':
        return d['w'] / 60 * 1000 / (100 * d['rho'] - d['w'])
    if m == 'buffer-neutralisation':
        return 4.76 + math.log10(d['base']) - math.log10(d['acid'] - d['base'])
    if m == 'precipitation-mixing':
        return 1000000.0 * d['ca'] * d['va'] * d['cb'] * d['vb'] / (d['va'] + d['vb']) ** 2
    if m == 'dissociation-equilibrium':
        return 2 * d['n'] * d['alpha'] ** 2 / (1 - d['alpha'])
    if m == 'salt-ionic-product':
        return 4000000000.0 * d['s'] ** 3 / d['dil'] ** 3
    if m == 'conductivity-ionisation':
        return 125 / (d['R'] * d['c'])
    if m == 'Nernst-composition':
        return 1.1 - 0.02958 * math.log10(10 * d['z'] * d['factor'])
    if m == 'Faraday-efficiency':
        return d['I'] * d['t'] * d['eff'] / 96500 * 31.75
    if m == 'cell-Gibbs':
        return -193 * (d['b'] - d['a'])
    if m == 'first-order-diagnostic-time':
        return math.log2(8) * d['t']
    if m == 'zero-order-history':
        return 0.5 * d['c0'] / d['k'] - 10
    if m == 'initial-rate-inference':
        return d['p'] ** d['m'] * d['q'] ** d['n']
    if m == 'activation-energy-profile':
        return d['ef'] - d['dh'] - d['lower']
    if m == 'ion-particle-accounting':
        return (d['A'] - d['z']) / (d['z'] - d['c'])
    if m == 'period-from-configuration':
        return {11: 31, 12: 32, 13: 43, 14: 44, 15: 45, 16: 46, 17: 47, 18: 48, 19: 41, 20: 42}[d['z']]
    if m == 'isoelectronic-size':
        return sorted(d['zs'])[0]
    if m == 'ionisation-jump-oxide':
        return 8 * d['n'] * d['val']
    if m == 'Fajans-polarisation':
        return d['rb'] ** 2 / d['ra'] ** 2
    if m == 'pblock-hydride-valence':
        H = {5: 3, 6: 4, 7: 3, 8: 2, 9: 1, 13: 3, 14: 4, 15: 3, 16: 2, 17: 1}[d['z']]
        return 100 * H / (d['Ar'] + H)
    if m == 'pblock-Lewis-count':
        return d['mol'] * (d['val'] - d['bonds']) / 2
    if m == 'peroxide-redox-count':
        return d['n'] * d['frac'] * 2
    if m == 'halogen-disproportionation':
        return 5 * d['n']
    if m == 'sulfur-oxyanion-redox':
        return 0.5 * d['n']
    if m == 'dion-magnetism':
        occupancy = d['Z'] - 18 - d['c']
        unpaired = sum((1 for i in range(5) if i < occupancy and i + 5 >= occupancy))
        return unpaired * (unpaired + 2)
    if m == 'permanganate-iron-assay':
        return 5 * d['n'] if 'n' in d else d['m'] / 392 / 5 / 0.02 * 1000
    if m == 'dichromate-oxalate':
        return d['n'] * 6 / 2
    if m == 'f-occupancy-spin':
        n = sum((1 for i in range(7) if i < d['d'] and i + 7 >= d['d']))
        return n * (n + 2)
    if m == 'permanganate-neutral':
        return 3 * d['n']
    if m == 'coordination-donor-accounting':
        return d['mol'] * (6 - d['n']) * 17
    if m == 'Werner-chloride-count':
        return d['x'] * d['n'] * (108 + 35.5) * 1000
    if m == 'CFT-low-spin':
        electrons = d['d']
        return (-0.4 * min(electrons, 6) + 0.6 * max(0, electrons - 6)) * d['delta']
    if m == 'chelate-site-charge':
        return 2 * d['en'] - 3
    if m == 'complex-particle-count':
        return d['n'] * (1 + d['m'])
    if m == 'solvent-extraction':
        remaining = d['mass']
        for _ in range(2):
            remaining = remaining / (1 + d['K'] * 0.2)
        return remaining
    if m == 'chromatographic-scaling':
        return d['new'] * d['spot'] / d['front']
    if m == 'combustion-element-analysis':
        return 100 - 100 / d['m'] * (d['co2'] * 3 / 11 + d['water'] / 9)
    if m == 'Carius-chlorine':
        return d['ag'] / 143.5 * 35.5 / d['m'] * 100
    if m == 'formula-hydrogenation':
        return (d['n'] + 1 - d['H'] / 2) * d['m'] / (12 * d['n'] + d['H'])
    if m == 'stereoisomer-count':
        return d['m'] / 2 ** d['n']
    if m == 'homology-functional-change':
        carbons = d['n'] + 1
        alcohol = 12 * carbons + 2 * carbons + 2 + 16
        acid = 12 * carbons + 2 * carbons + 32
        return d['m'] * acid / alcohol
    if m == 'functional-group-DBE':
        hydrogens = 2 * d['n'] - 2
        mass = 12 * d['n'] + hydrogens + 16
        return d['m'] / mass * (hydrogens / 2) * 18
    if m == 'amine-formula-Dumas':
        return d['m'] / (12 * d['n'] + (2 * d['n'] + 1) + 14) * 14
    if m == 'alkyne-hydrogenation':
        return d['m'] / (12 * d['n'] + 2 * d['n'] - 2) * 2
    if m == 'ozonolysis-Tollens':
        return d['n'] * 2 * 2 * 108
    if m == 'selective-hydrogenation-bromine':
        return d['n'] * 2 * 80
    if m == 'aromatic-sidechain-oxidation':
        return d['n'] * (7 * 12 + 5 + 32 + 23)
    if m == 'aromatic-decarboxylation':
        return d['n'] * (6 * 12 + 6)
    routes = {'nitrile-extension': (74, 1), 'Grignard-carboxylation': (74, 1), 'primary-alcohol-oxidation': (74, 1), 'elimination-ozonolysis': (30, 2), 'Grignard-secondary-oxidation': (58, 1), 'anisole-HI-cleavage': (94, 1), 'ester-alcohol-oxidation': (60, 1), 'carbonyl-reduction-esterification': (88, 1), 'Hofmann-rearrangement': (45, 1), 'diazonium-hydrolysis': (94, 1), 'Sandmeyer-chlorination': (112.5, 1), 'nitrile-amine-salt': (81.5, 1)}
    if m in routes:
        M, stoich = routes[m]
        return M * stoich * d['n'] * d['y']
    if m == 'peptide-water-loss':
        return 89 * d['ala'] + 75 * d['gly'] - 18 * (d['ala'] + d['gly'] - 1)
    if m == 'disaccharide-reducing-assay':
        return d['n'] * 2 * 2 * 108
    if m == 'DNA-pair-count':
        return 2 * d['pairs'] + d['gc']
    if m == 'carbohydrate-condensation':
        return 162 * d['n'] + 18
    if m == 'carbonate-standardisation':
        return d['m'] * d['p'] / 106 * 20000
    if m == 'acid-base-standardisation':
        return d['c'] * d['va'] / d['vb']
    if m == 'sulfate-assay':
        return 233 * d['n'] / 2
    if m == 'aluminium-precipitation':
        return (27 + 3 * 17) * d['n'] / 3
    if m == 'dissolution-calorimetry':
        return -(0.2 * 4.18 * d['dt']) / d['n']
    if m == 'aniline-yellow-preparation':
        return d['n'] * d['y'] * (144 + 11 + 42)
    if m == 'acetanilide-preparation':
        return d['n'] * d['y'] * (96 + 9 + 14 + 16)
    raise ValueError(m)
