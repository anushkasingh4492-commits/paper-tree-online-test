import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DX = ("CAT", "XAT")

# 001 -------------------------------------------------------------------------------------------
pj("V01-N-001", "Science and environment",
   "Seed vaults preserve old crop varieties but freeze their evolution, so they should complement farmers who keep varieties growing.", "Easy",
   ["Crop seed vaults store frozen samples of thousands of plant varieties, many of which are no longer grown by any farmer.",
    "The reasoning behind them is simple: a variety that has vanished from the fields may one day carry a trait, such as drought tolerance, that breeders urgently need.",
    "Yet a seed kept in a freezer is cut off from the pests, climates and growers that shaped it, and so it stops adapting.",
    "For this reason, many agronomists argue that vaults should support, not replace, the farmers who keep old varieties alive in their fields."],
   "Sentence [[1]] introduces crop seed vaults and what they hold. Sentence [[2]] gives 'the reasoning behind them', where 'them' needs the vaults of sentence [[1]]. Sentence [[3]] opens with 'Yet' and states the limitation: a frozen seed stops adapting. Sentence [[4]] begins 'For this reason' and draws the conclusion that only follows from that limitation, namely that living fields must continue alongside the vaults.",
   "Putting sentence [[4]] straight after sentence [[2]], although the case for keeping varieties alive in fields rests on the problem raised in sentence [[3]], not on the rationale for vaults.",
   "V01N-crop-seed-vaults",
   "The opener is clear and 'them', 'Yet' and 'For this reason' fix every link.",
   cognitive="Understanding",
   traps=[("1243", "Sentence [[4]] says vaults should not replace living fields; that conclusion follows from the frozen seed ceasing to adapt in sentence [[3]], so it cannot precede it.")])

# 002 -------------------------------------------------------------------------------------------
pj("V01-N-002", "Technology",
   "Flight data recorders let investigators reconstruct crashes, and the lessons drawn feed back into safety rules.", "Easy",
   ["After an airliner crashes, investigators search the wreckage first for its flight data recorder, a box built to survive fire, impact and deep water.",
    "Throughout every flight the device logs hundreds of measurements, from engine temperature to the position of each control surface.",
    "These records allow investigators to reconstruct the final minutes in detail, even when no one on board survives to describe what happened.",
    "The lessons drawn from such reconstructions are then turned into new rules and training, which is one reason air travel has grown steadily safer."],
   "Sentence [[1]] introduces the flight data recorder. Sentence [[2]] describes what 'the device' logs. Sentence [[3]] refers to 'These records', the logged measurements of sentence [[2]], and says what they make possible. Sentence [[4]] refers to 'such reconstructions' from sentence [[3]] and says how their lessons are used.",
   "Placing sentence [[3]] before sentence [[2]] because both concern investigators, which leaves 'These records' with nothing to refer to.",
   "V01N-flight-data-recorders",
   "Each sentence names something introduced by the one before it ('the device', 'These records', 'such reconstructions').",
   cognitive="Understanding",
   traps=[("1324", "Sentence [[3]] speaks of 'These records' before any record has been described; the measurements it refers to appear only in sentence [[2]].")])

# 003 -------------------------------------------------------------------------------------------
pj("V01-N-003", "Arts and literature",
   "A concert hall's sound depends on the timing and amount of reflected sound, which architects balance.", "Easy",
   ["A concert hall is judged not only by how it looks but, above all, by how it sounds to a listener in an ordinary seat.",
    "Sound reaches that listener twice: directly from the stage, and a fraction of a second later as reflections from the walls and ceiling.",
    "If the reflections arrive too late, the music turns muddy; if there are too few of them, it sounds thin and dry.",
    "Architects therefore shape surfaces and choose materials with great care, aiming at a balance between clarity and warmth."],
   "Sentence [[1]] introduces the subject, how a hall sounds to a listener. Sentence [[2]] refers to 'that listener' and introduces reflections. Sentence [[3]] describes what goes wrong when 'the reflections' are badly timed or too few. Sentence [[4]] draws the practical consequence with 'therefore': architects must balance them.",
   "Opening with sentence [[2]] because it explains the physics, although 'that listener' needs the listener introduced in sentence [[1]].",
   "V01N-concert-hall-acoustics",
   "Back-references ('that listener', 'the reflections') and 'therefore' make the chain direct.",
   cognitive="Understanding",
   traps=[("2134", "Sentence [[2]] cannot open because 'that listener' points back to the listener in an ordinary seat named in sentence [[1]].")])

# 004 -------------------------------------------------------------------------------------------
pj("V01-N-004", "Language and media",
   "Subtitling and dubbing each trade one kind of loss for another, and habit decides which an audience accepts.", "Easy",
   ["Countries differ sharply in how they present foreign films and television: some prefer subtitles, while others replace the original voices through dubbing.",
    "Subtitles keep the actors' own performances, but they ask viewers to read quickly, often at the cost of missing details in the picture.",
    "Dubbing, by contrast, frees the eye but substitutes a new voice, which may match neither the face nor the feeling of the original.",
    "Neither method is simply better, then; each trades one kind of loss for another, and habit largely decides which loss an audience will accept."],
   "Sentence [[1]] introduces the two practices. Sentence [[2]] takes subtitles first. Sentence [[3]] turns to dubbing 'by contrast', which presupposes that subtitles have already been discussed. Sentence [[4]] concludes with 'then' that neither method is better, a verdict that needs both descriptions before it.",
   "Treating sentences [[2]] and [[3]] as interchangeable, although 'by contrast' ties the dubbing sentence to a preceding account of subtitles.",
   "V01N-subtitles-versus-dubbing",
   "The general opener and the contrast marker settle the order quickly.",
   cognitive="Understanding",
   traps=[("1324", "Sentence [[3]] says 'Dubbing, by contrast'; placed before sentence [[2]] it has nothing to contrast with, since sentence [[1]] only names both practices.")])

