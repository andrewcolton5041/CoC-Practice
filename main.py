import os
import json

def load_character_from_json(filename):
    """Load a premade character from a JSON file."""
    with open(filename, 'r') as f:
        character_data = json.load(f)
    return character_data

def display_character(character_data):
    """Display a character's sheet in a formatted way."""
    print("\n" + "="*50)
    print(f"Name: {character_data['name']}")
    print(f"Age: {character_data['age']}")
    print(f"Occupation: {character_data.get('occupation', 'Unknown')}")
    print(f"Nationality: {character_data.get('nationality', 'Unknown')}")

    print("\n--- Attributes ---")
    for attr, value in character_data['attributes'].items():
        print(f"{attr}: {value}")

    if 'skills' in character_data:
        print("\n--- Skills ---")
        for skill, value in character_data['skills'].items():
            print(f"{skill}: {value}")

    if 'weapons' in character_data:
        print("\n--- Weapons ---")
        for weapon in character_data['weapons']:
            print(f"{weapon['name']} - Skill: {weapon['skill']} - Damage: {weapon['damage']}")

    if 'backstory' in character_data:
        print("\n--- Backstory ---")
        print(character_data['backstory'])

    print("="*50 + "\n")

def main():
    """Main menu function."""
    while True:
        print("\n=== Call of Cthulhu Character Viewer ===")
        print("1. View Premade Characters")
        print("2. Exit")

        choice = input("\nEnter your choice (1-2): ")

        if choice == '1':
            # List character files from the characters directory
            character_files = []
            try:
                character_files = [f for f in os.listdir('characters') if f.endswith('.json')]
            except FileNotFoundError:
                print("Characters directory not found!")
                continue

            if not character_files:
                print("No character files found!")
                continue

            # Display character list
            print("\n--- Available Characters ---")
            for i, filename in enumerate(character_files, 1):
                name = filename.replace('.json', '').capitalize()
                print(f"{i}. {name}")

            print(f"{len(character_files) + 1}. Back to Main Menu")

            # Let user select a character
            while True:
                try:
                    selection = int(input(f"\nSelect a character (1-{len(character_files) + 1}): "))
                    if 1 <= selection <= len(character_files):
                        # Load and display the selected character
                        filename = os.path.join('characters', character_files[selection - 1])
                        character_data = load_character_from_json(filename)
                        display_character(character_data)

                        # Wait for user to press Enter to continue
                        input("Press Enter to continue...")
                        break
                    elif selection == len(character_files) + 1:
                        break
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == '2':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()