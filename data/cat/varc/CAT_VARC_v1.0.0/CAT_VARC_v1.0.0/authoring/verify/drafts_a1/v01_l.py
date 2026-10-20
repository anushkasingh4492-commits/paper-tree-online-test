import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

AN = "Arts and literature"
LM = "Language and media"
ED = "Education"
HM = "Health and medicine"
CG = "Cities and geography"
PE = "Philosophy and ethics"
HARD = ("CAT", "XAT")

pj("V01-L-001", AN, "Letters in an epistolary novel seem to offer direct access to a mind but are always shaped for a reader.", "Medium",
   ["A novel told entirely in letters seems, at first, to offer the most direct access a reader could want to a character's private thoughts.",
    "Each letter is written in the heat of the moment, before its writer knows how events will turn out.",
    "Yet that very spontaneity carries a hidden constraint, because every letter is addressed to someone and is shaped for that person's eyes.",
    "What looks like a window into the heart is therefore always partly a performance, and the attentive reader learns to read between the lines."],
   "Sentence [[1]] introduces the novel in letters and its apparent directness. Sentence [[2]] supports that impression: 'Each letter' refers back to the letters of [[1]], and writing 'in the heat of the moment' explains the sense of directness. Sentence [[3]] turns with 'Yet that very spontaneity', which needs the spontaneity of writing 'in the heat of the moment' described in [[2]]; the 'direct access' of [[1]] is a reader's impression, not the writer's spontaneity. Sentence [[4]] draws the conclusion ('therefore') that the letter is partly a performance, which follows only from the constraint in [[3]].",
   "Placing sentence [[3]] straight after sentence [[1]], so that the objection arrives before the spontaneity it turns against has been described.",
   "V01L-epistolary-novel", "The supporting sentence about writing in the moment must precede 'that very spontaneity', and the conclusion needs the constraint before it; one step of inference beyond pronoun matching.",
   traps=[("1342", "Here sentence [[2]] is left stranded at the end, after the conclusion; its point about writing in the moment supports the first impression and cannot follow the verdict of sentence [[4]]."),
          ("1324", "Sentence [[3]] needs a spontaneity already described, and that description is in sentence [[2]]; placing [[2]] after [[3]] also separates the constraint from the 'therefore' of sentence [[4]].")],
   cognitive="Understanding")

pj("V01-L-002", AN, "Invented ruins in eighteenth-century landscapes offered a mood of pleasurable decay rather than a lesson in history.", "Difficult",
   ["Painters of the eighteenth century often placed a crumbling temple or a broken arch in the corner of an otherwise ordinary pastoral scene.",
    "The usual explanation is that such ruins invited the viewer to reflect on the grandeur of lost civilisations.",
    "Many of the ruins in these pictures, however, belong to no identifiable building, and some were simply invented by the painter.",
    "A ruin that commemorates nothing in particular can hardly be a lesson in history, so its appeal must lie elsewhere.",
    "The real attraction, it seems, was the chance to contemplate decay from a safe distance, as a mood to be savoured rather than a loss to be mourned."],
   "Sentence [[1]] sets the scene with the painted ruins. Sentence [[2]] gives 'The usual explanation' of 'such ruins', so it needs [[1]]. Sentence [[3]] objects with 'however': the ruins often depict no real building. Sentence [[4]] infers from that objection that a ruin commemorating nothing cannot teach history, and so its appeal 'must lie elsewhere'. Only then can sentence [[5]] name 'The real attraction'. Reversing the last two would have the paragraph name the attraction and then announce that it must lie somewhere not yet found.",
   "Putting sentence [[5]] before sentence [[4]] because both concern the true appeal, which makes [[4]] announce as an open question something already answered.",
   "V01L-ruins-in-landscape-painting", "Order depends mainly on the logic of the idea: the last two sentences have no pronoun lock, and the solver must see that 'must lie elsewhere' is a step that precedes naming the real attraction.",
   traps=[("12354", "Sentence [[5]] names the real attraction, so sentence [[4]] saying the appeal 'must lie elsewhere' would come after the question is already settled; the inference must precede the answer."),
          ("13245", "Sentence [[3]] objects to an explanation with 'however', but placed second it has no explanation to object to; the usual view in sentence [[2]] must come first.")],
   exams=HARD)

