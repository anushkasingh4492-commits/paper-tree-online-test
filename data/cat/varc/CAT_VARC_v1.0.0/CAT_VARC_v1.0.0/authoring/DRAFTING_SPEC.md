# CAT VARC bank: drafting spec (read fully before writing)

You are authoring part of a commercial CAT (IIM Common Admission Test) Verbal Ability and Reading
Comprehension bank for Paper Tree Educational Studio. It sits beside a finished 3,000-question CAT
Quantitative bank and NEET, MHT-CET and JEE banks that went through hostile errata audits. Every
item you write will be solved by TWO independent blind solvers who never see your key; both must
reach your key. A hostile editor then audits every key and every distractor defence. VARC cannot be
machine-solved, so the only protection is your precision: each item must have exactly one answer
that a strong, careful reader would defend from the text alone.

## The exam

- CAT VARC: 24 questions in 40 minutes. About 16 Reading Comprehension questions (4 passages with 4
  questions each) and about 8 Verbal Ability questions: para jumbles, para summaries, odd sentence
  out, sentence placement.
- MCQ: four options, +3 / -1. TITA (type in the answer): +3 / 0. Para jumbles and odd one out are
  TITA (the candidate types digits); RC, para summary and sentence placement are MCQ.
- CAT passages are dense, argumentative essays on ideas: philosophy, social science, history,
  economics, science, the arts, language. They take a position, qualify it, anticipate objections.
  They are not encyclopedia entries, news reports or textbook explanations. Questions test
  inference, the author's view, the function of parts, and what would strengthen or weaken a claim,
  far more than recall of details.

## Output

Write ONE Python file at the path in your brief. Start it with exactly:

```python
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *
```

Then call the vlib functions for your item kind. Read `/home/claude/catvarc/vlib.py` (signatures and
docstrings) and `/home/claude/catvarc/drafts/_sample.py` (one worked example of every kind). Use
plain Python strings; ASCII only. The subjects used in `_sample.py` are reserved.

Never choose option letters. You give the correct option and three distractors; the build assigns
letters. Never refer to options by letter anywhere.

## Originality and facts (non-negotiable)

1. **Everything is original prose written by you now.** Do not reproduce, paraphrase closely or
   stitch together any published passage, essay, book, article or past exam item, including famous
   openings and well-known quotations. Do not imitate a specific living author's text.
2. **No invented facts presented as real.** Do not invent statistics, study results, dates,
   quotations, book titles or positions and attribute them to real people, organisations or
   studies. Do not put words in the mouths of real people. Real names, events and works may appear
   only for facts that are well established and that you are sure of (for example, that Darwin
   published On the Origin of Species in 1859). When in doubt, argue about the idea without names
   ("some historians", "a common view holds", "consider a town where ...").
3. Hypothetical illustrations are welcome if they are clearly hypothetical.
4. Avoid hot-button current politics, religion-baiting, and anything defamatory or demeaning to a
   group. Contested topics may be discussed in the measured, even-handed way of a serious essay.
5. Each passage, paragraph and sentence set must be on a different subject from the others in your
   file and from every subject other batches have claimed. Claim subjects with `claim.py` (see your
   brief) before writing; a CLASH means choose a different subject. Your `family` slug should name
   the claimed subject.

## House style

- ASCII only: straight quotes, no curly quotes, **no em dash, en dash, or a hyphen or double hyphen
  used as a dash** (house rule). Use commas, colons, semicolons, brackets or separate sentences.
  Ordinary hyphenated words (long-term, well-known) are fine.
- British/Indian spelling is preferred (behaviour, organise, centre), consistently within an item.
- No meta commentary anywhere in student-facing text: never mention reviews, corrections, the bank,
  authors, "this item", or the drafting process.
- In explanations and defences, cite the passage: "paragraph 2 says ...", or a short quoted phrase.
- Quotations from the passage inside a stem, option or explanation use single quotes and must match
  the passage text exactly.

## Difficulty (CAT scale; overall split 30 / 45 / 25)

- **Easy**: the answer is located in one or two sentences, distractors are clearly off once the
  relevant lines are read. About 1 minute.
