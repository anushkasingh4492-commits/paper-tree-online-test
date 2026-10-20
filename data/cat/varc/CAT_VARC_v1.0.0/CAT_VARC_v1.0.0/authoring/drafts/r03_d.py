import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

T = "Work, class and status"
DX = ("CAT", "XAT")

# =====================================================================================
# R03-D-01  Credential inflation (Easy)
# =====================================================================================
passage("R03-D-01", T,
    "Rising degree requirements for many jobs reflect a competition for position rather than a rise in the skill the work demands, and the costs fall hardest on those who cannot pay for extra years of study.",
    [
        "When a job that was once filled by school leavers begins to advertise for graduates, the usual explanation is that the work has become more demanding. Machines have taken over the routine tasks, the story goes, and what remains calls for the analytical habits that only a university can supply. There is something to this. Some occupations really have changed beyond recognition, and an office clerk today handles systems that would have baffled a clerk of fifty years ago. But the explanation is offered far more often than it is checked, and when one looks at what people in many of these jobs actually do, the change in the work is often modest beside the change in the paperwork required to get it.",
        "A more economical account treats the degree less as a certificate of skill than as a ticket in a queue. When few people held degrees, an employer who asked for one was selecting a small group who were, on average, more persistent and better connected than the rest. As degrees became common, the same requirement no longer separated anyone, and employers who wanted to keep selecting raised the bar again, asking for a master's where a bachelor's had once sufficed. Each employer is behaving sensibly; it is merely using the cheapest filter available. Yet the sum of these sensible choices resembles a crowd at a parade in which everyone stands on tiptoe: no one sees better than before, and everyone is more tired.",
        "The costs of this arrangement are not evenly spread. Students from families that can afford several years of fees and forgone earnings keep pace with the rising bar; those who cannot are shut out of work they could perfectly well perform. A requirement introduced in the name of competence thus ends up rewarding the capacity to pay for time. Meanwhile the graduates themselves often discover that much of what they studied is barely used in the job, and that what the employer valued was the signal rather than the substance.",
        "None of this is an argument against education, which has goods that no labour market can measure. It is an argument against confusing two things that the word 'qualification' runs together: what a person can do, and how long a person has been able to stay in school. Some employers have begun to test applicants directly on the tasks the job involves. Where this is done, an awkward question comes into view, namely whether the degree requirement it replaces was ever a guarantee of quality or merely a habit that nobody had thought to examine.",
    ],
    "Easy", "One clear thesis, a vivid analogy and a plainly signalled concession at the start and end; little abstraction.",
    "R03D-credential-inflation")

rcq("R03-D-01-1", "Structure / function", "Easy",
    "The image of a crowd at a parade in which 'everyone stands on tiptoe' (paragraph 2) serves to",
    "illustrate how choices that make sense for each employer combine into an outcome that helps nobody.",
    [("show that employers have quietly agreed among themselves to keep raising the qualifications they demand from applicants.",
      "Paragraph 2 says 'Each employer is behaving sensibly' on its own account; there is no agreement or collusion among employers anywhere in the passage."),
     ("suggest that graduates are worn out by the number of years they have spent studying.",
      "This reads 'more tired' literally; the image is about the collective result of everyone raising the bar, not about the fatigue of students."),
     ("demonstrate that a degree gives an individual employer no useful information about applicants.",
      "The passage says the degree is 'the cheapest filter available' and once selected a more persistent group, so it does carry some information; the image concerns the collective result.")],
    "The image follows directly on 'Each employer is behaving sensibly' and 'the sum of these sensible choices'. When everyone stands on tiptoe, each person's move makes sense, but 'no one sees better than before, and everyone is more tired': raising the bar for all buys no advantage for anyone and only adds cost.",
    "Taking the image literally, or reading collusion into what the passage presents as separate sensible choices.",
    "The sentence introducing the image states its point outright.", cognitive="Understanding")

rcq("R03-D-01-2", "Specific detail", "Easy",
    "According to the passage, when few people held degrees, an employer who asked for one",
    "was picking out a small group who tended, on average, to be more persistent and better connected.",
    [("was ensuring that new staff had already been thoroughly trained in the particular tasks that the job would require.",
      "Paragraph 2 explains the selection in terms of persistence and connections, not task training, and paragraph 3 says much of what graduates studied 'is barely used in the job'."),
     ("was deliberately excluding applicants whose families could not afford fees, since that was the intended purpose.",
      "Paragraph 3 describes exclusion as a result of the rising bar, a requirement 'introduced in the name of competence'; the passage never says exclusion was intended."),
     ("was asking for a master's degree in order to separate the strongest applicants from ordinary graduates.",
      "Asking for a master's is what employers did later, once degrees had become common; it does not describe the period when few people held degrees.")],
    "Paragraph 2: 'When few people held degrees, an employer who asked for one was selecting a small group who were, on average, more persistent and better connected than the rest.'",
    "Confusing the early stage with the later stage of the process, or reading intention into an effect.",
    "The answer sits in a single sentence of paragraph 2.", cognitive="Recall")

rcq("R03-D-01-3", "Inference", "Medium",
    "The author would most likely agree with which of the following?",
    "A rise in the education a job demands does not by itself show that the job has become harder.",
    [("Most jobs now advertised for graduates involve exactly the same tasks that they involved fifty years ago, despite the new paperwork.",
      "Paragraph 1 concedes that 'Some occupations really have changed beyond recognition' and says only that the change in many jobs is 'often modest', which is far weaker than saying most jobs are exactly the same."),
     ("Governments should prohibit employers from asking applicants for degrees unless the job needs specialist knowledge.",
      "The passage proposes no regulation; paragraph 4 mentions employers who test applicants directly, but as a development that raises a question, not as a law the author recommends."),
     ("The main value of a university education lies in the signal of persistence it sends to employers.",
      "Paragraph 4 says education 'has goods that no labour market can measure', so the author does not reduce its value to a labour-market signal.")],
    "Paragraph 1 says the explanation that work has become more demanding 'is offered far more often than it is checked', and paragraph 2 offers a rival account in which requirements rise because degrees stop separating applicants. So a rising requirement does not by itself show the work is harder.",
    "Turning the author's 'often modest' into 'no change at all', or crediting the author with a prescription.",
    "Needs the author's hedged position across paragraphs 1 and 2 and rejection of two plausible overstatements.", cognitive="Analysis")

rcq("R03-D-01-4", "Strengthen / weaken / assumption", "Medium",
    "Which of the following, if true, would most weaken the 'more economical account' given in paragraph 2?",
    "In a firm that began requiring degrees for clerks, graduates did the job's tasks markedly better, and the gap was traced to their coursework.",
    [("In a firm that began requiring degrees for its clerks, the new recruits came mostly from families able to pay for several years of study.",
      "This fits paragraph 3's claim that the rising bar rewards 'the capacity to pay for time'; it does nothing to show that the degree certifies skill."),
     ("Employers who dropped their degree requirements found that screening applicants by other means took them longer and cost them considerably more.",
      "This supports the account, which says the degree is 'the cheapest filter available' to each employer."),
     ("The proportion of school leavers going on to university kept rising in the years after the requirement became common.",
      "More people seeking degrees is what the queue account predicts, as each tries to keep a place in line; it does not challenge the account.")],
    "The account in paragraph 2 treats the degree 'less as a certificate of skill than as a ticket in a queue', valued for 'the signal rather than the substance' (paragraph 3). Evidence that graduates do the job better because of what they learned shows the degree certifying real skill, which cuts directly against the account.",
    "Choosing an option that is about degrees and access but is consistent with, or even supports, the signalling account.",
    "Requires identifying the core claim (signal, not skill) and seeing which option contradicts it rather than merely touching the topic.", cognitive="Analysis")

