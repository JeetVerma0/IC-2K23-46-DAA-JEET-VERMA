"""
Program 03: Circular Queue (Fixed Capacity with Modular Arithmetic)
Course: IC-307D Data Structures and Algorithms Lab
Unit 5: Queues (CO1)

This program implements a Circular Queue using a fixed-capacity array:
- Resolving the Linear Queue Limitation:
    In a linear array queue, dequeuing elements leaves unfillable gaps at the front,
    eventually causing false overflow even when slots are vacant.
    A Circular Queue models the array as a continuous ring by wrapping around indices
    using modular arithmetic:
        next_rear  = (rear + 1) % capacity
        next_front = (front + 1) % capacity
- Full vs. Empty Discrimination:
    By maintaining an explicit count (_count) of active elements:
    - Empty condition: _count == 0
    - Full condition:  _count == capacity
    All capacity slots are fully utilized without sacrificing a sentinel slot.
- Memory Slot Reuse:
    Demonstrates that as front slots are vacated by dequeue(), subsequent enqueue()
    operations seamlessly wrap around to occupy those exact slots.
- Operations:
    enqueue, dequeue, peek, display (logical order and internal slot map), is_empty, is_full.
- Interactive console menu and automated test suite (--test flag).
"""

import sys
from typing import Any, List, Optional


