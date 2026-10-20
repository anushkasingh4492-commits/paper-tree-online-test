import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DIFF = ("CAT", "XAT")

# ============================================================ EASY (7)

pj("V01-I-001", "Economics and business", "A tip that began as an optional reward has become part of ordinary wages.", "Easy",
   ["In many countries a tip began as an optional gift, a small reward a diner left for service that seemed unusually attentive.",
    "Over time, however, the gift hardened into an expectation, and leaving nothing came to be read as a complaint rather than as ordinary behaviour.",
    "Once that happened, employers in some trades began to treat tips as part of the wage and set basic pay lower in anticipation of them.",
    "The result is a curious reversal: with basic pay cut to match, a custom meant to reward exceptional service now props up the ordinary income of the people who provide it."],
   "Sentence [[1]] introduces the tip as an optional gift. Sentence [[2]] says that 'the gift hardened into an expectation', which needs the gift of [[1]] and contrasts with it through 'however'. Sentence [[3]] opens 'Once that happened', referring to the change into an expectation, and describes employers lowering basic pay. Sentence [[4]] states 'The result', a reversal in which tips prop up ordinary income, which depends on the lowered pay in [[3]], as 'with basic pay cut to match' makes explicit.",
   "Ending with sentence [[3]] after sentence [[4]], which puts 'with basic pay cut to match' before any cut in pay has been described.",
   "V01I-restaurant-tipping-norms", "A simple chronological chain carried by 'however', 'Once that happened' and 'The result'.",
   traps=[("1243", "Sentence [[4]] cannot follow sentence [[2]]: the claim that the custom 'props up the ordinary income' rests on employers lowering basic pay, which only sentence [[3]] describes.")],
   cognitive="Understanding")

pj("V01-I-002", "Science and environment", "Matching ring patterns across trees lets wood be dated precisely.", "Easy",
   ["Most trees in temperate climates add one ring of wood each year, wide in good growing seasons and narrow in poor ones.",
    "Because the weather of a region varies from year to year, trees growing there share a recognisable sequence of wide and narrow rings.",
    "By matching this sequence in living trees with the inner rings of old beams and buried logs, researchers can extend the pattern far into the past.",
    "A wooden object of unknown date can then be placed in time by finding where its own rings fit within that long master sequence."],
   "Sentence [[1]] states the basic fact of annual rings. Sentence [[2]] explains why trees in one region share a sequence of wide and narrow rings. Sentence [[3]] refers to 'this sequence' and shows how it is extended backwards using old timber. Sentence [[4]] uses 'then' and 'that long master sequence', the extended record built in [[3]], to explain how an object is dated.",
   "Placing sentence [[4]] before sentence [[3]], which uses the 'long master sequence' before it has been built.",
   "V01I-tree-ring-dating", "Each sentence names what the previous one produced; the links are explicit.",
   traps=[("1243", "Sentence [[4]] speaks of 'that long master sequence', but the sequence becomes long only when sentence [[3]] extends it into the past with old beams and logs.")],
   cognitive="Understanding")

pj("V01-I-003", "Technology", "Separate national plug standards left the world with incompatible sockets.", "Easy",
   ["When electricity first reached homes, there was no agreed way of connecting an appliance to the supply, and manufacturers designed their own plugs.",
    "As national grids grew, each country eventually settled on a standard of its own, chosen to suit its voltage and its existing wiring.",
    "These national choices, sensible at the time, have left the world with many incompatible socket designs.",
    "Travellers who now carry a bag of adapters to cope with them are paying, in a small way, for decisions that were made separately long ago."],
   "Sentence [[1]] opens with the early absence of any standard. Sentence [[2]] follows chronologically: as grids grew, each country chose its own standard. Sentence [[3]] refers to 'These national choices' and states their consequence, many incompatible designs. Sentence [[4]] refers to those designs ('to cope with them') and brings the consequence to the present with travellers 'paying' for 'decisions that were made separately long ago', which are the national choices.",
   "Opening with sentence [[2]] because it sounds like a general statement, which skips the early period that sentence [[1]] sets up and that 'eventually' looks back to.",
   "V01I-plug-socket-standards", "Chronology plus a clear demonstrative ('These national choices').",
   traps=[("2134", "Sentence [[2]] cannot open: 'eventually settled' implies an earlier unsettled period, which sentence [[1]] supplies, and sentence [[3]] must follow the national choices of sentence [[2]] directly.")],
   cognitive="Understanding")

