"""
Investigator Development Phase Module

This module implements the skill improvement mechanics for the Call of Cthulhu RPG.
It handles the process of skill development based on successful skill usage during play.

Key Mechanics:
- Track skills used successfully during play
- Evaluate skill improvement at the end of a scenario
- Apply probabilistic skill point increases

Author: Andrew C
Version: 1.0
Last Updated: 3/31/2025
"""

from typing import Dict, List, Union
import random

from src.constants import (
    CharacterSheetKeys, 
    RuleConstants
)
from src.coc_rules import improvement_check


class InvestigatorDevelopmentPhase:
    """
    Manages the skill improvement process for investigators.

    This class handles the mechanics of skill development, 
    tracking successful skill usage, and applying skill improvements.
    """

    @staticmethod
    def can_improve_skill(skill_name: str) -> bool:
        """
        Determine if a skill is eligible for improvement.

        Args:
            skill_name (str): The name of the skill to check

        Returns:
            bool: Whether the skill can be improved
        """
        # Cthulhu Mythos and Credit Rating never improve
        excluded_skills = ["Cthulhu Mythos", "Credit Rating"]
        return skill_name not in excluded_skills

    @staticmethod
    def improve_skill(character_data: Dict, skill_name: str) -> Union[Dict, None]:
        """
        Attempt to improve a specific skill for an investigator.

        Args:
            character_data (dict): The character's full data dictionary
            skill_name (str): The name of the skill to improve

        Returns:
            dict or None: Updated character data if skill improved, None otherwise
        """
        # Validate skill improvement eligibility
        if not InvestigatorDevelopmentPhase.can_improve_skill(skill_name):
            return None

        # Ensure the skill exists in the character's skills
        if (CharacterSheetKeys.SKILLS not in character_data or 
            skill_name not in character_data[CharacterSheetKeys.SKILLS]):
            return None

        # Get current skill value
        current_skill = character_data[CharacterSheetKeys.SKILLS][skill_name]

        # Perform improvement check
        if improvement_check(current_skill):
            # Roll 1D10 for skill improvement
            improvement_points = random.randint(1, 10)

            # Update skill value
            new_skill_value = min(current_skill + improvement_points, 
                                  RuleConstants.MAX_SKILL_VALUE)

            # Update character data
            character_data[CharacterSheetKeys.SKILLS][skill_name] = new_skill_value

            return character_data

        return None

    def development_phase(self, character_data: Dict, checked_skills: List[str]) -> Dict:
        """
        Execute the full investigator development phase.

        Args:
            character_data (dict): The character's full data dictionary
            checked_skills (list): List of skills successfully used during play

        Returns:
            dict: Updated character data after skill improvements
        """
        # Create a copy to avoid modifying the original
        updated_character = character_data.copy()

        # Track skills that actually improved
        improved_skills = []

        # Check each checked skill for potential improvement
        for skill in checked_skills:
            result = self.improve_skill(updated_character, skill)
            if result:
                improved_skills.append(skill)

        return {
            'character_data': updated_character,
            'improved_skills': improved_skills
        }

# Example usage and helper function
def perform_development_phase(character_data: Dict, checked_skills: List[str]) -> Dict:
    """
    Convenience function to perform the development phase for a character.

    Args:
        character_data (dict): The character's full data dictionary
        checked_skills (list): List of skills successfully used during play

    Returns:
        dict: Results of the development phase
    """
    dev_phase = InvestigatorDevelopmentPhase()
    return dev_phase.development_phase(character_data, checked_skills)