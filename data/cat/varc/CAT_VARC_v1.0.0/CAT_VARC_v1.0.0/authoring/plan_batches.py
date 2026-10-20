# -*- coding: utf-8 -*-
"""Batch plan for the CAT VARC bank. Writes briefs/<TAG>.md and plan.json.

Totals: RC 400 passages / 1,700 Qs (100 five-question passages); VA 1,100 items.
Difficulty exactly 30/45/25 per chapter (largest remainder), whole bank 840/1260/700.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

RC = {
 "R01": ("Philosophy and Ethics", [
   ("A", "Knowledge and belief", "Epistemology: testimony and trust in others' word, scepticism, expertise and deference, rational disagreement, evidence and belief, self-knowledge, ignorance, intellectual humility, understanding versus knowing."),
   ("B", "Mind and self", "Philosophy of mind and personal identity: consciousness, other minds, free will and responsibility, the self over time, memory and identity, emotions and reason, attention, agency."),
   ("C", "Moral philosophy", "Ethical theory: moral luck, duty versus consequences, virtue and character, moral progress, blame and forgiveness, supererogation, moral intuitions, relativism, promises."),
   ("D", "Political philosophy", "Justice and the state: liberty, equality, toleration, rights, legitimacy and consent, punishment, civic virtue, merit and desert, public reason, the limits of majority rule."),
   ("E", "Applied ethics", "Ethics in practice: obligations to future generations, animals, medical consent, ethics of technology and surveillance, privacy, ethics of risk, lying and deception, charity and effective giving."),
   ("F", "Science and reasoning", "Philosophy of science and reasoning: explanation, models and idealisation, induction, simplicity, the role of anomalies, objectivity and values in science, thought experiments, probability and chance."),
   ("G", "Traditions and the good life", "Comparative philosophy and the good life: happiness and its measures, meaning, death and mortality, Stoic, Buddhist, Daoist or classical Indian ideas (only well-established doctrines, no invented attributions), work and leisure, boredom, solitude."),
 ]),
 "R02": ("Psychology and Cognitive Science", [
   ("A", "Perception, attention and memory", "How minds take in and keep information: perception as inference, attention and distraction, memory reconstruction, forgetting, false memory, expertise in seeing, time perception."),
   ("B", "Judgement and decision-making", "Heuristics and biases, risk perception, choice overload, intuition versus deliberation, the limits of bias research, framing, overconfidence, debiasing, rationality debates."),
   ("C", "Emotion, motivation and wellbeing", "Emotions and their functions, motivation and reward, habits, willpower debates, happiness research and its pitfalls, boredom, curiosity, grief, stress as a concept."),
   ("D", "Development and learning", "Childhood development, play, learning and teaching, expertise and practice, intelligence and its measurement debates, adolescence, language acquisition in children, ageing minds."),
   ("E", "Social psychology", "Conformity, group identity, trust and cooperation, persuasion, empathy and its limits, stereotypes, status, reputation, the replication debates in social psychology (stated cautiously)."),
   ("F", "Minds in nature", "Animal cognition, evolution of mind, language and thought, consciousness in science, embodied cognition, the brain and its metaphors, artificial versus natural intelligence."),
 ]),
 "R03": ("Society, Anthropology and Culture", [
   ("A", "Cities and space", "Urban life: neighbourhoods, public space, density, gentrification, informal settlements, streets and walking, the suburb, migration to cities, the meaning of home."),
   ("B", "Family and generations", "Kinship, marriage customs as social institutions, generational change, childhood across cultures, ageing societies, care work within families, naming practices."),
   ("C", "Ritual and belief as social practice", "Rituals, festivals, pilgrimage, the sociology of religion (neutral, descriptive), superstition, secularisation debates, sacred space, mourning practices."),
   ("D", "Work, class and status", "Professions, class and taste, status symbols, leisure and its history, the meaning of work, credentials, social mobility, servants and service work."),
   ("E", "Consumption and identity", "Food cultures, fashion, consumerism, globalisation and local identity, tourism, authenticity, nostalgia, brands as culture, collecting."),
   ("F", "Exchange and reciprocity", "Anthropology of gifts, money and debt as social relations, hospitality, reciprocity, indigenous and local knowledge, the commons in village life, oral traditions."),
   ("G", "Institutions and trust", "Schools and meritocracy, bureaucracy as experienced by citizens, trust in institutions, rules and norms, social capital, volunteering, clubs and associations, sport as institution."),
 ]),
 "R04": ("History and Politics", [
   ("A", "History and memory", "Historiography: archives and their silences, monuments and public memory, nationalism and history writing, oral history, counterfactuals, how periods get named, the uses of the past."),
   ("B", "Empire and its aftermath", "Empires, colonial rule and decolonisation (only well-established facts), indentured labour, cartography and borders, language and empire, the writing of colonial history."),
   ("C", "State, law and citizenship", "The modern state, bureaucracy, census and classification, constitutions, the rule of law, citizenship, policing as an institution, taxation and the state."),
   ("D", "Democracy and participation", "Elections and representation, populism (analytically, no current partisan politics), deliberation, protest, political parties, voting behaviour, the press in democracy."),
   ("E", "War, peace and world order", "Diplomacy, deterrence, the ethics and history of war, international institutions, sovereignty, sanctions, peace-making, alliances."),
   ("F", "Everyday life in history", "Trade routes, epidemics and societies, calendars and timekeeping, roads and travel, the history of reading, markets and fairs, households, the history of the senses."),
 ]),
 "R05": ("Economics, Business and Development", [
   ("A", "Markets and behaviour", "Prices and value, behavioural economics, auctions, advertising, consumer choice, market design, nudges and their critics, the economics of attention."),
   ("B", "Development and inequality", "Poverty measurement, growth and development, inequality debates, microfinance (cautious), cash transfers, institutions and development, informality, aid."),
   ("C", "Firms and organisations", "Management, corporate culture, innovation in firms, incentives, metrics, organisational failure, family businesses, start-ups and incumbents, leadership myths."),
   ("D", "Work and technology", "Automation, the future of work, gig work, skills and wages, productivity puzzles, unions as institutions, working hours, remote work."),
   ("E", "Money and finance", "Money and its forms, banking, financial crises, speculation and bubbles, debt, inflation as an idea, central banking, insurance and risk sharing."),
   ("F", "Trade and industry", "Trade and comparative advantage, globalisation and its discontents, industrial policy, supply chains, protectionism debates, special economic zones, standards."),
   ("G", "Growth and the environment", "Environmental economics, the commons, pricing nature, growth and degrowth debates, carbon pricing, resource curse, measuring wellbeing beyond GDP."),
 ]),
 "R06": ("Science, Environment and Technology", [
   ("A", "Evolution and life", "Evolution, adaptation and its misreadings, genes and environment, cooperation in nature, the origin of life debates, development and form, extinction."),
   ("B", "Ecology and conservation", "Ecosystems, biodiversity, rewilding, invasive species, conservation dilemmas, keystone species, wildlife and people, forests."),
   ("C", "Earth, climate and oceans", "Climate science as a field, deep time and geology, oceans, weather and forecasting, glaciers and ice, monsoons, natural hazards, adaptation."),
   ("D", "Physics, cosmos and measurement", "Measurement and units, cosmology, quantum ideas for the general reader, time and clocks (not the redefinition of the second), symmetry, the scale of the universe, the history of physics ideas."),
   ("E", "Medicine and the body", "Medicine as science, diagnosis and uncertainty, vaccines and public health as institutions, the microbiome, sleep, pain, antibiotics and resistance, placebo."),
   ("F", "Computing, AI and data", "Algorithms and society, artificial intelligence, data and privacy, software and failure, the history of computing, automation of judgement, digital infrastructure."),
   ("G", "Science as an institution", "Peer review, replication, expertise and public trust, science communication, citizen science, funding and fashions in research, the idea of the scientific method."),
 ]),
 "R07": ("Arts, Literature and Aesthetics", [
   ("A", "Literary form", "The novel and its conventions, poetry and meaning, narrative point of view, the short story, genre fiction and literary value, endings, character, the essay as form."),
   ("B", "Reading, translation and criticism", "Translation, the literary canon, criticism and its purposes, reading habits, the author and intention, adaptation, classics and their afterlives."),
   ("C", "Visual art and museums", "Painting and seeing, photography, museums and display, restoration and authenticity, forgery, the art market, public art, the history of portraiture."),
   ("D", "Music and performance", "Music and emotion, improvisation, classical traditions (well-established facts only), recording and listening, theatre, dance, the performer and the score, folk forms."),
   ("E", "Architecture, design and craft", "Architecture and everyday life, ornament, design for use, craft and skill, preservation of buildings, vernacular building, the handmade and the machine-made."),
   ("F", "Taste and popular culture", "Cinema, popular culture and seriousness, taste and judgement, beauty, kitsch, fandom, the aesthetics of nature, humour."),
 ]),
 "R08": ("Language, Media and Communication", [
   ("A", "Language and linguistics", "Language change, multilingualism, dialects and standards, grammar and prescriptivism, endangered languages, names and naming, metaphor in language, sign languages."),
   ("B", "Writing and the book", "Writing systems, literacy, the history of the book and print, handwriting, libraries, dictionaries, editing, reading on screens."),
   ("C", "News and journalism", "Journalism and objectivity, news values, the attention economy, misinformation (analytically), the business of news, investigative work, the public sphere."),
   ("D", "Persuasion and digital speech", "Rhetoric, persuasion, social media and conversation, online anonymity, memes and virality, euphemism, political language (analytical, non-partisan), listening."),
 ]),
}

VA = {
 "V01": ("Para jumbles", "PJ", 350, 14),
 "V02": ("Para summary", "PS", 350, 14),
 "V03": ("Odd sentence out", "OOO", 250, 10),
 "V04": ("Sentence placement", "SP", 150, 6),
}
VA_SUBJECTS = ["Philosophy and ethics", "Psychology", "Society and culture", "History and politics",
               "Economics and business", "Science and environment", "Technology", "Arts and literature",
               "Language and media", "Education", "Health and medicine", "Cities and geography"]

CH_TARGET = {  # chapter-level difficulty totals (whole bank 840/1260/700)
 "RC": (510, 765, 425), "V01": (105, 158, 87), "V02": (105, 157, 88), "V03": (75, 113, 62), "V04": (45, 67, 38)}


def split(total, sizes):
    """Distribute an integer total across batches proportionally to sizes (largest remainder)."""
    S = sum(sizes); raw = [total * s / S for s in sizes]; base = [int(r) for r in raw]
    rem = total - sum(base)
    for i in sorted(range(len(sizes)), key=lambda i: -(raw[i] - base[i]))[:rem]:
        base[i] += 1
    return base


def alloc(target, sizes):
    """Per-batch (E, M, D) with exact column totals and row sums == sizes."""
    n = len(sizes)
    E = split(target[0], sizes); M = split(target[1], sizes)
    D = [s - e - m for s, e, m in zip(sizes, E, M)]
    # repair any drift so column D also hits its target
    i = 0
    while sum(D) != target[2]:
        if sum(D) > target[2]:
            j = max(range(n), key=lambda k: D[k]); D[j] -= 1; M[j] += 1
        else:
            j = max(range(n), key=lambda k: M[k]); D[j] += 1; M[j] -= 1
        i += 1
    return list(zip(E, M, D))


def main():
    os.makedirs(os.path.join(HERE, "briefs"), exist_ok=True)
    plan = []
    rc_batches = [(c, b) for c in RC for b in RC[c][1]]
    sizes = [34] * len(rc_batches)
    q = alloc(CH_TARGET["RC"], sizes)
    for (c, (L, title, scope)), (e, m, d) in zip(rc_batches, q):
        tag = f"{c}-{L}"; fn = f"drafts/{c.lower()}_{L.lower()}.py"
        cmd = f"cd /home/claude/catvarc && python3 harness.py {fn} --sets 8 --q5 2 --easy {e} --medium {m} --difficult {d}"
        plan.append(dict(tag=tag, chapter=c, kind="RC", file=fn, cmd=cmd, n=34, sets=8, q5=2, E=e, M=m, D=d))
        open(os.path.join(HERE, "briefs", tag + ".md"), "w").write(f"""# Brief {tag}: Reading Comprehension, {RC[c][0]}: {title}

