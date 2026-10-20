import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D2 = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ooo("V03-F-001", "Psychology", "The first figure in a negotiation pulls the outcome towards it, within limits.", "Easy",
    ["In a negotiation, the first number placed on the table tends to pull the final agreement towards it, even when both sides know the figure is arbitrary.",
     "This is why experienced negotiators often prefer to make the opening offer themselves rather than wait for the other party to do so.",
     "An ambitious but defensible opening shifts the whole range within which the rest of the bargaining takes place.",
     "The advantage disappears, however, if the opening figure is so extreme that the other side walks away instead of adjusting."],
    "In many cultures, haggling in a market is treated as a social ritual as much as an economic exchange.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] make one argument about the pull of the opening figure: [[1]] states the effect, [[2]] draws the practical lesson ('This is why'), [[3]] explains how a strong opening works, and [[4]] sets its limit ('however'). Sentence [[X]] is about bargaining too, but it concerns the cultural meaning of haggling, not the influence of the first number, and nothing in the paragraph refers to it.",
    "Choosing sentence [[4]] because it seems to turn against the argument, when it is the qualification that completes it.",
    "V03F-anchoring-in-negotiation", "The odd sentence shifts from the effect of an opening offer to the culture of haggling, which is visible on a first reading.",
    traps=[(4, "Sentence [[4]] opens with 'however' and limits the advantage, but it qualifies the claim in sentence [[3]] about an ambitious opening and so belongs to the same argument.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 002
ooo("V03-F-002", "Psychology", "The idea that judgement is used up by the day's decisions, the routines it inspires, and its uncertain support.", "Medium",
    ["A popular idea holds that the capacity to make careful choices is gradually used up over the course of a day, so that later decisions are made more carelessly.",
     "On this view, a person who has spent the morning weighing many small options will, by evening, drift towards whatever is easiest or most familiar.",
     "Some people respond by stripping trivial choices out of their routines, wearing similar clothes or eating the same breakfast, to save their judgement for what matters.",
     "Whether such economies actually help depends on whether the underlying idea is sound, and laboratory attempts to confirm it have produced mixed results."],
    "Choosing among a large number of options can also leave people less satisfied with what they finally pick, because the rejected alternatives linger in the mind.",
    "The paragraph is about one idea: that judgement is depleted as decisions accumulate. Sentence [[1]] states it, [[2]] spells it out ('On this view'), [[3]] describes the routines people adopt to conserve judgement, and [[4]] asks whether 'such economies' work, given the mixed evidence. Sentence [[X]] uses the same vocabulary of choices and options, but it describes a different effect, dissatisfaction caused by many alternatives at one moment, rather than depletion across a day, and no other sentence takes it up.",
    "Treating sentence [[X]] as part of the argument because it also concerns the costs of choosing, without noticing that it describes a different mechanism.",
    "V03F-decision-fatigue", "The odd sentence shares the vocabulary of choice and must be rejected because it describes a different effect, not because of its topic.",
    traps=[(4, "Sentence [[4]] can look like a change of subject towards research, but 'such economies' refers back to the routines in sentence [[3]] and it tests the idea stated in sentence [[1]].")])

# ------------------------------------------------------------------ 003
ooo("V03-F-003", "Psychology", "Nostalgia, once treated as an illness, is now seen as a resource that steadies people during change.", "Medium",
    ["For a long time nostalgia was treated as a disorder, a homesickness so severe that it was thought capable of making soldiers and emigrants ill.",
     "More recent work tends to describe it instead as a resource, something people reach for when the present feels unsettled.",
     "Recalling a cherished past, on this account, reminds a person that their life has a continuous thread and that they have been valued by others.",
     "That would explain why nostalgic reverie seems to become more frequent during periods of transition, such as moving to a new city or starting a new job."],
    "Advertisers have learned to exploit the feeling, using the music of a buyer's youth to make an old product seem fresh again.",
    "The four coherent sentences trace a change in how nostalgia is understood: from a disorder ([[1]]) to a resource ([[2]], 'instead'), with the mechanism ([[3]], 'on this account') and the pattern it explains ([[4]], 'That would explain'). Sentence [[X]] mentions the same feeling but is about its commercial use, which plays no part in the account of what nostalgia does for the person who feels it.",
    "Picking sentence [[1]] because it belongs to an earlier period, when the paragraph needs it as the view that sentence [[2]] replaces.",
    "V03F-nostalgia-and-comfort", "The odd sentence is on the same subject; it is rejected because it concerns marketing rather than the function of the feeling.",
    traps=[(1, "Sentence [[1]] describes an old view, but sentence [[2]] says 'instead', so the newer account depends on it as a contrast.")])

# ------------------------------------------------------------------ 004
ooo("V03-F-004", "Psychology", "The cost of switching tasks lies mainly in the unfinished task that keeps a hold on attention.", "Difficult",
    ["When people move from one task to another, part of their attention tends to remain with the task they have just left, especially if it was left unfinished.",
     "This lingering preoccupation, sometimes called attention residue, means that the new task receives less than the full mind it appears to be getting.",
     "The cost, on this account, lies less in the act of switching than in the incompleteness of what was abandoned, since a finished task releases its hold far more readily.",
     "It follows that a brief note recording where one stopped and what remains to be done may reduce the residue, by persuading the mind that the loose end has been secured."],
    "Frequent switching also trains people to crave novelty, so that sustained work on a single task begins to feel intolerably slow.",
    "The paragraph locates the cost of switching in an unfinished task's hold on attention: [[1]] describes the effect, [[2]] names it, [[3]] states that the cost lies 'less in the act of switching than in the incompleteness' of the abandoned task, and [[4]] draws a remedy that works on incompleteness. Sentence [[X]] shares the vocabulary of switching and attention, but it blames the habit of switching itself, the very explanation sentence [[3]] plays down, and the remedy in [[4]] does nothing about a craving for novelty.",
    "Accepting sentence [[X]] as one more cost of switching, without seeing that the paragraph has deliberately moved the cost away from switching towards incompleteness.",
    "V03F-attention-residue", "The odd sentence sounds like a natural addition about costs of switching; rejecting it requires noticing that it runs against the paragraph's specific claim about where the cost lies.",
    traps=[(4, "Sentence [[4]] looks like practical advice tacked on, but 'It follows' ties it to sentence [[3]]: a note helps precisely because the cost lies in the loose end."),
           (3, "Sentence [[3]] may seem to repeat sentence [[2]], but it adds the central claim about where the cost lies, without which sentence [[4]] would not follow.")],
    exams=D2)

# ------------------------------------------------------------------ 005
ooo("V03-F-005", "Society and culture", "A queue's fairness depends on its visibility, which is why one shared line feels fairer.", "Medium",
    ["A queue is a remarkably efficient device for allocating something scarce without money, because it ranks claimants by a simple rule that everyone can observe.",
     "Its legitimacy rests on that visibility: people will accept a long wait more calmly than a short one in which others seem to jump ahead.",
     "This is why a single snaking line feeding several counters often feels fairer than separate lines, even when the average wait is exactly the same.",
     "With one line, nobody suffers the particular resentment of watching a neighbouring queue move faster through sheer luck."],
    "Selling priority access, as some theme parks now do, raises the question of whether time spent waiting should ever be for sale.",
    "The four linked sentences argue that a queue is accepted because its rule is visible: [[1]] introduces the rule 'that everyone can observe', [[2]] says legitimacy 'rests on that visibility', [[3]] applies this to single versus separate lines, and [[4]] explains why one line removes resentment. Sentence [[X]] is about queues as well, but it raises the ethics of paying to skip a wait, a question the paragraph never takes up.",
    "Picking sentence [[4]] because it seems to repeat sentence [[3]], when it supplies the reason a single line feels fairer.",
    "V03F-queues-and-fairness", "The odd sentence shares the subject of waiting and fairness and is excluded because it introduces a different question.",
    traps=[(4, "Sentence [[4]] begins 'With one line', picking up the single snaking line of sentence [[3]] and explaining why it feels fairer.")])

# ------------------------------------------------------------------ 006
ooo("V03-F-006", "Society and culture", "Museum labels shape what an object is taken to be, and no unlabelled encounter escapes that selectivity.", "Difficult",
    ["A museum label appears to be the most modest of texts, a few lines that merely identify what the visitor is already looking at.",
     "Yet by choosing what to mention, a maker's name, a date, a material, a former owner, the label quietly decides what kind of thing the object is taken to be.",
     "A bowl described by its glaze becomes a work of craft, while the same bowl described by the household that used it becomes evidence of a way of life.",
     "Removing labels altogether would not restore an innocent encounter, since visitors would then fill the silence with assumptions of their own that are no less selective."],
    "Some curators now invite communities connected to an object to check its label for factual errors, such as a wrong date or a misattributed maker.",
    "The paragraph argues that any description of an object is a selection that shapes how it is seen: [[1]] sets up the label's apparent modesty, [[2]] ('Yet') reveals its power to decide what the object is, [[3]] illustrates this with the bowl, and [[4]] closes off the escape of having no labels, since viewers' own assumptions are 'no less selective'. Sentence [[X]] uses the same vocabulary of labels, dates and makers, but it is about correcting factual mistakes. The paragraph's point is that a label shapes how an object is seen through what it chooses to mention even when every detail is accurate, so sentence [[X]] answers a problem the paragraph never poses.",
    "Reading sentence [[X]] as a natural remedy at the end, without seeing that the paragraph's concern is selection among true details, not errors in them.",
    "V03F-museum-object-labels", "The odd sentence reads like a fitting conclusion; rejecting it requires seeing that the paragraph is about selection among accurate details, not about mistakes.",
    traps=[(4, "Sentence [[4]] seems to shift to visitors, but it completes the argument by showing that even the absence of labels leaves the object framed by selective assumptions."),
           (1, "Sentence [[1]] looks like a mere opening, but sentence [[2]] begins 'Yet' against its claim that labels 'merely identify' the object.")],
    exams=D2)

# ------------------------------------------------------------------ 007
ooo("V03-F-007", "Society and culture", "Whatever its origin, a handshake conveys attitude through the way it is performed.", "Easy",
    ["The handshake is often explained as a gesture of peace, an open right hand showing that it holds no weapon.",
     "Whatever its origins, its meaning today depends heavily on how it is performed.",
     "A grip that is too limp may be read as indifference, while one that is too forceful can seem like an attempt at dominance.",
     "The gesture thus carries a surprising amount of information about attitude in the second or two that it lasts."],
    "In much of South Asia, a greeting with folded hands is customary and involves no touching at all.",
    "The four coherent sentences concern the handshake: its supposed origin ([[1]]), the claim that its present meaning depends on performance ([[2]], 'Whatever its origins'), examples of grips and their readings ([[3]]), and the conclusion ([[4]], 'thus'). Sentence [[X]] describes a different greeting altogether and connects to none of these steps.",
    "Choosing sentence [[1]] because it is about the past, though sentence [[2]] refers back to it with 'Whatever its origins'.",
    "V03F-handshake-greetings", "The odd sentence is about a different greeting, which is easy to spot once the focus on the handshake is noticed.",
    traps=[(1, "Sentence [[1]] is needed: 'Whatever its origins' in sentence [[2]] sets the present meaning against the explanation it gives.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 008
ooo("V03-F-008", "Society and culture", "The roadside tea stall works as an open public meeting place, doing the job planners expect of plazas.", "Medium",
    ["The roadside tea stall sells a product so cheap that the purchase is hardly the point of the visit.",
     "What a customer really buys for the price of a small glass is the right to stand around, to listen, and to join a conversation already in progress.",
     "Because no one needs credentials or a reservation to be there, drivers, clerks, students and labourers share its bench on roughly equal terms.",
     "In this sense the stall performs the work that planners often expect of expensive public plazas, many of which stand empty."],
    "Rising prices of milk and sugar have squeezed the margins of many stall owners, some of whom now sell snacks to stay afloat.",
    "The paragraph treats the tea stall as a social space: [[1]] says the purchase is not the point, [[2]] says what is really bought is the right to linger and talk, [[3]] adds that anyone may join on equal terms, and [[4]] concludes ('In this sense') that the stall does the work of a public plaza. Sentence [[X]] is about tea stalls too, but it turns to the owner's finances, which have no bearing on the stall's role as a meeting place.",
    "Linking sentence [[X]] to sentence [[1]] because both mention price, although sentence [[1]] uses cheapness only to show that the purchase is not the point.",
    "V03F-tea-stalls-as-meeting-places", "The odd sentence shares the subject and the theme of price; it must be rejected because it concerns the owner's business rather than the stall's social function.",
    traps=[(4, "Sentence [[4]] may seem to change the subject to planning, but 'In this sense' draws the conclusion from sentences [[2]] and [[3]].")])

# ------------------------------------------------------------------ 009
ooo("V03-F-009", "Economics and business", "The lighthouse example shows that whether a good can be sold depends on surrounding institutions.", "Difficult",
    ["The lighthouse has long served economists as the classic example of a good that markets cannot supply, since its light guides every passing ship whether or not the owner has been paid.",
     "Historians have pointed out, however, that some lighthouses were in fact built privately and financed by dues collected from ships when they docked at nearby ports.",
     "The lesson is not that the textbook was simply wrong but that its example hid a condition: provision became possible wherever there was a point at which users could be charged.",
     "Whether a good can be sold therefore depends less on its physical nature than on the institutions that happen to surround it."],
    "The same reasoning explains why national defence is usually paid for out of general taxation rather than sold to individual households.",
    "The paragraph takes the lighthouse, the textbook case of a good markets cannot supply ([[1]]), shows that some were financed privately ([[2]], 'however'), draws the lesson that provision depended on a point where users could be charged ([[3]]), and generalises ([[4]], 'therefore'). Sentence [[X]] extends the textbook reasoning of sentence [[1]] to defence, but the paragraph exists to qualify that reasoning, and nothing after it returns to defence or explains how the lesson applies to it. It shares the economic vocabulary but does no work in the argument.",
    "Accepting sentence [[X]] as a natural second example after sentence [[1]], without noticing that the rest of the paragraph questions the very reasoning it extends.",
    "V03F-lighthouse-provision", "The odd sentence fits smoothly after the opening and uses its logic; rejecting it requires following the whole argument, which undercuts that logic.",
    traps=[(3, "Sentence [[3]] may look like a hedge that could be dropped, but it supplies the condition, a point at which users can be charged, on which the conclusion in sentence [[4]] rests."),
           (2, "Sentence [[2]] seems like a historical aside, but its 'however' is the turn that the lesson in sentence [[3]] interprets.")],
    exams=D2)

# ------------------------------------------------------------------ 010
ooo("V03-F-010", "History and politics", "Early modern coffeehouses as a training ground for public opinion, and the limits of that picture.", "Medium",
    ["In the coffeehouses of seventeenth and eighteenth century Europe, the price of a cup bought a seat among strangers and access to whatever newspapers lay on the tables.",
     "Because rank counted for less there than in the drawing room, a merchant could argue with a gentleman about a pamphlet that both had just read.",
     "Some historians therefore see these rooms as an early training ground for public opinion, a place where private people learned to reason together about public affairs.",
     "Others warn that the picture is idealised, since the conversation was largely closed to women and its tone was often more partisan than rational."],
    "Coffee itself reached Europe through trade with the Ottoman lands, and its cultivation later spread to colonies in Asia and the Americas.",
    "The four connected sentences concern the coffeehouse as a setting for public debate: [[1]] describes what entry bought, [[2]] notes that rank mattered less there, [[3]] reports the view drawn 'therefore' that the rooms trained public opinion, and [[4]] reports the objection to that view ('Others warn'). Sentence [[X]] is about coffee, but it traces the trade and cultivation of the drink, which has nothing to do with the argument about conversation and opinion.",
    "Choosing sentence [[4]] because it disagrees with sentence [[3]], when 'Others' answers 'Some historians' and the paragraph is built on that exchange.",
    "V03F-coffeehouses-and-public-debate", "The odd sentence shares the subject of coffee and its history and is rejected because it concerns the commodity rather than the social setting.",
    traps=[(4, "Sentence [[4]] belongs because 'Others warn' responds to 'Some historians' in sentence [[3]], completing a comparison of two views.")])

# ------------------------------------------------------------------ 011
ooo("V03-F-011", "History and politics", "The jury is better defended by the authority of its verdicts than by its accuracy, an authority that depends on representativeness.", "Difficult",
    ["Critics of the jury often ask whether twelve untrained citizens decide cases as accurately as a professional judge would.",
     "The question is fair, but it assumes that accuracy is the only thing a trial is meant to produce.",
     "A verdict also has to be accepted, and a judgement delivered by ordinary people drawn from the community carries an authority that no official's ruling can fully borrow.",
     "That authority, however, is only as strong as the jury's claim to represent the community, which is why the methods used to select jurors matter so much."],
    "Jurors may also be more sceptical of police testimony than a judge who hears such evidence week after week.",
    "The paragraph moves the defence of the jury away from accuracy: [[1]] states the critics' question, [[2]] grants it but says it assumes accuracy is all a trial produces, [[3]] names the other product, acceptance and authority, and [[4]] qualifies that authority by tying it to representativeness. Sentence [[X]] is on the jury too, but it returns to the accuracy contest, suggesting jurors may weigh evidence better, which is exactly the ground sentence [[2]] says is too narrow. Its 'also' has nothing to attach to, since no earlier sentence lists an advantage of jurors in weighing evidence.",
    "Taking sentence [[X]] as support for the jury and therefore as part of a pro-jury paragraph, without seeing that the paragraph defends the jury on a different ground.",
    "V03F-jury-trials-by-peers", "The odd sentence supports the same institution and fits after the critics' question; it is rejected only by tracking which ground the defence is built on.",
    traps=[(4, "Sentence [[4]] may look like a concession that breaks the defence, but 'That authority' refers to sentence [[3]] and qualifies it, which the paragraph needs."),
           (2, "Sentence [[2]] is the hinge: it grants the critics' question and redirects it, and sentence [[3]] depends on its point that accuracy is not the only aim.")],
    exams=D2)

# ------------------------------------------------------------------ 012
ooo("V03-F-012", "History and politics", "Canals cut transport costs and helped British industry expand before the railways.", "Easy",
    ["In the late eighteenth century, Britain went through a burst of canal building that linked mines, mills and ports across much of the country.",
     "A single horse could pull a loaded barge carrying many times what it could haul in a cart on the rough roads of the day.",
     "Cheaper carriage of coal and raw materials helped factories to grow far from the places where those materials were found.",
     "In this way the canals lowered the cost of industrial expansion well before the railways arrived to compete with them."],
    "Today many old canals are popular with walkers, cyclists and people who live on narrowboats.",
    "The four coherent sentences explain the economic role of the canal age: [[1]] introduces the building boom, [[2]] gives the reason canals were efficient, [[3]] states the effect on industry, and [[4]] sums up ('In this way'). Sentence [[X]] is about canals but describes their present-day leisure use, a different time and a different subject from their role in industrial growth.",
    "Choosing sentence [[2]] because it is about horses rather than industry, though it explains why canal carriage was cheaper.",
    "V03F-canal-building-age", "The odd sentence jumps to the present and to leisure, which is easy to notice.",
    traps=[(2, "Sentence [[2]] is the reason behind the 'Cheaper carriage' of sentence [[3]], so it is part of the causal chain.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 013
ooo("V03-F-013", "Economics and business", "Stock options can push managers towards more risk than owners would want.", "Medium",
    ["Stock options are meant to align the interests of managers with those of shareholders by letting managers profit when the share price rises.",
     "An option, however, rewards a rise in price without imposing any matching loss when the price falls below the agreed level.",
     "A manager holding many options therefore has reason to favour risky strategies, since the gains from success are large while the cost of failure falls mainly on others.",
     "The device intended to make managers think like owners can thus make them bolder than owners would wish."],
    "Young companies often offer options to attract staff when they cannot yet afford to pay competitive salaries.",
    "The paragraph argues that options can distort risk-taking: [[1]] states their purpose, [[2]] ('however') points out the missing downside, [[3]] draws the consequence ('therefore') for risky strategies, and [[4]] concludes ('thus') that options can make managers bolder than owners would like. Sentence [[X]] is about options as well, but it concerns their use in recruitment, which has no place in the argument about incentives and risk.",
    "Accepting sentence [[X]] because it mentions a genuine purpose of options, just as sentence [[1]] does, without checking whether the argument uses it.",
    "V03F-employee-stock-options", "The odd sentence shares the subject and describes a real use of options; it is rejected because it does not bear on the incentive argument.",
    traps=[(1, "Sentence [[1]] is needed, since sentence [[4]] ('intended to make managers think like owners') returns to the purpose it states.")])

# ------------------------------------------------------------------ 014
ooo("V03-F-014", "Economics and business", "Subscription pricing turns a sale into a relationship, making customer retention central.", "Easy",
    ["Subscription pricing turns a single sale into a continuing relationship with the customer.",
     "For the seller, this brings a steady and predictable stream of revenue that makes planning easier.",
     "It also shifts the seller's attention towards keeping existing customers rather than constantly finding new ones.",
     "A business that loses subscribers quickly may therefore struggle even if it attracts many new sign-ups each month."],
    "Some newspapers in earlier centuries were sent by post to subscribers living far from the city where they were printed.",
    "The four coherent sentences explain what subscription pricing means for a seller today: it creates a relationship ([[1]]), brings steady revenue ([[2]]), makes retention the priority ([[3]], 'also'), and so makes losing subscribers costly ([[4]], 'therefore'). Sentence [[X]] uses the word subscribers but describes the historical delivery of newspapers, which says nothing about the business logic of the model.",
    "Choosing sentence [[4]] because it describes a business in trouble, though it follows directly from the point about retention in sentence [[3]].",
    "V03F-subscription-pricing", "The odd sentence is from a different period and concerns delivery, so it stands out once the paragraph's focus is clear.",
    traps=[(4, "Sentence [[4]] belongs: 'therefore' draws the consequence of sentence [[3]], that retention matters more than new sign-ups.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 015
ooo("V03-F-015", "Technology", "Network effects work within users' own circles, so a dominant platform is less secure than its size suggests.", "Difficult",
    ["A platform with network effects becomes more valuable to each user as more people join it, which is why such markets often tilt towards a single dominant firm.",
     "The usual inference is that the leader's position, once won, is almost impossible to challenge.",
     "Yet what matters to a user is rarely the total number of members but whether the particular people they want to reach are present.",
     "A newcomer that wins over one tightly knit group at a time can therefore erode a giant whose vast membership is, from any single user's point of view, largely irrelevant."],
    "Dominant platforms can also buy promising rivals early, before those rivals grow large enough to pose a threat.",
    "The paragraph questions the belief that network effects make a leader unassailable: [[1]] explains the tilt towards one firm, [[2]] states 'the usual inference', [[3]] ('Yet') argues that users care about their own contacts rather than total size, and [[4]] ('therefore') concludes that a newcomer can win group by group. Sentence [[X]] shares the subject of dominant platforms and rivals, but it offers a separate mechanism of entrenchment, acquisition, which the argument neither uses nor answers: sentence [[3]] rebuts reasoning from size, not buying out rivals, and if sentence [[X]] were kept, the conclusion in [[4]] would be left facing an objection it never meets.",
    "Placing sentence [[X]] after sentence [[2]] as extra support for the usual inference, without seeing that the 'Yet' of sentence [[3]] answers only the reasoning from network size.",
    "V03F-network-effects-in-platforms", "The odd sentence fits smoothly after the 'usual inference'; it is rejected only by checking what the rebuttal actually answers.",
    traps=[(2, "Sentence [[2]] states the inference that sentences [[3]] and [[4]] go on to challenge, so the argument has nothing to rebut without it."),
           (4, "Sentence [[4]] belongs because 'therefore' applies the point in sentence [[3]] about particular contacts to how a newcomer can compete.")],
    exams=D2)

# ------------------------------------------------------------------ 016
ooo("V03-F-016", "Economics and business", "Just-in-time production saves money but leaves no slack, forcing firms to weigh buffers against disruption.", "Medium",
    ["Just-in-time production keeps inventories low by arranging for parts to arrive only shortly before they are needed.",
     "The savings are real: less money is tied up in stock, less space is needed for storage, and defects are noticed before large batches pile up.",
     "The same leanness, however, leaves little slack when a supplier is delayed, so a disruption far up the chain can halt an assembly line within days.",
     "Firms have accordingly begun to weigh the cost of holding buffers against the cost of being caught without them."],
    "Some retailers apply a similar logic to staffing, scheduling workers only for the hours when customers are expected to arrive.",
    "The paragraph sets out a trade-off in managing parts: [[1]] describes the method, [[2]] its benefits, [[3]] ('The same leanness, however') its vulnerability to supply delays, and [[4]] ('accordingly') the response of weighing buffers against risk. Sentence [[X]] borrows the logic of leanness but moves to staffing, a different domain that the trade-off between stock and supply disruption does not cover.",
    "Treating sentence [[X]] as another illustration of the method, without noticing that the rest of the paragraph is about parts, suppliers and buffers of stock.",
    "V03F-just-in-time-inventory", "The odd sentence uses the same idea in a nearby domain and must be rejected because it breaks the focus on inventory.",
    traps=[(4, "Sentence [[4]] belongs: 'accordingly' answers the risk described in sentence [[3]], and its 'buffers' are the stock that the method cuts back.")])

# ------------------------------------------------------------------ 017
ooo("V03-F-017", "Science and environment", "Volcanic soils explain why people farm on dangerous slopes.", "Easy",
    ["Volcanic eruptions are destructive in the short term, burying fields and forcing people to abandon their homes.",
     "Over longer periods, however, the ash they deposit weathers into soils rich in the minerals that plants need.",
     "This is one reason why dense farming populations have often lived on the slopes of active volcanoes despite the danger.",
     "For such communities, the risk of an eruption is weighed against generations of unusually good harvests."],
    "Scientists watch for small earthquakes and changes in gas emissions in order to forecast when a volcano may erupt.",
    "The four coherent sentences explain why people farm near volcanoes: eruptions destroy ([[1]]), but ash becomes fertile soil ([[2]], 'however'), which is why farmers settle there ([[3]]), weighing risk against harvests ([[4]]). Sentence [[X]] is about volcanoes but describes how eruptions are forecast, which plays no part in the trade-off between danger and fertility.",
    "Choosing sentence [[1]] because it is about destruction rather than farming, though sentence [[2]] needs it for its 'however'.",
    "V03F-volcanic-soils-and-farming", "The odd sentence turns to forecasting techniques, which is clearly outside the paragraph's line of thought.",
    traps=[(1, "Sentence [[1]] is the short-term harm that sentence [[2]] sets against the long-term benefit with 'Over longer periods, however'.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 018
ooo("V03-F-018", "Science and environment", "Bleached corals can recover, but heat events are coming too often for recovery.", "Medium",
    ["Corals that build reefs live in partnership with tiny algae housed in their cells, trading shelter for the sugars the algae make from sunlight.",
     "Prolonged heat disrupts the arrangement: the stressed corals eject their lodgers and lose both their colour and their main source of food.",
     "Such an episode need not be fatal, for a reef that is given a few cool years can be recolonised by algae and slowly regain its health.",
     "What alarms marine scientists is that the gaps between severe heatwaves are narrowing, so that many reefs are struck again before they have recovered."],
    "Reefs also shield coastlines, absorbing much of the energy of incoming waves before they break on the shore.",
    "The paragraph explains bleaching and why its frequency is the real threat: [[1]] describes the partnership between coral and algae, [[2]] ('the arrangement') how heat breaks it, [[3]] ('Such an episode') that a reef can recover given time, and [[4]] that heatwaves now return before recovery is complete. Sentence [[X]] is about reefs but describes their value as coastal defences, which does not connect to the account of bleaching and recovery.",
    "Treating any true statement about reefs as part of the paragraph, instead of checking whether it advances the explanation of bleaching.",
    "V03F-coral-bleaching", "The odd sentence shares the subject and is plausible as a reason to care about reefs, so it must be rejected on function.",
    traps=[(3, "Sentence [[3]] may seem to soften the warning, but sentence [[4]] depends on it: the alarm is that recovery, which is possible, is no longer given time.")])

# ------------------------------------------------------------------ 019
ooo("V03-F-019", "Science and environment", "Earthworms improve soil by aerating it and recycling dead leaves.", "Easy",
    ["Earthworms are easy to overlook, but they do a great deal of work in the soil.",
     "As they burrow, they open channels that let air and water reach the roots of plants.",
     "They also drag dead leaves underground and break them down, returning nutrients to the soil.",
     "A field rich in earthworms is therefore often a sign of healthy, fertile ground."],
    "Some birds find worms by watching and listening closely before striking at the ground.",
    "The four coherent sentences describe the work earthworms do in soil: the claim ([[1]]), burrowing that lets in air and water ([[2]]), recycling of leaves ([[3]], 'also'), and the conclusion ([[4]], 'therefore'). Sentence [[X]] mentions worms but is about how birds hunt them, which has nothing to do with the soil.",
    "Choosing sentence [[4]] because it moves from worms to fields, though it draws the conclusion of the paragraph.",
    "V03F-earthworms-and-soil", "The odd sentence changes the focus from what worms do to what birds do, which is easy to see.",
    traps=[(4, "Sentence [[4]] belongs: 'therefore' concludes from the two kinds of work described in sentences [[2]] and [[3]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 020
ooo("V03-F-020", "Science and environment", "Light pollution's real loss is the night sky in ordinary experience, a loss hidden because people never knew it.", "Difficult",
    ["Light pollution is usually discussed as a problem for astronomers, whose instruments are blinded by the glow of nearby cities.",
     "Yet the professionals have largely dealt with their difficulty by moving their telescopes to remote mountains and deserts.",
     "The loss that remains falls on everyone else, for whom a sky that once shaped calendars, navigation and myth has shrunk to a handful of faint points.",
     "What makes this loss so easy to ignore is that a child raised under an orange haze has no memory of a starry sky with which to compare it."],
    "Poorly shielded lamps also waste a great deal of energy by sending light upward, where it illuminates nothing anyone needs to see.",
    "The paragraph argues that the real cost of light pollution is the disappearance of the night sky from ordinary experience: [[1]] gives the usual framing, [[2]] ('Yet') notes that astronomers have escaped it, [[3]] identifies 'the loss that remains', and [[4]] explains why 'this loss' goes unnoticed. Sentence [[X]] shares the vocabulary of lamps, light and sky, but it introduces a different kind of cost, wasted energy, and its 'also' has no earlier cost of the same kind to attach to. Wherever it is placed it breaks the thread: before sentence [[4]] it would leave 'this loss' pointing at wasted energy, and after sentence [[4]] it starts a new topic.",
    "Accepting sentence [[X]] as one more harm of light pollution, without noticing that the paragraph is about one particular loss and why it is overlooked.",
    "V03F-light-pollution-and-astronomy", "The odd sentence names a real harm in the same vocabulary; rejecting it requires seeing that the paragraph concerns a single, experiential loss.",
    traps=[(2, "Sentence [[2]] seems to drop the subject of astronomers abruptly, but it is what lets sentence [[3]] speak of 'the loss that remains' for everyone else."),
           (4, "Sentence [[4]] looks like a separate remark about children, but 'this loss' refers to the vanished sky of sentence [[3]] and explains why it is ignored.")],
    exams=D2)

# ------------------------------------------------------------------ 021
ooo("V03-F-021", "Science and environment", "Migrating birds use several navigation cues, a redundancy that guards against fatal errors.", "Medium",
    ["Migrating birds appear to rely on several navigational cues rather than on a single one.",
     "Many can sense the earth's magnetic field, some take bearings from the setting sun, and night migrants have been shown to orient by the pattern of the stars.",
     "Having more than one system allows a bird to keep its course when one cue becomes unavailable, as when clouds hide the sky.",
     "Such redundancy makes sense for an animal that may cross a sea or a desert with nowhere to land, where losing its way would be fatal."],
    "Before setting off, some species fatten rapidly, in certain cases nearly doubling their body weight to fuel the journey.",
    "The paragraph is about navigation: [[1]] states that birds use several cues, [[2]] lists them, [[3]] explains the benefit of having more than one, and [[4]] ('Such redundancy') explains why the benefit matters. Sentence [[X]] is about migration too, but it concerns fuel for the journey rather than finding the way, so it connects to none of the steps about cues and redundancy.",
    "Linking sentence [[X]] to sentence [[4]] because both mention the demands of a long crossing, though sentence [[4]] is about the cost of getting lost.",
    "V03F-bird-migration-navigation", "The odd sentence shares the subject of migration and is rejected because it concerns energy, not navigation.",
    traps=[(2, "Sentence [[2]] can look like a list of facts, but it supplies the several cues that sentence [[1]] promises and sentence [[3]] relies on.")])

# ------------------------------------------------------------------ 022
ooo("V03-F-022", "Technology", "An electric car's battery creates an upfront emissions debt whose repayment depends on use and on the grid.", "Medium",
    ["An electric car begins its life with a larger environmental debt than a petrol car, largely because making its battery requires mining and energy-intensive processing.",
     "It can repay that debt over time, because driving on electricity usually produces fewer emissions per kilometre than burning petrol.",
     "How quickly the debt is cleared therefore depends on how much the car is driven and on how the electricity that charges it is generated.",
     "A vehicle charged from a grid dominated by coal and driven little may take many years to break even, while one charged from cleaner sources does so much sooner."],
    "Battery prices have fallen steeply over the past decade, bringing electric cars within reach of many more buyers.",
    "The paragraph treats the battery's environmental cost as a debt: [[1]] describes the debt incurred in manufacture, [[2]] how driving repays it, [[3]] ('therefore') what the speed of repayment depends on, and [[4]] contrasts a coal-charged, little-used car with a cleanly charged one. Sentence [[X]] is about batteries too, but it concerns their price and affordability, which plays no part in the accounting of emissions.",
    "Accepting sentence [[X]] because it is about batteries, the very component sentence [[1]] blames for the debt, without checking whether it bears on emissions.",
    "V03F-electric-vehicle-batteries", "The odd sentence shares the central term (batteries) and must be rejected because it is about cost to buyers, not environmental cost.",
    traps=[(4, "Sentence [[4]] belongs because it illustrates the two factors named in sentence [[3]], amount of driving and source of electricity.")])

# ------------------------------------------------------------------ 023
ooo("V03-F-023", "Technology", "Spam filtering is an adversarial contest, so past accuracy overstates future performance and no victory is final.", "Difficult",
    ["A spam filter learns to recognise unwanted mail from examples of messages that users have already marked as junk.",
     "Unlike a system that learns to read handwriting, however, it faces opponents who study its decisions and change their messages to slip past it.",
     "A filter's accuracy on last month's mail is therefore an unreliable guide to how it will perform next month, since the mail itself is reacting to the filter.",
     "The contest has no final victory, only a shifting balance in which each improvement in detection invites a fresh round of evasion."],
    "Because people disagree about what counts as junk, a newsletter one user welcomes may be exactly what another wants filtered out.",
    "The paragraph is about the adversarial character of spam filtering: [[1]] describes how a filter learns, [[2]] ('however') contrasts it with handwriting recognition because senders adapt, [[3]] ('therefore') draws the consequence for measured accuracy, and [[4]] generalises that the contest never ends. Sentence [[X]] uses the same vocabulary of junk and filtering, but it raises a different difficulty, that users disagree about what is unwanted. That problem would exist even if senders never adapted, so it does nothing for the argument about opponents, and nothing in sentences [[3]] or [[4]] refers to it.",
    "Treating sentence [[X]] as another difficulty that filters face and so as part of the paragraph, without noticing that every other sentence concerns opponents who adapt.",
    "V03F-spam-filtering", "The odd sentence is a genuine problem for filters, in the same words; it is rejected only by identifying that the paragraph's argument is specifically about adversaries.",
    traps=[(1, "Sentence [[1]] can look like a bland definition, but 'it' in sentence [[2]] refers to the filter it introduces, and the handwriting contrast assumes learning from examples."),
           (4, "Sentence [[4]] may seem to repeat sentence [[3]], but it widens the point from measured accuracy to the endless cycle of detection and evasion, and so closes the argument.")],
    exams=D2)

# ------------------------------------------------------------------ 024
ooo("V03-F-024", "Technology", "Widely used open source code is under-funded because benefits are shared, and remedies try to attach payment to it.", "Medium",
    ["A good deal of the software on which businesses depend is maintained by a handful of volunteers who are paid nothing for the work.",
     "Companies that rely on such code have little individual incentive to fund it, since they benefit from it whether or not they contribute.",
     "The result is a quiet fragility, in which critical components may be neglected until a serious flaw is discovered in them.",
     "Proposals to remedy this, from foundations that pool corporate money to public grants, all try to attach payment to work whose benefits are widely shared."],
    "Open source licences allow anyone to read, modify and redistribute the code, which is what distinguishes such software from proprietary products.",
    "The paragraph traces a funding problem: [[1]] says vital code is maintained by unpaid volunteers, [[2]] explains why users do not pay, [[3]] ('The result') names the fragility that follows, and [[4]] ('to remedy this') describes the proposed fixes. Sentence [[X]] is about open source software, but it defines its licences, which does not advance the argument about incentives, neglect and funding.",
    "Choosing sentence [[X]] as background that the paragraph needs, although the argument never relies on how the licences work.",
    "V03F-open-source-funding", "The odd sentence shares the subject and reads like useful background, so it must be rejected on function.",
    traps=[(2, "Sentence [[2]] is the cause in the chain: without the free-rider point, 'The result' in sentence [[3]] has nothing to follow from.")])

# ------------------------------------------------------------------ 025
ooo("V03-F-025", "Technology", "Two-factor authentication blocks many break-ins because a stolen password is no longer enough.", "Easy",
    ["Passwords alone are a weak defence, because they can be guessed, stolen or reused across many sites.",
     "Two-factor authentication adds a second requirement, such as a code sent to the user's phone.",
     "An attacker who has stolen a password still cannot log in without also having that second item.",
     "This simple extra step can therefore block many attempts to break into accounts."],
    "Many people find long passwords hard to remember and end up writing them down on paper.",
    "The four coherent sentences explain why two-factor authentication works: passwords are weak ([[1]]), a second requirement is added ([[2]]), a stolen password is no longer enough ([[3]]), so the step blocks many break-ins ([[4]], 'therefore'). Sentence [[X]] is about passwords, but it describes a habit of users and plays no part in explaining the second factor.",
    "Choosing sentence [[1]] because it is about passwords rather than the second factor, though it states the weakness the rest of the paragraph answers.",
    "V03F-two-factor-authentication", "The odd sentence is about remembering passwords, which is plainly not part of the explanation.",
    traps=[(1, "Sentence [[1]] states the problem, and sentence [[3]]'s 'stolen a password' depends on it.")],
    cognitive="Understanding")
