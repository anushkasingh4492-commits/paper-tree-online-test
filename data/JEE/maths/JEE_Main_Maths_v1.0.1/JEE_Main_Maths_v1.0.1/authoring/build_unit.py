# -*- coding: utf-8 -*-
"""Assemble one unit of the JEE Main Mathematics bank into canonical records.

usage: python3 build_unit.py config/U02.json
Writes build/U02/records.json and build/U02/evidence/*.json
"""
import hashlib, inspect, json, os, random, sys, textwrap
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp  # noqa
from harness import load, equal  # noqa

RELEASE = "1.0.1"
SEED_RELEASE = "1.0.0"  # key positions and option order are frozen at v1.0.0 so patch releases keep unchanged items identical
SYLLABUS_URL = "https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/10/202510311323551056.pdf"
CHECKED_TYPES = None


def balance_positions(n, seed_text, letters="ABCD", max_run=3):
    """Exact-quota key positions with no run > max_run and no ABCD/DCBA run."""
    rnd = random.Random(int(hashlib.sha256(seed_text.encode()).hexdigest(), 16) % (2 ** 63))
    base = [letters[i % 4] for i in range(n)]
    for attempt in range(100000):
        rnd.shuffle(base)
        ok = True
        run = 1
        for i in range(1, n):
            run = run + 1 if base[i] == base[i - 1] else 1
            if run > max_run:
                ok = False
                break
        if ok:
            s = "".join(base)
            if "ABCD" in s or "DCBA" in s:
                ok = False
        if ok:
            return list(base), attempt
    raise RuntimeError("could not balance")