pj("V01-I-004", "Language and media", "Private listening makes podcasts feel personal in a way family radio did not.", "Easy",
   ["Radio was once a medium of the living room, heard by a whole family gathered around a single set.",
    "The podcast, by contrast, is usually heard alone, through earphones, while its listener walks, cooks or commutes.",
    "This private setting changes how presenters speak: they drop the formal address of the broadcaster and talk as if to one friend.",
    "Listeners, in turn, often feel that they know a presenter personally, though the presenter has never heard of them."],
   "Sentence [[1]] describes radio as shared family listening. Sentence [[2]] sets the podcast against it with 'by contrast'. Sentence [[3]] refers to 'This private setting', the solitary listening of [[2]], and its effect on presenters. Sentence [[4]] gives the listeners' side with 'in turn', responding to the friendly tone described in [[3]].",
   "Starting with sentence [[2]], which cannot open because 'by contrast' needs the radio described in sentence [[1]].",
   "V01I-podcast-intimacy", "Contrast marker and a demonstrative make the order direct.",
   traps=[("1243", "Sentence [[4]] says listeners respond 'in turn', which needs the presenters' friendly manner from sentence [[3]] to come first.")],
   cognitive="Understanding")

pj("V01-I-005", "Education", "Homework for young children often measures the parent more than the pupil.", "Easy",
   ["Homework for young children is often defended on the ground that it builds habits of independent study.",
    "Yet a seven-year-old rarely works independently at home; a parent usually sits beside the child, explaining and correcting.",
    "What the homework measures, then, is partly the time and education of the parent rather than the effort of the pupil.",
    "For this reason some schools have replaced written tasks for the youngest classes with reading aloud, which any family can support."],
   "Sentence [[1]] states the usual defence of homework. Sentence [[2]] answers it with 'Yet': young children do not in fact work independently. Sentence [[3]] draws the conclusion with 'then': the work partly measures the parent. Sentence [[4]] gives a response to that problem, 'For this reason', and so comes last.",
   "Placing sentence [[4]] straight after sentence [[2]], which gives 'For this reason' a weaker reason and leaves sentence [[3]] stranded at the end.",
   "V01I-primary-school-homework", "A claim, objection, conclusion and response, each marked by a connective.",
   traps=[("1243", "Sentence [[3]] cannot close the paragraph after sentence [[4]]: its 'then' draws a conclusion from the parent's help in sentence [[2]], and the replacement of written tasks in sentence [[4]] is a response to that conclusion.")],
   cognitive="Understanding")

pj("V01-I-006", "Arts and literature", "Recorded laughter was added to television comedies and later abandoned.", "Easy",
   ["Early television comedies were often recorded in front of a studio audience, whose laughter was captured along with the dialogue.",
    "When producers began filming without an audience, they found that jokes seemed flat to viewers at home without that sound.",
    "Their solution was the laugh track, recorded laughter added afterwards to tell viewers where the funny moments were.",
    "Critics soon complained that the device was manipulative, since it instructed the audience to laugh instead of letting them decide.",
    "Partly in answer to such complaints, many recent comedies have abandoned it altogether, trusting viewers to find the jokes for themselves."],
   "Sentence [[1]] describes live audiences. Sentence [[2]] follows chronologically with filming 'without an audience' and the missing sound. Sentence [[3]] gives 'Their solution', the laugh track. Sentence [[4]] reports criticism of 'the device'. Sentence [[5]] responds 'to such complaints', so it must follow sentence [[4]] and close the paragraph.",
   "Putting sentence [[5]] before sentence [[4]] because both discuss the laugh track's fate, which leaves 'such complaints' without any complaint to refer to.",
   "V01I-sitcom-laugh-tracks", "Five sentences in plain chronological order with clear back-references.",
   traps=[("12354", "Sentence [[5]] answers 'such complaints', which are first made in sentence [[4]], so it cannot come before it.")],
   cognitive="Understanding")

pj("V01-I-007", "Science and environment", "Air trapped in polar ice preserves a record of past atmospheres.", "Easy",
   ["Snow falling on the polar ice sheets traps small bubbles of air as it is compressed, year after year, into solid ice.",
    "Each bubble is therefore a tiny sample of the atmosphere as it was when that layer of snow was buried.",
    "By drilling deep cores and analysing the air in successive layers, scientists can read off how the composition of the atmosphere has changed.",
    "The deepest of these cores carry the record back many hundreds of thousands of years, far beyond any written history."],
   "Sentence [[1]] explains how air is trapped in ice. Sentence [[2]] concludes, 'therefore', that each bubble samples the old atmosphere. Sentence [[3]] describes drilling cores to read that record. Sentence [[4]] refers to 'these cores', which only sentence [[3]] introduces.",
   "Placing sentence [[3]] first because it names the scientific method, which leaves 'Each bubble' in sentence [[2]] without the bubbles of sentence [[1]].",
   "V01I-ice-core-climate-records", "Clear causal sequence and a demonstrative ('these cores').",
   traps=[("1324", "Sentence [[2]] must follow sentence [[1]] directly, since 'Each bubble' and 'therefore' depend on the bubbles trapped in compressing snow.")],
   cognitive="Understanding")

