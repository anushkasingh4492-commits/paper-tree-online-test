"""Separate audit solver reused on the corrected release; no authoring expressions imported."""
import re,math
from math import sqrt,pi,sin,cos,tan,acos,asin,atan,degrees,radians
def number(s):
    s = s.translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺', '0123456789-+')).replace('−', '-')
    m = re.match('\\s*([-+]?\\d+(?:\\.\\d*)?(?:[eE][-+]?\\d+)?)(?:\\s*×\\s*10([-+]?\\d+))?', s)
    if not m:
        raise ValueError(s)
    return float(m[1]) * (10 ** int(m[2]) if m[2] else 1)

def outcomes(k, p):
    g = 10
    if k == 'calibrated_annulus':
        scale = (p['s2'] - p['s1']) / (p['r2'] - p['r1'])
        zero = p['s1'] - scale * p['r1']
        ro = (p['so'] - zero) / scale
        ri = (p['si'] - zero) / scale
        density = p['m'] / (3.14 * p['L'] * (ro - ri) * (ro + ri))
        frac = 2 * p['ds'] / scale / (ro + ri)
        return dict(rho=density, err=100 * frac, absrho=density * frac)
    if k == 'resistance_loading_error':
        wire = p['I'] - p['V'] / p['Rv']
        density = p['V'] / wire * 3.14 * ((p['d'] - p['z']) * 0.001 / 2) ** 2 / p['L']
        fraction = (p['I'] * p['dv'] + p['V'] * p['di']) / (p['V'] * wire)
        return dict(rho=density, rel=100 * fraction, drho=density * fraction)
    if k == 'rebounding_projectile':
        total = 2 * p['uy'] / g
        hit = p['wall'] / p['ux']
        after = total - hit
        vx = -p['e'] * p['ux']
        t0 = hit - p['wall'] / vx
        return dict(land=p['wall'] + vx * after, speed=sqrt(vx ** 2 + p['uy'] ** 2), returnheight=p['uy'] * t0 - g * t0 * t0 / 2)
    if k == 'meeting_braking':
        catch = (p['w'] * p['delay'] + p['w'] ** 2 / (2 * p['a'])) / (p['w'] - p['v'])
        return dict(catch=catch, position=p['v'] * catch, separation=p['v'] * p['delay'] + p['v'] ** 2 / (2 * p['a']))
    if k == 'stacked_threshold':
        f = p['uk'] * p['m'] * g
        a = f / p['m']
        b = (p['F'] - f) / p['M']
        slide = (b - a) * p['t'] ** 2 / 2
        return dict(relative=slide, heat=f * slide, ratio=p['M'] * b * b / (p['m'] * a * a))
    if k == 'elevator_incline':
        normal = p['m'] * (g + p['a']) * p['c']
        P = p['m'] * (g + p['a']) * p['s'] + p['us'] * normal
        return dict(speed=sqrt(2 * (p['us'] - p['uk']) * normal * p['d'] / p['m']), work=P * p['d'], heat=p['uk'] * normal * p['d'])
    if k == 'pulley_inverse_friction':
        f = (p['m'] + p['h2']) * p['a2'] - p['h2'] * g
        a = (p['h3'] * g - f) / (p['m'] + p['h3'])
        return dict(T=p['h3'] * (g - a), time=sqrt(4 / a), work=2 * f)
    if k == 'vertical_embedding_spring':
        total = p['M'] + p['m']
        v = p['m'] * p['u'] / total
        x = (p['m'] * g + sqrt((p['m'] * g) ** 2 + p['k'] * total * v * v)) / p['k']
        return dict(maxdown=x, maxforce=p['M'] * g + p['k'] * x, gravwork=total * g * x)
    if k == 'rough_rebound':
        friction = p['mu'] * p['m'] * g
        x = (sqrt(friction ** 2 + p['k'] * p['m'] * p['u'] ** 2) - friction) / p['k']
        kin = p['m'] * p['u'] ** 2 / 2 - 2 * friction * x
        return dict(exit=sqrt(2 * kin / p['m']), after=kin / friction, loss=2 * friction * x)
    if k == 'oblique_collision':
        v = p['u'] * sin(radians(p['theta']))
        v1 = p['u'] * cos(radians(p['theta']))
        return dict(height=v * v / (2 * g), impulse=p['m'] * v, ratio=(v / v1) ** 2)
    if k == 'rod_embedding':
        inertia = (p['M'] / 3 + p['m']) * p['L'] ** 2
        omega = p['m'] * p['u'] * p['L'] / inertia
        energy = inertia * omega ** 2 / 2
        return dict(angle=degrees(acos(1 - energy / (g * p['L'] * (p['M'] / 2 + p['m'])))), loss=p['m'] * p['u'] ** 2 / 2 - energy, pivot=abs((p['M'] / 2 + p['m']) * p['L'] * omega - p['m'] * p['u']))
    if k == 'rotating_platform':
        inertia = 2 * p['m'] * (p['w1'] * p['r1'] ** 2 - p['w2'] * p['r2'] ** 2) / (p['w2'] - p['w1'])
        H = (inertia + 2 * p['m'] * p['r1'] ** 2) * p['w1']
        finalI = inertia + 2 * p['m'] * p['r3'] ** 2
        omega = H / finalI
        return dict(w3=omega, work=finalI * omega * omega / 2 - (inertia + 2 * p['m'] * p['r2'] ** 2) * p['w2'] ** 2 / 2, force=p['m'] * omega * omega * p['r3'])
    if k == 'impulse_rod_rebound':
        rodI = p['M'] * p['L'] ** 2 / 12
        J = (1 + p['e']) * p['u'] / (1 / p['m'] + 1 / p['M'] + (p['L'] / 2) ** 2 / rodI)
        return dict(w=J * p['L'] / 2 / rodI, v=p['u'] - J / p['m'])
    if k == 'gravity_two_altitudes':
        ratio = sqrt(p['g1'] / p['g2'])
        R = (p['h2'] - ratio * p['h1']) / (ratio - 1)
        GM = p['g1'] * (R + p['h1']) ** 2
        return dict(escape=sqrt(2 * GM / R), period=2 * pi * (R + p['h3']) / sqrt(GM / (R + p['h3'])), delta=GM * (p['h2'] - p['h1']) / ((R + p['h1']) * (R + p['h2'])))
    if k == 'tangential_orbit_change':
        vi = p['f'] * sqrt(p['gm'] / p['r'])
        h = p['r'] * vi
        epsilon = vi * vi / 2 - p['gm'] / p['r']
        a = -p['gm'] / (2 * epsilon)
        far = 2 * a - p['r']
        vf = h / far
        return dict(far=far, vf=vf, slowdown=vi - vf)
    if k == 'calorimeter_two_trials':
        A = p['ms'] * (100 - p['T1']) / (p['T1'] - 20)
        B = p['ms2'] * (100 - p['T2']) / (p['T2'] - 20)
        cs = 4200 * (p['mw2'] - p['mw']) / (B - A)
        C = A * cs - 4200 * p['mw']
        H = C + 4200 * p['mw']
        return dict(Tf=(H * p['hot'] - p['ice'] * 336000) / (H + p['ice'] * 4200), maxice=H * p['hot'] / 336000, extra=(H + p['ice'] * 4200) * 10, C=C, cs=cs)
    if k == 'inclined_venturi':
        Q = sqrt(2 * (p['dp'] / 1000 - g * p['h']) / (1 / (p['A2'] * 0.0001) ** 2 - 1 / (p['A1'] * 0.0001) ** 2))
        v1 = Q / (p['A1'] * 0.0001)
        v3 = Q / (p['A3'] * 0.0001)
        return dict(drop=500 * (v3 * v3 - v1 * v1), power=p['dp'] * Q, rise=1000 * g * Q * p['h'])
    if k == 'bonded_thermal_rods':
        k1 = p['A1'] * p['Y1'] * 1000 / p['L']
        k2 = p['A2'] * p['Y2'] * 1000 / p['L']
        free1 = p['L'] * p['al1'] * 1e-06 * p['DT']
        free2 = p['L'] * p['al2'] * 1e-06 * p['DT']
        x = (k1 * free1 + k2 * free2) / (k1 + k2)
        F = k1 * (x - free1)
        return dict(extension=x * 1000, force=abs(F), energy=F * F * (1 / k1 + 1 / k2) / 2)
    if k == 'heat_work_inverse':
        exponent = p['W'] / (8 * (p['T2'] - p['T1'])) + p['cv']
        ratio = (p['T2'] / p['T1']) ** exponent
        return dict(vtotal=ratio, ptotal=1 / ratio)
    if k == 'cascade_power_constraint':
        total = p['Q'] * (1 - p['Tc'] / p['Th'])
        w2 = total / (1 + p['ratio'])
        w1 = p['ratio'] * w2
        T = p['Th'] * (1 - w1 / p['Q'])
        discharge = w2 * T / (T - p['Tc'])
        return dict(T=T, reject=discharge, fraction=w1 / (p['Q'] + discharge))
    if k == 'gas_composition_inverse':
        totalCv = p['Q'] / p['dt']
        b = (3 * p['mass'] - totalCv) / 64
        a = (p['mass'] - 28 * b) / 4
        Tf = p['T'] * 2 ** (8 * (a + b) / totalCv)
        return dict(Tf=Tf, vrms=sqrt(24 * Tf / 0.028), workon=totalCv * (Tf - p['T']))
    if k == 'effusion_mixture':
        a = p['a'] / 2
        b = 3 * p['b'] / 4
        Cv = 12 * a + 20 * b
        Tf = p['T'] + p['Q'] / Cv
        return dict(pressure=(a + b) / (p['a'] + p['b']) * Tf / p['T'], reversible=p['Q'] * (Cv + 8 * (a + b)) / Cv)
    if k == 'spring_friction_cycles':
        B = p['A'] - 2 * p['F'] / p['k']
        C = B - 2 * p['F'] / p['k']
        return dict(right=C, v2=sqrt((p['k'] * B * B - 2 * p['F'] * B) / p['m']), heat=p['F'] * (p['A'] + 2 * B + C))
    if k == 'accelerating_pendulum_inverse':
        oldg = (2 * pi / p['T']) ** 2 * p['L']
        a = oldg * p['s']
        newg = sqrt(100 + a * a)
        return dict(newT=2 * pi * sqrt(p['L'] / newg), newangle=degrees(atan(a / 10)), ratio=newg / oldg)
    if k == 'floating_capacitor_switch':
        common = (p['C1'] * p['V1'] + p['C2'] * p['V2']) / (p['C1'] + p['C2'])
        a = p['K'] * p['C1']
        b = p['C2']
        dv = common - common / p['K']
        trans = a * b / (a + b) * dv
        return dict(loss2=0.5 * a * b / (a + b) * dv * dv * 1e-06, transfer=trans)
    if k == 'field_potential_inverse':
        a = p['V'] * p['x'] ** 2 / (9000000000.0 * p['d'])
        b = p['V'] * (p['d'] - p['x']) ** 2 / (9000000000.0 * p['d'])
        V1 = 9000000000.0 * (a / p['r1'] + b / (p['r1'] - p['d']))
        V2 = 9000000000.0 * (a / p['r2'] + b / (p['r2'] - p['d']))
        work = p['q'] * 1e-06 * (V2 - V1)
        return dict(work=work, field=9000000000.0 * (a / p['r2'] ** 2 + b / (p['r2'] - p['d']) ** 2), speed=sqrt(-2 * work / p['m']))
    if k == 'dipole_measurement_pair':
        scale = p['W'] + p['K']
        return dict(torque=sqrt(p['K'] * (2 * p['W'] + p['K'])), speed45=sqrt(sqrt(2) * scale / p['I']), period=2 * pi * sqrt(p['I'] / scale))
    if k == 'two_meter_loading':
        I1 = p['V1'] / p['R1']
        I2 = p['V2'] / p['R2']
        r = (p['V1'] - p['V2']) / (I2 - I1)
        emf = p['V1'] + r * I1
        G = 1 / p['R1'] + 1 / p['R2'] + 1 / p['load']
        V = emf / (1 + r * G)
        return dict(V=V, power=V * V / p['load'], loss=(V * G) ** 2 * r)
    if k == 'bridge_end_resistance':
        a = 1 - p['l1'] / 100
        b = 1 - p['l2'] / 100
        c = (p['l1'] - p['l2']) / 100
        ratio = (c + sqrt(c * c + 4 * a * b)) / (2 * a)
        X = p['R'] * ratio
        ideal = 100 * ratio / (1 + ratio)
        return dict(X=X, shift=ideal - p['l1'], parallel=p['R'] * ratio / (1 + ratio))
    if k == 'helix_from_measurements':
        path1 = sqrt((2 * pi * p['r']) ** 2 + p['p'] ** 2)
        qm = 8 * pi * pi * p['V'] / (p['B'] ** 2 * path1 ** 2)
        T = 2 * pi / (qm * p['B2'])
        scale = sqrt(p['V2'] / p['V']) * p['B'] / p['B2']
        return dict(period=T, path=path1 * scale, pitch=p['p'] * scale, qm=qm)
    if k == 'coil_torsion_calibration':
        kappa = 2 * p['U'] / p['cal'] ** 2
        angle = p['th1']
        magnetic = kappa * angle / cos(angle)
        return dict(B2=2 * p['B1'] * cos(angle) / cos(2 * angle), work=kappa * (2 * angle) ** 2 / 2 - magnetic * sin(2 * angle), moment=magnetic * cos(2 * angle) - 2 * kappa * angle)
    if k == 'rail_friction_inverse':
        damping = (p['F2'] - p['F1']) / (p['v2'] - p['v1'])
        f = p['F1'] - damping * p['v1']
        v = (p['F3'] - f) / damping
        I = sqrt(damping / p['R']) * v
        return dict(current=I, power=damping * v * v, charge=3 * sqrt(damping / p['R']))
    if k == 'two_frequency_rlc':
        resistance = p['V'] / (sqrt(2) * p['I'])
        resonance = p['w'] / sqrt(2)
        vc = sqrt(2) * p['V']
        capacitance = 1 / (resistance * p['w'])
        return dict(wr=resonance, Vc=vc, energy=capacitance * vc * vc)
    if k == 'radiation_calorimeter':
        H = p['I'] ** 2 * p['R'] * p['t'] / p['dT']
        power = H * p['rise'] / p['time']
        flux = power / (p['absorb'] * p['A'] * 0.0001 * cos(radians(p['theta'])))
        E = sqrt(2 * flux / (8.85e-12 * 300000000.0))
        return dict(E=E, B=E / 300000000.0, photons=power * p['lam'] * 1e-09 / (6.63e-34 * 300000000.0))
    if k == 'wave_photo_current':
        absorbed = 0.5 * 8.85e-12 * 300000000.0 * p['E'] ** 2 * p['A'] * 0.0001 * (1 - p['reflect'])
        charge = absorbed * p['t'] / (6.63e-34 * p['freq']) * p['yieldq'] * 1.6e-19
        C = p['C'] * 1e-06
        energy = charge * charge / (2 * C)
        return dict(V=charge / C, energy=energy, ratio=energy / (absorbed * p['t']))
    if k == 'lens_virtual_inverse':
        f1 = 1 / (1 / p['u'] + 1 / p['v'])
        f2 = 1 / (1 / p['z'] - 1 / (p['v'] - p['d']))
        v1 = 1 / (1 / f1 - 1 / p['u2'])
        v2 = 1 / (1 / f2 + 1 / (v1 - p['d']))
        magn = -v1 / p['u2'] * v2 / (v1 - p['d'])
        return dict(final=v2, mag=magn, distance=p['u2'] + p['d'] + v2)
    if k == 'interference_filter_inverse':
        a = (sqrt(p['imax']) + sqrt(p['imin'])) / 2
        b = (sqrt(p['imax']) - sqrt(p['imin'])) / 2
        c = a * sqrt(p['t'])
        return dict(I=c * c + b * b + 2 * c * b * cos(radians(p['phase'])), visibility=2 * c * b / (c * c + b * b), factor=(b / a) ** 2)
    if k == 'ydse_two_plates':
        firstdelay = p['shift'] * p['d'] / p['D']
        index = 1 + firstdelay / p['t']
        delay = (index - 1) * p['t2'] + (p['n3'] - 1) * p['t3']
        shift = p['D'] * delay / p['d']
        return dict(newshift=shift, fringes=shift / p['beta'], comp=delay / (p['n3'] - 1))
    if k == 'photoelectric_unknown_offset':
        work = p['E1'] - p['S1'] + p['offset']
        K = p['E3'] - work
        final = K + p['Va']
        return dict(wave=sqrt(0.015 / final), ratio=sqrt(final / K))
    if k == 'matter_wave_retardation':
        K = p['V'] * p['r'] ** 2 / (p['r'] ** 2 - 1)
        final = K + p['A']
        return dict(wave=sqrt(0.015 / final), threshold=1240 / (p['photon'] - K), ratio=final / (K - p['V']))
    if k == 'fusion_lab_frame':
        total = p['m1'] + p['m2']
        a = p['m1'] * 1.66e-27
        b = p['m2'] * 1.66e-27
        release = p['Q'] * 1.6e-13
        v1 = sqrt(2 * release * p['m2'] / total / a)
        v2 = sqrt(2 * release * p['m1'] / total / b)
        return dict(K1=0.5 * a * (p['V'] + v1) ** 2 / 1.6e-13, K2=0.5 * b * (p['V'] - v2) ** 2 / 1.6e-13, relative=v1 + v2)
    if k == 'hydrogen_spectrum_inverse':
        Z = p['radius'] * p['ion'] / 13.6
        binding = 13.6 * (Z / p['lower']) ** 2
        return dict(wave=1240 / (binding - p['ion']), ewave=sqrt(0.015 / (p['photon'] - binding)))
    if k == 'zener_two_regimes':
        i1 = p['U1'] / p['L1']
        i2 = p['Vz'] / p['L2'] + p['Iz']
        R = (p['Vz'] - p['U1']) / (i1 - i2)
        supply = p['U1'] + i1 * R
        unloaded = supply / (1 + R / p['L3'])
        node = min(p['Vz'], unloaded)
        return dict(node=node, P=node * node / p['L3'], limit=R * p['Vz'] / (supply - p['Vz']))
    if k == 'diode_two_thresholds':
        R = p['L'] * (p['S1'] / p['X1'] - 1)
        free = p['E'] / (1 + R / p['L'])
        node = max(p['lower'], min(p['upper'], free))
        return dict(Iupper=max(0, (p['E'] - node) / R - node / p['L']), power=(p['E'] - node) ** 2 / R, threshold=p['lower'] * (1 + R / p['L']))
    if k == 'caliper_density_experiment':
        least = 0.05
        d = p['ms'] + (p['coinc'] - p['zero']) * least
        density = p['mass'] / (3.14 * (d / 10) ** 3 / 6)
        uncorrected = p['ms'] + p['coinc'] * least
        return dict(absolute=density * 3 * least / d, bias=100 * ((d / uncorrected) ** 3 - 1))
    if k == 'half_deflection_loading':
        G = 1 / (1 / p['S'] - 1 / p['R'])
        I0 = p['E'] / (p['R'] + G)
        If = I0 * p['fs'] / p['div']
        drop = If * G
        return dict(shunt=drop / (p['range'] - If), power=If * drop, burden=drop)
    if k == 'loaded_piston_release':
        T2 = 2 * p['T']
        V2 = 2 * p['V']
        Tf = T2 * p['factor'] ** 0.4
        nR = p['p'] * p['V'] / p['T']
        deltaU = 1.5 * nR * (Tf - p['T'])
        heat = 2.5 * p['p'] * p['V']
        return dict(net=heat - deltaU, tf=Tf, ratio=deltaU / heat)
    if k == 'microscope_slab_layers':
        inverseN = (p['top'] - p['apparent']) / (p['top'] - p['b'])
        depth = p['t1'] * inverseN + p['t2'] / p['n2']
        thickness = p['t1'] + p['t2']
        return dict(reading=p['b'] + thickness - depth, effective=thickness / depth, depth=depth)
    if k == 'resonance_thermal_comparison':
        end = (p['l2'] - 3 * p['l1']) / 2
        f = p['c1'] / (0.02 * (p['l2'] - p['l1']))
        wavelength = 0.04 * (p['newl'] + end)
        return dict(speed2=f * wavelength, third=p['newl'] + 100 * wavelength)
    raise ValueError(k)

