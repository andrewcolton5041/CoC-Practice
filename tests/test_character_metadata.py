"""
Test module for the optimized CharacterMetadata implementation.

This module contains tests specifically designed to verify that the optimized
character metadata loading works correctly and efficiently, including
scenarios with large files, malformed JSON, and unusual formatting.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import unittest
import os
import time
import json
import tempfile
from src.character_metadata import CharacterMetadata


class TestOptimizedMetadataLoading(unittest.TestCase):
    """Test suite for the optimized CharacterMetadata loading mechanism."""

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

    def test_basic_metadata_loading(self):
        """Test basic metadata loading from valid file."""
        metadata = CharacterMetadata(self.test_filename)

        # Check that basic metadata is loaded correctly
        self.assertEqual(metadata.name, "Test Character")
        self.assertEqual(metadata.occupation, "Test Occupation")
        self.assertEqual(metadata.nationality, "Test Nation")

    def test_malformed_json_handling(self):
        """Test metadata loading from malformed JSON file."""
        metadata = CharacterMetadata(self.bad_filename)

        # Should use filename as fallback for name
        expected_name = "Bad_character"
        # First verify that name is not None
        self.assertIsNotNone(metadata.name, "Character name should not be None")
        # Then verify it matches the expected value (case-insensitive)
        self.assertEqual(metadata.name.lower(), expected_name.lower())
        self.assertEqual(metadata.occupation, "Unknown")

    def test_large_file_performance(self):
        """Test that metadata loading is efficient with large files."""
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
        load_time = end_time - start_time
        self.assertLess(load_time, 0.1, f"Loading took {load_time} seconds, which suggests full file reading")

        # Verify the metadata was correctly extracted
        self.assertEqual(metadata.name, "Large Character")
        self.assertEqual(metadata.occupation, "Test Occupation")
        self.assertEqual(metadata.nationality, "Test Nation")

    def test_fields_in_different_positions(self):
        """Test metadata loading when fields are in different positions in the file."""
        # Create a character with metadata fields in unusual positions
        character_with_reordered_fields = {
            "attributes": {"Strength": 60},
            "skills": {"Test Skill": 45},
            "occupation": "Buried Occupation",
            "backstory": "Some backstory text",
            "name": "Buried Name",
            "nationality": "Buried Nation"
        }

        # Create the test file
        reordered_filename = os.path.join(self.temp_dir.name, "reordered_character.json")
        with open(reordered_filename, 'w', encoding='utf-8') as f:
            json.dump(character_with_reordered_fields, f)

        # Load the metadata
        metadata = CharacterMetadata(reordered_filename)

        # Verify that all fields were found regardless of their position
        self.assertEqual(metadata.name, "Buried Name")
        self.assertEqual(metadata.occupation, "Buried Occupation")
        self.assertEqual(metadata.nationality, "Buried Nation")

    def test_fields_with_special_characters(self):
        """Test metadata loading when fields contain special characters."""
        # Create a character with special characters in metadata fields
        character_with_special_chars = {
            "name": "Special \"Quotes\" Character",
            "occupation": "Special \\ Backslash Occupation",
            "nationality": "Special\nNewline\tTab Nation"
        }

        # Create the test file
        special_chars_filename = os.path.join(self.temp_dir.name, "special_chars_character.json")
        with open(special_chars_filename, 'w', encoding='utf-8') as f:
            json.dump(character_with_special_chars, f)

        # Load the metadata
        metadata = CharacterMetadata(special_chars_filename)

        # Verify that fields with special characters were handled correctly
        self.assertEqual(metadata.name, "Special \"Quotes\" Character")
        self.assertEqual(metadata.occupation, "Special \\ Backslash Occupation")
        self.assertEqual(metadata.nationality, "Special\nNewline\tTab Nation")

    def test_directory_loading(self):
        """Test loading metadata for all files in a directory."""
        # Create multiple character files with different metadata
        characters = [
            {"name": "Character 1", "occupation": "Occupation 1", "nationality": "Nation 1"},
            {"name": "Character 2", "occupation": "Occupation 2", "nationality": "Nation 2"},
            {"name": "Character 3", "occupation": "Occupation 3", "nationality": "Nation 3"}
        ]

        for i, character in enumerate(characters):
            filename = os.path.join(self.temp_dir.name, f"character_{i+1}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(character, f)

        # Load metadata for all files in directory
        metadata_list = CharacterMetadata.load_all_from_directory(self.temp_dir.name)

        # Should find all valid character files (including the ones created in other tests)
        self.assertGreaterEqual(len(metadata_list), 3)

        # Verify that all names are found
        character_names = [m.name for m in metadata_list]
        self.assertIn("Character 1", character_names)
        self.assertIn("Character 2", character_names)
        self.assertIn("Character 3", character_names)

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove the temporary directory and its contents
        self.temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()