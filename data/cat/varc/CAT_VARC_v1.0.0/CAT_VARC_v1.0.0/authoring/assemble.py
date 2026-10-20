# -*- coding: utf-8 -*-
"""Assemble the CAT VARC release folder from build/bank.json and verify/.

python3 assemble.py           build release/CAT_VARC_v1.0.0
python3 assemble.py --docs    regenerate README / START_HERE / Build_Report only (after tests)
"""
import csv, glob, html, json, os, shutil, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
VER = "1.0.0"
NAME = f"CAT_VARC_v{VER}"
OUT = os.path.join(HERE, "release", NAME)
BANK = f"cat_varc_v{VER}"
DATE = "18 October 2026"
sys.path.insert(0, HERE)
from build import CHAPTERS  # noqa: E402

E = html.escape


def wj(rel, obj, indent=1):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, "w", encoding="utf-8"), indent=indent, ensure_ascii=False)


def wt(rel, text):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


CSS = """:root{--ink:#1b2a3a;--muted:#5b6f80;--line:#dde5ec;--bg:#f4f6f8;--card:#fff;--brand:#2c4a6e;--key:#e6f4ec;--tita:#fff6e3}
body{font:17px/1.6 Arial,Helvetica,sans-serif;margin:0;background:var(--bg);color:var(--ink)}
header{padding:40px max(20px,calc((100% - 1000px)/2)) 28px;background:var(--brand);color:#fff}h1{font-size:32px;margin:0 0 8px}
header p{max-width:900px;margin:6px 0;opacity:.95}.bar{position:sticky;top:0;z-index:5;background:#fff;padding:12px max(16px,calc((100% - 1000px)/2));display:flex;gap:10px;flex-wrap:wrap;box-shadow:0 2px 10px #0001}
input,select,button{font:inherit;padding:8px 10px;border:1px solid #c9d5df;border-radius:6px;background:#fff}main{max-width:1000px;margin:18px auto;padding:0 16px}
article{background:var(--card);padding:24px 28px;margin:16px 0;border-radius:10px;border:1px solid var(--line)}
.meta{font-size:13px;color:var(--muted)}.badge{display:inline-block;font-size:12px;font-weight:bold;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:1px}
.b-mcq{background:#e8eef6;color:#2c4a6e}.b-tita{background:#fdebc8;color:#7a4d00}.q{margin:10px 0 6px}
.passage{background:#fafbfc;border-left:4px solid var(--brand);padding:6px 18px;margin:10px 0 16px}.passage p{margin:10px 0}
.qq{border-top:1px solid var(--line);padding-top:12px;margin-top:14px}
ol{list-style:none;padding:0;margin:8px 0}li{margin:6px 0;padding:4px 8px}li b{display:inline-block;width:30px}li.key{background:var(--key);border-radius:6px}
.sents p{margin:6px 0}.sents b{display:inline-block;width:26px}.miss{background:#eef3f9;padding:8px 12px;border-radius:6px}
.box{display:inline-block;min-width:140px;border:1px dashed #b9c6d2;border-radius:6px;padding:8px 12px;color:var(--muted);margin-top:6px;font-size:14px}
details{background:#eef3f9;padding:12px 16px;border-radius:8px;margin-top:10px}summary{cursor:pointer;font-weight:bold}
.why{font-size:15px;margin:4px 0}.trap{background:var(--tita);padding:8px 12px;border-radius:6px;margin-top:8px;font-size:15px}article[hidden]{display:none}
.count{align-self:center;color:var(--muted);font-size:14px}table{border-collapse:collapse;margin:10px 0}td,th{border:1px solid var(--line);padding:6px 10px;text-align:left}th{background:#eef3f9}
@media print{body{background:#fff;font-size:10.5pt}.bar{display:none}header{padding:6mm 0;color:var(--brand);background:#fff}main{margin:0;padding:0}
article{border:0;border-top:1px solid #ddd;margin:0;padding:4mm 0;border-radius:0;break-inside:auto}details{display:block}details>summary{display:none}}"""

JS = """<script>
const qs=[...document.querySelectorAll('article')];const f=()=>{const g=id=>(document.getElementById(id)||{}).value||'';
const s=g('search'),t=g('topic'),d=g('diff');let n=0;
qs.forEach(a=>{const ok=(!s||a.textContent.toLowerCase().includes(s.toLowerCase()))&&(!t||(a.dataset.topic||'').split('|').includes(t))&&(!d||(a.dataset.diff||'').split('|').includes(d));a.hidden=!ok;if(ok)n++;});
const c=document.getElementById('count');if(c)c.textContent=n+' shown';};
document.querySelectorAll('.bar input,.bar select').forEach(e=>e.addEventListener('input',f));f();
</script>"""


