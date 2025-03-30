# Call of Cthulhu Character Viewer

A character management application for the Call of Cthulhu roleplaying game system. This application helps Game Masters and players quickly access and manage character information.

## Features

- **Character Management**
  - View premade characters from JSON files
  - Display formatted character sheets with all relevant information
  - **Improved lazy loading for optimized performance**

- **Dice Mechanics**
  - Robust dice notation parser (`3D6`, `1D20+5`, etc.)
  - Support for complex dice expressions (`(2D6+6)*5`)
  - Implements Call of Cthulhu 7th Edition skill check mechanics

- **Game Utilities**
  - Character skill checks
  - Opposed checks between characters
  - Weapon damage calculation
  - Success level determination (Extreme, Hard, Regular, Failure, Fumble)

- **Performance Optimizations**
  - Character data caching system
  - **Enhanced lazy loading implementation that only reads full character data when needed**
  - Memory usage statistics and management

- **Testing Framework**
  - Comprehensive test suites for critical components
  - Unit tests for dice parser functionality
  - Unit tests for character metadata handling
  - **Tests to verify correct lazy loading behavior**

## Usage

1. Run the application: `python main.py`
2. Navigate through the menu-based interface
3. Select characters to view their information
4. Use the various tools and utilities as needed

## Technical Details

- Written in Python 3.11+
- Modular architecture for easy extension
- JSON-based character data format
- No external dependencies required

## Changelog

### Version 1.5.1 (2025-03-30)
- Optimized lazy loading implementation to better leverage CharacterMetadata
- Fixed character data loading to only load full content when explicitly needed
- Added tests to verify lazy loading performance characteristics
- Improved fallback handling for malformed character files

### Version 1.5 (2025-03-28)
- Added lazy loading optimization for character files
- Created CharacterMetadata class for efficient character listing
- Added unit tests for the CharacterMetadata implementation
- Reorganized test functionality into a dedicated submenu
- Added ability to run all test suites at once

### Version 1.4 (2025-03-15)
- Added character caching system for improved performance
- Added cache statistics display
- Added ability to clear the character cache
- Improved error handling for file operations

### Version 1.3 (2025-02-20)
- Added dice parser test functionality
- Fixed several bugs in dice parsing
- Improved character display formatting
- Updated input validation

### Version 1.2 (2025-01-10)
- Added support for game mechanics utilities
- Implemented skill checks and opposed checks
- Added weapon damage calculation
- Fixed character loading issues

### Version 1.1 (2024-12-05)
- Added dice rolling functionality with robust parser
- Implemented Call of Cthulhu rules module
- Improved menu navigation
- Added error handling for user input

### Version 1.0 (2024-11-15)
- Initial release
- Basic character viewing functionality
- Support for JSON character files
- Simple menu-based interface