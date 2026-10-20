import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

# Worked examples of every item kind. Their subjects (maintenance versus invention, ocean
# soundings, gaming of hospital metrics, bee colour learning, the redefinition of the second)
# are RESERVED: do not reuse them.

# ------------------------------------------------------------------ RC (one passage, 4 questions)
passage("S-RC-01", "History of technology", "Histories of technology that centre on invention misdescribe how technologies matter, because they ignore maintenance.",
    [
        "Histories of technology are usually written as histories of invention. The decisive moment, in these accounts, is the one in which something new appears: the first steam engine that pays its way, the first vaccine, the first network that links two computers. What happens afterwards, the decades in which the new thing is repaired, adapted, patched and kept running, is treated as an epilogue, interesting chiefly to the people who were paid to do it. This emphasis is not innocent, and it is rarely examined. It flatters a particular picture of where value comes from, one in which a small number of original minds create and everyone else merely copies or tends.",
        "Consider what the picture leaves out. For most of the twentieth century the majority of engineers did not design new machines; they maintained, modified and extended existing ones. Railways, water systems and telephone exchanges remained useful not because they were well conceived at the outset but because generations of workers learned their peculiarities and compensated for them. Much of what we call reliability is accumulated care, and care of this kind leaves few documents. A patent records a claim of novelty; there is no comparable instrument for recording that a bridge did not fall down.",
        "The bias toward novelty also distorts how societies spend. Funding bodies reward proposals that promise something unprecedented, and politicians would rather open a new hospital wing than replace the wiring in an old one, because ribbons can be cut only once. The predictable result is infrastructure that is built with enthusiasm and then allowed to decay, until its failure becomes dramatic enough to count, at last, as news. By then the cost of repair is usually far higher than the cost of the care that was skipped.",
        "None of this means that invention is overrated in itself. The point is rather that innovation and maintenance are not rival activities but phases of a single process, and that a history which attends only to the first phase will misdescribe even that. Many celebrated inventions succeeded because they were designed to be repairable by ordinary hands; many failed because they were not. To see this, the historian has to look away from the moment of origin and toward the long, unglamorous middle of a technology's life, where most of its consequences are actually produced.",
    ],
    "Medium", "Abstract argument with a concession in the last paragraph; vocabulary is moderate.",
    "SRC-maintenance-vs-invention")

rcq("S-RC-01-1", "Main idea / primary purpose", "Medium",
    "The primary purpose of the passage is to",
    "argue that invention-centred histories misdescribe technologies by neglecting the long work of keeping them running.",
    [("show that most of the celebrated inventions of the last two centuries failed because ordinary users could not repair them.",
      "Paragraph 4 says many inventions failed for this reason, not most, and the point supports the thesis rather than being its purpose."),
     ("propose that funding bodies should stop rewarding novel proposals and pay for upkeep instead.",
      "Paragraph 3 describes how the bias distorts spending but proposes no policy; the option takes one illustration for the purpose."),
     ("establish that maintenance is more valuable than invention and deserves greater prestige.",
      "Paragraph 4 explicitly denies that invention is overrated and calls the two phases of one process, so ranking them contradicts the author.")],
    "Paragraph 1 identifies the invention-centred bias, paragraphs 2 and 3 show what it leaves out and what it costs, and paragraph 4 concludes that a history attending only to origins 'will misdescribe even that'. The purpose is to correct how technological history is told, by bringing in maintenance.",
    "Choosing a supporting detail, or overstating the author's position into a ranking of maintenance above invention.",
    "Two options borrow real details from the passage; the key requires holding the whole argument and the concession together.",
    cognitive="Analysis")

rcq("S-RC-01-2", "Inference", "Easy",
    "The remark that 'ribbons can be cut only once' (paragraph 3) suggests that",
    "spending favours projects that offer a single visible occasion for credit, which routine upkeep never provides.",
    [("politicians tend to avoid funding hospitals because the opening ceremonies for new buildings are expensive to arrange.",
      "The passage says politicians prefer opening a new wing, so they fund hospitals readily; the cost of ceremonies is never mentioned."),
     ("new infrastructure is usually built so poorly that it cannot be repaired once it opens.",
      "The passage blames later neglect, not poor construction: infrastructure is 'built with enthusiasm and then allowed to decay'."),
     ("voters ignore the state of public buildings except during the week a building opens.",
      "Voters' attention is not discussed; the passage says only that failure eventually becomes news, which is a different claim.")],
    "A ribbon-cutting is a one-time public moment of credit available for a new building but not for rewiring an old one. Paragraph 3 uses it to explain why politicians prefer new projects to maintenance.",
    "Reading the image literally (ceremony costs) instead of as a point about visible credit.",
    "The figurative phrase is explained by the sentence it sits in.", cognitive="Understanding")

