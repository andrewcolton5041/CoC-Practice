"""
Test module for the CharacterMetadata implementation.

This module contains tests for the CharacterMetadata class,
verifying that it correctly loads basic character information
without loading the full character data.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import unittest
import os
import time
import json
import tempfile
from character_metadata import CharacterMetadata


class TestCharacterMetadata(unittest.TestCase):
    """Test suite for the CharacterMetadata class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create test character data
        self.test_character = {
            "name": "Test Character",
            "age": 30,
            "occupation": "Test Occupation",
            "nationality": "Test Nation",
            "attributes": {
                "Strength": 60,
                "Intelligence": 70,
                "Health": 65
            },
            "skills": {
                "Test Skill": 45
            },
            "backstory": "This is a very long backstory that should not be loaded by metadata."
        }

        # Create a test character file
        self.test_filename = os.path.join(self.temp_dir.name, "test_character.json")
        with open(self.test_filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_character, f)

        # Create a malformed JSON file for testing error handling
        self.bad_filename = os.path.join(self.temp_dir.name, "bad_character.json")
        with open(self.bad_filename, 'w', encoding='utf-8') as f:
            f.write("{This is not valid JSON}")

    def test_metadata_loading(self):
        """Test basic metadata loading from valid file."""
        metadata = CharacterMetadata(self.test_filename)

        # Check that basic metadata is loaded correctly
        self.assertEqual(metadata.name, "Test Character")
        self.assertEqual(metadata.occupation, "Test Occupation")
        self.assertEqual(metadata.nationality, "Test Nation")

    def test_metadata_fallback(self):
        """Test metadata fallback for invalid files."""
        metadata = CharacterMetadata(self.bad_filename)

        # Should use filename as fallback for name
        expected_name = "Bad_character"
        # First verify that name is not None
        self.assertIsNotNone(metadata.name, "Character name should not be None")
        # Then verify it matches the expected value (case-insensitive)
        self.assertEqual(metadata.name.lower(), expected_name.lower())
        self.assertEqual(metadata.occupation, "Unknown")

    def test_nonexistent_file(self):
        """Test handling of non-existent files."""
        nonexistent_file = os.path.join(self.temp_dir.name, "nonexistent.json")
        metadata = CharacterMetadata(nonexistent_file)

        # Should use filename as fallback - case insensitive check
        self.assertEqual(metadata.name.lower(), "nonexistent")
        self.assertEqual(metadata.occupation, "Unknown")

    def test_load_all_from_directory(self):
        """Test loading metadata for all files in a directory."""
        # Create another test character
        second_character = {
            "name": "Second Character",
            "occupation": "Second Occupation",
            "nationality": "Second Nation"
        }
        second_filename = os.path.join(self.temp_dir.name, "second_character.json")
        with open(second_filename, 'w', encoding='utf-8') as f:
            json.dump(second_character, f)

        # Load metadata for all files in directory
        metadata_list = CharacterMetadata.load_all_from_directory(self.temp_dir.name)

        # Should find 3 files (including the bad file)
        self.assertEqual(len(metadata_list), 3)

        # Check that we can find both valid characters
        character_names = [m.name for m in metadata_list]
        self.assertIn("Test Character", character_names)
        self.assertIn("Second Character", character_names)

    def test_load_from_nonexistent_directory(self):
        """Test loading from a directory that doesn't exist."""
        nonexistent_dir = os.path.join(self.temp_dir.name, "nonexistent_dir")
        metadata_list = CharacterMetadata.load_all_from_directory(nonexistent_dir)

        # Should return an empty list
        self.assertEqual(metadata_list, [])

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove the temporary directory and its contents
        self.temp_dir.cleanup()

    def test_metadata_only_loads_minimal_data(self):
        """Test that metadata loading doesn't read the full character file."""
        # Create a character with a very large backstory to simulate a large file
        large_character = {
            "name": "Large Character",
            "occupation": "Test Occupation",
            "nationality": "Test Nation",
            "backstory": "X" * 1000000  # 1MB of data
        }

        large_filename = os.path.join(self.temp_dir.name, "large_character.json")
        with open(large_filename, 'w', encoding='utf-8') as f:
            json.dump(large_character, f)

        # Create a metadata object
        start_time = time.time()
        metadata = CharacterMetadata(large_filename)
        end_time = time.time()

        # Verify that loading was fast (shouldn't read the whole file)
        # Loading a 1MB file would take significantly longer if reading it all
        load_time = end_time - start_time
        self.assertLess(load_time, 0.1, f"Loading took {load_time} seconds, which suggests full file reading")

        # Verify the object size is small (which means we didn't load the whole file)
        metadata_size = len(str(metadata.__dict__))
        self.assertLess(metadata_size, 1000, 
                       f"Metadata object size is {metadata_size} bytes, which suggests it contains the full file data")

if __name__ == '__main__':
    unittest.main()