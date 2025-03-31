"""
Tests for User Interface Module

This module contains simplified tests for the UI functionality 
in the Call of Cthulhu text adventure game.

Author: Andrew C
Version: 1.1
Last Updated: 3/31/2025
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.ui import display_main_menu
from src.constants import UIStrings

def test_display_main_menu(capsys):
 """
 Verify that the main menu displays the correct options.
 """
 # Call the display function
 display_main_menu()

 # Capture the output
 captured = capsys.readouterr()
 output = captured.out

 # Assert core menu elements are present
 assert UIStrings.MainMenu.TITLE in output
 assert "View Premade Character" in output
 assert "Run Tests" in output
 assert "Exit" in output

def test_menu_basic_flow(monkeypatch, capsys):
 """
 Basic smoke test for menu navigation.

 This test ensures the menu can be instantiated and responds to basic inputs
 without getting into overly specific implementation details.
 """
 # Simulate user selecting exit
 inputs = iter(['3'])
 monkeypatch.setattr('builtins.input', lambda _: next(inputs))

 # Capture output to verify exit message
 from src.ui import menu
 menu()

 # Capture the output
 captured = capsys.readouterr()
 output = captured.out

 # Verify exit message appears
 assert "Exiting the Call of Cthulhu application" in output