def page(title, head, body, bar=""):
    return (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{E(title)}</title><style>{CSS}</style></head><body><header>{head}</header>{bar}<main>{body}</main>{JS}</body></html>")


def badge(q):
    return f"<span class=\"badge {'b-tita' if q['answer_format'] == 'TITA' else 'b-mcq'}\">{q['answer_format']}</span>"


def q_html(q, teacher, show_id=True):
    out = []
    meta = (f"{q['id']} &middot; " if show_id else "") + f"{E(q['question_type'])} &middot; {q['difficulty']}{badge(q)}"
    out.append(f"<div class=\"meta\">{meta}</div>")
    t = q["question_type"]
    if q["set_id"]:
        out.append(f"<div class=\"q\">{E(q['question'])}</div>")
    elif t in ("Para jumble", "Odd sentence out"):
        out.append(f"<div class=\"q\">{E(q['instructions'])}</div><div class=\"sents\">" +
                   "".join(f"<p><b>{s['label']}.</b>{E(s['text'])}</p>" for s in q["sentences"]) + "</div>")
    elif t == "Para summary":
        out.append(f"<div class=\"q\">{E(q['instructions'])}</div><div class=\"passage\"><p>{E(q['passage_text'])}</p></div>")
    else:
        out.append(f"<div class=\"q\">{E(q['instructions'])}</div><div class=\"miss\"><b>Missing sentence:</b> {E(q['missing_sentence'])}</div>"
                   f"<div class=\"passage\"><p>{E(q['passage_text'])}</p></div>")
    if q["options"]:
        out.append("<ol>" + "".join(f"<li class=\"{'key' if teacher and L == q['correct_option'] else ''}\"><b>({L})</b>{E(v)}</li>"
                                    for L, v in q["options"].items()) + "</ol>")
    else:
        out.append("<div class=\"box\">Type your answer</div>")
    if teacher:
        ans = f"({q['correct_option']})" if q["options"] else q["tita_answer"]
        d = [f"<details open><summary>Answer and explanation</summary><p><b>Answer: {E(ans)}</b></p><p>{E(q['explanation'])}</p>"]
        if q["option_rationales"]:
            d.append("".join(f"<p class=\"why\"><b>Why not ({L}):</b> {E(v)}</p>" for L, v in sorted(q["option_rationales"].items())))
        for w in q["tita_common_wrong_entries"]:
            d.append(f"<div class=\"trap\"><b>Common wrong entry {E(w['value'])}:</b> {E(w['reason'])}</div>")
        d.append(f"<p class=\"why\"><b>Common misconception:</b> {E(q['common_misconception'])}</p>"
                 f"<p class=\"meta\">Difficulty: {E(q['difficulty_reason'])} &middot; Exams: {', '.join(q['exam_tags'])}</p></details>")
        out.append("".join(d))
    return "".join(out)


def books(bank):
    qs = {q["id"]: q for q in bank["questions"]}
    for code, num, area, name in CHAPTERS:
        for teacher in (False, True):
            arts, topics = [], set()
            if area == "Reading Comprehension":
                for s in [s for s in bank["sets"] if s["chapter_number"] == num]:
                    qq = [qs[i] for i in s["question_ids"]]
                    types = sorted({q["question_type"] for q in qq}); topics |= set(types)
                    diffs = sorted({q["difficulty"] for q in qq} | {s["difficulty"]})
                    body = "".join(f"<p>{E(p)}</p>" for p in s["paragraphs"])
                    arts.append(f"<article data-topic=\"{E('|'.join(types))}\" data-diff=\"{'|'.join(diffs)}\"><div class=\"meta\">{s['set_id']} &middot; "
                                f"{E(s['topic'])} &middot; passage {s['difficulty']} &middot; {s['word_count']} words &middot; {len(qq)} questions</div>"
                                f"<div class=\"passage\">{body}</div>" + "".join(f"<div class=\"qq\">{q_html(q, teacher)}</div>" for q in qq) + "</article>")
            else:
                for q in [q for q in bank["questions"] if q["chapter_number"] == num]:
                    topics.add(q["topic"])
                    arts.append(f"<article data-topic=\"{E(q['topic'])}\" data-diff=\"{q['difficulty']}\">{q_html(q, teacher)}</article>")
            kind = "Teacher" if teacher else "Student"
            sel = "".join(f"<option>{E(t)}</option>" for t in sorted(topics))
            bar = (f"<div class=\"bar\"><input id=\"search\" placeholder=\"Search text or ID\"><select id=\"topic\"><option value=\"\">All "
                   f"{'question types' if area == 'Reading Comprehension' else 'subject areas'}</option>{sel}</select><select id=\"diff\"><option value=\"\">All levels</option>"
                   f"<option>Easy</option><option>Medium</option><option>Difficult</option></select><button onclick=\"print()\">Print</button><span class=\"count\" id=\"count\"></span></div>")
            n = sum(1 for q in bank["questions"] if q["chapter_number"] == num)
            head = (f"<h1>CAT VARC Chapter {num:02d}: {E(name)}</h1><p>{area} &middot; {n} questions"
                    + (f" in {len(arts)} passages" if area == "Reading Comprehension" else "") +
                    f" &middot; {kind} book</p><p>Paper Tree Educational Studio &middot; v{VER}</p>")
            wt(f"books/Chapter_{num:02d}_{kind}.html", page(f"CAT VARC Chapter {num:02d}, {name}: {kind} book", head, "".join(arts), bar))


def sample(bank):
    subprocess.run([sys.executable, os.path.join(OUT, "generate_paper.py"), "--bank", os.path.join(OUT, BANK + ".json"),
                    "--seed", "42", "--output", os.path.join(OUT, "sample")], check=True, capture_output=True)
    os.replace(os.path.join(OUT, "sample_paper.json"), os.path.join(OUT, "sample_paper.json"))
    paper = json.load(open(os.path.join(OUT, "sample_paper.json")))
    qs = {q["id"]: q for q in bank["questions"]}; sets = {s["set_id"]: s for s in bank["sets"]}
    for teacher in (False, True):
        parts, n = [], 0
        done_sets = set()
        for i in paper["questions"]:
            q = qs[i]
            if q["set_id"] and q["set_id"] not in done_sets:
                s = sets[q["set_id"]]; done_sets.add(s["set_id"])
                block = [f"<article><div class=\"meta\">Passage {len(done_sets)} &middot; questions {n + 1} to {n + len(s['question_ids'])}</div>"
                         f"<div class=\"passage\">{''.join(f'<p>{E(p)}</p>' for p in s['paragraphs'])}</div>"]
                for j in s["question_ids"]:
                    n += 1
                    block.append(f"<div class=\"qq\"><p><b>Question {n}</b></p>{q_html(qs[j], teacher, show_id=teacher)}</div>")
                parts.append("".join(block) + "</article>")
            elif not q["set_id"]:
                n += 1
                parts.append(f"<article><p><b>Question {n}</b></p>{q_html(q, teacher, show_id=teacher)}</article>")
        head = (f"<h1>CAT VARC sample section{': solutions' if teacher else ''}</h1><p>{paper['description']} Time: {paper['time_minutes']} minutes. "
                f"Maximum marks: {paper['max_marks']}. MCQ +3 / -1, TITA +3 / 0.</p><p>Generated with seed 42 &middot; Paper Tree Educational Studio</p>")
        wt("Sample_Solutions.html" if teacher else "Sample_Paper.html", page("CAT VARC sample section" + (" solutions" if teacher else ""), head, "".join(parts)))


def exports(bank):
    meta = dict(name="CAT VARC question bank", version=VER, date=DATE, publisher="Paper Tree Educational Studio",
                schema="question_bank_schema.json", sets=len(bank["sets"]), questions=len(bank["questions"]))
    full = dict(meta=meta, sets=bank["sets"], questions=bank["questions"])
    wj(BANK + ".json", full)
    with open(os.path.join(OUT, BANK + "_questions.jsonl"), "w", encoding="utf-8") as f:
        for q in bank["questions"]:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, BANK + "_passages.jsonl"), "w", encoding="utf-8") as f:
        for s in bank["sets"]:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    for name, rows in ((BANK + "_questions.csv", bank["questions"]), (BANK + "_passages.csv", bank["sets"])):
        keys = list(rows[0].keys())
        for r in rows:
            for k in r:
                if k not in keys:
                    keys.append(k)
        with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(keys)
            for r in rows:
                w.writerow([json.dumps(r.get(k), ensure_ascii=False) if isinstance(r.get(k), (list, dict)) else ("" if r.get(k) is None else r.get(k)) for k in keys])
    student_keys = ["id", "section", "area", "chapter_number", "chapter", "topic", "question_type", "set_id", "answer_format",
                    "instructions", "question", "sentences", "passage_text", "missing_sentence", "options", "difficulty", "exam_tags"]
    wj("questions_only.json", dict(meta=meta, passages=[{k: s[k] for k in ("set_id", "chapter_number", "chapter", "topic", "paragraphs", "word_count", "question_ids")} for s in bank["sets"]],
                                   questions=[{k: q.get(k) for k in student_keys if k in q} for q in bank["questions"]]))
    wj("answers_and_explanations.json", [dict(id=q["id"], answer_format=q["answer_format"], correct_option=q["correct_option"], tita_answer=q["tita_answer"],
                                              correct_answer=q["correct_answer"], explanation=q["explanation"], option_rationales=q["option_rationales"],
                                              tita_common_wrong_entries=q["tita_common_wrong_entries"], common_misconception=q["common_misconception"])
                                         for q in bank["questions"]])
    with open(os.path.join(OUT, "question_index.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "chapter_number", "chapter", "set_id", "question_type", "topic", "difficulty", "answer_format", "answer", "exam_tags", "local_id"])
        for q in bank["questions"]:
            w.writerow([q["id"], q["chapter_number"], q["chapter"], q["set_id"] or "", q["question_type"], q["topic"], q["difficulty"], q["answer_format"],
                        q["correct_option"] or q["tita_answer"], " ".join(q["exam_tags"]), q["provenance"]["local_id"]])
    wj("distractor_review.json", [dict(id=q["id"], correct=q["correct_option"] or q["tita_answer"], wrong_options=q["option_rationales"],
                                       common_wrong_entries=q["tita_common_wrong_entries"]) for q in bank["questions"]])
    groups = json.load(open(os.path.join(HERE, "build", "subject_groups.json")))
    lid = {q["provenance"]["local_id"]: q["id"] for q in bank["questions"]}
    lid.update({s["provenance"]["local_id"]: s["set_id"] for s in bank["sets"]})
    fams = defaultdict(list)
    for q in bank["questions"]:
        if not q["set_id"]:
            fams[q["concept_family"]].append(q["id"])
    for s in bank["sets"]:
        fams[s["concept_family"]].append(s["set_id"])
    wj("family_register.json", dict(note="Units (RC passages and VA items) that share any family_dependencies entry never appear in the same generated paper. SUBJ groups join units on related subjects across item types.",
                                    concept_families=fams, subject_groups={g: [lid[u] for u in m] for g, m in groups["groups"].items()}))
    cov = defaultdict(lambda: dict(questions=0, passages=0, difficulty=Counter(), types=Counter(), formats=Counter()))
    for q in bank["questions"]:
        c = cov[f"{q['chapter_number']:02d} {q['chapter']}"]; c["questions"] += 1; c["difficulty"][q["difficulty"]] += 1
        c["types"][q["question_type"]] += 1; c["formats"][q["answer_format"]] += 1
    for s in bank["sets"]:
        cov[f"{s['chapter_number']:02d} {s['chapter']}"]["passages"] += 1
    wj("coverage_map.json", {k: dict(v, difficulty=dict(v["difficulty"]), types=dict(v["types"]), formats=dict(v["formats"])) for k, v in sorted(cov.items())})


def evidence(bank):
    lid = {q["provenance"]["local_id"]: q["id"] for q in bank["questions"]}
    rounds = []
    for name, desc in (("b1", "Round 1: all 2,800 items, two independent blind solvers (S1, S2)"),
                       ("b2", "Round 2: the 257 items whose student-facing content changed in the audit, two new blind solvers")):
        s = json.load(open(os.path.join(HERE, "verify", "blind", f"{name}_score.json")))
        rounds.append(dict(round=name, description=desc, items=s["items"], both_solvers_agree=s["both_agree"],
                           disagreements=[dict(id=lid.get(d["id"], d["id"]), local_id=d["id"], **{k: v for k, v in d.items() if k in ("S1", "S2")}) for d in s["disagreements"]],
                           solver_notes=len(s["issues"])))
    adj = [
        "R05-B-04-2 (round 1, S2 answered differently): S2's own working argued for the keyed option; the typed letter was a slip. The keyed option was reworded to match the passage's 'came alongside' more exactly; round 2 both solvers agreed.",
        "V01-A-006 (round 1, S1 answered 52314 against key 53214): S1's working supported the key; the typed order was a slip. Key retained.",
        "V01-F-023 (round 1, both solvers answered 14325 against key 14352): the last two sentences could swap. The conclusion was rewritten so it can only follow the 'shields it' sentence; round 2 both solvers reached the key.",
    ]
    wj("evidence/blind_resolve_results.json", dict(rounds=rounds, adjudication=adj,
       method="Each pack was solved by a solver that saw only the student-facing item (options shuffled independently per solver). An item counts as agreed only when both solvers typed the keyed answer."))
    audits, sev = {}, Counter()
    for f in sorted(glob.glob(os.path.join(HERE, "verify", "audit_*.json"))):
        tag = os.path.basename(f)[6:-5]
        a = json.load(open(f))
        audits[tag] = a
        for x in a:
            sev[x.get("severity", "minor")] += 1
    wj("evidence/editorial_audit.json", dict(summary=dict(sev), files=len(audits), audits=audits,
       note="Hostile editorial audit of every file after blind round 1. Every critical and major finding was fixed in place; changed items were re-solved blind in round 2."))
    orig = json.load(open(os.path.join(HERE, "verify", "originality_check.json")))
    wj("evidence/originality.json", dict(
        internal="Every drafting file was checked against every other for shared 8-word runs (harness). Final state: no blocking overlaps; subject similarity across item types is recorded as SUBJ alias groups so related items never share a paper.",
        web_spot_check=dict(sentences=len(orig), matches=sum(1 for o in orig if o["result"] == "match"), results=orig,
                            limitation="Exact-phrase web searches on a random sample of 60 sentences; the search tool returned titles and URLs only, so this is a spot check, not a proof of originality.")))
    lc = {}
    for code, num, *_ in CHAPTERS:
        c = Counter(q["correct_option"] for q in bank["questions"] if q["chapter_number"] == num and q["correct_option"])
        if c:
            lc[f"{num:02d}"] = dict(c)
    wj("evidence/key_balance.json", dict(mcq_letters_by_chapter=lc,
       rules="MCQ letters assigned by code, balanced per chapter (difference at most 1 for RC and para summary), no run longer than 3 in chapter order, no letter more than twice inside one RC passage. Sentence-placement blanks balanced by authors; para-jumble and odd-sentence labels shuffled by code."))


def schema():
    opt = {"oneOf": [{"type": "null"}, {"type": "object", "properties": {L: {"type": "string", "minLength": 1} for L in "ABCD"},
                                        "required": list("ABCD"), "additionalProperties": False}]}
    q = {"type": "object", "required": ["id", "section", "area", "chapter_number", "chapter", "topic", "question_type", "standard", "exam_tags",
                                        "set_id", "answer_format", "question", "options", "correct_option", "tita_answer", "correct_answer",
                                        "explanation", "option_rationales", "tita_common_wrong_entries", "common_misconception", "difficulty",
                                        "difficulty_reason", "cognitive_level", "concept_family", "family_dependencies", "generator_eligible", "provenance"],
         "properties": {
             "id": {"type": "string", "pattern": "^CAT-VARC-(P(0[1-8])-\\d{3}-Q[1-5]|C(09|1[0-2])-\\d{3})$"},
             "section": {"const": "Verbal Ability and Reading Comprehension"},
             "area": {"enum": ["Reading Comprehension", "Verbal Ability"]},
             "chapter_number": {"type": "integer", "minimum": 1, "maximum": 12},
             "question_type": {"type": "string", "minLength": 1}, "standard": {"const": "CAT"},
             "exam_tags": {"type": "array", "items": {"enum": ["CAT", "XAT", "NMAT", "SNAP", "CMAT", "MAH-CET"]}, "contains": {"const": "CAT"}, "uniqueItems": True},
             "set_id": {"oneOf": [{"type": "null"}, {"type": "string", "pattern": "^CAT-VARC-P0[1-8]-\\d{3}$"}]},
             "answer_format": {"enum": ["MCQ", "TITA"]}, "question": {"type": "string", "minLength": 1}, "options": opt,
             "correct_option": {"enum": ["A", "B", "C", "D", None]},
             "tita_answer": {"oneOf": [{"type": "null"}, {"type": "string", "pattern": "^[1-5]{1,5}$"}]},
             "sentences": {"type": "array", "items": {"type": "object", "required": ["label", "text"]}},
             "explanation": {"type": "string", "minLength": 40}, "option_rationales": {"type": "object"},
             "tita_common_wrong_entries": {"type": "array", "items": {"type": "object", "required": ["value", "reason"]}},
             "difficulty": {"enum": ["Easy", "Medium", "Difficult"]},
             "cognitive_level": {"enum": ["Recall", "Understanding", "Application", "Analysis"]},
             "family_dependencies": {"type": "array", "items": {"type": "string"}, "minItems": 1},
             "generator_eligible": {"type": "boolean"}, "provenance": {"type": "object"}}}
    s = {"type": "object", "required": ["set_id", "set_type", "chapter_number", "chapter", "topic", "subtopic", "paragraphs", "word_count",
                                        "difficulty", "question_ids", "question_count", "exam_tags", "concept_family", "family_dependencies"],
         "properties": {"set_id": {"type": "string", "pattern": "^CAT-VARC-P0[1-8]-\\d{3}$"}, "set_type": {"const": "RC passage"},
                        "paragraphs": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1, "maxItems": 6},
                        "question_ids": {"type": "array", "minItems": 4, "maxItems": 5}, "question_count": {"enum": [4, 5]},
                        "difficulty": {"enum": ["Easy", "Medium", "Difficult"]}}}
    wj("question_bank_schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "urn:paper-tree:cat-varc:2.0.0",
        "title": "CAT VARC bank (schema v2, set-based)",
        "description": "Object with meta, sets (RC passages) and questions. RC questions link to their passage by set_id; VA questions have set_id null. "
                       "MCQ: four options, one correct (+3/-1). TITA: para jumbles key a digit string (e.g. 3142), odd sentence out a single digit (+3/0). "
                       "Cross-record rules (set membership, key balance, families) are checked by verify_release.py.",
        "type": "object", "required": ["meta", "sets", "questions"],
        "properties": {"meta": {"type": "object"}, "sets": {"type": "array", "items": s}, "questions": {"type": "array", "items": q}}})


