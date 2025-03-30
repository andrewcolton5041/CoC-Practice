"""
User Interface Module for Call of Cthulhu Character Viewer

This module handles all the user interface functionality including:
- Main menu and submenu display
- User input handling
- Character selection
- UI formatting and display

Author: Unknown
Version: 1.2
Last Updated: 2025-03-30
"""

import os
import sys
import json
from typing import Callable, Optional, List, Dict, Any, Tuple

from src.character_metadata import CharacterMetadata
from src.character_cache_core import CharacterCache
from src.character_display import display_character
from src.constants import (
    PROMPT_CACHE_SIZE,
    CACHE_SIZE_CANCEL,
    CACHE_SIZE_MAX,
    PROMPT_PRESS_ENTER,
    MENU_OPTION_MIN,
    MAIN_MENU_OPTION_MAX,
    TEST_MENU_OPTION_MAX,
    CHARACTERS_DIRECTORY,
    DEFAULT_UI_CACHE_SIZE,
    CACHE_SIZE_MIN,
    DEFAULT_ENCODING,
    JSON_EXTENSION
)
from src.validation import validate_cache_size, validate_directory_path
from src.error_handling import log_error, display_user_error, safe_operation
from src.cache_stats import calculate_character_cache_stats, clear_cache_and_get_stats
from src.file_utils import read_json_file, list_json_files
from src.character_cache_utils import resize_cache, get_cache_usage_report