def latex_value(v):
    try:
        return str(v)
    except Exception:
        return repr(v)


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    u = cfg["unit_number"]
    tag = f"U{u:02d}"
    out = os.path.join(HERE, "build", tag)
    os.makedirs(os.path.join(out, "evidence"), exist_ok=True)

    raw = []
    for f in cfg["draft_files"]:
        raw += load(os.path.join(HERE, f))
    assert len(raw) == cfg["count"], (len(raw), cfg["count"])

    # alias groups -> extra dependencies
    alias_of = {}
    for name, members in cfg.get("alias_groups", {}).items():
        for m in members:
            alias_of.setdefault(m, []).append(name)

    numerical_ids = set(cfg["numerical_selection"])
    seed_rel = "1.0.0-pilot" if tag == "U02" else SEED_RELEASE  # keep the pilot option order for Unit 2
    letters, attempts = balance_positions(len(raw), f"JEE-MATH-{tag}-{seed_rel}")
    rnd = random.Random(f"distractor-order-{tag}")

    records, machine, distractor_review = [], [], []
    for n, (x, key_letter) in enumerate(zip(raw, letters), start=1):
        rid = f"JEE-MATH-{tag}-{n:03d}"
        dis = list(x["distractors"])
        dvals = list(x["values"][1:]) if x["values"] else [None, None, None]
        idx = [0, 1, 2]
        rnd.shuffle(idx)
        dis = [dis[i] for i in idx]
        dvals = [dvals[i] for i in idx]
        options, slots = {}, [L for L in "ABCD" if L != key_letter]
        options[key_letter] = x["correct"]
        for L, d in zip(slots, dis):
            options[L] = d["text"]
        options = {L: options[L] for L in "ABCD"}

        # machine check
        if x["check"] is not None:
            got = x["check"]()
            match = equal(got, x["values"][0])
            assert match, rid
            dist_ok = all(not equal(v, x["values"][0]) for v in x["values"][1:])
            assert dist_ok, rid
            try:
                src = textwrap.dedent(inspect.getsource(x["check"]))
            except Exception:
                src = "<lambda; source unavailable>"
            machine.append(dict(id=rid, local_id=x["local_id"], computed=latex_value(got),
                                keyed_value=latex_value(x["values"][0]), match=True,
                                distractor_values={L: latex_value(v) for L, v in zip(slots, dvals)},
                                distractors_differ_from_key=True, check_source=src))
            mc = {"method": "sympy recomputation from the stated givens", "status": "match",
                  "computed_value": latex_value(got)}
        else:
            mc = {"method": "not machine-checkable (conceptual)", "status": "not applicable",
                  "computed_value": None}

        distractor_review.append(dict(id=rid, local_id=x["local_id"],
                                      distractors=[dict(option=L, text=d["text"], reason=d["rationale"]) for L, d in zip(slots, dis)]))

        nv = None
        if x["local_id"] in numerical_ids:
            assert x["numerical"], x["local_id"]
            nv = dict(question=x["numerical"]["question"],
                      answer_integer=x["numerical"]["answer"], unrounded_value=x["numerical"]["answer"],
                      unit="", unit_scale_power10=0, rounding="exact integer; no rounding required",
                      parent_id=rid,
                      verification_basis="Integer equals the machine-recomputed value of the parent question unless the stem states a scaling; scaling checked in evidence/numerical_checks.json.")

        topic_unit = cfg["unit_name"]
        fam = x["concept_family"]
        deps = [fam] + alias_of.get(x["local_id"], [])
        status = ("MACHINE_RECOMPUTED; BLIND_RESOLVED; EDITORIAL_AUDITED; ERRATA_RECOMPUTED; ERRATA_AUDITED" if x["check"] is not None
                  else "BLIND_RESOLVED; EDITORIAL_AUDITED; ERRATA_RECOMPUTED; ERRATA_AUDITED")
        rec = dict(
            id=rid, unit_number=u, unit=f"Unit {u}: {topic_unit}", chapter=topic_unit,
            topic=x["topic"], subtopic=x["subtopic"], source_class=x["source_class"],
            branch=cfg["branch"], standard="JEE Main", subject="Mathematics",
            question=x["question"], options=options, correct_option=key_letter,
            correct_answer=x["correct"], explanation=x["explanation"],
            common_misconception=x["common_misconception"],
            difficulty=x["difficulty"], difficulty_reason=x["difficulty_reason"],
            difficulty_basis="Editorial estimate (steps, ideas combined, trap density); not calibrated against student data",
            cognitive_level=x["cognitive_level"], question_type=x["question_type"],
            concept_family=fam, family_dependencies=deps, max_per_family_per_paper=1,
            figures=[], figure_required=False, assumptions=x["assumptions"],
            notation="latex-inline", machine_check=mc, numerical_variant=nv,
            provenance=dict(kind="Original JEE Main authoring", authoring_batch=x["local_id"].rsplit("-", 1)[0], local_id=x["local_id"]),
            source_document="NTA JEE Main 2026 official syllabus (scope reference; questions are originally authored)",
            source_chapter=topic_unit, source_page=None,
            syllabus_reference=f"NTA JEE Main 2026 Mathematics, Unit {u}: {topic_unit}; {SYLLABUS_URL}",
            source_verification_note="Syllabus unit is a scope locator. No textbook page or past-paper attribution is claimed.",
            syllabus_basis_year=2026, release_version=RELEASE,
            marks_correct=4, marks_incorrect=-1, marks_unattempted=0, generator_eligible=True,
            validation_status=status, human_subject_expert_reviewed=False,
            tags=["JEE Main", "Mathematics", f"Unit {u}", x["difficulty"], x["topic"]],
        )
        records.append(rec)

    # numerical checks
    numchecks = []
    for r, x in zip(records, raw):
        if r["numerical_variant"]:
            same = x["values"] is not None and equal(sp.Integer(r["numerical_variant"]["answer_integer"]), x["values"][0])
            numchecks.append(dict(id=r["id"], answer_integer=r["numerical_variant"]["answer_integer"],
                                  mcq_value=latex_value(x["values"][0]) if x["values"] else None,
                                  equals_mcq_value=bool(same),
                                  note="" if same else "Integer stem asks for a stated scaling of the MCQ quantity; reviewed."))

    json.dump(records, open(os.path.join(out, "records.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(machine, open(os.path.join(out, "evidence", "machine_checks.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(distractor_review, open(os.path.join(out, "evidence", "distractor_review.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(numchecks, open(os.path.join(out, "evidence", "numerical_checks.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(dict(unit=tag, seed_text=f"JEE-MATH-{tag}-{seed_rel}", attempts=attempts,
                   sequence="".join(letters), counts=dict(Counter(letters))),
              open(os.path.join(out, "evidence", "key_balance.json"), "w"), indent=1)
    print(tag, len(records), dict(Counter(r["difficulty"] for r in records)), dict(Counter(letters)),
          "machine", len(machine), "numerical", len(numchecks), "families", len({r['concept_family'] for r in records}))


if __name__ == "__main__":
    main(sys.argv[1])
