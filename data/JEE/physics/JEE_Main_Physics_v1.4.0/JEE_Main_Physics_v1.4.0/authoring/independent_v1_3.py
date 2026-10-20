"""Separate closure calculations. No authoring answers or expressions are imported.

Inputs below are transcribed from the printed stems and guarded by text anchors.
Several results use event roots, numerical integration, parameter solving or
enumeration rather than the closed forms used by the authoring module.
"""
import math,re,itertools,cmath
from math import sqrt,pi,log,sin,cos

def root(f,a,b):
    fa=f(a);fb=f(b);assert fa*fb<=0,(fa,fb)
    for _ in range(100):
        c=(a+b)/2;fc=f(c)
        if fa*fc<=0:b=c
        else:a=c;fa=fc
    return (a+b)/2

def integrate(f,a,b,N=10000):
    h=(b-a)/N
    return h/3*(f(a)+f(b)+sum((4 if j%2 else 2)*f(a+j*h) for j in range(1,N)))

def two(a,b,c,d,y,z):
    det=a*d-b*c;assert det
    return (y*d-b*z)/det,(a*z-y*c)/det

def check_revised(bank):
    B={int(q['id'][-4:]):q for q in bank};rows=[]
    def record(n,value,method,details,anchors):
        q=B[n]
        for t in anchors:assert t in q['question'],(n,'printed input changed',t)
        opts={k:float(v.split()[0]) for k,v in q['options'].items()}
        matches=[k for k,v in opts.items() if math.isclose(v,value,rel_tol=6e-6,abs_tol=2e-8)]
        assert matches==[q['correct_option']],(n,value,opts,matches)
        nearest=min(opts,key=lambda k:abs(opts[k]-value));assert nearest==q['correct_option']
        if q['numerical_variant']:
            assert math.isclose(q['numerical_variant']['unrounded_value'],value,rel_tol=1e-8,abs_tol=2e-8),(n,'numeric')
            assert q['numerical_variant']['parent_candidate']==q['candidate_id']
        rows.append(dict(id=q['id'],calculated_value=value,key=q['correct_option'],matching_options=matches,
            method=method,details=details,printed_input_anchors=anchors,status='PASS'))

    # Solve ballistic event equations in chronological order.
    t_ceiling=root(lambda t:20*t-5*t*t-15,0,2)
    vy=-.5*(20-10*t_ceiling);t_wall=18/12
    y_wall=15+vy*(t_wall-t_ceiling)-5*(t_wall-t_ceiling)**2
    vy_wall=vy-10*(t_wall-t_ceiling)
    dt=root(lambda t:y_wall+vy_wall*t-5*t*t,0,4)
    assert 0<t_ceiling<t_wall and y_wall>0 and vy_wall<0
    record(98,18-6*dt,'Chronological ballistic event roots',dict(ceiling=t_ceiling,wall=t_wall,floor=t_wall+dt,y_at_wall=y_wall),
        ['(12 i + 20 j)','y=15 m','x=18 m','floor is y=0','restitution 0.5','10 m/s² downward'])

    sep=lambda t:10*t-1.7*t*t
    a=root(lambda t:sep(t)-12,0,50/17);b=root(lambda t:sep(t)-12,50/17,8)
    c=root(sep,5,8)
    intervals=[(0,a),(b,c)]
    value=sum(integrate(lambda t:abs(12-3*t),a,b) for a,b in intervals)
    assert a<4<b<c<=8
    record(175,value,'Interval roots and numerical speed integration',dict(active_intervals=intervals,turn=4),
        ['0 ≤ t ≤ 8 s','v(t)=12−3t','starts at x=5 m','x_D(t)=5+2t+0.2t²','between 0 and 12 m','laboratory frame'])

    # 2M+f=24, 4M-f=12 from the two trials.
    M,f=two(2,1,4,-1,24,12);a=(50-f)/(M+5);v2=2*a*2;after=M*v2/(2*f)
    assert M>0 and f>0 and a>0
    record(225,2+after,'Two Newton-law equations followed by a work-energy stop',dict(M=M,friction=f,third_a=a,speed_squared=v2,coast=after),
        ['3 kg hanging mass descends with acceleration 2','2 kg hanging mass is initially moving upward','downward acceleration 4','5 kg hanging mass','descended 2 m','cut without an impulse','g=10'])

    net=5*10*.6-3*10*.5-.2*5*10*.8
    v0=sqrt(2*net/(3+5)*2)
    # Integrate the collision impulse on the two subsystems separately:
    # 5(v1-v0)=-J; 5v1-3v0=J for A plus its attached resting lump.
    v1,J=two(5,1,5,-1,5*v0,3*v0)
    net_after=5*10*.6-5*10*.5-.2*5*10*.8
    extra=(.5*10*v1*v1)/(-net_after)
    static_margin=.25*5*10*.8-abs(5*10*.6-5*10*.5)
    assert net>0 and net_after<0 and static_margin>0
    record(263,2+extra,'Impulse equations for the two coupled subsystems and stopping energy',dict(v0=v0,v_after=v1,string_impulse=J,static_margin=static_margin),
        ['A (3 kg)','B (5 kg)','30°','sin β=0.6 and cos β=0.8','μ_k=0.20 and μ_s=0.25','moved 2 m','2 kg lump initially at rest','neglect gravity and friction impulses','g=10'])

    x=0.;distance=0.;turns=[]
    for _ in range(20):
        force=18-2*x
        if abs(force)<=.15*3*10+1e-10:break
        direction=1 if force>0 else -1
        # Work is (18 - direction*3)(xnew-x) - (xnew^2-x^2).
        xnew=(18-direction*3)-x
        assert (xnew-x)*direction>0
        distance+=abs(xnew-x);turns.append(dict(start=x,end=xnew,direction=direction));x=xnew
    else:raise AssertionError('No permanent stop found')
    record(395,distance,'Successive work-zero roots with static tests at every stop',dict(legs=turns,final_x=x,final_force=18-2*x),
        ['3 kg','x=0','F(x)=18−2x','0.10 and 0.15','g=10','static-friction condition'])

    M=2;m=1;L=1.5;g=10;angle=pi/3
    Irod=M*L*L/3;Itot=Irod+m*L*L
    drop_before=(M*L/2+m*L)*sin(angle)
    kinetic_before=g*drop_before
    rod_kinetic_after=kinetic_before*Irod/Itot
    rod_kinetic_bottom=rod_kinetic_after+M*g*L/2*(1-sin(angle))
    omega2=2*rod_kinetic_bottom/Irod;reaction=M*g+M*omega2*L/2
    record(492,reaction,'Energy partition at detachment and radial Newton equation',dict(rod_energy_at_bottom=rod_kinetic_bottom,omega_squared=omega2),
        ['mass 2 kg and length 1.5 m','1 kg point mass','released from rest','60° below','detached without any impulse','g=10'])

    G=6.67e-11;m1=2e20;m2=6e20;d=2e6;M=m1+m2;mu=m1*m2/M
    v=sqrt(1.5*G*M/d);eps=v*v/2-G*M/d;h=d*v
    # At an apsis, 2 eps r^2 + 2 G M r - h^2=0.
    rsum=-G*M/eps;ra=rsum-d
    assert ra>d and eps<0
    va=h/ra;vc=sqrt(G*M/ra);work=.5*mu*(vc*vc-va*va)
    record(573,work/1e22,'Apsis quadratic from energy and angular momentum',dict(apocentre=ra,apocentre_speed=va,circular_speed=vc,work_J=work),
        ['2×10²⁰ kg and 6×10²⁰ kg','d=2×10⁶ m','√(3/2)','equal and opposite tangential impulses','G=6.67×10⁻¹¹','10²² J'])

    d=3e6;omega=1e-4;M=omega**2*d**3/G;m1=M/4;m2=3*M/4;mu=m1*m2/M
    v1=.75*omega*d;v2=-.25*omega*d
    def relative_energy(J):
        p=m1*(v1+J/m1)+m2*v2
        return .5*m1*(v1+J/m1)**2+.5*m2*v2**2-p*p/(2*M)-G*m1*m2/d
    J=root(relative_energy,0,4e23)
    assert abs(relative_energy(J))<abs(G*m1*m2/d)*1e-12
    record(576,J/1e23,'Subtract centre-of-mass energy after a one-body impulse and solve marginal binding',dict(light_mass=m1,heavy_mass=m2,initial_velocities=[v1,v2],impulse=J),
        ['separation 3×10⁶ m','period 2π×10⁴ s','three times as far','only to the lighter body','direction of its initial velocity','G=6.67×10⁻¹¹','10²³ kg m/s'])

    def engine(T):
        reject=1200*T/900;W1=1200-reject;Q2=.75*reject;W2=Q2*(1-300/T)
        return W1,W2,Q2-W2
    T=root(lambda T:engine(T)[0]-engine(T)[1],301,899)
    W1,W2,cold=engine(T);Qc=W1/(900/300-1)
    record(811,cold-Qc,'Solve heat-split work balance, then use refrigerator entropy balance',dict(T=T,W1=W1,W2=W2,engine_rejection=cold,fridge_removal=Qc),
        ['900 K','300 K','absorbs 1200 J','Only 75%','produce equal work','All the work of the first engine','removes heat from the 300 K'])

    # Unknown engine work e and refrigerator work w: e-w=500;
    # (1500-e)+(1+200/(300-200))*w=1400.
    e,w=two(1,-1,-1,3,500,-100)
    eta=e/1500;bound=1-300/800
    assert 0<eta<bound and w>0
    record(814,100*eta/bound,'Two independent device heat/work balances',dict(engine_work=e,refrigerator_work=w,actual_efficiency=eta,carnot_efficiency=bound),
        ['1500 J','800 K','300 K','200 K','remaining 500 J','together is 1400 J','engine need not be reversible'])

    nm,nd=two(12,20,12,28,2080/40,2720/40)
    Cv=12*nm+20*nd;Cp=Cv+8*(nm+nd);gamma=Cp/Cv
    T2=300*math.exp((gamma-1)*log(2));work=Cv*(T2-300)
    assert nm>0 and nd>0
    record(887,work,'Solve composition from two heat-capacity regimes; integrate adiabatic state law',dict(monatomic_mol=nm,diatomic_mol=nd,Cv=Cv,gamma=gamma,final_T=T2),
        ['40 K increase requires 2080 J','40 K increase requires 2720 J','R=8','prepared at 300 K','half its initial volume','vibration remains frozen'])

    initial=[f for f in [96,104] if abs(abs(1.25*f-100)-20)<1e-10];assert initial==[96]
    T0=4*.5**2*.001*initial[0]**2
    finals=[f for f in [145,155] if abs(f*1.000001-150)>abs(f-150)];assert finals==[155]
    T1=4*.4**2*.001*finals[0]**2
    record(1017,(T1-T0)/10*1000,'Enumerate both beat branches in both experiments',dict(initial_candidates=[96,104],valid_initial=initial,final_candidates=[145,155],valid_final=finals,T0=T0,T1=T1),
        ['length 0.50 m','0.001 kg/m','4 beats/s with a 100 Hz','1.5625','20 beats/s','0.40 m','5 beats/s with a 150 Hz','increases this beat frequency','g=10'])

    valid=[]
    for sign1,sign2 in itertools.product([-1,1],repeat=2):
        # f-F=sign1*5; 1.1f-F=sign2*7.
        f=(sign2*7-sign1*5)/.1;F=f-sign1*5
        if f>0 and F>0 and f<F:valid.append((f,F))
    assert len(valid)==1
    f,F=valid[0];mu=18.432/(2*.4*f)**2;newmu=18.432/(.3*F)**2
    record(1020,(newmu-mu)*1000,'Enumerate absolute-value branches and apply harmonic resonance',dict(f=f,fork=F,initial_density=mu,coated_density=newmu),
        ['length 0.40 m','tension 18.432 N','5 beats/s','decreases the beat frequency','1.21','7 beats/s','0.30 m','second harmonic'])

    par=lambda a,b:1/(1/a+1/b)
    R2=root(lambda R2:12*par(par(R2,6),6)/(R2+par(par(R2,6),6))-4,.01,100)
    R1=par(R2,6);openv=12*R2/(R1+R2)
    RL=root(lambda r:12*par(R2,r)/(R1+par(R2,r))-.9*openv,.01,1000)
    assert math.isclose(12*par(R2,6)/(R1+par(R2,6)),6)
    record(1275,RL,'Numerical positive-root solution of both loaded measurements and tolerance boundary',dict(R1_kohm=R1,R2_kohm=R2,open_circuit_V=openv,minimum_load_kohm=RL),
        ['source is 12 V','resistance is 6 kΩ','across R2 as drawn, it reads 6 V','across R1 and reads 4 V','at least 90%'])

    speed0=20000/.1;qm=speed0/(.2*.05);speed=sqrt(speed0**2-2*qm*600);omega=qm*.4;r=speed/omega
    assert .012<r
    time=root(lambda t:r*sin(omega*t)-.012,0,pi/(2*omega))
    record(1424,time*1e9,'First forward trajectory/boundary intersection after electrostatic slowing',dict(q_over_m=qm,speed=speed,radius=r,first_exit_s=time),
        ['E=20000 V/m','B₁=0.10 T','B₂=0.20 T','radius 0.050 m','600 V','0.40 T','0.012 m apart','in ns'])

    resistance=18/3;half_time=log(2)/2;L=resistance*half_time/log(2)
    initial=18/resistance*(1-math.exp(-resistance*2*half_time/L))
    final=-18/(resistance+6);tau=L/(resistance+6)
    time=root(lambda t:final+(initial-final)*math.exp(-t/tau)+.75,0,10*tau)
    zero=root(lambda t:final+(initial-final)*math.exp(-t/tau),0,time)
    assert zero<time
    record(1546,time,'Fit initial growth, carry continuous current into a signed reverse-source transient',dict(r=resistance,L=L,switch_current=initial,steady_after=final,zero_crossing=zero),
        ['18 V','steady current is 3 A','1.5 A at time (ln 2)/2 s','At twice that time','reverses the source polarity','extra 6 Ω','0.75 A','opposite'])

    def coil_energy_L(r):return 2*6.75/(18/r)**2
    r=root(lambda r:(18/r)*coil_energy_L(r)/(r+6)-.375,.1,100)
    L=coil_energy_L(r);steady=18/(r+6);tau=L/(r+6)
    time=root(lambda t:steady+(1-steady)*math.exp(-t/tau)-1.25,0,10*tau)
    record(1547,time*1000,'Infer coil from energy and integrated decay charge, then solve the reconnect transient',dict(r=r,L=L,new_steady=steady,time_constant=tau),
        ['18 V','6.75 J','extra 6 Ω','0.375 C','falls to 1 A','extra 6 Ω remains','reach 1.25 A','in ms'])

    m=.5;f=.5;b=(2*.5)**2/4;v0=(2-f)/b
    joule=integrate(lambda v:m*b*v*v/(f+b*v),0,v0)
    friction=integrate(lambda v:m*f*v/(f+b*v),0,v0)
    assert math.isclose(joule+friction,.5*m*v0*v0,rel_tol=1e-10)
    record(1556,joule,'Numerically integrate electrical and frictional dissipation over the velocity decay',dict(initial_speed=v0,joule_heat=joule,friction_heat=friction,initial_energy=.5*m*v0*v0),
        ['mass 0.50 kg','length 0.50 m','2.0 T','4.0 Ω','friction force','0.50 N','2.0 N force','force is then removed'])

    c=3e8;Pa=.0025488;Fn=1.58592e-11;Ft=5.0976e-12
    theta=math.asin(c*Ft/Pa);cp=cos(theta)
    P=(c*Fn/cp+Pa)/2;alpha=Pa/P;I=.5*8.85e-12*c*200**2;A=P/(I*cp)
    assert 0<alpha<1 and math.isclose((2-alpha)*P*cp/c,Fn,rel_tol=1e-12)
    record(1618,A*1e4,'Invert both photon-momentum components and the absorbed-power measurement',dict(angle_degrees=math.degrees(theta),absorption_fraction=alpha,intercepted_power=P,intensity=I),
        ['peak electric field 200 V/m','0.0025488 W','1.58592×10⁻¹¹ N','5.0976×10⁻¹² N','reflects the rest specularly','ε₀=8.85×10⁻¹²','c=3×10⁸'])

    strong=(sqrt(49)+sqrt(9))/2;weak=(sqrt(49)-sqrt(9))/2
    original=2*pi/6;added=2*pi*(1.5-1)*.5
    phasor=.5*strong*cmath.exp(1j*(original+added))+weak
    record(1752,abs(phasor)**2,'Recover amplitudes and add the filtered complex field phasors',dict(strong_intensity=strong**2,weak_intensity=weak**2,total_phase=original+added),
        ['maximum intensity 49','minimum intensity 9','exceeds that of the weaker by λ/6','intensity by 1/4','index 1.5 and thickness λ/2','replacing the same thickness of air'])

    wavelength=sqrt(.0150/3.5);emitted=.0150/wavelength**2-2;workfn=4-emitted
    gain,offset=two(3-workfn,1,5-workfn,1,.8,3.2)
    assert gain>0 and workfn>0
    record(1788,offset,'De Broglie/acceleration energy followed by simultaneous affine-calibration equations',dict(emission_energy=emitted,work_function=workfn,gain=gain,offset=offset),
        ['S=aV_stop+δ','3 eV and 5 eV','0.8 V and 3.2 V','using 4 eV photons','additional 2 V','√(0.0150/3.5) nm'])

    threshold=3*(300+600)/600
    def power(V):
        # Free-node solution tested against the clamp condition.
        Vx=min(V*600/(300+600),3)
        return ((V-Vx)/300)**2*300
    joules=(integrate(power,0,threshold)+integrate(power,threshold,12))/12
    always_clamped=integrate(lambda V:(V-3)**2/300,0,12)/12
    assert math.isclose(always_clamped*1000,70,abs_tol=1e-8)
    record(2043,joules*1000,'Solve each DC diode state and numerically integrate resistor power over both ramps',dict(threshold_V=threshold,cycle_seconds=1,always_clamped_wrong_mJ=always_clamped*1000),
        ['300 Ω','600 Ω','anode is at X','cathode at a fixed +3 V','0 to 12 V in 0.5 s','next 0.5 s','no capacitance or inductance','in mJ'])

    lc=1-19/20;err=lc/2;vertices=[]
    for dm,ed,eh,ez in itertools.product([-1,1],repeat=4):
        mass=16.01+dm*.01;zero=.15+ez*err
        d=10+5*lc+ed*err-zero;h=20+7*lc+eh*err-zero
        rho=mass/(3.141592654/4*d*d*h/1000)
        vertices.append(dict(mass=mass,d=d,h=h,zero=zero,density=rho))
    vertex=max(vertices,key=lambda v:v['density'])
    assert vertex['d']>0 and vertex['h']>0
    record(2135,vertex['density'],'Enumerate all 16 corners of the independent reading/mass bounds with one common zero error',dict(maximum_corner=vertex,corners=vertices),
        ['20 divisions equal to 19','division is 1 mm','reading 10 mm and coincidence 5','reading 20 mm and coincidence 7','error is 0.15 mm','half a least count','same unknown actual zero error','16.01±0.01','π=3.141592654'])

    X=90/(.5**2*60);ratio1=X/4;ratio2=4/X;rb=.003
    q,ra=two(61-ratio1*39,1,40-ratio2*60,1,ratio1*rb,ratio2*rb)
    diameter=(.5+(32-2)*.5/50)*1e-3
    rho=(q/.01)*3.14*diameter**2/4
    assert q>0 and ra>0
    assert math.isclose((61*q+ra)/(39*q+rb),ratio1) and math.isclose((40*q+ra)/(60*q+rb),ratio2)
    record(2160,rho/1e-8,'Directly solve end-resistance equations in ohms per centimetre, then apply the corrected gauge area',dict(X=X,ohms_per_cm=q,left_end_ohms=ra,right_end_ohms=rb,diameter_m=diameter),
        ['r_b=0.003 Ω','4 Ω','61 cm','40 cm','90 J','0.50 A for 60 s','pitch 0.5 mm','50 circular divisions','reading 0.5 mm','reading 32','zero error 2 divisions','π=3.14'])
    assert len(rows)==24
    return rows

