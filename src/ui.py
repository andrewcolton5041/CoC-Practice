import os
from src.json_reader import display_character, load_character_from_json

def menu():
  while True:
    # Display main menu
    print("\n=== Call of Cthulhu Character Viewer ===")
    print("1. View Premade Characters")
    print("2. Exit")

    # Get user choice
    choice = input("\nEnter your choice (1-2): ")

    if choice == '1':
        # Try to list character files from the characters directory
        character_files = []
        try:
            character_files = [f for f in os.listdir('characters') if f.endswith('.json')]
        except FileNotFoundError:
            print("Characters directory not found!")
            continue

        # Check if any character files were found
        if not character_files:
            print("No character files found!")
            continue

        # Display list of available characters
        print("\n--- Available Characters ---")
        for i, filename in enumerate(character_files, 1):
            # Format the name nicely by removing the file extension
            name = filename.replace('.json', '').capitalize()
            print(f"{i}. {name}")

        # Add option to return to main menu
        print(f"{len(character_files) + 1}. Back to Main Menu")

        # Let user select a character
        while True:
            try:
                selection = int(input(f"\nSelect a character (1-{len(character_files) + 1}): "))

                # Handle valid character selection
                if 1 <= selection <= len(character_files):
                    # Load and display the selected character
                    filename = os.path.join('characters', character_files[selection - 1])
                    character_data = load_character_from_json(filename)
                    display_character(character_data)

                    # Wait for user to press Enter before returning to menu
                    input("Press Enter to continue...")
                    break
                # Handle return to main menu
                elif selection == len(character_files) + 1:
                    break
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

    elif choice == '2':
        print("Exiting...")
        break
    elif choice == '3':
        # Exit the application
        print("Exiting program. Goodbye!")
        break

    else:
        # Handle invalid main menu choice
        print("Invalid choice. Please enter 1 or 2.")