import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DX = ("CAT", "XAT")

# 001 -------------------------------------------------------------------------------------------
pj("V01-K-001", "Society and culture",
   "Labour-saving appliances raised standards of cleanliness, so they saved less labour than promised.", "Medium",
   ["Washing machines, vacuum cleaners and electric irons were sold to households with the promise that they would free people from the drudgery of domestic work.",
    "Yet many historians of the household have argued that the hours spent on housework fell far less than the advertisements implied.",
    "The explanation is that the machines did make each task easier, but they also raised the standard of what counted as done: clothes were washed after one wearing, and floors were expected to shine.",
    "The effort saved on each task was thus spent on doing more tasks more often, which is how a labour-saving device can fail to save labour at all."],
   "Sentence [[1]] opens with the promise made for the appliances. Sentence [[2]] begins with 'Yet' and reports the puzzle that housework hours fell less than promised. Sentence [[3]] offers 'The explanation': the machines eased each task but raised standards. Sentence [[4]] draws the conclusion with 'thus', turning the solution into the general point that a labour-saving device need not save labour. A puzzle must be stated before its solution, so sentence [[3]] cannot come before sentence [[2]].",
   "Placing sentence [[3]] straight after sentence [[1]] because both describe the machines, which puts 'The explanation' before the puzzle it explains.",
   "V01K-household-appliances-housework",
   "The middle pair is fixed by the logic of puzzle followed by explanation rather than by a reference word.",
   traps=[("1324", "Sentence [[3]] explains why hours did not fall; placed before sentence [[2]] it answers a question nobody has yet asked, and 'Yet' in sentence [[2]] then has nothing to contrast with except an explanation that already concedes the point.")])

# 002 -------------------------------------------------------------------------------------------
pj("V01-K-002", "Society and culture",
   "Sports fans stay loyal through every change because the team carries a story about themselves.", "Easy",
   ["Few attachments are as durable as the one a person forms with a sports club in childhood.",
    "Players come and go, owners sell up, and the team may even move its ground to another part of the city.",
    "Through all these changes the fan's loyalty often survives, attaching itself to the name and colours rather than to any particular people.",
    "In this sense supporters are loyal less to a team than to a story about themselves that the team allows them to keep telling."],
   "Sentence [[1]] introduces the subject, the durability of a childhood attachment to a club. Sentence [[2]] lists the changes a club undergoes. Sentence [[3]] refers to 'all these changes' and says loyalty survives them. Sentence [[4]] begins 'In this sense' and interprets that survival as loyalty to a story about oneself.",
   "Starting with sentence [[2]] because it is vivid, although it never names what is changing until sentence [[1]] has introduced the club.",
   "V01K-sports-fan-loyalty",
   "Reference phrases ('all these changes', 'In this sense') fix the order once the opener is found.",
   cognitive="Understanding",
   traps=[("2134", "Sentence [[2]] cannot open: 'the team' and 'its ground' assume a club that only sentence [[1]] introduces, and 'all these changes' in sentence [[3]] must follow the list directly.")])

# 003 -------------------------------------------------------------------------------------------
pj("V01-K-003", "Society and culture",
   "Given names rise and fall like fads because parents of a generation independently seek the same kind of freshness.", "Difficult",
   ["No industry promotes given names, and nobody profits when a particular one becomes popular.",
    "Yet the popularity of a name rises and falls on the familiar curve of a fad, climbing slowly, peaking and fading within a generation, as though someone were marketing it.",
    "The puzzle dissolves once we notice how parents tend to choose: they look for a name that is uncommon but not strange, one that sounds fresh to their ear.",
    "Because parents of the same generation have heard much the same names while growing up, their ears agree, and they arrive independently at the same few choices.",
    "A name picked for its distinctiveness thus becomes common, and in becoming common it begins to sound dated to the next cohort of parents, who avoid it for the very reason it was once chosen."],
   "Sentence [[1]] states the background fact that nobody markets names. Sentence [[2]] sets up the puzzle with 'Yet': names still behave like marketed fads. Sentence [[3]] calls this 'the puzzle' and begins the answer with the way parents choose, seeking freshness. Sentence [[4]] adds why many parents converge on the same names. Sentence [[5]] concludes with 'thus': the name chosen as distinctive becomes common and then dated, which completes the rise and the fall described in sentence [[2]].",
   "Putting sentence [[5]] immediately after sentence [[2]] because both describe a name rising and falling, which leaves 'distinctiveness' and 'thus' without the reasoning of sentences [[3]] and [[4]].",
   "V01K-baby-name-fashions",
   "Five abstract sentences; the closing sentence echoes the fad curve and tempts an early placement, and the two explanatory sentences must be ordered by seeing that convergence presupposes the preference for freshness.",
   exams=DX,
   traps=[("12534", "Sentence [[5]] repeats the rise and fall of sentence [[2]] but its 'thus' and 'distinctiveness' depend on the preference for freshness in sentence [[3]] and the convergence in sentence [[4]], so it cannot follow sentence [[2]] directly."),
          ("12435", "Sentence [[4]] says the parents' 'ears agree', but what their ears are listening for, a fresh but not strange name, is introduced only in sentence [[3]], which also names 'the puzzle' and so must come right after sentence [[2]]."),
          ("12354", "After sentence [[3]] the 'thus' of sentence [[5]] has no ground, because a preference for fresh names does not make any one name common until sentence [[4]] shows that parents converge on the same choices; sentence [[4]] placed last would explain a result already narrated.")])

