"""
Test module for the optimized CharacterMetadata implementation.

This module contains tests specifically designed to verify that the optimized
character metadata loading works correctly and efficiently, including
scenarios with large files, malformed JSON, and unusual formatting.

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import unittest
import os
import time
import json
import tempfile
import sys
import stat


class TestOptimizedMetadataLoading(unittest.TestCase):
    """Test suite for the optimized CharacterMetadata loading mechanism."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create test character data
        self.test_characters = [
            {
                "name": "Character 1",
                "occupation": "Test Occupation 1",
                "nationality": "Test Nation 1"
            },
            {
                "name": "Character 2",
                "occupation": "Test Occupation 2", 
                "nationality": "Test Nation 2"
            },
            {
                "name": "Character 3",
                "occupation": "Test Occupation 3",
                "nationality": "Test Nation 3"
            }
        ]

        # Create test character files
        self.test_filenames = []
        for i, character in enumerate(self.test_characters):
            filename = os.path.join(self.temp_dir.name, f"test_character_{i+1}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(character, f)
            self.test_filenames.append(filename)

        # Add a non-JSON file to test filtering
        with open(os.path.join(self.temp_dir.name, "not_a_character.txt"), 'w') as f:
            f.write("This is not a JSON file")

        # Import CharacterMetadata after setup to avoid circular imports
        from src.character_metadata import CharacterMetadata
        self.CharacterMetadata = CharacterMetadata

    def test_directory_scanning_efficiency(self):
        """
        Test the efficiency of directory scanning using os.scandir().

        Verify that:
        1. Only JSON files are processed
        2. All valid JSON files are found
        3. Non-JSON files are ignored
        """
        # Load metadata for all files in directory
        metadata_list = self.CharacterMetadata.load_all_from_directory(self.temp_dir.name)

        # Should find only the JSON character files
        self.assertEqual(len(metadata_list), 3, 
            "Should only process JSON character files")

        # Verify metadata is correctly loaded
        metadata_names = [metadata.name for metadata in metadata_list]
        expected_names = [char['name'] for char in self.test_characters]
        self.assertCountEqual(metadata_names, expected_names, 
            "Metadata names should match original character names")

    def test_handling_of_unreadable_files(self):
        """
        Test handling of unreadable files in the directory.
        """
        # Create an unreadable file
        unreadable_file = os.path.join(self.temp_dir.name, "unreadable.json")
        with open(unreadable_file, 'w') as f:
            f.write('{"name": "Unreadable Character"}')

        # Remove read permissions
        os.chmod(unreadable_file, 0o000)

        try:
            # Attempt to load metadata
            metadata_list = self.CharacterMetadata.load_all_from_directory(self.temp_dir.name)

            # Should still process other readable files
            self.assertEqual(len(metadata_list), 3, 
                "Should skip unreadable files but process others")

        finally:
            # Restore permissions to allow cleanup
            os.chmod(unreadable_file, 0o666)

    def test_sorting_of_metadata(self):
        """
        Verify that metadata is sorted alphabetically by name.
        """
        metadata_list = self.CharacterMetadata.load_all_from_directory(self.temp_dir.name)

        # Verify sorting
        sorted_names = sorted([char['name'] for char in self.test_characters])
        loaded_names = [metadata.name for metadata in metadata_list]

        self.assertEqual(loaded_names, sorted_names, 
            "Metadata should be sorted alphabetically by name")

    def test_performance_of_directory_scanning(self):
        """
        Test the performance of directory scanning.

        Verify that scanning a directory with many files is efficient.
        """
        # Create a large number of test files
        large_num_files = 100
        for i in range(large_num_files):
            filename = os.path.join(self.temp_dir.name, f"large_test_{i}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "name": f"Large Character {i}",
                    "occupation": f"Test Occupation {i}",
                    "nationality": "Test Nation"
                }, f)

        # Measure time of directory scanning
        start_time = time.time()
        metadata_list = self.CharacterMetadata.load_all_from_directory(self.temp_dir.name)
        end_time = time.time()

        # Verify performance (should be relatively quick)
        scanning_time = end_time - start_time
        self.assertTrue(scanning_time < 1.0, 
            f"Directory scanning took too long: {scanning_time} seconds")

        # Verify correct number of files processed (original 3 + new 100)
        self.assertEqual(len(metadata_list), large_num_files + 3, 
            "Should process all JSON files in the directory")

    def test_error_handling_with_malformed_json(self):
        """
        Test handling of malformed JSON files in the directory.
        """
        # Create a malformed JSON file
        malformed_file = os.path.join(self.temp_dir.name, "malformed.json")
        with open(malformed_file, 'w', encoding='utf-8') as f:
            f.write("{This is not valid JSON}")

        # Attempt to load metadata
        metadata_list = self.CharacterMetadata.load_all_from_directory(self.temp_dir.name)

        # Should still process other valid files
        self.assertEqual(len(metadata_list), 3, 
            "Should skip malformed JSON files but process others")

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove the temporary directory and its contents
        self.temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()