# ============================================================ MEDIUM (11)

pj("V01-I-008", "Economics and business", "Insurance can weaken the care people take, so insurers make claimants share losses.", "Medium",
   ["Insurance exists to spread the cost of misfortunes that no single person could easily bear.",
    "But by softening the cost of a loss, it can also weaken the care people take to avoid one.",
    "A driver whose car is fully covered, for instance, may park in a street he would otherwise avoid.",
    "Insurers respond by making the insured bear a part of every claim, so that carelessness still costs something."],
   "Sentence [[1]] states the purpose of insurance. Sentence [[2]] turns, with 'But', to its side effect: less care. Sentence [[3]] illustrates that side effect with a fully covered driver. Sentence [[4]] gives the insurers' remedy. The logic also fixes the position of the example: if sentence [[4]] came before sentence [[3]], the driver would be 'fully covered' just after we are told that the insured always bear part of a claim, which contradicts the remedy.",
   "Treating the driver example as a closing illustration of the insurers' remedy, when it actually illustrates the problem the remedy answers.",
   "V01I-insurance-moral-hazard", "The order of the example and the remedy depends on what the example illustrates, not on a connective; a strong reader must see that a 'fully covered' driver exemplifies the problem.",
   traps=[("1243", "Sentence [[3]] after sentence [[4]] describes a 'fully covered' driver right after the paragraph says insurers make the insured share every claim, so the example contradicts the sentence before it instead of illustrating sentence [[2]]."),
          ("2314", "Sentence [[2]] cannot open: 'it' and 'also' need the insurance and its main purpose, introduced in sentence [[1]].")])

pj("V01-I-009", "Arts and literature", "Translating a poem forces a choice between losing sense and losing sound.", "Medium",
   ["A translator of prose can usually carry a sentence's meaning into another language and let its rhythm fall where it may.",
    "Poetry allows no such freedom, because in a poem the sound and the sense are bound together.",
    "A line that keeps the meaning of the original but loses its music has kept only half of what the poet made.",
    "Yet the opposite course is no safer, for a translator who chases the rhyme and metre must often bend the meaning to fit them.",
    "Every translation of a poem is thus a choice about which loss to accept, and no choice avoids loss entirely."],
   "Sentence [[1]] describes the prose translator's freedom. Sentence [[2]] says poetry 'allows no such freedom' because sound and sense are joined. Sentence [[3]] shows one consequence: keeping meaning loses music. Sentence [[4]] says 'the opposite course', chasing the sound, is no safer, so it must follow the course described in [[3]]. Sentence [[5]] concludes that every translation chooses 'which loss to accept', which needs both losses already stated.",
   "Placing sentence [[4]] before sentence [[3]] because both are about losses, which leaves 'the opposite course' with no course to be opposite to.",
   "V01I-poetry-translation", "Two parallel horns of a dilemma; the order of the horns and the conclusion follows from the argument, with only one light lock ('the opposite course').",
   traps=[("12435", "Sentence [[4]] speaks of 'the opposite course', which presupposes the course of keeping meaning described in sentence [[3]]."),
          ("21345", "Sentence [[2]] cannot open: 'no such freedom' refers back to the prose translator's freedom in sentence [[1]].")])

pj("V01-I-010", "Technology", "Turn-by-turn navigation may let spatial memory weaken from disuse.", "Medium",
   ["Finding one's way through an unfamiliar city once required building a mental map, noting landmarks and the turns between them.",
    "Satellite navigation removes that burden, issuing each turn at the moment it is needed.",
    "Convenient as this is, it means the traveller can reach a destination without ever forming a picture of the route.",
    "Some researchers worry that skills of spatial memory, like other unused abilities, may weaken when they are no longer exercised."],
   "Sentence [[1]] describes the old demand of building a mental map. Sentence [[2]] says satellite navigation 'removes that burden'. Sentence [[3]] grants the convenience but notes the traveller no longer forms a picture of the route. Sentence [[4]] draws the worry that follows: a skill no longer exercised may weaken. The worry in [[4]] depends on the claim in [[3]] that the skill is no longer used.",
   "Moving sentence [[4]] up to follow sentence [[2]], which states a worry about disuse before the paragraph has shown that the skill falls out of use.",
   "V01I-gps-spatial-memory", "The last two sentences are linked by the logic of disuse and decline rather than by a strong connective.",
   traps=[("1243", "After sentence [[4]], 'Convenient as this is' in sentence [[3]] would refer to the weakening of memory, which is not convenient; the phrase must refer to the navigation of sentence [[2]].")])

