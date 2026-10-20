import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

T = "Perception, attention and memory"
DX = ("CAT", "XAT")

# =====================================================================================
# R02-A-01  Perception as unconscious inference (Medium)
# =====================================================================================
passage("R02-A-01", T,
    "Seeing is an active, inferential interpretation of ambiguous sensory evidence, but this does not make the senses untrustworthy.",
    [
        "It is natural to think of seeing as a kind of recording. Light enters the eye, an image forms on the retina, and the brain, like a careful clerk, reads off what is there. The picture is attractive because it matches how perception feels: effortless, immediate, and apparently free of any contribution from the perceiver. Yet the retinal image is a poor document: it is upside down, flat, constantly jittering with the movements of the eye, and interrupted by a blind spot where the optic nerve leaves the retina. Above all, it is ambiguous, in the sense that a small image on the retina could be a small object nearby or a large one far away; a patch of dim grey could be a dark surface in bright light or a pale surface in shadow. The eye, in short, delivers considerably less information than we ordinarily experience ourselves as seeing.",
        "For this reason many students of vision have preferred to describe perception as a form of inference. The brain, on this account, treats the incoming signal as evidence and settles on the interpretation that best explains it, given what it has learned about how the world usually is. Light tends to come from above, so a disc shaded darker at the bottom is seen as a bump and the same disc turned over as a dent. Objects tend to keep their size, so a person walking away is seen as receding rather than shrinking. These are not conclusions we reach; they are conclusions reached on our behalf, before anything is presented to awareness.",
        "The word 'inference' invites an obvious objection: if perception is a guess shaped by expectation, why do we not simply see whatever we expect? The answer is that the guess is tightly disciplined by the evidence, and that the expectations doing the work are of a peculiar kind. They are not the beliefs we hold and can revise in conversation, but assumptions built up over a lifetime of looking, and perhaps over the history of the species. This is why many visual illusions survive full knowledge of the trick. A viewer who has measured two lines and found them equal will still see one as longer; what she knows and what she sees have been settled by different processes.",
        "It would be a mistake, then, to conclude that perception is unreliable because it is inferential. The assumptions it relies on are mostly true of the environments in which they were formed, which is why they so rarely mislead us outside the laboratory, where illusions are carefully built to exploit them. What the inferential view really overturns is not our trust in the senses but the idea that seeing is passive. Every glance is a small act of interpretation, and its seeming effortlessness is the mark of how well the work is done, not evidence that no work is being done.",
    ],
    "Medium", "Abstract argument that raises and answers an objection, then guards against an overreading; vocabulary is moderate.",
    "R02A-perception-as-unconscious-inference")

rcq("R02-A-01-1", "Main idea / primary purpose", "Medium",
    "The primary purpose of the passage is to",
    "argue that seeing actively interprets ambiguous evidence, while denying that this makes the senses untrustworthy.",
    [("show that visual illusions reveal how unreliable perception is, so that what we see should be checked against measurement.",
      "Paragraph 4 says it would be 'a mistake' to conclude that perception is unreliable, and that illusions are built in laboratories to exploit assumptions that rarely mislead us elsewhere."),
     ("explain how the defects of the retinal image, such as its blind spot, are corrected by the beliefs a viewer holds about the world.",
      "The blind spot is one detail of paragraph 1, and paragraph 3 says the expectations at work are not 'the beliefs we hold and can revise', so the option is both too narrow and a distortion."),
     ("defend the view that seeing is a form of conscious reasoning in which the brain, like a careful clerk, weighs the evidence.",
      "Paragraph 2 says these are 'not conclusions we reach', and the careful clerk belongs to the recording picture the author rejects in paragraph 1.")],
    "Paragraph 1 rejects the picture of seeing as recording, paragraph 2 offers the inferential account, paragraph 3 answers an objection to it, and paragraph 4 concludes that the view overturns 'the idea that seeing is passive' but not 'our trust in the senses'. The key holds both the thesis and the qualification.",
    "Picking the illusion option because illusions are discussed at length, and missing that the author uses them to make a different point.",
    "One distractor turns the author's concession into its opposite; another borrows the clerk image from the view being rejected.")

rcq("R02-A-01-2", "Specific detail", "Easy",
    "According to the passage, the retinal image is ambiguous in the sense that",
    "the same pattern on the retina is consistent with more than one arrangement of things in the world.",
    [("it is upside down and flat, so the brain has to turn it the right way up before anything can be seen at all.",
      "Paragraph 1 lists inversion and flatness as separate defects before 'Above all, it is ambiguous'; ambiguity is illustrated by the size and grey patch examples, not by inversion."),
     ("the blind spot removes part of every image, leaving gaps that the viewer's expectations must fill in.",
      "The blind spot is another of the listed defects; the passage illustrates ambiguity with one image fitting two different scenes, not with missing parts of the image."),
     ("eye movements make it change from moment to moment, so that no single image can ever be relied on.",
      "Jitter is mentioned as a separate defect, and the passage never says that no image can be relied on.")],
    "Paragraph 1 gives two illustrations of ambiguity: a small retinal image 'could be a small object nearby or a large one far away', and dim grey 'could be a dark surface in bright light or a pale surface in shadow'. In each, one image fits two states of the world.",
    "Choosing one of the other listed defects of the retinal image instead of the one the passage calls ambiguity.",
    "The answer is in two adjacent sentences; the distractors are the other defects in the same list.",
    cognitive="Recall")

rcq("R02-A-01-3", "Strengthen / weaken / assumption", "Difficult",
    "The author explains that perceptual assumptions rarely mislead us outside the laboratory because they are mostly true of the environments in which they were formed. Which of the following, if true, would most weaken this explanation?",
    "People who move into surroundings that violate their perceptual assumptions are, from the start, misled no more often than people who grew up there.",
    [("Laboratory illusions are deliberately constructed by researchers so as to exploit the assumptions that ordinary vision relies on.",
      "This repeats what paragraph 4 already says about illusions being 'carefully built to exploit' the assumptions, so it is consistent with the explanation rather than a challenge to it."),
     ("Some perceptual assumptions, such as the assumption that light comes from above, turn out to be shared by people raised in very different places and cultures.",
      "Shared assumptions fit paragraph 3's suggestion that some were formed 'over the history of the species'; the option says nothing about whether the assumptions mislead when they are false of a setting."),
     ("Viewers who are told exactly how an illusion works go on seeing it just as strongly as they did before being told.",
      "This bears on paragraph 3's point that knowledge does not alter what is seen, not on the paragraph 4 explanation of why the assumptions seldom mislead.")],
    "The explanation says the assumptions rarely mislead because they fit the settings that formed them. It predicts that people placed in settings where the assumptions are false will be misled more. If newcomers to such settings are misled no more often than natives, the fit between assumption and environment is not doing the work the author claims for it.",
    "Choosing the option about illusions surviving knowledge, which is true according to the passage but belongs to a different claim.",
    "Requires isolating the specific causal explanation in paragraph 4 and seeing which result breaks its prediction; two distractors restate claims the passage already makes.",
    cognitive="Analysis", exams=DX)

rcq("R02-A-01-4", "Meaning in context", "Medium",
    "In paragraph 3, the statement that 'the guess is tightly disciplined by the evidence' most nearly means that",
    "the interpretation perception settles on is held in check by what the incoming signal actually contains.",
    [("the viewer consciously tests each perceptual guess against careful measurement before accepting it as true.",
      "Paragraph 2 says the conclusions are 'reached on our behalf, before anything is presented to awareness', so conscious testing is the opposite of the claim; the measuring viewer of paragraph 3 still sees the illusion."),
     ("perception refuses to adopt any expectation that the viewer has not personally confirmed by experience.",
      "The passage allows that some assumptions may come from 'the history of the species', and it says nothing about perception refusing unconfirmed expectations."),
     ("repeated correction trains the brain, over time, to stop guessing and simply register the signal as it is.",
      "This brings back the recording picture of paragraph 1, which the author rejects; the passage says every glance remains 'a small act of interpretation'.")],
    "The phrase answers the objection 'why do we not simply see whatever we expect?' The reply is that the evidence constrains which interpretation wins, so expectation cannot override the signal at will. The key states this constraint.",
    "Reading 'disciplined' as a conscious checking process rather than a constraint built into the inference.",
    "The phrase has to be read against the objection it answers in the preceding sentence.",
    cognitive="Understanding")

