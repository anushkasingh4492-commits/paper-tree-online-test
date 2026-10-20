import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DX = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ps("V02-G-001", "Technology", "Clumsy standards survive because wide adoption gives them dependants, so their persistence records success.", "Medium",
   "Engineers often speak of legacy systems as if they were merely old, but what makes a legacy difficult is not its age but the number of things that have come to depend on it. A file format, a connector or a programming interface that was widely adopted becomes a promise to everyone who built on it, and each new version must keep that promise or break their work. This is why designs that almost everyone agrees are clumsy survive for decades: the cost of changing them would be borne not by the designer but by thousands of users who would all have to adapt at once. The awkwardness of a long-lived standard is therefore less a sign of poor judgement than a record of its success; only what was widely adopted acquires enough dependants to become impossible to fix.",
   "Awkward standards endure because wide adoption gives them many dependants who would bear the cost of any change, so their persistence reflects success, not poor design.",
   [("Old technical systems are hard to replace mainly because of their age, since the knowledge needed to modify them is lost as their original designers retire.",
     "The first sentence says the difficulty is 'not its age but the number of things that have come to depend on it', so this option names the very cause the paragraph rejects."),
    ("Designers of widely used standards should refuse to change them at all, because every new version breaks the work of the users who built on them.",
     "The paragraph explains why clumsy standards persist; it prescribes nothing, and it says each new version 'must keep that promise', which implies versions are made, not refused."),
    ("A widely adopted file format or connector becomes a promise to its users, and every later version of it has to remain compatible with their work.",
     "This restates only the second sentence and omits the paragraph's conclusion that a standard's awkwardness is 'a record of its success'.")],
   "The paragraph explains a phenomenon: clumsy standards survive because adoption creates dependants, the cost of change falls on those many users, and so awkwardness that cannot be fixed is evidence of success. The correct answer keeps the mechanism (dependants bearing the cost) and the conclusion (success, not poor judgement).",
   "Picking the compatibility option because it uses the paragraph's own terms, without noticing that it drops the conclusion about success.",
   "V02G-backward-compatibility", "The narrow distractor is a faithful paraphrase of one sentence, so the reader must test for the paragraph's conclusion.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 002
ps("V02-G-002", "Technology", "Tracking consent banners give only the appearance of control because their design steers the answer.", "Easy",
   "It is often said that the banners asking website visitors to accept or refuse tracking have handed people control over their personal data. The claim assumes that a choice offered is a choice made. In practice, a visitor who wants to read an article is asked, at the worst possible moment, to weigh consequences that are invisible and distant against an obstacle that is immediate and irritating. Many banners make acceptance a single click while refusal requires several screens of toggles. Unsurprisingly, most people click whatever makes the banner disappear. A mechanism built in this way records the visitor's impatience rather than the visitor's preference, and it lends the appearance of consent to an outcome largely decided by the design of the box.",
   "Consent banners only appear to give control: their timing and lopsided design lead people to click whatever removes them, so answers reflect impatience, not preference.",
   [("Most internet users do not really care about their personal data, which is why they accept tracking without reading what the banners on websites ask them.",
     "The paragraph attributes the clicks to timing and design ('an obstacle that is immediate and irritating'), not to indifference about data, so this supplies a cause the paragraph does not give."),
    ("Websites should be banned from tracking visitors altogether, since no banner, however carefully it was designed, could ever obtain genuine consent from a reader.",
     "The paragraph blames a mechanism 'built in this way', which implies that design matters; it neither says consent is impossible nor proposes a ban."),
    ("On many websites accepting tracking takes a single click, while refusing it requires the visitor to work through several screens of separate toggles.",
     "This is one supporting detail; it leaves out the central claim that the resulting 'consent' records impatience and only appears to give control.")],
   "The paragraph critiques the view that banners give people control. Its reasons are the timing of the request and the asymmetry between accepting and refusing, and its conclusion is that the banner records impatience and lends 'the appearance of consent'. The correct answer states the critique, the reasons and the conclusion.",
   "Choosing the ban because the paragraph is critical of banners, although it criticises a particular design, not consent as such.",
   "V02G-cookie-consent-banners", "The conclusion is stated outright in the last sentence and each distractor is plainly narrow, extreme or off-cause.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 003
ps("V02-G-003", "Technology", "Efficiency savings are partly eaten by extra use, but the size of the rebound varies, so estimate honestly.", "Difficult",
   "Making a machine more efficient seems an obvious way to reduce the energy it consumes, but economists have long noted an awkward complication. When a service becomes cheaper to run, people tend to use more of it: a more economical car makes longer journeys affordable, and cheaper lighting invites more of it. Some of the expected saving is therefore taken back in additional use. It does not follow, as enthusiasts of the idea sometimes conclude, that efficiency is futile. Whether the rebound swallows a small or a large part of the saving depends on how much more of the service people actually want once its price falls, and for many household uses that appetite is limited; nobody keeps the fridge door open because the fridge is economical. The finding is a reason to estimate savings honestly, not a reason to abandon the pursuit of them.",
   "Cheaper services get used more, so some efficiency savings are lost, but how much depends on how much extra use people want, which calls for realistic estimates rather than abandoning efficiency.",
   [("Because cheaper energy services are always used more, gains in efficiency end up raising total consumption, so efforts to save energy through better machines defeat themselves.",
     "This is the conclusion of the 'enthusiasts' whom the paragraph corrects when it says 'It does not follow' that 'efficiency is futile'. The paragraph says only 'some' of the saving is taken back."),
    ("Gains in efficiency cut energy use roughly in proportion to the improvement, since for most household devices people do not use them more when running costs fall.",
     "The paragraph says 'Some of the expected saving is therefore taken back', so savings are not proportional; the fridge shows that the appetite for some uses is limited, not that rebound is absent."),
    ("The rebound in use is larger for cars and lighting than for refrigerators, so policy on efficiency should concentrate on household appliances rather than on transport.",
     "Cars, lighting and fridges are illustrations, not a ranking, and the paragraph makes no recommendation about where policy should concentrate.")],
   "The paragraph reports a finding (cheaper services are used more, so some saving is lost) and then qualifies it against two misreadings: it is not proof that efficiency is futile, and its size depends on how much extra use people want. The correct answer holds the finding, the condition and the closing moral ('estimate savings honestly').",
   "Taking the efficiency defeats itself option because the paragraph spends its first half on the rebound, missing the turn at 'It does not follow'.",
   "V02G-efficiency-rebound", "Two distractors are the opposite overreadings (rebound is total; rebound is absent), and the correct answer must sit between them with the right condition.",
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 004
ps("V02-G-004", "Technology", "Code maintained by a few volunteers is not a free good; popularity raises its upkeep.", "Medium",
   "Much of the software that businesses rely on is maintained by a handful of volunteers, sometimes by a single person working in spare hours. Companies that would never run a factory on an unpaid supplier routinely build products on such code and treat it as a free natural resource, like air. The comparison flatters them. Air does not need anyone to fix it; code does, and the work of fixing security flaws, answering bug reports and keeping up with changes elsewhere does not get easier as more people use a project. It gets harder. Popularity, which looks like a sign of health, can thus be precisely what exhausts the few people who keep a project alive. A firm that depends on such work and contributes nothing to it is not enjoying a free good but drawing down a stock that someone else is paying to replenish.",
   "Firms treat volunteer-maintained code as free like air, yet its upkeep rests on a few people and grows with popularity, so taking without contributing depletes their effort.",
   [("Popular open software tends to be healthier and more secure than obscure software, because its many users report bugs and help its small group of volunteers fix them.",
     "The paragraph says the reverse: maintenance 'does not get easier as more people use a project. It gets harder', and popularity 'can thus be precisely what exhausts' the maintainers."),
    ("Businesses ought to stop using software maintained by volunteers and should buy commercial products whose suppliers are contractually responsible for fixing security flaws.",
     "The paragraph criticises firms that contribute 'nothing'; it does not tell them to abandon volunteer code or switch to commercial suppliers, so this adds a prescription."),
    ("Many companies build their products on code that unpaid volunteers maintain, and sometimes one person looks after an entire project in spare hours.",
     "This restates the opening facts and omits the argument: that popularity increases the burden and that taking without contributing draws down someone else's effort.")],
   "The paragraph argues against the 'free natural resource' picture: unlike air, code needs upkeep, the upkeep grows with popularity, and a firm that only takes is consuming a stock others replenish. The correct answer keeps the rejected comparison, the reason and the conclusion.",
   "Choosing the popular software is healthier option because popularity is usually a sign of health, which is the very assumption the paragraph overturns.",
   "V02G-open-source-maintainers", "The correct answer must combine the rejected analogy, the counter-intuitive role of popularity and the conclusion; the narrow option is accurate as far as it goes.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 005
ps("V02-G-005", "Arts and literature", "An ending should be faithful to what the novel is about; openness is not a virtue in itself.", "Medium",
   "Readers who complain that a novel simply stops often assume that an ending exists to settle what the story has raised: who is guilty, who marries whom, whether the journey succeeds. Some endings do that, and do it well. But an ending can also be judged by whether it completes the shape of the book's attention. A novel that has spent three hundred pages showing how hard it is to know another person would contradict itself if its last chapter revealed everything; the unresolved close is then not a failure of nerve but the argument carried through. Openness is not a virtue in itself, and a writer who withholds an answer merely to seem profound has evaded rather than completed the work. The question is not whether an ending is closed but whether it is faithful to what the novel has been about.",
   "An ending should be judged by its fit with the novel's concerns; an unresolved close can complete a book's argument, but openness adopted merely for effect is evasion.",
   [("Open endings are artistically superior to tidy ones, since resolving every question that a story raises insults the intelligence of its serious readers.",
     "The paragraph says 'Openness is not a virtue in itself' and grants that some closed endings settle questions 'and do it well', so it ranks neither kind above the other."),
    ("Readers who complain about unresolved endings are usually right, because a novel that withholds its answers has generally failed to finish what its early chapters began.",
     "The paragraph rejects this complaint's assumption; it says an unresolved close can be 'the argument carried through' rather than a failure."),
    ("A novel about how difficult it is to know another person would contradict itself if its final chapter revealed everything about its characters' hidden inner lives and motives.",
     "This is the paragraph's example only; it omits the general criterion of faithfulness and the warning about openness used merely to seem profound.")],
   "The paragraph argues for a criterion: an ending is good if it is 'faithful to what the novel has been about'. It illustrates with a novel whose open close completes its theme, and it qualifies the point by denying that openness is good in itself. The correct answer carries the criterion, the illustration's lesson and the qualification.",
   "Reading the defence of one open ending as a general preference for open endings, and so picking the 'artistically superior' option.",
   "V02G-open-endings-novels", "The tempting distractor overgeneralises the example; only the qualification in the penultimate sentence rules it out.",
   cognitive="Analysis")

# ------------------------------------------------------------------ 006
ps("V02-G-006", "Arts and literature", "Strict poetic forms can prompt invention rather than cage it, though they do not guarantee good work.", "Easy",
   "A familiar view holds that strict poetic forms, with their fixed line counts and rhyme schemes, are cages that a free imagination must escape. Poets who have worked in such forms often describe the opposite experience. The need to find a rhyme or to fit a thought into a fixed number of syllables pushes them away from the first phrase that comes to mind, which is usually the most worn, and towards words and connections they would not otherwise have found. The constraint works less as a wall than as a prompt. This does not make every sonnet good; a form can be filled mechanically. But the assumption that freedom from rules is the natural condition of creativity mistakes the absence of resistance for the presence of invention.",
   "Strict forms are not simply cages: by blocking the first, most worn phrase they can push poets towards fresh language, though a form can still be filled mechanically.",
   [("Poets write better in strict traditional forms than in free verse, because rhyme and fixed syllable counts guarantee that their work avoids worn and predictable phrasing.",
     "The paragraph says 'This does not make every sonnet good; a form can be filled mechanically', so 'guarantee' overstates it, and it makes no comparison with free verse."),
    ("Fixed forms such as the sonnet restrict what poets can say, so a truly free imagination needs to set aside rhyme schemes and fixed line counts altogether.",
     "This is the 'familiar view' stated in the first sentence, which the rest of the paragraph argues against."),
    ("Poets who write in fixed forms often say that hunting for a rhyme leads them away from the first words that occur to them while they compose.",
     "This reports the poets' experience but leaves out the paragraph's point about creativity and its qualification that forms can be filled mechanically.")],
   "The paragraph criticises the view that forms are cages. It argues that constraint works 'as a prompt' against worn phrasing, concedes that a form can be filled mechanically, and concludes that freedom from rules is not the natural condition of creativity. The correct answer keeps the reversal and the concession.",
   "Picking the 'guarantee' option because it agrees with the paragraph's direction, without noticing that the concession rules out any guarantee.",
   "V02G-poetic-form-constraints", "The view under attack is labelled 'A familiar view', and the concession is explicit.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 007
ps("V02-G-007", "Arts and literature", "Intention-based and reader-based accounts of meaning each explain one feature of interpretation; a sound view needs both.", "Difficult",
   "One school of critics holds that a poem means what its author intended, and that interpretation is the patient reconstruction of that intention from the text and its circumstances. Another holds that once a work is published its meaning belongs to its readers, so that the author's own account is just one reading among many. Each position captures something the other cannot. The first explains why we can be wrong about a poem, as we are when we take an ironic line for a sincere one; the second explains why a work can say more than its author knew, as when a later age sees in an old novel a pattern its writer never noticed. What neither can do alone is account for both experiences, of being corrected by the text and of being surprised by it, and a defensible view of interpretation will have to make room for both.",
   "Intention-centred and reader-centred views of meaning each explain one real feature of reading, that we can misread and that works can exceed their authors, so an adequate theory must accommodate both.",
   [("The view that a poem means what its author intended is the better supported one, since only the author's intention can explain how a reader comes to misread an ironic line.",
     "The paragraph credits the intention view with explaining error but says 'Each position captures something the other cannot', so it does not declare either view better supported."),
    ("Since critics disagree so deeply about where meaning lies, no interpretation of a poem can be judged more correct than another, and every reading stands on equal terms.",
     "The paragraph treats 'being corrected by the text' as a real experience any defensible view must explain, which presupposes that some readings are wrong."),
    ("A satisfactory account of interpretation should divide the work between the two, treating intention as decisive for older works and readers' responses as decisive for recent ones.",
     "The paragraph asks for a view that makes room for both experiences; it never divides authority by the age of a work, and its own example of surprise involves an 'old novel'.")],
   "The paragraph compares two views and concludes that each explains something the other cannot: intention explains error, reader-centred meaning explains surplus meaning. It ends by requiring a view that makes room for both. The correct answer states this comparison and the conclusion without inventing how the combination would work.",
   "Choosing the divide by age compromise because it sounds like making room for both, although the paragraph proposes no such rule and its own example cuts against it.",
   "V02G-authorial-intention", "The compromise distractor mimics the conclusion's spirit, and rejecting it requires noticing that the 'old novel' example contradicts it.",
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 008
ps("V02-G-008", "Arts and literature", "Amateur choirs attract hesitant singers because choral singing asks for mutual listening and gives belonging.", "Easy",
   "Why do people who insist they cannot sing keep turning up, week after week, to rehearse with amateur choirs? Part of the answer lies in what choral singing asks of them. Unlike a solo performance, it does not demand that any one voice be remarkable; it demands that each voice listen to the others and adjust, breathing and entering together. The individual's weaknesses are absorbed into the sound of the group, while the group's sound depends on everyone's attention. Members describe the result less as a musical achievement than as a feeling of belonging that few other activities supply so directly. The music matters, but for many singers it is the occasion for the coordination, and the coordination is what they come back for.",
   "People unsure of their voices keep joining choirs because group singing asks for mutual listening rather than individual brilliance, and that coordination gives them belonging.",
   [("People join amateur choirs mainly to improve their singing voices, since regular rehearsal with others gradually turns weak singers into capable soloists.",
     "The paragraph says members value 'a feeling of belonging' more than 'a musical achievement' and says nothing about becoming soloists."),
    ("Choral singing is a more valuable musical activity than solo performance, because it requires every singer to listen carefully and adjust to the voices nearby.",
     "The paragraph contrasts what the two demand but never ranks their musical value; this adds a judgement it does not make."),
    ("In a choir the weaknesses of any individual singer are absorbed into the sound of the whole group, so that no single voice has to be remarkable.",
     "This is one step in the explanation and omits the answer the paragraph gives to its question: belonging produced by coordination.")],
   "The paragraph asks why hesitant singers keep coming and answers: choral singing asks for listening and adjustment rather than a remarkable voice, and the coordination yields belonging, which is what members return for. The correct answer gives the question's answer with both parts.",
   "Taking the 'weaknesses are absorbed' option because it is accurate, without checking whether it answers the paragraph's question.",
   "V02G-amateur-choirs", "The answer is spelled out in the last two sentences; distractors are clearly narrow or out of scope.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 009
ps("V02-G-009", "Language and media", "Borrowing does not erode a language; preferring native words is a matter of taste, not defence.", "Medium",
   "Campaigns to purify a language usually begin from the fear that borrowed words are a kind of erosion, each foreign term a small loss of the native stock. The fear misdescribes how languages grow. A borrowed word rarely displaces an existing one outright; more often it settles beside it and the two divide the territory, one taking a formal shade and the other an everyday one, so that the language ends up able to say more rather than less. Borrowing is also old: most languages that purists wish to protect were themselves assembled from earlier contacts. None of this means that every borrowing is welcome or that speakers cannot reasonably prefer a native coinage. It means that the decision is one of taste, not a defence against decay.",
   "Purists wrongly treat borrowing as erosion, since loanwords usually add distinctions beside native words and languages have always borrowed; preferring native words is legitimate, but only as taste.",
   [("Borrowed words enrich every language they enter, so efforts by speakers to prefer native coinages over foreign terms are misguided and ought to be abandoned.",
     "The paragraph concedes that not 'every borrowing is welcome' and that it does not mean speakers cannot 'reasonably prefer a native coinage', so it does not call such preferences misguided."),
    ("The languages that purists protect were themselves formed through earlier contacts, which shows that campaigns for purity misunderstand the history of the languages they defend.",
     "This is the supporting point about history only; it omits the main mechanism (loanwords add distinctions) and the concession that preference is a matter of taste."),
    ("When a foreign word enters a language it usually replaces a native word, but the loss is made good because the newcomer tends to carry a more formal shade of meaning.",
     "The paragraph says a borrowed word 'rarely displaces an existing one outright'; it settles beside it, so 'usually replaces' reverses the claim.")],
   "The paragraph critiques the purist fear of erosion with two reasons (borrowings add distinctions; languages were always assembled by borrowing) and then limits its own claim: preferring native words is reasonable, but it is taste rather than defence. The correct answer holds the critique, both reasons and the limit.",
   "Choosing the 'enrich every language' option and missing the concession in the last two sentences.",
   "V02G-loanwords-purism", "One distractor follows the argument but drops the concession; another reverses a single word ('rarely' to 'usually').",
   cognitive="Analysis")

# ------------------------------------------------------------------ 010
ps("V02-G-010", "Language and media", "Lower incivility under real names may be confounded and has hidden costs, so it does not settle anonymity.", "Difficult",
   "Comparisons of online discussions are often said to show that comment threads in which participants use their real names contain fewer insults than anonymous ones, and the point is regularly offered in support of ending anonymity. The inference moves too fast. Sites that require real names tend to differ from anonymous ones in other ways as well: they are often smaller, more closely moderated and frequented by people who already know one another, any of which could explain the gentler tone. Even where the effect is genuine, it is bought at a price that the comparison does not measure, since the people most likely to fall silent when they must identify themselves include those with the most to fear from speaking, such as an employee criticising an employer. Less abuse in the threads that remain is not the same as better discussion overall.",
   "Gentler named threads may owe their tone to other features of such sites, and even a real effect could silence vulnerable speakers, so the comparison alone does not justify ending anonymity.",
   [("Requiring real names does nothing to reduce abuse in online comment threads, since the gentler tone of named forums comes entirely from closer moderation and smaller size.",
     "The paragraph says other features 'could explain' the tone and then considers the case 'Even where the effect is genuine', so it does not assert that the effect is absent or wholly due to moderation."),
    ("Anonymity should be kept in online discussion because it protects vulnerable people such as employees criticising employers, and this benefit plainly outweighs any increase in abuse.",
     "The paragraph says the price 'the comparison does not measure', which means the balance is unknown; it argues that the case for ending anonymity is incomplete, not that the benefit plainly outweighs the abuse."),
    ("Real-name rules make online discussion less abusive, but because they also deter some people from posting, sites should use them only together with strict moderation.",
     "This treats the effect as established and adds a recommendation about moderation that the paragraph never makes; it uses moderation only as a possible confounder.")],
   "The paragraph critiques an inference from a reported comparison. It gives two objections: confounding (named sites differ in size, moderation and familiarity) and an unmeasured cost (vulnerable speakers fall silent). Its conclusion is limited: less abuse is not the same as better discussion, so the comparison does not settle the matter. The correct answer states both objections and the limited conclusion.",
   "Choosing the option that defends anonymity outright, because the paragraph clearly leans that way, and missing that it claims only that the cost is unmeasured.",
   "V02G-anonymous-comment-sections", "Two distractors each overstate one of the paragraph's two objections into a firm conclusion, and the correct answer must keep both hedges ('could explain', 'does not measure').",
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 011
ps("V02-G-011", "Language and media", "Equal airtime misleads when experts largely agree; fairness to evidence requires proportion.", "Medium",
   "Giving each side of a dispute equal time looks like the essence of fair reporting, and on questions where informed opinion is genuinely divided it is. But when nearly all of those who have studied a matter agree and a small minority dissents, presenting the two positions as evenly matched misinforms the audience about the very thing it most needs to know: where the weight of evidence lies. The audience leaves believing that experts are split when they are not. Fairness to persons, letting each view be heard, has been confused with fairness to the evidence, which requires that views be presented in proportion to their support. A report can include a dissenting voice and still be accurate, provided it does not pretend that the dissent is as strong as the consensus.",
   "Equal coverage suits disputes where informed opinion is truly divided, but under near consensus it misleads audiences about the evidence; dissent may be reported without being made to look equal.",
   [("Journalists should leave dissenting views out of their reports whenever most experts agree, since giving such views any airtime misleads the audience about the evidence.",
     "The last sentence says 'A report can include a dissenting voice and still be accurate', which this option contradicts."),
    ("Giving each side of a dispute equal time is the essence of fair reporting, because it lets every view be heard and leaves audiences free to weigh the evidence themselves.",
     "This is the appearance the first sentence describes and the rest of the paragraph rejects for cases of near consensus, where equal time 'misinforms the audience'."),
    ("Audiences often come away believing that experts are deeply divided on questions where nearly everyone who has studied the matter in fact agrees.",
     "This is the consequence the paragraph describes, but it omits the cause (equal time for unequal support) and the remedy of proportion that the paragraph argues for.")],
   "The paragraph argues that equal time is fair only when opinion is truly divided; under near consensus it misleads, because fairness to evidence requires proportion. It ends by allowing dissent to be reported if not inflated. The correct answer captures the condition, the harm and the allowance.",
   "Picking the leave dissent out option because it follows from the paragraph's direction, overlooking the explicit allowance in the final sentence.",
   "V02G-false-balance-reporting", "The correct answer's condition ('truly divided') and allowance (dissent reported) must both be checked against distractors that drop one of them.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 012
ps("V02-G-012", "Language and media", "Spelling reform weighs future learners' convenience against continuity with existing writing and varied speech.", "Easy",
   "Proposals to make English spelling match pronunciation have a strong case on one side and a stubborn obstacle on the other. In favour, a regular system would spare children years of memorising exceptions and would make reading easier to learn. Against it stands not mere habit but the sheer amount already written: every reform would make the existing stock of books, signs and records look strange to the next generation, and the more successful the reform, the more foreign the past would become. There is also the awkward question of whose pronunciation should be the standard, since speakers in different regions say the same words differently. The case for reform rests on the convenience of future learners; the case against rests on continuity with what has been written and the variety of present speech.",
   "Phonetic spelling would make reading easier for future learners, but it would estrange readers from existing writing and would require choosing one region's pronunciation as the standard.",
   [("English spelling should be reformed to match pronunciation, because the only real obstacle to such a change is the habit of adult readers who dislike unfamiliar forms.",
     "The paragraph says the obstacle is 'not mere habit but the sheer amount already written', and it also raises the problem of whose pronunciation to use."),
    ("Children learning English spend years memorising irregular spellings, which a regular system matching spelling to pronunciation would allow them to avoid.",
     "This gives only the case in favour and omits the two objections that make up most of the paragraph."),
    ("Spelling reform has repeatedly failed in English because speakers from different regions could never agree on one standard for how words are pronounced.",
     "The paragraph says nothing about past attempts failing; it mentions regional pronunciation as one difficulty a reform would face, not as the cause of a history of failure.")],
   "The paragraph compares the case for reform (easier learning) with the case against (estrangement from existing writing, and no neutral pronunciation to follow), summarising them in its last sentence. The correct answer gives both sides.",
   "Choosing the one-sided option about children because it is the first point the paragraph makes.",
   "V02G-spelling-reform", "The last sentence states both sides directly; distractors are one-sided, contradicted, or about history not discussed.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 013
ps("V02-G-013", "Education", "Recall beats rereading, but it strengthens learning only after understanding and cannot replace teaching.", "Easy",
   "Memory researchers have repeatedly found that trying to recall material, for example by answering questions on it, fixes it in memory better than reading it again for the same amount of time. Students tend to resist the finding because rereading feels productive: the text grows familiar, and familiarity feels like knowing. Recall, by contrast, is effortful and exposes gaps, which feels like failure. The finding has limits that its enthusiasts sometimes forget. Testing oneself helps most when the material has first been understood; quizzing a student on ideas that were never properly explained simply rehearses confusion. Recall is a way of strengthening learning, not a substitute for the teaching that makes something worth recalling.",
   "Recall fixes material in memory better than rereading, though it feels less productive, but it works best after understanding and cannot replace teaching.",
   [("Students should stop rereading their notes entirely and should quiz themselves on new topics before any explanation, since effortful recall always beats passive review.",
     "The paragraph warns that quizzing on ideas 'never properly explained simply rehearses confusion', so testing before explanation is exactly what it cautions against."),
    ("Students prefer rereading to testing themselves because the familiarity of a reread text feels like knowledge, while the effort of recalling it feels like failure.",
     "This explains the students' resistance only and omits both the finding's main claim and its limits."),
    ("Testing oneself improves memory only for students who already understand the material very well, so it is of little use to most learners in an ordinary classroom.",
     "The paragraph says self-testing 'helps most' after understanding, not 'only', and it says nothing about most learners lacking understanding.")],
   "The paragraph states a finding (recall beats rereading), explains why students resist it, and qualifies it: recall works best after understanding and is no substitute for teaching. The correct answer holds the finding, the resistance in brief and the qualification.",
   "Picking the 'only for students who already understand' option, which turns 'helps most' into 'only'.",
   "V02G-retrieval-practice", "Finding and limit are each stated in a single sentence; distractors are plainly extreme or narrow.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 014
ps("V02-G-014", "Education", "What a school does with ability groups matters more than whether it groups.", "Difficult",
   "Arguments over whether schools should group pupils by ability usually proceed as if the choice were between two outcomes: grouping helps able pupils and harms the rest, or mixing helps the rest at some cost to the able. Both sides assume that the group itself does the work. Yet much of what happens to a pupil placed in a lower group depends on what the school then does with that group: whether it is given the most experienced teachers or the least, a demanding curriculum or a diluted one, and whether pupils can move up when they improve. A lower set taught ambitiously and kept open differs more from a lower set treated as a holding pen than either does from a mixed class. Asking whether grouping works is therefore a less useful question than asking what it is used to do.",
   "Debates on ability grouping wrongly assume grouping itself decides outcomes, when the teaching, curriculum and mobility given to each group matter more, so its effects depend on its use.",
   [("Grouping by ability helps only when lower groups receive the most experienced teachers and a demanding curriculum, so schools unable to provide these should teach mixed classes.",
     "The paragraph lists conditions that shape outcomes, but it never makes them the sole condition of benefit or tells any school to adopt mixed classes."),
    ("Mixed-ability classes and ability groups yield broadly similar results for pupils, since what matters is the quality of teaching rather than the way classes are formed.",
     "The paragraph says outcomes within grouping vary widely, with two lower sets differing 'more' from each other than from a mixed class; that is a claim about variation, not that grouped and mixed classes produce similar results."),
    ("Ability grouping helps able pupils at the expense of the others, but schools can reduce the harm by letting pupils in lower groups move up as they improve.",
     "This adopts one side's framing, that 'the group itself does the work', which the paragraph rejects as an assumption shared by both sides.")],
   "The paragraph compares the two usual positions, finds a shared assumption (the group itself does the work), and replaces it: what the school does with the group matters more, as the comparison of two kinds of lower set shows. The correct answer states the rejected assumption, what matters instead and the conclusion.",
   "Choosing the 'broadly similar results' option because the paragraph downplays the grouping decision, without seeing that it stresses wide variation rather than equal results.",
   "V02G-ability-grouping", "The 'similar results' distractor sounds like the paragraph's deflation of the debate; separating it needs a precise reading of the lower-set comparison.",
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 015
ps("V02-G-015", "Education", "Teenagers' later body clocks make early starts harmful, but a later bell alone may not add sleep.", "Medium",
   "Sleep researchers broadly agree that during adolescence the body clock shifts later, so that teenagers who are sent to bed early often lie awake and then struggle to wake for an early start. This has led to calls for secondary schools to begin later in the morning, in the expectation that pupils will then sleep longer. The expectation is reasonable but less simple than it looks. A later start helps only if bedtimes do not drift later in step, and the gain can be eroded by evening screens or by family and transport timetables that a school cannot alter. The biological finding is sound; what it shows is that early starts work against teenagers, not that moving the bell alone will give them the sleep they lack.",
   "Teenagers' later body clocks make early school starts a real burden, but starting later will add sleep only if bedtimes and other evening pressures do not shift along with it.",
   [("Secondary schools should start later in the morning, because the shift in teenagers' body clocks means that a later bell will by itself give them the sleep they need.",
     "The last sentence says the finding does not show 'that moving the bell alone will give them the sleep they lack', which this option asserts."),
    ("The claim that teenagers' body clocks shift later is doubtful, because their shortage of sleep is better explained by evening screens and family timetables.",
     "The paragraph calls the biological finding 'sound'; screens and timetables are factors that can erode the benefit of a later start, not rival explanations of the finding."),
    ("Teenagers who are sent to bed early often lie awake and then find it difficult to get up in time for lessons that begin early in the morning.",
     "This restates the opening observation and omits the paragraph's point, which is the limit on what a later start can achieve.")],
   "The paragraph accepts a finding about adolescent body clocks and qualifies the policy drawn from it: a later start adds sleep only if bedtimes and evening pressures do not drift later too. The correct answer keeps the accepted finding and the condition.",
   "Choosing the option that doubts the finding, because the paragraph raises screens and timetables, while it explicitly calls the finding 'sound'.",
   "V02G-school-start-times", "The reader must separate doubt about the policy from doubt about the finding.",
   cognitive="Analysis")

# ------------------------------------------------------------------ 016
ps("V02-G-016", "Education", "Rubrics give consistency, but for original work they reward template-matching, which is not fairness.", "Medium",
   "Detailed marking rubrics are usually defended as a protection for students: they make expectations explicit, reduce the influence of a marker's mood and allow two examiners to reach the same grade. These are real gains, especially for routine tasks. The trouble begins when the same apparatus is applied to work whose value lies in doing something unexpected. A rubric can list only the qualities its authors anticipated, and a student who learns to satisfy each line, an introduction here, three examples there, is rewarded for matching the template rather than for thinking. An essay that takes an original route may score worse than a dutiful one because its strengths fall between the boxes. Consistency is worth having, but a scheme that is perfectly consistent about the wrong things is not fair; it is reliably unfair.",
   "Rubrics bring real clarity and consistency, but for original work they reward conformity to anticipated features and may penalise unexpected strengths, so consistency need not mean fairness.",
   [("Detailed rubrics should be abolished, because a marker's own judgement is always fairer than any fixed scheme that tries to list the qualities of good work in advance.",
     "The paragraph calls the rubric's benefits 'real gains, especially for routine tasks' and says 'Consistency is worth having', so it does not call for abolition or claim judgement is always fairer."),
    ("Rubrics protect students by making expectations explicit and by ensuring that two examiners who mark the same piece of work will arrive at the same grade.",
     "This is the defence the paragraph reports and accepts only in part; it omits the central objection about original work."),
    ("Rubrics are unreliable because markers read their criteria differently, so two examiners using the same scheme often give an original essay quite different grades.",
     "The paragraph grants that rubrics 'allow two examiners to reach the same grade'; its complaint is that they are consistent about the wrong things, not inconsistent.")],
   "The paragraph critiques the standard defence of rubrics. It accepts the gains, then argues that for original work a rubric rewards matching a template and can penalise unexpected strengths, concluding that consistency about the wrong things is 'reliably unfair'. The correct answer holds the concession, the objection and the conclusion.",
   "Choosing the 'unreliable' option, which confuses the paragraph's charge of misdirected consistency with a charge of inconsistency.",
   "V02G-grading-rubrics", "One distractor reverses the kind of fault (inconsistency instead of consistency about the wrong things), which needs careful reading.",
   cognitive="Analysis")

# ------------------------------------------------------------------ 017
ps("V02-G-017", "Education", "Handwritten notes help memory because slowness forces selection and rephrasing, which a typist can also do.", "Easy",
   "It is often observed that students who take notes by hand remember a lecture better than classmates who typed nearly every word. The explanation is not that pens are magical but that they are slow. Unable to keep up with the speaker, the student writing by hand must decide what matters, compress it and put it in their own words, and this selecting and rephrasing is itself a form of learning. The fast typist can record the lecture almost verbatim without having to think about it at all. The advantage, then, belongs to the mental work rather than to the instrument, and a typist who deliberately summarises instead of transcribing can recover much of it.",
   "Handwritten notes aid memory because slowness forces students to select and rephrase, and typists who summarise rather than transcribe can gain much of the same benefit.",
   [("Students should always take lecture notes by hand, because typing on a laptop prevents them from learning anything from the lectures that they attend.",
     "The paragraph says a typist who summarises 'can recover much of' the advantage, so typing does not prevent learning and handwriting is not required."),
    ("Typing students remember lectures poorly because the screen distracts them with messages and other material that has nothing to do with the speaker.",
     "The paragraph gives a different cause, verbatim recording without thought, and never mentions distraction by other material."),
    ("A typist can record a lecture almost word for word, whereas a student writing by hand cannot keep up with the speaker and has to leave things out.",
     "This describes the difference in speed but omits why it matters (selection and rephrasing are learning) and the point that typists can recover the advantage.")],
   "The paragraph explains why handwriting helps: its slowness forces the mental work of selection and rephrasing, and that work, not the pen, is the cause, so a summarising typist can recover much of the advantage. The correct answer gives the cause and the consequence.",
   "Choosing the always by hand option and overlooking the final clause about typists who summarise.",
   "V02G-handwritten-notes", "The cause and the qualification are stated directly in the last sentence.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 018
ps("V02-G-018", "Health and medicine", "Symptom checkers should be judged against realistic alternatives, not doctors.", "Medium",
   "Online symptom checkers are usually compared with doctors, and by that standard they look poor: they miss diagnoses a clinician would catch and raise alarming possibilities a clinician would dismiss. But for most people the realistic alternative to a symptom checker is not a consultation; it is a search engine, a relative's opinion or simply waiting. Against those alternatives, a tool that asks structured questions and advises when to seek care may do better, even if it diagnoses worse than a doctor. The relevant question is not whether such tools match professionals but whether they improve the decisions people would otherwise make, and in particular whether they send the right people to a clinic and reassure the right people to stay at home.",
   "Symptom checkers should be judged against what people would realistically do without them, not against doctors, so the test is whether they improve decisions about seeking care.",
   [("Online symptom checkers are unreliable tools, because they miss diagnoses that clinicians would catch and raise alarming possibilities that clinicians would quickly dismiss.",
     "This judges the tools by the comparison with doctors, which the paragraph describes in its first sentence and then sets aside as the wrong standard."),
    ("Symptom checkers are now accurate enough to replace a first consultation with a doctor for most people, provided that they ask structured questions.",
     "The paragraph concedes that such a tool 'diagnoses worse than a doctor'; its claim is about the realistic alternative, not replacing consultations."),
    ("People should use structured symptom checkers in place of search engines or a relative's advice, since such tools will always give them better guidance about when to seek care.",
     "The paragraph says such a tool 'may do better', which is a question to be tested, not a guarantee, and it gives no instruction to users.")],
   "The paragraph compares two standards for judging symptom checkers and argues for the realistic one: what people would otherwise do. Its conclusion is a test, whether the tools improve care-seeking decisions. The correct answer states the change of standard and the test.",
   "Choosing the always better guidance option because the paragraph favours the tools over search engines, overlooking that it says only 'may'.",
   "V02G-symptom-checkers", "The correct answer is a change of comparison; one distractor overstates 'may do better' into 'always', which needs a careful eye.",
   cognitive="Analysis")

# ------------------------------------------------------------------ 019
ps("V02-G-019", "Health and medicine", "A daily step target is an encouragement, not a threshold, and treating it as a pass mark discourages beginners.", "Easy",
   "A round daily target of steps has become, for many people, the definition of an active day, and falling short of it can feel like failure. The number is better treated as a convenient goal than as a threshold. Nothing happens to the body at the moment the counter reaches it; the benefits of walking appear to rise gradually with activity, and an inactive person who adds a modest amount of walking gains something real even if the target remains far off. Treating the figure as a pass mark can discourage exactly the people who stand to gain most, by making their improvement look like a shortfall. A target is useful as an encouragement and harmful only when it is mistaken for a line between health and its absence.",
   "A daily step target is a useful encouragement rather than a health threshold, since benefits rise gradually, and treating it as a pass mark can discourage those who would gain the most.",
   [("Daily step targets are harmful and should be abandoned, because they make people who fall short of them feel that they have failed to take enough exercise.",
     "The paragraph says a target 'is useful as an encouragement and harmful only when it is mistaken for a line', so it does not call for abandoning targets."),
    ("People who do not reach a daily step target gain no real health benefit from their walking, so the target marks the minimum level of useful activity.",
     "The paragraph says an inactive person who walks a little more 'gains something real even if the target remains far off', the opposite of this option."),
    ("The benefits of walking seem to rise gradually as activity increases, rather than appearing all at once when a step counter reaches a particular figure.",
     "This is the supporting reason only; it omits the paragraph's point about how targets should be treated and the harm of treating them as pass marks.")],
   "The paragraph critiques treating a step target as a threshold. Because benefits rise gradually, the target is best seen as encouragement, and a pass-mark reading discourages those who gain most. The correct answer keeps both the reframing and the harm.",
   "Choosing the abandon targets option because the paragraph lists a harm, missing the word 'only' in the last sentence.",
   "V02G-daily-step-targets", "The final sentence states the conclusion; distractors are extreme, reversed or narrow.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 020
ps("V02-G-020", "Health and medicine", "Warnings lose force because overuse makes them uninformative, so the fault lies with issuers.", "Medium",
   "Why do warnings that once alarmed people come to be ignored? The usual answer is that people grow careless, but the process is more reasonable than that. A warning that appears everywhere, on products that are mostly harmless as well as on ones that are genuinely dangerous, teaches its readers that it carries little information. Each false alarm lowers the value of the next, and a sensible person learns to discount the signal. The fault then lies less with the reader than with the issuers, who, wishing to cover every conceivable risk, spend the credibility that a warning needs in order to work. A label that warned about fewer things would protect people better, because they would have reason to believe it.",
   "Warnings lose force not through carelessness but because, placed on harmless and dangerous things alike, they carry little information; issuers who overuse them squander their credibility.",
   [("People ignore health warnings because familiarity breeds carelessness, so warnings must be redesigned regularly with fresh images and wording to keep catching attention.",
     "The paragraph rejects carelessness as 'The usual answer' and says the reader's response is 'more reasonable than that'; it proposes fewer warnings, not redesigned ones."),
    ("Warning labels should be removed from products altogether, since readers have learned that such labels carry little information and no longer pay any attention to them.",
     "The paragraph says 'A label that warned about fewer things would protect people better', so it wants warnings used sparingly, not removed."),
    ("Each false alarm lowers the value of the next warning, so a sensible reader slowly learns to discount the warnings that appear on many different products.",
     "This describes the reader's learning but omits the paragraph's main conclusion, that the fault lies with issuers who spend the credibility of warnings.")],
   "The paragraph explains a phenomenon: warnings are ignored because overuse makes them uninformative, so discounting them is reasonable and the fault lies with issuers. It ends by suggesting fewer warnings. The correct answer carries the rejected explanation, the real mechanism and where the fault lies.",
   "Picking the 'false alarm' option because it describes the mechanism accurately, while it leaves out the shift of blame to the issuers.",
   "V02G-warning-fatigue", "The narrow distractor is an accurate paraphrase of the mechanism; the correct answer must be chosen for including the conclusion.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 021
ps("V02-G-021", "Health and medicine", "The free-rider charge fits those who could be vaccinated, not those who cannot, whose need is why protection must be kept.", "Difficult",
   "When most of a community is vaccinated against a contagious disease, the few who are not are protected too, because the infection struggles to find a path to them. This makes refusal look costless to the refuser, and some ethicists describe the unvaccinated as free riders on the efforts of others. The label is apt for some and unjust to others. It fits a person who could safely be vaccinated and declines because others have made the risk small, since that person's safety is borrowed from neighbours who accepted the minor burden. It does not fit an infant too young for the vaccine or a patient whose treatment rules it out; for them, the protection of the crowd is not a free ride but the only protection available, and it is precisely the reason the rest of us have to keep it intact.",
   "The free-rider charge fits those who could safely be vaccinated but rely on others' immunity, not those medically unable to be, whose dependence on shared protection is why it must be maintained.",
   [("Everyone who stays unvaccinated in a well-vaccinated community is a free rider, since each of them benefits from protection created by neighbours who accepted the burden of vaccination.",
     "The paragraph says the label is 'apt for some and unjust to others' and excludes infants and patients who cannot be vaccinated, so 'everyone' contradicts it."),
    ("Since community immunity protects people who are not vaccinated, an individual's choice to decline a vaccine has little effect on others and remains a private matter.",
     "The paragraph says only that this 'makes refusal look costless', and it says those who decline borrow safety from neighbours; it ends by saying 'the rest of us have to keep it intact', which treats the matter as shared, not private."),
    ("Vaccination should be compulsory for everyone who can safely receive it, since those who decline borrow safety from others, including infants and patients who cannot be vaccinated.",
     "The paragraph judges when the free-rider label is fair and says the protection must be kept intact, but it proposes no means of doing so; compulsion is a policy it never mentions.")],
   "The paragraph takes a reported view (the unvaccinated are free riders) and draws a distinction: the label fits those who could safely be vaccinated and decline, but not those who cannot, for whom communal protection is the only protection and the reason it must be maintained. The correct answer states the distinction and the closing point; it adds no policy.",
   "Choosing the compulsion option because its reasoning echoes the paragraph, without noticing that it adds a specific policy the paragraph does not propose.",
   "V02G-herd-immunity-free-riding", "The compulsion distractor shares the correct answer's moral reasoning and must be rejected for adding a prescription; the 'everyone' option is the reported view.",
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 022
ps("V02-G-022", "Cities and geography", "A bypass hurts trade that served passing traffic but may help trade that depends on lingering; early losses mislead.", "Medium",
   "When a bypass takes through traffic away from a small town, shopkeepers on the old main road often predict ruin, and in the first months after it opens some of them do lose trade from passing motorists. Yet the longer story is frequently different. Freed from heavy lorries, the main street grows quieter and safer to walk along, and the visitors who now stop do so because they mean to, staying longer than the drivers who once paused for fuel. Businesses that served passing traffic, such as filling stations and roadside cafes, tend to suffer most, while those that depend on people lingering may gain. Whether a town is helped or harmed thus depends on which kind of trade it lived on, and the early losses are a poor guide to the eventual result.",
   "A bypass harms businesses that served passing motorists but may help those depending on visitors who linger in a quieter centre, so early losses poorly predict the outcome.",
   [("Building a bypass around a small town eventually improves trade for all the businesses on its old main road, once the early losses from passing motorists are recovered.",
     "The paragraph says businesses serving passing traffic 'tend to suffer most', so the gain is not shared by 'all' the businesses."),
    ("Shopkeepers are right to fear bypasses, since the trade lost from passing motorists in the first months after opening usually proves permanent for the town.",
     "The paragraph says 'the longer story is frequently different' and that 'the early losses are a poor guide to the eventual result', which this option contradicts."),
    ("Planners should build bypasses only around towns whose shops depend on lingering visitors, and should keep through traffic in towns that serve passing motorists.",
     "The paragraph explains who gains and who loses but makes no recommendation about where bypasses should be built.")],
   "The paragraph reports an early finding (some shops lose trade) and qualifies it: over time the effect splits by kind of business, so the result depends on the town's trade and early losses mislead. The correct answer states the split and the warning about early losses.",
   "Choosing the all businesses improve option because the paragraph's turn is optimistic, overlooking the businesses it says suffer most.",
   "V02G-bypass-roads-towns", "The 'all businesses' distractor shares the paragraph's optimism; the differentiation in the fourth sentence rules it out.",
   cognitive="Analysis")

# ------------------------------------------------------------------ 023
ps("V02-G-023", "Cities and geography", "Moving behind gates is reasonable for each household but corrosive for the shared city.", "Medium",
   "Residents who move into walled housing estates with guarded gates usually describe their decision as a private one: they want safety for their families and are willing to pay for it. Taken one by one, such decisions are understandable. Their sum is something none of the residents chose. As more households withdraw behind walls, the streets outside lose the people whose presence made them feel safe, the public parks and schools lose the residents best placed to demand that they be improved, and the city comes to be organised around the boundaries between enclaves rather than the spaces they once shared. The insecurity that drove people indoors grows in the areas they left. A choice can be reasonable for each household and still be corrosive for the city they share.",
   "Each household's move behind gates is understandable, but together such moves drain public streets and services and deepen insecurity outside, harming the city they share.",
   [("Families who move into gated estates are acting selfishly, since they choose their own safety while knowingly abandoning the parks and schools that others rely on.",
     "The paragraph calls such decisions 'understandable' and says their sum is 'something none of the residents chose', so it rejects both the charge of selfishness and 'knowingly'."),
    ("Gated housing estates make cities safer overall, because the residents they protect are no longer exposed to the dangers found on public streets and in parks.",
     "The paragraph says the insecurity 'grows in the areas they left', so the city as a whole is not made safer."),
    ("Governments should ban walled housing estates, because the security they offer their residents is outweighed by the damage they do to the surrounding streets.",
     "The paragraph diagnoses a collective harm but proposes no ban or any other policy.")],
   "The paragraph argues that individually reasonable choices add up to an unchosen collective harm: public streets, parks and schools decline and insecurity grows outside the walls. The correct answer keeps the individual reasonableness and the collective harm.",
   "Picking the 'selfish' option because the paragraph is critical of the result, missing that it explicitly calls each decision understandable.",
   "V02G-gated-housing-enclaves", "The correct answer turns on the contrast between individual reason and collective effect; the moralising distractor drops that contrast.",
   cognitive="Understanding")

# ------------------------------------------------------------------ 024
ps("V02-G-024", "Cities and geography", "Plans that see informal settlements as disorder erase the order they contain; improvement should start by learning it.", "Difficult",
   "City master plans often treat informal settlements as blank spaces awaiting proper development, marking them for clearance or for replacement by orderly blocks of housing. The view assumes that what is unplanned is unorganised. Settlements that grew without permission frequently contain dense networks of their own: workshops next to homes, credit circles, arrangements for sharing water and minding children, all of them fitted to the needs of people with little money and long working days. Clearing such a place and rehousing its residents in tidier flats on the city's edge can improve their buildings while destroying the arrangements that made their lives workable. This is not an argument for leaving dangerous housing alone. It is an argument that improvement should begin by learning what a settlement already does, since a plan that sees only the absence of order will fail to notice the order it erases.",
   "Plans that treat informal settlements as mere disorder can destroy the arrangements they contain, so improving unsafe housing should begin by understanding how a settlement already works.",
   [("Informal settlements are better organised than planned housing, so cities should leave them as they are rather than clearing them or rehousing their residents elsewhere.",
     "The paragraph says 'This is not an argument for leaving dangerous housing alone', and it never ranks informal settlements above planned housing."),
    ("Rehousing the residents of informal settlements in flats on the city's edge fails because the new buildings are usually of poorer quality than the homes they replace.",
     "The paragraph says rehousing 'can improve their buildings'; the loss it describes is of social and economic arrangements, not of building quality."),
    ("Informal settlements should be upgraded where they stand rather than cleared, since residents moved to the city's edge lose the workshops and credit circles near their homes.",
     "The paragraph asks that improvement 'begin by learning what a settlement already does'; it does not settle in advance that upgrading in place is the answer or rule out relocation.")],
   "The paragraph critiques the assumption that the unplanned is unorganised, shows the networks such settlements contain, concedes that dangerous housing must not be left alone, and concludes that improvement should start by learning how the place works. The correct answer holds the critique, the harm and the method-level conclusion.",
   "Choosing the upgrade in place option because it follows the paragraph's sympathies, though the paragraph prescribes a starting point (learning), not a specific outcome.",
   "V02G-informal-settlements-plans", "The upgrade distractor is a plausible policy consistent with the paragraph's tone; telling it apart requires noticing that the conclusion is about how to begin, not what to decide.",
   cognitive="Analysis", exams=DX)

# ------------------------------------------------------------------ 025
ps("V02-G-025", "Cities and geography", "Cities treat the night as disorder or as opportunity; each sees something real and either alone backfires.", "Easy",
   "Cities tend to think about their evenings in one of two ways. Some treat the hours after dark as a problem to be contained, a time of noise, drinking and disorder to be managed with closing times and police patrols. Others treat them as an opportunity, encouraging late markets, theatres and restaurants that bring life and employment to streets otherwise deserted after the offices close. Each view sees something real; the first notices the residents kept awake, the second the workers and visitors who depend on the night. A city that adopts only one tends to get its worst version: enforcement alone empties the streets and makes them less safe, while promotion alone pushes disorder onto the people who live nearby.",
   "Cities see the night as disorder to contain or opportunity to promote; each view captures something real, and relying on only one tends to backfire.",
   [("Cities should promote late markets, theatres and restaurants after dark, since bringing activity to the streets at night creates jobs and makes those streets safer.",
     "The paragraph warns that 'promotion alone pushes disorder onto the people who live nearby', so it does not endorse promotion as the answer."),
    ("Strict closing times and police patrols are the most effective way for a city to keep its streets safe and to protect residents from noise at night.",
     "The paragraph says 'enforcement alone empties the streets and makes them less safe', the opposite of this claim."),
    ("Some cities manage the hours after dark through closing times and police patrols, treating evening activity as noise, drinking and disorder to be contained.",
     "This describes only the first of the two approaches and leaves out the comparison and the warning against relying on either alone.")],
   "The paragraph compares two approaches to the night, grants that each sees something real, and warns that either alone produces its worst version. The correct answer gives both views, the concession and the warning.",
   "Choosing the promotion option because the paragraph describes it warmly, overlooking the last sentence.",
   "V02G-night-time-economy", "Both approaches and the warning are stated plainly; distractors are one-sided or narrow.",
   cognitive="Understanding")
