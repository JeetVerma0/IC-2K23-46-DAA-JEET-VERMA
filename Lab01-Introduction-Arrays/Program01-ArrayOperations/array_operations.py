"""
Program 01: 1D Array Operations
Course: IC-307D Data Structures and Algorithms Lab
Unit 1: Introduction to Data Structures & Arrays (CO1)

This program demonstrates fundamental 1D array-like operations using Python lists:
1. Array creation and formatted display.
2. Insertion at a specified index with manual right-shifting of elements.
3. Deletion at a specified index with manual left-shifting of elements.
4. Linear search for locating elements.
5. In-place left rotation by k positions.
6. In-place right rotation by k positions.
7. Robust error handling for empty arrays and boundary / invalid indices.
8. Interactive menu-driven interface and automated self-tests.
"""

import sys
from typing import Any, List, Optional


# ---------------------------------------------------------------------------
# Core Array Operations
# ---------------------------------------------------------------------------

def display_array(arr: List[Any], name: str = "Array") -> None:
    """
    Displays the contents of an array along with its indices and length.

    Time Complexity: O(n) where n is the number of elements.
    Space Complexity: O(1) auxiliary space.

    Args:
        arr: The list representing the array.
        name: A descriptive label for display.
    """
    if not arr:
        print(f"\n{name} is EMPTY: [] (length = 0)")
        return

    print(f"\n{name} (length = {len(arr)}):")
    # Print indices row
    idx_str = "Index:   " + "\t".join(f"[{i}]" for i in range(len(arr)))
    # Print values row
    val_str = "Value:   " + "\t".join(str(val) for val in arr)
    divider = "-" * max(len(idx_str), len(val_str), 30)

    print(divider)
    print(idx_str)
    print(val_str)
    print(divider)


def insert_element(arr: List[Any], element: Any, position: int) -> None:
    """
    Inserts an element at a specified position in the array.

    Concept Explanation:
        In contiguous memory arrays, inserting at index 'k' requires shifting all
        elements from index 'k' through 'n-1' one position to the right to make
        room for the new element. We manually demonstrate this shifting process
        instead of relying purely on high-level list methods.

    Algorithm:
        1. Validate position: 0 <= position <= len(arr).
        2. Append a placeholder (None) at the end to expand size by 1.
        3. Shift elements: for i from len(arr) - 1 down to position + 1:
               arr[i] = arr[i - 1]
        4. Place the new element: arr[position] = element.

    Time Complexity:
        - Best Case (insert at end): O(1)
        - Worst/Average Case (insert at index 0 or middle): O(n) due to shifting.
    Space Complexity:
        - O(1) auxiliary space.

    Args:
        arr: The array (list) to modify in-place.
        element: The value to insert.
        position: The index at which to insert (0 <= position <= len(arr)).

    Raises:
        IndexError: If position is outside [0, len(arr)].
    """
    n = len(arr)
    if position < 0 or position > n:
        raise IndexError(
            f"Invalid insert position {position}. Valid range is [0, {n}]."
        )

    # Step 1: Expand array size by one slot
    arr.append(None)

    # Step 2: Shift existing elements rightward to create a vacant slot at 'position'
    for i in range(len(arr) - 1, position, -1):
        arr[i] = arr[i - 1]

    # Step 3: Insert the target element into the vacant position
    arr[position] = element


def delete_element(arr: List[Any], position: int) -> Any:
    """
    Deletes the element at a specified position from the array and returns it.

    Concept Explanation:
        In contiguous memory arrays, deleting an element at index 'k' leaves a gap.
        To maintain contiguity without empty holes, all elements from index 'k+1'
        up to 'n-1' must be shifted one position to the left. Finally, the last
        duplicate slot is removed.

    Algorithm:
        1. Check if array is empty (raise IndexError).
        2. Validate position: 0 <= position < len(arr).
        3. Save the target value: deleted_val = arr[position].
        4. Shift elements leftward: for i from position to len(arr) - 2:
               arr[i] = arr[i + 1]
        5. Truncate the redundant last slot using pop().

    Time Complexity:
        - Best Case (delete from end): O(1)
        - Worst/Average Case (delete from index 0 or middle): O(n) due to shifting.
    Space Complexity:
        - O(1) auxiliary space.

    Args:
        arr: The array (list) to modify in-place.
        position: The index of the element to delete (0 <= position < len(arr)).

    Returns:
        The deleted element.

    Raises:
        IndexError: If array is empty or position is outside [0, len(arr) - 1].
    """
    if not arr:
        raise IndexError("Cannot delete from an empty array.")

    n = len(arr)
    if position < 0 or position >= n:
        raise IndexError(
            f"Invalid delete position {position}. Valid range is [0, {n - 1}]."
        )

    deleted_val = arr[position]

    # Shift elements from right to left over the deleted element
    for i in range(position, n - 1):
        arr[i] = arr[i + 1]

    # Remove the redundant trailing element
    arr.pop()

    return deleted_val