pj("V01-L-003", AN, "Dutch vanitas still lifes turn a display of plenty into a reminder of mortality.", "Easy",
   ["Many Dutch still-life paintings of the seventeenth century look, at first glance, like simple celebrations of wealth and plenty.",
    "Their tables are crowded with polished silver, imported fruit and glasses of wine catching the light.",
    "Look closer, however, and the same tables hold a skull, a guttering candle or a watch lying open beside the fruit.",
    "These objects turn the display into a warning, reminding the viewer that such abundance cannot outlast the person who enjoys it."],
   "Sentence [[1]] introduces the paintings and their first impression. Sentence [[2]] describes 'Their tables', the evidence of plenty. Sentence [[3]] turns with 'Look closer, however' and 'the same tables', which need the tables of [[2]]. Sentence [[4]] explains what 'These objects', the skull, candle and watch of [[3]], do to the meaning of the picture.",
   "Reading sentence [[3]] before sentence [[2]], although 'the same tables' only makes sense once the tables have been described.",
   "V01L-still-life-vanitas", "Clear opener and reference words ('Their tables', 'the same tables', 'These objects') fix every link.",
   traps=[("1324", "Sentence [[3]] speaks of 'the same tables', which have not yet been described if it comes before sentence [[2]], and 'These objects' in sentence [[4]] would then point to silver and fruit instead of the skull and candle.")],
   cognitive="Understanding")

pj("V01-L-004", AN, "The chorus in Greek tragedy, often thought an interruption, models how citizens should respond to events.", "Medium",
   ["Modern readers of ancient Greek tragedy often find the chorus an awkward presence, a crowd of onlookers who comment at length but rarely act.",
    "To an audience used to realistic drama, its long songs seem to halt the story just when it should be gathering speed.",
    "That pause, however, may be the point, for the chorus models how ordinary citizens might respond to events too large for any one of them to control.",
    "Seen this way, the chorus is less an interruption of the tragedy than a guide to how the tragedy should be received."],
   "Sentence [[1]] states the modern complaint about the chorus. Sentence [[2]] develops it: the songs 'seem to halt the story'. Sentence [[3]] reinterprets 'That pause', which refers to the halting described in [[2]], as purposeful. Sentence [[4]] sums up the reinterpretation ('Seen this way'): the chorus is a guide rather than an interruption, which depends on the purpose given in [[3]].",
   "Starting with sentence [[4]] because it sounds like a thesis, though 'Seen this way' requires a way of seeing already offered.",
   "V01L-tragic-chorus", "Order depends mainly on the logic of the idea: complaint, its development, reinterpretation and verdict; the verdict cannot open because it answers the complaint.",
   traps=[("4123", "Sentence [[4]] begins 'Seen this way', which needs the reinterpretation in sentence [[3]]; it cannot open the paragraph."),
          ("1324", "Sentence [[3]] refers to 'That pause', and the halting of the story that creates the pause is described only in sentence [[2]].")])

pj("V01-L-005", LM, "Children who grow up with a pidgin turn it into a full creole, showing that they impose structure on language.", "Medium",
   ["When people with no shared language must trade or work together, they often improvise a simplified tongue known as a pidgin.",
    "A pidgin has a small vocabulary and few fixed rules, and nobody speaks it as a mother tongue.",
    "Something remarkable can happen, though, when children grow up hearing a pidgin as the main language of their community.",
    "Within a generation or two, those children may regularise its grammar and enlarge its vocabulary, turning it into a full language called a creole.",
    "The change suggests that children do not merely copy the language around them but actively impose structure on it."],
   "Sentence [[1]] defines the pidgin and how it arises. Sentence [[2]] describes its limits, including that 'nobody speaks it as a mother tongue'. Sentence [[3]] contrasts ('though') with exactly that limit: children who grow up hearing it. Sentence [[4]] says what 'those children' do, turning the pidgin into a creole. Sentence [[5]] draws the general conclusion from 'The change'.",
   "Putting sentence [[5]] immediately after sentence [[3]], so that a conclusion about what children do is drawn before anything they do has been described.",
   "V01L-pidgin-to-creole", "Order depends mainly on the logic of the idea: definition, limitation, the contrasting circumstance, the transformation and the inference drawn from it.",
   traps=[("13245", "Sentence [[3]] contrasts with the fact that nobody grows up speaking a pidgin, so the description of the pidgin's limits in sentence [[2]] must come before it."),
          ("12354", "Sentence [[5]] interprets 'The change', which is described only in sentence [[4]]; the inference cannot precede the evidence.")])

pj("V01-L-006", LM, "The footnote lets readers verify a claim rather than simply trust the author.", "Easy",
   ["The footnote is often mocked as a sign of academic fussiness, a place where scholars bury their trivial disputes.",
    "Yet its main purpose is a simple one: to show readers exactly where a claim comes from.",
    "With that information, a sceptical reader can go to the original source and check whether it says what the author claims.",
    "In this sense, the humble footnote turns an argument from a request for trust into an invitation to verify."],
   "Sentence [[1]] introduces the footnote and the mockery it attracts. Sentence [[2]] answers with 'Yet its main purpose', where 'its' is the footnote of [[1]]. Sentence [[3]] uses 'that information', the source identified in [[2]], to explain what a reader can do. Sentence [[4]] concludes 'In this sense' that the footnote invites verification, which rests on the checking described in [[3]].",
   "Ending with sentence [[3]] after sentence [[4]], although 'that information' must sit next to the purpose stated in sentence [[2]].",
   "V01L-scholarly-footnotes", "A clear opener and direct reference words ('its', 'that information', 'In this sense') fix the order.",
   traps=[("1243", "Sentence [[4]] says 'In this sense', meaning the sense in which a reader can check the source; that checking is described in sentence [[3]], which must come first.")],
   cognitive="Understanding")

