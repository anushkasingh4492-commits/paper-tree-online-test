import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

AX = ("CAT", "XAT")

# 001 Technology, Easy, 4
pj("V01-G-001", "Technology", "Repairing an undersea cable is a sequence: locate the fault, hook the cable, splice and relay it.", "Easy",
   ["When an undersea communications cable breaks, the first task is to work out where along its great length the fault actually lies.",
    "Engineers do this from the shore, sending a pulse down the line and timing the reflection that comes back from the break.",
    "Once the position is known, a repair ship sails to the spot and lowers a grapnel to drag the seabed and hook the damaged cable.",
    "The two severed ends are then hauled aboard, joined with a new section, and lowered back to the bottom."],
   "Sentence [[1]] opens by stating the first task, locating the fault. Sentence [[2]] says engineers 'do this', which can only refer to locating the fault. Sentence [[3]] begins 'Once the position is known', the result of the timing method in [[2]], and brings the cable up by grapnel. Sentence [[4]] follows with 'then', splicing the 'severed ends' that the grapnel in [[3]] has hooked.",
   "Starting with the ship sailing out, as if the repair began at sea, which leaves 'Once the position is known' with nothing before it.",
   "V01G-submarine-cable-repair",
   "A plain procedure with clear sequence markers ('the first task', 'do this', 'Once', 'then').",
   traps=[("1324", "Sentence [[3]] needs the position to be known already, which happens only through the shore measurement in sentence [[2]]; and 'do this' in [[2]] would then follow the hooking of the cable in [[3]], though it can only mean locating the fault.")],
   cognitive="Understanding")

# 002 Technology, Difficult, 4
pj("V01-G-002", "Technology", "Predictive text suits formulaic writing but pulls personal writing towards cliche.", "Difficult",
   ["Predictive text offers, at each point, the words that most often follow what a writer has already typed.",
    "For a note confirming a meeting this is exactly what is wanted, since such notes are formulaic and nobody reads them for their style.",
    "A letter of condolence is another matter, because what makes it worth receiving is precisely the phrase that most people would not have thought to use.",
    "Accept enough suggestions while writing one, and the letter drifts, word by word, towards what everyone says, which is the one thing it should not be."],
   "Sentence [[1]] describes the mechanism: the words that 'most often follow'. Sentence [[2]] judges that mechanism ('this') well suited to formulaic notes. Sentence [[3]] sets up the contrasting case with 'another matter', which needs the routine case of [[2]] before it, and explains that a condolence letter is valued for the unusual phrase. Sentence [[4]] applies the mechanism to that case: 'writing one' refers to the letter, and drifting 'towards what everyone says' is bad only because of the value named in [[3]].",
   "Ending with the meeting note, as a concession, which leaves 'another matter' in the condolence sentence with no prior case to contrast with.",
   "V01G-predictive-text-autocomplete",
   "The order depends on the logic of the contrast (routine note, then personal letter, then the cost to that letter); the tempting order puts the concession about routine notes last.",
   traps=[("1342", "Sentence [[3]] calls the condolence letter 'another matter', so a first case must come before it; that case is the meeting note in sentence [[2]], which cannot be postponed to the end."),
          ("1243", "Sentence [[4]] says 'while writing one', and the only thing it can mean is the letter of condolence introduced in sentence [[3]].")],
   exams=AX)

# 003 Technology, Difficult, 5
pj("V01-G-003", "Technology", "Digital copying preserves bits but not readability, so archivists favour open formats.", "Difficult",
   ["We tend to think of digital records as safer than paper, since they can be copied any number of times without the slightest loss.",
    "Copying, however, preserves only the sequence of bits, and a sequence of bits means nothing without a program that knows how to interpret it.",
    "A file in a format that no surviving program can read is in practice as lost as a letter that has been burned, even though every bit is intact.",
    "To guard against such losses, archivists concerned with centuries rather than years prefer plain, openly documented formats to convenient proprietary ones.",
    "Their reasoning is that a published specification allows the file to be read again by anyone willing to write a new program, even after every original program has vanished."],
   "Sentence [[1]] states the common belief. Sentence [[2]] qualifies it with 'however': copying keeps bits but not their meaning. Sentence [[3]] draws the consequence of [[2]], a file with intact bits that is still lost. Sentence [[4]] gives the practical response 'To guard against such losses', which needs the lost file of [[3]] before it, and sentence [[5]] explains the archivists' reasoning, 'Their' referring to the archivists of [[4]].",
   "Putting the burned-letter sentence directly after the opening belief because both talk about loss, which makes the 'however' of the bits sentence redundant.",
   "V01G-digital-file-format-obsolescence",
   "The sentences share vocabulary (copying, bits, programs), so the reader must follow the argument from belief to qualification to consequence to remedy; the burned-letter sentence is a tempting second sentence.",
   traps=[("13245", "Sentence [[3]] applies the principle that bits mean nothing without an interpreting program, which is stated only in sentence [[2]]; placed straight after the opening belief, it asserts a loss the paragraph has not yet explained, and the 'however' of [[2]] then has nothing left to qualify."),
          ("12354", "Sentence [[5]] begins 'Their reasoning', and the only people whose reasoning it can be are the archivists introduced in sentence [[4]].")],
   exams=AX)

