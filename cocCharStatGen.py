from dice_roll import roll_dice
"""
Investigator Attribute Generation

This module defines a dictionary of functions to roll initial attribute values
for an investigator according to Call of Cthulhu rules.
"""

# Mapping of attributes to their dice roll formulas
_attribute_formulas = {
    "str": "3D6 * 5",
    "con": "3D6 * 5",
    "siz": "(2D6 + 6) * 5",
    "dex": "3D6 * 5",
    "app": "3D6 * 5",
    "int": "(2D6 + 6) * 5",
    "pow": "3D6 * 5",
    "edu": "(2D6 + 6) * 5",
    "luck": "3D6 * 5",
}

# Create a dictionary of attribute generator functions
chargen_funcs = {
    key: (lambda f=formula: roll_dice(f))
    for key, formula in _attribute_formulas.items()
}
