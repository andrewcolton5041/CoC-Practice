"""
Call of Cthulhu Character Viewer

This is the main module for a Call of Cthulhu character management application.
It provides functionality to:
- Load premade characters from JSON files
- Display character information in a formatted way
- Navigate through a menu-based interface
- Run various test suites for validation

This application can be used by game masters and players to quickly access
character information for the Call of Cthulhu roleplaying game.

Author: Unknown
Version: 1.6.0
Last Updated: 2025-03-30
"""

import os
import json
import os.path
import sys
import unittest
from character_cache import CharacterCache
from character_metadata import CharacterMetadata


def validate_character_data(character_data):
    """
    Validate that character data contains all required fields.

    Args:
        character_data (dict): Character data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['name', 'attributes']
    return all(field in character_data for field in required_fields)


def load_character_from_json(filename, cache):
    """
    Load a premade character from a JSON file with intelligent caching.

    Checks if the character is already in the cache and if the file hasn't changed.

    Args:
        filename (str): Path to the JSON file containing character data
        cache (CharacterCache): Cache instance for storing character data

    Returns:
        dict: Dictionary containing the character data or None if file cannot be loaded

    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file cannot be accessed due to permissions
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        # Use the cache's load_character method to handle both cache retrieval and file loading
        character_data, status = cache.load_character(filename, validate_character_data)

        if status == "cache_hit":
            return character_data
        elif status == "loaded_from_file":
            return character_data
        elif status == "validation_failed":
            print(f"Error: Character data in '{filename}' is missing required fields.")
            return None
        elif status == "file_not_found":
            print(f"Error: File '{filename}' not found.")
            return None
        elif status == "invalid_json":
            print(f"Error: Invalid JSON format in '{filename}'.")
            return None
        else:
            print(f"Error loading character from '{filename}': {status}")
            return None

    except PermissionError:
        print(f"Error: No permission to access '{filename}'.")
        return None
    except OSError as e:
        print(f"Error accessing '{filename}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading character from '{filename}': {e}")
        return None


def display_character(character_data):
    """
    Display a character's sheet in a formatted way to the console.

    Prints all relevant character information including:
    - Basic info (name, age, occupation)
    - Attributes (STR, DEX, etc.)
    - Skills
    - Weapons
    - Backstory

    Args:
        character_data (dict): Dictionary containing the character data

    Returns:
        None
    """
    if not character_data:
        print("Error: No character data to display.")
        return

    # Print divider line and basic character information
    print("\n" + "=" * 50)
    print(f"Name: {character_data['name']}")
    print(f"Age: {character_data.get('age', 'Unknown')}")
    print(f"Occupation: {character_data.get('occupation', 'Unknown')}")
    print(f"Nationality: {character_data.get('nationality', 'Unknown')}")

    # Print character attributes
    print("\n--- Attributes ---")
    for attr, value in character_data.get('attributes', {}).items():
        print(f"{attr}: {value}")

    # Print character skills if available
    if 'skills' in character_data:
        print("\n--- Skills ---")
        for skill, value in character_data['skills'].items():
            print(f"{skill}: {value}")

    # Print character weapons if available
    if 'weapons' in character_data:
        print("\n--- Weapons ---")
        for weapon in character_data['weapons']:
            print(
                f"{weapon['name']} - Skill: {weapon['skill']} - Damage: {weapon['damage']}"
            )

    # Print character backstory if available
    if 'backstory' in character_data:
        print("\n--- Backstory ---")
        print(character_data['backstory'])

    # Print closing divider
    print("=" * 50 + "\n")


def list_character_metadata():
    """
    List all character metadata from JSON files in the characters directory.

    This is an optimized version that only loads minimal character information
    necessary for displaying the character selection list.

    Returns:
        list: List of CharacterMetadata objects, or empty list if directory not found
            or no character files exist
    """
    try:
        if not os.path.exists('characters'):
            print("Error: Characters directory not found!")
            return []

        # Load metadata for all character files
        metadata_list = CharacterMetadata.load_all_from_directory('characters')

        if not metadata_list:
            print("No character files found in the characters directory!")

        return metadata_list
    except PermissionError:
        print("Error: No permission to access the characters directory.")
        return []
    except Exception as e:
        print(f"Error listing character files: {e}")
        return []


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


