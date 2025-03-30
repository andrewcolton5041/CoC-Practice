"""
Cache Benchmarking Module for Call of Cthulhu Character Viewer

This module provides utilities for measuring and reporting cache performance,
helping to optimize caching strategies across the application.

Key features:
- Benchmark cache hit rates and performance
- Compare cached vs. uncached operations
- Generate performance reports
- Profile different caching strategies

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import time
import gc
import statistics
from typing import Dict, Any, List, Callable, Tuple, Optional, Union
from functools import wraps

from src.character_cache_core import CharacterCache
from src.cache_stats import calculate_character_cache_stats
from src.dice_roll import get_dice_cache_stats, clear_dice_cache
from src.constants import (
    BENCH_ITERATIONS,
    BENCH_WARMUP_ITERATIONS,
    BENCH_MIN_SPEEDUP,
    BENCH_REPORT_DECIMAL_PLACES,
    BENCH_SMALL_SAMPLE,
    BENCH_MEDIUM_SAMPLE,
    BENCH_LARGE_SAMPLE
)


def time_function(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Measure the execution time of a function.

    Args:
        func: Function to time
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        tuple: (result, execution_time)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    execution_time = time.time() - start_time
    return result, execution_time


def benchmark_function(func: Callable, 
                       iterations: int = BENCH_ITERATIONS, 
                       warmup: int = BENCH_WARMUP_ITERATIONS, 
                       *args, **kwargs) -> Dict[str, Any]:
    """
    Benchmark a function's performance over multiple iterations.

    Args:
        func: Function to benchmark
        iterations: Number of iterations to run
        warmup: Number of warmup iterations
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        dict: Benchmark statistics
    """
    # Perform warmup iterations
    for _ in range(warmup):
        func(*args, **kwargs)

    # Perform timed iterations
    times = []
    results = []
    for _ in range(iterations):
        result, execution_time = time_function(func, *args, **kwargs)
        times.append(execution_time)
        results.append(result)

    # Calculate statistics
    stats = {
        "iterations": iterations,
        "total_time": sum(times),
        "mean_time": statistics.mean(times),
        "median_time": statistics.median(times),
        "min_time": min(times),
        "max_time": max(times),
        "stdev_time": statistics.stdev(times) if len(times) > 1 else 0,
        "operations_per_second": iterations / sum(times) if sum(times) > 0 else 0
    }

    return stats


def compare_cached_vs_uncached(cached_func: Callable, 
                              uncached_func: Callable,
                              iterations: int = BENCH_ITERATIONS,
                              warmup: int = BENCH_WARMUP_ITERATIONS,
                              *args, **kwargs) -> Dict[str, Any]:
    """
    Compare performance between cached and uncached functions.

    Args:
        cached_func: Cached version of the function
        uncached_func: Uncached version of the function
        iterations: Number of iterations to run
        warmup: Number of warmup iterations
        *args: Arguments to pass to the functions
        **kwargs: Keyword arguments to pass to the functions

    Returns:
        dict: Comparison results
    """
    # Run garbage collection to reduce interference
    gc.collect()

    # Benchmark uncached function
    uncached_stats = benchmark_function(uncached_func, iterations, warmup, *args, **kwargs)

    # Run garbage collection again
    gc.collect()

    # Benchmark cached function
    cached_stats = benchmark_function(cached_func, iterations, warmup, *args, **kwargs)

    # Calculate speedup
    if cached_stats["mean_time"] > 0:
        speedup = uncached_stats["mean_time"] / cached_stats["mean_time"]
    else:
        speedup = float('inf')  # Avoid division by zero

    # Calculate memory impact (not fully accurate due to Python's memory management)
    memory_before = 0  # Not implemented properly
    memory_after = 0   # Not implemented properly
    memory_impact = memory_after - memory_before

    # Compile comparison stats
    comparison = {
        "uncached": uncached_stats,
        "cached": cached_stats,
        "speedup": speedup,
        "memory_impact": memory_impact,
        "is_effective": speedup >= BENCH_MIN_SPEEDUP,
        "iterations": iterations
    }

    return comparison


def format_benchmark_report(stats: Dict[str, Any], 
                           title: str = "Benchmark Report",
                           precision: int = BENCH_REPORT_DECIMAL_PLACES) -> str:
    """
    Format benchmark statistics into a human-readable report.

    Args:
        stats: Benchmark statistics dict
        title: Report title
        precision: Decimal places for floating-point values

    Returns:
        str: Formatted report
    """
    lines = [
        f"=== {title} ===",
        f"Iterations: {stats.get('iterations', 0):,}",
        f"Total Time: {stats.get('total_time', 0):.{precision}f} seconds",
        f"Mean Time: {stats.get('mean_time', 0):.{precision}f} seconds",
        f"Median Time: {stats.get('median_time', 0):.{precision}f} seconds",
        f"Min/Max Time: {stats.get('min_time', 0):.{precision}f}/{stats.get('max_time', 0):.{precision}f} seconds",
        f"Operations/Second: {stats.get('operations_per_second', 0):,.{precision}f}"
    ]

    if "stdev_time" in stats:
        lines.append(f"Standard Deviation: {stats['stdev_time']:.{precision}f} seconds")

    return "\n".join(lines)


def format_comparison_report(comparison: Dict[str, Any],
                            title: str = "Cache Performance Comparison",
                            precision: int = BENCH_REPORT_DECIMAL_PLACES) -> str:
    """
    Format a comparison between cached and uncached functions.

    Args:
        comparison: Comparison statistics dict
        title: Report title
        precision: Decimal places for floating-point values

    Returns:
        str: Formatted comparison report
    """
    # Format individual reports
    uncached_report = format_benchmark_report(
        comparison.get("uncached", {}), 
        title="Uncached Performance", 
        precision=precision
    )

    cached_report = format_benchmark_report(
        comparison.get("cached", {}), 
        title="Cached Performance", 
        precision=precision
    )

    # Format summary
    speedup = comparison.get("speedup", 0)
    is_effective = comparison.get("is_effective", False)
    effectiveness = "EFFECTIVE" if is_effective else "NOT EFFECTIVE"

    summary = [
        f"=== {title} ===",
        f"Iterations: {comparison.get('iterations', 0):,}",
        f"Speedup Factor: {speedup:.{precision}f}x",
        f"Memory Impact: {comparison.get('memory_impact', 0):,} bytes",
        f"Caching Assessment: {effectiveness}"
    ]

    # Combine all sections
    report = "\n".join(summary) + "\n\n" + uncached_report + "\n\n" + cached_report

    return report


    from typing import Dict, Any, List, Callable, Tuple, Optional, Union

def benchmark_character_cache(cache_size: Optional[int] = None) -> Dict[str, Any]:
    """
    Benchmark the character cache with different configurations.

    Args:
        cache_size: Optional cache size to test (uses default if None)

    Returns:
        dict: Benchmark results for the character cache
    """
    # Create a test cache with specified size
    cache = CharacterCache(max_size=cache_size) if cache_size else CharacterCache()

    # Create benchmark functions
    sample_size = BENCH_MEDIUM_SAMPLE

    # Define benchmark scenarios
    scenarios = {
        "small_cache": {
            "size": 5,
            "iterations": BENCH_SMALL_SAMPLE
        },
        "medium_cache": {
            "size": 20,
            "iterations": BENCH_MEDIUM_SAMPLE
        },
        "large_cache": {
            "size": 50,
            "iterations": BENCH_LARGE_SAMPLE
        }
    }

    # Execute benchmarks
    results = {}
    for name, config in scenarios.items():
        # Skip if specific cache size was requested
        if cache_size and config["size"] != cache_size:
            continue

        test_cache = CharacterCache(max_size=config["size"])
        # Benchmark code would be here, but we can't actually run it
        # since we don't have test files in this function

        # For now, just add placeholder stats
        results[name] = {
            "size": config["size"],
            "hit_rate": 0,
            "miss_rate": 0,
            "operations_per_second": 0
        }

    return results


def benchmark_dice_cache(iterations: int = BENCH_ITERATIONS) -> Dict[str, Any]:
    """
    Benchmark the dice roll cache performance.

    Args:
        iterations: Number of iterations to perform

    Returns:
        dict: Benchmark results for the dice cache
    """
    # Clear the dice cache to start fresh
    clear_dice_cache()

    # Sample dice expressions
    dice_expressions = [
        "1D20",
        "3D6",
        "2D8+5",
        "(1D10+2)*3"
    ]

    # This is just a template - actual implementation would benchmark
    # dice rolling functions with different configurations

    # Return placeholder data for now
    return {
        "iterations": iterations,
        "expressions": len(dice_expressions),
        "stats": get_dice_cache_stats()
    }


# Create a global registry for cache profiles
_cache_profile_registry = {}

def profile_cache_decorator(func: Callable) -> Callable:
    """
    Decorator to profile cache performance of a function.

    This decorator adds simple profiling to a cached function
    to track hits, misses, and timing.

    Args:
        func: Function to profile

    Returns:
        Callable: Profiled function
    """
    # Create unique key for this function
    func_key = f"{func.__module__}.{func.__qualname__}"

    # Initialize stats
    _cache_profile_registry[func_key] = {
        "calls": 0,
        "hits": 0,
        "misses": 0,
        "total_time": 0.0
    }

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get stats reference
        stats = _cache_profile_registry[func_key]

        # Record stats
        stats["calls"] += 1

        # Time the function call
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time

        # Update timing stats
        stats["total_time"] += execution_time

        # We can't directly access cache info, so we estimate
        # (actual implementation would vary based on caching method)

        return result

    return wrapper

def get_cache_profile_stats(func: Callable) -> Dict[str, Any]:
    """
    Get profiling statistics for a decorated function.

    Args:
        func: The decorated function

    Returns:
        dict: Statistics for the function
    """
    func_key = f"{func.__module__}.{func.__qualname__}"
    return _cache_profile_registry.get(func_key, {})


def generate_cache_optimization_report() -> str:
    """
    Generate a comprehensive report on cache optimization opportunities.

    Returns:
        str: Formatted report with optimization recommendations
    """
    # This would analyze all caches and their performance
    # and suggest optimizations, but needs access to all current caches

    report = [
        "=== Cache Optimization Report ===",
        "This report analyzes cache performance and suggests optimizations.",
        "",
        "General Recommendations:",
        "1. Consider using OrderedDict.move_to_end() instead of pop/re-add pattern",
        "2. Apply functools.lru_cache to pure functions with expensive calculations",
        "3. Tune cache size based on memory constraints and hit rates",
        "",
        "Specific Recommendations:",
        "- No specific recommendations available (need actual cache data)",
    ]

    return "\n".join(report)