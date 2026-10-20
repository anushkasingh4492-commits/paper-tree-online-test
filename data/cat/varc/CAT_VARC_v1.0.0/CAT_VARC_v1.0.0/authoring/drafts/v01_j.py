import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

HARD = ("CAT", "XAT")

# ------------------------------------------------------------------ Easy (7)
pj("V01-J-001", "Education", "Teaching to a single high-stakes test is an understandable temptation whose cost falls on pupils.", "Easy",
   ["When a school's reputation rests on a single annual examination, teachers face a strong temptation to teach only what that examination is likely to ask.",
    "This temptation is understandable, since a teacher whose pupils score poorly may be blamed regardless of what else those pupils have learned.",
    "Yet the cost of giving in to it is borne by the pupils, who learn to recognise question formats instead of understanding the subject behind them.",
    "Such pupils often do well in the examination hall and then struggle the moment a problem is posed in an unfamiliar form."],
   "Sentence [[1]] introduces the situation and names 'a strong temptation'. Sentence [[2]] picks it up as 'This temptation' and concedes that it is understandable. Sentence [[3]] turns with 'Yet' from that concession to the cost of 'giving in to it'. Sentence [[4]] describes 'Such pupils', the pupils of sentence [[3]] who recognise formats without understanding.",
   "Placing sentence [[3]] straight after sentence [[1]], which leaves 'Yet' with no concession to turn against and pushes 'This temptation is understandable' after the description of its consequences.",
   "V01J-teaching-to-the-test", "Each link is carried by a clear reference word ('This temptation', 'Yet', 'Such pupils').",
   traps=[("1342", "Sentence [[3]] needs a concession before its 'Yet', which sentence [[2]] supplies; placed last, sentence [[2]] also refers to a temptation mentioned two sentences earlier.")],
   cognitive="Understanding")

pj("V01-J-002", "Health and medicine", "Snow's cholera map mattered because it treated the pattern of cases as evidence.", "Easy",
   ["In the middle of the nineteenth century, most London physicians believed that cholera spread through foul air rising from filth and decay.",
    "During the outbreak of 1854, however, the physician John Snow traced the homes of the dead and found them clustered around one public water pump.",
    "When he persuaded the local authorities to remove the pump's handle, he was acting on his rival view that the disease travelled through contaminated water.",
    "The map he later drew of those deaths is remembered less for settling the question at once, which it did not, than for showing how the pattern of cases could itself be evidence."],
   "Sentence [[1]] states the prevailing belief and must open. Sentence [[2]] contrasts with it ('however') and introduces Snow and the pump. Sentence [[3]] continues with 'he' and 'the pump's handle', which need sentence [[2]], and names his 'rival view'. Sentence [[4]], 'The map he later drew of those deaths', steps back to judge the significance of the episode and closes.",
   "Putting the retrospective judgement in sentence [[4]] directly after the deaths are traced in sentence [[2]], which strands the action of sentence [[3]] after the verdict.",
   "V01J-broad-street-cholera-pump", "Chronology and reference words ('however', 'he', 'The map he later drew') fix the order.",
   traps=[("1243", "Sentence [[4]] passes a final verdict on the map; returning afterwards to the removal of the handle in sentence [[3]] breaks the move from event to assessment.")],
   cognitive="Understanding")

pj("V01-J-003", "Cities and geography", "Obsolete city walls were replaced by ring boulevards still visible on maps.", "Easy",
   ["For centuries, many European cities were enclosed by thick walls that protected their inhabitants but also confined their growth.",
    "As artillery improved and national armies replaced local militias, these fortifications lost most of their military value.",
    "Rather than leave them to crumble, several cities demolished their walls and laid out broad ring roads along the line they had occupied.",
    "The result is a pattern still visible on modern maps, in which a dense medieval core is circled by a wide boulevard lined with later public buildings."],
   "Sentence [[1]] introduces the walls. Sentence [[2]] refers to 'these fortifications' and explains why they became useless. Sentence [[3]] says what cities did with 'them' instead of letting them crumble. Sentence [[4]] describes 'The result' of that demolition on today's maps.",
   "Placing sentence [[3]] before sentence [[2]]: demolition is then described before any reason for it, and 'these fortifications lost most of their military value' comes after the walls are already gone.",
   "V01J-demolished-city-walls", "A simple chronological chain with backward references.",
   traps=[("1324", "Sentence [[3]] says cities chose not to 'leave them to crumble', which presupposes that the walls had already lost their purpose, the point made in sentence [[2]].")],
   cognitive="Understanding")