# 004 Technology, Medium, 4
pj("V01-G-004", "Technology", "Spreadsheets changed office work with figures from arithmetic to analysis rather than ending it.", "Medium",
   ["When electronic spreadsheets first appeared on personal computers, many predicted that they would make the clerks who kept ledgers redundant.",
    "Recalculating a large ledger by hand had taken days, and the new programs did it in seconds whenever a single figure was changed.",
    "Yet in many offices the work of handling figures did not disappear so much as change its shape.",
    "The new shape was analysis rather than arithmetic, because trying out an assumption had become so cheap that managers began asking for far more projections than anyone had prepared before."],
   "Sentence [[1]] states the prediction. Sentence [[2]] gives the reason the prediction seemed sound: the programs did in seconds what took days. Sentence [[3]] turns against the prediction with 'Yet', and sentence [[4]] names 'the new shape' that [[3]] mentions and explains why it arose.",
   "Placing the 'Yet' sentence immediately after the prediction, before the reason for the prediction has been given.",
   "V01G-spreadsheets-accounting-clerks",
   "The order follows the logic of prediction, its ground, its failure and the explanation; the sentence giving the ground for the prediction could be misplaced as evidence for the outcome.",
   traps=[("1324", "Sentence [[2]] supports the prediction of redundancy, not the outcome, so it must come before the 'Yet' of sentence [[3]]; placed after it, it would separate 'change its shape' from 'The new shape' in sentence [[4]].")])

# 005 Technology, Medium, 5
pj("V01-G-005", "Technology", "Pneumatic tube post was fast but fixed, and lost to the flexible telephone.", "Medium",
   ["In several large cities of the late nineteenth century, letters were sent through networks of underground tubes by compressed air, crossing town in minutes.",
    "For urgent messages within a crowded centre, nothing else available at the time came close to that speed.",
    "The weakness lay in what made the tubes fast: each was a fixed physical route that had to be dug, and reaching a new district meant digging again.",
    "Telephone wires, by contrast, needed no digging, since they could be strung cheaply along existing streets, and they carried not a written message but the conversation itself.",
    "The tubes were therefore not beaten at their own game of speed so much as made beside the point by a medium that could reach almost everywhere."],
   "Sentence [[1]] introduces the tube networks. Sentence [[2]] refers to 'that speed' and states their strength. Sentence [[3]] gives the weakness, the need to dig. Sentence [[4]] contrasts the telephone, which 'needed no digging', so it must follow [[3]]. Sentence [[5]] concludes with 'therefore', combining the strength of [[2]] with the reach of [[4]].",
   "Setting the telephone against the tubes immediately after their speed is praised, which leaves 'needed no digging' with nothing to contrast with.",
   "V01G-pneumatic-tube-mail",
   "Reference words help, but the reader must see that the telephone sentence contrasts with the cost of digging, not with speed.",
   traps=[("12435", "Sentence [[4]] says the telephone 'needed no digging', a contrast that only makes sense after sentence [[3]] has explained that the tubes had to be dug.")])

# 006 Arts and literature, Medium, 4
pj("V01-G-006", "Arts and literature", "The turn in the Italian sonnet makes the poem enact a change of mind.", "Medium",
   ["The Italian sonnet divides its fourteen lines into a group of eight and a group of six, and the shift between them is traditionally called the turn.",
    "In the first group the poet usually lays out a situation, a question or a complaint.",
    "The second group then answers, qualifies or overturns what has been set up, so that the poem enacts a change of mind rather than merely describing one.",
    "A reader who knows this learns to hold the opening lines provisionally, as positions the poem may yet abandon."],
   "Sentence [[1]] introduces the two groups and the turn. Sentence [[2]] describes the first group and sentence [[3]] the second, which 'then' responds to it. Sentence [[4]] draws the consequence for the reader: the opening lines are 'positions the poem may yet abandon', which depends on [[3]] having said that the second group may overturn them.",
   "Moving the reader sentence up to follow the description of the structure, before the paragraph has said that the second group can overturn the first.",
   "V01G-sonnet-volta",
   "The final sentence's place follows from the idea, not a pronoun alone: reading the opening as provisional only makes sense once overturning has been described.",
   traps=[("1423", "Sentence [[4]] treats the opening lines as positions the poem may 'abandon', which presupposes the overturning described in sentence [[3]]; placed second, it anticipates a claim the paragraph has not made.")])

