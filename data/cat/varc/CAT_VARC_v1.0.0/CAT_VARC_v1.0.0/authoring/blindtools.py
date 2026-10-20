# -*- coding: utf-8 -*-
"""Blind packs and scoring for the VARC bank.

make:  python3 blindtools.py make <round> [ids.json|-]     (two independent solver sets S1 and S2)
score: python3 blindtools.py score <round>
Packs go to /home/claude/blind_varc/<round>_<S>_<NN>.json; keys stay in verify/blind/.
"""
import glob, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import load
HERE = os.path.dirname(os.path.abspath(__file__))
BD = "/home/claude/blind_varc"
VD = os.path.join(HERE, "verify", "blind")
RC_PER_PACK = 20     # passages
VA_PER_PACK = 110    # items


def corpus():
    sets, qs = {}, []
    for f in sorted(glob.glob(os.path.join(HERE, "drafts", "[rv]*.py"))):
        S, Q = load(f)
        for s in S:
            sets[s["set_id"]] = s
        qs += Q
    return sets, qs


def present(x, rnd):
    """Student-facing item and its key under this solver's shuffle."""
    k = x["kind"]
    if k in ("RC", "PS"):
        opts = [(x["correct"], 1)] + [(d["text"], 0) for d in x["distractors"]]
        rnd.shuffle(opts)
        it = dict(id=x["local_id"], type="RC" if k == "RC" else "Para summary",
                  options={L: t for L, (t, _) in zip("ABCD", opts)})
        if k == "RC":
            it["question"] = x["question"]
        else:
            it["paragraph"] = x["paragraph"]
            it["question"] = "Choose the option that best captures the essence of the paragraph."
        key = [L for L, (t, c) in zip("ABCD", opts) if c][0]
    elif k == "PJ":
        n = len(x["printed"])
        it = dict(id=x["local_id"], type="Para jumble", sentences={str(i + 1): s for i, s in enumerate(x["printed"])},
                  question=f"The {n} sentences above, properly sequenced, form a coherent paragraph. Type the sequence of {n} numbers.")
        key = x["tita_answer"]
    elif k == "OOO":
        it = dict(id=x["local_id"], type="Odd sentence out", sentences={str(i + 1): s for i, s in enumerate(x["printed"])},
                  question="Four of these five sentences form a coherent paragraph. Type the number of the sentence that does not belong.")
        key = x["tita_answer"]
    else:
        it = dict(id=x["local_id"], type="Sentence placement", paragraph=x["printed_paragraph"], missing_sentence=x["missing"],
                  question="Which gap, (1), (2), (3) or (4), is the best place for the missing sentence? Answer 1, 2, 3 or 4.")
        key = str(x["key_number"])
    return it, key


def make(rnd_name, idfile="-"):
    os.makedirs(BD, exist_ok=True); os.makedirs(VD, exist_ok=True)
    sets, qs = corpus()
    want = None if idfile == "-" else set(json.load(open(idfile)))
    keys = {}
    for S in ("S1", "S2"):
        rnd = random.Random(rnd_name + S)
        rc = [x for x in qs if x["kind"] == "RC" and (want is None or x["local_id"] in want)]
        va = [x for x in qs if x["kind"] != "RC" and (want is None or x["local_id"] in want)]
        sids = sorted(set(x["set_id"] for x in rc)); rnd.shuffle(sids)
        packs = []
        for i in range(0, len(sids), RC_PER_PACK):
            chunk = sids[i:i + RC_PER_PACK]; items = []
            for sid in chunk:
                s = sets[sid]
                block = dict(passage_id=sid, passage=s["paragraphs"], questions=[])
                for x in sorted([y for y in rc if y["set_id"] == sid], key=lambda y: y["local_id"]):
                    it, key = present(x, rnd); keys[(S, x["local_id"])] = key; block["questions"].append(it)
                items.append(block)
            packs.append(dict(kind="RC", passages=items))
        rnd.shuffle(va)
        for i in range(0, len(va), VA_PER_PACK):
            items = []
            for x in va[i:i + VA_PER_PACK]:
                it, key = present(x, rnd); keys[(S, x["local_id"])] = key; items.append(it)
            packs.append(dict(kind="VA", items=items))
        for n, p in enumerate(packs, 1):
            json.dump(p, open(f"{BD}/{rnd_name}_{S}_{n:02d}.json", "w"), indent=1)
        print(rnd_name, S, len(packs), "packs")
    json.dump({f"{s}|{i}": k for (s, i), k in keys.items()}, open(f"{VD}/{rnd_name}_keys.json", "w"), indent=0)


def score(rnd_name):
    keys = json.load(open(f"{VD}/{rnd_name}_keys.json"))
    ans = {}
    for f in sorted(glob.glob(f"{BD}/{rnd_name}_S?_*.answers.json")):
        S = os.path.basename(f).split("_")[1]
        try:
            for a in json.load(open(f)):
                ans[f"{S}|{a['id']}"] = a
        except Exception as e:
            print("BAD FILE", f, e)
    ids = sorted(set(k.split("|", 1)[1] for k in keys))
    out = dict(round=rnd_name, items=len(ids), both_agree=0, disagreements=[], issues=[], missing=[])
    for i in ids:
        row = {}
        ok = True
        for S in ("S1", "S2"):
            a = ans.get(f"{S}|{i}")
            if a is None:
                out["missing"].append(f"{S}|{i}"); ok = False; continue
            got = str(a.get("answer")).strip().replace(" ", "")
            row[S] = dict(answer=got, key=keys[f"{S}|{i}"], working=a.get("working", ""), confidence=a.get("confidence"),
                          issue=a.get("issue", ""), alternative=a.get("alternative", ""))
            if got != keys[f"{S}|{i}"]:
                ok = False
        if ok and len(row) == 2:
            out["both_agree"] += 1
            if any(r["issue"] or r["alternative"] for r in row.values()):
                out["issues"].append(dict(id=i, **row))
        elif len(row) == 2 or any(r["answer"] != r["key"] for r in row.values()):
            out["disagreements"].append(dict(id=i, **row))
    json.dump(out, open(f"{VD}/{rnd_name}_score.json", "w"), indent=1)
    print(rnd_name, "items", out["items"], "both agree", out["both_agree"], "disagreements", len(out["disagreements"]),
          "issues", len(out["issues"]), "missing", len(out["missing"]))


if __name__ == "__main__":
    if sys.argv[1] == "make":
        make(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "-")
    else:
        score(sys.argv[2])
