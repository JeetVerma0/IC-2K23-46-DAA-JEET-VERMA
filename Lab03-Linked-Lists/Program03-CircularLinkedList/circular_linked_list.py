"""
Program 03: Circular Linked List
Course: IC-307D Data Structures and Algorithms Lab
Unit 3: Linked Lists (CO1)

This program implements a Circular Singly Linked List from first principles:
- The terminal node's 'next' pointer wraps around to point back to 'head',
  forming a closed continuous ring.
- Node class containing 'data' and 'next' pointer reference.
- CircularLinkedList class supporting insertion, deletion, searching, in-place
  reversal, and concatenation.
- Traversal mechanisms specifically designed to terminate after completing one
  full ring cycle, strictly preventing infinite loops.
- Robust handling of single-node self-referential cycles (node.next == node)
  and empty lists.
- Full time and space complexity documentation.
"""

from typing import Any, List, Optional


class CircularNode:
    """
    Represents an individual node in a Circular Linked List.

    Attributes:
        data: The payload or value stored in the node.
        next: Pointer to the next node in the circular ring.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional["CircularNode"] = None

    def __repr__(self) -> str:
        return f"CircularNode({self.data})"


class CircularLinkedList:
    """
    Circular Singly Linked List data structure.

    Invariant:
        For an empty list: head is None.
        For a single-node list: head.next == head.
        For an n-node list: following 'next' starting from head visits all n nodes
        and returns back to head.

    Zero-based Indexing Convention:
        Index 0 represents the head node.
        Index n - 1 represents the last node (whose .next == head).
        Valid insertion indices: [0, n].
        Valid deletion indices: [0, n - 1].
    """

    def __init__(self) -> None:
        self.head: Optional[CircularNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Checks whether the circular linked list is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self.head is None

    def __len__(self) -> int:
        """
        Returns the number of nodes in the circular list.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._size

    def insert_beginning(self, data: Any) -> None:
        """
        Inserts a new node at the beginning of the circular list.
        The new node becomes the new head, and the last node's next pointer
        is updated to point to this new head.

        Algorithm:
            1. Create new_node with data.
            2. If list is empty:
               new_node.next = new_node
               head = new_node
            3. Else:
               Traverse to last node (where current.next == head).
               new_node.next = head
               last_node.next = new_node
               head = new_node
            4. Increment size by 1.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        new_node = CircularNode(data)
        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            # Locate last node
            last = self.head
            while last.next != self.head:
                assert last.next is not None
                last = last.next

            new_node.next = self.head
            last.next = new_node
            self.head = new_node

        self._size += 1

    def insert_end(self, data: Any) -> None:
        """
        Inserts a new node at the end of the circular list.
        The new node becomes the last node, pointing back to head.

        Algorithm:
            1. Create new_node with data.
            2. If list is empty:
               new_node.next = new_node
               head = new_node
            3. Else:
               Traverse to last node (where current.next == head).
               last_node.next = new_node
               new_node.next = head
            4. Increment size by 1.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        new_node = CircularNode(data)
        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            last = self.head
            while last.next != self.head:
                assert last.next is not None
                last = last.next

            last.next = new_node
            new_node.next = self.head

        self._size += 1

    def insert_at_position(self, data: Any, position: int) -> None:
        """
        Inserts a new node at the specified zero-based position in the circular list.

        Args:
            data: Payload to store.
            position: Zero-based position in range [0, len(self)].

        Raises:
            TypeError: If position is not an integer.
            IndexError: If position < 0 or position > len(self).

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if not isinstance(position, int):
            raise TypeError("Position must be an integer.")

        if position < 0 or position > self._size:
            raise IndexError(
                f"Position {position} is out of bounds for list of size {self._size}. "
                f"Valid insertion range is [0, {self._size}]."
            )

        if position == 0:
            self.insert_beginning(data)
            return

        if position == self._size:
            self.insert_end(data)
            return

        new_node = CircularNode(data)
        current = self.head
        for _ in range(position - 1):
            assert current is not None
            current = current.next

        assert current is not None
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def delete_beginning(self) -> Any:
        """
        Deletes and returns data from the head node.
        Updates the last node's next pointer to point to the new head.

        Raises:
            IndexError: If list is empty.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None:
            raise IndexError("Cannot delete from an empty circular linked list.")

        deleted_data = self.head.data

        # Single-node circular cycle
        if self.head.next == self.head:
            self.head = None
        else:
            # Locate last node
            last = self.head
            while last.next != self.head:
                assert last.next is not None
                last = last.next

            last.next = self.head.next
            self.head = self.head.next

        self._size -= 1
        return deleted_data

    def delete_end(self) -> Any:
        """
        Deletes and returns data from the last node.
        Updates the second-to-last node's next pointer to point to head.

        Raises:
            IndexError: If list is empty.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None:
            raise IndexError("Cannot delete from an empty circular linked list.")

        # Single-node circular cycle
        if self.head.next == self.head:
            deleted_data = self.head.data
            self.head = None
            self._size -= 1
            return deleted_data

        # Traverse to second-to-last node
        current = self.head
        while current.next is not None and current.next.next != self.head:
            current = current.next

        assert current.next is not None
        deleted_data = current.next.data
        current.next = self.head
        self._size -= 1
        return deleted_data

    def delete_at_position(self, position: int) -> Any:
        """
        Deletes and returns data from the node at the specified zero-based position.

        Args:
            position: Zero-based position in range [0, len(self) - 1].

        Raises:
            TypeError: If position is not an integer.
            IndexError: If list is empty or position is out of bounds.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if not isinstance(position, int):
            raise TypeError("Position must be an integer.")

        if self.head is None:
            raise IndexError("Cannot delete from an empty circular linked list.")

        if position < 0 or position >= self._size:
            raise IndexError(
                f"Position {position} is out of bounds for list of size {self._size}. "
                f"Valid deletion range is [0, {self._size - 1}]."
            )

        if position == 0:
            return self.delete_beginning()

        if position == self._size - 1:
            return self.delete_end()

        current = self.head
        for _ in range(position - 1):
            assert current is not None
            current = current.next

        assert current is not None and current.next is not None
        deleted_node = current.next
        deleted_data = deleted_node.data
        current.next = deleted_node.next
        self._size -= 1
        return deleted_data

    def search(self, value: Any) -> int:
        """
        Searches for the first occurrence of 'value' in the circular list.

        Returns:
            Zero-based integer index, or -1 if value is not present.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None:
            return -1

        current = self.head
        index = 0
        while True:
            if current.data == value:
                return index
            current = current.next
            index += 1
            if current == self.head:
                break
        return -1

    def reverse(self) -> None:
        """
        Reverses the circular linked list in-place.

        Algorithm:
            If list has 0 or 1 nodes, nothing to reverse.
            Otherwise:
            1. Keep reference to original head (which will become the new tail).
            2. Reverse next pointers of all nodes in the cycle.
            3. The last node becomes the new head.
            4. Update the original head's next pointer to point to the new head.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None or self.head.next == self.head:
            return

        prev: Optional[CircularNode] = None
        current = self.head
        original_head = self.head

        # Traverse once around the ring
        while True:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
            if current == original_head:
                break

        # 'prev' is now the new head (former last node)
        # original_head is now the tail; link it to new head
        original_head.next = prev
        self.head = prev

    def concatenate(self, other: "CircularLinkedList") -> None:
        """
        Concatenates another CircularLinkedList to the end of this list.
        Clones all nodes from 'other' to preserve independent circular cycles.

        Args:
            other: CircularLinkedList instance to append.

        Raises:
            TypeError: If other is not a CircularLinkedList.

        Time Complexity: O(m) where m = len(other)
        Auxiliary Space Complexity: O(m) for copied nodes
        """
        if not isinstance(other, CircularLinkedList):
            raise TypeError("Argument must be an instance of CircularLinkedList.")

        if other.head is None:
            return

        other_current = other.head
        while True:
            self.insert_end(other_current.data)
            other_current = other_current.next
            if other_current == other.head:
                break

    def to_list(self) -> List[Any]:
        """
        Traverses the circular list exactly once and returns elements as a Python list.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        result: List[Any] = []
        if self.head is None:
            return result

        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break
        return result

    def display(self) -> str:
        """
        Returns a human-readable visual representation of the circular linked list:
        "10 -> 20 -> 30 -> (circular back to 10)" or "Empty Circular List"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.head is None:
            return "Empty Circular List"

        elements: List[str] = []
        current = self.head
        while True:
            elements.append(str(current.data))
            current = current.next
            if current == self.head:
                break

        return " -> ".join(elements) + f" -> (circular back to {self.head.data})"

    def __str__(self) -> str:
        return self.display()


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive tests covering all CircularLinkedList operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Circular Linked List (Program 03)")
    print("=" * 65)

    cll = CircularLinkedList()

    # 1. Empty list state
    assert cll.is_empty() is True
    assert len(cll) == 0
    assert cll.to_list() == []
    assert cll.display() == "Empty Circular List"
    assert cll.search(42) == -1
    print("  [Test 01 Passed] Initialized empty circular linked list.")

    # Boundary deletions on empty list
    try:
        cll.delete_beginning()
        assert False, "Should raise IndexError on empty delete_beginning"
    except IndexError:
        print("  [Test 02 Passed] Caught delete_beginning on empty list.")

    try:
        cll.delete_end()
        assert False, "Should raise IndexError on empty delete_end"
    except IndexError:
        print("  [Test 03 Passed] Caught delete_end on empty list.")

    # 2. Single-node operations
    cll.insert_beginning(100)
    assert len(cll) == 1
    assert cll.head is not None
    assert cll.head.next == cll.head  # Points to itself
    assert cll.to_list() == [100]
    print("  [Test 04 Passed] Single node insertion and self-referential cycle verified.")

    # Single-node deletion
    val = cll.delete_beginning()
    assert val == 100
    assert cll.is_empty() is True
    assert cll.head is None
    print("  [Test 05 Passed] Single node deletion leaving empty list verified.")

    # Single-node delete_end
    cll.insert_end(200)
    assert cll.head is not None and cll.head.next == cll.head
    val = cll.delete_end()
    assert val == 200
    assert cll.is_empty() is True
    print("  [Test 06 Passed] Single node delete_end verified.")

    # 3. Multiple insertions
    cll.insert_beginning(20)  # [20]
    cll.insert_beginning(10)  # [10, 20]
    cll.insert_end(40)        # [10, 20, 40]
    cll.insert_at_position(30, 2)  # [10, 20, 30, 40]
    cll.insert_at_position(5, 0)   # [5, 10, 20, 30, 40]
    cll.insert_at_position(50, 5)  # [5, 10, 20, 30, 40, 50]

    assert cll.to_list() == [5, 10, 20, 30, 40, 50]
    assert len(cll) == 6
    print("  [Test 07 Passed] Insertions (beginning, middle, end) verified.")

    # Circular termination check: walk 6 steps and ensure it wraps to head
    walk = cll.head
    for _ in range(6):
        assert walk is not None
        walk = walk.next
    assert walk == cll.head
    print("  [Test 08 Passed] Circular cycle closure verified (no infinite loop).")

    # 4. Search
    assert cll.search(5) == 0
    assert cll.search(30) == 3
    assert cll.search(50) == 5
    assert cll.search(999) == -1
    print("  [Test 09 Passed] Search for present and missing values verified.")

    # 5. Deletions
    # Delete beginning
    assert cll.delete_beginning() == 5  # [10, 20, 30, 40, 50]
    assert cll.to_list() == [10, 20, 30, 40, 50]

    # Delete end
    assert cll.delete_end() == 50        # [10, 20, 30, 40]
    assert cll.to_list() == [10, 20, 30, 40]

    # Delete at position 2 (value 30)
    assert cll.delete_at_position(2) == 30  # [10, 20, 40]
    assert cll.to_list() == [10, 20, 40]
    print("  [Test 10 Passed] Deletions with cycle restoration verified.")

    # 6. In-place Reversal
    cll.reverse()  # [40, 20, 10]
    assert cll.to_list() == [40, 20, 10]
    assert cll.head is not None and cll.head.data == 40

    # Ensure reversed ring is circular
    walk = cll.head
    for _ in range(3):
        assert walk is not None
        walk = walk.next
    assert walk == cll.head

    cll.reverse()  # Back to [10, 20, 40]
    assert cll.to_list() == [10, 20, 40]
    print("  [Test 11 Passed] In-place circular reversal verified.")

    # 7. Concatenation
    other = CircularLinkedList()
    other.insert_end(50)
    other.insert_end(60)

    cll.concatenate(other)
    assert cll.to_list() == [10, 20, 40, 50, 60]
    assert other.to_list() == [50, 60]  # Other intact

    # Verify combined ring is circular
    walk = cll.head
    for _ in range(5):
        assert walk is not None
        walk = walk.next
    assert walk == cll.head
    print("  [Test 12 Passed] Circular list concatenation verified.")

    print("\nAll Program 03 automated tests PASSED successfully!")


