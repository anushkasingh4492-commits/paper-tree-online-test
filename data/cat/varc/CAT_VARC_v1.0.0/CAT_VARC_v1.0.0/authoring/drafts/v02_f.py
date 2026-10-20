import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DT = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ps("V02-F-001", "Psychology", "Large assortments deter choice only under certain conditions, not because of their size alone.", "Medium",
   "A widely discussed finding holds that people offered many options are less likely to choose anything at all, and less satisfied when they do. Shoppers faced with two dozen varieties of a product, the story goes, walk away more often than those shown a handful. The finding has been influential, shaping everything from product ranges to pension menus. Yet attempts to reproduce it have produced a scattered picture: in some settings large assortments discourage choice, in others they make no difference, and in some they attract more buyers. What seems to matter is not the number of options alone but the conditions around it: whether people already know what they want, whether the options are easy to compare, and whether they are sorted in a way that makes the differences visible. Abundance becomes a burden mainly when it arrives without structure.",
   "Many options discourage choosing mainly when preferences are unclear and the options are hard to compare or poorly organised, not simply because there are many.",
   [("Repeated tests have shown that the well-known result about too many options was simply mistaken, since larger assortments in fact attract more buyers than small ones.",
     "The paragraph says large assortments attract more buyers only 'in some' settings and discourage choice in others, so it does not declare the original result simply mistaken."),
    ("The finding that large assortments deter shoppers has strongly influenced how businesses and pension providers decide how many products and plans they should offer to their customers.",
     "The paragraph mentions this influence only in passing; the option leaves out its central point that the effect depends on the conditions around the options."),
    ("Businesses and policymakers should reduce the number of options they offer, since people are generally less satisfied whenever they must choose among a great many alternatives.",
     "The paragraph makes no recommendation, and its point is that size alone does not decide the matter, which this generalisation about 'many alternatives' ignores.")],
   "The paragraph reports the original finding, notes that later attempts give 'a scattered picture', and concludes that what matters is 'not the number of options alone but the conditions around it': known preferences, ease of comparison and sorting. The correct answer keeps both the qualification and the conditions.",
   "Taking the mixed replication results as a refutation, or keeping the original finding without its qualification.",
   "V02F-choice-overload", "The correct answer must be separated from an overstatement of the replication results and from a prescription built on the original finding.")