rcq("S-RC-01-3", "Structure / function", "Easy",
    "Which of the following best describes the role of the patent example in paragraph 2?",
    "It illustrates why the work of keeping systems reliable tends to be missing from the historical record.",
    [("It shows that throughout the twentieth century inventors were paid considerably more than the engineers who maintained existing systems.",
      "Earnings are never discussed; the example contrasts what gets recorded, not what gets paid."),
     ("It offers evidence that bridges built after patents were introduced proved more reliable.",
      "The passage draws no causal link between patents and the reliability of bridges; the bridge is only an image of unrecorded success."),
     ("It suggests that legal protection for novelty discouraged engineers from maintaining old systems.",
      "Nothing in the passage says patents changed engineers' behaviour; the example concerns documentation only.")],
    "The sentence before it says that accumulated care 'leaves few documents'. The patent, which records novelty, is contrasted with the absence of any record that 'a bridge did not fall down', illustrating why maintenance is invisible to historians.",
    "Inventing a causal or economic claim that the example does not make.",
    "The function is signalled by the preceding sentence.", cognitive="Understanding")

rcq("S-RC-01-4", "Strengthen / weaken / assumption", "Medium",
    "Which of the following findings, if true, would most strengthen the claim in the final paragraph about why inventions succeed or fail?",
    "Of several rival designs for an early farm machine, the one that spread most widely was the one village blacksmiths could mend.",
    [("The inventor of an early farm machine kept detailed notebooks that historians now rely on to fix the date of its first successful trial.",
      "This concerns the moment of origin, which the author says historians should look away from; it says nothing about success or failure."),
     ("Most farm machines patented in one decade were never manufactured in large numbers.",
      "It reports failures without linking them to repairability, so it does not support the author's explanation of why they failed."),
     ("Railway maintenance staff reported higher job satisfaction than engineers designing new locomotives.",
      "Job satisfaction is irrelevant to the claim that repairability by ordinary hands decided which inventions succeeded.")],
    "The final paragraph claims that many inventions succeeded because they could be repaired by ordinary hands. A case in which the repairable design beat its rivals directly supports that causal claim.",
    "Picking an option that is on topic (inventions, maintenance) but does not bear on the specific causal claim.",
    "Requires isolating the precise claim and testing each option against it.", cognitive="Analysis")

# ------------------------------------------------------------------ Para jumble (TITA)
pj("S-PJ-001", "Science history", "Sparse depth soundings made early seafloor maps too smooth.", "Medium",
   ["Early maps of the ocean floor were drawn from soundings taken one at a time, a weighted line lowered until it touched bottom.",
    "Each measurement could take hours, so a single expedition might record only a few hundred depths across thousands of kilometres.",
    "Between those scattered points, cartographers had little choice but to interpolate, smoothing over whatever ridges and trenches lay undetected.",
    "It is no surprise, then, that the first echo-sounding surveys revealed a seabed far more rugged than the maps had shown."],
   "Sentence [[1]] introduces the method of single soundings. Sentence [[2]] opens with 'Each measurement', which refers back to those soundings, and explains why the record was sparse. Sentence [[3]] refers to 'those scattered points', the few hundred depths of [[2]], and draws the consequence of interpolation. Sentence [[4]] concludes with 'then', contrasting the smooth maps with what echo sounding revealed.",
   "Placing sentence [[3]] directly after sentence [[1]] because both concern how maps were drawn, which leaves 'those scattered points' without a referent.",
   "SPJ-soundings", "The chain is carried by reference words ('Each measurement', 'those scattered points', 'then').",
   traps=[("1324", "Students join sentences [[1]] and [[3]] as both describe mapping, but 'those scattered points' needs the sparse record described in sentence [[2]].")])

