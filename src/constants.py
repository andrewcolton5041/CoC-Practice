"""
Call of Cthulhu Constants
This module contains constants used throughout the application.
Author: Andrew C.
Version: 1.0
Last Updated: 31 March 2025
"""

import re
from enum import Enum, auto
from typing import Dict


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

  class BasicDice(Enum):
    '''
    Enum for the basic dices in Call of Cthulhu
    '''
    PERCENTILE_DIE = "1D100"  # Constant for the percentile die
    DFOUR = "1D4"  # Constant for the d4 die

  class DicePattern:
    DICE_PATTERN = r"""^\(?                   # Optional opening parenthesis
       (\d+)D(\d+)            # Number of dice and sides of the dice
       (\s?([\+\-])\s?(\d+))? # Optional modifier and add/subtract
       \)?                    # Optional closing parenthesis
       (\s?\*\s?(\d+))?       # Optional multiplier
       $                      # End of string
    """ # Constant for the dice pattern
    
  class DamageBonusDice:
    ONE_BONUS_DICE = "+1D4" # Constant for one 1D4 bonus dice

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
  VERBOSE = re.X # Constant for verbose regex flag


class ErrorMessages:
  '''
  Class for the error messages used in Call of Cthulhu
  '''
  
  DICE_VALUE_ERROR = "Invalid dice string format" # Constant for the error message for invalid dice string format
  DICE_NUM_ERROR = "Invalid number of dice" # Constant for the error message for invalid number of dice
  DICE_SIDE_ERROR = "Invalid number of sides" # Constant for the error message for invalid number of sides

  CHARACTER_FILE_NOT_FOUND = "Character file not found!" # Constant for the error message for character file not found
  NO_CHARACTER_FILES = "No character files found!" # Constant for the error message for no character files found"
  INVALID_CHOICE_REDO = "Please enter a valid number." # Constant for the error message for invalid choice and redo
  
  @staticmethod
  def skill_value_not_found(skill_name: str):
    return f"Skill or attribute '{skill_name}' not found for this character" # Constant for the error message for skill or attribute not found for this character

class MaxLimits:
  '''
  Class for the maximum limits used in Call of Cthulhu
  '''
  MAX_DICE_NUM = 100  # Constant for the maximum number of dice
  MAX_DICE_SIDES = 100  # Constant for the maximum number of dice sides

class OtherConstants:
  '''
  Class for other constants used in Call of Cthulhu
  '''
  
  NONE = None  # Constant for None value

class CharacterSheetKeys:
  '''
  Class for the character sheet constants used in Call of Cthulhu
  '''

  SKILLS = "skills"  # Constant for the skills key in the character sheet
  ATTRIBUTES = "attributes"  # Constant for the attributes key in the character sheet
  DAMAGE = "damage"  # Constant for the damage key in the weapon data
  NAME = "name"  # Constant for the name key in the character sheet
  AGE = "age"  # Constant for the age key in the character sheet
  OCCUPATION = "occupation"  # Constant for the occupation key in the character sheet
  NATIONALITY = "nationality"  # Constant for the nationality key in the character sheet
  WEAPONS = "weapons"  # Constant for the weapons key in the character sheet
  BACKSTORY = "backstory"  # Constant for the backstory key in the character sheet

class CharacterUtils:
  @staticmethod
  def opposed_check_win(name: str, margin: bool) -> str:
    if margin:
      return "%s wins the opposed check! (Better Margin)" % name
    else: 
      return "%s wins the opposed check!" % name

  OPP_CHECK_TIE = "The opposed check results in a tie"

class MenuStrings:
  '''
  Class for the menu strings used in Call of Cthulhu
  '''
  MAIN_MENU_TITLE = "\n=== Call of Cthulhu: Masks of Nyarlathotep ===" 
  MAIN_MENU_OPTION_1 = "1. View Premade Character" 
  MAIN_MENU_OPTION_2 = "2. Exit" 
  MAIN_MENU_CHOICE_PROMPT = "\nEnter your choice (1-2): "
  STARTING_NUMBER = 1
  INVALID_CHOICE_ERROR = "Invalid selection."
  EXIT_MESSAGE = "Exiting the Call of Cthulhu application."

  class ChoiceNumEnum(Enum):
    OPTION_1 = '1'
    OPTION_2 = '2'

  class CharacterViewerStrings:
    CHARACTERS = 'characters'
    CHARACTER_VIEWER_TITLE = "\n=== Character Viewer ==="
    INPUT_ENTER_KEY = "Press Enter to continue..."

    @staticmethod
    def available_characters(i: int, name: str) -> str:
      return "%i. %s" % (i,name)

    @staticmethod
    def character_to_main(i: int) -> str:
      return "%i. Return to Main Menu" % i

    @staticmethod
    def character_viewer_prompt(i: int) -> str:
      return "\nSelect a character you want to view (1-%i): " % i

class FileExtensions(Enum):
  JSON_FILE = '.json'

class Extra:
  NO_CHARACTER = ''
  NEW_LINE = '\n'
  EQUAL_SIGN = '='
  UNKNOWN = 'Unknown'

class JSONReaderConst:
  TOP_DIVIDER = "\n" + "=" * 50
  BOTTOM_DIVIDER =  "=" * 50 + '\n'
  ATTRIBUTES_DIVIDER = "\n--- Attributes ---"
  SKILLS_DIVIDER = "\n--- Skills ---"
  WEAPONS_DIVIDER = "\n--- Weapons ---"
  BACKSTORY_DIVIDER = "\n--- Backstory ---"
  
  @staticmethod
  def character_name(name: str) -> str:
    return "Name: %s" % name

  @staticmethod
  def character_age(age: int) -> str:
    return "Age: %i" % age

  @staticmethod
  def character_occupation(occupation: str) -> str:
    return "Occupation: %s" % occupation

  @staticmethod
  def character_nationality(nationality: str) -> str:
    return "Nationality: %s" % nationality

  @staticmethod
  def character_sheet_att_ski_printer(attr: str, value: str) -> str:
    return "%s: %s" % (attr, value)

  @staticmethod
  def character_sheet_weapons(name: str, skill: str, damage: str) -> str:
    return "%s - Skill: %s - Damage: %s" % (name, skill, damage)

class FileFlags:
  READ_FLAG = 'r'
  