def authoring():
    dst = os.path.join(OUT, "authoring")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for f in ("vlib.py", "harness.py", "DRAFTING_SPEC.md", "plan_batches.py", "plan.json", "claim.py", "claims.json", "blindtools.py",
              "changed.py", "build.py", "assemble.py", "status.py"):
        shutil.copy(os.path.join(HERE, f), dst)
    for d in ("briefs", "prompts", "tests"):
        if os.path.exists(os.path.join(HERE, d)):
            shutil.copytree(os.path.join(HERE, d), os.path.join(dst, d))
    shutil.copytree(os.path.join(HERE, "drafts"), os.path.join(dst, "drafts"), ignore=shutil.ignore_patterns("*.json", "__pycache__"))
    shutil.copytree(os.path.join(HERE, "verify"), os.path.join(dst, "verify"), ignore=shutil.ignore_patterns("drafts_*", "__pycache__"))
    shutil.copytree("/home/claude/blind_varc", os.path.join(dst, "verify", "blind_packs"))


def docs(bank, tests=None):
    Q = bank["questions"]; S = bank["sets"]
    fmt = Counter(q["answer_format"] for q in Q); dif = Counter(q["difficulty"] for q in Q)
    rows = []
    for code, num, area, name in CHAPTERS:
        qq = [q for q in Q if q["chapter_number"] == num]
        rows.append((num, name, area, len(qq), sum(1 for s in S if s["chapter_number"] == num), sum(1 for q in qq if q["answer_format"] == "TITA"),
                     Counter(q["difficulty"] for q in qq)))
    b1 = json.load(open(os.path.join(OUT, "evidence", "blind_resolve_results.json")))
    au = json.load(open(os.path.join(OUT, "evidence", "editorial_audit.json")))["summary"]
    tr = tests or (json.load(open(os.path.join(OUT, "evidence", "test_results.json"))) if os.path.exists(os.path.join(OUT, "evidence", "test_results.json")) else None)
    tline = f"{sum(1 for t in tr if t[1] == 'PASS')}/{len(tr)} automated tests pass" if tr else "automated tests not yet run"
    r1, r2 = b1["rounds"]
    words4 = [s["word_count"] for s in S if s["question_count"] == 4]; words5 = [s["word_count"] for s in S if s["question_count"] == 5]
    table = "| Ch | Chapter | Area | Questions | Passages | TITA | Easy / Medium / Difficult |\n|---|---|---|---:|---:|---:|---|\n" + "\n".join(
        f"| {n:02d} | {nm} | {ar} | {q} | {p or ''} | {t} | {d['Easy']} / {d['Medium']} / {d['Difficult']} |" for n, nm, ar, q, p, t, d in rows)
    readme = f"""# CAT VARC question bank v{VER}

Prepared {DATE} by Paper Tree Educational Studio. The complete CAT Verbal Ability and Reading Comprehension bank:
{len(Q)} original questions in 12 chapters, built on the same pipeline as the CAT QA bank v1.0.0.

Extract the whole folder and open **START_HERE.html**.

## At a glance

- {len(S)} original reading passages ({len(words4)} four-question passages of {min(words4)} to {max(words4)} words; {len(words5)} five-question passages of {min(words5)} to {max(words5)} words) carrying {sum(1 for q in Q if q['set_id'])} RC questions, in 8 subject domains.
- {sum(1 for q in Q if not q['set_id'])} verbal ability items: 350 para jumbles, 350 para summaries, 250 odd sentence out, 150 sentence placement.
- {fmt['MCQ']} MCQ (+3 / -1) and {fmt['TITA']} TITA (+3 / 0). TITA answers are digit strings: a para jumble is keyed like 3142, an odd sentence out like 4.
- {dif['Easy']} Easy / {dif['Medium']} Medium / {dif['Difficult']} Difficult (30 / 45 / 25 percent), on the CAT scale.
- Every wrong option carries a written reason why it is wrong; every para jumble and odd-one-out lists the most common wrong entries.
- MCQ letters balanced within each chapter (no run longer than 3, no letter more than twice in one passage).
- Exam reuse tags on every item (CAT always; XAT, NMAT, SNAP, CMAT, MAH-CET where suitable).

{table}

## Files

- `{BANK}.json`: the canonical bank (schema v2): `meta`, `sets` (passages) and `questions`. RC questions link to their passage by `set_id`.
- `{BANK}_questions.jsonl/.csv` and `{BANK}_passages.jsonl/.csv`: the same data, one record per line or row (nested fields JSON-encoded in CSV).
- `questions_only.json` and `answers_and_explanations.json`: student and teacher exports.
- `books/Chapter_NN_Student.html` and `Chapter_NN_Teacher.html`: searchable, filterable, printable books. RC books show each passage with its questions; teacher books add answers, explanations, the reason each wrong option fails and the common misconception.
- `Sample_Paper.html` and `Sample_Solutions.html`: a 24-question, 40-minute CAT-style VARC section (4 passages x 4 questions, 2 para jumbles, 3 para summaries, 2 odd sentence out, 1 sentence placement; seed 42).
- `generate_paper.py` and `Generator_Contract.md`: the paper generator (whole passages only). Example:
  `python generate_paper.py --bank {BANK}.json --seed 7 --output practice7`.
- `question_bank_schema.json`, `verify_release.py` (checks the release, including generator seeds 1 to 200).
- `coverage_map.json`, `family_register.json`, `question_index.csv`, `distractor_review.json`.
- `evidence/`: blind solving rounds, the editorial audit, originality checks, key balance and test results.
- `authoring/`: the full pipeline (drafting library, harness, spec, briefs, prompts, every drafting file, every verification file).

## For the CBT platform

- Passages are set records. A passage must be shown in a split-screen view beside its questions, and a paper must take whole passages.
- Para jumble answers are compared as exact digit strings; odd sentence out as a single digit. Sentence placement is an MCQ whose options are Blank (1) to Blank (4).
- `family_dependencies`: never put two units that share any entry into one paper (the generator enforces this).

## Verification

- Round 1: every item solved blind by two independent solvers who saw only the student view; both matched the key on {r1['both_solvers_agree']} of {r1['items']}. The {len(r1['disagreements'])} disagreements were adjudicated (two typing slips, one para jumble with a second defensible order, rewritten).
- Editorial audit of every file: {au.get('critical', 0)} critical, {au.get('major', 0)} major, {au.get('minor', 0)} minor findings; every critical and major finding fixed.
- Round 2: the {r2['items']} items whose student-facing content changed were solved blind again by two new solvers; both matched the key on {r2['both_solvers_agree']} of {r2['items']}.
- Originality: all passages and items are newly written; every file checked against every other for shared 8-word runs, with no blocking overlap left; a 60-sentence web spot check found no published match.
- {tline}.
- Not yet done: a human subject-expert review (`human_subject_expert_reviewed` is false on every record) and difficulty calibration with student data.
"""
    wt("README.md", readme)
    contract = f"""# Paper generator contract (CAT VARC)

`generate_paper.py` builds one CAT-style VARC section from the bank.

Inputs: `--bank`, `--seed` (same seed, same paper), `--output` (file prefix); optional `--rc-sets` (default 4),
`--rc-size` (4 = four-question passages only, the default; 5 = five-question passages only; 0 = both),
`--pj 2 --ps 3 --ooo 2 --sp 1` (verbal ability counts), `--exam`, `--chapter` (one RC chapter) and `--minutes` (default 40).

Guarantees:
1. Exactly `--rc-sets` whole passages with all their questions, followed by the requested numbers of each VA type.
2. Passages come from different RC chapters whenever at least `--rc-sets` chapters are available.
3. No two units (passages or VA items) share any entry of `family_dependencies`, so a paper never repeats a subject.
4. Difficulty as close as possible to 30 / 45 / 25 percent of the section (exact for the default 24-question paper); the deviation is written into the paper.
5. Only `generator_eligible` records; `--exam` keeps only passages whose questions are all tagged for that exam, and VA items tagged for it.
6. Marking: MCQ +3 / -1 / 0, TITA +3 / 0 / 0.

Outputs: `<prefix>_paper.json` (seed, passages, ordered question ids, marking, difficulty) and `<prefix>_answer_key.json`
(number, id, set_id, format, answer: letter for MCQ, digit string for TITA).

`verify_release.py` checks these guarantees for seeds 1 to 200.
"""
    wt("Generator_Contract.md", contract)
    tbl = "".join(f"<tr><td>{n:02d}</td><td><a href=\"books/Chapter_{n:02d}_Student.html\">{E(nm)}</a></td><td>{ar}</td><td>{q}</td><td>{p or ''}</td>"
                  f"<td><a href=\"books/Chapter_{n:02d}_Teacher.html\">Teacher book</a></td></tr>" for n, nm, ar, q, p, t, d in rows)
    start = page("CAT VARC question bank", f"<h1>CAT VARC question bank v{VER}</h1><p>{len(Q)} questions &middot; {len(S)} passages &middot; Paper Tree Educational Studio &middot; {DATE}</p>",
                 f"<article><h2>Start here</h2><p>Open a chapter's student book to practise, or its teacher book for answers and explanations. "
                 f"Try the <a href=\"Sample_Paper.html\">sample 24-question section</a> (<a href=\"Sample_Solutions.html\">solutions</a>). "
                 f"The <a href=\"Build_Report.html\">build report</a> explains how every item was verified.</p>"
                 f"<table><tr><th>Ch</th><th>Chapter</th><th>Area</th><th>Questions</th><th>Passages</th><th></th></tr>{tbl}</table></article>")
    wt("START_HERE.html", start)
    dis = "".join(f"<li>{E(a)}</li>" for a in b1["adjudication"])
    rep = page("CAT VARC build report", f"<h1>CAT VARC v{VER}: build report</h1><p>Paper Tree Educational Studio &middot; {DATE}</p>",
               f"""<article><h2>What was built</h2><p>{len(S)} original passages and {len(Q)} questions across 12 chapters; {fmt['MCQ']} MCQ and {fmt['TITA']} TITA;
{dif['Easy']} / {dif['Medium']} / {dif['Difficult']} Easy / Medium / Difficult. Passages average {round(sum(s['word_count'] for s in S) / len(S))} words.</p></article>
<article><h2>How it was made</h2><ol style="list-style:decimal;padding-left:22px">
<li>94 drafting batches written to a common spec: original prose only, no invented quotations or statistics attributed to real people, a written defence for every wrong option. Subjects claimed in a shared register so parallel batches could not collide.</li>
<li>Para jumble, odd one out and sentence placement keys are computed by code from the author's original ordered paragraph, so a key can never be mis-transcribed.</li>
<li>Machine harness on every file: counts, word counts, readability, option-length giveaways (the key may be the longest option in at most 40 percent of items), house style, and 8-word overlap against every other file.</li>
<li>Blind round 1: two independent solvers per item. Both matched the key on {r1['both_solvers_agree']} of {r1['items']}.</li>
<li>Hostile editorial audit of every file, informed by the solvers' notes: {au.get('critical', 0)} critical, {au.get('major', 0)} major and {au.get('minor', 0)} minor findings, all critical and major fixed.</li>
<li>Blind round 2 on the {r2['items']} changed items: both new solvers matched the key on {r2['both_solvers_agree']}.</li>
<li>Build: option letters balanced by code; subject alias groups computed across item types so related items never share a paper; {tline}.</li></ol></article>
<article><h2>Adjudicated disagreements</h2><ul>{dis}</ul></article>
<article><h2>Limits</h2><ul><li>No human subject expert has reviewed the bank yet; <code>human_subject_expert_reviewed</code> is false on every record.</li>
<li>Difficulty labels are editorial judgements on the CAT scale, not yet calibrated with student data.</li>
<li>The web originality check was a 60-sentence spot check; the main protection is that every passage was written fresh.</li>
<li>Next phase: DILR (sets with code-drawn charts), on the same pipeline.</li></ul></article>""")
    wt("Build_Report.html", rep)


def main():
    bank = json.load(open(os.path.join(HERE, "build", "bank.json")))
    if "--docs" in sys.argv:
        docs(bank); return
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copy(os.path.join(HERE, "release_files", "generate_paper.py"), OUT)
    shutil.copy(os.path.join(HERE, "release_files", "verify_release.py"), OUT)
    exports(bank); schema(); books(bank); sample(bank); evidence(bank); authoring(); docs(bank)
    print("assembled", OUT)


if __name__ == "__main__":
    main()
