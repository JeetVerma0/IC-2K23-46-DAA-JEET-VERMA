#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 5: Queues
Program 4: Double-Ended Queue (Deque) using Circular Array

Author: Student Implementation
Course: IC-307D — DSA Lab (CO1)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Double-Ended Queue (Deque, pronounced "deck") is a generalized linear data
structure in which elements can be inserted and deleted from both ends:
  - Front end: insert_front(), delete_front()
  - Rear end:  insert_rear(),  delete_rear()

A Deque can function as:
  1. A FIFO Queue: insert_rear() + delete_front()
  2. A LIFO Stack: insert_front() + delete_front() OR insert_rear() + delete_rear()
  3. A general sliding window or bidirectional buffer

CIRCULAR ARRAY IMPLEMENTATION:
Using a fixed-capacity linear array leads to unusable capacity when pointers
drift forward. A circular array wraps pointers using modulo arithmetic:
  - Front insertion moves counter-clockwise: front = (front - 1 + capacity) % capacity
  - Front deletion moves clockwise:          front = (front + 1) % capacity
  - Rear insertion moves clockwise:          rear  = (rear + 1) % capacity
  - Rear deletion moves counter-clockwise:   rear  = (rear - 1 + capacity) % capacity

COMPLEXITIES:
  - insert_front / insert_rear : O(1) time, O(1) auxiliary space
  - delete_front / delete_rear : O(1) time, O(1) auxiliary space
  - peek_front / peek_rear     : O(1) time, O(1) auxiliary space
  - display                    : O(n) time
  - Total Space                : O(capacity) fixed space
