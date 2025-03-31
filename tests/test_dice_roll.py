"""
Tests for Dice Rolling Utility Module

This module contains unit tests for the dice rolling mechanics in the 
Call of Cthulhu text adventure game.

These tests validate the dice rolling functions for accuracy, 
edge cases, and adherence to the game's probabilistic requirements.

Author: Andrew C
Version: 1.0
Last Updated: 03/31/2025
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dice_roll import roll_dice
from src.constants import (
    DiceConstants, 
    SystemLimits, 
    ErrorMessages, 
    TestConstants
)

def test_standard_dice_roll():
    """
    Test a standard dice roll with simple notation like "3D6".
    """
    # Arrange
    dice_string = "3D6"

    # Act
    result = roll_dice(dice_string)

    # Assert
    assert isinstance(result, int)
    assert result >= 3  # Minimum possible roll
    assert result <= 18  # Maximum possible roll

def test_dice_roll_with_modifier():
    """
    Test dice roll with a modifier like "2D6+3".
    """
    # Arrange
    dice_string = "2D6+3"

    # Act
    result = roll_dice(dice_string)

    # Assert
    assert isinstance(result, int)
    assert result >= 5  # Minimum possible roll (2 + 3)
    assert result <= 15  # Maximum possible roll (12 + 3)

def test_dice_roll_with_subtraction():
    """
    Test dice roll with subtraction like "2D6-1".
    """
    # Arrange
    dice_string = "2D6-1"

    # Act
    result = roll_dice(dice_string)

    # Assert
    assert isinstance(result, int)
    assert result >= 1  # Minimum possible roll (2 - 1)
    assert result <= 11  # Maximum possible roll (12 - 1)

def test_dice_roll_with_multiplication():
    """
    Test dice roll with multiplication like "2D6*5".
    """
    # Arrange
    dice_string = "(2D6)*5"

    # Act
    result = roll_dice(dice_string)

    # Assert
    assert isinstance(result, int)
    assert result >= 10  # Minimum possible roll (2 * 5)
    assert result <= 60  # Maximum possible roll (12 * 5)

def test_return_details_option():
    """
    Test that return_details provides both total and individual rolls.
    """
    # Arrange
    dice_string = "3D6"

    # Act
    result = roll_dice(dice_string, return_details=True)

    # Assert
    assert isinstance(result, dict)
    assert "total" in result
    assert "rolls" in result
    assert isinstance(result["total"], int)
    assert isinstance(result["rolls"], list)
    assert len(result["rolls"]) == 3  # Because we rolled 3D6

def test_invalid_dice_format():
    """
    Test that invalid dice string formats raise a ValueError.
    """
    # Arrange
    invalid_formats = [
        "XD6",     # Invalid number of dice
        "3DX",     # Invalid number of sides
        "3D6+X",   # Invalid modifier
        "3D6**5",  # Invalid multiplier
    ]

    # Act & Assert
    for invalid_format in invalid_formats:
        with pytest.raises(ValueError, match=ErrorMessages.INVALID_DICE_FORMAT):
            roll_dice(invalid_format)

def test_max_dice_count_limit():
    """
    Test that exceeding the maximum dice count raises a ValueError.
    """
    # Arrange
    excessive_dice_string = f"{SystemLimits.MAX_DICE_COUNT + 1}D6"

    # Act & Assert
    with pytest.raises(ValueError, match=ErrorMessages.INVALID_DICE_COUNT):
        roll_dice(excessive_dice_string)

def test_max_dice_sides_limit():
    """
    Test that exceeding the maximum dice sides raises a ValueError.
    """
    # Arrange
    excessive_sides_string = f"3D{SystemLimits.MAX_DICE_SIDES + 1}"

    # Act & Assert
    with pytest.raises(ValueError, match=ErrorMessages.INVALID_DICE_SIDES):
        roll_dice(excessive_sides_string)

def test_percentile_dice_roll():
    """
    Test rolling a percentile dice (1D100).
    """
    # Arrange
    dice_string = DiceConstants.StandardDice.PERCENTILE.value

    # Act
    result = roll_dice(dice_string)

    # Assert
    assert isinstance(result, int)
    assert 1 <= result <= 100

def test_randomness_distribution():
    """
    Simple statistical test to ensure some level of randomness.
    This is not a comprehensive statistical test, but a basic sanity check.
    """
    # Arrange
    dice_string = "1D6"
    rolls = [roll_dice(dice_string) for _ in range(1000)]

    # Act & Assert
    # Check that we have values from 1 to 6
    assert set(rolls) == set(range(1, 7))

    # Check that distribution is somewhat even (not perfectly, but reasonably)
    import statistics
    mean = statistics.mean(rolls)
    assert 3.0 <= mean <= 4.0  # Expected mean for 1D6