# 007 Arts and literature, Easy, 4
pj("V01-G-007", "Arts and literature", "An audiobook narrator interprets the text rather than delivering it neutrally.", "Easy",
   ["Listening to an audiobook is often described as reading by ear, as though the narrator merely delivered the text unchanged.",
    "In fact, every narrator must make decisions that a silent reader makes privately, such as where to pause, which word to stress and how each character should sound.",
    "These choices settle questions the printed page leaves open, so that an ironic line read sincerely can become a different line altogether.",
    "The listener therefore receives not only the author's book but also one performer's interpretation of it."],
   "Sentence [[1]] states the common description. Sentence [[2]] corrects it with 'In fact'. Sentence [[3]] refers to 'These choices', the decisions listed in [[2]]. Sentence [[4]] concludes with 'therefore'.",
   "Opening with the narrator's decisions, which leaves 'In fact' correcting nothing.",
   "V01G-audiobook-narration",
   "Clear chain of common view, correction ('In fact'), reference ('These choices') and conclusion ('therefore').",
   traps=[("2134", "Sentence [[2]] begins 'In fact', which corrects a view; that view is the description in sentence [[1]], so [[1]] must open.")],
   cognitive="Understanding")

# 008 Arts and literature, Medium, 5
pj("V01-G-008", "Arts and literature", "Darkening the auditorium changed how audiences behaved, not only how they saw.", "Medium",
   ["For most of theatrical history the auditorium stayed lit throughout a performance, since candles and oil lamps could not easily be dimmed and relit.",
    "In such a hall spectators could see one another as clearly as they saw the actors, and an evening at the theatre was as much about being seen as about watching.",
    "Gas, and later electric, lighting changed this by allowing the house to be darkened while the stage stayed bright.",
    "The change was social as well as technical, for an audience sitting in darkness cannot watch itself and is left with nothing to attend to but the play.",
    "If so, habits now regarded as simple good manners, such as silence and stillness during a scene, may owe as much to lighting as to any refinement of taste."],
   "Sentence [[1]] describes the lit auditorium and why it stayed lit. Sentence [[2]] begins 'In such a hall' and draws the social consequence. Sentence [[3]] says new lighting 'changed this'. Sentence [[4]] calls 'The change' social as well as technical, and sentence [[5]] draws a tentative conclusion with 'If so', which rests on the claim in [[4]].",
   "Jumping from the new lighting straight to modern manners, which leaves the 'If so' of the last sentence resting on a claim not yet made.",
   "V01G-theatre-stage-lighting",
   "Five sentences in historical order; the reader must see that the conclusion about manners depends on the social claim, not on the technical one.",
   traps=[("12354", "Sentence [[5]] opens 'If so', conditional on the claim that darkness leaves an audience nothing to watch but the play; that claim is made only in sentence [[4]]."),
          ("31245", "Sentence [[3]] says the new lighting 'changed this', so something must precede it; and sentence [[4]] must follow [[3]] directly, because 'The change' is the darkening of the house.")])

# 009 Arts and literature, Medium, 4
pj("V01-G-009", "Arts and literature", "The blank between comic panels is where readers supply the story.", "Medium",
   ["Nothing is drawn in the narrow blank between two comic panels, and most readers never consciously look at it.",
    "Yet it is there that much of the story happens, since whatever occurs between one frozen moment and the next must be supplied by the reader.",
    "Show a raised fist in one panel and a man rubbing his jaw in the next, and the reader imagines the punch without any sense of having done work.",
    "Acts of completion as small as this one are the medium's real material, and much of a cartoonist's craft lies in judging how many of them to ask for."],
   "Sentence [[1]] introduces the blank between panels. Sentence [[2]] turns with 'Yet' to claim that the story happens there. Sentence [[3]] illustrates the claim with the imagined punch. Sentence [[4]] generalises from 'this one', the punch, to the cartoonist's craft.",
   "Placing the general point about the craft before the example, which leaves 'this one' with no single act to refer to.",
   "V01G-comic-strip-panel-gutters",
   "The example must sit between the claim it illustrates and the generalisation that refers back to it; the order follows the logic of claim, illustration, lesson.",
   traps=[("1243", "Sentence [[4]] speaks of 'Acts of completion as small as this one', which needs the single imagined punch of sentence [[3]] before it.")])

