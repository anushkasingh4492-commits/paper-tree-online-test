import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ Health and medicine
ooo("V03-C-001", "Health and medicine", "Night workers sleep against their body clock, which harms health and shapes how rotas are designed.", "Easy",
    ["People who work through the night are asking their bodies to sleep at the very hours when an internal clock is urging them to be awake.",
     "Even when such workers draw the curtains and silence their phones, their daytime sleep tends to be shorter and more broken than sleep taken at night.",
     "Over months and years, this persistent shortfall has been linked to poorer mood, slower reactions and a greater risk of several long-term illnesses.",
     "For this reason, some employers now design rotas that limit the number of consecutive night shifts, so as to ease the strain on that clock."],
    "Many people also find that a short nap in the early afternoon leaves them more alert for the rest of an ordinary working day.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] form a chain about night work: the body clock resists daytime sleep ([[1]]), so 'such workers' sleep badly ([[2]]), 'this persistent shortfall' harms health ([[3]]), and 'For this reason' rotas are adjusted to ease 'that clock' ([[4]]). Sentence [[X]] is about sleep too, but it concerns afternoon naps during 'an ordinary working day', which has nothing to do with night workers or the body clock argument.",
    "Picking any sentence about sleep as belonging, without checking that the paragraph is specifically about night workers.",
    "V03C-shift-work-and-sleep", "The odd sentence shares the sleep vocabulary but shifts to day workers; the backward links ('such workers', 'this shortfall', 'that clock') make the chain easy to see.",
    traps=[(4, "Sentence [[4]] can look like a shift from biology to management, but 'For this reason' and 'that clock' tie it to the harm described in sentence [[3]] and the clock of sentence [[1]].")],
    cognitive="Understanding")

ooo("V03-C-002", "Health and medicine", "Linking isolation to poor health raises the problem of which causes which, which only long studies can settle.", "Medium",
    ["For a long time loneliness was treated as a private sorrow, something to be pitied perhaps, but hardly a matter for doctors.",
     "That view has become harder to hold as researchers have found that people who are persistently isolated tend to fare worse on a range of health measures.",
     "The difficulty is that the direction of influence is not obvious, since illness can itself shrink a person's social world by keeping them at home.",
     "Untangling the two therefore requires following people over long periods, to see whether isolation comes before the decline in health or only after it."],
    "Some towns have responded by funding clubs and community centres where older residents can meet, often with encouraging attendance.",
    "The paragraph moves from an old view of loneliness ([[1]]) to the finding that undermines 'That view' ([[2]]), then to the problem of causal direction ([[3]]) and the long-term studies needed to settle it ([[4]], 'Untangling the two'). Sentence [[X]] is about loneliness as well, but it describes a policy response; the paragraph is concerned with whether isolation causes poor health, and the club sentence neither raises nor answers that question. Placed after [[2]], it would also cut the link between the finding and 'The difficulty' that qualifies it.",
    "Treating a practical response to loneliness as a natural next step, when the paragraph is about a problem of evidence, not about remedies.",
    "V03C-loneliness-as-health-risk", "The odd sentence could seem to follow the health finding, so it must be rejected on function: the paragraph is about causal direction, not remedies.",
    traps=[(1, "Sentence [[1]] may look like mere background, but sentence [[2]] begins 'That view', which needs sentence [[1]] as its antecedent.")])

ooo("V03-C-003", "Health and medicine", "A second opinion is a normal safeguard against the uncertainty of diagnosis, not a sign of distrust.", "Easy",
    ["Asking a second doctor to review a serious diagnosis is sometimes seen as a sign of distrust, yet it is better understood as an ordinary safeguard.",
     "Diagnosis involves judgement under uncertainty, and even careful clinicians will occasionally read the same scans or symptoms in different ways.",
     "An independent review can catch such differences before a patient commits to a treatment that is costly, painful or hard to reverse.",
     "Seen in this light, a request for a second opinion is less an accusation than a recognition of how difficult the original task was."],
    "Many hospitals have also invested in newer imaging equipment, which has made scans faster to obtain and more widely available.",
    "Sentence [[1]] states the claim that a second opinion is a safeguard, sentence [[2]] gives the reason (diagnosis is uncertain), sentence [[3]] shows how a review catches 'such differences', and sentence [[4]] restates the claim 'in this light'. Sentence [[X]] mentions scans, but it is about investment in equipment and speed of imaging; it says nothing about second opinions or diagnostic disagreement.",
    "Being drawn by the shared word 'scans' into thinking sentence [[X]] continues the point about reading scans differently.",
    "V03C-second-opinions-in-diagnosis", "The odd sentence shares only one word with the paragraph and clearly changes topic to equipment.",
    traps=[(4, "Sentence [[4]] may seem to repeat sentence [[1]], but it is the conclusion: 'Seen in this light' draws on the reasons in sentences [[2]] and [[3]].")],
    cognitive="Understanding")

