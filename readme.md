# Call of Cthulhu Character Viewer

A character management application for the Call of Cthulhu roleplaying game system. This application helps Game Masters and players quickly access and manage character information.

## Project Structure

The project now follows a modular architecture with clear separation of concerns:

```
coc_character_viewer/
├── characters/            # Character JSON files
├── src/                   # Source code directory
│   ├── ui.py              # User interface functions
│   ├── character_loader.py # Character data loading
│   ├── character_display.py # Character display formatting
│   ├── test_runner.py     # Test execution utilities
│   ├── character_cache.py  # Character caching mechanism
│   ├── character_metadata.py # Character metadata loading
│   ├── dice_roll.py       # Dice rolling utilities
│   ├── dice_parser.py     # Optimized dice notation parser
│   ├── coc_rules.py       # Game rules implementation
│   └── game_utils.py      # Game mechanics utilities
├── tests/                 # Test directory
│   ├── test_dice_parser.py # Dice parser tests
│   ├── test_character_cache.py # Cache tests
│   ├── test_character_metadata.py # Metadata tests
│   └── test_metadata_loading.py # Optimized loading tests
├── main.py                # Application entry point
└── readme.md              # This file
```

## Features

- **Character Management**
  - View premade characters from JSON files
  - Display formatted character sheets with all relevant information
  - Lazy loading for optimized performance

- **Dice Mechanics**
  - **Optimized regex-based dice notation parser**
  - Support for complex dice expressions (`(2D6+6)*5`)
  - Implements Call of Cthulhu 7th Edition skill check mechanics

- **Game Utilities**
  - Character skill checks
  - Opposed checks between characters
  - Weapon damage calculation
  - Success level determination (Extreme, Hard, Regular, Failure, Fumble)

- **Performance Optimizations**
  - Memory-efficient caching with LRU eviction policy
  - Configurable cache size limits for memory management
  - Optimized metadata loading with single-pass parsing
  - **Regex-based tokenization for improved dice parsing performance**
  - Proper context management for file operations
  - Character data caching system
  - Enhanced lazy loading implementation
  - Memory usage statistics and management

- **Testing Framework**
  - Comprehensive test suites for critical components
  - Unit tests for dice parser functionality
  - Performance benchmarking for optimized components
  - Improved tests for character metadata handling
  - Tests for character cache and resource management
  - Dedicated tests for metadata loading performance

## Usage

1. Run the application: `python main.py`
2. Navigate through the menu-based interface
3. Select characters to view their information
4. Use the various tools and utilities as needed
5. Configure cache size to optimize memory usage

## Technical Details

- Written in Python 3.11+
- Modular architecture for easy extension
- JSON-based character data format
- No external dependencies required
- LRU (Least Recently Used) caching mechanism
- **Optimized regex-based parsing for better performance**

## Changelog

### Version 2.0.0 (2025-03-30)
- **Completely restructured the application into a modular architecture**
- **Created dedicated modules for UI, character loading, display, and testing**
- **Optimized dice parser with regex-based tokenization for improved performance**
- **Reorganized project into a more professional folder structure**
- **Enhanced test runner to work with the new structure**
- **Updated imports throughout the application for the new structure**

### Version 1.6.0 (2025-03-30)
- Implemented memory-efficient caching with LRU eviction policy
- Added configurable cache size limits
- Improved memory management through automatic eviction of least-used entries
- Added expanded cache statistics including hit-rate tracking
- Enhanced cache configuration options in the main menu
- Added tests for LRU eviction behavior

### Version 1.5.2 (2025-03-28)
- Optimized character metadata loading with single-pass file parsing
- Improved context management in CharacterCache to ensure proper file closing
- Added dedicated test suites for optimized metadata loading and file handling
- Updated test framework to include new test categories
- Enhanced error handling throughout the application

### Version 1.5.1 (2025-03-25)
- Optimized lazy loading implementation to better leverage CharacterMetadata
- Fixed character data loading to only load full content when explicitly needed
- Added tests to verify lazy loading performance characteristics
- Improved fallback handling for malformed character files

### Version 1.5 (2025-03-20)
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