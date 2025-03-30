from dice_roll import roll_dice

"""
Investigator Attribute Generation

This module defines functions to roll the initial attribute values for an investigator
according to standard Call of Cthulhu rules.

Each function returns an integer between 15 and 90, depending on the dice formula.

Usage:
    chargen_str()  -> Strength
    chargen_con()  -> Constitution
    chargen_siz()  -> Size
    chargen_dex()  -> Dexterity
    chargen_app()  -> Appearance
    chargen_int()  -> Intelligence
    chargen_pow()  -> Power
    chargen_edu()  -> Education
    chargen_luck() -> Luck
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

# Dynamically generate functions for each attribute
for attr, formula in _attribute_formulas.items():
    globals()[f"chargen_{attr}"] = lambda f=formula: roll_dice(f)
