"""
Program 03: Insertion Sort
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Insertion Sort:
- Builds the final sorted array one item at a time.
- Considers each element and inserts it into its proper position within
  the already-sorted prefix by shifting larger elements one position to the right.
- Fully manual implementation without using built-in sorted() or .sort().
- Handles empty lists, single elements, and duplicates.
"""

from typing import Any, List


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using Insertion Sort.

    Algorithm Explanation:
        1. Iterate from index 1 to n - 1 (element at index 0 is trivially sorted).
        2. Store current element as 'key' = arr[i].
        3. Compare 'key' with elements to its left (from index i - 1 down to 0).
        4. Shift all elements greater than 'key' one position to the right to
           create space for 'key'.
        5. Insert 'key' into its vacant sorted position.

    Time Complexity:
        - Best Case (Already sorted): O(n) comparisons and 0 shifts.
        - Average Case: O(n^2) comparisons and shifts (~ n^2 / 4).
        - Worst Case (Reverse sorted): O(n^2) comparisons and shifts (~ n^2 / 2).

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

    for i in range(1, n):
        key = result[i]
        j = i - 1

        # Move elements of result[0..i-1] that are greater than key
        # to one position ahead of their current position
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def demonstrate() -> None:
    """Demonstrates Insertion Sort with various test cases."""
    print("=" * 60)
    print("DEMONSTRATION: Insertion Sort (Program 03)")
    print("=" * 60)

    test_cases = [
        ("Normal unsorted list", [12, 11, 13, 5, 6]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [5, 4, 3, 2, 1]),
        ("List with duplicates", [5, 2, 8, 5, 2, 9, 1]),
        ("All identical elements", [3, 3, 3, 3]),
        ("Single element list", [7]),
        ("Empty list", []),
        ("Negative and positive numbers", [-10, 5, -2, 0, 8, -1])
    ]

    for label, data in test_cases:
        sorted_data = insertion_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")


if __name__ == "__main__":
    demonstrate()

