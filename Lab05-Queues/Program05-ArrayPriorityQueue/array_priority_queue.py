#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 5: Queues
Program 5: Priority Queue using Array (Sorted Array Implementation)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO1)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Priority Queue is an abstract data type where each element has an associated
priority. In a priority queue:
  1. An element with higher priority is dequeued before an element with lower priority.
  2. If two elements have equal priorities, they are served according to their
     order of arrival (FIFO stability).

PRIORITY CONVENTION:
  - Standard DSA convention: LOWER numeric value represents HIGHER priority.
    Example: Priority 1 (Emergency / Critical) > Priority 5 (Normal / Background).

ARRAY-BASED APPROACHES & TRADE-OFFS:
  1. Unordered Array:
     - insert: O(1) appending to array.
     - remove_highest_priority: O(n) linear search for the minimum priority element,
       then shifting remaining elements.
  2. Sorted / Ordered Array (Implemented here):
     - insert: O(n) linear scan to locate the correct sorted position preserving FIFO
       arrival sequence for identical priorities, then inserting the element.
     - peek: O(1) immediate access to index 0.
     - remove_highest_priority: O(n) removing index 0 (or O(1) if sorted descending).
       We maintain ascending order for clear front-to-rear display.

FIFO STABILITY:
To prevent starvation and guarantee fairness among equal-priority entries,
an internal monotonic arrival counter increments with each insertion:
  Tuple: (priority, arrival_counter, data)
When two items share the exact same numeric priority, the one with the smaller
arrival counter is placed first.

COMPLEXITY:
  - insert                  : O(n) time (search & shift), O(1) auxiliary space
  - remove_highest_priority : O(n) time (array shift)
  - peek                    : O(1) time
  - is_empty / is_full      : O(1) time
  - Total Space             : O(capacity) bounded space
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class PriorityQueueItem:
    """Represents a single entry in the Priority Queue."""

    def __init__(self, data: Any, priority: int, arrival_order: int) -> None:
        self.data: Any = data
        self.priority: int = priority
        self.arrival_order: int = arrival_order

    def __repr__(self) -> str:
        return f"Item(data={self.data!r}, priority={self.priority}, seq={self.arrival_order})"

    def __str__(self) -> str:
        return f"[Pri:{self.priority}, Seq:#{self.arrival_order}] {self.data}"


class ArrayPriorityQueue:
    """
    Priority Queue implemented using a bounded or dynamic array sorted by priority.
    Lower numeric value represents higher priority.
    Maintains FIFO order for elements with identical priority.
    """

    def __init__(self, capacity: Optional[int] = None) -> None:
        """
        Initialize the priority queue.

        Args:
            capacity: Maximum number of elements allowed (optional). If None, unbounded.
        """
        if capacity is not None and (not isinstance(capacity, int) or capacity <= 0):
            raise ValueError("Capacity must be a positive integer greater than zero.")

        self._capacity: Optional[int] = capacity
        self._items: List[PriorityQueueItem] = []
        self._counter: int = 0  # Monotonic arrival order sequence

    @property
    def capacity(self) -> Optional[int]:
        """Return the maximum capacity or None if unbounded."""
        return self._capacity

    def is_empty(self) -> bool:
        """Return True if the priority queue has no elements."""
        return len(self._items) == 0

    def is_full(self) -> bool:
        """Return True if the priority queue has reached maximum capacity."""
        if self._capacity is None:
            return False
        return len(self._items) >= self._capacity

    def size(self) -> int:
        """Return current number of items in the priority queue."""
        return len(self._items)

    def insert(self, data: Any, priority: int) -> None:
        """
        Insert an item with an assigned priority.

        Algorithm:
          1. Check for overflow if capacity is bounded.
          2. Create PriorityQueueItem(data, priority, self._counter).
          3. Increment arrival counter.
          4. Find sorted insertion index `idx` such that all preceding items
             have (priority < new_priority) or (priority == new_priority and seq < new_seq).
          5. Insert item at `idx`.
        """
        if not isinstance(priority, int):
            raise TypeError(f"Priority must be an integer, got {type(priority).__name__}.")

        if self.is_full():
            raise OverflowError(
                f"Priority Queue Overflow: Capacity limit ({self._capacity}) reached."
            )

        self._counter += 1
        new_item = PriorityQueueItem(data, priority, self._counter)

        # Find position to insert while maintaining ascending priority order
        # (lower priority value = higher precedence; earlier arrival = higher precedence)
        insert_idx = len(self._items)
        for i, item in enumerate(self._items):
            if priority < item.priority:
                insert_idx = i
                break
            elif priority == item.priority and self._counter < item.arrival_order:
                # Due to monotonic counter, new_item is always after existing items with equal priority
                insert_idx = i
                break

        self._items.insert(insert_idx, new_item)

    def remove_highest_priority(self) -> Any:
        """
        Remove and return the highest priority element (lowest priority number, earliest arrival).

        Algorithm:
          1. Check for underflow (is_empty()). If empty, raise IndexError.
          2. Pop element at index 0.
          3. Return item.data.
        """
        if self.is_empty():
            raise IndexError("Priority Queue Underflow: Cannot remove from an empty queue.")

        highest = self._items.pop(0)
        return highest.data

    def peek(self) -> Tuple[Any, int]:
        """
        Return (data, priority) of the highest priority element without removing it.
        """
        if self.is_empty():
            raise IndexError("Priority Queue is empty: No element to peek.")
        item = self._items[0]
        return item.data, item.priority

    def display(self) -> None:
        """Display the priority queue items ordered by priority and arrival sequence."""
        if self.is_empty():
            print("  Priority Queue: [EMPTY]")
            print(f"  Size: 0 / {self._capacity if self._capacity else 'Unbounded'}")
            return

        cap_str = str(self._capacity) if self._capacity else "Unbounded"
        print(f"  Priority Queue Items (Front=Highest Priority -> Rear=Lowest Priority):")
        print(f"  Capacity: {cap_str} | Current Size: {len(self._items)}")
        for idx, item in enumerate(self._items):
            tag = " <-- [FRONT / HIGHEST PRIORITY]" if idx == 0 else ""
            print(f"    [{idx}] Priority: {item.priority:2d} | Seq: #{item.arrival_order:2d} | Value: {item.data}{tag}")

    def to_list(self) -> List[Tuple[Any, int]]:
        """Return list of (data, priority) ordered from highest to lowest priority."""
        return [(item.data, item.priority) for item in self._items]