# 005 -------------------------------------------------------------------------------------------
pj("V01-N-005", "Education",
   "Arguing an assigned side in school debating is better seen as training in intellectual sympathy than in insincerity.", "Easy",
   ["Many schools run debating societies in which students argue for positions assigned to them, whatever they personally believe.",
    "Critics say that this practice teaches young people to value clever argument over honest conviction.",
    "Supporters reply that defending an unfamiliar view forces students to understand it from the inside, which is the first step towards judging it fairly.",
    "On this account, debating is less a training in insincerity than an exercise in intellectual sympathy."],
   "Sentence [[1]] describes the practice of arguing assigned positions. Sentence [[2]] gives the critics' objection to 'this practice'. Sentence [[3]] gives the supporters' 'reply', which must follow the objection it answers. Sentence [[4]] begins 'On this account', the supporters' account, and restates their view as a conclusion.",
   "Placing the supporters' reply in sentence [[3]] before the critics' objection in sentence [[2]], although one cannot reply to a charge that has not yet been made.",
   "V01N-school-debating-societies",
   "Objection, reply and 'On this account' give a standard and well-signalled sequence.",
   cognitive="Understanding",
   traps=[("1324", "Sentence [[3]] is a reply; before sentence [[2]] it answers nothing, and 'insincerity' in sentence [[4]] then echoes a charge made only after the defence.")])

# 006 -------------------------------------------------------------------------------------------
pj("V01-N-006", "Health and medicine",
   "A fixed daily step target hides the fact that the first extra steps matter most, so increases should be rewarded.", "Easy",
   ["Fitness apps commonly set a single daily step target and congratulate their users only when they reach it.",
    "Such a target is easy to remember, but it invites the belief that walking which falls short of it brings no benefit at all.",
    "For a sedentary person, however, that belief is badly wrong: the first few thousand extra steps are likely to matter far more than the last few hundred before the goal.",
    "A better message, then, might reward any increase over a person's usual level rather than a fixed and arbitrary line."],
   "Sentence [[1]] introduces the single step target. Sentence [[2]] refers to 'Such a target' and names the false belief it invites. Sentence [[3]] says 'that belief', the belief named in sentence [[2]], is wrong. Sentence [[4]] proposes, with 'then', a better message that follows from the counter-argument.",
   "Ending with sentence [[3]] after sentence [[4]], although the proposal in sentence [[4]] is drawn from the point about the first extra steps and so must come after it.",
   "V01N-daily-step-count-targets",
   "'Such a target', 'however' and 'then' fix the order once the opener is identified.",
   cognitive="Understanding",
   traps=[("1243", "Sentence [[4]] offers a remedy with 'then', but the reason for rewarding any increase is given only in sentence [[3]], so the remedy cannot come first.")])

# 007 -------------------------------------------------------------------------------------------
pj("V01-N-007", "Science and environment",
   "Legumes enrich the soil with nitrogen captured from the air, which explains the old practice of rotating cereals with pulses.", "Easy",
   ["Nitrogen makes up most of the air around every plant, yet most crops cannot use it in that form and must draw it from the soil instead.",
    "Plants of the pea and bean family are an exception, because bacteria living in small swellings on their roots convert the nitrogen of the air into a form the plant can use.",
    "When these plants die back or are ploughed in, part of that captured nitrogen is left behind in the soil.",
    "A wheat or rice crop sown in the same field the following season can draw on this store, and so needs less fertiliser than it otherwise would.",
    "This is why farmers in many regions have alternated cereals with pulses for centuries, long before anyone could explain what the roots were doing."],
   "Sentence [[1]] states the general problem: crops cannot use the nitrogen of the air. Sentence [[2]] names 'an exception', which needs the general rule of sentence [[1]] before it. Sentence [[3]] refers to 'these plants' and 'that captured nitrogen' from sentence [[2]]. Sentence [[4]] says the next crop draws on 'this store', the nitrogen left in the soil in sentence [[3]]. Sentence [[5]] explains the farming practice with 'This is why', which needs the benefit to the following cereal crop described in sentence [[4]].",
   "Placing sentence [[5]] straight after sentence [[3]] because both seem to sum up the value of legumes, although the practice of alternating cereals with pulses is explained only by the benefit to the next cereal crop in sentence [[4]].",
   "V01N-legume-nitrogen-fixation",
   "Five sentences, but each is tied to the previous one by 'an exception', 'these plants', 'this store' or 'This is why'.",
   cognitive="Understanding",
   traps=[("12354", "Sentence [[4]] draws on 'this store', which is the nitrogen left in the soil in sentence [[3]]; placed after sentence [[5]], it is cut off from that referent, and 'This is why' would then come before the benefit to cereals that it explains."),
          ("21345", "Sentence [[2]] calls legumes 'an exception', which needs the general rule of sentence [[1]] that crops cannot use the nitrogen of the air.")])