pj("V01-I-011", "Language and media", "Sign languages have independent grammars and are full languages.", "Medium",
   ["Many hearing people assume that a sign language is simply a spoken language spelled out on the hands.",
    "In fact, the sign languages of deaf communities have their own grammars, often quite unlike that of the spoken language around them.",
    "A sign language may, for example, mark a question with the eyebrows and place characters at points in space to track who did what to whom.",
    "Such features show that these are full languages in their own right, not manual codes for some other tongue."],
   "Sentence [[1]] states a common assumption. Sentence [[2]] rejects it with 'In fact'. Sentence [[3]] gives examples of independent grammar. Sentence [[4]] refers to 'Such features', the examples of [[3]], and concludes that these are full languages, which answers the assumption of [[1]].",
   "Opening with sentence [[2]] because it states the main claim, when 'In fact' signals a correction of the assumption in sentence [[1]].",
   "V01I-sign-language-grammar", "A misconception, correction, evidence and conclusion; the closing sentence could look like an opener.",
   traps=[("1243", "Sentence [[4]] refers to 'Such features', which are the eyebrow questions and spatial placement of sentence [[3]], so it cannot precede them.")])

pj("V01-I-012", "Education", "Early school start times collide with the later sleep of adolescents.", "Medium",
   ["During adolescence the body's internal clock shifts later, so that teenagers naturally feel sleepy and wake later than younger children.",
    "School timetables, however, are usually set for the convenience of transport and of working parents, and often begin early in the morning.",
    "The two schedules collide, leaving many teenagers chronically short of sleep on school days.",
    "Some districts that have moved the start of the day later report pupils who are more alert in morning classes, though the effect on results is still debated."],
   "Sentence [[1]] describes the adolescent body clock. Sentence [[2]] sets the school timetable against it. Sentence [[3]] joins them: 'The two schedules collide', which requires both to be described. Sentence [[4]] describes a remedy, a later start, which makes sense only once the collision is established.",
   "Placing sentence [[2]] first because it introduces schools, which makes 'however' contrast with nothing.",
   "V01I-school-start-times-sleep", "The collision sentence must follow both schedules, and the remedy must follow the collision: the order rests on the problem and solution structure.",
   traps=[("2134", "Sentence [[2]] contains 'however', which needs a prior claim to contrast with; that is the biological clock of sentence [[1]]."),
          ("1243", "Sentence [[4]] offers a later start as a remedy, but the problem it remedies, the collision of schedules, is stated only in sentence [[3]].")])

pj("V01-I-013", "Economics and business", "Winning an auction for an item of uncertain value suggests the winner overpaid.", "Medium",
   ["Suppose several firms bid for the right to drill in an oilfield whose true value no one knows.",
    "Each firm makes its own estimate, and while some estimates will be too high and others too low, their average may be close to the truth.",
    "The firm that wins, however, is the one that bid most, which usually means the one whose estimate was most optimistic.",
    "Winning is therefore itself a sign that the winner has probably overpaid.",
    "Experienced bidders learn to shade their offers below their estimates, precisely to protect themselves from this effect."],
   "Sentence [[1]] sets up the hypothetical auction. Sentence [[2]] describes the spread of estimates around the truth. Sentence [[3]] turns, with 'however', to the winner, whose estimate was the most optimistic. Sentence [[4]] concludes that winning signals overpayment. Sentence [[5]] describes how bidders guard against 'this effect', so it must come last.",
   "Placing sentence [[4]] right after sentence [[2]], which draws the conclusion before the paragraph has said that the winner is the most optimistic bidder.",
   "V01I-winners-curse-auctions", "The conclusion requires the reasoning that the highest bid comes from the highest estimate; the order follows the argument.",
   traps=[("12435", "Sentence [[4]] concludes 'therefore' that winning signals overpaying, but the reason, that the winner held the most optimistic estimate, is given only in sentence [[3]]."),
          ("12354", "Sentence [[5]] guards against 'this effect', which is named only in sentence [[4]], so the guard cannot precede the effect.")])