# 004 -------------------------------------------------------------------------------------------
pj("V01-K-004", "Society and culture",
   "Open-plan offices can reduce conversation because being overheard makes people guarded; privacy enables collaboration.", "Medium",
   ["Open-plan offices were championed on the grounds that removing walls would encourage colleagues to talk to one another and share ideas.",
    "In many offices that adopted them, however, the effect has often seemed to be the reverse, as people put on headphones and send messages to colleagues a few desks away.",
    "Being visible to everyone, it appears, makes people more guarded rather than more open, since any conversation can be overheard by the whole room.",
    "Privacy, on this view, is not the enemy of collaboration but one of its conditions, because people share half-formed ideas only where they can afford to be wrong in front of a few listeners."],
   "Sentence [[1]] states the case made for open-plan offices. Sentence [[2]] reports with 'however' that the effect often seemed reversed. Sentence [[3]] explains the reversal: visibility makes people guarded. Sentence [[4]] generalises that explanation into a view ('on this view') about privacy and collaboration.",
   "Placing sentence [[4]] before sentence [[3]], though 'on this view' needs the explanation in sentence [[3]] to refer to.",
   "V01K-open-plan-offices",
   "The connectives help, but the step from the observed reversal to its explanation and then to a general view must be followed.",
   traps=[("1243", "Sentence [[4]] says 'on this view', but at that point no view has been offered, only an observation; the explanation in sentence [[3]] must come first.")])

# 005 -------------------------------------------------------------------------------------------
pj("V01-K-005", "History and politics",
   "Natural ice was harvested, stored and shipped until mechanical ice-making ended the trade.", "Easy",
   ["Before mechanical refrigeration, ice was a harvested crop, cut in blocks from frozen lakes and ponds during the coldest weeks of winter.",
    "Packed in sawdust and stored in thick-walled ice houses, these blocks could last well into the following summer.",
    "Some merchants realised that well-insulated ice could survive even a long sea voyage, and began shipping it to hot ports far from any frozen lake.",
    "The trade collapsed only when machines that could make ice anywhere, at any time, removed the advantage of a cold winter."],
   "Sentence [[1]] introduces ice as a harvested crop. Sentence [[2]] refers to 'these blocks' and explains how they were stored. Sentence [[3]] extends storage to shipping over long voyages. Sentence [[4]] ends the story with the collapse of the trade when ice could be manufactured.",
   "Placing sentence [[3]] before sentence [[2]], although the idea that insulated ice survives a voyage builds on the storage method described in sentence [[2]].",
   "V01K-natural-ice-trade",
   "A chronological sequence with a clear back-reference ('these blocks').",
   cognitive="Understanding",
   traps=[("1324", "Sentence [[3]] assumes that insulation preserves ice, which sentence [[2]] establishes, and 'these blocks' in sentence [[2]] must follow sentence [[1]] directly.")])

# 006 -------------------------------------------------------------------------------------------
pj("V01-K-006", "History and politics",
   "Early modern coffeehouses fostered debate in which argument outweighed rank, though historians dispute how open they were.", "Medium",
   ["In several European cities of the seventeenth and eighteenth centuries, coffeehouses became places where strangers could sit together and discuss the news.",
    "For the price of a cup, a customer could read the pamphlets and newspapers left on the tables and join whatever argument was under way.",
    "What made these rooms unusual, however, was not the drink or the reading matter but the convention that rank mattered less inside them than the force of what one said.",
    "Some historians have seen in this convention an early form of public opinion, formed through argument among private persons rather than handed down by authority.",
    "Others caution that the openness was partial, since the customers were mostly men of some means, and the ideal of equal debate was more often professed than practised."],
   "Sentence [[1]] introduces coffeehouses as places of discussion. Sentence [[2]] describes what a customer could do there: read pamphlets and join an argument. Sentence [[3]] turns from these practical features ('not the drink or the reading matter') to the convention that made the rooms unusual. Sentence [[4]] refers to 'this convention' and reports one interpretation of it. Sentence [[5]] begins 'Others' and gives the opposing caution.",
   "Placing sentence [[3]] directly after sentence [[1]], which separates 'this convention' in sentence [[4]] from the sentence that introduces it and leaves 'the reading matter' in sentence [[3]] unexplained.",
   "V01K-coffeehouse-political-debate",
   "Five sentences; the position of the reading-matter sentence must be fixed by noticing that the 'unusual convention' sentence dismisses its details and must sit next to 'this convention'.",
   traps=[("13245", "Sentence [[3]] sets aside 'the drink or the reading matter', which only sentence [[2]] has mentioned, and 'this convention' in sentence [[4]] needs sentence [[3]] immediately before it, not sentence [[2]]."),
          ("12354", "'Others' in sentence [[5]] needs a group of interpreters to contrast with, which is 'Some historians' in sentence [[4]].")])

