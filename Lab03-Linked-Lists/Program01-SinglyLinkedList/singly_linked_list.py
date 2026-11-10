"""
Program 01: Singly Linked List
Course: IC-307D Data Structures and Algorithms Lab
Unit 3: Linked Lists (CO1)

This program implements a Singly Linked List from first principles:
- Node class containing 'data' and 'next' pointer reference.
- SinglyLinkedList class with comprehensive insertion, deletion, traversal,
  search, reversal, and concatenation operations.
- Zero-based indexing:
    Position 0 corresponds to the head node.
    Position k corresponds to the node reached after k 'next' traversals from head.
    Valid insertion positions: 0 <= position <= length (position == length appends).
    Valid deletion positions: 0 <= position < length.
- Pure node references without using Python list as the underlying storage.
- Full input validation, boundary checking, and custom exception handling.
"""

from typing import Any, List, Optional


class Node:
    """
    Represents an individual node in a Singly Linked List.

    Attributes:
        data: The payload or value stored in the node.
        next: Pointer/reference to the next Node, or None if terminal.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class SinglyLinkedList:
    """
    Singly Linked List data structure.

    Zero-based Indexing Convention:
        Index 0 represents the head node.
        Index 1 represents the node immediately following head, and so on.
        For a list of length n:
          - Valid retrieval/deletion indices are in the range [0, n - 1].
          - Valid insertion indices are in the range [0, n] (where n represents appending to the end).
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Checks whether the linked list is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self.head is None

    def __len__(self) -> int:
        """
        Returns the number of nodes in the linked list.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._size

    def insert_beginning(self, data: Any) -> None:
        """
        Inserts a new node containing 'data' at the beginning (head) of the list.

        Algorithm:
            1. Allocate a new Node with the given data.
            2. Set new_node.next to the current head.
            3. Update head to point to new_node.
            4. Increment size by 1.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_end(self, data: Any) -> None:
        """
        Inserts a new node containing 'data' at the end (tail) of the list.

        Algorithm:
            1. Allocate a new Node with the given data.
            2. If list is empty, set head = new_node.
            3. Otherwise, traverse from head to the last node (where current.next is None).
            4. Set last_node.next = new_node.
            5. Increment size by 1.

        Time Complexity: O(n) where n is the number of nodes.
        Auxiliary Space Complexity: O(1)
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at_position(self, data: Any, position: int) -> None:
        """
        Inserts a new node containing 'data' at the specified zero-based position.

        Args:
            data: The value to insert.
            position: Zero-based integer index where 0 <= position <= len(self).

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

        new_node = Node(data)
        current = self.head
        # Traverse to node at (position - 1)
        for _ in range(position - 1):
            assert current is not None
            current = current.next

        assert current is not None
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def delete_beginning(self) -> Any:
        """
        Deletes and returns the data of the first (head) node.

        Raises:
            IndexError: If attempting to delete from an empty list.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None:
            raise IndexError("Cannot delete from an empty linked list.")

        deleted_data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return deleted_data

    def delete_end(self) -> Any:
        """
        Deletes and returns the data of the last node in the list.

        Raises:
            IndexError: If attempting to delete from an empty list.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None:
            raise IndexError("Cannot delete from an empty linked list.")

        # Single-node case
        if self.head.next is None:
            deleted_data = self.head.data
            self.head = None
            self._size -= 1
            return deleted_data

        # Traverse to second-to-last node
        current = self.head
        while current.next is not None and current.next.next is not None:
            current = current.next

        assert current.next is not None
        deleted_data = current.next.data
        current.next = None
        self._size -= 1
        return deleted_data

    def delete_at_position(self, position: int) -> Any:
        """
        Deletes and returns the data of the node at the specified zero-based position.

        Args:
            position: Zero-based integer index where 0 <= position < len(self).

        Raises:
            TypeError: If position is not an integer.
            IndexError: If list is empty or position is out of bounds.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if not isinstance(position, int):
            raise TypeError("Position must be an integer.")

        if self.head is None:
            raise IndexError("Cannot delete from an empty linked list.")

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
        Searches for the first occurrence of 'value' in the linked list.

        Returns:
            Zero-based integer index of first matching node, or -1 if not found.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        current = self.head
        index = 0
        while current is not None:
            if current.data == value:
                return index
            current = current.next
            index += 1
        return -1

    def reverse(self) -> None:
        """
        Reverses the linked list in-place by updating pointer directions.

        Algorithm:
            Maintain three pointers:
            - prev: Initially None.
            - current: Initially head.
            - next_node: Temporarily stores current.next before reversing.
            In each step:
                next_node = current.next
                current.next = prev
                prev = current
                current = next_node
            Finally, update head = prev.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        prev: Optional[Node] = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def concatenate(self, other: "SinglyLinkedList") -> None:
        """
        Concatenates another SinglyLinkedList to the end of this list.
        Clones nodes from 'other' to preserve independent data integrity.

        Args:
            other: Another SinglyLinkedList instance.

        Raises:
            TypeError: If other is not an instance of SinglyLinkedList.

        Time Complexity: O(n + m) where n = len(self), m = len(other).
        Auxiliary Space Complexity: O(m) for the new copied nodes.
        """
        if not isinstance(other, SinglyLinkedList):
            raise TypeError("Argument must be an instance of SinglyLinkedList.")

        if other.head is None:
            return

        # Deep copy nodes from other list so neither list mutates the other
        other_current = other.head
        while other_current is not None:
            self.insert_end(other_current.data)
            other_current = other_current.next

    def to_list(self) -> List[Any]:
        """
        Converts the linked list into a standard Python list (for display/testing).

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        result: List[Any] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def display(self) -> str:
        """
        Returns a human-readable visual representation of the linked list.
        Example: "10 -> 20 -> 30 -> None" or "Empty List"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.head is None:
            return "Empty List"

        elements: List[str] = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        elements.append("None")
        return " -> ".join(elements)

    def __str__(self) -> str:
        return self.display()


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive unit tests covering all SinglyLinkedList operations."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Singly Linked List (Program 01)")
    print("=" * 65)

    sll = SinglyLinkedList()

    # 1. Empty list operations
    assert sll.is_empty() is True
    assert len(sll) == 0
    assert sll.display() == "Empty List"
    assert sll.search(99) == -1
    print("  [Test 01 Passed] Initialized empty list successfully.")

    # Boundary deletions on empty list
    try:
        sll.delete_beginning()
        assert False, "Should raise IndexError on empty delete_beginning"
    except IndexError:
        print("  [Test 02 Passed] Caught delete_beginning on empty list.")

    try:
        sll.delete_end()
        assert False, "Should raise IndexError on empty delete_end"
    except IndexError:
        print("  [Test 03 Passed] Caught delete_end on empty list.")

    try:
        sll.delete_at_position(0)
        assert False, "Should raise IndexError on empty delete_at_position"
    except IndexError:
        print("  [Test 04 Passed] Caught delete_at_position on empty list.")

    # 2. Insertions
    sll.insert_beginning(20)  # [20]
    assert sll.to_list() == [20]
    assert len(sll) == 1
    assert sll.is_empty() is False

    sll.insert_beginning(10)  # [10, 20]
    assert sll.to_list() == [10, 20]

    sll.insert_end(40)        # [10, 20, 40]
    assert sll.to_list() == [10, 20, 40]

    # Insert at middle position
    sll.insert_at_position(30, 2)  # [10, 20, 30, 40]
    assert sll.to_list() == [10, 20, 30, 40]

    # Insert at position 0 (beginning)
    sll.insert_at_position(5, 0)   # [5, 10, 20, 30, 40]
    assert sll.to_list() == [5, 10, 20, 30, 40]

    # Insert at position len (end)
    sll.insert_at_position(50, 5)  # [5, 10, 20, 30, 40, 50]
    assert sll.to_list() == [5, 10, 20, 30, 40, 50]
    assert len(sll) == 6
    print("  [Test 05 Passed] Insertions (beginning, middle, end) verified.")

    # Invalid insertion positions
    try:
        sll.insert_at_position(99, -1)
        assert False, "Should raise IndexError for negative position"
    except IndexError:
        print("  [Test 06 Passed] Caught negative position insertion.")

    try:
        sll.insert_at_position(99, 100)
        assert False, "Should raise IndexError for out-of-range position"
    except IndexError:
        print("  [Test 07 Passed] Caught out-of-range position insertion.")

    # 3. Searching
    assert sll.search(5) == 0
    assert sll.search(30) == 3
    assert sll.search(50) == 5
    assert sll.search(999) == -1
    print("  [Test 08 Passed] Search for present and missing values verified.")

    # 4. Deletions
    # Delete from beginning
    val = sll.delete_beginning()  # removes 5 -> [10, 20, 30, 40, 50]
    assert val == 5
    assert sll.to_list() == [10, 20, 30, 40, 50]

    # Delete from end
    val = sll.delete_end()        # removes 50 -> [10, 20, 30, 40]
    assert val == 50
    assert sll.to_list() == [10, 20, 30, 40]

    # Delete at middle position
    val = sll.delete_at_position(1)  # removes 20 at index 1 -> [10, 30, 40]
    assert val == 20
    assert sll.to_list() == [10, 30, 40]
    assert len(sll) == 3
    print("  [Test 09 Passed] Deletions (beginning, middle, end) verified.")

    # 5. In-place Reversal
    sll.reverse()  # [40, 30, 10]
    assert sll.to_list() == [40, 30, 10]
    sll.reverse()  # back to [10, 30, 40]
    assert sll.to_list() == [10, 30, 40]
    print("  [Test 10 Passed] In-place reversal verified.")

    # Single-node reversal
    single = SinglyLinkedList()
    single.insert_beginning(100)
    single.reverse()
    assert single.to_list() == [100]
    print("  [Test 11 Passed] Single-node list reversal verified.")

    # 6. Concatenation
    list_a = SinglyLinkedList()
    list_a.insert_end(1)
    list_a.insert_end(2)

    list_b = SinglyLinkedList()
    list_b.insert_end(3)
    list_b.insert_end(4)

    list_a.concatenate(list_b)
    assert list_a.to_list() == [1, 2, 3, 4]
    assert list_b.to_list() == [3, 4]  # list_b intact
    assert len(list_a) == 4

    # Concatenate empty list
    empty_list = SinglyLinkedList()
    list_a.concatenate(empty_list)
    assert list_a.to_list() == [1, 2, 3, 4]

    # Concatenate to empty list
    empty_target = SinglyLinkedList()
    empty_target.concatenate(list_a)
    assert empty_target.to_list() == [1, 2, 3, 4]
    print("  [Test 12 Passed] List concatenation verified.")

    print("\nAll Program 01 automated tests PASSED successfully!")