# =====================================================================================
# R02-A-02  Inattentional blindness (Easy)
# =====================================================================================
passage("R02-A-02", T,
    "Inattentional blindness shows that we are poor judges of what we would notice, so where misses are costly we should design for attention that is already occupied.",
    [
        "Most people believe that anything sufficiently striking will catch their eye. If a person in a gorilla suit walked through a game of catch we were watching, we assume we would notice. A well-known series of experiments suggests otherwise. When viewers are asked to count the passes made by one team in a short video, a large share of them fail to see an unexpected figure stroll through the middle of the scene, even when it pauses to face the camera. Asked afterwards, many insist that nothing unusual happened, and some are indignant when the recording is replayed.",
        "The phenomenon, usually called inattentional blindness, is easy to misread as a failure of the eyes. It is not, or at least not in any sense that an optician could detect: the light from the unexpected figure reaches the retina as surely as the light from the ball. What fails is the selection that decides which parts of the scene will be built into conscious experience. Attention is not a spotlight that merely brightens what we are looking at; it is closer to a gate, and what does not pass through the gate is not dimly seen but, for practical purposes, not seen at all.",
        "The finding matters less because of its surprise value than because of the confidence it exposes. We are poor judges of what we would notice, because the things we miss leave no trace in experience from which we could learn that we missed them. Ordinary experience, which might be expected to correct our overconfidence, cannot do so, because an occasion on which we failed to notice something is, from the inside, indistinguishable from an occasion on which there was nothing to notice. A driver who looks at a junction while thinking about something else may have no sense that a cyclist was in view. Afterwards he will report, quite sincerely, that the cyclist came from nowhere. His honesty is not in question; his access to his own lapse is.",
        "This should not be taken to mean that attention is simply defective. A mind that admitted everything in the visual field to awareness would be overwhelmed, unable to follow the ball, read a page or hold a conversation in a crowded room. Selectivity is the price of focus, and on most days, when little that we fail to notice turns out to matter, the price is low. The lesson is narrower and more practical: where the cost of missing something is high, we should not rely on the conviction that we would have seen it, and should instead design tasks, roads and warning signals on the assumption that attention is already spoken for.",
    ],
    "Easy", "Concrete examples and a clearly signposted argument; the stance is stated directly.",
    "R02A-inattentional-blindness")

rcq("R02-A-02-1", "Specific detail", "Easy",
    "According to the passage, viewers fail to see the unexpected figure because",
    "attention lets only part of what reaches the eye into conscious experience.",
    [("the light from an unexpected object does not reach the retina while the eyes are busy tracking a moving ball.",
      "Paragraph 2 says the light 'reaches the retina as surely as the light from the ball'; the failure is not in the eyes."),
     ("they do notice the figure faintly but forget the impression before they are questioned about the video.",
      "Paragraph 2 says what does not pass the gate 'is not dimly seen but, for practical purposes, not seen at all', which rules out a faint impression later forgotten."),
     ("the figure appears too briefly and too indistinctly to register clearly on a short recording.",
      "Paragraph 1 says the figure strolls through the middle of the scene and 'pauses to face the camera', so it is neither brief nor indistinct.")],
    "Paragraph 2 locates the failure in 'the selection that decides which parts of the scene will be built into conscious experience', and compares attention to a gate. The key restates this.",
    "Assuming the problem is visual (the eyes or the recording) rather than attentional.",
    "The cause is stated in one sentence of paragraph 2, and each distractor is ruled out by an explicit phrase.",
    cognitive="Recall")

rcq("R02-A-02-2", "Inference", "Medium",
    "The remark that the driver's 'honesty is not in question; his access to his own lapse is' implies that",
    "his account is sincere yet mistaken, since a cyclist he never consciously saw left nothing in his experience to report.",
    [("he is probably concealing his inattention at the junction in order to avoid being blamed for what happened.",
      "The passage says he reports 'quite sincerely' and that his honesty 'is not in question', which is the opposite of concealment."),
     ("he glimpsed the cyclist dimly at the junction but has since lost the memory of that fleeting impression.",
      "Paragraph 2 says what fails to pass the gate of attention is 'not dimly seen but, for practical purposes, not seen at all', so there was no glimpse to lose."),
     ("cyclists who appear suddenly at junctions are among the most common causes of collisions with careful drivers.",
      "The passage makes no claim about the causes or frequency of collisions; the example illustrates how a lapse can be invisible to the person who makes it.")],
    "Paragraph 3 says the things we miss 'leave no trace in experience from which we could learn that we missed them'. The driver therefore tells the truth as he experienced it, but his experience lacks the cyclist, so the report is wrong without being dishonest.",
    "Choosing the dim glimpse option, which sounds psychologically plausible but contradicts the gate image of paragraph 2.",
    "One distractor is ruled out only by connecting paragraph 3 to the gate claim in paragraph 2.",
    cognitive="Understanding")

rcq("R02-A-02-3", "Author's tone / attitude", "Easy",
    "The author's attitude towards the selectivity of attention is best described as",
    "accepting, treating it as the price of focus while warning against trusting it where misses are costly.",
    [("alarmed, regarding it as a serious defect of the mind that ought to be corrected through training.",
      "Paragraph 4 says the finding 'should not be taken to mean that attention is simply defective' and proposes changing tasks and signals, not training attention away."),
     ("dismissive, treating the experiments as amusing curiosities with little bearing on ordinary life.",
      "Paragraph 3 says the finding matters 'less because of its surprise value' than for what it exposes, and paragraph 4 draws practical lessons for roads and warning signals."),
     ("admiring, holding that attention can be relied on to admit whatever genuinely matters in a scene.",
      "The driver example in paragraph 3 shows attention excluding something that matters a great deal, and paragraph 4 warns against relying on it where misses are costly.")],
    "Paragraph 4 calls selectivity 'the price of focus' and says the price is usually low, but advises against relying on 'the conviction that we would have seen it' where the cost of missing is high. The attitude is acceptance with a practical caution.",
    "Reading the warning about high-stakes settings as general alarm about attention.",
    "The attitude is stated in the opening sentences of the final paragraph.",
    cognitive="Understanding")

rcq("R02-A-02-4", "Application / analogy", "Medium",
    "Which of the following design decisions best reflects the lesson drawn in the final paragraph?",
    "Fitting a machine with an alarm that halts the task in progress, so that an operator is not relied on to glance at a light.",
    [("Placing a warning light directly in the operator's line of sight, on the grounds that anything plainly in view will be noticed.",
      "Paragraph 1 shows that a figure in the middle of the scene, facing the camera, goes unseen; being in view does not guarantee being noticed, so this rests on the very assumption the author rejects."),
     ("Asking pilots how confident they are that they would spot an unexpected obstacle, and grounding those who report low confidence.",
      "Paragraph 3 says 'We are poor judges of what we would notice', so self-reported confidence is the conviction the author warns us not to rely on."),
     ("Training drivers to widen their attention so that they take in the whole visual field at once rather than one part of it.",
      "Paragraph 4 says a mind that admitted everything in the visual field 'would be overwhelmed'; the author does not propose abolishing selectivity.")],
    "The final paragraph says that where misses are costly we should design 'on the assumption that attention is already spoken for'. An alarm that interrupts the task does not depend on spare attention, so it fits the lesson.",
    "Choosing the line-of-sight option because it seems to make the warning hard to miss, forgetting that the gorilla was in plain view.",
    "The tempting distractor sounds sensible and is refuted only by applying the opening experiment.",
    cognitive="Application")

