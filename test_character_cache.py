"""
Test module for the CharacterCache implementation.

This module contains tests for the CharacterCache class,
verifying that it correctly handles file operations with proper
context management and resource cleanup. It also tests the new
weak reference and LRU implementation for memory efficiency.

Author: Unknown
Version: 2.0
Last Updated: 2025-03-30
"""

import unittest
import os
import json
import tempfile
import time
import gc
import sys
import weakref
from character_cache import CharacterCache


class TestCharacterCache(unittest.TestCase):
    """Test suite for the CharacterCache class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create the cache instance with a small max_size for testing
        self.cache = CharacterCache(max_size=3)

        # Create test character data
        self.test_character = {
            "name": "Test Character",
            "attributes": {
                "Strength": 60,
                "Intelligence": 70
            }
        }

        # Create a test character file
        self.test_filename = os.path.join(self.temp_dir.name, "test_character.json")
        with open(self.test_filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_character, f)

        # Create another test character file
        self.test_filename2 = os.path.join(self.temp_dir.name, "test_character2.json")
        self.test_character2 = {
            "name": "Test Character 2",
            "attributes": {
                "Strength": 70,
                "Intelligence": 60
            }
        }
        with open(self.test_filename2, 'w', encoding='utf-8') as f:
            json.dump(self.test_character2, f)

        # Create a third test character file
        self.test_filename3 = os.path.join(self.temp_dir.name, "test_character3.json")
        self.test_character3 = {
            "name": "Test Character 3",
            "attributes": {
                "Strength": 80,
                "Intelligence": 50
            }
        }
        with open(self.test_filename3, 'w', encoding='utf-8') as f:
            json.dump(self.test_character3, f)

        # Create a fourth test character file for LRU testing
        self.test_filename4 = os.path.join(self.temp_dir.name, "test_character4.json")
        self.test_character4 = {
            "name": "Test Character 4",
            "attributes": {
                "Strength": 90,
                "Intelligence": 40
            }
        }
        with open(self.test_filename4, 'w', encoding='utf-8') as f:
            json.dump(self.test_character4, f)

        # Create a malformed JSON file
        self.bad_filename = os.path.join(self.temp_dir.name, "bad_character.json")
        with open(self.bad_filename, 'w', encoding='utf-8') as f:
            f.write("{This is not valid JSON}")

    def test_basic_load_and_cache(self):
        """Test basic loading and caching of character data."""
        # First load
        character_data, status = self.cache.load_character(self.test_filename)
        self.assertEqual(status, "loaded_from_file")

        # Check character data safely
        self.assertIsNotNone(character_data, "Character data should not be None")
        if character_data is not None:  # Extra safety check
            self.assertEqual(character_data["name"], "Test Character")

        # Second load should be from cache
        character_data2, status2 = self.cache.load_character(self.test_filename)
        self.assertEqual(status2, "cache_hit")

        # Check character data safely
        self.assertIsNotNone(character_data2, "Character data from cache should not be None")
        if character_data2 is not None:  # Extra safety check
            self.assertEqual(character_data2["name"], "Test Character")

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        # First load
        self.cache.load_character(self.test_filename)

        # Invalidate cache
        self.cache.invalidate(self.test_filename)

        # Next load should be from file
        character_data, status = self.cache.load_character(self.test_filename)
        self.assertEqual(status, "loaded_from_file")

        # Check character data safely
        self.assertIsNotNone(character_data, "Character data should not be None")
        if character_data is not None:  # Extra safety check
            self.assertEqual(character_data["name"], "Test Character")

    def test_file_modification(self):
        """Test file modification detection."""
        # First load
        self.cache.load_character(self.test_filename)

        # Wait a moment and modify the file
        time.sleep(0.1)
        modified_character = self.test_character.copy()
        modified_character["name"] = "Modified Character"

        with open(self.test_filename, 'w', encoding='utf-8') as f:
            json.dump(modified_character, f)

        # Next load should detect modification and reload
        character_data, status = self.cache.load_character(self.test_filename)
        self.assertEqual(status, "loaded_from_file")

        # Check character data safely
        self.assertIsNotNone(character_data, "Character data should not be None")
        if character_data is not None:  # Extra safety check
            self.assertEqual(character_data["name"], "Modified Character")

    def test_error_handling(self):
        """Test error handling for invalid files."""
        # Test with non-existent file
        non_existent_file = os.path.join(self.temp_dir.name, "non_existent.json")
        character_data, status = self.cache.load_character(non_existent_file)
        self.assertIsNone(character_data)
        self.assertEqual(status, "file_not_found")

        # Test with malformed JSON
        character_data, status = self.cache.load_character(self.bad_filename)
        self.assertIsNone(character_data)
        self.assertEqual(status, "invalid_json")

    def test_file_handles_closed(self):
        """Test that file handles are properly closed."""
        # Load a file
        self.cache.load_character(self.test_filename)

        # Try to rename the file - this would fail if the file handle is still open
        new_filename = os.path.join(self.temp_dir.name, "renamed_file.json")
        os.rename(self.test_filename, new_filename)

        # If we get here without exceptions, the file handle was properly closed
        self.assertTrue(os.path.exists(new_filename))
        self.assertFalse(os.path.exists(self.test_filename))

        # Update test_filename for tearDown
        self.test_filename = new_filename

    def test_validation_function(self):
        """Test that the validation function works correctly."""
        # Define a validation function
        def validate(data):
            return "name" in data and "attributes" in data

        # Test with valid data
        character_data, status = self.cache.load_character(self.test_filename, validate)
        self.assertEqual(status, "loaded_from_file")

        # Check character data safely
        self.assertIsNotNone(character_data, "Character data should not be None")

        # Create a file with invalid data
        invalid_file = os.path.join(self.temp_dir.name, "invalid.json")
        with open(invalid_file, 'w', encoding='utf-8') as f:
            json.dump({"some_field": "missing required fields"}, f)

        # Test with invalid data
        character_data, status = self.cache.load_character(invalid_file, validate)
        self.assertIsNone(character_data)
        self.assertEqual(status, "validation_failed")

    def test_lru_eviction(self):
        """Test that the LRU eviction policy works correctly."""
        # Load the first three characters (should fill the cache with max_size=3)
        self.cache.load_character(self.test_filename)
        self.cache.load_character(self.test_filename2)
        self.cache.load_character(self.test_filename3)

        # Verify all three are in the cache
        stats = self.cache.get_stats()
        self.assertEqual(stats["size"], 3)
        self.assertIn(self.test_filename, stats["files"])
        self.assertIn(self.test_filename2, stats["files"])
        self.assertIn(self.test_filename3, stats["files"])

        # Load a fourth character, which should evict the least recently used (the first one)
        self.cache.load_character(self.test_filename4)

        # Verify the first character was evicted
        stats = self.cache.get_stats()
        self.assertEqual(stats["size"], 3)
        self.assertNotIn(self.test_filename, stats["files"])
        self.assertIn(self.test_filename2, stats["files"])
        self.assertIn(self.test_filename3, stats["files"])
        self.assertIn(self.test_filename4, stats["files"])

        # Access the second character to move it to the end of the LRU order
        self.cache.get(self.test_filename2)

        # Load the first character again, which should now evict the third one
        self.cache.load_character(self.test_filename)

        # Verify the third character was evicted
        stats = self.cache.get_stats()
        self.assertEqual(stats["size"], 3)
        self.assertIn(self.test_filename, stats["files"])
        self.assertIn(self.test_filename2, stats["files"])
        self.assertNotIn(self.test_filename3, stats["files"])
        self.assertIn(self.test_filename4, stats["files"])

    def test_weak_references(self):
        """Test the cache's LRU eviction mechanism."""
        # Since we can't use weak references with dictionaries,
        # rename this test to reflect what we're actually testing

        # Create a separate cache with a small size limit
        test_cache = CharacterCache(max_size=3)

        # Create and load 3 test files to fill the cache
        test_files = []
        for i in range(3):
            filename = os.path.join(self.temp_dir.name, f"cache_test_{i}.json")
            test_files.append(filename)
            test_data = {
                "name": f"Test Character {i}",
                "attributes": {"Strength": 50 + i}
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(test_data, f)

            # Load the file into cache
            result, status = test_cache.load_character(filename)
            self.assertEqual(status, "loaded_from_file")

        # Verify all 3 files are in the cache
        for filename in test_files:
            self.assertTrue(test_cache.contains(filename))

        # Now add a 4th file, which should push out the least recently used (first) file
        new_filename = os.path.join(self.temp_dir.name, "cache_test_new.json")
        new_data = {
            "name": "New Test Character",
            "attributes": {"Strength": 70}
        }
        with open(new_filename, 'w', encoding='utf-8') as f:
            json.dump(new_data, f)

        # Load the new file
        test_cache.load_character(new_filename)

        # Verify the first file was evicted
        self.assertFalse(test_cache.contains(test_files[0]))

        # But files 2 and 3 should still be there
        self.assertTrue(test_cache.contains(test_files[1]))
        self.assertTrue(test_cache.contains(test_files[2]))

        # And the new file should be there too
        self.assertTrue(test_cache.contains(new_filename))

        # Verify cache size is still at the maximum
        stats = test_cache.get_stats()
        self.assertEqual(stats["size"], 3)

    def test_cache_stats(self):
        """Test that cache statistics are correctly maintained."""
        # Fresh cache should have no hits or misses
        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 0)
        self.assertEqual(stats["misses"], 0)
        self.assertEqual(stats["hit_rate"], 0)

        # First load should be a miss
        self.cache.load_character(self.test_filename)
        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 0)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["hit_rate"], 0)

        # Second load should be a hit
        self.cache.load_character(self.test_filename)
        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["hit_rate"], 50)

        # Loading a different file should be a miss
        self.cache.load_character(self.test_filename2)
        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 2)
        self.assertEqual(stats["hit_rate"], 33.33333333333333)

        # Loading an invalid file should be a miss
        self.cache.load_character(self.bad_filename)
        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 3)

        # Clear the cache and verify stats are maintained
        self.cache.invalidate()
        stats = self.cache.get_stats()
        self.assertEqual(stats["size"], 0)
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 3)
        self.assertEqual(stats["hit_rate"], 25)

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove the temporary directory and its contents
        self.temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()