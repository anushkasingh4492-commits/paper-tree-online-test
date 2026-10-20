# -*- coding: utf-8 -*-
"""Authoring helper for the CAT VARC bank (Paper Tree Educational Studio).

Every drafting file does:   from vlib import *
and then calls, depending on its brief:
  RC files:  passage(...) once per passage, then rcq(...) once per question of that passage
  V01 files: pj(...)      para jumble
  V02 files: ps(...)      para summary
  V03 files: ooo(...)     odd sentence out
  V04 files: sp(...)      sentence placement

Option letters are NOT chosen by authors: give the correct option and three distractors; the
build assigns letters (balanced per chapter). Para-jumble and odd-one-out labels are produced by
code from the order you write, so the key always matches your original paragraph.

Placeholders (PJ and OOO only): in explanation, misconception and trap reasons refer to sentences
as [[1]], [[2]] ... meaning "the sentence you wrote first, second ..." in YOUR original order,
and (OOO) [[X]] for the odd sentence. Code replaces them with the printed labels.
"""
import hashlib, random, re

SETS = []
QUESTIONS = []

DIFFICULTIES = ("Easy", "Medium", "Difficult")
COGNITIVE = ("Recall", "Understanding", "Application", "Analysis")
EXAMS = ("CAT", "XAT", "NMAT", "SNAP", "CMAT", "MAH-CET")
RC_QTYPES = (
    "Main idea / primary purpose",
    "Specific detail",
    "Inference",
    "Author's tone / attitude",
    "Structure / function",
    "Strengthen / weaken / assumption",
    "Application / analogy",
    "Except / not supported",
    "Meaning in context",
)


def _rng(local_id, salt=""):
    return random.Random(int(hashlib.sha256((local_id + salt).encode()).hexdigest()[:12], 16))


def _common(local_id, difficulty, cognitive, exams):
    assert difficulty in DIFFICULTIES, (local_id, difficulty)
    assert cognitive in COGNITIVE, (local_id, cognitive)
    assert "CAT" in exams and all(e in EXAMS for e in exams), (local_id, exams)


def _dist(local_id, distractors):
    assert distractors and len(distractors) == 3, (local_id, "need exactly 3 distractors")
    out = []
    for d in distractors:
        assert isinstance(d, tuple) and len(d) == 2 and d[0].strip() and len(d[1].strip()) >= 25, \
            (local_id, "distractor = (option_text, why_wrong) with a real defence (>= 25 chars)")
        out.append(dict(text=d[0].strip(), rationale=d[1].strip()))
    return out


# ---------------------------------------------------------------- Reading comprehension
def passage(set_id, topic, subtopic, paragraphs, difficulty, difficulty_reason, family,
            exams=EXAMS, flags=""):
    """Register one RC passage.

    set_id      e.g. "R01-A-03" (prefix from the brief, two-digit passage number)
    topic       the brief's topic label; subtopic: one precise line on what the passage argues
    paragraphs  list of paragraph strings (plain text, ASCII), 1 to 6 paragraphs
    difficulty  of the passage itself (density, abstraction, argument structure)
    family      slug unique to this passage's subject, e.g. "R01A-moral-luck"
    """
    _common(set_id, difficulty, "Analysis", exams)
    assert isinstance(paragraphs, (list, tuple)) and 1 <= len(paragraphs) <= 6, (set_id, "1 to 6 paragraphs")
    assert all(isinstance(p, str) and p.strip() for p in paragraphs), (set_id, "empty paragraph")
    assert not any(s["set_id"] == set_id for s in SETS), (set_id, "duplicate set_id")
    SETS.append(dict(set_id=set_id, kind="RC", topic=topic, subtopic=subtopic,
                     paragraphs=[p.strip() for p in paragraphs], difficulty=difficulty,
                     difficulty_reason=difficulty_reason, family=family, exams=list(exams), flags=flags))


