"""
Test Runner Module

Provides functionality to run tests for different modules 
in the Call of Cthulhu text adventure game.

Author: Andrew C
Version: 1.1
Last Updated: 3/31/2025
"""

import subprocess
import os
from src.constants import (
    UIStrings, 
    ErrorMessages, 
    TestConstants
)


def test_menu():
    """
    Display and handle the test menu.

    Presents options to run individual tests, all tests, or return to main menu.
    """
    while True:
        # Display test menu
        print(UIStrings.TestMenu.TITLE)
        print(UIStrings.TestMenu.OPTION_CHARACTER_UTILS_TEST)
        print(UIStrings.TestMenu.OPTION_DICE_ROLL_TEST)
        print(UIStrings.TestMenu.OPTION_COC_RULES_TEST)
        print(UIStrings.TestMenu.OPTION_JSON_READER_TEST)
        print(UIStrings.TestMenu.OPTION_UI_TEST)
        print(UIStrings.TestMenu.OPTION_DEVELOPMENT_PHASE_TESTS)
        print(UIStrings.TestMenu.OPTION_RUN_ALL_TESTS)
        print(UIStrings.TestMenu.OPTION_RETURN_TO_MAIN)

        # Get user choice
        try:
            selection = input(UIStrings.TestMenu.PROMPT)

            # Handle user selection
            if selection == "1":
                run_character_utils_test()
            elif selection == "2":
                run_dice_roll_test()
            elif selection == "3":
                run_coc_rules_test()
            elif selection == "4":
                run_json_reader_test()
            elif selection == "5":
                run_ui_test()
            elif selection == "6":
                run_test(TestConstants.INVESTIGATOR_DEVELOPMENT_TEST, "Investigator Development")
            elif selection == "7":
                run_all_tests()
            elif selection == "8":
                # Return to main menu
                break
            else:
                print(UIStrings.MainMenu.INVALID_CHOICE)

        except ValueError:
            print(ErrorMessages.INVALID_CHOICE)


def run_character_utils_test():
    """
    Run the character utils tests using pytest.

    This function uses subprocess to run pytest against the test_character_utils.py file,
    displays the results to the user, and writes them to a 'Test Results.txt' file.
    """
    print("\nRunning Character Utils Tests...\n")

    try:
        # Run pytest for the character_utils test file
        result = subprocess.run(
            ["pytest", TestConstants.CHARACTER_UTILS_TEST, TestConstants.PYTEST_VERBOSE_FLAG],
            capture_output=True,
            text=True
        )

        # Print the output from pytest to the console
        if result.stdout:
            print(result.stdout)

        # Print any errors to the console
        if result.stderr:
            print(result.stderr)

        # Write results to a file (overwriting any existing file)
        with open(TestConstants.TEST_RESULTS_FILE, 'w') as file:
            file.write("=== Character Utils Test Results ===\n\n")

            # Write stdout
            if result.stdout:
                file.write(result.stdout)

            # Write stderr if there were any errors
            if result.stderr:
                file.write("\n=== ERRORS ===\n")
                file.write(result.stderr)

            # Write summary
            if result.returncode == 0:
                file.write("\n" + UIStrings.TestMenu.TEST_SUCCESS)
            else:
                file.write("\n" + UIStrings.TestMenu.TEST_FAILURE)

        # Check if tests passed successfully
        if result.returncode == 0:
            print(UIStrings.TestMenu.TEST_SUCCESS)
        else:
            print(UIStrings.TestMenu.TEST_FAILURE)

        print(f"\nTest results have been saved to '{TestConstants.TEST_RESULTS_FILE}'")

    except Exception as e:
        # Handle any exceptions that occur while running the tests
        error_message = f"Error running tests: {str(e)}"
        print(error_message)
        print(UIStrings.TestMenu.TEST_ERROR)

        # Write error to file
        with open(TestConstants.TEST_RESULTS_FILE, 'w') as file:
            file.write("=== Character Utils Test Results ===\n\n")
            file.write(error_message + "\n")
            file.write(UIStrings.TestMenu.TEST_ERROR)


def run_dice_roll_test():
    """
    Run the dice roll tests using pytest.
    """
    print("\nRunning Dice Roll Tests...\n")
    run_test(TestConstants.DICE_ROLL_TEST, "Dice Roll")


def run_coc_rules_test():
    """
    Run the CoC rules tests using pytest.
    """
    print("\nRunning CoC Rules Tests...\n")
    run_test(TestConstants.COC_RULES_TEST, "CoC Rules")


def run_json_reader_test():
    """
    Run the JSON reader tests using pytest.
    """
    print("\nRunning JSON Reader Tests...\n")
    run_test(TestConstants.JSON_READER_TEST, "JSON Reader")


