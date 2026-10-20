import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DX = ("CAT", "XAT")

# 001 Education, argument, Medium
ps("V02-J-001", "Education", "Age-graded classes rest on a false premise, and mixed-age classes justify training teachers for them.", "Medium",
   "Schools sort children by year of birth so routinely that the practice seems like a law of nature rather than an administrative convenience. Yet grouping by age assumes that children born within the same twelve months are ready for the same material at the same moment, an assumption that every experienced teacher knows to be false. In classrooms that deliberately mix ages, the older children consolidate what they know by explaining it, and the younger ones see, in the work of those just ahead of them, what the next step looks like. None of this makes mixed-age teaching easy: it demands careful planning and a teacher able to manage several levels at once, and without these it can fail badly. But that difficulty is a reason to prepare teachers for the task, not a reason to treat the age-graded class as the only sensible arrangement.",
   "Sorting pupils by age rests on a convenient but false premise; mixed-age classes bring real benefits, and their demands call for trained teachers rather than rejection.",
   [("Older pupils in a mixed-age class gain more than younger ones, since explaining material to others is the surest way of consolidating one's own understanding of it.",
     "The paragraph names benefits for the younger children as well ('see ... what the next step looks like') and never ranks the two groups; it also leaves out the central claim about age grading."),
    ("Schools should abolish grouping by birth year and adopt mixed-age classes everywhere, since every teacher knows that children of one age differ in readiness.",
     "The paragraph concedes that mixed-age teaching 'can fail badly' and argues only against treating the age-graded class as 'the only sensible arrangement'; it never calls for abolition everywhere."),
    ("Mixed-age teaching usually fails because teachers cannot manage several levels at once, which is why schools still sort their pupils by year of birth.",
     "The paragraph says such teaching fails only without planning and skilled teachers, and it attributes age sorting to 'administrative convenience', not to the failure of mixed-age classes.")],
   "The paragraph attacks the assumption behind age grading, gives the benefits of mixing ages, concedes the difficulty, and concludes that the difficulty calls for preparing teachers rather than abandoning the idea. The correct summary keeps the critique, the benefit, the concession and the conclusion.",
   "Picking the option that turns the argument into a call for abolition, missing the concession that mixed-age teaching can fail.",
   "V02J-mixed-age-classrooms", "The prescriptive distractor overstates a moderate conclusion and must be rejected on degree.",
   cognitive="Analysis")

# 002 Education, finding and qualification, Medium
ps("V02-J-002", "Education", "Evidence of holiday learning loss has been tempered by measurement concerns.", "Medium",
   "Comparisons of test scores taken at the end of one school year and the start of the next have often suggested that children lose ground over the long holiday, and that children from poorer homes lose more. The finding has been used to argue that much of the gap between richer and poorer pupils opens not in school but outside it. Later work has complicated the picture. Some of the apparent loss depends on which tests are used and how their scores are scaled, and some estimates shrink considerably when the same children are measured in a different way. What survives scrutiny is more modest: holiday loss is real for some children, but it is smaller and less consistent than first reported, so it cannot by itself account for the gap, even if the long break remains a time when unequal home resources count for more than usual.",
   "Early evidence that long holidays widen the gap between richer and poorer pupils has been tempered by measurement concerns, leaving a smaller, less uniform effect that cannot alone explain it.",
   [("The idea that children lose learning over the long holidays has been shown to be an artefact of test scaling, so the long break has no effect whatever on the gap between richer and poorer pupils.",
     "The paragraph says holiday loss 'is real for some children' and that the break is a time when home resources 'count for more'; it denies only that the loss explains the gap by itself."),
    ("Because most of the gap between richer and poorer pupils opens outside school, schools ought to shorten the long holiday to protect children from poorer homes.",
     "This repeats the earlier argument that later work 'complicated', and it adds a prescription about shortening holidays that the paragraph never makes."),
    ("Test scores taken at the start and end of school years are unreliable, and research on education should stop using them to compare different groups of pupils.",
     "The paragraph says only that some estimates depend on test choice and scaling; it neither condemns such scores in general nor recommends abandoning them.")],
   "The paragraph reports a finding, notes the use made of it, then qualifies it: the loss is real for some but smaller and less consistent, so it cannot alone explain the gap. The correct summary states the finding and the qualification with its scope.",
   "Choosing the option that turns 'smaller and less consistent' into no effect at all.",
   "V02J-summer-learning-loss", "The extreme distractor reuses the measurement point; the reader must notice that the loss is qualified, not denied.",
   cognitive="Understanding")

# 003 Education, critique of a view, Difficult
ps("V02-J-003", "Education", "Rewriting textbooks to improve readability scores can remove the links that comprehension needs.", "Difficult",
   "A familiar remedy for textbooks that students find hard is to rewrite them in shorter sentences with commoner words, guided by formulas that score a text by the length of its words and sentences. The formulas do measure something, but what makes a passage hard to understand is often not its vocabulary so much as the gaps it leaves for the reader to fill. Cutting one long sentence into three short ones frequently removes the very words, such as because, although and therefore, that told the reader how the ideas were related; the result scores as easier and is harder to follow. None of this means that dense prose is a virtue or that difficult words never obstruct learning. It means that a readability score measures surface features, and a text revised to improve its score can lose the connective tissue on which comprehension depends.",
   "Revising textbooks to raise readability scores can backfire, because the scores track surface features, and shortening sentences may strip out the links between ideas that understanding needs.",
   [("Readability formulas are worthless guides for textbook writers, since the length of the words and sentences in a passage has no bearing at all on how easily students can understand what it says.",
     "The paragraph says the formulas 'do measure something' and concedes that 'difficult words' can 'obstruct learning', so calling them worthless contradicts it."),
    ("Textbooks should be written in long and complex sentences, since students learn more from dense prose that forces them to work out the meaning for themselves.",
     "The paragraph explicitly denies that 'dense prose is a virtue'; its point concerns lost connectives, not the value of difficulty."),
    ("Short sentences make textbooks harder to follow than long ones, so formulas that reward brevity measure the opposite of what makes a text truly difficult.",
     "The paragraph says splitting sentences 'frequently' removes connectives, not that short sentences are always harder, and it grants that the formulas 'do measure something', not the opposite of difficulty.")],
   "The paragraph criticises the readability-formula remedy: the formulas capture surface features, and splitting sentences can delete the connectives that show how ideas relate, so a text can score as easier yet be harder to follow. The concession keeps the claim from becoming a defence of dense prose. The correct summary keeps the mechanism and the hedge 'can'.",
   "Choosing the option that inverts the formulas wholesale, missing that the paragraph says they 'do measure something' and that the harm is frequent, not universal.",
   "V02J-simplified-textbook-readability", "Two distractors sit close to the author's critique and fail only on degree ('opposite', 'worthless') against the paragraph's concessions.",
   cognitive="Analysis", exams=DX)

