"""Generate one Physics section: 20 MCQs and five numerical answers, +4/-1/0."""
from pathlib import Path
import json,random,collections,html,argparse
ROOT=Path(__file__).resolve().parent
def generate(bank,seed=1):
 rng=random.Random(seed)
 # Eight easy, eleven medium, six difficult items across 25 questions.
 # Numerical slots use one Easy, two Medium and two Difficult alternates.
 for attempt in range(3000):
  selected=[];families=set();units=collections.Counter();classes=collections.Counter();keys=collections.Counter()
  classlimit={'XI':12+seed%2,'XII':13-seed%2}
  pools={d:[q for q in bank if q['difficulty']==d] for d in ['Easy','Medium','Difficult']}
  numeric=[q for q in bank if q.get('numerical_variant')]
  slots=[('B','Easy')]+[('B','Medium')]*2+[('B','Difficult')]*2+[('A','Easy')]*7+[('A','Medium')]*9+[('A','Difficult')]*4
  # Select scarce numerical items first, then interleave the remaining levels.
  tail=slots[5:];rng.shuffle(tail);slots=slots[:5]+tail
  for section,diff in slots:
   candidates=[q for q in ([q for q in numeric if q['difficulty']==diff] if section=='B' else pools[diff]) if q['concept_family'] not in families and units[q['unit_number']]<3 and classes[q['source_class']]<classlimit[q['source_class']] and (section=='B' or keys[q['correct_option']]<5)]
   if not candidates:break
   q=rng.choice(candidates);selected.append((section,q));families.add(q['concept_family']);units[q['unit_number']]+=1;classes[q['source_class']]+=1
   if section=='A':keys[q['correct_option']]+=1
  if len(selected)==25 and set(keys.values())=={5}:break
 else:raise RuntimeError('No paper satisfying the requested constraints found')
 a=[q for s,q in selected if s=='A'];b=[q for s,q in selected if s=='B'];rng.shuffle(a);rng.shuffle(b)
 paper=[];answer=[]
 for j,q in enumerate(a+b,1):
  section='A' if j<=20 else 'B'
  r={k:q[k] for k in ['id','source_class','unit_number','difficulty','assumptions','figures','concept_family']}
  r.update(number=j,section=section,question=q['question'] if section=='A' else q['numerical_variant']['question'])
  if section=='A':r['options']=q['options']
  paper.append(r)
  answer.append({'number':j,'id':q['id'],'section':section,'answer':q['correct_option'] if section=='A' else q['numerical_variant']['answer_integer'],'answer_text':q['correct_answer'] if section=='A' else str(q['numerical_variant']['answer_integer']),'explanation':q['explanation'],'numerical_scaling':q['numerical_variant'] if section=='B' else None})
 return {'seed':seed,'max_marks':100,'marking':{'correct':4,'incorrect':-1,'unattempted':0},'basis':'Official JEE Main 2026 Paper 1 Physics format','questions':paper},answer
def render(paper,answers=None):
 parts=[]
 for q in paper['questions']:
  figures=''.join(f'<img src="{f["file"]}" alt="{html.escape(f["alt_text"])}">' for f in q['figures'])
  options=''.join(f'<p>{k}. {html.escape(v)}</p>' for k,v in q.get('options',{}).items()) or '<p>Numerical answer: __________________</p>'
  sol=''
  if answers:
   a=answers[q['number']-1];sol=f'<p><b>Answer: {html.escape(str(a["answer"]))}</b></p><p>{html.escape(a["explanation"])}</p>'
  parts.append(f'<article><small>Section {q["section"]} · {q["id"]}</small><h3>Question {q["number"]}</h3><p>{html.escape(q["question"])}</p><small>{html.escape(q["assumptions"])}</small>{figures}{options}{sol}</article>')
 return '<!doctype html><meta charset="utf-8"><title>JEE Main Physics sample paper</title><style>body{max-width:950px;margin:35px auto;font:17px/1.6 Arial;color:#183447}article{border-top:1px solid #ccd9df;margin:24px 0;padding:20px;break-inside:avoid}img{display:block;max-width:750px;width:100%}small{color:#4d6572}</style><h1>Paper Tree · JEE Main Physics</h1><p>Physics section: 20 MCQs + 5 numerical answers · Maximum 100 marks<br>+4 for correct, −1 for incorrect, 0 for unattempted. Attempt all 25 questions.<br>Numerical responses: nearest integer in the requested scaled units.<br>2026 official format; verify the 2027 bulletin when released.</p>'+''.join(parts)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=27);ap.add_argument('--bank',type=Path,default=ROOT/'jee_main_physics_v1.4.0.json');ap.add_argument('--output',type=Path,default=ROOT);args=ap.parse_args()
 bank=json.loads(args.bank.read_text(encoding='utf8'));paper,key=generate(bank,args.seed);args.output.mkdir(exist_ok=True,parents=True)
 for name,val in [('sample_paper.json',paper),('sample_answer_key.json',key)]: (args.output/name).write_text(json.dumps(val,ensure_ascii=False,indent=2),encoding='utf8')
 (args.output/'Sample_Paper.html').write_text(render(paper),encoding='utf8');(args.output/'Sample_Solutions.html').write_text(render(paper,key),encoding='utf8')
 print('Generated 20 MCQs + 5 numerical answers; seed',args.seed)