# =====================================================================================
# R02-A-03  Flashbulb memory confidence (Medium)
# =====================================================================================
passage("R02-A-03", T,
    "Vivid memories of shocking public events are held with great confidence but change as much as ordinary memories, so vividness and certainty are weak guides to accuracy.",
    [
        "Ask people where they were when they heard of some great public shock, an assassination, a disaster broadcast live, the sudden death of a famous figure, and many will answer at once and in detail. They remember the room, who told them, what they were holding, the first thing they said. Such recollections have been called flashbulb memories, the name suggesting that a moment of intense feeling exposes the scene, as a flash exposes film, and fixes it for good. The people who hold them are rarely in doubt. Of all their memories, these seem the least likely to be wrong.",
        "The difficulty is that when such memories have been checked, they have often turned out to be wrong in exactly the ways ordinary memories are. Researchers have questioned people within a day or two of a widely reported event and then again months or years later. The later accounts frequently differ from the earlier ones, sometimes in small particulars and sometimes wholesale: a person who first wrote that she heard the news from a colleague at work later describes, with complete assurance, watching it on television at home. Confronted with her own earlier account, she may concede that she wrote it while continuing to feel that her present memory is the true one.",
        "What sets these memories apart, then, is not their accuracy but the confidence and vividness with which they are held; in these memories, conviction and correctness have come apart. One explanation is that the events are rehearsed endlessly. They are discussed with friends, revisited in anniversary broadcasts and retold until the story has a familiar shape. Each retelling is less a replay than a reconstruction, and the most recent reconstruction is the one that feels like the original. Emotion contributes too, but perhaps less to the record than to the sense of its importance: a moment that mattered seems as though it must have been remembered faithfully.",
        "None of this means that strong feeling has no effect on memory. People rarely forget that the event happened, and there is reason to think that emotion sharpens memory for whatever is central to an experience while letting the periphery blur. The trouble is that the details we are proudest of recalling, the room, the messenger, the coffee cup, are precisely the peripheral ones. The practical lesson extends well beyond public events. Wherever memory is used as evidence, the vividness of a recollection and the certainty of the person reporting it are weaker guides to its truth than we are inclined to believe.",
    ],
    "Medium", "Critique of a common belief with an explanation and a concession; the final distinction between central and peripheral detail needs care.",
    "R02A-flashbulb-memory-confidence")

rcq("R02-A-03-1", "Meaning in context", "Easy",
    "In paragraph 3, the phrase 'conviction and correctness have come apart' means that",
    "how sure people feel about these memories no longer tracks how accurate the memories are.",
    [("people grow steadily less confident in these memories as the memories become less accurate over the years.",
      "Paragraph 2 says the later, changed accounts are given 'with complete assurance', so confidence does not fall as accuracy does."),
     ("each memory splits into a true core and an invented portion, which the person can readily tell apart.",
      "The passage says people cannot tell: the woman feels 'that her present memory is the true one' even when shown her earlier account."),
     ("people remember the shocking event correctly but feel unsure about the details surrounding it.",
      "This reverses the passage: people are most certain of the surrounding details, 'the room, the messenger, the coffee cup', which are the ones that drift.")],
    "The sentence contrasts 'accuracy' with 'the confidence and vividness with which they are held'. Saying conviction and correctness have come apart means the two no longer go together: confidence stays high while accuracy falls.",
    "Assuming the two must move together, so that falling accuracy would bring falling confidence.",
    "The meaning is fixed by the first half of the same sentence.",
    cognitive="Understanding")

rcq("R02-A-03-2", "Inference", "Medium",
    "The example of the woman who concedes that she wrote the earlier account suggests that",
    "evidence that a memory has changed need not shake the feeling that its present version is the authentic one.",
    [("people readily give up a vivid memory once they are shown a written record that contradicts what they now recall.",
      "Paragraph 2 says she concedes writing the account 'while continuing to feel that her present memory is the true one', so she does not give the memory up."),
     ("accounts written in the shock of the moment are less reliable than those formed after a period of calm reflection.",
      "The passage treats the early account as the check against which later ones are found to have changed, and says later versions are reconstructions; nothing suggests the early record is the weaker one."),
     ("she has knowingly revised her story over the years so as to make it more dramatic when telling it to others.",
      "The passage describes her later account as given 'with complete assurance' and explains change by unwitting reconstruction; nothing suggests deliberate embellishment.")],
    "She accepts the documentary evidence yet still feels her present memory is true. The example shows that recognising a discrepancy does not dislodge the sense of authenticity, which paragraph 3 then explains: 'the most recent reconstruction is the one that feels like the original'.",
    "Assuming that a rational person shown the evidence would revise the memory, and so choosing the first distractor.",
    "Requires reading the concession together with what she continues to feel.",
    cognitive="Analysis")

rcq("R02-A-03-3", "Structure / function", "Medium",
    "Which of the following best describes the role of the final paragraph in the passage?",
    "It grants a real effect of emotion on memory and shows that the grant leaves the main argument standing.",
    [("It withdraws the earlier claim that flashbulb memories are often inaccurate, in the light of evidence that emotion strengthens memory.",
      "The paragraph keeps the claim: it says the proudly recalled details 'are precisely the peripheral ones', which emotion lets blur, and ends by restating that vividness is a weak guide to truth."),
     ("It turns to a separate subject, the use of memory as evidence in courts, for which the earlier paragraphs have not prepared the reader.",
      "Courts are never mentioned; the remark about memory 'used as evidence' generalises the passage's own conclusion rather than opening an unprepared topic."),
     ("It offers readers a reliable technique for telling their accurate flashbulb memories apart from their inaccurate ones.",
      "No technique is offered; the paragraph explains why the most vivid details are the least trustworthy, which is a caution, not a method.")],
    "The paragraph opens with a concession ('None of this means that strong feeling has no effect on memory'), notes that emotion sharpens central detail, then shows that the details people are surest of are peripheral, so the concession does not rescue them. It ends by generalising the lesson.",
    "Taking the opening concession as a retreat from the thesis.",
    "Students must see how the central and peripheral distinction turns the concession back in favour of the thesis.",
    cognitive="Analysis")

rcq("R02-A-03-4", "Except / not supported", "Difficult",
    "Each of the following is supported by the passage EXCEPT:",
    "How vivid a memory is and how certain its owner feels give no indication at all of whether it is true.",
    [("A person can accept that her earlier account differs from her present one without ceasing to trust the present one.",
      "Supported by paragraph 2: the woman concedes she wrote the earlier account 'while continuing to feel that her present memory is the true one'."),
     ("Repeated retelling of an event can make a reconstructed version of it feel like the original memory.",
      "Supported by paragraph 3: each retelling is 'less a replay than a reconstruction, and the most recent reconstruction is the one that feels like the original'."),
     ("Emotion may improve memory for the features of an experience that were central to it.",
      "Supported by paragraph 4: 'there is reason to think that emotion sharpens memory for whatever is central to an experience'. The hedge in the passage matches the hedge 'may'.")],
    "The final sentence says vividness and certainty 'are weaker guides to its truth than we are inclined to believe'. A weaker guide is still some guide, so the claim that they give no indication at all overstates the passage. The other three statements are each found in the text.",
    "Rejecting the hedged statement about emotion because it seems to cut against the thesis, and accepting the extreme statement because it sounds like the thesis.",
    "The unsupported option is an exaggeration of the author's own conclusion, while one supported option looks like a counterpoint; telling them apart needs attention to degree.",
    cognitive="Analysis", exams=DX)