# 007 -------------------------------------------------------------------------------------------
pj("V01-K-007", "History and politics",
   "Writing may have begun as a way of keeping count rather than of recording speech.", "Difficult",
   ["It is tempting to suppose that writing was invented to record what people wished to say: their stories, their laws and their prayers.",
    "The earliest surviving tablets from Mesopotamia, however, consist overwhelmingly of lists of goods, rations and debts kept by administrators.",
    "On one influential account, these marks descend from small clay tokens that stood for quantities of grain or livestock long before anyone thought of representing a spoken word.",
    "If so, writing began not as a way of capturing language but as a way of keeping count, and only gradually acquired the power to say whatever a speaker could."],
   "Sentence [[1]] states a natural assumption about why writing was invented. Sentence [[2]] challenges it with 'however': the earliest tablets are administrative lists. Sentence [[3]] traces 'these marks' to accounting tokens. Sentence [[4]] opens with 'If so', accepting the account in sentence [[3]], and concludes that writing began as counting. The conclusion contradicts the assumption in sentence [[1]], so sentence [[1]] must come first as the view being overturned, not later as a premise.",
   "Reading 'If so' in sentence [[4]] as following sentence [[1]], which would make the passage conclude that writing began as counting from a premise that says the opposite.",
   "V01K-writing-from-accounting-tokens",
   "Solvers must see that the opening assumption is the view under attack and that 'If so' accepts only the token account; an order that moves the assumption later looks fluent but reverses the argument.",
   exams=DX,
   traps=[("2314", "Ending the evidence with sentence [[1]] turns the assumption into a premise, so 'If so' in sentence [[4]] would accept the very view the evidence has just undermined."),
          ("1423", "Sentence [[4]] concludes that writing began as counting, which does not follow from sentence [[1]]; 'If so' must accept the token account in sentence [[3]].")])

# 008 -------------------------------------------------------------------------------------------
pj("V01-K-008", "History and politics",
   "Prepaid uniform postage mattered more than the stamp, because it changed who paid and how much.", "Medium",
   ["Before postal reform in the nineteenth century, letters in Britain were usually paid for by the recipient, at a rate that depended on distance and the number of sheets.",
    "The system invited evasion: a sender could, for instance, mark the outside of a letter with an agreed sign, and the recipient could read the message at a glance and refuse to pay.",
    "Charging a single low rate, paid in advance by the sender, removed both the motive for such tricks and the labour of calculating each fee.",
    "The adhesive stamp was simply the device that made prepayment convenient; the real innovation was the change in who paid and how much."],
   "Sentence [[1]] describes the old system of payment by the recipient. Sentence [[2]] refers to 'The system' and shows how it invited evasion. Sentence [[3]] describes the reform, which removed 'such tricks'. Sentence [[4]] interprets the reform: the stamp only made 'prepayment', already introduced in sentence [[3]], convenient.",
   "Putting sentence [[4]] before sentence [[3]] because the stamp seems to be the obvious reform, although 'prepayment' and 'how much' presuppose the single prepaid rate of sentence [[3]].",
   "V01K-prepaid-postage-reform",
   "Back-references lock the first three sentences; the final pair requires seeing that the remark about the stamp interprets the reform of a single prepaid rate.",
   traps=[("1243", "Sentence [[4]] speaks of 'prepayment' and of a change in 'who paid and how much', both of which are introduced only by the single prepaid rate in sentence [[3]]; and 'such tricks' in sentence [[3]] must follow sentence [[2]].")])

# 009 -------------------------------------------------------------------------------------------
pj("V01-K-009", "History and politics",
   "Mass conscription helped drive the extension of the vote, so duty and entitlement grew together.", "Difficult",
   ["For centuries most European wars were fought by professionals and hired troops, while ordinary subjects contributed their taxes rather than their lives.",
    "When states began to require military service from the whole adult male population, they were asking for something far greater than money.",
    "Men compelled to risk death for a nation found it natural to ask why they should have no voice in how that nation was governed.",
    "Such demands for a voice shaped political debate in several countries, where the extension of the vote was argued for, at least in part, as the fair return for a burden every citizen now shared.",
    "If this reading is right, the right to vote and the duty to serve grew up together, and modern citizenship owes something to the barracks as well as to the debating chamber."],
   "Sentence [[1]] describes the older arrangement, in which subjects paid taxes rather than fought. Sentence [[2]] marks the change to universal service and contrasts it with 'money', which refers back to the taxes of sentence [[1]]. Sentence [[3]] gives the political consequence: those who must risk death ask for a voice. Sentence [[4]] refers to 'Such demands for a voice' and shows them taking public form in arguments for the vote. Sentence [[5]] says 'If this reading is right' and draws the general conclusion linking voting and service.",
   "Treating sentence [[3]] and sentence [[4]] as interchangeable, although the argument in sentence [[4]] presupposes the demand for a voice that sentence [[3]] explains.",
   "V01K-conscription-and-citizenship",
   "Few explicit connectives; the order follows the causal logic from conscription to the demand for a voice to the vote, and the conscription sentence tempts as an opener.",
   exams=DX,
   traps=[("21345", "Sentence [[2]] might seem to open, but 'something far greater than money' only makes sense after sentence [[1]] has said subjects paid taxes, and sentence [[3]] then could not follow sentence [[1]], which says nothing about compulsion."),
          ("12435", "'Such demands for a voice' in sentence [[4]] cannot follow sentence [[2]], where the only demand is the state's demand for service; the demand for a voice appears only in sentence [[3]], and 'this reading' in sentence [[5]] must follow the argument for the vote.")])