pj("V01-I-014", "Science and environment", "Island species lose defences in isolation and fall to introduced predators.", "Medium",
   ["Animals that evolve on remote islands often meet no large predators for thousands of generations.",
    "Over that time, defences that cost energy, such as flight or a fear of strangers, tend to fade.",
    "When ships bring rats, cats or snakes to such an island, the native birds face hunters they have no means of escaping.",
    "This is why island species make up a disproportionate share of recorded extinctions, though islands cover a small part of the earth's land."],
   "Sentence [[1]] describes long isolation from predators. Sentence [[2]] says what happens 'Over that time': costly defences fade. Sentence [[3]] introduces predators and explains why the birds cannot escape, which depends on the lost defences of [[2]]. Sentence [[4]] generalises with 'This is why'.",
   "Placing sentence [[3]] before sentence [[2]] because the arrival of predators seems to start the story, which makes 'Over that time' refer to the wrong period.",
   "V01I-invasive-species-islands", "The reader must see that defencelessness must be established before the predators arrive; the cause must precede the vulnerability.",
   traps=[("1324", "Sentence [[2]] says 'Over that time', meaning the generations without predators in sentence [[1]]; after sentence [[3]] it would refer to the arrival of rats and cats, which makes no sense.")])

pj("V01-I-015", "Arts and literature", "The conductor solves a real problem of timing and shapes the performance in rehearsal.", "Medium",
   ["To a concert audience the conductor can seem the least necessary person on stage, the only one who makes no sound.",
    "Yet a large orchestra cannot keep together by listening alone, since players at opposite ends of the stage hear one another a fraction of a second late.",
    "The conductor's beat gives them a shared visual signal that reaches everyone at the same instant.",
    "Much of the real work, moreover, is done before the concert, in rehearsals where the conductor decides how the piece should sound."],
   "Sentence [[1]] states how the conductor appears to an audience. Sentence [[2]] answers with 'Yet', explaining the timing problem of a large orchestra. Sentence [[3]] shows that the beat solves that problem, 'them' being the players of [[2]]. Sentence [[4]] adds, with 'moreover', a second contribution, so it follows the first.",
   "Ending with sentence [[3]] after sentence [[4]], which separates the solution from the timing problem it solves.",
   "V01I-orchestra-conductor-role", "Problem and solution must stay adjacent; the additive 'moreover' must follow a first contribution.",
   traps=[("1243", "Sentence [[3]] solves the timing problem of sentence [[2]] and its 'them' refers to the players there; placing sentence [[4]] between them breaks the link and leaves 'moreover' adding to a problem rather than a contribution.")])

pj("V01-I-016", "Technology", "Autocorrect replaces many obvious errors with fewer but subtler ones.", "Medium",
   ["Autocorrect was designed to catch the slips of fingers on small keyboards, replacing an unknown string of letters with the nearest familiar word.",
    "Its weakness follows from the same design: when a writer intends an unusual name or a technical term, the software confidently substitutes something common.",
    "Because the substitute is a real word, it passes the quick glance that would have caught an ordinary typing error.",
    "Autocorrect thus trades a large number of obvious mistakes for a smaller number of subtle ones, which may be the harder kind to notice."],
   "Sentence [[1]] states the design. Sentence [[2]] says the weakness 'follows from the same design', so it must come after the design is described. Sentence [[3]] explains why 'the substitute' escapes notice. Sentence [[4]] sums up with 'thus': fewer but subtler errors, which rests on [[3]].",
   "Ending with sentence [[3]] after sentence [[4]], which puts the reason after the conclusion drawn from it.",
   "V01I-autocorrect-errors", "The reasoning about why a real-word error is hard to see fixes the last two sentences.",
   traps=[("1243", "Sentence [[4]] says the errors are 'subtle' and 'the harder kind to notice', which is a conclusion from sentence [[3]]; and 'the substitute' in sentence [[3]] needs the substitution of sentence [[2]] immediately before it.")])

pj("V01-I-017", "Language and media", "Paywalls steady newspaper finances but divide readers by what they can trust.", "Medium",
   ["For years newspapers gave their articles away online, hoping that advertising would pay for the journalism.",
    "Advertising revenue, however, flowed increasingly to the large platforms that controlled where readers found the news.",
    "Many papers responded by putting their reporting behind a paywall and asking readers to subscribe.",
    "This has steadied the finances of some titles, but it has also divided readers into those who pay for careful reporting and those who rely on whatever is free.",
    "The worry is that the second group, often the larger, is left with the material least worth trusting."],
   "Sentence [[1]] describes the free model. Sentence [[2]] says, with 'however', that advertising did not stay with newspapers. Sentence [[3]] gives the response, paywalls. Sentence [[4]] states the effects of 'This', including the division of readers. Sentence [[5]] refers to 'the second group', which exists only after sentence [[4]] names two groups.",
   "Placing sentence [[3]] before sentence [[2]], which offers a response before the problem it responds to.",
   "V01I-news-paywalls", "Five sentences in a chain of problem, response and consequence; the middle requires seeing why papers 'responded'.",
   traps=[("13245", "Sentence [[3]] says papers 'responded', and the problem they responded to, advertising moving to platforms, is stated in sentence [[2]]."),
          ("12354", "Sentence [[5]] mentions 'the second group' before sentence [[4]] has divided readers into two groups.")])

