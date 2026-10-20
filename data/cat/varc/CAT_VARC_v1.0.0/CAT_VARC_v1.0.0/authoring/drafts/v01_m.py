import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ---------------------------------------------------------------- 001 problem of induction
pj("V01-M-001", "Philosophy and ethics",
   "Neither logic nor experience can justify the premise that the future will resemble the past, and philosophers respond in two ways.",
   "Difficult",
   ["Our confidence that bread will nourish us tomorrow, or that the sun will rise, rests on an unstated premise: that the future will resemble the past.",
    "Logic cannot supply that premise, since there is no contradiction in supposing that nature might change its course tomorrow.",
    "Experience is no better placed, for to argue that the future will resemble the past because it always has done so is to assume the very premise in question.",
    "Faced with this dilemma, some philosophers have concluded that inductive inference is not rationally justified at all, but merely a habit of mind.",
    "A second response holds that the demand was misplaced from the start, since induction is part of what we mean by reasoning well and needs no deeper foundation."],
   "Sentence [[1]] states the unstated premise behind everyday expectations. Sentence [[2]] tries the first possible source of justification, logic, and refers to 'that premise'. Sentence [[3]] says experience is 'no better placed', a comparison that only makes sense after one source has already failed, so it follows sentence [[2]]. The two failures together form 'this dilemma' of sentence [[4]], which gives the first response. Sentence [[5]], 'A second response', must come after the first.",
   "Putting sentence [[3]] straight after sentence [[1]] because experience seems the obvious first place to look, missing that 'no better placed' compares experience with a source already rejected.",
   "V01M-problem-of-induction",
   "Abstract argument with few explicit connectives; the order of the two horns depends on the comparative 'no better placed', and 'this dilemma' needs both horns before it.",
   traps=[("13245", "Experience cannot be 'no better placed' when nothing has yet been tried; the comparison needs the failure of logic in sentence [[2]] first."),
          ("12354", "Sentence [[5]] calls itself 'A second response', so it cannot precede the first response given in sentence [[4]].")],
   exams=D)

# ---------------------------------------------------------------- 002 slippery slope
pj("V01-M-002", "Philosophy and ethics",
   "Whether a slippery slope argument fails depends on what is supposed to carry us from one step to the next.",
   "Medium",
   ["Slippery slope arguments warn that a modest step, harmless in itself, will lead by stages to an outcome that nobody wants.",
    "Such arguments are often dismissed as fallacies, but whether they fail depends on what is supposed to carry us down the slope, and two cases must be distinguished.",
    "If each step merely makes the next one conceivable, the warning is weak, since conceivability is cheap and most conceivable steps are never taken.",
    "If, however, each step changes the incentives or precedents that govern the next decision, the slope may be real and the warning deserves a hearing."],
   "Sentence [[1]] defines the slippery slope argument. Sentence [[2]] refers to 'Such arguments' and announces that 'two cases must be distinguished'. Sentences [[3]] and [[4]] are those two cases, and sentence [[4]] begins 'If, however', contrasting with the weak case of sentence [[3]], so it comes last.",
   "Ending with sentence [[2]] as a summary, which leaves its announcement of 'two cases' pointing at nothing.",
   "V01M-slippery-slope-arguments",
   "The order depends on the logic of setting up a distinction and then giving its two branches; the sentence that announces the distinction can look like a closing judgement.",
   traps=[("1342", "Sentence [[2]] announces that two cases 'must be distinguished'; placed last it introduces a distinction that has already been drawn.")])

# ---------------------------------------------------------------- 003 Buridan's ass
pj("V01-M-003", "Philosophy and ethics",
   "The parable of the starving donkey shows that the ability to choose without a reason supports rationality.",
   "Medium",
   ["An old parable describes a donkey placed exactly midway between two identical bales of hay, which starves because it has no reason to prefer either.",
    "The story is absurd as zoology, since any real animal would simply start eating, but it poses a genuine puzzle for theories of rational choice.",
    "Put abstractly, the puzzle is this: if rational agents act only on reasons, an agent facing two perfectly equal options seems to have no rational way to begin.",
    "The real animal's escape, an arbitrary choice, suggests that the capacity to pick without a reason is not a flaw in rationality but one of its necessary supports."],
   "Sentence [[1]] tells the parable. Sentence [[2]] calls it 'The story', notes that 'any real animal would simply start eating' and says it poses 'a genuine puzzle'. Sentence [[3]] states 'the puzzle' abstractly. Sentence [[4]] resolves it by returning to 'The real animal's escape' mentioned in sentence [[2]]; a resolution must follow the statement of the problem.",
   "Placing sentence [[4]] right after sentence [[2]] because both mention the real animal, so that the resolution comes before the puzzle has been stated.",
   "V01M-buridans-ass-indecision",
   "The last two sentences must be ordered by the logic of problem before solution; the shared mention of the real animal tempts students to put the resolution straight after the story.",
   traps=[("1243", "Sentence [[4]] answers the puzzle, so it cannot come before sentence [[3]], which first states what the puzzle is.")])