def run_ui_test():
    """
    Run the UI tests using pytest.
    """
    print("\nRunning UI Tests...\n")
    run_test(TestConstants.UI_TEST, "UI")


def run_all_tests():
    """
    Run all available tests using pytest.
    """
    print(UIStrings.TestMenu.ALL_TESTS_RUNNING)

    test_files = [
        TestConstants.CHARACTER_UTILS_TEST,
        TestConstants.DICE_ROLL_TEST,
        TestConstants.COC_RULES_TEST,
        TestConstants.JSON_READER_TEST,
        TestConstants.UI_TEST,
        TestConstants.INVESTIGATOR_DEVELOPMENT_TEST
    ]

    # Create a list of test files that actually exist
    existing_test_files = [f for f in test_files if os.path.exists(f)]

    if not existing_test_files:
        print(UIStrings.TestMenu.NO_TESTS_FOUND)
        return

    try:
        # Run pytest for all test files
        result = subprocess.run(
            ["pytest"] + existing_test_files + [TestConstants.PYTEST_VERBOSE_FLAG],
            capture_output=True,
            text=True
        )

        # Print the output from pytest to the console
        if result.stdout:
            print(result.stdout)

        # Print any errors to the console
        if result.stderr:
            print(result.stderr)

        # Write results to a file
        with open(TestConstants.TEST_RESULTS_FILE, 'w') as file:
            file.write("=== All Tests Results ===\n\n")

            # Write stdout
            if result.stdout:
                file.write(result.stdout)

            # Write stderr if there were any errors
            if result.stderr:
                file.write("\n=== ERRORS ===\n")
                file.write(result.stderr)

            # Write summary
            if result.returncode == 0:
                file.write("\n" + UIStrings.TestMenu.ALL_TESTS_SUCCESS)
            else:
                file.write("\n" + UIStrings.TestMenu.SOME_TESTS_SUCCESS)

        # Check if tests passed successfully
        if result.returncode == 0:
            print(UIStrings.TestMenu.ALL_TESTS_SUCCESS)
        else:
            print(UIStrings.TestMenu.SOME_TESTS_SUCCESS)

        print(f"\nTest results have been saved to '{TestConstants.TEST_RESULTS_FILE}'")

    except Exception as e:
        # Handle any exceptions that occur while running the tests
        error_message = f"Error running tests: {str(e)}"
        print(error_message)
        print(UIStrings.TestMenu.TEST_ERROR)

        # Write error to file
        with open(TestConstants.TEST_RESULTS_FILE, 'w') as file:
            file.write("=== All Tests Results ===\n\n")
            file.write(error_message + "\n")
            file.write(UIStrings.TestMenu.TEST_ERROR)


def run_test(test_file, test_name):
    """
    Generic function to run a specific test file using pytest.

    Args:
        test_file (str): Path to the test file
        test_name (str): Name of the test for display purposes
    """
    try:
        # Check if the test file exists
        if not os.path.exists(test_file):
            print(f"Test file '{test_file}' does not exist.")
            return

        # Run pytest for the test file
        result = subprocess.run(
            ["pytest", test_file, TestConstants.PYTEST_VERBOSE_FLAG],
            capture_output=True,
            text=True
        )

        # Print the output from pytest to the console
        if result.stdout:
            print(result.stdout)

        # Print any errors to the console
        if result.stderr:
            print(result.stderr)

        # Write results to a file
        with open(TestConstants.TEST_RESULTS_FILE, 'w') as file:
            file.write(f"=== {test_name} Test Results ===\n\n")

            # Write stdout
            if result.stdout:
                file.write(result.stdout)

            # Write stderr if there were any errors
            if result.stderr:
                file.write("\n=== ERRORS ===\n")
                file.write(result.stderr)

            # Write summary
            if result.returncode == 0:
                file.write("\n" + UIStrings.TestMenu.TEST_SUCCESS)
            else:
                file.write("\n" + UIStrings.TestMenu.TEST_FAILURE)

        # Check if tests passed successfully
        if result.returncode == 0:
            print(UIStrings.TestMenu.TEST_SUCCESS)
        else:
            print(UIStrings.TestMenu.TEST_FAILURE)

        print(f"\nTest results have been saved to '{TestConstants.TEST_RESULTS_FILE}'")

    except Exception as e:
        # Handle any exceptions that occur while running the tests
        error_message = f"Error running tests: {str(e)}"
        print(error_message)
        print(UIStrings.TestMenu.TEST_ERROR)

        # Write error to file
        with open(TestConstants.TEST_RESULTS_FILE, 'w') as file:
            file.write(f"=== {test_name} Test Results ===\n\n")
            file.write(error_message + "\n")
            file.write(UIStrings.TestMenu.TEST_ERROR)