# 010 Language and media, Easy, 4
pj("V01-G-010", "Language and media", "Newspapers prepare obituaries of prominent people in advance for the sake of accuracy.", "Easy",
   ["Most newspaper obituaries are written quickly, within a day or two of the death they report.",
    "For prominent figures, many papers avoid that rush by preparing obituaries years in advance and quietly updating them as their subjects' lives go on.",
    "This practice can look macabre to outsiders, as if journalists were simply waiting for people to die.",
    "Its real purpose is accuracy, since a life summarised over months is less likely to contain errors than one summarised overnight."],
   "Sentence [[1]] describes the usual haste. Sentence [[2]] refers to 'that rush' and introduces advance obituaries. Sentence [[3]] says 'This practice' looks macabre. Sentence [[4]] answers with 'Its real purpose'.",
   "Starting with advance preparation, which leaves 'that rush' without a referent.",
   "V01G-obituary-writing",
   "Reference words ('that rush', 'This practice', 'Its real purpose') fix the order.",
   traps=[("2134", "Sentence [[2]] avoids 'that rush', which is the haste described in sentence [[1]]; and 'This practice' in sentence [[3]] means advance preparation, so [[3]] must follow [[2]].")],
   cognitive="Understanding")

# 011 Language and media, Medium, 5
pj("V01-G-011", "Language and media", "The semicolon joins two independent statements and leaves their connection to the reader.", "Medium",
   ["The semicolon is often treated as an ornament, a mark that careful writers use to show off and everyone else can safely ignore.",
    "Its actual job is more modest and more useful: it joins two statements that could each stand alone as sentences.",
    "A full stop between them would present the two as separate thoughts, while a comma alone would usually be a grammatical error.",
    "The semicolon sits between these options, telling the reader that the statements belong together without spelling out how.",
    "That last feature is both its strength and its risk, because the reader must work out the connection that a word like 'because' or 'but' would have supplied."],
   "Sentence [[1]] states the common view. Sentence [[2]] gives the 'actual job'. Sentence [[3]] considers alternatives placed 'between them', the two statements of [[2]]. Sentence [[4]] places the semicolon 'between these options', the full stop and comma of [[3]]. Sentence [[5]] takes up 'That last feature', not spelling out the connection, from the end of [[4]].",
   "Putting the semicolon's position between the options before the options have been named.",
   "V01G-semicolon-usage",
   "A chain of references ('between them', 'these options', 'That last feature') across five sentences.",
   traps=[("12435", "Sentence [[4]] places the semicolon 'between these options', the full stop and the comma, which are named only in sentence [[3]].")])

# 012 Language and media, Medium, 4
pj("V01-G-012", "Language and media", "Cryptic clues look lawless but their two converging routes make answers certain.", "Medium",
   ["To a newcomer, a cryptic crossword clue reads like a riddle without rules, a sentence whose answer could be almost anything.",
    "A well-made clue in fact offers two independent routes to one word: a plain definition at one end, and wordplay that assembles the answer from its parts.",
    "Taken alone, either route would leave the solver guessing, since many words fit a brief definition and most wordplay can be parsed in several ways.",
    "Where the two routes meet, however, there is usually just one word, and a solver who finds it can be surer of it than of any answer to an ordinary riddle."],
   "Sentence [[1]] gives the newcomer's impression. Sentence [[2]] corrects it ('in fact') by describing the two routes. Sentence [[3]] says either route 'alone' is insufficient. Sentence [[4]] contrasts with 'however': where the routes meet, the answer is fixed. The 'however' requires the limitation of [[3]] before it.",
   "Ending with the weakness of each route, which would leave the 'however' of the meeting-point sentence with nothing to contrast with.",
   "V01G-crossword-clue-conventions",
   "The last two sentences depend on the logic of insufficient parts and sufficient whole; the order of the limitation and the resolution must be grasped.",
   traps=[("1243", "Sentence [[4]] uses 'however' to contrast the meeting of the routes with something negative, and the only negative statement is that each route alone leaves the solver guessing, in sentence [[3]].")])

