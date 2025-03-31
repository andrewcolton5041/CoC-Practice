import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock
from src.character_utils import opposed_check, skill_check, get_skill_value, roll_damage
from src.constants import SuccessLevel, CharacterSheetKeys, TestConstants

# === Tests for skill_check function ===

def test_skill_check_from_skills_successful():
    """
    Test that skill_check correctly checks a skill from the character's skills
    and returns a success when the roll is below the skill value.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.SKILLS: {
            "Stealth": TestConstants.SkillValues.AVERAGE_SKILL  # Character has 50% in Stealth skill
        }
    }

    # We need to patch both the dice roll and the success_check function
    with patch('src.character_utils.roll_dice', return_value=TestConstants.DiceValues.REGULAR_SUCCESS), \
         patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):

        # Act
        roll_result, success_level = skill_check(character_data, "Stealth")

        # Assert
        assert roll_result == TestConstants.DiceValues.REGULAR_SUCCESS
        assert success_level == SuccessLevel.REGULAR_SUCCESS

def test_attribute_check_from_attributes_successful():
    """
    Test that attribute_check correctly checks an attribute from the character's attributes
    and returns a success when the roll is below the attribute value.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL  # Character has 50% in Strength attribute
        }
    }

    # We need to patch both the dice roll and the success_check function
    with patch('src.character_utils.roll_dice', return_value=TestConstants.DiceValues.REGULAR_SUCCESS), \
         patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):

        # Act
        roll_result, success_level = skill_check(character_data, "Strength")

        # Assert
        assert roll_result == TestConstants.DiceValues.REGULAR_SUCCESS
        assert success_level == SuccessLevel.REGULAR_SUCCESS

def test_non_existant_skill_or_attribute_returns_error():
    """
    Test that skill_check returns an error when the skill or attribute doesn't
    exist.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL  # Character has 50% in Strength attribute
        }
    }

    # We need to patch both the dice roll and the success_check function
    with patch('src.character_utils.roll_dice', return_value=TestConstants.DiceValues.REGULAR_SUCCESS), \
         patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):

        with pytest.raises(ValueError):
            # Act
            skill_check(character_data, "Intelligence")         

def test_skill_lower_edge_boundary():
    """
    Test that skill_check correctly checks a skill of 0
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.MIN_SKILL  
        }
    }

    with patch('src.character_utils.roll_dice', return_value=TestConstants.DiceValues.REGULAR_SUCCESS), \
     patch('src.character_utils.success_check', return_value=SuccessLevel.FAILURE):
         # Act
         roll_result, success_level = skill_check(character_data, "Strength")

         # Assert
         assert roll_result == TestConstants.DiceValues.REGULAR_SUCCESS
         assert success_level == SuccessLevel.FAILURE

def test_skill_upper_edge_boundary():
    """
    Test that skill_check correctly checks a skill of 100
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.MAX_SKILL  
        }
    }

    with patch('src.character_utils.roll_dice', return_value=TestConstants.DiceValues.CRITICAL_SUCCESS), \
     patch('src.character_utils.success_check', return_value=SuccessLevel.EXTREME_SUCCESS):
         # Act
         roll_result, success_level = skill_check(character_data, "Strength")

         # Assert
         assert roll_result == TestConstants.DiceValues.CRITICAL_SUCCESS
         assert success_level == SuccessLevel.EXTREME_SUCCESS

def test_skill_return_format_correct():
    """
    Test that skill_check correctly formats the return as a
    tuple with the expected types.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL  
        }
    }

    with patch('src.character_utils.roll_dice', return_value=TestConstants.DiceValues.REGULAR_SUCCESS), \
     patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):
         # Act
         tup = skill_check(character_data, "Strength")

         # Assert
         assert isinstance(tup, tuple)  # Check that the return is a tuple
         assert len(tup) == 2  # Check that the tuple has 2 elements
         assert isinstance(tup[0], int)  # Check that the first element is an int
         assert isinstance(tup[1], SuccessLevel)  # Check that the second element is a SuccessLevel