# 004 Education, finding and qualification, Easy
ps("V02-J-004", "Education", "Teacher expectations affect pupils, but modestly and unevenly.", "Easy",
   "It is widely believed that a teacher's expectations can shape how well pupils perform: tell a teacher that certain children are about to blossom, and they will. There is evidence that expectations matter, since teachers who expect more of a pupil may give that pupil more attention, more time to answer questions and more demanding work. But the effects found in careful studies are usually modest, and they tend to be larger for younger children and for pupils whom the teacher does not yet know well. Expectations, in other words, are one influence among many, not a force that can by itself transform a child's results.",
   "Teachers' expectations do affect pupils' performance, through how teachers treat them, but the effect is usually modest and uneven rather than transformative.",
   [("Telling teachers that certain children are about to blossom reliably causes those children to perform far better than the rest of their classmates.",
     "This is the popular belief the paragraph opens with and then qualifies; careful studies find effects that are 'usually modest', not reliable large gains."),
    ("Teachers' expectations have no real effect on how pupils perform, since careful studies have failed to find any difference in their results.",
     "The paragraph says there 'is evidence that expectations matter' and that the effects are modest, not absent."),
    ("Younger children need more attention and more demanding work than older pupils, because they are more easily influenced by what their teachers expect.",
     "The paragraph says only that expectation effects are larger for younger children; it says nothing about what younger children need, so this distorts a detail.")],
   "The paragraph grants that expectations matter through how teachers treat pupils, then limits the claim: effects are modest, larger in some groups, and one influence among many. The correct summary gives the effect and its limits.",
   "Accepting the popular opening claim as the paragraph's own conclusion.",
   "V02J-teacher-expectation-effects", "The qualification is stated directly in the last two sentences.",
   cognitive="Understanding")

# 005 Health, argument, Medium
ps("V02-J-005", "Health and medicine", "Improvement after surgery needs sham-controlled trials to show the procedure itself works.", "Medium",
   "It seems obvious that an operation cannot work by suggestion: the knife either repairs the tissue or it does not. For this reason, many surgical procedures entered routine use on the strength of surgeons' observations that their patients felt better afterwards. But patients who undergo surgery also receive attention, hope and a period of rest, and their symptoms often fluctuate and improve on their own. When some procedures have been tested against sham operations, in which patients are anaesthetised and given an incision but the key step is omitted, the improvement in the two groups has turned out to be similar. Such trials raise real ethical questions, since the sham group bears risk without the prospect of direct benefit. Yet without them, it is hard to know whether an operation helps because of what the surgeon does or because of everything that surrounds it.",
   "Improvement after surgery does not prove an operation works, since hope and natural recovery also play a part; sham-controlled trials, though ethically fraught, are needed to separate them.",
   [("Most surgical procedures now in routine use are no better than sham operations, and each of them should be withdrawn from practice until it has been properly tested against a placebo operation.",
     "The paragraph reports similar results only for 'some procedures' and makes no call for withdrawal; 'most' and the prescription go beyond it."),
    ("Sham surgery is unethical because patients in the control group bear the risks of an operation without any prospect of benefiting from it directly.",
     "The paragraph raises this as a concession ('real ethical questions') and then answers it with 'Yet without them'; making it the conclusion reverses the argument."),
    ("Surgery works mainly through suggestion, since the attention and hope that patients receive matter more than the repair the surgeon actually performs.",
     "The paragraph says it is 'hard to know' which factor helps; it does not claim that suggestion is the main mechanism.")],
   "The paragraph argues that post-operative improvement is not proof of effect because attention, hope and natural recovery also contribute, and that sham-controlled trials, despite their ethical cost, are needed to tell these apart. The correct summary states this with the concession.",
   "Taking the ethical concession as the paragraph's conclusion, overlooking the 'Yet' that answers it.",
   "V02J-sham-surgery-controls", "One distractor is a concession the paragraph raises and answers; the reader must follow the turn at 'Yet'.",
   cognitive="Analysis")

# 006 Health, critique of a view, Difficult
ps("V02-J-006", "Health and medicine", "Systematic misreporting in diet surveys can create or hide associations, and big samples do not cure it.", "Difficult",
   "Much of what is believed about diet and health rests on asking people what they eat. The objection usually raised against such surveys is that people forget, and forgetting, being random, merely adds noise. The deeper difficulty is that the errors are not random. People tend to under-report foods they regard as unhealthy and over-report those they think virtuous, and the size of the distortion varies with body weight, with education and with how much a person cares about appearing healthy. Since those same characteristics are themselves linked to health, the error can manufacture associations or hide real ones, rather than simply blurring them. This does not make dietary surveys useless; for some questions they are the only practical source. But it means that a large sample, which cures random error, offers no protection against this kind.",
   "Diet surveys suffer from systematic, not random, misreporting tied to traits that also affect health, so the errors can create or hide associations that large samples cannot remove.",
   [("Diet surveys are unreliable mainly because people forget what they have eaten, which is an error that larger samples can correct but that researchers seldom trouble to address properly.",
     "Forgetting is the 'usual' objection that the paragraph sets aside for 'The deeper difficulty' of non-random error; the claim about researchers is also unsupported."),
    ("Because people misreport their diets, dietary surveys are useless for health research and ought to be replaced by direct measurement of what people actually eat.",
     "The paragraph states that this 'does not make dietary surveys useless' and that for some questions they are 'the only practical source'."),
    ("People who care about appearing healthy are healthier than others, which is why diet surveys consistently overstate the benefits of foods regarded as virtuous.",
     "The paragraph says the error 'can manufacture associations or hide real ones', not that it consistently inflates benefits, and it never says image-conscious people are healthier.")],
   "The paragraph sets aside the familiar objection (random forgetting) for a deeper one: misreporting is systematic and tied to traits that also bear on health, so it can create or mask associations, and large samples do not help. The concession limits the claim. The correct summary captures the contrast, the mechanism and the point about samples.",
   "Choosing the option built on forgetting, which is the objection the paragraph calls less important.",
   "V02J-self-reported-diet-surveys", "The tempting distractor states the familiar objection the author demotes; separating random from systematic error needs the whole argument.",
   cognitive="Analysis", exams=DX)

