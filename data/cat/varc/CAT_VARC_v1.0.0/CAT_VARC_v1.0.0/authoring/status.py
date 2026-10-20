import json,os,subprocess,sys
p=json.load(open('plan.json'))
done,bad,missing=[],[],[]
for x in p:
    if not os.path.exists(x['file']): missing.append(x['tag']); continue
    r=subprocess.run(x['cmd'].split('&& ')[1].split(),capture_output=True,text=True,cwd='.')
    (done if r.returncode==0 else bad).append(x['tag'])
print('done',len(done));print('bad',bad);print('missing',missing)
