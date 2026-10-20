import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import *

T = "Cities and space"
DX = ("CAT", "XAT")

# =====================================================================================
# R03-A-01  Upgrading informal settlements in place (Easy)
# =====================================================================================
passage("R03-A-01", T,
    "Upgrading informal settlements where they stand usually serves residents better than clearance and relocation, because a settlement's location sustains its livelihoods, though upgrading has real limits.",
    [
        "For much of the last century, the standard official response to an informal settlement was to remove it. Planners looked at a hillside of self-built houses, narrow lanes and improvised water connections and saw a problem of housing quality, to be solved by demolition and the construction of orderly blocks elsewhere, usually on cheaper land at the edge of the city. The logic seemed humane as well as tidy: people living without drains or secure walls would be given drains and secure walls. That the residents frequently resisted, and that many of the new blocks were half empty within a few years, was read as ingratitude, or as evidence that the poor did not know their own interests.",
        "A different reading is now more common, and it is more persuasive. An informal settlement is not simply a stock of poor dwellings; it is a working arrangement of livelihoods, and its location is usually its chief asset. A family that sells cooked food near a bus depot, a tailor who takes in work from a nearby market, a mother whose children attend a school within walking distance: all of them chose the site because of what it is close to. Relocation to a distant estate improves the walls while destroying the arrangement. The household may gain a toilet and lose two hours a day to travel, or lose the income that made the new rent payable at all. Seen this way, the empty blocks were not a puzzle but a verdict.",
        "Upgrading in place starts from this recognition. Instead of replacing the settlement, it adds what is missing: paved lanes, drainage, water and sewer lines, street lighting and, crucially, some form of secure tenure, so that residents can invest in their houses without fearing that the next official survey will mark them for demolition. Because the residents remain where they are, the networks that sustain them survive, and the public money spent goes into infrastructure rather than into reproducing, at great cost and in the wrong place, a community that already existed.",
        "None of this makes upgrading a universal remedy. Some settlements stand on land that floods every monsoon or slides in heavy rain, and to improve them in place is to invest in a future disaster. Nor is upgrading automatically benign: lanes widened for drainage can require the demolition of some houses, and a programme that installs pipes but withholds tenure leaves residents improved and still insecure. The case for upgrading is therefore not that informal settlements are good as they are, a romantic view their residents rarely share. It is that the people who built them understood something about the city that the planners who wished to clear them did not.",
    ],
    "Easy", "A clear thesis stated early, concrete examples and a plainly signalled concession; little abstraction.",
    "R03A-informal-settlement-upgrading")

rcq("R03-A-01-1", "Main idea / primary purpose", "Easy",
    "The primary purpose of the passage is to",
    "argue that improving informal settlements where they stand generally serves residents better than relocating them, while noting where this approach falls short.",
    [("argue that informal settlements, having been built by their own residents, should be left as they are rather than altered by public authorities.",
      "Paragraph 4 calls the view that settlements are 'good as they are' a romantic one 'their residents rarely share', and paragraph 3 endorses adding lanes, drains and tenure."),
     ("explain why planners in the last century preferred to build replacement housing on cheap land at the edge of the city.",
      "The location of the new blocks is a detail of paragraph 1; the passage as a whole is about why upgrading in place is the better response, so the option is too narrow."),
     ("show that secure tenure matters more to the residents of informal settlements than drains, water supply or paved lanes.",
      "Paragraph 3 lists tenure among the things upgrading adds and calls it crucial, but it never ranks tenure above infrastructure; the option invents a comparison.")],
    "Paragraph 1 describes the old policy of clearance, paragraph 2 explains why it failed (location sustains livelihoods), paragraph 3 presents upgrading in place as the better alternative, and paragraph 4 notes its limits (hazardous land, demolitions, missing tenure). The correct answer captures both the thesis and the concession.",
    "Choosing the option that settlements should be left as they are because the author is sympathetic to residents, and missing the explicit rejection of the romantic view.",
    "The thesis is stated plainly in paragraphs 2 and 3; the distractors are a reversal, a detail and an invented ranking.",
    cognitive="Understanding")

rcq("R03-A-01-2", "Specific detail", "Easy",
    "According to the passage, the relocation blocks were often half empty within a few years because",
    "moving to them cut households off from the work, schools and markets that had made their earlier location valuable.",
    [("the residents were ungrateful and did not understand which kind of housing would serve their interests best.",
      "Paragraph 1 reports this as how officials 'read' the empty blocks; paragraph 2 rejects that reading as less persuasive than the author's own."),
     ("the new blocks lacked the drains and secure walls that the residents had been promised before they agreed to move.",
      "Paragraph 2 says relocation 'improves the walls'; the problem was what the move destroyed, not missing facilities in the blocks."),
     ("the land chosen for the estates was prone to flooding and landslides during the heavy rains of the monsoon.",
      "Flooding and landslides are mentioned in paragraph 4 about some informal settlements, not about the relocation estates.")],
    "Paragraph 2 says families chose their sites 'because of what it is close to', and that relocation to a distant estate 'improves the walls while destroying the arrangement', costing travel time or income. The empty blocks were 'a verdict' on that loss.",
    "Picking the official explanation in paragraph 1, which the author reports only to reject.",
    "The answer is stated in paragraph 2; the main trap is a view the author reports but rejects.",
    cognitive="Recall")

rcq("R03-A-01-3", "Meaning in context", "Easy",
    "In paragraph 2, the statement that the empty blocks were 'not a puzzle but a verdict' means that the empty blocks were",
    "a judgement on relocation that residents delivered by moving out, once the costs of distance are understood.",
    [("an official finding that the new housing had been badly designed and poorly built by the authorities.",
      "No official finding is mentioned, and the passage says relocation improved the walls; the verdict was passed by residents, not by officials."),
     ("a court ruling that later stopped the authorities from clearing further settlements across the city.",
      "The passage mentions no legal proceedings; 'verdict' is used figuratively for the residents' response."),
     ("a mystery that planners could not explain, even after they had studied the residents' reasons closely.",
      "This is the 'puzzle' reading the sentence explicitly denies; once location is understood, the empty blocks need no special explanation.")],
    "The sentence follows the account of what relocation cost households. By leaving the blocks, residents in effect pronounced judgement on the policy; their behaviour is explained, not mysterious, once the importance of location is seen.",
    "Taking 'verdict' literally as a legal or official decision.",
    "Figurative phrase explained by the sentences just before it.",
    cognitive="Understanding")

rcq("R03-A-01-4", "Inference", "Medium",
    "The author would most likely describe a programme that paves the lanes and lays sewers in a settlement but gives residents no protection against eviction as",
    "an incomplete improvement, because residents would remain unwilling to invest in houses they might still lose.",
    [("a successful upgrade, because residents stay where they are and the networks that sustain them are preserved.",
      "Paragraph 3 calls secure tenure crucial to upgrading, and paragraph 4 says a programme that 'installs pipes but withholds tenure' leaves residents 'still insecure', so the author would not call it a success."),
     ("worse than relocation, because improving such a settlement amounts to investing in a future disaster.",
      "The 'future disaster' remark in paragraph 4 concerns settlements on land that floods or slides, not settlements lacking tenure."),
     ("a romantic attempt to keep the settlement exactly as it was, against the wishes of most of its residents.",
      "Paving lanes and laying sewers changes the settlement; the romantic view in paragraph 4 is the belief that settlements are good unchanged.")],
    "Paragraph 3 says tenure is needed 'so that residents can invest in their houses without fearing' demolition, and paragraph 4 says a programme that 'installs pipes but withholds tenure leaves residents improved and still insecure'. The author would see such a programme as falling short.",
    "Choosing the 'successful upgrade' option because staying in place is the advantage the passage stresses, and overlooking the tenure condition.",
    "Requires connecting the tenure clause in paragraph 3 with the caution in paragraph 4; one distractor states a real advantage of upgrading.",
    cognitive="Application")