# ------------------------------------------------------------------ 002
ps("V02-F-002", "Psychology", "Unrecoverable past costs wrongly steer present choices because abandoning them feels like admitting waste.", "Easy",
   "Someone who has paid for a concert ticket and wakes up feeling unwell will often drag themselves to the hall anyway, reasoning that otherwise the money is wasted. But the money is gone whichever choice they make; the only question still open is whether the evening will be better spent at the concert or in bed. Letting past costs that cannot be recovered steer present decisions is what economists call the sunk cost fallacy. It persists partly because abandoning an investment feels like admitting a mistake, and people dislike the sense of waste more than they value the better outcome. The same pull keeps failing projects funded long after their prospects have faded, because each new payment is justified by the ones before it.",
   "People often let money they cannot recover drive present choices, though only future consequences should count, because walking away feels like admitting waste and error.",
   [("A person who feels unwell on the day of a concert should stay at home, since going to the hall will not bring back the money already spent on the ticket.",
     "This keeps only the opening illustration and turns it into advice; the paragraph's point is the general error and why it persists, including in funded projects."),
    ("Failing projects keep receiving money because the people who run them are poor at forecasting and overestimate how quickly their ventures will succeed.",
     "The paragraph explains continued funding by the fact that 'each new payment is justified by the ones before it', not by poor forecasting, which it never mentions."),
    ("People value saving money more than they value enjoying themselves, which is why they attend events they no longer wish to attend after paying for them.",
     "The paragraph says people dislike 'the sense of waste' more than they value 'the better outcome'; it makes no claim about saving money versus enjoyment.")],
   "The paragraph defines the sunk cost fallacy as letting 'past costs that cannot be recovered steer present decisions', notes that the money is gone 'whichever choice they make', and explains that the error persists because abandoning an investment 'feels like admitting a mistake'. The correct answer states the error and its cause.",
   "Choosing the option that repeats the concert example as advice instead of the general point.",
   "V02F-sunk-cost-fallacy", "The point and its cause are stated directly; wrong options are a single example, an invented cause and a distortion.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 003
ps("V02-F-003", "Psychology", "A witness's confidence signals accuracy only when recorded at a fair first identification, before later inflation.", "Difficult",
   "For decades the lesson drawn from wrongful convictions was that a witness's confidence tells us little about whether the witness is right: jurors are swayed by a certain voice, and certainty is no guarantee of accuracy. That lesson is now being refined rather than overturned. When an identification is made for the first time, from a fairly conducted line-up, and the witness's confidence is recorded on the spot, high confidence turns out to be a reasonably good sign of accuracy, and hesitant identifications deserve real doubt. The trouble lies in what happens afterwards. Confidence grows with feedback, rehearsal and the passage of months, so that the certainty displayed in a courtroom may bear little relation to the uncertainty felt at the original moment. Confidence, then, is informative evidence, but only if it is captured before the process of investigation has had a chance to manufacture it.",
   "A witness's certainty can indicate accuracy when it is recorded at a fair first identification, but it loses that value once later feedback and repetition have inflated it.",
   [("Because certainty is no guarantee of accuracy, courts should give no weight at all to how confident a witness is and should judge identifications on other evidence alone.",
     "This is the older lesson the paragraph says is being 'refined rather than overturned'; it denies the informative value that confidence has at a fair first identification."),
    ("Confidence is a reliable sign of accuracy whenever it is genuine, so the main danger in court comes from witnesses who deliberately exaggerate their certainty to impress jurors.",
     "The paragraph blames inflation by 'feedback, rehearsal and the passage of months', not deliberate exaggeration, and genuine but later confidence is exactly what it distrusts."),
    ("Witnesses tend to grow more certain of their identifications over time, as they receive feedback, rehearse their accounts and wait many months before giving evidence.",
     "This states only the inflation half of the argument and omits the central refinement that confidence recorded 'on the spot' is 'a reasonably good sign of accuracy'.")],
   "The paragraph refines an older lesson: initial confidence, from a fair line-up and 'recorded on the spot', is 'a reasonably good sign of accuracy', but confidence later 'grows with feedback, rehearsal and the passage of months'. Hence confidence is informative 'only if it is captured before' investigation can 'manufacture it'. The correct answer holds both halves.",
   "Picking the older lesson the paragraph refines, or the half that describes only how confidence inflates.",
   "V02F-eyewitness-confidence", "Two wrong options each state one true half of the argument; only the correct answer combines the finding with its time-bound qualification.",
   exams=DT)

# ------------------------------------------------------------------ 004
ps("V02-F-004", "Psychology", "Ordinary boredom is a useful signal, and the problem is how quickly it is now silenced.", "Medium",
   "Boredom is usually treated as a defect to be engineered away, whether by entertainment, by phones, or by the advice that interesting people are never bored. This view mistakes a signal for a malfunction. Boredom is unpleasant in the way hunger is unpleasant: it reports that the current activity is failing to engage us and pushes us to look for something that will. Seen this way, the problem is not boredom itself but the speed with which we now silence it. A feeling that once prompted people to change course, take up a project or simply let their minds wander is cut short within seconds by a screen, so its message is never heard. None of this makes boredom pleasant, and chronic boredom in a setting with no exits is genuinely harmful. The point is only that the brief, ordinary kind has a job to do.",
   "Brief boredom usefully prompts a search for something more engaging, so the trouble is our habit of silencing it at once, although persistent boredom with no escape does harm.",
   [("Boredom is a valuable experience in all its forms, so people should deliberately seek it out and avoid the entertainment that relieves the discomfort it brings.",
     "The paragraph concedes that 'chronic boredom in a setting with no exits is genuinely harmful', so 'all its forms' contradicts it, and it never advises seeking boredom out."),
    ("Phones and other screens have made people more bored than ever before, because constant entertainment weakens their capacity to engage with ordinary tasks.",
     "The paragraph says screens cut boredom short 'within seconds', silencing it; it does not claim they increase boredom or weaken engagement."),
    ("Boredom resembles hunger in being an unpleasant feeling that tells us something about our present state and pushes us to act on what it reports.",
     "This is only the analogy; it leaves out the paragraph's critique that the real problem is 'the speed with which we now silence it'.")],
   "The paragraph rejects the view of boredom as 'a defect' because it 'mistakes a signal for a malfunction', locates the problem in 'the speed with which we now silence it', and limits the claim with a concession about chronic boredom. The correct answer keeps the signal, the critique and the concession.",
   "Choosing the analogy with hunger, which is accurate but only a step in the argument.",
   "V02F-boredom-as-signal", "One wrong option overstates by ignoring the concession and another is a correct but partial step.")

# ------------------------------------------------------------------ 005
ps("V02-F-005", "Society and culture", "Queues need little enforcement because their order is visible, which also explains the anger at queue-jumpers.", "Easy",
   "A queue is one of the simplest institutions people have invented, and it works with almost no enforcement. Nobody has to be appointed to run it; the rule of first come, first served is understood at a glance, and anyone who breaks it is visible to everyone behind. That visibility is the queue's real strength. Because the order is public, a person who pushes in is not merely taking one place but openly claiming that their time matters more than everyone else's, which is why queue-jumping provokes anger out of all proportion to the minutes lost. Where the order cannot be seen, as in a crowd gathered loosely around a counter, the same people who would wait patiently in a line will jostle, because no one can tell who was there first.",
   "A queue keeps itself in order because everyone can see the sequence, which turns cheating into a public insult and explains why disorder follows where no sequence is visible.",
   [("People become angry at those who push into queues mainly because of the time they lose, which is why longer queues provoke the strongest reactions from those waiting.",
     "The paragraph says the anger is 'out of all proportion to the minutes lost' and comes from the open claim that one's time matters more, so this reverses it."),
    ("In crowds gathered loosely around a counter, people tend to push and jostle because none of them can tell who arrived first and who ought to be served next.",
     "This is only the contrasting case at the end; it leaves out the central point that visibility of the order is what makes queues work."),
    ("Queues work well only in cultures that value patience, and they break down in societies where people are not taught from childhood to respect a fair order.",
     "The paragraph explains the difference by whether the order 'can be seen', noting that 'the same people' behave differently; culture and upbringing are never mentioned.")],
   "The paragraph says a queue works 'with almost no enforcement' and that 'visibility is the queue's real strength': it makes queue-jumping an open claim of superiority, and where order 'cannot be seen' the same people jostle. The correct answer captures visibility as the cause of both effects.",
   "Picking the crowd example, which is true but only the contrasting illustration.",
   "V02F-queue-fairness-norms", "The central claim is stated in one sentence and the wrong options are a reversal, a detail and an outside cause.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 006
ps("V02-F-006", "Society and culture", "Gifts bind people through obligations that only further gifts can answer, so an unreturnable gift can humiliate.", "Difficult",
   "We like to think of a gift as the opposite of a transaction: something given freely, with no expectation of return. Yet anyone who has received a lavish present from a casual acquaintance knows the discomfort it brings, and the discomfort is telling. A gift creates a debt that cannot be settled in money without insult, for paying cash back would turn the gift into a sale and refuse the relationship it offered. It can be answered only by another gift, suitably timed and suitably sized, and so giving binds people into a continuing exchange. This does not make generosity a disguised form of bargaining, since the point of the exchange is the bond, not the goods. But it does mean that a gift which can never be returned, whether because it is too large or because the giver refuses anything in return, can humiliate rather than honour the person who receives it.",
   "Gifts create debts that only further gifts can repay, so they sustain bonds rather than hidden bargains, and a gift that can never be returned may shame the one receiving it.",
   [("Since every gift creates a debt that the receiver must repay, generosity is at bottom a polite form of bargaining in which each side expects goods of roughly equal value.",
     "The paragraph explicitly denies this: 'This does not make generosity a disguised form of bargaining, since the point of the exchange is the bond, not the goods.'"),
    ("Repaying a present with money is insulting because it turns the gift into a purchase and so rejects the relationship that the giver was hoping to begin.",
     "This is one step in the argument; it omits the continuing exchange of gifts and the conclusion that an unreturnable gift can humiliate its recipient."),
    ("Because generous gifts can humiliate those who receive them, people should give only small presents that can easily be returned with something of a similar size.",
     "The paragraph makes no recommendation, and it says gifts humiliate only when they 'can never be returned', not that generous gifts in general do so.")],
   "The paragraph argues that a gift 'creates a debt' answerable 'only by another gift', which binds people 'into a continuing exchange'. It then qualifies: this is not bargaining, because 'the point of the exchange is the bond'. Finally, a gift 'which can never be returned' can 'humiliate rather than honour'. The correct answer holds all three moves.",
   "Treating the obligation to reciprocate as proof that gifts are bargains, which the paragraph explicitly rules out.",
   "V02F-gift-obligation-reciprocity", "The tempting wrong option follows the first half of the argument but contradicts the qualification; the correct answer must also keep the final twist.",
   exams=DT)

# ------------------------------------------------------------------ 007
ps("V02-F-007", "Society and culture", "A tip means different things depending on whether wages assume it.", "Medium",
   "Tipping looks the same everywhere, a small sum left for good service, but it does quite different work in different places. Where wages for service staff are set on the assumption that tips will make up the difference, a tip is not a bonus at all; withholding it cuts the worker's basic pay, and the customer who tips carefully according to service is in effect setting a stranger's wage. Where staff are paid a full wage, the tip really is a discretionary reward, and leaving little or nothing is an ordinary judgement rather than a harm. Visitors who carry their home habits abroad therefore often get it wrong in both directions: they may seem mean in one country and needlessly lavish in another, since the same gesture carries a different meaning depending on how pay is organised.",
   "What a tip means depends on how staff are paid: where wages assume tips it is part of basic pay, but where full wages are paid it is a genuinely optional reward.",
   [("Customers should always tip generously wherever they travel, since a tip may form part of a worker's basic pay and withholding it can cause real harm to that worker.",
     "The paragraph says that where full wages are paid, 'leaving little or nothing is an ordinary judgement rather than a harm', so 'always' contradicts it."),
    ("Tipping customs differ from country to country mainly because some cultures value generosity towards strangers more highly than others, which confuses visiting travellers.",
     "The paragraph explains the difference by 'how pay is organised', not by cultural attitudes to generosity, which it never mentions."),
    ("In places where service wages are set on the assumption that tips will be paid, customers who tip according to the service they receive are effectively setting a wage.",
     "This describes only one of the two systems the paragraph compares; it leaves out the contrast with full-wage settings on which the point depends.")],
   "The paragraph compares two arrangements: where wages assume tips, withholding one 'cuts the worker's basic pay'; where staff get a full wage, the tip 'really is a discretionary reward'. It concludes that the same gesture means different things 'depending on how pay is organised'. The correct answer states the comparison and its basis.",
   "Choosing the option that describes only the tip-dependent case, which is accurate but half the comparison.",
   "V02F-tipping-custom", "One wrong option is a correct half of the comparison and another offers a plausible but unstated cause.")

# ------------------------------------------------------------------ 008
ps("V02-F-008", "History and politics", "The repatriation debate is as much about who controls an object as about where it sits.", "Difficult",
   "Arguments over whether museums should return objects taken during colonial rule are often framed as a contest between two principles. One side holds that objects belong to the communities that made them, and that their removal under unequal power was a wrong that persists as long as they stay away. The other holds that great collections let visitors encounter many cultures under one roof, and that this universal access is itself a public good. Both sides tend to assume the question is about where an object should physically sit. But much of what is at stake is who decides: who chooses how an object is displayed and described, who may study it, and whether its makers' descendants are consulted or merely informed. A museum could return an object and still treat its original owners as an audience rather than as partners, or keep one and share real authority over it. Location matters, but it is not the whole of the question.",
   "Debates over returning colonial-era objects focus too narrowly on location, when who controls their display, study and interpretation is also central to what is in dispute.",
   [("Objects taken under colonial rule should be returned to the communities that made them, since their removal under unequal power remains a continuing wrong until they come back.",
     "This is the position of 'one side' that the paragraph reports; the author takes neither side and argues that both rest on too narrow an assumption."),
    ("Since location is not what really matters, museums may keep disputed objects as long as they consult the descendants of the makers about how those objects are displayed.",
     "The paragraph says 'Location matters, but it is not the whole of the question', so it does not dismiss location, and it gives no licence to keep objects."),
    ("The claims of source communities and the public value of universal collections are equally strong, so disputes over objects from colonial rule can never be fully settled.",
     "The paragraph does not weigh the two principles against each other or call the dispute unresolvable; it reframes what the dispute is about.")],
   "After setting out both sides, the paragraph says they 'tend to assume the question is about where an object should physically sit', but 'much of what is at stake is who decides': display, study and consultation. Its last line keeps location relevant: 'Location matters, but it is not the whole of the question.' The correct answer keeps the reframing and its limit.",
   "Choosing a reported position as the author's, or turning 'not the whole of the question' into 'does not matter'.",
   "V02F-museum-repatriation-artefacts", "Two wrong options use the paragraph's own content: a reported view and a distortion of the final qualification.",
   exams=DT)

# ------------------------------------------------------------------ 009
ps("V02-F-009", "History and politics", "Term limits may move power to unelected insiders rather than to citizens.", "Medium",
   "Term limits for legislators are usually defended as a cure for entrenched power: if no one can hold a seat for decades, the argument goes, politics will be refreshed by newcomers who are closer to ordinary citizens. The newcomers do arrive, but the power does not necessarily disappear; it moves. Lawmakers who must leave after a few years have little time to master budgets, procedure or the details of policy, and they come to rely on those who stay: permanent staff, party organisations and lobbyists who have spent years in the building. A legislature of perpetual beginners can thus be more dependent on unelected insiders than one in which some members have served long enough to challenge them. This is not a decisive case against term limits, which may still be worth their costs, but it undercuts the claim that they simply return power to the people.",
   "Term limits can shift influence from experienced legislators to staff, parties and lobbyists instead of citizens, which weakens though does not settle the case for them.",
   [("Term limits ought to be abolished, since they hand power to unelected insiders and leave legislatures full of members who never learn how to do their work properly.",
     "The paragraph says 'This is not a decisive case against term limits, which may still be worth their costs', so a call for abolition overstates it."),
    ("By preventing anyone from holding a seat for decades, term limits refresh politics with newcomers who are closer to ordinary citizens than career lawmakers are.",
     "This is the usual defence that the paragraph reports and then undercuts; it ignores the claim that power 'does not necessarily disappear; it moves'."),
    ("Long-serving legislators are more honest than newcomers, because their years in office protect them from the influence of lobbyists and other powerful insiders.",
     "The paragraph says experienced members can 'challenge' insiders because they know the work; it says nothing about honesty or immunity from influence.")],
   "The paragraph accepts that newcomers arrive but argues that power 'moves' to 'permanent staff, party organisations and lobbyists' because short-serving members lack expertise. It limits the conclusion: not 'a decisive case', but it 'undercuts the claim that they simply return power to the people'. The correct answer holds the mechanism and the limit.",
   "Turning a qualified objection into a call for abolition.",
   "V02F-legislative-term-limits", "The extreme wrong option is close to the paragraph's argument and must be rejected on degree.")

# ------------------------------------------------------------------ 010
ps("V02-F-010", "History and politics", "Census categories help create the groups they record, so they should be scrutinised as policy choices.", "Difficult",
   "A census appears to be a passive instrument: the state asks who people are and writes down the answers. But the questions come first, and they are not neutral. To count people by language, religion or ethnicity, an official form must offer a fixed list of boxes, and those boxes rarely match the blurred, overlapping and shifting ways people actually describe themselves. Once printed and tallied, however, the categories acquire a weight of their own. Resources, representation and political claims come to be organised around them, and people begin to identify with the box that brings recognition. Counting, in short, can help to create the groups it claims merely to record. This does not mean censuses should stop asking such questions, since a state that refuses to count a disadvantaged group may also refuse to see its disadvantage; it means the categories deserve the scrutiny we give to any other policy choice.",
   "Because claims and resources come to be organised around its categories, a census helps form the identities it claims only to record, so those categories need scrutiny, not abandonment.",
   [("Because official categories distort the fluid ways in which people see themselves, governments should stop asking about language, religion and ethnicity in the census.",
     "The paragraph rejects this: 'This does not mean censuses should stop asking such questions', since not counting a disadvantaged group may hide its disadvantage."),
    ("Census forms offer fixed lists of boxes that seldom match the overlapping and changing ways in which people actually describe their own identities and origins.",
     "This is only the first step; it omits the central claim that the categories then shape identity, and the conclusion about scrutiny."),
    ("Groups that are counted in a census gain political power while those left out lose resources, so states design census categories in order to reward their supporters.",
     "The paragraph attributes no motive to states; it describes an unintended effect of counting, so the claim about rewarding supporters is outside its scope.")],
   "The paragraph argues that the boxes come first and 'acquire a weight of their own' as resources and claims are organised around them, so counting 'can help to create the groups it claims merely to record'. It then qualifies: censuses should not stop asking, but the categories 'deserve the scrutiny we give to any other policy choice'. The correct answer keeps the feedback loop and the qualified conclusion.",
   "Taking the critique of categories as a case for dropping them, which the last sentence rules out.",
   "V02F-census-categories-identity", "The correct answer turns on a feedback argument and a qualification that one wrong option reverses and another omits.",
   exams=DT)

# ------------------------------------------------------------------ 011
ps("V02-F-011", "Society and culture", "Printing standardised written languages through market pressure, often around where presses clustered.", "Medium",
   "Before printing, a language written across a wide region existed in many local forms: scribes spelled as they spoke, and a manuscript copied in one town might look foreign in another. Printing changed the economics of this variety. A printer selling thousands of copies wanted a form of the language that readers across the whole market could follow, and once a few presses settled on particular spellings and grammar, every later book that followed them reinforced the choice. Standard written languages owe at least as much to this commercial pressure as to the decrees of scholars or rulers. The standard that emerged was not necessarily the most elegant or the most widely spoken variety; it was often simply the one used where the presses happened to cluster, and the dialects of other regions came to look like departures from a norm that was partly an accident of trade.",
   "Printers' need for a form readable across large markets pushed written languages towards a standard that often reflected where presses clustered rather than any special merit of that variety.",
   [("Standard written languages were mainly created by scholars and rulers, who chose the most elegant regional varieties and then required printers to adopt them everywhere.",
     "The paragraph credits 'commercial pressure' at least as much as 'decrees of scholars or rulers' and says the standard was 'not necessarily the most elegant', so this reverses it."),
    ("Before printing, scribes spelled words as they pronounced them, so that a manuscript produced in one town could look foreign to readers living in another.",
     "This restates only the opening background; it says nothing about how printing produced a standard or why that standard was partly accidental."),
    ("Printing wiped out the regional dialects of written languages, because readers refused to buy books written in any variety other than the most widely spoken one.",
     "The paragraph says other dialects 'came to look like departures' from the norm, not that they vanished, and it denies that the standard was 'the most widely spoken variety'.")],
   "The paragraph explains that printers wanted a form 'readers across the whole market could follow' and that early choices were reinforced by later books. It adds that the standard was 'often simply the one used where the presses happened to cluster', 'partly an accident of trade'. The correct answer gives the mechanism and the qualification about merit.",
   "Picking the background detail about scribes, or assuming the standard must have been the best or most common variety.",
   "V02F-vernacular-printing-standardisation", "The correct answer combines a causal mechanism with a qualification that two wrong options contradict in different ways.")

# ------------------------------------------------------------------ 012
ps("V02-F-012", "History and politics", "A referendum's outcome is shaped by design choices made by others before anyone votes.", "Easy",
   "A referendum is often praised as the purest form of democracy, since the people decide directly rather than through representatives. But a referendum can only ask a question, and someone has to write it. The wording, the choice between two options or several, the timing of the vote and the threshold needed to win all shape the outcome before a single ballot is cast. A question that offers a single proposal against the status quo, for instance, may force voters who want a third course to choose between two options they both dislike. None of this makes referendums illegitimate, but it does mean that the direct voice of the people is always heard through a design chosen by somebody else.",
   "Though referendums let people decide directly, choices about wording, options, timing and thresholds made by others shape the result, so the popular voice always passes through someone's design.",
   [("Referendums are an illegitimate way to decide public questions, since those who write the questions can always secure whichever outcome they happen to prefer in advance.",
     "The paragraph says 'None of this makes referendums illegitimate', and it claims only that design shapes outcomes, not that designers can always secure them."),
    ("A referendum that sets a single proposal against the status quo may force voters who prefer a third course to choose between two options that they both dislike.",
     "This is the paragraph's single example; it omits the general point that every design choice shapes the result."),
    ("Representative democracy is superior to direct democracy, because elected officials can weigh competing options more carefully than voters can in a single ballot.",
     "The paragraph does not compare the two forms of democracy or praise representatives; this judgement is brought in from outside it.")],
   "The paragraph grants that in a referendum 'the people decide directly', but says that wording, options, timing and threshold 'all shape the outcome before a single ballot is cast'. It ends by denying illegitimacy while insisting that the people's voice 'is always heard through a design chosen by somebody else'. The correct answer keeps the point and the concession.",
   "Overstating the argument into a rejection of referendums.",
   "V02F-referendum-question-design", "The point is stated in the last sentence and the wrong options are an extreme, an example and an outside comparison.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 013
ps("V02-F-013", "Economics and business", "A displayed earlier price makes a price feel like a saving, even when shoppers know the device.", "Easy",
   "A jacket labelled as reduced from eight thousand rupees to four thousand seems a bargain in a way that the same jacket simply priced at four thousand does not. The higher figure works as an anchor: it sets the frame within which the shopper judges the price, so that four thousand feels like a saving rather than a cost. The effect does not depend on the original price being genuine, and some sellers inflate it precisely so that the discount looks larger. Shoppers know, in a general way, that sales are a marketing device, but knowing this does little to blunt the impression in the moment, because the comparison is made almost before any deliberate judgement begins. The anchor persuades by contrast, not by information.",
   "A higher earlier price shown beside the current one, even an inflated one, makes the current price feel like a saving, and knowing the trick hardly weakens the effect.",
   [("Shoppers who understand that sales are a marketing device are not affected by inflated original prices, and they judge discounted goods only by their actual value.",
     "The paragraph says such knowledge 'does little to blunt the impression in the moment', so this reverses its claim."),
    ("Some sellers deliberately raise the original price printed on a label so that the discount on their goods will appear larger to the shoppers who see it.",
     "This is one detail; the paragraph's point is how the anchor shapes judgement and why awareness does not protect against it."),
    ("Clothing is more often sold at a discount than other goods, because shoppers judge the value of clothes mainly by comparing them with the prices they paid before.",
     "The jacket is only an illustration; the paragraph compares nothing across kinds of goods and never refers to prices shoppers paid before.")],
   "The paragraph explains that the higher figure 'works as an anchor' so that the price 'feels like a saving', that this 'does not depend on the original price being genuine', and that awareness 'does little to blunt the impression'. The correct answer states the effect and both qualifications.",
   "Assuming that knowing about a sales trick protects a shopper from it.",
   "V02F-price-anchoring-discounts", "The point is stated directly; wrong options are a reversal, a single detail and an outside generalisation.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 014
ps("V02-F-014", "Economics and business", "Whether paying a brand premium for medicine is sensible depends on how reliable regulation is.", "Medium",
   "Many patients pay several times more for a branded medicine than for a generic version containing the same active ingredient, and this is often dismissed as simple irrationality. The dismissal is too quick. A buyer who cannot test a drug's quality personally has to rely on signals, and a familiar brand is a signal that a large firm has a reputation to lose if its product fails. Where regulation of manufacturing is strong and well enforced, that signal adds little, and the premium is mostly wasted money. Where inspection is patchy and substandard products do circulate, paying for a brand can be a reasonable way of buying assurance that the patient has no other means of obtaining. Whether the premium is foolish depends less on the buyer's psychology than on the reliability of the system that stands behind the cheaper pill.",
   "Paying extra for a branded medicine buys assurance of quality, which is largely wasted where regulation is strong but can be sensible where oversight of manufacturing is weak.",
   [("Patients should always buy branded medicines, because generic versions frequently fail to contain the same active ingredient and so cannot be relied upon to work properly.",
     "The paragraph says that under strong regulation the premium 'is mostly wasted money', and it states that generics contain 'the same active ingredient'."),
    ("Patients who pay several times more for branded medicines than for generic ones are behaving irrationally, since the active ingredient in both kinds of pill is identical.",
     "This is the view the paragraph calls 'too quick'; it argues the premium can be 'a reasonable way of buying assurance' where inspection is patchy."),
    ("Large drug firms charge high prices for their brands because patients trust familiar names, and governments ought to control these prices more strictly than they do at present.",
     "The paragraph proposes no price controls; its concern is when a brand premium is a rational purchase, which this option does not address.")],
   "The paragraph rejects the charge of 'simple irrationality': a brand signals that a firm 'has a reputation to lose'. That signal 'adds little' under strong regulation but is worth buying where 'inspection is patchy'. It concludes that the answer depends 'on the reliability of the system'. The correct answer captures this conditional judgement.",
   "Picking the view the paragraph criticises because it contains a true premise about identical ingredients.",
   "V02F-generic-drug-brand-premium", "The correct answer is conditional, and the criticised view is stated with a true premise that makes it tempting.")

# ------------------------------------------------------------------ 015
ps("V02-F-015", "Economics and business", "Four-day week trials show hidden slack in some jobs, not that every kind of work can adopt the change freely.", "Medium",
   "Firms that have experimented with a four-day working week at unchanged pay frequently report that output holds steady while staff are happier and less likely to leave. These results are encouraging, but they come with a caution that is easy to overlook. The firms that volunteer for such trials tend to be ones whose managers already expect them to succeed, and whose work, often office-based and flexible, can be compressed by cutting meetings and idle time. A hospital ward, a bus route or a factory line that runs continuously cannot squeeze five days of cover into four by working more efficiently; it needs more people. The trials show that many jobs contain more slack than was supposed, not that the shorter week can be adopted everywhere at no cost.",
   "Shorter-week trials reveal slack in many jobs, but because the volunteering firms suit the change unusually well, the trials do not show that it could work everywhere at no cost.",
   [("Since output holds steady when the working week is shortened, all employers could move to four working days at full pay without any loss of productivity or extra cost.",
     "The paragraph says the trials do not show 'that the shorter week can be adopted everywhere at no cost', so this is the overgeneralisation it warns against."),
    ("The apparent success of four-day week trials is an illusion created by enthusiastic managers, and the shorter week does not really make staff any more satisfied.",
     "The paragraph calls the results 'encouraging' and accepts that they show real slack; it raises a caution about selection, not a charge that the results are illusory."),
    ("Hospitals, bus services and factories that run continuously would need to employ more staff if they reduced the working week from five days to four.",
     "This is the supporting example; it leaves out both the encouraging finding and the point about which firms volunteer for trials.")],
   "The paragraph accepts the encouraging finding, then adds 'a caution': volunteering firms expect success and do compressible work, whereas a continuously running service 'needs more people'. It concludes that the trials show slack 'not that the shorter week can be adopted everywhere at no cost'. The correct answer states the finding with its limit.",
   "Treating a caution about who volunteers as proof that the trials failed.",
   "V02F-four-day-work-week", "The correct answer must balance a finding and its limit against one wrong option that drops the limit and one that drops the finding.")

# ------------------------------------------------------------------ 016
ps("V02-F-016", "Economics and business", "Small loans help poor households manage poverty rather than escape it.", "Difficult",
   "Small loans to poor households were once promoted as a route out of poverty: give a woman credit to buy a sewing machine or a few goats, and her business would grow and her family would prosper. Careful evaluations have since tempered that hope. On average, access to such loans does not seem to transform incomes, and most borrowers do not build businesses that grow much at all. Yet the loans are far from useless. They help households smooth out shocks, pay for a medical emergency without selling their livestock, or buy a large item without saving for years, and a minority of borrowers who already run promising enterprises do expand them. Microcredit, it turns out, is less a ladder out of poverty than a tool for managing it, which is valuable, but valuable in a different way from the one originally advertised.",
   "Small loans rarely lift typical borrowers out of poverty, yet they help households absorb shocks and large expenses and let a few existing businesses grow.",
   [("Careful evaluations have shown that small loans to poor households are a failure, since most borrowers never build businesses and their incomes do not rise.",
     "The paragraph says 'the loans are far from useless' and calls them 'valuable', so 'a failure' contradicts it."),
    ("Small loans transform the incomes of borrowers who spend them on productive assets such as sewing machines or goats, rather than on meeting emergencies.",
     "The sewing machine and goats belong to the original promise that evaluations 'tempered'; the paragraph credits the loans mainly with helping households manage shocks and large expenses."),
    ("The main value of small loans lies in allowing poor households to pay for a medical emergency without being forced to sell the livestock on which they depend.",
     "This is one of several benefits listed; it omits the central contrast between the advertised ladder out of poverty and the actual role of managing it.")],
   "The paragraph reports that evaluations 'tempered' the hope that loans transform incomes, then insists that 'the loans are far from useless': they smooth shocks, cover emergencies and large purchases, and help 'a minority' of promising enterprises. Hence microcredit is 'less a ladder out of poverty than a tool for managing it'. The correct answer holds both the deflation and the residual value.",
   "Reading the disappointing average result as total failure, or keeping one benefit and losing the contrast.",
   "V02F-microfinance-limits", "The correct answer must hold a negative finding and a positive qualification, against wrong options that keep only one side or a single benefit.",
   exams=DT)

# ------------------------------------------------------------------ 017
ps("V02-F-017", "Economics and business", "Communities with rules and enforcement can manage shared resources, so the choice is not only market or state.", "Medium",
   "A familiar argument holds that any resource open to all, such as a pasture, a fishery or a forest, will be overused until it is ruined, because each user gains the full benefit of taking more while the cost is shared by everyone. The only remedies, on this view, are private ownership or control by the state. The argument is sound for resources that truly are open to anyone, but many traditional commons were nothing of the kind. Villages that shared grazing land or irrigation water often had detailed rules about who could use the resource, how much and when, together with ways of watching for cheaters and punishing them. Such arrangements have kept some resources in good condition for centuries. They do not always work, and they tend to fail when outsiders arrive or when the community loses its authority, but they show that the choice is not limited to the market or the state.",
   "Shared resources need not end in ruin or be handed to markets or states, since rule-bound communities have managed some well, though such arrangements can break down.",
   [("Because each user gains fully from taking more while the cost is shared, resources open to all will be overused unless they are privatised or placed under state control.",
     "This is the 'familiar argument' the paragraph reports; the author accepts it only for resources that 'truly are open to anyone' and says many commons were not."),
    ("Local communities always manage shared resources better than markets or governments do, so pastures, fisheries and forests should be returned to village control.",
     "The paragraph says community arrangements 'do not always work' and recommends no transfer; it claims only that the options are not limited to market or state."),
    ("Villages that shared grazing land or water often set detailed rules about its use and had ways of detecting and punishing the people who broke those rules.",
     "This is the supporting evidence; it omits the conclusion that the choice is not only between the market and the state.")],
   "The paragraph limits the familiar argument to resources that 'truly are open to anyone' and says many commons 'were nothing of the kind', having rules and enforcement. It concedes they 'do not always work' but concludes 'the choice is not limited to the market or the state'. The correct answer keeps the challenge and the concession.",
   "Taking the reported argument as the author's view, or turning the counter-example into a claim of general superiority.",
   "V02F-commons-community-management", "The reported view is stated persuasively and the overstated option is close to the author's position.")

# ------------------------------------------------------------------ 018
ps("V02-F-018", "Science and environment", "Mangroves can give coasts a self-renewing defence that walls cannot, where they can grow.", "Easy",
   "Coastal towns threatened by storms have long relied on sea walls, which are visible, easy to understand and quick to build. A belt of mangrove forest offers protection of a different kind. Rather than stopping waves at a single line, the tangled roots and trunks absorb their energy gradually across a wide zone, and the forest traps sediment, so that it can build up the shore over time instead of being undermined by it. A wall, by contrast, needs constant maintenance and can be overtopped by a storm larger than it was designed for. Mangroves are no complete answer: they need space, take years to establish and cannot protect everywhere. But where they can grow, they often provide a defence that repairs and strengthens itself, which no wall can do.",
   "Where they can grow, mangroves offer a self-renewing defence that absorbs wave energy, unlike sea walls, though they are slow to establish and not suitable everywhere.",
   [("Coastal towns should pull down their sea walls and plant mangrove forests instead, since walls are always overtopped by large storms and need costly upkeep.",
     "The paragraph says mangroves 'are no complete answer' and 'cannot protect everywhere', and it says walls can be overtopped by larger storms, not always."),
    ("The tangled roots and trunks of mangrove trees absorb the energy of waves across a wide zone and trap sediment that gradually builds up the shoreline over time.",
     "This describes how mangroves work but leaves out the comparison with walls and the limits the paragraph places on mangroves."),
    ("Sea walls remain the best defence against storms because they are quick to build and easy to understand, while mangroves take many years to grow.",
     "The paragraph's conclusion favours mangroves where they can grow, since they give 'a defence that repairs and strengthens itself, which no wall can do'.")],
   "The paragraph compares two defences: walls stop waves 'at a single line' and need 'constant maintenance', whereas mangroves absorb energy 'across a wide zone' and build up the shore. It concedes mangroves 'are no complete answer' but concludes that where they grow they defend in a way 'no wall can do'. The correct answer holds the comparison and the concession.",
   "Choosing the description of how mangroves work, which misses the comparison.",
   "V02F-mangrove-coastal-protection", "The comparison and its concession are explicit; the wrong options are an extreme, a detail and a reversal.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 019
ps("V02-F-019", "Science and environment", "Projected certainty in scientific advice costs more trust in the long run than candour about uncertainty.", "Difficult",
   "Scientists advising the public are often urged to speak with one clear voice, on the theory that any admission of uncertainty will be seized upon and used to justify inaction. The worry is real, but the remedy of projected certainty has a cost that is paid later. When advice delivered as settled turns out to need revision, as advice on a fast-moving problem often does, the public has no way of telling a normal update from an error, and trust falls not only in the revised claim but in the advisers themselves. Stating plainly what is known, what is suspected and what might change does invite some to exploit the gaps. But it also prepares people for revision, so that a change of advice can be read as the system working rather than failing. Candour about uncertainty is not a weakness to be managed; over any length of time it is the condition on which credibility depends.",
   "Admitting uncertainty may let some exploit the gaps, but projecting certainty costs more, since later revisions then look like failures and erode trust in the advisers.",
   [("Scientific advisers should present one confident message to the public, because any admission of uncertainty will be seized upon and used to justify doing nothing.",
     "This is the advice the paragraph reports and rejects; it accepts that 'the worry is real' but says projected certainty 'has a cost that is paid later'."),
    ("Since advice on fast-moving problems is usually revised, the public should treat all scientific guidance as provisional and wait for settled conclusions before acting.",
     "The paragraph addresses how advisers should speak, not whether the public should delay action, and nothing in it recommends waiting for settled conclusions."),
    ("Openly stating uncertainty stops people from exploiting gaps in scientific knowledge, since a public prepared for revision will not be misled by those who doubt the advice.",
     "The paragraph concedes that candour 'does invite some to exploit the gaps'; its claim is that candour preserves trust despite this, not that it prevents exploitation.")],
   "The paragraph grants that 'the worry is real' and that candour 'does invite some to exploit the gaps', but argues that projected certainty makes revisions look like errors, so trust falls 'in the advisers themselves'. Candour 'prepares people for revision' and is 'the condition on which credibility depends'. The correct answer keeps the concession and the comparison of costs.",
   "Choosing the option that praises candour but erases the concession that it invites exploitation.",
   "V02F-communicating-scientific-uncertainty", "The most tempting wrong option agrees with the author's stance but contradicts a concession, so it must be rejected on a fine point.",
   exams=DT)

# ------------------------------------------------------------------ 020
ps("V02-F-020", "Science and environment", "Genetic uniformity makes crops efficient but exposes them to sweeping, if rare, disease losses.", "Easy",
   "Planting vast areas with a single, genetically uniform variety of a crop makes farming efficient: every plant ripens at the same time, responds to the same fertiliser and can be harvested by the same machine. The same uniformity, however, creates a hidden vulnerability. A disease or pest that can overcome the defences of one plant can overcome those of all of them, so it spreads through the field, and through every field planted with that variety, without meeting resistance. A mixed planting, in which plants differ in their defences, slows such spread because the pathogen keeps running into hosts it cannot attack. The efficiency of uniformity is visible every season; its risk appears rarely, but when it does, it can arrive all at once.",
   "Genetic uniformity makes crops efficient but leaves all plants open to any disease that beats one, a rare but sweeping risk that mixed planting reduces.",
   [("Farmers should give up uniform crop varieties altogether, since diseases and pests regularly destroy whole harvests that have been planted with a single variety of a crop.",
     "The paragraph says the risk 'appears rarely', not regularly, and it recommends nothing; it sets the efficiency of uniformity against an occasional danger."),
    ("Uniform crop varieties all ripen together, respond to the same fertiliser and can be harvested by a single machine, which makes large-scale farming highly efficient.",
     "This repeats only the first sentence; it leaves out the hidden vulnerability that is the paragraph's main point."),
    ("Mixed plantings are immune to disease because their plants have different defences, so pathogens cannot spread through them as they do through uniform fields.",
     "The paragraph says mixed planting 'slows such spread', not that it makes crops immune or stops spread entirely.")],
   "The paragraph states that uniformity 'makes farming efficient' but 'creates a hidden vulnerability', because a pathogen that beats one plant beats all; mixed planting 'slows such spread'. Its last sentence frames the trade-off: efficiency visible each season, a risk that 'appears rarely' but 'can arrive all at once'. The correct answer holds the trade-off.",
   "Choosing the efficiency description, or overstating what mixed planting achieves.",
   "V02F-monoculture-crop-vulnerability", "The trade-off is explicit and the wrong options misstate its frequency, its scope or the remedy.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 021
ps("V02-F-021", "Science and environment", "Night lighting harms wildlife by distorting light cues, and unusually it can be reversed at once.", "Medium",
   "Artificial light at night is usually discussed as a loss for astronomers and stargazers, but its larger effects fall on other species. Many animals use darkness and the cycle of light as information: moths navigate by it, some birds time their migration by it, and newly hatched turtles find the sea by moving towards the brighter horizon over the water. A lit coastline or city confuses these cues, so that insects circle lamps until they are exhausted, birds strike illuminated buildings and hatchlings crawl inland. What makes the problem unusual among forms of pollution is that it can be reversed almost instantly: unlike a poisoned river, a lit landscape is restored the moment the lights are dimmed or shielded. The difficulty is not technical but a matter of persuading people that darkness has value.",
   "Night lighting harms animals by confusing the light cues they depend on, and since it can be undone at once, the obstacle is valuing darkness, not technology.",
   [("Artificial light at night is chiefly a problem for astronomers and stargazers, who can no longer observe the night sky clearly from cities and brightly lit coastlines.",
     "The paragraph says this usual framing misses the point, since 'its larger effects fall on other species'."),
    ("Newly hatched turtles that would normally head for the brighter horizon over the sea now crawl inland because of the lights along developed coastlines.",
     "This is one example among several; it omits both the general harm to wildlife and the unusual reversibility that the paragraph stresses."),
    ("Light pollution does more harm to wildlife than the chemical pollution of rivers, because animals depend on darkness for navigation, migration and finding the sea.",
     "The paragraph compares light with a poisoned river only in how quickly each can be reversed, not in how much harm each does.")],
   "The paragraph explains that animals 'use darkness and the cycle of light as information' and that lighting 'confuses these cues'. It then notes what is 'unusual' about this pollution: it 'can be reversed almost instantly', so the difficulty 'is not technical'. The correct answer holds the harm, the reversibility and the conclusion.",
   "Reading the river comparison as a comparison of harm rather than of reversibility.",
   "V02F-light-pollution-ecology", "One wrong option misreads the function of the river comparison, which needs care to reject.")

# ------------------------------------------------------------------ 022
ps("V02-F-022", "Technology", "Complex, frequently changed password rules backfire, while long memorable phrases work better.", "Easy",
   "Many systems require passwords to contain capital letters, numbers and symbols, and to be changed every few months. The rules are meant to make passwords harder to guess, but they often achieve the opposite. Faced with demands they cannot remember, people adopt predictable patterns: a capital at the start, a number and an exclamation mark at the end, and a digit increased by one at each forced change. Attackers know these patterns well. Others simply write their passwords down or reuse them across sites. A long phrase that is easy for its owner to remember but not linked to them in any obvious way is generally stronger than a short string of mixed symbols, and it does not need to be changed unless there is reason to think it has been exposed.",
   "Strict, often changed password rules drive people into predictable habits that weaken security, whereas long memorable phrases, changed only after exposure, generally protect better.",
   [("Passwords give no real protection at all, since attackers already know the patterns people use and can guess almost any password that a person is able to remember.",
     "The paragraph says a long memorable phrase 'is generally stronger', so it does not claim that every memorable password can be guessed."),
    ("People forced to change their passwords often add one to the final digit, and they commonly place a capital letter at the start and a symbol at the end.",
     "This is the illustration of predictable patterns; it leaves out both the claim that the rules backfire and the better alternative."),
    ("Password rules fail mainly because people are careless about security, so organisations should train their users to memorise complex strings of mixed symbols instead.",
     "The paragraph blames rules that make 'demands they cannot remember', not carelessness, and it recommends long phrases rather than complex strings.")],
   "The paragraph says the rules 'often achieve the opposite' of their aim because people adopt 'predictable patterns' or write passwords down, and that a long memorable phrase 'is generally stronger' and need not be changed unless 'exposed'. The correct answer holds the critique and the alternative.",
   "Choosing the list of predictable habits, which is evidence rather than the point.",
   "V02F-password-complexity-rules", "The critique and its alternative are stated directly; wrong options are an extreme, a detail and a misplaced cause.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 023
ps("V02-F-023", "Technology", "Cockpit automation erodes the manual skill needed at the hardest moments, so work should keep it exercised.", "Medium",
   "Automation in aircraft cockpits has made flying far safer, since the systems handle routine tasks more consistently than tired humans do. But it has also changed what pilots practise. A pilot who spends most of each flight monitoring a system that rarely fails gets little experience of flying by hand, and the skill fades just as any unused skill does. The irony is that the moments when automation hands control back are precisely the unusual and difficult ones, so the human is asked to perform best in the situations for which their recent experience has least prepared them. The answer is not to abandon automation, whose benefits are real, but to design training and routine work so that people keep exercising the abilities they will need when the machine gives up.",
   "Cockpit automation improves safety but lets manual skill fade just when hard situations demand it, so training and work should keep those skills in regular use.",
   [("Because pilots lose their manual skills when automated systems fly the aircraft, airlines should reduce their reliance on automation and return to more flying by hand.",
     "The paragraph says 'The answer is not to abandon automation, whose benefits are real', so cutting back on it is the remedy it rejects."),
    ("Automated cockpit systems often fail during routine flights, so pilots must watch them constantly and be ready to take over control at a moment's notice.",
     "The paragraph describes 'a system that rarely fails' and says control returns in 'unusual and difficult' moments, not routine ones."),
    ("Pilots who spend most of each flight watching automated systems get little practice in flying by hand, and so their manual skills gradually fade as a result.",
     "This is one step of the argument; it omits the irony that skill is needed most in the hardest moments and the proposed remedy.")],
   "The paragraph grants that automation 'has made flying far safer', explains that manual skill 'fades' with disuse, and notes the irony that control returns in 'the unusual and difficult' moments. Its remedy is not to abandon automation but to design training so people 'keep exercising the abilities they will need'. The correct answer holds the benefit, the problem and the remedy.",
   "Choosing the remedy the paragraph explicitly rejects because it follows naturally from the problem.",
   "V02F-automation-deskilling-pilots", "One wrong option draws a natural but rejected conclusion and another is an accurate partial step.")

# ------------------------------------------------------------------ 024
ps("V02-F-024", "Technology", "Following app directions teaches less about a route, but the effect depends on how the tool is used.", "Easy",
   "People who follow turn-by-turn directions from a phone tend to remember less about the route afterwards than people who found their own way with a map. This is hardly surprising: following instructions requires attention to the next turn, not to the layout of the streets, and what we do not attend to we do not learn. It would be wrong, though, to conclude that navigation apps are steadily damaging our brains. The finding concerns what is learned on a given trip, and someone who uses an app to get around a new city but then explores it on foot can build a perfectly good mental map. The effect depends on how the tool is used, not merely on whether it is used.",
   "Following app directions teaches less about a route because attention goes to the next turn, but this reflects how the tool is used, not lasting harm from using it.",
   [("Navigation apps steadily weaken the brain's ability to form mental maps, so that people who rely on them gradually lose their sense of direction altogether.",
     "The paragraph says 'It would be wrong, though, to conclude that navigation apps are steadily damaging our brains', which this option asserts."),
    ("A traveller who uses an app to reach places in a new city and then explores the streets on foot can still build a perfectly good mental map of it.",
     "This is the example used to qualify the finding; it omits the finding itself and the general point about how the tool is used."),
    ("Paper maps are a better guide than navigation apps for travellers in unfamiliar cities, because they help such travellers reach their destinations more quickly.",
     "The paragraph compares what people remember, not how quickly they arrive, and it does not rank maps above apps as guides.")],
   "The paragraph reports that app users 'remember less about the route', explains this by attention, and then qualifies it: the finding 'concerns what is learned on a given trip', and 'the effect depends on how the tool is used'. The correct answer states the finding and its qualification.",
   "Overstating a trip-level finding into a claim of lasting brain damage.",
   "V02F-satnav-spatial-memory", "The finding and its qualification are both stated outright; the extreme wrong option is explicitly denied.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 025
ps("V02-F-025", "Technology", "Technical debt is like a loan in buying speed now, but unlike one its cost is hidden, so teams take on too much.", "Medium",
   "Software engineers speak of technical debt: the future cost created when code is written quickly rather than well. The metaphor is apt in one respect, since like a loan a shortcut lets a team deliver something sooner in exchange for paying more later, and taking it on can be a sensible choice. But it misleads in another. A financial debt has a known balance and a schedule of payments, so a borrower can decide whether it is worth it. The cost of hasty code is rarely visible; it shows up as features that take longer than expected and failures nobody can easily trace, and it grows in ways no one has agreed to. Teams therefore tend to take on far more of it than they would if the bill arrived in writing.",
   "Like a loan, a coding shortcut can sensibly buy speed at a later price, but its cost is hidden and grows unchecked, so teams take on too much.",
   [("Writing code quickly rather than well is always a mistake, because the hidden costs of shortcuts eventually exceed any benefit gained by delivering software sooner.",
     "The paragraph says taking on technical debt 'can be a sensible choice', so 'always a mistake' contradicts it."),
    ("Hasty code reveals its cost through features that take longer than expected to build and through failures that nobody in the team is able to trace easily.",
     "This describes how the cost appears; it leaves out the comparison with a loan and the conclusion that teams take on too much."),
    ("Technical debt closely resembles financial debt, since both have a known balance and a schedule of payments that let a team judge whether a particular shortcut is worthwhile.",
     "The paragraph says the metaphor 'misleads' precisely because the cost of hasty code, unlike a loan, has no known balance and 'is rarely visible'.")],
   "The paragraph compares technical debt with a loan: apt because a shortcut buys speed 'in exchange for paying more later' and 'can be a sensible choice'; misleading because a loan has 'a known balance', while the cost of hasty code 'is rarely visible' and grows 'in ways no one has agreed to'. So teams 'take on far more of it'. The correct answer holds both sides of the comparison and the consequence.",
   "Keeping only the apt half of the metaphor and missing where it misleads.",
   "V02F-software-technical-debt", "The correct answer must hold where an analogy fits and where it fails; one wrong option keeps only the fit.")
