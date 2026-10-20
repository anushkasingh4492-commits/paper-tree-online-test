import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

EB = "Economics and business"
SE = "Science and environment"
TE = "Technology"
AL = "Arts and literature"
LM = "Language and media"
ED = "Education"
HARD = ("CAT", "XAT")

# 001 ---------------------------------------------------------------- winner's curse
ps("V02-I-001", EB, "The winner of an auction for an item of uncertain value has probably guessed too high, so offers should be shaded more as bidders increase.", "Medium",
   "Imagine a sealed jar of coins auctioned to a room of thirty people, each of whom guesses its contents by eye. Their guesses will fall on both sides of the real sum, and taken together they may average out remarkably well. Yet the person who takes the jar home is the one who guessed highest, and so, even if every guesser is sensible and the crowd as a whole is accurate, the buyer has very probably paid more than the jar holds. Victory in such a contest is itself evidence of having guessed too high. Better guessing cannot cure this, since no guess is free of error; what helps is to offer less than one's own guess, and to hold back further when the room is larger, because a bigger crowd throws up a more extreme top guess.",
   "When many bid on something of uncertain value, the winner has probably guessed too high, so bidders should offer below their guesses, more so in larger crowds.",
   [("The person who wins the jar of coins usually does so because he or she is a worse judge of quantities than the others in the room.",
     "The paragraph says the buyer has probably overpaid 'even if every guesser is sensible', so the problem is selecting the highest of honest errors, not poor judgement."),
    ("Guesses about the contents of the jar fall on both sides of the real sum, and when they are taken together they tend to average out quite accurately.",
     "This restates only the second sentence; it omits the central point that the winner is the highest guesser and the remedy that follows."),
    ("Since every guess contains some error, bidders should study the jar more carefully until their estimates of its contents become reliable enough to bid on.",
     "The paragraph rejects this remedy outright: 'Better guessing cannot cure this, since no guess is free of error'.")],
   "The paragraph explains a selection effect: guesses scatter around the truth, but the highest one wins, so the winner has probably paid too much; 'Victory in such a contest is itself evidence of having guessed too high.' It then gives the remedy, offering less than one's guess and holding back further in a larger room. The correct summary keeps both the mechanism and the scaled remedy.",
   "Reading the outcome as a sign of poor judgement, or picking the option that restates the scatter of guesses without the selection effect.",
   "V02I-winners-curse-auctions", "Requires seeing the selection logic and the scaled remedy; the narrow option restates accurate details.",
   cognitive="Understanding")

# 002 ---------------------------------------------------------------- extended warranties
ps("V02-I-002", EB, "Extended warranties are overpriced for most buyers but may suit those who cannot absorb a large repair bill.", "Easy",
   "Shops selling televisions and washing machines press customers hard to buy an extended warranty at the till, and the reason is simple: these contracts are among the most profitable things the shop sells. The price is set well above the expected cost of repairs, because most appliances that survive their first months go on working for years, and those that fail early are already covered by the maker's own guarantee. A buyer who can afford an occasional repair bill is therefore better off keeping the money and paying for repairs if they come. The case changes only for someone who could not absorb a sudden large expense; for that buyer, paying a premium to avoid the risk may be sensible.",
   "Extended warranties cost more than expected repairs, so buyers able to pay for repairs should decline them, though they may suit someone who cannot bear a large expense.",
   [("Extended warranties are a dishonest sales trick, and no buyer of a household appliance, whatever their circumstances, should ever agree to buy one.",
     "The last sentence makes an exception for 'someone who could not absorb a sudden large expense', so 'whatever their circumstances' contradicts the paragraph."),
    ("Appliances rarely fail after their first few months, which is why their makers are willing to offer a guarantee covering only the early period of use.",
     "The paragraph mentions early failures and the maker's guarantee only as a reason the warranty is overpriced; it does not explain why makers offer guarantees, and the option misses the main point."),
    ("Shops push extended warranties chiefly because customers who buy them are more likely to return to the same shop when they come back to buy their next household appliances.",
     "The paragraph gives a different reason: the contracts are 'among the most profitable things the shop sells'. Repeat custom is never mentioned.")],
   "The paragraph argues that extended warranties are priced 'well above the expected cost of repairs', so a buyer who can afford occasional repairs should keep the money; it then qualifies this for buyers who cannot absorb a large expense. The correct summary states the claim and the exception.",
   "Ignoring the final qualification and choosing the absolute rejection of all warranties.",
   "V02I-extended-warranties", "The claim and its single exception are stated directly in the last two sentences.",
   cognitive="Understanding")

# 003 ---------------------------------------------------------------- just in time
ps("V02-I-003", EB, "Supply shocks discredit a cost-cutting imitation of lean production, not the method that relied on supplier knowledge.", "Difficult",
   "It became common, after a run of supply disruptions, to say that lean manufacturing had been exposed as a mistake: firms that held almost no inventory had saved money in calm years and paid for it many times over when deliveries stopped. The charge contains a truth but misplaces it. Holding little stock was never the whole of the method; its purpose was to make problems visible quickly so that they could be fixed, and the firms that practised it most seriously also cultivated close, long relationships with a few suppliers and knew in detail where their parts came from. What failed in many cases was a cheaper imitation: low inventory adopted as a cost target, combined with suppliers chosen solely on price and scattered across distant regions that nobody had mapped. The lesson, then, is less that buffers are always wise than that thin buffers are safe only where the knowledge and relationships the method assumed are actually present.",
   "The disruptions discredit less lean production itself than a version that cut stock while neglecting the supplier knowledge and ties on which thin inventories safely depend.",
   [("Recent supply disruptions have shown that holding minimal inventory was a costly error, and that manufacturers ought to return to keeping large buffers of stock.",
     "This is the common charge the paragraph reports and then says 'misplaces' the truth; the conclusion explicitly denies that 'buffers are always wise'."),
    ("Lean manufacturing failed during the recent disruptions because the firms practising it most seriously relied on a handful of suppliers they knew too closely.",
     "This reverses the paragraph, which presents close, long supplier relationships and detailed knowledge as what made thin stocks safe; the failures came from imitators with unmapped, price-chosen suppliers."),
    ("Lean manufacturing remains sound in every setting, since its critics have simply confused the genuine method with the cost-cutting targets that careless imitators pursued.",
     "The last sentence makes the safety of thin buffers conditional: they are safe 'only where' the assumed knowledge and relationships exist, so 'sound in every setting' overstates the defence.")],
   "The paragraph reports the charge that lean manufacturing was a mistake, concedes it 'contains a truth', and relocates the failure to an imitation that cut inventory without the supplier relationships and knowledge the real method relied on. Its conclusion is conditional: thin buffers are safe only where those conditions hold. The correct summary keeps the relocation of blame and the condition.",
   "Choosing the unconditional defence of lean manufacturing, which sounds like the author's side but drops the 'only where' condition.",
   "V02I-just-in-time-inventory", "Two options side against the critics; only one keeps the conditional conclusion, so scope must be read precisely.",
   exams=HARD)