# =====================================================================================
# R03-D-02  History of the weekend (Easy)
# =====================================================================================
passage("R03-D-02", T,
    "The weekend was a negotiated compromise that traded irregular, self-chosen rest for guaranteed but standardised free time, which in turn changed leisure into something scheduled and sold.",
    [
        "We tend to think of the weekend as a natural feature of the calendar, as if two days of rest had always followed five of work. In fact the arrangement is fairly recent, and its history suggests that free time is not simply the absence of work but something that has to be made, defended and shaped. Before the factory, many artisans worked in bursts, labouring late into the night to finish an order and then taking a day or two off whenever it suited them; in parts of England the habit of stretching Sunday's rest into Monday was common enough to be given a mock saint's name, 'Saint Monday'.",
        "Factory production could not tolerate this irregularity. Machines were expensive and had to run whenever the hands were present, and an employer could not plan production around workers who might drift in on Tuesday, so the long struggle over hours was therefore also a struggle over the shape of time. Workers wanted fewer hours; employers wanted predictable ones. The compromise that eventually emerged, first a half-day on Saturday and later the whole of it, gave each side part of what it sought. Workers won rest that was guaranteed rather than snatched, and employers won a workforce that turned up, sober, on Monday morning.",
        "It would be wrong to see the outcome merely as a defeat dressed up as a victory. For most working people, guaranteed free time was a real gain, and it was won against resistance. But the weekend also changed what free time was. Leisure that had once been taken at the worker's discretion became a fixed block, the same for everyone, and a block that was the same for everyone could be sold to. Football matches, excursion trains and seaside resorts arranged themselves around Saturday afternoon and Sunday, and leisure came increasingly to mean something one went out and paid for at a scheduled time.",
        "The lesson is not that the old irregular rhythm was better; it was often tied to poverty, to insecurity and to binges of overwork that left people exhausted. It is that arguments about working hours are never only about quantity. When people today argue over flexible schedules or a four-day week, they are reopening a question that the industrial age settled in one particular way: not merely how much time should be free, but who decides when it falls and what it is for.",
    ],
    "Easy", "Chronological narrative with an explicit moral; the stance and its qualification are stated directly.",
    "R03D-history-of-the-weekend")

rcq("R03-D-02-1", "Meaning in context", "Easy",
    "In paragraph 3, the remark that 'a block that was the same for everyone could be sold to' most nearly means that",
    "free time falling at the same hours for everyone became a market that businesses could plan to serve.",
    [("employers could buy back their workers' Saturdays by offering them extra pay for working at the weekend.",
      "The passage never mentions overtime; the sentence that follows lists football matches, excursion trains and resorts, which sell leisure to workers rather than buy their time."),
     ("workers were now free to sell their weekend hours to whichever employer offered them the best terms.",
      "The sellers in paragraph 3 are leisure businesses, and what changes is that leisure becomes 'something one went out and paid for'; workers are the buyers, not the sellers."),
     ("leisure became so expensive that most working families could no longer afford to enjoy the free time they had won.",
      "The passage says leisure came to be paid for, not that it became unaffordable; it calls guaranteed free time 'a real gain' for most working people.")],
    "The phrase is explained by the next sentence: football matches, excursion trains and seaside resorts 'arranged themselves around Saturday afternoon and Sunday'. Because everyone was free at the same time, businesses could sell leisure to that shared block.",
    "Reading 'sold' as a sale of labour time rather than a sale of leisure to workers.",
    "The following sentence glosses the phrase directly.", cognitive="Understanding")

rcq("R03-D-02-2", "Specific detail", "Easy",
    "According to the passage, what did employers gain from the compromise that produced the weekend?",
    "Workers who could be relied upon to arrive, in a fit state, at the start of the week.",
    [("A longer total working week overall, since Saturday afternoons were exchanged for extra hours on the other weekdays.",
      "Paragraph 2 says workers 'wanted fewer hours' and gained guaranteed rest; nothing suggests hours were added elsewhere in exchange."),
     ("Lower wage bills, since workers accepted reduced pay in return for having all of Saturday free.",
      "Wages are never mentioned in the passage; the employers' gain is stated as predictability, not savings on pay."),
     ("Influence over how workers spent their Sundays, since leisure was now organised and supplied by employers themselves.",
      "Paragraph 3 says leisure was organised by football, trains and resorts, not by employers, and gives employers no control over Sundays.")],
    "Paragraph 2: 'employers won a workforce that turned up, sober, on Monday morning.' Employers had wanted predictable hours, and this is what the compromise gave them.",
    "Supplying a plausible economic gain (hours, wages) that the passage does not state.",
    "The answer is a single explicit sentence.", cognitive="Recall")

rcq("R03-D-02-3", "Author's tone / attitude", "Easy",
    "The author's attitude towards the weekend is best described as",
    "appreciative of what it won for workers, while noting how it reshaped the nature of leisure.",
    [("nostalgic, regarding the irregular rhythm of pre-factory work as a freer and healthier way of living.",
      "Paragraph 4 says plainly that 'The lesson is not that the old irregular rhythm was better', noting its ties to poverty and overwork."),
     ("dismissive, treating the weekend as a defeat for workers that was presented to them as a victory.",
      "Paragraph 3 opens by saying it would be 'wrong to see the outcome merely as a defeat dressed up as a victory'."),
     ("grateful, crediting factory owners with the generosity that first gave workers a Saturday free of labour.",
      "Paragraph 3 says free time 'was won against resistance', and paragraph 2 presents a struggle and a compromise, not employer generosity.")],
    "Paragraph 3 calls guaranteed free time 'a real gain' won against resistance, yet adds that 'the weekend also changed what free time was', turning it into a scheduled block that could be sold to. The attitude is appreciation with a critical observation.",
    "Picking up the critical note in paragraph 3 and overstating it into dismissal.",
    "Each wrong attitude is explicitly ruled out by a sentence in the passage.", cognitive="Understanding")

rcq("R03-D-02-4", "Application / analogy", "Medium",
    "Which of the following situations most closely parallels the change described in paragraphs 2 and 3?",
    "Musicians who rested whenever bookings dried up join an orchestra with a fixed August holiday, and travel firms begin selling August trips to its players.",
    [("A company abolishes its fixed holiday calendar and allows staff to take leave whenever they choose, provided that their work is done on time.",
      "This moves from fixed to discretionary time, the reverse of the passage's change from rest taken 'at the worker's discretion' to 'a fixed block'."),
     ("A town council turns a disused railway yard into a public park so that residents have somewhere to spend their free afternoons.",
      "This provides a place for leisure but changes neither who decides when free time falls nor its regularity, which is the heart of the passage's change."),
     ("Workers in a factory strike for higher wages and win a large raise, though their daily hours of work stay exactly as they were.",
      "This concerns pay alone, whereas the passage stresses that the struggle over hours was 'also a struggle over the shape of time'.")],
    "The passage describes two linked shifts: irregular, self-chosen rest becomes guaranteed rest fixed for everyone (paragraph 2), and that shared block becomes something businesses sell to (paragraph 3). The orchestra case reproduces both: guaranteed, standardised holiday replaces rest taken when bookings ran out, and a market forms around the fixed period.",
    "Choosing any case that involves leisure or workers' gains without both the standardisation of time and the market that forms around it.",
    "The analogy must match two linked features at once; each distractor matches one surface element only.", cognitive="Application")

