"""
Program 05: Quick Sort
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Quick Sort:
- Follows the Divide-and-Conquer paradigm:
  1. Pick a pivot element using a sensible pivot strategy (median-of-three or middle element).
  2. Partition: Rearrange the array such that all elements less than the pivot
     come before it, and all elements greater than or equal come after it.
  3. Recursively sort the sub-arrays.
- Fully manual implementation without using built-in sorted() or .sort().
- Handles empty lists, single elements, and duplicates.
"""

from typing import Any, List


def _median_of_three(arr: List[int], low: int, high: int) -> int:
    """
    Selects the median of arr[low], arr[mid], and arr[high] to use as pivot.
    Places the pivot at index high and returns its value.

    This prevents the worst-case O(n^2) degradation on already sorted or
    reverse-sorted inputs.
    """
    mid = (low + high) // 2

    # Sort the three values arr[low], arr[mid], arr[high]
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]

    # Swap median (now at mid) with high - 1 or high
    arr[mid], arr[high] = arr[high], arr[mid]
    return arr[high]


def _partition(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto partition scheme with median-of-three pivot selection.
    Rearranges elements around the pivot and returns the pivot's final index.
    """
    pivot = _median_of_three(arr, low, high)

    # Pointer for smaller element
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Swap pivot (at high) with element at i + 1
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _quick_sort_recursive(arr: List[int], low: int, high: int) -> None:
    """Helper recursive function for in-place quicksort."""
    if low < high:
        pi = _partition(arr, low, high)
        _quick_sort_recursive(arr, low, pi - 1)
        _quick_sort_recursive(arr, pi + 1, high)


def quick_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using Quick Sort.

    Algorithm Explanation:
        1. If length of array is <= 1, return a copy of array.
        2. Select pivot using median-of-three strategy (avoids worst-case O(n^2) on sorted data).
        3. Partition the array around the pivot:
           - Elements <= pivot move to the left partition.
           - Elements > pivot move to the right partition.
        4. Recursively apply Quick Sort to left and right partitions.

    Time Complexity:
        - Best Case: O(n log n) - pivot splits the array into roughly equal halves.
        - Average Case: O(n log n) - randomized or balanced partitions.
        - Worst Case: O(n^2) - occurs if pivot is always the smallest or largest element
          (heavily mitigated by median-of-three pivot selection).

    Auxiliary Space Complexity:
        - O(log n) average recursion stack depth; O(n) worst case stack depth.

    Args:
        arr: List of integers to sort.

    Returns:
        A new list containing the sorted integers.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    result = list(arr)
    if len(result) <= 1:
        return result

    _quick_sort_recursive(result, 0, len(result) - 1)
    return result


def demonstrate() -> None:
    """Demonstrates Quick Sort with various test cases."""
    print("=" * 60)
    print("DEMONSTRATION: Quick Sort (Program 05)")
    print("=" * 60)

    test_cases = [
        ("Normal unsorted list", [10, 80, 30, 90, 40, 50, 70]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [5, 4, 3, 2, 1]),
        ("List with duplicates", [5, 2, 8, 5, 2, 9, 1]),
        ("All identical elements", [6, 6, 6, 6]),
        ("Single element list", [55]),
        ("Empty list", []),
        ("Negative and positive numbers", [-12, 15, -4, 0, 7, -2])
    ]

    for label, data in test_cases:
        sorted_data = quick_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")


if __name__ == "__main__":
    demonstrate()