def demonstrate() -> None:
    """Demonstrates Circular Linked List operations with visual console logging."""
    print("\n" + "=" * 65)
    print("DEMONSTRATION: Circular Linked List (Program 03)")
    print("=" * 65)

    cll = CircularLinkedList()
    print("1. Inserting into Circular Linked List:")
    cll.insert_beginning(20)
    cll.insert_beginning(10)
    cll.insert_end(40)
    cll.insert_at_position(30, 2)
    print(f"   List State: {cll}")

    print("\n2. Searching elements in circular ring:")
    for key in (30, 88):
        idx = cll.search(key)
        print(f"   search({key}) -> {'Found at index ' + str(idx) if idx != -1 else 'Not Found'}")

    print("\n3. Deleting elements from circular ring:")
    print(f"   delete_beginning() -> Removed {cll.delete_beginning()}")
    print(f"   delete_end()       -> Removed {cll.delete_end()}")
    print(f"   Current List: {cll}")

    print("\n4. In-Place Circular Reversal:")
    cll.insert_end(50)
    cll.insert_end(60)
    print(f"   Before Reversal : {cll}")
    cll.reverse()
    print(f"   After Reversal  : {cll}")

    print("\n5. Concatenating two circular linked lists:")
    other = CircularLinkedList()
    other.insert_end(70)
    other.insert_end(80)
    print(f"   List A : {cll}")
    print(f"   List B : {other}")
    cll.concatenate(other)
    print(f"   Combined List A : {cll}")


if __name__ == "__main__":
    run_tests()
    demonstrate()

