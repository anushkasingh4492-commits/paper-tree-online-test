# -*- coding: utf-8 -*-
"""Subject claims shared by all drafting batches (prevents parallel batches choosing the same subject).

usage: python3 claim.py <TAG> "<short subject>" ["<short subject>" ...]
       python3 claim.py --list [GROUP]
       python3 claim.py --release <TAG> "<short subject>"     (give back a subject you dropped)

Subjects are compared only within the same group: RC (all reading passages), PJ, PS, OOO, SP.
A subject is refused (CLASH) if it is too similar to one already claimed in its group.
"""
import fcntl, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "claims.json")
STOP = set("a an the of and or in on to for with by as at from its their his her is are be vs versus how why what when who which that this into about between".split())
GROUP = {"R": "RC", "V01": "PJ", "V02": "PS", "V03": "OOO", "V04": "SP"}


def group(tag):
    return "RC" if tag.startswith("R") or tag.startswith("S-RC") else GROUP.get(tag[:3], tag[:3])


def norm(w):
    w = w.lower()
    for suf in ("ies", "es", "s", "ing", "ed", "al", "ity"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def toks(s):
    return set(norm(w) for w in re.findall(r"[A-Za-z]+", s) if w.lower() not in STOP and len(w) > 2)


def similar(a, b):
    A, B = toks(a), toks(b)
    if not A or not B:
        return False
    j = len(A & B) / len(A | B)
    return j >= 0.5 or (len(A & B) >= 2 and (A <= B or B <= A))


def main():
    with open(DB + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        db = json.load(open(DB)) if os.path.exists(DB) else []
        if sys.argv[1] == "--list":
            g = sys.argv[2] if len(sys.argv) > 2 else None
            for c in db:
                if g is None or c["group"] == g:
                    print(c["group"], c["tag"], "|", c["subject"])
            return
        if sys.argv[1] == "--release":
            tag, subj = sys.argv[2], sys.argv[3]
            db = [c for c in db if not (c["tag"] == tag and c["subject"] == subj)]
            json.dump(db, open(DB, "w"), indent=0)
            print("RELEASED", subj)
            return
        tag = sys.argv[1]; g = group(tag)
        for subj in sys.argv[2:]:
            hits = [c for c in db if c["group"] == g and similar(subj, c["subject"]) and not (c["tag"] == tag and c["subject"] == subj)]
            if hits:
                print("CLASH", repr(subj), "with", "; ".join(f"{h['tag']}: {h['subject']}" for h in hits[:4]))
            elif any(c["tag"] == tag and c["subject"] == subj for c in db):
                print("OK (already yours)", repr(subj))
            else:
                db.append(dict(group=g, tag=tag, subject=subj))
                print("OK", repr(subj))
        json.dump(db, open(DB, "w"), indent=0)


if __name__ == "__main__":
    main()
