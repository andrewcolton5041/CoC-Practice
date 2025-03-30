"""
Call of Cthulhu Character Viewer

This is the main module for a Call of Cthulhu character management application.
It provides functionality to:
- Load premade characters from JSON files
- Display character information in a formatted way
- Navigate through a menu-based interface

This application can be used by game masters and players to quickly access
character information for the Call of Cthulhu roleplaying game.

Author: Unknown
Version: 1.0
Last Updated: Unknown
"""

import os
import json
import os.path

character_cache = {}




def load_character_from_json(filename):
  """
  Load a premade character from a JSON file with intelligent caching.

  Checks if the character is already in the cache and if the file hasn't changed.

  Args:
      filename (str): Path to the JSON file containing character data

  Returns:
      dict: Dictionary containing the character data
  """
  # Get the file's last modification time
  try:
      mod_time = os.path.getmtime(filename)
  except OSError:
      # If file doesn't exist or can't be accessed, return None
      print(f"Cannot access {filename}")
      return None

  # Check if file is in cache and if cached version is still current
  if filename in character_cache and character_cache[filename]["mod_time"] == mod_time:
      return character_cache[filename]["data"]

  # Load from file
  try:
      with open(filename, 'r') as f:
          character_data = json.load(f)

      # Store both the data and the modification time
      character_cache[filename] = {
          "data": character_data,
          "mod_time": mod_time
      }
      return character_data
  except Exception as e:
      print(f"Error loading character from {filename}: {e}")
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
    """
  # Print divider line and basic character information
  print("\n" + "=" * 50)
  print(f"Name: {character_data['name']}")
  print(f"Age: {character_data['age']}")
  print(f"Occupation: {character_data.get('occupation', 'Unknown')}")
  print(f"Nationality: {character_data.get('nationality', 'Unknown')}")

  # Print character attributes
  print("\n--- Attributes ---")
  for attr, value in character_data['attributes'].items():
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


def invalidate_cache(filename=None):
  """
  Invalidate the character cache.

  Args:
      filename (str, optional): Specific file to remove from cache.
          If None, clears the entire cache.
  """
  global character_cache

  if filename is None:
    # Clear the entire cache
    character_cache = {}
    print("Cache cleared")
  elif filename in character_cache:
    # Remove specific file from cache
    del character_cache[filename]
    print(f"{filename} removed from cache")


def get_cache_status():
  """
  Get information about the current state of the character cache.

  Returns:
      dict: Dictionary with cache statistics
  """
  return {
      "size": len(character_cache),
      "characters": list(character_cache.keys()),
      "memory_usage": sum(len(str(data)) for data in character_cache.values())
  }


def main():
  """
  Main menu function that handles user interaction with the application.

  This function displays the main menu, handles user input, and
  calls the appropriate functions based on user selection.
  Implements character caching for improved performance.
  """
  while True:
      # Display main menu
      print("\n=== Call of Cthulhu Character Viewer ===")
      print("1. View Premade Characters")
      print("2. Clear Character Cache")  # New option
      print("3. Exit")

      # Get user choice
      choice = input("\nEnter your choice (1-3): ")

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
                      # Load and display the selected character (now with caching)
                      filename = os.path.join('characters', character_files[selection - 1])
                      character_data = load_character_from_json(filename)
                      if character_data:  # Check if load was successful
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
          # Clear the character cache
          invalidate_cache()
          print("Character cache cleared.")

      elif choice == '3':
          # Exit the application
          print("Exiting program. Goodbye!")
          break

      else:
          # Handle invalid main menu choice
          print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
  main()
