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
  - **Advanced Memoization for Dice Rolls**
    - Intelligent caching of dice roll results
    - Configurable cache size and strategy
    - Performance tracking for repeated rolls
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
  - Memoization performance benchmarking
  - Unit tests for dice parser functionality
  - Performance tests for caching mechanisms
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
- **Advanced dice roll memoization**
- **Configurable caching strategies**

## Changelog

### Version 2.1.0 (2025-03-31)
- **Implemented advanced memoization for dice rolls**
- Added comprehensive caching mechanism for dice parser
- Enhanced performance tracking for repeated dice rolls
- Improved deterministic mode for testing
- Added configurable cache size and strategy for dice rolls
- Updated test suite to verify memoization functionality

### Version 2.0.0 (2025-03-30)
- **Completely restructured the application into a modular architecture**
- **Created dedicated modules for UI, character loading, display, and testing**
- **Optimized dice parser with regex-based tokenization for improved performance**
- **Reorganized project into a more professional folder structure**
- **Enhanced test runner to work with the new structure**
- **Updated imports throughout the application**

[... rest of the changelog remains the same ...]