================================================================================
"""

import sys
from typing import Any, List, Optional


class Deque:
    """
    Fixed-capacity double-ended queue implemented over a circular array.
    """

    def __init__(self, capacity: int) -> None:
        """
        Initialize the Deque with a fixed maximum capacity.

        Args:
            capacity: Maximum number of elements the deque can hold (must be >= 1).
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer greater than zero.")

        self._capacity: int = capacity
        self._data: List[Optional[Any]] = [None] * capacity
        self._front: int = -1
        self._rear: int = -1
        self._count: int = 0

    @property
    def capacity(self) -> int:
        """Return the maximum capacity of the deque."""
        return self._capacity

    def is_empty(self) -> bool:
        """Return True if the deque contains no elements, False otherwise."""
        return self._count == 0

    def is_full(self) -> bool:
        """Return True if the deque has reached maximum capacity, False otherwise."""
        return self._count == self._capacity

    def size(self) -> int:
        """Return current number of elements stored in the deque."""
        return self._count

    def insert_front(self, item: Any) -> None:
        """
        Insert an element at the front of the deque.

        Algorithm:
          1. Check for overflow (is_full()). If full, raise OverflowError.
          2. If queue is empty: front = rear = 0.
          3. Otherwise: front = (front - 1 + capacity) % capacity.
          4. Store item at data[front].
          5. Increment count.
        """
        if self.is_full():
            raise OverflowError(
                f"Deque Overflow: Cannot insert_front '{item}'. Deque is full (Capacity: {self._capacity})."
            )

        if self.is_empty():
            self._front = 0
            self._rear = 0
        else:
            self._front = (self._front - 1 + self._capacity) % self._capacity

        self._data[self._front] = item
        self._count += 1

    def insert_rear(self, item: Any) -> None:
        """
        Insert an element at the rear of the deque.

        Algorithm:
          1. Check for overflow (is_full()). If full, raise OverflowError.
          2. If queue is empty: front = rear = 0.
          3. Otherwise: rear = (rear + 1) % capacity.
          4. Store item at data[rear].
          5. Increment count.
        """
        if self.is_full():
            raise OverflowError(
                f"Deque Overflow: Cannot insert_rear '{item}'. Deque is full (Capacity: {self._capacity})."
            )

        if self.is_empty():
            self._front = 0
            self._rear = 0
        else:
            self._rear = (self._rear + 1) % self._capacity

        self._data[self._rear] = item
        self._count += 1

    def delete_front(self) -> Any:
        """
        Remove and return the element at the front of the deque.

        Algorithm:
          1. Check for underflow (is_empty()). If empty, raise IndexError.
          2. Retrieve item = data[front]; set data[front] = None.
          3. If count == 1 (deque becomes empty): front = rear = -1.
          4. Otherwise: front = (front + 1) % capacity.
          5. Decrement count; return item.
        """
        if self.is_empty():
            raise IndexError("Deque Underflow: Cannot delete_front from an empty deque.")

        item = self._data[self._front]
        self._data[self._front] = None
        self._count -= 1

        if self._count == 0:
            self._front = -1
            self._rear = -1
        else:
            self._front = (self._front + 1) % self._capacity

        return item

    def delete_rear(self) -> Any:
        """
        Remove and return the element at the rear of the deque.

        Algorithm:
          1. Check for underflow (is_empty()). If empty, raise IndexError.
          2. Retrieve item = data[rear]; set data[rear] = None.
          3. If count == 1 (deque becomes empty): front = rear = -1.
          4. Otherwise: rear = (rear - 1 + capacity) % capacity.
          5. Decrement count; return item.
        """
        if self.is_empty():
            raise IndexError("Deque Underflow: Cannot delete_rear from an empty deque.")

        item = self._data[self._rear]
        self._data[self._rear] = None
        self._count -= 1

        if self._count == 0:
            self._front = -1
            self._rear = -1
        else:
            self._rear = (self._rear - 1 + self._capacity) % self._capacity

        return item

    def peek_front(self) -> Any:
        """Return the front element without removing it."""
        if self.is_empty():
            raise IndexError("Deque is empty: No front element to peek.")
        return self._data[self._front]

    def peek_rear(self) -> Any:
        """Return the rear element without removing it."""
        if self.is_empty():
            raise IndexError("Deque is empty: No rear element to peek.")
        return self._data[self._rear]

    def to_list(self) -> List[Any]:
        """Return elements ordered from front to rear as a Python list."""
        if self.is_empty():
            return []
        items = []
        idx = self._front
        for _ in range(self._count):
            items.append(self._data[idx])
            idx = (idx + 1) % self._capacity
        return items

    def display(self) -> None:
        """Display the logical contents and internal circular slot layout."""
        if self.is_empty():
            print("  Deque Status: [EMPTY]")
            print(f"  Pointers: front={self._front}, rear={self._rear}, size=0/{self._capacity}")
            return

        items = self.to_list()
        items_str = " <-> ".join(str(x) for x in items)
        print(f"  Logical Order (FRONT -> REAR): [FRONT] {items_str} [REAR]")
        print(f"  Pointers: front={self._front}, rear={self._rear}, size={self._count}/{self._capacity}")

        slots = []
        for i in range(self._capacity):
            val = self._data[i]
            markers = []
            if i == self._front:
                markers.append("F")
            if i == self._rear:
                markers.append("R")
            tag = f"({','.join(markers)})" if markers else ""
            slots.append(f"[{i}]: {val}{tag}")
        print(f"  Physical Array: {' | '.join(slots)}")


