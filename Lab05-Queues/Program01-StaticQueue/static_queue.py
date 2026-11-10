"""
Program 01: Static Linear Queue (Fixed Capacity Array)
Course: IC-307D Data Structures and Algorithms Lab
Unit 5: Queues (CO1)

This program implements a Static Linear Queue using a fixed-capacity contiguous buffer:
- FIFO (First-In, First-Out) Principle:
    Elements are inserted at the 'rear' and removed from the 'front'.
    The first element enqueued is guaranteed to be the first element dequeued.
- Linear Array Queue Limitations:
    In a simple linear array queue, as elements are enqueued and dequeued, the 'front'
    and 'rear' indices advance rightward. Once 'rear' reaches capacity - 1, no further
    elements can be enqueued, even if multiple dequeues have vacated slots at the front.
    This creates 'false overflow' (unusable wasted memory) unless elements are shifted
    leftward on every dequeue at an expensive O(n) performance cost. This fundamental
    limitation directly motivates the Circular Queue (Program 03).
- Operations:
    enqueue, dequeue, peek/front, display, is_empty, is_full, and size tracking.
- Interactive console menu and automated test suite (--test flag).
"""

import sys
from typing import Any, List, Optional


class StaticQueue:
    """
    Fixed-capacity Linear Queue implementation adhering strictly to FIFO semantics.

    Attributes:
        capacity (int): Maximum number of elements the queue can store.
        _data (List[Optional[Any]]): Preallocated linear storage slots.
        _front (int): Index of the first element in the queue.
        _rear (int): Index of the last inserted element in the queue.
    """

    def __init__(self, capacity: int) -> None:
        """
        Initializes an empty StaticQueue with a positive fixed capacity.

        Raises:
            ValueError: If capacity is not a positive integer.
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError(f"Capacity must be a positive integer. Got: {capacity}")

        self.capacity: int = capacity
        self._data: List[Optional[Any]] = [None] * capacity
        self._front: int = 0
        self._rear: int = -1
        self._count: int = 0

    def is_empty(self) -> bool:
        """
        Checks whether the queue contains zero elements.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._count == 0

    def is_full(self) -> bool:
        """
        Checks whether the queue is full.
        In a simple linear queue, the queue is full when _rear reaches capacity - 1.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._rear == self.capacity - 1

    def size(self) -> int:
        """
        Returns the current number of elements in the queue.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._count

    def __len__(self) -> int:
        return self._count

    def enqueue(self, item: Any) -> None:
        """
        Inserts an item at the rear of the queue.

        Raises:
            OverflowError: If the queue is full (_rear == capacity - 1).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_full():
            raise OverflowError(
                f"Queue Overflow: Cannot enqueue into full linear queue (Capacity: {self.capacity}). "
                f"Even if elements were dequeued, linear arrays cannot reuse front slots."
            )

        self._rear += 1
        self._data[self._rear] = item
        self._count += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the item from the front of the queue.

        Raises:
            IndexError: If the queue is empty (Queue Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Queue Underflow: Cannot dequeue from an empty queue.")

        item = self._data[self._front]
        self._data[self._front] = None  # Clear reference to facilitate garbage collection
        self._front += 1
        self._count -= 1
        return item

    def peek(self) -> Any:
        """
        Returns the front item without removing it.

        Raises:
            IndexError: If the queue is empty (Queue Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Queue Underflow: Cannot peek into an empty queue.")

        return self._data[self._front]

    def display(self) -> str:
        """
        Returns a visual string representation of elements from front to rear.
        Example: "[Front -> 10, 20, 30 -> Rear]" or "[Empty Queue]"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.is_empty():
            return "[Empty Queue]"

        elements = [str(self._data[i]) for i in range(self._front, self._rear + 1)]
        return f"[Front -> {', '.join(elements)} -> Rear]"

    def to_list(self) -> List[Any]:
        """Returns queue elements from front to rear as a Python list (for testing)."""
        return [self._data[i] for i in range(self._front, self._rear + 1)]


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering all StaticQueue operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Static Queue (Program 01)")
    print("=" * 65)

    # 1. Capacity validation
    try:
        StaticQueue(0)
        assert False, "Should reject non-positive capacity"
    except ValueError:
        print("  [Test 01 Passed] Caught non-positive capacity.")

    # 2. Empty queue state and underflow
    q = StaticQueue(capacity=3)
    assert q.is_empty() is True
    assert q.is_full() is False
    assert q.size() == 0
    assert q.display() == "[Empty Queue]"

    try:
        q.dequeue()
        assert False, "Should raise IndexError on empty dequeue"
    except IndexError as err:
        print(f"  [Test 02 Passed] Caught dequeue underflow: {err}")

    try:
        q.peek()
        assert False, "Should raise IndexError on empty peek"
    except IndexError as err:
        print(f"  [Test 03 Passed] Caught peek underflow: {err}")

    # 3. Enqueue and peek operations
    q.enqueue("A")
    assert q.is_empty() is False
    assert q.size() == 1
    assert q.peek() == "A"

    q.enqueue("B")
    q.enqueue("C")
    assert q.size() == 3
    assert q.is_full() is True
    assert q.peek() == "A"
    assert q.to_list() == ["A", "B", "C"]
    print("  [Test 04 Passed] Enqueue, peek, and is_full verified.")

    # 4. Overflow handling
    try:
        q.enqueue("D")
        assert False, "Should raise OverflowError on full queue"
    except OverflowError as err:
        print(f"  [Test 05 Passed] Caught queue overflow: {err}")

    # 5. FIFO dequeue order
    assert q.dequeue() == "A"
    assert q.peek() == "B"
    assert q.size() == 2

    assert q.dequeue() == "B"
    assert q.dequeue() == "C"
    assert q.is_empty() is True
    print("  [Test 06 Passed] Strict FIFO dequeue order verified.")

    # 6. Demonstration of false overflow (limitation of linear queue)
    # The queue count is 0, but _rear is still 2 (capacity - 1)
    assert q.is_full() is True
    try:
        q.enqueue("X")
        assert False, "Should demonstrate false overflow"
    except OverflowError:
        print("  [Test 07 Passed] Linear queue limitation (false overflow) demonstrated.")

    print("\nAll Program 01 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n========================================")
    print("      STATIC QUEUE DEMONSTRATION")
    print("========================================")

    while True:
        try:
            cap_in = int(input("Enter fixed queue capacity (e.g. 5): ").strip())
            q = StaticQueue(capacity=cap_in)
            break
        except ValueError as err:
            print(f"Error: {err}. Please enter a positive integer.")

    menu = """
----------------------------------------
1. Enqueue Element
2. Dequeue Element
3. Peek Front Element
4. Display Queue Contents
5. Check if Empty
6. Check if Full
7. Run Automated Self-Tests
8. Exit
----------------------------------------
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            val = input("Enter value to enqueue: ").strip()
            if not val:
                print("Error: Value cannot be empty.")
                continue
            try:
                q.enqueue(val)
                print(f"Enqueued '{val}'. Queue: {q.display()} (Size: {q.size()}/{q.capacity})")
            except OverflowError as err:
                print(f"Overflow Error: {err}")

        elif choice == "2":
            try:
                item = q.dequeue()
                print(f"Dequeued: '{item}'. Remaining: {q.display()} (Size: {q.size()})")
            except IndexError as err:
                print(f"Underflow Error: {err}")

        elif choice == "3":
            try:
                print(f"Front element: '{q.peek()}'")
            except IndexError as err:
                print(f"Underflow Error: {err}")

        elif choice == "4":
            print(f"Queue Status: {q.display()} (Size: {q.size()}/{q.capacity})")

        elif choice == "5":
            print(f"is_empty: {q.is_empty()}")

        elif choice == "6":
            print(f"is_full: {q.is_full()}")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Static Queue. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()