# 010 -------------------------------------------------------------------------------------------
pj("V01-K-010", "Economics and business",
   "Whether piece rates beat hourly pay depends on what an employer can measure, not on effort.", "Medium",
   ["Paying workers by the piece rather than by the hour seems an obvious way to reward effort, since those who produce more will earn more.",
    "And so it is, wherever output is easy to count and quality easy to see, as when fruit is picked and paid for by the crate.",
    "In tasks where a careless item looks much like a careful one, however, the same incentive rewards haste, and the employer ends up paying for work that must later be redone.",
    "The choice between the two forms of pay therefore turns less on how hard people are willing to work than on what the employer is able to measure."],
   "Sentence [[1]] states the apparent case for piece rates. Sentence [[2]] ('And so it is') confirms it for tasks where output and quality are visible. Sentence [[3]] contrasts this with tasks where quality is hidden, in which piece rates reward haste. Sentence [[4]] concludes with 'therefore' that the choice depends on what can be measured, a conclusion that needs both the case where measurement is easy and the case where it is not.",
   "Placing sentence [[3]] right after sentence [[1]] as the obvious objection, which leaves 'And so it is' in sentence [[2]] confirming a claim that has just been undercut.",
   "V01K-piece-rate-wages",
   "The order depends on seeing the argument as claim, confirmation in one domain, failure in another and then a synthesis.",
   traps=[("1324", "'And so it is' in sentence [[2]] must answer the claim of sentence [[1]] directly; after sentence [[3]] it would confirm a claim the passage has just undermined, and 'the same incentive' in sentence [[3]] needs the working case of sentence [[2]] before it.")])

# 011 -------------------------------------------------------------------------------------------
pj("V01-K-011", "Economics and business",
   "Group lending with joint liability lets neighbours do the screening and collecting a lender cannot.", "Difficult",
   ["A lender advancing small sums to poor households faces two problems at once: it cannot tell careful borrowers from careless ones, and it has nothing to seize when a loan goes bad.",
    "Lending to small groups whose members are jointly liable for one another's debts addresses both problems without any new information ever reaching the lender.",
    "A member who must answer for a partner's default will choose partners known to be reliable, and will press any partner who begins to fall behind with repayments.",
    "By choosing and pressing their partners in this way, the members in effect do the screening and the collecting that the lender cannot, using knowledge no loan officer could gather cheaply."],
   "Sentence [[1]] sets out the lender's two problems: it cannot sort borrowers, and it cannot recover bad loans. Sentence [[2]] proposes joint-liability group lending as a remedy for both. Sentence [[3]] says what a member who must 'answer for a partner's default', that is, a member of such a group, will do: choose reliable partners and press laggards. Sentence [[4]] sums up ('in this way', 'in effect'): choosing partners is the screening and pressing laggards is the collecting, the two tasks that answer the two problems of sentence [[1]].",
   "Ending with sentence [[3]] because it describes the mechanism in detail, although sentence [[4]] is a summary that maps the mechanism onto the two problems and cannot precede what it summarises.",
   "V01K-group-lending-microfinance",
   "The lender's two problems must be matched with 'screening' and 'collecting' in the summary; the summary and the mechanism are easily swapped.",
   exams=DX,
   traps=[("1243", "Sentence [[4]] begins 'By choosing and pressing their partners in this way', which refers to the behaviour described in sentence [[3]]; placed before it, the summary would sum up something not yet said."),
          ("1324", "Sentence [[3]] speaks of a member who must 'answer for a partner's default', which presupposes the jointly liable groups introduced only in sentence [[2]].")])

# 012 -------------------------------------------------------------------------------------------
pj("V01-K-012", "Economics and business",
   "Both manufacturers' design and buyers' preferences shape how quickly goods become obsolete.", "Easy",
   ["Many household goods, from phones to printers, seem to wear out or become unusable sooner than their materials alone would require.",
    "Critics call this planned obsolescence and accuse manufacturers of designing products to fail so that customers will have to buy again.",
    "Manufacturers reply that buyers themselves demand lighter, cheaper and more elaborate goods, and that such goods are inevitably harder to make durable.",
    "The truth probably lies between these positions, since both the design of products and the preferences of buyers shape how long things last."],
   "Sentence [[1]] states the observation. Sentence [[2]] gives the critics' name and charge for it ('this'). Sentence [[3]] gives the manufacturers' reply to that charge. Sentence [[4]] weighs 'these positions' and settles between them.",
   "Putting the manufacturers' reply before the critics' charge, though a reply needs a charge to answer.",
   "V01K-planned-obsolescence",
   "A charge, a reply and a verdict; each step is clearly signalled.",
   cognitive="Understanding",
   traps=[("1324", "Sentence [[3]] is a reply ('Manufacturers reply'), so the accusation in sentence [[2]] must come before it.")])

