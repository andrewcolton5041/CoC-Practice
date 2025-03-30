"""
Character Metadata Module for Call of Cthulhu Character Viewer

This module provides lightweight metadata parsing for character files,
allowing the application to display a list of characters without loading
all character data into memory.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import os
import json


class CharacterMetadata:
    """
    A class for storing and retrieving basic metadata about character files.

    This class extracts only the essential information needed to display
    in character selection lists without loading the full character data.
    """

    def __init__(self, filename):
        """
        Initialize a character metadata object from a filename.

        Args:
            filename (str): Path to the character JSON file
        """
        self.filename = filename
        self.name = None
        self.occupation = None
        self.nationality = None
        self._load_metadata()

    def _load_metadata(self):
        """
        Load only the necessary metadata fields from the character file.

        This method opens the JSON file but only extracts the fields needed
        for display in the character list, minimizing memory usage.
        """
        try:
            # Only read the first 1024 bytes to extract basic info
            with open(self.filename, 'r', encoding='utf-8') as f:
                file_header = f.read(1024)

            # Parse the header portion to extract minimal data
            # This is a simplified approach that works for well-formatted JSON
            try:
                # Try to parse the header as JSON
                header_data = json.loads(file_header)
                self.name = header_data.get('name', os.path.basename(self.filename))
                self.occupation = header_data.get('occupation', 'Unknown')
                self.nationality = header_data.get('nationality', 'Unknown')
            except json.JSONDecodeError:
                # If parsing fails, use filename as fallback
                self.name = os.path.basename(self.filename).replace('.json', '').capitalize()
                self.occupation = 'Unknown'
                self.nationality = 'Unknown'
        except (IOError, OSError):
            # Use filename as fallback if file can't be read
            self.name = os.path.basename(self.filename).replace('.json', '').capitalize()
            self.occupation = 'Unknown'
            self.nationality = 'Unknown'

    @classmethod
    def load_all_from_directory(cls, directory_path):
        """
        Load metadata for all character files in a directory.

        Args:
            directory_path (str): Path to directory containing character files

        Returns:
            list: List of CharacterMetadata objects, one for each character file
        """
        metadata_list = []

        try:
            if not os.path.exists(directory_path):
                return []

            for filename in os.listdir(directory_path):
                if filename.endswith('.json'):
                    full_path = os.path.join(directory_path, filename)
                    metadata = cls(full_path)
                    metadata_list.append(metadata)

            return metadata_list
        except (PermissionError, OSError):
            return []