def demonstrate() -> None:
    """Interactive / visual demonstration of Singly Linked List operations."""
    print("\n" + "=" * 65)
    print("DEMONSTRATION: Singly Linked List (Program 01)")
    print("=" * 65)

    sll = SinglyLinkedList()
    print("1. Created an empty Singly Linked List.")
    print(f"   Current List: {sll}")

    print("\n2. Inserting elements:")
    sll.insert_beginning(20)
    print(f"   insert_beginning(20) : {sll}")
    sll.insert_beginning(10)
    print(f"   insert_beginning(10) : {sll}")
    sll.insert_end(40)
    print(f"   insert_end(40)       : {sll}")
    sll.insert_at_position(30, 2)
    print(f"   insert_at_position(30, pos=2): {sll}")

    print("\n3. Searching in the list:")
    for target in [30, 99]:
        idx = sll.search(target)
        if idx != -1:
            print(f"   search({target}) -> Found at zero-based index {idx}")
        else:
            print(f"   search({target}) -> Not Found (returned -1)")

    print("\n4. Deleting elements:")
    del_val = sll.delete_beginning()
    print(f"   delete_beginning() -> Removed {del_val} : {sll}")
    del_val = sll.delete_end()
    print(f"   delete_end()       -> Removed {del_val} : {sll}")
    del_val = sll.delete_at_position(0)
    print(f"   delete_at_position(0) -> Removed {del_val} : {sll}")

    print("\n5. Reversal:")
    sll.insert_end(50)
    sll.insert_end(60)
    sll.insert_end(70)
    print(f"   Before reversal: {sll}")
    sll.reverse()
    print(f"   After reversal : {sll}")

    print("\n6. Concatenation:")
    other = SinglyLinkedList()
    other.insert_end(80)
    other.insert_end(90)
    print(f"   List A: {sll}")
    print(f"   List B: {other}")
    sll.concatenate(other)
    print(f"   Concatenated List A: {sll}")


if __name__ == "__main__":
    run_tests()
    demonstrate()

