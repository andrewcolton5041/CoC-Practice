import subprocess
import os
from src.constants import UIStrings, ErrorMessages, TestConstants


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
        print(UIStrings.TestMenu.OPTION_RUN_ALL_TESTS)
        print(UIStrings.TestMenu.OPTION_RETURN_TO_MAIN)

        # Get user choice
        try:
            selection = input(UIStrings.TestMenu.PROMPT)

            # Handle user selection
            if selection == "1":
                run_character_utils_test()
            elif selection == "2":
                print("Not implemented yet")
            elif selection == "3":
                print("Not implemented yet")
            elif selection == "4":
                print("Not implemented yet")
            elif selection == "5":
                print("Not implemented yet")
            elif selection == "6":
                print("Not implemented yet")
            elif selection == "7":
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