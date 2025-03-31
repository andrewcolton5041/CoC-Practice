import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from src.character_utils import opposed_check, skill_check
from src.constants import SuccessLevel, CharacterSheetKeys

def test_skill_check_from_skills_successful():
    """
    Test that skill_check correctly checks a skill from the character's skills
    and returns a success when the roll is below the skill value.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.SKILLS: {
            "Stealth": 60  # Character has 60% in Stealth skill
        }
    }

    # We need to patch both the dice roll and the success_check function
    with patch('src.character_utils.roll_dice', return_value=40), \
         patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):

        # Act
        roll_result, success_level = skill_check(character_data, "Stealth")

        # Assert
        assert roll_result == 40
        assert success_level == SuccessLevel.REGULAR_SUCCESS

def test_attribute_check_from_attributes_successful():
    """
    Test that attribute_check correctly checks an attribute from the character's attributes
    and returns a success when the roll is below the attribute value.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 60  # Character has 60% in Strength attribute
        }
    }

    # We need to patch both the dice roll and the success_check function
    with patch('src.character_utils.roll_dice', return_value=40), \
         patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):

        # Act
        roll_result, success_level = skill_check(character_data, "Strength")

        # Assert
        assert roll_result == 40
        assert success_level == SuccessLevel.REGULAR_SUCCESS

def test_non_existant_skill_or_attribute_returns_error():
    """
    Test that skill_check returns an error when the skill or attribute doesn't
    exist.
    """

    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 60  # Character has 60% in Strength attribute
        }
    }

    # We need to patch both the dice roll and the success_check function
    with patch('src.character_utils.roll_dice', return_value=40), \
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
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 0  
        }
    }

    with patch('src.character_utils.roll_dice', return_value=40), \
     patch('src.character_utils.success_check', return_value=SuccessLevel.FAILURE):
         # Act
         roll_result, success_level = skill_check(character_data, "Strength")

         # Assert
         assert roll_result == 40
         assert success_level == SuccessLevel.FAILURE

def test_skill_upper_edge_boundary():
    """
    Test that skill_check correctly checks a skill of 100
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 100  
        }
    }

    with patch('src.character_utils.roll_dice', return_value=1), \
     patch('src.character_utils.success_check', return_value=SuccessLevel.EXTREME_SUCCESS):
         # Act
         roll_result, success_level = skill_check(character_data, "Strength")

         # Assert
         assert roll_result == 1
         assert success_level == SuccessLevel.EXTREME_SUCCESS

def test_skill_return_format_correct():
    """
    Test that skill_check correctly checks the return is a correctly
    formated tuple.
    """
    # Arrange
    character_data = {
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 60  
        }
    }

    with patch('src.character_utils.roll_dice', return_value=50), \
     patch('src.character_utils.success_check', return_value=SuccessLevel.REGULAR_SUCCESS):
         # Act
         tup = skill_check(character_data, "Strength")

         # Assert
          
        
         assert isinstance(tup, tuple) # Check that the return is a tuple
         assert len(tup) == 2 # Check that the tuple has 2 elements
         assert isinstance(tup[0], int) # Check that the first element is an int
         assert isinstance(tup[1], SuccessLevel) # Check that the second element is a SuccessLevel



#Test when first character clearly wins (higher success level)
def test_first_char_wins_opposed_check():
    """
    Test that opposed_check correctly checks the first character wins when the
    first character has a success and the second has a failure.
    
    """

    #Arrange
    character1_data = {
        CharacterSheetKeys.NAME: "A",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 60  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: "B",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 5
        }
    }

    with patch('src.character_utils.roll_dice', return_value = 10):
        #Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        #Assert
        assert result == "A wins the opposed check!"

#Test when second character clearly wins (higher success level)
def test_first_second_wins_opposed_check():
    """
    Test that opposed_check correctly checks the first character wins when the
    first character has a success and the second has a failure.

    """

    #Arrange
    character1_data = {
        CharacterSheetKeys.NAME: "A",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 5  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: "B",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 50
        }
    }

    with patch('src.character_utils.roll_dice', return_value = 10):
        #Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        #Assert
        assert result == "B wins the opposed check!"


#Test tie-breaking with margins when both have same success level
def test_first_second_wins_opposed_check():
    """
    Test that opposed_check correctly checks the first character wins when the
    first character has a success and the second has a failure.

    """

    #Arrange
    character1_data = {
        CharacterSheetKeys.NAME: "A",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 5  
        }
    }

    character2_data = {
        CharacterSheetKeys.NAME: "B",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 50
        }
    }

    with patch('src.character_utils.success_check', return_value = SuccessLevel.REGULAR_SUCCESS):
        #Act
        result = opposed_check(character1_data, "Strength", character2_data, "Strength")

        #Assert
        assert result == "B wins the opposed check!"