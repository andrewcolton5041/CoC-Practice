"""
Call of Cthulhu Main

This is the main module for a Call of Cthulhu character management application.
It provides functionality to:
- Load premade characters from JSON files
- Display character information in a formatted way
- Navigate through a menu-based interface

This application can be used by game masters and players to quickly access
character information for the Call of Cthulhu roleplaying game.

Author: Andrew C
Version: 1.0
Last Updated: 03/31/2025
"""

import os
from src.ui import menu

def main():
    """
    Main menu function that handles user interaction with the application.

    This function displays the main menu, handles user input, and
    calls the appropriate functions based on user selection.
    """
    menu()

if __name__ == "__main__":
    main()