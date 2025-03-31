"""
Call of Cthulhu Constants Module

This module contains all constant values used throughout the application to avoid
magic numbers and improve code readability and maintainability.

Constants are organized into logical groups:
- Success Levels: Possible outcomes of skill checks
- Dice Constants: Dice notation and patterns
- Character Sheet Constants: Keys used for character data access
- UI Constants: Strings displayed in the user interface
- File Operation Constants: File paths and flags
- Error Messages: Standardized error messages
- System Limits: Maximum allowed values

Author: Andrew C
Version: 1.1
Last Updated: March 31, 2025
"""

import re
from enum import Enum, auto
from typing import Dict


class SuccessLevel(Enum):
    """
    Enumeration of possible success levels for skill checks in Call of Cthulhu.

    These values determine the outcome of a skill check, from best to worst:
    - EXTREME_SUCCESS: Exceptional success (roll <= skill/5)
    - HARD_SUCCESS: Better than normal success (roll <= skill/2)
    - REGULAR_SUCCESS: Standard success (roll <= skill)
    - FAILURE: Failed attempt (roll > skill, not a fumble)
    - FUMBLE: Critical failure (roll >= 96 for skills ≤50, or 100 for skills >50)
    """
    EXTREME_SUCCESS = "Extreme Success"
    HARD_SUCCESS = "Hard Success"
    REGULAR_SUCCESS = "Regular Success"
    FAILURE = "Failure"
    FUMBLE = "Fumble"

    def __str__(self):
        """Return the string value when the enum is converted to string."""
        return self.value


class RuleConstants:
    """
    Constants for Call of Cthulhu game rule calculations.
    """

    class SkillDivisors:
        """
        Divisors used for determining success levels.
        """
        HALF_VALUE = 2  # Divider for Hard Success
        FIFTH_VALUE = 5  # Divider for Extreme Success

    class FumbleBoundaries:
        """
        Boundaries for determining fumble results.
        """
        FUMBLE_THRESHOLD = 50  # Skill level threshold for different fumble ranges
        FUMBLE_RANGE_LOW = 96  # Minimum roll for fumble when skill <= 50
        FUMBLE_CRITICAL = 100  # Roll value for fumble when skill > 50


class DiceConstants:
    """
    Constants related to dice rolling mechanics.
    """

    class StandardDice(Enum):
        """
        Standard dice notations used in the game.
        """
        PERCENTILE = "1D100"  # Standard percentile die
        D4 = "1D4"            # Four-sided die
        D6 = "1D6"            # Six-sided die
        D8 = "1D8"            # Eight-sided die
        D10 = "1D10"          # Ten-sided die
        D12 = "1D12"          # Twelve-sided die
        D20 = "1D20"          # Twenty-sided die

    class DamageModifiers:
        """
        Special damage modifiers used in character sheets.
        """
        DB_PLUS_1D4 = "+1D4"  # Common damage bonus modifier
        DB_NONE = "None"      # No damage bonus

    # Regular expression pattern for parsing dice notation
    DICE_PATTERN = r"""^\(?                   # Optional opening parenthesis
       (\d+)D(\d+)            # Number of dice and sides (e.g., 3D6)
       (\s?([\+\-])\s?(\d+))? # Optional modifier (e.g., +2, -1)
       \)?                    # Optional closing parenthesis
       (\s?\*\s?(\d+))?       # Optional multiplier (e.g., *5)
       $                      # End of string
    """


class SystemLimits:
    """
    System-defined maximum limits.
    """
    MAX_DICE_COUNT = 100  # Maximum number of dice to roll at once
    MAX_DICE_SIDES = 100  # Maximum sides on a single die


class CharacterSheetKeys:
    """
    Standard keys used to access character data from JSON files.
    """
    # Basic character information
    NAME = "name"
    AGE = "age"
    OCCUPATION = "occupation"
    NATIONALITY = "nationality"
    BACKSTORY = "backstory"

    # Character attributes and abilities
    ATTRIBUTES = "attributes"
    SKILLS = "skills"
    WEAPONS = "weapons"

    # Weapon properties
    WEAPON_NAME = "name"
    WEAPON_SKILL = "skill"
    WEAPON_DAMAGE = "damage"