# 013 -------------------------------------------------------------------------------------------
pj("V01-K-013", "Economics and business",
   "Loyalty-card discounts are payments for purchase data worth more to retailers than the discount.", "Medium",
   ["Supermarket loyalty cards are usually presented as a reward to customers, a small discount in return for coming back.",
    "For the retailer, however, the discount is less a gift than a payment, the price at which it buys a detailed record of what each household purchases.",
    "Such records reveal patterns that no shop assistant could notice, such as which products tend to be bought together and how a family's habits change over a year.",
    "With knowledge of such patterns the retailer can decide what to stock, where to place it on the shelves and which offers to send to which customers.",
    "Measured against the gains from stocking, shelving and targeting offers with such precision, the discount that pays for the information begins to look small."],
   "Sentence [[1]] gives the customer-facing view of loyalty cards. Sentence [[2]] contrasts the retailer's view with 'however': the discount buys a record of purchases. Sentence [[3]] refers to 'Such records' and says what they reveal. Sentence [[4]] says what the retailer does 'with knowledge of such patterns', the patterns of sentence [[3]]. Sentence [[5]] weighs the discount against the gains from 'stocking, shelving and targeting offers', which are the uses listed in sentence [[4]], so it must come last.",
   "Placing sentence [[5]] directly after sentence [[2]] because both speak of the discount as a payment, although sentence [[5]] measures it against gains that are listed only in sentence [[4]].",
   "V01K-loyalty-card-data",
   "Five sentences with a tempting early placement of the evaluative final sentence.",
   traps=[("12534", "Sentence [[5]] measures the discount against stocking, shelving and targeting offers, which are introduced only in sentence [[4]]; and 'Such records' in sentence [[3]] needs the 'detailed record' of sentence [[2]] immediately before it.")])

# 014 -------------------------------------------------------------------------------------------
pj("V01-K-014", "Science and environment",
   "Suppressing every wildfire let fuel build up and produced worse fires, so managers now use controlled burns.", "Medium",
   ["For much of the twentieth century, forest managers in several countries treated every wildfire as an enemy to be put out as quickly as possible.",
    "In forests adapted to frequent low fires, this policy allowed dead wood and undergrowth to build up year after year.",
    "When a fire eventually escaped control, it found so much fuel that it burned far hotter than the small fires it replaced, killing trees that would once have survived.",
    "Many managers now set controlled burns on purpose, accepting small fires in order to prevent catastrophic ones."],
   "Sentence [[1]] describes the policy of putting out every fire. Sentence [[2]] gives its first effect, a build-up of fuel. Sentence [[3]] gives the second effect, which depends on the first: when a fire escaped it found 'so much fuel' and burned hotter. Sentence [[4]] describes the present response, which only makes sense once the danger of accumulated fuel is clear.",
   "Placing sentence [[4]] immediately after sentence [[1]] as a simple then-and-now contrast, which separates the response from the causal chain that justifies it.",
   "V01K-wildfire-suppression-paradox",
   "The order follows a causal chain (policy, fuel build-up, hotter fires, new practice) rather than chronology alone.",
   traps=[("1423", "Sentence [[4]] says small fires prevent catastrophic ones, but the link between suppression and catastrophic fires is established only in sentences [[2]] and [[3]]; and 'this policy' in sentence [[2]] must follow sentence [[1]].")])

# 015 -------------------------------------------------------------------------------------------
pj("V01-K-015", "Science and environment",
   "Vaccines need an unbroken cold chain, which is hard to keep in remote areas.", "Easy",
   ["Many vaccines lose their potency if they become too warm, and some are also damaged by freezing.",
    "They must therefore be kept within a narrow range of temperatures all the way from the factory to the moment of injection.",
    "This unbroken sequence of refrigerators, insulated boxes and cooled vehicles is known as the cold chain.",
    "In remote areas with unreliable electricity, keeping the cold chain intact can be harder than obtaining the vaccine itself, which is why heat-stable vaccines are so valued."],
   "Sentence [[1]] states the problem of temperature sensitivity. Sentence [[2]] draws the consequence with 'therefore'. Sentence [[3]] names the resulting sequence 'the cold chain'. Sentence [[4]] uses that name and describes the difficulty of keeping it in remote areas.",
   "Placing sentence [[4]] before sentence [[3]], although sentence [[4]] uses the term 'cold chain' that sentence [[3]] introduces.",
   "V01K-vaccine-cold-chain",
   "A definition followed by its use, with 'therefore' and 'This' as clear links.",
   cognitive="Understanding",
   traps=[("1243", "Sentence [[4]] speaks of 'the cold chain' as a known term, but the term is defined only in sentence [[3]].")])