# 008 -------------------------------------------------------------------------------------------
pj("V01-N-008", "Science and environment",
   "A sunken whale carcass feeds a succession of deep-sea communities, from scavengers to bone bacteria.", "Medium",
   ["When a whale dies in the open ocean, its body usually sinks to the deep seafloor, where food is otherwise extremely scarce.",
    "Large scavengers such as hagfish and sleeper sharks arrive first, stripping away most of the soft tissue within months.",
    "With the flesh gone, smaller animals move in to colonise the exposed bones and the sediment enriched by the scavengers' leftovers.",
    "Long after that, bacteria begin to break down the fats stored inside the bones themselves, sustaining a distinctive community for decades."],
   "Sentence [[1]] sets the scene: a carcass reaching a food-poor seafloor. The rest is a succession that follows from what each stage consumes. Sentence [[2]] has large scavengers arrive 'first' and remove the soft tissue. Sentence [[3]] can only come next, since its animals colonise bones that are exposed only once 'the flesh' is gone and feed on 'the scavengers' leftovers'. Sentence [[4]] describes the last stage, bacteria feeding on fats inside the bones themselves, 'Long after that'.",
   "Placing the bacteria of sentence [[4]] before the bone colonisers of sentence [[3]] because both concern the bones, although the fats inside the bones are the last resource to be used.",
   "V01N-whale-fall-ecosystems",
   "Order depends mainly on the logic of ecological succession: soft tissue, then exposed bones and sediment, then the fats within the bones.",
   cognitive="Analysis",
   traps=[("1243", "Sentence [[3]] needs 'the flesh gone' and 'the scavengers' leftovers' to have just been described; after sentence [[4]] the narrative would jump back decades."),
          ("1324", "Sentence [[3]] says the flesh is already gone and mentions the scavengers' leftovers, so it cannot come before the scavengers of sentence [[2]] arrive.")])

# 009 -------------------------------------------------------------------------------------------
pj("V01-N-009", "Technology",
   "Frequent update prompts train users to postpone them, which attackers exploit, so updates may be best installed silently.", "Medium",
   ["Software companies release security updates frequently, and each one asks users to stop what they are doing and restart their devices.",
    "Faced with constant interruptions, many people learn to postpone updates by reflex, without reading what they fix.",
    "The habit is dangerous precisely because attackers study published fixes to learn which weaknesses remain open on machines that have not been patched.",
    "Since delay is so costly, some designers argue that the safest update is the one the user never notices, installed quietly while the device is idle."],
   "Sentence [[1]] introduces frequent updates that interrupt work. Sentence [[2]] describes the user response those 'constant interruptions' produce. Sentence [[3]] explains why 'The habit' of postponing is dangerous. Sentence [[4]] proposes silent installation 'Since delay is so costly', a premise established only by sentence [[3]].",
   "Putting sentence [[4]] right after sentence [[2]] on the thought that postponement alone motivates silent updates, although the cost of delay that sentence [[4]] relies on is shown only in sentence [[3]].",
   "V01N-software-update-fatigue",
   "Order depends mainly on the logic of the idea: a behaviour, why it is harmful, and a design response that presupposes the harm.",
   cognitive="Analysis",
   traps=[("1243", "Sentence [[4]] rests on 'delay is so costly', but the cost of delay is established only by sentence [[3]]; and sentence [[3]]'s 'The habit' would then refer back past the proposal.")])

# 010 -------------------------------------------------------------------------------------------
pj("V01-N-010", "Arts and literature",
   "Publishing a dead novelist's unfinished manuscript is best done with a frank account of its state.", "Medium",
   ["When a novelist dies leaving a manuscript unfinished, heirs and publishers must decide whether readers should ever see it.",
    "Publishing the fragment honours the labour that went into it and may satisfy a genuine public interest in the writer's last work.",
    "Against this, the writer may have regarded the draft as a failure, and an author's silence on the matter is not the same as consent.",
    "The most defensible course may be to publish with a clear account of the manuscript's condition, so that readers judge a draft as a draft."],
   "Sentence [[1]] poses the decision. Sentence [[2]] gives the case for publishing 'the fragment'. Sentence [[3]] opens 'Against this' and gives the case against, which must answer a case already made. Sentence [[4]] proposes a course that responds to both: it publishes, as sentence [[2]] urges, but with a clear account of the draft's state, which meets the worry of sentence [[3]] that a rejected draft will be taken as finished work.",
   "Ending with sentence [[3]] after sentence [[4]], although the compromise in sentence [[4]] is shaped by the objection and so must come after it.",
   "V01N-posthumous-unfinished-novels",
   "Order depends mainly on the logic of the argument: a dilemma, the case for, the case against, and a resolution that answers both.",
   cognitive="Analysis",
   traps=[("1243", "Sentence [[4]] already answers the worry that a draft may be mistaken for finished work; placed before sentence [[3]] it solves a problem not yet raised, and 'Against this' would then oppose the compromise rather than the case for publishing."),
          ("1324", "Sentence [[3]] begins 'Against this' but sentence [[1]] states only a question, not a position that can be argued against.")])