# =====================================================================================
# R03-A-02  Density versus crowding (Easy)
# =====================================================================================
passage("R03-A-02", T,
    "Density and crowding are different things, and policies that treat them as one misdiagnose urban problems, though density has costs of its own.",
    [
        "Few words in urban debate do as much damage as 'density', largely because it is used, often by the same speaker within a single argument, to mean two quite different things. In its technical sense density is a ratio: the number of people, or of dwellings, on a given area of land. In ordinary speech it usually means something closer to crowding, the experience of too many people in too little room: a family of six in a single room, a queue that spills into the road, a train in which nobody can turn round. The two can occur together, but they need not, and treating them as one has shaped a century of planning.",
        "Consider two districts with the same number of residents per hectare. In the first, people live in tall apartment buildings with generous flats, set among parks and wide streets. In the second, the same population is packed into low houses, several households to a building, with lanes too narrow for a cart. On a map of density the districts are identical; to anyone who lives in them they could hardly be more different. Conversely, a scattered agricultural village, where extended families share a single dwelling, can be acutely crowded indoors while being nearly empty by the hectare. Density, in short, describes land; crowding describes the conditions of daily life.",
        "The confusion has a history. The diseases that ravaged industrial cities in the nineteenth century were widely blamed on density, and reformers responded by trying to spread people out. Yet what made those cities so lethal was a combination of overcrowded rooms, contaminated water and absent sewers, and where water and drains were improved, death rates in dense districts fell even though the districts often remained dense. The reformers were right that something was wrong; they were imprecise about what it was, and the imprecision outlived them, surviving in zoning codes and building regulations long after the sanitary conditions that had justified it had disappeared.",
        "This is not to say that density is costless. Many people living close together compete for parks, school places and quiet, and a district can feel oppressive even when no room in it is overcrowded. Perception counts, and planners who dismiss it will find their schemes resented. But the remedies differ. Crowding is relieved by more floor space per person and by services; the costs of density are managed by design, by open space and by the quality of the street. A policy that caps density in the name of relieving crowding may achieve neither, pushing people into fewer and more crowded rooms, or out to the edge of the city.",
    ],
    "Easy", "One central distinction, illustrated by a concrete comparison and a historical case; the stance is explicit.",
    "R03A-density-versus-crowding")

rcq("R03-A-02-1", "Specific detail", "Easy",
    "According to the passage, density differs from crowding in that",
    "density is a ratio of people or dwellings to land, while crowding concerns too many people for the room they have.",
    [("density is found mainly in large cities, while crowding is a problem that arises chiefly in villages.",
      "Paragraph 2 uses the village only to show that crowding can occur without density; it does not confine either condition to one kind of place."),
     ("density refers to how many people share a room, while crowding refers to how many live on a hectare.",
      "This reverses the definitions in paragraph 1, where density is people 'on a given area of land' and crowding is 'too many people in too little room'."),
     ("density damages the health of residents, while crowding is merely uncomfortable for those who experience it.",
      "Paragraph 3 says the lethal conditions were overcrowded rooms and bad sanitation, and that death rates fell even where districts stayed dense, which is close to the opposite.")],
    "Paragraph 1 defines density technically as 'the number of people, or of dwellings, on a given area of land' and crowding as 'too many people in too little room'; paragraph 2 sums up: 'Density ... describes land; crowding describes the conditions of daily life.'",
    "Reversing the two definitions under time pressure.",
    "Both definitions are stated directly in paragraphs 1 and 2.",
    cognitive="Recall")

rcq("R03-A-02-2", "Structure / function", "Easy",
    "The comparison of two districts with the same number of residents per hectare (paragraph 2) serves mainly to",
    "show that areas equal in density can differ sharply in how crowded daily life within them is.",
    [("prove that tall apartment buildings are always better places to live than low houses on narrow lanes.",
      "The point is that density figures hide differences in living conditions, not that one building type is always superior; the word always goes beyond the example."),
     ("illustrate the method by which nineteenth-century reformers tried to spread the urban population out.",
      "The reformers appear in paragraph 3; the two districts are a hypothetical comparison with no connection to their methods."),
     ("suggest that maps showing population per hectare are usually drawn from inaccurate or outdated figures.",
      "The passage treats the maps as accurate; the districts are identical 'On a map of density', and the point is that density measures land, not daily life.")],
    "The districts share a density figure but one offers generous flats among parks and the other packs several households to a building. The paragraph concludes that 'density ... describes land; crowding describes the conditions of daily life'.",
    "Reading the example as a recommendation of tower blocks.",
    "The function is stated in the paragraph's closing sentence.",
    cognitive="Understanding")

rcq("R03-A-02-3", "Inference", "Medium",
    "The passage suggests that the nineteenth-century reformers mentioned in paragraph 3",
    "rightly sensed that the industrial cities were unhealthy but located the cause in density rather than in rooms and sanitation.",
    [("were mistaken in thinking that anything about conditions in the industrial cities needed to be changed at all.",
      "Paragraph 3 says 'The reformers were right that something was wrong', so the author does not think their concern mistaken."),
     ("succeeded in lowering death rates in industrial cities chiefly by persuading residents to move to less dense districts.",
      "Paragraph 3 credits improved water and drains with lowering death rates, and notes that districts 'often remained dense', so the fall was not due to dispersal."),
     ("deliberately exaggerated the dangers of density in order to win public support for large building programmes.",
      "Nothing is said about the reformers' motives; the passage calls them 'imprecise', which implies an honest error, not deliberate exaggeration.")],
    "The reformers blamed density and tried to 'spread people out', but the lethal factors were 'overcrowded rooms, contaminated water and absent sewers', and death rates fell with better water and drains even where density stayed high. They were 'right that something was wrong' but 'imprecise about what it was'.",
    "Choosing the option that credits dispersal with lower death rates, because reformers acted and death rates fell.",
    "Requires combining the cause of mortality with the observation that density often stayed high; one distractor confuses sequence with cause.",
    cognitive="Analysis")

rcq("R03-A-02-4", "Application / analogy", "Medium",
    "A city has a district in which several families typically share one room. Which approach would the author most likely recommend?",
    "Increasing the floor space available to each household and supplying water and drains, without necessarily reducing residents per hectare.",
    [("Capping the number of residents per hectare and moving those above the limit to new settlements on the edge of the city.",
      "Paragraph 4 warns that capping density to relieve crowding 'may achieve neither', pushing people into more crowded rooms or out to the city's edge."),
     ("Leaving the district as it is, since residents' sense of being crowded counts for less than the measured density of the land.",
      "Paragraph 4 says 'Perception counts' and the district described here is crowded in the literal sense, so the author would not leave it alone."),
     ("Replacing every low house in the district with high towers, because building upward removes crowding wherever it is tried.",
      "The towers in paragraph 2 relieve crowding because their flats are 'generous'; the author never says height by itself removes crowding, and the claim that it works wherever it is tried overreaches.")],
    "Several families to a room is crowding, not merely density. Paragraph 4 says 'Crowding is relieved by more floor space per person and by services', and paragraph 3 shows sanitation lowering death rates without lowering density.",
    "Choosing the density cap because the district sounds 'dense', which is exactly the confusion the passage criticises.",
    "Requires classifying the case as crowding and applying the matching remedy; the tower option borrows the paragraph 2 example.",
    cognitive="Application")