# =====================================================================================
# R02-A-04  Adaptive forgetting (Easy)
# =====================================================================================
passage("R02-A-04", T,
    "Forgetting is largely an editing function that keeps useful memories accessible, though not all forgetting is benign.",
    [
        "We tend to speak of forgetting as a failure, the mind's equivalent of a leaking roof: students blame it for poor marks, older people fear it as a sign of decline, and whole industries promise to reduce it. Behind these attitudes lies an assumption that an ideal memory would keep everything. Even our vocabulary betrays the attitude, since we speak of 'losing' a memory as though it were a possession that had slipped out of a pocket. It is worth asking whether the assumption behind such talk is true.",
        "Consider what such a memory would be like to live with. Every time you parked your car, you would recall not only today's space but every space you had ever used, each with equal force. Every time you met a friend, you would be confronted with each version of her face across the years. The problem would not be a shortage of information but a surplus of it, because the memory you needed would be buried among the memories you did not. Some people who report unusually complete recall of their own lives describe the gift less as a pleasure than as a burden, a past that will not stay in the past.",
        "Seen in this light, much forgetting looks less like decay than like editing. Memories that are rarely used become harder to reach, while those that are used often stay accessible, and the effect is less a loss than a reordering of priorities. This is roughly what a sensible filing system would do: it would keep the files you consult near at hand and move the rest to the back, on the reasonable bet that the past use of a memory predicts its future use. Some evidence even suggests that recalling one memory actively suppresses its competitors, so that using your new phone number makes the old one fade faster.",
        "This argument has limits, and it is easy to push it too far, for not all forgetting is useful: the losses caused by brain injury or dementia are not editing but damage, and nothing said here makes them less painful. Nor does a system that is well designed on average serve every individual case: the name you cannot recall at an important meeting is a real cost, even if it is the price of a sensible policy. The point is only that the capacity to forget is part of what makes memory useful, not simply a flaw in it. A memory that never let go would be a worse memory, not a better one.",
    ],
    "Easy", "Everyday examples, a clear thesis and an explicit list of limits.",
    "R02A-adaptive-forgetting")

rcq("R02-A-04-1", "Main idea / primary purpose", "Easy",
    "The passage is primarily concerned with",
    "questioning the belief that an ideal memory would keep everything, by showing how forgetting helps memory work.",
    [("arguing that the fear of forgetting in old age is unfounded, since most memory loss turns out to be beneficial.",
      "Paragraph 4 says the losses of 'brain injury or dementia are not editing but damage', so the author does not dismiss fears of decline."),
     ("describing the biological processes through which memories that are seldom used gradually decay in the brain.",
      "The passage describes no biological processes and says forgetting looks 'less like decay than like editing'."),
     ("recommending that people give up memory aids so that their minds can edit stored information more efficiently.",
      "The passage makes no recommendation about memory aids; its conclusion is only that the capacity to forget is 'part of what makes memory useful'.")],
    "Paragraph 1 names the assumption 'that an ideal memory would keep everything', paragraphs 2 and 3 show why forgetting is useful, and paragraph 4 limits the claim. The key captures the target and the method.",
    "Overextending the thesis to all memory loss, which the final paragraph explicitly blocks.",
    "The thesis is announced in paragraph 1 and restated at the end.",
    cognitive="Understanding")

rcq("R02-A-04-2", "Structure / function", "Easy",
    "The example of recalling every parking space one has ever used serves to",
    "illustrate how holding every memory with equal force would bury the one that is needed.",
    [("show that people with very complete recall are unusually good at everyday tasks such as finding their cars.",
      "The passage says such recall is described 'less as a pleasure than as a burden'; the example shows a cost, not a skill."),
     ("suggest that memories of places are forgotten more readily than memories of faces.",
      "Places and faces are two parallel illustrations of the same point; the passage never compares how quickly they are forgotten."),
     ("demonstrate that most forgetting is caused by the brain running short of room in which to store information.",
      "Paragraph 2 says the problem 'would not be a shortage of information but a surplus of it', which is the reverse of a storage shortage.")],
    "Paragraph 2 uses the parking spaces to make the point that 'the memory you needed would be buried among the memories you did not'. The example illustrates the cost of total retention.",
    "Missing the point of the thought experiment and reading it as a claim about storage capacity.",
    "The function is stated two sentences after the example.",
    cognitive="Understanding")

rcq("R02-A-04-3", "Application / analogy", "Medium",
    "Which of the following is most closely analogous to the account of forgetting given in paragraph 3?",
    "A library that sends rarely borrowed books to a distant store, keeping much-borrowed titles on the open shelves.",
    [("A library that destroys a share of its old books at random each year to free space for new acquisitions.",
      "Paragraph 3 describes memories becoming 'harder to reach' according to how often they are used; random destruction is neither selective by use nor a matter of reduced access."),
     ("A library that shelves every book it has ever owned in the main hall, arranged strictly in order of arrival.",
      "This is the keep-everything memory of paragraph 2, where nothing is moved back, which the author presents as the problem rather than the solution."),
     ("A library that withdraws books from its shelves once readers report that they contain factual errors.",
      "Paragraph 3 makes accessibility depend on 'past use', not on accuracy; withdrawing books for error is a different principle.")],
    "Paragraph 3 compares memory to a filing system that keeps frequently consulted files near at hand and moves the rest 'to the back', betting that past use predicts future use. Moving rarely borrowed books to a store keeps them but makes them harder to reach, on the same bet.",
    "Picking the random-destruction library because it involves losing books, which seems like forgetting, while ignoring that the forgetting in the passage is selective by use and a matter of reduced access rather than loss.",
    "Two features must both match: selection by frequency of use, and reduced access rather than destruction.",
    cognitive="Application")

rcq("R02-A-04-4", "Inference", "Medium",
    "The author would most likely agree with which of the following?",
    "Failing to recall a name at an important moment can be a genuine loss even when the forgetting comes from a sound design.",
    [("Because forgetting is the price of a sensible policy, the cost of any particular memory lapse is more apparent than real.",
      "Paragraph 4 calls the forgotten name 'a real cost, even if it is the price of a sensible policy', which contradicts the claim that such costs are only apparent."),
     ("The memory losses caused by dementia are best understood as an extreme form of the useful editing that all memories perform.",
      "Paragraph 4 says such losses 'are not editing but damage', so the author explicitly rejects this view."),
     ("A memory that held on to everything would be more useful, though less comfortable to live with, than the one we have.",
      "The last sentence says 'A memory that never let go would be a worse memory, not a better one'; the author denies that total retention is more useful.")],
    "Paragraph 4 says a system 'well designed on average' does not serve every case, and that the forgotten name is 'a real cost, even if it is the price of a sensible policy'. The key restates this.",
    "Assuming that defending forgetting as useful commits the author to calling every lapse harmless.",
    "The tempting distractor draws a natural but wrong conclusion from the 'sensible policy' phrase.",
    cognitive="Analysis")

# =====================================================================================
# R02-A-05  Expert perceptual chunking (Medium)
# =====================================================================================
passage("R02-A-05", T,
    "Much expertise is trained perception rather than superior memory or reasoning, which makes it fast and usually right but brittle outside the cases that trained it.",
    [
        "A familiar demonstration from the study of chess runs as follows. A position from a real game is shown for a few seconds and then removed, and players are asked to reconstruct it on an empty board. Strong players replace most of the pieces correctly, while novices manage only a handful, and the obvious conclusion is that strong players simply have better memories. The less obvious and more instructive part of the demonstration comes next. When the same pieces are scattered at random, in arrangements that could never arise in play, the masters' advantage largely disappears, and they do little better than beginners.",
        "What the masters possess, then, is not a larger store for holding pieces but a different way of seeing them. Years of play have given them a vocabulary of familiar configurations, a castled king with its pawns in front, a bishop aimed down a long diagonal, and they take in a position as a few such units rather than as two dozen separate pieces. A novice looking at the same board sees wood on squares. The master sees a situation, and often, before any conscious calculation has begun, a sense of what the situation calls for.",
        "Similar observations have been made in fields as different as radiology, birdwatching and the reading of geological maps, where experienced specialists frequently report knowing that something is wrong with an image within a second or two, before they can say what it is. The birdwatcher who names a distant species from the way it flies, long before any marking can be made out, is drawing on the same resource. It is tempting to describe this as intuition, as though it were a mysterious faculty standing apart from knowledge. It is better described as knowledge that has been absorbed into perception, so that it no longer needs to be consulted, because it shapes what is seen in the first place.",
        "This view has practical consequences, though they are easily overstated. If expertise lies partly in the eye, it cannot be fully transmitted by rules and explanations; the learner has to look at a great many cases, with feedback, until the patterns become visible. But perception is not the whole of expertise. Masters still calculate, and careful specialists still check their first impressions, because a pattern that is recognised instantly can also be misrecognised instantly. The trained eye is fast and usually right within the territory that trained it, and that qualification matters: presented with a case unlike those it has learned from, its speed becomes a liability rather than an asset.",
    ],
    "Medium", "A case study generalised across fields, with a concession that limits the thesis; the argument is clear but the final qualification must be tracked.",
    "R02A-expert-perceptual-chunking")