pj("V01-L-007", LM, "Indirect requests are not idle detours: the question form lets a request be granted as a favour.", "Difficult",
   ["It is tempting to treat indirect requests, such as asking whether someone could open a window, as pointless detours around a plain command.",
    "After all, no listener seriously takes such a question as an inquiry into their physical abilities.",
    "But the form of a question leaves the listener formally free to say no, which a command does not.",
    "That freedom matters even when it is never used, because it lets the request be granted as a favour rather than extracted as obedience."],
   "Sentence [[1]] states the tempting view that indirect requests are pointless. Sentence [[2]] supports that view ('After all'): everyone understands the real request. Sentence [[3]] replies ('But') that the question form leaves the listener free to refuse. Sentence [[4]] explains why 'That freedom' matters 'even when it is never used', a phrase that answers the point of [[2]] that nobody is really confused.",
   "Reading sentence [[2]] as support for the reply in sentence [[3]], and so placing it after [[3]].",
   "V01L-indirect-requests", "Order depends mainly on the logic of the idea: the solver must see that the 'After all' sentence supports the dismissive view, not the reply, and that 'even when it is never used' presupposes it.",
   traps=[("1324", "Sentence [[2]] backs the dismissive view of sentence [[1]], not the reply; placed after sentence [[3]] it undercuts the reply, and it also separates 'That freedom' in sentence [[4]] from the freedom named in [[3]]."),
          ("1342", "Ending with sentence [[2]] reopens the dismissive view after the paragraph has answered it, and 'After all' would then appear to support the conclusion it opposes.")],
   exams=HARD)

pj("V01-L-008", LM, "The passive voice survives in lab reports because it puts the repeatable procedure ahead of the person.", "Medium",
   ["Style guides have long urged scientists to abandon the passive voice in favour of livelier sentences that say who did what.",
    "The advice has merit, since a paper full of phrases like 'it was observed that' can be tiring to read.",
    "Still, the passive survives in laboratory reports for a reason: it keeps attention on the procedure rather than on the person who carried it out.",
    "A method is meant to be repeatable by anyone, and a grammar that leaves the experimenter unnamed quietly makes that point."],
   "Sentence [[1]] states the advice of style guides. Sentence [[2]] concedes that 'The advice has merit'. Sentence [[3]] turns with 'Still': the passive persists for a reason, keeping attention on the procedure. Sentence [[4]] explains why that focus matters, since a method should be repeatable by anyone, and so must follow [[3]].",
   "Placing sentence [[4]] before sentence [[3]] because it states a general principle, though its 'grammar that leaves the experimenter unnamed' presupposes the reason given in [[3]].",
   "V01L-passive-voice-science", "Concession then counter-claim then justification; the final sentence elaborates the reason in the third and cannot stand before it.",
   traps=[("1243", "Sentence [[4]] presents the unnamed experimenter as making a point, but the link between the passive and the procedure is first made in sentence [[3]]; and 'Still' in [[3]] needs the concession of sentence [[2]] directly before it.")])

pj("V01-L-009", ED, "Cramming feels effective but spaced review produces more lasting learning.", "Easy",
   ["Students preparing for an examination often cram, reviewing the same material many times in a single long session.",
    "Cramming can feel productive, because the material seems familiar by the end of the evening.",
    "That familiarity fades quickly, however, and much of what was crammed is gone within a few weeks.",
    "Spreading the same hours of review across several days produces far more durable learning, even though it feels harder at the time."],
   "Sentence [[1]] introduces cramming. Sentence [[2]] explains why it feels productive: the material seems 'familiar'. Sentence [[3]] says 'That familiarity fades quickly', referring to [[2]]. Sentence [[4]] offers the alternative, spaced review, which the shortcomings in [[3]] motivate.",
   "Placing sentence [[4]] second because it names the better method, which leaves 'That familiarity' in sentence [[3]] without its referent.",
   "V01L-spacing-effect", "Simple problem and solution sequence with a reference word ('That familiarity').",
   traps=[("1423", "Sentence [[4]] offers the remedy before the problem has been shown, and sentence [[3]] then has to refer back past it to the familiarity mentioned in sentence [[2]].")],
   cognitive="Understanding")

