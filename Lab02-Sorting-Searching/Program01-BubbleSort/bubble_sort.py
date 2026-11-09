"""
Program 01: Bubble Sort
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Bubble Sort:
- Iteratively steps through the list, compares adjacent elements, and swaps
  them if they are in the wrong order.
- Includes an early-termination optimization flag ('swapped') to achieve
  optimal O(n) performance when the array is already sorted.
- Fully manual implementation without using built-in sorted() or .sort().
- Handles empty lists, single elements, and duplicates.
"""

from typing import Any, List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using Bubble Sort.

    Algorithm Explanation:
        Bubble sort repeatedly sweeps through the array from left to right.
        In each pass:
        1. Compare adjacent elements: A[j] and A[j + 1].
        2. If A[j] > A[j + 1], swap them so the larger element moves right.
        3. After pass i, the i-th largest element is guaranteed to be in its
           final sorted position at the end of the array.
        4. Optimization: If a full pass completes with zero swaps, the array
           is already sorted, and we terminate early.

    Time Complexity:
        - Best Case (Already sorted): O(n) due to the early-termination flag.
        - Average Case: O(n^2) comparisons and swaps.
        - Worst Case (Reverse sorted): O(n^2) comparisons and swaps (~ n*(n-1)/2).

    Auxiliary Space Complexity:
        - O(1) in-place sorting. Modifies and returns a copy or original array.

    Args:
        arr: List of integers to sort.

    Returns:
        A new list containing the sorted integers.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    # Work on a copy to preserve the original list
    result = list(arr)
    n = len(result)

    if n <= 1:
        return result

    for i in range(n - 1):
        swapped = False
        # Last i elements are already in place
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                # Swap adjacent elements
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        # If no two elements were swapped, array is sorted
        if not swapped:
            break

    return result


def demonstrate() -> None:
    """Demonstrates Bubble Sort with various test cases."""
    print("=" * 60)
    print("DEMONSTRATION: Bubble Sort (Program 01)")
    print("=" * 60)

    test_cases = [
        ("Normal unsorted list", [64, 34, 25, 12, 22, 11, 90]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [5, 4, 3, 2, 1]),
        ("List with duplicates", [5, 2, 8, 5, 2, 9, 1]),
        ("All identical elements", [7, 7, 7, 7]),
        ("Single element list", [42]),
        ("Empty list", []),
        ("Negative and positive numbers", [3, -1, 4, -5, 0, 2])
    ]

    for label, data in test_cases:
        sorted_data = bubble_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")


if __name__ == "__main__":
    demonstrate()