# 004 ---------------------------------------------------------------- franchise standardisation
ps("V02-I-004", EB, "Franchise uniformity solves the problem of buying from strangers, which is why chains and independents locate differently.", "Medium",
   "A traveller who eats at a franchised restaurant in an unfamiliar town is buying something an independent cafe cannot easily offer: the assurance that the meal will be much like the one eaten at the same chain elsewhere. The independent may cook far better, but the stranger has no way of knowing that in advance, whereas the franchise's sameness is precisely what makes its quality knowable. This is why chains cluster along highways and near stations, where most customers are passing through, while independent places flourish more often in neighbourhoods whose residents return often enough to learn which kitchens are good. Uniformity, so often mocked, is less a failure of taste than an answer to the problem of buying from strangers.",
   "Franchises thrive among passing strangers because uniformity makes their quality predictable, while independents do better with returning locals who can learn which kitchens are good.",
   [("Franchised restaurants generally serve better food than independent cafes do, which explains why travellers so often choose them along highways and near stations.",
     "The paragraph concedes that 'The independent may cook far better'; travellers choose chains for predictability, not superior food."),
    ("Chain restaurants tend to cluster along highways and near railway stations, while independent cafes are found more commonly in the quieter residential neighbourhoods of most towns and cities.",
     "This reports the pattern but drops the explanation, that uniformity makes quality knowable to strangers, which is the paragraph's point."),
    ("Towns should protect independent cafes from franchised competitors, since the uniformity of chains steadily erodes local taste and the variety of neighbourhood kitchens.",
     "The paragraph makes no policy proposal and explicitly says uniformity is 'less a failure of taste than an answer' to a problem, so this contradicts it.")],
   "The paragraph explains franchise success by the problem of buying from strangers: sameness makes quality knowable. It uses this to explain why chains cluster where customers pass through and independents thrive where residents return. The correct summary links the mechanism to the location pattern.",
   "Picking the option that states the location pattern accurately but leaves out why it arises.",
   "V02I-franchise-standardisation", "The narrow option is factually accurate to the paragraph; the key must be preferred for including the explanation.",
   cognitive="Understanding")

# 005 ---------------------------------------------------------------- coral gardening
ps("V02-I-005", SE, "Coral gardening is a useful holding action but cannot match the scale of reef loss; only curbing warming addresses the cause.", "Medium",
   "Coral gardening, in which fragments are grown in underwater nurseries and then fixed onto damaged reefs, has become the most visible form of reef restoration, and its photographs of divers planting coral are genuinely encouraging. Yet its scale should be kept in view. A well-run project may replant a few hectares, while the reefs being lost to warming seas are measured in thousands of square kilometres, and transplanted corals die in the next marine heatwave as readily as wild ones. None of this makes the work pointless: nurseries can preserve heat-tolerant strains and keep particular reefs alive for tourism or fisheries. But treating gardening as a solution to reef decline mistakes a holding action for a cure, since only reducing the warming itself addresses the cause.",
   "Coral gardening has real but local value, such as preserving tolerant strains, yet it cannot match the scale of reef loss, and only curbing warming tackles the cause.",
   [("Coral gardening is a wasteful distraction from the real problem, and conservation groups should abandon it entirely in favour of campaigning for lower emissions.",
     "The paragraph says 'None of this makes the work pointless' and lists its uses, so calling it wasteful and urging its abandonment contradicts it."),
    ("Because transplanted corals are more vulnerable to heatwaves than wild ones, coral gardening tends to speed up rather than slow down the decline of reefs.",
     "The paragraph says transplanted corals die 'as readily as wild ones', not more readily, and never claims gardening accelerates decline."),
    ("With enough funding and divers, coral nurseries could be expanded to replant reefs as quickly as warming seas are destroying them across the world.",
     "The paragraph's contrast of 'a few hectares' with 'thousands of square kilometres', and its description of gardening as 'a holding action', run against this optimistic claim.")],
   "The paragraph criticises the view that coral gardening solves reef decline: its scale is tiny compared with losses and transplants die in heatwaves. It concedes local value (tolerant strains, particular reefs) and concludes that only reducing warming addresses the cause. The correct summary keeps the concession and the conclusion.",
   "Overreading the criticism into a call to abandon gardening, ignoring the concession 'None of this makes the work pointless'.",
   "V02I-coral-reef-gardening", "One distractor captures the critical tone but drops the concession; the reader must hold both.",
   cognitive="Understanding")

# 006 ---------------------------------------------------------------- honeybee focus
ps("V02-I-006", SE, "Pollinator concern wrongly centres on honeybees; wild pollinators are the ones declining and are helped by planting, not hives.", "Easy",
   "Public concern about the decline of pollinators has fastened almost entirely on the honeybee, and campaigns urge people to keep hives in gardens and on city rooftops. The honeybee, however, is a managed farm animal, kept in large numbers by beekeepers and in little danger of disappearing. The pollinators that are genuinely declining are mostly wild: solitary bees, bumblebees, hoverflies and moths, many of which need particular flowers and undisturbed nesting ground. Adding hives can even make matters worse for these species, because dense colonies of honeybees compete with them for the same nectar and pollen. Those who wish to help pollinators would do better to plant varied native flowers and leave patches of ground untidy.",
   "Concern for pollinators wrongly centres on the managed honeybee, when the declining species are wild ones that extra hives may harm and varied planting would help.",
   [("Many wild pollinators, including solitary bees, bumblebees and hoverflies, depend on particular flowers and on undisturbed patches of nesting ground in order to survive.",
     "This is one supporting detail from the third sentence; it omits the paragraph's point that concern is misdirected at honeybees."),
    ("The honeybee is the pollinator most at risk of disappearing, so keeping more hives on rooftops and in gardens is the best way to help pollinators.",
     "The paragraph says the honeybee is 'in little danger of disappearing' and that adding hives 'can even make matters worse', so this reverses it."),
    ("Honeybee colonies are the main cause of the decline of wild pollinators, so beekeeping both in towns and in the countryside ought to be banned.",
     "The paragraph says hives 'can' make matters worse through competition, not that they are the main cause, and it proposes planting flowers, not a ban.")],
   "The paragraph criticises the popular focus on honeybees: they are managed and not endangered, the declining pollinators are wild, extra hives can harm those, and native planting would help. The correct summary contains the critique, the reason and the better course.",
   "Choosing the accurate but narrow detail about wild pollinators' needs.",
   "V02I-honeybee-pollinator-focus", "The stance is explicit from the second sentence and the distractors are clearly narrow, reversed or extreme.",
   cognitive="Understanding")

