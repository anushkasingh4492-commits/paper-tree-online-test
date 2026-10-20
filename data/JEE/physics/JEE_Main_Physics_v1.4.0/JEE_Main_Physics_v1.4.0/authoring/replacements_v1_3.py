"""24 replacement tasks for E02. Values are checked by a separate physical solver."""
from math import sqrt, log, asin, pi

def replacements():
    out={}
    def put(n,stem,request,value,unit,wrong,explanation,reason):
        out[n]=dict(stem=stem,request=request,value=value,unit=unit,wrong=wrong,
                    explanation=explanation,reason=reason)

    t=(sqrt(325)-5)/10
    put(98,
        'A particle is launched from (0,0) with velocity (12 i + 20 j) m/s. A smooth horizontal ceiling is at y=15 m, a smooth vertical wall is at x=18 m, and the floor is y=0. Both surfaces have coefficient of restitution 0.5 for the velocity normal to them; the tangential component is unchanged. The ceiling and wall extend far enough for every stated collision. Gravity is 10 m/s² downward; neglect air resistance.',
        'Find the x-coordinate of its first subsequent impact with the floor.',18-6*(1+t-1.5),'m',[4.8,10.8,18],
        f'The first ceiling encounter solves 20t−5t²=15 on the rising branch, giving t=1 s and vertical velocity +10 m/s. The reflected vertical velocity is −5 m/s. The wall is reached at t=1.5 s, before the floor; the particle is then at y=11.25 m. The wall changes horizontal velocity from +12 to −6 m/s. From the ceiling, 15−5τ−5τ²=0 gives τ={t:.9g} s. Hence the floor time is {1+t:.9g} s and x=18−6(1+τ−1.5)={18-6*(t-.5):.9g} m. There is no further ceiling or wall collision.',
        'Select the first ceiling root, establish collision order, apply restitution to different components, and propagate the remaining flight to the floor.')

    a=(10-sqrt(18.4))/3.4;b=(10+sqrt(18.4))/3.4;c=100/17
    x=lambda t:5+12*t-1.5*t*t
    val=x(a)-x(0)+x(b)-x(c)
    put(175,
        'For 0 ≤ t ≤ 8 s a particle has v(t)=12−3t m/s and starts at x=5 m. A detector moves along the same axis at x_D(t)=5+2t+0.2t² m. A distance recorder is active only when the particle is ahead of the detector by between 0 and 12 m, inclusive. It records the distance travelled by the particle in the laboratory frame only during those active intervals. The accompanying graph represents the particle velocity.',
        'What total distance does the recorder register?',val,'m',[12,24,48],
        f'The separation is z=x−x_D=10t−1.7t². The condition 0≤z≤12 gives [0,{a:.9g}] and [{b:.9g},{c:.9g}] s. The particle reverses at 4 s, outside both intervals: its velocity is positive on the first and negative on the second. Integrating |v| over these two intervals gives [x(a)−x(0)]+[x(b)−x(c)]={val:.9g} m. The full-interval triangle area would count inactive motion; twice the 12 m relative-distance window also fails because the detector accelerates.',
        'Find two disjoint recording intervals from relative position, locate the laboratory-frame reversal, and integrate speed only over the active intervals.')

    put(225,
        'A block of unknown mass M slides on a horizontal rough table and is connected by a light string over a smooth massless pulley to a hanging mass. In one trial a 3 kg hanging mass descends with acceleration 2 m/s². In a second trial a 2 kg hanging mass is initially moving upward and, while still moving upward, has downward acceleration 4 m/s². The kinetic friction coefficient is the same in both directions. In a third trial a 5 kg hanging mass descends from rest. After it has descended 2 m, the string is cut without an impulse; the table block then slides freely until it stops. Use g=10 m/s² and assume the third trial starts sliding as stated.',
        'Find the total distance travelled by the table block in the third trial, including the motion after the cut.',60/11,'m',[2,38/11,82/11],
        'Let the kinetic friction force be f. The two moving trials give 30−f=2(M+3) and 20+f=4(M+2), hence M=6 kg and f=12 N, so μ=0.2. The third acceleration is (50−12)/11=38/11 m/s². After 2 m, v²=152/11 m²/s². With the string cut, deceleration is f/M=2 m/s², so the additional distance is 38/11 m. Total distance = 2+38/11 = 60/11 m.',
        'Infer both mass and friction using opposite friction signs, then connect the coupled acceleration to the independent stopping stage.')

    put(263,
        'Block A (3 kg) is on a smooth 30° incline and block B (5 kg) is on a rough incline with sin β=0.6 and cos β=0.8. They are joined over a smooth massless pulley by a light inextensible string; both inclines descend away from the pulley. For B, μ_k=0.20 and μ_s=0.25. Released from rest, B moves down. After each block has moved 2 m, a 2 kg lump initially at rest relative to the incline is attached instantaneously and inelastically to A. The lump sticks; the string remains taut. During this short attachment neglect gravity and friction impulses, but include the string impulse. Thereafter the surfaces and friction coefficients are unchanged. Take g=10 m/s².',
        'How far in total does B descend before it comes to permanent rest?',86/15,'m',[2,23/3,15/2],
        'Initially the net driving force is 5×10×0.6−3×10×0.5−0.2×5×10×0.8=7 N, so a=7/8 m/s² and v²=3.5 after 2 m. Project impulse equations along the constrained directions: 8v=10v′, giving v′²=2.24. After attachment the driving force while B still descends is 30−25−8=−3 N, hence deceleration 0.3 m/s². Its additional descent is 2.24/0.6=56/15 m. At rest the gravitational imbalance is 5 N, below the maximum static friction 10 N, so it stays stopped. Total = 86/15 m.',
        'Use coupled acceleration, constrained inelastic momentum, reversed net acceleration, and a final static-friction check.')

    put(395,
        'A 3 kg particle is released from rest at x=0 on a rough horizontal line. An external force F(x)=18−2x N acts throughout, with x in metres and positive force toward increasing x. The coefficients of kinetic and static friction are 0.10 and 0.15 respectively; take g=10 m/s². Whenever the particle stops, apply the static-friction condition before deciding whether it moves again. The line is long enough for the motion.',
        'Find the total distance travelled before the particle first remains permanently at rest.',27,'m',[15,24,30],
        'Kinetic friction has magnitude 3 N and maximum static friction is 4.5 N. On the first outward leg, work is 15x−x², so the nonzero turning point is x=15 m. There |F|=12 N>4.5 N, so it returns. On a leftward leg the total force is 21−2x; zero net work from 15 gives the next stop at x=6 m. There F=6 N>4.5 N, so it moves right. With force 15−2x during that leg, the next stop is x=9 m. Here F=0 and static friction can hold it. Distance =15+9+3=27 m.',
        'Track successive turning points with friction reversing sign and test static equilibrium at each stop; the first turning point is not the final rest point.')

    w=12*10*(sqrt(3)/2)/(5*1.5)+3*10/1.5*(1-sqrt(3)/2)
    put(492,
        'A uniform rod of mass 2 kg and length 1.5 m is hinged at one end to a fixed frictionless horizontal axle. A 1 kg point mass is attached at its free end. The system is released from rest with the rod horizontal. When the rod is 60° below the horizontal, the point mass is detached without any impulse on the rod. The rod then continues freely to its first vertically downward position. Take g=10 m/s².',
        'Find the magnitude of the hinge force on the rod at that vertically downward position.',20+1.5*w,'N',[35,50,60],
        f'Before detachment, I=(2/3+1)(1.5)²=3.75 kg m² and the released potential energy at 60° is (2/2+1)gL sin60°. Thus ω_d²=12g sin60°/(5L). Detachment leaves the rod angular velocity continuous; the escaping mass carries away its own kinetic energy. For the remaining rod, ω_b²=ω_d²+3g(1−sin60°)/L={w:.9g} s⁻². At the bottom the tangential acceleration is zero; R−Mg=Mω_b²L/2. Hence R={20+1.5*w:.9g} N.',
        'Use energy with the attached mass, retain angular velocity through impulse-free detachment, then combine rod energy and centripetal force.')

    put(573,
        'Two point masses 2×10²⁰ kg and 6×10²⁰ kg initially execute a circular binary orbit of separation d=2×10⁶ m with the centre of mass at rest. Equal and opposite tangential impulses increase their relative speed instantaneously to √(3/2) times its circular value, without changing the separation. They then follow a bound Kepler orbit. At the greatest subsequent separation, another pair of equal and opposite tangential impulses makes the relative orbit circular at that separation. Use G=6.67×10⁻¹¹ N m²/kg².',
        'Find the positive work done by the second pair of impulses, in units of 10²² J.',33.35,'(10²² J)',[16.675,66.7,200.1],
        'Write μ=m₁m₂/(m₁+m₂), K=G(m₁+m₂), and use energy per unit reduced mass. Immediately after the first impulses, ε=(3K/4d)−K/d=−K/(4d) and h²=(3/2)Kd. The orbit has semimajor axis 2d and apocentre 3d. Angular momentum gives v_a²=K/(6d); circular motion there needs v_c²=K/(3d). The second work is μ(v_c²−v_a²)/2=Gm₁m₂/(12d)=3.335×10²³ J, or 33.35 in the requested units.',
        'Infer the new apsis from energy and angular momentum, then compare actual and circular kinetic energies at that apsis.')

    impulse=(3e6**3/(6.67e-11*1e8)/4)*(sqrt(2)-1)*300/1e23
    put(576,
        'Two unknown point masses form an isolated circular binary of separation 3×10⁶ m and period 2π×10⁴ s. The lighter body is observed to be three times as far from the centre of mass as the heavier body. An instantaneous tangential impulse is now applied only to the lighter body, in the direction of its initial velocity; the heavier body receives no impulse. Use G=6.67×10⁻¹¹ N m²/kg².',
        'Find the minimum impulse that makes their relative orbit just unbound, in units of 10²³ kg m/s.',impulse,'(10²³ kg m/s)',[.62878,2.51512,3.77268],
        f'The distance ratio gives m_heavy=3m_light. Circular relative motion has v_rel=2πd/P=300 m/s and total mass M=d³/(G×10⁸). Thus m_light=M/4. The impulse changes relative velocity by J/m_light, while the new centre-of-mass motion does not affect relative binding. Marginal escape at the unchanged separation requires v_rel,new=√2 v_rel. Hence J=m_light(√2−1)300={impulse:.9g}×10²³ kg m/s.',
        'Recover the masses from centre-of-mass geometry and the orbital period, then apply the escape criterion to relative motion after a one-body impulse.')

    put(811,
        'Two reversible engines operate between 900 K and an intermediate reservoir at T, and between T and 300 K. For each composite cycle the first engine absorbs 1200 J. Only 75% of its rejected heat is supplied to the second engine; the other 25% remains in the externally maintained intermediate reservoir. The two engines produce equal work. All the work of the first engine drives a reversible refrigerator that removes heat from the 300 K reservoir and rejects it to the 900 K reservoir. The second engine work is delivered to an external load.',
        'Find the net heat gained by the 300 K reservoir per composite cycle, counting both devices connected to it.',900/7,'J',[300,1200/7,2400/7],
        'The engine works are W₁=1200(1−T/900) and W₂=0.75×1200(T−300)/900. Equality gives T=4500/7 K and W₁=W₂=2400/7 J. The second engine rejects 0.75×1200×300/900=300 J to the cold reservoir. The refrigerator COP is 300/(900−300)=1/2, so it removes 1200/7 J. Net heat gained is 300−1200/7=900/7 J. The diverted intermediate heat is not sent to the second engine.',
        'Apply the heat split and equal-work constraint, then combine the engine rejection with a refrigerator heat flow of the opposite sign.')

    put(814,
        'A heat engine absorbs 1500 J per cycle from an 800 K reservoir and rejects heat only to a 300 K reservoir. Part of its work runs a reversible refrigerator between 200 K and 300 K; the remaining 500 J per composite cycle is delivered to a load. The total heat rejected to the 300 K reservoir by the engine and refrigerator together is 1400 J per composite cycle. The engine need not be reversible.',
        'Express the actual engine efficiency as a percentage of the Carnot efficiency between its reservoirs.',224/3,'%',[46.6667,62.5,93.3333],
        'For the combined system, heat removed from 200 K is Q_c=1400+500−1500=400 J. The reversible refrigerator COP=200/(300−200)=2, so its work input is 200 J. The engine therefore produces 700 J, giving η=700/1500=7/15. Its Carnot bound is 1−300/800=5/8. The requested percentage is 100(7/15)/(5/8)=224/3 %. This is below 100%, as required.',
        'Use the whole-system heat balance to determine refrigerator cooling, recover its work and the engine work, then compare efficiencies without assuming a reversible engine.')

    work=52*300*(2**(6/13)-1)
    put(887,
        'A fixed mixture contains unknown positive amounts of a monatomic and a diatomic ideal gas. In a low-temperature constant-volume calibration, a 40 K increase requires 2080 J and diatomic vibration is frozen. In a separate high-temperature constant-volume calibration of the same amounts, a 40 K increase requires 2720 J and one diatomic vibrational mode is fully active. Use C_V=3R/2, 5R/2 and 7R/2 per mole for the monatomic gas, rigid diatomic gas and vibrating diatomic gas respectively, with R=8 J/(mol K). The mixture is then prepared at 300 K and compressed reversibly and adiabatically to half its initial volume. For this final process, diatomic vibration remains frozen throughout.',
        'Find the work done on the mixture in this compression.',work,'J',[3000,4800,7200],
        f'The two total heat capacities are 52 and 68 J/K. Their difference is n_d R=16 J/K, so n_d=2 mol. From 52=(3/2)n_m R+(5/2)n_d R, n_m=1 mol. In the final process nR=24 J/K and γ−1=nR/C_V=6/13. Therefore T_f=300×2^(6/13), and W_on=ΔU=52×300(2^(6/13)−1)={work:.9g} J. The high-temperature heat capacity is used to determine composition, not for the final adiabatic path.',
        'Extract composition from the change in active degrees of freedom, choose the correct heat capacity for the final regime, then compute adiabatic work.')

    put(1017,
        'A sonometer string has length 0.50 m between bridges and linear density 0.001 kg/m. At initial tension T₀ its fundamental makes 4 beats/s with a 100 Hz fork. Multiplying the tension by 1.5625, without changing length or linear density, gives 20 beats/s with the same fork; the sign of the frequency difference is not supplied. Restore T₀, then shorten the vibrating length to 0.40 m. Tension is supplied by a hanging mass through a smooth pulley. Mass is now added until the fundamental makes 5 beats/s with a 150 Hz fork; a further very small addition of mass increases this beat frequency. Use g=10 m/s² and neglect stretching.',
        'Find the total mass added after restoring T₀, in grams.',616,'g',[384,480,961],
        'Initial candidates are 96 and 104 Hz. Multiplication by √1.5625=1.25 gives 120 or 130 Hz; only 120 gives 20 beats with 100, so f₀=96 Hz and T₀=4L²μf₀²=9.216 N. In the final trial, increasing tension increases beats, so the final string frequency is above 150: f=155 Hz, not 145. At length 0.40 m the required tension is 4×0.40²×0.001×155²=15.376 N. Added mass =(15.376−9.216)/10=0.616 kg=616 g.',
        'Resolve the first two-sided beat ambiguity, recover the initial tension, resolve a second beat branch after a length change, and subtract tensions.')

    coating=(18.432/(.3*125)**2-.002)*1000
    put(1020,
        'A string of length 0.40 m and unknown uniform linear density has tension 18.432 N. Its fundamental makes 5 beats/s with an unknown fork; a very small increase in tension from this initial setting decreases the beat frequency. Increasing the tension to 1.21 times its initial value gives 7 beats/s with the same fork. Restore the initial tension and shorten the vibrating length to 0.30 m. A uniform coating is added without changing that length or tension until the second harmonic matches the fork frequency. Neglect stiffness and assume the coating changes only the linear density.',
        'Find the added mass per unit length, in g/m.',coating,'g/m',[2,9.1072,13.1072],
        f'Initially f<F, so F=f+5. The second observation gives |1.1f−F|=7, hence |0.1f−5|=7. Only the positive solution f=120 Hz is physical, and F=125 Hz. Thus μ=18.432/(4×0.40²×120²)=0.002 kg/m. For the coated string second harmonic, F=(1/0.30)√(18.432/μ_new), so μ_new=18.432/(0.30×125)² kg/m. The added density is {coating:.9g} g/m.',
        'Use the direction of beat change and an absolute-value constraint to infer both frequencies, then infer density and the coating needed for a different harmonic.')

    put(1275,
        'In the illustrated divider, the ideal source is 12 V and the voltmeter resistance is 6 kΩ. The fixed positive resistances R1 and R2 are unknown. With the meter across R2 as drawn, it reads 6 V. In a separate measurement it is moved across R1 and reads 4 V; no other load is present in either trial. Remove the meter and connect a load R_L across R2. All resistances are ohmic.',
        'Find the smallest R_L for which the loaded output across R2 is at least 90% of its no-load value.',10.8,'kΩ',[1.2,6,12],
        'Use kΩ. The first measurement gives R1=6R2/(6+R2); the second gives R2=2×6R1/(6+R1). The unique positive solution is R1=2 kΩ, R2=3 kΩ. The output has open-circuit voltage 7.2 V and Thevenin resistance 2||3=1.2 kΩ. Its loaded/no-load ratio is R_L/(R_L+1.2). Requiring this to be at least 0.90 gives R_L≥10.8 kΩ.',
        'Solve two differently loaded divider measurements for the unknown resistances, then translate the output-tolerance condition into a minimum load.')

    qm=2e7;v=sqrt(200000**2-2*qm*600);rad=v/(qm*.4);tm=asin(.012/rad)/(qm*.4)*1e9
    put(1424,
        'An ideal positive nonrelativistic particle passes undeflected through crossed fields E=20000 V/m and B₁=0.10 T, perpendicular to its velocity. In a calibration region with perpendicular B₂=0.20 T it describes a circle of radius 0.050 m. In a separate trial the same selected particle crosses a retarding potential difference of 600 V, then enters a magnetic strip normally at its straight near boundary. The strip field has magnitude 0.40 T perpendicular to the motion plane, and its parallel boundaries are 0.012 m apart. There are no other forces or fields, and the strip is unbounded along its boundaries.',
        'Find the time from entry to the first crossing of the far boundary, in ns.',tm,'ns',[75,196.35,392.699],
        f'The selector fixes v₀=E/B₁=2×10⁵ m/s. Curvature gives q/m=v₀/(B₂r₀)=2×10⁷ C/kg. After retardation, v²=v₀²−2(q/m)600, giving v={v:.9g} m/s. In the strip ω=(q/m)B=8×10⁶ s⁻¹ and radius r=v/ω={rad:.9g} m. Since 0.012<r, the far boundary is reached on the first forward arc. Its normal displacement is r sin(ωt)=0.012, so t=asin(0.012/r)/ω={tm:.9g} ns.',
        'Infer charge-to-mass ratio from two field regions, account for energy lost to retardation, and select the first geometric exit from a finite magnetic strip.')

    put(1546,
        'A coil with unknown inductance L and positive resistance r is connected to an ideal 18 V source at t=0 with zero current. The steady current is 3 A, and the current first reaches 1.5 A at time (ln 2)/2 s. At twice that time, a switch instantaneously reverses the source polarity and inserts an extra 6 Ω in series. The coil current is continuous at switching and the circuit remains closed. Inductance is constant.',
        'Find the time after switching at which the current first becomes 0.75 A in the direction opposite to its original direction.',log(5)/4,'s',[log(2)/4,log(3)/4,log(5)/2],
        'The original steady state gives r=18/3=6 Ω. Half-growth takes (L/r)ln2=(ln2)/2, so L=3 H. At twice that time the initial-direction current is 3(1−1/4)=2.25 A. After switching, total resistance is 12 Ω and the signed steady current is −18/12=−1.5 A. Hence I=−1.5+3.75 exp(−4τ). Setting I=−0.75 gives exp(−4τ)=1/5, so τ=(ln5)/4 s. The zero crossing occurs earlier.',
        'Infer both coil parameters, propagate current to the switching instant, and solve the signed transient after changing both resistance and source polarity.')

    put(1547,
        'A coil with unknown positive resistance r and inductance L has reached steady current from an ideal 18 V source. Its stored magnetic energy is 6.75 J. In a calibration decay, the source is removed and an extra 6 Ω resistor completes the closed coil loop; the total charge passing through this resistor over the full decay is 0.375 C. In a fresh identical decay, at the instant current falls to 1 A, the 18 V source is reconnected in the original current direction while the extra 6 Ω remains. Switching is ideal and current is continuous.',
        'Find the time after reconnection for the current to reach 1.25 A, in ms.',125*log(2),'ms',[43.3217,173.287,346.574],
        'Write I₀=18/r. Energy gives (1/2)L(18/r)²=6.75, hence L=r²/24. Total decay charge is I₀L/(r+6)=0.375. Substitution gives 0.75r/(r+6)=0.375, so r=6 Ω and L=1.5 H. After reconnection the final current is 18/12=1.5 A and time constant is 1.5/12=0.125 s. From initial 1 A, I=1.5−0.5 exp(−τ/0.125). The value 1.25 A occurs after 0.125 ln2 s =125 ln2 ms.',
        'Combine independent magnetic-energy and integrated-charge measurements to infer coil parameters, then use current continuity in a new growth stage.')

    put(1556,
        'A conducting rod of mass 0.50 kg and length 0.50 m slides to the right on horizontal rails as illustrated. The uniform field into the page is 2.0 T; total closed-loop resistance is 4.0 Ω and inductance is negligible. The kinetic friction force on the rod has constant magnitude 0.50 N while it moves. A constant 2.0 N force to the right first maintains steady motion. This applied force is then removed abruptly. The rails and magnetic field extend through the entire subsequent motion; the rod eventually stops. Neglect all other losses.',
        'Find the total Joule heat generated after the applied force is removed.',3+2*log(4),'J',[3,6.45482,9],
        'Magnetic drag is bv with b=(BL)²/R=0.25 N s/m. The initial steady speed is (2−0.5)/0.25=6 m/s. During coasting, m dv/dt=−f−bv. The stopping distance is ∫₀⁶ mv/(f+bv) dv = (m/b)[6−(f/b)ln(1+6b/f)] =12−4ln4 m. Initial kinetic energy is 9 J; friction dissipates 0.5(12−4ln4) J. The rest becomes Joule heat: 9−6+2ln4=3+2ln4 J. All energy has been accounted for when the rod stops.',
        'Infer steady speed with two drag mechanisms, integrate the coasting dynamics, and separate frictional dissipation from electrical heating.')

    put(1618,
        'A plane sinusoidal electromagnetic wave in vacuum, of peak electric field 200 V/m, illuminates a flat opaque sheet of unknown actual area A at an unknown oblique angle θ to its normal (0<θ<90°). The sheet absorbs a fraction α of the incident power and reflects the rest specularly; there is no transmission. Measurements give absorbed power 0.0025488 W, time-averaged force normal to the sheet 1.58592×10⁻¹¹ N, and force parallel to the sheet 5.0976×10⁻¹² N in the direction of the incident tangential momentum. Use ε₀=8.85×10⁻¹² F/m and c=3×10⁸ m/s. The beam fully covers the sheet.',
        'Find A in cm².',1,'cm²',[.6,.8,1.25],
        'The average incident intensity is I=ε₀cE₀²/2=53.1 W/m². Let P=IA cosθ be power intercepted by the sheet. Specular reflection transfers no tangential momentum, so F_parallel=αP sinθ/c=P_abs sinθ/c. Thus sinθ=cF_parallel/P_abs=0.6 and cosθ=0.8. Normal force obeys cF_normal=(2−α)P cosθ=(2P−P_abs)cosθ. This gives P=0.004248 W and α=0.6. Therefore A=P/(I cosθ)=10⁻⁴ m²=1 cm². All inferred fractions and angles are physical.',
        'Use tangential and normal momentum transfer to infer incidence angle and intercepted power before converting intensity to actual rather than projected area.')

    put(1752,
        'Two coherent beams of the same frequency and fixed linear polarisation produce maximum intensity 49 W/m² and minimum intensity 9 W/m². At a chosen point, the optical path of the stronger beam exceeds that of the weaker by λ/6 modulo λ. A nonreflecting neutral filter is placed in the stronger beam, multiplying its intensity by 1/4 without a phase change. A transparent plate of refractive index 1.5 and thickness λ/2 is also inserted normally in that beam, replacing the same thickness of air. Here λ is the wavelength in air; ignore absorption by the plate.',
        'Find the resulting intensity at that point.',10.25-5*sqrt(3),'W/m²',[.25,10.25,18.9103],
        'Let a≥b be the original field-amplitude factors. Then a+b=√49=7 and a−b=√9=3, so a=5, b=2 and individual intensities are 25 and 4. The filter changes the stronger amplitude to 2.5. The plate adds optical path (1.5−1)λ/2=λ/4. Total path excess is λ/6+λ/4=5λ/12 and phase difference is 5π/6. Thus I=2.5²+2²+2×2.5×2 cos(5π/6)=10.25−5√3 W/m².',
        'Recover the individual amplitudes, distinguish intensity attenuation from amplitude attenuation, and combine the original and inserted optical phase differences.')

    put(1788,
        'A photoelectric apparatus displays S=aV_stop+δ, with unknown positive dimensionless gain a and unknown constant offset δ in volts. For photon energies 3 eV and 5 eV on the same metal, the readings are 0.8 V and 3.2 V respectively. In a separate measurement using 4 eV photons on this metal, the fastest photoelectrons are accelerated through an additional 2 V; their final de Broglie wavelength is √(0.0150/3.5) nm. Use λ(nm)=√[0.0150/K(eV)] for a nonrelativistic electron. The work function, gain and offset stay fixed; there are no contact-potential shifts.',
        'Find the offset δ.',.2,'V',[.1,.4,.6],
        'The stopping potential changes by 2 V when photon energy changes by 2 eV, so a=(3.2−0.8)/2=1.2. The final wavelength gives kinetic energy 3.5 eV. Removing the added 2 eV leaves emitted K_max=1.5 eV for 4 eV photons, hence the work function is 2.5 eV. At 3 eV illumination the true stopping potential is 0.5 V. Consequently δ=0.8−1.2×0.5=0.2 V. The second reading verifies 1.2×2.5+0.2=3.2 V.',
        'Separate unknown display gain from offset, infer work function from an independent accelerated-electron wavelength, and then recover the zero offset.')

    put(2043,
        'Use the illustrated ideal-diode network: node X is fed through 300 Ω and connected to ground through 600 Ω; the diode anode is at X and its cathode at a fixed +3 V reference that can absorb current. The source labelled +12 V in the diagram is now varied periodically: it rises linearly from 0 to 12 V in 0.5 s, then falls linearly to 0 in the next 0.5 s. The ideal diode has zero forward drop and no reverse current. There is no capacitance or inductance, so the circuit is in its DC state at each instant.',
        'Find the heat generated in the 300 Ω resistor during one complete cycle, in mJ.',68.125,'mJ',[70,160/9,34.0625],
        'With the diode off, V_X=2V_s/3, so conduction begins at V_s=4.5 V. Below this threshold the 300 Ω voltage is V_s/3; above it V_X=3 V and the resistor voltage is V_s−3. The triangular cycle spends equal time per voltage interval, with total dt=dV_s/12 for both ramps together. Hence Q=(1/3600)[∫₀^4.5(V_s/3)² dV_s+∫₄.₅^12(V_s−3)² dV_s] = (3.375+241.875)/3600 J=0.068125 J=68.125 mJ.',
        'Determine the diode switching threshold, derive separate resistor voltages in both states, and integrate squared voltage with the correct time weighting.')

    density=16.02/(pi/4*10.05**2*20.15/1000)
    put(2135,
        'A vernier has 20 divisions equal to 19 main-scale divisions, and one main-scale division is 1 mm. For a solid cylinder, the indicated diameter has main-scale reading 10 mm and coincidence 5; the indicated height has main-scale reading 20 mm and coincidence 7. In a separate closed-jaw calibration the indicated positive zero error is 0.15 mm. Treat each of these three indicated readings as having an independent maximum error of half a least count. The same unknown actual zero error applies to both cylinder readings. The cylinder mass is (16.01±0.01) g. All values within these error bounds are admissible; use π=3.141592654 and ignore deformation.',
        'Find the largest density in g/cm³ consistent with these bounds, using the exact cylinder-volume formula rather than a first-order percentage approximation.',density,'g/cm³',
        [16.01/(pi/4*10.1**2*20.2/1000),16.02/(pi/4*10.075**2*20.175/1000),16.02/(pi/4*10.05**2*20.2/1000)],
        f'The least count is 1−19/20=0.05 mm, so each indicated-reading error is bounded by 0.025 mm. Diameter indication is 10.25 mm and height indication is 20.35 mm. To maximize density, take mass 16.02 g, both indications at their lower bounds, and the common actual zero error at its upper bound 0.175 mm. These choices are simultaneously allowed. Thus d_min=10.05 mm and h_min=20.15 mm. The density maximum is 16.02/[π(10.05)²(20.15)/(4×1000)]={density:.9g} g/cm³. The common zero error is not an independent correction for each dimension.',
        'Convert vernier readings and their resolution bounds, handle one shared zero error consistently, and optimize the nonlinear density over simultaneous admissible limits.')

    put(2160,
        'A uniform metre-bridge wire has an unknown resistance per unit length. Its left end connection has resistance r_a and its right end connection has resistance r_b=0.003 Ω; both lie in series with the corresponding wire segments, while gap connections are ideal. An unknown resistor X in the left gap and a 4 Ω standard in the right gap balance at 61 cm from the left end of the uniform wire. After interchanging only the gap resistors, balance is at 40 cm from the same left end. Separately, X generates 90 J of heat while carrying 0.50 A for 60 s at unchanged resistance. The bridge wire diameter is measured with a screw gauge of pitch 0.5 mm and 50 circular divisions: main-scale reading 0.5 mm, circular reading 32, and positive zero error 2 divisions. Take π=3.14.',
        'Find the resistivity of the uniform bridge wire, in units of 10⁻⁸ Ω m.',5.024,'(10⁻⁸ Ω m)',[2.512,5.27834,10.048],
        'The heating trial gives X=90/(0.50²×60)=6 Ω. Let q be wire resistance per cm, and a=r_a/q, b=r_b/q be equivalent end lengths in cm. The two balances give (61+a)/(39+b)=6/4 and (40+a)/(60+b)=4/6. Solving gives a=2 cm and b=3 cm; therefore q=0.003/3=0.001 Ω/cm=0.1 Ω/m. Gauge least count is 0.01 mm, and corrected diameter is 0.5+(32−2)0.01=0.80 mm. Hence ρ=(resistance/length)×area=0.1×3.14×(0.0008)²/4=5.024×10⁻⁸ Ω m.',
        'Use heat to calibrate the gap resistor, solve two end-corrected bridge balances, recover resistance per length, and apply the corrected gauge area.')
    assert len(out)==24
    return out