# 007 Health, finding and qualification, Easy
ps("V02-J-007", "Health and medicine", "Loneliness is linked with early death, but the link is not proven to be causal.", "Easy",
   "Studies that follow people over many years have found that those who report feeling lonely or socially isolated tend to die earlier than those who do not, and the association has led some to describe loneliness as a threat to public health. The finding is consistent and worth taking seriously. It is not, however, a simple demonstration that loneliness causes illness. People who are already unwell may withdraw from others, and poverty or disability can produce both isolation and poor health. Researchers try to adjust for such factors, but the most that can be said with confidence is that loneliness and early death travel together, and that loneliness may contribute to it.",
   "Loneliness is consistently linked with earlier death, but since illness or poverty may produce both, the link does not show that loneliness itself causes ill health.",
   [("Loneliness directly causes illness and early death, and it should therefore be treated by governments as a threat to public health quite as serious as smoking.",
     "The paragraph denies that the finding is 'a simple demonstration that loneliness causes illness', and the comparison with smoking comes from outside it."),
    ("The link between loneliness and early death is unreliable, since studies that follow people over many years cannot take account of poverty or disability.",
     "The paragraph calls the finding 'consistent' and says researchers 'try to adjust for such factors'; it questions the causal reading, not the link."),
    ("People who are already unwell tend to withdraw from friends and family, which explains why the sick are more often lonely than the healthy.",
     "This takes one of the alternative explanations as the whole point and omits the main finding and its qualification.")],
   "The paragraph accepts a consistent association between loneliness and early death but warns that illness, poverty or disability could produce both, so causation is not established. The correct summary keeps both halves.",
   "Treating a qualified association as proof of cause.",
   "V02J-loneliness-mortality-risk", "The paragraph states its qualification plainly with 'It is not, however'.",
   cognitive="Understanding")

# 008 Health, explanation of a phenomenon, Medium
ps("V02-J-008", "Health and medicine", "Observed hand-hygiene audits measure behaviour under observation, not ordinary behaviour.", "Medium",
   "Hospitals that check whether staff clean their hands by sending observers onto the wards routinely record high rates of compliance. The rates are less impressive than they look. Staff who notice an observer wash more often while the observer is present, so the audit measures behaviour under observation, which is precisely the condition that does not hold for most of a working day. Where observed rates have been compared with counts from electronic dispensers or with unannounced checks, the observed rates have often turned out considerably higher. The point is not that staff are dishonest, nor that audits are pointless, since being watched does improve hand hygiene for a time. It is that a measure which changes the behaviour it measures cannot tell us how people behave when no one is looking.",
   "Observed audits overstate routine hand-washing because staff act differently when watched, so although observation briefly improves hygiene, it cannot reveal ordinary behaviour.",
   [("Hospital staff deliberately exaggerate their hand-washing during audits, so observed audits should be replaced entirely by electronic counts from dispensers.",
     "The paragraph says the point is 'not that staff are dishonest' and that audits are not 'pointless'; it recommends no replacement."),
    ("Sending observers onto hospital wards is the most effective way to improve hand hygiene, because staff wash their hands far more often whenever they know that they are being watched.",
     "The paragraph says observation improves hygiene only 'for a time' and never compares methods; its point is about what the audit can measure."),
    ("Electronic dispensers and unannounced checks give hospitals a fully accurate picture of how often staff really clean their hands during a working day.",
     "The paragraph uses these only as comparisons that showed the observed rates to be higher; it makes no claim that they are fully accurate.")],
   "The paragraph explains why observed compliance figures are inflated: observation itself changes behaviour, so the audit samples an unusual condition. It concedes that watching helps for a while. The correct summary gives the mechanism, the concession and the conclusion.",
   "Reading the inflated figures as evidence of dishonesty, which the paragraph explicitly rules out.",
   "V02J-observed-hand-washing", "The distractors each misread one concession; the key must keep both the effect and its limit.",
   cognitive="Understanding")

# 009 Cities, comparison, Medium
ps("V02-J-009", "Cities and geography", "Cul-de-sacs give residents quiet but push the costs of distance and traffic elsewhere.", "Medium",
   "Two ideas of the residential street compete in suburban planning. The grid connects every street to several others, so drivers and walkers can take many routes and no single road carries the whole load. The cul-de-sac layout, with its looping roads and dead ends, keeps through traffic out, and residents of the closed streets often value the quiet and the safety of children playing outside. The difficulty is that the quiet is bought with distance: a shop a few hundred metres away as the crow flies may be more than a kilometre away by road, so residents drive for trips they might have walked, and the few roads that connect the loops carry heavy traffic. Each layout serves something real; the cul-de-sac simply moves its costs out of sight of those who enjoy its benefits.",
   "Cul-de-sacs give residents real quiet and safety, but unlike grids they lengthen trips and concentrate traffic on connecting roads, costs its beneficiaries tend not to see.",
   [("Grid layouts are superior to cul-de-sacs in every respect, since they let walkers and drivers take many different routes and spread the load of traffic across all the streets.",
     "The paragraph says each layout 'serves something real' and grants the cul-de-sac's quiet and safety, so 'in every respect' contradicts it."),
    ("Residents prefer cul-de-sacs because children can play safely in quiet streets, which explains why the layout has spread so widely in suburban planning.",
     "The paragraph mentions what residents value but says nothing about why the layout spread, and it omits the central point about displaced costs."),
    ("Residents of cul-de-sacs walk to nearby shops more often than residents of grids, because the absence of through traffic makes walking safer and pleasanter.",
     "The paragraph says the opposite: longer road distances mean residents 'drive for trips they might have walked'.")],
   "The paragraph compares the two layouts, grants the cul-de-sac its benefits, and argues that those benefits are paid for in longer trips and heavy traffic on connecting roads, costs borne out of residents' sight. The correct summary keeps the comparison and the shifted costs.",
   "Choosing the option that declares the grid better in every way, ignoring that each layout 'serves something real'.",
   "V02J-cul-de-sac-street-layouts", "The extreme distractor matches the author's leaning, so it must be rejected on degree.",
   cognitive="Analysis")

