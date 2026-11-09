"""
Program 09: Sorting Performance Analysis
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program performs empirical performance benchmarking on all seven sorting algorithms:
1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Merge Sort
5. Quick Sort
6. Heap Sort
7. Radix Sort (LSD)

Benchmarking Parameters:
- Input Sizes: 100, 500, 1000 elements
- Input Distributions:
  a. Random (unsorted)
  b. Already Sorted (best-case testing)
  c. Reverse Sorted (worst-case testing)
- Precise timing using time.perf_counter() averaged across repetitions
- Tabular display of execution times (in milliseconds)
- Generation of high-resolution Matplotlib graphs saved to Lab02-Sorting-Searching/outputs/
- Analysis and discussion of empirical vs theoretical performance.
"""

import os
import random
import sys
import time
from typing import Callable, Dict, List, Tuple

# Use non-interactive Agg backend for headless environments
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Import Sorting Algorithms from Sibling Directories
# ---------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LAB_DIR = os.path.dirname(CURRENT_DIR)

# Dynamically add program paths to sys.path
for prog_dir in [
    "Program01-BubbleSort",
    "Program02-SelectionSort",
    "Program03-InsertionSort",
    "Program04-MergeSort",
    "Program05-QuickSort",
    "Program06-HeapSort",
    "Program07-RadixSort"
]:
    sys.path.append(os.path.join(LAB_DIR, prog_dir))

from bubble_sort import bubble_sort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort
from heap_sort import heap_sort
from radix_sort import radix_sort


# ---------------------------------------------------------------------------
# Benchmarking Harness
# ---------------------------------------------------------------------------

ALGORITHMS: Dict[str, Callable[[List[int]], List[int]]] = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Radix Sort": radix_sort,
}


def generate_dataset(size: int, distribution: str, seed: int = 42) -> List[int]:
    """
    Generates reproducible datasets of non-negative integers.
    Non-negative integers ensure fair, uniform compatibility across all algorithms
    including Radix Sort.

    Args:
        size: Number of elements.
        distribution: 'random', 'sorted', or 'reverse'.
        seed: Random seed for reproducibility.

    Returns:
        List of integers.
    """
    rng = random.Random(seed + size)
    # Generate numbers in range [0, 10000]
    data = [rng.randint(0, 10000) for _ in range(size)]

    if distribution == "random":
        return data
    elif distribution == "sorted":
        # Sort manually using merge_sort to adhere to constraints
        return merge_sort(data)
    elif distribution == "reverse":
        sorted_data = merge_sort(data)
        # Reverse manually
        return sorted_data[::-1]
    else:
        raise ValueError(f"Unknown distribution: {distribution}")


def measure_execution_time(
    sort_fn: Callable[[List[int]], List[int]],
    data: List[int],
    repetitions: int = 3
) -> float:
    """
    Measures the average execution time in milliseconds over multiple repetitions.

    Args:
        sort_fn: The sorting function to benchmark.
        data: The input array.
        repetitions: Number of runs to average.

    Returns:
        Average execution time in milliseconds (ms).
    """
    total_time = 0.0

    for _ in range(repetitions):
        # Always pass a fresh copy so subsequent runs are not pre-sorted
        sample = list(data)
        start = time.perf_counter()
        result = sort_fn(sample)
        end = time.perf_counter()
        total_time += (end - start)

    # Convert average to milliseconds
    avg_ms = (total_time / repetitions) * 1000.0
    return avg_ms


def run_benchmark(
    sizes: List[int] = [100, 500, 1000],
    distributions: List[str] = ["random", "sorted", "reverse"],
    repetitions: int = 3
) -> Dict[str, Dict[str, Dict[int, float]]]:
    """
    Runs the full benchmarking suite across all algorithms, distributions, and sizes.

    Returns:
        results[distribution][algorithm_name][size] = time_in_ms
    """
    results: Dict[str, Dict[str, Dict[int, float]]] = {
        dist: {algo: {} for algo in ALGORITHMS} for dist in distributions
    }

    print("\n" + "=" * 78)
    print("STARTING EMPIRICAL SORTING BENCHMARK (Pure Python Execution)")
    print("=" * 78)

    for dist in distributions:
        print(f"\n--- Testing Distribution: {dist.upper()} ---")
        for size in sizes:
            dataset = generate_dataset(size, dist)
            print(f"  Input Size: {size:<5} elements | Benchmarking 7 algorithms...", end="", flush=True)

            for algo_name, algo_fn in ALGORITHMS.items():
                t_ms = measure_execution_time(algo_fn, dataset, repetitions=repetitions)
                results[dist][algo_name][size] = t_ms

            print(" [DONE]")

    return results


def print_results_table(
    results: Dict[str, Dict[str, Dict[int, float]]],
    sizes: List[int]
) -> None:
    """Prints formatted comparison tables for each distribution."""
    for dist, algo_data in results.items():
        print("\n" + "=" * 78)
        print(f"BENCHMARK RESULTS: {dist.upper()} DATASET (Times in milliseconds)")
        print("=" * 78)

        header = f"{'Algorithm':<18} | " + " | ".join(f"Size = {sz:<6}" for sz in sizes)
        print(header)
        print("-" * len(header))

        for algo_name, size_dict in algo_data.items():
            row = f"{algo_name:<18} | " + " | ".join(f"{size_dict[sz]:>10.4f} ms" for sz in sizes)
            print(row)

        print("-" * len(header))


