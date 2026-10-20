import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

SCI = "Science and environment"
TEC = "Technology"
ART = "Arts and literature"
LAN = "Language and media"
EDU = "Education"
HEA = "Health and medicine"
HARD = ("CAT", "XAT")

# ---------------------------------------------------------------- 001
ps("V02-N-001", SCI, "Removing a dam starts a slow, initially disruptive recovery rather than restoring the river at once.", "Easy",
   "When an old dam is taken down, people often expect the river to return at once to the condition it was in before the dam was built. What usually happens is messier. Sediment that piled up behind the wall for decades is released and travels downstream, burying gravel beds and clouding the water for a season or more. Fish that had been blocked may take years to recolonise the upstream reaches, and the plants that first cover the drained reservoir bed are often weeds rather than the species that grew there before. None of this means that removal fails; on many rivers the long-term gains in fish passage and natural flow are substantial. It means that removal starts a process of recovery rather than restoring a finished state, and that the early years can look worse than what came before.",
   "Taking down a dam begins a gradual, at first disruptive recovery rather than an instant return to the river's earlier state, though the long-term gains can be considerable.",
   [("Sediment released when a dam is removed travels downstream and buries gravel beds, which clouds the water and harms the river for at least a season afterwards.",
     "This is one detail from the third sentence; it leaves out the paragraph's point that removal begins a recovery whose long-term gains can be 'substantial'."),
    ("Because the first years after removal often look worse than before, taking down old dams usually does more harm to a river and its fish than simply leaving the old walls standing.",
     "The paragraph says 'None of this means that removal fails' and stresses long-term gains, so this option reverses its conclusion."),
    ("Old dams ought to be removed slowly and in stages, so that sediment and weeds do not overwhelm the river and fish can return upstream more quickly.",
     "The paragraph recommends no method of removal; staged removal is an outside prescription that the text never makes.")],
   "The paragraph corrects the expectation of an instant return: sediment, slow recolonisation and weeds make the early years 'messier', but 'None of this means that removal fails'. The correct answer keeps both halves: removal 'starts a process of recovery rather than restoring a finished state', and the long-term gains can be 'substantial'.",
   "Picking the vivid sediment detail, or reading the description of early damage as a verdict against removal.",
   "V02N-dam-removal-recovery", "The point is stated in the last two sentences and each wrong option is clearly narrow, reversed or prescriptive.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 002
ps("V02-N-002", SCI, "Earthquake forecasts are valuable when judged as probabilities, not as failed predictions.", "Medium",
   "Seismologists distinguish between predicting an earthquake and forecasting one, and public discussion often blurs the two. A prediction would name a place, a window of days or weeks and a magnitude, precisely enough to justify evacuating a city. No method has reliably done this, and claims to the contrary have tended to collapse under scrutiny. A forecast is more modest: it estimates the probability of a strong quake in a region over years or decades, using the record of past ruptures and the strain measured on faults. A forecast cannot tell anyone to leave on Tuesday, but it can tell a city how strict its building codes should be and where a hospital ought not to be built. Judged as failed predictions, forecasts look useless; judged as what they are, they are among the most practically valuable things the science produces.",
   "Although no method has reliably said when and where a quake will strike, long-range probability forecasts are very useful for decisions such as building codes, if judged on their own terms.",
   [("Since seismologists cannot say when an earthquake will strike, their probability estimates are of little practical use and should not be allowed to guide how cities are planned or where they build.",
     "The paragraph says forecasts 'look useless' only when wrongly 'Judged as failed predictions', and calls them highly valuable; this option adopts the mistaken judgement."),
    ("Better measurement of the strain on faults will soon let seismologists turn their long-range forecasts into precise predictions that justify evacuating whole cities.",
     "Nothing in the paragraph anticipates such progress; it says no method has reliably predicted quakes, so this is an outside speculation."),
    ("Claims to have predicted earthquakes have usually collapsed under scrutiny, so the public should distrust anyone who announces the date and place of a coming quake.",
     "This takes one sentence about failed predictions and adds advice; it omits the central contrast with forecasts and their practical value.")],
   "The paragraph contrasts prediction, which 'No method has reliably done', with forecasting, which estimates probabilities over 'years or decades' and guides 'building codes' and the siting of hospitals. Its conclusion is that forecasts are valuable 'judged as what they are'. The correct answer captures the contrast and that conclusion.",
   "Equating the failure of prediction with the failure of seismology, or picking the option that dwells on discredited predictions.",
   "V02N-earthquake-forecasting", "The narrow wrong option about failed predictions is partly right, so the reader must keep hold of the two-part contrast.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 003
ps("V02-N-003", SCI, "Captive breeding justifies zoos only under stated conditions, chiefly a wild habitat for release.", "Difficult",
   "Zoos often justify themselves by pointing to captive breeding: species that have vanished from the wild survive in enclosures and may one day be returned. The argument is not empty; a handful of animals have been reintroduced after being bred in captivity. But the justification works only under conditions that are seldom stated. A captive population must be large and genetically varied enough to avoid inbreeding, the animals must keep the behaviours they need to survive outside, and, most easily forgotten, there must be a wild habitat to return them to. Where the forest has been cleared, or the threat that emptied it persists, breeding preserves a species in something like suspended animation, alive but with nowhere to go. Captive breeding, in other words, is a bridge, and a bridge is valuable only if something is being built on the far side.",
   "Captive breeding can really help to conserve species, but only if demanding conditions are met, above all a wild habitat fit for release; without one, it keeps a species alive but cannot restore it.",
   [("Zoos are justified chiefly by their breeding programmes, which have kept alive species that vanished in the wild and have allowed several of them to be returned to their habitats.",
     "This is the zoos' own justification as the first two sentences report it; it drops the paragraph's main claim that the argument 'works only under conditions that are seldom stated'."),
    ("Captive breeding is an empty excuse for keeping zoos, because animals raised in enclosures lose the behaviours they need and can almost never be returned to the wild.",
     "The paragraph states 'The argument is not empty' and treats lost behaviours as one condition to be met, not as a fact that defeats breeding."),
    ("Money spent on breeding endangered animals in zoos would do more for conservation if it were spent instead on protecting forests and removing threats in the wild.",
     "The paragraph never compares the value of the two kinds of spending; it says breeding needs habitat, not that habitat protection should replace breeding.")],
   "The paragraph concedes that captive breeding is 'not empty' but argues that it 'works only under conditions', the most neglected being a habitat 'to return them to'. Without it a species is 'alive but with nowhere to go'; breeding is 'a bridge' that is valuable only if the far side is built. The correct answer states the concession, the conditions and what happens when habitat is missing.",
   "Choosing the funding comparison because it sounds like the bridge metaphor, when the paragraph sets a condition rather than ranking two policies.",
   "V02N-captive-breeding-conditions", "Two wrong options sit close to the author's stance: one repeats the reported justification, one turns the habitat condition into a spending recommendation.",
   exams=HARD)

# ---------------------------------------------------------------- 004
ps("V02-N-004", SCI, "Renaming eponymous species has a real record-keeping cost, so reform should look forward.", "Medium",
   "Naming a newly described species after a person is an old habit, and some critics now ask whether names honouring patrons, colonial officials or celebrities should be changed. The case for renaming is easy to feel when the honoured figure was cruel. Yet the strongest reason for caution has little to do with the reputations involved. A scientific name is a retrieval key: it links the specimen in a museum drawer to every paper ever written about it. Change the name and that chain is not cut, since the rules keep track of older names, but it is lengthened and made fragile, especially for the many species known only from a single description in an obscure journal. The more promising reform looks forward: choosing descriptive names for new species costs nothing, while renaming old ones carries a real price in scientific record-keeping.",
   "Whatever the honoured person's record, renaming species is costly because names are stable links to the literature, so reform should target how new species are named.",
   [("Species named after cruel colonial officials ought to be renamed at once, since the moral offence of such names plainly outweighs the trouble of updating the scientific records.",
     "The paragraph grants that the case for renaming is 'easy to feel' but argues for caution; this option takes the side the author resists."),
    ("Changing a species' name permanently severs the link between museum specimens and the literature, making many obscure species impossible for researchers to trace.",
     "The paragraph says 'that chain is not cut' but 'lengthened and made fragile', so this option overstates the cost into a severed link."),
    ("Species should be given names that describe their features rather than honour people, since honouring individuals has always led to disputes over reputations.",
     "The paragraph favours descriptive names because renaming is costly, not because honouring people 'always' causes disputes; it says caution 'has little to do with the reputations involved'.")],
   "The paragraph sets aside the reputation question and argues that a name's value is as a 'retrieval key'. Renaming does not cut the chain but makes it 'fragile', so the better reform 'looks forward' to new names. The correct answer gives the cost, its reason, and the forward-looking remedy.",
   "Choosing the 'severs the link' option because it sounds like the paragraph's concern, without noticing that the text explicitly says the chain is not cut.",
   "V02N-eponymous-species-names", "One wrong option differs from the text only in degree (cut versus made fragile) and another gives the right remedy for the wrong reason.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 005
ps("V02-N-005", TEC, "Undo makes mistakes cheap, which encourages experiment and so helps users learn software.", "Easy",
   "The undo command looks like a minor convenience, but it changes how people use software. When every action can be reversed, users explore: they try an unfamiliar menu, apply a filter just to see what it does, delete a paragraph to judge whether the essay reads better without it. Where actions are permanent, the same users grow cautious, read instructions first and stick to the few operations they already trust. Undo, in other words, lowers the cost of a mistake, and when mistakes are cheap, experimenting becomes rational. Much of what people learn about a program they learn by just such trial and error, so a design that forgives errors also turns out to be one that teaches.",
   "By making mistakes cheap to reverse, the undo command encourages users to experiment, and since people learn programs largely by trial and error, this tolerance of errors also helps them learn.",
   [("Software without an undo command makes users read instructions carefully, which leaves them more skilled and confident than users who simply reverse their errors.",
     "The paragraph treats caution without undo as limiting, since users 'stick to the few operations they already trust'; it never says they become more skilled."),
    ("People using software with an undo command make far more mistakes than other users do, because they know that any error they commit can be reversed at no cost at all.",
     "The paragraph says undo makes mistakes cheap and exploration rational; it makes no claim that users commit more errors."),
    ("When the actions in a program cannot be reversed, people become cautious, read the instructions first and use only the operations they already trust.",
     "This restates one sentence about permanent actions and misses the main point that undo encourages exploration and therefore learning.")],
   "The paragraph explains a chain: undo 'lowers the cost of a mistake', cheap mistakes make 'experimenting' rational, and people learn programs by 'trial and error', so 'a design that forgives errors' also 'teaches'. The correct answer states the whole chain.",
   "Choosing the narrow option about permanent actions because it is closely worded from the paragraph.",
   "V02N-undo-forgiving-design", "The causal chain is explicit and the wrong options are plainly narrow or unsupported.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 006
ps("V02-N-006", TEC, "Endless scrolling reflects the removal of stopping points more than weak willpower.", "Medium",
   "It is common to blame endless feeds on a lack of willpower, as if people who scroll for an hour simply could not stop. This misplaces the problem. Much everyday self-control depends less on resisting temptation moment by moment than on natural stopping points: the end of a chapter, the last page of a newspaper, the credits of an episode. Such boundaries invite a small decision about whether to go on, and many people, offered that decision, stop. A feed that loads new items before the old ones run out removes the boundary and with it the decision. The user never declines to stop; the moment to stop simply never arrives. Designers who wished to respect their users' time would therefore do more by restoring edges than by lecturing anyone about discipline.",
   "Long spells of scrolling owe less to weak willpower than to feeds that remove the natural stopping points where people would otherwise choose to quit, so restoring them would help.",
   [("People who scroll through endless feeds for hours lack the self-discipline of earlier generations of readers, who stopped at the end of a chapter or on the last page of a newspaper.",
     "The paragraph rejects the willpower explanation ('This misplaces the problem'); earlier readers stopped because boundaries offered a decision, not because they were more disciplined."),
    ("Endless feeds are built to exploit their users, and designers should be held legally responsible for the hours that people lose to scrolling every day.",
     "The paragraph says nothing of exploitation or legal responsibility; it suggests designers restore 'edges', which is a design change, not liability."),
    ("Self-control depends mainly on natural boundaries such as the ends of chapters, which is why people reading printed books rarely lose track of the time.",
     "The paragraph says 'Much everyday self-control' depends on stopping points and makes no claim about book readers losing track of time; this generalises one premise into an unsupported conclusion.")],
   "The paragraph rejects the willpower account: stopping points 'invite a small decision', and a feed that keeps loading 'removes the boundary and with it the decision'. Hence designers should restore 'edges' rather than lecture about 'discipline'. The correct answer gives the diagnosis and the remedy.",
   "Taking the reported willpower view at face value, or choosing the option that stretches the premise about chapter endings into a claim about readers.",
   "V02N-infinite-scroll-stopping-points", "The third wrong option reuses the paragraph's premise but extends it beyond what is said, which takes a careful reading to reject.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 007
ps("V02-N-007", TEC, "Steady satisfaction scores after chatbots may hide abandoned hard cases.", "Difficult",
   "Firms that replace telephone agents with chatbots often report that customer satisfaction scores barely move, and conclude that customers do not mind. The figure is real, but what it measures deserves a closer look. Satisfaction surveys are usually sent to customers whose conversations ended, and a conversation with a bot ends in two very different ways: the problem is solved, or the customer gives up. Those who give up rarely answer a survey about an exchange they abandoned, and some of them quietly take their business elsewhere. Meanwhile the simple queries that bots handle well, such as tracking a parcel, were never the ones that tested anyone's patience. Steady scores may therefore show only that bots cope with easy cases, while the frustrations of hard cases fall outside what is being counted.",
   "Unchanged satisfaction scores after chatbots arrive may reflect only the easy queries that bots resolve, since customers who abandon frustrating conversations tend to go unrecorded in the surveys.",
   [("Satisfaction scores show that customers do not mind chatbots, because bots resolve simple queries such as tracking a parcel as well as human agents ever did.",
     "This is the firms' conclusion that the paragraph questions; the author says the figure is real but that what it measures 'deserves a closer look'."),
    ("Chatbots deal badly with difficult problems, so firms that replace their telephone agents lose many customers and watch their satisfaction scores steadily fall.",
     "The paragraph says scores 'barely move', and it claims only that 'some' customers leave; falling scores and heavy losses contradict and overstate it."),
    ("Firms deliberately send satisfaction surveys only to customers whose problems were solved, so the scores they publish for chatbots are knowingly misleading.",
     "Surveys go to customers 'whose conversations ended', including those who gave up; the bias comes from who answers, and the paragraph alleges no deliberate deception.")],
   "The paragraph accepts the figure but questions its meaning: surveys reach conversations that ended, the customers who 'give up' rarely respond, and the easy queries bots handle were never the test. So steady scores 'may therefore show only that bots cope with easy cases'. The correct answer states this hedged reinterpretation and its mechanism.",
   "Choosing the deliberate-deception option, which mirrors the idea of a biased sample but misplaces where the bias arises.",
   "V02N-chatbot-satisfaction-scores", "The deception option is close to the correct answer's mechanism and must be rejected on a precise reading of who receives and who answers surveys.",
   exams=HARD)

# ---------------------------------------------------------------- 008
ps("V02-N-008", TEC, "Range anxiety about electric cars comes from rare trips and old habits, and fades with use.", "Easy",
   "Buyers considering an electric car often worry about range, picturing themselves stranded with a flat battery far from any charger. Yet the typical car spends most days on short trips that use a small fraction of even a modest battery, and owners who charge at home begin each morning with a full one. The worry is shaped by the rare long journey rather than the ordinary day, and by habits formed with petrol cars, for which refuelling means a special trip to a station. For many owners the anxiety fades within months, not because the battery has grown but because they have learned how their own driving actually uses it. Range does matter, but less often than the fear of it suggests.",
   "Worry about electric car range stems more from rare long trips and petrol-car habits than from daily driving, and it tends to fade as owners learn their real needs.",
   [("Electric cars now carry batteries large enough for any journey at all that a driver might plan, so every worry about being stranded far from a charger is simply mistaken.",
     "The paragraph says 'Range does matter', only 'less often than the fear of it suggests'; it never claims batteries suffice for any journey."),
    ("Owners who charge their electric cars at home begin every morning with a full battery and therefore never need to visit a public charging station.",
     "This expands one detail into 'never', which the paragraph does not say; it also misses the explanation of where the worry comes from."),
    ("People who mostly drive on long journeys should keep buying petrol cars for now, since they alone face a genuine risk of running out of charge far from home.",
     "The paragraph gives no buying advice and does not say that only long-distance drivers face any risk.")],
   "The paragraph explains range worry as shaped by 'the rare long journey rather than the ordinary day' and by petrol-car 'habits', and says it 'fades within months' as owners learn their driving. The correct answer covers the cause and the fading, and by saying the worry stems more from these than from daily driving it keeps the concession that 'Range does matter'.",
   "Choosing the option that turns the reassurance into a claim that range never matters.",
   "V02N-ev-range-anxiety", "Cause and conclusion are stated directly; wrong options are clearly extreme, narrow or prescriptive.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 009
ps("V02-N-009", ART, "Apparent flaws of serial novels were sensible responses to instalment publication.", "Medium",
   "Many nineteenth-century novels first reached readers in instalments, a part at a time over many months, and the form left marks on the books that later readers of the bound volume can miss. Each part needed its own small climax to bring buyers back, so chapters often close on suspense or revelation. Because readers might forget a minor character between instalments, writers gave such figures memorable tags, a phrase or a habit repeated at each appearance. The long gaps also let an author learn how the story was being received, and plots were sometimes adjusted in response. Features that a modern critic might fault as contrived or repetitive were, in their first setting, sensible answers to the conditions of publication.",
   "Some features of serialised nineteenth-century novels that now look like flaws, such as cliffhanger endings and repeated character tags, were sensible responses to publication in instalments.",
   [("Nineteenth-century novelists often wrote carelessly because they were paid by the instalment, which accounts for the contrived plots and repetitive minor characters found in their books.",
     "The paragraph never mentions payment or carelessness; it argues that such features were 'sensible answers', the opposite of careless writing."),
    ("Serial publication let readers shape the plots of nineteenth-century novels, which authors rewrote every month according to what their audience demanded.",
     "The paragraph says plots were 'sometimes adjusted' in response; 'rewrote every month' and audience demands overstate one detail into the main point."),
    ("Modern readers ought to read nineteenth-century novels in monthly parts, as their first readers did, in order to appreciate their suspense and their characters.",
     "The paragraph explains features of the books but recommends no way of reading them; this is an added prescription.")],
   "The paragraph lists effects of serial publication: chapter-end suspense, 'memorable tags' for minor characters, plots adjusted to reception. It concludes that features a critic 'might fault as contrived or repetitive' were 'sensible answers to the conditions of publication'. The correct answer states that reinterpretation with its examples.",
   "Choosing the reader-influence option, which inflates the 'sometimes adjusted' detail.",
   "V02N-serial-novel-instalments", "The reader-influence option rests on a real detail and must be rejected for degree and narrowness.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 010
ps("V02-N-010", ART, "Sympathetic villains are not a fault; the fault is letting backstory cancel judgement.", "Difficult",
   "A familiar complaint about recent fiction is that its villains have become too sympathetic: give every tyrant a sad childhood, the critics say, and evil dissolves into misfortune. The complaint mistakes explanation for excuse. To show how a person came to do terrible things is not to claim that the things were less terrible; it may make them more disturbing, since it removes the comfort of thinking that such acts belong to monsters unlike ourselves. Where the criticism does land is on stories that use the backstory to settle the moral question, inviting the reader to feel that a painful past cancels the harm done. The fault there is not sympathy but a failure of nerve: the writer has explained the villain and then flinched from judging him.",
   "Giving a villain an understandable past does not in itself excuse his deeds and may make them more unsettling; the real fault lies in stories that let such a past cancel moral judgement.",
   [("Recent fiction has weakened moral judgement by giving its tyrants sad childhoods, so that readers come to regard evil as mere misfortune rather than wrongdoing.",
     "This is the critics' complaint, which the author says 'mistakes explanation for excuse'; the author accepts it only for stories that let backstory settle the moral question."),
    ("Explaining how a villain came to commit terrible acts always makes those acts more disturbing, so writers should give every villain a detailed and painful past.",
     "The paragraph says explanation 'may' make acts more disturbing, and it recommends no backstory for every villain; 'always' and the prescription both overstate it."),
    ("Readers find sympathetic villains more disturbing than monstrous ones, because such characters remind them that ordinary people like themselves, and not only monsters, are capable of terrible acts.",
     "This reworks one supporting idea into a claim about readers' reactions and drops the central distinction between explaining and excusing, and the stated fault of flinching from judgement.")],
   "The paragraph separates 'explanation' from 'excuse': explaining a villain 'may make' his acts 'more disturbing'. It then concedes where the criticism lands, on stories in which 'a painful past cancels the harm done', and names that fault as flinching 'from judging him'. The correct answer keeps the distinction, the hedge and the concession.",
   "Choosing the option about readers being disturbed, which echoes the paragraph's middle but loses its argument.",
   "V02N-sympathetic-villains", "Every wrong option uses the paragraph's material; the correct answer is found only by tracking the explanation-versus-excuse distinction and the concession.",
   exams=HARD)

# ---------------------------------------------------------------- 011
ps("V02-N-011", ART, "Silence between movements is a recent convention, not tradition, so clappers should not be scorned.", "Easy",
   "At a symphony concert, a burst of clapping after the opening movement is often answered by hissing from seasoned listeners, who regard unbroken quiet until the final chord as a sacred inheritance. The custom is younger than they suppose. Listeners in the eighteenth and early nineteenth centuries commonly clapped when a movement ended, and on occasion broke in while the orchestra was still playing. The demand for total quiet hardened only later, once the concert hall began to be approached in a mood of reverence. A case for the pause can still be made: a soft close needs a moment to fade into the room. Yet that case has to stand on its own feet rather than on a claim of antiquity, and it gives no licence for treating first-time listeners with contempt.",
   "Quiet between movements is a later custom, not an ancient one, so while the pause may be worth keeping, it must be defended on its merits and gives no excuse for scorning newcomers.",
   [("Concert audiences ought to return to the older habit of clapping between and even during movements, since that is how such music was first received by the listeners who heard it when it was new.",
     "The paragraph grants that 'A case for the pause can still be made' and asks only that it be argued properly; it does not urge a return to the old habit."),
    ("Silence between the movements of a symphony has no real justification and survives only because modern listeners approach the concert hall with a kind of reverence.",
     "The paragraph concedes that a soft close 'needs a moment to fade into the room', so the claim that silence has no justification contradicts it."),
    ("Listeners in the eighteenth and early nineteenth centuries often clapped at the end of a movement and sometimes even interrupted the orchestra while it was playing.",
     "This repeats the historical evidence but omits the paragraph's conclusions about how the pause should be defended and how newcomers should be treated.")],
   "The paragraph shows that 'The custom is younger than they suppose', concedes that 'A case for the pause can still be made', and concludes that the case must 'stand on its own feet rather than on a claim of antiquity' and gives 'no licence' for contempt towards first-time listeners. The correct answer keeps all three parts.",
   "Choosing the historical detail, or reading the critique of the custom as a rejection of silence.",
   "V02N-applause-between-movements", "The concession and conclusion are explicit, and the wrong options fail on obvious grounds.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 012
ps("V02-N-012", ART, "Ruins appeal through imaginative completion and visible time, which is why restorations can disappoint.", "Medium",
   "Why do ruins draw visitors who would walk past the same building, intact, without a glance? Part of the answer is that a ruin asks the viewer to do some work. The missing roof and broken arches invite the mind to complete them, and an image a person has helped to build feels more vivid than one simply handed over. A ruin also makes time visible: weathered stone and the roots pushing through it show at a glance the centuries that a whole building conceals. This suggests why restorations sometimes disappoint. A restored castle may be more accurate than its broken neighbour, yet it leaves nothing to imagine and hides the very history it was meant to display.",
   "Ruins appeal because viewers must imagine what is missing and because decay displays the passing of time, which also explains why faithful restorations can disappoint those who visit them.",
   [("Ruined buildings should be left as they stand rather than restored, since restoration falsifies history and makes old castles less accurate than their broken neighbours.",
     "The paragraph says a restored castle 'may be more accurate', and it recommends no policy; this reverses one claim and adds a prescription."),
    ("Visitors prefer ruins to intact buildings mainly because ruins are older, and age has always been the chief source of a building's appeal to those who travel to see it.",
     "The paragraph gives two reasons, imaginative work and visible time; it never says ruins are older or that age 'always' governs appeal."),
    ("A building that a viewer must complete in the imagination feels more vivid than one presented whole, because people value images they have helped to create.",
     "This gives only the first of the two reasons and leaves out visible time and the consequence for restorations.")],
   "The paragraph gives two reasons for the pull of ruins: they ask the viewer 'to do some work' of completion, and they make 'time visible'. It then draws a consequence: a restoration 'leaves nothing to imagine and hides the very history' it was meant to show. The correct answer holds both reasons and the consequence.",
   "Choosing the single-reason option because it paraphrases the most quotable sentence.",
   "V02N-ruins-aesthetic", "The narrow option is accurate as far as it goes; the reader must notice the second reason and the restoration point.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 013
ps("V02-N-013", LAN, "Slang ages fast because its insider function ends once outsiders adopt it.", "Easy",
   "Slang tends to age quickly, and the reason lies in what it is for. A slang word marks its users as insiders: to say it is to show that one belongs to a particular group, often a young one, and knows its current code. That function depends on outsiders not using the word. Once parents, advertisers and newsreaders adopt it, the word stops marking anyone as an insider, and the group that coined it drops it for something fresh. A few slang terms survive this process by losing their flavour entirely and becoming ordinary vocabulary, but most simply fade. The speed of slang's decline is, in this sense, a sign that it worked.",
   "Slang ages fast because it marks membership of a group, a role it loses once outsiders take it up; most terms then fade, though a few become ordinary words.",
   [("Slang words fade because advertisers and newsreaders deliberately adopt them in order to make young people abandon the private vocabulary of their group.",
     "The paragraph describes outsiders adopting slang, not doing so on purpose to drive young people away; the motive is invented."),
    ("Most of the ordinary words in a language began life as slang terms that young people once coined in order to mark themselves out as members of a particular group.",
     "The paragraph says only 'A few slang terms' become ordinary vocabulary while 'most simply fade', so this reverses the proportion."),
    ("Slang is a poor and short-lived form of speech, and its rapid decline shows that it fails to communicate as clearly as the ordinary vocabulary of a language does.",
     "The paragraph calls the speed of decline 'a sign that it worked', the opposite of treating it as a failure to communicate.")],
   "The paragraph explains slang's short life by its function: it 'marks its users as insiders', which 'depends on outsiders not using the word'. When outsiders adopt it, the group drops it; 'A few' terms become ordinary words but 'most simply fade'. The correct answer gives the function, the mechanism and the outcome with its exception.",
   "Reading quick decline as a sign of failure, missing the paragraph's closing reversal.",
   "V02N-slang-lifecycle", "The mechanism is stated plainly, and each wrong option contradicts a specific sentence.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 014
ps("V02-N-014", LAN, "Accent penalties mix prejudice with processing effort, and only the latter fades with exposure.", "Difficult",
   "Listeners asked to rate recorded speakers often judge those with certain accents as less competent, even when the words spoken are identical. It is tempting to read this as simple prejudice against particular regions or classes, and partly it is. But some of the effect has a duller source: listeners find an unfamiliar accent harder to process, and the extra effort of understanding is easily misattributed to the speaker, as if a message that was hard to follow had been less clearly thought. This matters because the two explanations call for different remedies. Prejudice must be confronted; mere unfamiliarity tends to shrink with exposure, so that a listener who hears an accent regularly may stop penalising it without ever having examined an attitude.",
   "Lower competence ratings for some accents come partly from prejudice and partly from the effort of processing unfamiliar speech, and the difference matters because only the latter may fade through exposure.",
   [("Listeners rate speakers with unfamiliar accents as less competent not out of prejudice but simply because such accents take more effort to understand and process.",
     "The paragraph says the effect is prejudice 'partly', and adds processing effort as a second source; denying prejudice altogether contradicts it."),
    ("Prejudice against regional and class accents can be overcome simply by hearing those accents regularly, without any need for listeners to examine their own attitudes.",
     "The paragraph assigns exposure to unfamiliarity and says 'Prejudice must be confronted'; this option merges the two causes it is careful to separate."),
    ("Because speakers with unfamiliar accents are harder to follow, listeners are justified in judging the messages of such speakers as less clearly thought out.",
     "The paragraph says the effort is 'misattributed to the speaker', which means the judgement is a mistake, not a justified inference.")],
   "The paragraph identifies two sources of the accent penalty, prejudice ('partly it is') and processing effort that is 'misattributed to the speaker', and stresses that they 'call for different remedies': prejudice 'must be confronted', while unfamiliarity 'tends to shrink with exposure'. The correct answer states both sources and why the distinction matters.",
   "Choosing the exposure option because exposure is the paragraph's remedy, without noticing that it is the remedy for only one cause.",
   "V02N-accent-competence-judgements", "Each wrong option collapses or misreads the two-cause distinction in a different way, and two of them are close to the paragraph's wording.",
   exams=HARD)

# ---------------------------------------------------------------- 015
ps("V02-N-015", LAN, "Reality television can construct characters in the edit, so the question is assembly, not scripting.", "Medium",
   "Defenders of reality television often say that nothing in it is scripted, and in a narrow sense they may be right: the participants choose their own words. But a programme is made in the edit as much as on location. Hundreds of hours of footage are cut to a few, and the choice of which glance to keep, which remark to place after which, and what music to lay underneath can turn an ordinary disagreement into a feud or a tired participant into a villain. No line need be invented for a character to be. The question to ask of such shows is therefore not whether they are scripted but how they are assembled, and that is a question their defenders rarely answer.",
   "Even if participants' words are unscripted, editing can manufacture characters and conflicts, so the real question about reality television is how it is assembled, not whether it is scripted.",
   [("Reality television is in fact secretly scripted, with participants handed lines to deliver so that their ordinary disagreements look like bitter and lasting feuds.",
     "The paragraph grants that 'the participants choose their own words'; its point is that no scripting is needed, since 'No line need be invented'."),
    ("Editors of reality television deliberately turn innocent participants into villains to win viewers, and such programmes should be required by law to disclose how all their footage was cut.",
     "The paragraph says editing 'can' create villains and asks a question of the shows; legal disclosure is an outside prescription and 'deliberately' is not claimed."),
    ("Because reality television uses only the words its participants actually spoke, its portrayal of them is broadly accurate, whatever music or editing is added.",
     "This adopts the defenders' reasoning that the paragraph rejects: selection, order and music can turn 'a tired participant into a villain'.")],
   "The paragraph concedes that participants 'choose their own words' but argues that 'a programme is made in the edit', where selection, order and music can create a feud or a villain. Hence the question is 'not whether they are scripted but how they are assembled'. The correct answer keeps the concession and the conclusion.",
   "Choosing the disclosure option because it sounds like a natural next step, though the paragraph proposes no rule.",
   "V02N-reality-tv-editing", "The prescriptive option shares the author's suspicion and must be rejected for adding a remedy and an intention.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 016
ps("V02-N-016", LAN, "Voice notes shift effort from the sender to the listener.", "Medium",
   "Voice notes sit awkwardly between a phone call and a text, and both their appeal and their irritation come from that position. For the sender, a voice note combines the ease of talking with the freedom of a text: there is no need to type, and no need to catch the other person at a convenient moment. For the receiver, the balance often tips the other way. A text can be skimmed in seconds, read during a meeting and searched later for an address; a voice note must be played through at the speaker's pace, in a place where one can listen, and cannot easily be scanned for the one detail that matters. The format, in short, moves effort from the person speaking to the person listening, which explains how the same person can enjoy sending voice notes and dread receiving them.",
   "Voice notes are easy for senders, who can talk whenever they like, but costly for receivers, who cannot skim or search them, so the format moves effort onto the listener.",
   [("Voice notes combine the best features of phone calls and text messages, which is why they have now become more popular than either of those older formats for everyday messaging between friends.",
     "The paragraph says the format combines advantages only 'For the sender' and is costly for the receiver; popularity compared with other formats is never discussed."),
    ("Text messages are better than voice notes because they can be skimmed, read during meetings and searched later, so voice notes are best avoided.",
     "The paragraph acknowledges the sender's real gains and gives no advice; this takes the receiver's side alone and adds a recommendation."),
    ("People who send voice notes are inconsiderate, since they force those who receive them to play long messages at the speaker's pace in inconvenient places.",
     "The paragraph describes a shift of effort built into the format, not a fault of character; the same person can 'enjoy sending' and 'dread receiving' them.")],
   "The paragraph contrasts the sender's ease ('no need to type', no need to find a convenient moment) with the receiver's costs (no skimming or searching, listening at 'the speaker's pace'), and sums up that the format 'moves effort from the person speaking to the person listening'. The correct answer states both sides and the summary.",
   "Choosing the option that condemns senders, which turns a description of the format into a moral judgement.",
   "V02N-voice-notes-effort", "The two one-sided wrong options are each half right and must be rejected for dropping the other half or adding a judgement.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 017
ps("V02-N-017", EDU, "Hand calculation taught a sense of size; with calculators, estimation must be taught deliberately.", "Medium",
   "The quarrel over calculators in primary classrooms is usually staged as a choice between fluency and drudgery: either children grind through long division by hand, or a machine frees them for real mathematics. Both camps miss what hand calculation was quietly teaching. A child who has worked many sums develops a sense of size, so that an answer of four thousand to a problem about the price of a school lunch looks absurd at once. That sense is what catches the mistyped digit, and a calculator, which never doubts itself, cannot supply it. The point is not that the machines should be banned, but that estimation must be taught on purpose once the drills that used to teach it by accident are gone.",
   "Hand calculation built a feel for the size of answers that catches errors, so if calculators replace the drills, estimation has to be taught deliberately rather than left to chance.",
   [("Calculators should be kept out of primary classrooms altogether, because only children who work long sums by hand ever develop the sense of size needed to catch their own mistakes.",
     "The paragraph says 'The point is not that the machines should be banned', and it proposes teaching estimation directly, so this contradicts it."),
    ("Calculators free children from the drudgery of long division and let them spend their time on the real mathematics that endless drills used to crowd out.",
     "This is one camp's position, which the paragraph says misses 'what hand calculation was quietly teaching'."),
    ("Children who rely on calculators make more errors than those who work sums by hand, because the machines frequently produce answers that are simply wrong.",
     "The paragraph's concern is mistyped input that a calculator 'never doubts', not machines that compute wrongly; the comparison of error rates is not made.")],
   "The paragraph sets aside both camps and identifies a by-product of hand calculation, a 'sense of size' that 'catches the mistyped digit'. Since a calculator 'cannot supply it', estimation 'must be taught on purpose' once the drills go, and the machines need not be banned. The correct answer captures this.",
   "Choosing the ban option because the paragraph praises hand calculation, overlooking the explicit rejection of a ban.",
   "V02N-calculators-estimation", "The ban option matches the paragraph's sympathy for hand work and is ruled out only by its final sentence.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 018
ps("V02-N-018", EDU, "Student ratings are poor overall verdicts but good reports of observable teaching conduct.", "Difficult",
   "Student ratings of teaching are often dismissed as popularity contests, and there is something in the charge: ratings tend to rise when courses are easier and grades kinder, and they can reflect a lecturer's charm as much as what students learn. Yet throwing the ratings out entirely would discard information that no one else possesses. Only students sit through every class; only they know whether the lecturer arrived prepared, returned work on time or answered questions clearly. The sensible course is to ask students about what they observed rather than what they judge. 'Were assignments returned within two weeks?' is a question they can answer reliably; 'Was this a good teacher?' invites them to rate something they are not well placed to assess.",
   "Student ratings are unreliable as overall verdicts on teaching, but students alone witness everyday classroom conduct, so surveys should ask what they observed rather than how good the teacher was.",
   [("Student ratings measure popularity rather than learning, since they rise for easy courses and charming lecturers, and so universities would do better to abandon them altogether.",
     "The paragraph grants 'something in the charge' but says abandoning ratings 'would discard information that no one else possesses'; this option takes the dismissal further than the author does."),
    ("Students are poor judges even of whether lecturers prepare well or return work on time, so their ratings should always be checked against regular classroom visits by experienced colleagues.",
     "The paragraph says such factual questions are ones 'they can answer reliably'; this reverses that claim and adds a remedy it never proposes."),
    ("Because only students sit through every class, their verdict on whether a lecturer is a good teacher is more reliable than the verdict of any other observer.",
     "The paragraph uses students' presence to support asking about observations, and says 'Was this a good teacher?' asks them to rate 'something they are not well placed to assess'.")],
   "The paragraph concedes the popularity charge, then argues that students uniquely possess information about what happened in class. It distinguishes observation from judgement: students can reliably report whether work was returned on time but are 'not well placed' to judge overall quality. The correct answer keeps the concession, the unique information and the observe-not-judge remedy.",
   "Choosing the 'only students sit through every class' option, which uses the paragraph's premise to reach the conclusion it explicitly denies.",
   "V02N-student-teaching-evaluations", "The third wrong option turns the author's premise into the very verdict the author rejects, so it can be eliminated only by the observation-versus-judgement distinction.",
   exams=HARD)

# ---------------------------------------------------------------- 019
ps("V02-N-019", EDU, "Recorded lectures serve mainly as a reference to consult, not a substitute for attending.", "Easy",
   "When universities began recording lectures and posting them online, many lecturers feared that their halls would empty, and in some courses attendance did fall. Yet the way students tend to use the recordings is easy to overlook. They seldom sit through a whole lecture a second time; instead they return to the stretch that confused them, pause on a derivation, or replay a definition on the night before an examination. For a student who missed a class through illness or a part-time job, the recording is a lifeline. The loss of attendance is real, and a lecture watched alone offers no chance to put up a hand and ask. But the recordings mostly serve as a reference to be consulted rather than a substitute for being there.",
   "Recorded lectures may cut attendance somewhat, but students mostly use them to revisit hard passages or catch up on missed classes, as a reference rather than a replacement.",
   [("Recorded lectures have largely emptied university halls, since students now prefer to watch at home, where they can pause and replay every lecture whenever they like.",
     "The paragraph says attendance fell only 'in some courses' and that recordings are rarely watched in full; 'largely emptied' contradicts its conclusion."),
    ("Students who rely on recorded lectures learn more than those who attend in person, because they can pause on a derivation and replay a definition before an examination.",
     "The paragraph compares no learning outcomes, and it notes a cost of watching alone, the lack of any 'chance to put up a hand and ask'."),
    ("For students who miss a class because of illness or a part-time job, a recording of the lecture is the only way of keeping up with the course.",
     "This takes one detail and adds 'the only way'; it omits the paragraph's main point about how recordings are generally used.")],
   "The paragraph grants a real 'loss of attendance' but says students 'seldom sit through a whole lecture' again; they revisit confusing parts or catch up after missing a class. It concludes that recordings 'mostly serve as a reference to be consulted rather than a substitute for being there'. The correct answer keeps the concession and the conclusion.",
   "Taking the lecturers' fear as the paragraph's verdict, or choosing the detail about absent students.",
   "V02N-recorded-lectures-attendance", "The conclusion is stated in the last sentence, and each wrong option is plainly extreme, unsupported or narrow.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 020
ps("V02-N-020", EDU, "Reading aloud still serves fluent adolescents, by making demanding texts accessible.", "Medium",
   "Reading aloud is usually treated as something adults do for small children and stop once the children can read for themselves. That timing assumes that the only purpose of listening to a story is to gain access to words one cannot yet decode. But a teenager who reads fluently still gains from hearing a skilled reader. Spoken aloud, a difficult text arrives with its phrasing, pauses and emphasis already worked out, so that sentences which would stall a silent reader become easy to follow, and the listener meets books a little beyond what they would attempt alone. Reading aloud to older pupils is therefore not a step backwards. It serves a different purpose from the bedtime story, and that purpose does not expire once decoding is mastered.",
   "Reading aloud still helps adolescents who read fluently, because a skilled performance makes demanding texts accessible, a purpose quite separate from helping young children decode words.",
   [("Teenagers who are read to aloud fall behind in reading on their own, since hearing texts spoken stops them from learning to work through difficult sentences unaided.",
     "The paragraph presents listening as a benefit to fluent readers and says it is 'not a step backwards'; no harm to independent reading is suggested."),
    ("Reading aloud is mainly a way of helping children who cannot yet decode words, and adults are right to stop doing it once children can read by themselves.",
     "This is the assumption the paragraph criticises when it says the usual timing assumes decoding is 'the only purpose' of listening."),
    ("Secondary teachers should replace most silent reading with reading aloud, since pupils understand far more of a text when they hear it than when they read it.",
     "The paragraph argues that reading aloud keeps a purpose for older pupils; replacing silent reading and the 'far more' comparison are outside it.")],
   "The paragraph rejects the assumption that reading aloud serves only decoding, and argues that for a fluent teenager a skilled reading supplies 'phrasing, pauses and emphasis', making harder books followable. Its conclusion is that this purpose 'does not expire once decoding is mastered'. The correct answer states the claim and its reason.",
   "Choosing the replacement option, which overstates the paragraph's modest case into a classroom policy.",
   "V02N-reading-aloud-adolescents", "The prescriptive option sounds like a natural extension and must be rejected for overreach.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 021
ps("V02-N-021", HEA, "Fever is mainly a defence, so in healthy adults lowering it is chiefly for comfort.", "Medium",
   "It is natural to treat a fever as the illness itself and to bring it down as quickly as possible. Yet fever is in large part a response that the body mounts against infection, and a raised temperature can make conditions harder for some invading organisms while speeding parts of the immune response. This does not mean that fevers should be left alone. Very high temperatures can be dangerous, and in young children, the elderly or people with heart disease the strain of a fever may matter more than any benefit it brings. For most otherwise healthy adults, though, the main reason to take a fever-reducing drug is comfort, and it is worth knowing that one is treating a sign of the fight rather than the enemy.",
   "Fever is largely the body's defence against infection rather than the illness, so although it sometimes needs lowering, bringing it down in healthy adults mainly relieves discomfort.",
   [("Because fever helps the body fight infection, people should avoid fever-reducing drugs altogether and simply let a raised temperature run its full course in almost every case of illness.",
     "The paragraph says 'This does not mean that fevers should be left alone' and names cases where lowering matters, so this contradicts it."),
    ("Fever-reducing drugs are dangerous for young children, the elderly and people with heart disease, who should therefore have their fevers treated by other means.",
     "The paragraph says the strain of the fever itself may matter most for these groups; it says nothing about the drugs being dangerous to them."),
    ("Because a raised temperature speeds the immune response, people who run high fevers tend to recover faster than those whose temperatures stay near normal.",
     "The paragraph says fever speeds 'parts of the immune response' and warns that very high temperatures 'can be dangerous'; a faster recovery is never claimed.")],
   "The paragraph corrects the view of fever as 'the illness itself': it is largely a defensive response. It then qualifies ('This does not mean that fevers should be left alone') for very high fevers and vulnerable groups, and concludes that for healthy adults lowering a fever is mainly for 'comfort'. The correct answer keeps the claim, the qualification and the conclusion.",
   "Misreading the vulnerable groups sentence as a warning about the drugs rather than about the fever.",
   "V02N-fever-suppression", "One wrong option reverses the subject of a qualifying sentence, which needs careful reading to catch.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 022
ps("V02-N-022", HEA, "Pain scores track change within a patient but mislead when compared across patients or used as targets.", "Difficult",
   "Asking patients to rate their pain from zero to ten seems a sensible way of bringing a private experience into the clinic, and as a way of following one patient over time it often works: a drop from eight to four after a drug means something. The trouble begins when the numbers are compared across people or treated as targets. One patient's six is another's three, shaped by temperament, culture and past experience of pain, and a ward that aims to bring every score below a set threshold may end up dosing the number rather than the person. The scale is a ruler each patient carries privately; it can measure change in the one who holds it, but it was never calibrated against anyone else's.",
   "A zero-to-ten pain rating can track change within one patient, but since each person's scale is private, comparing scores across patients or using them as targets misleads.",
   [("Numeric pain scales are unreliable because patients rate pain according to temperament and culture, so clinicians should trust their own judgement of how much pain a patient feels.",
     "The paragraph says the scale 'often works' for following one patient, and it never recommends relying on the clinician's judgement instead."),
    ("Because pain is a private experience, no number a patient reports can tell a clinician anything meaningful, not even how that patient's own pain has changed.",
     "The paragraph says 'a drop from eight to four after a drug means something', so the scale does measure change within a patient."),
    ("Wards that aim to bring every pain score below a fixed level tend to overprescribe painkillers, because patients exaggerate their scores in order to receive more.",
     "The paragraph's warning is that a ward may treat 'the number rather than the person' because scales differ between people; it never says patients exaggerate.")],
   "The paragraph grants that the scale works 'as a way of following one patient over time' and locates the problem in comparing 'across people' or treating scores 'as targets', because each scale is 'a ruler each patient carries privately'. The correct answer keeps both the valid use and the two misuses with their reason.",
   "Choosing the option that blames temperament and culture and tells clinicians to trust their own judgement, which keeps the paragraph's reasons for doubt but discards its endorsement of within-patient tracking.",
   "V02N-pain-rating-scales", "All wrong options build on real phrases; the correct answer depends on holding the within-patient versus across-patient distinction.",
   exams=HARD)

# ---------------------------------------------------------------- 023
ps("V02-N-023", HEA, "A surrogate endpoint's reliability belongs to its link with outcomes, which each new drug type must re-establish.", "Difficult",
   "Drug trials often measure a surrogate, such as blood pressure or a level in the blood, instead of the outcome patients care about, such as living longer or avoiding a stroke. The practice is defensible: real outcomes may take years to appear, and a surrogate that reliably tracks them lets useful drugs reach patients sooner. But the reliability is a property of the link, not of the marker. A drug may improve the number by a route that has nothing to do with the disease, or improve it while causing harm elsewhere, so that a marker which tracked outcomes well for one class of drugs misleads for another. A surrogate is a promise made by past evidence about one mechanism, and each new kind of treatment has to earn the right to rely on it.",
   "Surrogate markers can legitimately speed trials, but since their link to real outcomes holds only for particular mechanisms, a new kind of drug that improves a marker cannot be assumed to help.",
   [("Drug trials should measure only the outcomes patients actually care about, such as survival, since markers like blood pressure have proved too unreliable to use.",
     "The paragraph calls the practice 'defensible' and says reliable surrogates let 'useful drugs reach patients sooner'; it does not reject surrogates."),
    ("Surrogate markers are acceptable in drug trials only when the real outcomes they stand for would take many years to appear and when patients urgently need new treatments for a serious disease.",
     "Delay is a reason the paragraph gives for using surrogates, but its condition for trusting one is a link established for the drug's mechanism, which this option leaves out."),
    ("Drugs that improve surrogate markers usually cause harm elsewhere in the body, which is why their apparent benefits so often fail to show up in real outcomes.",
     "The paragraph says a drug 'may' improve the number while causing harm; 'usually' and 'so often' turn a possibility into a general rule.")],
   "The paragraph defends surrogates in principle, then argues that 'the reliability is a property of the link, not of the marker': a marker valid for one class of drugs may mislead for another, so 'each new kind of treatment has to earn the right to rely on it'. The correct answer keeps the defence and the mechanism-specific limit.",
   "Choosing the delay-and-urgency option because delay is the paragraph's stated justification, confusing a reason for using surrogates with the condition for trusting one.",
   "V02N-surrogate-endpoints", "The second wrong option is built from the paragraph's own justification and is wrong only because it substitutes the wrong condition.",
   exams=HARD)

# ---------------------------------------------------------------- 024
ps("V02-N-024", HEA, "Video and clinic consultations suit different encounters; neither simply replaces the other.", "Easy",
   "A video consultation and a visit to the clinic are often compared as if one simply replaced the other, but each suits different needs. For a follow-up on a known condition, a review of test results or a question about medication, the video call saves the patient a journey and a waiting room, and loses little. For a new symptom, the screen is a poorer instrument: a doctor cannot press an abdomen, listen to a chest or notice the small signs a patient does not think to mention. The useful question is therefore not which format is better, but which encounters each one serves well.",
   "Video calls suit routine follow-ups and clinic visits suit new symptoms needing examination, so the real question is which encounters each format serves, not which is better.",
   [("Video consultations are more convenient than clinic visits in every respect and will in time replace face-to-face care for almost all patients, whatever their condition or symptoms.",
     "The paragraph says the screen is 'a poorer instrument' for new symptoms, so 'every respect' and near-total replacement contradict it."),
    ("Doctors cannot examine patients properly over a video link, so video consultations are an unsafe substitute for the clinic and should generally be avoided.",
     "The paragraph says video 'loses little' for follow-ups and test results; it limits video's role rather than rejecting it."),
    ("During a video call a doctor cannot press an abdomen or listen to a chest, and may miss small signs that a patient does not think to mention.",
     "This repeats one detail about new symptoms and leaves out the paragraph's main point that each format suits different encounters.")],
   "The paragraph matches each format to its use: video for follow-ups, results and medication questions, where it 'loses little', the clinic for new symptoms that need examination. It concludes that the question is 'which encounters each one serves well'. The correct answer states the division and the conclusion.",
   "Choosing the detail about physical examination, which supports only half of the comparison.",
   "V02N-telemedicine-consultations", "The comparison and conclusion are explicit, and the wrong options are clearly extreme or narrow.",
   cognitive="Understanding")

# ---------------------------------------------------------------- 025
ps("V02-N-025", HEA, "Guidelines beat unaided judgement for typical patients, but applying them needs judgement of fit.", "Medium",
   "Clinical guidelines are sometimes resented as cookbook medicine, a set of rules that turns the doctor into a technician. The resentment misunderstands what a good guideline is. It condenses the evidence on how a typical patient with a given condition fares under different treatments, and for that typical patient it will usually beat the unaided judgement of a busy clinician. But no patient is exactly typical. A guideline drawn from trials that excluded the very old, or people with several illnesses at once, says little about the frail patient with four conditions in the consulting room. Following it there is not rigour but a misreading of its scope. The skill that guidelines demand is knowing when a patient falls inside them.",
   "Guidelines distil evidence that usually serves typical patients better than unaided judgement, but they must be applied with care over whether a given patient resembles those the evidence covered.",
   [("Clinical guidelines reduce doctors to technicians following rules, and good doctors should rely on their own judgement rather than on summaries of trial evidence.",
     "This is the resentment the paragraph says 'misunderstands what a good guideline is'; the author holds that guidelines usually beat unaided judgement."),
    ("Guidelines are useless for elderly patients and for those with several illnesses, who should never be treated according to the evidence from clinical trials.",
     "The paragraph says a guideline drawn from trials that excluded such patients 'says little' about them; it does not call guidelines useless for all elderly patients or reject trial evidence."),
    ("Because no patient is exactly typical, doctors should treat clinical guidelines only as rough suggestions and depart from them whenever their own judgement of a case happens to differ.",
     "The paragraph says guidelines usually beat a clinician's unaided judgement; departing whenever judgement differs ignores that and the stated test of whether the patient 'falls inside them'.")],
   "The paragraph rejects the 'cookbook medicine' charge: guidelines condense evidence that 'will usually beat the unaided judgement' for typical patients. It then qualifies: 'no patient is exactly typical', and applying a guideline outside its evidence is 'a misreading of its scope'. The correct answer keeps both the value and the condition.",
   "Choosing the 'rough suggestions' option, which takes the qualification so far that it cancels the paragraph's main claim.",
   "V02N-clinical-practice-guidelines", "The 'rough suggestions' option begins with the paragraph's own words and must be rejected for overextending the qualification.",
   cognitive="Understanding")
