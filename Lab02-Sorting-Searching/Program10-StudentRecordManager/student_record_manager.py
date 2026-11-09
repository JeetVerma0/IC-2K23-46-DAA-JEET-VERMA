"""
Program 10: Student Record Manager
Course: IC-307D Data Structures and Algorithms Lab
Unit 2: Sorting and Searching Algorithms (CO2)

This program implements an in-memory, menu-driven Student Record Management System:
- Each record consists of:
  1. Roll Number (integer, unique)
  2. Student Name (string)
  3. Academic Marks (float, 0.0 - 100.0)
- Core Features:
  - Add student record with duplicate roll number prevention and marks validation.
  - Display all records in a formatted tabular layout.
  - Sort records by Roll Number using Merge Sort (stable, ascending).
  - Sort records by Student Name using Quick Sort (alphabetical).
  - Sort records by Marks using Merge Sort (descending: rank order).
  - Search student by Roll Number using Binary Search (O(log n)) on roll-sorted data.
- Built-in self-tests and interactive console menu.
"""

import sys
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Custom Sorting Algorithms Adapted for Student Records
# ---------------------------------------------------------------------------

def merge_sort_records(
    records: List[Dict[str, Any]],
    key: Callable[[Dict[str, Any]], Any],
    reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Sorts a list of student record dictionaries using manual Merge Sort.

    Time Complexity: O(n log n)
    Auxiliary Space Complexity: O(n)
    """
    if len(records) <= 1:
        return list(records)

    mid = len(records) // 2
    left = merge_sort_records(records[:mid], key, reverse)
    right = merge_sort_records(records[mid:], key, reverse)

    merged: List[Dict[str, Any]] = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        val_left = key(left[i])
        val_right = key(right[j])

        condition = (val_left >= val_right) if reverse else (val_left <= val_right)
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len_left:
        merged.append(left[i])
        i += 1
    while j < len_right:
        merged.append(right[j])
        j += 1

    return merged


def quick_sort_records(
    records: List[Dict[str, Any]],
    key: Callable[[Dict[str, Any]], Any],
    reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Sorts student records using manual Quick Sort with middle pivot.

    Time Complexity: O(n log n) average
    Auxiliary Space Complexity: O(log n) call stack
    """
    if len(records) <= 1:
        return list(records)

    pivot_record = records[len(records) // 2]
    pivot_val = key(pivot_record)

    left: List[Dict[str, Any]] = []
    middle: List[Dict[str, Any]] = []
    right: List[Dict[str, Any]] = []

    for r in records:
        val = key(r)
        if val == pivot_val:
            middle.append(r)
        elif (val > pivot_val) if reverse else (val < pivot_val):
            left.append(r)
        else:
            right.append(r)

    return quick_sort_records(left, key, reverse) + middle + quick_sort_records(right, key, reverse)


# ---------------------------------------------------------------------------
# Binary Search on Student Records
# ---------------------------------------------------------------------------

def binary_search_by_roll(records: List[Dict[str, Any]], target_roll: int) -> Optional[Dict[str, Any]]:
    """
    Searches for a student by roll number using Binary Search.
    Precondition: 'records' must be sorted by roll number in ascending order.

    Time Complexity: O(log n)
    Auxiliary Space Complexity: O(1)

    Returns:
        The matching record dictionary if found, None otherwise.
    """
    low = 0
    high = len(records) - 1

    while low <= high:
        mid = low + (high - low) // 2
        current_roll = records[mid]["roll_no"]

        if current_roll == target_roll:
            return records[mid]
        elif current_roll < target_roll:
            low = mid + 1
        else:
            high = mid - 1

    return None


# ---------------------------------------------------------------------------
# Student Manager Logic
# ---------------------------------------------------------------------------

class StudentRecordManager:
    """Manages an in-memory repository of student records."""

    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def roll_number_exists(self, roll_no: int) -> bool:
        """Checks if a roll number is already assigned."""
        for r in self.records:
            if r["roll_no"] == roll_no:
                return True
        return False

    def add_record(self, roll_no: int, name: str, marks: float) -> None:
        """
        Validates and adds a new student record.

        Raises:
            ValueError: If roll number is non-positive or already exists,
                        or if name is empty, or if marks are not in [0.0, 100.0].
        """
        if not isinstance(roll_no, int) or roll_no <= 0:
            raise ValueError(f"Roll number must be a positive integer. Got: {roll_no}.")

        if self.roll_number_exists(roll_no):
            raise ValueError(f"Duplicate Error: Roll number {roll_no} already exists.")

        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Student name cannot be empty or purely whitespace.")

        if not isinstance(marks, (int, float)) or marks < 0.0 or marks > 100.0:
            raise ValueError(f"Marks must be a numeric value between 0.0 and 100.0. Got: {marks}.")

        record = {
            "roll_no": roll_no,
            "name": clean_name,
            "marks": round(float(marks), 2)
        }
        self.records.append(record)

    def display_records(self, custom_list: Optional[List[Dict[str, Any]]] = None, title: str = "Student Records") -> None:
        """Prints records in a formatted ASCII table."""
        data = custom_list if custom_list is not None else self.records

        if not data:
            print(f"\n{title}: No records found.")
            return

        print(f"\n{title} (Total: {len(data)})")
        divider = "+" + "-" * 12 + "+" + "-" * 26 + "+" + "-" * 10 + "+"
        print(divider)
        print(f"| {'Roll No':<10} | {'Student Name':<24} | {'Marks':<8} |")
        print(divider)
        for r in data:
            print(f"| {r['roll_no']:<10} | {r['name']:<24} | {r['marks']:<8.2f} |")
        print(divider)

    def sort_by_roll_no(self) -> List[Dict[str, Any]]:
        """Sorts records by roll number ascending using Merge Sort."""
        self.records = merge_sort_records(self.records, key=lambda r: r["roll_no"], reverse=False)
        return self.records

    def sort_by_name(self) -> List[Dict[str, Any]]:
        """Sorts records alphabetically by name using Quick Sort."""
        self.records = quick_sort_records(self.records, key=lambda r: r["name"].lower(), reverse=False)
        return self.records

    def sort_by_marks(self) -> List[Dict[str, Any]]:
        """Sorts records by marks descending (rank order) using Merge Sort."""
        self.records = merge_sort_records(self.records, key=lambda r: r["marks"], reverse=True)
        return self.records

    def search_by_roll_no(self, roll_no: int) -> Optional[Dict[str, Any]]:
        """
        Sorts records by roll number and uses Binary Search to find the student.
        """
        # Ensure list is sorted by roll number before executing binary search
        self.sort_by_roll_no()
        return binary_search_by_roll(self.records, roll_no)


# ---------------------------------------------------------------------------
# Built-in Self-Tests
# ---------------------------------------------------------------------------

def run_self_tests() -> None:
    """Verifies all StudentRecordManager functions, boundary cases, and validations."""
    print("=" * 60)
    print("RUNNING SELF-TESTS: Student Record Manager (Program 10)")
    print("=" * 60)

    mgr = StudentRecordManager()

    # 1. Add valid records
    mgr.add_record(103, "Charlie Davis", 88.5)
    mgr.add_record(101, "Alice Brown", 94.0)
    mgr.add_record(105, "Edward Green", 72.0)
    mgr.add_record(102, "Bob Adams", 85.0)
    mgr.add_record(104, "Diana Evans", 94.0)  # Duplicate marks test
    assert len(mgr.records) == 5
    print("  [Test 1 Passed] Added 5 valid student records.")

    # 2. Duplicate roll number validation
    try:
        mgr.add_record(101, "Duplicate Alice", 50.0)
        assert False, "Should raise ValueError for duplicate roll number"
    except ValueError as err:
        print(f"  [Test 2 Passed] Caught duplicate roll number: {err}")

    # 3. Invalid marks validation
    try:
        mgr.add_record(109, "Bad Marks", 105.0)
        assert False, "Should raise ValueError for marks > 100"
    except ValueError:
        print("  [Test 3 Passed] Caught invalid marks (>100.0).")

    try:
        mgr.add_record(110, "Negative Marks", -5.0)
        assert False, "Should raise ValueError for marks < 0"
    except ValueError:
        print("  [Test 3b Passed] Caught invalid marks (<0.0).")

    # 4. Sort by Roll Number (Merge Sort)
    mgr.sort_by_roll_no()
    rolls = [r["roll_no"] for r in mgr.records]
    assert rolls == [101, 102, 103, 104, 105], f"Expected sorted rolls, got {rolls}"
    print(f"  [Test 4 Passed] Sorted by Roll No: {rolls}")

    # 5. Sort by Name (Quick Sort)
    mgr.sort_by_name()
    names = [r["name"] for r in mgr.records]
    assert names == ["Alice Brown", "Bob Adams", "Charlie Davis", "Diana Evans", "Edward Green"]
    print(f"  [Test 5 Passed] Sorted alphabetically by Name: {names}")

    # 6. Sort by Marks Descending (Merge Sort)
    mgr.sort_by_marks()
    marks = [r["marks"] for r in mgr.records]
    assert marks[0] >= marks[1] >= marks[2] >= marks[3] >= marks[4]
    print(f"  [Test 6 Passed] Sorted by Marks descending: {marks}")

    # 7. Binary Search by Roll Number
    found = mgr.search_by_roll_no(103)
    assert found is not None and found["name"] == "Charlie Davis"
    print(f"  [Test 7 Passed] Binary search found student 103: {found}")

    missing = mgr.search_by_roll_no(999)
    assert missing is None
    print("  [Test 8 Passed] Binary search correctly returned None for missing student 999.")

    print("\nAll Program 10 self-tests PASSED successfully!")


# ---------------------------------------------------------------------------
# Interactive Menu
# ---------------------------------------------------------------------------

def main() -> None:
    """Interactive command-line driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_self_tests()
        sys.exit(0)

    mgr = StudentRecordManager()

    # Pre-populate initial sample records
    mgr.add_record(102, "Bob Smith", 82.5)
    mgr.add_record(101, "Alice Walker", 91.0)
    mgr.add_record(104, "David Miller", 78.0)
    mgr.add_record(103, "Catherine Reed", 95.5)

    menu = """
========================================
    STUDENT RECORD MANAGER (CO2)
========================================
1. Add New Student Record
2. Display All Student Records
3. Sort Records by Roll Number (Merge Sort)
4. Sort Records by Name (Quick Sort)
5. Sort Records by Marks (Merge Sort Descending)
6. Search Record by Roll Number (Binary Search)
7. Run Automated Self-Tests
8. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            try:
                r_in = int(input("Enter Roll Number (positive integer): ").strip())
                n_in = input("Enter Student Name: ").strip()
                m_in = float(input("Enter Marks (0.0 to 100.0): ").strip())
                mgr.add_record(r_in, n_in, m_in)
                print(f"Record for '{n_in}' (Roll {r_in}) added successfully.")
            except ValueError as err:
                print(f"Input Error: {err}")

        elif choice == "2":
            mgr.display_records()

        elif choice == "3":
            mgr.sort_by_roll_no()
            print("Records sorted by Roll Number (Ascending):")
            mgr.display_records()

        elif choice == "4":
            mgr.sort_by_name()
            print("Records sorted alphabetically by Name:")
            mgr.display_records()

        elif choice == "5":
            mgr.sort_by_marks()
            print("Records sorted by Marks (Descending Rank):")
            mgr.display_records()

        elif choice == "6":
            try:
                target = int(input("Enter Roll Number to search: ").strip())
                res = mgr.search_by_roll_no(target)
                if res:
                    print(f"\nStudent Found:")
                    print(f"  Roll No : {res['roll_no']}")
                    print(f"  Name    : {res['name']}")
                    print(f"  Marks   : {res['marks']}")
                else:
                    print(f"\nStudent with Roll Number {target} was NOT found.")
            except ValueError:
                print("Error: Roll number must be an integer.")

        elif choice == "7":
            run_self_tests()

        elif choice == "8":
            print("Exiting Student Record Manager. Goodbye!")
            break

        else:
            print("Invalid choice! Please select 1-8.")


if __name__ == "__main__":
    main()