# =====================================================================================
# R03-D-03  The invisible servant (Medium)
# =====================================================================================
passage("R03-D-03", T,
    "The concealment of domestic servants helped produce the appearance of effortless gentility, and the wish to receive service without meeting the server survives in the modern service economy despite real gains for workers.",
    [
        "In the large households of the nineteenth century, the best servant was the one who was least noticed. Grand houses were built with back staircases so that maids carrying coal or slops need never meet the family on the main stairs, and bells rang in a basement corridor so that a summons could be issued without anyone having to see who answered it. In some houses servants were expected to turn aside, even to face the wall, when a member of the family passed. It is tempting to read all this as snobbery, a taste for keeping inferiors out of sight, but snobbery explains less than it seems to. The invisibility of servants was not a by-product of the genteel household; it was one of the things the household was for.",
        "What a gentleman's house displayed, above all, was ease: meals that appeared, fires that were lit, linen that was clean, all without visible effort. The ease was manufactured by a great deal of labour, and the labour had to be hidden for the ease to be believed. A servant glimpsed scrubbing a step was a reminder that comfort had a cost and a source; a servant unseen allowed the family to experience comfort as a natural condition of their kind of life. In this sense the architecture of concealment did not merely reflect a social hierarchy but helped to produce one, by allowing one class to appear exempt from necessity.",
        "Large-scale domestic service of this kind has largely disappeared, and it is easy to assume that its logic went with it. Yet much of the modern service economy seems designed to recreate the same experience by other means. Food arrives at the door from a kitchen the customer never sees, carried by a courier who is a first name on a screen. Offices are cleaned at night, after the staff have gone home. Apps promise that groceries, laundry and repairs will simply happen, and their designers speak, revealingly, of removing friction, as though the friction in question were not, very often, the encounter with another person who is doing the work.",
        "The comparison must not be pressed too far. The modern courier or cleaner is not bound to a single household, keeps hours that end, and has legal protections that a Victorian scullery maid lacked; to call such workers servants is to erase real gains. But the aspiration that the old houses expressed in brick and bells, the wish to receive service without meeting the server, has proved remarkably durable. What has changed is less the wish than the means of satisfying it, and the means are now available to far more people than ever owned a back staircase.",
    ],
    "Medium", "The thesis turns on a functional claim (concealment produced hierarchy) and a qualified historical comparison; moderate abstraction.",
    "R03D-invisible-domestic-servants")

rcq("R03-D-03-1", "Structure / function", "Easy",
    "The back staircases and basement bells mentioned in paragraph 1 serve primarily as",
    "examples of how a house was laid out so that the work of servants went unseen.",
    [("evidence that nineteenth-century families valued privacy from one another as much as privacy from their servants.",
      "The passage says nothing about family members avoiding one another; the staircases kept maids from meeting 'the family', and the bells hid 'who answered'."),
     ("illustrations of the technical improvements that made large households cheaper and easier to run in that period.",
      "Cost and efficiency are never discussed; paragraph 1 presents these features as means of keeping servants out of sight."),
     ("proof that servants in large houses were treated more harshly than those employed in small households.",
      "The passage makes no comparison between large and small households, and it treats the features as concealment rather than harshness.")],
    "Paragraph 1 introduces the staircases and bells right after saying that 'the best servant was the one who was least noticed'; the staircases mean maids 'need never meet the family', and the bells let a summons be answered without anyone seeing 'who answered it'.",
    "Inferring a purpose (efficiency, privacy) that the surrounding sentences do not give.",
    "The function is fixed by the topic sentence of paragraph 1.", cognitive="Understanding")

rcq("R03-D-03-2", "Inference", "Medium",
    "The author describes app designers' talk of 'removing friction' (paragraph 3) as revealing because the phrase",
    "treats as a nuisance what is often simply the customer's meeting with the person doing the work.",
    [("shows that app designers have consciously modelled their services on the households of the nineteenth century.",
      "The author claims a durable wish, not conscious imitation; nothing suggests designers have the Victorian household in mind."),
     ("admits that delivery and cleaning apps make the work of couriers and cleaners physically harder than it used to be.",
      "Workers' physical burden is not discussed; 'friction' in the passage refers to the encounter between customer and worker."),
     ("suggests that technical faults in apps are now the main obstacle standing between customers and good service.",
      "This takes 'friction' as a technical glitch; the author's 'as though' clause says the friction is, very often, a human encounter.")],
    "The sentence says designers speak of removing friction 'as though the friction in question were not, very often, the encounter with another person who is doing the work'. The phrase is revealing because it recasts contact with the worker as an inconvenience, echoing the old wish 'to receive service without meeting the server' (paragraph 4).",
    "Reading the author's point as a claim about designers' intentions or about technical faults.",
    "The meaning lies in an 'as though' clause that must be connected to the thesis in paragraph 4.", cognitive="Analysis")

rcq("R03-D-03-3", "Except / not supported", "Medium",
    "Each of the following is supported by the passage EXCEPT:",
    "Couriers and cleaners today work under essentially the same conditions as Victorian servants, though under a different name.",
    [("Comfort that seems to require no effort can depend on a great deal of labour deliberately kept from view.",
      "Supported: paragraph 2 says 'The ease was manufactured by a great deal of labour, and the labour had to be hidden for the ease to be believed'."),
     ("The modern means of receiving service without seeing the worker reach many more people than the older means did.",
      "Supported: paragraph 4 says the means 'are now available to far more people than ever owned a back staircase'."),
     ("A wish to keep social inferiors out of sight does not fully explain why servants were made invisible.",
      "Supported: paragraph 1 says 'snobbery explains less than it seems to' and that invisibility was 'one of the things the household was for'.")],
    "Paragraph 4 warns that 'The comparison must not be pressed too far': modern workers are not bound to one household, keep hours that end and have legal protections a scullery maid lacked, so 'to call such workers servants is to erase real gains'. The claim of essentially the same conditions contradicts this.",
    "Taking the passage's comparison between old and new service as an identity claim, missing the qualification in paragraph 4.",
    "Three true statements are paraphrased from different paragraphs; the false one echoes the passage's own comparison.", cognitive="Analysis")