# 013 Language and media, Easy, 4
pj("V01-G-013", "Language and media", "A percentage chance of rain describes frequency, not duration.", "Easy",
   ["A forecast that gives a seventy per cent chance of rain is often misread as a statement about how much of the day will be wet.",
    "What the figure actually expresses is how often rain falls at a given place on days with conditions like the ones expected.",
    "On seven such days in ten it rains at least a little there, and on the other three it stays dry.",
    "Understood this way, the number tells a reader whether to carry an umbrella, not how long the shower will last."],
   "Sentence [[1]] states the misreading. Sentence [[2]] gives what 'the figure actually expresses'. Sentence [[3]] spells it out with 'such days', the days with similar conditions in [[2]]. Sentence [[4]] concludes with 'Understood this way'.",
   "Beginning with the explanation of what the figure expresses, which leaves 'actually' correcting nothing.",
   "V01G-weather-forecast-wording",
   "Misreading, correction, illustration and conclusion, each marked by a clear cue.",
   traps=[("2314", "Sentence [[2]] says what the figure 'actually' expresses, which corrects a misreading; that misreading is sentence [[1]], so [[1]] opens.")],
   cognitive="Understanding")

# 014 Education, Medium, 4
pj("V01-G-014", "Education", "Setting by ability serves top sets more easily than lower ones, so its value depends on the lower sets.", "Medium",
   ["Placing pupils in classes according to their ability promises lessons pitched at the right level for everyone.",
    "The promise is easiest to keep for the top sets, whose teachers can move quickly without losing anyone.",
    "In the lower sets the arrangement tends to work less well, partly because expectations fall and partly because pupils come to see their placement as a verdict on themselves.",
    "Whether setting helps on balance therefore depends less on the principle than on whether schools can stop the lower sets from becoming places where little is asked."],
   "Sentence [[1]] states the promise. Sentence [[2]] says 'The promise' is easiest to keep in the top sets. Sentence [[3]] compares the lower sets, where it works 'less well', a comparison that needs [[2]]. Sentence [[4]] concludes with 'therefore' that the verdict depends on the lower sets.",
   "Taking the lower sets before the top sets, which leaves 'less well' without anything to be compared with.",
   "V01G-mixed-ability-grouping",
   "The order of the middle pair follows from the comparison ('easiest' then 'less well') and from the conclusion focusing on the lower sets.",
   traps=[("1324", "Sentence [[3]] says the arrangement works 'less well' in the lower sets, a comparison with the top sets of sentence [[2]]; and sentence [[4]] concludes about the lower sets, so it must follow [[3]] directly.")])

# 015 Education, Easy, 4
pj("V01-G-015", "Education", "Fluent handwriting frees attention for thought, which is one reason to keep teaching it.", "Easy",
   ["Many schools have cut the time spent teaching joined-up handwriting, reasoning that pupils will do most of their writing on keyboards.",
    "Some teachers resist the change, however, and they do so not only out of nostalgia.",
    "They point out that a child who forms each letter slowly and with effort has less attention left for what the sentence is meant to say.",
    "On this view, fluent handwriting matters not as a fine art but as a way of making the physical act of writing automatic, so that the mind is free for thought."],
   "Sentence [[1]] describes the change. Sentence [[2]] says some teachers resist 'the change'. Sentence [[3]] gives their argument ('They'). Sentence [[4]] states the conclusion 'On this view'.",
   "Starting with the teachers' resistance, which leaves 'the change' undefined.",
   "V01G-cursive-handwriting-instruction",
   "Simple chain: the change, resistance to it, the teachers' reason, the view it supports.",
   traps=[("2134", "Sentence [[2]] resists 'the change', which must already have been described; that is the cut in teaching time in sentence [[1]].")],
   cognitive="Understanding")

# 016 Education, Medium, 4
pj("V01-G-016", "Education", "School trips teach mainly through classroom preparation and follow-up.", "Medium",
   ["A school trip to a museum or a factory is usually justified by what pupils will learn while they are there.",
    "Teachers who run such trips often find that the visit itself is too crowded and too short for much to sink in.",
    "What rescues such trips is the work done in the classroom before and after, when pupils prepare questions to take with them and then make sense of what they saw.",
    "Without that framing, a trip is likely to be remembered chiefly as a day out, its lessons lost among the coach journey and the packed lunch."],
   "Sentence [[1]] states the usual justification. Sentence [[2]] raises the problem that the visit itself teaches little. Sentence [[3]] says what 'rescues' such trips, which presupposes the problem of [[2]]. Sentence [[4]] refers to 'that framing', the classroom work of [[3]].",
   "Putting the classroom work right after the justification, which leaves 'rescues' with nothing to rescue the trips from.",
   "V01G-school-field-trips",
   "The middle order follows from the logic of problem and remedy; 'rescues' only makes sense after the problem is stated.",
   traps=[("1324", "Sentence [[3]] says what 'rescues' trips, which presupposes the problem of crowded, short visits in sentence [[2]]; and 'that framing' in sentence [[4]] must follow [[3]] directly.")])