# === Tests for opposed_check function ===

def test_first_char_wins_opposed_check():
    """
    Test that opposed_check correctly identifies when the first character wins
    because they have a higher success level than the second character.
    """
    # Arrange
    character1_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_1_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_2_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.LOW_SKILL
        }
    }

    with patch('src.character_utils.skill_check') as mock_skill_check:
        # Configure mock to return different success levels for each character
        mock_skill_check.side_effect = [
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.HARD_SUCCESS),    # First character gets Hard Success
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS)  # Second character gets Regular Success
        ]

        # Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        # Assert
        assert result == f"{TestConstants.CharacterNames.CHARACTER_1_NAME} wins the opposed check!"

def test_second_char_wins_opposed_check():
    """
    Test that opposed_check correctly identifies when the second character wins
    because they have a higher success level than the first character.
    """
    # Arrange
    character1_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_1_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.LOW_SKILL  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_2_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL
        }
    }

    with patch('src.character_utils.skill_check') as mock_skill_check:
        # Configure mock to return different success levels for each character
        mock_skill_check.side_effect = [
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS),  # First character gets Regular Success
            (TestConstants.DiceValues.CRITICAL_SUCCESS, SuccessLevel.EXTREME_SUCCESS)   # Second character gets Extreme Success
        ]

        # Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        # Assert
        assert result == f"{TestConstants.CharacterNames.CHARACTER_2_NAME} wins the opposed check!"

def test_tie_breaking_with_better_margin():
    """
    Test that opposed_check correctly breaks ties when both characters have
    the same success level but different margins of success.
    """
    # Arrange
    character1_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_1_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_2_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.HIGH_SKILL
        }
    }

    with patch('src.character_utils.skill_check') as mock_skill_check, \
         patch('src.character_utils.get_skill_value') as mock_get_skill_value:
        # Both characters get Regular Success
        mock_skill_check.side_effect = [
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS),  # First character 
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS)   # Second character
        ]

        # But second character has a better margin (70-40=30 vs 50-40=10)
        mock_get_skill_value.side_effect = [
            TestConstants.SkillValues.AVERAGE_SKILL, 
            TestConstants.SkillValues.HIGH_SKILL
        ]

        # Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        # Assert
        assert result == f"{TestConstants.CharacterNames.CHARACTER_2_NAME} wins the opposed check! (Better Margin)"

def test_complete_tie_case():
    """
    Test that opposed_check correctly identifies a complete tie when both
    characters have the same success level and same margin of success.
    """
    # Arrange
    character1_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_1_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_2_NAME,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.AVERAGE_SKILL
        }
    }

    with patch('src.character_utils.skill_check') as mock_skill_check, \
         patch('src.character_utils.get_skill_value') as mock_get_skill_value:
        # Both characters get Regular Success
        mock_skill_check.side_effect = [
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS),  # First character 
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS)   # Second character
        ]

        # Both have the same margin (50-40=10)
        mock_get_skill_value.side_effect = [
            TestConstants.SkillValues.AVERAGE_SKILL, 
            TestConstants.SkillValues.AVERAGE_SKILL
        ]

        # Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        # Assert
        assert result == "The opposed check results in a tie"

def test_opposed_check_different_skills():
    """
    Test that opposed_check correctly handles when each character is using
    a different skill for the check.
    """
    # Arrange
    character1_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_1_NAME,
        CharacterSheetKeys.SKILLS: {
            "Stealth": TestConstants.SkillValues.HIGH_SKILL  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_2_NAME,
        CharacterSheetKeys.SKILLS: {
            "Spot Hidden": TestConstants.SkillValues.AVERAGE_SKILL
        }
    }

    with patch('src.character_utils.skill_check') as mock_skill_check:
        # Configure mock to return success levels
        mock_skill_check.side_effect = [
            (TestConstants.DiceValues.CRITICAL_SUCCESS, SuccessLevel.HARD_SUCCESS),     # First character using Stealth
            (TestConstants.DiceValues.REGULAR_SUCCESS, SuccessLevel.REGULAR_SUCCESS)   # Second character using Spot Hidden
        ]

        # Act
        result = opposed_check(character1_data, "Stealth", character2_data, "Spot Hidden")

        # Assert
        assert result == f"{TestConstants.CharacterNames.CHARACTER_1_NAME} wins the opposed check!"
        # Verify the correct skills were used
        mock_skill_check.assert_any_call(character1_data, "Stealth")
        mock_skill_check.assert_any_call(character2_data, "Spot Hidden")