# 010 Cities, explanation of a phenomenon, Easy
ps("V02-J-010", "Cities and geography", "Paved surfaces cause floods by sending rain to rivers quickly.", "Easy",
   "When rain falls on a field or a forest, much of the water soaks into the soil, and what runs off reaches the streams slowly. When the same rain falls on roofs, roads and car parks, almost none of it soaks in; it is gathered by gutters and drains and delivered to the river within minutes. A city can therefore flood after a storm that would have caused no trouble before the land was built on, not because more rain falls but because the rain reaches the river all at once. Wider drains can carry more water away, but they also speed its journey, which is why some cities now try to slow runoff with green roofs, permeable paving and ponds.",
   "Paved surfaces can cause urban floods by sending rain to rivers within minutes instead of letting it soak in, so some cities now try to slow runoff.",
   [("Cities flood more often than the countryside because building on land changes the local weather and causes heavier storms to fall over urban areas.",
     "The paragraph says floods happen 'not because more rain falls' but because water reaches the river all at once."),
    ("Wider drains are the most reliable way to protect a city from flooding, since they carry larger volumes of water away from its streets and car parks.",
     "The paragraph notes that wider drains 'also speed its journey', which is the problem; that is why some cities try to slow runoff instead."),
    ("Green roofs, permeable paving and ponds have now replaced conventional drains in most cities that suffer from repeated flooding after heavy storms.",
     "The paragraph says only that 'some cities now try' these methods; 'replaced' and 'most cities' overstate it, and the option omits the cause of flooding.")],
   "The paragraph explains that hard surfaces deliver rain to rivers in minutes rather than letting it soak in, so cities can flood without more rain; faster drains worsen the speed problem, hence efforts to slow runoff. The correct summary gives the cause and the response.",
   "Assuming urban floods mean more rain, which the paragraph rules out.",
   "V02J-paved-surfaces-urban-flooding", "The cause is stated directly and each distractor contradicts or overstates a plain sentence.",
   cognitive="Understanding")

# 011 Cities, finding and qualification, Difficult
ps("V02-J-011", "Cities and geography", "Lower cycling risk where cycling is common may reflect safety attracting cyclists, not numbers alone.", "Difficult",
   "In places where many people cycle, the risk of injury for each cyclist tends to be lower than in places where few do. This pattern is often read as proof that drivers become more careful when cyclists are common, so that simply encouraging more cycling will make it safer. The pattern is real, but the causal story may run partly the other way. Cities that have built protected lanes and calmed their traffic attract more cyclists precisely because cycling there is already safer, and more cautious people take up cycling only when it feels safe. Driver adaptation may contribute as well; nobody needs to deny it. What the pattern does not support is the hope that numbers alone, without the infrastructure that draws them, will deliver safety.",
   "Lower injury risk where cycling is common may partly reflect safer streets attracting cyclists, not only numbers creating safety, so numbers alone cannot be relied on to cut risk.",
   [("Drivers become more careful when cyclists are common, so cities can make cycling safer simply by persuading many more people to take it up, whatever their streets happen to be like.",
     "This is the reading the paragraph reports and then disputes; it ends by rejecting 'the hope that numbers alone ... will deliver safety'."),
    ("The lower injury risk in cities with many cyclists is an illusion, produced by the fact that only cautious people choose to cycle in such places.",
     "The paragraph says the 'pattern is real'; it questions the direction of cause, and cautious riders are only one part of its account."),
    ("Protected lanes and calmer traffic, rather than any change in driver behaviour, fully explain why cycling is safer in cities where many people cycle.",
     "The paragraph grants that driver adaptation 'may contribute as well', so claiming infrastructure 'fully' explains the pattern contradicts its concession.")],
   "The paragraph accepts the pattern but argues that causation may run partly from safety to numbers, through infrastructure and self-selection, while allowing that drivers may adapt. Its conclusion is narrow: numbers alone cannot be relied on. The correct summary keeps 'partly' and the narrow conclusion.",
   "Choosing the option that makes infrastructure the full explanation, missing the concession about drivers, or the one that calls the pattern an illusion.",
   "V02J-cycling-safety-in-numbers", "Two distractors each overcorrect the reported view in a different direction; only the key preserves both the concession and the limited conclusion.",
   cognitive="Analysis", exams=DX)

# 012 Cities, explanation of a phenomenon, Medium
ps("V02-J-012", "Cities and geography", "Faster transport yields bigger cities rather than shorter commutes, because people budget travel time.", "Medium",
   "Faster roads and railways are usually justified by the time they will save commuters. Yet in many cities and over long periods, the average time people spend travelling to work each day has stayed surprisingly stable. The explanation is that people treat travel time, not distance, as the quantity to be budgeted. When a new motorway cuts the journey, many households eventually move further out, to larger and cheaper homes, until the commute is roughly as long as it was before. The investment is not wasted: people gain space and a wider choice of jobs and housing. But its benefit arrives as a larger city rather than as the shorter commute that was promised.",
   "Because people budget travel time, not distance, faster transport tends to yield longer distances and larger cities rather than shorter commutes, though it still brings benefits.",
   [("Public investment in faster roads and railways is largely wasted, since commuters end up spending just as much time travelling to work each day as they did before the money was spent.",
     "The paragraph says plainly that the investment 'is not wasted', because people gain space and choice."),
    ("People move further from city centres mainly because homes there are larger and cheaper, regardless of how long their journey to work becomes as a result.",
     "The paragraph says households move out only 'until the commute is roughly as long as it was before', so travel time limits the move rather than being ignored."),
    ("New motorways shorten commutes permanently, giving households more free time each day and letting them choose jobs that lie closer to their homes.",
     "This is the promise the paragraph says is not kept: commuting time returns to roughly its old level.")],
   "The paragraph explains why commuting time stays stable: people budget time, so faster links lead them to live further away. It concedes that the investment brings benefits, but in the form of a larger city. The correct summary gives the mechanism, the result and the concession.",
   "Concluding that the investment is wasted, overlooking the concession about space and choice.",
   "V02J-commuting-time-budget", "One distractor misreads the concession and another misreads the mechanism; both need the paragraph as a whole.",
   cognitive="Understanding")

