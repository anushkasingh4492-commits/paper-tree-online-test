import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ooo("V03-B-001", "Science and environment",
    "Street trees cool a city by shading surfaces and releasing water vapour, which is why cities plant them against heatwaves.", "Easy",
    ["Streets lined with mature trees can be several degrees cooler on a summer afternoon than bare streets a few blocks away.",
     "The leaves shade the pavement and the walls of buildings, which would otherwise absorb sunlight all day and give off the stored heat long after dark.",
     "Trees also draw water from the soil and release it through their leaves as vapour, a process that takes heat from the surrounding air.",
     "For this reason, many cities now treat tree planting as a cheap way of making heatwaves less dangerous for their residents."],
    "Autumn leaf fall creates a recurring task for municipal workers, who must keep gutters and drains clear through the wetter months.",
    "Sentence [[1]] states the cooling effect, sentences [[2]] and [[3]] give its two causes (shade, and evaporation, linked by 'also'), and sentence [[4]] draws the practical conclusion ('For this reason'). Sentence [[X]] mentions trees and city workers, but it is about maintenance in autumn and has nothing to do with how trees cool streets in summer.",
    "Picking a sentence about the mechanism because it sounds technical, instead of checking which sentence plays no part in the cooling argument.",
    "V03B-urban-tree-canopy",
    "The odd sentence moves to a different season and a different concern, so it is quickly spotted once the cooling theme is seen.",
    traps=[(3, "Sentence [[3]] may look like a separate botanical fact, but 'also' marks it as the second cause of the cooling stated in sentence [[1]], alongside the shade of sentence [[2]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 002
ooo("V03-B-002", "Technology",
    "Complex, frequently changed password rules backfire by encouraging predictable habits; long passphrases are a better approach.", "Easy",
    ["Many websites insist that a password contain a capital letter, a number and a symbol, and that it be changed every few months.",
     "Such requirements were intended to defeat attackers, yet in practice they push ordinary users towards exactly the habits an attacker can exploit.",
     "Asked to change their password every quarter, people make the smallest change allowed, so that one password becomes the same word with a new digit at the end.",
     "A better approach, many now argue, is to allow long and memorable passphrases and to require a change only when there is reason to think one has been exposed."],
    "Fingerprint and face recognition now let many people unlock their phones without typing anything at all.",
    "Sentence [[1]] describes the familiar password rules, sentence [[2]] says ('Such requirements') that they backfire, sentence [[3]] shows how, and sentence [[4]] proposes a better policy. Sentence [[X]] is about security technology too, but biometric unlocking has no connection to the argument about password rules and the habits they produce.",
    "Treating any sentence about digital security as part of the paragraph without asking whether it advances the argument about password rules.",
    "V03B-password-rules",
    "The odd sentence changes the subject from password policy to a different way of unlocking devices.",
    traps=[(4, "Sentence [[4]] might seem to introduce something new, but it is the remedy for the problem described in sentences [[2]] and [[3]], and it answers both rules of sentence [[1]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 003
ooo("V03-B-003", "Language and media",
    "Languages borrow words for new things through contact, and the borrowings gradually become native, making vocabulary a record of contact.", "Easy",
    ["When two languages come into close contact, words tend to pass from one to the other, usually for things the borrowing language had no word for.",
     "A new food, tool or institution often arrives together with its name, which speakers simply adopt rather than invent a fresh term of their own.",
     "Over time, such borrowed words are reshaped to fit the sounds and grammar of their new home, until few speakers recognise them as foreign.",
     "This is why the vocabulary of almost any language is, on close inspection, a record of the peoples its speakers have traded, fought and lived with."],
    "Children learning their first language usually understand many words long before they are able to say them.",
    "Sentence [[1]] introduces borrowing between languages in contact, sentence [[2]] explains how a thing brings its name with it, sentence [[3]] describes how 'such borrowed words' become naturalised, and sentence [[4]] draws the conclusion ('This is why'). Sentence [[X]] is about words, but it concerns how children acquire a first language, not how words move between languages.",
    "Choosing a sentence merely because it shares the word 'words' or 'language', without checking that it concerns borrowing.",
    "V03B-loanwords",
    "The odd sentence is about language acquisition, a different topic from borrowing, and is easy to reject.",
    traps=[(2, "Sentence [[2]] can look like a list of examples that might be dropped, but it explains why borrowing is 'usually for things the borrowing language had no word for', as sentence [[1]] claims.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 004
ooo("V03-B-004", "Education",
    "Young children gain little from heavy homework; reading, talk and play at home do more, and light tasks mainly build habits.", "Easy",
    ["Parents often assume that more homework in the early school years must mean more learning.",
     "Yet a seven-year-old who has spent six hours in class has limited capacity left for further formal practice in the evening.",
     "What young children gain most from at home is reading with an adult, conversation and play, which build vocabulary and curiosity without feeling like extra lessons.",
     "Short, light tasks may still be useful, but chiefly as a way of building the habit of working independently rather than as a source of new learning."],
    "Many schools now publish their weekly homework timetables online so that parents can see at a glance what has been set.",
    "Sentence [[1]] states the common assumption, sentence [[2]] challenges it ('Yet'), sentence [[3]] says what helps young children instead, and sentence [[4]] concedes a limited role for light homework. Sentence [[X]] mentions homework and parents, but it is about how schools communicate assignments, not about whether homework helps young children learn.",
    "Being drawn by the shared words 'homework' and 'parents' and missing that the paragraph argues about the value of homework.",
    "V03B-homework-young-children",
    "The odd sentence shares vocabulary but concerns administration, which is clear once the argument is followed.",
    traps=[(4, "Sentence [[4]] may look like a contradiction of the paragraph, but it is a qualification: light tasks are allowed a role, building habits, which keeps the main claim about learning intact.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 005
ooo("V03-B-005", "Health and medicine",
    "Surgical checklists prevent errors of forgetting and give junior staff a moment to speak, ensuring known steps are done.", "Easy",
    ["Many errors in operating theatres come not from a lack of skill but from small steps that are simply forgotten under pressure.",
     "A short checklist, read aloud before the first incision, asks the team to confirm the patient's identity, the procedure and the side of the body to be operated on.",
     "It also gives junior members of the team an accepted moment to speak up if something seems wrong.",
     "Its value therefore lies less in teaching anything new than in making sure that what everyone already knows is actually done, every time."],
    "Modern anaesthetics allow operations that would once have been unbearably painful to be performed on patients who feel nothing.",
    "Sentence [[1]] locates many surgical errors in forgotten steps, sentence [[2]] introduces the checklist as the answer, sentence [[3]] adds a second benefit ('It also'), and sentence [[4]] sums up its value ('therefore'). Sentence [[X]] is about surgery but concerns anaesthesia and pain, which has no bearing on checklists or the prevention of forgotten steps.",
    "Choosing a sentence that is about surgery in general without asking whether it connects to the checklist argument.",
    "V03B-surgical-checklists",
    "The odd sentence changes topic within surgery and is easy to spot.",
    traps=[(3, "Sentence [[3]] can seem to drift from forgotten steps to hierarchy, but 'It also' ties it to the checklist of sentence [[2]] as a second way it catches errors.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 006
ooo("V03-B-006", "Science and environment",
    "Pooled records from many volunteer birdwatchers let researchers track species changes that professionals alone could not.", "Easy",
    ["Counting birds across an entire country would be impossible for professional scientists working alone.",
     "Volunteer birdwatchers, however, are spread across almost every town and valley, and many keep careful notes of what they see.",
     "When thousands of such records are pooled, researchers can track how the range and numbers of species change from year to year.",
     "Individual counts may be imperfect, but errors scattered across many observers tend to cancel out, leaving a picture no single expert could have drawn."],
    "Some birds migrate thousands of kilometres each year, finding their way by the sun, the stars and the Earth's magnetic field.",
    "Sentence [[1]] states the problem of scale, sentence [[2]] offers the volunteers ('however'), sentence [[3]] shows what pooling 'such records' achieves, and sentence [[4]] answers the worry about accuracy. Sentence [[X]] is about birds, but it describes migration and navigation, which has nothing to do with how volunteer records are gathered and used.",
    "Selecting a sentence because it is about birds, without noticing that the paragraph is about a method of counting them.",
    "V03B-citizen-science-birds",
    "The odd sentence is about bird behaviour rather than the counting method, which is quickly seen.",
    traps=[(4, "Sentence [[4]] may look like an afterthought, but it meets the obvious objection to amateur data and completes the case made in sentences [[2]] and [[3]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 007
ooo("V03-B-007", "Arts and literature",
    "Publication in instalments shaped nineteenth-century novels, giving them cliffhangers and responsive, sprawling plots.", "Easy",
    ["Many nineteenth-century novels first reached readers not as books but in instalments, published weekly or monthly in magazines.",
     "This form of publication shaped the writing itself, since each instalment had to end in a way that would bring readers back for the next.",
     "Authors could also watch how the public responded and adjust a subplot or a character's fate while the story was still appearing.",
     "Some features we now associate with these long novels, their cliffhangers and sprawling casts, are thus partly a product of how they were sold."],
    "Many readers today prefer to listen to novels as audiobooks during their daily journey to work.",
    "Sentence [[1]] describes serial publication, sentence [[2]] says 'This form of publication' shaped the writing, sentence [[3]] adds a second effect ('also'), and sentence [[4]] concludes ('thus') that familiar features of these novels came from the way they were sold. Sentence [[X]] mentions novels and readers, but it is about present-day listening habits, not about how serial publication shaped nineteenth-century fiction.",
    "Choosing a sentence that is about novels in general without checking that it belongs to the nineteenth-century argument.",
    "V03B-serialised-novels",
    "The odd sentence shifts to the present and to a different medium, so it is easy to reject.",
    traps=[(3, "Sentence [[3]] may seem to be about readers rather than writing, but it shows another way the instalment form shaped the novels, which sentence [[4]] sums up.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 008
ooo("V03-B-008", "Language and media",
    "A visible corrections column strengthens trust in a newspaper by showing that it checks and admits its errors.", "Easy",
    ["A newspaper that prints corrections might seem to be advertising its own mistakes.",
     "In practice, a clearly marked corrections column can strengthen readers' trust rather than weaken it.",
     "It shows that the paper checks its work after publication and is willing to admit error in public, something an unreliable source would not do.",
     "The column thus turns an unavoidable fact of journalism, that reporters sometimes get things wrong, into evidence of the paper's honesty."],
    "Many newspapers have moved their crossword and puzzle pages online, where readers can check their answers instantly.",
    "Sentence [[1]] raises the apparent paradox, sentence [[2]] answers it ('In practice'), sentence [[3]] explains why ('It shows'), and sentence [[4]] concludes ('thus'). Sentence [[X]] is about newspapers and even about checking, but checking puzzle answers online has nothing to do with corrections and trust.",
    "Being drawn by the word 'check' in sentence [[X]] and treating it as linked to the paper checking its own work.",
    "V03B-newspaper-corrections",
    "The odd sentence shares a word with the paragraph but is plainly about a different feature of newspapers.",
    traps=[(1, "Sentence [[1]] states a view the paragraph rejects, but that is its job: it sets up the paradox that sentence [[2]] resolves.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 009
ooo("V03-B-009", "Science and environment",
    "Suppressing every forest fire let fuel accumulate and made fires fiercer, so some controlled burning must return.", "Medium",
    ["Foresters long judged their success by how quickly they could extinguish any blaze, however small or remote.",
     "In many dry woodlands, however, modest ground fires had once returned every few years, consuming fallen needles and brush while sparing the mature trunks.",
     "By ending these regular burns, the policy let dead matter accumulate over decades, so that the rare blaze which slipped past the crews met a forest primed to explode.",
     "The lesson many foresters now accept is that some burning must be reintroduced deliberately, under watch, if the destructive kind is to grow rarer."],
    "Modern firefighting crews can call on aircraft that drop thousands of litres of water or retardant on a blaze within minutes of its being reported.",
    "Sentence [[1]] describes the policy of total suppression, sentence [[2]] contrasts it ('however') with the earlier pattern of small ground fires, sentence [[3]] explains the consequence of 'ending these regular burns', and sentence [[4]] draws the lesson. Sentence [[X]] uses the vocabulary of fighting fires, but it describes the speed of modern suppression, which plays no part in an argument that suppression itself was the problem; it neither explains the build-up of fuel nor supports controlled burning.",
    "Taking sentence [[X]] as a natural follow-on to sentence [[1]] because both are about putting fires out, and missing that the paragraph is critical of that very aim.",
    "V03B-fire-suppression",
    "The odd sentence shares the topic and vocabulary of firefighting and must be rejected because it does not serve the paradox the paragraph develops.",
    traps=[(2, "Sentence [[2]] looks like a step back into history, but the old pattern of small fires is the premise without which the harm described in sentence [[3]] cannot be explained.")])

# ------------------------------------------------------------------ 010
ooo("V03-B-010", "Technology",
    "Predictive text nudges writers towards common phrasing, so a time-saving tool may quietly make writing more uniform.", "Medium",
    ["Predictive text offers each next word before we have typed it, and accepting the suggestion is almost always quicker than refusing it.",
     "Because the suggestions are drawn from what most people tend to write, they steer us gently towards the most common phrasing.",
     "Over thousands of messages, this small pressure may make our writing more uniform, smoothing away the odd word choices that once marked a personal style.",
     "The convenience is real, but it is worth noticing that a tool designed to save effort also, quietly, makes some sentences easier to write than others."],
    "Early predictive systems were often mocked for their errors, replacing perfectly ordinary words with absurd ones at the worst possible moment.",
    "Sentence [[1]] notes that accepting a suggestion is the easy path, sentence [[2]] says the suggestions favour common phrasing, sentence [[3]] traces the cumulative effect ('this small pressure'), and sentence [[4]] weighs convenience against that effect. Sentence [[X]] is about predictive text, but it concerns the tool getting words wrong, whereas the argument depends on its suggestions being plausible enough to accept; an error that people laugh at steers no one towards common phrasing.",
    "Accepting sentence [[X]] because it is about predictive text, without noticing that the paragraph is about the influence of good suggestions, not the failures of bad ones.",
    "V03B-predictive-text",
    "The odd sentence uses the paragraph's subject and terms; rejecting it requires seeing that it pulls against the mechanism the paragraph describes.",
    traps=[(4, "Sentence [[4]] may look like a vague summary that could be cut, but it ties the convenience of sentence [[1]] to the uniformity of sentence [[3]] and states the paragraph's point.")])

# ------------------------------------------------------------------ 011
ooo("V03-B-011", "Technology",
    "Designs that block repair end devices' lives early, so owners should have access to parts, manuals and tools.", "Medium",
    ["Many modern devices are built in ways that make even simple repairs difficult, with batteries glued in place and parts tied by software to a single serial number.",
     "Manufacturers defend these designs as necessary for thinness, safety or security, and some of those justifications have merit.",
     "But the effect is that a cracked screen or a tired battery often ends a device's life, since an authorised repair can cost nearly as much as a replacement.",
     "Advocates of a right to repair argue that owners should at least have access to parts, manuals and tools, so that the choice between fixing and discarding is genuinely theirs."],
    "Some manufacturers offer trade-in schemes, giving customers credit towards a new device when they hand in an old one that still works.",
    "Sentence [[1]] describes designs that hinder repair, sentence [[2]] reports the manufacturers' defence and concedes part of it, sentence [[3]] turns ('But') to the cost for owners, and sentence [[4]] presents the right-to-repair remedy. Sentence [[X]] mentions manufacturers and devices, but trade-in credit concerns replacing a working device, not the difficulty or cost of repairing a broken one, and no other sentence takes it up.",
    "Linking sentence [[X]] to the theme of replacement in sentence [[3]] and overlooking that the paragraph is about access to repair.",
    "V03B-right-to-repair",
    "The odd sentence shares the vocabulary of manufacturers and replacement and must be rejected because it does not connect to the repair argument.",
    traps=[(2, "Sentence [[2]] seems to argue the other side, but it is the concession that sentence [[3]] answers with 'But'; without it that turn has nothing to push against.")])

# ------------------------------------------------------------------ 012
ooo("V03-B-012", "Arts and literature",
    "In poetry sound and sense are bound together, so every translation must choose which loss to accept.", "Medium",
    ["A translator of prose can usually carry the meaning of a sentence across languages and let the music of the original go.",
     "In a poem, however, sound and sense are so tightly bound that keeping one often means losing the other.",
     "A literal version may preserve every image while sounding flat, whereas a version that recreates the rhyme and rhythm must change words, and sometimes images, to do it.",
     "Every translation of a poem is therefore a decision about which loss to accept, and two good translators may reasonably decide differently."],
    "Some readers learn a language mainly so that they can read a favourite poet without relying on anyone's translation.",
    "Sentence [[1]] sets up prose as the easier case, sentence [[2]] contrasts poetry ('however'), sentence [[3]] illustrates the dilemma with the literal and the musical version, and sentence [[4]] concludes ('therefore') that translation means choosing a loss. Sentence [[X]] is about poetry and translation, but it describes readers avoiding translation altogether, which contributes nothing to the account of the translator's dilemma.",
    "Treating sentence [[X]] as evidence for the paragraph's point, when the paragraph is about the choices a translator faces, not about readers' responses to translation.",
    "V03B-translating-poetry",
    "The odd sentence shares all the key nouns of the paragraph and is rejected only because it plays no role in the argument.",
    traps=[(1, "Sentence [[1]] is about prose and can look off-topic, but it sets up the contrast that the 'however' of sentence [[2]] depends on.")])

# ------------------------------------------------------------------ 013
ooo("V03-B-013", "Arts and literature",
    "Cleaning an old painting reveals colour but may remove intended glazes, so restoration is an irreversible bet on intent.", "Medium",
    ["Restorers of old paintings face a choice that has no neutral answer.",
     "Varnish darkens and yellows with age, and removing it can reveal colours far brighter than viewers had grown used to.",
     "Yet the same cleaning may strip away thin glazes the painter added on purpose, and once removed, they cannot be put back.",
     "To clean a painting is thus to bet on a view of what the artist intended, and to accept the risk that later generations will judge the bet mistaken."],
    "Paintings in many museums are now hung behind glass and lit at low levels to slow the fading of their pigments.",
    "Sentence [[1]] announces a choice with 'no neutral answer', sentence [[2]] gives the case for cleaning, sentence [[3]] gives the risk ('Yet the same cleaning'), and sentence [[4]] concludes ('thus') that cleaning is a bet. Sentence [[X]] is about conserving paintings and the loss of colour, but protecting pictures with glass and dim light involves no irreversible choice about the artist's intentions, so it does not belong to the dilemma being described.",
    "Being drawn by the shared theme of preserving colour and treating sentence [[X]] as another part of the restorer's work, rather than seeing that the paragraph is about one specific dilemma.",
    "V03B-restoring-paintings",
    "The odd sentence is on conservation and colour, the paragraph's own terrain, and is rejected on function.",
    traps=[(1, "Sentence [[1]] is brief and abstract, but it is the claim the rest of the paragraph proves; sentence [[4]] answers it by calling the choice a bet.")])

# ------------------------------------------------------------------ 014
ooo("V03-B-014", "Language and media",
    "Exaggerated headlines win clicks but teach readers to distrust the publication, losing the attention they were meant to win.", "Medium",
    ["A headline must persuade a reader to stop scrolling, and it has only a few words in which to do so.",
     "This pressure rewards phrasing that promises more than the story beneath it delivers, such as a question the article never answers or a hint of a revelation.",
     "Each such headline may win a click, but readers who feel misled time after time learn to discount the publication's headlines altogether.",
     "The short-term gain of an exaggerated headline is therefore paid for with the slower loss of the very attention it was meant to capture."],
    "Headlines in printed newspapers were once written by sub-editors, who also checked the facts of each article and trimmed it to fit the page.",
    "Sentence [[1]] states the pressure on a headline, sentence [[2]] says 'This pressure' rewards overpromising, sentence [[3]] traces the effect on readers, and sentence [[4]] concludes ('therefore') that the gain costs attention. Sentence [[X]] is about headlines, but it describes who wrote them in the era of print, a historical aside that does nothing for the argument about exaggeration and trust.",
    "Accepting sentence [[X]] because it discusses headlines and checking, without noticing that it shifts from the incentives of headlines to the history of who wrote them.",
    "V03B-headline-writing",
    "The odd sentence shares the key term and is close in theme; it must be rejected because it is a historical aside with no role in the argument.",
    traps=[(3, "Sentence [[3]] may look like a separate point about readers, but it supplies the cost that sentence [[4]] weighs against the click.")])

# ------------------------------------------------------------------ 015
ooo("V03-B-015", "Education",
    "When top grades are given to more students they carry less information, so inflation harms grades as a signal.", "Medium",
    ["When the average grade at a school or university drifts steadily upwards, it is tempting to conclude that students are simply learning more.",
     "But if the top grade is awarded to a growing share of students, it carries less information about any one of them.",
     "An employer or admissions officer who sees a transcript full of top marks can no longer tell the excellent student from the merely good one.",
     "The harm of inflation, then, lies less in the grades themselves than in their weakened usefulness as a signal to those who must read them."],
    "Some teachers prefer written comments to grades, arguing that a letter or a number tells a student little about how to improve.",
    "Sentence [[1]] gives the tempting reading of rising grades, sentence [[2]] objects ('But') that top grades lose information, sentence [[3]] illustrates the loss for employers and admissions officers, and sentence [[4]] concludes ('then') that the harm is to grades as a signal. Sentence [[X]] also discusses what grades tell people, but its concern is feedback to the student, not the sorting of students by outside readers, and it says nothing about inflation.",
    "Thinking that sentence [[X]] belongs because it too criticises the information grades carry, without noticing that the audience and the problem are different.",
    "V03B-grade-inflation",
    "The odd sentence shares the idea that grades carry limited information, so it must be separated by its audience and purpose.",
    traps=[(1, "Sentence [[1]] states a view the paragraph rejects, but it is needed: sentence [[2]] begins with 'But' and answers it.")])

# ------------------------------------------------------------------ 016
ooo("V03-B-016", "Education",
    "Explaining a topic to a classmate exposes and fills one's own gaps, so peer teaching is a method of learning in itself.", "Medium",
    ["Students who are asked to explain a topic to a classmate often find that they understood it less well than they had thought.",
     "Putting an idea into one's own words exposes the gaps that rereading a textbook allows one to skip over.",
     "In filling those gaps to answer the classmate's questions, the student who explains ends up learning as much as the one who listens, and sometimes more.",
     "This suggests that pairing students to teach one another is not merely a way of saving the teacher's time but a powerful method of learning in its own right."],
    "Many students also like to revise in pairs simply because studying with a friend makes long sessions feel less tedious.",
    "Sentence [[1]] reports the surprise of the explaining student, sentence [[2]] explains it (explanation exposes gaps), sentence [[3]] shows the gaps being filled ('those gaps'), and sentence [[4]] draws the conclusion ('This suggests'). Sentence [[X]] mentions students working in pairs, but its point is enjoyment and motivation, not the learning that comes from explaining, so it does not support the claim that peer teaching is a method of learning.",
    "Accepting sentence [[X]] because it mentions pairs of students, without noticing that it offers a different reason for pairing from the one the paragraph argues.",
    "V03B-learning-by-teaching",
    "The odd sentence shares the setting of paired study and even the word 'also', so it must be rejected on its function.",
    traps=[(2, "Sentence [[2]] can look like a general remark about textbooks, but it gives the mechanism for sentence [[1]], and 'those gaps' in sentence [[3]] refers back to it.")])

# ------------------------------------------------------------------ 017
ooo("V03-B-017", "Education",
    "Good multiple-choice questions depend on distractors drawn from real student errors, which makes them hard to write.", "Medium",
    ["A multiple-choice question is only as good as its wrong answers.",
     "If the incorrect options are obviously absurd, a student who knows very little can reach the right one by elimination.",
     "Well-made distractors are drawn instead from the mistakes students actually make, so that choosing one reveals a specific misunderstanding.",
     "Writing such options is the hardest part of setting the question, because it requires the examiner to know not only the subject but also the ways it is commonly misunderstood."],
    "Such tests are also cheap to administer, since machines can mark thousands of answer sheets quickly and consistently.",
    "Sentence [[1]] states the thesis about wrong answers, sentence [[2]] shows what happens when they are weak, sentence [[3]] says what good ones look like ('instead'), and sentence [[4]] explains why 'such options' are hard to write. Sentence [[X]] is about multiple-choice tests and is linked by 'also' as if it added a further point, but cheap machine marking has nothing to do with the quality of distractors, which is the paragraph's only subject.",
    "Treating sentence [[X]] as one more remark about multiple-choice tests, though the paragraph is about how the wrong options are designed and why that is hard.",
    "V03B-mcq-design",
    "The odd sentence shares the subject and uses 'also' to look like a continuation, so it must be rejected on function.",
    traps=[(1, "Sentence [[1]] is short and could seem like a slogan, but it is the claim sentences [[2]], [[3]] and [[4]] develop, and it is the only sentence that can open the paragraph.")])

# ------------------------------------------------------------------ 018
ooo("V03-B-018", "Health and medicine",
    "Because placebos produce real improvement, drugs are tested against identical dummies, ideally with patients and doctors unaware.", "Medium",
    ["Patients given a sugar pill often report feeling better, especially when the condition involves pain, nausea or fatigue.",
     "This is why a new drug cannot be judged simply by whether the people who take it improve.",
     "Instead, researchers compare it with an identical-looking dummy, so that any benefit beyond what the dummy provides can be credited to the drug itself.",
     "Ideally neither the patients nor the doctors know who received which, since a doctor's expectations can colour how symptoms are assessed."],
    "It has sometimes been suggested that, since placebos can relieve symptoms, doctors might prescribe them openly for minor complaints.",
    "Sentence [[1]] reports the placebo response, sentence [[2]] draws its consequence for testing ('This is why'), sentence [[3]] gives the method ('Instead'), and sentence [[4]] refines it, with 'who received which' pointing back to the drug and the dummy. Sentence [[X]] starts from the same fact about placebos but turns to whether doctors should use them as treatment, a question about clinical practice rather than about how drugs are tested.",
    "Accepting sentence [[X]] because it begins from the same observation as sentence [[1]], without noticing that it draws a different conclusion that the rest of the paragraph never uses.",
    "V03B-placebo-trials",
    "The odd sentence builds on the paragraph's opening fact, so it is rejected only by tracking what the paragraph does with that fact.",
    traps=[(4, "Sentence [[4]] may look like a technical extra, but it completes the method of sentence [[3]], and 'who received which' only makes sense after the drug and the dummy have been introduced.")])

# ------------------------------------------------------------------ 019
ooo("V03-B-019", "Health and medicine",
    "Prescribing antibiotics for viral infections is convenient for doctor and patient but breeds resistance that harms everyone later.", "Medium",
    ["A doctor faced with a patient who has a sore throat and a busy waiting room may find it easier to prescribe an antibiotic than to explain why one is not needed.",
     "Most such infections are viral and the drug will do nothing for them, but the patient leaves satisfied and the consultation ends quickly.",
     "Each unnecessary course, however, gives bacteria in the patient's body another chance to develop resistance.",
     "The cost of the doctor's convenient choice is thus borne not by the patient in the room but by everyone who later needs the drug to work."],
    "Penicillin was among the first antibiotics to be widely used, and its arrival transformed the treatment of infected wounds.",
    "Sentence [[1]] describes the doctor's temptation, sentence [[2]] explains why the prescription is useless yet convenient ('such infections'), sentence [[3]] names its hidden cost ('however'), and sentence [[4]] concludes ('thus') that others bear that cost. Sentence [[X]] is about antibiotics, but it looks back to their early success and has no place in an argument about present-day overprescription and resistance.",
    "Choosing a sentence about the mechanism of resistance as the odd one, instead of the historical sentence that the argument never needs.",
    "V03B-antibiotic-overprescription",
    "The odd sentence shares the drug and its vocabulary but belongs to a different time and purpose.",
    traps=[(3, "Sentence [[3]] moves from the consultation to bacteria, but it is the turn ('however') that gives the paragraph its point, and sentence [[4]] depends on it.")])

# ------------------------------------------------------------------ 020
ooo("V03-B-020", "Health and medicine",
    "Teenagers' body clocks shift later, so early school starts cut their sleep, and later starts are an adjustment, not an indulgence.", "Medium",
    ["In the teenage years the timing of sleepiness moves later in the evening, so that many adolescents are wide awake at an hour when their parents are ready for bed.",
     "An early school start does not reset this inner timing; it simply cuts short the sleep that would otherwise have continued into the morning.",
     "The tired students who result are often described as lazy, when they are in fact responding to a biological change they did not choose.",
     "Moving the start of the school day later is therefore less an indulgence than an adjustment of the timetable to the bodies it is meant to serve."],
    "A dark, quiet and cool bedroom is widely recommended as a way of falling asleep more easily at any age.",
    "Sentence [[1]] describes the later body clock of adolescence, sentence [[2]] shows that early starts cut sleep without changing 'this inner timing', sentence [[3]] corrects the charge of laziness, and sentence [[4]] concludes ('therefore') that later starts are justified. Sentence [[X]] is about sleep, but it is general advice on bedrooms for all ages, unconnected to the teenage body clock or to school timetables.",
    "Treating sentence [[X]] as part of the paragraph because it is about getting enough sleep, without noticing that the paragraph argues about school start times.",
    "V03B-school-start-times",
    "The odd sentence shares the vocabulary of sleep and must be rejected because it neither concerns adolescents nor bears on the timetable argument.",
    traps=[(3, "Sentence [[3]] may seem to be about attitudes rather than biology, but it is the step that turns the facts of sentences [[1]] and [[2]] into the case for the change in sentence [[4]].")])

# ------------------------------------------------------------------ 021
ooo("V03-B-021", "Science and environment",
    "A failed replication usually reflects ordinary weaknesses and is science correcting itself; the real danger is replications never attempted or published.", "Difficult",
    ["When a celebrated finding fails to replicate, the news is often reported as a scandal, as if the original researchers must have cheated.",
     "Most such failures, though, have duller causes: small samples, flexible choices in the analysis and a publishing system that rewards striking results over careful ones.",
     "Seen this way, a failed replication is not science breaking down but science doing what it claims to do, which is to test its own results.",
     "The real worry is the many replications that are never attempted, or never published when they fail, since the errors they would have exposed stay in the record unchallenged."],
    "Journals should therefore retract any paper whose central finding another laboratory has been unable to reproduce.",
    "Sentence [[1]] reports the common reaction that a failed replication means cheating, sentence [[2]] rejects it ('though') by naming ordinary causes, sentence [[3]] reframes failure as self-correction ('Seen this way'), and sentence [[4]] relocates the danger to replications that are never done or never published. Sentence [[X]] uses the paragraph's vocabulary and sounds like a conclusion, but it treats a failed replication as grounds for punishment, the very attitude sentences [[2]] and [[3]] argue against; if failure is often due to small samples and is a normal part of testing results, automatic retraction does not follow, and nothing in the paragraph supports it.",
    "Reading sentence [[X]] as the practical conclusion because it begins with 'therefore', without checking that it contradicts the paragraph's claim that failure is normal rather than shameful.",
    "V03B-replication-crisis",
    "The odd sentence shares the subject and is phrased as a conclusion; it is rejected only by seeing that it reverses the author's stance, while the final coherent sentence tempts because it seems to change the subject.",
    traps=[(4, "Sentence [[4]] seems to change the subject from failed replications to missing ones, but it completes the argument: if failure is how science corrects itself, the worst case is the correction that never happens."),
           (1, "Sentence [[1]] states a view the author rejects, but sentence [[2]] answers it with 'though' and needs it in place.")],
    exams=D)

# ------------------------------------------------------------------ 022
ooo("V03-B-022", "Arts and literature",
    "An unreliable narrator works only if the reader can detect the deception through clues the novelist plants, and the meaning lies in that gap.", "Difficult",
    ["A narrator who misleads us is useful to a novelist only if we can eventually see through the deception.",
     "The craft lies in letting small details slip past the narrator's account, a sum of money that does not add up or a remark by another character that the narrator laughs off.",
     "The attentive reader assembles these details into a second story running beneath the one being told, and it is in the gap between the two that the novel's meaning lives.",
     "Such books ask us to read against the grain of the voice we are given, and they teach that skill by rewarding it."],
    "Some critics hold that every first-person narrator is unreliable to a degree, since no one can report their own life without bias.",
    "Sentence [[1]] states the condition for a useful unreliable narrator, that the deception be detectable, sentence [[2]] explains how the novelist meets it with planted details, sentence [[3]] shows the reader assembling 'these details' into a second story, and sentence [[4]] generalises ('Such books') about the reading skill involved. Sentence [[X]] is about unreliable narrators, but it widens the term to cover every first-person voice and every kind of bias, whereas the paragraph concerns a deliberate device whose deceptions the author plants and the reader can uncover; the claim neither builds on the clues of sentence [[2]] nor leads to sentence [[3]], and it shifts attention from the novelist's craft to a general thesis about all self-report.",
    "Treating sentence [[X]] as a natural qualification of sentence [[1]] because both define unreliability, without noticing that it shifts from a crafted device to a general claim about all narrators.",
    "V03B-unreliable-narrator",
    "The odd sentence uses the paragraph's central concept and reads like a scholarly aside; it is rejected only by seeing that it changes the scope of the concept the argument depends on.",
    traps=[(4, "Sentence [[4]] is general and can look detachable, but 'Such books' refers to the novels just described, and it states what the planted clues of sentences [[2]] and [[3]] do to the reader."),
           (1, "Sentence [[1]] can look like a separate definition, but its condition, that we 'can eventually see through the deception', is what sentences [[2]] and [[3]] explain how a novelist satisfies.")],
    exams=D)

# ------------------------------------------------------------------ 023
ooo("V03-B-023", "Language and media",
    "The standard dialect's status is social, but it is still worth learning, best taught as an extra register rather than a correction.", "Difficult",
    ["Linguists have long held that no dialect is inherently more logical or correct than another; the variety called standard owes its status to the social standing of those who speak it.",
     "This does not make the standard useless to learn, since it remains the variety of examinations, official letters and most job interviews.",
     "The question is how it is taught: as a correction of the way a child's family speaks, or as an additional register to be used when the occasion calls for it.",
     "The first approach tells children that their home speech is a mistake; the second gives them the standard without asking them to give anything up."],
    "The standard variety, moreover, has a richer vocabulary and a more precise grammar, which is why it is preferred for formal writing.",
    "Sentence [[1]] establishes that the standard's prestige is social rather than linguistic, sentence [[2]] concedes that it is still worth learning ('This does not make'), sentence [[3]] poses the question of how to teach it, and sentence [[4]] compares the two approaches ('The first ... the second'). Sentence [[X]] is about the standard variety and seems to add a reason for learning it ('moreover'), but it claims the standard is linguistically superior, which contradicts sentence [[1]]; the paragraph explains the standard's use in formal settings by social convention, not by any richer grammar.",
    "Reading sentence [[X]] as a further reason alongside sentence [[2]], and missing that it denies the premise on which the whole paragraph rests.",
    "V03B-dialect-prestige",
    "The odd sentence shares the subject and is linked by 'moreover' as if it supported the concession that the standard is worth learning; rejecting it requires noticing that it contradicts the opening premise.",
    traps=[(2, "Sentence [[2]] can look like it undercuts sentence [[1]], but it is a concession that keeps the premise intact: the standard is useful for social reasons, not because it is better."),
           (4, "Sentence [[4]] may seem to repeat sentence [[3]], but it judges the two approaches that sentence [[3]] only names, and 'The first' and 'the second' depend on that order.")],
    exams=D)

# ------------------------------------------------------------------ 024
ooo("V03-B-024", "Health and medicine",
    "Screening that finds more cancers can mislead because some are harmless; the honest test is whether deaths from the disease fall.", "Difficult",
    ["A screening programme that finds more cancers can look like an unqualified success, since earlier detection is generally thought to save lives.",
     "But some of the tumours it detects would never have grown enough to cause symptoms, and the people carrying them would have died of something else, unaware of them.",
     "Treating these people brings the costs of surgery and anxiety with no benefit, yet each one is counted as a patient whose cancer was caught in time.",
     "The honest test of a screening programme is therefore not how many cancers it finds but whether fewer people in the screened population die of the disease."],
    "A programme can also fail when the people most at risk of the disease are the least likely to accept an invitation to be screened.",
    "Sentence [[1]] states the appearance of success, sentence [[2]] objects ('But') that some detected tumours are harmless, sentence [[3]] shows how 'these people' inflate the record of success, and sentence [[4]] concludes ('therefore') that deaths, not detections, are the right measure. Sentence [[X]] is about screening programmes and their failure, but its problem is low uptake among high-risk groups, which has nothing to do with harmless tumours being counted as successes and does not lead to the conclusion of sentence [[4]].",
    "Accepting sentence [[X]] because 'also fail' seems to add a second weakness of screening, without seeing that the paragraph develops one specific flaw in how success is measured.",
    "V03B-screening-overdiagnosis",
    "The odd sentence shares the topic and presents itself as an extra point with 'also'; it is rejected because it introduces a separate problem the conclusion does not address.",
    traps=[(3, "Sentence [[3]] can look like a second, separate harm, but its point is the counting ('each one is counted'), which is what sentence [[4]] corrects."),
           (1, "Sentence [[1]] expresses the view being questioned, but sentence [[2]] begins with 'But' and needs it, and sentence [[4]] answers its measure of success.")],
    exams=D)

# ------------------------------------------------------------------ 025
ooo("V03-B-025", "Technology",
    "Old standards persist not from ignorance but because each user rationally values compatibility with everyone else.", "Difficult",
    ["A file format or technical standard often survives long after better alternatives have appeared.",
     "The reason is rarely ignorance: each user knows that a superior format is worth little if the people they exchange files with cannot open it.",
     "The value of a standard lies largely in how many others already use it, so the incumbent's advantage grows with every new adopter.",
     "What looks from outside like collective stubbornness is therefore a reasonable response, by each user, to the choices of everyone else."],
    "Users cling to an old format mainly because they have not heard of the alternatives or do not understand what they offer.",
    "Sentence [[1]] states the puzzle, sentence [[2]] rejects ignorance as the reason and points to compatibility, sentence [[3]] generalises that value grows with the number of users, and sentence [[4]] concludes ('therefore') that persistence is individually reasonable. Sentence [[X]] uses the paragraph's terms, but it offers ignorance as the main reason for persistence, which sentence [[2]] explicitly denies and which would make the 'reasonable response' of sentence [[4]] false.",
    "Thinking that sentence [[X]] explains the puzzle of sentence [[1]], and so belongs straight after it, without noticing that the next sentence rules that explanation out.",
    "V03B-format-lock-in",
    "The odd sentence offers a plausible answer to the opening puzzle in the paragraph's own vocabulary; it is rejected because it contradicts the explanation the paragraph gives.",
    traps=[(2, "Sentence [[2]] may look like the sentence to drop, since it clashes with another, but without it sentence [[3]] has no specific claim to generalise and sentence [[4]] no reason for calling persistence reasonable."),
           (3, "Sentence [[3]] can look like a repetition of sentence [[2]], but it turns one user's reasoning into a general rule about network value, which explains why the old standard's advantage grows.")],
    exams=D)