ooo("V03-C-004", "Health and medicine", "Pain scores are anchored to each patient's experience, so they track one patient well but compare patients poorly.", "Difficult",
    ["When a clinician asks a patient to score pain from nought to ten, the result is a number, and numbers carry an air of objectivity that a description lacks.",
     "Yet each patient anchors the scale to their own history, so that a seven from someone who has never been badly hurt may mean something quite different from a seven from someone who has.",
     "The scale is therefore most trustworthy when it is used to follow a single patient over time, since the same person is likely to keep roughly the same anchors from one day to the next.",
     "Comparing scores across different patients, by contrast, risks treating a private yardstick as though it were a shared one."],
    "Because the number comes from the patient alone, it can also be deliberately inflated, and for this reason some clinicians prefer to disregard it altogether.",
    "The four sentences build one argument: a pain score looks objective ([[1]]), but it is anchored to personal history ([[2]]), so it is reliable within one patient over time ([[3]]) and unreliable across patients ([[4]], 'by contrast'). Sentence [[X]] also criticises the score, which makes it tempting, but it raises a different problem (deliberate exaggeration rather than personal anchoring) and ends by recommending that the score be disregarded 'altogether'. That dismissal cuts against sentence [[3]], which holds that the scale is 'most trustworthy' for tracking one patient, and nothing in the argument about anchoring builds on the worry about exaggeration, so the paragraph is complete without it.",
    "Accepting sentence [[X]] because it, like sentence [[2]], doubts the pain score, without noticing that its remedy contradicts the paragraph's conclusion.",
    "V03C-pain-rating-scales", "The odd sentence shares the topic, the critical tone and the vocabulary of the paragraph; it is rejected only because its kind of objection and its conclusion clash with the argument about anchoring.",
    traps=[(4, "Sentence [[4]] may look like an afterthought, but 'by contrast' completes the contrast begun in sentence [[3]]: reliable within one patient, unreliable across patients."),
           (1, "Sentence [[1]] may seem neutral, but its 'air of objectivity' is exactly what sentence [[2]] begins to undercut with 'Yet'.")],
    exams=D)

# ------------------------------------------------------------------ Cities and geography
ooo("V03-C-005", "Cities and geography", "Widening a road attracts new traffic, so early gains in speed can fade.", "Medium",
    ["When a congested road is widened, journeys along it usually become quicker for a while, and the expansion is hailed as a success.",
     "The faster journeys, however, change people's choices: some who used to travel at other hours, by other routes or by other means begin to drive on the new road.",
     "Within a few years the extra lanes may fill up, and the road can end up nearly as congested as before, though now carrying more vehicles.",
     "This does not mean widening is always pointless, but it does mean that its benefits cannot be judged by the first year's journey times."],
    "Congestion has costs beyond lost time as well, since engines that keep stopping and starting can release more pollution per kilometre than vehicles moving steadily.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] trace one sequence: widening brings quicker journeys ([[1]]), the quicker journeys draw in new drivers ([[2]]), the lanes fill again ([[3]]), and so early results mislead ([[4]], which refers back to 'the first year'). Sentence [[X]] is about congestion, but it introduces pollution as a further cost of traffic jams; the paragraph is about how road building changes demand, and nothing before or after connects to pollution.",
    "Choosing a sentence about congestion as coherent because the paragraph is full of congestion, without asking what the paragraph is arguing.",
    "V03C-induced-traffic-demand", "The odd sentence uses the paragraph's key word 'congestion' and is plausible, so it must be rejected on its function rather than its subject.",
    traps=[(4, "Sentence [[4]] concedes that widening is not always pointless, which can look like a change of direction, but it is the conclusion drawn from sentences [[1]], [[2]] and [[3]] about judging benefits too early.")])

ooo("V03-C-006", "Cities and geography", "Street vendors provide services and street life that a city loses when it clears them away.", "Easy",
    ["Street vendors are often treated by city authorities as an obstruction to be cleared from pavements.",
     "Yet for many residents they provide cheap food, small repairs and household goods within a few steps of home or work.",
     "Their presence also keeps streets busy into the evening, which can make pedestrians feel safer walking there.",
     "A city that simply removes them may therefore lose services and a sense of security that no planner had deliberately provided."],
    "Many vendors begin their working day before dawn, buying fresh produce at wholesale markets on the edge of the city.",
    "Sentence [[1]] gives the official view, sentence [[2]] answers it with 'Yet' (vendors provide services), sentence [[3]] adds a second benefit ('also'), and sentence [[4]] concludes that removing vendors loses both 'services and a sense of security'. Sentence [[X]] describes the vendors' daily routine; it is about the same people but plays no part in the argument about what a city gains from them.",
    "Keeping sentence [[X]] because it is about vendors, though it describes their working day rather than their value to the city.",
    "V03C-street-vendors", "The routine detail is clearly outside the argument once the benefit-and-conclusion structure is seen.",
    traps=[(3, "Sentence [[3]] may seem to drift from services to safety, but sentence [[4]] names 'a sense of security' as one of the two things lost, so it needs sentence [[3]].")],
    cognitive="Understanding")

