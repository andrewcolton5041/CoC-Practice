"""
Test Runner Module for Call of Cthulhu Character Viewer

This module handles the execution of test suites for the application,
providing a consistent interface for running different test categories.

Author: Unknown
Version: 2.0
Last Updated: 2025-03-30
"""

import os
import unittest
import sys
import importlib
import constants


def run_test_suite(module_key, test_description):
    """
    Generalized function to run specified test suite.

    Args:
        module_key (str): Key of the test module in constants.TEST_MODULES
        test_description (str): Description to print when running tests

    Returns:
        bool: True if all tests passed, False otherwise
    """
    test_module_name = constants.TEST_MODULES[module_key]
    test_module_path = os.path.join(constants.TESTS_DIRECTORY, f"{test_module_name}.py")

    print(f"\n=== Running {test_description} ===\n")

    try:
        if not os.path.exists(test_module_path):
            print(f"Error: {test_module_path} not found!")
            return False

        tests_path = os.path.abspath(constants.TESTS_DIRECTORY)
        if tests_path not in sys.path:
            sys.path.insert(0, tests_path)

        if test_module_name in sys.modules:
            test_module = importlib.reload(sys.modules[test_module_name])
        else:
            test_module = importlib.import_module(test_module_name)

        loader = unittest.TestLoader()
        test_suite = loader.loadTestsFromModule(test_module)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)

        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error running {test_description.lower()}: {e}")
        return False
    finally:
        print("\n" + "=" * 50)


def run_dice_parser_tests():
    return run_test_suite('dice_parser', 'Dice Parser Tests')


def run_character_metadata_tests():
    return run_test_suite('character_metadata', 'Character Metadata Tests')


def run_character_cache_tests():
    return run_test_suite('character_cache', 'Character Cache Tests')


def run_metadata_loading_tests():
    return run_test_suite('metadata_loading', 'Optimized Metadata Loading Tests')


def run_all_tests():
    """
    Run all available test suites in sequence.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Running All Test Suites ===\n")

    dice_tests_passed = run_dice_parser_tests()
    metadata_tests_passed = run_character_metadata_tests()
    cache_tests_passed = run_character_cache_tests()
    loading_tests_passed = run_metadata_loading_tests()

    all_passed = all([
        dice_tests_passed,
        metadata_tests_passed,
        cache_tests_passed,
        loading_tests_passed
    ])

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

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("\n=== Discovering and Running All Tests ===\n")

    try:
        if not os.path.exists(constants.TESTS_DIRECTORY):
            print(f"Error: '{constants.TESTS_DIRECTORY}' directory not found!")
            return False

        loader = unittest.TestLoader()
        test_suite = loader.discover(constants.TESTS_DIRECTORY, pattern=constants.TEST_PATTERN)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)

        print("\n=== Test Summary ===")
        print(f"Ran {result.testsRun} tests")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        return len(result.failures) == 0 and len(result.errors) == 0

    except Exception as e:
        print(f"Error discovering and running tests: {e}")
        return False
    finally:
        print("\n" + "=" * 50)
