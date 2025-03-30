"""
User Interface Module for Call of Cthulhu Character Viewer

This module handles all the user interface functionality including:
- Main menu and submenu display
- User input handling
- Character selection
- UI formatting and display

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import os
import sys
import json
from src.character_metadata import CharacterMetadata
from src.character_cache_core import CharacterCache
from src.character_cache_stats import get_cache_stats, clear_cache
from src.character_display import display_character
import constants


def get_user_selection(prompt, min_value, max_value):
    """
    Get a numeric selection from the user within a specified range.

    Args:
        prompt (str): Prompt to display to the user
        min_value (int): Minimum acceptable value
        max_value (int): Maximum acceptable value

    Returns:
        int: User's selection as an integer, or None if user provides invalid input
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
                print(f"Invalid selection. Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except EOFError:
            print("\nInput closed.")
            return None


def list_character_metadata():
    """
    List all character metadata from JSON files in the characters directory.

    Returns:
        list: List of CharacterMetadata objects
    """
    try:
        if not os.path.exists(constants.CHARACTERS_DIRECTORY):
            print("Error: Characters directory not found!")
            return []

        metadata_list = []
        with os.scandir(constants.CHARACTERS_DIRECTORY) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(constants.JSON_EXTENSION):
                    try:
                        metadata = CharacterMetadata(entry.path)
                        metadata_list.append(metadata)
                    except Exception as e:
                        print(f"Error processing {entry.name}: {e}")

        metadata_list.sort(key=lambda x: x.name)

        if not metadata_list:
            print("No valid character files found in the characters directory!")

        return metadata_list

    except PermissionError:
        print("Error: No permission to access files in the characters directory.")
        return []

    except Exception as e:
        print(f"Error listing character files: {e}")
        return []


def configure_cache_settings(cache):
    """
    Allow user to configure cache settings.

    Args:
        cache (CharacterCache): The character cache instance
    """
    print("\n=== Cache Configuration ===")
    stats = get_cache_stats(cache)
    print(f"Current maximum cache size: {stats[constants.STAT_MAX_SIZE]}")

    try:
        new_size = get_user_selection(
            constants.PROMPT_CACHE_SIZE,
            constants.CACHE_SIZE_CANCEL,
            constants.CACHE_SIZE_MAX
        )

        if new_size in (None, constants.CACHE_SIZE_CANCEL):
            print("Cache configuration canceled.")
            return

        new_cache = CharacterCache(max_size=new_size)

        for filename in stats[constants.STAT_FILES][-new_size:]:
            try:
                with open(filename, 'r', encoding=constants.DEFAULT_ENCODING) as f:
                    character_data = json.load(f)
                new_cache.put(filename, character_data)
            except Exception as e:
                print(f"Error re-adding {filename} to new cache: {e}")

        print(f"Maximum cache size updated to {new_size}.")

    except (ValueError, TypeError):
        print("Invalid input. Cache configuration canceled.")
    except Exception as e:
        print(f"Error configuring cache: {e}")


def display_cache_stats(cache):
    """
    Display statistics about the character cache.

    Args:
        cache (CharacterCache): The character cache instance
    """
    stats = get_cache_stats(cache)
    print("\n--- Cache Status ---")
    print(f"Characters in cache metadata: {stats[constants.STAT_SIZE]}")
    print(f"Active entries in cache: {stats[constants.STAT_ACTIVE_ENTRIES]}")
    print(f"Maximum cache size: {stats[constants.STAT_MAX_SIZE]}")
    print(f"Approximate memory usage: {stats[constants.STAT_MEMORY_USAGE]} bytes")

    total_accesses = stats.get(constants.STAT_HITS, 0) + stats.get(constants.STAT_MISSES, 0)
    if total_accesses > 0:
        print(f"Cache hit rate: {stats.get(constants.STAT_HIT_RATE, 0):.1f}% "
              f"({stats.get(constants.STAT_HITS, 0)} hits, {stats.get(constants.STAT_MISSES, 0)} misses)")

    if stats[constants.STAT_SIZE] > 0:
        print("\nCached characters:")
        for i, char_file in enumerate(stats[constants.STAT_FILES], 1):
            print(f"{i}. {char_file}")

        if constants.STAT_OLDEST_AGE in stats:
            print(f"\nOldest entry age: {stats[constants.STAT_OLDEST_AGE]:.1f} seconds")
            print(f"Newest entry age: {stats[constants.STAT_NEWEST_AGE]:.1f} seconds")
    else:
        print("\nNo characters in cache.")


def run_tests_menu(run_dice_parser_tests, run_character_metadata_tests, 
                   run_character_cache_tests, run_metadata_loading_tests):
    """
    Display and handle the submenu for running various tests.
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
            f"\nEnter your choice ({constants.MENU_OPTION_MIN}-{constants.TEST_MENU_OPTION_MAX}): ",
            constants.MENU_OPTION_MIN,
            constants.TEST_MENU_OPTION_MAX
        )

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
            input(f"\n{constants.PROMPT_PRESS_ENTER}")
        except (KeyboardInterrupt, EOFError):
            pass


def main_menu(load_character_from_json, run_dice_parser_tests, run_character_metadata_tests, 
              run_character_cache_tests, run_metadata_loading_tests):
    """
    Main menu function handling user interaction.
    """
    cache = CharacterCache(max_size=constants.DEFAULT_UI_CACHE_SIZE)

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
                f"\nEnter your choice ({constants.MENU_OPTION_MIN}-{constants.MAIN_MENU_OPTION_MAX}): ",
                constants.MENU_OPTION_MIN,
                constants.MAIN_MENU_OPTION_MAX
            )

            if choice is None:
                continue

            menu_actions = {
                1: lambda: handle_character_view(cache, load_character_from_json),
                2: lambda: clear_cache(cache),
                3: lambda: display_cache_stats(cache),
                4: lambda: run_tests_menu(run_dice_parser_tests, run_character_metadata_tests, 
                                          run_character_cache_tests, run_metadata_loading_tests),
                5: lambda: configure_cache_settings(cache),
                6: lambda: sys.exit("Exiting program. Goodbye!")
            }

            action = menu_actions.get(choice, lambda: None)
            action()

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 1

    return 0