pj("V01-I-018", "Education", "Negative marking removes the gain from blind guessing but rewards nerve as well as knowledge.", "Medium",
   ["In a multiple-choice test, a candidate who knows nothing can still score by guessing.",
    "Negative marking is meant to remove this advantage by deducting marks for each wrong answer.",
    "Set at the right level, the penalty makes blind guessing worthless on average, while still rewarding a candidate who can eliminate some options.",
    "That reward reaches only those willing to claim it, however: some cautious candidates leave blank even questions they could narrow down, so the scheme measures nerve as well as knowledge."],
   "Sentence [[1]] states the problem of guessing. Sentence [[2]] introduces negative marking to remove 'this advantage'. Sentence [[3]] explains how a well-set penalty works and notes that it still rewards partial knowledge. Sentence [[4]] begins 'That reward', the reward for eliminating options in [[3]], and qualifies it, so it must come last.",
   "Treating sentence [[4]] as a general objection that could follow sentence [[2]], when 'That reward' points only to the reward described in sentence [[3]].",
   "V01I-negative-marking-guessing", "The closing qualification depends on seeing what 'That reward' refers to and why caution undercuts it.",
   traps=[("1243", "After sentence [[2]], 'That reward' in sentence [[4]] has no referent: the reward for eliminating options is introduced only in sentence [[3]].")])

# ============================================================ DIFFICULT (7)

pj("V01-I-019", "Economics and business", "Gift cards profit retailers through unspent value whose loss no one feels.", "Difficult",
   ["A gift card looks like a sensible compromise between a present and cash: it lets the recipient choose, while still showing that the giver thought of a particular shop.",
    "For the retailer, however, its chief attraction lies less in the sale it records than in the spending it never has to honour.",
    "A noticeable share of cards is lost, forgotten or left with a balance too small to bother with, and the value they carry then stays with the seller.",
    "One might expect such losses to make people wary of the cards, but the loss is spread thinly and felt by no one in particular, since the giver never sees it and the recipient rarely notices it.",
    "Retailers can therefore promote the cards energetically without provoking the resentment that a visible charge of the same size would arouse."],
   "Sentence [[1]] introduces the gift card from the point of view of the giver and the recipient. Sentence [[2]] turns, with 'For the retailer, however', to the seller's interest, stated compactly as 'the spending it never has to honour'. Sentence [[3]] unpacks that phrase: cards that are lost, forgotten or left with small balances leave their value 'with the seller'. Sentence [[4]] raises the expectation that 'such losses' would make people wary and answers it: the loss is 'felt by no one in particular'. Sentence [[5]] draws the consequence with 'therefore': because the loss is invisible, retailers can push the cards without provoking resentment.",
   "Placing sentence [[2]] last as a closing remark on the retailer's motive, which leaves 'For the retailer, however' contrasting with a sentence that is already about retailers.",
   "V01I-gift-card-breakage", "The second sentence states the retailer's interest in a compact phrase that only the third unpacks, and the close runs from an objection to its answer to the consequence, so the order rests on the logic of invisible loss rather than on pronouns.",
   traps=[("13245", "Sentence [[3]] cannot come straight after sentence [[1]]: the value it says 'stays with the seller' is the point of sentence [[2]], whose 'however' marks the turn from the recipient's view to the retailer's and must come first."),
          ("12354", "Sentence [[5]] says retailers can 'therefore' promote the cards without resentment, but the reason, that the loss is 'felt by no one in particular', is given only in sentence [[4]]; placed last, sentence [[4]] would reopen a doubt the paragraph has already settled.")],
   exams=DIFF)

pj("V01-I-020", "Science and environment", "A magnetic sense in birds was doubted because no organ for it could be found.", "Difficult",
   ["That migrating birds find their way across continents has never been in doubt; what has resisted explanation is the means.",
    "Experiments that altered the magnetic field around caged birds changed the direction in which they tried to fly, which pointed to a magnetic sense.",
    "The trouble was that no one could find the organ responsible, and a sense without an organ struck many biologists as no sense at all.",
    "That objection assumed that a sense must be housed in some visible structure, whereas this one might operate through molecules in the eye or particles scattered in tissue."],
   "Sentence [[1]] separates the established fact of navigation from the open question of how. Sentence [[2]] gives experimental evidence for one answer, a magnetic sense. Sentence [[3]] raises 'The trouble': no organ could be found, so the sense was doubted. Sentence [[4]] identifies the assumption behind 'That objection' and answers it. Each step depends on the previous claim: evidence, then doubt about the evidence, then a reply to the doubt.",
   "Reading sentence [[4]] as background that could come before the doubt, when it rebuts the specific objection voiced in sentence [[3]].",
   "V01I-bird-navigation-magnetic-sense", "Abstract claim, evidence, objection and reply; the reader must track which sentence answers which and resist placing the evidence first.",
   traps=[("2134", "Sentence [[2]] can look like a lively opener, but sentence [[1]] cannot then follow it: its contrast between the undoubted fact and the unexplained 'means' frames the question that the experiments begin to answer."),
          ("1324", "Sentence [[3]] speaks of 'the organ responsible', which presupposes the magnetic sense proposed in sentence [[2]].")],
   exams=DIFF)

