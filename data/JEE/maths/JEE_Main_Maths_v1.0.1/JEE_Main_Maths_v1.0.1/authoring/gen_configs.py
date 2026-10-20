import json, sys
sys.path.insert(0,'.')
from harness import load
from collections import Counter, defaultdict
plan=json.load(open('config/batch_plan.json'))
import sympy as sp
total_target=338
report={}
for u,p in plan.items():
    files=[b['file'] for b in p['batches']]
    qs=[]
    for f in files: qs+=load(f)
    assert len(qs)==p['count'],(u,len(qs))
    cls=Counter(x['source_class'] for x in qs)
    exp=Counter()
    for b in p['batches']:
        for k,v in b['classes'].items(): exp[k]+=v
    target=round(p['count']*total_target/2700)
    # candidates: non-negative integer, at most one per family
    cands=[x for x in qs if x['numerical'] and x['numerical']['answer']>=0 and x['numerical']['answer']<=99999]
    want={'Easy':round(target*0.15),'Medium':round(target*0.35)}
    want['Difficult']=target-want['Easy']-want['Medium']
    chosen=[];fams=set()
    for lvl in ['Difficult','Medium','Easy']:
        pool=[x for x in cands if x['difficulty']==lvl]
        # spread across batches: round robin by batch
        byb=defaultdict(list)
        for x in pool: byb[x['local_id'][:5]].append(x)
        order=[]
        while any(byb.values()):
            for k in sorted(byb):
                if byb[k]: order.append(byb[k].pop(0))
        n=0
        for x in order:
            if n>=want[lvl]: break
            if x['concept_family'] in fams: continue
            chosen.append(x['local_id']); fams.add(x['concept_family']); n+=1
    # top up if short
    for x in cands:
        if len(chosen)>=target: break
        if x['local_id'] not in chosen and x['concept_family'] not in fams:
            chosen.append(x['local_id']); fams.add(x['concept_family'])
    cfg=dict(unit_number=p['unit_number'],unit_name=p['unit_name'],branch=p['branch'],count=p['count'],
             draft_files=files,alias_groups={},numerical_selection=chosen)
    json.dump(cfg,open(f'config/{u}.json','w'),indent=1)
    report[u]=dict(classes=dict(cls),expected=dict(exp),num_target=target,num_chosen=len(chosen),
                   num_by_diff=dict(Counter(next(x['difficulty'] for x in qs if x['local_id']==i) for i in chosen)))
for k,v in report.items(): print(k,v)
