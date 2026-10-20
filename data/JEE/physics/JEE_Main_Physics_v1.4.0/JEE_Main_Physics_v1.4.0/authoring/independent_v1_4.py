"""Separate calculations from current printed inputs; no authoring module imported."""
import math,re
from fractions import Fraction as F
def root(fn,a,b):
 fa=fn(a);assert fa*fn(b)<=0
 for _ in range(90):
  c=(a+b)/2;fc=fn(c)
  if fa*fc<=0:b=c
  else:a=c;fa=fc
 return (a+b)/2
def integrate(fn,a,b,n=12000):
 h=(b-a)/n
 return h/3*(fn(a)+fn(b)+sum((4 if j%2 else 2)*fn(a+j*h) for j in range(1,n)))

def check_revised(bank):
 B={int(q['id'][-4:]):q for q in bank};rows=[]
 def record(n,value,method,detail,anchors):
  q=B[n]
  for anchor in anchors:assert anchor in q['question'],(n,anchor)
  values={k:float(v.split()[0]) for k,v in q['options'].items()}
  matches=[k for k,v in values.items() if math.isclose(v,value,rel_tol=6e-6,abs_tol=1e-8)]
  assert matches==[q['correct_option']],(n,value,values,matches)
  assert min(values,key=lambda k:abs(values[k]-value))==q['correct_option']
  nv=q['numerical_variant']
  if nv:
   assert math.isclose(nv['unrounded_value']*10**nv['unit_scale_power10'],value,rel_tol=1e-10)
   assert nv['parent_candidate']==q['candidate_id']
  rows.append(dict(id=q['id'],computed=value,matching_options=matches,key=q['correct_option'],method=method,details=detail,printed_anchors=anchors,status='PASS'))
 # Enumerate the two beat branches, rejecting a negative physical frequency.
 first=[(F(4)+sign*20)/(F(5,4)-1) for sign in [-1,1]]
 physical=[f for f in first if f>0];assert physical==[96]
 speed=2*F(1,2)*physical[0]/F(6,5)
 final_options=[250-5,250+5];selected=[f for f in final_options if f<250];assert selected==[245]
 length=speed/selected[0];shift=float(100*(F(1,2)-length))
 record(1015,shift,'Exact-rational beat-branch enumeration and harmonic geometry.',dict(initial_candidates=list(map(float,first)),wave_speed=float(speed),final_harmonic_candidates=final_options,final_length=float(length)),['0.50 m','4 beats/s','very small increase in tension decreases','1.5625','20 beats/s','44%','second harmonic','5 beats/s','250 Hz','inward movement decreases'])
 # Eliminate both speed and charge-to-mass ratio using the two energy differences.
 a1=.30*.040;a2=.20*.030;a3=.50*.010
 ratio=(a2*a2-a3*a3)/(a1*a1-a2*a2)
 delta=600*ratio
 k=1200/(a1*a1-a2*a2);v0=k*a1;v1=k*a2;v2=k*a3
 assert math.isclose((v0*v0-v1*v1)/(2*k),600)
 assert math.isclose((v1*v1-v2*v2)/(2*k),delta)
 record(1427,delta,'Ratio of work-energy equations eliminates unknown speed and charge-to-mass ratio; then check absolute energies.',dict(charge_to_mass=k,initial_speed=v0,after_600V_speed=v1,tangent_speed=v2,additional_potential=delta),['same unknown speed','0.040 m','0.30 T','600 V','0.030 m','field of 0.20 T','(600+ΔV) V','0.50 T','0.010 m','touches the far boundary tangentially'])
 # Integrate the resistor heat rather than assuming the switching current.
 resistance=18/3;L=(18-resistance*1)/4;tau=L/(resistance+6)
 current_decay=lambda t:3*math.exp(-t/tau)
 time_decay=root(lambda t:integrate(lambda s:6*current_decay(s)**2,0,t)-3,0,1)
 initial=current_decay(time_decay);steady=-18/(resistance+6)
 current_after=lambda t:steady+(initial-steady)*math.exp(-t/tau)
 time_after=root(lambda t:current_after(t)+.50,0,2)
 record(1548,time_after,'Numerical integration to the heat-trigger time, then root of the signed transient.',dict(coil_resistance=resistance,inductance=L,decay_time=time_decay,current_at_switch=initial,time_constant=tau,final_current=current_after(time_after)),['18 V','steady current is 3 A','4 A/s','equals 1 A','extra 6 Ω','reaches 3 J','opposite to the original current direction','current is continuous','0.50 A'])
 # Brute-force order pairs rather than using an LCM/count formula.
 l1=500e-9;l2=600e-9;D_over_d=.002/l1;opd=(1.50-1)*1.50e-6
 w1=.048/2;w2=w1*l2/l1;points=[]
 for m in range(-50,51):
  for n in range(-50,51):
   if abs(m*l1-n*l2)>1e-14:continue
   y=(m*l1-opd)*D_over_d
   if abs(y)<w1-1e-12 and abs(y)<w2-1e-12:points.append(dict(m=m,n=n,y_mm=y*1000))
 record(1745,len(points),'Enumerate both integer-order equations and check each point against both open envelopes.',dict(points=points,half_widths_mm=[w1*1000,w2*1000],extra_path_nm=opd*1e9),['500 nm','600 nm','2.0 mm','48 mm','index 1.50','thickness 1.50 μm','same for both wavelengths','dy/D+(n−1)t','strictly inside','integer multiples of 2π'])
 # Time-domain integration includes both rising and falling diode branches.
 R=800*(4/2-1);Vref=(12/R-.005)/(1/R+1/800)
 supply=lambda t:16*t if t<=1 else 16*(2-t)
 diode=lambda t:max(0,(supply(t)-Vref)/R-Vref/800)
 charge=integrate(diode,0,2)
 assert 2<Vref and math.isclose((12-Vref)/R-Vref/800,.005)
 record(2046,charge*1000,'Infer parameters from DC tests and integrate the positive diode current in time.',dict(series_R=R,reference=Vref,threshold=Vref*(1+R/800),charge_C=charge),['800 Ω','source voltage 4 V','X is at 2 V','source voltage 12 V','5.0 mA','0 to 16 V in 1.0 s','next 1.0 s','2.0 s cycle'])
 # Constant-volume elimination gives d_new^4/d_old^4 = R_old/R_new.
 original=F(6)*40/60;parallel=F(6)*25/75;S=1/(1/parallel-1/original)
 final_R=F(13)*50/50-S;diameter=F(1,2)+(32-2)*F(1,2)/50
 final_d=float(diameter)*float(original/final_R)**.25
 record(2159,final_d,'Three balance equations and direct resistance-diameter relation at fixed volume.',dict(original_R=float(original),parallel_R=float(parallel),S=float(S),stretched_R=float(final_R),corrected_diameter=float(diameter),resistance_ratio=float(final_R/original)),['6 Ω','40 cm','25 cm','without loss of volume','resistivity is unchanged','13 Ω','50 cm','pitch 0.50 mm','50 circular divisions','sleeve reading 0.50 mm','circular reading 32','positive zero error was 2'])
 return rows

def check_figure(bank):
 q=next(q for q in bank if q['id']=='JEE27-PHY-2129')
 assert 'shifted 1 cm toward the knife edge' in q['question'] and 'shifted 1 cm to the right' not in q['question']
 assert q['figure_required'] and q['figures'][0]['file']=='figures/experiment-04.png'
 assert q['correct_option']=='C' and q['options']['C']=='Move m2 2 cm to the left'
 # Current diagram: x1<0. Moving inward gives dx1>0. Reflecting the diagram
 # reverses the absolute direction while all printed scalar data stay identical.
 cases=[dict(m1_side='left',dx1_cm=1,dx2_cm=-2,key='C'),dict(m1_side='right',dx1_cm=-1,dx2_cm=2,key='A')]
 for c in cases:assert 2*c['dx1_cm']+c['dx2_cm']==0
 return dict(id=q['id'],status='PASS',cases=cases,without_figure_possible_options=['A','C'],necessary_visual_information='Which side of the knife edge carries m1.',check='The actual image places m1 on the left; its reflected arrangement requires the other direction.')
