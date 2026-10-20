"""v1.0.1 errata: merge alias requests into unit configs and repair numerical selections.

Keeps every existing alias group and every still-valid numerical selection, so unchanged
items keep their v1.0.0 behaviour. Writes errata/config_changes.json as evidence.
"""
import glob, json, sys
from collections import Counter
sys.path.insert(0, '.')
from harness import load

cfgs = {f: json.load(open(f)) for f in sorted(glob.glob('config/U[0-9][0-9].json'))}
items, unit_of = {}, {}
for f, c in cfgs.items():
    for d in c['draft_files']:
        for x in load(d):
            items[x['local_id']] = x
            unit_of[x['local_id']] = f

changes = dict(alias_groups_added=[], numerical_dropped=[], numerical_added=[])

# 1. alias requests
seen = set()
for cf in sorted(glob.glob('errata/fix/*_closure.json')):
    batch = cf.split('/')[-1].replace('_closure.json', '')
    for k, grp in enumerate(json.load(open(cf)).get('alias_requests', [])):
        grp = sorted(set(grp))
        assert len(grp) >= 2, (cf, grp)
        for m in grp:
            assert m in items, (cf, m)
        key = tuple(grp)
        if key in seen:
            continue
        seen.add(key)
        name = f"ALIAS-ERR-{batch}-{k + 1:02d}"
        for f in sorted({unit_of[m] for m in grp}):
            cfgs[f]['alias_groups'][name] = list(grp)
        changes['alias_groups_added'].append(dict(name=name, members=list(grp), requested_by=batch))

# 2. numerical selections
for f, c in cfgs.items():
    ids = [x['local_id'] for d in c['draft_files'] for x in load(d)]
    keep, fams = [], set()
    for i in c['numerical_selection']:
        x = items[i]
        ok = x['numerical'] is not None and 0 <= x['numerical']['answer'] <= 99999 and x['concept_family'] not in fams
        if ok:
            keep.append(i); fams.add(x['concept_family'])
        else:
            changes['numerical_dropped'].append(dict(local_id=i, difficulty=x['difficulty'],
                reason='no numerical alternate' if x['numerical'] is None else
                       ('negative or out-of-range answer' if not 0 <= x['numerical']['answer'] <= 99999 else 'family clash after rewrite')))
    dropped = [d for d in changes['numerical_dropped'] if d['local_id'] in c['numerical_selection']]
    for d in dropped:  # replace like for like by difficulty
        for i in ids:
            x = items[i]
            if i in keep or x['numerical'] is None or not 0 <= x['numerical']['answer'] <= 99999:
                continue
            if x['difficulty'] != d['difficulty'] or x['concept_family'] in fams:
                continue
            keep.append(i); fams.add(x['concept_family'])
            changes['numerical_added'].append(dict(local_id=i, difficulty=x['difficulty'], replaces=d['local_id']))
            break
        else:
            raise SystemExit(f"no replacement for {d['local_id']} in {f}")
    assert len(keep) == len(c['numerical_selection']), f
    c['numerical_selection'] = keep
    json.dump(c, open(f, 'w'), indent=1)

json.dump(changes, open('errata/config_changes.json', 'w'), indent=1)
print('alias groups added', len(changes['alias_groups_added']),
      'numerical dropped', len(changes['numerical_dropped']), 'added', len(changes['numerical_added']))
for f, c in cfgs.items():
    print(f, 'aliases', len(c['alias_groups']), 'numerical', len(c['numerical_selection']))