# 007 ---------------------------------------------------------------- instruments and theory
ps("V02-I-007", SE, "New instruments often set the agenda of science, though theory is still needed to interpret what they show.", "Difficult",
   "It is tempting to describe the history of science as a sequence of ideas, each tested by instruments built to check it. Often the order runs the other way. A new instrument, made for some modest practical purpose, reveals phenomena that no existing theory anticipated, and theory then scrambles to absorb them; the instrument, in effect, sets the agenda. This does not make theories mere reflections of the tools available, for a device shows nothing until someone has ideas about what its readings mean, and the same image has been read differently by observers holding different views. But it does suggest that the questions a science finds pressing at any moment depend heavily on what it has lately become able to see, and that some questions remain unasked not because they are unimportant but because nothing yet exists to make them answerable.",
   "Instruments often shape which questions science pursues by revealing what theory had not foreseen, though theory is still needed to interpret what instruments show.",
   [("Scientific theories are largely reflections of the instruments available at the time, since what scientists come to believe is fixed by what their devices display.",
     "The paragraph explicitly denies this: 'This does not make theories mere reflections of the tools available', because readings need interpretation and the same image is read differently."),
    ("Science advances as theories are proposed first and instruments are then built to test them, which is why its history is best told as a history of ideas.",
     "This is the 'tempting' description in the first sentence, which the author immediately qualifies with 'Often the order runs the other way'."),
    ("The most important scientific questions have often gone unasked because scientists preferred building practical instruments to speculating about what they could not see.",
     "The last sentence says such questions go unasked 'because nothing yet exists to make them answerable', not because of a preference, and it does not call them the most important.")],
   "The author qualifies the idea-first picture of science: instruments often reveal unanticipated phenomena and so set the agenda of questions. A concession follows, that theories are not mere reflections of tools since readings need interpretation. The correct summary holds both the claim and the concession.",
   "Taking the claim about instruments to its extreme and ignoring the concession about interpretation, or mistaking the opening description for the author's view.",
   "V02I-instruments-shape-theory", "Two distractors take one half of the argument each (reported view, overstated claim); the third distorts the final clause.",
   exams=HARD)

# 008 ---------------------------------------------------------------- urban wildlife boldness
ps("V02-I-008", SE, "Urban animals' boldness has several possible causes that only careful study can separate.", "Medium",
   "Animals living in cities often seem bolder than their rural relatives: urban birds let people approach more closely before flying off, and town foxes raid bins in daylight. It is natural to conclude that city life has bred a new temperament, and in some populations there may be genuine inherited change. But at least two other explanations fit the same observation. Individual animals may simply learn, over a lifetime of harmless encounters, that people pose little threat; or the city may attract the bolder individuals from the surrounding countryside while the timid ones stay away. Each would produce bold urban animals, and only careful study, such as raising young from both settings under identical conditions, can tell them apart.",
   "Urban animals' boldness may reflect inherited change, but learning or the arrival of bolder individuals could equally explain it, and only careful study can separate these causes.",
   [("City life has bred a genuinely new and inherited temperament in urban birds and foxes, and this explains why they tolerate people far more readily than their relatives in the countryside do.",
     "This is the 'natural' conclusion the paragraph reports and then challenges with two alternative explanations; it allows inherited change only 'in some populations'."),
    ("Urban animals merely appear bolder than rural ones because observers in cities are more likely to notice and record their encounters with wildlife.",
     "The paragraph accepts the observation of boldness and debates its cause; observer bias is never raised, so this is out of scope."),
    ("Raising young animals from the city and the countryside under identical conditions is the most reliable method of studying the temperament of wildlife in general.",
     "The paragraph offers this only as an example of the careful study needed for this question; it makes no general claim about studying wildlife temperament.")],
   "The paragraph presents a finding (urban animals seem bolder), the natural inference (an inherited temperament), and then two rival explanations, learning and selective settlement, that fit equally. It concludes that careful study is needed to tell them apart. The correct summary keeps the finding, the rivals and the methodological conclusion.",
   "Choosing the reported 'natural' conclusion as if it were the author's.",
   "V02I-urban-wildlife-boldness", "The paragraph reports a conclusion before qualifying it; the reader must separate report from stance.",
   cognitive="Understanding")

# 009 ---------------------------------------------------------------- dark patterns
ps("V02-I-009", TE, "Subscription sites deliberately make cancelling hard, keeping customers through their impatience rather than their choice.", "Easy",
   "Many websites make it easy to sign up for a subscription and remarkably hard to leave it. Joining takes a single click; cancelling requires finding a link buried in account settings, passing through several screens that ask whether the user is sure, and sometimes telephoning a support line during office hours. None of this is accidental. Designers know that each additional step causes some users to give up, and a user who gives up remains a paying customer. Such designs work not by persuading people that they want to stay but by exploiting the effort and impatience that make people abandon a task half done.",
   "Websites deliberately make cancelling far harder than joining, keeping subscribers not by persuading them to stay but by counting on them to give up.",
   [("Cancelling some online subscriptions requires users to telephone a support line, which is often open only during ordinary office hours on weekdays.",
     "This is one detail from the second sentence; it leaves out that the obstacles are deliberate and how they retain customers."),
    ("Websites make cancellation difficult mainly because their designers pay far less attention to the exit process than to the work of attracting new subscribers.",
     "The paragraph says 'None of this is accidental': designers add steps knowingly, so neglect is the wrong explanation."),
    ("Governments should require every website to let subscribers cancel with a single click, since making cancellation difficult is a form of fraud.",
     "The paragraph describes and explains the design; it proposes no law and does not call it fraud, so this adds an outside prescription.")],
   "The paragraph contrasts easy joining with hard cancelling, states that this is deliberate, and explains the mechanism: each extra step makes some users give up, and they keep paying. The correct summary contains the asymmetry, the intent and the mechanism.",
   "Choosing the neglect explanation, which overlooks 'None of this is accidental'.",
   "V02I-dark-patterns-cancellation", "Key points are stated in consecutive sentences; distractors are clearly narrow, contradicted or out of scope.",
   cognitive="Understanding")

