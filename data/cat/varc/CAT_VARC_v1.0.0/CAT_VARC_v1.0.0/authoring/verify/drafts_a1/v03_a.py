import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ooo("V03-A-001", "Philosophy and ethics",
    "Admiring moral struggle is apt only as praise for a stage; the goal of virtue is a character that no longer needs to struggle.", "Medium",
    ["We tend to admire the person who resists a strong temptation to lie more than the person who is never tempted at all.",
     "Yet on reflection the second person seems the better one, since honesty has become so much a part of her character that lying no longer appeals.",
     "The struggle we admire is evidence of effort, but it is also evidence that the desire to deceive is still present and still strong.",
     "Perhaps, then, we should praise struggle as a stage on the way to virtue, while recognising that the goal is a character in which the struggle is no longer needed."],
    "Moral philosophers have also asked whether a person can fairly be blamed for desires she never chose and cannot simply switch off.",
    "Sentence [[1]] reports our tendency to admire the person who struggles against temptation, sentence [[2]] turns ('Yet') to the untempted person as the better one, sentence [[3]] explains why the struggle is a mixed sign, and sentence [[4]] reconciles the two ('then') by treating struggle as a stage towards virtue. Sentence [[X]] uses the paragraph's vocabulary of desire and moral assessment, but it raises a separate question, blame for unchosen desires, which no other sentence takes up; the paragraph is about whom we should admire, not whom we may blame.",
    "Treating sentence [[X]] as part of the discussion because it mentions desires, without noticing that it concerns blame rather than admiration.",
    "V03A-effortless-virtue",
    "The odd sentence shares the moral vocabulary of desire and assessment; it is rejected because it asks a different question from the one the paragraph resolves.",
    traps=[(3, "Sentence [[3]] can look like a restatement, but it supplies the reason for the reversal in sentence [[2]]: the struggle shows the bad desire is still there, which is what sentence [[4]] builds on.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 002
ooo("V03-A-002", "Psychology",
    "Spaced study beats cramming for long-term retention, so revision should return to topics at intervals.", "Easy",
    ["Students who cram the night before an exam often perform reasonably well the next morning.",
     "Weeks later, however, much of what they learned has vanished, while material studied in several shorter sessions spread over time is retained far better.",
     "Psychologists call this the spacing effect, and one explanation is that each return to half-forgotten material forces the effortful recall that strengthens memory.",
     "The practical lesson is that a revision timetable should revisit topics at widening intervals rather than devote a single long block to each."],
    "Many students also find that background music helps them concentrate, though whether it improves learning remains uncertain.",
    "Sentences [[1]] and [[2]] contrast cramming with spaced study, sentence [[3]] names the result ('call this the spacing effect') and explains it, and sentence [[4]] draws the lesson for a revision timetable. Sentence [[X]] is about studying too, but it concerns concentration and background music, which has nothing to do with how study is distributed over time.",
    "Choosing a sentence simply because it is about students, without checking that it connects to the timing of study.",
    "V03A-spacing-effect",
    "The odd sentence moves to a different study habit and has no link to the timing argument.",
    traps=[(1, "Sentence [[1]] can seem to praise cramming against the drift of the paragraph, but the short-term success it reports is exactly what 'Weeks later, however' in sentence [[2]] sets up to overturn.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 003
ooo("V03-A-003", "Society and culture",
    "Recipes cannot carry the tacit judgements of cooking, which pass from person to person in the kitchen.", "Medium",
    ["A written recipe looks like a complete set of instructions, yet two cooks following it exactly can produce very different dishes.",
     "The difference lies in what the recipe leaves unsaid: how thick the batter should feel, what the onions should smell like when they are ready, when the heat must drop.",
     "Such judgements are learned by watching and tasting beside someone who already has them, not by reading.",
     "This is why cooking traditions have survived for generations in kitchens where little was ever written down, and why a cookbook alone rarely makes a cook."],
    "Recipes also record the history of trade, since a dish that calls for pepper or cloves tells us which spices a region could obtain.",
    "Sentence [[1]] sets up the puzzle that the same recipe yields different dishes, sentence [[2]] explains 'The difference' by what recipes leave unsaid, sentence [[3]] says how 'Such judgements' are acquired, and sentence [[4]] draws the consequence ('This is why') for how cooking is passed on. Sentence [[X]] is about recipes, but it treats them as historical evidence of trade, which has nothing to do with the argument that written instructions cannot carry a cook's judgement.",
    "Accepting sentence [[X]] because it is about recipes, without checking that it serves the argument about what recipes fail to transmit.",
    "V03A-recipes-and-tacit-skill",
    "The odd sentence shares the paragraph's central term and is rejected only on function: it uses recipes as evidence rather than asking what they can teach.",
    traps=[(1, "Sentence [[1]] may look like a mere observation, but 'The difference' in sentence [[2]] refers to the different dishes it describes.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 004
ooo("V03-A-004", "History and politics",
    "The secret ballot freed voters from those who could watch and punish them, making the vote truly theirs.", "Medium",
    ["For much of the history of elections, voters declared their choices in public, by a show of hands or by calling out a name before officials and neighbours.",
     "Open voting let landlords, employers and party agents see exactly how each person voted, and reward or punish them accordingly.",
     "The secret ballot removed that possibility, because a vote that cannot be seen cannot be reliably bought or punished.",
     "Its effect was to make the vote belong more fully to the voter, whose choice no longer had to answer to those with power over their livelihood."],
    "Open voting was also slow, since each voter had to be called forward and the choice recorded by hand before the next could speak.",
    "Sentence [[1]] describes public voting, sentence [[2]] shows how it exposed voters to pressure from the powerful, sentence [[3]] explains how the secret ballot removed 'that possibility', and sentence [[4]] states 'Its effect' on the voter's independence. Sentence [[X]] is about open voting too, but it makes a point about slowness, a practical inconvenience that plays no part in an argument about coercion and the voter's freedom.",
    "Accepting sentence [[X]] because it begins with 'Open voting', as sentence [[2]] does, and adds a further drawback, without asking whether that drawback connects to the secret ballot's purpose.",
    "V03A-secret-ballot",
    "The odd sentence shares the subject and opens like a coherent sentence; it is rejected because its drawback (delay) is not the one the secret ballot answers (pressure).",
    traps=[(4, "Sentence [[4]] may look like a summary that could be dropped, but it states what the paragraph is building to: the ballot's effect on whom the vote answers to, which links back to the 'landlords, employers and party agents' of sentence [[2]].")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 005
ooo("V03-A-005", "Economics and business",
    "If tips track mood and appearance rather than service, tipping shifts risk to workers without supplying its supposed incentive.", "Easy",
    ["In countries where tipping is customary, a large share of a waiter's income may depend on the generosity of strangers.",
     "Defenders of the custom argue that it rewards good service, since diners can tip more when they are well looked after.",
     "Critics reply that tips track the customer's mood, the size of the bill and even the server's appearance more closely than the quality of service.",
     "If the critics are right, tipping transfers risk from employers to workers without delivering the incentive that is supposed to justify it."],
    "In some restaurants the bill is presented in a small folder, a convention that lets the diner work out a tip without being watched.",
    "Sentence [[1]] establishes that waiters' income depends on tips, sentence [[2]] gives the defence of the custom, sentence [[3]] gives the critics' reply, and sentence [[4]] draws the conclusion 'If the critics are right', linking the risk of sentence [[1]] with the failed incentive of sentence [[2]]. Sentence [[X]] is about tipping, but it describes a point of restaurant etiquette that plays no part in the debate over whether tips reward service.",
    "Choosing sentence [[1]] because it states a fact rather than an argument, though the conclusion depends on it.",
    "V03A-tipping-incentives",
    "The paragraph is a simple defence and reply; the odd sentence is a piece of etiquette with no argumentative role.",
    traps=[(1, "Sentence [[1]] is needed: the 'risk' that sentence [[4]] says tipping transfers to workers is the dependence of income on strangers that sentence [[1]] describes.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 006
ooo("V03-A-006", "Science and environment",
    "Street lights trap night-flying insects with effects on food webs, but better lighting design can reduce the toll.", "Medium",
    ["Many night-flying insects are drawn to artificial lights and, once there, circle them until they are exhausted or eaten.",
     "A single street lamp can therefore draw insects out of the surrounding habitat night after night, acting as a trap rather than a beacon.",
     "Because insects pollinate plants and feed birds and bats, losses at countless lamps may ripple through whole food webs.",
     "Shielding lamps, dimming them late at night or choosing wavelengths that attract fewer insects can reduce this toll without leaving streets dark."],
    "Artificial light also hides the stars from many city dwellers, who may go years without seeing the Milky Way.",
    "Sentence [[1]] describes how insects are drawn to lights, sentence [[2]] draws the consequence ('therefore') that a lamp acts as a trap, sentence [[3]] widens the harm to food webs, and sentence [[4]] proposes ways to reduce 'this toll'. Sentence [[X]] is about artificial light at night too, but it concerns what people lose sight of, not what happens to insects, so it connects to none of the steps about insects, food webs or lamp design.",
    "Grouping every effect of artificial light together and so missing that the paragraph is about one harm, the toll on insects.",
    "V03A-street-lights-and-insects",
    "The odd sentence shares the theme of light pollution and begins with 'also'; it is rejected because it changes the victim from insects to people.",
    traps=[(3, "Sentence [[3]] can look like a jump from lamps to ecology, but it explains why the trap of sentence [[2]] matters, and the 'toll' of sentence [[4]] includes these losses.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 007
ooo("V03-A-007", "Philosophy and ethics",
    "The intuition that harming is worse than failing to rescue can be defended: negative duties, unlike positive ones, can be honoured by everyone at once.", "Difficult",
    ["Most people judge it worse to push someone into a river than to fail to rescue a stranger who has fallen in, even when the outcome is the same.",
     "Some philosophers dismiss this intuition as a bias, arguing that if the consequences are identical, the moral verdicts should be too.",
     "Defenders of the distinction answer that a duty not to harm can be owed to everyone at once, whereas a duty to rescue everyone in danger would consume a whole life.",
     "On their account the asymmetry is no bias but a recognition that negative duties, unlike positive ones, can be fully honoured by every person simultaneously."],
    "Philosophers also disagree about whether an omission can be a cause at all, since if failing to rescue causes a death, so do the failures of everyone else who might have helped.",
    "Sentence [[1]] states the intuition, sentence [[2]] reports the objection that it is a bias, sentence [[3]] gives the defenders' answer in terms of what duties can be owed to everyone, and sentence [[4]] concludes 'On their account' that the asymmetry rests on a difference between negative and positive duties. Sentence [[X]] shares the vocabulary of omissions and rescue, but it opens a separate metaphysical question about causation; neither the objection nor the reply turns on whether omissions cause anything, so it attaches to nothing.",
    "Assuming that any point about omissions must support the defenders, when their reply rests entirely on the structure of duties, not on causation.",
    "V03A-doing-and-allowing",
    "All five sentences discuss acts and omissions in philosophical vocabulary; the odd one can be seen only by tracking that the debate is about justifying the asymmetry through duties, not about causation.",
    traps=[(2, "Sentence [[2]] can look like an interruption, but the defenders in sentence [[3]] 'answer' it, and sentence [[4]] denies precisely its charge that the asymmetry is a bias."),
           (4, "Sentence [[4]] may seem to repeat sentence [[3]], but it turns the defenders' point into the conclusion that answers sentence [[2]]: the asymmetry is 'no bias'.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 008
ooo("V03-A-008", "Psychology",
    "Curiosity peaks when we know enough to see a gap in our knowledge, which suggests how teachers can arouse it.", "Medium",
    ["Curiosity is often imagined as strongest when we know nothing about a subject, but it seems to peak when we know a little.",
     "Knowing a little lets us see that there is a gap between what we know and what we could know, and the gap is what we want to close.",
     "Complete ignorance offers no visible gap, while complete knowledge leaves none, so interest is lowest at both extremes.",
     "A teacher who wants to arouse curiosity might therefore begin not with a blank slate but with a partial picture and a puzzle it cannot yet explain."],
    "Curiosity may also improve memory for incidental details that a person happens to meet while waiting for an answer they care about.",
    "Sentence [[1]] claims that curiosity peaks at partial knowledge, sentence [[2]] explains why in terms of a visible gap, sentence [[3]] applies the gap idea to the two extremes, and sentence [[4]] draws the teaching lesson ('therefore'). Sentence [[X]] is about curiosity, but it describes an effect of curiosity on memory, whereas the paragraph is about what causes curiosity; nothing in the gap argument leads to it or depends on it.",
    "Accepting any claim about curiosity, and missing that the paragraph explains when curiosity arises, not what it does.",
    "V03A-curiosity-and-gaps",
    "The odd sentence shares the subject and a learning context that seems to fit the teacher; it is rejected because it reverses the direction from cause to effect.",
    traps=[(3, "Sentence [[3]] may look repetitive, but it extends the gap explanation to both extremes, which is what justifies avoiding the 'blank slate' in sentence [[4]].")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 009
ooo("V03-A-009", "Society and culture",
    "Public libraries matter today less for lending books than as free indoor public space.", "Easy",
    ["Public libraries are often discussed as if their only purpose were lending books, a function that cheap downloads seem to make obsolete.",
     "In practice, many serve as one of the last indoor spaces where a person can stay for hours without being expected to buy anything.",
     "Students without quiet rooms at home, job seekers without computers and elderly readers who want company all depend on that free, open space.",
     "Judged by these uses, the library is less a warehouse of books than a piece of social infrastructure."],
    "The earliest libraries kept clay tablets and scrolls, and they were often open only to priests, officials and scholars.",
    "Sentence [[1]] states the common view that libraries exist to lend books, sentence [[2]] counters it with what libraries do 'in practice', sentence [[3]] lists who depends on 'that free, open space', and sentence [[4]] concludes from 'these uses'. Sentence [[X]] is about libraries, but it describes the distant past and restricted access, which has no place in an argument about the present role of public libraries.",
    "Choosing a sentence on the same institution without noticing the shift of period and purpose.",
    "V03A-library-as-public-space",
    "The odd sentence moves to ancient history, an easily spotted change of time and scope.",
    traps=[(1, "Sentence [[1]] states a view the paragraph rejects, which can make it look odd, but the contrast 'In practice' in sentence [[2]] needs it.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 010
ooo("V03-A-010", "History and politics",
    "In ancient states, issuing coins was a political declaration of who ruled.", "Medium",
    ["In many ancient states, minting coins was as much a political act as an economic one.",
     "A ruler's portrait or emblem stamped on every coin carried a claim of authority into markets far beyond the reach of his officials.",
     "That is why rebels and usurpers often struck coins of their own almost as soon as they seized power, even before they could collect taxes.",
     "To issue money was to announce, in a form that passed through every hand, who now governed."],
    "Before coinage, many exchanges were settled in goods such as grain or cattle, whose value varied with the season and their condition.",
    "Sentence [[1]] claims that minting was a political act, sentence [[2]] explains how a coin carried the ruler's claim of authority, sentence [[3]] draws on that ('That is why') to explain why usurpers minted at once, and sentence [[4]] states the general point. Sentence [[X]] is about money and exchange, but it describes what came before coinage and the economic drawback of goods as money, which says nothing about coins as political statements.",
    "Assuming that any sentence on the history of money belongs, when the paragraph argues about the political meaning of coins.",
    "V03A-coinage-and-authority",
    "The odd sentence shares the theme of money; it is rejected because it makes an economic point about barter, not a political one about coins.",
    traps=[(3, "Sentence [[3]] can look like a narrow historical detail, but 'That is why' ties it to sentence [[2]], and it is the evidence that coins served authority even before taxation did.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 011
ooo("V03-A-011", "Economics and business",
    "Airlines overbook to earn from predictable no-shows, and the policy pays while compensation costs less than empty seats.", "Medium",
    ["Many airlines sell more seats on a flight than the aircraft holds, because a predictable share of passengers fail to turn up.",
     "Flying with those seats empty would waste revenue that cannot be recovered once the plane has left.",
     "Overbooking turns this predictable absence into income, at the price of occasionally having more passengers at the gate than seats.",
     "The airline then pays compensation to volunteers who agree to take a later flight, and the policy pays as long as such payments cost less than the empty seats would have."],
    "Fares also tend to rise as the departure date approaches, since travellers who book late are often less sensitive to price.",
    "Sentence [[1]] states the practice and its basis in no-shows, sentence [[2]] gives the cost of not overbooking ('those seats empty'), sentence [[3]] shows how overbooking recovers 'this predictable absence' at a risk, and sentence [[4]] explains how the risk is handled and when the policy pays. Sentence [[X]] is about airline revenue, but it describes how fares change over time, a pricing strategy unrelated to selling seats beyond capacity.",
    "Treating every airline revenue practice as belonging, when the paragraph explains a single one, overbooking.",
    "V03A-airline-overbooking",
    "The odd sentence shares the setting and the theme of revenue; it is rejected because its mechanism (pricing by booking date) is not the one under discussion.",
    traps=[(2, "Sentence [[2]] can look obvious and removable, but 'those seats' refers to the no-shows of sentence [[1]], and the revenue it says would be lost is what sentence [[3]] says overbooking recovers.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 012
ooo("V03-A-012", "Science and environment",
    "Ploughing depletes soil organic matter, which has led some farmers to reduced tillage.", "Easy",
    ["Ploughing breaks up the soil and buries weeds, which is why farmers have relied on it for thousands of years.",
     "But each pass also exposes organic matter to air, speeding its decay and releasing carbon that the soil had stored.",
     "Repeated ploughing can therefore leave fields poorer in organic matter and more prone to erosion.",
     "For this reason some farmers have moved to reduced tillage, sowing seed directly into the residue of the previous crop."],
    "Tractors replaced draught animals on many farms during the twentieth century, greatly increasing the area one worker could cultivate.",
    "Sentence [[1]] gives the benefits of ploughing, sentence [[2]] introduces its cost with 'But', sentence [[3]] states the consequence ('therefore') for the soil, and sentence [[4]] describes the response 'For this reason'. Sentence [[X]] is about farming, but it concerns the mechanisation of labour, not what ploughing does to the soil.",
    "Choosing a sentence because it is about farms, without checking whether it bears on soil organic matter.",
    "V03A-tillage-and-soil-carbon",
    "The odd sentence turns to farm labour and machinery, an obvious change of focus.",
    traps=[(1, "Sentence [[1]] praises ploughing while the paragraph criticises it, but the 'But' of sentence [[2]] needs the benefit it states.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 013
ooo("V03-A-013", "Philosophy and ethics",
    "Testimony is a real source of knowledge, but trusting it well requires judging sources.", "Medium",
    ["Most of what any of us believes, from the shape of the Earth to the date of our own birth, rests on the word of others rather than on our own observation.",
     "If knowledge required checking everything for ourselves, we would know almost nothing.",
     "Yet trust in testimony need not be blind, for we can ask whether a source has been reliable before and whether it has any motive to deceive.",
     "Testimony is thus a genuine source of knowledge, but one that leaves us with the work of deciding whom to believe."],
    "In a courtroom, testimony is usually given under oath, and lying under oath is itself a punishable offence.",
    "Sentence [[1]] observes that most belief rests on the word of others, sentence [[2]] shows that knowledge could not do without it, sentence [[3]] answers the worry that such trust is blind, and sentence [[4]] concludes ('thus') that testimony yields knowledge but demands judgement. Sentence [[X]] uses the word testimony in its legal sense and describes court procedure, which plays no part in an argument about how ordinary belief can rest on others' word.",
    "Linking the oath to the 'motive to deceive' in sentence [[3]] and so treating a point of legal procedure as part of a general argument about knowledge.",
    "V03A-knowledge-from-testimony",
    "The odd sentence shares the key term and could seem to illustrate a motive not to deceive; it must be rejected because it shifts from the epistemology of belief to court procedure.",
    traps=[(2, "Sentence [[2]] may look too short to matter, but it is the reason sentence [[1]] matters: without it there is no case that testimony must count as knowledge.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 014
ooo("V03-A-014", "Psychology",
    "Idle and uncertain waits feel longer, so waits can be made more bearable without being shortened.", "Easy",
    ["Time spent waiting with nothing to do feels longer than the same time spent occupied.",
     "This is why some buildings place mirrors beside their lifts, giving people something to look at while they wait.",
     "Uncertainty stretches waiting further, so a delay of unknown length can feel worse than a longer one that has been announced in advance.",
     "Those who manage waiting rooms and counters can therefore make waits more bearable without shortening them, simply by filling the time and telling people how long it will last."],
    "Waiting for a reward can also be a test of self-control, as when a child is asked to hold off eating one sweet in order to earn two.",
    "Sentence [[1]] states that idle waiting feels longer, sentence [[2]] gives a practice explained by that ('This is why'), sentence [[3]] adds a second factor, uncertainty, and sentence [[4]] draws the lesson ('therefore') from both, filling the time and announcing its length. Sentence [[X]] is about waiting, but it treats waiting as a test of self-control, not as an experience whose felt length can be managed, so it connects to none of the other sentences.",
    "Choosing a sentence on the same word, waiting, without checking that it concerns how long a wait feels.",
    "V03A-felt-length-of-waiting",
    "The odd sentence uses the paragraph's key word in a different sense, and the paragraph's own chain of reasons is explicit.",
    traps=[(3, "Sentence [[3]] introduces a new factor and can look like a change of subject, but sentence [[4]] needs it: 'telling people how long it will last' is the remedy for uncertainty.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 015
ooo("V03-A-015", "Society and culture",
    "Oral epic singers recompose rather than memorise, so their idea of sameness is fidelity to story, not to a fixed text.", "Difficult",
    ["It was once assumed that singers of long oral epics must have memorised their poems word for word, as a modern actor learns a script.",
     "Closer study of living traditions suggested something different: singers rebuild each performance from a stock of formulaic phrases and familiar scenes.",
     "Two performances of the 'same' epic by one singer may therefore differ in hundreds of lines, while the singer insists, sincerely, that he has sung it exactly as before.",
     "What he means by sameness is fidelity to the story and its traditional manner, not repetition of a fixed text, a notion that belongs to cultures of writing."],
    "Writing, by contrast, allowed a poem to survive the death of every singer who knew it.",
    "Sentence [[1]] reports the old assumption of word-for-word memory, sentence [[2]] corrects it with the finding that singers rebuild each performance, sentence [[3]] draws the consequence ('therefore') that two performances differ though the singer calls them the same, and sentence [[4]] explains what 'sameness' means to him. Sentence [[X]] picks up the word 'writing' from sentence [[4]], but it turns to the survival of poems, a question of preservation; 'by contrast' sets writing against oral tradition, but on a point, survival, that the paragraph never raises; the paragraph is about what counts as the same poem in an oral tradition, and no sentence builds on or leads to a claim about preservation.",
    "Attaching sentence [[X]] to the end of sentence [[4]] because both mention writing, without noticing that the paragraph never discusses whether poems survive.",
    "V03A-oral-epic-sameness",
    "The odd sentence borrows a key word and a contrastive connective that seem to continue the last sentence; it is rejected only by seeing that its topic, preservation, is not the paragraph's topic, sameness.",
    traps=[(1, "Sentence [[1]] states a view the paragraph rejects, which tempts students to drop it, but 'something different' in sentence [[2]] needs it, and the actor's script is the model of sameness that sentence [[4]] sets aside."),
           (4, "Sentence [[4]] can look like a philosophical add-on, but it resolves the puzzle of sentence [[3]]: why the singer can sincerely call two different performances the same.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 016
ooo("V03-A-016", "History and politics",
    "Term limits trade protection against entrenchment for lost choice and experience, so their wisdom depends on context.", "Medium",
    ["Limits on how long a leader may hold office are meant to prevent the slow entrenchment of power, in which an incumbent bends institutions in order to keep winning.",
     "A leader who knows she must leave has less reason to capture courts or electoral bodies, since she will not be there to benefit.",
     "The cost is that voters lose the option of keeping a leader they still want, and the experience she has gained leaves with her.",
     "Whether term limits are wise therefore depends on how real the danger of entrenchment is in a given country, set against the value of that lost choice and experience."],
    "Many constitutions also set a minimum age for high office, on the view that maturity should come before power.",
    "Sentence [[1]] states the purpose of term limits, sentence [[2]] explains how they work against entrenchment, sentence [[3]] states 'The cost', and sentence [[4]] weighs the benefit against 'that lost choice and experience'. Sentence [[X]] concerns another constitutional rule about who may hold office, but an age requirement has nothing to do with entrenchment or the cost of forcing leaders out, so it plays no part in the trade-off.",
    "Treating any constitutional limit on office as part of the argument, when the paragraph weighs one rule only.",
    "V03A-term-limits",
    "The odd sentence shares the constitutional vocabulary and opens with 'also'; it is rejected because the paragraph is a cost and benefit analysis of term limits alone.",
    traps=[(3, "Sentence [[3]] runs against the case for term limits, but it is needed: sentence [[4]] weighs the danger of entrenchment against exactly the cost it states.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 017
ooo("V03-A-017", "Economics and business",
    "Rotating savings groups let people without banks save and borrow, with reputation in place of collateral.", "Easy",
    ["In a rotating savings group, each member contributes a fixed sum every month, and each month one member takes the whole pot.",
     "The member who receives it first gets, in effect, an interest-free loan, while the one who receives it last has simply saved.",
     "What keeps the arrangement from collapsing is social pressure: members are usually neighbours or colleagues who would lose face by defaulting after their turn.",
     "Such groups thus let people without access to banks save and borrow, using reputation in place of collateral."],
    "Many banks now offer mobile applications that let customers open an account without ever visiting a branch.",
    "Sentence [[1]] describes how a rotating savings group works, sentence [[2]] shows that it acts as a loan for early recipients and as saving for late ones, sentence [[3]] explains what prevents default, and sentence [[4]] concludes ('thus') what such groups achieve. Sentence [[X]] is about finance, but it describes banking technology, which has nothing to do with the informal mechanism the paragraph analyses.",
    "Choosing a sentence because it seems to contrast with banks, without seeing that the paragraph is about how the informal group itself works.",
    "V03A-rotating-savings-groups",
    "The odd sentence turns to formal banking technology, an evident change of focus.",
    traps=[(3, "Sentence [[3]] can look like a remark about social life, but it explains why the early recipient of sentence [[2]] does not run off, and it supplies the 'reputation' of sentence [[4]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 018
ooo("V03-A-018", "Science and environment",
    "A rugged coast has no single length, since measured length grows as the ruler shrinks; what can be compared is how length scales.", "Difficult",
    ["The length of a rugged coastline is not a fixed quantity waiting to be measured; it depends on the length of the ruler used to measure it.",
     "A surveyor stepping along it with a long rod skips every inlet smaller than the rod, while one using a short rod follows them and records a greater total.",
     "As the ruler shrinks, the measured length keeps growing, because ever smaller bays and rocks come into the count.",
     "The sensible question is therefore not how long a coast is, but how its measured length changes with the scale of measurement, a property that can be compared between coasts."],
    "Coastlines also change over time, as waves wear away headlands and rivers build new land at their mouths.",
    "Sentence [[1]] claims that a coast's length depends on the ruler, sentence [[2]] shows why with the long and short rods, sentence [[3]] generalises to an ever shrinking ruler, and sentence [[4]] concludes ('therefore') that the useful quantity is how length changes with scale. Sentence [[X]] also suggests that a coast's length is not fixed, but for a different reason: the coast itself changes. The paragraph's argument holds for a coast frozen in time, since it is about measurement, so sentence [[X]] supports none of its steps.",
    "Taking sentence [[X]] as support for 'not a fixed quantity' in sentence [[1]], and missing that sentence [[1]] at once names its reason, the length of the ruler.",
    "V03A-coastline-measurement",
    "The odd sentence seems to support the opening claim that length is not fixed; rejecting it needs the distinction between a coast that changes and a measurement that depends on scale.",
    traps=[(3, "Sentence [[3]] can look like a repetition of sentence [[2]], but it turns two rods into a trend ('keeps growing') without which the conclusion about how length changes with scale has no basis."),
           (4, "Sentence [[4]] may look like a change of subject from measuring to comparing, but it is the conclusion the paragraph has been building towards.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 019
ooo("V03-A-019", "Philosophy and ethics",
    "Whether copying is theft turns on whether a creator can own the opportunity of being the only source.", "Easy",
    ["Taking someone's bicycle deprives them of it, but copying someone's idea leaves them with the idea intact.",
     "For this reason some argue that copying cannot be theft in the ordinary sense, since nothing has been taken away.",
     "Others reply that what the creator loses is not the idea but the chance to profit from being its only source.",
     "The dispute over copying is thus a dispute about whether that lost opportunity is something a person can rightly own."],
    "Bicycles are often stolen in cities, because they are easy to ride away and hard to trace once they are repainted.",
    "Sentence [[1]] contrasts taking a bicycle with copying an idea, sentence [[2]] draws one side's conclusion ('For this reason'), sentence [[3]] gives the reply of 'Others', and sentence [[4]] states what the dispute turns on ('that lost opportunity'). Sentence [[X]] picks up the bicycle, but it is about urban bicycle theft, which plays no part in the argument over whether copying an idea is theft.",
    "Linking sentence [[X]] to the bicycle in sentence [[1]] without noticing that the bicycle is only a point of comparison.",
    "V03A-copying-and-theft",
    "The odd sentence borrows the illustration from the first sentence but has nothing to do with the argument; the shift is easy to spot.",
    traps=[(1, "Sentence [[1]] may look like a homely illustration that could be dropped, but 'For this reason' in sentence [[2]] depends on its contrast.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 020
ooo("V03-A-020", "Psychology",
    "People slacken in groups because their effort is invisible, so making contributions visible restores effort.", "Medium",
    ["When several people pull on a rope together, each tends to pull less hard than when pulling alone.",
     "The likeliest reason is that in a group no one's individual effort can be seen, so slacking carries no personal cost.",
     "Consistent with this, the effect shrinks when each person's contribution is measured separately, even though the task stays the same.",
     "Managers who want full effort from teams may therefore need to make individual contributions visible, rather than merely urging everyone to try harder."],
    "Groups can also reach riskier decisions than their members would reach alone, as discussion pushes opinion towards an extreme.",
    "Sentence [[1]] reports the drop in individual effort in a group, sentence [[2]] explains it by the invisibility of each person's effort, sentence [[3]] offers evidence 'Consistent with this', and sentence [[4]] draws the lesson for managers ('therefore'). Sentence [[X]] is about group behaviour too, but it concerns how group discussion shifts decisions, not how hard members work, so it connects to neither the explanation nor the remedy.",
    "Treating every finding about groups as belonging, when the paragraph is about one effect, reduced effort, and its cause.",
    "V03A-effort-in-groups",
    "The odd sentence shares the group setting and the vocabulary of individuals versus groups; it is rejected because it concerns judgement, not effort.",
    traps=[(3, "Sentence [[3]] may look like a technical detail, but it is the evidence for the explanation in sentence [[2]], and it is why sentence [[4]] recommends measuring contributions.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 021
ooo("V03-A-021", "Society and culture",
    "Fashion changes not along a single ladder of elite imitation but because many groups define themselves against one another.", "Difficult",
    ["Fashion is often explained as a chase: elites adopt a style to set themselves apart, others imitate it, and the elites move on once the style has become common.",
     "The account explains why styles change, but it struggles with the many trends that begin among the young or the poor and only later reach expensive shops.",
     "A more plausible view is that distinction can be sought in many directions, by groups who wish to differ from their parents, their rivals or the mainstream as a whole.",
     "Change then comes not from a single ladder of imitation but from many groups, each defining itself against the others."],
    "Because clothes are cheap to replace, fashion in dress moves faster than taste in housing or furniture, which shifts only over decades.",
    "Sentence [[1]] states the chase theory, sentence [[2]] grants what 'The account' explains and names what it cannot, sentence [[3]] offers 'A more plausible view', and sentence [[4]] states what that view implies about change ('then'). Sentence [[X]] is about how fashion changes, but it addresses its speed and explains it by cost; the paragraph asks where changes in style come from and who drives them, and no sentence answers or builds on a point about speed.",
    "Attaching sentence [[X]] because it, like the paragraph, explains fashion change, and missing that the paragraph is about the source of change, not its pace.",
    "V03A-sources-of-fashion-change",
    "Every sentence concerns why fashion changes; the odd one must be separated by seeing that it answers 'how fast' rather than 'from where', and the opening sentence states a view the author rejects, which tempts students to remove it.",
    traps=[(1, "Sentence [[1]] states a view the author goes on to reject, which makes it look odd, but 'The account' in sentence [[2]] refers to it and the 'single ladder' of sentence [[4]] is its picture of change."),
           (3, "Sentence [[3]] can look like an abstract aside, but it is the alternative that sentence [[4]] draws its conclusion from; without it the paragraph criticises a theory and offers nothing in its place.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 022
ooo("V03-A-022", "History and politics",
    "A monument's meaning changes with each generation, so disputes over statues are disputes over a city's story.", "Easy",
    ["A public statue is usually erected to fix a particular memory of a person or event in the life of a city.",
     "But the meaning of a monument does not stay fixed, for each generation passes it with different knowledge and different concerns.",
     "A figure honoured as a founder by one age may be seen by a later one chiefly as a symbol of the injustices of his time.",
     "The arguments that periodically erupt over old statues are thus less about stone and bronze than about who controls the story a city tells about itself."],
    "Bronze has long been favoured for outdoor statues because it withstands rain and frost better than many kinds of stone.",
    "Sentence [[1]] states what a statue is meant to do, sentence [[2]] says its meaning nonetheless changes ('But'), sentence [[3]] gives an example of such a change, and sentence [[4]] concludes ('thus') what disputes over statues are about. Sentence [[X]] is about statues, but it concerns the durability of their material, which has nothing to do with how their meaning shifts.",
    "Linking sentence [[X]] to 'stone and bronze' in sentence [[4]], though that phrase says precisely that the material is not what matters.",
    "V03A-changing-meaning-of-monuments",
    "The odd sentence is about the physical object while the paragraph is about meaning; the shift is easy to see.",
    traps=[(3, "Sentence [[3]] may look like a provocative aside, but it is the example that shows the change of meaning claimed in sentence [[2]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 023
ooo("V03-A-023", "Economics and business",
    "Insurance weakens the incentive to take care, so good policies share losses with the insured and balance cover against care.", "Difficult",
    ["Insurance protects people against losses they cannot afford, but by doing so it can weaken their incentive to avoid those losses.",
     "A driver whose car is fully insured has less reason to park it carefully than one who would bear the cost of every scratch.",
     "Insurers respond by making the insured share part of the loss, through deductibles and co-payments, so that carelessness still costs something.",
     "The design of a good policy is therefore a compromise: enough cover to provide security, but not so much that the insured stop taking care."],
    "Insurers also worry that the people most eager to buy cover are those who know privately that they face the highest risk.",
    "Sentence [[1]] states that insurance can weaken the incentive to avoid loss, sentence [[2]] illustrates it with the driver, sentence [[3]] describes the insurers' response 'so that carelessness still costs something', and sentence [[4]] concludes that policy design balances security against care. Sentence [[X]] names a real problem for insurers, but a different one: who chooses to buy insurance, not how people behave once insured. The deductibles of sentence [[3]] are justified by carelessness and the compromise of sentence [[4]] is about taking care, so neither answers or follows from sentence [[X]].",
    "Treating sentence [[X]] as a further problem that the deductibles of sentence [[3]] respond to, and missing that the paragraph's chain is about care taken after insurance is bought.",
    "V03A-insurance-and-care",
    "All five sentences concern problems insurers face, in the same technical vocabulary; separating the odd one requires distinguishing a problem of behaviour after purchase from a problem of who buys.",
    traps=[(2, "Sentence [[2]] can look like a dispensable example, but it makes the weakened incentive of sentence [[1]] concrete, and the 'carelessness' of sentence [[3]] is the careless parking it describes."),
           (3, "Sentence [[3]] may seem to start a new topic with the insurers' viewpoint, but it is the response to sentence [[1]] that sentence [[4]] generalises into a principle of design.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 024
ooo("V03-A-024", "Science and environment",
    "Mangroves protect coasts from waves and erosion, making their protection a cheap, self-maintaining sea defence.", "Medium",
    ["Mangrove forests grow in the shallow, salty margins between land and sea, where few other trees can survive.",
     "Their dense, tangled roots slow incoming waves and trap sediment, so that coasts behind them suffer less erosion and less damage from storm surges.",
     "Where mangroves have been cleared for fish ponds or seaside building, the same coasts often become far more exposed.",
     "Protecting mangroves can thus be a cheaper defence against the sea than building concrete walls, as well as one that maintains itself."],
    "Mangrove wood is dense and resists rot, and in some places it has long been cut for charcoal and for building poles.",
    "Sentence [[1]] places mangroves at the meeting of land and sea, sentence [[2]] explains how 'Their' roots protect the coast, sentence [[3]] confirms the effect by what happens when they are cleared, and sentence [[4]] concludes ('thus') that protecting them is a cheap sea defence. Sentence [[X]] is about mangroves too, but it concerns the uses of their wood, not their protective role, and nothing before or after it builds on that point.",
    "Linking sentence [[X]] to the clearing in sentence [[3]] as an extra reason mangroves are cut, though the paragraph's concern is what clearing does to the coast.",
    "V03A-mangroves-as-sea-defence",
    "The odd sentence shares the subject and could seem to explain why mangroves are cleared; it is rejected because it concerns resource use, not coastal protection.",
    traps=[(1, "Sentence [[1]] may look like scene-setting that could be cut, but 'Their dense, tangled roots' in sentence [[2]] needs it as its referent, and it places the forests at the edge they protect.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 025
ooo("V03-A-025", "Science and environment",
    "Seed banks preserve crop diversity unchanged, which is also their limit, so they complement rather than replace conservation on farms.", "Medium",
    ["Seed banks store the seeds of crop varieties in cold, dry vaults, so that diversity lost in the field can one day be restored.",
     "Their great strength is that a stored seed stays genetically as it was when it was collected.",
     "That strength is also a limitation, for the varieties still growing in fields keep adapting to new pests and a changing climate, while the frozen seeds do not.",
     "Conservation in vaults is therefore best seen as a complement to conservation on farms, not a substitute for it."],
    "Some vaults are built deep inside mountains or permafrost, so that the seeds stay cold even if the power fails.",
    "Sentence [[1]] states what seed banks are for, sentence [[2]] names 'Their great strength', sentence [[3]] turns 'That strength' into a limitation, and sentence [[4]] concludes ('therefore') that vaults complement farms. Sentence [[X]] is about seed vaults, but it describes how they are engineered to stay cold, which bears neither on the strength and limitation of unchanging seeds nor on the conclusion.",
    "Choosing a sentence because it seems technical, or accepting sentence [[X]] because it describes seed banks, without checking its role in the argument.",
    "V03A-seed-banks-and-farms",
    "The odd sentence shares the subject and vocabulary; it is rejected because it concerns engineering, not the argument about frozen versus evolving diversity.",
    traps=[(2, "Sentence [[2]] can look like praise that could be dropped, but 'That strength' in sentence [[3]] refers to it, and the whole argument turns on its being also a limitation.")],
    cognitive="Analysis")

