import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

D = ("CAT", "XAT")

# ------------------------------------------------------------------ 001
ooo("V03-D-001", "History and politics",
    "Wartime rationing was a political instrument as well as an economic one, because visibly equal sacrifice sustained consent.", "Easy",
    ["During long wars, governments that controlled scarce food often issued ration books, which entitled each household to a fixed weekly quantity of staples.",
     "The aim was not only to stretch supplies but to make sacrifice visibly equal, so that the poor were not priced out while the wealthy ate as before.",
     "This sense of fairness mattered for morale, because people tend to tolerate hardship far better when they believe it is being shared.",
     "Rationing was therefore as much a political instrument as an economic one, sustaining consent for a war that demanded endurance from everyone."],
    "Many families also kept chickens or dug vegetable plots in their gardens, and some of these habits outlasted the war by decades.",
    "Sentence [[1]] introduces ration books, sentence [[2]] gives their double aim of stretching supplies and making sacrifice 'visibly equal', sentence [[3]] explains why 'This sense of fairness' mattered for morale, and sentence [[4]] concludes ('therefore') that rationing was a political as well as an economic instrument. Sentence [[X]] is about wartime food, but it describes what households did for themselves, and its point about habits outlasting the war has nothing to do with fairness, morale or consent.",
    "Choosing sentence [[3]] because it states a general truth about people rather than a fact about rationing, though the conclusion in sentence [[4]] depends on it.",
    "V03D-wartime-ration-books",
    "The odd sentence is on wartime food but turns to household self-help and a later period; the four coherent sentences are joined by clear links.",
    traps=[(3, "Sentence [[3]] is needed: it explains why equal sacrifice mattered, and without it the 'therefore' in sentence [[4]] has no reason to rest on.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 002
ooo("V03-D-002", "History and politics",
    "Guild apprenticeship, justified by quality, also served to restrict entry and protect masters' incomes.", "Medium",
    ["In many medieval towns, a young person who wished to practise a craft had to serve a long apprenticeship under a master belonging to the guild.",
     "The official justification was quality: a customer buying a cabinet or a pair of shoes could trust that its maker had been properly trained.",
     "Yet the length of these terms often exceeded anything the skill itself required, and the masters' own sons were frequently admitted on easier conditions.",
     "Such patterns suggest that apprenticeship also served to limit the number of competitors, keeping prices and the masters' incomes high."],
    "Some guilds also kept common funds to support members who fell ill and the widows of masters who died.",
    "Sentence [[1]] describes the apprenticeship requirement, sentence [[2]] gives its 'official justification' of quality, sentence [[3]] ('Yet') offers evidence that does not fit that justification, and sentence [[4]] interprets 'Such patterns' as a hidden purpose of restricting competition. Sentence [[X]] uses the paragraph's vocabulary of guilds and masters, but it describes a welfare function of guilds that plays no part in the argument about what apprenticeship was really for.",
    "Accepting sentence [[X]] because it mentions guilds and masters, without checking whether it serves the contrast between the stated and the real purpose of apprenticeship.",
    "V03D-guild-apprenticeship",
    "The odd sentence shares the subject and key nouns; it is rejected because it describes a different guild activity, not apprenticeship's purpose.",
    traps=[(2, "Sentence [[2]] can look like a mere aside, but the 'Yet' of sentence [[3]] answers exactly this official justification, so the argument needs it.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 003
ooo("V03-D-003", "History and politics",
    "A census does not merely record a population; the categories it counts can help to create the divisions it reports.", "Difficult",
    ["A census is usually imagined as a mirror, recording a population that exists independently of the act of counting it.",
     "But every census must decide in advance which categories it will count, and those decisions are made by officials with administrative purposes of their own.",
     "Once a category appears on the form, it begins to matter: resources are allocated by it, political claims are framed in its terms, and people learn to describe themselves through it.",
     "Over time, then, the census can help to produce the very divisions it claims merely to report, so that the mirror ends up shaping the face it reflects."],
    "Because a census depends on the willingness of households to answer truthfully, a population that distrusts officials may be badly undercounted.",
    "Sentence [[1]] states the common picture of the census as a mirror, sentence [[2]] ('But') points out that its categories are chosen in advance by officials, sentence [[3]] shows how a counted category 'begins to matter', and sentence [[4]] concludes ('then') that the census can produce the divisions it reports, returning to the mirror image. Sentence [[X]] also questions how faithfully a census reflects a population, which makes it tempting, but it is about inaccurate counting. That worry assumes a fixed population that a better count would capture, which is the very picture the paragraph argues against; the paragraph is about how the categories shape the people counted, not about undercounting.",
    "Taking sentence [[X]] as part of the critique of the mirror picture because it too finds fault with the census, without noticing that undercounting is a failure of accuracy, not an effect of categories.",
    "V03D-census-and-state-power",
    "The odd sentence shares the vocabulary of census, officials and population, and even seems to criticise the census; it is rejected only by seeing that the argument concerns categories that construct, not counts that miss.",
    traps=[(2, "Sentence [[2]] can look like a remark about bureaucracy, but it is the turn of the argument: 'which categories it will count' is what sentence [[3]] picks up with 'Once a category appears on the form'."),
           (1, "Sentence [[1]] is needed because 'the mirror' in sentence [[4]] refers back to the image it introduces.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 004
ooo("V03-D-004", "History and politics",
    "Cheap, uniform, prepaid postage turned the letter from a commercial luxury into a part of ordinary private life.", "Medium",
    ["Before postal reform, sending a letter was often expensive, and the charge, which rose with distance, was commonly paid by the person who received it.",
     "Such a system made correspondence a luxury of merchants and the comfortable classes, and it invited evasions, such as a coded mark on the outside of a letter that the recipient read and then refused to pay for.",
     "When a single low rate, prepaid by the sender, replaced the old scale, the number of letters rose sharply as ordinary families began to write to one another.",
     "Cheap postage thus did more than lower a price; it turned the letter from an occasional commercial instrument into a routine part of private life."],
    "The adhesive stamp, introduced to show that the fee had been paid, soon attracted collectors, who came to prize misprinted issues above all others.",
    "Sentence [[1]] describes the old, costly system, sentence [[2]] shows its effects ('Such a system'), sentence [[3]] describes the reform and the growth in letters among 'ordinary families', and sentence [[4]] draws the conclusion ('thus') about the letter's new place in private life. Sentence [[X]] belongs to the history of postage, but stamp collecting has no bearing on how cheap postage changed who wrote letters.",
    "Accepting sentence [[X]] because it mentions the prepaid fee, which sentence [[3]] also mentions, without asking whether collecting stamps serves the argument.",
    "V03D-cheap-uniform-postage",
    "The odd sentence shares the vocabulary of fees and prepayment; it is rejected because it turns to collecting rather than letter writing.",
    traps=[(2, "Sentence [[2]] can look like an anecdote, but it establishes that correspondence was a 'luxury of merchants and the comfortable classes', which is the contrast sentence [[3]] needs for 'ordinary families'.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 005
ooo("V03-D-005", "Economics and business",
    "A loss leader works because shoppers drawn by one bargain buy other, profitable goods.", "Easy",
    ["Supermarkets sometimes sell a few popular items, such as milk or bread, at a price below what the items cost them.",
     "The logic of this loss leader is that shoppers drawn in by the bargain will rarely buy only the discounted item.",
     "Once in the store, they fill their baskets with other goods carrying ordinary margins, and the profit on these more than covers the loss.",
     "The strategy works best, therefore, when the bargain item is one that shoppers buy often and can compare easily, so that the low price is noticed."],
    "Supermarkets also tend to place fresh fruit and vegetables near the entrance, where bright colours give an impression of freshness.",
    "Sentence [[1]] describes selling some items below cost, sentence [[2]] names 'this loss leader' and gives its logic, sentence [[3]] completes the logic by showing where the profit comes from, and sentence [[4]] draws the practical conclusion ('therefore') about which items suit the strategy. Sentence [[X]] is about supermarkets too, but it describes a different selling tactic, store layout, which has no connection with pricing below cost.",
    "Treating any sentence about supermarket tactics as part of the paragraph, without checking that it concerns the loss leader.",
    "V03D-loss-leader-pricing",
    "The odd sentence is about a different tactic and is easy to reject once the paragraph's single subject is seen.",
    traps=[(4, "Sentence [[4]] might seem an afterthought, but it follows from the logic of sentence [[2]]: the bargain can draw shoppers in only if they notice it.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 006
ooo("V03-D-006", "Economics and business",
    "In common-value auctions, winning signals over-optimism, so a sensible bidder bids below its own estimate.", "Difficult",
    ["When several firms bid for the right to drill an oilfield, each forms its own estimate of how much oil lies underground, and these estimates scatter around the true amount.",
     "The firm that wins is the one whose estimate was highest, and the highest of many scattered estimates is likely to be too high.",
     "Winning therefore carries bad news: it tells the winner that it was probably the most optimistic bidder in the room, not the most perceptive.",
     "A bidder who understands this will deliberately bid below its own estimate, and the more rivals it faces, the further below it should go."],
    "Oil companies also face the danger that prices will fall between the auction and the first barrel, a risk that no estimate of the reserves can remove.",
    "Sentence [[1]] sets up scattered estimates of a single true value, sentence [[2]] notes that the winner holds the highest estimate, which is likely to be too high, sentence [[3]] draws the consequence ('therefore') that winning is bad news, and sentence [[4]] gives the rational response, bidding below one's estimate, the more so as rivals multiply. Sentence [[X]] shares the oilfield, the auction and even the danger of overpaying, but the risk it describes, a fall in prices, has nothing to do with the statistical pitfall of being the most optimistic estimator, and nothing in sentence [[4]] answers it.",
    "Picking a coherent sentence because sentence [[X]] also describes a way in which the winning firm can lose money, and so seems to belong to the same argument.",
    "V03D-winners-curse-in-auctions",
    "The odd sentence shares the setting and the theme of overpaying; separating it requires seeing that the paragraph is about the selection effect of winning, not market risk in general.",
    traps=[(4, "Sentence [[4]] can look like advice tacked on, but 'this' refers to the bad news of sentence [[3]], and 'the more rivals' follows from the logic of sentence [[2]]: more estimates make the highest one more likely to be too high."),
           (1, "Sentence [[1]] is essential because the idea that estimates 'scatter around the true amount' is what makes the highest estimate likely to be too high in sentence [[2]].")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 007
ooo("V03-D-007", "Economics and business",
    "Free-delivery thresholds lead shoppers to spend more while feeling they have saved, which is why retailers use them.", "Medium",
    ["Many online shops charge for delivery on small orders but waive the charge once a basket passes a set value.",
     "Shoppers just short of the threshold often add an item they had not planned to buy, reasoning that it is better to get something for the money than to pay for delivery.",
     "The added item frequently costs more than the delivery charge would have, so the customer spends more in total while feeling that she has saved.",
     "For the retailer, the threshold is thus less a gift than a lever, and it works best when it is set just above the value of a typical basket."],
    "Delivery charges themselves have become harder to justify as warehouses have automated and couriers have competed for the business of large retailers.",
    "Sentence [[1]] describes the threshold, sentence [[2]] shows how shoppers near it respond, sentence [[3]] shows the result, that they spend more while feeling they have saved, and sentence [[4]] concludes ('thus') that the threshold is a lever for the retailer. Sentence [[X]] shares the words delivery charges and retailers, but it raises a separate question, whether such charges are justified by costs, which has nothing to do with how the threshold changes shoppers' behaviour.",
    "Accepting sentence [[X]] because it mentions delivery charges, which every sentence of the paragraph is built around, without checking its function.",
    "V03D-free-delivery-thresholds",
    "The odd sentence shares the central term and is rejected on function: it is about the cost of delivery, not the psychology of the threshold.",
    traps=[(4, "Sentence [[4]] belongs: it draws the conclusion from sentence [[3]], and its point about where the threshold is set follows from the behaviour of shoppers 'just short of the threshold' in sentence [[2]].")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 008
ooo("V03-D-008", "Economics and business",
    "Franchising harnesses owners' incentives but risks quality shortcuts that damage a shared brand, hence its strict rules.", "Medium",
    ["A company that wishes to open hundreds of outlets faces a choice between running them through salaried managers and selling the right to run them to local owners.",
     "Franchising takes the second path, on the reasoning that an owner who keeps the profits will work harder and watch costs more closely than any employee.",
     "The difficulty is that a single owner who cuts corners on quality saves money for herself while damaging a brand shared by every outlet.",
     "This is why franchise agreements are so detailed, specifying everything from ingredients to opening hours, and why head offices send inspectors unannounced."],
    "Many franchise owners are first-time entrepreneurs, attracted by the security of a proven formula rather than by the freedom to invent their own.",
    "Sentence [[1]] sets out the choice between managers and owners, sentence [[2]] says franchising takes 'the second path' and why, sentence [[3]] states 'The difficulty' that the owner's incentive creates, and sentence [[4]] explains ('This is why') the detailed rules and inspections as the answer to that difficulty. Sentence [[X]] talks about franchise owners, but it describes why people become franchisees, which plays no part in the argument about incentives, quality and control.",
    "Choosing sentence [[1]] because it describes a general choice rather than franchising itself, though 'the second path' in sentence [[2]] depends on it.",
    "V03D-franchising",
    "The odd sentence shares the subject and the figure of the owner; it is rejected because it concerns the owner's motives for joining, not the incentive problem.",
    traps=[(1, "Sentence [[1]] is required: 'the second path' in sentence [[2]] makes sense only after the two options have been set out.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 009
ooo("V03-D-009", "Science and environment",
    "Because lichens draw everything from the air, surveys of their species give a cheap, long-term gauge of air quality.", "Easy",
    ["Lichens absorb water and nutrients directly from the air and rain, since they have no roots through which to draw them from the soil.",
     "This makes them unusually exposed to whatever the air carries, and many species die off where pollutants such as sulphur dioxide are common.",
     "Because different species tolerate different levels of pollution, a survey of which lichens grow on a town's trees and walls can serve as a cheap gauge of its air.",
     "Such surveys cannot replace instruments, but they record conditions over years rather than hours, which no single reading can do."],
    "Some lichens have long been gathered to make dyes for wool, giving traditional cloth its browns and purples.",
    "Sentence [[1]] explains that lichens draw everything from the air, sentence [[2]] draws the consequence ('This makes them unusually exposed') for pollution, sentence [[3]] shows how a survey of species can gauge air quality, and sentence [[4]] states what 'Such surveys' can and cannot do. Sentence [[X]] is about lichens, but their use for dyes has nothing to do with their sensitivity to pollution.",
    "Picking sentence [[4]] because it concedes a limitation, though it is the paragraph's qualified conclusion about the surveys of sentence [[3]].",
    "V03D-lichens-as-pollution-indicators",
    "The odd sentence names the paragraph's subject but has no link with the argument about pollution.",
    traps=[(4, "Sentence [[4]] belongs: 'Such surveys' refers to the survey in sentence [[3]], and it rounds off the argument by weighing the method against instruments.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 010
ooo("V03-D-010", "Science and environment",
    "Plants that pay animals with fruit to spread their seeds suffer when hunting removes the large animals they depend on.", "Medium",
    ["A fleshy fruit is a kind of payment: the plant surrounds its seeds with sugar so that an animal will eat them and carry them elsewhere.",
     "Many seeds survive the passage through a gut and are deposited far from the parent tree, where they escape the shade and pests that crowd around it.",
     "Trees with very large seeds, however, depend on the few animals big enough to swallow them, such as large birds and mammals.",
     "When hunting removes those animals from a forest, such trees may go on fruiting for decades while producing almost no seedlings away from their parents."],
    "Other plants rely on the wind instead, equipping their seeds with wings or tufts of fluff that let them drift a long way.",
    "Sentence [[1]] presents fruit as payment for transport by animals, sentence [[2]] explains the benefit of being carried away from the parent, sentence [[3]] ('however') narrows to large-seeded trees that depend on a few large animals, and sentence [[4]] shows what happens when 'those animals' are hunted out. Sentence [[X]] is about seed dispersal, but it turns to plants that do not use animals at all, and nothing in the argument about animal carriers and their loss builds on it.",
    "Accepting sentence [[X]] as a natural contrast because it is about seeds travelling, without noticing that the paragraph's argument concerns dependence on animals.",
    "V03D-seed-dispersal-by-animals",
    "The odd sentence shares the topic of seed travel and looks like a legitimate contrast; it is rejected because the paragraph is about dependence on animal carriers.",
    traps=[(3, "Sentence [[3]] can look like a new topic, but 'those animals' in sentence [[4]] refers to the large birds and mammals it names, so it cannot be removed.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 011
ooo("V03-D-011", "Science and environment",
    "Beaver dams create wetlands that store water and support life, so beavers can restore land cheaply, though not without conflict.", "Medium",
    ["By felling trees and piling branches across streams, beavers turn fast-running channels into chains of ponds and marshes.",
     "The dams slow the water, so that more of it soaks into the surrounding ground instead of rushing downstream after every storm.",
     "The resulting wetlands hold water through dry spells, shelter insects, fish and birds, and can even check the spread of fire across the land around them.",
     "For this reason, some conservationists see the return of beavers as a kind of restoration that does for nothing what engineers would charge heavily to imitate, though landowners whose fields flood may disagree."],
    "Beavers were once hunted heavily for their fur, which was made into felt for the hats that were fashionable in Europe for a long time.",
    "Sentence [[1]] describes how beavers build ponds and marshes, sentence [[2]] explains how the dams slow water, sentence [[3]] lists the benefits of 'The resulting wetlands', and sentence [[4]] concludes ('For this reason') that the return of beavers is a cheap form of restoration, with a concession about flooded fields. Sentence [[X]] can seem to explain why beavers need to 'return', but the paragraph is about what beavers do to land and water, and the fur trade plays no part in that argument. Placed before sentence [[4]], it would even make 'For this reason' point to hunting.",
    "Accepting sentence [[X]] because sentence [[4]] speaks of the 'return of beavers', which seems to call for an account of their disappearance.",
    "V03D-beaver-dams-and-wetlands",
    "The odd sentence shares the subject and seems to connect with the word 'return'; it is rejected because the argument is about the effects of dams.",
    traps=[(2, "Sentence [[2]] belongs: it explains the mechanism, slowed water soaking into the ground, that produces the water-holding wetlands of sentence [[3]].")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 012
ooo("V03-D-012", "Science and environment",
    "Removing an introduced predator from a long-altered island is not simple subtraction; eradication must be planned for the whole system.", "Difficult",
    ["On islands where introduced rats prey on the eggs and chicks of seabirds, removing the rats has in many cases allowed the colonies to recover.",
     "Such successes have made eradication look like a simple act of subtraction, in which taking away the intruder restores what was there before.",
     "Yet on islands altered for centuries, the intruder may have become part of the system, keeping in check some other newcomer, such as introduced mice or an invasive weed whose seeds the rats ate.",
     "The lesson is not that eradication is a mistake but that it must be planned for the whole altered system, since the island that results will be a new one rather than the old one restored."],
    "Poison baits laid for rats can also kill native birds that eat them, so eradication teams sometimes capture and hold vulnerable species until the poison has broken down.",
    "Sentence [[1]] reports the successes of removing rats, sentence [[2]] describes the picture those successes created ('a simple act of subtraction'), sentence [[3]] ('Yet') shows why the picture fails on long-altered islands, where the rats may be holding back another newcomer, and sentence [[4]] draws the qualified lesson about planning for 'the whole altered system'. Sentence [[X]] also complicates eradication, which makes it tempting, but it is about a hazard of the method, poison reaching native birds during the operation. The paragraph's point is about what the ecosystem becomes once the intruder is gone, and sentence [[4]]'s 'the island that results will be a new one' answers sentence [[3]], not sentence [[X]].",
    "Treating sentence [[X]] as one more reason why eradication is not simple, without separating a temporary side effect of poisoning from the lasting ecological interdependence the paragraph argues for.",
    "V03D-eradicating-island-predators",
    "The odd sentence shares vocabulary and even the theme of unexpected harm from eradication; it is rejected only by seeing that the argument concerns the system left behind, not the method used.",
    traps=[(1, "Sentence [[1]] is needed: 'Such successes' in sentence [[2]] refers to the recovering colonies it describes."),
           (2, "Sentence [[2]] can look like a restatement of sentence [[1]], but it introduces the 'simple act of subtraction' view that sentence [[3]] rejects with 'Yet'.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 013
ooo("V03-D-013", "Technology",
    "Interfaces that profit from users' inattention cannot claim user consent as their justification.", "Medium",
    ["On some booking pages, the box agreeing to costly travel insurance is ticked in advance, and declining it means clicking a pale link worded to sound reckless.",
     "Such tricks are known as dark patterns: layouts that exploit predictable habits of attention, so that the choice the firm prefers is also the one that takes the least effort.",
     "Their defenders point out that every option is technically available to a user who reads carefully.",
     "But a design that profits precisely from the fact that people do not read carefully cannot claim the user's consent as its justification."],
    "Interface designers also spend much effort on accessibility, enlarging buttons and adding captions so that people with impaired sight or hearing can use a site.",
    "Sentence [[1]] gives an example of a manipulative website, sentence [[2]] names 'Such tricks' as dark patterns and explains how they work, sentence [[3]] reports the defence that every option is available to a careful reader, and sentence [[4]] ('But') rebuts that defence. Sentence [[X]] shares the vocabulary of interface design, but it describes design that helps users, which plays no part in the argument about manipulation and consent.",
    "Accepting sentence [[X]] because it is about how designers lay out a site, as sentence [[2]] is, without checking that it bears on the argument about consent.",
    "V03D-dark-patterns-in-interfaces",
    "The odd sentence shares design vocabulary and is rejected on function; the four coherent sentences form an example, a definition, an objection and a reply.",
    traps=[(3, "Sentence [[3]] can look like it argues against the paragraph, but the 'But' of sentence [[4]] answers it directly, and 'read carefully' is repeated to turn the defence against itself.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 014
ooo("V03-D-014", "Technology",
    "Turn-by-turn directions spare drivers the effort that builds a mental map, so heavy reliance may weaken their sense of direction.", "Easy",
    ["A driver following spoken turn-by-turn directions need never form a picture of the route as a whole.",
     "She attends only to the next instruction, and once the turn is made, it can safely be forgotten.",
     "Finding one's way without such help, by contrast, forces a person to relate landmarks to one another, and this effort is what builds a mental map of a city.",
     "It is plausible, then, that heavy reliance on navigation apps leaves people less able to find their way when the signal fails."],
    "Navigation apps also reroute drivers around traffic jams, sometimes sending heavy traffic down quiet residential streets.",
    "Sentence [[1]] says a driver following directions need not picture the whole route, sentence [[2]] explains why, sentence [[3]] ('by contrast') describes how finding one's own way builds a mental map, and sentence [[4]] draws the cautious conclusion ('then') about heavy reliance on apps. Sentence [[X]] is about navigation apps, but its point about traffic on residential streets has nothing to do with how people learn to find their way.",
    "Choosing sentence [[2]] as a repetition of sentence [[1]], though it supplies the reason the whole route is never pictured.",
    "V03D-satellite-navigation-and-spatial-memory",
    "The odd sentence names the same technology but is about traffic, not memory; the coherent sentences are linked by 'by contrast' and 'then'.",
    traps=[(2, "Sentence [[2]] is not a mere repetition: it explains how the driver gets by without a picture of the route, which sentence [[3]] then contrasts with finding one's own way.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 015
ooo("V03-D-015", "Technology",
    "Old software often holds an organisation's only complete record of its rules, so it should be read like an archive before it is replaced.", "Difficult",
    ["Banks and government agencies still run systems written decades ago, and outsiders often treat this as a simple failure to modernise.",
     "Yet such systems are frequently the only complete record of the rules an organisation actually follows, since every exception and special case added over the years lives in the code and nowhere else.",
     "A team that sets out to replace one must first rediscover those rules, many of which no current employee can state, and it is at this step that ambitious rewrites tend to founder.",
     "None of this means that old systems should never be replaced; it means that they should be approached as archives to be read before they are treated as obstacles to be removed."],
    "The programmers who know the oldest languages are retiring, and organisations that depend on such code must pay a premium for the few who remain.",
    "Sentence [[1]] reports the outsider's view that running old systems is a failure to modernise, sentence [[2]] ('Yet') answers that such systems hold the only record of the organisation's rules, sentence [[3]] shows why this makes replacement hard ('those rules'), and sentence [[4]] concedes that replacement is not ruled out while concluding that old systems should be treated as archives. Sentence [[X]] shares the subject and seems to echo 'no current employee', but it is about a shortage of programmers who can read old languages, a labour problem that the argument about undocumented rules never uses; sentence [[4]]'s advice to read the systems as archives answers sentence [[3]], not a skills shortage.",
    "Accepting sentence [[X]] because it, like sentence [[3]], mentions people who understand the old systems, without seeing that the paragraph's difficulty is lost rules, not scarce programmers.",
    "V03D-legacy-software-maintenance",
    "The odd sentence shares the subject and seems to connect with the remark about employees; it is rejected only by tracking what the argument's difficulty actually is.",
    traps=[(1, "Sentence [[1]] states the view the paragraph corrects; without it, the 'Yet' of sentence [[2]] has nothing to answer."),
           (4, "Sentence [[4]] might look like a hedge that could be dropped, but it is the conclusion, and 'archives to be read' picks up the idea in sentence [[2]] that the code is the only record.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 016
ooo("V03-D-016", "Technology",
    "Backups protect data only when the copies cannot all be destroyed by the same event.", "Easy",
    ["A single backup of important files offers less protection than most people assume.",
     "If the backup sits on a drive in the same room as the computer, a fire, a flood or a burglary can destroy both at once.",
     "For this reason, careful users keep several copies, on different kinds of media, with at least one stored in a separate place.",
     "The principle is that copies protect against loss only when they cannot all be destroyed by the same event."],
    "Many people also find that sorting their files into clearly named folders saves time when they need to find an old document.",
    "Sentence [[1]] makes the claim that one backup protects less than people think, sentence [[2]] gives the reason, sentence [[3]] ('For this reason') gives the careful practice, and sentence [[4]] states the principle behind it. Sentence [[X]] is about managing files, but it concerns finding documents quickly, not protecting them against loss.",
    "Choosing sentence [[4]] because it restates rather than adds, though it states the general principle that ties the example to the practice.",
    "V03D-backup-redundancy",
    "The odd sentence moves to a different file habit and has no link with protection against loss.",
    traps=[(4, "Sentence [[4]] belongs: it generalises from the shared fire, flood or burglary in sentence [[2]] to the rule behind the practice in sentence [[3]].")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 017
ooo("V03-D-017", "Arts and literature",
    "The collapse in value of an exposed forgery is not mere snobbery, since a painting is valued as a record of a particular achievement.", "Medium",
    ["When a painting admired for decades is exposed as a forgery, its market value collapses, although not a single brushstroke on the canvas has changed.",
     "Some take this as proof that collectors buy names rather than beauty, and that the art market rests on snobbery.",
     "But the reaction is not as irrational as it looks, for a painting is valued not only as a pleasing surface but as the record of a particular artist's achievement at a particular moment.",
     "A forgery may match that surface perfectly, yet it records a different and lesser achievement: the skill of imitating a discovery rather than making one."],
    "Detecting forgeries has become a scientific discipline, in which experts analyse pigments to find materials that did not exist when the work was supposedly painted.",
    "Sentence [[1]] states the puzzle that an exposed forgery loses its value although nothing on the canvas changes, sentence [[2]] gives one explanation (snobbery), sentence [[3]] ('But') rejects it and offers another, and sentence [[4]] applies that explanation to the forgery ('that surface'). Sentence [[X]] is about forgeries, but it describes how they are detected, which has no bearing on why a forgery is worth less once exposed.",
    "Accepting sentence [[X]] because it shares the word 'forgery' and seems to explain how a painting comes to be 'exposed', without checking whether it serves the argument about value.",
    "V03D-art-forgeries-and-value",
    "The odd sentence shares the central term and even the idea of exposure; it is rejected because the paragraph is about value, not detection.",
    traps=[(2, "Sentence [[2]] is not the author's view, but it must stay: the 'But' of sentence [[3]] rebuts it, and the argument is built as an answer to it.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 018
ooo("V03-D-018", "Arts and literature",
    "Concert silence is a recent custom rooted in the idea of music as a unified work, which is why breaking it feels like an offence against the music.", "Difficult",
    ["The hushed audience of the modern concert hall, which suppresses even a cough until the end of a movement, is a more recent custom than most listeners suppose.",
     "Audiences in earlier centuries often talked, ate and applauded a favourite passage while the music was still playing, and nobody thought the performance spoiled.",
     "The change followed a new idea of what a piece of music was: no longer an entertainment accompanying a social occasion but a unified work whose meaning lay in its entire course.",
     "Silence, on this view, is not a mere rule of etiquette but a way of honouring the work's claim to be heard whole, which is why breaking it now feels like an offence against the music rather than against the neighbours."],
    "Some orchestras now hold relaxed performances at which talking and moving about are welcomed, hoping to attract listeners who find the formal hall intimidating.",
    "Sentence [[1]] claims that the silent audience is a recent custom, sentence [[2]] supports this with the behaviour of earlier audiences, sentence [[3]] explains 'The change' by a new idea of the musical work, and sentence [[4]] interprets silence 'on this view' as a way of honouring the work. Sentence [[X]] shares the vocabulary of halls and talking audiences, and it can even seem to follow from the custom being recent, but it is about present-day efforts to widen the audience. The paragraph explains why silence arose and what it means; nothing in it concerns making concerts less intimidating, and sentence [[4]] already closes the argument.",
    "Taking sentence [[X]] as a natural ending, a return to talking audiences, without noticing that it changes the question from what silence means to how orchestras attract newcomers.",
    "V03D-silence-of-concert-audiences",
    "The odd sentence shares the paragraph's vocabulary and could pass as a closing remark; it is rejected only by seeing that the argument is about the meaning of silence, not access to concerts.",
    traps=[(2, "Sentence [[2]] can look like a historical aside, but it is the evidence for the claim in sentence [[1]], and 'The change' in sentence [[3]] is the change from these earlier habits."),
           (4, "Sentence [[4]] is the conclusion: 'on this view' refers to the idea of the unified work in sentence [[3]], so it cannot be the sentence that does not belong.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 019
ooo("V03-D-019", "Arts and literature",
    "Fidelity is the wrong test for a film adaptation; the question is whether it achieves a comparable effect by cinematic means.", "Medium",
    ["Reviewers of film adaptations often complain that the film is unfaithful to the book, as if fidelity were the obvious measure of success.",
     "Yet much of what makes a novel distinctive, such as the narrator's voice and long passages of a character's private thought, has no direct equivalent on screen.",
     "A film that tries to reproduce such passages literally, through endless voice-over, usually ends up less true to the book than one that finds visual means of conveying the same inner life.",
     "The better question is therefore not whether a film copies its source but whether it achieves, by its own means, something of the effect the source achieved by its own."],
    "The film rights to a successful novel are sometimes sold before the book is even published, occasionally for more than the author was paid to write it.",
    "Sentence [[1]] reports the complaint that adaptations are unfaithful, sentence [[2]] ('Yet') notes that much of a novel has no screen equivalent, sentence [[3]] shows that literal copying of 'such passages' makes a film less true to the book, and sentence [[4]] concludes ('therefore') with a better standard. Sentence [[X]] links films and novels, but it is about the business of buying rights, which has no bearing on how an adaptation should be judged.",
    "Accepting sentence [[X]] because it is about turning novels into films, without checking that it bears on fidelity as a standard.",
    "V03D-film-adaptation-of-novels",
    "The odd sentence shares the subject of novels becoming films; it is rejected because it concerns money, not the standard for judging adaptations.",
    traps=[(3, "Sentence [[3]] is needed: it turns the observation of sentence [[2]] into an argument, showing that literal copying defeats fidelity, which is what sentence [[4]] builds on.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 020
ooo("V03-D-020", "Arts and literature",
    "Strict verse forms push poets past obvious phrasing and so work as tools for originality rather than limits.", "Easy",
    ["Strict verse forms, with their fixed number of lines and demanding rhyme schemes, can look like cages that a free imagination ought to escape.",
     "Many poets have found the opposite, because the need to fit a rhyme or a metre forces them past the first, most obvious phrase that comes to mind.",
     "In searching for a word that both sounds right and means right, they often stumble on an image they would never have reached by a direct route.",
     "The form, in other words, works less as a limit than as a tool for surprising the poet into originality."],
    "Poetry readings have become popular in cafes and bookshops, where audiences often seem to prefer loose, conversational verse.",
    "Sentence [[1]] states the view that strict forms are cages, sentence [[2]] reports 'the opposite' experience and its reason, sentence [[3]] shows how the search for a fitting word leads to new images, and sentence [[4]] sums up ('in other words') that form is a tool for originality. Sentence [[X]] is about poetry, but it concerns where poems are read and what audiences like, not how constraints affect the writing of verse.",
    "Choosing sentence [[1]] because it states a view the paragraph rejects, though 'the opposite' in sentence [[2]] depends on it.",
    "V03D-fixed-verse-forms",
    "The odd sentence is on poetry but about audiences and venues, clearly outside the argument about constraint.",
    traps=[(1, "Sentence [[1]] must stay: 'the opposite' in sentence [[2]] has meaning only as a reply to the view that forms are cages.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 021
ooo("V03-D-021", "Language and media",
    "Polite replacements for embarrassing words absorb the old discomfort, so renaming helps only as long as attitudes change with it.", "Medium",
    ["Words for things that embarrass us tend to wear out, and the polite term of one generation often sounds blunt to the next.",
     "The room once delicately called a water closet acquired a series of gentler names, each adopted because the last had come to seem too direct.",
     "The pattern suggests that a new word cannot by itself cleanse an uncomfortable subject, since the discomfort soon attaches to whatever word is used.",
     "Renaming is not pointless, for a fresh term can signal a change in attitude, but its effect lasts only as long as the attitude does."],
    "Some words drift in the opposite direction, so that a term once thought coarse becomes acceptable in polite company.",
    "Sentence [[1]] states the claim that polite words for embarrassing things wear out, sentence [[2]] illustrates it with the water closet, sentence [[3]] draws the lesson of 'The pattern', and sentence [[4]] qualifies it by saying renaming is not pointless. Sentence [[X]] is about words changing in politeness, which makes it look relevant, but it describes movement the other way, coarse to acceptable; the argument is about polite words absorbing discomfort, and nothing in sentences [[3]] or [[4]] draws on words becoming respectable.",
    "Accepting sentence [[X]] because it also describes words changing their social standing, without noticing that it runs against the direction the argument depends on.",
    "V03D-euphemism-treadmill",
    "The odd sentence shares the theme of shifting politeness and looks like a contrast; it is rejected because the argument uses only the wearing out of polite terms.",
    traps=[(4, "Sentence [[4]] can look like a retreat from the argument, but it is the qualified conclusion: having said in sentence [[3]] that a word cannot cleanse a subject, it explains what renaming can still do.")],
    cognitive="Analysis")

# ------------------------------------------------------------------ 022
ooo("V03-D-022", "Language and media",
    "Emoji restore some of the tone that typed messages lose, so they repair the medium rather than corrupt writing.", "Easy",
    ["In face-to-face talk, much of a sentence's meaning is carried by tone of voice, facial expression and gesture.",
     "A short typed message strips all of this away, so that a remark meant as a joke can easily be read as a rebuke.",
     "Emoji have spread partly because they restore some of the missing signals, a smile marking a comment as playful or a wink as ironic.",
     "Seen this way, they are less a decline in writing than a repair to a medium that was never designed to carry tone."],
    "Some companies design their own emoji sets, so the same symbol may look noticeably different on two brands of phone.",
    "Sentence [[1]] notes how much meaning tone and gesture carry in speech, sentence [[2]] says a typed message 'strips all of this away', sentence [[3]] explains that emoji restore 'the missing signals', and sentence [[4]] concludes ('Seen this way') that they repair the medium. Sentence [[X]] mentions emoji, but it is about how different phones draw them, which has nothing to do with restoring tone.",
    "Choosing sentence [[1]] because it does not mention emoji or messages, though 'all of this' in sentence [[2]] refers to it.",
    "V03D-emoji-and-tone-in-messages",
    "The odd sentence names emoji but is about their design across devices, outside the argument about tone.",
    traps=[(1, "Sentence [[1]] belongs: 'all of this' in sentence [[2]] refers to the tone, expression and gesture it lists.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 023
ooo("V03-D-023", "Language and media",
    "Phonetic spelling reform has costs, a choice of accent, hidden word links and old-looking books, that explain why it is rarely adopted.", "Easy",
    ["English spelling is notoriously irregular, and reformers have long proposed that words be written as they sound.",
     "The proposal is less simple than it appears, because speakers in different regions pronounce many words differently, and a phonetic spelling would have to choose one accent over the others.",
     "Sound-based spelling would also hide the links between related words, such as the shared root of 'sign' and 'signature', which the present spelling preserves.",
     "These costs, added to the burden of making every existing book look old-fashioned, explain why reform has been proposed so often and adopted so rarely."],
    "Spelling bees, in which children compete to spell difficult words aloud, remain popular in several English-speaking countries.",
    "Sentence [[1]] introduces the reformers' proposal, sentence [[2]] gives one cost (a single accent must be chosen), sentence [[3]] adds another ('also'), and sentence [[4]] sums up 'These costs' to explain why reform rarely succeeds. Sentence [[X]] is about English spelling, but spelling competitions have nothing to do with the case for or against reform.",
    "Choosing sentence [[3]] because its example of related words seems a separate point, though 'also' links it to sentence [[2]] as a second cost.",
    "V03D-spelling-reform",
    "The odd sentence shares the subject but has no role in the argument about reform; the coherent sentences are tied by 'also' and 'These costs'.",
    traps=[(3, "Sentence [[3]] is the second of 'These costs' summed up in sentence [[4]], so removing it would leave the conclusion with less to rest on.")],
    cognitive="Understanding")

# ------------------------------------------------------------------ 024
ooo("V03-D-024", "Language and media",
    "Indirect requests give both sides room, but politeness seeks the degree of indirectness that fits the relationship, not the most.", "Difficult",
    ["Someone who asks 'Could you pass the salt?' is not, of course, enquiring about the listener's physical abilities.",
     "The question form is used because it leaves the listener a way to decline without open refusal, and spares the speaker the appearance of giving an order.",
     "Yet it does not follow that the more indirect a request, the more polite it is, since elaborate hedging between close friends can sound cold or even sarcastic.",
     "What politeness seeks is not the greatest indirectness but the degree of it that fits the relationship, and misjudging it in either direction gives offence."],
    "Languages differ in how they mark politeness, and some build it into verb endings, so that a speaker cannot form a sentence without signalling the listener's status.",
    "Sentence [[1]] observes that a request phrased as a question is not really about ability, sentence [[2]] explains why 'The question form' is used, sentence [[3]] ('Yet') warns against concluding that more indirectness is always more polite, and sentence [[4]] states the resulting principle of fitting indirectness to the relationship. Sentence [[X]] shares the vocabulary of politeness and even of the listener's status, which echoes 'fits the relationship', but it is about grammatical marking of politeness across languages. The paragraph is about how indirect a request should be, and grammatical politeness markers have nothing to do with that question.",
    "Accepting sentence [[X]] because it mentions politeness and the listener, as the conclusion does, without seeing that grammar is a different means of politeness from indirectness.",
    "V03D-indirect-requests-and-politeness",
    "The odd sentence shares the central term and seems to echo the conclusion; it is rejected only by seeing that the paragraph concerns degrees of indirectness, not grammatical forms.",
    traps=[(1, "Sentence [[1]] gives the example that 'The question form' in sentence [[2]] refers to, so it is needed."),
           (3, "Sentence [[3]] can look like a change of subject to friendship, but it supplies the qualification that sentence [[4]] turns into the principle 'in either direction'.")],
    cognitive="Analysis", exams=D)

# ------------------------------------------------------------------ 025
ooo("V03-D-025", "Language and media",
    "The way podcasts are heard and spoken creates a one-sided intimacy that advertisers exploit.", "Medium",
    ["Podcasts are usually heard alone, through earphones, while the listener walks, cooks or travels to work.",
     "Hosts speak close to the microphone in an unscripted, conversational manner, so that the voice seems to arrive from just beside the listener's ear.",
     "Over months of such listening, many people come to feel that they know the hosts as they know a friend, though the hosts do not know them at all.",
     "Advertisers have learned to exploit this one-sided bond, which is why podcast advertisements are so often read by the hosts themselves in their ordinary voices."],
    "Because a podcast can be made with little more than a microphone and a laptop, the medium has far lower costs of entry than radio once had.",
    "Sentence [[1]] describes how podcasts are heard (alone, through earphones), sentence [[2]] how they are spoken (close to the microphone, conversationally), sentence [[3]] shows how 'such listening' creates a feeling of friendship, and sentence [[4]] explains how advertisers exploit 'this one-sided bond'. Sentence [[X]] shares the words podcast and microphone, but it is about how cheaply podcasts are made, which has nothing to do with the intimacy the paragraph traces from listening to advertising.",
    "Accepting sentence [[X]] because it mentions the microphone, as sentence [[2]] does, without checking that it serves the argument about intimacy.",
    "V03D-podcast-intimacy",
    "The odd sentence shares vocabulary with the paragraph and is rejected on function: it concerns production costs, not the listener's bond with the host.",
    traps=[(1, "Sentence [[1]] can look like scene-setting, but listening alone through earphones is part of what makes the voice feel close, and 'such listening' in sentence [[3]] depends on it.")],
    cognitive="Analysis")
