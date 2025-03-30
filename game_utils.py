import dice_roll as dr
import coc_rules as rules

def skill_check(character_data, skill_name):
    """
    Perform a skill check for a character.

    Args:
        character_data: The character dictionary data
        skill_name: The name of the skill to check

    Returns:
        Tuple of (roll, success_level)
    """
    # Get skill value
    skill_value = None
    if 'skills' in character_data and skill_name in character_data['skills']:
        skill_value = character_data['skills'][skill_name]
    elif skill_name in character_data['attributes']:
        skill_value = character_data['attributes'][skill_name]
    else:
        raise ValueError(f"Skill or attribute '{skill_name}' not found for this character")

    # Roll the check
    roll = dr.roll_dice("1D100")

    # Determine success level
    if roll <= skill_value / 5:
        success_level = "Extreme Success"
    elif roll <= skill_value / 2:
        success_level = "Hard Success"
    elif roll <= skill_value:
        success_level = "Regular Success"
    elif (skill_value <= 50 and 96 <= roll <= 100) or (skill_value > 50 and roll == 100):
        success_level = "Fumble"
    else:
        success_level = "Failure"

    return (roll, success_level)

def opposed_check(char1_data, char1_skill, char2_data, char2_skill):
    """
    Perform an opposed check between two characters.

    Args:
        char1_data: First character's data
        char1_skill: First character's skill name
        char2_data: Second character's data
        char2_skill: Second character's skill name

    Returns:
        String describing the result
    """
    char1_roll, char1_success = skill_check(char1_data, char1_skill)
    char2_roll, char2_success = skill_check(char2_data, char2_skill)

    success_levels = {
        "Extreme Success": 4,
        "Hard Success": 3,
        "Regular Success": 2,
        "Failure": 1,
        "Fumble": 0
    }

    char1_level = success_levels[char1_success]
    char2_level = success_levels[char2_success]

    if char1_level > char2_level:
        return f"{char1_data['name']} wins the opposed check"
    elif char2_level > char1_level:
        return f"{char2_data['name']} wins the opposed check"
    else:
        # Same success level - compare the rolls against skill values
        char1_margin = get_skill_value(char1_data, char1_skill) - char1_roll
        char2_margin = get_skill_value(char2_data, char2_skill) - char2_roll

        if char1_margin > char2_margin:
            return f"{char1_data['name']} wins the opposed check (better margin)"
        elif char2_margin > char1_margin:
            return f"{char2_data['name']} wins the opposed check (better margin)"
        else:
            return "The opposed check results in a tie"

def get_skill_value(character_data, skill_name):
    """Helper function to get skill value from character data."""
    if 'skills' in character_data and skill_name in character_data['skills']:
        return character_data['skills'][skill_name]
    elif skill_name in character_data['attributes']:
        return character_data['attributes'][skill_name]
    else:
        raise ValueError(f"Skill or attribute '{skill_name}' not found for this character")

def roll_damage(weapon_data):
    """
    Roll damage for a weapon.

    Args:
        weapon_data: The weapon dictionary containing damage formula

    Returns:
        Integer damage result
    """
    try:
        return dr.roll_dice(weapon_data['damage'])
    except ValueError:
        # Handle damage formulas that might involve damage bonus
        damage_formula = weapon_data['damage']
        if '+1D4' in damage_formula:
            base_damage = damage_formula.replace('+1D4', '')
            bonus_damage = dr.roll_dice('1D4')
            return dr.roll_dice(base_damage) + bonus_damage
        else:
            # Just return the formula if we can't parse it
            return damage_formula