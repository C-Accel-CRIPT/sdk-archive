"""
Official Control language support by CRIPT.
For material node

"""


keywords_material_p = {
    # General structure terms
    'thermoset': 'a cross-linked polymer',
    'thermoplastic': 'a polymer that becomes pliable at elevated temperature adn solidifies upon '
                     'cooling to room temperature',
    'semicrystalline': 'a polymer that does exhibit some crystalline structure',
    'elastomer': 'a cross-linked polymer with a glass transition well below room temperature',
    'amorphous': 'a polymer that does not exhibit any crystalline structure',

    'homopolymer': 'a polymer with a single repeating structure',
    'copolymer': 'a polymer with a two or more repeating structures',
    'random': 'a polymer with a two or more repeating structures are randomly distributed',
    'block': 'a polymer with a two or more repeating structures are distributed in groups',
    'alternating': 'a polymer where the composition oscillates between two repeating structures',
    'gradient': 'a polymer where the composition gradually transitions from one repeating structure into another',

    'isotactic': 'a polymer with all substituent having the same stereoconfiguration',
    'syndiotactic': 'a polymer with substituent alternating stereoconfiguration',
    'atactic': 'a polymer with substituent having a random distribution of stereoconfiguration',

    'regio_regular': 'a polymer with one positional isomer; all head-to-tail or tail-to-tail and head-to-head',
    'regio_irregular': 'a polymer with more than one positional isomer; mixture of head-to-tail, tail-to-tail, '
                       'and head-to-head',

    'linear': 'a polymer with a single line of repeat units',
    'star': 'a polymer with 3 or more arms originating from a single point',
    'ring': 'a polymer with no ends or a loop of repeat units',
    'comb': 'a polymer with a main chain with small chains branching off the main chain',
    'bottlebrush': 'a polymer with a very high density of chains branching off the main linear chain',
    'hyperbranch': 'a polymer with a very high degree of branches and branches have more branching',
    'network': 'a polymer with a where a molecular structure percolates through the full macroscopic sample',

    'conjugated_poly': 'a polymer with delocalized electrons in the p orbital along the backbone',

    'polymer_blend': 'a material with two or more composed of two or more polymers',
    'composite': 'a material with two or more components',

    # polymer types
    'polyolefins': 'a polymer with [$]CC(R)[$] structure and the locally surrounding is C and H',
    'polystyrenes': 'a polymer with [$]CC(c1ccccc1)[$] structure',
    'polyphenylenes': 'a polymer with [$]c1cccc(c1)[$] structure',

    'polyvinyls': 'a polymer with [$]CC(R)[$] structure and the locally surrounding by elements other than C and H',
    'polyacrylates': 'a polymer with [$]CC(C(=O)O-R)[$] structure',
    'polymethacrylates': 'a polymer with [$]CC(C)(C(=O)O-R)[$] structure',
    'polyvinyl_ethers': 'a polymer with [$]CC(OR)[$] structure',
    'polyvinyl_esters': 'a polymer with [$]CC(OC(=O)-R)[$] structure',

    'polyesters': 'a polymer with R-C(=O)O-R within the backbone',
    'polycarbonates': 'a polymer with R-O-C(=O)O-R within the backbone',
    'polyethers': 'a polymer with R-O-R within the backbone',
    'polyanydrides': 'a polymer with R-C(=O)-O-C(=O)-R within the backbone',
    'polyketones': 'a polymer with R-C(=O)-R with the backbone',
    'polyamines': 'a polymer with R-N(R)-R within the backbone',
    'polyurethanes': 'a polymer with R-N(R)-C(=O)O-R within the backbone',
    'polyamides': 'a polymer with R-C(=O)N(R)-R within the backbone',
    'polyureas': 'a polymer with R-N(R)-C(=O)-N(R)-R within the backbone',
    'silicones': 'a polymer with R-Si(R)(R)-R within the backbone',
    'polysulfides': 'a polymer with R-S-R within the backbone',
    'polysulfones': 'a polymer with R-S(=O)(=O)-R within the backbone',
    'polysulfoxides': 'a polymer with R-S(=O)-R within the backbone',
    'polythiophenes': 'a polymer with C=C1=CC=CS1 5 member ring within the backbone',
    'polyphosphazenes': 'a polymer with R-P(R)(R)=N-R within the backbone',
}

keywords_material = {
    # monomer types
    'olefin': 'a chemical with one double bond and is locally surrounded by only C and H',
    'diene': 'a chemical with two or more double bonds',
    'styrene': 'a chemical with C=C-(c1ccccc1) structure',
    'cyclic_olefin': 'a chemical where at least one double bond is found in a ring (excluding aromatic rings)',
    'acetylene': 'a chemical with one or more triple bounds (C≡C)',

    'vinyl': 'a chemical with C=C-R structure and the local surrounding contains elements other than C and H',
    'vinyl_ether': 'a chemical with C=C-O-R structure',
    'vinyl_ester': 'a chemical with C=C-O-(C=O)-R structure',
    'acrylate': 'a chemical with C=C-C(=O)O-R structure',
    'methylacrylate': 'a chemical with C=C(C)-C(=O)O-R structure',

    'lactone': '(cyclic ester) a chemical with R-C(=O)O-R within a ring',
    'cyclic_ether': 'a chemical with R-O-R within a ring',
    'cyclic_carbonate': 'a chemical with R-O-C(=O)O-R within a ring',
    'cyclic_anhydride': 'a chemical with R-C(=O)-O-C(=O)-R with a ring (includes N-carboxy anhydrides)',
    'oxazoline': 'a chemical with a R-N=C(R)-O-R within a five membered ring ',

    'lactam': '(cyclic amide) a chemical with R-C(=O)N(R)-R within a ring',
    'cyclic_amine': 'a chemical with R-N(R)-R within a ring',
    'cyclic_sulfur': 'a chemical with R-S-R or R-S(=O)-R within a ring',
    'thiophene': 'a chemical with C=C1=CC=CS1 5 member ring',
    'phosphoesters': 'a chemical with R-O-P(=O)(OR)-O-R within a ring',
    'phosphonate': 'a chemical with R-O-P(=O)(C(R)(R)R)-O-R within a ring',
    'phostone': 'a chemical with R-P(=O)(R)-O-R within a ring',
    'phosphazenes': 'a chemical with R-P(R)(R)=N-R within a ring',
    'siloxane': 'a chemical with R-O-Si(R)(R)-O-R within a ring',
    'carbosiloxane': 'a chemical with R-Si(R)(R)-R within a ring',

    'diol': 'a chemical with two or more -OH groups',
    'dicarboxylic_acid': 'a chemical with two or more -C(=O)OH groups',
    'diamines': 'a chemical with two or more -NH2 groups',
    'diacid chloride': 'a chemical with two or more -COCl groups',

    # other
    'filler': 'a substance that is added to resins',
    'matrix': 'a substance for binding and holding reinforcements together',

}
