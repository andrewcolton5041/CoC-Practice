import subprocess
from src.constants import UIStrings, ErrorMessages


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
        print("Not implemented yet")
      elif selection == "2":
        #run_specific_test(TestConstants.DICE_ROLL_TEST)
        print("Not implemented yet")
      elif selection == "3":
        #run_specific_test(TestConstants.COC_RULES_TEST)
        print("Not implemented yet")
      elif selection == "4":
        #run_specific_test(TestConstants.JSON_READER_TEST)
        print("Not implemented yet")
      elif selection == "5":
        #run_specific_test(TestConstants.UI_TEST)
        print("Not implemented yet")
      elif selection == "6":
        #run_all_tests()
        print("Not implemented yet")
      elif selection == "7":
        # Return to main menu
        break
      else:
        print(UIStrings.MainMenu.INVALID_CHOICE)

    except ValueError:
      print(ErrorMessages.INVALID_CHOICE)


def run_character_utils_test():
  return