Chapter {c} of the CAT VARC bank: Reading Comprehension, domain {RC[c][0]}.

- Output file: `/home/claude/catvarc/{fn}`
- Passage ids `{tag}-01` ... `{tag}-08`; question ids `{tag}-01-1`, `{tag}-01-2`, ...
- Family prefix: `{c}{L}-` (one family per passage, naming its subject)
- passage topic field: exactly `{title}`. subtopic: one sentence stating what the passage argues.

## Quotas (exact)
- 8 passages: passages 01 to 06 have 4 questions each (400 to 580 words); passages 07 and 08 have
  5 questions each (570 to 730 words). Total 34 questions.
- Question difficulty: Easy {e}, Medium {m}, Difficult {d}.
- Passage difficulty: 2 Easy, 4 Medium, 2 Difficult (passage difficulty should broadly match its
  questions; a Difficult passage may still carry an Easy question).
- At least 7 of the 9 RC question types across the file; Inference the most common; Main idea at
  most once per passage. At least 3 "Strengthen / weaken / assumption" or "Application / analogy"
  questions in the file.

## Scope
{scope}
Choose 8 clearly different subjects inside this scope (not 8 angles on one subject) and claim
each one BEFORE writing it: `cd /home/claude/catvarc && python3 claim.py {tag} "<short subject>"`.
If it prints CLASH, pick another subject (do not just reword).

