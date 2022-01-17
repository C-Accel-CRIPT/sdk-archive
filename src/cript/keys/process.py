"""
Official Control language support by CRIPT.
For Process node

"""

process_keywords = {
    # chemical transformations
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
    'lewis-pairs': 'a polymerization that employs a Lewis acid and a Lewis base to activate/initiate '
                   'the polymerization',
    'group-transfer': 'a polymerization that proceeds through the repetitive Michael addition',

    'bulk': 'bulk polymerization',
    'emulsion': 'emulsion polymerization',
    'suspension': 'suspension polymerization',
    'solution': 'solution polymerization',
    'interfacial': 'interfacial polymerization',

    # physical transformations
    'reactive_processing': '',
    'extrusion': '',
    'blow_molding': '',
    'self_assembly': '',
    'curing': '',
    'forming': '',
    'coating': '',
    'annealing_thermo': 'annealing with temperature',
    'annealing_sol': 'annealing with solvent vapor'
}
