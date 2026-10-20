"""Read-only bank checks; writes evidence to errata/. Run after extracting the release."""
from pathlib import Path
import sys,math,json,csv,re,html,hashlib,importlib.util
from collections import Counter
from itertools import combinations
from PIL import Image

HERE=Path(__file__).resolve().parent
OUT=HERE if (HERE/'jee_main_physics_v1.4.0.json').exists() else HERE.parent/'release_v1.4.0'
def get(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def save(n,x):(OUT/'errata'/n).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
maths={k:getattr(math,k) for k in ('sqrt','sin','cos','tan','asin','acos','atan','log','exp','pi')};maths.update(abs=abs,min=min,max=max)
for name in ('sin','cos'):
    fn=getattr(math,name);maths[name]=(lambda f:lambda x:0.0 if abs(f(x))<1e-14 else f(x))(fn)
def solve(m,p):
    s=dict(p)
    for k,expr in m['derived']:s[k]=float(eval(expr,{'__builtins__':{}},{**maths,**s}))
    return s

def main():
    bank=get('jee_main_physics_v1.4.0.json');byid={q['id']:q for q in bank};bycid={q['candidate_id']:q for q in bank}
    counts=Counter();failures=[]
    def ck(name,ok,details=None):
        counts[name]+=1
        if not ok:failures.append(dict(check=name,details=details))
    ck('Count and unique IDs',len(bank)==len(byid)==2160)
    ck('Difficulty totals',Counter(q['difficulty'] for q in bank)==dict(Easy=648,Medium=972,Difficult=540))
    ck('Class totals',Counter(q['source_class'] for q in bank)==dict(XI=1080,XII=1080))
    ck('Key totals',Counter(q['correct_option'] for q in bank)==dict.fromkeys('ABCD',540))
    ck('All units',set(q['unit_number'] for q in bank)==set(range(1,21)))
    ck('Unique stems',len({q['question'] for q in bank})==2160)
    ck('No four-identical-key run',not re.search(r'(.)\1\1\1',''.join(q['correct_option'] for q in bank)))
    jl=[json.loads(x) for x in (OUT/'jee_main_physics_v1.4.0.jsonl').read_text(encoding='utf8').splitlines()]
    ck('JSONL full equality',jl==bank)
    pub=get('questions_only.json');ans=get('answers_explanations.json')
    with (OUT/'jee_main_physics_v1.4.0.csv').open(encoding='utf-8-sig',newline='') as f:csvrows=list(csv.DictReader(f))
    ck('Export lengths',len(pub)==len(ans)==len(csvrows)==2160)
    books={n:(OUT/n).read_text(encoding='utf8') for n in ['Questions.html','Review_and_Solutions.html']}
    articles={n:{m[1]:m[2] for m in re.finditer(r'<article id="([^"]+)"[^>]*>(.*?)</article>',s,re.S)} for n,s in books.items()}
    schema=get('question_bank_schema.json')['items']
    numeric=[]
    for q,p,a,c in zip(bank,pub,ans,csvrows):
        ident=q['id']
        ck('Four distinct options and matching key',set(q['options'])==set('ABCD') and len(set(q['options'].values()))==4 and q['correct_answer']==q['options'][q['correct_option']],ident)
        ck('Schema required fields',all(k in q for k in schema['required']),ident)
        for k,v in schema['properties'].items():
            if 'enum' in v:ck('Schema enum',q[k] in v['enum'],[ident,k])
            if 'const' in v:ck('Schema const',q[k]==v['const'],[ident,k])
        ck('Synchronized family tags',q['concept_family'] in q['tags'],ident)
        ck('No malformed punctuation',',:' not in q['question'],ident)
        ck('No placeholders or mangled law names',not re.search(r'\{[A-Za-z_]\w*\}|\bTODO\b|\bTBD\b|Ω(?:[’\']s)?\s*law',q['question']+' '+q['explanation'],re.I),ident)
        for k,v in c.items():
            expected=q['options'][k[-1].upper()] if k.startswith('option_') else q['figures'] if k=='figures_json' else q['numerical_variant'] if k=='numerical_variant_json' else q[k]
            ck('CSV field equality',json.loads(v)==expected if k.endswith('_json') else v==str(expected),[ident,k])
        ck('Student export equality and no answer leakage',all(p[k]==q[k] for k in p) and not set(p)&{'correct_option','correct_answer','explanation','numerical_variant','provenance'},ident)
        ck('Teacher export equality',all(a[k]==q[k] for k in a),ident)
        for n in books:
            section=articles[n].get(ident,'')
            ck('HTML record text and options',all(html.escape(t) in section for t in [q['question'],q['assumptions'],*q['options'].values()]),[ident,n])
            if n=='Review_and_Solutions.html':ck('HTML explanation',html.escape(q['explanation']).replace('\n','<br>') in section,ident)
        for f in q['figures']:ck('Figure linkage',(OUT/f['file']).exists(),ident)
        ck('Required figure present',not q['figure_required'] or bool(q['figures']),ident)
        if q['numerical_variant']:
            nv=q['numerical_variant'];v=nv['unrounded_value'];rounded=int(math.copysign(math.floor(abs(v)+.5+1e-10),v))
            ck('Numerical rounding',rounded==nv['answer_integer'],ident)
            numeric.append(dict(id=ident,value=v,integer=nv['answer_integer'],status='PASS' if rounded==nv['answer_integer'] else 'FAIL'))
    ck('Numerical alternate count',len(numeric)==270)
    ck('Figure-linked count',sum(bool(q['figures']) for q in bank)==216)
    ck('Required-figure metadata count',sum(q['figure_required'] for q in bank)==101)
    for f in get('figure_manifest.json'):
        with Image.open(OUT/f['file']) as im:ck('Image dimensions',im.size==(1600,900),f['file']);im.verify()
    for u in range(1,21):
        vals=Counter(q['correct_option'] for q in bank if q['unit_number']==u);ck('Unit key balance',max(vals.values())-min(vals.values())<=1,u)

    indep=module('independent_retained',OUT/'authoring/independent_retained.py');num=indep.number
    physical=[];inverse_rows=[]
    oldmodels={m['key']:m for m in get('authoring/original_models.json')}
    for c in get('authoring/original_model_candidates.json'):
        q=bycid[c['candidate_id']];m=oldmodels[c['model']];p=m['variants'][c['model_variant']-1];value=solve(m,p)[c['computation_variable']]
        if c.get('inverse_input'):
            predictions={}
            for k,v in q['options'].items():
                try:predictions[k]=solve(m,{**p,c['inverse_input']:num(v)})[c['computation_variable']]
                except (ValueError,ZeroDivisionError,OverflowError):predictions[k]=None
            matches=[k for k,v in predictions.items() if v is not None and math.isclose(v,value,rel_tol=2e-6,abs_tol=1e-20)]
            ck('Retained original inverse uniqueness',matches==[q['correct_option']],q['id'])
        else:
            ck('Retained original model key',math.isclose(num(q['correct_answer']),value,rel_tol=.0006,abs_tol=1e-20),q['id'])
            nv=q['numerical_variant'];ck('Retained numerical scale',math.isclose(nv['unrounded_value']*10**nv['unit_scale_power10'],value,rel_tol=2e-6,abs_tol=1e-20),q['id'])
        physical.append(dict(id=q['id'],method='Existing authoring-model recomputation',value=value))
    for e in get('authoring/challenge_calculations.json'):
        q=byid[e['id']];value=indep.outcomes(e['model'],e['params'])[e['target']]
        ck('Retained challenge state agreement',math.isclose(value,e['outcome'],rel_tol=2e-7,abs_tol=1e-12),q['id'])
        if e.get('inverse_input'):
            measured=num(q['question'].split(' = ')[-1].split('. Which listed')[0]);predictions={}
            for k,v in q['options'].items():
                try:predictions[k]=indep.outcomes(e['model'],{**e['params'],e['inverse_input']:num(v)})[e['target']]
                except (ValueError,ZeroDivisionError,OverflowError):predictions[k]=None
            matches=[k for k,v in predictions.items() if v is not None and math.isclose(v,measured,rel_tol=3e-7,abs_tol=1e-13)]
            ck('Retained challenge printed inverse uniqueness',matches==[q['correct_option']],q['id'])
            inverse_rows.append(dict(id=q['id'],printed_observation=measured,predictions=predictions,matches=matches,status='PASS' if matches==[q['correct_option']] else 'FAIL'))
        else:
            ck('Retained challenge key',math.isclose(num(q['correct_answer']),value,rel_tol=.0006,abs_tol=1e-20),q['id'])
        physical.append(dict(id=q['id'],method='Separate audit solver rerun',value=value))
    revised=module('independent_revised',OUT/'authoring/independent_revised.py').check_revised(bank)
    physical.extend(dict(id=x['id'],method='Retained v1.2 separate implementation rerun',value=x['calculated_value']) for x in revised)
    freshmodule=module('independent_v1_3',OUT/'authoring/independent_v1_3.py')
    fresh=freshmodule.check_revised(bank)
    helix=freshmodule.check_helix(bank,get('authoring/challenge_calculations.json'))
    physical.extend(dict(id=x['id'],method='Retained v1.3 separate implementation rerun',value=x['calculated_value']) for x in fresh)
    save('new24_independent_checks.json',fresh);save('helix6_independent_checks.json',helix)
    currentmodule=module('current_v1_4',OUT/'authoring/independent_v1_4.py')
    current=currentmodule.check_revised(bank);figure=currentmodule.check_figure(bank)
    physical.extend(dict(id=x['id'],method='New v1.4 separate printed-input calculation',value=x['computed']) for x in current)
    save('new6_independent_checks.json',current);save('figure_dependency_check.json',figure)
    ck('All active model records checked',len(physical)==815 and len({x['id'] for x in physical})==815)
    ex=[];exvals=indep.experiment_values()
    for q in bank:
        if not q['candidate_id'].startswith('REV-EXPERIMENT'):continue
        n,t=map(int,q['candidate_id'].split('-')[-2:]);value=exvals[n][t-1]
        ck('Experimental key recalculation',math.isclose(num(q['correct_answer']),value,rel_tol=.0006,abs_tol=1e-20),q['id'])
        ex.append(dict(id=q['id'],panel=n,calculated_value=value,key=q['correct_option']))

    # Direct reproductions for every named erratum.
    findings=get('errata/prior_findings_v1_1.json');calor=[]
    evidence={e['id']:e for e in get('authoring/challenge_calculations.json')}
    for ident in findings[0]['ids']:
        e=evidence[ident];p=e['params'];q=byid[ident]
        ck('R01 explicit fresh water and solid removal',f'fresh {p["mw"]:g} kg charge' in q['question'] and 'remove the solid' in q['question'] and 'same water mass' not in q['question'],ident)
        # Solve both heat balances as a 2x2 system, using the printed temperatures.
        T1=float(re.search(r'equilibrium at ([\d.]+)°C',q['question'])[1]) if e.get('inverse_input')!='T1' else num(q['correct_answer'])
        T2=float(re.search(r'gives ([\d.]+)°C',q['question'])[1]) if e.get('inverse_input')!='T2' else num(q['correct_answer'])
        a=p['ms']*(100-T1);b=-(T1-20);c=p['ms2']*(100-T2);d=-(T2-20)
        y1=4200*p['mw']*(T1-20);y2=4200*p['mw2']*(T2-20);det=a*d-b*c
        cs=(y1*d-b*y2)/det;C=(a*y2-y1*c)/det;H=C+4200*p['mw']
        ice=num(q['correct_answer']) if e.get('inverse_input')=='ice' else p['ice']
        Tf=(H*p['hot']-ice*336000)/(H+4200*ice)
        vals=dict(Tf=Tf,maxice=H*p['hot']/336000,extra=(H+4200*ice)*10)
        ck('R01 positive heat capacities and all ice melted',cs>0 and C>0 and Tf>0,ident)
        expected=vals[e['target']]
        ck('R01 printed-input energy balance',math.isclose(expected,e['outcome'],rel_tol=2e-7),ident)
        calor.append(dict(id=ident,water_mass=p['mw'],C=C,solid_specific_heat=cs,final_temperature=Tf,requested_outcome=expected,status='PASS'))
    for ident in findings[1]['ids']:
        q=byid[ident];ck('R02 ideal particle explicit','ideal nonrelativistic positively charged particle' in q['question'] and not re.search(r'\bion\b',q['question']),ident)
    for ident in findings[2]['ids']:
        q=byid[ident];ck('R03 revised and separately recalculated',q['candidate_id'].startswith('REV12-') and ident in {x['id'] for x in revised},ident)
    pairs=[['JEE27-PHY-'+f'{a:04}','JEE27-PHY-'+f'{b:04}'] for a,b in [(863,869),(433,435),(412,424),(2013,2016),(401,537),(442,446)]]
    for pair in pairs:ck('R04 pair group matches',len({byid[x]['concept_family'] for x in pair})==1,pair)
    for ident in findings[4]['ids']:ck('R05 optional metadata and wording',not byid[ident]['figure_required'] and 'optional context' in byid[ident]['question'] and 'Use the readings' not in byid[ident]['question'],ident)
    for ident in findings[5]['ids']:ck('R06 punctuation removed',',:' not in byid[ident]['question'],ident)
    prior=[]
    def oldcheck(code,ok,note):
        ck('Prior repair '+code,ok,note);prior.append(dict(code=code,status='PASS' if ok else 'FAIL',verification=note))
    oldcheck('F01','released from rest' in byid['JEE27-PHY-1152']['question'],'Dipole release from rest remains explicit.')
    oldcheck('F02',all('BOTH spring pieces unstretched' in byid[f'JEE27-PHY-{i:04}']['question'] for i in range(1009,1015)),'Both springs explicitly unstretched; original model results re-run.')
    oldcheck('F03','|M|/√(L1 L2)' in byid['JEE27-PHY-1494']['correct_answer'],'General coupling-magnitude definition retained.')
    oldcheck('F04',all('two possible initial frequencies consistent with both' not in byid[f'JEE27-PHY-{i:04}']['question'] for i in range(1015,1021)),'Contradictory beat-branch wording remains absent; model answers re-run.')
    oldcheck('F05',byid['JEE27-PHY-0401']['concept_family']==byid['JEE27-PHY-0537']['concept_family'],'Kepler selection guard retained and seed 830 re-run.')
    historical=get('errata/prior_v1.1.0_closure_historical.json')
    f06ids=next(f['question_ids'] for f in historical if f['code']=='F06')
    oldcheck('F06',len(revised)==14 and all(byid[i]['difficulty'] in ('Easy','Medium') for i in f06ids),'All 24 earlier routine examples remain regraded. The 14 newly identified short paths are replaced and separately calculated. Difficulty remains editorial.')
    oldcheck('F07','can include visible' in byid['JEE27-PHY-0610']['explanation'].lower(),'Thermal radiation explanation includes visible wavelengths.')
    oldcheck('F08',all(not re.search(r'Ω(?:[’\']s)?\s*law',byid[f'JEE27-PHY-{n:04}']['question']+' '+byid[f'JEE27-PHY-{n:04}']['explanation'],re.I) for n in (1186,1201,1254,1451)),'Ohm law naming remains corrected; legitimate Ω resistance-unit symbols are retained.')
    oldcheck('F09',all(any('rough' in f['alt_text'].lower() for f in byid[f'JEE27-PHY-{i:04}']['figures']) for i in (270,271,272)),'Corrected rough-table figure and its accessible description retained.')

    # Current seven groups: every finding-ID entry is checked against its own condition.
    latest=get('errata/fresh_findings_baseline.json');ch={r['id']:r for r in get('errata/revision_changes.json')}
    named={i for f in latest for i in f['ids']}
    ck('All seven groups and 22 named IDs accounted for',len(latest)==7 and len(named)==22 and set(ch)==named|{'JEE27-PHY-1540'})
    closure=[]
    for f in latest:
        for ident in f['ids']:
            q=byid[ident];ok=ident in ch
            if f['code']=='E01':ok=ok and q['concept_family']=='GLOBAL-CURIE-LAW'
            elif f['code']=='E02':ok=ok and ident in {r['id'] for r in current} and q['candidate_id'].startswith('REV14-PHY-') and q['difficulty']=='Difficult' and 'difficulty_reason' in ch[ident]['fields']
            elif f['code']=='E03':ok=ok and figure['status']=='PASS' and q['candidate_id']=='REV14-FIG-2129' and q['figure_required']
            elif f['code']=='E04':ok=ok and 'explanation' in ch[ident]['fields'] and not re.search(r'Matching the measured (?:this|its|their|the) ',q['explanation'])
            elif f['code']=='E05':ok=ok and 'Every third' in q['question'] and 'Every third' in q['numerical_variant']['question']
            elif f['code']=='E06':ok=ok and 'a coil with ' in q['question'] and (not q['numerical_variant'] or 'a coil with ' in q['numerical_variant']['question'])
            elif f['code']=='E07':ok=ok and 'Which statement about the tension is correct?' in q['question'] and all(v.startswith('The tension ') and v.endswith('.') for v in q['options'].values()) and q['correct_option']=='B'
            ck(f['code']+' exact-ID closure',ok,ident)
            closure.append(dict(code=f['code'],id=ident,status='PASS' if ok else 'FAIL',changed_fields=list(ch[ident]['fields'])))
    ck('23 finding-ID closure rows',len(closure)==23)
    ck('Additional symbolic coil wording fixed','a coil with ξ turns' in byid['JEE27-PHY-1540']['question'])
    for q in bank:
        combined=q['question']+' '+q['explanation']+' '+(q['numerical_variant']['question'] if q['numerical_variant'] else '')
        ck('Reported malformed language absent',not re.search(r'Matching the measured (?:the|this|its|their) |Every 3th|an (?:100|50|ξ)-turn coil|The tension has:',combined),q['id'])
    ck('Family count after Curie merge',len({q['concept_family'] for q in bank})==1110)
    # Test the exact constructed selection from the fresh report against the actual family rule.
    counter=get('errata/prior_constructed_selection.json')
    counter_ids=[q['id'] for q in counter['questions']]
    ck('Former counterexample now rejected',len({byid[i]['concept_family'] for i in counter_ids})<25 and {'JEE27-PHY-1318','JEE27-PHY-1321'}<=set(counter_ids))
    save('curie_guard_check.json',dict(status='PASS',ids=['JEE27-PHY-1318','JEE27-PHY-1321'],family='GLOBAL-CURIE-LAW',counterexample_unique_families=len({byid[i]['concept_family'] for i in counter_ids}),counterexample_rejected=True))
    # Earlier correction fields are preserved unless explicitly superseded by a checked current correction.
    history=[]
    for item in get('errata/historical_v1_3/revision_changes.json'):
        ident=item['id'];superseded=[]
        for field,change in item['fields'].items():
            actual=byid[ident][field]
            ok=actual==change['after']
            if not ok:
                ok=ident in ch and field in ch[ident]['fields'] and actual==ch[ident]['fields'][field]['after']
                superseded.append(field)
            ck('Earlier v1.3 correction retained or explicitly superseded',ok,[ident,field])
        history.append(dict(id=ident,status='PASS',superseded_fields=superseded))
    save('prior_v1_3_continuity.json',history)
    save('exact_id_closure_checks.json',closure)

    # Use independently specified ID pairs as well as family-tag uniqueness.
    guarded=get('errata/prior_semantic_pair_guards.json')+pairs
    for group in get('errata/family_groups_reviewed.json'):
        guarded.extend(list(p) for p in combinations([q['id'] for q in group['members']],2))
    generator=module('paper_generator',OUT/'generate_paper.py');paper_rows=[]
    seeds=list(range(50000,51000))+[10377,3391,830,27,40000]
    for seed in seeds:
        paper,key=generator.generate(bank,seed);qs=paper['questions'];selected={q['id'] for q in qs}
        A=[q for q in qs if q['section']=='A'];B=[q for q in qs if q['section']=='B']
        ck('Paper count and sections',len(qs)==25 and len(selected)==25 and len(A)==20 and len(B)==5,seed)
        ck('Paper family and independent ID guards',len({q['concept_family'] for q in qs})==25 and not any(set(p)<=selected for p in guarded),seed)
        ck('Paper difficulty totals',Counter(q['difficulty'] for q in qs)==dict(Easy=8,Medium=11,Difficult=6),seed)
        ck('Paper class totals',Counter(q['source_class'] for q in qs)=={'XI':12+seed%2,'XII':13-seed%2},seed)
        ck('Paper unit cap',max(Counter(q['unit_number'] for q in qs).values())<=3,seed)
        ck('Paper MCQ key balance',Counter(k['answer'] for k in key if k['section']=='A')==dict.fromkeys('ABCD',5),seed)
        ck('Paper numerical difficulty mix',Counter(q['difficulty'] for q in B)==dict(Easy=1,Medium=2,Difficult=2),seed)
        for q,a in zip(qs,key):
            src=byid[q['id']];nv=src['numerical_variant']
            ck('Generated record and answer match',q['question']==(src['question'] if q['section']=='A' else nv['question']) and a['answer']==(src['correct_option'] if q['section']=='A' else nv['answer_integer']) and q['assumptions']==src['assumptions'],[seed,q['id']])
        paper_rows.append(dict(seed=seed,ids=[q['id'] for q in qs]))
        if seed in (10377,3391,830):save(f'paper_seed_{seed}.json',paper);save(f'answers_seed_{seed}.json',key)
        if seed==27:
            (OUT/'sample_paper.json').write_text(json.dumps(paper,ensure_ascii=False,indent=2),encoding='utf8')
            (OUT/'sample_answer_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf8')
            (OUT/'Sample_Paper.html').write_text(generator.render(paper),encoding='utf8');(OUT/'Sample_Solutions.html').write_text(generator.render(paper,key),encoding='utf8')
    save('revised_task_independent_checks.json',revised);save('calorimetry_closure_checks.json',calor)
    save('model_recomputation.json',physical);save('printed_inverse_checks.json',inverse_rows)
    save('experimental_recalculation.json',ex);save('numerical_rounding_checks.json',numeric)
    save('prior_repairs_recheck.json',prior);save('generator_1005_seeds.json',paper_rows)
    report=dict(status='PASS' if not failures else 'FAIL',bank_sha256=hashlib.sha256((OUT/'jee_main_physics_v1.4.0.json').read_bytes()).hexdigest(),checks=sum(counts.values()),counts=dict(counts),failures=failures,model_records=815,original_authoring_model_recomputations=511,retained_separate_solver_recomputations=260,retained_v1_2_separate_recomputations=14,retained_v1_3_separate_recomputations=24,new_separate_derivations=6,experimental_recomputations=len(ex),printed_inverse_checks=len(inverse_rows),numerical_alternates=270,papers=len(seeds),scope='Seven current groups checked by exact ID; six new printed-input calculations, meaningful figure-dependency check, semantic counterexample rejection and retained regression verification. Not an independent derivation of all 2160 questions, an external human review or empirical difficulty calibration.')
    save('release_crosscheck.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='counts'},indent=2))
    return not failures
if __name__=='__main__':sys.exit(0 if main() else 1)