# 013 Philosophy, critique of a view, Difficult
ps("V02-J-013", "Philosophy and ethics", "The argument that distance is morally irrelevant moves too quickly.", "Difficult",
   "Most people feel that they would be obliged to help a stranger in danger in front of them, yet feel no comparable obligation to help a stranger in equal danger on another continent. Some philosophers conclude that this feeling is simply a bias: distance, they argue, cannot by itself make a moral difference, so our duties to the distant are as strong as our duties to the near. The argument is powerful, but it moves too quickly. Distance usually travels with other features that may matter, such as whether one is uniquely placed to help, whether one's help will actually arrive, and whether many others could help equally well. To show that the feeling is mere bias, one must show that it survives when these features are held constant, and that is harder than the argument assumes.",
   "The claim that distance makes no moral difference is too hasty: distance accompanies features that may matter, and the intuition is mere bias only if it survives once they are controlled.",
   [("Our moral duties to strangers in danger on other continents are just as strong as our duties to strangers in danger in front of us, since distance by itself cannot make any moral difference.",
     "This is the conclusion of the philosophers whose argument the paragraph says 'moves too quickly'; the author neither endorses nor fully rejects it."),
    ("We are more strongly obliged to help those near us than those far away, because physical distance is itself a morally relevant feature of any situation.",
     "The author never claims distance itself matters; the point is that distance 'travels with other features that may matter', which is a different claim."),
    ("The feeling that we must help strangers nearby is a bias, but a useful one, since we are usually uniquely placed to help those who are in front of us.",
     "The paragraph does not concede that the feeling is a bias; it says showing it to be one is 'harder than the argument assumes'.")],
   "The paragraph reports an argument that the near-far intuition is mere bias, then objects that distance correlates with other possibly relevant features, so the intuition can be dismissed only if it survives when those are held fixed. The correct summary captures the critique without overstating it.",
   "Choosing the option that says distance itself matters, mistaking the author's methodological objection for a substantive defence of the intuition.",
   "V02J-moral-distance-duty", "The tempting distractor reverses the reported view; the reader must see that the author only questions the argument's speed.",
   cognitive="Analysis", exams=DX)

# 014 Philosophy, argument, Difficult
ps("V02-J-014", "Philosophy and ethics", "Delay weakens the reforming reason for punishment but not the reason of answering the wrong.", "Difficult",
   "When a crime is discovered decades after it was committed, it is sometimes said that punishing the offender now punishes a different person: the frail old man in the dock shares a name with the young man who did the deed, but little else. The objection has force where punishment is meant to reform, for a person who has long since changed has nothing left to reform. It has less force where punishment is meant to answer the wrong itself, to affirm that the victim mattered and that the act was not acceptable. For that purpose what matters is not whether the offender has changed but whether he is the one responsible, and a change of character, however real, does not transfer responsibility to someone else. Time may therefore weaken some reasons for punishment while leaving others intact.",
   "Long delay undermines punishment's reforming purpose, since the offender may have changed, but not its purpose of answering the wrong, which rests on responsibility, not present character.",
   [("Offenders who have truly changed over the decades should not be punished for crimes they committed long ago, because punishing them now would mean punishing a different person.",
     "This is the objection the paragraph reports and then limits; it says the objection 'has less force' where punishment answers the wrong."),
    ("Punishment is justified only as a way of affirming that victims mattered, so whether an offender has changed is irrelevant to every reason for punishing.",
     "The paragraph grants that the objection 'has force where punishment is meant to reform'; it recognises more than one purpose, so 'only' and 'every' contradict it."),
    ("Since old offenders cannot be reformed, punishment for crimes discovered decades later should aim instead at deterring others from committing similar acts.",
     "Deterrence is never mentioned; the paragraph contrasts reform with answering the wrong, so this adds an outside purpose.")],
   "The paragraph distinguishes two purposes of punishment: reform, which a long delay may undercut, and answering the wrong, which depends on responsibility and so survives a change of character. Its conclusion is that time weakens some reasons but not others. The correct summary states that distinction.",
   "Treating the reported 'different person' objection as the author's verdict, or swinging to the claim that only retribution counts.",
   "V02J-punishing-old-crimes", "Requires holding two purposes apart; one distractor states the reported objection and another overcorrects to a single purpose.",
   cognitive="Analysis", exams=DX)

# 015 Philosophy, comparison, Medium
ps("V02-J-015", "Philosophy and ethics", "Misleading wrongs the listener as lying does; any difference lies in the speaker's self-imposed rule.", "Medium",
   "Many people believe there is a moral difference between telling a lie and saying something true that is designed to mislead. Asked whether he has been drinking, the driver who answers 'I had a glass of water an hour ago' has not lied, though he hopes the listener will draw a false conclusion. One defence of the distinction is that the misleader leaves the listener a share of the responsibility, since the false belief comes from the listener's own inference. But the listener drew that inference precisely because the speaker counted on it. Whatever difference remains seems to lie less in the harm done to the listener than in what the speaker permits himself: a rule against outright falsehood that he keeps even while evading its purpose.",
   "Misleading with true words wrongs the listener scarcely less than lying, since it exploits the listener's inference; whatever difference remains lies mainly in the speaker's self-imposed rule.",
   [("Misleading with true statements is morally better than lying, because a listener who draws a false inference must share the responsibility for the resulting belief.",
     "This is the defence the paragraph reports and then rebuts: the listener drew the inference 'precisely because the speaker counted on it'."),
    ("Misleading is morally worse than lying, because a speaker who deceives with true words adds hypocrisy to deception by pretending to honour a rule whose purpose he is evading.",
     "The paragraph locates the remaining difference in the speaker's rule but never ranks misleading as worse; the claim of added hypocrisy goes beyond it."),
    ("Drivers questioned about drinking often reply with literally true statements, which shows that people prefer misleading to lying when they fear being caught.",
     "The driver is a single illustration; the paragraph makes no claim about how drivers usually answer or about general preferences.")],
   "The paragraph compares lying and misleading, rejects the defence that the listener shares responsibility, and suggests that what difference remains lies in the speaker's own rule rather than in harm to the listener. The correct summary keeps both the rejection and the residual difference.",
   "Choosing the option that ranks misleading as worse, reading a description of the speaker's rule as a verdict.",
   "V02J-lying-versus-misleading", "One distractor builds on the author's last sentence but adds a ranking the paragraph does not make.",
   cognitive="Analysis")