# 011 -------------------------------------------------------------------------------------------
pj("V01-N-011", "Language and media",
   "A brand name that becomes the everyday word for a product risks losing its legal protection.", "Medium",
   ["Some brand names become so successful that people begin using them for every product of the same kind, whoever made it.",
    "This might seem the ultimate commercial triumph, yet it carries a real danger for the company that owns the name.",
    "In many legal systems, a trademark that has come to mean the general product, rather than one maker's version of it, can lose its protection.",
    "To keep that protection, firms sometimes run advertisements reminding the public that their name is a brand and should be followed by the ordinary word for the thing."],
   "Sentence [[1]] describes brand names becoming generic. Sentence [[2]] calls 'This' a triumph that carries a danger, without yet saying what the danger is. Sentence [[3]] specifies it: loss of legal protection. Sentence [[4]] begins 'To keep that protection', which refers to the legal protection named in sentence [[3]], and the advertisements it describes make sense only as a defence against that specific risk.",
   "Placing sentence [[4]] before sentence [[3]], since 'a real danger' in sentence [[2]] seems enough to explain the advertisements; but 'that protection' has no referent until sentence [[3]] mentions it, and the advertisements answer only the specific risk of the name coming to mean the general product.",
   "V01N-generic-trademark-brand-names",
   "The danger is announced before it is specified, and the firms' response fits only the specified danger.",
   cognitive="Analysis",
   traps=[("1243", "Sentence [[4]] speaks of 'that protection', which is first mentioned in sentence [[3]]; the remedy it describes answers that specific legal risk, so it cannot precede it.")])

# 012 -------------------------------------------------------------------------------------------
pj("V01-N-012", "Education",
   "The belief in matching teaching to learning styles lacks support; methods should fit the content instead.", "Medium",
   ["A widely held belief in education is that each student learns best through a preferred channel, such as seeing, hearing or doing.",
    "The idea is appealing because it flatters teachers and learners alike: failure becomes a mismatch of style rather than a lack of effort or skill.",
    "Yet appealing as it is, the idea has generally failed when tested directly, since teaching students in their supposed style has not produced better results.",
    "What seems to matter more is the nature of the material, since a map is best learned by looking and a melody by listening, whoever the learner is.",
    "Teachers would therefore do better to match their methods to the content than to labels attached to individual students."],
   "Sentence [[1]] states the belief. Sentence [[2]] explains why 'The idea' appeals. Sentence [[3]] turns with 'Yet appealing as it is' to the evidence against it, a phrase that needs the appeal of sentence [[2]] to have been stated. Sentence [[4]] offers what matters 'more' than style, which presupposes that style has just been shown not to matter. Sentence [[5]] draws the practical conclusion with 'therefore', matching methods to content, which rests on sentence [[4]].",
   "Placing the appeal of sentence [[2]] after the evidence of sentence [[3]], although 'appealing as it is' in sentence [[3]] refers back to an appeal already explained, and sentence [[4]]'s 'What seems to matter more' must answer the failed test directly.",
   "V01N-learning-styles-myth",
   "Order depends mainly on the logic of a critique: belief, its appeal, the evidence against it, the alternative factor and the recommendation.",
   cognitive="Analysis",
   traps=[("13245", "Sentence [[3]] says 'appealing as it is', which needs the appeal explained in sentence [[2]]; and sentence [[4]]'s 'matter more' must follow the failed test directly, not the appeal of the belief."),
          ("12354", "Sentence [[5]] recommends matching methods to content, but the reason, that the material decides the best channel, is given only in sentence [[4]].")])

# 013 -------------------------------------------------------------------------------------------
pj("V01-N-013", "Health and medicine",
   "Sham surgery trials seem to break a doctor's duty, but they have exposed operations that do no more than the fake.", "Medium",
   ["Testing a new drug against a dummy pill is routine, but testing an operation against a fake one raises far harder questions.",
    "In such a sham procedure, patients receive anaesthesia and small incisions, yet the step of the surgery thought to help them is left out.",
    "Critics object that this exposes people to real risks with no chance of benefit, which seems to violate a doctor's first duty.",
    "Defenders answer that some widely used operations, once compared with shams, have turned out to help patients no more than the fake version did."],
   "Sentence [[1]] contrasts dummy pills with fake operations. Sentence [[2]] describes 'such a sham procedure', the fake operation of sentence [[1]]. Sentence [[3]] gives the critics' objection to 'this'. Sentence [[4]] gives the defenders' 'answer', which must follow the objection it answers.",
   "Opening with sentence [[2]] because it defines the procedure, although 'such a sham procedure' refers back to the fake operation introduced in sentence [[1]].",
   "V01N-sham-surgery-trials",
   "The opener must be found from 'such', and the objection must precede the answer.",
   cognitive="Understanding",
   traps=[("2134", "Sentence [[2]] begins 'In such a sham procedure', which needs the fake operation of sentence [[1]] as its referent."),
          ("1243", "Sentence [[4]] is an answer from defenders; before sentence [[3]] there is no objection for it to answer.")])

# 014 -------------------------------------------------------------------------------------------
pj("V01-N-014", "Science and environment",
   "City birds sing higher to escape low-pitched traffic noise, though whether the shift is learned or inherited is unclear.", "Medium",
   ["Birds that live in noisy cities face a problem that their rural relatives do not: their songs must be heard above the rumble of traffic.",
    "Studies of several species have found that city birds tend to sing at a higher pitch than birds of the same species in quiet woodland.",
    "The shift makes sense, because traffic noise is concentrated at low frequencies, so a higher song is less likely to be drowned out.",
    "Less clear is whether such a useful adjustment is learned during each bird's life or inherited over generations, and both may be at work."],
   "Sentence [[1]] states the problem of being heard over traffic. Sentence [[2]] reports the observation that city birds sing higher. Sentence [[3]] explains why 'The shift' makes sense, linking the pitch change to the low frequencies of traffic. Sentence [[4]] turns to what remains open about 'such a useful adjustment', a phrase that presupposes sentence [[3]] has already shown why the higher pitch helps.",
   "Placing sentence [[4]] before sentence [[3]], since both comment on the change; but calling it 'such a useful adjustment' assumes its usefulness has been explained, which happens only in sentence [[3]].",
   "V01N-urban-birdsong-noise",
   "Order depends mainly on the logic of the idea: problem, finding, explanation of the finding, then the unresolved question.",
   cognitive="Analysis",
   traps=[("1243", "Sentence [[4]] calls the change 'such a useful adjustment', but its usefulness against low-frequency traffic noise is explained only in sentence [[3]], so sentence [[4]] must come after it.")])

