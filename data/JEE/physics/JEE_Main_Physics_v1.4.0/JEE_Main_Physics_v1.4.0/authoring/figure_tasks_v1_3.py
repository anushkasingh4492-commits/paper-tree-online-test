"""Figure-dependent E04 rewrites. Alternatives are plausible apparatus mappings."""

def replacements():
    out={}
    def put(n,panel,stem,answer,wrong,explanation,visual):
        out[n]=dict(panel=panel,question=stem+f' Refer to experimental arrangement {panel:02}.',
                    answer=answer,wrong=wrong,explanation=explanation,visual_evidence=visual)

    put(2084,1,'Which labelled component is used to measure the depth of a narrow blind hole?',
        'The lower extension on the right',
        ['The upper pair of projections on the left','The lower pair of projections on the left','The long graduated bar on the upper right'],
        'The drawing labels the slender extension below the main scale as the depth rod. With the end face seated at the mouth of a hole, this rod reaches its bottom. The upper jaws serve internal widths and the lower jaws external widths.',
        'Depth rod is the lower right extension; jaw pairs are on the left.')
    put(2085,8,'Which displacement boundary conditions belong to the resonating system shown?',
        'A displacement antinode at the upper open end and a node at the liquid surface',
        ['Displacement antinodes at both ends of an open pipe','Displacement nodes at both fixed ends of a stretched string','A displacement node at a clamped end and an antinode at a free end of a rod'],
        'The figure shows an air column open near the tuning fork and closed by water below. Air displacement is large at the open end and approximately zero at the liquid boundary. The other options describe different resonators.',
        'Tuning fork above open tube; lower end of air column terminated by water.')
    put(2088,6,'Which experiment-specific preparation applies to the narrow vertical component shown?',
        'Clean the narrow tube and keep it vertical so its bore and wetting remain suitable for a rise measurement',
        ['Remove kinks from a loaded wire before measuring its elastic extension','Approach a screw-gauge reading from one direction to reduce backlash','Set a pendulum to a small angular amplitude before timing its oscillations'],
        'The drawing shows a capillary in a liquid bath with a raised meniscus and height h. A clean, uniform bore and a vertical tube are needed for the rise measurement. Each alternative is useful for its named apparatus, but that apparatus is absent here.',
        'Capillary, raised meniscus, reservoir surface and vertical height h.')
    put(2099,5,'Which experimental procedure applies to the apparatus in the drawing?',
        'Remove kinks, measure its diameter at several positions, and add loads within its elastic limit',
        ['Clean the bore and measure a meniscus height above the surrounding liquid','Strike the tuning fork gently and vary the liquid level to locate resonance','Focus successively on a slab surface and its apparent bottom mark'],
        'The right-hand element is labelled test wire and carries the variable load; the other hanging wire is the reference. The selected procedure controls the specimen geometry and elastic regime needed for extension measurements.',
        'Right wire labelled test wire and load; left reference wire; level and micrometer between them.')
    put(2113,2,'Which reading rule belongs to the measuring instrument shown, before applying its signed zero correction?',
        'Sleeve reading plus thimble-division reading multiplied by pitch divided by the number of thimble divisions',
        ['Main-scale reading plus vernier coincidence multiplied by the vernier least count','Final burette reading minus initial burette reading for delivered volume','Number of full stopwatch revolutions times its period plus the remaining dial reading'],
        'The anvil, spindle and rotating thimble identify a screw gauge. One complete revolution advances the spindle by the pitch; each thimble division advances it by pitch/N. The other options are valid reading rules for different instruments.',
        'U-shaped frame with anvil, spindle and thimble, rather than a sliding vernier.')
    put(2118,15,'Which top-to-bottom order of the three objects agrees with the drawing and places the marked object beyond the refracting slab along the viewing direction?',
        'Microscope, glass slab, reference mark',
        ['Microscope, reference mark, glass slab','Glass slab, microscope, reference mark','Reference mark, glass slab, microscope'],
        'The microscope is drawn above the glass slab, while the cross-shaped reference mark lies below it. The microscope therefore views that mark through the slab. The order must be read from this arrangement; moving the mark between the microscope and slab would remove the slab from its line of sight.',
        'Microscope above slab, cross-shaped reference mark below slab.')
    # The reference label positions are part of the question: without the figure,
    # A/B/C/D are not identified by the stem.
    put(2122,18,'Which ordered pair of component labels identifies (first) the device designed to emit light under suitable forward bias and (second) the device that stores electrostatic energy?',
        'B, D',['A, D','B, C','C, A'],
        'Component B is drawn with outward light arrows at a diode symbol, identifying an LED. Component D has two parallel separated plates, identifying a capacitor. A is an ordinary diode and C is a resistor.',
        'B has diode plus outward arrows; D has two parallel plates; A diode, C resistor.')
    put(2124,8,'Which procedure is used to excite oscillations in the system depicted?',
        'Hold a vibrating tuning fork just above the upper opening without touching the tube',
        ['Displace a suspended bob slightly and release it without a push','Pull a stretched string sideways and release it while its ends remain fixed','Tap one end of a supported metal rod to excite its longitudinal vibration'],
        'The drawing places a tuning fork above the open air column. Its sound excites the column while avoiding direct contact. The other procedures excite the different oscillators named in those options.',
        'Tuning fork is immediately above the upper opening of the tube.')
    put(2125,7,'Which force balance describes the steady state of the system depicted?',
        'Weight downward equals buoyancy plus viscous drag upward',
        ['For a freely floating object at rest, weight equals buoyancy','For a block at rest on a horizontal table, weight equals the normal reaction','For a hanging bob at rest in air, weight equals string tension'],
        'The figure shows the same unsupported sphere at successive downward positions inside a liquid. At terminal falling speed, its net force is zero: weight is balanced jointly by buoyancy and upward viscous drag. None of the alternative supports or floating conditions is shown.',
        'Successive sphere positions descend in a liquid with no supporting string or surface.')
    put(2128,9,'Which procedure helps the particular measurement made with the vessel and immersed instruments shown?',
        'Transfer the hot specimen quickly, stir gently, and record the equilibrium temperature while limiting heat exchange',
        ['Move the observation pin until its image has no relative parallax','Vary the length of the air column and listen for a resonance maximum','Adjust the jockey along the bridge wire until the galvanometer reads zero'],
        'The drawing is an insulated calorimeter with a thermometer and stirrer. Prompt transfer and mixing help establish a meaningful equilibrium temperature with small environmental heat exchange. The alternatives concern optical, acoustic and electrical arrangements.',
        'Insulated vessel, thermometer and stirrer immersed in its contents.')
    put(2129,4,'The displayed scale is initially balanced with its knife edge exactly under its own centre of gravity and m1=2m2. The point of suspension of m1 is shifted 1 cm to the right, remaining on its original side of the pivot. Which shift of m2 restores balance if the knife edge stays fixed?',
        'Move m2 2 cm to the left',['Move m2 2 cm to the right','Move m2 1 cm to the left','Move m2 1 cm to the right'],
        'The drawing places m1 left of the pivot and m2 right of it. Moving m1 right by 1 cm reduces its lever arm and anticlockwise moment by m1 g×1 cm. The clockwise moment must decrease equally, so the right-hand mass m2 moves toward the pivot, to the left, by (m1/m2)×1=2 cm. The scale’s own weight acts through the specified fixed pivot.',
        'm1 is on the left and m2 on the right of the knife edge.')
    put(2130,13,'Where should the observation pin tip be placed to remove parallax with the real image in the ray arrangement shown?',
        'To the right of the lens and below the optical axis',
        ['To the left of the lens and above the optical axis','To the right of the lens and above the optical axis','To the left of the lens and below the optical axis'],
        'The two emergent rays meet to the right of the lens below its optical axis, forming an inverted real image. The observation pin tip must coincide with that image point, not with the object, focus or optical centre.',
        'Ray intersection to the right below axis; O and F lie on axis.')
    put(2131,9,'Which measurement set is appropriate for determining the material property investigated with the displayed arrangement?',
        'Hot-body and water masses, their initial temperatures, final equilibrium temperature, and vessel heat capacity',
        ['Wire length, diameter, applied load and elastic extension','Sphere radius and density, liquid density, and terminal falling speed','Fork frequency and the difference between successive resonant lengths'],
        'The thermometer, stirrer and insulation identify a calorimetric mixing experiment. Its heat balance uses the energy lost by the hot body and gained by water and vessel. The three other data sets belong respectively to elasticity, viscosity and sound-speed experiments.',
        'Vessel insulation, thermometer and stirrer rather than wire, falling-sphere timing tube or fork.')
    put(2132,10,'Let J be the jockey contact on the uniform wire, and neglect end resistance. Using the gap positions and labels in the picture, what is X when the galvanometer shows zero?',
        'R × JB/AJ',['R × AJ/JB','R × AB/AJ','R × AB/JB'],
        'The known R is in the left gap next to A; X is in the right gap next to B. At null, R/X=AJ/JB, so X=R(JB/AJ). The orientation in this drawing matters: interchanging the two gap resistors would reverse the length ratio.',
        'R in left gap adjacent A, X right adjacent B, G joins gap midpoint to jockey.')
    put(2134,14,'Which of these standard results applies to the optical element in this drawing?',
        'At minimum deviation, the internal refraction angles at the two sloping faces are equal',
        ['The object and its real image lie at twice the focal length on opposite sides of a thin converging lens','The emergent and incident rays from a parallel-sided slab are parallel','The angle of incidence equals the angle of reflection at a plane mirror'],
        'The triangular element has two nonparallel refracting faces, so it is a prism. At minimum deviation its path is symmetric, with equal internal refraction angles (each A/2) and equal incidence and emergence angles. The alternatives describe different optical elements.',
        'Triangular prism and refraction through its two sloping, nonparallel faces.')
    put(2136,3,'Which operating procedure applies to the apparatus shown?',
        'Release the bob from a small angle without a push and time several complete oscillations',
        ['Keep the test wire within its elastic limit while changing the suspended load','Keep the capillary clean and vertical while observing its meniscus height','Time the falling sphere between marks only after its speed is steady'],
        'The single bob suspended from a fixed point forms a simple pendulum. Small amplitude and release without a push keep the motion close to the small-angle model; timing several oscillations reduces reaction-time error. The other procedures concern different drawings.',
        'Single bob suspended by a line, shown displaced from a vertical mean-position line.')
    put(2137,4,'What is the direction of the gravitational turning effect of each labelled suspended mass about the knife edge in the drawing, viewed as shown?',
        'm1 anticlockwise; m2 clockwise',
        ['m1 clockwise; m2 anticlockwise','Both clockwise','Both anticlockwise'],
        'm1 hangs to the left of the knife edge and pulls downward, producing an anticlockwise moment. m2 hangs to the right and pulls downward, producing a clockwise moment. Their locations in the diagram determine the signs.',
        'Left suspended m1 and right suspended m2, pivot between.')
    put(2138,17,'Which current–voltage region is being investigated with the diode type and supply polarity actually drawn?',
        'Reverse breakdown of a Zener diode',
        ['The forward-bias knee of a silicon junction diode','The approximately linear bidirectional response of an ohmic resistor','The charging transient of a capacitor under DC'],
        'The component is labelled Zener diode, and its cathode is connected toward the positive supply terminal on the right. This is the reverse-bias arrangement used to study Zener breakdown, with a series resistor limiting current.',
        'Zener label and cathode at right; positive battery terminal on right.')
    put(2140,7,'Which selection of observation interval suits the object and timing marks shown?',
        'Measure descent between the two marks only after the sphere has reached terminal speed, away from the vessel walls',
        ['Measure the elapsed time for many small-angle oscillations past a fixed mean-position marker','Measure the delay between sound pulses over a known separation in air','Measure several wheel revolutions after its angular speed has become steady'],
        'The diagram shows one sphere at successive positions falling through liquid and two horizontal timing marks. The marks should bracket a terminal-speed interval away from wall effects. The other intervals apply to different moving systems.',
        'Two horizontal timing marks across a liquid vessel with a downward sphere sequence.')
    put(2142,16,'For the diode in the drawing, which ordered pair identifies the terminal at higher potential (first) with the supply as drawn and (second) after reversing only the supply?',
        'Anode, cathode',
        ['Cathode, anode','Anode, anode','Cathode, cathode'],
        'As drawn, the positive terminal is on the left and feeds the diode anode through the protective resistor and ammeter. Reversing the supply puts positive potential toward the cathode on the right. Keep the series protection and use a suitable reverse-current range.',
        'Positive terminal left, anode left, cathode bar right, with series R.')
    put(2143,1,'Which parts should contact the outside of a cylinder when its external diameter is measured with the shown instrument?',
        'The facing surfaces of the lower pair of projections on the left',
        ['The outward-facing tips of the upper pair of projections on the left','The tip of the lower right extension and the instrument end face','Two chosen graduation marks on the upper right bar'],
        'The lower jaw pair is labelled outer jaws and closes around an external object. The upper jaws expand against internal surfaces, while the depth rod measures a recess depth. Choosing the contact pair requires identifying the pictured components.',
        'Outer-jaw label under lower left pair; upper jaws and right depth rod are distinct.')
    put(2148,17,'Where is the protective current-limiting component located in the displayed breakdown-measurement circuit?',
        'In the upper left part of the series loop',
        ['In the small branch drawn below and parallel to the diode','At the centre of the bottom branch','At the upper right, between the two voltmeter connections'],
        'The drawing places Series R in the current path with the reverse-biased Zener. Its voltage drop limits current. An ideal ammeter has negligible resistance, an ideal voltmeter draws negligible current, and an ideal voltage source does not itself provide current limiting.',
        'Series R upper left in loop; V across diode; A in series; source below.')
    assert len(out)==22
    return out
