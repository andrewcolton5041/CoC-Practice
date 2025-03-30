"""
Test Runner Module for Call of Cthulhu Character Viewer

This module handles the execution of test suites for the application,
providing a consistent interface for running different test categories.

The module loads and executes test suites using the unittest framework,
providing formatted output and error handling.

Author: Unknown
Version: 2.0
Last Updated: 2025-03-30
"""

import os
import unittest
import sys
import importlib


def run_dice_parser_tests():
    """
    Run the dice parser test suite.

    This function loads and executes the tests defined in tests/test_dice_parser.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Dice Parser Tests ===\n")

    try:
        # Check if the test file exists in the tests directory
        if not os.path.exists('tests/test_dice_parser.py'):
            print("Error: tests/test_dice_parser.py not found!")
            return False

        # Import the test module
        try:
            # Add tests directory to path if not already there
            tests_path = os.path.abspath('tests')
            if tests_path not in sys.path:
                sys.path.insert(0, tests_path)

            # Import the module
            if 'test_dice_parser' in sys.modules:
                # Reload if already imported
                test_module = importlib.reload(sys.modules['test_dice_parser'])
            else:
                # Import if not already imported
                test_module = importlib.import_module('test_dice_parser')
        except ImportError as e:
            print(f"Error: Failed to import test_dice_parser module: {e}")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_module)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running dice parser tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_character_metadata_tests():
    """
    Run the character metadata test suite.

    This function loads and executes the tests defined in tests/test_character_metadata.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Character Metadata Tests ===\n")

    try:
        # Check if the test file exists in the tests directory
        if not os.path.exists('tests/test_character_metadata.py'):
            print("Error: tests/test_character_metadata.py not found!")
            return False

        # Import the test module
        try:
            # Add tests directory to path if not already there
            tests_path = os.path.abspath('tests')
            if tests_path not in sys.path:
                sys.path.insert(0, tests_path)

            # Import the module
            if 'test_character_metadata' in sys.modules:
                # Reload if already imported
                test_module = importlib.reload(sys.modules['test_character_metadata'])
            else:
                # Import if not already imported
                test_module = importlib.import_module('test_character_metadata')
        except ImportError as e:
            print(f"Error: Failed to import test_character_metadata module: {e}")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_module)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running character metadata tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_character_cache_tests():
    """
    Run the character cache test suite.

    This function loads and executes the tests defined in tests/test_character_cache.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Character Cache Tests ===\n")

    try:
        # Check if the test file exists in the tests directory
        if not os.path.exists('tests/test_character_cache.py'):
            print("Error: tests/test_character_cache.py not found!")
            return False

        # Import the test module
        try:
            # Add tests directory to path if not already there
            tests_path = os.path.abspath('tests')
            if tests_path not in sys.path:
                sys.path.insert(0, tests_path)

            # Import the module
            if 'test_character_cache' in sys.modules:
                # Reload if already imported
                test_module = importlib.reload(sys.modules['test_character_cache'])
            else:
                # Import if not already imported
                test_module = importlib.import_module('test_character_cache')
        except ImportError as e:
            print(f"Error: Failed to import test_character_cache module: {e}")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_module)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running character cache tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_metadata_loading_tests():
    """
    Run the optimized metadata loading test suite.

    This function loads and executes the tests defined in tests/test_metadata_loading.py.
    It uses the unittest framework to discover and run the tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running Optimized Metadata Loading Tests ===\n")

    try:
        # Check if the test file exists in the tests directory
        if not os.path.exists('tests/test_metadata_loading.py'):
            print("Error: tests/test_metadata_loading.py not found!")
            return False

        # Import the test module
        try:
            # Add tests directory to path if not already there
            tests_path = os.path.abspath('tests')
            if tests_path not in sys.path:
                sys.path.insert(0, tests_path)

            # Import the module
            if 'test_metadata_loading' in sys.modules:
                # Reload if already imported
                test_module = importlib.reload(sys.modules['test_metadata_loading'])
            else:
                # Import if not already imported
                test_module = importlib.import_module('test_metadata_loading')
        except ImportError as e:
            print(f"Error: Failed to import test_metadata_loading module: {e}")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Load tests from the test module
        test_suite = loader.loadTestsFromModule(test_module)

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running optimized metadata loading tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_all_tests():
    """
    Run all available test suites in sequence.

    This function runs all test categories and collects overall results.

    Returns:
        bool: True if all tests in all suites passed, False otherwise
    """
    print("\n=== Running All Test Suites ===\n")

    all_passed = True

    # Run each test suite in sequence
    dice_tests_passed = run_dice_parser_tests()
    metadata_tests_passed = run_character_metadata_tests()
    cache_tests_passed = run_character_cache_tests()
    loading_tests_passed = run_metadata_loading_tests()

    # Check if all tests passed
    all_passed = (
        dice_tests_passed and 
        metadata_tests_passed and 
        cache_tests_passed and 
        loading_tests_passed
    )

    # Print overall summary
    print("\n=== Overall Test Summary ===")
    print(f"Dice Parser Tests: {'PASS' if dice_tests_passed else 'FAIL'}")
    print(f"Character Metadata Tests: {'PASS' if metadata_tests_passed else 'FAIL'}")
    print(f"Character Cache Tests: {'PASS' if cache_tests_passed else 'FAIL'}")
    print(f"Metadata Loading Tests: {'PASS' if loading_tests_passed else 'FAIL'}")
    print(f"\nOverall Result: {'PASS' if all_passed else 'FAIL'}")

    return all_passed


def discover_and_run_tests():
    """
    Automatically discover and run all test files in the tests directory.

    This function uses unittest's test discovery to find and run all tests.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Discovering and Running All Tests ===\n")

    try:
        # Check if the tests directory exists
        if not os.path.exists('tests'):
            print("Error: 'tests' directory not found!")
            return False

        # Create a test loader
        loader = unittest.TestLoader()

        # Discover tests in the tests directory
        test_suite = loader.discover('tests', pattern='test_*.py')

        # Create a test runner
        runner = unittest.TextTestRunner(verbosity=2)

        # Run the tests
        result = runner.run(test_suite)

        # Print a summary
        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        # Return True if all tests passed
        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error discovering and running tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)