class UIStrings:
    """
    User interface strings used in menus and displays.
    """

    class MainMenu:
        """
        Strings for the main application menu.
        """
        TITLE = "\n=== Call of Cthulhu: Masks of Nyarlathotep ==="
        OPTION_VIEW_CHARACTER = "1. View Premade Character"
        OPTION_RUN_TESTS = "2. Run Tests"
        OPTION_EXIT = "3. Exit"
        PROMPT = "\nEnter your choice (1-3): "
        EXIT_MESSAGE = "Exiting the Call of Cthulhu application."
        INVALID_CHOICE = "Invalid selection."

    class CharacterViewer:
        """
        Strings for the character viewer interface.
        """
        TITLE = "\n=== Character Viewer ==="
        CONTINUE_PROMPT = "Press Enter to continue..."
        CHARACTERS_DIR = "characters"

        @staticmethod
        def character_option(index: int, name: str) -> str:
            """Format a character selection option."""
            return f"{index}. {name}"

        @staticmethod
        def return_option(index: int) -> str:
            """Format the return to main menu option."""
            return f"{index}. Return to Main Menu"

        @staticmethod
        def selection_prompt(max_index: int) -> str:
            """Format the character selection prompt."""
            return f"\nSelect a character you want to view (1-{max_index}): "

    class CharacterSheet:
        """
        Strings for displaying character sheets.
        """
        DIVIDER = "=" * 50
        SECTION_ATTRIBUTES = "\n--- Attributes ---"
        SECTION_SKILLS = "\n--- Skills ---"
        SECTION_WEAPONS = "\n--- Weapons ---"
        SECTION_BACKSTORY = "\n--- Backstory ---"

        @staticmethod
        def format_header(name: str, age: int, occupation: str, nationality: str) -> str:
            """Format the character sheet header."""
            return (f"\n{UIStrings.CharacterSheet.DIVIDER}\n"
                    f"Name: {name}\n"
                    f"Age: {age}\n"
                    f"Occupation: {occupation}\n"
                    f"Nationality: {nationality}")

        @staticmethod
        def format_stat(name: str, value) -> str:
            """Format a character stat line."""
            return f"{name}: {value}"

        @staticmethod
        def format_weapon(name: str, skill: int, damage: str) -> str:
            """Format a weapon line."""
            return f"{name} - Skill: {skill} - Damage: {damage}"

    class TestMenu:
        TITLE = "\n=== Test Menu ==="
        OPTION_CHARACTER_UTILS_TEST = "1. Character Utilities Test"
        OPTION_DICE_ROLL_TEST = "2. Dice"
        OPTION_COC_RULES_TEST = "3. Coc Rules Test"
        OPTION_JSON_READER_TEST = "4. Json Reader Test"
        OPTION_UI_TEST = "5. UI Test"
        OPTION_RUN_ALL_TESTS = "6. Run All Tests"
        OPTION_RETURN_TO_MAIN = "7. Return to Main Menu"

        PROMPT = "\nEnter your choice (1-7): "

        # Success messages
        TEST_SUCCESS = "✓ Test passed successfully!"
        ALL_TESTS_SUCCESS = "✓ All tests completed successfully!"
        SOME_TESTS_SUCCESS = "⚠ Some tests passed, but others failed. See details above."

        # Failure messages
        TEST_FAILURE = "✗ Test failed. See details above."
        ALL_TESTS_FAILURE = "✗ All tests failed. See details above."
        TEST_ERROR = "⚠ Error running test. Make sure the test file exists and is properly formatted."

        # Informational messages
        TEST_RUNNING = "Running test: {}"
        ALL_TESTS_RUNNING = "Running all tests..."
        NO_TESTS_FOUND = "No test files found in the tests directory."

        # Result summary
        TEST_SUMMARY = "\n--- Test Summary ---"
        TOTAL_TESTS = "Total tests run: {}"
        TESTS_PASSED = "Tests passed: {}"
        TESTS_FAILED = "Tests failed: {}"
        TEST_RUN_TIME = "Total run time: {:.2f} seconds"


class FileConstants:
    """
    Constants related to file operations.
    """
    READ_MODE = 'r'
    WRITE_MODE = 'w'
    JSON_EXTENSION = '.json'


