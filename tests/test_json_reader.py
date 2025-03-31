"""
Tests for JSON Reader Module

This module contains unit tests for the JSON character file loading
and display functionality in the Call of Cthulhu text adventure game.

These tests validate the JSON reading and character display functions
for accuracy and proper error handling.

Author: Andrew C
Version: 1.0
Last Updated: 03/31/2025
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, mock_open

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.json_reader import load_character_from_json, display_character
from src.constants import (
    CharacterSheetKeys, 
    FileConstants, 
    TestConstants,
    ErrorMessages
)

@pytest.fixture
def sample_character_data():
    """
    Fixture providing a sample character data dictionary for testing.
    """
    return {
        CharacterSheetKeys.NAME: "Test Character",
        CharacterSheetKeys.AGE: 30,
        CharacterSheetKeys.OCCUPATION: "Investigator",
        CharacterSheetKeys.NATIONALITY: "American",
        CharacterSheetKeys.ATTRIBUTES: {
            "Strength": 50,
            "Dexterity": 60
        },
        CharacterSheetKeys.SKILLS: {
            "Stealth": 40,
            "History": 50
        },
        CharacterSheetKeys.WEAPONS: [
            {
                CharacterSheetKeys.WEAPON_NAME: "Revolver",
                CharacterSheetKeys.WEAPON_SKILL: 50,
                CharacterSheetKeys.WEAPON_DAMAGE: "1D8"
            }
        ],
        CharacterSheetKeys.BACKSTORY: "A brave investigator seeking truth."
    }

def test_load_character_from_json(sample_character_data):
    """
    Test loading a character from a JSON file.
    """
    # Arrange
    json_string = """{
        "name": "Test Character",
        "age": 30,
        "occupation": "Investigator",
        "nationality": "American",
        "attributes": {"Strength": 50, "Dexterity": 60},
        "skills": {"Stealth": 40, "History": 50},
        "weapons": [{"name": "Revolver", "skill": 50, "damage": "1D8"}],
        "backstory": "A brave investigator seeking truth."
    }"""

    # Mock the file opening
    m = mock_open(read_data=json_string)

    # Act
    with patch('builtins.open', m):
        character_data = load_character_from_json("test_character.json")

    # Assert
    assert character_data == sample_character_data

def test_load_character_from_json_file_not_found():
    """
    Test error handling when the JSON file is not found.
    """
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        load_character_from_json("nonexistent_file.json")

def test_display_character(sample_character_data, capsys):
    """
    Test the display_character function outputs correct information.
    """
    # Act
    display_character(sample_character_data)

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out

    # Assert
    # Check for key character information in the output
    assert "Test Character" in output
    assert "30" in output
    assert "Investigator" in output
    assert "American" in output

    # Check attribute display
    assert "Strength: 50" in output
    assert "Dexterity: 60" in output

    # Check skills display
    assert "Stealth: 40" in output
    assert "History: 50" in output

    # Check weapons display
    assert "Revolver" in output
    assert "Skill: 50" in output
    assert "Damage: 1D8" in output

    # Check backstory display
    assert "A brave investigator seeking truth." in output

def test_display_character_minimal_data():
    """
    Test display_character with minimal character data.
    """
    # Arrange
    minimal_data = {
        CharacterSheetKeys.NAME: "Minimal Character",
        CharacterSheetKeys.AGE: 25,
        CharacterSheetKeys.ATTRIBUTES: {}
    }

    # Act & Assert
    try:
        display_character(minimal_data)
    except Exception as e:
        pytest.fail(f"display_character raised an exception with minimal data: {e}")

def test_display_character_missing_optional_fields(sample_character_data):
    """
    Test display_character when some optional fields are missing.
    """
    # Arrange
    incomplete_data = sample_character_data.copy()
    del incomplete_data[CharacterSheetKeys.SKILLS]
    del incomplete_data[CharacterSheetKeys.WEAPONS]
    del incomplete_data[CharacterSheetKeys.BACKSTORY]

    # Act & Assert
    try:
        display_character(incomplete_data)
    except Exception as e:
        pytest.fail(f"display_character raised an exception with missing fields: {e}")

def test_json_file_extension():
    """
    Test that only JSON files can be loaded.
    """
    # Arrange
    non_json_files = [
        "character.txt",
        "character.csv",
        "character",
        "character.py"
    ]

    # Act & Assert
    for filename in non_json_files:
        with pytest.raises(ValueError, match=r".*\.json"):
            load_character_from_json(filename)