def experiment_values():
    d = 12 + (7 - 2) * 0.05
    wire = 0.5 + (0.28 - 0.03)
    unknown = (50 * 30 - 100 * 10) / 30
    Y = 20 * 2 / (3.14 * (0.0005 / 2) ** 2 * 0.0004)
    eta = (7800 - 1000) * 10 * 2 * 0.0005 ** 2 / (9 * (0.06 / 20))
    solid = (0.2 * 4200 + 80) * 10 / (0.1 * 70)
    G = 1000 / 9
    n = sin(radians(49)) / 0.5
    return {1: [d, 100 * 3 * 0.05 / d, 100 * 0.1 / d], 2: [wire, 8 * 3.14 * (wire * 0.001 / 2) ** 2 / 2, 100 * 2 * 0.01 / wire], 3: [1 - (6 / 8) ** 2, 0.32 * (1 - (4.5 / 8) ** 2) / 120, 0.75 ** 6], 4: [unknown, (150 + unknown) * 0.01, 40 + (50 * 36 - 100 * 10) / unknown], 5: [Y, (10 + 30) / 2 * 0.0004, 4], 6: [0.03 * 1000 * 10 * 0.0005 / 2, (0.03 - 0.018) * 1000 * 10 * 0.0005 / 2, 3.6], 7: [eta, 20 * 4, 4 / 3 * 3.14 * 0.0005 ** 3 * (7800 - 1000) * 10 * 0.003], 8: [2 * (0.5 - 0.16) * 500, (50 - 3 * 16) / 2, 340 / 400 / 4 * 100 - 1], 9: [solid, 100 * 80 / (0.2 * 4200 + 80), (0.2 * solid * 100 + 920 * 20) / (0.2 * solid + 920)], 10: [6 * 40 / 60 * 3.14 * (0.0005 / 2) ** 2 / 2, 100 * 2 / (2 + 6), 100 * 0.5 * (1 / 40 + 1 / 60)], 11: [(1.55 - 0.55) / (0.3 - 0.1), 100 * (1.55 / 0.3 / 5 - 1), 5 * 2e-07], 12: [G, 2 / (1000 + G) / 20, 2 / (1000 + G * 100 / (G + 100))], 13: [1 / (1 / 20 + 1 / 30), -30 / 20, 50 + 1 / (1 / 12 - 1 / 24)], 14: [n, 30, degrees(asin(1 / n))], 15: [12 / 8, 10 + 24 * (1 - 1 / 1.5), 13 / 9], 16: [(0.8 - 0.7) / (0.02 - 0.008), 0.7 + (0.014 - 0.008) / (0.02 - 0.008) * 0.1, (5 - 0.75) / 0.014], 17: [0.2 / (0.03 - 0.01), (9 - 4.9) / (150 + 10), (9 - 4.9) / 160 * (4.9 + 10 * (9 - 4.9) / 160)], 18: [(5 - 2) / 0.01, 60 / 3, 3 * 3 / (2 / 0.01)]}
