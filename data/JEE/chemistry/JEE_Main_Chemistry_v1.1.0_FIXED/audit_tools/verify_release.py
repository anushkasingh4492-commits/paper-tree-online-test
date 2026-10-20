"""Run from the extracted release: python audit_tools/verify_release.py."""
from pathlib import Path
import json,math,csv,collections,hashlib,re,importlib.util
from independent_models import recompute
P=Path(__file__).resolve().parents[1]
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
b=read('jee_main_chemistry_v1.1.0.json');byid={q['id']:q for q in b}
assert len(b)==len(byid)==2160
assert collections.Counter(q['difficulty'] for q in b)=={'Easy':648,'Medium':972,'Difficult':540}
assert collections.Counter(q['source_class'] for q in b)=={'XI':1080,'XII':1080}
assert collections.Counter(q['correct_option'] for q in b)==dict.fromkeys('ABCD',540)
assert collections.Counter(q['difficulty'] for q in b if q['numerical_variant'])=={'Easy':12,'Medium':108,'Difficult':150}
numeric=0
for q in b:
 assert len(set(q['options'].values()))==4 and q['correct_answer']==q['options'][q['correct_option']]
 assert all((P/f['file']).is_file() for f in q['figures'])
 if q['calculation']:
  c=q['calculation'];r=recompute(q,c['inputs']);assert math.isclose(r,c['result'],rel_tol=1e-8,abs_tol=1e-8),q['id']
  opts={k:float(re.match(r'^[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?',v.replace('−','-'),re.I).group()) for k,v in q['options'].items()}
  assert min(opts,key=lambda k:abs(opts[k]-r))==q['correct_option'],q['id']
  assert len(set(opts.values()))==4
  if q['numerical_variant']:
   n=q['numerical_variant'];scaled=r*10**n['unit_scale_power10'];rounded=math.floor(scaled+.5) if scaled>=0 else math.ceil(scaled-.5)
   assert math.isclose(scaled,n['unrounded_value'],rel_tol=1e-8,abs_tol=1e-8) and rounded==n['answer_integer']
  numeric+=1
assert numeric==1450
assert [json.loads(s) for s in (P/'jee_main_chemistry_v1.1.0.jsonl').read_text(encoding='utf8').splitlines()]==b
with (P/'jee_main_chemistry_v1.1.0.csv').open(encoding='utf-8-sig',newline='') as h:cs=list(csv.DictReader(h))
assert len(cs)==2160
for x,q in zip(cs,b):
 for k,v in q.items():assert x[k]==(json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,bool)) or v is None else str(v))
for name in ['questions_only.json','answers_and_explanations.json']:
 records=read(name);assert len(records)==2160
 for record,q in zip(records,b):assert all(q[k]==v for k,v in record.items())
manifest=read('manifest.json')
for record in manifest['files']:
 path=P/record['path'];assert path.stat().st_size==record['bytes'];assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],record['path']
for line in (P/'checksums.sha256').read_text(encoding='utf8').splitlines():
 sha,name=line.split('  ',1);assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha,name
with (P/'Errata_Closure_Register.csv').open(encoding='utf-8-sig',newline='') as h:closure=list(csv.DictReader(h))
assert len(closure)==1195 and all(r['Closure_test']=='PASS' and r['Question_ID'] in byid for r in closure)
assert len(read('practical_coverage_crosswalk.json'))==39
assert all(e['evidence_ids'] for e in read('practical_coverage_crosswalk.json'))
spec=importlib.util.spec_from_file_location('packaged_generator',P/'generate_paper.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
seeds=list(range(1000))+[2026,9072026,99999,2**31-1,123456789]
for seed in seeds:
 paper,answers=g.generate(b,seed);qs=paper['questions'];a=qs[:20];bb=qs[20:];deps=set()
 assert len(qs)==25 and len(set(q['id'] for q in qs))==25
 assert collections.Counter(q['difficulty'] for q in qs)=={'Easy':8,'Medium':11,'Difficult':6}
 assert collections.Counter(q['difficulty'] for q in bb)=={'Easy':1,'Medium':2,'Difficult':2}
 assert collections.Counter(byid[q['id']]['correct_option'] for q in a)==dict.fromkeys('ABCD',5)
 assert collections.Counter(q['source_class'] for q in qs)=={'XI':12+seed%2,'XII':13-seed%2}
 assert max(collections.Counter(q['unit_number'] for q in qs).values())<=3
 for q,ans in zip(qs,answers):
  assert not deps.intersection(q['family_dependencies']);deps.update(q['family_dependencies'])
  original=byid[q['id']];assert q['figures']==original['figures']
  if q['section']=='A':assert q['question']==original['question'] and q['options']==original['options'] and ans['answer']==original['correct_option']
  else:assert q['question']==original['numerical_variant']['question'] and 'options' not in q and ans['answer']==original['numerical_variant']['answer_integer']
print(json.dumps({'status':'PASS','questions':len(b),'numeric_recalculations':numeric,'generator_seeds':len(seeds),'manifest_files':len(manifest['files']),'closure_rows':len(closure)}))