# 015 -------------------------------------------------------------------------------------------
pj("V01-N-015", "Technology",
   "Hidden photo data is a useful but fallible clue for verifiers, to be weighed with evidence in the picture itself.", "Medium",
   ["Every digital photograph can carry hidden data recording when it was taken, with which device and sometimes where.",
    "Journalists checking images from social media have learned to treat this data as a useful first clue to whether a picture is what it claims to be.",
    "A clue, however, is not proof, because such data can be stripped out or rewritten with freely available tools.",
    "Equally, missing data says little on its own, since many platforms remove it automatically to protect the privacy of their users.",
    "The careful verifier therefore treats the hidden record, whether present or missing, as one witness among several, to be weighed against shadows, weather and landmarks in the picture itself."],
   "Sentence [[1]] introduces hidden photo data. Sentence [[2]] says journalists use 'this data' as a first clue. Sentence [[3]] picks up the word 'clue' and qualifies it with 'however': the data can be faked. Sentence [[4]] adds a second limitation with 'Equally': its absence proves nothing either. Sentence [[5]] concludes with 'therefore' that the record, 'whether present or missing', is one witness among several, which needs both limitations: present data can be faked (sentence [[3]]) and missing data proves nothing (sentence [[4]]).",
   "Putting sentence [[4]] before sentence [[3]]; but 'Equally' adds a second limitation and needs a first one before it, while after sentence [[2]] it would pair with the praise of the data as a clue.",
   "V01N-photo-metadata-provenance",
   "Two limitations must be ordered by 'however' and 'Equally', and the conclusion must follow both.",
   cognitive="Analysis",
   traps=[("12435", "Sentence [[4]] begins 'Equally', marking a second limitation; directly after sentence [[2]], which praises the data, there is no first limitation for it to match."),
          ("12354", "Sentence [[5]] treats the record 'whether present or missing' with caution, which needs sentence [[4]]'s point about missing data first; and 'Equally' in sentence [[4]] must pair with the limitation of sentence [[3]], not with the conclusion.")])

# 016 -------------------------------------------------------------------------------------------
pj("V01-N-016", "Arts and literature",
   "A literary prize serves readers more through its shortlist than through its single winner.", "Medium",
   ["Literary prizes are usually discussed in terms of their winners, but their shortlists may matter more to the reading public.",
    "A shortlist of five or six books gives undecided readers a manageable menu, and every title on it tends to find new readers.",
    "Only one of those books will win, and its victory rests on the verdict of a handful of judges whose tastes may be far from those of ordinary readers.",
    "Seen this way, the lasting service of a prize lies less in that one verdict than in directing attention towards a small group of books."],
   "Sentence [[1]] makes the claim that shortlists may matter more than winners. Sentence [[2]] explains how a shortlist helps readers. Sentence [[3]] refers to 'those books', the five or six of sentence [[2]], and contrasts the narrow basis of the single victory. Sentence [[4]] concludes, 'Seen this way', that the prize's service lies less in 'that one verdict', the judges' choice of sentence [[3]], than in directing attention to a group.",
   "Putting sentence [[3]] before sentence [[2]] because it speaks of winners, as sentence [[1]] does, although 'those books' needs the shortlist of sentence [[2]].",
   "V01N-literary-prize-shortlists",
   "The opener states the thesis; 'those books' and 'that one verdict' fix the remaining links.",
   cognitive="Understanding",
   traps=[("1324", "Sentence [[3]] says 'Only one of those books will win', but no set of books has been named until the shortlist of sentence [[2]]."),
          ("1243", "Sentence [[4]] speaks of 'that one verdict', the judges' verdict described only in sentence [[3]], so it cannot come before it.")])

# 017 -------------------------------------------------------------------------------------------
pj("V01-N-017", "Technology",
   "Noise cancellation works by predicting and inverting sound, so steady noise is cancelled but sudden noise is not.", "Medium",
   ["Noise-cancelling headphones do not so much block sound as answer it, playing back a mirror image of the noise that a small microphone picks up outside.",
    "Where the incoming wave rises, the added wave falls, so that the two largely erase each other before they reach the ear.",
    "For the answer to arrive in time, however, the device must in effect predict the noise a fraction of a second ahead.",
    "That condition explains why a steady engine drone is silenced well, while a voice or a slammed door, changing shape from moment to moment, largely gets through."],
   "Sentence [[1]] introduces the principle of answering noise with its mirror image. Sentence [[2]] describes how 'the incoming wave' and 'the added wave' cancel. Sentence [[3]] adds the requirement that the device must predict the noise. Sentence [[4]] refers to 'That condition', the need for prediction, and uses it to explain which noises are cancelled and which are not.",
   "Placing sentence [[4]] before sentence [[3]] because it gives concrete examples, although 'That condition' refers to the requirement of prediction stated in sentence [[3]].",
   "V01N-noise-cancelling-headphones",
   "Order depends mainly on the logic of the mechanism: principle, how cancellation works, the prediction requirement, and what follows from it.",
   cognitive="Analysis",
   traps=[("1243", "Sentence [[4]] begins 'That condition', but no condition has been stated until sentence [[3]] says the device must predict the noise."),
          ("1324", "Sentence [[2]] describes the cancellation itself and needs to follow sentence [[1]] directly; after sentence [[3]] it would separate the prediction requirement from the examples it explains.")])

