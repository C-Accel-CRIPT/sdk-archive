"""
Keywords for Process node

"""

keywords_Ingredients = {
    'monomer': 'the major chemical to be incorporated into a repeating unit of a polymer',
    'polymer': 'a chemical that consists of a large number of similar units bonded together',
    'initiator': 'a chemical which starts the growth of a polymer',
    'catalyst': 'a chemical that increases the rate of a chemical reaction',
    'solvent': 'an inert liquid that facilitates a reaction',
    'cta': 'chain transfer agent, a chemical added to the reaction resulting in the exchange of the propagating site',
    'quench': 'a chemical which terminates the chemical reaction',
    'reagent': 'a chemical which is chemical reacts during the course of the process',
    'workup': 'a chemical used in the purification or isolation of a polymer',
}

keywords_Process = {
    # ** chemical transformations **
    'polymerization': 'a chemical reaction that convert monomer(s) to a polymer',
    'kinetics': 'an experiment were multiple data points are take over a span of time',
    'chain_growth': 'chain growth polymerization',
    'step_growth': 'step-growth polymerization',
    'post_poly_mod': 'a chemical reaction preformed on a polymer to modify the chemical functionality',
    'living_poly': 'living polymerization',
    'controlled_poly': 'a polymerization that produce narrowly dispersed polymers (Ð<1.2)',
    'immortal_poly': 'a polymerization where chain transfer reaction and termination is reversible',

    'radical_poly': 'Free radical polymerization',
    'rop': 'ring-opening polymerization (excluding ROMP)',
    'romp': 'ring-opening metathesis polymerization',
    'atrp': 'atom transfer radical polymerization',
    'nmp': 'nitroxide-mediated radical polymerization',
    'raft': 'reversible addition−fragmentation chain-transfer polymerization',
    'anionic': 'anionic addition polymerization',
    'cationic': 'cationic polymerization',
    'insertion': 'coordination insertion polymerization',
    'lewis-pairs': 'a polymerization that employs a Lewis acid and a Lewis base to activate/initiate the polymerization',
    'group-transfer': 'a polymerization that proceeds through the repetitive Michael addition',

    'bulk': 'bulk polymerization',
    'emulsion': 'emulsion polymerization',
    'suspension': 'suspension polymerization',
    'solution': 'solution polymerization',
    'interfacial': 'interfacial polymerization',

    # ** physical transformations **
    'reactive_processing': '',
    'extrusion': '',
    'blow_molding': '',
    'self_assembly': '',
    'curing': '',
    'forming': '',
    'coating': '',
    'annealing': '',
    'sol_annealing': ''
}
