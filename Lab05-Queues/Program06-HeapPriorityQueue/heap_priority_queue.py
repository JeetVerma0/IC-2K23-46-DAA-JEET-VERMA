#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 5: Queues
Program 6: Priority Queue using Binary Min-Heap (Manual Implementation)

Author: Student Implementation
Course: IC-307D — DSA Lab (CO1)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
A Binary Heap is a complete binary tree stored compactly inside a linear array
without explicit child/parent pointers:
  - Root index:          0
  - Parent of node i:    (i - 1) // 2
  - Left child of i:     2 * i + 1
  - Right child of i:    2 * i + 2

MIN-HEAP PROPERTY:
In a Min-Heap, the key of every node is less than or equal to the keys of its
children. Consequently, the minimum element (highest priority) is always at the root.

PRIORITY CONVENTION & FIFO STABILITY:
  - Lower numeric priority value = higher precedence (e.g., 1 is higher than 5).
  - To maintain strict FIFO fairness when two items share the exact same priority,
    we store each entry as a tuple/object:
      key = (priority, arrival_counter)
    Because Python compares tuples lexicographically:
      (pri_A, seq_A) < (pri_B, seq_B)
    If pri_A == pri_B, the entry with the smaller arrival_counter wins.

ALGORITHMS:
  1. insert(data, priority):
     - Append entry to the end of the heap array: size increments by 1.
     - Call _heapify_up(last_index): compare entry with its parent. If smaller,
       swap and repeat upwards until root or heap property is satisfied.
     - Time Complexity: O(log n)

  2. remove_highest_priority() (Extract-Min):
     - Check underflow.
     - If heap has only 1 element, pop and return.
     - Swap root (index 0) with the last element.
     - Pop last element (which is the minimum).
     - Call _heapify_down(0): compare current node with its smaller child. If larger,
       swap and repeat downwards until leaf or heap property is satisfied.
     - Time Complexity: O(log n)

COMPARISON: ARRAY vs BINARY HEAP PRIORITY QUEUE
--------------------------------------------------------------------------------
Operation           Unsorted Array    Sorted Array        Binary Heap
--------------------------------------------------------------------------------
insert              O(1)              O(n)                O(log n)
remove_highest      O(n)              O(1) [from back]    O(log n)
peek                O(n)              O(1)                O(1)
Auxiliary Space     O(1)              O(1)                O(1)
--------------------------------------------------------------------------------
Binary Heap provides an optimal, scalable trade-off for dynamic priority queues!
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class HeapNode:
    """Represents a single element in the heap with priority and arrival counter."""

    def __init__(self, data: Any, priority: int, arrival_counter: int) -> None:
        self.data: Any = data
        self.priority: int = priority
        self.arrival_counter: int = arrival_counter

    def key(self) -> Tuple[int, int]:
        """Return comparable key (priority, arrival_counter)."""
        return (self.priority, self.arrival_counter)

    def __lt__(self, other: "HeapNode") -> bool:
        return self.key() < other.key()

    def __le__(self, other: "HeapNode") -> bool:
        return self.key() <= other.key()

    def __gt__(self, other: "HeapNode") -> bool:
        return self.key() > other.key()

    def __ge__(self, other: "HeapNode") -> bool:
        return self.key() >= other.key()

    def __repr__(self) -> str:
        return f"Node(data={self.data!r}, pri={self.priority}, seq={self.arrival_counter})"

    def __str__(self) -> str:
        return f"[Pri:{self.priority}, Seq:#{self.arrival_counter}] {self.data}"