rcq("R02-A-05-1", "Specific detail", "Easy",
    "According to the passage, when chess pieces are arranged at random,",
    "strong players reconstruct the positions little better than beginners do.",
    [("strong players recall them more accurately than real positions, since no familiar habits mislead them.",
      "Paragraph 1 says the masters' advantage 'largely disappears'; nothing suggests they do better with random positions than with real ones."),
     ("beginners outperform masters, because the masters try to force the pieces into familiar patterns.",
      "The passage says masters 'do little better than beginners', not worse, and gives no account of masters imposing patterns."),
     ("neither group can reconstruct a single piece of the position after it has been removed.",
      "The passage says the advantage disappears, not that everyone fails completely; novices manage 'a handful' even of real positions.")],
    "The last sentence of paragraph 1 says that with random arrangements 'the masters' advantage largely disappears, and they do little better than beginners'.",
    "Over-reading the result into a reversal of the masters' advantage.",
    "The answer is a close paraphrase of one sentence.",
    cognitive="Recall")

rcq("R02-A-05-2", "Inference", "Medium",
    "The author calls the random-position result 'more instructive' than the first result most probably because it",
    "rules out the explanation that masters simply have a greater capacity to store pieces in memory.",
    [("shows that beginners could become strong players more quickly by studying random positions instead of real games.",
      "The passage draws no lesson about training on random positions; paragraph 4 says learners need 'a great many cases', which in context means real ones."),
     ("proves that skill at chess depends entirely on perception and not at all on calculation.",
      "Paragraph 4 says 'perception is not the whole of expertise' and that 'Masters still calculate', so the word entirely contradicts the author."),
     ("reveals that the memory of strong players fails when they are given only a few seconds to look at a board.",
      "Masters are given the same few seconds in both conditions and succeed with real positions; the time limit is not what changes.")],
    "If masters merely had better memories, they should excel with any arrangement. Their advantage vanishing with random positions shows the advantage depends on meaningful configurations, which paragraph 2 makes explicit: 'not a larger store for holding pieces but a different way of seeing them'.",
    "Choosing the option claiming skill rests entirely on perception, which pushes the inference beyond what the author allows.",
    "The key is an inference from the contrast of two results; one distractor overstates the conclusion.",
    cognitive="Analysis")

rcq("R02-A-05-3", "Meaning in context", "Easy",
    "In paragraph 3, 'knowledge that has been absorbed into perception' refers to",
    "learning that now shapes what the specialist sees, without having to be called up step by step.",
    [("a mysterious faculty that works independently of anything the specialist has studied or practised.",
      "This is the account of intuition that paragraph 3 calls 'tempting' and then replaces; the author denies that it stands apart from knowledge."),
     ("rules that the specialist silently recites to herself while she looks over an image or a board.",
      "The passage says the knowledge 'no longer needs to be consulted', which excludes reciting rules."),
     ("facts the specialist has forgotten that resurface without warning when she is under pressure.",
      "Nothing in the passage concerns forgotten facts or pressure; the knowledge is in constant use, shaping 'what is seen in the first place'.")],
    "The phrase is glossed in the same sentence: the knowledge 'no longer needs to be consulted, because it shapes what is seen in the first place'.",
    "Confusing the author's view with the view of intuition as a mysterious faculty the author sets aside.",
    "The meaning is glossed in the rest of the sentence.",
    cognitive="Understanding")

rcq("R02-A-05-4", "Application / analogy", "Medium",
    "On the passage's account, an experienced radiologist shown an image of a rare condition unlike any she has studied would be most at risk of",
    "forming a quick and confident first impression that turns out to be wrong.",
    [("failing to form any impression of the image until she had worked through written diagnostic rules.",
      "The passage says the trained eye responds 'within a second or two'; nothing suggests it falls silent on unfamiliar cases, and the risk named is speed, not hesitation."),
     ("performing exactly as a novice would, since her skill rests only on a larger memory for images.",
      "Paragraph 2 rejects the idea that expertise is 'a larger store', and the passage says the risk is misrecognition, not a return to novice performance."),
     ("recognising the condition at once, because trained perception carries over to every image in her field.",
      "Paragraph 4 limits the trained eye to 'the territory that trained it'; a case unlike those it learned from is exactly where it is said to fail.")],
    "Paragraph 4 says a pattern 'recognised instantly can also be misrecognised instantly' and that with 'a case unlike those it has learned from' the trained eye's 'speed becomes a liability rather than an asset'. A rare, unfamiliar image is such a case.",
    "Assuming expertise transfers across a whole field, ignoring the limit the author sets in the final sentence.",
    "Applying the final qualification to a new case; the tempting distractor uses the radiology example of paragraph 3.",
    cognitive="Application")

# =====================================================================================
# R02-A-06  Subjective duration of time (Medium)
# =====================================================================================
passage("R02-A-06", T,
    "We judge duration in two ways, by attention while it passes and by memory afterwards, so there is no single answer to how long something felt.",
    [
        "There is a small puzzle about time that most people have noticed without ever stating it. A week spent travelling somewhere new seems to vanish while it is happening, so that there is never enough of it; yet once the traveller is home, the same week looks enormous, crowded with places and faces, as if it had lasted a month. A week at a familiar desk behaves in the opposite way. It drags while it is lived, each afternoon longer than the last, and then collapses in memory into a single grey item that seems to have taken no time at all.",
        "The puzzle dissolves once we accept that we judge duration in two quite different ways. While an interval is passing, our sense of its length depends largely on how much attention we pay to time itself: boredom draws attention to the clock and stretches the hour, while absorption draws it away and the hour shrinks. Looking back, however, we have no clock to consult. We estimate how long a period lasted from what it left behind, and a period that left many distinct memories is judged to have been long. Novelty therefore works in opposite directions on the two judgements, shortening the interval as experienced and lengthening it as remembered.",
        "This distinction sheds light on a complaint that becomes common in middle age, that the years go faster than they used to. The complaint is almost always retrospective. Few people find that a particular afternoon passes faster at fifty than at fifteen; what they find is that last year, viewed as a whole, seems to have been brief. If remembered duration tracks the number of distinct memories, the explanation is not far to seek, since adult life is more routine than youth, with fewer firsts, and a year of repeated weeks leaves less behind to measure it by.",
        "The account is persuasive, but it should be held loosely. It is unlikely that a single factor explains how time seems at every age, and other changes, in health, in responsibility, in how far ahead people habitually plan, probably play a part. Still less does it follow, as some cheerful advice suggests, that one can lengthen a life simply by filling it with novelty. A crowded year may indeed look longer in retrospect, but it will feel shorter while it is lived, and there is no obvious reason to prefer one of these measures over the other. What the distinction teaches is not a technique for buying time but a caution against speaking of how long something 'really' felt, as though there were only one answer.",
    ],
    "Medium", "A puzzle resolved by a distinction, applied to a familiar complaint and then hedged; the two kinds of judgement must be kept apart throughout.",
    "R02A-subjective-duration-of-time")