# 016 Philosophy, argument, Medium
ps("V02-J-016", "Philosophy and ethics", "Since choices must be arranged somehow, the real question about nudges is who arranges them and how openly.", "Medium",
   "Arranging choices so that people are steered towards better outcomes, by setting a sensible default for pension saving or putting fruit at eye level in a canteen, is often defended on the ground that no option is forbidden and anyone can choose otherwise. Critics reply that such arrangements are manipulative, working on inertia and habit rather than on reason. The reply is weaker than it sounds, because some arrangement is unavoidable: a canteen must put something at eye level, and a pension scheme must have some default. The real question is therefore not whether choices will be shaped but by whom and for whose benefit, and whether the shaping is open enough that people could object to it if they knew of it.",
   "Since choices must be arranged somehow, the charge that steering them is manipulative is weak; what matters is who shapes them, for whose benefit, and how openly.",
   [("Steering choices is acceptable because no option is forbidden, so people who end up with poor outcomes have only themselves to blame for not choosing otherwise.",
     "The paragraph reports the 'no option is forbidden' defence without adopting it, and the claim about blame is not in the paragraph at all."),
    ("Setting defaults and arranging goods is manipulative, since it works on inertia and habit rather than appealing to people's capacity to reason for themselves.",
     "This is the critics' reply, which the paragraph says 'is weaker than it sounds' because some arrangement is unavoidable."),
    ("Governments and employers should set defaults for every important decision, because people left to choose for themselves will usually choose badly.",
     "The paragraph makes no such prescription and says nothing about people choosing badly; it asks only who shapes choices and how openly.")],
   "The paragraph presents a defence and a criticism of steering choices, rejects the criticism on the ground that some arrangement is inevitable, and reframes the issue as one of who shapes choices, for whom, and how openly. The correct summary gives the reason and the reframing.",
   "Picking the critics' view because the paragraph discusses it at length.",
   "V02J-nudges-paternalism", "The critics' view is stated in the paragraph's own terms and must be recognised as the view rejected.",
   cognitive="Analysis")

# 017 Psychology, explanation of a phenomenon, Easy
ps("V02-J-017", "Psychology", "Experts explain badly because knowledge hides the beginner's view; checking understanding is the remedy.", "Easy",
   "A specialist asked to introduce a field to newcomers frequently leaves them more confused than before, and ill will rarely has anything to do with it. Understanding, once gained, erases the memory of what it was like to lack it. So the specialist jumps over steps that now feel self-evident, reaches for terms that have become automatic and misjudges how much time a novice needs to keep up. The mastery that earns someone the right to teach thus hides from that person the view of the subject a newcomer has. The best teachers get round this not by knowing less but by repeatedly testing what their audience has in fact understood.",
   "Experts often explain badly because their own understanding makes a beginner's position hard to imagine, a problem overcome by checking what learners grasp, not by knowing less.",
   [("Experts explain their subjects badly because they care little about beginners and are unwilling to spend the time needed to teach them properly.",
     "The paragraph says at the outset that 'ill will rarely has anything to do with it'."),
    ("The more a person knows about a subject, the worse a teacher of that subject the person is bound to be, whatever effort is made to explain it.",
     "The paragraph says the best teachers 'get round this', so the difficulty is not inevitable whatever the effort."),
    ("Beginners learn best from teachers who know only a little more than they do themselves, since such teachers can still remember clearly what it was like not to understand the subject.",
     "The paragraph never compares teachers by level of knowledge; its remedy is testing what the audience understands, not choosing less expert teachers.")],
   "The paragraph explains why experts explain poorly: understanding makes it hard to imagine not understanding, so they skip steps and use jargon. It names the remedy. The correct summary gives the cause and the remedy.",
   "Attributing the problem to indifference, which the first sentence rules out.",
   "V02J-curse-of-knowledge", "Cause and remedy are both stated in single sentences.",
   cognitive="Understanding")

# 018 Psychology, finding and qualification, Medium
ps("V02-J-018", "Psychology", "Ownership raises the value people place on things, but the effect depends on how the thing is regarded.", "Medium",
   "In a familiar kind of experiment, people given a simple object such as a mug ask for considerably more to part with it than others, not given one, will pay to acquire it. The gap has been taken as evidence that owning a thing makes us value it more, simply because it is ours. The finding has proved robust in many settings, but its size depends on circumstances. It tends to shrink among experienced traders, who regard goods as stock to be sold, and it is larger for items people expect to keep and use than for those they hold only for exchange. Ownership, it seems, raises value most when a thing is seen as part of one's possessions rather than as a token in a market.",
   "People tend to value things more once they own them, but the effect varies, being weaker among traders and for goods held for exchange than for things owners mean to keep.",
   [("Ownership makes everyone value an object above its market price, a bias that persists unchanged among experienced traders as much as among ordinary buyers.",
     "The paragraph says the effect 'tends to shrink among experienced traders', so 'unchanged' contradicts it."),
    ("Experiments with mugs show that sellers are greedier than buyers, which is why people who own goods ask higher prices than others are willing to pay.",
     "The paragraph explains the gap by ownership raising value, not by greed; this replaces its explanation with an outside one."),
    ("The effect of ownership disappears entirely among experienced traders, which shows that it was never more than an artefact of laboratory experiments.",
     "The paragraph says the effect tends to 'shrink', not that it disappears, and it calls the finding 'robust in many settings'.")],
   "The paragraph reports a robust finding that ownership raises valuation and then qualifies its size: smaller for traders and for goods held for exchange, larger for things owners mean to keep. The correct summary states the finding and both qualifications.",
   "Turning 'tends to shrink' into 'disappears', and so dismissing a finding the paragraph calls robust.",
   "V02J-endowment-effect", "Two distractors misstate the qualification in opposite directions.",
   cognitive="Understanding")

# 019 Psychology, explanation of a phenomenon, Easy
ps("V02-J-019", "Psychology", "People overestimate agreement with their views because of skewed company and a sense of what is natural.", "Easy",
   "People tend to overestimate how many others share their opinions, habits and preferences. Part of the reason is that we spend most of our time with people like ourselves, so the sample of views we meet is not representative of the wider population. Part is that our own choices seem to us the natural response to a situation, so we assume that others facing it would choose the same. The tendency is not simply vanity; it arises from the limited and familiar evidence that each of us has about what other people think. It also helps explain why people are often surprised when an election or a survey reveals how divided opinion really is.",
   "People overestimate how widely others share their views, chiefly because the company they keep and their sense of what is natural skew their evidence.",
   [("People overestimate agreement with their views mainly out of vanity, since they like to believe that sensible people must think exactly as they do.",
     "The paragraph says the tendency 'is not simply vanity' and traces it to limited and familiar evidence."),
    ("Elections and surveys usually surprise people, because opinion in most societies is far more divided than ordinary experience would lead them to expect.",
     "This takes the final illustration as the main point and adds a claim about 'most societies'; the paragraph's subject is why people overestimate agreement."),
    ("Spending time with people unlike ourselves is the only reliable way to escape the habit of overestimating how many others agree with us.",
     "The paragraph offers no remedy at all, and 'the only reliable way' is an outside prescription.")],
   "The paragraph describes the tendency to overestimate agreement and gives two causes, an unrepresentative social sample and the sense that one's choices are natural, while denying that vanity is the explanation. The correct summary gives the tendency and its causes.",
   "Taking the closing example about elections as the paragraph's main point.",
   "V02J-false-consensus-effect", "The causes are listed plainly; distractors contradict, narrow or add a remedy.",
   cognitive="Understanding")

