import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ 001 Easy, 4
pj("V01-A-001", "Philosophy and ethics", "When claims to an indivisible good are equal, a lottery is fair because of how it decides, not because of what it decides.", "Easy",
   ["Suppose a popular school has one remaining place and two applicants whose claims to it are, by every relevant measure, exactly equal.",
    "Giving the place to either child on the strength of some further feature, such as which parent argued more forcefully, would reward something that has no bearing on the claim.",
    "A lottery avoids this, because it gives each applicant the same chance and lets no irrelevant feature decide.",
    "Its fairness, in other words, lies not in the outcome, which still disappoints one family, but in the way the outcome was reached."],
   "Sentence [[1]] sets up the case ('Suppose') of one place and two equal claims. Sentence [[2]] refers to 'either child' from that case and shows what is wrong with deciding by a further feature. Sentence [[3]] says 'A lottery avoids this', where 'this' is the problem of rewarding an irrelevant feature described in [[2]]. Sentence [[4]] explains 'Its fairness', the lottery's, in general terms ('in other words').",
   "Placing sentence [[3]] straight after sentence [[1]] because the lottery seems to answer the case directly, which leaves 'avoids this' without the problem it avoids.",
   "V01A-fair-lottery", "Clear reference words ('either child', 'avoids this', 'Its fairness') fix the order once the opener is found.",
   traps=[("1324", "Sentence [[3]] says the lottery 'avoids this', and the thing avoided, rewarding a feature with no bearing on the claim, is described only in sentence [[2]]."),
          ("1243", "Sentence [[4]] begins 'Its fairness', which must refer to the lottery; before sentence [[3]] no lottery has been mentioned.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 002 Medium, 5
pj("V01-A-002", "Philosophy and ethics", "Consent is a matter of degree, because the weight of a 'yes' depends on how acceptable the alternatives to agreeing were.", "Medium",
   ["Consent is usually treated as a switch: either a person agreed to something or they did not.",
    "Yet an agreement given under heavy pressure, by a worker who will lose her job if she refuses extra hours, hardly carries the same moral weight as one freely offered.",
    "The difference lies not in the words spoken, which may be identical, but in the options the person had when speaking them.",
    "Where those options are bad enough, where refusing would cost her something she cannot afford to lose, her 'yes' tells us more about her circumstances than about her wishes.",
    "Consent is therefore better understood as a matter of degree, its weight depending on how acceptable the alternatives to agreeing actually were."],
   "Sentence [[1]] states the common all-or-nothing view of consent. Sentence [[2]] challenges it ('Yet') with the pressured worker. Sentence [[3]] explains 'The difference' between pressured and free agreement: it lies in the options available. Sentence [[4]] refers to 'those options' and applies the point to the worker, using 'her' from [[2]]. Sentence [[5]] concludes ('therefore') that consent comes in degrees, which reverses the switch picture of [[1]].",
   "Placing sentence [[4]] straight after sentence [[2]] because both describe the worker, which leaves 'those options' in sentence [[4]] without the options that sentence [[3]] introduces.",
   "V01A-degrees-of-consent", "Order depends mainly on the logic of the idea: the example must be explained by the idea of options before the options can be judged and the switch picture replaced.",
   traps=[("12435", "Sentence [[4]] speaks of 'those options', and options are introduced only in sentence [[3]] as what really separates pressured from free agreement."),
          ("13245", "Sentence [[3]] explains 'The difference', which needs the contrast between pressured and freely offered agreement drawn in sentence [[2]].")])

# ------------------------------------------------------------------ 003 Medium, 4
pj("V01-A-003", "Philosophy and ethics", "White lies seem costless, but by making praise unconditional they destroy what honest praise could tell a friend.", "Medium",
   ["White lies are usually defended as small kindnesses: telling a friend that a mediocre meal was delicious spares feelings and seems to cost nothing.",
    "The cost, however, is hidden rather than absent, because it falls on the meaning of praise itself.",
    "If everyone knows that compliments are given regardless of merit, then a compliment can no longer tell anyone that their work was actually good.",
    "The friend who is always told that the meal was wonderful thus loses the one thing an honest friend could offer, which is a reason to believe it."],
   "Sentence [[1]] states the usual defence of white lies, ending on the claim that they 'cost nothing'. Sentence [[2]] answers that claim: 'The cost, however, is hidden rather than absent' and locates it in 'the meaning of praise'. Sentence [[3]] explains that general mechanism: unconditional compliments carry no information. Sentence [[4]] returns to the friend and the meal and applies the mechanism ('thus'), so it must follow the general explanation in [[3]].",
   "Placing sentence [[4]] before sentence [[3]] because it mentions the friend and the meal from sentence [[1]], although its 'thus' depends on the principle that sentence [[3]] states.",
   "V01A-white-lies", "The last two sentences are ordered by logic (principle before application) rather than by a pronoun.",
   traps=[("1243", "Sentence [[4]] concludes with 'thus' that the friend has lost a reason to believe the praise, but that conclusion rests on the principle in sentence [[3]] that indiscriminate compliments carry no information."),
          ("1324", "Sentence [[3]] explains how praise loses meaning, but the claim that the cost falls on praise is introduced only in sentence [[2]], which also answers 'cost nothing' in sentence [[1]].")])

# ------------------------------------------------------------------ 004 Difficult, 5
pj("V01-A-004", "Philosophy and ethics", "The paradox of the heap forces a choice between an unlocatable sharp boundary and giving up vague words in strict reasoning.", "Difficult",
   ["Remove a single grain from a heap of sand and you still have a heap; no one seriously thinks that one grain could make that difference.",
    "Repeat the step patiently enough, though, and the same principle commits you to calling a lone grain, or even nothing at all, a heap.",
    "Something has to give, and the two obvious candidates each carry an unwelcome price.",
    "Denying the principle means insisting that somewhere there is an exact grain whose removal ends the heap, a boundary that no speaker could ever locate.",
    "Keeping it instead means conceding that words like 'heap', 'tall' and 'bald' cannot be trusted in strict reasoning at all, which asks far more of them than they were made for."],
   "Sentence [[1]] sets up the principle that one grain makes no difference. Sentence [[2]] shows that repeating the step leads to an absurd conclusion; 'the same principle' and 'the step' point back to [[1]]. Only once the contradiction is in view can sentence [[3]] say 'Something has to give' and announce two candidates. Sentence [[4]] takes the first candidate, denying the principle, and sentence [[5]] the alternative, 'Keeping it instead', where 'it' is the principle and 'instead' requires the option already stated in [[4]].",
   "Treating sentence [[3]] as a closing summary after both options, or opening with it, without noticing that 'Something has to give' presupposes the contradiction reached in sentence [[2]].",
   "V01A-heap-paradox", "Order depends mainly on the logic of the idea: the contradiction must be complete before 'Something has to give', and 'Keeping it instead' must answer the denial; the material is abstract and the two options look interchangeable at first glance.",
   traps=[("12453", "Sentence [[3]] could look like a summary, but [[4]] and [[5]] would then arrive with no announcement that there are two candidates, and 'Something has to give' after both responses makes no sense."),
          ("12354", "Sentence [[5]] says 'Keeping it instead', which only makes sense once the opposite option, denying the principle, has been stated in sentence [[4]].")],
   exams=D)

# ------------------------------------------------------------------ 005 Easy, 4
pj("V01-A-005", "Psychology", "More options help only until the effort of comparing and the risk of regret outweigh the benefit.", "Easy",
   ["Shoppers often say that they want as many options as possible, and shops compete with one another to provide them.",
    "Yet a page listing dozens of nearly identical phone plans can leave a customer more hesitant than a page listing only a handful.",
    "The reason is that each extra option adds to the effort of comparing, and raises the chance of later regret about the plans not chosen.",
    "More choice, in other words, is welcome only up to the point where that effort and that risk of regret begin to outweigh its rewards."],
   "Sentence [[1]] states the common belief that more options are better. Sentence [[2]] contradicts it with 'Yet' and the phone-plan example. Sentence [[3]] explains that observation ('The reason is'). Sentence [[4]] restates the conclusion in general terms ('in other words'), and its 'that effort and that risk of regret' points back to the reasons given in [[3]], so it must come last.",
   "Opening with sentence [[2]] because it contains the concrete example, although its 'Yet' needs the belief stated in sentence [[1]].",
   "V01A-choice-overload", "The order follows explicit connectives ('Yet', 'The reason is', 'in other words').",
   traps=[("2134", "Sentence [[2]] begins with 'Yet', which needs a prior claim to contrast with; that claim is the belief in sentence [[1]]."),
          ("1243", "Sentence [[4]] speaks of 'that effort and that risk of regret', which are named only in sentence [[3]], so sentence [[4]] cannot come before it.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 006 Easy, 5
pj("V01-A-006", "Psychology", "Repeated exposure breeds liking because ease of processing is mistaken for quality, which is how repetitive advertising persuades.", "Easy",
   ["People often come to like things simply because they have encountered them many times before.",
    "A song that seemed dull on first hearing, for example, can become a favourite after it has been played often enough on the radio.",
    "One explanation is that familiar things are easier to take in, and this ease is mistaken for a sign that the thing itself is good.",
    "Advertisers exploit exactly this confusion when they repeat a brand name far more often than any new information would require.",
    "Repetition of this kind persuades, if it does, not by argument but by making the product feel like something we already know."],
   "Sentence [[1]] states the general tendency. Sentence [[2]] illustrates it ('for example'). Sentence [[3]] offers 'One explanation', that ease of processing is mistaken for quality. Sentence [[4]] says advertisers exploit 'exactly this confusion', the mistake named in [[3]]. Sentence [[5]] comments on 'Repetition of this kind', the advertisers' repetition of [[4]].",
   "Placing sentence [[4]] right after sentence [[2]] because both give everyday examples, although 'this confusion' needs the explanation in sentence [[3]].",
   "V01A-mere-exposure", "General claim, example, explanation, application and comment, each with a clear link.",
   traps=[("12435", "Sentence [[4]] refers to 'exactly this confusion', which is the mistaking of ease for quality that sentence [[3]] describes."),
          ("13245", "Sentence [[2]] illustrates sentence [[1]] with 'for example'; after sentence [[3]] it would interrupt the link between the explanation and 'this confusion' in sentence [[4]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 007 Medium, 4
pj("V01-A-007", "Psychology", "An opening price anchors a negotiation because adjustments from it are too small, so a buyer should not accept a seller's anchor.", "Medium",
   ["In a negotiation over price, the first number mentioned tends to pull the final agreement towards itself, even when it was chosen with little justification.",
    "Each side adjusts away from that opening figure as talks proceed, but adjustments of this kind are usually too small.",
    "Because the adjustment falls short, a seller who opens high can end up with a better price than one who opens with a reasonable figure and waits to be talked up.",
    "For a buyer facing such a seller, the lesson is to name a figure first, or else to refuse to treat the seller's opening as the starting point of discussion."],
   "Sentence [[1]] states the anchoring tendency. Sentence [[2]] explains it: adjustments from 'that opening figure' are too small. Sentence [[3]] draws the consequence for a seller who opens high, and its opening 'Because the adjustment falls short' refers to the insufficient adjustment described in [[2]]. Sentence [[4]] draws the lesson for 'a buyer facing such a seller', that is, the high-opening seller of [[3]].",
   "Placing sentence [[3]] before sentence [[2]] because it follows naturally from the first number pulling the deal, missing that its opening 'Because the adjustment falls short' rests on the mechanism stated in sentence [[2]].",
   "V01A-price-anchoring", "Order depends mainly on the logic of the idea: the mechanism (too small adjustment) must come before the consequence for sellers and the lesson for buyers.",
   traps=[("1324", "Sentence [[3]] begins 'Because the adjustment falls short', but no adjustment has been mentioned until sentence [[2]]; moving sentence [[2]] later also separates sentence [[4]] from 'such a seller'."),
          ("1243", "Sentence [[4]] speaks of 'such a seller', the one who opens high, who is introduced only in sentence [[3]].")])

# ------------------------------------------------------------------ 008 Difficult, 4
pj("V01-A-008", "Psychology", "The view that emotions are judgements explains why anger fades when beliefs change, but persistent fear despite knowledge suggests emotions are not only judgements.", "Difficult",
   ["On one influential view, an emotion is a kind of judgement: to be angry, for instance, is to judge that one has been wronged.",
    "The view neatly explains why anger usually fades once we learn that an apparent insult was an accident, since the judgement on which it rested has been withdrawn.",
    "It struggles, however, with the traveller who knows perfectly well that flying is safer than driving and is terrified on every flight all the same.",
    "If her fear were simply a judgement of danger, her knowledge should dissolve it, and its persistence suggests that emotions answer partly to something older and less easily corrected than belief."],
   "Sentence [[1]] states the view that emotions are judgements. Sentence [[2]] gives its success: anger fades when the judgement is withdrawn. Sentence [[3]] turns ('however') to a case the view handles badly, and its 'however' needs the success in [[2]]. Sentence [[4]] analyses 'her fear', the traveller's from [[3]], and draws the conclusion that emotions are not only judgements.",
   "Placing sentence [[3]] right after sentence [[1]] because its 'It struggles' can seem to answer the view directly, which separates the traveller from 'her fear' in sentence [[4]] and leaves 'however' with no success to qualify.",
   "V01A-emotions-as-judgements", "Order depends mainly on the logic of the idea: success of a theory, its counterexample and the lesson drawn from the counterexample must come in that sequence; the content is abstract and the counterexample can look like it belongs anywhere after the view.",
   traps=[("1324", "Sentence [[3]] can follow the view directly, but sentence [[4]] then comes after the anger example, and 'her fear' must sit next to the traveller it refers to."),
          ("1243", "Sentence [[4]] speaks of 'her fear' and 'her knowledge', which need the traveller of sentence [[3]] to be introduced first.")],
   exams=D)

# ------------------------------------------------------------------ 009 Easy, 4
pj("V01-A-009", "Society and culture", "Cultures read conversational silence differently, so speakers from different traditions can misjudge one another without meaning offence.", "Easy",
   ["How long a pause in conversation can last before it feels awkward varies a great deal from one culture to another.",
    "In some places a silence of several seconds is a sign of respect, showing that the listener is giving thought to what was said.",
    "Elsewhere the same silence is read as disagreement or discomfort, and speakers hurry to fill it with words.",
    "When people from these two traditions talk, each may misjudge the other, one as evasive and the other as rash, without either intending any offence."],
   "Sentence [[1]] states that the tolerance for pauses varies across cultures. Sentence [[2]] gives one case ('In some places'). Sentence [[3]] gives the contrasting case ('Elsewhere the same silence'). Sentence [[4]] refers to 'these two traditions' and describes the misunderstanding between them.",
   "Opening with sentence [[2]] because it is concrete, although the general claim in sentence [[1]] is what the two contrasting cases illustrate.",
   "V01A-conversational-silence", "General claim, two contrasting cases and the consequence, each signposted.",
   traps=[("2314", "Sentence [[1]] states the general claim that sentences [[2]] and [[3]] illustrate; placed after them it would interrupt the move to 'these two traditions' in sentence [[4]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 010 Medium, 4
pj("V01-A-010", "Society and culture", "Cheap paperbacks were feared as a threat to serious reading but widened readership for every kind of book.", "Medium",
   ["When cheap paperback editions first became widely available, some critics warned that they would lower the standard of literature along with the price of books.",
    "Their fear was that publishers chasing mass sales would print mainly sensational fiction and crowd out serious work.",
    "What actually happened was more mixed: sensational fiction did multiply, but classics and serious essays also reached readers who had never been able to afford hardbound copies.",
    "The episode suggests that lowering the cost of access tends to enlarge every kind of reading at once, rather than simply replacing the better kind with the worse."],
   "Sentence [[1]] introduces the critics' warning about cheap paperbacks. Sentence [[2]] spells out 'Their fear'. Sentence [[3]] reports 'What actually happened', which answers the fear. Sentence [[4]] draws the general lesson from 'The episode'.",
   "Placing sentence [[4]] before sentence [[3]] as if the general lesson came first, although 'The episode suggests' depends on the outcome reported in sentence [[3]].",
   "V01A-paperback-readership", "The expectation and outcome pair must be read for sense: the lesson in the last sentence follows from the mixed outcome, not from the fear.",
   traps=[("1243", "Sentence [[4]] draws a lesson that contradicts the critics, but the evidence for it, the mixed outcome, appears only in sentence [[3]]."),
          ("1324", "Sentence [[3]] answers a specific fear, crowding out by sensational fiction, which is stated only in sentence [[2]].")])

# ------------------------------------------------------------------ 011 Medium, 5
pj("V01-A-011", "Society and culture", "Minority languages are lost through reasonable family choices, so lasting revival gives the language practical use rather than appealing only to pride.", "Medium",
   ["Minority languages are lost far less often through outright prohibition than one might suppose.",
    "More commonly they fade within a few generations, as parents decide that their children's prospects lie in the language of schools and employers.",
    "Each such decision is reasonable on its own terms, which is precisely what makes the overall loss so hard to reverse.",
    "Campaigns that appeal only to heritage and pride ask families to set aside the very calculation that led them to switch in the first place.",
    "Efforts that last tend instead to give the language practical uses, in local media, administration or trade, so that speaking it no longer feels like a sacrifice."],
   "Sentence [[1]] sets aside prohibition as the usual cause. Sentence [[2]] gives the more common cause, parents' decisions. Sentence [[3]] comments on 'Each such decision': being reasonable, the decisions are hard to reverse. Sentence [[4]] explains why appeals to pride fail against that reasonable calculation. Sentence [[5]] offers the alternative that works ('instead').",
   "Placing sentence [[4]] right after sentence [[2]], since both mention families' choices, which separates 'Each such decision' in sentence [[3]] from the decisions it refers to.",
   "V01A-language-shift", "Order depends mainly on the logic of the idea: the reasonableness of each family's choice must be established before the paragraph can explain why appeals to pride fail and what works instead.",
   traps=[("12435", "Sentence [[3]] says 'Each such decision', which must sit next to the parents' decisions in sentence [[2]]; after sentence [[4]] it would refer to campaigns."),
          ("12354", "Sentence [[5]] describes efforts that work 'instead', a contrast with the failing campaigns that sentence [[4]] must first describe.")])

# ------------------------------------------------------------------ 012 Medium, 4
pj("V01-A-012", "Society and culture", "First-name address at work removes the outward sign of rank, not rank itself, which may make power harder to question.", "Medium",
   ["Many workplaces have abandoned titles and surnames, so that a junior clerk now addresses the managing director by her first name.",
    "The change is often celebrated as a flattening of hierarchy, a sign that everyone is now treated as an equal.",
    "Yet the director still decides who is promoted and who is let go, so the equality being celebrated extends only to the way people speak to one another.",
    "What has disappeared is the outward marker of rank rather than rank itself, which may make power harder to see and therefore harder to question."],
   "Sentence [[1]] describes the shift to first names. Sentence [[2]] reports how 'The change' is celebrated, as making everyone equal. Sentence [[3]] answers with 'Yet': the director still holds power, so 'the equality being celebrated', the equality claimed in [[2]], is only verbal. Sentence [[4]] states the conclusion about outward markers and real rank.",
   "Placing sentence [[3]] right after sentence [[1]], since 'Yet the director still decides' seems to answer the first-name example directly, which leaves 'the equality being celebrated' without the celebration it refers to.",
   "V01A-first-name-address", "The middle pair is ordered by sense: the rebuttal must follow the celebration it rebuts, and both sentences can look like the second.",
   traps=[("1324", "Sentence [[3]] limits 'the equality being celebrated', and the celebration is reported only in sentence [[2]]; placed before it, the rebuttal would precede the view it rebuts.")])

# ------------------------------------------------------------------ 013 Difficult, 5
pj("V01-A-013", "Society and culture", "A gift creates an indefinite obligation: neither non-return nor exact immediate repayment preserves the relationship.", "Difficult",
   ["A gift appears to be the one transaction in which nothing at all is expected in return.",
    "Yet in many societies a gift that is never reciprocated slowly sours the relationship it was meant to strengthen.",
    "Oddly, repaying it at once, with something of exactly equal value, can give offence as well.",
    "An immediate and precise return turns the exchange into a purchase, cancelling the debt and with it the bond.",
    "What the gift creates, then, is neither a demand for payment nor a freedom from all obligation, but a lasting and slightly indefinite debt, and it is the indefiniteness that keeps the relationship alive."],
   "Sentence [[1]] states the appearance that gifts expect nothing. Sentence [[2]] contradicts it ('Yet'): an unreturned gift sours the relationship. Sentence [[3]] adds the opposite failure, and its 'as well' requires the first kind of offence from [[2]]. Sentence [[4]] explains why exact immediate repayment offends, so it must follow [[3]]. Sentence [[5]] combines both failures ('then') into the conclusion that the gift creates an indefinite debt.",
   "Placing sentence [[3]] before sentence [[2]] because 'Oddly' seems to answer the opening claim directly, missing that 'as well' needs an earlier offence.",
   "V01A-gift-obligation", "Order depends mainly on the logic of the idea: two opposite failures must both be in place before the conclusion, and the 'as well' that orders them is easy to overlook.",
   traps=[("13245", "Sentence [[3]] says exact repayment can give offence 'as well', so the first offence, the unreturned gift of sentence [[2]], must come before it; sentence [[4]] would also be cut off from the repayment it explains."),
          ("12435", "Sentence [[4]] explains why an immediate and precise return offends, which assumes that sentence [[3]] has already raised the case of repaying at once.")],
   exams=D)

# ------------------------------------------------------------------ 014 Easy, 4
pj("V01-A-014", "History and politics", "Canals were once the cheapest freight carriers but lost their traffic to railways and survive mainly for leisure.", "Easy",
   ["For a time, canals were the cheapest way of moving heavy goods such as coal and stone across parts of Europe.",
    "A single horse walking along the towpath could pull a barge carrying far more than any cart on the roads of the day.",
    "Once railways spread, however, they offered speed as well as capacity, and most canals steadily lost their traffic.",
    "Many of those that survive are now used mainly for leisure, a quiet afterlife for what was once vital industrial transport."],
   "Sentence [[1]] introduces canals as the cheapest freight route. Sentence [[2]] explains why, with the horse and barge. Sentence [[3]] turns ('however') to the railways that took their traffic. Sentence [[4]] describes 'those that survive', which presupposes the decline in [[3]].",
   "Placing sentence [[3]] before sentence [[2]], although the horse and barge explain the cheapness claimed in sentence [[1]] and belong before the decline.",
   "V01A-canal-decline", "Chronology and a clear 'however' mark the order.",
   traps=[("1324", "Sentence [[2]] supports the cheapness claimed in sentence [[1]]; after the railways in sentence [[3]] it would break the link between the decline and the canals 'that survive' in sentence [[4]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 015 Medium, 4
pj("V01-A-015", "History and politics", "Standard spelling emerged gradually from printing habits rather than from deliberate reform.", "Medium",
   ["Before printing, a single English word might be spelled in several ways, sometimes by the same scribe on the same page.",
    "Printing did not abolish this variety at once, since early printers sometimes adjusted spellings simply to fit a line of type.",
    "Over time, however, the repetition of the same forms across thousands of copies gave readers a sense that one spelling was correct.",
    "The standard that dictionaries later recorded was thus less a deliberate reform than the slow sediment of habits formed in the print shop."],
   "Sentence [[1]] describes spelling variety before printing. Sentence [[2]] says printing 'did not abolish this variety at once', referring back to [[1]]. Sentence [[3]] turns ('Over time, however') to the gradual effect of repetition. Sentence [[4]] concludes ('thus') that the standard grew out of print habits.",
   "Placing sentence [[3]] directly after sentence [[1]] because it describes the effect of printing, which leaves 'however' with no immediate claim to qualify.",
   "V01A-print-spelling", "Chronology plus a concession and its reversal; the 'however' in the third sentence must answer the second.",
   traps=[("1324", "Sentence [[3]] opens 'Over time, however', which reverses the claim in sentence [[2]] that printing did not end variety at once; directly after sentence [[1]] there is nothing to reverse.")])

# ------------------------------------------------------------------ 016 Medium, 5
pj("V01-A-016", "History and politics", "Censuses were instruments of state reach rather than neutral description, because being counted made people visible to taxation and conscription.", "Medium",
   ["A government that wants to tax, conscript or feed its population must first know who that population is and where it lives.",
    "Early censuses were undertaken for exactly these purposes, and people often had good reason to fear the officials who came to count them.",
    "Their fear was well founded, since being counted made a household visible, and visibility was the precondition of being taxed or summoned.",
    "It is hardly surprising, then, that people wishing to stay beyond a state's reach have sometimes avoided being counted, giving false numbers or simply being away when the officials came.",
    "Such evasion, like the fear that prompted it, suggests that the census is less a neutral act of description than an instrument through which a state extends its reach."],
   "Sentence [[1]] states what a government needs to know in order to tax, conscript or feed people. Sentence [[2]] says early censuses served 'exactly these purposes', the three named in [[1]], and that people feared the counters. Sentence [[3]] explains 'Their fear', which needs [[2]]. Sentence [[4]] draws the consequence ('then') that people avoided being counted. Sentence [[5]] refers to 'Such evasion', the avoidance described in [[4]], and draws the general reinterpretation of the census.",
   "Placing sentence [[4]] straight after sentence [[2]] because both describe people's response to the counters, which separates 'Their fear' in sentence [[3]] from the fear it refers to.",
   "V01A-census-and-state", "Order depends mainly on the logic of the idea: purpose, fear, the reason the fear was justified, the response and the reinterpretation form a causal chain.",
   traps=[("12435", "Sentence [[3]] begins 'Their fear', which must follow the fear of the officials mentioned in sentence [[2]]; after sentence [[4]] it would refer to people avoiding the count, and the 'then' of sentence [[4]] would lack its reason."),
          ("13245", "Sentence [[3]] explains 'Their fear', and no one has been said to fear anything until sentence [[2]]."),
          ("12354", "Sentence [[5]] begins 'Such evasion', and the evasion, people avoiding the count or giving false numbers, is described only in sentence [[4]].")])

# ------------------------------------------------------------------ 017 Difficult, 4
pj("V01-A-017", "History and politics", "Complaints of decline found in every age cannot all be true, so they reveal how each age compares its present with a selectively remembered past.", "Difficult",
   ["Complaints that manners, learning or public life have declined since some better age can be found in the writings of a great many periods.",
    "If each generation's complaint were accurate, the decline would have been continuous for thousands of years, leaving the present unimaginably worse than any past.",
    "Since that conclusion is absurd, the complaints are better read as evidence about those who make them than about the times they describe.",
    "What such evidence shows, most likely, is a habit of comparing an untidy present with a past known only through what was worth remembering, a contest the past always wins."],
   "Sentence [[1]] observes that complaints of decline recur across many periods. Sentence [[2]] tests them: if all were accurate, decline would be continuous and the present unimaginably bad. Sentence [[3]] rejects 'that conclusion' as absurd and reinterprets the complaints as 'evidence about those who make them'. Sentence [[4]] says what 'such evidence' shows about the complainers, so it must follow [[3]].",
   "Moving sentence [[4]] forward as an explanation of the complaints in sentence [[1]], missing that 'such evidence' refers to the reinterpretation reached only in sentence [[3]].",
   "V01A-golden-age-complaints", "Order depends mainly on the logic of the idea: a reduction to absurdity has to be run before the complaints can be reinterpreted, and the explanatory sentence tempts as an early or opening sentence.",
   traps=[("1423", "Sentence [[4]] can look like an explanation of the complaints in sentence [[1]], but it speaks of 'such evidence', and the complaints become evidence about their makers only in sentence [[3]]."),
          ("4123", "Sentence [[4]] has a general ring that tempts as an opener, but 'such evidence' needs a prior mention of evidence, which only sentence [[3]] supplies.")],
   exams=D)

# ------------------------------------------------------------------ 018 Easy, 5
pj("V01-A-018", "Economics and business", "Prices ending in nine exploit left-to-right reading, which is also why some upmarket shops prefer round prices.", "Easy",
   ["Many prices in shops end in nine, so that an item is marked at 499 rupees rather than at a round 500.",
    "The difference of a single rupee is trivial, yet sellers persist with the practice in almost every kind of shop.",
    "One explanation is that shoppers read prices from left to right and give most weight to the first digit they see.",
    "A price beginning with four then feels distinctly cheaper than one beginning with five, even though the gap is almost nothing.",
    "Some upmarket shops deliberately avoid such endings for the same reason, preferring round figures that suggest quality rather than a bargain."],
   "Sentence [[1]] introduces prices ending in nine. Sentence [[2]] notes the puzzle: 'The difference of a single rupee' is trivial yet the practice persists. Sentence [[3]] offers 'One explanation'. Sentence [[4]] works out its consequence ('then') for a price beginning with four. Sentence [[5]] says some shops avoid 'such endings for the same reason', that such prices feel like bargains.",
   "Placing sentence [[5]] right after sentence [[2]] as a second observation about pricing, although 'for the same reason' needs the explanation in sentences [[3]] and [[4]].",
   "V01A-charm-pricing", "Observation, puzzle, explanation, consequence and a contrasting case, each with a clear link.",
   traps=[("12534", "Sentence [[5]] says upmarket shops avoid such endings 'for the same reason', which has not been given until sentences [[3]] and [[4]]."),
          ("13245", "Sentence [[3]] offers 'One explanation', which needs the puzzle of the trivial rupee in sentence [[2]] to explain.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 019 Easy, 4
pj("V01-A-019", "Economics and business", "Spent money should not affect decisions to continue, yet managers keep funding failing projects to avoid admitting waste.", "Easy",
   ["Money already spent on a project cannot be recovered, whatever its managers decide to do about the project next.",
    "Logically, then, that spending should play no part in deciding whether the project ought to continue.",
    "In practice, managers often keep funding failing projects precisely because so much has already gone into them.",
    "Abandoning the project feels like admitting that the earlier spending was wasted, even though continuing only adds to the waste."],
   "Sentence [[1]] states that spent money is unrecoverable. Sentence [[2]] draws the logical consequence ('then'). Sentence [[3]] contrasts what happens 'In practice' with what logic says. Sentence [[4]] explains why managers continue.",
   "Opening with sentence [[3]], the concrete behaviour, although 'In practice' needs the logical rule of sentence [[2]] to contrast with.",
   "V01A-sunk-cost", "Theory then practice, marked by 'Logically, then' and 'In practice'.",
   traps=[("3412", "Sentence [[3]] contrasts practice with logic, so the logical rule in sentences [[1]] and [[2]] must come first.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 020 Medium, 4
pj("V01-A-020", "Economics and business", "Even a country more efficient at everything gains from trade, because what matters is what each gives up to produce a good.", "Medium",
   ["Suppose one country can produce both machine parts and textiles with less labour than its neighbour needs for either.",
    "It might seem that such a country has nothing to gain from trade, since it can make everything more cheaply at home.",
    "But every hour spent on textiles is an hour not spent on machine parts, so what matters is which good each country gives up least to produce.",
    "If each specialises in the good it sacrifices least to make and trades for the other, both can end up with more of each than they could produce alone."],
   "Sentence [[1]] sets up the case of a country more efficient at both goods. Sentence [[2]] states the tempting inference about 'such a country'. Sentence [[3]] rejects it ('But') by shifting attention to what each country gives up. Sentence [[4]] draws the conclusion from that idea of sacrifice: specialising in the good each gives up least to make benefits both.",
   "Placing sentence [[4]] before sentence [[3]], although the idea of the good a country 'sacrifices least to make' is introduced only by the reasoning in sentence [[3]].",
   "V01A-comparative-advantage", "Order depends mainly on the logic of the idea: the paragraph moves from a case, to a tempting inference, to its correction and the conclusion that follows only from the correction.",
   traps=[("1243", "Sentence [[4]] relies on the notion of the good each country 'sacrifices least to make', which sentence [[3]] establishes by pointing out that every hour has another use."),
          ("2134", "Sentence [[2]] speaks of 'such a country', which needs the case set up in sentence [[1]].")])

# ------------------------------------------------------------------ 021 Medium, 4
pj("V01-A-021", "Economics and business", "A large store's low rent in a shopping centre pays for the customers it draws to the smaller shops, whose higher rents cover the cost.", "Medium",
   ["In a large shopping centre, the department store at one end often pays far less rent for each square metre than the small boutiques along the corridors.",
    "This looks like favouritism until one asks why shoppers come to the centre at all.",
    "Many of them come for the large store, and on their way to it they pass, and sometimes enter, the smaller shops.",
    "The low rent is therefore a payment for a service, the traffic the large store brings to everyone else, which the landlord recovers through the higher rents of its neighbours."],
   "Sentence [[1]] states the puzzling fact about rents. Sentence [[2]] calls 'This' apparent favouritism and raises the question of why shoppers come. Sentence [[3]] answers it: 'Many of them', the shoppers of [[2]], come for the large store and pass the small ones. Sentence [[4]] concludes ('therefore') that the low rent pays for the traffic.",
   "Placing sentence [[3]] before sentence [[2]] because it explains the rent difference, which leaves 'Many of them' without the shoppers it refers to.",
   "V01A-anchor-store-rents", "Order depends mainly on the logic of the idea: a puzzle, the question that reframes it, its answer and the conclusion; the explanatory sentence tempts as an early move.",
   traps=[("1324", "Sentence [[3]] begins 'Many of them', which refers to the shoppers introduced in the question of sentence [[2]]; placed earlier it has no referent."),
          ("1243", "Sentence [[4]] concludes that the low rent pays for traffic, which needs the fact in sentence [[3]] that shoppers come for the large store and pass the small ones.")])

# ------------------------------------------------------------------ 022 Easy, 4
pj("V01-A-022", "Science and environment", "Antibiotics select for resistant survivors, so unnecessary prescriptions carry a real cost.", "Easy",
   ["An antibiotic kills most of the bacteria it reaches, but a few may survive because of chance mutations that happen to protect them.",
    "These survivors then multiply with less competition, passing their protection on to their descendants.",
    "Every unnecessary course of treatment therefore gives resistant strains another opportunity to spread.",
    "It is this added opportunity that makes prescribing antibiotics for illnesses they cannot treat, such as common viral infections, not harmless caution but a real cost."],
   "Sentence [[1]] describes survival by chance mutation. Sentence [[2]] continues with 'These survivors'. Sentence [[3]] draws a consequence ('therefore') about unnecessary treatment. Sentence [[4]] applies it to prescribing for viral infections, and 'this added opportunity' points back to the 'another opportunity to spread' of [[3]].",
   "Placing sentence [[4]] before sentence [[3]], although 'this added opportunity' rests on the claim in sentence [[3]] that unnecessary treatment spreads resistance.",
   "V01A-antibiotic-resistance", "A short causal chain with clear reference words.",
   traps=[("1243", "Sentence [[4]] speaks of 'this added opportunity', which needs the 'another opportunity to spread' stated in sentence [[3]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 023 Medium, 5
pj("V01-A-023", "Science and environment", "Vaccination's indirect protection tempts individuals to free-ride, and widespread free-riding destroys that protection.", "Medium",
   ["A vaccine protects not only the person who receives it but also, indirectly, the people around them.",
    "When enough members of a community are immune, an infection that enters it finds too few susceptible hosts to keep spreading, and it dies out.",
    "Those who cannot be vaccinated, such as very young infants, are then shielded by the immunity of others.",
    "This shared protection, however, creates a temptation: each person may reason that, with everyone else immunised, their own vaccination adds little.",
    "If enough people act on that reasoning, immunity falls below the level at which it works, and the protection that made the reasoning plausible disappears."],
   "Sentence [[1]] states that vaccines protect others indirectly. Sentence [[2]] explains how, by starving an infection of hosts. Sentence [[3]] names who benefits ('then'), those who cannot be vaccinated. Sentence [[4]] turns ('however') to the temptation that 'This shared protection' creates. Sentence [[5]] follows 'that reasoning' to its self-defeating result.",
   "Placing sentence [[3]] before sentence [[2]] because both describe who is protected, although 'then' in sentence [[3]] depends on the mechanism of too few hosts.",
   "V01A-herd-immunity", "Order depends mainly on the logic of the idea: mechanism, beneficiaries, temptation and its self-defeating result form a chain that must be followed for sense.",
   traps=[("13245", "Sentence [[3]] says infants are 'then' shielded, which follows from the infection dying out for lack of hosts in sentence [[2]]."),
          ("12354", "Sentence [[5]] refers to 'that reasoning', which is the free-riding thought set out in sentence [[4]].")])

# ------------------------------------------------------------------ 024 Medium, 4
pj("V01-A-024", "Science and environment", "Geologists resisted continental drift for lack of a mechanism, not simply from closed minds, and accepted it once ocean-floor evidence supplied one.", "Medium",
   ["When it was first proposed, early in the twentieth century, that the continents had once been joined and had since drifted apart, most geologists rejected the idea.",
    "Their resistance is sometimes told as a story of closed minds, but they had a serious objection: no one could explain what force could move a continent.",
    "The fit of coastlines and the matching fossils on distant shores were suggestive, yet without a mechanism they could not overcome that objection.",
    "Only when studies of the ocean floor in the middle decades of the century revealed new crust forming at undersea ridges did the theory gain wide acceptance."],
   "Sentence [[1]] introduces the proposal and its rejection. Sentence [[2]] explains 'Their resistance' with the objection about force. Sentence [[3]] says the evidence could not overcome 'that objection'. Sentence [[4]] gives the turning point ('Only when') that supplied the missing mechanism.",
   "Placing sentence [[3]] before sentence [[2]] because the coastline evidence seems to belong with the original proposal, which leaves 'that objection' without a referent.",
   "V01A-continental-drift", "Chronology plus a backward reference ('that objection') and a final 'Only when'; the evidence sentence tempts toward the opening.",
   traps=[("1324", "Sentence [[3]] refers to 'that objection', and the objection, that no force could move a continent, is stated only in sentence [[2]].")])

# ------------------------------------------------------------------ 025 Difficult, 4
pj("V01-A-025", "Science and environment", "When a condition is rare, most positive results from even a highly accurate test are false alarms, so accuracy alone does not say what a positive result means.", "Difficult",
   ["Most people assume that if a medical test is highly accurate, a positive result from it must almost certainly be correct.",
    "Consider such a test, one that is right ninety-nine times in a hundred, used to screen for a condition that affects one person in ten thousand.",
    "Among every ten thousand people screened, about a hundred healthy ones will be wrongly flagged, against the single person who is actually ill.",
    "A positive result from such a test is therefore far more likely to be a false alarm than a diagnosis, which is why accuracy means little until we know how rare the condition is."],
   "Sentence [[1]] states the common assumption about accurate tests. Sentence [[2]] says 'Consider such a test', referring to the highly accurate test of [[1]], and adds the rarity of the condition. Sentence [[3]] works out the numbers, which requires both the error rate and the rarity given in [[2]]. Sentence [[4]] draws the conclusion ('therefore') that overturns the assumption of [[1]].",
   "Opening with the concrete test in sentence [[2]] and treating the assumption in sentence [[1]] as a later aside, missing that 'such a test' refers back to the accurate test of sentence [[1]].",
   "V01A-base-rates", "Order depends mainly on the logic of the idea: the arithmetic in the third sentence needs the setup of the second, and the conclusion overturns the opening assumption; the statistical reasoning is counterintuitive.",
   traps=[("2134", "Sentence [[2]] tempts as an opener because it is concrete, but 'such a test' refers back to the highly accurate test described in sentence [[1]]."),
          ("1324", "Sentence [[3]] counts healthy people wrongly flagged among ten thousand, figures that make sense only once sentence [[2]] has given the error rate and the rarity of the condition.")],
   exams=D)

