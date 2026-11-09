"""
Program 02: Selection Sort
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Selection Sort:
- Divides the list into a sorted prefix and an unsorted suffix.
- Repeatedly searches the unsorted portion to find the minimum element,
  then swaps it into its correct position at the boundary.
- Fully manual implementation without using built-in sorted() or .sort().
- Handles empty lists, single elements, and duplicates.
"""

from typing import Any, List


def selection_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using Selection Sort.

    Algorithm Explanation:
        1. Maintain two sub-arrays in a given array:
           - Already sorted sub-array (from index 0 to i-1).
           - Remaining unsorted sub-array (from index i to n-1).
        2. In each iteration i from 0 to n - 2:
           - Find the minimum element in the unsorted sub-array arr[i ... n-1].
           - Swap the found minimum element with the element at index i.
        3. Repeat until the entire array is sorted.

    Time Complexity:
        - Best Case: O(n^2) - must always perform all comparisons.
        - Average Case: O(n^2) comparisons, O(n) swaps.
        - Worst Case: O(n^2) comparisons, O(n) swaps.

    Auxiliary Space Complexity:
        - O(1) in-place sorting. Modifies and returns a copy or original array.

    Args:
        arr: List of integers to sort.

    Returns:
        A new list containing the sorted integers.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    result = list(arr)
    n = len(result)

    if n <= 1:
        return result

    for i in range(n - 1):
        # Assume the first element of unsorted portion is minimum
        min_idx = i
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j

        # Swap the found minimum element with the first element
        if min_idx != i:
            result[i], result[min_idx] = result[min_idx], result[i]

    return result


def demonstrate() -> None:
    """Demonstrates Selection Sort with various test cases."""
    print("=" * 60)
    print("DEMONSTRATION: Selection Sort (Program 02)")
    print("=" * 60)

    test_cases = [
        ("Normal unsorted list", [29, 10, 14, 37, 13]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [5, 4, 3, 2, 1]),
        ("List with duplicates", [4, 2, 4, 3, 1, 2]),
        ("All identical elements", [9, 9, 9, 9]),
        ("Single element list", [100]),
        ("Empty list", []),
        ("Negative and positive numbers", [-7, 12, -3, 0, 5, -1])
    ]

    for label, data in test_cases:
        sorted_data = selection_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")


if __name__ == "__main__":
    demonstrate()