pj("V01-L-010", ED, "Rubrics make marking consistent but can penalise originality as students write to the list.", "Difficult",
   ["Detailed marking rubrics were introduced in many schools to make the grading of essays fairer and more consistent.",
    "By spelling out in advance what earns each mark, such rubrics reduce the weight of any single teacher's personal taste.",
    "Students, being sensible, soon learn to write towards the rubric, ticking off each listed feature in turn.",
    "Their essays grow more uniform, and the rare piece that succeeds by doing something unlisted risks being marked down.",
    "The fairness the rubric was meant to secure is thus purchased by penalising exactly the originality that good writing often needs."],
   "Sentence [[1]] states the purpose of rubrics. Sentence [[2]] explains how 'such rubrics' serve it, by limiting individual taste, so it must follow [[1]]. Sentence [[3]] describes the students' response, writing towards the rubric, and sentence [[4]] its effect ('Their essays'): uniformity, and penalties for the unlisted. Sentence [[5]] concludes with 'thus' that fairness is 'purchased by penalising' originality, which depends on the marking down described in [[4]].",
   "Placing sentence [[5]] third as a thesis, although its 'thus' and 'penalising' depend on the consequence described in sentence [[4]].",
   "V01L-rubric-marking", "Order depends mainly on the logic of the idea: purpose, mechanism, response, effect, verdict; few pronouns help, and the verdict is tempting as an early thesis.",
   traps=[("12534", "Sentence [[5]] says the fairness is 'thus' bought by penalising originality, but at that point no penalty has been described; the marking down appears only in sentence [[4]]."),
          ("13245", "Sentence [[2]] explains how rubrics achieve fairness and belongs with the purpose in sentence [[1]]; placed after the students' response it breaks the cause and effect running from sentence [[3]] to [[4]].")],
   exams=HARD)

pj("V01-L-011", ED, "Recipe-style school practicals teach pupils to reproduce known answers, the reverse of real inquiry.", "Medium",
   ["School science practicals are usually defended as a way of teaching pupils how scientists actually find things out.",
    "In many classrooms, though, the practical arrives as a worksheet listing the apparatus, the steps and even the result that should be obtained.",
    "Pupils who follow such a recipe learn to reproduce an answer already known, and a reading that deviates from it is treated as a mistake.",
    "Real inquiry runs the other way, for it is precisely the unexpected reading that a scientist would stop to investigate."],
   "Sentence [[1]] states the usual defence of practicals. Sentence [[2]] contrasts ('though') with how they are actually run. Sentence [[3]] describes the effect of 'such a recipe', the worksheet of [[2]], including that a deviating reading counts as a mistake. Sentence [[4]] says real inquiry 'runs the other way', which only makes sense against the treatment of deviation in [[3]].",
   "Reading sentence [[4]] as a natural second sentence because it describes real science, although 'the other way' needs the contrary practice described in sentence [[3]].",
   "V01L-school-science-practicals", "Order depends mainly on the logic of the idea: the closing contrast hinges on the treatment of an unexpected reading.",
   traps=[("1423", "After sentence [[1]], sentence [[4]] would say real inquiry runs 'the other way' from the defence of practicals, which is the reverse of the point; it contrasts with the recipe practice described in sentence [[3]].")])

pj("V01-L-012", ED, "A longer pause after a teacher's question lets more pupils think and answer.", "Easy",
   ["When a teacher asks the class a question, the pause before someone is called on, or before the teacher answers, is often very short.",
    "Such a brief pause rewards the quickest pupils and gives the others little reason to think at all.",
    "If the teacher instead waits several seconds in silence, more pupils attempt an answer, and their answers tend to be fuller.",
    "The silence that feels awkward to the teacher is, for the class, the time in which thinking actually happens."],
   "Sentence [[1]] introduces the short pause. Sentence [[2]] refers to 'Such a brief pause' and its effect. Sentence [[3]] offers the alternative ('instead') of waiting in silence. Sentence [[4]] interprets 'The silence' of [[3]] as the time in which thinking happens.",
   "Placing sentence [[3]] second, which leaves 'Such a brief pause' in sentence [[2]] after the longer wait has already been described.",
   "V01L-teacher-wait-time", "Reference words ('Such a brief pause', 'instead', 'The silence') fix the order.",
   traps=[("1324", "With sentence [[3]] second, sentence [[2]] then returns to the brief pause after the remedy has been proposed, and 'The silence' in sentence [[4]] is separated from the silence it refers to.")],
   cognitive="Understanding")

pj("V01-L-013", HM, "Pain scores are useful for tracking one patient over time, not for comparing patients.", "Medium",
   ["Hospitals commonly ask patients to rate their pain on a scale from zero to ten.",
    "The number is easy to record and compare, which is why it has become a routine part of clinical charts.",
    "But two patients who both say 'seven' may mean very different things, since each anchors the scale to the worst pain they have personally known.",
    "The score is therefore most useful for tracking change in one patient over time, not for comparing one patient with another."],
   "Sentence [[1]] introduces the pain scale. Sentence [[2]] gives its appeal: 'The number' is easy to record and compare. Sentence [[3]] objects with 'But': the same number can mean different things to different patients. Sentence [[4]] concludes ('therefore') where the score is useful, which follows from the objection in [[3]] and limits the claim about comparison in [[2]].",
   "Putting sentence [[3]] before sentence [[2]], which makes 'But' contrast with the bare description of the scale instead of with its supposed comparability.",
   "V01L-pain-rating-scales", "Order depends mainly on the logic of the idea: the conclusion narrows the use of the score, which needs both the claimed comparability and the objection to it.",
   traps=[("1324", "Sentence [[3]] objects to comparing patients, and that only makes sense once sentence [[2]] has claimed the number is easy to compare; placed after [[3]], sentence [[2]] also breaks the 'therefore' link to sentence [[4]].")])

