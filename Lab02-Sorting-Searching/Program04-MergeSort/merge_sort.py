"""
Program 04: Merge Sort
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Merge Sort:
- Follows the Divide-and-Conquer paradigm:
  1. Divide: Break array into two halves at the midpoint.
  2. Conquer: Recursively sort both sub-arrays.
  3. Combine: Merge the two sorted sub-arrays into a single sorted array.
- Stable, comparison-based sorting algorithm.
- Fully manual implementation without using built-in sorted() or .sort().
- Handles empty lists, single elements, and duplicates.
"""

from typing import Any, List


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merges two sorted lists into a single sorted list.

    Time Complexity: O(len(left) + len(right))
    Auxiliary Space Complexity: O(len(left) + len(right))

    Args:
        left: Sorted list of integers.
        right: Sorted list of integers.

    Returns:
        Combined sorted list.
    """
    merged: List[int] = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        if left[i] <= right[j]:  # <= ensures stability
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements from left (if any)
    while i < len_left:
        merged.append(left[i])
        i += 1

    # Append remaining elements from right (if any)
    while j < len_right:
        merged.append(right[j])
        j += 1

    return merged


def merge_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using Merge Sort.

    Algorithm Explanation:
        1. Base Case: If array has 0 or 1 elements, it is already sorted.
        2. Divide: Find midpoint mid = len(arr) // 2.
        3. Recursive Sort:
           left_sorted = merge_sort(arr[:mid])
           right_sorted = merge_sort(arr[mid:])
        4. Combine: merge(left_sorted, right_sorted).

    Time Complexity:
        - Best Case: O(n log n)
        - Average Case: O(n log n)
        - Worst Case: O(n log n)
        The recurrence relation T(n) = 2T(n/2) + O(n) always resolves to O(n log n).

    Auxiliary Space Complexity:
        - O(n) auxiliary space to store sub-arrays and merged output.

    Args:
        arr: List of integers to sort.

    Returns:
        A new list containing the sorted integers.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    n = len(arr)
    if n <= 1:
        return list(arr)

    mid = n // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def demonstrate() -> None:
    """Demonstrates Merge Sort with various test cases."""
    print("=" * 60)
    print("DEMONSTRATION: Merge Sort (Program 04)")
    print("=" * 60)

    test_cases = [
        ("Normal unsorted list", [38, 27, 43, 3, 9, 82, 10]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [5, 4, 3, 2, 1]),
        ("List with duplicates", [5, 1, 3, 5, 2, 1, 8]),
        ("All identical elements", [4, 4, 4, 4]),
        ("Single element list", [99]),
        ("Empty list", []),
        ("Negative and positive numbers", [-15, 20, -3, 0, 8, -1])
    ]

    for label, data in test_cases:
        sorted_data = merge_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")


if __name__ == "__main__":
    demonstrate()