# 016 -------------------------------------------------------------------------------------------
pj("V01-K-016", "Science and environment",
   "Glacier-fed rivers may run high for a while as warming draws down the ice store, hiding a coming shortage.", "Difficult",
   ["Rivers fed by mountain glaciers are especially valuable in late summer, when rain is scarce and the ice releases water stored over many winters.",
    "As the climate warms these glaciers melt faster, and for a time the rivers they feed may actually carry more water than before.",
    "The extra flow comes from drawing down the store itself, much as a household might live comfortably for a while by spending its savings.",
    "Once the glaciers have shrunk past a certain point, summer flows must fall, and communities that planned around the temporary surplus will face a shortage they did not see coming."],
   "Sentence [[1]] establishes glaciers as a store of water released in late summer. Sentence [[2]] says warming increases river flow for a time. Sentence [[3]] reinterprets that increase: it is the store being spent, like savings. Sentence [[4]] follows from this: once the store shrinks, flows must fall, and the 'surplus' is called 'temporary' because sentence [[3]] has shown that it is a drawdown.",
   "Putting sentence [[4]] straight after sentence [[2]] as the natural sequel of faster melting, although it treats the extra water as a 'temporary surplus', which only the savings analogy in sentence [[3]] has shown it to be.",
   "V01K-glacier-meltwater-supply",
   "The shortage sentence reads fluently right after the faster-melting sentence, with the savings analogy as a closing remark; rejecting that order requires seeing that 'temporary surplus' depends on the analogy.",
   exams=DX,
   traps=[("1243", "Sentence [[4]] calls the surplus 'temporary' and predicts that flows 'must fall'; these follow only once sentence [[3]] has shown that the extra water is the store being spent, so sentence [[3]] must come between them."),
          ("2314", "Sentence [[3]] refers to 'the store itself', which is introduced in sentence [[1]] ('water stored over many winters'), and 'these glaciers' in sentence [[2]] needs sentence [[1]] before it.")])

# 017 -------------------------------------------------------------------------------------------
pj("V01-K-017", "Science and environment",
   "Mangroves protect coasts from storm surges, so some authorities replant what was cleared.", "Easy",
   ["Along many tropical coasts, mangrove forests grow in the shallow zone where land meets sea.",
    "Their roots, arching down into the mud, break the force of waves and hold silt in place that the tide would otherwise carry off.",
    "For this reason, coastal villages behind healthy mangroves tend to suffer less damage from storm surges than villages on cleared shores.",
    "Yet mangroves have often been cut down to make room for fish ponds, ports and holiday resorts, which offer quicker returns.",
    "Some coastal authorities now replant them, having learned that the cheapest sea wall may be the one that grows by itself."],
   "Sentence [[1]] introduces mangrove forests. Sentence [[2]] describes 'Their' roots and what they do. Sentence [[3]] draws the protective consequence ('For this reason'). Sentence [[4]] turns with 'Yet' to the clearing of mangroves despite this value. Sentence [[5]] describes replanting, which presupposes the clearing in sentence [[4]].",
   "Placing sentence [[5]] before sentence [[4]], although replanting presupposes that mangroves were first cut down.",
   "V01K-mangrove-coastal-protection",
   "Five sentences, but each link is marked ('Their', 'For this reason', 'Yet', replanting after clearing).",
   cognitive="Understanding",
   traps=[("12354", "Replanting in sentence [[5]] assumes the forests were cleared, which is stated only in sentence [[4]]."),
          ("12435", "'For this reason' in sentence [[3]] must follow the roots' action in sentence [[2]], and 'Yet' in sentence [[4]] needs the protective value of sentence [[3]] before it.")])

# 018 -------------------------------------------------------------------------------------------
pj("V01-K-018", "Science and environment",
   "Irrigation without drainage leaves salt that can slowly ruin the land it made fertile.", "Medium",
   ["Irrigation can turn dry land into some of the most productive farmland in the world, at least for a while.",
    "The water brought to the fields, however, carries small amounts of dissolved salt, which stays behind in the soil when the water evaporates.",
    "Over decades these deposits accumulate, and in poorly drained fields they can reach levels that stunt or kill crops.",
    "The very practice that made the desert bloom can thus, without careful drainage, slowly return it to desert."],
   "Sentence [[1]] states the benefit of irrigation with a warning hedge ('at least for a while'). Sentence [[2]] introduces the problem with 'however': the irrigation water leaves salt. Sentence [[3]] describes 'these deposits' accumulating. Sentence [[4]] concludes with 'thus' that irrigation can undo itself.",
   "Starting with sentence [[2]] because it explains the mechanism, though 'the water brought to the fields' and 'however' presuppose the irrigation introduced in sentence [[1]].",
   "V01K-irrigation-soil-salinisation",
   "A cause-and-effect chain; the concluding irony requires the mechanism first.",
   traps=[("2314", "Sentence [[2]] contrasts ('however') with a benefit that has not yet been stated, and 'thus' in sentence [[4]] must follow the accumulation in sentence [[3]], not the general claim in sentence [[1]].")])