def display_cache_stats(cache):
    """
    Display statistics about the character cache.

    Args:
        cache (CharacterCache): The character cache instance

    Returns:
        None
    """
    stats = cache.get_stats()
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


def run_tests_menu():
    """
    Display and handle the submenu for running various tests.

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


def run_dice_parser_tests():
    """
    Run the dice parser test suite.

    This function loads and executes the tests defined in test_dice_parser.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Dice Parser Tests ===\n")

    try:
        # Check if the test file exists
        if not os.path.exists('test_dice_parser.py'):
            print("Error: test_dice_parser.py not found!")
            return False

        # Import the test module
        try:
            import test_dice_parser
        except ImportError:
            print("Error: Failed to import test_dice_parser module.")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_dice_parser)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running dice parser tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_character_metadata_tests():
    """
    Run the character metadata test suite.

    This function loads and executes the tests defined in test_character_metadata.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Character Metadata Tests ===\n")

    try:
        # Check if the test file exists
        if not os.path.exists('test_character_metadata.py'):
            print("Error: test_character_metadata.py not found!")
            return False

        # Import the test module
        try:
            import test_character_metadata
        except ImportError:
            print("Error: Failed to import test_character_metadata module.")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_character_metadata)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running character metadata tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_character_cache_tests():
    """
    Run the character cache test suite.

    This function loads and executes the tests defined in test_character_cache.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Character Cache Tests ===\n")

    try:
        # Check if the test file exists
        if not os.path.exists('test_character_cache.py'):
            print("Error: test_character_cache.py not found!")
            return False

        # Import the test module
        try:
            import test_character_cache
        except ImportError:
            print("Error: Failed to import test_character_cache module.")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_character_cache)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running character cache tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_metadata_loading_tests():
    """
    Run the optimized metadata loading test suite.

    This function loads and executes the tests defined in test_metadata_loading.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Optimized Metadata Loading Tests ===\n")

    try:
        # Check if the test file exists
        if not os.path.exists('test_metadata_loading.py'):
            print("Error: test_metadata_loading.py not found!")
            return False

        # Import the test module
        try:
            import test_metadata_loading
        except ImportError:
            print("Error: Failed to import test_metadata_loading module.")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_metadata_loading)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running optimized metadata loading tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def main():
    """
    Main menu function that handles user interaction with the application.

    This function displays the main menu, handles user input, and
    calls the appropriate functions based on user selection.
    Implements character caching for improved performance.

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
                cache.invalidate()
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
                run_tests_menu()

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


def configure_cache_settings(cache):
    """
    Allow user to configure cache settings.

    Args:
        cache (CharacterCache): The character cache instance

    Returns:
        None
    """
    print("\n=== Cache Configuration ===")
    print(f"Current maximum cache size: {cache._max_size}")

    # Get new cache size from user
    try:
        new_size = get_user_selection("Enter new maximum cache size (3-50, or 0 to cancel): ", 0, 50)

        if new_size is None or new_size == 0:
            print("Cache configuration canceled.")
            return

        # Update cache size
        cache._max_size = new_size
        print(f"Maximum cache size updated to {new_size}.")

        # Note: We may need to enforce the new limit by clearing excess entries
        current_size = len(cache._metadata)
        if current_size > new_size:
            # Remove oldest entries to meet new size
            excess = current_size - new_size
            for _ in range(excess):
                if cache._metadata:
                    # Remove least recently used item (first item in OrderedDict)
                    cache._metadata.popitem(last=False)

            print(f"Removed {excess} least recently used entries to meet new cache size limit.")

    except (ValueError, TypeError):
        print("Invalid input. Cache configuration canceled.")
    except Exception as e:
        print(f"Error configuring cache: {e}")                                                                                                                            


if __name__ == "__main__":
    sys.exit(main())