pj("V01-L-014", HM, "Bed rest after surgery was replaced by early walking once its dangers became clear.", "Easy",
   ["For much of the last century, patients recovering from major surgery were told to stay in bed for many days.",
    "Rest seemed the obvious way to let wounds heal and to spare a weakened body any strain.",
    "Prolonged bed rest, however, turned out to carry dangers of its own, including blood clots, weakened muscles and chest infections.",
    "Today, many patients are encouraged to get up and walk within a day or so of their operation."],
   "Sentence [[1]] describes the old practice. Sentence [[2]] gives the reasoning behind it. Sentence [[3]] reverses that reasoning with 'however': bed rest had dangers. Sentence [[4]] describes the present practice ('Today'), which the dangers in [[3]] explain.",
   "Placing sentence [[4]] second because it contrasts with sentence [[1]], which leaves the dangers of bed rest unexplained until after the change.",
   "V01L-early-walking-after-surgery", "Chronology (last century, today) and 'however' make the order clear.",
   traps=[("1423", "Jumping to 'Today' in sentence [[4]] straight after sentence [[1]] skips the reasoning and the discovery that explain the change; sentences [[2]] and [[3]] would then dangle after the conclusion.")],
   cognitive="Understanding")

pj("V01-L-015", HM, "Variolation protected against smallpox at real risk and was abandoned once cowpox inoculation offered the same protection.", "Medium",
   ["Long before vaccines existed, people in several parts of the world protected themselves against smallpox by a riskier practice called variolation.",
    "Material from a smallpox sore was deliberately introduced into a small cut in a healthy person's skin.",
    "The resulting illness was usually milder than smallpox caught in the ordinary way, and those who recovered were protected against the disease.",
    "Yet some of those treated died, and others passed the full disease to the people around them.",
    "When inoculation with the far milder cowpox was found to give the same protection, variolation was gradually abandoned."],
   "Sentence [[1]] names variolation. Sentence [[2]] describes the procedure. Sentence [[3]] gives 'The resulting illness', which needs the procedure of [[2]], and its benefit. Sentence [[4]] sets the risks against the benefit with 'Yet'. Sentence [[5]] explains why the practice ended: a safer method, which the risks in [[4]] make decisive.",
   "Placing sentence [[4]] before sentence [[3]], although 'Yet' must contrast with the benefit, and the illness it concerns has not yet been described.",
   "V01L-variolation-history", "Order depends mainly on the logic of the idea: procedure, benefit, cost and replacement; the replacement makes sense only after the cost.",
   traps=[("12435", "Sentence [[4]] begins 'Yet', which needs a benefit to set against; placed before sentence [[3]] it follows only the procedure, and the risks appear before any reason for running them."),
          ("12354", "Ending with the risks in sentence [[4]] after the practice has been abandoned leaves the abandonment unexplained and makes 'Yet' contrast with the arrival of a better method.")])

pj("V01-L-016", HM, "The danger of many prescriptions for an elderly patient lies in nobody overseeing the whole list.", "Difficult",
   ["An elderly patient who sees several specialists often leaves each appointment with one more prescription.",
    "Each of these prescriptions, considered by itself, may be entirely appropriate to the condition it was written for.",
    "Taken together, however, the medicines can interact, and a side effect of one may be mistaken for a new illness and treated with yet another drug.",
    "No single doctor need be at fault, and the danger therefore lies in the absence of anyone whose job is to look at the whole list."],
   "Sentence [[1]] sets up the situation: several specialists, one more prescription each. Sentence [[2]] grants that 'Each of these prescriptions, considered by itself' may be sound, and 'these' ties it to [[1]]. Sentence [[3]] turns with 'Taken together, however', a contrast that needs the 'by itself' of [[2]]. Sentence [[4]] concludes that no doctor need be at fault, since each acted soundly as [[2]] says, and that the danger lies in the missing overview, the harm of the combination described in [[3]].",
   "Placing sentence [[3]] directly after sentence [[1]] because both concern several medicines, which leaves 'however' with no favourable judgement to contrast with.",
   "V01L-polypharmacy-elderly", "Order depends mainly on the logic of the idea: the mandatory pair is 'considered by itself' followed by 'Taken together', and the conclusion draws on both halves of that contrast.",
   traps=[("1324", "Sentence [[1]] is neutral, so 'Taken together, however' in sentence [[3]] has nothing favourable to turn against; the contrast is with 'considered by itself' in sentence [[2]]."),
          ("1243", "Sentence [[4]] locates 'the danger' before any danger has been described; the interactions of sentence [[3]] must come first.")],
   exams=HARD)