## Harness command
`{cmd}`
""")
    for c, (name, kind, total, nb) in VA.items():
        sizes = split(total, [1] * nb)
        q = alloc(CH_TARGET[c], sizes)
        fives = split(105, [1] * nb) if kind == "PJ" else [None] * nb
        for i, (sz, (e, m, d), f5) in enumerate(zip(sizes, q, fives)):
            L = "ABCDEFGHIJKLMNOP"[i]; tag = f"{c}-{L}"; fn = f"drafts/{c.lower()}_{L.lower()}.py"
            subj = [VA_SUBJECTS[(i * 5 + k) % len(VA_SUBJECTS)] for k in range(6)]
            cmd = f"cd /home/claude/catvarc && python3 harness.py {fn} --items {sz} --easy {e} --medium {m} --difficult {d}" + (f" --five {f5}" if f5 is not None else "")
            plan.append(dict(tag=tag, chapter=c, kind=kind, file=fn, cmd=cmd, n=sz, E=e, M=m, D=d, five=f5))
            fn_name = {"PJ": "pj", "PS": "ps", "OOO": "ooo", "SP": "sp"}[kind]
            extra = {
              "PJ": f"- {f5} of the {sz} jumbles have 5 sentences; the rest have 4.\n- At least 8 items whose order depends mainly on the logic of the idea rather than on pronouns or connectives alone.",
              "PS": "- Paragraph types varied: argument, explanation of a phenomenon, critique of a view, comparison, a finding and its qualification.\n- Option lengths within about 30% of each other in every item.",
              "OOO": "- In at least two thirds of the items the odd sentence shares the paragraph's subject and vocabulary and is rejected on function.",
              "SP": "- True gap spread exactly: as close to equal across (1), (2), (3), (4) as the count allows.\n- Vary the clue: backward reference, forward set-up, contrast marker, example after claim, conclusion.",
            }[kind]
            open(os.path.join(HERE, "briefs", tag + ".md"), "w").write(f"""# Brief {tag}: Verbal Ability, {name}

Chapter {c} of the CAT VARC bank: {name}. Use `{fn_name}(...)` for every item.

- Output file: `/home/claude/catvarc/{fn}`
- Local ids `{tag}-001` ... `{tag}-{sz:03d}`
- Family prefix: `{c}{L}-` (normally one family per item, naming its subject)
- topic field: one of {', '.join(subj)} (the subject area of the item, spread across them).
  subtopic: one line stating the point of the paragraph.

## Quotas (exact)
- {sz} items: Easy {e}, Medium {m}, Difficult {d}.
{extra}
- Every item on a different subject. Claim every subject BEFORE writing the item (you may claim
  several at once): `cd /home/claude/catvarc && python3 claim.py {tag} "<short subject>" ...`.
  If it prints CLASH, choose another subject (do not just reword). If you drop a claimed subject,
  release it with `python3 claim.py --release {tag} "<subject>"`.

## Harness command
`{cmd}`
""")
    json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    import collections
    tot = collections.Counter()
    for p in plan:
        tot["n"] += p["n"]; tot["E"] += p["E"]; tot["M"] += p["M"]; tot["D"] += p["D"]
    print(len(plan), "batches", dict(tot))


if __name__ == "__main__":
    main()