def run_tests() -> None:
    """Automated unit verification test suite for Deque."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Circular Array Deque")
    print("=" * 70)

    # Test 1: Initialization & state
    dq = Deque(5)
    assert dq.is_empty() is True
    assert dq.is_full() is False
    assert dq.size() == 0
    print("[PASS] Test 1: Initial state verified.")

    # Test 2: Insert rear & delete front (standard FIFO behavior)
    dq.insert_rear(10)
    dq.insert_rear(20)
    dq.insert_rear(30)
    assert dq.size() == 3
    assert dq.peek_front() == 10
    assert dq.peek_rear() == 30
    assert dq.to_list() == [10, 20, 30]
    assert dq.delete_front() == 10
    assert dq.delete_front() == 20
    assert dq.to_list() == [30]
    print("[PASS] Test 2: Standard FIFO queue operations verified.")

    # Test 3: Insert front & delete rear (bidirectional capability)
    dq.insert_front(99)
    dq.insert_front(88)
    # List is now [88, 99, 30]
    assert dq.to_list() == [88, 99, 30]
    assert dq.peek_front() == 88
    assert dq.peek_rear() == 30
    assert dq.delete_rear() == 30
    assert dq.delete_rear() == 99
    assert dq.delete_rear() == 88
    assert dq.is_empty() is True
    print("[PASS] Test 3: Bidirectional front/rear additions & removals verified.")

    # Test 4: Full capacity & wraparound
    dq = Deque(4)
    dq.insert_rear("A")
    dq.insert_rear("B")
    dq.insert_rear("C")
    dq.insert_rear("D")
    assert dq.is_full() is True
    try:
        dq.insert_rear("Overflow")
        assert False, "Failed to raise OverflowError on insert_rear"
    except OverflowError:
        pass
    try:
        dq.insert_front("Overflow")
        assert False, "Failed to raise OverflowError on insert_front"
    except OverflowError:
        pass
    print("[PASS] Test 4: Capacity limit & Overflow handling verified.")

    # Test 5: Circular wraparound across edges
    # Delete 2 from front: "A", "B" removed -> slots 0, 1 free; items "C", "D" at slots 2, 3
    assert dq.delete_front() == "A"
    assert dq.delete_front() == "B"
    # Insert at rear wraps to slot 0:
    dq.insert_rear("E")
    # Insert at front wraps to slot 1:
    dq.insert_front("Z")
    # Logical order should be: Z, C, D, E
    assert dq.to_list() == ["Z", "C", "D", "E"]
    assert dq.is_full() is True
    print("[PASS] Test 5: Circular modular wraparound verified.")

    # Test 6: Underflow on empty deque
    empty_dq = Deque(3)
    try:
        empty_dq.delete_front()
        assert False, "Should raise IndexError on empty delete_front"
    except IndexError:
        pass
    try:
        empty_dq.delete_rear()
        assert False, "Should raise IndexError on empty delete_rear"
    except IndexError:
        pass
    print("[PASS] Test 6: Underflow handling verified.")

    print("\nALL 6 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu options."""
    print("\n" + "=" * 45)
    print("      DOUBLE-ENDED QUEUE (DEQUE) MENU")
    print("=" * 45)
    print(" 1. Insert Front")
    print(" 2. Insert Rear")
    print(" 3. Delete Front")
    print(" 4. Delete Rear")
    print(" 5. Peek Front")
    print(" 6. Peek Rear")
    print(" 7. Display Deque Status")
    print(" 8. Check Is Empty / Is Full")
    print(" 9. Exit")
    print("=" * 45)


def main() -> None:
    """Main function supporting CLI interaction and automated testing."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 5 — Double-Ended Queue (Deque) Demo")
    print("==========================================================")

    while True:
        try:
            cap_input = input("Enter Deque capacity (positive integer): ").strip()
            capacity = int(cap_input)
            if capacity <= 0:
                print("Error: Capacity must be greater than zero.")
                continue
            deque = Deque(capacity)
            break
        except ValueError:
            print("Invalid input! Please enter a valid positive integer.")

    while True:
        print_menu()
        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            val = input("Enter element to insert at front: ").strip()
            try:
                deque.insert_front(val)
                print(f"Successfully inserted '{val}' at the FRONT.")
            except OverflowError as err:
                print(f"Error: {err}")

        elif choice == "2":
            val = input("Enter element to insert at rear: ").strip()
            try:
                deque.insert_rear(val)
                print(f"Successfully inserted '{val}' at the REAR.")
            except OverflowError as err:
                print(f"Error: {err}")

        elif choice == "3":
            try:
                item = deque.delete_front()
                print(f"Deleted from FRONT: {item}")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "4":
            try:
                item = deque.delete_rear()
                print(f"Deleted from REAR: {item}")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "5":
            try:
                item = deque.peek_front()
                print(f"Front element: {item}")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "6":
            try:
                item = deque.peek_rear()
                print(f"Rear element: {item}")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "7":
            print("\nDeque Details:")
            deque.display()

        elif choice == "8":
            print(f"Is Empty: {deque.is_empty()}")
            print(f"Is Full:  {deque.is_full()}")
            print(f"Current Size: {deque.size()} / {deque.capacity}")

        elif choice == "9":
            print("Exiting Deque Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 9.")


if __name__ == "__main__":
    main()