pj("V01-I-021", "Arts and literature", "A strict poetic form can aid invention by forcing poets past obvious phrases.", "Difficult",
   ["It is tempting to think that a strict form, with its fixed count of lines and its demanding rhyme scheme, can only hamper a poet.",
    "Yet the constraint can work the other way, since the need to find a rhyme pushes the poet past the first, obvious phrase towards one that would otherwise never have been reached.",
    "The form, on this view, is less a cage than an instrument of search, a way of making the mind try possibilities it would have skipped.",
    "If that is right, free verse, which offers no such instrument, may be harder to write well than it looks."],
   "Sentence [[1]] states the tempting view that form only hampers. Sentence [[2]] counters it with 'Yet': the constraint can push the poet past the obvious. Sentence [[3]] generalises 'on this view' that form is an instrument of search. Sentence [[4]] draws an implication for free verse, 'which offers no such instrument', so it must follow the image of the instrument in [[3]]. The order moves from a view, to its reversal, to the general principle, to its implication.",
   "Starting with sentence [[3]] because it sounds like a thesis, when 'on this view' requires the view argued in sentence [[2]].",
   "V01I-sonnet-form-constraint", "The order rests on the movement from a rejected view to the principle and its consequence; the thesis-like sentence is a tempting wrong opener.",
   traps=[("3124", "Sentence [[3]] cannot open: 'on this view' points back to the argument of sentence [[2]] that constraint aids invention."),
          ("1243", "Sentence [[4]] speaks of 'no such instrument', and the form is described as an instrument only in sentence [[3]].")],
   exams=DIFF)

pj("V01-I-022", "Technology", "Popular volunteer software can collapse when the burden on its few maintainers grows.", "Difficult",
   ["A great deal of the code that businesses rely on every day is maintained, without pay, by a handful of volunteers.",
    "In the early life of a project this arrangement works well enough, since the people who write the code are also the people who use it.",
    "As the project grows popular, its users multiply far faster than its maintainers, and most of them contribute nothing but requests.",
    "The few volunteers end up answering complaints instead of writing code, and some of them simply walk away.",
    "When they do, companies that had treated the software as free discover that it was free only because someone else was paying with time."],
   "Sentence [[1]] states the situation of unpaid maintenance. Sentence [[2]] says 'this arrangement' works early on, because writers and users coincide. Sentence [[3]] describes growth, which breaks that coincidence. Sentence [[4]] gives the effect on the volunteers. Sentence [[5]] begins 'When they do', referring to volunteers walking away, so it must follow [[4]]. The middle three follow the life of a project from early to popular to strained.",
   "Placing sentence [[4]] straight after sentence [[2]], which makes the volunteers overworked before the paragraph has introduced the growth in users that overworks them.",
   "V01I-open-source-maintainer-burnout", "Few connectives: the middle of the paragraph is ordered by the logic of a project's growth, and the reader must see that the burden comes from the surge of users.",
   traps=[("12435", "Sentence [[4]] says the volunteers 'end up' answering complaints; the complaints come from the flood of users described in sentence [[3]], so the effect cannot precede its cause."),
          ("13245", "Sentence [[2]] describes the 'early life' of a project, and placing it after the growth of sentence [[3]] reverses the chronology the paragraph depends on.")],
   exams=DIFF)