def rcq(local_id, qtype, difficulty, question, correct, distractors, explanation, misconception,
        difficulty_reason, cognitive="Analysis", exams=EXAMS, flags=""):
    """Register one RC question. local_id = "<set_id>-<n>", e.g. "R01-A-03-2".

    Its passage must already be registered. explanation cites the passage (paragraph numbers or
    short quoted phrases) and says why the key is right; each distractor carries why it is wrong.
    """
    _common(local_id, difficulty, cognitive, exams)
    assert qtype in RC_QTYPES, (local_id, qtype)
    m = re.fullmatch(r"(.+)-(\d)", local_id)
    assert m, (local_id, "RC id must be <set_id>-<n>")
    sid = m.group(1)
    assert any(s["set_id"] == sid for s in SETS), (local_id, "register the passage first")
    QUESTIONS.append(dict(local_id=local_id, kind="RC", set_id=sid, topic=qtype, question_type=qtype,
                          difficulty=difficulty, question=question.strip(), answer_format="MCQ",
                          correct=correct.strip(), distractors=_dist(local_id, distractors),
                          explanation=explanation.strip(), common_misconception=misconception.strip(),
                          difficulty_reason=difficulty_reason, cognitive_level=cognitive,
                          exams=list(exams), flags=flags, family=None))


# ---------------------------------------------------------------- Para jumble
def _pj_order(local_id, n):
    """Printed order: a derangement-like shuffle that keeps at most one original adjacent pair."""
    r = _rng(local_id, "pj")
    while True:
        perm = list(range(n)); r.shuffle(perm)
        if perm == list(range(n)):
            continue
        adj = sum(1 for i in range(n - 1) if perm[i + 1] == perm[i] + 1)
        if adj <= 1:
            return perm  # perm[k] = original index printed at label k+1


def _sub(text, mapping):
    def rep(m):
        k = m.group(1)
        assert k in mapping, ("unknown placeholder [[%s]]" % k)
        return mapping[k]
    return re.sub(r"\[\[(\w+)\]\]", rep, text)


def pj(local_id, topic, subtopic, difficulty, sentences, explanation, misconception, family,
       difficulty_reason, traps=(), cognitive="Analysis", exams=EXAMS, flags=""):
    """Para jumble (TITA). sentences = the 4 or 5 sentences IN THE CORRECT ORDER.

    traps = up to 3 tuples (wrong_order, reason) where wrong_order uses YOUR original numbering,
    e.g. "2134" means "your 2nd sentence first, then your 1st, ...". Code converts to labels.
    """
    _common(local_id, difficulty, cognitive, exams)
    n = len(sentences)
    assert n in (4, 5), (local_id, "4 or 5 sentences")
    perm = _pj_order(local_id, n)
    label_of = {orig: k + 1 for k, orig in enumerate(perm)}           # original index -> printed label
    mapping = {str(i + 1): str(label_of[i]) for i in range(n)}
    key = "".join(str(label_of[i]) for i in range(n))
    tr = []
    for wo, reason in traps:
        assert sorted(wo) == [str(i + 1) for i in range(n)] and wo != "".join(str(i + 1) for i in range(n)), (local_id, "bad trap order", wo)
        tr.append(dict(value="".join(mapping[c] for c in wo), rationale=_sub(reason, mapping)))
    printed = [sentences[perm[k]].strip() for k in range(n)]
    QUESTIONS.append(dict(local_id=local_id, kind="PJ", topic=topic, subtopic=subtopic,
                          question_type="Para jumble", difficulty=difficulty, answer_format="TITA",
                          sentences_original=[s.strip() for s in sentences], printed=printed,
                          tita_answer=key, tita_traps=tr,
                          explanation=_sub(explanation, mapping).strip(),
                          common_misconception=_sub(misconception, mapping).strip(),
                          family=family, difficulty_reason=difficulty_reason, cognitive_level=cognitive,
                          exams=list(exams), flags=flags, raw_explanation=explanation))


# ---------------------------------------------------------------- Odd sentence out
def ooo(local_id, topic, subtopic, difficulty, sentences, odd, explanation, misconception, family,
        difficulty_reason, traps=(), cognitive="Analysis", exams=EXAMS, flags=""):
    """Odd sentence out (TITA). sentences = the 4 coherent sentences IN THEIR NATURAL ORDER;
    odd = the sentence that does not belong. Code jumbles all five and keys the odd one's label.
    traps = up to 2 tuples (i, reason): a coherent sentence i (1 to 4, your numbering) that
    students wrongly pick, and why it actually belongs.
    """
    _common(local_id, difficulty, cognitive, exams)
    assert len(sentences) == 4 and odd.strip(), (local_id, "4 coherent sentences + 1 odd")
    allx = [s.strip() for s in sentences] + [odd.strip()]
    r = _rng(local_id, "ooo")
    while True:
        perm = list(range(5)); r.shuffle(perm)
        adj = sum(1 for i in range(4) if perm[i + 1] == perm[i] + 1 and perm[i] < 4)
        if adj <= 1:
            break
    label_of = {orig: k + 1 for k, orig in enumerate(perm)}
    mapping = {str(i + 1): str(label_of[i]) for i in range(4)}
    mapping["X"] = str(label_of[4])
    tr = []
    for i, reason in traps:
        assert i in (1, 2, 3, 4), (local_id, "trap index 1..4")
        tr.append(dict(value=mapping[str(i)], rationale=_sub(reason, mapping)))
    QUESTIONS.append(dict(local_id=local_id, kind="OOO", topic=topic, subtopic=subtopic,
                          question_type="Odd sentence out", difficulty=difficulty, answer_format="TITA",
                          sentences_original=allx, printed=[allx[perm[k]] for k in range(5)],
                          tita_answer=mapping["X"], tita_traps=tr,
                          explanation=_sub(explanation, mapping).strip(),
                          common_misconception=_sub(misconception, mapping).strip(),
                          family=family, difficulty_reason=difficulty_reason, cognitive_level=cognitive,
                          exams=list(exams), flags=flags, raw_explanation=explanation))


