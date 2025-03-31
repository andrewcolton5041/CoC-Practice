"""
Call of Cthulhu Constants
This module contains constants used throughout the application.
Author: Andrew C.
Version: 1.0
Last Updated: 31 March 2025
"""

import re
from enum import Enum, auto


class SuccessLevel(Enum):
  '''
  Enum for the success levels in Call of Cthulhu
  '''
  
  EXTREME_SUCCESS = "Extreme Success"
  HARD_SUCCESS = "Hard Success"
  REGULAR_SUCCESS = "Regular Success"
  FUMBLE = "Fumble"
  FAILURE = "Failure"

  def __str__(self):
    """Return the string value when the enum is converted to string."""
    return self.value


class Dice:
  '''
  Class for the dice in Call of Cthulhu
  '''
  
  PERCENTILE_DIE = "1D100"  # Constant for the percentile die

  class DicePattern:
    DICE_PATTERN = r"""^\(?                   # Optional opening parenthesis
       (\d+)D(\d+)            # Number of dice and sides of the dice
       (\s?([\+\-])\s?(\d+))? # Optional modifier and add/subtract
       \)?                    # Optional closing parenthesis
       (\s?\*\s?(\d+))?       # Optional multiplier
       $                      # End of string
    """ # Constant for the dice pattern
    


class FumbleBoundaries:
  '''
  Class for the fumble boundaries in Call of Cthulhu
  '''
  
  FUMBLE_REDUCED_CHECK = 50  # Constant for the check to see if the skill is below 50
  FUMBLE_REDUCED_CHECK_MIN = 96  # Constant marking the lower boundary of a fumble when skill is below 50
  FUMBLE_CHECK_MIN = 100  # Constant marking the lower boundary of a fumble when skill is over 50


class HalfFifth:
  '''
  Class for the half-fifth boundaries in Call of Cthulhu
  '''
  
  HALF_VALUE = 2  # Constant for half value on skills
  FIFTH_VALUE = 5  # Constant for fifth value on skills


class RegexFlags:
  """
  Class for the regular expression patterns used in Call of Cthulhu
  """
  
  CASE_INSENSITIVE = re.I # Constant for case insensitive regex flag


class ErrorMessages:
  '''
  Class for the error messages used in Call of Cthulhu
  '''
  
  DICE_VALUE_ERROR = "Invalid dice string format" # Constant for the error message for invalid dice string format
  DICE_NUM_ERROR = "Invalid number of dice" # Constant for the error message for invalid number of dice
  DICE_SIDE_ERROR = "Invalid number of sides" # Constant for the error message for invalid number of sides

class MaxLimits:
  MAX_DICE_NUM = 100  # Constant for the maximum number of dice
  MAX_DICE_SIDES = 100  # Constant for the maximum number of dice sides