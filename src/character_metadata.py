"""Character Metadata Module for Call of Cthulhu Character Viewer

Provides lightweight metadata parsing for character files,
allowing the application to display a list of characters without loading all data into memory.
"""

import os
import json
import re
import typing
from src.constants import (
    DEFAULT_OCCUPATION,
    DEFAULT_NATIONALITY,
    DEFAULT_ENCODING,
    JSON_EXTENSION,
    REQUIRED_METADATA_FIELDS,
    FIELD_REGEX_PATTERNS
)


class CharacterMetadata:
    def __init__(self, filename):
        self.filename = filename
        self.name = os.path.basename(filename).replace(JSON_EXTENSION, '').capitalize()
        self.occupation = DEFAULT_OCCUPATION
        self.nationality = DEFAULT_NATIONALITY
        self._load_metadata()

    def _load_metadata(self):
        try:
            found_fields = set()
            with open(self.filename, 'r', encoding=DEFAULT_ENCODING) as f:
                raw_content = f.read()
                try:
                    partial_data = json.loads(raw_content)
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
                    for field, pattern in FIELD_REGEX_PATTERNS.items():
                        match = re.search(pattern, raw_content)
                        if match:
                            try:
                                value = json.loads(f'"{match.group(1)}"')
                            except (ValueError, TypeError):
                                value = match.group(1)
                            setattr(self, field, value)
                            found_fields.add(field)
        except (IOError, UnicodeDecodeError):
            return

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'occupation': self.occupation,
            'nationality': self.nationality,
            'filename': self.filename
        }

    def __repr__(self) -> str:
        return (
            f"CharacterMetadata(name='{self.name}', "
            f"occupation='{self.occupation}', "
            f"nationality='{self.nationality}')"
        )

    @classmethod
    def load_all_from_directory(cls, directory_path: str) -> typing.List['CharacterMetadata']:
        metadata_list = []
        try:
            if not os.path.exists(directory_path):
                return []

            with os.scandir(directory_path) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith(JSON_EXTENSION):
                        try:
                            if not os.access(entry.path, os.R_OK):
                                continue
                            with open(entry.path, 'r', encoding=DEFAULT_ENCODING) as f:
                                content = f.read()
                            try:
                                data = json.loads(content)
                                if not all(field in data for field in REQUIRED_METADATA_FIELDS):
                                    continue
                            except (json.JSONDecodeError, ValueError):
                                continue
                            metadata = cls(entry.path)
                            if (
                                metadata.name and metadata.name != DEFAULT_OCCUPATION and
                                metadata.occupation != DEFAULT_OCCUPATION and
                                metadata.nationality != DEFAULT_NATIONALITY
                            ):
                                metadata_list.append(metadata)
                        except Exception:
                            continue
            return sorted(metadata_list, key=lambda x: x.name)
        except (PermissionError, OSError):
            return []