ooo("V03-C-007", "Cities and geography", "Rent control is popular because its gains go to visible sitting tenants while its costs fall on dispersed newcomers.", "Difficult",
    ["The political appeal of rent control is easy to understand, because its benefits fall on people who already live in a city and can vote there.",
     "Sitting tenants see their rents held down and their tenancies made more secure, and they are rarely slow to say so.",
     "The costs, if there are any, tend to fall on those who are still looking for a home, since landlords facing capped returns may sell or convert flats rather than let them.",
     "Such people are dispersed and often not yet resident, so their losses seldom register in the debate as clearly as the gains of those already housed."],
    "Landlords, for their part, often argue that controlled rents leave them unable to pay for repairs, so that controlled buildings slowly deteriorate.",
    "The paragraph explains a political asymmetry: benefits go to existing residents who can vote ([[1]]), those tenants are vocal ([[2]]), costs fall on people still looking for a home ([[3]]), and 'Such people' are too dispersed to be heard ([[4]]). Sentence [[X]] mentions a cost of rent control, which makes it tempting, but the cost it describes (decaying buildings) falls on the sitting tenants themselves, which cuts against the claim that the costs fall on outsiders. It also cannot be placed: after [[3]] it would leave 'Such people' in [[4]] pointing to landlords, and before [[3]] it would make 'The costs, if there are any' read oddly after a cost has already been named.",
    "Reading sentence [[X]] as one more cost of rent control and missing that the paragraph is about who bears the costs and why they go unheard.",
    "V03C-rent-control", "The odd sentence shares the topic and seems to extend the list of costs; rejecting it requires seeing that it breaks the paragraph's insider and outsider structure and its reference chain.",
    traps=[(2, "Sentence [[2]] may look like a mere restatement of sentence [[1]], but it supplies the point that tenants are vocal, which sentence [[4]] contrasts with the silence of the dispersed losers."),
           (3, "Sentence [[3]] can seem a shift from politics to economics, but sentence [[4]] begins 'Such people', which refers to those 'still looking for a home' in sentence [[3]].")],
    exams=D)

ooo("V03-C-008", "Cities and geography", "Cities that once turned their backs on rivers now face a choice over who will use the reclaimed banks.", "Medium",
    ["Many cities that grew up beside rivers later turned their backs on them, lining the banks with warehouses, rail yards and drains.",
     "As long as the water served as a working channel for cargo and waste, there was little reason to make its edges pleasant for people.",
     "Once shipping moved elsewhere and the water was cleaned, those same banks became some of the most valuable open land a city possessed.",
     "The question many such cities now face is whether the reclaimed riverside will become a public promenade or a strip of expensive private frontage."],
    "Rivers have also served as natural boundaries between districts, and in some cities the two banks still differ markedly in wealth and character.",
    "The paragraph tells one story about riverbanks: neglected for industry ([[1]]), for an understandable reason ([[2]]), then valuable once industry left ([[3]], 'those same banks'), and now contested ([[4]], 'the reclaimed riverside'). Sentence [[X]] is about rivers in cities, but it treats the river as a boundary dividing districts; it has no place in the account of how the banks were used, abandoned and reclaimed.",
    "Accepting sentence [[X]] because it, like sentence [[4]], hints at wealth and inequality, though it concerns the river as a dividing line rather than the use of its banks.",
    "V03C-riverfronts-of-cities", "The odd sentence shares the urban river subject and a hint of inequality, so it must be rejected on function within the narrative.",
    traps=[(2, "Sentence [[2]] can look like a digression, but it explains why cities turned their backs on the rivers, and sentence [[3]] reverses exactly that condition with 'Once shipping moved elsewhere'.")])

# ------------------------------------------------------------------ Philosophy and ethics
ooo("V03-C-009", "Philosophy and ethics", "Blaming people for outcomes they did not control exposes the puzzle of moral luck.", "Medium",
    ["Two neighbours each leave a pan of oil on a lit stove and step out for ten minutes; one comes back to a smoky kitchen, while the other finds that a fire has spread to the flat next door.",
     "Most of us condemn the second neighbour far more harshly, even though the two acted with exactly the same carelessness.",
     "Yet what separates them is something neither of them could govern, such as a draught through a window or the position of a curtain.",
     "This is the puzzle of moral luck: our verdicts seem to follow outcomes, whereas our principles say that people deserve blame only for what was in their control."],
    "Fire services often warn that hot cooking oil left unattended is a common cause of household fires, and advise never leaving such a pan alone.",
    "Sentence [[1]] sets up a case, sentence [[2]] reports how we judge it, sentence [[3]] ('Yet') points out that the difference lay outside the neighbours' control, and sentence [[4]] names the resulting puzzle. Sentence [[X]] shares the example's vocabulary of cooking oil and fire, but it is a point about household safety; the paragraph uses the neighbours only to raise a question about blame, and how fires start is never its subject.",
    "Treating the kitchen example as the topic of the paragraph, when it is only an illustration of a puzzle about blame.",
    "V03C-moral-luck", "The odd sentence matches the illustration closely, so the solver must see that the paragraph's subject is the ethics of blame, not fire safety.",
    traps=[(1, "Sentence [[1]] may look like a story rather than an argument, but sentences [[2]] and [[3]] refer to 'the second neighbour' and 'the two', so it is the case the whole argument depends on.")])