def test_opposed_check_error_handling():
    """
    Test that opposed_check properly handles errors when skills don't exist.
    """
    # Arrange
    character1_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_1_NAME,
        CharacterSheetKeys.SKILLS: {
            "Stealth": TestConstants.SkillValues.HIGH_SKILL  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.CHARACTER_2_NAME,
        CharacterSheetKeys.SKILLS: {
            "Spot Hidden": TestConstants.SkillValues.AVERAGE_SKILL
        }
    }

    with patch('src.character_utils.skill_check') as mock_skill_check:
        # First call works, second call raises ValueError for non-existent skill
        mock_skill_check.side_effect = [
            (TestConstants.DiceValues.CRITICAL_SUCCESS, SuccessLevel.HARD_SUCCESS),  # First character
            ValueError("Skill 'Nonexistent' not found for this character")  # Second character
        ]

        # Act and Assert
        with pytest.raises(ValueError):
            opposed_check(character1_data, "Stealth", character2_data, "Nonexistent")


# === Tests for get_skill_value function ===

def test_get_skill_from_skills():
    """
    Test that get_skill_value correctly retrieves a skill value from
    the character's skills dictionary.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.SKILLS: {
            "Stealth": TestConstants.SkillValues.AVERAGE_SKILL
        }
    }

    # Act
    skill_value = get_skill_value(character_data, "Stealth")

    # Assert
    assert skill_value == TestConstants.SkillValues.AVERAGE_SKILL

def test_get_skill_from_attributes():
    """
    Test that get_skill_value correctly retrieves a value from
    the character's attributes dictionary.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.HIGH_SKILL
        }
    }

    # Act
    attribute_value = get_skill_value(character_data, "Strength")

    # Assert
    assert attribute_value == TestConstants.SkillValues.HIGH_SKILL

