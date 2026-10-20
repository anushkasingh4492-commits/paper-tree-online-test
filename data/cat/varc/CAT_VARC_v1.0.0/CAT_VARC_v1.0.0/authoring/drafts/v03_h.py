import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ 001 Easy, night markets
ooo("V03-H-001", "Cities and geography",
    "Night markets make cheap, flexible use of urban space that would otherwise lie idle after dark.", "Easy",
    ["Night markets turn streets that carry traffic by day into places of trade and sociability after dark.",
     "Because the stalls are set up and taken down every evening, they need almost no permanent infrastructure beyond lighting, water and a cleared surface.",
     "This low cost of entry lets a small vendor try out a product, such as a new snack or a handmade item, without committing to a shop lease.",
     "For the city, the result is a lively use of space that would otherwise stand empty, achieved with very little public spending."],
    "Many visitors insist that the food at night markets tastes better than the same dishes served in restaurants.",
    "Sentence [[1]] introduces night markets as an after-dark use of streets. Sentence [[2]] explains why they need so little infrastructure, sentence [[3]] ('This low cost of entry') draws the benefit for vendors, and sentence [[4]] states the benefit for the city. Sentence [[X]] mentions night markets but reports visitors' opinions about taste, which has nothing to do with the paragraph's point about cheap, flexible use of space.",
    "Picking a sentence that mentions vendors or the city instead of noticing that the paragraph is about cost and use of space.",
    "V03H-night-markets",
    "The odd sentence keeps the subject but its focus on taste is clearly separate from the economic argument.",
    traps=[(3, "Sentence [[3]] can look like a narrow aside about snacks, but 'This low cost of entry' picks up sentence [[2]] and supplies the vendor's side of the benefit that sentence [[4]] completes for the city.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 002 Easy, gated communities
ooo("V03-H-002", "Cities and geography",
    "Gated communities supply private order to residents but weaken pressure for public services and so widen urban divides.", "Easy",
    ["Gated communities promise their residents a degree of safety and order that the surrounding city seems unable to supply.",
     "Behind the wall, private guards, well-kept parks and reliable services are paid for through fees that only residents contribute.",
     "Yet the very success of this arrangement weakens the incentive of its wealthiest residents to press for better public services outside it.",
     "Over time the city divides into tended enclaves and neglected streets between them, and the gap the walls were meant to shut out grows wider."],
    "Developers often market gated communities under names that call to mind country estates, lakes or distant foreign cities.",
    "Sentence [[1]] states the promise of gated communities, sentence [[2]] explains how it is delivered privately, sentence [[3]] ('Yet the very success of this arrangement') turns to the cost, and sentence [[4]] describes the long-run result for the city. Sentence [[X]] is about gated communities but concerns how they are advertised, which plays no part in the argument about private provision and public neglect.",
    "Treating any sentence about gated communities as part of the paragraph without asking what the paragraph argues.",
    "V03H-gated-communities",
    "The odd sentence is on the same subject but its marketing focus is plainly outside the argument.",
    traps=[(2, "Sentence [[2]] may look like mere description, but the fees 'that only residents contribute' are what sentence [[3]] calls 'this arrangement', the source of the weakened incentive.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 003 Medium, urban groundwater depletion
ooo("V03-H-003", "Cities and geography",
    "Private borewells are individually sensible but together deplete a shared aquifer whose cost no single pumper bears.", "Medium",
    ["In many growing cities, households and businesses that cannot rely on the piped supply sink borewells of their own.",
     "Each well is a sensible private response to an unreliable public service, and the water it draws is cheap because no one pays for what is left in the aquifer.",
     "Taken together, however, thousands of such wells lower the water table faster than the monsoon can recharge it, so every owner must drill deeper every few years.",
     "The cost of the shortage thus falls on everyone who shares the aquifer, while the benefit of each extra litre pumped goes only to the person pumping it."],
    "Groundwater that has lain undisturbed for a long time often carries dissolved minerals that make it unpleasant to drink without treatment.",
    "Sentence [[1]] introduces private borewells, sentence [[2]] explains why each is individually rational, sentence [[3]] ('Taken together, however') shows the collective effect on the water table, and sentence [[4]] ('thus') draws the conclusion that costs are shared while benefits are private. Sentence [[X]] is about groundwater too, but it concerns water quality, whereas the paragraph is about the depletion of a shared stock.",
    "Choosing a sentence on the strength of its being about groundwater, and missing that the paragraph's subject is depletion and who bears its cost.",
    "V03H-urban-groundwater-depletion",
    "The odd sentence shares the key noun (groundwater) and must be rejected because quality is a different problem from depletion.",
    traps=[(2, "Sentence [[2]] can look like a side remark about price, but its point that no one pays 'for what is left in the aquifer' is the private logic that sentences [[3]] and [[4]] turn into a shared cost.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 004 Difficult, floodplain zoning
ooo("V03-H-004", "Cities and geography",
    "Embankments invite development onto floodplains and so raise the losses from rare floods; keeping floodplains open can be cheaper protection.", "Difficult",
    ["When a town builds an embankment along its river, the land behind it suddenly looks safe enough for houses, shops and schools.",
     "Development follows, and within a generation far more property stands on the floodplain than stood there before the defence was raised.",
     "The embankment works as designed, holding back the ordinary floods of most years, but when a rare flood overtops it the damage exceeds anything the unprotected town could have suffered.",
     "This is why some planners argue that keeping floodplains as parks or farmland, though it looks like a waste of valuable land, is the cheaper form of protection."],
    "Earth embankments also fail far more often than their designers expect, because seepage weakens them long before the river reaches its peak.",
    "The paragraph's argument is behavioural: the embankment makes land look safe (sentence [[1]]), development follows (sentence [[2]]), and so a defence that 'works as designed' still raises losses when a rare flood overtops it (sentence [[3]]); 'This is why' in sentence [[4]] draws the planning conclusion. Sentence [[X]] attacks embankments on engineering grounds, claiming they often fail, which contradicts the concession in sentence [[3]] that the embankment works as designed and replaces the paragraph's mechanism (more property exposed) with a different one (structural failure).",
    "Choosing the concession in sentence [[3]] because it seems to defend embankments, or keeping sentence [[X]] because it also sounds critical of embankments.",
    "V03H-floodplain-zoning",
    "The odd sentence shares the paragraph's scepticism about embankments, so it must be rejected because it changes the mechanism and clashes with the concession.",
    traps=[(3, "Sentence [[3]] concedes that embankments work, which can look out of place in a critical paragraph, but it is the hinge of the argument: the losses grow even when the defence performs, and 'This is why' in sentence [[4]] refers to it."),
           (4, "Sentence [[4]] introduces planners, but it is the conclusion the whole chain leads to, and without it the paragraph has no point.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 005 Medium, paradox of tolerance
ooo("V03-H-005", "Philosophy and ethics",
    "Toleration may exclude those who would destroy it, but only if the exception is drawn narrowly at organised action.", "Medium",
    ["A society that tolerates every view, including views that seek to abolish toleration, seems to risk being undone by its own generosity.",
     "The usual answer is that toleration may refuse protection to those who would destroy it, much as a club may expel members who set out to wreck the club.",
     "But this answer is safe only if the exception is drawn narrowly, at the point where intolerant speech becomes organised action against the freedom of others.",
     "Drawn more widely, at mere disagreement with liberal values, it would license precisely the suppression that toleration was meant to prevent."],
    "Historically, toleration first emerged as a truce between rival communities exhausted by war, rather than as an ideal valued for its own sake.",
    "Sentence [[1]] poses the puzzle, sentence [[2]] gives 'the usual answer', sentence [[3]] ('But this answer') qualifies it, and sentence [[4]] ('Drawn more widely') shows the danger of an exception drawn too broadly. Sentence [[X]] is about toleration but gives a historical account of its origin, which does nothing to resolve or qualify the logical puzzle the paragraph works through.",
    "Picking sentence [[4]] because it seems to oppose the answer in sentence [[2]], when it actually completes the qualification begun in sentence [[3]].",
    "V03H-paradox-of-tolerance",
    "The odd sentence shares the key term and must be rejected because history of origins is a different question from the limits of toleration.",
    traps=[(4, "Sentence [[4]] has no subject of its own until one sees that 'it' is the exception from sentence [[3]]; it supplies the reason the exception must be narrow.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 006 Medium, veil of ignorance
ooo("V03-H-006", "Philosophy and ethics",
    "Choosing rules without knowing one's own position makes self-interest yield impartiality, though critics question the assumed caution.", "Medium",
    ["One way to test whether a rule is fair is to imagine choosing it without knowing what place you will occupy in the society it governs.",
     "Unable to tell whether you will be rich or poor, healthy or ill, you cannot tilt the rule toward your own advantage.",
     "Self-interest, which normally corrupts judgements about justice, is thereby made to do the work of impartiality.",
     "Critics reply that the device yields cautious, protective rules only if we assume that the chooser is unwilling to gamble on landing near the top."],
    "Judges in many legal systems are expected to step aside from cases in which they have a personal stake in the outcome.",
    "Sentence [[1]] sets out the thought experiment, sentence [[2]] explains its effect, sentence [[3]] ('thereby') states what it achieves, and sentence [[4]] reports the critics' reply to 'the device'. Sentence [[X]] shares the theme of impartiality, but it describes an institutional rule for judges, not the imagined choice the paragraph analyses, and nothing in the paragraph refers to it.",
    "Being drawn to sentence [[X]] by the shared idea of impartiality, or dropping the critics' sentence [[4]] because it disagrees with the rest.",
    "V03H-veil-of-ignorance",
    "The odd sentence shares the theme of impartiality; it must be rejected because it concerns a real-world rule rather than the thought experiment.",
    traps=[(4, "Sentence [[4]] disagrees with the device, but 'the device' refers back to the thought experiment, and a reported objection is a normal part of such a paragraph.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 007 Easy, whistleblowing and loyalty
ooo("V03-H-007", "Philosophy and ethics",
    "Whistleblowing can be loyalty to an institution's purpose, though loyalty still asks for internal channels first where they work.", "Easy",
    ["A nurse who reports unsafe practices to an outside regulator will often hear that she has let down her own hospital.",
     "Behind that reproach lies the idea that fidelity is owed to colleagues and superiors, regardless of their conduct.",
     "Yet a hospital exists to heal, and staff who hide dangers to patients betray that purpose far more deeply than anyone who brings the dangers to light.",
     "This does not make every disclosure an act of fidelity, for the institution may still ask that warnings be raised internally first, wherever internal channels genuinely work."],
    "In several countries the law now shields employees who report fraud from dismissal, though such protection is often hard to enforce.",
    "Sentence [[1]] states the accusation against the nurse, sentence [[2]] ('that reproach') exposes the view of loyalty behind it, sentence [[3]] ('Yet') reverses it by appeal to the hospital's purpose, and sentence [[4]] ('This does not make every disclosure') adds a qualification about internal channels. Sentence [[X]] is about legal protection, a practical matter, while the paragraph is a moral argument about what loyalty means.",
    "Mistaking the qualification in sentence [[4]] for a change of subject.",
    "V03H-whistleblowing-and-loyalty",
    "The odd sentence moves from the ethics of loyalty to law, a clear change of focus.",
    traps=[(4, "Sentence [[4]] limits the argument, but it is still about what fidelity to the institution requires, so it belongs.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 008 Difficult, moral relativism
ooo("V03-H-008", "Philosophy and ethics",
    "Relativism adopted out of modesty undermines itself, because its ban on imposition is a universal rule relativism rejects.", "Difficult",
    ["Many people adopt moral relativism out of modesty: since no society can show its own code to be superior, none is entitled to force that code on others.",
     "Yet the conclusion, that no society may force its code on others, is itself offered as binding on every society, which is the very sort of universal rule relativism rejects.",
     "If each society's morality is valid only for itself, a society whose morality approves of conquest is, by the relativist's own standard, beyond criticism.",
     "The humility that drew people to relativism therefore needs a firmer footing than relativism can offer it."],
    "Anthropologists have recorded wide variation in moral codes, though a few values, such as care for one's own children, appear almost everywhere.",
    "The paragraph is a logical critique: sentence [[1]] gives the motive for relativism, sentence [[2]] ('Yet the conclusion') shows that the motive relies on a universal rule, sentence [[3]] shows that relativism cannot condemn conquest, the very imposition the motive objected to, and sentence [[4]] ('therefore') concludes. Sentence [[X]] reports what moral codes are actually like, a descriptive question, and its remark about near-universal values pulls in a different direction; no other sentence uses it, and it neither supports nor is answered by the critique.",
    "Keeping sentence [[X]] because it seems to give the empirical background to relativism, without noticing that the paragraph argues only about whether relativism is coherent.",
    "V03H-moral-relativism",
    "The odd sentence shares the subject and could pass as background; rejecting it needs the distinction between describing moral variety and the normative claim under attack.",
    traps=[(3, "Sentence [[3]] can look like a fresh objection, but conquest is the imposition that sentence [[1]] said relativism forbids, so it shows relativism failing its own motive and sets up 'therefore' in sentence [[4]].")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 009 Easy, anchoring effect
ooo("V03-H-009", "Psychology",
    "An arbitrary number seen beforehand pulls estimates towards it, a tendency used in negotiation and hard to resist.", "Easy",
    ["When people estimate an unknown quantity, an arbitrary number they have just seen tends to pull their estimate towards it.",
     "Suppose a class first writes down the last two digits of their phone numbers and then guesses the price of an unfamiliar object; the guesses would be expected to drift towards those digits.",
     "Negotiators exploit the same tendency when they open with an extreme offer, knowing that the counter-offer will be framed in relation to it.",
     "The pull is hard to resist even for people who know about it, which suggests that it works below the level of deliberate reasoning."],
    "Many shoppers respond to prices ending in nine, which seem noticeably lower than the round number just above them.",
    "Sentence [[1]] states the anchoring tendency, sentence [[2]] illustrates it with a hypothetical classroom case, sentence [[3]] ('the same tendency') applies it to negotiation, and sentence [[4]] ('The pull') comments on how hard it is to resist. Sentence [[X]] is about prices and numbers but describes a different effect, the appeal of prices ending in nine, which involves no prior arbitrary number pulling an estimate.",
    "Accepting sentence [[X]] because it, too, is about numbers and prices.",
    "V03H-anchoring-effect",
    "The odd sentence describes a different pricing effect; the difference is easy to see once the definition in the first sentence is read.",
    traps=[(2, "Sentence [[2]] is hypothetical and might look like an aside, but it is the illustration of the effect that sentence [[3]] then calls 'the same tendency'.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 010 Medium, learned helplessness
ooo("V03-H-010", "Psychology",
    "Repeated uncontrollable failure teaches a lesson about the self, which is why passivity persists and spreads to new settings.", "Medium",
    ["When effort repeatedly makes no difference to outcomes, people and animals alike may stop trying.",
     "What is striking is that the passivity outlasts the circumstances that produced it, so that an escape which has become easy goes unattempted.",
     "The lesson absorbed is not about one situation but about oneself: that one's actions do not matter.",
     "Because that lesson travels from one setting to another, a student who has failed again and again in mathematics may give up quickly on a history essay as well."],
    "Some failure is useful, since a task at which one never fails is probably too easy to teach one anything.",
    "Sentence [[1]] states the phenomenon, sentence [[2]] adds its striking persistence, sentence [[3]] explains it as a lesson about oneself, and sentence [[4]] ('that lesson') shows the lesson spreading to new settings. Sentence [[X]] also concerns failure, but it argues that failure can be beneficial, a different point from the paragraph's account of how uncontrollable failure produces lasting passivity, and nothing before or after it connects to it.",
    "Choosing sentence [[4]] because the student example seems to shift to schooling, when it actually illustrates the generalising lesson of sentence [[3]].",
    "V03H-learned-helplessness",
    "The odd sentence shares the theme of failure and is rejected on function, since it praises failure rather than explaining passivity.",
    traps=[(4, "Sentence [[4]] moves to a classroom, but 'that lesson' refers to sentence [[3]] and the example shows exactly the transfer the paragraph explains.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 011 Easy, confirmation bias in reading news
ooo("V03-H-011", "Psychology",
    "Readers scrutinise unwelcome news more closely than welcome news, so more information does not correct their bias.", "Easy",
    ["Readers rarely meet the news as neutral judges; they arrive with views and look, often without noticing, for reports that confirm them.",
     "A story that fits their beliefs is accepted after a quick glance, while one that challenges them is read closely for errors.",
     "Since almost any report contains some flaw when inspected closely, this unequal scrutiny lets the reader reject unwelcome news while feeling entirely rational.",
     "The bias is therefore hard to correct by supplying more information, because the extra information passes through the same uneven attention."],
    "Newspapers have long competed for buyers by placing their most sensational stories on the front page.",
    "Sentence [[1]] states the reader's tendency, sentence [[2]] describes the unequal reading of welcome and unwelcome stories, sentence [[3]] ('this unequal scrutiny') explains why it feels rational, and sentence [[4]] ('therefore') concludes that more information will not help. Sentence [[X]] is about newspapers' selling tactics, not about how readers weigh what they read.",
    "Being drawn to sentence [[X]] because it mentions the news.",
    "V03H-confirmation-bias-news",
    "The odd sentence moves from readers' minds to publishers' tactics, an easy shift to spot.",
    traps=[(3, "Sentence [[3]] can look like a general claim about reports, but its phrase 'this unequal scrutiny' ties it to sentence [[2]] and it supplies the step that sentence [[4]] concludes from.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 012 Difficult, framing of choices
ooo("V03-H-012", "Psychology",
    "Equivalent descriptions change choices, but this may reflect reasonable inference of advice from the speaker's frame rather than confusion.", "Difficult",
    ["People told that a treatment has a ninety per cent survival rate tend to accept it more readily than people told that one patient in ten dies.",
     "Since the two descriptions are logically equivalent, the difference seems to show that preferences attach to words rather than to outcomes.",
     "A more charitable reading notes that speakers do not choose frames at random: a doctor who mentions survival is usually signalling that she recommends the treatment.",
     "On this view the listener is not fooled by the wording but is reasonably inferring advice from it, even when no advice was intended."],
    "Choices also shift when one option is set as the default, since many people simply accept whatever has already been selected for them.",
    "Sentence [[1]] gives the framing result, sentence [[2]] draws the sceptical interpretation, sentence [[3]] ('A more charitable reading') offers an alternative interpretation of the same result, and sentence [[4]] ('On this view') spells it out. Sentence [[X]] introduces a different influence on choice, defaults, which involve no equivalent descriptions; placed anywhere it breaks the debate about how to interpret the framing result, and sentence [[3]] would no longer have a reading to be more charitable than.",
    "Treating sentence [[3]] as the odd one because it disagrees with sentence [[2]], or keeping sentence [[X]] because it is also about how choices are swayed.",
    "V03H-framing-of-choices",
    "The odd sentence comes from the same field and even says 'also', so it must be rejected because the paragraph is an argument about interpreting one result.",
    traps=[(3, "Sentence [[3]] reverses the interpretation in sentence [[2]], but that reversal is the paragraph's development, and 'On this view' in sentence [[4]] depends on it."),
           (1, "Sentence [[1]] reads like a stand-alone fact, but it is the result that 'the two descriptions' in sentence [[2]] refers to.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 013 Easy, queueing norms
ooo("V03-H-013", "Society and culture",
    "Queues are kept orderly by the people waiting in them, showing that everyday fairness rests on shared expectations.", "Easy",
    ["A queue is a small social order maintained almost entirely without enforcement.",
     "No official assigns places; each person simply notes who was there first and takes the position behind them.",
     "When someone pushes in, the response usually comes not from staff but from the other people waiting, through glances, remarks or a pointed cough.",
     "That ordinary strangers police the line themselves shows how much of everyday fairness rests on shared expectations rather than rules."],
    "Some banks and post offices now hand out numbered tokens, which let customers sit down while they wait to be called.",
    "Sentence [[1]] states that queues work without enforcement, sentence [[2]] describes how places are taken, sentence [[3]] describes how queue-jumpers are handled by those waiting, and sentence [[4]] ('That ordinary strangers police the line') draws the general lesson. Sentence [[X]] is about waiting, but it describes a formal ticket system, which is not part of the self-policed order the paragraph explains.",
    "Choosing sentence [[3]] because it describes conflict in what is said to be an orderly system.",
    "V03H-queueing-norms",
    "The odd sentence concerns a managed system rather than the informal norm under discussion.",
    traps=[(3, "Sentence [[3]] describes a breach, but the point is who corrects it, the people waiting, which is the evidence sentence [[4]] relies on.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 014 Easy, wedding expenditure
ooo("V03-H-014", "Society and culture",
    "Lavish wedding spending is partly reciprocal hospitality within a network, which makes it hard to scale down even for poorer families.", "Easy",
    ["Lavish weddings are often explained as status competition, each family trying to outdo the last celebration its guests attended.",
     "That account captures something real, but it misses how much of the spending goes to feeding and honouring relatives and neighbours who will one day host the family in turn.",
     "Seen this way, a wedding is partly a repayment of past hospitality and partly a deposit against help in some future crisis.",
     "The difficulty is that such obligations are hard to scale down, so households with modest incomes may borrow heavily to meet them."],
    "Wedding photography has grown into an industry of its own, with couples commissioning elaborate shoots in scenic places months before the ceremony.",
    "Sentence [[1]] gives the usual explanation, sentence [[2]] ('That account') qualifies it by pointing to reciprocal hospitality, sentence [[3]] ('Seen this way') restates the wedding as repayment and deposit, and sentence [[4]] ('such obligations') notes the burden this creates. Sentence [[X]] is about weddings, but it describes a commercial trend unrelated to the argument about status and reciprocal obligation.",
    "Rejecting sentence [[1]] because the paragraph goes on to question it, when it is the view the paragraph responds to.",
    "V03H-wedding-expenditure",
    "The odd sentence keeps the subject but adds a trend that the argument never uses.",
    traps=[(1, "Sentence [[1]] states the view the rest qualifies, and 'That account' in sentence [[2]] needs it.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 015 Difficult, museum repatriation
ooo("V03-H-015", "Society and culture",
    "The claim that universal museums serve humanity fails where those closest to the objects cannot reach them, though return need not improve access.", "Difficult",
    ["Museums that hold objects taken from other countries often defend themselves by claiming to serve all of humanity rather than any one nation.",
     "The claim has force only if humanity can actually reach the collection, and for many people in an object's country of origin, the cost of travel and the difficulty of obtaining a visa put it out of reach.",
     "The universal museum is thus most accessible to the people who have the least connection with many of the things it displays.",
     "None of this shows that every return will improve access, since an object sent home may end up in a storeroom; it shows only that the universal argument cannot settle the question by itself."],
    "Some objects were bought or exchanged on terms thought legitimate at the time, which complicates any single verdict on how such collections were formed.",
    "The paragraph tests one defence, the claim to serve all humanity: sentence [[1]] states it, sentence [[2]] ('The claim has force only if') sets the condition of access, sentence [[3]] ('thus') shows the condition failing for those most connected to the objects, and sentence [[4]] ('None of this') limits the conclusion to that defence. Sentence [[X]] raises a different issue, the legitimacy of how objects were acquired, which the access argument never relies on; although it sounds like a balancing qualification, it qualifies nothing the paragraph has said.",
    "Taking sentence [[X]] for a qualification like sentence [[4]], or treating sentence [[4]] as odd because it seems to argue against returns.",
    "V03H-museum-repatriation",
    "Both the odd sentence and the last coherent sentence are hedging qualifications; separating them needs a clear view of which argument is being qualified.",
    traps=[(4, "Sentence [[4]] seems to turn against returns, but it limits the paragraph's own conclusion about the universal argument, and 'None of this' refers to sentences [[2]] and [[3]].")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 016 Medium, board games revival
ooo("V03-H-016", "Society and culture",
    "Adults play board games despite screens because the inconvenient gathering they require is what they actually seek.", "Medium",
    ["The recent popularity of board games among adults is puzzling at first, since almost any of them could be played more conveniently on a screen.",
     "The puzzle dissolves once we notice that the inconvenience is part of the appeal: players must gather in one room, around one table, at one time.",
     "The game supplies a structure for spending an evening together, with rules that tell everyone when to speak, when to wait and when to laugh at a rival's bad luck.",
     "What is being bought, in other words, is less a game than a reason to be in company without the strain of keeping a conversation going unaided."],
    "Designers of modern board games have moved steadily away from luck towards strategy, so that the more skilful players win more consistently.",
    "Sentence [[1]] poses the puzzle, sentence [[2]] ('The puzzle dissolves') answers it, sentence [[3]] explains how the game structures time together, and sentence [[4]] ('in other words') restates the point as what is really being bought. Sentence [[X]] is about board games but concerns a trend in design, which has nothing to do with why people gather to play; its remark about luck even sits awkwardly beside the 'bad luck' that sentence [[3]] treats as part of the fun.",
    "Choosing sentence [[3]] because it describes rules, as sentence [[X]] does.",
    "V03H-board-games-revival",
    "The odd sentence shares the subject and vocabulary of games and rules, and is rejected because design trends do not explain the social appeal.",
    traps=[(3, "Sentence [[3]] mentions rules, but only as a structure for company, which is exactly what sentence [[4]] sums up.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 017 Medium, tax farming
ooo("V03-H-017", "History and politics",
    "Tax farming gave pre-modern rulers revenue without a bureaucracy but gave collectors reason to squeeze taxpayers.", "Medium",
    ["Many pre-modern states lacked the officials needed to assess and collect taxes across their territories.",
     "Their solution was to auction the right to collect: a private contractor paid the treasury a fixed sum in advance and kept whatever more he could extract.",
     "The arrangement gave rulers predictable revenue without the expense of maintaining a bureaucracy.",
     "But it also gave the collector every reason to squeeze taxpayers hard during his term, since any goodwill he preserved would benefit only his successor."],
    "Taxes on land were generally easier to assess than taxes on trade, because fields could be measured while goods kept moving.",
    "Sentence [[1]] states the problem, sentence [[2]] ('Their solution') gives the auction of collection rights, sentence [[3]] ('The arrangement') states its advantage, and sentence [[4]] ('But it also') states its cost. Sentence [[X]] is about pre-modern taxes, but it compares kinds of tax, a point that neither follows from the shortage of officials nor bears on how tax farming worked; inserted after sentence [[1]] it would also leave 'Their solution' without its proper referent.",
    "Keeping sentence [[X]] because it seems to explain the difficulty of assessment mentioned in sentence [[1]].",
    "V03H-tax-farming",
    "The odd sentence shares the subject and the word 'assess', and must be rejected because the paragraph is about the incentives of a collection system.",
    traps=[(3, "Sentence [[3]] is brief and may look dispensable, but it supplies the benefit that 'But it also' in sentence [[4]] sets against the cost.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 018 Medium, coalition governments
ooo("V03-H-018", "History and politics",
    "Coalitions are less stable but their bargaining yields broader, more durable policy, at the cost of blurred accountability.", "Medium",
    ["Coalition governments are commonly blamed for instability, since the withdrawal of a single partner can bring them down.",
     "Less often noticed is that the need to keep partners on board forces a coalition to bargain, and bargaining tends to strip proposals of their most extreme features.",
     "Policies that survive this process usually command broader support than those a single party could impose, and are therefore less likely to be reversed by the next government.",
     "The price is that voters find it harder to tell which party is responsible for any given decision, and so harder to reward or punish it at the next election."],
    "Smaller parties often agree to join a coalition in the hope of securing a ministry that matters to their own core supporters.",
    "The paragraph weighs coalition government: sentence [[1]] gives the usual charge, sentence [[2]] ('Less often noticed') adds the moderating effect of bargaining, sentence [[3]] ('this process') draws out its benefit, and sentence [[4]] ('The price') states the cost. Sentence [[X]] is about coalitions, but it explains why small parties join them, which is not part of the assessment of what coalition government does to policy and accountability.",
    "Linking sentence [[X]] to the bargaining in sentence [[2]] because both concern what partners want.",
    "V03H-coalition-governments",
    "The odd sentence shares the subject and the idea of bargaining, and must be rejected because party motives are a different question from the merits of coalition rule.",
    traps=[(4, "Sentence [[4]] turns from benefits to a drawback, but 'The price' marks it as the cost of the bargaining described before, so it completes the assessment.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 019 Difficult, maps and empire
ooo("V03-H-019", "History and politics",
    "Imperial maps helped create the territory they seemed to describe, though published lines could also bind the states that drew them.", "Difficult",
    ["Maps are usually thought of as describing territory, but in the age of empires they often helped to create it.",
     "A boundary drawn across land that its surveyors had barely seen became, once printed, the line along which taxes were collected and soldiers posted.",
     "Areas left blank were read not as places unknown to the mapmaker but as places awaiting an owner, which made them seem open to claim.",
     "Yet the power of maps cut both ways, for a line once published could be cited against the very state that drew it when that state later wished to move it."],
    "Improvements in surveying instruments made maps steadily more accurate, so that later maps of a region often corrected the outlines of earlier ones.",
    "Sentence [[1]] states the thesis that imperial maps created territory, sentences [[2]] and [[3]] give two ways they did so (printed boundaries became administrative fact; blank spaces invited claims), and sentence [[4]] ('Yet the power of maps cut both ways') adds that a published line could also bind its maker. Sentence [[X]] is about maps, but it tells a story of growing accuracy, that is, of maps getting better at describing, which is the view sentence [[1]] sets aside; it contributes nothing to the argument about maps shaping power.",
    "Keeping sentence [[X]] because correcting old outlines seems related to moving a line in sentence [[4]], or dropping sentence [[4]] because it reverses the direction of the argument.",
    "V03H-maps-and-empire",
    "The odd sentence shares the vocabulary of lines and outlines and seems to echo the sentence about moving a published line; it is rejected only by seeing that it treats maps as description, the view the paragraph moves beyond.",
    traps=[(4, "Sentence [[4]] begins 'Yet' and seems to undercut the thesis, but it extends it: the power of maps to fix territory is what lets a line be 'cited against the very state that drew it'."),
           (3, "Sentence [[3]] can look like a separate point about blank spaces, but it is the second way, after sentence [[2]], in which maps created territory.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 020 Medium, referendums
ooo("V03-H-020", "History and politics",
    "Referendums force complex trade-offs into a yes or no and hide the drafter's power, so they suit ratifying detailed proposals.", "Medium",
    ["A referendum appears to be democracy in its purest form, with citizens deciding a question directly instead of through representatives.",
     "But a single vote can only answer yes or no, while most important questions involve trade-offs that a binary choice cannot express.",
     "Whoever drafts the question, moreover, decides which options appear on the ballot and in what words, and so exercises a power that the vote itself conceals.",
     "Referendums therefore work best when they ratify a detailed proposal already negotiated, rather than when they are asked to settle a vague principle."],
    "Turnout in referendums varies widely, and a decision taken on a low turnout may be resented by the many who did not vote.",
    "Sentence [[1]] states the appeal of referendums, sentence [[2]] ('But') raises the problem of the binary choice, sentence [[3]] ('moreover') adds the hidden power of the drafter, and sentence [[4]] ('therefore') concludes that referendums suit ratification of detailed proposals, a remedy for exactly those two problems. Sentence [[X]] raises turnout and legitimacy, a concern the conclusion in sentence [[4]] does nothing to address, so it does not belong to the argument.",
    "Accepting sentence [[X]] as one more objection to referendums without checking whether the conclusion answers it.",
    "V03H-referendums",
    "The odd sentence looks like another objection in a list of objections; it is rejected because the conclusion responds only to the other two.",
    traps=[(3, "Sentence [[3]] changes from the ballot's form to its author, but 'moreover' marks it as a second problem, and a pre-negotiated proposal in sentence [[4]] answers it.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 021 Difficult, minimum wage
ooo("V03-H-021", "Economics and business",
    "Whether a minimum wage costs jobs depends on its level and on employers' power over wages, not on the principle itself.", "Difficult",
    ["The simplest model of the labour market predicts that a minimum wage set above the going rate will price some workers out of jobs.",
     "That prediction assumes that employers must pay whatever wage the market sets, but in a small town with one large employer, that employer can hold wages below what workers' labour is worth.",
     "In such a market, a moderate minimum can raise pay without reducing employment, and may even draw in workers who were unwilling to work at the old wage.",
     "The effect of a minimum wage therefore depends less on the principle than on how high it is set and on how much power employers hold where it applies."],
    "A minimum wage also differs from a cash transfer to low earners in that its cost falls on employers and customers rather than on taxpayers.",
    "Sentence [[1]] gives the simple prediction, sentence [[2]] ('That prediction assumes') exposes its assumption and offers a counter-case, sentence [[3]] ('In such a market') shows a moderate minimum raising pay without job losses, and sentence [[4]] ('therefore') concludes that the effect depends on level and employer power. Sentence [[X]] is about the minimum wage, but it compares who bears its cost with who bears the cost of a transfer, a question of incidence that the argument about employment never takes up.",
    "Keeping sentence [[X]] because 'also' makes it look like one more point in the same discussion, or rejecting sentence [[1]] because the paragraph disputes it.",
    "V03H-minimum-wage",
    "The odd sentence uses the paragraph's vocabulary and an additive 'also'; it must be rejected because incidence is a different question from employment effects.",
    traps=[(1, "Sentence [[1]] is the view the paragraph argues against, but 'That prediction' in sentence [[2]] needs it."),
           (3, "Sentence [[3]] may seem to overstate the case, but 'moderate' is what sentence [[4]] builds on when it says the effect depends on how high the minimum is set.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 022 Medium, store brands
ooo("V03-H-022", "Economics and business",
    "Store brands rivalled makers' brands once retailers' own reputation could do the work a maker's brand had done.", "Medium",
    ["Supermarket store brands were once sold as cheap substitutes for shoppers who could not afford the familiar names.",
     "They became serious rivals only when retailers realised that their own reputation could do the work that a manufacturer's brand had always done.",
     "A shopper who trusts the supermarket's handling of fresh food will extend that trust to a tin of beans carrying the supermarket's name.",
     "The manufacturer's brand, whose job was to vouch for quality to buyers who knew nothing else about the product, thus loses its edge wherever shoppers trust the shop more than any single maker."],
    "Store brands are usually shelved right beside the branded products they imitate, often in packaging of a similar colour and shape.",
    "Sentence [[1]] gives the old role of store brands, sentence [[2]] ('They became serious rivals only when') identifies the change, sentence [[3]] illustrates how trust in the retailer transfers, and sentence [[4]] ('thus') concludes that the maker's brand loses its function. Sentence [[X]] is about store brands, but it concerns shelf placement and imitative packaging, a selling tactic that plays no part in the argument about whose reputation vouches for quality.",
    "Keeping sentence [[X]] because imitation seems to explain why store brands compete with makers' brands.",
    "V03H-store-brands",
    "The odd sentence shares the subject and offers a rival explanation of competition, so it must be rejected on function.",
    traps=[(3, "Sentence [[3]] is a concrete example and may seem trivial, but it shows the transfer of trust on which the conclusion in sentence [[4]] rests.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 023 Medium, microfinance group lending
ooo("V03-H-023", "Economics and business",
    "Joint liability lets lenders reach borrowers without collateral, because members screen and monitor one another.", "Medium",
    ["Banks have long refused small loans to the very poor, because such borrowers have no collateral and are costly to assess one by one.",
     "Group lending answers both difficulties by making a handful of borrowers jointly responsible, so that if one member defaults the others must repay or lose access to future credit.",
     "Since the members choose one another, they bring to that choice a knowledge of each other's habits and reliability that no loan officer could gather cheaply.",
     "The same arrangement turns neighbours into watchful monitors, which is why repayment can stay high even though no borrower has pledged anything the lender could seize."],
    "Microfinance lenders usually charge interest well above ordinary bank rates, and critics ask whether such loans relieve poverty or merely deepen debt.",
    "Sentence [[1]] states the two obstacles, missing collateral and costly assessment, sentence [[2]] ('answers both difficulties') introduces joint liability, sentence [[3]] shows members doing the screening, and sentence [[4]] ('The same arrangement') adds monitoring and explains why repayment holds up without collateral. Sentence [[X]] is about microfinance too, but it raises the price of the loans and their effect on poverty, a question about outcomes for borrowers that the paragraph's account of how joint liability replaces collateral never takes up.",
    "Keeping sentence [[X]] because it mentions lenders, banks and repayment, or because a critical remark seems a natural follow-up, without checking whether any sentence uses it.",
    "V03H-microfinance-group-lending",
    "The odd sentence shares the subject and vocabulary (lenders, bank, loans) and must be rejected because pricing and poverty impact are a different question from the repayment mechanism.",
    traps=[(3, "Sentence [[3]] can look like a side remark about neighbours, but it is how joint liability solves the second difficulty in sentence [[1]], the cost of assessing borrowers, and 'The same arrangement' in sentence [[4]] builds on it.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 024 Medium, menu costs of inflation
ooo("V03-H-024", "Economics and business",
    "Costly price revisions make firms change prices late and in jumps, so the main cost of inflation here is distorted relative prices.", "Medium",
    ["When prices are rising steadily, every firm must from time to time revise what it charges, and each revision has a cost of its own.",
     "Labels must be changed, catalogues reprinted and customers persuaded that the new price is fair, so firms tend to put off revisions and then make them in large steps.",
     "Because different firms revise at different moments, the prices of goods drift out of line with one another, and buyers react to gaps that reflect nothing but the timing of revisions.",
     "The cost of such revisions, then, lies less in the reprinting itself than in the misleading signals that staggered price changes send to buyers."],
    "Firms with well-known brands can raise their prices during inflation with little loss of customers, while firms selling interchangeable goods must hold back.",
    "Sentence [[1]] says each price revision has a cost, sentence [[2]] lists those costs and their effect (revisions delayed and made in large steps), sentence [[3]] ('Because different firms revise at different moments') shows relative prices drifting apart, and sentence [[4]] ('then') concludes that the real cost is the misleading signal. Sentence [[X]] also concerns firms raising prices in inflation, but it is about how much pricing power a firm has, not about the cost and timing of revising prices, and nothing in the chain from revision cost to distorted signals depends on it.",
    "Keeping sentence [[X]] because it seems to explain why firms 'put off revisions' in sentence [[2]], when sentence [[2]] already gives the reason: revisions are costly.",
    "V03H-menu-costs-of-inflation",
    "The odd sentence uses the paragraph's words (firms, prices, raise, inflation) and offers a rival reason for holding back prices, so it must be rejected on function.",
    traps=[(4, "Sentence [[4]] may look like a vague summary, but 'the reprinting itself' recalls sentence [[2]] and 'misleading signals' sums up sentence [[3]]; without it the paragraph makes no point about where the cost lies.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 025 Difficult, planned obsolescence
ooo("V03-H-025", "Economics and business",
    "Short product life is often a trade-off buyers choose; the charge of planned obsolescence holds only where firms block repair.", "Difficult",
    ["The charge of planned obsolescence holds that manufacturers deliberately build goods to fail so that customers must buy again.",
     "Much of what looks like deliberate frailty, however, reflects choices buyers make themselves, since a lighter, cheaper or more up-to-date product usually lasts less long than a heavy one built for decades.",
     "Durability, on this view, is one quality among others, and a market that supplies short-lived goods may simply be supplying what people prefer to pay for.",
     "The charge regains its force only where a firm prevents repair, by sealing in batteries or withholding spare parts, for then a short life is imposed on buyers rather than chosen by them."],
    "Short-lived goods also impose a cost on people who never bought them, since the discarded products must be buried, burned or shipped elsewhere.",
    "The paragraph tests the charge against one question, whether short product life is chosen by buyers or imposed on them: sentence [[1]] states the charge, sentence [[2]] ('however') argues that much short life is chosen, sentence [[3]] ('on this view') generalises that durability is one quality buyers trade off, and sentence [[4]] says the charge 'regains its force only where' repair is blocked. Sentence [[X]] shares the critical tone but argues from harm to third parties, a consideration that would condemn short-lived goods however freely buyers chose them; that clashes with the 'only' in sentence [[4]], which allows the charge force solely where short life is imposed.",
    "Keeping sentence [[X]] because it sounds like a natural rejoinder to the market defence in sentence [[3]], or dropping sentence [[2]] or sentence [[4]] because each seems to reverse the direction of the paragraph.",
    "V03H-planned-obsolescence",
    "The odd sentence shares the subject and seems to answer the market defence of short-lived goods, so a reader must see that its third-party argument contradicts the 'only' in the conclusion.",
    traps=[(2, "Sentence [[2]] seems to abandon the charge stated in sentence [[1]], but it is the paragraph's main move, and 'on this view' in sentence [[3]] refers to it."),
           (4, "Sentence [[4]] turns back towards the charge, but 'regains' presupposes the weakening in sentences [[2]] and [[3]], and it gives the paragraph its conclusion.")],
    cognitive="Analysis", exams=D)
