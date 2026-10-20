import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ 001 Medium, 4
pj("V01-E-001", "Language and media", "Words called untranslatable show only that languages package meanings differently, not that some thoughts are closed to other languages.", "Medium",
   ["Lists of 'untranslatable' words circulate widely, each entry offering a term from some language for which English supposedly has no equivalent.",
    "The implication is usually that speakers of that language possess a feeling or concept that English speakers simply lack.",
    "But the lists themselves undercut the implication, since every entry is followed by a short English gloss that readers grasp at once.",
    "What such words reveal, then, is not a limit on what can be thought, only that one language has packed into a single word what another says in a phrase."],
   "Sentence [[1]] introduces the lists of 'untranslatable' words. Sentence [[2]] states 'The implication' usually drawn from them, that speakers of the other language have a concept English speakers lack. Sentence [[3]] answers with 'But the lists themselves undercut the implication': the English gloss shows the concept is expressible. Sentence [[4]] draws the conclusion ('then'): the words show a difference in packaging, not a limit on thought.",
   "Placing sentence [[4]] straight after sentence [[2]] as a reply to the implication, which leaves its 'then' without the evidence of the English glosses that sentence [[3]] supplies.",
   "V01E-untranslatable-words", "The rebuttal must come before the conclusion it supports, and the conclusion's 'then' can look as though it answers the implication directly.",
   traps=[("1243", "Sentence [[4]] concludes with 'then' that the words reveal no limit on thought, but that conclusion rests on the observation in sentence [[3]] that every entry is understood through a short English gloss."),
          ("1324", "Sentence [[3]] says the lists 'undercut the implication', but the implication is first stated in sentence [[2]].")])

