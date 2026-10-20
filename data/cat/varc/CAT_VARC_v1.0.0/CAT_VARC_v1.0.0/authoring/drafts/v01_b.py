import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")
SE, TE, AL, LM, ED, HM = ("Science and environment", "Technology", "Arts and literature",
                          "Language and media", "Education", "Health and medicine")

# ------------------------------------------------------------------ 001 Easy, 4
pj("V01-B-001", SE, "Because each generation takes the wildlife it first saw as normal, long declines in nature go unnoticed.", "Easy",
   ["Each generation of naturalists tends to take the abundance of wildlife it first encountered as the natural state of things.",
    "When numbers fall during their working lives, they record the loss against that starting point rather than against any earlier one.",
    "Their successors, beginning from the depleted world that those records describe, then treat the reduced numbers as normal in turn.",
    "Over several generations, this quiet resetting of expectations allows a dramatic decline to pass almost unnoticed, since no one remembers the earlier abundance."],
   "Sentence [[1]] states the general tendency: each generation treats the wildlife it first saw as natural. Sentence [[2]] refers to 'that starting point', the abundance of [[1]], and says losses are recorded against it. Sentence [[3]] speaks of 'Their successors' and 'the depleted world that those records describe', which needs the records of [[2]]. Sentence [[4]] sums up the process as 'this quiet resetting of expectations' and states its consequence.",
   "Placing sentence [[3]] straight after sentence [[1]] because both describe a generation's starting point, which leaves 'those records' without the recording described in sentence [[2]].",
   "V01B-shifting-baselines", "The opener is clear and each later sentence carries a reference word ('that starting point', 'those records', 'this quiet resetting').",
   traps=[("1324", "Sentence [[3]] speaks of 'the depleted world that those records describe', and the records of loss appear only in sentence [[2]]."),
          ("1243", "Sentence [[4]] summarises a process across 'several generations', so it cannot come before sentence [[3]] introduces the successors.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 002 Medium, 5
pj("V01-B-002", SE, "A carbon offset should be judged by how securely its carbon stays stored, not by how much it captures at first.", "Medium",
   ["A company that pays for trees to be planted can claim that its emissions have been offset by the carbon those trees absorb.",
    "The claim assumes, however, that the carbon will stay locked away for as long as the emitted carbon dioxide remains in the atmosphere, which may be centuries.",
    "A forest offers no such guarantee: it can burn, be felled when land prices change, or die back in a drought.",
    "If any of these happens, the stored carbon returns to the air, and the emission that was supposedly cancelled turns out only to have been postponed.",
    "An offset, then, should be judged not by how much carbon it captures in its first years but by how confident we can be that the carbon will stay captured."],
   "Sentence [[1]] states the offset claim. Sentence [[2]] exposes the hidden assumption behind 'The claim': the carbon must stay stored as long as the emission stays in the air. Sentence [[3]] says a forest gives 'no such guarantee' and lists the risks. Sentence [[4]] follows the risks ('If any of these happens') to their consequence: the emission was only postponed. Sentence [[5]] draws the conclusion ('then') that permanence, not initial capture, is the right test.",
   "Ending with sentence [[3]] or [[4]] after the conclusion because they mention concrete risks, which leaves the conclusion of sentence [[5]] without the argument it rests on.",
   "V01B-carbon-offset-permanence", "Order depends mainly on the logic of the idea: claim, hidden assumption, threat to the assumption, consequence, and only then the revised test.",
   traps=[("12354", "Sentence [[5]] draws its conclusion from the consequence that an emission may only be postponed, which is stated in sentence [[4]]; and 'any of these' in sentence [[4]] must sit directly after the list of risks in sentence [[3]]."),
          ("13245", "Sentence [[3]] says a forest offers 'no such guarantee', and the guarantee in question, that carbon stays stored for centuries, is set out only in sentence [[2]].")])

# ------------------------------------------------------------------ 003 Easy, 4
pj("V01-B-003", SE, "Because groundwater is invisible, aquifers can be drained for decades before the loss is noticed.", "Easy",
   ["Rivers and lakes that are shrinking can be seen, photographed and argued over, which is one reason their decline draws public attention.",
    "Groundwater enjoys no such visibility, since it lies in rock and gravel beneath the very fields that draw on it.",
    "As a result, an aquifer can be pumped faster than rain refills it for decades before anyone notices, usually when wells must be drilled ever deeper.",
    "By the time that happens, the water lost may have taken thousands of years to accumulate and cannot be replaced within any human lifetime."],
   "Sentence [[1]] describes visible surface water and why its decline is noticed. Sentence [[2]] contrasts groundwater, which has 'no such visibility'. Sentence [[3]] gives the consequence ('As a result'): aquifers are over-pumped unnoticed until wells must go deeper. Sentence [[4]] begins 'By the time that happens', referring to that moment of discovery, and adds that the loss cannot be undone.",
   "Opening with sentence [[2]] because groundwater is the real subject, although 'no such visibility' compares it with the visible rivers and lakes of sentence [[1]].",
   "V01B-groundwater-depletion", "Each link is marked ('no such visibility', 'As a result', 'By the time that happens').",
   traps=[("2134", "Sentence [[2]] cannot open, because 'no such visibility' needs the visible rivers and lakes of sentence [[1]] to compare against.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 004 Medium, 4
pj("V01-B-004", SE, "The main losers from light pollution are not astronomers but city dwellers who do not know what they have lost.", "Medium",
   ["Complaints about light pollution are often dismissed as the special pleading of astronomers, a small group whose instruments are troubled by the glow of cities.",
    "Professional observatories, though, have largely solved their problem by moving to remote mountains, so they are not the ones who lose most.",
    "The real losers are the millions of city dwellers who have never seen the Milky Way and do not know what has been taken from them.",
    "That ignorance is precisely what keeps the complaint marginal, since a loss nobody remembers is a loss nobody demands back."],
   "Sentence [[1]] reports the common dismissal of the complaint as astronomers' special pleading. Sentence [[2]] answers it ('though'): observatories have moved away, so astronomers do not lose most. Sentence [[3]] names 'The real losers', which presupposes the denial in [[2]]. Sentence [[4]] refers to 'That ignorance', the city dwellers not knowing what they lost in [[3]], and explains why the complaint stays marginal.",
   "Placing sentence [[3]] straight after sentence [[1]] to contrast astronomers with city dwellers, which leaves 'The real losers' with no earlier claim about who loses most to correct.",
   "V01B-light-pollution-stargazing", "The reply to the dismissal must come before the claim about the real losers; the tempting order puts the losers first.",
   traps=[("1324", "'The real losers' in sentence [[3]] corrects a claim about who loses most, and that claim, that observatories are 'not the ones who lose most', is made in sentence [[2]]; sentence [[4]]'s 'That ignorance' must also follow sentence [[3]] directly.")])

# ------------------------------------------------------------------ 005 Medium, 4
pj("V01-B-005", TE, "Password composition rules produce predictable passwords that are weaker than they look.", "Medium",
   ["Rules that require every password to contain a capital letter, a digit and a symbol are meant to make passwords harder to guess.",
    "Faced with such demands, most people do the least the rules allow, capitalising the first letter and adding a digit and an exclamation mark at the end.",
    "Because so many users follow the same pattern, attackers simply build it into their guessing programs, and the extra characters add far less protection than their number suggests.",
    "Against such programs, a long phrase of ordinary words, which the rules may even reject, can be stronger than the predictable short password they end up producing."],
   "Sentence [[1]] states the rules and their purpose. Sentence [[2]] describes how people respond to 'such demands' with the minimum. Sentence [[3]] explains that because the response is a shared pattern, attackers exploit it. Sentence [[4]] begins 'Against such programs', the guessing programs of [[3]], and concludes that a long ordinary phrase can beat 'the predictable short password' the rules produce.",
   "Putting sentence [[4]] before sentence [[3]] because it states the payoff, although 'Against such programs' needs the guessing programs described in sentence [[3]].",
   "V01B-password-complexity-rules", "Order depends mainly on the logic of the idea: the rule, the human response, the attacker's exploitation of that response, and only then the counter-intuitive conclusion.",
   traps=[("1423", "Sentence [[4]] begins 'Against such programs', and the guessing programs are introduced only in sentence [[3]], so sentence [[4]] must come last."),
          ("1324", "Sentence [[3]] speaks of 'the same pattern', which must already have been described; the pattern appears only in sentence [[2]].")])

# ------------------------------------------------------------------ 006 Easy, 4
pj("V01-B-006", TE, "Technical debt, like a loan, buys speed now at the cost of interest paid on every later change.", "Easy",
   ["Programmers speak of 'technical debt' when a team ships a quick fix instead of the careful solution it knows it should build.",
    "Like a loan, the shortcut brings an immediate benefit, because the feature reaches users weeks earlier than it otherwise would.",
    "Also like a loan, it charges interest: every later change has to work around the hasty code and so takes longer than it should.",
    "Unless the team eventually sets aside time to rewrite that code, the interest can grow until most of its effort goes into servicing old shortcuts."],
   "Sentence [[1]] introduces the term 'technical debt'. Sentence [[2]] gives the first way the shortcut is 'Like a loan', its immediate benefit. Sentence [[3]] gives the second ('Also like a loan'), the interest. Sentence [[4]] speaks of 'that code' and 'the interest', both introduced in [[3]], and warns where unchecked interest leads.",
   "Swapping sentences [[2]] and [[3]], overlooking that 'Also like a loan' marks a second comparison and must follow the first.",
   "V01B-software-technical-debt", "The comparison is signposted ('Like a loan', 'Also like a loan', 'the interest').",
   traps=[("1324", "Sentence [[3]] begins 'Also like a loan', which requires an earlier comparison with a loan; that comparison is made in sentence [[2]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 007 Difficult, 5
pj("V01-B-007", TE, "Lock-in can explain why an inferior standard persists, but it cannot show that a surviving standard is inferior.", "Difficult",
   ["It is often said that a familiar keyboard layout survives only because of lock-in: everyone learned it, so no one can afford to abandon it.",
    "The argument has a real logic, since a typist who retrains alone pays the full cost of switching while gaining little until offices, schools and manufacturers switch too.",
    "Even granting this, the argument rests on a premise that is rarely examined, namely that a clearly better layout exists and is being passed over.",
    "If careful trials showed the supposed improvement to be marginal, the old layout's survival would need no special explanation at all.",
    "So lock-in can explain why an inferior standard persists, but whether the standard is inferior is a separate question that only such trials can settle."],
   "Sentence [[1]] reports the lock-in view. Sentence [[2]] concedes its logic: an individual switcher bears the cost alone. Sentence [[3]] grants that ('Even granting this') and exposes its unexamined premise, that a clearly better layout exists. Sentence [[4]] tests the premise: if 'the supposed improvement', the better layout of [[3]], proved marginal, no explanation would be needed. Sentence [[5]] concludes that lock-in explains persistence but cannot establish inferiority, which only 'such trials', those of [[4]], can settle.",
   "Moving straight from the reported view in sentence [[1]] to the challenge, as if the paragraph only criticised lock-in, which strands the concession of sentence [[2]] after the critique it is meant to precede.",
   "V01B-keyboard-layout-lock-in", "Order depends mainly on the logic of the idea: the reader must separate a concession from a critique and see that the critique targets a premise, not the mechanism; the concluding distinction between explaining persistence and proving inferiority is abstract.",
   traps=[("13425", "Sentence [[3]] says 'Even granting this', which concedes something; the only thing conceded is the logic of switching costs, stated in sentence [[2]], so sentence [[2]] must come before it."),
          ("12354", "Sentence [[5]] refers to 'such trials', which are introduced in sentence [[4]]; ending with sentence [[4]] leaves that reference without an antecedent.")],
   exams=D)

# ------------------------------------------------------------------ 008 Medium, 4
pj("V01-B-008", TE, "Range anxiety is about rare long trips, so roadside chargers may reassure buyers more than bigger batteries.", "Medium",
   ["Drivers considering an electric car often ask first how far it can go on a single charge.",
    "The question is natural, yet most of them drive only a short distance on a typical day, far less than even a modest battery provides.",
    "What they are really insuring against is the rare long journey, the holiday drive or the emergency trip, on which running out of charge would be a serious problem.",
    "For that reason, a dense network of fast chargers along major roads may reassure buyers more than any increase in battery size."],
   "Sentence [[1]] introduces the buyers' first question about range. Sentence [[2]] comments on 'The question' and notes that daily driving needs little range. Sentence [[3]] identifies what buyers are 'really' insuring against, the rare long journey, which corrects the impression left by [[2]]. Sentence [[4]] concludes ('For that reason') that chargers along major roads, where long journeys happen, may matter more than bigger batteries.",
   "Placing sentence [[4]] right after sentence [[2]], although chargers 'along major roads' answer the worry about long journeys, which appears only in sentence [[3]].",
   "V01B-electric-car-range-anxiety", "One must see that the conclusion about roadside chargers follows from the long-journey point, not from the daily-distance point.",
   traps=[("1243", "The reason that makes roadside chargers the answer is the fear of the rare long journey in sentence [[3]]; after sentence [[2]] alone, which says daily trips are short, the conclusion of sentence [[4]] has no basis.")])

# ------------------------------------------------------------------ 009 Medium, 5
pj("V01-B-009", AL, "An unreliable narrator works only when the author leaves clues that let readers see past the narration.", "Medium",
   ["A narrator who misreports events might seem to be a defect in a novel, since readers depend on the teller for everything they learn.",
    "Yet some of the most admired fiction is built on exactly such a teller, whose account the reader gradually learns to distrust.",
    "The pleasure lies in reading through the narration to what it conceals, noticing a detail the narrator mentions but fails to understand.",
    "This kind of reading is possible, however, only if the author has planted enough clues for the gap between account and event to be detected.",
    "A narrator who deceives the reader completely, leaving no such clues, produces not irony but merely a trick revealed on the last page."],
   "Sentence [[1]] raises the apparent objection to a misreporting narrator. Sentence [[2]] answers it ('Yet') with admired fiction built on 'such a teller'. Sentence [[3]] says where 'The pleasure' of such fiction lies, in reading through the narration. Sentence [[4]] refers to 'This kind of reading' and states its condition, planted clues. Sentence [[5]] describes the case with 'no such clues' and why it fails.",
   "Placing sentence [[5]] before sentence [[4]] because both concern deception, although 'no such clues' needs the clues introduced in sentence [[4]].",
   "V01B-unreliable-narrator", "Order depends mainly on the logic of the idea: objection, counter-example, the source of the pleasure, its condition, and the failure when the condition is absent.",
   traps=[("12354", "Sentence [[5]] speaks of 'no such clues', and clues are introduced only in sentence [[4]]."),
          ("12435", "Sentence [[4]] refers to 'This kind of reading', which must already have been described; reading through the narration is described in sentence [[3]].")])

# ------------------------------------------------------------------ 010 Difficult, 4
pj("V01-B-010", AL, "A forgery loses value because a painting is admired as an achievement, which a later copy cannot be.", "Difficult",
   ["When a painting long admired as a master's work is exposed as a forgery, its price collapses, even though not a single brushstroke has changed.",
    "This can look like snobbery, as if buyers had been paying for a signature rather than for anything they could see.",
    "The charge misses something, for a painting is admired not only as a surface but also as an achievement, the solution an artist found to problems of a particular time.",
    "A copy made later, by someone who already knew the solution, reproduces the look of that achievement without being one, and it is the achievement whose loss the price records."],
   "Sentence [[1]] presents the puzzle: the price of an exposed forgery collapses although nothing visible has changed. Sentence [[2]] states the tempting reading of 'This', snobbery. Sentence [[3]] replies that 'The charge', the accusation of snobbery, misses that a painting is an achievement. Sentence [[4]] applies the idea to the later copy, which reproduces 'that achievement' without being one, and explains the price.",
   "Opening with sentence [[3]] because it states the general principle, although it begins by answering 'The charge' of snobbery made in sentence [[2]].",
   "V01B-art-forgery-value", "Order depends mainly on the logic of the idea: puzzle, tempting explanation, rebuttal by a distinction, application; the general principle tempts as an opener, and the reader must see that it is a reply.",
   traps=[("3124", "Sentence [[3]] cannot open: 'The charge' it answers is the charge of snobbery in sentence [[2]], and sentence [[4]] needs 'that achievement' immediately before it."),
          ("1324", "Sentence [[2]]'s 'This can look like snobbery' would then follow the account of paintings as achievements, so the paragraph would raise the snobbery charge after having already answered it.")],
   exams=D)

# ------------------------------------------------------------------ 011 Easy, 4
pj("V01-B-011", AL, "Since a film cannot hold a whole novel, an adaptation should be judged by its spirit, not its completeness.", "Easy",
   ["Readers often complain that a film has betrayed the novel on which it was based.",
    "The complaint usually assumes that a good adaptation should include as much of the book as possible.",
    "That assumption, however, ignores the form, since a two-hour film cannot hold all the incidents of a long novel; cutting is not betrayal but a condition of film.",
    "The fairer test is therefore whether the film keeps the spirit of the book, not whether it keeps its scenes."],
   "Sentence [[1]] states the readers' complaint. Sentence [[2]] identifies the assumption behind 'The complaint'. Sentence [[3]] challenges 'That assumption': a film cannot contain a whole novel. Sentence [[4]] proposes 'The fairer test' as the conclusion ('therefore').",
   "Placing sentence [[3]] before sentence [[2]], although 'That assumption' refers to the belief, stated in sentence [[2]], that an adaptation should include as much as possible.",
   "V01B-film-adaptation-novels", "Clear chain of complaint, assumption, objection and conclusion, marked by 'The complaint', 'That assumption' and 'therefore'.",
   traps=[("1324", "Sentence [[3]] begins 'That assumption', and the only assumption in the paragraph is the one stated in sentence [[2]]; sentence [[2]]'s 'The complaint' must also directly follow sentence [[1]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 012 Medium, 4
pj("V01-B-012", AL, "Cleaning old paintings can remove the artist's own glazes, making the picture brighter but less faithful.", "Medium",
   ["Cleaning an old painting seems a straightforward good: centuries of grime and yellowed varnish are removed, and the colours the artist chose appear again.",
    "The difficulty is that some of what looks like dirt may be the artist's own work, a thin tinted glaze laid over the paint to soften it.",
    "Since such glazes and later varnish can be chemically similar, a restorer may remove both together without realising it.",
    "The brighter picture that results can then be less faithful than the dim one it replaced, however much it pleases the eye."],
   "Sentence [[1]] states the common view that cleaning restores the artist's colours. Sentence [[2]] introduces 'The difficulty': the apparent dirt may include the artist's glaze. Sentence [[3]] explains how 'such glazes' come to be removed. Sentence [[4]] states the result: a brighter but less faithful picture.",
   "Placing sentence [[4]] before sentence [[3]], although the 'brighter picture that results' is the result of the accidental removal described in sentence [[3]].",
   "V01B-cleaning-old-paintings", "The final pair must be ordered by cause and effect, since both could appear to follow the statement of the difficulty.",
   traps=[("1243", "Sentence [[4]] describes the picture 'that results' from removing the glaze along with the varnish; that removal is explained only in sentence [[3]], so sentence [[3]] must come first.")])

# ------------------------------------------------------------------ 013 Easy, 4
pj("V01-B-013", LM, "Since every language is built partly from borrowings, a pure language has never existed.", "Easy",
   ["Campaigns to keep a language pure usually target words borrowed from other languages.",
    "Yet almost every language has absorbed foreign words for centuries, often so thoroughly that its speakers no longer recognise them as borrowed.",
    "Many of the words that purists defend as native were themselves once newcomers, adopted from traders, conquerors or neighbours.",
    "If even the purists' own vocabulary was once borrowed, a pure language is not something that has been lost but something that has never existed."],
   "Sentence [[1]] introduces purist campaigns against borrowed words. Sentence [[2]] objects ('Yet') that languages have always absorbed foreign words. Sentence [[3]] sharpens the point: even the words purists defend were once borrowed. Sentence [[4]] builds on that example ('If even the purists' own vocabulary was once borrowed') to conclude that a pure language has never existed.",
   "Placing sentence [[3]] before sentence [[2]], although the general claim that languages absorb words unnoticed must come before the pointed example of the purists' own words.",
   "V01B-loanwords-purity", "The order follows a clear objection and conclusion, marked by 'Yet' and by the final sentence's reference to the purists' own vocabulary.",
   traps=[("1324", "The 'Yet' of sentence [[2]] contrasts with the purist campaigns of sentence [[1]]; placed after sentence [[3]], which already undercuts the purists, it contrasts with nothing.")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 014 Medium, 4
pj("V01-B-014", LM, "Question headlines protect the publisher while leaving readers with impressions the evidence may not support.", "Medium",
   ["A headline phrased as a question, such as one asking whether a common food causes illness, lets a publication raise a frightening possibility without asserting it.",
    "If the article finds no good evidence, the publication can still say that it merely asked, and no one can accuse it of having made a false claim.",
    "Readers are not protected in the same way, since they tend to remember the possibility the headline raised rather than the doubt in its grammar.",
    "That grammatical doubt thus shields the writer without reaching the reader, who leaves with an impression the article itself may not support."],
   "Sentence [[1]] introduces the question headline and its effect. Sentence [[2]] shows how it protects the publication. Sentence [[3]] says readers are 'not protected in the same way', which refers back to the protection in [[2]]. Sentence [[4]] concludes ('thus'), and its 'That grammatical doubt' points back to 'the doubt in its grammar' at the end of [[3]], so it must come last.",
   "Placing sentence [[3]] straight after sentence [[1]], although 'in the same way' refers to the publication's protection, which is described only in sentence [[2]].",
   "V01B-headline-questions", "The two middle sentences both follow from the opener; only 'in the same way' and the logic of contrast fix their order.",
   traps=[("1324", "Sentence [[3]] says readers are 'not protected in the same way', which compares them with the protected publication of sentence [[2]]."),
          ("1243", "Sentence [[4]] begins 'That grammatical doubt', which refers to 'the doubt in its grammar' mentioned only in sentence [[3]], so sentence [[4]] cannot precede it.")])

# ------------------------------------------------------------------ 015 Difficult, 5
pj("V01-B-015", LM, "Euphemisms wear out because the contempt lies in attitudes rather than words, so renaming alone cannot succeed.", "Difficult",
   ["A polite term is often introduced to replace a word that has come to sound insulting when applied to some condition or group.",
    "For a while the new term works, because it carries none of the contempt that had gathered around the old one.",
    "But the contempt was never in the old word's sounds; it lay in attitudes towards the people the word described.",
    "As long as those attitudes persist, they attach themselves to the replacement, which in time sounds as harsh as the word it displaced.",
    "Renaming can signal respect, then, but it cannot by itself produce the change in attitude on which its success depends."],
   "Sentence [[1]] introduces the practice of replacing a word that sounds insulting. Sentence [[2]] says the new term works 'For a while' because it lacks the old contempt. Sentence [[3]] argues ('But') that the contempt was in attitudes, not sounds. Sentence [[4]] follows: 'those attitudes', if they persist, attach to the replacement. Sentence [[5]] concludes ('then') that renaming cannot by itself bring about the change it depends on.",
   "Ending with sentence [[4]] because the worn-out replacement seems a natural close, which leaves sentence [[5]]'s concluding 'then' with nothing after it to sum up and strands its weighing of renaming against attitude.",
   "V01B-euphemism-treadmill", "Order depends mainly on the logic of the idea: the diagnosis that contempt lies in attitudes must precede the prediction that it migrates, and the concession that renaming 'can signal respect' must close it; the reasoning is abstract.",
   traps=[("13245", "Sentence [[3]] speaks of 'the contempt', which is first introduced in sentence [[2]] as what the new term lacks; it cannot directly follow sentence [[1]]."),
          ("12354", "Sentence [[4]] refers to 'those attitudes', introduced in sentence [[3]], and the conclusion in sentence [[5]] depends on the migration of attitude that sentence [[4]] describes, so it cannot come before it.")],
   exams=D)

# ------------------------------------------------------------------ 016 Medium, 5
pj("V01-B-016", LM, "Dictionaries record usage rather than lay down rules, so blaming them for including new senses misreads their purpose.", "Medium",
   ["Many people consult a dictionary to find out how a word ought to be used, as if it were a rulebook.",
    "Most modern dictionary makers, by contrast, see their task as recording how words are actually used by speakers and writers.",
    "When enough people use a word in a new sense, they add that sense, even if it began as what older speakers regard as an error.",
    "Readers who expected a rulebook then accuse the dictionary of approving mistakes.",
    "The accusation misreads the dictionary's purpose, much as one might blame a map for showing a road that the mapmaker thinks should never have been built."],
   "Sentence [[1]] states the popular view of the dictionary as a rulebook. Sentence [[2]] contrasts ('by contrast') the makers' view that they record usage. Sentence [[3]] shows what follows: 'they', the makers, add new senses even when these began as errors. Sentence [[4]] describes the reaction of readers 'who expected a rulebook'. Sentence [[5]] answers 'The accusation' with the map comparison.",
   "Placing sentence [[4]] straight after sentence [[1]] because both concern readers who want a rulebook, although the accusation of 'approving mistakes' needs the inclusion of erroneous senses described in sentence [[3]].",
   "V01B-dictionaries-describe-usage", "Two sentences mention readers who expect a rulebook, so the reader must see that the accusation responds to what the makers do.",
   traps=[("14235", "The readers' accusation of 'approving mistakes' in sentence [[4]] reacts to the inclusion of senses that began as errors, which is described only in sentence [[3]]; and 'they' in sentence [[3]] must refer to the makers of sentence [[2]]."),
          ("13245", "In sentence [[3]], 'they add that sense' needs a subject who compiles dictionaries; placed after sentence [[1]] it would refer to the people consulting them.")])

# ------------------------------------------------------------------ 017 Medium, 4
pj("V01-B-017", ED, "Grade inflation pushes selectors towards institutional reputation, which penalises able students from obscure schools.", "Medium",
   ["When most students in a course receive top grades, the grade stops distinguishing the excellent from the merely competent.",
    "Employers and admissions officers, unable to learn much from the grade, begin to rely on other signals, such as the reputation of the institution.",
    "Those signals favour students who attended well-known schools, whatever their individual ability.",
    "Generous grading, intended as kindness to students, can thus end up penalising the able student from an obscure school, whose top grade no longer stands out."],
   "Sentence [[1]] states that inflated grades stop distinguishing students. Sentence [[2]] gives the response of selectors, who turn to 'other signals' such as reputation. Sentence [[3]] says 'Those signals' favour students from well-known schools. Sentence [[4]] concludes ('thus') with the irony that generous grading hurts the able student from an obscure school.",
   "Placing sentence [[4]] before sentence [[3]] because it states the harm, although the harm to students from obscure schools follows from the bias of the signals described in sentence [[3]].",
   "V01B-grade-inflation", "Order depends mainly on the logic of the idea: a chain of consequences (uninformative grades, substitute signals, bias of those signals, ironic harm) that must run in causal sequence.",
   traps=[("1243", "Sentence [[4]] says the able student from an obscure school is penalised, which follows only once sentence [[3]] has shown that the substitute signals favour well-known schools; sentence [[3]]'s 'Those signals' must also directly follow sentence [[2]].")])

# ------------------------------------------------------------------ 018 Easy, 4
pj("V01-B-018", ED, "Recalling material from memory is a better way to study than rereading, even though it feels less productive.", "Easy",
   ["Students preparing for an exam often reread their notes, since the material feels more familiar each time.",
    "That feeling of familiarity, however, is a poor guide to whether they will be able to recall the material without the notes in front of them.",
    "Testing oneself without the notes is harder and less pleasant, but it practises exactly that act of recall, the one the exam will demand.",
    "The more effective method is thus the one that feels less productive while it is being used."],
   "Sentence [[1]] describes rereading and why it appeals. Sentence [[2]] refers to 'That feeling of familiarity' and says it is misleading. Sentence [[3]] presents the alternative, testing oneself, which practises 'that act of recall', the recall without notes named in [[2]]. Sentence [[4]] concludes ('thus') that the better method feels less productive.",
   "Placing sentence [[3]] before sentence [[2]], although the case for recall practice depends on first showing that familiarity misleads.",
   "V01B-retrieval-practice", "Each step is marked ('That feeling of familiarity', 'that act of recall', 'thus').",
   traps=[("1324", "Sentence [[3]] speaks of 'that act of recall', which needs the recall without notes mentioned in sentence [[2]]; and 'That feeling of familiarity' in sentence [[2]] must directly follow sentence [[1]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 019 Medium, 4
pj("V01-B-019", ED, "Smaller classes help only if teaching changes and recruits are good, so large rapid reforms may disappoint.", "Medium",
   ["Reducing class sizes seems an obvious way to improve teaching, since each pupil can receive more of the teacher's attention.",
    "That benefit depends, though, on teachers changing how they teach, for a lecture delivered to twenty pupils differs little from one delivered to thirty-five.",
    "Even where teachers do adapt, a policy that cuts class sizes across a whole country must find many more teachers at once, and the new recruits may be less experienced than those already employed.",
    "The gain from smaller classes can therefore be smaller than expected, or can disappear altogether, when the reform is made too quickly and on too large a scale."],
   "Sentence [[1]] gives the apparent benefit of smaller classes. Sentence [[2]] qualifies 'That benefit': it requires teachers to change their methods. Sentence [[3]] adds a second difficulty 'Even where teachers do adapt', the need for many inexperienced recruits. Sentence [[4]] concludes ('therefore') that a fast, large reform may lose the gain.",
   "Putting sentence [[3]] second because it reads like a fresh start about national policy, although it opens with 'Even where teachers do adapt', which presupposes the condition stated in sentence [[2]].",
   "V01B-class-size", "Order depends mainly on the logic of the idea: two qualifications must be ordered, since the second grants the first, and the conclusion's 'too large a scale' depends on the second.",
   traps=[("1324", "Sentence [[3]] begins 'Even where teachers do adapt', which grants the condition set out in sentence [[2]]; before that condition is stated, the concession has nothing to grant, and 'That benefit' in sentence [[2]] would no longer follow the benefit in sentence [[1]].")])

# ------------------------------------------------------------------ 020 Medium, 4
pj("V01-B-020", ED, "Returning comments without marks makes pupils read the advice, but only if the comments are worth reading.", "Medium",
   ["Teachers who return written work with both a mark and detailed comments often find that pupils look at the mark and ignore the rest.",
    "The mark, once seen, settles the question most pupils care about, which is how they did compared with their classmates.",
    "Since that question cannot be answered from a page with no mark on it, some schools have experimented with returning comments alone, at least for drafts.",
    "The approach asks a great deal of teachers, however, since comments that are vague or generic give pupils nothing worth reading in place of the mark."],
   "Sentence [[1]] describes the problem: pupils read the mark and ignore the comments. Sentence [[2]] explains why: 'The mark, once seen' answers what pupils care about. Sentence [[3]] gives the response, comments without marks, justified by the fact that 'that question', the comparison of [[2]], cannot then be answered. Sentence [[4]] qualifies 'The approach' with its demand on teachers.",
   "Placing sentence [[3]] straight after sentence [[1]] because it answers the problem, although its 'that question' refers to the question of how pupils compare with classmates, raised only in sentence [[2]].",
   "V01B-comments-instead-of-marks", "The remedy could seem to follow the problem directly; the reader must see that it rests on the explanation in between.",
   traps=[("1324", "Sentence [[3]] refers to 'that question', the question of how pupils did compared with their classmates, which is raised only in sentence [[2]]; and sentence [[4]]'s 'The approach' must follow sentence [[3]].")])

# ------------------------------------------------------------------ 021 Difficult, 5
pj("V01-B-021", ED, "Memorised facts are the material understanding works on, so memory and understanding are partners, not rivals.", "Difficult",
   ["Rote memorisation is often contrasted unfavourably with understanding, as if the two competed for a pupil's time.",
    "Understanding a topic, however, largely consists in seeing how facts connect, and facts that are not held in memory cannot be connected.",
    "A pupil who must look up every date while reading about a historical period has no attention left for noticing which events caused which.",
    "None of this means that memorised facts amount to understanding, and a pupil who could recite every date might still miss what links them.",
    "Memory and understanding are thus partners rather than rivals: memorised facts are the material, and understanding is the work that, as the reciting pupil shows, must still be done on them."],
   "Sentence [[1]] reports the view that memorisation and understanding compete. Sentence [[2]] challenges it ('however'): understanding is the connecting of remembered facts. Sentence [[3]] illustrates this with the pupil looking up dates. Sentence [[4]] concedes ('None of this means') that memorised facts are not yet understanding, with the pupil who 'could recite every date'. Sentence [[5]] concludes that the two are partners, citing 'the reciting pupil' of [[4]].",
   "Placing the concession of sentence [[4]] straight after sentence [[1]], where it seems to agree with the critics, although 'None of this' refers to the argument of sentences [[2]] and [[3]] and 'every date' echoes the example of sentence [[3]].",
   "V01B-rote-memorisation", "Order depends mainly on the logic of the idea: a concession that could seem to agree with the reported view must be placed after the argument it limits; the tempting order puts it second.",
   traps=[("14235", "Sentence [[4]] opens 'None of this means', which limits an argument already made; after sentence [[1]] there is no argument yet, only a reported view, and 'every date' presupposes the example in sentence [[3]]."),
          ("12354", "Sentence [[5]] refers to 'the reciting pupil', who appears only in sentence [[4]]; ending with sentence [[4]] would leave that reference without an antecedent.")],
   exams=D)

# ------------------------------------------------------------------ 022 Difficult, 5
pj("V01-B-022", HM, "Overdiagnosis inflates screening's apparent success, so more cancers detected and survived does not prove lives saved.", "Difficult",
   ["Screening healthy people for cancer seems an unmixed good, since a tumour found early is usually easier to treat.",
    "Some tumours that screening finds, however, grow so slowly that they would never have caused symptoms in the patient's lifetime.",
    "Because doctors cannot always tell such tumours from dangerous ones, many of them are treated anyway, with surgery or radiation that carries its own harms.",
    "Those who come through the treatment, as nearly all such patients do, are then counted among the successes of screening, which makes the programme look better than it is.",
    "A rise in the number of cancers detected and survived is therefore not, on its own, evidence that screening is saving lives."],
   "Sentence [[1]] states the common view that early detection is an unmixed good. Sentence [[2]] qualifies it ('however'): some detected tumours would never have caused harm. Sentence [[3]] explains that 'such tumours' are treated anyway. Sentence [[4]] says that those who 'come through the treatment', the treatment of [[3]], are counted as successes, inflating the programme's record. Sentence [[5]] concludes ('therefore') that detection and survival figures alone do not show lives saved.",
   "Placing sentence [[4]] straight after sentence [[2]] because patients with harmless tumours would obviously survive, although 'the treatment' they come through is introduced only in sentence [[3]].",
   "V01B-cancer-screening-overdiagnosis", "Order depends mainly on the logic of the idea: the statistical point that harmless cases inflate survival figures must follow both their detection and their treatment, and the conclusion is about evidence, not about screening being harmful.",
   traps=[("12435", "Sentence [[4]] speaks of those who 'come through the treatment', and treatment of the slow tumours is described only in sentence [[3]]."),
          ("12354", "The conclusion in sentence [[5]] concerns figures for cancers 'detected and survived', which become misleading only because sentence [[4]] shows harmless cases being counted as successes.")],
   exams=D)

# ------------------------------------------------------------------ 023 Easy, 4
pj("V01-B-023", HM, "Hand hygiene in hospitals improves more by making cleaning easy than by urging staff.", "Easy",
   ["Hospitals have long known that cleaning hands between patients is one of the simplest ways to prevent infections from spreading.",
    "Even so, staff often skip it, not out of carelessness but because a busy shift may call for cleaning their hands dozens of times.",
    "Placing alcohol rub dispensers at every bedside reduces this burden, since cleaning hands then takes seconds rather than a walk to a sink.",
    "The lesson is that compliance often depends less on exhorting staff than on making the right action easy."],
   "Sentence [[1]] states what hospitals know about hand cleaning. Sentence [[2]] says 'Even so' staff skip it, because of the burden. Sentence [[3]] says bedside dispensers reduce 'this burden'. Sentence [[4]] draws 'The lesson'.",
   "Placing sentence [[3]] before sentence [[2]], although 'this burden' refers to the repeated cleaning described in sentence [[2]].",
   "V01B-hospital-hand-hygiene", "The links are explicit ('Even so', 'this burden', 'The lesson').",
   traps=[("1324", "Sentence [[3]] says the dispensers reduce 'this burden', and the burden, cleaning hands dozens of times in a shift, is described only in sentence [[2]].")],
   cognitive="Understanding")

# ------------------------------------------------------------------ 024 Medium, 4
pj("V01-B-024", HM, "Fever is often part of the body's defence, so suppressing it eases discomfort without always aiding recovery.", "Medium",
   ["A fever is usually treated as part of the illness, something to be brought down as quickly as possible.",
    "In many infections, however, the raised temperature is the body's own response, and it may help the immune system while slowing the growth of some pathogens.",
    "If so, routinely suppressing a moderate fever could in some cases lengthen the very illness it seems to relieve.",
    "This does not mean that fevers should simply be left alone, since very high temperatures are dangerous in themselves, but it does suggest that comfort and cure are not always the same goal."],
   "Sentence [[1]] states the usual view of fever. Sentence [[2]] counters it ('however'): fever may be part of the defence. Sentence [[3]] draws the hedged implication ('If so') that suppressing it could lengthen illness. Sentence [[4]] limits that implication ('This does not mean') and states the distinction between comfort and cure.",
   "Placing sentence [[4]] directly after sentence [[2]] as a caution, although its point that 'comfort and cure are not always the same goal' rests on the possibility, raised in sentence [[3]], that relief could lengthen illness.",
   "V01B-fever-as-defence", "Both the implication and the caution could seem to follow the counter-claim; their order must be fixed by what each presupposes.",
   traps=[("1243", "Sentence [[3]]'s 'If so' would then refer to the caution of sentence [[4]] rather than to the claim about fever as a defence, and sentence [[4]]'s contrast between comfort and cure would come before the reason for it.")])

# ------------------------------------------------------------------ 025 Easy, 5
pj("V01-B-025", HM, "Weekend lie-ins do not fully repay lost sleep, and sleep loss also distorts people's sense of how impaired they are.", "Easy",
   ["Many people treat sleep as an account they can overdraw during the week and repay at the weekend.",
    "A night of short sleep does leave a debt of sorts, felt as drowsiness and slower reactions the next day.",
    "One long lie-in, however, does not seem to repay several such nights in full, since some of the impairment persists.",
    "The second problem is harder to notice: people who are chronically short of sleep often underestimate how impaired they are, because the tiredness comes to feel normal.",
    "The weekend repayment plan therefore fails twice, since it does not fully restore performance and it relies on a judgement that the debt itself has distorted."],
   "Sentence [[1]] introduces the idea of sleep as an account. Sentence [[2]] grants that short sleep leaves 'a debt of sorts'. Sentence [[3]] gives the first problem ('however'): a lie-in does not repay 'several such nights'. Sentence [[4]] announces 'The second problem', distorted self-judgement. Sentence [[5]] concludes that the plan 'fails twice', naming both problems in order.",
   "Placing sentence [[4]] before sentence [[3]], although 'The second problem' needs a first problem, which sentence [[3]] supplies.",
   "V01B-sleep-debt", "Explicit markers ('such nights', 'The second problem', 'fails twice') fix the order.",
   traps=[("12435", "Sentence [[4]] begins 'The second problem', so the first problem, the incomplete repayment in sentence [[3]], must come before it.")],
   cognitive="Understanding")