def linear_search(arr: List[Any], target: Any) -> List[int]:
    """
    Searches for target in the array sequentially and returns all matching indices.

    Algorithm:
        Traverse from index 0 to len(arr) - 1. Compare each element with target.

    Time Complexity:
        - Best Case (found at index 0): O(1)
        - Worst/Average Case: O(n) linear scan across all elements.
    Space Complexity:
        - O(k) where k is the number of occurrences found.

    Args:
        arr: The array to search.
        target: The value to search for.

    Returns:
        A list of integer indices where target is present. Empty list if not found.
    """
    matches: List[int] = []
    for idx, val in enumerate(arr):
        if val == target:
            matches.append(idx)
    return matches


def reverse_subarray(arr: List[Any], start: int, end: int) -> None:
    """
    Helper function to reverse a segment of an array in-place between start and end.

    Time Complexity: O(end - start + 1)
    Space Complexity: O(1) auxiliary space.
    """
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1


def rotate_left(arr: List[Any], k: int) -> None:
    """
    Rotates the array to the left by k positions in-place using the Reversal Algorithm.

    Reversal Algorithm Principle:
        To rotate an array of length n left by k positions:
        1. Normalize k: k = k % n (handles k >= n and negative rotations).
        2. If k == 0 or n <= 1, no rotation needed.
        3. Reverse first k elements: arr[0 ... k-1]
        4. Reverse remaining n-k elements: arr[k ... n-1]
        5. Reverse entire array: arr[0 ... n-1]

        Example: arr = [1, 2, 3, 4, 5], k = 2
            Step 1: Reverse [1, 2] -> [2, 1, 3, 4, 5]
            Step 2: Reverse [3, 4, 5] -> [2, 1, 5, 4, 3]
            Step 3: Reverse all -> [3, 4, 5, 1, 2] (Correct left rotation by 2)

    Time Complexity: O(n) - 3 reversals touching elements at most twice.
    Space Complexity: O(1) auxiliary space (in-place).

    Args:
        arr: The array to rotate.
        k: Number of positions to rotate left (can be >= n or negative).
    """
    n = len(arr)
    if n <= 1:
        return

    # Normalize rotation count
    k = k % n
    if k == 0:
        return

    reverse_subarray(arr, 0, k - 1)
    reverse_subarray(arr, k, n - 1)
    reverse_subarray(arr, 0, n - 1)


def rotate_right(arr: List[Any], k: int) -> None:
    """
    Rotates the array to the right by k positions in-place using the Reversal Algorithm.

    Reversal Algorithm Principle:
        To rotate an array of length n right by k positions:
        1. Normalize k: k = k % n.
        2. If k == 0 or n <= 1, no rotation needed.
        3. Reverse entire array: arr[0 ... n-1]
        4. Reverse first k elements: arr[0 ... k-1]
        5. Reverse remaining n-k elements: arr[k ... n-1]

        Example: arr = [1, 2, 3, 4, 5], k = 2
            Step 1: Reverse all -> [5, 4, 3, 2, 1]
            Step 2: Reverse [5, 4] -> [4, 5, 3, 2, 1]
            Step 3: Reverse [3, 2, 1] -> [4, 5, 1, 2, 3] (Correct right rotation by 2)

    Time Complexity: O(n)
    Space Complexity: O(1) auxiliary space (in-place).

    Args:
        arr: The array to rotate.
        k: Number of positions to rotate right.
    """
    n = len(arr)
    if n <= 1:
        return

    # Normalize rotation count
    k = k % n
    if k == 0:
        return

    reverse_subarray(arr, 0, n - 1)
    reverse_subarray(arr, 0, k - 1)
    reverse_subarray(arr, k, n - 1)


# ---------------------------------------------------------------------------
# Built-in Self-Tests
# ---------------------------------------------------------------------------

