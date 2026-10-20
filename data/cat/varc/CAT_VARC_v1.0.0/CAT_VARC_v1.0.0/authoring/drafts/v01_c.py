import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

HARD = ("CAT", "XAT")

# ------------------------------------------------------------------ 001 open-label placebos
pj("V01-C-001", "Health and medicine",
   "Placebos given openly, if they work, remove the ethical objection that placebos require deception.", "Easy",
   ["For decades, researchers assumed that a placebo could work only if the patient believed it to be a genuine drug.",
    "That assumption made the placebo ethically awkward, since using one in ordinary practice seemed to require deceiving the patient.",
    "In recent years, however, some trials have asked whether the deception is necessary at all, handing patients pills openly described as inert.",
    "If findings of relief among such patients hold up, the ethical objection loses much of its force, because a remedy offered honestly involves no deception."],
   "Sentence [[1]] states the old assumption and opens the paragraph. Sentence [[2]] begins 'That assumption' and draws its ethical cost, the need to deceive. Sentence [[3]] refers to 'the deception' just mentioned and introduces the open-label trials with 'however'. Sentence [[4]] speaks of 'such patients', those given openly inert pills in sentence [[3]], and concludes that the objection weakens.",
   "Placing sentence [[3]] straight after sentence [[1]] because 'however' seems to answer the assumption, which leaves 'the deception' in sentence [[3]] without anything to refer to.",
   "V01C-open-label-placebos",
   "A simple chain of reference words ('That assumption', 'the deception', 'such patients') fixes every link.",
   traps=[("1324", "Sentence [[3]] can seem to answer sentence [[1]] directly, but it speaks of 'the deception', which is first raised in sentence [[2]], and sentence [[2]] cannot follow the trials it would then be ignoring.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 002 disaster triage
pj("V01-C-002", "Health and medicine",
   "Disaster triage gives up treating the worst-hurt first because scarce care must go where it saves most lives.", "Medium",
   ["In ordinary emergency medicine, the patient in greatest danger is treated first, a rule so natural that it rarely needs defending.",
    "Disaster triage deliberately abandons that rule when casualties overwhelm the staff and supplies available.",
    "Under such conditions, an hour spent on a patient who will probably die anyway is an hour denied to several who could be saved with modest care.",
    "Triage officers therefore sort the injured by how much difference treatment will make, a practice that looks callous only until one counts everyone who is waiting."],
   "Sentence [[1]] sets out the ordinary rule. Sentence [[2]] says disaster triage 'abandons that rule' and names the condition, overwhelming casualties. Sentence [[3]] opens 'Under such conditions' and gives the reason the rule fails there. Sentence [[4]] draws the consequence with 'therefore' and defends the practice, so it closes the paragraph.",
   "Putting sentence [[4]] before sentence [[3]] because 'therefore' seems to follow from the abandonment of the rule, which leaves 'such conditions' in sentence [[3]] with no conditions to point to.",
   "V01C-disaster-triage",
   "The 'therefore' sentence is tempting right after the abandonment of the rule; the student must see that the reason has to come first and is tied to the 'conditions' just named.",
   traps=[("1243", "Sentence [[4]] seems to follow from sentence [[2]], but sentence [[3]] then opens 'Under such conditions' after a sentence about officers' sorting, which states no conditions, and the 'therefore' has no reason before it.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 003 hospital handwashing
pj("V01-C-003", "Health and medicine",
   "Early resistance to handwashing came less from arrogance than from the lack of any theory explaining why it worked.", "Easy",
   ["When a nineteenth-century physician urged his colleagues to wash their hands between the autopsy room and the maternity ward, many of them refused.",
    "Their resistance is usually told as a story of mere arrogance, but it had a more interesting source.",
    "No accepted theory of disease at the time explained how invisible matter on the hands could carry illness from a corpse to a mother.",
    "A remedy that worked without a reason struck them as a coincidence rather than a discovery, and only when germ theory supplied the mechanism did handwashing become common sense."],
   "Sentence [[1]] tells the episode. Sentence [[2]] refers to 'Their resistance' and promises 'a more interesting source'. Sentence [[3]] supplies that source, the absence of any theory. Sentence [[4]] depends on it: 'A remedy that worked without a reason' only makes sense once sentence [[3]] has said there was no reason available, and it ends with the later resolution.",
   "Reading sentence [[4]] as the source promised in sentence [[2]] and placing sentence [[3]] last, so that the explanation follows its own consequence.",
   "V01C-hospital-handwashing",
   "The order follows the logic of claim, cause and consequence, with only light reference cues.",
   traps=[("1243", "Sentence [[4]] speaks of 'A remedy that worked without a reason', which presupposes the missing theory of sentence [[3]]; putting sentence [[3]] last explains the doctors' attitude after the story has already ended."),
          ("1324", "Sentence [[2]] promises 'a more interesting source' for the resistance; if the missing theory of sentence [[3]] came first, that promise would point forward to an explanation already given.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 004 donor organ allocation
pj("V01-C-004", "Health and medicine",
   "Neither waiting time nor expected benefit alone is an acceptable rule for allocating organs, so practical schemes blend them.", "Medium",
   ["When a kidney becomes available, one way to choose among the many patients waiting is to give it to whoever has waited longest, a rule that is transparent and hard to manipulate.",
    "Yet waiting time ignores how well the organ will function in a particular body, so a strict queue can send a scarce kidney where it will fail within a few years.",
    "The opposite rule, allocating each organ to the patient expected to gain the most years from it, corrects this flaw but tends to favour the young and the otherwise healthy.",
    "Practical schemes therefore tend to blend the two principles, accepting some loss of efficiency to stay fair and some loss of simple fairness to avoid wasting organs."],
   "Sentence [[1]] poses the problem and offers the first rule, the queue. Sentence [[2]] objects to it with 'Yet waiting time'. Sentence [[3]] presents 'The opposite rule', which 'corrects this flaw', the flaw just named in sentence [[2]], and states its own cost. Sentence [[4]] concludes that schemes blend 'the two principles', so both must already be on the table.",
   "Placing sentence [[3]] directly after sentence [[1]] as the second option, which leaves 'this flaw' pointing to a rule whose flaw has not yet been stated.",
   "V01C-donor-organ-allocation",
   "The order follows the argument: rule, objection, the rival rule that answers the objection, then the compromise.",
   traps=[("1324", "Sentence [[3]] says the opposite rule 'corrects this flaw', but no flaw has been named until sentence [[2]]; and sentence [[2]] after sentence [[3]] would return to the queue after its rival has been offered.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 005 quarantine origins
pj("V01-C-005", "Health and medicine",
   "Quarantine worked even though those who devised it did not know how plague spread.", "Easy",
   ["The word quarantine comes from the Italian for forty days, the period that ships arriving from plague-stricken ports were once made to wait before landing.",
    "Nobody at the time knew how plague spread, and the figure of forty may have owed more to tradition than to any observation of the disease.",
    "Even so, the practice often worked, because a delay long enough for infected passengers to fall ill revealed the danger before it came ashore.",
    "Quarantine is thus an early case of a public health measure that succeeded for reasons its inventors could not have stated."],
   "Sentence [[1]] introduces the word and the practice. Sentence [[2]] adds that the forty days had no medical basis. Sentence [[3]] opens 'Even so', conceding that despite this ignorance the practice worked, and says why. Sentence [[4]] draws the general point with 'thus'.",
   "Placing sentence [[3]] before sentence [[2]], which leaves 'Even so' with nothing to concede against.",
   "V01C-quarantine-origins",
   "The 'Even so' concession and the concluding 'thus' make the order clear quickly.",
   traps=[("1324", "Sentence [[3]] needs the ignorance described in sentence [[2]] for 'Even so' to make sense; after sentence [[1]] there is nothing to concede.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 006 desire paths
pj("V01-C-006", "Cities and geography",
   "Desire paths, once treated as damage, can be read as evidence of where people want to walk.", "Easy",
   ["Walk through almost any public park and you will find bare strips of earth cutting across the lawns where no path was ever laid.",
    "Planners call these desire paths, and for a long time they treated them as damage to be fenced off or replanted.",
    "Some designers now take the opposite view, reading such tracks as a free survey of where people actually want to go.",
    "On this view, a new campus might open with no paved walks at all and be paved only after a season, along the lines its walkers have worn."],
   "Sentence [[1]] describes the bare strips. Sentence [[2]] names them with 'these desire paths' and gives the older attitude. Sentence [[3]] offers 'the opposite view', which needs the older attitude before it. Sentence [[4]] begins 'On this view' and applies the new view to a hypothetical campus.",
   "Opening with sentence [[2]] because it names the subject, though 'these' needs the strips described in sentence [[1]].",
   "V01C-desire-paths",
   "Reference words ('these', 'the opposite view', 'On this view') lock each pair.",
   traps=[("2134", "Sentence [[2]] names the subject but begins 'Planners call these', which has no referent until sentence [[1]] describes the strips of bare earth.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 007 street grid planning
pj("V01-C-007", "Cities and geography",
   "The street grid's indifference to particular uses lets a city change in ways winding streets resist.", "Medium",
   ["The rectangular street grid is often dismissed as the plan of a surveyor rather than a designer, monotonous and indifferent to the land beneath it.",
    "Its defenders reply that this indifference, far from being a weakness, is precisely its strength.",
    "Because every block resembles every other, no block is committed in advance to a particular use, and a district laid out for warehouses can later fill with flats or offices.",
    "Winding medieval streets, by contrast, were shaped around the markets, walls and landholdings of their own time, and they tend to resist uses their builders never imagined.",
    "Seen beside such streets, the grid looks less like a design for one city than a framework within which many cities can succeed one another."],
   "Sentence [[1]] states the common criticism. Sentence [[2]] turns 'this indifference' into a strength, and sentence [[3]] must come next because it explains why ('Because every block resembles every other'). Sentence [[4]] sets winding streets against the grid 'by contrast'. Sentence [[5]] refers to 'such streets', the winding ones, and so must follow sentence [[4]], closing with the general point.",
   "Ending with the contrast in sentence [[4]] and treating sentence [[5]] as the conclusion of the defence, which leaves 'such streets' in sentence [[5]] with no streets to refer to.",
   "V01C-street-grid-planning",
   "Students must see that the 'Because' sentence is the reason for the claimed strength and that the closing comparison depends on the contrast sentence; logic rather than pronouns places the reason.",
   traps=[("12354", "Sentence [[5]] cannot precede sentence [[4]]: 'Seen beside such streets' needs the winding streets that sentence [[4]] introduces."),
          ("12435", "Sentence [[4]] says 'by contrast', but nothing about how the grid works has yet been said for it to contrast with, and sentence [[3]] then explains the strength only after the comparison.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 008 delta subsidence
pj("V01-C-008", "Cities and geography",
   "Embankments that keep floods off deltas also starve them of the silt that kept them from sinking.", "Medium",
   ["River deltas are, in a sense, always sinking, as the soft sediment that forms them slowly compacts under its own weight.",
    "For most of their history this loss was made good by floods, which spread fresh silt across the land and raised it a little each season.",
    "Embankments built to keep those floods out of farms and towns have broken the cycle, so that much of the sediment now runs straight to the sea.",
    "Deprived of its yearly supply, the land goes on settling, and in places it now lies lower relative to the river than it did before the embankments were raised.",
    "The defences are thus caught in a loop of their own making: the more completely they keep the river out, the further the land behind them falls, and the higher they must be raised."],
   "Sentence [[1]] states the natural sinking. Sentence [[2]] calls it 'this loss' and explains how floods made it good. Sentence [[3]] refers to 'those floods' and says embankments broke the cycle. Sentence [[4]] follows from that: 'Deprived of its yearly supply', the land keeps sinking. Sentence [[5]] concludes with 'thus' that the defences create the danger they guard against.",
   "Placing sentence [[3]] before sentence [[2]] because embankments seem the natural topic after sinking, which leaves 'those floods' and 'the cycle' unexplained.",
   "V01C-delta-subsidence",
   "The chain follows a causal process (sinking, replenishment, interruption, consequence, feedback loop) that must be grasped as well as tracked through reference words.",
   traps=[("13245", "Sentence [[3]] refers to 'those floods' and 'the cycle', both introduced in sentence [[2]]; placed second it points to nothing.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 009 induced traffic demand
pj("V01-C-009", "Cities and geography",
   "Widening a congested road tends to create new traffic rather than relieve the old.", "Easy",
   ["When a congested road is widened, traffic usually flows faster for the first few months.",
    "The quicker journey, though, tempts people who had been travelling at other hours, by other routes or not at all.",
    "Within a few years the new lanes are often as crowded as the old ones were, carrying more cars at much the same speed.",
    "Widening a road, then, may do less to relieve congestion than to enlarge the amount of driving the road must carry."],
   "Sentence [[1]] states the first effect of widening. Sentence [[2]] refers to 'The quicker journey' of sentence [[1]] and adds the new drivers it attracts. Sentence [[3]] gives the result some years later. Sentence [[4]] concludes with 'then'.",
   "Placing sentence [[3]] before sentence [[2]], so that the new lanes fill up before anything has been said to explain why.",
   "V01C-induced-traffic-demand",
   "A short causal sequence with a clear opener and a 'then' conclusion.",
   traps=[("1324", "Sentence [[3]] reports the crowding before sentence [[2]] has introduced the new drivers who cause it, and sentence [[2]]'s 'quicker journey' would then follow a description of slow, crowded lanes.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 010 promises under changed circumstances
pj("V01-C-010", "Philosophy and ethics",
   "A promise broken for a weightier reason is outweighed rather than cancelled, which is why something is still owed.", "Medium",
   ["If you have promised to help a friend move house on Saturday and your child falls ill on Friday night, almost everyone agrees that you should stay at home.",
    "One view holds that the promise has simply lapsed, since every promise carries an unspoken condition that nothing serious intervenes.",
    "The difficulty with this view is that you still owe your friend something: an apology, an explanation, perhaps an offer to help another day.",
    "Such lingering debts suggest that the promise was outweighed rather than cancelled, and an outweighed obligation leaves a trace that a lapsed one would not."],
   "Sentence [[1]] sets up the case. Sentence [[2]] offers 'One view' of what happened to 'the promise'. Sentence [[3]] objects to 'this view'. Sentence [[4]] turns the objection's evidence, 'Such lingering debts', into the author's conclusion that the promise was outweighed.",
   "Placing sentence [[4]] before sentence [[3]] because both reject the lapse view, which leaves 'Such lingering debts' with no debts yet mentioned.",
   "V01C-promises-changed-circumstances",
   "The argument runs case, view, objection, conclusion; the conclusion can only be drawn from the debts listed in the objection.",
   traps=[("1243", "Sentence [[4]] rests on 'Such lingering debts', which are the apology and explanation listed in sentence [[3]]; before them the conclusion has no evidence.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 011 ship of Theseus
pj("V01-C-011", "Philosophy and ethics",
   "The rebuilt ship puzzle shows that our idea of sameness combines criteria that normally agree.", "Medium",
   ["If every plank of a ship is replaced one by one over many years, most people are content to say that it remains the same ship.",
    "Their confidence is shaken when they learn that someone has kept the discarded planks and assembled them, in the original arrangement, into a second vessel.",
    "Now two ships have a claim to the original's identity, one by continuity of form and use, the other by continuity of material.",
    "That the puzzle arises only when both claims are pressed at once suggests that our idea of sameness serves several purposes, which ordinarily coincide and only occasionally come apart."],
   "Sentence [[1]] gives the gradual replacement and the usual verdict. Sentence [[2]] refers to 'Their confidence' and introduces the reassembled planks. Sentence [[3]] says 'Now two ships' have a claim, which needs the second vessel of sentence [[2]]. Sentence [[4]] refers to 'both claims' of sentence [[3]] and draws the lesson.",
   "Opening with sentence [[3]] as a statement of the puzzle, though 'Now two ships' needs the second vessel to have been built first.",
   "V01C-ship-of-theseus",
   "The sequence of the thought experiment must be followed: verdict, complication, rival claims, lesson.",
   traps=[("1324", "Sentence [[3]] speaks of two ships before sentence [[2]] has built the second one, and sentence [[2]]'s 'Their confidence' would then follow a sentence that expresses no one's confidence.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 012 duty to rescue strangers
pj("V01-C-012", "Philosophy and ethics",
   "Resistance to a legal duty to rescue rests on the difficulty of setting its limits, not on denying the bystander's fault.", "Medium",
   ["Some legal systems impose no general duty to rescue a stranger, even when rescue would cost the bystander almost nothing.",
    "This strikes most people as morally perverse, since a passer-by who watches a child drown in shallow water seems plainly to have done wrong.",
    "Defenders of the rule reply that the law must draw lines it can enforce, and that a duty to rescue has no natural limit once the cost of helping is allowed to grow.",
    "Their worry, in other words, is not that the bystander is blameless but that a court cannot say how much he should have risked."],
   "Sentence [[1]] states the legal position. Sentence [[2]] calls 'This' perverse and gives the drowning child. Sentence [[3]] gives the defenders' reply. Sentence [[4]] restates 'Their worry, in other words', so it must follow the defenders' reply, and its point that the bystander is not blameless answers the moral intuition of sentence [[2]].",
   "Placing sentence [[4]] after sentence [[2]] and reading 'Their worry' as the worry of the people who find the rule perverse, which contradicts what those people think.",
   "V01C-duty-to-rescue",
   "The 'in other words' restatement must be matched to the right speaker; a careless reader attaches it to the wrong group.",
   traps=[("1243", "Sentence [[4]] says 'Their worry' is not that the bystander is blameless; that cannot describe the people of sentence [[2]], who think he plainly did wrong, so it must restate the defenders of sentence [[3]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 013 thought experiment intuitions
pj("V01-C-013", "Philosophy and ethics",
   "Intuitions about imagined cases, like perception, are fallible evidence that can be corrected, not worthless.", "Difficult",
   ["Philosophers often test a theory by imagining an unusual case and asking whether the theory's verdict on it seems right.",
    "Critics object that such verdicts are unreliable, since the same case can draw different responses when it is described in different words or put to different audiences.",
    "The objection proves less than it seems to, because ordinary perception is open to the same charge, and nobody concludes that we should stop trusting our eyes.",
    "What we do instead is learn the conditions under which sight misleads, and correct for them.",
    "A careful philosopher can treat intuitions in the same way, as evidence that is fallible in known ways rather than as an oracle or as mere noise."],
   "Sentence [[1]] describes the method. Sentence [[2]] states the critics' objection to 'such verdicts'. Sentence [[3]] answers 'The objection' with the analogy of perception. Sentence [[4]], 'What we do instead', continues the analogy: it describes what we do rather than stop trusting our eyes, so it must follow sentence [[3]] directly. Sentence [[5]] carries the lesson back to philosophy, 'in the same way', meaning the correction just described.",
   "Placing sentence [[5]] before sentence [[4]] because it seems to finish the reply to the critics, which leaves 'in the same way' without the method of correction it compares with, and strands sentence [[4]].",
   "V01C-thought-experiment-intuitions",
   "The last two sentences both develop the reply; only the logic of the analogy (what we do with sight, then the same for intuition) fixes their order, and the analogy must be followed across three sentences.",
   traps=[("12354", "Sentence [[5]] says philosophers can treat intuitions 'in the same way', but the way, learning when sight misleads and correcting for it, is only described in sentence [[4]]; and sentence [[4]]'s 'instead' must answer 'stop trusting our eyes' in sentence [[3]]."),
          ("13245", "Sentence [[3]] answers 'The objection', which does not exist until sentence [[2]] raises it.")],
   cognitive="Analysis", exams=HARD)

# ------------------------------------------------------------------ 014 eyewitness memory
pj("V01-C-014", "Psychology",
   "An eyewitness's confidence can be inflated by later feedback, so only the confidence first recorded should count.", "Medium",
   ["A confident eyewitness is among the most persuasive figures in a courtroom, and jurors tend to treat certainty as a sign of accuracy.",
    "The trouble is that confidence can grow after the event for reasons that have nothing to do with what was seen.",
    "A witness who picks a suspect from a line-up and is then told he chose correctly will often recall being surer than he was, so his later certainty reflects the encouragement as much as the glimpse.",
    "For this reason, some researchers argue that only the confidence a witness expresses at the first identification, before any feedback, deserves much weight."],
   "Sentence [[1]] describes how jurors trust certainty. Sentence [[2]] names 'The trouble', that confidence can grow later for irrelevant reasons. Sentence [[3]] gives the mechanism, feedback after a line-up. Sentence [[4]] draws the practical lesson 'For this reason', and its mention of feedback depends on the example in sentence [[3]].",
   "Placing sentence [[4]] straight after sentence [[2]] because it answers 'The trouble', which leaves 'before any feedback' referring to feedback not yet described.",
   "V01C-eyewitness-confidence",
   "The proposal must come after the mechanism it responds to, which requires noticing that 'feedback' is introduced only by the line-up example.",
   traps=[("1243", "Sentence [[4]] proposes ignoring confidence formed after 'any feedback', but feedback is only introduced in sentence [[3]]; and sentence [[3]] as the closer would end on an illustration rather than the conclusion it supports.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 015 learned helplessness
pj("V01-C-015", "Psychology",
   "A student who stops trying after repeated failure has drawn a reasonable conclusion, which only fresh experience can overturn.", "Medium",
   ["A student who fails repeatedly at a subject, whatever he does, may stop trying even when success later comes within reach.",
    "Teachers sometimes read this withdrawal as laziness, but it is closer to a reasonable conclusion drawn from experience.",
    "The conclusion is that effort makes no difference, and for this student, so far, it has been true.",
    "The remedy, accordingly, is not exhortation but a run of tasks in which effort visibly pays, so that the conclusion is overturned by fresh evidence rather than by argument."],
   "Sentence [[1]] describes the student who stops trying. Sentence [[2]] calls 'this withdrawal' a 'reasonable conclusion'. Sentence [[3]] states what 'The conclusion' is and why it is reasonable. Sentence [[4]] infers the remedy 'accordingly': if the conclusion was learned from evidence, new evidence must undo it.",
   "Placing sentence [[4]] before sentence [[3]] because a remedy seems to answer the teachers' misreading, which leaves the remedy's logic (overturning a conclusion with evidence) unexplained until afterwards.",
   "V01C-learned-helplessness-students",
   "The remedy follows from understanding why giving up is rational, so the order depends on the argument as well as on the repeated word 'conclusion'.",
   traps=[("1243", "Sentence [[4]] says the remedy follows 'accordingly' and aims to overturn 'the conclusion', but what that conclusion is, and why it is reasonable, is only stated in sentence [[3]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 016 uses of boredom
pj("V01-C-016", "Psychology",
   "Boredom is better seen as a signal worth heeding than as a defect to be relieved at once.", "Difficult",
   ["Boredom is usually treated as a defect of the situation, the mark of a lecture too slow or a task too repetitive.",
    "It may be better understood as a signal, much as pain is, telling us that what we are doing has stopped repaying the attention we give it.",
    "Seen this way, the habit of relieving every idle moment with a screen looks less like a cure than like taking painkillers for an injury one never examines.",
    "The discomfort is muffled, but the information it carried, that something in one's activity ought to change, goes unread.",
    "None of this makes boredom pleasant, or the screen an enemy; it suggests only that the urge to escape may be worth hearing out before it is silenced."],
   "Sentence [[1]] gives the usual view. Sentence [[2]] offers the alternative, boredom as a signal like pain; its 'It' needs boredom already named. Sentence [[3]] applies that view ('Seen this way') through the painkiller image, which depends on the comparison with pain. Sentence [[4]] completes the image: what the painkiller does is muffle the discomfort while its information goes unread. Sentence [[5]] qualifies the whole argument and mentions 'the screen', so it must come after sentence [[3]] and close the paragraph.",
   "Treating the concession in sentence [[5]] as a hinge between the theory and its application, or placing sentence [[4]] last, without seeing that sentence [[4]] continues the painkiller image directly.",
   "V01C-uses-of-boredom",
   "The middle of the paragraph is held together by an analogy (pain, painkillers, muffled discomfort) rather than by pronouns, and a concessive sentence that looks movable must be fixed by its reference to the screen.",
   traps=[("12354", "Sentence [[4]] would then follow a concession about not treating screens as enemies, but 'The discomfort is muffled' is the effect of the painkiller in sentence [[3]] and must continue that image; the concession belongs at the end, after the argument it qualifies."),
          ("21345", "Sentence [[2]] begins 'It may be better understood', which presupposes a subject and a prior understanding; only sentence [[1]] supplies both.")],
   cognitive="Analysis", exams=HARD)

# ------------------------------------------------------------------ 017 flow state
pj("V01-C-017", "Psychology",
   "Absorption in work depends on the match between skill and challenge, not on temperament.", "Easy",
   ["People often describe their best hours of work as times when they lost track of the clock and forgot themselves in the task.",
    "Psychologists who have studied such states find that they arise most readily when a task is hard enough to demand full attention but not so hard as to provoke anxiety.",
    "Too easy a task leaves room for the mind to wander, while too difficult a one fills it with worry about failure.",
    "Since each of these failures is a failure of fit, the absorption people prize is less a gift of temperament than a product of the match between their skill and the challenge before them."],
   "Sentence [[1]] describes the experience. Sentence [[2]] refers to 'such states' and gives the condition under which they arise. Sentence [[3]] spells out the two ways the balance fails, too easy and too hard. Sentence [[4]] refers to 'each of these failures', the two just described, and concludes that absorption depends on matching skill to challenge.",
   "Placing sentence [[3]] before sentence [[2]], so that 'Too easy' and 'too difficult' appear before the balance they depart from has been described.",
   "V01C-flow-state",
   "A straightforward sequence of experience, finding, elaboration and conclusion.",
   traps=[("1324", "Sentence [[3]] describes departures from a balance that sentence [[2]] has not yet stated, and sentence [[2]]'s 'such states' would then point back across an unrelated sentence."),
          ("1243", "Sentence [[4]] speaks of 'each of these failures', the too easy and too difficult tasks of sentence [[3]], so it cannot come before that sentence.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 018 museum labels
pj("V01-C-018", "Society and culture",
   "No museum label, brief or long, is neutral, so the honest course is to show that a choice has been made.", "Difficult",
   ["A museum label seems the most modest of texts, a few lines giving a name, a date and a material.",
    "Yet even this minimum involves a choice about what kind of thing the object is.",
    "A mask described only by its wood and its century is being presented as a sculpture to be looked at, rather than as an object that was once worn, danced in and perhaps feared.",
    "Adding a paragraph about its ceremonial use does not escape the difficulty, since that too selects one story about the mask from among several.",
    "If neither the bare label nor the long one is neutral, the honest course is not to search for neutrality but to let visitors see that a choice has been made."],
   "Sentence [[1]] describes the label as modest. Sentence [[2]] turns on it with 'Yet even this minimum'. Sentence [[3]] illustrates the choice with the mask. Sentence [[4]] considers the obvious remedy, a longer label, and refers to 'its ceremonial use', the mask's. Sentence [[5]] concludes from both cases, 'neither the bare label nor the long one', so it must come after sentence [[4]].",
   "Ending with sentence [[4]], reading it as a final twist, and placing sentence [[5]] after the mask example, which leaves 'the long one' in sentence [[5]] referring to a label not yet proposed.",
   "V01C-museum-labels",
   "The paragraph moves claim, example, rejected remedy, conclusion; the student must see that the conclusion depends on both the bare and the long label and that the remedy sentence answers the example.",
   traps=[("12354", "Sentence [[5]] concludes that 'neither the bare label nor the long one' is neutral, but the long label is first proposed and rejected in sentence [[4]], so the conclusion cannot precede it."),
          ("13245", "Sentence [[2]]'s 'this minimum' must refer to the few lines of sentence [[1]]; after the mask example it would have no clear referent, and the example would illustrate a claim not yet made.")],
   cognitive="Analysis", exams=HARD)

# ------------------------------------------------------------------ 019 cookbook measurement standards
pj("V01-C-019", "Society and culture",
   "Exact measures in recipes replaced not missing skill but the teacher who once stood beside the cook.", "Medium",
   ["Older recipes are often maddeningly vague, calling for a handful of flour, butter the size of an egg, or an oven that is moderately hot.",
    "Modern readers tend to see this vagueness as a failure of precision, which later cookbooks corrected with level cups, exact weights and oven temperatures.",
    "But the older writers were not failing at precision; they were addressing cooks who had learned by watching and could judge the feel of a dough better than any measure could describe it.",
    "Exact quantities became necessary only when such cooks gave way to readers who learned from books, with no one at their elbow to show them."],
   "Sentence [[1]] describes vague recipes. Sentence [[2]] gives the modern reading of 'this vagueness'. Sentence [[3]] answers that charge directly ('the older writers were not failing at precision') and explains whom they wrote for. Sentence [[4]] refers to 'such cooks', the ones who learned by watching, and says when precision became necessary.",
   "Placing sentence [[4]] right after sentence [[2]] because both concern exact measures, which leaves 'such cooks' without the cooks of sentence [[3]].",
   "V01C-cookbook-measurement",
   "Two sentences about precision look adjacent; the order depends on seeing that the explanation of the older readers must come before their replacement.",
   traps=[("1243", "Sentence [[4]] speaks of 'such cooks' giving way to book-learners, but the cooks who learned by watching are introduced only in sentence [[3]]."),
          ("1324", "Sentence [[3]] denies that the older writers were 'failing at precision', a charge first made in sentence [[2]]; directly after sentence [[1]] it rebuts an accusation nobody has yet made.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 020 decline of letter writing
pj("V01-C-020", "Society and culture",
   "What the decline of letters has cost is mainly a durable record, not depth of private feeling.", "Easy",
   ["It is often said that the decline of the handwritten letter has made our private lives shallower.",
    "Anyone who reads through an old family's correspondence, however, will find that most of the letters were dutiful reports of health, weather and the price of things.",
    "What has really been lost is not depth of feeling but a durable record, since letters were kept in drawers while much of what replaced them is deleted or never written down.",
    "It may be historians, then, rather than the people who once had to write them, who have most reason to miss the letters."],
   "Sentence [[1]] states the common view. Sentence [[2]] challenges it with 'however', showing that old letters were mostly routine. Sentence [[3]] says what 'has really been lost', a record. Sentence [[4]] concludes with 'then' that historians lose most, which depends on the point about records.",
   "Placing sentence [[4]] before sentence [[3]], so that historians are mentioned before the loss of a record explains why they would care.",
   "V01C-letter-writing-decline",
   "Clear opener, a 'however', and a conclusion that depends on the previous sentence.",
   traps=[("1243", "Sentence [[4]] says historians have most reason to miss letters, which only follows once sentence [[3]] has identified the loss as a durable record.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 021 public library lending
pj("V01-C-021", "Society and culture",
   "Free libraries create the readers on whom the book trade depends, even if some sales are lost.", "Medium",
   ["A familiar objection to free lending libraries is that nobody will buy a book that can be borrowed for nothing.",
    "The objection treats readers as a fixed population, each of whom will obtain a given book in one way or another.",
    "But readers are made, not found, and a child who grows up near a library is likely to become an adult who buys books as well as borrowing them.",
    "This reply does not settle every case, since a popular novel borrowed fifty times may indeed have cost its author several sales.",
    "Even so, a trade that depends on a reading public has reason to welcome the institution that does most to create one."],
   "Sentence [[1]] states the objection. Sentence [[2]] exposes its assumption, a fixed population of readers. Sentence [[3]] denies that assumption with 'But readers are made, not found'. Sentence [[4]] qualifies 'This reply'. Sentence [[5]] concludes 'Even so', overriding the qualification, and its point about creating a reading public echoes sentence [[3]].",
   "Ending with sentence [[4]] as a balanced close, which leaves 'Even so' in sentence [[5]] with no qualification to override.",
   "V01C-public-library-lending",
   "The argument runs objection, its hidden assumption, reply, concession, verdict; the assumption sentence must be placed by logic, since it could look like a second statement of the objection.",
   traps=[("12354", "Sentence [[5]] says 'Even so', which must answer a concession; the concession is sentence [[4]], so sentence [[5]] cannot precede it."),
          ("13245", "Sentence [[3]]'s 'But readers are made, not found' answers the idea of a fixed population, which is stated only in sentence [[2]]; after sentence [[1]] the contrast is weaker, and 'The objection' in sentence [[2]] would then follow the reply.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 022 salt taxation
pj("V01-C-022", "History and politics",
   "The features that made salt easy to tax also made the tax a lasting grievance.", "Medium",
   ["Salt was once among the most reliable things a government could tax.",
    "Everyone needed it, rich and poor alike, and in many regions it could be produced only at a few coastal pans or mines that officials could easily watch.",
    "These same features, however, made the tax unusually resented, since it fell hardest on the poor, who spent a larger share of their income on necessities.",
    "Salt duties thus became a recurring grievance in popular protest, precisely because they were so efficient at raising money."],
   "Sentence [[1]] makes the claim that salt was easy to tax. Sentence [[2]] gives the reasons, universal need and few production sites. Sentence [[3]] refers to 'These same features' and turns them against the tax. Sentence [[4]] concludes with 'thus' that efficiency and grievance went together.",
   "Opening with sentence [[2]] because it seems to introduce salt, though 'it' needs the subject named in sentence [[1]] and the reasons need a claim to support.",
   "V01C-salt-taxation",
   "The paradox at the end (resented because efficient) only works if the reasons for efficiency come before their turn into a grievance.",
   traps=[("2134", "Sentence [[2]] begins 'Everyone needed it' with no noun for 'it' to refer to; sentence [[1]] must name salt and make the claim that sentence [[2]] supports.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 023 term limits
pj("V01-C-023", "History and politics",
   "Whether term limits are worth their costs depends on how unequal elections actually are.", "Difficult",
   ["Term limits are usually defended as a check on entrenched power, a way of ensuring that no officeholder grows too comfortable to be removed.",
    "The argument assumes that voters, left to themselves, will not reliably remove a leader who has outstayed his usefulness.",
    "The assumption is not as insulting as it sounds: voters may be sensible and still face an incumbent with advantages in money, publicity and patronage that no challenger can match.",
    "Even so, a limit removes the competent along with the complacent, and it hands the last years of every final term to a leader who no longer needs anyone's approval.",
    "Whether the trade is worth making depends less on any principle than on how unequal elections in a given country actually are."],
   "Sentence [[1]] states the usual defence. Sentence [[2]] identifies 'The argument' and its assumption about voters. Sentence [[3]] defends 'The assumption', so it supports the case for limits. Sentence [[4]] answers with 'Even so', setting out the costs. Sentence [[5]] weighs 'the trade' between the benefit and these costs and ties it to the inequality of elections that sentence [[3]] described.",
   "Placing sentence [[4]] before sentence [[3]] because 'Even so' seems to answer the assumption, which then leaves 'The assumption' in sentence [[3]] referring back across the costs, and gives 'Even so' nothing conceded to push against.",
   "V01C-term-limits",
   "Both the concession and the counter-argument could seem to follow the assumption; only the direction of the argument (defence of the assumption, then the costs despite it) fixes the order, and the close links back to the earlier point about unequal contests.",
   traps=[("12435", "Sentence [[4]]'s 'Even so' needs a point in favour of limits to push against; that point is sentence [[3]]'s defence of the assumption, and sentence [[3]] after sentence [[4]] would revive the case for limits after its costs have been stated, breaking the run into the final weighing."),
          ("13245", "Sentence [[3]] refers to 'The assumption', which is first stated in sentence [[2]]; directly after sentence [[1]] it has no referent.")],
   cognitive="Analysis", exams=HARD)

# ------------------------------------------------------------------ 024 roman road networks
pj("V01-C-024", "History and politics",
   "Roads built for military control went on to shape the economic geography of a continent.", "Easy",
   ["The roads the Romans built across their empire were laid out chiefly for the rapid movement of soldiers, not for the convenience of traders.",
    "Once built, however, they served everyone who could use them, and merchants, officials and letters travelled along them as readily as legions.",
    "Towns grew up at their junctions and river crossings, and some of these places are still inhabited where the old routes met.",
    "A network designed to hold territory by force thus ended by shaping the economic life of a continent long after the force was gone."],
   "Sentence [[1]] states the military purpose of the roads. Sentence [[2]] turns with 'however' to their wider use. Sentence [[3]] adds the growth of towns at 'their junctions'. Sentence [[4]] concludes with 'thus', contrasting the military design with the lasting economic result.",
   "Placing sentence [[3]] before sentence [[2]], so that towns grow along the roads before the roads have been opened to traders and travellers.",
   "V01C-roman-road-networks",
   "A plain chronological and causal sequence with a 'however' and a 'thus'.",
   traps=[("1324", "Sentence [[2]]'s 'Once built, however' must turn directly from the military purpose of sentence [[1]]; placed after the towns of sentence [[3]] it would announce a change that has already been described.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 025 mercenary armies
pj("V01-C-025", "History and politics",
   "Rulers hired soldiers because citizen armies were politically dangerous; the real risk of hired troops was running out of money.", "Difficult",
   ["Political writers have long warned against hiring soldiers, arguing that men who fight for pay will desert the moment a battle turns against them.",
    "Yet rulers went on hiring them regardless, and they did so not only out of necessity.",
    "An army of armed citizens could turn its weapons on the government that raised it, whereas a hired company had no stake in local quarrels.",
    "Its loyalty was narrow but predictable: it served whoever paid, for as long as he paid.",
    "The real danger, then, lay less on the battlefield than in the treasury, since a ruler who ran out of money might find his own unpaid soldiers camped outside his gates."],
   "Sentence [[1]] states the traditional warning. Sentence [[2]] turns with 'Yet' and hints at a reason beyond necessity. Sentence [[3]] gives that reason, the political danger of citizen armies. Sentence [[4]] describes 'Its loyalty', that of the hired company just mentioned. Sentence [[5]] draws the conclusion with 'then': since loyalty lasted only as long as pay, the danger lay in the treasury, which answers the battlefield worry of sentence [[1]].",
   "Taking sentence [[4]] as the direct reply to the warning about desertion and placing it before sentence [[3]], which leaves 'Its loyalty' without the singular 'hired company' it refers to.",
   "V01C-mercenary-armies",
   "The reply to the opening warning is indirect: the student must see that the political reason comes before the description of loyalty and that the conclusion relocates the danger from battle to treasury.",
   traps=[("12435", "Sentence [[4]]'s 'Its loyalty' needs a singular antecedent; 'them' in sentence [[2]] is plural, and only 'a hired company' in sentence [[3]] fits."),
          ("13245", "Sentence [[2]]'s 'Yet rulers went on hiring them' must turn against the warning of sentence [[1]] directly; after sentence [[3]] has already given the reason rulers hired soldiers, 'not only out of necessity' would come too late.")],
   cognitive="Analysis", exams=HARD)