# ---------------------------------------------------------------- 004 universalisability
pj("V01-M-004", "Philosophy and ethics",
   "The universalisability test condemns lying promises but also harmless policies, so it needs a better way of describing actions.",
   "Difficult",
   ["One influential test in ethics asks whether the principle behind an action could be willed as a rule that everyone follows.",
    "A lying promise fails the test neatly: if everyone made promises they meant to break, nobody would accept a promise, and the lie could not even be told.",
    "Critics point out that the test seems to condemn harmless policies just as readily, such as playing tennis on Sunday mornings because the courts are empty, which would defeat itself if everyone did it.",
    "What the test needs, then, is a way of describing actions that separates the deceiver's principle from the tennis player's, and supplying it has proved harder than it first appears."],
   "Sentence [[1]] introduces the test. Sentence [[2]] shows the test working on a lying promise, which defeats itself when universalised. Sentence [[3]] says the test condemns harmless policies 'just as readily', a comparison that requires the successful case of sentence [[2]] to come first. Sentence [[4]] draws the conclusion 'then' and names both 'the deceiver' and 'the tennis player', so it must come last.",
   "Reading the critics' objection as the natural follow-up to the definition and placing sentence [[3]] second, which leaves 'just as readily' without anything to compare with.",
   "V01M-universalisability-of-maxims",
   "Students must see that the tennis case has the same self-defeating structure as the lying promise; the order turns on the comparison 'just as readily' rather than on pronouns.",
   traps=[("1324", "The objection says the test condemns harmless policies 'just as readily' as something else; that something is the lying promise of sentence [[2]], which must come first."),
          ("1342", "Sentence [[4]] refers to 'the deceiver', who appears only in sentence [[2]], so sentence [[2]] cannot come after it.")],
   exams=D)