ooo("V03-C-010", "Philosophy and ethics", "A promise binds despite inconvenience but lapses for changes both parties would have accepted as cancelling it.", "Difficult",
    ["A promise would be worth little if it bound us only when keeping it happened to suit us, since its whole purpose is to let others rely on what we will do.",
     "Still, few people think a promise binds no matter what, and someone who misses a lunch appointment to take an injured stranger to hospital is not usually thought to have done wrong.",
     "What seems to matter is whether the change is one that both parties, had they foreseen it, would have agreed should cancel the commitment.",
     "Mere inconvenience fails this test, because the person relying on us would never have accepted 'unless something more pleasant comes up' as a condition."],
    "Some philosophers hold that the duty to keep promises rests on the general good that comes from living in a society where promises are reliable.",
    "The paragraph asks when a promise may be broken: it binds even when inconvenient ([[1]]), 'Still' it does not bind absolutely ([[2]]), the test is whether both parties would have accepted the change as cancelling it ([[3]]), and 'this test' rules out mere inconvenience ([[4]]). Sentence [[X]] is about promises and echoes the idea of reliance in sentence [[1]], but it answers a different question, namely why there is a duty to keep promises at all. The paragraph takes that duty for granted and asks only about its limits, so sentence [[X]] does not connect to the test that the other sentences develop.",
    "Choosing to keep sentence [[X]] because it seems to expand on the 'purpose' of promises mentioned in sentence [[1]], missing that the paragraph is about exceptions, not foundations.",
    "V03C-promises-under-changed-circumstances", "The odd sentence shares the paragraph's terms and appears to develop the opening claim about reliance; rejecting it requires separating the question of the duty's basis from the question of its limits.",
    traps=[(1, "Sentence [[1]] may look like the foundational point that belongs with sentence [[X]], but sentence [[2]] opens with 'Still', which needs the claim in sentence [[1]] that promises bind even when inconvenient, and sentence [[4]] returns to that claim."),
           (2, "Sentence [[2]] may look like an isolated anecdote, but it introduces 'the change' that sentence [[3]] tests.")],
    exams=D)

ooo("V03-C-011", "Philosophy and ethics", "Medicine moved from withholding the truth to informed consent, though consent is only as good as the explanation behind it.", "Medium",
    ["In older medical practice, doctors often withheld a grave diagnosis from patients, believing that the truth would only add fear to illness.",
     "Such paternalism was usually well meant, but it treated patients as people to be managed rather than as adults entitled to decide about their own lives.",
     "The modern emphasis on informed consent reverses this assumption, holding that a patient must understand the options before agreeing to any of them.",
     "Even so, consent is only as meaningful as the explanation behind it, and a hurried list of risks can leave a patient formally informed but no wiser."],
    "Confidentiality, the duty not to reveal a patient's condition to other people, is a long-standing principle of medical ethics.",
    "The paragraph is about what patients themselves are told: doctors once withheld the truth ([[1]]), 'Such paternalism' disrespected patients ([[2]]), informed consent 'reverses this assumption' ([[3]]), and consent still depends on a real explanation ([[4]]). Sentence [[X]] belongs to medical ethics as well, but it concerns disclosure to third parties, which is a different relationship; it neither continues the history of paternalism nor bears on the quality of consent.",
    "Accepting sentence [[X]] because it is about disclosure and medical ethics, without noticing that it concerns others learning about the patient rather than the patient learning the truth.",
    "V03C-medical-paternalism", "The odd sentence shares the vocabulary of medical ethics and of disclosure; the solver must notice that the direction of disclosure is different.",
    traps=[(4, "Sentence [[4]] may seem to undercut the paragraph, but 'Even so' marks a qualification of sentence [[3]]: consent is the right ideal, but it needs a genuine explanation.")])

