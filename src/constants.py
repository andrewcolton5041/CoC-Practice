# Shared Constants for Call of Cthulhu Character Viewer

# === Character Data Validation ===
REQUIRED_FIELDS = ['name', 'attributes']
REQUIRED_METADATA_FIELDS = ['name', 'occupation', 'nationality']

# === File and JSON Handling ===
JSON_EXTENSION = '.json'
DEFAULT_DIRECTORY = 'characters'
DEFAULT_ENCODING = 'utf-8'
JSON_INDENT = 2

# === Metadata Defaults ===
DEFAULT_OCCUPATION = "Unknown"
DEFAULT_NATIONALITY = "Unknown"
FIELD_REGEX_PATTERNS = {
    'name': r'"name"\s*:\s*"([^"]+)"',
    'occupation': r'"occupation"\s*:\s*"([^"]+)"',
    'nationality': r'"nationality"\s*:\s*"([^"]+)"'
}

# === Cache Keys ===
KEY_DATA = 'data'
KEY_MOD_TIME = 'mod_time'
KEY_CACHE_TIME = 'cached_time'  # unified name across modules

# === Cache Status Messages ===
STATUS_CACHE_HIT = 'cache_hit'
STATUS_LOADED_FROM_FILE = 'loaded_from_file'
STATUS_VALIDATION_FAILED = 'validation_failed'
STATUS_FILE_NOT_FOUND = 'file_not_found'
STATUS_INVALID_JSON = 'invalid_json'

# === Cache Stats Keys ===
STAT_SIZE = 'size'
STAT_ACTIVE_ENTRIES = 'active_entries'
STAT_FILES = 'files'
STAT_MEMORY_USAGE = 'memory_usage'
STAT_MAX_SIZE = 'max_size'
STAT_HIT_RATE = 'hit_rate'
STAT_HITS = 'hits'
STAT_MISSES = 'misses'
STAT_OLDEST_AGE = 'oldest_entry_age'
STAT_NEWEST_AGE = 'newest_entry_age'

# === Utility ===
PERCENTAGE_MULTIPLIER = 100
DEFAULT_CACHE_SIZE = 15

# === Rules Constants ===
EXTREME_SUCCESS_DIVISOR = 5
HARD_SUCCESS_DIVISOR = 2
FUMBLE_THRESHOLD_MIN = 96
FUMBLE_THRESHOLD_STAT = 50
D100_DICE = "1D100"

SUCCESS_LEVELS = {
    "EXTREME_SUCCESS": "Extreme Success",
    "HARD_SUCCESS": "Hard Success",
    "REGULAR_SUCCESS": "Regular Success",
    "FAILURE": "Failure",
    "FUMBLE": "Fumble"
}

# === Dice Parser ===
MAX_DICE_STRING_LENGTH = 1000
MAX_DICE_COUNT = 100
MAX_DICE_SIDES = 1000

# === Dice Cache Constants ===
DEFAULT_DICE_CACHE_SIZE = 128

# === Success Level Thresholds ===
SUCCESS_EXTREME = "Extreme Success"
SUCCESS_HARD = "Hard Success"
SUCCESS_REGULAR = "Regular Success"
SUCCESS_FAILURE = "Failure"
SUCCESS_FUMBLE = "Fumble"

SUCCESS_LEVEL_VALUES = {
    SUCCESS_EXTREME: 4,
    SUCCESS_HARD: 3,
    SUCCESS_REGULAR: 2,
    SUCCESS_FAILURE: 1,
    SUCCESS_FUMBLE: 0
}

# === Damage Formulas ===
DAMAGE_BONUS_PATTERN = "+1D4"
DAMAGE_BONUS_DICE = "1D4"

# === Test Runner Constants ===
TESTS_DIRECTORY = 'tests'
TEST_PATTERN = 'test_*.py'

TEST_MODULES = {
    'dice_parser': 'test_dice_parser',
    'character_metadata': 'test_character_metadata',
    'character_cache': 'test_character_cache',
    'metadata_loading': 'test_metadata_loading'
}

# === UI Constants ===
CHARACTERS_DIRECTORY = 'characters'

# Cache settings
DEFAULT_UI_CACHE_SIZE = 10
CACHE_SIZE_MIN = 3
CACHE_SIZE_MAX = 50
CACHE_SIZE_CANCEL = 0

# User Input Ranges
MENU_OPTION_MIN = 1
MAIN_MENU_OPTION_MAX = 6
TEST_MENU_OPTION_MAX = 6

# UI Prompts
PROMPT_CACHE_SIZE = f"Enter new maximum cache size ({CACHE_SIZE_MIN}-{CACHE_SIZE_MAX}, or {CACHE_SIZE_CANCEL} to cancel): "
PROMPT_PRESS_ENTER = "Press Enter to continue..."


# UI Prompts
PROMPT_CACHE_SIZE = f"Enter new maximum cache size ({CACHE_SIZE_MIN}-{CACHE_SIZE_MAX}, or {CACHE_SIZE_CANCEL} to cancel): "
PROMPT_PRESS_ENTER = "Press Enter to continue..."

# Character Display Constants
MAX_ATTRIBUTE_VALUE = 100
HIGH_THRESHOLD = 0.75  # Attributes above 75% of max value are considered exceptional
LOW_THRESHOLD = 0.25   # Attributes below 25% of max value are considered poor
SEPARATOR_WIDTH = 50   # Width of separators in character display