# 010 ---------------------------------------------------------------- default settings
ps("V02-I-010", TE, "If defaults are read as advice, designers who set self-serving defaults are giving misleading advice.", "Difficult",
   "When software ships with a setting already chosen, most users never change it, and this is often described as laziness. A more charitable reading is available. A default carries an implicit message that this is what the makers, who presumably understand the product, consider suitable, and many users reasonably treat it as advice. That reading, however, cuts both ways. If defaults function as recommendations, then the people who set them bear something like the responsibility of an adviser, and a default chosen because it serves the maker's interest in data or revenue, rather than the user's, is not a neutral starting point but a misleading recommendation. The defence of inert users thus becomes a charge against designers.",
   "If users keep defaults because they reasonably take them as the makers' advice, then designers who choose defaults to serve themselves are giving misleading advice.",
   [("Most users never change software defaults because they are too lazy to explore the settings, which leaves designers free to choose whatever settings suit them.",
     "The paragraph mentions laziness only as the common description that the next sentence replaces with a more charitable reading, and it argues designers are not free of responsibility."),
    ("Defaults are neutral starting points that users would be wise to treat as advice, since software makers understand their products better than the people using them.",
     "The paragraph denies that a self-serving default is 'a neutral starting point' and never advises users to trust defaults; it turns the point into a charge against designers."),
    ("Users who leave software settings unchanged are behaving reasonably, because a default implicitly signals what the makers of a product consider suitable for them.",
     "This captures only the first move, the charitable reading of users; it misses the turn 'That reading, however, cuts both ways' and the conclusion about designers' responsibility.")],
   "The paragraph replaces the laziness explanation with a charitable one, that users treat defaults as advice, and then turns it: if defaults are advice, those who set them carry an adviser's responsibility, so self-serving defaults are misleading. The final sentence states the point: 'The defence of inert users thus becomes a charge against designers.' The correct summary includes the turn.",
   "Stopping at the charitable reading of users and missing that the paragraph's conclusion concerns designers.",
   "V02I-software-default-settings", "The too-narrow option states a true premise accurately; the key requires following the argument's turn to its conclusion.",
   exams=HARD)

# 011 ---------------------------------------------------------------- algorithmic hiring
ps("V02-I-011", TE, "Hiring software applies past biases consistently, and its apparent impartiality hides them from correction.", "Medium",
   "Firms that screen job applications with software trained on the records of past hires often defend the practice as more objective than human judgement, since the program applies the same rule to every applicant and cannot be swayed by a candidate's charm. Consistency, however, is not the same as fairness. A program that learns which applicants were hired in the past learns whatever preferences shaped those decisions, including any unjustified ones, and then applies them with perfect regularity. Human recruiters are inconsistent, but their inconsistency at least leaves room for a manager to notice and correct a pattern; a rule embedded in software may go unexamined precisely because it looks impartial.",
   "Hiring software trained on past decisions applies their biases consistently, and its look of impartiality may shield those biases from scrutiny that human judgement still allows.",
   [("Screening software is fairer than human recruiters because it applies one identical rule to every single applicant and can never be swayed by a candidate's personal charm, however persuasive it is.",
     "This is the defence the paragraph reports in its first sentence and rejects with 'Consistency, however, is not the same as fairness'."),
    ("Firms should stop using software to screen job applications altogether and return to human recruiters, whose judgement is both more reliable and more fair.",
     "The paragraph calls human recruiters 'inconsistent' and claims only that their errors are easier to notice; it neither calls them fairer nor proposes abandoning software."),
    ("Human recruiters are inconsistent in their decisions, and this inconsistency is the main source of the unfairness that appears in the hiring records of firms.",
     "The paragraph treats human inconsistency as leaving 'room for a manager to notice and correct a pattern', not as the main source of unfairness.")],
   "The paragraph critiques the claim that screening software is more objective: consistency differs from fairness, the software learns and applies past preferences including unjustified ones, and its impartial appearance can keep the rule from being examined. The correct summary keeps both the inheritance of bias and the concealment.",
   "Accepting the 'more objective' defence, or turning the critique into a blanket preference for human recruiters.",
   "V02I-algorithmic-hiring-screening", "One distractor is the reported view and another overextends the critique; both are tempting.",
   cognitive="Understanding")

# 012 ---------------------------------------------------------------- version control
ps("V02-I-012", TE, "Version control keeps every change with its reasons, which encourages experiment and explains code to newcomers.", "Medium",
   "A writer revising a manuscript on paper keeps, if anything, a few dated drafts, and the reasons behind each change are lost unless recorded separately. Software teams that use version control keep something quite different: every change, however small, is stored with its author, its time and a short note explaining it, so that any earlier state of the work can be recovered and the history of a single line traced. The difference is not merely one of convenience. Because nothing is irretrievably lost, programmers can experiment boldly, abandoning a failed approach without fear; and because each change is explained, a newcomer can learn why the code is as it is rather than only what it does.",
   "Unlike a few paper drafts, version control keeps every change with its reasons, which both frees programmers to experiment and shows newcomers why code is as it is.",
   [("Version control stores each change made to a piece of software together with the name of its author, the time it was made and a short explanatory note.",
     "This describes only the mechanism in the second sentence; it omits the paragraph's point that the difference is 'not merely one of convenience' and its two consequences."),
    ("Writers revising manuscripts ought to adopt the version control tools used by software teams, since dated paper drafts lose the reasons behind every change.",
     "The paragraph compares the two practices but recommends nothing to writers; this adds a prescription it does not make."),
    ("The chief advantage of version control over paper drafts is convenience, since earlier versions of the work can be recovered quickly whenever they are needed.",
     "The paragraph says explicitly 'The difference is not merely one of convenience' and stresses bold experiment and understanding instead.")],
   "The paragraph compares paper drafts with version control, describes what version control records, and argues that the difference matters beyond convenience: it permits bold experiment and lets newcomers learn why the code is as it is. The correct summary keeps the comparison and both consequences.",
   "Choosing the accurate description of the mechanism, which leaves out what the paragraph says follows from it.",
   "V02I-version-control-history", "The narrow option is an accurate paraphrase of one sentence; the key is preferred for including the consequences.",
   cognitive="Understanding")

