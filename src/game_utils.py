    """
    Game Utilities for Call of Cthulhu

    This module provides game mechanics utilities for the Call of Cthulhu RPG system,
    building on the basic dice rolling and rules modules.

    Major functions include:
    - Character skill checks
    - Opposed checks between characters
    - Weapon damage calculation

    These functions implement game mechanics based on Call of Cthulhu 7th edition rules.

    Author: Unknown
    Version: 1.2
    Last Updated: 2025-03-30
    """

    from src.dice_roll import roll_dice
    from src.dice_parser_core import DiceParserCore
    from src.dice_parser_utils import DiceParserUtils
    from src.dice_parser_exceptions import DiceParserError
    import constants


    def get_skill_value(character_data, skill_name):
        """
        Get the value of a skill or attribute from character data.

        Args:
            character_data (dict): Character data dictionary
            skill_name (str): Name of the skill or attribute to retrieve

        Returns:
            int: The skill or attribute value

        Raises:
            ValueError: If the skill or attribute doesn't exist
        """
        if 'skills' in character_data and skill_name in character_data['skills']:
            return character_data['skills'][skill_name]
        elif 'attributes' in character_data and skill_name in character_data['attributes']:
            return character_data['attributes'][skill_name]
        else:
            raise ValueError(f"Skill or attribute '{skill_name}' not found for character")


    def skill_check(character_data, skill_name):
        """
        Perform a skill check for a character using their character sheet data.

        The function accesses the character's skill or attribute value and then
        performs a d100 roll to determine the success level.

        Args:
            character_data (dict): The character dictionary containing all character information
            skill_name (str): The name of the skill or attribute to check

        Returns:
            tuple: A tuple containing (roll_result, success_level)

        Raises:
            ValueError: If the specified skill or attribute doesn't exist for the character
        """
        skill_value = get_skill_value(character_data, skill_name)
        roll = roll_dice(constants.D100_DICE)

        extreme_threshold = skill_value // constants.EXTREME_SUCCESS_DIVISOR
        hard_threshold = skill_value // constants.HARD_SUCCESS_DIVISOR

        if roll <= extreme_threshold:
            success_level = constants.SUCCESS_EXTREME
        elif roll <= hard_threshold:
            success_level = constants.SUCCESS_HARD
        elif roll <= skill_value:
            success_level = constants.SUCCESS_REGULAR
        elif (skill_value <= constants.FUMBLE_THRESHOLD_STAT and constants.FUMBLE_THRESHOLD_MIN <= roll <= 100) or \
             (skill_value > constants.FUMBLE_THRESHOLD_STAT and roll == 100):
            success_level = constants.SUCCESS_FUMBLE
        else:
            success_level = constants.SUCCESS_FAILURE

        return (roll, success_level)


    def opposed_check(char1_data, char1_skill, char2_data, char2_skill):
        """
        Perform an opposed check between two characters.

        Args:
            char1_data (dict): First character's data dictionary
            char1_skill (str): First character's skill name to check
            char2_data (dict): Second character's data dictionary
            char2_skill (str): Second character's skill name to check

        Returns:
            str: A string describing the result of the opposed check
        """
        char1_roll, char1_success = skill_check(char1_data, char1_skill)
        char2_roll, char2_success = skill_check(char2_data, char2_skill)

        char1_level = constants.SUCCESS_LEVEL_VALUES[char1_success]
        char2_level = constants.SUCCESS_LEVEL_VALUES[char2_success]

        if char1_level > char2_level:
            return f"{char1_data['name']} wins the opposed check"
        elif char2_level > char1_level:
            return f"{char2_data['name']} wins the opposed check"
        else:
            char1_margin = get_skill_value(char1_data, char1_skill) - char1_roll
            char2_margin = get_skill_value(char2_data, char2_skill) - char2_roll

            if char1_margin > char2_margin:
                return f"{char1_data['name']} wins the opposed check (better margin)"
            elif char2_margin > char1_margin:
                return f"{char2_data['name']} wins the opposed check (better margin)"
            else:
                return "The opposed check results in a tie"


    def roll_damage(weapon_data):
        """
        Calculate damage for a weapon attack based on its damage formula.

        Args:
            weapon_data (dict): The weapon dictionary containing the damage formula

        Returns:
            int or str: The calculated damage result or the damage formula if it can't be calculated
        """
        try:
            damage_formula = weapon_data['damage']

            if constants.DAMAGE_BONUS_PATTERN in damage_formula:
                base_formula = damage_formula.split(constants.DAMAGE_BONUS_PATTERN)[0]

                base_damage = roll_dice(base_formula)
                bonus_damage = roll_dice(constants.DAMAGE_BONUS_DICE)

                return base_damage + bonus_damage
            else:
                return roll_dice(damage_formula)

        except DiceParserError:
            return weapon_data['damage']


    def calculate_skill_check_details(skill_value):
        """
        Calculate detailed skill check thresholds based on skill value.

        Args:
            skill_value (int): The character's skill value

        Returns:
            dict: A dictionary containing skill check thresholds
        """
        return {
            'regular_success': skill_value,
            'hard_success': skill_value // constants.HARD_SUCCESS_DIVISOR,
            'extreme_success': skill_value // constants.EXTREME_SUCCESS_DIVISOR
        }
