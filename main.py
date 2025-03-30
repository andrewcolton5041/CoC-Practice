"""
Call of Cthulhu Character Viewer

This is the main module for a Call of Cthulhu character management application.
It serves as the entry point and coordinates between the various modules:
- UI (user interface)
- Character loading
- Character display
- Test execution

This application can be used by game masters and players to quickly access
character information for the Call of Cthulhu roleplaying game.

Author: Unknown
Version: 2.0.0
Last Updated: 2025-03-30
"""

import sys
from src.ui import main_menu
from src.character_loader import load_character_from_json
from src.character_cache_core import CharacterCache
from src.test_runner import (
    run_dice_parser_tests,
    run_character_metadata_tests,
    run_character_cache_tests,
    run_metadata_loading_tests
)


def main():
    """
    Main function that serves as the entry point for the application.

    This function initializes the application and starts the main menu,
    passing in the required functions from other modules.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        # Start the main menu, passing in required functions from other modules
        exit_code = main_menu(
            load_character_from_json,
            run_dice_parser_tests,
            run_character_metadata_tests,
            run_character_cache_tests,
            run_metadata_loading_tests
        )
        return exit_code
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        return 0
    except Exception as e:
        print(f"\nAn unexpected error occurred in the main program: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())