# 013 ---------------------------------------------------------------- cover songs
ps("V02-I-013", AL, "A cover version is an interpretation and should be judged by what it reveals in the song.", "Easy",
   "A cover version of a song is often treated as a lesser thing than the original, a copy made by musicians who could not write their own material. Yet many of the most admired recordings in popular music are covers, and what makes them admired is precisely what they change: a different tempo, an unexpected arrangement, a singer who finds sorrow in a lyric that was first sung cheerfully. A good cover is an interpretation, in the way that a pianist's performance of a sonata is an interpretation, and it should be judged by what it reveals in the song rather than by whether its performers also wrote it.",
   "Cover versions deserve to be judged as interpretations, by what they reveal in a song, not dismissed as copies by musicians lacking material of their own.",
   [("Cover versions are usually better than the original recordings, because later musicians are able to correct the mistakes of the songwriters who came before them.",
     "The paragraph defends covers as interpretations; it never ranks them above originals or speaks of correcting songwriters' mistakes."),
    ("Many admired cover versions change the tempo or the arrangement of a song, or find sorrow in a lyric that was first sung in a cheerful manner.",
     "These are the examples in the second sentence; the option leaves out the paragraph's conclusion about how covers should be judged."),
    ("Pianists who perform sonatas and singers who record cover songs are alike in being performers who have failed to compose any original music of their own.",
     "The paragraph uses the pianist to show that a cover is a legitimate interpretation; this turns the comparison into the dismissive view it rejects.")],
   "The paragraph reports a dismissive view of covers, counters it with the observation that admired covers are admired for what they change, and concludes that a cover is an interpretation to be judged 'by what it reveals in the song'. The correct summary gives the rejected view and the alternative standard.",
   "Choosing the list of changes, which supports the point but does not state it.",
   "V02I-cover-songs-interpretation", "The conclusion is stated plainly in the final sentence.",
   cognitive="Understanding")

# 014 ---------------------------------------------------------------- ghostwriting
ps("V02-I-014", AL, "Whether ghostwriting deceives depends on what readers of a given kind of book actually expect.", "Difficult",
   "Critics of ghostwriting say that a memoir written by someone other than its named author deceives readers, who believe they are reading the subject's own words. The charge assumes a convention that many readers do not share. Few people who buy the autobiography of a famous athlete suppose that the athlete sat alone composing sentences; what they expect is that the story, the opinions and the memories are genuinely the athlete's, and that he or she has approved the result. Measured against that expectation, a ghostwritten memoir deceives only when the content is invented or the subject has not endorsed it. Where readers do expect sole authorship, as with a novel or a scholarly article, concealed ghostwriting remains a real deception.",
   "Ghostwriting deceives only when it breaks what readers expect: memoir readers expect the subject's story and approval, not the subject's own prose, while novels still imply sole authorship.",
   [("Ghostwriting is never truly deceptive, since readers of every kind of book understand that named authors routinely depend on hidden professional writers for help.",
     "The last sentence says that where readers expect sole authorship, 'as with a novel or a scholarly article', concealed ghostwriting 'remains a real deception'."),
    ("A memoir written by someone other than its named author deceives its readers, who believe that they are reading the subject's own words throughout the book.",
     "This is the critics' charge from the first sentence, which the paragraph says 'assumes a convention that many readers do not share'."),
    ("Readers of celebrity memoirs care only that the memories are broadly genuine, so a ghostwriter may freely invent minor details and whole scenes provided the subject approves the finished book.",
     "The paragraph says a memoir deceives 'when the content is invented', so invented details remain deceptive even with approval.")],
   "The paragraph rejects the blanket charge against ghostwriting by tying deception to readers' actual expectations. For memoirs readers expect genuine content and the subject's approval, so ghostwriting deceives only when those fail; for novels and scholarly articles sole authorship is expected, so concealed ghostwriting does deceive. The correct summary keeps the principle and both sides of its application.",
   "Choosing the blanket defence of ghostwriting and missing the final sentence's limit, or the approval option and missing that invented content still deceives.",
   "V02I-ghostwriting-deception", "Two distractors take the author's side but each breaks one stated limit; separating them needs close reading of the last two sentences.",
   exams=HARD)

# 015 ---------------------------------------------------------------- conductor
ps("V02-I-015", AL, "A conductor's beat solves a timing problem in large orchestras, but the main work is done in rehearsal.", "Medium",
   "Audiences sometimes wonder what a conductor does, since the players have the notes in front of them and could, it seems, keep together by listening to one another. In a small ensemble they often do. But in an orchestra of eighty or more, spread across a wide stage, sound takes a noticeable time to travel, and players at the back may hear their colleagues at the front slightly late; following the ear alone would make the orchestra drag. The conductor's beat gives everyone a visual signal that arrives at once. Most of the conductor's work, however, happens earlier, in rehearsal, where decisions about balance, tempo and phrasing are made and agreed, so that the gestures in performance mainly remind players of what has already been settled.",
   "A large orchestra needs a visible beat since sound reaches distant players late, but a conductor's main work is settling interpretation in rehearsal.",
   [("In a large orchestra, players at the back of a wide stage hear their colleagues at the front slightly late, because sound takes a noticeable time to travel.",
     "This is the mechanism in the third sentence only; it leaves out the role of the beat and the paragraph's point that most of the work happens in rehearsal."),
    ("Every musical ensemble, however small, needs a conductor to lead it, because players cannot keep together simply by listening to one another while performing.",
     "The paragraph says that in a small ensemble players 'often do' keep together by listening, so this contradicts it."),
    ("The conductor's most important contribution is made during the performance itself, when gestures decide the balance, tempo and phrasing that the audience hears.",
     "The paragraph says these decisions are 'made and agreed' in rehearsal and that gestures in performance 'mainly remind players' of them, so this reverses it.")],
   "The paragraph explains why large orchestras need a conductor's beat (sound reaches distant players late, so following the ear makes the orchestra drag) and then adds, with 'however', that most of the conductor's work happens in rehearsal. The correct summary keeps both parts.",
   "Choosing the acoustic detail and missing the 'however' sentence that shifts the emphasis to rehearsal.",
   "V02I-orchestra-conductor-role", "Two-part explanation with a turn; the narrow option is an accurate detail.",
   cognitive="Understanding")

