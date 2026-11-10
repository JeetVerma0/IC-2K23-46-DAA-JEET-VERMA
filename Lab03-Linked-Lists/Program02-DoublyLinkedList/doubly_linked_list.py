"""
Program 02: Doubly Linked List
Course: IC-307D Data Structures and Algorithms Lab
Unit 3: Linked Lists (CO1)

This program implements a Doubly Linked List from first principles:
- Node class containing 'data', 'prev' (previous), and 'next' pointer references.
- DoublyLinkedList maintaining both 'head' and 'tail' references for optimal O(1)
  endpoints operations.
- Full bidirectional traversal (forward and backward).
- In-place reversal by swapping 'next' and 'prev' pointers for all nodes.
- Concatenation of two doubly linked lists with full bidirectional pointer linking.
- Rigorous handling of edge cases (empty list, single-node list, head/tail boundaries).
- Time and space complexity annotations for every operation.
"""

from typing import Any, List, Optional


class DoublyNode:
    """
    Represents an individual node in a Doubly Linked List.

    Attributes:
        data: The payload or value stored in the node.
        prev: Pointer/reference to the preceding Node (or None if head).
        next: Pointer/reference to the succeeding Node (or None if tail).
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.prev: Optional["DoublyNode"] = None
        self.next: Optional["DoublyNode"] = None

    def __repr__(self) -> str:
        return f"DoublyNode({self.data})"


class DoublyLinkedList:
    """
    Doubly Linked List data structure.

    Zero-based Indexing Convention:
        Index 0 represents the head node.
        Index n - 1 represents the tail node.
        Valid insertion indices: [0, n] where position == n appends to the tail.
        Valid deletion indices: [0, n - 1].
    """

    def __init__(self) -> None:
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Checks whether the doubly linked list is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self.head is None

    def __len__(self) -> int:
        """
        Returns the number of nodes in the list.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        return self._size

    def insert_beginning(self, data: Any) -> None:
        """
        Inserts a new node at the beginning (head) of the list.

        Algorithm:
            1. Create new node with 'data'.
            2. If list is empty: head = tail = new_node.
            3. Else:
               new_node.next = head
               head.prev = new_node
               head = new_node
            4. Increment size by 1.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_end(self, data: Any) -> None:
        """
        Inserts a new node at the end (tail) of the list.

        Algorithm:
            1. Create new node with 'data'.
            2. If list is empty: head = tail = new_node.
            3. Else:
               tail.next = new_node
               new_node.prev = tail
               tail = new_node
            4. Increment size by 1.

        Time Complexity: O(1) (leveraging tail reference)
        Auxiliary Space Complexity: O(1)
        """
        new_node = DoublyNode(data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def insert_at_position(self, data: Any, position: int) -> None:
        """
        Inserts a new node at the specified zero-based position.

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

        new_node = DoublyNode(data)

        # Optimize traversal direction: search from head or tail depending on position
        if position <= self._size // 2:
            current = self.head
            for _ in range(position):
                assert current is not None
                current = current.next
        else:
            current = self.tail
            for _ in range(self._size - 1 - position):
                assert current is not None
                current = current.prev

        # Insert new_node before current
        assert current is not None and current.prev is not None
        prev_node = current.prev

        new_node.next = current
        new_node.prev = prev_node
        prev_node.next = new_node
        current.prev = new_node

        self._size += 1

    def delete_beginning(self) -> Any:
        """
        Deletes and returns data from the head node.

        Raises:
            IndexError: If list is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None:
            raise IndexError("Cannot delete from an empty doubly linked list.")

        deleted_data = self.head.data

        # Single-node case
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            assert self.head is not None
            self.head.prev = None

        self._size -= 1
        return deleted_data

    def delete_end(self) -> Any:
        """
        Deletes and returns data from the tail node.

        Raises:
            IndexError: If list is empty.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.tail is None:
            raise IndexError("Cannot delete from an empty doubly linked list.")

        deleted_data = self.tail.data

        # Single-node case
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            assert self.tail is not None
            self.tail.next = None

        self._size -= 1
        return deleted_data

    def delete_at_position(self, position: int) -> Any:
        """
        Deletes and returns data from the specified zero-based position.

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
            raise IndexError("Cannot delete from an empty doubly linked list.")

        if position < 0 or position >= self._size:
            raise IndexError(
                f"Position {position} is out of bounds for list of size {self._size}. "
                f"Valid deletion range is [0, {self._size - 1}]."
            )

        if position == 0:
            return self.delete_beginning()

        if position == self._size - 1:
            return self.delete_end()

        # Traverse to target node
        if position <= self._size // 2:
            current = self.head
            for _ in range(position):
                assert current is not None
                current = current.next
        else:
            current = self.tail
            for _ in range(self._size - 1 - position):
                assert current is not None
                current = current.prev

        assert current is not None
        assert current.prev is not None and current.next is not None

        deleted_data = current.data
        current.prev.next = current.next
        current.next.prev = current.prev

        self._size -= 1
        return deleted_data

    def search(self, value: Any) -> int:
        """
        Searches for the first occurrence of 'value' in forward order.

        Returns:
            Zero-based integer index, or -1 if value is not present.

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
        Reverses the doubly linked list in-place by swapping 'next' and 'prev'
        references for every node, and swapping the 'head' and 'tail' pointers.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.head is None or self.head == self.tail:
            return  # Empty or single-node list is trivially reversed

        current = self.head
        new_tail = self.head

        while current is not None:
            # Swap next and prev pointers
            current.prev, current.next = current.next, current.prev
            # Move to the original next node (which is now in current.prev)
            current = current.prev

        # The previous tail becomes the new head
        self.head = self.tail
        self.tail = new_tail

    def concatenate(self, other: "DoublyLinkedList") -> None:
        """
        Concatenates another DoublyLinkedList to the end of this list.
        Clones all nodes from 'other' to maintain independent lists with
        correct forward and backward pointers.

        Args:
            other: DoublyLinkedList instance to append.

        Raises:
            TypeError: If other is not a DoublyLinkedList.

        Time Complexity: O(m) where m = len(other)
        Auxiliary Space Complexity: O(m) for newly created nodes
        """
        if not isinstance(other, DoublyLinkedList):
            raise TypeError("Argument must be an instance of DoublyLinkedList.")

        if other.head is None:
            return

        other_current = other.head
        while other_current is not None:
            self.insert_end(other_current.data)
            other_current = other_current.next

    def to_list_forward(self) -> List[Any]:
        """
        Returns elements traversed from head to tail as a Python list.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        result: List[Any] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_backward(self) -> List[Any]:
        """
        Returns elements traversed from tail to head as a Python list.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        result: List[Any] = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result

    def display_forward(self) -> str:
        """
        Returns forward string representation: "None <- 10 <=> 20 <=> 30 -> None"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.head is None:
            return "Empty Doubly Linked List"

        elements: List[str] = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        return "None <- " + " <=> ".join(elements) + " -> None"

    def display_backward(self) -> str:
        """
        Returns backward string representation: "None <- 30 <=> 20 <=> 10 -> None"

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(n)
        """
        if self.tail is None:
            return "Empty Doubly Linked List"

        elements: List[str] = []
        current = self.tail
        while current is not None:
            elements.append(str(current.data))
            current = current.prev
        return "None <- " + " <=> ".join(elements) + " -> None"

    def __str__(self) -> str:
        return self.display_forward()


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive tests covering all DoublyLinkedList operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Doubly Linked List (Program 02)")
    print("=" * 65)

    dll = DoublyLinkedList()

    # 1. Empty list state
    assert dll.is_empty() is True
    assert len(dll) == 0
    assert dll.to_list_forward() == []
    assert dll.to_list_backward() == []
    assert dll.search(10) == -1
    print("  [Test 01 Passed] Initialized empty doubly linked list.")

    # Boundary deletions on empty list
    try:
        dll.delete_beginning()
        assert False, "Should raise IndexError"
    except IndexError:
        print("  [Test 02 Passed] Caught delete_beginning on empty list.")

    try:
        dll.delete_end()
        assert False, "Should raise IndexError"
    except IndexError:
        print("  [Test 03 Passed] Caught delete_end on empty list.")

    # 2. Single node insertions and pointer integrity
    dll.insert_beginning(100)
    assert len(dll) == 1
    assert dll.head is not None and dll.tail is not None
    assert dll.head == dll.tail
    assert dll.head.prev is None and dll.head.next is None
    assert dll.to_list_forward() == [100]
    assert dll.to_list_backward() == [100]
    print("  [Test 04 Passed] Single node insertion and pointer symmetry verified.")

    # Single node deletion
    val = dll.delete_end()
    assert val == 100
    assert dll.is_empty() is True
    assert dll.head is None and dll.tail is None
    print("  [Test 05 Passed] Single node deletion leaving empty list verified.")

    # 3. Multiple insertions
    dll.insert_beginning(20)  # [20]
    dll.insert_beginning(10)  # [10, 20]
    dll.insert_end(40)        # [10, 20, 40]
    dll.insert_at_position(30, 2)  # [10, 20, 30, 40]
    dll.insert_at_position(5, 0)   # [5, 10, 20, 30, 40]
    dll.insert_at_position(50, 5)  # [5, 10, 20, 30, 40, 50]

    assert dll.to_list_forward() == [5, 10, 20, 30, 40, 50]
    assert dll.to_list_backward() == [50, 40, 30, 20, 10, 5]
    assert len(dll) == 6
    print("  [Test 06 Passed] Insertions and bidirectional traversals verified.")

    # 4. Search
    assert dll.search(5) == 0
    assert dll.search(30) == 3
    assert dll.search(50) == 5
    assert dll.search(999) == -1
    print("  [Test 07 Passed] Search for present and absent keys verified.")

    # 5. Deletions at boundaries and intermediate positions
    # Delete beginning
    assert dll.delete_beginning() == 5
    assert dll.head is not None and dll.head.prev is None
    assert dll.to_list_forward() == [10, 20, 30, 40, 50]

    # Delete end
    assert dll.delete_end() == 50
    assert dll.tail is not None and dll.tail.next is None
    assert dll.to_list_forward() == [10, 20, 30, 40]

    # Delete at position 2 (value 30)
    assert dll.delete_at_position(2) == 30
    assert dll.to_list_forward() == [10, 20, 40]
    assert dll.to_list_backward() == [40, 20, 10]
    print("  [Test 08 Passed] Deletions with bidirectional pointer checks verified.")

    # 6. In-place Reversal
    dll.reverse()
    assert dll.to_list_forward() == [40, 20, 10]
    assert dll.to_list_backward() == [10, 20, 40]
    assert dll.head is not None and dll.head.data == 40 and dll.head.prev is None
    assert dll.tail is not None and dll.tail.data == 10 and dll.tail.next is None

    dll.reverse()
    assert dll.to_list_forward() == [10, 20, 40]
    assert dll.to_list_backward() == [40, 20, 10]
    print("  [Test 09 Passed] In-place reversal and pointer integrity verified.")

    # 7. Concatenation
    other = DoublyLinkedList()
    other.insert_end(50)
    other.insert_end(60)

    dll.concatenate(other)
    assert dll.to_list_forward() == [10, 20, 40, 50, 60]
    assert dll.to_list_backward() == [60, 50, 40, 20, 10]
    assert dll.tail is not None and dll.tail.data == 60 and dll.tail.next is None
    assert other.to_list_forward() == [50, 60]  # Original other intact
    print("  [Test 10 Passed] Concatenation with backward pointer integrity verified.")

    print("\nAll Program 02 automated tests PASSED successfully!")


def demonstrate() -> None:
    """Demonstrates Doubly Linked List operations with visual console logging."""
    print("\n" + "=" * 65)
    print("DEMONSTRATION: Doubly Linked List (Program 02)")
    print("=" * 65)

    dll = DoublyLinkedList()
    print("1. Inserting into Doubly Linked List:")
    dll.insert_beginning(20)
    dll.insert_beginning(10)
    dll.insert_end(40)
    dll.insert_at_position(30, 2)
    print(f"   Forward  : {dll.display_forward()}")
    print(f"   Backward : {dll.display_backward()}")

    print("\n2. Searching elements:")
    for key in (30, 99):
        idx = dll.search(key)
        print(f"   search({key}) -> {'Found at index ' + str(idx) if idx != -1 else 'Not Found'}")

    print("\n3. Deleting elements:")
    print(f"   delete_beginning() -> Removed {dll.delete_beginning()}")
    print(f"   delete_end()       -> Removed {dll.delete_end()}")
    print(f"   Current List: {dll.display_forward()}")

    print("\n4. In-Place Reversal:")
    dll.insert_end(50)
    dll.insert_end(60)
    print(f"   Before Reversal : {dll.display_forward()}")
    dll.reverse()
    print(f"   After Reversal  : {dll.display_forward()}")
    print(f"   Reversed Backw. : {dll.display_backward()}")

    print("\n5. Concatenation:")
    list_b = DoublyLinkedList()
    list_b.insert_end(70)
    list_b.insert_end(80)
    print(f"   List A : {dll.display_forward()}")
    print(f"   List B : {list_b.display_forward()}")
    dll.concatenate(list_b)
    print(f"   Combined List A : {dll.display_forward()}")
    print(f"   Combined Backw. : {dll.display_backward()}")


if __name__ == "__main__":
    run_tests()
    demonstrate()

