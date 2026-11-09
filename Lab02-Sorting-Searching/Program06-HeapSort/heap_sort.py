"""
Program 06: Heap Sort
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Heap Sort:
- Comparison-based sorting algorithm based on a Binary Max-Heap data structure.
- Two primary phases:
  1. Build Max-Heap: Transform the input array into a binary max heap where each
     parent node is greater than or equal to its children.
  2. Heap Sort: Repeatedly swap the root (maximum element) with the last element
     of the unsorted heap, reduce heap size by 1, and restore heap property
     via 'heapify'.
- Fully manual implementation without using built-in sorted(), .sort(), or heapq.
- Handles empty lists, single elements, and duplicates.
"""

from typing import Any, List


def heapify(arr: List[int], n: int, i: int) -> None:
    """
    Maintains the max-heap property for a subtree rooted at index i in arr of size n.

    Time Complexity: O(log n)
    Auxiliary Space Complexity: O(1) iterative approach.

    Args:
        arr: List representing binary heap.
        n: Current size of the active heap.
        i: Root index of the subtree to heapify.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # If left child is larger than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child is larger than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root, swap and continue heapifying downward
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers in ascending order using Heap Sort.

    Algorithm Explanation:
        1. Build a max-heap from the input data:
           Start from the last non-leaf node ((n // 2) - 1) down to 0, calling
           heapify() on each node. Building the heap takes O(n) time.
        2. One by one, extract elements from the heap:
           - Swap the root (arr[0], which holds maximum element) with the last
             element of the heap (arr[i]).
           - Reduce heap size to i.
           - Call heapify() on the root (index 0) to maintain max-heap property.
        3. Once all elements are extracted, the array is sorted in ascending order.

    Time Complexity:
        - Best Case: O(n log n)
        - Average Case: O(n log n)
        - Worst Case: O(n log n)
        Unlike quicksort, heap sort guarantees O(n log n) worst-case time.

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

    # Phase 1: Build max heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(result, n, i)

    # Phase 2: One by one extract an element from heap
    for i in range(n - 1, 0, -1):
        # Move current root (maximum element) to end
        result[i], result[0] = result[0], result[i]
        # Call max heapify on the reduced heap
        heapify(result, i, 0)

    return result


def demonstrate() -> None:
    """Demonstrates Heap Sort with various test cases."""
    print("=" * 60)
    print("DEMONSTRATION: Heap Sort (Program 06)")
    print("=" * 60)

    test_cases = [
        ("Normal unsorted list", [12, 11, 13, 5, 6, 7]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [5, 4, 3, 2, 1]),
        ("List with duplicates", [4, 10, 3, 5, 1, 4, 3]),
        ("All identical elements", [8, 8, 8, 8]),
        ("Single element list", [33]),
        ("Empty list", []),
        ("Negative and positive numbers", [-9, 14, -2, 0, 6, -1])
    ]

    for label, data in test_cases:
        sorted_data = heap_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")


if __name__ == "__main__":
    demonstrate()

