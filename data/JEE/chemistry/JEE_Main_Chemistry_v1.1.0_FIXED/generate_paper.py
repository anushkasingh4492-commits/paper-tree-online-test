"""Generate a JEE Main Chemistry practice section from the packaged bank."""
import argparse,collections,html,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def generate(bank,seed=1):
 rng=random.Random(seed)
 pools={d:[q for q in bank if q['difficulty']==d] for d in ['Easy','Medium','Difficult']}
 numeric={d:[q for q in pools[d] if q.get('numerical_variant')] for d in pools}
 for attempt in range(3000):
  selected=[];dependencies=set();unit=collections.Counter();cl=collections.Counter();keys=collections.Counter();limits={'XI':12+seed%2,'XII':13-seed%2}
  slots=[('B','Easy')]+[('B','Medium')]*2+[('B','Difficult')]*2
  tail=[('A','Easy')]*7+[('A','Medium')]*9+[('A','Difficult')]*4;rng.shuffle(tail);slots+=tail
  for section,d in slots:
   possible=[q for q in (numeric[d] if section=='B' else pools[d]) if not dependencies.intersection(q['family_dependencies']) and unit[q['unit_number']]<3 and cl[q['source_class']]<limits[q['source_class']] and (section=='B' or keys[q['correct_option']]<5)]
   if not possible:break
   q=rng.choice(possible);selected.append((section,q));dependencies.update(q['family_dependencies']);unit[q['unit_number']]+=1;cl[q['source_class']]+=1
   if section=='A':keys[q['correct_option']]+=1
  if len(selected)==25 and set(keys.values())=={5}:break
 else:raise RuntimeError('Could not satisfy all paper constraints for this seed.')
 a=[q for s,q in selected if s=='A'];b=[q for s,q in selected if s=='B'];rng.shuffle(a);rng.shuffle(b)
 paper=[];answers=[]
 for i,q in enumerate(a+b,1):
  s='A' if i<=20 else 'B';v=q['numerical_variant']
  p={k:q[k] for k in ['id','difficulty','unit_number','source_class','figures','figure_required','family_dependencies','concept_family','assumptions']};p.update(number=i,section=s,question=q['question'] if s=='A' else v['question'])
  if s=='A':p['options']=q['options']
  paper.append(p);answers.append({'number':i,'id':q['id'],'section':s,'answer':q['correct_option'] if s=='A' else v['answer_integer'],'answer_text':q['correct_answer'] if s=='A' else str(v['answer_integer']),'explanation':q['explanation'],'numerical_scaling':v if s=='B' else None})
 return {'seed':seed,'max_marks':100,'marking':{'correct':4,'incorrect':-1,'unattempted':0},'basis':'JEE Main 2026 Paper 1 Chemistry format','questions':paper},answers
def render(paper,answers=None):
 a={x['id']:x for x in answers or []};blocks=[]
 for q in paper['questions']:
  t=f'<article><h2>{q["number"]}. Section {q["section"]}</h2><p>{html.escape(q["question"]).replace(chr(10),"<br>")}</p>'
  for fig in q['figures']:t+=f'<img src="{fig["file"]}" alt="{html.escape(fig["alt_text"])}">'
  for k,v in q.get('options',{}).items():t+=f'<p><b>{k}.</b> {html.escape(v)}</p>'
  if q['id'] in a:
   ans=a[q['id']];t+=f'<aside><b>Answer: {html.escape(str(ans["answer"]))}</b><p>{html.escape(ans["explanation"]).replace(chr(10),"<br>")}</p></aside>'
   if ans.get('numerical_scaling'):
    v=ans['numerical_scaling'];t+=f'<p>Numerical entry: apply the stated factor 10<sup>{v["unit_scale_power10"]}</sup>, giving {v["unrounded_value"]:.7g}; round to {v["answer_integer"]}.</p>'
  blocks.append(t+'</article>')
 return '<!doctype html><html><head><meta charset="utf-8"><title>JEE Main Chemistry practice section</title><style>body{font:17px Arial;max-width:950px;margin:40px auto;color:#163044;line-height:1.55}article{border-top:1px solid #c8d6df;padding:20px 0;break-inside:avoid}img{max-width:100%;width:750px}aside{background:#edf7f6;padding:18px}h1,h2{line-height:1.2}@media print{body{font-size:11pt;margin:10mm}}</style></head><body><h1>JEE Main Chemistry</h1><p>25 questions · 100 marks · +4 correct / −1 incorrect / 0 unattempted</p><p>Section A: select one option. Section B: enter the nearest integer; half-integers round away from zero. Use the units and scaling stated in each question.</p>'+''.join(blocks)+'</body></html>'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=1);ap.add_argument('--output',default='practice');args=ap.parse_args()
 bank=json.loads((ROOT/'jee_main_chemistry_v1.1.0.json').read_text(encoding='utf-8'));p,a=generate(bank,args.seed)
 for suffix,value in [('_questions.json',p),('_answers.json',a)]: (ROOT/(args.output+suffix)).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/(args.output+'_student.html')).write_text(render(p),encoding='utf-8');(ROOT/(args.output+'_teacher.html')).write_text(render(p,a),encoding='utf-8')
 print('Practice section and solutions written beside the bank.')