# ------------------------------------------------------------------ Para summary (MCQ)
ps("S-PS-001", "Public policy", "Rewarded performance measures get gamed.", "Medium",
   "When a hospital is judged by how quickly patients in its emergency department are seen, the number it reports soon improves. Sometimes this reflects real change: more staff, better triage. But the figure can also be improved in ways that leave patients no better off, for instance by having a nurse greet arrivals within minutes and then leaving them to wait for a doctor as long as before. The measure was chosen because it seemed to track the quality of care; once rewards were attached to it, it began to track mainly the effort spent on the measure itself. The problem is not measurement as such but forgetting that people respond to it.",
   "Once rewards attach to a performance figure, it can improve without any gain in what it was meant to indicate, as people adapt to the figure.",
   [("Emergency departments should never be judged by their waiting times, because hospital staff routinely falsify such figures to earn rewards and avoid penalties.",
     "The paragraph describes legal gaming, not falsification, and it rejects blaming measurement itself, so the prescription misstates it."),
    ("Hospitals usually improve their reported waiting times by hiring more staff, improving triage and reorganising how arriving patients are received.",
     "This is the 'sometimes' case the paragraph sets aside; it omits the central point that the figure can improve without real change."),
    ("Numerical measures of care are inherently meaningless and ought to be replaced by qualitative judgement.",
     "The last sentence says the problem is 'not measurement as such', which this option contradicts.")],
   "The paragraph uses the hospital example to make a general point: a rewarded measure starts to track effort spent on the measure rather than the quality it was chosen to track, because people respond to it. The key captures both the mechanism and the scope.",
   "Choosing an option that keeps the example but loses the general point, or one that overstates it into rejecting measurement.",
   "SPS-metric-gaming", "Distractors are close in wording; the key must be told apart by scope.")

# ------------------------------------------------------------------ Odd sentence out (TITA)
ooo("S-OOO-001", "Biology", "Training bees with sugar rewards lets researchers test colour discrimination.", "Medium",
    ["Bees can be trained to associate a colour with a sugar reward within a few visits.",
     "Once trained, they will approach that colour even after the reward has been removed.",
     "Researchers have used this dependable learning to map which wavelengths bees can distinguish.",
     "By rewarding one of two similar shades, they can test whether the insects tell those shades apart."],
    "Some flowers have evolved ultraviolet patterns that are invisible to people but guide bees towards nectar.",
    "Sentences [[1]], [[2]], [[3]] and [[4]] describe one experimental method: bees learn a colour-reward link, the learning persists, and researchers exploit it to test which shades bees can tell apart. Sentence [[X]] is about bee colour vision too, but it describes floral evolution and plays no part in the training-and-testing argument.",
    "Treating shared subject matter (bees and colour) as coherence and missing that the paragraph is about a method.",
    "SOOO-bee-training", "The odd sentence shares the topic, so it must be rejected on function, not subject.",
    traps=[(2, "Sentence [[2]] can look like a digression, but persistence after the reward is removed is what makes the learning usable as a test in sentence [[3]].")])

# ------------------------------------------------------------------ Sentence placement (MCQ)
sp("S-SP-001", "Science history", "Why the second was redefined from astronomical to atomic time.", "Medium",
   ["For centuries, the length of a day was the natural unit against which all other time was measured.",
    "Astronomers defined the second as a fixed fraction of the mean solar day, and clocks were judged by how well they kept pace with the sky.",
    "By the middle of the twentieth century, however, the best clocks had become steadier than the planet itself.",
    "Measurements showed that the rotation of the Earth speeds up and slows down by small amounts, influenced by tides, winds and movements deep inside the planet.",
    "In 1967 the second was redefined in terms of the vibrations of caesium atoms, and the reference for time moved from the heavens to the laboratory.",
    "One consequence is that atomic time and astronomical time slowly drift apart, so that leap seconds have occasionally been inserted to keep them aligned."],
   "A standard that wobbled in this way could no longer serve as the foundation for precise timekeeping.",
   [1, 3, 4, 6],
   "The missing sentence refers to 'a standard that wobbled in this way', so it must follow the description of the Earth's irregular rotation, and it explains why a new definition was needed, so it must precede the 1967 redefinition. Only gap (3) lies between those two sentences.",
   {1: "At gap (1) no irregularity has been mentioned, so 'wobbled in this way' has nothing to refer to.",
    3: "At gap (2) the clocks have only just been called steadier; the speeding up and slowing down that 'this way' refers to comes in the next sentence.",
    6: "At gap (4) the redefinition and its consequences have already been described, so a sentence motivating the change comes too late."},
   "Placing the sentence right after 'steadier than the planet itself', before the wobble has been described.",
   "SSP-redefining-second", "The fit is fixed by a backward reference and a forward causal link.")