# =====================================================================================
# R03-A-03  Walkability indices and the experience of walking (Medium)
# =====================================================================================
passage("R03-A-03", T,
    "Walkability indices measure proximity to destinations rather than the quality of the walk, so they undervalue what streets give pedestrians, especially when used as targets.",
    [
        "In the last two decades the walkable neighbourhood has become one of the few planning ideals on which almost everyone claims to agree, and with agreement has come measurement. Composite indices now rate districts by the number of shops, schools and stops within a short radius, the density of street intersections and the share of homes near public transport. Estate agents quote such figures; municipal plans set targets for raising them. It would be churlish to deny the good these indices have done. They gave walking, long treated as what people did when they could not drive, a place in the arithmetic of planning, and they made visible how many districts had been designed as if nobody would ever arrive on foot.",
        "Yet what the indices measure is proximity, and proximity is not the same as walkability. A street can lie within five minutes of a pharmacy, a school and a bus stop and still be miserable to walk along: a narrow pavement beside four lanes of fast traffic, no shade under a summer sun, the blank walls of parking structures on either side, crossings that demand a long detour. Two districts with identical scores can therefore offer entirely different experiences, and the index has no way of registering the difference, because it counts what lies at the end of the walk and ignores the walk itself.",
        "This blindness is not accidental; it reflects an assumption that walking is chiefly a means of reaching places. For many people it is that, but it is also something more: the way a child learns a neighbourhood, the way an elderly resident keeps in contact with the world, the occasion for the chance encounters on which local life depends. These goods are produced en route, by the quality of the street, its pace, its frontages, its benches and its shade, not by the count of destinations. A measure built around destinations will systematically undervalue them.",
        "The danger is sharpest when the index ceases to be a description and becomes a target. A city told to raise its score can do so cheaply by permitting a few more shops near existing homes, while the hostile road that separates residents from those shops remains untouched. The number improves; the walk does not. None of this argues for abandoning measurement. It argues for remembering what the measurement leaves out, and for treating a high score as the beginning of an inquiry into a street rather than its conclusion.",
    ],
    "Medium", "A critique that opens with a concession, rests on a conceptual distinction (proximity versus walkability) and ends with a qualified recommendation.",
    "R03A-walkability-indices")

rcq("R03-A-03-1", "Inference", "Easy",
    "The passage implies that, before walkability indices became common, walking was widely regarded in planning as",
    "a fallback way of getting about for people who had no option of driving.",
    [("the most important consideration in the design of new residential districts.",
      "Paragraph 1 says many districts were designed 'as if nobody would ever arrive on foot', the opposite of walking being the main consideration."),
     ("a leisure pursuit with little bearing on how people reached shops and schools.",
      "The passage says walking was treated as what people did 'when they could not drive', that is, as transport of last resort, not as leisure."),
     ("a form of exercise that estate agents promoted in order to sell homes in the suburbs.",
      "Estate agents are said to quote index figures now; nothing suggests they promoted walking as exercise before the indices existed.")],
    "Paragraph 1 says the indices gave walking, 'long treated as what people did when they could not drive', a place in planning arithmetic. Walking was thus seen as a fallback.",
    "Missing the phrase 'long treated as' and reading the later enthusiasm back into the past.",
    "The inference rests on one phrase in paragraph 1.",
    cognitive="Understanding")

rcq("R03-A-03-2", "Except / not supported", "Medium",
    "Each of the following is a claim the author makes about walkability indices EXCEPT that they",
    "tend to overstate the number of shops, schools and stops that lie within a short walk of a typical home.",
    [("have helped to bring walking into the calculations that planners use when they lay out districts.",
      "Paragraph 1 says the indices 'gave walking ... a place in the arithmetic of planning', so the author does make this claim."),
     ("can be raised by a city without making the experience of walking in it any better than before.",
      "Paragraph 4 says a city can raise its score by adding shops while the hostile road remains: 'The number improves; the walk does not.'"),
     ("rest on an assumption that the main purpose of walking is to reach some destination or other.",
      "Paragraph 3 says the indices' blindness 'reflects an assumption that walking is chiefly a means of reaching places'.")],
    "The author never questions the accuracy of the counts. The complaint in paragraph 2 is that an accurate count of proximity still ignores 'the walk itself'. The other three claims appear in paragraphs 1, 4 and 3.",
    "Assuming that a critic of the indices must think their figures are wrong, when the author's point is that they measure the wrong thing.",
    "The distractors are paraphrased from three different paragraphs, and the key is a plausible criticism that the author does not make: rejecting it requires seeing that the critique concerns what is measured, not how accurately.",
    cognitive="Analysis")

rcq("R03-A-03-3", "Strengthen / weaken / assumption", "Medium",
    "Which of the following, if true, would most weaken the author's claim that two districts with identical scores can offer entirely different experiences of walking?",
    "Across a large sample of districts, residents' ratings of how pleasant their streets are to walk along closely match the districts' index scores.",
    [("Homes in districts with high index scores tend to sell for more than similar homes in districts with low scores.",
      "Prices bear on how the scores are used by estate agents, not on whether equal scores can hide different walking experiences."),
     ("Narrow pavements beside fast traffic are found in about as many high-scoring districts as low-scoring ones.",
      "If hostile streets occur regardless of score, the score fails to capture the experience, which supports rather than weakens the author."),
     ("Many residents of districts with high index scores continue to own cars and drive for most of their journeys.",
      "Car ownership says nothing about whether the walks that are taken feel different in districts with the same score.")],
    "The author's claim is that proximity scores do not track the experience of the walk. Evidence that experienced pleasantness closely tracks the score would suggest that districts with equal scores tend to offer similar experiences, undermining the claim.",
    "Picking the traffic option because it is on topic, without noticing that it supports the author.",
    "One distractor strengthens the claim and must be told apart from the key by direction; the others are on topic but irrelevant.",
    cognitive="Analysis")

rcq("R03-A-03-4", "Application / analogy", "Difficult",
    "On the author's view, a city that wished to improve walking in a district, and not merely its walkability score, should begin by",
    "studying the routes residents actually use between their homes and nearby destinations, and the conditions they meet along them.",
    [("permitting more shops, clinics and services to open within a short radius of the homes already in the district.",
      "This is what paragraph 4 describes as the cheap way to raise the score while 'the hostile road ... remains untouched'; it improves the number, not the walk."),
     ("abandoning composite indices and relying instead on residents' own descriptions of what their streets are like.",
      "Paragraph 4 says 'None of this argues for abandoning measurement'; the author wants a score treated as the beginning of an inquiry, not discarded."),
     ("raising the share of homes that lie near public transport, since reaching transport is what walking is chiefly for.",
      "Paragraph 3 identifies the belief that walking is 'chiefly a means of reaching places' as the assumption behind the indices' blindness; the author does not hold it.")],
    "Paragraph 3 locates the goods of walking 'en route, by the quality of the street', and paragraph 4 recommends treating a score as 'the beginning of an inquiry into a street'. Examining the actual routes and their conditions follows from both.",
    "Choosing to abandon the indices, which overstates the author's critique, or to add destinations, which is the very move the author warns about.",
    "Each distractor reflects a position that appears in the passage (the score-raising move, abandoning measurement, the destination assumption); the key requires combining paragraphs 3 and 4.",
    cognitive="Application", exams=DX)

# =====================================================================================
# R03-A-04  Privately owned public plazas (Medium)
# =====================================================================================
passage("R03-A-04", T,
    "Whether a plaza is public depends on the permissions of use it guarantees and on who sets and answers for its rules, not on who owns it.",
    [
        "In many large cities, a good part of the open space created in recent decades does not belong to the public at all. Developers are permitted to build taller or larger than the rules would otherwise allow on condition that they provide a plaza, an arcade or a garden that anyone may enter. The arrangement looks like an elegant bargain: the city gains open space without paying for it, and the developer gains floor area worth far more than the ground surrendered. Critics have long complained that the resulting spaces are often bleak, hidden or quietly discouraging, with benches too narrow to sit on and guards who appear the moment anyone lingers.",
        "The usual form of the complaint is that these spaces are private, and that private space can never be truly public. This puts the matter in the wrong place. Ownership, by itself, settles very little. Many publicly owned squares are fenced at night, patrolled against skateboarders and stripped of seating to deter people who might sleep there, while some privately owned courtyards are generous, well kept and genuinely welcoming. If the test of publicness were the name on the title deed, we would have to call the first kind more public than the second, which is absurd.",
        "What makes a space public is better described as a set of permissions: the right to be there without a reason, to stay without buying anything, to gather with others, to hand out a leaflet or to hold a placard. These permissions are exactly what private management is tempted to withdraw, not out of malice but because each of them is a small risk to the owner and none of them earns anything. A plaza can be open to all in the formal sense while being governed by rules, often unpublished, that make it public only for the well dressed and the briefly passing. The question to ask is therefore not who owns a space but who writes its rules, and to whom the writers must answer.",
        "Seen this way, the bargain need not be abandoned; it needs to be completed. A city that trades floor area for open space is entitled to specify not only the dimensions of the plaza but the permissions that come with it, to publish them at the entrance, and to enforce them against owners as firmly as it enforces its building codes. Where it fails to do so, it has not acquired public space at all. It has paid, in floor area, for something that looks like a square and behaves like a lobby.",
    ],
    "Medium", "Reframes a familiar complaint through a conceptual distinction (ownership versus permissions) and ends with a qualified policy conclusion.",
    "R03A-privately-owned-public-plazas")