ooo("V03-C-012", "Philosophy and ethics", "People see a moral difference between lying and misleading, a difference critics doubt.", "Easy",
    ["Many people sense an ethical gap between an outright lie and a true statement chosen in order to mislead.",
     "Asked whether he has eaten the last biscuit, a child who replies 'I had my dinner hours ago' has not lied, though he plainly hopes to deceive.",
     "Defenders of the distinction say that the misleader at least leaves the listener room to ask a further question, whereas the liar closes it off.",
     "Critics reply that the listener ends up just as deceived in either case, so that the difference is one of technique rather than of morality."],
    "Most children tell their first lies at a young age, and parents often find the discovery more alarming than it needs to be.",
    "Sentence [[1]] states the distinction, sentence [[2]] illustrates misleading without lying, sentence [[3]] gives the defence of 'the distinction', and sentence [[4]] gives the critics' reply. Sentence [[X]] is about lying, but it concerns children's development and parents' reactions, not the moral difference between lying and misleading.",
    "Being misled by the child in sentence [[2]] into thinking a sentence about children's lies belongs.",
    "V03C-lying-versus-misleading", "Once the defence-and-reply structure is seen, the sentence about child development is plainly outside it.",
    traps=[(2, "Sentence [[2]] is about a child, which may make it look like the odd one, but it is the example of truthful misleading that sentences [[3]] and [[4]] go on to discuss.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ Psychology
ooo("V03-C-013", "Psychology", "We overrate how much others notice us, because each of us is at the centre of our own attention.", "Easy",
    ["People tend to overestimate how much others notice about them, from a stain on a shirt to a stumble over a word in a meeting.",
     "The error arises partly because each of us is the centre of our own attention, and we assume, without quite realising it, that we are at the centre of other people's attention too.",
     "In fact, those around us are mostly busy with their own affairs, not least with anxieties about the impression they are making.",
     "Seeing this clearly can bring a certain relief, because the watchers we dread are much less attentive than we suppose."],
    "Many people dread speaking in public and will go to considerable lengths to avoid being asked to address a meeting.",
    "Sentence [[1]] names a tendency, sentence [[2]] explains 'The error', sentence [[3]] corrects the false assumption ('In fact'), and sentence [[4]] draws the consequence of 'Seeing this clearly'. Sentence [[X]] is about social anxiety and mentions meetings, but it describes a fear of public speaking; it says nothing about overestimating how much others notice, and nothing in the paragraph refers to it.",
    "Linking sentence [[X]] to 'the watchers we dread' in sentence [[4]] and so treating it as part of the argument.",
    "V03C-spotlight-effect-self-consciousness", "The shared vocabulary of meetings and fear is slight; the explain-correct-conclude chain is easy to follow.",
    traps=[(4, "Sentence [[4]] uses the word 'dread', which may make it look like the odd one, but 'Seeing this clearly' refers to the correction in sentence [[3]] and draws the paragraph's conclusion.")],
    cognitive="Understanding")

ooo("V03-C-014", "Psychology", "Honouring money already spent distorts present choices, though the habit may serve a wish for consistency.", "Medium",
    ["Having paid for a concert ticket, many people will travel through a storm to attend, even when they would by then much rather stay at home.",
     "The money is gone whether they go or not, so the only question that ought to matter is which evening they would now prefer.",
     "Yet the thought of 'wasting' the ticket pulls them out of the door, as though attending could somehow recover what was spent.",
     "Economists call this honouring of sunk costs an error, though some psychologists suggest it may reflect a reasonable wish to appear consistent to oneself and to others."],
    "Buying tickets well in advance is often sensible, since the price of seats for a popular event tends to rise as the date approaches.",
    "Sentence [[1]] gives the case, sentence [[2]] states what a rational choice would consider, sentence [[3]] ('Yet') shows how people actually reason, and sentence [[4]] names 'this honouring of sunk costs' and qualifies the verdict. Sentence [[X]] is about concert tickets, but it is advice on when to buy; the paragraph is about how money already spent distorts a later decision, and the timing of a purchase plays no part in that.",
    "Accepting sentence [[X]] because it is about the price of tickets, the same object as in the example.",
    "V03C-sunk-cost-reasoning", "The odd sentence shares the example's vocabulary of tickets and prices, so it is rejected because it gives purchasing advice rather than contributing to the argument about sunk costs.",
    traps=[(4, "Sentence [[4]] may look like a shift because it introduces a defence of the behaviour, but 'this honouring of sunk costs' names exactly the reasoning shown in sentence [[3]], and the qualification completes the paragraph.")])

ooo("V03-C-015", "Psychology", "More options add the work of comparison, so the value of choice depends on ways of narrowing it.", "Medium",
    ["It seems obvious that more choice is always welcome, since a shopper offered forty kinds of tea can still pick whichever one she would have chosen from five.",
     "But each added option also adds work, because the alternatives must be compared, and the comparison grows harder as the list grows longer.",
     "Faced with too many, some people put off deciding altogether, while others do choose and then dwell on the options they left behind.",
     "The lesson is not that choice is bad, but that its value depends on whether people have some way, such as trusted advice or a simple rule, of narrowing it down."],
    "Shops arrange their shelves with care, often placing the most profitable products at eye level, where shoppers are most likely to notice them.",
    "Sentence [[1]] states the common assumption, sentence [[2]] ('But') objects that options carry a cost, sentence [[3]] describes the effects of 'too many', and sentence [[4]] gives the balanced lesson. Sentence [[X]] is about shoppers and products, but it concerns how shops steer attention for profit, not how the number of options affects the person choosing.",
    "Keeping sentence [[X]] because the paragraph's example is a shopper, and taking a sentence about shopping to be part of the argument.",
    "V03C-choice-overload", "The odd sentence shares the shopping setting, so the solver must reject it on what it says about choice rather than on its subject.",
    traps=[(4, "Sentence [[4]] may seem to soften the argument too much to belong, but 'The lesson is not that choice is bad' is the conclusion that sentences [[1]], [[2]] and [[3]] lead to.")])

ooo("V03-C-016", "Psychology", "Habits depend on cues, so moving house breaks old routines and offers a good moment to change.", "Medium",
    ["Much of what we call habit is less a matter of willpower than of cues, since a familiar place or hour can set off an action before we have decided anything.",
     "This is why people who move house often find that old routines, good and bad, are suddenly easier to break.",
     "The cues that used to trigger them have vanished, and for a short while behaviour must be chosen deliberately rather than performed automatically.",
     "Someone hoping to change a habit may therefore do well to begin during such a disruption, when the old prompts have lost their grip."],
    "Forming a new habit can take weeks or months of repetition, and the time required seems to vary a good deal from one person to another.",
    "Sentence [[1]] claims that habits depend on cues, sentence [[2]] gives the moving-house case ('This is why'), sentence [[3]] explains it (the cues 'have vanished'), and sentence [[4]] draws the practical conclusion about 'such a disruption'. Sentence [[X]] is about habits too, but it concerns how long a habit takes to form; the paragraph's argument is about cues and the opportunity created when they disappear, and nothing in it depends on how long repetition takes.",
    "Taking any sentence about habit formation to belong, without checking that the paragraph is specifically about cues.",
    "V03C-habits-and-context-cues", "The odd sentence shares the vocabulary of habit and change, so it must be rejected on function rather than topic.",
    traps=[(3, "Sentence [[3]] may seem to repeat sentence [[1]], but it explains the moving-house example of sentence [[2]] and supplies the 'disruption' that sentence [[4]] recommends using.")])

ooo("V03-C-017", "Psychology", "Boredom is a useful signal to seek something better, and smothering it at once with distraction silences it.", "Difficult",
    ["Boredom is usually treated as a problem to be solved, an empty discomfort that a phone or a television can quickly relieve.",
     "Yet its very unpleasantness may be the point, since it tells us that what we are doing no longer repays our attention and that we should look for something that does.",
     "Understood in this way, boredom resembles hunger: disagreeable in itself, but useful for what it prompts us to go and find.",
     "If every flicker of it is smothered at once by the nearest distraction, the signal is silenced before it can lead anywhere more rewarding."],
    "Some people seem far more prone to boredom than others, and a few will seek out risk and danger simply to escape the feeling.",
    "The four sentences argue that boredom has a function: it is usually seen as a mere discomfort ([[1]]), 'Yet' it signals that we should look for something better ([[2]]), it is 'in this way' like hunger ([[3]]), and quick distraction silences 'the signal' ([[4]]). Sentence [[X]] is about boredom and about seeking something new, which makes it tempting, but it shifts to differences between individuals and presents the seeking as reckless escape. The paragraph is about what the state of boredom does for anyone who feels it, and sentence [[X]] neither develops the signal idea nor connects to 'the nearest distraction' in sentence [[4]].",
    "Seeing 'seek out risk' as a version of 'look for something that does' in sentence [[2]], and missing that sentence [[X]] is about a personal trait and treats seeking as escape rather than as the useful response the paragraph describes.",
    "V03C-uses-of-boredom", "The odd sentence shares both the subject and the idea of seeking something new; the solver must notice the shift from the function of a state to differences between people, while also judging the hunger analogy to be part of the argument.",
    traps=[(3, "Sentence [[3]] may look like a decorative comparison that could be dropped, but 'Understood in this way' ties it to sentence [[2]], and the analogy explains why an unpleasant feeling can still be useful, which sentence [[4]] relies on."),
           (1, "Sentence [[1]] may seem to state a view the author rejects and so to be out of place, but sentence [[2]] begins 'Yet', which needs this common view to answer, and sentence [[4]] returns to its 'a phone or a television' as 'the nearest distraction'.")],
    exams=D)

# ------------------------------------------------------------------ Society and culture
ooo("V03-C-018", "Society and culture", "Gifts create vague obligations whose very vagueness keeps relationships going.", "Medium",
    ["A gift appears to be the opposite of a trade, since nothing is asked for in return and any mention of payment would spoil it.",
     "Yet in many societies a gift creates an obligation all the same, and a person who never reciprocates soon finds the gifts drying up.",
     "The obligation is kept deliberately vague, however: the return must come later, in a different form, and never as an exact equivalent.",
     "That vagueness is what keeps the relationship open, because a debt repaid precisely would close the account, whereas an uneven exchange invites a further round."],
    "Choosing a gift well requires knowing the tastes of the person who receives it, which is why a thoughtful present is often valued above an expensive one.",
    "Sentence [[1]] gives the appearance (a gift is not a trade), sentence [[2]] ('Yet') shows that gifts still create obligations, sentence [[3]] says 'The obligation' is kept vague, and sentence [[4]] explains what 'That vagueness' achieves. Sentence [[X]] is about gifts, but it concerns how to choose a good one; the paragraph is about reciprocity and obligation, and the quality of a present plays no part in that argument.",
    "Treating a sentence about the value of gifts as part of a paragraph about the obligations they create.",
    "V03C-gifts-and-reciprocity", "The odd sentence shares the subject and even a contrast about value, so it is rejected on function, not topic.",
    traps=[(1, "Sentence [[1]] may look like a claim the paragraph abandons, but sentence [[2]] needs it for 'Yet ... all the same', and sentence [[4]] returns to the language of trade with 'a debt repaid' and 'the account'.")])

ooo("V03-C-019", "Society and culture", "Names that parents think original rise and fall together, and so come to mark a generation.", "Easy",
    ["Parents choosing a name for a child usually believe they are making a personal and even original decision.",
     "Yet names rise and fall in popularity in broad waves, so that a name chosen for its freshness may turn out to be shared by several children in the same class.",
     "The reason is that parents draw on the same pool of sounds and associations at the same moment, often without being aware of it.",
     "A name that once seemed distinctive can therefore come to mark its bearer as belonging to a particular generation."],
    "In some cultures a child is not formally named until several days after birth, when a ceremony is held for the purpose.",
    "Sentence [[1]] states the parents' belief, sentence [[2]] ('Yet') shows that names move in waves, sentence [[3]] gives 'The reason', and sentence [[4]] draws the consequence ('therefore'). Sentence [[X]] is about naming, but it describes when and how a name is formally given in some cultures; it has nothing to do with fashions in names or with parents' sense of originality.",
    "Keeping sentence [[X]] simply because it is about naming children.",
    "V03C-naming-fashions", "The odd sentence shares the topic of naming but clearly changes the point to ceremony.",
    traps=[(4, "Sentence [[4]] may look like a new idea about generations, but 'therefore' marks it as the result of the waves described in sentences [[2]] and [[3]].")],
    cognitive="Understanding")

ooo("V03-C-020", "Society and culture", "The debate over teaching handwriting turns on whether the hand teaches the mind something the keyboard does not.", "Medium",
    ["As more writing is done on keyboards, many schools have reduced the time they spend teaching children to write by hand.",
     "Some teachers regret this, arguing that forming letters by hand helps young children learn to recognise them and to remember what they write.",
     "Others reply that what matters is fluency with whatever tool a child will actually use, and that hours spent on joined-up script could go to other skills.",
     "The disagreement is less about nostalgia than about a real question: whether the hand teaches the mind something that the keyboard does not."],
    "Handwriting analysis is sometimes offered as a way of judging a person's character, though there is little good evidence that it works.",
    "Sentence [[1]] describes the change in schools, sentences [[2]] and [[3]] give the two sides ('Some teachers' and 'Others'), and sentence [[4]] names what 'The disagreement' is really about. Sentence [[X]] is about handwriting, but it concerns reading character from it; the paragraph is about whether children should be taught to write by hand, and the claims of handwriting analysis play no part in that debate.",
    "Accepting sentence [[X]] because it, like sentence [[2]], links handwriting to the mind.",
    "V03C-decline-of-handwriting", "The odd sentence shares the subject and a link between handwriting and the mind, so it is rejected on function within the debate about teaching.",
    traps=[(4, "Sentence [[4]] may seem to step back from the debate, but 'The disagreement' refers to the two sides in sentences [[2]] and [[3]], and it is the paragraph's conclusion.")])

ooo("V03-C-021", "Society and culture", "Minority languages usually fade when parents stop passing them on, which is where efforts to save them should focus.", "Medium",
    ["A minority language need not disappear because anyone forbids it; often, parents simply stop passing it on to their children.",
     "They do so for understandable reasons, believing that fluency in the dominant language will open doors to schooling and work.",
     "Their children grow up able to understand the old language but reluctant to speak it, and their grandchildren may not understand it at all.",
     "For this reason, efforts to save such languages that rely only on dictionaries and recordings, valuable as they are, miss the point at which the chain actually breaks."],
    "Some minority languages contain words for plants, places and practices that have no exact equivalent in the dominant language.",
    "The paragraph traces how a language is lost between generations: parents stop passing it on ([[1]]), for understandable reasons ([[2]]), so their children and grandchildren lose it ([[3]]), and efforts to save it must therefore address that break ([[4]], 'the chain'). Sentence [[X]] concerns minority languages too, but it argues for what they contain and so for their value; the paragraph is about the mechanism of loss, and sentence [[X]] does not connect to the passing on of the language.",
    "Taking sentence [[X]] as part of the argument because it seems to explain why such languages are worth saving, a point the paragraph never makes.",
    "V03C-minority-language-shift", "The odd sentence shares the subject and could seem to motivate the closing talk of saving languages, so it is rejected on function.",
    traps=[(4, "Sentence [[4]] may look like a policy point added at the end, but 'For this reason' and 'the chain' tie it to the generational break described in sentences [[1]], [[2]] and [[3]].")])

# ------------------------------------------------------------------ History and politics
ooo("V03-C-022", "History and politics", "Railway timetables made local solar time unworkable and led to standard time.", "Easy",
    ["Before the railways, most towns kept their own local time, setting their clocks by the position of the sun overhead.",
     "Noon in one town might therefore fall several minutes earlier or later than noon in a town a short distance to the east or west.",
     "Such differences hardly mattered while travel was slow, but they caused real confusion once trains began to run to published timetables over long distances.",
     "Railway companies accordingly adopted a single standard time along their lines, and in time whole countries followed their example."],
    "Early railway carriages were often open to the weather, and passengers in the cheapest seats travelled with little protection from wind and rain.",
    "Sentence [[1]] describes local solar time, sentence [[2]] gives its consequence ('therefore'), sentence [[3]] explains why 'Such differences' became a problem with railways, and sentence [[4]] describes the response ('accordingly'). Sentence [[X]] is about early railways, but it describes the comfort of carriages; it has nothing to do with timekeeping.",
    "Keeping sentence [[X]] because it is about early railways, which the paragraph also mentions.",
    "V03C-railways-and-standard-time", "The odd sentence is about railways but plainly not about time, so the chain of 'therefore', 'such differences' and 'accordingly' makes it easy to reject.",
    traps=[(2, "Sentence [[2]] may look like a technical aside, but 'Such differences' in sentence [[3]] needs it as an antecedent.")],
    cognitive="Understanding")

ooo("V03-C-023", "History and politics", "Archives record what institutions chose to keep, so historians read them against their purpose, within limits.", "Difficult",
    ["An archive is not a neutral sample of the past but a deposit of what particular institutions thought worth writing down and keeping.",
     "The resulting silences are not random: a tax office records who owed what, a court records who was accused of what, and people who neither paid much nor offended anyone may leave hardly a trace.",
     "Historians have learned to read such records against their purpose, finding in a list of debts or a trial transcript glimpses of lives the clerks never meant to describe.",
     "Even so, there are limits to what this method can recover, and where the documents fall silent the honest course is to mark the gap rather than fill it with conjecture."],
    "Many archives have also suffered losses through fire, flood and neglect, so that some records once carefully kept now survive only in fragments.",
    "The paragraph argues that archival silence reflects what institutions chose to record ([[1]]), that these silences fall on particular kinds of people ([[2]], 'not random'), that historians answer this bias by reading records 'against their purpose' ([[3]]), and that 'this method' has limits ([[4]]). Sentence [[X]] also concerns gaps in archives, which makes it tempting, but it describes accidental destruction, the kind of loss that sentence [[2]] sets aside by calling the silences 'not random'. Reading against the purpose of a record is a reply to what clerks chose to note, not to what fire destroyed, so sentence [[X]] does not connect to the method the paragraph goes on to discuss.",
    "Accepting sentence [[X]] because it, like sentence [[4]], is about gaps in the record, without noticing that the paragraph is about gaps produced by selection rather than by accident.",
    "V03C-silences-of-archives", "The odd sentence shares the theme of gaps in the record and the vocabulary of archives; it is rejected only by seeing that the paragraph's silences are chosen, not accidental, and that the method it describes answers selection alone.",
    traps=[(4, "Sentence [[4]] may look as if it moves to a separate point about honesty, but 'this method' refers to reading records 'against their purpose' in sentence [[3]], and the paragraph needs this limit as its qualification."),
           (2, "Sentence [[2]] may look like a list of examples that could be dropped, but 'such records' in sentence [[3]] refers to its tax and court records, and its claim that the silences are 'not random' carries the argument of sentence [[1]] forward.")],
    exams=D)

ooo("V03-C-024", "History and politics", "Every causal claim in history contains a counterfactual, so the choice is to state such claims openly or leave them hidden.", "Medium",
    ["Historians are often warned against asking what would have happened if events had gone differently, on the ground that such questions cannot be answered.",
     "Yet every claim that one thing caused another quietly contains a counterfactual, since to say a drought caused a revolt is to imply that without the drought the revolt would not have occurred, or not then.",
     "The real choice, then, is not between using counterfactuals and avoiding them, but between stating them openly and leaving them unexamined.",
     "Stated openly, they can at least be tested against what is known of the period, and the most fanciful among them can be set aside."],
    "Novelists have long been drawn to imagined histories in which a famous battle was lost or a great invention was never made.",
    "Sentence [[1]] states the warning against counterfactual questions, sentence [[2]] ('Yet') shows that causal claims contain them anyway, sentence [[3]] draws the conclusion ('then') about the real choice, and sentence [[4]] explains the advantage of stating them 'openly'. Sentence [[X]] is about imagined histories, but it concerns fiction; the paragraph is about how historians reason about causes, and novelists' alternative histories play no part in that argument.",
    "Accepting sentence [[X]] because it, like the paragraph, imagines events going differently.",
    "V03C-counterfactual-history", "The odd sentence shares the idea of history going differently, so it must be rejected because it concerns fiction, not historical method.",
    traps=[(4, "Sentence [[4]] may look like an extra point, but 'Stated openly' picks up the option named in sentence [[3]] and shows why it is the better one.")])

ooo("V03-C-025", "History and politics", "Printing for vernacular readers forced printers to choose spellings, which helped standardise written languages.", "Easy",
    ["As printing spread through Europe, a growing share of books came to be produced in the languages people spoke rather than in Latin.",
     "Printers had every reason to encourage this, since a book in a widely spoken tongue could reach far more buyers than one in a learned language.",
     "Producing such books, however, forced printers to choose among many regional spellings and dialects, and the forms they chose spread with their books.",
     "In this way the needs of a commercial trade helped to fix the standard written forms of several modern languages."],
    "Before printing, books were copied by hand, and a single volume could take a scribe many months to complete.",
    "Sentence [[1]] describes the shift to vernacular books, sentence [[2]] gives the printers' motive ('this'), sentence [[3]] shows the consequence for spelling ('such books'), and sentence [[4]] sums up the effect ('In this way'). Sentence [[X]] is about books, but it describes hand copying before printing; it belongs to a different period and plays no part in the argument about printing and standard languages.",
    "Keeping sentence [[X]] because it is about the history of books, without checking that the paragraph concerns printing and language.",
    "V03C-print-and-vernaculars", "The odd sentence shares the subject of books but is about a different period and process, which is easy to see.",
    traps=[(2, "Sentence [[2]] may look like a commercial aside, but it explains the shift in sentence [[1]] and prepares 'the needs of a commercial trade' in sentence [[4]].")],
    cognitive="Understanding")
