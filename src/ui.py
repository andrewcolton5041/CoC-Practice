import os
from src.json_reader import display_character, load_character_from_json
from src.constants import MenuStrings, FileExtensions, ErrorMessages, Extra

def menu():
  while True:
    # Display main menu
    print(MenuStrings.MAIN_MENU_TITLE)
    print(MenuStrings.MAIN_MENU_OPTION_1)
    print(MenuStrings.MAIN_MENU_OPTION_2)

    # Get user choice
    choice = input(MenuStrings.MAIN_MENU_CHOICE_PROMPT)

    if choice == MenuStrings.ChoiceNumEnum.OPTION_1.value:
        # Try to list character files from the characters directory
        character_files = []
        try:
            character_files = [f for f in os.listdir(MenuStrings.CharacterViewerStrings.CHARACTERS) if f.endswith(FileExtensions.JSON_FILE.value)]
        except FileNotFoundError:
            print(ErrorMessages.CHARACTER_FILE_NOT_FOUND)
            continue

        # Check if any character files were found
        if not character_files:
            print(ErrorMessages.NO_CHARACTER_FILES)
            continue

        # Display list of available characters
        print(MenuStrings.CharacterViewerStrings.CHARACTER_VIEWER_TITLE)
        for i, filename in enumerate(character_files, MenuStrings.STARTING_NUMBER):
            # Format the name nicely by removing the file extension
            name = filename.replace(FileExtensions.JSON_FILE.value, Extra.NO_CHARACTER).capitalize()
            print(MenuStrings.CharacterViewerStrings.available_characters(i, name))

        # Add option to return to main menu
        print(MenuStrings.CharacterViewerStrings.character_to_main(len(character_files) + MenuStrings.STARTING_NUMBER))

        # Let user select a character
        while True:
            try:
                selection = int(input(MenuStrings.CharacterViewerStrings.character_viewer_prompt(len(character_files) + MenuStrings.STARTING_NUMBER)))

                # Handle valid character selection
                if MenuStrings.STARTING_NUMBER <= selection <= len(character_files):
                    # Load and display the selected character
                    filename = os.path.join(MenuStrings.CharacterViewerStrings.CHARACTERS, character_files[selection - MenuStrings.STARTING_NUMBER])
                    character_data = load_character_from_json(filename)
                    display_character(character_data)

                    # Wait for user to press Enter before returning to menu
                    input(MenuStrings.CharacterViewerStrings.INPUT_ENTER_KEY)
                    break
                # Handle return to main menu
                elif selection == len(character_files) + MenuStrings.STARTING_NUMBER:
                    break
                else:
                    print(MenuStrings.INVALID_CHOICE_ERROR)
            except ValueError:
                print(ErrorMessages.INVALID_CHOICE_REDO)

    elif choice == MenuStrings.ChoiceNumEnum.OPTION_2.value:
        # Exit the application
        print(MenuStrings.EXIT_MESSAGE)
        break

    else:
        # Handle invalid main menu choice
        print(MenuStrings.INVALID_CHOICE_ERROR)