rcq("R03-A-04-1", "Specific detail", "Easy",
    "According to the passage, developers come to provide plazas, arcades and gardens open to the public because",
    "they are allowed to build larger or taller than the rules would otherwise permit in return.",
    [("the city pays them for the ground at a price well above what it would fetch on the open market.",
      "Paragraph 1 says the city 'gains open space without paying for it'; the developer is compensated in floor area, not money."),
     ("building codes in most large cities require every new tower to include some open space at its base.",
      "The passage describes a voluntary exchange 'on condition that' open space is provided, not a requirement imposed on every building."),
     ("open spaces attract tenants and shoppers, and so add to the rents that the developer can later charge.",
      "No commercial motive of this kind is mentioned; the passage names the extra floor area as what the developer gains.")],
    "Paragraph 1: 'Developers are permitted to build taller or larger than the rules would otherwise allow on condition that they provide a plaza, an arcade or a garden that anyone may enter.'",
    "Assuming a commercial motive from general knowledge rather than reading the stated bargain.",
    "The answer is stated in one sentence of paragraph 1.",
    cognitive="Recall")

rcq("R03-A-04-2", "Inference", "Medium",
    "It can be inferred that, in the author's view, private managers tend to withdraw the permissions listed in paragraph 3 chiefly because",
    "those permissions bring the owner a little risk and no income, rather than because owners dislike the public.",
    [("planning law in most cities forbids protest and leafleting on land that remains in private ownership.",
      "The passage mentions no such law; it says the permissions are withdrawn by management, often through 'unpublished' rules."),
     ("owners regard the people who would linger or protest in their plazas with open hostility and contempt.",
      "Paragraph 3 says the permissions are withdrawn 'not out of malice', which rules out hostility as the explanation."),
     ("few people who use such plazas actually wish to stay in them, meet others there or hand out leaflets.",
      "The passage gives no evidence about what users want; guards who appear 'the moment anyone lingers' imply that some people do wish to stay.")],
    "Paragraph 3 says the permissions are withdrawn 'not out of malice but because each of them is a small risk to the owner and none of them earns anything'. The motive is a calculation of risk and return.",
    "Choosing hostility because the plazas are described as discouraging, and missing 'not out of malice'.",
    "The key paraphrases a contrast in paragraph 3; the hostility distractor tempts readers who infer motive from effect.",
    cognitive="Understanding")

rcq("R03-A-04-3", "Author's tone / attitude", "Medium",
    "The author's attitude towards the practice of trading extra floor area for open space is best described as",
    "qualified approval: the exchange is sound in principle but worthless unless the city secures and enforces permissions.",
    [("outright rejection, because a space in private ownership can never become genuinely public whatever rules are attached to it.",
      "Paragraph 2 says this complaint 'puts the matter in the wrong place', and paragraph 4 says the bargain 'need not be abandoned'."),
     ("warm enthusiasm, because the city obtains open space without spending any public money and owners keep it well maintained.",
      "The author accepts the critics' account of bleak, discouraging plazas and says a city that does not enforce permissions 'has not acquired public space at all'."),
     ("weary indifference, because ownership settles very little and the resulting spaces will be much the same either way.",
      "That ownership 'settles very little' leads the author to focus on rules, not to indifference; paragraph 4 makes firm demands of cities.")],
    "Paragraph 4 says 'the bargain need not be abandoned; it needs to be completed' by specifying, publishing and enforcing permissions. Without that, the city has paid for 'something that looks like a square and behaves like a lobby'. This is support conditional on enforcement.",
    "Reading the sharp final sentence as rejection of the whole practice.",
    "The tone is mixed: a sharp critique of current practice within acceptance of the bargain itself; one distractor misreads 'settles very little'.",
    cognitive="Analysis")