class CharacterUtils:
    """
    Utility functions for character operations.
    """

    @staticmethod
    def opposed_check_result(winner_name: str, by_margin: bool = False) -> str:
        """Format the result of an opposed check."""
        if by_margin:
            return f"{winner_name} wins the opposed check! (Better Margin)"
        return f"{winner_name} wins the opposed check!"

    TIE_RESULT = "The opposed check results in a tie"


class ErrorMessages:
    """
    Standardized error messages used throughout the application.
    """
    # Dice-related errors
    INVALID_DICE_FORMAT = "Invalid dice string format"
    INVALID_DICE_COUNT = "Invalid number of dice"
    INVALID_DICE_SIDES = "Invalid number of sides"

    # File-related errors
    CHARACTER_FILE_NOT_FOUND = "Character file not found!"
    NO_CHARACTER_FILES = "No character files found!"

    # Input validation errors
    INVALID_CHOICE = "Please enter a valid number."

    @staticmethod
    def skill_not_found(skill_name: str) -> str:
        """Format error for missing skill."""
        return f"Skill or attribute '{skill_name}' not found for this character"


class Defaults:
    """
    Default values used when specific data is missing.
    """
    UNKNOWN = "Unknown"
    EMPTY_STRING = ""
    NEW_LINE = "\n"
    NONE = None


# Regex flags used throughout the application
class RegexFlags:
    """
    Regular expression flags used for pattern matching.
    """
    IGNORE_CASE = re.I
    VERBOSE = re.X

class TestConstants:
    """
    Constants used for testing purposes.
    """

    # Test file paths
    CHARACTER_UTILS_TEST = "tests/test_character_utils.py"
    DICE_ROLL_TEST = "tests/test_dice_roll.py"
    COC_RULES_TEST = "tests/test_coc_rules.py"
    JSON_READER_TEST = "tests/test_json_reader.py"
    UI_TEST = "tests/test_ui.py"

    # Test output file
    TEST_RESULTS_FILE = "Test Results.txt"

    # Test command options
    PYTEST_VERBOSE_FLAG = "-v"

    # For testing success_check function:
    SKILL_EXTREME_THRESHOLD = 20  # Value at which roll <= skill/5 is extreme success
    SKILL_HARD_THRESHOLD = 40     # Value at which roll <= skill/2 is hard success
    SKILL_REGULAR_THRESHOLD = 85  # Value for testing regular success

    # Common dice roll results for testing:
    EXTREME_SUCCESS_ROLL = 4      # Roll below SKILL_EXTREME_THRESHOLD/5
    HARD_SUCCESS_ROLL = 15        # Roll below SKILL_HARD_THRESHOLD/2
    REGULAR_SUCCESS_ROLL = 70     # Roll below SKILL_REGULAR_THRESHOLD 
    FAILURE_ROLL = 90             # Roll above skill but not a fumble
    FUMBLE_ROLL_LOW_SKILL = 98    # Fumble roll for skill <= 50
    FUMBLE_ROLL_HIGH_SKILL = 100  # Fumble roll for skill > 50
    NEAR_FUMBLE_ROLL = 95         # Roll near fumble threshold but not a fumble for high skill

    # Edge case skills:
    MIN_SKILL = 0                 # Minimum skill value
    MAX_SKILL = 100               # Maximum skill value

    class CharacterNames:
        """Character names used in tests."""
        CHARACTER_1_NAME = "Alice"
        CHARACTER_2_NAME = "Bob"
        TEST_CHARACTER = "Test Character"

    class SkillValues:
        """Skill value ranges and test values."""
        MIN_SKILL = 0
        MAX_SKILL = 100
        AVERAGE_SKILL = 50
        HIGH_SKILL = 70
        LOW_SKILL = 30

    class DiceValues:
        """Common dice roll results for consistent testing."""
        CRITICAL_SUCCESS = 1
        REGULAR_SUCCESS = 40
        FAILURE = 95

    class WeaponData:
        """Test weapon data."""
        SIMPLE_WEAPON_DAMAGE = "1D6"
        COMPLEX_WEAPON_DAMAGE = "1D8+1"
        BONUS_WEAPON_DAMAGE = "1D3+1D4"
        UNPARSEABLE_DAMAGE = "Special Damage"
        MIN_WEAPON_DAMAGE = "1D4"
        MAX_WEAPON_DAMAGE = "4D6"