# 020 Psychology, a finding and its qualification, Medium
ps("V02-J-020", "Psychology", "Familiarity is mistaken for understanding of how things work, less so where knowledge is easily self-tested.", "Medium",
   "Ask people how well they understand how a zip, a flush toilet or a bicycle works, and most will rate their understanding highly. Ask them then to explain, step by step, how the device actually works, and many find they cannot; when asked to rate their understanding again, they mark it down. The confidence was not a lie but a confusion: familiarity with using something, and knowing that an explanation exists somewhere, feels from the inside like possessing the explanation. Notably, the gap is narrower for facts and procedures, such as the names of capital cities or how to tie a knot, where people can check their knowledge by trying to recall or perform it.",
   "People overrate their grasp of how things work because familiarity feels like understanding; trying to explain exposes the illusion, which is weaker where knowledge is self-tested.",
   [("People pretend to understand everyday devices in order to avoid appearing ignorant, and they admit the truth only when they are forced to explain in detail how the devices actually work.",
     "The paragraph says the confidence 'was not a lie but a confusion', so the claim of pretence contradicts it."),
    ("Most people understand facts such as capital cities better than they understand machines, because facts are simpler to learn than the workings of devices.",
     "The paragraph says the gap between confidence and knowledge is narrower for facts because they can be self-checked, not that facts are better understood or simpler."),
    ("Asking people to explain step by step how something works is the best way to teach them how everyday devices such as zips and toilets function.",
     "Explaining exposes the gap in the paragraph; it is not presented as a teaching method, and 'the best way' is outside the paragraph.")],
   "The paragraph reports that people overrate their understanding of mechanisms until asked to explain them, attributes this to familiarity being mistaken for knowledge, and qualifies it: the gap is narrower where knowledge can be self-tested. The correct summary captures the finding, the cause and the qualification.",
   "Reading the contrast with facts as a claim that facts are better understood, rather than that confidence about them is better calibrated.",
   "V02J-illusion-of-explanatory-depth", "One distractor distorts the qualification subtly from calibration to understanding.",
   cognitive="Analysis")

# 021 Psychology, critique of a view, Difficult
ps("V02-J-021", "Psychology", "The fate of the limited-resource account of self-control shows how small published studies can inflate an effect.", "Difficult",
   "For years it was widely accepted that self-control draws on a limited resource, so that resisting one temptation leaves a person less able to resist the next. The idea was supported by many small experiments and fitted the everyday experience of feeling worn out after a demanding day. When the effect was retested in large studies run to a common plan across many laboratories, it proved much smaller than the earlier work had suggested, and in some cases indistinguishable from zero. It would be too quick to conclude that people never tire of exercising self-control. What the episode shows is that a stack of small studies, each published because it found an effect, can make a weak or absent phenomenon look established, and that agreement with everyday experience is no substitute for a test designed in advance.",
   "Large planned tests that failed to confirm the limited-resource view of self-control show how selectively published small studies can inflate an effect, though such fatigue may still exist.",
   [("Large replications have shown that self-control draws on no limited resource at all and that feeling worn out after a demanding day is merely an illusion.",
     "The paragraph warns that it 'would be too quick to conclude that people never tire of exercising self-control', so this overstates the result."),
    ("Everyday experience of tiring after effort still confirms the limited-resource view of self-control, even though large studies across many different laboratories later found only small effects.",
     "The paragraph says agreement with everyday experience 'is no substitute for a test designed in advance', so it does not treat that experience as confirmation."),
    ("The early experiments on self-control were biased by researchers who wanted to confirm a theory that matched their own experience of tiring after effort.",
     "The paragraph blames the selective publication of small studies, 'each published because it found an effect', not the motives of individual researchers.")],
   "The paragraph recounts how an accepted effect shrank under large pre-planned tests, cautions against concluding that self-control never tires, and draws a lesson about selective publication and the limits of intuition. The correct summary keeps the lesson and the caution.",
   "Choosing the option that blames researchers' motives, confusing a problem of selective publication with deliberate bias.",
   "V02J-ego-depletion-replication", "Distractors fail on the caution, on the role of intuition and on the mechanism of inflation; telling them apart needs the whole paragraph.",
   cognitive="Analysis", exams=DX)

# 022 Society, comparison, Medium
ps("V02-J-022", "Society and culture", "A single form of 'you' moves the marking of rank elsewhere rather than abolishing it.", "Medium",
   "Languages that oblige speakers to choose between a familiar and a respectful form of 'you' are sometimes thought more hierarchical than those, like modern English, that use a single form for everyone. The comparison is misleading. Speakers of English mark distance and rank in other ways: through first names or titles, through how directly they make requests, through who may start a conversation and who may end it. A language without the grammatical choice has not abolished the social one; it has moved it elsewhere, often to places where it is harder for a newcomer to notice. If anything, the explicit pronoun makes the rules of respect easier to see and therefore easier to learn.",
   "Having a single form of 'you' does not make a language less hierarchical, since speakers mark rank and distance by other, often less visible means that may be harder to learn.",
   [("Languages with separate familiar and respectful forms of 'you' are more hierarchical than English, because their grammar forces speakers to mark rank in every conversation.",
     "This is the view the paragraph calls 'misleading'; it argues that English marks rank too, only by other means."),
    ("Modern English is more hierarchical than languages with two forms of 'you', since its rules of respect are hidden and therefore harder for newcomers to learn.",
     "The paragraph's 'If anything' concerns only how easily the rules can be seen and learnt; it never claims English is more hierarchical."),
    ("Newcomers to English find titles and first names the hardest part of the language to master, harder than either its grammar or its pronunciation.",
     "The paragraph makes no comparison with grammar or pronunciation; this adds an outside claim and misses the main point.")],
   "The paragraph rejects the inference from a single pronoun to less hierarchy: English marks rank through names, directness and conversational rules, so the social distinction has moved, not vanished, and may even be harder to learn. The correct summary gives this point with its hedge.",
   "Choosing the reversal that makes English more hierarchical, mistaking a point about visibility for a point about degree of hierarchy.",
   "V02J-forms-of-address", "The reversal distractor builds on the paragraph's final hedge and must be separated by scope.",
   cognitive="Analysis")

