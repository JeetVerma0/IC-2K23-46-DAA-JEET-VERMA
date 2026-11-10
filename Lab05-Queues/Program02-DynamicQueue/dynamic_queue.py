"""
Program 02: Dynamic Queue (Singly Linked List)
Course: IC-307D Data Structures and Algorithms Lab
Unit 5: Queues (CO1)

This program implements a Dynamic Queue using a singly linked list from first principles:
- Dynamic Heap Allocation:
    Unlike static array queues, a linked queue grows and contracts on demand,
    eliminating capacity bounds and false overflow issues entirely.
- Dual Pointer Maintenance:
    - 'front': Points to the first element in the queue (head of linked list).
    - 'rear': Points to the most recently inserted element (tail of linked list).
- Core Operations:
    - enqueue: Appends a new QueueNode at 'rear' in O(1) time.
    - dequeue: Removes the node at 'front' in O(1) time.
    - peek: Inspects front.data in O(1) time without modifying pointers.
    - Boundary Update: When the last remaining element is dequeued, both
      'front' and 'rear' are reset to None.
- Zero-dependency:
    Pure node pointer manipulation without using Python lists as queue storage.
- Interactive console menu and automated test suite (--test flag).
"""

import sys
from typing import Any, List, Optional


class QueueNode:
    """
    Represents an individual node in the dynamic linked queue.

    Attributes:
        data (Any): Payload stored in the node.
        next (Optional[QueueNode]): Pointer to the succeeding node in the queue.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional["QueueNode"] = None

    def __repr__(self) -> str:
        return f"QueueNode({self.data})"


class DynamicQueue:
    """
    Dynamic Queue implemented using a Singly Linked List with front and rear pointers.

    Attributes:
        front (Optional[QueueNode]): Points to the head (removal end).
        rear (Optional[QueueNode]): Points to the tail (insertion end).
        _size (int): Number of active elements.
    """

    def __init__(self) -> None:
        self.front: Optional[QueueNode] = None
        self.rear: Optional[QueueNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Checks whether the queue contains zero elements.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self.front is None

    def size(self) -> int:
        """
        Returns the number of elements in the queue.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._size

    def __len__(self) -> int:
        return self._size

    def enqueue(self, item: Any) -> None:
        """
        Inserts an item at the rear of the queue.

        Algorithm:
            1. Allocate new_node = QueueNode(item).
            2. If queue is empty: front = rear = new_node.
            3. Else:
               rear.next = new_node
               rear = new_node
            4. Increment _size by 1.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1) per node
        """
        new_node = QueueNode(item)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the item from the front of the queue.

        Raises:
            IndexError: If the queue is empty (Queue Underflow).

        Algorithm:
            1. If front is None, raise IndexError.
            2. Store item = front.data.
            3. Update front = front.next.
            4. If front is now None, also set rear = None (queue became empty).
            5. Decrement _size by 1. Return item.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.front is None:
            raise IndexError("Queue Underflow: Cannot dequeue from an empty dynamic queue.")

        item = self.front.data
        self.front = self.front.next

        # If queue became empty, reset rear pointer
        if self.front is None:
            self.rear = None

        self._size -= 1
        return item

    def peek(self) -> Any:
        """
        Returns the front item without removing it.

        Raises:
            IndexError: If the queue is empty (Queue Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.front is None:
            raise IndexError("Queue Underflow: Cannot peek into an empty dynamic queue.")

        return self.front.data

    def display(self) -> str:
        """
        Returns a visual string representation of elements from front to rear.
        Example: "[Front -> 10 -> 20 -> 30 -> Rear]" or "[Empty Queue]"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.front is None:
            return "[Empty Queue]"

        elements: List[str] = []
        current = self.front
        while current is not None:
            elements.append(str(current.data))
            current = current.next

        return f"[Front -> {' -> '.join(elements)} -> Rear]"

    def to_list(self) -> List[Any]:
        """Returns queue elements from front to rear as a Python list (for testing)."""
        elements: List[Any] = []
        current = self.front
        while current is not None:
            elements.append(current.data)
            current = current.next
        return elements


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering all DynamicQueue operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Dynamic Queue (Program 02)")
    print("=" * 65)

    q = DynamicQueue()

    # 1. Empty queue state and underflow
    assert q.is_empty() is True
    assert q.size() == 0
    assert q.front is None and q.rear is None
    assert q.display() == "[Empty Queue]"

    try:
        q.dequeue()
        assert False, "Should raise IndexError on empty dequeue"
    except IndexError as err:
        print(f"  [Test 01 Passed] Caught dequeue underflow: {err}")

    try:
        q.peek()
        assert False, "Should raise IndexError on empty peek"
    except IndexError as err:
        print(f"  [Test 02 Passed] Caught peek underflow: {err}")

    # 2. Single-element operations & pointer integrity
    q.enqueue("First")
    assert q.is_empty() is False
    assert q.size() == 1
    assert q.front is not None and q.rear is not None
    assert q.front == q.rear
    assert q.peek() == "First"
    print("  [Test 03 Passed] Single-element enqueue verified.")

    # Dequeue single element
    assert q.dequeue() == "First"
    assert q.is_empty() is True
    assert q.size() == 0
    assert q.front is None and q.rear is None
    print("  [Test 04 Passed] Dequeue to empty correctly cleared front and rear.")

    # 3. Multi-element enqueue & FIFO order
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    assert q.size() == 3
    assert q.peek() == 10
    assert q.to_list() == [10, 20, 30]

    assert q.dequeue() == 10
    assert q.peek() == 20
    assert q.dequeue() == 20
    assert q.peek() == 30
    assert q.dequeue() == 30
    assert q.is_empty() is True
    print("  [Test 05 Passed] FIFO order and size tracking verified.")

    # 4. Continuous reuse without overflow
    for i in range(100):
        q.enqueue(i)
    assert q.size() == 100
    assert q.peek() == 0

    for i in range(100):
        assert q.dequeue() == i
    assert q.is_empty() is True
    assert q.front is None and q.rear is None
    print("  [Test 06 Passed] Dynamic heap scaling and deallocation verified.")

    print("\nAll Program 02 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    q = DynamicQueue()

    menu = """
========================================
     DYNAMIC QUEUE (Linked List)
========================================
1. Enqueue Element
2. Dequeue Element
3. Peek Front Element
4. Display Queue Contents
5. Check if Empty
6. View Current Size
7. Run Automated Self-Tests
8. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            val = input("Enter value to enqueue: ").strip()
            if not val:
                print("Error: Value cannot be empty.")
                continue
            q.enqueue(val)
            print(f"Enqueued '{val}'. Queue: {q.display()} (Size: {q.size()})")

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
            print(f"Queue Status: {q.display()} (Size: {q.size()})")

        elif choice == "5":
            print(f"is_empty: {q.is_empty()}")

        elif choice == "6":
            print(f"Current Size: {q.size()}")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Dynamic Queue. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose 1-8.")


if __name__ == "__main__":
    main()

