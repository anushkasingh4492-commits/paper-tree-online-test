import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

DIFF = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ooo("V03-J-001", "Education", "A longer pause after a classroom question changes who takes part.", "Easy",
    ["When teachers put a question to a class, most wait barely a second before calling on someone or answering it themselves.",
     "That brief pause rewards the quickest students and teaches the rest that thinking aloud is a race they cannot win.",
     "Teachers who deliberately stretch the silence to several seconds often find that more hands go up and that answers grow longer and more considered.",
     "The extra seconds cost almost nothing, yet they change who gets to take part in the lesson."],
    "Many schools now fit classrooms with projectors so that teachers can display their questions on a screen.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] form one argument about the pause after a question: teachers wait barely a second, 'That brief pause' favours the quickest students, a longer silence draws in more students, and the conclusion notes that 'The extra seconds' cost little but widen participation. Sentence [[X]] is about classroom equipment for displaying questions and says nothing about how long teachers wait, so it is the odd one out.",
    "Picking a sentence that reports an effect, such as sentence [[3]], instead of noticing that sentence [[X]] changes the subject from timing to technology.",
    "V03J-teacher-wait-time", "The odd sentence shifts from the timing of questions to classroom equipment, a change of focus that is easy to spot.",
    traps=[(2, "Sentence [[2]] can look like an aside, but it explains why the short wait in sentence [[1]] matters, and sentence [[3]] offers the remedy for the problem it names.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 002
ooo("V03-J-002", "Education", "Mixed-age classes force teaching to the individual child, a lesson for all schools.", "Medium",
    ["In a classroom that mixes children of different ages, the teacher cannot pretend that everyone has reached the same point in the syllabus.",
     "This apparent drawback forces a habit that single-age classes often neglect: planning work around what each child can actually do rather than what the year group is supposed to do.",
     "Older children, meanwhile, consolidate their own understanding when they explain a task to younger ones.",
     "The arrangement, long regarded as a compromise for small rural schools, therefore holds lessons even for schools with every resource to keep ages apart."],
    "Parents choosing a school often ask how many children sit in each class, though class size by itself may predict less about how much is learnt than they suppose.",
    "The four linked sentences argue that mixing ages is a hidden strength: sentence [[1]] states the condition, sentence [[2]] calls it an 'apparent drawback' that forces teaching to each child, sentence [[3]] adds a second benefit with 'meanwhile', and sentence [[4]] concludes with 'therefore' that all schools can learn from the arrangement. Sentence [[X]] uses classroom vocabulary but raises a different question, class size, and plays no part in the case for mixed ages.",
    "Choosing sentence [[3]] because it shifts from the teacher to the older pupils, without seeing that it supplies the second reason behind the 'therefore' of sentence [[4]].",
    "V03J-mixed-age-classrooms", "The odd sentence shares the school setting and sounds evaluative, so it must be rejected because it addresses class size, not age mixing.",
    traps=[(3, "Sentence [[3]] moves from the teacher to the older pupils, but 'meanwhile' marks it as a second advantage of the same arrangement, and sentence [[4]] draws its conclusion from both advantages."),
           (4, "Sentence [[4]] mentions rural schools and resources and may look like a new topic, yet its 'therefore' completes the argument by generalising the benefits just described.")])

# ------------------------------------------------------------------ 003
ooo("V03-J-003", "Education", "Stopping reading aloud once a child can read mistakes one aim of the practice for all of it.", "Difficult",
    ["Parents commonly stop reading aloud to their children once the children can read on their own, as if the purpose of the habit had been fulfilled.",
     "But for years after a child learns to decode print, the stories she can follow by ear remain far more complex than the ones she can manage on the page.",
     "Reading aloud is how she meets that richer vocabulary and syntax before her own reading has caught up with it.",
     "To stop at the moment of independent reading is thus to mistake one aim of the practice, teaching a child to read, for the whole of it."],
    "Children who are read to before they start school tend to arrive already knowing how books work, which way the pages turn and that print carries meaning.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] argue against stopping read-aloud sessions once a child reads independently: sentence [[1]] states the common practice, sentence [[2]] objects with 'But' that listening comprehension runs well ahead of reading, sentence [[3]] says reading aloud supplies 'that richer vocabulary and syntax', and sentence [[4]] concludes with 'thus'. Sentence [[X]] is about reading aloud too, but it describes the benefit before a child can read, which is the very aim the paragraph says is only part of the story; it supports nothing in the argument about older children.",
    "Keeping sentence [[X]] because it praises reading aloud, without noticing that the paragraph concerns the years after a child can already read.",
    "V03J-reading-aloud-to-children", "Every sentence praises reading aloud, so the odd one must be spotted by its stage of childhood and by the fact that it argues for the aim the paragraph treats as incomplete.",
    traps=[(1, "Sentence [[1]] reports a practice the author rejects and may seem detachable, but it is what 'But' in sentence [[2]] answers and what sentence [[4]] finally judges."),
           (3, "Sentence [[3]] may look like a restatement, yet 'that richer vocabulary and syntax' depends on sentence [[2]], and it supplies the purpose that sentence [[4]] says parents forget.")],
    exams=DIFF)

# ------------------------------------------------------------------ 004
ooo("V03-J-004", "Education", "Report-card comments written hurriedly at term's end turn into uninformative stock phrases.", "Medium",
    ["Written comments on report cards are meant to tell parents what a grade cannot: how a child works, where she struggles and what might help.",
     "In practice, teachers writing dozens of them at the end of term fall back on stock phrases such as 'works hard' or 'could participate more'.",
     "Parents soon learn to read such phrases as filler, and the comment ends up carrying even less information than the grade printed beside it.",
     "A few lines jotted down during the term, while a particular episode is still fresh, would often say more than a polished paragraph composed in a hurry at its end."],
    "Some schools have dropped letter grades altogether in favour of descriptive reports, arguing that a single letter conceals more than it reveals.",
    "The paragraph traces one problem and a remedy: sentence [[1]] states what comments are for, sentence [[2]] says that in practice they become stock phrases, sentence [[3]] shows parents discounting 'such phrases', and sentence [[4]] proposes notes written during the term. Sentence [[X]] shares the vocabulary of grades and reports but turns to a different debate, whether to abolish letter grades, which the paragraph never takes up.",
    "Rejecting sentence [[4]] because it moves from description to suggestion, when it answers the end-of-term haste described in sentence [[2]].",
    "V03J-report-card-comments", "The odd sentence uses the paragraph's own terms (grades, descriptive reports), so it must be rejected on its different question rather than its topic.",
    traps=[(4, "Sentence [[4]] can look like a change of direction, but its contrast between notes 'during the term' and a paragraph 'composed in a hurry at its end' answers the cause given in sentence [[2]].")])

# ------------------------------------------------------------------ 005
ooo("V03-J-005", "Health and medicine", "Iodising salt is a cheap remedy for iodine deficiency whose success depends on producers.", "Easy",
    ["Iodine deficiency was once common in inland and mountainous regions, where the soil and the food grown in it contain little of the element.",
     "Its effects range from goitre, a visible swelling of the thyroid gland, to impaired mental development in children whose mothers lacked iodine during pregnancy.",
     "Adding small amounts of iodine to table salt proved an unusually cheap remedy, because nearly everyone eats salt and in fairly steady quantities.",
     "The success of the measure has therefore depended less on medical sophistication than on persuading salt producers to iodise their product consistently."],
    "Doctors also advise people with high blood pressure to cut down on the amount of salt they eat.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] follow iodine deficiency from its cause (poor soils), to its effects, to the remedy of iodised salt and the condition for that remedy's success. Sentence [[X]] mentions salt but concerns blood pressure and eating less salt, a separate health issue that has no link to iodine.",
    "Being drawn by the shared word 'salt' and failing to notice that sentence [[X]] is about a different health problem.",
    "V03J-salt-iodisation", "The odd sentence shares only the word 'salt' and turns to an unrelated health concern, so it is quickly spotted.",
    traps=[(2, "Sentence [[2]] lists medical effects and might seem a detour, but it explains why the deficiency of sentence [[1]] needed the remedy offered in sentence [[3]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 006
ooo("V03-J-006", "Health and medicine", "Longer visiting hours can add observant relatives to a patient's care.", "Medium",
    ["Many hospitals long restricted visitors to short fixed hours, on the assumption that relatives tire patients and get in the way of the staff.",
     "Yet relatives often notice changes in a patient's mood or alertness that a busy nurse, seeing her for a few minutes at a time, can miss.",
     "They can also help with eating and offer reassurance, small tasks that stretched wards struggle to cover.",
     "Opening wards to families for longer periods need not, then, be a concession to sentiment; it can add a pair of observant hands to the care team."],
    "Visitors are usually asked to wash their hands on entering a ward, since they can carry infections in from outside.",
    "The paragraph challenges strict visiting hours: sentence [[1]] gives the old assumption, sentence [[2]] answers it with 'Yet', sentence [[3]] adds a second contribution relatives make ('also'), and sentence [[4]] concludes with 'then' that longer hours can strengthen care. Sentence [[X]] is about visitors and wards, but it gives an infection-control rule that neither supports the case for longer hours nor joins the chain of reasons.",
    "Taking sentence [[X]] as a natural concession because it mentions a risk visitors pose, although the paragraph's argument never turns to infection.",
    "V03J-hospital-visiting-hours", "The odd sentence shares 'visitors' and 'ward' and sounds like a relevant caution, so it is rejected on function rather than topic.",
    traps=[(3, "Sentence [[3]] can look like a list item that could be dropped, but 'also' ties it to sentence [[2]], and together they supply the 'pair of observant hands' that sentence [[4]] concludes with.")])

# ------------------------------------------------------------------ 007
ooo("V03-J-007", "Health and medicine", "A patient's online symptom search is better read as a disclosure of fear than as a rival diagnosis.", "Difficult",
    ["Doctors often complain that patients arrive having searched their symptoms online and convinced of some rare and frightening disease.",
     "The complaint treats the search as a rival diagnosis to be corrected, when it is more usefully read as a confession of what the patient fears.",
     "A patient who has spent a night reading about brain tumours is telling the doctor, indirectly, which possibility must be addressed before any reassurance can work.",
     "Brushing the printouts aside may save a few minutes, but it leaves that fear untouched, and the patient is likely to go home and search again."],
    "The quality of medical information online varies enormously, from pages written by specialists to forums where rumour passes for experience.",
    "The four linked sentences reinterpret the doctor's complaint: sentence [[1]] states it, sentence [[2]] says the search should be read not as a rival diagnosis but as 'a confession of what the patient fears', sentence [[3]] illustrates this with the night spent reading about tumours, and sentence [[4]] warns that dismissing the search leaves 'that fear' untouched. Sentence [[X]] is about online health information, but it judges how reliable that information is, which is exactly the 'rival diagnosis' framing the paragraph sets aside; nothing in the argument depends on it.",
    "Keeping sentence [[X]] because it seems to explain why patients arrive misinformed, when the paragraph's point is that the accuracy of the search matters less than what it reveals.",
    "V03J-online-symptom-searching", "The odd sentence is on the same subject and appears to support the complaint, so the reader must see that the argument deliberately moves away from questions of accuracy.",
    traps=[(4, "Sentence [[4]] can seem a practical aside, but 'that fear' refers back to sentences [[2]] and [[3]], and it states the cost of ignoring the paragraph's advice."),
           (1, "Sentence [[1]] states a view the author revises, yet 'The complaint' in sentence [[2]] needs it as its referent.")],
    exams=DIFF)

# ------------------------------------------------------------------ 008
ooo("V03-J-008", "Health and medicine", "Heat-sensitive labels on vials make invisible damage to vaccines visible.", "Easy",
    ["A vaccine that has been left in the sun or kept in a faulty refrigerator usually looks exactly like one that has been stored properly.",
     "For a health worker at a remote clinic, this creates a quiet dilemma: inject a dose that may be worthless, or discard one that may be perfectly good.",
     "Small heat-sensitive labels printed on vials, whose inner square darkens as heat exposure accumulates, were designed to settle exactly this uncertainty.",
     "By making invisible damage visible, such labels let workers trust the doses they give and stop throwing away good ones out of mere caution."],
    "Some vaccines are given as a single dose, whereas others must be repeated several times during the first years of a child's life.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] form one chain: heat damage to a vaccine cannot be seen, 'this' creates a dilemma for the health worker, heat-sensitive labels were made to settle 'this uncertainty', and 'such labels' make the damage visible. Sentence [[X]] is about how many doses a vaccine needs and has no connection with heat damage or the labels.",
    "Choosing sentence [[2]] because it narrows to one health worker, when it states the problem that the labels in sentence [[3]] were designed to solve.",
    "V03J-vaccine-vial-heat-labels", "The odd sentence concerns dosing schedules rather than storage damage, a change of focus that is clear once the chain is read.",
    traps=[(2, "Sentence [[2]] describes one worker's situation, but 'this' depends on sentence [[1]], and 'this uncertainty' in sentence [[3]] refers back to the dilemma it states.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 009
ooo("V03-J-009", "Cities and geography", "Shopkeepers who fear car-free town centres often end up defending them.", "Medium",
    ["When a city first proposes closing its old centre to cars, shopkeepers are usually the loudest opponents, fearing that customers who cannot park will not come.",
     "Their fear rests on the belief that their best customers arrive by car, a belief that tends to overestimate how many of them actually do.",
     "People on foot also visit more often and linger longer, even if each of them spends less on a single trip.",
     "Once the change has been made, the same shopkeepers are frequently among those most reluctant to see the traffic return."],
    "Planners in some cities have also experimented with car-free Sundays, when main roads are opened to cyclists and walkers for a single day.",
    "The paragraph follows shopkeepers' opposition to car-free centres: sentence [[1]] states the fear, sentence [[2]] says it rests on an overestimate, sentence [[3]] adds that walkers visit more often, and sentence [[4]] notes that 'the same shopkeepers' later resist reversing the change. Sentence [[X]] shares the car-free theme, but it describes a different, temporary measure and says nothing about shopkeepers or their customers.",
    "Accepting sentence [[X]] because 'car-free' and 'walkers' echo the paragraph, without checking that it joins the argument about shopkeepers.",
    "V03J-pedestrianised-town-centres", "The odd sentence shares the car-free vocabulary, so it has to be rejected because it introduces a separate policy rather than advancing the shopkeepers' story.",
    traps=[(3, "Sentence [[3]] may look like a stray fact about pedestrians, but it is the second reason the shopkeepers' fear is misplaced and prepares for their change of heart in sentence [[4]].")])

# ------------------------------------------------------------------ 010
ooo("V03-J-010", "Cities and geography", "Painting roofs white is a cheap way to cool homes, held back mainly by habit.", "Medium",
    ["On a summer afternoon a dark roof can become far hotter than the air around it, and much of that heat passes into the rooms below.",
     "Painting the roof white or another pale colour reflects a large share of the sunlight before it can be absorbed.",
     "For households in hot cities that cannot afford air conditioning, the result can be a noticeably cooler home at the cost of a few tins of paint.",
     "The measure is so cheap that its main obstacle is not money but the habit of assuming that cooling must come from a machine."],
    "Many traditional houses in hot regions were built with thick walls and small windows to keep out the midday sun.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] make one argument about roof colour: a dark roof heats the rooms below, a pale coat reflects sunlight, 'the result' is a cooler home for poor households, and 'The measure' is held back by habit rather than cost. Sentence [[X]] is about keeping houses cool in hot climates, but it describes traditional building design, not roof colour, and none of the other sentences refers to it.",
    "Rejecting sentence [[4]] because it moves from physics to attitudes, without noticing that 'The measure' and 'so cheap' sum up the case built in sentences [[2]] and [[3]].",
    "V03J-white-roofs-cooling", "The odd sentence shares the theme of passive cooling in hot places, so it must be rejected because it concerns building design rather than the roof-painting argument.",
    traps=[(4, "Sentence [[4]] shifts to habits of mind, but 'The measure' refers to the roof painting of sentence [[2]], and 'so cheap' picks up 'a few tins of paint' in sentence [[3]].")])

# ------------------------------------------------------------------ 011
ooo("V03-J-011", "Cities and geography", "The idle docks of port cities changed function rather than simply dying, with gains going to new users.", "Difficult",
    ["When cargo began to travel in standard containers, the old docks at the heart of many port cities fell idle, since the new ships needed deep water and vast stacking yards that cramped central harbours could not offer.",
     "The usual account of what followed is one of decline: lost jobs, empty warehouses, and neighbourhoods that had lived off the docks left without a purpose.",
     "Yet the same vacated land, central and facing the water, soon became some of the most valuable that these cities possessed.",
     "What looked like the death of the waterfront was in many cases a change in what it was for, though those who gained from the new uses were seldom those who had lost the old ones."],
    "Container ships have grown steadily larger over the decades, and each new generation has demanded still deeper channels and taller cranes.",
    "The four linked sentences reinterpret the fate of old harbour districts: sentence [[1]] explains why the central docks fell idle, sentence [[2]] gives 'The usual account' of decline, sentence [[3]] counters with 'Yet' that 'the same vacated land' became highly valuable, and sentence [[4]] concludes that the waterfront changed function, with a qualification about who gained. Sentence [[X]] shares the shipping vocabulary of sentence [[1]], but it follows the later growth of ships and ports, while the paragraph is about what became of the abandoned city waterfront; nothing after sentence [[1]] uses it.",
    "Keeping sentence [[X]] because it seems to elaborate the technical cause in sentence [[1]], although the argument is about the vacated land, not about shipping technology.",
    "V03J-port-city-waterfronts", "The odd sentence extends the opening sentence's technical point and uses its vocabulary, so the reader must see that the paragraph's subject is the fate of the old waterfront.",
    traps=[(2, "Sentence [[2]] presents a view the author goes on to revise, yet 'Yet' in sentence [[3]] answers it, and sentence [[4]] says what that decline 'looked like'."),
           (1, "Sentence [[1]] is the most technical of the four, but 'what followed' in sentence [[2]] and 'the same vacated land' in sentence [[3]] both depend on it.")],
    exams=DIFF)

# ------------------------------------------------------------------ 012
ooo("V03-J-012", "Cities and geography", "Suburbs whose residents commute away become places where people sleep but rarely meet.", "Easy",
    ["Some suburbs empty out each morning, as most of their working residents travel to jobs elsewhere in the city.",
     "During the day such places can feel almost deserted, with few shops open and little reason for anyone to walk the streets.",
     "In the evening the residents return, but tired from long journeys, many of them stay indoors rather than joining in local life.",
     "The result is a neighbourhood where people sleep but rarely meet, which is why such suburbs are sometimes called dormitory towns."],
    "Some cities have built cycle lanes alongside their main roads to encourage people to leave their cars at home.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] follow a commuter suburb through the day: it empties in the morning, 'such places' feel deserted by day, the residents return tired in the evening, and 'The result' explains the name 'dormitory towns'. Sentence [[X]] is about cycle lanes and car use, a transport policy that plays no part in this portrait of the suburb.",
    "Choosing sentence [[4]] because it introduces a name, when it is the conclusion that the morning, day and evening sentences build towards.",
    "V03J-dormitory-suburbs", "The odd sentence turns to transport policy, which is easy to separate from the description of the suburb's daily rhythm.",
    traps=[(2, "Sentence [[2]] could seem a minor detail, but 'such places' refers to the suburbs of sentence [[1]], and the deserted daytime is half of the picture summed up in sentence [[4]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 013
ooo("V03-J-013", "Philosophy and ethics", "Forgiving requires remembering a wrong, so forgetting it is not forgiveness.", "Difficult",
    ["The phrase 'forgive and forget' runs together two things that in fact pull in different directions.",
     "To forgive someone, one must keep the wrong clearly in view, since there is nothing to forgive in an injury one no longer recalls.",
     "What forgiveness gives up is not the memory but the resentment, the standing claim that the wrongdoer still owes something for what was done.",
     "Someone who has simply forgotten has therefore not forgiven at all; the wrong has merely faded, and nothing has been offered."],
    "Resentment that is nursed for years can harm the person who holds it as much as the one at whom it is aimed.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] build a conceptual distinction: sentence [[1]] says the phrase joins two opposed things, sentence [[2]] argues that forgiving needs memory, sentence [[3]] says that what is given up is resentment, not memory, and sentence [[4]] concludes with 'therefore' that forgetting is not forgiving. Sentence [[X]] shares the word 'resentment' with sentence [[3]], but it makes a practical claim about the harm of holding a grudge, which is a reason to forgive, not part of the argument about what forgiving is.",
    "Keeping sentence [[X]] because it seems to follow naturally from the mention of resentment in sentence [[3]], without noticing that the paragraph asks what forgiveness is, not why one should forgive.",
    "V03J-forgiveness-and-forgetting", "The odd sentence repeats the paragraph's key term and sounds like support, so the reader must separate a claim about consequences from an analysis of a concept.",
    traps=[(1, "Sentence [[1]] may look like a loose opening remark, but it states the thesis that sentences [[2]], [[3]] and [[4]] prove, and sentence [[4]] returns to its pairing of forgiving and forgetting."),
           (3, "Sentence [[3]] can seem a digression into resentment, yet it is what lets sentence [[4]] say that the forgetter has offered nothing: the resentment was never given up.")],
    exams=DIFF)

# ------------------------------------------------------------------ 014
ooo("V03-J-014", "Philosophy and ethics", "An offer to a desperate person may leave no real choice, but the wrong lies in the circumstances, not the offer.", "Difficult",
    ["It is commonly said that threats coerce and offers do not, because a threat narrows a person's options while an offer only adds to them.",
     "Yet an offer made to someone in desperate straits, such as a very low wage held out to a person with no other income, can be one she has no real freedom to refuse.",
     "Banning such offers, however, would not restore her freedom; it would simply remove the one option she had.",
     "The wrong in these cases may lie less in the offer itself than in the circumstances that make refusing it impossible, which suggests that the remedy, too, lies in changing those circumstances."],
    "Offers can also be manipulative when they exploit a weakness of will, as when a tempting reward is dangled before someone who is trying to break a habit.",
    "The paragraph develops one line of thought: sentence [[1]] states the common view, sentence [[2]] objects with 'Yet' that an offer to a desperate person may not be freely refusable, sentence [[3]] adds with 'however' that banning 'such offers' would not help, and sentence [[4]] concludes that the wrong lies in the circumstances. Sentence [[X]] also discusses wrongful offers, but it locates the wrong in the offerer's exploitation of a psychological weakness, a different kind of case that the paragraph never takes up and that cuts across its conclusion that the offer itself is not the problem.",
    "Keeping sentence [[X]] because it seems to extend the case against offers in sentence [[2]], without noticing that the paragraph's concern is desperate circumstances, not manipulation.",
    "V03J-coercive-offers-and-consent", "The odd sentence shares the paragraph's central idea (offers that wrong their recipients) and could follow the objection about desperate straits on the surface, so it must be rejected because it concerns a different source of wrong.",
    traps=[(3, "Sentence [[3]] seems to change direction with 'however', but 'such offers' refers back to sentence [[2]], and its point that a ban would only remove her option is what leads sentence [[4]] to place the remedy in the circumstances."),
           (1, "Sentence [[1]] gives a view the author qualifies, yet the 'Yet' of sentence [[2]] is a reply to it.")],
    exams=DIFF)

# ------------------------------------------------------------------ 015
ooo("V03-J-015", "Philosophy and ethics", "Imagined moral cases are artificial by design, like controlled experiments.", "Medium",
    ["Moral philosophers often test principles against imagined cases, such as a runaway trolley that can be diverted so that it kills one person instead of five.",
     "Critics object that such cases are so artificial that our reactions to them reveal little about how we ought to act in real life.",
     "But the artificiality is deliberate: by stripping away the uncertainties of real situations, the case isolates a single feature and asks whether it alone makes a moral difference.",
     "A thought experiment is in this respect like a laboratory experiment, which is no less informative for taking place under conditions that never arise outside the laboratory."],
    "Some imagined cases from moral philosophy have become so famous that they now turn up in films and popular television series.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] form a claim, objection and reply: imagined cases are used to test principles, critics call 'such cases' too artificial, 'But' the artificiality is deliberate, and the comparison with a laboratory experiment completes the defence. Sentence [[X]] mentions the same imagined cases, but it is about their fame in popular culture, which has no bearing on whether they are a sound method.",
    "Rejecting sentence [[4]] because it switches to science, without seeing that the laboratory comparison is the final step of the reply begun in sentence [[3]].",
    "V03J-thought-experiments-ethics", "The odd sentence shares the subject of imagined cases, so it has to be rejected because it does not take part in the argument about their value.",
    traps=[(4, "Sentence [[4]] moves to science, but 'in this respect' refers to the deliberate isolation described in sentence [[3]], and the comparison answers the critics of sentence [[2]].")])

# ------------------------------------------------------------------ 016
ooo("V03-J-016", "Philosophy and ethics", "Gratitude is genuinely owed, yet the benefactor is the one person who cannot demand it.", "Medium",
    ["We speak of owing gratitude to those who help us, as though it were a debt like any other.",
     "Yet a benefactor who demands thanks seems to cancel the very kindness that would have earned them.",
     "The oddity is that the debt is real, and an ungrateful recipient is rightly criticised, but the one person who cannot press for payment is the creditor.",
     "Gratitude may thus be best understood as owed to the benefactor without being owed on the benefactor's demand."],
    "Expressing gratitude regularly, for instance by writing down what one is thankful for each day, is often said to improve a person's mood.",
    "The paragraph works through a puzzle: sentence [[1]] treats gratitude as a debt, sentence [[2]] objects with 'Yet' that demanding it spoils the kindness, sentence [[3]] names 'The oddity' that the debt is real but the creditor cannot claim it, and sentence [[4]] resolves it with 'thus'. Sentence [[X]] is about gratitude too, but it concerns its psychological benefits for the grateful person, which has nothing to do with whether, or to whom, gratitude is owed.",
    "Being drawn by the shared word 'gratitude' and not seeing that sentence [[X]] turns from what is owed to what is beneficial.",
    "V03J-obligations-of-gratitude", "The odd sentence shares the topic and sounds positive about gratitude, so it must be rejected because it changes the question from obligation to well-being.",
    traps=[(3, "Sentence [[3]] can look like a repetition of sentence [[2]], but it adds that the debt is still real, the step that sentence [[4]] needs for its resolution.")])

# ------------------------------------------------------------------ 017
ooo("V03-J-017", "Psychology", "Capable people who feel like frauds are helped more by shared experience than by praise.", "Easy",
    ["Many people who are good at their work privately believe that their success is undeserved and that they will one day be found out.",
     "Such feelings are surprisingly common among high achievers, perhaps because each new success raises the standard they think they must meet.",
     "Praise does little to relieve them, since it is easily dismissed as the product of luck or of other people's kindness.",
     "For this reason, talking openly about the experience, and discovering how widely it is shared, often helps more than reassurance does."],
    "Job interviews often ask candidates to describe their greatest weakness, a question that many find difficult to answer.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] describe one experience and how to ease it: capable people feel like frauds, 'Such feelings' are common among high achievers, praise does not relieve 'them', and 'For this reason' sharing the experience helps more than reassurance. Sentence [[X]] is about a job-interview question and has no link to the feeling of being undeserving.",
    "Choosing sentence [[2]] because it offers a tentative explanation, when 'Such feelings' ties it to sentence [[1]] and the rising standard it mentions explains why praise fails in sentence [[3]].",
    "V03J-impostor-feelings", "The odd sentence concerns job interviews, a clearly different focus from the experience the other four sentences describe.",
    traps=[(3, "Sentence [[3]] can look detachable, but 'For this reason' in sentence [[4]] refers to its point that praise is dismissed.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 018
ooo("V03-J-018", "Psychology", "Owning something raises the value we place on it.", "Medium",
    ["People who are handed a simple object, such as a coffee mug, tend to ask a higher price to part with it than they would have paid to acquire it.",
     "Merely owning the thing, even for a few minutes, seems to raise its value in the owner's eyes.",
     "Sellers in many markets appear to know this, which is why they offer free trials: once a product is in the customer's home, giving it back feels like a loss.",
     "The effect suggests that the value we place on things depends not only on the things themselves but on whether we already possess them."],
    "Shoppers also tend to buy more of a product when it is displayed at eye level, where it is easiest to notice.",
    "The four linked sentences describe one tendency: sentence [[1]] gives the observation about the mug, sentence [[2]] interprets it as ownership raising value, sentence [[3]] shows sellers exploiting 'this' through free trials, and sentence [[4]] states what 'The effect' implies about value. Sentence [[X]] shares the shopping vocabulary of sentence [[3]], but it describes a different influence on buying, the position of goods on a shelf, which has nothing to do with ownership.",
    "Rejecting sentence [[3]] because it turns from an experiment to commerce, although its free trials work only because of the ownership effect described in sentence [[2]].",
    "V03J-endowment-effect", "The odd sentence uses the language of shoppers and products, like the free-trial sentence, so it must be rejected because it names a different mechanism.",
    traps=[(3, "Sentence [[3]] moves to the world of sellers, but 'this' refers to the ownership effect of sentence [[2]], and the free trial works because giving the product back 'feels like a loss'.")])

# ------------------------------------------------------------------ 019
ooo("V03-J-019", "Psychology", "Memory of an unpleasant experience is shaped by its worst moment and its ending rather than its length.", "Easy",
    ["When people recall an unpleasant experience, such as a medical procedure, their judgement of it tends to depend heavily on its worst moment and on how it ended.",
     "The total length of the experience, by contrast, seems to matter surprisingly little to the memory.",
     "As a result, a procedure extended by a few milder minutes at the end can be remembered as less unpleasant than a shorter one that stopped at its worst point.",
     "What we remember of an experience, in other words, is not a faithful summary of what we actually lived through."],
    "Many hospitals now let patients choose music to listen to while they wait for treatment.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] explain one feature of memory: the worst moment and the ending dominate, length matters little 'by contrast', 'As a result' a longer procedure can be remembered as better, and 'in other words' memory is not a faithful summary. Sentence [[X]] mentions hospitals and patients, but it is about a comfort offered while waiting, not about how an experience is remembered.",
    "Choosing sentence [[4]] because it generalises beyond medicine, when 'in other words' marks it as the conclusion drawn from sentence [[3]].",
    "V03J-peak-end-memory", "The odd sentence shares only the hospital setting and is easily separated from the argument about memory.",
    traps=[(2, "Sentence [[2]] can look like a minor aside, but the claim that length matters little is what makes the surprising result in sentence [[3]] possible.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 020
ooo("V03-J-020", "Psychology", "Procrastination is a problem of managing mood more than of managing time.", "Medium",
    ["The habit of putting tasks off is commonly blamed on disorganisation, as though a sharper timetable would be enough to cure it.",
     "Yet those who delay a piece of work can usually say exactly how long it will take; what they shrink from is the discomfort it stirs up.",
     "Turning to something easier brings immediate relief, and that relief is what makes the habit so hard to break.",
     "On this view, procrastination is a way of handling feelings rather than a lapse in planning, so remedies that ignore emotion are likely to fail."],
    "Deadlines set by someone else are often met more reliably than the ones people set for themselves.",
    "The paragraph replaces one account with another: sentence [[1]] states the usual view, sentence [[2]] objects with 'Yet' that what is avoided is discomfort, not lost track of time, sentence [[3]] explains how 'that relief' keeps the habit going, and sentence [[4]] concludes 'On this view' that the problem is one of handling feelings. Sentence [[X]] uses the language of deadlines and scheduling, but it belongs to the time-management account that the paragraph sets aside, and none of the other sentences builds on it.",
    "Keeping sentence [[X]] because it is about putting things off, without noticing that it treats delay as a matter of deadlines, the view sentence [[2]] rejects.",
    "V03J-procrastination-mood-repair", "The odd sentence is on the same subject and sounds like practical advice, so it must be rejected because it belongs to the view the paragraph argues against.",
    traps=[(1, "Sentence [[1]] gives a view the author rejects, but it is what 'Yet' in sentence [[2]] answers and what sentence [[4]] finally replaces.")])

# ------------------------------------------------------------------ 021
ooo("V03-J-021", "Psychology", "Familiarity with using an object is mistaken for understanding how it works.", "Difficult",
    ["Most people feel confident that they understand how familiar devices work, such as a zip or a flush toilet.",
     "Asked to explain the mechanism step by step, however, many discover that their understanding was far thinner than they had believed.",
     "The confidence seems to come from long familiarity with using the object, which is easily mistaken for knowledge of how it works.",
     "The same confusion may be at work in public debate, where people often hold firm opinions about policies whose workings they could not explain if asked."],
    "Explaining a subject to someone else is also one of the most effective ways of learning it thoroughly.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] trace one illusion: people feel they understand familiar devices, attempting an explanation 'however' exposes how thin that understanding is, 'The confidence' is traced to familiarity with use, and 'The same confusion' is extended to opinions about policy. Sentence [[X]] shares the idea of explaining, but it praises explanation as a way of learning, a point about study technique that does not concern the gap between felt and real understanding.",
    "Keeping sentence [[X]] because it seems to follow from the step-by-step explanation in sentence [[2]], without seeing that in the paragraph explaining is a test that reveals an illusion, not a method of learning.",
    "V03J-illusion-of-explanatory-depth", "The odd sentence echoes the paragraph's key activity, explaining, so it must be rejected on function; the sentence extending the point to public debate also moves to a new domain and tempts as the odd one.",
    traps=[(4, "Sentence [[4]] moves from devices to public debate, but 'The same confusion' refers to the mistake described in sentence [[3]], so it extends the argument rather than leaving it."),
           (3, "Sentence [[3]] might look like an optional aside, yet without it 'The same confusion' in sentence [[4]] would have nothing to refer to.")],
    exams=DIFF)

# ------------------------------------------------------------------ 022
ooo("V03-J-022", "Society and culture", "Relaxed dress codes can make choosing clothes for work harder, not easier.", "Medium",
    ["Workplaces that relax their dress codes often expect the change to remove a source of anxiety for their staff.",
     "Instead, many employees find that the absence of a clear rule makes deciding what to wear harder rather than easier.",
     "A suit was a safe answer to the question of what to put on; 'smart casual' demands judgement, and the unwritten standards it hides can be harder to read than the old written ones.",
     "Freedom from a rule, it seems, does not always mean freedom from the pressure that the rule once absorbed."],
    "Some professions, such as medicine and aviation, keep uniforms partly so that the public can recognise at a glance who is responsible.",
    "The four linked sentences describe an unexpected result: sentence [[1]] gives the expectation, sentence [[2]] reports with 'Instead' that the change made choosing harder, sentence [[3]] explains why the old rule was easier, and sentence [[4]] draws the general lesson about 'Freedom from a rule'. Sentence [[X]] is about uniforms at work, but its point is that uniforms help the public identify staff, which has nothing to do with the anxiety of employees choosing clothes.",
    "Choosing sentence [[3]] because it compares old and new styles in detail, when it explains the difficulty reported in sentence [[2]].",
    "V03J-workplace-dress-codes", "The odd sentence shares the vocabulary of workplace clothing, so it must be rejected because it serves a different purpose (public recognition) rather than the employees' experience.",
    traps=[(3, "Sentence [[3]] can look like a detour into fashion, but it gives the reason behind sentence [[2]]: the old rule supplied 'a safe answer', and its absence leaves unwritten standards.")])

# ------------------------------------------------------------------ 023
ooo("V03-J-023", "Society and culture", "The shared family meal matters mainly for the conversation it makes possible.", "Easy",
    ["In many households, the evening meal is one of the few times when the whole family sits down together.",
     "Over the food, conversation drifts easily between the day's events, plans for the weekend and the small worries of each member.",
     "When everyone eats at different times, often in front of separate screens, these unplanned exchanges become rare.",
     "The shared meal, in other words, matters less for what is eaten than for the talk it makes possible."],
    "Supermarkets now sell a wide range of ready-made dishes that need only a few minutes in an oven.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] make one point about family meals: the evening meal gathers the family, conversation flows over it, 'these unplanned exchanges' vanish when people eat apart, and 'in other words' the meal matters for the talk. Sentence [[X]] is about convenience food sold in shops and says nothing about families eating together or talking.",
    "Choosing sentence [[3]] because it describes the opposite situation, when it is the contrast that supports the conclusion in sentence [[4]].",
    "V03J-shared-family-meals", "The odd sentence turns to shop-bought food, which is clearly separate from the point about conversation at the table.",
    traps=[(3, "Sentence [[3]] describes families eating apart, which can look like a change of topic, but 'these unplanned exchanges' refers to the talk of sentence [[2]], and their loss shows why the meal matters.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 024
ooo("V03-J-024", "Society and culture", "The interval in popular Indian films shapes their structure, so removing it weakens them.", "Medium",
    ["Popular Indian films have long been made with an interval in the middle, a pause during which audiences stretch, talk and buy snacks.",
     "Film-makers learnt to build their stories around this break, placing a dramatic turn just before it so that viewers return to their seats eager to know what follows.",
     "The interval thus shapes the structure of the film itself, dividing it into two halves with distinct rhythms.",
     "When such films are streamed without a break, that carefully placed turn can lose much of its force."],
    "Multiplex cinemas, with several small screens under one roof, have allowed halls to show a wider range of films to smaller audiences.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] follow the interval from custom to craft: films include a break, film-makers build 'this break' into the story, the interval 'thus' shapes the film's structure, and without it 'that carefully placed turn' weakens. Sentence [[X]] is about cinema halls, but it concerns how multiplexes changed what is screened, not the place of the interval in a film's construction.",
    "Choosing sentence [[4]] because it moves from cinema halls to streaming, when 'that carefully placed turn' links it to sentence [[2]] and it draws the consequence of the argument.",
    "V03J-intervals-in-indian-cinema", "The odd sentence shares the cinema setting, so it must be rejected because it concerns film exhibition rather than how the interval shapes a story.",
    traps=[(4, "Sentence [[4]] shifts to streaming, but 'that carefully placed turn' refers to the dramatic turn of sentence [[2]], so it completes the argument by showing what is lost without the break.")])

# ------------------------------------------------------------------ 025
ooo("V03-J-025", "Society and culture", "A potluck turns a dinner from one household's gift into a joint production with no debts.", "Difficult",
    ["A potluck, in which each guest brings a dish to share, looks at first like a simple way of spreading the cost of a dinner.",
     "Its deeper effect is on the relation between host and guest: since everyone has contributed, no one leaves owing a return invitation.",
     "The meal becomes a joint production rather than a gift from one household to the others.",
     "This is also why a potluck tolerates wildly uneven contributions, a lavish curry beside a packet of crisps, without embarrassment: what is being shared is participation, not an exact division of costs."],
    "Because guests cook without consulting one another, a potluck can easily end up with three rice dishes and no dessert.",
    "The paragraph moves from an apparent purpose to a deeper one: sentence [[1]] gives the cost-sharing view, sentence [[2]] says the 'deeper effect' is on the host-guest relation, sentence [[3]] restates it as a 'joint production', and sentence [[4]] uses that idea to explain why uneven contributions cause no embarrassment, returning to the 'division of costs' of sentence [[1]]. Sentence [[X]] is about potlucks too, but it describes a practical problem of coordination, which plays no part in the argument about obligation and participation.",
    "Keeping sentence [[X]] because it seems to belong with the mixed dishes of sentence [[4]], although sentence [[4]] concerns uneven generosity, not lack of planning.",
    "V03J-potluck-dinners", "The odd sentence is a lively detail on the same subject and sits naturally beside the mention of uneven contributions, so it must be rejected on function.",
    traps=[(3, "Sentence [[3]] can look like a mere restatement of sentence [[2]], but 'joint production' is the idea that 'This is also why' in sentence [[4]] relies on."),
           (1, "Sentence [[1]] gives a view the paragraph goes beyond, yet 'Its deeper effect' in sentence [[2]] needs it, and sentence [[4]] returns to its talk of costs.")],
    exams=DIFF)