pj("V01-L-017", CG, "Colonial hill stations in India were built as imitations of home as much as refuges from heat.", "Easy",
   ["In the nineteenth century, British officials in India began building towns in the hills to escape the summer heat of the plains.",
    "These hill stations, as they came to be called, soon grew beyond simple retreats, and some even served as seats of government for part of the year.",
    "Whether summer retreat or seasonal capital, each hill station was laid out by its builders to resemble the towns of home, with churches, promenades and cottages bearing English names.",
    "Such deliberate imitation shows that the hills offered more than a cooler climate; they offered the illusion of never having left home."],
   "Sentence [[1]] introduces the hill towns. Sentence [[2]] names them ('These hill stations, as they came to be called'), so it must follow [[1]] immediately. Sentence [[3]] ('Whether summer retreat or seasonal capital, each hill station') picks up both the name and the government role introduced in [[2]], and describes how the towns were designed. Sentence [[4]] interprets 'Such deliberate imitation', which is the imitation described in [[3]].",
   "Placing sentence [[3]] second, although 'each hill station' and 'seasonal capital' in it presuppose the name and the government role that sentence [[2]] introduces.",
   "V01L-colonial-hill-stations", "The naming phrase, the echo of 'seasonal capital' and 'Such deliberate imitation' fix the order.",
   traps=[("1324", "Sentence [[3]] already uses the term 'hill station' and speaks of a 'seasonal capital', but the name and the government role are introduced only in sentence [[2]], which 'as they came to be called' places right after the towns first appear."),
          ("1342", "Ending with sentence [[2]] leaves 'each hill station' and 'seasonal capital' in sentence [[3]] without anything to refer to, and the name the towns 'came to be called' would arrive only after they had been discussed.")],
   cognitive="Understanding")

pj("V01-L-018", CG, "Planned capitals seem sterile because the neutrality for which their sites were chosen left them no local life.", "Difficult",
   ["Several countries in the twentieth century built a new capital from scratch rather than enlarge an existing city.",
    "Visitors often find these planned capitals sterile, with grand avenues that seem to lead nowhere and few signs of ordinary street life.",
    "It is easy to read this as a failure of design, but the emptiness follows from the reason the sites were chosen in the first place.",
    "That reason was political: land belonging to no established region could be claimed as a prize by none of them, and so the city began with no local life to inherit."],
   "Sentence [[1]] introduces the planned capitals. Sentence [[2]] reports the common impression that 'these planned capitals' are sterile. Sentence [[3]] rejects the obvious reading of 'this' sterility and points to 'the reason the sites were chosen'. Sentence [[4]] begins 'That reason', so it must come straight after [[3]], and supplies the political motive that explains the emptiness.",
   "Following chronology and putting the political motive of sentence [[4]] second, although 'That reason' needs the reason first mentioned in sentence [[3]].",
   "V01L-planned-capital-cities", "Order depends mainly on the logic of the idea: the chronological order (motive, then result) is tempting, but the argument runs observation, misreading, true cause, and only that order gives 'That reason' a referent.",
   traps=[("1423", "Chronology tempts students to give the motive before the result, but sentence [[4]] opens with 'That reason', and no reason has been mentioned until sentence [[3]] speaks of 'the reason the sites were chosen'."),
          ("1342", "Sentence [[3]] reads 'this' as a failure of design, but the sterility it refers to is described only in sentence [[2]].")],
   exams=HARD)

pj("V01-L-019", CG, "Artists revive cheap districts and are then priced out, a cycle that consumes its own makers.", "Medium",
   ["In many cities, artists are the first newcomers to move into a run-down district, drawn by cheap rents and large empty buildings.",
    "Their studios, galleries and cafes slowly give the area a reputation for being interesting rather than merely cheap.",
    "That reputation attracts better-off residents and developers, and rents begin to climb.",
    "Before long, the artists themselves can no longer afford the neighbourhood they helped to make fashionable.",
    "The pattern is common enough to suggest that cultural revival, left to the market alone, tends to consume its own makers."],
   "Sentence [[1]] introduces the artists and why they arrive. Sentence [[2]] describes what 'Their studios' do to the area's reputation. Sentence [[3]] traces the effect of 'That reputation': wealthier arrivals and rising rents. Sentence [[4]] gives the result for the artists. Sentence [[5]] generalises 'The pattern' into a conclusion.",
   "Ending with sentence [[4]] after sentence [[5]] because it sounds like a final irony, though 'The pattern' needs the whole cycle, including the artists being priced out.",
   "V01L-artists-and-gentrification", "Order depends mainly on the logic of the idea: a causal chain whose stages must run in sequence, closed by a generalisation.",
   traps=[("12354", "Sentence [[5]] generalises about revival consuming 'its own makers', which presupposes the artists being priced out in sentence [[4]]; the outcome must come before the moral drawn from it."),
          ("13245", "Sentence [[3]] needs 'That reputation', which the artists' studios create in sentence [[2]]; rents cannot climb on a reputation not yet established.")])