# 023 Society, critique of a view, Difficult
ps("V02-J-023", "Society and culture", "That gossip enforces norms corrects its bad name but does not justify it.", "Difficult",
   "Gossip has a poor reputation: it is condemned as idle, malicious and a waste of time. A more sympathetic view, now common among those who study small communities, holds that gossip performs a social function, spreading knowledge of who can be trusted and deterring cheats who fear for their reputations. This view is a useful corrective, but it can slide into a defence of gossip as such. The same mechanism that deters the cheat also punishes the nonconformist, the newcomer and anyone whose private life departs from local expectation, and it does so without a hearing. To say that gossip enforces norms is to say nothing yet about whether the norms deserve enforcing, or whether those it targets had any chance to answer.",
   "Seeing gossip as norm enforcement rightly corrects its idle image but does not justify it, since the norms may be unworthy and its targets get no hearing.",
   [("Gossip deserves its poor reputation, because whatever it may do to deter cheats, it remains chiefly a malicious and idle waste of everyone's time.",
     "The paragraph calls the sympathetic view 'a useful corrective' to that reputation, so it does not endorse the old condemnation."),
    ("Gossip benefits small communities by spreading knowledge of who can be trusted, so its usefulness outweighs the harm it does to newcomers and nonconformists.",
     "This is the slide 'into a defence of gossip as such' that the paragraph warns against; it never weighs benefit against harm in gossip's favour."),
    ("Gossip in small communities targets newcomers and nonconformists more often than cheats, and so on balance it does more harm than good to such communities.",
     "The paragraph says the same mechanism reaches both groups; it makes no claim about frequency and reaches no verdict on the overall balance.")],
   "The paragraph accepts the functional view as a corrective, warns that it does not amount to a defence, and gives two reasons: the mechanism also punishes harmless difference without a hearing, and enforcing norms says nothing about their merit. The correct summary keeps the corrective and the limit.",
   "Choosing the net-harm verdict, which sounds like the author's critical tone but adds a balance the paragraph never strikes.",
   "V02J-gossip-social-control", "Three distractors each take a definite side on gossip, while the author's position is a carefully limited one.",
   cognitive="Analysis", exams=DX)

# 024 Society, finding and qualification, Easy
ps("V02-J-024", "Society and culture", "Shared family meals are linked with children's wellbeing, but the meal's own effect is uncertain.", "Easy",
   "Children in families that eat together regularly tend, on average, to do better at school and to report fewer emotional difficulties. This has led to the advice that parents should make shared meals a priority. Yet families that manage regular meals together often differ in other ways too: they may have more predictable working hours, more money and less conflict at home. Some of what looks like the effect of the meal may be the effect of the kind of household that can arrange one. The meal may still help, but the evidence for it is weaker than the advice suggests.",
   "Shared meals are linked with children's wellbeing, but since such families differ in other ways too, the meal's own benefit is less certain than advice implies.",
   [("Eating together every day is the most important thing parents can do to help their children succeed at school and stay emotionally healthy.",
     "The paragraph says the evidence is 'weaker than the advice suggests'; 'the most important thing' goes far beyond it."),
    ("Shared family meals have no real effect on children, since any benefit linked to them can be fully explained by money, working hours and the level of conflict at home.",
     "The paragraph says the meal 'may still help' and that only part ('Some of what looks like the effect') may come from the household."),
    ("Families with predictable working hours and more money eat together more often than other families, because they have more time to cook.",
     "This picks out a detail and adds a cause, time to cook, that the paragraph never gives; it misses the point about weak evidence.")],
   "The paragraph reports an association, notes the advice drawn from it, and qualifies it: families who eat together differ in other ways, so the meal's own effect is uncertain though possible. The correct summary gives the association and the qualification.",
   "Swinging from the advice to the opposite extreme that meals have no effect.",
   "V02J-shared-family-meals", "The qualification is explicit and the distractors are clearly extreme or narrow.",
   cognitive="Understanding")

# 025 Society, argument, Easy
ps("V02-J-025", "Society and culture", "Fixed mourning customs, though rigid, gave grief a shared structure that has been lost.", "Easy",
   "Many traditional societies set out how long the bereaved should mourn, what they should wear and when they might return to ordinary life. Such rules are easily dismissed today as rigid impositions on private feeling. But they also did something for the grieving. They told others how to behave towards the bereaved, gave the mourner permission to withdraw for a time, and marked a point at which life could resume without guilt. Where the rules have faded, people are often left unsure how long grief is allowed to last and what their friends expect of them. The old customs had their costs, but they offered a shared structure that private feeling alone does not supply.",
   "Though fixed mourning customs can seem rigid, they gave the bereaved and those around them a shared structure for grief, which their decline has left many people without.",
   [("Traditional mourning rules should be brought back, since people today have no idea how to grieve properly and their friends do not know how to help them through it.",
     "The paragraph prescribes nothing, grants that the customs 'had their costs', and says people are 'often' unsure, not that they have 'no idea'."),
    ("Rules about mourning dress and duration were rigid impositions that forced the bereaved to display feelings they may not actually have had.",
     "This is the dismissive view the paragraph mentions and then answers with 'But they also did something for the grieving'."),
    ("In traditional societies the bereaved were expected to withdraw from ordinary life for a fixed period and to wear particular clothing while mourning.",
     "This restates a descriptive detail from the first sentence and omits the paragraph's argument about what the customs did for people.")],
   "The paragraph concedes that mourning rules look rigid, then argues that they guided others, licensed withdrawal and marked an end to mourning, a structure whose loss leaves people unsure. The correct summary keeps the concession and the main point.",
   "Choosing the dismissive view the paragraph reports in its second sentence.",
   "V02J-mourning-period-customs", "The turn at 'But' signals the point clearly.",
   cognitive="Understanding")