# 018 -------------------------------------------------------------------------------------------
pj("V01-N-018", "Health and medicine",
   "Cautious monitor alarms produce so many false alerts that staff respond less, so fewer alarms can be safer.", "Medium",
   ["Hospital monitors are designed to sound an alarm whenever a patient's heart rate, breathing or oxygen level moves outside a safe range.",
    "Because the limits are set cautiously, most alarms are triggered by harmless events, such as a patient shifting in bed or a loose sensor.",
    "Nurses who hear dozens of false alarms in a single shift naturally begin to respond more slowly, or to silence the devices altogether.",
    "The result is a cruel irony: a system built to catch every emergency makes staff less likely to notice the real one when it comes.",
    "Reducing alarms, by setting limits for each patient and adding short delays, can therefore make a ward safer rather than more dangerous."],
   "Sentence [[1]] describes what monitors are designed to do. Sentence [[2]] says that cautious limits make most alarms false. Sentence [[3]] describes how staff respond to 'dozens of false alarms'. Sentence [[4]] names 'The result', the irony that the system hides real emergencies. Sentence [[5]] draws the conclusion with 'therefore' that fewer alarms can be safer, which follows only once the irony has been stated.",
   "Placing sentence [[5]] before sentence [[4]] because both comment on the problem, although the claim that fewer alarms can be safer depends on the irony spelled out in sentence [[4]].",
   "V01N-monitor-alarm-fatigue",
   "Order depends mainly on the causal logic: design, false alarms, staff response, ironic result, remedy.",
   cognitive="Analysis",
   traps=[("12354", "Sentence [[5]] concludes 'therefore' that reducing alarms can make a ward safer; that rests on the irony in sentence [[4]], and 'The result' in sentence [[4]] must follow the staff behaviour of sentence [[3]] directly."),
          ("13245", "Sentence [[3]] speaks of 'false alarms', but only sentence [[2]] explains that most alarms are false, so sentence [[3]] cannot come before it.")])

# 019 -------------------------------------------------------------------------------------------
pj("V01-N-019", "Science and environment",
   "The tidy story of a returning predator healing an ecosystem outruns the evidence, though predators may still matter.", "Difficult",
   ["Few conservation stories are told with more enthusiasm than that of the returning predator who, by frightening grazing animals, allows forests and riverbanks to recover.",
    "Its appeal lies partly in its moral shape: a wrong is undone, and a damaged system rights itself once a single missing piece is restored.",
    "Ecologists who have revisited such cases are wary of precisely this tidiness, pointing out that drought, hunting and patterns of land use often changed during the same years.",
    "None of this shows that the predators made no difference; it shows that a before-and-after comparison cannot by itself say how much."],
   "Sentence [[1]] introduces the popular story of the returning predator. Sentence [[2]] explains 'Its appeal', the story's moral shape of a single missing piece restored. Sentence [[3]] reports that ecologists are wary of 'precisely this tidiness', which refers to that moral shape, and supplies the rival causes. Sentence [[4]] qualifies the scepticism: 'None of this' shows that predators did nothing, only that a before-and-after comparison cannot measure their effect. The concession must come last because it limits the doubt raised in sentence [[3]].",
   "Moving straight from the story in sentence [[1]] to the ecologists in sentence [[3]] because it seems natural to bring in the experts next, which leaves 'this tidiness' with nothing to refer to and strands the appeal of sentence [[2]] between the doubt and its qualification.",
   "V01N-wolf-reintroduction-trophic-cascade",
   "Order depends mainly on the logic of the argument: the story, why it appeals, why that appeal invites doubt, and a concession that limits the doubt. The tempting order brings in the sceptics too early.",
   cognitive="Analysis", exams=DX,
   traps=[("1324", "Sentence [[3]] is wary of 'precisely this tidiness', which is the moral shape described in sentence [[2]]; and sentence [[4]]'s 'before-and-after comparison' answers the rival causes of sentence [[3]], so the two cannot be separated by sentence [[2]]."),
          ("1243", "Sentence [[4]] concedes that the predators may have mattered; before sentence [[3]] there is no doubt for it to qualify.")])

