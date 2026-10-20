"""Bank-wide near-duplicate scan: stem token similarity plus shared-key heuristics.
usage: python3 dup_scan.py [focus_ids.json]  -> errata/dup_scan.json"""
import json, re, sys, itertools
from collections import defaultdict
recs = [r for u in range(1, 15) for r in json.load(open(f'build/U{u:02d}/records.json'))]
focus = set(json.load(open(sys.argv[1]))) if len(sys.argv) > 1 else None
def toks(s):
    s = re.sub(r'\\(left|right|,|;|!)', ' ', s)
    return set(re.findall(r'[A-Za-z]+|\d+|\\[a-zA-Z]+|[^\s\w]', s))
def nums(s): return tuple(sorted(re.findall(r'\d+', s)))
T = {r['id']: toks(r['question']) for r in recs}
deps = {r['id']: set(r['family_dependencies']) for r in recs}
out = []
for a, b in itertools.combinations(recs, 2):
    if focus and a['id'] not in focus and b['id'] not in focus: continue
    ta, tb = T[a['id']], T[b['id']]
    j = len(ta & tb) / max(1, len(ta | tb))
    same_key = a['correct_answer'].replace(' ', '') == b['correct_answer'].replace(' ', '')
    same_nums = nums(a['question']) == nums(b['question']) and len(nums(a['question'])) >= 3
    if j >= 0.8 or (j >= 0.6 and (same_key or same_nums)):
        out.append(dict(a=a['id'], b=b['id'], la=a['provenance']['local_id'], lb=b['provenance']['local_id'],
                        jaccard=round(j, 3), same_key=same_key, same_numbers=same_nums,
                        linked=bool(deps[a['id']] & deps[b['id']]),
                        qa=a['question'][:200], qb=b['question'][:200], ka=a['correct_answer'], kb=b['correct_answer']))
json.dump(out, open('errata/dup_scan.json', 'w'), indent=1, ensure_ascii=False)
print('pairs flagged', len(out), 'unlinked', sum(not x['linked'] for x in out))
