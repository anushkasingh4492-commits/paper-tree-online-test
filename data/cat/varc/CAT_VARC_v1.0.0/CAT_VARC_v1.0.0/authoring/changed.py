import sys,glob,os,json,importlib.util,re
sys.path.insert(0,'.')
import vlib
def loadf(path):
    vlib.SETS.clear(); vlib.QUESTIONS.clear()
    spec=importlib.util.spec_from_file_location("m"+re.sub(r"\W","_",path),path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return list(vlib.SETS),list(vlib.QUESTIONS)
def face(x,sets):
    k=x['kind']
    if k=='RC': return (tuple(sets[x['set_id']]['paragraphs']),x['question'],x['correct'],tuple(sorted(d['text'] for d in x['distractors'])))
    if k=='PS': return (x['paragraph'],x['correct'],tuple(sorted(d['text'] for d in x['distractors'])))
    if k in('PJ','OOO'): return tuple(x['printed'])+(x['tita_answer'],)
    return (x['printed_paragraph'],x['missing'],x['key_number'])
def corpus(d):
    S,Q={},[]
    for f in sorted(glob.glob(d+'/[rv]*.py')):
        s,q=loadf(f); S.update({a['set_id']:a for a in s}); Q+=q
    return S,Q
old_dir,new_dir,out=sys.argv[1],sys.argv[2],sys.argv[3]
S0,Q0=corpus(old_dir);S1,Q1=corpus(new_dir)
o={x['local_id']:face(x,S0) for x in Q0}
ch=[x['local_id'] for x in Q1 if o.get(x['local_id'])!=face(x,S1)]
json.dump(ch,open(out,'w'));print(len(ch),'changed')
import collections;print(collections.Counter(i[:3] for i in ch))