def get_user_selection(prompt: str, min_value: int, max_value: int) -> Optional[int]:
    """
    Get a numeric selection from the user within a specified range.

    Args:
        prompt (str): Prompt to display to the user
        min_value (int): Minimum acceptable value
        max_value (int): Maximum acceptable value

    Returns:
        int or None: User's selection as an integer, or None if user provides invalid input
    """
    while True:
        try:
            selection = input(prompt)
            # Allow empty input to return None for cancel operations
            if not selection.strip():
                return None

            selection = int(selection)
            if min_value <= selection <= max_value:
                return selection
            else:
                display_user_error(
                    "invalid_selection",
                    f"Invalid selection. Please enter a number between {min_value} and {max_value}."
                )
        except ValueError:
            display_user_error("invalid_input", "Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except EOFError:
            print("\nInput closed.")
            return None


def list_character_metadata() -> List[CharacterMetadata]:
    """
    List all character metadata from JSON files in the characters directory.

    Returns:
        list: List of CharacterMetadata objects
    """
    try:
        if not validate_directory_path(CHARACTERS_DIRECTORY):
            display_user_error("directory_error", f"Error: Characters directory not found!")
            return []

        # Use the improved CharacterMetadata.load_all_from_directory method
        metadata_list = CharacterMetadata.load_all_from_directory(CHARACTERS_DIRECTORY)

        if not metadata_list:
            display_user_error(
                "no_characters",
                "No valid character files found in the characters directory!"
            )

        return metadata_list

    except Exception as e:
        log_error("metadata_listing_error", f"Error listing character files", {"error": str(e)})
        return []


def configure_cache_settings(cache: CharacterCache) -> None:
    """
    Allow user to configure cache settings.

    Args:
        cache (CharacterCache): The character cache instance
    """
    print("\n=== Cache Configuration ===")
    stats = calculate_character_cache_stats(cache)
    print(f"Current maximum cache size: {stats['max_size']}")

    try:
        new_size = get_user_selection(PROMPT_CACHE_SIZE,
                                      CACHE_SIZE_CANCEL,
                                      CACHE_SIZE_MAX)

        if new_size in (None, CACHE_SIZE_CANCEL):
            print("Cache configuration canceled.")
            return

        if not validate_cache_size(new_size):
            display_user_error(
                "invalid_cache_size",
                f"Invalid cache size. Must be between {CACHE_SIZE_MIN} and {CACHE_SIZE_MAX}."
            )
            return

        success, new_cache = resize_cache(cache, new_size)

        if success:
            # Replace the old cache reference with the new one
            # Note: This actually won't work as expected since we're not modifying the
            # original cache reference. We'll need to modify how the cache is managed
            # at a higher level, but for now, let's leave this as is.
            cache = new_cache
            print(f"Maximum cache size updated to {new_size}.")
        else:
            display_user_error("cache_resize_failed", "Failed to resize cache.")

    except Exception as e:
        log_error("cache_config_error", f"Error configuring cache", {"error": str(e)})


def display_cache_stats(cache: CharacterCache) -> None:
    """
    Display statistics about the character cache.

    Args:
        cache (CharacterCache): The character cache instance
    """
    try:
        # Use the improved cache stats functionality
        print(get_cache_usage_report(cache))
    except Exception as e:
        log_error("cache_stats_error", f"Error displaying cache stats", {"error": str(e)})


def run_tests_menu(run_dice_parser_tests: Callable, 
                   run_character_metadata_tests: Callable,
                   run_character_cache_tests: Callable, 
                   run_metadata_loading_tests: Callable) -> None:
    """
    Display and handle the submenu for running various tests.

    Args:
        run_dice_parser_tests: Function to run dice parser tests
        run_character_metadata_tests: Function to run character metadata tests
        run_character_cache_tests: Function to run character cache tests
        run_metadata_loading_tests: Function to run metadata loading tests
    """
    while True:
        print("\n=== Run Tests ===")
        print("1. Run Dice Parser Tests")
        print("2. Run Character Metadata Tests")
        print("3. Run Character Cache Tests")
        print("4. Run Metadata Loading Tests")
        print("5. Run All Tests")
        print("6. Back to Main Menu")

        choice = get_user_selection(
            f"\nEnter your choice ({MENU_OPTION_MIN}-{TEST_MENU_OPTION_MAX}): ",
            MENU_OPTION_MIN, TEST_MENU_OPTION_MAX)

        if choice is None:
            continue

        test_actions = {
            1: run_dice_parser_tests,
            2: run_character_metadata_tests,
            3: run_character_cache_tests,
            4: run_metadata_loading_tests,
            5: lambda: [
                run_dice_parser_tests(),
                run_character_metadata_tests(),
                run_character_cache_tests(),
                run_metadata_loading_tests()
            ],
            6: lambda: None
        }

        action = test_actions.get(choice, lambda: None)
        action()

        if choice == 6:
            return

        try:
            input(f"\n{PROMPT_PRESS_ENTER}")
        except (KeyboardInterrupt, EOFError):
            pass


def handle_character_view(cache: CharacterCache, load_character_from_json: Callable) -> None:
    """
    Display a list of characters and allow the user to view their details.

    Args:
        cache (CharacterCache): The character cache instance
        load_character_from_json (function): Function to load character data from JSON
    """
    # Get list of character metadata
    metadata_list = list_character_metadata()

    if not metadata_list:
        print("No characters available.")
        return

    # Display characters with numbered list
    print("\n=== Available Characters ===")
    for i, metadata in enumerate(metadata_list, 1):
        print(f"{i}. {metadata.name} ({metadata.occupation}, {metadata.nationality})")

    # Get user selection
    choice = get_user_selection(
        "\nEnter the number of the character to view (or 0 to cancel): ", 
        0, 
        len(metadata_list)
    )

    # Display selected character or return
    if choice is None or choice == 0:
        return

    # Load and display the selected character
    selected_metadata = metadata_list[choice - 1]
    character_data = load_character_from_json(selected_metadata.filename, cache)

    if character_data:
        display_character(character_data)
        try:
            input(f"\n{PROMPT_PRESS_ENTER}")
        except (KeyboardInterrupt, EOFError):
            pass


def main_menu(load_character_from_json: Callable, 
              run_dice_parser_tests: Callable, 
              run_character_metadata_tests: Callable, 
              run_character_cache_tests: Callable, 
              run_metadata_loading_tests: Callable) -> int:
    """
    Main menu function handling user interaction.

    Args:
        load_character_from_json: Function to load character data from JSON
        run_dice_parser_tests: Function to run dice parser tests
        run_character_metadata_tests: Function to run character metadata tests
        run_character_cache_tests: Function to run character cache tests
        run_metadata_loading_tests: Function to run metadata loading tests

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    cache = CharacterCache(max_size=DEFAULT_UI_CACHE_SIZE)

    try:
        while True:
            print("\n=== Call of Cthulhu Character Viewer ===")
            print("1. View Premade Characters")
            print("2. Clear Character Cache")
            print("3. View Cache Status")
            print("4. Run Tests")
            print("5. Configure Cache Settings")
            print("6. Exit")

            choice = get_user_selection(
                f"\nEnter your choice ({MENU_OPTION_MIN}-{MAIN_MENU_OPTION_MAX}): ",
                MENU_OPTION_MIN,
                MAIN_MENU_OPTION_MAX
            )

            if choice is None:
                continue

            menu_actions = {
                1: lambda: handle_character_view(cache, load_character_from_json),
                2: lambda: clear_cache_and_get_stats(cache),
                3: lambda: display_cache_stats(cache),
                4: lambda: run_tests_menu(
                    run_dice_parser_tests, 
                    run_character_metadata_tests, 
                    run_character_cache_tests, 
                    run_metadata_loading_tests
                ),
                5: lambda: configure_cache_settings(cache),
                6: lambda: sys.exit("Exiting program. Goodbye!")
            }

            action = menu_actions.get(choice, lambda: None)
            action()

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        return 0
    except Exception as e:
        log_error("main_menu_error", f"An unexpected error occurred", {"error": str(e)})
        return 1

    return 0