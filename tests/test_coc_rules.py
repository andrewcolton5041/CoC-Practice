"""
Tests for Call of Cthulhu Rules Module

This module contains unit tests for the core rules mechanics for the Call of Cthulhu
roleplaying game, focusing on testing the success checks and improvement checks.

These tests validate that the functions in coc_rules.py follow the 7th edition
Call of Cthulhu rules correctly.

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

from unittest.mock import patch
from src.coc_rules import improvement_check, success_check
from src.constants import (
    SuccessLevel, 
    TestConstants, 
    RuleConstants,
    DiceConstants
)

import src.dice_roll as dr

# === Tests for success_check function ===

def test_extreme_success():
    """
    Test that success_check correctly identifies extreme success
    when the roll is less than or equal to skill/5.
    """
    # Arrange
    skill = TestConstants.SKILL_EXTREME_THRESHOLD
    expected_result = SuccessLevel.EXTREME_SUCCESS

    # Act
    with patch('src.dice_roll.roll_dice', return_value=TestConstants.EXTREME_SUCCESS_ROLL):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_hard_success():
    """
    Test that success_check correctly identifies hard success
    when the roll is less than or equal to skill/2 but greater than skill/5.
    """
    # Arrange
    skill = TestConstants.SKILL_HARD_THRESHOLD
    expected_result = SuccessLevel.HARD_SUCCESS

    # Act
    with patch('src.dice_roll.roll_dice', return_value=TestConstants.HARD_SUCCESS_ROLL):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_regular_success():
    """
    Test that success_check correctly identifies regular success
    when the roll is less than or equal to skill but greater than skill/2.
    """
    # Arrange
    skill = TestConstants.SKILL_REGULAR_THRESHOLD
    expected_result = SuccessLevel.REGULAR_SUCCESS

    # Act
    with patch('src.dice_roll.roll_dice', return_value=TestConstants.REGULAR_SUCCESS_ROLL):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_failure():
    """
    Test that success_check correctly identifies failure
    when the roll is greater than skill but not a fumble.
    """
    # Arrange
    skill = TestConstants.SKILL_REGULAR_THRESHOLD
    expected_result = SuccessLevel.FAILURE

    # Act
    with patch('src.dice_roll.roll_dice', return_value=TestConstants.FAILURE_ROLL):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_fumble_low_skill():
    """
    Test that success_check correctly identifies fumble for skills <= 50
    when the roll is 96-100.
    """
    # Arrange
    skill = RuleConstants.FumbleBoundaries.FUMBLE_THRESHOLD  # 50
    expected_result = SuccessLevel.FUMBLE

    # Act
    with patch('src.dice_roll.roll_dice', return_value=98):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_fumble_high_skill():
    """
    Test that success_check correctly identifies fumble for skills > 50
    when the roll is exactly 100.
    """
    # Arrange
    skill = RuleConstants.FumbleBoundaries.FUMBLE_THRESHOLD + 10  # 60
    expected_result = SuccessLevel.FUMBLE

    # Act
    with patch('src.dice_roll.roll_dice', return_value=100):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_high_skill_not_fumble():
    """
    Test that success_check correctly does not identify rolls of 96-99 as fumbles
    for skills > 50.
    """
    # Arrange
    skill = RuleConstants.FumbleBoundaries.FUMBLE_THRESHOLD + 10  # 60
    expected_result = SuccessLevel.FAILURE

    # Act
    with patch('src.dice_roll.roll_dice', return_value=97):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_exact_skill_roll():
    """
    Test that success_check correctly identifies regular success
    when the roll is exactly equal to the skill value.
    """
    # Arrange
    skill = TestConstants.SKILL_REGULAR_THRESHOLD
    expected_result = SuccessLevel.REGULAR_SUCCESS

    # Act
    with patch('src.dice_roll.roll_dice', return_value=skill):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_exact_half_skill_roll():
    """
    Test that success_check correctly identifies hard success
    when the roll is exactly equal to half the skill value.
    """
    # Arrange
    skill = TestConstants.SKILL_HARD_THRESHOLD
    expected_result = SuccessLevel.HARD_SUCCESS

    # Act
    with patch('src.dice_roll.roll_dice', return_value=skill // RuleConstants.SkillDivisors.HALF_VALUE):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_exact_fifth_skill_roll():
    """
    Test that success_check correctly identifies extreme success
    when the roll is exactly equal to one fifth of the skill value.
    """
    # Arrange
    skill = TestConstants.SKILL_EXTREME_THRESHOLD
    expected_result = SuccessLevel.EXTREME_SUCCESS

    # Act
    with patch('src.dice_roll.roll_dice', return_value=skill // RuleConstants.SkillDivisors.FIFTH_VALUE):
        result = success_check(skill)

    # Assert
    assert result == expected_result


def test_min_skill():
    """
    Test that success_check handles the minimum skill value (0) correctly.
    Everything should be a failure with zero skill.
    """
    # Arrange
    skill = TestConstants.MIN_SKILL
    expected_result = SuccessLevel.FAILURE

    # Act
    with patch('src.dice_roll.roll_dice', return_value=1):  # Even a roll of 1
        result = success_check(skill)

    # Assert
    assert result == expected_result


def success_check(stat: int) -> SuccessLevel:
    """
    Rolls 1D100 and determines the level of success based on the character's stat.

    According to CoC rules, the success level depends on how much lower the roll is
    compared to the character's stat:
    - Extreme Success: roll <= stat/5
    - Hard Success: roll <= stat/2
    - Regular Success: roll <= stat
    - Fumble: special case for very high rolls
    - Failure: roll > stat (and not a fumble)

    Args:
        stat (int): The character's stat or skill value (0-100).

    Returns:
        SuccessLevel: One of: EXTREME_SUCCESS, HARD_SUCCESS, REGULAR_SUCCESS, FAILURE, or FUMBLE
    """
    # Roll a d100
    roll = dr.roll_dice(DiceConstants.StandardDice.PERCENTILE.value)

    # Check for Extreme Success (Critical) - 1/5 of skill value
    if roll <= stat / RuleConstants.SkillDivisors.FIFTH_VALUE:
        return SuccessLevel.EXTREME_SUCCESS
    # Check for Hard Success - 1/2 of skill value
    elif roll <= stat / RuleConstants.SkillDivisors.HALF_VALUE:
        return SuccessLevel.HARD_SUCCESS
    # Check for Regular Success - equal to or under skill value
    elif roll <= stat:
        return SuccessLevel.REGULAR_SUCCESS
    # Check for Fumble
    elif (stat <= RuleConstants.FumbleBoundaries.FUMBLE_THRESHOLD and 
          RuleConstants.FumbleBoundaries.FUMBLE_RANGE_LOW <= roll) or \
         (stat > RuleConstants.FumbleBoundaries.FUMBLE_THRESHOLD and roll == 100):
        return SuccessLevel.FUMBLE
    # Everything else is a normal failure
    else:
        return SuccessLevel.FAILURE


# === Tests for improvement_check function ===

def test_improvement_successful():
    """
    Test that improvement_check returns True when the roll is greater than the stat.
    """
    # Arrange
    stat = 50

    # Act
    with patch('src.dice_roll.roll_dice', return_value=60):
        result = improvement_check(stat)

    # Assert
    assert result == True


def test_improvement_failed():
    """
    Test that improvement_check returns False when the roll is less than or equal to the stat.
    """
    # Arrange
    stat = 50

    # Act
    with patch('src.dice_roll.roll_dice', return_value=40):
        result = improvement_check(stat)

    # Assert
    assert result == False


def test_improvement_equal_to_stat():
    """
    Test that improvement_check returns False when the roll is exactly equal to the stat.
    """
    # Arrange
    stat = 50

    # Act
    with patch('src.dice_roll.roll_dice', return_value=50):
        result = improvement_check(stat)

    # Assert
    assert result == False


def test_improvement_low_stat():
    """
    Test improvement_check with a very low stat.
    """
    # Arrange
    stat = 5

    # Act - Test with roll 10 (should be success)
    with patch('src.dice_roll.roll_dice', return_value=10):
        result = improvement_check(stat)
        assert result == True

    # Act - Test with roll 1 (should be failure)
    with patch('src.dice_roll.roll_dice', return_value=1):
        result = improvement_check(stat)
        assert result == False


def test_improvement_high_stat():
    """
    Test improvement_check with a very high stat.
    Improvement chances are very low for high stats.
    """
    # Arrange
    stat = 95

    # Act - Test with roll 96 (should be success)
    with patch('src.dice_roll.roll_dice', return_value=96):
        result = improvement_check(stat)
        assert result == True

    # Act - Test with roll 94 (should be failure)
    with patch('src.dice_roll.roll_dice', return_value=94):
        result = improvement_check(stat)
        assert result == False