# 017 Education, Difficult, 5
pj("V01-G-017", "Education", "Chess in schools is better defended for its own sake than for doubtful transfer to other subjects.", "Difficult",
   ["Chess is often brought into schools with the promise that it will sharpen pupils' thinking in other subjects, mathematics above all.",
    "Behind the promise lies a picture of the mind as a muscle, strengthened by any hard exercise and then available for every task.",
    "Skills, however, tend to be narrower than that picture allows, so that a pupil who gets better at calculating chess variations need not get any better at algebra.",
    "None of this is a reason to drop the game from the timetable.",
    "It does mean, though, that chess is better defended as a rich and absorbing activity in its own right than as a disguised lesson in something else."],
   "Sentence [[1]] states the promise. Sentence [[2]] names the assumption 'Behind the promise'. Sentence [[3]] challenges 'that picture'. Sentence [[4]] concedes that 'None of this', the challenge of [[3]], justifies dropping chess. Sentence [[5]] says what the challenge 'does mean, though', which needs the concession of [[4]] before it.",
   "Treating the two closing sentences as interchangeable, when the 'though' of the final sentence must answer the concession that the game should stay.",
   "V01G-chess-in-schools",
   "The argument moves from promise to assumption to critique to a qualified conclusion; the reader must see that the concession precedes the reframing, and that the critique attacks the assumption rather than the promise directly.",
   traps=[("12354", "Sentence [[5]] says what the critique 'does mean, though', a contrast with what it does not mean; that is stated in sentence [[4]], so [[4]] must come first."),
          ("13245", "Sentence [[3]] says skills are narrower than 'that picture allows', and the picture of the mind as a muscle is introduced only in sentence [[2]].")],
   exams=AX)

# 018 Health and medicine, Easy, 4
pj("V01-G-018", "Health and medicine", "Distrust of generic medicines reflects judging quality by price.", "Easy",
   ["A generic medicine contains the same active ingredient, in the same dose, as the branded product it copies.",
    "Before it can be sold, its maker must usually show that it is absorbed into the body at a comparable rate and to a comparable extent.",
    "Despite these requirements, many patients suspect that the cheaper pill must be the weaker one.",
    "The suspicion says more about how we judge quality by price than about any measured difference between the drugs."],
   "Sentence [[1]] defines a generic medicine. Sentence [[2]] adds the testing requirement for 'it'. Sentence [[3]] says 'Despite these requirements' patients are suspicious. Sentence [[4]] comments on 'The suspicion'.",
   "Opening with the patients' suspicion, which leaves 'these requirements' with nothing to refer to.",
   "V01G-generic-drug-trust",
   "The facts come first, then the suspicion 'despite' them, then a comment on 'The suspicion'.",
   traps=[("1342", "Sentence [[3]] reacts to 'these requirements', the absorption tests in sentence [[2]], so [[2]] must precede it.")],
   cognitive="Understanding")

# 019 Health and medicine, Medium, 5
pj("V01-G-019", "Health and medicine", "The harm lies in holding any posture too long, so moving matters more than standing.", "Medium",
   ["Standing desks became popular on the strength of a simple idea: sitting for long hours is bad for the body, so office workers should stand.",
    "The idea mistakes the problem, however, for what seems to matter is less the posture itself than the length of time spent in any one posture.",
    "By that measure, a worker who stands motionless at a desk all afternoon has gained little, having merely swapped one fixed posture for another.",
    "Such a worker may simply exchange a stiff back for aching feet and legs.",
    "The more useful advice is therefore duller than any piece of furniture: change position often, and get up and move about."],
   "Sentence [[1]] states the idea behind standing desks. Sentence [[2]] says 'The idea' mistakes the problem. Sentence [[3]] applies 'that measure', the length of time spent in one posture, to a motionless standing worker, and sentence [[4]] continues with 'Such a worker'. Sentence [[5]] concludes with 'therefore'.",
   "Placing the aching feet before the motionless worker, which leaves 'Such a worker' without a referent.",
   "V01G-standing-desks",
   "Carried by references ('The idea', 'By that measure', 'Such a worker'), but the reader must see that the example of the motionless worker illustrates the point about duration.",
   traps=[("12435", "Sentence [[4]] begins 'Such a worker', which refers to the motionless standing worker of sentence [[3]]."),
          ("13425", "Sentence [[3]] judges the standing worker 'By that measure', the length of time in one posture, which is introduced only in sentence [[2]]; straight after the idea in sentence [[1]] it has no measure to refer to.")])