rcq("R02-A-06-1", "Specific detail", "Easy",
    "According to the passage, while an interval is passing, the sense of how long it is lasting depends largely on",
    "how much attention is being paid to the passing of time itself.",
    [("how many distinct memories the events of the interval are laying down.",
      "Paragraph 2 makes the number of distinct memories the basis of the judgement made 'Looking back', not of the judgement made while the interval passes."),
     ("how pleasant or unpleasant the person finds the activity that fills the interval.",
      "The passage contrasts boredom with absorption as states of attention; pleasantness as such is never given as the factor."),
     ("how old the person is and how routine the rest of his life has become.",
      "Age and routine are used in paragraph 3 to explain the retrospective complaint about years, not the felt length of an interval in progress.")],
    "Paragraph 2: 'While an interval is passing, our sense of its length depends largely on how much attention we pay to time itself'.",
    "Mixing up the two kinds of judgement and choosing the memory-based factor.",
    "The answer is stated in one sentence; the main distractor belongs to the other judgement.",
    cognitive="Recall")

rcq("R02-A-06-2", "Inference", "Medium",
    "The passage suggests that the middle-aged complaint that the years go faster",
    "concerns how a past year looks as a whole, not how its hours feel while they are being lived.",
    [("shows that the felt passage of a single afternoon speeds up steadily as people grow older.",
      "Paragraph 3 says 'Few people find that a particular afternoon passes faster at fifty than at fifteen', which contradicts this."),
     ("is mistaken, because older people in fact keep more distinct memories of each year than young people do.",
      "The passage suggests the reverse: adult life has 'fewer firsts' and a routine year 'leaves less behind', and it does not call the complaint mistaken."),
     ("arises because adults pay closer attention to clocks and calendars than young people usually do.",
      "Attention to time governs the judgement made while an interval passes; the passage explains the complaint by remembered duration, not by attention.")],
    "Paragraph 3 says 'The complaint is almost always retrospective' and contrasts the unchanged afternoon with last year 'viewed as a whole'. The complaint is about remembered duration.",
    "Applying the attention mechanism, which belongs to experienced duration, to a retrospective complaint.",
    "The attention distractor is tempting because attention is the passage's first mechanism.",
    cognitive="Analysis")

rcq("R02-A-06-3", "Meaning in context", "Medium",
    "In the last sentence, the quotation marks around 'really' serve to",
    "cast doubt on the idea that there is one true fact about how long an experience felt.",
    [("signal the author's view that remembered duration is truer than the duration felt at the time.",
      "Paragraph 4 says 'there is no obvious reason to prefer one of these measures over the other', so the author ranks neither as truer."),
     ("express scorn for people who believe that novelty can be used to lengthen their lives.",
      "The author does question that advice in the preceding sentences, but the marked word concerns 'how long something' felt, and the sentence explains it with 'as though there were only one answer'."),
     ("show that the word is quoted from the cheerful advice that the author criticises earlier in the paragraph.",
      "Nothing indicates that the advice used this word; the marks flag a doubtful assumption in ordinary speech, explained by 'as though there were only one answer'.")],
    "The sentence ends 'as though there were only one answer'. Having shown that duration is judged in two ways that can disagree, the author marks 'really' to question the assumption of a single true felt duration.",
    "Linking the marks to the nearby criticism of cheerful advice rather than to the clause that explains them.",
    "Two distractors draw on genuine content of the paragraph and must be separated from what the marks themselves do.",
    cognitive="Understanding")

rcq("R02-A-06-4", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most weaken the explanation offered in paragraph 3 for why the years seem to pass faster in middle age?",
    "Adults whose lives remain as full of first experiences as in youth report the same speeding up of the years as adults with routine lives.",
    [("Middle-aged adults report that individual afternoons pass at much the same rate as they did when they were adolescents.",
      "This matches what paragraph 3 says about afternoons and supports treating the complaint as retrospective, so it does not weaken the explanation."),
     ("Travellers returning from a varied holiday judge it to have lasted longer than a routine week at work of the same length.",
      "This illustrates the principle that distinct memories lengthen remembered duration, on which the explanation rests, so it strengthens rather than weakens it."),
     ("Middle-aged adults habitually plan further ahead than adolescents do, and many of them say that they spend more of their time thinking about the future.",
      "Paragraph 4 already lists 'how far ahead people habitually plan' among changes that 'probably play a part'; showing that another factor is present does not show that routine plays no role.")],
    "The explanation is that routine adult life, with 'fewer firsts', leaves fewer distinct memories, so years seem brief. If adults with as many firsts as the young feel the same speeding up, the proposed cause is absent while the effect remains, which undercuts it directly.",
    "Choosing the planning option because it names a rival factor, without noticing that the passage already accepts several factors and that a co-existing cause does not remove this one.",
    "Requires seeing that only a case with the cause absent and the effect present tests the explanation; the rival-factor distractor is the classic trap.",
    cognitive="Analysis", exams=DX)

# =====================================================================================
# R02-A-07  Mind wandering costs and uses (Difficult, 5 questions)
# =====================================================================================
passage("R02-A-07", T,
    "The rival verdicts that mind wandering is a costly lapse or a useful activity come from studying different occasions; its value depends on context and on the wanderer's awareness.",
    [
        "For much of its short history as a subject of research, the wandering mind was treated as noise. Participants in experiments were supposed to attend to the task in front of them, and the moments when their thoughts drifted to lunch or to an argument with a sibling were lapses to be minimised or averaged away. When researchers began to study these lapses directly, by interrupting people at random moments in their day and asking what they had been thinking about, the first surprise was how common the lapses were. The method had the merit of catching thought in the act, before the thinker had time to tidy it into a more respectable account of where her attention had been. A considerable part of waking thought, it turned out, is about something other than what the thinker is doing.",
        "Two quite different interpretations of this finding have since competed. On the first, mind wandering is a failure of control: it is associated with errors in reading and driving, with poorer performance on tests of sustained attention and, in some studies, with lower reported mood at the moment of wandering. The mind that drifts is the mind that has lost its grip, and the remedy is training in attention. On the second interpretation, these costs are real but partial, and they ignore what the drifting mind is actually doing. Much wandering thought is directed at the future, at plans, rehearsals of conversations and the weighing of unfinished business, and some of the solutions that arrive unbidden in the shower or on a walk may owe something to the same process. On this view the mind that drifts is not idle but working on a different problem, one it has judged, so to speak, more pressing than the task at hand.",
        "Each interpretation, I think, makes the same mistake, which is to speak of mind wandering as though it were one thing with one value. The evidence for costs comes largely from tasks that demand continuous attention, where any lapse is damaging by design, while the evidence for benefits comes largely from situations in which the external task is undemanding, so that little is lost by leaving it. Tasks of the first kind are chosen precisely because they make lapses easy to count, and situations of the second kind because they leave room for thought. It is hardly surprising that the two literatures reach different verdicts, since they are, for the most part, looking at different occasions. Nor does the link with low mood settle the matter. A person who is worried is likely both to feel worse and to find his thoughts pulled towards his worries, so that wandering may be as much a symptom of unhappiness as its cause.",
        "A more useful question is not whether the mind should wander but when, and with what awareness. Drifting during a lecture one has chosen to attend is a cost; drifting while washing dishes may be a free opportunity to think. There also seems to be a real difference between thought that slips away unnoticed and thought that is allowed to roam, as when a person deliberately sets a problem aside and lets her attention go where it will. The second kind is under a loose but genuine control, since the person can notice it and call it back. If this is right, the goal of training attention should not be to abolish wandering, an aim that is probably unachievable and possibly harmful, but to make wandering more visible to the wanderer, so that she can tell which kind of occasion she is in.",
    ],
    "Difficult", "Two rival views are reported at length before the author's own position, which rejects a shared assumption of both; the stance must be kept apart from the views reported.",
    "R02A-mind-wandering-costs-and-uses", exams=DX)