# ---------------------------------------------------------------- Para summary
def ps(local_id, topic, subtopic, difficulty, paragraph, correct, distractors, explanation,
       misconception, family, difficulty_reason, cognitive="Analysis", exams=EXAMS, flags=""):
    """Para summary (MCQ). paragraph = one paragraph; correct = the best summary; distractors =
    3 tuples (summary_text, why_wrong)."""
    _common(local_id, difficulty, cognitive, exams)
    QUESTIONS.append(dict(local_id=local_id, kind="PS", topic=topic, subtopic=subtopic,
                          question_type="Para summary", difficulty=difficulty, answer_format="MCQ",
                          paragraph=paragraph.strip(), correct=correct.strip(),
                          distractors=_dist(local_id, distractors), explanation=explanation.strip(),
                          common_misconception=misconception.strip(), family=family,
                          difficulty_reason=difficulty_reason, cognitive_level=cognitive,
                          exams=list(exams), flags=flags))


# ---------------------------------------------------------------- Sentence placement
def sp(local_id, topic, subtopic, difficulty, sentences, missing, gaps, explanation, gap_reasons,
       misconception, family, difficulty_reason, cognitive="Analysis", exams=EXAMS, flags=""):
    """Sentence placement (MCQ over gaps 1 to 4).

    sentences   the paragraph WITHOUT the missing sentence, in order (5 to 9 sentences)
    missing     the removed sentence
    gaps        4 distinct gap positions, ascending; position p means "just before sentences[p]",
                and p == len(sentences) means "after the last sentence". Exactly one of them is
                the true position (the first entry of gap_reasons is NOT special; see below).
    gap_reasons dict {position: why the missing sentence does not fit there} for the THREE wrong
                gaps; the true gap is the one position in gaps not in gap_reasons.
    The printed paragraph shows (1) (2) (3) (4) at the gaps in order; options are 1, 2, 3, 4.
    explanation refers to gaps by their printed numbers, e.g. "gap (3)".
    """
    _common(local_id, difficulty, cognitive, exams)
    n = len(sentences)
    assert 5 <= n <= 9, (local_id, "5 to 9 remaining sentences")
    assert len(gaps) == 4 and list(gaps) == sorted(set(gaps)) and all(0 <= g <= n for g in gaps), (local_id, "gaps")
    wrong = set(gap_reasons)
    assert len(wrong) == 3 and wrong <= set(gaps), (local_id, "gap_reasons must cover exactly 3 of the gaps")
    true = [g for g in gaps if g not in wrong][0]
    ordinal = gaps.index(true)  # 0..3 -> printed gap number ordinal+1
    parts = []
    for i in range(n + 1):
        if i in gaps:
            parts.append("(%d)" % (gaps.index(i) + 1))
        if i < n:
            parts.append(sentences[i].strip())
    QUESTIONS.append(dict(local_id=local_id, kind="SP", topic=topic, subtopic=subtopic,
                          question_type="Sentence placement", difficulty=difficulty, answer_format="MCQ",
                          sentences=[s.strip() for s in sentences], missing=missing.strip(), gaps=list(gaps),
                          true_gap=true, key_number=ordinal + 1, printed_paragraph=" ".join(parts),
                          gap_reasons={str(gaps.index(g) + 1): v.strip() for g, v in gap_reasons.items()},
                          explanation=explanation.strip(), common_misconception=misconception.strip(),
                          family=family, difficulty_reason=difficulty_reason, cognitive_level=cognitive,
                          exams=list(exams), flags=flags))