# 020 -------------------------------------------------------------------------------------------
pj("V01-N-020", "Arts and literature",
   "Folk tale variants cannot be traced to one original because tellers combine versions; the better question is why variants took root.", "Difficult",
   ["For a long time, scholars who collected the many versions of a familiar folk tale treated them as clues to a lost original, the form in which the story was first told.",
    "Each retelling, on this view, was an imperfect copy of an earlier one, and the scholar's task was to strip away accumulated errors until the source emerged.",
    "Storytellers, though, are not copyists: they shape a tale to the audience in front of them and freely combine what they have heard from several tellers.",
    "Once versions mingle like this, there is no single line of descent to trace, and the family tree that the method requires gives way to something more like a web.",
    "The more fruitful question may be not what the first telling was, but why certain variations took root in certain places and not in others."],
   "Sentence [[1]] introduces the old search for a lost original. Sentence [[2]] spells out the assumption behind it 'on this view': every version is a copy of an earlier one. Sentence [[3]] challenges that assumption with 'though': tellers are not copyists and combine versions. Sentence [[4]] draws the consequence of mingling 'like this': there is no single line of descent. Sentence [[5]] proposes a better question, which makes sense only once the search for the first telling has been shown to fail.",
   "Treating sentence [[5]] as the natural response to sentence [[3]] and ending with sentence [[4]]; but 'the more fruitful question' replaces the search for an original, and it is sentence [[4]] that shows that search cannot succeed.",
   "V01N-folk-tale-variants",
   "Order depends mainly on the logic of the idea: a method, its assumption, the fact that defeats the assumption, the consequence for the method and the alternative question. The last two sentences tempt a swap.",
   cognitive="Analysis", exams=DX,
   traps=[("12354", "Sentence [[4]] explains the consequence of tellers mixing versions 'like this', and it must follow sentence [[3]] directly; after sentence [[5]] the paragraph would propose a new question before showing why the old one fails."),
          ("13245", "Sentence [[2]] expounds the view of sentence [[1]] ('on this view'); after sentence [[3]] has already denied that tellers are copyists, restating the copying assumption would come too late.")])

# 021 -------------------------------------------------------------------------------------------
pj("V01-N-021", "Health and medicine",
   "The last stage of disease eradication looks costly per case, but that ignores the permanent end of vaccination costs.", "Difficult",
   ["In the early years of a campaign to eradicate a disease, each round of vaccination prevents a great many cases at modest cost.",
    "As the disease retreats into a few remote or unsettled regions, every remaining case becomes far more expensive to prevent.",
    "Measured by cases averted for each unit of money spent, the final stage can look like poor value, since the same funds might save more lives if spent on common illnesses.",
    "That comparison leaves out the one return that only eradication offers: once transmission has ended everywhere, vaccination can eventually stop and its costs end with it."],
   "Sentence [[1]] describes the cheap early stage of eradication. Sentence [[2]] describes the expensive late stage, and the order of the two follows from the logic of a disease that 'retreats' over time. Sentence [[3]] judges the final stage by cost per case and finds it poor value. Sentence [[4]] answers 'That comparison', the cost-per-case reckoning of sentence [[3]], by pointing to the permanent saving it ignores. The rebuttal must close, because it overturns the verdict of sentence [[3]].",
   "Ending with sentence [[3]] on the thought that 'poor value' is the paragraph's verdict; but sentence [[4]] begins 'That comparison', which needs the comparison of sentence [[3]] before it, and it reverses that verdict.",
   "V01N-polio-eradication-last-cases",
   "Order depends mainly on the logic of the idea: rising marginal cost, a cost-per-case verdict and its rebuttal. The cost-per-case verdict looks like a conclusion, tempting candidates to end on it.",
   cognitive="Analysis", exams=DX,
   traps=[("1243", "Sentence [[4]] refers to 'That comparison', but the comparison of cases averted per unit of money is made only in sentence [[3]]."),
          ("2134", "Sentence [[2]] says the disease 'retreats', which presupposes the campaign already under way in sentence [[1]]; and the cheap early years cannot follow a description of the costly final stage.")])

# 022 -------------------------------------------------------------------------------------------
pj("V01-N-022", "Education",
   "Mathematics anxiety both results from and causes poor performance, since worry uses up working memory.", "Difficult",
   ["Students who fear mathematics tend to perform worse in it, and the obvious explanation is that weak skills breed anxiety.",
    "That explanation is not wrong, but it is incomplete, for anxiety also consumes the working memory that a calculation needs.",
    "A student who is busy worrying about failure has less mental room to hold numbers and steps in mind, and so makes errors that seem to confirm the fear.",
    "The relationship thus runs in both directions, which suggests that easing the fear may improve performance even before any new skill is taught."],
   "Sentence [[1]] states the link between fear and poor performance and the 'obvious explanation' that weak skills cause anxiety. Sentence [[2]] judges 'That explanation' incomplete and introduces the reverse mechanism, anxiety using up working memory. Sentence [[3]] illustrates that mechanism with a worrying student. Sentence [[4]] concludes that 'The relationship thus runs in both directions', which needs both causal directions to have been stated.",
   "Placing the worrying student of sentence [[3]] directly after sentence [[1]] because it seems to describe the fear; but sentence [[3]] illustrates the claim about working memory, which sentence [[2]] introduces with 'also', and sentence [[2]] would then repeat what has already been shown.",
   "V01N-maths-anxiety",
   "Order depends mainly on the logic of the idea: one causal direction, the claim that it is incomplete, an illustration of the reverse direction, and the two-way conclusion. The illustration of the worrying student is tempting immediately after the opener.",
   cognitive="Analysis", exams=DX,
   traps=[("1324", "After sentence [[3]] has shown worry crowding out working memory, sentence [[2]] would introduce that mechanism as new with 'also', and 'That explanation' would refer to the illustration rather than to the obvious explanation of sentence [[1]].")])