rcq("R02-A-07-1", "Main idea / primary purpose", "Difficult",
    "Which of the following best expresses the main point of the passage?",
    "The opposed verdicts on mind wandering largely reflect the different occasions studied; its worth depends on when it occurs and whether it is noticed.",
    [("Mind wandering is chiefly productive work on plans and unfinished problems, and its costs have been exaggerated by narrowly designed experiments.",
      "This is the second interpretation reported in paragraph 2; the author says 'Each interpretation' makes the same mistake, and accepts that the costs on demanding tasks are real."),
     ("Mind wandering is better understood as a symptom of unhappiness than as its cause, contrary to what researchers at first believed.",
      "Paragraph 3 says only that wandering 'may be as much a symptom of unhappiness as its cause', a point used to unsettle one argument; it is a detail, and the option hardens it into a claim the author does not make."),
     ("Training in attention should be abandoned, since every attempt to suppress the wandering mind is futile and does real harm.",
      "Paragraph 4 redirects training rather than abandoning it, aiming 'to make wandering more visible to the wanderer', and calls abolition only 'probably unachievable and possibly harmful'.")],
    "Paragraph 3 states the author's thesis: both interpretations treat wandering 'as though it were one thing with one value', when their evidence comes from 'different occasions'. Paragraph 4 replaces the question with 'not whether the mind should wander but when, and with what awareness'. The key combines the diagnosis and the proposal.",
    "Taking the second, more sympathetic interpretation in paragraph 2 for the author's own view.",
    "The longest paragraph presents a view the author rejects; the main point requires separating reported views from the author's and combining paragraphs 3 and 4.",
    cognitive="Analysis", exams=DX)

rcq("R02-A-07-2", "Specific detail", "Easy",
    "According to the passage, researchers began to study mind wandering directly by",
    "interrupting people at random moments and asking what they had been thinking about.",
    [("measuring the errors people made while reading or driving under laboratory conditions.",
      "Errors in reading and driving are mentioned in paragraph 2 as findings linked to wandering, not as the method that first studied wandering directly."),
     ("asking people at the end of each day to estimate how often their minds had drifted.",
      "The passage describes interruptions at random moments, not end-of-day estimates; this method is never mentioned."),
     ("recording the solutions that came to people unbidden while they were in the shower or out walking.",
      "Unbidden solutions appear in paragraph 2 as part of the case for the benefits of wandering, not as a research method.")],
    "Paragraph 1: 'When researchers began to study these lapses directly, by interrupting people at random moments in their day and asking what they had been thinking about'.",
    "Picking a detail from paragraph 2 that concerns findings rather than method.",
    "Located in one sentence of paragraph 1.",
    cognitive="Recall")

rcq("R02-A-07-3", "Inference", "Medium",
    "The author's remark about a person who is worried implies that",
    "a link between mind wandering and low mood does not by itself show that wandering makes people unhappy.",
    [("mind wandering is always produced by unhappiness and never contributes to it in any way.",
      "The author says wandering 'may be as much a symptom of unhappiness as its cause', which allows that it can also be a cause; the words always and never go beyond this."),
     ("worried people perform better than others on tasks that demand continuous attention.",
      "Nothing in the passage compares the task performance of worried and untroubled people."),
     ("the studies that linked wandering with low mood were badly conducted and ought to be set aside.",
      "The author accepts the association, reported 'in some studies', and questions only the direction of cause, not the quality of the research.")],
    "Paragraph 3 introduces the example with 'Nor does the link with low mood settle the matter': worry could produce both the bad mood and the wandering. The point is that the correlation leaves the direction of cause open.",
    "Turning 'may be as much a symptom ... as its cause' into a claim that wandering is only a symptom.",
    "Requires reading the hedge exactly; the main distractor overstates it.",
    cognitive="Analysis")

rcq("R02-A-07-4", "Application / analogy", "Medium",
    "Which of the following outcomes of a course in attention training would the author regard as most successful?",
    "A trainee still lets her thoughts drift while gardening but now notices quickly when they drift in a meeting she needs to follow.",
    [("A trainee no longer lets her thoughts drift on any occasion, whether at work, at lectures or at home.",
      "Paragraph 4 says the goal 'should not be to abolish wandering', calling that aim 'probably unachievable and possibly harmful'."),
     ("A trainee now lets her thoughts roam freely during important meetings, on the chance that unbidden solutions may come to her there.",
      "Paragraph 4 treats drifting during a demanding event one has chosen to attend as 'a cost'; a meeting she must follow is such an occasion."),
     ("A trainee feels happier than before because she now spends more of her waking time thinking about her future plans.",
      "The author's goal for training is awareness of 'which kind of occasion she is in'; mood and time spent planning are not the measure of success the author proposes.")],
    "Paragraph 4 sets the goal of training as making wandering 'more visible to the wanderer, so that she can tell which kind of occasion she is in'. The trainee who drifts freely in an undemanding activity but catches herself in a demanding one fits that goal exactly.",
    "Choosing the trainee who never drifts, which matches the first interpretation's remedy but not the author's.",
    "Each distractor matches one reported view or one detail; only the key fits the author's stated goal.",
    cognitive="Application")

rcq("R02-A-07-5", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most weaken the author's claim that the two bodies of research 'are, for the most part, looking at different occasions'?",
    "A survey of the research finds that studies reporting costs and studies reporting benefits mostly used tasks of very similar difficulty.",
    [("Studies reporting costs were run mainly in laboratories, while studies reporting benefits were often run in everyday settings.",
      "This describes another difference in the occasions studied, so if anything it supports the claim that the two literatures look at different situations."),
     ("People report that their minds wander more often when they are worried than when they are content.",
      "This concerns the link with mood discussed later in paragraph 3, not where the evidence for costs and benefits comes from."),
     ("Errors made while driving are more dangerous than errors made while reading, so lapses at the wheel matter more.",
      "This compares the seriousness of two costs and says nothing about whether the cost and benefit studies examined different kinds of task.")],
    "The author's claim is that cost studies used demanding tasks and benefit studies used undemanding ones, so their verdicts differ because their occasions differ. If both used tasks of similar difficulty, the difference in verdicts could not be explained this way, and the claim fails.",
    "Picking the laboratory option because it mentions the two literatures, without seeing that it adds a further difference and so fits the claim.",
    "The strongest distractor names a methodological contrast that sounds like a challenge but actually supports the author.",
    cognitive="Analysis", exams=DX)

# =====================================================================================
# R02-A-08  Retrieval practice and the testing effect (Difficult, 5 questions)
# =====================================================================================
passage("R02-A-08", T,
    "Retrieving material strengthens memory more than restudying it, though learners misjudge this, and the benefit lies in low-stakes recall with feedback rather than in more examinations.",
    [
        "In most schools a test is understood as a thermometer. It is applied at the end of a period of learning to find out how much has been learned, and like a thermometer it is supposed to leave the thing it measures unchanged. The understanding is so familiar that it seldom occurs to anyone that it might be false. Yet one of the more robust findings in the psychology of memory is that the act of retrieving something from memory is not a neutral reading: it changes the memory, and generally strengthens it, so that material which has been recalled once is more likely to be recalled again than material which has merely been seen again.",
        "The contrast is clearest when the two activities are set against each other. Suppose two groups of students study the same passage, after which one group rereads it while the other closes the book and writes down whatever it can remember. The design holds constant both the material and the time spent on it, so that the only difference between the groups is whether they looked at the passage again or tried to bring it back unaided. Tested a few minutes later, the rereaders often do as well or better; tested a week later, the group that practised recall tends to remember considerably more. The advantage of retrieval, in other words, is easily hidden by the timing of the measurement, which may be one reason why it was overlooked for so long by teachers and students alike.",
        "What is more striking is how little the students themselves sense any of this. Asked to predict their own performance, rereaders tend to be the more confident group. Rereading produces a feeling of fluency, in which the sentences are familiar and slide past easily, and ease of processing is readily mistaken for mastery. Attempting recall produces the opposite feeling, since it is effortful, it exposes gaps and it is often unpleasant, which is presumably why students left to themselves so rarely choose it. Teachers are not immune to the same illusion, since a class that has just reread its notes looks, and feels, better prepared than one that has just struggled to recall them. The method that feels like learning and the method that produces it are, at least here, not the same, and the lesson generalises uncomfortably: a learner's own sense of how well a session went is an unreliable guide to how much it achieved.",
        "It would be easy to draw from all this a crude conclusion, that schools should simply test more, but the finding does not support it. What strengthens memory is the effort of retrieval, not the apparatus of examination, and the apparatus can work against the effort. A high-stakes test that provokes anxiety, or that is followed by no feedback, may teach students little except to fear tests, and a wrong answer recalled confidently and never corrected may itself be strengthened. The useful practice is humbler than the word 'test' suggests: it consists of frequent, low-stakes attempts to recall, each followed by a chance to check, built into ordinary study. None of this requires abolishing examinations, which serve purposes of certification that have little to do with memory; it requires only that they not be mistaken for the whole of what testing can do. Understood in this way, the thermometer turns out to be one of the more effective means of raising the temperature it was meant only to record.",
    ],
    "Difficult", "Dense argument that overturns a common belief, adds a finding about self-assessment and then blocks a crude policy conclusion; several fine distinctions are tested.",
    "R02A-retrieval-practice-testing-effect", exams=DX)

