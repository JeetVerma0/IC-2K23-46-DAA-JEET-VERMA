"""
Program 01: Static Stack Implementation (Fixed Capacity)
Course: IC-307D Data Structures and Algorithms Lab
Unit 4: Stacks (CO1)

This program implements a Static Stack using a fixed-capacity contiguous buffer:
- LIFO (Last-In, First-Out) Principle:
    The most recently added element is always the first to be retrieved or removed.
    Access to elements is strictly restricted to one end, termed the 'top'.
- Fixed-Capacity Limitation:
    The stack is initialized with a predetermined maximum capacity.
    Memory is allocated upfront. If insertions exceed this capacity, a Stack Overflow
    condition occurs. Conversely, attempting to pop or peek an empty stack triggers
    a Stack Underflow condition.
- Core Operations:
    push, pop, peek, is_empty, is_full, display, and size tracking.
- Interactive console menu and automated test suite (--test flag).
"""

import sys
from typing import Any, List, Optional


class StaticStack:
    """
    Fixed-capacity Stack implementation adhering strictly to LIFO semantics.

    Attributes:
        capacity (int): Maximum number of elements the stack can accommodate.
        _data (List[Any]): Preallocated internal buffer.
        _top (int): Index pointing to current top element (-1 when empty).
    """

    def __init__(self, capacity: int) -> None:
        """
        Initializes an empty StaticStack with a positive fixed capacity.

        Raises:
            ValueError: If capacity is not a positive integer.
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError(f"Capacity must be a positive integer. Got: {capacity}")

        self.capacity: int = capacity
        # Preallocate fixed array slots
        self._data: List[Optional[Any]] = [None] * capacity
        self._top: int = -1

    def is_empty(self) -> bool:
        """
        Checks whether the stack contains zero elements.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._top == -1

    def is_full(self) -> bool:
        """
        Checks whether the stack has reached its maximum capacity.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._top == self.capacity - 1

    def size(self) -> int:
        """
        Returns the current number of elements in the stack.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._top + 1

    def __len__(self) -> int:
        return self.size()

    def push(self, item: Any) -> None:
        """
        Pushes a new item onto the top of the stack.

        Raises:
            OverflowError: If stack is already full (Stack Overflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_full():
            raise OverflowError(
                f"Stack Overflow: Cannot push onto full stack (Capacity: {self.capacity})."
            )

        self._top += 1
        self._data[self._top] = item

    def pop(self) -> Any:
        """
        Removes and returns the top element of the stack.

        Raises:
            IndexError: If stack is empty (Stack Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Stack Underflow: Cannot pop from an empty stack.")

        item = self._data[self._top]
        self._data[self._top] = None  # Clear reference to assist garbage collection
        self._top -= 1
        return item

    def peek(self) -> Any:
        """
        Returns the top element without removing it.

        Raises:
            IndexError: If stack is empty (Stack Underflow).

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Stack Underflow: Cannot peek into an empty stack.")

        return self._data[self._top]

    def display(self) -> str:
        """
        Returns a visual string representation of the stack from top to bottom.
        Example: "[Top -> 30, 20, 10 -> Bottom]" or "[Empty Stack]"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.is_empty():
            return "[Empty Stack]"

        elements = [str(self._data[i]) for i in range(self._top, -1, -1)]
        return f"[Top -> {', '.join(elements)} -> Bottom]"

    def to_list(self) -> List[Any]:
        """Returns stack elements as a Python list from bottom to top (for testing)."""
        return [self._data[i] for i in range(self._top + 1)]


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering all StaticStack operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Static Stack (Program 01)")
    print("=" * 65)

    # 1. Capacity validation
    try:
        StaticStack(0)
        assert False, "Should reject capacity <= 0"
    except ValueError:
        print("  [Test 01 Passed] Caught non-positive capacity.")

    # 2. Empty stack state and underflow
    stack = StaticStack(capacity=3)
    assert stack.is_empty() is True
    assert stack.is_full() is False
    assert stack.size() == 0
    assert stack.display() == "[Empty Stack]"

    try:
        stack.pop()
        assert False, "Should raise IndexError on empty pop"
    except IndexError as err:
        print(f"  [Test 02 Passed] Caught pop underflow: {err}")

    try:
        stack.peek()
        assert False, "Should raise IndexError on empty peek"
    except IndexError as err:
        print(f"  [Test 03 Passed] Caught peek underflow: {err}")

    # 3. Push and peek operations
    stack.push(10)
    assert stack.is_empty() is False
    assert stack.size() == 1
    assert stack.peek() == 10

    stack.push(20)
    stack.push(30)
    assert stack.size() == 3
    assert stack.is_full() is True
    assert stack.peek() == 30
    assert stack.to_list() == [10, 20, 30]
    print("  [Test 04 Passed] Push and peek operations verified.")

    # 4. Overflow handling
    try:
        stack.push(40)
        assert False, "Should raise OverflowError on full stack"
    except OverflowError as err:
        print(f"  [Test 05 Passed] Caught push overflow: {err}")

    # 5. LIFO pop order
    assert stack.pop() == 30
    assert stack.size() == 2
    assert stack.is_full() is False

    assert stack.pop() == 20
    assert stack.pop() == 10
    assert stack.is_empty() is True
    print("  [Test 06 Passed] Strict LIFO pop order verified.")

    # 6. Push after popping to verify boundary reuse
    stack.push(99)
    assert stack.peek() == 99
    assert stack.pop() == 99
    assert stack.is_empty() is True
    print("  [Test 07 Passed] Post-underflow push/pop reuse verified.")

    print("\nAll Program 01 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("\n========================================")
    print("      STATIC STACK DEMONSTRATION")
    print("========================================")

    while True:
        try:
            cap_in = int(input("Enter fixed stack capacity (e.g. 5): ").strip())
            stack = StaticStack(capacity=cap_in)
            break
        except ValueError as err:
            print(f"Error: {err}. Please enter a positive integer.")

    menu = """
----------------------------------------
1. Push Element
2. Pop Element
3. Peek Top Element
4. Display Stack Contents
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
            val = input("Enter value to push: ").strip()
            if not val:
                print("Error: Value cannot be empty.")
                continue
            try:
                stack.push(val)
                print(f"Pushed '{val}' successfully. Size: {stack.size()}/{stack.capacity}")
            except OverflowError as err:
                print(f"Overflow Error: {err}")

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
            print(f"Stack Status: {stack.display()} (Size: {stack.size()}/{stack.capacity})")

        elif choice == "5":
            print(f"is_empty: {stack.is_empty()}")

        elif choice == "6":
            print(f"is_full: {stack.is_full()}")

        elif choice == "7":
            run_tests()

        elif choice == "8":
            print("Exiting Static Stack. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()