rcq("R03-D-03-4", "Main idea / primary purpose", "Difficult",
    "Which of the following best expresses the central argument of the passage?",
    "Hiding the labour behind comfort once helped a class seem exempt from necessity, and the wish behind that concealment outlives the old form of service.",
    [("Modern delivery and cleaning work amounts to a revival of domestic servitude, and its workers ought to be recognised openly as servants.",
      "Paragraph 4 says that calling such workers servants 'is to erase real gains'; the author draws a qualified parallel, not an identity."),
     ("Victorian families hid their servants out of snobbery, and apps have now made that same snobbery affordable for the middle classes.",
      "Paragraph 1 says 'snobbery explains less than it seems to'; the author's explanation is that concealment produced the appearance of ease and so produced hierarchy."),
     ("The disappearance of large-scale domestic service shows that the social hierarchy it once supported has also come to an end.",
      "Paragraph 3 says 'it is easy to assume that its logic went with it' and then argues the opposite, that the logic survives by other means.")],
    "Paragraph 2 argues that hiding labour let a class 'appear exempt from necessity', and paragraphs 3 and 4 argue that 'the wish to receive service without meeting the server' survives in new forms, even though modern workers have real gains. The correct answer holds both halves.",
    "Choosing the option that echoes the passage's comparison most strongly, or the familiar snobbery explanation the author sets aside.",
    "All distractors reuse the passage's own material; the key needs both the functional claim and the qualified comparison.", cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-D-04  Emotional labour (Medium)
# =====================================================================================
passage("R03-D-04", T,
    "The concept of emotional labour survives the objection that all work involves emotion, because it concerns who controls and profits from the display of feeling, not whether feeling is present.",
    [
        "The idea that some jobs require workers to manage their own feelings, and not merely their hands or their minds, has travelled a long way from its origins in the study of flight attendants and debt collectors. It now turns up in discussions of nursing, teaching, retail and call centres, and even of the unpaid work of keeping a family cheerful. This expansion has drawn a predictable objection: if every job involves some management of emotion, the critics say, then the concept marks out nothing in particular. A surgeon must stay calm, a lawyer must appear confident, and a builder who loses his temper with clients will not keep them; are these, too, emotional labourers?",
        "The objection is fair against the loose use of the term, but it misses what the original idea was pointing at. The distinction was never between jobs that involve feeling and jobs that do not. It was between feeling that a worker manages according to her own judgement and feeling whose display is specified, monitored and sold by someone else. The surgeon's calm serves the operation and is left to her; nobody scripts it. The call-centre agent, by contrast, may be told how often to use the customer's name, scored on the warmth of her voice, and disciplined for a sigh. The emotion is part of the product, and the employer, not the worker, sets its terms.",
        "Seen this way, the concept is narrower than its popular use suggests, but also sharper. It directs attention not to the presence of emotion at work but to its ownership, and it suggests where the cost of such work lies. Most people can smile at a stranger without harm; the difficulty arises when the smile must be produced on demand, for hours, regardless of how the worker is treated, and when failing to produce it is a disciplinary matter. One would expect work of this kind to produce a fatigue unlike ordinary tiredness, and perhaps an uncertainty about which friendly feelings are one's own.",
        "None of this implies that friendliness in service is a sham, or that customers who enjoy it are dupes. Many workers take pride in easing a stranger's day, and a scripted greeting can be delivered with real goodwill. The point is that goodwill freely given and goodwill required by contract are different things, even when they look identical from the other side of the counter, and a concept that cannot tell them apart has lost the very thing that made it worth having.",
    ],
    "Medium", "Objection and reply structure with a redefinition; the key distinction is abstract but illustrated by a clear contrast.",
    "R03D-emotional-labour-service-work")

rcq("R03-D-04-1", "Meaning in context", "Easy",
    "As used in paragraph 3, the 'ownership' of emotion at work refers to",
    "who sets the terms on which a worker's feelings are displayed, and for whose benefit.",
    [("whether the worker genuinely feels the warmth or calm that she shows to the people she serves.",
      "Paragraph 4 says a scripted greeting 'can be delivered with real goodwill', so sincerity is a separate matter from who controls the display."),
     ("the legal rights that a worker holds over the recordings her employer makes of her calls.",
      "This takes 'ownership' literally; the passage never discusses recordings or legal rights over them."),
     ("how much emotion a particular job demands in comparison with the emotional demands of other jobs.",
      "Paragraph 2 says the distinction 'was never between jobs that involve feeling and jobs that do not', and paragraph 3 contrasts ownership with mere presence.")],
    "Paragraph 3 contrasts 'the presence of emotion at work' with 'its ownership', picking up paragraph 2's distinction between feeling a worker manages 'according to her own judgement' and feeling whose display is 'specified, monitored and sold by someone else', where 'the employer, not the worker, sets its terms'.",
    "Equating ownership with sincerity, or with the amount of emotion involved.",
    "The term is defined by the preceding paragraph's contrast.", cognitive="Understanding")

rcq("R03-D-04-2", "Inference", "Medium",
    "On the author's account, the builder in paragraph 1 who keeps his temper with clients would most likely count as",
    "no emotional labourer in the strict sense, provided nobody else scripts or monitors how his courtesy is displayed.",
    [("an emotional labourer, because every job that requires the management of feeling falls within the concept.",
      "This is the critics' reductio, which the author answers: the distinction 'was never between jobs that involve feeling and jobs that do not'."),
     ("no emotional labourer, because the feelings of manual workers play no real part in how well they do their jobs.",
      "Paragraph 1 says a builder who loses his temper 'will not keep' his clients, so feeling clearly matters to his work; the author's criterion is control, not relevance."),
     ("an emotional labourer, because he would lose business and income if he failed to manage his feelings with clients.",
      "Losing clients shows only that emotion matters to his work; on the author's test what counts is whether someone else specifies and sells the display.")],
    "Paragraph 2 puts the line between feeling managed 'according to her own judgement' and feeling 'specified, monitored and sold by someone else'. The surgeon's calm 'is left to her; nobody scripts it'. The self-managing builder resembles the surgeon, so he falls outside the strict concept unless someone else controls his display.",
    "Accepting the critics' broad criterion, or treating the commercial consequences of emotion as the test.",
    "Requires applying the author's criterion to a case the critics raised, and separating it from the critics' criterion.", cognitive="Application")

rcq("R03-D-04-3", "Strengthen / weaken / assumption", "Medium",
    "Which of the following findings, if true, would most strengthen the author's suggestion in paragraph 3 about where the cost of emotional labour lies?",
    "In one chain of shops, staff whose greetings were scripted and scored were more exhausted than staff serving the same customers as they saw fit.",
    [("Workers whose jobs involve dealing with members of the public all day report more exhaustion than people who work largely on their own.",
      "This compares contact with solitude, not controlled display with self-managed display, so it cannot isolate the factor the author identifies."),
     ("Customers rate scripted greetings as noticeably less sincere than greetings that shop staff are free to phrase however they like.",
      "This concerns how customers perceive the greeting, whereas paragraph 3 is about the cost borne by the worker."),
     ("Surgeons report higher levels of stress at work than call-centre agents do, especially during long and difficult operations.",
      "Surgeons' stress arises from feeling that is 'left to her', so it says nothing about the cost of feeling produced on demand under supervision.")],
    "Paragraph 3 locates the cost not in smiling as such but in a smile that 'must be produced on demand' and whose absence is 'a disciplinary matter'. A comparison that holds the customers constant and varies only who controls the display isolates exactly that factor.",
    "Choosing a finding about emotion at work in general rather than about externally controlled display.",
    "Two distractors are on topic; only a controlled comparison tests the author's specific mechanism.", cognitive="Analysis")

rcq("R03-D-04-4", "Inference", "Difficult",
    "The author's reply to the critics in paragraph 2 implies that",
    "they are right about how the term is often used, but wrong to infer that the concept itself picks out nothing distinctive.",
    [("they are right that the concept is too broad, and that the remedy is to restrict it to occupations whose main task is serving customers.",
      "The author narrows the concept by the test of who controls the display, not by occupation; a customer-facing worker left to her own judgement would fall outside it."),
     ("they have shown that the concept should be dropped and replaced with a narrower term that names only scripted forms of feeling.",
      "The author keeps the concept and calls it 'narrower than its popular use suggests, but also sharper', so it is clarified rather than abandoned."),
     ("their examples of the surgeon and the lawyer reveal that professionals perform more emotional labour than call-centre agents.",
      "The author uses the surgeon to show feeling that 'nobody scripts', the opposite of the agent's case, so the reply reverses the critics' examples rather than ranking them.")],
    "Paragraph 2 opens: 'The objection is fair against the loose use of the term, but it misses what the original idea was pointing at.' The author grants the point about usage while denying that the concept itself is empty, since it marks off feeling 'specified, monitored and sold by someone else'.",
    "Picking the occupational restriction because it resembles the author's narrowing, without noticing that the criterion is control, not job type.",
    "The most tempting distractor narrows the concept as the author does but by the wrong criterion; separating them needs paragraphs 2 and 3 together.", cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-D-05  The cultural omnivore (Medium)
# =====================================================================================
passage("R03-D-05", T,
    "The rise of omnivorous taste among elites has not ended cultural distinction but moved it, since breadth, a knowing manner of liking and selective dislikes now mark class as refusal once did.",
    [
        "For a long time the sociology of taste worked with a simple map. At the top of the social order sat a refined culture of opera, poetry and the old masters, at the bottom sat popular entertainments, and a person's place in society could be read, with fair accuracy, from the position of their preferences on this ladder. Elites, on this picture, distinguished themselves by what they refused. Liking the wrong music was not merely a private failing but a mark of origin.",
        "Surveys of cultural consumption in a number of wealthy countries have since complicated the map. The most educated and affluent groups, it turns out, are no longer best described as snobs who like only high culture. They are more often omnivores: they go to the opera and to the cinema, read literary fiction and crime novels, and are happy to discuss both a string quartet and a pop album. Some observers have greeted this as the end of cultural hierarchy, a sign that the old boundaries between high and low have dissolved and that taste has become a matter of individual preference rather than of class.",
        "That conclusion is premature. Breadth of taste is itself unevenly distributed, because it requires money, time, travel and, above all, the confidence to move between worlds without feeling out of place. The person who can talk knowledgeably about both a symphony and a street-food stall has accumulated a cultural range that is far harder to acquire than a liking for either alone. Moreover, omnivores rarely consume popular forms in the same way as their usual audiences. They tend to approach them with a knowing, curatorial attitude, prizing a song for its place in the history of a genre or enjoying a film with a touch of irony, and this manner of liking can mark distance as effectively as refusal once did.",
        "Nor is the omnivore's appetite unlimited. Research on what people say they dislike has suggested that the forms most often rejected by the highly educated tend to be those most associated with the least educated, so that the boundary has moved rather than vanished. None of this means that the loosening of old hierarchies is an illusion; it is a genuine change that the opera house must now compete for prestige with a well-chosen food truck. But distinction has not disappeared with the decline of snobbery. It has learned to express itself through openness, and openness is harder to criticise than exclusion because it looks so much like a virtue.",
    ],
    "Medium", "Critique of a common interpretation, with two separate counter-arguments and a concession; ideas are abstract but clearly signposted.",
    "R03D-cultural-omnivore-taste")

rcq("R03-D-05-1", "Specific detail", "Easy",
    "According to the passage, the older 'simple map' of taste held that",
    "a person's social standing could be read from where their preferences fell on a ladder from refined to popular culture.",
    [("educated people enjoyed both high and popular culture, though they tended to enjoy the two in quite different settings.",
      "This describes the omnivore pattern that surveys later found (paragraph 2), not the older map of paragraph 1."),
     ("taste was largely a matter of individual preference, with only a loose and unreliable connection to social class.",
      "This is the conclusion that 'Some observers' draw from the omnivore findings in paragraph 2; the old map tied taste closely to class."),
     ("elites marked themselves out mainly by how much they spent on concerts, exhibitions and other cultural events.",
      "Paragraph 1 says elites 'distinguished themselves by what they refused', not by how much they spent.")],
    "Paragraph 1: 'a person's place in society could be read, with fair accuracy, from the position of their preferences on this ladder', a ladder running from opera, poetry and the old masters down to popular entertainments.",
    "Confusing the old map with the later findings or with the observers' interpretation of them.",
    "The answer is stated in one sentence of paragraph 1.", cognitive="Recall")

rcq("R03-D-05-2", "Inference", "Medium",
    "The author's discussion of the 'knowing, curatorial attitude' (paragraph 3) suggests that",
    "two people may enjoy the same popular film while their way of enjoying it marks quite different social positions.",
    [("omnivores secretly dislike the popular forms they claim to enjoy and consume them only in order to appear open-minded.",
      "The passage says omnivores do enjoy popular forms, 'prizing a song' or 'enjoying a film', but in a distinctive manner; nothing suggests secret dislike."),
     ("popular culture is transformed into high culture once educated audiences begin to adopt it and write about it.",
      "The passage says nothing about popular forms changing their status; it is the manner of consumption, not the form, that marks distance."),
     ("the manner in which something is liked matters more than breadth of taste in every form of social distinction.",
      "The author offers manner as one marker beside breadth and selective dislike, and never ranks them, let alone for every form of distinction.")],
    "Paragraph 3 says omnivores 'rarely consume popular forms in the same way as their usual audiences' and that 'this manner of liking can mark distance'. So the same object can be enjoyed by two audiences whose enjoyment signals different positions.",
    "Turning a claim about manner of enjoyment into insincerity, or into a ranking of markers.",
    "Requires moving from the description of an attitude to its social implication.", cognitive="Analysis")

rcq("R03-D-05-3", "Application / analogy", "Medium",
    "Which of the following would the author most likely treat as an instance of the shifted boundary described in paragraph 4?",
    "A graduate who boasts of enjoying every kind of music but finds one genre, loved chiefly by her town's least schooled residents, beneath notice.",
    [("A retired factory worker who listens only to the songs he grew up with and has never felt any wish to attend an opera.",
      "He shows neither omnivorous breadth nor a highly educated person's selective dislike; paragraph 4 concerns the boundary drawn by the highly educated."),
     ("A music critic who dismisses all popular music as worthless and attends only concerts of classical and early music.",
      "This is distinction by refusal of the old kind described in paragraph 1, not the moved boundary of the omnivore."),
     ("A student who listens to a very wide range of music, from folk to jazz, because her friends keep introducing her to new things.",
      "Her breadth involves no excluded form associated with the least educated, which is the feature paragraph 4 describes.")],
    "Paragraph 4 says the forms 'most often rejected by the highly educated tend to be those most associated with the least educated', so that 'the boundary has moved rather than vanished'. A self-described omnivore who excludes the one genre of the least schooled fits this exactly.",
    "Choosing the classic snob, who also draws a class boundary but in the old way the passage contrasts with the new.",
    "Two distractors involve taste and class; the key must match the specific combination of openness and selective exclusion.", cognitive="Application")

rcq("R03-D-05-4", "Structure / function", "Difficult",
    "Which of the following best describes the role of the final paragraph in the passage?",
    "It adds a further reason to doubt that hierarchy has ended, grants that real change has occurred, and then restates that distinction persists in a new form.",
    [("It withdraws the doubts raised in paragraph 3 by conceding that the loosening of cultural hierarchy is genuine after all.",
      "The concession is followed at once by 'But distinction has not disappeared', so it qualifies the argument without withdrawing paragraph 3's doubts."),
     ("It introduces evidence showing that the omnivore pattern found in surveys is confined to a small number of wealthy countries and does not hold elsewhere.",
      "Paragraph 4 says nothing about the geographic spread of the pattern; its evidence concerns what the highly educated dislike."),
     ("It shows that the old snobbery of paragraph 1 has returned among the highly educated in exactly its earlier form.",
      "Paragraph 4 speaks of 'the decline of snobbery' and says distinction now works 'through openness', which is a new form, not the old one returned.")],
    "Paragraph 4 opens with 'Nor is the omnivore's appetite unlimited', adding the evidence of selective dislikes to paragraph 3's objections; it concedes that loosening 'is a genuine change'; and it concludes that distinction 'has learned to express itself through openness'.",
    "Treating the concession as a reversal, or mistaking the moved boundary for a return of old snobbery.",
    "The paragraph does three things, including a concession that can be misread as a retraction.", cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-D-06  Professions and jurisdiction (Difficult)
# =====================================================================================
passage("R03-D-06", T,
    "Professions are better understood as rivals contesting jurisdiction over problems than as either guarantors of competence or cartels, so their fortunes depend on claiming problems more than on skill.",
    [
        "Two accounts of the professions have long competed for our assent, and each is right about something. The first, which professionals themselves favour, holds that a profession is defined by esoteric knowledge put at the service of clients who cannot judge it. Because a patient cannot assess a diagnosis or a litigant a legal argument, the state licenses practitioners, and the licence is a guarantee of competence that protects the public from charlatans. The second account, favoured by economists of a sceptical turn, treats the same licence as a barrier to entry: by limiting the number who may practise, a profession raises its fees, and its talk of public protection is simply the language in which a cartel describes itself.",
        "What the two accounts share is more interesting than what divides them. Both look at one profession at a time, as if each stood alone facing its clients, and both assume that the work a profession does is simply given: there are diseases, so there are doctors; there are disputes, so there are lawyers. Yet the boundaries of professional work are anything but given. Whether persistent unhappiness is a medical condition, a psychological difficulty, a spiritual crisis or a social problem is not settled by the nature of unhappiness. It is settled, provisionally and repeatedly, by contests among psychiatrists, psychologists, clergy and social workers, each of whom claims that the problem properly belongs to it.",
        "Seen from this angle, a profession is less a guild guarding a fixed territory than one party in a system of rival claims, and its history is a history of conquests and retreats. Licensing remains important, but as a weapon in a jurisdictional struggle rather than as either a certificate or a mere device for fixing prices. Knowledge, too, matters in a different way. What wins a contested problem is often not superior skill in treating it but a more abstract body of theory, one that allows a profession to redefine the problem in its own terms and so to argue that its rivals were treating the symptoms rather than the thing itself. A profession whose knowledge is purely practical can be displaced by one that can explain why that practice works.",
        "This does not mean that competence is irrelevant or that the cartel theorist is merely cynical. Clients are protected by licensing, and fees are raised by it. But neither effect explains why some professions grow while others shrink, or why a body of practitioners who are perfectly good at their work can find that work quietly reassigned to others. The fate of a profession, on this view, depends less on how well it does what it does than on its ability to persuade others, including the state and the public, that the problems of the moment are its problems.",
    ],
    "Difficult", "Compares two views, identifies their shared assumption and replaces both with a third, abstract model; the stance is reached only through the whole argument.",
    "R03D-professional-jurisdiction-contests", exams=DX)

rcq("R03-D-06-1", "Structure / function", "Medium",
    "The example of persistent unhappiness in paragraph 2 serves mainly to",
    "show that the profession to which a problem belongs is decided by rivalry among professions rather than by the problem itself.",
    [("suggest that psychiatrists have been steadily losing ground to clergy and social workers in the treatment of unhappiness.",
      "The passage names the rival claimants but reports no winner or trend; it says only that the question is settled 'provisionally and repeatedly'."),
     ("illustrate that some human problems are too complex for any single profession to treat adequately on its own.",
      "The point is not that the problem exceeds any one profession's ability but that its classification 'is not settled by the nature of unhappiness'."),
     ("demonstrate that licensing has failed to protect the public from practitioners who are not properly qualified to help.",
      "Licensing is not discussed in paragraph 2, and the example concerns which profession owns a problem, not the qualifications of practitioners.")],
    "Paragraph 2 says the boundaries of professional work 'are anything but given'. Unhappiness could be medical, psychological, spiritual or social, and which it is 'is not settled by the nature of unhappiness' but 'by contests' among professions. The example undermines the shared assumption that a profession's work is simply given.",
    "Reading the example as a report on who is winning, rather than as a counter to the assumption that work is given.",
    "The function depends on the preceding claim about what the two accounts share.", cognitive="Analysis")

rcq("R03-D-06-2", "Inference", "Medium",
    "It can be inferred that the author regards the two accounts in paragraph 1 as",
    "each capturing a real effect of licensing, while sharing an assumption that prevents either from explaining professional change.",
    [("equally mistaken, since licensing in fact neither protects clients from charlatans nor raises the fees that professionals charge.",
      "Paragraph 4 says 'Clients are protected by licensing, and fees are raised by it', so the author grants both effects."),
     ("incompatible with each other, so that anyone who accepts one of them is bound to reject the other entirely.",
      "Paragraph 4 accepts the effect each account describes at once, so the author does not treat them as mutually exclusive."),
     ("correct when taken together, since in combination they give a complete account of how professions rise and fall.",
      "Paragraph 4 says 'neither effect explains why some professions grow while others shrink', so together they remain incomplete.")],
    "Paragraph 1 says 'each is right about something', and paragraph 4 confirms that licensing both protects clients and raises fees. But paragraph 2 says both 'look at one profession at a time' and treat its work as 'simply given', and paragraph 4 adds that neither explains growth and decline.",
    "Overlooking the concession in paragraph 4 and concluding that the author rejects both accounts outright.",
    "Requires joining paragraph 1's framing, paragraph 2's diagnosis and paragraph 4's concession.", cognitive="Analysis")

rcq("R03-D-06-3", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most weaken the author's claim about how knowledge matters in contests over problems (paragraph 3)?",
    "Across many contests over newly recognised problems, the winner was usually the group with the best record of treating them, whatever theories its rivals offered.",
    [("A profession with an abstract theory took over a problem that its rivals had long treated, and later lost it again when that theory fell from favour.",
      "This is consistent with the author's view: theory won the problem, and the loss fits a history 'of conquests and retreats'."),
     ("Practitioners in a profession that lost a problem to a rival were later found to have been entirely competent at treating it.",
      "This supports paragraph 4's claim that people 'perfectly good at their work can find that work quietly reassigned'."),
     ("After one profession won control of a problem, licensing rules were rewritten so as to bar its rivals from treating that problem.",
      "This fits the author's description of licensing as 'a weapon in a jurisdictional struggle', and says nothing against the role of theory.")],
    "Paragraph 3 claims that 'What wins a contested problem is often not superior skill in treating it but a more abstract body of theory'. A broad pattern in which practical success, regardless of rivals' theories, usually decided the contest directly contradicts this.",
    "Choosing a case that mentions theory or competence but is consistent with, or supports, the author's model.",
    "Each distractor is drawn from the passage's own model and supports it in a different way; only the key reverses the specific claim about theory and skill.", cognitive="Analysis", exams=DX)

rcq("R03-D-06-4", "Inference", "Difficult",
    "The author would most likely agree with which of the following?",
    "A body of practitioners could become more skilled over a decade and still end it with a narrower field of work.",
    [("The size of a profession at a given moment is a reliable measure of how well it serves the clients who rely on it.",
      "Paragraph 4 says a profession's fate 'depends less on how well it does what it does' than on its persuasiveness, so size does not track quality of service."),
     ("A profession armed with abstract theory will always defeat a rival whose knowledge is purely practical in a contest over a problem.",
      "Paragraph 3 says theory 'often' wins and that a practical profession 'can be' displaced; saying always overstates a hedged claim."),
     ("The state's part in professional life is confined to certifying the competence of individual practitioners through licences.",
      "Paragraph 3 treats licensing as 'a weapon in a jurisdictional struggle', and paragraph 4 names the state among those a profession must persuade.")],
    "Paragraph 4 says practitioners 'perfectly good at their work can find that work quietly reassigned', because fate depends 'less on how well it does what it does' than on claiming problems. Growing skill is therefore compatible with a shrinking jurisdiction.",
    "Choosing the 'always' option because it echoes paragraph 3's claim about theory, missing the hedge.",
    "The key is an unstated consequence of paragraph 4; the strongest distractor overstates a hedged claim from paragraph 3.", cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-D-07  Inconspicuous consumption (Medium, 5 questions)
# =====================================================================================
passage("R03-D-07", T,
    "Affluent households have shifted from conspicuous display to hard-to-see spending on schooling, health and time, which transmits advantage more effectively and shields it from criticism by presenting it as virtue.",
    [
        "The phrase 'conspicuous consumption', coined by Thorstein Veblen in the 1890s, named a habit of the wealthy of his day: the purchase of goods whose chief use was to show that one could afford them. The mansion, the carriage and the idle household were, on this account, less comforts than advertisements. The idea proved so useful that it outlived the society that prompted it, and it still shapes how we picture status spending: the logo on the handbag, the oversized car, the watch that costs more than a year's rent.",
        "The picture now misleads more than it reveals, at least at the top. As mass production and global supply chains have made once-rare goods cheap, the handbag and the car have become available, in passable imitations, to almost anyone with a credit card. Display of this kind has lost much of its power to separate, and many of the most advantaged households have turned away from it. Their spending flows instead into things that are hard to see and harder to copy: private tuition and a house in the right school catchment, retirement savings, organic groceries, exercise classes, domestic help that frees time for reading, and clothing whose quality is recognised only by those who know what to look for. The signal, where there is one, is addressed to a narrow audience of peers rather than to the street. The pattern has come to be called inconspicuous consumption.",
        "It would be easy to treat the change as an improvement in taste, a retreat from vulgar display into quieter and more sensible habits. In part it is. Much of this spending yields real benefits in health, in learning and in security, and few would wish the rich to return to buying gold-plated taps. But the shift has two consequences that the language of good taste conceals. The first is that inconspicuous goods are more effective at reproducing advantage than conspicuous ones ever were. A diamond can be sold; a childhood spent in good schools, with books at home and parents who have time, becomes part of a person and can neither be taken away nor easily acquired later. Spending of this kind does not merely display a position; it passes it on.",
        "The second consequence is moral. Conspicuous consumption invited criticism precisely because it was conspicuous. The flashy car was an obvious target for the satirist and the moralist, and its owner could be accused of vanity. Inconspicuous consumption is much harder to criticise, because it presents itself not as display but as virtue: one is not showing off, one is merely eating well, looking after one's health and investing in one's children. The vocabulary that surrounds it, of wellness, sensible choices and doing the best for one's family, offers the satirist nothing obviously vulgar to mock. Those who cannot afford to do the same are not envied so much as quietly judged, as though their diets and their children's results were failures of character rather than of income.",
        "None of this is an accusation of bad faith. It does not require us to think the affluent hypocritical, or the parent paying for tuition secretly bent on buying status; most such choices are made sincerely, for the reasons people give. The point is structural rather than personal. A society in which advantage is transmitted through the visible accumulation of objects at least makes its inequalities legible. One in which advantage flows through habits, schooling and time has made them harder to see, and inequalities that are hard to see are also harder to argue about.",
    ],
    "Medium", "A familiar concept is updated and critiqued through two named consequences, a concession and a disclaimer about motives; argument is clearly signposted.",
    "R03D-inconspicuous-consumption-status")

rcq("R03-D-07-1", "Specific detail", "Easy",
    "According to the passage, conspicuous display has lost much of its power to separate the advantaged from others because",
    "cheaper production has put passable versions of once-rare goods within reach of most people.",
    [("satirists and moralists have made the owners of showy goods into figures of public ridicule.",
      "Paragraph 4 says showy goods invited criticism, but the passage gives cheap imitation, not ridicule, as the reason display lost its power to separate."),
     ("the wealthiest households now keep most of their wealth in savings rather than in goods of any kind.",
      "Retirement savings appear in a list of inconspicuous spending, but the passage never says most wealth is held this way or that this caused the change."),
     ("rising taxes on imported luxury goods have made open displays of wealth far more costly than they were.",
      "Taxes are never mentioned; paragraph 2 says such goods became cheaper, not more costly.")],
    "Paragraph 2: 'As mass production and global supply chains have made once-rare goods cheap, the handbag and the car have become available, in passable imitations, to almost anyone with a credit card. Display of this kind has lost much of its power to separate'.",
    "Picking a detail from elsewhere in the passage that is not given as the cause.",
    "The cause is stated in the sentence just before the claim.", cognitive="Recall")

rcq("R03-D-07-2", "Inference", "Medium",
    "The contrast between a diamond and a childhood in good schools (paragraph 3) implies that",
    "advantages built into a person are passed on more securely than those held as saleable property.",
    [("diamonds are a poor financial investment compared with spending on a child's education, which yields a higher return.",
      "The passage makes no comparison of financial returns; its point is that one can be sold or lost while the other 'becomes part of a person'."),
     ("parents who spend money on jewellery tend to care less about their children's futures than parents who pay for schooling.",
      "Nothing is said about the motives or care of particular parents; paragraph 5 explicitly sets aside personal motives."),
     ("the benefits of a good education can be gained just as readily in adult life as in childhood, given enough money.",
      "This contradicts the passage, which says such a childhood 'can neither be taken away nor easily acquired later'.")],
    "Paragraph 3 says 'A diamond can be sold', whereas a good childhood 'becomes part of a person and can neither be taken away nor easily acquired later', and concludes that such spending 'passes it on'. Advantage embodied in a person is transmitted more securely than property.",
    "Reading the contrast as one of financial value or of parental attitudes.",
    "The implication must be drawn from the contrast together with the sentence that follows it.", cognitive="Understanding")

rcq("R03-D-07-3", "Structure / function", "Medium",
    "The reference to gold-plated taps in paragraph 3 serves to",
    "concede that the turn away from showy spending is, in some respects, a genuinely welcome change.",
    [("illustrate the sort of quiet, hard-to-copy goods on which affluent households now prefer to spend their money.",
      "Gold-plated taps are the opposite of inconspicuous goods; they stand for the vulgar display that the rich have abandoned."),
     ("suggest that inconspicuous consumption is simply conspicuous consumption carried on in more refined and tasteful forms.",
      "The author argues that the new spending works differently, by passing advantage on and by looking like virtue; it is not the old display in new dress."),
     ("argue that wealthy households ought to be discouraged by public policy from spending on luxuries of every kind.",
      "No policy is proposed, and the remark appears in a sentence granting that the new spending 'yields real benefits'.")],
    "The remark comes in the concession 'In part it is': much inconspicuous spending 'yields real benefits', and 'few would wish the rich to return to buying gold-plated taps'. It grants the improvement before the author turns, with 'But', to the two concealed consequences.",
    "Treating the taps as an example of the new spending, or reading the concession as the author's main claim.",
    "The function depends on recognising the concession before the turn signalled by 'But'.", cognitive="Analysis")

rcq("R03-D-07-4", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most weaken the author's claim that inconspicuous goods reproduce advantage more effectively than conspicuous ones?",
    "Children of wealthy families that spent heavily on schooling ended up no better placed as adults than children of equally wealthy families that spent on luxuries.",
    [("Most affluent parents who pay for private tuition say that they do so out of concern for their children's learning and not out of any wish for status.",
      "Paragraph 5 says 'most such choices are made sincerely' and 'The point is structural rather than personal', so motives do not bear on the claim."),
     ("Imitations of luxury handbags, cars and watches have continued to become cheaper and more widely available to ordinary households.",
      "This supports paragraph 2's explanation of why display lost its power to separate; it does not test which spending transmits advantage."),
     ("Households that spend on organic food and exercise classes report better health than households of similar income that do not.",
      "This fits the concession in paragraph 3 that such spending 'yields real benefits', and it says nothing about transmission to the next generation.")],
    "Paragraph 3 claims that spending on schooling and upbringing 'does not merely display a position; it passes it on', more effectively than conspicuous goods. If equally wealthy families spending on schooling secured no better adult positions than those spending on luxuries, that claim would fail.",
    "Choosing the sincerity option, which addresses motives that the author has already declared irrelevant.",
    "The strongest distractor answers a different charge, one that paragraph 5 explicitly sets aside; seeing this needs the whole passage.", cognitive="Analysis", exams=DX)

rcq("R03-D-07-5", "Author's tone / attitude", "Difficult",
    "The author's attitude towards inconspicuous consumption is best described as",
    "critical of its social effects, while declining to impugn the motives of those who practise it.",
    [("scornful, regarding it as a form of hypocrisy that disguises a hunger for status as healthy and responsible living.",
      "Paragraph 5 says 'None of this is an accusation of bad faith' and that 'most such choices are made sincerely, for the reasons people give'."),
     ("approving, regarding it chiefly as a welcome advance in good taste over the vulgar display of earlier generations of the rich.",
      "The author grants the change is an improvement only 'In part', and devotes paragraphs 3 to 5 to consequences that 'the language of good taste conceals'."),
     ("neutral, describing a change in the spending of the rich without passing any judgement on what that change brings about.",
      "The author judges the consequences plainly: it reproduces advantage, leads to the poor being 'quietly judged', and makes inequality 'harder to argue about'.")],
    "Paragraphs 3 and 4 criticise the effects (more effective transmission of advantage, moral cover, judgement of those who cannot afford it), and paragraph 5 adds that 'The point is structural rather than personal', explicitly declining to call the affluent hypocritical.",
    "Mistaking the critique for scorn of individuals, or overweighting the concession in paragraph 3.",
    "Requires holding the critique, the concession and the disclaimer about motives together.", cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-D-08  Absolute and relative mobility (Difficult, 5 questions)
# =====================================================================================
passage("R03-D-08", T,
    "Public debate confuses absolute mobility, which can rise for all, with relative mobility, which is zero-sum, and so misreads economic slowdowns as closure and hides the cost that greater fairness imposes.",
    [
        "Few political promises are as widely shared as the promise of social mobility. Parties that agree on little else agree that a child's prospects should not be fixed by the circumstances of her birth, and the claim that mobility has stalled is one of the most damaging charges that can be laid against a government. Yet the word covers two quite different things, and much public argument about it goes astray because the two are run together.",
        "The first is absolute mobility: the share of people who end up better off than their parents, whether by income or by the kind of work they do. The second is relative mobility: the extent to which a person's position in the distribution, as opposed to their standard of living, differs from their parents' position. The two can move independently. In a period of rapid growth and expanding professional employment, most children may outearn their parents and many may enter occupations their parents never held, even if the chance of a child born near the bottom reaching the top, compared with that of a child born near the top, has not changed at all. Everyone rides the escalator up, but the order of people on it stays the same.",
        "This distinction explains a puzzle. When growth slows and the expansion of professional jobs levels off, absolute mobility falls, and people who do no better than their parents feel, reasonably enough, that something has closed. They often conclude that society has become less fair. Imagine a town where a mill employed one generation and new offices employed the next. The children did better than their parents without anyone being pushed aside, and the town experienced this as openness. When the offices stop hiring, the grandchildren find that the climb has ended. Yet on the measures that track their position against the children of the office managers, the chances may be much as they were: what has disappeared is not openness but the rising tide that once let a whole generation move up without anyone having to move down. The sense of closure is real; its diagnosis is frequently mistaken.",
        "The distinction also exposes an awkwardness that politicians prefer to leave unspoken. Absolute mobility can, in principle, be enjoyed by everyone at once. Relative mobility cannot. If positions are ranked, then for one family to climb another must fall, and a serious commitment to relative mobility is therefore a commitment to downward mobility for some children of the comfortable. It is not surprising that the comfortable resist it, often without any sense of doing so, through the ordinary devices of private tuition, a well-placed word, or the purchase of a house near the right school. Each of these looks like ordinary care for one's own children; together they amount to a defence of position.",
        "None of this makes one kind of mobility the real one. Absolute mobility answers a question about material progress: are people living better than their parents did? Relative mobility answers a question about fairness: does birth still decide where one ends up? Both questions matter, and neither is easy to answer with confidence, since incomes fluctuate and occupations change their meaning across generations. But a society that wants more of the second kind should be honest that it cannot be had at no one's expense, and a society that mourns the loss of the first should not mistake a slower economy for a more rigid one.",
    ],
    "Difficult", "Rests on an abstract conceptual distinction whose consequences are drawn out in two directions, with an even-handed conclusion; requires tracking which measure each claim concerns.",
    "R03D-absolute-relative-social-mobility", exams=DX)

rcq("R03-D-08-1", "Meaning in context", "Easy",
    "The image of the escalator in paragraph 2 conveys that",
    "living standards can rise for everyone together while people's ranking relative to one another stays fixed.",
    [("people born near the bottom rise faster than those born near the top whenever the economy is growing quickly.",
      "The image says 'the order of people on it stays the same', so no group overtakes another."),
     ("moving up in society is automatic and calls for no effort or ability on the part of the individuals concerned.",
      "Effort and ability are never discussed; the image concerns the difference between rising standards and unchanged rank."),
     ("a society can carry people downwards just as easily as it carries them upwards, depending on economic conditions.",
      "The escalator in the passage only goes up; downward movement is discussed in paragraph 4 as a feature of relative mobility.")],
    "The escalator sentence sums up the preceding one: most children may outearn their parents 'even if the chance of a child born near the bottom reaching the top ... has not changed at all'. All rise, but 'the order of people on it stays the same'.",
    "Reading the image as a claim about effort or about who rises faster.",
    "The image glosses the sentence immediately before it.", cognitive="Understanding")

rcq("R03-D-08-2", "Inference", "Medium",
    "It can be inferred from paragraph 3 that people who conclude, when growth slows, that society has become less fair",
    "may be rightly sensing a real loss but wrongly attributing it to a decline in openness.",
    [("are mistaken in believing that they are doing no better than their parents did at the same stage of life.",
      "The author says they feel something has closed 'reasonably enough' and that 'The sense of closure is real'; their experience is not in doubt."),
     ("have generally lived through a genuine fall in relative mobility that the usual measures have failed to detect.",
      "The passage says that on measures of relative position 'the chances may be much as they were', which points the other way."),
     ("are reacting chiefly to a rise in downward mobility among the children of comfortable and well-placed families.",
      "Paragraph 3 attributes the feeling to falling absolute mobility; downward mobility of the comfortable comes up only in paragraph 4, as something they resist.")],
    "Paragraph 3: 'The sense of closure is real; its diagnosis is frequently mistaken.' What has disappeared 'is not openness but the rising tide', so the loss is in absolute mobility, while relative chances 'may be much as they were'.",
    "Treating the author as dismissing these people's experience, rather than their explanation of it.",
    "Requires separating the experience the author accepts from the diagnosis the author questions.", cognitive="Analysis")

rcq("R03-D-08-3", "Application / analogy", "Medium",
    "Which of the following would be a case of relative mobility rising while absolute mobility falls, in the passage's sense?",
    "In a stagnant economy where few children outearn their parents, children of poor families increasingly overtake children of rich families in the income ranking.",
    [("In a booming economy where nearly all children outearn their parents, the income ranking is substantially reshuffled from one generation to the next.",
      "Here absolute mobility rises, since nearly all outearn their parents, so it is a case of both kinds rising, not of absolute mobility falling."),
     ("In a stagnant economy where few children outearn their parents, children remain in much the same place in the income ranking as their parents held.",
      "Absolute mobility falls here, but relative mobility is unchanged rather than rising; this is the situation described in paragraph 3."),
     ("In a booming economy where most children outearn their parents, the order of families in the income ranking remains exactly what it was before.",
      "This is the escalator of paragraph 2: absolute mobility is high and relative mobility unchanged, the reverse of what is asked.")],
    "Absolute mobility is 'the share of people who end up better off than their parents'; relative mobility concerns changes in 'position in the distribution'. A stagnant economy where few outearn their parents has low absolute mobility, and poor children overtaking rich ones in rank is a rise in relative mobility.",
    "Mixing up the two measures, especially choosing the paragraph 3 case in which relative mobility merely stays the same.",
    "Requires applying both definitions to four cases that differ on two dimensions.", cognitive="Application")

rcq("R03-D-08-4", "Main idea / primary purpose", "Difficult",
    "Which of the following best captures the main argument of the passage?",
    "Since absolute and relative mobility answer different questions and can diverge, running them together leads people to misread slowdowns and to ignore what fairness costs.",
    [("Relative mobility is the only true measure of whether a society is open, while absolute mobility merely reflects how fast its economy is growing.",
      "Paragraph 5 says 'None of this makes one kind of mobility the real one', and that the question absolute mobility answers also matters."),
     ("Social mobility has not stalled as its critics claim; it has simply become much harder to measure than it was in earlier generations.",
      "The author accepts that absolute mobility falls when growth slows, and the difficulty of measurement is a passing remark, not the thesis."),
     ("Comfortable families use private tuition and housing choices to block relative mobility, and governments should act to prevent them from doing so.",
      "This narrows the passage to paragraph 4 and adds a prescription; the author asks for honesty about costs, not for action against families.")],
    "Paragraph 1 says argument goes astray 'because the two are run together'; paragraph 3 shows this leads people to read slower growth as closure; paragraph 4 shows it hides the fact that relative mobility requires some to fall; paragraph 5 says both kinds matter and draws both lessons.",
    "Choosing the option that ranks one kind of mobility above the other, which the final paragraph explicitly rejects.",
    "Each distractor captures part of the passage or a plausible stance; the key requires all four movements of the argument.", cognitive="Analysis", exams=DX)

rcq("R03-D-08-5", "Inference", "Difficult",
    "The author would most likely say that a government promising to raise relative mobility while ensuring that no family moves down the ranking",
    "is promising something that cannot be delivered when positions are ranked, whatever the rate of economic growth.",
    [("could keep its promise provided that the economy grew fast enough to raise the incomes of every family at once.",
      "Growth raises absolute mobility, which can 'be enjoyed by everyone at once'; it cannot let one family climb the ranking without another falling."),
     ("could keep its promise by abolishing private tuition and other devices that comfortable families use to defend their position.",
      "Removing such devices might raise relative mobility, but paragraph 4 says that 'for one family to climb another must fall', so some would still move down."),
     ("is making essentially the same promise as a government that pledges to raise the living standards of each new generation.",
      "That pledge concerns absolute mobility; treating the two promises as the same is the very confusion the passage criticises.")],
    "Paragraph 4: 'If positions are ranked, then for one family to climb another must fall', so relative mobility 'cannot' be enjoyed by everyone at once, unlike absolute mobility. Growth changes standards of living, not rankings, so no growth rate rescues the promise; paragraph 5 adds that it 'cannot be had at no one's expense'.",
    "Believing that growth can make relative mobility painless, which confuses the two measures.",
    "The most tempting distractor applies the logic of absolute mobility to relative mobility; spotting this needs paragraphs 2 and 4 together.", cognitive="Analysis", exams=DX)
