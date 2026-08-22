"""Standalone structural, schema, asset and generator validation for v2.1.0."""

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
BANK_PATH = ROOT / "MHT-CET_Biology_question_bank_v2.1.0.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def option_signature(q):
    return tuple(sorted(" ".join(v.lower().split()) for v in q["options"].values()))


def main():
    errors = []
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if len(bank) != 2120:
        errors.append("Question count must be 2120")
    if len({q["id"] for q in bank}) != len(bank):
        errors.append("Question IDs are not unique")
    if len({" ".join(q["stem"].lower().split()) for q in bank}) != len(bank):
        errors.append("Question stems are not unique")
    if Counter(q["correct_option"] for q in bank) != Counter({"A":530,"B":530,"C":530,"D":530}):
        errors.append("Answer-key balance failed")
    if Counter(q["difficulty"] for q in bank) != Counter({"Easy":534,"Medium":853,"Hard":524,"Challenging":209}):
        errors.append("Difficulty totals failed")
    for q in bank:
        if set(q["options"]) != set("ABCD") or len(set(q["options"].values())) != 4:
            errors.append(f"{q['id']}: invalid options")
        if q["options"].get(q["correct_option"]) != q["correct_answer_text"]:
            errors.append(f"{q['id']}: answer mismatch")
        if set(q["distractor_rationale"]) != set("ABCD") - {q["correct_option"]}:
            errors.append(f"{q['id']}: rationale keys mismatch")
        if not q.get("source_locator"):
            errors.append(f"{q['id']}: source locator missing")
        if "human_review_status" in q:
            errors.append(f"{q['id']}: removed approval-status field is still present")
        if q["figure_asset"] and not (ROOT / q["figure_asset"]).is_file():
            errors.append(f"{q['id']}: missing figure")

    record_schema = json.loads((ROOT / "MHT-CET_Biology_question_record_v2.1.0.schema.json").read_text(encoding="utf-8"))
    required = set(record_schema["required"])
    allowed = set(record_schema["properties"])
    for q in bank:
        if set(q) != required or set(q) - allowed:
            errors.append(f"{q.get('id','unknown')}: schema field set mismatch")
        if q.get("difficulty") not in {"Easy","Medium","Hard","Challenging"}:
            errors.append(f"{q.get('id','unknown')}: schema difficulty enum failed")
        if q.get("standard") not in {11,12} or q.get("correct_option") not in set("ABCD"):
            errors.append(f"{q.get('id','unknown')}: schema enum failed")

    manifest = json.loads((ROOT / "figures" / "asset_manifest_v2.1.0.json").read_text(encoding="utf-8"))
    if len(manifest) != 44:
        errors.append("Figure manifest must contain 44 assets")
    for entry in manifest:
        path = ROOT / entry["asset"]
        if not path.is_file() or sha256(path) != entry["sha256"]:
            errors.append(f"{entry['asset']}: missing or hash mismatch")
            continue
        with Image.open(path) as image:
            if image.size != (1800, 1100) or image.format != "PNG":
                errors.append(f"{entry['asset']}: invalid image format/dimensions")

    generator_failures = []
    duplicate_option_papers = 0
    for seed in range(1000, 1100):
        result = subprocess.run([sys.executable, str(ROOT / "assemble_test.py"), "--seed", str(seed), "--output", f"examples/_validation_{seed}.json"], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            generator_failures.append(seed)
            continue
        paper = json.loads((ROOT / f"examples/_validation_{seed}.json").read_text(encoding="utf-8"))
        qs = paper["questions"]
        if len({option_signature(q) for q in qs}) != 100:
            duplicate_option_papers += 1
        if Counter(q["correct_option"] for q in qs) != Counter({"A":25,"B":25,"C":25,"D":25}):
            generator_failures.append(seed)
        if Counter(q["difficulty"] for q in qs) != Counter({"Easy":25,"Medium":40,"Hard":25,"Challenging":10}):
            generator_failures.append(seed)
        (ROOT / f"examples/_validation_{seed}.json").unlink(missing_ok=True)
    if generator_failures:
        errors.append(f"Generator failures on seeds: {generator_failures[:10]}")
    if duplicate_option_papers:
        errors.append(f"Duplicate option sets in {duplicate_option_papers}/100 generated papers")

    report = {
        "status": "PASS" if not errors else "FAIL", "questions": len(bank), "assets": len(manifest),
        "figure_linked_questions": sum(bool(q["figure_asset"]) for q in bank),
        "difficulty": dict(Counter(q["difficulty"] for q in bank)),
        "answer_key": dict(Counter(q["correct_option"] for q in bank)),
        "generator_seeds_tested": 100, "generator_failures": len(generator_failures),
        "papers_with_duplicate_option_sets": duplicate_option_papers, "errors": errors,
    }
    (ROOT / "reports" / "FUNCTIONAL_VALIDATION_REPORT_v2.1.0.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