pj("V01-I-023", "Education", "Ability grouping can become self-confirming because placement shapes what pupils learn.", "Difficult",
   ["Grouping pupils by ability appears to help everyone, since teachers can pitch each lesson to the level of the class in front of them.",
    "The appearance depends on treating a pupil's placement as a measurement of what that pupil can do.",
    "In practice the placement also shapes what the pupil will be able to do, because lower groups are usually taught less and expected to achieve less.",
    "A judgement made at eleven can thus become self-confirming, as the groups grow further apart each year and seem to prove the original sorting right."],
   "Sentence [[1]] states the apparent benefit. Sentence [[2]] exposes the assumption behind 'The appearance': placement is treated as a measurement. Sentence [[3]] challenges that assumption, since placement also shapes ability. Sentence [[4]] draws the conclusion, 'thus', that the sorting confirms itself, which follows only from the claim that placement shapes ability.",
   "Placing sentence [[3]] before sentence [[2]] because it sounds like the main criticism, which separates 'The appearance' from the claim in sentence [[1]] and gives 'also' nothing to add to.",
   "V01I-ability-streaming", "The order turns on the distinction between measuring and shaping ability; 'also' in the third sentence only makes sense after the measuring view is stated.",
   traps=[("1324", "Sentence [[3]] says placement 'also' shapes ability, which adds to the view of placement as a measurement stated in sentence [[2]]; and 'The appearance' must follow 'appears' in sentence [[1]]."),
          ("1243", "Sentence [[4]] concludes that the sorting is self-confirming, which follows only once sentence [[3]] has shown that placement shapes what pupils can do.")],
   exams=DIFF)

pj("V01-I-024", "Economics and business", "A franchise trades the owner's freedom for reduced uncertainty.", "Difficult",
   ["A franchise lets an entrepreneur buy into a proven formula rather than invent one, paying fees in return for the brand, the methods and the suppliers.",
    "The fees, though, are not the real price; what the franchisee surrenders in exchange for less uncertainty is the freedom to decide.",
    "The owner of a franchised cafe, for instance, may not change the menu, the decor or the opening hours, even where local customers would plainly prefer something else.",
    "Whether the bargain is a good one depends on which a particular entrepreneur values more: freedom to experiment or protection from the cost of experiments that fail."],
   "Sentence [[1]] describes what a franchise offers for its fees. Sentence [[2]] turns, with 'though', to the real price: loss of the freedom to decide. Sentence [[3]] illustrates that loss with a cafe owner who cannot change the menu. Sentence [[4]] weighs 'the bargain', freedom against protection, so it must come after both sides are stated. The example must follow the claim about lost freedom, since it shows nothing about the fees of sentence [[1]].",
   "Putting the cafe example after sentence [[1]], where 'for instance' would illustrate the benefits of a proven formula, which the example does not show.",
   "V01I-franchise-business-model", "The example's position depends on recognising which claim it illustrates, and the closing sentence weighs two sides that must both be in place.",
   traps=[("1324", "After sentence [[1]], the cafe example would be an instance of buying a proven formula, but it shows a restriction, which is the loss of freedom stated in sentence [[2]]."),
          ("1243", "Sentence [[3]] after sentence [[4]] would illustrate the general weighing of freedom against protection, and the paragraph would end on an example instead of the judgement it leads to.")],
   exams=DIFF)

pj("V01-I-025", "Arts and literature", "Respelling dialect speech makes characters seem ignorant, so writers often keep standard spelling.", "Difficult",
   ["A novelist who wants readers to hear the speech of a region must decide how far to let spelling follow sound.",
    "Respelling words as they are pronounced looks like the most faithful course, and many earlier novelists took it freely.",
    "Its cost is that the reader meets the speech as a page of misspellings, and misspelling, on the page, suggests ignorance rather than an accent.",
    "Worse, characters rendered this way can come to seem less intelligent than the narrator who describes them in standard spelling, an effect the novelist seldom intends.",
    "Many later writers have therefore kept conventional spelling for dialogue and conveyed the region through vocabulary, idiom and the rhythm of the sentence."],
   "Sentence [[1]] sets out the novelist's decision. Sentence [[2]] gives the apparently faithful option, respelling. Sentence [[3]] states 'Its cost': misspelling suggests ignorance. Sentence [[4]] escalates with 'Worse', a further cost that builds on the first, the contrast with a standard-spelling narrator. Sentence [[5]] draws the consequence, 'therefore', in the practice of later writers, which needs both costs before it.",
   "Placing sentence [[4]] before sentence [[3]] because 'rendered this way' can refer to the respelling of sentence [[2]], which leaves 'Worse' escalating from nothing and makes 'Its cost' ambiguous.",
   "V01I-dialect-spelling-fiction", "Two costs must be ordered by degree; 'rendered this way' and 'Its' could both attach to the respelling sentence, so the reader must use 'Worse' and the logic of escalation.",
   traps=[("12435", "Sentence [[4]] begins 'Worse', which needs a first cost before it; that cost, misspelling suggesting ignorance, is stated in sentence [[3]]."),
          ("12354","Sentence [[5]] says later writers 'therefore' kept standard spelling, which must follow the full case against respelling, including the further cost in sentence [[4]].")],
   exams=DIFF)