class HeapPriorityQueue:
    """
    Priority Queue implemented using a custom binary min-heap without external libraries.
    """

    def __init__(self, capacity: Optional[int] = None) -> None:
        """
        Initialize the binary min-heap priority queue.

        Args:
            capacity: Maximum capacity (optional). If None, dynamically grows.
        """
        if capacity is not None and (not isinstance(capacity, int) or capacity <= 0):
            raise ValueError("Capacity must be a positive integer greater than zero.")

        self._capacity: Optional[int] = capacity
        self._heap: List[HeapNode] = []
        self._counter: int = 0  # Monotonic arrival order counter

    @property
    def capacity(self) -> Optional[int]:
        """Return maximum capacity or None if unbounded."""
        return self._capacity

    def is_empty(self) -> bool:
        """Return True if heap contains no elements."""
        return len(self._heap) == 0

    def is_full(self) -> bool:
        """Return True if heap reached fixed capacity limit."""
        if self._capacity is None:
            return False
        return len(self._heap) >= self._capacity

    def size(self) -> int:
        """Return number of elements currently stored in heap."""
        return len(self._heap)

    def _parent(self, index: int) -> int:
        """Return index of parent node."""
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Return index of left child node."""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Return index of right child node."""
        return 2 * index + 2

    def _heapify_up(self, index: int) -> None:
        """
        Restore min-heap property upward from index to root.
        Time Complexity: O(log n)
        """
        while index > 0:
            parent_idx = self._parent(index)
            if self._heap[index] < self._heap[parent_idx]:
                # Swap current with parent
                self._heap[index], self._heap[parent_idx] = self._heap[parent_idx], self._heap[index]
                index = parent_idx
            else:
                break

    def _heapify_down(self, index: int) -> None:
        """
        Restore min-heap property downward from index to leaf.
        Time Complexity: O(log n)
        """
        n = len(self._heap)
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left

            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != index:
                # Swap and continue downwards
                self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
                index = smallest
            else:
                break

    def insert(self, data: Any, priority: int) -> None:
        """
        Insert element with given integer priority into the min-heap.

        Time Complexity: O(log n)
        """
        if not isinstance(priority, int):
            raise TypeError(f"Priority must be an integer, got {type(priority).__name__}.")

        if self.is_full():
            raise OverflowError(
                f"Heap Priority Queue Overflow: Capacity limit ({self._capacity}) reached."
            )

        self._counter += 1
        node = HeapNode(data, priority, self._counter)
        self._heap.append(node)
        self._heapify_up(len(self._heap) - 1)

    def remove_highest_priority(self) -> Any:
        """
        Extract and return element with highest priority (min priority key).

        Time Complexity: O(log n)
        """
        if self.is_empty():
            raise IndexError("Heap Priority Queue Underflow: Queue is empty.")

        if len(self._heap) == 1:
            return self._heap.pop().data

        root_data = self._heap[0].data
        # Replace root with last element and heapify down
        self._heap[0] = self._heap.pop()
        self._heapify_down(0)
        return root_data

    def peek(self) -> Tuple[Any, int]:
        """
        Return (data, priority) of the highest priority element without removing it.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Heap Priority Queue is empty: No element to peek.")
        return self._heap[0].data, self._heap[0].priority

    def display(self) -> None:
        """Display the internal heap array and formatted hierarchical tree levels."""
        if self.is_empty():
            print("  Heap Priority Queue: [EMPTY]")
            print(f"  Size: 0 / {self._capacity if self._capacity else 'Unbounded'}")
            return

        cap_str = str(self._capacity) if self._capacity else "Unbounded"
        print(f"  Heap Size: {len(self._heap)} / {cap_str}")
        print("  Array Representation (index: [Pri, Seq] Value):")
        for i, node in enumerate(self._heap):
            print(f"    [{i:2d}] Priority: {node.priority:2d} | Seq: #{node.arrival_counter:2d} | Value: {node.data}")

        print("\n  Hierarchical Tree Levels:")
        level = 0
        level_count = 1
        i = 0
        n = len(self._heap)
        while i < n:
            level_nodes = []
            for _ in range(level_count):
                if i < n:
                    node = self._heap[i]
                    level_nodes.append(f"({node.priority}, #{node.arrival_counter}: {node.data})")
                    i += 1
            print(f"    Level {level}: " + "  ".join(level_nodes))
            level += 1
            level_count *= 2


def run_tests() -> None:
    """Automated unit verification test suite for Heap Priority Queue."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: Binary Min-Heap Priority Queue")
    print("=" * 70)

    # Test 1: Initial state
    hpq = HeapPriorityQueue(capacity=5)
    assert hpq.is_empty() is True
    assert hpq.is_full() is False
    assert hpq.size() == 0
    print("[PASS] Test 1: Initial state verified.")

    # Test 2: Min-heap ordering & peek
    hpq.insert("Process Low", priority=10)
    hpq.insert("Process High", priority=1)
    hpq.insert("Process Med", priority=5)
    assert hpq.size() == 3
    assert hpq.peek() == ("Process High", 1)
    print("[PASS] Test 2: Min-heap ordering verified.")

    # Test 3: FIFO stability under equal priorities
    # Current heap has: 1, 5, 10
    hpq.insert("Process High 2", priority=1)  # Same priority 1
    # Process High (seq 2) must come before Process High 2 (seq 4)
    res1 = hpq.remove_highest_priority()
    res2 = hpq.remove_highest_priority()
    assert res1 == "Process High"
    assert res2 == "Process High 2"
    print("[PASS] Test 3: FIFO tie-breaking for equal priorities verified.")

    # Test 4: Capacity limit & Overflow
    hpq.insert("Task X", 2)
    hpq.insert("Task Y", 3)
    hpq.insert("Task Z", 4)
    # Remaining capacity: hpq had 2 elements ("Process Med", "Process Low"), now 5
    assert hpq.is_full() is True
    try:
        hpq.insert("Overflow Task", 0)
        assert False, "Should raise OverflowError on full capacity"
    except OverflowError:
        pass
    print("[PASS] Test 4: Capacity limit & overflow verified.")

    # Test 5: Exhaustive removal in priority order
    extracted = []
    while not hpq.is_empty():
        extracted.append(hpq.remove_highest_priority())
    assert extracted == ["Task X", "Task Y", "Task Z", "Process Med", "Process Low"]
    assert hpq.is_empty() is True
    try:
        hpq.remove_highest_priority()
        assert False, "Should raise IndexError on empty removal"
    except IndexError:
        pass
    print("[PASS] Test 5: Full extraction sequence and underflow handling verified.")

    print("\nALL 5 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu options."""
    print("\n" + "=" * 55)
    print("     BINARY MIN-HEAP PRIORITY QUEUE MENU")
    print("   (Note: Lower Number = Higher Priority)")
    print("=" * 55)
    print(" 1. Insert Item with Priority (O(log n))")
    print(" 2. Remove Highest Priority Item (Extract-Min O(log n))")
    print(" 3. Peek Highest Priority Item (O(1))")
    print(" 4. Display Heap Array & Tree Levels")
    print(" 5. Check Empty / Full / Size")
    print(" 6. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 5 — Binary Heap Priority Queue Demo")
    print("==========================================================")

    while True:
        cap_str = input("Enter capacity limit (or press Enter for unbounded): ").strip()
        if not cap_str:
            hpq = HeapPriorityQueue()
            print("Created unbounded Binary Heap Priority Queue.")
            break
        try:
            capacity = int(cap_str)
            if capacity <= 0:
                print("Error: Capacity must be > 0.")
                continue
            hpq = HeapPriorityQueue(capacity=capacity)
            print(f"Created Binary Heap Priority Queue with capacity {capacity}.")
            break
        except ValueError:
            print("Invalid input! Please enter a valid integer or press Enter.")

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            data = input("Enter item / task name: ").strip()
            pri_str = input("Enter integer priority (e.g. 1=Critical, 10=Low): ").strip()
            try:
                priority = int(pri_str)
                hpq.insert(data, priority)
                print(f"Inserted '{data}' with priority {priority}.")
            except ValueError:
                print("Error: Priority must be an integer!")
            except OverflowError as err:
                print(f"Error: {err}")

        elif choice == "2":
            try:
                item = hpq.remove_highest_priority()
                print(f"Removed Highest Priority Item: '{item}'")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "3":
            try:
                data, pri = hpq.peek()
                print(f"Highest Priority Item: '{data}' (Priority: {pri})")
            except IndexError as err:
                print(f"Error: {err}")

        elif choice == "4":
            print("\nCurrent Heap Status:")
            hpq.display()

        elif choice == "5":
            print(f"Is Empty: {hpq.is_empty()}")
            print(f"Is Full:  {hpq.is_full()}")
            cap_str = str(hpq.capacity) if hpq.capacity else "Unbounded"
            print(f"Size:     {hpq.size()} / {cap_str}")

        elif choice == "6":
            print("Exiting Binary Heap Priority Queue Program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()

