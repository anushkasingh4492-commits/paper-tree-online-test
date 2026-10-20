import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DX = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
pj("V01-H-001", "Cities and geography", "Many towns grew up at river crossings because traffic converged there.", "Easy",
   ["Before modern engineering, the place where a river could most easily be crossed was among the most valuable sites in any region.",
    "Roads from both banks converged on such a crossing, since travellers and carters had no other way to reach the far side without a long detour.",
    "Wherever traffic gathered in this way, inns, markets and workshops followed, and a small settlement took shape around the people obliged to pass through.",
    "Over the centuries, many such settlements grew into towns whose very names still recall the ford or bridge from which they began."],
   "Sentence [[1]] introduces the subject, the value of an easy river crossing. Sentence [[2]] explains why, referring back with 'such a crossing'. Sentence [[3]] picks up the converging roads with 'traffic gathered in this way' and describes a settlement forming. Sentence [[4]] follows that settlement over 'the centuries' with 'many such settlements', closing the account.",
   "Opening with sentence [[3]] because it sounds like a general rule, which leaves 'in this way' with nothing to refer to.",
   "V01H-bridging-points-town-siting", "Each link is carried by a clear reference word ('such a crossing', 'in this way', 'such settlements') and the sequence is chronological.",
   traps=[("1324", "Sentence [[3]] needs the converging roads of sentence [[2]] for 'traffic gathered in this way' to make sense, and sentence [[2]] cannot follow a settlement that has already formed."),
          ("3124", "Sentence [[3]] cannot open: 'in this way' points back to a gathering of traffic that has not yet been described.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 002
pj("V01-H-002", "Philosophy and ethics", "Because no one could personally verify enough sources, trust in testimony must be a basic source of justification.", "Medium",
   ["Most of what any of us believes about distant places, past events and the workings of our own bodies rests on nothing but the word of other people.",
    "One tradition holds that such beliefs are justified only when we have personally confirmed, through our own observation, that the speakers concerned are generally reliable.",
    "The difficulty is that no individual could ever perform enough checks to vouch for more than a tiny fraction of the sources on which he or she depends.",
    "If that demand were taken seriously, almost all of our knowledge would therefore collapse, which suggests that trust in testimony is a basic source of justification rather than a derived one."],
   "Sentence [[1]] states the fact under discussion: most beliefs rest on others' word. Sentence [[2]] reports a view about when 'such beliefs' are justified. Sentence [[3]] raises 'The difficulty' with that view, that no one can check enough sources. Sentence [[4]] draws the consequence of 'that demand' with 'therefore': the demand would destroy most knowledge, so testimony must be basic. The conclusion needs the difficulty as its premise, so sentence [[3]] must come before sentence [[4]].",
   "Placing sentence [[4]] straight after sentence [[2]] because 'that demand' points to the view in sentence [[2]], which leaves 'therefore' without the premise that makes the collapse follow.",
   "V01H-trusting-testimony", "The order of the last two sentences follows from the logic of the idea: the objection is the premise and the collapse of knowledge is its consequence.",
   traps=[("1243", "Sentence [[4]] concludes with 'therefore', so it needs the reason in sentence [[3]] before it; ending on 'The difficulty' after the conclusion has been drawn reverses premise and conclusion."),
          ("2134", "Sentence [[2]] speaks of 'such beliefs', which needs the beliefs resting on others' word described in sentence [[1]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 003
pj("V01-H-003", "Psychology", "People underestimate task durations because they imagine each step going smoothly; past durations of similar projects are a better guide.", "Easy",
   ["People asked to estimate how long a task will take tend to underestimate, even when they have often run late on similar tasks before.",
    "This pattern, known as the planning fallacy, seems to arise because forecasters picture the specific steps of the job and imagine each going smoothly.",
    "What they leave out are the interruptions, delays and mistakes that, though individually unforeseeable, almost always occur somewhere along the way.",
    "A simple remedy, accordingly, is to set aside the details of the plan and ask instead how long comparable projects actually took in the past."],
   "Sentence [[1]] describes the tendency to underestimate. Sentence [[2]] names 'This pattern' and gives its cause, picturing each step going smoothly. Sentence [[3]] says what that picture leaves out. Sentence [[4]] offers a remedy that follows 'accordingly' from the diagnosis: ignore the step-by-step plan and look at past projects.",
   "Putting the remedy in sentence [[4]] before sentence [[3]], which separates 'What they leave out' from the picturing it completes.",
   "V01H-planning-fallacy", "The sentences follow a plain observation, cause, detail, remedy pattern with reference words at each link.",
   traps=[("1243", "Sentence [[3]] completes the explanation in sentence [[2]] ('What they leave out' of the pictured steps), so it cannot follow the remedy in sentence [[4]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 004
pj("V01-H-004", "Society and culture", "The trickle-down theory of fashion explains its restlessness, and even upward borrowing may fit its logic of distinction.", "Medium",
   ["An old explanation of fashion holds that styles begin among the wealthy, who adopt them precisely because others cannot afford to.",
    "As cheaper copies spread downward, the style loses its power to mark distinction, and the wealthy abandon it for something new.",
    "The theory thus accounts neatly for why fashion never stands still: every act of imitation from below sets off a fresh flight from above.",
    "Yet the theory's neatness is also its weakness, for in recent decades many styles have plainly travelled the other way, from street clothing and working dress into expensive boutiques.",
    "Even these reversals may confirm the underlying logic, however, since what the affluent borrow from below is often prized because it signals a knowingness that money alone cannot buy."],
   "Sentence [[1]] states the theory. Sentence [[2]] continues the mechanism with 'cheaper copies' of 'the style'. Sentence [[3]] sums up what the theory explains ('thus accounts neatly'). Sentence [[4]] turns on that 'neatness' and raises the counter-example of styles travelling 'the other way'. Sentence [[5]] answers with 'these reversals', arguing they may still fit the logic of distinction.",
   "Ending with sentence [[3]] because it sounds like a summary, which leaves 'the theory's neatness' in sentence [[4]] referring to a judgement not yet made.",
   "V01H-fashion-trickle-down", "Five sentences with a claim, objection and reply; the summary sentence is tempting as a closer but must precede the objection.",
   traps=[("12453", "Sentence [[4]] speaks of 'the theory's neatness', which is the judgement made in sentence [[3]]; and sentence [[3]] restates the theory as if unchallenged, so it cannot come after the reversals have been raised."),
          ("13245", "Sentence [[3]] says 'thus', summing up a mechanism of imitation and flight that is completed only in sentence [[2]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 005
pj("V01-H-005", "History and politics", "The secret ballot undermined vote buying by making it impossible to verify a purchased vote.", "Medium",
   ["For much of the nineteenth century, voters in many countries declared their choices aloud or on coloured ballots that onlookers could easily identify.",
    "Landlords, employers and party agents could therefore see exactly how each man voted, and reward or punish him accordingly.",
    "The secret ballot changed this not by making bribery illegal, which it often already was, but by making it impossible for a briber to confirm what he had bought.",
    "A vote that cannot be verified is a poor investment, and the market in purchased votes withered in many places once the ballot became private."],
   "Sentence [[1]] describes open voting. Sentence [[2]] draws the consequence with 'therefore': powerful onlookers could see each vote. Sentence [[3]] says the secret ballot 'changed this' and explains how, by removing the briber's ability to confirm the vote. Sentence [[4]] generalises that mechanism: an unverifiable vote is a poor investment, so vote buying withered. The economic reasoning in sentence [[4]] presupposes the point about confirmation in sentence [[3]].",
   "Placing sentence [[4]] before sentence [[3]] because both concern bought votes, which puts the effect of private ballots before private ballots have been introduced.",
   "V01H-secret-ballot", "The final pair is fixed by the logic of the idea: the general principle about unverifiable votes depends on the mechanism explained in the sentence before it.",
   traps=[("1243", "Sentence [[4]] speaks of the ballot becoming private and of votes that 'cannot be verified', which presupposes the secret ballot introduced in sentence [[3]]; and 'changed this' in sentence [[3]] must follow the open voting of sentence [[2]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 006
pj("V01-H-006", "Economics and business", "Farm prices can swing in a self-sustaining cycle because planting decisions lag their reward and farmers read the future off the present price.", "Difficult",
   ["Farmers must decide how much to plant months before they learn what the harvest will fetch, and many simply assume that next season's price will match this season's.",
    "After a year of high prices, that assumption leads many of them to plant more, and the larger harvest that follows pushes the price down.",
    "Expecting the low price to last, they plant less the next season, and the smaller harvest sends the price back up, so that the swing begins again.",
    "What sustains the swing is neither the weather nor any change in tastes but the lag between decision and reward, together with the habit of reading the future off the present.",
    "If that diagnosis is right, the remedy may lie less in subsidies than in information, since farmers who could see how much was being planted in total would stop treating today's price as a forecast."],
   "Sentence [[1]] sets up the lag and the farmers' assumption that next season's price will match this one. Sentence [[2]] applies 'that assumption' to a year of high prices: more planting, a larger harvest, a falling price. Sentence [[3]] can only come next, because 'the low price' it expects to last is the fall produced in [[2]], and it completes the cycle. Sentence [[4]] explains what sustains 'the swing' once the swing has been described in full. Sentence [[5]] draws a remedy 'If that diagnosis is right', which needs the diagnosis of [[4]] before it.",
   "Placing the remedy in sentence [[5]] straight after the description of the cycle, as if the cycle alone suggested it, which leaves 'that diagnosis' with nothing to refer to and puts the explanation after its consequence.",
   "V01H-cobweb-cycle-farm-prices", "The two phases of the cycle look interchangeable until the reader sees that 'the low price' must be the fall caused by overplanting; the diagnosis and remedy then follow the logic of explanation before consequence.",
   traps=[("13245", "Sentence [[3]] begins 'Expecting the low price to last', but no low price exists until the larger harvest of sentence [[2]] has pushed the price down; and 'that assumption' in [[2]] would then be separated from the assumption stated in [[1]]."),
          ("12354", "Sentence [[5]] proposes a remedy 'If that diagnosis is right', and the diagnosis, the lag and the habit of reading the future off the present, is given only in sentence [[4]].")],
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 007
pj("V01-H-007", "Cities and geography", "River silt stranded many old ports, and trade moved to deeper harbours.", "Easy",
   ["Many ports that flourished in earlier centuries now lie some distance inland, stranded behind marshes and fields.",
    "Their fate was usually sealed by the rivers that had once made them prosperous, which carried silt downstream and deposited it where the current slowed.",
    "Year by year, these deposits narrowed the channels until the larger ships of later periods could no longer reach the quays.",
    "Trade then moved to deeper harbours along the coast, and the old ports, deprived of their purpose, shrank into quiet market towns."],
   "Sentence [[1]] presents the puzzle of inland ports. Sentence [[2]] names the cause, 'Their fate' being sealed by silt. Sentence [[3]] traces how 'these deposits' closed the channels. Sentence [[4]] gives the result, with 'then', as trade moved elsewhere.",
   "Starting with sentence [[2]], which leaves 'Their fate' without the ports it refers to.",
   "V01H-harbour-silting-port-decline", "A simple cause and effect chain with clear reference words ('Their fate', 'these deposits', 'then').",
   traps=[("2134", "Sentence [[2]] begins 'Their fate', which needs the stranded ports of sentence [[1]] to refer to.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 008
pj("V01-H-008", "Philosophy and ethics", "The doctrine of double effect can answer the charge that intention is easily redescribed by testing whether the plan needs the harm.", "Difficult",
   ["A long-standing principle in ethics holds that it can be permissible to cause a harm one foresees but does not intend, when it would be wrong to cause the same harm as a goal or a means.",
    "Critics object that the line between intending and merely foreseeing is too easily redrawn, since almost any harmful act can be redescribed so that the harm appears incidental.",
    "This objection loses much of its force once intention is tested not by how an act is described but by whether the agent's plan would still succeed if, by some fluke, the harm did not occur.",
    "By that measure, an engineer who opens a sluice to save a town, foreseeing that fields downstream will flood, succeeds even if the fields happen to stay dry; one who floods them to drive the farmers away does not."],
   "Sentence [[1]] states the principle distinguishing foreseen from intended harm. Sentence [[2]] gives the critics' objection that the line is easily redrawn. Sentence [[3]] answers 'This objection' with a test: would the plan still succeed if the harm did not occur? Sentence [[4]] applies 'that measure' to the two engineers: one 'succeeds even if the fields happen to stay dry', the other does not. The example is not a mere illustration of the principle; its point (success even if the fields stay dry) is the counterfactual test, so it must follow sentence [[3]].",
   "Placing the engineer example in sentence [[4]] right after sentence [[1]] as a natural illustration of the principle, missing that 'By that measure' and the 'even if the fields happen to stay dry' clause apply the test given only in sentence [[3]].",
   "V01H-doctrine-of-double-effect", "The tempting order puts the example after the principle; rejecting it needs the logic of the idea, seeing that the example applies the counterfactual test, not the bare principle.",
   traps=[("1423", "The example in sentence [[4]] judges success by whether the plan works 'even if the fields happen to stay dry', which is the test introduced in sentence [[3]]; 'By that measure' has nothing to refer to straight after sentence [[1]]."),
          ("1324", "Sentence [[3]] answers 'This objection', which is first stated in sentence [[2]].")],
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 009
pj("V01-H-009", "Psychology", "Failure to notice changes across a flash suggests vision keeps only a sketch of the scene.", "Medium",
   ["In a familiar kind of experiment, a scene on a screen is briefly interrupted by a blank flash, and some detail of it is altered during the interruption.",
    "Viewers frequently fail to notice even large changes of this sort, such as a building vanishing from the background, unless they happen to be attending to the altered spot.",
    "The finding unsettles the common assumption that we hold a detailed, picture-like record of whatever lies in front of our eyes.",
    "It suggests instead that the visual system keeps only a sketch, trusting that the world itself will be there to consult whenever more detail is needed."],
   "Sentence [[1]] describes the experiment. Sentence [[2]] gives the result for 'changes of this sort'. Sentence [[3]] says what 'The finding' unsettles, the assumption of a detailed inner picture. Sentence [[4]] offers the alternative view 'instead' of that assumption. The rejected assumption must be stated before the view that replaces it.",
   "Putting sentence [[4]] before sentence [[3]], so that 'instead' appears before the assumption it replaces has been stated.",
   "V01H-change-blindness", "The last pair depends on the logic of a claim and its replacement, marked only lightly by 'instead'; students often reverse the interpretive sentences.",
   traps=[("1243", "Sentence [[4]] offers a view 'instead' of something; that something is the picture-like record rejected in sentence [[3]], which must therefore come first."),
          ("2134", "Sentence [[2]] speaks of 'changes of this sort', which needs the altered detail described in sentence [[1]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 010
pj("V01-H-010", "Society and culture", "Table manners served mainly to mark social rank rather than hygiene, though the two can coincide.", "Difficult",
   ["Rules about how to eat, which fork to use, when to begin, what never to do with a knife, are often defended today as matters of simple hygiene.",
    "Yet many such rules were laid down long before anyone understood how disease spreads, and some, like the ban on resting elbows on the table, have no bearing on cleanliness at all.",
    "Their real function seems to have been social: an elaborate code could be learned only through long exposure, and so it marked out those raised in the right households.",
    "This would also explain why such codes tend to grow more intricate wherever newcomers can afford to imitate the outward signs of rank, since a distinction that money can buy soon stops distinguishing.",
    "None of this means the hygienic reading is simply false, for a code adopted to keep newcomers out may also, by happy accident, keep food and hands a little cleaner."],
   "Sentence [[1]] states the common hygienic defence. Sentence [[2]] objects with 'Yet': many rules predate any idea of contagion and some are irrelevant to cleanliness. Sentence [[3]] proposes 'Their real function', social distinction. Sentence [[4]] extends that account to newcomers who can imitate outward signs. Sentence [[5]] concedes that the hygienic reading is not 'simply false', describing the code as one 'adopted to keep newcomers out', which presupposes sentence [[4]]. 'None of this' also gathers up the whole social argument, so the concession must come last.",
   "Moving the concession in sentence [[5]] up to follow the rebuttal in sentence [[2]], where 'None of this means the hygienic reading is simply false' seems to fit, missing that it speaks of a code 'adopted to keep newcomers out'.",
   "V01H-table-manners-history", "Rejecting the tempting position for the concession needs the logic of the idea: the concession relies on the newcomers argument, not just on the rebuttal of the hygienic view.",
   traps=[("12534", "The concession in sentence [[5]] describes a code 'adopted to keep newcomers out', an idea that appears only in sentence [[4]]; placed after sentence [[2]] it would also concede before the social explanation it qualifies has been offered."),
          ("13245", "Sentence [[3]] claims a 'real function' only after the hygienic one has been undermined; and sentence [[2]] begins 'Yet', which cannot answer the social account in sentence [[3]].")],
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 011
pj("V01-H-011", "History and politics", "After the fourteenth-century plague, labour scarcity raised wages despite laws trying to hold them down.", "Easy",
   ["The plague that swept across Europe in the middle of the fourteenth century killed a large share of the population within a few years.",
    "Those who survived found that their labour had become scarce, and landowners desperate for workers began offering higher wages to attract them.",
    "Alarmed by this, authorities in several kingdoms passed laws attempting to hold wages at their old levels.",
    "Such laws proved difficult to enforce, however, because employers who needed hands were often among the first to break them."],
   "Sentence [[1]] describes the plague. Sentence [[2]] gives its consequence for 'Those who survived': scarce labour and rising wages. Sentence [[3]] reacts, 'Alarmed by this', with wage laws. Sentence [[4]] explains why 'Such laws' failed.",
   "Placing sentence [[3]] before sentence [[2]], which leaves 'Alarmed by this' with nothing to be alarmed about.",
   "V01H-plague-labour-shortage-wages", "Chronological sequence with explicit reference words at each step.",
   traps=[("1324", "Sentence [[3]] reacts to rising wages ('Alarmed by this'), which are described only in sentence [[2]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 012
pj("V01-H-012", "Economics and business", "When sellers know more than buyers, good cars leave the used car market and average quality spirals down.", "Medium",
   ["In a market for used cars, sellers usually know far more than buyers about whether a particular vehicle is sound or defective.",
    "Unable to tell the difference, buyers will offer only a price that reflects the average quality they expect to find.",
    "Owners of good cars, who know their vehicles are worth more than that average, are then reluctant to sell, and many withdraw from the market.",
    "As they do, the average quality of cars on offer falls, buyers lower their offers further, and the market can shrink until mostly poor vehicles remain."],
   "Sentence [[1]] sets up the information gap. Sentence [[2]] says buyers, 'Unable to tell the difference', offer an average price. Sentence [[3]] shows owners of good cars withdrawing because their cars are worth more than 'that average'. Sentence [[4]] follows the withdrawal ('As they do') to its result, a falling average and a shrinking market. Each step is a consequence of the one before it.",
   "Placing sentence [[4]] before sentence [[3]] because it mentions falling average quality, which reverses the cause (good owners withdrawing) and its effect.",
   "V01H-used-car-lemons", "The order follows the logic of the idea, a causal chain in which each sentence's premise is the previous sentence's result.",
   traps=[("1243", "The falling average in sentence [[4]] is caused by good cars leaving ('As they do'), which is described only in sentence [[3]]."),
          ("1324", "Sentence [[3]] refers to 'that average', the average-quality price introduced in sentence [[2]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 013
pj("V01-H-013", "Cities and geography", "A bypass relieves a town centre of traffic but also of passing trade, so towns must plan for the loss.", "Medium",
   ["When a busy highway runs through the centre of a small town, residents often campaign for a bypass to carry through traffic around it.",
    "Once the bypass opens, the main street becomes quieter and safer, and the air along it noticeably cleaner.",
    "Yet the same traffic that residents resented also brought customers to the petrol stations, cafes and shops that depended on passing trade.",
    "Some of these businesses close within a few years, and the relief of a calmer centre is mixed with the sight of empty shopfronts.",
    "The towns that fare best tend to be those that plan for this loss in advance, giving visitors new reasons to turn off the bypass and stop."],
   "Sentence [[1]] introduces the campaign for a bypass. Sentence [[2]] describes the benefits 'Once the bypass opens'. Sentence [[3]] turns with 'Yet' to the cost: 'the same traffic' had brought customers. Sentence [[4]] follows 'these businesses' to their closure. Sentence [[5]] concludes with how towns can plan for 'this loss'.",
   "Placing sentence [[3]] before sentence [[2]], so that 'Yet' sets the hidden cost against the campaign before the benefits it is meant to qualify have been described.",
   "V01H-bypass-roads-town-centres", "Five sentences in a benefit, cost, consequence, response pattern; the 'Yet' sentence could seem to attach to the opener.",
   traps=[("13245", "Sentence [[3]] says 'Yet' to qualify the gains of a quieter street; after sentence [[1]] there is no gain yet to qualify, and sentence [[4]] would then refer to 'these businesses' across the intervening sentence [[2]]."),
          ("12354", "Sentence [[5]] speaks of 'this loss', the closures and empty shopfronts of sentence [[4]], so it cannot come before them.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 014
pj("V01-H-014", "Philosophy and ethics", "Theories that always require the best act cannot accommodate acts beyond duty, which many take as a reason to doubt them.", "Medium",
   ["Ordinary moral thinking recognises a class of acts that are good to do but not wrong to omit, such as giving a kidney to a stranger.",
    "Some moral theories have difficulty making room for such acts, because they hold that we are always required to do whatever would produce the most good.",
    "On that view the generous donor has merely done her duty, and anyone in a position to donate who declines has done wrong.",
    "Many find this conclusion so implausible that they treat it as a reason to doubt the theory rather than to revise their admiration for the donor."],
   "Sentence [[1]] identifies acts that are good but optional. Sentence [[2]] introduces theories that cannot accommodate 'such acts'. Sentence [[3]] draws out what 'that view' implies for the donor. Sentence [[4]] reports the reaction to 'this conclusion', treating it as grounds to doubt the theory. The implication must be drawn before anyone can react to it.",
   "Placing sentence [[4]] before sentence [[3]] because it mentions the theory and the donor, which leaves 'this conclusion' with no conclusion yet drawn.",
   "V01H-supererogation-beyond-duty", "The order follows the logic of the idea, a theory, its consequence, then a reductio drawn from that consequence.",
   traps=[("1243", "Sentence [[4]] responds to 'this conclusion', the verdict that the donor merely did her duty, which is drawn only in sentence [[3]]."),
          ("2134", "Sentence [[2]] speaks of 'such acts', which needs the optional good acts introduced in sentence [[1]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 015
pj("V01-H-015", "Psychology", "The sense of understanding everyday devices is largely familiarity, a mistake that is reasonable because knowledge is shared.", "Difficult",
   ["Most people feel that they understand how ordinary devices such as zips, locks and flush toilets work.",
    "That feeling rarely survives a request to explain the mechanism step by step, which tends to produce accounts riddled with gaps the explainer had not noticed.",
    "What had passed for understanding was, in large part, familiarity: having seen the device work countless times, people mistook ease of recognition for a grasp of how it works.",
    "Nor is the mistake mere carelessness, for in daily life the difference between recognising and understanding seldom matters, since what we lack is stored in manuals, repairers and other people."],
   "Sentence [[1]] states the feeling of understanding. Sentence [[2]] shows 'That feeling' failing when an explanation is requested. Sentence [[3]] diagnoses what 'had passed for understanding': it was familiarity, mistaken for grasp. Sentence [[4]] qualifies 'the mistake' by noting that 'the difference between recognising and understanding' seldom matters in daily life. Sentence [[3]] can say what 'had passed for' understanding only once the feeling has been exposed in sentence [[2]], and sentence [[4]] uses the distinction that sentence [[3]] first draws.",
   "Treating sentence [[4]] as an answer to sentence [[2]] (the failure to explain is not carelessness), which places it before the distinction between recognising and understanding has been drawn.",
   "V01H-illusion-of-explanatory-depth", "Abstract sentences whose order depends on the logic of the idea: a diagnosis of familiarity that the closing qualification presupposes, with a tempting swap of the two.",
   traps=[("1243", "Sentence [[4]] speaks of 'the mistake' and 'the difference between recognising and understanding'; both are introduced in sentence [[3]], where people 'mistook ease of recognition' for a grasp of the mechanism."),
          ("1324", "Sentence [[3]] says what 'had passed for understanding', a past tense that presupposes the feeling has already been exposed as false, which happens in sentence [[2]].")],
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 016
pj("V01-H-016", "Society and culture", "Tipping norms differ, and visitors can err by not tipping where wages assume it or by tipping where service is fully priced.", "Easy",
   ["In some countries a tip is expected for almost every service, from a restaurant meal to a taxi ride.",
    "Where tipping is customary in this way, wages in restaurants and hotels are often set on the assumption that customers will add to them.",
    "A visitor who fails to tip in such a place is therefore not being thrifty but, in effect, cutting the pay of the person who served them.",
    "Travellers from such places can err in the opposite way abroad, pressing money on workers in countries where service is fully priced and a tip may seem to imply that they need charity."],
   "Sentence [[1]] introduces countries where tips are expected. Sentence [[2]] explains the wage arrangement 'Where tipping is customary in this way'. Sentence [[3]] draws the consequence with 'therefore' for a visitor who does not tip. Sentence [[4]] describes the error 'in the opposite way', which must follow the first error in sentence [[3]].",
   "Putting sentence [[4]] second because it also concerns travellers, which leaves 'the opposite way' with no first error to be opposite to.",
   "V01H-tipping-customs", "Reference words ('in this way', 'such a place', 'the opposite way') fix every link.",
   traps=[("1423", "Sentence [[4]] describes an error 'in the opposite way', which needs the failure to tip in sentence [[3]] before it.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 017
pj("V01-H-017", "History and politics", "Debasing coinage gave rulers a short-lived profit that hoarding and rising prices soon erased.", "Medium",
   ["Rulers short of money once had a tempting alternative to raising taxes: they could reduce the silver in each coin while keeping its face value unchanged.",
    "For a time this produced a handsome profit, since the mint could strike more coins from the same quantity of metal.",
    "But people soon noticed that the new coins contained less silver, and they began hoarding the older, purer ones and spending only the debased.",
    "As prices rose to reflect the reduced metal in circulation, the ruler's gain melted away, leaving behind a currency that fewer people trusted."],
   "Sentence [[1]] describes debasement. Sentence [[2]] gives its immediate profit, 'For a time'. Sentence [[3]] turns with 'But' to the public's response of hoarding. Sentence [[4]] completes the story: rising prices erase 'the ruler's gain'. The gain must be described before it can melt away, and the public's detection of debasement drives the price rise.",
   "Placing sentence [[4]] straight after sentence [[2]], which puts the erosion of the gain before the public has noticed anything.",
   "V01H-coin-debasement", "Short-term gain then reaction then outcome; the 'But' sentence must sit between profit and its erosion, which needs some reasoning about cause.",
   traps=[("1243", "Sentence [[3]] begins 'But' and introduces the public's discovery; after sentence [[4]] has already described the gain melting away, the contrast has nothing to turn against."),
          ("1324", "Sentence [[3]] says 'But people soon noticed', contrasting with a profit that is described only in sentence [[2]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 018
pj("V01-H-018", "Economics and business", "Free delivery thresholds prompt extra purchases, so delivery is paid for in purchases rather than fees.", "Easy",
   ["Many online shops offer free delivery only on orders above a certain value.",
    "A customer whose basket falls just short of that figure will often add an item she did not originally intend to buy.",
    "From her point of view this feels like a saving, since the extra item seems to cost little more than the delivery charge she has avoided.",
    "For the shop, the arrangement is more attractive still, because the threshold is set so that the extra sales it prompts bring in more than the deliveries it gives away.",
    "Free delivery, in other words, is less a gift than a bargain struck on the shop's terms, one that the customer pays for in purchases rather than in a separate fee."],
   "Sentence [[1]] introduces the threshold. Sentence [[2]] describes a customer just short of 'that figure'. Sentence [[3]] gives 'her point of view'. Sentence [[4]] turns to the shop, for which the arrangement is 'more attractive still', a comparison with the customer's view just given. Sentence [[5]] sums up 'in other words', and its phrase 'on the shop's terms' draws on sentence [[4]].",
   "Ending with sentence [[4]] after the summary in sentence [[5]], which separates 'more attractive still' from the customer's view it is compared with.",
   "V01H-free-shipping-thresholds", "Reference words and the comparative 'still' fix each link; the summary draws on both perspectives.",
   traps=[("12354", "Sentence [[4]] says the arrangement is 'more attractive still' for the shop, a comparison with the customer's view in sentence [[3]]; and sentence [[5]] speaks of 'the shop's terms', which only sentence [[4]] has set out.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 019
pj("V01-H-019", "Cities and geography", "Railway timetables made local solar time unworkable, leading to standard time.", "Medium",
   ["Until the nineteenth century, each town set its clocks by the sun, so that noon came a few minutes earlier in an eastern town than in one further west.",
    "This mattered little while travel was slow, since a journey between two towns took long enough to make a few minutes' discrepancy irrelevant.",
    "Railways changed that, because a timetable listing departures and arrivals across many stations was nearly impossible to compile if every station kept its own local time.",
    "Railway companies therefore adopted a single standard time across their networks, and the public, which increasingly planned its days around the trains, gradually followed."],
   "Sentence [[1]] describes local solar time. Sentence [[2]] says 'This mattered little' while travel was slow. Sentence [[3]] says railways 'changed that', since timetables could not work with many local times. Sentence [[4]] gives the response with 'therefore'. Sentence [[2]] must precede sentence [[3]] because the railways change a situation in which the discrepancy did not matter; that is the logic of the contrast.",
   "Putting sentence [[3]] before sentence [[2]] since both concern travel, which leaves 'Railways changed that' with no settled situation to change.",
   "V01H-railway-standard-time-zones", "The middle pair depends on the logic of the idea: slow travel made local time harmless, and the railway's change only makes sense against that.",
   traps=[("1324", "Sentence [[3]] says railways 'changed that', meaning the harmlessness of local time while travel was slow, which is stated only in sentence [[2]]; and sentence [[4]] must follow the timetable problem it resolves.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 020
pj("V01-H-020", "Philosophy and ethics", "Belief in other minds is better defended as an explanatory theory than by analogy from one's own case.", "Difficult",
   ["How do I know that other people have thoughts and feelings at all, rather than merely behaving as though they do?",
    "A traditional answer reasons by analogy: in my own case pain is linked to wincing and crying out, so when others wince and cry out, I infer that they too are in pain.",
    "The weakness of this argument is that it generalises from a single instance, my own, which is the kind of inference we would reject in almost any other setting.",
    "A better defence abandons the analogy and treats the existence of other minds as a theory, adopted because no rival explains so economically the vast range of what other people say and do.",
    "On this view my belief rests not on my own case at all but on the same kind of reasoning that leads us to accept unseen causes elsewhere in science."],
   "Sentence [[1]] poses the question. Sentence [[2]] gives 'A traditional answer', the argument from analogy. Sentence [[3]] names 'The weakness of this argument', generalising from one case. Sentence [[4]] offers 'A better defence', which is better precisely because it avoids that weakness. Sentence [[5]] spells out 'this view': the belief no longer rests on 'my own case', the single instance criticised in sentence [[3]].",
   "Placing sentence [[5]] before sentence [[4]] because 'not on my own case' seems to answer the weakness directly, which leaves 'On this view' pointing to the analogy it rejects.",
   "V01H-other-minds-analogy-argument", "Abstract argument whose last three sentences depend on the logic of the idea: a weakness, a defence that avoids it, and what that defence implies; the closing sentence is tempting to move up.",
   traps=[("12354", "Sentence [[5]] says 'On this view my belief rests not on my own case', which cannot describe the analogy view of sentence [[2]]; it describes the theory introduced in sentence [[4]], so it must follow it."),
          ("12435", "Sentence [[4]] calls itself 'A better defence', which only makes sense once a weakness in the first defence has been shown in sentence [[3]].")],
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 021
pj("V01-H-021", "Psychology", "After choosing, people revalue options to reduce discomfort, so satisfaction partly reflects the act of choosing.", "Medium",
   ["Before choosing between two attractive options, people often rate them as nearly equal in appeal.",
    "Once the choice is made, however, their ratings tend to drift apart, with the chosen option rising in esteem and the rejected one falling.",
    "A common explanation is that holding a decision while still valuing what was given up is uncomfortable, and revising one's opinions is the easiest way to ease that discomfort.",
    "If this is right, the satisfaction people report with their choices partly reflects the choosing itself, not only the merits of what they chose."],
   "Sentence [[1]] gives the ratings before a choice. Sentence [[2]] contrasts, with 'however', the ratings after it. Sentence [[3]] offers 'A common explanation' of that drift. Sentence [[4]] draws an implication 'If this is right', which needs the explanation first. The finding, its explanation and its implication must come in that order.",
   "Placing sentence [[4]] before sentence [[3]], since both interpret the finding, which leaves 'If this is right' with no explanation to be right.",
   "V01H-post-choice-dissonance", "Order follows the logic of the idea: observation, explanation, then an implication that is conditional on the explanation.",
   traps=[("1243", "Sentence [[4]] is conditional on an explanation ('If this is right'), and the explanation is supplied only in sentence [[3]]."),
          ("2134", "Sentence [[2]] says 'Once the choice is made, however', contrasting with the equal ratings before the choice in sentence [[1]].")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 022
pj("V01-H-022", "Society and culture", "Repetition in oral epics looks like padding only by the standards of writing; it enabled composition in performance.", "Difficult",
   ["Readers meeting an ancient oral epic for the first time are often struck by its repetitions: the same phrase attached to the same hero, the same line describing every dawn.",
    "A modern editor would strike most of them out, on the principle that a good writer never says the same thing twice in the same words.",
    "That principle, however, belongs to a culture of the page, in which a writer can pause, revise and consult what has already been written.",
    "A singer composing aloud before an audience could do none of these things, and the stock phrases that look like padding were what let him keep the line moving while he thought ahead."],
   "Sentence [[1]] notes the repetitions. Sentence [[2]] gives the modern editor's verdict and 'the principle' behind it. Sentence [[3]] limits 'That principle' to a culture of the page, where one can pause, revise and consult. Sentence [[4]] says the oral singer 'could do none of these things' and so needed stock phrases. Sentence [[4]] explains the repetitions of sentence [[1]] and looks like their natural sequel, but 'none of these things' requires the list in sentence [[3]].",
   "Placing sentence [[4]] right after sentence [[1]] as the explanation of the repetitions, missing that 'none of these things' refers to pausing, revising and consulting.",
   "V01H-oral-epic-formulas", "The tempting order joins the singer to the repetitions he explains; rejecting it needs the referent of 'none of these things' and the argument's turn from the editor's principle to its limits.",
   traps=[("1423", "Sentence [[4]] explains the repetitions, but 'could do none of these things' points to the pausing, revising and consulting listed in sentence [[3]], so it cannot follow sentence [[1]]."),
          ("1324", "Sentence [[3]] limits 'That principle', which is the editor's principle stated in sentence [[2]].")],
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 023
pj("V01-H-023", "History and politics", "Optical telegraph towers relayed messages quickly but failed at night and in fog.", "Easy",
   ["In the late eighteenth century, chains of towers with movable arms were built across parts of Europe to send messages over long distances.",
    "An operator in each tower watched the next one through a telescope and copied the position of its arms, passing the signal along the line.",
    "In clear weather a short message could cross a whole country in a small fraction of the time a mounted courier would need.",
    "That speed came at a price, however: at night or in fog the towers could not see one another, and the line fell silent."],
   "Sentence [[1]] introduces the towers. Sentence [[2]] explains how an operator 'in each tower' relayed signals. Sentence [[3]] describes the resulting speed. Sentence [[4]] turns to the cost of 'That speed', which must follow sentence [[3]].",
   "Ending with sentence [[3]] because 'In clear weather' seems to answer the fog of sentence [[4]], which leaves 'That speed' with no speed to refer to.",
   "V01H-optical-semaphore-telegraph", "A description, mechanism, benefit and limitation, with 'That speed' locking the final pair.",
   traps=[("1243", "Sentence [[4]] begins 'That speed', which refers back to the fast transmission described in sentence [[3]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 024
pj("V01-H-024", "Economics and business", "Revenue from forgotten auto-renewals rests on inattention and so is fragile.", "Medium",
   ["Many subscriptions begin with a free trial that converts automatically into a paid plan unless the customer cancels in time.",
    "Firms favour this design because a good many customers who meant to cancel simply forget, or put it off until the deadline has passed.",
    "Revenue gathered in this way, however, rests on inattention rather than on any judgement by the customer that the service is worth its price.",
    "Such income is correspondingly fragile, since customers who notice the charge often leave resentfully, so a firm relying on forgotten renewals may be trading long-term goodwill for short-term revenue."],
   "Sentence [[1]] describes the trial that converts automatically. Sentence [[2]] explains why firms favour 'this design'. Sentence [[3]] says revenue 'gathered in this way' rests on inattention. Sentence [[4]] concludes that 'Such income is correspondingly fragile': the fragility corresponds to the inattention just described, so sentence [[4]] must follow sentence [[3]].",
   "Ending with sentence [[3]] because 'however' sounds like a final caution, which detaches 'correspondingly fragile' from the inattention it corresponds to.",
   "V01H-subscription-auto-renewal-pricing", "The last pair is fixed by the logic of the idea: fragility is inferred from the fact that the revenue rests on inattention.",
   traps=[("1243", "Sentence [[4]] calls the income 'correspondingly fragile', drawing on the point in sentence [[3]] that it rests on inattention; ending on sentence [[3]] leaves that inference without its premise.")],
   cognitive="Analysis")

# ------------------------------------------------------------------ 025
pj("V01-H-025", "History and politics", "Turnpike tolls fixed the mismatch of parish road labour by charging those who caused the wear, but created new local grievances.", "Difficult",
   ["Under the older system in England, each parish was responsible for the roads that ran through it, and local inhabitants were required to give a few days of unpaid labour every year to repair them.",
    "The arrangement worked tolerably for lanes used mainly by villagers, but it broke down on the main routes, where most of the wear came from carriers and coaches merely passing through.",
    "On those routes parishioners had little reason to labour hard on a road whose damage was done by strangers, and the great highways were often in a deplorable state.",
    "The turnpike trusts that spread in the eighteenth century addressed this mismatch by charging tolls, so that the cost of upkeep fell on those who caused the wear.",
    "The remedy created a grievance of its own, however, for local people making short journeys now found themselves paying tolls on roads they had once mended with their own hands."],
   "Sentence [[1]] describes parish road labour. Sentence [[2]] says where 'The arrangement' broke down: on main routes worn by through traffic. Sentence [[3]] gives the reason it broke down 'On those routes', with the 'strangers' who did the damage. Sentence [[4]] says the turnpike trusts addressed 'this mismatch' between who did the work and who caused the wear. Sentence [[5]] notes that 'The remedy' created its own grievance. Sentence [[2]] must precede sentence [[3]]: the claim that the system failed on main routes comes before the explanation, and 'On those routes' and the 'strangers' of sentence [[3]] point back to the main routes and the carriers and coaches introduced in sentence [[2]].",
   "Placing sentence [[3]] before sentence [[2]] because it explains the bad state of the roads, missing that its 'strangers' are first introduced as the carriers and coaches passing through.",
   "V01H-turnpike-toll-roads", "The middle pair depends on the logic of the idea (claim, then the incentive that explains it), and the mismatch must be fully stated before the remedy and its grievance.",
   traps=[("13245", "Sentence [[3]] begins 'On those routes' and speaks of damage 'done by strangers', which presuppose the distinction between village lanes and main routes and the through traffic introduced in sentence [[2]]."),
          ("12435", "Sentence [[4]] addresses 'this mismatch', between parish labour and wear caused by strangers, which is only complete once sentence [[3]] explains why parishioners would not maintain such roads.")],
   cognitive="Analysis", exams=DX)
