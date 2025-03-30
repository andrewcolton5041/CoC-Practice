"""
Character Metadata Module for Call of Cthulhu Character Viewer

This module provides lightweight metadata parsing for character files,
allowing the application to display a list of characters without loading
all character data into memory.

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import os
import json
import re


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
        Load only the necessary metadata fields from the character file
        using an optimized single-pass approach.
        """
        # Define the fields we're interested in
        target_fields = {'name', 'occupation', 'nationality'}
        found_fields = set()

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                # Use a buffer size large enough for typical metadata
                buffer_size = 4096  # 4KB should be sufficient for most headers

                # Read the initial chunk of the file
                chunk = f.read(buffer_size)

                # Check if we have potentially incomplete JSON
                if len(chunk) >= buffer_size and not chunk.rstrip().endswith('}'):
                    # We might have incomplete JSON, use regex extraction instead
                    # Extract the fields with regex patterns
                    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', chunk)
                    if name_match:
                        self.name = name_match.group(1)
                        found_fields.add('name')

                    occupation_match = re.search(r'"occupation"\s*:\s*"([^"]+)"', chunk)
                    if occupation_match:
                        self.occupation = occupation_match.group(1)
                        found_fields.add('occupation')

                    nationality_match = re.search(r'"nationality"\s*:\s*"([^"]+)"', chunk)
                    if nationality_match:
                        self.nationality = nationality_match.group(1)
                        found_fields.add('nationality')
                else:
                    # We likely have complete JSON or a small file, try to parse it
                    try:
                        data = json.loads(chunk)
                        # Extract the metadata fields
                        if 'name' in data:
                            self.name = data['name']
                            found_fields.add('name')
                        if 'occupation' in data:
                            self.occupation = data['occupation']
                            found_fields.add('occupation')
                        if 'nationality' in data:
                            self.nationality = data['nationality']
                            found_fields.add('nationality')
                    except json.JSONDecodeError:
                        # If JSON parsing fails, try the regex approach
                        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', chunk)
                        if name_match:
                            self.name = name_match.group(1)
                            found_fields.add('name')

                        occupation_match = re.search(r'"occupation"\s*:\s*"([^"]+)"', chunk)
                        if occupation_match:
                            self.occupation = occupation_match.group(1)
                            found_fields.add('occupation')

                        nationality_match = re.search(r'"nationality"\s*:\s*"([^"]+)"', chunk)
                        if nationality_match:
                            self.nationality = nationality_match.group(1)
                            found_fields.add('nationality')

                # If we're missing any fields and haven't read the whole file, try
                # reading more of the file to find the remaining fields
                if len(found_fields) < len(target_fields) and len(chunk) >= buffer_size:
                    # Read more of the file to look for the remaining fields
                    remaining_fields = target_fields - found_fields

                    # Read a bit more to try to find these fields
                    chunk = f.read(buffer_size)

                    # Look for the remaining fields with regex
                    if 'name' in remaining_fields:
                        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', chunk)
                        if name_match:
                            self.name = name_match.group(1)

                    if 'occupation' in remaining_fields:
                        occupation_match = re.search(r'"occupation"\s*:\s*"([^"]+)"', chunk)
                        if occupation_match:
                            self.occupation = occupation_match.group(1)

                    if 'nationality' in remaining_fields:
                        nationality_match = re.search(r'"nationality"\s*:\s*"([^"]+)"', chunk)
                        if nationality_match:
                            self.nationality = nationality_match.group(1)

        except (IOError, OSError, UnicodeDecodeError):
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