def test_get_skill_value_error_handling():
    """
    Test that get_skill_value raises an appropriate error when
    the requested skill or attribute doesn't exist.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: TestConstants.CharacterNames.TEST_CHARACTER,
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": TestConstants.SkillValues.HIGH_SKILL
        },
        CharacterSheetKeys.SKILLS: {
            "Stealth": TestConstants.SkillValues.AVERAGE_SKILL
        }
    }

    # Act and Assert
    with pytest.raises(ValueError) as excinfo:
        get_skill_value(character_data, "Nonexistent")

    # Check that the error message contains the name of the missing skill
    assert "Nonexistent" in str(excinfo.value)


# === Tests for roll_damage function ===

def test_simple_damage_formula():
    """
    Test that roll_damage correctly calculates damage for a simple
    dice formula like "1D6".
    """
    # Arrange
    weapon_data = {
        CharacterSheetKeys.WEAPON_NAME: "Dagger",
        CharacterSheetKeys.WEAPON_SKILL: TestConstants.SkillValues.AVERAGE_SKILL,
        CharacterSheetKeys.WEAPON_DAMAGE: TestConstants.WeaponData.SIMPLE_WEAPON_DAMAGE
    }

    with patch('src.character_utils.roll_dice', return_value=4):
        # Act
        damage = roll_damage(weapon_data)

        # Assert
        assert damage == 4

def test_complex_damage_formula():
    """
    Test that roll_damage correctly calculates damage for a complex
    formula with addition/subtraction like "1D8+1".
    """
    # Arrange
    weapon_data = {
        CharacterSheetKeys.WEAPON_NAME: "Sword",
        CharacterSheetKeys.WEAPON_SKILL: TestConstants.SkillValues.AVERAGE_SKILL,
        CharacterSheetKeys.WEAPON_DAMAGE: TestConstants.WeaponData.COMPLEX_WEAPON_DAMAGE
    }

    with patch('src.character_utils.roll_dice', return_value=7):
        # Act
        damage = roll_damage(weapon_data)

        # Assert
        assert damage == 7

def test_damage_formula_with_damage_bonus():
    """
    Test that roll_damage correctly handles damage formulas that include
    the character's damage bonus, like "1D3+1D4".
    """
    # Arrange
    weapon_data = {
        CharacterSheetKeys.WEAPON_NAME: "Brawl",
        CharacterSheetKeys.WEAPON_SKILL: TestConstants.SkillValues.AVERAGE_SKILL,
        CharacterSheetKeys.WEAPON_DAMAGE: TestConstants.WeaponData.BONUS_WEAPON_DAMAGE
    }

    # We need to mock roll_dice differently for this case
    with patch('src.character_utils.roll_dice') as mock_roll_dice:
        # Configure the mock to handle different arguments
        def side_effect(dice_string, *args, **kwargs):
            if dice_string == "1D3":
                return 2
            elif dice_string == "1D4":
                return 3
            elif dice_string == "1D3+1D4":  # The full formula
                # This should raise ValueError to trigger the special handling
                raise ValueError("Complex formula")
            return 0

        mock_roll_dice.side_effect = side_effect

        # Act
        damage = roll_damage(weapon_data)

        # Assert
        assert damage == 5

def test_unparseable_damage_formula():
    """
    Test that roll_damage correctly handles damage formulas that can't be parsed,
    by returning the formula string.
    """
    # Arrange
    weapon_data = {
        CharacterSheetKeys.WEAPON_NAME: "Special Weapon",
        CharacterSheetKeys.WEAPON_SKILL: TestConstants.SkillValues.AVERAGE_SKILL,
        CharacterSheetKeys.WEAPON_DAMAGE: TestConstants.WeaponData.UNPARSEABLE_DAMAGE
    }

    with patch('src.character_utils.roll_dice', side_effect=ValueError("Invalid dice format")):
        # Act
        damage = roll_damage(weapon_data)

        # Assert
        assert damage == TestConstants.WeaponData.UNPARSEABLE_DAMAGE
        assert isinstance(damage, str)

def test_damage_edge_cases():
    """
    Test that roll_damage correctly handles extreme damage values,
    both minimum and maximum possible.
    """
    # Arrange - Minimum possible damage (1 on 1D4)
    min_weapon_data = {
        CharacterSheetKeys.WEAPON_NAME: "Weak Weapon",
        CharacterSheetKeys.WEAPON_SKILL: TestConstants.SkillValues.LOW_SKILL,
        CharacterSheetKeys.WEAPON_DAMAGE: TestConstants.WeaponData.MIN_WEAPON_DAMAGE
    }

    # Arrange - Maximum possible damage (24 on 4D6)
    max_weapon_data = {
        CharacterSheetKeys.WEAPON_NAME: "Powerful Weapon",
        CharacterSheetKeys.WEAPON_SKILL: TestConstants.SkillValues.HIGH_SKILL,
        CharacterSheetKeys.WEAPON_DAMAGE: TestConstants.WeaponData.MAX_WEAPON_DAMAGE
    }

    with patch('src.character_utils.roll_dice') as mock_roll_dice:
        # Min roll - 1 on 1D4
        mock_roll_dice.return_value = 1
        min_damage = roll_damage(min_weapon_data)

        # Reset mock for max roll
        mock_roll_dice.return_value = 24
        max_damage = roll_damage(max_weapon_data)

    # Assert
    assert min_damage == 1
    assert max_damage == 24