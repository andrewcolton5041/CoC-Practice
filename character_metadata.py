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
        # Always initialize with default values
        self.name = os.path.basename(filename).replace('.json', '').capitalize()
        self.occupation = "Unknown"
        self.nationality = "Unknown"
        # Then try to load better values from the file
        self._load_metadata()

    def _load_metadata(self):
        """
        Load only the necessary metadata fields from the character file.
        """
        try:
            # Only read the first 1024 bytes to extract basic info
            with open(self.filename, 'r', encoding='utf-8') as f:
                file_header = f.read(1024)

            # Try to parse the header as JSON - check if it might be truncated
            try:
                header_data = json.loads(file_header)
                # The JSON might be incomplete if the file is large
                # Make sure we're getting a complete "name" field
                if 'name' in header_data:
                    self.name = header_data['name']
                if 'occupation' in header_data:
                    self.occupation = header_data['occupation']
                if 'nationality' in header_data:
                    self.nationality = header_data['nationality']
            except json.JSONDecodeError:
                # Try reading a bit more of the file
                with open(self.filename, 'r', encoding='utf-8') as f:
                    file_header = f.read(4096)  # Read more data
                    try:
                        header_data = json.loads(file_header)
                        if 'name' in header_data:
                            self.name = header_data['name']
                        if 'occupation' in header_data:
                            self.occupation = header_data['occupation']
                        if 'nationality' in header_data:
                            self.nationality = header_data['nationality']
                    except json.JSONDecodeError:
                        # Keep using default values set in __init__
                        pass
        except (IOError, OSError):
            # If file can't be read, keep using default values set in __init__
            pass

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