# 016 ---------------------------------------------------------------- abstract art titles
ps("V02-I-016", AL, "Untitled and evocative titles for abstract works each have a benefit and a cost; neither is simply correct.", "Medium",
   "Two habits divide painters of abstract pictures. Some call their works 'Untitled' or give them only numbers, on the ground that a title would tell viewers what to see and so narrow a picture meant to be met on its own terms. Others give evocative titles, a word or phrase that suggests a mood or a landscape. The first habit protects the viewer's freedom but can leave the uncertain viewer with nothing to hold on to; the second offers a way in but risks fixing one reading so firmly that others become hard to notice. Neither is simply correct, and the choice reveals less about the picture than about how much guidance the painter believes a viewer wants.",
   "Leaving abstract works untitled preserves viewers' freedom but may leave them lost, while evocative titles give entry but may fix a reading; neither choice is simply right.",
   [("Painters who give abstract works evocative titles help their viewers, whereas painters who leave works untitled leave their audience without any guidance at all.",
     "This takes one side, while the paragraph gives each habit a cost: evocative titles risk 'fixing one reading', and it says 'Neither is simply correct'."),
    ("The title that an abstract painter chooses reveals more about the meaning of the picture itself than any careful study of its colours and forms could do.",
     "The last sentence says the choice 'reveals less about the picture' than about the painter's view of viewers, so this reverses it."),
    ("Some painters of abstract pictures give their works only numbers, believing that any title would narrow what viewers are able to see in the work.",
     "This describes only the first habit and its rationale; it omits the comparison and the conclusion that neither habit is simply correct.")],
   "The paragraph compares two titling habits, gives each a benefit and a cost, and concludes that neither is simply correct. The correct summary keeps the balanced comparison.",
   "Choosing the one-sided option, which sounds sensible but ignores the cost the paragraph assigns to evocative titles.",
   "V02I-abstract-art-titles", "Balanced comparison; distractors are one-sided, reversed or narrow, with the one-sided option tempting.",
   cognitive="Understanding")

# 017 ---------------------------------------------------------------- audio guides
ps("V02-I-017", AL, "Longer visits by audio guide users support only a weak claim, because of self-selection and the gap between time and attention.", "Difficult",
   "Museums that track visitors often find that those using audio guides spend longer in the galleries than those without, and this is readily taken as proof that the guides deepen engagement. The figure deserves a second look. Visitors who choose to rent a guide may already be the more interested ones, so the longer visits might have occurred anyway. And time is an uncertain measure of attention: a visitor can stand before a painting for the full length of a recorded commentary while looking at the floor, listening rather than seeing. The finding is not worthless, since it shows at least that guided visitors are not hurrying through, but it supports a weaker claim than the one usually drawn from it.",
   "Guide users' longer visits show they are not hurrying but support less than deeper engagement, since self-selection and the gap between time and attention weaken that inference.",
   [("Audio guides reduce visitors' engagement with art, because those who listen attend to recorded commentary rather than looking at the paintings in front of them.",
     "The paragraph says only that a visitor 'can' listen rather than look, as a reason time is an uncertain measure; it does not conclude that guides reduce engagement."),
    ("Because visitors with audio guides spend longer in the galleries, museums can be confident that the guides deepen their engagement with the works on display.",
     "This is the inference the paragraph says 'deserves a second look' and finally calls stronger than the finding supports."),
    ("The longer visits of audio guide users reveal nothing at all about their experience, since the visitors who rent guides were already far more interested in art before they arrived.",
     "The paragraph says 'The finding is not worthless' and that guide users 'may' already be more interested; this denies all value and turns a possibility into a fact.")],
   "The paragraph presents a finding, notes the inference usually drawn, and gives two reasons to doubt it: self-selection of interested visitors and time being an uncertain measure of attention. It then qualifies its own doubt: the finding shows guided visitors are not hurrying, but supports only a weaker claim. The correct summary keeps the finding, both doubts and the limited conclusion.",
   "Swinging from the overclaim to the opposite extreme, calling the finding worthless or the guides harmful.",
   "V02I-museum-audio-guides", "Three distractors are near positions (overclaim, worthless, harmful); only the key keeps 'not worthless' with 'weaker claim'.",
   exams=HARD)

# 018 ---------------------------------------------------------------- weather probabilities
ps("V02-I-018", LM, "Probability forecasts confuse listeners who are not told what the percentage is out of.", "Medium",
   "When a forecast announces a seventy per cent chance of rain, many listeners are unsure what has been promised. Some suppose it will rain over seventy per cent of the area, others that it will rain for seventy per cent of the day. The intended meaning is different: on days when conditions resemble today's, rain falls at the given place on about seven days in ten. The confusion arises because the number answers a question listeners did not know had been asked, namely 'out of what?', and forecasters seldom say. A forecast can be perfectly accurate in its own terms and still mislead an audience that supplies the wrong reference class.",
   "Rain probabilities mislead because listeners, never told what the figure is out of, supply their own basis such as area or duration, even when forecasts are accurate.",
   [("Forecasts that announce a percentage chance of rain are frequently inaccurate, which is why so many listeners have learned not to trust what they are promised.",
     "The paragraph says a forecast 'can be perfectly accurate in its own terms and still mislead'; the problem is interpretation, not inaccuracy."),
    ("A seventy per cent chance of rain means that, on days resembling today, rain falls at the given place on about seven days out of every ten.",
     "This gives only the correct meaning from the third sentence and omits the paragraph's point about why listeners misread it."),
    ("Forecasters should abandon numerical probabilities altogether and return to plain verbal descriptions of the weather, which all listeners can understand without any confusion.",
     "The paragraph notes that forecasters 'seldom say' what the number refers to but recommends nothing, least of all giving up numbers.")],
   "The paragraph explains a confusion: listeners read a rain probability as a share of area or time, while it means a frequency over similar days, and they err because they are not told what the number is 'out of'. Its last sentence stresses that accuracy and clarity differ. The correct summary keeps the cause of the confusion and the point about accuracy.",
   "Selecting the correct definition of the forecast, which is true but is not the paragraph's point.",
   "V02I-weather-forecast-probability", "The narrow option is an exact and correct detail; the key must be preferred for the explanation of the confusion.",
   cognitive="Understanding")