# 020 Health and medicine, Medium, 4
pj("V01-G-020", "Health and medicine", "The stigma of hearing aids, like that once attached to spectacles, can fade.", "Medium",
   ["Many people who would benefit from hearing aids wait years before getting them.",
    "Cost and inconvenience play a part, but the larger obstacle is often what the device seems to announce about its wearer.",
    "Spectacles were once regarded in a similar way, yet they have long since become ordinary and are sometimes even fashionable.",
    "Their example suggests that such a stigma is not fixed, and that a device seen often enough comes to signal not weakness but a practical solution."],
   "Sentence [[1]] states the delay. Sentence [[2]] explains it, chiefly by what the device 'seems to announce'. Sentence [[3]] compares spectacles, regarded 'in a similar way', which requires the stigma of [[2]]. Sentence [[4]] draws the lesson from 'Their example'.",
   "Introducing spectacles before the stigma has been named, so that 'in a similar way' has no comparison.",
   "V01G-hearing-aid-stigma",
   "The analogy must come after the stigma it compares and before the lesson drawn from it; the logic of problem, analogy and lesson fixes the order.",
   traps=[("1324", "Sentence [[3]] says spectacles were regarded 'in a similar way', which presupposes the stigma described in sentence [[2]]; and 'Their example' in sentence [[4]] must follow [[3]].")])

# 021 Health and medicine, Difficult, 5
pj("V01-G-021", "Health and medicine", "Hospitals have shifted from seeing relatives as disturbances to seeing them as partners in care.", "Difficult",
   ["Hospitals long restricted visitors to a few fixed hours, on the grounds that patients needed rest and staff needed room to work.",
    "The rule treated relatives as a disturbance to be managed, something that happened to the ward from outside.",
    "Many hospitals have since relaxed it, on the view that a familiar person at the bedside may notice a change in a patient that a busy nurse would miss.",
    "On this understanding the relative is less a visitor than a partner in care, someone whose knowledge of the patient is itself a resource.",
    "Treating relatives as partners is not costless, and wards must still protect patients who need quiet, but the burden of justification has shifted from those who want to come in to those who would keep them out."],
   "Sentence [[1]] describes the old restriction. Sentence [[2]] interprets 'The rule' as treating relatives as a disturbance. Sentence [[3]] says hospitals have 'relaxed it', giving a reason. Sentence [[4]] states the new understanding that follows from that reason. Sentence [[5]] concedes the costs of 'Treating relatives as partners', a phrase that needs [[4]], and draws the final conclusion.",
   "Putting the concession about costs straight after the relaxation of the rule, before the idea of relatives as partners has been stated.",
   "V01G-hospital-visiting-hours",
   "The paragraph contrasts two conceptions of the relative; the reader must see that the interpretation of the old rule precedes its relaxation and that the concession presupposes the partnership idea.",
   traps=[("12354", "Sentence [[5]] concedes the cost of 'Treating relatives as partners', and relatives are called partners only in sentence [[4]]."),
          ("13245", "Sentence [[2]] interprets the rule as a closed policy; placed after sentence [[3]] it would break the link between the relaxation and 'On this understanding' in sentence [[4]], which must follow [[3]].")],
   exams=AX)

# 022 Cities and geography, Easy, 4
pj("V01-G-022", "Cities and geography", "Cul-de-sac layouts quieten streets but lengthen walks and push traffic onto main roads.", "Easy",
   ["Many suburbs built in the second half of the twentieth century were laid out as networks of curving streets ending in cul-de-sacs.",
    "The design kept through traffic away from houses, giving residents quiet roads where children could play.",
    "The same layout, however, made walking to a shop or a school far longer than the straight-line distance would suggest.",
    "As a result, journeys that could have been short walks were often made by car, adding traffic to the few main roads that every route was forced to join."],
   "Sentence [[1]] introduces the layout. Sentence [[2]] gives its benefit ('The design'). Sentence [[3]] gives the cost ('The same layout, however'). Sentence [[4]] states the consequence of that cost ('As a result').",
   "Placing the consequence about car journeys before the cost that causes it.",
   "V01G-cul-de-sac-suburbs",
   "Benefit, cost and consequence are each clearly marked.",
   traps=[("1243", "Sentence [[4]] says car journeys followed 'As a result' of long walking distances, which are described only in sentence [[3]].")],
   cognitive="Understanding")