def run_self_tests() -> None:
    """
    Executes automated test cases covering normal, boundary, and error scenarios.
    """
    print("\n==========================================")
    print("Running Self-Tests for Program 1 (1D Arrays)")
    print("==========================================")

    # 1. Insertion Tests
    test_arr: List[int] = []
    print("\n[Test 1] Insert into empty array at index 0:")
    insert_element(test_arr, 10, 0)
    assert test_arr == [10], f"Expected [10], got {test_arr}"
    print("  Passed: [10]")

    print("[Test 2] Insert at beginning (index 0):")
    insert_element(test_arr, 5, 0)
    assert test_arr == [5, 10], f"Expected [5, 10], got {test_arr}"
    print("  Passed: [5, 10]")

    print("[Test 3] Insert at end (index len):")
    insert_element(test_arr, 20, len(test_arr))
    assert test_arr == [5, 10, 20], f"Expected [5, 10, 20], got {test_arr}"
    print("  Passed: [5, 10, 20]")

    print("[Test 4] Insert in the middle (index 1):")
    insert_element(test_arr, 8, 1)
    assert test_arr == [5, 8, 10, 20], f"Expected [5, 8, 10, 20], got {test_arr}"
    print("  Passed: [5, 8, 10, 20]")

    print("[Test 5] Invalid insert positions (boundary check):")
    try:
        insert_element(test_arr, 99, -1)
        assert False, "Should have raised IndexError for negative index"
    except IndexError:
        print("  Passed: Negative index caught")

    try:
        insert_element(test_arr, 99, 100)
        assert False, "Should have raised IndexError for out-of-bounds index"
    except IndexError:
        print("  Passed: Out-of-bounds index caught")

    # 2. Deletion Tests
    print("\n[Test 6] Delete from middle:")
    removed = delete_element(test_arr, 1)
    assert removed == 8 and test_arr == [5, 10, 20], f"Failed: {test_arr}"
    print(f"  Passed: Deleted {removed}, remaining: {test_arr}")

    print("[Test 7] Delete from beginning (index 0):")
    removed = delete_element(test_arr, 0)
    assert removed == 5 and test_arr == [10, 20], f"Failed: {test_arr}"
    print(f"  Passed: Deleted {removed}, remaining: {test_arr}")

    print("[Test 8] Delete from end:")
    removed = delete_element(test_arr, len(test_arr) - 1)
    assert removed == 20 and test_arr == [10], f"Failed: {test_arr}"
    print(f"  Passed: Deleted {removed}, remaining: {test_arr}")

    print("[Test 9] Delete the last remaining element:")
    removed = delete_element(test_arr, 0)
    assert removed == 10 and test_arr == [], f"Failed: {test_arr}"
    print(f"  Passed: Deleted {removed}, remaining is empty: {test_arr}")

    print("[Test 10] Delete from empty array:")
    try:
        delete_element(test_arr, 0)
        assert False, "Should have raised IndexError for empty array deletion"
    except IndexError:
        print("  Passed: Deletion from empty array rejected")

    # 3. Linear Search Tests
    print("\n[Test 11] Linear search for existing and missing elements:")
    search_arr = [10, 25, 30, 25, 50]
    indices = linear_search(search_arr, 25)
    assert indices == [1, 3], f"Expected [1, 3], got {indices}"
    print(f"  Passed: Search 25 -> positions {indices}")

    missing = linear_search(search_arr, 999)
    assert missing == [], f"Expected [], got {missing}"
    print(f"  Passed: Search 999 (missing) -> {missing}")

    empty_search = linear_search([], 10)
    assert empty_search == [], f"Expected [], got {empty_search}"
    print("  Passed: Search in empty array -> []")

    # 4. Rotation Tests
    print("\n[Test 12] Left rotation:")
    rot_arr = [1, 2, 3, 4, 5]
    rotate_left(rot_arr, 2)
    assert rot_arr == [3, 4, 5, 1, 2], f"Expected [3, 4, 5, 1, 2], got {rot_arr}"
    print(f"  Passed: [1,2,3,4,5] left rotated by 2 -> {rot_arr}")

    print("[Test 13] Right rotation:")
    rot_arr2 = [1, 2, 3, 4, 5]
    rotate_right(rot_arr2, 2)
    assert rot_arr2 == [4, 5, 1, 2, 3], f"Expected [4, 5, 1, 2, 3], got {rot_arr2}"
    print(f"  Passed: [1,2,3,4,5] right rotated by 2 -> {rot_arr2}")

    print("[Test 14] Rotation boundary cases (k=0, k=len, k > len):")
    rot_arr3 = [1, 2, 3]
    rotate_left(rot_arr3, 0)
    assert rot_arr3 == [1, 2, 3], f"Expected [1, 2, 3], got {rot_arr3}"
    print("  Passed: Rotate by 0 leaves array unchanged")

    rotate_left(rot_arr3, 3)
    assert rot_arr3 == [1, 2, 3], f"Expected [1, 2, 3], got {rot_arr3}"
    print("  Passed: Rotate by length leaves array unchanged")

    rotate_left(rot_arr3, 7)  # 7 % 3 = 1 -> [2, 3, 1]
    assert rot_arr3 == [2, 3, 1], f"Expected [2, 3, 1], got {rot_arr3}"
    print("  Passed: Rotate by 7 (k > len) left rotated correctly -> [2, 3, 1]")

    # Empty array rotation
    empty_arr: List[int] = []
    rotate_left(empty_arr, 3)
    rotate_right(empty_arr, 3)
    assert empty_arr == [], "Empty array rotation should not fail"
    print("  Passed: Rotation on empty array handled cleanly")

    print("\nAll Program 1 self-tests PASSED successfully!")