pj("V01-L-020", CG, "Embankments that make floods rarer encourage building that makes the eventual flood more destructive.", "Medium",
   ["When a town builds embankments to protect itself from a river, the land behind them seems newly safe for houses and shops.",
    "Development duly spreads across the old floodplain, and the value of what stands there rises year by year.",
    "Floods become rarer, but when an unusually high river finally overtops the embankment, it finds far more to destroy than before.",
    "Protection intended to reduce flood losses can thus, over decades, make the eventual losses larger."],
   "Sentence [[1]] describes the embankment and the sense of safety it creates. Sentence [[2]] follows ('duly') with development on the floodplain. Sentence [[3]] shows the consequence when a large flood comes: 'far more to destroy', which presupposes the development of [[2]]. Sentence [[4]] states the general paradox with 'thus'.",
   "Placing sentence [[3]] before sentence [[2]] because floods becoming rarer seems to follow the embankment directly, which leaves 'far more to destroy than before' unexplained.",
   "V01L-building-on-floodplains", "Order depends mainly on the logic of the idea: the greater destruction in the flood sentence depends on the development sentence, without any pronoun to signal it.",
   traps=[("1324", "Sentence [[3]] says the flood finds 'far more to destroy than before', which only follows once sentence [[2]] has described development spreading across the floodplain; and 'duly' in [[2]] needs the sense of safety of sentence [[1]] directly before it.")])

pj("V01-L-021", CG, "Oasis towns flourished on desert caravan trade and shrank when trade found other routes.", "Easy",
   ["Across the great deserts, towns grew up wherever a reliable spring or well made a stopping place possible.",
    "Caravans crossing the sand had to rest and water their animals, and these oasis towns grew rich supplying food, shelter and markets.",
    "That prosperity, however, depended on the trade routes that passed through them.",
    "When ships and later railways carried goods by other paths, many of these towns shrank to a fraction of their former size."],
   "Sentence [[1]] explains where the towns grew. Sentence [[2]] describes the caravan trade that made the towns rich. Sentence [[3]] qualifies 'That prosperity' with 'however': it depended on those routes. Sentence [[4]] shows the consequence when trade moved elsewhere.",
   "Placing sentence [[3]] last, which leaves the decline in sentence [[4]] stated before the dependence that explains it.",
   "V01L-oasis-caravan-towns", "Clear chronology and 'however' make the order plain.",
   traps=[("1243", "Sentence [[3]] explains why the towns were vulnerable, so it must come before the decline in sentence [[4]], not after it."),
          ("1324", "Sentence [[3]] refers to 'That prosperity', but no prosperity has been mentioned until the towns grow rich in sentence [[2]].")],
   cognitive="Understanding")

pj("V01-L-022", PE, "A whistleblower who reports fraud may be the most loyal employee, if loyalty is owed to an institution's purpose.", "Medium",
   ["Whistleblowers are often accused of disloyalty, as though exposing wrongdoing were a betrayal of their colleagues.",
    "The charge assumes that loyalty is owed to the people of an organisation, whatever they happen to be doing.",
    "But loyalty to an institution is usually loyalty to its stated purpose, whether that is healing patients or serving customers honestly.",
    "On that view, the employee who reports fraud may be the most loyal person in the building."],
   "Sentence [[1]] states the accusation of disloyalty. Sentence [[2]] identifies the assumption behind 'The charge'. Sentence [[3]] challenges that assumption with 'But', offering a different object of loyalty. Sentence [[4]] draws the conclusion 'On that view', which refers to the view of [[3]].",
   "Placing sentence [[3]] before sentence [[2]], so that the rival account of loyalty is offered before the assumption it challenges has been exposed.",
   "V01L-whistleblowing-and-loyalty", "Order depends mainly on the logic of the idea: accusation, hidden assumption, rival account and its consequence.",
   traps=[("1324", "Sentence [[3]] answers the assumption about whom loyalty is owed to, which is stated only in sentence [[2]]; and 'On that view' in sentence [[4]] must follow the view of [[3]], not the assumption.")])