# 023 Cities and geography, Difficult, 4
pj("V01-G-023", "Cities and geography", "Public tower blocks failed through neglect that height amplified, not through height itself.", "Difficult",
   ["The tower blocks of post-war public housing are often cited as proof that people cannot live well high above the ground.",
    "Yet expensive private towers in the same cities are eagerly sought, and their residents seldom complain of the isolation supposedly built into height.",
    "What separates the two is less the shape of the building than the care around it: lifts repaired promptly, entrances watched, shared spaces kept up.",
    "Where that care lapsed, height made every failure worse, since a broken lift strands the tenth floor as it never strands the first, and so the form took the blame for a failure of upkeep."],
   "Sentence [[1]] states the common belief. Sentence [[2]] offers a counter-example with 'Yet'. Sentence [[3]] explains what 'separates the two' kinds of tower. Sentence [[4]] reconciles the evidence: 'that care' failed, and height magnified the failure, which explains why the belief in [[1]] arose.",
   "Reading the last sentence as a defence of the common belief and placing it before the counter-example.",
   "V01G-high-rise-housing-estates",
   "The reader must see how the final sentence reconciles the belief and the counter-example; the argument (belief, counter-example, real cause, explanation of the error) fixes the order.",
   traps=[("1342", "Sentence [[3]] explains what separates 'the two', which requires both kinds of tower to have been mentioned; the private towers appear only in sentence [[2]]."),
          ("1243", "Sentence [[4]] says 'that care' lapsed, which refers to the care for lifts and entrances described in sentence [[3]].")],
   exams=AX)

# 024 Cities and geography, Difficult, 5
pj("V01-G-024", "Cities and geography", "A border between paired towns binds them through the differences it creates.", "Difficult",
   ["Where a national border runs through a populated valley, towns often grow up in pairs, facing each other across the line.",
    "It might be expected that the border would simply cut each town off from its natural partner.",
    "Often the reverse happens, because differences in prices, taxes and rules on the two sides give residents a reason to cross that they would not otherwise have.",
    "Whole trades grow up around those differences, from currency exchange to shops selling goods that are cheaper on only one side.",
    "The line that separates the two towns is, in this sense, also what binds them, and an end to its differences could leave both poorer."],
   "Sentence [[1]] describes the paired towns. Sentence [[2]] states an expectation about 'its natural partner', which needs the pairs of [[1]]. Sentence [[3]] says 'the reverse' happens, explaining why. Sentence [[4]] builds on 'those differences'. Sentence [[5]] concludes 'in this sense' that the border binds as well as separates.",
   "Taking the expectation of separation as the opening claim, when it presupposes the paired towns.",
   "V01G-twin-border-towns",
   "The paragraph turns on a reversal of expectation; the reader must place the expectation before its reversal and the trades after the differences that create them.",
   traps=[("21345", "Sentence [[2]] speaks of each town's 'natural partner', which needs the paired towns of sentence [[1]] to be introduced first."),
          ("13245", "Sentence [[3]] says 'the reverse happens', which needs an expectation to reverse; the expectation is stated in sentence [[2]].")],
   exams=AX)

# 025 Cities and geography, Easy, 4
pj("V01-G-025", "Cities and geography", "Allotment gardens now meet social needs more than food needs.", "Easy",
   ["Allotment gardens, small plots rented to city dwellers for growing their own food, are often seen as a relic of wartime shortage.",
    "Yet the waiting lists for plots in many cities suggest that they meet a need that has little to do with food supply.",
    "Indeed, most allotment holders could buy their vegetables more cheaply than they can grow them.",
    "What they gain instead is time outdoors, a reason to be in one place regularly, and the company of neighbours they would not otherwise meet."],
   "Sentence [[1]] states the common view. Sentence [[2]] counters it with 'Yet'. Sentence [[3]] supports [[2]] with 'Indeed'. Sentence [[4]] says what holders gain 'instead' of cheap food.",
   "Placing the point about the cost of vegetables before the 'Yet' sentence, which leaves 'Yet' contrasting with the wrong thing.",
   "V01G-allotment-gardens",
   "Clear connectives ('Yet', 'Indeed', 'instead') fix the order.",
   traps=[("1342", "Sentence [[2]] begins 'Yet', contrasting with the view of allotments as a wartime relic in sentence [[1]]; placed last, it would contrast with the social benefits, which makes no sense.")],
   cognitive="Understanding")