# 019 -------------------------------------------------------------------------------------------
pj("V01-K-019", "Technology",
   "As software improves, tests meant to tell humans from machines increasingly frustrate the humans.", "Medium",
   ["Many websites ask visitors to prove that they are human by reading distorted letters or picking out traffic lights in a grid of photographs.",
    "These tests rest on the assumption that some tasks are easy for people but hard for computers.",
    "As image-recognition software improves, however, the set of such tasks keeps shrinking, and the puzzles must grow harder to stay ahead.",
    "The odd result is that a test designed to admit humans and exclude machines increasingly frustrates the humans, while capable software often passes it."],
   "Sentence [[1]] describes the tests. Sentence [[2]] names the assumption behind 'These tests'. Sentence [[3]] says, with 'however', that improving software shrinks 'such tasks', forcing harder puzzles. Sentence [[4]] states 'the odd result' of that escalation.",
   "Placing sentence [[4]] before sentence [[3]], although the frustration it describes is a result of puzzles growing harder, which sentence [[3]] explains.",
   "V01K-captcha-tests",
   "Back-references fix the first three sentences; the conclusion requires the escalation to precede it.",
   traps=[("1243", "Sentence [[4]] presents 'the odd result', but the cause, puzzles growing harder as software improves, appears only in sentence [[3]]; and 'such tasks' in sentence [[3]] needs sentence [[2]].")])

# 020 -------------------------------------------------------------------------------------------
pj("V01-K-020", "Technology",
   "Because collisions in orbit can multiply debris past a threshold, the risk grows faster than the number of satellites.", "Difficult",
   ["Every satellite launched into low orbit adds to a population of objects that will remain there, in many cases, for years or decades.",
    "When two such objects collide, they do not simply vanish but shatter into thousands of fragments travelling at enormous speeds.",
    "A fragment no larger than a coin can disable a satellite, and a disabled satellite struck again becomes a fresh source of fragments.",
    "Beyond a certain density, then, collisions could feed on themselves, multiplying debris faster than it falls back to Earth.",
    "Because of this tipping point, the danger does not grow in step with the number of objects in orbit, which is why a modest rise in launches may matter far more than it seems."],
   "Sentence [[1]] establishes the growing population of orbiting objects. Sentence [[2]] says collisions between 'such objects' create fragments. Sentence [[3]] says fragments disable satellites that then produce more fragments. Sentence [[4]] draws the first inference ('then'): past a certain density the process becomes self-sustaining. Sentence [[5]] draws the second inference, 'Because of this tipping point', which refers to the density threshold of sentence [[4]]: because there is such a threshold, danger does not rise in proportion to numbers.",
   "Swapping the last two sentences because both are conclusions, although the claim that danger is not proportional to numbers depends on the threshold described in sentence [[4]].",
   "V01K-orbital-debris-cascade",
   "Two successive conclusions must be ordered by which one depends on the other; both carry inference words.",
   exams=DX,
   traps=[("12354", "Sentence [[5]] says danger does not grow in step with numbers, which follows from the existence of a runaway threshold; that threshold is introduced only in sentence [[4]], so sentence [[5]] cannot precede it."),
          ("13245", "Sentence [[3]] speaks of fragments before any collision has produced them; the fragments come from the collision described in sentence [[2]].")])

# 021 -------------------------------------------------------------------------------------------
pj("V01-K-021", "Technology",
   "Touchscreens cut costs for carmakers but distract drivers, so some physical controls are returning.", "Easy",
   ["In many new cars, physical buttons and knobs have been replaced by a single large touchscreen.",
    "Manufacturers favour the change because one screen is cheaper to build than dozens of separate controls and can be updated with new features.",
    "Drivers, however, cannot find a spot on a smooth screen by touch, so they must take their eyes off the road to adjust even the temperature.",
    "For this reason some carmakers have begun to bring back physical controls for the functions that drivers use most often."],
   "Sentence [[1]] describes the change to touchscreens. Sentence [[2]] gives the manufacturers' reason for 'the change'. Sentence [[3]] gives the drawback for drivers with 'however'. Sentence [[4]] says 'For this reason', referring to that drawback, some carmakers are restoring controls.",
   "Placing sentence [[4]] after sentence [[2]], although bringing back physical controls is a response to the drivers' problem in sentence [[3]], not to the manufacturers' savings.",
   "V01K-touchscreen-car-controls",
   "Clear connectives and a simple advantage, drawback and response structure.",
   cognitive="Understanding",
   traps=[("1243", "'For this reason' in sentence [[4]] must refer to the distraction described in sentence [[3]]; the cost savings in sentence [[2]] are a reason to keep touchscreens, not to remove them.")])

# 022 -------------------------------------------------------------------------------------------
pj("V01-K-022", "Arts and literature",
   "Sequels must balance familiarity and surprise; the best keep the characters and change the situation.", "Medium",
   ["Studios favour sequels because an audience that enjoyed the first film is a market that already exists.",
    "The familiarity that guarantees this audience also sets a trap, since viewers want both to recognise what they loved and to be surprised.",
    "Lean too far toward the first desire and the film is dismissed as a copy; lean toward the second and it is accused of betraying the original.",
    "The best sequels escape this bind by keeping the characters audiences care about and placing them in a situation the first film never imagined."],
   "Sentence [[1]] gives the commercial reason for sequels. Sentence [[2]] says the familiarity behind 'this audience' also sets a trap, because viewers want two things. Sentence [[3]] refers to 'the first desire' and 'the second', which are the two wants named in sentence [[2]]. Sentence [[4]] says how the best sequels escape 'this bind'.",
   "Placing sentence [[3]] after sentence [[1]] because both concern how sequels fare, though 'the first desire' and 'the second' have no referent until sentence [[2]] names the two wants.",
   "V01K-film-sequels",
   "The middle sentences are linked by the logic of the two competing desires rather than by an obvious pronoun.",
   traps=[("1324", "Sentence [[3]] speaks of 'the first desire' and 'the second', which only make sense after sentence [[2]] has said viewers want both recognition and surprise.")])

