"""
Tests for Investigator Development Phase Module

This module contains unit tests for the skill improvement mechanics
in the Call of Cthulhu RPG development phase.

Author: Andrew C
Version: 1.0
Last Updated: 3/31/2025
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch
from typing import Dict, List, Optional

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.investigator_development_phase import (
    InvestigatorDevelopmentPhase, 
    perform_development_phase
)
from src.constants import (
    CharacterSheetKeys, 
    TestConstants,
    RuleConstants
)

@pytest.fixture
def sample_character_data():
    """
    Fixture providing a sample character data dictionary for testing.
    """
    return {
        CharacterSheetKeys.NAME: "Test Investigator",
        CharacterSheetKeys.SKILLS: {
            "Stealth": 40,
            "History": 50,
            "Cthulhu Mythos": 10,
            "Credit Rating": 30,
            "Persuade": 60
        }
    }


def test_can_improve_skill():
    """
    Test that skills can be correctly identified as improvable.
    """
    dev_phase = InvestigatorDevelopmentPhase()

    # Assert skills that can be improved
    assert dev_phase.can_improve_skill("Stealth") == True
    assert dev_phase.can_improve_skill("History") == True
    assert dev_phase.can_improve_skill("Persuade") == True

    # Assert skills that cannot be improved
    assert dev_phase.can_improve_skill("Cthulhu Mythos") == False
    assert dev_phase.can_improve_skill("Credit Rating") == False


def test_skill_improvement_success(sample_character_data: Dict):
    """
    Test that a skill can be successfully improved.
    """
    dev_phase = InvestigatorDevelopmentPhase()

    # Mock improvement check to always return True
    with patch('src.investigator_development_phase.improvement_check', return_value=True), \
         patch('random.randint', return_value=5):

        # Attempt to improve Stealth skill
        improved_character: Optional[Dict] = dev_phase.improve_skill(sample_character_data, "Stealth")

        # Assert skill was improved
        assert improved_character is not None
        assert improved_character[CharacterSheetKeys.SKILLS]["Stealth"] == 45


def test_skill_improvement_failure(sample_character_data):
    """
    Test that a skill is not improved when improvement check fails.
    """
    dev_phase = InvestigatorDevelopmentPhase()

    # Mock improvement check to always return False
    with patch('src.investigator_development_phase.improvement_check', return_value=False):

        # Attempt to improve Stealth skill
        improved_character = dev_phase.improve_skill(sample_character_data, "Stealth")

        # Assert skill was not improved
        assert improved_character is None


def test_development_phase_multiple_skills(sample_character_data):
    """
    Test the full development phase with multiple skills.
    """
    # List of skills to check for improvement
    checked_skills = ["Stealth", "History", "Persuade"]

    # Mock improvement process to always succeed and add 5 points
    with patch('src.investigator_development_phase.improvement_check', return_value=True), \
         patch('random.randint', return_value=5):

        # Perform development phase
        result = perform_development_phase(sample_character_data, checked_skills)

        # Assert character data was updated
        assert result['character_data'][CharacterSheetKeys.SKILLS]["Stealth"] == 45
        assert result['character_data'][CharacterSheetKeys.SKILLS]["History"] == 55
        assert result['character_data'][CharacterSheetKeys.SKILLS]["Persuade"] == 65

        # Assert improved skills were tracked
        assert set(result['improved_skills']) == set(["Stealth", "History", "Persuade"])


def test_skill_improvement_max_value(sample_character_data: Dict):
    """
    Test that skills cannot exceed the maximum skill value.
    """
    # Set a skill close to max value
    sample_character_data[CharacterSheetKeys.SKILLS]["Stealth"] = 98

    dev_phase = InvestigatorDevelopmentPhase()

    # Mock improvement check to always return True with high improvement
    with patch('src.investigator_development_phase.improvement_check', return_value=True), \
         patch('random.randint', return_value=10):

        # Attempt to improve Stealth skill
        improved_character = dev_phase.improve_skill(sample_character_data, "Stealth")

        # Assert the character was improved and check the skill value
        assert improved_character is not None
        assert improved_character[CharacterSheetKeys.SKILLS]["Stealth"] == RuleConstants.MAX_SKILL_VALUE


def test_excluded_skills_not_improved(sample_character_data):
    """
    Test that Cthulhu Mythos and Credit Rating are never improved.
    """
    dev_phase = InvestigatorDevelopmentPhase()

    # Attempt to improve excluded skills
    mythos_result = dev_phase.improve_skill(sample_character_data, "Cthulhu Mythos")
    credit_result = dev_phase.improve_skill(sample_character_data, "Credit Rating")

    # Assert no improvement occurs
    assert mythos_result is None
    assert credit_result is None