def check_helix(bank,calcs):
    B={q['id']:q for q in bank};rows=[]
    def number(s):
        t=s.translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺','0123456789-+')).replace('−','-')
        m=re.match(r'\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)(?:\s*×\s*10([-+]?\d+))?',t)
        assert m,s
        return float(m[1])*(10**int(m[2]) if m[2] else 1)
    def values(p):
        qm=2*p['V']/(p['B']**2*(p['r']**2+(p['p']/(2*pi))**2))
        scale=sqrt(p['V2']/p['V'])*p['B']/p['B2']
        r2=p['r']*scale;pitch=p['p']*scale;period=2*pi/(qm*p['B2'])
        return dict(q_over_m=qm,period=period,path=math.hypot(2*pi*r2,pitch),pitch=pitch)
    for e in calcs:
        if e['model']!='helix_from_measurements':continue
        q=B[e['id']]
        assert 'For a separate second trial, the particle is first brought to rest' in q['question']
        assert 'kinetic energy on entering the second magnetic region is qV₂' in q['explanation']
        # Recover every displayed calibration input; ξ is supplied separately by each option.
        stem=q['question'];p={}
        pats=dict(V=r'accelerated from rest through ([\d.]+|ξ) V',B=r'uniform magnetic field ([\d.]+|ξ) T',
                  r=r'helical radius is ([\d.]+|ξ) m',p=r'per turn is ([\d.]+|ξ) m',
                  V2=r'then accelerated through ([\d.]+|ξ) V',B2=r'second magnetic region of field ([\d.]+|ξ) T')
        for name,pat in pats.items():
            v=re.search(pat,stem)[1];p[name]=None if v=='ξ' else float(v)
        if e.get('inverse_input'):
            measured=number(stem.split(' = ')[-1]);pred={}
            for k,s in q['options'].items():
                params={**p,e['inverse_input']:number(s)};pred[k]=values(params)[e['target']]
            matches=[k for k,v in pred.items() if math.isclose(v,measured,rel_tol=3e-7,abs_tol=1e-13)]
        else:
            computed=values(p)[e['target']];pred={k:number(s) for k,s in q['options'].items()}
            measured=computed;matches=[k for k,v in pred.items() if math.isclose(v,computed,rel_tol=.0006,abs_tol=1e-13)]
        assert matches==[q['correct_option']],(e['id'],pred,measured,matches)
        rows.append(dict(id=e['id'],printed_inputs=p,target=e['target'],computed_or_observed=measured,
            option_predictions_or_values=pred,matches=matches,key=q['correct_option'],status='PASS',
            method='Printed-input energy and helical geometry; second trial independently from rest.'))
    assert len(rows)==6
    return rows