pj("V01-J-004", "Psychology", "The spotlight effect makes us overrate how much others notice us.", "Easy",
   ["Most people overestimate how much others notice their appearance and behaviour, a tendency psychologists call the spotlight effect.",
    "Someone who arrives at a party with a stain on a shirt, for instance, may spend the evening convinced that everyone has seen it.",
    "In fact, the other guests are largely occupied with their own worries about how they themselves are coming across.",
    "Recognising this can be oddly liberating, because it suggests that the audience we imagine judging us is mostly absorbed in its own performance."],
   "Sentence [[1]] defines the tendency. Sentence [[2]] gives an example ('for instance') of a guest at a party. Sentence [[3]] corrects the guest's belief with 'In fact, the other guests'. Sentence [[4]] draws the consoling lesson from sentence [[3]]: the imagined audience is 'absorbed in its own performance'.",
   "Putting sentence [[4]] right after the definition, so that 'Recognising this' refers only to the definition and the party example is left hanging at the end.",
   "V01J-spotlight-effect", "Definition, example, correction and lesson, each marked by a cue.",
   traps=[("1423", "Sentence [[4]]'s point that the audience is absorbed in its own performance rests on sentence [[3]]'s observation about the other guests, so it cannot precede the example.")],
   cognitive="Understanding")

pj("V01-J-005", "Society and culture", "Wedding costs escalate through comparison and can only be checked by a shared change of expectation.", "Easy",
   ["In many communities, the expected cost of a wedding has risen far faster than the incomes of the families who must pay for it.",
    "One reason is that a wedding is a public display, and each family's celebration is measured against the most lavish ones its guests have recently attended.",
    "Because no family wishes to appear meaner than its neighbours, the standard keeps rising even when most hosts privately wish it would stop.",
    "Breaking this cycle therefore requires a shared change in expectations, since a single family that spends modestly only invites comment."],
   "Sentence [[1]] states the trend. Sentence [[2]] offers 'One reason' for it, the comparison with other weddings. Sentence [[3]] shows how that comparison makes the standard keep rising, which is the cycle. Sentence [[4]] refers to 'this cycle' and draws the conclusion with 'therefore'.",
   "Starting with sentence [[2]] because it sounds like a general claim, although 'One reason' needs a trend to explain.",
   "V01J-wedding-spending-escalation", "Problem, cause, mechanism and conclusion with explicit cues.",
   traps=[("1324", "Sentence [[3]] relies on the comparison that sentence [[2]] introduces, and placed after sentence [[3]] the phrase 'One reason' would interrupt the move to the conclusion.")],
   cognitive="Understanding")

pj("V01-J-006", "Education", "Summer learning loss falls unevenly and may explain part of the inequality blamed on schools.", "Easy",
   ["Teachers have long noticed that pupils return from the long summer holiday having forgotten part of what they learned the previous year.",
    "This loss is not spread evenly, however, because children from homes with books, outings and educated parents often hold their ground or even advance.",
    "Children without such resources, by contrast, tend to fall back, so that a gap which was small in June has widened by September.",
    "Repeated over several summers, these seasonal differences may account for a good share of the gap observed between the two groups by the end of school.",
    "If that is so, then some of the inequality usually blamed on schools arises in the months when schools are closed."],
   "Sentence [[1]] introduces the summer loss. Sentence [[2]] qualifies it ('This loss is not spread evenly') with the advantaged children. Sentence [[3]] gives the contrasting group, 'Children without such resources'. Sentence [[4]] accumulates 'these seasonal differences' over several summers. Sentence [[5]] draws the implication with 'If that is so', which needs the claim of sentence [[4]].",
   "Ending with sentence [[4]] after sentence [[5]], although 'If that is so' must refer to the cumulative claim of sentence [[4]].",
   "V01J-summer-learning-loss", "Five sentences, but each is tied to the last by a clear marker.",
   traps=[("12354", "Without sentence [[4]] before it, 'If that is so' in sentence [[5]] has only the single-summer gap to refer to, which does not support a claim about inequality over a school career.")],
   cognitive="Understanding")

