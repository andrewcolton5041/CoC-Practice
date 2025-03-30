"""
Dice Roller Utility for Call of Cthulhu RPG

This module provides functionality to parse and evaluate dice notation strings
commonly used in tabletop RPGs like Call of Cthulhu. It uses a robust
token-based parser instead of complex regular expressions.

The module can handle various dice formats including:
- Basic rolls:         "3D6" or "1D20+3" or "4D4-1" 
- Parenthetical rolls: "(2D6+6)*5" or "(3D4-2)*2"

Author: Unknown
Version: 2.0
Last Updated: 2025-03-30
"""

from dice_parser import DiceParser

# Create a singleton instance of the DiceParser
_parser = DiceParser()


def roll_dice(dice_string):
    """
    Parses and rolls a dice expression, evaluating the result according to RPG dice notation.

    Supports standard dice notation with various formats:
    - Simple dice rolls: "3D6", "1D20"
    - Dice with modifiers: "1D20+3", "4D4-1"
    - Complex expressions: "(2D6+6)*5"

    Args:
        dice_string (str): A string representing dice to roll in standard RPG notation.

    Returns:
        int: The final calculated result of the dice roll expression.

    Raises:
        ValueError: If the input dice string format is invalid or cannot be parsed.
    """
    return _parser.roll_dice(dice_string)


def roll_dice_with_details(dice_string):
    """
    Roll dice and return both the total and individual die results.

    This is useful for systems that need to know the individual die results,
    such as critical hit determination in some RPG systems.

    Args:
        dice_string (str): A simple dice notation (e.g., "3d6")

    Returns:
        tuple: (total, individual_rolls)

    Raises:
        ValueError: If the dice string is not a simple dice roll
    """
    return _parser.roll_dice_with_details(dice_string)


# Keep the original function signature for backwards compatibility
def roll_dice_original(dice_string):
    """
    Original dice rolling function kept for backwards compatibility.
    Uses the new parser internally.

    This function has the same signature and behavior as the original
    roll_dice function, but uses the new parser for better reliability.

    Args:
        dice_string (str): A string representing dice to roll in standard RPG notation.

    Returns:
        int: The final calculated result of the dice roll expression.

    Raises:
        ValueError: If the input dice string format is invalid or cannot be parsed.
    """
    return roll_dice(dice_string)