# ---------------------------------------------------------------- 005 decoy effect
pj("V01-M-005", "Psychology",
   "A decoy option is added not to be bought but to make a neighbouring option look better.",
   "Easy",
   ["Imagine a gym offering two memberships, a monthly plan and a much pricier annual one, and finding that most new members pick the monthly plan.",
    "The owner then introduces a six-month plan that costs almost as much as the annual membership.",
    "Hardly anyone signs up for the new six-month plan, but annual memberships climb, because the annual plan now looks generous beside its costly neighbour.",
    "Having done its work without being bought, the six-month plan is what marketers call a decoy, an option whose job is to flatter a rival placed beside it."],
   "Sentence [[1]] sets up the hypothetical gym. Sentence [[2]] adds the six-month plan ('then'). Sentence [[3]] reports the result for 'the new six-month plan'. Sentence [[4]] says the plan did its work 'without being bought', which is known only once sentence [[3]] has reported that hardly anyone chose it, and then names the device, so it closes the paragraph.",
   "Placing the definition in sentence [[4]] straight after the new plan appears in sentence [[2]], although 'without being bought' needs the sales result reported in sentence [[3]].",
   "V01M-decoy-effect",
   "A simple narrative with time order and clear back-references ('then', 'the new six-month plan', 'without being bought').",
   traps=[("1243", "Sentence [[4]] says the six-month plan worked 'without being bought'; that cannot be said until sentence [[3]] reports that hardly anyone signed up for it."),
          ("4123", "Sentence [[4]] refers to 'the six-month plan' and its work, neither of which exists until sentences [[2]] and [[3]].")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 006 unfinished tasks
pj("V01-M-006", "Psychology",
   "Unfinished tasks linger in the mind, which can help or burden, and planning can relieve the burden.",
   "Medium",
   ["Psychologists have long observed that an interrupted task tends to linger in the mind longer than one brought to completion.",
    "The interrupted task, whether a half-written letter or an unsolved puzzle, keeps returning to awareness, as though the mind were reluctant to let go of an unreached goal.",
    "This persistence can be useful, since a problem left open overnight is sometimes solved in the morning without further effort.",
    "It can also be a burden, as anyone who has lain awake rehearsing tomorrow's unfinished chores will know.",
    "The burden, interestingly, often lifts once a person writes down a concrete plan for completing the task, even before any of the work is done."],
   "Sentence [[1]] states the general observation. Sentence [[2]] picks up 'The interrupted task' and illustrates it. Sentence [[3]] calls this 'This persistence' and gives its benefit. Sentence [[4]] adds 'also' a cost, which needs the benefit before it. Sentence [[5]] says how 'The burden' of sentence [[4]] lifts, so it comes last.",
   "Placing sentence [[5]] after sentence [[2]] because both describe how the mind holds on to a task, which leaves 'The burden' without a referent.",
   "V01M-zeigarnik-unfinished-tasks",
   "Five sentences with a benefit and cost pair and a final remedy; students must track 'This persistence', 'also' and 'The burden' across the chain.",
   traps=[("12435", "Sentence [[4]] says the persistence 'can also be a burden', so it must follow the first effect given in sentence [[3]]."),
          ("12534", "Sentence [[5]] explains how 'The burden' lifts, but no burden has been mentioned until sentence [[4]].")])

# ---------------------------------------------------------------- 007 self-serving attribution
pj("V01-M-007", "Psychology",
   "Crediting successes to oneself and failures to circumstance may be a protective buffer rather than vanity.",
   "Medium",
   ["People tend to credit their successes to their own ability and effort while blaming their failures on bad luck, unfair tests or difficult circumstances.",
    "At first sight this looks like simple vanity, a refusal to face unwelcome truths about oneself.",
    "Yet the habit may serve a purpose, because someone who reads every failure as proof of personal inadequacy may stop trying altogether.",
    "The bias, on this view, is less a defect of reasoning than a buffer that keeps people persisting long enough to improve."],
   "Sentence [[1]] describes the tendency. Sentence [[2]] gives the first, unflattering reading of 'this'. Sentence [[3]] answers it with 'Yet', proposing a purpose. Sentence [[4]] states 'this view', the buffer interpretation that sentence [[3]] introduced, and so comes last.",
   "Following sentence [[1]] with sentence [[3]], since 'Yet the habit' seems to contrast with the description, and then ending with the vanity reading.",
   "V01M-self-serving-attribution",
   "The order rests on the logic of a first reading followed by a reinterpretation; 'Yet' could attach to the opening description on a quick reading.",
   traps=[("1342", "Placed last, sentence [[2]] offers a first impression ('At first sight') after the considered view has already been reached, and the 'Yet' of sentence [[3]] then has no earlier judgement to push against.")])

# ---------------------------------------------------------------- 008 tip of the tongue
pj("V01-M-008", "Psychology",
   "Tip-of-the-tongue states show that word meaning and word sound are retrieved in separate stages.",
   "Easy",
   ["Most people know the frustration of a word that seems about to surface but refuses to appear, a state psychologists call being on the tip of the tongue.",
    "In this state, people can often report the first letter of the missing word, or how many syllables it has, though the word itself stays out of reach.",
    "Such partial knowledge suggests that retrieving a word happens in stages, with its meaning and its sound stored somewhat separately.",
    "When the state occurs, then, the meaning has been found but the route to the sound has briefly failed."],
   "Sentence [[1]] names the tip-of-the-tongue state. Sentence [[2]] refers to 'this state' and describes what people can report. Sentence [[3]] calls that 'Such partial knowledge' and draws the inference about stages. Sentence [[4]] applies the inference ('then') to the state.",
   "Placing sentence [[3]] before sentence [[2]], although 'Such partial knowledge' refers to the letters and syllables described in sentence [[2]].",
   "V01M-tip-of-the-tongue-states",
   "Clear chain of reference words ('this state', 'Such partial knowledge', 'then').",
   traps=[("1324", "Sentence [[3]] speaks of 'Such partial knowledge', which needs the first letter and syllable count reported in sentence [[2]].")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 009 chunking
pj("V01-M-009", "Psychology",
   "Expertise works around the limit of working memory by packing information into larger meaningful units.",
   "Medium",
   ["Working memory can hold only a handful of separate items at once, which is why a long string of random digits is so hard to repeat.",
    "The limit, however, applies to the number of items, not to the amount of information each item carries.",
    "A chess master glancing at a board sees not twenty-odd pieces but a few familiar patterns, each of which counts as a single item.",
    "Expertise, on this account, does not enlarge memory so much as reorganise what is held in it into larger meaningful units."],
   "Sentence [[1]] states the limit of working memory. Sentence [[2]] qualifies 'The limit': it counts items, not information. Sentence [[3]] illustrates that distinction with the chess master, whose patterns each count 'as a single item'. Sentence [[4]] draws the conclusion 'on this account'.",
   "Putting the chess example in sentence [[3]] before the distinction in sentence [[2]], because the example seems to follow naturally from the limit.",
   "V01M-chunking-working-memory",
   "The order depends on the logic of the idea: the chess example only makes sense once the distinction between items and information has been drawn.",
   traps=[("1324", "The chess master's patterns 'count as a single item' only because of the distinction drawn in sentence [[2]]; placed earlier, the example contradicts the limit just stated.")])

# ---------------------------------------------------------------- 010 gully cricket
pj("V01-M-010", "Society and culture",
   "The local rules of street cricket record the geography and people of the lane.",
   "Easy",
   ["Children playing cricket in narrow lanes rarely follow the official laws of the game.",
    "Instead, they invent local rules suited to the space, such as declaring a batter out for hitting the ball into a neighbour's balcony.",
    "These rules are not arbitrary, since each one solves a practical problem that the particular lane presents, like a ball lost in a drain or a neighbour who complains.",
    "A lane's rulebook is therefore a small record of its problems, and so of the street's geography and of the people who live along it."],
   "Sentence [[1]] says lane cricket ignores the official laws. Sentence [[2]] begins 'Instead' and describes the local rules. Sentence [[3]] refers to 'These rules' and explains them. Sentence [[4]] concludes 'therefore' that the rulebook records the lane's 'problems', the practical problems named in sentence [[3]].",
   "Opening with sentence [[2]], although 'Instead' needs the official laws of sentence [[1]] to contrast with.",
   "V01M-gully-cricket-local-rules",
   "Short chain held together by 'Instead', 'These rules' and 'therefore'.",
   traps=[("2134", "Sentence [[2]] opens with 'Instead', which cannot begin a paragraph; it replaces the official laws mentioned in sentence [[1]]."),
          ("1243", "Sentence [[4]] says the rulebook is 'therefore' a record of the lane's problems; those practical problems are named only in sentence [[3]].")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 011 library silence
pj("V01-M-011", "Society and culture",
   "Libraries should protect silence in some rooms rather than restore it everywhere.",
   "Medium",
   ["For generations, the public library was defined by its rule of silence, enforced by stern notices and sterner librarians.",
    "Many libraries today have relaxed that rule, adding cafes, children's corners and rooms for group study.",
    "Some regular users complain that the change has destroyed the one public space where concentration was possible.",
    "Their complaint is not merely nostalgic, since homes and offices now offer fewer quiet places than they once did.",
    "The better answer, then, is not to restore silence everywhere but to protect it in some rooms while letting the rest of the building be noisy."],
   "Sentence [[1]] describes the old rule of silence. Sentence [[2]] says libraries have relaxed 'that rule'. Sentence [[3]] reports a reaction to 'the change'. Sentence [[4]] defends 'Their complaint'. Sentence [[5]] proposes 'The better answer, then', a compromise that responds to both the change and the complaint.",
   "Placing sentence [[4]] before sentence [[3]] because it explains why quiet matters, although 'Their complaint' needs the complaining users of sentence [[3]].",
   "V01M-library-silence-norm",
   "Five sentences in a history, objection and resolution structure; the links are reference words spread across the chain.",
   traps=[("12435", "Sentence [[4]] begins 'Their complaint', which has no referent until the users in sentence [[3]] complain."),
          ("13245", "Sentence [[3]] speaks of 'the change', which has not happened until sentence [[2]] relaxes the rule.")])

# ---------------------------------------------------------------- 012 family group chats
pj("V01-M-012", "Society and culture",
   "Family group chats connect relatives but also create friction, which members manage by muting.",
   "Easy",
   ["Many extended families now keep in touch through a single group chat on their phones.",
    "Such a group lets distant cousins share news, photographs and birthday wishes without the effort of individual calls.",
    "The same group, however, can become a source of friction, as forwarded rumours and unwanted advice reach everyone at once.",
    "Many members respond by muting the chat, staying in it for the sake of family peace while rarely reading what is posted."],
   "Sentence [[1]] introduces the family group chat. Sentence [[2]] gives its benefit ('Such a group'). Sentence [[3]] turns to the cost with 'however'. Sentence [[4]] describes how members 'respond' to that friction.",
   "Putting sentence [[4]] after sentence [[2]], though muting is a response to the friction described only in sentence [[3]].",
   "V01M-family-group-chats",
   "Benefit, cost and response, marked by 'Such a group', 'however' and 'respond'.",
   traps=[("1243", "Members mute the chat in response to friction, which is introduced only in sentence [[3]]; placed earlier, sentence [[4]] has nothing to respond to.")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 013 tea stalls
pj("V01-M-013", "Society and culture",
   "The tea stall is a meeting place because using it creates no obligation of hospitality.",
   "Medium",
   ["The neighbourhood tea stall sells a cheap drink, but what keeps its customers coming back is the conversation around it.",
    "Strangers who would never visit one another's homes stand shoulder to shoulder there, exchanging news about jobs, prices and local disputes.",
    "They can mix so freely because the space belongs to nobody in particular, so no one has to play host and no one owes an invitation in return.",
    "It is this absence of obligation, more than the tea, that makes the stall a meeting place open to almost anyone."],
   "Sentence [[1]] introduces the stall and its conversation. Sentence [[2]] describes strangers mixing 'there'. Sentence [[3]] explains why 'They' can mix so freely. Sentence [[4]] picks out 'this absence of obligation' from sentence [[3]] and concludes.",
   "Placing the explanation in sentence [[3]] directly after sentence [[1]], though 'They can mix so freely' needs the strangers of sentence [[2]].",
   "V01M-neighbourhood-tea-stalls",
   "The order follows the logic of observation, explanation and conclusion; the explanation can look as if it belongs right after the opener.",
   traps=[("1324", "Sentence [[3]] explains why 'They' mix so freely; the strangers who mix appear only in sentence [[2]].")])

# ---------------------------------------------------------------- 014 Athenian ostracism
pj("V01-M-014", "History and politics",
   "Athenian ostracism removed dangerously influential men without punishing them, but it could be abused by factions.",
   "Medium",
   ["Citizens of classical Athens could, if they chose, hold a vote to send one prominent man into exile for ten years.",
    "Each voter scratched a name on a fragment of broken pottery, and the man named most often had to leave the city.",
    "Remarkably, the exile kept his property and his citizenship, and could return with full rights when the decade ended.",
    "The procedure was thus not a punishment for a crime but a way of removing a man whose influence had grown dangerous to the balance of the city.",
    "Its weakness was that the same tool could be turned against any rival whom a faction wished to be rid of, whether or not he posed a real threat."],
   "Sentence [[1]] introduces the vote to exile a prominent man. Sentence [[2]] explains how 'Each voter' took part and who had to leave. Sentence [[3]] says what 'the exile' kept. Sentence [[4]] draws the conclusion 'thus' from the fact that nothing was confiscated: the procedure was not a punishment. Sentence [[5]] turns to 'Its weakness', which presupposes that the purpose of the procedure has been stated.",
   "Placing sentence [[5]] before sentence [[4]] because both evaluate the procedure, which leaves 'thus' in sentence [[4]] drawing its conclusion from a weakness rather than from the kept property.",
   "V01M-athenian-ostracism",
   "Five sentences of description and evaluation; the conclusion 'not a punishment' must be drawn from the kept property before the weakness can be weighed.",
   traps=[("12354", "'The procedure was thus not a punishment' follows from the exile keeping his property and citizenship, not from the abuse described in sentence [[5]]."),
          ("13245", "Sentence [[3]] speaks of 'the exile', but no one has been sent away until the vote is counted in sentence [[2]].")])

# ---------------------------------------------------------------- 015 fire brigades
pj("V01-M-015", "History and politics",
   "Private insurance fire brigades gave way to public fire services because fire spreads beyond insured property.",
   "Easy",
   ["In many growing cities of the past, fires were fought by whoever happened to be nearby, with buckets passed from hand to hand.",
    "As property became more valuable, insurance companies began to employ their own teams of trained firefighters.",
    "These private brigades had an obvious interest in saving insured buildings, but fire rarely respects the boundaries of a policy.",
    "Over time, the case for a single public fire service, paid for by everyone and serving everyone, became hard to resist."],
   "Sentence [[1]] describes the earliest, improvised firefighting. Sentence [[2]] moves forward in time to insurers' own teams. Sentence [[3]] refers to 'These private brigades' and names their limitation. Sentence [[4]] concludes 'Over time' with the public service that answered it.",
   "Placing sentence [[4]] before sentence [[3]], though the case for a public service rests on the limitation of private brigades stated in sentence [[3]].",
   "V01M-fire-insurance-brigades",
   "Chronological order with a clear back-reference ('These private brigades').",
   traps=[("1243", "The public service of sentence [[4]] answers the problem that fire ignores 'the boundaries of a policy', so it must follow sentence [[3]].")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 016 medieval fairs
pj("V01-M-016", "History and politics",
   "Medieval fairs secured trust among strangers through recorded reputations, which worked only because the fairs mattered.",
   "Difficult",
   ["Merchants who met at the great medieval fairs faced a problem that had little to do with goods: how to trust partners they might never see again.",
    "A cheated trader could hardly pursue such a partner through foreign courts, and a dishonest one could simply stay away from the next gathering.",
    "The fairs' answer was not stronger law but memory, for officials recorded disputes, and a merchant who defaulted could be barred from every future fair.",
    "Exclusion worked only because the fairs mattered so much; a market that traders could easily do without would have had no such hold on its members."],
   "Sentence [[1]] states the problem of trusting partners 'they might never see again'. Sentence [[2]] refers to 'such a partner' and explains why ordinary remedies fail. Sentence [[3]] gives 'The fairs' answer', which must follow the full statement of the problem. Sentence [[4]] states the condition under which 'Exclusion', the barring described in sentence [[3]], could work.",
   "Treating sentence [[4]] as a general opener about why fairs mattered, although 'Exclusion' refers to the barring of defaulters introduced in sentence [[3]].",
   "V01M-medieval-trade-fairs-credit",
   "Problem, failed remedy, solution and the condition of the solution; the order follows the logic of the argument, and the condition sentence can look like a free-standing opener.",
   traps=[("4123", "Sentence [[4]] begins with 'Exclusion', which means nothing until sentence [[3]] describes defaulters being barred from future fairs."),
          ("1324", "Sentence [[3]] offers 'The fairs' answer' before sentence [[2]] has shown why courts could not help, and 'such a partner' in sentence [[2]] would then be cut off from the partners of sentence [[1]].")],
   exams=D)

# ---------------------------------------------------------------- 017 civil service examinations
pj("V01-M-017", "History and politics",
   "Imperial examinations favoured the wealthy in practice, yet kept the ideal of merit believable, binding ambitious men to the state.",
   "Difficult",
   ["For centuries, imperial China recruited many of its officials through written examinations open, in principle, to men of almost any family.",
    "The ideal was striking: office would go to learning rather than to birth, and a farmer's son might one day govern a province.",
    "In practice, years of study for the examinations required leisure and tutors, which wealthy families could buy far more easily than poor ones.",
    "Yet the system was not a mere disguise for privilege, since the occasional rise of a humble candidate kept the ideal believable to everyone.",
    "That belief may have been its most important product, binding ambitious men across a vast empire to the state that examined them."],
   "Sentence [[1]] introduces the examinations, 'open, in principle'. Sentence [[2]] states 'The ideal'. Sentence [[3]] contrasts it with what happened 'In practice'. Sentence [[4]] answers sentence [[3]] with 'Yet': the system was 'not a mere disguise for privilege', a denial that only makes sense after the advantage of wealth has been described. Sentence [[5]] takes up 'That belief', the believability of the ideal in sentence [[4]].",
   "Attaching sentence [[4]] directly to the ideal in sentence [[2]], because both speak of the ideal, although its denial that the system disguised privilege answers the point about wealth in sentence [[3]].",
   "V01M-civil-service-examinations",
   "Two contrast moves in a row ('In practice' and 'Yet'); students must see that the denial of privilege answers the practical objection, not the ideal, and that 'That belief' needs the believability claim.",
   traps=[("12435", "Sentence [[4]] denies that the system was 'a mere disguise for privilege'; before sentence [[3]] no privilege has been mentioned, so the denial answers nothing."),
          ("12354", "Sentence [[5]] refers to 'That belief', which is the believability of the ideal established only in sentence [[4]].")],
   exams=D)

# ---------------------------------------------------------------- 018 Veblen goods
pj("V01-M-018", "Economics and business",
   "For some luxury goods a high price is part of what is bought, so demand can fall when the price is cut.",
   "Easy",
   ["Economics textbooks usually assume that when the price of a good rises, people buy less of it.",
    "Some luxury goods seem to break this rule, because part of what their buyers want is the very fact that the item is expensive.",
    "A designer handbag is a familiar case, since one that anyone could afford would no longer signal its owner's wealth, and cutting its price might even reduce demand.",
    "The handbag's price, in other words, is not a cost its buyer tolerates but part of what she is paying for."],
   "Sentence [[1]] states the usual rule. Sentence [[2]] says some luxury goods 'break this rule'. Sentence [[3]] gives the handbag as 'a familiar case' of such goods. Sentence [[4]] restates the point 'in other words' using 'The handbag's price', so it must follow the handbag example.",
   "Placing sentence [[3]] straight after sentence [[1]], though the handbag is 'a familiar case' of rule-breaking goods introduced only in sentence [[2]].",
   "V01M-veblen-goods",
   "Rule, exception, example and restatement, marked by 'this rule', 'a familiar case' and 'in other words'.",
   traps=[("1324", "The handbag is offered as 'a familiar case' of goods that break the rule; that class is introduced only in sentence [[2]].")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 019 just-in-time
pj("V01-M-019", "Economics and business",
   "Lean inventory saved money but removed the buffer that protects production when a supplier fails.",
   "Medium",
   ["Holding large stocks of parts ties up money and warehouse space, so many manufacturers learned to order parts only as they were needed.",
    "The savings were real, and for years the lean approach looked like simple good management.",
    "What it had quietly traded away was the cushion that let a factory keep running when a single supplier failed.",
    "When disruptions came, the missing cushion was felt at once, and firms with nearly empty shelves were often the first to halt production."],
   "Sentence [[1]] explains why manufacturers moved to ordering parts only as needed. Sentence [[2]] grants 'The savings' and names 'the lean approach'. Sentence [[3]] says what 'it' had 'quietly traded away', a hidden cost that the years of apparent success in sentence [[2]] concealed. Sentence [[4]] shows the cost appearing when disruptions came and refers to 'the missing cushion' of sentence [[3]].",
   "Putting the disruption of sentence [[4]] before the hidden cost of sentence [[3]], as if the story ran in time order, which leaves 'the missing cushion' without a referent.",
   "V01M-just-in-time-inventory-fragility",
   "The order follows the logic of benefit, hidden cost and the cost revealed; the time sequence tempts students to put the disruption before the explanation.",
   traps=[("1243", "Sentence [[4]] speaks of 'the missing cushion', which is identified only in sentence [[3]].")])

# ---------------------------------------------------------------- 020 pay transparency
pj("V01-M-020", "Economics and business",
   "Publishing salaries narrows unjustified gaps but also discourages justified ones, making pay uniform rather than fair.",
   "Difficult",
   ["Advocates of publishing every employee's salary argue that secrecy protects unfair gaps in pay, which survive only because nobody can see them.",
    "Openness does tend to narrow gaps that cannot be justified, since a manager must now defend each difference to everyone it affects.",
    "That pressure is indiscriminate, however, falling equally on differences that can be justified, and managers who dread explaining a large raise may simply decline to give it.",
    "Transparency, in short, does not so much make pay fair as make it uniform, and the two coincide only where performance is roughly equal."],
   "Sentence [[1]] gives the advocates' case. Sentence [[2]] concedes it ('does tend'), an emphatic concession that needs a claim already on the table. Sentence [[3]] takes 'That pressure', the need to defend each difference, and shows its cost. Sentence [[4]] sums up 'in short', weighing both the gain of sentence [[2]] and the cost of sentence [[3]].",
   "Opening with sentence [[2]] because it reads like a plain statement, missing that 'does tend' concedes a point someone has already made.",
   "V01M-pay-transparency",
   "Abstract argument built on concession and qualification; the emphatic 'does tend' marks a concession to the advocates, and the summary must weigh both the gain and the cost.",
   traps=[("2134", "The emphatic 'does tend' concedes a claim already made, so sentence [[2]] cannot open; it grants the advocates' argument in sentence [[1]]."),
          ("1324", "'That pressure' refers to a manager having to 'defend each difference', which is introduced only in sentence [[2]].")],
   exams=D)

# ---------------------------------------------------------------- 021 brand extension
pj("V01-M-021", "Economics and business",
   "Stretching a brand saves money but can empty the name of meaning and destroy the trust it rests on.",
   "Medium",
   ["A company with a trusted brand is often tempted to stretch the name across new products, since customers already know and like it.",
    "The stretch saves money, because a familiar name needs far less advertising than an unknown one.",
    "It also carries a risk that is easy to overlook while sales of the new product are going well.",
    "Every product that bears the name teaches customers something about what the name means, and a cheap or unrelated product can teach them the wrong thing.",
    "A brand stretched too far may end up meaning nothing in particular, and so lose the very trust that made the stretch attractive."],
   "Sentence [[1]] introduces the temptation to stretch a brand. Sentence [[2]] gives the benefit of 'The stretch'. Sentence [[3]] adds that 'It also' carries a risk, which needs the benefit first. Sentence [[4]] explains the risk: each product teaches customers what the name means. Sentence [[5]] draws the end point, a name that means nothing, and returns to the trust of sentence [[1]].",
   "Placing sentence [[4]] immediately after sentence [[1]] because it explains how brands work, which leaves sentence [[3]] announcing a risk after it has already been described.",
   "V01M-brand-extension-dilution",
   "Five sentences in a benefit, risk, mechanism and consequence pattern; the mechanism sentence is general enough to seem to fit early.",
   traps=[("14235", "Sentence [[3]] announces a risk 'that is easy to overlook'; if sentence [[4]] has already set out the mechanism, the announcement comes too late and 'also' follows the wrong point."),
          ("12354", "Sentence [[5]] is the end result of the teaching process described in sentence [[4]]; a brand cannot be shown to mean 'nothing in particular' before the reader learns how products teach meaning.")])

# ---------------------------------------------------------------- 022 river straightening
pj("V01-M-022", "Science and environment",
   "Straightening rivers sped water downstream and worsened floods there, so some regions are restoring bends and wetlands.",
   "Easy",
   ["In the past, engineers straightened many winding rivers, cutting through their bends so that floodwater would be carried away faster.",
    "The straightened channels did move water quickly past the farms beside them, but they delivered it all the sooner to the towns downstream.",
    "Floods that the old meanders and marshes had once spread out and slowed now arrived downstream higher and faster, sometimes overwhelming defences built for gentler peaks.",
    "Some regions are therefore restoring the bends and wetlands that earlier generations of engineers removed, accepting slower drainage in return for safer towns."],
   "Sentence [[1]] describes the straightening. Sentence [[2]] refers to 'The straightened channels' and states the drawback. Sentence [[3]] spells out the effect on floods downstream. Sentence [[4]] gives the response 'therefore'.",
   "Placing sentence [[4]] before sentence [[3]], though the restoration is a response to the worsened floods described in sentence [[3]].",
   "V01M-river-straightening-floods",
   "Cause, effect and response in time order with 'The straightened channels' and 'therefore' as markers.",
   traps=[("1243", "Sentence [[4]] says regions are 'therefore' restoring bends; the reason is the higher, faster floods of sentence [[3]], which must come first.")],
   cognitive="Understanding")

# ---------------------------------------------------------------- 023 monoculture
pj("V01-M-023", "Science and environment",
   "Mixed planting trades some yield in good years for protection against a disease that could wipe out a uniform field.",
   "Medium",
   ["A field planted with a single high-yielding variety is easy to sow, tend and harvest, and in a good year it outproduces any mixed planting.",
    "Its uniformity is also its weakness, because a disease that can infect one plant in such a field can infect every plant in it.",
    "In a mixed field, by contrast, susceptible plants are separated by resistant ones, which slow the spread of the disease from neighbour to neighbour.",
    "The farmer who grows a mixture thus accepts a smaller harvest in good years in exchange for protection against the bad year that could destroy everything."],
   "Sentence [[1]] gives the advantage of a single-variety field. Sentence [[2]] names the weakness of 'Its uniformity'. Sentence [[3]] contrasts the mixed field and refers to 'the disease' of sentence [[2]]. Sentence [[4]] draws the trade-off 'thus', which needs both the yield advantage and the protection already stated.",
   "Placing sentence [[4]] after sentence [[1]] because both compare yields, although 'protection against the bad year' depends on the disease argument of sentences [[2]] and [[3]].",
   "V01M-monoculture-crop-disease",
   "The order follows the logic of a trade-off: advantage, weakness, the alternative's defence, then the farmer's choice.",
   traps=[("1423", "The farmer's trade-off in sentence [[4]] weighs yield against 'protection', which means nothing before the disease risk of sentence [[2]] and the mixed field's defence in sentence [[3]].")])

# ---------------------------------------------------------------- 024 volcanic winter
pj("V01-M-024", "Science and environment",
   "Eruptions cool the planet through long-lived stratospheric sulphur haze rather than through short-lived ash.",
   "Difficult",
   ["A great volcanic eruption can cool the whole planet, but not, as one might expect, because of the ash that darkens the sky around it.",
    "Ash is heavy and falls out of the air within days or weeks, long before it could affect the climate of distant continents.",
    "The lasting effect comes from sulphur gases carried high into the stratosphere, where they form a fine haze of droplets that reflects sunlight back into space.",
    "Above the weather, with no rain to wash it out, this haze can linger for a year or more and spread around the globe.",
    "That is why an eruption in the tropics can be followed by failed harvests on the other side of the world in the following summer."],
   "Sentence [[1]] says eruptions cool the planet but 'not' through ash. Sentence [[2]] justifies that denial: ash falls out within weeks. Sentence [[3]] gives 'The lasting effect', contrasting with the short-lived ash. Sentence [[4]] explains why 'this haze' persists and spreads. Sentence [[5]], 'That is why', draws the distant consequence that needs both persistence and global spread.",
   "Following sentence [[1]] with the sulphur explanation of sentence [[3]] because it gives the real cause, which leaves the ash sentence stranded between the haze and 'this haze'.",
   "V01M-volcanic-winter",
   "The order depends on the logic of the explanation: the denial in the opener must be justified before the real cause is given, and the consequence needs both the persistence and the spread of the haze.",
   traps=[("13245", "With sentence [[2]] after sentence [[3]], 'this haze' in sentence [[4]] is separated from its referent, and the reason for denying the role of ash comes after the real cause has already displaced it."),
          ("12354", "Sentence [[5]] explains effects 'on the other side of the world' a season later, which requires the haze to linger and spread as sentence [[4]] says.")],
   exams=D)

# ---------------------------------------------------------------- 025 replication crisis
pj("V01-M-025", "Science and environment",
   "Failed replications can arise from publication bias without misconduct, so the remedy lies in what journals publish.",
   "Difficult",
   ["When many published findings in a field fail to reappear on repetition, the natural suspicion is that some researchers have been careless or dishonest.",
    "A more troubling explanation needs no wrongdoing at all, only journals that prefer striking positive results to dull null ones.",
    "If many teams test unlikely ideas and only the lucky successes are printed, the literature will fill with flukes even if every study was conducted honestly.",
    "Repairing such a field, then, requires changing what gets published, not merely policing the people who publish it."],
   "Sentence [[1]] gives the 'natural suspicion' of misconduct. Sentence [[2]] offers 'A more troubling explanation', a comparison with the suspicion already stated. Sentence [[3]] works through the mechanism of that explanation, showing how flukes accumulate 'even if every study was conducted honestly'. Sentence [[4]] concludes 'then' that the remedy lies in publishing practice.",
   "Placing the mechanism of sentence [[3]] right after sentence [[1]], so that the selective printing appears before the explanation it belongs to is introduced.",
   "V01M-replication-crisis",
   "Abstract argument comparing two explanations; the order rests on 'more troubling' needing the first explanation and on the mechanism elaborating the second.",
   traps=[("1324", "Sentence [[3]] describes selective printing, the mechanism of the journal explanation, before sentence [[2]] has introduced that explanation; 'A more troubling explanation' would then arrive after it had already been set out."),
          ("2134", "Sentence [[2]] is 'more troubling' than something, so it cannot open; it is compared with the suspicion of carelessness or dishonesty in sentence [[1]].")],
   exams=D)
