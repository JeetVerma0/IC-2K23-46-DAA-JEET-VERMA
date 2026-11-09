"""
Program 08: Binary Search (Iterative & Recursive)
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Binary Search:
- Fundamental search algorithm on sorted collections.
- Halves the search space in each iteration by comparing the target with the
  middle element.
- Provides both:
  1. Iterative Binary Search
  2. Recursive Binary Search
- Validates that the input list is strictly sorted before proceeding.
- Returns clear result indicators and diagnostic messages when elements are missing.
"""

from typing import Any, List, Optional, Tuple


def is_sorted(arr: List[int]) -> bool:
    """
    Checks if a list is sorted in non-decreasing order.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    Searches for target in a sorted list using the iterative binary search algorithm.

    Algorithm Explanation:
        1. Precondition: arr MUST be sorted in ascending order.
        2. Set low = 0 and high = len(arr) - 1.
        3. While low <= high:
           - Calculate mid = low + (high - low) // 2 (prevents integer overflow).
           - If arr[mid] == target, target is found at index mid.
           - If target < arr[mid], narrow search to left half: high = mid - 1.
           - If target > arr[mid], narrow search to right half: low = mid + 1.
        4. If loop terminates without match, target is not in array (return -1).

    Time Complexity:
        - Best Case: O(1) when target is at the initial midpoint.
        - Average Case: O(log n)
        - Worst Case: O(log n) when target is absent or at boundaries.

    Auxiliary Space Complexity:
        - O(1) iterative execution with no additional memory allocation.

    Args:
        arr: Sorted list of integers.
        target: The integer to locate.

    Returns:
        The zero-based index of target if found; -1 otherwise.

    Raises:
        ValueError: If the array is not sorted.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    if not is_sorted(arr):
        raise ValueError(
            "Binary Search requires a sorted list. Input array is not sorted."
        )

    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def _binary_search_recursive_helper(arr: List[int], target: int, low: int, high: int) -> int:
    """Helper recursive function for binary search."""
    if low > high:
        return -1

    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return _binary_search_recursive_helper(arr, target, mid + 1, high)
    else:
        return _binary_search_recursive_helper(arr, target, low, mid - 1)


def binary_search_recursive(arr: List[int], target: int) -> int:
    """
    Searches for target in a sorted list using recursive binary search.

    Time Complexity:
        - Best Case: O(1)
        - Average Case: O(log n)
        - Worst Case: O(log n)

    Auxiliary Space Complexity:
        - O(log n) recursive call stack frames.

    Args:
        arr: Sorted list of integers.
        target: The integer to locate.

    Returns:
        The zero-based index of target if found; -1 otherwise.

    Raises:
        ValueError: If the array is not sorted.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    if not is_sorted(arr):
        raise ValueError(
            "Binary Search requires a sorted list. Input array is not sorted."
        )

    return _binary_search_recursive_helper(arr, target, 0, len(arr) - 1)


def search_and_report(arr: List[int], target: int) -> None:
    """Executes both iterative and recursive searches and prints a clear report."""
    print(f"\nSearching for target: {target} in array: {arr}")
    try:
        idx_iter = binary_search_iterative(arr, target)
        idx_rec = binary_search_recursive(arr, target)

        assert idx_iter == idx_rec, "Iterative and Recursive results must match"

        if idx_iter != -1:
            print(f"  [Found] Target {target} is present at index {idx_iter}.")
        else:
            print(f"  [Not Found] Target {target} was not found in the array.")
    except ValueError as err:
        print(f"  [Validation Error] {err}")


def demonstrate() -> None:
    """Demonstrates Binary Search with various scenarios."""
    print("=" * 60)
    print("DEMONSTRATION: Binary Search (Program 08)")
    print("=" * 60)

    sample_sorted = [11, 22, 33, 44, 55, 66, 77, 88, 99]

    # Search for present elements
    search_and_report(sample_sorted, 44)   # Middle element
    search_and_report(sample_sorted, 11)   # First element
    search_and_report(sample_sorted, 99)   # Last element

    # Search for missing elements
    search_and_report(sample_sorted, 50)   # Element in between
    search_and_report(sample_sorted, 5)    # Element smaller than minimum
    search_and_report(sample_sorted, 1000) # Element greater than maximum

    # Boundary cases
    search_and_report([], 10)              # Empty array
    search_and_report([42], 42)            # Single element present
    search_and_report([42], 99)            # Single element missing

    # Unsorted input validation
    print("\nCase: Unsorted array validation (Expected ValueError)")
    unsorted_list = [50, 10, 40, 20]
    search_and_report(unsorted_list, 20)


if __name__ == "__main__":
    demonstrate()