# 019 ---------------------------------------------------------------- sports commentary
ps("V02-I-019", LM, "Radio and television commentary differ because each responds to what its audience can already see.", "Easy",
   "Radio and television commentary on the same match sound strikingly different. The radio commentator must describe almost everything: where the ball is, who has it, which way the play is moving, because the listener has no other way of knowing. The television commentator, whose audience can see all this, would be tiresome doing the same, and so speaks less, leaving silences and using words to add what the picture cannot show, such as a player's record, a tactical change or the significance of the moment. Each style is a response to what its audience already possesses.",
   "Radio commentators describe play constantly since listeners cannot see it, while television commentators say less and add what the picture lacks; each suits its audience.",
   [("Radio commentary is more skilful than television commentary, since describing every movement of play demands far greater talent than adding a few occasional remarks.",
     "The paragraph explains the difference by the audience and makes no judgement about which style needs more skill."),
    ("Television commentators often use their words to add information such as a player's record, a tactical change or the significance of the moment.",
     "This covers only the television half; it leaves out the contrast with radio and the explanation that each style responds to its audience."),
    ("Television commentators speak less than radio commentators mainly because broadcasters wish to reduce their costs by shortening the spoken commentary on all televised matches.",
     "The paragraph gives a different reason: the audience 'can see all this', so describing it would be 'tiresome'. Cost is never mentioned.")],
   "The paragraph contrasts the two styles and explains both by the same principle: 'Each style is a response to what its audience already possesses.' The correct summary keeps the contrast and the principle.",
   "Choosing the television detail, which is accurate but covers only half the comparison.",
   "V02I-live-sports-commentary", "The principle is stated in the last sentence and the distractors are clearly narrow or out of scope.",
   cognitive="Understanding")

# 020 ---------------------------------------------------------------- corporate jargon
ps("V02-I-020", LM, "Corporate jargon is evasive rather than empty, which makes it worse than critics allow.", "Difficult",
   "Corporate jargon is usually mocked as empty: phrases about 'leveraging synergies' and 'circling back' are taken to show that those who use them have nothing to say. The mockery misses what the vocabulary does. Much of it serves to soften or blur, so that a decision to close a department can be announced as a 'realignment' without anyone having to state plainly that people will lose their jobs. Such language is not empty but evasive, and evasion has uses for the speaker. This makes it more troubling than the critics allow, not less: an empty phrase merely wastes time, whereas an evasive one shifts the burden of understanding onto listeners, who must work out for themselves what is being done to them.",
   "Corporate jargon is less empty than evasive, sparing speakers from stating unwelcome facts, which makes it worse than its mockers think, since listeners must decode it.",
   [("Corporate jargon shows that the managers who rely on phrases such as 'circling back' usually have nothing of real substance to say to their staff.",
     "This is the mockery the paragraph reports and says 'misses what the vocabulary does'; the author holds the language does a great deal."),
    ("Critics who mock corporate jargon overstate its harm, since phrases that merely blur unwelcome news serve useful purposes and waste very little of anyone's working time.",
     "The paragraph says evasive jargon is 'more troubling than the critics allow, not less'; the uses it mentions are uses 'for the speaker', not a defence."),
    ("Firms often announce the closure of a department as a 'realignment', so that nobody has to state plainly that people will lose their jobs.",
     "This is the illustrating example only; it leaves out the general claim that jargon is evasive and the conclusion about why that is worse than emptiness.")],
   "The paragraph rejects the view that jargon is empty, argues it is evasive and useful to the speaker, and concludes this makes it 'more troubling than the critics allow, not less', because it shifts the burden of understanding to listeners. The correct summary keeps the reclassification and the conclusion about degree.",
   "Reading the rejection of the critics as a defence of jargon, when the author thinks the critics understate the problem.",
   "V02I-corporate-jargon-evasion", "The author disagrees with the critics but in the direction of greater, not lesser, concern; one distractor exploits that.",
   exams=HARD)

# 021 ---------------------------------------------------------------- obituaries
ps("V02-I-021", LM, "Obituary discretion is defensible for private failings but not for the public harms of the powerful.", "Medium",
   "Newspaper obituaries have long followed a convention of discretion: the dead are praised for their achievements, while their failings are passed over or hinted at in phrases that knowing readers decode. The convention is defended as kindness to grieving families, and kindness is a real consideration. But an obituary is also the first draft of a public record, often consulted later by people who never knew the subject. When it omits the serious harm a powerful person did, it does not merely spare feelings; it misinforms everyone who relies on it afterwards. Discretion is defensible for private failings that harmed no one beyond the household, far less so for public conduct that harmed many.",
   "Since obituaries become a public record, discretion that hides the serious public harms of the powerful misinforms later readers, though private failings may be spared.",
   [("Obituaries should record every failing of the person who has died, since any omission at all betrays the readers who rely on the newspaper for accurate information.",
     "The last sentence says discretion 'is defensible for private failings that harmed no one beyond the household', so 'every failing' contradicts it."),
    ("Obituaries rightly pass over the failings of the dead in silence, because kindness to grieving families matters more than the completeness of any public record.",
     "The paragraph grants that kindness is 'a real consideration' but argues that for public harms omission 'misinforms everyone', so this reverses its conclusion."),
    ("Obituaries often hint at the failings of the dead in coded phrases that knowing readers can decode, while openly praising their achievements and careers.",
     "This describes the convention in the first sentence only; it omits the argument about the public record and where discretion stops being defensible.")],
   "The paragraph describes the convention of discretion, concedes its justification in kindness, and argues that because obituaries form a public record, omitting serious public harms by powerful people misinforms later readers. It ends by drawing the line between private failings and public conduct. The correct summary keeps the reason and the line.",
   "Choosing the extreme option that every failing must be reported, which ignores the private failings exception.",
   "V02I-obituary-discretion", "Distractors take each extreme of a position that draws a line, plus a narrow description.",
   cognitive="Understanding")

# 022 ---------------------------------------------------------------- praising effort
ps("V02-I-022", ED, "Effort praise helps only when it links what a child did to the result, not when used as a formula.", "Difficult",
   "Teachers are now widely advised to praise children for effort rather than for cleverness, on the reasoning that a child told she is clever may avoid hard tasks for fear of disproving it, while one praised for trying learns that ability grows with work. The advice has something in it, but it is easily turned into a formula. Praise for effort that is given regardless of outcome can teach a child that trying is what counts even when the method is hopeless, and children are quick to notice when 'good effort' is offered as consolation for failure. What seems to matter is less the word used than whether praise connects what the child did to what resulted, so that the child learns which kinds of effort work.",
   "Praising effort has merit, but as a formula it can reward hopeless methods or sound like consolation; praise works best when it ties children's actions to results.",
   [("Children praised for cleverness avoid hard tasks, so teachers should always praise effort rather than intelligence, whatever the result of the child's work.",
     "The paragraph reports this reasoning and grants it 'something', but warns precisely against effort praise 'given regardless of outcome'."),
    ("Praising children for effort is generally harmful, because they soon recognise it as consolation for failure and then stop trying hard at difficult tasks.",
     "The paragraph says the advice 'has something in it' and that formulaic praise 'can' mislead; it neither calls effort praise harmful in general nor says children stop trying."),
    ("The precise words that teachers choose when praising children matter more than anything else, so 'good effort' should be replaced by more specific phrases.",
     "The last sentence says what matters is 'less the word used than whether praise connects what the child did to what resulted', so this inverts the priority.")],
   "The paragraph reports the advice to praise effort and its rationale, grants it merit, then warns that as a formula it can mislead children and be read as consolation. It concludes that what matters is whether praise connects action to result. The correct summary keeps the concession, the warning and the alternative principle.",
   "Choosing the option about precise wording, which sounds like a refinement but reverses the final sentence's 'less the word used'.",
   "V02I-praising-effort", "Every distractor uses the paragraph's terms; separating them needs the concession and the exact contrast in the last sentence.",
   exams=HARD)

