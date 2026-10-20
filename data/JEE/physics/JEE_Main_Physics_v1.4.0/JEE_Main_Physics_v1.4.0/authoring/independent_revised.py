"""Separate physical verification of the 14 revised tasks, using printed inputs.
Does not import the task authoring module or its calculated answers.
"""
import math, re, itertools
from math import sqrt, pi

def check_revised(bank):
    B={int(q['id'][-4:]):q for q in bank};rows=[]
    def extract(n,pattern):return float(re.search(pattern,B[n]['question'])[1])
    def record(n,value,method,details,anchors):
        q=B[n]
        for t in anchors:assert t in q['question'],(n,t)
        values={k:float(v.split()[0]) for k,v in q['options'].items()}
        matches=[k for k,v in values.items() if math.isclose(v,value,rel_tol=6e-6,abs_tol=1e-8)]
        assert matches==[q['correct_option']],(n,value,matches)
        if q['numerical_variant']:
            nv=q['numerical_variant']
            assert math.isclose(nv['unrounded_value'],value,rel_tol=2e-8,abs_tol=1e-8)
        rows.append(dict(id=q['id'],calculated_value=value,key=q['correct_option'],matching_options=matches,
                         method=method,details=details,printed_input_anchors=anchors,status='PASS'))

    # Event-driven time integration with analytic ballistic events.
    n=95;x=0.;t=0.;vx=10.;end=4.;events=[]
    while t<end:
        wall=10 if vx>0 else -2
        dt=(wall-x)/vx
        if t+dt>=end:x+=vx*(end-t);break
        x=wall;t+=dt
        assert 20*t-5*t*t>0
        vx*=-(.5 if wall==10 else .4);events.append(dict(t=t,x=x,vx_after=vx))
    record(n,x,'Successive collision events, checked against the ballistic floor time.',events,
           ['(10 i + 20 j)','x=10 m','x=-2 m','0.5 at the right wall','0.4 at the left wall','10 m/s² downward'])

    # Recover P and static coefficient directly from measured kinetic work.
    measured=extract(235,r'relative speed is ([\d.]+) m/s')
    work_per_m=2*measured**2/(2*3)
    P=(work_per_m+2*12*(.6+.2*.8))/(.8+.2*.6)
    N=2*12*.8-.6*P;us=(.8*P-2*12*.6)/N
    assert N>0 and us>.2
    predictions={}
    for k,v in B[235]['options'].items():
        s=float(v);force=2*12*(.6+s*.8)/(.8+s*.6);normal=19.2-.6*force
        pred=sqrt(2*3*(.8*force-14.4-.2*normal)/2)
        predictions[k]=pred
    assert sum(math.isclose(v,measured,rel_tol=1e-7) for v in predictions.values())==1
    record(235,us,'Invert the measured kinetic work, then check every static-coefficient option.',
           dict(measured_speed=measured,P=P,N=N,predicted_speeds=predictions),
           ['2 m/s²','2 kg','0.8P','0.6P','0.20','3.0 m'])
    # Energy over the complete two-stage ascent, independent of an intermediate speed.
    Ps=24/1.1;normal=19.2-.6*Ps
    kinetic_gain=3*(.8*Ps-14.4-.2*normal)
    extra=kinetic_gain/(14.4+.2*19.2)
    record(240,extra,'Work-energy over powered motion followed by unpowered stopping.',
           dict(P_threshold=Ps,N_powered=normal,kinetic_gain=kinetic_gain,stopping_resistance=18.24),
           ['0.50','0.20','0.8P','0.6P','3.0 m','switched off instantaneously'])

    # Net work sets the common kinetic energy without solving for pulley tension.
    f=.2*2*10*sqrt(3)/2;totalK=(4*10*.8-2*10*.5-f)*2
    KA=totalK*(2/6);additional=KA/(10+f)
    record(260,2+additional,'Connected-system work, kinetic-energy sharing, then post-cut stopping work.',
           dict(friction=f,totalK=totalK,KA_at_cut=KA,additional_ascent=additional),
           ['Block A (2 kg)','Block B (4 kg)','30°','sinβ=0.8','0.20','2.0 m','without imparting an impulse'])

    vfirst=10*math.cos(pi/6);first_vector=(vfirst*math.cos(pi/6),vfirst*math.sin(pi/6))
    second_vector=(10-first_vector[0],-first_vector[1]);K2=sum(v*v for v in second_vector)
    assert math.isclose(vfirst*vfirst+K2,100)
    # Monotone energy residual root found by bisection, not the authored quadratic expression.
    lo=0.;hi=1.
    for _ in range(80):
        x=(lo+hi)/2
        if 50*x*x+16*(1+x)>K2:hi=x
        else:lo=x
    record(349,(lo+hi)/2,'Vector momentum and energy, then monotone compression-energy root.',
           dict(second_velocity=second_vector,second_K=K2,residual=50*x*x+16*(1+x)-K2),
           ['mass 2 kg','10 m/s','30°','sinθ=0.6','cosθ=0.8','0.25','1.0 m','100 N/m'])

    T1=extract(923,r'equilibrium is ([\d.]+) s');T2=extract(923,r'period is ([\d.]+) s')
    A=(4*pi*pi*2/T1**2)**2;C=(4*pi*pi*2/T2**2)**2
    a2=C-100;b=sqrt(A-a2)-10
    record(923,b,'Eliminate the common horizontal component between two squared effective gravities.',
           dict(T1=T1,T2=T2,horizontal_acceleration=sqrt(a2),upward_acceleration=b),
           ['length 2.0 m','b>0','upward acceleration is set to zero','g=10 m/s²'])

    e=(.50-3*.16)/2;f=340/(4*(.16+e));temps=[300*(4*(.18+e)*ff/340)**2 for ff in (f-50,f+50)]
    valid=[t for t in temps if 400<t<500];assert len(valid)==1
    record(972,valid[0],'Independent end-correction calibration and both beat-temperature branches.',
           dict(end_correction_m=e,frequency=f,possible_temperatures=temps),
           ['300 K','16.0 cm','50.0 cm','340 m/s','50 beats','400 K and 500 K','18.0 cm'])

    # Solve directly in r=X/14 using the two balance conditions.
    # e=5.6r-2.4=4/r-4 -> 5.6r²+1.6r-4=0.
    r=(-1.6+sqrt(1.6**2+4*5.6*4))/(2*5.6);e=5.6*r-2.4
    assert e>=0
    record(1203,100*r/(1+r)-30,'Eliminate end resistance to solve for the gap ratio directly.',
           dict(ratio=r,end_resistance=e,unknown_resistance=14*r),
           ['8.0 Ω','14.0 Ω','30.0 cm','50.0 cm','nonnegative contact resistance'])

    # Conductance variables make the two loading equations linear.
    # 9g1-9g2=9/6; 4.5g1-13.5g2=-4.5/6, in kΩ.
    a,b,c,d=9.,-9.,4.5,-13.5;rhs1=1.5;rhs2=-.75
    det=a*d-b*c;g1=(rhs1*d-b*rhs2)/det;g2=(a*rhs2-rhs1*c)/det
    assert g1>0 and g2>0
    result=18*g1/(g1+g2)
    record(1276,result,'Two linear node equations in conductances; no authored resistor elimination used.',
           dict(R1_kohm=1/g1,R2_kohm=1/g2,determinant=det),
           ['18.0 V','6.0 kΩ','9.0 V','4.5 V','removed completely'])

    coefficient=(5-3)/(8-4);friction=3-coefficient*4;field=sqrt(coefficient*4/.5**2)
    v=(2-friction)*8/(field*field*.5**2);current=field*.5*v/8
    record(1555,current*current*8,'Infer the field and friction, then compute the third-trial current and I²R.',
           dict(B=field,friction=friction,speed=v,current=current),
           ['0.50 m','4.0 Ω','3.0 N','4.0 m/s','5.0 N','8.0 m/s','8.0 Ω','2.0 N'])

    E1=extract(1872,r'energy ([\d.]+) MeV');E2=extract(1872,r'energy [\d.]+ MeV, while.*energy ([\d.]+) MeV')
    m1=2*1.66e-27;m2=4*1.66e-27;conv=1.60e-13
    # Relative kinetic energy is invariant under the COM boost.
    v1=sqrt(2*E1*conv/m1);v2=-sqrt(2*E2*conv/m2);mu=m1*m2/(m1+m2)
    Q=.5*mu*(v1-v2)**2/conv;V=(m1*v1+m2*v2)/(m1+m2)
    assert V>0 and max(abs(v1),abs(v2))<3e7
    record(1872,Q,'Compute the COM relative kinetic energy using the reduced mass.',
           dict(v1=v1,v2=v2,parent_velocity=V,relative_energy_MeV=Q),
           ['masses 2u and 4u','travels along +x','travels along -x','1.66×10⁻²⁷','1.60×10⁻¹³'])

    # Enumerate static diode states, and verify power conservation in each.
    def state(E,R,L,lower,upper):
        free=E*L/(R+L);X=max(lower,min(upper,free));Is=(E-X)/R;Il=X/L
        Ir=Is-Il
        reference_absorbed=X*Ir
        assert math.isclose(E*Is,Is**2*R+X*X/L+reference_absorbed,abs_tol=1e-10)
        return dict(node=X,reference_power=reference_absorbed,resistor_power=Is**2*R,free=free)
    high=state(16,100,100,2,6);low=state(0,100,100,2,6)
    record(1994,.4*high['reference_power']+.6*low['reference_power'],
           'Piecewise node solution with energy conservation checked in each state.',dict(high=high,low=low),
           ['100 Ω','+6.0 V','+2.0 V','6.0 V gives X=3.0 V','40%','60%','16.0 V','at 0 V'])

    obs=extract(2010,r'in R is ([\d.]+) W');rat=10/4-1
    preds={}
    for key,s in B[2010]['options'].items():
        L=float(s.split()[0]);R=rat*L
        h=state(24,R,L,3,8);l=state(0,R,L,3,8)
        preds[key]=(h['resistor_power']+2*l['resistor_power'])/3
    matching=[k for k,v in preds.items() if math.isclose(v,obs,rel_tol=1e-7)];assert matching==[B[2010]['correct_option']]
    result=(16**2+2*3**2)/(3*obs)/rat
    record(2010,result,'Substitute all four loads into both diode states and the measured power.',
           dict(measured=obs,predicted_powers=preds),
           ['10.0 V gives X=4.0 V','+8.0 V','+3.0 V','24.0 V','one-third','two-thirds'])

    lc=1-19/20;D=20+(6-2)*lc;d=12+(10-2)*lc
    # Enumerate the corners of three independent error bounds; include covariance explicitly.
    relative=[]
    for z,ed,ei in itertools.product((-lc,lc),(-lc/2,lc/2),(-lc/2,lc/2)):
        relative.append(abs((2*D*(z+ed)-2*d*(z+ei))/(D*D-d*d)))
    record(2103,100*max(relative),'Enumerate all eight error-bound corners for the common-offset model.',
           dict(least_count=lc,D=D,d=d,relative_error_corners=relative),
           ['20 divisions equal to 19','division 2 coincides','20 mm with division 6','12 mm with division 10','SAME additive error','half a least count','first-order'])
    assert len(rows)==14
    return rows