def run_tests() -> None:
    """Automated unit verification test suite for Array Priority Queue."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Array Priority Queue")
    print("=" * 70)

    # Test 1: Initialization
    pq = ArrayPriorityQueue(capacity=5)
    assert pq.is_empty() is True
    assert pq.is_full() is False
    assert pq.size() == 0
    print("[PASS] Test 1: Initial state verified.")

    # Test 2: Priority ordering (lower number = higher priority)
    pq.insert("Task C", priority=3)
    pq.insert("Task A", priority=1)
    pq.insert("Task B", priority=2)
    assert pq.size() == 3
    assert pq.peek() == ("Task A", 1)
    assert pq.to_list() == [("Task A", 1), ("Task B", 2), ("Task C", 3)]
    print("[PASS] Test 2: Priority ordering verified.")

    # Test 3: FIFO stability for equal priorities
    pq.insert("Task A-2", priority=1)  # Same priority as Task A
    pq.insert("Task B-2", priority=2)  # Same priority as Task B
    # Order should be: Task A (seq 2), Task A-2 (seq 4), Task B (seq 1), Task B-2 (seq 5), Task C (seq 1)
    items = [data for data, _ in pq.to_list()]
    assert items == ["Task A", "Task A-2", "Task B", "Task B-2", "Task C"]
    print("[PASS] Test 3: FIFO stability for identical priorities verified.")

    # Test 4: Capacity limit & Overflow
    assert pq.is_full() is True
    try:
        pq.insert("Task Overflow", priority=1)
        assert False, "Should raise OverflowError when full"
    except OverflowError:
        pass
    print("[PASS] Test 4: Capacity limit and overflow verified.")

    # Test 5: Removal & Underflow
    assert pq.remove_highest_priority() == "Task A"
    assert pq.remove_highest_priority() == "Task A-2"
    assert pq.remove_highest_priority() == "Task B"
    assert pq.remove_highest_priority() == "Task B-2"
    assert pq.remove_highest_priority() == "Task C"
    assert pq.is_empty() is True
    try:
        pq.remove_highest_priority()
        assert False, "Should raise IndexError on empty removal"
    except IndexError:
        pass
    print("[PASS] Test 5: Removal in order & underflow handling verified.")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu options."""
    print("\n" + "=" * 50)
    print("       ARRAY PRIORITY QUEUE MENU")
    print("   (Note: Lower Number = Higher Priority)")
    print("=" * 50)
    print(" 1. Insert Item with Priority")
    print(" 2. Remove Highest Priority Item")
    print(" 3. Peek Highest Priority Item")
    print(" 4. Display Priority Queue")
    print(" 5. Check Empty / Full / Size")
    print(" 6. Exit")
    print("=" * 50)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 5 — Array-Based Priority Queue Demo")
    print("==========================================================")

    while True:
        cap_str = input("Enter capacity limit (or press Enter for unbounded): ").strip()
        if not cap_str:
            pq = ArrayPriorityQueue()
            print("Created unbounded Array Priority Queue.")
            break
        try:
            capacity = int(cap_str)
            if capacity <= 0:
                print("Error: Capacity must be > 0.")
                continue
            pq = ArrayPriorityQueue(capacity=capacity)
            print(f"Created Array Priority Queue with capacity {capacity}.")
            break
        except ValueError:
            print("Invalid input! Please enter a valid integer or press Enter.")

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            data = input("Enter element / task description: ").strip()
            pri_str = input("Enter integer priority (e.g., 1=Urgent, 5=Normal): ").strip()
            try:
                priority = int(pri_str)
                pq.insert(data, priority)
                print(f"Inserted '{data}' with priority {priority}.")
            except ValueError:
                print("Error: Priority must be an integer!")
            except OverflowError as err:
                print(f"Error: {err}")

        elif choice == "2":
            try:
                item = pq.remove_highest_priority()
                print(f"Removed Highest Priority Item: '{item}'")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "3":
            try:
                data, pri = pq.peek()
                print(f"Highest Priority Item: '{data}' (Priority: {pri})")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "4":
            print("\nCurrent Priority Queue Status:")
            pq.display()

        elif choice == "5":
            print(f"Is Empty: {pq.is_empty()}")
            print(f"Is Full:  {pq.is_full()}")
            cap_str = str(pq.capacity) if pq.capacity else "Unbounded"
            print(f"Size:     {pq.size()} / {cap_str}")

        elif choice == "6":
            print("Exiting Array Priority Queue Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()

