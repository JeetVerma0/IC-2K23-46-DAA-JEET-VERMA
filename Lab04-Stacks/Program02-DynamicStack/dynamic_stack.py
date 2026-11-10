"""
Program 02: Dynamic Stack Implementation (Linked List)
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program implements a Dynamic Stack using a singly linked list from first principles:
- Dynamic Memory Allocation:
    Unlike static arrays, a linked stack has no fixed capacity. Each element is
    encapsulated in an independently allocated heap Node.
    The stack grows and contracts dynamically, bounded only by the host system's
    available physical memory.
- LIFO Semantics via Head Pointer:
    The 'top' of the stack corresponds directly to the 'head' of the singly linked list.
    - push: Prepends a new Node at head in O(1) time.
    - pop: Removes the head Node in O(1) time.
    - peek: Inspects head.data in O(1) time.
    No elements need to be shifted, and no geometric array reallocations occur.
- Zero-dependency:
    Pure Node-based pointer manipulation without using Python lists as internal storage.
- Interactive console menu and automated test suite (--test flag).
"""

import sys
from typing import Any, List, Optional


class StackNode:
    """
    Represents an individual node in the dynamic linked stack.

    Attributes:
        data (Any): Payload stored in the node.
        next (Optional[StackNode]): Pointer to the node beneath it in the stack.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional["StackNode"] = None

    def __repr__(self) -> str:
        return f"StackNode({self.data})"


class DynamicStack:
    """
    Dynamic Stack implemented using a Singly Linked List.

    Attributes:
        top (Optional[StackNode]): Reference to the topmost node (head of linked list).
        _size (int): Current element count.
    """

    def __init__(self) -> None:
        self.top: Optional[StackNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Checks whether the stack contains zero elements.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self.top is None

    def size(self) -> int:
        """
        Returns the number of elements currently stored in the stack.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._size

    def __len__(self) -> int:
        return self._size

    def push(self, item: Any) -> None:
        """
        Pushes a new item onto the top of the stack.
        Dynamically allocates a new node and prepends it to the top.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1) per push
        """
        new_node = StackNode(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self) -> Any:
        """
        Removes and returns the topmost item from the stack.

        Raises:
            IndexError: If the stack is empty (Stack Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.top is None:
            raise IndexError("Stack Underflow: Cannot pop from an empty dynamic stack.")

        item = self.top.data
        self.top = self.top.next
        self._size -= 1
        return item

    def peek(self) -> Any:
        """
        Returns the topmost item without removing it.

        Raises:
            IndexError: If the stack is empty (Stack Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.top is None:
            raise IndexError("Stack Underflow: Cannot peek into an empty dynamic stack.")

        return self.top.data

    def display(self) -> str:
        """
        Returns a visual string representation of the stack from top to bottom.
        Example: "[Top -> 30 -> 20 -> 10 -> Bottom]" or "[Empty Stack]"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.top is None:
            return "[Empty Stack]"

        elements: List[str] = []
        current = self.top
        while current is not None:
            elements.append(str(current.data))
            current = current.next

        return f"[Top -> {' -> '.join(elements)} -> Bottom]"

    def to_list(self) -> List[Any]:
        """Returns stack elements as a Python list from bottom to top (for testing)."""
        elements: List[Any] = []
        current = self.top
        while current is not None:
            elements.append(current.data)
            current = current.next
        # Reverse so index 0 is bottom
        return elements[::-1]


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering all DynamicStack operations."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Dynamic Stack (Program 02)")
    print("=" * 65)

    stack = DynamicStack()

    # 1. Empty stack state and underflow
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert stack.display() == "[Empty Stack]"

    try:
        stack.pop()
        assert False, "Should raise IndexError on empty pop"
    except IndexError as err:
        print(f"  [Test 01 Passed] Caught pop underflow: {err}")

    try:
        stack.peek()
        assert False, "Should raise IndexError on empty peek"
    except IndexError as err:
        print(f"  [Test 02 Passed] Caught peek underflow: {err}")

    # 2. Push operations and dynamic growth
    stack.push(10)
    assert stack.is_empty() is False
    assert stack.size() == 1
    assert stack.peek() == 10

    stack.push(20)
    stack.push(30)
    stack.push(40)
    stack.push(50)
    assert stack.size() == 5
    assert stack.peek() == 50
    assert stack.to_list() == [10, 20, 30, 40, 50]
    print("  [Test 03 Passed] Dynamic stack growth and peek verified.")

    # 3. LIFO pop sequence
    assert stack.pop() == 50
    assert stack.size() == 4
    assert stack.peek() == 40

    assert stack.pop() == 40
    assert stack.pop() == 30
    assert stack.pop() == 20
    assert stack.pop() == 10
    assert stack.is_empty() is True
    assert stack.size() == 0
    print("  [Test 04 Passed] Strict LIFO pop sequence verified.")

    # 4. Push after complete emptying
    stack.push("Alpha")
    stack.push("Beta")
    assert stack.peek() == "Beta"
    assert stack.pop() == "Beta"
    assert stack.pop() == "Alpha"
    assert stack.is_empty() is True
    print("  [Test 05 Passed] Dynamic re-growth after emptying verified.")

    print("\nAll Program 02 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    stack = DynamicStack()

    menu = """
========================================
     DYNAMIC STACK (Linked List)
========================================
1. Push Element
2. Pop Element
3. Peek Top Element
4. Display Stack Contents
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
            val = input("Enter value to push: ").strip()
            if not val:
                print("Error: Value cannot be empty.")
                continue
            stack.push(val)
            print(f"Pushed '{val}' successfully. Current Size: {stack.size()}")

        elif choice == "2":
            try:
                item = stack.pop()
                print(f"Popped element: '{item}' | Remaining size: {stack.size()}")
            except IndexError as err:
                print(f"Underflow Error: {err}")

        elif choice == "3":
            try:
                print(f"Top element: '{stack.peek()}'")
            except IndexError as err:
                print(f"Underflow Error: {err}")

        elif choice == "4":
            print(f"Stack Status: {stack.display()} (Size: {stack.size()})")

        elif choice == "5":
            print(f"is_empty: {stack.is_empty()}")

        elif choice == "6":
            print(f"Current Size: {stack.size()}")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Dynamic Stack. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()