# 023 ---------------------------------------------------------------- peer tutoring
ps("V02-I-023", ED, "Peer tutoring benefits tutors when, and only when, it requires them to explain.", "Medium",
   "Schools that pair older pupils with younger ones for tutoring usually set out to help the younger children, and they often do. A recurring observation, however, is that the tutors gain as much or more: having to explain an idea to someone who does not yet grasp it forces the tutor to organise what he or she half knows, to notice gaps and to find examples. This benefit is not automatic. A tutor who merely supplies answers, or who is given material far below his or her own level with no need to explain it, gains little. The gain comes from the effort of explanation, and schools that want it must design tutoring so that explanation is actually required.",
   "Peer tutoring can help tutors as much as tutees, but only when tutors must truly explain, so schools should design it to require explanation.",
   [("Older pupils who tutor younger children are made to organise what they half know, to notice gaps in their understanding and to search for suitable examples.",
     "This lists the benefits in the second sentence but drops the paragraph's qualification, 'This benefit is not automatic', and its conclusion about design."),
    ("Peer tutoring always benefits the older tutors more than the younger pupils, whatever material they are given or whatever method they follow in the sessions.",
     "The paragraph says tutors gain 'as much or more' and that a tutor who merely supplies answers 'gains little', so 'always' and 'whatever' contradict it."),
    ("Peer tutoring helps younger children only when their older tutors are given material well above their own level, which forces the tutors to work harder.",
     "The paragraph speaks of material 'far below' the tutor's level as a problem when no explanation is needed; it never requires material above their level or ties the tutees' gain to it.")],
   "The paragraph reports a finding (tutors gain at least as much as tutees), explains it by the work of explanation, and qualifies it: the benefit is not automatic and disappears when no explanation is required. It concludes that tutoring must be designed to require explanation. The correct summary keeps the finding, its condition and the conclusion.",
   "Choosing the list of benefits, which is accurate but omits the condition on which they depend.",
   "V02I-peer-tutoring-tutors", "A finding with a qualification; the narrow option reads as a fair summary until the qualification is noticed.",
   cognitive="Understanding")

# 024 ---------------------------------------------------------------- multiple-choice tests
ps("V02-I-024", ED, "Multiple-choice tests can test demanding reasoning; their weakness lies in poor writing, not the format.", "Easy",
   "Multiple-choice tests are commonly dismissed as measuring only recognition: the answer is on the page, the critics say, so the student need only spot it. This is true of badly written questions, whose wrong options are obviously absurd. A well-made question is different. If its wrong options reflect the mistakes that students actually make, choosing correctly requires the student to tell a sound piece of reasoning from several plausible but flawed ones, which is itself a demanding skill. The weakness of many such tests lies in the craft of writing them, not in the format.",
   "Multiple-choice tests need not measure mere recognition; with options built on real mistakes they test demanding judgement, so weak tests reflect poor writing, not the format.",
   [("Multiple-choice tests can measure only the recognition of answers, because the correct answer is always printed somewhere on the page right in front of the student taking the test.",
     "This is the critics' view in the first sentence, which the paragraph accepts only for 'badly written questions' and rejects for well-made ones."),
    ("Multiple-choice tests are the most demanding form of assessment available, since every question requires students to weigh several flawed lines of reasoning.",
     "The paragraph grants that badly written questions are easy and never ranks the format above others, so 'most demanding' and 'every question' overstate it."),
    ("Badly written multiple-choice questions often contain wrong options so obviously absurd that students can reject them without giving the matter much thought.",
     "This restates the concession in the second sentence; it omits the paragraph's main claim about well-made questions and where the weakness lies.")],
   "The paragraph critiques the view that multiple-choice tests measure only recognition, concedes it for badly written questions, and argues that well-made questions test the demanding skill of telling sound reasoning from plausible errors. It concludes that the weakness lies in the writing, not the format. The correct summary keeps the rejection, the concession and the conclusion.",
   "Choosing the option that restates the concession about badly written questions.",
   "V02I-multiple-choice-tests", "The critique and conclusion are explicit in the first and last sentences.",
   cognitive="Understanding")

# 025 ---------------------------------------------------------------- field trips
ps("V02-I-025", ED, "School trips are real learning, anchoring later lessons and reaching pupils who would otherwise miss such experiences.", "Easy",
   "School trips to museums, factories and nature reserves are often the first thing cut when budgets tighten, on the ground that they are enjoyable outings rather than real learning. That judgement undervalues what a visit can do. A child who has stood in a working mill or watched a river carry silt remembers it vividly, and the memory gives later lessons something concrete to attach to; an abstract idea in a textbook becomes an explanation of something the child has seen. For pupils whose families cannot afford such visits themselves, the school trip may be the only chance of these experiences.",
   "School trips are wrongly cut as mere outings, since vivid visits anchor later lessons and may be poorer pupils' only chance of such experiences.",
   [("Field trips teach children far more than classroom lessons do, so schools should spend a larger share of their budgets on visits than on textbooks.",
     "The paragraph says trips give lessons 'something concrete to attach to'; it does not rank trips above lessons or propose shifting budgets from textbooks."),
    ("Children who visit a working mill or watch a river carrying silt are likely to remember the experience vividly for a long time after the visit.",
     "This is the example in the third sentence; it omits the argument against cutting trips and the point about pupils who cannot otherwise go."),
    ("School trips are enjoyable outings rather than real learning, so they are sensibly the first expense to be cut when a school's budget becomes tight.",
     "This is the judgement the paragraph says 'undervalues what a visit can do', so it reverses the author's view.")],
   "The paragraph rejects the view that school trips are mere outings to be cut first. It gives two reasons: vivid memories anchor later lessons, and for some pupils the trip may be the only such chance. The correct summary keeps the rejection and both reasons.",
   "Picking the prescription about budgets, which goes further than the paragraph.",
   "V02I-school-field-trips", "The stance and both reasons are explicit; distractors are clearly reversed, narrow or extreme.",
   cognitive="Understanding")
