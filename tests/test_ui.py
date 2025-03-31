"""
Tests for User Interface Module

This module contains unit tests for the UI functionality in the 
Call of Cthulhu text adventure game.

These tests validate menu interactions, input handling, and 
navigation between different parts of the application.

Author: Andrew C
Version: 1.0
Last Updated: 3/31/2025
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui import menu, display_main_menu, run_character_view
from src.constants import (
    UIStrings, 
    FileConstants, 
    TestConstants,
    ErrorMessages
)

def test_display_main_menu(capsys):
    """
    Test that the main menu displays correctly.
    """
    # Call the display function
    display_main_menu()

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out

    # Assert all menu options are displayed
    assert UIStrings.MainMenu.TITLE in output
    assert UIStrings.MainMenu.OPTION_VIEW_CHARACTER in output
    assert UIStrings.MainMenu.OPTION_RUN_TESTS in output
    assert UIStrings.MainMenu.OPTION_EXIT in output

def test_run_character_view():
    """
    Test the character view process.
    """
    # Prepare mock character files
    mock_characters = ['eleanor.json', 'jennifer.json']

    # Patch the individual methods separately to capture their calls
    with patch('os.path.join', return_value='characters/eleanor.json') as mock_path_join, \
         patch('builtins.input', side_effect=['1', '']), \
         patch('src.json_reader.load_character_from_json') as mock_load, \
         patch('src.json_reader.display_character') as mock_display:

        # Setup mock data for character loading
        expected_data = {
            'name': 'Eleanor Butler',
            'age': 39,
            'occupation': 'History Professor'
        }
        mock_load.return_value = expected_data

        # Call the character view function
        result = run_character_view(mock_characters)

        # Verify specific method calls
        mock_path_join.assert_called_with(UIStrings.CharacterViewer.CHARACTERS_DIR, 'eleanor.json')
        mock_load.assert_called_with('characters/eleanor.json')
        mock_display.assert_called_with(expected_data)
        assert result == expected_data

def test_run_character_view_return_to_menu():
    """
    Test returning to main menu in character view.
    """
    # Prepare mock character files
    mock_characters = ['eleanor.json', 'jennifer.json']

    with patch('builtins.input', return_value=str(len(mock_characters) + 1)), \
         patch('src.json_reader.load_character_from_json') as mock_load, \
         patch('src.json_reader.display_character') as mock_display:

        # Call the character view function
        result = run_character_view(mock_characters)

        # Verify no loading or display occurred
        mock_load.assert_not_called()
        mock_display.assert_not_called()
        assert result is None

def test_menu_flow():
    """
    Test the overall menu flow when viewing characters.
    """
    with patch('os.listdir', return_value=['eleanor.json', 'jennifer.json']), \
         patch('builtins.input', side_effect=['1', '1', '', '3']) as mock_input, \
         patch('os.path.join', return_value='characters/eleanor.json'), \
         patch('src.json_reader.load_character_from_json') as mock_load, \
         patch('src.json_reader.display_character') as mock_display, \
         patch('builtins.print') as mock_print, \
         patch('src.test_runner.test_menu') as mock_test_menu:

        # Setup mock character data
        expected_data = {
            'name': 'Eleanor Butler',
            'age': 39,
            'occupation': 'History Professor'
        }
        mock_load.return_value = expected_data

        # Call the menu function
        menu()

        # Verify the expected interactions
        mock_input.assert_has_calls([
            call(UIStrings.MainMenu.PROMPT),
            call(UIStrings.CharacterViewer.selection_prompt(3)),
            call(UIStrings.CharacterViewer.CONTINUE_PROMPT),
            call(UIStrings.MainMenu.PROMPT)
        ])
        mock_load.assert_called_once()
        mock_display.assert_called_once()
        mock_print.assert_any_call(UIStrings.MainMenu.EXIT_MESSAGE)

def test_menu_test_option_flow():
    """
    Test the test menu option flow.
    """
    with patch('builtins.input', side_effect=['2', '7', '3']) as mock_input, \
         patch('os.listdir', return_value=[]), \
         patch('src.test_runner.test_menu') as mock_test_menu, \
         patch('builtins.print') as mock_print:

        # Call the menu function
        menu()

        # Verify test menu was called and exit message printed
        mock_input.assert_has_calls([
            call(UIStrings.MainMenu.PROMPT),
            call(UIStrings.TestMenu.PROMPT),
            call(UIStrings.MainMenu.PROMPT)
        ])
        mock_test_menu.assert_called_once()
        mock_print.assert_any_call(UIStrings.MainMenu.EXIT_MESSAGE)

def test_menu_invalid_choice():
    """
    Test handling of invalid menu choices.
    """
    with patch('builtins.input', side_effect=['4', '3']) as mock_input, \
         patch('os.listdir', return_value=[]), \
         patch('builtins.print') as mock_print:

        # Call the menu function
        menu()

        # Verify invalid choice and exit messages
        mock_input.assert_has_calls([
            call(UIStrings.MainMenu.PROMPT),
            call(UIStrings.MainMenu.PROMPT)
        ])
        mock_print.assert_has_calls([
            call(UIStrings.MainMenu.INVALID_CHOICE),
            call(UIStrings.MainMenu.EXIT_MESSAGE)
        ])