rcq("R02-A-08-1", "Structure / function", "Easy",
    "The comparison of a test to a thermometer in paragraph 1 serves mainly to",
    "capture the common assumption that testing records learning without changing it, which the passage goes on to reject.",
    [("suggest that tests, like thermometers, are precise instruments that schools ought to use more often.",
      "Paragraph 4 says the finding does not support the conclusion that 'schools should simply test more'; the image is introduced in order to be challenged."),
     ("illustrate how a student's anxiety rises during an examination much as a temperature rises during a fever.",
      "The passage uses the thermometer for an instrument that measures without altering, not for rising anxiety; anxiety is a separate point in paragraph 4."),
     ("show that the effects of a test can be measured accurately only when a week has passed since it was taken.",
      "The one-week interval belongs to the experiment in paragraph 2 and has nothing to do with the thermometer image.")],
    "Paragraph 1 says a test, like a thermometer, 'is supposed to leave the thing it measures unchanged', then calls this understanding possibly 'false', since retrieval 'changes the memory'. The image states the belief under attack, and the final sentence turns it around.",
    "Reading the image as endorsing tests because the passage ends by praising a kind of testing.",
    "The function is stated in the sentence that introduces the image.",
    cognitive="Understanding")

rcq("R02-A-08-2", "Inference", "Medium",
    "The passage suggests that the advantage of retrieval practice was long overlooked partly because",
    "measurements taken soon after study could make rereading look at least as effective as recall.",
    [("students who practised recall concealed their gains from researchers because they were anxious about being tested.",
      "Nothing in the passage says students concealed anything; anxiety appears only in paragraph 4 as a risk of high-stakes tests."),
     ("rereading produces stronger memories in the short run, which later decay into confidently held errors.",
      "The passage says rereaders 'often do as well or better' at first; it never says their memories turn into errors, and confident errors are linked in paragraph 4 to uncorrected recall."),
     ("researchers regarded tests as too unpleasant to be worth studying as a method of learning.",
      "The unpleasantness of recall is offered in paragraph 3 to explain why students avoid it, not why researchers overlooked it.")],
    "Paragraph 2 says that after a few minutes 'the rereaders often do as well or better' and that the advantage of retrieval 'is easily hidden by the timing of the measurement, which may be one reason why it was overlooked'.",
    "Attaching the unpleasantness of recall, which explains students' choices, to the question of why the effect was overlooked.",
    "Distractors combine real passage elements in wrong causal roles.",
    cognitive="Analysis")

rcq("R02-A-08-3", "Application / analogy", "Medium",
    "Which of the following study routines best matches the practice the author recommends?",
    "After each chapter, a student shuts the book, writes out what she remembers and then checks her account against the text.",
    [("A student reads each chapter three times over, until every sentence feels familiar and slides past without effort.",
      "Paragraph 3 says this feeling of fluency 'is readily mistaken for mastery'; rereading is the method the passage contrasts unfavourably with recall."),
     ("A student sits one long, formally graded examination at the end of term, whose marked scripts are never returned to her.",
      "Paragraph 4 warns that a high-stakes test 'followed by no feedback' may teach little; the recommended practice is 'frequent, low-stakes' recall."),
     ("A student answers practice questions from memory every evening but never looks up whether her answers were right.",
      "Paragraph 4 requires each attempt to be 'followed by a chance to check', and warns that an uncorrected wrong answer 'may itself be strengthened'.")],
    "Paragraph 4 recommends 'frequent, low-stakes attempts to recall, each followed by a chance to check, built into ordinary study'. Writing out what one remembers after each chapter and checking it meets every element.",
    "Choosing the daily practice questions, which satisfy frequency and recall but omit the check the author insists on.",
    "One distractor meets two of the three conditions; the solver must hold all three.",
    cognitive="Application")

rcq("R02-A-08-4", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most weaken the author's claim that what strengthens memory is 'the effort of retrieval, not the apparatus of examination'?",
    "Answering recall questions improved memory a week later only when done under formal examination conditions, and not when done in an informal, ungraded session.",
    [("Students who sat a formal, high-stakes examination reported feeling far more anxious than students who practised recall at home with their books closed.",
      "This fits paragraph 4's warning that high-stakes tests provoke anxiety and says nothing about which element produces the memory benefit."),
     ("Students who received feedback after each attempt at recall remembered more a week later than students who attempted the same recall without any feedback.",
      "This agrees with the author's insistence on 'a chance to check'; it does not suggest that formal examination conditions are what matters."),
     ("Students who reread a passage felt more confident about a coming test than those who practised recall, although a week later they remembered less of it.",
      "This restates the finding of paragraph 3 about confidence and fluency; it is consistent with the author and irrelevant to the effort versus apparatus claim.")],
    "The claim credits the effort of recalling, not the formal trappings of a test. If the same recall effort helps only when done under formal examination conditions and not in an ungraded session, the apparatus is doing the work, which directly contradicts the claim.",
    "Choosing the feedback option because it adds a condition to the benefit, without noticing that the author already requires feedback.",
    "Every distractor is consistent with the passage; only the key separates effort from apparatus and comes out against the author.",
    cognitive="Analysis", exams=DX)

rcq("R02-A-08-5", "Except / not supported", "Difficult",
    "The author would agree with each of the following statements EXCEPT:",
    "Attempting to recall material benefits memory only when the learner succeeds in producing the right answer.",
    [("A learner's confidence at the end of a study session can be a misleading guide to what the session achieved.",
      "Paragraph 3 says 'a learner's own sense of how well a session went is an unreliable guide to how much it achieved', so the author agrees."),
     ("Students who are left to choose their own method of study will seldom choose to practise recall.",
      "Paragraph 3 says recall is effortful and unpleasant, 'which is presumably why students left to themselves so rarely choose it', so the author agrees."),
     ("The benefit of retrieval practice may fail to appear in a test given only a few minutes after study.",
      "Paragraph 2 says that tested 'a few minutes later, the rereaders often do as well or better', so the author agrees.")],
    "Paragraph 4 says 'What strengthens memory is the effort of retrieval', not its success, and recommends 'attempts to recall, each followed by a chance to check', which presupposes that attempts may fail and still be worth making; paragraph 3 even counts it a feature of recall that 'it exposes gaps'. Paragraph 4 also says a wrong answer recalled confidently 'may itself be strengthened', so retrieval acts on whatever is retrieved. The statement that recall helps only when it succeeds conflicts with all of this.",
    "Treating the unsupported statement as one the author would accept because it sounds like a sensible caution, without connecting it to the claim that the effort of retrieval, not its success, does the work.",
    "The unsupported statement is plausible in itself and can be rejected only by linking it to one clause of paragraph 4.",
    cognitive="Analysis", exams=DX)
