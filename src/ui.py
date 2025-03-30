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

    This is an optimized version using os.scandir() for efficient directory traversal.

    Returns:
        list: List of CharacterMetadata objects, or empty list if directory not found
            or no character files exist
    """
    try:
        # Check if characters directory exists
        if not os.path.exists('characters'):
            print("Error: Characters directory not found!")
            return []

        # Use os.scandir() for efficient directory iteration
        metadata_list = []
        try:
            with os.scandir('characters') as entries:
                for entry in entries:
                    # Check if it's a file and has .json extension
                    if entry.is_file() and entry.name.endswith('.json'):
                        try:
                            # Create metadata object for the file
                            metadata = CharacterMetadata(entry.path)
                            metadata_list.append(metadata)
                        except Exception as e:
                            # Log any individual file processing errors without stopping entire process
                            print(f"Error processing {entry.name}: {e}")

            # Sort metadata alphabetically by name for consistent display
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

    Returns:
        None
    """
    print("\n=== Cache Configuration ===")
    stats = get_cache_stats(cache)
    print(f"Current maximum cache size: {stats['max_size']}")

    # Get new cache size from user
    try:
        new_size = get_user_selection("Enter new maximum cache size (3-50, or 0 to cancel): ", 0, 50)

        if new_size is None or new_size == 0:
            print("Cache configuration canceled.")
            return

        # Create a new cache with the updated size
        # Effectively reset the cache to the new size
        new_cache = CharacterCache(max_size=new_size)

        # Copy over the most recently used entries that fit within the new size
        for filename in stats['files'][-new_size:]:
            try:
                # Re-add the most recently used entries
                with open(filename, 'r', encoding='utf-8') as f:
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

    Returns:
        None
    """
    stats = get_cache_stats(cache)
    print("\n--- Cache Status ---")
    print(f"Characters in cache metadata: {stats['size']}")
    print(f"Active entries in cache: {stats['active_entries']}")
    print(f"Maximum cache size: {stats['max_size']}")
    print(f"Approximate memory usage: {stats['memory_usage']} bytes")

    # Display hit rate statistics
    total_accesses = stats.get('hits', 0) + stats.get('misses', 0)
    if total_accesses > 0:
        print(f"Cache hit rate: {stats.get('hit_rate', 0):.1f}% ({stats.get('hits', 0)} hits, {stats.get('misses', 0)} misses)")

    if stats['size'] > 0:
        print("\nCached characters:")
        for i, char_file in enumerate(stats['files'], 1):
            print(f"{i}. {char_file}")

        if 'oldest_entry_age' in stats:
            print(f"\nOldest entry age: {stats['oldest_entry_age']:.1f} seconds")
            print(f"Newest entry age: {stats['newest_entry_age']:.1f} seconds")
    else:
        print("\nNo characters in cache.")


def run_tests_menu(run_dice_parser_tests, run_character_metadata_tests, 
                  run_character_cache_tests, run_metadata_loading_tests):
    """
    Display and handle the submenu for running various tests.

    Args:
        run_dice_parser_tests (function): Function to run dice parser tests
        run_character_metadata_tests (function): Function to run character metadata tests
        run_character_cache_tests (function): Function to run character cache tests
        run_metadata_loading_tests (function): Function to run metadata loading tests

    Returns:
        None
    """
    while True:
        # Display test menu
        print("\n=== Run Tests ===")
        print("1. Run Dice Parser Tests")
        print("2. Run Character Metadata Tests")
        print("3. Run Character Cache Tests")
        print("4. Run Metadata Loading Tests")
        print("5. Run All Tests")
        print("6. Back to Main Menu")

        # Get user choice
        choice = get_user_selection("\nEnter your choice (1-6): ", 1, 6)

        # Handle canceled selection
        if choice is None:
            continue

        if choice == 1:
            # Run dice parser tests
            run_dice_parser_tests()
        elif choice == 2:
            # Run character metadata tests
            run_character_metadata_tests()
        elif choice == 3:
            # Run character cache tests
            run_character_cache_tests()
        elif choice == 4:
            # Run optimized metadata loading tests
            run_metadata_loading_tests()
        elif choice == 5:
            # Run all tests
            print("\n=== Running All Tests ===\n")
            run_dice_parser_tests()
            run_character_metadata_tests()
            run_character_cache_tests()
            run_metadata_loading_tests()
        elif choice == 6:
            # Return to main menu
            return

        # Wait for user to press Enter before continuing
        try:
            input("\nPress Enter to continue...")
        except (KeyboardInterrupt, EOFError):
            pass


def main_menu(load_character_from_json, run_dice_parser_tests, run_character_metadata_tests, 
             run_character_cache_tests, run_metadata_loading_tests):
    """
    Main menu function that handles user interaction with the application.

    This function displays the main menu, handles user input, and
    calls the appropriate functions based on user selection.
    Implements character caching for improved performance.

    Args:
        load_character_from_json (function): Function to load character from JSON
        run_dice_parser_tests (function): Function to run dice parser tests
        run_character_metadata_tests (function): Function to run character metadata tests
        run_character_cache_tests (function): Function to run character cache tests
        run_metadata_loading_tests (function): Function to run metadata loading tests

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    # Initialize the character cache with a sensible maximum size
    cache = CharacterCache(max_size=10)

    try:
        while True:
            # Display main menu
            print("\n=== Call of Cthulhu Character Viewer ===")
            print("1. View Premade Characters")
            print("2. Clear Character Cache")
            print("3. View Cache Status")
            print("4. Run Tests")
            print("5. Configure Cache Settings")
            print("6. Exit")

            # Get user choice
            choice = get_user_selection("\nEnter your choice (1-6): ", 1, 6)

            # Handle canceled selection
            if choice is None:
                continue

            if choice == 1:
                # List character metadata - LAZY LOADING OPTIMIZATION
                character_metadata = list_character_metadata()
                if not character_metadata:
                    continue

                # Display list of available characters with basic info
                print("\n--- Available Characters ---")
                for i, metadata in enumerate(character_metadata, 1):
                    # Only use metadata for display without loading full character data
                    print(f"{i}. {metadata.name} - {metadata.occupation} ({metadata.nationality})")

                # Add option to return to main menu
                print(f"{len(character_metadata) + 1}. Back to Main Menu")

                # Let user select a character
                selection = get_user_selection(
                    f"\nSelect a character (1-{len(character_metadata) + 1}): ", 
                    1, 
                    len(character_metadata) + 1
                )

                # Handle canceled selection
                if selection is None:
                    continue

                # Handle valid character selection
                if 1 <= selection <= len(character_metadata):
                    # Only load the full character data when explicitly viewing a character
                    selected_metadata = character_metadata[selection - 1]
                    try:
                        print(f"\nLoading character: {selected_metadata.name}...")
                        # Load full character data from cache or file only at this point
                        character_data = load_character_from_json(selected_metadata.filename, cache)
                        if character_data:  # Check if load was successful
                            display_character(character_data)
                        else:
                            print(f"Failed to load full character data for {selected_metadata.name}.")
                    except Exception as e:
                        print(f"Error loading character: {e}")

                    # Wait for user to press Enter before returning to menu
                    try:
                        input("Press Enter to continue...")
                    except (KeyboardInterrupt, EOFError):
                        pass

            elif choice == 2:
                # Clear the character cache
                clear_cache(cache)
                print("Character cache cleared successfully.")

            elif choice == 3:
                # Display cache status
                display_cache_stats(cache)

                # Wait for user to press Enter before returning to menu
                try:
                    input("\nPress Enter to continue...")
                except (KeyboardInterrupt, EOFError):
                    pass

            elif choice == 4:
                # Display the tests submenu
                run_tests_menu(run_dice_parser_tests, run_character_metadata_tests, 
                              run_character_cache_tests, run_metadata_loading_tests)

            elif choice == 5:
                # Configure cache settings
                configure_cache_settings(cache)

            elif choice == 6:
                # Exit the application
                print("Exiting program. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 1

    return 0