rcq("R03-A-04-4", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most strengthen the author's claim that the important question is who writes a space's rules and to whom the writers must answer?",
    "In one city, private plazas whose rules of use the municipality set and published were as open to loiterers and leafleters as its best squares; plazas with owner-written rules were not.",
    [("Surveys in one city found that visitors consistently rated its privately owned plazas as cleaner, quieter and safer than publicly owned squares of a similar size and age.",
      "Cleanliness and safety are not the permissions the author treats as defining publicness, so the finding does not bear on who writes the rules."),
     ("Over a period of several decades, developers in one city were granted progressively larger floor-area bonuses for each plaza, arcade or garden that they provided.",
      "The size of the bonus concerns the terms of the bargain, not whether rule-making and accountability determine how public a space is."),
     ("A study in one city found that its privately owned plazas were, on average, smaller, darker and harder to find from the street than its publicly owned squares.",
      "Size and visibility echo the critics' complaint in paragraph 1, but the finding says nothing about whether the author of the rules decides how public a space is.")],
    "The correct answer holds ownership constant (all the plazas are private) and varies only who writes the rules; publicness then follows the rule-writer, exactly as paragraph 3 claims. The other options concern cleanliness, the bonus and physical design, none of which isolates rule-making.",
    "Picking the size and visibility finding because it matches the critics' complaints, which the author accepts but does not use to support this claim.",
    "Two distractors are on topic and echo points the passage makes; the key requires seeing that only a comparison which holds ownership fixed and varies the rule-writer tests the claim.",
    cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-A-05  The critique of the suburb (Medium)
# =====================================================================================
passage("R03-A-05", T,
    "The standard critique of the suburb is right about specific design faults but wrong to condemn the preferences of those who choose suburban life.",
    [
        "Few settlement forms have been as consistently disparaged by writers as the suburb. For the better part of a century, novelists, critics and social scientists have described it in a nearly fixed vocabulary: monotonous rows of identical houses, lawns tended out of anxiety rather than pleasure, a life of commuting, shopping and television in which neighbours are near but never known. The suburb, in this account, is where individuality goes to be smoothed away. The striking thing about the indictment is not its severity but its uniformity, which ought to make us suspicious. A form of life chosen by many millions of households can hardly be as simple as the language used to dismiss it.",
        "Part of the indictment is sound. A district built around the car leaves those who cannot drive, the young, the old and the poor, stranded in a landscape in which nothing is within reach on foot. Zoning that separates homes from shops and workplaces by law multiplies journeys and empties the streets of the casual traffic through which neighbours become familiar. These are real costs, and they fall unevenly. But they are the costs of particular design decisions, and the critique of the suburb has rarely been content to remain at that level.",
        "Its deeper charge is cultural, and here it is weakest. It reads sameness of form as sameness of life, as if a street of similar houses must contain similar people living similar days; anyone who has knocked on the doors of such a street knows otherwise. It also tends to treat the wish for a garden, a quiet bedroom and a door one can close as a failure of imagination, when for families leaving cramped flats these were precisely the goods that city life had denied them. The critics, many of whom lived by choice in the centres of large cities, were often describing a preference they did not share as a pathology from which others suffered.",
        "None of this requires us to admire the suburb, or to ignore the costs of a pattern of building that consumes land and fuel at a great rate. It requires only that criticism be aimed at what can be changed. The desire for privacy and space is not a defect to be corrected; the absence of a shop within walking distance is. A suburb with a small centre, mixed uses and streets that a child can safely cross would answer most of the sound objections without asking anyone to want a different life.",
    ],
    "Medium", "Critique of a common belief that separates a sound practical objection from an unsound cultural one; the stance emerges through concession and reply.",
    "R03A-suburb-critique")

rcq("R03-A-05-1", "Main idea / primary purpose", "Medium",
    "The primary purpose of the passage is to",
    "argue that criticism of the suburb should address its remediable design faults instead of condemning what its residents want.",
    [("defend the suburb as a better form of settlement than the dense centre of a large city, in which families are denied space.",
      "Paragraph 4 says 'None of this requires us to admire the suburb', and the passage never ranks the suburb above the city centre."),
     ("show that the residents of suburban streets lead far more varied lives than novelists and critics have claimed.",
      "The variety of suburban lives is one point in paragraph 3; the passage uses it within a larger argument about where criticism should aim, so the option is too narrow."),
     ("explain how districts designed around the car leave the young, the old and the poor unable to reach shops on foot.",
      "This is the concession in paragraph 2, one part of the argument rather than its purpose.")],
    "Paragraph 1 questions the uniform indictment, paragraph 2 accepts its practical part, paragraph 3 rejects its cultural part, and paragraph 4 concludes that 'criticism be aimed at what can be changed': design, not desire.",
    "Taking the defence of suburban preferences in paragraph 3 for a defence of the suburb as such.",
    "Two distractors are accurate details; the key requires holding the concession and the rejection together.",
    cognitive="Analysis")

rcq("R03-A-05-2", "Inference", "Medium",
    "The author treats the uniformity of the language used against the suburb (paragraph 1) as",
    "grounds for doubting that the indictment does justice to what suburban life is actually like.",
    [("evidence that many critics had studied suburbs closely and independently reached the same conclusions.",
      "The author says the uniformity 'ought to make us suspicious', which is the opposite of treating it as confirmation."),
     ("proof that suburban streets really are as monotonous as the critics' descriptions make them out to be.",
      "The author argues the reverse: a way of life chosen by millions 'can hardly be as simple as the language used to dismiss it'."),
     ("a sign that suburban residents themselves had come to accept the critics' description of their lives.",
      "Residents' views of the critique are never discussed; the remark concerns the critics' vocabulary.")],
    "Paragraph 1 says the indictment's uniformity 'ought to make us suspicious', because a form of life chosen by many millions 'can hardly be as simple as the language used to dismiss it'. Uniform language suggests a stereotype rather than observation.",
    "Reading agreement among critics as evidence for their view.",
    "The inference turns on 'suspicious' and the sentence that follows; one distractor reverses the author's inference.",
    cognitive="Understanding")

rcq("R03-A-05-3", "Structure / function", "Medium",
    "Which of the following best describes the role of paragraph 2 in the passage?",
    "It concedes part of the critics' case but casts those faults as products of design, preparing the later contrast between design and desire.",
    [("It sets out the strongest evidence for the author's thesis that the suburb is a better place to raise children than the city.",
      "Paragraph 2 lists costs of the suburb, not advantages, and the author makes no claim that the suburb is better for children."),
     ("It dismisses the critics' practical objections to the suburb before the author turns to answer their cultural objections.",
      "Paragraph 2 begins 'Part of the indictment is sound' and calls the costs 'real'; it accepts the practical objections rather than dismissing them."),
     ("It raises a fresh objection to the suburb that the critics described in paragraph 1 had failed to notice or discuss.",
      "The paragraph opens 'Part of the indictment is sound', so these objections belong to the critique already described, not a new one.")],
    "Paragraph 2 concedes that car dependence and single-use zoning are 'real costs', then adds that they are 'the costs of particular design decisions'. Paragraph 4 builds on this when it says criticism should aim at 'what can be changed'.",
    "Missing the concession and assuming that the author is answering every objection.",
    "Requires seeing how the paragraph's last two sentences set up paragraph 4; one distractor reverses concession into dismissal.",
    cognitive="Analysis")

rcq("R03-A-05-4", "Application / analogy", "Difficult",
    "Which of the following proposals for an existing suburb would the author most likely regard as answering the objections accepted in paragraph 2, in the way the passage recommends?",
    "Allowing a grocer and a clinic on a few corner plots, and making the main road safe for children to cross.",
    [("Requiring new houses to have varied facades and materials, so that the streets no longer look monotonous to visitors.",
      "Monotony of appearance belongs to the cultural charge the author calls weakest in paragraph 3; it is not among the costs accepted in paragraph 2."),
     ("Replacing detached houses with blocks of flats, so that families learn to prefer shared space over private gardens.",
      "Paragraph 4 says the desire for privacy and space 'is not a defect to be corrected' and favours remedies that do not ask 'anyone to want a different life'."),
     ("Halting all further suburban building in the district, because development of this kind consumes land and fuel at a great rate.",
      "The author acknowledges these costs in paragraph 4 but does not propose a halt; a halt also does nothing for the stranded non-drivers and separated uses of paragraph 2.")],
    "Paragraph 2 accepts that car-centred design strands non-drivers and that single-use zoning empties streets. Paragraph 4 recommends 'a small centre, mixed uses and streets that a child can safely cross'. Shops on corner plots and a safe crossing apply that remedy without changing what residents want.",
    "Choosing varied facades because monotony is the most familiar complaint, without noticing that the author rejects that complaint as a reading of form for life.",
    "The facade option answers a real complaint, but the wrong one; separating it requires distinguishing the practical charge of paragraph 2 from the cultural charge of paragraph 3.",
    cognitive="Application", exams=DX)

# =====================================================================================
# R03-A-06  Gentrification, displacement and neighbourhood character (Difficult)
# =====================================================================================
passage("R03-A-06", T,
    "Gentrification can dispossess residents who never move, but the language of neighbourhood character that names this harm must be tied to relations of use, not to built fabric, or it becomes a defence of exclusion.",
    [
        "Arguments about gentrification tend to collapse into a single question: are the people who lived in a neighbourhood forced out when wealthier newcomers arrive? The question has the merit of being answerable, at least in principle. One can follow households over time, count how many leave, and compare the rate with that in neighbourhoods that have not changed. Suppose such a count found that long-standing residents of a gentrifying district left no faster than residents of similar districts elsewhere. Many would conclude that the harm of gentrification had been exaggerated, and that what remained of the complaint was mere nostalgia.",
        "That conclusion would be premature, because it assumes that the only way to lose a neighbourhood is to leave it. Consider the resident who stays. The grocer who extended credit has been replaced by a shop whose prices assume another income; the bench outside it, once a place to sit for an afternoon, now draws the attention of a security guard; the park is the same park, but the conduct expected in it has quietly changed, and complaints to the police now come from people she does not know, about behaviour that was ordinary a decade ago. She has not moved, and no count of departures will register her, yet the place in which she lives has been withdrawn from her as surely as if she had. To call this nostalgia is to mistake a loss of standing for a loss of scenery.",
        "The difficulty is that the language best suited to describing this loss, the language of a neighbourhood's 'character', is also the language most readily turned to the opposite purpose. Affluent districts invoke their character to resist new housing, to keep out flats that might bring poorer residents, to preserve a streetscape that functions, whatever its owners intend, as a barrier. If character means the look of the buildings and the tone of the streets, then the long-standing resident and the exclusionary homeowner are making the same argument, and it is not one that deserves much sympathy.",
        "The way out is to locate character not in the fabric of a place but in the relations it sustains: who is able to use it, on what terms, and with what claim to be heard. On this view, what the staying resident has lost is not a familiar shopfront but the practical standing she once had in her own street, and what the exclusionary homeowner defends is not a set of relations at all but the absence of people who might form new ones. The distinction will not settle every case, and it asks more of planners than a count of departures does. But it allows us to take the quieter harms of gentrification seriously without lending our sympathy to every resident who would prefer that nothing near them ever changed.",
    ],
    "Difficult", "Abstract argument that moves from a hypothetical finding to an objection, then to a difficulty with the author's own vocabulary and a refined distinction; the stance is carried by fine conceptual contrasts.",
    "R03A-gentrification-and-neighbourhood-character", exams=DX)

rcq("R03-A-06-1", "Inference", "Medium",
    "The author implies that the count of departures described in paragraph 1, if carried out carefully, would",
    "measure what it set out to measure, but would miss a kind of harm suffered by residents who stay.",
    [("show that long-standing residents of gentrifying districts leave much faster than residents of districts that have not changed.",
      "The passage supposes the opposite result, that residents left 'no faster', and the author's objection does not depend on disputing that result."),
     ("prove that complaints about gentrification amount to little more than nostalgia for a vanished streetscape.",
      "This is the conclusion that, in paragraph 1, many would draw, which paragraph 2 calls 'premature' and answers with the staying resident."),
     ("be impossible to carry out in practice, because households that leave a district cannot be traced afterwards.",
      "Paragraph 1 says the question is 'answerable, at least in principle' and describes how to follow households over time.")],
    "The author does not challenge the count itself; paragraph 2 says the conclusion drawn from it 'assumes that the only way to lose a neighbourhood is to leave it', and the staying resident is someone 'no count of departures will register'.",
    "Choosing the nostalgia option, which is the reported view the author rejects.",
    "Requires separating the reliability of the count, which is not disputed, from the scope of what it measures.",
    cognitive="Analysis")

rcq("R03-A-06-2", "Meaning in context", "Medium",
    "In paragraph 2, the 'loss of standing' that the author distinguishes from 'a loss of scenery' refers to",
    "the decline of the resident's accepted place in her street: her ease in using it and her claim to belong there.",
    [("a fall in the market value of the resident's home as the neighbourhood around it changes and its prices rise.",
      "Property values are not discussed; the examples are credit, sitting on a bench, conduct in the park and complaints to the police."),
     ("the resident's being compelled, sooner or later, to leave the district in which she has lived for many years.",
      "The point of the example is that 'She has not moved'; the loss is suffered in place."),
     ("the disappearance of familiar shopfronts, benches and buildings that once gave the street its particular look.",
      "Changes of appearance are the 'scenery'; paragraph 4 confirms that what she lost is 'not a familiar shopfront but the practical standing she once had'.")],
    "Each example in paragraph 2 concerns how the resident may use her street and how others treat her: credit withdrawn, a guard watching her on the bench, strangers complaining about ordinary behaviour. Paragraph 4 names this 'the practical standing she once had in her own street'.",
    "Taking 'scenery' and 'standing' as synonyms for physical change.",
    "The phrase must be read against both the examples of paragraph 2 and the restatement in paragraph 4.",
    cognitive="Understanding")

rcq("R03-A-06-3", "Strengthen / weaken / assumption", "Difficult",
    "Which of the following, if true, would most weaken the distinction the author draws in paragraph 4?",
    "Residents of many affluent districts that resist new housing object chiefly that newcomers would erode the informal ties and local voice they have built up over decades.",
    [("Later and more careful counts showed that departures from gentrifying districts were in fact somewhat higher than the earlier counts had suggested.",
      "This bears on the measurement discussed in paragraph 1, not on whether character located in relations separates the staying resident from the exclusionary homeowner."),
     ("Planners report that judging which relations a place sustains is a good deal harder and slower than counting the households that leave it.",
      "The author already concedes that the distinction 'asks more of planners than a count of departures does', so this does not weaken it."),
     ("Newcomers to gentrifying districts frequently form close ties with one another through the new shops, schools and associations that open there.",
      "Ties among newcomers are consistent with the author's view that relations are what matter; they do not blur the line between the two kinds of claimant.")],
    "Paragraph 4 says the exclusionary homeowner defends 'not a set of relations at all but the absence of people who might form new ones'. If such homeowners are in fact defending relations of use and voice, the relational test no longer separates them from the staying resident, which is the work the distinction was meant to do.",
    "Choosing the planners option because it sounds like a real weakness, without noticing that the author has already conceded it.",
    "The key must be seen to strike at the specific claim about the exclusionary homeowner; one distractor restates a concession, another targets a different paragraph.",
    cognitive="Analysis", exams=DX)

rcq("R03-A-06-4", "Except / not supported", "Difficult",
    "The passage supports each of the following statements EXCEPT:",
    "A resident who stays in a gentrifying district loses more of her neighbourhood than one who is forced to leave it.",
    [("A count of departures, however careful, cannot register the losses of residents who remain in a changing district.",
      "Paragraph 2 says of the staying resident that 'no count of departures will register her', so the statement is supported."),
     ("The same appeal to a neighbourhood's character can serve both to describe a genuine loss and to justify exclusion.",
      "Paragraph 3 says the language of character is 'also the language most readily turned to the opposite purpose', so the statement is supported."),
     ("Judging character by the relations a place sustains demands more of planners than counting those who leave.",
      "Paragraph 4 says the distinction 'asks more of planners than a count of departures does', so the statement is supported.")],
    "Paragraph 2 says the place has been withdrawn from the staying resident 'as surely as if she had' moved: her loss is comparable to that of one who leaves, not greater. The passage never ranks the two losses, so the comparison is unsupported. The other three statements restate paragraphs 2, 3 and 4.",
    "Reading the author's insistence that the staying resident's loss is real as a claim that it is the greater loss.",
    "The unsupported statement turns on the degree word in 'as surely as if she had' and sounds like the author's sympathy for the staying resident; the supported statements are paraphrases spread across three paragraphs.",
    cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-A-07  Circular migration and urban belonging (Medium, 5 questions)
# =====================================================================================
passage("R03-A-07", T,
    "Circular migration between village and city is often a rational spreading of risk rather than an incomplete transition, and cities should stop making the surrender of one home the price of belonging in another.",
    [
        "The familiar story of urbanisation runs in one direction. People leave the countryside for the city, struggle for a generation in its least desirable quarters, and are eventually absorbed, their children speaking the city's idiom and regarding the village as a place of grandparents and holidays. Migration, on this account, is a passage with a beginning and an end, and the only question worth asking about a migrant is how far along it he has come. The story is not false; it describes what happened to many families in many countries. But it has acquired the status of a norm, against which other patterns are measured and found wanting, and this has made it difficult to see a pattern that is, in much of the world, at least as common.",
        "A large number of those who work in cities never complete the journey the story describes. They come for a season of construction or a few years in a factory, return for the harvest, a wedding or an illness in the family, and come back again, sometimes to the same city and sometimes to another. Their earnings pay school fees and debts in the village; the village holds their land, their elders and, often, their spouses and children. A household can live this way for decades, and many do. Seen through the one-way story, such people are migrants who have not yet settled, a transitional population whose double life is a symptom of incomplete integration. Seen on its own terms, the pattern looks rather different: a way of spreading risk across two places, so that a lost job in the city or a failed crop in the village need not be ruinous, because the other place remains.",
        "The distinction matters because city governments have tended to act on the first reading. A resident whose household is registered elsewhere, whose stay is irregular, and whose address is a worksite or a shared rented room is easily treated as a visitor: excluded from subsidised housing, from schools for the children who come along, from the electoral roll, and from the attention of politicians who answer to those who are on it. The exclusion then produces the very evidence that justifies it. Denied a secure foothold in the city, the circular migrant has every reason to keep the village in reserve, and the persistence of his village ties is then cited as proof that he never really belonged.",
        "It would be a mistake to romanticise circulation in its turn. Some who move back and forth would settle in the city if they could, and return to the village only because the city offers them nothing to stay for; for them, circularity is less a strategy than a sentence. Others genuinely prefer a life lived in two places and would keep it even if the city were more welcoming. The difficulty is that from the outside the two groups look identical, and a policy designed for one will misjudge the other.",
        "What follows is not a single programme but a change in the condition attached to belonging. A city that made its entitlements portable, that allowed a worker to enrol his children in school without proving permanent residence, and that encouraged cheap rental housing suited to stays of months rather than decades would serve both groups at once. It would allow those who wish to settle to do so, and those who wish to circulate to circulate without penalty. What it would cease to do is demand that a person surrender one home as the price of being recognised in another.",
    ],
    "Medium", "A critique of a dominant narrative with a self-reinforcing mechanism, a concession that complicates the author's own view, and a recommendation designed to survive it; the prose is clear but the argument has several steps.",
    "R03A-circular-migration-urban-belonging")

rcq("R03-A-07-1", "Specific detail", "Easy",
    "According to paragraph 2, circular migration, when viewed on its own terms rather than through the one-way story, appears as",
    "a way of spreading a household's risk across two places, so that a setback in one is softened by the other.",
    [("a temporary stage in a longer journey, which comes to an end once the migrants' children have been absorbed into city life.",
      "This is the one-way reading of paragraph 1, which paragraph 2 contrasts with the pattern seen on its own terms."),
     ("a choice made chiefly because wages in the city are so much higher than anything the village can offer.",
      "Paragraph 2 never compares wages; it explains circulation by the security of having 'the other place' when one fails."),
     ("a means by which migrants avoid paying the school fees that the city charges to families who settle there.",
      "Paragraph 2 says city earnings pay school fees in the village; nothing suggests migrants circulate to avoid fees in the city.")],
    "Paragraph 2: 'Seen on its own terms, the pattern looks rather different: a way of spreading risk across two places, so that a lost job in the city or a failed crop in the village need not be ruinous, because the other place remains.'",
    "Choosing the one-way reading because it is described in the same paragraph.",
    "The phrase in the stem leads directly to the answer in paragraph 2.",
    cognitive="Recall")

rcq("R03-A-07-2", "Meaning in context", "Easy",
    "In paragraph 4, the remark that for some migrants circularity is 'less a strategy than a sentence' means that for them it is",
    "a condition forced on them by the city's failure to offer a place, not a course they would choose.",
    [("a brief phase that will soon end as they save enough money to buy land and settle in their village.",
      "Nothing in paragraph 4 says the pattern is brief; the contrast is between choosing circulation and having it imposed."),
     ("a legal penalty imposed by the city's courts on workers whose residence there is irregular or unregistered.",
      "The word 'sentence' is figurative; no courts or legal penalties are mentioned in the passage."),
     ("a carefully planned way of spreading risk between a job in the city and a farm in the village.",
      "This is the 'strategy' reading that the phrase says does not fit this group; it describes those who 'genuinely prefer' two places.")],
    "The sentence describes migrants who 'would settle in the city if they could' and return 'only because the city offers them nothing to stay for'. For them circulation is imposed, as a sentence is, rather than chosen, as a strategy is.",
    "Reading 'sentence' literally as a legal punishment.",
    "The figurative phrase is explained in the same sentence.",
    cognitive="Understanding")

rcq("R03-A-07-3", "Inference", "Medium",
    "The passage suggests that the persistence of circular migrants' village ties",
    "is partly a result of their exclusion from the city, and so cannot fairly be taken as proof that they do not belong there.",
    [("shows that circular migrants have no wish to become part of the cities in which they work for months or years.",
      "Paragraph 4 says some circular migrants 'would settle in the city if they could', so the ties do not show an absence of that wish."),
     ("was the original reason why city governments decided to exclude them from housing, schools and the electoral roll.",
      "Paragraph 3 says governments acted on the one-way reading and that the ties are later 'cited as proof'; it does not make the ties the original cause of exclusion."),
     ("will gradually disappear once the migrants' children have grown up speaking the idiom of the city.",
      "That is the outcome of the one-way story in paragraph 1, which the author says does not describe this group.")],
    "Paragraph 3: 'The exclusion then produces the very evidence that justifies it. Denied a secure foothold in the city, the circular migrant has every reason to keep the village in reserve, and the persistence of his village ties is then cited as proof that he never really belonged.'",
    "Choosing the 'original reason' option and reversing the causal order the author describes.",
    "Requires following a self-reinforcing loop; one distractor reverses cause and effect.",
    cognitive="Analysis")

rcq("R03-A-07-4", "Author's tone / attitude", "Medium",
    "The author's attitude towards the one-way story of urbanisation is best described as",
    "critical of its use as a yardstick for all migration, while granting that it fits many families' history.",
    [("dismissive, since the author regards it as a myth that never described the experience of any real migrants.",
      "Paragraph 1 says 'The story is not false; it describes what happened to many families in many countries'."),
     ("approving, since the author treats it as the proper goal against which circular migration ought to be measured.",
      "The author objects that it 'has acquired the status of a norm, against which other patterns are measured and found wanting'."),
     ("neutral, since the author presents it only as one account among others and passes no judgement on its influence.",
      "The author judges its influence explicitly, saying it has made another pattern 'difficult to see' and has shaped exclusionary policy.")],
    "Paragraph 1 grants that the story 'is not false' but objects that it has become 'a norm' against which other patterns are 'found wanting'; paragraph 3 shows the harm of acting on it. The attitude is qualified criticism.",
    "Choosing outright dismissal because the passage argues against the story's dominance.",
    "The concession 'The story is not false' must be weighed against the criticism that follows it.",
    cognitive="Analysis")

rcq("R03-A-07-5", "Inference", "Difficult",
    "The recommendations in paragraph 5 are suited to the difficulty raised in paragraph 4 chiefly because they",
    "would help both migrants forced to circulate and those who choose to, without the city having to tell the two groups apart.",
    [("would persuade migrants who prefer a life in two places to settle permanently in the city instead.",
      "Paragraph 5 says the measures would let 'those who wish to circulate ... circulate without penalty'; they are not designed to change that preference."),
     ("would identify which migrants wish to settle, so that each group could be offered a programme designed for it.",
      "Paragraph 4 says that from the outside 'the two groups look identical', so sorting them is exactly what the city cannot do; paragraph 5 instead offers measures that 'would serve both groups at once'."),
     ("would end circular migration altogether by removing the hostility of cities that is its underlying cause.",
      "Paragraph 4 says some migrants 'genuinely prefer' two places, so hostility is not the cause of all circulation, and paragraph 5 does not aim to end it.")],
    "Paragraph 4 says the two groups 'look identical' from outside, so 'a policy designed for one will misjudge the other'. Paragraph 5 proposes measures that 'serve both groups at once', letting settlers settle and circulators circulate. The measures work without distinguishing the groups.",
    "Choosing the sorting option because it seems the natural response to two groups with different needs.",
    "Requires linking the problem in paragraph 4 (the groups cannot be told apart) to the design of the remedy in paragraph 5; the sorting distractor is the intuitive but wrong solution.",
    cognitive="Analysis", exams=DX)

# =====================================================================================
# R03-A-08  Home as practice, not title (Difficult, 5 questions)
# =====================================================================================
passage("R03-A-08", T,
    "Home is a practice that depends on control and security rather than on title, so treating ownership as the only route to home misdirects policy and weakens neighbourhoods.",
    [
        "In the language of property, home and ownership have become almost interchangeable. To own the place one lives in is to 'have a home'; to rent is to be on the way to one, or to have failed to arrive. The equation is so familiar that it seems less a claim than a definition, and policies built on it, from subsidised mortgages to the sale of public housing to its tenants, present themselves not as choices among ways of housing people but as the extension of home itself to those who lack it.",
        "Yet if one asks what people mean when they say that a place feels like home, the answers rarely mention title. They mention routines that have settled into the rooms, objects arranged by one's own hand, the confidence that one will be there next year, the freedom to decide who comes in, the ability to paint a wall or plant a window box or keep a dog. Home, in this sense, is less a thing one possesses than something one does, a practice of shaping a space and being shaped by it over time. And a practice of this kind needs two conditions: enough control over the space to shape it, and enough security of tenure to make the shaping worthwhile.",
        "Neither condition is the same as ownership, though ownership has usually supplied both. A tenant on a twelve-month lease who may be asked to leave at short notice, who must seek permission to hang a picture, and whose rent can rise without limit, has good reason not to invest himself in his rooms; he is camping, however long he stays. But the cause of his condition is not that he rents. It is that his tenancy is short, revocable and hedged with prohibitions. Where tenancies are long, rents predictable and tenants free to alter their surroundings within reason, renters make homes much as owners do, while an owner whose mortgage payments consume most of his income, and who fears that a lost job means a lost house, may know the very precariousness that the equation reserves for tenants.",
        "None of this means that ownership confers nothing distinctive. The owner can knock down a wall, not merely paint it; he can leave the house to his children; he answers to no landlord. A tenant, however secure, lives in a space whose final shape is decided by someone else. These are real goods, and it would be odd to deny that many people want them for good reasons. The objection is not to ownership but to the assumption that it is the only door into home, an assumption that directs public effort towards turning tenants into owners while leaving the conditions of tenancy, under which a large and often growing share of urban households live, largely untouched.",
        "The cost of that assumption is not only sentimental. A household that expects to move at a landlord's word does not join the school committee, does not plant a tree it will not see grow, does not learn the names of neighbours it may lose within the year. Schools, associations and local shops all depend on residents who expect to stay long enough for their efforts to bear fruit. The practices through which people make a home are continuous with those through which they make a neighbourhood, so that insecurity inside the door becomes thinness of attachment outside it. To treat home as a matter of title is therefore to misunderstand not only what renters lack but what cities lose when they lack it.",
    ],
    "Difficult", "A conceptual redefinition (home as practice) argued against an equation presented as definitional, with a substantial concession and a final step from private to civic consequences.",
    "R03A-home-as-practice-renters", exams=DX)

rcq("R03-A-08-1", "Structure / function", "Easy",
    "The example of the tenant on a twelve-month lease in paragraph 3 serves mainly to",
    "show that a short, revocable and restrictive tenancy, not renting as such, keeps a person from making a home.",
    [("show that renters, whatever the terms of their tenancy, invest less of themselves in their rooms than owners do.",
      "Paragraph 3 goes on to say that where tenancies are long and secure 'renters make homes much as owners do', which contradicts the claim that the terms make no difference."),
     ("suggest that tenants ought to be allowed to knock down walls and alter the structure of the houses they rent.",
      "Knocking down a wall is listed in paragraph 4 as a distinctive good of ownership; the passage never proposes extending it to tenants."),
     ("argue that strict limits on rent increases are the most effective single measure for improving the lives of tenants.",
      "Unlimited rent rises are one feature of the example, but the passage ranks no single measure as most effective.")],
    "Right after the example, paragraph 3 says 'the cause of his condition is not that he rents. It is that his tenancy is short, revocable and hedged with prohibitions.' The example isolates insecurity and lack of control as the obstacles.",
    "Taking the example as evidence against renting in general.",
    "The function is stated in the sentences that follow the example.",
    cognitive="Understanding")

rcq("R03-A-08-2", "Inference", "Medium",
    "The author would most likely regard the owner described at the end of paragraph 3, whose mortgage consumes most of his income, as",
    "someone who holds title yet may lack the security on which making a home depends.",
    [("proof that owning a house is generally a worse arrangement than renting one on secure and long-term terms.",
      "The owner is offered as a case in which ownership fails to supply security, not as proof about owning in general; paragraph 4 affirms the real goods of ownership."),
     ("a person who has 'failed to arrive' at home because of the debts he took on in order to buy his house.",
      "The phrase 'failed to arrive' belongs to the equation in paragraph 1, which describes renters, not indebted owners; the author rejects that equation."),
     ("an exception that confirms the rule that ownership always supplies both of the conditions a home requires.",
      "Paragraph 3 says ownership has 'usually' supplied both conditions; this owner shows that it does not always do so.")],
    "Paragraph 2 names security as one of the two conditions of home-making, and paragraph 3 says this owner 'may know the very precariousness that the equation reserves for tenants'. Title has not given him the security that home requires.",
    "Overreading the example into a general verdict against ownership.",
    "Requires linking the owner example to the two conditions in paragraph 2; one distractor generalises, another misattributes a phrase from paragraph 1.",
    cognitive="Analysis")

rcq("R03-A-08-3", "Strengthen / weaken / assumption", "Medium",
    "The argument of paragraph 5 depends on the assumption that",
    "people are less willing to invest effort in places and relationships they expect soon to be separated from.",
    [("renters as a group take less interest in local schools than owners do, whatever the length and security of their tenancies.",
      "The author attributes thin attachment to the expectation of moving 'at a landlord's word', not to renting as such; paragraph 3 says secure renters make homes as owners do."),
     ("the attachment residents feel to a neighbourhood depends mainly on the physical design of its streets and public spaces.",
      "Street design plays no part in the argument; paragraph 5 links attachment to security of tenure."),
     ("most households that rent would prefer to own their homes if the price of buying one were to fall far enough.",
      "The argument concerns the effects of insecurity, not tenants' preferences about tenure, so it does not need this claim.")],
    "Paragraph 5 reasons that a household that 'expects to move at a landlord's word' will not join the school committee, plant a tree or learn neighbours' names. This holds only if expected separation discourages such investment.",
    "Choosing the 'renters as a group' option, which states the equation the author rejects.",
    "The tempting distractor sounds like the paragraph's conclusion but contradicts paragraph 3.",
    cognitive="Analysis")

rcq("R03-A-08-4", "Main idea / primary purpose", "Difficult",
    "Which of the following best expresses the central argument of the passage?",
    "Home is made through practices that need control and security, which ownership usually but not necessarily supplies, so policy should not treat ownership as the only route to home.",
    [("Ownership confers no real advantage over a secure tenancy, so public support for buyers should be ended and redirected entirely to tenants.",
      "Paragraph 4 says ownership confers 'real goods' that many want 'for good reasons', and the author's objection 'is not to ownership'."),
     ("What people value in a home is above all security rather than control, so tenancy reform should give every tenant a lease without any end date.",
      "Paragraph 2 names control and security as two conditions together, and the passage proposes no specific form of lease."),
     ("Renting has become the usual tenure in cities, and tenancy law has failed to keep pace with the growing number of households that rent.",
      "Paragraph 4 says only that 'a large and often growing share' rent; this detail serves the argument and is not its centre.")],
    "Paragraph 2 redefines home as a practice requiring control and security; paragraph 3 shows that tenancy terms, not tenure, decide whether these exist; paragraph 4 concedes the goods of ownership while rejecting it as 'the only door into home'; paragraph 5 adds the civic cost of that assumption.",
    "Choosing the option that ends support for buyers, which turns the author's objection to an assumption into an objection to ownership.",
    "Two distractors are distorted versions of the thesis (one drops the concession, one drops a condition); the key must keep both conditions and the 'usually but not necessarily' scope.",
    cognitive="Analysis", exams=DX)

rcq("R03-A-08-5", "Inference", "Difficult",
    "The passage suggests that the policies mentioned in paragraph 1 can 'present themselves' as the extension of home rather than as choices among ways of housing people because",
    "once home is defined as ownership, promoting ownership seems to need no defence against alternatives.",
    [("their designers knew that renters could never make real homes and therefore saw no alternative to promoting ownership.",
      "The author argues that renters can make homes under secure tenancies, and says nothing about what designers knew; the point concerns how an equation frames choices."),
     ("subsidised mortgages and the sale of public housing have in fact extended home to nearly all of those who lacked it.",
      "Paragraph 4 says such efforts leave the conditions of tenancy 'largely untouched', so the author does not accept that home has been extended to all."),
     ("tenants who bought the public housing they had rented reported feeling far more at home there after the purchase.",
      "No such reports appear in the passage, and the author's explanation lies in the definition of home, not in tenants' testimony.")],
    "Paragraph 1 says the equation 'seems less a claim than a definition'. If owning simply is having a home, then a policy that spreads ownership looks like spreading home itself, and the question whether other arrangements (such as secure tenancy) could serve as well never arises.",
    "Choosing an option that supplies a factual reason, when the passage's explanation is conceptual.",
    "The key depends on grasping how a claim disguised as a definition removes the appearance of choice; the distractors offer motives or outcomes instead.",
    cognitive="Analysis", exams=DX)