class CircularQueue:
    """
    Fixed-capacity Circular Queue using modular arithmetic for wraparound.

    Attributes:
        capacity (int): Maximum storage capacity.
        _data (List[Optional[Any]]): Fixed-size internal buffer.
        _front (int): Index of the front element.
        _rear (int): Index of the rear element.
        _count (int): Active element count.
    """

    def __init__(self, capacity: int) -> None:
        """
        Initializes an empty CircularQueue with a fixed capacity.

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
        Checks whether the circular queue contains zero elements.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._count == 0

    def is_full(self) -> bool:
        """
        Checks whether the circular queue has reached maximum capacity.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._count == self.capacity

    def size(self) -> int:
        """
        Returns the number of elements currently stored.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._count

    def __len__(self) -> int:
        return self._count

    def enqueue(self, item: Any) -> None:
        """
        Inserts an item at the rear using circular wraparound.

        Raises:
            OverflowError: If the circular queue is full.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_full():
            raise OverflowError(
                f"Circular Queue Overflow: All {self.capacity} slots are occupied."
            )

        self._rear = (self._rear + 1) % self.capacity
        self._data[self._rear] = item
        self._count += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the item from the front using circular wraparound.

        Raises:
            IndexError: If the circular queue is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Circular Queue Underflow: Cannot dequeue from an empty queue.")

        item = self._data[self._front]
        self._data[self._front] = None  # Free slot reference
        self._front = (self._front + 1) % self.capacity
        self._count -= 1
        return item

    def peek(self) -> Any:
        """
        Returns the front item without removing it.

        Raises:
            IndexError: If the circular queue is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Circular Queue Underflow: Cannot peek into an empty queue.")

        return self._data[self._front]

    def display(self) -> str:
        """
        Returns elements in logical FIFO order from front to rear.
        Example: "[Front -> 10, 20, 30 -> Rear]" or "[Empty Queue]"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.is_empty():
            return "[Empty Queue]"

        elements = [
            str(self._data[(self._front + i) % self.capacity])
            for i in range(self._count)
        ]
        return f"[Front -> {', '.join(elements)} -> Rear]"

    def display_physical(self) -> str:
        """
        Returns the underlying physical array buffer showing actual slot positions,
        front/rear indices, and vacant slots.
        """
        slots = []
        for i in range(self.capacity):
            val = self._data[i]
            markers = []
            if i == self._front and not self.is_empty():
                markers.append("F")
            if i == self._rear and not self.is_empty():
                markers.append("R")
            tag = f"({'/'.join(markers)})" if markers else ""
            slots.append(f"[{i}]: {val} {tag}".strip())

        return " | ".join(slots)

    def to_list(self) -> List[Any]:
        """Returns logical elements from front to rear as a Python list (for testing)."""
        return [
            self._data[(self._front + i) % self.capacity]
            for i in range(self._count)
        ]


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive tests covering all CircularQueue operations and wraparound logic."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Circular Queue (Program 03)")
    print("=" * 65)

    cq = CircularQueue(capacity=4)

    # 1. Empty state & underflow
    assert cq.is_empty() is True
    assert cq.is_full() is False
    assert cq.size() == 0
    assert cq.display() == "[Empty Queue]"

    try:
        cq.dequeue()
        assert False, "Should raise IndexError on empty dequeue"
    except IndexError as err:
        print(f"  [Test 01 Passed] Caught dequeue underflow: {err}")

    # 2. Fill queue to capacity (indices 0, 1, 2, 3)
    cq.enqueue("A")  # slot 0
    cq.enqueue("B")  # slot 1
    cq.enqueue("C")  # slot 2
    cq.enqueue("D")  # slot 3
    assert cq.size() == 4
    assert cq.is_full() is True
    assert cq.to_list() == ["A", "B", "C", "D"]
    assert cq.peek() == "A"
    print("  [Test 02 Passed] Full capacity enqueue verified.")

    # 3. Overflow error
    try:
        cq.enqueue("E")
        assert False, "Should raise OverflowError on full queue"
    except OverflowError as err:
        print(f"  [Test 03 Passed] Caught circular queue overflow: {err}")

    # 4. Dequeue two elements (freeing slots 0 and 1)
    assert cq.dequeue() == "A"  # front moves to 1
    assert cq.dequeue() == "B"  # front moves to 2
    assert cq.size() == 2
    assert cq.is_full() is False
    assert cq.to_list() == ["C", "D"]
    print("  [Test 04 Passed] Dequeued elements freeing front physical slots.")

    # 5. WRAPAROUND TEST: Enqueue two elements into freed slots 0 and 1
    # In a linear queue, this causes false overflow.
    # In a circular queue, rear wraps around from index 3 -> 0 -> 1!
    cq.enqueue("E")  # wraps to slot 0
    cq.enqueue("F")  # wraps to slot 1
    assert cq.size() == 4
    assert cq.is_full() is True
    # Logical order MUST preserve FIFO: C, D, E, F
    assert cq.to_list() == ["C", "D", "E", "F"]
    assert cq.peek() == "C"
    # Physical buffer check: [0]=E, [1]=F, [2]=C, [3]=D
    assert cq._data == ["E", "F", "C", "D"]
    print("  [Test 05 Passed] Modular wraparound and slot reuse successfully verified.")

    # 6. Dequeue all remaining wrapped elements
    assert cq.dequeue() == "C"
    assert cq.dequeue() == "D"
    assert cq.dequeue() == "E"
    assert cq.dequeue() == "F"
    assert cq.is_empty() is True
    assert cq.size() == 0
    print("  [Test 06 Passed] Complete FIFO dequeue across wraparound boundary verified.")

    print("\nAll Program 03 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n========================================")
    print("     CIRCULAR QUEUE DEMONSTRATION")
    print("========================================")

    while True:
        try:
            cap_in = int(input("Enter fixed queue capacity (e.g. 4): ").strip())
            cq = CircularQueue(capacity=cap_in)
            break
        except ValueError as err:
            print(f"Error: {err}. Please enter a positive integer.")

    menu = """
----------------------------------------
1. Enqueue Element (Modular Insertion)
2. Dequeue Element (Modular Removal)
3. Peek Front Element
4. Display Logical Queue (FIFO Order)
5. Display Physical Array (Slot Map)
6. Check if Empty / Full
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
                cq.enqueue(val)
                print(f"Enqueued '{val}'. Logical: {cq.display()}")
                print(f"Physical Array: {cq.display_physical()}")
            except OverflowError as err:
                print(f"Overflow Error: {err}")

        elif choice == "2":
            try:
                item = cq.dequeue()
                print(f"Dequeued: '{item}'. Logical: {cq.display()}")
                print(f"Physical Array: {cq.display_physical()}")
            except IndexError as err:
                print(f"Underflow Error: {err}")

        elif choice == "3":
            try:
                print(f"Front element: '{cq.peek()}'")
            except IndexError as err:
                print(f"Underflow Error: {err}")

        elif choice == "4":
            print(f"Logical Queue: {cq.display()} (Size: {cq.size()}/{cq.capacity})")

        elif choice == "5":
            print(f"Physical Slot Map: {cq.display_physical()}")

        elif choice == "6":
            print(f"is_empty: {cq.is_empty()} | is_full: {cq.is_full()} (Size: {cq.size()}/{cq.capacity})")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Circular Queue. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose 1-8.")


if __name__ == "__main__":
    main()

