"""Character Metadata Module for Call of Cthulhu Character Viewer

Provides lightweight metadata parsing for character files,
allowing the application to display a list of characters without loading all data into memory.

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple

from src.constants import (
    DEFAULT_OCCUPATION,
    DEFAULT_NATIONALITY,
    JSON_EXTENSION,
    REQUIRED_METADATA_FIELDS,
    FIELD_REGEX_PATTERNS
)
from src.file_utils import read_file_partial, list_json_files
from src.validation import validate_character_metadata, validate_file_path
from src.error_handling import log_error


class CharacterMetadata:
    """
    Lightweight class for character metadata.
    Extracts basic information without loading the entire character file.
    """

    def __init__(self, filename: str):
        """
        Initialize metadata for a character file.

        Args:
            filename (str): Path to the character file
        """
        self.filename = filename
        self.name = os.path.basename(filename).replace(JSON_EXTENSION, '').capitalize()
        self.occupation = DEFAULT_OCCUPATION
        self.nationality = DEFAULT_NATIONALITY
        self._load_metadata()

    def _load_metadata(self) -> None:
        """
        Load metadata from the character file efficiently.
        Uses partial file reading and regex for large files.
        """
        if not validate_file_path(self.filename):
            return

        try:
            content, status = read_file_partial(self.filename)
            if status != "success" or not content:
                return

            found_fields = set()

            # Try JSON parsing first (more reliable but can be slower)
            try:
                partial_data = json.loads(content)
                for field in REQUIRED_METADATA_FIELDS:
                    if field in partial_data:
                        value = str(partial_data[field])
                        try:
                            value = json.loads(f'"{value}"')
                        except (ValueError, TypeError):
                            pass
                        setattr(self, field, value)
                        found_fields.add(field)

            except json.JSONDecodeError:
                # Fallback to regex for partial or malformed JSON
                for field, pattern in FIELD_REGEX_PATTERNS.items():
                    match = re.search(pattern, content)
                    if match:
                        try:
                            value = json.loads(f'"{match.group(1)}"')
                        except (ValueError, TypeError):
                            value = match.group(1)
                        setattr(self, field, value)
                        found_fields.add(field)

        except Exception as e:
            log_error("metadata_load_error", f"Error loading metadata from {self.filename}", 
                     {"error": str(e)})

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to a dictionary.

        Returns:
            dict: Dictionary representation of metadata
        """
        return {
            'name': self.name,
            'occupation': self.occupation,
            'nationality': self.nationality,
            'filename': self.filename
        }

    def __repr__(self) -> str:
        """
        String representation of metadata.

        Returns:
            str: Formatted string representation
        """
        return (
            f"CharacterMetadata(name='{self.name}', "
            f"occupation='{self.occupation}', "
            f"nationality='{self.nationality}')"
        )

    @classmethod
    def load_all_from_directory(cls, directory_path: str) -> List['CharacterMetadata']:
        """
        Load metadata for all character files in a directory.

        Args:
            directory_path (str): Path to the directory containing character files

        Returns:
            list: List of CharacterMetadata objects
        """
        metadata_list = []

        try:
            json_files = list_json_files(directory_path)

            for file_path in json_files:
                try:
                    # Try to load the file partially first to check validity
                    content, status = read_file_partial(file_path)
                    if status != "success" or not content:
                        continue

                    # Attempt to parse as JSON
                    try:
                        data = json.loads(content)
                        if not all(field in data for field in REQUIRED_METADATA_FIELDS):
                            continue
                    except (json.JSONDecodeError, ValueError):
                        continue

                    # Create metadata object
                    metadata = cls(file_path)

                    # Validate metadata
                    if validate_character_metadata(metadata.to_dict()):
                        metadata_list.append(metadata)

                except Exception as e:
                    log_error("metadata_error", f"Error processing {file_path}", {"error": str(e)})
                    continue

            return sorted(metadata_list, key=lambda x: x.name)

        except Exception as e:
            log_error("directory_error", f"Error listing metadata from {directory_path}", 
                     {"error": str(e)})
            return []