# 023 -------------------------------------------------------------------------------------------
pj("V01-K-023", "Arts and literature",
   "Direct address to the audience is older than the realist fourth wall it is said to break.", "Difficult",
   ["Theatre audiences are often said to watch a play through a 'fourth wall', an imaginary barrier that keeps the characters from seeing the people who look at them.",
    "An actor who turns to address those people directly is therefore described as breaking the wall, and the device is usually called modern and disruptive.",
    "Yet direct address is far older than the convention it supposedly breaks, since actors in many earlier theatres delivered asides and soliloquies straight to the crowd.",
    "What is modern, then, is not the broken wall but the wall itself, a convention that became dominant only when realism made the stage resemble a room with one side removed."],
   "Sentence [[1]] introduces the idea of the fourth wall. Sentence [[2]] follows with 'therefore': addressing 'those people', the audience, counts as breaking the wall, a device called modern. Sentence [[3]] objects with 'Yet' that direct address is older than the wall. Sentence [[4]] draws the reversed conclusion with 'then': the wall, not its breaking, is the modern thing. The conclusion needs the historical evidence of sentence [[3]] before it.",
   "Treating sentence [[4]] as the direct reply to the claim of novelty in sentence [[2]] and leaving the historical evidence of sentence [[3]] to the end, which makes 'Yet' contradict a conclusion it actually supports.",
   "V01K-theatre-fourth-wall",
   "The conclusion reverses the common view, and solvers must see that the historical evidence must precede the reversal, since both answer the claim that direct address is modern.",
   exams=DX,
   traps=[("1243", "Sentence [[4]] concludes 'then' that the wall is modern, but nothing before it has shown that direct address is old; and 'Yet' in sentence [[3]] would then oppose a conclusion it supports."),
          ("1324", "'the convention it supposedly breaks' in sentence [[3]] needs the claim that direct address breaks the wall, which is made in sentence [[2]]; and 'those people' in sentence [[2]] must follow sentence [[1]].")])

# 024 -------------------------------------------------------------------------------------------
pj("V01-K-024", "Arts and literature",
   "Sample-clearance requirements changed the sound of sample-based music, not merely its legality.", "Medium",
   ["Sampling, the practice of building a new track from fragments of existing recordings, became central to several genres of popular music.",
    "In its early years, producers often borrowed drum breaks and vocal phrases freely, treating old records as raw material.",
    "Once courts in some countries held that even short samples could infringe copyright, record labels began to insist that every fragment be cleared and paid for.",
    "The fees made dense collages of dozens of samples prohibitively expensive, and producers turned instead to a few licensed loops or to replaying the parts themselves.",
    "The law, in other words, did not merely regulate a style of music; by pricing certain sounds out of reach, it changed what that style sounded like."],
   "Sentence [[1]] defines sampling. Sentence [[2]] describes its early, free-borrowing years. Sentence [[3]] describes the legal change that ended free borrowing. Sentence [[4]] gives the effect of the clearance fees on how tracks were made. Sentence [[5]] restates that effect as a general point ('in other words'): the law changed the sound itself.",
   "Placing sentence [[5]] after sentence [[3]] because it mentions the law, although 'changed what that style sounded like' restates the change in production described in sentence [[4]].",
   "V01K-music-sampling",
   "Five sentences in chronological order; the closing restatement must follow the effect it restates.",
   traps=[("12354", "Sentence [[5]] claims the law changed the sound, which restates the turn to loops and replayed parts in sentence [[4]]; and 'The fees' in sentence [[4]] needs the clearance requirement in sentence [[3]] directly before it.")])

# 025 -------------------------------------------------------------------------------------------
pj("V01-K-025", "Arts and literature",
   "Because authors blurb their friends, blurbs reveal connections more than quality.", "Easy",
   ["The back cover of almost any new novel carries short words of praise from other writers.",
    "These blurbs are meant to reassure a browsing reader that the book is worth the risk of buying it.",
    "Readers have learned, however, that authors often praise friends, colleagues and writers who share their publisher.",
    "As a result, a blurb now tells a careful reader more about the author's connections than about the quality of the book."],
   "Sentence [[1]] introduces praise on back covers. Sentence [[2]] calls them 'These blurbs' and states their purpose. Sentence [[3]] contrasts ('however') that purpose with what readers have learned. Sentence [[4]] gives the result.",
   "Putting sentence [[3]] before sentence [[2]], which leaves 'however' with nothing to contrast and 'These blurbs' far from its referent.",
   "V01K-book-jacket-blurbs",
   "Clear reference and contrast words.",
   cognitive="Understanding",
   traps=[("1324", "'however' in sentence [[3]] contrasts with the reassuring purpose stated in sentence [[2]], so sentence [[2]] must come first.")])