pj("V01-J-007", "Health and medicine", "Menu calorie labels may change restaurant offerings more than diners' choices.", "Easy",
   ["Requiring restaurants to print the calorie content of each dish beside its price seems an obvious way to help diners eat more healthily.",
    "The reasoning behind the rule is simple: people choose badly partly because they do not know what their food contains.",
    "But diners who already care about calories tend to know roughly what they are ordering, while those who do not care are unlikely to be moved by a number.",
    "The labels may therefore change less what customers choose than what restaurants offer, since few chains wish to advertise a dish with an alarming figure."],
   "Sentence [[1]] introduces the requirement. Sentence [[2]] states 'The reasoning behind the rule', which needs the rule of sentence [[1]]. Sentence [[3]] objects with 'But'. Sentence [[4]] concludes with 'therefore' that the effect falls on restaurants rather than diners.",
   "Opening with sentence [[2]], which cannot stand first because 'the rule' has not been introduced.",
   "V01J-calorie-labels-on-menus", "Proposal, rationale, objection, conclusion, with clear cues.",
   traps=[("1324", "Sentence [[3]]'s 'But' objects to the reasoning that diners lack information, so that reasoning, sentence [[2]], must come first.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ Medium (11)
pj("V01-J-008", "Education", "Tacit craft knowledge passes only by imitation, which explains the survival of apprenticeship.", "Medium",
   ["Much of what a skilled craftsperson knows cannot be written down, because it lives in the hands and the eye rather than in rules.",
    "A master carpenter, for example, can tell from the sound of a plane whether the blade needs sharpening, yet would struggle to explain how.",
    "Knowledge of this kind, like the carpenter's ear for a blunt blade, passes from one person to another only through long periods of watching, trying and being corrected.",
    "That is why the apprenticeship, slow and costly as it seems, survived for centuries even in trades that had plenty of printed manuals."],
   "Sentence [[1]] states the general claim that craft knowledge cannot be written down. Sentence [[2]] illustrates it with the carpenter ('for example'). Sentence [[3]] says how 'Knowledge of this kind' is transmitted, and its comparison 'like the carpenter's ear' needs the carpenter of sentence [[2]] before it. Sentence [[4]] must follow sentence [[3]] directly: the apprenticeship survives because transmission requires watching and correction, which is exactly what an apprenticeship provides, and that is why printed manuals could not replace it.",
   "Treating the carpenter example as movable and placing it after sentence [[3]], which separates the explanation in sentence [[3]] from the conclusion it supports.",
   "V01J-apprenticeship-tacit-knowledge", "Order depends on the logic of the idea: the conclusion about apprenticeship needs the claim about how such knowledge travels immediately before it.",
   traps=[("1324", "Sentence [[2]] illustrates knowledge that cannot be explained, not transmission by watching, and sentence [[3]] already refers back to 'the carpenter's ear'; placed after sentence [[3]] it also breaks the link between that sentence and the 'That is why' of sentence [[4]]."),
          ("2134", "Sentence [[2]] contains 'for example', so it needs the general claim of sentence [[1]] before it.")])

pj("V01-J-009", "Health and medicine", "Incentives for rare-disease drugs solved one problem and created a pricing problem.", "Medium",
   ["A disease that affects only a few thousand people worldwide offers a drug company little prospect of recovering the cost of developing a treatment.",
    "Left to the market alone, such conditions would therefore attract almost no research, however severe the suffering they cause.",
    "Several governments have responded by offering firms that develop drugs for rare diseases extended periods of exclusive sale and other incentives.",
    "These incentives have worked, perhaps too well, since some companies now charge prices for such drugs that strain even wealthy health systems.",
    "The policy has thus traded one problem for another: treatments that once did not exist now exist but are rationed by their cost."],
   "Sentence [[1]] sets out the economics of a rare disease. Sentence [[2]] draws the consequence ('therefore') for 'such conditions'. Sentence [[3]] describes how governments 'responded' to that neglect. Sentence [[4]] evaluates 'These incentives', which must follow sentence [[3]] directly. Sentence [[5]] sums up the trade of one problem for another, which needs both the original problem and the new one.",
   "Placing sentence [[3]] immediately after sentence [[1]], since a response seems to follow a problem, which leaves sentence [[2]] with nowhere to go once sentences [[3]] and [[4]] are locked together.",
   "V01J-orphan-drugs-rare-diseases", "Five sentences; the student must see that the governments respond to the neglect of rare diseases, not merely to their cost.",
   traps=[("13245", "Sentences [[3]] and [[4]] form a pair ('These incentives'); inserting sentence [[2]] between them breaks it, and the governments of sentence [[3]] respond to the neglect that sentence [[2]] describes.")])

pj("V01-J-010", "Cities and geography", "Relocating slum dwellers failed because it cut them off from livelihoods, which led to upgrading in place.", "Medium",
   ["For decades, the standard response to informal settlements was to clear them and move their residents to new housing on the edge of the city.",
    "The new blocks were often sound, but they stood far from the markets, workshops and households where residents had earned their living.",
    "Cut off from these sources of income, many families sold or abandoned their allotted flats and drifted back towards the centre.",
    "Such failures pushed planners towards upgrading settlements where they stand, laying pipes and paving lanes while leaving the networks of livelihood intact."],
   "Sentence [[1]] describes the old policy of clearance and relocation. Sentence [[2]] identifies the flaw in 'The new blocks': distance from work. Sentence [[3]] gives the consequence, families 'Cut off from these sources of income' returning to the centre. Sentence [[4]] draws the policy lesson from 'Such failures', and its stress on 'leaving the networks of livelihood intact' answers the flaw of sentence [[2]].",
   "Reading sentence [[4]] as the second sentence because it also concerns policy, which puts the families' return after the new policy that was a response to it.",
   "V01J-in-situ-slum-upgrading", "Order follows the logic of cause and consequence: the flaw, then its effect, then the policy that answers it.",
   traps=[("1243", "Sentence [[3]] describes the failure of relocation; after sentence [[4]] it would describe residents abandoning flats under a policy that no longer moves them."),
          ("1324", "'these sources of income' in sentence [[3]] has no referent until sentence [[2]] lists the markets and workshops.")])

pj("V01-J-011", "Philosophy and ethics", "Refusing the experience machine suggests we value contact with reality for its own sake.", "Medium",
   ["Imagine a machine that could give you any experiences you wished, indistinguishable from real life, for as long as you remained plugged in.",
    "If pleasure were the only thing that mattered, we should all be eager to connect ourselves to it for life.",
    "Most people, however, recoil from the offer, and the reasons they give are telling: they want actually to do things, not merely to feel that they are doing them.",
    "The thought experiment is therefore usually taken as evidence that we value contact with reality for its own sake, and not only for the feelings it produces."],
   "Sentence [[1]] sets up the machine. Sentence [[2]] states what a pleasure-only view predicts about 'it'. Sentence [[3]] reports that people in fact 'recoil', which contrasts ('however') with that prediction. Sentence [[4]] concludes ('therefore') what the refusal shows about our values.",
   "Placing sentence [[3]] directly after sentence [[1]], although its 'however' contrasts with an expectation that only sentence [[2]] supplies.",
   "V01J-experience-machine", "Order depends on the structure of the argument: prediction, contrary response, inference.",
   traps=[("1324", "With sentence [[2]] after sentence [[3]], the prediction appears after people have already recoiled, and 'however' contrasts with nothing.")])

pj("V01-J-012", "Psychology", "Remembered pain follows peak and end, so the experiencing and remembering selves keep different accounts.", "Medium",
   ["When people look back on a painful experience, their verdict depends surprisingly little on how long the pain lasted.",
    "What they remember instead is chiefly how bad it was at its worst moment and how it felt at the very end.",
    "This produces a strange possibility: adding a few minutes of milder discomfort to the end of a procedure can make the whole of it remembered as less unpleasant.",
    "Measured minute by minute, of course, the longer procedure contains strictly more suffering than the shorter one.",
    "Between them, these two verdicts show that the self who lives through an experience and the self who later remembers it may keep very different accounts."],
   "Sentence [[1]] says duration matters little in memory. Sentence [[2]] says what matters 'instead'. Sentence [[3]] draws the odd consequence ('This produces'). Sentence [[4]] sets the minute-by-minute measure against it, referring to 'the longer procedure' that sentence [[3]] created. Sentence [[5]] combines 'these two verdicts', the remembered one and the measured one, and so must come last.",
   "Treating sentence [[4]] as an opener because it sounds like a general point, although 'the longer procedure' refers to the extended procedure of sentence [[3]].",
   "V01J-peak-end-rule", "Order depends on the logic: the conclusion compares two verdicts, both of which must precede it.",
   traps=[("12354", "Sentence [[5]] speaks of 'these two verdicts'; before sentence [[4]] only the remembered verdict has been given."),
          ("14235", "Sentence [[4]] refers to 'the longer procedure', which does not exist until sentence [[3]] adds minutes to the procedure.")])

pj("V01-J-013", "Society and culture", "Tattoos have lost their marginal associations but kept their power to signal something else.", "Medium",
   ["Not long ago, a visible tattoo in many societies marked its wearer as belonging to the margins: sailors, prisoners, or members of rough trades.",
    "Over a few decades the same marks have migrated to the arms of accountants, teachers and grandmothers, and the old associations have largely faded.",
    "Yet the change has not erased the tattoo's power to signal; it has simply altered what is being signalled.",
    "Where a tattoo once announced that its wearer stood outside respectable society, it now more often announces a taste, a memory or an attachment the wearer wishes to display."],
   "Sentence [[1]] gives the old meaning. Sentence [[2]] describes the spread of 'the same marks' and the fading of the old associations. Sentence [[3]] qualifies this with 'Yet': the power to signal survives with a new content. Sentence [[4]] spells out the old and new content, elaborating 'altered what is being signalled'.",
   "Putting sentence [[3]] last as a summary, although its 'Yet' answers the fading of associations in sentence [[2]] and would make no sense after sentence [[4]] has already shown the tattoo still signalling.",
   "V01J-tattoo-respectability", "The final pair depends on seeing that the old-and-new contrast elaborates the claim that tattoos still signal, rather than summing up.",
   traps=[("1243", "After sentence [[4]] has shown what tattoos now announce, sentence [[3]]'s 'Yet the change has not erased the tattoo's power to signal' contradicts nothing and reads as a redundant reversal.")])

pj("V01-J-014", "Education", "Peer marking is valuable for what the marker learns, provided pupils are taught the criteria.", "Medium",
   ["Asking pupils to mark one another's work is often defended as a way of saving teachers' time.",
    "Its real value lies elsewhere, in what the marker learns by applying the criteria to someone else's attempt.",
    "A pupil who has had to decide why a classmate's answer earns only half the marks is far more likely to notice the same weakness in her own.",
    "Her judgement is only as sound as her grasp of the criteria, however, so pupils must first be taught what good work looks like, or they will simply reward neatness and length."],
   "Sentence [[1]] gives the common defence. Sentence [[2]] relocates the value ('lies elsewhere'). Sentence [[3]] illustrates that value with a pupil who learns from marking. Sentence [[4]] adds the condition with 'Her judgement' and 'however': 'Her' refers to the pupil of sentence [[3]], and the caveat about grasping the criteria qualifies the benefit just shown, so it closes the paragraph.",
   "Placing the condition of sentence [[4]] immediately after sentence [[2]], so that the illustration in sentence [[3]] arrives after the warning and no longer supports the claim it was meant to show.",
   "V01J-peer-marking-classrooms", "Order depends on the logic: claim, illustration of the benefit, then the condition for that benefit.",
   traps=[("1243", "'Her judgement' in sentence [[4]] needs the pupil introduced in sentence [[3]]; the caveat also qualifies a benefit that only sentence [[3]] has demonstrated.")])

pj("V01-J-015", "Health and medicine", "A second opinion is valuable only if it is formed independently of the first.", "Medium",
   ["Patients facing a serious diagnosis are often advised to seek a second opinion, on the reasonable ground that any single doctor can be mistaken.",
    "The value of that second opinion, however, depends on its independence from the first.",
    "A specialist who is shown the original report before examining the patient will tend to see what it describes, and to confirm a diagnosis she might otherwise have questioned.",
    "To guard against this anchoring, the new doctor should examine the patient and form a view before reading what the first one concluded."],
   "Sentence [[1]] introduces the advice. Sentence [[2]] qualifies it ('however') by making value depend on independence. Sentence [[3]] shows how independence is lost when the report is read first. Sentence [[4]] answers 'this anchoring', the effect described in sentence [[3]], with a remedy.",
   "Moving the remedy of sentence [[4]] next to the claim about independence in sentence [[2]], which leaves 'this anchoring' without a referent.",
   "V01J-diagnostic-second-opinions", "Order depends on the logic of claim, mechanism and remedy; the remedy must follow the mechanism it answers.",
   traps=[("1243", "'this anchoring' in sentence [[4]] names the effect of seeing the report first, which only sentence [[3]] describes.")])

pj("V01-J-016", "Cities and geography", "Clearing street vendors removes real services; regulation is wiser than prohibition.", "Medium",
   ["City authorities often treat street vendors as an obstruction to be cleared from pavements in the name of order and hygiene.",
    "Yet the same vendors supply cheap food and goods to commuters and workers whom formal shops, with their higher rents, do not serve.",
    "They also keep streets occupied after offices close, and an occupied street is, by most accounts, a safer one.",
    "Clearing them therefore removes services that someone must then replace, often at greater public cost.",
    "A wiser policy would regulate where and when vending takes place rather than pretend that the demand it meets can be abolished."],
   "Sentence [[1]] states the official view. Sentence [[2]] counters it with 'Yet the same vendors' and a first service. Sentence [[3]] adds a second ('They also'). Sentence [[4]] draws the consequence ('therefore') from both services. Sentence [[5]] proposes the alternative policy, which builds on sentence [[4]]'s point that the services must be replaced.",
   "Closing with sentence [[4]] because 'therefore' sounds final, although sentence [[5]]'s 'wiser policy' depends on the cost of clearance that sentence [[4]] establishes.",
   "V01J-street-vendors-public-space", "Five sentences with one logic-dependent final pair.",
   traps=[("12354", "Sentence [[5]] proposes regulation 'rather than' clearance on the ground that the demand persists; sentence [[4]] supplies that ground and must come first, and after the proposal it would read as a step backwards."),
          ("13245", "'They also' in sentence [[3]] needs a first service; only sentence [[2]] provides it.")])

pj("V01-J-017", "Philosophy and ethics", "Resentment contains a judgement of wrong, so genuine forgiveness must acknowledge the wrong.", "Medium",
   ["Resentment is sometimes treated as a mere failing, a refusal to let go that harms the person who feels it more than anyone else.",
    "But resentment also carries a judgement: that one has been wronged, and that the wrong matters.",
    "This is why forgiveness given too quickly can seem less a virtue than a kind of self-disrespect, as though the injury had not really counted.",
    "Genuine forgiveness, then, must avoid that appearance: it acknowledges the wrong fully and only then gives up the resentment the wrong justified."],
   "Sentence [[1]] states the common view of resentment. Sentence [[2]] counters it ('But') by finding a judgement in resentment. Sentence [[3]] draws a consequence from that judgement ('This is why'). Sentence [[4]] says what genuine forgiveness must do to avoid 'that appearance', the appearance of self-disrespect in sentence [[3]].",
   "Placing sentence [[4]] before sentence [[3]] because both are about forgiveness, which leaves 'that appearance' with nothing to refer to.",
   "V01J-forgiveness-and-resentment", "Abstract ethical content; the order depends on following how the judgement in resentment leads to the account of forgiveness.",
   traps=[("1243", "Sentence [[4]] must avoid 'that appearance', the self-disrespect described only in sentence [[3]].")])

pj("V01-J-018", "Society and culture", "The variety of surname customs shows they answer social needs, not facts about families.", "Medium",
   ["In many societies a child takes the father's surname, a custom so familiar that it is easily mistaken for a natural arrangement.",
    "Elsewhere, children receive both parents' names, or a name derived from a parent's given name, or no fixed family name at all.",
    "The variety suggests that surnames answer social needs, such as tracing inheritance or registering citizens, rather than any fact about families themselves.",
    "Seen in that light, disputes over which name a child should carry are less about tradition than about which of those needs a society now considers most important."],
   "Sentence [[1]] describes the familiar custom and the illusion that it is natural. Sentence [[2]] lists the alternatives found 'Elsewhere'. Sentence [[3]] interprets 'The variety' just shown. Sentence [[4]] applies that interpretation ('Seen in that light', 'those needs') to modern disputes.",
   "Placing sentence [[3]] before sentence [[2]] because it sounds like a thesis, although 'The variety' requires the list of customs first.",
   "V01J-surname-inheritance-customs", "Observation, contrast, interpretation, application; the general claim is tempting as an early sentence.",
   traps=[("1324", "Sentence [[3]] interprets 'The variety', which only exists once sentence [[2]] has listed the other customs; sentence [[4]] must also follow the 'social needs' it calls 'those needs'.")])

# ------------------------------------------------------------------ Difficult (7)
pj("V01-J-019", "Philosophy and ethics", "The veil of ignorance does not settle justice by itself but exposes each side's attitude to risk.", "Difficult",
   ["Suppose you had to choose the rules of a society without knowing what place you would occupy in it: your class, talents, sex or health.",
    "Unable to favour yourself, you would have to consider how the rules looked from every position, including the worst.",
    "Fearing that the worst position might be their own, prudent choosers behind such a veil, it has been argued, would insist that the least advantaged be made as well off as possible.",
    "Critics reply that this conclusion owes less to the veil than to an assumed horror of risk, since a chooser willing to gamble might prefer greater rewards at the top.",
    "The device, then, does not settle what justice requires by itself, but it does force each side to state openly the attitude to risk on which its answer depends."],
   "Sentence [[1]] sets up the thought experiment. Sentence [[2]] draws its first implication: one must consider every position 'including the worst'. Sentence [[3]] picks up 'the worst position' and states the argued conclusion. Sentence [[4]] reports the critics' reply to 'this conclusion', introducing risk. Sentence [[5]] is the author's verdict: the device does not settle justice but forces each side to state its 'attitude to risk', which needs sentence [[4]].",
   "Ending with sentence [[4]] because a critics' reply often closes a debate, although the verdict of sentence [[5]] turns on the risk point that sentence [[4]] introduces.",
   "V01J-veil-of-ignorance", "Order depends on the logic of the argument: the verdict balances the argued conclusion against the critics' point about risk, so it must follow both.",
   traps=[("12354", "Sentence [[5]] speaks of 'the attitude to risk on which its answer depends', a notion that only sentence [[4]] introduces."),
          ("13245", "Sentence [[3]] refers to 'the worst position', which is introduced as a consideration only in sentence [[2]].")],
   exams=HARD)

pj("V01-J-020", "Philosophy and ethics", "On the dirty hands view, necessary political wrongs remain wrongs and good leaders bear the guilt.", "Difficult",
   ["A politician who refuses ever to lie, bargain with scoundrels or break a promise may keep a clean conscience while the people they serve pay for those scruples.",
    "Some have concluded that public office simply suspends private morality, so that what would be wrong for a citizen is permitted to a minister.",
    "The more troubling view is that the act remains wrong even when it is necessary, so that a good politician must sometimes do wrong and know it.",
    "On this account the mark of such a leader is not innocence but the willingness to carry guilt for what the office required."],
   "Sentence [[1]] states the dilemma that gives rise to the debate. Sentence [[2]] reports one conclusion drawn from it ('Some have concluded'). Sentence [[3]] offers 'The more troubling view', which is defined against the view of sentence [[2]]. Sentence [[4]] develops 'this account'; its talk of guilt fits only sentence [[3]], since on the view of sentence [[2]] there would be no wrong to feel guilty about.",
   "Opening with sentence [[2]] because it states a general position, although 'concluded' presupposes the dilemma of sentence [[1]].",
   "V01J-dirty-hands-in-politics", "Order depends on the logic of two rival views: the student must see that the talk of guilt belongs to the view that necessary acts remain wrong, not to the view that office suspends morality.",
   traps=[("2134", "Sentence [[2]] reports what 'Some have concluded', but the conclusion needs a premise; sentence [[1]]'s dilemma supplies it and must come first."),
          ("1324", "'The more troubling view' needs a less troubling view before it, and sentence [[4]]'s guilt cannot belong to the view that office suspends morality.")],
   exams=HARD)

pj("V01-J-021", "Psychology", "Equivalent risk frames change choices by shifting attention, not by conveying different information.", "Difficult",
   ["Told that a treatment gives ninety out of a hundred patients five more years of life, most people find it attractive.",
    "Told that ten out of a hundred will die within five years, many of the same people hesitate, although the two statements describe exactly the same outcome.",
    "A tempting conclusion is that people are simply careless with numbers, but the effect has been reported even among doctors who understand that the figures are equivalent.",
    "If arithmetic is not what fails, then what the framing alters is not the information people receive but the feature of the situation on which their attention settles."],
   "Sentence [[1]] gives the positive frame. Sentence [[2]] gives the negative frame, mentions 'the same people' and notes that the statements are equivalent. Sentence [[3]] considers and rejects the explanation that people cannot handle numbers. Sentence [[4]] follows from that rejection ('If arithmetic is not what fails') and offers the alternative explanation.",
   "Placing the explanation of sentence [[4]] before the objection in sentence [[3]], although sentence [[4]] presupposes that the arithmetic explanation has already been ruled out.",
   "V01J-risk-framing-gains-losses", "Order depends on the logic of eliminating one explanation before offering another; the two frames could seem to swap until 'the same people' is noticed.",
   traps=[("2134", "Sentence [[2]] refers to 'the same people' and 'the two statements', so the first frame in sentence [[1]] must precede it."),
          ("1243", "Sentence [[4]] begins from the premise that arithmetic does not fail, which only the evidence about doctors in sentence [[3]] establishes.")],
   exams=HARD)

pj("V01-J-022", "Psychology", "False consensus persists because believing one's views common is comforting, not only because of exposure.", "Difficult",
   ["People tend to assume that their own opinions and habits are more widely shared than they actually are.",
    "Part of the explanation is simply exposure, since we spend our time among people who resemble us and so mistake our circle for the world.",
    "But if exposure were the whole story, the bias should vanish once people learn the true figures, and it often seems not to.",
    "One likely addition is motive: believing that one's views are common is comforting, because it makes them seem normal and therefore reasonable.",
    "A belief that serves such a need is not easily corrected by information, since it was never held merely on the strength of information."],
   "Sentence [[1]] states the bias. Sentence [[2]] gives 'Part of the explanation', exposure. Sentence [[3]] shows that exposure cannot be 'the whole story'. Sentence [[4]] supplies 'One likely addition', the comfort motive. Sentence [[5]] uses 'such a need' to explain the observation in sentence [[3]] that information does not cure the bias, and so closes the argument.",
   "Placing sentence [[4]] straight after sentence [[2]] as a second cause, although 'addition' answers the gap that sentence [[3]] opens.",
   "V01J-false-consensus-effect", "Order depends on the logic of a partial explanation, its failure, and a supplement; two causes look listable in either order.",
   traps=[("12435", "Sentence [[4]]'s 'addition' answers the claim in sentence [[3]] that exposure is not the whole story, and sentence [[5]]'s 'such a need' must follow sentence [[4]] immediately."),
          ("13245", "Sentence [[3]] tests exposure as an explanation, which has not been proposed until sentence [[2]].")],
   exams=HARD)

pj("V01-J-023", "Cities and geography", "Rivers make attractive borders but move, turning their visibility into a source of dispute.", "Difficult",
   ["Rivers seem ideal boundaries, visible to everyone and hard to cross, which is why so many treaties have fixed borders along them.",
    "Yet a river is not a line but a process, forever eroding one bank, building up the other and occasionally abandoning its bed altogether.",
    "A border drawn along the channel as it ran on the day of signing may within a generation leave fields and villages on the wrong side of the water.",
    "Such stranded villages turn the river's chief merit as a frontier, its plain visibility, into a source of dispute, since anyone can see that the water no longer runs where the treaty says."],
   "Sentence [[1]] gives the case for rivers as borders. Sentence [[2]] objects ('Yet') that a river moves. Sentence [[3]] draws the practical consequence of that movement for a border fixed on one day. Sentence [[4]] refers to 'Such stranded villages' from sentence [[3]] and closes by turning the original advantage of sentence [[1]], visibility, into the source of the problem.",
   "Placing sentence [[3]] before sentence [[2]], as if the misplaced villages were the objection, although sentence [[3]] presupposes the movement of the channel that sentence [[2]] explains.",
   "V01J-rivers-as-shifting-borders", "Order depends on the logic of the idea: the consequence presupposes the process, and the conclusion ties back to the opening advantage.",
   traps=[("1324", "Sentence [[3]] takes for granted that the channel shifts after signing; only sentence [[2]] establishes that rivers move, and its 'Yet' must answer sentence [[1]]."),
          ("1243", "Sentence [[4]] begins 'Such stranded villages', which needs the villages left on the wrong side of the water in sentence [[3]]; as a closing example sentence [[3]] would also follow the conclusion it supports.")],
   exams=HARD)

pj("V01-J-024", "Society and culture", "A fixed retirement age is a recent arrangement whose original assumptions have changed.", "Difficult",
   ["A fixed age at which working life ends seems to many people a natural feature of the life course, like adolescence or old age itself.",
    "It is in fact a fairly recent invention, which spread with state pension schemes from the late nineteenth century onwards.",
    "When those schemes began, the qualifying age was set high enough that relatively few workers could expect to draw a pension for many years.",
    "Life expectancy has since risen greatly, but in many countries the qualifying age has risen far less, turning retirement from a brief coda into a long stage of life.",
    "Debates about raising that age are therefore not attempts to abolish a timeless right, but disputes over how to adjust an arrangement whose original assumptions no longer hold."],
   "Sentence [[1]] states the common belief that retirement is natural. Sentence [[2]] corrects it ('in fact') and links it to pension schemes. Sentence [[3]] describes the conditions when 'those schemes' began. Sentence [[4]] describes what has changed 'since'. Sentence [[5]] concludes ('therefore') by rejecting the 'timeless right' framing of sentence [[1]] and naming the changed assumptions of sentences [[3]] and [[4]].",
   "Placing sentence [[4]] before sentence [[3]], although 'since' and 'has risen far less' measure change from the starting point that sentence [[3]] fixes.",
   "V01J-retirement-age-social-invention", "Five sentences; the student must see that the conclusion answers the opening belief and needs the historical comparison.",
   traps=[("12435", "Sentence [[4]] says life expectancy has risen 'since', and that the age has risen less, which needs the original setting of the age in sentence [[3]]."),
          ("21345", "Sentence [[2]] begins 'It is in fact', a correction that needs the belief stated in sentence [[1]].")],
   exams=HARD)

pj("V01-J-025", "Psychology", "Treating money by its source looks irrational but may be a serviceable defence against temptation.", "Difficult",
   ["Money is supposed to be interchangeable: a rupee won in a lottery buys exactly what a rupee earned at work buys.",
    "Yet people treat money differently according to where it came from, spending a windfall freely while guarding wages with care.",
    "Economic theory long treated such habits as simple errors, a failure to see that the source of a sum makes no difference to its value.",
    "On reflection, though, keeping separate mental accounts may be a rough but serviceable defence against temptation, a way of protecting rent money from the lure of a holiday."],
   "Sentence [[1]] states the principle of interchangeability. Sentence [[2]] contrasts actual behaviour ('Yet'). Sentence [[3]] reports how theory judged 'such habits', as errors. Sentence [[4]] revises that judgement ('On reflection, though'), so it must follow the judgement it revises.",
   "Placing sentence [[4]] before sentence [[3]], although its 'though' reverses a dismissal and sentence [[2]] dismisses nothing.",
   "V01J-mental-accounting-windfalls", "Order depends on separating the reported judgement from the author's revision of it; the last two sentences look reversible.",
   traps=[("1243", "Sentence [[4]]'s 'On reflection, though' revises a verdict; only sentence [[3]] gives one, and after sentence [[4]] the dismissal would end the paragraph on a view the author has already answered."),
          ("1324", "'such habits' in sentence [[3]] requires the behaviour described in sentence [[2]].")],
   exams=HARD)