def plot_graphs(
    results: Dict[str, Dict[str, Dict[int, float]]],
    sizes: List[int],
    output_dir: str
) -> List[str]:
    """
    Generates and saves Matplotlib comparison graphs for each distribution and a combined view.

    Returns:
        List of paths to generated graph images.
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []

    colors = {
        "Bubble Sort": "#e74c3c",      # Red
        "Selection Sort": "#e67e22",   # Orange
        "Insertion Sort": "#f1c40f",   # Yellow
        "Merge Sort": "#2ecc71",       # Green
        "Quick Sort": "#3498db",       # Blue
        "Heap Sort": "#9b59b6",        # Purple
        "Radix Sort": "#1abc9c",       # Teal
    }
    markers = {
        "Bubble Sort": "o",
        "Selection Sort": "s",
        "Insertion Sort": "^",
        "Merge Sort": "D",
        "Quick Sort": "v",
        "Heap Sort": "P",
        "Radix Sort": "*",
    }

    # 1. Individual plots for each distribution
    for dist in ["random", "sorted", "reverse"]:
        plt.figure(figsize=(9, 6))
        for algo_name in ALGORITHMS:
            times = [results[dist][algo_name][sz] for sz in sizes]
            plt.plot(
                sizes,
                times,
                marker=markers[algo_name],
                color=colors[algo_name],
                linewidth=2,
                markersize=7,
                label=algo_name
            )

        plt.title(f"Sorting Performance on {dist.capitalize()} Data", fontsize=14, fontweight="bold")
        plt.xlabel("Input Size (Number of Elements)", fontsize=12)
        plt.ylabel("Execution Time (milliseconds)", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(loc="upper left", frameon=True)
        plt.tight_layout()

        filepath = os.path.join(output_dir, f"sorting_comparison_{dist}.png")
        plt.savefig(filepath, dpi=300)
        plt.close()
        generated_files.append(filepath)

    # 2. Combined 1x3 Subplot Grid
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=False)
    for idx, dist in enumerate(["random", "sorted", "reverse"]):
        ax = axes[idx]
        for algo_name in ALGORITHMS:
            times = [results[dist][algo_name][sz] for sz in sizes]
            ax.plot(
                sizes,
                times,
                marker=markers[algo_name],
                color=colors[algo_name],
                linewidth=1.8,
                markersize=6,
                label=algo_name
            )
        ax.set_title(f"Distribution: {dist.capitalize()}", fontsize=13, fontweight="bold")
        ax.set_xlabel("Input Size", fontsize=11)
        ax.set_ylabel("Execution Time (ms)", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.6)
        if idx == 0:
            ax.legend(loc="upper left", fontsize=9)

    plt.suptitle("Empirical Comparison of 7 Sorting Algorithms (CO2 Performance Analysis)", fontsize=15, fontweight="bold")
    plt.tight_layout()
    combined_path = os.path.join(output_dir, "sorting_comparison_all.png")
    plt.savefig(combined_path, dpi=300)
    plt.close()
    generated_files.append(combined_path)

    return generated_files


def discuss_observations() -> None:
    """Prints analytical discussion of empirical results."""
    discussion = """
==============================================================================
                      EMPIRICAL OBSERVATIONS & DISCUSSION
==============================================================================
1. O(n log n) vs O(n^2) Algorithms:
   - On Random Data: Merge Sort, Quick Sort, Heap Sort, and Radix Sort massively
     outperform Bubble, Selection, and Insertion Sort as input size reaches 1000.
   - For n = 1000, quadratic algorithms (Bubble, Selection, Insertion) take tens
     to hundreds of milliseconds, whereas O(n log n) algorithms finish in single-digit ms.

2. Impact of Input Distribution (Sorted vs Reverse-Sorted):
   - Already Sorted:
     * Bubble Sort (optimized with 'swapped' flag) and Insertion Sort achieve their
       O(n) best-case, executing nearly instantaneously with zero swaps.
     * Selection Sort remains strictly O(n^2) because it unconditionally sweeps the
       unsorted suffix for the minimum element regardless of order.
     * Quick Sort with median-of-three pivot avoids the classical O(n^2) degradation.
   - Reverse Sorted:
     * Insertion Sort and Bubble Sort encounter their absolute worst-case O(n^2)
       performance due to maximum element inversions and shifts.
     * Merge Sort and Heap Sort maintain consistent O(n log n) execution time
       irrespective of data ordering.

3. Linear-Time Radix Sort:
   - Radix Sort exhibits steady, predictable O(d * (n + b)) scaling. Because d (digits)
     is bounded, it scales linearly with n and remains insensitive to initial data sorting.
==============================================================================
"""
    print(discussion)


def main() -> None:
    """Main execution entry point."""
    sizes = [100, 500, 1000]
    output_dir = os.path.join(LAB_DIR, "outputs")

    results = run_benchmark(sizes=sizes, repetitions=3)
    print_results_table(results, sizes)

    print(f"\nGenerating and saving Matplotlib comparison graphs to:\n  {output_dir}")
    saved_graphs = plot_graphs(results, sizes, output_dir)
    for g in saved_graphs:
        print(f"  [Created Graph] {os.path.basename(g)}")

    discuss_observations()


if __name__ == "__main__":
    main()

