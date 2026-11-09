"""
Program 07: Radix Sort (LSD)
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements Least Significant Digit (LSD) Radix Sort:
- Non-comparative sorting algorithm for non-negative integers.
- Processes individual digits starting from the least significant digit (1s place)
  to the most significant digit (10s, 100s, ... places).
- Uses Counting Sort as a stable intermediate subroutine to sort digits.
- Explicitly validates non-negative integers and rejects negative values with a clear error.
- Fully manual implementation without using built-in sorted() or .sort().
"""

from typing import Any, List


def _counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """
    Stable counting sort subroutine that sorts arr based on the digit represented by exp.

    Args:
        arr: List of non-negative integers.
        exp: Current digit place (1 for 1s, 10 for 10s, 100 for 100s, etc.).

    Returns:
        Sorted list based on the specified digit position.
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # Base 10 decimal digits: 0 to 9

    # Store count of occurrences of each digit at place 'exp'
    for val in arr:
        digit = (val // exp) % 10
        count[digit] += 1

    # Change count[i] so that count[i] contains actual position of digit in output
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array in reverse order to ensure stability
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    return output


def radix_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of non-negative integers in ascending order using LSD Radix Sort.

    Algorithm Explanation:
        1. Validate inputs: ensure all elements are non-negative integers.
        2. Find the maximum element in arr to determine the number of digits (d).
        3. Do counting sort for every digit position: exp = 1, 10, 100, ... up to max_val.
        4. Because Counting Sort is stable, relative order from previous digit passes
           is strictly preserved, resulting in a fully sorted array after the most
           significant digit pass.

    Time Complexity:
        - Best Case: O(d * (n + b))
        - Average Case: O(d * (n + b))
        - Worst Case: O(d * (n + b))
        where n is number of elements, d is number of digits in maximum value,
        and b is the radix base (b = 10 for decimal numbers).

    Auxiliary Space Complexity:
        - O(n + b) for the intermediate count array and output buffer.

    Args:
        arr: List of non-negative integers to sort.

    Returns:
        A new list containing the sorted integers.

    Raises:
        TypeError: If input is not a list of integers.
        ValueError: If any negative integer is encountered.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a Python list.")

    if len(arr) <= 1:
        # Validate elements even for single-element lists
        for val in arr:
            if not isinstance(val, int):
                raise TypeError(f"All elements must be integers. Found {type(val).__name__}.")
            if val < 0:
                raise ValueError(
                    f"Radix Sort requires non-negative integers. Negative value found: {val}."
                )
        return list(arr)

    # Validate that all elements are non-negative integers
    for val in arr:
        if not isinstance(val, int):
            raise TypeError(f"All elements must be integers. Found {type(val).__name__}.")
        if val < 0:
            raise ValueError(
                f"Radix Sort requires non-negative integers. Negative value found: {val}."
            )

    # Find the maximum number to know number of digits
    max_val = max(arr)

    # Do counting sort for every digit. exp is 10^i where i is current digit number
    result = list(arr)
    exp = 1
    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp)
        exp *= 10

    return result


def demonstrate() -> None:
    """Demonstrates Radix Sort with various test cases including validation."""
    print("=" * 60)
    print("DEMONSTRATION: Radix Sort (Program 07)")
    print("=" * 60)

    test_cases = [
        ("Normal non-negative list", [170, 45, 75, 90, 802, 24, 2, 66]),
        ("Already sorted list", [1, 2, 3, 4, 5]),
        ("Reverse sorted list", [50, 40, 30, 20, 10]),
        ("List with duplicates and single digits", [4, 2, 4, 3, 1, 2, 0]),
        ("List containing zero", [0, 5, 0, 100, 25, 0]),
        ("All identical elements", [111, 111, 111]),
        ("Single element list", [42]),
        ("Empty list", [])
    ]

    for label, data in test_cases:
        sorted_data = radix_sort(data)
        print(f"\nCase: {label}")
        print(f"  Original : {data}")
        print(f"  Sorted   : {sorted_data}")

    # Boundary test: Reject negative numbers
    print("\nCase: Negative value validation (Expected ValueError)")
    try:
        radix_sort([10, -5, 20])
        print("  Error: Failed to catch negative value!")
    except ValueError as err:
        print(f"  Successfully caught invalid input: {err}")


if __name__ == "__main__":
    demonstrate()