- **Medium**: typical CAT; needs inference or paraphrase across a paragraph, with one tempting
  distractor that is partly right. 1.5 to 2 minutes.
- **Difficult**: upper end of CAT; needs the whole argument, a subtle distinction (scope, degree,
  the author's view versus a view the author reports), or two distractors that are hard to
  separate. Still exactly one defensible answer.

`difficulty_reason` says concretely why. `cognitive`: Recall, Understanding, Application, Analysis.

## Distractors and defences (MCQ: RC and para summary)

Each wrong option is wrong for a reason you can state from the text, and you state it in the
defence (at least one full sentence that cites the passage). Use the classic CAT traps:
- distortion: uses passage words but changes the relation (cause for correlation, some for all);
- extreme or absolute: "always", "only", "proves", where the passage hedges;
- out of scope: plausible in the world but not supported by the passage;
- too narrow or too broad (for main idea and summary items);
- opposite or reversal of the author's view;
- the view of someone the author reports or rejects, presented as the author's own;
- true but irrelevant to the question asked.

Rules:
- The key must be clearly supported and must survive a hostile reading; no distractor may also be
  defensible. If a distractor is "arguably also true", rewrite it.
- **Length and wording give nothing away.** The key is NOT systematically the longest, the most
  qualified or the most nuanced option. The harness blocks a file in which the key is the longest
  option in more than 40% of MCQs. Make distractors as carefully worded and as long as the key.
- Do not make the key the only option that paraphrases while all distractors copy passage words.
  Mix: some distractors should paraphrase, and the key may reuse a key term.
- Options are grammatically parallel and each completes the stem.
- Banned options: "None of these", "All of the above", "Cannot be determined", "Both ... and ...".

## Reading comprehension

Passage (`passage(...)`):
- 4-question passages: 400 to 580 words. 5-question passages: 570 to 730 words.
- 2 to 5 paragraphs. An argument with a clear authorial stance, at least one qualification or
  concession, and some development (example, contrast, objection and reply). It may begin in the
  middle of a debate, as CAT excerpts do, but must be self-contained.
- Register: serious essay prose, readability grade about 12 to 17. Long sentences are fine;
  obscurity for its own sake is not.
- Vary structures across your file: problem and solution, claim and objection, comparison of two
  views, history of an idea, critique of a common belief, case study leading to a general point.
- Passage difficulty: set by density, abstraction and how indirect the stance is.

Questions (`rcq(...)`), ids `<set_id>-1` ... `-4` or `-5`:
- Mix question types within each passage (no type more than twice per passage, normally three or
  four types per passage). Across your file use at least 7 of the 9 types; "Main idea / primary
  purpose" at most once per passage; Inference is the most common type.
- "Except / not supported" stems capitalise EXCEPT, NOT or LEAST.
- Stems are CAT-like: "The author would most likely agree with which of the following?", "Which of
  the following, if true, would most weaken the claim that ...?", "The passage suggests that ...",
  "The example of ... serves to ...", "Which one of the following best captures the meaning of
  'X' as used in paragraph 3?". A stem may end with "?" or be an incomplete sentence completed by
  the options.
- Every question must be answerable from the passage alone (plus ordinary general knowledge), and
  the answer must not be guessable without reading the passage.
- Questions within a passage must not give away each other's answers.
- Difficult questions should need synthesis across paragraphs or a fine distinction.

## Para jumble (`pj`, TITA)

- Write the 4 or 5 sentences of a coherent paragraph IN THE CORRECT ORDER. Code shuffles them and
  computes the key. In explanation, misconception and trap reasons refer to sentences only as
  "sentence [[1]]", "sentence [[2]]" ... (your original order); code replaces these with the
  printed labels. Never write a raw sentence number.
- Each sentence 12 to 40 words. The paragraph is about 70 to 170 words.
- **Exactly one order is defensible.** Lock every link: a clear opener that introduces the subject
  (and no other sentence that could open), backward references (this, such, these, the latter, the
  same), connectives (however, therefore, yet), chronology, general to specific, claim to example to
  conclusion. Check every adjacent pair: could two sentences swap? Could the paragraph begin or end
  differently? Could a pair be moved as a block? If yes, add a lock or rewrite.
- Do not make it trivial with mechanical cues alone. Medium and Difficult jumbles should depend on
  the logic of the idea (a mandatory pair whose order follows from the argument), not only on
  pronouns. Difficult jumbles often have a tempting but wrong opener.
- Common ambiguities to rule out: a 'reason' sentence and an 'in other words / thus' restatement
  that could come in either order at the end; two examples that could swap; a general claim that
  could open or close; a 'Yet' sentence that could attach to two different sentences. If the
  last two sentences could swap, rewrite one so it must come last (or must follow the other).
- traps: the one or two most tempting wrong orders (in your numbering) with the reason each fails.

## Odd sentence out (`ooo`, TITA)

- Four sentences that form one coherent paragraph (in natural order) and one odd sentence. Code
  jumbles all five and keys the odd one.
- The odd sentence must be **on the same broad subject** and plausible-looking, but it must break
  the paragraph: a different focus, a different time or scope, a claim that does not connect to the
  argument. Easy items may be more obviously off-topic; Medium and Difficult ones share vocabulary
  with the paragraph and must be rejected on function.
- **Exactly one sentence can be removed.** Check that each of the four coherent sentences is needed
  and linked, and that the four still form a paragraph without the odd one. If two sentences could
  each be the odd one, rewrite.
- traps: one or two coherent sentences students wrongly pick ([[n]] numbering) and why each belongs.

## Para summary (`ps`, MCQ)

- One paragraph of 90 to 190 words making a point (not a list of facts).
- The key captures the central point AND its scope and qualification, in fresh words, 15 to 45
  words. It may not add anything absent from the paragraph.
- Distractors: too narrow (one detail), too broad or extreme, distortion of the relation, adds an
  outside idea or a prescription the paragraph does not make, contradicts a qualification. All four
  options should be of similar length (within about 30% of each other) and similar tone.

## Sentence placement (`sp`, MCQ)

- A paragraph of 5 to 8 sentences (120 to 280 words) with one sentence removed. You choose four gap
  positions (see the docstring); exactly one fits. The paragraph prints with (1) (2) (3) (4).
- The missing sentence must fit at exactly one gap because of a backward reference and a forward
  link (or a structural role). For each wrong gap give a concrete reason in `gap_reasons`.
- Spread the true gap: across your file, the true gap is (1), (2), (3) and (4) about equally often
  (the harness checks).
- The paragraph must read naturally without the sentence too (no dangling "this" that only the
  missing sentence explains, except at the true gap).

## Families and exam tags

- `family`: a slug starting with your brief's family prefix that names the subject, for example
  `R03B-dowry-and-inheritance` or `V02C-urban-heat`. Every passage has its own family. VA items:
  each item normally has its own family; at most 3 items may share one.
- `exams`: the entrance tests the item suits. CAT always. Easy and Medium items: all six (the
  default). Difficult items: usually `("CAT", "XAT")` only.

## Self-audit (after the harness passes, before reporting)

Re-read every item as a hostile editor who is trying to break it:
1. Solve it cold. Is the key the only defensible answer? Try hard to defend each distractor; if you
   can, rewrite it.
2. Each defence: is it true, and does it cite the text?
3. Quotations match the passage exactly; paragraph numbers in stems and explanations are right.
4. Para jumble: try at least three alternative orders and confirm each fails. Odd one out: try
   removing each of the other four sentences and confirm the result is worse.
5. Facts: nothing invented and attributed to a real person, body or study; no fabricated numbers
   presented as real.
6. Difficulty labels fair; no near-duplicate subjects inside your file; every subject claimed.

## Before reporting back

Run the harness command in your brief. Fix everything under BLOCKING. Read every ADVISORY line and
fix what is real (word counts, uneven options, overlaps). Report back ONLY: the harness summary
lines (kinds, counts, key longest/shortest, gaps), any flags you set, and any item you are still
unsure about. Do not paste the items.