# 023 -------------------------------------------------------------------------------------------
pj("V01-N-023", "Education",
   "Student ratings measure the experience of a course, not learning, so they answer a narrower question than they are asked.", "Difficult",
   ["Universities increasingly ask students to rate their teachers, on the reasonable ground that learners are the people best placed to say what a course was like.",
    "What students can report well, however, is their experience of a course: whether lectures were clear, and whether the teacher seemed prepared and approachable.",
    "That experience is an unreliable guide to how much they learned, since a demanding course may feel worse at the time than an easy one.",
    "Ratings can therefore reward the very comfort that sometimes works against learning, especially when they are used to decide promotions.",
    "None of this makes student opinion worthless; it means that the ratings answer a narrower question than the one they are often asked to settle."],
   "Sentence [[1]] introduces student ratings and the reasonable case for them. Sentence [[2]] narrows what students report well, with 'however', to their experience of a course. Sentence [[3]] says 'That experience' is a poor guide to learning. Sentence [[4]] concludes with 'therefore' that ratings may reward comfort over learning, which needs the gap between experience and learning in sentence [[3]]. Sentence [[5]] concedes that the ratings still have value but answer a narrower question, a qualification that must follow the criticism.",
   "Placing the concession of sentence [[5]] before sentence [[4]] because it seems to soften the critique at the right moment; but 'therefore' in sentence [[4]] then follows a concession instead of the reason it draws on.",
   "V01N-student-evaluations-of-teaching",
   "Order depends mainly on the logic of the argument: a reasonable practice, the distinction between experience and learning, the consequence, and a closing concession. The concession tempts an earlier placement.",
   cognitive="Analysis", exams=DX,
   traps=[("12354", "Sentence [[4]] draws its 'therefore' from the gap between experience and learning in sentence [[3]]; placed after the concession of sentence [[5]], it would make the concession the ground for the criticism."),
          ("13245", "Sentence [[3]] begins 'That experience', which needs the experience of a course described in sentence [[2]].")])

# 024 -------------------------------------------------------------------------------------------
pj("V01-N-024", "Language and media",
   "Radio commentary must describe the play while television commentary must add context, so the crafts differ.", "Difficult",
   ["Radio commentators at a sporting event carry a burden that their television counterparts do not: the listener can see nothing except what the voice provides.",
    "Each pass, each shift in position and each change in the weather has to be turned into words at the pace of play.",
    "For a television audience the picture already does that work, and a commentator who describes what viewers can plainly see soon becomes an irritation.",
    "What the screen cannot supply is context: the history of a rivalry, the tactical reason for a substitution, the meaning of a moment within the season.",
    "The two crafts share a microphone but little else, which may be why a fine radio voice does not always succeed on television."],
   "Sentence [[1]] sets up the contrast and states the radio commentator's burden. Sentence [[2]] spells out that burden: everything must be turned into words. Sentence [[3]] says that on television the picture 'already does that work', the work of description just described, so describing becomes tiresome. Sentence [[4]] names what the screen cannot do and so what the television commentator must add. Sentence [[5]] concludes that the crafts share little, which needs both job descriptions before it.",
   "Placing sentence [[4]] before sentence [[3]] because both concern the screen; but 'that work' in sentence [[3]] would then refer to supplying context, which sentence [[4]] says the picture cannot do.",
   "V01N-live-sports-commentary",
   "Order depends mainly on the logic of a comparison: the radio task, why that task is redundant on television, what television needs instead, and the conclusion. Few connectives mark the links.",
   cognitive="Analysis", exams=DX,
   traps=[("12435", "If sentence [[4]] comes before sentence [[3]], the picture 'already does that work' would mean it supplies context, contradicting the claim that context is what the screen cannot supply."),
          ("13245", "Sentence [[3]] says the picture 'already does that work'; the work in question is turning every pass into words, which is described only in sentence [[2]], and the radio burden of sentence [[2]] would otherwise interrupt the account of television.")])

# 025 -------------------------------------------------------------------------------------------
pj("V01-N-025", "Language and media",
   "Because text messages usually omit the final full stop, including one has become a marked choice read as coldness.", "Difficult",
   ["In formal prose a full stop is the most neutral of marks, telling the reader nothing except that a sentence has ended.",
    "A text message hardly needs that information, because each one arrives in its own bubble, and many writers have stopped bothering with the final mark.",
    "Once leaving it out became normal, putting it in turned into a choice, and readers who notice a choice tend to look for a motive behind it.",
    "Many settle on coldness or annoyance, even when the writer was merely following habits formed in letters and essays."],
   "Sentence [[1]] states the neutral function of the full stop in formal prose. Sentence [[2]] says a text message 'hardly needs that information', the information that a sentence has ended, so writers drop the mark. Sentence [[3]] follows from this: once omission is 'normal', inclusion becomes a choice that invites a search for a motive. Sentence [[4]] gives the motive many readers settle on, and its 'Many' refers to the readers of sentence [[3]].",
   "Placing sentence [[3]] directly after sentence [[1]] because it seems to continue the discussion of the mark; but omission cannot be 'normal' until sentence [[2]] has described why texters leave the stop out.",
   "V01N-full-stop-in-text-messages",
   "Order depends mainly on the logic of the idea: a neutral norm, a new medium that makes the mark unnecessary, the resulting shift in meaning and how readers interpret it. The links are conceptual, with few connectives.",
   cognitive="Analysis", exams=DX,
   traps=[("1324", "Sentence [[3]] says leaving the mark out 'became normal', but nothing has yet explained why it would be left out; and sentence [[2]]'s 'that information' would then refer to a motive rather than to the end of a sentence.")])