pj("V01-L-023", PE, "The transitivity objection suggests memory is evidence of personal identity rather than what identity consists in.", "Difficult",
   ["One influential view holds that what makes you the same person as some earlier individual is your ability to remember that individual's experiences from the inside.",
    "The view has obvious appeal, since memory seems to be what binds the separate episodes of a life into a single story.",
    "A well-known objection imagines an old general who remembers his first battle but has forgotten his boyhood, which the young officer at that battle recalled clearly.",
    "If remembering is what identity consists in, the general is the officer and the officer is the boy, yet the general is not the boy.",
    "Since sameness cannot behave like this, memory may be evidence of who someone is without being what personal identity consists in."],
   "Sentence [[1]] states the memory view. Sentence [[2]] grants its appeal. Sentence [[3]] introduces the objection with the general, the officer and the boy. Sentence [[4]] works through the case: by the memory view the general is the officer and the officer the boy, yet the general is not the boy. Sentence [[5]] concludes from 'this' failure of sameness that memory is evidence of identity rather than its substance.",
   "Placing sentence [[4]] before sentence [[3]] because it states the logic of the objection, though the general, the officer and the boy are introduced only in sentence [[3]].",
   "V01L-memory-theory-identity", "Order depends mainly on the logic of the idea: the solver must follow a transitivity argument, setting the case before its analysis and the analysis before the verdict.",
   traps=[("12435", "Sentence [[4]] speaks of 'the general', 'the officer' and 'the boy' as already known, but they are introduced only in sentence [[3]]."),
          ("13245", "Granting the view 'obvious appeal' in sentence [[2]] after the objection has been raised breaks the argument; the concession belongs before the objection, and sentence [[4]] must follow the case in sentence [[3]] directly.")],
   exams=HARD)

pj("V01-L-024", PE, "Deferring to experts is rational but shifts the layperson's judgement to choosing whom to trust.", "Difficult",
   ["Most of what any of us believes about medicine, climate or economics rests not on our own investigation but on the word of experts.",
    "This is not a failing, since no one could check more than a tiny fraction of such claims for themselves.",
    "Deference does not free us from judgement entirely, however, because experts sometimes disagree and someone must decide whom to believe.",
    "The layperson's task is thus shifted rather than abolished: from weighing the evidence to weighing the track records and incentives of those who report it."],
   "Sentence [[1]] observes that most beliefs rest on experts. Sentence [[2]] defends 'This' reliance. Sentence [[3]] qualifies the defence with 'however': deference still requires judgement when experts disagree. Sentence [[4]] concludes ('thus') that the task is 'shifted rather than abolished', which presupposes both that deference is reasonable ([[2]]) and that judgement remains ([[3]]).",
   "Placing sentence [[3]] second, so that the qualification arrives before the defence it qualifies, and 'This is not a failing' then seems to defend the need for judgement.",
   "V01L-deferring-to-experts", "Order depends mainly on the logic of the idea: defence must precede qualification, and the conclusion combines both; the word 'Deference' first appears in the qualifying sentence, which tempts solvers to place it early.",
   traps=[("1324", "With sentence [[3]] second, 'This is not a failing' in sentence [[2]] would refer to the need for judgement rather than to reliance on experts, and 'however' in [[3]] would have no defence to qualify."),
          ("1243", "Sentence [[4]] says the task is 'thus shifted rather than abolished', but without sentence [[3]] before it nothing has shown that any task remains.")],
   exams=HARD)

pj("V01-L-025", PE, "A duty of gratitude makes sense as a duty to acknowledge a benefit, not to feel an emotion on demand.", "Medium",
   ["It seems odd to speak of a duty of gratitude, since thanks extracted by obligation hardly feel like thanks at all.",
    "Yet we do blame people who accept great kindness and then behave as though nothing had been done for them.",
    "The blame suggests that gratitude is owed after all, even if it cannot be demanded in the way a debt can.",
    "Perhaps the duty is not to feel a particular emotion on cue but to acknowledge the benefit and not act against the benefactor.",
    "Understood this way, a duty of gratitude no longer clashes with the spontaneity that makes thanks valuable."],
   "Sentence [[1]] raises the puzzle: a duty of gratitude seems self-defeating. Sentence [[2]] counters with 'Yet': we blame the ungrateful. Sentence [[3]] interprets 'The blame' as evidence that gratitude is owed. Sentence [[4]] proposes what the duty might be. Sentence [[5]] shows that, 'Understood this way', the duty resolves the puzzle of [[1]].",
   "Placing sentence [[4]] before sentence [[3]], so that the duty is redefined before the paragraph has shown that there is any duty to redefine.",
   "V01L-duties-of-gratitude", "Order depends mainly on the logic of the idea: puzzle, counter-evidence, inference, proposal and resolution; the proposal must follow the inference that a duty exists.",
   traps=[("12435", "Sentence [[4]] proposes what 'the duty' consists of, but that there is a duty at all is first inferred in sentence [[3]]; and 'The blame' in [[3]] must follow the blaming described in sentence [[2]]."),
          ("13245", "Sentence [[3]] refers to 'The blame', which needs the blaming of the ungrateful in sentence [[2]] before it.")])