# ------------------------------------------------------------------ 002 Easy, 4
pj("V01-E-002", "Language and media", "Reading aloud was once common for practical reasons, and silent reading spread as those reasons weakened.", "Easy",
   ["Many historians believe that for long stretches of the past, reading was usually a spoken activity, with texts voiced to oneself or to a listening group.",
    "One reason was practical: books were scarce and costly, and a single copy read aloud could serve a whole household.",
    "Another lay in the page itself, since some early manuscripts ran their words together without spaces, and sounding them out helped readers find where each word ended.",
    "As books grew cheaper and pages easier to scan by eye, these reasons weakened, and the silent, solitary reader slowly became the norm."],
   "Sentence [[1]] introduces the claim that reading was once mostly done aloud. Sentence [[2]] gives 'One reason', the scarcity of books. Sentence [[3]] gives 'Another', the layout of early manuscripts. Sentence [[4]] refers to 'these reasons' and shows both weakening: books 'grew cheaper' (answering [[2]]) and pages became 'easier to scan' (answering [[3]]).",
   "Putting sentence [[3]] before sentence [[2]] because manuscripts seem to come first historically, although 'Another' must follow 'One reason'.",
   "V01E-silent-reading-history", "The order is carried by 'One reason', 'Another' and 'these reasons'.",
   traps=[("1324", "Sentence [[3]] begins 'Another', which presupposes the first reason given in sentence [[2]]."),
          ("1243", "Sentence [[4]] speaks of 'these reasons' weakening and answers both scarcity and the unspaced page, so it can come only after both reasons are given.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 003 Medium, 5
pj("V01-E-003", "Language and media", "Emoji work as written gestures standing in for face and voice, and like gestures they depend on shared conventions.", "Medium",
   ["In face-to-face talk, a teasing remark is softened by a smile or a tone of voice that tells the listener it is not meant seriously.",
    "Written messages strip away these signals, which is why a brief text can read as curt or hostile when its writer intended nothing of the kind.",
    "Emoji added to the end of a message have come to fill part of this gap, marking a line as a joke, an apology or a friendly aside.",
    "Seen this way, they are less a new language than a set of written gestures, standing in for the face and voice that typed words leave behind.",
    "But like all gestures, they work only among people who read them the same way, which is why a message that delights one friend can puzzle another."],
   "Sentence [[1]] describes how face and voice soften spoken remarks. Sentence [[2]] says written messages 'strip away these signals'. Sentence [[3]] presents emoji as filling 'this gap'. Sentence [[4]] interprets them ('Seen this way') as written gestures. Sentence [[5]] qualifies with 'But like all gestures', which needs the gesture idea from [[4]], and adds the limit that gestures depend on shared reading.",
   "Placing sentence [[5]] before sentence [[4]] because it seems to continue the description of emoji, although 'like all gestures' depends on [[4]] having called them gestures.",
   "V01E-emoji-tone-markers", "The final pair must be ordered by the idea: emoji must first be classed as gestures before the limit common to all gestures applies to them.",
   traps=[("12354", "Sentence [[5]] says 'like all gestures', but emoji are first described as gestures in sentence [[4]]; before that they are only marks filling a gap."),
          ("13245", "Sentence [[3]] says emoji 'fill part of this gap', and the gap, the loss of face and voice in writing, is created only in sentence [[2]].")])

# ------------------------------------------------------------------ 004 Difficult, 5
pj("V01-E-004", "Language and media", "Judgements of accent track the social standing of speakers rather than qualities of the sound.", "Difficult",
   ["Listeners asked to rate recordings of unfamiliar accents often judge some speakers more intelligent or trustworthy than others, though the recordings differ in nothing but pronunciation.",
    "A natural explanation is that certain accents simply sound clearer or more elegant, and that listeners are responding to qualities in the sound itself.",
    "Yet a pronunciation admired as refined in one region is often ridiculed as lazy in another, where a different group happens to use it.",
    "If the sound were doing the work, it should earn the same verdict everywhere; what varies with the verdict is the standing of the people heard using it.",
    "Judgements of accent, then, are largely judgements of speakers, which is why a once-mocked accent can rise in esteem when its speakers rise in the world."],
   "Sentence [[1]] reports the finding to be explained: ratings differ though only pronunciation differs. Sentence [[2]] offers 'A natural explanation', that the sounds themselves differ in quality. Sentence [[3]] objects ('Yet') with the case of one pronunciation judged differently in two regions. Sentence [[4]] draws out why that case refutes the explanation: if the sound did the work the verdict would not vary, and what varies with it is the speakers' standing. Sentence [[5]] states the general conclusion ('then') and its consequence.",
   "Treating sentence [[3]] as the reply to sentence [[1]] and placing the explanation in sentence [[2]] after it, without noticing that 'Yet' in [[3]] objects to the explanation, not to the finding.",
   "V01E-accent-prestige", "Order depends mainly on the logic of the idea: the regional counter-example must precede the reasoning that turns it against the sound-quality explanation, and the closing general claim looks like a possible thesis.",
   traps=[("13245", "Sentence [[3]] after [[1]] makes 'Yet' contrast with the finding, which it does not contradict; its target is the claim in sentence [[2]] that the sound itself is responsible, and sentence [[4]] ('If the sound were doing the work') must answer that claim directly after the counter-example."),
          ("12435", "Sentence [[4]] says what 'varies with the verdict', but the variation of verdicts between regions is first shown in sentence [[3]]; and sentence [[3]] after [[4]] would make 'Yet' contrast with a claim it supports.")],
   exams=D)

# ------------------------------------------------------------------ 005 Easy, 4
pj("V01-E-005", "Cities and geography", "Street names record what a city chose to honour, which is why renaming them is contested.", "Easy",
   ["Street names look like neutral labels, chosen only so that letters arrive and visitors can find their way.",
    "In practice, many of them record what a city once wished to honour, whether a battle, a benefactor or a local hero.",
    "This is why renaming a street so often provokes argument, since removing a name can feel like withdrawing that honour.",
    "Some residents who object care mainly about the bother of changing their addresses, but the bitterest disputes are usually about memory rather than maps."],
   "Sentence [[1]] states the appearance that street names are neutral labels. Sentence [[2]] corrects it ('In practice'): names record what a city wished to honour. Sentence [[3]] draws the consequence ('This is why'): renaming provokes argument because it withdraws 'that honour'. Sentence [[4]] refers to 'residents who object', which needs the argument of [[3]], and adds the concession about addresses.",
   "Placing sentence [[4]] before sentence [[3]], although the objectors it describes appear only once renaming and its arguments are introduced in [[3]].",
   "V01E-street-naming", "The order follows from 'In practice', 'This is why' and 'that honour'.",
   traps=[("1243", "Sentence [[4]] speaks of residents who object, but nothing has been proposed for them to object to until sentence [[3]] introduces renaming."),
          ("2134", "Sentence [[2]] opens 'In practice', which corrects an appearance; that appearance, names as neutral labels, is stated only in sentence [[1]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 006 Easy, 4
pj("V01-E-006", "Education", "Preparing to teach material improves learning because it forces organisation and exposes gaps.", "Easy",
   ["Students who expect to teach material to others often learn it better than those who study it only to pass a test.",
    "Part of the reason is that preparing to explain something forces a learner to organise it, deciding what matters most and how the parts connect.",
    "It also exposes gaps, because an explanation that seemed clear in one's head tends to falter the moment it has to be spoken aloud.",
    "For these reasons, some teachers now ask pupils to explain a new idea to a partner before they practise it on their own."],
   "Sentence [[1]] states the observation that expecting to teach improves learning. Sentence [[2]] gives 'Part of the reason': explaining forces organisation. Sentence [[3]] adds a second effect with 'It also', where 'It' is preparing to explain. Sentence [[4]] draws the practical consequence 'For these reasons', which needs both reasons.",
   "Starting with sentence [[2]] because it sounds like a general principle, although 'Part of the reason' needs the observation in sentence [[1]] that it explains.",
   "V01E-learning-by-teaching", "The links 'Part of the reason', 'It also' and 'For these reasons' fix the order.",
   traps=[("2314", "Sentence [[2]] opens 'Part of the reason is that', so it must follow the observation it explains, which is sentence [[1]]."),
          ("1324", "Sentence [[3]] begins 'It also', adding to an effect already described; the first effect, organising the material, is in sentence [[2]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 007 Medium, 4
pj("V01-E-007", "Education", "Open-book examinations do not lower the demand on students but shift it from recall to use.", "Medium",
   ["Open-book examinations are often assumed to be easy, as if allowing notes into the hall removed any need to study.",
    "Students who prepare on that assumption tend to discover their mistake within the first hour, leafing through pages for answers that are printed nowhere.",
    "Such answers are missing because a well-set paper of this kind asks not what a theorem states, which the book would supply, but when it applies and what follows from it.",
    "The format does not lower the demand on students so much as move it, from remembering material to knowing how to use it."],
   "Sentence [[1]] states the common assumption that open-book papers are easy. Sentence [[2]] follows students who act 'on that assumption' and find the answers 'printed nowhere'. Sentence [[3]] explains why 'Such answers are missing': the paper tests application, not statement. Sentence [[4]] generalises: the demand is moved from recall to use.",
   "Placing sentence [[3]] straight after sentence [[1]] because it describes the paper, although 'Such answers are missing' refers to the answers students fail to find in sentence [[2]].",
   "V01E-open-book-exams", "The explanation must follow the experience it explains, and the conclusion must follow the explanation; one middle sentence describes the exam and looks movable.",
   traps=[("1324", "Sentence [[3]] begins 'Such answers are missing', which refers to the 'answers that are printed nowhere' in sentence [[2]]."),
          ("1243", "Sentence [[4]] says the demand is moved 'to knowing how to use it', which is a generalisation of the point in sentence [[3]] that the paper asks when a theorem applies; without [[3]] the conclusion is unsupported, and [[3]] cannot follow the conclusion.")])

# ------------------------------------------------------------------ 008 Medium, 5
pj("V01-E-008", "Education", "Early teaching in the home language builds the skills that later make a second language learnable.", "Medium",
   ["In many multilingual countries, children begin school in a language they rarely hear at home, on the theory that early immersion is the quickest route to fluency.",
    "The theory has intuitive appeal, but it overlooks what a child must accomplish in the first years of school besides acquiring a language.",
    "Those years are when children learn to read, to reason with numbers and to ask questions, and each of these is harder in a language they only half understand.",
    "A child taught first in the home language can build these skills on secure ground and later carry them over into the second language.",
    "Far from delaying the second language, then, the home language becomes the bridge by which a child crosses into it."],
   "Sentence [[1]] describes the practice and 'the theory' of early immersion. Sentence [[2]] grants the theory's appeal but says it overlooks what children must do in 'the first years of school'. Sentence [[3]] picks up 'Those years' and names the skills learnt in them. Sentence [[4]] refers to 'these skills' and shows they can be carried over. Sentence [[5]] concludes ('then') that the home language is a bridge, an image that depends on the carrying over in [[4]].",
   "Placing sentence [[5]] before sentence [[4]] as a summary of the case against immersion, although 'the bridge' it describes is the transfer of skills that only sentence [[4]] states.",
   "V01E-mother-tongue-instruction", "The last two sentences must be ordered by the idea: the transfer of skills has to be stated before the home language can be called a bridge into the second.",
   traps=[("12354", "Sentence [[5]] calls the home language a bridge into the second, which presupposes the claim in sentence [[4]] that skills built in it are carried over; sentence [[3]] shows only the cost of immersion."),
          ("13245", "Sentence [[3]] begins 'Those years', referring to 'the first years of school' that sentence [[2]] introduces.")])

# ------------------------------------------------------------------ 009 Easy, 4
pj("V01-E-009", "Education", "Handwritten notes, though shorter, may aid memory because writing by hand forces selection and rephrasing.", "Easy",
   ["Students who type their lecture notes can usually record far more of what is said than students who write by hand.",
    "That speed, however, tempts typists to take down the lecturer's words almost verbatim, without pausing to think about them.",
    "Those writing by hand cannot keep up, and so they are forced to choose what matters and to put it into their own words.",
    "This selection and rephrasing is a form of thinking about the material, which may be why handwritten notes, though shorter, are sometimes remembered better."],
   "Sentence [[1]] states the advantage of typing: more is recorded. Sentence [[2]] turns ('That speed, however') to its drawback, verbatim copying. Sentence [[3]] contrasts the handwriters, who must select and rephrase. Sentence [[4]] refers to 'This selection and rephrasing' from [[3]] and draws the conclusion about memory.",
   "Placing sentence [[3]] straight after sentence [[1]], which leaves 'That speed' in sentence [[2]] separated from the speed it refers to and puts the drawback of typing just before a conclusion about handwriting.",
   "V01E-handwritten-lecture-notes", "The chain is carried by 'That speed', the contrast with handwriters and 'This selection and rephrasing'.",
   traps=[("1324", "Sentence [[4]] begins 'This selection and rephrasing', which refers to what handwriters do in sentence [[3]]; with [[2]] in between, the reference is broken."),
          ("1243", "Sentence [[4]] speaks of 'This selection and rephrasing' before any selection has been mentioned; only sentence [[3]] describes it.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 010 Difficult, 4
pj("V01-E-010", "Education", "Worked solutions help beginners but hinder those who already command the patterns, so the best method depends on the learner.", "Difficult",
   ["For beginners in algebra, studying a fully worked solution is often more instructive than attempting the same problem unaided.",
    "Lacking the patterns that would guide them, they spend their attention on fruitless search and have little left for noticing why a method works.",
    "Learners who already command the patterns are in the opposite position, since every worked step repeats what they could have supplied themselves.",
    "For them, reading the solution becomes a distraction, and attempting the problem unaided is the better exercise."],
   "Sentence [[1]] states that beginners gain from worked solutions. Sentence [[2]] explains why: 'they', the beginners, lack the patterns and waste attention in search. Sentence [[3]] turns to learners who already have the patterns, who are 'in the opposite position'. Sentence [[4]] says 'For them' attempting the problem is better, which can only describe the experienced learners of [[3]], since it reverses what [[1]] says of beginners.",
   "Placing sentence [[4]] after sentence [[2]] because 'For them' seems to refer to the beginners just discussed, although its claim, that reading the solution is a distraction, contradicts sentence [[1]].",
   "V01E-worked-examples", "Order depends mainly on the logic of the idea: 'them' and 'they' could grammatically point to either group, so the reader must use what is claimed about each group to decide.",
   traps=[("1243", "Read after sentence [[2]], 'For them' would refer to beginners, and sentence [[4]] would then say that beginners should not study worked solutions, contradicting sentence [[1]]."),
          ("1342", "Sentence [[2]] says 'they' lack the patterns, but after [[3]] and [[4]] 'they' would refer to learners who already command the patterns.")],
   exams=D)

# ------------------------------------------------------------------ 011 Medium, 4
pj("V01-E-011", "Health and medicine", "The nocebo effect makes informing patients of side effects partly harmful, and the answer lies in framing rather than silence.", "Medium",
   ["Patients warned that a drug may cause headaches or nausea report those symptoms more often than patients given no warning, even when their pills contain no active ingredient.",
    "This nocebo effect places doctors in an awkward position, because the duty to inform patients of risks seems to produce some of the very harms described.",
    "Withholding the warnings is hardly an answer, since it would sacrifice the patient's right to decide about treatment with full knowledge.",
    "A more promising approach is to change how risks are framed, for instance by noting that most people taking the drug feel no side effects at all."],
   "Sentence [[1]] describes the observation that warnings produce symptoms. Sentence [[2]] names it ('This nocebo effect') and states the dilemma for doctors. Sentence [[3]] rejects one way out, withholding warnings. Sentence [[4]] offers 'A more promising approach', a comparative that needs the rejected option in [[3]].",
   "Placing sentence [[4]] before sentence [[3]] because it proposes a solution to the dilemma, although 'more promising' compares it with the option rejected in [[3]].",
   "V01E-nocebo-effect", "A dilemma is posed, one answer rejected and a better one offered; the comparative 'more promising' fixes the last pair.",
   traps=[("1243", "Sentence [[4]] calls its proposal 'A more promising approach', which needs a less promising one already on the table; that is the withholding of warnings in sentence [[3]]."),
          ("2134", "Sentence [[2]] begins 'This nocebo effect', which must refer back to the effect described in sentence [[1]].")])

# ------------------------------------------------------------------ 012 Easy, 5
pj("V01-E-012", "Health and medicine", "Surgical checklists protect what experts already know from ordinary lapses of attention.", "Easy",
   ["Surgical teams are made up of highly trained people, so it can seem odd to ask them to work through a simple checklist before an operation.",
    "Yet many surgical errors arise not from ignorance but from small omissions, such as failing to confirm which side of the body is to be operated on.",
    "These are exactly the steps that experts, working under pressure and confident in their routine, are most likely to skip.",
    "A checklist catches such lapses by making the routine explicit and requiring each member of the team to confirm it aloud.",
    "Its value, then, lies not in teaching surgeons anything new but in protecting what they already know from ordinary failures of attention."],
   "Sentence [[1]] raises the puzzle of checklists for experts. Sentence [[2]] answers it ('Yet'): errors come from small omissions. Sentence [[3]] says 'These are exactly the steps' experts skip. Sentence [[4]] shows how 'A checklist catches such lapses'. Sentence [[5]] concludes ('then') with the checklist's value.",
   "Placing sentence [[4]] before sentence [[3]], although 'such lapses' refers to the skipped steps that sentence [[3]] describes.",
   "V01E-surgical-checklists", "Clear links ('Yet', 'These are exactly the steps', 'such lapses', 'then') fix the order.",
   traps=[("12435", "Sentence [[4]] says the checklist catches 'such lapses', but the lapses, steps that experts under pressure skip, are described in sentence [[3]]."),
          ("13245", "Sentence [[3]] begins 'These are exactly the steps', which refers to the omissions listed in sentence [[2]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 013 Medium, 4
pj("V01-E-013", "Health and medicine", "Many patients stop long-term medicines by reasonable inference from what they feel, so explanation matters more than reminders.", "Medium",
   ["A large share of patients prescribed long-term medicines stop taking them sooner than their doctors intended.",
    "This is often blamed on forgetfulness, yet many of those who stop do so deliberately, and for reasons that seem sound from where they stand.",
    "A patient taking a drug for high blood pressure, for example, may feel no different with it than without it, and conclude that the pills are doing nothing.",
    "Given that experience, stopping is a reasonable inference rather than a lapse, which suggests that the remedy lies less in reminders than in explanation."],
   "Sentence [[1]] states the problem of patients stopping their medicines. Sentence [[2]] rejects the usual blame on forgetfulness: many stop deliberately, for reasons 'that seem sound from where they stand'. Sentence [[3]] illustrates such a reason ('for example'). Sentence [[4]] refers to 'that experience', feeling no benefit, and draws the conclusion that explanation, not reminders, is needed; 'reminders' answers the forgetfulness of [[2]].",
   "Placing sentence [[3]] straight after sentence [[1]] as an illustration of stopping, which makes the forgetfulness explanation in sentence [[2]] arrive after a case that has already refuted it.",
   "V01E-medication-adherence", "Order depends mainly on the logic of the idea: the example illustrates deliberate stopping, so it must follow the claim that stopping is deliberate, and the conclusion must answer the forgetfulness view.",
   traps=[("1324", "The example in sentence [[3]] illustrates a deliberate reason for stopping, which only sentence [[2]] introduces; placed first, it would precede the forgetfulness view it is meant to refute."),
          ("1243", "Sentence [[4]] begins 'Given that experience', which needs the experience of feeling no different on the drug described in sentence [[3]]; sentence [[2]] describes no experience.")])

# ------------------------------------------------------------------ 014 Difficult, 4
pj("V01-E-014", "Health and medicine", "The link between loneliness and ill health may run from illness to isolation, but where loneliness predicts later illness it deserves attention as a cause.", "Difficult",
   ["People who report persistent loneliness tend, on average, to be in poorer health than people who do not.",
    "It would be rash to conclude from this alone that loneliness causes illness, since illness can itself confine people to their homes and thin out their social lives.",
    "Studies that follow the same people over many years help here, because they can check whether loneliness at the start predicts illness that was not yet present.",
    "Where it does, the reverse explanation cannot be the whole story, and loneliness deserves attention as a possible cause of ill health rather than merely its by-product."],
   "Sentence [[1]] reports the association between loneliness and poor health. Sentence [[2]] warns against reading it causally, because the influence could run from illness to isolation. Sentence [[3]] says long-term studies 'help here', that is, with separating the two directions, by checking whether early loneliness predicts later illness. Sentence [[4]] begins 'Where it does', which needs the prediction tested in [[3]], and concludes that 'the reverse explanation', illness causing isolation from [[2]], cannot be the whole story.",
   "Placing sentence [[3]] straight after sentence [[1]] because studies seem to follow naturally from a finding, which leaves 'help here' with no problem to help with; the problem of direction is raised only in sentence [[2]].",
   "V01E-loneliness-health-risk", "Order depends mainly on the logic of the idea: the reader must see that the long-term studies address the problem of causal direction, and that 'the reverse explanation' names the illness-to-isolation story.",
   traps=[("1324", "Sentence [[3]] says such studies 'help here', but before sentence [[2]] there is no difficulty to help with; the finding in [[1]] has not yet been questioned."),
          ("1243", "Sentence [[4]] begins 'Where it does', and the only thing it can refer to is loneliness predicting later illness, which is introduced in sentence [[3]].")],
   exams=D)

# ------------------------------------------------------------------ 015 Medium, 4
pj("V01-E-015", "Cities and geography", "Closing shopping streets to cars can raise trade, despite shopkeepers' fears, where enough people live or work nearby.", "Medium",
   ["When a city proposes closing a shopping street to cars, the loudest objections usually come from the shopkeepers who trade on it.",
    "Their fear is understandable: customers who cannot park outside, they reason, will simply take their custom elsewhere.",
    "Yet traders often overestimate how many of their customers arrive by car, and underestimate how much those on foot spend over repeated visits.",
    "A street that is pleasant to linger in can therefore gain trade, although the gain is likeliest where enough people already live or work within walking distance."],
   "Sentence [[1]] introduces the shopkeepers' objection to closing a street to cars. Sentence [[2]] explains 'Their fear'. Sentence [[3]] replies ('Yet') that traders misjudge where their custom comes from. Sentence [[4]] concludes ('therefore') that such a street can gain trade, with a qualification about nearby residents and workers.",
   "Ending with sentence [[3]] after sentence [[4]] because it reads like a closing correction, although the 'therefore' of [[4]] rests on the misjudgement it describes.",
   "V01E-pedestrianised-shopping-streets", "A concession, a reply and a qualified conclusion; the 'Yet' sentence could seem to attach to the conclusion.",
   traps=[("1243", "Sentence [[4]] says a pedestrian street can 'therefore' gain trade, but the reason, that traders overestimate car-borne customers, comes only in sentence [[3]]; and 'Yet' in [[3]] would then contradict the conclusion it supports."),
          ("2134", "Sentence [[2]] begins 'Their fear', which needs the shopkeepers and their objection introduced in sentence [[1]].")])

# ------------------------------------------------------------------ 016 Easy, 4
pj("V01-E-016", "Cities and geography", "Benches designed to prevent lying down are aimed at people with nowhere to sleep and hide rather than solve a problem.", "Easy",
   ["Many cities have installed benches with armrests spaced along their length or seats tilted at an uncomfortable angle.",
    "Such designs are usually justified as ways of keeping public seating available to everyone who needs it.",
    "In practice, their chief effect is to stop people from lying down, which means they are aimed above all at those with nowhere else to sleep.",
    "Critics argue that this moves a social problem out of sight without doing anything to solve it."],
   "Sentence [[1]] describes the benches. Sentence [[2]] gives the usual justification for 'Such designs'. Sentence [[3]] contrasts it ('In practice') with their real effect, which targets people with nowhere to sleep. Sentence [[4]] reports the critics' view that 'this' hides a social problem, which needs the effect described in [[3]].",
   "Placing sentence [[4]] after sentence [[2]], although the 'social problem' and the 'this' it criticises appear only in sentence [[3]].",
   "V01E-hostile-bench-design", "The links 'Such designs', 'In practice' and 'this' fix the order.",
   traps=[("1243", "Sentence [[4]] says 'this moves a social problem out of sight', but the social problem, people with nowhere to sleep, is introduced only in sentence [[3]]."),
          ("1324", "Sentence [[3]] begins 'In practice', contrasting with a stated justification; the justification is given in sentence [[2]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 017 Medium, 5
pj("V01-E-017", "Cities and geography", "Mountain passes concentrated trade, enriching the towns beside them but making their wealth insecure.", "Medium",
   ["Before railways and paved roads, a mountain range could be crossed by loaded animals at only a few places where the terrain allowed it.",
    "Traders from a wide region were therefore funnelled through the same narrow passes, whatever their origin or destination.",
    "Settlements at the foot of such passes could profit handsomely, supplying fresh animals, lodging and guides to every caravan that came through.",
    "The same concentration made them targets, however, since whoever held a pass could tax or block all the traffic that depended on it.",
    "The wealth of a pass town was thus never secure, resting as it did on a position that others had every reason to covet."],
   "Sentence [[1]] gives the geographical constraint: few crossing points. Sentence [[2]] draws the consequence ('therefore') that trade was funnelled through them. Sentence [[3]] shows the benefit to settlements beside 'such passes'. Sentence [[4]] turns ('however') to the danger created by 'The same concentration'. Sentence [[5]] concludes ('thus') that pass towns' wealth was insecure, which rests on the danger in [[4]].",
   "Placing sentence [[4]] before sentence [[3]] because both describe consequences of funnelling, although 'them' in sentence [[4]] refers to the settlements first introduced in [[3]] and 'however' contrasts with their profit.",
   "V01E-mountain-pass-trade-routes", "Order depends mainly on the logic of the idea: constraint, concentration, benefit, then the danger that the same concentration creates, and finally the insecurity that follows from benefit and danger together.",
   traps=[("12435", "Sentence [[4]] says the concentration 'made them targets, however', which needs the settlements and their profit from sentence [[3]] both as referent and as the thing contrasted."),
          ("12354", "Sentence [[5]] says the wealth was 'never secure' because others coveted the position, which depends on the point in sentence [[4]] that whoever held a pass controlled its traffic.")])

# ------------------------------------------------------------------ 018 Difficult, 5
pj("V01-E-018", "Cities and geography", "Every flat map sacrifices some property, so the sea chart's inflation of high latitudes is a trade-off, though misused as a picture of the world.", "Difficult",
   ["No flat map can show the curved surface of the earth without distortion; it can keep shapes true over small regions, or keep areas true, but never both at once.",
    "Every projection is therefore a choice about which property to sacrifice, and the right choice depends on what the map is meant to do.",
    "The projection long used for sea charts shows what such a choice involves: it keeps compass directions true, so that a sailor can follow a straight line on the chart at a constant bearing.",
    "The price is that lands far from the equator are drawn much larger than they really are, an exaggeration that grows steadily towards the poles.",
    "To fault the chart's makers for this exaggeration is to forget what the chart was for, though the fault is real when a navigator's tool hangs on classroom walls as a picture of the world."],
   "Sentence [[1]] states the constraint that every flat map distorts. Sentence [[2]] draws the consequence ('therefore'): a projection is a choice, made according to the map's purpose. Sentence [[3]] shows what 'such a choice' involves, which needs the choice named in [[2]]: the sea-chart projection keeps directions true because sailors need them. Sentence [[4]] names 'The price' of that choice, the enlargement of high latitudes. Sentence [[5]] refers to 'this exaggeration' and judges complaints about it, appealing to 'what the chart was for', the principle of [[2]].",
   "Moving sentence [[2]] after the example, as a general lesson drawn from it, which leaves 'such a choice' in sentence [[3]] without a choice to refer to and separates 'this exaggeration' in sentence [[5]] from sentence [[4]].",
   "V01E-map-projections", "The material is abstract, and the general principle that every projection is a choice looks equally at home before or after the sea-chart example; only the backward references of the example and of the closing verdict settle it.",
   traps=[("13425", "Sentence [[3]] speaks of 'such a choice', but the idea of a projection as a choice is introduced only in sentence [[2]]; placing [[2]] after the example also breaks the link between 'this exaggeration' in sentence [[5]] and the exaggeration described in sentence [[4]]."),
          ("12354", "Sentence [[5]] speaks of 'this exaggeration', which is described only in sentence [[4]]; before that the chart has been presented only as keeping directions true.")],
   exams=D)

# ------------------------------------------------------------------ 019 Medium, 4
pj("V01-E-019", "Philosophy and ethics", "Misleading with a true statement harms as much as lying, so any moral difference must lie elsewhere than in the harm.", "Medium",
   ["Many people feel that deceiving someone with a carefully chosen truth is less wrong than telling an outright lie.",
    "Asked whether a used car has given trouble, a seller who replies that 'it passed its inspection last month' may avoid any false statement while concealing a history of breakdowns.",
    "The buyer who trusts that answer ends up exactly as deceived, and exactly as much out of pocket, as one who had been told a direct falsehood.",
    "If the difference matters at all, it must lie in something other than the harm done, perhaps in how much of the work of being misled is left to the listener."],
   "Sentence [[1]] states the common view that misleading with a truth is less wrong than lying. Sentence [[2]] gives a case of misleading with a truth. Sentence [[3]] refers to 'that answer' and shows the buyer is harmed exactly as by a lie. Sentence [[4]] concludes that 'the difference', the one the common view asserts, cannot lie in the harm, a conclusion that rests on [[3]].",
   "Opening with the vivid case in sentence [[2]] and placing the general view after it, which separates 'that answer' in sentence [[3]] from the seller's reply it refers to.",
   "V01E-lying-versus-misleading", "Order depends mainly on the logic of the idea: the conclusion that the difference lies 'in something other than the harm' needs the case to have shown the harm to be equal.",
   traps=[("2134", "With sentence [[2]] first and sentence [[1]] second, 'that answer' in sentence [[3]] no longer follows the seller's reply, and the paragraph opens on an example before saying what it exemplifies."),
          ("1243", "Sentence [[4]] says the difference lies in 'something other than the harm done', but that the harm is the same is shown only in sentence [[3]].")])

# ------------------------------------------------------------------ 020 Easy, 4
pj("V01-E-020", "Philosophy and ethics", "The debate over paternalism sets prevention of harm against the right to run risks, and turns on where to draw the line.", "Easy",
   ["Paternalism is the practice of restricting people's choices for their own good, as when a law requires riders of motorcycles to wear helmets.",
    "Its defenders point out that people often choose badly when risks seem remote, and that a small restriction can prevent a great deal of suffering.",
    "Its critics reply that adults have a right to run risks with their own lives, even foolish ones, and that a state deciding their good for them treats them as children.",
    "Since neither side holds its view without exception, much of the debate turns on where to draw the line: few would ban mountain climbing, yet few object to warning labels on poisonous medicines."],
   "Sentence [[1]] defines paternalism. Sentence [[2]] gives the defenders' case ('Its defenders'). Sentence [[3]] gives the critics' answer; 'reply' shows it responds to the defence. Sentence [[4]] begins 'Since neither side holds its view without exception', which needs both sides already stated, and locates the crux of the debate.",
   "Placing the critics in sentence [[3]] before the defenders in sentence [[2]], although the critics 'reply' to a case that must already have been made.",
   "V01E-paternalism", "The definition, 'Its defenders', the critics' 'reply' and 'neither side' fix the order.",
   traps=[("1324", "Sentence [[3]] says the critics 'reply', which needs the defenders' case in sentence [[2]] to come first."),
          ("1423", "Sentence [[4]] says 'neither side' holds its view without exception, but the two sides are stated only in sentences [[2]] and [[3]]; placed second, it would refer to sides not yet named.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 021 Difficult, 5
pj("V01-E-021", "Philosophy and ethics", "Moral luck sets the principle that we are judged only for what we control against our harsher verdict on unlucky wrongdoers.", "Difficult",
   ["It is widely held that a person should be judged only for what lay within their control.",
    "Two hikers who each toss a lit match into dry grass are, on this principle, equally culpable, whatever happens next.",
    "Suppose one match fizzles out harmlessly while the other starts a blaze that destroys a neighbouring farm.",
    "Almost no one would then judge the two alike: the hiker whose match caught is condemned, and punished, far more severely than the other.",
    "The case leaves us choosing between a principle that seems obviously right and a response that seems just as hard to give up."],
   "Sentence [[1]] states the control principle. Sentence [[2]] applies it ('on this principle') to two equally careless hikers. Sentence [[3]] adds the difference in outcome, which the hikers did not control. Sentence [[4]] says that 'then', once the outcomes differ, we judge the two differently. Sentence [[5]] names the resulting dilemma between the principle and our response.",
   "Placing sentence [[4]] straight after sentence [[2]], as if the harsher verdict directly answered the principle, although the verdict depends on the different outcomes that only sentence [[3]] supplies.",
   "V01E-moral-luck", "Order depends mainly on the logic of the idea: the reader must see that the differing verdict presupposes differing outcomes, and that the dilemma requires both the principle and the response; the case can also be mistaken for an opener.",
   traps=[("12435", "Sentence [[4]] says no one would 'then' judge the two alike and singles out 'the hiker whose match caught', but before sentence [[3]] the hikers differ in nothing and no match has caught."),
          ("31245", "Sentence [[3]] cannot open the paragraph, since 'one match' and 'the other' need the two hikers and their matches introduced in sentence [[2]], and sentence [[2]] in turn needs 'this principle' from sentence [[1]].")],
   exams=D)

# ------------------------------------------------------------------ 022 Medium, 4
pj("V01-E-022", "Philosophy and ethics", "Because our choices decide who will exist, duties to future generations must be owed to whoever comes to live, not to particular people.", "Medium",
   ["It is often said that we owe obligations to people who will live centuries from now, though they cannot thank us or hold us to account.",
    "A puzzle arises because many of our larger choices, about where to build or how to use resources, will affect which particular people come to be born at all.",
    "A person who owes her very existence to such a choice can hardly complain that it harmed her, since without it she would never have lived.",
    "If the obligation survives this puzzle, it must be owed not to particular future individuals but to whoever comes to live, as a duty to leave them a world worth inheriting."],
   "Sentence [[1]] states the claim that we owe obligations to distant future people. Sentence [[2]] says 'A puzzle arises' because our choices decide who is born. Sentence [[3]] draws out the puzzle: a person who owes her existence to 'such a choice' cannot claim it harmed her. Sentence [[4]] refers to 'this puzzle' and says how the obligation could survive it.",
   "Placing sentence [[3]] before sentence [[2]] because it states the sharpest form of the problem, although 'such a choice' refers to the choices that sentence [[2]] says affect who is born.",
   "V01E-obligations-to-future-generations", "The puzzle is abstract, and the reader must see that the complaint of the person who owes her existence to a choice presupposes the identity-affecting choices that raise the puzzle.",
   traps=[("1324", "Sentence [[3]] speaks of owing one's existence 'to such a choice', and the choices that decide who is born are introduced in sentence [[2]]."),
          ("1243", "Sentence [[4]] answers 'this puzzle' by shifting the duty away from particular individuals, a move that makes sense only after sentence [[3]] shows that particular individuals cannot complain of harm.")])

# ------------------------------------------------------------------ 023 Easy, 4
pj("V01-E-023", "Psychology", "Experts forget what not knowing is like, which makes them skip steps; testing explanations on novices helps.", "Easy",
   ["Once we understand something well, it becomes surprisingly hard to imagine what it was like not to understand it.",
    "This is why experts so often make poor teachers of beginners, skipping steps that seem too obvious to mention.",
    "The steps are obvious only to them, however, because their own knowledge fills the gaps without their noticing.",
    "A useful remedy is to try an explanation on someone new to the subject, who will stumble exactly where the hidden steps were left out."],
   "Sentence [[1]] states the general difficulty of imagining one's former ignorance. Sentence [[2]] draws a consequence ('This is why'): experts skip steps. Sentence [[3]] explains that 'The steps' are obvious only to the experts. Sentence [[4]] offers a remedy, which relies on the 'hidden steps' described in [[2]] and [[3]].",
   "Placing sentence [[3]] before sentence [[2]], although 'The steps' and 'them' need the experts and the skipped steps that sentence [[2]] introduces.",
   "V01E-curse-of-knowledge", "The links 'This is why', 'The steps' and 'the hidden steps' fix the order.",
   traps=[("1324", "Sentence [[3]] refers to 'The steps' and to 'them', but neither the experts nor the steps they skip appear before sentence [[2]]."),
          ("1243", "Sentence [[3]] uses 'however' to correct the impression in [[2]] that the steps are obvious, so it must follow [[2]] directly; placed after the remedy, its 'them' would also point at the newcomer instead of the experts.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 024 Medium, 5
pj("V01-E-024", "Psychology", "Owners ask more for a mug than buyers offer because losing weighs more than gaining, so neither misjudges the mug.", "Medium",
   ["People who have just been given a mug typically ask more to part with it than people without one will offer for an identical mug.",
    "The gap is puzzling on a simple view of value, since a few minutes of ownership cannot have made the mug any more useful.",
    "One explanation is that giving something up registers as a loss, and losses weigh more heavily with us than gains of the same size.",
    "On this account, owner and buyer are not really pricing the same thing, since the owner is weighing the loss of a mug and the buyer the gain of one.",
    "Their figures differ, then, because they are answering different questions, and neither need be mistaken about the mug itself."],
   "Sentence [[1]] describes the gap between what owners ask and buyers offer. Sentence [[2]] calls 'The gap' puzzling. Sentence [[3]] offers 'One explanation', loss weighing more than gain. Sentence [[4]] applies it ('On this account'): owner and buyer value different things. Sentence [[5]] concludes ('then') that 'Their figures' differ because they answer different questions; 'Their' needs the owner and buyer named in [[4]], and the 'different questions' are the loss and the gain that [[4]] distinguishes.",
   "Placing sentence [[5]] before sentence [[4]] as a direct consequence of loss aversion, although the claim that the two answer different questions depends on the point in sentence [[4]] that they are weighing different prospects.",
   "V01E-endowment-effect", "Order depends mainly on the logic of the idea: the conclusion that the two parties answer different questions follows only once they are shown to be weighing a loss and a gain, so the last pair is fixed mainly by reasoning.",
   traps=[("12354", "Sentence [[5]] says the parties are 'answering different questions', which follows from sentence [[4]], where they are shown to be weighing a loss and a gain; sentence [[3]] states only the general asymmetry, and 'Their figures' needs the owner and buyer of [[4]]."),
          ("13245", "Sentence [[3]] offers 'One explanation', which needs a puzzle to explain; the gap is called puzzling only in sentence [[2]].")])

# ------------------------------------------------------------------ 025 Difficult, 4
pj("V01-E-025", "Psychology", "Much chronic delay is not a planning failure but a trade of immediate relief for later cost, which better schedules do not touch.", "Difficult",
   ["Chronic delay is commonly diagnosed as a failure of planning, and the usual cures are calendars, deadlines and lists.",
    "The diagnosis fits poorly those habitual delayers who can say exactly when a task is due and how long it will take, yet put it off regardless.",
    "Their difficulty is that the task stirs boredom, self-doubt or fear of judgement, and delay relieves these feelings at once, while its costs arrive only later.",
    "Remedies that merely improve the schedule leave this bargain intact, which may be why some people keep buying new planners without delaying any less."],
   "Sentence [[1]] states the usual diagnosis of delay as poor planning. Sentence [[2]] says 'The diagnosis fits poorly' delayers who plan well yet still delay. Sentence [[3]] explains 'Their difficulty': delay buys immediate relief from bad feelings at a later cost. Sentence [[4]] calls this trade 'this bargain' and concludes that better schedules leave it intact.",
   "Placing sentence [[4]] straight after sentence [[2]] because both concern the failure of planning remedies, although 'this bargain' names the trade of relief now for cost later that only sentence [[3]] describes.",
   "V01E-procrastination-and-mood", "Order depends mainly on the logic of the idea: 'this bargain' is never named as such, so the reader must recognise the relief-now, cost-later trade described in the 'Their difficulty' sentence as the bargain the remedies fail to touch.",
   traps=[("1243", "Sentence [[4]] says scheduling remedies leave 'this bargain' intact, but the bargain, immediate relief from bad feelings in exchange for later costs, is set out only in sentence [[3]]."),
          ("1324", "Sentence [[3]] begins 'Their difficulty', and the only people it can refer to are the habitual delayers introduced in sentence [[2]].")],
   exams=D)