# ---------------------------------------------------------------------------
# Menu-Driven User Interface
# ---------------------------------------------------------------------------

def parse_element_input(val_str: str) -> Any:
    """Helper to convert string input to int or float if possible, else keep string."""
    val_str = val_str.strip()
    try:
        return int(val_str)
    except ValueError:
        try:
            return float(val_str)
        except ValueError:
            return val_str


def main() -> None:
    """Main interactive driver for Program 1."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_self_tests()
        sys.exit(0)

    array: List[Any] = []

    menu = """
========================================
     1D ARRAY OPERATIONS MENU (CO1)
========================================
1. Create / Reinitialize Array
2. Display Array
3. Insert Element (with manual shifting)
4. Delete Element (with manual shifting)
5. Search Element (Linear Search)
6. Rotate Array Left (by k positions)
7. Rotate Array Right (by k positions)
8. Run Automated Self-Tests
9. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            raw = input("Enter space-separated elements (or press Enter for empty): ")
            tokens = raw.strip().split()
            array = [parse_element_input(t) for t in tokens]
            print(f"Array created successfully with {len(array)} element(s).")
            display_array(array)

        elif choice == "2":
            display_array(array)

        elif choice == "3":
            display_array(array)
            val_input = input("Enter element to insert: ")
            elem = parse_element_input(val_input)
            pos_input = input(f"Enter position [0 to {len(array)}]: ").strip()
            try:
                pos = int(pos_input)
                insert_element(array, elem, pos)
                print(f"Successfully inserted '{elem}' at position {pos}.")
                display_array(array)
            except ValueError:
                print("Error: Position must be an integer.")
            except IndexError as err:
                print(f"Index Error: {err}")

        elif choice == "4":
            if not array:
                print("Error: Array is currently empty. Cannot delete.")
                continue
            display_array(array)
            pos_input = input(f"Enter position to delete [0 to {len(array) - 1}]: ").strip()
            try:
                pos = int(pos_input)
                removed = delete_element(array, pos)
                print(f"Successfully deleted element '{removed}' from position {pos}.")
                display_array(array)
            except ValueError:
                print("Error: Position must be an integer.")
            except IndexError as err:
                print(f"Index Error: {err}")

        elif choice == "5":
            if not array:
                print("Warning: Array is empty.")
            target_input = input("Enter element to search for: ")
            target = parse_element_input(target_input)
            indices = linear_search(array, target)
            if indices:
                print(f"Element '{target}' found at index/indices: {indices}")
            else:
                print(f"Element '{target}' was NOT found in the array.")

        elif choice == "6":
            if not array:
                print("Array is empty. Nothing to rotate.")
                continue
            k_input = input("Enter number of positions to rotate left: ").strip()
            try:
                k = int(k_input)
                rotate_left(array, k)
                print(f"Array rotated left by {k} position(s).")
                display_array(array)
            except ValueError:
                print("Error: Rotation count must be an integer.")

        elif choice == "7":
            if not array:
                print("Array is empty. Nothing to rotate.")
                continue
            k_input = input("Enter number of positions to rotate right: ").strip()
            try:
                k = int(k_input)
                rotate_right(array, k)
                print(f"Array rotated right by {k} position(s).")
                display_array(array)
            except ValueError:
                print("Error: Rotation count must be an integer.")

        elif choice == "8":
            run_self_tests()

        elif choice == "9":
            print("Exiting 1D Array Operations. Goodbye!")
            break

        else:
            print("Invalid choice! Please select a valid option (1-9).")


if __name__ == "__main__":
    main()

