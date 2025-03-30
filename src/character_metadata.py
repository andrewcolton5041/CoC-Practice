"""
Character Metadata Module for Call of Cthulhu Character Viewer

This module provides lightweight metadata parsing for character files,
allowing the application to display a list of characters without loading
all character data into memory.

Author: Unknown
Version: 1.3
Last Updated: 2025-03-30
"""

import os
import json
import re
import typing


class CharacterMetadata:
    """
    A class for storing and retrieving basic metadata about character files.

    This class extracts only the essential information needed to display
    characters without loading full character data.
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

        # Load metadata, with a more robust approach
        self._load_metadata()

    def _load_metadata(self):
        """
        Load only the necessary metadata fields from the character file.

        Uses an optimized, multi-strategy approach to extract metadata:
        1. Partial JSON parsing (primary method)
        2. Regex fallback
        3. Fallback to default values
        """
        try:
            # Target fields to extract
            target_fields = {'name', 'occupation', 'nationality'}
            found_fields = set()

            # Primary approach: Use json parsing
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    # Use a more careful parsing approach
                    raw_content = f.read()
                    try:
                        partial_data = json.loads(raw_content)

                        # Update fields from parsed JSON
                        for field in target_fields:
                            if field in partial_data:
                                # Ensure value is converted to string
                                value = str(partial_data[field])
                                # Unescape JSON-encoded characters if needed
                                try:
                                    # Use json.loads to properly unescape special characters
                                    value = json.loads(f'"{value}"')
                                except (ValueError, TypeError):
                                    pass

                                setattr(self, field, value)
                                found_fields.add(field)

                    except json.JSONDecodeError:
                        # If full JSON parsing fails, fall back to regex
                        field_patterns = {
                            'name': r'"name"\s*:\s*"([^"]+)"',
                            'occupation': r'"occupation"\s*:\s*"([^"]+)"',
                            'nationality': r'"nationality"\s*:\s*"([^"]+)"'
                        }

                        for field, pattern in field_patterns.items():
                            match = re.search(pattern, raw_content)
                            if match:
                                # Unescape the matched value
                                try:
                                    value = json.loads(f'"{match.group(1)}"')
                                except (ValueError, TypeError):
                                    value = match.group(1)

                                setattr(self, field, value)
                                found_fields.add(field)

            except (IOError, UnicodeDecodeError):
                # If file can't be read, keep default values
                return

        except Exception:
            # Ensure we always have at least the filename-based name
            pass

    @classmethod
    def load_all_from_directory(cls, directory_path: str) -> typing.List['CharacterMetadata']:
        """
        Load metadata for all character files in a directory.

        Args:
            directory_path (str): Path to directory containing character files

        Returns:
            list: List of CharacterMetadata objects for valid character files
        """
        metadata_list = []

        try:
            # Validate directory existence
            if not os.path.exists(directory_path):
                return []

            # Use os.scandir for efficient directory traversal
            with os.scandir(directory_path) as entries:
                # Collect all valid character file metadata
                for entry in entries:
                    # Only process .json files
                    if entry.is_file() and entry.name.endswith('.json'):
                        try:
                            # Ignore files that can't be read
                            if not os.access(entry.path, os.R_OK):
                                continue

                            # Carefully check file contents for valid JSON
                            with open(entry.path, 'r', encoding='utf-8') as f:
                                content = f.read()

                                # Validate JSON structure and required fields
                                try:
                                    data = json.loads(content)

                                    # Check for required fields
                                    if not all(field in data for field in ['name', 'occupation', 'nationality']):
                                        continue

                                except (json.JSONDecodeError, ValueError):
                                    # Skip malformed JSON
                                    continue

                            # Create metadata for each valid file
                            metadata = cls(entry.path)

                            # Only add if metadata extraction was successful
                            if (metadata.name and 
                                metadata.name != "Unknown" and 
                                metadata.occupation != "Unknown" and 
                                metadata.nationality != "Unknown"):
                                metadata_list.append(metadata)

                        except Exception:
                            # Skip files that can't be processed
                            continue

            # Sort metadata alphabetically by name
            return sorted(metadata_list, key=lambda x: x.name)

        except (PermissionError, OSError):
            # Handle directory access issues
            return []

    def __repr__(self) -> str:
        """
        Provide a string representation of the metadata.

        Returns:
            str: Formatted string with character metadata
        """
        return (f"CharacterMetadata(name='{self.name}', "
                f"occupation='{self.occupation}', "
                f"nationality='{self.nationality}')")

    def to_dict(self) -> dict:
        """
        Convert metadata to a dictionary.

        Returns:
            dict: Dictionary representation of character metadata
        """
        return {
            'name': self.name,
            'occupation': self.occupation,
            'nationality': self.nationality,
            'filename': self.filename
        }